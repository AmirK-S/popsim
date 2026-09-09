"""
a25_mesures : ecart agent contre humain, item par item, sur les items du GSS que NORC
classe sensibles au mode de collecte et sur ses temoins negatifs.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a2_commun, a2_baselines_gss, a5_evaluer et
a25_commun sont importes tels quels.

Question posee. Si une population simulee est "presentable", c'est a dire si elle rend le
dicible et efface ce que les gens cachent, alors l'ecart entre agents et humains doit etre
plus grand sur les items ou les humains eux memes repondent differemment selon qu'ils sont
observes ou non, et le sens de l'ecart doit aller vers la modalite socialement desirable.
La liste des items sensibles n'est pas construite par nous : elle vient de NORC (2023),
*Mode Sensitivity in the 2022 GSS, Release 1*, recopiee dans a25_commun.

Trois mesures par couple (condition, item) :
  - exactitude au niveau de la cellule, sur les memes personnes et la meme verite que a2
    et a23 ;
  - ecart de distribution entre la population simulee et la population humaine de la
    vague 1 : distance de Wasserstein d'ordre 1 sur les rangs normalises pour les items
    ordinaux, distance de variation totale pour les items nominaux, les deux dans [0, 1]
    et egales entre elles quand l'item est binaire ;
  - sens de l'ecart : difference entre le score moyen de desirabilite de la population
    simulee et celui de la population humaine, sur les seules modalites auxquelles
    a25_commun attribue un score. Positif veut dire que la masse simulee s'est deplacee
    vers le pole socialement desirable.

Deux perimetres, parce que les conditions ne portent pas sur les memes gens :
  - "1052" : les six conditions d'agents de l'archive de Stanford, les baselines et les
    humains de la vague 2, sur les 1 052 participants ;
  - "150"  : les memes, restreintes aux personnes de notre run, plus C2 et C3.
Les comparaisons entre nos agents et les autres methodes se lisent sur le perimetre 150 et
sur lui seul.

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl, data/traces/a5-personnes.csv.
Sortie  : resultats/a25-croisement.csv, a25-par-item-condition.csv,
          a25-bootstrap-personnes.csv.

Usage :
  .venv/bin/python analyses/a25_mesures.py
  .venv/bin/python analyses/a25_mesures.py --cache /tmp/a25-matrices.pkl --bootstrap 1000
"""

import argparse
import json
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_commun import est_manquant
from a2_baselines_gss import CONDITIONS_LLM, GRAINE, PREP, charger, evaluer, grille
from a5_evaluer import lire_traces, moyenner_passes, en_matrices
from a5_agents_locaux_gss import TRACES, nomenclature
from a25_commun import (CORRESPONDANCE, LITTERATURE_SENSIBLE, ORDINAUX, classe_norc,
                        options_par_item, sans_score, scores_desirabilite)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

BASELINES = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax"]


def norm(v):
    return str(v).lower().strip()


# ---------------------------------------------------------------------------
# Mesures de distribution
# ---------------------------------------------------------------------------

def distance(p, q, ordinal):
    """Distance entre deux distributions sur les memes K modalites ordonnees.

    p et q sont des tableaux (..., K) de masses sommant a 1 sur le dernier axe.
    Ordinal : Wasserstein d'ordre 1 sur les rangs ramenes a [0, 1], soit la somme des
    ecarts de fonctions de repartition divisee par K - 1. Nominal : distance de variation
    totale. Les deux valent |p1 - q1| quand K = 2, ce qui rend les items binaires
    comparables quel que soit le traitement choisi.
    """
    k = p.shape[-1]
    if not ordinal or k < 2:
        return 0.5 * np.abs(p - q).sum(axis=-1)
    cp, cq = np.cumsum(p, axis=-1), np.cumsum(q, axis=-1)
    return np.abs(cp[..., :-1] - cq[..., :-1]).sum(axis=-1) / (k - 1)


def desirabilite_moyenne(p, scores_vec, defini):
    """Score moyen de desirabilite d'une distribution, et masse sans score.

    p : tableau (..., K). scores_vec : (K,) avec 0 la ou le score n'existe pas.
    defini : (K,) booleen. Le score moyen est renormalise sur les seules modalites qui en
    portent un, de sorte qu'une condition qui repond souvent "Inapplicable" ne soit pas
    comptee comme moins desirable pour cette seule raison.
    """
    masse = (p * defini).sum(axis=-1)
    with np.errstate(invalid="ignore", divide="ignore"):
        d = np.where(masse > 0, (p * scores_vec * defini).sum(axis=-1) / np.maximum(masse, 1e-12),
                     np.nan)
    return d, 1.0 - masse


# ---------------------------------------------------------------------------
# Construction des matrices de predictions
# ---------------------------------------------------------------------------

def matrices(args):
    """Renvoie ids, items, verite vague 1, et un dictionnaire condition -> matrice objet.

    Les matrices sont sur les 1 052 participants et les 149 items, sauf C2 et C3 qui ne
    couvrent que les 150 personnes du run : elles sont remplies de None ailleurs.
    """
    ids, items, y1, y2, x, _ = charger()
    index_personne = {p: i for i, p in enumerate(ids)}
    index_item = {c: j for j, c in enumerate(items)}

    M = {"humains vague 2": y2}

    for libelle, fichier in CONDITIONS_LLM.items():
        chemin = os.path.join(PREP, fichier)
        if not os.path.exists(chemin):
            continue
        d = pd.read_csv(chemin)
        assert list(d["email"]) == ids, f"{fichier} n'est pas aligne sur charger()"
        M[libelle] = d[items].values.astype(object)

    if args.cache and os.path.exists(args.cache):
        pred_b = pickle.load(open(args.cache, "rb"))
    else:
        plis, blocs = grille(len(ids), len(items), GRAINE)
        pred_b = evaluer(items, y1, x, plis, blocs)
        if args.cache:
            pickle.dump(pred_b, open(args.cache, "wb"))
    for nom in BASELINES:
        M[nom] = pred_b[nom]

    # C2 et C3 : traces du run a5, memes 150 personnes, memes 149 items.
    table = nomenclature()
    tables, _ = lire_traces("")
    ech = pd.read_csv(os.path.join(TRACES, "a5-personnes.csv"))
    vus = set()
    for t in tables.values():
        vus |= {k[0] for k in t}
    personnes150 = [p for p in ech["pid"] if p in vus]
    lignes150 = [index_personne[p] for p in personnes150]
    for condition in ["C2", "C3"]:
        fusion, _ = moyenner_passes(tables, condition)
        if not fusion:
            continue
        pred, _ = en_matrices(fusion, personnes150, items, table)
        plein = np.empty((len(ids), len(items)), dtype=object)
        plein[:] = None
        plein[np.ix_(lignes150, list(range(len(items))))] = pred
        M[condition] = plein

    return ids, items, y1, M, np.array(lignes150)


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--graine", type=int, default=20260908)
    args = ap.parse_args()

    ids, items, y1, M, lignes150 = matrices(args)
    options = options_par_item(RACINE)
    print(f"{len(ids)} personnes, {len(items)} items, {len(M)} conditions", flush=True)

    # ---------------------------------------------------------------- croisement
    lignes_croisement = []
    codage = {}
    for it in items:
        opts = [o for o in options[it]]
        classe, vars_gss = classe_norc(it)
        ordinal = it in ORDINAUX and not any(sans_score(o) for o in opts)
        scores, niveau, source = scores_desirabilite(it, opts)
        index = {o: k for k, o in enumerate(opts)}
        vec = np.zeros(len(opts))
        defini = np.zeros(len(opts))
        if scores:
            for o, v in scores.items():
                vec[index[o]] = v
                defini[index[o]] = 1.0
        codage[it] = (index, vec, defini, ordinal)
        lignes_croisement.append({
            "item": it,
            "variables_gss": " ".join(vars_gss) if vars_gss else "",
            "classe_norc": classe,
            "groupe_litterature": ("sensible litterature" if it in LITTERATURE_SENSIBLE
                                   else "temoin litterature"),
            "n_modalites": len(opts),
            "type": "ordinal" if ordinal else "nominal",
            "pole_desirable": " | ".join(o for o in opts if scores and scores.get(o) == 1.0)
                              if scores else "",
            "pole_defini": bool(scores),
            "niveau": niveau,
            "source_du_pole": source,
        })
    croisement = pd.DataFrame(lignes_croisement)
    os.makedirs(SORTIE, exist_ok=True)
    croisement.to_csv(os.path.join(SORTIE, "a25-croisement.csv"), index=False)
    print("\n--- croisement NORC x 149 items ---")
    print(croisement.groupby("classe_norc").agg(
        items=("item", "size"), poles_definis=("pole_defini", "sum")).to_string())

    # -------------------------------------------------- tenseurs indicatrices
    P, I = len(ids), len(items)
    Kmax = max(len(options[it]) for it in items)

    def onehot(mat, lignes):
        """Tableau (n, I, Kmax) des indicatrices de reponse, 0 partout si cellule vide."""
        t = np.zeros((len(lignes), I, Kmax), dtype=np.float32)
        for jj, it in enumerate(items):
            index = codage[it][0]
            col = mat[lignes, jj]
            for ii, v in enumerate(col):
                if v is None or est_manquant(v):
                    continue
                k = index.get(norm(v))
                if k is not None:
                    t[ii, jj, k] = 1.0
        return t

    def justes(mat, lignes):
        """Matrices (n, I) : cellule evaluable, et cellule correctement predite."""
        dispo = np.zeros((len(lignes), I), dtype=np.float32)
        bon = np.zeros((len(lignes), I), dtype=np.float32)
        for jj in range(I):
            col = mat[lignes, jj]
            vrai = y1[lignes, jj]
            for ii, (p, v) in enumerate(zip(col, vrai)):
                if p is None or est_manquant(p) or est_manquant(v):
                    continue
                dispo[ii, jj] = 1.0
                bon[ii, jj] = float(norm(p) == norm(v))
        return dispo, bon

    perimetres = {"1052": np.arange(P), "150": lignes150}
    rng = np.random.default_rng(args.graine)

    lignes_item, lignes_boot = [], []
    for nom_per, lignes in perimetres.items():
        n = len(lignes)
        oh_hum = onehot(y1, lignes)
        W = rng.multinomial(n, np.full(n, 1.0 / n), size=args.bootstrap).astype(np.float32)
        W /= n

        for cond, mat in M.items():
            if cond in ("C2", "C3") and nom_per != "150":
                continue
            oh = onehot(mat, lignes)
            dispo, bon = justes(mat, lignes)
            if dispo.sum() == 0:
                continue

            # ---- estimations ponctuelles, item par item
            for jj, it in enumerate(items):
                index, vec, defini, ordinal = codage[it]
                ns = int(dispo[:, jj].sum())
                if ns == 0:
                    continue
                k = len(options[it])
                ps = oh[:, jj, :k].sum(axis=0)
                ph = oh_hum[:, jj, :k].sum(axis=0)
                if ps.sum() == 0 or ph.sum() == 0:
                    continue
                ps, ph = ps / ps.sum(), ph / ph.sum()
                d = float(distance(ps[None, :], ph[None, :], ordinal)[0])
                ds, m_s = desirabilite_moyenne(ps[None, :], vec, defini)
                dh, m_h = desirabilite_moyenne(ph[None, :], vec, defini)
                classe, _ = classe_norc(it)
                lignes_item.append({
                    "perimetre": nom_per, "condition": cond, "item": it,
                    "classe_norc": classe, "type": "ordinal" if ordinal else "nominal",
                    "n_cellules": ns,
                    "exactitude": float(bon[:, jj].sum() / dispo[:, jj].sum()),
                    "distance": d,
                    "desirabilite_simulee": float(ds[0]),
                    "desirabilite_humaine": float(dh[0]),
                    "ecart_desirabilite": float(ds[0] - dh[0]) if defini.sum() else np.nan,
                    "masse_sans_score_simulee": float(m_s[0]),
                })

            # ---- bootstrap sur les personnes, par groupe d'items
            groupes = {}
            for g in ["sensible", "investiguer", "temoin"]:
                idx = [jj for jj, it in enumerate(items) if classe_norc(it)[0] == g]
                groupes[g] = idx
            groupes["sensible+investiguer"] = groupes["sensible"] + groupes["investiguer"]

            cs = np.einsum("bp,pik->bik", W, oh)
            ch = np.einsum("bp,pik->bik", W, oh_hum)
            d_boot = np.full((args.bootstrap, I), np.nan)
            ed_boot = np.full((args.bootstrap, I), np.nan)
            for jj, it in enumerate(items):
                _, vec, defini, ordinal = codage[it]
                k = len(options[it])
                a, b = cs[:, jj, :k], ch[:, jj, :k]
                sa, sb = a.sum(axis=1, keepdims=True), b.sum(axis=1, keepdims=True)
                ok = (sa[:, 0] > 0) & (sb[:, 0] > 0)
                if not ok.any():
                    continue
                pa = np.where(sa > 0, a / np.maximum(sa, 1e-12), 0.0)
                pb = np.where(sb > 0, b / np.maximum(sb, 1e-12), 0.0)
                d_boot[ok, jj] = distance(pa[ok], pb[ok], ordinal)
                if defini.sum():
                    da, _ = desirabilite_moyenne(pa[ok], vec[:k], defini[:k])
                    db, _ = desirabilite_moyenne(pb[ok], vec[:k], defini[:k])
                    ed_boot[ok, jj] = da - db
            acc_boot = (W @ bon) / np.maximum(W @ dispo, 1e-12)
            acc_boot = np.where((W @ dispo) > 0, acc_boot, np.nan)

            for g, idx in groupes.items():
                if not idx:
                    continue
                for nom_m, tab in [("exactitude", acc_boot), ("distance", d_boot),
                                   ("ecart_desirabilite", ed_boot)]:
                    v = np.nanmean(tab[:, idx], axis=1)
                    lignes_boot.append({
                        "perimetre": nom_per, "condition": cond, "groupe": g,
                        "metrique": nom_m, "moyenne": float(np.nanmean(v)),
                        "ic_bas": float(np.nanpercentile(v, 2.5)),
                        "ic_haut": float(np.nanpercentile(v, 97.5)),
                    })
            # contraste sensible moins temoin, par tirage de personnes
            for nom_m, tab in [("exactitude", acc_boot), ("distance", d_boot),
                               ("ecart_desirabilite", ed_boot)]:
                for g in ["sensible", "sensible+investiguer"]:
                    v = (np.nanmean(tab[:, groupes[g]], axis=1)
                         - np.nanmean(tab[:, groupes["temoin"]], axis=1))
                    lignes_boot.append({
                        "perimetre": nom_per, "condition": cond,
                        "groupe": f"{g} moins temoin", "metrique": nom_m,
                        "moyenne": float(np.nanmean(v)),
                        "ic_bas": float(np.nanpercentile(v, 2.5)),
                        "ic_haut": float(np.nanpercentile(v, 97.5)),
                    })
            print(f"  {nom_per:>5} {cond:<28} fait", flush=True)

    pd.DataFrame(lignes_item).to_csv(os.path.join(SORTIE, "a25-par-item-condition.csv"),
                                     index=False, float_format="%.6f")
    pd.DataFrame(lignes_boot).to_csv(os.path.join(SORTIE, "a25-bootstrap-personnes.csv"),
                                     index=False, float_format="%.6f")
    print(f"\necrit dans {SORTIE} : a25-croisement.csv, a25-par-item-condition.csv, "
          "a25-bootstrap-personnes.csv")


if __name__ == "__main__":
    main()
