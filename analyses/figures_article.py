"""
figures_article : les deux figures du manuscrit (article/manuscrit.md).

Ne recalcule rien. Lit uniquement des CSV deja calcules dans resultats/ :
  - c7-monde-ouvert.csv, c7-monde-ouvert-roc.csv       -> figure 1
  - c7-compromis-robustesse-points.csv (13 points, dont le retest humain,
    superset de c7-compromis.csv), c7-disjoint-nul.csv,
    c7-disjoint-resume.csv                              -> figure 2

Aucun appel de modele, aucun reseau. Etiquettes/axes/legendes en anglais,
lisibles en noir et blanc (formes + styles de trait distincts, la couleur est
un renfort optionnel jamais le seul signal). Sortie : article/figures/*.png
(300 dpi, taille colonne simple ~3.4 in de large).

Usage : .venv/bin/python analyses/figures_article.py

Donnees manquantes signalees ici (ne pas inventer, ne pas combler) :
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
    "meilleur": dict(ls="-", marker="o", lw=1.6, ms=3.2, color="black",
                      label="Best twin/agent"),
    "demo": dict(ls="--", marker="s", lw=1.1, ms=2.6, color="0.35",
                  label="Demographics Only"),
    "pmm": dict(ls=":", marker="^", lw=1.1, ms=2.6, color="0.4",
                 label="PMM k=10"),
    "humain": dict(ls="-.", marker="", lw=1.6, ms=0, color="0.1",
                     label="Human retest (ceiling)"),
}

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


def figure1():
    roc = pd.read_csv(os.path.join(RESULTATS, "c7-monde-ouvert-roc.csv"))
    resume = pd.read_csv(os.path.join(RESULTATS, "c7-monde-ouvert.csv"))

    fig, axes = plt.subplots(2, 1, figsize=(3.4, 5.6), sharex=True)

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
        ligne_res = resume[resume["jeu"] == jeu]
        for fpr_repere, colonne in [(0.001, "tpr_fpr_0_1pct"), (0.01, "tpr_fpr_1pct")]:
            ax.axvline(fpr_repere, color="0.6", lw=0.7, ls=(0, (1, 1)), zorder=0)
            ligne_meilleur = ligne_res[ligne_res["predicteur"].isin(
                ["Meilleur jumeau (JSON Persona GPT4.1)", "Meilleur agent (composite)"])]
            if not ligne_meilleur.empty:
                tpr_val = float(ligne_meilleur[colonne].iloc[0])
                ax.annotate(f"{tpr_val * 100:.1f}%", xy=(fpr_repere, tpr_val),
                             xytext=(2, 4), textcoords="offset points", fontsize=6.3,
                             color="black")

        ax.set_xscale("log")
        ax.set_xlim(FPR_FLOOR, 1.0)
        ax.set_ylim(-0.02, 1.02)
        ax.set_title(titre, fontsize=9, loc="left")
        ax.grid(True, which="major", axis="both", color="0.85", lw=0.5, zorder=0)
        ax.set_ylabel("True positive rate")

    axes[-1].set_xlabel("False positive rate (log scale)")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", ncol=2, frameon=False,
               bbox_to_anchor=(0.55, -0.02))
    fig.suptitle("Open-world reidentification risk (ROC)", fontsize=9.5, y=0.995)
    fig.tight_layout(rect=(0, 0.06, 1, 0.97))

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

    fig, ax = plt.subplots(figsize=(3.4, 3.3))

    vus = set()
    for _, r in points.iterrows():
        st = _style_point(r["groupe"], r["configuration"])
        lbl = st["label"] if st["label"] not in vus else None
        vus.add(st["label"])
        ax.scatter(r["fidelite_plancher"], r["fuite_top1"], marker=st["marker"],
                    s=42 if st["marker"] != "*" else 90, color=st["color"],
                    edgecolor="white", linewidth=0.4, label=lbl, zorder=3)
        if r["configuration"].startswith("humains"):
            ax.annotate("human retest", xy=(r["fidelite_plancher"], r["fuite_top1"]),
                         xytext=(-6, -10), textcoords="offset points", fontsize=6.3,
                         ha="right")

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

    fig.tight_layout()
    chemin = os.path.join(FIGURES, "fig2-couplage.png")
    fig.savefig(chemin, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("ecrit :", chemin)


if __name__ == "__main__":
    figure1()
    figure2()
