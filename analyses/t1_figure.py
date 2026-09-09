"""
t1_figure : la mesure de personne sur Twin-2K-500, deux panneaux.

Ne recalcule rien. Lit resultats/t1-chute-segmentations.csv et
resultats/t1-generateur-nul.csv, pour que la figure et les chiffres du rapport ne puissent
pas diverger. La palette et les conventions de trace viennent de a28_figures, importees
telles quelles. Aucun script existant modifie, aucun appel de modele.

Panneau A. La chute d'exactitude sous permutation des personnes intra segment, en part du
plancher humain, sous les deux segmentations qui commandent la lecture : `S_ideo`, qui
contient l'ideologie, et `S_gra`, genre x ethnicite x age, qui ne la contient pas. Deux
points relies par condition. Un trait long veut dire que le chiffre depend de ce qu'on met
dans le segment, ce qui est le resultat de a47 sur le GSS.

Panneau B. Le ratio inter de l'axe ideologie, valeur mesuree contre valeur de son
generateur nul, echelle logarithmique. Un trait invisible veut dire que le nul reproduit le
chiffre, donc que le chiffre ne porte aucune structure individuelle.

Sortie : resultats/t1-figure-personne-twin.png et .svg
Usage  : .venv/bin/python analyses/t1_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt          # noqa: E402
import numpy as np                       # noqa: E402
import pandas as pd                      # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import (ENCRE, ENCRE_SECONDE, FOND, GRILLE, HUMAIN,   # noqa: E402
                         LANGAGE, NEUTRE, STATISTIQUE, style)
import t1_commun as C                    # noqa: E402

HUMAINS = {C.PLANCHER}
STATS = set(C.STATISTIQUES)


def couleur(nom):
    if nom in HUMAINS:
        return HUMAIN
    if nom in STATS:
        return STATISTIQUE
    return LANGAGE


def main():
    ch = pd.read_csv(os.path.join(C.SORTIE, "t1-chute-segmentations.csv"))
    nul = pd.read_csv(os.path.join(C.SORTIE, "t1-generateur-nul.csv"))
    nul = nul[nul["terme"] == "inter"].set_index("condition")

    a = ch[ch["segmentation"] == "S_gra"].set_index("condition")
    b = ch[ch["segmentation"] == "S_ideo"].set_index("condition")
    ordre = list(a.sort_values("part_du_plancher_humain").index)

    fig, axes = plt.subplots(1, 3, figsize=(16.4, 7.6),
                             gridspec_kw={"width_ratios": [1.15, 0.95, 0.95]})
    fig.patch.set_facecolor(FOND)

    ax = axes[0]
    for i, c in enumerate(ordre):
        x1 = float(a.loc[c, "part_du_plancher_humain"])
        x2 = float(b.loc[c, "part_du_plancher_humain"])
        col = couleur(c)
        ax.plot([x2, x1], [i, i], color=col, linewidth=1.6, alpha=0.45, zorder=2)
        ax.scatter([x2], [i], s=42, facecolor="white", edgecolor=NEUTRE,
                   linewidth=1.4, zorder=3)
        ax.scatter([x1], [i], s=46, color=col, zorder=4)
    ax.axvline(C.SEUIL_GABARIT, color=GRILLE, linewidth=1.2, zorder=0)
    ax.axvline(C.SEUIL_PERSONNE, color=GRILLE, linewidth=1.2, zorder=0)
    ax.axvline(0.0, color=GRILLE, linewidth=1.0, zorder=0)
    ax.set_yticks(range(len(ordre)))
    ax.set_yticklabels([C.ETIQUETTE.get(c, c) for c in ordre], fontsize=9, color=ENCRE)
    ax.set_ylim(-0.7, len(ordre) - 0.3)
    ax.set_title("A. Chute sous permutation des personnes intra segment,\n"
                 "en part du plancher humain", fontsize=11, color=ENCRE, loc="left",
                 pad=12)
    ax.set_xlabel("plein : genre x ethnicite x age ; cercle : ideologie seule",
                  fontsize=8.5, color=ENCRE_SECONDE)
    style(ax)

    ax = axes[1]
    for i, c in enumerate(ordre):
        if c not in nul.index or c in ("B0 mode", "B0 tirage"):
            continue    # leur ratio vrai est nul par construction, la ligne n'apprend rien
        r = float(nul.loc[c, "ratio_mesure"])
        n = float(nul.loc[c, "ratio_nul_moyen"])
        bas, haut = float(nul.loc[c, "nul_bas"]), float(nul.loc[c, "nul_haut"])
        col = couleur(c)
        ax.plot([n, r], [i, i], color=col, linewidth=1.6, alpha=0.45, zorder=2)
        ax.plot([bas, haut], [i, i], color=NEUTRE, linewidth=4.0, alpha=0.30, zorder=1)
        ax.scatter([n], [i], s=42, facecolor="white", edgecolor=NEUTRE,
                   linewidth=1.4, zorder=3)
        ax.scatter([r], [i], s=46, color=col, zorder=4)
    ax.axvline(1.0, color=GRILLE, linewidth=1.0, zorder=0)
    ax.set_yticks(range(len(ordre)))
    ax.set_yticklabels([])
    ax.set_ylim(-0.7, len(ordre) - 0.3)
    ax.set_xscale("log")
    ax.set_title("B. Ratio inter sur l'axe ideologie,\n"
                 "mesure contre son generateur nul", fontsize=11, color=ENCRE,
                 loc="left", pad=12)
    ax.set_xlabel("plein : la population ; cercle : son nul ; barre : 200 replicats",
                  fontsize=8.5, color=ENCRE_SECONDE)
    ax.set_xticks([0.3, 0.5, 1.0, 2.0, 3.0, 5.0])
    ax.get_xaxis().set_major_formatter(matplotlib.ticker.ScalarFormatter())
    ax.get_xaxis().set_minor_formatter(matplotlib.ticker.NullFormatter())
    style(ax)

    # Panneau C : le facteur de changement entre les deux segmentations, sur les deux
    # jeux. C'est le resultat que a45 point 10 demandait : le chiffre depend il du jeu ?
    ax = axes[2]
    gss = pd.read_csv(os.path.join(C.SORTIE, "a47-chute-deux-segmentations.csv"))
    gp = gss.pivot_table(index="condition", columns="segmentation",
                         values="part_du_plancher_humain")
    gp = gp[gp["S_ideo"].abs() > 0.02]
    gf = (gp["S_gra"] / gp["S_ideo"]).sort_values()
    tf = (a["part_du_plancher_humain"] / b["part_du_plancher_humain"])
    tf = tf[b["part_du_plancher_humain"].abs() > 0.02].sort_values()
    for i, (nom, v) in enumerate(gf.items()):
        gras = nom in ("agents v8", "C2")
        ax.scatter([v], [i], s=52 if gras else 34,
                   color=ENCRE if gras else NEUTRE, zorder=3)
        ax.text(v + 0.06, i, nom, fontsize=7.5, va="center",
                color=ENCRE if gras else ENCRE_SECONDE)
    dec = len(gf) + 1.4
    for i, (nom, v) in enumerate(tf.items()):
        ax.scatter([v], [dec + i], s=34, color=couleur(nom), zorder=3)
        ax.text(v + 0.06, dec + i, C.ETIQUETTE.get(nom, nom), fontsize=7.5,
                va="center", color=ENCRE_SECONDE)
    ax.axvline(1.0, color=GRILLE, linewidth=1.2, zorder=0)
    ax.axhline(len(gf) + 0.2, color=GRILLE, linewidth=1.0, zorder=0)
    ax.set_yticks([len(gf) / 2, dec + len(tf) / 2])
    ax.set_yticklabels(["GSS, a47", "Twin, t1"], fontsize=10, color=ENCRE)
    ax.set_xlim(0.3, 4.6)
    ax.set_ylim(-1.0, dec + len(tf))
    ax.set_title("C. Facteur de changement de la chute\n"
                 "quand on retire l'ideologie du segment", fontsize=11, color=ENCRE,
                 loc="left", pad=12)
    ax.set_xlabel("part sous genre x ethnicite x age, divisee par la part "
                  "sous ideologie", fontsize=8.5, color=ENCRE_SECONDE)
    style(ax)

    legende = [
        plt.Line2D([], [], marker="o", linestyle="", color=LANGAGE,
                   label="configuration a modele de langage"),
        plt.Line2D([], [], marker="o", linestyle="", color=STATISTIQUE,
                   label="predicteur statistique ou temoin"),
        plt.Line2D([], [], marker="o", linestyle="", color=HUMAIN,
                   label="retest humain, plancher"),
    ]
    fig.legend(handles=legende, loc="lower center", ncol=3, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, 0.005))
    fig.suptitle("t1. La mesure de personne sur Twin-2K-500, 2 058 personnes, "
                 "108 items, treize configurations",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left", y=0.985)
    fig.tight_layout(rect=[0, 0.045, 1, 0.955])
    for ext in ("png", "svg"):
        chemin = os.path.join(C.SORTIE, f"t1-figure-personne-twin.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND)
        print(f"ecrit {chemin}")


if __name__ == "__main__":
    main()
