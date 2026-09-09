"""
a34_figure : le rappel des cellules minoritaires par tercile de deductibilite.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par `a34_deductibilite.py`, pour que la figure et les chiffres du rapport
ne puissent pas diverger. Aucun script existant n'est modifie. La palette et les
conventions de trace sont celles de a25_figure, a28_figures, a29_figure et a31_figure,
importees telles quelles.

Trois panneaux, une courbe par methode, terciles de deductibilite en abscisse.

  1. Partition principale, D_seg, perimetre 1 052. Les deux planchers en pointille : le
     tirage dans la marginale du segment de la personne, qui est le plancher de bruit de
     cellule de la lecture 01, et le tirage dans la marginale de l'item, esperance de
     `B0 tirage`.
  2. Partition secondaire, D_logit, perimetre 1 052. La ligne de `B1 argmax` y est plate a
     zero sur T1 et T2 par arithmetique et non par mesure : la partition est sa propre
     confiance. L'avertissement est ecrit dans le panneau.
  3. Perimetre 150, partition D_seg, avec C2 et C3.

Entree  : resultats/a34-par-tercile.csv, a34-terciles-description.csv
Sortie  : resultats/a34-figure-rarete-deductible.png et .svg

Usage : .venv/bin/python analyses/a34_figure.py
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
from a29_figure import COURT

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

TERCILES = ["T1 non deductible", "T2 intermediaire", "T3 deductible"]
ETIQUETTES = ["T1\nnon deductible", "T2\nintermediaire", "T3\ndeductible"]


def panneau(ax, mes, desc, perimetre, partition, titre, sous_titre, avec_c2c3):
    s = mes[(mes.perimetre == perimetre) & (mes.seuil == 0.10)
            & (mes.partition == partition)]
    d = desc[(desc.perimetre == perimetre) & (desc.seuil == 0.10)
             & (desc.partition == partition)]
    xs = np.arange(3)

    # Les deux planchers, en pointille, traces avant les courbes pour rester en fond.
    pl_seg = [float(d[d.tercile == t]["plancher_segment"].iloc[0]) for t in TERCILES]
    pl_item = [float(d[d.tercile == t]["plancher_item"].iloc[0]) for t in TERCILES]
    ax.plot(xs, pl_seg, linestyle=(0, (4, 3)), color=ENCRE, linewidth=2.0, zorder=3)
    ax.plot(xs, pl_item, linestyle=(0, (1, 2)), color=NEUTRE, linewidth=2.0, zorder=3)
    ax.annotate("plancher : tirage dans la marginale du segment",
                (xs[-1], pl_seg[-1]), textcoords="offset points", xytext=(-6, 7),
                ha="right", fontsize=8, color=ENCRE, style="italic")
    ax.annotate("plancher : tirage dans la marginale de l'item",
                (xs[0], pl_item[0]), textcoords="offset points", xytext=(2, -15),
                ha="left", fontsize=8, color=NEUTRE, style="italic")

    conditions = [c for c in ORDRE_METHODES if c in set(s.condition)]
    if not avec_c2c3:
        conditions = [c for c in conditions if c not in ("C2", "C3")]
    etiquettes = []
    for cond in conditions:
        v = [s[(s.condition == cond) & (s.tercile == t)]["rappel"] for t in TERCILES]
        v = [float(a.iloc[0]) if len(a) else np.nan for a in v]
        if all(np.isnan(a) for a in v):
            continue
        col = couleur(cond)
        gros = cond in ("agents composite", "B1 argmax", "humains vague 2", "C2", "C3")
        ax.plot(xs, v, marker="o", markersize=5.5 if gros else 4.0,
                linewidth=2.4 if gros else 1.3, color=col,
                alpha=1.0 if gros else 0.55, zorder=6 if gros else 4)
        etiquettes.append([v[-1], COURT.get(cond, cond), col, gros])

    # Ecartement des etiquettes de fin de courbe : elles se chevauchent sinon, et une
    # etiquette illisible vaut moins qu'une etiquette deplacee de deux millemes de rappel.
    # Le point de la courbe n'est pas deplace, seul le texte l'est.
    ecart = 0.026
    etiquettes.sort(key=lambda e: e[0])
    for k in range(1, len(etiquettes)):
        if etiquettes[k][0] - etiquettes[k - 1][0] < ecart:
            etiquettes[k][0] = etiquettes[k - 1][0] + ecart
    for y, texte, col, gros in etiquettes:
        ax.annotate(texte, (xs[-1] + 0.06, y), fontsize=8.5 if gros else 7.5, color=col,
                    fontweight="bold" if gros else "normal", va="center",
                    annotation_clip=False)

    style(ax, axe_grille="y")
    ax.set_xticks(xs)
    ax.set_xticklabels(ETIQUETTES, fontsize=9)
    ax.set_xlim(-0.25, 2.68)
    ax.set_ylim(-0.03, 0.74)
    ax.set_ylabel("rappel des cellules minoritaires", fontsize=9.5, color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=11.5, color=ENCRE, loc="left", pad=16)
    ax.annotate(sous_titre, (0, 1.012), xycoords="axes fraction", fontsize=8.5,
                color=ENCRE_SECONDE, va="bottom")


def main():
    mes = pd.read_csv(os.path.join(SORTIE, "a34-par-tercile.csv"))
    desc = pd.read_csv(os.path.join(SORTIE, "a34-terciles-description.csv"))

    fig, axes = plt.subplots(1, 3, figsize=(18.5, 6.4), facecolor=FOND)
    panneau(axes[0], mes, desc, 1052, "D_seg segment",
            "1. Partition principale : la modalite est elle frequente\n"
            "dans le segment ideologie x genre x age de la personne ?",
            "perimetre 1 052, seuil 10 %, 5 114 cellules minoritaires classees sur 5 709",
            avec_c2c3=False)
    panneau(axes[1], mes, desc, 1052, "D_logit regression",
            "2. Partition secondaire : probabilite hors pli que la regression\n"
            "logistique sur demographies attribue cette modalite",
            "perimetre 1 052, seuil 10 %. B1 est a zero sur T1 et T2 PAR ARITHMETIQUE : "
            "la partition est sa propre confiance",
            avec_c2c3=False)
    panneau(axes[2], mes, desc, 150, "D_seg segment",
            "3. Partition principale, perimetre du run local,\n"
            "avec C2 (etiquette) et C3 (sans etiquette)",
            "perimetre 150, seuil 10 %, 651 cellules minoritaires classees sur 747",
            avec_c2c3=True)

    fig.suptitle("Le rappel des reponses rares monte avec la deductibilite pour toutes "
                 "les methodes, et le plancher de bruit monte plus vite",
                 fontsize=13.5, color=ENCRE, x=0.012, ha="left", y=1.005)
    fig.text(0.012, -0.035,
             "Lecture : dans le tercile non deductible, ou aucune autre personne du "
             "segment de l'individu n'a donne cette reponse, les agents riches en "
             "retrouvent 20 a 22 pour cent\net la regression logistique 1,5 pour cent, "
             "sous le plancher d'un tirage aveugle dans la marginale de l'item. "
             "a34, 8 septembre 2026, zero appel de modele de langage.",
             fontsize=8.5, color=ENCRE_SECONDE, ha="left", va="top")
    fig.tight_layout()

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a34-figure-rarete-deductible.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print(f"ecrit : {chemin}")


if __name__ == "__main__":
    main()
