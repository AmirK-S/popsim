"""
t1_nul : le generateur nul conditionnellement independant de Yuan, applique aux ratios
inter et intra de Twin-2K-500 publies par a6.

Preenregistrement : resultats/t1-preenregistrement.md, quantites Q4 et Q5.

QUESTION. a44 a montre sur le GSS que les deux ratios de a1 sont des fonctionnelles de la
seule table de contingence (segment, modalite), donc exactement invariants sous permutation
des personnes intra segment, et reproduits a un pour cent pres par un generateur qui tire
chaque reponse independamment dans la marginale de son segment. a6 publie les memes deux
ratios sur Twin, avec un gonflement de 1,57 a 3,73. Le nul les reproduit il aussi ?

CE QUI EST IMPORTE TEL QUEL : a44_commun.lois_par_segment et a44_commun.tirer_nul pour le
generateur ; a1_double_distorsion.construire_index / compter / decomposer / agreger pour
la mesure, par t1_commun.chaine_a1.

Q4, primaire   : axe ideologie, nul conditionne sur l'ideologie. Le nul et la mesure
                 partagent le meme axe, comme le tableau 1 de a44 l'impose.
Q5, secondaire : les six axes de a6 agreges, sous un nul qui ne connait que l'ideologie.
                 Declaree d'avance comme une BORNE INFERIEURE de la part reproduite.

SORTIES : resultats/t1-generateur-nul.csv, resultats/t1-generateur-nul-six-axes.csv

Usage : .venv/bin/python analyses/t1_nul.py --replicats 200
"""

import argparse
import os
import pickle
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np                  # noqa: E402

import t1_commun as C               # noqa: E402
import a44_commun as C44            # noqa: E402
import i3b_commun as J              # noqa: E402

AXE = "ideologie politique"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicats", type=int, default=C.N_REPLICATS)
    ap.add_argument("--replicats-six-axes", type=int, default=50)
    ap.add_argument("--sous", type=int, default=100)
    ap.add_argument("--replicats-sous", type=int, default=20)
    ap.add_argument("--cache-baselines", default="/tmp/t1-baselines.pkl")
    args = ap.parse_args()
    t0 = time.time()

    paq = C.charger()
    base = pickle.load(open(args.cache_baselines, "rb"))
    for nom, mat in base.items():
        paq["codes"][nom] = mat
        paq["couverture"][nom] = np.arange(paq["n"])
    per = C.perimetres(paq)
    conditions = [c for c in paq["codes"] if c != C.REF]
    y_ref = paq["codes"][C.REF]
    seg_ideo = paq["seg_a6"][AXE]
    axes_i, axes6 = [AXE], paq["axes_a6"]
    i_axe = axes6.index(AXE)

    def mesure_axe(codes, s, n_perm, rng):
        return C.chaine_a1(codes, {AXE: s}, axes_i, paq, n_perm=n_perm, rng=rng)

    def mesure_six(codes, sg6, n_perm, rng):
        return C.chaine_a1(codes, sg6, axes6, paq, n_perm=n_perm, rng=rng)

    lignes_sortie, lignes_six = [], []
    for nom in conditions:
        t1 = time.time()
        li = per[nom]
        cd, s = paq["codes"][nom][li], seg_ideo[li]
        ref_i, ref_a = mesure_axe(y_ref[li], s, C.N_PERM_A1,
                                  np.random.default_rng(C.GRAINE + 20))
        obs_i, obs_a = mesure_axe(cd, s, C.N_PERM_A1,
                                  np.random.default_rng(C.GRAINE + 21))
        cum, rep, tot = C44.lois_par_segment(cd, s, paq["k_items"])

        rng = np.random.default_rng(C.GRAINE + 22)
        ni, na = [], []
        for r in range(args.replicats):
            nul = C44.tirer_nul(cd, s, cum, rng)
            a, b = mesure_axe(nul, s, C.N_PERM_A1_NUL, rng)
            ni.append(a)
            na.append(b)
        ni, na = np.asarray(ni), np.asarray(na)

        # IC pivote sur la difference d = ratio mesure moins ratio de son nul. Le nul est
        # RETIRE dans chaque sous echantillon, seule facon d'avoir un intervalle qui porte
        # l'incertitude d'echantillon et pas seulement celle du nul.
        rngs = np.random.default_rng(C.GRAINE + 23)
        n = len(li)
        m = max(n // 2, 2)
        d_i, d_a = [], []
        for _ in range(args.sous):
            idx = np.sort(rngs.permutation(n)[:m])
            r_i, r_a = mesure_axe(y_ref[li][idx], s[idx], C.N_PERM_A1_NUL, rngs)
            o_i, o_a = mesure_axe(cd[idx], s[idx], C.N_PERM_A1_NUL, rngs)
            cum2, _, _ = C44.lois_par_segment(cd[idx], s[idx], paq["k_items"])
            vi, va = [], []
            for _ in range(args.replicats_sous):
                nul = C44.tirer_nul(cd[idx], s[idx], cum2, rngs)
                a, b = mesure_axe(nul, s[idx], C.N_PERM_A1_NUL, rngs)
                vi.append(a)
                va.append(b)
            d_i.append(o_i / r_i - float(np.mean(vi)) / r_i)
            d_a.append(o_a / r_a - float(np.mean(va)) / r_a)
        echelle = np.sqrt(m / n) * J.correction_population_finie(m, n)

        for terme, obs, ref, tir, dd in (("inter", obs_i, ref_i, ni, d_i),
                                         ("intra", obs_a, ref_a, na, d_a)):
            ratio = obs / ref if ref else np.nan
            r_nul = tir / ref if ref else np.full(len(tir), np.nan)
            d = ratio - float(r_nul.mean())
            sd = float(r_nul.std(ddof=1))
            p = 2.0 * min((r_nul >= ratio).mean(), (r_nul <= ratio).mean())
            bas, haut, et = J.ic_pivote(dd, centre=d, echelle=echelle)
            lignes_sortie.append({
                "condition": nom, "etiquette": C.ETIQUETTE.get(nom, nom), "n": n,
                "segmentation": "S_ideo", "axe": AXE, "terme": terme,
                "ratio_mesure": ratio,
                "ratio_nul_moyen": float(r_nul.mean()),
                "nul_bas": float(np.percentile(r_nul, 2.5)),
                "nul_haut": float(np.percentile(r_nul, 97.5)),
                "part_reproduite": float(r_nul.mean()) / ratio if ratio else np.nan,
                "d": d, "z": d / sd if sd > 0 else np.nan,
                "d_ic_bas": bas, "d_ic_haut": haut, "d_ecart_type_sous_ech": et,
                "p_replicats": float(min(max(p, 1.0 / len(r_nul)), 1.0)),
                "replicats": args.replicats,
                "taux_repli_nul": rep / tot if tot else np.nan,
                "masque_douteux": nom in C.MASQUE_DOUTEUX})

        # ------------------------------------- Q5, les six axes, borne inferieure
        sg6 = {a: paq["seg_a6"][a][li] for a in axes6}
        r6_i, r6_a = mesure_six(y_ref[li], sg6, C.N_PERM_A1,
                                np.random.default_rng(C.GRAINE + 24))
        o6_i, o6_a = mesure_six(cd, sg6, C.N_PERM_A1,
                                np.random.default_rng(C.GRAINE + 25))
        rng6 = np.random.default_rng(C.GRAINE + 26)
        n6i, n6a = [], []
        for _ in range(args.replicats_six_axes):
            nul = C44.tirer_nul(cd, s, cum, rng6)
            a, b = mesure_six(nul, sg6, C.N_PERM_A1_NUL, rng6)
            n6i.append(a)
            n6a.append(b)
        for terme, obs, ref, tir in (("inter", o6_i, r6_i, np.asarray(n6i)),
                                     ("intra", o6_a, r6_a, np.asarray(n6a))):
            ratio = obs / ref if ref else np.nan
            r_nul = tir / ref if ref else np.full(len(tir), np.nan)
            lignes_six.append({
                "condition": nom, "etiquette": C.ETIQUETTE.get(nom, nom), "n": n,
                "axes": "six axes de a6", "nul_conditionne_sur": "ideologie seule",
                "terme": terme, "ratio_mesure": ratio,
                "ratio_nul_moyen": float(r_nul.mean()),
                "nul_bas": float(np.percentile(r_nul, 2.5)),
                "nul_haut": float(np.percentile(r_nul, 97.5)),
                "part_reproduite_borne_inferieure":
                    float(r_nul.mean()) / ratio if ratio else np.nan,
                "replicats": args.replicats_six_axes})
        print(f"  {C.ETIQUETTE.get(nom, nom)}, {time.time() - t1:.0f}s "
              f"(total {time.time() - t0:.0f}s)", flush=True)

    C.ecrire(lignes_sortie, "t1-generateur-nul.csv")
    C.ecrire(lignes_six, "t1-generateur-nul-six-axes.csv")
    print(f"\ntermine en {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
