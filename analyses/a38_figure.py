"""
a38_figure : l'ecart agent contre humain par item en fonction de l'ampleur de mode
mesuree, modeles de langage contre predicteurs statistiques.

Statut : script d'analyse jetable, aucun appel de modele. Il ne recalcule rien, il lit les
tableaux ecrits par a38_ampleurs.py, a38_mesures.py et a38_tests.py, pour que la figure et
les chiffres du rapport ne puissent pas diverger. Aucun script existant n'est modifie. La
palette et les conventions de trace sont celles de a25_figure et de a28_figures.

Trois panneaux.
  Gauche  : nuage item par item, abscisse l'ampleur de mode M1 en points, ordonnee la
            distance moyenne aux humains sur les huit conditions a modele de langage.
  Milieu  : le meme nuage pour les cinq predicteurs statistiques.
  Droite  : la correlation de rang de chaque methode, avec son intervalle bootstrap sur
            les items. C'est la lecture que le rapport commente.

Entree  : resultats/a38-ampleurs-items.csv, a38-par-item-condition.csv, a38-continu.csv
Sortie  : resultats/a38-figure-mode-continu.png et .svg

Usage : .venv/bin/python analyses/a38_figure.py --perimetre 150
"""

import argparse
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


def couleur(cond):
    if cond == "humains vague 2":
        return HUMAIN
    return LANGAGE if cond in LLM else STATISTIQUE


def style(ax, axe_grille="both"):
    ax.set_facecolor(FOND)
    ax.grid(True, axis=axe_grille, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=9)


def nuage(ax, amp, moy, ecart, rho, ic, titre, coul, etiquettes):
    style(ax)
    ax.vlines(amp, moy - ecart, moy + ecart, color=coul, alpha=0.25, linewidth=1.6,
              zorder=2)
    ax.scatter(amp, moy, s=46, color=coul, edgecolor=FOND, linewidth=0.8, zorder=3)
    # droite des moindres carres, guide de lecture et rien de plus : la statistique
    # commentee est la correlation de rang, pas cette pente
    if len(amp) >= 3:
        b = np.polyfit(amp, moy, 1)
        xs = np.linspace(min(amp), max(amp), 20)
        ax.plot(xs, np.polyval(b, xs), color=coul, linewidth=1.4, alpha=0.5, zorder=1)
    for x, y, nom in zip(amp, moy, etiquettes):
        ax.annotate(nom, (x, y), textcoords="offset points", xytext=(5, 3),
                    fontsize=6.6, color=ENCRE_SECONDE)
    ax.set_title(titre, fontsize=10.5, color=ENCRE, loc="left", pad=9)
    ax.set_xlabel("ampleur de mode mesuree, en points (M1)", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_ylabel("distance moyenne a la population humaine", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.text(0.98, 0.03, f"rho de Spearman moyen {rho:+.3f}\nIC items [{ic[0]:+.2f} ; "
                        f"{ic[1]:+.2f}]",
            transform=ax.transAxes, ha="right", va="bottom", fontsize=8.5,
            color=ENCRE_SECONDE)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--perimetre", default="150")
    args = ap.parse_args()
    per = str(args.perimetre)

    amp = pd.read_csv(os.path.join(SORTIE, "a38-ampleurs-items.csv")).set_index("item")
    d = pd.read_csv(os.path.join(SORTIE, "a38-par-item-condition.csv"))
    c = pd.read_csv(os.path.join(SORTIE, "a38-continu.csv"))
    d["perimetre"] = d.perimetre.astype(str)
    c["perimetre"] = c.perimetre.astype(str)
    d = d[(d.perimetre == per) & (d.camp == "tous")]
    c = c[(c.perimetre == per) & (c.score == "M1 mode") & (c.hypothese == "K1 distance")]

    couverts = amp.index[amp.m1_mode.notna()]
    d = d[d.item.isin(couverts)]

    fig, axes = plt.subplots(1, 3, figsize=(17.2, 6.2),
                             gridspec_kw={"width_ratios": [1.0, 1.0, 0.95]})
    fig.patch.set_facecolor(FOND)

    for ax, groupe, coul, titre in [
            (axes[0], [g for g in LLM if g in set(d.condition)], LANGAGE,
             "Huit conditions a modele de langage"),
            (axes[1], [g for g in STAT if g in set(d.condition)], STATISTIQUE,
             "Cinq predicteurs statistiques")]:
        s = d[d.condition.isin(groupe)]
        piv = s.pivot_table(index="item", columns="condition", values="distance")
        moy = piv.mean(axis=1)
        ecart = piv.std(axis=1)
        a = amp.loc[moy.index, "m1_mode"]
        rhos = c[c.condition.isin(groupe)]
        nuage(ax, a.values, moy.values, ecart.values,
              float(rhos.rho_spearman.mean()),
              (float(rhos.ic_items_bas.mean()), float(rhos.ic_items_haut.mean())),
              titre, coul, list(moy.index))

    # ---------------------------------------------------------------- panneau droit
    ax = axes[2]
    style(ax, "x")
    ordre = [m for m in ORDRE_METHODES if m in set(c.condition)]
    ys = np.arange(len(ordre))[::-1]
    for y, cond in zip(ys, ordre):
        r = c[c.condition == cond].iloc[0]
        col = couleur(cond)
        ax.plot([r.ic_items_bas, r.ic_items_haut], [y, y], color=col, linewidth=2.0,
                alpha=0.55, zorder=2)
        ax.plot([r.rho_spearman], [y], "o", color=col, markersize=7,
                markeredgecolor=FOND, markeredgewidth=0.8, zorder=3)
        ax.annotate(f"p = {r.p_permutation:.3f}", (0.985, y), xycoords=("axes fraction",
                    "data"), ha="right", va="center", fontsize=7.6,
                    color=ENCRE_SECONDE)
    ax.axvline(0.0, color=ENCRE, linewidth=1.0, alpha=0.65, zorder=1)
    ax.set_yticks(ys)
    ax.set_yticklabels(ordre, fontsize=8.6, color=ENCRE)
    ax.set_xlabel("correlation de rang entre ampleur de mode et distance", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_title("Par methode, intervalle bootstrap sur les items",
                 fontsize=10.5, color=ENCRE, loc="left", pad=9)
    ax.set_xlim(-1.0, 1.0)

    n = int(amp.m1_mode.notna().sum())
    fig.suptitle(
        f"a38. Ecart agent contre humain et ampleur de mode publiee, {n} items sur 149, "
        f"perimetre {per}",
        fontsize=13, color=ENCRE, x=0.012, ha="left", y=0.985)
    fig.text(0.012, 0.030,
             "Ampleur M1 : contrastes de mode mesures par NORC, MR099 face a face contre "
             "web sur les 16 items de depense, MR021 vote declare contre resultats "
             "officiels, MR086 presence d'un tiers, et l'atlas NBER 2025 declaration "
             "contre registre individuel.",
             fontsize=8.2, color=ENCRE_SECONDE)
    fig.text(0.012, 0.010,
             "Barre verticale du nuage : ecart type entre conditions du groupe. Droite : "
             "moindres carres, guide de lecture seulement. Aucune correlation "
             "individuelle ne se distingue de zero.",
             fontsize=8.2, color=ENCRE_SECONDE)
    fig.tight_layout(rect=[0.004, 0.055, 0.996, 0.945])

    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"a38-figure-mode-continu.{ext}")
        fig.savefig(chemin, dpi=190, facecolor=FOND)
        print(f"ecrit : {chemin}")


if __name__ == "__main__":
    main()
