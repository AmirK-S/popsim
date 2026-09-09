"""
a42_commun : briques partagees par le test du PLANCHER DE BRUIT DE CELLULE sur des
partitions tierces, question du 8 septembre 2026, "le resultat des rares est il du bruit
de petites cellules ?".

C'est le verrou 2 de `MODELE-DU-MONDE.md` section 6 et la premiere des trois objections de
la section 7. a34 a mesure l'exces sur plancher, mais sur deux partitions dont il declare
lui meme en section 9 point 2 qu'aucune n'est a la fois non circulaire pour le plancher et
non tautologique pour la regression : D_seg est le calcul meme du plancher, D_logit est la
confiance de `B1 argmax`. a42 construit trois partitions tierces, dont une qui n'emploie
aucun attribut demographique ni aucun predicteur.

LA FAMILLE, LES SEUILS ET LES PLANCHERS SONT ECRITS DANS
`resultats/a42-preenregistrement.md`, HORODATE DU 8 SEPTEMBRE 2026 A 15:42:15 CEST, AVANT
TOUT CALCUL. Ce fichier n'est pas modifie ensuite.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a34_commun, et par
lui a31_commun, a29_commun, a28_commun, a25_commun, a25_mesures, a8_commun, a2_commun,
a2_baselines_gss, a5_evaluer et a5_agents_locaux_gss ; plus les matrices de `PMM k=5`,
`PMM k=10` et `IM m=10 mode des m` relues du cache de a35, produites par
`a35_commun.imputations_regression` sans une ligne recopiee.

Ce module ne teste rien. Il construit les TROIS PARTITIONS, les TROIS PLANCHERS et le
support de modalite du controle de Rennard.

  1. P_A, la stabilite en vague 2. Une cellule minoritaire est STABLE si la personne a
     redonne exactement la meme modalite deux semaines plus tard, INSTABLE sinon. Les
     cellules sans reponse de vague 2 sont hors partition. C'est la seule partition du
     dossier qui n'emploie ni la confiance d'un predicteur, ni une frequence de segment,
     ni un attribut demographique : elle est prise sur la personne elle meme. Une rarete
     stable est de la vraie heterogeneite individuelle, une rarete instable est
     indistinguable du bruit humain de reponse.
     Identite declaree d'avance : sur P_A, `humains vague 2` a un rappel de 1 sur les
     stables et de 0 sur les instables PAR CONSTRUCTION, la partition etant cette ligne.
     Elle est imprimee comme identite et n'entre dans aucun test.
  2. P_B, la division de recensement. Frequence de la modalite dans la division de
     recensement de la personne, neuf niveaux, calculee sans la personne, decoupee en
     terciles. Elle n'est ni la confiance de `B1` ni le segment ideologie x genre x age du
     plancher. Defaut residuel declare : `census_division` fait partie des onze attributs
     que `B1`, `B3 foret` et les personas demographiques recoivent ; la partition est
     independante du plancher et de la regle de decision de `B1`, pas de la famille des
     predicteurs.
  3. P_C, la partition aleatoire fixee. Neuf groupes de personnes tires au hasard, graine
     fixee dans le preenregistrement. Le score est la frequence de la modalite dans le
     groupe aleatoire, sans la personne. Un groupe aleatoire ne porte aucune information :
     tout gradient le long de P_C est du bruit d'echantillonnage de petites cellules, et
     donne la taille de l'artefact de Rennard mesuree chez nous. C'est le placebo.

  4. Les trois planchers, tous calcules sur les memes cellules que le rappel qu'ils
     jugent : tirage dans la marginale de l'item, tirage dans la marginale du segment
     ideologie x genre x age (le plancher de bruit de cellule de la lecture 01, importe de
     a34 sans changement), et les memes humains reinterrogeus a deux semaines, qui est en
     pratique un plafond et qui est degenere sur P_A.

  5. Le support de modalite du controle de Rennard : nombre de personnes du perimetre qui
     ont donne cette modalite sur cet item en vague 1.

Convention de masque, reprise de a8 section 6, a29, a31 et a34 sans changement : une
cellule est evaluable des que la vraie reponse de la vague 1 est observee ; une prediction
refusee compte comme non minoritaire.

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

import a34_commun as C34
import a28_commun as C28
from a2_commun import est_manquant

RACINE = C34.RACINE
SORTIE = C34.SORTIE

# Graines : celle de l'analyse est celle de a34 et de a35 ; celle de la partition
# aleatoire est ecrite dans le preenregistrement et ne doit plus bouger.
GRAINE = 20260908
GRAINE_PLACEBO = 20260908
SEUIL = 0.10
SEUILS = [0.10, 0.20]

AXE_TIERS = "census_division"
N_GROUPES_PLACEBO = 9
N_MIN_TIERS = 5
SUPPORTS_RENNARD = [0, 5, 10, 20]
SUPPORT_TESTE = 20

COMPARATEUR = C34.COMPARATEUR          # "B1 argmax"

# Les trois methodes d'imputation de a35, relues de son cache.
IMPUTATIONS_A35 = ["PMM k=5", "PMM k=10", "IM m=10 mode des m"]

# Les treize methodes testees, telles que le preenregistrement les fixe. `B1 argmax` est
# le comparateur, il n'est pas dans cette liste ; il entre dans H2 et H4 seulement.
TESTEES = ["agents composite", "agents entretien (v3)", "agents enquete",
           "agents demographiques (v6)", "agents v7", "agents v8",
           "B2 argmax", "B3 foret"] + IMPUTATIONS_A35 + ["C2", "C3"]

# Ordre d'affichage stable dans tous les tableaux de a42.
ORDRE = ["humains vague 2",
         "agents composite", "agents entretien (v3)", "agents enquete",
         "agents demographiques (v6)", "agents v7", "agents v8", "C2", "C3",
         "PMM k=5", "PMM k=10", "IM m=10 mode des m",
         "B2 argmax", "B1 argmax", "B3 foret", "B0 tirage", "B0 mode"]

LLM = C34.LLM
STAT = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax", "B3 foret"] + IMPUTATIONS_A35

PERIMETRE_NATUREL = {m: ("150" if m in ("C2", "C3") else "1052") for m in TESTEES}

CLASSES_PA = ["rarete stable", "rarete instable"]
TERCILES = ["T1 non deductible", "T2 intermediaire", "T3 deductible"]
PLANCHERS = ["item", "segment", "humains vague 2"]

# Briques reprises telles quelles.
observe = C34.observe
appartient = C34.appartient
masques = C34.masques
modalites_rares = C34.modalites_rares
par_personne = C34.par_personne
moyenne_par_personne = C34.moyenne_par_personne
taux = C34.taux
taux_ic = C34.taux_ic
contraste = C34.contraste
tirages_bootstrap = C34.tirages_bootstrap
holm = C34.holm
benjamini_hochberg = C34.benjamini_hochberg
ecrire = C34.ecrire
p_contre_zero = C34.p_contre_zero
segment_fin = C34.segment_fin
frequence_segment = C34.frequence_segment
frequence_item = C34.frequence_item
bornes_terciles = C34.bornes_terciles
terciles = C34.terciles
perimetres = C34.perimetres


def charger(cache, cache_foret, cache_a35):
    """Paquet de a34, plus les trois methodes d'imputation de a35 relues de son cache.

    Le cache de a35 est lu, jamais reecrit. S'il manque ou s'il ne porte pas les trois
    matrices attendues, elles sont declarees non importables : la liste des methodes
    testees est reduite d'autant par l'appelant et le fait est ecrit dans le rapport,
    comme le preenregistrement l'exige.
    """
    paquet = C34.charger(cache, cache_foret)
    manquantes = []
    if cache_a35 and os.path.exists(cache_a35):
        with open(cache_a35, "rb") as f:
            brut = pickle.load(f)
        for nom in IMPUTATIONS_A35:
            if nom in brut and isinstance(brut[nom], np.ndarray):
                paquet["M"][nom] = brut[nom]
            else:
                manquantes.append(nom)
    else:
        manquantes = list(IMPUTATIONS_A35)
    paquet["imputations_manquantes"] = manquantes
    return paquet


# ---------------------------------------------------------------------------
# 1. P_A, la stabilite en vague 2
# ---------------------------------------------------------------------------

def classes_stabilite(y1, y2):
    """Matrice d'entiers : 1 stable, 0 instable, -1 hors partition.

    Une cellule est dans la partition des que les DEUX vagues portent une reponse
    exploitable. Stable veut dire que la personne a redonne exactement la meme modalite
    deux semaines plus tard. La definition ne regarde pas si la modalite est rare : elle
    est une propriete de la personne sur cet item, et c'est ce qui permet de l'appliquer
    identiquement au numerateur du rappel et au denominateur de la precision.
    """
    o1, o2 = observe(y1), observe(y2)
    dedans = o1 & o2
    stable = dedans & (y1 == y2)
    out = np.full(y1.shape, -1, dtype=np.int8)
    out[dedans] = 0
    out[stable] = 1
    return out


def rappel_vague2(y1, y2):
    """Matrice de flottants : 1 si la vague 2 redonne la modalite de la vague 1, sinon 0.

    NaN la ou l'une des deux vagues manque. Sa moyenne sur un jeu de cellules est
    exactement le rappel des memes humains reinterroges sur ce jeu : c'est le troisieme
    plancher, qui est en pratique un plafond.
    """
    o1, o2 = observe(y1), observe(y2)
    out = np.full(y1.shape, np.nan)
    dedans = o1 & o2
    out[dedans] = 0.0
    out[dedans & (y1 == y2)] = 1.0
    return out


# ---------------------------------------------------------------------------
# 2. P_B et P_C, les deux partitions par frequence dans un segment tiers
# ---------------------------------------------------------------------------

def segment_axe(x, attributs, axe=AXE_TIERS):
    """Segment defini par un seul attribut, vecteur d'entiers, -1 si l'attribut manque."""
    col = {a: i for i, a in enumerate(attributs)}
    if axe not in col:
        raise KeyError(f"attribut absent des demographies : {axe}")
    brut = [C28.norm(v) for v in x[:, col[axe]]]
    libelles = [None if ((not v.strip()) or v == "non renseigne") else v for v in brut]
    mods = sorted({v for v in libelles if v is not None})
    idx = {mod: k for k, mod in enumerate(mods)}
    return np.array([idx.get(v, -1) for v in libelles], dtype=np.int32), mods


def segment_placebo(n, k=N_GROUPES_PLACEBO, graine=GRAINE_PLACEBO):
    """Groupes aleatoires de tailles egales, graine fixee dans le preenregistrement.

    Le placebo n'est pas un ornement : l'esperance du score dans un groupe aleatoire est
    la marginale de l'item, donc tout gradient observe le long de cette partition est du
    bruit d'echantillonnage de petites cellules et rien d'autre. Il donne l'etalon de
    l'artefact que Rennard et Xypolopoulos decrivent.
    """
    rng = np.random.default_rng(graine)
    ordre = rng.permutation(n)
    seg = np.empty(n, dtype=np.int32)
    seg[ordre] = np.arange(n) % k
    return seg, [f"groupe aleatoire {i + 1}" for i in range(k)]


# ---------------------------------------------------------------------------
# 3. Support de modalite, controle de Rennard
# ---------------------------------------------------------------------------

def support_modalite(mat, verite, ok):
    """Nombre de personnes du perimetre qui donnent la modalite de la cellule sur l'item.

    mat    : matrice des modalites dont on veut le support, la verite ou une prediction.
    verite : matrice de la vague 1, qui fournit les effectifs.
    ok     : cellules evaluables.

    A la difference des planchers, la personne elle meme n'est PAS retiree : le support
    est ici une propriete de la cellule de verite terrain au sens de Rennard, "la modalite
    est elle portee par au moins n personnes", et retirer la personne rendrait le seuil
    dependant de sa propre reponse. Le controle est donc, de ce point de vue, legerement
    conservateur : une modalite portee par exactement n personnes reste dedans.
    """
    n, m = mat.shape
    out = np.full((n, m), np.nan)
    for j in range(m):
        colv, colo, colm = verite[:, j], ok[:, j], mat[:, j]
        cpt = {}
        for i in range(n):
            if colo[i]:
                cpt[colv[i]] = cpt.get(colv[i], 0) + 1
        for i in range(n):
            v = colm[i]
            if v is None or est_manquant(v):
                continue
            out[i, j] = float(cpt.get(v, 0))
    return out


# ---------------------------------------------------------------------------
# 4. Une mesure, ses planchers, ses exces
# ---------------------------------------------------------------------------

def mesure_sur(selv, selp, juste, planchers):
    """Rappel, precision, F1 et les trois exces sur un jeu de cellules donne.

    selv : cellules minoritaires REELLES retenues, denominateur du rappel.
    selp : cellules ou la methode OSE une minorite, retenues, denominateur de la precision.
    juste: cellules ou la prediction est une minorite juste.
    planchers : nom -> matrice de flottants, la valeur attendue sous le tirage de
                reference, NaN la ou elle n'est pas definie.

    Retourne un dictionnaire de couples (numerateur, denominateur) PAR PERSONNE, plus les
    valeurs ponctuelles. Le bootstrap est fait par l'appelant sur ces couples, ce qui rend
    tous les contrastes apparies : le meme tirage de personnes sert a toutes les methodes.
    """
    nr, dr = par_personne(juste, selv)
    npx, dpx = par_personne(juste, selp)
    out = {"_rappel": (nr, dr), "_precision": (npx, dpx),
           "cellules": int(dr.sum()), "raretes_osees": int(dpx.sum())}
    rap, pre = taux(nr, dr), taux(npx, dpx)
    out["rappel"], out["precision"] = rap, pre
    out["f1"] = (2 * rap * pre / (rap + pre)
                 if np.isfinite(rap) and np.isfinite(pre) and (rap + pre) > 0
                 else (0.0 if np.isfinite(rap) else np.nan))
    for nom, F in planchers.items():
        okp = selv & ~np.isnan(F)
        npl, dpl = moyenne_par_personne(okp, F)
        nre, dre = par_personne(juste, okp)
        out[f"_exces_{nom}"] = (nre - npl, dre)
        out[f"plancher_{nom}"] = taux(npl, dpl)
        out[f"rappel_sur_{nom}"] = taux(nre, dre)
        out[f"exces_{nom}"] = taux(nre, dre) - taux(npl, dpl)
        out[f"cellules_{nom}"] = int(dre.sum())
    return out


def difference_de_differences(a1, b1, a3, b3, idx_boot):
    """((a1 - b1) - (a3 - b3)) sur quatre rapports de sommes, memes personnes tirees.

    Chaque argument est un couple (numerateur, denominateur) par personne. C'est la forme
    de H3 : l'avantage sur le comparateur dans une classe, moins le meme avantage dans
    l'autre classe. Le bootstrap porte sur les quatre rapports simultanement, sinon la
    correlation entre eux serait ignoree et l'intervalle serait faux.
    """
    def r(couple, idx=None):
        nu, de = couple
        if idx is None:
            d = de.sum()
            return nu.sum() / d if d > 0 else np.nan
        d = de[idx].sum(axis=1)
        n_ = nu[idx].sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            return np.where(d > 0, n_ / np.maximum(d, 1e-12), np.nan)

    obs = (r(a1) - r(b1)) - (r(a3) - r(b3))
    tir = ((r(a1, idx_boot) - r(b1, idx_boot))
           - (r(a3, idx_boot) - r(b3, idx_boot)))
    tir = tir[~np.isnan(tir)]
    if len(tir) == 0 or not np.isfinite(obs):
        return np.nan, np.nan, np.nan, 1.0
    return (float(obs), float(np.percentile(tir, 2.5)),
            float(np.percentile(tir, 97.5)), p_contre_zero(tir))


def valeur_ic_p(couple, idx_boot):
    """Valeur d'un rapport de sommes, son intervalle, et le p bilateral contre zero."""
    v, lo, hi, tir = taux_ic(couple[0], couple[1], idx_boot)
    return v, lo, hi, p_contre_zero(tir)
