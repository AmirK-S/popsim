"""
a39_commun : briques partagees par la replication de la mesure de queue de Peng et al.

Question du 8 septembre 2026 : leur depot public calcule, sans jamais le publier dans
l'article, une exactitude par tranche de la valeur humaine. On trie les participants par
leur vraie valeur sur chaque resultat, on prend les 5 pour cent du bas, les 5 pour cent du
haut et les 90 pour cent du milieu, et on calcule l'exactitude individuelle sur chaque
tranche. Leurs valeurs, lues dans `average_metrics_by_specification.csv` et rapportees
telles quelles par a36 section 6.3 :

    specification                     mid_90    bottom_5   top_5
    full_persona_without_reasoning    0,7643    0,5416     0,6623
    demographics_only                 0,7644    0,5165     0,6475
    empty_persona                     0,7530    0,4644     0,6504
    random_benchmark                  0,6401    0,5325     0,5221

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a2_commun,
a25_commun, a28_commun, et par leur intermediaire a2_baselines_gss, a5_evaluer,
a5_agents_locaux_gss, a25_mesures, a29_commun pour les corrections. La foret aleatoire
`B3 foret` est relue du cache de a28, elle n'est pas redefinie.

Ce module porte cinq choses et rien d'autre.

  1. Le chargement, delegue a a28_commun.charger_tout : memes 1 052 personnes, memes
     149 items, memes plis, memes graines, memes 150 personnes du run local pour C2 et C3.
  2. **La definition des tranches, version rarete**, seule transposition possible de leur
     tri sur une reponse categorielle. Pour chaque item, la distribution des vraies
     reponses de la vague 1 est calculee sur les repondants observes du perimetre. Une
     cellule est
       - **bas** si sa vraie modalite est donnee par moins de 5 pour cent des repondants ;
       - **haut** si sa vraie modalite est la modalite majoritaire ET que cette modalite
         depasse 95 pour cent des repondants ;
       - **milieu** sinon.
     La tranche est definie par la VERITE HUMAINE seule : elle est donc la meme cellule
     par cellule pour les quatorze conditions, ce qui rend tous les contrastes apparies.
  3. **La definition des tranches, version ordinale**, qui est la leur mot pour mot,
     restreinte aux 71 items ordinaux de a25. Les modalites recoivent leur rang normalise
     dans [0, 1] selon l'ordre de `question_master/gss/main.csv`, les repondants observes
     sont tries par cette valeur, les 5 pour cent du bas et les 5 pour cent du haut sont
     pris par rang, le reste est le milieu. Les egalites, massives sur une echelle a trois
     modalites, sont departagees par une permutation aleatoire de graine fixe : c'est le
     seul point ou notre definition ajoute une convention a la leur, et la section
     protocole du rapport le dit.
  4. **Les deux exactitudes.** Sur la version rarete, l'exactitude est la concordance
     exacte, seule mesure definie sur une reponse nominale. Sur la version ordinale, c'est
     leur mesure, `1 - |reponse_predite - reponse_vraie| / etendue`, les deux reponses
     etant ramenees dans [0, 1] par leur rang normalise, donc etendue = 1. Une prediction
     absente ou hors nomenclature recoit la valeur la plus severe, zero, comme en a29 ou
     un refus compte comme une reponse non minoritaire ; le taux de refus est rapporte.
  5. **Le rapport d'ecarts types par resultat**, leur quatrieme mesure : pour chaque item
     ordinal, l'ecart type des valeurs predites sur les personnes divise par l'ecart type
     des valeurs humaines de la vague 1 sur les memes personnes, puis moyenne sur les
     items. C'est un rapport TOTAL, comme le leur, et non le rapport INTRA de a1 et de
     FAITS-ETABLIS section 1 : les deux quantites ne sont pas comparables en valeur et le
     rapport le dit.

Toutes les incertitudes sont des bootstraps sur les PERSONNES : deux reponses d'une meme
personne ne sont pas independantes, un bootstrap sur les cellules donnerait un intervalle
faussement etroit.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import sys
from collections import Counter

# Limite de quatre coeurs, posee avant l'import de numpy sinon elle est sans effet.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
from a2_commun import est_manquant
from a25_commun import ORDINAUX, sans_score

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260908

# Les trois seuils. Les deux premiers sont ceux de leur code, le troisieme est la
# transposition categorielle du "5 pour cent du haut" : une modalite majoritaire qui
# depasse 95 pour cent des repondants.
PART = 0.05
SEUIL_BAS = 0.05
SEUIL_HAUT = 0.95

TRANCHES = ["bas", "milieu", "haut"]

LLM = C28.LLM
STAT = C28.STAT

# Un temoin de plus que a28 et a29 : le tirage UNIFORME sur la nomenclature de l'item.
# C'est leur `random_benchmark`, "tirage uniforme sur l'etendue du resultat", et ce n'est
# pas notre `B0 tirage`, qui tire dans la marginale observee de l'item et se concentre
# donc sur la modalite majoritaire. Sans lui, la ligne de leur tableau qui dit que le
# hasard bat l'etiquette sur les 5 pour cent du bas n'a pas d'equivalent chez nous.
UNIFORME = "B0 uniforme"

ORDRE_METHODES = [c for c in C28.ORDRE_METHODES if c != "humains vague 2"]
ORDRE_METHODES = (ORDRE_METHODES[:ORDRE_METHODES.index("B0 mode")] + [UNIFORME]
                  + ORDRE_METHODES[ORDRE_METHODES.index("B0 mode"):]
                  + ["humains vague 2"])

# Les trois familles de conditions, telles que le rapport les lit. Ce n'est pas un
# resultat, c'est une nomenclature, et elle est ecrite ici pour qu'elle soit contestable.
#   "riche"     : la persona porte de l'information individuelle au dela de l'etiquette ;
#   "etiquette" : l'invite ne porte que des attributs de segment ;
#   "aveugle"   : aucune information individuelle, ou aucun modele de langage.
FAMILLE_CONDITION = {
    "agents composite": "riche", "agents entretien (v3)": "riche",
    "agents enquete": "riche", "agents v7": "riche", "C3": "riche",
    "agents demographiques (v6)": "etiquette", "agents v8": "etiquette", "C2": "etiquette",
    "B0 mode": "aveugle", "B0 tirage": "aveugle", UNIFORME: "aveugle",
    "B1 argmax": "statistique", "B2 argmax": "statistique", "B3 foret": "statistique",
    "humains vague 2": "plancher",
}

# Les valeurs publiees dans le depot de Peng et al., lues telles quelles par a36 section
# 6.3 et section 6.2. Aucun calcul de notre part sur ces nombres, ils servent de colonne
# de comparaison et de rien d'autre.
PENG_TRANCHES = {
    "full_persona_without_reasoning": {"milieu": 0.7643, "bas": 0.5416, "haut": 0.6623},
    "demographics_only": {"milieu": 0.7644, "bas": 0.5165, "haut": 0.6475},
    "empty_persona": {"milieu": 0.7530, "bas": 0.4644, "haut": 0.6504},
    "random_benchmark": {"milieu": 0.6401, "bas": 0.5325, "haut": 0.5221},
}

PENG_STD_RATIO = {
    "random_benchmark": 1.139,
    "full_persona_fine_tuned_temperature_7": 1.061,
    "full_persona_fine_tuned_temperature_0": 0.897,
    "llama_persona_summary": 0.924,
    "deepseek": 0.734,
    "gemini": 0.685,
    "centaur_persona_summary": 0.666,
    "full_persona_without_reasoning": 0.634,
    "persona_summary": 0.623,
    "temperature_zero": 0.615,
    "demographics_only": 0.575,
    "demographics_only_temperature_zero": 0.557,
    "empty_persona": 0.446,
    "empty_persona_temperature_zero": 0.377,
}

holm = C28.holm
benjamini_hochberg = C28.benjamini_hochberg
ecrire = C28.ecrire


def norm(v):
    return str(v).lower().strip()


# ---------------------------------------------------------------------------
# 1. Chargement
# ---------------------------------------------------------------------------

def charger(cache, cache_foret):
    return C28.charger_tout(cache, cache_foret)


def perimetres(paquet):
    return {"150": np.asarray(paquet["lignes150"], dtype=int),
            "1052": np.arange(len(paquet["ids"]), dtype=int)}


def baseline_uniforme(items, options, n, graine=GRAINE):
    """Tirage uniforme sur la nomenclature declaree de chaque item.

    C'est leur `random_benchmark`, transpose a une reponse categorielle : chaque cellule
    recoit une modalite tiree uniformement parmi les modalites declarees de l'item dans
    `question_master/gss/main.csv`, sans regarder ni la personne ni la distribution
    observee. Ce temoin ne connait donc pas la marginale, contrairement a `B0 tirage`,
    et il est le seul de nos temoins qui soit comparable au leur.
    """
    rng = np.random.default_rng(graine)
    out = np.empty((n, len(items)), dtype=object)
    for j, it in enumerate(items):
        opts = options[it]
        out[:, j] = np.array([opts[k] for k in rng.integers(0, len(opts), n)],
                             dtype=object)
    return out


def methodes_du_perimetre(paquet, nom_perimetre):
    toutes = [c for c in ORDRE_METHODES if c in paquet["M"]]
    if nom_perimetre == "1052":
        return [c for c in toutes if c not in ("C2", "C3")]
    return toutes


def observe(mat):
    return np.array([[not est_manquant(v) for v in ligne] for ligne in mat], dtype=bool)


# ---------------------------------------------------------------------------
# 2. Items ordinaux et scores de rang
# ---------------------------------------------------------------------------

def items_ordinaux(items, options):
    """Les items traites comme ordinaux, definition de a25 importee sans retouche.

    Un item est ordinal s'il figure dans a25_commun.ORDINAUX et s'il ne porte aucune
    modalite du type "Inapplicable", qui n'a pas de place sur une echelle.
    """
    return [it for it in items
            if it in ORDINAUX and not any(sans_score(o) for o in options[it])]


def table_de_rang(items, options):
    """item -> {modalite normalisee: rang normalise dans [0, 1]}.

    L'ordre employe est celui de `question_master/gss/main.csv`, le meme que celui de a1,
    a25 et a28 pour la distance de Wasserstein. C'est une hypothese heritee et non
    verifiee item par item : si l'ordre du fichier n'etait pas l'ordre de l'echelle, la
    mesure ordinale serait fausse pour cet item. Le rapport la signale.
    """
    table = {}
    for it in items:
        opts = options[it]
        k = len(opts)
        if k < 2:
            continue
        table[it] = {norm(o): r / (k - 1.0) for r, o in enumerate(opts)}
    return table


def matrice_scores(mat, colonnes, items, rangs):
    """Matrice de valeurs dans [0, 1], NaN si la cellule est vide ou hors nomenclature."""
    n = mat.shape[0]
    out = np.full((n, len(colonnes)), np.nan)
    for c, j in enumerate(colonnes):
        table = rangs.get(items[j])
        if table is None:
            continue
        col = mat[:, j]
        for i in range(n):
            v = col[i]
            if v is None or est_manquant(v):
                continue
            s = table.get(norm(v))
            if s is not None:
                out[i, c] = s
    return out


# ---------------------------------------------------------------------------
# 3. Les deux definitions de tranche
# ---------------------------------------------------------------------------

def tranches_rarete(verite, seuil_bas=SEUIL_BAS, seuil_haut=SEUIL_HAUT):
    """Matrice d'entiers : 0 bas, 1 milieu, 2 haut, -1 cellule non evaluable.

    Renvoie aussi, item par item, la part de la modalite majoritaire et le nombre de
    modalites sous le seuil bas, pour que le rapport puisse dire combien d'items portent
    reellement une tranche haute.
    """
    ok = observe(verite)
    n, m = verite.shape
    tr = np.full((n, m), -1, dtype=np.int8)
    detail = []
    for j in range(m):
        vals = [norm(v) for v, o in zip(verite[:, j], ok[:, j]) if o]
        if not vals:
            detail.append({"n": 0, "part_modale": np.nan, "n_modalites_rares": 0})
            continue
        c = Counter(vals)
        total = float(len(vals))
        rares = {k for k, v in c.items() if v / total < seuil_bas}
        modale, effectif = c.most_common(1)[0]
        haut = {modale} if effectif / total > seuil_haut else set()
        for i in range(n):
            if not ok[i, j]:
                continue
            v = norm(verite[i, j])
            tr[i, j] = 0 if v in rares else (2 if v in haut else 1)
        detail.append({"n": int(total), "part_modale": effectif / total,
                       "n_modalites_rares": len(rares)})
    return tr, pd.DataFrame(detail)


def tranches_ordinales(scores_vrais, part=PART, graine=GRAINE):
    """Leur definition, mot pour mot : tri des repondants par leur vraie valeur.

    scores_vrais : matrice (personnes x items ordinaux) de valeurs dans [0, 1], NaN si la
    cellule est vide. Pour chaque item, les repondants observes sont tries ; les `part`
    premiers sont la tranche basse, les `part` derniers la tranche haute, le reste est le
    milieu.

    Les egalites sont departagees par une permutation aleatoire de graine fixe. Sur une
    echelle a trois modalites la tranche basse est presque toujours un sous ensemble
    arbitraire des personnes qui ont donne la valeur minimale : c'est une propriete de
    leur definition appliquee a des reponses discretes, pas un choix de notre part, et le
    tirage aleatoire est la maniere non biaisee de la subir.
    """
    rng = np.random.default_rng(graine)
    n, m = scores_vrais.shape
    tr = np.full((n, m), -1, dtype=np.int8)
    tailles = []
    for j in range(m):
        rows = np.flatnonzero(~np.isnan(scores_vrais[:, j]))
        if len(rows) < 20:
            tailles.append({"n": len(rows), "n_bas": 0, "n_haut": 0})
            continue
        melange = rng.permutation(len(rows))
        rows_m = rows[melange]
        ordre = rows_m[np.argsort(scores_vrais[rows_m, j], kind="stable")]
        nb = max(1, int(round(part * len(rows))))
        tr[ordre, j] = 1
        tr[ordre[:nb], j] = 0
        tr[ordre[-nb:], j] = 2
        tailles.append({"n": len(rows), "n_bas": nb, "n_haut": nb})
    return tr, pd.DataFrame(tailles)


def tranches_extremes_echelle(scores_vrais):
    """Variante de robustesse, sans convention d'egalite : les bouts de l'echelle.

    bas  = la personne a donne la modalite la plus basse de l'item ;
    haut = la personne a donne la modalite la plus haute ;
    milieu = le reste. Les tranches ne font plus 5 et 90 pour cent, mais aucune personne
    n'est classee par un tirage.
    """
    n, m = scores_vrais.shape
    tr = np.full((n, m), -1, dtype=np.int8)
    for j in range(m):
        col = scores_vrais[:, j]
        ok = ~np.isnan(col)
        if ok.sum() == 0:
            continue
        tr[ok, j] = 1
        tr[ok & (col <= 0.0), j] = 0
        tr[ok & (col >= 1.0), j] = 2
    return tr


# ---------------------------------------------------------------------------
# 4. Exactitude par tranche, comptes par personne
# ---------------------------------------------------------------------------

def scores_exactitude_categorielle(pred, verite, ok):
    """Matrice de scores dans {0, 1} : 1 si la prediction egale la vraie reponse.

    Une prediction absente compte comme fausse et la cellule reste au denominateur.
    C'est la convention severe de a29, reprise sans changement.
    """
    juste = np.full(verite.shape, np.nan)
    juste[ok] = 0.0
    juste[(pred == verite) & ok] = 1.0
    return juste


def scores_exactitude_ordinale(pred_scores, vrais_scores):
    """Leur mesure : 1 - |predit - vrai| / etendue, les valeurs etant deja dans [0, 1].

    Une prediction absente ou hors nomenclature recoit zero, valeur la plus severe.
    """
    d = np.abs(pred_scores - vrais_scores)
    s = 1.0 - d
    s[np.isnan(pred_scores)] = 0.0
    s[np.isnan(vrais_scores)] = np.nan
    return s


def comptes_par_tranche(scores, tranche, lignes):
    """num et den par personne et par tranche, sur un perimetre de lignes.

    scores  : matrice de scores d'exactitude, NaN hors perimetre d'evaluation ;
    tranche : matrice d'entiers 0 / 1 / 2, -1 hors evaluation ;
    Retourne {nom_de_tranche: (num, den)}, deux vecteurs de longueur len(lignes).
    """
    s = scores[lignes]
    t = tranche[lignes]
    out = {}
    for k, nom in enumerate(TRANCHES):
        masque = (t == k) & ~np.isnan(s)
        num = np.where(masque, np.nan_to_num(s), 0.0).sum(axis=1)
        den = masque.sum(axis=1).astype(float)
        out[nom] = (num, den)
    masque = (t >= 0) & ~np.isnan(s)
    out["ensemble"] = (np.where(masque, np.nan_to_num(s), 0.0).sum(axis=1),
                       masque.sum(axis=1).astype(float))
    return out


def ratio(num, den, idx=None):
    if idx is None:
        d = den.sum()
        return float(num.sum() / d) if d > 0 else np.nan
    d = den[idx].sum(axis=-1)
    n = num[idx].sum(axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(d > 0, n / np.maximum(d, 1e-12), np.nan)


def bootstrap_ratio(num, den, idx_boot):
    """Distribution bootstrap du ratio, personnes reechantillonnees."""
    return ratio(num, den, idx_boot)


def ic(tir):
    tir = np.asarray(tir, float)
    tir = tir[~np.isnan(tir)]
    if len(tir) == 0:
        return np.nan, np.nan
    return float(np.percentile(tir, 2.5)), float(np.percentile(tir, 97.5))


def p_bilateral(tir):
    """p bilateral d'une distribution bootstrap de difference, contre zero.

    Plancher a 1 / nombre de tirages, ce qui evite d'ecrire p = 0 apres une correction
    pour tests multiples. Convention de a28, a29 et a31.
    """
    tir = np.asarray(tir, float)
    tir = tir[~np.isnan(tir)]
    if len(tir) == 0:
        return 1.0
    p = 2.0 * min(float((tir <= 0).mean()), float((tir >= 0).mean()))
    return float(min(max(p, 1.0 / len(tir)), 1.0))


def tirages_bootstrap(n, tirages, rng):
    return rng.integers(0, n, (tirages, n))


# ---------------------------------------------------------------------------
# 5. Rapport d'ecarts types par resultat, leur quatrieme mesure
# ---------------------------------------------------------------------------

def _sd_colonnes(a, ddof=1):
    """Ecart type colonne par colonne en ignorant les NaN, sans biais."""
    with np.errstate(invalid="ignore", divide="ignore"):
        n = (~np.isnan(a)).sum(axis=0)
        s = np.nanstd(a, axis=0, ddof=ddof)
    return np.where(n > ddof, s, np.nan), n


def rapport_ecarts_types(pred_scores, vrais_scores, lignes, n_min=30):
    """Un rapport par item ordinal : ecart type predit sur ecart type humain.

    Comme chez eux, le rapport est calcule sur l'echantillon APPARIE : une personne entre
    dans le calcul d'un item si sa vraie reponse de la vague 1 et la prediction de la
    methode sont toutes deux exploitables. Le numerateur et le denominateur portent donc
    exactement sur les memes personnes, ce qui est necessaire pour que le rapport mesure
    une difference de dispersion et non une difference d'echantillon. Ecart type sans
    biais, ddof = 1.
    """
    p = pred_scores[lignes]
    v = vrais_scores[lignes]
    commun = ~np.isnan(p) & ~np.isnan(v)
    pa = np.where(commun, p, np.nan)
    va = np.where(commun, v, np.nan)
    sp, n = _sd_colonnes(pa)
    sh, _ = _sd_colonnes(va)
    assez = n >= n_min
    with np.errstate(invalid="ignore", divide="ignore"):
        r = np.where(assez & (sh > 0), sp / sh, np.nan)
    return pd.DataFrame({"sd_pred": np.where(assez, sp, np.nan),
                         "sd_humain": np.where(assez, sh, np.nan),
                         "ratio": r, "n": n})


def _variances_par_colonne(a, seg, n_seg):
    """var totale, var inter segments et var intra segments, colonne par colonne.

    a   : matrice (personnes x items) de valeurs dans [0, 1], NaN si la cellule est vide ;
    seg : vecteur d'entiers de segment, -1 pour un segment inconnu.
    La decomposition est celle de la variance totale : var_total = var_inter + var_intra,
    avec des estimateurs a la population, denominateur N. C'est la meme identite que a1,
    sur la valeur numerique de la reponse et non sur l'indice de Gini Simpson : les deux
    quantites ne sont pas la meme et le rapport le dit.
    """
    ok = ~np.isnan(a) & (seg >= 0)[:, None]
    x = np.where(ok, np.nan_to_num(a), 0.0)
    n = ok.sum(axis=0).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        m = np.where(n > 0, x.sum(axis=0) / np.maximum(n, 1), np.nan)
        v_tot = np.where(n > 0, (x ** 2).sum(axis=0) / np.maximum(n, 1) - m ** 2, np.nan)
    v_inter = np.zeros(a.shape[1])
    for g in range(n_seg):
        mg = ok & (seg == g)[:, None]
        ng = mg.sum(axis=0).astype(float)
        with np.errstate(invalid="ignore", divide="ignore"):
            mgm = np.where(ng > 0, np.where(mg, np.nan_to_num(a), 0.0).sum(axis=0)
                           / np.maximum(ng, 1), 0.0)
        v_inter += np.where(ng > 0, ng * (mgm - np.nan_to_num(m)) ** 2, 0.0)
    with np.errstate(invalid="ignore", divide="ignore"):
        v_inter = np.where(n > 0, v_inter / np.maximum(n, 1), np.nan)
    return v_tot, v_inter, np.maximum(v_tot - v_inter, 0.0), n


def decomposition_dispersion(pred_scores, vrais_scores, seg, lignes, n_seg,
                             idx_boot=None, n_min=30):
    """Rapport d'ecarts types total, inter segments et intra segment, par item ordinal.

    Le rapport total est celui de Peng et al. Les deux autres sont notre decomposition,
    celle que leur mesure ne fait pas et que a36 section 3.1 signale comme absente de leur
    article. Tout est calcule sur l'echantillon apparie, personnes ou la vraie reponse et
    la prediction sont toutes deux exploitables.
    """
    p = pred_scores[lignes]
    v = vrais_scores[lignes]
    s = seg[lignes]
    commun = ~np.isnan(p) & ~np.isnan(v)
    pa, va = np.where(commun, p, np.nan), np.where(commun, v, np.nan)

    def moyennes(pa_, va_, s_):
        tp, ip, wp, n = _variances_par_colonne(pa_, s_, n_seg)
        th, ih, wh, _ = _variances_par_colonne(va_, s_, n_seg)
        assez = n >= n_min
        out = {}
        for nom, a_, b_ in (("total", tp, th), ("inter", ip, ih), ("intra", wp, wh)):
            with np.errstate(invalid="ignore", divide="ignore"):
                r = np.where(assez & (b_ > 0), np.sqrt(np.maximum(a_, 0.0)
                                                       / np.maximum(b_, 1e-300)), np.nan)
            out[nom] = r
        return out

    point = moyennes(pa, va, s)
    res = {nom: {"moyenne": float(np.nanmean(r)),
                 "mediane": float(np.nanmedian(r)),
                 "n_items": int(np.isfinite(r).sum())}
           for nom, r in point.items()}
    if idx_boot is not None:
        tir = {nom: np.empty(len(idx_boot)) for nom in point}
        for t, idx in enumerate(idx_boot):
            o = moyennes(pa[idx], va[idx], s[idx])
            for nom in point:
                tir[nom][t] = (float(np.nanmean(o[nom]))
                               if np.isfinite(o[nom]).any() else np.nan)
        for nom in point:
            lo, hi = ic(tir[nom])
            res[nom]["ic_bas"], res[nom]["ic_haut"] = lo, hi
    return res, point


def bootstrap_moyenne_ratio(pred_scores, vrais_scores, lignes, idx_boot, n_min=30):
    """Intervalle du rapport moyen, personnes reechantillonnees.

    Le rapport est recalcule item par item sur chaque tirage puis moyenne : c'est le meme
    estimateur que la valeur observee, ce qui evite qu'un intervalle porte sur une autre
    quantite que le point.
    """
    p = pred_scores[lignes]
    v = vrais_scores[lignes]
    commun = ~np.isnan(p) & ~np.isnan(v)
    pa = np.where(commun, p, np.nan)
    va = np.where(commun, v, np.nan)
    tir = np.empty(len(idx_boot))
    for t, idx in enumerate(idx_boot):
        sp, n = _sd_colonnes(pa[idx])
        sh, _ = _sd_colonnes(va[idx])
        with np.errstate(invalid="ignore", divide="ignore"):
            r = np.where((n >= n_min) & (sh > 0), sp / sh, np.nan)
        tir[t] = float(np.nanmean(r)) if np.isfinite(r).any() else np.nan
    return tir
