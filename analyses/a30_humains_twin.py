"""
a30_humains_twin : la variete interne des camps chez les vrais humains de Twin-2K-500.

Volet 1 de a30, cote Twin. 2 058 personnes, 609 items categoriels des vagues 1 a 3
(hors demographies), et les 108 items reposes en vague 4 comme controle de retest.
Aucun appel de modele de langage.

MEME FAMILLE D'HYPOTHESES QUE a30_humains_gss, transposee.
H1 : dispersion interne droite / gauche > 1 sur les 609 items, blocs d'ideologie.
H2 : ce rapport depasse 1 dans chacun des six blocs du catalogue.
H3 : ce rapport depasse 1 item par item, 609 tests.
H4 : il survit a l'ancrage partisan, a l'egalisation des effectifs, et a l'appariement
     demographique exact.
H5 : la vague 4, les memes personnes plus tard, donne le meme rapport sur ses 108 items.
H6 : le centre n'est pas le camp le plus varie.

Correction pour tests multiples : Holm dans chaque famille de tests, plus Benjamini
Hochberg sur la famille des 609 items.

SORTIES
-------
  resultats/a30-twin-par-camp.csv, a30-twin-par-item.csv, a30-twin-par-bloc.csv,
  resultats/a30-twin-global.csv, a30-twin-appariement.csv

Usage : .venv/bin/python analyses/a30_humains_twin.py
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a30_commun as C  # noqa: E402
import a9_commun as T  # noqa: E402


def charger_twin():
    items = T.table_items()
    w13 = T.charger_humains("1_3")
    w4 = T.charger_humains("4")
    cols = [c for c in items.index
            if c in w13.columns and items.at[c, "domaine"] != "demographies"]
    camps = C.camps_twin(w13)
    cellules = C.cellules_twin(w13)
    return items, w13, w4, cols, camps, cellules


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=C.N_BOOT)
    ap.add_argument("--perm", type=int, default=C.N_PERM)
    ap.add_argument("--perm-item", type=int, default=10000, dest="perm_item")
    ap.add_argument("--rare", type=int, default=200)
    ap.add_argument("--appar", type=int, default=200)
    args = ap.parse_args()
    rng = np.random.default_rng(C.GRAINE)

    items, w13, w4, cols, camps, cellules = charger_twin()
    codes, ks = C.coder_numerique(w13, cols)
    ind = C.Indicatrice(codes, ks)
    J = len(cols)
    print(f"{len(w13)} personnes, {J} items categoriels hors demographies, "
          f"K max {ind.k}", flush=True)

    mg = camps["bloc3"] == "gauche"
    mc = camps["bloc3"] == "centre"
    md = camps["bloc3"] == "droite"
    print(f"bloc3 : gauche {mg.sum()}, centre {mc.sum()}, droite {md.sum()}", flush=True)
    tous = np.ones(J, dtype=bool)
    dom = np.array([items.at[c, "domaine"] for c in cols], dtype=object)

    # ---------------------------------------------------------------- par camp
    lignes = []
    for part, et in [("bloc3", ["gauche", "centre", "droite"]),
                     ("points5", list(C.TWIN_POINTS5.values())),
                     ("parti3", ["gauche", "centre", "droite"])]:
        for e in et:
            m = camps[part] == e
            if m.sum() < 10:
                continue
            mm = C.mesures(ind.tables(C.poids_plein(m)))
            garde = tous & (mm["n"][0] >= C.N_MIN_ITEM)
            lignes.append({"partition": part, "camp": e, "n_personnes": int(m.sum()),
                           "n_items": int(garde.sum()),
                           "gini_simpson": float(C.agreger(mm["gs"], garde)[0]),
                           "entropie": float(C.agreger(mm["h"], garde)[0])})
    C.ecrire(pd.DataFrame(lignes), "a30-twin-par-camp.csv")

    # ---------------------------------------------------------------- par item
    tg = C.mesures(ind.tables(C.poids_plein(mg)))
    td = C.mesures(ind.tables(C.poids_plein(md)))
    tc = C.mesures(ind.tables(C.poids_plein(mc)))
    garde_item = tous & (tg["n"][0] >= C.N_MIN_ITEM) & (td["n"][0] >= C.N_MIN_ITEM)

    with np.errstate(divide="ignore", invalid="ignore"):
        ratio_obs = td["gs"][0] / tg["gs"][0]
        wa = C.poids_bootstrap(md, args.boot, rng)
        wb = C.poids_bootstrap(mg, args.boot, rng)
        boot = C.mesures(ind.tables(wa))["gs"] / C.mesures(ind.tables(wb))["gs"]
    p_item = C.p_permutation_par_item(ind, md, mg, ratio_obs, args.perm_item, rng)
    p_item = np.where(garde_item, p_item, np.nan)
    ok = np.isfinite(p_item)
    p_holm = np.full(J, np.nan)
    p_bh = np.full(J, np.nan)
    p_holm[ok] = C.holm(p_item[ok])
    p_bh[ok] = C.benjamini_hochberg(p_item[ok])
    with np.errstate(invalid="ignore"):
        b = np.where(np.isfinite(boot), boot, np.nan)
        ic_bas, ic_haut = np.nanpercentile(b, 2.5, axis=0), np.nanpercentile(b, 97.5, axis=0)

    C.ecrire(pd.DataFrame({
        "item": cols, "domaine": dom, "bloc": [items.at[c, "bloc"] for c in cols],
        "retenu": garde_item, "n_gauche": tg["n"][0], "n_droite": td["n"][0],
        "gs_gauche": tg["gs"][0], "gs_centre": tc["gs"][0], "gs_droite": td["gs"][0],
        "ratio_droite_gauche": ratio_obs, "ic_bas": ic_bas, "ic_haut": ic_haut,
        "p_permutation": p_item, "p_holm": p_holm, "p_bh": p_bh,
    }), "a30-twin-par-item.csv")
    print(f"H3 : {int(ok.sum())} items testes, {int((p_holm[ok] < 0.05).sum())} "
          f"significatifs apres Holm, {int((p_bh[ok] < 0.05).sum())} apres BH, dont "
          f"{int(((p_bh[ok] < 0.05) & (ratio_obs[ok] > 1)).sum())} en faveur de la droite",
          flush=True)

    # ---------------------------------------------------------------- par bloc
    lignes = []
    for d in T.ORDRE_DOMAINES:
        mf = dom == d
        if mf.sum() < 3:
            continue
        gardes = C.masque_items(ind, md, mg, mf)
        r = C.contraste(ind, md, mg, gardes, rng, args.boot, args.perm, "gs")
        rh = C.contraste(ind, md, mg, gardes, rng, 0, 0, "h")
        rcg = C.contraste(ind, mc, mg, C.masque_items(ind, mc, mg, mf), rng, 0, 0, "gs")
        rcd = C.contraste(ind, mc, md, C.masque_items(ind, mc, md, mf), rng, 0, 0, "gs")
        lignes.append({"domaine": d, "n_items": r["n_items"],
                       "gs_gauche": r["valeur_b"], "gs_droite": r["valeur_a"],
                       "gs_centre": rcg["valeur_a"], "ratio_droite_gauche": r["ratio"],
                       "ic_bas": r["ic_bas"], "ic_haut": r["ic_haut"],
                       "p_permutation": r["p"], "ratio_entropie": rh["ratio"],
                       "ratio_centre_gauche": rcg["ratio"],
                       "ratio_centre_droite": rcd["ratio"]})
    df = pd.DataFrame(lignes)
    df["p_holm"] = C.holm(df["p_permutation"].values)
    C.ecrire(df, "a30-twin-par-bloc.csv")
    print(df.to_string(index=False), flush=True)

    # ---------------------------------------------------------------- global
    glob = []

    def ajoute(nom, indic, ma, mb, fam, mesure="gs", mf=None, boot=None, perm=None):
        mf = np.ones(indic.J, dtype=bool) if mf is None else mf
        gardes = C.masque_items(indic, ma, mb, mf)
        r = C.contraste(indic, ma, mb, gardes, rng,
                        args.boot if boot is None else boot,
                        args.perm if perm is None else perm, mesure)
        r.update({"test": nom, "famille_de_tests": fam, "mesure": mesure,
                  "n_a": int(ma.sum()), "n_b": int(mb.sum())})
        glob.append(r)
        print(f"{nom:52s} R = {r['ratio']:.4f} [{r['ic_bas']:.4f} ; {r['ic_haut']:.4f}] "
              f"p = {r['p']:.4f}", flush=True)

    ajoute("H1 droite / gauche, ideologie, Gini Simpson", ind, md, mg, "H1")
    ajoute("H1 bis droite / gauche, ideologie, entropie", ind, md, mg, "H1 bis", "h")
    pg, pdd, pc = (camps["parti3"] == "gauche", camps["parti3"] == "droite",
                   camps["parti3"] == "centre")
    ajoute("H4a droite / gauche, ancrage parti", ind, pdd, pg, "H4")
    ajoute("H6a centre / gauche", ind, mc, mg, "H6")
    ajoute("H6b centre / droite", ind, mc, md, "H6")
    for a, b in [("tres conservateur", "tres liberal"), ("conservateur", "liberal")]:
        ajoute(f"cinq points : {a} / {b}", ind, camps["points5"] == a,
               camps["points5"] == b, "cinq points")

    # H5 : la vague 4, memes personnes, memes 108 items reposes.
    cols4 = [c for c in cols if c in w4.columns]
    codes4, ks4 = C.coder_numerique(w4, cols4)
    ind4 = C.Indicatrice(codes4, ks4)
    j4 = np.array([c in set(cols4) for c in cols])
    ajoute("H5a vagues 1 a 3, restreint aux 108 items reposes", ind, md, mg, "H5",
           mf=j4)
    ajoute("H5b vague 4, memes 108 items (controle)", ind4, md, mg, "H5")

    dfg = pd.DataFrame(glob)
    for f in dfg["famille_de_tests"].unique():
        s = dfg["famille_de_tests"] == f
        dfg.loc[s, "p_holm"] = C.holm(dfg.loc[s, "p"].values)
    C.ecrire(dfg[["test", "famille_de_tests", "mesure", "n_a", "n_b", "n_items",
                  "valeur_a", "valeur_b", "ratio", "ic_bas", "ic_haut", "p", "p_holm"]],
             "a30-twin-global.csv")

    # ---------------------------------------------------------------- controles
    lignes = []
    gardes = C.masque_items(ind, md, mg, tous)
    taille = int(min(md.sum(), mg.sum()))
    wd = C.poids_rarefaction(md, taille, args.rare, rng)
    wg = C.poids_rarefaction(mg, taille, args.rare, rng)
    for mesure in ("gs", "h"):
        xd = C.agreger(C.mesures(ind.tables(wd))[mesure], gardes)
        xg = C.agreger(C.mesures(ind.tables(wg))[mesure], gardes)
        r = xd / xg
        lignes.append({"controle": "rarefaction a effectif egal", "mesure": mesure,
                       "taille": taille, "tirages": args.rare,
                       "valeur_droite": float(np.nanmean(xd)),
                       "valeur_gauche": float(np.nanmean(xg)),
                       "ratio": float(np.nanmean(r)),
                       "ic_bas": float(np.nanpercentile(r, 2.5)),
                       "ic_haut": float(np.nanpercentile(r, 97.5)),
                       "n_items": int(gardes.sum())})
    ad, ag, taille_app = C.poids_appariement(md, mg, cellules, args.appar, rng)
    for mesure in ("gs", "h"):
        xd = C.agreger(C.mesures(ind.tables(ad))[mesure], gardes)
        xg = C.agreger(C.mesures(ind.tables(ag))[mesure], gardes)
        r = xd / xg
        lignes.append({"controle": "appariement genre x ethnicite x age x education",
                       "mesure": mesure, "taille": taille_app, "tirages": args.appar,
                       "valeur_droite": float(np.nanmean(xd)),
                       "valeur_gauche": float(np.nanmean(xg)),
                       "ratio": float(np.nanmean(r)),
                       "ic_bas": float(np.nanpercentile(r, 2.5)),
                       "ic_haut": float(np.nanpercentile(r, 97.5)),
                       "n_items": int(gardes.sum())})
    dfa = pd.DataFrame(lignes)
    C.ecrire(dfa, "a30-twin-appariement.csv")
    print(dfa.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
