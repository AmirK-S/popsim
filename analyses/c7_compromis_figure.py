"""
c7_compromis_figure : fidelite (abscisse) contre fuite de reidentification (ordonnee).

Ne recalcule rien. Lit resultats/c7-compromis.csv, ecrit par analyses/c7_compromis.py.
Palette et conventions de trace de a28_figures, importees telles quelles. Aucun script
existant modifie, aucun appel de modele.

Forme des points : rond pour un jumeau a modele de langage (les 8 configurations
admissibles), losange pour un predicteur statistique (B0, B1, B2, PMM). Couleur : rouge
LANGAGE pour les jumeaux, bleu STATISTIQUE pour les predicteurs, vert HUMAIN pour
Demographics Only (groupe a part, ni jumeau riche ni predicteur).

Sortie : resultats/c7-compromis.png (et .svg)
Usage  : .venv/bin/python analyses/c7_compromis_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import pandas as pd                      # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import ENCRE, ENCRE_SECONDE, FOND, GRILLE, LANGAGE, STATISTIQUE, style  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

DEMO = "Demographics Only - GPT4.1-mini"
COULEUR_DEMO = "#c8a02b"


def couleur_forme(groupe, nom):
    if nom == DEMO:
        return COULEUR_DEMO, "^"
    if groupe == "statistique":
        return STATISTIQUE, "D"
    return LANGAGE, "o"


def main():
    df = pd.read_csv(os.path.join(SORTIE, "c7-compromis.csv"))
    rho = df["rho_spearman_fidelite_fuite"].iloc[0]
    bas = df["rho_ic_bas"].iloc[0]
    haut = df["rho_ic_haut"].iloc[0]

    fig, ax = plt.subplots(figsize=(7.6, 6.4))
    fig.patch.set_facecolor(FOND)
    style(ax)

    for _, r in df.iterrows():
        col, marq = couleur_forme(r["groupe"], r["configuration"])
        ax.scatter([r["fidelite_plancher"]], [r["fuite_top1"]], s=90, color=col,
                   marker=marq, edgecolor="white", linewidth=0.6, zorder=3)

    ax.set_xlabel("fidelite individuelle (part du plancher humain, chute sous "
                  "permutation intra-segment, S_gra)", fontsize=9.5, color=ENCRE_SECONDE)
    ax.set_ylabel("fuite de reidentification (top-1, cible vague 4)", fontsize=9.5,
                  color=ENCRE_SECONDE)
    ax.set_title(f"Fidelite et fuite sur Twin-2K-500, 12 configurations\n"
                 f"Spearman = {rho:.2f}  IC 95% [{bas:.2f} ; {haut:.2f}]",
                 fontsize=11.5, color=ENCRE, loc="left", pad=12)

    ax.plot([], [], "o", color=LANGAGE, label="jumeau LLM (8)")
    ax.plot([], [], "D", color=STATISTIQUE, label="predicteur statistique (4)")
    ax.plot([], [], "^", color=COULEUR_DEMO, label="Demographics Only")
    ax.legend(loc="upper left", fontsize=8.5, frameon=False, labelcolor=ENCRE_SECONDE)

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"c7-compromis.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
