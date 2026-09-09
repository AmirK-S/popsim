"""a19 : objection a17 4.3, la correlation de 0,80 de a8 section 5.3.

Recalcul de la correlation de rang entre l'avantage du modele par item et la stabilite
test retest de l'item, avec et sans le bloc de preferences de prix, et au niveau du bloc
et non de l'item. Lecture seule de resultats/a8-twin-par-item.csv, aucun script modifie.
"""
import csv
import os
import sys

import numpy as np
import pandas as pd
from scipy.stats import spearmanr

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

CONFIGS = ["GPT-4.1-mini, persona texte", "GPT-4.1, persona JSON",
           "Gemini-Flash-2.5, persona texte", "GPT-4.1-mini, affine sur 500 exemples"]


def main():
    d = pd.read_csv(os.path.join(SORTIE, "a8-twin-par-item.csv"))
    print(f"{len(d)} items, {d['bloc'].nunique()} blocs")
    tailles = d["bloc"].value_counts()
    print("blocs les plus gros :")
    print(tailles.head(5).to_string())
    base = np.maximum(d["B1 argmax"].values, d["B2 argmax"].values)

    # identification du bloc de prix : le plus gros bloc, verifie par son nom
    bloc_prix = tailles.index[0]
    print(f"\nbloc le plus gros : {bloc_prix!r}, {tailles.iloc[0]} items")
    hors = d["bloc"].values != bloc_prix

    lignes = [["configuration", "perimetre", "n", "spearman_avantage_retest", "p"]]
    for cfg in CONFIGS:
        av = d[cfg].values - base
        for lib, msk in [("108 items, tous", np.ones(len(d), dtype=bool)),
                         (f"hors bloc {bloc_prix}", hors)]:
            r, p = spearmanr(av[msk], d["retest_humain"].values[msk])
            print(f"{cfg:<45}{lib:<28}n={msk.sum():>4}  r={r:+.3f}  p={p:.2e}")
            lignes.append([cfg, lib, int(msk.sum()), f"{r:.4f}", f"{p:.3e}"])
        # au niveau du bloc : moyenne par bloc, puis correlation sur les blocs
        t = pd.DataFrame({"bloc": d["bloc"], "av": av, "ret": d["retest_humain"]})
        g = t.groupby("bloc").mean(numeric_only=True)
        r, p = spearmanr(g["av"], g["ret"])
        print(f"{cfg:<45}{'au niveau du bloc':<28}n={len(g):>4}  r={r:+.3f}  p={p:.2e}")
        lignes.append([cfg, "au niveau du bloc", len(g), f"{r:.4f}", f"{p:.3e}"])
        # blocs a plus d'un item seulement
        gm = t.groupby("bloc").agg(n=("av", "size"), av=("av", "mean"), ret=("ret", "mean"))
        gm = gm[gm["n"] > 1]
        r, p = spearmanr(gm["av"], gm["ret"])
        print(f"{cfg:<45}{'blocs a plus d un item':<28}n={len(gm):>4}  r={r:+.3f}  p={p:.2e}")
        lignes.append([cfg, "blocs a plus d un item", len(gm), f"{r:.4f}", f"{p:.3e}"])
        print()

    # avantage moyen dans et hors le bloc de prix, config principale
    av = d[CONFIGS[0]].values - base
    print(f"avantage moyen dans le bloc {bloc_prix} : {av[~hors].mean():+.4f}")
    print(f"avantage moyen hors ce bloc           : {av[hors].mean():+.4f}")
    lignes.append(["GPT-4.1-mini, persona texte", f"avantage moyen dans {bloc_prix}",
                   int((~hors).sum()), f"{av[~hors].mean():.4f}", ""])
    lignes.append(["GPT-4.1-mini, persona texte", "avantage moyen hors ce bloc",
                   int(hors.sum()), f"{av[hors].mean():.4f}", ""])
    n_blocs = d["bloc"].nunique()
    n_uniq = int((d["bloc"].value_counts() == 1).sum())
    print(f"{n_blocs} blocs, dont {n_uniq} a un seul item")
    lignes.append(["structure", "blocs", n_blocs, "", ""])
    lignes.append(["structure", "blocs a un seul item", n_uniq, "", ""])

    with open(os.path.join(SORTIE, "a19-a8-correlation-blocs.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)
    print("ecrit : resultats/a19-a8-correlation-blocs.csv")


if __name__ == "__main__":
    main()
