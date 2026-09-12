"""P5 vu echouer, et vu passer."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from socle import CasDePorte, lance

CIBLE = """# Rapport cible

## 1. Question
## 2. Instrument
### 2.1 Seuil
## 3 bis. Multiplicite
"""


class TestP5(CasDePorte):

    def _paire(self, tmp: Path, renvoi: str) -> Path:
        (tmp / "cible.md").write_text(CIBLE, encoding="utf-8")
        src = tmp / "source.md"
        src.write_text(renvoi, encoding="utf-8")
        return src

    def test_echec_renvoi_vers_section_inexistante(self):
        """v1 §2.4 : trois renvois faux sur soixante, silencieux."""
        with tempfile.TemporaryDirectory() as t:
            src = self._paire(Path(t), "Voir `cible.md` §7.4 pour le detail.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertEchoue(code, sortie, "aucune section 7.4")

    def test_echec_sous_section_inexistante(self):
        with tempfile.TemporaryDirectory() as t:
            src = self._paire(Path(t), "Voir `cible.md` §2.9.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertEchoue(code, sortie, "aucune section 2.9")

    def test_passage_renvoi_exact(self):
        with tempfile.TemporaryDirectory() as t:
            src = self._paire(Path(t), "Voir `cible.md` §2.1 et `cible.md` §1.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertPasse(code, sortie)

    def test_passage_renvoi_bis(self):
        with tempfile.TemporaryDirectory() as t:
            src = self._paire(Path(t), "Voir `cible.md` §3 bis.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertPasse(code, sortie)

    def test_passage_renvoi_sans_fichier_nomme(self):
        """Un §N.M seul n'est pas devine : la porte n'accuse pas a tort (v2 §6)."""
        with tempfile.TemporaryDirectory() as t:
            src = self._paire(Path(t), "Comme dit plus haut en §9.9.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertPasse(code, sortie)

    def test_echec_alias_manuscrit(self):
        """L'alias « manuscrit » resout vers article/manuscrit.md du depot reel."""
        with tempfile.TemporaryDirectory() as t:
            src = Path(t) / "s.md"
            src.write_text("Voir manuscrit §99.99 pour le confondu.\n", encoding="utf-8")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertEchoue(code, sortie, "aucune section 99.99")


if __name__ == "__main__":
    unittest.main()
