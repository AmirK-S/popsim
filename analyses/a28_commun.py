"""
a28_commun : briques partagees par les trois tests decisifs de la seance du 8 septembre 2026.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a2_commun,
a2_baselines_gss, a5_evaluer, a5_agents_locaux_gss, a25_commun, a25_mesures, a8_commun.

Ce module porte cinq choses et rien d'autre.

  1. Le chargement unique des matrices de prediction, delegue a a25_mesures.matrices :
     memes 1 052 personnes, memes 149 items, memes plis et memes graines que a2, a23 et
     a25. C2 et C3 ne couvrent que les 150 personnes du run.
  2. Une methode nouvelle et une seule, la foret aleatoire sur demographies, notee
     "B3 foret". C'est l'adversaire nomme par Ku 2026 : un predicteur statistique non
     lineaire, sans langage et sans alignement. Meme protocole que B1, memes plis, memes
     colonnes, meme encodage indicatrice ajuste sur l'entrainement seul.
  3. La segmentation de a1, reprise a l'identique : six axes, dont le profil croise
     genre x race x bloc d'ideologie.
  4. Les estimateurs de dispersion de a1, recopies dans leur version item par item :
     entropie de Shannon corrigee par Miller Madow, indice de Gini Simpson sans biais, et
     leur decomposition exacte en une part inter segments et une part intra segment.
  5. Les corrections pour tests multiples, Holm et Benjamini Hochberg, et les outils de
     bootstrap sur les items.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_commun import est_manquant, encodeur_demographies
from a2_baselines_gss import GRAINE, charger, grille
from a25_commun import ORDINAUX, classe_norc, options_par_item, sans_score
from a25_mesures import matrices as matrices_a25

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
LN2 = np.log(2.0)

# Ordre d'affichage stable dans tous les tableaux de a28.
ORDRE_METHODES = [
    "agents composite", "agents entretien (v3)", "agents enquete",
    "agents demographiques (v6)", "agents v7", "agents v8", "C2", "C3",
    "B0 mode", "B0 tirage", "B1 argmax", "B2 argmax", "B3 foret",
    "humains vague 2",
]

# Les huit conditions qui emploient un modele de langage, et les cinq predicteurs qui
# n'en emploient pas. La ligne "humains vague 2" n'est ni l'un ni l'autre, c'est le
# plancher de bruit.
LLM = ["agents composite", "agents entretien (v3)", "agents enquete",
       "agents demographiques (v6)", "agents v7", "agents v8", "C2", "C3"]
STAT = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax", "B3 foret"]


def norm(v):
    return str(v).lower().strip()


# ---------------------------------------------------------------------------
# 1 et 2. Chargement, plus la foret aleatoire
# ---------------------------------------------------------------------------

class _Args:
    """Adaptateur minimal pour appeler a25_mesures.matrices sans modifier ce script."""

    def __init__(self, cache):
        self.cache = cache
        self.bootstrap = 0
        self.graine = GRAINE


def foret_demographies(items, y, x, plis, graine=GRAINE, arbres=300, n_jobs=4):
    """Foret aleatoire sur les seules demographies, une foret par item.

    C'est l'adversaire de Ku 2026 : un predicteur statistique capable d'interactions, la
    ou B1 est lineaire dans les indicatrices. Meme decoupage sur les personnes que B1 et
    B2, meme encodage indicatrice ajuste sur le pli d'entrainement seul, meme convention
    de sortie, la classe la plus probable. Aucun item de contexte n'est employe, comme
    pour B1 : la comparaison porte sur l'information demographique et sur elle seule.
    """
    from sklearn.ensemble import RandomForestClassifier

    n, m = y.shape
    pred = np.empty((n, m), dtype=object)
    for i_pli, (tr, te) in enumerate(plis):
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        for j in range(m):
            obs = np.array([not est_manquant(v) for v in y[tr, j]])
            if obs.sum() < 5:
                continue
            cible = np.asarray(y[tr, j], dtype=object)[obs]
            classes = list(dict.fromkeys(cible))
            if len(classes) == 1:
                pred[np.ix_(te, [j])] = np.array([classes[0]] * len(te),
                                                 dtype=object)[:, None]
                continue
            rang = {c: i for i, c in enumerate(classes)}
            modele = RandomForestClassifier(
                n_estimators=arbres, min_samples_leaf=5, n_jobs=n_jobs,
                random_state=graine + i_pli)
            modele.fit(xt[obs], np.array([rang[v] for v in cible]))
            idx = modele.predict(xe)
            pred[np.ix_(te, [j])] = np.array([classes[i] for i in idx],
                                             dtype=object)[:, None]
        print(f"  foret, pli {i_pli + 1}/{len(plis)} termine", flush=True)
    return pred


def charger_tout(cache, cache_foret=None):
    """Retourne le paquet complet employe par les trois tests.

    Cle "M" : nom de methode -> matrice objet (1 052 x 149). C2 et C3 sont remplies de
    None hors des 150 personnes du run.
    """
    args = _Args(cache)
    ids, items, y1, M, lignes150 = matrices_a25(args)
    _, _, _, _, x, attributs = charger()

    if cache_foret and os.path.exists(cache_foret):
        M["B3 foret"] = np.load(cache_foret, allow_pickle=True)
    else:
        plis, _ = grille(len(ids), len(items), GRAINE)
        M["B3 foret"] = foret_demographies(items, y1, x, plis)
        if cache_foret:
            np.save(cache_foret, M["B3 foret"], allow_pickle=True)

    options = options_par_item(RACINE)
    return {
        "ids": ids, "items": items, "y1": y1, "M": M, "lignes150": lignes150,
        "x": x, "attributs": attributs, "options": options,
    }


# ---------------------------------------------------------------------------
# 3. Segmentation, reprise de a1_double_distorsion
# ---------------------------------------------------------------------------

AXES = ["gender", "race", "political_ideology", "age", "education", "profil croise"]


def _bloc_ideologie(v):
    """Les sept niveaux du GSS ramenes a trois. Regle mecanique sur le libelle, comme a1."""
    if "liberal" in v:
        return "gauche"
    if "conservative" in v:
        return "droite"
    return "centre"


def segments(x, attributs):
    """axe -> vecteur d'entiers de segment (-1 si manquant), et la liste des niveaux."""
    col = {a: i for i, a in enumerate(attributs)}
    brut = {a: [norm(v) for v in x[:, col[a]]] for a in
            ["gender", "race", "political_ideology", "age", "education"]}
    valeurs = dict(brut)
    valeurs["profil croise"] = [
        f"{g}|{r}|{_bloc_ideologie(i)}"
        for g, r, i in zip(brut["gender"], brut["race"], brut["political_ideology"])]
    seg, niveaux = {}, {}
    for axe in AXES:
        mods = sorted({v for v in valeurs[axe] if v.strip() and v != "non renseigne"})
        idx = {m: k for k, m in enumerate(mods)}
        seg[axe] = np.array([idx.get(v, -1) for v in valeurs[axe]], dtype=np.int32)
        niveaux[axe] = mods
    return seg, niveaux


# ---------------------------------------------------------------------------
# 4. Dispersion, item par item : Gini Simpson et entropie, avec correction de biais
# ---------------------------------------------------------------------------
#
# Les deux estimateurs sont ceux de a1_double_distorsion.decomposer, recopies ici dans
# leur version "un item a la fois" pour que le ratio soit disponible item par item et non
# seulement en somme. Le motif de la correction de biais est le meme qu'en a1 : les
# agents emploient moins de modalites que les humains, et l'estimateur naif du terme
# inter est positivement biaise d'un montant qui croit avec le nombre de cases occupees.

def _simpson_unb(counts, axis):
    """1 - somme p^2, estimateur sans biais : somme n_k (n_k - 1) / (N (N - 1))."""
    total = counts.sum(axis=axis)
    den = np.where(total > 1.0, total * (total - 1.0), np.nan)
    return 1.0 - (counts * (counts - 1.0)).sum(axis=axis) / den


def _h_mm(counts):
    """Entropie de Shannon en bits, estimateur de Miller Madow."""
    N = counts.sum()
    if N <= 0:
        return np.nan
    p = counts / N
    h = -np.sum(np.where(p > 0, p * np.log2(np.maximum(p, 1e-300)), 0.0))
    m = int((counts > 0).sum())
    return h + (m - 1.0) / (2.0 * N * LN2)


def dispersion_item(codes, seg, k, n_min=30):
    """Dispersion d'un item pour une segmentation donnee.

    codes : vecteur d'entiers de reponse, -1 pour une cellule vide.
    seg   : vecteur d'entiers de segment, -1 pour un segment inconnu.
    k     : nombre de modalites declarees de l'item.

    Renvoie un dictionnaire :
      gs_total, gs_intra, gs_inter : indice de Gini Simpson total, part intra segment
        (moyenne ponderee des indices dans les segments) et part inter, sans biais ;
      h_total, h_intra, h_inter : entropie totale, entropie conditionnelle H(R|S) et
        information mutuelle I(R;S), corrigees par Miller Madow ;
      n : nombre de cellules exploitables.
    Les valeurs sont NaN si moins de n_min cellules sont exploitables.
    """
    ok = (codes >= 0) & (seg >= 0)
    n = int(ok.sum())
    vide = {"gs_total": np.nan, "gs_intra": np.nan, "gs_inter": np.nan,
            "h_total": np.nan, "h_intra": np.nan, "h_inter": np.nan, "n": n}
    if n < n_min:
        return vide
    r, s = codes[ok], seg[ok]
    g = int(s.max()) + 1
    c = np.zeros((g, k), dtype=np.float64)
    np.add.at(c, (s, r), 1.0)

    n_k = c.sum(axis=0)
    n_g = c.sum(axis=1)
    gs_total = _simpson_unb(n_k[None, :], 1)[0]
    ok_g = n_g >= 2
    gs_g = np.full(g, np.nan)
    if ok_g.any():
        gs_g[ok_g] = _simpson_unb(c[ok_g], 1)
    poids = np.where(ok_g, n_g, 0.0)
    gs_intra = (np.where(ok_g, poids * np.nan_to_num(gs_g), 0.0).sum() / poids.sum()
                if poids.sum() > 0 else np.nan)

    h_r = _h_mm(n_k)
    h_s = _h_mm(n_g)
    h_rs = _h_mm(c.ravel())
    h_intra = h_rs - h_s
    return {"gs_total": float(gs_total), "gs_intra": float(gs_intra),
            "gs_inter": float(gs_total - gs_intra),
            "h_total": float(h_r), "h_intra": float(h_intra),
            "h_inter": float(h_r - h_intra), "n": n}


def coder(matrice, lignes, items, options):
    """Matrice de reponses en clair -> matrice d'entiers, -1 pour une cellule vide.

    Le codage suit l'ordre des modalites de question_master/gss/main.csv, le meme que
    celui de a25 et de a1. Une reponse hors nomenclature est traitee comme vide.
    """
    n, m = len(lignes), len(items)
    codes = np.full((n, m), -1, dtype=np.int32)
    for j, it in enumerate(items):
        index = {o: k for k, o in enumerate(options[it])}
        col = matrice[lignes, j]
        for i, v in enumerate(col):
            if v is None or est_manquant(v):
                continue
            k = index.get(norm(v))
            if k is not None:
                codes[i, j] = k
    return codes


# ---------------------------------------------------------------------------
# 5. Tests multiples et bootstrap
# ---------------------------------------------------------------------------

def holm(p):
    """p ajustes par la procedure de Holm, controle du taux d'erreur par famille (FWER).

    Valide sans hypothese sur la dependance entre tests, ce qui est necessaire ici :
    les contrastes des douze methodes portent sur les memes items et sont fortement
    correles entre eux.
    """
    p = np.asarray(p, dtype=float)
    ordre = np.argsort(p)
    m = len(p)
    ajuste = np.empty(m)
    courant = 0.0
    for rang, i in enumerate(ordre):
        val = (m - rang) * p[i]
        courant = max(courant, val)
        ajuste[i] = min(courant, 1.0)
    return ajuste


def benjamini_hochberg(p):
    """p ajustes par Benjamini Hochberg, controle du taux de fausses decouvertes (FDR).

    Plus permissif que Holm. Valide sous independance ou sous dependance positive au sens
    PRDS, hypothese plausible mais non verifiee ici : elle est signalee dans le rapport.
    """
    p = np.asarray(p, dtype=float)
    m = len(p)
    ordre = np.argsort(p)
    ajuste = np.empty(m)
    courant = 1.0
    for rang in range(m - 1, -1, -1):
        i = ordre[rang]
        courant = min(courant, m * p[i] / (rang + 1))
        ajuste[i] = min(courant, 1.0)
    return ajuste


def bootstrap_items(a, b, tirages, rng):
    """Difference de moyennes et intervalle, items reechantillonnes dans chaque groupe.

    Identique a a25_contrastes.bootstrap_items, recopie pour que a28 ne depende pas de
    l'ordre d'appel de ce script.
    """
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan, np.nan
    ta = a[rng.integers(0, len(a), (tirages, len(a)))].mean(axis=1)
    tb = b[rng.integers(0, len(b), (tirages, len(b)))].mean(axis=1)
    d = ta - tb
    return (float(a.mean() - b.mean()), float(np.percentile(d, 2.5)),
            float(np.percentile(d, 97.5)))


def permutation(a, b, tirages, rng):
    """p bilateral du test de permutation des etiquettes, sur la difference de moyennes."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan
    obs = a.mean() - b.mean()
    pool = np.concatenate([a, b])
    n = len(a)
    idx = np.argsort(rng.random((tirages, len(pool))), axis=1)
    perm = pool[idx]
    stat = perm[:, :n].mean(axis=1) - perm[:, n:].mean(axis=1)
    # Estimateur de Phipson et Smyth : (b + 1) / (m + 1), jamais nul, ce qui evite
    # d'ecrire "p = 0" apres une correction pour tests multiples.
    b_ge = int((np.abs(stat) >= abs(obs) - 1e-12).sum())
    return float(obs), (b_ge + 1.0) / (tirages + 1.0)


def spearman(u, v):
    """Correlation de rang de Spearman, NaN ecartes par paires."""
    u, v = np.asarray(u, float), np.asarray(v, float)
    ok = ~np.isnan(u) & ~np.isnan(v)
    if ok.sum() < 4:
        return np.nan, 0
    from scipy.stats import rankdata
    ru, rv = rankdata(u[ok]), rankdata(v[ok])
    ru = ru - ru.mean()
    rv = rv - rv.mean()
    den = np.sqrt((ru ** 2).sum() * (rv ** 2).sum())
    return (float((ru * rv).sum() / den) if den > 0 else np.nan), int(ok.sum())


def bootstrap_correlation(u, v, tirages, rng):
    """Correlation de Spearman et son intervalle, items reechantillonnes."""
    u, v = np.asarray(u, float), np.asarray(v, float)
    ok = ~np.isnan(u) & ~np.isnan(v)
    u, v = u[ok], v[ok]
    if len(u) < 6:
        return np.nan, np.nan, np.nan, len(u)
    r, _ = spearman(u, v)
    tir = np.empty(tirages)
    for t in range(tirages):
        i = rng.integers(0, len(u), len(u))
        tir[t], _ = spearman(u[i], v[i])
    tir = tir[~np.isnan(tir)]
    return (r, float(np.percentile(tir, 2.5)), float(np.percentile(tir, 97.5)), len(u))


def classes_items(items):
    """item -> classe NORC, telle que a25 la calcule."""
    return {it: classe_norc(it)[0] for it in items}


def type_item(it, options):
    """Type d'item pour la stratification : nominal, ordinal binaire, ordinal long.

    Le decoupage demande par le cahier des charges. Un item est traite comme ordinal
    exactement comme en a25 : il figure dans ORDINAUX et ne porte aucune modalite du type
    "Inapplicable". Les items binaires sont isoles parce que la distance de Wasserstein
    et la distance de variation totale y coincident, ce qui les rend comparables quel que
    soit le traitement.
    """
    opts = options[it]
    ordinal = it in ORDINAUX and not any(sans_score(o) for o in opts)
    if len(opts) == 2:
        return "binaire"
    if not ordinal:
        return "nominal"
    return "ordinal 3 et plus"


def ecrire(df, nom):
    os.makedirs(SORTIE, exist_ok=True)
    chemin = os.path.join(SORTIE, nom)
    df.to_csv(chemin, index=False, float_format="%.6f")
    print(f"ecrit : {chemin}")
    return chemin
