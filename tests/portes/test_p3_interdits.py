"""P3 vu echouer, et vu passer."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from socle import RACINE, CasDePorte, lance

SYNTHESE_JOUET = """# Synthese jouet

**A1 — couplage.** Autorise : « la qualite globale et le taux s'ordonnent ensemble. »
INTERDIT : « la fidelite individuelle cause la fuite », « fidelite et identifiabilite
sont le meme axe », et toute formulation causale.

**A3 — monde ouvert.** INTERDIT : citer 20,7 % sans preciser que ce sont des taux en
monde ferme ; « notre loi est refutee par Argyle ».
"""


class TestP3(CasDePorte):

    def _synthese(self, tmp: Path) -> Path:
        p = tmp / "synthese.md"
        p.write_text(SYNTHESE_JOUET, encoding="utf-8")
        return p

    def test_echec_formulation_interdite_recopiee(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            s = self._synthese(tmp)
            m = tmp / "manuscrit.md"
            m.write_text("Nos resultats montrent que la fidelite individuelle cause "
                         "la fuite.\n", encoding="utf-8")
            code, sortie = lance("interdits",
                                 ["--synthese", str(s), "--fichier", str(m)])
            self.assertEchoue(code, sortie, "formulation INTERDITE")
            self.assertIn("cause la fuite", sortie)

    def test_echec_malgre_une_autre_typographie(self):
        """Accents, gras et apostrophe courbe ne doivent pas suffire a passer."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            s = self._synthese(tmp)
            m = tmp / "manuscrit.md"
            # accents, gras, guillemets courbes et apostrophe typographique
            m.write_text("On lira que **“notre loi est réfutée par Argyle”**, "
                         "et l’on aurait tort.\n", encoding="utf-8")
            code, sortie = lance("interdits",
                                 ["--synthese", str(s), "--fichier", str(m)])
            self.assertEchoue(code, sortie, "formulation INTERDITE")

    def test_passage_formulation_autorisee(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            s = self._synthese(tmp)
            m = tmp / "manuscrit.md"
            m.write_text("La qualite globale et le taux s'ordonnent ensemble ; "
                         "manquee mais hors domaine.\n", encoding="utf-8")
            code, sortie = lance("interdits",
                                 ["--synthese", str(s), "--fichier", str(m)])
            self.assertPasse(code, sortie)

    def test_abandon_si_aucune_formulation_extraite(self):
        """Une porte qui ne refuserait jamais rien doit se declarer inoperante (code 2)."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            s = tmp / "vide.md"
            s.write_text("# rien d'interdit ici\n", encoding="utf-8")
            m = tmp / "m.md"
            m.write_text("texte\n", encoding="utf-8")
            code, sortie = lance("interdits",
                                 ["--synthese", str(s), "--fichier", str(m)])
            self.assertEqual(code, 2, sortie)
            self.assertIn("ne refuserait jamais rien", sortie)

    def test_extraction_sur_la_vraie_synthese(self):
        """La source de verite reelle doit livrer des formulations grep-ables."""
        code, sortie = lance("interdits", ["--lister"])
        self.assertEqual(code, 0, sortie)
        nombre = int(sortie.strip().rsplit("] ", 1)[1].split()[0])
        self.assertGreaterEqual(nombre, 10,
                                "moins de 10 formulations verbatim extraites : la porte "
                                "serait decorative")


if __name__ == "__main__":
    unittest.main()
