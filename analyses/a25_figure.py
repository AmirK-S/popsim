"""
a25_figure : ecart moyen aux humains sur les items sensibles au mode contre les temoins.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux de a25_mesures.py et a25_contrastes.py pour que la figure et les chiffres du
rapport ne puissent pas diverger. Aucun script existant n'est modifie.

Entree  : resultats/a25-bootstrap-personnes.csv, resultats/a25-contrastes.csv
Sortie  : resultats/a25-figure-mode.png et .svg

Usage : .venv/bin/python analyses/a25_figure.py [--perimetre 150]
"""

import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

FOND = "#fcfcfb"
ENCRE = "#0b0b0b"
ENCRE_SECONDE = "#52514e"
GRILLE = "#e2e1dd"
SENSIBLE = "#c8412b"
TEMOIN = "#2a78d6"
NEUTRE = "#8d8b86"

# Trois familles de methodes, pour que la lecture ne repose pas sur la couleur seule : le
# libelle porte deja la marque.
FAMILLE = {
    "humains vague 2": "humains",
    "B0 mode": "statistique", "B0 tirage": "statistique",
    "B1 argmax": "statistique", "B2 argmax": "statistique",
}


def famille(nom):
    return FAMILLE.get(nom, "modele de langage")


def style(ax):
    ax.set_facecolor(FOND)
    ax.grid(True, axis="x", color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=9)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perimetre", type=int, default=150)
    args = ap.parse_args()

    boot = pd.read_csv(os.path.join(SORTIE, "a25-bootstrap-personnes.csv"))
    contr = pd.read_csv(os.path.join(SORTIE, "a25-contrastes.csv"))
    boot = boot[(boot.perimetre == args.perimetre) & (boot.metrique == "distance")]
    contr = contr[(contr.perimetre == args.perimetre) & (contr.metrique == "distance")
                  & (contr.groupe == "sensible")]

    diff = contr.set_index("condition")
    ordre = list(diff.sort_values("difference").index)
    g = {c: boot[boot.condition == c].set_index("groupe") for c in ordre}
    y = range(len(ordre))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.4, 6.4),
                                   gridspec_kw={"width_ratios": [1.15, 1]})
    fig.patch.set_facecolor(FOND)

    # --- panneau de gauche : niveau, par groupe d'items
    for i, cond in enumerate(ordre):
        for groupe, couleur in (("temoin", TEMOIN), ("sensible", SENSIBLE)):
            r = g[cond].loc[groupe]
            ax1.plot([r.ic_bas, r.ic_haut], [i, i], color=couleur, linewidth=1.4,
                     solid_capstyle="butt", zorder=2)
            ax1.plot([r.moyenne], [i], "o", color=couleur, markersize=6.5, zorder=3)
        r1, r2 = g[cond].loc["temoin"], g[cond].loc["sensible"]
        ax1.plot([r1.moyenne, r2.moyenne], [i, i], color=GRILLE, linewidth=1.0, zorder=1)
    style(ax1)
    ax1.set_yticks(list(y))
    ax1.set_yticklabels([f"{c}  [{famille(c)[:3]}]" for c in ordre], fontsize=9,
                        color=ENCRE)
    ax1.set_xlabel("ecart de distribution a la population humaine, moyenne par item",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax1.set_title("Niveau de l'ecart, par groupe d'items", fontsize=11, color=ENCRE,
                  loc="left")
    ax1.plot([], [], "o", color=SENSIBLE, label="items sensibles au mode (NORC, 12)")
    ax1.plot([], [], "o", color=TEMOIN, label="temoins negatifs (NORC, 65)")
    ax1.legend(loc="upper center", bbox_to_anchor=(0.5, -0.09), ncol=2,
               fontsize=8.5, frameon=False, labelcolor=ENCRE_SECONDE)

    # --- panneau de droite : la difference, deux intervalles
    for i, cond in enumerate(ordre):
        r = diff.loc[cond]
        p = g[cond].loc["sensible moins temoin"]
        ax2.plot([r.ic_items_bas, r.ic_items_haut], [i, i], color=NEUTRE, linewidth=1.2,
                 zorder=2)
        ax2.plot([p.ic_bas, p.ic_haut], [i, i], color=ENCRE, linewidth=3.0,
                 solid_capstyle="butt", zorder=3)
        ax2.plot([r.difference], [i], "o", color=SENSIBLE if r.difference > 0 else TEMOIN,
                 markersize=6.5, zorder=4)
        ax2.text(0.163, i, f"p = {r.p_permutation:.3f}", fontsize=8,
                 color=ENCRE_SECONDE, va="center")
    ax2.axvline(0, color=ENCRE_SECONDE, linewidth=1.0, zorder=1)
    style(ax2)
    ax2.set_yticks(list(y))
    ax2.set_yticklabels([])
    ax2.set_xlabel("difference sensibles moins temoins", fontsize=9.5, color=ENCRE_SECONDE)
    ax2.set_title("Contraste, intervalle epais sur les personnes,\n"
                  "intervalle fin sur les items ; p par permutation",
                  fontsize=11, color=ENCRE, loc="left")
    ax2.set_xlim(-0.095, 0.205)

    fig.suptitle(f"Items du GSS sensibles au mode de collecte contre temoins negatifs, "
                 f"{args.perimetre} personnes",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.955])
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a25-figure-mode.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
