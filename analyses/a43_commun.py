"""
a43_commun : briques partagees par le verrou 7, "le R2 demoyenne avec et sans etiquette,
et les criteres de Peng".

Question du 8 septembre 2026 : ce que Ahn, Mao et Lee (arXiv 2608.29455) mesurent sur
quatre jeux, porte sur les notres. Retirer la moyenne humaine de chaque item des deux
cotes et regarder ce qui correle encore ; puis retirer en plus la moyenne du segment, ce
qui reste etant la part "personne" au dela du groupe. Plus les quatre mesures de Peng et
al. telles que a36 les a lues.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a2_commun,
a25_commun, a28_commun, a39_commun, et par leur intermediaire a2_baselines_gss,
a5_evaluer, a5_agents_locaux_gss, a25_mesures. La foret de a28 et les imputations de a35
sont relues de leurs caches, elles ne sont pas redefinies.

Le preenregistrement est dans resultats/a43-preenregistrement.md, ecrit avant tout calcul.

Ce module porte six choses et rien d'autre.

  1. Le chargement, delegue a a39_commun.charger donc a a28_commun.charger_tout, plus la
     relecture du cache de a35 pour PMM et l'imputation multiple.
  2. La segmentation ideologie x genre x age, dans ses deux versions : la primaire a
     18 segments, avec l'age regroupe en trois, et la secondaire a 42 segments.
  3. Les moyennes leave-one-out, d'item et de segment, toujours estimees sur les
     1 052 personnes, y compris quand la mesure porte sur les 150.
  4. Le R2 demoyenne et son bootstrap sur les personnes, par sommes partielles : la
     correlation d'un tirage se recalcule a partir des six sommes par personne, ce qui
     evite de reparcourir un million de cellules a chaque tirage.
  5. Le r par personne a travers les items, contre les deux moyennes leave-one-out.
  6. La decomposition de variance personne x item, en trois parts pour une methode et en
     quatre parts pour les humains a deux vagues.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import pickle
import sys

# Limite de quatre coeurs, posee avant l'import de numpy sinon elle est sans effet.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
import a39_commun as C39

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260908
BOOTSTRAP = 2000
N_MIN_SEGMENT = 10      # repondants observes minimaux dans une cellule item x segment
N_MIN_ITEMS_PERSONNE = 10   # items valides minimaux pour qu'un r par personne existe

ecrire = C28.ecrire
holm = C28.holm
benjamini_hochberg = C28.benjamini_hochberg
ic = C39.ic
p_bilateral = C39.p_bilateral

# Les trois methodes de a35 relues du cache. Ce sont les deux appariements sur moyenne
# predite et l'imputation multiple, c'est a dire les methodes que le preenregistrement
# nomme "imputations statistiques par tirage".
METHODES_A35 = ["PMM k=5", "PMM k=10", "IM m=10 mode des m"]

ORDRE_METHODES = [
    "agents composite", "agents entretien (v3)", "agents enquete",
    "agents demographiques (v6)", "agents v7", "agents v8", "C2", "C3",
    "PMM k=5", "PMM k=10", "IM m=10 mode des m",
    "B0 mode", "B1 argmax", "B2 argmax", "B3 foret",
    "humains vague 2",
]

FAMILLE = dict(C39.FAMILLE_CONDITION)
FAMILLE.update({"PMM k=5": "imputation par tirage", "PMM k=10": "imputation par tirage",
                "IM m=10 mode des m": "imputation multiple"})

# Valeurs de Peng et al., lues par a36 sections 6.2 et 2.3, jamais recalculees ici.
PENG = {
    "empty_persona": {"std_ratio": 0.446, "exactitude": 0.734, "correlation": 0.080},
    "demographics_only": {"std_ratio": 0.575, "exactitude": 0.746, "correlation": 0.145},
    "full_persona_without_reasoning": {"std_ratio": 0.634, "exactitude": 0.748,
                                       "correlation": 0.197},
    "full_persona_fine_tuned_temperature_7": {"std_ratio": 1.061, "exactitude": 0.704,
                                              "correlation": 0.140},
    "random_benchmark": {"std_ratio": 1.139, "exactitude": 0.629, "correlation": 0.0006},
}

# Chiffres de Ahn, Mao et Lee, recopies de la lecture 01. Aucun calcul de notre part.
AHN = {"r2_demoyenne": 0.0305, "plafond": 0.536, "part_du_plafond": 0.057,
       "r_llm": 0.34, "r_moyenne_item": 0.45,
       "part_personne": 0.049, "part_item": 0.087, "part_interaction": 0.440,
       "part_transitoire": 0.424, "rapport_interaction_personne": 8.9}


# ---------------------------------------------------------------------------
# 1. Chargement
# ---------------------------------------------------------------------------

def charger(cache, cache_foret, cache_a35):
    """Paquet de a28 et a39, plus les trois methodes d'imputation de a35.

    Le cache de a35 est relu tel quel. S'il est absent, les trois methodes sont
    simplement absentes du tableau et le rapport le dit : elles ne sont pas recalculees,
    ce qui garantit qu'aucun tirage ne differe de celui de a35.
    """
    paquet = C39.charger(cache, cache_foret)
    presentes = []
    if cache_a35 and os.path.exists(cache_a35):
        brut = pickle.load(open(cache_a35, "rb"))
        for nom in METHODES_A35:
            if nom in brut:
                paquet["M"][nom] = brut[nom]
                presentes.append(nom)
    paquet["a35_presentes"] = presentes
    return paquet


def methodes_du_perimetre(paquet, nom_perimetre):
    toutes = [c for c in ORDRE_METHODES if c in paquet["M"]]
    if nom_perimetre == "1052":
        return [c for c in toutes if c not in ("C2", "C3")]
    return toutes


perimetres = C39.perimetres


# ---------------------------------------------------------------------------
# 2. Segmentation ideologie x genre x age
# ---------------------------------------------------------------------------

_AGE_REGROUPE = {
    "18 - 24": "jeune", "25 - 34": "jeune",
    "35 - 44": "median", "45 - 54": "median",
    "55 - 64": "age", "65 - 74": "age", "75 or more": "age",
}


def segments_ideologie_genre_age(paquet, age_regroupe=True):
    """Vecteur d'entiers de segment et liste des libelles.

    Le bloc d'ideologie est celui de a28_commun._bloc_ideologie, importe et non recopie.
    Une personne dont l'un des trois attributs est absent recoit -1 et sort des calculs
    qui retirent la moyenne de segment.
    """
    col = {a: i for i, a in enumerate(paquet["attributs"])}
    x = paquet["x"]
    ideo = [C28._bloc_ideologie(C28.norm(v)) for v in x[:, col["political_ideology"]]]
    genre = [C28.norm(v) for v in x[:, col["gender"]]]
    age = [C28.norm(v) for v in x[:, col["age"]]]
    if age_regroupe:
        age = [_AGE_REGROUPE.get(a, "") for a in age]
    libelles = []
    for i, g, a in zip(ideo, genre, age):
        if not g or not a or g == "non renseigne" or a == "non renseigne":
            libelles.append("")
        else:
            libelles.append(f"{i}|{g}|{a}")
    niveaux = sorted({v for v in libelles if v})
    index = {v: k for k, v in enumerate(niveaux)}
    return np.array([index.get(v, -1) for v in libelles], dtype=np.int32), niveaux


# ---------------------------------------------------------------------------
# 3. Matrices de valeurs ordinales et moyennes leave-one-out
# ---------------------------------------------------------------------------

def preparer_valeurs(paquet):
    """Colonnes ordinales, table de rang, et matrice humaine de la vague 1 en [0, 1]."""
    items = paquet["items"]
    ords = C39.items_ordinaux(items, paquet["options"])
    colonnes = [items.index(it) for it in ords]
    rangs = C39.table_de_rang(items, paquet["options"])
    H = C39.matrice_scores(paquet["y1"], colonnes, items, rangs)
    return ords, colonnes, rangs, H


def scores_methode(paquet, nom, colonnes, rangs):
    return C39.matrice_scores(paquet["M"][nom], colonnes, paquet["items"], rangs)


def moyennes_loo(H, seg=None, n_seg=0, n_min=N_MIN_SEGMENT):
    """Moyenne leave-one-out, d'item si seg est None, d'item x segment sinon.

    H : matrice (personnes x items) de valeurs dans [0, 1], NaN si la cellule est vide.
    Retourne une matrice de meme forme, NaN la ou la moyenne n'est pas definie : segment
    inconnu, ou moins de n_min repondants observes dans la cellule apres retrait de la
    personne.

    La convention est celle du preenregistrement : la personne est retiree, qu'elle ait
    repondu ou non. Si elle n'a pas repondu elle ne contribuait deja pas, et la moyenne
    est celle de tous les repondants.
    """
    ok = ~np.isnan(H)
    V = np.where(ok, np.nan_to_num(H), 0.0)
    if seg is None:
        S = V.sum(axis=0)[None, :]
        N = ok.sum(axis=0)[None, :].astype(float)
        S = np.broadcast_to(S, H.shape)
        N = np.broadcast_to(N, H.shape)
        Sl = S - V
        Nl = N - ok
    else:
        n, m = H.shape
        Sl = np.full((n, m), np.nan)
        Nl = np.full((n, m), np.nan)
        for g in range(n_seg):
            lignes = np.flatnonzero(seg == g)
            if len(lignes) == 0:
                continue
            s = V[lignes].sum(axis=0)
            c = ok[lignes].sum(axis=0).astype(float)
            Sl[lignes] = s[None, :] - V[lignes]
            Nl[lignes] = c[None, :] - ok[lignes]
    with np.errstate(invalid="ignore", divide="ignore"):
        M = np.where(Nl >= n_min, Sl / np.maximum(Nl, 1.0), np.nan)
    return M


# ---------------------------------------------------------------------------
# 4. R2 demoyenne, par sommes partielles
# ---------------------------------------------------------------------------

def sommes_par_personne(x, y, valides):
    """Six sommes par personne, de quoi recalculer une correlation de Pearson poolee.

    x, y : matrices (personnes x items) ; valides : masque booleen des cellules retenues.
    """
    xv = np.where(valides, np.nan_to_num(x), 0.0)
    yv = np.where(valides, np.nan_to_num(y), 0.0)
    return np.stack([
        valides.sum(axis=1).astype(float),
        xv.sum(axis=1), yv.sum(axis=1),
        (xv * xv).sum(axis=1), (yv * yv).sum(axis=1), (xv * yv).sum(axis=1),
    ], axis=1)


def _r_de_sommes(S):
    """Correlation de Pearson a partir du vecteur des six sommes cumulees."""
    n, sx, sy, sxx, syy, sxy = S
    if n < 3:
        return np.nan
    cov = sxy - sx * sy / n
    vx = sxx - sx * sx / n
    vy = syy - sy * sy / n
    if vx <= 0 or vy <= 0:
        return np.nan
    return float(cov / np.sqrt(vx * vy))


def r_poole(sommes, idx=None):
    S = sommes.sum(axis=0) if idx is None else sommes[idx].sum(axis=0)
    return _r_de_sommes(S)


def bootstrap_r(sommes, idx_boot):
    """Distribution bootstrap de la correlation poolee, personnes reechantillonnees."""
    out = np.empty(len(idx_boot))
    for t, idx in enumerate(idx_boot):
        out[t] = _r_de_sommes(sommes[idx].sum(axis=0))
    return out


def preparer_r2(H, P, MOY, lignes):
    """Sommes par personne pour le R2 demoyenne d'une methode sur un perimetre.

    H : humains vague 1 ; P : methode ; MOY : moyenne retiree des deux cotes.
    Une cellule est valide si les trois valeurs existent.
    """
    h, p, m = H[lignes], P[lignes], MOY[lignes]
    valides = ~np.isnan(h) & ~np.isnan(p) & ~np.isnan(m)
    x = h - m
    y = p - m
    return sommes_par_personne(x, y, valides), int(valides.sum())


# ---------------------------------------------------------------------------
# 5. r par personne, a travers les items
# ---------------------------------------------------------------------------

def r_par_personne(H, P, lignes, n_min=N_MIN_ITEMS_PERSONNE):
    """Correlation a travers les items, une valeur par personne du perimetre.

    Valeurs brutes, non demoyennees : c'est la mesure de Ahn, celle qui donne 0,34 pour
    le modele de langage contre 0,45 pour la moyenne d'item leave-one-out.
    """
    h, p = H[lignes], P[lignes]
    ok = ~np.isnan(h) & ~np.isnan(p)
    n = ok.sum(axis=1)
    hv = np.where(ok, np.nan_to_num(h), 0.0)
    pv = np.where(ok, np.nan_to_num(p), 0.0)
    nn = np.maximum(n, 1).astype(float)
    mh = hv.sum(axis=1) / nn
    mp = pv.sum(axis=1) / nn
    cov = (hv * pv).sum(axis=1) - nn * mh * mp
    vh = (hv * hv).sum(axis=1) - nn * mh * mh
    vp = (pv * pv).sum(axis=1) - nn * mp * mp
    with np.errstate(invalid="ignore", divide="ignore"):
        r = np.where((n >= n_min) & (vh > 0) & (vp > 0),
                     cov / np.sqrt(np.maximum(vh * vp, 1e-300)), np.nan)
    return r


def z_moyen(r):
    """Moyenne des r transformes en z de Fisher, retransformee en correlation."""
    r = np.asarray(r, float)
    r = r[~np.isnan(r)]
    if len(r) == 0:
        return np.nan
    z = np.arctanh(np.clip(r, -0.999999, 0.999999))
    return float(np.tanh(z.mean()))


def bootstrap_z(r, idx_boot):
    r = np.asarray(r, float)
    z = np.arctanh(np.clip(r, -0.999999, 0.999999))
    ok = ~np.isnan(z)
    out = np.empty(len(idx_boot))
    for t, idx in enumerate(idx_boot):
        zz = z[idx][ok[idx]]
        out[t] = np.tanh(zz.mean()) if len(zz) else np.nan
    return out


def bootstrap_diff_z(ra, rb, idx_boot):
    """Difference appariee de deux moyennes de Fisher, memes personnes tirees."""
    za = np.arctanh(np.clip(np.asarray(ra, float), -0.999999, 0.999999))
    zb = np.arctanh(np.clip(np.asarray(rb, float), -0.999999, 0.999999))
    ok = ~np.isnan(za) & ~np.isnan(zb)
    out = np.empty(len(idx_boot))
    for t, idx in enumerate(idx_boot):
        m = ok[idx]
        out[t] = (np.tanh(za[idx][m].mean()) - np.tanh(zb[idx][m].mean())
                  if m.any() else np.nan)
    return out


def d_de_cohen_apparie(ra, rb):
    """dz apparie sur les z de Fisher, la statistique que Ahn publie a -0,55."""
    za = np.arctanh(np.clip(np.asarray(ra, float), -0.999999, 0.999999))
    zb = np.arctanh(np.clip(np.asarray(rb, float), -0.999999, 0.999999))
    ok = ~np.isnan(za) & ~np.isnan(zb)
    d = za[ok] - zb[ok]
    if len(d) < 3 or d.std(ddof=1) == 0:
        return np.nan, int(len(d))
    return float(d.mean() / d.std(ddof=1)), int(len(d))


# ---------------------------------------------------------------------------
# 6. Decomposition de variance personne x item
# ---------------------------------------------------------------------------

def _ajustement_additif(Z, iterations=60):
    """Moindres carres du modele additif mu + a_i + b_j sur une matrice a trous.

    Moindres carres alternes, ce qui est la solution exacte du probleme additif quand il
    converge. Retourne (mu, a, b, residus, nombre de cellules observees).
    """
    ok = ~np.isnan(Z)
    n, m = Z.shape
    a = np.zeros(n)
    b = np.zeros(m)
    V = np.where(ok, np.nan_to_num(Z), 0.0)
    ni = ok.sum(axis=1).astype(float)
    nj = ok.sum(axis=0).astype(float)
    mu = V.sum() / max(ok.sum(), 1)
    for _ in range(iterations):
        r = V - np.where(ok, mu + b[None, :], 0.0)
        a = np.where(ni > 0, np.where(ok, r, 0.0).sum(axis=1) / np.maximum(ni, 1), 0.0)
        r = V - np.where(ok, mu + a[:, None], 0.0)
        b = np.where(nj > 0, np.where(ok, r, 0.0).sum(axis=0) / np.maximum(nj, 1), 0.0)
        # recentrage, la parametrisation additive n'est definie qu'a une constante pres
        da = a[ni > 0].mean() if (ni > 0).any() else 0.0
        db = b[nj > 0].mean() if (nj > 0).any() else 0.0
        a = a - da
        b = b - db
        mu = mu + da + db
    res = np.where(ok, Z - (mu + a[:, None] + b[None, :]), np.nan)
    return mu, a, b, res, int(ok.sum())


def decomposition(Z, Z2=None):
    """Parts de variance personne, item, interaction, erreur.

    Z  : matrice (personnes x items) de valeurs, NaN si vide. Une seule occasion.
    Z2 : seconde occasion des memes cellules, ou None.

    Sans seconde occasion, trois parts : personne, item, residu, ce dernier confondant
    l'interaction stable et l'erreur. Le rapport residu sur personne est alors une BORNE
    SUPERIEURE du rapport de Ahn.

    Avec seconde occasion, quatre parts. L'erreur transitoire est estimee sur la demi
    variance des differences entre vagues, la moyenne des deux vagues sert de support a
    l'ajustement additif, et l'interaction stable est le residu de cette moyenne diminue
    de la moitie de l'erreur transitoire. Les effets principaux sont corriges du bruit
    d'echantillonnage qu'un effet estime sur un nombre fini de cellules porte
    mecaniquement.
    """
    if Z2 is None:
        cible = Z
        v_e = 0.0
        facteur = 1.0
    else:
        ok2 = ~np.isnan(Z) & ~np.isnan(Z2)
        d = np.where(ok2, Z - Z2, np.nan)
        v_e = float(np.nanmean(d ** 2) / 2.0) if ok2.any() else np.nan
        cible = np.where(ok2, (np.nan_to_num(Z) + np.nan_to_num(Z2)) / 2.0, np.nan)
        facteur = 0.5   # la moyenne de deux occasions porte v_e / 2
    mu, a, b, res, n_obs = _ajustement_additif(cible)
    ok = ~np.isnan(cible)
    n = int((ok.sum(axis=1) > 0).sum())
    m = int((ok.sum(axis=0) > 0).sum())
    ddl = max(n_obs - n - m + 1, 1)
    v_res = float(np.nansum(res ** 2) / ddl)          # interaction + facteur * v_e
    v_pi = max(v_res - facteur * (v_e if Z2 is not None else 0.0), 0.0)
    ni = ok.sum(axis=1).astype(float)
    nj = ok.sum(axis=0).astype(float)
    ai, bj = a[ni > 0], b[nj > 0]
    biais_a = float(np.mean(v_res / np.maximum(ni[ni > 0], 1)))
    biais_b = float(np.mean(v_res / np.maximum(nj[nj > 0], 1)))
    v_p = max(float(ai.var(ddof=1)) - biais_a, 0.0) if len(ai) > 2 else np.nan
    v_i = max(float(bj.var(ddof=1)) - biais_b, 0.0) if len(bj) > 2 else np.nan
    if Z2 is None:
        total = v_p + v_i + v_res
        return {"var_personne": v_p, "var_item": v_i, "var_residu": v_res,
                "var_interaction": np.nan, "var_transitoire": np.nan,
                "part_personne": v_p / total, "part_item": v_i / total,
                "part_residu": v_res / total, "part_interaction": np.nan,
                "part_transitoire": np.nan,
                "rapport_interaction_personne": v_res / v_p if v_p > 0 else np.nan,
                "borne_superieure": True, "n_cellules": n_obs}
    total = v_p + v_i + v_pi + v_e
    return {"var_personne": v_p, "var_item": v_i, "var_residu": v_res,
            "var_interaction": v_pi, "var_transitoire": v_e,
            "part_personne": v_p / total, "part_item": v_i / total,
            "part_residu": np.nan,
            "part_interaction": v_pi / total, "part_transitoire": v_e / total,
            "rapport_interaction_personne": v_pi / v_p if v_p > 0 else np.nan,
            "borne_superieure": False, "n_cellules": n_obs}


# ---------------------------------------------------------------------------
# 7. Divers
# ---------------------------------------------------------------------------

def tirages_bootstrap(n, tirages=BOOTSTRAP, graine=GRAINE):
    return np.random.default_rng(graine).integers(0, n, (tirages, n))
