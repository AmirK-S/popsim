"""
a30_humains_gss : la variete interne des camps chez les vrais humains du GSS.

Volet 1 de a30, cote GSS. 1 052 personnes, 149 items, vague 1 comme mesure et vague 2
comme controle. Aucun appel de modele de langage.

FAMILLE D'HYPOTHESES, ECRITE AVANT DE REGARDER LE MOINDRE RESULTAT
------------------------------------------------------------------
H1 (principale, un test)  : sur les trois blocs d'ideologie, la dispersion interne
    agregee du camp de droite depasse celle du camp de gauche, rapport R > 1.
H2 (neuf tests)           : ce rapport depasse 1 dans chacune des neuf familles de sujets.
H3 (149 tests)            : ce rapport depasse 1 item par item.
H4 (trois tests)          : le rapport survit au changement d'ancrage (parti au lieu
    d'ideologie), a l'egalisation des tailles de camp (rarefaction) et a l'egalisation
    de la composition demographique (appariement exact par cellule).
H5 (un test)              : la vague 2, les memes personnes deux semaines plus tard,
    donne le meme rapport.
H6 (deux tests)           : le centre n'est pas le camp le plus varie, c'est a dire que
    le rapport centre sur gauche et le rapport centre sur droite sont inferieurs a 1.

Correction pour tests multiples : Holm a l'interieur de chaque famille de tests, prise
separement, plus Benjamini Hochberg en second sur la famille de 149 items. La famille
H1 ne contient qu'un test et n'est pas corrigee.

SORTIES
-------
  resultats/a30-gss-classement-items.csv   le classement des 149 items en familles
  resultats/a30-gss-par-item.csv           dispersion et rapport droite / gauche par item
  resultats/a30-gss-par-famille.csv        idem par famille de sujets
  resultats/a30-gss-global.csv             les contrastes globaux et les controles
  resultats/a30-gss-par-camp.csv           dispersion de chaque camp, toutes partitions
  resultats/a30-gss-appariement.csv        le controle de composition demographique

Usage : .venv/bin/python analyses/a30_humains_gss.py [--boot 1000] [--perm 2000]
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a30_commun as C  # noqa: E402
from a2_baselines_gss import charger  # noqa: E402
from a25_commun import options_par_item  # noqa: E402


def charger_gss():
    ids, items, y1, y2, x, attributs = charger()
    options = options_par_item(C.RACINE)
    codes1, ks = C.coder_gss(y1, items, options)
    codes2, _ = C.coder_gss(y2, items, options)
    camps = C.camps_gss(x, attributs)
    cellules = C.cellules_gss(x, attributs)
    return ids, items, codes1, codes2, ks, camps, cellules, x, attributs


def table_par_camp(ind, camps, partition, items_tous, etiquettes):
    """Dispersion agregee sur tous les items, camp par camp."""
    lignes = []
    for e in etiquettes:
        m = camps[partition] == e
        if m.sum() < 10:
            continue
        t = ind.tables(C.poids_plein(m))
        mm = C.mesures(t)
        garde = items_tous & (mm["n"][0] >= C.N_MIN_ITEM)
        lignes.append({
            "partition": partition, "camp": e, "n_personnes": int(m.sum()),
            "n_items": int(garde.sum()),
            "gini_simpson": float(C.agreger(mm["gs"], garde)[0]),
            "entropie": float(C.agreger(mm["h"], garde)[0]),
        })
    return lignes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=C.N_BOOT)
    ap.add_argument("--perm", type=int, default=C.N_PERM)
    ap.add_argument("--perm-item", type=int, default=10000,
                    dest="perm_item", help="permutations pour les 149 tests par item ; "
                         "il en faut au moins 3 000 pour qu'un p corrige par Holm "
                         "sur 149 tests puisse descendre sous 0,05")
    ap.add_argument("--rare", type=int, default=200, help="tirages de rarefaction")
    ap.add_argument("--appar", type=int, default=200, help="tirages d'appariement")
    args = ap.parse_args()
    rng = np.random.default_rng(C.GRAINE)

    ids, items, codes1, codes2, ks, camps, cellules, x, attributs = charger_gss()
    J = len(items)
    ind1 = C.Indicatrice(codes1, ks)
    ind2 = C.Indicatrice(codes2, ks)
    print(f"{len(ids)} personnes, {J} items", flush=True)

    fam = C.familles_gss(items)
    familles = sorted(set(fam.values()))
    C.ecrire(pd.DataFrame({"item": items, "famille": [fam[i] for i in items],
                           "n_modalites": ks}), "a30-gss-classement-items.csv")
    print({f: sum(1 for i in items if fam[i] == f) for f in familles}, flush=True)

    tous = np.ones(J, dtype=bool)
    mg = camps["bloc3"] == "gauche"
    mc = camps["bloc3"] == "centre"
    md = camps["bloc3"] == "droite"
    print(f"bloc3 : gauche {mg.sum()}, centre {mc.sum()}, droite {md.sum()}", flush=True)

    # ---------------------------------------------------------------- par camp
    lignes = []
    for part, et in [("bloc3", ["gauche", "centre", "droite"]),
                     ("points7", C.GSS_POINTS7),
                     ("parti3", ["gauche", "centre", "droite"])]:
        lignes += table_par_camp(ind1, camps, part, tous, et)
    C.ecrire(pd.DataFrame(lignes), "a30-gss-par-camp.csv")

    # ---------------------------------------------------------------- par item
    # H3 : 149 tests. Le rapport par item est le rapport de deux dispersions estimees
    # sur des effectifs differents ; l'estimateur de Gini Simpson etant sans biais, la
    # difference de taille des camps ne le fausse pas, seule sa variance en depend.
    tg = C.mesures(ind1.tables(C.poids_plein(mg)))
    td = C.mesures(ind1.tables(C.poids_plein(md)))
    tc = C.mesures(ind1.tables(C.poids_plein(mc)))
    garde_item = tous & (tg["n"][0] >= C.N_MIN_ITEM) & (td["n"][0] >= C.N_MIN_ITEM)

    with np.errstate(divide="ignore", invalid="ignore"):
        ratio_obs = td["gs"][0] / tg["gs"][0]
        wa = C.poids_bootstrap(md, args.boot, rng)
        wb = C.poids_bootstrap(mg, args.boot, rng)
        boot = C.mesures(ind1.tables(wa))["gs"] / C.mesures(ind1.tables(wb))["gs"]
    p_item = C.p_permutation_par_item(ind1, md, mg, ratio_obs, args.perm_item, rng)
    p_item = np.where(garde_item, p_item, np.nan)

    ok = np.isfinite(p_item)
    p_holm = np.full(J, np.nan)
    p_bh = np.full(J, np.nan)
    p_holm[ok] = C.holm(p_item[ok])
    p_bh[ok] = C.benjamini_hochberg(p_item[ok])

    with np.errstate(invalid="ignore"):
        ic_bas = np.nanpercentile(np.where(np.isfinite(boot), boot, np.nan), 2.5, axis=0)
        ic_haut = np.nanpercentile(np.where(np.isfinite(boot), boot, np.nan), 97.5, axis=0)

    C.ecrire(pd.DataFrame({
        "item": items, "famille": [fam[i] for i in items],
        "retenu": garde_item,
        "n_gauche": tg["n"][0], "n_centre": tc["n"][0], "n_droite": td["n"][0],
        "gs_gauche": tg["gs"][0], "gs_centre": tc["gs"][0], "gs_droite": td["gs"][0],
        "h_gauche": tg["h"][0], "h_centre": tc["h"][0], "h_droite": td["h"][0],
        "ratio_droite_gauche": ratio_obs,
        "ic_bas": ic_bas, "ic_haut": ic_haut,
        "p_permutation": p_item, "p_holm": p_holm, "p_bh": p_bh,
    }), "a30-gss-par-item.csv")

    n_test = int(ok.sum())
    print(f"H3 : {n_test} items testes, {int((p_holm[ok] < 0.05).sum())} significatifs "
          f"apres Holm, {int((p_bh[ok] < 0.05).sum())} apres Benjamini Hochberg, "
          f"dont {int(((p_bh[ok] < 0.05) & (ratio_obs[ok] > 1)).sum())} en faveur de la "
          f"droite", flush=True)

    # ---------------------------------------------------------------- par famille
    lignes = []
    for f in familles:
        mf = np.array([fam[i] == f for i in items])
        gardes = C.masque_items(ind1, md, mg, mf)
        if gardes.sum() < 3:
            continue
        r = C.contraste(ind1, md, mg, gardes, rng, args.boot, args.perm, "gs")
        rh = C.contraste(ind1, md, mg, gardes, rng, 0, 0, "h")
        rc_g = C.contraste(ind1, mc, mg, C.masque_items(ind1, mc, mg, mf), rng, 0, 0, "gs")
        rc_d = C.contraste(ind1, mc, md, C.masque_items(ind1, mc, md, mf), rng, 0, 0, "gs")
        lignes.append({
            "famille": f, "n_items": r["n_items"],
            "gs_gauche": r["valeur_b"], "gs_droite": r["valeur_a"],
            "gs_centre": rc_g["valeur_a"],
            "ratio_droite_gauche": r["ratio"], "ic_bas": r["ic_bas"],
            "ic_haut": r["ic_haut"], "p_permutation": r["p"],
            "ratio_entropie": rh["ratio"],
            "ratio_centre_gauche": rc_g["ratio"], "ratio_centre_droite": rc_d["ratio"],
        })
    df_fam = pd.DataFrame(lignes)
    df_fam["p_holm"] = C.holm(df_fam["p_permutation"].values)
    C.ecrire(df_fam, "a30-gss-par-famille.csv")

    # ---------------------------------------------------------------- global et controles
    glob = []

    def ajoute(nom, ind, ma, mb, famille_test, mesure="gs", items_famille=None,
               boot=None, perm=None):
        mf = tous if items_famille is None else items_famille
        gardes = C.masque_items(ind, ma, mb, mf)
        r = C.contraste(ind, ma, mb, gardes, rng,
                        args.boot if boot is None else boot,
                        args.perm if perm is None else perm, mesure)
        r.update({"test": nom, "famille_de_tests": famille_test, "mesure": mesure,
                  "n_a": int(ma.sum()), "n_b": int(mb.sum())})
        glob.append(r)
        print(f"{nom:52s} R = {r['ratio']:.4f} [{r['ic_bas']:.4f} ; {r['ic_haut']:.4f}] "
              f"p = {r['p']:.4f}", flush=True)
        return r

    # H1
    ajoute("H1 droite / gauche, ideologie, Gini Simpson", ind1, md, mg, "H1")
    ajoute("H1 bis droite / gauche, ideologie, entropie", ind1, md, mg, "H1 bis", "h")

    # H4 : trois controles
    pg = camps["parti3"] == "gauche"
    pd_ = camps["parti3"] == "droite"
    pc = camps["parti3"] == "centre"
    ajoute("H4a droite / gauche, ancrage parti", ind1, pd_, pg, "H4")

    # H5 : vague 2
    ajoute("H5 droite / gauche, vague 2 (controle)", ind2, md, mg, "H5")

    # H6 : le centre
    ajoute("H6a centre / gauche", ind1, mc, mg, "H6")
    ajoute("H6b centre / droite", ind1, mc, md, "H6")
    ajoute("H6c centre / gauche, ancrage parti", ind1, pc, pg, "H6 bis")
    ajoute("H6d centre / droite, ancrage parti", ind1, pc, pd_, "H6 bis")

    # Sept points : extremes contre moderes, moins exposes a l'erreur de classement
    for a, b in [("extremely conservative", "extremely liberal"),
                 ("conservative", "liberal"),
                 ("slightly conservative", "slightly liberal")]:
        ma = camps["points7"] == a
        mb = camps["points7"] == b
        ajoute(f"sept points : {a} / {b}", ind1, ma, mb, "sept points")

    df_glob = pd.DataFrame(glob)
    for f in df_glob["famille_de_tests"].unique():
        s = df_glob["famille_de_tests"] == f
        df_glob.loc[s, "p_holm"] = C.holm(df_glob.loc[s, "p"].values)
    C.ecrire(df_glob[["test", "famille_de_tests", "mesure", "n_a", "n_b", "n_items",
                      "valeur_a", "valeur_b", "ratio", "ic_bas", "ic_haut", "p",
                      "p_holm"]], "a30-gss-global.csv")

    # ---------------------------------------------------------------- rarefaction
    # H4b : egaliser la taille des deux camps. L'estimateur de Gini Simpson est sans
    # biais, celui de Miller Madow ne l'est qu'au premier ordre ; ce controle dit si le
    # rapport en entropie doit quelque chose a la difference d'effectif.
    lignes = []
    taille = int(min(md.sum(), mg.sum()))
    gardes = C.masque_items(ind1, md, mg, tous)
    wd = C.poids_rarefaction(md, taille, args.rare, rng)
    wg = C.poids_rarefaction(mg, taille, args.rare, rng)
    for mesure in ("gs", "h"):
        xd = C.agreger(C.mesures(ind1.tables(wd))[mesure], gardes)
        xg = C.agreger(C.mesures(ind1.tables(wg))[mesure], gardes)
        r = xd / xg
        lignes.append({"controle": "rarefaction a effectif egal", "mesure": mesure,
                       "taille": taille, "tirages": args.rare,
                       "valeur_droite": float(np.nanmean(xd)),
                       "valeur_gauche": float(np.nanmean(xg)),
                       "ratio": float(np.nanmean(r)),
                       "ic_bas": float(np.nanpercentile(r, 2.5)),
                       "ic_haut": float(np.nanpercentile(r, 97.5)), "n_items": int(gardes.sum())})

    # ---------------------------------------------------------------- appariement
    # H4c : meme composition demographique exacte des deux cotes. Le sous echantillon
    # apparie est plus petit : l'intervalle qui l'accompagne melange l'incertitude de
    # tirage et la perte d'effectif, et il doit etre lu comme tel.
    ad, ag, taille_app = C.poids_appariement(md, mg, cellules, args.appar, rng)
    for mesure in ("gs", "h"):
        xd = C.agreger(C.mesures(ind1.tables(ad))[mesure], gardes)
        xg = C.agreger(C.mesures(ind1.tables(ag))[mesure], gardes)
        r = xd / xg
        lignes.append({"controle": "appariement genre x race x age x education",
                       "mesure": mesure, "taille": taille_app, "tirages": args.appar,
                       "valeur_droite": float(np.nanmean(xd)),
                       "valeur_gauche": float(np.nanmean(xg)),
                       "ratio": float(np.nanmean(r)),
                       "ic_bas": float(np.nanpercentile(r, 2.5)),
                       "ic_haut": float(np.nanpercentile(r, 97.5)),
                       "n_items": int(gardes.sum())})
    df_app = pd.DataFrame(lignes)
    C.ecrire(df_app, "a30-gss-appariement.csv")
    print(df_app.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
