"""
c7_a9_ic : l'intervalle de confiance de A9 (et de ses jumeaux dans le depot) est faux.

===========================================================================
CONSTAT (relecture hostile du 12/09, F2 dans `resultats/revue-hostile-finale-2026-09-12.md`) :
la reidentification n=30, x=0 succes de `c7-fort-resultats.md` (A9, ligne 605 et 815 du
manuscrit) est rapportee avec un intervalle de confiance a 95 % **[0 ; 0]**. Un intervalle
de largeur nulle sur 0 succes est structurellement impossible : il ne peut exister aucune
observation, meme extreme, qui exclue un taux reel de, disons, 3 % avec un denominateur de
30. L'intervalle publie n'est pas un intervalle de confiance, c'est un artefact du
bootstrap percentile de `a2_commun.bootstrap_personnes` (reechantillonner 30 zeros avec
remise ne produit jamais que des zeros -- verifie ligne 110-123 de ce fichier) applique a
une proportion rare. La regle de trois donne une borne haute a 95 % d'environ 9,5 % pour
n=30 -- au-dessus du seuil preenregistre de 5 % : la prediction "top-1 > 5 %" n'est donc
PAS refutee, elle est non concluante (puissance insuffisante).

CE QUE FAIT CE SCRIPT : calcule, pour (0 succes, n) donne, les trois intervalles a 95 %
qui font consensus pour une proportion binomiale -- Clopper-Pearson exact (methode de
reference, jamais anticonservatrice), Wilson (bonne couverture, plus etroit), regle de
trois (approximation mnemotechnique de Clopper-Pearson pour x=0) -- et les applique a
CHAQUE occurrence de "0 succes / n, IC [0 ; 0]" trouvee dans le depot, pas seulement A9 :
c7-fort (A9, n=30), c7-synth-ajuste (A2, n=2058), c7-recette (n=40 et n=10, prediction 9
du tableau 3), c7-gen (quatre cellules a n=200), c7-dp (eps=10, n=2058). Le meme bug de
bootstrap explique les six.

Aucun appel de modele. Aucune dependance a un autre script c7_*.py. Lecture seule des CSV
deja publies dans resultats/ (pour retrouver n et x) ; ecrit uniquement sur stdout.
Usage : .venv/bin/python analyses/c7_a9_ic.py
===========================================================================
"""

import math

from scipy import stats

Z95 = 1.959963984540054  # quantile normal a 97,5 %


def clopper_pearson(x, n, alpha=0.05):
    """Intervalle exact de Clopper-Pearson a 95 % pour x succes sur n essais."""
    if x == 0:
        bas = 0.0
    else:
        bas = stats.beta.ppf(alpha / 2, x, n - x + 1)
    if x == n:
        haut = 1.0
    else:
        haut = stats.beta.ppf(1 - alpha / 2, x + 1, n - x)
    return bas, haut


def wilson(x, n, z=Z95):
    """Intervalle de Wilson (score) a 95 % pour x succes sur n essais."""
    p = x / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    marge = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, centre - marge), min(1.0, centre + marge)


def regle_de_trois(n):
    """Approximation mnemotechnique de la borne haute de Clopper-Pearson pour x=0."""
    return 3.0 / n


def rapporte(nom, x, n, seuil=None):
    cp_bas, cp_haut = clopper_pearson(x, n)
    wi_bas, wi_haut = wilson(x, n)
    r3 = regle_de_trois(n) if x == 0 else float("nan")
    print(f"\n{nom} : x={x}, n={n}, observe = {100 * x / n:.4f} %")
    print(f"  bootstrap percentile publie : [0 ; 0]  <-- artefact, x resamples de x=0 "
          f"ne peuvent produire que 0")
    print(f"  Clopper-Pearson exact 95 %  : [{100*cp_bas:.4f} ; {100*cp_haut:.4f}] %")
    print(f"  Wilson (score) 95 %        : [{100*wi_bas:.4f} ; {100*wi_haut:.4f}] %")
    if x == 0:
        print(f"  regle de trois (3/n)       : borne haute ~= {100*r3:.4f} %")
    if seuil is not None:
        contient = cp_haut >= seuil
        verdict = ("NON refutee (seuil dans l'IC, non concluant)" if contient
                   else "refutee (seuil hors de l'IC)")
        print(f"  seuil preenregistre {100*seuil:.2f} % : {verdict}")
    return cp_bas, cp_haut, wi_bas, wi_haut, r3


def main():
    print(__doc__.split("=" * 75)[1])

    print("=" * 75)
    print("1. A9 -- c7-fort-resultats.md : test payant, modele fort, appel par item")
    print("=" * 75)
    rapporte("A9 top-1 (30 personnes x 60 items, GPT-4.1, c7-fort-reidentification.csv)",
              x=0, n=30, seuil=0.05)
    rapporte("A9 top-10 (meme bras)", x=0, n=30)

    print("\n" + "=" * 75)
    print("2. Meme defaut ailleurs dans le depot (meme bug de bootstrap percentile)")
    print("=" * 75)

    rapporte("A2 -- c7-synth-ajuste-resultats.md : donneur ajuste sur bloc cible, top-1 "
             "(2058 personnes)", x=0, n=2058)
    print("  --> conclusion de A2 inchangee : borne haute << 20,7 % du jumeau. Defaut de "
          "notation, pas de fond.")

    rapporte("Table 3, ligne 9 -- c7-recette-resultats.md : appel unique (60 items/pers.)",
             x=0, n=40)
    rapporte("Table 3, ligne 9 -- c7-recette-resultats.md : appel par item", x=0, n=10)
    print("  --> a n=10, la borne haute de Clopper-Pearson depasse 25 % : le verdict "
          "\"refutee\" sur la prediction \"item >= 5x unique\" n'est pas etabli non plus, "
          "le facteur reste incalculable dans les deux sens.")

    for nom, n in [("llama31-8b/R1/t0", 200), ("llama31-8b/R2/t0", 200),
                   ("qwen37-flash/R2/t0", 200), ("qwen37-flash/R1/t1", 200)]:
        rapporte(f"c7-gen-resultats.md : {nom}, top-1", x=0, n=n)
    print("  --> n=200 ici (pas 30) : la borne haute exacte reste sous 1,83 %, donc la "
          "conclusion de A9-partie-1 (aucun de nos jumeaux bon marche n'egale Twin) "
          "resiste ; seule la notation [0 ; 0] est fausse.")

    rapporte("Table 3, ligne 14 -- c7-dp-resultats.md : DP epsilon=10, top-1 (2058 "
             "personnes)", x=0, n=2058)
    print("  --> sans consequence sur le verdict (la refutation tient sur la perte "
          "d'utilite, pas sur ce top-1) ; meme defaut de notation.")


if __name__ == "__main__":
    main()
