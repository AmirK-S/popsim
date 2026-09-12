"""
c7_fort_monde_ouvert_ic : IC bootstrap du 60,17 % (A3, attaquant FORT, monde ouvert)

===========================================================================
PREENREGISTREMENT (ecrit ci-dessous, AVANT tout calcul de bootstrap) :

Defaut vise : A3 cite comme chiffre de tete, en monde ouvert a FPR = 1 %, **60,17 %**
sur l'archive Park (et 4,28 % sur Twin ; 44,37 % / 1,01 % a FPR = 0,1 %). Ces quatre
chiffres viennent de l'attaquant FORT A-LLR, parametres estimes HORS PLI en 5 plis
(`analyses/c7_attaquant_fort.py`, fonction `scores_hors_pli`, colonne
"A-LLR (vraisemblance, hors pli)" de `resultats/c7-attaquant-fort.csv`). Ils sont
publies sans IC. `resultats/c7-monde-ouvert-ic-2026-09-12.md` a deja traite l'IC de
l'attaque NAIVE (Hamming) pour la meme paire de FPR : ce script ne refait PAS ce
travail, il l'importe (lecture du CSV existant) pour la comparaison du point 4.

Attente 1 (largeur) : memes ordres de grandeur qu'en naif, en un peu plus etroit sur
Park puisque le TPR y est beaucoup plus haut (60 % n'est pas cale sur une poignee de
faux positifs comme 20 %) ; sur Twin, le TPR reste bas (4,28 %) donc l'IC devrait
rester large et proche de celui de l'attaque naive, pour les memes raisons (FP absolus
en poignee a FPR = 0,1 %).

Attente 2 (rejeu du seuil) : identique au rapport naif, le seuil est choisi a
posteriori sur le meme echantillon ; un IC a seuil fixe serait trop etroit, surtout a
FPR = 0,1 %.

Attente 3 (piege propre a l'attaquant fort, LE POINT CENTRAL DE CE SCRIPT) : les
parametres a_j (fiabilite du jumeau par item) et q_j (rarete des modalites) de A-LLR
sont estimes HORS PLI, sur 4 plis sur 5, avant d'attaquer le 5e. Un bootstrap qui se
contenterait de rechantillonner les LIGNES de la matrice de score DEJA CALCULEE (sans
jamais rappeler `parametres`/`score_llr`) traite a_j, q_j comme connus et fixes : il ne
capture QUE la variabilite d'echantillonnage de "qui depasse le seuil", pas celle de
l'estimation des parametres eux-memes. C'est optimiste (IC trop etroit), du meme ordre
d'idee qu'un IC qui ignorerait l'incertitude d'un modele ajuste. Attente : un bootstrap
qui RE-ESTIME a_j, q_j a chaque tirage (en respectant la structure en plis, voir
methode ci-dessous) donnera un IC au moins aussi large, probablement plus large, que le
bootstrap a parametres figes.

Piege a eviter explicitement : si l'on rechantillonne les personnes attaquees AVEC
REMISE puis qu'on relance `plis()` (permutation naive de 0..n-1) sur cet echantillon,
une meme personne originale dupliquee par le bootstrap peut atterrir a la fois dans un
pli d'ENTRAINEMENT (sa vraie reponse alimente a_j/q_j) et dans le pli de TEST (sa copie
est attaquee) : c'est une fuite de la personne sur elle-meme, qui gonflerait le score de
cette personne dans CE tirage precis. La parade retenue ici : l'appartenance aux 5 plis
est assignee par IDENTITE ORIGINALE (l'indice de la personne AVANT rechantillonnage),
pas par position dans l'echantillon bootstrap ; toutes les copies d'une meme personne
originale, dans un tirage donne, vont donc necessairement dans le MEME pli, jamais
scindees entre entrainement et test.

Methode, deux bootstraps rapportes cote a cote (memes 2 jeux, meme predicteur : le
meilleur jumeau Twin JSON Persona GPT4.1, le meilleur agent Park "composite", tous
deux sous A-LLR hors pli) :

  (A) "parametres figes" : la matrice de score A-LLR hors pli est calculee UNE FOIS,
      exactement comme dans c7_attaquant_fort.py (memes etiquettes de graine "twin|llr"
      et "stan|llr", memes fonctions importees telles quelles) ; le bootstrap
      rechantillonne ensuite seulement les LIGNES (personnes attaquees) de cette
      matrice deja figee, avec remise, pool de candidats non rechantillonne (meme
      raison qu'en naif : eviter qu'un candidat duplique ne rende sa propre marge
      triviale). Le seuil est REJOUE a chaque tirage (`marges_deux_regimes` et
      `roc_et_taux`, importees sans modification, rappelees a neuf). 2000 tirages,
      graine fixee. CET IC EST OPTIMISTE (voir attente 3) : il est rapporte comme
      methode COMPARABLE a l'IC naif deja publie (meme recette), pas comme le dernier
      mot sur l'incertitude de l'attaquant fort.

  (B) "parametres re-estimes, plis bloques par identite" : a chaque tirage, les
      personnes attaquees sont rechantillonnees avec remise (memes indices que (A)) ;
      les 5 plis sont ensuite assignes par IDENTITE ORIGINALE (voir piege ci-dessus) ;
      pour chaque pli, `parametres` et `score_llr` (importees de c7_attaquant_fort.py
      SANS MODIFICATION) sont rappelees sur les positions d'entrainement du tirage, et
      notent le pli de test contre le pool COMPLET, non rechantillonne. Le seuil est
      rejoue comme en (A). C'est le bootstrap qui respecte la structure hors-pli.
      DEVIATION DOCUMENTEE : par cout de calcul (chaque tirage rappelle l'estimation
      complete des parametres et le score de vraisemblance sur tout le pool, environ
      0,45-0,5 s par tirage mesures en amont), le nombre de tirages est reduit de 2000
      a 300 SEULEMENT POUR (B) ; (A) garde 2000 tirages. Le nombre reellement utilise
      pour (B) est imprime et ecrit dans le CSV (colonne n_boot_reestime).

Aucun appel de modele de langage, aucun reseau. Lecture seule sur data/. Rien n'est
modifie dans c7_attaquant_fort.py, c7_monde_ouvert.py, c7_reidentification.py :
seules leurs fonctions sont importees et appelees. Usage :
.venv/bin/python analyses/c7_fort_monde_ouvert_ic.py
===========================================================================
"""

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from a2_commun import en_codes                                            # noqa: E402
from c7_reidentification import items_communs, REF_V4, REF_V13           # noqa: E402
import c7_stanford as CS                                                  # noqa: E402
from c7_monde_ouvert import (                                            # noqa: E402
    marges_deux_regimes, roc_et_taux, compte_au_moins, graine_nom, GRAINE, FPR_CIBLES,
)
from c7_attaquant_fort import (                                          # noqa: E402
    scores_hors_pli, parametres, score_llr, CIBLE_TWIN, CIBLE_STAN, N_PLIS,
)

N_BOOT_FIGE = 2000              # (A) parametres figes, seuil rejoue -- comparable au script naif
N_BOOT_REESTIME = 300           # (B) re-estimation, plis bloques -- REDUIT de 2000 (voir preenreg.)
GRAINE_IC = [GRAINE, 199]       # sous-graine dediee a ce script (distincte de [GRAINE,99] du script naif)


# ---------------------------------------------------------------------------
# Chargement + score A-LLR hors pli, EXACTEMENT comme bloc_twin/bloc_stanford de
# c7_attaquant_fort.py (memes etiquettes de graine, donc meme matrice que celle
# qui a produit 60,17 % / 44,37 % / 4,28 % / 1,01 % -- sanity check ci-dessous).
# ---------------------------------------------------------------------------

def charger_twin():
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    x = codes[CIBLE_TWIN][:, items]
    couverts = np.flatnonzero((codes[CIBLE_TWIN] >= 0).any(axis=1))
    xc = x[couverts]
    return xc, pool, couverts


def charger_stanford():
    _, items, tables, _ = CS.charger_domaine("gss")
    codes_gss = CS.coder_categoriel_commun(tables, items)
    pool = codes_gss[CS.VAGUE1]
    x = codes_gss[CIBLE_STAN]
    n = pool.shape[0]
    vrai_idx = np.arange(n)
    return x, pool, vrai_idx


def seuil_et_compte_fp(marge_p, marge_r, f_cible, n):
    seuils = np.unique(np.concatenate([marge_p, marge_r]))
    fp_counts = compte_au_moins(np.sort(marge_r), seuils)
    fpr = fp_counts / n
    ordre = np.argsort(fpr)
    fpr_asc, seuils_asc, counts_asc = fpr[ordre], seuils[ordre], fp_counts[ordre]
    h = float(np.interp(f_cible, fpr_asc, seuils_asc))
    k = float(np.interp(f_cible, fpr_asc, counts_asc))
    return h, k


def percentile_ic(vals):
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return float(lo), float(hi)


# ---------------------------------------------------------------------------
# (A) Bootstrap a parametres FIGES : rechantillonnage des lignes d'une matrice de
# score A-LLR hors pli deja calculee une fois. Seuil rejoue a chaque tirage.
# NE CAPTURE PAS l'incertitude d'estimation de a_j, q_j (voir attente 3).
# ---------------------------------------------------------------------------

def bootstrap_fige(nom_jeu, score0, vrai_idx0, n_boot=N_BOOT_FIGE, fpr_cibles=FPR_CIBLES):
    n = score0.shape[0]
    tag = graine_nom(f"{nom_jeu}|fort|fige")

    rng_tie0 = np.random.default_rng([GRAINE, 2, tag])
    marge_p0, correct0, marge_r0 = marges_deux_regimes(score0, vrai_idx0, rng_tie0, n_tirages=1)
    r0 = roc_et_taux(marge_p0, correct0, marge_r0, n)
    top1_0 = float(correct0.mean())
    seuils_pt = {f: seuil_et_compte_fp(marge_p0, marge_r0, f, n) for f in fpr_cibles}

    boot_top1 = np.empty(n_boot)
    boot_tpr_rejoue = {f: np.empty(n_boot) for f in fpr_cibles}
    boot_tpr_fixe = {f: np.empty(n_boot) for f in fpr_cibles}

    rng_boot = np.random.default_rng([GRAINE_IC[0], GRAINE_IC[1], tag])
    t0 = time.time()
    for b in range(n_boot):
        idx = rng_boot.integers(0, n, size=n)
        score_b = score0[idx, :]
        vrai_b = vrai_idx0[idx]
        marge_p_b, correct_b, marge_r_b = marges_deux_regimes(score_b, vrai_b, rng_boot, n_tirages=1)
        boot_top1[b] = correct_b.mean()
        r_b = roc_et_taux(marge_p_b, correct_b, marge_r_b, n)
        tpr_num_b = marge_p_b[correct_b >= 0.5]
        for f in fpr_cibles:
            boot_tpr_rejoue[f][b] = r_b["tpr_fpr_0_1pct"] if f == 0.001 else r_b["tpr_fpr_1pct"]
            h_pt = seuils_pt[f][0]
            boot_tpr_fixe[f][b] = float(np.sum(tpr_num_b >= h_pt)) / n
    dt = time.time() - t0
    print(f"[fige] {nom_jeu:9s} top1={top1_0:.4f} TPR@0,1%={r0['tpr_fpr_0_1pct']:.4f} "
          f"TPR@1%={r0['tpr_fpr_1pct']:.4f} [{n_boot} tirages, {dt:.1f}s]", flush=True)

    ligne = {"jeu": nom_jeu, "n": n, "top1_fort": top1_0,
             "top1_fort_ic_bas": percentile_ic(boot_top1)[0],
             "top1_fort_ic_haut": percentile_ic(boot_top1)[1]}
    for f in fpr_cibles:
        cle = "0_1pct" if f == 0.001 else "1pct"
        tpr_pt = r0["tpr_fpr_0_1pct"] if f == 0.001 else r0["tpr_fpr_1pct"]
        h_pt, k_pt = seuils_pt[f]
        lo_r, hi_r = percentile_ic(boot_tpr_rejoue[f])
        lo_x, hi_x = percentile_ic(boot_tpr_fixe[f])
        ligne[f"tpr_{cle}_fort"] = tpr_pt
        ligne[f"tpr_{cle}_fort_fp_absolus"] = k_pt
        ligne[f"tpr_{cle}_fort_ic_bas_fige"] = lo_r
        ligne[f"tpr_{cle}_fort_ic_haut_fige"] = hi_r
        ligne[f"tpr_{cle}_fort_ic_bas_fige_seuilfixe"] = lo_x
        ligne[f"tpr_{cle}_fort_ic_haut_fige_seuilfixe"] = hi_x
    return ligne


# ---------------------------------------------------------------------------
# (B) Bootstrap avec RE-ESTIMATION de a_j, q_j, plis assignes par IDENTITE
# ORIGINALE (pas par position bootstrap) pour eviter qu'une personne dupliquee
# ne s'entraine sur sa propre copie de test. N reduit (voir preenreg.).
# ---------------------------------------------------------------------------

def plis_bloques_par_identite(idx_resample, n_plis, rng):
    """Groupe les positions du tirage bootstrap en n_plis, en assignant TOUTES les
    copies d'une meme personne originale (meme valeur dans idx_resample) au meme
    pli. Empeche la fuite ou une copie de test partagerait son identite avec une
    copie d'entrainement."""
    valeurs = np.unique(idx_resample)
    perm = rng.permutation(len(valeurs))
    blocs = np.array_split(perm, n_plis)
    fold_de_valeur = np.empty(len(valeurs), dtype=int)
    for k, bloc in enumerate(blocs):
        fold_de_valeur[bloc] = k
    table = np.full(idx_resample.max() + 1, -1, dtype=int)
    table[valeurs] = fold_de_valeur
    fold_assign = table[idx_resample]
    return [np.flatnonzero(fold_assign == k) for k in range(n_plis)]


def bootstrap_reestime(nom_jeu, x0, y_pool, vrai_idx0, n_boot=N_BOOT_REESTIME,
                        fpr_cibles=FPR_CIBLES):
    n = x0.shape[0]
    n_pool = y_pool.shape[0]
    tag = graine_nom(f"{nom_jeu}|fort|reestime")

    boot_top1 = np.empty(n_boot)
    boot_tpr_rejoue = {f: np.empty(n_boot) for f in fpr_cibles}

    rng_boot = np.random.default_rng([GRAINE_IC[0], GRAINE_IC[1] + 1, tag])
    t0 = time.time()
    for b in range(n_boot):
        idx = rng_boot.integers(0, n, size=n)
        x_b = x0[idx]
        vrai_b = vrai_idx0[idx]
        plis_b = plis_bloques_par_identite(idx, N_PLIS, rng_boot)

        s_b = np.zeros((n, n_pool))
        for pli in plis_b:
            if len(pli) == 0:
                continue
            entr = np.setdiff1d(np.arange(n), pli)
            a, q = parametres(x_b[entr], y_pool[vrai_b[entr]])
            s_b[pli] = score_llr(x_b[pli], y_pool, a, q)

        marge_p_b, correct_b, marge_r_b = marges_deux_regimes(s_b, vrai_b, rng_boot, n_tirages=1)
        boot_top1[b] = correct_b.mean()
        r_b = roc_et_taux(marge_p_b, correct_b, marge_r_b, n)
        for f in fpr_cibles:
            boot_tpr_rejoue[f][b] = r_b["tpr_fpr_0_1pct"] if f == 0.001 else r_b["tpr_fpr_1pct"]
        if (b + 1) % 50 == 0:
            print(f"  [reestime] {nom_jeu} tirage {b + 1}/{n_boot} "
                  f"({time.time() - t0:.0f}s ecoulees)", flush=True)
    dt = time.time() - t0
    print(f"[reestime] {nom_jeu:9s} [{n_boot} tirages, {dt:.1f}s]", flush=True)

    ligne = {"jeu": nom_jeu, "n_boot_reestime": n_boot,
             "top1_fort_ic_bas_reestime": percentile_ic(boot_top1)[0],
             "top1_fort_ic_haut_reestime": percentile_ic(boot_top1)[1]}
    for f in fpr_cibles:
        cle = "0_1pct" if f == 0.001 else "1pct"
        lo, hi = percentile_ic(boot_tpr_rejoue[f])
        ligne[f"tpr_{cle}_fort_ic_bas_reestime"] = lo
        ligne[f"tpr_{cle}_fort_ic_haut_reestime"] = hi
    return ligne


def main():
    print(__doc__.split("=" * 75)[1][:600] + " ...", flush=True)

    print("\n=== Chargement + score A-LLR hors pli, Twin ===", flush=True)
    xc, pool_t, couverts = charger_twin()
    s_llr_t = scores_hors_pli(xc, pool_t, couverts, "twin|llr")
    print(f"Twin : n={s_llr_t.shape[0]}, n_pool={s_llr_t.shape[1]}", flush=True)

    print("\n=== Chargement + score A-LLR hors pli, Stanford (Park GSS) ===", flush=True)
    xs, pool_s, vrai_s = charger_stanford()
    s_llr_s = scores_hors_pli(xs, pool_s, vrai_s, "stan|llr")
    print(f"Stanford : n={s_llr_s.shape[0]}, n_pool={s_llr_s.shape[1]}", flush=True)

    # Sanity check : reproduit-on bien les chiffres publies (60,17 % etc.) ?
    for nom, score, vidx in (("Twin", s_llr_t, couverts), ("Stanford", s_llr_s, vrai_s)):
        rng_chk = np.random.default_rng([GRAINE, 2, graine_nom(f"{nom}|fort|fige")])
        mp, cor, mr = marges_deux_regimes(score, vidx, rng_chk, n_tirages=1)
        r = roc_et_taux(mp, cor, mr, score.shape[0])
        print(f"  sanity {nom} : top1={cor.mean():.4f} TPR@1%={r['tpr_fpr_1pct']:.4f} "
              f"TPR@0,1%={r['tpr_fpr_0_1pct']:.4f}", flush=True)

    lignes_fige = []
    print("\n=== (A) Bootstrap parametres FIGES, 2000 tirages ===", flush=True)
    lignes_fige.append(bootstrap_fige("Twin", s_llr_t, couverts))
    lignes_fige.append(bootstrap_fige("Stanford", s_llr_s, vrai_s))

    lignes_reest = []
    print(f"\n=== (B) Bootstrap RE-ESTIME (plis bloques), {N_BOOT_REESTIME} tirages ===", flush=True)
    lignes_reest.append(bootstrap_reestime("Twin", xc, pool_t, couverts))
    lignes_reest.append(bootstrap_reestime("Stanford", xs, pool_s, vrai_s))

    df_fige = pd.DataFrame(lignes_fige)
    df_reest = pd.DataFrame(lignes_reest)
    df = df_fige.merge(df_reest, on="jeu")

    # Comparaison a l'attaque naive deja publiee (lecture seule du CSV existant,
    # aucun recalcul : ce chiffre appartient au script naif).
    try:
        naif = pd.read_csv(os.path.join(T1.SORTIE, "c7-monde-ouvert-ic.csv"))
        corr = {"Twin": "Meilleur jumeau (JSON Persona GPT4.1)",
                "Stanford": "Meilleur agent (composite)"}
        for i, row in df.iterrows():
            nrow = naif[(naif.jeu == row.jeu) & (naif.predicteur == corr[row.jeu])]
            if len(nrow):
                nrow = nrow.iloc[0]
                for cle in ["1pct", "0_1pct"]:
                    df.loc[i, f"naif_tpr_{cle}"] = nrow[f"tpr_{cle}"]
                    df.loc[i, f"naif_tpr_{cle}_ic_bas"] = nrow[f"tpr_{cle}_ic_bas_seuil_rejoue"]
                    df.loc[i, f"naif_tpr_{cle}_ic_haut"] = nrow[f"tpr_{cle}_ic_haut_seuil_rejoue"]
    except FileNotFoundError:
        print("resultats/c7-monde-ouvert-ic.csv absent : comparaison naif non jointe", flush=True)

    T1.ecrire(df, "c7-fort-monde-ouvert-ic.csv")

    print("\n--- recapitulatif ---", flush=True)
    for _, row in df.iterrows():
        print(f"{row['jeu']:9s} TPR@1%={row['tpr_1pct_fort']:.4f} "
              f"[fige {row['tpr_1pct_fort_ic_bas_fige']:.4f};{row['tpr_1pct_fort_ic_haut_fige']:.4f}] "
              f"[reestime {row['tpr_1pct_fort_ic_bas_reestime']:.4f};{row['tpr_1pct_fort_ic_haut_reestime']:.4f}] "
              f"FP_abs={row['tpr_1pct_fort_fp_absolus']:.2f}", flush=True)
        print(f"{'':9s} TPR@0,1%={row['tpr_0_1pct_fort']:.4f} "
              f"[fige {row['tpr_0_1pct_fort_ic_bas_fige']:.4f};{row['tpr_0_1pct_fort_ic_haut_fige']:.4f}] "
              f"[reestime {row['tpr_0_1pct_fort_ic_bas_reestime']:.4f};{row['tpr_0_1pct_fort_ic_haut_reestime']:.4f}] "
              f"FP_abs={row['tpr_0_1pct_fort_fp_absolus']:.2f}", flush=True)


if __name__ == "__main__":
    main()
