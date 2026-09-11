"""
c7_bits : convertir la fuite de C7 en bits d'identite, puis en bits par point d'exactitude.

===========================================================================
PREENREGISTREMENT : resultats/c7-bits-preenregistrement.md, ecrit le 12 septembre 2026,
AVANT ce fichier et avant tout calcul.

POURQUOI. C7 rapporte des taux top-1 (20,7 % sur Twin-2K-500, 65,7 % sur l'archive
Stanford). Un taux depend du pool, du nombre d'items et du jeu : il ne se transporte pas.
Ce script mesure la meme fuite en BITS D'IDENTITE (voie rang, minorant de
I(identite ; sortie)), la met en regard de l'UTILITE (gain d'exactitude sur la modalite
modale de l'item), et en tire le rapport bits par point d'exactitude.

ETUDE DE RISQUE DE VIE PRIVEE sur deux jeux deja publics. Ce script ne calcule, n'imprime
et n'ecrit JAMAIS d'identifiant, de pid, d'email ni d'appariement individuel. Seules des
quantites agregees sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                  les quinze tables de Twin
  t1_baselines.calculer              B0, B1, B2, PMM k=10 (cible restreinte aux 60 items)
  a2_commun.distance_hamming         la distance de Hamming masquee
  c7_reidentification.items_communs  les 60 items toujours renseignes
  c7_stanford.charger_domaine / coder_categoriel_commun / accord_categoriel
                                     le bloc GSS de l'archive Stanford

CE QUI EST NOUVEAU ICI : les estimateurs de bits d'identite (bornage dyadique de
l'entropie du rang + Miller-Madow), l'information mutuelle par item corrigee du biais,
le couple (utilite, fuite) et son rapport, et la normalisation par l'entropie humaine qui
rend la mesure comparable entre jeux.

POURQUOI LES RANGS SONT RECALCULES ICI. c7_reidentification.rangs_attaque et
c7_stanford.rangs_depuis_accord renvoient le rang MOYENNE sur les tirages de departage des
ex aequo. Moyenner ecrase la dispersion du rang et gonflerait artificiellement les bits
(un predicteur constant, tous ses candidats ex aequo, verrait son rang moyen se concentrer
vers N/2 et paraitrait informatif). La fonction locale rangs_tous_tirages garde donc les
tirages separes ; elle est verifiee contre les taux top-1 publies de C7.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_bits.py
===========================================================================
"""

import os
import pickle
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")          # deux runs llama.cpp tournent : rester leger

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                        # noqa: E402
import t1_baselines as TB                                     # noqa: E402
import c7_stanford as S                                       # noqa: E402
from a2_commun import distance_hamming                        # noqa: E402
from c7_reidentification import items_communs, REF_V4, REF_V13, CONFIGURATIONS  # noqa: E402

GRAINE = 20260912
N_TIRAGES_LIENS = 20
N_BOOTSTRAP = 2000
LN2 = np.log(2.0)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
CACHE_BASELINES = os.environ.get(
    "C7_BITS_CACHE", "/tmp/c7-bits-baselines-60.pkl")

STATS_TWIN = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]


# ---------------------------------------------------------------------------
# 1. Estimateurs d'entropie et d'information
# ---------------------------------------------------------------------------

def entropie_mm(comptes, n_effectif=None):
    """Entropie de Shannon en bits, corrigee Miller-Madow.

    H_MM = H_plugin + (m_observe - 1) / (2 n ln 2). Le plug-in sous-estime l'entropie ;
    corriger vers le haut diminue les bits de fuite, c'est donc le sens conservateur.
    n_effectif permet de declarer moins d'observations independantes qu'il n'y a de
    comptes (cas des tirages de departage des ex aequo, non independants entre eux).
    """
    comptes = np.asarray(comptes, dtype=float)
    comptes = comptes[comptes > 0]
    n = comptes.sum()
    if n <= 0:
        return float("nan")
    p = comptes / n
    h = float(-(p * np.log2(p)).sum())
    n_eff = n if n_effectif is None else float(n_effectif)
    return h + (len(comptes) - 1) / (2.0 * n_eff * LN2)


def bins_dyadiques(n_pool):
    """Bins de rang {1}, {2,3}, {4..7}, ... et leur log2(taille). Renvoie aussi, pour
    chaque rang 1..n_pool, l'indice de son bin."""
    bornes = []
    debut = 1
    while debut <= n_pool:
        fin = min(2 * debut - 1, n_pool)
        bornes.append((debut, fin))
        debut = fin + 1
    tailles = np.array([f - d + 1 for d, f in bornes], dtype=float)
    idx = np.zeros(n_pool + 1, dtype=np.int32)
    for b, (d, f) in enumerate(bornes):
        idx[d:f + 1] = b
    return idx, np.log2(tailles)


def bits_depuis_comptes_bins(comptes, log2_tailles, n_pool, n_effectif):
    """Bits d'identite par la voie rang, borne dyadique.

    H(R) <= H(B) + somme_b p(b) log2|b| : l'entropie du rang est majoree par celle de son
    bin plus l'entropie maximale a l'interieur du bin. Les bits valent
    log2(N) - cette majoration, donc un MINORANT de log2(N) - H(R), lui-meme minorant de
    I(identite ; sortie) puisque l'ordre des candidats est une fonction de la sortie.
    """
    comptes = np.asarray(comptes, dtype=float)
    total = comptes.sum()
    if total <= 0:
        return float("nan")
    p = comptes / total
    h_bin = entropie_mm(comptes, n_effectif=n_effectif)
    borne_h_rang = h_bin + float((p * log2_tailles).sum())
    return float(np.log2(n_pool) - borne_h_rang)


def bits_plugin(rangs_plats, n_pool, n_effectif):
    """Estimateur secondaire : plug-in sur les N rangs + Miller-Madow, sans bornage.
    Biaise vers le haut pour les bits (l'entropie du rang est sous-estimee malgre la
    correction quand N est du meme ordre que n) : rapporte a titre de comparaison."""
    comptes = np.bincount(rangs_plats.astype(np.int64), minlength=n_pool + 1)[1:]
    h = entropie_mm(comptes, n_effectif=n_effectif)
    return float(np.log2(n_pool) - h)


def mi_mm(x, y):
    """Information mutuelle empirique en bits entre deux colonnes de codes entiers
    (-1 = manquant), corrigee Miller-Madow sur chacune des trois entropies.

    I_MM = I_plugin + [(m_x - 1) + (m_y - 1) - (m_xy - 1)] / (2 n ln 2). Le plug-in de
    l'information mutuelle est biaise vers le HAUT : la correction le tire vers le bas,
    sens conservateur pour une mesure de fuite.
    """
    ok = (x >= 0) & (y >= 0)
    n = int(ok.sum())
    if n < 2:
        return float("nan")
    xa, ya = x[ok], y[ok]
    vx, ix = np.unique(xa, return_inverse=True)
    vy, iy = np.unique(ya, return_inverse=True)
    if len(vx) < 2 or len(vy) < 2:
        return 0.0
    conj = np.bincount(ix * len(vy) + iy, minlength=len(vx) * len(vy)).astype(float)
    pxy = conj / n
    px = pxy.reshape(len(vx), len(vy)).sum(axis=1)
    py = pxy.reshape(len(vx), len(vy)).sum(axis=0)

    def h(p):
        p = p[p > 0]
        return float(-(p * np.log2(p)).sum())

    i_plugin = h(px) + h(py) - h(pxy)
    m_xy = int((conj > 0).sum())
    corr = ((len(vx) - 1) + (len(vy) - 1) - (m_xy - 1)) / (2.0 * n * LN2)
    return float(i_plugin + corr)


def entropie_item(col):
    """Entropie humaine d'un item, en bits, corrigee Miller-Madow."""
    vals = col[col >= 0]
    if len(vals) == 0:
        return float("nan")
    _, comptes = np.unique(vals, return_counts=True)
    return entropie_mm(comptes)


# ---------------------------------------------------------------------------
# 2. Attaque : rangs, tous les tirages conserves
# ---------------------------------------------------------------------------

def rangs_tous_tirages(accord, vrai_idx, rng, n_tirages=N_TIRAGES_LIENS):
    """Rang du vrai repondant, une colonne par tirage de departage des ex aequo.

    Memes conventions que c7_reidentification.rangs_attaque (bruit i.i.d. sur les scores
    d'accord avant tri, pour qu'aucun raccourci d'index n'imite une identification), mais
    les tirages ne sont PAS moyennes : la dispersion du rang est la matiere premiere de
    l'entropie. Renvoie une matrice (n_test, n_tirages) d'entiers >= 1.
    """
    n = accord.shape[0]
    out = np.zeros((n, n_tirages), dtype=np.int32)
    for t in range(n_tirages):
        bruit = rng.random(accord.shape) * 1e-9
        ordre = np.argsort(-(accord + bruit), axis=1, kind="stable")
        place = np.argsort(ordre, axis=1)
        out[:, t] = place[np.arange(n), vrai_idx] + 1
    return out


def bits_et_ic(rangs, n_pool, graine):
    """Bits d'identite (borne dyadique, chiffre principal) et IC 95 % bootstrap sur les
    personnes ; l'estimateur plug-in secondaire est renvoye a titre de comparaison."""
    idx_bin, log2_tailles = bins_dyadiques(n_pool)
    n_bins = len(log2_tailles)
    n_pers, n_tir = rangs.shape
    bins_pers = np.zeros((n_pers, n_bins))
    for i in range(n_pers):
        bins_pers[i] = np.bincount(idx_bin[rangs[i]], minlength=n_bins)

    point = bits_depuis_comptes_bins(bins_pers.sum(axis=0), log2_tailles,
                                     n_pool, n_effectif=n_pers)
    plug = bits_plugin(rangs.ravel(), n_pool, n_effectif=n_pers)

    rng = np.random.default_rng(graine)
    tirages = np.empty(N_BOOTSTRAP)
    for b in range(N_BOOTSTRAP):
        idx = rng.integers(0, n_pers, n_pers)
        tirages[b] = bits_depuis_comptes_bins(bins_pers[idx].sum(axis=0), log2_tailles,
                                              n_pool, n_effectif=n_pers)
    return (point, float(np.percentile(tirages, 2.5)),
            float(np.percentile(tirages, 97.5)), plug,
            float((rangs == 1).mean()), float(np.median(rangs)))


# ---------------------------------------------------------------------------
# 3. Exactitude par personne
# ---------------------------------------------------------------------------

def exactitude_par_personne(pred, verite):
    """Part d'items ou la prediction egale la reponse humaine, par personne, sur les
    seules cellules renseignees des deux cotes. NaN si aucune cellule commune."""
    ok = (pred >= 0) & (verite >= 0)
    n = ok.sum(axis=1)
    juste = ((pred == verite) & ok).sum(axis=1)
    with np.errstate(invalid="ignore"):
        return np.where(n > 0, juste / np.maximum(n, 1), np.nan)


def mode_item(verite):
    """Vecteur constant : la modalite modale de chaque item, repetee pour tout le monde."""
    n, m = verite.shape
    out = np.full((n, m), -1, dtype=np.int32)
    for j in range(m):
        v = verite[:, j]
        v = v[v >= 0]
        if len(v):
            vals, cpt = np.unique(v, return_counts=True)
            out[:, j] = vals[int(np.argmax(cpt))]
    return out


def mode_segment(verite, seg):
    """La modalite modale de l'item DANS le segment de la personne ; repli sur la modale
    globale quand le segment est absent ou vide. Reference d'utilite plus exigeante."""
    out = mode_item(verite).copy()
    for g in np.unique(seg):
        if g is None or (isinstance(g, (int, np.integer)) and g < 0):
            continue
        membres = np.flatnonzero(seg == g)
        if len(membres) < 2:
            continue
        for j in range(verite.shape[1]):
            v = verite[membres, j]
            v = v[v >= 0]
            if len(v):
                vals, cpt = np.unique(v, return_counts=True)
                out[np.ix_(membres, [j])] = vals[int(np.argmax(cpt))]
    return out


def gain_et_ic(acc, acc_ref, graine):
    """Gain d'exactitude en points de pourcentage sur la reference, IC 95 % bootstrap
    apparie sur les personnes (meme reechantillon des deux cotes)."""
    ok = ~np.isnan(acc) & ~np.isnan(acc_ref)
    d = (acc[ok] - acc_ref[ok]) * 100.0
    rng = np.random.default_rng(graine)
    n = len(d)
    tir = rng.choice(d, size=(N_BOOTSTRAP, n), replace=True).mean(axis=1)
    return (float(d.mean()), float(np.percentile(tir, 2.5)),
            float(np.percentile(tir, 97.5)), float(np.nanmean(acc[ok])))


# ---------------------------------------------------------------------------
# 4. Twin-2K-500
# ---------------------------------------------------------------------------

def baselines_60(paq, items):
    """B0, B1, B2, PMM sur les seuls 60 items de l'attaque, via t1_baselines.calculer
    importe sans modification (chaque item y est ajuste independamment : restreindre la
    cible avant l'appel donne exactement les memes predictions qu'apres)."""
    if os.path.exists(CACHE_BASELINES):
        print(f"cache baselines : {CACHE_BASELINES}", flush=True)
        return pickle.load(open(CACHE_BASELINES, "rb"))
    t0 = time.time()
    paq60 = dict(paq)
    paq60["codes"] = {T1.REF: paq["codes"][T1.REF][:, items]}
    out = TB.calculer(paq60, avec_pmm=True)
    pickle.dump(out, open(CACHE_BASELINES, "wb"))
    print(f"baselines calculees en {time.time() - t0:.0f}s", flush=True)
    return out


def traiter_twin():
    print("\n=== Twin-2K-500 ===", flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    verite = codes[REF_V4][:, items].astype(np.int32)
    n_pool = verite.shape[0]
    n_items = len(items)
    print(f"{n_pool} personnes, {n_items} items communs", flush=True)

    base = baselines_60(paq, items)
    pred = {nom: base[nom].astype(np.int32) for nom in STATS_TWIN}
    for nom in CONFIGURATIONS:
        if nom in codes:
            pred[nom] = codes[nom][:, items].astype(np.int32)
    pred["retest humain v1-3"] = codes[REF_V13][:, items].astype(np.int32)

    ref_mode = mode_item(verite)
    ref_seg = mode_segment(verite, paq["seg"]["S_gra"])
    acc_mode = exactitude_par_personne(ref_mode, verite)
    acc_seg = exactitude_par_personne(ref_seg, verite)
    ent_items = np.array([entropie_item(verite[:, j]) for j in range(n_items)])
    print(f"entropie humaine totale des 60 items : {np.nansum(ent_items):.2f} bits "
          f"({np.nanmean(ent_items):.3f} par item)", flush=True)

    lignes, par_item = [], []
    for nom, x in pred.items():
        couverts = np.flatnonzero((x >= 0).any(axis=1))
        rng = np.random.default_rng([GRAINE, S.graine_domaine("twin|" + nom)])
        accord = 1.0 - distance_hamming(x[couverts], verite)
        rangs = rangs_tous_tirages(accord, couverts, rng)
        bits, b_bas, b_haut, plug, top1, rang_med = bits_et_ic(
            rangs, n_pool, [GRAINE, 11])
        acc = exactitude_par_personne(x, verite)
        gain, g_bas, g_haut, acc_moy = gain_et_ic(acc[couverts], acc_mode[couverts],
                                                  [GRAINE, 12])
        gain_s, gs_bas, gs_haut, _ = gain_et_ic(acc[couverts], acc_seg[couverts],
                                                [GRAINE, 13])
        mis = np.array([mi_mm(x[couverts, j], verite[couverts, j])
                        for j in range(n_items)])
        lignes.append(dict(
            jeu="Twin-2K-500", predicteur=nom, famille=famille(nom),
            n_attaques=len(couverts), n_pool=n_pool, n_items=n_items,
            top1=top1, rang_median=rang_med,
            bits=bits, bits_bas=b_bas, bits_haut=b_haut, bits_plugin=plug,
            bits_par_item=bits / n_items,
            bits_normalises=bits / float(np.nansum(ent_items)),
            exactitude=acc_moy, gain_pp=gain, gain_bas=g_bas, gain_haut=g_haut,
            gain_segment_pp=gain_s, gain_segment_bas=gs_bas, gain_segment_haut=gs_haut,
            mi_moyenne_par_item=float(np.nanmean(mis)),
            mi_somme_items=float(np.nansum(mis))))
        par_item.append(pd.DataFrame(dict(
            jeu="Twin-2K-500", predicteur=nom, item=np.arange(n_items),
            mi_bits=mis, entropie_humaine_bits=ent_items)))
        print(f"  {nom:45s} bits={bits:6.2f} [{b_bas:5.2f};{b_haut:5.2f}] "
              f"top1={top1:.3f} exact={acc_moy:.3f} gain={gain:+.2f} pp", flush=True)
    ctx = dict(paq=paq, verite=verite, pred=pred, items=items, ent=ent_items)
    return pd.DataFrame(lignes), pd.concat(par_item, ignore_index=True), ent_items, ctx


def famille(nom):
    if nom.startswith("retest") or nom.startswith("humains"):
        return "humain"
    if nom in STATS_TWIN or nom in ("B0 mode Stanford",):
        return "statistique"
    if nom in ("demographique", "composite", "enquete", "entretien", "persona"):
        return "LLM"
    return "LLM"


# ---------------------------------------------------------------------------
# 5. Stanford, bloc GSS
# ---------------------------------------------------------------------------

CONDITIONS_STANFORD = ["composite", "enquete", "entretien", "persona", "demographique"]


def traiter_stanford():
    print("\n=== archive Stanford, bloc GSS ===", flush=True)
    ordre, items, tables, _ = S.charger_domaine("gss")
    codes = S.coder_categoriel_commun(tables, items)
    verite = codes[S.VAGUE1].astype(np.int32)
    n_pool, n_items = verite.shape
    print(f"{n_pool} personnes, {n_items} items", flush=True)

    pred = {c: codes[c].astype(np.int32) for c in CONDITIONS_STANFORD if c in codes}
    pred["retest humain vague 2"] = codes[S.VAGUE2].astype(np.int32)
    pred["B0 mode Stanford"] = mode_item(verite)

    acc_mode = exactitude_par_personne(pred["B0 mode Stanford"], verite)
    ent_items = np.array([entropie_item(verite[:, j]) for j in range(n_items)])
    print(f"entropie humaine totale des {n_items} items : {np.nansum(ent_items):.2f} bits "
          f"({np.nanmean(ent_items):.3f} par item)", flush=True)

    vrai_idx = np.arange(n_pool)
    lignes, par_item = [], []
    for nom, x in pred.items():
        rng = np.random.default_rng([GRAINE, S.graine_domaine("stanford|" + nom)])
        accord = S.accord_categoriel(x, verite)
        rangs = rangs_tous_tirages(accord, vrai_idx, rng)
        bits, b_bas, b_haut, plug, top1, rang_med = bits_et_ic(
            rangs, n_pool, [GRAINE, 21])
        acc = exactitude_par_personne(x, verite)
        gain, g_bas, g_haut, acc_moy = gain_et_ic(acc, acc_mode, [GRAINE, 22])
        mis = np.array([mi_mm(x[:, j], verite[:, j]) for j in range(n_items)])
        lignes.append(dict(
            jeu="Stanford GSS", predicteur=nom,
            famille="humain" if nom.startswith("retest")
            else ("statistique" if nom.startswith("B0") else "LLM"),
            n_attaques=n_pool, n_pool=n_pool, n_items=n_items,
            top1=top1, rang_median=rang_med,
            bits=bits, bits_bas=b_bas, bits_haut=b_haut, bits_plugin=plug,
            bits_par_item=bits / n_items,
            bits_normalises=bits / float(np.nansum(ent_items)),
            exactitude=acc_moy, gain_pp=gain, gain_bas=g_bas, gain_haut=g_haut,
            gain_segment_pp=np.nan, gain_segment_bas=np.nan, gain_segment_haut=np.nan,
            mi_moyenne_par_item=float(np.nanmean(mis)),
            mi_somme_items=float(np.nansum(mis))))
        par_item.append(pd.DataFrame(dict(
            jeu="Stanford GSS", predicteur=nom, item=np.arange(n_items),
            mi_bits=mis, entropie_humaine_bits=ent_items)))
        print(f"  {nom:45s} bits={bits:6.2f} [{b_bas:5.2f};{b_haut:5.2f}] "
              f"top1={top1:.3f} exact={acc_moy:.3f} gain={gain:+.2f} pp", flush=True)
    ctx = dict(verite=verite, pred=pred, ordre=ordre, ent=ent_items)
    return pd.DataFrame(lignes), pd.concat(par_item, ignore_index=True), ent_items, ctx


# ---------------------------------------------------------------------------
# 6. Avenant du 12 septembre : information par item et pouvoir d'identification
#    (resultats/c7-bits-preenregistrement-avenant.md, ecrit avant cette section)
# ---------------------------------------------------------------------------

def a_et_c_par_item(x, verite, lignes):
    """Par item : a_j = P(sortie du jumeau = reponse de la VRAIE personne), et
    c_j = somme_c q_j(c) p_j(c) = P(la sortie coincide avec la reponse d'un candidat pris
    au hasard), q etant la loi des sorties du jumeau et p la marginale humaine du pool.

    delta_j = a_j - c_j est l'exces de coincidence sur lequel l'attaque par accord de
    Hamming trie les candidats. Un item ou le jumeau reproduit la marginale sans rien
    savoir de la personne a delta_j = 0, quelle que soit son entropie.
    """
    m = x.shape[1]
    a = np.full(m, np.nan)
    c = np.full(m, np.nan)
    for j in range(m):
        xj, yj = x[lignes, j], verite[lignes, j]
        ok = (xj >= 0) & (yj >= 0)
        if ok.sum() < 2:
            continue
        a[j] = float((xj[ok] == yj[ok]).mean())
        y_pool = verite[:, j]
        y_pool = y_pool[y_pool >= 0]
        if len(y_pool) == 0:
            continue
        mods = np.unique(np.concatenate([xj[ok], y_pool]))
        q = np.array([(xj[ok] == v).mean() for v in mods])
        p = np.array([(y_pool == v).mean() for v in mods])
        c[j] = float((q * p).sum())
    return a, c


def replier_age(vals, n_groupes=3):
    """Les modalites d'age repliees en trois groupes par ordre des modalites, pour que
    les cellules du controle d'information conditionnelle restent peuplees."""
    mods = sorted({str(v).strip() for v in vals if str(v).strip() not in ("", "nan")})
    if not mods:
        return np.zeros(len(vals), dtype=np.int32)
    taille = max(1, int(np.ceil(len(mods) / n_groupes)))
    rang = {m: min(i // taille, n_groupes - 1) for i, m in enumerate(mods)}
    return np.array([rang.get(str(v).strip(), -1) for v in vals], dtype=np.int32)


def cellule_grossiere(genre, age):
    """Cellule genre x age replie (<= 12 cellules), -1 si une des deux est absente."""
    g_mods = sorted({str(v).strip() for v in genre if str(v).strip() not in ("", "nan")})
    g_idx = {m: i for i, m in enumerate(g_mods)}
    a3 = replier_age(age)
    out = np.full(len(genre), -1, dtype=np.int32)
    for i, (g, a) in enumerate(zip(genre, a3)):
        gi = g_idx.get(str(g).strip(), -1)
        if gi >= 0 and a >= 0:
            out[i] = gi * 3 + a
    return out


def mi_conditionnelle(x, y, cellule, n_min=40):
    """I(X ; Y | C) = somme_c p(c) I_MM(X ; Y | C = c), cellules de moins de n_min
    personnes ecartees (et signalees par la part de population couverte)."""
    tot, n = 0.0, 0
    for g in np.unique(cellule):
        if g < 0:
            continue
        idx = np.flatnonzero(cellule == g)
        if len(idx) < n_min:
            continue
        v = mi_mm(x[idx], y[idx])
        if not np.isnan(v):
            tot += len(idx) * v
            n += len(idx)
    return (tot / n if n else float("nan")), (n / len(cellule) if len(cellule) else 0.0)


def regression_standardisee(y, X, noms, graine, n_boot=1000):
    """Poids standardises (regresseurs et reponse centres-reduits) et IC 95 % par
    bootstrap SUR LES ITEMS, plus la correlation simple de chaque regresseur."""
    y = np.asarray(y, dtype=float)
    X = np.asarray(X, dtype=float)
    ok = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
    y, X = y[ok], X[ok]

    def beta(yy, XX):
        sy = yy.std() or 1.0
        zx_sd = np.where(XX.std(axis=0) > 0, XX.std(axis=0), 1.0)
        A = np.column_stack([np.ones(len(yy)), (XX - XX.mean(axis=0)) / zx_sd])
        return np.linalg.lstsq(A, (yy - yy.mean()) / sy, rcond=None)[0][1:]

    b = beta(y, X)
    rng = np.random.default_rng(graine)
    tir = np.empty((n_boot, X.shape[1]))
    for i in range(n_boot):
        idx = rng.integers(0, len(y), len(y))
        tir[i] = beta(y[idx], X[idx])
    lignes = []
    for k, nom in enumerate(noms):
        r = float(np.corrcoef(y, X[:, k])[0, 1])
        lignes.append(dict(regresseur=nom, beta=float(b[k]),
                           beta_bas=float(np.percentile(tir[:, k], 2.5)),
                           beta_haut=float(np.percentile(tir[:, k], 97.5)),
                           r_simple=r, n_items=int(len(y))))
    return lignes


def phi_dependance(accord, vrai_idx, var_binom_c, k):
    """Facteur d'inflation de variance des scores de leurres : ecart type observe des
    accords contre les MAUVAIS candidats, divise par l'ecart type binomial attendu si les
    k items etaient independants. Il encaisse la dependance entre items et
    l'heterogeneite des personnes ; c'est le seul parametre transporte d'un jeu a l'autre.
    """
    m = np.ones(accord.shape, dtype=bool)
    m[np.arange(len(vrai_idx)), vrai_idx] = False
    leurres = accord[m]
    sd_obs = float(leurres.std())
    sd_binom = float(np.sqrt(var_binom_c / k))
    return sd_obs / sd_binom if sd_binom > 0 else float("nan"), float(leurres.mean()), sd_obs


def top1_modele(a_j, c_j, k, n_pool, phi):
    """Top-1 predit : P(la vraie personne bat les N-1 leurres), approximation normale.

    Score = part d'items ou la sortie coincide. Vraie personne : moyenne mean(a_j),
    variance mean(a_j(1-a_j))/k. Leurre : moyenne mean(c_j), variance
    mean(c_j(1-c_j))/k inflatee par phi^2. Integration numerique de
    P = integrale f_vraie(s) * Phi((s - mu_leurre)/sigma_leurre)^(N-1) ds.
    """
    from scipy.stats import norm
    a_j = a_j[~np.isnan(a_j)]
    c_j = c_j[~np.isnan(c_j)]
    mu_a, mu_c = float(a_j.mean()), float(c_j.mean())
    sd_a = float(np.sqrt((a_j * (1 - a_j)).mean() / k))
    sd_c = float(np.sqrt((c_j * (1 - c_j)).mean() / k)) * phi
    s = np.linspace(mu_a - 6 * sd_a, mu_a + 6 * sd_a, 6000)
    dens = norm.pdf(s, mu_a, sd_a)
    gagne = norm.cdf((s - mu_c) / sd_c) ** (n_pool - 1)
    return float(np.trapezoid(dens * gagne, s)), mu_a, mu_c, sd_a, sd_c


def partie_items(jeu, x_llm, x_demo, verite, lignes, cellule, ent_items, etiquettes=None):
    """Table par item (H, MI, MI conditionnelle, a, c, delta) et regressions declarees."""
    n_items = verite.shape[1]
    a, c = a_et_c_par_item(x_llm, verite, lignes)
    delta = a - c
    mi_llm = np.array([mi_mm(x_llm[lignes, j], verite[lignes, j]) for j in range(n_items)])
    mi_demo = np.array([mi_mm(x_demo[lignes, j], verite[lignes, j]) for j in range(n_items)])
    i_cond = mi_llm - mi_demo
    cond_vraie = np.full(n_items, np.nan)
    couverture = 0.0
    for j in range(n_items):
        cond_vraie[j], couverture = mi_conditionnelle(
            x_llm[lignes, j], verite[lignes, j], cellule[lignes])
    tab = pd.DataFrame(dict(
        jeu=jeu, item=np.arange(n_items), entropie_humaine_bits=ent_items,
        mi_jumeau_bits=mi_llm, mi_demographique_bits=mi_demo,
        information_conditionnelle_bits=i_cond,
        mi_conditionnelle_vraie_bits=cond_vraie,
        a_vraie_personne=a, c_candidat_hasard=c, delta_identification=delta,
        bloc=(etiquettes if etiquettes is not None else "")))
    reg3 = regression_standardisee(
        delta, np.column_stack([ent_items, i_cond, a]),
        ["entropie", "information conditionnelle", "justesse a_j"], [GRAINE, 31])
    reg2 = regression_standardisee(
        delta, np.column_stack([ent_items, i_cond]),
        ["entropie", "information conditionnelle"], [GRAINE, 32])
    reg2v = regression_standardisee(
        delta, np.column_stack([ent_items, cond_vraie]),
        ["entropie", "MI conditionnelle vraie"], [GRAINE, 33])
    for r in reg3:
        r.update(jeu=jeu, modele="delta ~ H + I_cond + a")
    for r in reg2:
        r.update(jeu=jeu, modele="delta ~ H + I_cond")
    for r in reg2v:
        r.update(jeu=jeu, modele="delta ~ H + MI cond. vraie")
    print(f"  {jeu} : couverture des cellules grossieres = {couverture:.2f}", flush=True)
    return tab, pd.DataFrame(reg3 + reg2 + reg2v), a, c


# ---------------------------------------------------------------------------
# 7. Ratio, figure, verdicts
# ---------------------------------------------------------------------------

def ajouter_ratio(df):
    """Bits par point d'exactitude gagne. Regle preenregistree : si le gain est <= 0 ou
    si son IC couvre 0, le ratio n'est pas calcule (NaN) et la ligne se lit « fuite sans
    gain d'exactitude mesurable »."""
    gain_utile = (df.gain_pp > 0) & (df.gain_bas > 0)
    df["gain_significatif"] = gain_utile
    df["ratio_bits_par_pp"] = np.where(gain_utile, df.bits / df.gain_pp.replace(0, np.nan),
                                       np.nan)
    return df


def figure(df, chemin):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception as e:                     # pragma: no cover
        print(f"matplotlib indisponible ({e}), figure non produite", flush=True)
        return
    couleurs = {"LLM": "#b2182b", "statistique": "#2166ac", "humain": "#4d4d4d"}
    marqueurs = {"Twin-2K-500": "o", "Stanford GSS": "^"}
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.6))
    for ax, jeu in zip(axes, ["Twin-2K-500", "Stanford GSS"]):
        d = df[df.jeu == jeu]
        for i_pt, (_, r) in enumerate(d.iterrows()):
            ax.errorbar(r.gain_pp, r.bits,
                        yerr=[[max(r.bits - r.bits_bas, 0)], [max(r.bits_haut - r.bits, 0)]],
                        xerr=[[max(r.gain_pp - r.gain_bas, 0)], [max(r.gain_haut - r.gain_pp, 0)]],
                        fmt=marqueurs[jeu], ms=6, lw=1, capsize=2,
                        color=couleurs.get(r.famille, "#777777"), alpha=0.9)
            etiq = T1.ETIQUETTE.get(r.predicteur, str(r.predicteur))
            ax.annotate(etiq[:20], (r.gain_pp, r.bits), fontsize=6,
                        xytext=(5, 4 if i_pt % 2 else -9),   # alternance deterministe
                        textcoords="offset points")
        ax.axhline(0, color="#999999", lw=0.6)
        ax.axvline(0, color="#999999", lw=0.6)
        ax.axhline(np.log2(d.n_pool.iloc[0]), color="#999999", lw=0.6, ls=":")
        ax.set_title(f"{jeu} (plafond log2 N = {np.log2(d.n_pool.iloc[0]):.1f} bits)",
                     fontsize=9)
        ax.set_xlabel("utilite : gain d'exactitude sur la modale de l'item (points)",
                      fontsize=8)
        ax.set_ylabel("fuite : bits d'identite (minorant)", fontsize=8)
        ax.tick_params(labelsize=7)
    poignees = [plt.Line2D([], [], color=c, marker="s", ls="", label=f)
                for f, c in couleurs.items()]
    axes[0].legend(handles=poignees, fontsize=7, loc="upper left")
    fig.tight_layout()
    fig.savefig(chemin, dpi=170)
    fig.savefig(chemin.replace(".png", ".svg"))
    print(f"ecrit : {chemin}", flush=True)


def partie_avenant(ctx_twin, ctx_stan, top1_twin_obs, top1_stan_obs):
    """Les quatre points de l'avenant : decomposition par item, regression, transport,
    prediction hors echantillon du top-1 de Stanford a k = 60."""
    print("\n=== avenant : information par item et pouvoir d'identification ===",
          flush=True)

    # --- Twin : jumeau = JSON Persona GPT4.1, demographique = B1 argmax ---
    paq, verite_tw = ctx_twin["paq"], ctx_twin["verite"]
    items_tw = ctx_twin["items"]
    x_llm_tw = ctx_twin["pred"]["JSON Persona - GPT4.1"]
    x_demo_tw = ctx_twin["pred"]["B1 argmax"]
    lig_tw = np.flatnonzero((x_llm_tw >= 0).any(axis=1))
    lab = T1._labels(T1.RACINE_TWIN, paq["ids"])
    cell_tw = cellule_grossiere(lab["QID12"].values, lab["QID13"].values)
    try:
        import c7_mecanisme as MEC
        achat = set(MEC.items_achat(paq).tolist())
        etiq_tw = np.array(["achat" if int(i) in achat else "opinion" for i in items_tw])
    except Exception as e:                                   # pragma: no cover
        print(f"bloc d'achat non identifie ({e}), etiquettes vides", flush=True)
        etiq_tw = np.array(["inconnu"] * len(items_tw))
    tab_tw, reg_tw, a_tw, c_tw = partie_items(
        "Twin-2K-500", x_llm_tw, x_demo_tw, verite_tw, lig_tw, cell_tw,
        ctx_twin["ent"], etiq_tw)

    # --- Stanford : jumeau = composite, demographique = condition demographique ---
    verite_st = ctx_stan["verite"]
    x_llm_st = ctx_stan["pred"]["composite"]
    x_demo_st = ctx_stan["pred"]["demographique"]
    lig_st = np.arange(verite_st.shape[0])
    d_demo = pd.read_csv(S.DEMO_CSV).set_index("email").loc[ctx_stan["ordre"]]
    cell_st = cellule_grossiere(d_demo["gender"].values, d_demo["age"].values)
    tab_st, reg_st, a_st, c_st = partie_items(
        "Stanford GSS", x_llm_st, x_demo_st, verite_st, lig_st, cell_st,
        ctx_stan["ent"], np.array(["gss"] * verite_st.shape[1]))

    tab = pd.concat([tab_tw, tab_st], ignore_index=True)
    reg = pd.concat([reg_tw, reg_st], ignore_index=True)
    T1.ecrire(tab, "c7-bits-par-item-avenant.csv")
    T1.ecrire(reg[["jeu", "modele", "regresseur", "beta", "beta_bas", "beta_haut",
                   "r_simple", "n_items"]], "c7-bits-regressions.csv")
    print("\nregressions (poids standardises, IC bootstrap sur les items) :", flush=True)
    print(reg[["jeu", "modele", "regresseur", "beta", "beta_bas", "beta_haut",
               "r_simple"]].to_string(index=False), flush=True)

    # --- anomalie achat / opinion sur Twin ---
    for bloc in ("achat", "opinion"):
        d = tab_tw[tab_tw.bloc == bloc]
        if len(d):
            print(f"Twin {bloc:8s} n={len(d):3d} delta median={d.delta_identification.median():.4f} "
                  f"entropie mediane={d.entropie_humaine_bits.median():.3f} "
                  f"I_cond median={d.information_conditionnelle_bits.median():.4f}", flush=True)

    # --- transport : phi mesure sur Twin, applique a Stanford ---
    k_tw, n_tw = len(items_tw), verite_tw.shape[0]
    accord_tw = 1.0 - distance_hamming(x_llm_tw[lig_tw], verite_tw)
    var_c_tw = float(np.nanmean(c_tw * (1 - c_tw)))
    phi_tw, mu_leurre, sd_leurre = phi_dependance(accord_tw, lig_tw, var_c_tw, k_tw)
    t1_tw_mod, mu_a, mu_c, sd_a, sd_c = top1_modele(a_tw, c_tw, k_tw, n_tw, phi_tw)
    print(f"\nTwin : a_moyen={mu_a:.4f} c_moyen={mu_c:.4f} (accord leurre observe "
          f"{mu_leurre:.4f}) phi={phi_tw:.2f} -> top-1 modele={t1_tw_mod:.4f} "
          f"contre observe {top1_twin_obs:.4f}", flush=True)

    n_st = verite_st.shape[0]
    t1_st60, a60, c60, _, _ = top1_modele(a_st, c_st, 60, n_st, phi_tw)
    t1_st177, *_ = top1_modele(a_st, c_st, verite_st.shape[1], n_st, phi_tw)
    print(f"Stanford : a_moyen={a60:.4f} c_moyen={c60:.4f}, phi TRANSPORTE de Twin "
          f"({phi_tw:.2f}) -> top-1 predit a k=60 : {t1_st60:.4f} contre 0,3400 observe "
          f"(prediction declaree dans [0,24 ; 0,44] : "
          f"{bool(0.24 <= t1_st60 <= 0.44)})", flush=True)
    print(f"           controle a k=177 : predit {t1_st177:.4f} contre "
          f"{top1_stan_obs:.4f} observe", flush=True)
    T1.ecrire(pd.DataFrame([
        dict(jeu="Twin-2K-500", k_items=k_tw, n_pool=n_tw, a_moyen=mu_a, c_moyen=mu_c,
             phi=phi_tw, phi_origine="mesure ici", top1_modele=t1_tw_mod,
             top1_observe=top1_twin_obs),
        dict(jeu="Stanford GSS", k_items=60, n_pool=n_st, a_moyen=a60, c_moyen=c60,
             phi=phi_tw, phi_origine="transporte de Twin", top1_modele=t1_st60,
             top1_observe=0.340),
        dict(jeu="Stanford GSS", k_items=verite_st.shape[1], n_pool=n_st, a_moyen=a60,
             c_moyen=c60, phi=phi_tw, phi_origine="transporte de Twin",
             top1_modele=t1_st177, top1_observe=top1_stan_obs),
    ]), "c7-bits-transport.csv")
    return tab, reg


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    d_twin, item_twin, ent_twin, ctx_twin = traiter_twin()
    d_stan, item_stan, ent_stan, ctx_stan = traiter_stanford()
    df = ajouter_ratio(pd.concat([d_twin, d_stan], ignore_index=True))
    T1.ecrire(df, "c7-bits.csv")
    T1.ecrire(pd.concat([item_twin, item_stan], ignore_index=True), "c7-bits-par-item.csv")
    figure(df, os.path.join(SORTIE, "c7-bits.png"))

    print("\n--- verdicts preenregistres ---", flush=True)
    tw = df[df.jeu == "Twin-2K-500"].set_index("predicteur")
    st = df[df.jeu == "Stanford GSS"].set_index("predicteur")

    # P4 : validation de l'estimateur et ordres de grandeur
    b0 = tw.loc["B0 mode"]
    print(f"P4a B0 mode : bits={b0.bits:.3f} IC [{b0.bits_bas:.3f};{b0.bits_haut:.3f}] "
          f"-> IC contient 0 : {bool(b0.bits_bas <= 0 <= b0.bits_haut)}", flush=True)
    stats = tw.loc[[n for n in ["B1 argmax", "B2 argmax", "PMM k=10"] if n in tw.index]]
    print(f"P4b max bits des predicteurs statistiques = {stats.bits.max():.3f} "
          f"(< 0,5 : {bool(stats.bits.max() < 0.5)})", flush=True)
    jp = tw.loc["JSON Persona - GPT4.1"]
    print(f"P4c JSON Persona GPT4.1 : bits={jp.bits:.2f} (>= 3 : {bool(jp.bits >= 3)})",
          flush=True)
    co = st.loc["composite"]
    print(f"P4d Stanford composite : bits={co.bits:.2f} (>= 6 : {bool(co.bits >= 6)})",
          flush=True)

    # P1 : ratio LLM contre PMM
    pmm = tw.loc["PMM k=10"]
    llm = tw[(tw.famille == "LLM")]
    if bool(pmm.gain_significatif) and llm.ratio_bits_par_pp.notna().any():
        r_llm = llm.ratio_bits_par_pp.max()
        print(f"P1 ratio max LLM={r_llm:.3f} contre PMM={pmm.ratio_bits_par_pp:.3f} "
              f"-> facteur {r_llm / pmm.ratio_bits_par_pp:.1f} "
              f"(>= 5 : {bool(r_llm >= 5 * pmm.ratio_bits_par_pp)})", flush=True)
    else:
        print(f"P1 repli declare : gain PMM = {pmm.gain_pp:+.2f} pp "
              f"[{pmm.gain_bas:+.2f};{pmm.gain_haut:+.2f}], ratio non calcule. "
              f"Comparaison en fuite a gain comparable : JSON 4.1 {jp.bits:.2f} bits "
              f"contre PMM {pmm.bits:.3f} bits, facteur "
              f"{jp.bits / max(pmm.bits, 1e-6):.0f} (>= 10 : "
              f"{bool(jp.bits >= 10 * max(pmm.bits, 1e-6))})", flush=True)

    # P2 : transportabilite
    m_tw = tw[tw.famille == "LLM"].bits_normalises.max()
    m_st = st[st.famille == "LLM"].bits_normalises.max()
    fac = max(m_tw, m_st) / max(min(m_tw, m_st), 1e-9)
    print(f"P2 bits normalises par l'entropie humaine : Twin {m_tw:.4f}, "
          f"Stanford {m_st:.4f}, facteur {fac:.2f} (<= 2 : {bool(fac <= 2)})", flush=True)
    print(f"   bits par item : Twin {tw[tw.famille=='LLM'].bits_par_item.max():.4f}, "
          f"Stanford {st[st.famille=='LLM'].bits_par_item.max():.4f}", flush=True)

    # P3 : plafond humain
    rt_tw = tw.loc["retest humain v1-3"]
    rt_st = st.loc["retest humain vague 2"]
    print(f"P3 retest Twin bits={rt_tw.bits:.2f} gain={rt_tw.gain_pp:+.2f} pp ; "
          f"Stanford bits={rt_st.bits:.2f} gain={rt_st.gain_pp:+.2f} pp -> domine : "
          f"{bool(rt_tw.bits >= tw[tw.famille=='LLM'].bits.max() and rt_st.bits >= st[st.famille=='LLM'].bits.max())}",
          flush=True)

    # coherence des deux voies
    print(f"\nvoie appariement (somme des MI par item, plafond indicatif) : "
          f"Twin JSON 4.1 {jp.mi_somme_items:.1f} bits contre voie rang {jp.bits:.2f} ; "
          f"Stanford composite {co.mi_somme_items:.1f} contre {co.bits:.2f}", flush=True)

    partie_avenant(ctx_twin, ctx_stan, float(jp.top1), float(co.top1))


if __name__ == "__main__":
    main()
