"""P9 vue echouer, et vue passer — sur le run arrete a 20 replicats.

Cas fautif reel du 13/09/2026 : `c7-nul-corrige-preenregistrement.md` §5
prescrivait 100 replicats, `int(os.environ.get("NREP", "20"))` en a fait 20, et
rho 0,974 [0,950 ; 0,993] a ete publie au tableau 1 puis envoye a un tiers. Les
tests rejouent les deux lignes reelles du registre : celle a 20 (la porte se
ferme) et celle a 100 qui l'a remplacee (la porte passe).
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from socle import RACINE, CasDePorte, lance

DOUZE = ("id,grandeur,valeur,ic_bas,ic_haut,methode_ic,n_replicats,graine,"
         "script,commit,csv_source,statut")
MIGRE = DOUZE + ",preenregistrement,n_replicats_prescrit"
PLAN = "resultats/c7-nul-corrige-preenregistrement.md"


def ligne(ident: str, n_replicats: str, plan: str = PLAN, prescrit: str = "100",
          statut: str = "courant") -> str:
    return (f'{ident},"rho du nul de marge appariee",0.974,0.950,0.993,'
            f'centiles 5/95,{n_replicats},20260912,analyses/c7_temoin.py,218c955,'
            f'resultats/c7-nul-corrige-marginal.csv,{statut},{plan},{prescrit}\n')


class TestP9(CasDePorte):

    def _registre(self, tmp: Path, contenu: str) -> Path:
        p = tmp / "registre.csv"
        p.write_text(contenu, encoding="utf-8")
        return p

    def _lance(self, p: Path, *extra: str):
        return lance("conformite_preenregistrement",
                     ["--registre", str(p), *extra])

    # --- LE cas : 20 replicats pour 100 prescrits ---------------------------

    def test_echec_run_arrete_a_20_pour_100_prescrits(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), MIGRE + "\n"
                               + ligne("rho-nul-marge-appariee-12conf", "20"))
            code, sortie = self._lance(p, "--exiger-colonnes")
            self.assertEchoue(code, sortie, "20 replicats alors que")
            self.assertIn("100", sortie)

    def test_passage_serie_a_100_replicats(self):
        """La ligne qui l'a remplacee : 100 effectifs, 100 prescrits."""
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), MIGRE + "\n"
                               + ligne("rho-nul-marge-appariee-12conf-n100", "100"))
            self.assertPasse(*self._lance(p, "--exiger-colonnes"))

    def test_echec_run_plus_long_que_le_plan(self):
        """Un run plus long n'est pas non plus le plan : la loi nulle change."""
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), MIGRE + "\n" + ligne("trop-long", "500"))
            code, sortie = self._lance(p, "--exiger-colonnes")
            self.assertEchoue(code, sortie, "500 replicats alors que")

    # --- ce que la porte refuse de deviner ----------------------------------

    def test_echec_n_replicats_non_comparable(self):
        """« 1 passe ; 20 tirages de departage » : deux entiers, un piege.

        La porte refuse de choisir. C'est la graphie reelle de plusieurs lignes
        du registre ; elle doit etre rendue comparable, pas interpretee.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(
                Path(t), MIGRE + "\n"
                + 'ambigu,"factoriel",0.67,0.00,1.75,bootstrap,'
                  '"1 passe ; 20 tirages ; 2000 bootstrap",20260912,a.py,ee73f70,'
                  f'resultats/c7-factoriel.csv,courant,{PLAN},20\n')
            code, sortie = self._lance(p, "--exiger-colonnes")
            self.assertEchoue(code, sortie, "n'est pas un entier comparable")

    def test_echec_prescription_non_entiere(self):
        """« 100 par configuration » n'est pas un entier nu : refuse."""
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(
                Path(t), MIGRE + "\n"
                + ligne("prose", "100", prescrit='"100 par configuration"'))
            code, sortie = self._lance(p, "--exiger-colonnes")
            self.assertEchoue(code, sortie, "n'est pas un entier > 0")

    def test_echec_prescription_sans_plan(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), MIGRE + "\n"
                               + ligne("orphelin", "100", plan="ABSENT"))
            code, sortie = self._lance(p, "--exiger-colonnes")
            self.assertEchoue(code, sortie, "sans nommer le plan")

    def test_echec_plan_introuvable(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), MIGRE + "\n"
                               + ligne("fantome", "100",
                                       plan="resultats/jamais-ecrit.md"))
            code, sortie = self._lance(p, "--exiger-colonnes")
            self.assertEchoue(code, sortie, "introuvable")

    def test_passage_sans_prescription_declaree(self):
        """ABSENT : aucun plan ne prescrit de nombre. La porte se tait."""
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), MIGRE + "\n"
                               + ligne("libre", "2000", plan="ABSENT",
                                       prescrit="ABSENT"))
            self.assertPasse(*self._lance(p, "--exiger-colonnes"))

    def test_passage_ligne_retractee_hors_perimetre(self):
        """Une ligne deja retractee n'est plus opposable : hors perimetre.

        Sans cette regle, la porte rouvrirait eternellement un defaut deja
        reconnu, corrige et documente — le bruit typique qui fait desarmer une
        porte.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), MIGRE + "\n"
                               + ligne("deja-retracte", "20", statut="retracte"))
            self.assertPasse(*self._lance(p, "--exiger-colonnes"))

    # --- avant migration : la porte ne bloque pas ---------------------------

    def test_passage_colonnes_absentes_sans_exigence(self):
        """Registre a douze colonnes : la porte le dit et sort en 0."""
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), DOUZE + "\n")
            code, sortie = self._lance(p)
            self.assertPasse(code, sortie)
            self.assertIn("ne controle RIEN", sortie)

    def test_echec_colonnes_absentes_avec_exigence(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), DOUZE + "\n")
            code, sortie = self._lance(p, "--exiger-colonnes")
            self.assertEchoue(code, sortie, "absente(s) du registre")

    def test_passage_registre_reel_du_depot(self):
        """Le registre du depot n'est pas migre : la porte ne bloque rien."""
        code, sortie = lance("conformite_preenregistrement", [])
        self.assertPasse(code, sortie)

    def test_echec_registre_reel_si_on_exige_les_colonnes(self):
        """Et elle dit exactement ce qui manque quand on le lui demande."""
        code, sortie = lance("conformite_preenregistrement", ["--exiger-colonnes"])
        self.assertEchoue(code, sortie, "preenregistrement")

    def test_procedure_migration_imprimee(self):
        code, sortie = lance("conformite_preenregistrement",
                             ["--procedure-migration"])
        self.assertEqual(code, 0, sortie)
        self.assertIn("n_replicats_prescrit", sortie)

    # --- la migration ne doit pas casser P2 --------------------------------

    def test_passage_p2_accepte_le_registre_migre(self):
        """Les deux colonnes ajoutees en fin d'en-tete passent P2.

        C'est l'etape 3 de la procedure : sans elle, migrer le registre fermerait
        P2 au meme commit et la migration serait impossible a livrer d'un bloc.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), MIGRE + "\n"
                               + ligne("rho-n100", "100"))
            code, sortie = lance("registre_chiffres",
                                 ["--registre", str(p), "--registre-seul"])
            self.assertPasse(code, sortie)

    def test_echec_p2_refuse_une_colonne_non_declaree(self):
        """La tolerance de P2 est nommee, pas generale."""
        with tempfile.TemporaryDirectory() as t:
            p = self._registre(Path(t), DOUZE + ",colonne_inventee\n")
            code, sortie = lance("registre_chiffres",
                                 ["--registre", str(p), "--registre-seul"])
            self.assertEchoue(code, sortie, "au lieu des colonnes du §1.3")

    def test_plan_reel_existe(self):
        """Le preenregistrement cite par les tests est bien celui du depot."""
        self.assertTrue((RACINE / PLAN).exists(), PLAN)


if __name__ == "__main__":
    unittest.main()
