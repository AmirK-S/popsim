"""
a18 : decomposition inter et intra des traces a5, condition C2 contre condition C3.

Statut : script d'analyse jetable, pas du code de production. Il ne fait AUCUN appel de
modele de langage. Il relit en LECTURE SEULE les traces JSONL ecrites par le run a5, les
compare aux humains des deux vagues et aux six conditions d'agents de Stanford, et tranche
les quatre questions ouvertes que a15, a7 et a1 ont laissees.

CE QU'IL REPOND
---------------
1. La decomposition de a1 (M1 entropie corrigee, M2 Gini Simpson sans biais), par axe,
   pour C2 et C3, calculee DEUX FOIS : sur l'argmax, et sur la distribution complete.
2. Le contraste prioritaire de a15 : ratio inter par axe, C2 contre C3, ideologie contre
   genre et age.
3. La mesure "a la Chen" (arXiv 2607.26348) : ecart max moins min de la proportion de la
   modalite haute d'echelle entre groupes d'un axe, et delta eta carre.
4. La question decodage contre conditionnement de a7 : le deficit de dispersion totale, en
   trois versions (argmax, tirage, borne en temperature).
5. Le critere A6 en version positive : la variance intra en plus de C3 est elle informative.
6. Le tableau recapitulatif du papier.

CE QU'IL REUTILISE, SANS MODIFIER UNE LIGNE DES SCRIPTS EXISTANTS
-----------------------------------------------------------------
  a1_double_distorsion : lire_nomenclature, lire_demographies, AXES, normaliser,
                         construire_index, compter, decomposer, agreger
                         -> les estimateurs a biais corrige et la segmentation.
  a2_commun            : exactitude_par_personne, bootstrap_personnes, profil_diversite
                         -> exactitude, intervalle sur les personnes, diversite conservee.
  a2_baselines_gss     : charger, CONDITIONS_LLM, PREP
                         -> les 149 items, les deux vagues, les six conditions de Stanford.
  a5_agents_locaux_gss : TRACES, nomenclature
  a5_evaluer           : lire_traces, moyenner_passes, en_matrices,
                         mesures_distributionnelles
                         -> les chargeurs de traces, tolerants a une trace partielle.

LA VERSION DISTRIBUTIONNELLE, SA FORMULE ET SON CONTROLE
---------------------------------------------------------
Chaque cellule (personne i, item j) de C2 et de C3 porte une distribution complete
p_ij(.) sur les K_j modalites de l'item. La version ponctuelle durcit cette distribution
par argmax et retombe sur le format des humains. La version distributionnelle ne la
durcit pas et remplace le comptage d'effectifs par un comptage de MASSE :

    c[g, k] = somme sur les personnes i du segment g de p_ij(k)          (fractionnaire)
    n_g = somme_k c[g, k] = effectif du segment g   (chaque personne pese exactement 1)
    n_k = somme_g c[g, k] = masse totale de la modalite k
    N   = somme_g n_g = nombre de personnes

La distribution de population de l'item est alors le MELANGE des distributions
individuelles, P(k) = n_k / N, et la distribution du segment g est le melange restreint
au segment, P_g(k) = c[g, k] / n_g. Les deux termes sont ceux de a1, calcules sur ces
melanges :

    M1  intra = H(R|S) = somme_g w_g H(P_g)        inter = I(R;S) = H(P) - H(R|S)
    M2  intra = somme_g w_g D(P_g)                 inter = D(P) - intra

Les estimateurs sont EXACTEMENT ceux de a1, avec deux points a documenter.

  a) Gini Simpson sans biais, somme_k c_k (c_k - 1) / (N (N - 1)), s'ecrit tel quel sur
     des effectifs fractionnaires. Sur des effectifs entiers il redonne a1 a l'identique.

  b) Correction de Miller Madow, H_corrige = H_naif + (m - 1) / (2 N ln 2). Le nombre m
     de cases occupees est defini dans a1 par "effectif strictement positif". Sur des
     effectifs fractionnaires cette regle compte toutes les cases, y compris celles qui
     portent 1e-7 personne, et la correction devient enorme et fausse : elle corrigerait
     un bruit d'echantillonnage qui n'existe pas, puisque la masse d'une case ne provient
     pas d'un tirage mais d'une somme de probabilites. La regle employee ici est donc
     "case occupee = case portant au moins UNE personne equivalente", c >= 1. Sur des
     effectifs entiers, toute case occupee porte au moins 1, donc cette regle redonne
     a1 a l'identique. C'est le seul degre de liberte de la version distributionnelle et
     il est teste : la sensibilite au choix c > 0 est calculee et rapportee.

CONTROLE OBLIGATOIRE, ET IL EST EXECUTE A CHAQUE LANCEMENT
------------------------------------------------------------
Les humains n'ont pas de distribution. Leur version distributionnelle est degeneree :
p_ij est une masse de Dirac sur la reponse donnee. Le controle verifie que le chemin
distributionnel, alimente par ces Dirac, redonne le chemin ponctuel de a1 au bit pres,
pour les deux mesures et les six axes. Si l'ecart depasse 1e-9 le script s'arrete.

SORTIES, toutes dans resultats/
-------------------------------
  a18-decomposition.csv           les deux ratios par condition, version et mesure
  a18-ratios-par-axe.csv          le detail axe par axe, contraste 1 de a15
  a18-chen.csv                    gonflement d'ecart et delta eta carre, huit conditions
  a18-dispersion-totale.csv       les trois versions du ratio de dispersion totale
  a18-calibration.csv             entropie individuelle, deciles, fiabilite, ECE
  a18-critere-a6.csv              critere A6 en version positive
  a18-recapitulatif.csv           le tableau du papier
  a18-controle-degenerescence.csv le controle ci dessus, chiffre
  a18-figure-c2-c3.png et .svg    le plan (inter, intra)

AUCUNE MICRODONNEE NE SORT DE data/. Tous les fichiers ci dessus sont des agregats.

Usage :
  .venv/bin/python analyses/a18_decomposition_traces.py
  .venv/bin/python analyses/a18_decomposition_traces.py --bootstrap 200 --rapide
"""

import os
import sys

# Quatre coeurs, consigne de la mission : le run a5 tourne sur la meme machine et deux
# serveurs ou deux calculs qui saturent le GPU s'effondrent mutuellement (a5 section 4.4,
# facteur 9,5 mesure). Ces variables doivent etre posees AVANT l'import de numpy.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "4")

import argparse
import csv
import json
import math
import warnings

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a1_double_distorsion import (AXES, agreger, compter, construire_index, decomposer,
                                  lire_demographies, lire_nomenclature, normaliser)
from a2_commun import (bootstrap_personnes, est_manquant, exactitude_par_personne,
                       profil_diversite)
from a2_baselines_gss import CONDITIONS_LLM, PREP, charger
from a5_agents_locaux_gss import TRACES, nomenclature
from a5_evaluer import (en_matrices, lire_traces, mesures_distributionnelles,
                        moyenner_passes)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OSF = os.path.join(RACINE, "data/osf-t6g7k-stanford")
SORTIE = os.path.join(RACINE, "resultats")
LN2 = math.log(2.0)

MESURES = ["entropie", "gini_simpson"]

# Nos deux conditions, dans l'ordre du run.
NOS_CONDITIONS = ["C2", "C3"]

# Les six conditions de Stanford, libelles de a2_baselines_gss. Ce sont les six points de
# comparaison du plan (inter, intra) de a1, restreints ici a nos personnes et nos items.
STANFORD = list(CONDITIONS_LLM.keys())

REFERENCE = "humains vague 1"


# =======================================================================================
# 1. Estimateurs sur effectifs fractionnaires
# =======================================================================================

def _xlogx(p):
    """p log2 p, prolonge par 0 en 0. Copie conforme de a1."""
    out = np.zeros_like(p)
    m = p > 0
    out[m] = p[m] * np.log2(p[m])
    return out


def decomposer_frac(c, n_min=30, occupation=1.0):
    """Decomposition inter et intra sur des effectifs FRACTIONNAIRES.

    Entree : table (A, J, G, K) de masses, ou c[a, j, g, k] est la somme des probabilites
    accordees a la modalite k, par les personnes du segment g de l'axe a, sur l'item j.
    Pour des reponses ponctuelles c'est la table de contingence entiere de a1.

    Sortie : mesure -> (inter, intra, valide), memes conventions que a1.decomposer.

    Les formules sont celles de a1, cf. l'entete du fichier. `occupation` est le seuil de
    masse au dessus duquel une case compte dans le m de Miller Madow. La valeur 1.0 (une
    personne equivalente) redonne a1 a l'identique sur des effectifs entiers ; la valeur
    0.0 reproduit litteralement la regle de a1 et sert de test de sensibilite.
    """
    n_g = c.sum(axis=3)
    n_k = c.sum(axis=2)
    N = n_g.sum(axis=2)
    valide = N >= n_min
    N_s = np.where(valide, N, 1.0)

    def h_mm(counts):
        p = counts / N_s[:, :, None]
        h = -_xlogx(p).sum(axis=2)
        m = (counts >= occupation).sum(axis=2) if occupation > 0 else (counts > 0).sum(axis=2)
        return h + (m - 1.0) / (2.0 * N_s * LN2)

    h_r = h_mm(n_k)
    h_s = h_mm(n_g)
    h_rs = h_mm(c.reshape(c.shape[0], c.shape[1], -1))
    m1_intra = h_rs - h_s
    m1_inter = h_r - m1_intra

    def simpson_unb(counts, total, axe):
        den = np.where(total > 1.0, total * (total - 1.0), 1.0)
        return 1.0 - (counts * (counts - 1.0)).sum(axis=axe) / den

    d_tot = simpson_unb(n_k, N_s, 2)
    n_g_ok = n_g >= 2
    d_g = simpson_unb(c, np.where(n_g_ok, n_g, 2.0), 3)
    poids = np.where(n_g_ok, n_g, 0.0)
    poids_tot = np.where(poids.sum(axis=2) > 0, poids.sum(axis=2), 1.0)
    m2_intra = (poids * d_g).sum(axis=2) / poids_tot
    m2_inter = d_tot - m2_intra

    return {"entropie": (m1_inter, m1_intra, valide),
            "gini_simpson": (m2_inter, m2_intra, valide)}


def agreger2(dec, masque_items, axes_gardes=None):
    """Somme les termes inter et intra sur les axes et les items retenus.

    Reprise de a1.agreger, sans la branche de la variance ordinale qui n'est pas employee
    ici : la mission demande M1 et M2. Meme regle d'agregation, on somme les termes plutot
    que de moyenner des ratios item par item, pour la raison donnee dans a1 : un item ou la
    dispersion humaine est presque nulle produirait un ratio explosif.
    """
    out = {}
    for m, (inter, intra, valide) in dec.items():
        msk = valide & masque_items[None, :]
        if axes_gardes is not None:
            sel = np.zeros(inter.shape[0], dtype=bool)
            sel[axes_gardes] = True
            msk = msk & sel[:, None]
        out[m] = (float(np.where(msk, inter, 0.0).sum()),
                  float(np.where(msk, intra, 0.0).sum()))
    return out


def compter_frac(P, valide_cell, W, poids=None):
    """Table (A, J, G, K) de masses, a partir des distributions individuelles.

    P            : (n, J, K) probabilites, zero hors des K_j modalites de l'item.
    valide_cell  : (n, J) booleen, cellule effectivement predite et verite disponible.
    W            : liste par axe de matrices (n, G) indicatrices d'appartenance au segment.
    poids        : (n,) poids bootstrap, 1 par defaut.

    c[a, j, g, k] = somme_i W[a][i, g] * poids_i * P[i, j, k] * valide_cell[i, j]
    """
    n, J, K = P.shape
    w = np.ones(n, dtype=np.float64) if poids is None else np.asarray(poids, dtype=np.float64)
    Pm = (P * valide_cell[:, :, None]).reshape(n, J * K)
    A, G = len(W), W[0].shape[1]
    c = np.empty((A, J, G, K), dtype=np.float64)
    for a in range(A):
        # (G, n) @ (n, J*K) -> (G, J*K)
        bloc = (W[a] * w[:, None]).T @ Pm
        c[a] = bloc.reshape(G, J, K).transpose(1, 0, 2)
    return c


# =======================================================================================
# 2. Chargement, alignement, restriction aux cellules disponibles
# =======================================================================================

def coder(matrice, items, options):
    """Code une matrice de reponses en clair en entiers, -1 pour non codable.

    Meme convention que a1.lire_condition : l'index d'une modalite est sa position dans la
    liste ORDONNEE du question_master, jamais un ordre alphabetique ni un ordre
    d'apparition. C'est cet ordre qui donne un sens a "modalite haute d'echelle".
    """
    n, J = matrice.shape
    x = np.full((n, J), -1, dtype=np.int16)
    index = [{m: k for k, m in enumerate(options[q.lower()])} for q in items]
    for j in range(J):
        for i in range(n):
            v = matrice[i, j]
            if est_manquant(v):
                continue
            k = index[j].get(normaliser(str(v)), -1)
            if k >= 0:
                x[i, j] = k
    return x


def charger_traces(suffixe, personnes_csv, items, index_item):
    """Lit les traces a5 en lecture seule et rend, par condition, l'argmax et la distribution.

    Tolere une trace partielle : le run ecrit personne par personne, une troncature coute
    des personnes entieres et jamais des items (a5 section 1). On rapporte donc, par
    condition, le nombre de cellules, le nombre de personnes completes et la couverture.
    """
    tables, fichiers = lire_traces(suffixe)
    if not tables:
        sys.exit(f"aucune trace lue dans {TRACES} (suffixe '{suffixe}')")
    table_nom = nomenclature()
    presents = {}
    for condition in NOS_CONDITIONS:
        fusion, passes = moyenner_passes(tables, condition)
        if not fusion:
            continue
        presents[condition] = {"fusion": fusion, "passes": passes,
                               "n_appels": len(fusion),
                               "pids": sorted({k[0] for k in fusion}),
                               "items": {k[1] for k in fusion}}
    return presents, fichiers, table_nom


def personnes_completes(fusion, items, seuil):
    """Personnes dont la trace couvre au moins `seuil` des items cibles."""
    par_pid = {}
    for (pid, it) in fusion:
        if it in items:
            par_pid[pid] = par_pid.get(pid, 0) + 1
    return {p for p, c in par_pid.items() if c >= seuil * len(items)}


# =======================================================================================
# 3. Le bloc de mesure : un jeu de conditions, une population, une grille d'items
# =======================================================================================

class Banc:
    """Porte la population evaluee, la segmentation, et calcule les deux ratios.

    Un Banc fige : les personnes retenues, les items retenus, le masque de cellules
    valides commun a toutes les conditions, et les indicatrices de segment. Toutes les
    conditions sont ensuite mesurees sur exactement les memes cellules, ce qui est la
    condition sine qua non pour que les ratios veuillent dire quelque chose.
    """

    def __init__(self, lignes, colonnes, items, seg, niveaux, options, n_min):
        self.lignes = lignes
        self.colonnes = colonnes
        self.items = items
        self.n = len(lignes)
        self.J = len(colonnes)
        self.n_min = n_min
        self.seg = {a: seg[a][lignes] for a in AXES}
        self.niveaux = niveaux
        self.g_max = int(max(len(niveaux[a]) for a in AXES))
        self.k_par_item = np.array([len(options[q.lower()]) for q in items])
        self.k_max = int(self.k_par_item.max())
        self.masque_items = np.ones(self.J, dtype=bool)
        # Indicatrices de segment, une matrice (n, g_max) par axe. Une personne sans
        # etiquette sur un axe (segment -1) ne pese dans aucun segment de cet axe.
        self.W = []
        for a in AXES:
            m = np.zeros((self.n, self.g_max), dtype=np.float64)
            g = self.seg[a]
            ok = g >= 0
            m[np.arange(self.n)[ok], g[ok]] = 1.0
            self.W.append(m)
        self.n_axes = len(AXES)
        self._faux_ordinal = np.zeros((self.J, self.k_max))

        # Axe supplementaire, employe UNIQUEMENT par la mesure a la Chen : l'ideologie
        # ramenee a trois blocs. Motif chiffre, et il n'est pas cosmetique. Chen mesure
        # l'axe "political views" sur 14 704 repondants ; nous en avons 150 au plus,
        # repartis sur les sept niveaux du GSS, dont "extremely liberal" et "extremely
        # conservative" qui pesent quelques personnes. A seuil d'effectif, deux ou trois
        # niveaux seulement survivent et l'ecart max moins min porte alors sur une paire
        # arbitraire. La regle de regroupement est celle de a1, recopiee a l'identique de
        # sa fonction bloc_ideologie : "liberal" dans le libelle donne gauche,
        # "conservative" donne droite, le reste donne centre. Elle est mecanique et ne
        # depend d'aucun jugement.
        blocs = {"gauche": 0, "centre": 1, "droite": 2}
        w3 = np.zeros((self.n, self.g_max), dtype=np.float64)
        for i in range(self.n):
            g = self.seg["political_ideology"][i]
            if g < 0:
                continue
            v = niveaux["political_ideology"][g]
            b = "gauche" if "liberal" in v else ("droite" if "conservative" in v
                                                 else "centre")
            w3[i, blocs[b]] = 1.0
        self.W_chen = self.W + [w3]
        self.axes_chen = AXES + ["ideologie en 3 blocs"]
        self.niveaux_chen = dict(niveaux)
        self.niveaux_chen["ideologie en 3 blocs"] = ["gauche", "centre", "droite"]

    def index_point(self, x):
        """Index plat de a1 pour une matrice de codes entiers deja restreinte au banc."""
        return construire_index(x, self.seg, self.k_max, self.g_max, self.J)

    def compter_point(self, idx, poubelle, lignes_sel):
        return compter(idx, lignes_sel, poubelle, self.J, self.g_max, self.k_max,
                       self.n_axes)


def masse_valide(x_dict, verite_codes):
    """Masque (n, J) des cellules exploitables pour TOUTES les conditions du jeu.

    Une cellule est retenue si la verite terrain est codable et si chaque condition a
    produit une reponse codable. Sans ce masque commun, une condition qui couvre moins de
    cellules aurait une population differente et son ratio serait faux.
    """
    m = verite_codes >= 0
    for x in x_dict.values():
        m = m & (x >= 0)
    return m


# =======================================================================================
# 4. Programme principal
# =======================================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suffixe", default="", help="suffixe des traces, par exemple smoke")
    ap.add_argument("--sortie", default=SORTIE)
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--permutations", type=int, default=50)
    ap.add_argument("--graine", type=int, default=20260908)
    ap.add_argument("--n-min", type=int, default=30,
                    help="effectif minimal par item pour qu'il entre dans la decomposition")
    ap.add_argument("--seg-min", type=int, default=8,
                    help="effectif minimal d'un segment pour la mesure a la Chen")
    ap.add_argument("--couverture", type=float, default=0.98,
                    help="part des items requise pour qu'une personne compte comme complete")
    ap.add_argument("--rapide", action="store_true",
                    help="bootstrap 100 et 15 permutations, pour un essai")
    args = ap.parse_args()
    if args.rapide:
        args.bootstrap, args.permutations = 100, 15
    os.makedirs(args.sortie, exist_ok=True)
    rng = np.random.default_rng(args.graine)
    journal = {}

    print("=" * 100)
    print("a18 : DECOMPOSITION INTER ET INTRA DES TRACES a5, C2 CONTRE C3")
    print("=" * 100)

    # --- donnees de reference -----------------------------------------------------
    options, ordinal = lire_nomenclature(OSF)
    ids, items, y1, y2, x_dem, attributs = charger()
    index_personne = {p: i for i, p in enumerate(ids)}
    index_item = {c: j for j, c in enumerate(items)}
    seg, niveaux = lire_demographies(OSF, ids)
    est_ordinal = np.array([ordinal.get(q.lower(), False) for q in items])
    print(f"{len(ids)} personnes dans le corpus, {len(items)} items cibles, "
          f"{int(est_ordinal.sum())} ordinaux")

    # --- traces ---------------------------------------------------------------------
    presents, fichiers, table_nom = charger_traces(args.suffixe, None, items, index_item)
    print("\ntraces lues en LECTURE SEULE :")
    for f in fichiers:
        print(f"  {f}")
    couverture = {}
    for c, d in presents.items():
        complets = personnes_completes(d["fusion"], set(items), args.couverture)
        couverture[c] = complets
        print(f"  {c} : {d['n_appels']} appels, {len(d['pids'])} personnes touchees, "
              f"{len(complets)} personnes couvertes a {args.couverture:.0%}, "
              f"{len(d['items'] & set(items))} items")
    journal["traces"] = {c: {"appels": d["n_appels"], "personnes_touchees": len(d["pids"]),
                             "personnes_completes": len(couverture[c])}
                         for c, d in presents.items()}

    # Population commune : les personnes de l'echantillon du run couvertes par TOUTES les
    # conditions presentes. C'est le seul choix qui rende C2 et C3 comparables.
    ech = pd.read_csv(os.path.join(TRACES, "a5-personnes.csv"))
    ordre_ech = [p for p in ech["pid"]]
    commun = set(ordre_ech)
    for c in presents:
        commun &= couverture[c]
    personnes = [p for p in ordre_ech if p in commun]
    if not personnes:
        sys.exit("aucune personne complete dans les traces, rien a mesurer")
    lignes = [index_personne[p] for p in personnes]

    # Items : ceux vus dans toutes les conditions presentes.
    items_vus = set(items)
    for c, d in presents.items():
        items_vus &= d["items"]
    items_ev = [c for c in items if c in items_vus]
    colonnes = [index_item[c] for c in items_ev]
    print(f"\npopulation commune : {len(personnes)} personnes, {len(items_ev)} items, "
          f"soit {len(personnes) * len(items_ev)} cellules par condition")
    journal["population"] = {"n_personnes": len(personnes), "n_items": len(items_ev),
                             "conditions_presentes": sorted(presents)}

    n_min = args.n_min
    if len(personnes) < n_min:
        n_min = max(5, len(personnes))
        print(f"AVERTISSEMENT : moins de {args.n_min} personnes, seuil d'item abaisse "
              f"a {n_min}. Les termes inter sont alors tres bruites.")
    journal["n_min"] = n_min

    # --- matrices de reponses, toutes conditions ------------------------------------
    verite = y1[np.ix_(lignes, colonnes)]
    verite2 = y2[np.ix_(lignes, colonnes)]
    brut = {REFERENCE: verite, "humains vague 2": verite2}
    for libelle, fichier in CONDITIONS_LLM.items():
        chemin = os.path.join(PREP, fichier)
        if not os.path.exists(chemin):
            continue
        d = pd.read_csv(chemin)
        assert list(d["email"]) == ids, f"{fichier} n'est pas aligne sur charger()"
        brut[libelle] = d[items_ev].values.astype(object)[lignes]

    distributions = {}
    for c, d in presents.items():
        pred, dist = en_matrices(d["fusion"], personnes, items_ev, table_nom)
        brut[c] = pred
        distributions[c] = dist

    codes = {nom: coder(m, items_ev, options) for nom, m in brut.items()}
    masque = masse_valide(codes, codes[REFERENCE])
    print(f"cellules exploitables par toutes les conditions : {int(masque.sum())} "
          f"sur {masque.size} ({100 * masque.mean():.2f} pour cent)")
    journal["cellules_exploitables"] = int(masque.sum())
    for nom, x in codes.items():
        codes[nom] = np.where(masque, x, -1).astype(np.int16)

    banc = Banc(lignes, colonnes, items_ev, seg, niveaux, options, n_min)
    noms = [REFERENCE, "humains vague 2"] + sorted(presents) + \
           [s for s in STANFORD if s in brut]

    # --- tenseurs de distributions ---------------------------------------------------
    # P[i, j, k] pour chaque condition. Les humains et Stanford sont degeneres : masse 1
    # sur la modalite donnee. C'est ce qui rend le controle de degenerescence possible.
    def tenseur_degenere(x):
        P = np.zeros((banc.n, banc.J, banc.k_max))
        ii, jj = np.where(x >= 0)
        P[ii, jj, x[ii, jj]] = 1.0
        return P

    P = {nom: tenseur_degenere(codes[nom]) for nom in noms}
    for c in presents:
        Q = np.zeros((banc.n, banc.J, banc.k_max))
        for j, it in enumerate(items_ev):
            liste = [normaliser(o) for o in options[it.lower()]]
            pos = {m: k for k, m in enumerate(liste)}
            for i in range(banc.n):
                d = distributions[c][i][j]
                if d is None or not masque[i, j]:
                    continue
                for mod, p in d.items():
                    k = pos.get(normaliser(str(mod)))
                    if k is not None:
                        Q[i, j, k] += p
        s = Q.sum(axis=2, keepdims=True)
        Q = np.where(s > 0, Q / np.where(s > 0, s, 1.0), 0.0)
        P[c] = Q

    valide_cell = masque.astype(np.float64)

    # ================================================================================
    # CONTROLE 1 : la version distributionnelle degeneree redonne la version ponctuelle
    # ================================================================================
    print("\n" + "=" * 100)
    print("CONTROLE DE DEGENERESCENCE")
    print("Les humains n'ont pas de distribution. Alimente par leurs Dirac, le chemin")
    print("distributionnel doit redonner le chemin ponctuel de a1 au bit pres.")
    print("=" * 100)
    lignes_ctrl = [["condition", "mesure", "terme", "voie_ponctuelle_a1",
                    "voie_distributionnelle", "ecart_absolu"]]
    pire = 0.0
    for nom in [REFERENCE, "humains vague 2"] + [s for s in STANFORD if s in brut][:2]:
        idx, poubelle = banc.index_point(codes[nom])
        c_pt = banc.compter_point(idx, poubelle, np.arange(banc.n))
        dec_pt = decomposer(c_pt, banc._faux_ordinal, n_min=n_min)
        c_fr = compter_frac(P[nom], valide_cell, banc.W)
        dec_fr = decomposer_frac(c_fr, n_min=n_min)
        a_pt = agreger2({m: dec_pt[m] for m in MESURES}, banc.masque_items)
        a_fr = agreger2(dec_fr, banc.masque_items)
        for m in MESURES:
            for t, lib in ((0, "inter"), (1, "intra")):
                e = abs(a_pt[m][t] - a_fr[m][t])
                pire = max(pire, e)
                lignes_ctrl.append([nom, m, lib, f"{a_pt[m][t]:.10f}",
                                    f"{a_fr[m][t]:.10f}", f"{e:.3e}"])
    print(f"ecart maximal entre les deux voies sur les conditions ponctuelles : {pire:.3e}")
    if pire > 1e-9:
        sys.exit("CONTROLE ECHOUE : les deux voies ne coincident pas sur des reponses "
                 "ponctuelles. Aucun chiffre distributionnel n'est publiable.")
    print("CONTROLE PASSE. La voie distributionnelle est une generalisation exacte.")
    journal["controle_degenerescence_ecart_max"] = pire
    with open(os.path.join(args.sortie, "a18-controle-degenerescence.csv"), "w",
              newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_ctrl)

    # ================================================================================
    # 5. La decomposition, deux versions
    # ================================================================================
    # Un "jeu" est un couple (libelle affiche, fonction qui rend la table de comptage a
    # partir d'un vecteur de poids bootstrap). Les conditions ponctuelles passent par
    # a1.compter, nos deux conditions passent en plus par la voie fractionnaire.
    # T[libelle] est le tenseur (n, J, K) employe par TOUTES les mesures pour ce libelle :
    # decomposition, permutation, bootstrap, mesure de Chen, dispersion totale. Le durcir
    # ici une fois et pour toutes evite qu'une voie lise la distribution la ou une autre
    # lit l'argmax, ce qui a ete une erreur reelle de la premiere version de ce script.
    T = {}
    jeux = []
    index_pt = {}
    for nom in noms:
        idx, poubelle = banc.index_point(codes[nom])
        index_pt[nom] = (idx, poubelle)
        lib = nom if nom not in presents else f"{nom} argmax"
        T[lib] = _degenerer(P[nom]) if nom in presents else P[nom]
        jeux.append((lib, nom, "argmax"))
    for c in sorted(presents):
        T[f"{c} distribution"] = P[c]
        jeux.append((f"{c} distribution", c, "distribution"))

    # Controle : le durcissement du tenseur redonne bien la matrice d'argmax de la trace.
    for c in sorted(presents):
        d = _degenerer(P[c])
        rec = np.where(d.sum(axis=2) > 0, np.argmax(d, axis=2), -1)
        att = np.where(masque, codes[c], -1)
        ecart = int(((rec != att) & (att >= 0)).sum())
        if ecart:
            sys.exit(f"{ecart} cellules ou l'argmax du tenseur de {c} differe de "
                     "l'argmax enregistre dans la trace. Chaine de lecture incoherente.")
    print("controle : l'argmax du tenseur de distributions coincide avec celui de la "
          "trace sur toutes les cellules.")

    def dec_de(lib, poids=None, seg_perm=None):
        W = banc.W if seg_perm is None else seg_perm
        return decomposer_frac(compter_frac(T[lib], valide_cell, W, poids), n_min=n_min)

    print("\ncalcul du point, puis correction residuelle par permutation "
          f"({args.permutations} permutations), puis bootstrap ({args.bootstrap} tirages)")

    # --- point ---------------------------------------------------------------------
    dec_point = {lib: dec_de(lib) for lib, _, _ in jeux}
    obs = {lib: agreger2(dec_point[lib], banc.masque_items) for lib, _, _ in jeux}
    obs_axe = {lib: {a: agreger2(dec_point[lib], banc.masque_items, axes_gardes=[i])
                     for i, a in enumerate(AXES)} for lib, _, _ in jeux}

    # --- correction residuelle par permutation --------------------------------------
    # Sous permutation des etiquettes de segment, le terme inter DOIT valoir zero. Ce qui
    # subsiste est un biais d'estimation et il est soustrait, exactement comme dans a1.
    nul = {lib: {m: [] for m in MESURES} for lib, _, _ in jeux}
    nul_axe = {lib: {a: {m: [] for m in MESURES} for a in AXES} for lib, _, _ in jeux}
    for _ in range(args.permutations):
        perm = rng.permutation(banc.n)
        Wp = [w[perm] for w in banc.W]
        for lib, _, _ in jeux:
            d = dec_de(lib, seg_perm=Wp)
            ag = agreger2(d, banc.masque_items)
            for m in MESURES:
                nul[lib][m].append(ag[m][0])
            for i, a in enumerate(AXES):
                ag_a = agreger2(d, banc.masque_items, axes_gardes=[i])
                for m in MESURES:
                    nul_axe[lib][a][m].append(ag_a[m][0])
    nul = {lib: {m: float(np.mean(v)) for m, v in d.items()} for lib, d in nul.items()}
    nul_axe = {lib: {a: {m: float(np.mean(v)) for m, v in d.items()} for a, d in dd.items()}
               for lib, dd in nul_axe.items()}

    point = {lib: {m: (obs[lib][m][0] - nul[lib][m], obs[lib][m][1]) for m in MESURES}
             for lib, _, _ in jeux}
    point_axe = {lib: {a: {m: (obs_axe[lib][a][m][0] - nul_axe[lib][a][m],
                               obs_axe[lib][a][m][1]) for m in MESURES} for a in AXES}
                 for lib, _, _ in jeux}
    ref = point[REFERENCE]
    ref_axe = point_axe[REFERENCE]

    # --- bootstrap recentre sur les personnes ---------------------------------------
    # Meme point de methode que a1 : le terme inter est une composante dont la valeur
    # vraie est petite, un tirage bootstrap ajoute une couche de bruit qui se loge
    # entierement dedans. On recentre donc chaque distribution bootstrap, de facon
    # additive, sur son estimation ponctuelle avant de former le ratio. Le tirage sert a
    # estimer la FORME de la distribution d'echantillonnage, pas son centre.
    tir = {lib: {m: ([], []) for m in MESURES} for lib, _, _ in jeux}
    for b in range(args.bootstrap):
        sel = rng.integers(0, banc.n, size=banc.n)
        poids = np.bincount(sel, minlength=banc.n).astype(np.float64)
        for lib, _, _ in jeux:
            ag = agreger2(dec_de(lib, poids=poids), banc.masque_items)
            for m in MESURES:
                tir[lib][m][0].append(ag[m][0])
                tir[lib][m][1].append(ag[m][1])
        if (b + 1) % max(1, args.bootstrap // 8) == 0:
            print(f"  bootstrap {b + 1}/{args.bootstrap}", flush=True)

    def recentrer(v, cible):
        v = np.asarray(v, dtype=float)
        f = np.isfinite(v)
        if f.sum() < 20:
            return v
        return v - v[f].mean() + cible

    boot = {lib: {m: (recentrer(tir[lib][m][0], point[lib][m][0]),
                      recentrer(tir[lib][m][1], point[lib][m][1])) for m in MESURES}
            for lib, _, _ in jeux}

    def ic(v):
        v = np.asarray(v, dtype=float)
        v = v[np.isfinite(v)]
        if v.size < 20:
            return float("nan"), float("nan")
        return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))

    ratios, ic_ratios, signe = {}, {}, {}
    for lib, _, _ in jeux:
        ratios[lib] = {m: (point[lib][m][0] / ref[m][0], point[lib][m][1] / ref[m][1])
                       for m in MESURES}
        ic_ratios[lib] = {m: (ic(boot[lib][m][0] / boot[REFERENCE][m][0]),
                              ic(boot[lib][m][1] / boot[REFERENCE][m][1]))
                          for m in MESURES}
        # Statistique de signe, robuste quand le denominateur bootstrap s'approche de zero
        # et fait exploser l'intervalle du RATIO. Elle repond a la seule question qui
        # compte pour la these : le terme inter de la condition depasse t il celui des
        # humains ? Elle reste definie meme quand l'intervalle du ratio ne l'est pas.
        signe[lib] = {m: float(np.mean(boot[lib][m][0] > boot[REFERENCE][m][0]))
                      for m in MESURES}

    globaux = {lib: {m: (point[lib][m][0] + point[lib][m][1]) / (ref[m][0] + ref[m][1])
                     for m in MESURES} for lib, _, _ in jeux}

    print("\n" + "=" * 100)
    print("LES DEUX RATIOS, condition rapportee aux humains de la vague 1")
    print("=" * 100)
    l_csv = [["condition", "mesure", "ratio_inter", "inter_ic_bas", "inter_ic_haut",
              "part_tirages_inter_sup_humain", "ratio_intra", "intra_ic_bas",
              "intra_ic_haut", "produit", "ratio_total"]]
    for m in MESURES:
        print(f"\n--- {m} ---")
        print(f"{'condition':<26}{'ratio inter':>26}{'P(sup)':>8}{'ratio intra':>26}"
              f"{'produit':>10}{'total':>9}")
        for lib, _, _ in jeux:
            ri, ra = ratios[lib][m]
            (i1, i2), (a1_, a2_) = ic_ratios[lib][m]
            sg = "     -  " if lib == REFERENCE else f"{signe[lib][m]:>8.2f}"
            print(f"{lib:<26}{ri:>9.3f} [{i1:6.3f} ; {i2:6.3f}]{sg}"
                  f"{ra:>10.3f} [{a1_:5.3f} ; {a2_:5.3f}]{ri * ra:>10.3f}"
                  f"{globaux[lib][m]:>9.3f}")
            l_csv.append([lib, m, f"{ri:.4f}", f"{i1:.4f}", f"{i2:.4f}",
                          f"{signe[lib][m]:.4f}", f"{ra:.4f}",
                          f"{a1_:.4f}", f"{a2_:.4f}", f"{ri * ra:.4f}",
                          f"{globaux[lib][m]:.4f}"])
    print("\nP(sup) : part des tirages bootstrap ou le terme inter de la condition depasse")
    print("celui des humains vague 1. Elle reste lisible quand l'intervalle du RATIO")
    print("explose, ce qui arrive des que le denominateur bootstrap approche zero.")
    with open(os.path.join(args.sortie, "a18-decomposition.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(l_csv)

    # --- sensibilite au seuil d'occupation de Miller Madow ---------------------------
    print("\nSensibilite de la voie distributionnelle au seuil d'occupation de Miller Madow")
    print("c >= 1 personne equivalente (retenu) contre c > 0 (regle litterale de a1)")
    sens = [["condition", "mesure", "inter_seuil_1", "inter_seuil_0", "intra_seuil_1",
             "intra_seuil_0"]]
    for c in sorted(presents):
        d0 = decomposer_frac(compter_frac(T[f"{c} distribution"], valide_cell, banc.W),
                             n_min=n_min, occupation=0.0)
        a0 = agreger2(d0, banc.masque_items)
        a1v = obs[f"{c} distribution"]
        for m in MESURES:
            print(f"  {c} {m:<14} inter {a1v[m][0]:9.3f} contre {a0[m][0]:9.3f}   "
                  f"intra {a1v[m][1]:9.3f} contre {a0[m][1]:9.3f}")
            sens.append([c, m, f"{a1v[m][0]:.4f}", f"{a0[m][0]:.4f}",
                         f"{a1v[m][1]:.4f}", f"{a0[m][1]:.4f}"])
    with open(os.path.join(args.sortie, "a18-sensibilite-occupation.csv"), "w",
              newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(sens)

    # ================================================================================
    # 6. Contraste 1 de a15 : le ratio inter par axe
    # ================================================================================
    print("\n" + "=" * 100)
    print("CONTRASTE 1 DE a15 : RATIO INTER PAR AXE, mesure entropie")
    print("=" * 100)
    print(f"{'condition':<26}" + "".join(f"{a[:13]:>14}" for a in AXES))
    # Le denominateur, en clair. Un ratio dont le denominateur vaut quelques centiemes de
    # bit n'est pas interpretable, et c'est le cas du genre : chez les humains le segment
    # de genre n'explique presque rien. Il faut le voir avant de lire la colonne.
    print(f"{'DENOMINATEUR, inter humain':<26}"
          + "".join(f"{ref_axe[a]['entropie'][0]:>14.2f}" for a in AXES)
          + "   <- bits, sur tous les items")
    l_axe = [["condition", "axe", "mesure", "inter_humain_vague1", "ratio_inter",
              "ratio_intra"]]
    tab_axe = {}
    for lib, _, _ in jeux:
        cells, ligne = "", {}
        for a in AXES:
            for m in MESURES:
                b = ref_axe[a][m]
                if b[0] != 0 and b[1] != 0:
                    l_axe.append([lib, a, m, f"{b[0]:.4f}",
                                  f"{point_axe[lib][a][m][0] / b[0]:.4f}",
                                  f"{point_axe[lib][a][m][1] / b[1]:.4f}"])
            r = point_axe[lib][a]["entropie"][0] / ref_axe[a]["entropie"][0]
            ligne[a] = r
            cells += f"{r:>14.2f}"
        tab_axe[lib] = ligne
        print(f"{lib:<26}{cells}")
    with open(os.path.join(args.sortie, "a18-ratios-par-axe.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(l_axe)

    # Verdict mecanique sur les trois issues ecrites dans a15 section 8, sous condition
    # que le controle passe : les humains de la vague 2 sont les MEMES personnes deux
    # semaines plus tard, leur ratio inter doit tomber au voisinage de 1 sur chaque axe.
    # La ou il n'y tombe pas, l'axe est trop bruite pour porter une conclusion, et c'est
    # une propriete de la taille d'echantillon, pas des agents.
    verdict = trancher_a15(tab_axe, presents)
    print("\nVERDICT SUR LES TROIS ISSUES DE a15 SECTION 8")
    for l in verdict["texte"]:
        print("  " + l)
    journal["verdict_a15"] = verdict
    journal["part_tirages_inter_sup_humain"] = {l: signe[l] for l, _, _ in jeux}
    journal["ratios"] = {l: {m: {"inter": ratios[l][m][0], "intra": ratios[l][m][1],
                                 "total": globaux[l][m]} for m in MESURES}
                         for l, _, _ in jeux}
    journal["ratios_par_axe_entropie"] = tab_axe

    # --- le bon vis a vis de C2 dans l'archive de Stanford -------------------------
    journal["c2_contre_v8"] = comparer_v6_v8(tab_axe, presents)

    # ================================================================================
    # 7. La mesure a la Chen
    # ================================================================================
    chen = mesure_chen(banc, T, valide_cell, est_ordinal[colonnes], options, items_ev,
                       jeux, noms, presents, args.sortie, seg_min=args.seg_min)
    journal["chen"] = chen["resume"]

    # ================================================================================
    # 8. Dispersion totale : decodage ou conditionnement
    # ================================================================================
    disp = dispersion_totale(banc, T, P, valide_cell, presents, args.sortie)
    journal["dispersion_totale"] = disp

    # ================================================================================
    # 9. Calibration et entropie individuelle
    # ================================================================================
    calib = {}
    for c in sorted(presents):
        calib[c] = mesures_distributionnelles(
            np.array([[distributions[c][i][j] if masque[i, j] else None
                       for j in range(banc.J)] for i in range(banc.n)], dtype=object),
            np.where(masque, verite, None))
    ecrire_calibration(calib, P, valide_cell, banc, args.sortie)
    journal["calibration"] = {c: {k: v for k, v in m.items()
                                  if k != "calibration_par_decile"}
                              for c, m in calib.items() if m}

    # ================================================================================
    # 10. Critere A6 en version positive
    # ================================================================================
    a6 = critere_a6(banc, codes, brut, verite, verite2, noms, presents, seg, lignes,
                    args.sortie)
    journal["critere_a6"] = a6

    # ================================================================================
    # 11. Le tableau recapitulatif
    # ================================================================================
    recap = recapitulatif(brut, verite, verite2, masque, calib, ratios, tab_axe, globaux,
                          noms, presents, args.sortie)
    journal["recapitulatif"] = recap

    # ================================================================================
    # 12. La figure
    # ================================================================================
    tracer(ratios, ic_ratios, globaux, jeux, presents, args.sortie,
           len(personnes), len(items_ev))

    with open(os.path.join(args.sortie, "a18-journal.json"), "w", encoding="utf-8") as fh:
        json.dump(journal, fh, indent=2, ensure_ascii=False, default=float)
    print(f"\necrit dans {args.sortie}/ : a18-decomposition.csv, a18-ratios-par-axe.csv, "
          "a18-chen.csv,\n  a18-dispersion-totale.csv, a18-calibration.csv, "
          "a18-critere-a6.csv, a18-recapitulatif.csv,\n  "
          "a18-controle-degenerescence.csv, a18-sensibilite-occupation.csv, "
          "a18-journal.json,\n  a18-figure-c2-c3.png et .svg")


# =======================================================================================
# Le verdict de a15
# =======================================================================================

def trancher_a15(tab, presents, seuil_gonflement=1.25, seuil_voisinage=1.25):
    """Applique mecaniquement les trois issues ecrites dans a15 section 8.

    Issue A : C2 gonfle sur l'ideologie et reste au voisinage de 1 sur genre et age, C3
              fait de meme mais moins. La variable qui separe est l'AXE de segmentation.
    Issue B : C2 gonfle sur tous les axes et C3 sur aucun. C'est l'ETIQUETTE de groupe
              dans l'invite qui commande.
    Issue C : C2 et C3 gonflent l'ideologie a un niveau comparable. Ni l'etiquette ni la
              richesse ne commandent : le modele reconstruit l'ideologie et essentialise.
    """
    out = {"texte": [], "issue": "indeterminee"}

    # Le controle d'abord. Les humains de la vague 2 doivent tomber au voisinage de 1.
    ctrl = tab.get("humains vague 2", {})
    axes_sains = [a for a in AXES
                  if a in ctrl and 1 / seuil_voisinage <= ctrl[a] <= seuil_voisinage]
    out["controle_vague2"] = {a: ctrl.get(a, float("nan")) for a in AXES}
    out["axes_sains"] = axes_sains
    out["texte"].append(
        "controle vague 2 par axe : "
        + ", ".join(f"{a} {ctrl.get(a, float('nan')):.2f}" for a in AXES))
    manquants = [a for a in ("political_ideology", "gender", "age") if a not in axes_sains]
    if manquants:
        out["texte"].append(
            "CONTROLE NON PASSE sur " + ", ".join(manquants)
            + ". Sur ces axes le ratio inter des memes personnes reinterrogees s'ecarte "
              "deja de 1 : l'echantillon est trop petit pour que l'axe porte une "
              "conclusion, et aucun verdict de a15 n'y est lisible.")

    lib = {c: (f"{c} argmax" if f"{c} argmax" in tab else c) for c in presents}
    if "C2" not in lib or "C3" not in lib:
        out["texte"].append(
            f"les deux conditions ne sont pas toutes deux disponibles ({sorted(presents)}), "
            "le contraste 1 ne peut pas etre tranche")
        return out
    v = {}
    for c in ("C2", "C3"):
        v[c] = {a: tab[lib[c]][a] for a in AXES}
    ideo2, ideo3 = v["C2"]["political_ideology"], v["C3"]["political_ideology"]
    autres2 = [v["C2"][a] for a in ("gender", "age")]
    autres3 = [v["C3"][a] for a in ("gender", "age")]
    tous2 = [v["C2"][a] for a in AXES if a != "political_ideology"]
    out["ratios"] = v
    out["texte"].append(f"ratio inter ideologie : C2 = {ideo2:.2f}, C3 = {ideo3:.2f}")
    out["texte"].append(f"ratio inter genre     : C2 = {v['C2']['gender']:.2f}, "
                        f"C3 = {v['C3']['gender']:.2f}")
    out["texte"].append(f"ratio inter age       : C2 = {v['C2']['age']:.2f}, "
                        f"C3 = {v['C3']['age']:.2f}")
    a_gonfle2 = ideo2 > seuil_gonflement
    a_gonfle3 = ideo3 > seuil_gonflement
    voisin2 = all(1 / seuil_voisinage <= r <= seuil_voisinage for r in autres2)
    voisin3 = all(1 / seuil_voisinage <= r <= seuil_voisinage for r in autres3)
    tous_gonfles2 = all(r > seuil_gonflement for r in tous2)
    comparable = a_gonfle2 and a_gonfle3 and \
        (min(ideo2, ideo3) / max(ideo2, ideo3) > 0.75)

    if comparable:
        out["issue"] = "C : le modele reconstruit l'ideologie"
        out["texte"].append(
            "ISSUE C observee : C2 et C3 gonflent l'ideologie a un niveau comparable. "
            "Ni l'etiquette ni la richesse de l'invite ne commandent. C3 n'a jamais vu "
            "l'etiquette ideologique et gonfle quand meme : le modele la reconstruit a "
            "partir des reponses puis essentialise. C'est le resultat le plus interessant "
            "et le plus difficile a defendre, il exige de montrer que C3 a bien "
            "reconstruit l'ideologie.")
    elif tous_gonfles2 and not a_gonfle3:
        out["issue"] = "B : l'etiquette de groupe commande"
        out["texte"].append(
            "ISSUE B observee : C2 gonfle uniformement, C3 sur aucun axe. C'est "
            "l'etiquette de groupe dans l'invite qui commande, H2 elargie est soutenue, "
            "et la phrase de synthese de a15 section 7.1 doit etre reecrite autour de "
            "l'etiquette et non de l'axe.")
    elif a_gonfle2 and voisin2 and (ideo3 < ideo2):
        out["issue"] = "A : l'axe de segmentation commande"
        out["texte"].append(
            "ISSUE A observee : C2 gonfle sur l'ideologie et reste au voisinage de 1 sur "
            "genre et age, C3 fait de meme en moins fort. La variable qui separe est "
            "l'axe de segmentation, pas le contenu de l'invite. C'est le resultat attendu "
            "par a15 et il valide sa phrase de synthese 7.1.")
    else:
        out["texte"].append(
            "AUCUNE des trois issues ecrites dans a15 ne decrit ce tableau. Le detail par "
            "axe doit etre lu tel quel et a15 section 7.1 doit etre reouverte.")
    if manquants:
        out["issue"] = out["issue"] + " (SOUS RESERVE, controle non passe sur " \
            + ", ".join(manquants) + ")"
        out["texte"].append(
            "Ce verdict est SOUS RESERVE : le controle de la vague 2 ne passe pas sur "
            + ", ".join(manquants) + ". Il ne doit pas etre ecrit dans un rapport tant "
            "que le controle n'est pas passe sur l'axe concerne.")
    out["texte"].append(
        "Reserve a porter avec le resultat, elle est dans a15 : pour C2 l'axe "
        "political_ideology est DANS l'invite, pour C3 il ne l'est pas. Mesurer un "
        "gonflement sur un axe fourni au modele n'est pas la meme chose que le mesurer "
        "sur un axe qu'il doit inferer.")
    return out


# =======================================================================================
# Le bon vis a vis de C2 dans l'archive : v8 et non v6
# =======================================================================================

def comparer_v6_v8(tab, presents):
    """Place C2 en regard de gss_v8 et dit pourquoi la comparaison a gss_v6 est faussee.

    Fait etabli dans resultats/a17-relecture-adverse.md, objection 3, par les taux de
    recopie mesures dans le paquet OSF : gss_v6 est un agent demographique SANS ideologie
    ni parti dans son invite, il recopie marital, religion, diplome et revenu a plus de
    99 pour cent mais n'obtient que 0,20 sur polviews ; gss_v8 est un agent demographique
    AVEC ideologie et parti, il recopie polviews a 0,96 et partyid a 0,99. [CONFIRME]

    Notre C2 porte les onze attributs de demographic_summary.csv, political_ideology et
    political_party compris. Son homologue est donc v8. Comparer C2 a v6 reviendrait a
    comparer une invite qui contient l'ideologie a une invite qui ne la contient pas, et
    a attribuer au modele un ecart qui vient de l'invite.

    La prediction a confronter est l'ecart v6 contre v8 sur le ratio inter de l'axe
    ideologie : 0,34 contre 8,51 sur les 1 052 personnes de a1. Si C2 tombe du cote de
    v8 et non du cote de v6, notre pipeline reproduit ce fait sur un autre modele et une
    autre invite, ce qui en fait un fait de generateur et non un accident d'archive.
    """
    print("\n" + "=" * 100)
    print("LE BON VIS A VIS DE C2 : gss_v8, ET NON gss_v6")
    print("v6 est un agent demographique SANS ideologie ni parti dans l'invite ;")
    print("v8 en est un AVEC. C2 porte les onze attributs, ideologie et parti compris.")
    print("Comparer C2 a v6 n'est pas une comparaison a armes egales.")
    print("=" * 100)
    out = {}
    ligne = {"C2": tab.get("C2 argmax"), "C2 distribution": tab.get("C2 distribution"),
             "gss_v8, avec ideologie": tab.get("agents v8"),
             "gss_v6, sans ideologie": tab.get("agents demographiques (v6)")}
    print(f"{'condition':<30}" + "".join(f"{a[:13]:>14}" for a in AXES))
    for nom, v in ligne.items():
        if v is None:
            continue
        print(f"{nom:<30}" + "".join(f"{v[a]:>14.2f}" for a in AXES))
        out[nom] = {a: v[a] for a in AXES}
    c2 = ligne.get("C2")
    v8 = ligne.get("gss_v8, avec ideologie")
    v6 = ligne.get("gss_v6, sans ideologie")
    if c2 and v8 and v6:
        a = "political_ideology"
        d8, d6 = abs(c2[a] - v8[a]), abs(c2[a] - v6[a])
        cote = "v8" if d8 < d6 else "v6"
        out["cote"] = cote
        print(f"\nsur l'axe ideologie, C2 vaut {c2[a]:.2f}, v8 vaut {v8[a]:.2f}, "
              f"v6 vaut {v6[a]:.2f}")
        print(f"C2 tombe du cote de {cote}.")
        if cote == "v8":
            print("Notre pipeline reproduit donc, sur un autre modele et une autre invite,")
            print("le fait etabli par a17 : ce qui separe v6 de v8 est la presence de")
            print("l'etiquette ideologique dans l'invite, et l'effet est de premier ordre.")
        else:
            print("C2 ne se comporte PAS comme v8 alors que son invite est du meme type.")
            print("C'est un desaccord a expliquer avant toute publication du contraste.")
    return out


# =======================================================================================
# La mesure a la Chen
# =======================================================================================

def mesure_chen(banc, T, valide_cell, ordinal_col, options, items_ev, jeux, noms,
                presents, sortie, plancher=0.05, seg_min=8):
    """Ecart max moins min de la proportion de modalite haute, et delta eta carre.

    Definition de la modalite haute, arXiv 2607.26348 section 3.3 : "the fraction of
    segment g on the high end of the answer scale". Les modalites d'un item ordinal sont
    codees 0..K-1 dans l'ordre du questionnaire puis ramenees dans [0, 1]. Est haute toute
    modalite de valeur STRICTEMENT superieure a 0,5, c'est a dire la moitie haute de
    l'echelle hors mediane. Pour K = 2 c'est la seconde modalite, pour K = 5 les deux
    dernieres.

    ecart_g = max_g p_g - min_g p_g, calcule par item et par axe.
    Le rapport publie est la MEDIANE sur les couples (item, axe) du rapport
    ecart_modele / ecart_humain, restreint aux couples ou l'ecart humain depasse un
    plancher, faute de quoi un ecart humain de 0,001 fabriquerait un rapport de 300.

    eta carre est la part de variance des reponses imputable au groupe, sur les memes
    items ordinaux, codage 0..1. Chen le publie en version plug in pour les humains et
    pour le modele et compare la difference : c'est cette version qui est calculee ici,
    pour rester sur la meme regle graduee que son tableau. delta eta carre = eta carre du
    modele moins eta carre des humains.

    SEUIL D'EFFECTIF DE SEGMENT, et il n'est pas cosmetique. Chen mesure sur 14 704
    repondants, nous sur 150 au plus. Un segment de deux personnes donne une proportion
    de modalite haute qui vaut 0, 0,5 ou 1 ; max moins min sature alors a 1 chez les
    humains COMME chez le modele et le rapport vaut mecaniquement 1. Sur les traces
    partielles cet artefact a ete constate : mediane de rapport egale a 1,0000 sur cinq
    axes a la fois. Les segments de moins de `seg_min` personnes sont donc ecartes, pour
    l'ecart comme pour eta carre, et le nombre de segments retenus est rapporte.
    """
    J, K = banc.J, banc.k_max
    haute = np.zeros((J, K), dtype=bool)
    val = np.zeros((J, K))
    for j, it in enumerate(items_ev):
        kj = len(options[it.lower()])
        if kj > 1:
            v = np.arange(kj) / (kj - 1)
            val[j, :kj] = v
            haute[j, :kj] = v > 0.5
    ord_ok = ordinal_col.astype(bool)

    # Segments retenus : ceux qui portent au moins seg_min personnes, effectif compte sur
    # les humains de la vague 1, donc identique pour toutes les conditions.
    axes_c = banc.axes_chen
    ref_c = compter_frac(T[REFERENCE], valide_cell, banc.W_chen)
    seg_garde = ref_c.sum(axis=3) >= seg_min          # (A, J, G)
    n_seg = [int(seg_garde[i].any(axis=0).sum()) for i in range(len(axes_c))]

    def stats(lib):
        c = compter_frac(T[lib], valide_cell, banc.W_chen)     # (A, J, G, K)
        c = c * seg_garde[:, :, :, None]
        n_g = c.sum(axis=3)
        with np.errstate(invalid="ignore", divide="ignore"):
            p_haut = (c * haute[None, :, None, :]).sum(axis=3) / np.where(n_g > 0, n_g, 1.0)
        vide = n_g <= 0
        ph = np.where(vide, np.nan, p_haut)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            ecart = np.nanmax(ph, axis=2) - np.nanmin(ph, axis=2)
        # eta carre plug in, sur le codage ordinal
        n_k = c.sum(axis=2)
        N = n_g.sum(axis=2)
        Ns = np.where(N > 0, N, 1.0)
        moy = (n_k * val[None, :, :]).sum(axis=2) / Ns
        sct = (n_k * (val ** 2)[None, :, :]).sum(axis=2) - Ns * moy ** 2
        moy_g = (c * val[None, :, None, :]).sum(axis=3) / np.where(n_g > 0, n_g, 1.0)
        sce = (n_g * (moy_g - moy[:, :, None]) ** 2).sum(axis=2)
        with np.errstate(invalid="ignore", divide="ignore"):
            eta = np.where(sct > 1e-12, sce / np.where(sct > 1e-12, sct, 1.0), np.nan)
        return ecart, eta

    ec_ref, eta_ref = stats(REFERENCE)
    l = [["condition", "version", "axe", "n_segments_retenus", "n_couples",
          "mediane_rapport_ecart", "mediane_delta_eta2", "part_cellules_positives"]]
    resume = {}
    print("\n" + "=" * 100)
    print("CONTRASTE 3 : LA MESURE A LA CHEN, arXiv 2607.26348")
    print("regle graduee de leur 2,3 : mediane du rapport d'ecart entre groupes")
    print(f"items ordinaux retenus : {int(ord_ok.sum())} sur {J} ; "
          f"segments d'au moins {seg_min} personnes seulement")
    print("segments retenus par axe : "
          + ", ".join(f"{a} {n}/{len(banc.niveaux_chen[a])}"
                      for a, n in zip(axes_c, n_seg)))
    print(f"plancher sur l'ecart humain : {plancher}")
    print("=" * 100)
    print(f"{'condition':<26}{'axe':<22}{'n':>6}{'rapport ecart':>16}{'delta eta2':>14}")
    for lib, cle, ver in jeux:
        if lib == REFERENCE:
            continue
        ec, eta = stats(lib)
        resume[lib] = {}
        for i, a in enumerate(axes_c):
            msk = ord_ok & np.isfinite(ec[i]) & np.isfinite(ec_ref[i]) & \
                (ec_ref[i] > plancher)
            msk_e = ord_ok & np.isfinite(eta[i]) & np.isfinite(eta_ref[i])
            if msk.sum() < 3:
                continue
            rap = float(np.median(ec[i][msk] / ec_ref[i][msk]))
            dlt = float(np.median(eta[i][msk_e] - eta_ref[i][msk_e]))
            pos = float(np.mean((eta[i][msk_e] - eta_ref[i][msk_e]) > 0))
            resume[lib][a] = {"rapport_ecart": rap, "delta_eta2": dlt}
            print(f"{lib:<26}{a:<22}{int(msk.sum()):>6}{rap:>16.3f}{dlt:>14.4f}")
            l.append([lib, ver, a, n_seg[i], int(msk.sum()), f"{rap:.4f}", f"{dlt:.4f}",
                      f"{pos:.4f}"])
    with open(os.path.join(sortie, "a18-chen.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(l)
    return {"resume": resume, "n_items_ordinaux": int(ord_ok.sum()),
            "seg_min": seg_min, "plancher_ecart_humain": plancher,
            "segments_retenus": dict(zip(axes_c, n_seg))}


# =======================================================================================
# Dispersion totale : decodage ou conditionnement
# =======================================================================================

def entropie_totale(P, valide_cell, k_par_item, occupation=1.0):
    """Somme sur les items de l'entropie du melange des distributions individuelles.

    C'est la dispersion TOTALE de la population predite, hors toute segmentation. Pour des
    reponses ponctuelles c'est l'entropie de la distribution marginale de l'item, corrigee
    par Miller Madow, exactement comme dans a1.
    """
    c = (P * valide_cell[:, :, None]).sum(axis=0)        # (J, K)
    N = c.sum(axis=1)
    Ns = np.where(N > 0, N, 1.0)
    p = c / Ns[:, None]
    h = -_xlogx(p).sum(axis=1)
    m = (c >= occupation).sum(axis=1)
    return h + (m - 1.0) / (2.0 * Ns * LN2), N


def rechauffer(P, tau, k_par_item):
    """Applique une temperature tau aux distributions individuelles : q proportionnel a p^(1/tau).

    tau = 1 rend P inchange. tau grand ecrase vers l'uniforme sur les K_j modalites de
    l'item. L'argmax est invariant par cette transformation, ce qui est le point : la
    temperature ne peut pas rendre le modele plus juste, elle ne peut que le rendre plus
    disperse.
    """
    n, J, K = P.shape
    dispo = np.zeros((J, K), dtype=bool)
    for j in range(J):
        dispo[j, :k_par_item[j]] = True
    with np.errstate(divide="ignore"):
        lg = np.where(P > 0, np.log(np.maximum(P, 1e-300)), -np.inf) / tau
    lg = np.where(dispo[None, :, :], lg, -np.inf)
    mx = np.max(np.where(np.isfinite(lg), lg, -np.inf), axis=2, keepdims=True)
    mx = np.where(np.isfinite(mx), mx, 0.0)      # cellule entierement vide
    e = np.where(np.isfinite(lg), np.exp(lg - mx), 0.0)
    s = e.sum(axis=2, keepdims=True)
    return np.where(s > 0, e / np.where(s > 0, s, 1.0), 0.0)


def entropie_individuelle(P, valide_cell):
    """Entropie moyenne de la distribution d'une cellule, en bits, et le vecteur complet."""
    with np.errstate(divide="ignore", invalid="ignore"):
        h = -np.where(P > 0, P * np.log2(np.maximum(P, 1e-300)), 0.0).sum(axis=2)
    v = h[valide_cell > 0]
    return float(v.mean()) if v.size else float("nan"), v


def dispersion_totale(banc, T, P, valide_cell, presents, sortie):
    """Les trois versions du ratio de dispersion totale, question 3 de a7 section 10.

    Version 1, ARGMAX : la reponse du modele est durcie, comme une reponse humaine. C'est
      le T de a7 section 0, celui qui vaut 0,80 a 0,89 pour les conditions de Stanford.

    Version 2, TIRAGE : au lieu de durcir, on tire la reponse de chaque personne dans sa
      propre distribution. La distribution de population qui en resulte a pour ESPERANCE
      exacte le melange des distributions individuelles : E[n_k]/N = moyenne_i p_ik. On
      calcule donc l'entropie de ce melange, ce qui est l'esperance analytique demandee et
      non un tirage. Reserve a ecrire : l'entropie de la distribution esperee n'est pas
      l'esperance de l'entropie d'un tirage fini ; la seconde est legerement plus basse,
      d'un terme d'ordre (m - 1) / (2 N ln 2) que la correction de Miller Madow chiffre
      deja et qui est ici de l'ordre du centieme de bit.

    Version 3, BORNE EN TEMPERATURE : on cherche le scalaire tau tel que le ratio de
      dispersion totale de la version tirage atteigne 1. On rapporte tau, l'entropie
      individuelle moyenne qu'il exige, et ce que devient le ratio inter a ce reglage.
      L'argmax etant invariant par temperature, l'exactitude argmax ne bouge pas ; c'est
      l'exactitude esperee qui paie.

    LECTURE. Si le ratio de la version tirage reste loin de 1, le deficit de dispersion
    totale n'est pas dans le decodage, il est dans le modele : lire les logits au lieu de
    durcir ne le comble pas.
    """
    print("\n" + "=" * 100)
    print("QUESTION 3 DE a7 : LE DEFICIT DE DISPERSION TOTALE EST IL DANS LE DECODAGE ?")
    print("=" * 100)
    h_ref, _ = entropie_totale(T[REFERENCE], valide_cell, banc.k_par_item)
    tot_ref = float(h_ref.sum())
    l = [["condition", "version", "dispersion_totale_bits", "ratio_total",
          "entropie_individuelle_moyenne_bits", "tau", "exactitude_esperee"]]
    out = {"total_humain_bits": tot_ref}
    for nom in [REFERENCE, "humains vague 2"]:
        if nom not in T:
            continue
        h, _ = entropie_totale(T[nom], valide_cell, banc.k_par_item)
        l.append([nom, "ponctuelle", f"{h.sum():.4f}", f"{h.sum() / tot_ref:.4f}",
                  "0.0000", "", ""])
    print(f"{'condition':<14}{'version':<26}{'total bits':>12}{'ratio':>9}"
          f"{'H individuelle':>16}{'tau':>8}")
    for c in sorted(presents):
        # Voie argmax : la distribution est durcie, comme une reponse humaine.
        h_arg, _ = entropie_totale(T[f"{c} argmax"], valide_cell, banc.k_par_item)
        r_arg = float(h_arg.sum()) / tot_ref
        h_dis, _ = entropie_totale(P[c], valide_cell, banc.k_par_item)
        r_dis = float(h_dis.sum()) / tot_ref
        hi, _ = entropie_individuelle(P[c], valide_cell)
        print(f"{c:<14}{'1 argmax':<26}{h_arg.sum():>12.2f}{r_arg:>9.3f}"
              f"{0.0:>16.4f}{'':>8}")
        print(f"{c:<14}{'2 tirage, esperance':<26}{h_dis.sum():>12.2f}{r_dis:>9.3f}"
              f"{hi:>16.4f}{1.0:>8.2f}")
        l.append([c, "1 argmax", f"{h_arg.sum():.4f}", f"{r_arg:.4f}", "0.0000", "", ""])
        l.append([c, "2 tirage esperance", f"{h_dis.sum():.4f}", f"{r_dis:.4f}",
                  f"{hi:.4f}", "1.0", ""])
        # version 3 : bisection sur log tau
        def ratio(tau):
            Q = rechauffer(P[c], tau, banc.k_par_item)
            h, _ = entropie_totale(Q, valide_cell, banc.k_par_item)
            return float(h.sum()) / tot_ref
        lo, hi_t = 1.0, 1.0
        if r_dis < 1.0:
            hi_t = 1.0
            for _ in range(40):
                hi_t *= 1.6
                if ratio(hi_t) >= 1.0:
                    break
            lo = hi_t / 1.6
        else:
            lo = 1.0
            for _ in range(40):
                lo /= 1.6
                if ratio(lo) <= 1.0:
                    break
            hi_t = lo * 1.6
        for _ in range(45):
            mid = math.sqrt(lo * hi_t)
            if ratio(mid) < 1.0:
                lo = mid
            else:
                hi_t = mid
        tau = math.sqrt(lo * hi_t)
        Q = rechauffer(P[c], tau, banc.k_par_item)
        h3, _ = entropie_totale(Q, valide_cell, banc.k_par_item)
        hi3, _ = entropie_individuelle(Q, valide_cell)
        print(f"{c:<14}{'3 borne en temperature':<26}{h3.sum():>12.2f}"
              f"{h3.sum() / tot_ref:>9.3f}{hi3:>16.4f}{tau:>8.2f}")
        l.append([c, "3 borne en temperature", f"{h3.sum():.4f}",
                  f"{h3.sum() / tot_ref:.4f}", f"{hi3:.4f}", f"{tau:.4f}", ""])
        out[c] = {"ratio_argmax": r_arg, "ratio_tirage": r_dis,
                  "entropie_individuelle_bits": hi, "tau_pour_ratio_1": tau,
                  "entropie_individuelle_requise_bits": hi3}
    print("\nLecture. Si le ratio de la version tirage reste loin de 1, le deficit n'est")
    print("pas dans le decodage : lire les logits au lieu de durcir ne le comble pas,")
    print("il faut un modele different ou un conditionnement different.")
    with open(os.path.join(sortie, "a18-dispersion-totale.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(l)
    return out


def _degenerer(P):
    """Durcit un tenseur de distributions par argmax, en gardant sa forme."""
    n, J, K = P.shape
    D = np.zeros_like(P)
    s = P.sum(axis=2)
    ii, jj = np.where(s > 0)
    D[ii, jj, np.argmax(P[ii, jj], axis=1)] = 1.0
    return D


# =======================================================================================
# Calibration
# =======================================================================================

def ecrire_calibration(calib, P, valide_cell, banc, sortie):
    print("\n" + "=" * 100)
    print("ENTROPIE INDIVIDUELLE ET CALIBRATION")
    print("=" * 100)
    l = [["condition", "bloc", "cle", "valeur"]]
    for c, m in calib.items():
        if not m:
            continue
        _, v = entropie_individuelle(P[c], valide_cell)
        q = np.percentile(v, [0, 10, 25, 50, 75, 90, 100]) if v.size else [np.nan] * 7
        print(f"\n  {c} sur {m['n_cellules']} cellules")
        print(f"    exactitude esperee {m['exactitude_esperee']:.4f}, "
              f"exactitude argmax implicite dans le tableau recapitulatif")
        print(f"    entropie individuelle moyenne {m['entropie_moyenne_bits']:.4f} bits "
              f"sur un maximum moyen de {m['entropie_maximale_moyenne_bits']:.4f}, "
              f"soit {m['part_entropie_maximale'] * 100:.1f} pour cent")
        print("    deciles de l'entropie individuelle  "
              + "  ".join(f"{x:.3f}" for x in q))
        print(f"    part des cellules a p max > 0,99 : "
              f"{m['part_cellules_quasi_certaines'] * 100:.1f} pour cent")
        print(f"    ecart de calibration attendu (ECE) : "
              f"{m['ecart_de_calibration_attendu']:.4f}")
        print(f"    {'decile':<12}{'n':>8}{'confiance':>12}{'exactitude':>12}{'ecart':>10}")
        for d in m["calibration_par_decile"]:
            print(f"    {d['decile']:<12}{d['n']:>8}{d['confiance_moyenne']:>12.4f}"
                  f"{d['exactitude_reelle']:>12.4f}{d['ecart']:>10.4f}")
        for k, val in m.items():
            if k == "calibration_par_decile":
                continue
            l.append([c, "resume", k, f"{val:.6f}" if isinstance(val, float) else val])
        for nom, x in zip(["q0", "q10", "q25", "q50", "q75", "q90", "q100"], q):
            l.append([c, "entropie_individuelle_percentile", nom, f"{x:.6f}"])
        for d in m["calibration_par_decile"]:
            l.append([c, "calibration", d["decile"],
                      f"n={d['n']};conf={d['confiance_moyenne']:.4f};"
                      f"exact={d['exactitude_reelle']:.4f};ecart={d['ecart']:.4f}"])
    with open(os.path.join(sortie, "a18-calibration.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(l)


# =======================================================================================
# Critere A6 en version positive
# =======================================================================================

def critere_a6(banc, codes, brut, verite, verite2, noms, presents, seg, lignes, sortie):
    """La variance intra que C3 possede en plus de C2 est elle informative ?

    a7 a pose le critere A6 en version negative : quand on FABRIQUE de la variance intra,
    les individus deplaces ne se rapprochent pas de leur vraie reponse. Ici la version
    positive : la variance intra que le modele produit SPONTANEMENT est elle placee sur
    les bons individus ?

    Protocole. Pour chaque personne, on mesure sa DEVIANCE : la part des items ou sa
    reponse s'ecarte du mode de son segment. Le mode est calcule sur les humains de la
    vague 1, en LAISSANT LA PERSONNE DE COTE, sans quoi une personne influencerait son
    propre mode et les deviances seraient mecaniquement correlees a la taille du segment.
    On correle ensuite, sur les personnes, la deviance de l'agent et la deviance de la
    vraie personne. Une correlation positive dit que l'agent s'ecarte du stereotype de
    groupe pour les memes personnes qui s'en ecartent reellement. Une correlation nulle
    dit que sa variance intra est du bruit place au hasard.

    Le controle est la vague 2 : les memes personnes deux semaines plus tard, dont la
    deviance doit etre fortement correlee a celle de la vague 1.

    On ajoute le r entre exactitude par personne et consistance test retest de la personne,
    que a1 section 6 trouve a 0,684 pour les agents composite sur les 1 052 personnes.
    """
    print("\n" + "=" * 100)
    print("CRITERE A6 EN VERSION POSITIVE : la variance intra est elle informative ?")
    print("=" * 100)
    l = [["condition", "axe", "n_personnes", "r_pearson_deviance", "r_spearman_deviance",
          "deviance_moyenne_agent", "deviance_moyenne_humaine",
          "r_exactitude_consistance"]]
    out = {}

    x_ref = codes[REFERENCE]
    valide = x_ref >= 0
    retest = exactitude_par_personne(verite2, verite)

    for axe in ("political_ideology", "profil croise"):
        g = seg[axe][lignes]
        # mode par (segment, item) sur les humains vague 1, en laissant la personne de cote
        G = int(g.max()) + 1 if g.size else 0
        K = banc.k_max
        eff = np.zeros((G, banc.J, K))
        for k in range(K):
            m = (x_ref == k) & valide
            for gg in range(G):
                eff[gg, :, k] = m[g == gg].sum(axis=0)

        def deviance(x):
            """Part des items ou la reponse s'ecarte du mode de son segment, hors soi."""
            d = np.full(banc.n, np.nan)
            for i in range(banc.n):
                gg = g[i]
                if gg < 0:
                    continue
                e = eff[gg].copy()
                # retrait de la personne elle meme, uniquement de la table humaine
                for j in range(banc.J):
                    if valide[i, j]:
                        e[j, x_ref[i, j]] -= 1.0
                mode = np.argmax(e, axis=1)
                ok = (x[i] >= 0) & (e.sum(axis=1) > 0)
                if ok.sum() == 0:
                    continue
                d[i] = float((x[i][ok] != mode[ok]).mean())
            return d

        d_hum = deviance(x_ref)
        for nom in noms:
            if nom == REFERENCE:
                continue
            d_ag = deviance(codes[nom])
            ok = np.isfinite(d_ag) & np.isfinite(d_hum)
            if ok.sum() < 5:
                continue
            r = float(np.corrcoef(d_ag[ok], d_hum[ok])[0, 1])
            rs = float(_spearman(d_ag[ok], d_hum[ok]))
            acc = exactitude_par_personne(np.where(valide, brut[nom], None),
                                          np.where(valide, verite, None), valide)
            ok2 = np.isfinite(acc) & np.isfinite(retest)
            r_ac = float(np.corrcoef(acc[ok2], retest[ok2])[0, 1]) if ok2.sum() > 5 \
                else float("nan")
            l.append([nom, axe, int(ok.sum()), f"{r:.4f}", f"{rs:.4f}",
                      f"{np.nanmean(d_ag):.4f}", f"{np.nanmean(d_hum):.4f}",
                      f"{r_ac:.4f}"])
            out.setdefault(axe, {})[nom] = {"r_deviance": r, "rho_deviance": rs,
                                            "deviance_agent": float(np.nanmean(d_ag)),
                                            "deviance_humaine": float(np.nanmean(d_hum)),
                                            "r_exactitude_consistance": r_ac}
        print(f"\n  axe {axe}, deviance au mode de segment, mode calcule hors soi")
        print(f"  {'condition':<26}{'r':>9}{'rho':>9}{'dev agent':>12}"
              f"{'dev humaine':>13}{'r exact/consist':>17}")
        for nom, v in out.get(axe, {}).items():
            print(f"  {nom:<26}{v['r_deviance']:>9.3f}{v['rho_deviance']:>9.3f}"
                  f"{v['deviance_agent']:>12.3f}{v['deviance_humaine']:>13.3f}"
                  f"{v['r_exactitude_consistance']:>17.3f}")
    with open(os.path.join(sortie, "a18-critere-a6.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(l)
    return out


def _spearman(a, b):
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    return np.corrcoef(ra, rb)[0, 1]


# =======================================================================================
# Le tableau recapitulatif
# =======================================================================================

def recapitulatif(brut, verite, verite2, masque, calib, ratios, tab_axe, globaux, noms,
                  presents, sortie):
    """Le tableau du papier. Une ligne par condition, huit colonnes.

    exactitude esperee : pour les conditions sans distribution elle est egale a
    l'exactitude argmax par construction, une reponse ponctuelle etant une distribution
    de Dirac. La colonne n'est donc informative que pour C2 et C3, et c'est ecrit.
    """
    print("\n" + "=" * 100)
    print("TABLEAU RECAPITULATIF")
    print("=" * 100)
    # L'invite contient elle l'etiquette ideologique ? Fait etabli par a17 objection 3 a
    # partir des taux de recopie du paquet OSF : v6 ne l'a pas, v8 l'a. C2 l'a. C'est la
    # colonne qui dit avec qui chaque ligne est comparable. Pour les conditions riches en
    # reponses reelles la question ne se pose pas de la meme facon, l'invite ne porte pas
    # d'etiquette et le modele peut reconstruire l'ideologie.
    ETIQUETTE = {
        "humains vague 2": "sans objet",
        "C2": "oui, dans l'invite", "C3": "non, a reconstruire",
        "agents composite": "non, a reconstruire",
        "agents entretien (v3)": "non, a reconstruire",
        "agents enquete": "non, a reconstruire",
        "agents demographiques (v6)": "non",
        "agents v7": "inconnu", "agents v8": "oui, dans l'invite",
    }
    l = [["condition", "ideologie_dans_l_invite", "exactitude_argmax", "ic_bas",
          "ic_haut", "exactitude_esperee", "ratio_inter_ideologie", "ratio_inter_genre",
          "ratio_intra", "ratio_total", "diversite_conservee", "accord_par_paires"]]
    out = {}
    print("colonne ideologie : l'etiquette ideologique est elle dans l'invite ?")
    print("v6 ne l'a pas, v8 l'a, C2 l'a. C2 se compare a v8, pas a v6. [CONFIRME, a17]")
    print(f"{'condition':<26}{'ideologie':<21}{'exact.':>8}{'esperee':>9}"
          f"{'inter ideo':>12}{'inter genre':>13}{'intra':>8}{'total':>8}"
          f"{'diversite':>11}{'accord':>9}")
    # C2 et son homologue v8 sont mis cote a cote, C3 et les conditions riches ensuite.
    prio = ["humains vague 2", "C2", "agents v8", "C3", "agents composite",
            "agents enquete", "agents entretien (v3)", "agents demographiques (v6)",
            "agents v7"]
    ordre = [n for n in prio if n in noms and n != REFERENCE]
    ordre += [n for n in noms if n != REFERENCE and n not in ordre]
    for nom in ordre:
        pred = np.where(masque, brut[nom], None)
        ver = np.where(masque, verite, None)
        acc = exactitude_par_personne(pred, ver, masque)
        moy, bas, haut = bootstrap_personnes(acc)
        div = profil_diversite(pred, ver)
        lib = f"{nom} argmax" if nom in presents else nom
        esp = calib.get(nom, {}).get("exactitude_esperee", moy) if nom in presents else moy
        r_ideo = tab_axe[lib]["political_ideology"]
        r_gen = tab_axe[lib]["gender"]
        r_intra = ratios[lib]["entropie"][1]
        r_tot = globaux[lib]["entropie"]
        etiq = ETIQUETTE.get(nom, "inconnu")
        print(f"{nom:<26}{etiq:<21}{moy:>8.4f}{esp:>9.4f}{r_ideo:>12.2f}{r_gen:>13.2f}"
              f"{r_intra:>8.3f}{r_tot:>8.3f}{div['part_diversite_humaine'] * 100:>10.1f}%"
              f"{div['accord_par_paires'] * 100:>8.1f}%")
        l.append([nom, etiq, f"{moy:.4f}", f"{bas:.4f}", f"{haut:.4f}", f"{esp:.4f}",
                  f"{r_ideo:.4f}", f"{r_gen:.4f}", f"{r_intra:.4f}", f"{r_tot:.4f}",
                  f"{div['part_diversite_humaine']:.4f}",
                  f"{div['accord_par_paires']:.4f}"])
        out[nom] = {"exactitude": moy, "exactitude_esperee": esp,
                    "ratio_inter_ideologie": r_ideo, "ratio_inter_genre": r_gen,
                    "ratio_intra": r_intra, "ratio_total": r_tot,
                    "diversite": div["part_diversite_humaine"],
                    "accord": div["accord_par_paires"]}
        if nom in presents:
            lib_d = f"{nom} distribution"
            l.append([f"{nom} (version distributionnelle)", ETIQUETTE.get(nom, ""),
                      "", "", "", "",
                      f"{tab_axe[lib_d]['political_ideology']:.4f}",
                      f"{tab_axe[lib_d]['gender']:.4f}",
                      f"{ratios[lib_d]['entropie'][1]:.4f}",
                      f"{globaux[lib_d]['entropie']:.4f}", "", ""])
    # plafond humain, pour memoire
    accr = exactitude_par_personne(np.where(masque, verite2, None),
                                   np.where(masque, verite, None), masque)
    m, b, h = bootstrap_personnes(accr)
    print(f"\nplafond humain test retest de ces personnes sur ces items : "
          f"{m:.4f} [{b:.4f} ; {h:.4f}]")
    l.append(["plafond humain test retest", "sans objet", f"{m:.4f}", f"{b:.4f}",
              f"{h:.4f}", "", "", "", "", "", "", ""])
    out["plafond_humain"] = m
    with open(os.path.join(sortie, "a18-recapitulatif.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(l)
    return out


# =======================================================================================
# La figure
# =======================================================================================

def tracer(ratios, ic_ratios, globaux, jeux, presents, sortie, n_pers, n_items,
           mesure="entropie"):
    """Le plan (inter, intra), C2 et C3 en deux versions a cote des six de Stanford."""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        print("matplotlib absent, figure non produite.")
        return

    style = {
        REFERENCE: ("o", "white", 15),
        "humains vague 2": ("s", "white", 10),
        "agents composite": ("^", "black", 12),
        "agents entretien (v3)": ("v", "black", 12),
        "agents enquete": ("D", "0.35", 10),
        "agents demographiques (v6)": ("X", "0.75", 14),
        "agents v7": ("P", "0.75", 14),
        "agents v8": ("*", "0.75", 19),
        "C2 argmax": ("h", "#c0392b", 14),
        "C2 distribution": ("h", "white", 14),
        "C3 argmax": ("8", "#1f4e79", 14),
        "C3 distribution": ("8", "white", 14),
    }
    libs = [l for l, _, _ in jeux]
    xs = [ratios[l][mesure][0] for l in libs]
    ys = [ratios[l][mesure][1] for l in libs]
    xs = [v for v in xs if v > 0]
    ys = [v for v in ys if v > 0]
    if not xs or not ys:
        print("ratios non exploitables, figure non produite.")
        return
    fig, ax = plt.subplots(figsize=(11.5, 8.0))
    x_lo, x_hi = min(xs) * 0.45, max(xs) * 2.4
    y_lo, y_hi = min(ys) * 0.88, max(ys) * 1.25

    ax.fill_between([1.0, x_hi], y_lo, 1.0, color="0.91", zorder=0)
    ax.text(x_hi * 0.97, y_lo * 1.02, "quadrant de la double distorsion :\n"
            "ecarts entre groupes gonfles, dispersion interne ecrasee",
            ha="right", va="bottom", fontsize=9.5, color="0.30", zorder=1)
    t = np.geomspace(x_lo, x_hi, 400)
    ax.plot(t, 1.0 / t, color="black", lw=1.6, ls="--", zorder=2,
            label="produit des deux ratios egal a 1 :\nfaux deux fois, invisible sur une "
                  "mesure globale")
    ax.axhline(1.0, color="0.5", lw=0.9, zorder=1)
    ax.axvline(1.0, color="0.5", lw=0.9, zorder=1)

    # Les fleches relient les deux versions d'une meme condition : c'est le contraste 2
    # de a15, argmax contre distribution, a modele, temperature et donnees constants.
    for c in presents:
        a, b = f"{c} argmax", f"{c} distribution"
        if a in ratios and b in ratios:
            ax.annotate("", xy=(ratios[b][mesure][0], ratios[b][mesure][1]),
                        xytext=(ratios[a][mesure][0], ratios[a][mesure][1]),
                        arrowprops=dict(arrowstyle="->", lw=1.6, color="0.25"), zorder=3)

    # Decalages d'etiquette en points typographiques, un par condition, pour que les
    # douze etiquettes ne se recouvrent pas. Meme principe que a1.
    decal = {
        REFERENCE: (-16, 14, "right"), "humains vague 2": (16, 10, "left"),
        "agents composite": (-14, 16, "right"), "agents entretien (v3)": (16, 4, "left"),
        "agents enquete": (-14, -16, "right"),
        "agents demographiques (v6)": (0, -22, "center"),
        "agents v7": (0, 20, "center"), "agents v8": (14, 16, "left"),
        "C2 argmax": (-14, -16, "right"), "C2 distribution": (14, 14, "left"),
        "C3 argmax": (-14, 16, "right"), "C3 distribution": (14, -16, "left"),
    }
    for lib in libs:
        ri, ra = ratios[lib][mesure]
        (i1, i2), (a1_, a2_) = ic_ratios[lib][mesure]
        mk, coul, taille = style.get(lib, ("o", "0.5", 10))
        # L'intervalle du terme inter explose des que le denominateur bootstrap approche
        # zero. On ne trace que sa partie lisible, bornee par le cadre, et on ne trace
        # rien quand la borne basse est negative : une barre qui sort du cadre ferait
        # croire a une precision qui n'existe pas. Le CSV porte les valeurs completes.
        if np.isfinite(i1) and i1 > 0 and (i2 - i1) > 1e-9:
            ax.plot([max(i1, x_lo), min(i2, x_hi)], [ra, ra], color="0.35", lw=1.0,
                    zorder=3, alpha=0.8)
        if np.isfinite(a1_) and (a2_ - a1_) > 1e-9:
            ax.plot([ri, ri], [max(a1_, y_lo), min(a2_, y_hi)], color="0.35", lw=1.0,
                    zorder=3, alpha=0.8)
        ax.plot(ri, ra, marker=mk, ms=taille, mfc=coul, mec="black", mew=1.3,
                ls="none", zorder=4)
        dx, dy, ha = decal.get(lib, (0, 15, "center"))
        ax.annotate(f"{lib}\nmesure globale : {globaux[lib][mesure]:.2f}", (ri, ra),
                    textcoords="offset points", xytext=(dx, dy), ha=ha,
                    va="center", fontsize=8.5, zorder=5, linespacing=1.3,
                    bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="0.8", lw=0.5,
                              alpha=0.90))

    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xlim(x_lo, x_hi); ax.set_ylim(y_lo, y_hi)
    tx = [v for v in (0.2, 0.3, 0.5, 0.7, 1.0, 1.5, 2, 3, 5, 8, 12) if x_lo <= v <= x_hi]
    ty = [v for v in (0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1, 1.2)
          if y_lo <= v <= y_hi]
    ax.set_xticks(tx); ax.set_yticks(ty)
    ax.set_xticklabels([f"{v:g}" for v in tx])
    ax.set_yticklabels([f"{v:g}" for v in ty])
    ax.minorticks_off()
    ax.set_xlabel("Ratio de dispersion ENTRE segments demographiques   "
                  "(condition / humains vague 1)", fontsize=11)
    ax.set_ylabel("Ratio de dispersion A L'INTERIEUR des segments\n"
                  "(condition / humains vague 1)", fontsize=11)
    ax.set_title("C2 et C3 dans le plan de la double distorsion, en deux versions\n"
                 f"GSS, {n_pers} personnes du run a5, {n_items} items, 6 segmentations, "
                 "entropie a biais corrige\n"
                 "la fleche relie l'argmax a la distribution complete de la meme condition",
                 fontsize=11.5)
    ax.grid(True, which="major", color="0.88", lw=0.6)
    ax.set_axisbelow(True)
    ax.legend(loc="lower left", fontsize=8.5, framealpha=0.95)
    fig.tight_layout()
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(sortie, f"a18-figure-c2-c3.{ext}"), dpi=200)
    plt.close(fig)


if __name__ == "__main__":
    main()
