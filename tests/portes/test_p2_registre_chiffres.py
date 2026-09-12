"""P2 vu echouer, et vu passer."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from socle import RACINE, CasDePorte, lance

ENTETE = ("id,grandeur,valeur,ic_bas,ic_haut,methode_ic,n_replicats,graine,"
          "script,commit,csv_source,statut\n")
LIGNE_OK = ("t1,Twin top-1,20.7,19.0,22.4,bootstrap percentile,2000,20260911,"
            "analyses/c7_reidentification.py,931916c,resultats/c7-reidentification.csv,"
            "courant\n")


def registre(tmp: Path, corps: str) -> Path:
    p = tmp / "registre-chiffres.csv"
    p.write_text(ENTETE + corps, encoding="utf-8")
    return p


class TestP2(CasDePorte):

    # --- (c) chiffres en dur ------------------------------------------------

    def test_echec_nombre_en_dur_deux_decimales(self):
        """Le coeur de la porte : « 60,17 % » tape a la main est refuse."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            r = registre(tmp, LIGNE_OK)
            m = tmp / "manuscrit.md"
            m.write_text(
                "A 1 % de fausses accusations, l'attaquant a raison 60,17 % du temps.\n",
                encoding="utf-8")
            code, sortie = lance("registre_chiffres",
                                 ["--fichier", str(m), "--registre", str(r)])
            self.assertEchoue(code, sortie, "60,17")
            self.assertIn("hors motif", sortie)

    def test_passage_nombre_remplace_par_un_renvoi(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            r = registre(tmp, LIGNE_OK)
            m = tmp / "manuscrit.md"
            m.write_text("Le top-1 vaut {{R:t1}} %.\n", encoding="utf-8")
            code, sortie = lance("registre_chiffres",
                                 ["--fichier", str(m), "--registre", str(r)])
            self.assertPasse(code, sortie)

    def test_passage_doi_et_arxiv_ne_sont_pas_des_mesures(self):
        """Exclusion declaree : un DOI n'est pas un chiffre publie."""
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            r = registre(tmp, LIGNE_OK)
            m = tmp / "biblio.md"
            m.write_text("Harvard Dataverse 10.7910/DVN/JPV20K ; arXiv 2406.16201.\n",
                         encoding="utf-8")
            code, sortie = lance("registre_chiffres",
                                 ["--fichier", str(m), "--registre", str(r)])
            self.assertPasse(code, sortie)

    def test_passage_bloc_de_code(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            r = registre(tmp, LIGNE_OK)
            m = tmp / "code.md"
            m.write_text("Sortie :\n\n```\nrho = 0.9741\n```\n", encoding="utf-8")
            code, sortie = lance("registre_chiffres",
                                 ["--fichier", str(m), "--registre", str(r)])
            self.assertPasse(code, sortie)

    # --- (b) renvois --------------------------------------------------------

    def test_echec_renvoi_inconnu(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            r = registre(tmp, LIGNE_OK)
            m = tmp / "m.md"
            m.write_text("Valeur : {{R:inexistant}}.\n", encoding="utf-8")
            code, sortie = lance("registre_chiffres",
                                 ["--fichier", str(m), "--registre", str(r)])
            self.assertEchoue(code, sortie, "absent du registre")

    def test_echec_renvoi_vers_ligne_retractee(self):
        with tempfile.TemporaryDirectory() as t:
            tmp = Path(t)
            r = registre(tmp, LIGNE_OK + (
                "t2,ancien nul,31.15,ABSENT,ABSENT,ABSENT,ABSENT,ABSENT,"
                "analyses/c7_disjoint.py,37b58b2,resultats/c7-disjoint-nul.csv,retracte\n"))
            m = tmp / "m.md"
            m.write_text("Valeur : {{R:t2}}.\n", encoding="utf-8")
            code, sortie = lance("registre_chiffres",
                                 ["--fichier", str(m), "--registre", str(r)])
            self.assertEchoue(code, sortie, "RETRACTEE")

    # --- (a) integrite du registre -----------------------------------------

    def test_echec_id_en_double(self):
        """v1 §2.6 : deux mesures differentes, deux id — et un id ne sert qu'une fois."""
        with tempfile.TemporaryDirectory() as t:
            r = registre(Path(t), LIGNE_OK + LIGNE_OK)
            code, sortie = lance("registre_chiffres",
                                 ["--registre", str(r), "--registre-seul"])
            self.assertEchoue(code, sortie, "deja utilise")

    def test_echec_absent_avec_statut_courant(self):
        """Le champ dont l'absence a produit 31,15 vs 31,62 % (v1 §4.3)."""
        with tempfile.TemporaryDirectory() as t:
            r = registre(Path(t), (
                "t3,grandeur sans graine,36.4,ABSENT,ABSENT,ABSENT,ABSENT,ABSENT,"
                "analyses/c7_transfert.py,921635d,resultats/c7-transfert-voletA.csv,"
                "courant\n"))
            code, sortie = lance("registre_chiffres",
                                 ["--registre", str(r), "--registre-seul"])
            self.assertEchoue(code, sortie, "ABSENT mais porte statut courant")

    def test_echec_colonne_obligatoire_vide(self):
        with tempfile.TemporaryDirectory() as t:
            r = registre(Path(t), "t4,sans script,1.0,,,,,,,,,courant\n")
            code, sortie = lance("registre_chiffres",
                                 ["--registre", str(r), "--registre-seul"])
            self.assertEchoue(code, sortie, "script")

    def test_echec_entete_non_conforme(self):
        with tempfile.TemporaryDirectory() as t:
            p = Path(t) / "faux.csv"
            p.write_text("id,valeur\nt1,20.7\n", encoding="utf-8")
            code, sortie = lance("registre_chiffres",
                                 ["--registre", str(p), "--registre-seul"])
            self.assertEchoue(code, sortie, "au lieu des colonnes du §1.3")

    # --- le registre reel du depot doit etre propre -------------------------

    def test_passage_registre_du_depot(self):
        code, sortie = lance("registre_chiffres", ["--registre-seul"])
        self.assertPasse(code, sortie)


if __name__ == "__main__":
    unittest.main()
