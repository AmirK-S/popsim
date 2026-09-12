"""
c7_disjoint : la corrélation fidélité/fuite de c7-compromis survit-elle à la disjonction
des items, et dépasse-t-elle un nul où seule la marge d'exactitude par personne existe ?

===========================================================================
PREENREGISTREMENT : resultats/c7-disjoint-preenregistrement.md, écrit le 12 septembre
2026, AVANT ce fichier et avant tout calcul.

OBJECTION TESTEE : dans c7-compromis-resultats.md, Spearman(fidélité, fuite) = 0,958 sur
12 points pourrait être en partie une identité arithmétique, les deux axes étant des
fonctions monotones de la même marge d'exactitude par personne.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu déjà public (Twin-2K-500). Aucun identifiant ni
pid n'est jamais imprimé ou écrit : uniquement des taux agrégés.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiée :
  t1_commun.charger                les quinze tables de Twin, segment S_gra
  a44_commun.permuter_intra        la permutation des personnes intra segment
  a44_mesures.exactitude_codes     l'exactitude par personne sur codes entiers
  a2_commun.distance_hamming       la distance de Hamming normalisee, masquage deja fait
  c7_reidentification.items_communs, graine_nom, CONFIGURATIONS, REF_V4
  t1_baselines.calculer            les 4 prédicteurs statistiques

CE QUI EST NOUVEAU ICI : le partage aléatoire des 60 items en deux moitiés A/B pour
mesurer fidélité et fuite sur des items disjoints ; le calcul direct du top-1 (le vrai
répondant est-il le maximum d'accord de sa ligne, bruit i.i.d. pour départager les ex
æquo) sans passer par le rang complet de c7_reidentification.rangs_attaque, strictement
équivalent sur le seul indicateur top-1 mais sans les deux tris couteux ; le prédicteur
artificiel « nul de marge » qui ne conserve que le taux d'exactitude conditionnelle par
personne ; le recalcul du point humain sans le diviser par sa propre valeur.

Aucun appel de modèle de langage. Lecture seule sur data/. Aucun script existant modifié.
Usage : .venv/bin/python analyses/c7_disjoint.py
===========================================================================
"""

import argparse
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np                             # noqa: E402
import pandas as pd                            # noqa: E402
from scipy import stats                        # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                         # noqa: E402
import t1_baselines as TB                      # noqa: E402
import a44_commun as C44                       # noqa: E402
from a44_mesures import exactitude_codes       # noqa: E402
from a2_commun import distance_hamming         # noqa: E402
import c7_reidentification as C7               # noqa: E402

GRAINE = 20260912
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

STATISTIQUES = ["B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]
HUMAIN = C7.REF_V13     # le retest humain, traité à part, jamais comme dénominateur

N_SPLITS = 50
N_PERM_CHUTE = 40
N_TIRAGES_FUITE = 3
N_NUL = 100


def ecrire(df, nom):
    p = os.path.join(SORTIE, nom)
    df.to_csv(p, index=False)
    print(f"ecrit {p}", flush=True)


def partage_stratifie(est_ord_60, rng):
    """Deux moitiés A/B des 60 items, ordinal et non ordinal séparément équilibrés."""
    idx_ord = np.flatnonzero(est_ord_60)
    idx_non = np.flatnonzero(~est_ord_60)
    a, b = [], []
    for idx in (idx_ord, idx_non):
        p = rng.permutation(idx)
        m = len(p) // 2
        a.extend(p[:m].tolist())
        b.extend(p[m:].tolist())
    return np.array(sorted(a)), np.array(sorted(b))


def chute_brute(cd, y1, s, n_perm, rng):
    """Chute = exactitude vraie - exactitude moyenne sous permutation intra-segment."""
    vraie = float(np.nanmean(exactitude_codes(cd, y1)))
    acc_p = np.empty(n_perm)
    for r in range(n_perm):
        p = C44.permuter_intra(cd.shape[0], s, rng)
        acc_p[r] = float(np.nanmean(exactitude_codes(cd[p], y1)))
    return vraie - float(acc_p.mean())


def fuite_top1(x_sub, pool_sub, vrai_idx, rng, n_tirages=N_TIRAGES_FUITE):
    """Top-1 moyen : le vrai répondant est-il le maximum d'accord de sa ligne ?

    Équivalent exact, sur le seul indicateur top-1, de
    c7_reidentification.rangs_attaque (vérifié numériquement) : même distance de
    Hamming, même bruit i.i.d. pour départager les ex æquo, mais sans les deux tris
    (argsort) par tirage que rangs_attaque calcule pour obtenir le rang complet et le
    top-10, inutiles ici.
    """
    accord = 1.0 - distance_hamming(x_sub, pool_sub)
    n = accord.shape[0]
    lignes = np.arange(n)
    acc = np.zeros(n)
    for _ in range(n_tirages):
        combo = accord + rng.random(accord.shape) * 1e-9
        acc += combo[lignes, vrai_idx] >= combo.max(axis=1)
    return float(np.mean(acc / n_tirages))


def construire_nul(x_reel, y_ref, k_items_60, rng):
    """Prédicteur artificiel : même masque de couverture et même marge d'exactitude
    conditionnelle par personne que x_reel, aucune structure au-delà (garde-fou du
    préenregistrement, section « nul de marge »)."""
    n, m = x_reel.shape
    masque = x_reel >= 0
    correct_reel = masque & (x_reel == y_ref)
    n_obs = masque.sum(axis=1)
    q = np.divide(correct_reel.sum(axis=1), np.maximum(n_obs, 1),
                  out=np.zeros(n), where=n_obs > 0)
    out = np.full((n, m), -1, dtype=x_reel.dtype)
    tirage_correct = rng.random((n, m)) < q[:, None]
    faux = rng.integers(0, np.maximum(k_items_60 - 1, 1)[None, :].repeat(n, axis=0))
    faux = faux + (faux >= y_ref)          # saute la vraie modalité
    out = np.where(masque, np.where(tirage_correct, y_ref, faux), -1).astype(x_reel.dtype)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--splits", type=int, default=N_SPLITS)
    ap.add_argument("--nul", type=int, default=N_NUL)
    ap.add_argument("--permutations", type=int, default=N_PERM_CHUTE)
    ap.add_argument("--tirages", type=int, default=N_TIRAGES_FUITE)
    args = ap.parse_args()
    n_splits, n_nul = args.splits, args.nul
    n_perm, n_tir = args.permutations, args.tirages

    print(__doc__.split("=" * 75)[1], flush=True)
    t0 = time.time()
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]
    n_total = paq["n"]

    items = C7.items_communs(codes, [C7.REF_V4, C7.REF_V13])
    est_ord_60 = paq["est_ordinal"][items]
    k_items_60 = paq["k_items"][items]
    y_ref = codes[C7.REF_V4][:, items]     # vérité et pool des candidats
    print(f"{n_total} personnes, {len(items)} items communs "
          f"({int(est_ord_60.sum())} ordinaux), charge en {time.time()-t0:.0f}s",
          flush=True)

    # ------------------------------------------------------------------
    # les 12 prédicteurs, plus le retest humain traité à part
    # ------------------------------------------------------------------
    noms_12 = list(C7.CONFIGURATIONS) + STATISTIQUES
    pred = {}
    for nom in C7.CONFIGURATIONS:
        pred[nom] = codes[nom][:, items]

    paq_slim = dict(paq)
    codes_slim = dict(codes)
    codes_slim[T1.REF] = codes[T1.REF][:, items]
    paq_slim["codes"] = codes_slim
    base = TB.calculer(paq_slim, avec_pmm=True)
    for nom in STATISTIQUES:
        pred[nom] = base[nom]

    pred[HUMAIN] = codes[HUMAIN][:, items]      # traité à part, jamais dans noms_12

    couverts = {nom: np.flatnonzero((pred[nom] >= 0).any(axis=1))
                for nom in noms_12 + [HUMAIN]}
    print(f"predicteurs charges, {time.time()-t0:.0f}s", flush=True)

    # ------------------------------------------------------------------
    # 1. Test principal : 50 partages disjoints des items
    # ------------------------------------------------------------------
    rng_split = np.random.default_rng(GRAINE)
    lignes_split = []
    rhos = []
    for s_i in range(n_splits):
        A, B = partage_stratifie(est_ord_60, rng_split)
        fid, fui = {}, {}
        for nom in noms_12 + [HUMAIN]:
            cv = couverts[nom]
            x = pred[nom][cv]
            y = y_ref[cv]
            seg = seg_gra[cv]
            rng_c = np.random.default_rng([GRAINE, 1, s_i, C7.graine_nom(nom)])
            fid[nom] = chute_brute(x[:, A], y[:, A], seg, n_perm, rng_c)
            rng_f = np.random.default_rng([GRAINE, 2, s_i, C7.graine_nom(nom)])
            fui[nom] = fuite_top1(x[:, B], y_ref[:, B], cv, rng_f, n_tirages=n_tir)
        rho, _ = stats.spearmanr([fid[n] for n in noms_12], [fui[n] for n in noms_12])
        rhos.append(rho)
        for nom in noms_12 + [HUMAIN]:
            lignes_split.append({"partage": s_i, "configuration": nom,
                                  "fidelite_A": fid[nom], "fuite_B": fui[nom]})
        if s_i % 10 == 0:
            print(f"  partage {s_i}, rho={rho:.4f}, {time.time()-t0:.0f}s", flush=True)
    rhos = np.array(rhos)
    ecrire(pd.DataFrame(lignes_split), "c7-disjoint-partages.csv")
    print(f"\nSpearman disjoint : moyenne={rhos.mean():.4f}, mediane={np.median(rhos):.4f}, "
          f"IC95%=[{np.percentile(rhos,2.5):.4f} ; {np.percentile(rhos,97.5):.4f}], "
          f"part > 0.7 = {(rhos > 0.7).mean():.2f}", flush=True)

    # ------------------------------------------------------------------
    # 2. Nul de marge : prédicteurs artificiels, 100 réplicats, items entiers
    # ------------------------------------------------------------------
    rng_nul = np.random.default_rng(GRAINE + 1)
    rhos_nul = np.empty(n_nul)
    for r in range(n_nul):
        fid, fui = {}, {}
        for nom in noms_12:
            cv = couverts[nom]
            x = pred[nom][cv]
            y = y_ref[cv]
            seg = seg_gra[cv]
            rng_g = np.random.default_rng([GRAINE, 3, r, C7.graine_nom(nom)])
            x_nul = construire_nul(x, y, k_items_60, rng_g)
            rng_c = np.random.default_rng([GRAINE, 4, r, C7.graine_nom(nom)])
            fid[nom] = chute_brute(x_nul, y, seg, n_perm, rng_c)
            rng_f = np.random.default_rng([GRAINE, 5, r, C7.graine_nom(nom)])
            fui[nom] = fuite_top1(x_nul, y_ref, cv, rng_f, n_tirages=n_tir)
        rhos_nul[r], _ = stats.spearmanr([fid[n] for n in noms_12],
                                          [fui[n] for n in noms_12])
        if r % 20 == 0:
            print(f"  nul {r}, rho={rhos_nul[r]:.4f}, {time.time()-t0:.0f}s", flush=True)
    ecrire(pd.DataFrame({"replicat": np.arange(n_nul), "rho_nul": rhos_nul}),
           "c7-disjoint-nul.csv")
    seuil95 = float(np.percentile(rhos_nul, 95))
    print(f"\nNul de marge ({n_nul} replicats) : moyenne={rhos_nul.mean():.4f}, "
          f"95e centile={seuil95:.4f}", flush=True)
    print(f"rho observe (moyenne disjointe) {rhos.mean():.4f} > "
          f"95e centile du nul {seuil95:.4f} : {bool(rhos.mean() > seuil95)}", flush=True)

    # ------------------------------------------------------------------
    # 3. Point humain, position brute, jamais divisée par sa propre valeur
    # ------------------------------------------------------------------
    df_split = pd.DataFrame(lignes_split)
    humain_fid = df_split[df_split.configuration == HUMAIN].fidelite_A.mean()
    humain_fui = df_split[df_split.configuration == HUMAIN].fuite_B.mean()
    meilleur = df_split[df_split.configuration != HUMAIN].groupby(
        "configuration").fuite_B.mean().idxmax()
    meilleur_fid = df_split[df_split.configuration == meilleur].fidelite_A.mean()
    meilleur_fui = df_split[df_split.configuration == meilleur].fuite_B.mean()
    print(f"\nPoint humain (brut, moyenne des 50 partages) : "
          f"fidelite_A={humain_fid:.4f}, fuite_B={humain_fui:.4f}", flush=True)
    print(f"Meilleur predicteur riche ({meilleur}) : "
          f"fidelite_A={meilleur_fid:.4f}, fuite_B={meilleur_fui:.4f}", flush=True)
    print(f"Saturation en haut de plage : humain devant le meilleur sur les deux axes = "
          f"{bool(humain_fid >= meilleur_fid and humain_fui >= meilleur_fui)}", flush=True)

    resume = pd.DataFrame([{
        "rho_disjoint_moyen": float(rhos.mean()),
        "rho_disjoint_median": float(np.median(rhos)),
        "rho_disjoint_ic_bas": float(np.percentile(rhos, 2.5)),
        "rho_disjoint_ic_haut": float(np.percentile(rhos, 97.5)),
        "part_rho_superieur_07": float((rhos > 0.7).mean()),
        "nul_moyenne": float(rhos_nul.mean()),
        "nul_95e_centile": float(seuil95),
        "rho_observe_depasse_nul_95": bool(rhos.mean() > seuil95),
        "humain_fidelite_brute": float(humain_fid),
        "humain_fuite_brute": float(humain_fui),
        "meilleur_predicteur": meilleur,
        "meilleur_fidelite_brute": float(meilleur_fid),
        "meilleur_fuite_brute": float(meilleur_fui),
    }])
    ecrire(resume, "c7-disjoint-resume.csv")
    print(f"\ntermine en {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
