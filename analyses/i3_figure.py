"""
i3_figure : les trois statistiques non supervisees en fonction du taux de contamination,
par type de population synthetique, avec la reference humaine et sa bande.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par i3_melanges.py, pour que la figure et les chiffres du rapport ne
puissent pas diverger. Aucun script existant n'est modifie. La palette et les conventions
de trace sont celles de a28_figures, importees telles quelles.

Quatre panneaux, la meme liste de sources dans le meme ordre sur les quatre.

  A  deficit de patrons de reponses distincts, relatif au generateur nul du flux lui meme
  B  exces de correlation inter items residualisee sur la demographie
  C  concentration par segment, part du patron modal du segment
  D  I4, l'ecart gauche droite mesure, qui monte avec le gabarit et descend avec le tirage

La bande grise horizontale est l'IC a 95 pour cent de la reference humaine ; une courbe
qui en sort est un flux que le detecteur signale.

Entrees : resultats/i3-melanges.csv, i3-reference-humaine.csv, i3-polarisation.csv
Sorties : resultats/i3-figure-detecteur.png et .svg

Usage : .venv/bin/python analyses/i3_figure.py
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
import i3_commun as I

SORTIE = I.SORTIE

# ordre, couleur et trait de chaque source
TRACE = [
    ("agents v8", LANGAGE, "-", "o", "v8, etiquette ideologique"),
    ("agents demographiques (v6)", LANGAGE, "--", "s", "v6, demographies"),
    ("agents composite", LANGAGE, ":", "^", "composite, riche"),
    ("C2", "#e0714f", "-", "D", "C2, etiquette, local"),
    ("C3", "#e0714f", "--", "v", "C3, sans etiquette, local"),
    ("PMM k=10", STATISTIQUE, "-", "o", "PMM k=10, tirage"),
    ("E2 regression contexte tirage", STATISTIQUE, "--", "s", "E2 regression, tirage"),
    ("IM m=10 mode des m", STATISTIQUE, ":", "^", "IM m=10, mode"),
    ("B0 segment", NEUTRE, "-", "x", "B0 segment, adversaire nul"),
    ("humains vague 2", HUMAIN, "-", "+", "humains vague 2, controle"),
]

PANNEAUX = [
    ("A", "A. Deficit de patrons distincts\nrelatif au nul du flux",
     "deficit relatif"),
    ("B", "B. Exces de correlation inter items\napres retrait du segment",
     "exces de |rho| moyen"),
    ("C", "C. Concentration par segment\npart du patron modal",
     "part"),
    ("polarisation", "D. I4. Ecart gauche droite mesure\n(ecart standardise de rang)",
     "polarisation"),
]


def main():
    mel = pd.read_csv(os.path.join(SORTIE, "i3-melanges.csv"))
    ref = pd.read_csv(os.path.join(SORTIE, "i3-reference-humaine.csv")).set_index(
        "statistique")
    pol = pd.read_csv(os.path.join(SORTIE, "i3-polarisation.csv"))
    pol_ref = pol[pol.source == "humains purs"].iloc[0]

    fig, axes = plt.subplots(2, 2, figsize=(11.6, 8.4))
    fig.patch.set_facecolor(FOND)

    for ax, (cle, titre, ylab) in zip(axes.ravel(), PANNEAUX):
        style(ax, axe_grille="both")
        if cle == "polarisation":
            v0, bas, haut = pol_ref.polarisation, pol_ref.ic_bas, pol_ref.ic_haut
        else:
            v0 = float(ref.loc[cle, "valeur"])
            bas, haut = float(ref.loc[cle, "ic_bas"]), float(ref.loc[cle, "ic_haut"])
        ax.axhspan(bas, haut, color=GRILLE, zorder=1)
        ax.axhline(v0, color=ENCRE_SECONDE, linewidth=1.0, linestyle=(0, (4, 3)),
                   zorder=2)
        for nom, coul, trait, marque, _lib in TRACE:
            d = mel[mel.source == nom]
            if not len(d):
                continue
            taux = sorted(d.taux.unique())
            moy = [float(d[d.taux == t][cle].mean()) for t in taux]
            ax.plot([0.0] + [t * 100 for t in taux], [v0] + moy, trait, color=coul,
                    marker=marque, markersize=4.5, linewidth=1.5, zorder=3)
        ax.set_title(titre, fontsize=10.5, color=ENCRE, loc="left", pad=8)
        ax.set_xlabel("taux de contamination, pour cent", fontsize=9,
                      color=ENCRE_SECONDE)
        ax.set_ylabel(ylab, fontsize=9, color=ENCRE_SECONDE)
        ax.set_xlim(-1.5, 51.5)

    fig.text(0.5, 0.945, "sur chaque panneau, le trait tirete est la valeur de reference "
                         "sur le flux pur humain et la bande grise son IC a 95 pour cent ; "
                         "une courbe qui sort de la bande est un flux signale",
             ha="center", fontsize=8.5, color=ENCRE_SECONDE)

    poignees = [plt.Line2D([], [], color=c, linestyle=t, marker=m, markersize=4.5,
                           linewidth=1.5, label=lib)
                for _n, c, t, m, lib in TRACE]
    fig.legend(handles=poignees, loc="lower center", ncol=5, fontsize=8.5,
               frameon=False, labelcolor=ENCRE_SECONDE, bbox_to_anchor=(0.5, -0.045))
    fig.suptitle("i3. Trois statistiques non supervisees contre le taux de population "
                 "synthetique dans un flux de 1 052 reponses",
                 fontsize=12, color=ENCRE, y=0.985)
    fig.tight_layout(rect=(0, 0.03, 1, 0.935))
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"i3-figure-detecteur.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
