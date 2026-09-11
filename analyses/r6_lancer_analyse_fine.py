"""Lance localement l'analyse fine d'un seul modèle R6 terminal.

Le module n'utilise ni réseau, ni sous-processus, ni signal. Il ne contacte donc jamais une
campagne R6 en cours. Le chargeur ``r6_analyse_fine`` contrôle le ledger complet avant toute
ouverture de trace : une collecte partielle est seulement journalisée comme refusée.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile

import r6_analyse_fine as FINE


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_OUTPUT = ROOT / "resultats" / "r6-analyse-fine"
VERSION = "R6-analyse-fine-lanceur-1"


def sha256(path: Path) -> str:
    return FINE.sha256(path)


def _json(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FINE.ChargementTerminalRefuse("manifeste analyse fine absent ou invalide") from exc
    if not isinstance(value, dict):
        raise FINE.ChargementTerminalRefuse("manifeste analyse fine non objet")
    return value


def _slug(model: str) -> str:
    readable = re.sub(r"[^a-zA-Z0-9]+", "-", model).strip("-").lower()
    return f"{readable}-{hashlib.sha256(model.encode('utf-8')).hexdigest()[:10]}"


def _source_fingerprint(manifest_sha: str, model_spec: dict) -> str:
    canonical = json.dumps(model_spec, ensure_ascii=False, sort_keys=True,
                           separators=(",", ":")).encode("utf-8")
    code_sha = sha256(Path(FINE.__file__).resolve())
    return hashlib.sha256(manifest_sha.encode("ascii") + b"\0" + canonical + b"\0" +
                          code_sha.encode("ascii")).hexdigest()


def _absolutiser_spec(base: Path, spec: dict) -> dict:
    if not isinstance(spec, dict):
        raise FINE.ChargementTerminalRefuse("specification source invalide")
    copy = dict(spec)
    raw = copy.get("path")
    if not isinstance(raw, str) or not raw:
        raise FINE.ChargementTerminalRefuse("specification source sans chemin")
    p = Path(raw)
    copy["path"] = str(p if p.is_absolute() else (base / p).resolve())
    return copy


def manifeste_modele(manifeste_path: Path, model: str) -> tuple[dict, dict, str]:
    """Construit en mémoire un manifeste à un modèle, sans modifier la source."""
    root = _json(manifeste_path)
    if root.get("version") != "R6-analyse-fine-1" or not isinstance(root.get("models"), list):
        raise FINE.ChargementTerminalRefuse("version ou liste de modèles incompatible")
    specs = [x for x in root["models"] if isinstance(x, dict) and x.get("model") == model]
    if len(specs) != 1:
        raise FINE.ChargementTerminalRefuse("modèle absent ou dupliqué dans le manifeste")
    base = manifeste_path.resolve().parent
    spec = dict(specs[0])
    spec["floor_cells"] = _absolutiser_spec(base, spec.get("floor_cells"))
    spec["ledger"] = _absolutiser_spec(base, spec.get("ledger"))
    traces = spec.get("traces")
    if not isinstance(traces, list):
        raise FINE.ChargementTerminalRefuse("traces du modèle absentes")
    spec["traces"] = [dict(_absolutiser_spec(base, trace)) for trace in traces]
    selected = {"version": root["version"],
                "orientation": _absolutiser_spec(base, root.get("orientation")),
                "referent": _absolutiser_spec(base, root.get("referent")), "models": [spec]}
    return selected, specs[0], sha256(manifeste_path)


def _journal_refus(root: Path, model: str, manifest_sha: str, reason: str) -> None:
    root.mkdir(parents=True, exist_ok=True)
    path = root / "refus.jsonl"
    record = {"version": VERSION, "horodatage": dt.datetime.now(dt.timezone.utc).isoformat(),
              "modele": model, "manifeste_sha256": manifest_sha, "statut": "REFUSE",
              "raison": reason}
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.chmod(path, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False, allow_nan=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _receipt_valide(path: Path, fingerprint: str, model: str) -> bool:
    if not path.is_file():
        return False
    try:
        receipt = _json(path)
        files = receipt["fichiers"]
    except (KeyError, FINE.ChargementTerminalRefuse):
        return False
    if (receipt.get("version") != VERSION or receipt.get("statut") != "TERMINE"
            or receipt.get("modele") != model or receipt.get("empreinte_source") != fingerprint
            or not isinstance(files, dict) or not files):
        return False
    return all(isinstance(name, str) and isinstance(digest, str)
               and (path.parent / name).is_file() and sha256(path.parent / name) == digest
               for name, digest in files.items())


def executer(manifeste_path: Path, model: str, sortie: Path = DEFAULT_OUTPUT) -> dict:
    """Produit une analyse seulement après le contrôle terminal de ce modèle précis."""
    manifeste_path, sortie = manifeste_path.resolve(), sortie.resolve()
    try:
        selected, spec_source, manifest_sha = manifeste_modele(manifeste_path, model)
    except FINE.ChargementTerminalRefuse as exc:
        _journal_refus(sortie, model, sha256(manifeste_path) if manifeste_path.is_file() else "absent", str(exc))
        return {"statut": "REFUSE", "modele": model, "raison": str(exc)}
    fingerprint = _source_fingerprint(manifest_sha, spec_source)
    target = sortie / _slug(model) / fingerprint[:16]
    receipt = target / "execution.json"
    lock_path = sortie / ".locks" / f"{_slug(model)}-{fingerprint[:16]}.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a", encoding="utf-8") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        if _receipt_valide(receipt, fingerprint, model):
            return {"statut": "DEJA_TERMINE", "modele": model, "sortie": str(target),
                    "empreinte_source": fingerprint}
        try:
            with tempfile.TemporaryDirectory(prefix="r6-analyse-fine-", dir=sortie) as tmp:
                tmp_path = Path(tmp)
                selected_path = tmp_path / "manifeste-modele.json"
                selected_path.write_text(json.dumps(selected, ensure_ascii=False, sort_keys=True),
                                         encoding="utf-8")
                # Le chargeur ouvre les traces seulement après 1 250 opérations réglées exactes.
                campaigns, context = FINE.charger_campagnes(selected_path)
                tables = FINE.analyser(campaigns, context)
                stage = tmp_path / "sortie"
                FINE.ecrire(stage, tables)
                hashes = {p.name: sha256(p) for p in sorted(stage.glob("*.csv"))}
                if len(hashes) != len(tables):
                    raise RuntimeError("sorties exploratoires incomplètes")
                receipt_data = {"version": VERSION, "statut": "TERMINE", "modele": model,
                                "manifeste_sha256": manifest_sha, "empreinte_source": fingerprint,
                                "fichiers": hashes}
                (stage / "execution.json").write_text(
                    json.dumps(receipt_data, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
                target.parent.mkdir(parents=True, exist_ok=True)
                if target.exists():
                    # Un ancien répertoire sans reçu valide n'est jamais réemployé ni écrasé.
                    raise RuntimeError("sortie existante sans reçu idempotent valide")
                os.replace(stage, target)
        except (FINE.ChargementTerminalRefuse, OSError, RuntimeError, ValueError) as exc:
            _journal_refus(sortie, model, manifest_sha, str(exc))
            return {"statut": "REFUSE", "modele": model, "raison": str(exc)}
    return {"statut": "TERMINE", "modele": model, "sortie": str(target),
            "empreinte_source": fingerprint}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifeste", type=Path, required=True)
    parser.add_argument("--modele", required=True)
    parser.add_argument("--sortie", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    result = executer(args.manifeste, args.modele, args.sortie)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["statut"] in {"TERMINE", "DEJA_TERMINE"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
