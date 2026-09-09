"""
i1_figure : la figure d'I1 jour 1, quatre panneaux.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit
les tableaux ecrits par i1_changement.py, i1_previsibilite.py et i1_profils.py, pour que
la figure et les chiffres du rapport ne puissent pas diverger. Aucun script existant
n'est modifie. La palette et les conventions de trace sont celles de a28_figures,
importees telles quelles.

  A  Le plancher de bruit. Taux de changement a quatre ans contre taux de changement a
     deux semaines chez Stanford, un point par item. Au dessus de la diagonale, le delai
     ajoute du changement ; sur la diagonale, tout le changement est deja du bruit de
     retest.

  B  Le changement monotone contre la derive agregee. Un point par item : en abscisse la
     derive nette de l'item dans la fenetre, en ordonnee la part du changement qui va
     dans le sens de cette derive. Les croix grises sont le nul avec derive, qui conserve
     les deux marginales et le taux de changement et detruit le lien entre qui part et ou
     il va.

  C  La previsibilite. Pour chaque predicteur et chaque temoin, l'AUC observee et l'AUC
     apres permutation des personnes a l'interieur du segment. La longueur du trait est
     la quantite de verdict.

  D  Qui bouge. Taux de changement selon la position initiale et selon la distance au
     patron modal du segment.

Entrees : resultats/i1-changement-par-item.csv, i1-auc-synthese.csv,
          i1-position-initiale.csv, i1-deciles-cross-pression.csv
Sorties : resultats/i1-figure-qui-bouge.png et .svg

Usage : .venv/bin/python analyses/i1_figure.py
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

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

ORDRE = ["F foret", "L1 logistique resumee", "L2 logistique complete",
         "V voisins k=25", "P position initiale seule", "T1 temoin de segment",
         "T0 nul avec derive", "T0b nul a taux commun"]
COURT = {"F foret": "F, foret", "L1 logistique resumee": "L1, logistique resumee",
         "L2 logistique complete": "L2, logistique complete (primaire)",
         "V voisins k=25": "V, voisins k=25",
         "T1 temoin de segment": "T1, temoin de segment",
         "T0 nul avec derive": "T0, nul avec derive",
         "P position initiale seule": "P, position initiale seule",
         "T0b nul a taux commun": "T0b, nul a taux commun"}


def lire(nom):
    return pd.read_csv(os.path.join(SORTIE, nom))


def panneau_a(ax, ch):
    d = ch[ch["perimetre"] == "4 ans"].dropna(subset=["taux_changement_2sem"])
    ax.plot([0, 0.9], [0, 0.9], color=ENCRE_SECONDE, linewidth=1.0, linestyle="--",
            zorder=1, label="egalite, tout le changement est du bruit de retest")
    ax.scatter(d["taux_changement_2sem"], d["taux_changement"], s=16, alpha=0.75,
               color=STATISTIQUE, edgecolor="none", zorder=3)
    ax.set_xlabel("taux de changement a deux semaines, Stanford", fontsize=9)
    ax.set_ylabel("taux de changement a quatre ans, panels GSS", fontsize=9)
    ax.set_xlim(0, 0.9)
    ax.set_ylim(0, 0.9)
    part = float((d["taux_changement"] > d["taux_changement_2sem"]).mean())
    ax.set_title(f"A. Le plancher de bruit\n{len(d)} items, {100 * part:.0f} pour cent "
                 "au dessus de la diagonale", fontsize=10, color=ENCRE, loc="left")
    ax.legend(fontsize=7.5, frameon=False, loc="upper left")
    style(ax, axe_grille="both")


def panneau_b(ax, ch):
    d = ch[ch["perimetre"] == "4 ans"]
    ax.scatter(d["derive_nette_tv"], d["nul_part_monotone"], s=26, marker="x",
               color=NEUTRE, linewidths=0.9, zorder=2,
               label="nul avec derive, destinations remelangees")
    ax.scatter(d["derive_nette_tv"], d["part_monotone_du_changement"], s=16,
               color=LANGAGE, edgecolor="none", alpha=0.85, zorder=3,
               label="observe")
    ax.axhline(1 / 3, color=ENCRE_SECONDE, linewidth=0.9, linestyle=":",
               zorder=1)
    ax.text(0.176, 1 / 3 + 0.012, "un tiers", fontsize=7.5, color=ENCRE_SECONDE)
    ax.set_xlabel("derive nette de l'item dans la fenetre, distance en variation totale",
                  fontsize=9)
    ax.set_ylabel("part du changement qui va dans le sens de la derive", fontsize=9)
    ax.set_title("B. Le changement monotone est ce que la derive impose\n"
                 "un point par item, perimetre a quatre ans",
                 fontsize=10, color=ENCRE, loc="left")
    ax.legend(fontsize=7.5, frameon=False, loc="lower right")
    style(ax, axe_grille="both")


def panneau_c(ax, syn):
    s = syn.set_index("predicteur")
    y = np.arange(len(ORDRE))[::-1]
    for k, nom in enumerate(ORDRE):
        if nom not in s.index:
            continue
        r = s.loc[nom]
        c = HUMAIN if nom.startswith(("L", "V", "F")) else (
            STATISTIQUE if nom.startswith("P") else NEUTRE)
        ax.plot([r["auc_permutee_moyenne"], r["auc_moyenne_ponderee"]], [y[k], y[k]],
                color=c, linewidth=2.4, solid_capstyle="round", zorder=3)
        ax.scatter([r["auc_permutee_moyenne"]], [y[k]], s=34, facecolor=FOND,
                   edgecolor=c, linewidth=1.4, zorder=4)
        ax.scatter([r["auc_moyenne_ponderee"]], [y[k]], s=34, color=c, zorder=4)
        ax.plot([r["auc_ic_bas"], r["auc_ic_haut"]], [y[k] - 0.26, y[k] - 0.26],
                color=c, linewidth=1.0, alpha=0.6, zorder=2)
    ax.axvline(0.5, color=ENCRE_SECONDE, linewidth=0.9, linestyle="--", zorder=1)
    ax.set_yticks(y)
    ax.set_yticklabels([COURT.get(n, n) for n in ORDRE], fontsize=8.5)
    ax.set_xlabel("AUC moyenne ponderee sur les items, cible : changement a quatre ans",
                  fontsize=9)
    ax.set_title("C. AUC observee (plein) et apres permutation des personnes\n"
                 "dans le segment (creux) ; le trait est la chute",
                 fontsize=10, color=ENCRE, loc="left")
    style(ax, axe_grille="x")


def panneau_d(ax, pos, dec):
    d = dec[dec["variable"] == "distance au patron modal du segment"]
    ax.plot(d["decile"], d["taux_changement"], marker="o", markersize=4,
            color=STATISTIQUE, linewidth=1.6, label="changement brut")
    ax.plot(d["decile"], d["taux_monotone"], marker="o", markersize=4,
            color=LANGAGE, linewidth=1.6, label="changement monotone")
    for etq, couleur, style_trait in (
            ("modalite rare, moins de 10 pour cent", ENCRE, "--"),
            ("modalite majoritaire", ENCRE_SECONDE, ":")):
        e = pos[pos["position_initiale"] == etq]
        if not len(e):
            continue
        w = e["n_porteurs"] + e["n_autres"]
        v = float(np.average(e["taux_changement_porteurs"], weights=w))
        ax.axhline(v, color=couleur, linewidth=1.0, linestyle=style_trait, zorder=1)
        ax.text(5.5, v + 0.008,
                f"changement des porteurs d'une {etq.split(',')[0]} en vague 1, "
                f"{100 * v:.0f} pour cent",
                fontsize=7.5, color=couleur, va="bottom", ha="center")
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("decile de distance au patron modal de son propre segment", fontsize=9)
    ax.set_ylabel("taux de changement", fontsize=9)
    ax.set_xlim(0.6, 10.4)
    ax.set_ylim(0.08, 0.80)
    ax.set_title("D. Qui bouge : l'incoherence initiale et la position initiale",
                 fontsize=10, color=ENCRE, loc="left")
    ax.legend(fontsize=7.5, frameon=False, loc="center left")
    style(ax, axe_grille="y")


def main():
    ch = lire("i1-changement-par-item.csv")
    syn = lire("i1-auc-synthese.csv")
    pos = lire("i1-position-initiale.csv")
    dec = lire("i1-deciles-cross-pression.csv")

    fig, axes = plt.subplots(2, 2, figsize=(13.2, 9.6))
    fig.patch.set_facecolor(FOND)
    panneau_a(axes[0, 0], ch)
    panneau_b(axes[0, 1], ch)
    panneau_c(axes[1, 0], syn)
    panneau_d(axes[1, 1], pos, dec)
    fig.suptitle("I1, jour 1 : qui change d'avis dans les panels GSS, et est ce previsible",
                 fontsize=12.5, color=ENCRE, x=0.008, ha="left", y=0.985)
    fig.text(0.008, 0.012,
             "Quatre panels GSS, 4 683 personnes reinterrogees a quatre ans, 118 items du "
             "noyau commun de a12. Zero appel de modele. Preenregistrement "
             "resultats/i1-preenregistrement.md.",
             fontsize=7.5, color=ENCRE_SECONDE, ha="left")
    fig.tight_layout(rect=[0, 0.028, 1, 0.965])
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"i1-figure-qui-bouge.{ext}")
        fig.savefig(chemin, dpi=190, facecolor=FOND)
        print("ecrit", chemin, flush=True)


if __name__ == "__main__":
    main()
