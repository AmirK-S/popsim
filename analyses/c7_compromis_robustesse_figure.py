"""
c7_compromis_robustesse_figure : les 13 points (8 LLM, 4 statistiques, 1 retest humain),
echelle log en ordonnee pour montrer a la fois le palier bas (statistiques, quasi au
hasard) et l'absence de second palier en haut (le retest humain depasse largement le
meilleur jumeau, pas de saturation).

Ne recalcule rien. Lit resultats/c7-compromis-robustesse-points.csv, ecrit par
analyses/c7_compromis_robustesse.py. Palette de a28_figures, importee telle quelle.

Sortie : resultats/c7-compromis-robustesse.png (et .svg)
Usage  : .venv/bin/python analyses/c7_compromis_robustesse_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import pandas as pd                      # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import ENCRE, ENCRE_SECONDE, FOND, GRILLE, HUMAIN, LANGAGE, STATISTIQUE, style  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
DEMO = "Demographics Only - GPT4.1-mini"
COULEUR_DEMO = "#c8a02b"


def couleur_forme(groupe, nom):
    if nom == DEMO:
        return COULEUR_DEMO, "^"
    if groupe == "statistique":
        return STATISTIQUE, "D"
    if groupe == "humain":
        return HUMAIN, "*"
    return LANGAGE, "o"


def main():
    df = pd.read_csv(os.path.join(SORTIE, "c7-compromis-robustesse-points.csv"))
    hasard = float(df["hasard_top1"].iloc[0])

    fig, ax = plt.subplots(figsize=(7.8, 6.6))
    fig.patch.set_facecolor(FOND)
    style(ax)
    ax.set_yscale("log")

    for _, r in df.iterrows():
        col, marq = couleur_forme(r["groupe"], r["configuration"])
        taille = 170 if r["groupe"] == "humain" else 90
        y = max(r["fuite_top1"], hasard * 0.6)
        ax.scatter([r["fidelite_plancher"]], [y], s=taille, color=col, marker=marq,
                   edgecolor="white", linewidth=0.6, zorder=3)

    ax.axhline(hasard, color=GRILLE, linewidth=1.2, linestyle="--", zorder=1)
    ax.text(0.98, hasard, " hasard", ha="right", va="bottom", fontsize=8,
            color=ENCRE_SECONDE, transform=ax.get_yaxis_transform())

    ax.set_xlabel("fidelite individuelle (part du plancher humain, S_gra)", fontsize=9.5,
                  color=ENCRE_SECONDE)
    ax.set_ylabel("fuite de reidentification (top-1, echelle log)", fontsize=9.5,
                  color=ENCRE_SECONDE)
    ax.set_title("13 points : palier bas (statistiques, quasi au hasard),\n"
                 "puis hausse sans second palier jusqu'au retest humain",
                 fontsize=11.5, color=ENCRE, loc="left", pad=12)

    ax.plot([], [], "o", color=LANGAGE, label="jumeau LLM (7)")
    ax.plot([], [], "^", color=COULEUR_DEMO, label="Demographics Only")
    ax.plot([], [], "D", color=STATISTIQUE, label="predicteur statistique (4)")
    ax.plot([], [], "*", color=HUMAIN, markersize=11, label="retest humain (v1-3 -> v4)")
    ax.legend(loc="upper left", fontsize=8.5, frameon=False, labelcolor=ENCRE_SECONDE)

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"c7-compromis-robustesse.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
