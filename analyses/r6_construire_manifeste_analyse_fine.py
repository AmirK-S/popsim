"""Construit puis lance l'analyse fine d'un reçu terminal R6, hors réseau.

Une analyse ne peut être créée qu'à partir d'une file QUEUE_READY, d'un reçu terminal écrit
par ``r6_runner_campagnes`` et de 1 250 opérations réglées dans l'ordre. Les traces ne sont
ni ouvertes ni hachées avant cette dernière garde. Le module ne démarre, n'arrête ni ne
signale aucun processus R6.
"""
from __future__ import annotations

import argparse
import datetime as dt
import fcntl
import hashlib
import json
import os
from pathlib import Path
import tempfile

import r6_analyse_fine as FINE
import r6_lancer_analyse_fine as LANCER
import r6_runner_campagnes as RUNNER


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_MANIFESTS = ROOT / "resultats" / "r6-manifestes-analyse-fine"
DEFAULT_ANALYSES = ROOT / "resultats" / "r6-analyse-fine"
VERSION = "R6-analyse-fine-construction-1"
RECEIPT_VERSION = "R6-campaign-terminal-receipt-1"
PASSES = (("campagne", "q4", 894), ("campagne", "q4gab3", 316),
          ("plancher", "q4", 40))


def _json(path: Path, label: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise FINE.ChargementTerminalRefuse(f"{label} absent ou JSON invalide") from exc
    if not isinstance(value, dict):
        raise FINE.ChargementTerminalRefuse(f"{label} non objet")
    return value


def _sha(path: Path) -> str:
    return FINE.sha256(path)


def _journal_refus(root: Path, model: str, reason: str) -> None:
    root.mkdir(parents=True, exist_ok=True)
    path = root / "refus-construction.jsonl"
    line = {"version": VERSION, "horodatage": dt.datetime.now(dt.timezone.utc).isoformat(),
            "modele": model, "statut": "REFUSE", "raison": reason}
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.chmod(path, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as handle:
        handle.write(json.dumps(line, ensure_ascii=False, allow_nan=False, sort_keys=True) + "\n")
        handle.flush()
        os.fsync(handle.fileno())


def _spec(path: Path) -> dict:
    if not path.is_file():
        raise FINE.ChargementTerminalRefuse(f"source absente: {path}")
    return {"path": str(path.resolve()), "sha256": _sha(path)}


def _model_from_receipt(receipt_path: Path, queue: dict, queue_sha: str,
                        orientation: Path, referent: Path) -> tuple[str, dict]:
    receipt = _json(receipt_path, "reçu terminal")
    model = receipt.get("modele")
    if (receipt.get("version") != RECEIPT_VERSION or receipt.get("statut") != "TERMINE"
            or not isinstance(model, str) or receipt.get("queue_manifest_sha256") != queue_sha):
        raise FINE.ChargementTerminalRefuse("reçu terminal incompatible avec QUEUE_READY")
    policies = [x for x in queue["models"] if x.get("model") == model]
    if len(policies) != 1:
        raise FINE.ChargementTerminalRefuse("modèle du reçu absent ou dupliqué dans la file")
    policy = RUNNER.politique_modele(queue, model)
    if (receipt.get("fournisseur") != policy["provider_fixed"]
            or receipt.get("analysis_role") != policy["analysis_role"]
            or receipt.get("non_deterministe") is not policy["non_deterministe"]):
        raise FINE.ChargementTerminalRefuse("rôle ou provenance du reçu incompatible avec la file")
    consumed = receipt.get("go_consomme")
    if not isinstance(consumed, str) or not Path(consumed).is_file():
        raise FINE.ChargementTerminalRefuse("GO consommé absent du reçu terminal")
    ledger_raw = receipt.get("ledger")
    if not isinstance(ledger_raw, dict) or not isinstance(ledger_raw.get("path"), str):
        raise FINE.ChargementTerminalRefuse("ledger absent du reçu terminal")
    ledger = Path(ledger_raw["path"])
    if (not ledger.is_file() or ledger.resolve() != Path(queue["ledger_path"]).resolve()
            or ledger_raw.get("sha256") != _sha(ledger)):
        raise FINE.ChargementTerminalRefuse("ledger reçu/file absent ou empreinte différente")
    floor_raw = receipt.get("floor_cells")
    floor_step = policy["steps"][2]
    if not isinstance(floor_raw, dict) or not isinstance(floor_raw.get("path"), str):
        raise FINE.ChargementTerminalRefuse("liste plancher absente du reçu")
    floor = Path(floor_raw["path"])
    if (not floor.is_file() or floor.resolve() != Path(floor_step["cell_list"]).resolve()
            or floor_raw.get("sha256") != floor_step["cell_list_sha256"]
            or _sha(floor) != floor_step["cell_list_sha256"]):
        raise FINE.ChargementTerminalRefuse("liste plancher reçue différente de la file")

    # Cette garde parcourt le ledger, jamais une trace : 220 F1 est donc refusé ici.
    orientation_spec, referent_spec = _spec(orientation), _spec(referent)
    items, orientes, _sens, _ = FINE.lire_orientation(orientation)
    expected = FINE._attendus(items, orientes, FINE._lire_plancher(floor))
    FINE._operations_terminales(ledger, model, expected)

    rows = receipt.get("traces")
    if not isinstance(rows, list) or len(rows) != 3:
        raise FINE.ChargementTerminalRefuse("reçu terminal sans les trois traces")
    by_pass = {(x.get("passe"), x.get("format")): x for x in rows if isinstance(x, dict)}
    if set(by_pass) != {(p, f) for p, f, _ in PASSES}:
        raise FINE.ChargementTerminalRefuse("passes du reçu différentes de F1/F2/plancher")
    trace_specs = []
    for passe, format_, cells in PASSES:
        trace = by_pass[(passe, format_)]
        if trace.get("cellules") != cells or not isinstance(trace.get("path"), str):
            raise FINE.ChargementTerminalRefuse("volume ou chemin de trace terminale invalide")
        path = Path(trace["path"])
        if Path(str(path) + ".en-cours").exists():
            raise FINE.ChargementTerminalRefuse("trace marquée active après reçu terminal")
        configuration = trace.get("configuration")
        if not isinstance(configuration, dict):
            raise FINE.ChargementTerminalRefuse("configuration absente du reçu terminal")
        # Les octets ne sont lus qu'après la garde des 1 250 opérations.
        if not path.is_file() or trace.get("sha256") != _sha(path):
            raise FINE.ChargementTerminalRefuse("empreinte de trace terminale différente")
        trace_specs.append({"path": str(path.resolve()), "sha256": trace["sha256"],
                            "passe": passe, "format": format_, "configuration": configuration})
    spec = {"model": model, "provider": policy["provider_fixed"], "terminal": "TERMINE",
            "analysis_role": policy["analysis_role"],
            "non_deterministe": policy["non_deterministe"], "floor_cells": _spec(floor),
            "ledger": _spec(ledger), "traces": trace_specs}
    return model, {"version": "R6-analyse-fine-1", "orientation": orientation_spec,
                   "referent": referent_spec, "models": [spec]}


def executer(queue_path: Path, queue_sha: str, receipt_path: Path, orientation: Path,
             referent: Path, manifests: Path = DEFAULT_MANIFESTS,
             analyses: Path = DEFAULT_ANALYSES) -> dict:
    """Construit un manifeste terminal idempotent, puis délègue au lanceur local."""
    manifests, analyses = manifests.resolve(), analyses.resolve()
    model = "inconnu"
    try:
        queue = RUNNER.charger_file(str(queue_path), queue_sha)
        if queue.get("state") != "QUEUE_READY" or queue.get("executable") is not True:
            raise FINE.ChargementTerminalRefuse("QUEUE_READY exécutable requis")
        model, manifest = _model_from_receipt(receipt_path, queue, queue_sha, orientation, referent)
        source = hashlib.sha256((queue_sha + "\0" + _sha(receipt_path) + "\0" +
                                 _sha(orientation) + "\0" + _sha(referent)).encode("ascii")).hexdigest()
        target = manifests / LANCER._slug(model) / f"{source[:16]}.json"
        lock_path = manifests / ".locks" / f"{LANCER._slug(model)}-{source[:16]}.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        with lock_path.open("a", encoding="utf-8") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX)
            rendered = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
            if target.is_file():
                if target.read_text(encoding="utf-8") != rendered:
                    raise FINE.ChargementTerminalRefuse("manifeste idempotent existant différent")
                construction = "DEJA_CONSTRUIT"
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile("w", encoding="utf-8", dir=target.parent,
                                                 delete=False) as tmp:
                    tmp.write(rendered)
                    tmp.flush()
                    os.fsync(tmp.fileno())
                    temporary = tmp.name
                os.replace(temporary, target)
                construction = "CONSTRUIT"
        launched = LANCER.executer(target, model, analyses)
        status = construction if launched.get("statut") in {"TERMINE", "DEJA_TERMINE"} else "REFUSE"
        return {"statut": status, "construction": construction, "modele": model, "manifeste": str(target),
                "manifeste_sha256": _sha(target), "lanceur": launched}
    except (FINE.ChargementTerminalRefuse, OSError, ValueError) as exc:
        _journal_refus(manifests, model, str(exc))
        return {"statut": "REFUSE", "modele": model, "raison": str(exc)}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--queue", type=Path, required=True)
    parser.add_argument("--queue-sha256", required=True)
    parser.add_argument("--recu", type=Path, required=True)
    parser.add_argument("--orientation", type=Path, required=True)
    parser.add_argument("--referent", type=Path, required=True)
    parser.add_argument("--sortie-manifestes", type=Path, default=DEFAULT_MANIFESTS)
    parser.add_argument("--sortie-analyses", type=Path, default=DEFAULT_ANALYSES)
    args = parser.parse_args(argv)
    result = executer(args.queue, args.queue_sha256, args.recu, args.orientation, args.referent,
                      args.sortie_manifestes, args.sortie_analyses)
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if result["statut"] in {"CONSTRUIT", "DEJA_CONSTRUIT"} else 2


if __name__ == "__main__":
    raise SystemExit(main())
