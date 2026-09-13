"""
c7_controle_generateur : un generateur synthetique BANAL, sans aucune IA, fuit-il autant
qu'un jumeau LLM ajuste sur les memes humains ?

===========================================================================
PREENREGISTREMENT : resultats/c7-controle-generateur-preenregistrement.md, ecrit le
13 septembre 2026, AVANT ce fichier et avant tout calcul.

QUESTION TRANCHEE ICI. L'article dit que les jumeaux LLM laissent fuiter l'identite des
repondants. Rien dans le protocole ne demontre que le LLM y est pour quelque chose : si un
generateur synthetique classique, ajuste sur les memes donnees et soumis a la meme attaque
sur le meme bassin, atteint le meme taux, le resultat redecouvre la fuite des donnees
synthetiques (Narayanan-Shmatikov 2008) au lieu de dire quoi que ce soit sur les LLM.

CINQ GENERATEURS, aucun appel de modele, aucun reseau, aucune bibliotheque installee :
  G0  marginales independantes (plancher)
  G1  marginales conditionnees au segment demographique (le generateur du praticien)
  G2  Chow-Liu global (dependances entre items, code ici : synthpop/copulas/sdv absents)
  G3  Chow-Liu par segment (le plus fort des comparateurs non memorisants)
  G4(eps) copie perturbee : le vrai vecteur de la personne, chaque item remplace avec
      probabilite eps par un tirage dans la marginale. L'ETALON DU HAUT, qui donne
      l'echelle de memorisation sur laquelle situer le jumeau LLM.

BASSIN STRICTEMENT IDENTIQUE a celui du jumeau LLM pour chaque generateur (le top-1 depend
mecaniquement de la taille du bassin ; ce piege a deja coute deux erreurs a ce projet) :
Twin 2 058 attaques / 2 058 candidats / 60 items ; Stanford 1 052 / 1 052 / 177 items.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                        les quinze tables de Twin, dont le segment S_gra
  c7_reidentification.items_communs         les 60 items toujours renseignes
  c7_reidentification.rangs_attaque         l'attaque de reidentification et ses garde-fous
  c7_reidentification.graine_nom            une graine stable par nom
  c7_monde_ouvert.marges_deux_regimes       la marge top1-top2 et le regime cible absente
  c7_monde_ouvert.roc_et_taux               la ROC exacte, l'AUC, le TPR aux FPR cibles
  c7_stanford.charger_domaine / coder_categoriel_commun / accord_categoriel / DEMO_CSV
                                            le chargeur du bloc GSS Stanford, inchange
  a2_commun.distance_hamming                la distance de Hamming normalisee
  a2_commun.bootstrap_personnes             l'IC a 95 % par reechantillonnage de personnes
  c7_controle_interpretabilite.controle_avant_interpretation   le controle de fidelite

CE QUI EST NOUVEAU ICI : les cinq generateurs, l'arbre de Chow-Liu (information mutuelle par
paires, arbre couvrant maximal, echantillonnage ancestral) code en une centaine de lignes, et
la lecture croisee eps*_fuite contre eps*_exactitude qui situe le jumeau LLM entre « modele
qui generalise » et « modele qui recopie ».

ETHIQUE : etude de risque de vie privee sur des jeux deja publics. Aucun pid, aucune identite,
aucun appariement individuel n'est jamais imprime ni ecrit : seuls des taux agreges sortent
dans resultats/. Aucun appel de modele de langage, aucun reseau, aucune depense. Lecture seule
sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_controle_generateur.py
===========================================================================
"""

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import minimum_spanning_tree, breadth_first_order

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                    # noqa: E402
import c7_stanford as CS                                                   # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes                # noqa: E402
from c7_reidentification import (                                          # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)
from c7_monde_ouvert import marges_deux_regimes, roc_et_taux               # noqa: E402
from c7_controle_interpretabilite import (                                 # noqa: E402
    controle_avant_interpretation, EchecControleInterpretabilite,
)

GRAINE = 20260913
N_REP = 5                 # tirages de generation par generateur stochastique (reduction declaree)
N_REP_G4 = 2              # idem, pour les 21 points de la courbe G4 (reduction declaree)
N_TIRAGES_LIENS = 5       # tirages d'ex aequo, comme c7_monde_ouvert (reduction declaree)
N_BOOTSTRAP = 2000
MIN_CELLULE_MARGINALE = 10   # sous ce seuil, G1 retombe sur la marginale globale
MIN_CELLULE_ARBRE = 30       # sous ce seuil, G3 retombe sur l'arbre global
EPS_GRILLE = [round(x, 2) for x in np.arange(0.0, 1.0001, 0.05)]

# Reference LLM de chaque jeu : la configuration dont l'article tire son chiffre.
REF_LLM = {"Twin": "JSON Persona - GPT4.1", "Stanford": "composite"}


# ---------------------------------------------------------------------------
# Briques de generation : marginales
# ---------------------------------------------------------------------------

def marginales(y, k_max):
    """Distribution empirique de chaque item sur les lignes fournies, en (n_items, k_max).

    Les manquants (-1) sont exclus du decompte ; un item entierement manquant recoit une
    distribution uniforme sur {0}, cas qui ne se produit sur aucun des deux jeux (les
    matrices d'attaque sont pleines) mais qu'il vaut mieux ne pas laisser exploser.
    """
    m = y.shape[1]
    p = np.zeros((m, k_max))
    for j in range(m):
        col = y[:, j]
        col = col[col >= 0]
        if len(col) == 0:
            p[j, 0] = 1.0
            continue
        vals, cnt = np.unique(col, return_counts=True)
        p[j, vals] = cnt / cnt.sum()
    return p


def tirer_marginales(p, n, rng):
    """n lignes tirees independamment item par item dans les distributions p."""
    m, k_max = p.shape
    out = np.zeros((n, m), dtype=np.int64)
    u = rng.random((n, m))
    for j in range(m):
        out[:, j] = np.searchsorted(np.cumsum(p[j]), u[:, j], side="right")
    return np.clip(out, 0, k_max - 1)


def groupes_hierarchiques(niveaux, min_taille, n):
    """Decoupe la population en groupes (cible, estimation) a segmentation adaptative.

    `niveaux` liste des segmentations candidates, de la plus FINE a la plus grossiere (une
    cle par personne). Chaque personne est generee dans la cellule la plus fine dont
    l'effectif atteint min_taille ; les parametres de cette cellule sont estimes sur TOUS
    ses membres, y compris ceux qui, eux, sont generes dans une cellule plus fine (sinon on
    estimerait sur les seuls « restes », ce qui n'a aucun sens statistique). Le dernier
    repli est la population entiere.

    Ce repli existe pour donner au generateur classique SA MEILLEURE CHANCE : figer une
    segmentation unique trop fine le condamnerait au repli global sur la moitie des
    personnes, ce qui ferait baisser sa fuite et arrangerait notre these.
    """
    groupes = []
    restants = np.ones(n, dtype=bool)
    for cles in niveaux:
        if not restants.any():
            break
        _, inv, cnt = np.unique(cles, return_inverse=True, return_counts=True)
        assez = restants & (cnt[inv] >= min_taille)
        for g in np.unique(inv[assez]):
            cible = np.flatnonzero(assez & (inv == g))
            estim = np.flatnonzero(inv == g)
            groupes.append((cible, estim))
        restants &= ~assez
    if restants.any():
        groupes.append((np.flatnonzero(restants), np.arange(n)))
    return groupes


def generer_G0(y, k_max, rng):
    """G0 : marginales independantes sur la population entiere."""
    return tirer_marginales(marginales(y, k_max), y.shape[0], rng)


def generer_G1(y, k_max, groupes, rng):
    """G1 : marginales estimees dans la cellule demographique de la personne."""
    out = np.zeros(y.shape, dtype=np.int64)
    for cible, estim in groupes:
        out[cible] = tirer_marginales(marginales(y[estim], k_max), len(cible), rng)
    return out


# ---------------------------------------------------------------------------
# Chow-Liu : information mutuelle par paires, arbre couvrant maximal, tirage ancestral
# ---------------------------------------------------------------------------

def _info_mutuelle(y, k_max):
    """Matrice (m, m) d'information mutuelle empirique en nats entre items categoriels.

    Calculee par contingence en une passe sur les indicatrices : pour chaque paire (j, k),
    N_jk = O_j^T O_k ou O est la matrice indicatrice (n, m * k_max). Le produit matriciel
    fait tout le travail, ce qui evite une double boucle sur m^2 paires.
    """
    n, m = y.shape
    O = np.zeros((n, m * k_max))
    lignes = np.arange(n)
    for j in range(m):
        col = y[:, j]
        ok = col >= 0
        O[lignes[ok], j * k_max + col[ok]] = 1.0
    C = O.T @ O                                     # (m*k_max, m*k_max) comptes conjoints
    marg = O.sum(axis=0)                            # comptes marginaux par (item, modalite)
    mi = np.zeros((m, m))
    for j in range(m):
        aj = slice(j * k_max, (j + 1) * k_max)
        for k in range(j + 1, m):
            ak = slice(k * k_max, (k + 1) * k_max)
            njk = C[aj, ak]
            tot = njk.sum()
            if tot <= 0:
                continue
            pjk = njk / tot
            pj = marg[aj] / max(marg[aj].sum(), 1)
            pk = marg[ak] / max(marg[ak].sum(), 1)
            att = np.outer(pj, pk)
            msk = (pjk > 0) & (att > 0)
            v = float(np.sum(pjk[msk] * np.log(pjk[msk] / att[msk])))
            mi[j, k] = mi[k, j] = max(v, 0.0)
    return mi


def ajuster_chow_liu(y, k_max, lissage=1.0):
    """Ajuste un arbre de Chow-Liu : structure (parent de chaque item) et parametres.

    Structure : arbre couvrant de poids MAXIMAL sur l'information mutuelle (obtenu comme
    arbre couvrant minimal sur -MI), enracine a l'item 0, parents donnes par un parcours en
    largeur. Parametres : marginale de la racine, et une conditionnelle P(enfant | parent)
    par arete, lissee facon Laplace (lissage = 1 par modalite) pour qu'aucune cellule vide
    du pli ne rende le tirage impossible.
    """
    n, m = y.shape
    mi = _info_mutuelle(y, k_max)
    arbre = minimum_spanning_tree(csr_matrix(-mi))
    sym = arbre + arbre.T
    ordre, predecesseurs = breadth_first_order(sym, 0, directed=False, return_predecessors=True)
    ordre = [int(v) for v in ordre]
    # Un item dont toutes les informations mutuelles sont nulles (item constant, par
    # exemple dans un petit segment) n'est relie a rien : l'arbre est alors une foret et le
    # parcours ne l'atteint pas. On le rattache a la racine, ou sa conditionnelle lissee
    # degenere vers sa propre marginale -- jamais laisse non tire en silence.
    orphelins = [j for j in range(y.shape[1]) if j not in set(ordre)]
    for j in orphelins:
        predecesseurs[j] = ordre[0]
        ordre.append(j)

    p_racine = marginales(y, k_max)[0]
    cond = {}
    for enfant in ordre[1:]:
        parent = int(predecesseurs[enfant])
        tab = np.full((k_max, k_max), lissage)
        yp, ye = y[:, parent], y[:, enfant]
        ok = (yp >= 0) & (ye >= 0)
        np.add.at(tab, (yp[ok], ye[ok]), 1.0)
        cond[int(enfant)] = tab / tab.sum(axis=1, keepdims=True)
    return {"ordre": ordre, "parent": predecesseurs, "racine": p_racine,
            "cond": cond, "k_max": k_max, "m": m}


def tirer_chow_liu(modele, n, rng):
    """n lignes tirees du modele par echantillonnage ancestral, vectorise par arete."""
    m, k_max = modele["m"], modele["k_max"]
    out = np.zeros((n, m), dtype=np.int64)
    cum_r = np.cumsum(modele["racine"])
    out[:, modele["ordre"][0]] = np.clip(
        np.searchsorted(cum_r, rng.random(n), side="right"), 0, k_max - 1)
    for enfant in modele["ordre"][1:]:
        parent = int(modele["parent"][enfant])
        cum = np.cumsum(modele["cond"][enfant], axis=1)          # (k_max, k_max)
        u = rng.random(n)
        vp = out[:, parent]
        out[:, enfant] = np.clip(
            (cum[vp] < u[:, None]).sum(axis=1), 0, k_max - 1)
    return out


def generer_G2(y, k_max, modele_glob, rng):
    """G2 : Chow-Liu ajuste sur la population entiere."""
    return tirer_chow_liu(modele_glob, y.shape[0], rng)


def generer_G3(y, modeles, rng):
    """G3 : Chow-Liu ajuste dans la cellule demographique de la personne.

    `modeles` est la liste (cible, modele) produite une fois pour toutes : reajuster un
    arbre a chaque tirage couterait 5 fois le meme calcul pour le meme resultat.
    """
    out = np.zeros(y.shape, dtype=np.int64)
    for cible, mod in modeles:
        out[cible] = tirer_chow_liu(mod, len(cible), rng)
    return out


def generer_G4(y, p_glob, eps, rng):
    """G4(eps) : le vrai vecteur de chaque personne, chaque item remplace independamment
    avec probabilite eps par un tirage dans la marginale globale de cet item.

    eps = 0 est la copie litterale (memorisation totale), eps = 1 redonne G0 en esperance.
    Ce generateur n'est pas propose comme methode : c'est l'etalon du haut, la seule facon
    de donner une echelle de memorisation sur laquelle situer le jumeau LLM.
    """
    n = y.shape[0]
    bruit = tirer_marginales(p_glob, n, rng)
    masque = rng.random(y.shape) < eps
    return np.where(masque, bruit, y)


# ---------------------------------------------------------------------------
# Mesures : exactitude, attaque en monde ferme, attaque en monde ouvert
# ---------------------------------------------------------------------------

def exactitude_personne(gen, pool):
    """Part des items de l'attaque correctement retrouves, une valeur par personne."""
    valide = pool >= 0
    juste = (gen == pool) & valide
    nb = valide.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(nb > 0, juste.sum(axis=1) / np.maximum(nb, 1), np.nan)


def mesurer(nom, gens, pool, accord_fn):
    """Rejoue l'attaque sur chaque tirage de generation, moyenne PAR PERSONNE avant le
    bootstrap (le bootstrap reste un reechantillonnage de personnes, jamais de tirages)."""
    n = pool.shape[0]
    vrai = np.arange(n)
    t1s, t10s, rgs, accs = [], [], [], []
    ouv = []
    for r, gen in enumerate(gens):
        rng = np.random.default_rng([GRAINE, graine_nom(nom), 500, r])
        rang, top1, top10 = rangs_attaque(gen, pool, vrai, rng, n_tirages=N_TIRAGES_LIENS)
        t1s.append(top1)
        t10s.append(top10)
        rgs.append(rang)
        accs.append(exactitude_personne(gen, pool))

        rng_o = np.random.default_rng([GRAINE, graine_nom(nom), 600, r])
        accord = accord_fn(gen, pool)
        mp, corr, mr = marges_deux_regimes(accord, vrai, rng_o)
        ouv.append(roc_et_taux(mp, corr, mr, n))

    top1_m = np.mean(t1s, axis=0)
    top10_m = np.mean(t10s, axis=0)
    acc_m = np.nanmean(accs, axis=0)
    m1, b1, h1 = bootstrap_personnes(top1_m, N_BOOTSTRAP, [GRAINE, 700, graine_nom(nom)])
    m10, b10, h10 = bootstrap_personnes(top10_m, N_BOOTSTRAP, [GRAINE, 701, graine_nom(nom)])
    ma, ba, ha = bootstrap_personnes(acc_m, N_BOOTSTRAP, [GRAINE, 702, graine_nom(nom)])
    return {
        "generateur": nom, "n": n, "n_pool": n, "n_rep": len(gens),
        "exactitude": ma, "exactitude_bas": ba, "exactitude_haut": ha,
        "top1": m1, "top1_bas": b1, "top1_haut": h1,
        "top10": m10, "top10_bas": b10, "top10_haut": h10,
        "rang_median": float(np.median(np.mean(rgs, axis=0))),
        "top1_hasard": 1.0 / n,
        "auc_ouvert": float(np.mean([o["auc"] for o in ouv])),
        "tpr_fpr_0_1pct": float(np.mean([o["tpr_fpr_0_1pct"] for o in ouv])),
        "tpr_fpr_1pct": float(np.mean([o["tpr_fpr_1pct"] for o in ouv])),
    }


def accord_hamming(gen, pool):
    return 1.0 - distance_hamming(gen, pool)


# ---------------------------------------------------------------------------
# Lecture de l'echelle de memorisation
# ---------------------------------------------------------------------------

def eps_etoile(df_eps, colonne, valeur):
    """La valeur de eps ou la courbe G4 croise `valeur`, par interpolation lineaire sur la
    grille mesuree. La courbe est decroissante en eps : on interpole sur l'axe retourne.
    Renvoie NaN (et la raison) si la valeur cible sort de l'intervalle mesure -- jamais
    d'extrapolation, le depot en a deja paye le prix sur c7_echelle.
    """
    x = df_eps["eps"].to_numpy(dtype=float)
    y = df_eps[colonne].to_numpy(dtype=float)
    ordre = np.argsort(y)
    ys, xs = y[ordre], x[ordre]
    if valeur > ys.max():
        return float("nan"), "au-dessus de G4(eps=0), hors grille"
    if valeur < ys.min():
        return float("nan"), "en dessous de G4(eps=1), hors grille"
    return float(np.interp(valeur, ys, xs)), "interpole dans la grille mesuree"


def verdict_specificite(m_top1, m_ic, l_top1, l_ic):
    """La regle preenregistree, section 5 du preenregistrement, appliquee telle quelle."""
    chevauchent = not (m_ic[1] < l_ic[0])
    if m_top1 >= 0.5 * l_top1 or chevauchent:
        return "NON SPECIFIQUE AUX LLM"
    if m_top1 >= 0.2 * l_top1:
        return "AFFAIBLI (effet LLM reel mais bien plus petit qu'annonce)"
    return "SPECIFIQUE AUX LLM"


# ---------------------------------------------------------------------------
# Blocs de donnees
# ---------------------------------------------------------------------------

def bloc_twin():
    """Twin-2K-500 : 2 058 personnes, les 60 items toujours renseignes, segment S_gra."""
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    return {"jeu": "Twin", "pool": codes[REF_V4][:, items], "k_max": paq["k_max"],
            "niveaux": [paq["seg"]["S_gra"].astype(str)],
            "niveaux_nom": "S_gra (40 segments)",
            "items_globaux": items, "llm": codes[REF_LLM["Twin"]][:, items],
            "llm_nom": REF_LLM["Twin"], "plafond": codes[REF_V13][:, items],
            "accord": accord_hamming, "paq": paq}


def bloc_stanford():
    """Park et al. / GSS : 1 052 personnes, 177 items categoriels, demographies de
    `demographic_summary.csv`. La hierarchie de segmentation va du plus fin
    (genre x race x age x education) au plus grossier (age seul)."""
    ordre, items, tables, _ = CS.charger_domaine("gss")
    codes = CS.coder_categoriel_commun(tables, items)
    pool = codes[CS.VAGUE1]
    demo = pd.read_csv(CS.DEMO_CSV).set_index("email").loc[ordre]
    col = {c: demo[c].astype(str).to_numpy() for c in ("gender", "race", "age", "education")}
    niveaux = [
        col["gender"] + "|" + col["race"] + "|" + col["age"] + "|" + col["education"],
        col["gender"] + "|" + col["race"] + "|" + col["age"],
        col["gender"] + "|" + col["age"],
        col["age"],
    ]
    return {"jeu": "Stanford", "pool": pool, "k_max": int(pool.max()) + 1,
            "niveaux": niveaux,
            "niveaux_nom": "genre x race x age x education, replis successifs",
            "items_globaux": None, "llm": codes[REF_LLM["Stanford"]],
            "llm_nom": "agent composite (Park et al.)",
            "plafond": codes[CS.VAGUE2], "accord": CS.accord_categoriel, "paq": None}


def traiter(bloc):
    jeu, pool, k_max = bloc["jeu"], bloc["pool"], bloc["k_max"]
    acc_fn = bloc["accord"]
    n, m = pool.shape

    g_marg = groupes_hierarchiques(bloc["niveaux"], MIN_CELLULE_MARGINALE, n)
    g_arbre = groupes_hierarchiques(bloc["niveaux"], MIN_CELLULE_ARBRE, n)
    print(f"\n=== {jeu} : {n} personnes, {m} items ; segmentation "
          f"{bloc['niveaux_nom']} -> {len(g_marg)} cellules >= {MIN_CELLULE_MARGINALE} "
          f"(G1), {len(g_arbre)} cellules >= {MIN_CELLULE_ARBRE} (G3) ===", flush=True)

    p_glob = marginales(pool, k_max)
    t0 = time.time()
    modele_glob = ajuster_chow_liu(pool, k_max)
    modeles_seg = [(cible, ajuster_chow_liu(pool[estim], k_max)) for cible, estim in g_arbre]
    print(f"Chow-Liu ajuste ({time.time() - t0:.0f}s) : 1 arbre global, "
          f"{len(modeles_seg)} arbres de cellule", flush=True)

    fabriques = {
        "G0 marginales independantes": lambda r: generer_G0(pool, k_max, r),
        "G1 marginales par segment": lambda r: generer_G1(pool, k_max, g_marg, r),
        "G2 Chow-Liu global": lambda r: generer_G2(pool, k_max, modele_glob, r),
        "G3 Chow-Liu par segment": lambda r: generer_G3(pool, modeles_seg, r),
    }

    lignes = []
    gens_par_nom = {}
    for nom, fab in fabriques.items():
        t0 = time.time()
        gens = [fab(np.random.default_rng([GRAINE, graine_nom(nom), 900, r]))
                for r in range(N_REP)]
        gens_par_nom[nom] = gens
        l = mesurer(nom, gens, pool, acc_fn)
        l["jeu"] = jeu
        lignes.append(l)
        print(f"{nom:32s} exactitude={l['exactitude']:.4f} top1={l['top1']*100:6.3f} % "
              f"[{l['top1_bas']*100:.3f};{l['top1_haut']*100:.3f}] "
              f"TPR@1%={l['tpr_fpr_1pct']*100:.3f} % ({time.time() - t0:.0f}s)", flush=True)

    # Reference LLM et plafond humain, MEME bassin, MEME attaque, MEMES graines.
    for nom, x in ((f"LLM : {bloc['llm_nom']}", bloc["llm"]),
                   ("Plafond humain (retest)", bloc["plafond"])):
        l = mesurer(nom, [x], pool, acc_fn)
        l["jeu"] = jeu
        lignes.append(l)
        print(f"{nom:32s} exactitude={l['exactitude']:.4f} top1={l['top1']*100:6.3f} % "
              f"[{l['top1_bas']*100:.3f};{l['top1_haut']*100:.3f}] "
              f"TPR@1%={l['tpr_fpr_1pct']*100:.3f} %", flush=True)

    # G4 : l'echelle de memorisation.
    print(f"--- {jeu} : echelle de memorisation G4(eps) ---", flush=True)
    lignes_eps = []
    for eps in EPS_GRILLE:
        nom = f"G4 copie perturbee eps={eps:.2f}"
        n_rep = 1 if eps == 0.0 else N_REP_G4   # eps=0 est deterministe
        gens = [generer_G4(pool, p_glob, eps,
                           np.random.default_rng([GRAINE, 950, int(eps * 100), r]))
                for r in range(n_rep)]
        l = mesurer(nom, gens, pool, acc_fn)
        l["jeu"] = jeu
        l["eps"] = eps
        lignes_eps.append(l)
        print(f"  eps={eps:4.2f}  exactitude={l['exactitude']:.4f}  "
              f"top1={l['top1']*100:6.2f} %  TPR@1%={l['tpr_fpr_1pct']*100:6.2f} %",
              flush=True)

    # Controle de fidelite prealable, applique AVANT toute interpretation.
    controles = []
    if jeu == "Twin":
        idx_pers = np.arange(n)
        cibles = {nom: gens[0] for nom, gens in gens_par_nom.items()}
        cibles[f"LLM : {bloc['llm_nom']}"] = bloc["llm"]
        for nom, mat in cibles.items():
            try:
                d = controle_avant_interpretation(idx_pers, bloc["items_globaux"], mat,
                                                   nom, paq=bloc["paq"])
                controles.append({"jeu": jeu, "candidat": nom, "passe": True,
                                  "top1": d["candidat_top1"],
                                  "baseline_top1": d["baseline_top1"]})
                print(f"controle fidelite : {nom} PASSE "
                      f"(top1={d['candidat_top1']*100:.2f} % vs baseline "
                      f"{d['baseline_top1']*100:.2f} %)", flush=True)
            except EchecControleInterpretabilite as e:
                d = getattr(e, "diagnostic", {})
                controles.append({"jeu": jeu, "candidat": nom, "passe": False,
                                  "top1": d.get("candidat_top1", np.nan),
                                  "baseline_top1": d.get("baseline_top1", np.nan)})
                print(f"controle fidelite : {nom} ECHOUE -- aucune information "
                      f"individuelle demontrable sur ce bassin "
                      f"(top1={d.get('candidat_top1', float('nan'))*100:.2f} % vs baseline "
                      f"{d.get('baseline_top1', float('nan'))*100:.2f} %)", flush=True)

    return pd.DataFrame(lignes), pd.DataFrame(lignes_eps), pd.DataFrame(controles)


def rendre_verdict(df, df_eps, jeu, llm_nom):
    """La regle preenregistree, sections 5 et 6, appliquee sans marge de manoeuvre."""
    d = df[df.jeu == jeu].set_index("generateur")
    ref = f"LLM : {llm_nom}"
    l = d.loc[ref]
    classiques = d.loc[[i for i in d.index if i.startswith(("G0", "G1", "G2", "G3"))]]
    meilleur = classiques.top1.idxmax()
    m = classiques.loc[meilleur]

    v_ferme = verdict_specificite(m.top1, (m.top1_bas, m.top1_haut),
                                  l.top1, (l.top1_bas, l.top1_haut))
    meilleur_o = classiques.tpr_fpr_1pct.idxmax()
    mo = classiques.loc[meilleur_o]
    v_ouvert = verdict_specificite(mo.tpr_fpr_1pct, (mo.tpr_fpr_1pct, mo.tpr_fpr_1pct),
                                   l.tpr_fpr_1pct, (l.tpr_fpr_1pct, l.tpr_fpr_1pct))

    e = df_eps[df_eps.jeu == jeu]
    eps_f, note_f = eps_etoile(e, "top1", l.top1)
    eps_a, note_a = eps_etoile(e, "exactitude", l.exactitude)
    if np.isnan(eps_f) or np.isnan(eps_a):
        lecture = "hors grille, non concluant"
    elif eps_f > eps_a + 0.10:
        lecture = "GENERALISE : fuit MOINS qu'un copieur de meme exactitude"
    elif eps_f < eps_a - 0.10:
        lecture = "RECOPIE ET PLUS : fuit PLUS qu'un copieur de meme exactitude"
    else:
        lecture = "SE COMPORTE COMME UN COPIEUR : fuite = ce qu'implique son exactitude"

    print(f"\n----- VERDICT {jeu} -----", flush=True)
    print(f"meilleur generateur classique non memorisant : {meilleur} "
          f"top1={m.top1*100:.3f} % [{m.top1_bas*100:.3f};{m.top1_haut*100:.3f}]", flush=True)
    print(f"jumeau LLM : top1={l.top1*100:.3f} % "
          f"[{l.top1_bas*100:.3f};{l.top1_haut*100:.3f}]", flush=True)
    print(f"seuil preenregistre de non-specificite : M >= {0.5*l.top1*100:.3f} %", flush=True)
    print(f"monde ferme  : {v_ferme}", flush=True)
    print(f"monde ouvert : {v_ouvert} (meilleur classique {meilleur_o} "
          f"TPR@1%={mo.tpr_fpr_1pct*100:.3f} % vs LLM {l.tpr_fpr_1pct*100:.3f} %)", flush=True)
    print(f"echelle de memorisation : eps*_fuite={eps_f:.3f} ({note_f}) ; "
          f"eps*_exactitude={eps_a:.3f} ({note_a}) -> {lecture}", flush=True)

    return {"jeu": jeu, "llm": ref, "llm_top1": l.top1, "llm_top1_bas": l.top1_bas,
            "llm_top1_haut": l.top1_haut, "llm_tpr_1pct": l.tpr_fpr_1pct,
            "llm_exactitude": l.exactitude,
            "meilleur_classique": meilleur, "meilleur_classique_top1": m.top1,
            "meilleur_classique_top1_bas": m.top1_bas,
            "meilleur_classique_top1_haut": m.top1_haut,
            "meilleur_classique_ouvert": meilleur_o,
            "meilleur_classique_tpr_1pct": mo.tpr_fpr_1pct,
            "seuil_non_specifique_top1": 0.5 * l.top1,
            "verdict_monde_ferme": v_ferme, "verdict_monde_ouvert": v_ouvert,
            "eps_etoile_fuite": eps_f, "eps_etoile_exactitude": eps_a,
            "lecture_memorisation": lecture}


CHEMIN_CSV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "resultats", "c7-controle-generateur.csv")


def main(jeux=("Twin", "Stanford")):
    """Un jeu par invocation si besoin : les lignes du jeu recalcule remplacent les
    anciennes dans le CSV unique, celles de l'autre jeu sont conservees telles quelles.
    Cela permet de tenir la contrainte « tout en avant-plan » sans lancer une seule
    commande d'une heure, sans rien changer aux resultats."""
    print(__doc__.split("=" * 75)[1], flush=True)
    t_total = time.time()

    morceaux = []
    for bloc_fn in (bloc_twin, bloc_stanford):
        bloc = bloc_fn.__name__.replace("bloc_", "")
        if bloc.capitalize() not in [j.capitalize() for j in jeux]:
            continue
        b = bloc_fn()
        df, df_eps, df_ctl = traiter(b)
        v = rendre_verdict(df, df_eps, b["jeu"], b["llm_nom"])
        morceaux.append(df.assign(table="generateurs"))
        morceaux.append(df_eps.assign(table="echelle_memorisation"))
        if len(df_ctl):
            morceaux.append(df_ctl.assign(table="controle_fidelite"))
        morceaux.append(pd.DataFrame([v]).assign(table="verdict"))

    sortie = pd.concat(morceaux, ignore_index=True)
    if os.path.exists(CHEMIN_CSV):
        ancien = pd.read_csv(CHEMIN_CSV)
        garde = ancien[~ancien["jeu"].isin(sortie["jeu"].unique())]
        sortie = pd.concat([garde, sortie], ignore_index=True)
    T1.ecrire(sortie, "c7-controle-generateur.csv")
    print(f"\nTOTAL {time.time() - t_total:.0f}s", flush=True)


if __name__ == "__main__":
    main(tuple(sys.argv[1:]) or ("Twin", "Stanford"))
