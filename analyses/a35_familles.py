"""
a35_familles : le regime severe applique aux methodes d'imputation nouvelles.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a2_baselines_gss, a8_commun, a8_familles,
a28_commun et a35_commun sont importes tels quels.

Pourquoi ce script existe. Le tableau principal de a35 donne au modele d'imputation par
regression les 119 autres items du questionnaire comme contexte, decoupes au hasard. a2
signalait deja la faille en limite 7 et a8 l'a chiffree pour B2 : quand le bloc secret est
tire au hasard, un item d'avortement garde ses six cousins dans le contexte, et la methode
gagne 3,4 points qu'elle ne gagnerait pas sur une question reellement nouvelle. a8 a montre
que dans le regime severe, ou la famille thematique entiere sort du contexte ET sert de
cible, l'agent composite de Stanford repasse DEVANT B2 et le domine sur les deux axes a la
fois. Si l'imputation par regression a le meme comportement, la conclusion principale de
a35, "une regression sur contexte bat les six conditions de Stanford", ne vaut que dans le
regime facile, et il faut le dire.

Le protocole est celui de a8_familles, repris sans retouche : six familles thematiques de
a2_baselines_gss, 58 items, la famille entiere retiree du contexte et predite, memes cinq
plis sur les personnes, memes graines. Seules les methodes changent.

Ce test n'appartient a aucune famille d'hypotheses de a35_imputation : c'est une
verification de robustesse de la lecture, declaree comme telle, et elle est rapportee avec
son signe quel qu'il soit.

Entree  : paquet OSF t6g7k, cache de matrices de a25, cache de la foret de a28.
Sortie  : resultats/a35-familles-regime-severe.csv.

Usage :
  .venv/bin/python analyses/a35_familles.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl
"""

import argparse
import os
import sys
import time

import numpy as np
import pandas as pd
from sklearn.preprocessing import OneHotEncoder

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
import a35_commun as C
import a2_baselines_gss as G
from a2_baselines_gss import GRAINE, grille

M_IM = 10
K_PMM = 10


def imputer_par_famille(y1, x, plis, familles, force, graine=C.GRAINE_A35):
    """E1, E2, PMM et IM sous le regime severe : la famille entiere hors du contexte."""
    n, m = y1.shape
    rng = np.random.default_rng(graine)
    noms = ["E1 famille retiree (argmax)", "E2 famille retiree (tirage)",
            f"PMM k={K_PMM} famille retiree", f"IM m={M_IM} mode, famille retiree"]
    out = {nom: np.full((n, m), None, dtype=object) for nom in noms}
    for i_pli, (tr, te) in enumerate(plis):
        for nom_fam, cols in familles.items():
            ctx = np.setdiff1d(np.arange(m), cols)
            Z = np.concatenate([C.texte(y1[:, ctx]), x.astype(object)], axis=1)
            enc = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
            enc.fit(Z[tr])
            Xt, Xe = enc.transform(Z[tr]), enc.transform(Z[te])
            for j in cols:
                classes, p_te, p_tr, obs = C._fit_item(Xt, Xe, y1[tr, j], force)
                if classes is None:
                    continue
                if p_te is None:
                    seul = np.array([classes[0]] * len(te), dtype=object)
                    for nom in noms:
                        out[nom][np.ix_(te, [j])] = seul[:, None]
                    continue
                cl = np.asarray(classes, dtype=object)
                out["E1 famille retiree (argmax)"][np.ix_(te, [j])] = \
                    cl[p_te.argmax(axis=1)][:, None]
                tir = np.empty((M_IM, len(te)), dtype=object)
                for t in range(M_IM):
                    idx = np.array([rng.choice(len(cl), p=p) for p in p_te])
                    tir[t] = cl[idx]
                out["E2 famille retiree (tirage)"][np.ix_(te, [j])] = tir[0][:, None]
                mode = np.empty(len(te), dtype=object)
                for i in range(len(te)):
                    vals, cpt = np.unique(tir[:, i].astype(str), return_counts=True)
                    mode[i] = vals[cpt.argmax()]
                out[f"IM m={M_IM} mode, famille retiree"][np.ix_(te, [j])] = mode[:, None]
                donneurs = np.asarray(y1[tr, j], dtype=object)[obs]
                d2 = ((p_te[:, None, :] - p_tr[None, :, :]) ** 2).sum(axis=2)
                keff = min(K_PMM, d2.shape[1])
                prox = np.argpartition(d2, keff - 1, axis=1)[:, :keff]
                choix = rng.integers(0, keff, size=len(te))
                out[f"PMM k={K_PMM} famille retiree"][np.ix_(te, [j])] = \
                    donneurs[prox[np.arange(len(te)), choix]][:, None]
        print(f"  pli {i_pli + 1}/{len(plis)} termine", flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--force", type=float, default=0.03,
                    help="penalite retenue par a35_imputation, voir a35-choix-penalite.csv")
    args = ap.parse_args()

    t0 = time.time()
    paquet = C.charger_paquet(args.cache, args.cache_foret)
    if args.cache_a35 and os.path.exists(args.cache_a35):
        import pickle
        brut = pickle.load(open(args.cache_a35, "rb"))
        for nom, mat in brut.items():
            if not nom.startswith("_"):
                paquet["M"][nom] = mat
    y1, x, items, options = paquet["y1"], paquet["x"], paquet["items"], paquet["options"]
    n, m = y1.shape
    plis, _ = grille(n, m, GRAINE)
    index = {it: j for j, it in enumerate(items)}
    familles = {nom: [index[i] for i in membres if i in index]
                for nom, membres in G.FAMILLES.items()}
    tous = sorted({j for cols in familles.values() for j in cols})
    print(f"{len(familles)} familles, {len(tous)} items, penalite C = {args.force}")

    neuf = imputer_par_famille(y1, x, plis, familles, args.force)
    for nom, mat in neuf.items():
        paquet["M"][nom] = mat

    seg = C28.segments(paquet["x"], paquet["attributs"])[0][C.AXE_PRINCIPAL]
    k_items = [len(options[it]) for it in items]
    codes_h = C28.coder(y1, np.arange(n), items, options)
    ref = C.sommes_dispersion(codes_h, seg, k_items, tous)
    lignes_pers = np.arange(n)

    a_lire = list(neuf) + ["agents composite", "agents entretien (v3)", "agents enquete",
                           "agents demographiques (v6)", "agents v7", "agents v8",
                           "E1 regression contexte argmax", "E2 regression contexte tirage",
                           "PMM k=10", "IM m=10 mode des m", "B2 argmax", "B2 tirage",
                           "B1 argmax", "B0 mode", "humains vague 2"]
    acc_h = C.exactitude(paquet["M"]["humains vague 2"], y1, lignes_pers, tous)
    plafond = float(np.nanmean(acc_h))

    out = []
    for nom in a_lire:
        pred = paquet["M"][nom]
        acc = C.exactitude(pred, y1, lignes_pers, tous)
        div = C.diversite(pred, y1, lignes_pers, tous)
        codes = C28.coder(pred, lignes_pers, items, options)
        s = C.sommes_dispersion(codes, seg, k_items, tous)
        out.append({
            "methode": nom, "n_items": len(tous),
            "exactitude": float(np.nanmean(acc)),
            "exactitude_normalisee": float(np.nanmean(acc)) / plafond,
            "part_diversite_humaine": div["part_diversite_humaine"],
            "accord_par_paires": div["accord_par_paires"],
            "ratio_intra_ideologie": s["intra"] / ref["intra"] if ref["intra"] else np.nan,
            "ratio_inter_ideologie": s["inter"] / ref["inter"] if ref["inter"] else np.nan})
    d = pd.DataFrame(out).sort_values("exactitude", ascending=False)
    C.ecrire(d, "a35-familles-regime-severe.csv")
    print(d.to_string(index=False))
    print(f"duree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
