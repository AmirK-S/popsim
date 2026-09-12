"""P4 vu echouer, et vu passer."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from socle import RACINE, CasDePorte, commit, depot_jetable, lance

ENTETE_OK = """# Rapport jouet

statut: courant
mandat: trancher si la porte se ferme
agent: Opus 5, Anthropic
ecriture: resultats/jouet-resultats.md
lecture_seule: tout le reste
interdits: appel payant sans GO, reseau, commit sur master, arriere-plan
cout_reel_usd: 0.0

Corps du rapport.
"""


class TestP4(CasDePorte):

    def _fichier(self, tmp: Path, texte: str, nom="r.md") -> Path:
        d = tmp / "resultats"
        d.mkdir(exist_ok=True)
        p = d / nom
        p.write_text(texte, encoding="utf-8")
        return p

    # --- (a) en-tete --------------------------------------------------------

    def test_echec_aucun_entete(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), "# Rapport\n\nDes mesures.\n")
            code, sortie = lance("entetes", ["--fichier", str(p)])
            self.assertEchoue(code, sortie, "aucune ligne « statut: »")

    def test_echec_cle_manquante(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), ENTETE_OK.replace("cout_reel_usd: 0.0", ""))
            code, sortie = lance("entetes", ["--fichier", str(p)])
            self.assertEchoue(code, sortie, "cout_reel_usd")

    def test_echec_retracte_sans_fait_foi(self):
        """v1 §2.7 : une retractation doit dire ce qui fait foi a la place."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), ENTETE_OK.replace(
                "statut: courant", "retracte_par: resultats/audit.md"))
            code, sortie = lance("entetes", ["--fichier", str(p)])
            self.assertEchoue(code, sortie, "fait_foi")

    def test_passage_entete_complete(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), ENTETE_OK)
            code, sortie = lance("entetes", ["--fichier", str(p)])
            self.assertPasse(code, sortie)

    def test_passage_retracte_avec_fait_foi(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), ENTETE_OK.replace(
                "statut: courant",
                "retracte_par: resultats/audit.md\nfait_foi: resultats/audit.md"))
            code, sortie = lance("entetes", ["--fichier", str(p)])
            self.assertPasse(code, sortie)

    # --- (b) retractation dans le meme commit (G3.1) ------------------------

    def _depot(self, t):
        d = depot_jetable(Path(t))
        (d / "resultats").mkdir()
        (d / "resultats" / "c7-nul-corrige-resultats.md").write_text(
            ENTETE_OK, encoding="utf-8")
        (d / "resultats" / "audit.md").write_text(ENTETE_OK, encoding="utf-8")
        base = commit(d, "base")
        copie = d / "outils" / "portes"
        copie.mkdir(parents=True)
        for nom in ("commun.py", "entetes.py"):
            shutil.copy(RACINE / "outils" / "portes" / nom, copie / nom)
        return d, base

    def _dans(self, d: Path, argv: list[str]):
        res = subprocess.run(
            [sys.executable, str(d / "outils" / "portes" / "entetes.py"), *argv],
            capture_output=True, text=True, cwd=str(d))
        return res.returncode, res.stdout + res.stderr

    def test_echec_invalidation_sans_retractation_de_l_audite(self):
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            a = d / "resultats" / "audit.md"
            a.write_text(a.read_text(encoding="utf-8")
                         + "\nLe rapport c7-nul-corrige-resultats.md est refute.\n",
                         encoding="utf-8")
            commit(d, "Audit : renversement")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertEchoue(code, sortie, "sans toucher au fichier lui-meme")
            self.assertIn("c7-nul-corrige-resultats.md", sortie)

    def test_passage_mot_d_invalidation_dans_une_ligne_de_donnees(self):
        """Une retractation se declare dans de la prose, jamais dans une ligne de
        donnees. Cas reel du 12/09 : un identifiant de registre nomme
        « pmm-k10-top1-ferme-contre-examen » a fait croire a la porte qu'un CSV
        declarait un rapport invalide, et a bloque une PR a tort."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            csv = d / "resultats" / "registre-chiffres.csv"
            csv.write_text(
                "id,grandeur\n"
                "pmm-k10-contre-examen,\"PMM k=10 ; voir c7-nul-corrige-resultats.md refute\"\n",
                encoding="utf-8")
            commit(d, "Registre : une grandeur de plus")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)

    def test_passage_invalidation_et_retractation_dans_le_meme_commit(self):
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            a = d / "resultats" / "audit.md"
            a.write_text(a.read_text(encoding="utf-8")
                         + "\nLe rapport c7-nul-corrige-resultats.md est refute.\n",
                         encoding="utf-8")
            r = d / "resultats" / "c7-nul-corrige-resultats.md"
            r.write_text(r.read_text(encoding="utf-8").replace(
                "statut: courant",
                "retracte_par: resultats/audit.md\nfait_foi: resultats/audit.md"),
                encoding="utf-8")
            commit(d, "Audit : renversement + retractation")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)


if __name__ == "__main__":
    unittest.main()
