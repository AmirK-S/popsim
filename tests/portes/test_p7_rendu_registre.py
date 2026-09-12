"""Tests du script de rendu `outils/rendu_registre.py` — Methode v2 §1.3.

Regle G0.5 de la v1 : « un controle qu'on n'a jamais vu echouer n'est pas un
controle ». Le rendu est le pendant du §1.3 : il doit REFUSER de rendre plutot
que de rendre quelque chose de faux. Les cas d'echec ci-dessous sont donc la
partie utile du fichier.

Les trois echecs exiges par le mandat sont `test_echec_identifiant_inconnu`,
`test_echec_ligne_retractee` et `test_echec_champ_vide` ; les autres couvrent
les modes de defaillance voisins (ABSENT, champ inconnu, registre malforme,
id en double) parce qu'ils produiraient le meme degat : un chiffre publie que
personne n'a etabli.
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
RENDU = RACINE / "outils" / "rendu_registre.py"

COLONNES = ("id,grandeur,valeur,ic_bas,ic_haut,methode_ic,n_replicats,graine,"
            "script,commit,csv_source,statut")

# Une ligne saine, dont chaque test ne degrade qu'un champ a la fois.
SAINE = ("g1,grandeur de test,20.7,19.0,22.4,bootstrap percentile sur les personnes,"
         "2000,20260911,analyses/x.py,abc1234,resultats/x.csv,courant")


def lance(argv: list[str]) -> tuple[int, str]:
    res = subprocess.run([sys.executable, str(RENDU), *argv],
                         capture_output=True, text=True, cwd=str(RACINE))
    return res.returncode, res.stdout + res.stderr


class CasDeRendu(unittest.TestCase):

    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp.name)
        self.addCleanup(self._tmp.cleanup)

    def prepare(self, lignes: list[str], texte: str) -> tuple[str, str]:
        reg = self.tmp / "registre.csv"
        reg.write_text("\n".join([COLONNES, *lignes]) + "\n", encoding="utf-8")
        src = self.tmp / "source.md"
        src.write_text(texte, encoding="utf-8")
        return str(src), str(reg)

    def assertEchoue(self, code: int, sortie: str, motif: str) -> None:
        self.assertEqual(code, 1, f"le rendu aurait du refuser.\n{sortie}")
        self.assertIn(motif, sortie)

    # ------------------------------------------------------------------ #
    # ECHECS — les trois exiges                                          #
    # ------------------------------------------------------------------ #

    def test_echec_identifiant_inconnu(self) -> None:
        src, reg = self.prepare([SAINE], "Le taux vaut {{R:g_inexistant}} %.\n")
        code, sortie = lance(["--fichier", src, "--registre", reg])
        self.assertEchoue(code, sortie, "ABSENT du registre")

    def test_echec_ligne_retractee(self) -> None:
        retractee = SAINE.replace("g1,", "g1,").replace(",courant", ",retracte")
        src, reg = self.prepare([retractee], "Le taux vaut {{R:g1}} %.\n")
        code, sortie = lance(["--fichier", src, "--registre", reg])
        self.assertEchoue(code, sortie, "RETRACTEE")

    def test_echec_champ_vide(self) -> None:
        # `csv_source` vide : la grandeur n'a pas de provenance.
        vide = SAINE.replace(",resultats/x.csv,", ",,")
        src, reg = self.prepare([vide], "Le taux vaut {{R:g1}} %.\n")
        code, sortie = lance(["--fichier", src, "--registre", reg])
        self.assertEchoue(code, sortie, "VIDE")

    # ------------------------------------------------------------------ #
    # ECHECS — modes voisins, meme degat                                 #
    # ------------------------------------------------------------------ #

    def test_echec_champ_absent_non_rendu(self) -> None:
        """Un champ ABSENT ne se rend pas : ce serait publier un faux."""
        sans_ic = SAINE.replace(",19.0,22.4,", ",ABSENT,ABSENT,")
        src, reg = self.prepare([sans_ic], "Le taux vaut {{R:g1}} {{R:g1.ic}}.\n")
        code, sortie = lance(["--fichier", src, "--registre", reg])
        self.assertEchoue(code, sortie, "vaut ABSENT")

    def test_echec_champ_inconnu(self) -> None:
        src, reg = self.prepare([SAINE], "Voir {{R:g1.intervalle}}.\n")
        code, sortie = lance(["--fichier", src, "--registre", reg])
        self.assertEchoue(code, sortie, "champ « intervalle » INCONNU")

    def test_echec_id_en_double(self) -> None:
        src, reg = self.prepare([SAINE, SAINE.replace("20.7", "23.2")],
                                "Le taux vaut {{R:g1}} %.\n")
        code, sortie = lance(["--fichier", src, "--registre", reg])
        self.assertEchoue(code, sortie, "deja utilise")

    def test_echec_registre_malforme(self) -> None:
        reg = self.tmp / "registre.csv"
        reg.write_text("id,valeur\ng1,20.7\n", encoding="utf-8")
        src = self.tmp / "source.md"
        src.write_text("{{R:g1}}\n", encoding="utf-8")
        code, sortie = lance(["--fichier", str(src), "--registre", str(reg)])
        self.assertEchoue(code, sortie, "colonnes du §1.3")

    def test_echec_rien_n_est_ecrit_en_cas_de_probleme(self) -> None:
        """Un rendu partiel est pire qu'un refus : le fichier ne doit pas naitre."""
        src, reg = self.prepare([SAINE], "{{R:g1}} puis {{R:inconnu}}.\n")
        sortie_attendue = self.tmp / "rendu.md"
        code, _ = lance(["--fichier", src, "--registre", reg,
                         "--sortie", str(sortie_attendue)])
        self.assertEqual(code, 1)
        self.assertFalse(sortie_attendue.exists(),
                         "un fichier a ete ecrit malgre l'echec")

    def test_echec_verifier_signale_sans_rendre(self) -> None:
        src, reg = self.prepare([SAINE], "{{R:inconnu}}\n")
        code, sortie = lance(["--fichier", src, "--registre", reg, "--verifier"])
        self.assertEchoue(code, sortie, "ABSENT du registre")

    def test_code_2_si_fichier_absent(self) -> None:
        _, reg = self.prepare([SAINE], "")
        code, sortie = lance(["--fichier", str(self.tmp / "pasla.md"),
                              "--registre", reg])
        self.assertEqual(code, 2, sortie)
        self.assertIn("IMPOSSIBLE D'EXECUTER", sortie)

    # ------------------------------------------------------------------ #
    # PASSAGES                                                            #
    # ------------------------------------------------------------------ #

    def test_passage_valeur_et_ic(self) -> None:
        src, reg = self.prepare(
            [SAINE], "Le taux vaut {{R:g1}} % {{R:g1.ic}} selon {{R:g1.methode_ic}}.\n")
        rendu = self.tmp / "rendu.md"
        code, sortie = lance(["--fichier", src, "--registre", reg,
                              "--sortie", str(rendu)])
        self.assertEqual(code, 0, sortie)
        self.assertEqual(
            rendu.read_text(encoding="utf-8"),
            "Le taux vaut 20.7 % [19.0 ; 22.4] selon bootstrap percentile "
            "sur les personnes.\n")

    def test_passage_substitution_verbatim_sans_reformatage(self) -> None:
        """La graphie est celle du registre : ni arrondi, ni conversion."""
        graphie = SAINE.replace(",20.7,", ",0.13,")
        src, reg = self.prepare([graphie], "{{R:g1}}\n")
        code, _ = lance(["--fichier", src, "--registre", reg,
                         "--sortie", str(self.tmp / "r.md")])
        self.assertEqual(code, 0)
        self.assertEqual((self.tmp / "r.md").read_text(encoding="utf-8"), "0.13\n")

    def test_passage_ligne_provisoire_est_rendable(self) -> None:
        """`provisoire` n'est pas `retracte` : la ligne se rend."""
        prov = SAINE.replace(",courant", ",provisoire")
        src, reg = self.prepare([prov], "{{R:g1}}\n")
        code, sortie = lance(["--fichier", src, "--registre", reg])
        self.assertEqual(code, 0, sortie)

    def test_passage_verifier_sur_le_registre_reel(self) -> None:
        """Le registre du depot doit rester rendable : c'est un test de non-regression."""
        src = self.tmp / "s.md"
        src.write_text("{{R:twin-top1-ferme-json41-naif}} "
                       "{{R:twin-top1-ferme-json41-naif.ic}}\n", encoding="utf-8")
        code, sortie = lance(["--fichier", str(src), "--verifier"])
        self.assertEqual(code, 0, sortie)

    def test_passage_fichier_sans_renvoi_est_identique(self) -> None:
        src, reg = self.prepare([SAINE], "Aucun renvoi ici.\nDeux lignes.\n")
        code, _ = lance(["--fichier", src, "--registre", reg,
                         "--sortie", str(self.tmp / "r.md")])
        self.assertEqual(code, 0)
        self.assertEqual((self.tmp / "r.md").read_text(encoding="utf-8"),
                         "Aucun renvoi ici.\nDeux lignes.\n")


if __name__ == "__main__":
    unittest.main()
