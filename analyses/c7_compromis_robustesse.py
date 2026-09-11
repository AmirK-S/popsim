"""
c7_compromis_robustesse : le rho fidelite/fuite de c7_compromis.py tient-il a un choix de
points, ou porte-t-il sur un seul point isole ?

===========================================================================
PREENREGISTREMENT : resultats/c7-compromis-robustesse-preenregistrement.md, ecrit le
12 septembre 2026, AVANT ce fichier et avant tout calcul.

OBJECTION RECUE : Platzer & Reutterer (arXiv 2104.00635) et Adams et al. (iScience 2025)
rapportent une fidelite et un risque separables ; arXiv 2605.06835 (2026) rapporte un
decouplage direct, le risque croissant quand la qualite sature. Ce script teste si le
resultat de c7_compromis.py (Spearman 0,958 sur 12 points) resiste a quatre controles.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee : t1_commun.charger, t1_baselines.calculer,
c7_reidentification.items_communs / rangs_attaque / graine_nom, a2_commun.bootstrap_personnes
(convention).

CE QUI EST NOUVEAU ICI :
  1. Un 13e point, le retest humain (vagues 1-3) attaquant la vague 4 : jamais calcule avant
     ce script, fidelite fixee a 1 par construction.
  2. Retrait par famille (LLM huit configurations, statistique quatre reperes, humain un
     point) et jackknife point par point, avec IC par bootstrap joint.
  3. Un diagnostic de forme : les reperes statistiques sont-ils indiscernables du hasard
     (palier), et la relation continue-t-elle de monter jusqu'au retest humain (pas de
     second palier en haut de plage) ?
  4. Une lecture, non un recalcul, des taux deja publies de resultats/c7-stanford-resultats.md
     (c7_stanford.py n'est pas touche : chantier d'un autre agent).

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_compromis_robustesse.py
===========================================================================
"""

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                       # noqa: E402
import t1_baselines as TB                    # noqa: E402
import c7_reidentification as C7             # noqa: E402
from a2_commun import bootstrap_personnes    # noqa: E402,F401

GRAINE = 20260911
N_BOOTSTRAP = 2000
STATISTIQUES = ["B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]
HUMAIN = "humains vagues 1-3 (retest)"

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")


def vecteur_dense(couverts, valeurs, n_total):
    out = np.full(n_total, np.nan)
    out[couverts] = valeurs
    return out


def rho_bootstrap(noms, vecteurs, fidelite, n_tirages=N_BOOTSTRAP, graine=GRAINE):
    """Spearman(fidelite fixee, fuite) et son IC par bootstrap joint (chaque point
    reechantillonne independamment sur ses propres personnes, convention de
    a2_commun.bootstrap_personnes)."""
    moyennes = np.array([np.nanmean(vecteurs[n]) for n in noms])
    rho_obs, p_obs = stats.spearmanr(fidelite, moyennes)
    rng = np.random.default_rng(graine)
    rhos = np.empty(n_tirages)
    for b in range(n_tirages):
        boot = np.empty(len(noms))
        for i, n in enumerate(noms):
            v = vecteurs[n]
            v = v[~np.isnan(v)]
            boot[i] = rng.choice(v, size=len(v), replace=True).mean()
        r, _ = stats.spearmanr(fidelite, boot)
        rhos[b] = r
    bas, haut = np.percentile(rhos, [2.5, 97.5])
    return rho_obs, p_obs, bas, haut


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t0 = time.time()
    paq = T1.charger()
    codes = paq["codes"]
    n_total = paq["n"]
    items = C7.items_communs(codes, [C7.REF_V4, C7.REF_V13])
    pool_v4 = codes[C7.REF_V4][:, items]
    print(f"{n_total} personnes, {len(items)} items communs, charge en "
          f"{time.time() - t0:.0f}s", flush=True)

    vecteurs = {}
    moyennes = {}

    # ------------------------------------------------------------------ 1. les 8 LLM
    for nom in C7.CONFIGURATIONS:
        x = codes[nom][:, items]
        couverts = np.flatnonzero((codes[nom] >= 0).any(axis=1))
        rng = np.random.default_rng([GRAINE, C7.graine_nom(nom)])
        _, top1, _ = C7.rangs_attaque(x[couverts], pool_v4, couverts, rng)
        vecteurs[nom] = vecteur_dense(couverts, top1, n_total)
        moyennes[nom] = float(np.nanmean(top1))

    # ------------------------------------------------------------------ 2. le 13e point : humain
    x = codes[C7.REF_V13][:, items]
    couverts = np.flatnonzero((codes[C7.REF_V13] >= 0).any(axis=1))
    rng = np.random.default_rng([GRAINE, C7.graine_nom(HUMAIN)])
    _, top1, _ = C7.rangs_attaque(x[couverts], pool_v4, couverts, rng)
    vecteurs[HUMAIN] = vecteur_dense(couverts, top1, n_total)
    moyennes[HUMAIN] = float(np.nanmean(top1))
    m, bas, haut = bootstrap_personnes(top1, n_tirages=2000, graine=GRAINE)
    print(f"\nretest humain (attaque vague 1-3 -> pool vague 4) : top1={m:.4f} "
          f"[{bas:.4f};{haut:.4f}] (n={len(couverts)})", flush=True)

    # ------------------------------------------------------------------ 3. les 4 statistiques
    t0 = time.time()
    paq_slim = dict(paq)
    codes_slim = dict(paq["codes"])
    codes_slim[T1.REF] = paq["codes"][T1.REF][:, items]
    paq_slim["codes"] = codes_slim
    base = TB.calculer(paq_slim, avec_pmm=True)
    print(f"t1_baselines.calculer (60 items) : {time.time() - t0:.0f}s", flush=True)

    ic_stat = {}
    for nom in STATISTIQUES:
        x = base[nom]
        couverts = np.arange(n_total)
        rng = np.random.default_rng([GRAINE, C7.graine_nom(nom)])
        _, top1, _ = C7.rangs_attaque(x[couverts], pool_v4, couverts, rng)
        vecteurs[nom] = vecteur_dense(couverts, top1, n_total)
        moyennes[nom] = float(np.nanmean(top1))
        m, bas, haut = bootstrap_personnes(top1, n_tirages=2000, graine=GRAINE)
        ic_stat[nom] = (m, bas, haut)
        print(f"  {nom} : top1={m:.4f} [{bas:.4f};{haut:.4f}]", flush=True)

    # ------------------------------------------------------------------ 4. table des 13 points
    classement = pd.read_csv(os.path.join(SORTIE, "t1-classement.csv"))
    classement = classement[classement.segmentation == "S_gra"]
    noms_13 = C7.CONFIGURATIONS + STATISTIQUES + [HUMAIN]

    def groupe_de(nom):
        if nom in STATISTIQUES:
            return "statistique"
        if nom == HUMAIN:
            return "humain"
        return "LLM"

    lignes = []
    for nom in noms_13:
        row = classement[classement.condition == nom].iloc[0]
        lignes.append({
            "configuration": nom, "groupe": groupe_de(nom),
            "fidelite_plancher": float(row.part_du_plancher_humain),
            "exactitude": float(row.exactitude_vraie),
            "fuite_top1": moyennes[nom],
        })
    df = pd.DataFrame(lignes).sort_values("fidelite_plancher").reset_index(drop=True)
    print("\n" + df.to_string(index=False), flush=True)

    hasard = 1.0 / n_total
    print(f"\nhasard top-1 = {hasard:.5f}", flush=True)

    # ------------------------------------------------------------------ 5. rho sur les 13, et sur les 12 (sans l'humain)
    fid13 = df.fidelite_plancher.values
    rho13, p13, bas13, haut13 = rho_bootstrap(list(df.configuration), vecteurs, fid13)
    print(f"\nrho (13 points, avec retest humain) = {rho13:.4f} "
          f"[{bas13:.4f};{haut13:.4f}] (p={p13:.4g})", flush=True)

    sorties = {"n": [], "groupe_retire": [], "rho": [], "p": [], "ic_bas": [], "ic_haut": []}

    def ajouter(etiquette, sous_df):
        noms = list(sous_df.configuration)
        fid = sous_df.fidelite_plancher.values
        r, p, b, h = rho_bootstrap(noms, vecteurs, fid)
        sorties["n"].append(len(noms))
        sorties["groupe_retire"].append(etiquette)
        sorties["rho"].append(r)
        sorties["p"].append(p)
        sorties["ic_bas"].append(b)
        sorties["ic_haut"].append(h)
        print(f"  retrait '{etiquette}' (n={len(noms)}) : rho={r:.4f} [{b:.4f};{h:.4f}] "
              f"p={p:.4g}", flush=True)

    print("\n--- 6. retrait par famille ---", flush=True)
    ajouter("aucun (13 points)", df)
    ajouter("LLM retire (stat + humain)", df[df.groupe != "LLM"])
    ajouter("statistique retiree (LLM + humain)", df[df.groupe != "statistique"])
    ajouter("humain retire (12 points, = c7-compromis.csv)", df[df.groupe != "humain"])
    ajouter("LLM SEUL (stat et humain retires)", df[df.groupe == "LLM"])

    df_familles = pd.DataFrame(sorties)

    # ------------------------------------------------------------------ 7. jackknife point par point
    print("\n--- 7. jackknife, un point retire a la fois ---", flush=True)
    jack = []
    for _, r_out in df.iterrows():
        reste = df[df.configuration != r_out.configuration]
        r, p = stats.spearmanr(reste.fidelite_plancher, reste.fuite_top1)
        jack.append({"point_retire": r_out.configuration, "groupe": r_out.groupe,
                     "rho_sans_ce_point": r, "p": p})
        print(f"  sans {r_out.configuration} : rho={r:.4f}", flush=True)
    df_jack = pd.DataFrame(jack).sort_values("rho_sans_ce_point")

    # ------------------------------------------------------------------ 8. forme de la relation
    print("\n--- 8. forme : palier bas puis hausse, ou lineaire partout ? ---", flush=True)
    seuil = 0.15
    bas_plage = df[df.fidelite_plancher < seuil]
    haut_plage = df[df.fidelite_plancher >= seuil]
    print(f"sous fidelite {seuil} (n={len(bas_plage)}) : fuite {bas_plage.fuite_top1.min():.5f} "
          f"a {bas_plage.fuite_top1.max():.5f}, hasard={hasard:.5f}", flush=True)
    for nom in STATISTIQUES:
        m, b, h = ic_stat[nom]
        print(f"  {nom} : IC contient le hasard = {b <= hasard <= h}", flush=True)

    pente_lin, ord_lin, r_lin, p_lin, _ = stats.linregress(
        df.fidelite_plancher, df.fuite_top1)
    sse_lin = float(np.sum((df.fuite_top1 - (ord_lin + pente_lin * df.fidelite_plancher)) ** 2))

    # modele a deux regimes : plancher constant sous c, lineaire au-dessus, c balaye sur
    # les valeurs de fidelite observees (au moins 3 points de chaque cote)
    candidats = sorted(df.fidelite_plancher.unique())
    meilleur = None
    for c in candidats:
        sous = df[df.fidelite_plancher < c]
        sur = df[df.fidelite_plancher >= c]
        if len(sous) < 3 or len(sur) < 3:
            continue
        pred_sous = np.full(len(sous), sous.fuite_top1.mean())
        if len(sur) >= 2:
            p2, o2, _, _, _ = stats.linregress(sur.fidelite_plancher, sur.fuite_top1)
            pred_sur = o2 + p2 * sur.fidelite_plancher
        else:
            pred_sur = sur.fuite_top1.values
        sse = float(np.sum((sous.fuite_top1 - pred_sous) ** 2)
                    + np.sum((sur.fuite_top1 - pred_sur) ** 2))
        if meilleur is None or sse < meilleur[1]:
            meilleur = (c, sse)
    print(f"\nSSE regression lineaire simple (13 points) = {sse_lin:.6f}", flush=True)
    if meilleur:
        print(f"SSE meilleur modele a deux regimes (seuil={meilleur[0]:.3f}) = "
              f"{meilleur[1]:.6f}", flush=True)

    # saturation en haut de plage : le retest humain depasse-t-il le meilleur LLM ?
    meilleur_llm = df[df.groupe == "LLM"].sort_values("fuite_top1").iloc[-1]
    fuite_humain = float(df[df.configuration == HUMAIN].fuite_top1.iloc[0])
    print(f"\nmeilleur LLM : {meilleur_llm.configuration}, fuite={meilleur_llm.fuite_top1:.4f} "
          f"; retest humain fuite={fuite_humain:.4f} ; "
          f"ratio={fuite_humain / meilleur_llm.fuite_top1:.2f}", flush=True)

    df["hasard_top1"] = hasard
    df.to_csv(os.path.join(SORTIE, "c7-compromis-robustesse-points.csv"), index=False)
    df_familles.to_csv(os.path.join(SORTIE, "c7-compromis-robustesse-familles.csv"),
                        index=False)
    df_jack.to_csv(os.path.join(SORTIE, "c7-compromis-robustesse-jackknife.csv"), index=False)
    print("\necrit : c7-compromis-robustesse-{points,familles,jackknife}.csv", flush=True)


if __name__ == "__main__":
    main()
