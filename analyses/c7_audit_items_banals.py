"""
c7_audit_items_banals : l'effet « items banals » est-il une propriete des donnees, ou une
selection post hoc sur les donnees qui servent a le mesurer ?

===========================================================================
PREENREGISTREMENT : resultats/audit-items-banals-2026-09-13.md section 0, ecrite et
COMMITEE SEULE avant ce fichier et avant le moindre chiffre nouveau.

CE QUI EST AUDITE. La branche agent/mesures/attaquant-imparfait etablit qu'un attaquant
restreint aux 45 items les plus ordinaires atteint 30,25 % de reidentification, contre
20,57 % avec les 60 items. Dans c7_attaquant_imparfait.py, le critere de banalite
(entropies_items / frequences_modales) est calcule sur `pool`, c'est-a-dire EXACTEMENT la
matrice des humains vague 4 qui sert ensuite de bassin de candidats et de verite pour
mesurer le taux. Les items sont donc choisis sur les memes personnes que celles sur
lesquelles le taux est mesure, et le volet tourne a repetitions = 1. Le seul test propre
est hors pli : choisir les items sur une moitie des personnes, mesurer sur l'autre.

LE PIEGE DU BASSIN, deja paye trois fois dans ce projet. Le top-1 depend mecaniquement de
la taille du bassin. Ici toutes les conditions d'un meme volet sont mesurees sur le MEME
demi-bassin (V1 a V3) ou sur le MEME bassin complet (V4), et la baseline demographique est
recalculee dans CHAQUE condition sur EXACTEMENT le meme sous-ensemble d'items et le meme
pool. Comparer un taux sur 45 items a une baseline sur 60 items serait le meme piege sous
un autre nom.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Ce script ne calcule,
n'imprime et n'ecrit JAMAIS l'identite ou le pid d'une personne retrouvee, ni aucune liste
d'appariements individuels. Seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / t1_commun.ecrire            les tables Twin, l'ecriture du csv
  c7_reidentification.items_communs               les 60 items toujours renseignes
  c7_reidentification.rangs_attaque               l'attaque naive (Hamming)
  c7_reidentification.graine_nom                  la graine stable par nom
  c7_reidentification.REF_V4 / DEMO / N_BOOTSTRAP les constantes de reference
  a2_commun.bootstrap_personnes                   l'IC 95 % par reechantillonnage
  c7_attaquant_fort.scores_hors_pli               l'attaquant fort A-LLR, hors pli, NON
                                                   reimplemente (argument `colonnes` deja
                                                   prevu pour restreindre les items)
  c7_stanford.rangs_depuis_accord                 les rangs a partir d'une matrice de score
  c7_controle_interpretabilite.controle_avant_interpretation
                                                   le controle de fidelite prealable
  c7_attaquant_imparfait (branche auditee)        RIEN n'est importe : la branche n'est pas
                                                   fusionnee. Les trois fonctions de
                                                   classement (entropie, frequence modale,
                                                   nombre de modalites) sont reecrites ici a
                                                   l'identique fonctionnel, et la section 1
                                                   du rapport verifie qu'elles reproduisent
                                                   les chiffres publies par la branche.

CE QUI EST NOUVEAU ICI, et rien d'autre : la selection HORS PLI du sous-ensemble d'items,
le balayage complet du nombre d'items retenus, le classement alternatif par nombre de
modalites, et le rejeu de la condition centrale sous A-LLR.

REDUCTION DECLAREE (preenregistrement 0.3) : 5 tirages de departage des ex aequo au lieu
de 20, exactement comme la branche auditee, pour que les chiffres soient comparables aux
siens. Le bootstrap reste a 2 000. Aucune autre reduction.

Aucun appel de modele de langage, aucun reseau, aucune depense. Lecture seule sur data/.
Aucun script existant n'est modifie.

Usage (chaque volet tient en avant-plan) :
  .venv/bin/python analyses/c7_audit_items_banals.py --volet v1 --cache <dir>
  .venv/bin/python analyses/c7_audit_items_banals.py --volet v2 --cache <dir>
  .venv/bin/python analyses/c7_audit_items_banals.py --volet v3 --cache <dir>
  .venv/bin/python analyses/c7_audit_items_banals.py --volet v4 --cache <dir>
  .venv/bin/python analyses/c7_audit_items_banals.py --volet v5 --cache <dir>
  .venv/bin/python analyses/c7_audit_items_banals.py --volet synthese --cache <dir>
===========================================================================
"""

import argparse
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from a2_commun import bootstrap_personnes                                # noqa: E402
from c7_reidentification import (                                        # noqa: E402
    DEMO, N_BOOTSTRAP, REF_V4, graine_nom, items_communs, rangs_attaque,
)
from c7_stanford import rangs_depuis_accord                              # noqa: E402
import c7_attaquant_fort as CF                                           # noqa: E402
from c7_controle_interpretabilite import (                               # noqa: E402
    EchecControleInterpretabilite, controle_avant_interpretation,
)

GRAINE = 20260913
N_TIRAGES_LIENS = 5            # reduction declaree, identique a la branche auditee
CANDIDAT = "JSON Persona - GPT4.1"
REF_V13 = "humains vagues 1-3 (retest)"

# Balayage preenregistre (section 0.3, volet V2 et V3)
GRILLE_K = [6, 10, 15, 20, 30, 40, 45, 50, 55, 60]
K_CENTRAL = 45
N_TIRAGES_ALEA = 5             # jeux d'items aleatoires communs, pour la condition temoin

SORTIE_CSV = "c7-audit-items-banals.csv"


# ---------------------------------------------------------------------------
# 1. Les trois criteres de classement des items, estimes sur un jeu de personnes donne
# ---------------------------------------------------------------------------
# Reecrits ici (la branche auditee n'est pas fusionnee, rien ne peut en etre importe).
# La section 1 du rapport verifie qu'ils reproduisent bien ses chiffres.

def entropies_items(bloc):
    """Entropie de Shannon (bits) de la distribution des reponses humaines, par item.

    `bloc` est une matrice (personnes, items) de codes humains. Le point de l'audit est
    precisement que `bloc` peut etre un SOUS-ENSEMBLE de personnes disjoint de celles sur
    lesquelles le taux sera mesure : c'est ce que la branche auditee ne fait pas.
    """
    h = np.zeros(bloc.shape[1])
    for j in range(bloc.shape[1]):
        col = bloc[:, j]
        col = col[col >= 0]
        if len(col) == 0:
            h[j] = 0.0
            continue
        _, cnt = np.unique(col, return_counts=True)
        p = cnt / cnt.sum()
        h[j] = float(-(p * np.log2(p)).sum())
    return h


def frequences_modales(bloc):
    """Frequence de la reponse modale, par item : la seconde mesure de banalite."""
    f = np.zeros(bloc.shape[1])
    for j in range(bloc.shape[1]):
        col = bloc[:, j]
        col = col[col >= 0]
        if len(col) == 0:
            f[j] = 1.0
            continue
        _, cnt = np.unique(col, return_counts=True)
        f[j] = float(cnt.max() / cnt.sum())
    return f


def n_modalites(bloc):
    """Nombre de modalites observees par item."""
    return np.array([len(np.unique(bloc[:, j][bloc[:, j] >= 0]))
                     for j in range(bloc.shape[1])], dtype=float)


def classement(bloc, critere, rng_egalites):
    """Ordre des items du plus « banal » au moins, selon le critere demande.

    'entropie'          : entropie croissante (operationnalisation preenregistree de la
                          branche auditee).
    'frequence_modale'  : frequence modale decroissante (sa variante post hoc).
    'n_modalites'       : nombre de modalites croissant. LES EGALITES SONT DEPARTAGEES PAR
                          UNE PERMUTATION ALEATOIRE DE GRAINE FIXE, jamais par l'entropie :
                          departager par l'entropie reintroduirait le critere qu'on cherche
                          justement a separer du nombre de modalites, et le volet V3 ne
                          testerait plus rien.
    """
    if critere == "entropie":
        cle = entropies_items(bloc)
    elif critere == "frequence_modale":
        cle = -frequences_modales(bloc)
    elif critere == "n_modalites":
        cle = n_modalites(bloc)
    else:
        raise ValueError(critere)
    brouillage = rng_egalites.permutation(len(cle))
    return np.lexsort((brouillage, cle))


# ---------------------------------------------------------------------------
# 2. Une mesure : candidat et baseline sur le MEME pool et les MEMES colonnes
# ---------------------------------------------------------------------------

def mesurer_hamming(X_cand, X_demo, pool, colonnes, etiquette):
    """top-1 du candidat et de la baseline, restreints aux memes colonnes, meme pool.

    Restreindre les colonnes plutot que masquer a -1 est equivalent pour la distance de
    Hamming normalisee (son denominateur est le nombre d'items renseignes des deux cotes)
    et evite un tirage inutile. La baseline demographique n'est jamais importee d'ailleurs :
    elle est recalculee ici, sur ces memes colonnes et ce meme pool.
    """
    n = X_cand.shape[0]
    vrai = np.arange(n)
    out = {}
    for role, X in (("cand", X_cand), ("base", X_demo)):
        rng = np.random.default_rng([GRAINE, graine_nom(role + "|" + etiquette)])
        _, top1, top10 = rangs_attaque(X[:, colonnes], pool[:, colonnes], vrai, rng,
                                       n_tirages=N_TIRAGES_LIENS)
        m1, b1, h1 = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP,
                                         graine=[GRAINE, graine_nom(role + etiquette), 1])
        m10, _, _ = bootstrap_personnes(top10, n_tirages=N_BOOTSTRAP,
                                        graine=[GRAINE, graine_nom(role + etiquette), 2])
        out[role + "_top1"] = m1
        out[role + "_top1_bas"] = b1
        out[role + "_top1_haut"] = h1
        out[role + "_top10"] = m10
    out["hasard"] = 1.0 / n
    out["n_bassin"] = n
    out["k_items"] = len(colonnes)
    return out


def mesurer_allr(X_cand, X_demo, pool, colonnes, etiquette):
    """La meme chose sous l'attaquant fort A-LLR, parametres estimes HORS PLI.

    c7_attaquant_fort.scores_hors_pli est appelee telle quelle (elle accepte deja
    `colonnes`). Elle estime a_j (accord apparie jumeau/personne) et q_j (marginale du
    jumeau) sur quatre plis de personnes et note le cinquieme : aucune reponse de la
    personne attaquee n'entre dans ses propres parametres.
    """
    n = X_cand.shape[0]
    vrai = np.arange(n)
    out = {}
    for role, X in (("cand", X_cand), ("base", X_demo)):
        s = CF.scores_hors_pli(X, pool, vrai, f"audit|{role}|{etiquette}",
                               colonnes=colonnes)
        rng = np.random.default_rng([GRAINE, graine_nom("llr|" + role + etiquette)])
        _, top1, top10 = rangs_depuis_accord(s, vrai, rng, n_tirages=N_TIRAGES_LIENS)
        m1, b1, h1 = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP,
                                         graine=[GRAINE, graine_nom(role + etiquette), 3])
        m10, _, _ = bootstrap_personnes(top10, n_tirages=N_BOOTSTRAP,
                                        graine=[GRAINE, graine_nom(role + etiquette), 4])
        out[role + "_top1"] = m1
        out[role + "_top1_bas"] = b1
        out[role + "_top1_haut"] = h1
        out[role + "_top10"] = m10
    out["hasard"] = 1.0 / n
    out["n_bassin"] = n
    out["k_items"] = len(colonnes)
    return out


def ligne(volet, attaque, selection, k, pli, res, note=""):
    d = {"volet": volet, "attaque": attaque, "selection": selection, "k_items": k,
         "pli": pli, "note": note}
    d.update(res)
    d["ratio_cand_base"] = (res["cand_top1"] / res["base_top1"]
                            if res["base_top1"] > 0 else np.nan)
    d["au_dessus_baseline"] = bool(res["cand_top1_bas"] > res["base_top1_haut"])
    print(f"  {volet:4s} {attaque:8s} {selection:22s} k={k:2d} pli={pli:5s} "
          f"cand={res['cand_top1']*100:6.2f} % "
          f"[{res['cand_top1_bas']*100:5.2f};{res['cand_top1_haut']*100:5.2f}] "
          f"base={res['base_top1']*100:5.2f} % ratio={d['ratio_cand_base']:5.2f}",
          flush=True)
    return d


# ---------------------------------------------------------------------------
# 3. Bassin (identique a celui de la branche auditee) et decoupage en plis
# ---------------------------------------------------------------------------

def preparer():
    """Le bassin de la branche auditee, reconstruit a l'identique : 2 058 personnes,
    60 items toujours renseignes, candidat JSON Persona - GPT4.1."""
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    couv_c = (codes[CANDIDAT] >= 0).any(axis=1)
    couv_d = (codes[DEMO] >= 0).any(axis=1)
    couv_h = (codes[REF_V4][:, items] >= 0).all(axis=1)
    bassin = np.flatnonzero(couv_c & couv_d & couv_h)
    pool = codes[REF_V4][bassin][:, items]
    X_cand = codes[CANDIDAT][bassin][:, items]
    X_demo = codes[DEMO][bassin][:, items]
    return paq, bassin, items, pool, X_cand, X_demo


def moities(n):
    """Deux moities de personnes, disjointes, graine fixe. A sert a CHOISIR les items,
    B a MESURER le taux, puis l'inverse."""
    rng = np.random.default_rng([GRAINE, 4242])
    perm = rng.permutation(n)
    return perm[: n // 2], perm[n // 2:]


def chemin_cache(cache, volet):
    return os.path.join(cache, f"c7-audit-items-banals-{volet}.csv")


# ---------------------------------------------------------------------------
# 4. Volets
# ---------------------------------------------------------------------------

def volet_v1(pool, X_cand, X_demo):
    """Hors pli contre dans le pli, a k = 45, sur le meme demi-bassin.

    Quatre conditions par demi-bassin, toutes mesurees sur les MEMES personnes et le MEME
    pool -- seul le JEU D'ITEMS change :
      hors_pli   : items choisis sur l'AUTRE moitie des personnes
      dans_pli   : items choisis sur la moitie mesuree (replique exacte du defaut audite)
      alea_commun: k items tires au hasard, identiques pour tous (temoin D1b)
      tous       : les 60 items
    """
    lignes = []
    mA, mB = moities(pool.shape[0])
    for nom_pli, choix, mesure in (("A", mA, mB), ("B", mB, mA)):
        p_mes = pool[mesure]
        c_mes = X_cand[mesure]
        d_mes = X_demo[mesure]
        rng_eg = np.random.default_rng([GRAINE, 31])
        for crit in ("entropie", "frequence_modale"):
            ordre_hp = classement(pool[choix], crit, np.random.default_rng([GRAINE, 31]))
            ordre_dp = classement(p_mes, crit, np.random.default_rng([GRAINE, 31]))
            recouv = len(np.intersect1d(ordre_hp[:K_CENTRAL], ordre_dp[:K_CENTRAL]))
            lignes.append(ligne("V1", "hamming", f"{crit}_hors_pli", K_CENTRAL, nom_pli,
                                mesurer_hamming(c_mes, d_mes, p_mes,
                                                np.sort(ordre_hp[:K_CENTRAL]),
                                                f"v1|hp|{crit}|{nom_pli}"),
                                note=f"recouvrement_hp_dp={recouv}/{K_CENTRAL}"))
            lignes.append(ligne("V1", "hamming", f"{crit}_dans_pli", K_CENTRAL, nom_pli,
                                mesurer_hamming(c_mes, d_mes, p_mes,
                                                np.sort(ordre_dp[:K_CENTRAL]),
                                                f"v1|dp|{crit}|{nom_pli}")))
        for t in range(N_TIRAGES_ALEA):
            rng_a = np.random.default_rng([GRAINE, graine_nom(f"alea|{nom_pli}|{t}")])
            cols = np.sort(rng_a.choice(pool.shape[1], size=K_CENTRAL, replace=False))
            lignes.append(ligne("V1", "hamming", "aleatoire_commun", K_CENTRAL, nom_pli,
                                mesurer_hamming(c_mes, d_mes, p_mes, cols,
                                                f"v1|al|{nom_pli}|{t}"),
                                note=f"tirage={t}"))
        lignes.append(ligne("V1", "hamming", "tous_les_items", pool.shape[1], nom_pli,
                            mesurer_hamming(c_mes, d_mes, p_mes,
                                            np.arange(pool.shape[1]),
                                            f"v1|tous|{nom_pli}")))
        del rng_eg
    return lignes


def volet_balayage(pool, X_cand, X_demo, critere, volet):
    """Le profil complet sur le nombre d'items retenus, hors pli, pour un critere donne."""
    lignes = []
    mA, mB = moities(pool.shape[0])
    for nom_pli, choix, mesure in (("A", mA, mB), ("B", mB, mA)):
        p_mes, c_mes, d_mes = pool[mesure], X_cand[mesure], X_demo[mesure]
        ordre = classement(pool[choix], critere, np.random.default_rng([GRAINE, 31]))
        for k in GRILLE_K:
            if k > pool.shape[1]:
                continue
            lignes.append(ligne(volet, "hamming", f"{critere}_hors_pli", k, nom_pli,
                                mesurer_hamming(c_mes, d_mes, p_mes,
                                                np.sort(ordre[:k]),
                                                f"{volet}|{critere}|{k}|{nom_pli}")))
    return lignes


def volet_v4(pool, X_cand, X_demo):
    """La condition centrale sous A-LLR, et son temoin Hamming sur le bassin complet.

    Ici le bassin est le bassin COMPLET (2 058) et non un demi-bassin : A-LLR estime ses
    parametres hors pli en interne, il n'y a donc pas de fuite a corriger par un decoupage
    supplementaire. Le classement des items reste celui de la branche auditee (calcule sur
    tout le pool) : le but de ce volet n'est pas de tester la selection -- V1 s'en charge --
    mais de savoir si le gain survit a un attaquant qui sait deja exploiter la rarete.
    Toutes les conditions partagent le meme bassin et le meme pool.
    """
    lignes = []
    ordre = classement(pool, "entropie", np.random.default_rng([GRAINE, 31]))
    rng_a = np.random.default_rng([GRAINE, graine_nom("v4|alea")])
    sous_ensembles = [
        ("entropie_basse", np.sort(ordre[:K_CENTRAL])),
        ("aleatoire_commun", np.sort(rng_a.choice(pool.shape[1], size=K_CENTRAL,
                                                  replace=False))),
        ("tous_les_items", np.arange(pool.shape[1])),
    ]
    for nom, cols in sous_ensembles:
        for att, fn in (("hamming", mesurer_hamming), ("A-LLR", mesurer_allr)):
            t = time.time()
            lignes.append(ligne("V4", att, nom, len(cols), "complet",
                                fn(X_cand, X_demo, pool, cols, f"v4|{att}|{nom}"),
                                note=f"{time.time() - t:.0f}s"))
    return lignes


def volet_v5(paq, bassin, items, pool, X_cand):
    """Le controle d'interpretabilite applique a la condition « 45 items banals ».

    Il est applique AVANT toute interpretation de la section 3 du rapport, sur exactement
    les 45 colonnes utilisees et exactement le bassin utilise. La fonction recalcule
    elle-meme la baseline demographique sur ces memes indices : aucune baseline ne lui est
    fournie, il n'y a pas de parametre pour ca.
    """
    ordre = classement(pool, "entropie", np.random.default_rng([GRAINE, 31]))
    cols = np.sort(ordre[:K_CENTRAL])
    lignes = []
    for nom, sous in (("45_items_banals", cols),
                      ("60_items_reference", np.arange(pool.shape[1]))):
        try:
            d = controle_avant_interpretation(bassin, items[sous], X_cand[:, sous],
                                              f"{CANDIDAT} / {nom}", paq=paq)
            statut = "PASSE"
        except EchecControleInterpretabilite as exc:
            d = getattr(exc, "diagnostic", {})
            statut = "ECHEC"
        lignes.append({"volet": "V5", "attaque": "hamming", "selection": nom,
                       "k_items": len(sous), "pli": "complet", "controle": statut,
                       "cand_top1": d.get("candidat_top1", np.nan),
                       "cand_top1_bas": d.get("candidat_ic", (np.nan, np.nan))[0],
                       "cand_top1_haut": d.get("candidat_ic", (np.nan, np.nan))[1],
                       "base_top1": d.get("baseline_top1", np.nan),
                       "base_top1_bas": d.get("baseline_ic", (np.nan, np.nan))[0],
                       "base_top1_haut": d.get("baseline_ic", (np.nan, np.nan))[1],
                       "hasard": d.get("hasard", np.nan),
                       "n_bassin": d.get("bassin", np.nan)})
        print(f"  V5 controle {nom:20s} : {statut} — cand "
              f"{d.get('candidat_top1', float('nan'))*100:.2f} % vs base "
              f"{d.get('baseline_top1', float('nan'))*100:.2f} %", flush=True)
    return lignes


def diagnostic_criteres(pool):
    """Les correlations entre les trois criteres, sur le pool complet : sert a savoir si
    « banalite » et « nombre de modalites » sont seulement deux noms de la meme chose."""
    h = entropies_items(pool)
    f = frequences_modales(pool)
    nm = n_modalites(pool)
    print(f"  entropie : min {h.min():.3f}, mediane {np.median(h):.3f}, max {h.max():.3f}",
          flush=True)
    print(f"  frequence modale : min {f.min():.3f}, mediane {np.median(f):.3f}, "
          f"max {f.max():.3f}", flush=True)
    print(f"  nombre de modalites : min {int(nm.min())}, mediane {int(np.median(nm))}, "
          f"max {int(nm.max())}", flush=True)
    print(f"  r(entropie, frequence modale) = {np.corrcoef(h, f)[0, 1]:.3f}", flush=True)
    print(f"  r(entropie, n modalites)      = {np.corrcoef(h, nm)[0, 1]:.3f}", flush=True)
    print(f"  r(freq modale, n modalites)   = {np.corrcoef(f, nm)[0, 1]:.3f}", flush=True)
    rng = np.random.default_rng([GRAINE, 31])
    o_h = classement(pool, "entropie", np.random.default_rng([GRAINE, 31]))[:K_CENTRAL]
    o_f = classement(pool, "frequence_modale",
                     np.random.default_rng([GRAINE, 31]))[:K_CENTRAL]
    o_n = classement(pool, "n_modalites", np.random.default_rng([GRAINE, 31]))[:K_CENTRAL]
    del rng
    print(f"  recouvrement des 45 retenus : entropie/freq {len(np.intersect1d(o_h, o_f))}, "
          f"entropie/modalites {len(np.intersect1d(o_h, o_n))}, "
          f"freq/modalites {len(np.intersect1d(o_f, o_n))}", flush=True)
    return [{"volet": "diag", "attaque": "-", "selection": "criteres", "k_items": K_CENTRAL,
             "pli": "complet",
             "note": (f"r_h_f={np.corrcoef(h, f)[0, 1]:.3f};"
                      f"r_h_nm={np.corrcoef(h, nm)[0, 1]:.3f};"
                      f"r_f_nm={np.corrcoef(f, nm)[0, 1]:.3f};"
                      f"recouv_h_n={len(np.intersect1d(o_h, o_n))};"
                      f"nm_max={int(nm.max())};f_max={f.max():.3f}")}]


# ---------------------------------------------------------------------------
# 5. Synthese
# ---------------------------------------------------------------------------

def synthese(cache):
    parts = []
    for v in ("v1", "v2", "v3", "v4", "v5"):
        c = chemin_cache(cache, v)
        if os.path.exists(c):
            parts.append(pd.read_csv(c))
        else:
            print(f"volet manquant : {v}", flush=True)
    df = pd.concat(parts, ignore_index=True)
    cles = ["volet", "attaque", "selection", "k_items"]
    num = [c for c in ("cand_top1", "cand_top1_bas", "cand_top1_haut", "cand_top10",
                       "base_top1", "base_top1_bas", "base_top1_haut", "base_top10",
                       "hasard", "n_bassin", "ratio_cand_base") if c in df.columns]
    agg = df.groupby(cles, sort=False, dropna=False)[num].mean().reset_index()
    agg["n_plis"] = df.groupby(cles, sort=False, dropna=False).size().values
    if "controle" in df.columns:
        ctl = df.dropna(subset=["controle"]).set_index(
            ["volet", "selection"])["controle"].to_dict()
        agg["controle"] = [ctl.get((r.volet, r.selection), "") for r in agg.itertuples()]
    T1.ecrire(agg, SORTIE_CSV)

    print("\n=== toutes les conditions (moyenne des deux plis) ===", flush=True)
    for _, r in agg.iterrows():
        if np.isnan(r.get("cand_top1", np.nan)):
            continue
        print(f"{r.volet:4s} {r.attaque:8s} {str(r.selection):24s} k={int(r.k_items):2d} "
              f"n={int(r.n_bassin):4d} cand={r.cand_top1*100:6.2f} % "
              f"[{r.cand_top1_bas*100:5.2f};{r.cand_top1_haut*100:5.2f}] "
              f"base={r.base_top1*100:5.2f} % ratio={r.ratio_cand_base:5.2f}", flush=True)

    print("\n=== V2 / V3 : profil sur le nombre d'items (hors pli) ===", flush=True)
    for volet in ("V2", "V3"):
        sous = agg[(agg.volet == volet)].sort_values("k_items")
        if not len(sous):
            continue
        pic = sous.loc[sous.cand_top1.idxmax()]
        print(f"  {volet} ({sous.selection.iloc[0]}) : " + " ".join(
            f"k{int(r.k_items)}={r.cand_top1*100:.1f}" for _, r in sous.iterrows()),
            flush=True)
        print(f"    maximum a k = {int(pic.k_items)} ({pic.cand_top1*100:.2f} %), "
              f"k=60 = {float(sous[sous.k_items == 60].cand_top1.iloc[0])*100:.2f} %",
              flush=True)
    return agg


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volet", required=True,
                    choices=["v1", "v2", "v3", "v4", "v5", "synthese"])
    ap.add_argument("--cache", required=True)
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)
    t0 = time.time()

    if args.volet == "synthese":
        synthese(args.cache)
        return

    print(__doc__.split("=" * 75)[1], flush=True)
    paq, bassin, items, pool, X_cand, X_demo = preparer()
    mA, mB = moities(pool.shape[0])
    print(f"bassin : {len(bassin)} personnes, {len(items)} items, candidat = {CANDIDAT}",
          flush=True)
    print(f"moities hors pli : {len(mA)} / {len(mB)} personnes, disjointes = "
          f"{len(np.intersect1d(mA, mB)) == 0}", flush=True)
    print("\n=== diagnostic des criteres de banalite ===", flush=True)
    diag = diagnostic_criteres(pool)

    if args.volet == "v1":
        print("\n=== V1 : hors pli contre dans le pli, k = 45 ===", flush=True)
        lignes = volet_v1(pool, X_cand, X_demo) + diag
    elif args.volet == "v2":
        print("\n=== V2 : balayage du nombre d'items, entropie, hors pli ===", flush=True)
        lignes = volet_balayage(pool, X_cand, X_demo, "entropie", "V2")
    elif args.volet == "v3":
        print("\n=== V3 : balayage par NOMBRE DE MODALITES, hors pli ===", flush=True)
        lignes = volet_balayage(pool, X_cand, X_demo, "n_modalites", "V3")
    elif args.volet == "v4":
        print("\n=== V4 : condition centrale sous A-LLR, bassin complet ===", flush=True)
        lignes = volet_v4(pool, X_cand, X_demo)
    elif args.volet == "v5":
        print("\n=== V5 : controle d'interpretabilite ===", flush=True)
        lignes = volet_v5(paq, bassin, items, pool, X_cand)

    pd.DataFrame(lignes).to_csv(chemin_cache(args.cache, args.volet), index=False)
    print(f"\n{args.volet} : {len(lignes)} lignes, {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
