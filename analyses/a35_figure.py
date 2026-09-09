"""
a35_figure : le plan exactitude contre ratio intra, avec le terme inter en taille de point.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit
`resultats/a35-tableau-quatre-cases.csv` et `a35-front-pareto.csv` ecrits par
a35_imputation.py, pour que la figure et les chiffres du rapport ne puissent pas diverger.
Aucun script existant n'est modifie. Le fond, l'encre, la grille et la couleur des humains
sont ceux de a28_figures, importes tels quels ; deux couleurs sont ajoutees ici pour
separer les deux regimes d'imputation, qui n'existaient pas dans les figures precedentes.

Ce que la figure montre, et pourquoi ces axes. L'abscisse est l'exactitude individuelle,
la quantite que la litterature publie. L'ordonnee est le ratio de dispersion INTRA groupe,
rapporte aux memes humains : un ratio de 1 veut dire que la methode laisse les gens d'un
meme segment aussi differents les uns des autres qu'ils le sont vraiment, un ratio bas veut
dire qu'elle les rend semblables. La taille du point porte la troisieme dimension, le ratio
de dispersion INTER groupes : un gros point est une methode qui exagere les ecarts entre
segments. Le second panneau lit cette troisieme dimension directement, en echelle
logarithmique, parce qu'un rapport de 8 et un rapport de 1,5 ne se distinguent pas a l'oeil
sur une aire de disque.

Entree  : resultats/a35-tableau-quatre-cases.csv, a35-front-pareto.csv
Sortie  : resultats/a35-figure-imputation.png et .svg

Usage : .venv/bin/python analyses/a35_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import ENCRE, ENCRE_SECONDE, FOND, GRILLE, HUMAIN, LANGAGE, NEUTRE, style

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

# Deux couleurs nouvelles pour les deux regimes d'imputation. Le bleu de a28 designait
# "predicteur statistique" en bloc ; ici la distinction utile n'est plus statistique contre
# langage, c'est esperance contre tirage, et il faut deux teintes. Le violet est choisi
# contre le rouge du langage plutot qu'un orange, qui se confondrait avec lui.
ESPERANCE = "#2a78d6"
TIRAGE = "#7d5ba6"

COULEUR_REGIME = {"esperance": ESPERANCE, "tirage": TIRAGE,
                  "modele de langage": LANGAGE, "humains": HUMAIN}

COURT = {
    "agents composite": "composite", "agents entretien (v3)": "entretien",
    "agents enquete": "enquete", "agents demographiques (v6)": "demo v6",
    "agents v7": "v7", "agents v8": "v8", "C2": "C2", "C3": "C3",
    "B0 mode": "B0 mode", "B0 tirage": "B0 tirage",
    "B1 argmax": "B1 argmax", "B1 tirage": "B1 tirage",
    "B2 argmax": "B2 argmax (hot deck mode)", "B2 tirage": "B2 tirage (hot deck k=30)",
    "B3 foret": "B3 foret",
    "E1 regression contexte argmax": "E1 esperance",
    "E2 regression contexte tirage": "E2 tirage",
    "PMM k=5": "PMM k=5", "PMM k=10": "PMM k=10",
    "IM m=10 mode des m": "IM mode des 10",
    "hot deck k=5 tirage": "hot deck k=5", "hot deck k=10 tirage": "hot deck k=10",
    "humains vague 2": "humains vague 2",
}

# Decalage manuel des etiquettes, en points, un jeu par panneau : les memes methodes ne
# se bousculent pas aux memes endroits selon que l'ordonnee porte le terme intra ou le
# terme inter.
DECALAGE = {
    "intra": {
        "E1 regression contexte argmax": (9, -3),
        "E2 regression contexte tirage": (9, 4),
        "PMM k=5": (9, 8), "PMM k=10": (9, -3),
        "IM m=10 mode des m": (-9, 8),
        "B2 argmax": (-9, 1), "B2 tirage": (-9, -13),
        "B1 argmax": (-9, -10), "B1 tirage": (2, -13),
        "B0 mode": (9, -1), "B0 tirage": (9, 2),
        "B3 foret": (-9, 2),
        "hot deck k=5 tirage": (9, -11), "hot deck k=10 tirage": (2, 9),
        "agents composite": (9, 4), "agents entretien (v3)": (9, -9),
        "agents enquete": (-9, 7), "agents demographiques (v6)": (9, -9),
        "agents v7": (-9, -10), "agents v8": (9, 1),
        "C2": (9, -9), "C3": (9, 3), "humains vague 2": (-11, 8),
    },
    "inter": {
        "E1 regression contexte argmax": (9, 0),
        "E2 regression contexte tirage": (2, -13),
        "PMM k=5": (-9, -11), "PMM k=10": (-9, 7),
        "IM m=10 mode des m": (9, -9),
        "B2 argmax": (-9, 2), "B2 tirage": (-9, 2),
        "B1 argmax": (-9, -10), "B1 tirage": (-9, 6),
        "B3 foret": (-2, 10),
        "hot deck k=5 tirage": (9, 3), "hot deck k=10 tirage": (-2, -13),
        "agents composite": (9, 2), "agents entretien (v3)": (9, 2),
        "agents enquete": (-9, 6), "agents demographiques (v6)": (9, -4),
        "agents v7": (-9, -10), "agents v8": (9, -2),
        "C2": (9, -9), "C3": (9, 3), "humains vague 2": (-11, -14),
    },
}


def taille(inter):
    """Aire du disque croissante avec le ratio inter, plancher a zero.

    La racine carree plutot que la valeur brute : c'est l'aire du disque, et non son
    diametre, qui doit etre proportionnelle a la quantite lue, sinon un rapport de 8
    parait huit fois plus gros qu'il ne l'est.
    """
    v = max(float(inter), 0.0)
    return 4.0 + 8.5 * np.sqrt(v)


def points(ax, d, x, y, front, panneau):
    for _, r in d.iterrows():
        if not np.isfinite(r[x]) or not np.isfinite(r[y]):
            continue
        c = COULEUR_REGIME[r.regime]
        humain = r.methode == "humains vague 2"
        sur = bool(front.get(r.methode, False))
        ax.plot([r[x]], [r[y]], "o", color=c, markersize=taille(r.ratio_inter_ideologie),
                zorder=4, alpha=0.92,
                markeredgecolor=ENCRE if (humain or sur) else "none",
                markeredgewidth=1.3 if humain else (0.9 if sur else 0))
        dx, dy = DECALAGE[panneau].get(r.methode, (9, 2))
        ax.annotate(COURT.get(r.methode, r.methode), (r[x], r[y]),
                    textcoords="offset points", xytext=(dx, dy),
                    fontsize=8.4 if humain else 7.8,
                    color=ENCRE if humain else ENCRE_SECONDE,
                    fontweight="bold" if humain else "normal", zorder=5,
                    ha="right" if dx < 0 else "left")


def main():
    d = pd.read_csv(os.path.join(SORTIE, "a35-tableau-quatre-cases.csv"))
    pf = pd.read_csv(os.path.join(SORTIE, "a35-front-pareto.csv"))
    front = dict(zip(pf.methode, pf.sur_le_front))

    base = d[d.perimetre == 1052].copy()
    c23 = d[(d.perimetre == 150) & (d.methode.isin(["C2", "C3"]))].copy()
    t = pd.concat([base, c23], ignore_index=True)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.4, 7.0))
    fig.patch.set_facecolor(FOND)

    # ---- panneau gauche : le plan demande, exactitude contre ratio intra
    style(ax1, axe_grille="both")
    ax1.axhline(1.0, color=HUMAIN, linewidth=1.2, linestyle="--", zorder=1)
    ax1.axvline(0.795, color=HUMAIN, linewidth=1.2, linestyle="--", zorder=1)
    ax1.text(0.474, 1.005, "dispersion intra humaine", fontsize=7.6, color=HUMAIN,
             ha="left", va="bottom", zorder=2)
    points(ax1, t, "exactitude", "ratio_intra_ideologie", front, "intra")
    ax1.set_xlim(0.47, 0.83)
    ax1.set_ylim(-0.02, 1.13)
    ax1.set_xlabel("exactitude individuelle, 149 items, egalite exacte",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax1.set_ylabel("ratio de dispersion intra groupe, methode sur humains",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax1.set_title("Le plan des methodes d'imputation. Taille du point : ratio inter groupes",
                  fontsize=11, color=ENCRE, loc="left")

    # ---- panneau droit : la troisieme dimension lue directement
    style(ax2, axe_grille="both")
    ax2.axhline(1.0, color=HUMAIN, linewidth=1.2, linestyle="--", zorder=1)
    ax2.axvline(0.795, color=HUMAIN, linewidth=1.2, linestyle="--", zorder=1)
    ax2.text(0.828, 1.07, "dispersion inter humaine", fontsize=7.6, color=HUMAIN,
             ha="right", va="bottom", zorder=2)
    t2 = t[t.ratio_inter_ideologie > 0.05]
    points(ax2, t2, "exactitude", "ratio_inter_ideologie", front, "inter")
    ax2.set_yscale("log")
    ax2.set_xlim(0.47, 0.83)
    ax2.set_ylim(0.10, 12.0)
    ax2.set_yticks([0.125, 0.25, 0.5, 1, 2, 4, 8])
    ax2.set_yticklabels(["0,125", "0,25", "0,5", "1", "2", "4", "8"])
    ax2.set_xlabel("exactitude individuelle, 149 items, egalite exacte",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax2.set_ylabel("ratio de dispersion inter groupes, echelle logarithmique",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax2.set_title("La meme population, vue par le terme inter. `B0` est hors cadre, "
                  "son inter est nul",
                  fontsize=11, color=ENCRE, loc="left")

    for ax in (ax1, ax2):
        ax.plot([], [], "o", color=ESPERANCE, markersize=7,
                label="imputation par esperance")
        ax.plot([], [], "o", color=TIRAGE, markersize=7, label="imputation par tirage")
        ax.plot([], [], "o", color=LANGAGE, markersize=7, label="modele de langage")
        ax.plot([], [], "o", color=HUMAIN, markersize=7, label="memes humains reinterroges")
        ax.plot([], [], "o", color="none", markeredgecolor=ENCRE, markeredgewidth=0.9,
                markersize=7, label="sur le front de Pareto a trois criteres")
    ax1.legend(loc="upper center", bbox_to_anchor=(1.06, -0.10), ncol=5, fontsize=8.5,
               frameon=False, labelcolor=ENCRE_SECONDE)

    fig.suptitle("a35. Ou se place un agent de langage parmi les methodes d'imputation, "
                 "sur les memes 1 052 personnes et les memes 149 items",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left", y=0.985)
    fig.text(0.012, 0.925,
             "Segmentation : ideologie politique, sept niveaux. Dispersion : indice de "
             "Gini Simpson, estimateur sans biais de a1. C2 et C3 sont mesurees sur leurs "
             "150 personnes, toutes les autres sur 1 052.",
             fontsize=8.6, color=ENCRE_SECONDE, ha="left")
    fig.subplots_adjust(top=0.86, bottom=0.16, wspace=0.22)

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a35-figure-imputation.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
