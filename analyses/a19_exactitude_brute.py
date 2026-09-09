"""a19 : exactitude appariee calculee sur les chaines BRUTES, sans appariement a la
nomenclature, c'est a dire avec la definition litterale des auteurs ("responses match
exactly"). Complement de a19_denominateurs.py, qui emploie le codage de a1.

Le but est de montrer que la conclusion de l'objection 1.1 de a17 ne depend pas du
choix de definition.
"""
import csv
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a1_double_distorsion as A1

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREP = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                            "new_analysis_summaries/gss_filtered/preparation")
SORTIE = os.path.join(RACINE, "resultats")
EXCLUS_STANFORD = {q.lower() for q in [
    "BORN", "DEGREE*", "DWELOWN", "EDUC*", "FAMDIF16", "HISPANIC", "MADEG*", "MAEDUC*",
    "MARITAL", "MARTYPE*", "MAWRKGRW", "PADEG*", "PAEDUC*", "PARTYID", "RACE*", "REG16",
    "RELIG*", "RELPERSN", "RVISITOR", "SEX*", "SPEDUC*", "SPRTPRSN", "SPWRKSTA",
    "VETYEARS", "VISITORS", "WIDOWED", "ZODIAC"]}

FICHIERS = {
    "humains vague 2": "p_wave2_summary.csv",
    "agents composite": "composite_agents_summary.csv",
    "agents entretien (v3)": "gss_v3_summary.csv",
    "agents enquete": "survey_agents_summary.csv",
    "agents persona (v7)": "gss_v7_summary.csv",
    "agents demographiques (v6)": "gss_v6_summary.csv",
    "agents demographiques (v8)": "gss_v8_summary.csv",
}


def main():
    w1 = pd.read_csv(os.path.join(PREP, "p_wave1_summary.csv"))
    entetes = [c for c in w1.columns if c != "email"]
    n = len(w1)
    ref = w1[entetes].astype(str).values

    jeux = {
        "177 items (tous)": entetes,
        "169 items (a1)": [q for q in entetes if q not in A1.ITEMS_DEMOGRAPHIQUES],
        "150 items (Stanford)": [q for q in entetes if q.lower() not in EXCLUS_STANFORD],
        "149 items (a2, a7, a8, a12)": [q for q in entetes
                                        if q.lower() not in EXCLUS_STANFORD and q != "polviews"],
    }
    cond = {}
    for lib, f in FICHIERS.items():
        cond[lib] = pd.read_csv(os.path.join(PREP, f))[entetes].astype(str).values

    rng = np.random.default_rng(20260910)
    lignes = [["jeu_items", "n_items", "condition_a", "condition_b", "acc_a", "acc_b",
               "ecart_appari_b_moins_a", "ic_bas", "ic_haut", "t_appari"]]
    lignes_r = [["jeu_items", "n_items", "test_retest_pct"]]
    idx = {q: j for j, q in enumerate(entetes)}
    for lib, qs in jeux.items():
        col = np.array([idx[q] for q in qs])
        acc = {c: (cond[c][:, col] == ref[:, col]).mean(axis=1) for c in cond}
        print(f"\n{lib}, {len(qs)} items  (chaines brutes)")
        for c in acc:
            print(f"   {c:<30}{acc[c].mean() * 100:8.4f} %")
        lignes_r.append([lib, len(qs), f"{acc['humains vague 2'].mean() * 100:.4f}"])
        for a, b in [("agents persona (v7)", "agents demographiques (v8)"),
                     ("agents demographiques (v6)", "agents demographiques (v8)")]:
            d = acc[b] - acc[a]
            tir = [d[rng.integers(0, n, size=n)].mean() for _ in range(2000)]
            bas, haut = np.percentile(tir, [2.5, 97.5])
            t = d.mean() / (d.std(ddof=1) / np.sqrt(n))
            print(f"   {b} moins {a} : {d.mean() * 100:+.2f} pt "
                  f"[{bas * 100:+.2f} ; {haut * 100:+.2f}]  t = {t:.2f}")
            lignes.append([lib, len(qs), a, b, f"{acc[a].mean() * 100:.4f}",
                           f"{acc[b].mean() * 100:.4f}", f"{d.mean() * 100:.4f}",
                           f"{bas * 100:.4f}", f"{haut * 100:.4f}", f"{t:.4f}"])
    with open(os.path.join(SORTIE, "a19-exactitude-brute.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes + [[]] + lignes_r)
    print("\necrit : resultats/a19-exactitude-brute.csv")


if __name__ == "__main__":
    main()
