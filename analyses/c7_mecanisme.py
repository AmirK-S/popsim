"""
c7_mecanisme : pourquoi les items d'achat servent-ils d'empreinte ?

===========================================================================
PREENREGISTREMENT : resultats/c7-mecanisme-preenregistrement.md, ecrit le 11 septembre
2026, AVANT ce fichier et avant tout calcul.

QUESTION. c7_reidentification.py a montre que le top-1 (JSON Persona - GPT4.1) vient a
33 % des 40 items d'achat (bloc *Product Preferences - Pricing*, QID9_1..40) et a 0,25 %
des 20 autres items communs. Quatre hypotheses non exclusives sont departagees ici :
H1 variance/entropie, H2 sensibilite au prix recopiee, H3 structure de matrice,
H4 stereotypie sur l'opinion.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                les quinze tables de Twin
  a2_commun.bootstrap_personnes     l'intervalle de confiance par reechantillonnage
  c7_reidentification.items_communs / rangs_attaque / graine_nom
                                    l'attaque de reidentification et ses garde-fous

CE QUI EST NOUVEAU ICI : l'identification des 40 items d'achat via la nomenclature
question_catalog.json / wave4_formatted_to_catalog_mapping.json, l'appariement par
entropie (H1), la coherence de seuil de prix (H2), la permutation intra-jumeau (H3),
et le mode de segment en LOO (H4).

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
ETHIQUE : aucun pid ni appariement individuel n'est jamais imprime ou ecrit ; uniquement
des taux agreges.
Usage : .venv/bin/python analyses/c7_mecanisme.py
===========================================================================
"""

import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from scipy.optimize import linear_sum_assignment
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                      # noqa: E402
from a2_commun import bootstrap_personnes, entropie          # noqa: E402
from c7_reidentification import (                            # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)

GRAINE = 20260911
N_BOOTSTRAP = 2000
CIBLE = "JSON Persona - GPT4.1"
RACINE_TWIN = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                            "data", "twin2k500")
BLOC_ACHAT = "Product Preferences - Pricing"


def items_achat(paq, racine=RACINE_TWIN):
    """Les indices, dans les 108 colonnes de la nomenclature commune, des 40 items
    d'achat du bloc Product Preferences - Pricing, retrouves via la meme table de
    correspondance que celle employee par a6_double_distorsion_hors_gss.charger_twin."""
    p_cat = os.path.join(racine, "question_catalog_and_human_response_csv",
                          "question_catalog.json")
    p_map = os.path.join(racine, "llm", "wave4_formatted_to_catalog_mapping.json")
    catalogue = {q["QuestionID"]: q for q in json.load(open(p_cat, encoding="utf-8"))}
    mapping = json.load(open(p_map, encoding="utf-8"))
    achat_cols = {e["formatted_column"] for e in mapping
                  if catalogue[e["QuestionID"]]["BlockName"].strip() == BLOC_ACHAT}
    cols = list(paq["colonnes"])
    return np.array([i for i, c in enumerate(cols) if c in achat_cols])


def top1_sous_ensemble(codes, nom, items_idx, pool_v4, couverts, graine_suffixe):
    """Top-1 (moyenne, IC 95 %) de `nom` contre le pool humain v4, restreint a items_idx.
    Reprend rangs_attaque telle quelle ; seule la restriction de colonnes est nouvelle."""
    x = codes[nom][:, items_idx][couverts]
    rng = np.random.default_rng([GRAINE, graine_suffixe, graine_nom(nom)])
    _, top1, _ = rangs_attaque(x, pool_v4[:, items_idx], couverts, rng)
    return bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP, graine=[GRAINE, graine_suffixe])


# ---------------------------------------------------------------------------
# H1 : variance / entropie
# ---------------------------------------------------------------------------

def test_h1(paq, codes, items, i_achat_rel, i_opinion_rel, pool_v4, couverts):
    """Apparie par assignation hongroise les items d'achat les plus proches en entropie
    humaine (vague 4) des 20 items d'opinion, puis compare le top-1 sur ce sous ensemble
    apparie au top-1 sur les 20 items d'opinion."""
    hum = codes[REF_V4]
    ent = np.array([entropie(hum[:, j][hum[:, j] >= 0]) for j in items])
    ent_achat, ent_opinion = ent[i_achat_rel], ent[i_opinion_rel]
    cout = np.abs(ent_achat[:, None] - ent_opinion[None, :])
    row_ind, col_ind = linear_sum_assignment(cout)   # row_ind[k] <-> col_ind[k], appariement optimal
    achat_apparie_rel = i_achat_rel[row_ind]

    idx_achat_app = items[achat_apparie_rel]
    idx_opinion = items[i_opinion_rel]
    m1, b1, h1 = top1_sous_ensemble(codes, CIBLE, idx_achat_app, pool_v4, couverts, 11)
    m2, b2, h2 = top1_sous_ensemble(codes, CIBLE, idx_opinion, pool_v4, couverts, 12)
    ecart_entropie = float(np.mean(cout[row_ind, col_ind]))
    return {
        "top1_achat_apparie": m1, "top1_achat_apparie_bas": b1, "top1_achat_apparie_haut": h1,
        "top1_opinion": m2, "top1_opinion_bas": b2, "top1_opinion_haut": h2,
        "ecart_entropie_moyen_bits": ecart_entropie,
        "chevauchement_ic": bool(b1 <= h2 and b2 <= h1),
    }


# ---------------------------------------------------------------------------
# H2 : coherence de seuil de prix
# ---------------------------------------------------------------------------

def coherence_seuil(vec_binaire, attractivite):
    """Correlation de Spearman, personne par personne, entre son vecteur d'achat et le
    taux moyen d'achat humain par item (proxy d'attractivite/prix, sans prix exact)."""
    n = vec_binaire.shape[0]
    rho = np.full(n, np.nan)
    for i in range(n):
        v = vec_binaire[i]
        ok = v >= 0
        if ok.sum() >= 10 and len(set(v[ok])) > 1:
            r, _ = spearmanr(v[ok], attractivite[ok])
            rho[i] = r
    return rho


def test_h2(codes, idx_achat, couverts):
    hum = codes[REF_V4][:, idx_achat]
    binaire_hum = np.where(hum >= 0, hum, np.nan)
    attractivite = np.nanmean(binaire_hum, axis=0)  # taux moyen d'achat humain par item

    twin = codes[CIBLE][:, idx_achat][couverts]
    rho_hum = coherence_seuil(hum[couverts], attractivite)
    rho_ai = coherence_seuil(twin, attractivite)

    ok = ~np.isnan(rho_hum) & ~np.isnan(rho_ai)
    m_hum, b_hum, h_hum = bootstrap_personnes(rho_hum, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 21])
    m_ai, b_ai, h_ai = bootstrap_personnes(rho_ai, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 22])

    rng = np.random.default_rng([GRAINE, 23])
    r_obs, _ = spearmanr(rho_hum[ok], rho_ai[ok])
    tirages = []
    idx_ok = np.flatnonzero(ok)
    for _ in range(N_BOOTSTRAP):
        s = rng.choice(idx_ok, size=len(idx_ok), replace=True)
        r, _ = spearmanr(rho_hum[s], rho_ai[s])
        tirages.append(r)
    return {
        "coherence_moyenne_humains": m_hum, "coherence_bas_humains": b_hum, "coherence_haut_humains": h_hum,
        "coherence_moyenne_ia": m_ai, "coherence_bas_ia": b_ai, "coherence_haut_ia": h_ai,
        "correlation_personne_a_personne": float(r_obs),
        "correlation_bas": float(np.percentile(tirages, 2.5)),
        "correlation_haut": float(np.percentile(tirages, 97.5)),
        "n_personnes": int(ok.sum()),
    }


# ---------------------------------------------------------------------------
# H3 : structure de matrice, permutation intra-jumeau
# ---------------------------------------------------------------------------

def test_h3(codes, idx_achat, pool_v4, couverts):
    m_avant, b_avant, h_avant = top1_sous_ensemble(codes, CIBLE, idx_achat, pool_v4, couverts, 31)

    x = codes[CIBLE][:, idx_achat][couverts].copy()
    rng_perm = np.random.default_rng([GRAINE, 32])
    for i in range(x.shape[0]):
        x[i] = rng_perm.permutation(x[i])
    pool_restreint = pool_v4[:, idx_achat]

    rng = np.random.default_rng([GRAINE, 32, graine_nom(CIBLE)])
    _, top1_perm, _ = rangs_attaque(x, pool_restreint, couverts, rng)
    m_apres, b_apres, h_apres = bootstrap_personnes(top1_perm, n_tirages=N_BOOTSTRAP,
                                                      graine=[GRAINE, 33])
    return {
        "top1_avant_permutation": m_avant, "top1_avant_bas": b_avant, "top1_avant_haut": h_avant,
        "top1_apres_permutation": m_apres, "top1_apres_bas": b_apres, "top1_apres_haut": h_apres,
        "plancher_oracle_compte_contre_examen": 0.0029,
    }


# ---------------------------------------------------------------------------
# H4 : stereotypie de segment sur l'opinion
# ---------------------------------------------------------------------------

def taux_accord_mode_loo(codes_item, seg, cible_reponses, exclure_soi):
    """Pour chaque personne, mode du segment en laissant de cote la personne elle meme
    (exclure_soi=True, calibrage sur les humains) ou en gardant tout le segment humain
    (exclure_soi=False, pour comparer le jumeau au meme mode que les humains n'ont pas
    vu leur propre reponse influencer). cible_reponses est le vecteur compare au mode."""
    n = len(codes_item)
    accord = np.full(n, np.nan)
    for g in np.unique(seg):
        if g < 0:
            continue
        membres = np.flatnonzero((seg == g) & (codes_item >= 0))
        if len(membres) < 3:
            continue
        for i in membres:
            if exclure_soi:
                autres = codes_item[membres[membres != i]]
            else:
                autres = codes_item[membres]
            if len(autres) < 2:
                continue
            valeurs, comptes = np.unique(autres, return_counts=True)
            mode = valeurs[np.argmax(comptes)]
            if cible_reponses[i] >= 0:
                accord[i] = float(cible_reponses[i] == mode)
    return accord


def test_h4(codes, idx_opinion, seg_gra, couverts):
    hum = codes[REF_V4]
    twin = codes[CIBLE]
    lignes = []
    for j in idx_opinion:
        acc_hum = taux_accord_mode_loo(hum[:, j], seg_gra, hum[:, j], exclure_soi=True)
        acc_ai = taux_accord_mode_loo(hum[:, j], seg_gra, twin[:, j], exclure_soi=False)
        acc_ai = np.where(couverts_mask(len(hum), couverts), acc_ai, np.nan)
        lignes.append((acc_hum, acc_ai))
    acc_hum_tot = np.nanmean(np.stack([a for a, _ in lignes], axis=1), axis=1)
    acc_ai_tot = np.nanmean(np.stack([a for _, a in lignes], axis=1), axis=1)
    m_hum, b_hum, h_hum = bootstrap_personnes(acc_hum_tot, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 41])
    m_ai, b_ai, h_ai = bootstrap_personnes(acc_ai_tot, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 42])
    return {
        "taux_stereotypie_humains": m_hum, "taux_stereotypie_humains_bas": b_hum,
        "taux_stereotypie_humains_haut": h_hum,
        "taux_stereotypie_ia": m_ai, "taux_stereotypie_ia_bas": b_ai,
        "taux_stereotypie_ia_haut": h_ai,
    }


def couverts_mask(n, couverts):
    m = np.zeros(n, dtype=bool)
    m[couverts] = True
    return m


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]

    items = items_communs(codes, [REF_V4, REF_V13])
    idx_achat_abs = items_achat(paq)
    est_achat = np.isin(items, idx_achat_abs)
    i_achat_rel = np.flatnonzero(est_achat)
    i_opinion_rel = np.flatnonzero(~est_achat)
    print(f"{len(items)} items communs : {len(i_achat_rel)} achat, {len(i_opinion_rel)} opinion",
          flush=True)

    pool_v4 = codes[REF_V4]
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))

    print("\n--- H1 : variance / entropie ---", flush=True)
    r1 = test_h1(paq, codes, items, i_achat_rel, i_opinion_rel, pool_v4, couverts)
    print(r1, flush=True)

    print("\n--- H2 : coherence de seuil de prix ---", flush=True)
    r2 = test_h2(codes, items[i_achat_rel], couverts)
    print(r2, flush=True)

    print("\n--- H3 : permutation intra-jumeau ---", flush=True)
    r3 = test_h3(codes, items[i_achat_rel], pool_v4, couverts)
    print(r3, flush=True)

    print("\n--- H4 : stereotypie de segment ---", flush=True)
    r4 = test_h4(codes, items[i_opinion_rel], seg_gra, couverts)
    print(r4, flush=True)

    T1.ecrire(pd.DataFrame([r1]), "c7-mecanisme-h1.csv")
    T1.ecrire(pd.DataFrame([r2]), "c7-mecanisme-h2.csv")
    T1.ecrire(pd.DataFrame([r3]), "c7-mecanisme-h3.csv")
    T1.ecrire(pd.DataFrame([r4]), "c7-mecanisme-h4.csv")


if __name__ == "__main__":
    main()
