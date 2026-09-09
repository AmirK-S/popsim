"""
a33_figure : ce que change l'amputation du contexte, C3F contre C3.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par a33_contexte_rarete.py, pour que la figure et les chiffres du rapport
ne puissent pas diverger. Aucun script existant n'est modifie. La palette et les
conventions de trace sont celles de a25_figure, a28_figures, a29_figure et a31_figure,
importees telles quelles.

Quatre panneaux.

  1. L'exactitude famille par famille, C3 contre C3F, sur les memes 60 personnes et les
     memes cellules. La fleche va du contexte complet au contexte ampute.
  2. Les sept contrastes declares C3F moins C3, plus les deux descriptions post hoc, avec
     leur intervalle bootstrap sur les personnes. La ligne verticale est zero.
  3. Le depart entre H1 et H2 : lift du cote de la personne en abscisse contre lift du
     cote du groupe en ordonnee, avec les deux intervalles bootstrap. La diagonale est le
     lieu du rapport egal a 1. Les intervalles disent d'un coup d'oeil que sur 60
     personnes le rapport n'est pas identifiable.
  4. Le taux de fausses raretes par quintile de rarete du contexte REELLEMENT VU par
     chaque condition, hors du bloc secret pour C3, hors de la famille pour C3F.

Entree  : resultats/a33-par-famille.csv, a33-contrastes.csv, a33-mesures.csv,
          a33-quintiles.csv
Sortie  : resultats/a33-figure-c3f.png et .svg

Usage : .venv/bin/python analyses/a33_figure.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_figures import (ENCRE, ENCRE_SECONDE, FOND, GRILLE, HUMAIN, LANGAGE, NEUTRE,
                         STATISTIQUE, style)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

# C3F est la condition nouvelle : elle porte la couleur du langage en plein, C3 la meme
# couleur en creux, pour que l'oeil lise "meme modele, contexte different".
COUL = {"C3F": LANGAGE, "C3": LANGAGE, "humains vague 2": HUMAIN,
        "B2 famille retiree": STATISTIQUE, "B2 argmax": STATISTIQUE,
        "B0 mode": STATISTIQUE, "C2": ENCRE_SECONDE, "agents composite": "#e08a1e"}

COURT_FAM = {
    "depenses publiques (nat*)": "depenses nat*",
    "confiance dans les institutions (con*)": "confiance con*",
    "avortement (ab*)": "avortement ab*",
    "libertes civiles (spk/col/lib)": "libertes civiles",
    "fin de vie (suicide/letdie)": "fin de vie",
    "roles de genre (fe*)": "roles de genre fe*",
}

# Decalage manuel des etiquettes du panneau 3, en points, pour eviter les chevauchements.
DECALAGE = {"C3": (9, 5), "C3F": (-9, -12), "humains vague 2": (9, 2),
            "C2": (9, 2), "agents composite": (9, 2), "B2 famille retiree": (9, 4)}

COURT_TEST = {
    "P1 exactitude": "P1 exactitude",
    "P2 taux de fausses raretes": "P2 taux de fausses raretes",
    "P3 rappel des cellules minoritaires": "P3 rappel des minorites",
    "P4 precision des cellules minoritaires": "P4 precision des minorites",
    "P5 H1b rarete de la personne": "P5 H1b rarete de la personne",
    "P6 H2b rarete du segment": "P6 H2b rarete du segment",
    "P7 H2a modale rare du segment": "P7 H2a modale du segment",
    "fausses raretes par cellule": "fausses raretes par cellule",
    "raretes osees par cellule": "raretes osees par cellule",
}


def lire(nom):
    return pd.read_csv(os.path.join(SORTIE, nom))


def enregistrer(fig, base):
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"{base}.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


# ---------------------------------------------------------------------------

def panneau_familles(ax, fam):
    d = fam[fam.condition.isin(["C3", "C3F"])]
    piv = d.pivot_table(index="famille", columns="condition", values="exactitude")
    cous = fam.groupby("famille").cousins_vus_par_C3.first()
    piv = piv.join(cous).sort_values("C3", ascending=True)
    y = np.arange(len(piv))
    for i, (nom, r) in enumerate(piv.iterrows()):
        ax.annotate("", xy=(r["C3F"], i), xytext=(r["C3"], i),
                    arrowprops=dict(arrowstyle="-|>", color=NEUTRE, linewidth=1.4,
                                    shrinkA=3, shrinkB=1))
        ax.plot([r["C3"]], [i], "o", color=FOND, markersize=7,
                markeredgecolor=LANGAGE, markeredgewidth=1.6, zorder=3)
        ax.plot([r["C3F"]], [i], "o", color=LANGAGE, markersize=7, zorder=3)
        ax.annotate(f"{r['cousins_vus_par_C3']:.1f}", (0.995, i), xycoords=("axes fraction",
                                                                           "data"),
                    ha="right", va="center", fontsize=7.5, color=ENCRE_SECONDE)
    ax.set_xlim(0.38, 0.95)
    ax.set_ylim(-0.7, len(piv) - 0.3)
    ax.set_yticks(y)
    ax.set_yticklabels([COURT_FAM.get(n, n) for n in piv.index], fontsize=8.5)
    ax.set_xlabel("exactitude sur les memes cellules", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("1. Retirer la famille du contexte coute de l'exactitude\n"
                 "cercle creux C3, contexte complet ; disque plein C3F, famille retiree ;\n"
                 "a droite, le nombre moyen de cousins que C3 voyait",
                 fontsize=9.5, color=ENCRE, loc="left")
    style(ax, "x")


def panneau_contrastes(ax, ct):
    d = ct[ct.famille.isin(["primaire", "post hoc, hors famille"])].copy()
    d = d.iloc[::-1]
    y = np.arange(len(d))
    for i, (_k, r) in enumerate(d.iterrows()):
        if not np.isfinite(r.difference):
            ax.annotate("test non evaluable, aucun item du perimetre ne porte deux\n"
                        "modalites minoritaires", (0.02, i), xycoords=("axes fraction",
                                                                       "data"),
                        fontsize=7.5, color=NEUTRE, va="center")
            continue
        gras = r.p_holm < 0.05 and r.famille == "primaire"
        coul = LANGAGE if gras else NEUTRE
        ax.plot([r.ic_bas, r.ic_haut], [i, i], color=coul, linewidth=1.6, zorder=2)
        ax.plot([r.difference], [i], "o", color=coul, markersize=6.5, zorder=3)
    ax.axvline(0.0, color=ENCRE_SECONDE, linewidth=1.0, zorder=1)
    ax.set_yticks(y)
    etiq = []
    for _k, r in d.iterrows():
        marque = " *" if (r.famille == "primaire" and r.p_holm < 0.05) else ""
        if r.famille != "primaire":
            marque = " (post hoc)"
        etiq.append(COURT_TEST.get(r.test, r.test) + marque)
    ax.set_yticklabels(etiq, fontsize=8)
    ax.set_xlabel("C3F moins C3, memes cellules", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("2. Les sept contrastes declares\n"
                 "intervalle bootstrap sur les 60 personnes, 4 000 tirages ;\n"
                 "* passe la correction de Holm sur la famille primaire",
                 fontsize=9.5, color=ENCRE, loc="left")
    style(ax, "x")


def panneau_depart(ax, mes):
    d = mes[mes.condition.isin(["C3F", "C3", "C2", "humains vague 2", "agents composite",
                                "B2 famille retiree"])]
    lim = [-0.9, 2.4]
    ax.plot(lim, lim, color=GRILLE, linewidth=1.2, zorder=1)
    ax.axhline(0.0, color=GRILLE, linewidth=0.9, zorder=1)
    ax.axvline(0.0, color=GRILLE, linewidth=0.9, zorder=1)
    for _k, r in d.iterrows():
        c = COUL.get(r.condition, NEUTRE)
        creux = r.condition == "C3"
        ax.plot([r.h_personne_lift_ic_bas, r.h_personne_lift_ic_haut],
                [r.h_segment_lift, r.h_segment_lift], color=c, alpha=0.45, linewidth=1.2)
        ax.plot([r.h_personne_lift, r.h_personne_lift],
                [r.h_segment_lift_ic_bas, r.h_segment_lift_ic_haut],
                color=c, alpha=0.45, linewidth=1.2)
        ax.plot([r.h_personne_lift], [r.h_segment_lift], "o",
                color=FOND if creux else c, markersize=8 if r.condition in ("C3", "C3F")
                else 6.5, markeredgecolor=c, markeredgewidth=1.8 if creux else 0,
                zorder=3)
        dx, dy = DECALAGE.get(r.condition, (8, 6))
        ax.annotate(r.condition, (r.h_personne_lift, r.h_segment_lift),
                    textcoords="offset points", xytext=(dx, dy), fontsize=8,
                    ha="right" if dx < 0 else "left",
                    color=ENCRE if r.condition in ("C3", "C3F") else ENCRE_SECONDE,
                    fontweight="bold" if r.condition in ("C3", "C3F") else "normal")
    ax.set_xlim(lim)
    ax.set_ylim(-0.9, 2.4)
    ax.set_xlabel("lift du cote de la PERSONNE, H1b", fontsize=9, color=ENCRE_SECONDE)
    ax.set_ylabel("lift du cote du GROUPE, H2b", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("3. Le depart entre H1 et H2, sur 60 personnes\n"
                 "au dessus de la diagonale, le groupe pese plus que la personne ;\n"
                 "les intervalles se recouvrent : le rapport n'est pas identifiable ici",
                 fontsize=9.5, color=ENCRE, loc="left")
    style(ax, "both")


def panneau_quintiles(ax, qui):
    for nom, style_ligne in (("C3", "--"), ("C3F", "-")):
        d = qui[qui.condition == nom].sort_values("quintile")
        ax.plot(d.quintile, d.taux_fausses_raretes, style_ligne, color=LANGAGE,
                marker="o" if nom == "C3F" else "s",
                markerfacecolor=LANGAGE if nom == "C3F" else FOND,
                markeredgecolor=LANGAGE, linewidth=1.6, markersize=6.5, label=nom)
        dy = -17 if nom == "C3F" else 11
        for _k, r in d.iterrows():
            ax.annotate(f"{int(r.raretes_osees)}", (r.quintile, r.taux_fausses_raretes),
                        textcoords="offset points", xytext=(0, dy), ha="center",
                        fontsize=7, color=ENCRE_SECONDE)
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.set_xlim(0.7, 5.3)
    ax.set_ylim(0.55, 1.07)
    ax.set_xlabel("quintile de rarete du contexte REELLEMENT VU", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_ylabel("taux de fausses raretes", fontsize=9, color=ENCRE_SECONDE)
    ax.legend(fontsize=8.5, frameon=False, labelcolor=ENCRE_SECONDE, loc="lower left")
    ax.set_title("4. Un contexte pauvre en raretes ne produit pas plus de fausses raretes\n"
                 "hors du bloc secret pour C3, hors de la famille pour C3F ;\n"
                 "sous chaque point, le nombre de raretes osees",
                 fontsize=9.5, color=ENCRE, loc="left")
    style(ax, "y")


def main():
    fam = lire("a33-par-famille.csv")
    ct = lire("a33-contrastes.csv")
    mes = lire("a33-mesures.csv")
    qui = lire("a33-quintiles.csv")

    fig, axes = plt.subplots(2, 2, figsize=(13.4, 10.6))
    fig.patch.set_facecolor(FOND)
    panneau_familles(axes[0, 0], fam)
    panneau_contrastes(axes[0, 1], ct)
    panneau_depart(axes[1, 0], mes)
    panneau_quintiles(axes[1, 1], qui)
    fig.suptitle("a33. Le contexte ampute a personne constante : ce que C3F change et ce "
                 "qu'il ne change pas",
                 fontsize=12.5, color=ENCRE, x=0.02, ha="left", y=0.995)
    fig.tight_layout(rect=(0, 0, 1, 0.975))
    enregistrer(fig, "a33-figure-c3f")


if __name__ == "__main__":
    main()
