"""
a7 : premier prototype du transport de variance a somme constante.

Statut : script d'analyse, pas du code de production. Il existe pour qu'un tiers puisse
rejouer chaque chiffre de resultats/a7-transport-de-variance.md en une commande.

QUESTION POSEE
--------------
a1 a mesure une double distorsion : les agents gonflent les ecarts ENTRE segments
(ratio inter 1,75 a 5,9) et ecrasent la dispersion A L'INTERIEUR des segments (ratio
intra 0,64 a 0,89). Le correctif ne peut donc pas etre une dilatation de la variance :
il doit en DEPLACER de l'inter vers l'intra en gardant la marge globale constante.
Ce script prototype ce transport en post traitement pur, sans aucun appel de modele.

L'OPERATEUR
-----------
Pour chaque item j et chaque segment s, la distribution des reponses de l'agent est
retrecie vers la distribution poolee de l'agent sur le meme item :

    p'(r | s) = lambda * p(r | s) + (1 - lambda) * p(r)

Comme p(r) est exactement la moyenne ponderee des p(r|s) par les effectifs de segment,
la marge poolee est INVARIANTE par construction : sum_s w_s p'(r|s) = p(r). H(R) est
donc conserve exactement, I(R;S) diminue et H(R|S) augmente d'autant. C'est la propriete
"a somme constante" ; elle est verifiee numeriquement et imprimee.

QUI CHANGE DE REPONSE, C'EST LA QUE LE CORRECTIF SE JOUE
-------------------------------------------------------
Retrecir la distribution ne dit pas quels individus changent. Deux variantes :

  naive    : parmi les individus du segment qui portent une modalite excedentaire, on
             tire au hasard ceux qui basculent vers une modalite deficitaire. C'est le
             TEMOIN. Il doit degrader la fidelite individuelle.
  informee : on bascule en priorite les individus dont le profil de reponses sur les
             AUTRES items rend la nouvelle modalite plus plausible. La plausibilite vient
             d'un modele de plus proches voisins HUMAINS, du meme type que la baseline B2
             de a2, entraine uniquement sur des personnes hors du pli de l'individu. Le
             transport devient un appariement individuel et non un tirage.

PROTOCOLE DE VALIDATION
-----------------------
  - lambda est calibre sur des items de calibration et applique a des items d'evaluation
    disjoints. Validation croisee a 5 blocs d'items : chaque item est evalue une fois
    et une seule, avec un lambda choisi sans lui.
  - les voisins humains sont cherches en validation croisee a 5 plis sur les personnes ;
    aucune reponse d'une personne du pli de test n'entre dans son propre score.
  - la verite humaine de l'item evalue n'entre jamais dans la construction du correctif.

ENTREES
-------
  data/osf-t6g7k-stanford/figure2/data/new_analysis_summaries/gss_filtered/preparation/
  data/osf-t6g7k-stanford/figure2/data/question_master/gss/
  data/osf-t6g7k-stanford/figure3/data/demographic_summary.csv

SORTIES, toutes dans resultats/
-------------------------------
  a7-figure-transport.png et .svg   trajectoire de chaque condition dans le plan
                                    (ratio inter, ratio intra) quand lambda varie
  a7-trajectoires.csv               le balayage complet de lambda, par condition,
                                    variante, axe de transport et mesure
  a7-avant-apres.csv                le tableau avant / apres au lambda calibre,
                                    avec intervalles bootstrap
  a7-par-axe.csv                    effet du transport sur les six axes, y compris
                                    ceux sur lesquels on n'a pas corrige
  a7-critere-a6.csv                 le test de la variance utile : qui change, et le
                                    changement rapproche t il de la vraie reponse
  a7-lambda-calibre.csv             lambda retenu par bloc d'items et par condition
  a7-dilatation-temoin.csv          le temoin a un seul bouton : dilatation pure vers
                                    ratio intra = 1, sans contrainte de somme

Estimateurs : STRICTEMENT ceux de analyses/a1_double_distorsion.py (entropie corrigee
Miller Madow, Gini Simpson sans biais, bootstrap recentre) et de analyses/a2_commun.py
(profil_diversite, exactitude_par_personne, bootstrap_personnes, distance de Hamming).
Aucun n'est modifie ; ils sont importes.

Aucun appel de modele de langage. Quatre coeurs au plus.
Usage : .venv/bin/python analyses/a7_transport_variance.py [--rapide]
"""

import os

# Un llama-server tourne sur la machine pour un autre agent : on se limite a 4 coeurs.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import argparse
import csv
import sys
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import spearmanr

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "analyses"))

# --- estimateurs de a1, importes tels quels, jamais modifies ----------------
from a1_double_distorsion import (AXES, agreger, compter, construire_index, decomposer,
                                  lire_condition, lire_demographies, lire_nomenclature,
                                  matrice_distance)
# --- estimateurs de a2, importes tels quels, jamais modifies ---------------
from a2_commun import (bootstrap_personnes, distance_hamming, exactitude_par_personne,
                       profil_diversite)
# --- la liste d'exclusion d'items de a2, recopiee de Stanford --------------
from a2_baselines_gss import EXCLUS_STANFORD, FUITE_DEMOGRAPHIQUE

PREP = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                            "new_analysis_summaries/gss_filtered/preparation")
SORTIE_DEFAUT = os.path.join(RACINE, "resultats")

# Conditions retenues, cf. l'enonce de la mission. Les deux vagues humaines sont la
# reference et le controle ; elles ne sont jamais transportees.
HUMAIN_REF = "humains vague 1"
HUMAIN_CTRL = "humains vague 2"
FICHIERS = {
    HUMAIN_REF: "p_wave1_summary.csv",
    HUMAIN_CTRL: "p_wave2_summary.csv",
    "agents composite": "composite_agents_summary.csv",
    "agents enquete": "survey_agents_summary.csv",
    "agents entretien (v3)": "gss_v3_summary.csv",
    "agents demographiques (v8)": "gss_v8_summary.csv",
}
AGENTS = ["agents composite", "agents enquete", "agents entretien (v3)",
          "agents demographiques (v8)"]

# L'axe qui porte le gonflement, cf. a1 section 4, et le profil croise qui approche ce
# qu'un agent demographique recoit dans son invite.
AXES_TRANSPORT = ["political_ideology", "profil croise"]

LAMBDAS = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
N_BLOCS = 5        # blocs d'items : calibration de lambda sans l'item evalue
N_PLIS = 5         # plis sur les personnes : voisins humains hors pli
K_VOISINS = 30     # meme k que la baseline B2 de a2
N_MIN_CELLULE = 20  # sous cet effectif un couple (item, segment) n'est pas transporte
GRAINE = 20260907

# Plancher a battre, recopie de resultats/a2-baselines.md section 4 : la baseline B2,
# plus proches voisins humains sur les items de contexte, vote majoritaire, k = 30,
# obtient 0,6717 d'exactitude sur exactement ces 149 items et ces 1052 personnes. Toute
# exactitude d'agent qui passe sous cette ligne est battue par du scikit-learn.
B2_A2 = 0.6717


# ===========================================================================
# 1. Chargement, avec les lecteurs de a1
# ===========================================================================

def charger(racine):
    options, ordinal = lire_nomenclature(racine)
    entetes = next(csv.reader(open(os.path.join(PREP, "p_wave1_summary.csv"),
                                   encoding="utf-8")))[1:]
    n_items = len(entetes)
    donnees, ids_ref, taux_nc = {}, None, {}
    for libelle, fichier in FICHIERS.items():
        x, ids, nc = lire_condition(os.path.join(PREP, fichier), entetes, options)
        if ids_ref is None:
            ids_ref = ids
        elif ids != ids_ref:
            sys.exit(f"Identifiants desalignes dans {fichier}.")
        donnees[libelle], taux_nc[libelle] = x, nc
    seg, niveaux = lire_demographies(racine, ids_ref)
    return options, ordinal, entetes, n_items, donnees, taux_nc, ids_ref, seg, niveaux


def en_objets(x):
    """Codes entiers vers tableau objet, -1 devenant None.

    profil_diversite et exactitude_par_personne de a2_commun testent les manquants avec
    est_manquant, qui ne connait pas la convention -1 de a1. Sans cette conversion, -1
    serait compte comme une modalite a part entiere et gonflerait la diversite.
    """
    o = x.astype(object)
    o[x < 0] = None
    return o


def masque_items(entetes):
    """Les 149 items de a2, et non les 169 de a1. Justification dans le rapport.

    C'est la liste d'exclusion de Stanford elle meme, recopiee dans a2_baselines_gss
    depuis figure2/code/source/new_analysis/analyze_gss_filtered.py, plus polviews.
    Elle est un sur ensemble strict des huit items ecartes par a1. Elle retire tout
    item qui redit une information deja donnee a l'agent dans son invite. Un transport
    qui retrecirait p(r|s) sur un item comme polviews, dont la reponse EST l'etiquette
    de segment, detruirait mecaniquement l'exactitude sans rien mesurer d'interessant.
    """
    return np.array([(q.lower() not in EXCLUS_STANFORD) and (q not in FUITE_DEMOGRAPHIQUE)
                     for q in entetes])


# ===========================================================================
# 2. L'operateur de transport
# ===========================================================================

def quota_plus_grand_reste(p, n):
    """Repartit n unites selon les proportions p, methode du plus grand reste.

    Garantit que la somme des effectifs cibles vaut exactement n, ce qui est ce qui
    rend le transport conservatif : personne n'est cree ni detruit.
    """
    brut = p * n
    base = np.floor(brut).astype(np.int64)
    reste = n - base.sum()
    if reste > 0:
        ordre = np.argsort(-(brut - base))
        base[ordre[:reste]] += 1
    return base


def transporter(x, seg_axe, lam, items, k_par_item, scores=None, rng=None,
                journal=None, vers="pool"):
    """Applique le retrecissement p'(r|s) = lam p(r|s) + (1-lam) q(r), puis reassigne.

    vers="pool"     : q(r) est la marge poolee de l'agent. C'est le TRANSPORT a somme
                      constante : la marge est invariante, la variance change de place.
    vers="uniforme" : q(r) est la loi uniforme sur les modalites reellement employees
                      par l'agent pour cet item. C'est la DILATATION PURE, le temoin a
                      un seul bouton : elle augmente aussi H(R|S), mais elle augmente
                      en meme temps H(R), donc elle CREE de la dispersion au lieu d'en
                      deplacer. C'est l'analogue mesurable de ce que revendique LifeMem
                      (arXiv 2608.19621), qui publie un ecart intra groupe reduit de 22
                      pour cent sans jamais republier le terme inter apres correction.

    x        : matrice (personnes, items) de codes entiers, -1 si non codable.
    seg_axe  : vecteur (personnes,) d'entiers de segment, -1 si manquant.
    lam      : soit un flottant, soit un vecteur (items,) de lambda par item.
    items    : indices des items a transporter.
    scores   : None pour la variante naive. Sinon tableau (personnes, items, K) de
               log plausibilite de chaque modalite pour chaque personne, servant a
               choisir QUI bascule. Variante informee.
    journal  : liste optionnelle ou l'on empile (personne, item, ancien, nouveau).

    Retourne une copie transportee de x.
    """
    out = x.copy()
    lam_vec = np.full(x.shape[1], float(lam)) if np.isscalar(lam) else np.asarray(lam)
    segments = [g for g in np.unique(seg_axe) if g >= 0]
    for j in items:
        k = int(k_par_item[j])
        col = x[:, j]
        valide_global = (col >= 0) & (seg_axe >= 0)
        n_tot = int(valide_global.sum())
        if n_tot < 2 * N_MIN_CELLULE:
            continue
        # distribution poolee : moyenne ponderee exacte des distributions de segment,
        # ce qui garantit l'invariance de la marge.
        p_pool = np.bincount(col[valide_global].astype(np.int64),
                             minlength=k).astype(np.float64) / n_tot
        if vers == "uniforme":
            support = p_pool > 0
            cible_globale = support.astype(np.float64) / support.sum()
        else:
            cible_globale = p_pool
        lam_j = lam_vec[j]
        for g in segments:
            sel = np.where(valide_global & (seg_axe == g))[0]
            n_s = sel.size
            if n_s < N_MIN_CELLULE:
                continue
            obs = np.bincount(col[sel].astype(np.int64), minlength=k).astype(np.int64)
            p_s = obs / n_s
            cible_p = lam_j * p_s + (1.0 - lam_j) * cible_globale
            cible_p = cible_p / cible_p.sum()
            cible = quota_plus_grand_reste(cible_p, n_s)
            delta = cible - obs
            if not np.any(delta):
                continue
            sources = [r for r in range(k) if delta[r] < 0]
            cibles = [r for r in range(k) if delta[r] > 0]
            if not sources or not cibles:
                continue
            quota_sortie = {r: int(-delta[r]) for r in sources}
            places = {r: int(delta[r]) for r in cibles}

            candidats = np.array([i for i in sel if int(col[i]) in quota_sortie],
                                 dtype=np.int64)
            if candidats.size == 0:
                continue
            if scores is None:
                # TEMOIN : tirage au hasard dans le segment.
                candidats = candidats.copy()
                rng.shuffle(candidats)
                fentes = np.array([r for r in cibles for _ in range(places[r])],
                                  dtype=np.int64)
                rng.shuffle(fentes)
                deja = set()
                f = 0
                for i in candidats:
                    i = int(i)
                    if f >= len(fentes):
                        break
                    r_src = int(col[i])
                    if quota_sortie[r_src] <= 0 or i in deja:
                        continue
                    r_dst = int(fentes[f])
                    f += 1
                    quota_sortie[r_src] -= 1
                    deja.add(i)
                    out[i, j] = r_dst
                    if journal is not None:
                        journal.append((i, j, r_src, r_dst))
            else:
                # INFORMEE : appariement glouton sur le gain de plausibilite.
                sc = scores[:, j, :k]
                paires = []
                for i in candidats:
                    i = int(i)
                    r_src = int(col[i])
                    base = float(sc[i, r_src])
                    for r_dst in cibles:
                        paires.append((float(sc[i, r_dst]) - base, i, r_src, r_dst))
                paires.sort(key=lambda t: -t[0])
                deja = set()
                for gain, i, r_src, r_dst in paires:
                    if i in deja or quota_sortie[r_src] <= 0 or places[r_dst] <= 0:
                        continue
                    quota_sortie[r_src] -= 1
                    places[r_dst] -= 1
                    deja.add(i)
                    out[i, j] = r_dst
                    if journal is not None:
                        journal.append((i, j, r_src, r_dst))
    return out


# ===========================================================================
# 3. Plausibilite individuelle : plus proches voisins humains, hors pli
# ===========================================================================

def scores_voisins(x_agent, x_humain, items, k_par_item, k_max, plis, blocs,
                   k=K_VOISINS):
    """log plausibilite de chaque modalite pour chaque personne et chaque item.

    Pour la personne i et l'item j, on cherche les k personnes du pli d'ENTRAINEMENT
    dont les reponses HUMAINES sur les items de contexte ressemblent le plus aux
    reponses de l'AGENT de i sur ces memes items, puis on lit leur distribution de
    reponses humaines sur j. Aucune verite sur la personne i n'est employee, ni sur
    l'item j ni ailleurs : seul le profil produit par l'agent sert de requete. C'est
    exactement l'information dont dispose un praticien qui a un echantillon humain de
    calibration, hypothese identique a celle de la baseline B2 de a2.

    Le contexte exclut le bloc d'items auquel appartient j, jamais moins.
    """
    n = x_agent.shape[0]
    ens_items = set(int(j) for j in items)
    scores = np.zeros((n, x_agent.shape[1], k_max), dtype=np.float32)
    for bloc in blocs:
        ens_bloc = set(int(j) for j in bloc)
        contexte = np.array([j for j in items if int(j) not in ens_bloc])
        for tr, te in plis:
            d = distance_hamming(x_agent[np.ix_(te, contexte)],
                                 x_humain[np.ix_(tr, contexte)])
            k_eff = min(k, d.shape[1])
            ordre = np.argpartition(d, k_eff - 1, axis=1)[:, :k_eff]
            for j in bloc:
                if int(j) not in ens_items:
                    continue
                kj = int(k_par_item[j])
                col = x_humain[tr, j]
                for pos, i in enumerate(te):
                    v = col[ordre[pos]]
                    v = v[v >= 0]
                    c = np.bincount(v, minlength=kj).astype(np.float64) if v.size else \
                        np.zeros(kj)
                    # lissage de Laplace : une modalite jamais vue chez les voisins
                    # reste possible, avec une plausibilite faible et non nulle.
                    p = (c + 1.0) / (c.sum() + kj)
                    scores[i, j, :kj] = np.log(p)
    return scores


# ===========================================================================
# 4. Mesure : les deux ratios, avec les estimateurs de a1
# ===========================================================================

class Mesureur:
    """Enveloppe autour de construire_index / compter / decomposer / agreger de a1."""

    def __init__(self, seg, niveaux, n_items, k_max, garder, est_ordinal,
                 valeurs_ordinales):
        self.seg, self.niveaux, self.n_items = seg, niveaux, n_items
        self.k_max = k_max
        self.g_max = int(max(len(niveaux[a]) for a in AXES))
        self.garder, self.est_ordinal = garder, est_ordinal
        self.valeurs_ordinales = valeurs_ordinales
        self.n_axes = len(AXES)
        self._cache = {}

    def index(self, x, cache=True):
        # On garde une reference sur x dans le cache : sans elle, un tableau libere
        # rendrait son id() reutilisable et le cache renverrait un index d'un autre
        # tableau. Bug silencieux, et il fausserait tous les chiffres. Le cache n'est
        # employe que pour les matrices persistantes, sinon il ferait des centaines de
        # megaoctets pendant le balayage de lambda.
        if not cache:
            return construire_index(x, self.seg, self.k_max, self.g_max, self.n_items)
        cle = id(x)
        if cle not in self._cache:
            idx, poubelle = construire_index(x, self.seg, self.k_max, self.g_max,
                                             self.n_items)
            self._cache[cle] = (idx, poubelle, x)
        idx, poubelle, _ = self._cache[cle]
        return idx, poubelle

    def decomposition(self, x, lignes=None, cache=True):
        idx, poubelle = self.index(x, cache)
        if lignes is None:
            lignes = np.arange(x.shape[0])
        cnt = compter(idx, lignes, poubelle, self.n_items, self.g_max, self.k_max,
                      self.n_axes)
        return decomposer(cnt, self.valeurs_ordinales)

    def termes(self, x, axes_gardes=None, lignes=None, cache=True):
        dec = self.decomposition(x, lignes, cache)
        return agreger(dec, self.garder, self.est_ordinal, axes_gardes=axes_gardes)


def recentrer(tirages, cible):
    """Bootstrap recentre, exactement la regle de a1 : le tirage donne la forme de la
    distribution d'echantillonnage, pas son centre."""
    v = np.asarray(tirages, dtype=float)
    fini = np.isfinite(v)
    if fini.sum() < 20:
        return v
    return v - np.mean(v[fini]) + cible


def ic95(v):
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    if v.size < 20:
        return float("nan"), float("nan")
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


# ===========================================================================
# 5. Programme principal
# ===========================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=os.path.join(RACINE, "data/osf-t6g7k-stanford"))
    ap.add_argument("--sortie", default=SORTIE_DEFAUT)
    ap.add_argument("--bootstrap", type=int, default=400)
    ap.add_argument("--graine", type=int, default=GRAINE)
    ap.add_argument("--rapide", action="store_true")
    args = ap.parse_args()
    if args.rapide:
        args.bootstrap = 60
    t0 = time.time()
    os.makedirs(args.sortie, exist_ok=True)
    rng = np.random.default_rng(args.graine)

    options, ordinal, entetes, n_items, donnees, taux_nc, ids, seg, niveaux = \
        charger(args.racine)
    n = len(ids)
    garder = masque_items(entetes)
    items = np.where(garder)[0]
    est_ordinal = np.array([ordinal.get(q, False) for q in entetes])
    k_par_item = np.array([len(options[q]) for q in entetes])
    k_max = int(k_par_item.max())
    valeurs_ordinales = np.zeros((n_items, k_max))
    for j, q in enumerate(entetes):
        if est_ordinal[j] and k_par_item[j] > 1:
            valeurs_ordinales[j, :k_par_item[j]] = np.arange(k_par_item[j]) / \
                (k_par_item[j] - 1)

    print("=" * 94)
    print("a7 : TRANSPORT DE VARIANCE A SOMME CONSTANTE, prototype en post traitement")
    print("=" * 94)
    print(f"{n} participants, {n_items} items lus, {len(items)} items retenus "
          f"(liste d'exclusion de Stanford + polviews, soit le jeu de 149 items de a2)")
    print(f"{int((est_ordinal & garder).sum())} items ordinaux parmi les retenus")
    print("Axes de transport : " + ", ".join(AXES_TRANSPORT))
    print("Taux de cellules non codables : " +
          ", ".join(f"{c} {taux_nc[c] * 100:.2f}%" for c in donnees))

    mes = Mesureur(seg, niveaux, n_items, k_max, garder, est_ordinal, valeurs_ordinales)

    # --- decoupages -------------------------------------------------------
    ordre = np.random.default_rng(args.graine).permutation(items)
    blocs = np.array_split(ordre, N_BLOCS)
    idx_pers = np.arange(n)
    perm = np.random.default_rng(args.graine + 1).permutation(idx_pers)
    parts = np.array_split(perm, N_PLIS)
    plis = [(np.sort(np.concatenate([parts[q] for q in range(N_PLIS) if q != p])),
             np.sort(parts[p])) for p in range(N_PLIS)]

    # --- reference et controle -------------------------------------------
    ref_axe = {a: mes.termes(donnees[HUMAIN_REF], axes_gardes=[AXES.index(a)])
               for a in AXES}
    ref_tot = mes.termes(donnees[HUMAIN_REF])

    def ratios(x, axe=None, cache=True):
        """(ratio inter, ratio intra) pour chaque mesure, contre les humains vague 1."""
        if axe is None:
            t, base = mes.termes(x, cache=cache), ref_tot
        else:
            t = mes.termes(x, axes_gardes=[AXES.index(axe)], cache=cache)
            base = ref_axe[axe]
        return {m: (t[m][0] / base[m][0], t[m][1] / base[m][1]) for m in t}

    print("\n--- point de depart, sur les 149 items, avant tout transport ---")
    print(f"{'condition':<28}{'axe':<20}{'inter M1':>10}{'intra M1':>10}"
          f"{'inter M2':>10}{'intra M2':>10}")
    avant = {}
    for c in [HUMAIN_CTRL] + AGENTS:
        for a in AXES_TRANSPORT + ["_tous_axes"]:
            r = ratios(donnees[c], None if a == "_tous_axes" else a)
            avant[(c, a)] = r
            print(f"{c:<28}{a:<20}{r['entropie'][0]:>10.3f}{r['entropie'][1]:>10.3f}"
                  f"{r['gini_simpson'][0]:>10.3f}{r['gini_simpson'][1]:>10.3f}")

    # --- verification de l'invariance de la marge -------------------------
    # Le transport doit laisser H(R) inchange item par item. On le verifie sur une
    # condition et un lambda arbitraires : c'est la propriete "a somme constante".
    x_test = transporter(donnees["agents composite"], seg["political_ideology"], 0.5,
                         items, k_par_item, scores=None,
                         rng=np.random.default_rng(1))
    t_av = mes.termes(donnees["agents composite"])
    t_ap = mes.termes(x_test)
    print("\nInvariance de la marge globale (inter + intra), lambda = 0,5, "
          "axe ideologie, variante naive")
    for m in t_av:
        s_av, s_ap = sum(t_av[m]), sum(t_ap[m])
        print(f"  {m:<20} avant {s_av:9.4f}   apres {s_ap:9.4f}   "
              f"ecart {100 * (s_ap - s_av) / s_av:+6.3f} %")

    # --- scores de plausibilite, une fois par condition -------------------
    print("\nCalcul des scores de plausibilite (voisins humains hors pli)...")
    scores = {}
    for c in AGENTS:
        scores[c] = scores_voisins(donnees[c], donnees[HUMAIN_REF], items, k_par_item,
                                   k_max, plis, blocs)
        print(f"  {c} fait, {time.time() - t0:.0f} s")

    # ==================================================================
    # 6. Balayage de lambda : les trajectoires
    # ==================================================================
    print("\n" + "=" * 94)
    print("BALAYAGE DE LAMBDA : trajectoire de chaque condition dans le plan "
          "(inter, intra)")
    print("=" * 94)
    verite = donnees[HUMAIN_REF]
    verite_obj = en_objets(verite[:, items])
    masque_ev = np.zeros_like(verite, dtype=bool)
    masque_ev[:, items] = verite[:, items] >= 0
    exact_ref = {c: exactitude_par_personne(donnees[c], verite, masque_ev)
                 for c in AGENTS}

    # POINT DE METHODE, il vaut d'etre dit : les deux variantes produisent EXACTEMENT
    # les memes effectifs par couple (item, segment), puisque la cible est la meme. Elles
    # ne different que par le CHOIX des individus qui basculent. Les deux ratios sont
    # donc rigoureusement identiques d'une variante a l'autre, et seule la fidelite
    # individuelle les separe. C'est verifie numeriquement ci dessous, puis les ratios
    # ne sont calcules qu'une fois pour les deux.
    lignes_traj = [["condition", "axe_transport", "variante", "lambda", "mesure",
                    "ratio_inter", "ratio_intra", "exactitude", "diversite_conservee",
                    "accord_paires", "part_changee"]]
    traj = {}
    verif_faite = False
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            for lam in LAMBDAS:
                x_par_var = {}
                for variante in ["naive", "informee"]:
                    x_par_var[variante] = transporter(
                        donnees[c], seg[axe], lam, items, k_par_item,
                        scores=None if variante == "naive" else scores[c],
                        rng=np.random.default_rng(args.graine + 7))
                rr = ratios(x_par_var["naive"], axe, cache=False)
                if not verif_faite and lam == 0.5:
                    rr2 = ratios(x_par_var["informee"], axe, cache=False)
                    ecart = max(abs(rr[m][i] - rr2[m][i]) for m in rr for i in (0, 1))
                    print(f"\n  Verification : ecart maximal entre les ratios des deux "
                          f"variantes = {ecart:.2e} (doit etre nul)")
                    verif_faite = True
                for variante in ["naive", "informee"]:
                    xt = x_par_var[variante]
                    ex = float(np.nanmean(exactitude_par_personne(xt, verite,
                                                                  masque_ev)))
                    pd_ = profil_diversite(en_objets(xt[:, items]), verite_obj)
                    chg = float(np.mean((xt[:, items] != donnees[c][:, items])
                                        & (donnees[c][:, items] >= 0)))
                    traj[(c, axe, variante, lam)] = (rr, ex, pd_, chg)
                    for m in rr:
                        lignes_traj.append([c, axe, variante, f"{lam:.1f}", m,
                                            f"{rr[m][0]:.4f}", f"{rr[m][1]:.4f}",
                                            f"{ex:.4f}",
                                            f"{pd_['part_diversite_humaine']:.4f}",
                                            f"{pd_['accord_par_paires']:.4f}",
                                            f"{chg:.4f}"])
            print(f"  {c} / {axe} : balaye, {time.time() - t0:.0f} s")

    with open(os.path.join(args.sortie, "a7-trajectoires.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_traj)

    for axe in AXES_TRANSPORT:
        print(f"\n--- axe {axe}, mesure entropie, variante informee ---")
        print(f"{'condition':<28}" + "".join(f"{l:>16.1f}" for l in LAMBDAS))
        for c in AGENTS:
            print(f"{c + ' inter':<28}" +
                  "".join(f"{traj[(c, axe, 'informee', l)][0]['entropie'][0]:>16.3f}"
                          for l in LAMBDAS))
            print(f"{c + ' intra':<28}" +
                  "".join(f"{traj[(c, axe, 'informee', l)][0]['entropie'][1]:>16.3f}"
                          for l in LAMBDAS))
            print(f"{c + ' exact.':<28}" +
                  "".join(f"{traj[(c, axe, 'informee', l)][1]:>16.4f}"
                          for l in LAMBDAS))

    # --- le plafond du transport ------------------------------------------
    # A lambda = 0 tout ecart entre segments est supprime : c'est le maximum de variance
    # que l'operateur peut deplacer vers l'intra. Si ce plafond reste sous 1, aucun
    # reglage de lambda ne peut amener les deux ratios en (1, 1), et c'est une limite de
    # l'operateur, pas un defaut de calibration.
    print("\n" + "=" * 94)
    print("PLAFOND DU TRANSPORT : ratio intra atteint quand lambda = 0, soit quand tout")
    print("ecart entre segments est supprime. C'est le maximum deplacable.")
    print("=" * 94)
    print(f"{'condition':<28}{'axe':<20}{'intra avant':>13}{'intra plafond':>15}"
          f"{'intra vise':>12}{'exactitude plafond':>20}")
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            av_ = traj[(c, axe, "informee", 1.0)]
            pl_ = traj[(c, axe, "informee", 0.0)]
            print(f"{c:<28}{axe:<20}{av_[0]['entropie'][1]:>13.3f}"
                  f"{pl_[0]['entropie'][1]:>15.3f}{1.0:>12.3f}{pl_[1]:>20.4f}")

    # ==================================================================
    # 7. Calibration de lambda hors des items evalues
    # ==================================================================
    print("\n" + "=" * 94)
    print("CALIBRATION DE LAMBDA : choisi sur 4 blocs d'items, applique au 5e")
    print("Critere : ratio inter le plus proche de 1 sur les items de calibration,")
    print("entropie, axe de transport. La verite de l'item evalue n'entre jamais.")
    print("=" * 94)

    dec_humain = mes.decomposition(donnees[HUMAIN_REF])

    def ratios_items(x, axe, sous_items, dec=None):
        """(inter, intra, total) restreints a un sous ensemble d'items, mesure entropie.

        Le troisieme terme, le total H(R), est celui que la mission impose de rapporter
        systematiquement : c'est lui qui distingue un TRANSPORT, ou il ne bouge pas,
        d'une DILATATION, ou il augmente.
        """
        g = np.zeros(n_items, dtype=bool)
        g[sous_items] = True
        a_i = AXES.index(axe)
        d_x = dec if dec is not None else mes.decomposition(x, cache=False)
        num = agreger(d_x, g, est_ordinal, axes_gardes=[a_i])["entropie"]
        den = agreger(dec_humain, g, est_ordinal, axes_gardes=[a_i])["entropie"]
        return (num[0] / den[0], num[1] / den[1],
                (num[0] + num[1]) / (den[0] + den[1]))

    def ratio_inter_items(x, axe, sous_items, dec=None):
        return ratios_items(x, axe, sous_items, dec)[0]

    lignes_lam = [["condition", "axe_transport", "bloc", "lambda_retenu",
                   "ratio_inter_calibration_avant", "ratio_inter_calibration_apres"]]
    lam_par_item = {}
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            vec = np.ones(n_items)
            for b, bloc in enumerate(blocs):
                calib = np.array([j for j in items if j not in set(bloc.tolist())])
                avant_cal = ratio_inter_items(donnees[c], axe, calib,
                                              dec=mes.decomposition(donnees[c]))
                meilleur, meilleur_ecart, apres_cal = 1.0, float("inf"), avant_cal
                for lam in LAMBDAS:
                    xt = transporter(donnees[c], seg[axe], lam, calib, k_par_item,
                                     scores=None,
                                     rng=np.random.default_rng(args.graine + 11))
                    r = ratio_inter_items(xt, axe, calib)
                    if abs(r - 1.0) < meilleur_ecart:
                        meilleur, meilleur_ecart, apres_cal = lam, abs(r - 1.0), r
                vec[bloc] = meilleur
                lignes_lam.append([c, axe, str(b), f"{meilleur:.1f}",
                                   f"{avant_cal:.4f}", f"{apres_cal:.4f}"])
                print(f"  {c:<28}{axe:<20}bloc {b} : lambda = {meilleur:.1f}  "
                      f"(inter calib {avant_cal:.3f} -> {apres_cal:.3f})")
            lam_par_item[(c, axe)] = vec
    with open(os.path.join(args.sortie, "a7-lambda-calibre.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_lam)

    # ==================================================================
    # 7 bis. TEMOIN : la dilatation pure, correctif a un seul bouton
    # ==================================================================
    # Pourquoi ce temoin. LifeMem (Wang et al., arXiv 2608.19621, 20 aout 2026) corrige
    # explicitement l'identity essentialism et publie un ecart intra groupe reduit de 22
    # pour cent et une KL reduite de 30 pour cent, mais ne republie JAMAIS le terme inter
    # apres correction et ne formule aucune contrainte de somme constante [CONFIRME, cf.
    # resultats/a10-verification-sources.md section 3.a]. On ne peut donc pas savoir, en
    # lisant ce papier, s'il a deplace de la variance ou s'il en a cree. Ici on fabrique
    # l'analogue mesurable de ce que revendique un tel correctif : on augmente la
    # dispersion intra segment jusqu'a ratio intra = 1, en retrecissant vers la loi
    # UNIFORME et non vers la marge poolee, et on regarde ce qu'il advient du terme inter
    # et du total H(R). Ce que LifeMem ne publie pas, nous le mesurons sur notre temoin.
    print("\n" + "=" * 94)
    print("TEMOIN, DILATATION PURE : on vise ratio intra = 1 sans contrainte de somme")
    print("Retrecissement vers la loi uniforme. mu calibre par bloc d'items, comme lambda.")
    print("=" * 94)
    lignes_dil = [["condition", "axe", "mu_median", "ratio_inter_avant",
                   "ratio_inter_apres", "ratio_intra_avant", "ratio_intra_apres",
                   "ratio_total_avant", "ratio_total_apres", "exactitude_avant",
                   "exactitude_apres", "delta_exactitude", "delta_ic_bas",
                   "delta_ic_haut", "part_changee", "n_change", "n_reparation",
                   "n_casse"]]
    print(f"{'condition':<26}{'axe':<19}{'mu':>5}{'inter av':>10}{'inter ap':>10}"
          f"{'intra av':>10}{'intra ap':>10}{'total av':>10}{'total ap':>10}"
          f"{'exact ap':>10}{'net rep':>9}")
    transportes, journaux, mu_median = {}, {}, {}
    for c in AGENTS:
        dec_c = mes.decomposition(donnees[c])
        for axe in AXES_TRANSPORT:
            vec_mu = np.ones(n_items)
            for bloc in blocs:
                calib = np.array([j for j in items if j not in set(bloc.tolist())])
                meilleur, ecart = 1.0, float("inf")
                for mu in LAMBDAS:
                    xd = transporter(donnees[c], seg[axe], mu, calib, k_par_item,
                                     scores=None,
                                     rng=np.random.default_rng(args.graine + 19),
                                     vers="uniforme")
                    r = ratios_items(xd, axe, calib)[1]
                    if abs(r - 1.0) < ecart:
                        meilleur, ecart = mu, abs(r - 1.0)
                vec_mu[bloc] = meilleur
            jr = []
            xd = transporter(donnees[c], seg[axe], vec_mu, items, k_par_item,
                             scores=scores[c],
                             rng=np.random.default_rng(args.graine + 19),
                             journal=jr, vers="uniforme")
            transportes[(c, axe, "dilatation")] = xd
            journaux[(c, axe, "dilatation")] = jr
            av = ratios_items(donnees[c], axe, items, dec=dec_c)
            ap = ratios_items(xd, axe, items)
            ex_ap = exactitude_par_personne(xd, verite, masque_ev)
            e_av = float(np.nanmean(exact_ref[c]))
            e_ap = float(np.nanmean(ex_ap))
            d_m, d_b, d_h_ = bootstrap_personnes(ex_ap - exact_ref[c], n_tirages=2000,
                                                 graine=args.graine)
            chg = float(np.mean((xd[:, items] != donnees[c][:, items])
                                & (donnees[c][:, items] >= 0)))
            rep = sum(1 for (i, j, s_, d_) in jr
                      if verite[i, j] >= 0 and d_ == verite[i, j] and s_ != verite[i, j])
            cas = sum(1 for (i, j, s_, d_) in jr
                      if verite[i, j] >= 0 and s_ == verite[i, j] and d_ != verite[i, j])
            mu_med = float(np.median(vec_mu[items]))
            mu_median[(c, axe)] = mu_med
            lignes_dil.append([c, axe, f"{mu_med:.1f}", f"{av[0]:.4f}", f"{ap[0]:.4f}",
                               f"{av[1]:.4f}", f"{ap[1]:.4f}", f"{av[2]:.4f}",
                               f"{ap[2]:.4f}", f"{e_av:.4f}", f"{e_ap:.4f}",
                               f"{d_m:.4f}", f"{d_b:.4f}", f"{d_h_:.4f}", f"{chg:.4f}",
                               str(len(jr)), str(rep), str(cas)])
            print(f"{c:<26}{axe:<19}{mu_med:>5.1f}{av[0]:>10.3f}{ap[0]:>10.3f}"
                  f"{av[1]:>10.3f}{ap[1]:>10.3f}{av[2]:>10.3f}{ap[2]:>10.3f}"
                  f"{e_ap:>10.4f}{rep - cas:>9}")
    with open(os.path.join(args.sortie, "a7-dilatation-temoin.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_dil)

    # ==================================================================
    # 8. Application du lambda calibre, avant / apres avec bootstrap
    # ==================================================================
    print("\n" + "=" * 94)
    print("AVANT / APRES au lambda calibre, intervalles bootstrap sur les personnes")
    print("=" * 94)

    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            for variante in ["naive", "informee"]:
                jr = []
                xt = transporter(donnees[c], seg[axe], lam_par_item[(c, axe)], items,
                                 k_par_item,
                                 scores=None if variante == "naive" else scores[c],
                                 rng=np.random.default_rng(args.graine + 13),
                                 journal=jr)
                transportes[(c, axe, variante)] = xt
                journaux[(c, axe, variante)] = jr

    # bootstrap : meme tirage de personnes pour toutes les conditions, comme a1.
    print(f"\nBootstrap : {args.bootstrap} tirages avec remise sur les {n} participants.")
    cles = [(HUMAIN_CTRL, None, None)] + \
           [(c, None, None) for c in AGENTS] + list(transportes.keys())
    mat = {(HUMAIN_CTRL, None, None): donnees[HUMAIN_CTRL]}
    mat.update({(c, None, None): donnees[c] for c in AGENTS})
    mat.update(transportes)

    axes_eval = AXES_TRANSPORT + ["_tous_axes"]
    brut = {(k, a, m): ([], []) for k in cles for a in axes_eval
            for m in ["entropie", "gini_simpson"]}
    brut_ref = {(a, m): ([], []) for a in axes_eval
                for m in ["entropie", "gini_simpson"]}
    rng_b = np.random.default_rng(args.graine + 17)
    for b in range(args.bootstrap):
        lignes = rng_b.integers(0, n, size=n)
        for a in axes_eval:
            ag = None if a == "_tous_axes" else [AXES.index(a)]
            t = agreger(mes.decomposition(donnees[HUMAIN_REF], lignes), garder,
                        est_ordinal, axes_gardes=ag)
            for m in ["entropie", "gini_simpson"]:
                brut_ref[(a, m)][0].append(t[m][0])
                brut_ref[(a, m)][1].append(t[m][1])
        for k in cles:
            d = mes.decomposition(mat[k], lignes)
            for a in axes_eval:
                ag = None if a == "_tous_axes" else [AXES.index(a)]
                t = agreger(d, garder, est_ordinal, axes_gardes=ag)
                for m in ["entropie", "gini_simpson"]:
                    brut[(k, a, m)][0].append(t[m][0])
                    brut[(k, a, m)][1].append(t[m][1])
        if (b + 1) % max(1, args.bootstrap // 8) == 0:
            print(f"  {b + 1}/{args.bootstrap}  ({time.time() - t0:.0f} s)", flush=True)

    point = {}
    for k in cles:
        for a in axes_eval:
            ag = None if a == "_tous_axes" else [AXES.index(a)]
            point[(k, a)] = mes.termes(mat[k], axes_gardes=ag)
    point_ref = {a: (ref_tot if a == "_tous_axes" else ref_axe[a]) for a in axes_eval}

    lignes_ap = [["condition", "axe_transport", "variante", "axe_mesure", "mesure",
                  "ratio_inter", "inter_ic_bas", "inter_ic_haut",
                  "ratio_intra", "intra_ic_bas", "intra_ic_haut",
                  "ratio_global", "exactitude", "exact_ic_bas", "exact_ic_haut",
                  "delta_exactitude", "delta_ic_bas", "delta_ic_haut",
                  "diversite_conservee", "accord_paires", "part_changee"]]
    print(f"\n{'condition':<26}{'transport':<17}{'variante':<10}"
          f"{'inter':>22}{'intra':>20}{'exactitude':>23}"
          f"{'ecart apparie':>25}{'divers.':>8}{'accord':>8}")
    for k in cles:
        c, axe, variante = k
        x = mat[k]
        ex = exactitude_par_personne(x, verite, masque_ev)
        e_m, e_b, e_h = bootstrap_personnes(ex, n_tirages=2000, graine=args.graine)
        # Test APPARIE de la perte d'exactitude : on bootstrappe le vecteur des ecarts
        # personne par personne, et non les deux exactitudes separement. Deux
        # intervalles qui se chevauchent ne prouvent rien ; l'intervalle de l'ecart, si.
        if axe:
            d_m, d_b, d_h_ = bootstrap_personnes(ex - exact_ref[c], n_tirages=2000,
                                                 graine=args.graine)
        else:
            d_m = d_b = d_h_ = 0.0
        pd_ = profil_diversite(en_objets(x[:, items]), verite_obj)
        base_c = donnees[c]
        chg = float(np.mean((x[:, items] != base_c[:, items]) & (base_c[:, items] >= 0))) \
            if axe else 0.0
        for a in axes_eval:
            for m in ["entropie", "gini_simpson"]:
                pi = point[(k, a)][m][0] / point_ref[a][m][0]
                pa = point[(k, a)][m][1] / point_ref[a][m][1]
                bi = recentrer(np.array(brut[(k, a, m)][0]) /
                               np.array(brut_ref[(a, m)][0]), pi)
                ba = recentrer(np.array(brut[(k, a, m)][1]) /
                               np.array(brut_ref[(a, m)][1]), pa)
                i1, i2 = ic95(bi)
                a1_, a2_ = ic95(ba)
                glob = (point[(k, a)][m][0] + point[(k, a)][m][1]) / \
                       (point_ref[a][m][0] + point_ref[a][m][1])
                lignes_ap.append([c, axe or "aucun", variante or "aucune", a, m,
                                  f"{pi:.4f}", f"{i1:.4f}", f"{i2:.4f}",
                                  f"{pa:.4f}", f"{a1_:.4f}", f"{a2_:.4f}",
                                  f"{glob:.4f}", f"{e_m:.4f}", f"{e_b:.4f}",
                                  f"{e_h:.4f}", f"{d_m:.4f}", f"{d_b:.4f}",
                                  f"{d_h_:.4f}",
                                  f"{pd_['part_diversite_humaine']:.4f}",
                                  f"{pd_['accord_par_paires']:.4f}", f"{chg:.4f}"])
                if a == (axe or AXES_TRANSPORT[0]) and m == "entropie":
                    print(f"{c:<26}{(axe or 'aucun'):<17}{(variante or 'aucune'):<10}"
                          f"{pi:>8.3f} [{i1:5.3f};{i2:5.3f}]"
                          f"{pa:>8.3f} [{a1_:5.3f};{a2_:5.3f}]"
                          f"{e_m:>9.4f} [{e_b:5.4f};{e_h:5.4f}]"
                          f"{d_m:>9.4f} [{d_b:+6.4f};{d_h_:+6.4f}]"
                          f"{pd_['part_diversite_humaine']:>8.3f}"
                          f"{pd_['accord_par_paires']:>8.3f}")
    with open(os.path.join(args.sortie, "a7-avant-apres.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_ap)

    # ==================================================================
    # 9. Effet sur les autres axes
    # ==================================================================
    print("\n" + "=" * 94)
    print("EFFET SUR LES SIX AXES quand on ne corrige que sur un seul")
    print("=" * 94)
    lignes_axe = [["condition", "axe_transport", "variante", "axe_mesure",
                   "ratio_inter_avant", "ratio_inter_apres",
                   "ratio_intra_avant", "ratio_intra_apres"]]
    print(f"{'condition':<24}{'transport':<16}{'variante':<10}" +
          "".join(f"{a[:11]:>13}" for a in AXES))
    for c in AGENTS:
        av = {a: ratios(donnees[c], a)["entropie"] for a in AXES}
        print(f"{c:<24}{'avant':<16}{'-':<10}" +
              "".join(f"{av[a][0]:>13.2f}" for a in AXES))
        for axe in AXES_TRANSPORT:
            for variante in ["naive", "informee", "dilatation"]:
                x = transportes[(c, axe, variante)]
                ap = {a: ratios(x, a)["entropie"] for a in AXES}
                print(f"{'':<24}{axe:<16}{variante:<10}" +
                      "".join(f"{ap[a][0]:>13.2f}" for a in AXES))
                for a in AXES:
                    lignes_axe.append([c, axe, variante, a, f"{av[a][0]:.4f}",
                                       f"{ap[a][0]:.4f}", f"{av[a][1]:.4f}",
                                       f"{ap[a][1]:.4f}"])
    with open(os.path.join(args.sortie, "a7-par-axe.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_axe)

    # ==================================================================
    # 10. Critere A6 : le gain de variance intra est il informatif ?
    # ==================================================================
    print("\n" + "=" * 94)
    print("CRITERE A6 : qui change, et le changement rapproche t il de la vraie reponse")
    print("=" * 94)
    print("reparation = l'agent avait faux et la nouvelle reponse est juste.")
    print("casse      = l'agent avait juste et la nouvelle reponse est fausse.")
    print("La vague 2 sert de controle : meme personne, deux semaines plus tard.")

    v1, v2 = donnees[HUMAIN_REF], donnees[HUMAIN_CTRL]
    lignes_a6 = [["condition", "axe_transport", "variante", "verite", "n_change",
                  "n_reparation", "n_casse", "net", "taux_reparation_parmi_changes",
                  "taux_uniforme_1_sur_K", "spearman_paires_avant", "spearman_paires_apres",
                  "corr_item_change_erreur", "corr_personne_change_erreur"]]
    print(f"\n{'condition':<24}{'transport':<16}{'variante':<10}{'verite':<8}"
          f"{'change':>8}{'repare':>8}{'casse':>8}{'net':>8}"
          f"{'tx rep':>9}{'tx unif':>9}")
    d_h = matrice_distance(v1, garder)
    iu = np.triu_indices(n, 1)
    d_h_v = d_h[iu]
    for c in AGENTS:
        d_av = matrice_distance(donnees[c], garder)
        rho_av = float(spearmanr(d_h_v, d_av[iu])[0])
        err_item = np.array([np.mean(donnees[c][:, j][v1[:, j] >= 0] !=
                                     v1[:, j][v1[:, j] >= 0]) for j in items])
        err_pers = 1.0 - exact_ref[c]
        for axe in AXES_TRANSPORT:
            for variante in ["naive", "informee", "dilatation"]:
                x = transportes[(c, axe, variante)]
                jr = journaux[(c, axe, variante)]
                d_ap = matrice_distance(x, garder)
                rho_ap = float(spearmanr(d_h_v, d_ap[iu])[0])
                chg_item = np.array([np.mean(x[:, j] != donnees[c][:, j]) for j in items])
                chg_pers = np.array([np.mean(x[i, items] != donnees[c][i, items])
                                     for i in range(n)])
                ci = float(spearmanr(chg_item, err_item)[0])
                cp = float(spearmanr(chg_pers, err_pers, nan_policy="omit")[0])
                for nom_v, vv in (("vague1", v1), ("vague2", v2)):
                    rep = cas = tot = 0
                    base = 0.0
                    for (i, j, r_src, r_dst) in jr:
                        t = vv[i, j]
                        if t < 0:
                            continue
                        tot += 1
                        av_ok, ap_ok = (r_src == t), (r_dst == t)
                        if ap_ok and not av_ok:
                            rep += 1
                        elif av_ok and not ap_ok:
                            cas += 1
                        base += 1.0 / max(int(k_par_item[j]), 1)
                    tx = rep / tot if tot else float("nan")
                    txb = base / tot if tot else float("nan")
                    lignes_a6.append([c, axe, variante, nom_v, str(tot), str(rep),
                                      str(cas), str(rep - cas), f"{tx:.4f}",
                                      f"{txb:.4f}", f"{rho_av:.4f}", f"{rho_ap:.4f}",
                                      f"{ci:.4f}", f"{cp:.4f}"])
                    print(f"{c:<24}{axe:<16}{variante:<10}{nom_v:<8}"
                          f"{tot:>8}{rep:>8}{cas:>8}{rep - cas:>8}"
                          f"{tx:>9.3f}{txb:>9.3f}")
                print(f"{'':<24}{'':<16}{'':<10}{'T2 :':<8}"
                      f"spearman distances paires humaines : avant {rho_av:.4f}  "
                      f"apres {rho_ap:.4f}   |   correlation changement/erreur : "
                      f"item {ci:+.3f}, personne {cp:+.3f}")
    with open(os.path.join(args.sortie, "a7-critere-a6.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_a6)

    # ==================================================================
    # 11. Figure
    # ==================================================================
    reperes = {(c, axe): float(np.median(lam_par_item[(c, axe)][items]))
               for c in AGENTS for axe in AXES_TRANSPORT}
    dilat = {}
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            xd = transportes[(c, axe, "dilatation")]
            rr = ratios(xd, axe)["entropie"]
            ed = float(np.nanmean(exactitude_par_personne(xd, verite, masque_ev)))
            dilat[(c, axe)] = (rr[0], rr[1], ed, mu_median[(c, axe)])
    plancher = {"humains v2": float(np.nanmean(
        exactitude_par_personne(donnees[HUMAIN_CTRL], verite, masque_ev))),
        "B2": B2_A2}
    tracer(traj, avant, args.sortie, reperes, dilat, plancher)
    print(f"\nTermine en {time.time() - t0:.0f} s. Fichiers dans {args.sortie}/")


def tracer(traj, avant, sortie, reperes, dilat, plancher):
    """Deux etages.

    En haut, la trajectoire de chaque condition dans le plan (ratio inter, ratio intra)
    quand lambda varie, l'exactitude individuelle en couleur. Les deux variantes,
    naive et informee, sont RIGOUREUSEMENT confondues dans ce plan, puisqu'elles
    realisent les memes effectifs par segment : une seule trajectoire est donc tracee,
    et c'est en soi le message de la figure. Le point du temoin de dilatation pure est
    ajoute pour montrer ou mene un correctif a un seul bouton.

    En bas, ce que le plan ne peut pas montrer : l'exactitude individuelle en fonction
    de lambda, variante par variante, avec le plancher B2 de a2 et le plafond humain.

    L'axe des abscisses est en echelle symetrique et non logarithmique : a lambda = 0 le
    terme inter estime devient legerement negatif, residu de la correction de Miller
    Madow, et une echelle logarithmique le ferait disparaitre sans le dire.
    """
    fig, axs = plt.subplots(2, 2, figsize=(14.5, 11.0),
                            gridspec_kw={"height_ratios": [1.35, 1.0]})
    couleurs = plt.get_cmap("viridis")
    marques = ["o", "s", "^", "D"]
    exacts = [traj[(c, a, v, l)][1] for c in AGENTS for a in AXES_TRANSPORT
              for v in ("naive", "informee") for l in LAMBDAS]
    vmin, vmax = min(exacts), max(exacts)

    for col, axe in enumerate(AXES_TRANSPORT):
        ax = axs[0][col]
        for ic_, c in enumerate(AGENTS):
            xs = [traj[(c, axe, "informee", l)][0]["entropie"][0] for l in LAMBDAS]
            ys = [traj[(c, axe, "informee", l)][0]["entropie"][1] for l in LAMBDAS]
            cs = [traj[(c, axe, "informee", l)][1] for l in LAMBDAS]
            ax.plot(xs, ys, "-", color="0.55", lw=1.1, zorder=1)
            ax.scatter(xs, ys, c=cs, cmap=couleurs, vmin=vmin, vmax=vmax,
                       marker=marques[ic_], s=62, edgecolors="k", linewidths=0.5,
                       zorder=3)
            for l, xx, yy in zip(LAMBDAS, xs, ys):
                if l == 1.0:
                    ax.annotate("lambda=1", (xx, yy), fontsize=7,
                                xytext=(7, -3), textcoords="offset points",
                                color="0.25")
            lam_r = reperes[(c, axe)]
            k_r = min(range(len(LAMBDAS)), key=lambda q: abs(LAMBDAS[q] - lam_r))
            ax.scatter([xs[k_r]], [ys[k_r]], s=230, facecolors="none",
                       edgecolors="crimson", linewidths=1.6, zorder=4)
            di = dilat[(c, axe)]
            ax.scatter([di[0]], [di[1]], marker=marques[ic_], s=70, c=[di[2]],
                       cmap=couleurs, vmin=vmin, vmax=vmax, edgecolors="darkorange",
                       linewidths=1.8, zorder=5)
        ax.axhline(1.0, color="0.75", lw=0.8)
        ax.axvline(1.0, color="0.75", lw=0.8)
        ax.plot([1], [1], marker="*", ms=20, color="crimson", zorder=6)
        ax.annotate("humains vague 1 (cible)", (1, 1), fontsize=8.5,
                    xytext=(-10, -18), textcoords="offset points", color="crimson",
                    ha="right")
        hc = avant[("humains vague 2", axe)]["entropie"]
        ax.plot([hc[0]], [hc[1]], marker="P", ms=11, color="crimson", zorder=6)
        ax.annotate("vague 2 (controle)", (hc[0], hc[1]), fontsize=8,
                    xytext=(10, 4), textcoords="offset points", color="crimson")
        ax.set_xscale("symlog", linthresh=0.2, linscale=0.6)
        ax.set_xlabel("Ratio de dispersion ENTRE segments  (condition / humains v1)",
                      fontsize=10)
        if col == 0:
            ax.set_ylabel("Ratio de dispersion A L'INTERIEUR des segments\n"
                          "(condition / humains v1)", fontsize=10)
        ax.set_title(f"transport sur l'axe : {axe}", fontsize=11)
        ax.grid(True, color="0.9", lw=0.6)
        ax.set_axisbelow(True)

    for col, axe in enumerate(AXES_TRANSPORT):
        ax = axs[1][col]
        for ic_, c in enumerate(AGENTS):
            for variante, style in (("informee", "-"), ("naive", ":")):
                ys = [traj[(c, axe, variante, l)][1] for l in LAMBDAS]
                ax.plot(LAMBDAS, ys, style, marker=marques[ic_], ms=4.5, lw=1.3,
                        color=f"C{ic_}", label=None)
            ax.plot([dilat[(c, axe)][3]], [dilat[(c, axe)][2]], marker="X", ms=10,
                    color=f"C{ic_}", markeredgecolor="darkorange", mew=1.8)
        ax.axhline(plancher["humains v2"], color="crimson", lw=1.0, ls="--")
        ax.text(0.015, plancher["humains v2"], "  plafond humain, retest v1 contre v2 : "
                f"{plancher['humains v2']:.3f}", transform=ax.get_yaxis_transform(),
                fontsize=7.5, color="crimson", va="bottom", ha="left")
        ax.axhline(plancher["B2"], color="0.35", lw=1.0, ls="--")
        ax.text(0.015, plancher["B2"], "  B2, plus proches voisins humains, a2 : "
                f"{plancher['B2']:.3f}", transform=ax.get_yaxis_transform(),
                fontsize=7.5, color="0.25", va="bottom", ha="left")
        ax.set_xlabel("lambda   (1 = agent d'origine, 0 = plus aucun ecart entre "
                      "segments)", fontsize=9.5)
        if col == 0:
            ax.set_ylabel("Exactitude individuelle\n(egalite exacte, 149 items)",
                          fontsize=10)
        ax.invert_xaxis()
        ax.grid(True, color="0.9", lw=0.6)
        ax.set_axisbelow(True)

    sm = plt.cm.ScalarMappable(cmap=couleurs,
                               norm=plt.Normalize(vmin=vmin, vmax=vmax))
    sm.set_array([])
    cb = fig.colorbar(sm, ax=axs, fraction=0.028, pad=0.02)
    cb.set_label("exactitude individuelle (egalite exacte, 149 items)", fontsize=9)
    leg = [Line2D([], [], marker=m, color="w", markerfacecolor=f"C{i}",
                  markeredgecolor="k", ms=9, label=c)
           for i, (m, c) in enumerate(zip(marques, AGENTS))]
    leg += [Line2D([], [], ls="-", color="0.4", label="variante informee"),
            Line2D([], [], ls=":", color="0.4", label="variante naive (temoin)"),
            Line2D([], [], marker="o", color="w", markerfacecolor="none",
                   markeredgecolor="crimson", ms=11, label="lambda calibre hors item"),
            Line2D([], [], marker="X", color="w", markerfacecolor="0.6",
                   markeredgecolor="darkorange", ms=9,
                   label="temoin, dilatation pure vers intra = 1")]
    axs[0][0].legend(handles=leg, fontsize=8, loc="lower left", framealpha=0.95)
    fig.suptitle("Transport de variance a somme constante : ce que fait lambda, et ce "
                 "qu'il en coute\n"
                 "GSS, archive OSF t6g7k, 1052 participants, 149 items, entropie et "
                 "information mutuelle, estimateurs de a1\n"
                 "Les deux variantes sont confondues dans le plan du haut : elles "
                 "produisent les memes effectifs par segment et ne different que par le "
                 "choix des individus qui basculent",
                 fontsize=11)
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(sortie, f"a7-figure-transport.{ext}"), dpi=175,
                    bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
