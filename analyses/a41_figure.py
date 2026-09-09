"""
a41_figure : le plan exactitude contre ratio intra en regime severe, et la comparaison honnete.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit
`resultats/a41-tableau-quatre-cases.csv` et `a41-condition-appariee.csv` ecrits par
a41_regime_severe.py, pour que la figure et les chiffres du rapport ne puissent pas
diverger. Aucun script existant n'est modifie. Le fond, l'encre, la grille et la couleur
des humains sont ceux de a28_figures, importes tels quels ; les deux teintes d'imputation
sont celles de a35_figure, importees de la meme facon.

Ce que la figure montre.

Panneau gauche, le plan demande. L'abscisse est l'exactitude individuelle sur les 58 items
de famille, l'ordonnee le ratio de dispersion INTRA groupe rapporte aux memes humains. Un
ratio de 1 veut dire que la methode laisse les gens d'un meme segment ideologique aussi
differents qu'ils le sont vraiment. La FORME du point porte l'information que ce rapport
existe pour porter : un rond plein est une methode dont la famille thematique a ete retiree
du contexte, un carre vide est la meme methode avec le decoupage aleatoire de a2, un
triangle est une methode qui ne voit aucun item et pour qui le regime n'a pas de sens. Les
six conditions de Stanford sont des ronds pleins ROUGES bordes de tirets : elles sont
tracees dans ce plan sans avoir subi le retrait, parce que leurs agents gardent les items
cousins dans leur invite, et c'est exactement ce que la figure doit laisser voir.

Panneau droit, la comparaison honnete. Pour chaque couple (condition riche de Stanford,
methode statistique du regime severe), l'ecart d'exactitude mesure tel quel, puis le meme
ecart apres le decalage de la condition appariee que le papier de Stanford publie lui meme,
0,05 de score normalise entre le retrait du seul item predit et le retrait du bloc entier.
La barre est l'intervalle bootstrap sur les 1 052 personnes ; le decalage est une
translation deterministe et non une mesure, ce que le titre du panneau dit.

Entree  : resultats/a41-tableau-quatre-cases.csv, a41-condition-appariee.csv
Sortie  : resultats/a41-figure-regime-severe.png et .svg

Usage : .venv/bin/python analyses/a41_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import ENCRE, ENCRE_SECONDE, FOND, HUMAIN, LANGAGE, NEUTRE, style
from a35_figure import ESPERANCE, TIRAGE

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

COURT = {
    "humains vague 2": "humains vague 2",
    "agents composite": "composite", "agents entretien (v3)": "entretien",
    "agents enquete": "enquete", "agents demographiques (v6)": "demo v6",
    "agents v7": "v7", "agents v8": "v8",
    "E1 famille retiree (argmax)": "E1 fam. retiree",
    "E2 famille retiree (tirage)": "E2 fam. retiree",
    "PMM k=10 famille retiree": "PMM k=10 fam. retiree",
    "IM m=10 mode, famille retiree": "IM mode fam. retiree",
    "B2 famille retiree (argmax)": "B2 fam. retiree",
    "B2 famille retiree (tirage)": "B2 fam. retiree tirage",
    "B3 foret": "B3 foret", "B1 argmax": "B1 argmax",
    "B0 mode": "B0 mode", "B0 tirage": "B0 tirage",
    "E1 regression contexte argmax": "E1 blocs alea.",
    "E2 regression contexte tirage": "E2 blocs alea.",
    "PMM k=10": "PMM blocs alea.", "IM m=10 mode des m": "IM blocs alea.",
    "B2 argmax": "B2 blocs alea.", "B2 tirage": "B2 tirage blocs alea.",
}

# Decalage manuel des etiquettes, en points. Sans cela une dizaine d'etiquettes se
# recouvrent dans la bande 0,63 a 0,70 d'exactitude, qui est justement la bande ou tout
# se joue.
DECALAGE = {
    "humains vague 2": (-11, 5),
    "agents composite": (8, 5), "agents entretien (v3)": (-9, -11),
    "agents enquete": (-9, 2), "agents demographiques (v6)": (-9, 4),
    "agents v7": (8, -3), "agents v8": (8, -2),
    "E1 famille retiree (argmax)": (-9, -3),
    "E2 famille retiree (tirage)": (-9, 4),
    "PMM k=10 famille retiree": (0, -14),
    "IM m=10 mode, famille retiree": (-9, 5),
    "B2 famille retiree (argmax)": (-9, 3),
    "B2 famille retiree (tirage)": (-9, -12),
    "B3 foret": (8, -3), "B1 argmax": (8, 3),
    "B0 mode": (8, 1), "B0 tirage": (8, 0),
    "E1 regression contexte argmax": (8, -2),
    "E2 regression contexte tirage": (8, 3),
    "PMM k=10": (8, 2), "IM m=10 mode des m": (8, -9),
    "B2 argmax": (8, 2), "B2 tirage": (-9, -12),
}

# Etiquettes courtes du panneau droit : les noms longs debordent sur le panneau gauche.
COURT_DROITE = {
    "agents composite": "composite", "agents enquete": "enquete",
    "agents entretien (v3)": "entretien",
    "E1 famille retiree (argmax)": "E1", "IM m=10 mode, famille retiree": "IM mode",
    "B2 famille retiree (argmax)": "B2", "PMM k=10 famille retiree": "PMM k=10",
}


def apparence(r):
    """Couleur, forme et bord d'un point, selon le regime et le traitement de la famille."""
    if r.methode == "humains vague 2":
        return HUMAIN, "o", 10.0, ENCRE, 1.4
    if r.regime == "modele de langage":
        return LANGAGE, "o", 8.5, ENCRE, 1.2
    if r.famille_retiree.startswith("sans objet"):
        return NEUTRE, "^", 8.0, "none", 0.0
    couleur = ESPERANCE if r.regime == "esperance" else TIRAGE
    if r.famille_retiree == "oui":
        return couleur, "o", 8.5, "none", 0.0
    return couleur, "s", 7.0, couleur, 1.1


def main():
    d = pd.read_csv(os.path.join(SORTIE, "a41-tableau-quatre-cases.csv"))
    ap = pd.read_csv(os.path.join(SORTIE, "a41-condition-appariee.csv"))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16.2, 8.0),
                                   gridspec_kw={"width_ratios": [1.42, 1.0]})
    fig.patch.set_facecolor(FOND)

    # ------------------------------------------------ panneau gauche : le plan demande
    style(ax1, axe_grille="both")
    plafond = float(d.loc[d.methode == "humains vague 2", "exactitude"].iloc[0])
    ax1.axhline(1.0, color=HUMAIN, linewidth=1.1, linestyle="--", zorder=1)
    ax1.axvline(plafond, color=HUMAIN, linewidth=1.1, linestyle="--", zorder=1)
    ax1.text(0.818, 0.996, "dispersion intra humaine", fontsize=7.6, color=HUMAIN,
             ha="right", va="top", zorder=2)
    ax1.text(plafond - 0.004, 0.045, "plafond humain", fontsize=7.6, color=HUMAIN,
             ha="right", va="bottom", rotation=90, zorder=2)

    for _, r in d.iterrows():
        if not np.isfinite(r.exactitude) or not np.isfinite(r.ratio_intra_ideologie):
            continue
        c, forme, taille, bord, lw = apparence(r)
        ax1.errorbar([r.exactitude], [r.ratio_intra_ideologie],
                     xerr=[[r.exactitude - r.exactitude_ic_bas],
                           [r.exactitude_ic_haut - r.exactitude]],
                     yerr=[[max(r.ratio_intra_ideologie - r.ratio_intra_ic_bas, 0)],
                           [max(r.ratio_intra_ic_haut - r.ratio_intra_ideologie, 0)]],
                     fmt="none", ecolor=c, elinewidth=0.9, alpha=0.55, zorder=3)
        ax1.plot([r.exactitude], [r.ratio_intra_ideologie], forme, color=c,
                 markersize=taille, markeredgecolor=bord, markeredgewidth=lw,
                 alpha=0.94, zorder=4)
        dx, dy = DECALAGE.get(r.methode, (8, 3))
        gras = r.methode in ("agents composite", "humains vague 2",
                             "E1 famille retiree (argmax)")
        ax1.annotate(COURT.get(r.methode, r.methode),
                     (r.exactitude, r.ratio_intra_ideologie),
                     textcoords="offset points", xytext=(dx, dy),
                     fontsize=8.3 if gras else 7.7,
                     color=ENCRE if gras else ENCRE_SECONDE,
                     fontweight="bold" if gras else "normal",
                     ha="right" if dx < 0 else "left", zorder=5)

    ax1.set_xlim(0.495, 0.822)
    ax1.set_ylim(-0.05, 1.20)
    ax1.set_xlabel("exactitude individuelle, 58 items de famille, egalite exacte",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax1.set_ylabel("ratio de dispersion intra groupe, methode sur humains",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax1.set_title("Le plan du regime severe. Rond plein : famille retiree du contexte. "
                  "Carre : blocs aleatoires",
                  fontsize=10.4, color=ENCRE, loc="left")

    ax1.plot([], [], "o", color=LANGAGE, markersize=8, markeredgecolor=ENCRE,
             markeredgewidth=1.2,
             label="Stanford, cousins gardes dans l'invite")
    ax1.plot([], [], "o", color=ESPERANCE, markersize=8,
             label="imputation par esperance, famille retiree")
    ax1.plot([], [], "o", color=TIRAGE, markersize=8,
             label="imputation par tirage, famille retiree")
    ax1.plot([], [], "s", color="none", markeredgecolor=ESPERANCE, markeredgewidth=1.1,
             markersize=7, label="la meme, blocs aleatoires de a2")
    ax1.plot([], [], "^", color=NEUTRE, markersize=8,
             label="ne voit aucun item, regime sans objet")
    ax1.plot([], [], "o", color=HUMAIN, markersize=8, markeredgecolor=ENCRE,
             markeredgewidth=1.4, label="memes humains reinterroges")
    ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.095), fontsize=8.2,
               frameon=False, labelcolor=ENCRE_SECONDE, ncol=3, handletextpad=0.4,
               columnspacing=1.4)

    # ------------------------------------- panneau droit : la comparaison appariee
    style(ax2, axe_grille="x")
    conds = ["agents composite", "agents enquete", "agents entretien (v3)"]
    refs = ["E1 famille retiree (argmax)", "IM m=10 mode, famille retiree",
            "B2 famille retiree (argmax)", "PMM k=10 famille retiree"]
    d0 = ap[ap.decalage_applique == 0.0]
    dap = ap[ap.est_le_decalage_de_a8]
    decal = float(dap.decalage_applique.iloc[0])

    etiquettes, y = [], 0
    ax2.axvline(0.0, color=ENCRE_SECONDE, linewidth=1.1, zorder=1)
    for cond in conds:
        for ref in refs:
            a = d0[(d0.condition == cond) & (d0.reference == ref)].iloc[0]
            b = dap[(dap.condition == cond) & (dap.reference == ref)].iloc[0]
            ax2.plot([a.ic_bas, a.ic_haut], [y, y], color=LANGAGE, linewidth=1.6,
                     alpha=0.45, zorder=2)
            ax2.plot([b.ic_bas, b.ic_haut], [y, y], color=ENCRE_SECONDE, linewidth=1.6,
                     alpha=0.45, zorder=2)
            ax2.plot([a.difference], [y], "o", color=LANGAGE, markersize=7.5, zorder=4)
            ax2.plot([b.difference], [y], "D", color=ENCRE_SECONDE, markersize=6.0,
                     zorder=4)
            ax2.annotate("", xy=(b.difference, y), xytext=(a.difference, y),
                         arrowprops=dict(arrowstyle="->", color=ENCRE_SECONDE,
                                         linewidth=0.9, alpha=0.7), zorder=3)
            etiquettes.append(f"{COURT_DROITE[cond]} contre {COURT_DROITE[ref]}")
            y += 1
        y += 0.6

    ax2.set_yticks([i + (i // len(refs)) * 0.6 for i in range(len(etiquettes))])
    ax2.set_yticklabels(etiquettes, fontsize=8.2, color=ENCRE_SECONDE)
    ax2.invert_yaxis()
    ax2.set_xlabel("ecart d'exactitude, condition de Stanford moins methode statistique",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax2.set_title("La comparaison appariee. Le losange retranche "
                  f"{decal * 100:.2f} point (a8 errata E1)",
                  fontsize=10.4, color=ENCRE, loc="left")
    ax2.plot([], [], "o", color=LANGAGE, markersize=7.5,
             label="ecart mesure, cousins gardes par l'agent")
    ax2.plot([], [], "D", color=ENCRE_SECONDE, markersize=6.0,
             label=f"ecart apres le decalage apparie, moins {decal * 100:.2f} point")
    ax2.legend(loc="upper center", bbox_to_anchor=(0.5, -0.095), fontsize=8.2,
               frameon=False, labelcolor=ENCRE_SECONDE, ncol=1)

    fig.suptitle("a41. Le regime severe, avec des intervalles : la famille thematique "
                 "entiere hors du contexte, 58 items, 1 052 personnes",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left", y=0.985)
    fig.text(0.012, 0.928,
             "Segmentation : ideologie politique. Dispersion : indice de Gini Simpson, "
             "estimateur sans biais de a1. Barres : bootstrap apparie sur les personnes, "
             "2 000 tirages. Les six conditions de Stanford ne sont PAS dans le regime "
             "severe : leurs agents gardent les items cousins de la question dans leur "
             "invite, ce que le papier declare et que nous ne pouvons pas defaire.",
             fontsize=8.5, color=ENCRE_SECONDE, ha="left")
    fig.subplots_adjust(top=0.870, bottom=0.150, wspace=0.42)

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a41-figure-regime-severe.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
