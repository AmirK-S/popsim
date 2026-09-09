"""
a8_minorites : qui retrouve les minorites d'opinion.

Repond a la fiche B4 du BRAINSTORM, "un institut achete des segments et des queues de
distribution, pas une moyenne". Le rapport a2 ne mesure que des exactitudes moyennes, ou
une methode qui repond toujours la modalite majoritaire parait honorable. Ici on regarde
les seules cellules ou la vraie reponse est une modalite minoritaire.

Trois quantites par methode et par seuil :
  - rappel : part des cellules a reponse minoritaire qui sont bien predites ;
  - precision : part des cellules ou la methode predit une modalite minoritaire et a raison ;
  - masse minoritaire predite au niveau population, a comparer a la masse humaine, qui est
    la part des cellules dont la vraie reponse est minoritaire.
Une methode peut atteindre une bonne exactitude moyenne avec un rappel minoritaire nul.
C'est le cas, par construction, de la modalite majoritaire.

Deux seuils : une modalite est minoritaire si moins de 10 pour cent, puis moins de 20 pour
cent, des repondants de l'item l'ont choisie. Le seuil est descriptif, il est calcule sur
la population observee et n'entre dans aucune prediction.

Entree  : data/osf-t6g7k-stanford, data/twin2k500.
Sortie  : resultats/a8-minorites-gss.csv, resultats/a8-minorites-twin.csv.

Aucun appel de modele. Duree : environ dix minutes.

Usage : .venv/bin/python analyses/a8_minorites.py
"""

import time

import numpy as np

import a8_commun as C
from a2_commun import (b0_marginale, b1_logistique, b2_voisins, distance_hamming, en_codes,
                       encodeur_demographies, est_manquant)

SEUILS = [0.10, 0.20]


def lignes_pour(nom, pred, verite, masque, seuils_mods, exactitude):
    out = []
    for seuil, mods in seuils_mods.items():
        r = C.mesures_minorites(pred, verite, mods, masque)
        out.append({"methode": nom, "seuil": seuil, "exactitude_globale": exactitude, **r})
    return out


def gss():
    g = C.charger_gss()
    y, x, items = g["y1"], g["x"], g["items"]
    n, m = y.shape
    plis, blocs = C.grille_gss(n, m)
    codes = en_codes(y)
    rng = np.random.default_rng(C.GRAINE)
    noms = ["B0 mode", "B0 tirage", "B1 argmax", "B1 tirage", "B2 argmax", "B2 tirage"]
    pred = {nom: np.empty((n, m), dtype=object) for nom in noms}
    for i_pli, (tr, te) in enumerate(plis):
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        for j in range(m):
            pred["B0 mode"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng, mode=True)[:, None]
            pred["B0 tirage"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng)[:, None]
            pred["B1 argmax"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
            pred["B1 tirage"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng, tirage=True)[:, None]
        for bloc in blocs:
            contexte = np.setdiff1d(np.arange(m), bloc)
            d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
            for j in bloc:
                pred["B2 argmax"][np.ix_(te, [j])] = b2_voisins(d, y[tr, j], C.K_A2, rng)[:, None]
                pred["B2 tirage"][np.ix_(te, [j])] = b2_voisins(d, y[tr, j], C.K_A2, rng, tirage=True)[:, None]
        print(f"  pli {i_pli + 1}/{len(plis)} termine", flush=True)

    pred.update(C.charger_agents_gss(items))
    pred["humains reinterroges"] = g["y2"]
    seuils_mods = {s: C.modalites_minoritaires(y, s) for s in SEUILS}
    cols = list(range(m))
    lignes = []
    for nom, p in pred.items():
        moy, _, _ = C.exactitude_sur(p, y, cols)
        lignes += lignes_pour(nom, p, y, None, seuils_mods, moy)
    return lignes


def twin():
    d0 = C.charger_twin()
    y, x, ctx = d0["y"], d0["x"], d0["ctx"]
    n, m = y.shape
    plis = C.plis_twin(n)
    masque = np.array([[not est_manquant(v) for v in l] for l in y])
    codes = en_codes(ctx)
    rng = np.random.default_rng(C.GRAINE)
    noms = ["B0 mode", "B0 tirage", "B1 argmax", "B1 tirage", "B2 argmax", "B2 tirage"]
    pred = {nom: np.empty((n, m), dtype=object) for nom in noms}
    for i_pli, (tr, te) in enumerate(plis):
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        dist = distance_hamming(codes[te], codes[tr])
        for j in range(m):
            pred["B0 mode"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng, mode=True)[:, None]
            pred["B0 tirage"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng)[:, None]
            pred["B1 argmax"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
            pred["B1 tirage"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng, tirage=True)[:, None]
            pred["B2 argmax"][np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], C.K_A2, rng)[:, None]
            pred["B2 tirage"][np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], C.K_A2, rng, tirage=True)[:, None]
        print(f"  pli {i_pli + 1}/{len(plis)} termine", flush=True)

    seuils_mods = {s: C.modalites_minoritaires(y, s) for s in SEUILS}
    cols = list(range(m))
    lignes = []
    for nom, p in pred.items():
        pm = np.where(masque, p, None)
        moy, _, _ = C.exactitude_sur(pm, y, cols, masque)
        lignes += lignes_pour(nom, pm, y, masque, seuils_mods, moy)

    # Les simulations sont dans le codage numerique du catalogue : la cible aussi.
    yn = C.cible_twin_numerique(d0)
    seuils_mods_n = {s: C.modalites_minoritaires(yn, s) for s in SEUILS}
    for libelle, spec in C.charger_llm_twin(d0).items():
        mq = masque & spec["personnes"][:, None]
        moy, _, _ = C.exactitude_sur(spec["matrice"], yn, cols, mq)
        lignes += lignes_pour(libelle, spec["matrice"], yn, mq, seuils_mods_n, moy)
    mq = masque
    moy, _, _ = C.exactitude_sur(np.where(mq, d0["y_retest"], None), y, cols, mq)
    lignes += lignes_pour("humains retest vagues 1 a 3",
                          np.where(mq, d0["y_retest"], None), y, mq, seuils_mods, moy)
    return lignes


def main():
    t0 = time.time()
    print("GSS")
    C.ecrire_csv(gss(), "a8-minorites-gss.csv")
    print("\nTwin-2K-500")
    C.ecrire_csv(twin(), "a8-minorites-twin.csv")
    print(f"duree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
