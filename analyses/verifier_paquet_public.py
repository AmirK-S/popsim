#!/usr/bin/env python3
"""Refuse les contenus incompatibles avec une archive publique popsim.

Utilisation :
    python analyses/verifier_paquet_public.py CHEMIN_VERS_PAQUET

Le controle est volontairement conservateur. Il ne rend pas des donnees anonymes et ne
certifie pas une licence : il refuse les categories qui ne doivent pas se trouver dans
une archive publique. Aucun acces reseau, aucune ecriture dans le paquet examine.
"""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import sys


WEIGHT_SUFFIXES = {".gguf", ".safetensors", ".ckpt", ".pth", ".pt", ".onnx", ".mlmodel"}
MICRODATA_SUFFIXES = {".dta", ".sav", ".parquet", ".rds", ".rdata", ".xlsx", ".xls", ".feather"}
PRIVATE_KEY = re.compile(rb"-----BEGIN (?:RSA|EC|OPENSSH|DSA) PRIVATE KEY-----")
TOKEN = re.compile(rb"(?:gh[pousr]_[A-Za-z0-9_]{20,}|(?:sk|rk|or)-[A-Za-z0-9_-]{20,})")
KEY_ASSIGNMENT = re.compile(
    rb"(?:api|openai|openrouter|anthropic|huggingface|hf)[_-]?(?:api[_-]?)?key\s*[:=]\s*[\"']?[A-Za-z0-9_-]{16,}",
    re.IGNORECASE,
)
SENSITIVE_HEADER = re.compile(
    r"(?i)(?:^|[,;\t])(?:pid|userid|user_id|respondent(?:_id)?|participant(?:_id)?|persona|free[_ -]?text|open[_ -]?ended)(?:$|[,;\t])"
)


def issue(path: Path, code: str) -> tuple[str, str]:
    return (path.as_posix(), code)


def _contains_credential(path: Path) -> bool:
    """Cherche aussi dans les gros fichiers, sans afficher leur contenu."""
    overlap = b""
    try:
        with path.open("rb") as stream:
            while chunk := stream.read(64 * 1024):
                sample = overlap + chunk
                if (PRIVATE_KEY.search(sample) or TOKEN.search(sample)
                        or KEY_ASSIGNMENT.search(sample)):
                    return True
                overlap = sample[-1024:]
    except OSError:
        return False
    return False


def _sensitive_header(path: Path) -> bool:
    try:
        with path.open("rb") as stream:
            header = stream.read(64 * 1024).decode("utf-8", errors="replace").splitlines()[0]
    except (OSError, IndexError):
        return False
    return bool(SENSITIVE_HEADER.search(header))


def inspect_path(root: Path, path: Path) -> list[tuple[str, str]]:
    rel = path.relative_to(root)
    parts = {part.casefold() for part in rel.parts}
    name = path.name.casefold()
    suffix = path.suffix.casefold()
    found: list[tuple[str, str]] = []

    if path.is_symlink():
        return [issue(rel, "symlink")]
    if "data" in parts:
        found.append(issue(rel, "data-directory"))
    if any(part.startswith("trace") for part in parts) or any("ledger" in part for part in parts):
        found.append(issue(rel, "trace-or-ledger"))
    if name == ".env":
        found.append(issue(rel, "environment-file"))
    if any(part in {"modeles", "models", "weights", "checkpoints"} for part in parts):
        found.append(issue(rel, "model-directory"))
    if suffix in WEIGHT_SUFFIXES:
        found.append(issue(rel, "model-weight"))
    if suffix in MICRODATA_SUFFIXES or any(x in name for x in ("microdata", "microdonnee", "personnes")):
        found.append(issue(rel, "microdata"))
    if suffix == ".jsonl":
        found.append(issue(rel, "raw-jsonl"))
    if path.is_file():
        if _contains_credential(path):
            found.append(issue(rel, "credential-pattern"))
        if suffix in {".csv", ".tsv"} and _sensitive_header(path):
            found.append(issue(rel, "sensitive-tabular-header"))
    return found


def scan(root: Path) -> list[tuple[str, str]]:
    if not root.is_dir():
        raise ValueError(f"not a directory: {root}")
    findings: list[tuple[str, str]] = []
    for current, dirs, files in os.walk(root, followlinks=False):
        base = Path(current)
        for dirname in list(dirs):
            path = base / dirname
            if path.is_symlink():
                findings.append(issue(path.relative_to(root), "symlink"))
                dirs.remove(dirname)
            else:
                findings.extend(inspect_path(root, path))
        for filename in files:
            findings.extend(inspect_path(root, base / filename))
    return sorted(set(findings))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("package", type=Path, help="racine de l'archive publique a controler")
    args = parser.parse_args()
    if args.package.is_symlink():
        print("REFUS: la racine du paquet est un lien symbolique", file=sys.stderr)
        return 1
    try:
        findings = scan(args.package.resolve())
    except ValueError as exc:
        print(f"REFUS: {exc}", file=sys.stderr)
        return 2
    if findings:
        print("REFUS: contenu non publiable detecte", file=sys.stderr)
        for path, code in findings:
            print(f"- {code}: {path}", file=sys.stderr)
        return 1
    print("OK: aucune categorie interdite detectee")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
