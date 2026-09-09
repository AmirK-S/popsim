"""
i3b_commun : briques du mois 1 du programme B. Abaque du plus petit taux detectable par
taille de flux, transport de la bande humaine sur Twin-2K-500, contamination concentree sur
un camp, fabricant qui vise la bande, surface d'attaque.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. AUCUN SCRIPT EXISTANT N'EST MODIFIE. Sont importes tels quels i3_commun, et par lui
a44_commun, a28_commun, a29_commun, a31_commun, a35_commun, a2_commun, a8_commun ; plus
a6_double_distorsion_hors_gss pour le seul chargeur de Twin-2K-500, et a2_commun pour la
distance de Hamming.

LE PREENREGISTREMENT EST resultats/i3b-preenregistrement.md, ECRIT AVANT CE FICHIER,
le 8 septembre 2026 a 21 h 05 CEST, empreinte SHA-256
57f921196aef0789bc17d63ef4d2ebbffa5d95c8c0bb78b5c31497d734781168.

Ce module porte huit choses et rien d'autre.

  1. Le chargement du paquet GSS (par i3_commun) et du paquet Twin (par a6).
  2. Le sous echantillonnage EMBOITE d'un flux, qui donne l'abaque a taille variable.
  3. Le bruit de reference s0(N) avec correction de population finie (preenr. section 4).
  4. Les deux statistiques de RESERVE, R1 ordre trois et R2 plus proche voisin humain
     (preenr. section 3.2).
  5. Le melange concentre sur un bloc ideologique (preenr. section 6).
  6. Le fabricant qui vise la bande, A* archetypes, et sa variante a microdonnees
     (preenr. section 7).
  7. Les trois marginales de consequence (preenr. section 3.3).
  8. Les seuils z par famille et les outils d'ajustement, repris de i3_commun.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

from math import erfc, sqrt

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a44_commun as C44
import i3_commun as I
from a2_commun import distance_hamming

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = I.GRAINE                      # 20260909, la graine du projet
TAILLES_MESUREES = [300, 500, 750, 1052]
TAILLES_EXTRAPOLEES = [1500, 2000, 3000, 5000]
N_TRIPLETS = 20000                     # T de la statistique R1
N_MIN_TRIPLET = 30                     # personnes completes minimales pour un triplet
Z_PUISSANCE = I.Z_PUISSANCE            # 0,8416, puissance 80 pour cent


# ---------------------------------------------------------------------------
# 0. Seuils z par famille (preenregistrement section 5)
# ---------------------------------------------------------------------------

def z_holm(k, alpha=0.05):
    """Quantile normal bilateral du seuil de Bonferroni Holm le plus severe d'une famille
    de k tests : quantile de 1 - alpha / (2 k). Bissection, sans scipy."""
    cible = 1.0 - alpha / (2.0 * k)
    bas, haut = 0.0, 10.0
    for _ in range(200):
        mil = 0.5 * (bas + haut)
        phi = 1.0 - 0.5 * erfc(mil / sqrt(2.0))
        if phi < cible:
            bas = mil
        else:
            haut = mil
    return 0.5 * (bas + haut)


Z_F1 = z_holm(3)        # 2,394, l'auditeur reel : trois statistiques sur un fichier
Z_I3 = 3.113            # le seuil de i3, famille de 27, publie a cote pour comparaison
Z_F2 = z_holm(39)       # Twin, 3 statistiques x 13 configurations
Z_F3 = z_holm(5)        # 2,576, le fabricant qui vise la bande, publiees + reserve


def p_bilateral(z):
    return I.p_bilateral_normale(z)


holm = I.holm
benjamini_hochberg = I.benjamini_hochberg
ajuster_courbe = I.ajuster_courbe
racine_courbe = I.racine_courbe
inverser_courbe = I.inverser_courbe
ecrire = I.ecrire


# ---------------------------------------------------------------------------
# 1. Sous echantillonnage emboite
# ---------------------------------------------------------------------------

def ordre_emboite(n, rng):
    """Une permutation des n lignes. Le sous echantillon de taille N est ses N premiers
    elements, donc les sous echantillons sont emboites : celui a 300 est inclus dans celui
    a 500. Preenregistrement section 6."""
    return rng.permutation(n)


def restreindre(codes, seg, blocs, idx):
    """Le flux, la segmentation et les blocs restreints aux lignes idx."""
    return codes[idx], seg[idx], (blocs[idx] if blocs is not None else None)


# ---------------------------------------------------------------------------
# 2. Le bruit de reference a la taille N, avec correction de population finie
# ---------------------------------------------------------------------------

def correction_population_finie(m, n_pop):
    """1 / racine(1 - m / n_pop). Var d'un tirage sans remise = (S^2/m)(1 - m/n_pop) ; le
    sous echantillonnage sous estime donc le bruit d'un echantillon frais de taille m, et
    ce facteur le retablit. Preenregistrement section 4."""
    r = 1.0 - float(m) / float(n_pop)
    return float("inf") if r <= 0 else 1.0 / np.sqrt(r)


def ic_pivote(tirages, centre, echelle=1.0):
    """IC a 95 pour cent par sous echantillonnage pivote sur la MOYENNE des tirages,
    correctif E2 de i3, avec mise a l'echelle. Renvoie (bas, haut, ecart type)."""
    return I.ic_percentile(tirages, centre=centre, echelle=echelle)


# ---------------------------------------------------------------------------
# 3. Les deux statistiques de reserve
# ---------------------------------------------------------------------------

def triplets(n_items, n_triplets=N_TRIPLETS, graine=GRAINE):
    """T triplets d'items distincts, tires une fois pour toutes a la graine du projet."""
    rng = np.random.default_rng([graine, 3])
    out = np.empty((n_triplets, 3), dtype=np.int32)
    k = 0
    while k < n_triplets:
        t = rng.integers(0, n_items, size=(n_triplets - k, 3))
        bon = (t[:, 0] != t[:, 1]) & (t[:, 0] != t[:, 2]) & (t[:, 1] != t[:, 2])
        pris = t[bon]
        out[k:k + len(pris)] = pris
        k += len(pris)
    return out


def rangs_standardises(codes, seg):
    """Rangs residualises du segment puis standardises colonne par colonne.

    Renvoie (Z, W) : Z de forme (n, m) avec 0 sur les cellules non exploitables, W le
    masque en flottant. Mettre 0 et non NaN rend le produit d'un triplet automatiquement
    nul pour une personne incomplete, ce qui evite tout traitement de NaN dans R1.
    """
    r = C44.rangs_colonne(codes).astype(np.float64)
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
    w = (~np.isnan(r)).astype(np.float64)
    z = np.where(np.isnan(r), 0.0, r)
    n_obs = w.sum(axis=0)
    moy = np.divide(z.sum(axis=0), np.maximum(n_obs, 1.0))
    z = np.where(w > 0, z - moy[None, :], 0.0)
    var = np.divide((z ** 2).sum(axis=0), np.maximum(n_obs - 1.0, 1.0))
    et = np.sqrt(np.maximum(var, 0.0))
    bon = et > 1e-12
    z[:, bon] = z[:, bon] / et[None, bon]
    z[:, ~bon] = 0.0
    w[:, ~bon] = 0.0
    return z.astype(np.float32), w.astype(np.float32)


def r1_ordre_trois(codes, seg, trip, bloc=4000, n_min=N_MIN_TRIPLET):
    """R1 : moyenne des |E[z_i z_j z_k]| sur les triplets d'items declares.

    Sous tout modele a dependance purement de paires, chaque terme a une esperance nulle ;
    R1 mesure donc la structure a l'ordre trois. Comme B, elle est publiee en EXCES sur le
    generateur nul du flux, ce qui retire le plancher d'echantillonnage.
    """
    z, w = rangs_standardises(codes, seg)
    valeurs = []
    for d in range(0, len(trip), bloc):
        t = trip[d:d + bloc]
        pz = z[:, t[:, 0]] * z[:, t[:, 1]] * z[:, t[:, 2]]
        pw = w[:, t[:, 0]] * w[:, t[:, 1]] * w[:, t[:, 2]]
        num = pz.sum(axis=0)
        den = pw.sum(axis=0)
        ok = den >= n_min
        if ok.any():
            valeurs.append(np.abs(num[ok] / den[ok]))
    if not valeurs:
        return np.nan, 0
    v = np.concatenate(valeurs)
    return float(v.mean()), int(len(v))


def r2_plus_proche_voisin(codes_flux, codes_reference):
    """R2 : moyenne des distances de Hamming au plus proche voisin de l'echantillon humain
    de reference, disjoint du flux. Renvoie aussi le dixieme percentile, publie sans test.

    a2_commun.distance_hamming est importee telle quelle : cellules manquantes d'un cote
    ou de l'autre ignorees, denominateur = items renseignes chez les deux personnes.
    """
    d = distance_hamming(codes_flux.astype(np.int32), codes_reference.astype(np.int32))
    proche = d.min(axis=1)
    return float(proche.mean()), float(np.percentile(proche, 10))


# ---------------------------------------------------------------------------
# 4. Melange concentre sur un bloc ideologique
# ---------------------------------------------------------------------------

def flux_concentre(codes_humain, codes_source, lignes_possibles, blocs, camp, tau, rng):
    """Melange dont les faux repondants sont TOUS du bloc vise.

    tau reste la part du FLUX ENTIER remplacee. Leve ValueError si le bloc ne contient pas
    assez de personnes couvertes par la source. Preenregistrement section 6.
    """
    n = codes_humain.shape[0]
    k = int(round(tau * n))
    eligibles = np.intersect1d(np.asarray(lignes_possibles),
                               np.flatnonzero(blocs == camp))
    if k > len(eligibles):
        raise ValueError(f"camp {camp} : {k} lignes demandees pour {len(eligibles)} "
                         "disponibles")
    out = codes_humain.copy()
    if k <= 0:
        return out, np.zeros(0, dtype=np.int64)
    choisies = rng.choice(eligibles, size=k, replace=False)
    out[choisies] = codes_source[choisies]
    return out, choisies


# ---------------------------------------------------------------------------
# 5. Le fabricant qui vise la bande
# ---------------------------------------------------------------------------

def lois_p(codes, seg, k_items, beta=1.0, n_min=C44.N_MIN_SEGMENT):
    """Marginales p_{j,g} elevees a la puissance beta et renormalisees, sous forme
    cumulee, pretes pour un tirage. Ce sont les seules donnees dont A* a besoin : des
    tableaux croises item x segment, c'est a dire ce que tout sondage publie."""
    cum, replis, total = C44.lois_par_segment(codes, seg, k_items, n_min=n_min)
    if beta == 1.0:
        return cum, replis, total
    out = []
    for c in cum:
        p = np.diff(np.concatenate([np.zeros((c.shape[0], 1)), c], axis=1), axis=1)
        p = np.power(np.maximum(p, 0.0), beta)
        s = p.sum(axis=1, keepdims=True)
        p = np.divide(p, np.where(s > 0, s, 1.0))
        p[s[:, 0] <= 0] = 0.0
        out.append(np.cumsum(p, axis=1))
    return out, replis, total


def _tirer(cum, seg, masque, rng):
    """Tirage independant item par item dans les lois cumulees du segment, masque impose.
    Meme mecanique que a44_commun.tirer_nul, appliquee a un masque quelconque."""
    n, m = masque.shape
    out = np.full((n, m), -1, dtype=np.int16)
    g_max = len(cum[0]) - 1
    s = np.where(seg >= 0, seg, g_max)
    u = rng.random((n, m))
    for j in range(m):
        lignes = np.flatnonzero(masque[:, j])
        if not len(lignes):
            continue
        c = cum[j]
        lc = c[s[lignes]]
        vide = lc[:, -1] <= 0
        tir = (lc < u[lignes, j][:, None]).sum(axis=1)
        tir = np.minimum(tir, c.shape[1] - 1)
        tir[vide] = 0
        out[lignes, j] = tir
    return out


def adversaire_archetypes(codes_humain, seg, cum, m_arch, rho, rng):
    """A* archetypes : le fabricant qui ne connait que les marginales publiees.

    Pour chaque segment, m_arch archetypes tires dans p_{j,g}. Chaque faux repondant recoit
    un archetype de son segment, garde sa reponse avec la probabilite rho, et tire une
    valeur fraiche sinon. m_arch cree le deficit de patrons, rho la correlation residuelle
    intra segment, et le beta deja applique a cum regle la concentration.
    AUCUNE MICRODONNEE REELLE N'ENTRE ICI, seulement cum et le masque du flux.
    """
    n, m = codes_humain.shape
    g_max = len(cum[0]) - 1
    niveaux = [g for g in np.unique(seg) if g >= 0]
    n_arch = max(1, m_arch) * (len(niveaux) + 1)
    seg_arch = np.repeat(np.array(niveaux + [-1], dtype=seg.dtype), max(1, m_arch))
    arch = _tirer(cum, seg_arch, np.ones((n_arch, m), dtype=bool), rng)
    rang = {g: k for k, g in enumerate(niveaux + [-1])}
    choix = rng.integers(0, max(1, m_arch), size=n)
    ligne_arch = np.array([rang.get(int(g), len(niveaux)) * max(1, m_arch)
                           for g in np.where(seg >= 0, seg, -1)]) + choix
    frais = _tirer(cum, seg, codes_humain >= 0, rng)
    garder = rng.random((n, m)) < rho
    out = np.where(garder, arch[ligne_arch], frais).astype(np.int16)
    out[codes_humain < 0] = -1
    _ = g_max
    return out


def adversaire_microdonnees(codes_humain, seg, seg_vol, codes_voles, cum, rho, rng):
    """A** : le meme fabricant, mais dont les archetypes sont de VRAIES lignes volees.

    Chaque faux repondant copie une ligne reelle de son segment, puis resample chaque item
    avec la probabilite 1 - rho dans les marginales du segment. Il mesure de combien de
    vraies microdonnees abaissent la detectabilite.
    """
    n, m = codes_humain.shape
    src = np.full((n, m), -1, dtype=np.int16)
    niveaux = [g for g in np.unique(seg_vol) if g >= 0]
    for g in np.unique(np.where(seg >= 0, seg, -1)):
        lignes = np.flatnonzero(np.where(seg >= 0, seg, -1) == g)
        pool = np.flatnonzero(seg_vol == g) if g in niveaux else np.arange(len(seg_vol))
        if not len(pool):
            pool = np.arange(len(seg_vol))
        src[lignes] = codes_voles[rng.choice(pool, size=len(lignes), replace=True)]
    frais = _tirer(cum, seg, codes_humain >= 0, rng)
    garder = (rng.random((n, m)) < rho) & (src >= 0)
    out = np.where(garder, src, frais).astype(np.int16)
    out[codes_humain < 0] = -1
    return out


# ---------------------------------------------------------------------------
# 6. Les trois marginales de consequence
# ---------------------------------------------------------------------------

def ecarts_items(codes, blocs, n_min=30):
    """Ecart standardise de rang gauche moins droite, item par item. Sert a designer les
    trois marginales par la regle mecanique du preenregistrement section 3.3."""
    r = C44.rangs_colonne(codes)
    gauche, droite = blocs == "gauche", blocs == "droite"
    g = np.full(r.shape[1], np.nan)
    for j in range(r.shape[1]):
        col = r[:, j]
        ok = ~np.isnan(col)
        a, b = col[ok & gauche], col[ok & droite]
        if len(a) < n_min or len(b) < n_min:
            continue
        s = np.nanstd(col[ok], ddof=1)
        if np.isfinite(s) and s > 0:
            g[j] = (a.mean() - b.mean()) / s
    return g


def choisir_marginales(codes_humain, blocs, k=3):
    """Les k items au plus grand ecart standardise entre camps chez les humains purs, et
    pour chacun la modalite modale humaine. Regle fixee avant tout calcul."""
    g = np.abs(ecarts_items(codes_humain, blocs))
    ordre = np.argsort(np.where(np.isfinite(g), -g, np.inf))[:k]
    modales = []
    for j in ordre:
        col = codes_humain[:, j]
        col = col[col >= 0]
        modales.append(int(np.bincount(col).argmax()) if len(col) else -1)
    return list(map(int, ordre)), modales, [float(g[j]) for j in ordre]


def part_modale(codes, item, modalite):
    """Part de la modalite modale humaine dans le flux, en points de pourcentage. C'est le
    nombre qu'un institut publie."""
    col = codes[:, item]
    obs = col[col >= 0]
    return 100.0 * float((obs == modalite).mean()) if len(obs) else np.nan
