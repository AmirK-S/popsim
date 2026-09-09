"""
c1_figures : les deux figures du mois 1 du programme C version menages.

Ce script ne recalcule rien. Il lit les tableaux ecrits par c1_dispersion.py,
c1_stabilite.py et c1_previsibilite.py, pour que la figure et les chiffres du rapport ne
puissent pas diverger. La palette et les conventions de trace sont celles de a28_figures,
importees telles quelles ; aucun script existant n'est modifie.

Figure 1, c1-figure-dispersion-mensuelle
  A  La dispersion inter menages des anticipations d'inflation a un an, mois par mois, de
     2017 a 2025 : ecart interquartile total et mediane des ecarts interquartiles a
     l'interieur des cohortes. Le choc de 2025 est marque par les deux regles.
  B  La part de la dispersion qui est INTER cohortes, mois par mois, pour les sept
     variables primaires. C'est la quantite qui decide de l'enonce du programme C.
  C  Avant et apres le choc, l'ecart interquartile de chaque variable, sous la regle
     primaire et sous la regle secondaire.

Figure 2, c1-figure-chute-permutation
  A  Pour chaque predicteur, le Spearman observe et le Spearman apres permutation des
     menages a l'interieur du couple (mois, cohorte). La longueur du trait est la chute,
     quantite de verdict preenregistree.
  B  La chute, variable par variable, pour l'historique du menage contre les demographies
     seules.
  C  La courbe de retest par delai, un a onze mois, avec la part stable en trait plein.
  D  Qui bouge au choc : l'AUC et sa chute pour chaque predicteur, sur l'ampleur de la
     revision et sur sa direction.

Sorties : resultats/c1-figure-dispersion-mensuelle.{png,svg}
          resultats/c1-figure-chute-permutation.{png,svg}
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

COURT = {"infl1": "inflation 1 an", "infl3": "inflation 3 ans",
         "revenu": "revenu du menage", "depense": "depense du menage",
         "logement": "prix du logement", "perte_emploi": "perte d'emploi",
         "chomage": "chomage en hausse", "infl1_var": "incertitude d'inflation",
         "infl1_point": "inflation, point"}
ORDRE_PRED = ["F", "HD", "H", "P", "T0b", "T1", "D"]
NOM_PRED = {"P": "P, persistance seule", "D": "D, demographies seules",
            "H": "H, historique du menage", "HD": "HD, historique et demographies",
            "F": "F, foret", "T1": "T1, temoin de cohorte hors pli",
            "T0b": "T0b, cohorte a plein echantillon"}
NOM_BOUGE = {"V": "V, volatilite passee seule", "N": "N, ecart au niveau moyen",
             "L": "L, niveau d'avant, signe", "D": "D, demographies seules",
             "H": "H, historique du menage", "HD": "HD, historique et demographies",
             "T0b": "T0b, temoin constant"}


def lire(nom):
    return pd.read_csv(os.path.join(SORTIE, nom))


def enregistrer(fig, nom):
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"{nom}.{ext}")
        fig.savefig(chemin, dpi=200, facecolor=FOND, bbox_inches="tight")
        print(f"ecrit {chemin}", flush=True)
    plt.close(fig)


# ---------------------------------------------------------------------------
# Figure 1
# ---------------------------------------------------------------------------

def figure_dispersion():
    mens = lire("c1-dispersion-mensuelle.csv")
    choc = lire("c1-choc-2025.csv")
    ap = lire("c1-avant-apres-choc.csv")
    t_prim = int(choc[choc["regle"].str.startswith("primaire")]["t"].iloc[0])
    t_sec = int(choc[choc["regle"].str.startswith("secondaire")]["t"].iloc[0])

    fig = plt.figure(figsize=(12.4, 10.2), facecolor=FOND)
    gs = fig.add_gridspec(3, 1, height_ratios=[1.05, 1.05, 0.95], hspace=0.42)

    # A -------------------------------------------------------------------
    ax = fig.add_subplot(gs[0])
    style(ax, axe_grille="both")
    d = mens[mens["variable"] == "infl1"].sort_values("t")
    ax.plot(d["t"], d["iqr_total"], color=ENCRE, linewidth=1.7,
            label="dispersion totale, ecart interquartile entre menages")
    ax.plot(d["t"], d["iqr_intra_median"], color=STATISTIQUE, linewidth=1.5,
            linestyle="-", label="dispersion a l'interieur des cohortes, mediane des IQR")
    ax.plot(d["t"], d["iqr_medianes"], color=LANGAGE, linewidth=1.5,
            label="dispersion entre cohortes, IQR des medianes de cohorte")
    ax.plot(d["t"], d["moyenne"], color=HUMAIN, linewidth=1.3, linestyle="--",
            label="moyenne des anticipations, pour situer")
    bas = float(d["iqr_medianes"].min())
    for t, cle, style_ in ((t_prim, "choc, regle primaire", "-"),
                           (t_sec, "choc, regle secondaire", ":")):
        ax.axvline(t, color=NEUTRE, linewidth=1.2, linestyle=style_, zorder=1)
        ax.text(t - 1.2, bas, cle + "  ", rotation=90, va="bottom", ha="right",
                fontsize=7.5, color=ENCRE_SECONDE)
    ax.axvspan(mens[mens["perimetre"] == "descriptif 2017-2019"]["t"].min(),
               mens[mens["perimetre"] == "descriptif 2017-2019"]["t"].max(),
               color=GRILLE, alpha=0.45, zorder=0)
    ticks = [t for t in d["t"] if (t % 12) == 0]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{2013 + t // 12}" for t in ticks])
    ax.set_ylabel("points de pourcentage", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("A. Anticipation d'inflation a un an : la dispersion entre menages est "
                 "presque toute a l'interieur des cohortes\n"
                 "zone grisee : 2017-2019, descriptif ; le reste est le perimetre "
                 "primaire 2020-2025",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    ax.legend(fontsize=8.2, frameon=False, labelcolor=ENCRE_SECONDE, ncol=2,
              loc="upper left")

    # B -------------------------------------------------------------------
    ax = fig.add_subplot(gs[1])
    style(ax, axe_grille="both")
    prim = mens[mens["perimetre"] == "primaire 2020-2025"]
    couleurs = [ENCRE, STATISTIQUE, LANGAGE, HUMAIN, NEUTRE, ENCRE_SECONDE, "#a06cd5",
                "#d59a2a", "#4aa3a3"]
    for c, v in zip(couleurs, ["infl1", "infl3", "revenu", "depense", "logement",
                               "perte_emploi", "chomage", "infl1_var", "infl1_point"]):
        dd = prim[prim["variable"] == v].sort_values("t")
        ax.plot(dd["t"], dd["part_inter"], color=c, linewidth=1.3, label=COURT[v])
    ax.axhline(0, color=ENCRE_SECONDE, linewidth=0.9)
    ax.axhline(0.15, color=NEUTRE, linewidth=1.0, linestyle="--")
    ax.text(prim["t"].min(), 0.155, "borne de la prediction P1, 0,15", fontsize=8,
            color=ENCRE_SECONDE, va="bottom")
    for t, s_ in ((t_prim, "-"), (t_sec, ":")):
        ax.axvline(t, color=NEUTRE, linewidth=1.2, linestyle=s_, zorder=1)
    ticks = [t for t in prim["t"].unique() if (t % 12) == 0]
    ax.set_xticks(ticks)
    ax.set_xticklabels([f"{2013 + t // 12}" for t in ticks])
    ax.set_ylabel("part inter cohortes", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("B. Part de la dispersion qui separe les cohortes age x diplome x revenu, "
                 "variance corrigee du biais d'echantillonnage",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    ax.legend(fontsize=8, frameon=False, labelcolor=ENCRE_SECONDE, ncol=5,
              loc="upper left")

    # C -------------------------------------------------------------------
    ax = fig.add_subplot(gs[2])
    style(ax, axe_grille="y")
    vars_ = ["infl1", "infl3", "revenu", "depense", "logement", "perte_emploi",
             "chomage", "infl1_var", "infl1_point"]
    x = np.arange(len(vars_))
    for k, (regle, coul, dec) in enumerate(
            (("primaire, saut de moyenne", ENCRE, -0.18),
             ("secondaire, saut d'IQR", STATISTIQUE, 0.18))):
        d = ap[ap["regle"] == regle].set_index("variable").loc[vars_]
        ax.bar(x + dec, d["ratio_iqr"] - 1.0, width=0.32, color=coul, alpha=0.85,
               label=f"{regle}, mois {d['mois_choc'].iloc[0]}")
    ax.axhline(0, color=ENCRE_SECONDE, linewidth=0.9)
    ax.axhline(0.10, color=NEUTRE, linewidth=1.0, linestyle="--")
    ax.text(-0.45, 0.105, "borne de la prediction P3, plus 10 pour cent", fontsize=8,
            color=ENCRE_SECONDE, va="bottom")
    ax.set_xticks(x)
    ax.set_xticklabels([COURT[v] for v in vars_], fontsize=8.5, rotation=20, ha="right")
    ax.set_ylabel("variation relative de l'IQR", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("C. Ce que le choc de 2025 fait a la dispersion : trois mois avant contre "
                 "trois mois a partir du choc",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    ax.legend(fontsize=8.2, frameon=False, labelcolor=ENCRE_SECONDE)

    enregistrer(fig, "c1-figure-dispersion-mensuelle")


# ---------------------------------------------------------------------------
# Figure 2
# ---------------------------------------------------------------------------

def figure_permutation():
    par_var = lire("c1-previsibilite-par-variable.csv")
    synth = lire("c1-previsibilite-synthese.csv")
    retest = lire("c1-retest-par-delai.csv")
    stable = lire("c1-part-stable.csv")
    bouge = lire("c1-qui-bouge-choc.csv")

    fig = plt.figure(figsize=(12.4, 9.6), facecolor=FOND)
    gs = fig.add_gridspec(2, 2, hspace=0.44, wspace=0.26)

    # A -------------------------------------------------------------------
    ax = fig.add_subplot(gs[0, 0])
    style(ax, axe_grille="x")
    d = synth.set_index("predicteur").reindex(ORDRE_PRED).dropna(subset=["rho_moyen"])
    y = np.arange(len(d))[::-1]
    for yy, (nom, r) in zip(y, d.iterrows()):
        depart = r["rho_moyen"] - r["chute_moyenne"]
        coul = NEUTRE if nom.startswith("T") else (STATISTIQUE if nom in ("D",) else ENCRE)
        ax.plot([depart, r["rho_moyen"]], [yy, yy], color=coul, linewidth=3.2,
                solid_capstyle="butt", zorder=2)
        ax.plot(depart, yy, "o", color=NEUTRE, markersize=5, zorder=3)
        ax.plot(r["rho_moyen"], yy, "o", color=coul, markersize=6, zorder=3)
        ax.text(max(r["rho_moyen"], depart) + 0.012, yy,
                f"chute {r['chute_moyenne']:.3f}", fontsize=8, va="center",
                color=ENCRE_SECONDE)
    ax.set_yticks(y)
    ax.set_yticklabels([NOM_PRED.get(i, i) for i in d.index], fontsize=8.5)
    ax.set_xlabel("Spearman moyen sur les neuf variables", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("A. Predire l'anticipation du mois suivant.\nLe point gris est la valeur "
                 "apres permutation des menages\ndans (mois, cohorte) ; le trait est la "
                 "quantite de verdict",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)

    # B -------------------------------------------------------------------
    ax = fig.add_subplot(gs[0, 1])
    style(ax, axe_grille="y")
    vars_ = [v for v in COURT if v in set(par_var["variable"])]
    x = np.arange(len(vars_))
    for nom, coul, dec in (("H", ENCRE, -0.22), ("P", HUMAIN, 0.0),
                           ("D", STATISTIQUE, 0.22)):
        d = par_var[par_var["predicteur"] == nom].set_index("variable").reindex(vars_)
        ax.bar(x + dec, d["chute"], width=0.2, color=coul, alpha=0.9,
               label=NOM_PRED[nom])
        ax.errorbar(x + dec, d["chute"],
                    yerr=[np.maximum(d["chute"] - d["chute_ic_bas"], 0),
                          np.maximum(d["chute_ic_haut"] - d["chute"], 0)],
                    fmt="none", ecolor=ENCRE_SECONDE, elinewidth=0.9, capsize=2)
    ax.axhline(0, color=ENCRE_SECONDE, linewidth=0.9)
    ax.set_xticks(x)
    ax.set_xticklabels([COURT[v] for v in vars_], fontsize=8, rotation=25, ha="right")
    ax.set_ylabel("chute sous permutation intra cohorte", fontsize=9, color=ENCRE_SECONDE)
    ax.set_title("B. La meme quantite, variable par variable,\nintervalles bootstrap sur "
                 "les menages",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    bas, haut = ax.get_ylim()
    ax.set_ylim(bas, haut * 1.22)
    ax.legend(fontsize=8.2, frameon=False, labelcolor=ENCRE_SECONDE, ncol=3,
              loc="upper center")

    # C -------------------------------------------------------------------
    ax = fig.add_subplot(gs[1, 0])
    style(ax, axe_grille="both")
    couleurs = {"infl1": ENCRE, "infl3": STATISTIQUE, "revenu": LANGAGE,
                "depense": HUMAIN, "logement": NEUTRE, "perte_emploi": ENCRE_SECONDE,
                "chomage": "#a06cd5", "infl1_var": "#d59a2a", "infl1_point": "#4aa3a3"}
    for v, coul in couleurs.items():
        d = retest[retest["variable"] == v].sort_values("delai_mois")
        if not len(d):
            continue
        ax.plot(d["delai_mois"], d["rho"], color=coul, linewidth=1.4, marker="o",
                markersize=3, label=COURT[v])
        s = stable[stable["variable"] == v]
        if len(s):
            ax.axhline(float(s["part_stable"].iloc[0]), color=coul, linewidth=0.8,
                       linestyle=":", alpha=0.7)
    ax.set_xlabel("delai entre les deux passations, en mois", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_ylabel("Spearman de retest, moyennes de mois retirees", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_title("C. Le plancher de reinterrogation, onze delais.\nLes pointilles sont la "
                 "part stable estimee par analyse de variance",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    ax.legend(fontsize=7.6, frameon=False, labelcolor=ENCRE_SECONDE, ncol=2,
              loc="lower left")

    # D -------------------------------------------------------------------
    ax = fig.add_subplot(gs[1, 1])
    style(ax, axe_grille="x")
    d = bouge[(bouge["variable"] == "infl1")
              & (bouge["regle_choc"].str.startswith("primaire"))]
    ordre = ["HD", "H", "V", "L", "N", "D", "T0b"]
    y = np.arange(len(ordre))[::-1]
    for cible, coul, dec in (("Y_rev", ENCRE, 0.16), ("Y_dir", STATISTIQUE, -0.16)):
        dd = d[d["cible"] == cible].set_index("predicteur").reindex(ordre)
        ax.barh(y + dec, dd["chute"], height=0.3, color=coul, alpha=0.9,
                label="ampleur de la revision" if cible == "Y_rev"
                else "direction de la revision")
        ax.errorbar(dd["chute"], y + dec,
                    xerr=[np.maximum(dd["chute"] - dd["chute_ic_bas"], 0),
                          np.maximum(dd["chute_ic_haut"] - dd["chute"], 0)],
                    fmt="none", ecolor=ENCRE_SECONDE, elinewidth=0.9, capsize=2)
    ax.axvline(0, color=ENCRE_SECONDE, linewidth=0.9)
    ax.set_yticks(y)
    ax.set_yticklabels([NOM_BOUGE[i] for i in ordre], fontsize=8.5)
    ax.yaxis.tick_right()   # sinon les libelles mordent sur le panneau C
    ax.tick_params(axis="y", colors=ENCRE_SECONDE, labelsize=8.5)
    ax.set_xlabel("chute de l'AUC sous permutation intra cohorte", fontsize=9,
                  color=ENCRE_SECONDE)
    ax.set_title("D. Qui revise son anticipation d'inflation au choc,\n"
                 f"regle primaire, mois {d['mois_choc'].iloc[0] if len(d) else ''}",
                 fontsize=10.5, color=ENCRE, loc="left", pad=10)
    ax.legend(fontsize=8.2, frameon=False, labelcolor=ENCRE_SECONDE, loc="lower right")

    enregistrer(fig, "c1-figure-chute-permutation")


def main():
    figure_dispersion()
    figure_permutation()
    print("c1_figures termine")


if __name__ == "__main__":
    main()
