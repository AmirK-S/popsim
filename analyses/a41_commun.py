"""
a41_commun : briques partagees par a41, "le regime severe mesure proprement".

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a2_commun,
a2_baselines_gss, a8_commun, a28_commun, a29_commun, a31_commun, a33_commun, a34_commun,
a35_commun et a35_familles. Les 1 052 personnes, les 149 items, les six familles
thematiques, les cinq plis, les graines, les estimateurs de dispersion, la definition des
modalites minoritaires, le score de deductibilite par segment et la matrice C3F viennent
de la, sans une ligne recopiee.

Pourquoi ce module existe. a35 section 6 mesure le regime severe, celui ou la famille
thematique entiere sort du contexte du predicteur, et c'est desormais ce regime qui porte
l'essentiel de la these du projet : c'est le seul ou une condition a modele de langage
domine les methodes statistiques sur l'exactitude ET sur la dispersion. a35 section 11
point 1 le dit lui meme : "les chiffres de la section 6 sont des estimations ponctuelles
sur 58 items et 1 052 personnes, sans bootstrap et sans correction. L'ecart de 1,3 point
entre agents composite et E1 famille retiree n'est pas teste. C'est la verification la
plus utile qui manque." a41 fait cette verification.

Ce module porte cinq choses et rien d'autre.

  1. Les methodes du regime severe. Le protocole est celui de a8 section 3.1, repris par
     a35_familles sans retouche : la famille thematique entiere sort du contexte ET sert
     de cible, sur les 58 items des six familles de a2_baselines_gss.
       E1, E2, PMM k=10, IM m=10 : appel direct de a35_familles.imputer_par_famille.
       B2 famille retiree argmax : appel direct de a33_commun.b2_famille_retiree, dont le
         controle de a33 section 7 verifie qu'elle reproduit a8-familles-gss.csv a
         0,000000 pres.
       B2 famille retiree tirage : construite ici a partir des memes primitives importees
         de a2_commun. Elle n'est PAS bit a bit celle de a8 : a8 consomme son generateur
         pour B0 et B1 avant d'arriver a ce tirage, et nous ne rejouons ni B0 ni B1. Le
         controle publie verifie que la valeur tombe dans l'intervalle de a8.
       B3 foret, B0 mode, B0 tirage, B1 argmax : elles ne conditionnent que sur les
         demographies, le retrait de la famille ne change rien pour elles ; seul le
         perimetre d'items change. Le fait est ecrit dans le rapport plutot que masque.
       Les six conditions de Stanford : elles ne sont PAS replacees dans ce regime, et
         c'est l'objet de l'errata E1 de a8. Elles gardent les items cousins dans leur
         invite. Le module ne corrige pas ce biais, il le mesure a cote.

  2. Le tableau a quatre cases du regime severe : exactitude par personne, ratios inter et
     intra de a1 en Gini Simpson sans biais, diversite conservee et accord par paires de
     a0, rappel et precision des cellules minoritaires de a29, et le rappel dans le tercile
     NON deductible de a34, c'est a dire sur les cellules minoritaires ou aucune autre
     personne du segment ideologie x genre x age n'a donne cette reponse.

  3. Le bootstrap sur les PERSONNES, applique au meme tirage pour toutes les methodes, ce
     qui rend les contrastes apparies. Deux reponses d'une meme personne ne sont pas
     independantes : un bootstrap sur les cellules donnerait un intervalle faussement
     etroit. C'est la convention de a2, a29, a31, a33, a34 et a35.

  4. Des versions vectorisees de la dispersion, de l'entropie et de l'accord par paires,
     employees UNIQUEMENT dans la boucle de bootstrap pour des raisons de temps. Chacune
     est verifiee contre l'implementation de reference sur l'echantillon complet, et
     l'ecart maximal est publie dans le rapport.

  5. La condition appariee du papier de Stanford, telle que a8 errata E1 la chiffre : le
     materiel supplementaire evalue les Survey Agents sous les deux strategies de retrait,
     0,82 en score normalise avec retrait du seul item predit, 0,77 avec retrait du bloc
     entier. L'ecart de 5 points de score normalise est applique ici comme un decalage
     constant de l'exactitude par personne. Ce n'est PAS une mesure : c'est une
     transposition, elle est declaree partout ou elle apparait, et une sensibilite sur
     l'ampleur du decalage est publiee a cote.

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
import a33_commun as C33
import a34_commun as C34
import a35_commun as C35
import a35_familles as F35
import a2_baselines_gss as G
import a8_commun as C8
from a2_commun import b2_voisins, distance_hamming, en_codes, est_manquant
from a8_commun import modalites_minoritaires

RACINE = C35.RACINE
SORTIE = C35.SORTIE

GRAINE_A41 = 20260908
SEUIL_MINORITE = 0.10
AXE_PRINCIPAL = "political_ideology"
FORCE_E1 = 0.03           # penalite retenue par a35, voir a35-choix-penalite.csv

# Decalage de la condition appariee, en points d'exactitude brute. a8 errata E1 :
# 0,82 contre 0,77 de score normalise, soit 5 points, ramenes en exactitude brute par le
# plafond humain des 58 items. Le plafond est passe en argument pour que le chiffre soit
# calcule et non recopie.
ECART_NORMALISE_APPARIE = 0.05

ecrire = C35.ecrire
holm = C28.holm
benjamini_hochberg = C28.benjamini_hochberg
exactitude = C35.exactitude
diversite = C35.diversite
sommes_dispersion = C35.sommes_dispersion
sommes_dispersion_rapide = C35.sommes_dispersion_rapide
p_bilateral = C35.p_bilateral


# ---------------------------------------------------------------------------
# Nomenclature du regime severe
# ---------------------------------------------------------------------------
# Trois etiquettes par methode : le REGIME au sens de van Buuren (esperance ou tirage),
# le CONDITIONNEMENT, c'est a dire ce que la methode sait de la personne, et le
# TRAITEMENT DE LA FAMILLE, qui est la colonne nouvelle de ce rapport : la famille
# thematique est elle retiree du contexte de la methode, oui, non, ou sans objet parce que
# la methode ne voit aucun item.

SEVERE = [
    "E1 famille retiree (argmax)",
    "E2 famille retiree (tirage)",
    "PMM k=10 famille retiree",
    "IM m=10 mode, famille retiree",
    "B2 famille retiree (argmax)",
    "B2 famille retiree (tirage)",
]

DEMOGRAPHIQUES = ["B3 foret", "B1 argmax", "B0 mode", "B0 tirage"]

STANFORD = ["agents composite", "agents entretien (v3)", "agents enquete",
            "agents demographiques (v6)", "agents v7", "agents v8"]

# Lignes de repere du regime facile, les memes methodes avec le decoupage aleatoire en
# blocs de a2. Elles ne sont jamais dans une famille d'hypotheses : elles servent a lire
# ce que le retrait coute.
FACILE = ["E1 regression contexte argmax", "E2 regression contexte tirage",
          "PMM k=10", "IM m=10 mode des m", "B2 argmax", "B2 tirage"]

# Les neuf methodes statistiques du regime severe qui portent la famille primaire. Les
# sept nommees par la consigne, plus les deux methodes a tirage qui manquaient a la liste
# et sans lesquelles la question finale, "le modele de langage domine t il les imputations
# STATISTIQUES A TIRAGE", ne pourrait pas etre posee.
ADVERSAIRES_F1 = [
    "E1 famille retiree (argmax)",
    "E2 famille retiree (tirage)",
    "PMM k=10 famille retiree",
    "IM m=10 mode, famille retiree",
    "B2 famille retiree (argmax)",
    "B2 famille retiree (tirage)",
    "B3 foret",
    "B0 mode",
    "B0 tirage",
]

REGIME = {
    "E1 famille retiree (argmax)": "esperance",
    "E2 famille retiree (tirage)": "tirage",
    "PMM k=10 famille retiree": "tirage",
    "IM m=10 mode, famille retiree": "esperance",
    "B2 famille retiree (argmax)": "esperance",
    "B2 famille retiree (tirage)": "tirage",
    "E1 regression contexte argmax": "esperance",
    "E2 regression contexte tirage": "tirage",
    "PMM k=10": "tirage",
    "IM m=10 mode des m": "esperance",
    "B2 argmax": "esperance",
    "B2 tirage": "tirage",
    "B3 foret": "esperance",
    "B1 argmax": "esperance",
    "B0 mode": "esperance",
    "B0 tirage": "tirage",
    "humains vague 2": "humains",
}
for _c in STANFORD + ["C2", "C3", "C3F"]:
    REGIME[_c] = "modele de langage"

FAMILLE_RETIREE = {}
for _c in SEVERE:
    FAMILLE_RETIREE[_c] = "oui"
for _c in FACILE:
    FAMILLE_RETIREE[_c] = "non, blocs aleatoires"
for _c in DEMOGRAPHIQUES:
    FAMILLE_RETIREE[_c] = "sans objet, aucun item vu"
for _c in STANFORD + ["C2"]:
    FAMILLE_RETIREE[_c] = "NON, les cousins restent dans l'invite"
FAMILLE_RETIREE["C3"] = "non, bloc secret retire seulement"
FAMILLE_RETIREE["C3F"] = "oui"
FAMILLE_RETIREE["humains vague 2"] = "sans objet"

CONDITIONNEMENT = {
    "E1 famille retiree (argmax)": "149 moins la famille, et 11 demographies",
    "E2 famille retiree (tirage)": "149 moins la famille, et 11 demographies",
    "PMM k=10 famille retiree": "149 moins la famille, et 11 demographies",
    "IM m=10 mode, famille retiree": "149 moins la famille, et 11 demographies",
    "B2 famille retiree (argmax)": "149 moins la famille",
    "B2 famille retiree (tirage)": "149 moins la famille",
    "E1 regression contexte argmax": "119 items et 11 demographies",
    "E2 regression contexte tirage": "119 items et 11 demographies",
    "PMM k=10": "119 items et 11 demographies",
    "IM m=10 mode des m": "119 items et 11 demographies",
    "B2 argmax": "119 items", "B2 tirage": "119 items",
    "B3 foret": "11 demographies", "B1 argmax": "11 demographies",
    "B0 mode": "rien", "B0 tirage": "rien",
    "agents composite": "entretien et questionnaire, cousins compris",
    "agents entretien (v3)": "entretien, cousins compris",
    "agents enquete": "questionnaire, cousins compris",
    "agents demographiques (v6)": "etiquette demographique",
    "agents v7": "persona", "agents v8": "etiquette demographique",
    "C2": "etiquette demographique",
    "C3": "119 items, sans etiquette",
    "C3F": "149 moins la famille, sans etiquette",
    "humains vague 2": "la personne elle meme",
}

# Ordre d'affichage stable dans tous les tableaux de a41.
ORDRE = (["humains vague 2"] + STANFORD + ["C3", "C3F", "C2"]
         + SEVERE + DEMOGRAPHIQUES + FACILE)


# ---------------------------------------------------------------------------
# 1. Chargement et construction des methodes du regime severe
# ---------------------------------------------------------------------------

def charger_paquet(cache, cache_foret, cache_a35):
    """Paquet de a35, plus les methodes nouvelles de a35 relues de son cache."""
    import pickle
    paquet = C35.charger_paquet(cache, cache_foret)
    if cache_a35 and os.path.exists(cache_a35):
        brut = pickle.load(open(cache_a35, "rb"))
        for nom, mat in brut.items():
            if not nom.startswith("_"):
                paquet["M"][nom] = mat
        print(f"methodes de a35 relues du cache {cache_a35}")
    else:
        raise SystemExit(
            f"cache a35 absent : {cache_a35}. Rejouer a35_imputation.py d'abord, "
            "sans quoi les methodes du regime facile ne sont pas disponibles.")
    return paquet


def colonnes_familles(items):
    """Indices des 58 items de famille, et le dictionnaire nom -> colonnes."""
    index = {it: j for j, it in enumerate(items)}
    familles = {nom: [index[i] for i in membres if i in index]
                for nom, membres in G.FAMILLES.items()}
    tous = sorted({j for cols in familles.values() for j in cols})
    return tous, familles


def b2_famille_retiree_tirage(paquet, graine=GRAINE_A41, verbeux=True):
    """B2 famille retiree en mode TIRAGE, memes plis, meme K, meme distance que a8.

    Elle n'est pas bit a bit celle de a8 : a8 consomme son generateur pour B0 et B1 avant
    d'arriver a ce tirage, et nous ne rejouons ni B0 ni B1. Ce serait recopier a8_familles
    pour rien. Le controle publie verifie que la valeur obtenue tombe dans l'intervalle de
    confiance publie par a8, [0,5777 ; 0,5892].
    """
    items, y1 = paquet["items"], paquet["y1"]
    n, m = y1.shape
    plis, _ = C8.grille_gss(n, m)
    codes = en_codes(y1)
    _tous, familles = colonnes_familles(items)
    rng = np.random.default_rng(graine)
    pred = np.empty((n, m), dtype=object)
    pred[:] = None
    for i_pli, (tr, te) in enumerate(plis):
        for _nom, cols in familles.items():
            contexte = np.setdiff1d(np.arange(m), cols)
            d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
            for j in cols:
                pred[np.ix_(te, [j])] = b2_voisins(d, y1[tr, j], C8.K_A2, rng,
                                                   tirage=True)[:, None]
        if verbeux:
            print(f"  B2 famille retiree tirage, pli {i_pli + 1}/{len(plis)}", flush=True)
    return pred


def construire_severe(paquet, force=FORCE_E1, cache=None):
    """Ajoute au dictionnaire de matrices les six methodes du regime severe."""
    import pickle
    if cache and os.path.exists(cache):
        neuf = pickle.load(open(cache, "rb"))
        print(f"methodes du regime severe relues du cache {cache}")
    else:
        y1, x, items = paquet["y1"], paquet["x"], paquet["items"]
        n, m = y1.shape
        plis, _ = G.grille(n, m, G.GRAINE)
        _tous, familles = colonnes_familles(items)
        print("construction du regime severe, E1 E2 PMM IM par a35_familles")
        neuf = dict(F35.imputer_par_famille(y1, x, plis, familles, force))
        print("construction du regime severe, B2 famille retiree argmax par a33_commun")
        neuf["B2 famille retiree (argmax)"] = C33.b2_famille_retiree(paquet)
        print("construction du regime severe, B2 famille retiree tirage")
        neuf["B2 famille retiree (tirage)"] = b2_famille_retiree_tirage(paquet)
        if cache:
            pickle.dump(neuf, open(cache, "wb"))
    for nom, mat in neuf.items():
        paquet["M"][nom] = mat
    return neuf


def methodes_disponibles(paquet, avec_facile=True, avec_locales=True):
    """Liste ordonnee des conditions presentes dans le paquet."""
    out = []
    for nom in ORDRE:
        if nom not in paquet["M"]:
            continue
        if not avec_facile and nom in FACILE:
            continue
        if not avec_locales and nom in ("C2", "C3", "C3F"):
            continue
        out.append(nom)
    return out


# ---------------------------------------------------------------------------
# 2. Codage libre, pour l'entropie et l'accord par paires vectorises
# ---------------------------------------------------------------------------

def codes_libres(matrices, colonnes):
    """Codage entier commun a toutes les matrices, colonne par colonne.

    a2.entropie et a2.accord_par_paires travaillent sur les valeurs telles quelles, apres
    normalisation en minuscules, et non sur la nomenclature de question_master employee
    par a28_commun.coder : une prediction hors nomenclature y compte comme une modalite de
    plus au lieu d'etre traitee comme une cellule vide. Pour que la version vectorisee
    reproduise a2 exactement, il faut donc un codage qui couvre l'union des valeurs vues
    dans TOUTES les matrices, colonne par colonne, et non la seule nomenclature.

    Retourne un dictionnaire nom -> matrice d'entiers de meme forme, -1 pour un manquant,
    plus le nombre maximal de modalites rencontrees.
    """
    tables = {}
    for j in colonnes:
        vus = {}
        for mat in matrices.values():
            for v in mat[:, j]:
                if est_manquant(v):
                    continue
                s = C28.norm(v)
                if s not in vus:
                    vus[s] = len(vus)
        tables[j] = vus
    k_max = max((len(t) for t in tables.values()), default=1)
    out = {}
    for nom, mat in matrices.items():
        c = np.full(mat.shape, -1, dtype=np.int32)
        for j in colonnes:
            t = tables[j]
            col = mat[:, j]
            for i in range(mat.shape[0]):
                v = col[i]
                if est_manquant(v):
                    continue
                k = t.get(C28.norm(v))
                if k is not None:
                    c[i, j] = k
        out[nom] = c
    return out, max(k_max, 1)


def entropie_accord_rapide(codes, colonnes, k_max, n_min_accord=50):
    """Entropie de Shannon en bits et accord par paires, item par item, vectorises.

    Memes definitions que a2_commun.entropie et a2_commun.accord_par_paires : entropie
    naive, sans correction de Miller Madow, et indice de Simpson SANS remise, avec le
    plancher de 50 observations sous lequel a2 n'estime pas l'accord.
    """
    sub = codes[:, colonnes]
    n, m = sub.shape
    c = np.zeros((m, k_max), dtype=np.float64)
    ii, jj = np.nonzero(sub >= 0)
    np.add.at(c, (jj, sub[ii, jj]), 1.0)
    N = c.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        p = c / np.where(N[:, None] > 0, N[:, None], 1.0)
        h = -np.where(p > 0, p * np.log2(np.maximum(p, 1e-300)), 0.0).sum(axis=1)
        h = np.where(N > 0, h, np.nan)
        den = N * (N - 1.0)
        acc = np.where((N >= n_min_accord) & (den > 0),
                       (c * (c - 1.0)).sum(axis=1) / np.where(den > 0, den, 1.0), np.nan)
    return h, acc


def diversite_rapide(h_pred, acc_pred, h_hum):
    """Diversite conservee et accord par paires, regle d'agregation de a2.

    Un item n'entre dans la somme que si les deux entropies sont definies, exactement
    comme a2_commun.profil_diversite le fait avec son test `if e_h is None or e_p is None`.
    """
    ok = ~np.isnan(h_pred) & ~np.isnan(h_hum)
    s_h = float(h_hum[ok].sum())
    s_p = float(h_pred[ok].sum())
    a = acc_pred[ok]
    a = a[~np.isnan(a)]
    return (s_p / s_h if s_h else np.nan), (float(a.mean()) if len(a) else np.nan)


# ---------------------------------------------------------------------------
# 3. Minorites, terciles de deductibilite
# ---------------------------------------------------------------------------

def deductibilite_segment(paquet, colonnes):
    """Score D_seg de a34 sur les colonnes demandees, et son masque de cellules rares.

    D_seg est la frequence de la modalite dans le segment ideologie x genre x age de la
    personne, calculee sur les humains de la vague 1 EN LAISSANT DE COTE la personne elle
    meme. Une cellule dont le segment compte moins de cinq autres repondants exploitables
    sur l'item recoit NaN. C'est le score de a34 section 0.2, importe et non redefini ;
    seules les colonnes changent.

    Les BORNES de tercile sont recalculees sur ce perimetre d'items, comme a34 le fait
    pour les siens : le rapport le declare, et le tableau des bornes est publie.
    """
    y1, x = paquet["y1"], paquet["x"]
    seg_fin, niveaux = C34.segment_fin(x, paquet["attributs"])
    ys = y1[:, colonnes]
    ok = C29.observe(ys)
    d_seg = C34.frequence_segment(ys, ys, ok, seg_fin)
    mods = modalites_minoritaires(y1, SEUIL_MINORITE)
    mods_sub = [mods[j] for j in colonnes]
    rare_vrai = C29.appartient(ys, mods_sub) & ok
    b1, b2 = C34.bornes_terciles(d_seg, rare_vrai)
    tvrai = C34.terciles(d_seg, b1, b2)
    return {"d_seg": d_seg, "rare_vrai": rare_vrai, "ok": ok, "mods": mods_sub,
            "bornes": (b1, b2), "tercile": tvrai, "n_segments": len(niveaux)}


def comptes_minorites(pred, y1, colonnes, ded):
    """Compteurs par personne pour le rappel global et le rappel du tercile T1.

    Renvoie quatre vecteurs par personne : les cellules minoritaires reelles, les raretes
    justes, et les memes deux quantites restreintes au tercile T1 non deductible. Les
    definitions de rare et de juste sont celles de a29, importees.
    """
    p = pred[:, colonnes]
    v = y1[:, colonnes]
    ok = ded["ok"]
    dispo = C29.observe(p)
    rare_vrai = ded["rare_vrai"]
    rare_pred = C29.appartient(p, ded["mods"]) & ok & dispo
    juste = rare_pred & (p == v)
    t1 = ded["tercile"] == 0
    return {
        "n_rare_vrai": rare_vrai.sum(axis=1).astype(float),
        "n_rare_pred": rare_pred.sum(axis=1).astype(float),
        "n_juste": juste.sum(axis=1).astype(float),
        "n_rare_vrai_t1": (rare_vrai & t1).sum(axis=1).astype(float),
        "n_juste_t1": (juste & t1).sum(axis=1).astype(float),
    }


def taux(num, den, idx=None):
    """Rapport de deux sommes par personne, sur un tirage bootstrap eventuel."""
    a = float(num[idx].sum()) if idx is not None else float(num.sum())
    b = float(den[idx].sum()) if idx is not None else float(den.sum())
    return a / b if b > 0 else np.nan


# ---------------------------------------------------------------------------
# 4. Bootstrap sur les personnes
# ---------------------------------------------------------------------------

def tirages(n, b, rng):
    """Indices de b tirages bootstrap de n personnes avec remise, partages par toutes
    les methodes pour que les contrastes soient apparies."""
    return rng.integers(0, n, (b, n))


def bootstrap_quantites(paquet, lignes, colonnes, codes_nom, codes_lib, seg, k_max_nom,
                        k_max_lib, idx_boot, methodes, comptes, decalage=None,
                        pas_de_trace=100):
    """Distributions bootstrap des six quantites suivies, tirages partages.

    Pour chaque tirage de personnes, toutes les quantites sont recalculees pour toutes les
    methodes sur le MEME tirage. C'est ce qui rend les contrastes apparies : la difference
    entre deux methodes ne porte plus la variance de l'echantillon de personnes, seulement
    celle de l'ecart.

    decalage, s'il est fourni, est un dictionnaire nom -> nombre de points a retrancher a
    l'exactitude par personne. Il sert a la condition appariee de a8 errata E1 et a rien
    d'autre ; il ne touche aucune autre quantite, parce qu'aucune autre quantite n'est
    publiee par le papier sous la condition appariee.
    """
    y1 = paquet["y1"]
    acc = {}
    for nom in methodes:
        a = exactitude(paquet["M"][nom], y1, lignes, colonnes)
        if decalage and nom in decalage:
            a = a - decalage[nom]
        acc[nom] = a
    ch_nom = codes_nom["_humains"][lignes]
    cm_nom = {nom: codes_nom[nom][lignes] for nom in methodes}
    ch_lib = codes_lib["_humains"][lignes]
    cm_lib = {nom: codes_lib[nom][lignes] for nom in methodes}
    sg = seg[lignes]

    cles = ["exactitude", "intra", "inter", "diversite", "accord",
            "rappel", "rappel_t1"]
    dist = {nom: {c: np.empty(len(idx_boot)) for c in cles} for nom in methodes}
    for t, idx in enumerate(idx_boot):
        h = sommes_dispersion_rapide(ch_nom[idx], sg[idx], k_max_nom, colonnes)
        hh, _ = entropie_accord_rapide(ch_lib[idx], colonnes, k_max_lib)
        for nom in methodes:
            s = sommes_dispersion_rapide(cm_nom[nom][idx], sg[idx], k_max_nom, colonnes)
            hp, ap = entropie_accord_rapide(cm_lib[nom][idx], colonnes, k_max_lib)
            div, acp = diversite_rapide(hp, ap, hh)
            c = comptes[nom]
            d = dist[nom]
            d["exactitude"][t] = np.nanmean(acc[nom][idx])
            d["intra"][t] = s["intra"] / h["intra"] if h["intra"] else np.nan
            d["inter"][t] = s["inter"] / h["inter"] if h["inter"] else np.nan
            d["diversite"][t] = div
            d["accord"][t] = acp
            d["rappel"][t] = taux(c["n_juste"], c["n_rare_vrai"], idx)
            d["rappel_t1"][t] = taux(c["n_juste_t1"], c["n_rare_vrai_t1"], idx)
        if pas_de_trace and (t + 1) % pas_de_trace == 0:
            print(f"    bootstrap {t + 1}/{len(idx_boot)}", flush=True)
    return dist


def contraste(dist, a, b, cle):
    """Difference a moins b d'une quantite, son intervalle et son p bilateral."""
    d = dist[a][cle] - dist[b][cle]
    d = d[~np.isnan(d)]
    if len(d) == 0:
        return np.nan, np.nan, np.nan, 1.0
    return (float(d.mean()), float(np.percentile(d, 2.5)),
            float(np.percentile(d, 97.5)), p_bilateral(d))


def contraste_proximite(dist, a, b, cle="intra"):
    """Difference des ECARTS ABSOLUS a 1, a moins b.

    Le ratio intra vaut 1 quand la methode laisse les gens d'un meme segment aussi
    differents qu'ils le sont vraiment. Le critere de structure n'est donc pas "plus
    haut", c'est "plus proche de 1" : une methode a 1,05 n'est pas meilleure qu'une
    methode a 0,95. Un contraste NEGATIF veut dire que a est plus proche de 1 que b.
    """
    d = np.abs(dist[a][cle] - 1.0) - np.abs(dist[b][cle] - 1.0)
    d = d[~np.isnan(d)]
    if len(d) == 0:
        return np.nan, np.nan, np.nan, 1.0
    return (float(d.mean()), float(np.percentile(d, 2.5)),
            float(np.percentile(d, 97.5)), p_bilateral(d))
