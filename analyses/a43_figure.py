"""
a43_figure : le R2 demoyenne par methode, avec et sans retrait de la moyenne de segment.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit
`resultats/a43-r2-demoyenne.csv` ecrit par a43_r2_demoyenne.py, pour que la figure et les
chiffres du rapport ne puissent pas diverger. Aucun script existant n'est modifie. Le
fond, l'encre, la grille et les couleurs sont ceux de a28_figures, importes tels quels.

Ce que la figure montre. Deux panneaux, un par perimetre. Pour chaque methode, deux
barres : a gauche la part de variance individuelle expliquee apres retrait de la seule
moyenne d'item, a droite la meme quantite apres retrait en plus de la moyenne du segment
ideologie x genre x age. La difference entre les deux barres est ce que la methode ne
savait que parce qu'elle connaissait le groupe. Les deux traits verticaux sont les deux
plafonds correspondants, mesures sur les MEMES humains reinterroges deux semaines plus
tard. La barre d'incertitude est un bootstrap sur les personnes.

Entree  : resultats/a43-r2-demoyenne.csv
Sortie  : resultats/a43-figure-r2.png et .svg

Usage : .venv/bin/python analyses/a43_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import (ENCRE, ENCRE_SECONDE, FOND, HUMAIN, LANGAGE, NEUTRE,
                         STATISTIQUE, enregistrer, lire, style)

COURT = {
    "agents composite": "composite", "agents entretien (v3)": "entretien",
    "agents enquete": "enquete", "agents demographiques (v6)": "demo v6",
    "agents v7": "v7", "agents v8": "v8", "C2": "C2 etiquette", "C3": "C3 sans etiquette",
    "PMM k=5": "PMM k=5", "PMM k=10": "PMM k=10", "IM m=10 mode des m": "IM m=10",
    "B0 mode": "B0 mode", "B1 argmax": "B1 argmax", "B2 argmax": "B2 argmax",
    "B3 foret": "B3 foret",
}

ORDRE = ["agents composite", "agents entretien (v3)", "agents enquete",
         "IM m=10 mode des m", "PMM k=5", "PMM k=10", "B2 argmax", "C3",
         "B1 argmax", "B3 foret", "agents demographiques (v6)", "agents v7",
         "agents v8", "C2", "B0 mode"]

IMPUTATION = "#7d5ba6"


def couleur(cond):
    if cond in ("PMM k=5", "PMM k=10", "IM m=10 mode des m"):
        return IMPUTATION
    if cond.startswith("agents") or cond in ("C2", "C3"):
        return LANGAGE
    return STATISTIQUE


def main():
    df = lire("a43-r2-demoyenne.csv")
    df["perimetre"] = df["perimetre"].astype(str)
    v_item = "moyenne d'item"
    v_seg = "moyenne d'item et de segment 18"

    fig, axes = plt.subplots(1, 2, figsize=(12.6, 7.0), sharex=True)
    fig.patch.set_facecolor(FOND)

    for ax, nom_per, titre in zip(
            axes, ("1052", "150"),
            ("1 052 personnes, 13 methodes",
             "150 personnes du run local, C2 et C3 comprises")):
        s = df[df["perimetre"] == nom_per]
        conds = [c for c in ORDRE if c in set(s["condition"])]
        y = np.arange(len(conds))[::-1]
        h = 0.36
        for k, (variante, hachure, etiquette) in enumerate(
                ((v_item, "", "moyenne d'item retiree"),
                 (v_seg, "///", "moyenne d'item et de segment retirees"))):
            vals, bas, haut, coul = [], [], [], []
            for c in conds:
                r = s[(s["condition"] == c) & (s["variante"] == variante)].iloc[0]
                vals.append(100 * r["r2"])
                bas.append(100 * r["r2_ic_bas"])
                haut.append(100 * r["r2_ic_haut"])
                coul.append(couleur(c))
            dec = h / 2 if k == 0 else -h / 2
            ax.barh(y + dec, vals, height=h, color=coul, edgecolor=FOND,
                    linewidth=0.6, hatch=hachure, alpha=1.0 if k == 0 else 0.75,
                    zorder=3)
            ax.hlines(y + dec, bas, haut, color=ENCRE_SECONDE, linewidth=1.0, zorder=4)

        for variante, trait, lib in ((v_item, "-", "plafond humain, moyenne d'item"),
                                     (v_seg, "--", "plafond humain, item et segment")):
            p = s[(s["condition"] == "humains vague 2") & (s["variante"] == variante)]
            if len(p):
                ax.axvline(100 * p.iloc[0]["r2"], color=HUMAIN, linewidth=1.4,
                           linestyle=trait, zorder=2)

        ax.set_yticks(y)
        ax.set_yticklabels([COURT.get(c, c) for c in conds], fontsize=9.5,
                           color=ENCRE)
        style(ax, axe_grille="x")
        ax.set_title(titre, fontsize=11, color=ENCRE, loc="left")
        ax.set_xlabel("part de variance individuelle expliquee, en pour cent",
                      fontsize=9.5, color=ENCRE_SECONDE)
        ax.set_xlim(0, 46)

    from matplotlib.patches import Patch
    from matplotlib.lines import Line2D
    poignees = [
        Patch(facecolor=NEUTRE, edgecolor=FOND, label="moyenne d'item retiree"),
        Patch(facecolor=NEUTRE, edgecolor=FOND, hatch="///", alpha=0.75,
              label="item ET segment ideologie x genre x age retires"),
        Line2D([], [], color=HUMAIN, linewidth=1.4,
               label="plafond humain a deux semaines"),
    ]
    axes[0].legend(handles=poignees, loc="upper center", bbox_to_anchor=(1.05, -0.085),
                   ncol=3, fontsize=8.5, frameon=False, labelcolor=ENCRE_SECONDE)

    fig.suptitle("a43. Ce qui reste d'une personne quand on lui retire son item, "
                 "puis son groupe", fontsize=13, color=ENCRE, x=0.02, ha="left")
    fig.text(0.02, 0.945,
             "Mesure de Ahn, Mao et Lee sur nos 71 items ordinaux. Barres : bootstrap "
             "2 000 tirages sur les personnes. Rouge, modele de langage ; violet, "
             "imputation ; bleu, predicteur statistique. Le plafond est en trait plein "
             "sans retrait de segment, en tirete avec.",
             fontsize=9, color=ENCRE_SECONDE, ha="left")
    fig.tight_layout(rect=[0, 0.03, 1, 0.92])
    enregistrer(fig, "a43-figure-r2")


if __name__ == "__main__":
    main()
