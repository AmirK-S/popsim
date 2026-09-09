"""
a31_figure : les fausses raretes par mecanisme et par condition.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par a31_mecanismes.py, pour que la figure et les chiffres du rapport ne
puissent pas diverger. Aucun script existant n'est modifie. La palette et les conventions
de trace sont celles de a25_figure, a28_figures et a29_figure, importees telles quelles.

Six panneaux. Les cinq premiers portent chacun un mecanisme ; le sixieme porte le depart
entre les deux qui restent en lice a la fin.

Convention commune aux panneaux 1 a 4 : le LIFT, c'est a dire la valeur mesuree sur les
fausses raretes divisee par celle du temoin aveugle a la personne, moins un. Zero veut
dire "le mecanisme n'explique rien de plus qu'un placement au hasard parmi les repondants
du meme item" ; 0,50 veut dire "la moitie de plus que ce hasard". Le lift est sans unite,
c'est ce qui permet de mettre cinq mecanismes de natures differentes sur le meme axe.

Entree  : resultats/a31-mecanismes.csv, a31-h4-confiance.csv,
          a31-leviers-personne-segment.csv
Sortie  : resultats/a31-figure-rarete.png et .svg

Usage : .venv/bin/python analyses/a31_figure.py
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

M_H1A = "H1a deplacement dans la famille"
M_H2A = "H2a rarete modale du segment"
M_H3 = "H3 position extreme"
M_H5 = "H5 rarete du contexte"
M_H2B = "H2b exces de rarete du segment"

# Perimetre naturel : les 1 052 personnes partout, sauf C2 et C3 qui n'existent que sur
# les 150 du run local. La ligne humaine des deux perimetres est tracee separement.
PERIMETRE = {c: ("150" if c in ("C2", "C3") else "1052") for c in ORDRE_METHODES}


def lire(nom):
    return pd.read_csv(os.path.join(SORTIE, nom))


def lift(d, mecanisme, condition, perimetre):
    s = d[(d.mecanisme == mecanisme) & (d.condition == condition)
          & (d.perimetre.astype(str) == perimetre)]
    if s.empty:
        return np.nan, np.nan, np.nan
    v, t = float(s.valeur.iloc[0]), float(s.temoin.iloc[0])
    b, h = float(s.ic_bas.iloc[0]), float(s.ic_haut.iloc[0])
    if not np.isfinite(v) or not np.isfinite(t) or t <= 0:
        return np.nan, np.nan, np.nan
    return v / t - 1.0, b / t - 1.0, h / t - 1.0


def panneau_lift(ax, d, mecanisme, titre, sous_titre, xlim):
    """Une ligne par condition, le lift et son intervalle bootstrap sur les personnes."""
    style(ax, axe_grille="x")
    ordre = [c for c in ORDRE_METHODES if c != "humains vague 2"]
    ordre = [c for c in ordre if np.isfinite(lift(d, mecanisme, c, PERIMETRE[c])[0])]
    for i, cond in enumerate(ordre):
        v, b, h = lift(d, mecanisme, cond, PERIMETRE[cond])
        ax.plot([b, h], [i, i], color=NEUTRE, linewidth=1.4, zorder=2)
        ax.plot([v], [i], "o", color=couleur(cond), markersize=6.4, zorder=3,
                markeredgecolor=ENCRE if cond in ("C2", "C3") else "none",
                markeredgewidth=1.0 if cond in ("C2", "C3") else 0)
    for nom_per, trait in (("1052", "--"), ("150", ":")):
        v, _, _ = lift(d, mecanisme, "humains vague 2", nom_per)
        if np.isfinite(v):
            ax.axvline(v, color=HUMAIN, linewidth=1.2, linestyle=trait, zorder=1)
    ax.axvline(0.0, color=ENCRE_SECONDE, linewidth=1.0, zorder=1)
    ax.set_yticks(range(len(ordre)))
    ax.set_yticklabels([COURT.get(c, c) for c in ordre], fontsize=8.2, color=ENCRE)
    ax.set_ylim(len(ordre) + 0.1, -0.7)
    ax.set_xlim(*xlim)
    ax.set_xlabel("lift sur le temoin aveugle a la personne", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=10.5, color=ENCRE, loc="left")
    ax.text(0.0, -0.55, sous_titre, fontsize=7.8, color=ENCRE_SECONDE,
            transform=ax.get_yaxis_transform(), ha="left", va="center", clip_on=False)


def panneau_confiance(ax, cfd):
    """H4 : la confiance du modele selon le type de cellule, C2 et C3."""
    style(ax, axe_grille="y")
    types = ["rarete non osee, cellule majoritaire", "rarete juste", "fausse rarete",
             "mauvaise modalite rare"]
    libelles = ["cellule ou aucune\nrarete n'est osee", "rarete juste",
                "fausse rarete", "mauvaise\nmodalite rare"]
    largeur = 0.36
    for k, (cond, teinte) in enumerate((("C2", LANGAGE), ("C3", STATISTIQUE))):
        vals = [float(cfd[(cfd.condition == cond)
                          & (cfd.cellules == t)].part_p_max_sup_099.iloc[0])
                if not cfd[(cfd.condition == cond) & (cfd.cellules == t)].empty
                else np.nan for t in types]
        x = np.arange(len(types)) + (k - 0.5) * largeur
        ax.bar(x, vals, width=largeur, color=teinte, zorder=3,
               label=f"{cond}, avec etiquette" if cond == "C2" else f"{cond}, sans etiquette")
        for xi, v in zip(x, vals):
            if np.isfinite(v):
                ax.text(xi, v + 0.015, f"{v:.2f}", ha="center", va="bottom",
                        fontsize=7.6, color=ENCRE_SECONDE)
    ax.set_xticks(range(len(types)))
    ax.set_xticklabels(libelles, fontsize=8.0, color=ENCRE)
    ax.set_ylim(0, 1.0)
    ax.set_ylabel("part des cellules a p max superieur a 0,99", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_title("5. H4, sur confiance : le signe est l'inverse de l'hypothese",
                 fontsize=10.5, color=ENCRE, loc="left")
    ax.legend(loc="upper right", fontsize=8, frameon=False, labelcolor=ENCRE_SECONDE)


def panneau_depart(ax, lv):
    """Le depart entre H1 et H2 : lift du cote de la personne contre lift du segment."""
    style(ax, axe_grille="both")
    d = lv[lv.apply(lambda r: PERIMETRE.get(r.condition, "1052") == str(r.perimetre),
                    axis=1)]
    lim = (-0.08, 0.92)
    ax.plot(lim, lim, color=GRILLE, linewidth=1.2, zorder=1)
    ax.text(0.62, 0.66, "autant par la personne\nque par le groupe", fontsize=7.6,
            color=NEUTRE, ha="left", va="center", rotation=38)
    ax.axhline(0, color=ENCRE_SECONDE, linewidth=0.9, zorder=1)
    ax.axvline(0, color=ENCRE_SECONDE, linewidth=0.9, zorder=1)
    decalage = {"agents enquete": (-9, 9), "B2 argmax": (-9, 3),
                "agents v7": (-9, -9), "B0 tirage": (8, -10),
                "agents composite": (8, -10), "humains vague 2": (-12, 8),
                "agents demographiques (v6)": (8, 4), "C3": (8, -10)}
    for _, r in d.iterrows():
        c = couleur(r.condition)
        gros = r.condition == "humains vague 2"
        ax.plot([r.lift_personne], [r.lift_segment], "o", color=c,
                markersize=9.0 if gros else 6.5, zorder=4,
                markeredgecolor=ENCRE if (gros or r.condition in ("C2", "C3")) else "none",
                markeredgewidth=1.1 if (gros or r.condition in ("C2", "C3")) else 0)
        dx, dy = decalage.get(r.condition, (8, 3))
        ax.annotate(COURT.get(r.condition, r.condition),
                    (r.lift_personne, r.lift_segment), textcoords="offset points",
                    xytext=(dx, dy), fontsize=8.2 if gros else 7.8,
                    color=ENCRE if gros else ENCRE_SECONDE,
                    fontweight="bold" if gros else "normal", zorder=5,
                    ha="right" if dx < 0 else "left")
    ax.set_xlim(*lim)
    ax.set_ylim(*lim)
    ax.set_xlabel("lift du cote de la PERSONNE : rarete reelle de la personne",
                  fontsize=9, color=ENCRE_SECONDE)
    ax.set_ylabel("lift du cote du GROUPE : rarete reelle du segment ideologique",
                  fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("6. Le depart : la fausse rarete suit elle la personne ou le groupe ?",
                 fontsize=10.5, color=ENCRE, loc="left")


def main():
    mes = lire("a31-mecanismes.csv")
    mes = mes[mes.seuil == 0.10]
    mes["perimetre"] = mes.perimetre.astype(str)
    cfd = lire("a31-h4-confiance.csv")
    lv = lire("a31-leviers-personne-segment.csv")
    lv["perimetre"] = lv.perimetre.astype(str)

    fig, axes = plt.subplots(2, 3, figsize=(18.0, 11.0),
                             gridspec_kw={"wspace": 0.34, "hspace": 0.30})
    fig.patch.set_facecolor(FOND)

    panneau_lift(axes[0][0], mes, M_H1A,
                 "1. H1, deplacement de rarete",
                 "la personne est rare ailleurs dans la meme famille thematique",
                 (-0.85, 2.10))
    panneau_lift(axes[0][1], mes, M_H2A,
                 "2. H2a, rarete de groupe, le choix de la modalite",
                 "la modalite predite est la modalite rare modale du segment ideologique",
                 (-0.45, 1.30))
    panneau_lift(axes[0][2], mes, M_H2B,
                 "3. H2b, rarete de groupe, le placement",
                 "le segment ideologique est reellement souvent rare sur cet item la",
                 (-0.20, 1.05))
    panneau_lift(axes[1][0], mes, M_H3,
                 "4. H3, position de la modalite",
                 "la modalite predite est en premiere ou en derniere position",
                 (-0.35, 0.55))
    panneau_confiance(axes[1][1], cfd)
    panneau_depart(axes[1][2], lv)

    axes[0][0].plot([], [], "o", color=LANGAGE, label=f"condition a modele de langage ({len(LLM)})")
    axes[0][0].plot([], [], "o", color=STATISTIQUE, label=f"predicteur statistique ({len(STAT)})")
    axes[0][0].plot([], [], color=HUMAIN, linestyle="--",
                    label="memes humains reinterroges, 1 052 personnes")
    axes[0][0].plot([], [], color=HUMAIN, linestyle=":",
                    label="memes humains reinterroges, 150 personnes")
    axes[0][0].legend(loc="upper center", bbox_to_anchor=(1.72, 1.19), ncol=4,
                      fontsize=9, frameon=False, labelcolor=ENCRE_SECONDE)

    fig.suptitle("a31. Pourquoi la bonne personne recoit elle la mauvaise rarete ? "
                 "Les fausses raretes par mecanisme et par condition, seuil 10 pour cent",
                 fontsize=12.5, color=ENCRE, x=0.012, ha="left", y=0.985)
    fig.text(0.012, 0.945,
             "Une fausse rarete est une cellule ou la methode ose une modalite "
             "minoritaire et ou la personne a en realite repondu comme la majorite. "
             "C2 et C3 sont mesures sur les 150 personnes du run local, cercles cernes "
             "de noir ; toutes les autres sur les 1 052.",
             fontsize=9, color=ENCRE_SECONDE, ha="left")

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a31-figure-rarete.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print("ecrit :", chemin)
    plt.close(fig)


if __name__ == "__main__":
    main()
