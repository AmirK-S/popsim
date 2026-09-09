"""
a37_agents : ce que la simulation fait du modele generatif de Brandt et Sleegers.

Volet 2 de a37. Aucun appel de modele de langage, lecture seule sur data/, quatre coeurs.
Aucun fichier existant n'est modifie.

LA QUESTION
-----------
Chez les vrais humains, le rapport de dispersion droite sur gauche d'un item est une
fonction decroissante de la derive agregee de cet item : la ou l'opinion penche a gauche
la gauche est unie, la ou elle penche a droite c'est la droite qui l'est. C'est le
mecanisme que Brandt et Sleegers obtiennent par simulation a partir de deux parametres.
Une population simulee par un modele de langage reproduit elle cette pente, l'efface t
elle, ou l'exagere t elle ?

FAMILLE D'HYPOTHESES, ECRITE AVANT DE REGARDER LE MOINDRE RESULTAT
------------------------------------------------------------------
A1, une famille de huit tests (les six conditions de Stanford, C2, C3), Holm :
    la pente de la condition differe de la pente humaine mesuree sur les memes personnes
    et les memes items.
A2, une famille de deux tests, Holm : les deux conditions qui portent l'etiquette
    ideologique dans l'invite (C2 et v8) ont une pente plus raide que la condition
    correspondante sans etiquette (C3 et v6), contraste apparie sur les memes personnes.
A3, un test : sans etiquette, la pente est indistinguable de la pente humaine.

Prediction de la these, ecrite avant : avec l'etiquette la pente est exageree et le camp
du cote du consensus devient unanime, donc le rapport diverge ; sans etiquette la pente
est proche de l'humaine.

CE QUI EST MESURE, ET SUR QUEL AXE
----------------------------------
Deux abscisses, jamais melangees.
  « derive propre »  : la derive agregee de la population simulee elle meme. C'est le
                       calcul de Brandt et Sleegers applique a la population simulee, et
                       c'est la mesure principale.
  « derive humaine » : la derive agregee des vrais humains, tenue fixe. Elle dit si la
                       simulation reproduit le classement des items des humains, meme
                       quand sa propre derive a bouge.

Deux ordonnees, pour la meme raison.
  log du rapport de dispersion : la mesure principale, mais elle est infinie des qu'un
                       camp simule devient unanime sur un item.
  difference de dispersion     : toujours finie, employee comme controle et pour compter
                       ce que le logarithme jette.

SORTIES : resultats/a37-agents-gss.csv, a37-agents-gss-150.csv, a37-agents-twin.csv,
          a37-agents-contrastes.csv, a37-agents-par-item.csv

Usage : .venv/bin/python analyses/a37_agents.py
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a30_commun as C  # noqa: E402
import a37_commun as A  # noqa: E402
import a9_commun as T  # noqa: E402
from a28_commun import charger_tout, ORDRE_METHODES  # noqa: E402
from a25_commun import options_par_item  # noqa: E402


def pente_condition(ind, mg, md, S, garde, W, x_fixe=None, m_tous=None):
    """Pente, ordonnee, R2 sur l'estimation ponctuelle, et la serie de bootstrap.

    W : (B, n) poids de bootstrap sur les personnes, partages entre toutes les conditions
    pour que les contrastes soient apparies. x_fixe, s'il est donne, remplace la derive
    propre de la condition par une abscisse imposee (la derive humaine).
    m_tous : la population sur laquelle la derive agregee est calculee. Elle doit etre
    exactement la population dont les deux camps sont tires, sinon la derive du perimetre
    a 150 personnes serait lue sur 1 052 pour les conditions qui couvrent tout le monde et
    sur 150 pour C2 et C3, et l'abscisse ne serait pas la meme d'une ligne a l'autre.
    """
    n = ind.n
    fg = np.asarray(mg, dtype=np.float32)
    fd = np.asarray(md, dtype=np.float32)
    un = (np.ones(n, dtype=np.float32) if m_tous is None
          else np.asarray(m_tous, dtype=np.float32))[None, :]

    d0, vg0, vd0, lr0 = A.ratios_et_derive(ind, un, fg[None, :], fd[None, :], S)
    x0 = d0[0] if x_fixe is None else np.asarray(x_fixe, dtype=float)
    x0 = np.where(garde, x0, np.nan)
    y0 = np.where(garde, lr0[0], np.nan)
    diff0 = np.where(garde, vd0[0] - vg0[0], np.nan)
    pente, const, r2, n_it = A.ols(x0, y0)
    rho = A.spearman(x0, y0)
    p_diff, c_diff, r2_diff, _ = A.ols(x0, diff0)

    d, vg, vd, lr = A.ratios_et_derive(ind, W * un, W * fg[None, :], W * fd[None, :], S)
    pentes = np.empty(W.shape[0])
    pentes_diff = np.empty(W.shape[0])
    for t in range(W.shape[0]):
        xt = np.where(garde, d[t], np.nan) if x_fixe is None else x0
        pentes[t], _, _, _ = A.ols(xt, np.where(garde, lr[t], np.nan))
        pentes_diff[t], _, _, _ = A.ols(xt, np.where(garde, vd[t] - vg[t], np.nan))

    n_infini = int((garde & ~np.isfinite(lr0[0])).sum())
    n_unanime_g = int((garde & (vg0[0] <= 1e-12)).sum())
    n_unanime_d = int((garde & (vd0[0] <= 1e-12)).sum())
    return {"pente": pente, "ordonnee": const, "r2": r2, "spearman": rho,
            "n_items": n_it, "n_items_offerts": int(garde.sum()),
            "n_items_perdus_log": n_infini,
            "n_items_gauche_unanime": n_unanime_g,
            "n_items_droite_unanime": n_unanime_d,
            "pente_difference": p_diff, "r2_difference": r2_diff,
            "gs_gauche": float(np.nanmean(np.where(garde, vg0[0], np.nan))),
            "gs_droite": float(np.nanmean(np.where(garde, vd0[0], np.nan))),
            "_pentes": pentes, "_pentes_diff": pentes_diff, "_x": x0, "_y": y0}


def ic(v):
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) < 10:
        return np.nan, np.nan
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


def bloc(nom, res, ref, perimetre):
    b, h = ic(res["_pentes"])
    d = res["_pentes"] - ref["_pentes"] if ref is not None else None
    lig = {"perimetre": perimetre, "condition": nom,
           "pente": res["pente"], "pente_ic_bas": b, "pente_ic_haut": h,
           "ordonnee": res["ordonnee"],
           "ratio_a_derive_nulle": float(np.exp(res["ordonnee"]))
           if np.isfinite(res["ordonnee"]) else np.nan,
           "r2": res["r2"], "spearman": res["spearman"],
           "gs_gauche": res["gs_gauche"], "gs_droite": res["gs_droite"],
           "n_items": res["n_items"], "n_items_offerts": res["n_items_offerts"],
           "n_items_perdus_log": res["n_items_perdus_log"],
           "n_items_gauche_unanime": res["n_items_gauche_unanime"],
           "n_items_droite_unanime": res["n_items_droite_unanime"],
           "pente_difference": res["pente_difference"],
           "r2_difference": res["r2_difference"]}
    if d is not None:
        lb, lh = ic(d)
        lig.update({"ecart_pente_vs_humains": float(res["pente"] - ref["pente"]),
                    "ecart_ic_bas": lb, "ecart_ic_haut": lh,
                    "p": A.p_bootstrap_bilateral(d)})
    else:
        lig.update({"ecart_pente_vs_humains": np.nan, "ecart_ic_bas": np.nan,
                    "ecart_ic_haut": np.nan, "p": np.nan})
    print(f"{perimetre:16s} {nom:34s} pente {lig['pente']:+7.3f} "
          f"[{lig['pente_ic_bas']:+7.3f} ; {lig['pente_ic_haut']:+7.3f}] "
          f"R2 {lig['r2'] if np.isfinite(lig['r2']) else float('nan'):.3f}  "
          f"items {lig['n_items']:3d}/{lig['n_items_offerts']:3d}  "
          f"gauche unanime {lig['n_items_gauche_unanime']:2d}", flush=True)
    return lig


def volet_gss(args, rng):
    paq = charger_tout(args.cache, args.cache_foret)
    ids, items, y1, M = paq["ids"], paq["items"], paq["y1"], paq["M"]
    lignes150 = paq["lignes150"]
    options = options_par_item(A.RACINE)
    camps = C.camps_gss(paq["x"], paq["attributs"])
    mg = camps["bloc3"] == "gauche"
    md = camps["bloc3"] == "droite"

    S, oriente, sens_a, niveaux, _ = A.scores_gss(items, options)
    codes_h, ks = C.coder_gss(y1, items, options)
    ind_h = C.Indicatrice(codes_h, ks)
    tg = C.mesures(ind_h.tables(C.poids_plein(mg)))
    td = C.mesures(ind_h.tables(C.poids_plein(md)))
    garde = oriente & (tg["n"][0] >= C.N_MIN_ITEM) & (td["n"][0] >= C.N_MIN_ITEM)
    tous = np.ones(len(ids), dtype=np.float32)
    un = tous[None, :]
    derive_humaine = np.where(garde, A.derive(ind_h.tables(un), S)[0], np.nan)

    inds = {"humains vague 1": ind_h}
    for nom in ORDRE_METHODES:
        if nom not in M:
            continue
        codes, _ = C.coder_gss(np.asarray(M[nom], dtype=object), items, options)
        inds[nom] = C.Indicatrice(codes, ks)

    # Un seul jeu de poids de bootstrap, partage par toutes les conditions : les ecarts
    # sont ainsi apparies personne par personne.
    W = A.poids_bootstrap_global(len(ids), args.boot, rng)

    lignes, par_item = [], []
    ref = pente_condition(ind_h, mg, md, S, garde, W, m_tous=tous)
    lignes.append(bloc("humains vague 1", ref, None, "1052 personnes"))
    for nom, ind in inds.items():
        if nom in ("C2", "C3", "humains vague 1"):
            continue
        r = pente_condition(ind, mg, md, S, garde, W, m_tous=tous)
        lig = bloc(nom, r, ref, "1052 personnes")
        rf = pente_condition(ind, mg, md, S, garde, W, x_fixe=derive_humaine,
                             m_tous=tous)
        lig["pente_sur_derive_humaine"] = rf["pente"]
        lig["r2_sur_derive_humaine"] = rf["r2"]
        lignes.append(lig)
    lignes[0]["pente_sur_derive_humaine"] = ref["pente"]
    lignes[0]["r2_sur_derive_humaine"] = ref["r2"]

    # Detail par item, pour la figure : quatre series suffisent, les autres sont dans
    # les tableaux agreges.
    for nom in ("humains vague 1", "agents v8", "agents enquete",
                "agents demographiques (v6)"):
        if nom not in inds:
            continue
        ind = inds[nom]
        d0, vg0, vd0, lr0 = A.ratios_et_derive(
            ind, un, mg.astype(np.float32)[None, :], md.astype(np.float32)[None, :], S)
        for j, it in enumerate(items):
            if not garde[j]:
                continue
            par_item.append({"perimetre": "1052 personnes", "condition": nom,
                             "item": it, "derive_propre": d0[0, j],
                             "derive_humaine": derive_humaine[j],
                             "gs_gauche": vg0[0, j], "gs_droite": vd0[0, j],
                             "log_ratio": lr0[0, j]})

    df = pd.DataFrame(lignes)
    s = df["p"].notna()
    df.loc[s, "p_holm"] = C.holm(df.loc[s, "p"].values)
    C.ecrire(df, "a37-agents-gss.csv")

    # ------------------------------------------------------- les 150 personnes
    m150 = np.zeros(len(ids), dtype=bool)
    m150[lignes150] = True
    mg150, md150 = mg & m150, md & m150
    tg1 = C.mesures(ind_h.tables(C.poids_plein(mg150)))
    td1 = C.mesures(ind_h.tables(C.poids_plein(md150)))
    garde150 = oriente & (tg1["n"][0] >= 15) & (td1["n"][0] >= 15)
    print(f"150 personnes : gauche {int(mg150.sum())}, droite {int(md150.sum())}, "
          f"{int(garde150.sum())} items orientes retenus", flush=True)
    W150 = A.poids_bootstrap_global(len(ids), args.boot, rng)
    f150 = m150.astype(np.float32)
    l2 = []
    ref150 = pente_condition(ind_h, mg150, md150, S, garde150, W150, m_tous=f150)
    l2.append(bloc("humains vague 1", ref150, None, "150 personnes"))
    for nom, ind in inds.items():
        if nom == "humains vague 1":
            continue
        r = pente_condition(ind, mg150, md150, S, garde150, W150, m_tous=f150)
        l2.append(bloc(nom, r, ref150, "150 personnes"))
    for nom in ("humains vague 1", "C2", "C3"):
        if nom not in inds:
            continue
        ind = inds[nom]
        d0, vg0, vd0, lr0 = A.ratios_et_derive(
            ind, f150[None, :], mg150.astype(np.float32)[None, :],
            md150.astype(np.float32)[None, :], S)
        dh150 = A.derive(ind_h.tables(f150[None, :]), S)[0]
        for j, it in enumerate(items):
            if not garde150[j]:
                continue
            par_item.append({"perimetre": "150 personnes", "condition": nom,
                             "item": it, "derive_propre": d0[0, j],
                             "derive_humaine": dh150[j],
                             "gs_gauche": vg0[0, j], "gs_droite": vd0[0, j],
                             "log_ratio": lr0[0, j]})
    df2 = pd.DataFrame(l2)
    s = df2["p"].notna()
    df2.loc[s, "p_holm"] = C.holm(df2.loc[s, "p"].values)
    C.ecrire(df2, "a37-agents-gss-150.csv")
    C.ecrire(pd.DataFrame(par_item), "a37-agents-par-item.csv")

    # ------------------------------------------------------- A2, l'etiquette
    couples = [("C2", "C3", mg150, md150, garde150, W150, f150, "150 personnes"),
               ("agents v8", "agents demographiques (v6)", mg150, md150, garde150,
                W150, f150, "150 personnes"),
               ("agents v8", "agents demographiques (v6)", mg, md, garde, W, tous,
                "1052 personnes")]
    lc = []
    for na, nb, ga, dr, gd, Wc, mt, per in couples:
        if na not in inds or nb not in inds:
            continue
        ra = pente_condition(inds[na], ga, dr, S, gd, Wc, m_tous=mt)
        rb = pente_condition(inds[nb], ga, dr, S, gd, Wc, m_tous=mt)
        d = ra["_pentes"] - rb["_pentes"]
        dd = ra["_pentes_diff"] - rb["_pentes_diff"]
        lb, lh = ic(d)
        db, dh = ic(dd)
        lc.append({"perimetre": per, "avec_etiquette": na, "sans_etiquette": nb,
                   "pente_avec": ra["pente"], "pente_sans": rb["pente"],
                   "ecart": float(ra["pente"] - rb["pente"]),
                   "ic_bas": lb, "ic_haut": lh,
                   "p": A.p_bootstrap_bilateral(d),
                   "pente_diff_avec": ra["pente_difference"],
                   "pente_diff_sans": rb["pente_difference"],
                   "ecart_diff": float(ra["pente_difference"] - rb["pente_difference"]),
                   "ecart_diff_ic_bas": db, "ecart_diff_ic_haut": dh,
                   "p_diff": A.p_bootstrap_bilateral(dd),
                   "items_gauche_unanime_avec": ra["n_items_gauche_unanime"],
                   "items_gauche_unanime_sans": rb["n_items_gauche_unanime"],
                   "items_perdus_log_avec": ra["n_items_perdus_log"],
                   "items_perdus_log_sans": rb["n_items_perdus_log"]})
    dfc = pd.DataFrame(lc)
    dfc["p_holm"] = C.holm(dfc["p"].fillna(1.0).values)
    dfc["p_diff_holm"] = C.holm(dfc["p_diff"].fillna(1.0).values)
    C.ecrire(dfc, "a37-agents-contrastes.csv")
    print(dfc.to_string(index=False), flush=True)
    return df, df2


def volet_twin(args, rng):
    """Les treize configurations publiees par les auteurs, sur les dix items politiques."""
    w13 = T.charger_humains("1_3")
    w4 = T.charger_humains("4")
    pid = list(w13.index)
    camps = C.camps_twin(w13)
    mg = camps["bloc3"] == "gauche"
    md = camps["bloc3"] == "droite"
    cols = list(A.ORIENTATION_TWIN.keys())
    configs = T.configs_llm_disponibles()
    tables = [w4.reindex(pid)] + [T.charger_llm(f).reindex(pid) for f in configs.values()]
    noms = ["humains vague 4"] + list(configs.keys())
    manquant = [n for n, d in zip(noms, tables) if any(c not in d.columns for c in cols)]
    ok = [(n, d) for n, d in zip(noms, tables) if n not in manquant]
    codes, ks, hors = A.coder_echelle_fixe([d for _, d in ok], cols, [1.0, 2.0, 3.0,
                                                                       4.0, 5.0])
    for (n, _), h in zip(ok, hors):
        if h:
            print(f"  {n} : {h} reponses hors de l'echelle a cinq points, comptees "
                  f"manquantes", flush=True)
    sens = np.array([A.ORIENTATION_TWIN[c][0] for c in cols])
    S = A.scores_generiques(ks, sens)
    inds = {n: C.Indicatrice(c, ks) for (n, _), c in zip(ok, codes)}
    ind_h = inds["humains vague 4"]
    tg = C.mesures(ind_h.tables(C.poids_plein(mg)))
    td = C.mesures(ind_h.tables(C.poids_plein(md)))
    garde = (tg["n"][0] >= C.N_MIN_ITEM) & (td["n"][0] >= C.N_MIN_ITEM)
    W = A.poids_bootstrap_global(ind_h.n, args.boot, rng)
    lignes = []
    tous = np.ones(ind_h.n, dtype=np.float32)
    ref = pente_condition(ind_h, mg, md, S, garde, W, m_tous=tous)
    lignes.append(bloc("humains vague 4", ref, None, "Twin, 10 items"))
    for nom, ind in inds.items():
        if nom == "humains vague 4":
            continue
        r = pente_condition(ind, mg, md, S, garde, W, m_tous=tous)
        lignes.append(bloc(nom, r, ref, "Twin, 10 items"))
    df = pd.DataFrame(lignes)
    s = df["p"].notna()
    df.loc[s, "p_holm"] = C.holm(df.loc[s, "p"].values)
    C.ecrire(df, "a37-agents-twin.csv")
    if manquant:
        print(f"configurations sans les dix items, ignorees : {manquant}", flush=True)
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", dest="cache_foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--boot", type=int, default=A.N_BOOT)
    args = ap.parse_args()
    rng = np.random.default_rng(A.GRAINE)
    volet_gss(args, rng)
    volet_twin(args, rng)


if __name__ == "__main__":
    main()
