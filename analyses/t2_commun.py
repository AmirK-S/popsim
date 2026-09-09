"""
t2_commun : briques partagees par T2, la version agregee de « qui bouge » et le
transport du nul a derive de C1 sur les panels GSS.

Statut : script d'analyse jetable. Aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie : i1_commun, a12_retest_delai, a2_commun,
a30_commun, a44_commun (par i1) et c1_commun sont importes tels quels.

LE PREENREGISTREMENT EST resultats/t2-preenregistrement.md, ECRIT AVANT CE FICHIER,
le 9 septembre 2026 a 01 h 05 CEST.

Ce module porte six choses et rien d'autre.

  1. Le chargement des deux perimetres de i1 (quatre ans, deux ans) et leur cache local,
     hors du depot.
  2. Les groupes du preenregistrement section 2 : camp, age, education, genre et leurs
     croisements, avec la regle d'effectif.
  3. Le repere ordinal : quels items du noyau commun sont marques ordinaux par le
     question_master de Stanford, et la valeur numerique brute du GSS derriere chaque
     code d'alphabet.
  4. Les quantites par personne et par item qui alimentent tout le volet 1 :
     changement observe, changement predit, deplacement observe et predit projetes sur
     la derive de l'item, deplacement ordinal observe et predit.
  5. Le nul a derive de C1 transpose : remelange de la vague d'arrivee dans le panel (N1)
     ou dans le segment (N2).
  6. Les outils d'agregation ponderee, de bootstrap sur les personnes et de correction.

Aucune microdonnee n'est ecrite par ce module ni par aucun script t2_*.
"""

import csv
import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import i1_commun as I1
import a12_retest_delai as A12
from a2_baselines_gss import FAMILLES  # noqa: F401  familles thematiques de a12

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
QCAT = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                            "question_master/gss/groups/categorical.csv")
QMAIN = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                             "question_master/gss/main.csv")

CACHE = os.environ.get(
    "T2_CACHE",
    "/private/tmp/claude-501/-Users-amirkellousidhoum-Desktop-Code-Projets-popsim/"
    "a472cb16-733d-4672-998b-78e94a129780/scratchpad")

GRAINE = 20260909
N_BOOTSTRAP = 400
N_PERMUTATIONS = 200
N_REPLICATS_NUL = 50
N_REPETITIONS = 5          # coupures 50 / 50 des personnes
MIN_GROUPE = 200           # effectif minimal d'un groupe
MIN_CELLULE = 50           # effectif minimal d'une cellule (groupe, item) de chaque cote
MIN_MODALITE_TRANSITION = 5  # sous ce seuil la ligne de transition retombe sur l'item


# ---------------------------------------------------------------------------
# 1. Perimetres
# ---------------------------------------------------------------------------

def charger(perimetre="4ans", forcer=False):
    """Construit le paquet personne x item d'un perimetre de i1, avec cache local.

    Le cache est ecrit hors du depot (variable T2_CACHE) : il contient des microdonnees
    et ne doit jamais entrer dans resultats/ ni dans data/.
    """
    os.makedirs(CACHE, exist_ok=True)
    chemin = os.path.join(CACHE, f"t2-paquet-{perimetre}.npz")
    meta = os.path.join(CACHE, f"t2-paquet-{perimetre}.json")
    if os.path.exists(chemin) and not forcer:
        z = np.load(chemin, allow_pickle=True)
        with open(meta, encoding="utf-8") as f:
            m = json.load(f)
        paquet = {k: z[k] for k in z.files}
        paquet["items"] = m["items"]
        paquet["k_par_item"] = m["k_par_item"]
        paquet["valeurs"] = [np.array(v, dtype=float) for v in m["valeurs"]]
        paquet["demos"] = {d: paquet.pop("demo_" + d) for d in I1.DEMOS}
        paquet["n"] = int(paquet["c_a"].shape[0])
        return paquet

    noyau, brut, n_paires = I1.charger_panels()
    tables = I1.alphabet_panel(brut, len(noyau))
    paires = I1.PAIRES_4ANS if perimetre == "4ans" else I1.PAIRES_2ANS
    p = I1.assembler(paires, noyau, brut, tables)
    # valeurs numeriques brutes du GSS derriere chaque code d'alphabet
    valeurs = []
    for t in tables:
        v = np.full(max(len(t), 1), np.nan)
        for cle, idx in t.items():
            v[idx] = float(cle) if isinstance(cle, (int, float)) else np.nan
        valeurs.append(v)
    p["valeurs"] = valeurs
    dump = {"c_a": p["c_a"], "c_b": p["c_b"], "ok": p["ok"], "classe": p["classe"],
            "panel": p["panel"].astype(str), "segment": p["segment"].astype(str)}
    for d in I1.DEMOS:
        dump["demo_" + d] = p["demos"][d]
    np.savez_compressed(chemin, **dump)
    with open(meta, "w", encoding="utf-8") as f:
        json.dump({"items": list(p["items"]), "k_par_item": list(map(int, p["k_par_item"])),
                   "valeurs": [list(map(lambda x: None if not np.isfinite(x) else float(x), v))
                               for v in valeurs]}, f)
    p["valeurs"] = [np.array([np.nan if x is None else x for x in v], dtype=float)
                    for v in [list(map(lambda x: None if not np.isfinite(x) else float(x), v))
                              for v in valeurs]]
    return p


def controle_consistance():
    """Controle bloquant C1 : reproduire les deux consistances de a12 par ses fonctions."""
    items149 = A12.items_stanford()
    brut = {}
    for nom in A12.PANELS:
        mat, _, _, _ = A12.charger_panel(nom, items149)
        brut[nom] = mat
    compte = {it: 0 for it in items149}
    n_paires = 0
    par_delai = {2: [], 4: []}
    for nom in A12.PANELS:
        for a, b, d in A12.PANELS[nom]["paires"]:
            n_paires += 1
            _, par_item, _, _ = A12.consistance(brut[nom][a], brut[nom][b])
            for j, it in enumerate(items149):
                if np.isfinite(par_item[j]):
                    compte[it] += 1
    noyau = [it for it in items149 if compte[it] == n_paires]
    idx = [items149.index(it) for it in noyau]
    for nom in A12.PANELS:
        for a, b, d in A12.PANELS[nom]["paires"]:
            pp, _, _, _ = A12.consistance(brut[nom][a], brut[nom][b], idx)
            fini = np.isfinite(pp)
            par_delai[d].append((float(np.nanmean(pp[fini])), int(fini.sum())))
    out = {}
    for d in (2, 4):
        v = np.array([g for g, _ in par_delai[d]], dtype=float)
        w = np.array([n for _, n in par_delai[d]], dtype=float)
        out[d] = float(np.sum(v * w) / np.sum(w))
    return out, len(noyau)


# ---------------------------------------------------------------------------
# 2. Groupes
# ---------------------------------------------------------------------------

AXES_SIMPLES = ["camp", "age", "education", "genre"]
AXES_CROISES = [("camp", "age"), ("camp", "education"), ("camp", "genre"),
                ("age", "education"), ("age", "genre"), ("education", "genre")]


def _bloc_genre(v):
    if not np.isfinite(v):
        return "non renseigne"
    if int(v) == 1:
        return "homme"
    if int(v) == 2:
        return "femme"
    return "non renseigne"


def axes(paquet):
    """Les quatre axes simples, etiquettes de la vague de depart uniquement."""
    d = paquet["demos"]
    return {
        "camp": np.array([I1.bloc_ideologie(v) for v in d["polviews"]], dtype=object),
        "age": np.array([I1.bloc_age(v) for v in d["age"]], dtype=object),
        "education": np.array([I1.bloc_education(v) for v in d["degree"]], dtype=object),
        "genre": np.array([_bloc_genre(v) for v in d["sex"]], dtype=object),
    }


def parti(paquet):
    """Camp partisan, repliement standard de a30, pour le controle d'ancrage du volet 3.

    partyid du GSS : 0 a 6 de democrate fort a republicain fort, 7 = other party, ecarte.
    """
    out = []
    for v in paquet["demos"]["partyid"]:
        if not np.isfinite(v) or v > 6:
            out.append("non renseigne")
        elif v <= 2:
            out.append("gauche")
        elif v == 3:
            out.append("centre")
        else:
            out.append("droite")
    return np.array(out, dtype=object)


def groupes(paquet, min_groupe=MIN_GROUPE):
    """Tous les groupes retenus : axes simples plus croisements, seuil d'effectif.

    Retourne une liste de dictionnaires {axe, groupe, masque} et le tableau des axes.
    """
    ax = axes(paquet)
    liste = []
    for a in AXES_SIMPLES:
        for g in sorted(set(ax[a])):
            m = ax[a] == g
            if m.sum() >= min_groupe:
                liste.append({"axe": a, "groupe": g, "masque": m, "n": int(m.sum())})
    for a, b in AXES_CROISES:
        for ga in sorted(set(ax[a])):
            for gb in sorted(set(ax[b])):
                m = (ax[a] == ga) & (ax[b] == gb)
                if m.sum() >= min_groupe:
                    liste.append({"axe": f"{a} x {b}", "groupe": f"{ga} | {gb}",
                                  "masque": m, "n": int(m.sum())})
    return liste, ax


# ---------------------------------------------------------------------------
# 3. Repere ordinal
# ---------------------------------------------------------------------------

def items_ordinaux(items):
    """Marquage ordinal du question_master de Stanford, lu tel quel.

    Dans groups/categorical.csv, « Categorical = Y » veut dire nominal et « N » veut
    dire ordinal ; c'est la lecture de a1_double_distorsion.lire_nomenclature, reprise
    sans changement.
    """
    ordinal = {}
    with open(QCAT, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cle = [k for k in r if k.strip().lower().startswith("categorical")][0]
            ordinal[r["Question ID"].strip().lower()] = (r[cle].strip().upper() == "N")
    return np.array([bool(ordinal.get(it.lower(), False)) for it in items])


def valeurs_ordinales(paquet, est_ord):
    """Pour chaque item ordinal, le vecteur des valeurs numeriques brutes du GSS.

    Un item est retenu au volet ordinal si toutes ses modalites observees portent une
    valeur numerique finie. Retourne le masque des items retenus et une matrice
    (n_items, k_max) des valeurs, NaN ailleurs.
    """
    kmax = max(len(v) for v in paquet["valeurs"])
    V = np.full((len(paquet["items"]), kmax), np.nan)
    garde = np.zeros(len(paquet["items"]), dtype=bool)
    for j, v in enumerate(paquet["valeurs"]):
        k = paquet["k_par_item"][j]
        vv = np.asarray(v, dtype=float)[:k]
        V[j, :len(vv)] = vv
        garde[j] = est_ord[j] and np.isfinite(vv).all() and len(set(vv.tolist())) == len(vv)
    return garde, V


# ---------------------------------------------------------------------------
# 4. Quantites par personne et par item, sur une coupure en demi echantillons
# ---------------------------------------------------------------------------

def coupure(paquet, rep, graine=GRAINE):
    """Coupure 50 / 50 des personnes, stratifiee par panel. Retourne le masque de A."""
    rng = np.random.default_rng(graine + 1000 * rep)
    a = np.zeros(paquet["n"], dtype=bool)
    for pan in np.unique(paquet["panel"]):
        idx = np.flatnonzero(paquet["panel"] == pan)
        perm = rng.permutation(idx)
        a[perm[:len(perm) // 2]] = True
    return a


def transitions(paquet, masque_a, valeurs_ord, garde_ord):
    """Le modele de transition estime sur la moitie A, item par item, sans les groupes.

    Pour l'item j et la modalite de depart m, la ligne T[j][m] est la distribution des
    modalites d'arrivee des personnes de A qui donnent m en vague 1. Sous le seuil
    MIN_MODALITE_TRANSITION, la ligne retombe sur la distribution d'arrivee de l'item
    entier, ce qui est le repli le plus neutre.

    Retourne, pour toutes les personnes du perimetre et tous les items :
      chg        changement observe (0/1), NaN hors perimetre evaluable
      pchg       probabilite de changement predite par le modele de transition
      proj_obs   deplacement observe de la personne projete sur la derive de l'item (A)
      proj_pred  le meme, predit
      ord_obs    difference de code ordinal observee, NaN si item non ordinal
      ord_pred   la meme, predite
      u          direction de derive de chaque item, estimee sur A
    """
    ca, cb, ok = paquet["c_a"], paquet["c_b"], paquet["ok"]
    n, P = ca.shape
    kmax = max(paquet["k_par_item"])
    chg = np.where(ok, (ca != cb).astype(float), np.nan)
    pchg = np.full((n, P), np.nan)
    proj_obs = np.full((n, P), np.nan)
    proj_pred = np.full((n, P), np.nan)
    ord_obs = np.full((n, P), np.nan)
    ord_pred = np.full((n, P), np.nan)
    U = np.zeros((P, kmax))
    for j in range(P):
        k = paquet["k_par_item"][j]
        okj = ok[:, j]
        aj, bj = ca[:, j], cb[:, j]
        ma = okj & masque_a
        if ma.sum() < 2:
            continue
        p1 = np.bincount(aj[ma], minlength=k).astype(float)
        p2 = np.bincount(bj[ma], minlength=k).astype(float)
        p1 /= p1.sum()
        p2 /= p2.sum()
        delta = p2 - p1
        nrm = np.linalg.norm(delta)
        u = delta / nrm if nrm > 1e-12 else np.zeros(k)
        U[j, :k] = u
        # matrice de transition sur A
        T = np.zeros((k, k))
        for m in range(k):
            sel = ma & (aj == m)
            if sel.sum() >= MIN_MODALITE_TRANSITION:
                T[m] = np.bincount(bj[sel], minlength=k).astype(float) / sel.sum()
            else:
                T[m] = p2
        # quantites par personne
        idx = np.flatnonzero(okj)
        a_i, b_i = aj[idx], bj[idx]
        eye = np.eye(k)
        pchg[idx, j] = 1.0 - T[a_i, a_i]
        proj_obs[idx, j] = u[b_i] - u[a_i]
        proj_pred[idx, j] = (T[a_i] - eye[a_i]) @ u
        if garde_ord[j]:
            v = valeurs_ord[j, :k]
            ord_obs[idx, j] = v[b_i] - v[a_i]
            ord_pred[idx, j] = T[a_i] @ v - v[a_i]
    return {"chg": chg, "pchg": pchg, "proj_obs": proj_obs, "proj_pred": proj_pred,
            "ord_obs": ord_obs, "ord_pred": ord_pred, "u": U}


# ---------------------------------------------------------------------------
# 5. Le nul a derive de C1, transpose
# ---------------------------------------------------------------------------

def nul_amplitude(paquet, variante, n_replicats, rng, valeurs_ord=None, garde_ord=None):
    """Remelange de la vague d'arrivee, C1 section 6.3 transpose au GSS.

    variante « panel » : la permutation se fait entre les personnes du meme panel
    evaluees a l'item (N1). variante « segment » : entre les personnes du meme panel ET
    du meme segment ideologie x age x education (N2), pendant exact de la cohorte de C1.

    Les deux marginales de l'item, dans le groupe de permutation, sont conservees
    exactement ; l'appariement des personnes est detruit. Retourne, par personne, la
    moyenne sur les replicats du taux de changement et de la distance ordinale, plus le
    nombre d'items evalues, plus l'ecart maximal de marginale (controle C3).
    """
    ca, cb, ok = paquet["c_a"], paquet["c_b"], paquet["ok"]
    n, P = ca.shape
    if variante == "panel":
        cle = paquet["panel"].astype(str)
    else:
        cle = np.array([f"{p}|{s}" for p, s in
                        zip(paquet["panel"].astype(str), paquet["segment"].astype(str))],
                       dtype=object)
    groupes_perm = {}
    for g in np.unique(cle):
        groupes_perm[g] = np.flatnonzero(cle == g)
    n_chg = np.zeros(n)
    s_ord = np.zeros(n)
    n_ord = np.zeros(n)
    chg_par_item = np.zeros((n, P), dtype=np.float32)
    ecart_max = 0.0
    for _ in range(n_replicats):
        cbp = cb.copy()
        for j in range(P):
            for g, idx in groupes_perm.items():
                sel = idx[ok[idx, j]]
                if len(sel) > 1:
                    cbp[sel, j] = cb[rng.permutation(sel), j]
        chg = (ca != cbp) & ok
        n_chg += chg.sum(axis=1)
        chg_par_item += chg
        if garde_ord is not None:
            for j in np.flatnonzero(garde_ord):
                k = paquet["k_par_item"][j]
                v = valeurs_ord[j, :k]
                sel = np.flatnonzero(ok[:, j])
                s_ord[sel] += np.abs(v[cbp[sel, j]] - v[ca[sel, j]])
        # controle C3 : marginale d'arrivee conservee
        for j in range(0, P, 17):
            k = paquet["k_par_item"][j]
            m1 = np.bincount(cb[ok[:, j], j], minlength=k)
            m2 = np.bincount(cbp[ok[:, j], j], minlength=k)
            ecart_max = max(ecart_max, float(np.abs(m1 - m2).max()))
    if garde_ord is not None:
        n_ord = ok[:, garde_ord].sum(axis=1).astype(float)
    n_eval = ok.sum(axis=1).astype(float)
    return {"taux_nul": n_chg / np.maximum(n_eval * n_replicats, 1),
            "ord_nul": s_ord / np.maximum(n_ord * n_replicats, 1),
            "chg_par_item": chg_par_item,
            "n_eval": n_eval, "n_ord": n_ord, "ecart_marginale": ecart_max}


def amplitude_reelle(paquet, valeurs_ord=None, garde_ord=None):
    """Les memes quantites, observees."""
    ca, cb, ok = paquet["c_a"], paquet["c_b"], paquet["ok"]
    n_eval = ok.sum(axis=1).astype(float)
    n_chg = ((ca != cb) & ok).sum(axis=1).astype(float)
    s_ord = np.zeros(paquet["n"])
    n_ord = np.zeros(paquet["n"])
    if garde_ord is not None:
        for j in np.flatnonzero(garde_ord):
            k = paquet["k_par_item"][j]
            v = valeurs_ord[j, :k]
            sel = np.flatnonzero(ok[:, j])
            s_ord[sel] += np.abs(v[cb[sel, j]] - v[ca[sel, j]])
        n_ord = ok[:, garde_ord].sum(axis=1).astype(float)
    return {"taux": n_chg / np.maximum(n_eval, 1), "ord": s_ord / np.maximum(n_ord, 1),
            "n_eval": n_eval, "n_ord": n_ord}


# ---------------------------------------------------------------------------
# 6. Outils
# ---------------------------------------------------------------------------

def poids_bootstrap(n, b, rng):
    """Multiplicites multinomiales sur les personnes. Ligne 0 : le poids unitaire."""
    W = np.empty((b + 1, n), dtype=np.float32)
    W[0] = 1.0
    W[1:] = rng.multinomial(n, np.full(n, 1.0 / n), size=b).astype(np.float32)
    return W


def moyennes_ponderees(W, X, OK):
    """Moyenne ponderee colonne par colonne, en ignorant les cellules non evaluables.

    W : (B, n). X : (n, P) valeurs, NaN hors perimetre. OK : (n, P) 0/1.
    Retourne (num, den) de formes (B, P).
    """
    Xz = np.nan_to_num(np.asarray(X, dtype=np.float32), nan=0.0) * OK
    return W @ Xz, W @ OK


def ic(tirages, niveau=95):
    """Intervalle de confiance par percentiles du bootstrap."""
    t = np.asarray(tirages, dtype=float)
    t = t[np.isfinite(t)]
    if t.size == 0:
        return np.nan, np.nan
    lo = (100 - niveau) / 2.0
    return float(np.percentile(t, lo)), float(np.percentile(t, 100 - lo))


def p_bootstrap(tirages):
    """p bilateral d'un contraste par bootstrap : deux fois la masse du mauvais cote."""
    t = np.asarray(tirages, dtype=float)
    t = t[np.isfinite(t)]
    if t.size == 0:
        return np.nan
    p = 2.0 * min((t <= 0).mean(), (t >= 0).mean())
    return float(min(max(p, 1.0 / (t.size + 1)), 1.0))


def holm(p):
    return I1.holm(p)


def ecrire(lignes, nom):
    return I1.ecrire(lignes, nom)
