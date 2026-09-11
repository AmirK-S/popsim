"""
c7_deviations : la fuite de c7_reidentification vient-elle de la partie previsible ou de
l'ecart personnel ?

===========================================================================
PREENREGISTREMENT : resultats/c7-deviations-preenregistrement.md, ecrit le 12 septembre
2026, AVANT ce fichier et avant tout calcul.

QUESTION. c7-contre-examen-2026-09-11.md constate qu'a exactitude comparable (0,47 a 0,59)
un jumeau LLM retrouve la personne dans 20,7 % des cas contre 0,23 % pour PMM et 0,07 %
pour B2. Hypothese : les predicteurs statistiques ramenent chacun vers le mode de l'item
(ou du segment), le jumeau produit au contraire des ecarts personnels coherents, et ce sont
ces ecarts qui signent la personne.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                    les quinze tables de Twin
  t1_baselines.calculer                B0 mode/tirage, B1 argmax, B2 argmax, PMM k=10
  c7_reidentification.items_communs    les 60 items toujours renseignes
  c7_reidentification.rangs_attaque    l'attaque de reidentification et ses garde-fous
  c7_reidentification.graine_nom       une graine stable par nom de configuration
  a2_commun.distance_hamming           la distance de Hamming normalisee, masquage deja fait
  a2_commun.bootstrap_personnes        l'intervalle de confiance par reechantillonnage

CE QUI EST NOUVEAU ICI : la decomposition mode-de-l-item / ecart personnel, la mesure de
part d'ecarts / justesse / diversite, les trois regimes d'attaque (complet, previsible
seul, ecarts seuls) et la sous-partition ecarts corrects / ecarts faux.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
ETHIQUE : aucun pid ni appariement individuel n'est jamais imprime ou ecrit ; uniquement
des taux agreges.
Usage : .venv/bin/python analyses/c7_deviations.py
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                        # noqa: E402
import t1_baselines as TB                                      # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes     # noqa: E402
from c7_reidentification import (                              # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13, CONFIGURATIONS,
)

GRAINE = 20260912
N_BOOTSTRAP = 2000
BASELINES = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]
PREDICTEURS = [REF_V13] + CONFIGURATIONS + BASELINES
REGIMES = ["complet", "previsible", "ecarts", "ecarts_correct", "ecarts_faux"]


def modes_reference(codes_ref, items):
    """La modalite modale de chaque item, une fois, sur les humains vague 4."""
    sub = codes_ref[:, items]
    modes = np.zeros(len(items), dtype=np.int64)
    for j in range(len(items)):
        col = sub[:, j]
        col = col[col >= 0]
        vals, comptes = np.unique(col, return_counts=True)
        modes[j] = vals[np.argmax(comptes)]
    return modes


def decomposer(mat, items, modes):
    """Retourne (reponses, valide, ecart) sur le sous ensemble d'items, -1 = manquant."""
    r = mat[:, items]
    valide = r >= 0
    ecart = (r != modes[None, :]) & valide
    return r, valide, ecart


def mesures_decomposition(nom, r_c, dev_c, correct_c, truth_dev_c, pred_c=None):
    """Part d'ecarts, justesse des ecarts, taux de deviation humaine de reference,
    avec IC 95 % par personne (a2_commun.bootstrap_personnes)."""
    part_personne = dev_c.mean(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        justesse_personne = np.where(dev_c.sum(axis=1) > 0,
                                      correct_c.sum(axis=1) / np.maximum(dev_c.sum(axis=1), 1),
                                      np.nan)
    justesse_personne = np.where(dev_c.sum(axis=1) > 0, justesse_personne, np.nan)
    taux_humain_personne = truth_dev_c.mean(axis=1)

    g = graine_nom(nom)
    m_p, b_p, h_p = bootstrap_personnes(part_personne, N_BOOTSTRAP, [GRAINE, 1, g])
    m_j, b_j, h_j = bootstrap_personnes(justesse_personne, N_BOOTSTRAP, [GRAINE, 2, g])
    m_h, b_h, h_h = bootstrap_personnes(taux_humain_personne, N_BOOTSTRAP, [GRAINE, 3, g])
    return {
        "part_ecarts": m_p, "part_ecarts_bas": b_p, "part_ecarts_haut": h_p,
        "justesse_ecarts": m_j, "justesse_bas": b_j, "justesse_haut": h_j,
        "taux_deviation_humaine_ref": m_h, "taux_deviation_humaine_bas": b_h,
        "taux_deviation_humaine_haut": h_h,
    }


def diversite_paires(r_c):
    """Distance de Hamming moyenne entre paires de personnes simulees (hors diagonale)."""
    n = r_c.shape[0]
    if n < 2:
        return float("nan")
    d = distance_hamming(r_c, r_c)
    hors_diag = ~np.eye(n, dtype=bool)
    return float(d[hors_diag].mean())


def attaque_regime(nom, x, pool, couverts, suffixe, rng_tag):
    """Une attaque (rangs_attaque, deja ecrite) sur un regime donne, IC par bootstrap."""
    rng = np.random.default_rng([GRAINE, rng_tag, graine_nom(nom)])
    _, top1, top10 = rangs_attaque(x, pool, couverts, rng)
    m_t1, b_t1, h_t1 = bootstrap_personnes(top1, N_BOOTSTRAP, [GRAINE, 4, rng_tag, graine_nom(nom)])
    m_t10, _, _ = bootstrap_personnes(top10, N_BOOTSTRAP, [GRAINE, 5, rng_tag, graine_nom(nom)])
    return {"regime": suffixe, "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1, "top10": m_t10}


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t0 = time.time()
    paq = T1.charger()
    codes = dict(paq["codes"])
    print(f"charge en {time.time() - t0:.0f}s, {paq['n']} personnes", flush=True)

    t0 = time.time()
    baselines = TB.calculer(paq, avec_pmm=True)
    codes.update(baselines)
    print(f"baselines calculees en {time.time() - t0:.0f}s : {list(baselines)}", flush=True)

    items = items_communs(codes, [REF_V4, REF_V13])
    print(f"{len(items)} items communs", flush=True)
    modes = modes_reference(codes[REF_V4], items)

    truth_r, _, truth_dev = decomposer(codes[REF_V4], items, modes)
    pool_complet = truth_r
    pool_previsible = np.tile(modes, (truth_r.shape[0], 1))
    pool_ecarts = np.where(truth_dev, truth_r, -1)

    lignes_decomp, lignes_fuite = [], []
    n_hasard = truth_r.shape[0]

    for nom in PREDICTEURS:
        if nom not in codes:
            print(f"absent : {nom}", flush=True)
            continue
        t0 = time.time()
        r, valide, dev = decomposer(codes[nom], items, modes)
        couverts = np.flatnonzero(valide.all(axis=1))
        n_c = len(couverts)
        if n_c < 2:
            print(f"{nom} : couverture insuffisante ({n_c})", flush=True)
            continue

        r_c, dev_c = r[couverts], dev[couverts]
        truth_r_c, truth_dev_c = truth_r[couverts], truth_dev[couverts]
        correct_c = dev_c & (r_c == truth_r_c)
        wrong_c = dev_c & ~correct_c

        ligne = {"predicteur": nom, "n": n_c}
        ligne.update(mesures_decomposition(nom, r_c, dev_c, correct_c, truth_dev_c))
        ligne["diversite"] = diversite_paires(r_c)
        lignes_decomp.append(ligne)

        x_previsible = np.tile(modes, (n_c, 1))
        x_ecarts = np.where(dev_c, r_c, -1)
        x_correct = np.where(correct_c, r_c, -1)
        x_faux = np.where(wrong_c, r_c, -1)

        regimes = [
            ("complet", r_c, pool_complet, 10),
            ("previsible", x_previsible, pool_previsible, 11),
            ("ecarts", x_ecarts, pool_ecarts, 12),
            ("ecarts_correct", x_correct, pool_ecarts, 13),
            ("ecarts_faux", x_faux, pool_ecarts, 14),
        ]
        for suffixe, x, pool, tag in regimes:
            res = attaque_regime(nom, x, pool, couverts, suffixe, tag)
            res["predicteur"] = nom
            res["n"] = n_c
            res["top1_hasard"] = 1.0 / n_hasard
            lignes_fuite.append(res)

        print(f"{nom} : n={n_c}, part_ecarts={ligne['part_ecarts']:.3f}, "
              f"justesse={ligne['justesse_ecarts']:.3f}, diversite={ligne['diversite']:.3f}, "
              f"top1 complet={[x for x in lignes_fuite if x['predicteur']==nom and x['regime']=='complet'][0]['top1']:.4f}, "
              f"({time.time() - t0:.0f}s)", flush=True)

    T1.ecrire(pd.DataFrame(lignes_decomp), "c7-deviations-decomposition.csv")
    T1.ecrire(pd.DataFrame(lignes_fuite), "c7-deviations-fuite.csv")


if __name__ == "__main__":
    main()
