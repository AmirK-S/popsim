"""
a29_figure : rappel contre precision sur les cellules minoritaires, et la correlation par
personne qui separe "garder la masse" de "garder les bonnes personnes".

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par a29_mesures.py, pour que la figure et les chiffres du rapport ne
puissent pas diverger. Aucun script existant n'est modifie. La palette et les conventions
de trace sont celles de a25_figure et de a28_figures, importees telles quelles.

Entree  : resultats/a29-minorites-global.csv, a29-correlation-personne.csv
Sortie  : resultats/a29-figure-minorites.png et .svg

Usage : .venv/bin/python analyses/a29_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_commun import LLM, ORDRE_METHODES, STAT
from a28_figures import (ENCRE, ENCRE_SECONDE, FOND, GRILLE, HUMAIN, LANGAGE, NEUTRE,
                         STATISTIQUE, couleur, style)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

# Abreviations d'affichage : les noms complets ne tiennent pas a cote d'un point.
COURT = {
    "agents composite": "composite", "agents entretien (v3)": "entretien",
    "agents enquete": "enquete", "agents demographiques (v6)": "demo v6",
    "agents v7": "v7", "agents v8": "v8", "C2": "C2", "C3": "C3",
    "B0 mode": "B0 mode", "B0 tirage": "B0 tirage", "B1 argmax": "B1",
    "B2 argmax": "B2", "B3 foret": "B3 foret", "humains vague 2": "humains vague 2",
}

# Decalage manuel des etiquettes, en points, pour eviter les chevauchements.
DECALAGE = {
    "1052": {"agents composite": (7, 4), "agents entretien (v3)": (7, -10),
             "agents enquete": (7, 2), "agents demographiques (v6)": (7, 3),
             "agents v7": (7, -11), "agents v8": (7, 2), "B0 tirage": (7, -3),
             "B1 argmax": (7, 2), "B2 argmax": (-8, 4), "B3 foret": (7, -9),
             "humains vague 2": (-12, 8), "B0 mode": (7, 2)},
    "150": {"agents composite": (7, 4), "agents entretien (v3)": (7, -10),
            "agents enquete": (7, 2), "agents demographiques (v6)": (7, 3),
            "agents v7": (-8, -9), "agents v8": (-8, 5), "C2": (8, -10),
            "C3": (8, 3), "B0 tirage": (8, -11), "B1 argmax": (-8, -9),
            "B2 argmax": (-8, 4), "B3 foret": (7, -9),
            "humains vague 2": (-12, 8), "B0 mode": (7, 2)},
}


def lire(nom):
    return pd.read_csv(os.path.join(SORTIE, nom))


def nuage(ax, d, nom_per, titre):
    """Rappel en abscisse, precision en ordonnee, une methode par point."""
    style(ax, axe_grille="both")
    # courbes d'iso F1, en fond : elles disent ce que vaut un point sans le lire deux fois
    r = np.linspace(0.005, 0.70, 400)
    for f in (0.1, 0.2, 0.3, 0.4, 0.5):
        with np.errstate(divide="ignore", invalid="ignore"):
            p = f * r / (2 * r - f)
        p = np.where((p > 0) & (p <= 0.78), p, np.nan)
        ax.plot(r, p, color=GRILLE, linewidth=0.9, zorder=1)
        bord = f * 0.70 / (2 * 0.70 - f)
        ax.text(0.712, bord, f"F1 = {f:.1f}", fontsize=7, color=NEUTRE,
                ha="left", va="center", zorder=1)

    for _, row in d.iterrows():
        cond = row.condition
        if not np.isfinite(row.precision):
            continue
        c = couleur(cond)
        gros = cond == "humains vague 2"
        ax.plot([row.rappel_ic_bas, row.rappel_ic_haut], [row.precision] * 2,
                color=NEUTRE, linewidth=1.0, zorder=2, alpha=0.7)
        ax.plot([row.rappel] * 2, [row.precision_ic_bas, row.precision_ic_haut],
                color=NEUTRE, linewidth=1.0, zorder=2, alpha=0.7)
        ax.plot([row.rappel], [row.precision], "o", color=c,
                markersize=9.0 if gros else 6.5, zorder=4,
                markeredgecolor=ENCRE if gros else "none",
                markeredgewidth=1.1 if gros else 0)
        dx, dy = DECALAGE[nom_per].get(cond, (7, 2))
        ax.annotate(COURT.get(cond, cond), (row.rappel, row.precision),
                    textcoords="offset points", xytext=(dx, dy),
                    fontsize=8.2 if gros else 7.8,
                    color=ENCRE if gros else ENCRE_SECONDE,
                    fontweight="bold" if gros else "normal", zorder=5,
                    ha="right" if dx < 0 else "left")

    ax.set_xlim(-0.02, 0.80)
    ax.set_ylim(-0.02, 0.78)
    ax.set_xlabel("rappel : part des reponses rares reelles retrouvees",
                  fontsize=9.5, color=ENCRE_SECONDE)
    ax.set_ylabel("precision : quand la methode ose une modalite rare, a t elle raison",
                  fontsize=9.5, color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=11, color=ENCRE, loc="left")


def barres(ax, k, titre):
    """Correlation par personne, rares reelles contre rares predites."""
    style(ax, axe_grille="x")
    ordre = [c for c in ORDRE_METHODES if c in set(k.condition)]
    ordre = [c for c in ordre if np.isfinite(
        float(k[k.condition == c].rho_spearman.iloc[0]))]
    plafond = float(k[k.condition == "humains vague 2"].rho_spearman.iloc[0])
    ax.axvline(plafond, color=HUMAIN, linewidth=1.2, linestyle="--", zorder=1)
    ax.axvline(0, color=ENCRE_SECONDE, linewidth=1.0, zorder=1)
    for i, cond in enumerate(ordre):
        r = k[k.condition == cond].iloc[0]
        ax.plot([r.ic_bas, r.ic_haut], [i, i], color=NEUTRE, linewidth=1.4, zorder=2)
        ax.plot([r.rho_spearman], [i], "o", color=couleur(cond), markersize=6.5, zorder=3)
    ax.set_yticks(range(len(ordre)))
    ax.set_yticklabels([COURT.get(c, c) for c in ordre], fontsize=8.6, color=ENCRE)
    ax.set_ylim(len(ordre) + 0.2, -0.6)
    ax.set_xlim(-0.12, 0.88)
    ax.set_xlabel("correlation de rang, par personne", fontsize=9.5, color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=11, color=ENCRE, loc="left")
    ax.text(plafond - 0.015, len(ordre) - 0.05, "plafond humain", fontsize=7.6,
            color=HUMAIN, ha="right", va="center")
    ax.text(0.015, len(ordre) - 0.05, "rarete distribuee au hasard", fontsize=7.6,
            color=NEUTRE, ha="left", va="center")


def main():
    glob = lire("a29-minorites-global.csv")
    corr = lire("a29-correlation-personne.csv")
    glob = glob[glob.seuil == 0.10]
    corr = corr[corr.seuil == 0.10]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(17.0, 6.4),
                                        gridspec_kw={"wspace": 0.36})
    fig.patch.set_facecolor(FOND)

    nuage(ax1, glob[glob.perimetre == 1052], "1052",
          "1. Les 1 052 personnes, six conditions de Stanford\net cinq predicteurs "
          "statistiques")
    nuage(ax2, glob[glob.perimetre == 150], "150",
          "2. Les 150 personnes du run local, avec nos C2 et C3\net la meme reference "
          "restreinte")
    barres(ax3, corr[corr.perimetre == 1052].copy(),
           "3. Les bonnes personnes : nombre de reponses rares\nreelles contre nombre "
           "predit, perimetre 1 052")

    ax1.plot([], [], "o", color=LANGAGE, label=f"condition a modele de langage ({len(LLM)})")
    ax1.plot([], [], "o", color=STATISTIQUE, label=f"predicteur statistique ({len(STAT)})")
    ax1.plot([], [], "o", color=HUMAIN, label="memes humains reinterroges")
    ax1.legend(loc="upper center", bbox_to_anchor=(1.75, -0.13), ncol=3, fontsize=9,
               frameon=False, labelcolor=ENCRE_SECONDE)

    fig.suptitle("a29. Les minorites gardees sont elles les bonnes personnes ? "
                 "Cellules ou la vraie reponse est donnee par moins de 10 pour cent "
                 "des humains",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left")
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a29-figure-minorites.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
