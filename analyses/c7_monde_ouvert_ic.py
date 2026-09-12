"""
c7_monde_ouvert_ic : intervalles de confiance bootstrap pour A3 (monde ouvert, attaque naive)

===========================================================================
PREENREGISTREMENT (ecrit ci-dessous, AVANT tout calcul de bootstrap) :

Defaut vise : A3 (l'attaque en monde ouvert, resultats/c7-monde-ouvert-resultats.md,
`analyses/c7_monde_ouvert.py`) est publiee sans intervalle de confiance. Les chiffres
concernes ICI sont ceux que produit c7_monde_ouvert.py lui-meme (attaque NAIVE par accord
de Hamming) : TPR a FPR = 0,1 % et 1 % pour le meilleur jumeau Twin (JSON Persona GPT4.1,
0,93 % / 3,04 %), le meilleur agent Stanford (composite, 8,47 % / 20,39 %), les comparateurs
(Demographics Only, PMM k=10, environ 0 %) et le plafond humain (retest, 36,9-63,5 % / 54,5-
90,7 %). Le chiffre 60,17 % (et 44,37 %, 4,28 %, 1,01 %) cite dans le meme volet A3 vient de
l'ATTAQUANT FORT (`analyses/c7_attaquant_fort.py`, A-LLR hors pli) : ce script n'importe QUE
c7_monde_ouvert.py et c7_reidentification.py (consigne explicite), donc le 60,17 % est HORS
PERIMETRE ici et doit etre traite par l'agent qui a la main sur c7_attaquant_fort.py.

Attente 1 (largeur) : a FPR = 1 %, le nombre de personnes est de l'ordre de 1 000-2 000, donc
l'IC sur le TPR a FPR = 1 % devrait rester raisonnable (quelques points de pourcentage).
A FPR = 0,1 %, le seuil est cale sur environ 1 a 2 personnes (Stanford, n=1052) ou 2 a 3
personnes (Twin, n=2058) : l'IC devrait etre TRES large, probablement un facteur 3-10 entre
borne basse et borne haute, et la borne basse pourrait toucher 0.

Attente 2 (rejeu du seuil) : le seuil (la valeur de marge qui donne FPR = 0,1 % ou 1 %) est
choisi APRES avoir vu les donnees : `roc_et_taux` l'obtient par interpolation sur la courbe
ROC empirique du meme echantillon que celui sur lequel le TPR est ensuite lu. Un bootstrap
naif qui fixerait ce seuil une fois pour toutes puis ne rejouerait que le TPR sous-estimerait
la variabilite, surtout a FPR = 0,1 % ou le seuil lui-meme est instable. Attente : l'IC avec
rejeu du seuil dans chaque tirage est PLUS LARGE que l'IC a seuil fixe, l'ecart etant plus
marque a 0,1 % qu'a 1 %.

Methode : bootstrap non parametrique sur les PERSONNES ATTAQUEES (2000 tirages, graine fixee
GRAINE_IC = [20260912, 99, ...]). Le pool de candidats (l'ensemble complet des personnes,
utilise comme reference) N'EST PAS rechantillonne : seules les lignes (personnes attaquees,
avec remise) le sont, ce qui evite le probleme des doublons de colonnes qu'un rechantillonnage
du pool entier introduirait (une meme personne dupliquee comme candidat rendrait la marge de
confiance triviale pour sa propre copie). C'est un bootstrap standard "sur les unites testees,
population de reference fixe". Pour chaque tirage, `marges_deux_regimes` et `roc_et_taux`
(importes de c7_monde_ouvert.py, non modifies) sont appeles a neuf sur l'echantillon
rechantillonne : le seuil est donc recalcule (rejoue) a chaque tirage. Un second jeu de
colonnes ("seuil fixe") applique en plus, pour comparaison, le seuil du seul echantillon
observe a chaque tirage bootstrap, afin de chiffrer l'ecart annonce en attente 2.

Deviation documentee : le nombre de tirages de departage des ex-aequo de marge
(N_TIRAGES_LIENS de c7_monde_ouvert.py, =5) est reduit a 1 DANS LE BOOTSTRAP SEULEMENT, pour
tenir le calcul (2000 x 8 predicteurs x n_tirages) en temps raisonnable ; l'estimation
ponctuelle (avant bootstrap) garde n_tirages=5, identique a c7_monde_ouvert.py. Les ex-aequo
exacts de marge sont rares sur des distances de Hamming continues (60 items Twin, items GSS
Stanford) : cette reduction ne change pas l'ordre de grandeur du bruit de departage, seulement
sa moyenne sur un tirage au lieu de cinq.

Aucun appel de modele de langage, aucun reseau. Lecture seule sur data/. c7_monde_ouvert.py et
c7_reidentification.py sont importes tels quels, aucun fichier existant n'est modifie. Usage :
.venv/bin/python analyses/c7_monde_ouvert_ic.py
===========================================================================
"""

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from a2_commun import distance_hamming, en_codes                         # noqa: E402
from c7_reidentification import items_communs, REF_V4, REF_V13, DEMO     # noqa: E402
import c7_stanford as CS                                                  # noqa: E402
from c7_monde_ouvert import (                                            # noqa: E402
    marges_deux_regimes, roc_et_taux, compte_au_moins, pmm_depuis_demo,
    graine_nom, GRAINE, FPR_CIBLES,
)

N_BOOT = 2000
N_TIRAGES_LIENS_BOOT = 1        # reduit de 5 (voir deviation documentee ci-dessus)
GRAINE_IC = [GRAINE, 99]        # sous-graine fixe, dediee a ce script


# ---------------------------------------------------------------------------
# Reconstruction des matrices d'accord par predicteur (meme protocole que
# bloc_twin/bloc_stanford de c7_monde_ouvert.py, dont on reprend chaque fonction
# de calcul telle quelle ; seule la glue "quelles matrices garder" est reecrite
# ici puisque bloc_twin/bloc_stanford ne renvoient que la ligne resume).
# ---------------------------------------------------------------------------

def accords_twin():
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    n = pool.shape[0]

    demo_codes = en_codes(paq["demo"]["x"])
    rng_pmm = np.random.default_rng([GRAINE, 1])
    pmm = pmm_depuis_demo(demo_codes, pool, rng_pmm)

    sondes = {
        "Meilleur jumeau (JSON Persona GPT4.1)": codes["JSON Persona - GPT4.1"][:, items],
        DEMO: codes[DEMO][:, items],
        "PMM k=10": pmm,
        "Retest humain (plafond)": codes[REF_V13][:, items],
    }
    return {nom: 1.0 - distance_hamming(x, pool) for nom, x in sondes.items()}, n


def accords_stanford():
    ordre, items, tables, _ = CS.charger_domaine("gss")
    codes_gss = CS.coder_categoriel_commun(tables, items)
    pool = codes_gss[CS.VAGUE1]
    n = pool.shape[0]

    demo = pd.read_csv(CS.DEMO_CSV).set_index("email").loc[ordre]
    demo_arr = demo[["gender", "race", "age", "education"]].astype(str).to_numpy(dtype=object)
    demo_codes = en_codes(demo_arr)
    rng_pmm = np.random.default_rng([GRAINE, 3])
    pmm = pmm_depuis_demo(demo_codes, pool, rng_pmm)

    sondes = {
        "Meilleur agent (composite)": codes_gss["composite"],
        "démographique": codes_gss[CS.DEMO_COND],
        "PMM k=10": pmm,
        "Retest humain (plafond)": codes_gss[CS.VAGUE2],
    }
    return {nom: CS.accord_categoriel(x, pool) for nom, x in sondes.items()}, n


# ---------------------------------------------------------------------------
# Seuil (valeur de marge) et nombre absolu de faux positifs qui definissent un
# FPR cible, sur UN echantillon donne (recalcul local, memes fonctions internes
# que roc_et_taux : compte_au_moins, importee sans modification).
# ---------------------------------------------------------------------------

def seuil_et_compte_fp(marge_p, marge_r, f_cible, n):
    seuils = np.unique(np.concatenate([marge_p, marge_r]))
    fp_counts = compte_au_moins(np.sort(marge_r), seuils)
    fpr = fp_counts / n
    ordre = np.argsort(fpr)
    fpr_asc, seuils_asc, counts_asc = fpr[ordre], seuils[ordre], fp_counts[ordre]
    h = float(np.interp(f_cible, fpr_asc, seuils_asc))
    k = float(np.interp(f_cible, fpr_asc, counts_asc))
    return h, k


def percentile_ic(vals):
    lo, hi = np.percentile(vals, [2.5, 97.5])
    return float(lo), float(hi)


# ---------------------------------------------------------------------------
# Bootstrap sur les personnes attaquees, pool de candidats fixe (voir preenreg.)
# ---------------------------------------------------------------------------

def bootstrap_predicteur(nom_jeu, nom_pred, accord, n_boot=N_BOOT, fpr_cibles=FPR_CIBLES):
    n = accord.shape[0]
    vrai0 = np.arange(n)
    tag = graine_nom(f"{nom_jeu}|{nom_pred}")

    rng_pt = np.random.default_rng([GRAINE, 2, tag])           # meme graine/appel que le point publie
    marge_p0, correct0, marge_r0 = marges_deux_regimes(accord, vrai0, rng_pt)
    r0 = roc_et_taux(marge_p0, correct0, marge_r0, n)
    top1_0 = float(correct0.mean())

    seuils_pt = {f: seuil_et_compte_fp(marge_p0, marge_r0, f, n) for f in fpr_cibles}

    boot_top1 = np.empty(n_boot)
    boot_tpr_rejoue = {f: np.empty(n_boot) for f in fpr_cibles}
    boot_tpr_fixe = {f: np.empty(n_boot) for f in fpr_cibles}

    rng_boot = np.random.default_rng([GRAINE_IC[0], GRAINE_IC[1], tag])
    t0 = time.time()
    for b in range(n_boot):
        idx = rng_boot.integers(0, n, size=n)
        accord_b = accord[idx, :]                 # lignes (attaques) rechantillonnees, pool colonne inchange
        marge_p_b, correct_b, marge_r_b = marges_deux_regimes(
            accord_b, idx, rng_boot, n_tirages=N_TIRAGES_LIENS_BOOT
        )
        boot_top1[b] = correct_b.mean()

        r_b = roc_et_taux(marge_p_b, correct_b, marge_r_b, n)
        tpr_num_b = marge_p_b[correct_b >= 0.5]
        for f in fpr_cibles:
            boot_tpr_rejoue[f][b] = r_b["tpr_fpr_0_1pct"] if f == 0.001 else r_b["tpr_fpr_1pct"]
            h_pt = seuils_pt[f][0]
            boot_tpr_fixe[f][b] = float(np.sum(tpr_num_b >= h_pt)) / n

    dt = time.time() - t0
    print(f"{nom_jeu:9s} / {nom_pred:38s} top1={top1_0:.4f} "
          f"TPR@0,1%={r0['tpr_fpr_0_1pct']:.4f} TPR@1%={r0['tpr_fpr_1pct']:.4f} "
          f"[{n_boot} tirages, {dt:.1f}s]", flush=True)

    ligne = {
        "jeu": nom_jeu, "predicteur": nom_pred, "n": n,
        "top1_monde_ferme": top1_0,
        "top1_ic_bas": percentile_ic(boot_top1)[0], "top1_ic_haut": percentile_ic(boot_top1)[1],
    }
    for f in fpr_cibles:
        cle = "0_1pct" if f == 0.001 else "1pct"
        tpr_pt = r0["tpr_fpr_0_1pct"] if f == 0.001 else r0["tpr_fpr_1pct"]
        h_pt, k_pt = seuils_pt[f]
        lo_r, hi_r = percentile_ic(boot_tpr_rejoue[f])
        lo_x, hi_x = percentile_ic(boot_tpr_fixe[f])
        ligne[f"tpr_{cle}"] = tpr_pt
        ligne[f"tpr_{cle}_fp_absolus"] = k_pt
        ligne[f"tpr_{cle}_ic_bas_seuil_rejoue"] = lo_r
        ligne[f"tpr_{cle}_ic_haut_seuil_rejoue"] = hi_r
        ligne[f"tpr_{cle}_ic_bas_seuil_fixe"] = lo_x
        ligne[f"tpr_{cle}_ic_haut_seuil_fixe"] = hi_x
    return ligne


def main():
    print(__doc__.split("=" * 75)[1][:400] + " ...", flush=True)

    print("\n=== Chargement Twin ===", flush=True)
    accords_t, n_t = accords_twin()
    print(f"Twin : n={n_t}", flush=True)

    print("\n=== Chargement Stanford ===", flush=True)
    accords_s, n_s = accords_stanford()
    print(f"Stanford : n={n_s}", flush=True)

    lignes = []
    print("\n=== Bootstrap Twin ===", flush=True)
    for nom, accord in accords_t.items():
        lignes.append(bootstrap_predicteur("Twin", nom, accord))

    print("\n=== Bootstrap Stanford ===", flush=True)
    for nom, accord in accords_s.items():
        lignes.append(bootstrap_predicteur("Stanford", nom, accord))

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-monde-ouvert-ic.csv")

    print("\n--- ecart seuil rejoue vs seuil fixe (largeur d'IC, points de %) ---", flush=True)
    for _, row in df.iterrows():
        for cle in ["0_1pct", "1pct"]:
            larg_r = (row[f"tpr_{cle}_ic_haut_seuil_rejoue"] - row[f"tpr_{cle}_ic_bas_seuil_rejoue"]) * 100
            larg_x = (row[f"tpr_{cle}_ic_haut_seuil_fixe"] - row[f"tpr_{cle}_ic_bas_seuil_fixe"]) * 100
            print(f"{row['jeu']:9s} / {row['predicteur']:38s} FPR={cle:6s} "
                  f"largeur rejoue={larg_r:.2f}pp largeur fixe={larg_x:.2f}pp "
                  f"fp_absolus={row[f'tpr_{cle}_fp_absolus']:.2f}", flush=True)


if __name__ == "__main__":
    main()
