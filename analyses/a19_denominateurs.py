"""a19 : recalculs demandes par la relecture adverse a17.

Trois blocs, aucun appel de modele, aucune ecriture dans data/.

  1. exactitude appariee v7 contre v8 (et v6 contre v8) ET ratios inter/intra
     sur le MEME jeu d'items, pour les quatre jeux 177 / 169 / 150 / 149.
  2. taux de recopie item par item des items ecartes, par condition, avec la
     modalite majoritaire en regard.
  3. presence de `income` dans les 149 items de a2 et accord avec l'attribut.

Les fonctions de mesure sont importees telles quelles de a1_double_distorsion,
aucun script existant n'est modifie.

Usage : .venv/bin/python analyses/a19_denominateurs.py [--bootstrap 1000] [--permutations 50]
"""
import argparse
import csv
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a1_double_distorsion as A1

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PREP = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                            "new_analysis_summaries/gss_filtered/preparation")
DEMOG = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure3/data/demographic_summary.csv")
SORTIE = os.path.join(RACINE, "resultats")

# Liste d'exclusion de Stanford, recopiee a l'identique de a2_baselines_gss.py.
EXCLUS_STANFORD = {q.lower() for q in [
    "BORN", "DEGREE*", "DWELOWN", "EDUC*", "FAMDIF16", "HISPANIC", "MADEG*", "MAEDUC*",
    "MARITAL", "MARTYPE*", "MAWRKGRW", "PADEG*", "PAEDUC*", "PARTYID", "RACE*", "REG16",
    "RELIG*", "RELPERSN", "RVISITOR", "SEX*", "SPEDUC*", "SPRTPRSN", "SPWRKSTA",
    "VETYEARS", "VISITORS", "WIDOWED", "ZODIAC"]}
FUITE_A2 = {"polviews"}

CONDITIONS = A1.CONDITIONS
MESURES = A1.MESURES
AXES = A1.AXES


def ic_percentile_translate(tirages, cible):
    """Intervalle de percentile translate sur l'estimation ponctuelle.

    C'est exactement la fonction `recentrer` de a1 : v - moyenne(v) + cible. Le nom
    employe ici est celui que a17 objection 1.6 demande ; le calcul est inchange.
    """
    v = np.asarray(tirages, dtype=float)
    v = v[np.isfinite(v)]
    if v.size == 0:
        return float("nan"), float("nan")
    v = v - v.mean() + cible
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--permutations", type=int, default=50)
    ap.add_argument("--graine", type=int, default=20260903)
    args = ap.parse_args()

    rng = np.random.default_rng(args.graine)
    os.makedirs(SORTIE, exist_ok=True)

    options, ordinal = A1.lire_nomenclature(os.path.join(RACINE, A1.RACINE_DEFAUT))
    entetes = next(csv.reader(open(os.path.join(PREP, "p_wave1_summary.csv"),
                                   encoding="utf-8")))[1:]
    n_items = len(entetes)

    donnees, ids_ref = {}, None
    for libelle, fichier in CONDITIONS:
        chemin = os.path.join(PREP, fichier)
        if not os.path.exists(chemin):
            continue
        x, ids, _ = A1.lire_condition(chemin, entetes, options)
        if ids_ref is None:
            ids_ref = ids
        donnees[libelle] = x
    noms = [c for c, _ in CONDITIONS if c in donnees]
    n = len(ids_ref)
    seg, niveaux = A1.lire_demographies(os.path.join(RACINE, A1.RACINE_DEFAUT), ids_ref)

    # ---- les quatre jeux d'items ------------------------------------------
    m177 = np.ones(n_items, dtype=bool)
    m169 = np.array([q not in A1.ITEMS_DEMOGRAPHIQUES for q in entetes])
    m150 = np.array([q.lower() not in EXCLUS_STANFORD for q in entetes])
    m149 = np.array([(q.lower() not in EXCLUS_STANFORD) and (q not in FUITE_A2)
                     for q in entetes])
    JEUX = [("177 items (tous)", m177), ("169 items (a1)", m169),
            ("150 items (Stanford)", m150), ("149 items (a2, a7, a8, a12)", m149)]
    for lib, msk in JEUX:
        print(f"{lib:<32}{int(msk.sum()):>5} items")

    # ---- 1. exactitude appariee -------------------------------------------
    # Exactitude par personne : moyenne sur les items du jeu des cellules identiques a
    # la vague 1. On travaille sur les codes entiers, un non codable (-1) ne peut pas
    # egaler une reponse humaine valide, ce qui est le comportement voulu.
    ref = donnees["humains vague 1"]

    def acc_par_personne(cond, msk):
        x = donnees[cond]
        ok = (x == ref) & (ref >= 0)
        return ok[:, msk].sum(axis=1) / float(msk.sum())

    lignes_acc = [["jeu_items", "n_items", "condition_a", "condition_b",
                   "acc_a", "acc_b", "ecart_appari_b_moins_a",
                   "ic_bas", "ic_haut", "t_appari"]]
    print("\n" + "=" * 92)
    print("1. EXACTITUDE APPARIEE SUR LE MEME JEU D'ITEMS")
    print("=" * 92)
    paires = [("agents persona (v7)", "agents demographiques (v8)"),
              ("agents demographiques (v6)", "agents demographiques (v8)")]
    accs = {}
    for lib, msk in JEUX:
        for c in noms:
            accs[(lib, c)] = acc_par_personne(c, msk)
        print(f"\n{lib}, {int(msk.sum())} items")
        for c in noms:
            print(f"   {c:<30}{accs[(lib, c)].mean() * 100:8.2f} %")
        for a, b in paires:
            d = accs[(lib, b)] - accs[(lib, a)]
            # bootstrap apparie sur les personnes, meme tirage des deux cotes
            tirages = []
            r2 = np.random.default_rng(args.graine + 7)
            for _ in range(args.bootstrap):
                idx = r2.integers(0, n, size=n)
                tirages.append(d[idx].mean())
            bas, haut = np.percentile(tirages, [2.5, 97.5])
            t = d.mean() / (d.std(ddof=1) / np.sqrt(n))
            print(f"   {b} moins {a} : {d.mean() * 100:+.2f} pt "
                  f"[{bas * 100:+.2f} ; {haut * 100:+.2f}]  t = {t:.2f}")
            lignes_acc.append([lib, int(msk.sum()), a, b,
                               f"{accs[(lib, a)].mean() * 100:.4f}",
                               f"{accs[(lib, b)].mean() * 100:.4f}",
                               f"{d.mean() * 100:.4f}", f"{bas * 100:.4f}",
                               f"{haut * 100:.4f}", f"{t:.4f}"])
    # consistance test retest sur les quatre jeux, controle du denominateur
    lignes_ret = [["jeu_items", "n_items", "test_retest_pct"]]
    print("\nconsistance test retest humaine (controle du denominateur)")
    for lib, msk in JEUX:
        v = accs[(lib, "humains vague 2")].mean() * 100
        print(f"   {lib:<32}{v:8.4f} %")
        lignes_ret.append([lib, int(msk.sum()), f"{v:.4f}"])

    # ---- ratios inter et intra sur les memes jeux -------------------------
    print("\n" + "=" * 92)
    print("RATIOS INTER ET INTRA, MEME MACHINERIE QUE a1, SUR LES DEUX JEUX D'ITEMS")
    print("=" * 92)
    est_ordinal = np.array([ordinal.get(q, False) for q in entetes])
    k_par_item = np.array([len(options[q]) for q in entetes])
    k_max = int(k_par_item.max())
    g_max = int(max(len(niveaux[a]) for a in AXES))
    valeurs_ordinales = np.zeros((n_items, k_max))
    for j, q in enumerate(entetes):
        if est_ordinal[j] and k_par_item[j] > 1:
            valeurs_ordinales[j, :k_par_item[j]] = np.arange(k_par_item[j]) / (k_par_item[j] - 1)
    n_axes = len(AXES)
    index, poubelle = {}, None
    for c in noms:
        index[c], poubelle = A1.construire_index(donnees[c], seg, k_max, g_max, n_items)
    toutes = np.arange(n)

    def mesurer(cond, lignes):
        cnt = A1.compter(index[cond], lignes, poubelle, n_items, g_max, k_max, n_axes)
        return A1.decomposer(cnt, valeurs_ordinales)

    lignes_ratios = [["jeu_items", "n_items", "condition", "mesure",
                      "ratio_inter", "inter_bas", "inter_haut",
                      "ratio_intra", "intra_bas", "intra_haut"]]
    for lib, msk in [("169 items (a1)", m169), ("149 items (a2, a7, a8, a12)", m149)]:
        dec = {c: mesurer(c, toutes) for c in noms}
        observe = {c: A1.agreger(dec[c], msk, est_ordinal) for c in noms}
        # correction residuelle par permutation, identique a a1
        nul = {}
        for c in noms:
            vals = {m: [] for m in MESURES}
            for _ in range(args.permutations):
                perm = rng.permutation(n)
                ip, pb = A1.construire_index(donnees[c], {a: seg[a][perm] for a in AXES},
                                             k_max, g_max, n_items)
                d = A1.decomposer(A1.compter(ip, toutes, pb, n_items, g_max, k_max, n_axes),
                                  valeurs_ordinales)
                agg = A1.agreger(d, msk, est_ordinal)
                for m in MESURES:
                    vals[m].append(agg[m][0])
            nul[c] = {m: float(np.mean(vals[m])) for m in MESURES}
        point = {c: {m: (observe[c][m][0] - nul[c][m], observe[c][m][1]) for m in MESURES}
                 for c in noms}
        r0 = point[A1.REFERENCE]
        ratios = {c: {m: (point[c][m][0] / r0[m][0], point[c][m][1] / r0[m][1])
                      for m in MESURES} for c in noms}
        brut = {c: {m: ([], []) for m in MESURES} for c in noms}
        rb = np.random.default_rng(args.graine + 11)
        for b in range(args.bootstrap):
            lig = rb.integers(0, n, size=n)
            agg = {c: A1.agreger(mesurer(c, lig), msk, est_ordinal) for c in noms}
            for c in noms:
                for m in MESURES:
                    ri = (agg[c][m][0] - nul[c][m]) / (agg[A1.REFERENCE][m][0] - nul[A1.REFERENCE][m])
                    ra = agg[c][m][1] / agg[A1.REFERENCE][m][1]
                    brut[c][m][0].append(ri)
                    brut[c][m][1].append(ra)
            if (b + 1) % max(1, args.bootstrap // 5) == 0:
                print(f"  {lib} bootstrap {b + 1}/{args.bootstrap}", flush=True)
        print(f"\n{lib}, {int(msk.sum())} items, mesure entropie")
        print(f"{'condition':<30}{'ratio inter':>28}{'ratio intra':>28}")
        for c in noms:
            for m in MESURES:
                ib, ih = ic_percentile_translate(brut[c][m][0], ratios[c][m][0])
                ab, ah = ic_percentile_translate(brut[c][m][1], ratios[c][m][1])
                lignes_ratios.append([lib, int(msk.sum()), c, m,
                                      f"{ratios[c][m][0]:.4f}", f"{ib:.4f}", f"{ih:.4f}",
                                      f"{ratios[c][m][1]:.4f}", f"{ab:.4f}", f"{ah:.4f}"])
                if m == "entropie":
                    print(f"{c:<30}{ratios[c][m][0]:>10.3f} [{ib:6.3f} ; {ih:6.3f}]"
                          f"{ratios[c][m][1]:>10.3f} [{ab:6.3f} ; {ah:6.3f}]")

    # ---- 2. taux de recopie des items ecartes -----------------------------
    print("\n" + "=" * 92)
    print("2. TAUX DE RECOPIE DES ITEMS ECARTES, PAR CONDITION")
    print("=" * 92)
    # union des items ecartes par a1 (169) et par le jeu de a2 (149) : 29 items
    ecartes = [j for j in range(n_items) if (not m149[j]) or (not m169[j])]
    lignes_rec = [["item", "ecarte_par_a1", "ecarte_par_stanford", "modalite_majoritaire_pct"]
                  + [c for c in noms if c != "humains vague 1"]]
    print(f"{'item':<14}{'majo':>8}" + "".join(f"{c[:12]:>14}" for c in noms if c != "humains vague 1"))
    for j in ecartes:
        q = entetes[j]
        col = ref[:, j]
        valides = col[col >= 0]
        majo = np.bincount(valides).max() / len(valides) if len(valides) else float("nan")
        vals = []
        for c in noms:
            if c == "humains vague 1":
                continue
            ok = (donnees[c][:, j] == col) & (col >= 0)
            vals.append(ok.sum() / max(1, (col >= 0).sum()))
        lignes_rec.append([q, q in A1.ITEMS_DEMOGRAPHIQUES,
                           q.lower() in EXCLUS_STANFORD, f"{majo:.4f}"]
                          + [f"{v:.4f}" for v in vals])
        print(f"{q:<14}{majo:>8.3f}" + "".join(f"{v:>14.3f}" for v in vals))

    # ---- 3. income --------------------------------------------------------
    print("\n" + "=" * 92)
    print("3. INCOME")
    print("=" * 92)
    j_inc = entetes.index("income")
    print(f"income est dans les 169 items de a1 : {bool(m169[j_inc])}")
    print(f"income est dans les 149 items de a2 : {bool(m149[j_inc])}")
    dem = {r["email"]: r for r in csv.DictReader(open(DEMOG, encoding="utf-8"))}
    attributs = [c for c in next(csv.DictReader(open(DEMOG, encoding="utf-8"))).keys()
                 if c != "email"]
    print(f"attributs de demographic_summary.csv : {', '.join(attributs)}")
    print(f"`income` figure parmi les attributs donnes a B1 : {'income' in attributs}")
    import pandas as pd
    w1 = pd.read_csv(os.path.join(PREP, "p_wave1_summary.csv"))
    item_inc = [str(v).strip().lower() for v in w1["income"]]
    attr_inc = [str(dem[e]["income"]).strip().lower() for e in w1["email"]]
    accord = np.mean([a == b for a, b in zip(item_inc, attr_inc)])
    print(f"accord exact item income contre attribut income : {accord:.4f}")
    ren = np.mean([b not in ("", "nan", "none") for b in attr_inc])
    print(f"attribut income renseigne : {ren * 100:.1f} %")

    # ---- ecritures --------------------------------------------------------
    def ecrire(nom, lignes):
        with open(os.path.join(SORTIE, nom), "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(lignes)
        print(f"ecrit : resultats/{nom}")

    ecrire("a19-exactitude-appariee.csv", lignes_acc)
    ecrire("a19-test-retest-par-jeu.csv", lignes_ret)
    ecrire("a19-ratios-par-jeu-items.csv", lignes_ratios)
    ecrire("a19-recopie-items-ecartes.csv", lignes_rec)


if __name__ == "__main__":
    main()
