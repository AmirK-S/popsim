"""
t1_verdict : le test preenregistre, refait avec assez de sous echantillons pour que la
correction de Holm puisse atteindre 0,05.

POURQUOI CE SCRIPT EXISTE. Le preenregistrement fixe la famille primaire a seize
conditions et la correction de Holm. Le premier passage de t1_mesures.py emploie
S = 200 sous echantillons, ce qui plafonne la plus petite valeur de p atteignable a
1 / 200 = 0,005 ; Holm sur seize tests exige p <= 0,05 / 16 = 0,003125. Le verdict etait
donc arithmetiquement hors d'atteinte, quelle que soit la force du signal. Ce n'est pas un
resultat, c'est une resolution insuffisante, et le rapport le declare. Ce script refait le
seul test de verdict avec S = 2 000, ce qui porte le plancher a 0,0005.

Rien d'autre ne change : meme segmentation de verdict `S_gra`, meme famille de seize, meme
statistique, memes graines de base, meme comparateur `B0 tirage`.

Sortie : resultats/t1-holm-contre-b0.csv, reecrit avec la colonne `sous_echantillons`.

Usage : .venv/bin/python analyses/t1_verdict.py --sous 2000
"""

import argparse
import os
import pickle
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np           # noqa: E402

import t1_commun as C        # noqa: E402
import a44_commun as C44     # noqa: E402

SEG_VERDICT = "S_gra"
N_PERM_IC = 30


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sous", type=int, default=2000)
    ap.add_argument("--cache-baselines", default="/tmp/t1-baselines.pkl")
    args = ap.parse_args()
    t0 = time.time()

    paq = C.charger()
    base = pickle.load(open(args.cache_baselines, "rb"))
    for nom, mat in base.items():
        paq["codes"][nom] = mat
        paq["couverture"][nom] = np.arange(paq["n"])
    per = C.perimetres(paq)
    y_ref = paq["codes"][C.REF]
    famille = [c for c in paq["codes"]
               if c not in (C.REF, C.PLANCHER, "B0 mode", "B0 tirage")]

    tests = []
    for nom in famille:
        li = per[nom]
        s = paq["seg"][SEG_VERDICT][li]
        cd, y1, b0 = paq["codes"][nom][li], y_ref[li], paq["codes"]["B0 tirage"][li]
        rngs = np.random.default_rng(C.GRAINE + 12)
        m = max(len(li) // 2, 2)
        diffs = np.empty(args.sous)
        for b in range(args.sous):
            idx = np.sort(rngs.permutation(len(li))[:m])
            r = np.random.default_rng(C.GRAINE + 13)
            p1 = np.empty(N_PERM_IC)
            p2 = np.empty(N_PERM_IC)
            for k in range(N_PERM_IC):
                p = C44.permuter_intra(len(idx), s[idx], r)
                p1[k] = np.nanmean(C.exactitude_codes(cd[idx][p], y1[idx]))
                p2[k] = np.nanmean(C.exactitude_codes(b0[idx][p], y1[idx]))
            c1 = float(np.nanmean(C.exactitude_codes(cd[idx], y1[idx]))) - p1.mean()
            c2 = float(np.nanmean(C.exactitude_codes(b0[idx], y1[idx]))) - p2.mean()
            diffs[b] = c1 - c2
        p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
        tests.append({"condition": nom, "etiquette": C.ETIQUETTE.get(nom, nom),
                      "segmentation": SEG_VERDICT,
                      "difference_moyenne": float(diffs.mean()),
                      "difference_bas": float(np.percentile(diffs, 2.5)),
                      "difference_haut": float(np.percentile(diffs, 97.5)),
                      "part_des_sous_echantillons_positifs": float((diffs > 0).mean()),
                      "p": float(min(max(p, 1.0 / args.sous), 1.0)),
                      "sous_echantillons": args.sous})
        print(f"  {C.ETIQUETTE.get(nom, nom)}, {time.time() - t0:.0f}s", flush=True)

    for t, v in zip(tests, C.holm([x["p"] for x in tests])):
        t["p_holm"] = float(v)
        t["verdict_holm_5pc"] = bool(v <= 0.05)
    C.ecrire(tests, "t1-holm-contre-b0.csv")
    print(f"termine en {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
