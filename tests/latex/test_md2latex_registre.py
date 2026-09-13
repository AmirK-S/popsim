"""La chaine de rendu du registre dans md2latex.py, vue echouer et vue passer.

Regle G0.5 de la v1, reprise par `tests/portes/socle.py` : « un controle qu'on
n'a jamais vu echouer n'est pas un controle ».

LE DEFAUT QUE CES TESTS FERMENT
-------------------------------
Le §1.3 de la Methode v2 impose que le manuscrit ne tape aucune valeur : il cite
`{{R:id}}`, et `outils/rendu_registre.py` substitue depuis
`resultats/registre-chiffres.csv`. Jusqu'au 13/09/2026, `md2latex.py` **ne
l'appelait pas**. Le `main.tex` de la branche d'integration portait donc 51
marqueurs `{{R:...}}` litteraux, resume compris, et le PDF deposable aurait
affiche des accolades a la place de ses chiffres. Personne ne l'avait vu parce
que personne n'avait ouvert le PDF compile
(`resultats/relecture-post-nuit-2026-09-13.md`, defaut G1).

Le trou etait DELIBERE : l'agent d'integration avait juge qu'un echec bruyant
vaut mieux qu'un chiffre retracte qui a l'air juste. Ces tests verifient que la
fermeture du trou n'a pas perdu cette propriete — que la chaine **refuse**
plutot que de deviner, et que `main.tex` reste alors INTACT.

CE QUI EST VERIFIE, cas fautif d'abord :
  - `test_echec_id_absent`        : un id qui n'est pas au registre ;
  - `test_echec_ligne_retractee`  : un id dont la ligne porte `statut: retracte`
    — le cas dangereux, puisqu'une substitution silencieuse publierait un
    chiffre retracte qui a l'air juste ;
  - `test_echec_registre_absent`  : pas de registre du tout ;
  - `test_echec_renvoi_hors_zone_generee` : un `{{R:...}}` pose a la main dans
    `main.tex` HORS des zones GENERATED — le rendu du manuscrit ne peut pas le
    voir, c'est le garde-fou de SORTIE qui doit l'arreter ;
  - dans les quatre : code de sortie non nul, et `main.tex` octet pour octet
    identique a ce qu'il etait avant l'appel ;
  - `test_passage_*` : le cas correct est bien rendu, la valeur du registre
    apparait dans la zone generee, et aucun `{{R:` ne subsiste.

COMMENT ON LES A VUS ECHOUER (trace reelle, pas supposee). Comme
`test_md2latex_annexe.py`, ces tests s'executent contre un convertisseur passe
par la variable d'environnement `MD2LATEX`. Lances contre la version d'avant la
fermeture de la chaine --

    git show 8892e5c:article/latex/md2latex.py > /tmp/md2latex-avant.py
    MD2LATEX=/tmp/md2latex-avant.py python3 -m unittest test_md2latex_registre

-- les **sept** echouent. Les quatre `test_echec_*` parce que l'ancien
convertisseur rend 0 dans tous les cas fautifs, y compris sur une ligne
retractee ; les trois `test_passage_*` parce que le `main.tex` produit porte
alors, dans son resume, `{{R:temoin-ok}}` litteral au lieu de 42.0. C'est le
defaut G1 reproduit en miniature.

Ces tests n'ecrivent que dans un repertoire temporaire.
"""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]
MD2LATEX = Path(os.environ.get("MD2LATEX",
                               RACINE / "article" / "latex" / "md2latex.py"))

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_md2latex_annexe import (  # noqa: E402
    MAIN_TEX_SQUELETTE, PNG_1x1, installe_machine_registre)

# Le registre jetable porte `temoin-ok` (courant, valeur 42.0) et
# `temoin-retracte` (statut retracte, valeur 13.0) — voir
# test_md2latex_annexe.REGISTRE_MINIMAL.
VALEUR_RENDUE = "42.0"
VALEUR_RETRACTEE = "13.0"

MANUSCRIT = """# Titre complet: sous-titre

## Abstract

Resume de controle, taux mesure {renvoi} pour cent.

## 1. Introduction

Corps de controle.

> **Figure 1 -- Legende de controle.** Data: aucune.

## 8. Ethics Considerations

Section obligatoire.

## 9. Availability

Section obligatoire.

## 10. AI Use

Section obligatoire.

## References

[1] Rien.
"""


def prepare(tmp: Path, renvoi: str, main_tex: str = MAIN_TEX_SQUELETTE) -> Path:
    """Arborescence jetable complete ; renvoie le chemin du convertisseur."""
    installe_machine_registre(tmp)
    art = tmp / "article"
    (art / "latex").mkdir(parents=True)
    (art / "figures").mkdir()
    (art / "figures" / "fig1-monde-ouvert.png").write_bytes(PNG_1x1)
    (art / "references.bib").write_text("@misc{rien, title={Rien}}\n",
                                        encoding="utf-8")
    (art / "manuscrit.md").write_text(MANUSCRIT.format(renvoi=renvoi),
                                      encoding="utf-8")
    (art / "latex" / "main.tex").write_text(main_tex, encoding="utf-8")
    cible = art / "latex" / "md2latex.py"
    shutil.copyfile(MD2LATEX, cible)
    return cible


def lance(cible: Path) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(cible)],
                          capture_output=True, text=True,
                          cwd=str(cible.parent))


class TestChaineDeRendu(unittest.TestCase):

    # ------------------------------------------------------------------ #
    # Les cas fautifs : la chaine refuse, et main.tex ne bouge pas.       #
    # ------------------------------------------------------------------ #

    def _echoue_et_laisse_main_tex_intact(self, tmp: Path, renvoi: str,
                                          attendu: str,
                                          main_tex: str = MAIN_TEX_SQUELETTE):
        cible = prepare(tmp, renvoi, main_tex)
        avant = (cible.parent / "main.tex").read_bytes()
        res = lance(cible)
        trace = res.stdout + res.stderr
        self.assertNotEqual(
            res.returncode, 0,
            "la chaine devait REFUSER de convertir ; elle a rendu 0.\n" + trace)
        self.assertIn(attendu, trace,
                      "le message d'echec doit nommer la cause.\n" + trace)
        self.assertEqual(
            avant, (cible.parent / "main.tex").read_bytes(),
            "main.tex a ete modifie alors que la chaine a echoue : un echec "
            "doit laisser le .tex precedent intact, jamais un .tex ampute.")

    def test_echec_id_absent(self):
        """Un id qui n'existe pas au registre arrete la conversion."""
        with tempfile.TemporaryDirectory() as t:
            self._echoue_et_laisse_main_tex_intact(
                Path(t), "{{R:id-qui-nexiste-pas}}", "ABSENT du ")

    def test_echec_ligne_retractee(self):
        """Le cas dangereux : citer une ligne `statut: retracte`.

        Une substitution silencieuse publierait ici 13.0, un chiffre retracte
        qui a l'air juste. La chaine doit s'arreter."""
        with tempfile.TemporaryDirectory() as t:
            cible = prepare(Path(t), "{{R:temoin-retracte}}")
            avant = (cible.parent / "main.tex").read_bytes()
            res = lance(cible)
            trace = res.stdout + res.stderr
            self.assertNotEqual(res.returncode, 0, trace)
            self.assertIn("RETRACTEE", trace)
            self.assertEqual(avant, (cible.parent / "main.tex").read_bytes())
            self.assertNotIn(
                VALEUR_RETRACTEE,
                (cible.parent / "main.tex").read_text(encoding="utf-8"),
                "la valeur retractee ne doit JAMAIS atteindre main.tex")

    def test_echec_registre_absent(self):
        """Sans registre, on n'ecrit pas un main.tex aux chiffres non gouvernes."""
        with tempfile.TemporaryDirectory() as t:
            cible = prepare(Path(t), "{{R:temoin-ok}}")
            (Path(t) / "resultats" / "registre-chiffres.csv").unlink()
            avant = (cible.parent / "main.tex").read_bytes()
            res = lance(cible)
            self.assertNotEqual(res.returncode, 0, res.stdout + res.stderr)
            self.assertIn("registre absent", res.stdout + res.stderr)
            self.assertEqual(avant, (cible.parent / "main.tex").read_bytes())

    def test_echec_renvoi_hors_zone_generee(self):
        """Garde-fou de SORTIE : un `{{R:...}}` pose a la main dans main.tex,
        hors des zones GENERATED, n'est pas visible du rendu du manuscrit.
        C'est exactement par la que le defaut G1 pouvait revenir."""
        pollue = MAIN_TEX_SQUELETTE.replace(
            "\\maketitle",
            "\\maketitle\n\\textbf{Taux : {{R:temoin-ok}} \\%}")
        with tempfile.TemporaryDirectory() as t:
            self._echoue_et_laisse_main_tex_intact(
                Path(t), "{{R:temoin-ok}}", "subsistent dans le main.tex",
                main_tex=pollue)

    # ------------------------------------------------------------------ #
    # Le cas correct : la chaine rend, et rien ne reste a rendre.         #
    # ------------------------------------------------------------------ #

    def test_passage_valeur_substituee_dans_la_zone_generee(self):
        with tempfile.TemporaryDirectory() as t:
            cible = prepare(Path(t), "{{R:temoin-ok}}")
            res = lance(cible)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            tex = (cible.parent / "main.tex").read_text(encoding="utf-8")
            self.assertIn(VALEUR_RENDUE, tex,
                          "la valeur du registre doit apparaitre dans main.tex")

    def test_passage_aucun_marqueur_ne_subsiste(self):
        with tempfile.TemporaryDirectory() as t:
            cible = prepare(Path(t), "{{R:temoin-ok}}")
            res = lance(cible)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            tex = (cible.parent / "main.tex").read_text(encoding="utf-8")
            self.assertNotIn("{{R:", tex)

    def test_passage_le_composite_ic_est_rendu(self):
        """`{{R:id.ic}}` rend « [ic_bas ; ic_haut] » — la forme que le manuscrit
        emploie le plus, et celle dont l'absence se verrait le moins."""
        with tempfile.TemporaryDirectory() as t:
            cible = prepare(Path(t), "{{R:temoin-ok}} {{R:temoin-ok.ic}}")
            res = lance(cible)
            self.assertEqual(res.returncode, 0, res.stdout + res.stderr)
            tex = (cible.parent / "main.tex").read_text(encoding="utf-8")
            self.assertIn("41.0", tex)
            self.assertIn("43.0", tex)


if __name__ == "__main__":
    unittest.main()
