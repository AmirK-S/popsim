"""P4 vu echouer, et vu passer.

Le volet (b) — G3.1, retractation dans le commit qui invalide — a change de
principe le 12/09/2026 : la porte ne DEVINE plus une invalidation dans la prose,
elle exige un MARQUEUR canonique (`RETRACTE: resultats/<fichier>.md`, ligne
entiere, colonne 0). Les quatre tests `test_passage_faux_positif_*` sont les
quatre faux positifs reels d'une meme journee ; ils echouaient tous avec la
porte par inference, ils passent avec la porte par marqueur.
"""

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

RETRACTATION = ("retracte_par: resultats/audit.md\n"
                "fait_foi: resultats/audit.md")


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
                "statut: courant", RETRACTATION))
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

    def _ajoute(self, d: Path, nom: str, texte: str) -> Path:
        p = d / "resultats" / nom
        p.write_text(p.read_text(encoding="utf-8") + texte, encoding="utf-8")
        return p

    def _retracte(self, d: Path, nom: str) -> Path:
        p = d / "resultats" / nom
        p.write_text(p.read_text(encoding="utf-8").replace(
            "statut: courant", RETRACTATION), encoding="utf-8")
        return p

    # (b.1) le cas reel : le marqueur est pose, l'audite n'est pas touche.
    def test_echec_marqueur_sans_retractation_de_l_audite(self):
        """G3.1 : declarer un rapport invalide sans poser l'en-tete dans le
        MEME commit laisse un rapport faux public — les 6 minutes du 12/09."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md",
                         "\nLe renversement tombe.\n\n"
                         "RETRACTE: resultats/c7-nul-corrige-resultats.md\n")
            commit(d, "Audit : renversement")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertEchoue(code, sortie, "sans toucher au fichier lui-meme")
            self.assertIn("c7-nul-corrige-resultats.md", sortie)

    def test_echec_marqueur_et_audite_touche_sans_en_tete(self):
        """Toucher le fichier ne suffit pas : il faut y POSER la retractation.
        Sinon la porte se satisferait d'une virgule ajoutee en fin de rapport."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md",
                         "\nRETRACTE: resultats/c7-nul-corrige-resultats.md\n")
            self._ajoute(d, "c7-nul-corrige-resultats.md", "\nNote de bas de page.\n")
            commit(d, "Audit : renversement, en-tete oubliee")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertEchoue(code, sortie, "sans y poser l'en-tete de retractation")

    def test_echec_marqueur_mal_forme(self):
        """Un marqueur mal ecrit n'est JAMAIS ignore en silence : sans cela, une
        faute de frappe desarmerait la regle sans que personne le sache."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md", "\nRETRACTE: c7-nul-corige-resultats.md\n")
            commit(d, "Audit : marqueur fautif")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertEchoue(code, sortie, "mal forme")

    def test_echec_marqueur_vers_un_fichier_inexistant(self):
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md", "\nRETRACTE: resultats/jamais-ecrit.md\n")
            commit(d, "Audit : cible fantome")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertEchoue(code, sortie, "introuvable")

    def test_passage_marqueur_et_retractation_dans_le_meme_commit(self):
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md",
                         "\nRETRACTE: resultats/c7-nul-corrige-resultats.md\n")
            self._retracte(d, "c7-nul-corrige-resultats.md")
            commit(d, "Audit : renversement + retractation")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)

    # --- les quatre faux positifs du 12/09/2026 -----------------------------
    # Quatre PR bloquees a tort en une journee par la porte par inference.
    # Chacun de ces quatre commits ne declare RIEN : ils doivent passer.

    def test_passage_faux_positif_1_renvoi_attribue_au_mauvais_fichier(self):
        """FP n°1 : un renvoi §N dans une phrase qui cite deux fichiers. Le mot
        d'invalidation portait sur l'un, la porte l'a attribue a l'autre."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md",
                         "\nVoir §2.7 : l'hypothese H2 de audit.md est refutee ; "
                         "les mesures de c7-nul-corrige-resultats.md restent lisibles.\n")
            commit(d, "Audit : renvoi interne")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)

    def test_passage_faux_positif_2_identifiant_de_registre_csv(self):
        """FP n°2 : un identifiant de registre nomme
        « pmm-k10-top1-ferme-contre-examen » a fait croire a la porte qu'un CSV
        declarait un rapport invalide, et a bloque une PR a tort."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            (d / "resultats" / "registre-chiffres.csv").write_text(
                "id,grandeur\n"
                "pmm-k10-contre-examen,\"PMM k=10 ; voir "
                "c7-nul-corrige-resultats.md refute\"\n",
                encoding="utf-8")
            commit(d, "Registre : une grandeur de plus")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)

    def test_passage_faux_positif_3_mot_et_fichier_distants_de_360_caracteres(self):
        """FP n°3 : un mot d'invalidation et un nom de fichier a 360 caracteres
        l'un de l'autre dans le meme paragraphe. Aucun lien entre les deux."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            remplissage = ("La campagne R6 a produit six rapports dont la "
                           "comparabilite reste a etablir, et la discussion de "
                           "methode qui suit ne porte sur aucun d'eux en "
                           "particulier mais sur la facon dont le projet traite "
                           "les renversements en general, ce qui demande un "
                           "detour un peu long, dont le seul objet est de mettre "
                           "assez de texte entre le mot d'invalidation et le nom "
                           "de fichier pour reproduire exactement le troisieme "
                           "faux positif du 12 septembre 2026. ")
            self.assertGreater(len(remplissage), 360)
            self._ajoute(d, "audit.md",
                         "\nL'hypothese initiale est refutee. " + remplissage
                         + "Le lecteur se reportera a c7-nul-corrige-resultats.md.\n")
            commit(d, "Audit : discussion de methode")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)

    def test_passage_faux_positif_4_negation(self):
        """FP n°4, le plus net : « ils ne sont pas invalides ». La porte y voyait
        une invalidation, faute de savoir lire une negation — et aucun raffinement
        du vocabulaire ne l'aurait jamais su."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md",
                         "\nLes chiffres de c7-nul-corrige-resultats.md sont "
                         "conserves : ils ne sont pas invalides par cet audit, "
                         "et rien n'y est retracte.\n")
            commit(d, "Audit : ce qui tient")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)

    def test_passage_indice_de_prose_signale_mais_ne_bloque_pas(self):
        """Le faux negatif assume — une invalidation en prose sans marqueur — n'est
        rattrapable que par un filet large. Il rend des NOTES, jamais un verdict."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md",
                         "\nLe rapport c7-nul-corrige-resultats.md est refute.\n")
            commit(d, "Audit : renversement sans marqueur")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)
            self.assertNotIn("indice", sortie)
            code, sortie = self._dans(
                d, ["--retractation", "--depuis", base, "--indice-prose"])
            self.assertPasse(code, sortie)
            self.assertIn("indice (NON bloquant", sortie)
            self.assertIn("c7-nul-corrige-resultats.md", sortie)

    def test_passage_marqueur_cite_en_bloc_de_code(self):
        """La documentation et les rapports qui PARLENT du marqueur doivent
        pouvoir le citer : indente ou entre backticks, il ne declenche rien."""
        with tempfile.TemporaryDirectory() as t:
            d, base = self._depot(t)
            self._ajoute(d, "audit.md",
                         "\nOn declare une retractation ainsi :\n\n"
                         "    RETRACTE: resultats/c7-nul-corrige-resultats.md\n\n"
                         "soit, en ligne, `RETRACTE: "
                         "resultats/c7-nul-corrige-resultats.md`.\n")
            commit(d, "Audit : documentation du marqueur")
            code, sortie = self._dans(d, ["--retractation", "--depuis", base])
            self.assertPasse(code, sortie)


if __name__ == "__main__":
    unittest.main()
