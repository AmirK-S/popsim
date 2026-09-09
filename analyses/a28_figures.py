"""
a28_figures : une figure par test decisif.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par a28_test1_mode.py, a28_test2_ecrasement.py et a28_test3_stereotype.py,
pour que les figures et les chiffres du rapport ne puissent pas diverger. Aucun script
existant n'est modifie. La palette et les conventions de trace sont celles de a25_figure.

Entree  : resultats/a28-t1-contrastes.csv, a28-t1-robustesse.csv,
          a28-t2-selectivite.csv, a28-t2-dispersion-item.csv,
          a28-t3-profil-erreur.csv, a28-t3-minorites.csv
Sortie  : resultats/a28-figure-test1.png et .svg, a28-figure-test2.*, a28-figure-test3.*

Usage : .venv/bin/python analyses/a28_figures.py
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

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

FOND = "#fcfcfb"
ENCRE = "#0b0b0b"
ENCRE_SECONDE = "#52514e"
GRILLE = "#e2e1dd"
LANGAGE = "#c8412b"
STATISTIQUE = "#2a78d6"
HUMAIN = "#1f7a52"
NEUTRE = "#8d8b86"


def couleur(cond):
    if cond == "humains vague 2":
        return HUMAIN
    return LANGAGE if cond in LLM else STATISTIQUE


def style(ax, axe_grille="x"):
    ax.set_facecolor(FOND)
    ax.grid(True, axis=axe_grille, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=9)


def legende(ax):
    ax.plot([], [], "o", color=LANGAGE, label="condition a modele de langage (8)")
    ax.plot([], [], "o", color=STATISTIQUE, label="predicteur statistique (5)")
    ax.plot([], [], "o", color=HUMAIN, label="memes humains reinterroges")
    ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.17), ncol=3, fontsize=8.5,
              frameon=False, labelcolor=ENCRE_SECONDE)


def lire(nom):
    return pd.read_csv(os.path.join(SORTIE, nom))


def enregistrer(fig, nom):
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"{nom}.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 1 : test decisif de l'idee de rang 1
# ---------------------------------------------------------------------------

def figure1():
    c = lire("a28-t1-contrastes.csv")
    c = c[c.perimetre == 150]
    rob = lire("a28-t1-robustesse.csv")

    h1 = c[c.hypothese == "H1 distance"].set_index("condition")
    h2 = c[c.hypothese == "H2 dispersion"].set_index("condition")
    ordre = [m for m in ORDRE_METHODES if m in h1.index][::-1]
    y = np.arange(len(ordre))

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15.2, 6.6),
                                        gridspec_kw={"width_ratios": [1.25, 1, 1]})
    fig.patch.set_facecolor(FOND)

    for ax, tab, titre, xl in (
            (ax1, h1, "H1. Distance a la population humaine",
             "difference sensibles moins temoins"),
            (ax2, h2, "H2. Rapport d'entropie agent sur humain",
             "difference sensibles moins temoins")):
        for i, cond in enumerate(ordre):
            r = tab.loc[cond]
            ax.plot([r.ic_items_bas, r.ic_items_haut], [i, i], color=NEUTRE,
                    linewidth=1.3, zorder=2)
            ax.plot([r.difference], [i], "o", color=couleur(cond), markersize=6.5,
                    zorder=3)
        ax.axvline(0, color=ENCRE_SECONDE, linewidth=1.0, zorder=1)
        style(ax)
        ax.set_yticks(y)
        ax.set_xlabel(xl, fontsize=9.5, color=ENCRE_SECONDE)
        ax.set_title(titre, fontsize=11, color=ENCRE, loc="left")
    ax1.set_yticklabels(ordre, fontsize=9, color=ENCRE)
    ax2.set_yticklabels([])

    # p bruts et p corriges par Holm sur la famille complete de 52 tests
    for i, cond in enumerate(ordre):
        r = h1.loc[cond]
        txt = f"p = {r.p_permutation:.3f}"
        if not np.isnan(r.p_holm_famille_complete):
            txt += f" / Holm {r.p_holm_famille_complete:.2f}"
        ax1.text(0.168, i, txt, fontsize=7.5, color=ENCRE_SECONDE, va="center")
    ax1.set_xlim(-0.055, 0.295)

    # panneau 3 : robustesse au retrait des quatre items nominaux
    r0 = rob[(rob.metrique == "distance") & (rob.retrait == "aucun")]\
        .set_index("condition")
    r4 = rob[(rob.metrique == "distance") & (rob.retrait == "les quatre nominaux")]\
        .set_index("condition")
    for i, cond in enumerate(ordre):
        a, b = r0.loc[cond, "difference"], r4.loc[cond, "difference"]
        ax3.annotate("", xy=(b, i), xytext=(a, i),
                     arrowprops=dict(arrowstyle="->", color=NEUTRE, linewidth=1.2))
        ax3.plot([a], [i], "o", color=couleur(cond), markersize=6.0, zorder=3)
        ax3.plot([b], [i], "s", color=couleur(cond), markersize=5.0, zorder=3,
                 markerfacecolor=FOND)
    ax3.axvline(0, color=ENCRE_SECONDE, linewidth=1.0, zorder=1)
    style(ax3)
    ax3.set_yticks(y)
    ax3.set_yticklabels([])
    ax3.set_xlabel("difference, avant (rond) et apres (carre) retrait",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax3.set_title("Robustesse. Retrait des quatre items nominaux\n"
                  "spkrac, polabuse, polattak, vote16",
                  fontsize=11, color=ENCRE, loc="left")
    legende(ax2)

    fig.suptitle("Test 1. La simulation devie t elle la ou les humains se surveillent ? "
                 "150 personnes, 12 items sensibles contre 65 temoins",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.945])
    enregistrer(fig, "a28-figure-test1")


# ---------------------------------------------------------------------------
# Figure 2 : test decisif de l'idee de rang 2
# ---------------------------------------------------------------------------

def figure2():
    s = lire("a28-t2-selectivite.csv")
    s = s[(s.perimetre == 150) & (s.axe == "profil croise")
          & (s.mesure_x == "part expliquee Gini Simpson")].set_index("condition")
    d = lire("a28-t2-dispersion-item.csv")
    d = d[(d.perimetre == 150) & (d.axe == "profil croise") & d.item_retenu]

    ordre = [m for m in ORDRE_METHODES if m in s.index][::-1]
    y = np.arange(len(ordre))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.6, 6.6),
                                   gridspec_kw={"width_ratios": [1.15, 1]})
    fig.patch.set_facecolor(FOND)

    for i, cond in enumerate(ordre):
        r = s.loc[cond]
        ax1.plot([r.ic_items_bas, r.ic_items_haut], [i, i], color=NEUTRE, linewidth=1.3,
                 zorder=2)
        ax1.plot([r.rho_spearman], [i], "o", color=couleur(cond), markersize=6.5, zorder=3)
        ax1.text(0.665, i, f"p = {r.p_permutation:.3f}", fontsize=7.5,
                 color=ENCRE_SECONDE, va="center")
    ax1.axvline(0, color=ENCRE_SECONDE, linewidth=1.0, zorder=1)
    style(ax1)
    ax1.set_yticks(y)
    ax1.set_yticklabels(ordre, fontsize=9, color=ENCRE)
    ax1.set_xlim(-0.28, 0.95)
    ax1.set_xlabel("correlation de rang entre le rapport de dispersion intra par item\n"
                   "et la part de variance humaine expliquee par la segmentation",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax1.set_title("Selectivite de l'ecrasement.\n"
                  "La these predit du positif a gauche en rouge, du nul en bleu",
                  fontsize=11, color=ENCRE, loc="left")

    donnees = [d[d.condition == c].ratio_intra.dropna().values for c in ordre]
    bp = ax2.boxplot(donnees, orientation="horizontal", widths=0.62, showfliers=False,
                     patch_artist=True, medianprops=dict(color=ENCRE, linewidth=1.4))
    for cond, boite in zip(ordre, bp["boxes"]):
        boite.set_facecolor(couleur(cond))
        boite.set_alpha(0.28)
        boite.set_edgecolor(couleur(cond))
    for element in ("whiskers", "caps"):
        for trait in bp[element]:
            trait.set_color(NEUTRE)
    ax2.axvline(1.0, color=ENCRE_SECONDE, linewidth=1.0, linestyle=(0, (4, 3)), zorder=1)
    style(ax2)
    ax2.set_yticks(np.arange(1, len(ordre) + 1))
    ax2.set_yticklabels([])
    ax2.set_xlabel("rapport de dispersion intra groupe, methode sur humains, par item",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax2.set_title("Uniformite de l'ecrasement.\n"
                  "Une boite etroite est un ecrasement uniforme",
                  fontsize=11, color=ENCRE, loc="left")
    legende(ax2)

    fig.suptitle("Test 2. L'ecrasement est il uniforme ou selectif ? "
                 "Gini Simpson intra, profil croise genre x race x ideologie, 150 personnes",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.945])
    enregistrer(fig, "a28-figure-test2")


# ---------------------------------------------------------------------------
# Figure 3 : test decisif de l'idee de rang 3
# ---------------------------------------------------------------------------

def figure3():
    p = lire("a28-t3-profil-erreur.csv")
    p150 = p[(p.perimetre == 150) & (p.axe == "political_ideology")].set_index("condition")
    m = lire("a28-t3-minorites.csv")
    m = m[(m.perimetre == 150) & (m.seuil == 0.10)].set_index("condition")

    ordre = [c for c in ORDRE_METHODES if c in p150.index][::-1]
    y = np.arange(len(ordre))
    plancher = p150.loc["humains vague 2", "part_stereotype"]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13.6, 6.6),
                                   gridspec_kw={"width_ratios": [1.2, 1]})
    fig.patch.set_facecolor(FOND)

    ax1.axvspan(p150.loc["humains vague 2", "ic_bas"],
                p150.loc["humains vague 2", "ic_haut"],
                color=HUMAIN, alpha=0.10, zorder=0)
    ax1.axvline(plancher, color=HUMAIN, linewidth=1.2, linestyle=(0, (4, 3)), zorder=1)
    ax1.axvline(0.5, color=ENCRE_SECONDE, linewidth=0.9, zorder=1)
    for i, cond in enumerate(ordre):
        r = p150.loc[cond]
        ax1.plot([r.ic_bas, r.ic_haut], [i, i], color=NEUTRE, linewidth=1.3, zorder=2)
        ax1.plot([r.part_stereotype], [i], "o", color=couleur(cond), markersize=6.5,
                 zorder=3)
        ax1.text(0.80, i, f"n = {int(r.erreurs_vers_stereotype + r.erreurs_vers_moyenne)}",
                 fontsize=7.5, color=ENCRE_SECONDE, va="center")
    style(ax1)
    ax1.set_yticks(y)
    ax1.set_yticklabels(ordre, fontsize=9, color=ENCRE)
    ax1.set_xlim(0.0, 0.90)
    ax1.set_xlabel("part des erreurs qui vont vers la modalite majoritaire du segment,\n"
                   "le reste allant vers la modalite majoritaire de la population",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax1.set_title("Profil d'erreur, axe ideologie politique.\n"
                  "Trait vert : les memes humains reinterroges",
                  fontsize=11, color=ENCRE, loc="left")

    for i, cond in enumerate(ordre):
        v = m.loc[cond, "rappel_minoritaire"]
        ax2.barh(i, v, height=0.62, color=couleur(cond), alpha=0.75, zorder=2)
    ax2.axvline(m.loc["humains vague 2", "rappel_minoritaire"], color=HUMAIN,
                linewidth=1.2, linestyle=(0, (4, 3)), zorder=3)
    style(ax2)
    ax2.set_yticks(y)
    ax2.set_yticklabels([])
    ax2.set_xlabel("rappel des cellules dont la vraie reponse est choisie par moins\n"
                   "de 10 pour cent des repondants de l'item",
                   fontsize=9.5, color=ENCRE_SECONDE)
    ax2.set_title("Ce qui est efface : la part minoritaire.\n"
                  "Definition de a8 section 6, memes lignes",
                  fontsize=11, color=ENCRE, loc="left")
    legende(ax2)

    fig.suptitle("Test 3. Le modele se trompe t il vers la moyenne ou vers le stereotype ? "
                 "150 personnes, cellules ou les deux modalites different",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left")
    fig.tight_layout(rect=[0, 0, 1, 0.945])
    enregistrer(fig, "a28-figure-test3")


if __name__ == "__main__":
    figure1()
    figure2()
    figure3()
