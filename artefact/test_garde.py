"""test_garde : verifie que artefact/garde.py refuse tout chemin qui, une
fois resolu (liens symboliques suivis, '.'/'..' elimines, casse normalisee),
mene reellement dans un dossier "data" -- quelle que soit la maniere dont ce
chemin a ete ecrit (casse, separateur, nom de variable d'environnement, lien
symbolique de nom neutre, chemin relatif ou absolu, chaine de liens, etc.).

Isolation : aucun test n'ecrit quoi que ce soit dans le vrai depot. Chaque
test construit sa propre arborescence jetable sous un dossier temporaire
(tempfile.TemporaryDirectory) qui imite la structure "<racine>/data" et
"<racine>/artefact", puis redirige `garde._DONNEES_INTERDITES` vers le
"data" de cette arborescence jetable (monkeypatch manuel, restaure dans
tearDown). Le vrai artefact/../data/ du depot n'est jamais lu ni modifie.

Usage : .venv/bin/python artefact/test_garde.py
   ou : .venv/bin/python -m unittest discover -s artefact -p "test_garde.py"
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

ICI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ICI)

import garde  # noqa: E402


class _BaseIsolee(unittest.TestCase):
    """Cree une arborescence jetable <tmp>/depot/{data,artefact}/ et redirige
    le dossier interdit de `garde` vers <tmp>/depot/data, pour ne jamais
    toucher au vrai depot. Restaure tout dans tearDown, y compris le
    dossier courant et les variables d'environnement touchees."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name).resolve()
        self.depot = self.tmp / "depot"
        self.data = self.depot / "data"
        self.artefact = self.depot / "artefact"
        (self.data / "twin2k500").mkdir(parents=True)
        self.artefact.mkdir(parents=True)
        (self.data / "twin2k500" / "reponses.csv").write_text("VRAIES_DONNEES\n")

        # getattr/hasattr : avant la correction, garde.py n'a pas encore
        # d'attribut _DONNEES_INTERDITES (l'ancienne version code le dossier
        # interdit en dur dans _suspect()) ; le setUp doit rester utilisable
        # tel quel pour pouvoir constater l'echec des tests sur l'ancien
        # code, pas seulement apres la correction.
        self._avait_attribut = hasattr(garde, "_DONNEES_INTERDITES")
        self._donnees_interdites_orig = getattr(garde, "_DONNEES_INTERDITES", None)
        garde._DONNEES_INTERDITES = self.data.resolve()

        self._cwd_orig = os.getcwd()
        os.chdir(self.depot)

        self._env_orig = dict(os.environ)

    def tearDown(self):
        os.chdir(self._cwd_orig)
        if self._avait_attribut:
            garde._DONNEES_INTERDITES = self._donnees_interdites_orig
        else:
            del garde._DONNEES_INTERDITES
        os.environ.clear()
        os.environ.update(self._env_orig)
        self._tmp.cleanup()

    # -- petits utilitaires communs --

    def assert_bloque(self, chemin, msg=None):
        self.assertTrue(garde._suspect(chemin), msg or f"aurait du etre refuse : {chemin!r}")

    def assert_autorise(self, chemin, msg=None):
        self.assertFalse(garde._suspect(chemin), msg or f"n'aurait pas du etre refuse : {chemin!r}")


class TestContournementsRapportes(_BaseIsolee):
    """Un test par contournement demontre par le relecteur dans
    resultats/artefact-reproduction-2026-09-12.md."""

    def test_difference_de_casse(self):
        self.assert_bloque("DATA/twin2k500/reponses.csv")
        self.assert_bloque("Data/twin2k500/reponses.csv")
        self.assert_bloque(str(self.depot / "DATA" / "twin2k500" / "reponses.csv"))

    def test_separateur_windows(self):
        # Ecrit avec la convention Windows alors qu'on tourne sur un systeme
        # POSIX : doit tout de meme etre juge comme visant data/.
        self.assert_bloque("data\\twin2k500\\reponses.csv")

    def test_variable_environnement_hors_liste_surveillee(self):
        # L'ancienne version ne surveillait que 4 noms fixes ; un nom
        # quelconque doit desormais aussi etre pris en compte.
        os.environ["POPSIM_TWIN_PATH"] = str(self.data / "twin2k500" / "reponses.csv")
        try:
            garde.verifier_environnement()
            self.fail("verifier_environnement() aurait du lever SystemExit")
        except SystemExit as e:
            self.assertEqual(e.code, 1)

    def test_variable_environnement_en_minuscules(self):
        os.environ["popsim_data"] = str(self.data)
        try:
            garde.verifier_environnement()
            self.fail("verifier_environnement() aurait du lever SystemExit")
        except SystemExit as e:
            self.assertEqual(e.code, 1)

    def test_lien_symbolique_de_nom_neutre(self):
        raccourci = self.artefact / "raccourci_prive"
        raccourci.symlink_to(self.data, target_is_directory=True)
        cible = raccourci / "twin2k500" / "reponses.csv"
        # Preuve que le lien symbolique lit reellement data/ (comme dans le
        # rapport du relecteur), avant de verifier que le garde le refuse.
        self.assertEqual(cible.read_text(), "VRAIES_DONNEES\n")
        self.assert_bloque(str(cible))


class TestContournementsSupplementaires(_BaseIsolee):
    """Vecteurs de contournement supplementaires, non demontres dans le
    rapport mais plausibles pour la meme classe de faille."""

    def test_chemin_relatif_remontant_en_dotdot(self):
        # cwd = self.depot : on grimpe hors d'un dossier autorise puis on
        # redescend dans data/ -- doit rester detecte apres normalisation,
        # comme le rapport du relecteur l'a lui-meme constate (tentative
        # echouee cote relecteur, donc deja correcte, mais couverte ici en
        # non-regression).
        self.assert_bloque("artefact/../data/twin2k500/reponses.csv")
        self.assert_bloque("artefact/donnees_fictives/../../data/twin2k500/reponses.csv")

    def test_chemin_absolu(self):
        self.assert_bloque(str(self.data / "twin2k500" / "reponses.csv"))

    def test_lien_symbolique_en_chaine(self):
        premier = self.artefact / "premier_maillon"
        second = self.artefact / "second_maillon"
        second.symlink_to(self.data, target_is_directory=True)
        premier.symlink_to(second, target_is_directory=True)
        cible = premier / "twin2k500" / "reponses.csv"
        self.assertEqual(cible.read_text(), "VRAIES_DONNEES\n")
        self.assert_bloque(str(cible))

    def test_jonction_de_casse_mixte_via_symlink(self):
        # Un lien symbolique dont le NOM n'evoque rien, mais dont la CIBLE
        # est ecrite dans une casse differente de celle du dossier reel.
        raccourci = self.artefact / "config_partagee"
        cible_ecrite = str(self.data).upper()
        raccourci.symlink_to(cible_ecrite, target_is_directory=True)
        chemin = raccourci / "twin2k500" / "reponses.csv"
        self.assert_bloque(str(chemin))

    def test_chemin_avec_points_intercales(self):
        self.assert_bloque("data/./twin2k500/../twin2k500/reponses.csv")
        self.assert_bloque(str(self.depot) + "/./data/twin2k500/reponses.csv")

    def test_non_suspect_ne_doit_pas_etre_bloque(self):
        # Controles negatifs : un dossier qui contient "data" comme sous-
        # chaine mais pas comme composant ancestral ne doit pas etre bloque,
        # ni les dossiers reellement autorises de l'artefact.
        self.assert_autorise("database/x.csv")
        self.assert_autorise("metadata/y.csv")
        self.assert_autorise(str(self.artefact / "donnees_fictives" / "personnes.csv"))
        self.assert_autorise(str(self.artefact / "resultats_artefact" / "attaque.csv"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
