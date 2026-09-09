"""
a43_r2_demoyenne : le R2 demoyenne de Ahn, avec et sans retrait de la moyenne de segment,
le test d'Ahn par personne, et la decomposition personne x item.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Preenregistrement :
resultats/a43-preenregistrement.md, ecrit avant tout calcul.

Entree  : paquet OSF t6g7k, cache de matrices de a25, cache de la foret de a28, cache des
          imputations de a35. Aucun de ces caches n'est reecrit.
Sortie  : resultats/a43-items-ordinaux.csv, a43-segments.csv, a43-r2-demoyenne.csv,
          a43-test-ahn.csv, a43-decomposition.csv, a43-contrastes.csv.

Usage :
  .venv/bin/python analyses/a43_r2_demoyenne.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a43_commun as C


def ligne_r2(perimetre, condition, variante, sommes, n_cellules, idx_boot):
    r = C.r_poole(sommes)
    tir = C.bootstrap_r(sommes, idx_boot)
    r_bas, r_haut = C.ic(tir)
    r2 = tir ** 2
    r2_bas, r2_haut = C.ic(r2)
    return {
        "perimetre": perimetre, "condition": condition,
        "famille_condition": C.FAMILLE.get(condition, ""),
        "variante": variante,
        "r": r, "r_ic_bas": r_bas, "r_ic_haut": r_haut,
        "r2": r * r if not np.isnan(r) else np.nan,
        "r2_ic_bas": r2_bas, "r2_ic_haut": r2_haut,
        "p_bilateral": C.p_bilateral(tir),
        "n_cellules": n_cellules,
    }, tir


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--bootstrap", type=int, default=C.BOOTSTRAP)
    args = ap.parse_args()

    paquet = C.charger(args.cache, args.cache_foret, args.cache_a35)
    print("methodes de a35 relues du cache :", paquet["a35_presentes"], flush=True)

    ords, colonnes, rangs, H = C.preparer_valeurs(paquet)
    print(f"items ordinaux retenus : {len(ords)}", flush=True)
    H2 = C.scores_methode(paquet, "humains vague 2", colonnes, rangs)

    C.ecrire(pd.DataFrame({"item": ords, "colonne": colonnes,
                           "n_modalites": [len(paquet["options"][it]) for it in ords]}),
             "a43-items-ordinaux.csv")

    # --- segmentations
    seg18, niv18 = C.segments_ideologie_genre_age(paquet, age_regroupe=True)
    seg42, niv42 = C.segments_ideologie_genre_age(paquet, age_regroupe=False)
    lignes150 = np.asarray(paquet["lignes150"], dtype=int)
    det = []
    for nom, seg, niv in (("primaire 18", seg18, niv18), ("secondaire 42", seg42, niv42)):
        for g, lib in enumerate(niv):
            n_tot = int((seg == g).sum())
            n_150 = int((seg[lignes150] == g).sum())
            det.append({"segmentation": nom, "segment": lib,
                        "n_1052": n_tot, "n_150": n_150})
        det.append({"segmentation": nom, "segment": "SANS SEGMENT",
                    "n_1052": int((seg < 0).sum()),
                    "n_150": int((seg[lignes150] < 0).sum())})
    C.ecrire(pd.DataFrame(det), "a43-segments.csv")

    # --- moyennes leave-one-out, estimees sur les 1 052 dans tous les cas
    MOY_ITEM = C.moyennes_loo(H, None, 0)
    MOY_S18 = C.moyennes_loo(H, seg18, len(niv18))
    MOY_S42 = C.moyennes_loo(H, seg42, len(niv42))
    VARIANTES = [("moyenne d'item", MOY_ITEM),
                 ("moyenne d'item et de segment 18", MOY_S18),
                 ("moyenne d'item et de segment 42", MOY_S42)]

    per = C.perimetres(paquet)
    idx_boot = {k: C.tirages_bootstrap(len(v), args.bootstrap)
                for k, v in per.items()}

    lignes_r2, tirages_r2 = [], {}
    lignes_ahn, tirages_ahn = [], {}
    lignes_dec = []

    for nom_per, lignes in per.items():
        conditions = C.methodes_du_perimetre(paquet, nom_per)
        ib = idx_boot[nom_per]
        # les deux moyennes leave-one-out comme predicteurs a part entiere
        predicteurs = {c: C.scores_methode(paquet, c, colonnes, rangs) for c in conditions}
        predicteurs["moyenne d'item LOO"] = MOY_ITEM
        predicteurs["moyenne de segment LOO"] = MOY_S18

        # --- M1 et M2
        for cond in conditions:
            P = predicteurs[cond]
            for nom_var, MOY in VARIANTES:
                s, n_cell = C.preparer_r2(H, P, MOY, lignes)
                lg, tir = ligne_r2(nom_per, cond, nom_var, s, n_cell, ib)
                lignes_r2.append(lg)
                tirages_r2[(nom_per, cond, nom_var)] = tir
            print(f"  R2 {nom_per} {cond}", flush=True)

        # --- M3
        r_item = C.r_par_personne(H, MOY_ITEM, lignes)
        r_seg = C.r_par_personne(H, MOY_S18, lignes)
        for cond in conditions:
            r_m = C.r_par_personne(H, predicteurs[cond], lignes)
            tir = C.bootstrap_z(r_m, ib)
            bas, haut = C.ic(tir)
            d1 = C.bootstrap_diff_z(r_m, r_item, ib)
            d2 = C.bootstrap_diff_z(r_m, r_seg, ib)
            dz1, n1 = C.d_de_cohen_apparie(r_m, r_item)
            dz2, n2 = C.d_de_cohen_apparie(r_m, r_seg)
            lignes_ahn.append({
                "perimetre": nom_per, "condition": cond,
                "famille_condition": C.FAMILLE.get(cond, ""),
                "r_moyen_fisher": C.z_moyen(r_m),
                "r_moyen_brut": float(np.nanmean(r_m)),
                "ic_bas": bas, "ic_haut": haut,
                "n_personnes": int((~np.isnan(r_m)).sum()),
                "diff_moyenne_item": float(np.nanmean(d1)),
                "diff_item_ic_bas": C.ic(d1)[0], "diff_item_ic_haut": C.ic(d1)[1],
                "dz_item": dz1,
                "diff_moyenne_segment": float(np.nanmean(d2)),
                "diff_segment_ic_bas": C.ic(d2)[0], "diff_segment_ic_haut": C.ic(d2)[1],
                "dz_segment": dz2,
            })
            tirages_ahn[(nom_per, cond, "item")] = d1
            tirages_ahn[(nom_per, cond, "segment")] = d2
        for nom, rr in (("moyenne d'item LOO", r_item), ("moyenne de segment LOO", r_seg)):
            tir = C.bootstrap_z(rr, ib)
            bas, haut = C.ic(tir)
            lignes_ahn.append({
                "perimetre": nom_per, "condition": nom, "famille_condition": "reference",
                "r_moyen_fisher": C.z_moyen(rr), "r_moyen_brut": float(np.nanmean(rr)),
                "ic_bas": bas, "ic_haut": haut,
                "n_personnes": int((~np.isnan(rr)).sum()),
                "diff_moyenne_item": np.nan, "diff_item_ic_bas": np.nan,
                "diff_item_ic_haut": np.nan, "dz_item": np.nan,
                "diff_moyenne_segment": np.nan, "diff_segment_ic_bas": np.nan,
                "diff_segment_ic_haut": np.nan, "dz_segment": np.nan,
            })

        # --- M4
        for cond in conditions + ["moyenne d'item LOO"]:
            P = predicteurs[cond]
            d = C.decomposition(P[lignes])
            d.update({"perimetre": nom_per, "condition": cond,
                      "famille_condition": C.FAMILLE.get(cond, ""),
                      "support": "une occasion"})
            lignes_dec.append(d)
        d = C.decomposition(H[lignes], H2[lignes])
        d.update({"perimetre": nom_per, "condition": "humains, deux vagues",
                  "famille_condition": "plancher", "support": "deux occasions"})
        lignes_dec.append(d)
        d = C.decomposition(H[lignes])
        d.update({"perimetre": nom_per, "condition": "humains vague 1",
                  "famille_condition": "plancher", "support": "une occasion"})
        lignes_dec.append(d)

    df_r2 = pd.DataFrame(lignes_r2)
    df_ahn = pd.DataFrame(lignes_ahn)
    df_dec = pd.DataFrame(lignes_dec)

    # --- corrections pour tests multiples, trois familles
    contrastes = []
    f1 = df_r2[df_r2["variante"] == "moyenne d'item et de segment 18"].copy()
    p = f1["p_bilateral"].values
    f1["p_holm"] = C.holm(p)
    f1["p_bh"] = C.benjamini_hochberg(p)
    for _, r in f1.iterrows():
        contrastes.append({"famille": "F1 correlation apres retrait du segment differe de zero",
                           "perimetre": r["perimetre"], "condition": r["condition"],
                           "statistique": r["r"], "ic_bas": r["r_ic_bas"],
                           "ic_haut": r["r_ic_haut"], "p": r["p_bilateral"],
                           "p_holm": r["p_holm"], "p_bh": r["p_bh"]})

    for cle, nom_famille, col_d, col_b, col_h in (
            ("item", "F2 bat la moyenne d'item leave-one-out", "diff_moyenne_item",
             "diff_item_ic_bas", "diff_item_ic_haut"),
            ("segment", "F3 bat la moyenne de segment leave-one-out",
             "diff_moyenne_segment", "diff_segment_ic_bas", "diff_segment_ic_haut")):
        sous = df_ahn[df_ahn["famille_condition"] != "reference"]
        ps = np.array([C.p_bilateral(tirages_ahn[(r["perimetre"], r["condition"], cle)])
                       for _, r in sous.iterrows()])
        ph, pb = C.holm(ps), C.benjamini_hochberg(ps)
        for k, (_, r) in enumerate(sous.iterrows()):
            contrastes.append({"famille": nom_famille, "perimetre": r["perimetre"],
                               "condition": r["condition"], "statistique": r[col_d],
                               "ic_bas": r[col_b], "ic_haut": r[col_h], "p": ps[k],
                               "p_holm": ph[k], "p_bh": pb[k]})

    C.ecrire(df_r2, "a43-r2-demoyenne.csv")
    C.ecrire(df_ahn, "a43-test-ahn.csv")
    C.ecrire(df_dec, "a43-decomposition.csv")
    C.ecrire(pd.DataFrame(contrastes), "a43-contrastes.csv")
    np.save("/tmp/a43-tirages-r2.npy",
            np.array({k: v for k, v in tirages_r2.items()}, dtype=object),
            allow_pickle=True)

    # --- resume lisible
    print()
    for nom_per in ("1052", "150"):
        print(f"=== perimetre {nom_per} ===")
        sous = df_r2[df_r2["perimetre"] == nom_per]
        plaf = sous[sous["condition"] == "humains vague 2"]
        for _, r in plaf.iterrows():
            print(f"  PLAFOND {r['variante']:<34s} r2 = {r['r2']:.4f}")
        for cond in C.ORDRE_METHODES:
            b = sous[sous["condition"] == cond]
            if b.empty or cond == "humains vague 2":
                continue
            a = b[b["variante"] == "moyenne d'item"].iloc[0]
            c = b[b["variante"] == "moyenne d'item et de segment 18"].iloc[0]
            print(f"  {cond:<28s} item {a['r2']*100:6.2f} %   "
                  f"item+segment {c['r2']*100:6.2f} % "
                  f"[{c['r2_ic_bas']*100:5.2f} ; {c['r2_ic_haut']*100:5.2f}]  r = {c['r']:+.4f}")
        print()


if __name__ == "__main__":
    main()
