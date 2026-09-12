"""P1 vu echouer, et vu passer (regle G0.5 de la v1)."""

from __future__ import annotations

import shutil
import tempfile
import unittest
from pathlib import Path

from socle import RACINE, CasDePorte, commit, depot_jetable, lance

GABARIT = RACINE / "gabarits" / "preenregistrement.md"


class TestP1(CasDePorte):

    # --- (b) completude PAP -------------------------------------------------

    def test_echec_section_instrument_absente(self):
        """Sans la section 2 « Instrument », P1 doit refuser le fichier (v2 §2.1)."""
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "x-preenregistrement.md"
            texte = GABARIT.read_text(encoding="utf-8")
            texte = texte.replace("## 2. Instrument", "## 2. Blabla")
            texte = texte.replace("vu échouer sur", "sans avoir jamais echoue sur")
            f.write_text(texte, encoding="utf-8")
            code, sortie = lance("preenregistrement_seul", ["--fichier", str(f)])
            self.assertEchoue(code, sortie, "section A1 n°2 introuvable")
            self.assertIn("VU ECHOUER", sortie)

    def test_echec_clause_aucun_appel_absente(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "y-preenregistrement.md"
            texte = GABARIT.read_text(encoding="utf-8").replace(
                "Aucun appel n'a eu lieu", "Des appels ont eu lieu")
            f.write_text(texte, encoding="utf-8")
            code, sortie = lance("preenregistrement_seul", ["--fichier", str(f)])
            self.assertEchoue(code, sortie, "Aucun appel")

    def test_echec_entete_incomplete(self):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "z-preenregistrement.md"
            texte = GABARIT.read_text(encoding="utf-8").replace(
                "horodatage_ots: preuves/<fichier>.ots", "")
            f.write_text(texte, encoding="utf-8")
            code, sortie = lance("preenregistrement_seul", ["--fichier", str(f)])
            self.assertEchoue(code, sortie, "horodatage_ots")

    def test_passage_gabarit_a1(self):
        """Le gabarit A4/A1 livre doit passer sa propre porte, sinon il est faux."""
        code, sortie = lance("preenregistrement_seul", ["--fichier", str(GABARIT)])
        self.assertPasse(code, sortie)

    # --- (a) commit seul ----------------------------------------------------

    def _depot(self, t):
        d = depot_jetable(Path(t))
        (d / "resultats").mkdir()
        (d / "socle.txt").write_text("base\n", encoding="utf-8")
        base = commit(d, "base")
        return d, base

    def test_echec_preenregistrement_commis_avec_son_script(self):
        """Le cas G0.1 de la v1 : le plan et le script dans le meme commit."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            shutil.copy(GABARIT, d / "resultats" / "c9-preenregistrement.md")
            (d / "c9.py").write_text("print('calcul')\n", encoding="utf-8")
            commit(d, "C9 : plan + script")
            code, sortie = self._dans(d, ["--depuis", base])
            self.assertEchoue(code, sortie, "ET touche")
            self.assertIn("c9.py", sortie)

    def test_passage_preenregistrement_commis_seul(self):
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            shutil.copy(GABARIT, d / "resultats" / "c9-preenregistrement.md")
            commit(d, "C9 : preenregistrement seul")
            code, sortie = self._dans(d, ["--depuis", base])
            self.assertPasse(code, sortie)

    @staticmethod
    def _dans(depot: Path, argv: list[str]) -> tuple[int, str]:
        """Rejoue la porte avec RACINE pointee sur le depot jetable."""
        import subprocess
        import sys
        copie = depot / "outils" / "portes"
        copie.mkdir(parents=True, exist_ok=True)
        for nom in ("commun.py", "preenregistrement_seul.py"):
            shutil.copy(RACINE / "outils" / "portes" / nom, copie / nom)
        res = subprocess.run(
            [sys.executable, str(copie / "preenregistrement_seul.py"), *argv],
            capture_output=True, text=True, cwd=str(depot))
        return res.returncode, res.stdout + res.stderr


if __name__ == "__main__":
    unittest.main()
