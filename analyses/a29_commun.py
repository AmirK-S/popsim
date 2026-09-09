"""
a29_commun : briques partagees par l'analyse des minorites d'opinion, question du
8 septembre 2026, "les modeles de langage gardent la moitie des minorites, mais pas
forcement les bonnes personnes".

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a2_commun,
a8_commun, a25_commun, a28_commun, et par leur intermediaire a2_baselines_gss,
a5_evaluer, a5_agents_locaux_gss, a25_mesures. La matrice de la foret aleatoire est
reprise du cache de a28, elle n'est pas redefinie ici.

Ce module porte cinq choses et rien d'autre.

  1. Le chargement, delegue a a28_commun.charger_tout : memes 1 052 personnes, memes
     149 items, memes plis, memes graines, memes 150 personnes du run local pour C2 et C3.
     La vague 2 des memes humains est recuperee comme une condition ordinaire, sous le
     nom "humains vague 2" : c'est le plafond de bruit, pas une methode.
  2. La definition des cellules minoritaires, celle de a8 section 6, reprise sans
     retouche par import de a8_commun.modalites_minoritaires. Une modalite est
     minoritaire si moins de 10 pour cent, puis moins de 20 pour cent, des repondants
     OBSERVES de l'item l'ont choisie. Le seuil est descriptif, il est calcule sur la
     population du perimetre et n'entre dans aucune prediction. Sur le perimetre 150 la
     reference est calculee sur ces 150 personnes, comme en a28 : c'est ce qui rend les
     deux tableaux comparables ligne a ligne avec a28-t3-minorites.csv.
  3. Le comptage par personne : pour chaque personne, le nombre de cellules evaluables,
     le nombre de reponses rares reelles, le nombre de reponses rares predites, le nombre
     de reponses rares justes, et les deux facons de se tromper en predisant une
     minorite. Tout le reste du rapport se deduit de ces six vecteurs.
  4. Les agregats et leurs intervalles : rappel, precision, F1, taux de fausses
     minorites, avec bootstrap sur les PERSONNES et non sur les cellules. Deux reponses
     d'une meme personne ne sont pas independantes ; un bootstrap sur les cellules
     donnerait un intervalle faussement etroit.
  5. La correlation par personne entre taux de rares reelles et taux de rares predites,
     son intervalle bootstrap sur les personnes, et son temoin par permutation des
     colonnes, qui detruit l'appariement personne par personne en gardant exactement la
     masse minoritaire predite item par item.

Convention de masque, reprise de a8 section 6 sans changement : une cellule est
evaluable des que la vraie reponse de la vague 1 est observee. Une prediction manquante
ou refusee compte comme une reponse non minoritaire et non comme une cellule absente.
C'est la convention la plus severe pour les methodes qui refusent de repondre, et le taux
de refus est rapporte a cote de chaque ligne pour que le lecteur puisse en tenir compte.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import sys

# Limite de quatre coeurs, posee avant l'import de numpy sinon elle est sans effet.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
from a2_commun import est_manquant
from a8_commun import modalites_minoritaires
from a25_commun import classe_norc

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260908
SEUILS = [0.10, 0.20]

ORDRE_METHODES = C28.ORDRE_METHODES
LLM = C28.LLM
STAT = C28.STAT
AXES = C28.AXES

# Les 13 methodes non humaines, avec le perimetre sur lequel elles sont declarees dans la
# famille d'hypotheses primaire. C2 et C3 n'existent que sur les 150 personnes du run.
PERIMETRE_NATUREL = {m: ("150" if m in ("C2", "C3") else "1052")
                     for m in ORDRE_METHODES if m != "humains vague 2"}

holm = C28.holm
benjamini_hochberg = C28.benjamini_hochberg
ecrire = C28.ecrire


# ---------------------------------------------------------------------------
# 1. Chargement
# ---------------------------------------------------------------------------

def charger(cache, cache_foret):
    """Paquet de a28, plus la vague 2 sortie du dictionnaire pour un usage direct."""
    paquet = C28.charger_tout(cache, cache_foret)
    paquet["y2"] = paquet["M"]["humains vague 2"]
    return paquet


def methodes_du_perimetre(paquet, nom_perimetre):
    """Liste ordonnee des conditions disponibles sur un perimetre, humains inclus."""
    toutes = [c for c in ORDRE_METHODES if c in paquet["M"]]
    if nom_perimetre == "1052":
        return [c for c in toutes if c not in ("C2", "C3")]
    return toutes


def perimetres(paquet):
    return {"150": np.asarray(paquet["lignes150"]),
            "1052": np.arange(len(paquet["ids"]))}


# ---------------------------------------------------------------------------
# 2. Cellules minoritaires
# ---------------------------------------------------------------------------

def observe(mat):
    """Matrice booleenne des cellules qui portent une valeur exploitable."""
    return np.array([[not est_manquant(v) for v in ligne] for ligne in mat], dtype=bool)


def appartient(mat, mods):
    """Matrice booleenne : la valeur de la cellule est une modalite minoritaire de l'item.

    mods est la liste, item par item, des modalites sous le seuil, telle que
    a8_commun.modalites_minoritaires la construit.
    """
    n, m = mat.shape
    out = np.zeros((n, m), dtype=bool)
    for j in range(m):
        s = mods[j]
        if not s:
            continue
        out[:, j] = np.fromiter((v in s for v in mat[:, j]), dtype=bool, count=n)
    return out


# ---------------------------------------------------------------------------
# 3. Comptage par personne
# ---------------------------------------------------------------------------

def compter(pred, verite, mods):
    """Six vecteurs par personne, sur un perimetre et un seuil donnes.

    n_eval        : cellules evaluables, c'est a dire vraie reponse observee ;
    n_rare_vrai   : cellules dont la vraie reponse est minoritaire ;
    n_rare_pred   : cellules dont la PREDICTION est une modalite minoritaire ;
    n_juste       : cellules ou la prediction est minoritaire et egale a la verite ;
    n_faux_maj    : cellules ou la prediction est minoritaire et la vraie reponse
                    MAJORITAIRE, c'est a dire une minorite attribuee a une personne qui
                    n'en donne pas sur cet item ;
    n_faux_min    : cellules ou la prediction est minoritaire et la vraie reponse est une
                    AUTRE modalite minoritaire, c'est a dire la bonne personne mais la
                    mauvaise minorite ;
    n_refus       : cellules evaluables ou la methode ne rend aucune reponse.
    Par construction n_rare_pred = n_juste + n_faux_maj + n_faux_min.
    """
    ok = observe(verite)
    rare_vrai = appartient(verite, mods) & ok
    dispo = observe(pred)
    rare_pred = appartient(pred, mods) & ok & dispo
    juste = rare_pred & (pred == verite)
    faux_min = rare_pred & ~juste & rare_vrai
    faux_maj = rare_pred & ~juste & ~rare_vrai
    return {
        "n_eval": ok.sum(axis=1).astype(float),
        "n_rare_vrai": rare_vrai.sum(axis=1).astype(float),
        "n_rare_pred": rare_pred.sum(axis=1).astype(float),
        "n_juste": juste.sum(axis=1).astype(float),
        "n_faux_maj": faux_maj.sum(axis=1).astype(float),
        "n_faux_min": faux_min.sum(axis=1).astype(float),
        "n_refus": (ok & ~dispo).sum(axis=1).astype(float),
        "_rare_vrai": rare_vrai,
        "_rare_pred": rare_pred,
        "_juste": juste,
        "_ok": ok,
    }


def agreger(c, idx=None):
    """Rappel, precision, F1 et taux de fausses minorites a partir des comptes.

    idx, s'il est fourni, est un vecteur d'indices de personnes : c'est le tirage
    bootstrap. Les sommes sont refaites sur les personnes tirees, jamais sur les cellules.
    """
    def s(cle):
        v = c[cle]
        return float(v[idx].sum()) if idx is not None else float(v.sum())

    juste, rv, rp = s("n_juste"), s("n_rare_vrai"), s("n_rare_pred")
    rappel = juste / rv if rv > 0 else np.nan
    precision = juste / rp if rp > 0 else np.nan
    f1 = (2 * rappel * precision / (rappel + precision)
          if rappel and precision and (rappel + precision) > 0 else
          (0.0 if rp > 0 or rv > 0 else np.nan))
    return {
        "rappel": rappel,
        "precision": precision,
        "f1": f1,
        "taux_fausses_minorites": s("n_faux_maj") / rp if rp > 0 else np.nan,
        "taux_mauvaise_minorite": s("n_faux_min") / rp if rp > 0 else np.nan,
        "masse_predite": rp / s("n_eval") if s("n_eval") > 0 else np.nan,
        "masse_humaine": rv / s("n_eval") if s("n_eval") > 0 else np.nan,
    }


def bootstrap_agregats(c, idx_boot):
    """Intervalles a 95 pour cent des agregats, personnes reechantillonnees."""
    cles = ["rappel", "precision", "f1", "taux_fausses_minorites",
            "taux_mauvaise_minorite", "masse_predite"]
    tir = {k: np.empty(len(idx_boot)) for k in cles}
    for t, idx in enumerate(idx_boot):
        a = agreger(c, idx)
        for k in cles:
            tir[k][t] = a[k]
    out = {}
    for k in cles:
        v = tir[k][~np.isnan(tir[k])]
        out[k + "_ic_bas"] = float(np.percentile(v, 2.5)) if len(v) else np.nan
        out[k + "_ic_haut"] = float(np.percentile(v, 97.5)) if len(v) else np.nan
    return out, tir


# ---------------------------------------------------------------------------
# 4. Correlation par personne
# ---------------------------------------------------------------------------

def rangs(v):
    from scipy.stats import rankdata
    return rankdata(v)


def spearman(u, v, n_min=4):
    """Correlation de rang, NaN ecartes par paires.

    n_min vaut 4, comme dans a28_commun.spearman. Sur les profils demographiques le
    nombre de points est le nombre de niveaux de l'axe : deux ou trois niveaux ne donnent
    rien d'interpretable, et les axes concernes sont signales dans le rapport.
    """
    u, v = np.asarray(u, float), np.asarray(v, float)
    ok = ~np.isnan(u) & ~np.isnan(v)
    if ok.sum() < n_min:
        return np.nan
    ru, rv = rangs(u[ok]), rangs(v[ok])
    ru = ru - ru.mean()
    rv = rv - rv.mean()
    den = np.sqrt((ru ** 2).sum() * (rv ** 2).sum())
    return float((ru * rv).sum() / den) if den > 0 else np.nan


def pearson(u, v, n_min=4):
    u, v = np.asarray(u, float), np.asarray(v, float)
    ok = ~np.isnan(u) & ~np.isnan(v)
    if ok.sum() < n_min:
        return np.nan
    u, v = u[ok] - u[ok].mean(), v[ok] - v[ok].mean()
    den = np.sqrt((u ** 2).sum() * (v ** 2).sum())
    return float((u * v).sum() / den) if den > 0 else np.nan


def taux(c):
    """Taux de rares reelles et taux de rares predites par personne.

    Le taux et non le compte : les personnes n'ont pas toutes le meme nombre de cellules
    evaluables, et une correlation sur les comptes bruts serait en partie une correlation
    entre deux fois le meme denominateur.
    """
    n = np.where(c["n_eval"] > 0, c["n_eval"], np.nan)
    return c["n_rare_vrai"] / n, c["n_rare_pred"] / n


def correlation_personne(c, idx_boot, permutations=0, rng=None):
    """Correlation par personne, son intervalle bootstrap et son temoin de permutation.

    Le temoin permute, item par item, les predictions entre les personnes du perimetre.
    Il conserve exactement la masse minoritaire predite de chaque item et detruit
    l'appariement personne par personne : c'est la valeur qu'une methode obtiendrait si
    elle distribuait la rarete au hasard entre les gens tout en la mettant au bon taux sur
    chaque question.
    """
    u, v = taux(c)
    r_s, r_p = spearman(u, v), pearson(u, v)
    tir = np.empty(len(idx_boot))
    for t, idx in enumerate(idx_boot):
        tir[t] = spearman(u[idx], v[idx])
    tir = tir[~np.isnan(tir)]
    out = {"rho_spearman": r_s, "r_pearson": r_p,
           "ic_bas": float(np.percentile(tir, 2.5)) if len(tir) else np.nan,
           "ic_haut": float(np.percentile(tir, 97.5)) if len(tir) else np.nan}
    if permutations and rng is not None:
        rp_mat, ok = c["_rare_pred"], c["_ok"]
        den = np.where(c["n_eval"] > 0, c["n_eval"], np.nan)
        # Les lignes evaluables de chaque item, calculees une fois : la permutation ne
        # doit deplacer une prediction rare que vers une personne dont la vraie reponse
        # est observee, sinon elle detruirait la masse au lieu de la deplacer.
        lignes_item = [np.flatnonzero(ok[:, j]) for j in range(rp_mat.shape[1])]
        nul = np.empty(permutations)
        for t in range(permutations):
            perm = np.zeros_like(rp_mat)
            for j, rows in enumerate(lignes_item):
                if len(rows) == 0:
                    continue
                perm[rows, j] = rp_mat[rng.permutation(rows), j]
            nul[t] = spearman(u, perm.sum(axis=1) / den)
        nul = nul[~np.isnan(nul)]
        out["temoin_permutation"] = float(np.mean(nul)) if len(nul) else np.nan
        out["temoin_p975"] = float(np.percentile(nul, 97.5)) if len(nul) else np.nan
    return out, u, v, tir


def contraste_correlations(ca, cb, idx_boot):
    """Difference de correlations entre deux methodes, memes personnes tirees.

    Le p bilateral est lu sur la position de zero dans la distribution bootstrap, comme
    en a28. Il ne descend jamais sous 1 / nombre de tirages, ce qui evite d'ecrire p = 0
    apres une correction pour tests multiples.
    """
    ua, va = taux(ca)
    ub, vb = taux(cb)
    obs = spearman(ua, va) - spearman(ub, vb)
    tir = np.array([spearman(ua[i], va[i]) - spearman(ub[i], vb[i]) for i in idx_boot])
    tir = tir[~np.isnan(tir)]
    if len(tir) == 0:
        # Cas degenere : la methode ne predit jamais de modalite minoritaire, la
        # correlation n'est pas definie. Le test est declare non evaluable et recoit
        # p = 1, choix conservateur : il ne peut pas creer de fausse decouverte et il
        # n'allege pas la correction appliquee aux autres.
        return np.nan, np.nan, np.nan, 1.0
    p = 2.0 * min((tir <= 0).mean(), (tir >= 0).mean())
    return (float(obs), float(np.percentile(tir, 2.5)), float(np.percentile(tir, 97.5)),
            float(min(max(p, 1.0 / len(tir)), 1.0)))


def contraste_agregat(ca, cb, cle, idx_boot):
    """Difference d'un agregat entre deux methodes, memes personnes tirees."""
    obs = agreger(ca)[cle] - agreger(cb)[cle]
    tir = np.array([agreger(ca, i)[cle] - agreger(cb, i)[cle] for i in idx_boot])
    tir = tir[~np.isnan(tir)]
    if len(tir) == 0:
        # meme convention que contraste_correlations : test non evaluable, p = 1
        return np.nan, np.nan, np.nan, 1.0
    p = 2.0 * min((tir <= 0).mean(), (tir >= 0).mean())
    return (float(obs), float(np.percentile(tir, 2.5)), float(np.percentile(tir, 97.5)),
            float(min(max(p, 1.0 / len(tir)), 1.0)))


def p_contre_zero(tir):
    """p bilateral d'une statistique bootstrap contre zero."""
    tir = np.asarray(tir, float)
    tir = tir[~np.isnan(tir)]
    if len(tir) == 0:
        return 1.0
    p = 2.0 * min((tir <= 0).mean(), (tir >= 0).mean())
    return float(min(max(p, 1.0 / len(tir)), 1.0))


# ---------------------------------------------------------------------------
# 5. Items sensibles au mode
# ---------------------------------------------------------------------------

def classes_norc(items):
    """item -> classe NORC, memes listes et meme correspondance que a25 et a28."""
    return {it: classe_norc(it)[0] for it in items}


def colonnes_classe(items, classe):
    cl = classes_norc(items)
    return np.array([j for j, it in enumerate(items) if cl[it] == classe], dtype=int)


def restreindre(c, colonnes):
    """Recompte les six vecteurs sur un sous ensemble d'items."""
    out = {}
    for cle, mat in (("n_eval", c["_ok"]), ("n_rare_vrai", c["_rare_vrai"] & c["_ok"]),
                     ("n_rare_pred", c["_rare_pred"]), ("n_juste", c["_juste"])):
        out[cle] = mat[:, colonnes].sum(axis=1).astype(float)
    faux = c["_rare_pred"] & ~c["_juste"]
    out["n_faux_maj"] = (faux & ~c["_rare_vrai"])[:, colonnes].sum(axis=1).astype(float)
    out["n_faux_min"] = (faux & c["_rare_vrai"])[:, colonnes].sum(axis=1).astype(float)
    out["n_refus"] = np.zeros(len(out["n_eval"]))
    out["_rare_vrai"] = c["_rare_vrai"][:, colonnes]
    out["_rare_pred"] = c["_rare_pred"][:, colonnes]
    out["_juste"] = c["_juste"][:, colonnes]
    out["_ok"] = c["_ok"][:, colonnes]
    return out


# ---------------------------------------------------------------------------
# 6. Divers
# ---------------------------------------------------------------------------

def tirages_bootstrap(n, tirages, rng):
    return rng.integers(0, n, (tirages, n))


def fidelite_test_retest(y1, y2, lignes):
    """Part des items ou la personne redonne la meme reponse deux semaines plus tard.

    NaN si la personne n'a aucune cellule observee dans les deux vagues. C'est la mesure
    de consistance employee par a12, recalculee ici sur le meme perimetre pour eviter tout
    ecart de denominateur.
    """
    a, b = y1[lignes], y2[lignes]
    ok = observe(a) & observe(b)
    juste = ok & (a == b)
    n = ok.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, juste.sum(axis=1) / np.maximum(n, 1), np.nan)


def segments_et_niveaux(paquet):
    """Segmentation de a1 et a28, reprise a l'identique par import de a28_commun."""
    return C28.segments(paquet["x"], paquet["attributs"])
