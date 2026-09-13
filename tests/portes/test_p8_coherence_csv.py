"""P8 vue echouer, et vue passer — sur la faute reelle du 13/09/2026.

Regle G0.5 : « un controle qu'on n'a jamais vu echouer n'est pas un controle ».
Le cas fautif n'est pas invente : c'est la phrase de
`c7-controle-generateur-resultats.md` §3 destinee au manuscrit, « ne depasse
0,15 % », confrontee au 0,0015354713 de `resultats/c7-controle-generateur.csv`
(ligne jeu=Twin / table=verdict, colonne meilleur_classique_top1). Le test lit le
CSV REEL du depot : si un jour la valeur change, le test le dira.
"""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from socle import CasDePorte, lance

CSV_REEL = "resultats/c7-controle-generateur.csv"
SEL_TWIN = "jeu=Twin ; table=verdict"
COL = "meilleur_classique_top1"

ENTETE = "# Rapport jouet\n\nstatut: courant\n\n"


def marqueur(valeur: str, sens: str, colonne: str = COL,
             csv_rel: str = CSV_REEL, selecteurs: str = SEL_TWIN,
             echelle: str = "x100") -> str:
    return f"CHIFFRE: {valeur} | {csv_rel} | {colonne} | {selecteurs} | {echelle} | {sens}\n"


class TestP8(CasDePorte):

    def _fichier(self, tmp: Path, corps: str, nom="r.md") -> Path:
        d = tmp / "resultats"
        d.mkdir(exist_ok=True)
        p = d / nom
        p.write_text(ENTETE + corps, encoding="utf-8")
        return p

    def _lance(self, p: Path, *extra: str):
        return lance("coherence_csv", ["--sans-registre", "--fichier", str(p), *extra])

    # --- LE cas : la borne franchie du 13/09 --------------------------------

    def test_echec_borne_franchie_015_contre_01535(self):
        """« ne depasse 0,15 % » alors que le CSV porte 0,1535 %.

        C'est la faute publiee dans la phrase destinee au manuscrit. La porte
        doit la refuser SANS lire un mot de la prose qui l'entoure.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t),
                              "Aucun generateur classique ne depasse 0,15 % (Twin).\n\n"
                              + marqueur("0,15", "max"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "BORNE FRANCHIE")
            self.assertIn("0.1535", sortie.replace(",", "."))

    def test_passage_meme_borne_du_bon_cote_016(self):
        """« 0,16 % » — la borne que le §1 du meme rapport ecrivait deja juste.

        Un arrondi qui reste du BON cote est accepte : la porte ne punit pas
        l'arrondi, elle punit le franchissement.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,16", "max"))
            self.assertPasse(*self._lance(p))

    def test_echec_01535_annonce_comme_borne(self):
        """La valeur RETABLIE par l'audit, si on l'annonce comme un plafond.

        Constat inattendu et conserve tel quel : le CSV porte 0,15354713, donc
        « ne depasse 0,1535 % » franchit encore la valeur, de 4,7e-5 point. La
        correction du 13/09 retablit la bonne VALEUR, mais la phrase reste, a la
        lettre, une borne franchie. Une borne s'arrondit vers le haut : 0,1536.
        La porte dit cela, et il n'y a rien a assouplir — assouplir un plafond
        d'un demi-rang, c'est reintroduire exactement le defaut qu'elle ferme.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,1535", "max"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "BORNE FRANCHIE")

    def test_passage_01535_publiee_comme_valeur(self):
        """La meme graphie, declaree pour ce qu'elle est : une valeur, pas une
        borne. C'est la forme correcte, et la porte l'accepte."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,1535", "exact"))
            self.assertPasse(*self._lance(p))

    def test_passage_borne_arrondie_vers_le_haut(self):
        """0,1536 : le plafond correct a quatre decimales."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,1536", "max"))
            self.assertPasse(*self._lance(p))

    def test_passage_borne_a_trois_decimales(self):
        """0,154 : le plafond correct a trois decimales (le §2 l'ecrivait deja)."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,154", "max"))
            self.assertPasse(*self._lance(p))

    def test_passage_015_en_sens_exact(self):
        """0,15 EST l'arrondi correct de 0,1535 a deux decimales.

        En `exact`, la porte l'accepte — et c'est deliberé : la faute n'etait pas
        l'arrondi, c'etait de l'annoncer comme un plafond. Une porte qui refuserait
        les deux confondrait deux choses differentes et deviendrait bruyante.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,15", "exact"))
            self.assertPasse(*self._lance(p))

    def test_echec_arrondi_faux_dun_rang_entier(self):
        """0,14 % n'est l'arrondi de rien : l'ecart depasse la precision ecrite."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,14", "exact"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "ecart")

    def test_echec_plancher_franchi(self):
        """`min` : « au moins 0,16 % » quand le reel vaut 0,1535 % est faux."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,16", "min"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "BORNE FRANCHIE")

    def test_passage_deuxieme_ligne_du_meme_csv(self):
        """Park : 2,27 % contre 0,0226616 au CSV — l'autre correction du 13/09."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t),
                              marqueur("2,27", "exact", selecteurs="jeu=Stanford ; table=verdict"))
            self.assertPasse(*self._lance(p))

    def test_echec_23_pour_park_annonce_comme_plafond(self):
        """« 2,3 % (Park et al.) », l'autre arrondi de la meme phrase.

        2,3 >= 2,2662 : la borne n'est PAS franchie, mais le sens `exact` le
        refuserait-il ? Non : |2,3 - 2,2662| = 0,034 < 0,1. La porte accepte,
        et c'est correct — 2,3 est un arrondi fidele. Ce test fixe cette limite
        pour qu'elle ne soit pas durcie par megarde.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t),
                              marqueur("2,3", "exact", selecteurs="jeu=Stanford ; table=verdict"))
            self.assertPasse(*self._lance(p))

    # --- une declaration irresolvable n'est jamais ignoree en silence -------

    def test_echec_colonne_inconnue(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,15", "max", colonne="top1_inexistant"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "absente")

    def test_echec_selecteurs_ambigus(self):
        """Un selecteur qui designe plusieurs lignes ne choisit pas au hasard."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,15", "max", selecteurs="table=verdict"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "exactement une")

    def test_echec_selecteurs_sans_correspondance(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,15", "max", selecteurs="jeu=Jamais"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "0 ligne")

    def test_echec_csv_introuvable(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t),
                              marqueur("0,15", "max", csv_rel="resultats/jamais-ecrit.csv"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "introuvable")

    def test_echec_marqueur_mal_forme(self):
        """Une faute de frappe ne doit pas desarmer la regle en silence."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), "CHIFFRE: 0,15 | resultats/x.csv | col\n")
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "champ(s) au lieu de 6")

    def test_echec_sens_inconnu(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), marqueur("0,15", "plafond"))
            code, sortie = self._lance(p)
            self.assertEchoue(code, sortie, "sens")

    # --- la prose ne declenche JAMAIS la porte ------------------------------

    def test_passage_prose_qui_contient_le_chiffre_faux(self):
        """La phrase fautive elle-meme, SANS marqueur : la porte ne dit rien.

        Faux negatif assume. C'est le prix explicite de zero faux positif : la
        porte ne lit pas la prose, donc un chiffre non rattache lui echappe.
        """
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t),
                              "Aucun generateur classique ne depasse 0,15 % (Twin-2K-500), "
                              "contre 2,3 % chez Park et al.\n")
            self.assertPasse(*self._lance(p))

    def test_passage_marqueur_cite_indente(self):
        """Citer le marqueur sans le declencher : l'indenter (comme pour P4)."""
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), "    " + marqueur("0,15", "max"))
            self.assertPasse(*self._lance(p))

    def test_passage_marqueur_dans_un_bloc_de_code(self):
        with tempfile.TemporaryDirectory() as t:
            p = self._fichier(Path(t), "```\n" + marqueur("0,15", "max") + "```\n")
            self.assertPasse(*self._lance(p))

    # --- controle (b) : registre <-> CSV ------------------------------------

    def test_echec_registre_valeur_incoherente(self):
        """Une ligne de registre qui declare `colonne=` et se trompe de valeur."""
        with tempfile.TemporaryDirectory() as t:
            reg = Path(t) / "registre.csv"
            reg.write_text(
                "id,grandeur,valeur,ic_bas,ic_haut,methode_ic,n_replicats,graine,"
                "script,commit,csv_source,statut\n"
                "faux,\"plafond classique Twin\",0.99,,,,,,s.py,abc,"
                f"\"{CSV_REEL} (colonne=meilleur_classique_top1; echelle=x100; "
                "jeu=Twin; table=verdict)\",courant\n",
                encoding="utf-8")
            code, sortie = lance("coherence_csv",
                                 ["--registre", str(reg), "--registre-seul"])
            self.assertEchoue(code, sortie, "ecart")

    def test_passage_registre_valeur_coherente(self):
        with tempfile.TemporaryDirectory() as t:
            reg = Path(t) / "registre.csv"
            reg.write_text(
                "id,grandeur,valeur,ic_bas,ic_haut,methode_ic,n_replicats,graine,"
                "script,commit,csv_source,statut\n"
                "juste,\"plafond classique Twin\",0.1535,,,,,,s.py,abc,"
                f"\"{CSV_REEL} (colonne=meilleur_classique_top1; echelle=x100; "
                "jeu=Twin; table=verdict)\",courant\n",
                encoding="utf-8")
            code, sortie = lance("coherence_csv",
                                 ["--registre", str(reg), "--registre-seul"])
            self.assertPasse(code, sortie)

    def test_passage_registre_reel_du_depot(self):
        """Le registre du depot ne declare aucun `colonne=` : la porte se tait.

        Elle DOIT se taire — un controle dormant ne signale rien. Ce test fixe ce
        comportement pour que la migration ne soit pas confondue avec une panne.
        """
        code, sortie = lance("coherence_csv", ["--registre-seul"])
        self.assertPasse(code, sortie)
        self.assertIn("sans selecteur", sortie)

    # --- le depot entier ----------------------------------------------------

    def test_passage_depot_entier(self):
        """Mesure du bruit : la porte sur tout resultats/ et article/."""
        code, sortie = lance("coherence_csv", ["--tous"])
        self.assertPasse(code, sortie)


if __name__ == "__main__":
    unittest.main()
