"""
a39_figure : l'exactitude par tranche de la vraie valeur humaine, une courbe par methode.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par a39_tranches.py, pour que la figure et les chiffres du rapport ne
puissent pas diverger. Aucun script existant n'est modifie. La palette et les conventions
de trace sont celles de a25_figure, a28_figures et a29_figure, importees telles quelles.

Entree  : resultats/a39-tranches.csv, a39-ecarts-types-decomposition.csv
Sortie  : resultats/a39-figure-tranches.png et .svg

Usage : .venv/bin/python analyses/a39_figure.py
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
import a39_commun as A

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

ETIQUETTE = "#b8860b"   # les conditions qui ne recoivent qu'une etiquette de segment
AVEUGLE = "#8d8b86"

COURT = {
    "agents composite": "composite", "agents entretien (v3)": "entretien",
    "agents enquete": "enquete", "agents demographiques (v6)": "demo v6",
    "agents v7": "v7", "agents v8": "v8", "C2": "C2", "C3": "C3",
    "B0 mode": "B0 mode", "B0 tirage": "B0 tirage", "B0 uniforme": "B0 uniforme",
    "B1 argmax": "B1", "B2 argmax": "B2", "B3 foret": "B3 foret",
    "humains vague 2": "humains vague 2",
}

TRANCHES = ["bas", "milieu", "haut"]


def couleur(cond):
    f = A.FAMILLE_CONDITION.get(cond, "")
    if f == "plancher":
        return HUMAIN
    if f == "etiquette":
        return ETIQUETTE
    if f == "riche":
        return LANGAGE
    if f == "statistique":
        return STATISTIQUE
    return AVEUGLE


def lire(nom):
    d = pd.read_csv(os.path.join(SORTIE, nom))
    # la colonne perimetre porte "150" et "1052" : pandas la lit en entier, ce qui ferait
    # echouer toutes les selections par chaine
    if "perimetre" in d.columns:
        d["perimetre"] = d["perimetre"].astype(str)
    return d


def panneau(ax, d, titre, sous_titre, peng=None, ancre="droite"):
    """Une courbe par methode : exactitude sur les trois tranches, avec intervalle."""
    style(ax, axe_grille="y")
    x = np.arange(len(TRANCHES))
    conds = [c for c in A.ORDRE_METHODES if c in set(d.condition)]
    for cond in conds:
        g = d[d.condition == cond].set_index("tranche")
        if not all(t in g.index for t in TRANCHES):
            continue
        y = np.array([g.loc[t, "exactitude"] for t in TRANCHES], dtype=float)
        lo = np.array([g.loc[t, "ic_bas"] for t in TRANCHES], dtype=float)
        hi = np.array([g.loc[t, "ic_haut"] for t in TRANCHES], dtype=float)
        c = couleur(cond)
        humain = cond == "humains vague 2"
        ax.fill_between(x, lo, hi, color=c, alpha=0.10, linewidth=0, zorder=2)
        ax.plot(x, y, "-o", color=c, linewidth=2.2 if humain else 1.4,
                markersize=5 if humain else 3.6,
                markeredgecolor=ENCRE if humain else "none",
                markeredgewidth=0.8 if humain else 0, zorder=4 if humain else 3)
        k, dx, ha = ((-1, 6, "left") if ancre == "droite" else (0, -6, "right"))
        ax.annotate(COURT.get(cond, cond), (x[k], y[k]), textcoords="offset points",
                    xytext=(dx, 0), fontsize=7, color=c, va="center", ha=ha,
                    fontweight="bold" if humain else "normal")
    if peng:
        for spec, val in peng.items():
            yv = [val[t] for t in TRANCHES]
            ax.plot(x, yv, "--", color=NEUTRE, linewidth=1.0, zorder=1)
            ax.annotate(spec, (x[0], yv[0]), textcoords="offset points",
                        xytext=(-6, 0), fontsize=6.5, color=NEUTRE, ha="right",
                        va="center")
    ax.set_xticks(x)
    ax.set_xticklabels(["5 % du bas", "90 % du milieu", "5 % du haut"], fontsize=8.5)
    ax.set_xlim(-0.95 if ancre == "gauche" else -0.55,
                len(TRANCHES) - 0.35 if ancre == "droite" else len(TRANCHES) - 0.85)
    ax.set_ylabel("exactitude", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=10.5, color=ENCRE, loc="left", pad=26)
    ax.text(0, 1.012, sous_titre, transform=ax.transAxes, fontsize=7.6,
            color=ENCRE_SECONDE, va="bottom")


def panneau_decomposition(ax, d):
    """Le rapport inter en abscisse contre le rapport intra en ordonnee."""
    style(ax, axe_grille="both")
    ax.axhline(1.0, color=GRILLE, linewidth=1.0, zorder=1)
    ax.axvline(1.0, color=GRILLE, linewidth=1.0, zorder=1)
    for _, row in d.iterrows():
        c = couleur(row.condition)
        cerne = row.condition in ("C2", "C3")
        ax.plot(row.ratio_inter, row.ratio_intra, "o", color=c,
                markersize=7 if cerne else 5.5,
                markeredgecolor=ENCRE if cerne else "none",
                markeredgewidth=0.9 if cerne else 0, zorder=3)
        ax.annotate(COURT.get(row.condition, row.condition),
                    (row.ratio_inter, row.ratio_intra), textcoords="offset points",
                    xytext=(7, 2), fontsize=7, color=c)
    ax.set_xscale("log")
    ax.set_xlabel("rapport d'ecarts types INTER segments ideologiques", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_ylabel("rapport INTRA segment", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("4. Ce que leur rapport total confond", fontsize=10.5, color=ENCRE,
                 loc="left", pad=26)
    ax.text(0, 1.012, "C2 et C3 ont le meme rapport total, 0,77 et 0,78, et deux "
                      "positions opposees sur ce plan",
            transform=ax.transAxes, fontsize=7.6, color=ENCRE_SECONDE, va="bottom")
    ax.text(0.98, 0.04, "le point de fidelite parfaite est (1 ; 1)", fontsize=7.5,
            color=NEUTRE, transform=ax.transAxes, ha="right")


def main():
    t = lire("a39-tranches.csv")
    dec = lire("a39-ecarts-types-decomposition.csv")
    t = t[t.tranche != "ensemble"]

    fig, axes = plt.subplots(2, 2, figsize=(13.6, 10.4))
    fig.patch.set_facecolor(FOND)

    panneau(axes[0][0],
            t[(t.definition == "rarete") & (t.perimetre == "1052")],
            "1. Tranches de rarete, concordance exacte, 1 052 personnes",
            "bas = vraie modalite donnee par moins de 5 % des repondants de l'item ; "
            "haut = modalite majoritaire au dela de 95 %", ancre="gauche")
    panneau(axes[0][1],
            t[(t.definition == "ordinale") & (t.perimetre == "1052")],
            "2. Tranches ordinales, leur mesure, 71 items, 1 052 personnes",
            "tri par la vraie valeur ; exactitude 1 - |predit - vrai| / etendue ; "
            "en gris, leurs quatre specifications publiees",
            peng=A.PENG_TRANCHES)
    panneau(axes[1][0],
            t[(t.definition == "ordinale") & (t.perimetre == "150")],
            "3. Tranches ordinales, 150 personnes, avec l'ablation C2 contre C3",
            "meme modele, memes personnes, memes questions ; C2 recoit l'etiquette, "
            "C3 ne la recoit pas")
    dec_fig = pd.concat(
        [dec[dec.perimetre == "1052"],
         dec[(dec.perimetre == "150") & (dec.condition.isin(["C2", "C3"]))]],
        ignore_index=True)
    panneau_decomposition(axes[1][1], dec_fig)

    poignees = [
        plt.Line2D([], [], marker="o", linestyle="-", color=LANGAGE,
                   label="condition riche en information individuelle"),
        plt.Line2D([], [], marker="o", linestyle="-", color=ETIQUETTE,
                   label="condition a etiquette de segment seule"),
        plt.Line2D([], [], marker="o", linestyle="-", color=STATISTIQUE,
                   label="predicteur statistique"),
        plt.Line2D([], [], marker="o", linestyle="-", color=AVEUGLE,
                   label="temoin aveugle a la personne"),
        plt.Line2D([], [], marker="o", linestyle="-", color=HUMAIN,
                   label="memes humains reinterroges, plancher de bruit"),
    ]
    fig.legend(handles=poignees, loc="lower center", ncol=3, fontsize=8.5,
               frameon=False, labelcolor=ENCRE_SECONDE, bbox_to_anchor=(0.5, 0.004))
    fig.suptitle("a39. La mesure de queue de Peng et al., rejouee sur le GSS",
                 fontsize=13, color=ENCRE, x=0.055, ha="left", y=0.985)
    fig.tight_layout(rect=[0, 0.075, 1, 0.962])
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a39-figure-tranches.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND)
        print(f"ecrit : {chemin}")


if __name__ == "__main__":
    main()
