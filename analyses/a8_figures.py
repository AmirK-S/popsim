"""
a8_figures : la figure des familles, exactitude par famille et par methode.

Statut : script d'exploration. Il ne recalcule rien, il lit les CSV deja ecrits pour que
la figure et les tableaux du rapport ne puissent pas diverger.

Entree  : resultats/a8-familles-gss.csv, resultats/a8-familles-twin.csv.
Sortie  : resultats/a8-figure-familles.png et .svg.
          Axes, titres et legendes en francais.

Aucun appel de modele. Duree : quelques secondes.

Usage : .venv/bin/python analyses/a8_figures.py
"""

import os
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

FOND = "#fcfcfb"
ENCRE = "#0b0b0b"
ENCRE_SECONDE = "#52514e"
GRILLE = "#e2e1dd"

# Une teinte par methode, stable d'un panneau a l'autre. Les baselines sans modele de
# langage sont dans les bleus et les verts, les agents de langage dans les orange et les
# violets, le plancher en gris. La lecture ne depend pas de la distinction fine des
# teintes : l'ordre des barres est le meme dans chaque groupe et il est rappele en legende.
METHODES_GSS = [
    ("B0 mode", "#9a9791"),
    ("B1 argmax", "#2a78d6"),
    ("B2 blocs aleatoires (a2)", "#7fd0b0"),
    ("B2 famille retiree (argmax)", "#1baf7a"),
    ("agents enquete", "#eb6834"),
    ("agents composite", "#a83a12"),
    ("humains reinterroges", "#4a3aa7"),
]
METHODES_TWIN = [
    ("B0 mode", "#9a9791"),
    ("B1 argmax", "#2a78d6"),
    ("B2 contexte complet (a2)", "#1baf7a"),
    ("GPT-4.1-mini, persona texte", "#eb6834"),
    ("GPT-4.1, persona JSON", "#a83a12"),
    ("humains retest vagues 1 a 3", "#4a3aa7"),
]


def style(ax):
    ax.set_facecolor(FOND)
    ax.grid(True, axis="y", color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=9)


def panneau(ax, table, familles, methodes, titre):
    largeur = 0.8 / len(methodes)
    positions = np.arange(len(familles))
    for i, (nom, couleur) in enumerate(methodes):
        vals, bas, haut = [], [], []
        for f in familles:
            s = table[(table["famille"] == f) & (table["methode"] == nom)]
            vals.append(float(s["exactitude"].iloc[0]) if len(s) else np.nan)
            bas.append(float(s["ic_bas"].iloc[0]) if len(s) else np.nan)
            haut.append(float(s["ic_haut"].iloc[0]) if len(s) else np.nan)
        vals = np.array(vals)
        err = np.vstack([vals - np.array(bas), np.array(haut) - vals])
        ax.bar(positions + i * largeur, vals, largeur * 0.92, color=couleur, zorder=3,
               label=nom, yerr=err, error_kw={"elinewidth": 0.7, "ecolor": ENCRE_SECONDE,
                                              "capsize": 0})
    ax.set_xticks(positions + 0.4 - largeur / 2)
    ax.set_xticklabels(["\n".join(textwrap.wrap(f, 18)) for f in familles], fontsize=8.5,
                       color=ENCRE_SECONDE)
    ax.set_ylabel("exactitude exacte", color=ENCRE_SECONDE, fontsize=9)
    ax.set_title("\n".join(textwrap.wrap(titre, 95)), color=ENCRE, fontsize=11,
                 loc="left", pad=34)
    style(ax)
    ax.legend(fontsize=8, frameon=False, ncol=4, labelcolor=ENCRE_SECONDE,
              loc="lower left", bbox_to_anchor=(0, 1.0, 1, 0.10), mode="expand",
              borderaxespad=0)


def main():
    gss = pd.read_csv(os.path.join(SORTIE, "a8-familles-gss.csv"))
    twin = pd.read_csv(os.path.join(SORTIE, "a8-familles-twin.csv"))
    familles_gss = [f for f in gss["famille"].unique()]
    familles_twin = [f for f in twin["famille"].unique()]

    fig, axes = plt.subplots(2, 1, figsize=(13, 8.2))
    fig.patch.set_facecolor(FOND)
    panneau(axes[0], gss, familles_gss, METHODES_GSS,
            "GSS : la famille entiere est retiree du contexte et predite. "
            "Les barres vert clair sont le decoupage aleatoire de a2, les vert fonce le "
            "decoupage par famille.")
    panneau(axes[1], twin, familles_twin, METHODES_TWIN,
            "Twin-2K-500 : par bloc de la vague 4. Le contexte des vagues 1 a 3 ne "
            "contient deja aucun item de ces blocs.")
    # L'axe part de zero : ce sont des barres, un axe tronque exagererait les ecarts.
    axes[0].set_ylim(0, 1.0)
    axes[1].set_ylim(0, 1.0)
    fig.tight_layout(h_pad=3.5)
    for extension in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a8-figure-familles.{extension}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
