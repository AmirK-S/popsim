"""
i1_changement : Q-A du preenregistrement I1. Combien de personnes changent, sur combien
d'items, et quelle part de ce changement est dirigee dans le sens de la derive de la
periode plutot qu'un aller retour.

Zero appel de modele. Lecture seule sur data/. Aucun script existant modifie.

Sorties :
  resultats/i1-controles.csv
  resultats/i1-changement-par-item.csv
  resultats/i1-changement-par-personne.csv
  resultats/i1-trois-vagues.csv
  resultats/i1-synthese-changement.csv

Usage : .venv/bin/python analyses/i1_changement.py
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import i1_commun as I1
import a12_retest_delai as A12
from a2_commun import bootstrap_personnes


def controles(noyau, brut, tables, n_paires):
    """Les controles bloquants du preenregistrement, section 8, executes avant tout le reste."""
    lignes = []
    lignes.append({"controle": "nombre de paires de vagues", "attendu": 11,
                   "obtenu": n_paires, "passe": n_paires == 11})
    lignes.append({"controle": "taille du noyau commun", "attendu": 118,
                   "obtenu": len(noyau), "passe": len(noyau) == 118})

    # C1 : reproduction des deux denominateurs de a12 sur le noyau commun, onze paires.
    idx = list(range(len(noyau)))
    for ecart, cible in ((2, 0.6953), (4, 0.6745)):
        num, den = 0.0, 0
        for nom in A12.PANELS:
            for a, b, e in A12.PANELS[nom]["paires"]:
                if e != ecart:
                    continue
                pp, _, _, _ = A12.consistance(brut[nom]["mat"][a], brut[nom]["mat"][b], idx)
                n = int(np.isfinite(pp).sum())
                num += float(np.nanmean(pp)) * n
                den += n
        obt = num / den
        lignes.append({"controle": f"consistance a {ecart} ans, noyau commun, a12",
                       "attendu": cible, "obtenu": round(obt, 6),
                       "passe": abs(obt - cible) < 0.002, "n_personnes": den})
    return lignes


def par_item(paquet, tables):
    """Une ligne par item et par paire : taux de changement, derive, classes."""
    lignes = []
    k = paquet["k_par_item"]
    for bloc in paquet["blocs"]:
        taux, tv, neval = I1.derive_item(bloc["c_a"], bloc["c_b"], k)
        cls = bloc["classe"]
        for j, it in enumerate(paquet["items"]):
            n = int(neval[j])
            if n == 0:
                continue
            c = cls[:, j]
            n_chg = int((c > 0).sum())
            lignes.append({
                "item": it, "panel": bloc["panel"],
                "paire": f"{bloc['depart']}-{bloc['arrivee']}",
                "ecart_annees": bloc["arrivee"] - bloc["depart"],
                "n_personnes": n, "n_changeurs": n_chg,
                "taux_changement": taux[j], "derive_nette_tv": tv[j],
                "part_dirigee": tv[j] / taux[j] if taux[j] > 0 else np.nan,
                "n_monotone": int((c == 1).sum()),
                "n_contraire": int((c == 2).sum()),
                "n_indetermine": int((c == 3).sum()),
                "part_monotone_du_changement": (c == 1).sum() / n_chg if n_chg else np.nan,
                "part_contraire_du_changement": (c == 2).sum() / n_chg if n_chg else np.nan,
            })
    return pd.DataFrame(lignes)


def nul_remelange(paquet, n_replicats, rng):
    """Le temoin de derive : la colonne d'arrivee est remelangee entre les personnes.

    Les deux marginales et donc la derive agregee de l'item sont conservees exactement ;
    l'appariement individuel est detruit. C'est le nul avec derive du preenregistrement,
    applique ici a la classification et non a la prediction : il dit quelle part de
    l'exces de changement monotone est une consequence mecanique de la derive.
    """
    k = paquet["k_par_item"]
    acc = []
    for r in range(n_replicats):
        n_mono = np.zeros(len(paquet["items"]))
        n_contre = np.zeros(len(paquet["items"]))
        n_chg = np.zeros(len(paquet["items"]))
        for bloc in paquet["blocs"]:
            ca, cb = bloc["c_a"], bloc["c_b"].copy()
            for j in range(cb.shape[1]):
                ok = np.flatnonzero((ca[:, j] >= 0) & (cb[:, j] >= 0))
                if len(ok) > 1:
                    cb[ok, j] = cb[rng.permutation(ok), j]
            cls = I1.classer_changement(ca, cb, k)
            n_mono += (cls == 1).sum(axis=0)
            n_contre += (cls == 2).sum(axis=0)
            n_chg += (cls > 0).sum(axis=0)
        acc.append({"replicat": r,
                    "part_monotone": float(n_mono.sum() / max(n_chg.sum(), 1)),
                    "part_contraire": float(n_contre.sum() / max(n_chg.sum(), 1)),
                    "taux_changement_relatif": float(n_chg.sum())})
    return pd.DataFrame(acc)


def _sans_point_fixe(origines, destinations, rng, essais=50):
    """Permute les destinations sans qu'aucun changeur ne recoive sa propre origine.

    Sans cette precaution un tiers des changeurs redeviendrait stable et le taux de
    changement du temoin ne serait plus celui de la population, ce qui rendrait la
    comparaison des parts inutilisable. Permutation, puis reparation des conflits par
    echange avec une position tiree au hasard ; si des conflits subsistent apres le
    nombre d'essais, ils sont laisses et le taux de changement obtenu est publie.
    """
    d = destinations[rng.permutation(len(destinations))]
    for _ in range(essais):
        conflits = np.flatnonzero(d == origines)
        if not len(conflits):
            break
        cible = rng.integers(0, len(d), size=len(conflits))
        d[conflits], d[cible] = d[cible], d[conflits]
    return d


def nul_destinations(paquet, n_replicats, rng):
    """Le nul avec derive a taux de changement conserve : on remelange les DESTINATIONS
    entre les seuls changeurs de chaque item.

    Les origines et les destinations restent les memes multiensembles, donc les deux
    marginales et la derive agregee de l'item sont conservees EXACTEMENT ; les stables
    restent stables, donc le taux de changement brut est conserve a la reflexivite pres
    (un changeur peut recevoir sa propre modalite de depart et devenir stable ; le taux
    obtenu est publie a cote). Ce qui est detruit est le lien entre qui part et ou il va.
    C'est le temoin qui dit si l'exces de changement monotone est une consequence
    mecanique de la derive ou s'il tient a la structure des trajectoires.
    """
    k = paquet["k_par_item"]
    acc = []
    p = len(paquet["items"])
    par_item = {c: np.zeros(p) for c in ("mono", "contre", "chg", "eval")}
    for r in range(n_replicats):
        n_mono = n_contre = n_chg = n_eval = 0
        for bloc in paquet["blocs"]:
            ca, cb = bloc["c_a"], bloc["c_b"].copy()
            for j in range(cb.shape[1]):
                bouge = np.flatnonzero((ca[:, j] >= 0) & (cb[:, j] >= 0)
                                       & (ca[:, j] != cb[:, j]))
                if len(bouge) > 1:
                    cb[bouge, j] = _sans_point_fixe(ca[bouge, j], cb[bouge, j], rng)
            cls = I1.classer_changement(ca, cb, k)
            n_mono += int((cls == 1).sum())
            n_contre += int((cls == 2).sum())
            n_chg += int((cls > 0).sum())
            n_eval += int((cls >= 0).sum())
            par_item["mono"] += (cls == 1).sum(axis=0)
            par_item["contre"] += (cls == 2).sum(axis=0)
            par_item["chg"] += (cls > 0).sum(axis=0)
            par_item["eval"] += (cls >= 0).sum(axis=0)
        acc.append({"replicat": r, "part_monotone": n_mono / max(n_chg, 1),
                    "part_contraire": n_contre / max(n_chg, 1),
                    "taux_changement": n_chg / max(n_eval, 1)})
    detail = pd.DataFrame({
        "item": paquet["items"],
        "nul_part_monotone": par_item["mono"] / np.maximum(par_item["chg"], 1),
        "nul_part_contraire": par_item["contre"] / np.maximum(par_item["chg"], 1),
        "nul_taux_changement": par_item["chg"] / np.maximum(par_item["eval"], 1)})
    return pd.DataFrame(acc), detail


def trois_vagues(noyau, brut, tables):
    """Decomposition stable / aller retour / persistant / erratique, trois panels."""
    k = [max(len(t), 1) for t in tables]
    lignes, par_pers = [], []
    for nom, a, b, c in I1.TROIS_VAGUES:
        ca = I1.coder(brut[nom]["mat"][a], tables)
        cb = I1.coder(brut[nom]["mat"][b], tables)
        cc = I1.coder(brut[nom]["mat"][c], tables)
        ok = (ca >= 0) & (cb >= 0) & (cc >= 0)
        garde = ok.sum(axis=1) >= I1.MIN_ITEMS_INDIVIDU
        ca, cb, cc, ok = ca[garde], cb[garde], cc[garde], ok[garde]
        stable = ok & (ca == cb) & (cb == cc)
        aller_retour = ok & (ca == cc) & (cb != ca)
        persistant = ok & (ca != cc) & ((cb == ca) | (cb == cc))
        erratique = ok & (ca != cc) & (cb != ca) & (cb != cc)
        cls14 = I1.classer_changement(ca, cc, k)
        mono_pers = persistant & (cls14 == 1)
        n = ok.sum(axis=0)
        for j, it in enumerate(noyau):
            if n[j] < I1.MIN_PERSONNES_ITEM:
                continue
            lignes.append({
                "item": it, "panel": nom, "n_personnes": int(n[j]),
                "part_stable": stable[:, j].sum() / n[j],
                "part_aller_retour": aller_retour[:, j].sum() / n[j],
                "part_persistant": persistant[:, j].sum() / n[j],
                "part_erratique": erratique[:, j].sum() / n[j],
                "part_monotone_persistant": mono_pers[:, j].sum() / n[j],
            })
        d = np.maximum(ok.sum(axis=1), 1)
        for i in range(ok.shape[0]):
            par_pers.append({"panel": nom, "n_items": int(ok[i].sum()),
                             "part_aller_retour": aller_retour[i].sum() / d[i],
                             "part_persistant": persistant[i].sum() / d[i]})
    return pd.DataFrame(lignes), pd.DataFrame(par_pers)


def main():
    rng = np.random.default_rng(I1.GRAINE)
    print("chargement des quatre panels", flush=True)
    noyau, brut, n_paires = I1.charger_panels()
    print(f"{len(noyau)} items dans le noyau commun, {n_paires} paires de vagues",
          flush=True)
    tables = I1.alphabet_panel(brut, len(noyau))

    ctrl = controles(noyau, brut, tables, n_paires)
    for l in ctrl:
        print("  controle :", l, flush=True)

    resume = []
    tables_item = {}
    for etiquette, paires in (("4 ans", I1.PAIRES_4ANS), ("2 ans", I1.PAIRES_2ANS)):
        print(f"\nperimetre {etiquette}", flush=True)
        paquet = I1.assembler(paires, noyau, brut, tables)
        print(f"  {paquet['n']} personnes", flush=True)
        ti = par_item(paquet, tables)
        ti["perimetre"] = etiquette
        tables_item[etiquette] = (paquet, ti)

        # agregation par item, ponderee par les personnes evaluees
        g = ti.groupby("item").apply(lambda d: pd.Series({
            "n_personnes": d["n_personnes"].sum(),
            "n_changeurs": d["n_changeurs"].sum(),
            "taux_changement": np.average(d["taux_changement"], weights=d["n_personnes"]),
            "derive_nette_tv": np.average(d["derive_nette_tv"], weights=d["n_personnes"]),
            "part_dirigee": np.average(d["derive_nette_tv"], weights=d["n_personnes"])
            / np.average(d["taux_changement"], weights=d["n_personnes"]),
            "n_monotone": d["n_monotone"].sum(), "n_contraire": d["n_contraire"].sum(),
            "n_indetermine": d["n_indetermine"].sum(),
        }), include_groups=False).reset_index()
        g["part_monotone_du_changement"] = g["n_monotone"] / g["n_changeurs"]
        g["part_contraire_du_changement"] = g["n_contraire"] / g["n_changeurs"]
        g["exces_monotone"] = ((g["n_monotone"] - g["n_contraire"]) / g["n_changeurs"])
        g["perimetre"] = etiquette
        tables_item[etiquette + "_agrege"] = g

        # taux de changement par personne
        cls = paquet["classe"]
        ok = cls >= 0
        d = np.maximum(ok.sum(axis=1), 1)
        taux_p = (cls > 0).sum(axis=1) / d
        mono_p = (cls == 1).sum(axis=1) / d
        m, bas, haut = bootstrap_personnes(taux_p, n_tirages=I1.N_BOOTSTRAP,
                                           graine=I1.GRAINE)
        mm, mbas, mhaut = bootstrap_personnes(mono_p, n_tirages=I1.N_BOOTSTRAP,
                                              graine=I1.GRAINE)
        q = np.percentile(taux_p, [10, 25, 50, 75, 90])
        resume.append({
            "perimetre": etiquette, "n_personnes": paquet["n"],
            "n_items": len(noyau),
            "items_par_personne_median": float(np.median(ok.sum(axis=1))),
            "taux_changement_moyen": m, "ic_bas": bas, "ic_haut": haut,
            "p10": q[0], "p25": q[1], "mediane": q[2], "p75": q[3], "p90": q[4],
            "part_monotone_moyenne": mm, "mono_ic_bas": mbas, "mono_ic_haut": mhaut,
            "part_du_changement_monotone": float((cls == 1).sum() / max((cls > 0).sum(), 1)),
            "part_du_changement_contraire": float((cls == 2).sum() / max((cls > 0).sum(), 1)),
            "part_du_changement_indetermine": float((cls == 3).sum() / max((cls > 0).sum(), 1)),
            "part_personnes_zero_changement": float((taux_p == 0).mean()),
        })

    ti_tout = pd.concat([tables_item["4 ans"][1], tables_item["2 ans"][1]])
    ag = pd.concat([tables_item["4 ans_agrege"], tables_item["2 ans_agrege"]])

    # plancher de Stanford, item par item
    st = pd.read_csv(os.path.join(I1.SORTIE, "a12-items-stables-instables.csv"))
    st = st[["item", "consistance_2sem", "libelle"]].copy()
    st["taux_changement_2sem"] = 1.0 - st["consistance_2sem"]
    ag = ag.merge(st[["item", "libelle", "taux_changement_2sem"]], on="item", how="left")
    ag["surcroit_sur_plancher_stanford"] = (ag["taux_changement"]
                                            - ag["taux_changement_2sem"])
    ag_ref = ag
    I1.ecrire(ti_tout, "i1-changement-par-item-detail.csv")

    # controle 2 du preenregistrement : l'inversion de l'ordre des vagues
    paquet4 = tables_item["4 ans"][0]
    k = paquet4["k_par_item"]
    inv_mono, inv_contre, inv_chg = 0, 0, 0
    tirage = rng.random(len(noyau)) < 0.5
    for bloc in paquet4["blocs"]:
        ca, cb = bloc["c_a"].copy(), bloc["c_b"].copy()
        ca[:, tirage], cb[:, tirage] = bloc["c_b"][:, tirage], bloc["c_a"][:, tirage]
        cls = I1.classer_changement(ca, cb, k)
        inv_mono += int((cls == 1).sum())
        inv_contre += int((cls == 2).sum())
        inv_chg += int((cls > 0).sum())
    ctrl.append({"controle": "inversion de l'ordre des vagues, part monotone",
                 "attendu": round(float((paquet4["classe"] == 1).sum()
                                        / max((paquet4["classe"] > 0).sum(), 1)), 6),
                 "obtenu": round(inv_mono / max(inv_chg, 1), 6),
                 "passe": abs(inv_mono / max(inv_chg, 1)
                              - (paquet4["classe"] == 1).sum()
                              / max((paquet4["classe"] > 0).sum(), 1)) < 1e-12,
                 "n_personnes": inv_chg})

    # le nul avec derive applique a la classification
    print("\nnul avec derive, 50 replicats de remelange", flush=True)
    nul = nul_remelange(paquet4, 50, rng)
    nul["temoin"] = "remelange complet"
    nul2, nul2_item = nul_destinations(paquet4, 50, rng)
    nul2["temoin"] = "remelange des destinations, derive et taux conserves"
    I1.ecrire(pd.concat([nul, nul2]), "i1-nul-remelange.csv")
    obs_mono = float((paquet4["classe"] == 1).sum() / max((paquet4["classe"] > 0).sum(), 1))
    obs_contre = float((paquet4["classe"] == 2).sum() / max((paquet4["classe"] > 0).sum(), 1))
    for etq, t in (("4 ans, nul avec derive, remelange complet", nul),
                   ("4 ans, nul avec derive, destinations remelangees", nul2)):
        resume.append({
            "perimetre": etq,
            "n_personnes": paquet4["n"], "n_items": len(noyau),
            "part_du_changement_monotone": float(t["part_monotone"].mean()),
            "part_du_changement_contraire": float(t["part_contraire"].mean()),
            "taux_changement_moyen": float(t["taux_changement"].mean())
            if "taux_changement" in t else np.nan,
        })
    print(f"  nul destinations monotone {nul2['part_monotone'].mean():.4f} "
          f"contraire {nul2['part_contraire'].mean():.4f} "
          f"taux {nul2['taux_changement'].mean():.4f}", flush=True)
    print(f"  observe monotone {obs_mono:.4f} contraire {obs_contre:.4f}", flush=True)
    print(f"  nul     monotone {nul['part_monotone'].mean():.4f} "
          f"contraire {nul['part_contraire'].mean():.4f}", flush=True)

    ag = ag.merge(nul2_item, on="item", how="left")
    ag["exces_monotone_nul"] = ag["nul_part_monotone"] - ag["nul_part_contraire"]
    I1.ecrire(ag, "i1-changement-par-item.csv")

    tv3, pp3 = trois_vagues(noyau, brut, tables)
    I1.ecrire(tv3, "i1-trois-vagues.csv")
    n = tv3["n_personnes"]
    resume.append({
        "perimetre": "trois vagues, 2006 a 2014",
        "n_personnes": int(pp3["panel"].size), "n_items": int(tv3["item"].nunique()),
        "part_stable": float(np.average(tv3["part_stable"], weights=n)),
        "part_aller_retour": float(np.average(tv3["part_aller_retour"], weights=n)),
        "part_persistant": float(np.average(tv3["part_persistant"], weights=n)),
        "part_erratique": float(np.average(tv3["part_erratique"], weights=n)),
        "part_monotone_persistant": float(np.average(tv3["part_monotone_persistant"],
                                                     weights=n)),
    })
    m, bas, haut = bootstrap_personnes(pp3["part_aller_retour"].values,
                                       n_tirages=I1.N_BOOTSTRAP, graine=I1.GRAINE)
    resume[-1].update({"aller_retour_ic_bas": bas, "aller_retour_ic_haut": haut})

    I1.ecrire(pd.DataFrame(ctrl), "i1-controles.csv")
    I1.ecrire(pd.DataFrame(resume), "i1-synthese-changement.csv")

    # distribution par personne, agregee en deciles, aucune microdonnee
    lignes = []
    for etiquette in ("4 ans", "2 ans"):
        paquet = tables_item[etiquette][0]
        cls = paquet["classe"]
        ok = cls >= 0
        d = np.maximum(ok.sum(axis=1), 1)
        t = (cls > 0).sum(axis=1) / d
        for q in range(10, 100, 10):
            lignes.append({"perimetre": etiquette, "centile": q,
                           "taux_changement": float(np.percentile(t, q))})
    I1.ecrire(pd.DataFrame(lignes), "i1-changement-par-personne.csv")
    print("\ni1_changement termine", flush=True)


if __name__ == "__main__":
    main()
