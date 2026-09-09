"""
t1_mesures : la chute d'exactitude sous permutation des personnes intra segment, sur
Twin-2K-500, quatre segmentations, vingt et une conditions.

Preenregistrement : resultats/t1-preenregistrement.md, ecrit le 9 septembre 2026 a
01 h 08 CEST, avant ce script et avant tout calcul de resultat.

SORTIES, dans resultats/
  t1-controles.csv                     les sept controles, dont deux bloquants
  t1-chute-segmentations.csv           Q1, Q2 et Q3 pour toutes les conditions
  t1-reassignation.csv                 le gain hongrois absolu et son plancher B0 tirage
  t1-correlation-chute-exactitude.csv  Q6, brute et partialisee
  t1-classement.csv                    le verdict et sa coherence avec i3b
  t1-gss-contre-twin.csv               les conditions analogues des deux jeux

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.

Usage : .venv/bin/python analyses/t1_mesures.py --permutations 200
"""

import argparse
import os
import pickle
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np                              # noqa: E402
import pandas as pd                             # noqa: E402

import t1_commun as C                           # noqa: E402
import a44_commun as C44                        # noqa: E402
from a2_commun import exactitude_par_personne   # noqa: E402

SEGS = ["S_ideo", "S_fin", "S_gra", "S_parti"]
SEG_VERDICT = "S_gra"          # declaree au preenregistrement section 7
N_PERM_IC = 30                 # permutations a l'interieur d'un sous echantillon


# ---------------------------------------------------------------------------

def chute(cd, y1, s, n_perm, rng):
    """(exactitude vraie, exactitude permutee moyenne, bande) sur un perimetre donne."""
    vraie = float(np.nanmean(C.exactitude_codes(cd, y1)))
    perms = np.empty(n_perm)
    n = cd.shape[0]
    for r in range(n_perm):
        p = C44.permuter_intra(n, s, rng)
        perms[r] = float(np.nanmean(C.exactitude_codes(cd[p], y1)))
    return vraie, perms


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--permutations", type=int, default=C.N_PERMUTATIONS)
    ap.add_argument("--sous", type=int, default=C.N_SOUS)
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

    print(f"{paq['n']} personnes, {len(paq['colonnes'])} items, "
          f"{len(conditions)} conditions hors verite", flush=True)

    # ------------------------------------------------------------ controles
    ctrl = []

    # C1 bloquant : invariance exacte des deux ratios sous permutation intra segment.
    axes_i = ["ideologie politique"]
    sg = {"ideologie politique": paq["seg_a6"]["ideologie politique"]}
    rng_c = np.random.default_rng(C.GRAINE + 1)
    # La propriete a verifier est celle de a44 section 3.1 : les deux termes ne dependent
    # que de la table de contingence (segment, modalite), donc ils sont invariants sous
    # permutation des personnes A L'INTERIEUR DU MEME segment que celui de la mesure. La
    # mesure et la permutation partagent donc la segmentation, sans exception.
    pire = 0.0
    for nom in conditions:
        cd = paq["codes"][nom]
        for nom_seg in SEGS:
            s = paq["seg"][nom_seg]
            axes_s, sg_s = [nom_seg], {nom_seg: s}
            v0 = C.chaine_a1(cd, sg_s, axes_s, paq)
            p = C44.permuter_intra(cd.shape[0], s, rng_c)
            v1 = C.chaine_a1(cd[p], sg_s, axes_s, paq)
            pire = max(pire, abs(v0[0] - v1[0]), abs(v0[1] - v1[1]))
    ctrl.append({"controle": "bloquant 1, invariance des ratios sous permutation "
                             "intra segment", "valeur": pire, "seuil": 1e-12,
                 "passe": bool(pire <= 1e-12)})
    print(f"  controle 1, invariance : {pire:.3e}", flush=True)

    # C2 bloquant : le generateur nul redonne les marginales par item et par segment.
    n_items = len(paq["colonnes"])
    k_max = paq["k_max"]

    def marginales(mat, s, g_max):
        """Loi empirique de chaque item a l'interieur de chaque segment, (G, J, K)."""
        li, co = np.nonzero(mat >= 0)
        val = mat[li, co].astype(np.int64)
        plat = (s[li].astype(np.int64) * n_items + co) * k_max + val
        c = np.bincount(plat, minlength=g_max * n_items * k_max)
        c = c[:g_max * n_items * k_max].reshape(g_max, n_items, k_max).astype(float)
        tot = c.sum(axis=2, keepdims=True)
        return np.divide(c, np.where(tot > 0, tot, 1.0)), tot[:, :, 0]

    ecarts = []
    for nom in list(paq["codes"]):
        lignes = per.get(nom, np.arange(paq["n"]))
        cd = paq["codes"][nom][lignes]
        s = paq["seg"]["S_ideo"][lignes]
        g_max = int(s.max()) + 1
        cum, rep, tot_c = C44.lois_par_segment(cd, s, paq["k_items"])
        obs, eff = marginales(cd, s, g_max)
        rng = np.random.default_rng(C.GRAINE + 2)
        acc = np.zeros_like(obs)
        for _ in range(100):
            acc += marginales(C44.tirer_nul(cd, s, cum, rng), s, g_max)[0]
        acc /= 100.0
        masque = (eff >= C44.N_MIN_SEGMENT)
        e = float(np.abs(acc - obs).sum(axis=2)[masque].mean()) if masque.any() else 0.0
        ecarts.append({"condition": nom, "ecart_marginales": e,
                       "repli": rep / tot_c if tot_c else np.nan})
    pire2 = max(x["ecart_marginales"] for x in ecarts)
    ctrl.append({"controle": "bloquant 2, marginales du generateur nul, S_ideo, "
                             "100 replicats", "valeur": pire2, "seuil": 0.01,
                 "passe": bool(pire2 <= 0.01)})
    print(f"  controle 2, marginales : {pire2:.6f}", flush=True)

    # C4 : le masque, part des cellules ou la verite est observee et la prediction absente.
    for nom in conditions:
        lignes = per[nom]
        v = y_ref[lignes] >= 0
        p = paq["codes"][nom][lignes] >= 0
        perdu = float((v & ~p).sum() / max(int(v.sum()), 1))
        ctrl.append({"controle": f"masque, {nom}", "valeur": perdu, "seuil": 0.005,
                     "passe": bool(perdu <= 0.005)})

    # C5 : taux de repli du generateur nul, par segmentation et par condition.
    for nom_seg in SEGS:
        for nom in list(paq["codes"]):
            lignes = per.get(nom, np.arange(paq["n"]))
            cum, rep, tot = C44.lois_par_segment(paq["codes"][nom][lignes],
                                                 paq["seg"][nom_seg][lignes],
                                                 paq["k_items"])
            ctrl.append({"controle": f"repli du nul, {nom_seg}, {nom}",
                         "valeur": rep / tot if tot else np.nan,
                         "seuil": C.SEUIL_REPLI, "passe": bool(rep / tot <= C.SEUIL_REPLI)})

    # C6 : reproduction de a6 sur l'axe ideologie.
    rng = np.random.default_rng(C.GRAINE + 3)
    ref_a1 = C.chaine_a1(y_ref, sg, axes_i, paq, n_perm=C.N_PERM_A1, rng=rng)
    a6 = pd.read_csv(os.path.join(C.SORTIE, "a6-ratios-par-axe.csv"))
    a6 = a6[(a6["jeu"] == "twin2k500") & (a6["axe"] == "ideologie politique")
            & (a6["mesure"] == "entropie")].set_index("condition")
    for nom in conditions:
        if nom not in a6.index:
            continue
        v = C.chaine_a1(paq["codes"][nom], sg, axes_i, paq,
                        n_perm=C.N_PERM_A1, rng=np.random.default_rng(C.GRAINE + 3))
        ri, ra = v[0] / ref_a1[0], v[1] / ref_a1[1]
        e = max(abs(ri / float(a6.loc[nom, "ratio_inter"]) - 1),
                abs(ra / float(a6.loc[nom, "ratio_intra"]) - 1))
        ctrl.append({"controle": f"reproduction de a6, {nom}", "valeur": e,
                     "seuil": 0.02, "passe": bool(e <= 0.02)})

    # C7 : l'exactitude sur codes egale celle de a2_commun sur les chaines.
    obj_v = np.where(y_ref >= 0, y_ref.astype(object), None)
    e7 = 0.0
    for nom in ("Demographics Only - GPT4.1-mini", "Text Persona - GPT4.1-mini",
                C.PLANCHER):
        cd = paq["codes"][nom]
        obj_p = np.where(cd >= 0, cd.astype(object), -1)
        a = np.nanmean(C.exactitude_codes(cd, y_ref))
        b = np.nanmean(exactitude_par_personne(obj_p, obj_v))
        e7 = max(e7, abs(a - b))
    ctrl.append({"controle": "exactitude codes contre a2_commun sur chaines",
                 "valeur": e7, "seuil": 1e-12, "passe": bool(e7 <= 1e-12)})
    C.ecrire(ctrl, "t1-controles.csv")
    print(f"controles termines, {time.time() - t0:.0f}s", flush=True)

    # ------------------------------------------------- Q1, Q2, Q3 : la chute
    rng_p = np.random.default_rng(C.GRAINE + 10)
    brut = []
    for nom in conditions:
        lignes = per[nom]
        cd, y1 = paq["codes"][nom][lignes], y_ref[lignes]
        exa = C.exactitude_codes(cd, y1)
        moy, eb, eh = C.ic_bootstrap_moyenne(exa)
        for nom_seg in SEGS:
            s = paq["seg"][nom_seg][lignes]
            vraie, perms = chute(cd, y1, s, args.permutations, rng_p)
            moyp = float(perms.mean())
            opt = C.reassignation_codes(cd, y1, s)

            def f(idx, cd=cd, y1=y1, s=s):
                r = np.random.default_rng(C.GRAINE + 11)
                v = float(np.nanmean(C.exactitude_codes(cd[idx], y1[idx])))
                pp = np.mean([float(np.nanmean(C.exactitude_codes(
                    cd[idx][C44.permuter_intra(len(idx), s[idx], r)], y1[idx])))
                    for _ in range(N_PERM_IC)])
                return v - pp

            cb, ch, cet = C.ic_sous_echantillonnage(f, len(lignes), vraie - moyp,
                                                    s=args.sous)
            brut.append({
                "condition": nom, "etiquette": C.ETIQUETTE.get(nom, nom),
                "n": len(lignes), "segmentation": nom_seg,
                "n_cellules": len({int(k) for k in np.unique(s) if k >= 0}),
                "exactitude_vraie": vraie,
                "exactitude_ic_bas": eb, "exactitude_ic_haut": eh,
                "exactitude_permutee": moyp,
                "permutee_bas": float(np.percentile(perms, 2.5)),
                "permutee_haut": float(np.percentile(perms, 97.5)),
                "chute": vraie - moyp,
                "chute_ic_bas": cb, "chute_ic_haut": ch, "chute_ecart_type": cet,
                "chute_relative": (vraie - moyp) / vraie if vraie else np.nan,
                "exactitude_reassignation_optimale": opt,
                "gain_hongrois_absolu": opt - moyp,
                "part_recuperee_par_reassignation":
                    ((opt - moyp) / (vraie - moyp)) if abs(vraie - moyp) > 1e-9
                    else np.nan,
                "permutations": args.permutations,
                "masque_douteux": nom in C.MASQUE_DOUTEUX})
        print(f"  {C.ETIQUETTE.get(nom, nom)}, {time.time() - t0:.0f}s", flush=True)

    # plancher humain, recalcule par perimetre et par segmentation
    print("plancher humain par perimetre", flush=True)
    planchers = {}
    for n_uniq in sorted({len(per[c]) for c in conditions}):
        lignes = next(per[c] for c in conditions if len(per[c]) == n_uniq)
        cd, y1 = paq["codes"][C.PLANCHER][lignes], y_ref[lignes]
        for nom_seg in SEGS:
            s = paq["seg"][nom_seg][lignes]
            vraie, perms = chute(cd, y1, s, args.permutations, rng_p)
            planchers[(n_uniq, nom_seg)] = ((vraie - float(perms.mean())) / vraie,
                                            vraie - float(perms.mean()))
    for l in brut:
        cr, ca = planchers.get((l["n"], l["segmentation"]), (np.nan, np.nan))
        l["plancher_humain_chute_relative"] = cr
        l["plancher_humain_chute_absolue"] = ca
        l["part_du_plancher_humain"] = (l["chute_relative"] / cr
                                        if cr and abs(cr) > 1e-12 else np.nan)
    C.ecrire(brut, "t1-chute-segmentations.csv")

    # ------------------------------------------- test de Holm contre B0 tirage
    print("test de Holm contre B0 tirage", flush=True)
    famille = [c for c in conditions
               if c not in (C.PLANCHER, "B0 mode", "B0 tirage")]
    tests = []
    for nom in famille:
        lignes = per[nom]
        s = paq["seg"][SEG_VERDICT][lignes]
        cd, y1 = paq["codes"][nom][lignes], y_ref[lignes]
        b0 = paq["codes"]["B0 tirage"][lignes]
        rngs = np.random.default_rng(C.GRAINE + 12)
        m = max(len(lignes) // 2, 2)
        diffs = []
        for _ in range(args.sous):
            idx = np.sort(rngs.permutation(len(lignes))[:m])
            r = np.random.default_rng(C.GRAINE + 13)
            d1 = []
            d2 = []
            for _ in range(N_PERM_IC):
                p = C44.permuter_intra(len(idx), s[idx], r)
                d1.append(float(np.nanmean(C.exactitude_codes(cd[idx][p], y1[idx]))))
                d2.append(float(np.nanmean(C.exactitude_codes(b0[idx][p], y1[idx]))))
            c1 = float(np.nanmean(C.exactitude_codes(cd[idx], y1[idx]))) - np.mean(d1)
            c2 = float(np.nanmean(C.exactitude_codes(b0[idx], y1[idx]))) - np.mean(d2)
            diffs.append(c1 - c2)
        diffs = np.asarray(diffs)
        p = 2.0 * min((diffs <= 0).mean(), (diffs >= 0).mean())
        tests.append({"condition": nom, "difference_moyenne": float(diffs.mean()),
                      "p": float(min(max(p, 1.0 / len(diffs)), 1.0))})
    ph = C.holm([t["p"] for t in tests])
    for t, v in zip(tests, ph):
        t["p_holm"] = float(v)
        t["segmentation"] = SEG_VERDICT

    # ---------------------------------------------------- Q3 : la reassignation
    plancher_b0 = {}
    for l in brut:
        if l["condition"] == "B0 tirage":
            plancher_b0[l["segmentation"]] = l["gain_hongrois_absolu"]
    reas = []
    for l in brut:
        reas.append({
            "condition": l["condition"], "etiquette": l["etiquette"], "n": l["n"],
            "segmentation": l["segmentation"],
            "gain_hongrois_absolu": l["gain_hongrois_absolu"],
            "plancher_B0_tirage": plancher_b0.get(l["segmentation"], np.nan),
            "au_dessus_du_plancher":
                bool(l["gain_hongrois_absolu"] > plancher_b0.get(l["segmentation"],
                                                                np.inf)),
            "chute": l["chute"],
            "rapport_publie": l["part_recuperee_par_reassignation"]})
    C.ecrire(reas, "t1-reassignation.csv")

    # ------------------------- Q6 : correlation chute contre exactitude brute
    from scipy.stats import pearsonr, spearmanr
    cor, resid = [], []
    for nom_seg in SEGS:
        for etendue, garde in (
                ("les seize conditions de la famille primaire",
                 lambda l: l["condition"] in famille),
                ("famille primaire plus le plancher humain",
                 lambda l: l["condition"] in famille + [C.PLANCHER]),
                ("toutes conditions, temoins compris", lambda l: True)):
            sel = [l for l in brut if l["segmentation"] == nom_seg and garde(l)]
            x = np.array([l["exactitude_vraie"] for l in sel])
            y = np.array([l["chute"] for l in sel])
            pr, sp = float(pearsonr(x, y)[0]), float(spearmanr(x, y)[0])
            cor.append({"segmentation": nom_seg, "etendue": etendue,
                        "n_conditions": len(sel), "pearson": pr, "spearman": sp,
                        "variance_partagee": pr ** 2})
            if etendue.startswith("les seize"):
                a, b = np.polyfit(x, y, 1)
                for l, xi, yi in zip(sel, x, y):
                    resid.append({
                        "segmentation": nom_seg, "condition": l["condition"],
                        "etiquette": l["etiquette"],
                        "exactitude": xi, "chute": yi,
                        "chute_predite_par_exactitude": a * xi + b,
                        "residu": yi - (a * xi + b),
                        "part_du_plancher_humain": l["part_du_plancher_humain"]})
    C.ecrire(cor, "t1-correlation-chute-exactitude.csv")
    C.ecrire(resid, "t1-correlation-residus.csv")

    # ------------------------------- classement et coherence avec i3b
    i3b_s = pd.read_csv(os.path.join(C.SORTIE, "i3b-twin-sources-pures.csv"))
    i3b_s = i3b_s.set_index("source")
    ab = pd.read_csv(os.path.join(C.SORTIE, "i3b-twin-abaque.csv"))
    ab = (ab[ab["taille"] == 2058].groupby("configuration")["tau_etoile_holm39"]
          .min().to_dict())
    ptests = {t["condition"]: t for t in tests}
    classement = []
    for l in brut:
        if l["condition"] in ("B0 mode", "B0 tirage", C.PLANCHER):
            lecture = "temoin ou reference"
        else:
            v = l["part_du_plancher_humain"]
            lecture = ("gabarit de groupe" if v < C.SEUIL_GABARIT else
                       "porteur de personne" if v > C.SEUIL_PERSONNE else
                       "intermediaire")
        t = ptests.get(l["condition"], {})
        classement.append({
            "condition": l["condition"], "etiquette": l["etiquette"], "n": l["n"],
            "segmentation": l["segmentation"],
            "exactitude_vraie": l["exactitude_vraie"],
            "chute": l["chute"], "chute_relative": l["chute_relative"],
            "part_du_plancher_humain": l["part_du_plancher_humain"],
            "rapport_de_reassignation": l["part_recuperee_par_reassignation"],
            "lecture": lecture,
            "p_holm_contre_B0_tirage": t.get("p_holm", np.nan)
            if l["segmentation"] == SEG_VERDICT else np.nan,
            "i3b_A_deficit_patrons": float(i3b_s.loc[l["condition"], "A"])
            if l["condition"] in i3b_s.index else np.nan,
            "i3b_B_exces_correlation": float(i3b_s.loc[l["condition"], "B"])
            if l["condition"] in i3b_s.index else np.nan,
            "i3b_tau_etoile_holm39_2058": ab.get(l["condition"], np.nan),
            "masque_douteux": l["masque_douteux"]})
    C.ecrire(classement, "t1-classement.csv")

    # coherence, Spearman
    lignes_coh = []
    for nom_seg in SEGS:
        sel = [c for c in classement if c["segmentation"] == nom_seg
               and np.isfinite(c["i3b_tau_etoile_holm39_2058"])
               and np.isfinite(c["part_du_plancher_humain"])]
        if len(sel) >= 4:
            x = np.array([c["part_du_plancher_humain"] for c in sel])
            y = np.array([c["i3b_tau_etoile_holm39_2058"] for c in sel])
            a = np.array([c["i3b_A_deficit_patrons"] for c in sel])
            e = np.array([c["exactitude_vraie"] for c in sel])
            lignes_coh.append({
                "segmentation": nom_seg, "n": len(sel),
                "spearman_part_contre_tau_etoile": float(spearmanr(x, y)[0]),
                "spearman_part_contre_A": float(spearmanr(x, a)[0]),
                "spearman_part_contre_exactitude": float(spearmanr(x, e)[0]),
                "spearman_exactitude_contre_tau_etoile": float(spearmanr(e, y)[0])})
    C.ecrire(lignes_coh, "t1-coherence-i3b.csv")

    # ----------------------------------------- GSS contre Twin, conditions analogues
    gss = pd.read_csv(os.path.join(C.SORTIE, "a47-chute-deux-segmentations.csv"))
    corr = {"S_ideo": "S_ideo", "S_fin": "S_fin", "S_gra": "S_gra"}
    comp = []
    for nom_seg in ("S_ideo", "S_fin", "S_gra"):
        g = gss[gss["segmentation"] == corr[nom_seg]].set_index("condition")
        for cond_g in g.index:
            comp.append({"jeu": "GSS", "condition": cond_g, "segmentation": nom_seg,
                         "n": int(g.loc[cond_g, "n_cellules"]),
                         "exactitude_vraie": float(g.loc[cond_g, "exactitude_vraie"]),
                         "chute_relative": float(g.loc[cond_g, "chute_relative"]),
                         "part_du_plancher_humain":
                             float(g.loc[cond_g, "part_du_plancher_humain"])})
        for l in brut:
            if l["segmentation"] != nom_seg:
                continue
            comp.append({"jeu": "Twin", "condition": l["condition"],
                         "segmentation": nom_seg, "n": l["n_cellules"],
                         "exactitude_vraie": l["exactitude_vraie"],
                         "chute_relative": l["chute_relative"],
                         "part_du_plancher_humain": l["part_du_plancher_humain"]})
    C.ecrire(comp, "t1-gss-contre-twin.csv")
    C.ecrire(tests, "t1-holm-contre-b0.csv")

    print(f"\ntermine en {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
