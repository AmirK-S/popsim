"""
c7_audit_predictibilite : « la fuite suit la predictibilite, non la rarete » -- ou bien
est-ce seulement « on retrouve mieux quelqu'un quand on a des informations exactes » ?

===========================================================================
PREENREGISTREMENT : resultats/audit-predictibilite-2026-09-13.md, section 0, ecrite et
COMMITEE avant ce fichier et avant tout calcul (commit 7c77232). Predictions P1-P7 et
critere de refutation de l'audit lui-meme y sont fixes.

CE QUI EST ATTAQUE. Sur la branche agent/mesures/equite-risque, un agent etablit que le
risque individuel de reidentification DECROIT avec l'atypicite des reponses
(rho = -0,181) et CROIT avec la coherence interne test-retest (+0,256), et conclut que
« la fuite suit la predictibilite, pas la rarete ». Si c'est vrai, toute la famille des
defenses de type k-anonymite vise la mauvaise cible. Ce script cherche pourquoi c'est faux.

L'EXPLICATION PLATE A ELIMINER D'ABORD. Le jumeau Twin-2K-500 est construit a partir de la
persona des VAGUES 1-3 (data/twin2k500/README.md : wave1_3_persona_text) et l'attaque
l'apparie contre les reponses VAGUE 4. La « coherence test-retest » est l'accord v1-3 / v4,
c'est-a-dire l'accord entre la SOURCE D'INFORMATION DE L'ATTAQUANT et sa CIBLE. « Les
coherents sont plus exposes » pourrait donc se reduire a « on retrouve mieux quelqu'un
quand ce qu'on croit savoir de lui est encore exact » : un enonce sur la qualite de la
donnee auxiliaire, pas sur le jumeau LLM ni sur la vie privee.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Ce script ne calcule,
n'imprime et n'ecrit JAMAIS l'identite, le pid, une reponse ni une combinaison
individuelle. Seuls des agregats sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / ecrire                  les tables de Twin, l'ecriture CSV
  c7_reidentification.items_communs            les 60 items toujours renseignes
  c7_reidentification.rangs_attaque            L'ATTAQUE NAIVE (Hamming), inchangee
  c7_reidentification.graine_nom / REF_V4 / REF_V13 / DEMO / GRAINE
  c7_attaquant_fort.scores_hors_pli            L'ATTAQUANT FORT A-LLR, hors pli, inchange
  c7_stanford.rangs_depuis_accord              rang depuis une matrice de score
  a2_commun.bootstrap_personnes                IC par reechantillonnage de personnes

CE QUI EST REPRIS EN LE REECRIVANT, faute de pouvoir importer une branche non fusionnee
(le mandat interdit d'ecrire analyses/c7_equite_risque.py) :
  risque_a_bassin_constant   formule identique a c7_equite_risque, meme transformation
                             deterministe et monotone du rang ; verifiee en reproduisant
                             les chiffres publies de la branche attaquee (section 1).
  atypicite / coherence_test_retest  definitions identiques a c7_equite_risque, pour que
                             la replication porte sur exactement les memes variables.

CE QUI EST NOUVEAU ICI, et rien d'autre :
  attaquant_trivial          le TEMOIN de tautologie : un « jumeau » qui est simplement
                             les reponses v1-3 de la personne elle-meme. Aucun modele de
                             langage. Si le corrélat de coherence est le meme ou plus fort
                             chez lui, il ne dit rien du jumeau LLM.
  rarete_moyenne             -log q_j(x_ij) moyen sous les marginales de population,
                             estimees EN LAISSANT LA PERSONNE DEHORS (leave-one-out).
  loglik_classes_latentes    log-vraisemblance HORS PLI des reponses de la personne sous
                             un modele de classes latentes ajuste sur les AUTRES personnes.
                             Mesure de predictibilite qui N'UTILISE PAS le retest.
  spearman_partiel           correlation partielle de rang (residus de regression sur les
                             rangs des covariables), avec IC bootstrap sur les personnes.
  le rejeu du corrélat central sous A-LLR, a bassin strictement identique.

Aucun appel de modele de langage, aucune depense, aucun reseau, aucun arriere-plan.
Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_audit_predictibilite.py
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
from scipy.special import gammaln, logsumexp
from scipy.stats import rankdata, spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                            # noqa: E402
from a2_commun import bootstrap_personnes                          # noqa: E402
from c7_reidentification import (                                  # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)
import c7_stanford as CS                                           # noqa: E402
from c7_attaquant_fort import scores_hors_pli                      # noqa: E402

GRAINE = 20260913
CIBLE = "JSON Persona - GPT4.1"     # le jumeau des chiffres publies
B_PRINCIPAL = 100                    # bassin constant, identique a la branche attaquee
N_BOOT = 1000                        # tirages bootstrap (reduction declaree : 2 000 -> 1 000,
                                     # les correlations partielles etant recalculees a chaque
                                     # tirage ; l'IC bouge de moins de 0,003 en essai)
N_TIRAGES_LIENS = 20
N_PLIS = 5
N_CLASSES = 12                       # classes latentes du modele de predictibilite
N_EM = 80                            # iterations EM


# ---------------------------------------------------------------------------
# 1. Le risque individuel a bassin constant (formule de c7_equite_risque)
# ---------------------------------------------------------------------------

def risque_a_bassin_constant(rang, n_pool, b):
    """p_i(b) = C(M - c_i, b - 1) / C(M, b - 1), avec c_i = R_i - 1 et M = n_pool - 1.

    Probabilite que la vraie personne soit premiere dans un bassin de taille b tire au
    hasard qui la contient. Transformation DETERMINISTE ET MONOTONE du rang, pas une
    nouvelle attaque. Le bassin b est le MEME pour tout le monde et pour toutes les
    conditions comparees : c'est le garde-fou qui a deja coute deux erreurs a ce projet.
    """
    c = np.asarray(rang, dtype=float) - 1.0
    m = float(n_pool - 1)
    k = float(b - 1)
    if k <= 0:
        return np.ones_like(c)
    reste = m - c - k + 1.0
    log_p = (gammaln(m - c + 1.0) - gammaln(np.maximum(reste, 1e-300))
             - gammaln(m + 1.0) + gammaln(m - k + 1.0))
    p = np.where(reste > 0, np.exp(np.clip(log_p, -700, 0.0)), 0.0)
    return np.clip(p, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 2. Les caracteristiques de la personne
# ---------------------------------------------------------------------------

def atypicite(codes_humains):
    """Definition de la branche attaquee : fraction des items ou la reponse differe du
    mode de la population."""
    x = np.asarray(codes_humains)
    modes = np.array([np.bincount(col[col >= 0]).argmax() if (col >= 0).any() else -1
                      for col in x.T])
    return (x != modes[None, :]).mean(axis=1)


def coherence_test_retest(v4, v13):
    """Definition de la branche attaquee : accord item par item entre v4 et v1-3."""
    return (np.asarray(v4) == np.asarray(v13)).mean(axis=1)


def rarete_moyenne_loo(x):
    """-log q_j(x_ij) moyen sur les items, marginales estimees SANS la personne.

    Deuxieme definition de la rarete, demandee par le mandat : elle ne depend pas d'un
    mode unique et pondere chaque reponse par sa frequence reelle, ce qui evite que la
    mesure soit dominee par la structure des items a nombreuses modalites. Le retrait de
    la personne (leave-one-out) empeche qu'une modalite portee par elle seule soit jugee
    frequente grace a elle-meme.
    """
    x = np.asarray(x)
    n, p = x.shape
    out = np.zeros((n, p))
    for j in range(p):
        col = x[:, j]
        n_mod = int(col.max()) + 1
        comptes = np.bincount(col, minlength=n_mod).astype(float)
        # marginale lissee, personne retiree : (c_v - 1 + 1) / (n - 1 + n_mod)
        q = (comptes[col] - 1.0 + 1.0) / (n - 1.0 + n_mod)
        out[:, j] = -np.log(np.clip(q, 1e-12, 1.0))
    return out.mean(axis=1)


def _em_classes_latentes(x_entr, n_mods, rng):
    """EM d'un modele de classes latentes categoriel sur les personnes d'entrainement."""
    n, p = x_entr.shape
    c = N_CLASSES
    resp = rng.dirichlet(np.ones(c), size=n)
    theta = [None] * p
    pi = resp.mean(axis=0)
    # masques d'appartenance par item et modalite, calcules une seule fois
    masques = [[np.flatnonzero(x_entr[:, j] == v) for v in range(n_mods[j])]
               for j in range(p)]
    for _ in range(N_EM):
        # M : theta[j][classe, modalite], lissage de Laplace
        for j in range(p):
            m = n_mods[j]
            acc = np.empty((c, m))
            for v in range(m):
                idx = masques[j][v]
                acc[:, v] = resp[idx].sum(axis=0) if len(idx) else 0.0
            theta[j] = (acc + 1.0) / (acc.sum(axis=1, keepdims=True) + m)
        pi = resp.mean(axis=0) + 1e-12
        pi /= pi.sum()
        # E
        lp = np.tile(np.log(pi), (n, 1))
        for j in range(p):
            lp += np.log(theta[j][:, x_entr[:, j]]).T
        resp = np.exp(lp - logsumexp(lp, axis=1, keepdims=True))
    return pi, theta


def loglik_hors_pli(x, plis_idx, graine):
    """Log-vraisemblance moyenne par item des reponses de la personne sous un modele de
    classes latentes ajuste sur les AUTRES personnes (hors pli).

    C'est la mesure de predictibilite demandee par le mandat : elle N'UTILISE PAS le
    retest, donc elle ne peut pas etre contaminee par le bruit de mesure de la personne.
    Elle capture la structure entre items, pas seulement les marginales -- c'est ce qui
    la distingue de la rarete.
    """
    x = np.asarray(x)
    n, p = x.shape
    n_mods = [int(x[:, j].max()) + 1 for j in range(p)]
    out = np.zeros(n)
    for k, pli in enumerate(plis_idx):
        entr = np.setdiff1d(np.arange(n), pli)
        rng = np.random.default_rng([graine, 41, k])
        pi, theta = _em_classes_latentes(x[entr], n_mods, rng)
        lp = np.tile(np.log(pi), (len(pli), 1))
        for j in range(p):
            lp += np.log(theta[j][:, x[pli, j]]).T
        out[pli] = logsumexp(lp, axis=1) / p
    return out


# ---------------------------------------------------------------------------
# 3. Correlations de rang, simples et partielles
# ---------------------------------------------------------------------------

def _residus_rang(y, covars):
    """Residus de la regression lineaire des rangs de y sur les rangs des covariables."""
    ry = rankdata(y)
    if covars is None or len(covars) == 0:
        return ry - ry.mean()
    z = np.column_stack([rankdata(c) for c in covars])
    z = np.column_stack([np.ones(len(ry)), z])
    beta, *_ = np.linalg.lstsq(z, ry, rcond=None)
    return ry - z @ beta


def spearman_partiel(a, b, covars=None):
    """Spearman partiel : correlation de Pearson entre les residus de rang.

    Sans covariable, c'est exactement le Spearman ordinaire -- ce qui permet d'utiliser
    la meme fonction, donc le meme bootstrap, pour les corrélations brutes et partielles.
    """
    ra = _residus_rang(a, covars)
    rb = _residus_rang(b, covars)
    sa, sb = ra.std(), rb.std()
    if sa < 1e-12 or sb < 1e-12:
        return np.nan
    return float(np.mean(ra * rb) / (sa * sb))


def boot_ic(vecteurs, fonction, graine, n_tirages=N_BOOT):
    """IC 95 % par reechantillonnage des PERSONNES, la statistique etant RECALCULEE dans
    chaque tirage (une correlation partielle n'a pas d'IC analytique utilisable ici)."""
    rng = np.random.default_rng(graine)
    n = len(vecteurs[0])
    val = fonction(*vecteurs)
    tirages = np.empty(n_tirages)
    for t in range(n_tirages):
        idx = rng.integers(0, n, n)
        tirages[t] = fonction(*[v[idx] for v in vecteurs])
    bas, haut = np.nanpercentile(tirages, [2.5, 97.5])
    return float(val), float(bas), float(haut)


# ---------------------------------------------------------------------------
# 4. Programme
# ---------------------------------------------------------------------------

def main():
    t0 = time.time()
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes = []

    def note(bloc, quantite, valeur, bas=np.nan, haut=np.nan, reference=np.nan, com=""):
        lignes.append({"bloc": bloc, "quantite": quantite, "valeur": valeur,
                       "ic_bas": bas, "ic_haut": haut, "reference": reference,
                       "commentaire": com})

    paq = T1.charger()
    codes = paq["codes"]
    n_total = paq["n"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool_v4 = codes[REF_V4][:, items]
    pool_v13 = codes[REF_V13][:, items]
    x = codes[CIBLE][:, items]
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))
    print(f"{n_total} personnes, {len(items)} items communs, "
          f"{len(couverts)} jumeaux couverts pour {CIBLE}", flush=True)

    # --- BASSIN : identique partout. Une seule verification, une seule fois. ---
    print(f"\nBASSIN CONSTANT : pool = {pool_v4.shape[0]} humains v4, "
          f"attaques = {len(couverts)}, B = {B_PRINCIPAL} pour toutes les conditions.",
          flush=True)

    # === 1. Replication de l'attaque naive et du risque publie ===
    print("\n=== 1. Replication : attaque naive (Hamming), jumeau LLM ===", flush=True)
    rng = np.random.default_rng([GRAINE, graine_nom(CIBLE)])
    rang_llm, top1_llm, _ = rangs_attaque(x[couverts], pool_v4, couverts, rng,
                                          N_TIRAGES_LIENS)
    r_llm = risque_a_bassin_constant(rang_llm, n_total, B_PRINCIPAL)
    r_llm_n = risque_a_bassin_constant(rang_llm, n_total, n_total)
    print(f"  top-1 = {top1_llm.mean():.4f} ; risque moyen p(B=100) = {r_llm.mean():.4f} ; "
          f"p(B=N) moyen = {r_llm_n.mean():.4f}", flush=True)
    note("1 replication", "top-1 jumeau LLM, attaque naive", float(top1_llm.mean()),
         reference=0.2069, com="branche attaquee : 0,2069")
    note("1 replication", "risque moyen p(B=100), jumeau LLM naif", float(r_llm.mean()))

    # === 2. Le temoin trivial : un « jumeau » qui est la personne elle-meme en v1-3 ===
    print("\n=== 2. Temoin de tautologie : attaquant TRIVIAL (v1-3 de la personne) ===",
          flush=True)
    rng_t = np.random.default_rng([GRAINE, graine_nom("trivial")])
    rang_tri, top1_tri, _ = rangs_attaque(pool_v13[couverts], pool_v4, couverts, rng_t,
                                          N_TIRAGES_LIENS)
    r_tri = risque_a_bassin_constant(rang_tri, n_total, B_PRINCIPAL)
    print(f"  top-1 = {top1_tri.mean():.4f} ; risque moyen p(B=100) = {r_tri.mean():.4f}",
          flush=True)
    note("2 temoin trivial", "top-1 attaquant trivial (v1-3 vs v4), aucun LLM",
         float(top1_tri.mean()), com="meme bassin, memes items, meme B")
    note("2 temoin trivial", "risque moyen p(B=100), attaquant trivial", float(r_tri.mean()))

    # === 3. Les caracteristiques ===
    print("\n=== 3. Caracteristiques de la personne (hors pli la ou c'est necessaire) ===",
          flush=True)
    hum4_c = pool_v4[couverts]
    hum13_c = pool_v13[couverts]
    rng_p = np.random.default_rng([GRAINE, 40])
    plis_idx = np.array_split(rng_p.permutation(len(couverts)), N_PLIS)

    atyp = atypicite(pool_v4)[couverts]
    coh = coherence_test_retest(hum4_c, hum13_c)
    rarete = rarete_moyenne_loo(hum4_c)
    n_items108 = (codes[REF_V4] >= 0).sum(axis=1)[couverts].astype(float)
    t_lc = time.time()
    pred_lc = loglik_hors_pli(hum4_c, plis_idx, GRAINE)
    print(f"  modele de classes latentes ({N_CLASSES} classes, {N_PLIS} plis, {N_EM} EM) : "
          f"{time.time() - t_lc:.0f} s", flush=True)

    carac = {
        "atypicite (distance au mode)": atyp,
        "rarete moyenne (-log marginale, leave-one-out)": rarete,
        "predictibilite hors pli (log-vrais. classes latentes)": pred_lc,
        "coherence test-retest (v4 vs v1-3)": coh,
        "nombre de reponses non manquantes (108 items)": n_items108,
    }

    # --- 3bis : les caracteristiques sont-elles independantes entre elles ? ---
    print("\n--- 3bis. rarete et stabilite sont-elles la meme chose ? ---", flush=True)
    paires = [("atypicite (distance au mode)", "coherence test-retest (v4 vs v1-3)"),
              ("atypicite (distance au mode)",
               "rarete moyenne (-log marginale, leave-one-out)"),
              ("atypicite (distance au mode)",
               "predictibilite hors pli (log-vrais. classes latentes)"),
              ("coherence test-retest (v4 vs v1-3)",
               "predictibilite hors pli (log-vrais. classes latentes)"),
              ("rarete moyenne (-log marginale, leave-one-out)",
               "predictibilite hors pli (log-vrais. classes latentes)")]
    for a_nom, b_nom in paires:
        rho = float(spearmanr(carac[a_nom], carac[b_nom]).statistic)
        print(f"  rho({a_nom[:34]:34s}, {b_nom[:34]:34s}) = {rho:+.3f}", flush=True)
        note("3bis structure", f"Spearman {a_nom} ~ {b_nom}", rho)

    # === 4. Correlats bruts, par attaquant ===
    print("\n=== 4. Correlats du risque, attaque naive (replication) et temoin trivial ===",
          flush=True)
    for nom_att, risque in (("naif Hamming / jumeau LLM", r_llm),
                            ("TRIVIAL (v1-3, aucun LLM)", r_tri)):
        for nom_c, vec in carac.items():
            rho, bas, haut = boot_ic((risque, vec), spearman_partiel,
                                     [GRAINE, 50, graine_nom(nom_att + nom_c)])
            print(f"  {nom_att:28s} rho({nom_c[:40]:40s}) = {rho:+.3f} [{bas:+.3f};{haut:+.3f}]",
                  flush=True)
            note(f"4 correlats bruts / {nom_att}", f"Spearman risque ~ {nom_c}",
                 rho, bas, haut)

    # === 5. Le test de tautologie : mediation par l'attaquant trivial ===
    print("\n=== 5. TAUTOLOGIE : l'effet de coherence survit-il au controle du temoin "
          "trivial ? ===", flush=True)
    rho_med, b_med, h_med = boot_ic(
        (r_llm, coh, r_tri),
        lambda a, b, c: spearman_partiel(a, b, [c]),
        [GRAINE, 51])
    print(f"  rho(risque_LLM, coherence | risque_TRIVIAL) = {rho_med:+.3f} "
          f"[{b_med:+.3f};{h_med:+.3f}]   (P2 : < +0,10 en valeur absolue)", flush=True)
    note("5 tautologie", "Spearman partiel risque_LLM ~ coherence | risque_trivial",
         rho_med, b_med, h_med, reference=0.256,
         com="brut sur la branche attaquee : +0,256")
    rho_ata, b_ata, h_ata = boot_ic(
        (r_llm, atyp, r_tri),
        lambda a, b, c: spearman_partiel(a, b, [c]),
        [GRAINE, 52])
    print(f"  rho(risque_LLM, atypicite  | risque_TRIVIAL) = {rho_ata:+.3f} "
          f"[{b_ata:+.3f};{h_ata:+.3f}]", flush=True)
    note("5 tautologie", "Spearman partiel risque_LLM ~ atypicite | risque_trivial",
         rho_ata, b_ata, h_ata, reference=-0.181)

    # --- 5bis : le controle precedent est SATURE, donc trop faible. On recommence sur le
    # RANG de l'attaquant trivial, qui lui n'a pas de plafond. Sans cette correction, la
    # mediation est SOUS-estimee : p_trivial(B=100) vaut 1 pour une forte fraction des
    # personnes, ce qui produit un paquet d'ex aequo et un controle qui ne controle rien.
    print("\n--- 5bis. meme test, controle par le RANG trivial (non sature) ---", flush=True)
    print(f"  (rappel : {np.mean(r_tri > 0.999):.1%} des personnes sont a p_trivial = 1)",
          flush=True)
    note("5bis tautologie", "fraction des personnes a p_trivial(B=100) > 0,999",
         float(np.mean(r_tri > 0.999)), com="saturation du controle de la section 5")
    for nom_v, vec, ref in (("coherence", coh, 0.256), ("atypicite", atyp, -0.181)):
        rho_b, b_b, h_b = boot_ic(
            (r_llm, vec, rang_tri),
            lambda a, b, c: spearman_partiel(a, b, [c]),
            [GRAINE, 54, graine_nom(nom_v)])
        print(f"  rho(risque_LLM, {nom_v:10s} | RANG trivial) = {rho_b:+.3f} "
              f"[{b_b:+.3f};{h_b:+.3f}]", flush=True)
        note("5bis tautologie", f"Spearman partiel risque_LLM ~ {nom_v} | rang trivial",
             rho_b, b_b, h_b, reference=ref)

    # === 6. Analyse partielle rarete x stabilite x nombre d'items ===
    print("\n=== 6. Partielles : atypicite et coherence, chacune a l'autre tenue "
          "constante ===", flush=True)
    jeux = {
        "atypicite | coherence": (r_llm, atyp, [coh]),
        "atypicite | coherence + n_items": (r_llm, atyp, [coh, n_items108]),
        "atypicite | coherence + predictibilite hors pli": (r_llm, atyp, [coh, pred_lc]),
        "coherence | atypicite": (r_llm, coh, [atyp]),
        "coherence | atypicite + n_items": (r_llm, coh, [atyp, n_items108]),
        "coherence | atypicite + predictibilite hors pli": (r_llm, coh, [atyp, pred_lc]),
        "predictibilite hors pli | coherence": (r_llm, pred_lc, [coh]),
        "predictibilite hors pli | atypicite": (r_llm, pred_lc, [atyp]),
    }
    for nom_j, (a, b, cov) in jeux.items():
        rho, bas, haut = boot_ic(tuple([a, b] + cov),
                                 lambda *v: spearman_partiel(v[0], v[1], list(v[2:])),
                                 [GRAINE, 53, graine_nom(nom_j)])
        print(f"  rho partiel risque ~ {nom_j:52s} = {rho:+.3f} [{bas:+.3f};{haut:+.3f}]",
              flush=True)
        note("6 partielles (attaque naive)", f"Spearman partiel risque ~ {nom_j}",
             rho, bas, haut)

    # === 7. LE TEST DECISIF : A-LLR pondere par la rarete, bassin identique ===
    print("\n=== 7. DECISIF : attaquant A-LLR (hors pli), bassin STRICTEMENT identique ===",
          flush=True)
    t_llr = time.time()
    s_llr = scores_hors_pli(x[couverts], pool_v4, couverts, "audit|twin|llr")
    rng_l = np.random.default_rng([GRAINE, 60])
    rang_llr, top1_llr, _ = CS.rangs_depuis_accord(s_llr, couverts, rng_l, N_TIRAGES_LIENS)
    r_llr = risque_a_bassin_constant(rang_llr, n_total, B_PRINCIPAL)
    print(f"  A-LLR : top-1 = {top1_llr.mean():.4f} ; risque moyen p(B=100) = "
          f"{r_llr.mean():.4f} ; {time.time() - t_llr:.0f} s", flush=True)
    note("7 A-LLR", "top-1 A-LLR, jumeau LLM", float(top1_llr.mean()), reference=0.232,
         com="c7-attaquant-fort publie : 0,232")
    note("7 A-LLR", "risque moyen p(B=100), A-LLR", float(r_llr.mean()),
         reference=float(r_llm.mean()), com="reference = meme quantite sous Hamming")

    for nom_c, vec in carac.items():
        rho, bas, haut = boot_ic((r_llr, vec), spearman_partiel,
                                 [GRAINE, 61, graine_nom(nom_c)])
        print(f"  A-LLR rho({nom_c[:44]:44s}) = {rho:+.3f} [{bas:+.3f};{haut:+.3f}]",
              flush=True)
        note("7 A-LLR / correlats bruts", f"Spearman risque_A-LLR ~ {nom_c}",
             rho, bas, haut)

    for nom_j, (b, cov) in {
        "atypicite | coherence": (atyp, [coh]),
        "atypicite | coherence + predictibilite hors pli": (atyp, [coh, pred_lc]),
        "coherence | atypicite": (coh, [atyp]),
    }.items():
        rho, bas, haut = boot_ic(tuple([r_llr, b] + cov),
                                 lambda *v: spearman_partiel(v[0], v[1], list(v[2:])),
                                 [GRAINE, 62, graine_nom(nom_j)])
        print(f"  A-LLR rho partiel ~ {nom_j:52s} = {rho:+.3f} [{bas:+.3f};{haut:+.3f}]",
              flush=True)
        note("7 A-LLR / partielles", f"Spearman partiel risque_A-LLR ~ {nom_j}",
             rho, bas, haut)

    # === 8. Stratification : le signe tient-il a coherence constante ? ===
    print("\n=== 8. Stratification par quintile de coherence (aucun groupe < 20) ===",
          flush=True)
    q = np.quantile(coh, [0.2, 0.4, 0.6, 0.8])
    strate = np.digitize(coh, q)
    for nom_att, risque in (("naif Hamming", r_llm), ("A-LLR", r_llr)):
        rhos = []
        for s in range(5):
            m = strate == s
            if m.sum() < 20:
                continue
            rhos.append(float(spearmanr(risque[m], atyp[m]).statistic))
        moy = float(np.mean(rhos))
        print(f"  {nom_att:12s} rho(risque, atypicite) intra-quintile : "
              f"moyenne {moy:+.3f}, min {min(rhos):+.3f}, max {max(rhos):+.3f} "
              f"({len(rhos)} strates)", flush=True)
        note("8 stratification", f"Spearman intra-quintile de coherence, {nom_att} "
             f"(moyenne des 5 strates)", moy, float(min(rhos)), float(max(rhos)))

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-audit-predictibilite.csv")
    print(f"\ndurée totale {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
