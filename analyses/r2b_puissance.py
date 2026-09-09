"""
r2b_puissance : puissance de R2, ponts entre modeles et entre regimes, et figure.

Complement de lecture de `analyses/r2_evaluer.py`. AUCUN SCRIPT EXISTANT N'EST MODIFIE et
aucun fichier existant n'est reecrit : toutes les sorties portent le prefixe `r2b-`. Zero
appel de modele de langage, lecture seule sur data/traces/.

Ce que ce script ajoute a r2_evaluer, et qui n'y est pas :

  1. LA PUISSANCE. r2_evaluer rend les intervalles ; il ne dit pas combien de personnes il
     faudrait pour que les contrastes de la famille primaire soient decidables. Ici, pour
     chaque contraste de F1, l'ecart type de bootstrap apparie, le z observe, le z exige
     par Holm sur une famille de 7 tests, et l'effectif de personnes qu'il faudrait a
     effet constant (mise a l'echelle en 1/racine(n), donc une ESTIMATION, pas une mesure).
     Plus le plus petit effet detectable a n constant.

  2. LE PONT AVEC LE PETIT MODELE. Les memes mesures de rarete stable pour C3F gpt-oss-20b
     et C3F Qwen3-4B RESTREINTES AUX PERSONNES COMMUNES, avec les six methodes du regime
     severe restreintes aux memes personnes : la question « le gros modele reduit il
     l'ecart avec la statistique ? » ne se lit que sur ce perimetre la.

  3. LE COUT DU RETRAIT DE LA FAMILLE POUR LE MODELE DE 20 MILLIARDS. C3 moins C3F sur les
     personnes communes aux deux traces gpt-oss, exactitude et rappel des raretes stables,
     a comparer aux moins 6,24 points d'exactitude que a33 mesure sur Qwen3-4B.

  4. LA FIGURE : rappel et precision des raretes stables, C3F gpt-oss contre les six
     methodes du regime severe, plancher de segment en pointille.

Entree  : les memes traces et caches que r2_evaluer.
Sortie  : resultats/r2b-puissance.csv, r2b-pont-modeles.csv, r2b-pont-regimes.csv,
          r2b-cellules-par-personne.csv, r2b-figure-rares.png et .svg

Usage : .venv/bin/python analyses/r2b_puissance.py --tirages 4000
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import a41_commun as C41
import a42_commun as C42
import r2_evaluer as R2
from a5_agents_locaux_gss import nomenclature

SORTIE = C41.SORTIE

FOND = "#fcfcfb"
ENCRE = "#0b0b0b"
ENCRE_SECONDE = "#52514e"
GRILLE = "#e2e1dd"
LLM = "#c8412b"
STAT_TIRAGE = "#2a78d6"
STAT_ESPERANCE = "#8d8b86"
HUMAIN = "#1f7a45"

# Les six methodes du regime severe, dans l'ordre de a41, plus le repere humain.
ORDRE = ["E1 famille retiree (argmax)", "E2 famille retiree (tirage)",
         "PMM k=10 famille retiree", "IM m=10 mode, famille retiree",
         "B2 famille retiree (argmax)", "B2 famille retiree (tirage)"]

# Nature de chaque methode, pour que la lecture ne repose pas sur la couleur seule.
NATURE = {
    "E1 famille retiree (argmax)": "esperance",
    "IM m=10 mode, famille retiree": "esperance",
    "B2 famille retiree (argmax)": "esperance",
    "E2 famille retiree (tirage)": "tirage",
    "PMM k=10 famille retiree": "tirage",
    "B2 famille retiree (tirage)": "tirage",
}

COURT = {
    "E1 famille retiree (argmax)": "E1 regression, argmax",
    "E2 famille retiree (tirage)": "E2 regression, tirage",
    "PMM k=10 famille retiree": "PMM k=10",
    "IM m=10 mode, famille retiree": "IM m=10, mode",
    "B2 famille retiree (argmax)": "B2 argmax",
    "B2 famille retiree (tirage)": "B2 tirage",
}


def style(ax):
    ax.set_facecolor(FOND)
    ax.grid(True, axis="x", color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(GRILLE)
    ax.tick_params(colors=ENCRE_SECONDE, labelsize=9)


def dist_contraste(ra, rb, idx):
    """Distribution bootstrap appariee de la difference de rappel, methode a moins b.

    Memes tirages de personnes pour les deux methodes : c'est ce qui rend le contraste
    apparie. Les couples (numerateur, denominateur) par personne viennent de
    a42_commun.mesure_sur, importe tel quel par r2_evaluer.
    """
    na, da = ra["_rappel"]
    nb, db = rb["_rappel"]
    sa, sda = na[idx].sum(1), da[idx].sum(1)
    sb, sdb = nb[idx].sum(1), db[idx].sum(1)
    ok = (sda > 0) & (sdb > 0)
    return (sa[ok] / sda[ok]) - (sb[ok] / sdb[ok])


def z_exige(m, alpha=0.05):
    """z unilateral exige par Holm pour le test le plus severe d'une famille de m tests.

    Holm compare le plus petit p a alpha / m. C'est la barre que doit franchir un
    contraste isole dans une famille de m, et c'est la barre la plus exigeante ; un
    contraste classe deuxieme n'a besoin que de alpha / (m - 1). On publie la plus
    exigeante, ce qui rend l'effectif exige conservateur.
    """
    from scipy.stats import norm
    return float(norm.isf(alpha / m))


def bloc_structure(paquet, lignes, colonnes, noms):
    """Exactitude, diversite conservee et ratios sur un perimetre de personnes.

    Meme chaine que r2_evaluer.mesures_structure, appelee ici sur un perimetre commun a
    deux conditions : c'est la seule facon de comparer la dispersion de deux modeles sans
    melanger un effet de modele et un effet d'echantillon.
    """
    import a28_commun as C28
    seg_tous, _ = C28.segments(paquet["x"], paquet["attributs"])
    seg = seg_tous[C41.AXE_PRINCIPAL][lignes]
    items, options = paquet["items"], paquet["options"]
    k_max_nom = max(len(options[it]) for it in items)
    codes_nom = {"_humains": C28.coder(paquet["y1"], lignes, items, options)}
    for nom in noms:
        codes_nom[nom] = C28.coder(paquet["M"][nom], lignes, items, options)
    brut = {"_humains": paquet["y1"][lignes]}
    brut.update({nom: paquet["M"][nom][lignes] for nom in noms})
    codes_lib, k_max_lib = C41.codes_libres(brut, colonnes)
    out = {}
    for nom in noms:
        out[nom] = R2.mesures_structure(paquet, nom, lignes, colonnes, codes_nom,
                                        codes_lib, seg, k_max_nom, k_max_lib)
        out[nom].pop("acc", None)
    return out


def bloc_rares(paquet, refs, lignes, nom_llm, colonnes, idx):
    """Rappel, precision, exces et distributions bootstrap sur un perimetre de personnes."""
    prep = R2.preparer(paquet, lignes, refs, "perimetre")
    noms = [nom_llm] + [m for m in ORDRE if m in paquet["M"]] + ["humains vague 2"]
    out = {}
    for nom in noms:
        if nom not in paquet["M"] and nom != nom_llm:
            continue
        out[nom] = R2.mesures_rares(paquet["M"][nom][lignes], prep, colonnes, "stable")
    return prep, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--cache-a41", default="/tmp/a41-severe.pkl")
    ap.add_argument("--tirages", type=int, default=4000)
    ap.add_argument("--suffixe", default="")
    args = ap.parse_args()

    print("chargement du paquet et des six methodes du regime severe", flush=True)
    paquet = C41.charger_paquet(args.cache, args.cache_foret, args.cache_a35)
    C41.construire_severe(paquet, cache=args.cache_a41)
    colonnes, familles = C41.colonnes_familles(paquet["items"])
    refs = R2.references_population(paquet)
    table = nomenclature()

    infos = {}
    for nom_llm, fichier, condition in R2.TRACES_R2:
        chemin = os.path.join(R2.DOSSIER_TRACES, fichier)
        info = R2.matrice_depuis_trace(paquet, chemin, condition, table, len(colonnes))
        if info is None:
            print(f"  trace absente ou vide : {chemin}")
            continue
        paquet["M"][nom_llm] = info["matrice"]
        infos[nom_llm] = info
        print(f"  {nom_llm} : {len(info['personnes'])} personnes completes, "
              f"{info['appels']} appels")

    principal = "C3F gpt-oss-20b"
    if principal not in infos:
        raise SystemExit("la trace C3F gpt-oss est absente : rien a mesurer")

    # ------------------------------------------------------------------ 1. puissance
    lignes = infos[principal]["lignes"]
    n = len(lignes)
    rng = np.random.default_rng(C41.GRAINE_A41)
    idx = C41.tirages(n, args.tirages, rng)
    prep, rares = bloc_rares(paquet, refs, lignes, principal, colonnes, idx)

    # cellules rares stables par personne : c'est le denominateur reel du rappel
    _, den = rares[principal]["_rappel"]
    par_pers = den.astype(int)
    cpp = pd.DataFrame({
        "condition": principal, "personnes": n,
        "cellules_rares_stables_total": int(par_pers.sum()),
        "personnes_sans_aucune_cellule": int((par_pers == 0).sum()),
        "mediane_par_personne": float(np.median(par_pers)),
        "moyenne_par_personne": float(par_pers.mean()),
        "max_par_personne": int(par_pers.max()),
        "attendu_par_a42_sur_150": 78.0,
    }, index=[0])

    zh = z_exige(7)          # famille F1, 7 tests, Holm, le plus severe
    z95 = 1.959963985
    puiss = []
    # H1a, l'exces sur le plancher de segment
    num_e, den_e = rares[principal]["_exces_segment"]
    v, lo, hi, tir_exces = C42.taux_ic(num_e, den_e, idx)
    se = float(np.std(tir_exces, ddof=1))
    puiss.append({"hypothese": "H1a", "adversaire": "plancher de segment",
                  "effet": v, "ic_bas": lo, "ic_haut": hi, "ecart_type_bootstrap": se})
    for m in ORDRE:
        if m not in rares:
            continue
        d = dist_contraste(rares[principal], rares[m], idx)
        na, da = rares[principal]["_rappel"]
        nb, db = rares[m]["_rappel"]
        pt = float(na.sum() / da.sum() - nb.sum() / db.sum())
        puiss.append({"hypothese": "H1b", "adversaire": m, "effet": pt,
                      "ic_bas": float(np.percentile(d, 2.5)),
                      "ic_haut": float(np.percentile(d, 97.5)),
                      "ecart_type_bootstrap": float(np.std(d, ddof=1))})
    puiss = pd.DataFrame(puiss)
    puiss["personnes"] = n
    puiss["z_observe"] = puiss["effet"] / puiss["ecart_type_bootstrap"]
    puiss["z_exige_holm_7"] = zh
    # effet minimal detectable a n constant, sous Holm et sous un IC 95 simple
    puiss["plus_petit_effet_detectable_holm"] = zh * puiss["ecart_type_bootstrap"]
    puiss["plus_petit_effet_detectable_ic95"] = z95 * puiss["ecart_type_bootstrap"]
    # effectif exige, a effet constant, mise a l'echelle en 1/racine(n) : ESTIMATION
    ratio = (zh / puiss["z_observe"].abs()) ** 2
    puiss["personnes_exigees_holm"] = np.ceil(n * ratio)
    puiss["personnes_exigees_ic95"] = np.ceil(n * (z95 / puiss["z_observe"].abs()) ** 2)
    puiss["signe_observe"] = np.where(puiss["effet"] >= 0, "en faveur du jumeau",
                                      "contre le jumeau")
    C41.ecrire(puiss, f"r2b-puissance{args.suffixe}.csv")
    C41.ecrire(cpp, f"r2b-cellules-par-personne{args.suffixe}.csv")

    # ------------------------------------------- 2. pont avec le petit modele, 60 communes
    ponts = []
    petit = "C3F Qwen3-4B"
    if petit in infos:
        communes = np.array(sorted(set(lignes.tolist())
                                   & set(infos[petit]["lignes"].tolist())))
        rngc = np.random.default_rng(C41.GRAINE_A41)
        idxc = C41.tirages(len(communes), args.tirages, rngc)
        prepc = R2.preparer(paquet, communes, refs, "perimetre")
        noms = [principal, petit] + [m for m in ORDRE if m in paquet["M"]] \
            + ["humains vague 2"]
        rc = {nom: R2.mesures_rares(paquet["M"][nom][communes], prepc, colonnes,
                                    "stable") for nom in noms}
        acc = {nom: C41.exactitude(paquet["M"][nom], paquet["y1"], communes, colonnes)
               for nom in noms}
        stru = bloc_structure(paquet, communes, colonnes, noms)
        for nom in noms:
            r = rc[nom]
            vr, lor, hir, _ = C42.taux_ic(r["_rappel"][0], r["_rappel"][1], idxc)
            vp, lop, hip, _ = C42.taux_ic(r["_precision"][0], r["_precision"][1], idxc)
            ve, loe, hie, _ = C42.taux_ic(r["_exces_segment"][0], r["_exces_segment"][1],
                                          idxc)
            ponts.append({
                "perimetre": f"{len(communes)} personnes communes C3F gpt-oss et C3F Qwen3-4B",
                "methode": nom, "cellules_rares_stables": r["cellules"],
                "raretes_osees": r["raretes_osees"],
                "exactitude": float(np.nanmean(acc[nom])),
                "diversite_conservee": stru[nom]["diversite"],
                "ratio_intra": stru[nom]["intra"], "ratio_inter": stru[nom]["inter"],
                "rappel_stables": vr, "rappel_ic_bas": lor, "rappel_ic_haut": hir,
                "precision_stables": vp, "precision_ic_bas": lop, "precision_ic_haut": hip,
                "exces_segment": ve, "exces_ic_bas": loe, "exces_ic_haut": hie})
        # les deux ecarts a la meilleure statistique, gros modele et petit modele
        ecarts = []
        for llm in (principal, petit):
            for m in ORDRE:
                if m not in rc:
                    continue
                d = dist_contraste(rc[llm], rc[m], idxc)
                na, da = rc[llm]["_rappel"]
                nb, db = rc[m]["_rappel"]
                ecarts.append({
                    "personnes_communes": len(communes), "llm": llm, "adversaire": m,
                    "quantite": "rappel des raretes stables",
                    "difference": float(na.sum() / da.sum() - nb.sum() / db.sum()),
                    "ic_bas": float(np.percentile(d, 2.5)),
                    "ic_haut": float(np.percentile(d, 97.5)),
                    "p_bootstrap": C42.p_contre_zero(d)})
                da_ = np.array([np.nanmean(acc[llm][k]) - np.nanmean(acc[m][k])
                                for k in idxc])
                da_ = da_[~np.isnan(da_)]
                ecarts.append({
                    "personnes_communes": len(communes), "llm": llm, "adversaire": m,
                    "quantite": "exactitude",
                    "difference": float(np.nanmean(acc[llm]) - np.nanmean(acc[m])),
                    "ic_bas": float(np.percentile(da_, 2.5)),
                    "ic_haut": float(np.percentile(da_, 97.5)),
                    "p_bootstrap": C42.p_contre_zero(da_)})
        C41.ecrire(pd.DataFrame(ecarts), f"r2b-ecarts-a-la-statistique{args.suffixe}.csv")
    C41.ecrire(pd.DataFrame(ponts), f"r2b-pont-modeles{args.suffixe}.csv")

    # ------------------------------- 3. cout du retrait de la famille pour gpt-oss-20b
    reg = []
    autre = "C3 gpt-oss-20b"
    if autre in infos:
        communes = np.array(sorted(set(lignes.tolist())
                                   & set(infos[autre]["lignes"].tolist())))
        rngr = np.random.default_rng(C41.GRAINE_A41)
        idxr = C41.tirages(len(communes), args.tirages, rngr)
        prepr = R2.preparer(paquet, communes, refs, "perimetre")
        for nom in (principal, autre):
            r = R2.mesures_rares(paquet["M"][nom][communes], prepr, colonnes, "stable")
            a = C41.exactitude(paquet["M"][nom], paquet["y1"], communes, colonnes)
            vr, lor, hir, _ = C42.taux_ic(r["_rappel"][0], r["_rappel"][1], idxr)
            vp, lop, hip, _ = C42.taux_ic(r["_precision"][0], r["_precision"][1], idxr)
            ve, loe, hie, _ = C42.taux_ic(r["_exces_segment"][0], r["_exces_segment"][1],
                                          idxr)
            reg.append({"perimetre": f"{len(communes)} personnes communes C3F et C3 gpt-oss",
                        "condition": nom, "exactitude": float(np.nanmean(a)),
                        "cellules_rares_stables": r["cellules"],
                        "raretes_osees": r["raretes_osees"],
                        "rappel_stables": vr, "rappel_ic_bas": lor, "rappel_ic_haut": hir,
                        "precision_stables": vp, "exces_segment": ve,
                        "exces_ic_bas": loe, "exces_ic_haut": hie})
    C41.ecrire(pd.DataFrame(reg), f"r2b-pont-regimes{args.suffixe}.csv")

    # ------------------------------------------------------------------ 4. la figure
    figure(paquet, rares, prep, n, idx, args.suffixe)
    print("termine")


def figure(paquet, rares, prep, n, idx, suffixe):
    principal = "C3F gpt-oss-20b"
    noms = [principal] + [m for m in ORDRE if m in rares]
    # le plancher est celui que a42_commun.mesure_sur calcule lui meme sur ces cellules :
    # un tirage dans la marginale du segment ideologie x genre x age, sans la personne.
    plancher = float(rares[principal]["plancher_segment"])

    vals = {}
    for nom in noms:
        r = rares[nom]
        vr, lor, hir, _ = C42.taux_ic(r["_rappel"][0], r["_rappel"][1], idx)
        vp, lop, hip, _ = C42.taux_ic(r["_precision"][0], r["_precision"][1], idx)
        vals[nom] = (vr, lor, hir, vp, lop, hip, r["raretes_osees"])

    fig, axes = plt.subplots(1, 2, figsize=(11.5, 4.9), facecolor=FOND)
    y = np.arange(len(noms))[::-1]
    etiquettes = [("C3F gpt-oss-20b, jumeau" if nom == principal else COURT[nom])
                  for nom in noms]

    for ax, (k_v, k_lo, k_hi, titre) in zip(
            axes, [(0, 1, 2, "Rappel des raretes stables"),
                   (3, 4, 5, "Precision sur les raretes osees")]):
        style(ax)
        for yi, nom in zip(y, noms):
            couleur = (LLM if nom == principal
                       else (STAT_TIRAGE if NATURE[nom] == "tirage" else STAT_ESPERANCE))
            v, lo, hi = vals[nom][k_v], vals[nom][k_lo], vals[nom][k_hi]
            ax.barh(yi, v, height=0.62, color=couleur, alpha=0.92, zorder=3)
            ax.plot([lo, hi], [yi, yi], color=ENCRE, linewidth=1.4, zorder=4)
            ax.plot([lo, lo, np.nan, hi, hi], [yi - .12, yi + .12, np.nan,
                                               yi - .12, yi + .12],
                    color=ENCRE, linewidth=1.4, zorder=4)
            ax.text(hi + 0.012, yi, f"{v:.3f}", va="center", fontsize=8.5,
                    color=ENCRE_SECONDE)
        ax.set_yticks(y)
        ax.set_yticklabels(etiquettes, fontsize=9.5, color=ENCRE)
        ax.set_title(titre, fontsize=11.5, color=ENCRE, loc="left", pad=9)
        ax.set_xlim(0, max(0.55, max(vals[nom][k_hi] for nom in noms) * 1.22))

    axes[0].axvline(plancher, color=HUMAIN, linestyle=(0, (4, 3)), linewidth=1.7,
                    zorder=5)
    axes[0].annotate(f"plancher de segment {plancher:.3f}",
                     xy=(plancher, len(noms) - 0.55),
                     xytext=(plancher + 0.075, len(noms) - 0.55),
                     fontsize=8.5, color=HUMAIN, va="center",
                     arrowprops=dict(arrowstyle="-", color=HUMAIN, linewidth=0.9))
    axes[0].set_xlabel("part des raretes stables retrouvees", fontsize=9.5,
                       color=ENCRE_SECONDE)
    axes[1].set_xlabel("part des raretes osees qui sont justes", fontsize=9.5,
                       color=ENCRE_SECONDE)

    fig.suptitle(
        f"R2, regime severe : la famille thematique entiere retiree des deux cotes. "
        f"{n} personnes, 58 items, {rares[principal]['cellules']} cellules rares stables.",
        fontsize=11.5, color=ENCRE, x=0.008, ha="left", y=0.985)
    fig.text(0.008, 0.075,
             "Rouge : notre jumeau de langage. Bleu : imputation par tirage. Gris : "
             "imputation par esperance. Barres : IC 95 % bootstrap apparie sur les "
             "personnes, 4 000 tirages.",
             fontsize=8, color=ENCRE_SECONDE, ha="left")
    fig.text(0.008, 0.043,
             "Plancher de segment : tirage au sort dans la marginale du segment "
             "ideologie x genre x age de la personne, calcule sans elle.",
             fontsize=8, color=ENCRE_SECONDE, ha="left")
    fig.text(0.008, 0.011,
             "Il ne figure que sur le rappel : le plancher de precision depend des "
             "cellules que chaque methode ose, et differe donc d'une methode a l'autre.",
             fontsize=8, color=ENCRE_SECONDE, ha="left")
    fig.tight_layout(rect=[0, 0.115, 1, 0.955])
    for ext in ("png", "svg"):
        chemin = os.path.join(SORTIE, f"r2b-figure-rares{suffixe}.{ext}")
        fig.savefig(chemin, dpi=170, facecolor=FOND)
        print(f"ecrit : {chemin}")
    plt.close(fig)


if __name__ == "__main__":
    main()
