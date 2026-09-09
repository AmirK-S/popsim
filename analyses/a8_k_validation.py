"""
a8_k_validation : le k de B2 choisi par validation interne au pli d'entrainement.

Repond a la limite 1 du rapport a2 : "le k de B2 a ete choisi sur un pli de test", ce qui
est un choix d'hyperparametre regarde sur la reponse. Ici, k est choisi a l'interieur du
seul pli d'entrainement, par validation croisee interne, puis applique au pli de test sans
retouche. L'ecart avec le k = 30 de a2 chiffre l'optimisme induit.

Protocole, identique a a2 par ailleurs : graine 20260903, 5 plis de personnes, 5 blocs
d'items sur le GSS, decoupage temporel fourni sur Twin-2K-500.

Entree  : data/osf-t6g7k-stanford, data/twin2k500.
Sortie  : resultats/a8-k-validation.csv, tableau agrege.

Aucun appel de modele. Duree : environ dix minutes.

Usage : .venv/bin/python analyses/a8_k_validation.py
"""

import time

import numpy as np
from sklearn.model_selection import KFold

import a8_commun as C
from a2_commun import (b2_voisins, bootstrap_personnes, distance_hamming, en_codes,
                       est_manquant, exactitude_par_personne)

GRILLE_K = [1, 3, 5, 10, 15, 20, 25, 30, 40, 60, 100, 150]
N_PLIS_INTERNES = 3


def balayage_k(distances, y_train, y_test, grille=GRILLE_K):
    """Exactitude du vote majoritaire des k voisins, pour tous les k de la grille.

    Le classement des voisins est calcule une fois, puis les votes sont accumules par
    ajout du voisin suivant. C'est algebriquement le meme predicteur que b2_voisins, a
    la regle de departage pres : ici un ex aequo est tranche par l'ordre d'apparition de
    la modalite dans le pli d'entrainement, la ou b2_voisins suit l'ordre du compteur.
    Cette fonction ne sert qu'a choisir k ; le score final est toujours recalcule avec
    b2_voisins, pour qu'aucun chiffre publie ne depende de ce detail.
    """
    obs = np.array([not est_manquant(v) for v in y_train])
    if obs.sum() < 2:
        return {k: float("nan") for k in grille}, 0
    y = np.asarray(y_train, dtype=object)[obs]
    classes = list(dict.fromkeys(y))
    rang = {c: i for i, c in enumerate(classes)}
    codes_y = np.array([rang[v] for v in y], dtype=np.int32)
    d = distances[:, obs]
    kmax = min(max(grille), d.shape[1])
    part = np.argpartition(d, kmax - 1, axis=1)[:, :kmax]
    ordre = np.take_along_axis(part, np.argsort(np.take_along_axis(d, part, 1), axis=1), 1)
    voisins = codes_y[ordre]                       # (n_test, kmax)

    masque_test = np.array([not est_manquant(v) for v in y_test])
    verite = np.array([rang.get(v, -1) for v in y_test], dtype=np.int32)
    n_test = d.shape[0]
    comptes = np.zeros((n_test, len(classes)), dtype=np.int32)
    lignes = np.arange(n_test)
    scores, evaluables = {}, int(masque_test.sum())
    for kk in range(1, kmax + 1):
        np.add.at(comptes, (lignes, voisins[:, kk - 1]), 1)
        if kk in grille:
            pred = comptes.argmax(axis=1)
            scores[kk] = float(((pred == verite) & masque_test).sum())
    for k in grille:
        scores.setdefault(k, float("nan"))
    return scores, evaluables


# ---------------------------------------------------------------------------
# GSS
# ---------------------------------------------------------------------------

def gss():
    g = C.charger_gss()
    y, items = g["y1"], g["items"]
    n, m = y.shape
    plis, blocs = C.grille_gss(n, m)
    codes = en_codes(y)
    rng = np.random.default_rng(C.GRAINE)
    lignes, pred_interne = [], np.empty((n, m), dtype=object)
    pred_a2 = np.empty((n, m), dtype=object)

    for i_pli, (tr, te) in enumerate(plis):
        # Validation interne : le pli de test n'est jamais regarde pour choisir k.
        kf = KFold(n_splits=N_PLIS_INTERNES, shuffle=True, random_state=C.GRAINE + i_pli)
        cumul = {k: [0.0, 0] for k in GRILLE_K}
        for itr, ival in kf.split(tr):
            a, b = tr[itr], tr[ival]
            for bloc in blocs:
                contexte = np.setdiff1d(np.arange(m), bloc)
                d = distance_hamming(codes[np.ix_(b, contexte)], codes[np.ix_(a, contexte)])
                for j in bloc:
                    s, nev = balayage_k(d, y[a, j], y[b, j])
                    for k in GRILLE_K:
                        cumul[k][0] += s[k]
                        cumul[k][1] += nev
        moyennes = {k: cumul[k][0] / cumul[k][1] for k in GRILLE_K}
        k_choisi = max(GRILLE_K, key=lambda k: moyennes[k])
        print(f"  pli {i_pli + 1} : k interne = {k_choisi} "
              f"(interne {moyennes[k_choisi]:.4f}, k=30 interne {moyennes[30]:.4f})", flush=True)
        lignes.append({
            "jeu": "GSS", "pli": i_pli + 1, "k_choisi_interne": k_choisi,
            "exactitude_interne_k_choisi": moyennes[k_choisi],
            "exactitude_interne_k30": moyennes[30],
            **{f"interne_k{k}": moyennes[k] for k in GRILLE_K},
        })
        # Application au pli de test, avec le predicteur de a2 sans modification.
        for bloc in blocs:
            contexte = np.setdiff1d(np.arange(m), bloc)
            d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
            for j in bloc:
                pred_interne[np.ix_(te, [j])] = b2_voisins(d, y[tr, j], k_choisi, rng)[:, None]
                pred_a2[np.ix_(te, [j])] = b2_voisins(d, y[tr, j], C.K_A2, rng)[:, None]
    return lignes, pred_interne, pred_a2, y, None


# ---------------------------------------------------------------------------
# Twin-2K-500
# ---------------------------------------------------------------------------

def twin():
    d0 = C.charger_twin()
    y, ctx = d0["y"], d0["ctx"]
    n, m = y.shape
    plis = C.plis_twin(n)
    codes = en_codes(ctx)
    masque = np.array([[not est_manquant(v) for v in l] for l in y])
    rng = np.random.default_rng(C.GRAINE)
    lignes = []
    pred_interne = np.empty((n, m), dtype=object)
    pred_a2 = np.empty((n, m), dtype=object)

    for i_pli, (tr, te) in enumerate(plis):
        kf = KFold(n_splits=N_PLIS_INTERNES, shuffle=True, random_state=C.GRAINE + i_pli)
        cumul = {k: [0.0, 0] for k in GRILLE_K}
        for itr, ival in kf.split(tr):
            a, b = tr[itr], tr[ival]
            dist = distance_hamming(codes[b], codes[a])
            for j in range(m):
                s, nev = balayage_k(dist, y[a, j], y[b, j])
                for k in GRILLE_K:
                    if not np.isnan(s[k]):
                        cumul[k][0] += s[k]
                        cumul[k][1] += nev
        moyennes = {k: cumul[k][0] / cumul[k][1] for k in GRILLE_K}
        k_choisi = max(GRILLE_K, key=lambda k: moyennes[k])
        print(f"  pli {i_pli + 1} : k interne = {k_choisi} "
              f"(interne {moyennes[k_choisi]:.4f}, k=30 interne {moyennes[30]:.4f})", flush=True)
        lignes.append({
            "jeu": "Twin", "pli": i_pli + 1, "k_choisi_interne": k_choisi,
            "exactitude_interne_k_choisi": moyennes[k_choisi],
            "exactitude_interne_k30": moyennes[30],
            **{f"interne_k{k}": moyennes[k] for k in GRILLE_K},
        })
        dist = distance_hamming(codes[te], codes[tr])
        for j in range(m):
            pred_interne[np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], k_choisi, rng)[:, None]
            pred_a2[np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], C.K_A2, rng)[:, None]
    return lignes, pred_interne, pred_a2, y, masque


def resume(nom, pred, y, masque):
    p = pred if masque is None else np.where(masque, pred, None)
    acc = exactitude_par_personne(p, y, masque)
    moy, bas, haut = bootstrap_personnes(acc, graine=C.GRAINE)
    return {"variante": nom, "exactitude": moy, "ic_bas": bas, "ic_haut": haut}


def main():
    t0 = time.time()
    tout, resumes = [], []

    print("GSS : choix de k par validation interne")
    lg, pi, pa, y, mq = gss()
    tout += lg
    r_i = resume("B2 k interne", pi, y, mq)
    r_a = resume("B2 k = 30 (a2)", pa, y, mq)
    resumes += [{"jeu": "GSS", **r_i}, {"jeu": "GSS", **r_a}]
    print(f"  GSS  k interne {r_i['exactitude']:.4f}  contre k=30 {r_a['exactitude']:.4f}  "
          f"ecart {(r_i['exactitude'] - r_a['exactitude']) * 100:+.2f} point\n")

    print("Twin-2K-500 : choix de k par validation interne")
    lt, pi, pa, y, mq = twin()
    tout += lt
    r_i = resume("B2 k interne", pi, y, mq)
    r_a = resume("B2 k = 30 (a2)", pa, y, mq)
    resumes += [{"jeu": "Twin", **r_i}, {"jeu": "Twin", **r_a}]
    print(f"  Twin k interne {r_i['exactitude']:.4f}  contre k=30 {r_a['exactitude']:.4f}  "
          f"ecart {(r_i['exactitude'] - r_a['exactitude']) * 100:+.2f} point\n")

    C.ecrire_csv(tout, "a8-k-validation-plis.csv")
    C.ecrire_csv(resumes, "a8-k-validation.csv")
    print(f"duree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
