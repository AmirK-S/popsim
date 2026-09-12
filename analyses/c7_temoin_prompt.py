"""
c7_temoin_prompt : l'accord inter-jumeaux vient-il de la personne, ou seulement du prompt
et du segment demographique ?

===========================================================================
PREENREGISTREMENT : resultats/c7-temoin-prompt-preenregistrement.md, ecrit le 12 septembre
2026, AVANT ce fichier et avant tout calcul.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Ce script ne calcule,
n'imprime et n'ecrit JAMAIS l'identite ou le pid d'une personne, ni aucune liste
d'appariements individuels. Seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                 les quinze tables de Twin, les segmentations
  a2_commun.distance_hamming         la distance de Hamming normalisee, masquage deja fait
  a2_commun.bootstrap_personnes      l'IC 95 pour cent par reechantillonnage des personnes
  c7_reidentification.rangs_attaque  le rang du vrai repondant contre un bassin
  c7_reidentification.graine_nom     un entier stable a partir d'une chaine
  c7_reidentification.resume_taux    moyenne + IC par a2_commun.bootstrap_personnes
  c7_transfert.items_pair            les colonnes pleines a 100 pour cent des deux cotes
  c7_transfert.CONFIGURATIONS        alias de c7_reidentification.CONFIGURATIONS

CE QUI EST NOUVEAU ICI : la decomposition exacte de l'accord entre deux jumeaux en
plancher de prompt + apport de segment + apport individuel (section 1 du preenregistrement),
et le temoin de population pure par mode de segment leave-one-out (section 2).

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_temoin_prompt.py
===========================================================================
"""

import itertools
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                              # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes           # noqa: E402
import c7_transfert as C7T                                            # noqa: E402
from c7_reidentification import rangs_attaque, graine_nom, resume_taux  # noqa: E402

GRAINE = 20260912
N_BOOTSTRAP = 2000
SEG = "S_fin"          # bloc d'ideologie x genre x age : cf. preenregistrement
SEUIL_DESTRUCTEUR_RATIO = 1.0 / 3.0   # top1 mode-segment >= 1/3 du top1 individuel publie


# ---------------------------------------------------------------------------
# Les 30 paires riches a 60 items (mêmes que celles retabulees dans
# resultats/c7-transfert-resultats.md), retrouvees par le meme critere que
# c7_transfert.items_pair, sans recalculer la matrice deja publiee.
# ---------------------------------------------------------------------------

def paires_riches_60_items(codes, couverture):
    riches = [c for c in C7T.CONFIGURATIONS if c != C7T.DEMO]
    paires = []
    for x_nom, y_nom in itertools.permutations(riches, 2):
        cov_x, cov_y = couverture[x_nom], couverture[y_nom]
        attaques_idx = np.intersect1d(cov_x, cov_y)
        pool_idx = cov_y
        items = C7T.items_pair(codes, x_nom, y_nom, attaques_idx, pool_idx)
        if len(items) == 60:
            paires.append((x_nom, y_nom, attaques_idx, pool_idx, items))
    return paires


# ---------------------------------------------------------------------------
# 1. Decomposition exacte : plancher + apport de segment + apport individuel
# ---------------------------------------------------------------------------

def decomposer_accord(codes, x_nom, y_nom, attaques_idx, pool_idx, items, seg):
    """Pour une paire (X attaquant, Y bassin), l'accord (1 - distance de Hamming) de
    chaque personne a son vrai jumeau, a la moyenne des autres membres de son segment, et
    a la moyenne de tout le reste du bassin. Renvoie un DataFrame indexe par la position
    de la personne dans attaques_idx (jamais son pid).
    """
    vec_test = codes[x_nom][attaques_idx][:, items]
    pool = codes[y_nom][pool_idx][:, items]
    accord = 1.0 - distance_hamming(vec_test, pool)          # (n_test, n_pool)

    vrai_idx = np.searchsorted(pool_idx, attaques_idx)        # position du vrai jumeau
    n_test, n_pool = accord.shape

    seg_row = seg[attaques_idx]           # segment de la personne attaquee (verite)
    seg_col = seg[pool_idx]               # segment de chaque membre du bassin

    segs = np.unique(seg_col[seg_col >= 0])
    g_max = int(segs.max()) + 1 if len(segs) else 0
    S = np.zeros((n_pool, g_max))
    for g in segs:
        S[:, g] = (seg_col == g)
    col_count = S.sum(axis=0)                                  # taille de segment dans le bassin

    ligne_totale = accord.sum(axis=1)
    accord_vrai = accord[np.arange(n_test), vrai_idx]

    seg_sum_par_ligne = accord @ S                             # (n_test, g_max)
    valide = (seg_row >= 0) & (seg_row < g_max)

    meme_seg_sum = np.full(n_test, np.nan)
    meme_seg_n = np.full(n_test, np.nan)
    for i in np.flatnonzero(valide):
        g = seg_row[i]
        meme_seg_sum[i] = seg_sum_par_ligne[i, g] - accord_vrai[i]
        meme_seg_n[i] = col_count[g] - 1

    plancher_n = (n_pool - 1)
    plancher = (ligne_totale - accord_vrai) / plancher_n
    with np.errstate(invalid="ignore", divide="ignore"):
        accord_meme_segment = np.where(meme_seg_n > 0, meme_seg_sum / np.maximum(meme_seg_n, 1),
                                        np.nan)

    return pd.DataFrame({
        "config_x": x_nom, "config_y": y_nom,
        "accord_vrai": accord_vrai,
        "plancher": plancher,
        "accord_meme_segment": accord_meme_segment,
        "taille_segment": meme_seg_n + 1,
    })


# ---------------------------------------------------------------------------
# 2. Temoin de population pure : mode de segment leave-one-out
# ---------------------------------------------------------------------------

def profil_mode_segment_loo(mat, seg):
    """Pour chaque personne, le profil ou chaque item est remplace par le code le plus
    frequent DANS SON SEGMENT, en excluant sa propre reponse (leave-one-out). Ex aequo
    tranches par le plus petit code (deterministe). -1 si le segment est inconnu ou si
    la personne est seule dans son segment (aucun mode leave-one-out defini)."""
    n, m = mat.shape
    profil = np.full((n, m), -1, dtype=np.int32)
    segs = np.unique(seg[seg >= 0])
    for g in segs:
        idx = np.flatnonzero(seg == g)
        if len(idx) < 2:
            continue
        sous = mat[idx]                       # (n_g, m)
        for j in range(m):
            col = sous[:, j]
            k_max = int(col.max()) + 1
            comptes = np.bincount(col, minlength=k_max)
            for pos, i in enumerate(idx):
                v = col[pos]
                c = comptes.copy()
                c[v] -= 1
                profil[i, j] = int(np.argmax(c))
    return profil


def temoin_population(codes, x_nom, y_nom, attaques_idx, pool_idx, items, seg, rng):
    """Top-1 d'identification quand le jumeau Y est remplace par le mode leave-one-out de
    son segment S_fin. rangs_attaque est reprise sans modification."""
    vec_test = codes[x_nom][attaques_idx][:, items]
    pool_reel = codes[y_nom][pool_idx][:, items]
    seg_pool = seg[pool_idx]

    profil = profil_mode_segment_loo(pool_reel, seg_pool)
    couverts = np.flatnonzero((profil >= 0).all(axis=1))     # segment connu et taille >= 2
    if len(couverts) < 5:
        return None
    pool_idx_c = pool_idx[couverts]
    attaques_c = np.intersect1d(attaques_idx, pool_idx_c)
    if len(attaques_c) < 5:
        return None

    vrai_idx = np.searchsorted(pool_idx_c, attaques_c)
    vec_test_c = codes[x_nom][attaques_c][:, items]
    pool_profil = profil[couverts]

    rang, top1, top10 = rangs_attaque(vec_test_c, pool_profil, vrai_idx, rng)
    m_t1, b_t1, h_t1 = resume_taux(top1, [GRAINE, graine_nom(f"{x_nom}|{y_nom}|modeseg"), 1])
    taille_med = float(np.median(np.bincount(seg_pool[seg_pool >= 0])[
        np.bincount(seg_pool[seg_pool >= 0]) > 0]))
    return {"config_x": x_nom, "config_y": y_nom, "n_attaques": len(attaques_c),
            "n_pool": len(pool_profil), "top1_mode_segment": m_t1,
            "top1_mode_segment_bas": b_t1, "top1_mode_segment_haut": h_t1,
            "hasard_pool": 1.0 / len(pool_profil), "taille_segment_mediane": taille_med}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    couverture = paq["couverture"]
    seg = paq["seg"][SEG]
    vals, comptes = np.unique(seg[seg >= 0], return_counts=True)
    print(f"segmentation {SEG} : {len(vals)} segments, taille mediane "
          f"{np.median(comptes):.1f}, min {comptes.min()}, max {comptes.max()}, "
          f"couverture {int((seg >= 0).sum())}/{len(seg)}", flush=True)

    paires = paires_riches_60_items(codes, couverture)
    print(f"{len(paires)} paires riches a 60 items communs", flush=True)

    # --- section 1 : decomposition exacte, personne par personne, paire par paire ---
    # ATTENTION vie privee : `decomposer_accord` renvoie un DataFrame indexe par la POSITION
    # de la personne (un entier interne), qui serait reversible au pid public par simple
    # alignement d'ordre sur le CSV Twin-2K-500. Conformement a la regle deja posee par
    # c7_reidentification ("aucun pid, aucune liste d'appariements individuels, seuls des
    # taux agreges sortent dans resultats/"), ce niveau personne x paire reste EN MEMOIRE et
    # n'est agrege QUE par paire (30 lignes, aucun index de personne) avant d'etre ecrit.
    morceaux = []
    par_personne_listes = []
    for x_nom, y_nom, attaques_idx, pool_idx, items in paires:
        d = decomposer_accord(codes, x_nom, y_nom, attaques_idx, pool_idx, items, seg)
        morceaux.append({
            "config_x": x_nom, "config_y": y_nom, "n_personnes": len(d),
            "plancher_paire": d["plancher"].mean(),
            "accord_meme_segment_paire": d["accord_meme_segment"].mean(),
            "accord_vrai_paire": d["accord_vrai"].mean(),
        })
        d = d.set_index(attaques_idx)[["accord_vrai", "plancher", "accord_meme_segment"]]
        par_personne_listes.append(d)
    resume_paires = pd.DataFrame(morceaux)

    # moyenne par personne a travers les 30 paires (index = position interne, jamais ecrit
    # sur disque), puis bootstrap sur les personnes
    par_personne = pd.concat(par_personne_listes).groupby(level=0).mean()
    apport_segment = (par_personne["accord_meme_segment"] - par_personne["plancher"]).values
    apport_individuel = (par_personne["accord_vrai"] - par_personne["accord_meme_segment"]).values

    m_plancher, b_plancher, h_plancher = bootstrap_personnes(
        par_personne["plancher"].values, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 1])
    m_seg, b_seg, h_seg = bootstrap_personnes(
        par_personne["accord_meme_segment"].values, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 2])
    m_vrai, b_vrai, h_vrai = bootstrap_personnes(
        par_personne["accord_vrai"].values, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 3])
    m_apport_seg, b_apport_seg, h_apport_seg = bootstrap_personnes(
        apport_segment, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 4])
    m_apport_ind, b_apport_ind, h_apport_ind = bootstrap_personnes(
        apport_individuel, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 5])

    print("\n--- decomposition (accord = fraction d'items ou les deux jumeaux "
          "s'accordent, moyenne sur les 30 paires puis sur les personnes) ---", flush=True)
    print(f"plancher (accord de fond, hors segment)     : {m_plancher*100:.2f} "
          f"[{b_plancher*100:.2f};{h_plancher*100:.2f}] pts", flush=True)
    print(f"accord meme segment (permutation intra-seg) : {m_seg*100:.2f} "
          f"[{b_seg*100:.2f};{h_seg*100:.2f}] pts", flush=True)
    print(f"accord au vrai jumeau                        : {m_vrai*100:.2f} "
          f"[{b_vrai*100:.2f};{h_vrai*100:.2f}] pts", flush=True)
    print(f"  -> apport de segment  (meme-seg - plancher) : {m_apport_seg*100:.2f} "
          f"[{b_apport_seg*100:.2f};{h_apport_seg*100:.2f}] pts", flush=True)
    print(f"  -> apport individuel  (vrai - meme-seg)      : {m_apport_ind*100:.2f} "
          f"[{b_apport_ind*100:.2f};{h_apport_ind*100:.2f}] pts", flush=True)

    decomp = pd.DataFrame([{
        "plancher": m_plancher, "plancher_bas": b_plancher, "plancher_haut": h_plancher,
        "accord_meme_segment": m_seg, "accord_meme_segment_bas": b_seg,
        "accord_meme_segment_haut": h_seg,
        "accord_vrai": m_vrai, "accord_vrai_bas": b_vrai, "accord_vrai_haut": h_vrai,
        "apport_segment": m_apport_seg, "apport_segment_bas": b_apport_seg,
        "apport_segment_haut": h_apport_seg,
        "apport_individuel": m_apport_ind, "apport_individuel_bas": b_apport_ind,
        "apport_individuel_haut": h_apport_ind,
        "n_personnes": len(par_personne), "n_paires": len(paires),
    }])

    # --- section 2 : temoin de population pure (top-1, mode de segment leave-one-out) ---
    print("\n--- temoin population pure : top-1 par mode de segment leave-one-out ---",
          flush=True)
    lignes_temoin = []
    for x_nom, y_nom, attaques_idx, pool_idx, items in paires:
        rng = np.random.default_rng([GRAINE, graine_nom(f"{x_nom}|{y_nom}|modeseg")])
        r = temoin_population(codes, x_nom, y_nom, attaques_idx, pool_idx, items, seg, rng)
        if r is not None:
            lignes_temoin.append(r)
    df_temoin = pd.DataFrame(lignes_temoin)

    top1_mode_moyen = df_temoin.top1_mode_segment.mean()
    top1_mode_bas = df_temoin.top1_mode_segment_bas.mean()
    top1_mode_haut = df_temoin.top1_mode_segment_haut.mean()
    print(f"top-1 moyen (mode de segment, {len(df_temoin)} paires) : "
          f"{top1_mode_moyen*100:.2f} [{top1_mode_bas*100:.2f};{top1_mode_haut*100:.2f}] %",
          flush=True)

    # comparaison au top-1 individuel deja publie, relu depuis le disque (non recalcule)
    chemin_publie = os.path.join(T1.SORTIE, "c7-transfert-voletA.csv")
    top1_individuel_publie = np.nan
    if os.path.exists(chemin_publie):
        publie = pd.read_csv(chemin_publie)
        riches = [c for c in C7T.CONFIGURATIONS if c != C7T.DEMO]
        m60 = publie[(publie.config_x.isin(riches)) & (publie.config_y.isin(riches))
                      & (publie.n_items == 60)]
        top1_individuel_publie = m60.top1.mean()
        print(f"top-1 individuel deja publie (c7-transfert-voletA.csv, {len(m60)} paires "
              f"a 60 items) : {top1_individuel_publie*100:.2f} %", flush=True)
    else:
        print("c7-transfert-voletA.csv absent : comparaison au top-1 individuel impossible",
              flush=True)

    # --- verdict, critere preenregistre ---
    print("\n--- verdict (critere preenregistre) ---", flush=True)
    seuil_destructeur = (SEUIL_DESTRUCTEUR_RATIO * top1_individuel_publie
                         if np.isfinite(top1_individuel_publie) else np.nan)
    cond1 = bool(np.isfinite(seuil_destructeur) and top1_mode_moyen >= seuil_destructeur)
    cond2 = bool(m_apport_ind <= m_apport_seg)
    refute = cond1 or cond2
    print(f"top-1 mode-segment ({top1_mode_moyen*100:.2f} %) >= seuil destructeur "
          f"({seuil_destructeur*100:.2f} %) ? {cond1}", flush=True)
    print(f"apport_individuel ({m_apport_ind*100:.2f} pts) <= apport_segment "
          f"({m_apport_seg*100:.2f} pts) ? {cond2}", flush=True)
    print(f"A2 refutee par ce temoin = {refute}", flush=True)

    # --- ecriture : UNE seule sortie CSV, uniquement des agreges par paire (30 lignes)
    # plus une ligne de synthese globale (bootstrap sur les personnes) ; aucun index de
    # personne, conformement a la regle de vie privee de c7_reidentification. ---
    table = resume_paires.merge(
        df_temoin[["config_x", "config_y", "n_pool", "top1_mode_segment",
                   "top1_mode_segment_bas", "top1_mode_segment_haut", "hasard_pool",
                   "taille_segment_mediane"]],
        on=["config_x", "config_y"], how="left")
    synthese = pd.DataFrame([{
        "config_x": "TOUTES (moyenne 30 paires)", "config_y": "", "n_personnes": len(par_personne),
        "plancher_paire": m_plancher, "accord_meme_segment_paire": m_seg,
        "accord_vrai_paire": m_vrai,
        "plancher_bas": b_plancher, "plancher_haut": h_plancher,
        "accord_meme_segment_bas": b_seg, "accord_meme_segment_haut": h_seg,
        "accord_vrai_bas": b_vrai, "accord_vrai_haut": h_vrai,
        "apport_segment": m_apport_seg, "apport_segment_bas": b_apport_seg,
        "apport_segment_haut": h_apport_seg,
        "apport_individuel": m_apport_ind, "apport_individuel_bas": b_apport_ind,
        "apport_individuel_haut": h_apport_ind,
        "top1_mode_segment": top1_mode_moyen, "top1_mode_segment_bas": top1_mode_bas,
        "top1_mode_segment_haut": top1_mode_haut,
        "top1_individuel_publie": top1_individuel_publie,
        "seuil_destructeur": seuil_destructeur,
        "A2_refutee": refute,
    }])
    table = pd.concat([table, synthese], ignore_index=True)
    T1.ecrire(table, "c7-temoin-prompt.csv")


if __name__ == "__main__":
    main()
