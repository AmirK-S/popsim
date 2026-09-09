"""
t1_baselines : les cinq predicteurs sans modele de langage sur Twin-2K-500.

Preenregistrement : resultats/t1-preenregistrement.md, section 3 et section 10 point 3.

B0 mode    la modalite majoritaire de l'item, aveugle a la personne
B0 tirage  un tirage dans la marginale de l'item, aveugle a la personne
B1 argmax  regression logistique multinomiale sur les seules 14 demographies
B2 argmax  les k = 30 plus proches voisins sur les 494 items de contexte des vagues 1 a 3
PMM k=10   appariement sur distribution predite, un donneur tire parmi les dix plus proches

Les quatre premiers emploient a2_commun sans une ligne modifiee, et le decoupage en cinq
plis de personnes de a2_baselines_twin. PMM est une TRANSPOSITION, declaree au
preenregistrement : la recette de tirage chez un donneur vient de
a35_commun.imputations_regression, mais Twin n'a pas de blocs a retirer, le contexte
etant temporellement disjoint de la cible.

Sortie : un cache /tmp/t1-baselines.pkl, matrices de codes entiers dans la nomenclature
commune de t1. Aucun appel de modele de langage.

Usage : .venv/bin/python analyses/t1_baselines.py
"""

import argparse
import os
import pickle
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as C                                     # noqa: E402
import numpy as np                                        # noqa: E402
from sklearn.linear_model import LogisticRegression       # noqa: E402
from sklearn.model_selection import KFold                 # noqa: E402
from sklearn.preprocessing import OneHotEncoder           # noqa: E402
from a2_commun import (b2_voisins, distance_hamming, en_codes,   # noqa: E402
                       encodeur_demographies, est_manquant)

N_PLIS = 5
K_VOISINS = 30
K_PMM = 10
FORCE = 1.0          # le C de scikit-learn, valeur de a2_commun.b1_logistique


def plis(n, graine=C.GRAINE):
    kf = KFold(n_splits=N_PLIS, shuffle=True, random_state=graine)
    return [(tr, te) for tr, te in kf.split(np.arange(n))]


def _codes_objets(y):
    """Les codes entiers de la nomenclature commune vus comme etiquettes categorielles.

    -1 devient None : a2_commun.est_manquant reconnait None et le predicteur ne s'entraine
    donc jamais sur une cellule vide, exactement comme sur les chaines.
    """
    out = np.empty(y.shape, dtype=object)
    out[:] = None
    plein = y >= 0
    out[plein] = y[plein].astype(int)
    return out


def _vers_codes(pred, forme):
    """Retour au format code entier, -1 pour une prediction absente."""
    out = np.full(forme, -1, dtype=np.int16)
    for i in range(forme[0]):
        for j in range(forme[1]):
            v = pred[i, j]
            if v is not None and not (isinstance(v, float) and np.isnan(v)):
                out[i, j] = int(v)
    return out


def calculer(paq, avec_pmm=True):
    y = paq["codes"][C.REF]
    yo = _codes_objets(y)
    x = paq["demo"]["x"]
    ctx = paq["demo"]["ctx"]
    n, m = y.shape
    rng = np.random.default_rng(C.GRAINE)
    noms = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax"] + \
           (["PMM k=10"] if avec_pmm else [])
    pred = {nom: np.empty((n, m), dtype=object) for nom in noms}
    codes_ctx = en_codes(ctx)
    dec = plis(n)
    Z = np.concatenate([_texte(ctx), x.astype(object)], axis=1) if avec_pmm else None

    for i_pli, (tr, te) in enumerate(dec):
        t0 = time.time()
        enc = encodeur_demographies(x[tr])
        Xt, Xe = enc.transform(x[tr]), enc.transform(x[te])
        d = distance_hamming(codes_ctx[te], codes_ctx[tr])

        if avec_pmm:
            enc2 = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
            enc2.fit(Z[tr])
            Zt, Ze = enc2.transform(Z[tr]), enc2.transform(Z[te])

        for j in range(m):
            col = yo[tr, j]
            obs = np.array([not est_manquant(v) for v in col])
            vus = [v for v in col if not est_manquant(v)]
            if not vus:
                continue
            cpt = Counter(vus)
            pred["B0 mode"][te, j] = cpt.most_common(1)[0][0]
            mods, eff = zip(*cpt.items())
            p = np.array(eff, dtype=float) / sum(eff)
            pred["B0 tirage"][te, j] = rng.choice(mods, size=len(te), p=p)

            classes = list(dict.fromkeys(vus))
            if len(classes) == 1:
                for nom in noms[2:]:
                    pred[nom][te, j] = classes[0]
                continue
            rang = {c: i for i, c in enumerate(classes)}
            mod = LogisticRegression(max_iter=2000, C=FORCE)
            mod.fit(Xt[obs], np.array([rang[v] for v in np.asarray(col)[obs]]))
            pred["B1 argmax"][te, j] = [classes[i] for i in mod.predict(Xe)]

            pred["B2 argmax"][te, j] = b2_voisins(d, col, K_VOISINS, rng)

            if avec_pmm:
                mod2 = LogisticRegression(max_iter=1000, C=FORCE)
                mod2.fit(Zt[obs], np.array([rang[v] for v in np.asarray(col)[obs]]))
                ordre = np.argsort(mod2.classes_)
                p_te = mod2.predict_proba(Ze)[:, ordre]
                p_tr = mod2.predict_proba(Zt[obs])[:, ordre]
                donneurs = np.asarray(col, dtype=object)[obs]
                d2 = ((p_te[:, None, :] - p_tr[None, :, :]) ** 2).sum(axis=2)
                keff = min(K_PMM, d2.shape[1])
                prox = np.argpartition(d2, keff - 1, axis=1)[:, :keff]
                choix = rng.integers(0, keff, size=len(te))
                pred["PMM k=10"][te, j] = donneurs[prox[np.arange(len(te)), choix]]
        print(f"  pli {i_pli + 1}/{N_PLIS}, {time.time() - t0:.0f}s", flush=True)

    return {nom: _vers_codes(pred[nom], (n, m)) for nom in noms}


def _texte(mat):
    """Une matrice objet en chaines, None devenant une modalite explicite. Convention de
    a35_commun.texte, recopiee ici en trois lignes parce qu'elle y est triviale et que
    a35_commun n'est pas importable sans le cache du GSS."""
    out = np.empty(mat.shape, dtype=object)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            out[i, j] = "manquant" if est_manquant(v) else str(v)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/t1-baselines.pkl")
    ap.add_argument("--sans-pmm", action="store_true")
    args = ap.parse_args()
    t0 = time.time()
    paq = C.charger()
    out = calculer(paq, avec_pmm=not args.sans_pmm)
    pickle.dump(out, open(args.cache, "wb"))
    print(f"ecrit {args.cache}, {list(out)}, {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
