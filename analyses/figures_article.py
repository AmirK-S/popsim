"""
figures_article : les deux figures du manuscrit (article/manuscrit.md).

Ne recalcule rien. Lit uniquement des CSV deja calcules dans resultats/ :
  - c7-monde-ouvert.csv, c7-monde-ouvert-roc.csv,
    c7-attaquant-fort.csv                               -> figure 1
  - c7-compromis-robustesse-points.csv (13 points, dont le retest humain,
    superset de c7-compromis.csv), c7-disjoint-nul.csv,
    c7-disjoint-resume.csv, c7-ic-manquants.csv          -> figure 2

Aucun appel de modele, aucun reseau. Etiquettes/axes/legendes en anglais,
lisibles en noir et blanc (formes + styles de trait distincts, la couleur est
un renfort optionnel jamais le seul signal). Sortie : article/figures/*.png
(300 dpi, taille colonne simple ~3.4 in de large).

Usage : .venv/bin/python analyses/figures_article.py

Donnees manquantes signalees ici (ne pas inventer, ne pas combler) :
  - Figure 1 : l'attaquant fort (A-LLR hors pli, analyses/c7_attaquant_fort.py) n'a
    ete evalue qu'a deux seuils de FPR (0,1 % et 1 %), jamais sur une courbe ROC
    complete, et c7-attaquant-fort.csv ne porte pas de colonnes _bas/_haut pour ces
    deux taux (seul le top-1 en monde ferme a un IC bootstrap). L'attaque forte est
    donc tracee comme deux points isoles, sans ligne qui relierait des seuils
    intermediaires jamais mesures, et sans barre d'erreur.
  - Figure 2 : le "nul de marge" disponible (c7-disjoint-nul.csv) ne donne
    qu'une distribution de rho de Spearman simule (corr. globale
    fidelite~fuite), pas de valeurs de fuite simulees par predicteur/point.
    Impossible donc de tracer une bande spatiale (x,y) superposee au nuage
    sans inventer des points. A la place : un encart montre la distribution
    des rho nuls (bande 5e-95e centile) contre le rho observe correspondant
    (meme test, items disjoints), ce qui est la comparaison decisive du
    controle sans invention de donnees.
"""

import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTATS = os.path.join(RACINE, "resultats")
FIGURES = os.path.join(RACINE, "article", "figures")
os.makedirs(FIGURES, exist_ok=True)

plt.rcParams.update({
    "font.size": 8,
    "axes.titlesize": 9,
    "axes.labelsize": 8.5,
    "legend.fontsize": 6.8,
    "xtick.labelsize": 7.5,
    "ytick.labelsize": 7.5,
    "axes.edgecolor": "black",
    "axes.linewidth": 0.8,
    "figure.facecolor": "white",
    "axes.facecolor": "white",
})

FPR_FLOOR = 4e-4  # plancher d'affichage log pour les points fpr=0 (rendu seulement,
                    # aucune valeur numerique n'est modifiee dans les CSV sources)


def _floor_fpr(fpr):
    fpr = np.asarray(fpr, dtype=float)
    return np.where(fpr <= 0.0, FPR_FLOOR, fpr)


# ---------------------------------------------------------------------------
# Figure 1 : monde ouvert, TPR vs FPR (log), Twin et Stanford
# ---------------------------------------------------------------------------

STYLES_F1 = {
    "meilleur": dict(ls="--", marker="o", lw=1.3, ms=3.0, color="0.25",
                      label="Naive attack (Hamming)"),
    "demo": dict(ls="--", marker="s", lw=1.1, ms=2.6, color="0.35",
                  label="Demographics Only"),
    "pmm": dict(ls=":", marker="^", lw=1.1, ms=2.6, color="0.4",
                 label="PMM k=10"),
    "humain": dict(ls="-.", marker="", lw=1.6, ms=0, color="0.1",
                     label="Human retest (ceiling)"),
}

# Attaquant fort (A-LLR, hors pli) : jamais evalue en courbe complete, seulement aux
# deux seuils de FPR deja affiches en repere (0,1 % et 1 %). Trace en points isoles,
# trait plein absent par construction (relier deux seuils mesures inventerait la forme
# entre eux). Marqueur plein noir pour rester net en noir et blanc.
STYLE_FORT = dict(marker="D", ms=4.6, color="black",
                   label="Strong attack (A-LLR), 0.1%/1% FPR points only")

PREDICTEUR_A_CLE = {
    ("Twin", "Meilleur jumeau (JSON Persona GPT4.1)"): "meilleur",
    ("Twin", "Demographics Only - GPT4.1-mini"): "demo",
    ("Twin", "PMM k=10"): "pmm",
    ("Twin", "Retest humain (plafond)"): "humain",
    ("Stanford", "Meilleur agent (composite)"): "meilleur",
    ("Stanford", "démographique"): "demo",
    ("Stanford", "PMM k=10"): "pmm",
    ("Stanford", "Retest humain (plafond)"): "humain",
}

# jeu de la figure -> jeu de c7-attaquant-fort.csv, et l'etiquette de l'attaque forte
# retenue par le preenregistrement (A-LLR hors pli, pas A-MI qui est en echantillon).
JEU_ATTAQUANT_FORT = {"Twin": "Twin", "Stanford": "Park GSS"}
ATTAQUE_FORTE = "A-LLR (vraisemblance, hors pli)"


def figure1():
    roc = pd.read_csv(os.path.join(RESULTATS, "c7-monde-ouvert-roc.csv"))
    resume = pd.read_csv(os.path.join(RESULTATS, "c7-monde-ouvert.csv"))
    fort = pd.read_csv(os.path.join(RESULTATS, "c7-attaquant-fort.csv"))
    fort = fort[fort["attaque"] == ATTAQUE_FORTE]

    fig, axes = plt.subplots(2, 1, figsize=(3.4, 6.3), sharex=True)

    for ax, jeu, titre in zip(axes, ["Twin", "Stanford"],
                               ["Twin-2K-500 (2,058 respondents)",
                                "Park et al. (1,052 agents)"]):
        sous = roc[roc["jeu"] == jeu]
        for predicteur, groupe in sous.groupby("predicteur"):
            cle = PREDICTEUR_A_CLE.get((jeu, predicteur))
            if cle is None:
                continue  # predicteur non prevu dans la figure, on ne l'invente pas
            # tri par fpr puis tpr, puis enveloppe monotone (cummax) : les CSV source
            # contiennent des points a fpr identique (ex ties a fpr=0) dans un ordre non
            # trie sur tpr, ce qui cree un zigzag visuel sans signification si on relie
            # les points bruts. La courbe ROC correcte est l'enveloppe superieure
            # (tpr max atteignable a fpr donne ou en-deca) ; aucune valeur n'est modifiee,
            # seul l'ordre de tracé est corrige.
            groupe = groupe.sort_values(["fpr", "tpr"])
            x = _floor_fpr(groupe["fpr"].to_numpy())
            y = np.maximum.accumulate(groupe["tpr"].to_numpy())
            st = STYLES_F1[cle]
            ax.plot(x, y, linestyle=st["ls"], marker=st["marker"], lw=st["lw"],
                     ms=st["ms"], color=st["color"], label=st["label"],
                     markerfacecolor=st["color"], markeredgecolor=st["color"])

        # lignes reperes FPR = 0.1% et 1%, TPR annote pour le meilleur jumeau/agent
        # (attaque naive) et pour l'attaquant fort (A-LLR, hors pli)
        ligne_res = resume[resume["jeu"] == jeu]
        ligne_fort = fort[fort["jeu"] == JEU_ATTAQUANT_FORT[jeu]]
        for fpr_repere, colonne in [(0.001, "tpr_fpr_0_1pct"), (0.01, "tpr_fpr_1pct")]:
            ax.axvline(fpr_repere, color="0.6", lw=0.7, ls=(0, (1, 1)), zorder=0)
            ligne_meilleur = ligne_res[ligne_res["predicteur"].isin(
                ["Meilleur jumeau (JSON Persona GPT4.1)", "Meilleur agent (composite)"])]
            if not ligne_meilleur.empty:
                tpr_val = float(ligne_meilleur[colonne].iloc[0])
                ax.annotate(f"{tpr_val * 100:.1f}%", xy=(fpr_repere, tpr_val),
                             xytext=(-3, 7), textcoords="offset points", fontsize=6.0,
                             color="0.25", ha="right", clip_on=False)
            if not ligne_fort.empty:
                tpr_fort = float(ligne_fort[colonne].iloc[0])
                ax.annotate(f"{tpr_fort * 100:.1f}%", xy=(fpr_repere, tpr_fort),
                             xytext=(9, 1), textcoords="offset points", fontsize=6.0,
                             color="black", fontweight="bold", ha="left", va="center",
                             clip_on=False)

        # attaquant fort : deux points mesures (0,1 % et 1 % de FPR), aucune ligne --
        # relier deux seuils par un trait inventerait une forme de courbe jamais
        # mesuree entre eux (cf. docstring du module). Pas de barre d'erreur : les
        # colonnes tpr_fpr_*_bas/haut n'existent pas dans c7-attaquant-fort.csv.
        if not ligne_fort.empty:
            xf = [0.001, 0.01]
            yf = [float(ligne_fort["tpr_fpr_0_1pct"].iloc[0]),
                  float(ligne_fort["tpr_fpr_1pct"].iloc[0])]
            ax.scatter(xf, yf, marker=STYLE_FORT["marker"], s=STYLE_FORT["ms"] ** 2,
                       color=STYLE_FORT["color"], edgecolor="white", linewidth=0.5,
                       label=STYLE_FORT["label"], zorder=4)

        ax.set_xscale("log")
        ax.set_xlim(FPR_FLOOR, 1.0)
        ax.set_ylim(-0.02, 1.02)
        ax.set_title(titre, fontsize=9, loc="left")
        ax.grid(True, which="major", axis="both", color="0.85", lw=0.5, zorder=0)
        ax.set_ylabel("True positive rate")

    axes[-1].set_xlabel("False positive rate (log scale)")
    fig.subplots_adjust(top=0.90, bottom=0.20, hspace=0.30, left=0.17, right=0.97)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.55, 0.045))
    fig.suptitle("Open-world reidentification risk (ROC)", fontsize=9.5, y=0.965)
    fig.text(0.5, 0.006,
              "Strong attack (A-LLR, out-of-fold): 2 measured points per panel, no "
              "full ROC and no bootstrap CI in the source CSV.",
              fontsize=5.3, color="0.25", ha="center", va="bottom")

    chemin = os.path.join(FIGURES, "fig1-monde-ouvert.png")
    fig.savefig(chemin, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("ecrit :", chemin)


# ---------------------------------------------------------------------------
# Figure 2 : fidelite (imitation) vs fuite, nuage + encart nul de marge
# ---------------------------------------------------------------------------

DEMO_NOM = "Demographics Only - GPT4.1-mini"


def _style_point(groupe, nom):
    if nom == DEMO_NOM:
        return dict(marker="^", color="0.3", label="Demographics Only")
    if nom.startswith("humains"):
        return dict(marker="*", color="black", label="Human retest (ceiling)")
    if groupe == "statistique":
        return dict(marker="D", color="0.45", label="Statistical predictor")
    return dict(marker="o", color="black", label="LLM twin")


def figure2():
    points = pd.read_csv(os.path.join(RESULTATS, "c7-compromis-robustesse-points.csv"))
    nul = pd.read_csv(os.path.join(RESULTATS, "c7-disjoint-nul.csv"))
    resume = pd.read_csv(os.path.join(RESULTATS, "c7-disjoint-resume.csv"))
    # IC bootstrap de la fuite (top-1), 8 des 13 points depuis c7-reidentification.csv,
    # cible="humains vague 4" (verifie a 1e-9 pres contre fuite_top1) ; les 5 manquants
    # (les 4 temoins statistiques et le retest humain) et l'IC de fidelite pour les 13
    # points (jamais calcule avant) viennent de c7-ic-manquants.csv (meme convention de
    # bootstrap par personne, cf. analyses/c7_ic_manquants.py). Les deux axes ont
    # desormais un IC pour les 13 points.
    reid = pd.read_csv(os.path.join(RESULTATS, "c7-reidentification.csv"))
    reid_cible = reid[reid["cible"] == "humains vague 4"].set_index("configuration")
    ic_fuite = reid_cible[["top1", "top1_bas", "top1_haut"]].rename(
        columns={"top1": "point_central", "top1_bas": "ic_bas", "top1_haut": "ic_haut"})

    manquants = pd.read_csv(os.path.join(RESULTATS, "c7-ic-manquants.csv"))
    ic_fuite_manquante = manquants[manquants["axe"] == "fuite_top1"].set_index(
        "predicteur")[["point_central", "ic_bas", "ic_haut"]]
    ic_fuite = pd.concat([ic_fuite, ic_fuite_manquante])
    ic_fidelite = manquants[manquants["axe"] == "fidelite_plancher"].set_index(
        "predicteur")[["point_central", "ic_bas", "ic_haut"]]

    fig, ax = plt.subplots(figsize=(3.4, 3.3))

    vus = set()
    n_avec_ic_y, n_avec_ic_x = 0, 0
    for _, r in points.iterrows():
        st = _style_point(r["groupe"], r["configuration"])
        lbl = st["label"] if st["label"] not in vus else None
        vus.add(st["label"])
        if r["configuration"] in ic_fuite.index:
            ligne_ic = ic_fuite.loc[r["configuration"]]
            assert abs(ligne_ic["point_central"] - r["fuite_top1"]) < 1e-8
            bas = r["fuite_top1"] - float(ligne_ic["ic_bas"])
            haut = float(ligne_ic["ic_haut"]) - r["fuite_top1"]
            ax.errorbar(r["fidelite_plancher"], r["fuite_top1"],
                         yerr=[[bas], [haut]], fmt="none", ecolor=st["color"],
                         elinewidth=0.8, capsize=2, capthick=0.8, zorder=2)
            n_avec_ic_y += 1
        if r["configuration"] in ic_fidelite.index:
            ligne_ic = ic_fidelite.loc[r["configuration"]]
            assert abs(ligne_ic["point_central"] - r["fidelite_plancher"]) < 1e-8
            gauche = r["fidelite_plancher"] - float(ligne_ic["ic_bas"])
            droite = float(ligne_ic["ic_haut"]) - r["fidelite_plancher"]
            ax.errorbar(r["fidelite_plancher"], r["fuite_top1"],
                         xerr=[[gauche], [droite]], fmt="none", ecolor=st["color"],
                         elinewidth=0.8, capsize=2, capthick=0.8, zorder=2)
            n_avec_ic_x += 1
        ax.scatter(r["fidelite_plancher"], r["fuite_top1"], marker=st["marker"],
                    s=42 if st["marker"] != "*" else 90, color=st["color"],
                    edgecolor="white", linewidth=0.4, label=lbl, zorder=3)
        if r["configuration"].startswith("humains"):
            ax.annotate("human retest", xy=(r["fidelite_plancher"], r["fuite_top1"]),
                         xytext=(-6, -10), textcoords="offset points", fontsize=6.3,
                         ha="right")
    print(f"figure2 : IC bootstrap tracees pour {n_avec_ic_y}/{len(points)} points "
          f"(fuite) et {n_avec_ic_x}/{len(points)} points (fidelite)")

    ax.set_xlabel("Imitation quality (fidelity, share of human floor)")
    ax.set_ylabel("Reidentification leakage (top-1 rate)")
    ax.set_title("Fidelity vs. leakage, 13 predictors", fontsize=9, loc="left")
    ax.grid(True, color="0.88", lw=0.5, zorder=0)
    ax.legend(loc="upper left", frameon=False, fontsize=6.6)

    # encart : rho observe (items disjoints) contre bande du nul de marge (5e-95e centile)
    rho_obs = float(resume["rho_disjoint_moyen"].iloc[0])
    bas5, haut95 = np.percentile(nul["rho_nul"], [5, 95])
    # position en fraction des axes principaux (pas de la figure) pour rester ancree
    # dans une zone du nuage sans point : fidelite 0.5-0.88, fuite ~0.25-0.53, vide
    # (LLM max fuite 0.21, humain a fuite 0.82 hors de cette zone).
    inset = ax.inset_axes([0.50, 0.30, 0.38, 0.32])
    inset.set_facecolor("white")
    inset.set_zorder(5)
    inset.axhspan(bas5, haut95, color="0.75", zorder=1)
    inset.scatter([0.5], [rho_obs], marker="o", color="black", s=22, zorder=3)
    inset.set_xlim(0, 1)
    inset.set_xticks([])
    inset.set_ylim(min(bas5, rho_obs) - 0.01, max(haut95, rho_obs) + 0.01)
    inset.set_ylabel("Spearman rho", fontsize=6.0, labelpad=1)
    inset.set_title("Margin-null band\n(disjoint items, 5th-95th pct)", fontsize=5.8,
                      pad=2)
    inset.tick_params(labelsize=5.6)
    for spine in inset.spines.values():
        spine.set_linewidth(0.6)

    fig.text(0.01, 0.005,
              "Error bars: 95% bootstrap CI, per-person resampling, both axes, "
              "all 13 predictors.",
              fontsize=5.3, color="0.25", ha="left", va="bottom")
    fig.tight_layout(rect=(0, 0.035, 1, 1))
    chemin = os.path.join(FIGURES, "fig2-couplage.png")
    fig.savefig(chemin, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("ecrit :", chemin)


if __name__ == "__main__":
    figure1()
    figure2()
