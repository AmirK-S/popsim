"""
figures_article : les deux figures du manuscrit (article/manuscrit.md).

Ne recalcule rien. Lit uniquement des CSV deja calcules dans resultats/ :
  - c7-monde-ouvert.csv, c7-monde-ouvert-roc.csv,
    c7-attaquant-fort.csv, c7-monde-ouvert-ic.csv,
    c7-fort-monde-ouvert-ic.csv                          -> figure 1
  - c7-compromis-robustesse-points.csv (13 points, dont le retest humain,
    superset de c7-compromis.csv), c7-nul-corrige.csv (point reel),
    c7-reidentification.csv, c7-ic-manquants.csv         -> figure 2
    (bande du temoin corrige : constantes chiffrees, cf. docstring figure 2
    ci-dessous -- aucun CSV de replicats verse au depot pour ce temoin)

Aucun appel de modele, aucun reseau. Etiquettes/axes/legendes en anglais,
lisibles en noir et blanc (formes + styles de trait distincts, la couleur est
un renfort optionnel jamais le seul signal). Sortie : article/figures/*.png
(300 dpi, taille colonne simple ~3.4 in de large).

Usage : .venv/bin/python analyses/figures_article.py

Donnees manquantes signalees ici (ne pas inventer, ne pas combler) :
  - Figure 1 : l'attaquant fort (A-LLR hors pli, analyses/c7_attaquant_fort.py) n'a
    ete evalue qu'a deux seuils de FPR (0,1 % et 1 %), jamais sur une courbe ROC
    complete : trace donc comme deux points isoles, sans ligne qui relierait des
    seuils intermediaires jamais mesures (regle non negociable, cf. figure). Les IC
    a 95 % (bootstrap (B), parametres re-estimes par pli pour l'attaque forte,
    cf. resultats/c7-fort-monde-ouvert-ic-2026-09-12.md ; seuil rejoue pour la
    naive, cf. resultats/c7-monde-ouvert-ic-2026-09-12.md) sont lus dans
    c7-fort-monde-ouvert-ic.csv / c7-monde-ouvert-ic.csv et affiches en barres
    d'erreur, seulement aux deux seuils reperes. A FPR = 0,1 %, le seuil ne repose
    que sur ~1-2 faux positifs absolus (marqueur evide) contre ~11-21 a 1 %
    (marqueur plein) : instabilite rendue visible, pas une mesure de meme qualite.
    Sur Twin, les IC de l'attaque forte et de la naive se chevauchent largement aux
    deux FPR (gain non etabli) ; sur Park ils ne se chevauchent pas (gain net).
  - Figure 2 : nul de marge, VERSION CORRIGEE le 12/09 (revue hostile
    resultats/revue-hostile-gel-2026-09-12.md, D1/D2 ; audit adverse
    resultats/audit-renversement-2026-09-12.md). Historique : la bande
    provenait de c7-disjoint-nul.csv / c7-disjoint-resume.csv (items
    disjoints, analyses/c7_disjoint.py::construire_nul), avec un defaut reel
    ligne 133 (les cellules fausses evitent la vraie modalite de la
    personne) qui gonflait la fuite du nul d'un facteur ~1,3 (top-1 41,2 %
    contre 31,6 % une fois les fausses valeurs retirees dans la marginale de
    population). Un renversement tente dans la nuit du 11 au 12/09
    (c7-nul-corrige.csv, 5 temoins qui apparient l'exactitude contre une
    CIBLE DE SUBSTITUTION) a ete audite et retire : ces 5 temoins detruisent
    l'exactitude contre la verite (0,41-0,44 contre 0,53 pour le reel) et ne
    prouvent rien. L'audit a construit, lui, le temoin qui manquait --
    exactitude EXACTE contre la verite par personne, positions tirees au
    hasard, cellules fausses tirees dans la marginale de population de
    l'item (script scratchpad audit_contre_nul.py, non verse au depot ; run
    en avant-plan le 12/09 pour cette figure, 20 replicats x 12
    configurations, ~130 s, meme graine que l'audit -> rho moyen 0,9741,
    mediane 0,9720, p5 0,9500, p95 0,9934, reproduit a l'identique les
    chiffres de resultats/audit-renversement-2026-09-12.md §1.3). C'est ce
    temoin, et non plus le nul d'origine ni les 5 temoins retires, qui est
    desormais publie ici et dans le texte du §5.1 (rho 0,974 [0,950 ; 0,993]
    contre 0,965 observe). Ni ce temoin ni le reel n'ont de CSV de replicats
    verse au depot : la bande [BANDE_P5, BANDE_P95] et le point rho_obs
    ci-dessous sont donc des CONSTANTES chiffrees dans ce fichier, sourcees
    au run ci-dessus et a resultats/audit-renversement-2026-09-12.md (bande)
    et a c7-nul-corrige.csv, ligne rho_resume/reel (point, 0,965034965...,
    memes 12 configurations/memes items que le temoin, "items entiers" et
    non disjoints -- d'ou l'ecart avec le 0,969 historique sur items
    disjoints, note heritee D7 de l'audit). Le point continue de tomber DANS
    la bande : la prediction (b) reste refutee, le verdict visuel ne change
    pas. Ce temoin n'est pas non plus depourvu de structure individuelle
    (31,6 % de top-1 une fois apparie sur l'exactitude, contre 20,73 % /
    3,56 bits pour le jumeau reel et 0,049 % pour le hasard pur) ; AUCUNE
    source ne donne de bits pour la mesure a 31,6 % (le 4,63 bits qui
    circulait est celui de l'ancienne mesure a 31,15 %, abandonnee -- cf.
    resultats/audit-chiffres-2026-09-12.md) : ce chiffre de bits est donc
    volontairement absent de la legende. Toute formulation "aucune structure
    individuelle" serait fausse et n'est plus utilisee. Pas de bande
    spatiale (x,y) : on ne dispose que d'une distribution de rho global, pas
    d'une fuite simulee par predicteur/point.
    A CORRIGER COTE MANUSCRIT, PAS ICI (signale, non traite par ce script) :
    §5.1 n'appelle jamais "Figure 2" -- la figure reste orpheline tant que
    le texte ne la cite pas explicitement (revue hostile D2).
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

# Figure 2, encart : temoin de marge CORRIGE (exactitude exacte contre la verite par
# personne, positions au hasard, cellules fausses tirees dans la marginale de population
# de l'item). Aucun CSV de replicats n'est verse au depot pour ce temoin -- seules des
# statistiques agregees existent, sourcees a resultats/audit-renversement-2026-09-12.md
# §1.3 et reproduites a l'identique le 12/09 en avant-plan (scratchpad audit_contre_nul.py,
# 20 replicats x 12 configurations, meme graine : rho moyen 0.9741, mediane 0.9720,
# p5 0.9500, p95 0.9934, min 0.9301, max 1.0000). D'ou des CONSTANTES, pas une colonne
# de CSV chargee dynamiquement.
NUL_CORRIGE_P5 = 0.9500
NUL_CORRIGE_P95 = 0.9934
NUL_CORRIGE_MOYEN = 0.9741


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
# entre eux). Marqueur plein noir pour rester net en noir et blanc ; evide (blanc) a
# FPR = 0,1 % pour signaler un seuil cale sur ~1-2 faux positifs seulement (cf. legende).
STYLE_FORT = dict(marker="D", ms=4.8, color="black",
                   label="Strong attack (A-LLR), 0.1%/1% FPR only (95% CI)")

# Reperes FPR = 0,1 % et 1 % : colonnes du point et de l'IC bootstrap a lire dans
# c7-monde-ouvert-ic.csv (naive, seuil rejoue) et c7-fort-monde-ouvert-ic.csv (fort,
# bootstrap (B) re-estime -- celui recommande par le rapport, cf. docstring). evide=True
# marque le seuil FPR=0,1 % (~1-2 FP absolus), le plus instable des deux.
REPERES_F1 = [
    (0.001, dict(naif_pt="tpr_0_1pct", naif_bas="tpr_0_1pct_ic_bas_seuil_rejoue",
                 naif_haut="tpr_0_1pct_ic_haut_seuil_rejoue",
                 fort_pt="tpr_0_1pct_fort", fort_bas="tpr_0_1pct_fort_ic_bas_reestime",
                 fort_haut="tpr_0_1pct_fort_ic_haut_reestime", evide=True)),
    (0.01, dict(naif_pt="tpr_1pct", naif_bas="tpr_1pct_ic_bas_seuil_rejoue",
                naif_haut="tpr_1pct_ic_haut_seuil_rejoue",
                fort_pt="tpr_1pct_fort", fort_bas="tpr_1pct_fort_ic_bas_reestime",
                fort_haut="tpr_1pct_fort_ic_haut_reestime", evide=False)),
]

NOMS_MEILLEUR = ["Meilleur jumeau (JSON Persona GPT4.1)", "Meilleur agent (composite)"]

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
    # Points + IC a 95 % lus dans les CSV dedies (cf. docstring) : source de verite
    # pour les deux seuils reperes (0,1 % et 1 %), naive et forte.
    ic_naif = pd.read_csv(os.path.join(RESULTATS, "c7-monde-ouvert-ic.csv"))
    ic_fort = pd.read_csv(os.path.join(RESULTATS, "c7-fort-monde-ouvert-ic.csv"))

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

        # reperes FPR = 0,1 % et 1 % : point + IC a 95 % (bootstrap), pour le meilleur
        # jumeau/agent (attaque naive, seuil rejoue) et pour l'attaquant fort (A-LLR,
        # hors pli, bootstrap (B) re-estime). Deux points mesures pour l'attaquant
        # fort, aucune ligne entre eux -- relier deux seuils inventerait une forme de
        # courbe jamais mesuree (cf. docstring du module). Marqueur evide (blanc) a
        # FPR = 0,1 % : seuil cale sur ~1-2 faux positifs absolus seulement, contre
        # ~11-21 a FPR = 1 % (marqueur plein) -- instabilite rendue visible, pas une
        # mesure de meme qualite.
        ligne_naif_jeu = ic_naif[(ic_naif["jeu"] == jeu) &
                                  (ic_naif["predicteur"].isin(NOMS_MEILLEUR))]
        ligne_fort_jeu = ic_fort[ic_fort["jeu"] == jeu]
        st_meilleur = STYLES_F1["meilleur"]
        xf, yf = [], []
        for fpr_repere, cols in REPERES_F1:
            ax.axvline(fpr_repere, color="0.6", lw=0.7, ls=(0, (1, 1)), zorder=0)
            face_naif = "white" if cols["evide"] else st_meilleur["color"]
            face_fort = "white" if cols["evide"] else STYLE_FORT["color"]

            if not ligne_naif_jeu.empty:
                r = ligne_naif_jeu.iloc[0]
                y = float(r[cols["naif_pt"]])
                lo = float(r[cols["naif_bas"]])
                hi = float(r[cols["naif_haut"]])
                ax.errorbar([fpr_repere], [y], yerr=[[max(y - lo, 0)], [max(hi - y, 0)]],
                             fmt=st_meilleur["marker"], ms=st_meilleur["ms"] + 1.2,
                             color=st_meilleur["color"], markerfacecolor=face_naif,
                             markeredgecolor=st_meilleur["color"], mew=0.8,
                             elinewidth=0.9, capsize=2.2, zorder=4)
                # CORRECTIF (relecture de rendu 2026-09-13, defaut 2) : sur le
                # panneau Twin, les quatre reperes (naif/fort x 0,1 %/1 %)
                # tombent tous a moins de 0,05 en TPR -- l'ancien decalage
                # oblique ("au-dessus a gauche" pour le naif, "a droite, meme
                # hauteur" pour le fort) faisait se chevaucher le naif d'un
                # repere et le fort du repere voisin, les deux etiquettes
                # visant le meme espace etroit entre les deux reperes.
                # Desormais : le naif reste au-dessus de SON marqueur (centre
                # dessus, sans reach lateral vers le repere voisin) ; le fort
                # (ci-dessous) passe en diagonale bas-droite, qui degage a la
                # fois le naif du meme repere (au-dessus) et l'erreur-bar
                # verticale du fort lui-meme (cf. commentaire plus bas -- sur
                # Park, cette barre est large et une etiquette juste EN
                # DESSOUS la traverserait). Aucune donnee/valeur affichee
                # n'est modifiee, seul l'emplacement du texte change ; verifie
                # par rendu d'image sur les deux panneaux (Twin serre, Park
                # large, IC etroites et larges).
                ax.annotate(f"{y * 100:.1f}%", xy=(fpr_repere, y),
                             xytext=(0, 9), textcoords="offset points", fontsize=6.0,
                             color="0.25", ha="center", va="bottom", clip_on=False)

            if not ligne_fort_jeu.empty:
                r = ligne_fort_jeu.iloc[0]
                y = float(r[cols["fort_pt"]])
                lo = float(r[cols["fort_bas"]])
                hi = float(r[cols["fort_haut"]])
                xf.append(fpr_repere)
                yf.append(y)
                ax.errorbar([fpr_repere], [y], yerr=[[max(y - lo, 0)], [max(hi - y, 0)]],
                             fmt="none", ecolor=STYLE_FORT["color"], elinewidth=0.9,
                             capsize=2.2, zorder=4)
                ax.scatter([fpr_repere], [y], marker=STYLE_FORT["marker"],
                           s=STYLE_FORT["ms"] ** 2, color=STYLE_FORT["color"],
                           facecolor=face_fort, edgecolor=STYLE_FORT["color"],
                           linewidth=0.8, zorder=5)
                # CORRECTIF (relecture de rendu 2026-09-13, defaut 2) : decalage
                # diagonal bas-droite (pas juste "en dessous") -- sur le
                # panneau Park, l'IC bootstrap du repere 0,1 % est large
                # (0,233-0,538, soit ~0,30 de TPR) : une etiquette placee
                # directement sous le marqueur retombait en plein sur la
                # barre d'erreur verticale. Le decalage horizontal degage la
                # barre d'erreur ; le decalage vertical (sous le marqueur, pas
                # a cote) degage l'etiquette naive du meme repere, restee
                # au-dessus. Verifie par rendu d'image sur les deux panneaux.
                ax.annotate(f"{y * 100:.1f}%", xy=(fpr_repere, y),
                             xytext=(7, -9), textcoords="offset points", fontsize=6.0,
                             color="black", fontweight="bold", ha="left", va="top",
                             clip_on=False)

        # entree de legende unique pour l'attaquant fort (les scatter ci-dessus ont
        # deja trace les deux points ; celui-ci ne sert qu'a fabriquer le pictogramme
        # de legende, hors axes)
        if xf:
            ax.scatter([], [], marker=STYLE_FORT["marker"], s=STYLE_FORT["ms"] ** 2,
                       color=STYLE_FORT["color"], edgecolor=STYLE_FORT["color"],
                       linewidth=0.8, label=STYLE_FORT["label"])

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
              "Error bars: 95% bootstrap CI (naive: threshold re-drawn each trial; "
              "strong attack: A-LLR re-fit per fold, n=300).\n"
              "Open marker = FPR 0.1% (~1-2 abs. FP, n=2058/1052); filled = FPR 1% "
              "(~11-21 FP). No interpolation between points.\n"
              "Twin: strong-vs-naive 95% CIs overlap widely at both FPR (gain not "
              "established). Park: no overlap (gain robust).",
              fontsize=4.8, color="0.25", ha="center", va="bottom", linespacing=1.3)

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

    # encart : rho observe contre la bande du temoin de marge CORRIGE (5e-95e centile).
    # Temoin corrige = exactitude EXACTE contre la verite par personne (et donc par
    # configuration), positions tirees au hasard, cellules fausses tirees dans la
    # marginale de population de l'item -- pas le nul d'origine (defaut ligne 133 de
    # analyses/c7_disjoint.py) ni les 5 temoins a cible de substitution retires apres
    # audit (cf. docstring du module et resultats/audit-renversement-2026-09-12.md).
    # Bande [NUL_CORRIGE_P5, NUL_CORRIGE_P95] : constantes chiffrees (voir module,
    # pas de CSV de replicats verse au depot). Point = rho reel sur les memes 12
    # configurations/items que le temoin ("items entiers"), lu dans c7-nul-corrige.csv
    # (ligne rho_resume/reel) -- distinct du 0,969 historique sur items disjoints. La
    # bande recouvre toujours le point observe : la prediction (b) reste refutee.
    nul_corrige = pd.read_csv(os.path.join(RESULTATS, "c7-nul-corrige.csv"))
    ligne_reelle = nul_corrige[(nul_corrige["type"] == "rho_resume")
                                & (nul_corrige["construction"] == "reel")].iloc[0]
    rho_obs = float(ligne_reelle["rho_moyen"])
    bas5, haut95 = NUL_CORRIGE_P5, NUL_CORRIGE_P95
    assert abs(rho_obs - 0.9650) < 1e-3 and bas5 < rho_obs < haut95

    # position en fraction des axes principaux (pas de la figure) pour rester ancree
    # dans une zone du nuage sans point : fidelite 0.5-0.88, fuite ~0.25-0.53, vide
    # (LLM max fuite 0.21, humain a fuite 0.82 hors de cette zone).
    inset = ax.inset_axes([0.50, 0.30, 0.38, 0.32])
    inset.set_facecolor("white")
    inset.set_zorder(5)
    inset.axhspan(bas5, haut95, color="0.75", zorder=1,
                   label="corrected margin null, 5th-95th pct (truth-matched accuracy)")
    inset.scatter([0.5], [rho_obs], marker="o", color="black", s=22, zorder=3,
                   label="observed rho")
    inset.set_xlim(0, 1)
    inset.set_xticks([])
    inset.set_ylim(min(bas5, rho_obs) - 0.01, max(haut95, rho_obs) + 0.01)
    inset.set_ylabel("Spearman rho", fontsize=6.0, labelpad=1)
    inset.set_title("Corrected margin-null band\n(truth-matched accuracy, 5th-95th pct)",
                      fontsize=5.8, pad=2)
    inset.tick_params(labelsize=5.6)
    for spine in inset.spines.values():
        spine.set_linewidth(0.6)

    fig.text(0.01, 0.005,
              "Error bars: 95% bootstrap CI, per-person resampling, both axes, all 13 "
              "predictors. Inset: CORRECTED margin null (audit-renversement-2026-09-12.md) "
              "-- truth-matched per-person accuracy, false cells from the population "
              "marginal, not the original disjoint-item null (c7_disjoint.py l.133 "
              "inflated its leakage ~1.3x, 41.2% vs 31.6% top-1) nor the 5 withdrawn "
              "substitute-target witnesses. Band [0.950, 0.993] still covers the observed "
              "rho=0.965 (12 configs, vs. the historical 0.969 on disjoint items): "
              "verdict unchanged. Leaks 31.6% top-1 (no bits reported for this figure) "
              "vs 20.73% / 3.56 bits for the real twin and 0.049% for chance.",
              fontsize=4.7, color="0.25", ha="left", va="bottom", wrap=True)
    fig.tight_layout(rect=(0, 0.145, 1, 1))
    chemin = os.path.join(FIGURES, "fig2-couplage.png")
    fig.savefig(chemin, dpi=300, bbox_inches="tight")
    plt.close(fig)
    print("ecrit :", chemin)


if __name__ == "__main__":
    figure1()
    figure2()
