"""
a42_figure : l'exces de rappel sur le plancher de bruit de cellule, raretes STABLES contre
raretes INSTABLES, par methode ; et le placebo qui dit ce que vaut un gradient de
deductibilite.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par `a42_plancher.py`, pour que la figure et les chiffres du rapport ne
puissent pas diverger. Aucun script existant n'est modifie. La palette et les conventions
de trace sont celles de a25_figure, a28_figures, a29_figure, a31_figure et a34_figure,
importees telles quelles.

Trois panneaux.

  1. Perimetre 1 052. Une ligne par methode, deux barres : l'exces de rappel sur le
     plancher de tirage dans la marginale du segment, sur les raretes que la personne a
     REDONNEES deux semaines plus tard, et sur celles qu'elle n'a pas redonnees. Le zero
     est le plancher : a gauche du zero, la methode fait moins bien qu'un tirage au sort
     dans le segment demographique de la personne. Barres d'erreur : intervalle a 95 pour
     cent, bootstrap sur les personnes.
  2. Meme chose sur le perimetre du run local, avec C2 et C3, l'ablation de l'etiquette.
  3. Le placebo. En abscisse le gradient de l'exces entre le tercile deductible et le
     tercile non deductible d'une partition ALEATOIRE, qui ne porte aucune information ;
     en ordonnee le meme gradient sur la partition par division de recensement. Les points
     sur la diagonale disent que le gradient de deductibilite est du bruit de petites
     cellules et rien d'autre.

Entree  : resultats/a42-stabilite.csv, a42-partitions-tierces.csv
Sortie  : resultats/a42-figure-plancher.png et .svg

Usage : .venv/bin/python analyses/a42_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import (ENCRE, ENCRE_SECONDE, FOND, GRILLE, HUMAIN, LANGAGE, NEUTRE,
                         STATISTIQUE, style)
import a42_commun as C

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

COURT = {"agents composite": "composite", "agents entretien (v3)": "entretien",
         "agents enquete": "enquete", "agents demographiques (v6)": "demo v6",
         "agents v7": "v7", "agents v8": "v8", "C2": "C2, avec etiquette",
         "C3": "C3, sans etiquette", "PMM k=5": "PMM k=5", "PMM k=10": "PMM k=10",
         "IM m=10 mode des m": "imputation multiple", "B1 argmax": "B1 regression",
         "B2 argmax": "B2 voisins", "B3 foret": "B3 foret aleatoire",
         "B0 tirage": "B0 tirage aveugle", "B0 mode": "B0 mode",
         "humains vague 2": "humains vague 2"}

# L'ordre des lignes est celui de l'exces sur les raretes stables, decroissant : c'est la
# quantite dont le panneau parle, et un classement par elle se lit sans chercher.
MONTREES = ["agents composite", "agents entretien (v3)", "agents enquete",
            "agents demographiques (v6)", "agents v7", "agents v8",
            "PMM k=5", "PMM k=10", "IM m=10 mode des m",
            "B2 argmax", "B1 argmax", "B3 foret", "B0 tirage"]


def couleur(cond):
    if cond == "humains vague 2":
        return HUMAIN
    return LANGAGE if cond in C.LLM else STATISTIQUE


def panneau_barres(ax, tab, perimetre, conditions, titre, sous_titre, xlim, pad,
                   note_plancher=True):
    s = tab[(tab.perimetre == perimetre) & (tab.seuil == 0.10)]
    lignes = []
    for cond in conditions:
        a = s[(s.condition == cond) & (s.classe == "rarete stable")]
        b = s[(s.condition == cond) & (s.classe == "rarete instable")]
        if a.empty or b.empty:
            continue
        lignes.append((cond, a.iloc[0], b.iloc[0]))
    lignes.sort(key=lambda e: e[1]["exces_segment"])

    h = 0.36
    for k, (cond, a, b) in enumerate(lignes):
        col = couleur(cond)
        for dy, row, plein in ((+0.21, a, True), (-0.21, b, False)):
            v = float(row["exces_segment"])
            ax.barh(k + dy, v, height=h, color=col if plein else FOND,
                    edgecolor=col, linewidth=0.0 if plein else 1.4,
                    alpha=1.0 if plein else 0.95, zorder=4)
            lo = float(row["exces_segment_ic_bas"])
            hi = float(row["exces_segment_ic_haut"])
            ax.plot([lo, hi], [k + dy, k + dy], color=ENCRE, linewidth=1.1, zorder=6,
                    solid_capstyle="butt")
            ax.plot([lo, lo, np.nan, hi, hi], [k + dy - 0.09, k + dy + 0.09, np.nan,
                                               k + dy - 0.09, k + dy + 0.09],
                    color=ENCRE, linewidth=1.1, zorder=6)

    ax.axvline(0.0, color=ENCRE, linewidth=1.6, zorder=5)
    if note_plancher:
        ax.annotate("zero = plancher : tirage dans la\nmarginale du segment de la personne",
                    (0.0, -0.60), textcoords="offset points", xytext=(7, 0),
                    fontsize=8, color=ENCRE, style="italic", va="center", zorder=7)

    style(ax, axe_grille="x")
    ax.set_yticks(range(len(lignes)))
    ax.set_yticklabels([COURT.get(c, c) for c in [l[0] for l in lignes]], fontsize=9)
    ax.set_ylim(-0.7, len(lignes) - 0.3)
    ax.set_xlim(*xlim)
    ax.set_xlabel("exces de rappel sur le plancher de bruit de cellule",
                  fontsize=9.5, color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=11.5, color=ENCRE, loc="left", pad=pad)
    ax.annotate(sous_titre, (0, 1.008), xycoords="axes fraction", fontsize=8.5,
                color=ENCRE_SECONDE, va="bottom")


def panneau_placebo(ax, tie):
    s = tie[(tie.perimetre == 1052) & (tie.seuil == 0.10)]
    pts = []
    for cond in MONTREES:
        v = {}
        for part, cle in (("P_B division de recensement", "pb"),
                          ("P_C partition aleatoire", "pc")):
            q = s[(s.partition == part) & (s.condition == cond)]
            if q.empty:
                continue
            t1 = q[q.tercile == "T1 non deductible"]["exces_segment"]
            t3 = q[q.tercile == "T3 deductible"]["exces_segment"]
            if len(t1) and len(t3):
                v[cle] = float(t3.iloc[0]) - float(t1.iloc[0])
        if len(v) == 2:
            pts.append((cond, v["pc"], v["pb"]))

    lim = (-0.23, 0.17)
    ax.plot(lim, lim, color=NEUTRE, linewidth=1.4, linestyle=(0, (4, 3)), zorder=2)
    ax.axhline(0, color=GRILLE, linewidth=1.0, zorder=1)
    ax.axvline(0, color=GRILLE, linewidth=1.0, zorder=1)
    decalage = {"agents entretien (v3)": (-10, 5), "PMM k=10": (-10, 8),
                "PMM k=5": (-10, -8), "IM m=10 mode des m": (-10, 8),
                "agents composite": (10, -2), "agents enquete": (-10, 4),
                "agents v8": (10, -9), "B1 argmax": (10, 2), "B2 argmax": (10, -9),
                "B0 tirage": (10, 4), "agents v7": (-10, -6),
                "B3 foret": (10, -9), "agents demographiques (v6)": (10, 2)}
    for cond, xpc, ypb in pts:
        col = couleur(cond)
        dx, dy = decalage.get(cond, (9, 2))
        ax.plot([xpc], [ypb], "o", markersize=8, color=col, markeredgecolor=FOND,
                markeredgewidth=1.6, zorder=6)
        ax.annotate(COURT.get(cond, cond), (xpc, ypb), textcoords="offset points",
                    xytext=(dx, dy), fontsize=7.6, color=ENCRE_SECONDE, zorder=7,
                    ha="right" if dx < 0 else "left")
    ax.annotate("la diagonale : le meme gradient mesure sur une\n"
                "partition aleatoire, donc sans aucune information",
                (lim[0] + 0.012, lim[1] - 0.012), fontsize=8, color=NEUTRE,
                style="italic", zorder=3, va="top")

    style(ax, axe_grille="both")
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)
    ax.set_xlabel("gradient sur la partition ALEATOIRE, T3 moins T1",
                  fontsize=9.5, color=ENCRE_SECONDE)
    ax.set_ylabel("gradient sur la division de recensement",
                  fontsize=9.5, color=ENCRE_SECONDE)
    ax.set_title("3. Le placebo : un gradient de deductibilite\n"
                 "que le hasard reproduit trait pour trait",
                 fontsize=11.5, color=ENCRE, loc="left", pad=16)


def main():
    tab = pd.read_csv(os.path.join(SORTIE, "a42-stabilite.csv"))
    tie = pd.read_csv(os.path.join(SORTIE, "a42-partitions-tierces.csv"))

    fig = plt.figure(figsize=(18.0, 9.4), facecolor=FOND)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.22, 1.0], height_ratios=[1.0, 0.92],
                          wspace=0.30, hspace=0.55)
    ax1 = fig.add_subplot(gs[:, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 1])
    for ax in (ax1, ax2, ax3):
        ax.set_facecolor(FOND)

    panneau_barres(
        ax1, tab, 1052, MONTREES,
        "1. Ce qui reste une fois le bruit de petites cellules paye,\n"
        "perimetre 1 052",
        "seuil 10 %, 3 130 raretes stables et 2 579 instables, "
        "intervalles a 95 % par bootstrap sur les personnes",
        (-0.135, 0.345), pad=34)

    panneau_barres(
        ax2, tab, 150, MONTREES + ["C2", "C3"],
        "2. L'ablation de l'etiquette, perimetre du run local",
        "seuil 10 %, 354 raretes stables et 393 instables sur 150 personnes",
        (-0.135, 0.345), pad=20, note_plancher=False)

    panneau_placebo(ax3, tie)

    # Legende de classe, unique et placee une fois : l'identite de la methode est portee
    # par la couleur, la classe de rarete par le remplissage.
    ax1.barh([], [], color=ENCRE, label="rarete STABLE : la personne a redonne la meme "
                                       "reponse deux semaines plus tard")
    ax1.barh([], [], color=FOND, edgecolor=ENCRE, linewidth=1.4,
             label="rarete INSTABLE : elle a donne autre chose")
    ax1.plot([], [], "s", color=LANGAGE, label="condition a modele de langage")
    ax1.plot([], [], "s", color=STATISTIQUE, label="methode statistique ou d'imputation")
    leg = ax1.legend(loc="lower right", frameon=False, fontsize=8.4,
                     labelcolor=ENCRE_SECONDE, handlelength=1.6,
                     bbox_to_anchor=(0.998, 0.02))
    for t in leg.get_texts():
        t.set_color(ENCRE_SECONDE)

    fig.suptitle("L'avantage sur les reponses rares tient sur les raretes que la personne "
                 "reproduit, et il est plus grand la que sur les raretes instables",
                 fontsize=13.5, color=ENCRE, x=0.010, ha="left", y=1.005)
    fig.text(0.010, -0.030,
             "Lecture : sur les reponses rares qu'une personne redonne a deux semaines, "
             "c'est a dire de la vraie heterogeneite et non du bruit de reponse, "
             "`agents composite` retrouve 29 points de rappel de plus\nqu'un tirage au "
             "sort dans le segment ideologie x genre x age de cette personne, quand la "
             "regression logistique en retrouve 3,5 de moins et la foret aleatoire 8,8 de "
             "moins. a42, 8 septembre 2026,\npreenregistre, zero appel de modele de "
             "langage. La ligne `humains vague 2` n'est pas tracee : sur cette partition "
             "elle vaut 1 sur les stables et 0 sur les instables par construction.",
             fontsize=8.5, color=ENCRE_SECONDE, ha="left", va="top")
    fig.tight_layout()

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a42-figure-plancher.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print(f"ecrit : {chemin}")


if __name__ == "__main__":
    main()
