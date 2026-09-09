"""
r3b_figure : les quatre quantites de R3, avant et apres l'ajout de l'etiquette.

Statut : script de figure, aucun appel de modele, aucun recalcul. Il lit les tableaux
ecrits par r3_evaluer.py et r3b_appariement.py, pour que la figure et les chiffres du
rapport ne puissent pas diverger. Aucun script existant n'est modifie. Palette et
conventions de trace importees telles quelles de a28_figures.

Quatre panneaux, les memes quatre conditions sur chacun, dans le meme ordre :
C3 -> C3E (regime riche, on AJOUTE les onze attributs) puis C2S -> C2 (regime pauvre, on
AJOUTE l'ideologie et le parti). Une fleche relie chaque paire dans le sens de l'ajout.
Le trait vert est le plancher humain, calcule sur les MEMES personnes et les MEMES
58 items que la paire au dessus de laquelle il court : il y en a donc deux par panneau,
un par perimetre (94 personnes pour H1, 130 pour H2).

  Panneau 1  la chute d'exactitude sous permutation intra segment, en part du plancher
             humain, sous les DEUX segmentations exigees par a45. C'est la seule quantite
             de personne des quatre.
  Panneau 2  le ratio inter sur l'axe ideologie, rapporte aux humains de la vague 1.
             Quantite de gabarit (a44 section 3), donc plancher a 1 et non a 0.
  Panneau 3  le rapport de rarete groupe sur personne de a31 section 2.3, sur le
             perimetre d'items APPARIE de r3b. Quantite de gabarit chez les conditions
             dont le lift de personne est au niveau du nul (a44 section 6).
  Panneau 4  le rappel des raretes stables sur les 58 items, perimetre apparie. Le
             plancher humain y vaut 1,000 PAR CONSTRUCTION, la stabilite etant definie
             par la vague 2 : le trait est trace en pointille pour le dire.

Entree  : resultats/r3-tableau.csv, r3b-plancher-humain.csv, r3b-rarete-appariee.csv
Sortie  : resultats/r3b-figure-ablation-etiquette.png et .svg

Usage : .venv/bin/python analyses/r3b_figure.py
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
    style

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

# (condition, contraste d'ou vient sa ligne). L'ordre est celui de l'ajout : sans
# etiquette a gauche de sa paire, avec etiquette a droite.
ORDRE = [("C3", "H1"), ("C3E", "H1"), ("C2S", "H2"), ("C2", "H2")]
AVEC = {"C3E", "C2"}
ETIQ = {"C3": "C3\n119 reponses", "C3E": "C3E\n119 reponses\n+ 11 attributs",
        "C2S": "C2S\n9 attributs", "C2": "C2\n9 attributs\n+ ideologie, parti"}


def charger():
    plancher = pd.read_csv(os.path.join(SORTIE, "r3b-plancher-humain.csv"))
    rarete = pd.read_csv(os.path.join(SORTIE, "r3b-rarete-appariee.csv"))
    return plancher, rarete


def valeur(df, contraste, condition, colonne):
    sel = df[(df["contraste"] == contraste) & (df["condition"] == condition)]
    if not len(sel):
        return np.nan
    return float(sel.iloc[0][colonne])


def barres(ax, valeurs, plancher, titre, sous_titre, plancher_pointille=False,
           second=None, legende_second=None):
    """Un panneau : quatre barres, deux fleches d'ajout, un plancher humain par paire."""
    x = np.arange(4)
    couleurs = [LANGAGE if c in AVEC else NEUTRE for c, _ in ORDRE]
    ax.bar(x, valeurs, width=0.58, color=couleurs, edgecolor=ENCRE, linewidth=0.7,
           zorder=3)
    # Les losanges sont decales a droite du centre de la barre pour ne pas recouvrir son
    # etiquette de valeur : deux quantites sur un meme panneau, jamais superposees.
    if second is not None:
        ax.plot(x + 0.23, second, marker="D", markersize=5.5, linestyle="none",
                color=ENCRE, markerfacecolor="white", markeredgewidth=1.1, zorder=5,
                label=legende_second)
        ax.legend(loc="upper left", frameon=False, fontsize=8,
                  labelcolor=ENCRE_SECONDE)

    hauteur = max([v for v in list(valeurs) + list(plancher) if np.isfinite(v)] or [1.0])

    # Le plancher humain, un segment par perimetre : il n'est pas le meme sur 94 et sur
    # 130 personnes, et le confondre serait une faute de denominateur.
    style_trait = (0, (3, 2)) if plancher_pointille else "-"
    for i, (deb, fin) in enumerate(((-0.42, 1.42), (1.58, 3.42))):
        ax.plot([deb, fin], [plancher[i], plancher[i]], color=HUMAIN, linewidth=1.9,
                linestyle=style_trait, zorder=4)
    ax.text(1.50, max(plancher) + 0.018 * hauteur, "plancher humain", ha="center",
            va="bottom", fontsize=7.5, color=HUMAIN)

    for i, v in enumerate(valeurs):
        if np.isfinite(v):
            decal = -0.16 if second is not None else 0.0
            ax.text(i + decal, v + 0.035 * hauteur, f"{v:.3f}".replace(".", ","),
                    ha="center", va="bottom", fontsize=8.5, color=ENCRE)
        else:
            ax.text(i, 0.02 * hauteur, "non defini", ha="center", va="bottom",
                    fontsize=8, color=ENCRE_SECONDE, rotation=90)

    for deb, fin in ((0, 1), (2, 3)):
        y = hauteur * 1.16
        ax.annotate("", xy=(fin - 0.12, y), xytext=(deb + 0.12, y),
                    arrowprops=dict(arrowstyle="-|>", color=ENCRE_SECONDE,
                                    linewidth=1.0, shrinkA=0, shrinkB=0))
        ax.text((deb + fin) / 2, y * 1.015, "on ajoute l'etiquette", ha="center",
                va="bottom", fontsize=7.5, color=ENCRE_SECONDE)

    ax.set_xticks(x)
    ax.set_xticklabels([ETIQ[c] for c, _ in ORDRE], fontsize=8, color=ENCRE)
    ax.set_title(titre, fontsize=11, color=ENCRE, loc="left", pad=16)
    ax.text(0, 1.005, sous_titre, transform=ax.transAxes, fontsize=8,
            color=ENCRE_SECONDE, va="bottom")
    ax.set_ylim(0, hauteur * 1.30)
    style(ax, axe_grille="y")


def main():
    plancher, rarete = charger()

    # ---------------------------------------------------------------- panneau 1
    part_ideo = [valeur(plancher, ct, c, "part du plancher humain S_ideo")
                 for c, ct in ORDRE]
    part_gra = [valeur(plancher, ct, c, "part du plancher humain S_gra")
                for c, ct in ORDRE]
    plancher_1 = [1.0, 1.0]

    # ---------------------------------------------------------------- panneau 2
    inter = [valeur(plancher, ct, c, "ratio inter (S_ideo)") for c, ct in ORDRE]
    plancher_2 = [1.0, 1.0]

    # ---------------------------------------------------------------- panneau 3
    gsp = [valeur(rarete, ct, c, "groupe sur personne") for c, ct in ORDRE]
    plancher_3 = [valeur(rarete, "H1", "humains vague 2", "groupe sur personne"),
                  valeur(rarete, "H2", "humains vague 2", "groupe sur personne")]

    # ---------------------------------------------------------------- panneau 4
    stable = [valeur(rarete, ct, c, "rappel (stable)") for c, ct in ORDRE]
    plancher_4 = [valeur(rarete, "H1", "humains vague 2", "rappel (stable)"),
                  valeur(rarete, "H2", "humains vague 2", "rappel (stable)")]

    fig, axes = plt.subplots(2, 2, figsize=(13.6, 10.4))
    fig.patch.set_facecolor(FOND)

    barres(axes[0][0], part_ideo, plancher_1,
           "1. Chute sous permutation, en part du plancher humain",
           "barres : segmentation par l'ideologie (S_ideo) ; losanges : genre x race x age "
           "(S_gra), sans ideologie",
           second=part_gra, legende_second="S_gra, sans ideologie")
    barres(axes[0][1], inter, plancher_2,
           "2. Ratio inter sur l'axe ideologie",
           "ecart entre segments rapporte aux humains de la vague 1 ; 1,000 = les humains. "
           "Quantite de gabarit (a44, 3)")
    barres(axes[1][0], gsp, plancher_3,
           "3. Rarete de groupe sur rarete de personne (a31, 2.3)",
           "perimetre d'items apparie (r3b) ; C2S non defini, son lift de personne est "
           "negatif")
    barres(axes[1][1], stable, plancher_4,
           "4. Rappel des raretes stables, 58 items, perimetre apparie",
           "plancher humain a 1,000 PAR CONSTRUCTION, la stabilite etant definie par la "
           "vague 2 : trait pointille",
           plancher_pointille=True)

    fig.suptitle("R3, la vraie ablation de l'etiquette : ce que l'ajout d'une etiquette "
                 "change, a information de la personne constante",
                 fontsize=13.5, color=ENCRE, y=0.985)
    fig.text(0.5, 0.005,
             "Qwen3-4B-Instruct-2507 Q4_K_M, argmax, passe 1, 58 items de six familles du "
             "GSS. H1 : 94 personnes communes a C3E et C3. H2 : 130 personnes communes a "
             "C2 et C2S.\nLe plancher humain est la vague 2 sur les memes personnes et les "
             "memes items. Panneaux 3 et 4 : perimetre d'items apparie, voir "
             "resultats/r3b-rarete-appariee.csv.",
             ha="center", fontsize=8, color=ENCRE_SECONDE)
    fig.tight_layout(rect=(0, 0.035, 1, 0.955))

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"r3b-figure-ablation-etiquette.{ext}")
        fig.savefig(chemin, dpi=170, facecolor=FOND)
        print(f"ecrit {chemin}")


if __name__ == "__main__":
    main()
