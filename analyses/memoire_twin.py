"""
memoire_twin : « les jumeaux numeriques ne sont qu'une memoire » ?

Preenregistrement : resultats/memoire-predictions.md, ecrit le 11 septembre 2026, AVANT ce
script et avant tout calcul.

QUESTION. Si l'on connait deja les reponses passees d'une personne (vagues 1-3 de
Twin-2K-500), un jumeau LLM fait-il mieux sur la vague 4 que la regle bete de persistance
« elle repondra comme la derniere fois » ? Voit-il venir un changement d'avis ?

FAIT DECLARE (audit resultats/twin-ab-audit-provenance-2026-09-11.md, section 2.2, point 1) :
le persona des vagues 1-3 ne contient AUCUNE des 75 QID des 108 items repetes. Le jumeau n'a
donc pas vu la reponse passee a la meme question, alors que la persistance l'utilise. C'est
la question elle-meme, pas un artefact a corriger.

PERIMETRE : les 8 configurations « admissibles sous reserve » de l'audit (exclut les deux
Predicted Output, Finetuning 500, et les deux Persona Summary suspectes). Chaque
configuration sur son propre perimetre de personnes (regle t1 : jamais de valeur absolue
comparee entre perimetres).

CE QUI EST IMPORTE TEL QUEL : t1_commun.charger (quinze tables Twin, segmentations,
constantes REF/PLANCHER), le cache de t1_baselines.py (B0 mode, B0 tirage, B1, B2, PMM si
disponible).

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.

Usage : .venv/bin/python analyses/memoire_twin.py [--cache-baselines CHEMIN]
"""

import argparse
import os
import pickle
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np                                    # noqa: E402
import pandas as pd                                   # noqa: E402
from sklearn.metrics import roc_auc_score             # noqa: E402

import t1_commun as C                                 # noqa: E402

REF = C.REF
PLANCHER = C.PLANCHER

ADMISSIBLES = [
    "Demographics Only - GPT4.1-mini",
    "JSON Persona - GPT4.1",
    "JSON Persona - GPT4.1-mini",
    "Text Persona (Default Temperature) - GPT4.1-mini",
    "Text Persona (Reasoning) - GPT4.1-mini",
    "Text Persona (Repeating Questions) - GPT4.1-mini",
    "Text Persona - GPT4.1-mini",
    "Text Persona - Gemini-Flash2.5",
]

GRAINE = 20260909
N_BOOT = 1000
SEUIL_VOTE = 5     # sur 8 jumeaux admissibles, regle combinee P4


# ---------------------------------------------------------------------------
# 1. Perimetres et cellules
# ---------------------------------------------------------------------------

def couverture_bool(paq, nom):
    b = np.zeros(paq["n"], dtype=bool)
    b[paq["couverture"][nom]] = True
    return b


def cellules(paq, nom):
    """(i, j) valides pour une configuration : couverte, REF et PLANCHER renseignes,
    prediction de la configuration renseignee. Meme jeu de cellules pour toutes les
    methodes comparees sur cette configuration."""
    ref, pla, cd = paq["codes"][REF], paq["codes"][PLANCHER], paq["codes"][nom]
    couv = couverture_bool(paq, nom)
    masque = couv[:, None] & (ref >= 0) & (pla >= 0) & (cd >= 0)
    return np.nonzero(masque)


# ---------------------------------------------------------------------------
# 2. Bootstrap personnes x items (tirage avec remise independant sur les deux axes)
# ---------------------------------------------------------------------------

def bootstrap_2voies(ii, jj, valeurs, b=N_BOOT, graine=GRAINE):
    """valeurs : dict nom -> tableau aligne sur (ii, jj). Retourne nom -> (point, bas, haut).

    Resample independamment l'ensemble des personnes distinctes et l'ensemble des items
    distincts presents dans le perimetre, puis repondere chaque cellule observee par le
    produit des multiplicites de sa personne et de son item. Evite de materialiser le
    produit cartesien complet.
    """
    pers_u, ci = np.unique(ii, return_inverse=True)
    it_u, cj = np.unique(jj, return_inverse=True)
    n_p, n_j = len(pers_u), len(it_u)
    noms = list(valeurs)
    V = np.stack([valeurs[k].astype(float) for k in noms], axis=1)
    point = {k: float(np.mean(valeurs[k])) for k in noms}
    rng = np.random.default_rng(graine)
    reps = np.empty((b, len(noms)))
    for r in range(b):
        cp = np.bincount(rng.integers(0, n_p, size=n_p), minlength=n_p)
        cq = np.bincount(rng.integers(0, n_j, size=n_j), minlength=n_j)
        w = cp[ci] * cq[cj]
        tot = w.sum()
        reps[r] = (w @ V) / tot if tot > 0 else np.nan
    out = {}
    for k in range(len(noms)):
        bas, haut = np.percentile(reps[:, k], [2.5, 97.5])
        out[noms[k]] = (point[noms[k]], float(bas), float(haut))
    return out


def bootstrap_auc(ii, jj, y, score, b=N_BOOT, graine=GRAINE):
    """Meme schema de tirage, applique a l'AUC ponderee (sample_weight)."""
    pers_u, ci = np.unique(ii, return_inverse=True)
    it_u, cj = np.unique(jj, return_inverse=True)
    n_p, n_j = len(pers_u), len(it_u)
    point = roc_auc_score(y, score) if len(set(y)) > 1 else np.nan
    rng = np.random.default_rng(graine)
    reps = np.empty(b)
    for r in range(b):
        cp = np.bincount(rng.integers(0, n_p, size=n_p), minlength=n_p)
        cq = np.bincount(rng.integers(0, n_j, size=n_j), minlength=n_j)
        w = cp[ci] * cq[cj]
        try:
            reps[r] = roc_auc_score(y, score, sample_weight=w) if len(set(y)) > 1 \
                else np.nan
        except ValueError:
            reps[r] = np.nan
    bas, haut = np.nanpercentile(reps, [2.5, 97.5])
    return point, float(bas), float(haut)


# ---------------------------------------------------------------------------
# 3. Table principale, par configuration
# ---------------------------------------------------------------------------

def ligne_configuration(paq, nom, avec_auc_ic=False):
    ii, jj = cellules(paq, nom)
    ref = paq["codes"][REF][ii, jj]
    pla = paq["codes"][PLANCHER][ii, jj]
    jum = paq["codes"][nom][ii, jj]
    b0 = paq["codes"]["B0 mode"][ii, jj]
    a_pmm = "PMM k=10" in paq["codes"]
    pmm = paq["codes"]["PMM k=10"][ii, jj] if a_pmm else None

    changee = pla != ref
    correct = {
        "persistance": (pla == ref),
        "jumeau": (jum == ref),
        "B0 mode": (b0 == ref) & (b0 >= 0),
    }
    if a_pmm:
        correct["PMM k=10"] = (pmm == ref) & (pmm >= 0)

    ic = bootstrap_2voies(ii, jj, correct)
    ic_ch = bootstrap_2voies(ii[changee], jj[changee],
                             {k: v[changee] for k, v in correct.items()}) \
        if changee.sum() else {k: (np.nan, np.nan, np.nan) for k in correct}

    desaccord = (jum != pla).astype(int)
    if avec_auc_ic:
        auc = bootstrap_auc(ii, jj, changee.astype(int), desaccord)
    else:
        auc_pt = roc_auc_score(changee, desaccord) if len(set(changee)) > 1 else np.nan
        auc = (auc_pt, np.nan, np.nan)

    ligne = {
        "configuration": nom, "n_personnes": int(len(np.unique(ii))),
        "n_cellules": int(len(ii)), "taux_changement": float(np.mean(changee)),
        "auc_desaccord_changement": auc[0], "auc_ic_bas": auc[1], "auc_ic_haut": auc[2],
    }
    for k, (pt, bas, haut) in ic.items():
        ligne[f"exactitude_{k}"] = pt
        ligne[f"exactitude_{k}_ic_bas"] = bas
        ligne[f"exactitude_{k}_ic_haut"] = haut
    for k, (pt, bas, haut) in ic_ch.items():
        ligne[f"exactitude_changees_{k}"] = pt
        ligne[f"exactitude_changees_{k}_ic_bas"] = bas
        ligne[f"exactitude_changees_{k}_ic_haut"] = haut
    return ligne


# ---------------------------------------------------------------------------
# 4. Regle combinee P4 : persistance + accord inter-jumeaux comme proxy de confiance
# ---------------------------------------------------------------------------

def regle_combinee(paq):
    ref, pla = paq["codes"][REF], paq["codes"][PLANCHER]
    couv = np.ones(paq["n"], dtype=bool)
    for nom in ADMISSIBLES:
        couv &= couverture_bool(paq, nom)
    masque = couv[:, None] & (ref >= 0) & (pla >= 0)
    for nom in ADMISSIBLES:
        masque &= (paq["codes"][nom] >= 0)
    ii, jj = np.nonzero(masque)

    k_max = paq["k_max"]
    votes = np.zeros((len(ii), k_max), dtype=np.int16)
    for nom in ADMISSIBLES:
        v = paq["codes"][nom][ii, jj]
        np.add.at(votes, (np.arange(len(ii)), v), 1)
    n_vote = votes.max(axis=1)
    alt = votes.argmax(axis=1)
    pla_v = pla[ii, jj]
    ref_v = ref[ii, jj]
    utiliser_alt = (n_vote >= SEUIL_VOTE) & (alt != pla_v)
    combinee = np.where(utiliser_alt, alt, pla_v)

    correct = {"persistance": (pla_v == ref_v), "combinee": (combinee == ref_v)}
    ic = bootstrap_2voies(ii, jj, correct)
    return {
        "n_personnes": int(len(np.unique(ii))), "n_cellules": int(len(ii)),
        "part_cellules_basculees": float(np.mean(utiliser_alt)),
        "exactitude_persistance": ic["persistance"][0],
        "exactitude_persistance_ic_bas": ic["persistance"][1],
        "exactitude_persistance_ic_haut": ic["persistance"][2],
        "exactitude_combinee": ic["combinee"][0],
        "exactitude_combinee_ic_bas": ic["combinee"][1],
        "exactitude_combinee_ic_haut": ic["combinee"][2],
        "gain_combinee_moins_persistance": ic["combinee"][0] - ic["persistance"][0],
    }


# ---------------------------------------------------------------------------
# 5. Taux de changement global, controle contre l'audit (3 448 cellules, 294 personnes)
# ---------------------------------------------------------------------------

def controle_taux_changement(paq):
    ref, pla = paq["codes"][REF], paq["codes"][PLANCHER]
    masque = (ref >= 0) & (pla >= 0)
    changee = masque & (ref != pla)
    return {
        "personnes": paq["n"], "items": len(paq["colonnes"]),
        "cellules_les_deux_renseignees": int(masque.sum()),
        "cellules_changees": int(changee.sum()),
        "taux_changement": float(changee.sum() / max(masque.sum(), 1)),
    }


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache-baselines", default="/tmp/memoire-baselines-avec-pmm.pkl")
    ap.add_argument("--cache-baselines-repli", default="/tmp/memoire-baselines-sans-pmm.pkl")
    args = ap.parse_args()
    t0 = time.time()

    paq = C.charger()
    chemin = args.cache_baselines if os.path.exists(args.cache_baselines) \
        else args.cache_baselines_repli
    base = pickle.load(open(chemin, "rb"))
    for nom, mat in base.items():
        paq["codes"][nom] = mat
        paq["couverture"][nom] = np.arange(paq["n"])
    print(f"baselines relues depuis {chemin} : {list(base)}", flush=True)

    ctrl = controle_taux_changement(paq)
    print(f"controle taux de changement, {ctrl['personnes']} personnes, "
          f"{ctrl['cellules_changees']} cellules changees sur "
          f"{ctrl['cellules_les_deux_renseignees']} "
          f"({ctrl['taux_changement']:.4f}) ; audit : 3448 sur 294 personnes",
          flush=True)
    C.ecrire([ctrl], "memoire-controle-taux-changement.csv")

    lignes = []
    for i, nom in enumerate(ADMISSIBLES):
        t = time.time()
        lig = ligne_configuration(paq, nom, avec_auc_ic=True)
        lignes.append(lig)
        print(f"  {nom:55s} exact.={lig['exactitude_jumeau']:.4f} "
              f"(persist.={lig['exactitude_persistance']:.4f}) "
              f"n={lig['n_cellules']}  {time.time() - t:.1f}s", flush=True)
    tab = pd.DataFrame(lignes)
    C.ecrire(lignes, "memoire-table-principale.csv")

    meilleur = tab.loc[tab.exactitude_jumeau.idxmax(), "configuration"]
    print(f"\nmeilleur jumeau (exactitude globale, sur son propre perimetre) : "
          f"{meilleur}", flush=True)
    lig_meilleur = ligne_configuration(paq, meilleur, avec_auc_ic=True)
    C.ecrire([lig_meilleur], "memoire-meilleur-jumeau.csv")

    comb = regle_combinee(paq)
    print(f"\nregle combinee P4 : persistance={comb['exactitude_persistance']:.4f} "
          f"combinee={comb['exactitude_combinee']:.4f} "
          f"gain={comb['gain_combinee_moins_persistance']:+.4f} "
          f"({comb['part_cellules_basculees']:.4f} des cellules basculees)", flush=True)
    C.ecrire([comb], "memoire-regle-combinee.csv")

    print(f"\ntermine en {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
