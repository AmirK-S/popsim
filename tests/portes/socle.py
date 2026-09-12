"""Outillage commun aux tests des six portes (Methode v2 §1.7).

Regle G0.5 de la v1 : « un controle qu'on n'a jamais vu echouer n'est pas un
controle ». Chaque porte a donc ici DEUX tests au minimum :
  - `test_echec_*`  : un cas fabrique qui doit faire sortir la porte en code 1 ;
  - `test_passage_*`: un cas propre qui doit la faire sortir en code 0.

Les tests n'ecrivent que dans un repertoire temporaire, sauf lecture du depot.
"""

from __future__ import annotations

import contextlib
import io
import subprocess
import sys
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
PORTES = RACINE / "outils" / "portes"
sys.path.insert(0, str(PORTES))


def lance(module: str, argv: list[str]) -> tuple[int, str]:
    """Execute une porte en process separe : c'est ainsi que la CI l'appelle."""
    res = subprocess.run(
        [sys.executable, str(PORTES / f"{module}.py"), *argv],
        capture_output=True, text=True, cwd=str(RACINE),
    )
    return res.returncode, res.stdout + res.stderr


def lance_en_processus(fonction, argv: list[str]) -> tuple[int, str]:
    """Variante rapide, en processus, pour les cas nombreux."""
    tampon = io.StringIO()
    with contextlib.redirect_stdout(tampon), contextlib.redirect_stderr(tampon):
        code = fonction(argv)
    return code, tampon.getvalue()


def depot_jetable(tmp: Path) -> Path:
    """Un petit depot git autonome, pour les portes qui lisent l'historique."""
    d = tmp / "depot"
    d.mkdir()
    subprocess.run(["git", "init", "-q", "-b", "master"], cwd=d, check=True)
    subprocess.run(["git", "config", "user.email", "t@t"], cwd=d, check=True)
    subprocess.run(["git", "config", "user.name", "t"], cwd=d, check=True)
    subprocess.run(["git", "config", "commit.gpgsign", "false"], cwd=d, check=True)
    return d


def commit(d: Path, message: str) -> str:
    subprocess.run(["git", "add", "-A"], cwd=d, check=True)
    subprocess.run(["git", "commit", "-q", "-m", message], cwd=d, check=True)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=d,
                          capture_output=True, text=True, check=True).stdout.strip()


class CasDePorte(unittest.TestCase):
    def assertEchoue(self, code: int, sortie: str, motif: str = "") -> None:
        self.assertEqual(code, 1, f"la porte aurait du se fermer.\n{sortie}")
        if motif:
            self.assertIn(motif, sortie)

    def assertPasse(self, code: int, sortie: str) -> None:
        self.assertEqual(code, 0, f"la porte aurait du laisser passer.\n{sortie}")
