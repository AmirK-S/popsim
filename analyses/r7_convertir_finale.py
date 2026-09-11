"""Préflight par défaut; --execute convertit uniquement le final R7 local figé.

Refuse R2b/serveurs/conversions actifs. Aucun téléchargement. Écrit une nouvelle
session cache (GGUF temporaire, log, provenance), jamais le GGUF original.
SHA sources et validation GGUF obligatoires. Aucun serveur n'est lancé.
"""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import struct
import subprocess
import tempfile
import time

from r7_valider_gguf import CACHE, validate

REV = '6e5971d9eba42665f5bd5a0fcf047f299ce1dccc'
COMMIT = 'c1d0e7a004015f23bc0233470b747b596f29b264'
SNAPSHOT = CACHE/'hf-cache/hub/models--allenai--Olmo-3-7B-Instruct/snapshots'/REV
REPO = CACHE/'outils/llama.cpp'
PYTHON = CACHE/'outils/venv-conversion/bin/python'
# OID LFS et tailles de l'API officielle à REV, vérifiés le 10/09/2026.
SHARDS = {
    'model-00001-of-00003.safetensors': (4969984976, 'e7bd4c8ba52177a815aee5929cb458a116a65799688d3e51402500a1cb77023c'),
    'model-00002-of-00003.safetensors': (4981161496, 'ea92aa0499a2ca02400e5d87324009e172bdbfb9809f2ac501485d8224382328'),
    'model-00003-of-00003.safetensors': (4644917240, 'd50f95e4f2ec5fc4fbce6217cbf54fd1d700928b05e5550c8ee08bf4ba948925'),
}


def blockers():
    # Aucun appel au serveur. ps non disponible => exception, refus conservateur.
    lines = subprocess.check_output(['ps', '-axo', 'pid=,comm=,args='], text=True).splitlines()
    found = []
    for line in lines:
        parts = line.strip().split(None, 2)
        if len(parts) != 3:
            continue
        pid, comm, args = parts
        if int(pid) == os.getpid():
            continue
        # macOS tronque comm à 15 caractères; args conserve l'exécutable.
        executable = Path(args.split(None, 1)[0]).name
        if executable == 'llama-server' or (executable.lower().startswith(('python', 'pypy')) and
                any(x in args for x in ('r2b_extension.py', 'r2_rares_apparie.py', 'convert_hf_to_gguf.py'))):
            found.append({'pid':int(pid), 'command':executable})
    return found


def require_idle():
    busy = blockers()
    if busy:
        raise RuntimeError(f'GPU/mémoire réservés à une autre tâche: {busy}')


def sha256(path, check_idle=False):
    h = hashlib.sha256()
    last = 0
    with Path(path).open('rb') as f:
        while True:
            if check_idle and time.monotonic()-last >= 1:
                require_idle()
                last = time.monotonic()
            chunk = f.read(4*1024**2)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


def preflight():
    head = subprocess.check_output(['git', '-C', str(REPO), 'rev-parse', 'HEAD'], text=True).strip()
    dirty = subprocess.check_output(['git', '-C', str(REPO), 'status', '--porcelain'], text=True).strip()
    if head != COMMIT or dirty:
        raise RuntimeError('convertisseur: mauvais commit ou checkout modifié')
    if not PYTHON.is_file():
        raise RuntimeError('Python de conversion absent')
    index = json.loads((SNAPSHOT/'model.safetensors.index.json').read_text())
    mapping = {}
    for name, (size, oid) in SHARDS.items():
        path = SNAPSHOT/name
        if path.stat().st_size != size or path.resolve().name != oid:
            raise RuntimeError(f'{name}: taille ou blob inattendu')
        with path.open('rb') as f:
            n = struct.unpack('<Q', f.read(8))[0]
            if n > 1024**2:
                raise RuntimeError('en-tête safetensors excessif')
            header = json.loads(f.read(n))
        ts = {k:v for k,v in header.items() if k != '__metadata__'}
        if not ts or 8+n+max(v['data_offsets'][1] for v in ts.values()) != size:
            raise RuntimeError(f'{name}: structure tronquée')
        for key, val in ts.items():
            if key in mapping or val['dtype'] != 'BF16':
                raise RuntimeError('tenseurs dupliqués ou non BF16')
            mapping[key] = name
    if len(mapping) != 355 or mapping != index['weight_map']:
        raise RuntimeError('index des shards incohérent')
    return {'revision':REV, 'converter_commit':head, 'source_tensor_count':len(mapping),
            'snapshot':str(SNAPSHOT), 'blockers':blockers(), 'mode':'preflight seulement'}


def run_converter(command, log):
    env = dict(os.environ, HF_HUB_OFFLINE='1', TRANSFORMERS_OFFLINE='1',
               HF_HUB_DISABLE_TELEMETRY='1', HF_HOME=str(CACHE/'hf-cache'),
               PYTHONDONTWRITEBYTECODE='1')
    require_idle()
    with log.open('x') as stream:
        process = subprocess.Popen(command, stdout=stream, stderr=subprocess.STDOUT, env=env)
        try:
            while process.poll() is None:
                # Ignore notre convertisseur, surveille uniquement les autres tâches.
                other = [b for b in blockers() if b['pid'] != process.pid]
                if other:
                    raise RuntimeError(f'autre tâche apparue; arrêt de NOTRE conversion: {other}')
                time.sleep(1)
            return process.returncode
        except BaseException:
            if process.poll() is None:
                process.terminate()
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    process.kill()
                    process.wait()
            raise


def convert(session):
    output = session/'Olmo-3-7B-rlvr-Q8_0.partial.gguf'
    command = [str(PYTHON), str(REPO/'convert_hf_to_gguf.py'), str(SNAPSHOT),
               '--outtype', 'q8_0', '--outfile', str(output)]
    record = {'started_utc':datetime.now(timezone.utc).isoformat(), 'status':'STARTED',
              'revision':REV, 'converter_commit':COMMIT, 'command':command,
              'output':str(output), 'original_untouched':str(CACHE/'gguf/Olmo-3-7B-rlvr-Q8_0.gguf'),
              'source_url':f'https://huggingface.co/api/models/allenai/Olmo-3-7B-Instruct/revision/{REV}?blobs=true',
              'shards':{}, 'scripts_sha256':{}, 'metadata_sha256':{}}
    provenance = session/'provenance.json'
    def save():
        provenance.write_text(json.dumps(record, ensure_ascii=False, indent=2)+'\n')
    save()
    try:
        if output.exists():
            raise RuntimeError('sortie déjà présente')
        record['preflight'] = preflight()
        require_idle()
        for p in (Path(__file__), Path(__file__).with_name('r7_valider_gguf.py'), REPO/'convert_hf_to_gguf.py'):
            record['scripts_sha256'][str(p)] = sha256(p)
        for p in sorted(SNAPSHOT.iterdir()):
            if p.suffix in ('.json', '.txt', '.model'):
                record['metadata_sha256'][p.name] = sha256(p)
        for name, (size, expected) in SHARDS.items():
            actual = sha256(SNAPSHOT/name, check_idle=True)
            record['shards'][name] = {'bytes':size, 'expected':expected, 'actual':actual}
            save()
            if actual != expected:
                raise RuntimeError(f'SHA-256 incorrect: {name}; conversion interdite')
        preflight()  # recontrôle checkout et fichiers après la lecture longue
        require_idle()
        rc = run_converter(command, session/'conversion.log')
        record['returncode'] = rc
        record['validation'] = validate(output)
        if rc != 0 or record['validation']['status'] != 'PASS':
            raise RuntimeError('conversion ou validation échouée; aucune promotion')
        record['output_sha256'] = sha256(output, check_idle=True)
        record['status'] = 'VALIDATED_TEMPORARY'
        # Pas de rename/promotion, même après succès: l'original est une preuve.
    except BaseException as exc:
        record['status'] = 'FAILED'
        record['error'] = str(exc)
        raise
    finally:
        record['finished_utc'] = datetime.now(timezone.utc).isoformat()
        save()
    return record


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--execute', action='store_true', help='exécuter après préflight et contrôle exclusivité')
    args = ap.parse_args()
    try:
        info = preflight()
        if not args.execute:
            print(json.dumps(info, ensure_ascii=False, indent=2))
            return 0
        require_idle()  # avant création de fichiers et avant SHA lourds
        if shutil.disk_usage(CACHE).free < 16*1024**3:
            raise RuntimeError('moins de 16 Gio libres')
        with (CACHE/'outils/r7-conversion.lock').open('a') as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            require_idle()
            session = Path(tempfile.mkdtemp(prefix='r7-final-', dir=CACHE/'outils'))
            print(f'Provenance: {session / "provenance.json"}', flush=True)
            print(json.dumps(convert(session), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.SubprocessError) as exc:
        print(f'REFUS R7: {exc}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
