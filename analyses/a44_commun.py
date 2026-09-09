"""
a44_commun : briques partagees par le test du generateur nul conditionnellement
independant de Yuan (arXiv 2607.02368 v3), applique a nos populations simulees.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a28_commun,
a29_commun, a31_commun, a35_commun, a2_commun, a25_commun, a8_commun, et par eux
a2_baselines_gss, a5_evaluer, a5_agents_locaux_gss, a25_mesures. Les 1 052 personnes, les
149 items, les plis, les blocs, les graines, les 150 personnes du run local, la definition
des modalites minoritaires, les estimateurs de dispersion a biais corrige et le temoin
aveugle a la personne viennent de la, sans une ligne recopiee.

LE PREENREGISTREMENT EST resultats/a44-preenregistrement.md, ECRIT AVANT CE FICHIER.

Ce module porte cinq choses et rien d'autre.

  1. Le codage entier des matrices de reponse sur la nomenclature ORDONNEE de
     question_master/gss/main.csv. Le meme alphabet sert a toutes les conditions, ce qui
     rend le generateur nul et la population comparables case par case.

  2. Le generateur nul, transposition categorielle de l'equation (2) de Yuan. Chez lui
     X_ij ~ N(mu_{j,g}, sigma_{j,g}) tronque et arrondi sur cinq points ; ici
     X_ij ~ Multinomiale(p_{j,g}), ou p_{j,g} est la loi empirique de l'item j a
     l'interieur du segment g DE LA CONDITION ELLE MEME. Aucune structure latente, aucune
     covariance entre items, aucune dependance entre cellules. Le masque de la condition
     est conserve a l'identique : une cellule vide ou refusee reste vide.

  3. Les sept quantites du preenregistrement, calculees a l'identique sur une population
     et sur son nul :
       Q1 ratio inter, Q2 ratio intra   -> a35_commun.sommes_dispersion_rapide, qui est la
                                           version vectorisee des estimateurs de a1
       Q3 patrons de reponses distincts -> nouveau
       Q4 correlation inter items brute -> nouveau
       Q5 correlation inter items residualisee du segment -> nouveau, quantite primaire
       Q6 rapport groupe sur personne   -> a31_commun, temoin aveugle a la personne
       Q7 rappel des cellules rares     -> a29_commun / a8_commun

  4. La permutation des personnes a l'interieur du segment, qui remplace la perturbation
     d'ordre des items de Yuan, impossible sans appel de modele (cf. preenregistrement
     section 6).

  5. Les deux controles bloquants du preenregistrement section 8.

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
import a29_commun as C29
import a31_commun as C31
from a35_commun import sommes_dispersion_rapide
from a2_commun import est_manquant, exactitude_par_personne
from a8_commun import modalites_minoritaires

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260908
SEUIL_RARE = 0.10
N_REPLICATS = 200
N_PERMUTATIONS = 200
N_BOOTSTRAP = 1000
N_MIN_SEGMENT = 5          # sous cet effectif observe, repli sur la marginale de l'item
N_MIN_ITEM = 30            # seuil de a1 pour qu'un item entre dans la somme de dispersion
N_MIN_PAIRE = 30           # personnes communes minimales pour qu'une paire d'items compte

# Les treize conditions de la famille declaree, plus les trois descriptives.
CONDITIONS = [
    "humains vague 1", "humains vague 2",
    "agents composite", "agents entretien (v3)", "agents enquete",
    "agents demographiques (v6)", "agents v7", "agents v8",
    "C2", "C3",
    "B1 argmax", "B2 argmax", "PMM k=10",
]
DESCRIPTIVES = ["B0 mode", "B0 tirage", "B3 foret"]

# Les memes humains restreints aux 150 personnes du run local. Sans eux, C2 et C3 n'ont
# aucune reference sur leur propre perimetre : le plancher de bruit de toutes les
# quantites depend de l'effectif, et une comparaison a la ligne humaine des 1 052 serait
# fausse. Ce sont des references descriptives, elles n'entrent dans aucune famille.
DOUBLONS_150 = {"humains vague 1 (150)": "humains vague 1",
                "humains vague 2 (150)": "humains vague 2"}
TOUTES = CONDITIONS + DESCRIPTIVES + list(DOUBLONS_150)

# Perimetre naturel de chaque condition. C2 et C3 n'existent que sur les 150 personnes du
# run local ; les mesures a 150 et a 1 052 ne sont jamais comparees dans un test.
PERIMETRE = {c: ("150" if c in ("C2", "C3") or c in DOUBLONS_150 else "1052")
             for c in TOUTES}

ETIQUETTE = {
    "humains vague 1": "humains v1", "humains vague 2": "humains v2",
    "agents composite": "composite", "agents entretien (v3)": "entretien v3",
    "agents enquete": "enquete", "agents demographiques (v6)": "v6",
    "agents v7": "v7", "agents v8": "v8", "C2": "C2", "C3": "C3",
    "B1 argmax": "B1", "B2 argmax": "B2", "PMM k=10": "PMM k=10",
    "B0 mode": "B0 mode", "B0 tirage": "B0 tirage", "B3 foret": "B3 foret",
    "humains vague 1 (150)": "humains v1, 150", "humains vague 2 (150)": "humains v2, 150",
}


# ---------------------------------------------------------------------------
# 1. Chargement et codage
# ---------------------------------------------------------------------------

def charger(cache, cache_foret, cache_a35):
    """Paquet de a28 / a29, augmente de PMM k=10 relu du cache de a35.

    Rien n'est recalcule : les trois caches sont ceux que a25, a28 et a35 ont deja ecrits.
    Si le cache de a35 est absent, PMM est simplement absent du tableau et le rapport le
    dit ; il n'est jamais recalcule ici, ce qui reviendrait a refaire a35.
    """
    paquet = C29.charger(cache, cache_foret)
    paquet["M"]["humains vague 1"] = paquet["y1"]
    manquantes = []
    if cache_a35 and os.path.exists(cache_a35):
        import pickle
        neuf = pickle.load(open(cache_a35, "rb"))
        if "PMM k=10" in neuf:
            paquet["M"]["PMM k=10"] = np.asarray(neuf["PMM k=10"], dtype=object)
        else:
            manquantes.append("PMM k=10")
    else:
        manquantes.append("PMM k=10")
    for double, source in DOUBLONS_150.items():
        paquet["M"][double] = paquet["M"][source]
    paquet["absentes"] = manquantes
    return paquet


def alphabet(items, options):
    """item -> (modalite -> code entier), dans l'ORDRE de la nomenclature officielle.

    L'ordre est celui du champ Options de question_master/gss/main.csv. Pour les items
    ordinaux il correspond a l'echelle du questionnaire, ce qui autorise Q4 et Q5 sans
    invention de notre part. Le meme alphabet sert a toutes les conditions.
    """
    return [{m: k for k, m in enumerate(options[it])} for it in items]


def coder(mat, alpha):
    """Matrice objet -> matrice d'entiers, -1 pour un manquant ou un hors nomenclature.

    Renvoie aussi le taux de cellules renseignees mais hors nomenclature, qui doit rester
    au niveau mesure par a1, au plus quelques dixiemes de pour cent.
    """
    m = np.asarray(mat, dtype=object)
    codes = np.full(m.shape, -1, dtype=np.int16)
    hors = 0
    for j in range(m.shape[1]):
        table = alpha[j]
        col = m[:, j]
        for i in range(m.shape[0]):
            v = col[i]
            if est_manquant(v):
                continue
            k = table.get(v if isinstance(v, str) else str(v), -1)
            if k < 0:
                hors += 1
            else:
                codes[i, j] = k
    return codes, hors / max(m.size, 1)


def decoder(codes, options, items):
    """Matrice d'entiers -> matrice objet, l'inverse exact de coder sur les cellules pleines."""
    n, m = codes.shape
    out = np.empty((n, m), dtype=object)
    out[:] = None
    for j in range(m):
        o = options[items[j]]
        col = codes[:, j]
        pleines = np.flatnonzero(col >= 0)
        if len(pleines):
            out[pleines, j] = [o[k] for k in col[pleines]]
    return out


# ---------------------------------------------------------------------------
# 2. Segmentations
# ---------------------------------------------------------------------------

def _bloc_ideologie(v):
    """Les sept niveaux du GSS ramenes a trois. Regle mecanique de a1, sans jugement."""
    if "liberal" in v:
        return "gauche"
    if "conservative" in v:
        return "droite"
    return "centre"


def segmentations(paquet):
    """Les deux segmentations declarees, plus les six axes de a1 pour le descriptif.

    S_fin  : bloc d'ideologie x genre x age, 3 x 2 x 7 = 42 cellules au plus. Le bloc a
             trois niveaux est la regle mecanique de a1 ; les sept niveaux bruts croises
             au genre et a l'age donneraient 98 cellules pour 1 052 personnes, soit un
             repli quasi systematique sur la marginale d'item, ce qui viderait le nul de
             son conditionnement.
    S_ideo : ideologie politique, les sept niveaux bruts, exactement l'axe sur lequel a1
             section 4 et a23 lisent le 8,16 et le 8,51.
    """
    seg6, niv6 = C28.segments(paquet["x"], paquet["attributs"])
    col = {a: i for i, a in enumerate(paquet["attributs"])}
    brut = {a: [C28.norm(v) for v in paquet["x"][:, col[a]]]
            for a in ("political_ideology", "gender", "age")}
    fin = [f"{_bloc_ideologie(i)}|{g}|{a}"
           for i, g, a in zip(brut["political_ideology"], brut["gender"], brut["age"])]
    mods = sorted({v for v in fin if v.strip() and "non renseigne" not in v})
    idx = {m: k for k, m in enumerate(mods)}
    seg = {"S_fin": np.array([idx.get(v, -1) for v in fin], dtype=np.int32),
           "S_ideo": seg6["political_ideology"]}
    niveaux = {"S_fin": mods, "S_ideo": niv6["political_ideology"]}
    for a in C28.AXES:
        seg[a] = seg6[a]
        niveaux[a] = niv6[a]
    return seg, niveaux


# ---------------------------------------------------------------------------
# 3. Le generateur nul, equation (2) de Yuan transposee au categoriel
# ---------------------------------------------------------------------------

def lois_par_segment(codes, seg, k_items, n_min=N_MIN_SEGMENT):
    """Loi empirique de chaque item a l'interieur de chaque segment.

    Renvoie une liste, un element par item : un tableau (G + 1, K_j) de probabilites
    cumulees. La derniere ligne est la loi de l'item sur la condition entiere ; elle sert
    de repli pour un segment de moins de n_min repondants observes sur cet item, et pour
    les personnes de segment inconnu. Renvoie aussi le nombre de couples (item, segment)
    replies, qui est publie.
    """
    n, m = codes.shape
    g_max = int(seg.max()) + 1 if seg.size and seg.max() >= 0 else 1
    cumules, replis, total = [], 0, 0
    for j in range(m):
        col = codes[:, j]
        ok = col >= 0
        k = k_items[j]
        c = np.zeros((g_max + 1, k), dtype=np.float64)
        val = ok & (seg >= 0)
        if val.any():
            np.add.at(c, (seg[val], col[val]), 1.0)
        marge = np.zeros(k, dtype=np.float64)
        if ok.any():
            np.add.at(marge, col[ok], 1.0)
        c[g_max] = marge
        n_g = c[:g_max].sum(axis=1)
        maigre = n_g < n_min
        total += g_max
        replis += int(maigre.sum())
        c[:g_max][maigre] = marge
        somme = c.sum(axis=1, keepdims=True)
        p = np.divide(c, np.where(somme > 0, somme, 1.0))
        p[somme[:, 0] <= 0] = 0.0
        cumules.append(np.cumsum(p, axis=1))
    return cumules, replis, total


def tirer_nul(codes, seg, cumules, rng):
    """Un replicat du generateur nul, meme forme et meme masque que codes.

    X_ij ~ Multinomiale(p_{j, g(i)}), independamment sur i et sur j. Aucune structure
    latente, aucune covariance entre items. Une cellule vide dans codes reste vide.
    """
    n, m = codes.shape
    out = np.full((n, m), -1, dtype=np.int16)
    g_max = len(cumules[0]) - 1
    s = np.where(seg >= 0, seg, g_max)
    u = rng.random((n, m))
    for j in range(m):
        lignes = np.flatnonzero(codes[:, j] >= 0)
        if not len(lignes):
            continue
        cum = cumules[j]
        lig_cum = cum[s[lignes]]
        vide = lig_cum[:, -1] <= 0
        tir = (lig_cum < u[lignes, j][:, None]).sum(axis=1)
        tir = np.minimum(tir, cum.shape[1] - 1)
        tir[vide] = codes[lignes[vide], j]
        out[lignes, j] = tir
    return out


# ---------------------------------------------------------------------------
# 4. Q1 et Q2 : les deux ratios de a1
# ---------------------------------------------------------------------------

def dispersion(codes, seg, k_max, colonnes):
    """Somme sur les items des termes inter et intra, estimateur Gini Simpson sans biais.

    Appel direct de a35_commun.sommes_dispersion_rapide, qui est la version vectorisee,
    verifiee item par item contre a28_commun.dispersion_item par a35.
    """
    return sommes_dispersion_rapide(codes.astype(np.int32), seg.astype(np.int32),
                                    k_max, colonnes, n_min=N_MIN_ITEM)


def ratios(codes, ref, seg, k_max, colonnes):
    """Ratios inter et intra d'une population, rapportes aux humains de la vague 1."""
    a = dispersion(codes, seg, k_max, colonnes)
    b = dispersion(ref, seg, k_max, colonnes)
    return {"inter": a["inter"] / b["inter"] if b["inter"] else np.nan,
            "intra": a["intra"] / b["intra"] if b["intra"] else np.nan,
            "inter_brut": a["inter"], "intra_brut": a["intra"],
            "n_items": a["n_items"]}


# ---------------------------------------------------------------------------
# 5. Q3 : patrons de reponses distincts
# ---------------------------------------------------------------------------

def sous_ensembles_items(n_items, n_tirages=20, taille=10, graine=GRAINE):
    """Vingt sous ensembles de dix items, tires une fois et partages par toutes les
    conditions et par tous les replicats. Un patron sur les 149 items serait unique pour
    presque chaque personne, la quantite ne separerait rien."""
    rng = np.random.default_rng(graine)
    return [np.sort(rng.choice(n_items, size=taille, replace=False))
            for _ in range(n_tirages)]


def patrons_distincts(codes, sous_ens):
    """Nombre moyen de lignes distinctes sur les sous ensembles d'items declares.

    Une ligne comportant une cellule vide est ecartee du comptage de son sous ensemble :
    deux lignes qui different seulement par un manquant ne sont pas deux patrons.
    Renvoie la moyenne sur les sous ensembles et le nombre moyen de lignes comptees.
    """
    valeurs, effectifs = [], []
    for cols in sous_ens:
        sub = codes[:, cols]
        pleines = sub[(sub >= 0).all(axis=1)]
        if not len(pleines):
            continue
        valeurs.append(len(np.unique(pleines, axis=0)))
        effectifs.append(len(pleines))
    if not valeurs:
        return np.nan, np.nan
    return float(np.mean(valeurs)), float(np.mean(effectifs))


# ---------------------------------------------------------------------------
# 6. Q4 et Q5 : la structure de correlation entre items
# ---------------------------------------------------------------------------
#
# C'est la transposition du critere de Yuan. Chez lui, la structure interne d'un jeu de
# reponses est la matrice de correlation entre DIMENSIONS a l'interieur d'une instance,
# lue comme un point de la variete SPD. Nous n'avons pas dix items par dimension et nous
# n'avons qu'une passation par personne : la matrice intra instance n'existe pas chez
# nous. La quantite qui joue le meme role est la matrice de correlation ENTRE ITEMS sur
# la population, et surtout sa part qui survit au retrait du segment.
#
# Q4, brute, contient deux choses : ce que le segment induit, et ce qui reste a
# l'interieur du segment. Le generateur nul reproduit la premiere par construction et
# detruit la seconde. Q5 est donc la quantite qui separe, et son esperance sous le nul
# est nulle a l'erreur d'echantillonnage pres. C'est exactement ce que Yuan appelle
# "structure internal to one respondent that survives a change of measurement frame",
# ramene a ce que notre plan permet de mesurer.

def rangs_colonne(codes):
    """Rangs moyens par item sur les personnes observees, NaN pour un manquant.

    Le rang plutot que le code : la nomenclature est ordonnee mais rien ne dit que les
    intervalles sont egaux, et le rho de Spearman ne le suppose pas.
    """
    n, m = codes.shape
    r = np.full((n, m), np.nan)
    for j in range(m):
        col = codes[:, j]
        ok = np.flatnonzero(col >= 0)
        if len(ok) < 2:
            continue
        v = col[ok].astype(np.float64)
        ordre = np.argsort(v, kind="mergesort")
        tri = v[ordre]
        rg = np.empty(len(v), dtype=np.float64)
        i = 0
        while i < len(tri):
            k = i
            while k + 1 < len(tri) and tri[k + 1] == tri[i]:
                k += 1
            rg[ordre[i:k + 1]] = 0.5 * (i + k) + 1.0
            i = k + 1
        r[ok, j] = rg
    return r


def _correlation_moyenne(r, colonnes, n_min=N_MIN_PAIRE):
    """Moyenne des |rho| sur les paires d'items, correlation par paires completes.

    Les moyennes et les variances sont calculees sur l'ensemble observe de chaque item et
    non paire par paire ; l'ecart est de l'ordre du taux de manquants, qui est faible, et
    la meme convention s'applique a la population et a son nul, donc elle ne peut pas
    creer de distance entre les deux.
    """
    sub = r[:, colonnes]
    masque = ~np.isnan(sub)
    v = np.where(masque, sub, 0.0)
    n_obs = masque.sum(axis=0).astype(np.float64)
    if (n_obs < 2).any():
        garder = n_obs >= 2
        sub, masque, v = sub[:, garder], masque[:, garder], v[:, garder]
        n_obs = n_obs[garder]
    moyennes = v.sum(axis=0) / np.maximum(n_obs, 1.0)
    b = np.where(masque, sub - moyennes[None, :], 0.0)
    n_paire = masque.T.astype(np.float64) @ masque.astype(np.float64)
    cov = b.T @ b
    var = (b ** 2).T @ masque.astype(np.float64)
    with np.errstate(invalid="ignore", divide="ignore"):
        rho = cov / np.sqrt(np.maximum(var * var.T, 1e-300))
    haut = np.triu_indices(rho.shape[0], k=1)
    val, npr = rho[haut], n_paire[haut]
    bon = np.isfinite(val) & (npr >= n_min)
    if not bon.any():
        return np.nan, 0
    return float(np.abs(val[bon]).mean()), int(bon.sum())


def correlation_items(codes, colonnes, seg=None):
    """Q4 si seg est None, Q5 sinon.

    Q5 retire, item par item, le rang moyen du segment de la personne. Ce qui reste est
    la co-variation entre items A L'INTERIEUR des segments, c'est a dire exactement ce
    qu'un generateur qui tire les items independamment dans le gabarit du segment ne peut
    pas produire.
    """
    r = rangs_colonne(codes)
    if seg is not None:
        r = r.copy()
        for k in [x for x in np.unique(seg) if x >= 0]:
            lignes = np.flatnonzero(seg == k)
            if len(lignes) < 2:
                r[lignes] = np.nan
                continue
            bloc = r[lignes]
            m = ~np.isnan(bloc)
            n_g = m.sum(axis=0)
            moy = np.where(n_g > 0, np.nansum(np.where(m, bloc, 0.0), axis=0)
                           / np.maximum(n_g, 1), np.nan)
            r[lignes] = bloc - moy[None, :]
        r[seg < 0] = np.nan
    return _correlation_moyenne(r, colonnes)


# ---------------------------------------------------------------------------
# 7. Q6 et Q7 : rarete de groupe et rappel des rares, definitions de a31 et de a29
# ---------------------------------------------------------------------------

def covariables_rarete(y1_perimetre, seg_ideo, seuil=SEUIL_RARE):
    """Les covariables de a31 dont Q6 a besoin, calculees une fois par perimetre.

    Elles ne dependent que de la verite humaine, jamais de la condition evaluee : le meme
    objet sert donc a la population et a ses deux cents replicats nuls.
    """
    mods = modalites_minoritaires(y1_perimetre, seuil)
    ok = C29.observe(y1_perimetre)
    rare_vrai = C29.appartient(y1_perimetre, mods) & ok
    return {"verite": y1_perimetre, "mods": mods, "ok": ok, "rare_vrai": rare_vrai,
            "r_personne": C31.rarete_personne(rare_vrai, ok),
            "r_segment": C31.rarete_segment(rare_vrai, ok, seg_ideo)}


def masques(pred, cv):
    """Les trois masques de a29 : rarete predite, rarete juste, fausse rarete."""
    ok, rare_vrai = cv["ok"], cv["rare_vrai"]
    dispo = C29.observe(pred)
    rare_pred = C29.appartient(pred, cv["mods"]) & ok & dispo
    juste = rare_pred & (pred == cv["verite"])
    return {"rare_pred": rare_pred, "juste": juste,
            "faux_maj": rare_pred & ~juste & ~rare_vrai}


def groupe_sur_personne(pred, cv):
    """Q6 : lift de rarete de segment divise par lift de rarete de personne.

    Definition de a31 section 2.3, reprise sans retouche : la valeur mesuree sur les
    fausses raretes, divisee par le temoin aveugle a la personne, moins un ; puis le
    rapport des deux lifts. Renvoie aussi Q7, le rappel des cellules rares de a29.
    """
    m = masques(pred, cv)
    sortie = {}
    for cle, mat in (("personne", cv["r_personne"]), ("segment", cv["r_segment"])):
        num, den = C31.moyenne_par_personne(m["faux_maj"], mat)
        v = C31.taux(num, den)
        t = C31.temoin_item(m["faux_maj"], cv["ok"], mat)
        sortie[f"lift_{cle}"] = (v / t - 1.0) if (np.isfinite(t) and t > 0) else np.nan
    lp, ls = sortie["lift_personne"], sortie["lift_segment"]
    sortie["groupe_sur_personne"] = (ls / lp) if (np.isfinite(lp) and lp > 0) else np.nan
    n_rare = int(cv["rare_vrai"].sum())
    sortie["rappel_rares"] = (int(m["juste"].sum()) / n_rare) if n_rare else np.nan
    sortie["fausses_raretes"] = int(m["faux_maj"].sum())
    sortie["raretes_osees"] = int(m["rare_pred"].sum())
    return sortie


# ---------------------------------------------------------------------------
# 8. La permutation des personnes a l'interieur du segment
# ---------------------------------------------------------------------------
#
# Elle remplace la perturbation d'ordre des items de Yuan, qui demanderait 22 350 appels
# de modele par condition et qu'aucune trace a ordre fixe ne permet de reconstruire. Le
# raisonnement est le meme applique a l'autre axe de la matrice : si un agent est un
# gabarit de groupe, les reponses sont echangeables entre personnes du meme segment et
# l'exactitude ne bouge pas ; s'il porte la personne, elle chute.

def permuter_intra(n_lignes, seg, rng):
    """Une permutation des personnes a l'interieur de chaque segment.

    Les personnes de segment inconnu sont permutees entre elles. Renvoie le vecteur
    d'indices tel que pred[perm] est la matrice permutee.
    """
    perm = np.arange(n_lignes)
    for k in np.unique(seg):
        lignes = np.flatnonzero(seg == k)
        if len(lignes) > 1:
            perm[lignes] = rng.permutation(lignes)
    return perm


def exactitude(pred, verite):
    """Exactitude par personne, definition de a2 reprise sans retouche."""
    return exactitude_par_personne(pred, verite)


def reassignation_optimale(pred, verite, seg):
    """Exactitude sous le meilleur appariement intra segment, analogue de RO-BTSP.

    Reserve ecrite dans le preenregistrement section 6 : le realignement de Yuan est tire
    au hasard et n'exploite pas les donnees, celui ci les exploite. Il borne donc par le
    haut ce qu'un gabarit de groupe atteint en choisissant son alignement apres coup, il
    ne l'estime pas. Descriptif, il ne fonde aucun verdict.
    """
    from scipy.optimize import linear_sum_assignment
    ok = np.array([[not est_manquant(v) for v in ligne] for ligne in verite])
    total, compte = 0.0, 0
    for k in np.unique(seg):
        lignes = np.flatnonzero(seg == k)
        if len(lignes) < 2:
            continue
        p, v, o = pred[lignes], verite[lignes], ok[lignes]
        gain = np.zeros((len(lignes), len(lignes)))
        for a in range(len(lignes)):
            gain[:, a] = ((p == v[a][None, :]) & o[a][None, :]).sum(axis=1) \
                / max(int(o[a].sum()), 1)
        li, co = linear_sum_assignment(-gain)
        total += gain[li, co].sum()
        compte += len(lignes)
    return total / compte if compte else np.nan


# ---------------------------------------------------------------------------
# 9. Petits outils
# ---------------------------------------------------------------------------

def holm(p):
    return C29.holm(p)


def benjamini_hochberg(p):
    return C29.benjamini_hochberg(p)


def ecrire(lignes, nom):
    chemin = os.path.join(SORTIE, nom)
    pd.DataFrame(lignes).to_csv(chemin, index=False)
    print(f"ecrit {chemin}, {len(lignes)} lignes", flush=True)
    return chemin


def ic_percentile(tirages):
    t = np.asarray([x for x in tirages if np.isfinite(x)], dtype=float)
    if not len(t):
        return np.nan, np.nan, 1.0
    p = 2.0 * min((t <= 0).mean(), (t >= 0).mean())
    return (float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5)),
            float(min(max(p, 1.0 / len(t)), 1.0)))
