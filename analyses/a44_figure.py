"""
a44_figure : la distance au generateur nul, par condition, sur deux quantites.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par a44_mesures.py, pour que la figure et les chiffres du rapport ne
puissent pas diverger. Aucun script existant n'est modifie. La palette et les conventions
de trace sont celles de a28_figures, importees telles quelles.

Deux panneaux, la meme liste de conditions dans le meme ordre sur les deux.

  Panneau gauche  Q1b, le ratio inter sur l'axe ideologie, celui qui porte le 8,16 de C2
                  et le 8,5 de v8. Deux points par condition relies par un trait : la
                  valeur mesuree, et la valeur du generateur nul construit sur les seules
                  marginales de cette meme condition. Un trait court veut dire que le nul
                  reproduit le chiffre, donc que le chiffre ne porte aucune structure
                  individuelle.

  Panneau droit   Q5, la correlation moyenne entre items apres retrait du segment. Meme
                  convention. C'est la quantite primaire du verdict : le nul ne peut pas
                  la produire, son esperance y est le plancher de bruit d'echantillonnage.

Entree  : resultats/a44-quantites.csv
Sortie  : resultats/a44-figure-generateur-nul.png et .svg

Usage : .venv/bin/python analyses/a44_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import ENCRE, ENCRE_SECONDE, FOND, GRILLE, HUMAIN, LANGAGE, NEUTRE, \
    STATISTIQUE, style
import a44_commun as C

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

# Les onze conditions du perimetre 1 052, puis les quatre du perimetre 150. Les deux
# blocs ne se comparent pas : le plancher de bruit de chaque quantite depend de
# l'effectif. Un trait horizontal les separe sur la figure.
ORDRE_1052 = ["humains vague 1", "humains vague 2", "agents composite",
              "agents entretien (v3)", "agents enquete", "agents v7",
              "agents demographiques (v6)", "agents v8",
              "B1 argmax", "B2 argmax", "PMM k=10"]
ORDRE_150 = ["humains vague 1 (150)", "humains vague 2 (150)", "C3", "C2"]
ORDRE = ORDRE_1052 + ORDRE_150

HUMAINS = {"humains vague 1", "humains vague 2",
           "humains vague 1 (150)", "humains vague 2 (150)"}
LLM = {"agents composite", "agents entretien (v3)", "agents enquete", "agents v7",
       "agents demographiques (v6)", "agents v8", "C2", "C3"}


def teinte(cond):
    if cond in HUMAINS:
        return HUMAIN
    if cond in LLM:
        return LANGAGE
    return STATISTIQUE


def panneau(ax, d, quantite, titre, sous_titre, log=False):
    y = np.arange(len(ORDRE))[::-1]
    for i, cond in zip(y, ORDRE):
        s = d[(d.condition == cond) & (d.quantite == quantite)]
        if s.empty:
            continue
        r, n = float(s.reel.iloc[0]), float(s.nul_moyenne.iloc[0])
        bas, haut = float(s.nul_bas.iloc[0]), float(s.nul_haut.iloc[0])
        col = teinte(cond)
        if np.isfinite(r) and np.isfinite(n):
            ax.plot([n, r], [i, i], color=col, linewidth=1.6, alpha=0.45, zorder=2,
                    solid_capstyle="round")
        if np.isfinite(bas) and np.isfinite(haut):
            ax.plot([bas, haut], [i, i], color=NEUTRE, linewidth=4.0, alpha=0.30,
                    zorder=1, solid_capstyle="round")
        ax.scatter([n], [i], s=42, facecolor="white", edgecolor=NEUTRE, linewidth=1.4,
                   zorder=3)
        ax.scatter([r], [i], s=46, color=col, zorder=4)
    ax.axhline(len(ORDRE_150) - 0.5, color=GRILLE, linewidth=1.2, zorder=0)
    ax.set_yticks(y)
    ax.set_yticklabels([C.ETIQUETTE[c] for c in ORDRE], fontsize=9, color=ENCRE)
    ax.set_ylim(-0.8, len(ORDRE) - 0.2)
    if log:
        ax.set_xscale("log")
    style(ax)
    ax.set_title(titre, fontsize=11, color=ENCRE, loc="left", pad=12)
    ax.set_xlabel(sous_titre, fontsize=8.5, color=ENCRE_SECONDE)


def main():
    d = pd.read_csv(os.path.join(SORTIE, "a44-quantites.csv"))
    d = d[d.segmentation == "S_ideo"]

    fig, axes = plt.subplots(1, 2, figsize=(12.6, 6.4))
    fig.patch.set_facecolor(FOND)

    panneau(axes[0], d, "Q1b ratio inter, axe ideologie",
            "A. L'ecart entre camps politiques",
            "ratio inter, humains vague 1 = 1 ; echelle logarithmique", log=True)
    axes[0].axvline(1.0, color=GRILLE, linewidth=1.0, zorder=0)

    panneau(axes[1], d, "Q5 correlation residualisee",
            "B. La structure entre items a l'interieur du segment",
            "moyenne des |rho| apres retrait du segment")

    for ax in axes:
        ax.tick_params(axis="y", length=0)

    poignees = [
        plt.Line2D([], [], marker="o", linestyle="", color=ENCRE_SECONDE,
                   markersize=7, label="population mesuree"),
        plt.Line2D([], [], marker="o", linestyle="", markerfacecolor="white",
                   markeredgecolor=NEUTRE, markeredgewidth=1.4, color="none",
                   markersize=7, label="son generateur nul, moyenne de 200 replicats"),
        plt.Line2D([], [], linestyle="-", color=NEUTRE, linewidth=4, alpha=0.30,
                   label="bande du nul, 2,5 a 97,5 pour cent"),
    ]
    fig.legend(handles=poignees, loc="lower center", ncol=3, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, 0.125))
    fig.suptitle("a44. Distance au generateur nul conditionnellement independant de Yuan, "
                 "par condition\n"
                 "memes marginales par item et par segment ideologique, reponses tirees "
                 "independamment, aucune structure individuelle",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left", y=0.985)
    fig.text(0.012, 0.078,
             "Vert : humains. Rouge : conditions a modele de langage. Bleu : predicteurs "
             "statistiques. Un trait court veut dire que le generateur nul reproduit la "
             "quantite mesuree.\nSous le trait horizontal : les quatre populations "
             "mesurees sur les 150 personnes du run local ; au dessus, les onze mesurees "
             "sur les 1 052. Les deux blocs ne se comparent pas,\nle plancher de bruit de "
             "chaque quantite depend de l'effectif. Panneau B : le nul ne peut pas "
             "produire de correlation entre items, sa valeur est ce plancher.",
             fontsize=8, color=ENCRE_SECONDE, ha="left", va="top")
    fig.subplots_adjust(left=0.13, right=0.985, top=0.86, bottom=0.265, wspace=0.30)

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a44-figure-generateur-nul.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND)
        print(f"ecrit {chemin}", flush=True)


if __name__ == "__main__":
    main()
