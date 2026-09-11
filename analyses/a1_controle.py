"""
a1_controle : la vague 4 est un retest a deux semaines et Demographics Only atteint deja
une AUC de 0,607 (memoire-resultats.md, idees-A-atouts-2026-09-11.md idee 1). Ce controle
demande si l'AUC 0,65 de P3 (desaccord jumeau/passe -> changement) survit aux effets fixes
d'item et a la propension individuelle au changement, ou si ce n'est que de la volatilite
deja connue.

PREENREGISTREMENT : resultats/a1-controle-preenregistrement.md, ecrit le 11 septembre 2026,
AVANT ce script et avant tout calcul.

CE QUI EST IMPORTE TEL QUEL : t1_commun.charger, memoire_twin.cellules, memoire_twin.ADMISSIBLES.
Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.

Usage : .venv/bin/python analyses/a1_controle.py
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np                                     # noqa: E402
import pandas as pd                                     # noqa: E402
from scipy.sparse import csr_matrix, hstack             # noqa: E402
from sklearn.linear_model import LogisticRegression      # noqa: E402
from sklearn.metrics import roc_auc_score                # noqa: E402
from sklearn.preprocessing import OneHotEncoder          # noqa: E402

import t1_commun as C                                    # noqa: E402
import memoire_twin as MT                                # noqa: E402

REF = C.REF
PLANCHER = C.PLANCHER
GRAINE = 20260909
N_PLIS = 5
N_BOOT = 1000


# ---------------------------------------------------------------------------
# 1. Propension personne (leave-one-item-out) et plis par personne
# ---------------------------------------------------------------------------

def propension_hors_item(ii, changee):
    """Propension individuelle au changement par personne, item courant exclu (leave-
    one-item-out) : moyenne des AUTRES cellules de cette personne. Repli sur le taux
    global si la personne n'a qu'une cellule dans ce perimetre. Pas un effet fixe personne
    (qui ne se generalise pas a une personne inedite sous validation croisee par personne)."""
    df = pd.DataFrame({"i": ii, "y": changee})
    somme = df.groupby("i")["y"].transform("sum").to_numpy()
    effectif = df.groupby("i")["y"].transform("count").to_numpy()
    global_taux = float(changee.mean())
    return np.where(effectif > 1, (somme - changee) / np.maximum(effectif - 1, 1),
                     global_taux)


def plis_par_personne(ii, n_plis=N_PLIS, graine=GRAINE):
    """Assigne chaque personne (jamais coupee entre plis) a l'un des n_plis plis."""
    personnes = np.unique(ii)
    rng = np.random.default_rng(graine)
    ordre = rng.permutation(personnes)
    pli_personne = {p: k % n_plis for k, p in enumerate(ordre)}
    return np.array([pli_personne[p] for p in ii])


# ---------------------------------------------------------------------------
# 2. Predictions hors pli : reference (item + propension) vs reference + desaccord
# ---------------------------------------------------------------------------

def predictions_oof(ii, jj, changee, desaccord, prop):
    pli = plis_par_personne(ii)
    pred_ref = np.full(len(ii), np.nan)
    pred_test = np.full(len(ii), np.nan)
    for k in range(N_PLIS):
        tr, te = pli != k, pli == k
        ohe = OneHotEncoder(handle_unknown="ignore")
        Xj_tr = ohe.fit_transform(jj[tr, None])
        Xj_te = ohe.transform(jj[te, None])
        X_ref_tr = hstack([Xj_tr, csr_matrix(prop[tr, None])]).tocsr()
        X_ref_te = hstack([Xj_te, csr_matrix(prop[te, None])]).tocsr()
        X_test_tr = hstack([X_ref_tr, csr_matrix(desaccord[tr, None])]).tocsr()
        X_test_te = hstack([X_ref_te, csr_matrix(desaccord[te, None])]).tocsr()
        m_ref = LogisticRegression(max_iter=2000).fit(X_ref_tr, changee[tr])
        m_test = LogisticRegression(max_iter=2000).fit(X_test_tr, changee[tr])
        pred_ref[te] = m_ref.predict_proba(X_ref_te)[:, 1]
        pred_test[te] = m_test.predict_proba(X_test_te)[:, 1]
    return pred_ref, pred_test


# ---------------------------------------------------------------------------
# 3. Bootstrap apparie du gain d'AUC (meme schema que memoire_twin.bootstrap_auc)
# ---------------------------------------------------------------------------

def bootstrap_gain(ii, jj, y, score_ref, score_test, b=N_BOOT, graine=GRAINE):
    """Tirage avec remise independant sur personnes et items (meme schema que
    memoire_twin.bootstrap_auc), applique en PAIRE (memes poids pour les deux modeles a
    chaque replicat) pour obtenir l'IC du gain d'AUC."""
    pers_u, ci = np.unique(ii, return_inverse=True)
    it_u, cj = np.unique(jj, return_inverse=True)
    n_p, n_j = len(pers_u), len(it_u)
    point_ref = roc_auc_score(y, score_ref)
    point_test = roc_auc_score(y, score_test)
    rng = np.random.default_rng(graine)
    reps = np.empty(b)
    for r in range(b):
        cp = np.bincount(rng.integers(0, n_p, size=n_p), minlength=n_p)
        cq = np.bincount(rng.integers(0, n_j, size=n_j), minlength=n_j)
        w = cp[ci] * cq[cj]
        try:
            a_ref = roc_auc_score(y, score_ref, sample_weight=w)
            a_test = roc_auc_score(y, score_test, sample_weight=w)
            reps[r] = a_test - a_ref
        except ValueError:
            reps[r] = np.nan
    bas, haut = np.nanpercentile(reps, [2.5, 97.5])
    return point_test - point_ref, float(bas), float(haut), point_ref, point_test


# ---------------------------------------------------------------------------
# 4. Par configuration
# ---------------------------------------------------------------------------

def ligne_configuration(paq, nom):
    ii, jj = MT.cellules(paq, nom)
    ref = paq["codes"][REF][ii, jj]
    pla = paq["codes"][PLANCHER][ii, jj]
    jum = paq["codes"][nom][ii, jj]
    changee = (pla != ref).astype(int)
    desaccord = (jum != pla).astype(int)
    prop = propension_hors_item(ii, changee)
    pred_ref, pred_test = predictions_oof(ii, jj, changee, desaccord, prop)
    gain, bas, haut, auc_ref, auc_test = bootstrap_gain(
        ii, jj, changee, pred_ref, pred_test)
    return {
        "configuration": nom, "n_personnes": int(len(np.unique(ii))),
        "n_cellules": int(len(ii)), "taux_changement": float(changee.mean()),
        "auc_reference": auc_ref, "auc_reference_plus_desaccord": auc_test,
        "gain_auc": gain, "gain_auc_ic_bas": bas, "gain_auc_ic_haut": haut,
    }


def main():
    t0 = time.time()
    paq = C.charger()
    lignes = []
    for nom in MT.ADMISSIBLES:
        t = time.time()
        lig = ligne_configuration(paq, nom)
        lignes.append(lig)
        print(f"  {nom:55s} ref={lig['auc_reference']:.4f} "
              f"ref+desaccord={lig['auc_reference_plus_desaccord']:.4f} "
              f"gain={lig['gain_auc']:+.4f} [{lig['gain_auc_ic_bas']:+.4f}, "
              f"{lig['gain_auc_ic_haut']:+.4f}]  {time.time() - t:.1f}s", flush=True)
    C.ecrire(lignes, "a1-controle-resultats.csv")
    print(f"\ntermine en {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
