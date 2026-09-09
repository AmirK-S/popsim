"""
a37_humains : l'effet de consensus liberal chez les vrais humains, GSS et Twin-2K-500.

Volet 1 de a37. Aucun appel de modele de langage, lecture seule sur data/, quatre coeurs.
Aucun fichier existant n'est modifie.

LA QUESTION
-----------
Brandt et Sleegers (2021) reproduisent par simulation le fait que la gauche americaine est
plus consensuelle que la droite, a partir de deux parametres et de rien d'autre : sur les
items de politique publique, l'opinion majoritaire penche a gauche ; sur l'etiquette
ideologique, elle penche a droite. Leur diagnostic est explicite : les gens de gauche sont
pres du consensus parce que la derive agregee va dans leur sens, et les gens de droite s'en
ecartent de facon variee. Ce modele a une consequence testable que personne n'a testee sur
des reponses individuelles : le rapport de dispersion droite sur gauche d'un item doit
dependre du SENS de la derive agregee de cet item, et s'inverser la ou la majorite penche
a droite.

FAMILLE D'HYPOTHESES, ECRITE AVANT DE REGARDER LE MOINDRE RESULTAT
------------------------------------------------------------------
Convention de signe : la derive D d'un item est la position moyenne de l'echantillon moins
le point neutre de l'item, orientee gauche vers droite. D > 0 veut dire que l'echantillon
penche a droite sur cet item.

Famille « pentes humaines », quatre tests, correction de Holm :
  H1 : sur le GSS, la pente de log(rapport droite sur gauche) sur D est NEGATIVE.
  H2 : la meme pente reste negative quand on retire les items dont l'orientation est de
       niveau [HYPOTHESE].
  H3 : la meme pente reste negative quand l'orientation vient du codeur automatique B et
       non du codeur A qui lit les libelles.
  H4 : sur les dix items de politique publique de Twin-2K-500, la pente est negative.

Famille « ce qui reste », trois tests, correction de Holm :
  H5 : l'ordonnee a l'origine de la regression, c'est a dire le rapport attendu pour un
       item de derive nulle, ne differe pas de 0 en logarithme. Si H5 n'est pas rejetee,
       le modele a deux parametres suffit ; si elle est rejetee, il reste une asymetrie
       que la derive n'explique pas.
  H6 : le rapport global predit par le seul temoin de position (la dispersion maximale a
       position donnee, camp par camp et item par item) ne differe pas du rapport global
       observe, 1,122.
  H7 : la vague 2, memes personnes deux semaines plus tard, donne la meme pente
       (plancher de bruit).

Famille « accord des codeurs », un test, non corrige :
  H8 : le taux d'accord entre le codeur A et le codeur B depasse le hasard.

SORTIES
-------
  resultats/a37-orientation-items.csv      l'orientation item par item, les deux codeurs
  resultats/a37-gss-par-item.csv           derive, dispersions, rapport, temoin de position
  resultats/a37-regressions-humains.csv    les pentes, avec IC de bootstrap et p corriges
  resultats/a37-decomposition.csv          ce qui reste du 1,122 une fois la derive otee
  resultats/a37-twin-par-item.csv          les dix items de politique publique de Twin

Usage : .venv/bin/python analyses/a37_humains.py [--boot 1000] [--perm 2000]
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
from a2_baselines_gss import charger  # noqa: E402
from a25_commun import options_par_item  # noqa: E402

STRICT = ("[CONFIRME]", "[PROBABLE]")


def charger_gss():
    ids, items, y1, y2, x, attributs = charger()
    options = options_par_item(A.RACINE)
    codes1, ks = C.coder_gss(y1, items, options)
    codes2, _ = C.coder_gss(y2, items, options)
    camps = C.camps_gss(x, attributs)
    return ids, items, options, codes1, codes2, ks, camps


def bloc_regression(nom, famille, ind, mg, md, S, garde, rng, boot, perm):
    r = A.regression_bootstrap(ind, mg, md, S, garde, rng, boot)
    r["p"] = A.p_permutation_pente(ind, mg, md, S, garde, r["pente"], rng, perm)
    r["test"] = nom
    r["famille_de_tests"] = famille
    print(f"{nom:46s} pente {r['pente']:+.4f} "
          f"[{r['pente_ic_bas']:+.4f} ; {r['pente_ic_haut']:+.4f}] "
          f"R2 {r['r2']:.3f}  rho {r['spearman']:+.3f}  "
          f"ordonnee {r['ordonnee']:+.4f}  p {r['p']:.4f}  n {r['n_items']}", flush=True)
    return r


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot", type=int, default=A.N_BOOT)
    ap.add_argument("--perm", type=int, default=A.N_PERM)
    args = ap.parse_args()
    rng = np.random.default_rng(A.GRAINE)

    ids, items, options, codes1, codes2, ks, camps = charger_gss()
    J = len(items)
    ind1 = C.Indicatrice(codes1, ks)
    ind2 = C.Indicatrice(codes2, ks)
    mg = camps["bloc3"] == "gauche"
    md = camps["bloc3"] == "droite"
    fam = C.familles_gss(items)
    print(f"{len(ids)} personnes, {J} items ; gauche {mg.sum()}, droite {md.sum()}",
          flush=True)

    # ------------------------------------------------------- orientation, codeur A
    S, oriente, sens_a, niveaux, justifs = A.scores_gss(items, options)
    print(f"codeur A : {int(oriente.sum())} items orientes, "
          f"{J - int(oriente.sum())} sans orientation", flush=True)
    manquants = [it for it in items
                 if it not in A.ORIENTATION and it not in A.SANS_ORIENTATION]
    if manquants:
        print(f"AVERTISSEMENT : items ni orientes ni declares sans orientation : "
              f"{manquants}", flush=True)

    # ------------------------------------------------------- orientation, codeur B
    sens_b, ecart_camps = A.codeur_empirique(ind1, mg, md, ks)
    sens_b2, _ = A.codeur_empirique(ind2, mg, md, ks)
    accord = (sens_a == sens_b) & oriente
    n_or = int(oriente.sum())
    taux = float(accord.sum()) / n_or
    # Test binomial exact contre le hasard (une chance sur deux de tomber juste).
    from math import comb
    k = int(accord.sum())
    p_accord = sum(comb(n_or, i) for i in range(k, n_or + 1)) / (2.0 ** n_or)
    stab_b = float((sens_b == sens_b2).mean())
    print(f"codeur B : accord avec A sur {k}/{n_or} items, taux {taux:.3f}, "
          f"p binomial {p_accord:.2e} ; stabilite de B entre vagues {stab_b:.3f}",
          flush=True)

    S_b = A.scores_generiques(ks, np.where(oriente, sens_b, 0))

    # ------------------------------------------------------- table d'orientation
    C.ecrire(pd.DataFrame({
        "item": items, "famille": [fam[i] for i in items],
        "n_modalites": ks,
        "modalites": [" | ".join(options[i]) for i in items],
        "oriente": oriente,
        "sens_codeur_A": sens_a, "niveau_codeur_A": niveaux,
        "justification_codeur_A": justifs,
        "sens_codeur_B": np.where(oriente, sens_b, 0),
        "ecart_position_droite_moins_gauche": ecart_camps,
        "accord_A_B": np.where(oriente, accord, None),
    }), "a37-orientation-items.csv")

    # ------------------------------------------------------- par item
    tous = np.ones(len(ids), dtype=np.float32)
    d_obs = A.derive(ind1.tables(tous[None, :]), S)[0]
    tg = C.mesures(ind1.tables(C.poids_plein(mg)))
    td = C.mesures(ind1.tables(C.poids_plein(md)))
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = td["gs"][0] / tg["gs"][0]
    garde_base = (tg["n"][0] >= C.N_MIN_ITEM) & (td["n"][0] >= C.N_MIN_ITEM)
    garde = oriente & garde_base & np.isfinite(d_obs) & np.isfinite(ratio) & (ratio > 0)
    garde_strict = garde & np.isin(niveaux, STRICT)
    print(f"items retenus : {int(garde.sum())} pour la regression principale, "
          f"{int(garde_strict.sum())} pour la version stricte", flush=True)

    # Temoin de position : la dispersion maximale a position donnee, camp par camp.
    pos_g = A.position(ind1.tables(C.poids_plein(mg)), S)
    pos_d = A.position(ind1.tables(C.poids_plein(md)), S)
    gs_tem_g = A.gs_temoin(ind1.tables(C.poids_plein(mg)), S)[0]
    gs_tem_d = A.gs_temoin(ind1.tables(C.poids_plein(md)), S)[0]
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio_tem = gs_tem_d / gs_tem_g

    d_v2 = A.derive(ind2.tables(tous[None, :]), S)[0]
    tg2 = C.mesures(ind2.tables(C.poids_plein(mg)))
    td2 = C.mesures(ind2.tables(C.poids_plein(md)))
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio_v2 = td2["gs"][0] / tg2["gs"][0]

    C.ecrire(pd.DataFrame({
        "item": items, "famille": [fam[i] for i in items],
        "retenu": garde, "retenu_strict": garde_strict,
        "niveau_orientation": niveaux,
        "derive_agregee": d_obs,
        "position_moyenne": d_obs + 0.5,
        "position_gauche": pos_g[0], "position_droite": pos_d[0],
        "gs_gauche": tg["gs"][0], "gs_droite": td["gs"][0],
        "ratio_droite_gauche": ratio, "log_ratio": np.log(ratio),
        "gs_temoin_gauche": gs_tem_g, "gs_temoin_droite": gs_tem_d,
        "ratio_temoin_position": ratio_tem,
        "residu_log": np.log(ratio) - np.log(ratio_tem),
        "derive_vague2": d_v2, "ratio_vague2": ratio_v2,
    }), "a37-gss-par-item.csv")

    # ------------------------------------------------------- regressions
    regs = []
    r1 = bloc_regression("H1 GSS, codeur A, tous items orientes", "pentes humaines",
                         ind1, mg, md, S, garde, rng, args.boot, args.perm)
    regs.append(r1)
    regs.append(bloc_regression("H2 GSS, codeur A, orientation stricte",
                                "pentes humaines", ind1, mg, md, S, garde_strict, rng,
                                args.boot, args.perm))
    garde_b = oriente & garde_base & np.isfinite(ratio) & (ratio > 0)
    regs.append(bloc_regression("H3 GSS, codeur B automatique", "pentes humaines",
                                ind1, mg, md, S_b, garde_b, rng, args.boot, args.perm))
    r7 = bloc_regression("H7 GSS vague 2, plancher de bruit", "ce qui reste",
                         ind2, mg, md, S, garde, rng, args.boot, args.perm)

    # ------------------------------------------------------- Twin, items politiques
    w13 = T.charger_humains("1_3")
    w4 = T.charger_humains("4")
    camps_t = C.camps_twin(w13)
    mgt = camps_t["bloc3"] == "gauche"
    mdt = camps_t["bloc3"] == "droite"
    cols_t = list(A.ORIENTATION_TWIN.keys())
    codes_t, ks_t = C.coder_numerique(w13, cols_t)
    ind_t = C.Indicatrice(codes_t, ks_t)
    sens_t = np.array([A.ORIENTATION_TWIN[c][0] for c in cols_t])
    S_t = A.scores_generiques(ks_t, sens_t)
    sens_tb, _ = A.codeur_empirique(ind_t, mgt, mdt, ks_t)
    print(f"Twin : {int(mgt.sum())} a gauche, {int(mdt.sum())} a droite, "
          f"{len(cols_t)} items ; accord des codeurs "
          f"{int((sens_t == sens_tb).sum())}/{len(cols_t)}", flush=True)

    tous_t = np.ones(ind_t.n, dtype=np.float32)
    d_t = A.derive(ind_t.tables(tous_t[None, :]), S_t)[0]
    tgt = C.mesures(ind_t.tables(C.poids_plein(mgt)))
    tdt = C.mesures(ind_t.tables(C.poids_plein(mdt)))
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio_t = tdt["gs"][0] / tgt["gs"][0]
    garde_t = (tgt["n"][0] >= C.N_MIN_ITEM) & (tdt["n"][0] >= C.N_MIN_ITEM) \
        & np.isfinite(ratio_t) & (ratio_t > 0)

    # vague 4, memes personnes, memes items : plancher de bruit du cote Twin
    codes_t4, _ = C.coder_numerique_commun([w13, w4.reindex(w13.index)], cols_t)
    ind_t4 = C.Indicatrice(codes_t4[1], ks_t)
    d_t4 = A.derive(ind_t4.tables(tous_t[None, :]), S_t)[0]
    tgt4 = C.mesures(ind_t4.tables(C.poids_plein(mgt)))
    tdt4 = C.mesures(ind_t4.tables(C.poids_plein(mdt)))
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio_t4 = tdt4["gs"][0] / tgt4["gs"][0]

    C.ecrire(pd.DataFrame({
        "item": cols_t,
        "libelle": [T.table_items().at[c, "libelle"] for c in cols_t],
        "sens_codeur_A": sens_t, "sens_codeur_B": sens_tb,
        "retenu": garde_t,
        "derive_agregee": d_t, "position_moyenne": d_t + 0.5,
        "gs_gauche": tgt["gs"][0], "gs_droite": tdt["gs"][0],
        "ratio_droite_gauche": ratio_t, "log_ratio": np.log(ratio_t),
        "derive_vague4": d_t4, "ratio_vague4": ratio_t4,
    }), "a37-twin-par-item.csv")

    regs.append(bloc_regression("H4 Twin, dix items de politique publique",
                                "pentes humaines", ind_t, mgt, mdt, S_t, garde_t, rng,
                                args.boot, args.perm))
    r_t4 = bloc_regression("Twin vague 4, plancher de bruit", "ce qui reste",
                           ind_t4, mgt, mdt, S_t, garde_t, rng, args.boot, args.perm)

    # ------------------------------------------------------- H5 : l'ordonnee
    # L'ordonnee a l'origine est le logarithme du rapport attendu pour un item dont la
    # derive agregee est nulle. Si le modele a deux parametres suffisait, elle vaudrait
    # zero. Le p est tire de la distribution de bootstrap sur les personnes.
    p_ord = A.p_bootstrap_bilateral(r1["_consts_boot"])

    # ------------------------------------------------------- H6 : le temoin de position
    n_p = len(ids)
    W = A.poids_bootstrap_global(n_p, args.boot, rng)
    mg_f = mg.astype(np.float32)
    md_f = md.astype(np.float32)
    obs_g = float(np.nanmean(np.where(garde, tg["gs"][0], np.nan)))
    obs_d = float(np.nanmean(np.where(garde, td["gs"][0], np.nan)))
    tem_g = float(np.nanmean(np.where(garde, gs_tem_g, np.nan)))
    tem_d = float(np.nanmean(np.where(garde, gs_tem_d, np.nan)))
    temg_b = A.gs_temoin(ind1.tables(W * mg_f[None, :]), S)
    temd_b = A.gs_temoin(ind1.tables(W * md_f[None, :]), S)
    obsg_b = C.mesures(ind1.tables(W * mg_f[None, :]))["gs"]
    obsd_b = C.mesures(ind1.tables(W * md_f[None, :]))["gs"]
    gm = garde[None, :]
    with np.errstate(invalid="ignore"):
        r_obs_b = (np.nanmean(np.where(gm, obsd_b, np.nan), axis=1)
                   / np.nanmean(np.where(gm, obsg_b, np.nan), axis=1))
        r_tem_b = (np.nanmean(np.where(gm, temd_b, np.nan), axis=1)
                   / np.nanmean(np.where(gm, temg_b, np.nan), axis=1))
    ecart_b = r_obs_b - r_tem_b
    p_tem = A.p_bootstrap_bilateral(ecart_b)

    # Rapport global sur les memes items, mesure et temoin, plus la part expliquee.
    lr_obs = np.where(garde, np.log(ratio), np.nan)
    lr_tem = np.where(garde, np.log(ratio_tem), np.nan)
    ok = np.isfinite(lr_obs) & np.isfinite(lr_tem)
    part_expliquee = float(1.0 - np.nanvar(lr_obs[ok] - lr_tem[ok])
                           / np.nanvar(lr_obs[ok]))

    # Les deux parametres du modele generatif, mesures et non supposes.
    # Parametre 1 : la derive agregee des items de politique publique.
    # Parametre 2 : la derive agregee de l'etiquette ideologique elle meme.
    d1 = float(np.nanmean(np.where(garde, d_obs, np.nan)))
    ordre7 = C.GSS_POINTS7
    pos7 = np.array([ordre7.index(v) / 6.0 for v in camps["points7"] if v in ordre7])
    d2 = float(pos7.mean() - 0.5)
    v_t = pd.to_numeric(w13["QID22"], errors="coerce").dropna().to_numpy()
    d2t = float(((5.0 - v_t) / 4.0).mean() - 0.5)
    d1t = float(np.nanmean(np.where(garde_t, d_t, np.nan)))

    deco = pd.DataFrame([
        {"quantite": "parametre 1 de Brandt et Sleegers, GSS : derive agregee des items",
         "gauche": np.nan, "droite": np.nan, "rapport": d1,
         "ic_bas": np.nan, "ic_haut": np.nan, "n_items": int(garde.sum()),
         "commentaire": f"negatif = les items penchent a gauche ; "
                        f"{int((np.where(garde, d_obs, np.nan) < 0).sum())} items sur "
                        f"{int(garde.sum())} penchent a gauche"},
        {"quantite": "parametre 2 de Brandt et Sleegers, GSS : derive de l'etiquette",
         "gauche": np.nan, "droite": np.nan, "rapport": d2,
         "ic_bas": np.nan, "ic_haut": np.nan, "n_items": len(pos7),
         "commentaire": "positif = l'etiquette penche a droite, ce que le modele "
                        "suppose ; NEGATIF ICI, le parametre 2 n'est pas verifie"},
        {"quantite": "parametre 1, Twin : derive agregee des dix items politiques",
         "gauche": np.nan, "droite": np.nan, "rapport": d1t,
         "ic_bas": np.nan, "ic_haut": np.nan, "n_items": int(garde_t.sum()),
         "commentaire": "negatif = les items penchent a gauche"},
        {"quantite": "parametre 2, Twin : derive de l'etiquette QID22",
         "gauche": np.nan, "droite": np.nan, "rapport": d2t,
         "ic_bas": np.nan, "ic_haut": np.nan, "n_items": len(v_t),
         "commentaire": "NEGATIF ICI aussi, le parametre 2 n'est pas verifie"},
    ] + [
        {"quantite": "rapport global observe, items orientes retenus",
         "gauche": obs_g, "droite": obs_d, "rapport": obs_d / obs_g,
         "ic_bas": float(np.percentile(r_obs_b[np.isfinite(r_obs_b)], 2.5)),
         "ic_haut": float(np.percentile(r_obs_b[np.isfinite(r_obs_b)], 97.5)),
         "n_items": int(garde.sum()), "commentaire":
             "sous ensemble des items orientes, a comparer au 1,1225 de a30 sur les 149"},
        {"quantite": "rapport global du temoin de position",
         "gauche": tem_g, "droite": tem_d, "rapport": tem_d / tem_g,
         "ic_bas": float(np.percentile(r_tem_b[np.isfinite(r_tem_b)], 2.5)),
         "ic_haut": float(np.percentile(r_tem_b[np.isfinite(r_tem_b)], 97.5)),
         "n_items": int(garde.sum()), "commentaire":
             "dispersion maximale a position donnee, camp par camp et item par item"},
        {"quantite": "ecart observe moins temoin",
         "gauche": np.nan, "droite": np.nan,
         "rapport": obs_d / obs_g - tem_d / tem_g,
         "ic_bas": float(np.percentile(ecart_b[np.isfinite(ecart_b)], 2.5)),
         "ic_haut": float(np.percentile(ecart_b[np.isfinite(ecart_b)], 97.5)),
         "n_items": int(garde.sum()), "commentaire": f"p de bootstrap {p_tem:.4f}"},
        {"quantite": "rapport attendu a derive nulle (ordonnee de H1)",
         "gauche": np.nan, "droite": np.nan,
         "rapport": r1["ratio_a_derive_nulle"],
         "ic_bas": float(np.exp(r1["ordonnee_ic_bas"])),
         "ic_haut": float(np.exp(r1["ordonnee_ic_haut"])),
         "n_items": r1["n_items"], "commentaire": f"p de bootstrap {p_ord:.4f}"},
        {"quantite": "part de la variance item par item du log rapport expliquee par le "
                     "temoin de position",
         "gauche": np.nan, "droite": np.nan, "rapport": part_expliquee,
         "ic_bas": np.nan, "ic_haut": np.nan, "n_items": int(ok.sum()),
         "commentaire": "1 moins variance du residu sur variance du log rapport"},
        {"quantite": "temoin de position, items BINAIRES seulement",
         "gauche": np.nan, "droite": np.nan, "rapport": np.nan,
         "ic_bas": np.nan, "ic_haut": np.nan, "n_items": 0,
         "commentaire": "rempli plus bas"},
        {"quantite": "part expliquee par la derive agregee seule (R2 de H1)",
         "gauche": np.nan, "droite": np.nan, "rapport": r1["r2"],
         "ic_bas": r1["r2_ic_bas"], "ic_haut": r1["r2_ic_haut"],
         "n_items": r1["n_items"], "commentaire": "regression a un seul predicteur"},
    ])
    # Le temoin de position est une identite arithmetique sur un item binaire : la
    # moyenne y determine la loi. La quantite lisible est donc sa part expliquee sur les
    # seuls items a plus de deux modalites, ou il peut se tromper.
    lignes_k = []
    for lab, sel in (("items binaires", ks == 2),
                     ("items a plus de deux modalites", ks > 2)):
        m = garde & sel
        lo = np.where(m, np.log(ratio), np.nan)
        lt = np.where(m, np.log(ratio_tem), np.nan)
        okk = np.isfinite(lo) & np.isfinite(lt)
        part = float(1.0 - np.nanvar(lo[okk] - lt[okk]) / np.nanvar(lo[okk]))
        og = float(np.nanmean(np.where(m, tg["gs"][0], np.nan)))
        od = float(np.nanmean(np.where(m, td["gs"][0], np.nan)))
        tgm = float(np.nanmean(np.where(m, gs_tem_g, np.nan)))
        tdm = float(np.nanmean(np.where(m, gs_tem_d, np.nan)))
        p_, _, r2_, _ = A.ols(np.where(m, d_obs, np.nan), lo)
        lignes_k.append({
            "quantite": f"temoin de position, {lab}", "gauche": og, "droite": od,
            "rapport": od / og, "ic_bas": np.nan, "ic_haut": np.nan,
            "n_items": int(m.sum()),
            "commentaire": f"rapport du temoin {tdm / tgm:.4f} ; part de variance "
                           f"expliquee par le temoin {part:.4f} ; pente {p_:.3f} ; "
                           f"R2 de la derive {r2_:.3f}"})
    deco = pd.concat([deco[deco["quantite"] != "temoin de position, items BINAIRES "
                                               "seulement"],
                      pd.DataFrame(lignes_k)], ignore_index=True)
    C.ecrire(deco, "a37-decomposition.csv")
    print(deco.to_string(index=False), flush=True)

    # ------------------------------------------------------- tableau des regressions
    lignes = []
    for r in regs + [r7, r_t4]:
        lignes.append({k: v for k, v in r.items() if not k.startswith("_")})
    lignes.append({"test": "H5 ordonnee a l'origine differente de 0",
                   "famille_de_tests": "ce qui reste",
                   "pente": np.nan, "pente_ic_bas": np.nan, "pente_ic_haut": np.nan,
                   "ordonnee": r1["ordonnee"], "ordonnee_ic_bas": r1["ordonnee_ic_bas"],
                   "ordonnee_ic_haut": r1["ordonnee_ic_haut"],
                   "ratio_a_derive_nulle": r1["ratio_a_derive_nulle"],
                   "r2": np.nan, "r2_ic_bas": np.nan, "r2_ic_haut": np.nan,
                   "spearman": np.nan, "n_items": r1["n_items"], "p": p_ord})
    lignes.append({"test": "H6 rapport observe contre temoin de position",
                   "famille_de_tests": "ce qui reste",
                   "pente": np.nan, "pente_ic_bas": np.nan, "pente_ic_haut": np.nan,
                   "ordonnee": np.nan, "ordonnee_ic_bas": np.nan,
                   "ordonnee_ic_haut": np.nan,
                   "ratio_a_derive_nulle": np.nan, "r2": np.nan, "r2_ic_bas": np.nan,
                   "r2_ic_haut": np.nan, "spearman": np.nan,
                   "n_items": int(garde.sum()), "p": p_tem})
    lignes.append({"test": "H8 accord des deux codeurs d'orientation",
                   "famille_de_tests": "accord des codeurs",
                   "pente": np.nan, "pente_ic_bas": np.nan, "pente_ic_haut": np.nan,
                   "ordonnee": np.nan, "ordonnee_ic_bas": np.nan,
                   "ordonnee_ic_haut": np.nan,
                   "ratio_a_derive_nulle": taux, "r2": np.nan, "r2_ic_bas": np.nan,
                   "r2_ic_haut": np.nan, "spearman": stab_b, "n_items": n_or,
                   "p": p_accord})
    df = pd.DataFrame(lignes)
    for f in df["famille_de_tests"].unique():
        s = df["famille_de_tests"] == f
        if s.sum() > 1:
            df.loc[s, "p_holm"] = C.holm(df.loc[s, "p"].fillna(1.0).values)
        else:
            df.loc[s, "p_holm"] = df.loc[s, "p"]
    C.ecrire(df, "a37-regressions-humains.csv")
    print(df[["test", "famille_de_tests", "pente", "pente_ic_bas", "pente_ic_haut",
              "r2", "n_items", "p", "p_holm"]].to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
