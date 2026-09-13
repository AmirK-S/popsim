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

    # --- Faux positifs constates sur la PR #8 (13/09/2026), et leur contrepartie
    # fautive : chaque correction de la porte doit continuer a refuser le cas faux.

    def test_passage_titre_prefixe_par_paragraphe(self):
        """« ## §8 — … » est un titre de section 8 (audit-comparaison-dp-2026-09-13.md)."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            (tmp / "audit.md").write_text("# A\n\n## §8 — Formulation\n## §9 — Code\n",
                                          encoding="utf-8")
            src = tmp / "source.md"
            src.write_text("Voir `audit.md` §8. Cible : le §9 de `audit.md`.\n", encoding="utf-8")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertPasse(code, sortie)

    def test_echec_titre_prefixe_par_paragraphe_section_absente(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            (tmp / "audit.md").write_text("# A\n\n## §18 — Formulation\n", encoding="utf-8")
            src = tmp / "source.md"
            src.write_text("Voir `audit.md` §1.\n", encoding="utf-8")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertEchoue(code, sortie, "aucune section 1")

    def test_passage_renvoi_attribue_au_fichier_qui_le_precede(self):
        """« cite dans autre (§5) et dans `cible.md` §2.1 » : §5 va a autre, pas a cible."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            (tmp / "autre.md").write_text("# B\n\n## 5. Cinq\n", encoding="utf-8")
            src = self._paire(tmp, "Cite dans `autre.md` (§5) et dans `cible.md` §2.1.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertPasse(code, sortie)

    def test_echec_renvoi_faux_vers_le_second_fichier(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            (tmp / "autre.md").write_text("# B\n\n## 5. Cinq\n", encoding="utf-8")
            src = self._paire(tmp, "Cite dans `autre.md` (§5) et dans `cible.md` §5.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertEchoue(code, sortie, "aucune section 5")

    def test_passage_section_externe_avant_un_fichier_sans_lien(self):
        """Numeros d'une norme externe (AAPOR §6.2.3), puis un fichier nomme sans lien."""
        with tempfile.TemporaryDirectory() as t:
            src = self._paire(Path(t), "Relecture des §6.2.3, §6.2.4) : conforme a `cible.md`.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertPasse(code, sortie)

    def test_echec_renvoi_suivi_de_son_fichier(self):
        """« le §7 de `cible.md` » reste resolu vers cible.md."""
        with tempfile.TemporaryDirectory() as t:
            src = self._paire(Path(t), "Cible : le §7 de `cible.md`, repris in extenso.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertEchoue(code, sortie, "aucune section 7")

    def test_echec_liste_de_renvois_suivie_de_son_fichier(self):
        with tempfile.TemporaryDirectory() as t:
            src = self._paire(Path(t), "Voir les §2.1 et §8 dans `cible.md`.\n")
            code, sortie = lance("renvois", ["--fichier", str(src)])
            self.assertEchoue(code, sortie, "aucune section 8")


if __name__ == "__main__":
    unittest.main()
