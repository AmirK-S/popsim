"""
a47_verifications : les points de a45 qui demandent un calcul et non une relecture.

===========================================================================
CHANTIER a47, 9 septembre 2026. Trois verifications, aucune reecriture de script existant,
aucun appel de modele de langage, lecture seule sur data/.

1. OBJECTION 3, le facteur d'amplification de a38 est une quantite de gabarit. Le score de
   desirabilite d'une condition dans un camp est construit par `a28_test1_mode.mesurer`
   a partir de `compte(mat, j, it)`, qui denombre les modalites sur les lignes du camp.
   C'est donc une fonctionnelle de la seule table (camp, modalite). On le verifie
   numeriquement : le facteur est recalcule apres permutation des personnes a l'interieur
   de leur camp, et compare au facteur de la vraie assignation.

2. OBJECTION 7, la taille du contexte du regime severe de a35. Les six familles de
   `a2_baselines_gss.FAMILLES` sont intersectees avec les items reellement presents, et
   la taille du contexte severe, 149 moins la famille, est comparee aux 119 items du
   regime facile (149 moins un bloc de 30).

3. OBJECTION 2.3, `B2 argmax` ne recoit aucune demographie. Verifie par lecture de
   `a2_baselines_gss.baselines`, ou `B2` n'emploie que `codes[:, contexte]`, et par la
   presence de `enc.transform` dans le seul chemin de `B1`.

SORTIES, dans resultats/
------------------------
  a47-a38-invariance-facteur.csv     le facteur avant et apres permutation intra camp
  a47-contexte-regimes.csv           la taille du contexte des deux regimes de a35

Usage : .venv/bin/python analyses/a47_verifications.py
===========================================================================
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import a28_commun as C28
import a38_commun as A38
import a2_baselines_gss as B
from a28_test1_mode import mesurer
from a30_commun import camps_gss
from a38_mesures import desirabilite_humaine


def facteur_par_condition(paquet, lignes, conds, camps, items_camp):
    """Le facteur d'amplification de a38 pour chaque condition, sur un perimetre donne.

    Reprend exactement la chaine de `a38_tests` : mesure par camp avec `mesurer`, ecart
    humain gauche moins droite lu sur `desirabilite_humaine`, et
    facteur = 1 - moyenne(ecart_droite - ecart_gauche) / ecart_humain.
    """
    par_camp = []
    for camp in A38.CAMPS:
        sel = np.array([i for i in lignes if camps[i] == camp], dtype=int)
        if len(sel) < 20:
            continue
        d = mesurer(paquet, sel, conds)
        d["camp"] = camp
        par_camp.append(d)
    d = pd.concat(par_camp, ignore_index=True)

    hum = {}
    for camp in A38.CAMPS:
        sel = np.array([i for i in lignes if camps[i] == camp], dtype=int)
        if len(sel) < 20:
            continue
        hum[camp] = desirabilite_humaine(paquet, sel)
    gap_hum = pd.Series({it: hum["gauche"][it] - hum["droite"][it]
                         for it in items_camp
                         if it in hum["gauche"] and it in hum["droite"]})

    out = {}
    for cond, dc in d.groupby("condition"):
        piv = dc[dc.item.isin(items_camp)].pivot_table(
            index="item", columns="camp", values="ecart_desirabilite")
        if not {"gauche", "droite"}.issubset(piv.columns):
            continue
        g = piv["gauche"].values.astype(float)
        dr = piv["droite"].values.astype(float)
        ok = ~np.isnan(g) & ~np.isnan(dr)
        if ok.sum() < 4:
            continue
        gh = float(np.nanmean(gap_hum.reindex(piv.index).values[ok]))
        gs = gh - float((dr[ok] - g[ok]).mean())
        out[cond] = (gs / gh if abs(gh) > 1e-9 else np.nan, int(ok.sum()))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    args = ap.parse_args()

    paquet = C28.charger_tout(args.cache, args.cache_foret)
    items = paquet["items"]
    items_camp = [it for it in items if it in A38.POLE_ENDOGROUPE]
    camps = camps_gss(paquet["x"], paquet["attributs"])["bloc3"]
    toutes = [c for c in C28.ORDRE_METHODES if c in paquet["M"]]
    perimetres = {"1052": np.arange(len(paquet["ids"])),
                  "150": np.asarray(paquet["lignes150"])}

    # ------------------------------------------------ 1. invariance du facteur
    print("1. facteur d'amplification de a38, vraie assignation contre permutation "
          "intra camp", flush=True)
    rng = np.random.default_rng(A38.GRAINE)
    lignes_inv = []
    for nom_per, lignes in perimetres.items():
        conds = toutes if nom_per == "150" else [c for c in toutes
                                                 if c not in ("C2", "C3")]
        avant = facteur_par_condition(paquet, lignes, conds, camps, items_camp)

        # permutation des personnes a l'interieur de leur camp : les matrices simulees
        # sont reindexees, la verite humaine ne bouge pas. Si le facteur mesure les
        # personnes, il chute ; s'il mesure les marges du camp, il ne bouge pas.
        paquet_p = dict(paquet)
        perm = np.arange(len(paquet["ids"]))
        for camp in A38.CAMPS:
            sel = np.array([i for i in lignes if camps[i] == camp], dtype=int)
            if len(sel) > 1:
                perm[sel] = rng.permutation(sel)
        paquet_p["M"] = {c: (m[perm] if c not in ("humains vague 1",) else m)
                         for c, m in paquet["M"].items()}
        apres = facteur_par_condition(paquet_p, lignes, conds, camps, items_camp)

        for cond in avant:
            if cond not in apres:
                continue
            fa, n = avant[cond]
            fp, _ = apres[cond]
            lignes_inv.append({
                "perimetre": nom_per, "condition": cond, "n_items": n,
                "facteur_vraie_assignation": fa,
                "facteur_apres_permutation_intra_camp": fp,
                "ecart_absolu": abs(fa - fp)})
            print(f"  {nom_per} {cond:<28s} {fa: .6f} -> {fp: .6f} "
                  f"(ecart {abs(fa - fp):.2e})", flush=True)
    A38.ecrire(pd.DataFrame(lignes_inv), "a47-a38-invariance-facteur.csv")

    # -------------------------------------------- 2. taille du contexte de a35
    print("\n2. taille du contexte, regime facile contre regime severe", flush=True)
    m = len(items)
    index = {it: j for j, it in enumerate(items)}
    lignes_ctx = []
    for nom, membres in B.FAMILLES.items():
        cols = [index[i] for i in membres if i in index]
        lignes_ctx.append({
            "regime": "severe, retrait de la famille",
            "famille": nom, "n_items_retires": len(cols),
            "n_items_de_contexte": m - len(cols)})
        print(f"  {nom:<45s} {len(cols):>3d} retires, "
              f"{m - len(cols):>3d} items de contexte", flush=True)
    taille_bloc = int(np.ceil(m / B.N_BLOCS))
    lignes_ctx.append({
        "regime": "facile, retrait du bloc de validation croisee",
        "famille": f"bloc de {taille_bloc} items", "n_items_retires": taille_bloc,
        "n_items_de_contexte": m - taille_bloc})
    print(f"  bloc de validation croisee ({B.N_BLOCS} blocs)      "
          f"{taille_bloc:>3d} retires, {m - taille_bloc:>3d} items de contexte")
    A38.ecrire(pd.DataFrame(lignes_ctx), "a47-contexte-regimes.csv")

    # ------------------------------------------------- 3. B2 et les demographies
    print("\n3. B2 argmax et les demographies, par lecture de a2_baselines_gss",
          flush=True)
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                            "a2_baselines_gss.py")).read().splitlines()
    for i, l in enumerate(src, 1):
        if "b2_voisins" in l or "enc.transform" in l or "distance_hamming" in l:
            print(f"  ligne {i:>4d} : {l.strip()}", flush=True)


if __name__ == "__main__":
    main()
