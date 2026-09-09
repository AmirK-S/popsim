"""
a42_plancher : le resultat des rares est il du bruit de petites cellules ?

Verrou 2 de `MODELE-DU-MONDE.md` section 6, premiere des trois objections de la section 7.
a34 avait mesure l'exces sur plancher mais sur deux partitions dont il declarait lui meme
qu'aucune n'etait a la fois non circulaire pour le plancher et non tautologique pour la
regression. a42 apporte trois partitions tierces, dont une, la stabilite en vague 2, qui
n'emploie aucun predicteur et aucun attribut demographique.

LA FAMILLE D'HYPOTHESES, LES SEUILS ET LES PLANCHERS SONT ECRITS DANS
`resultats/a42-preenregistrement.md`, HORODATE DU 8 SEPTEMBRE 2026 A 15:42:15 CEST, AVANT
TOUT CALCUL, ET CE FICHIER N'A PAS ETE MODIFIE ENSUITE. Il est reproduit dans le rapport.
Rappel de la famille, pour que le script porte lui aussi la trace :

  H1 primaire   13 tests  avantage de rappel sur `B1 argmax` sur les raretes STABLES > 0
  H2 primaire   14 tests  exces sur le plancher de SEGMENT sur les raretes STABLES > 0
  H3 secondaire 13 tests  cet avantage differe t il entre STABLES et INSTABLES, bilateral
  H4 secondaire 14 tests  l'exces sur plancher differe t il entre T3 et T1 de P_B, bilateral
  H5 tertiaire  13 tests  H1 survit il au retrait des modalites portees par moins de 20
                          personnes, controle de Rennard

  Familles corrigees SEPAREMENT par Holm, Benjamini Hochberg rapporte a cote. Tous les p
  sont des p de bootstrap APPARIE SUR LES PERSONNES, 4 000 tirages, lus sur la position de
  zero dans la distribution, plancher a 1 sur 4 000. Un contraste dont un denominateur est
  vide recoit p = 1, convention conservatrice de a29, a31 et a34.

Zero appel de modele de langage. Lecture seule sur data/. Quatre coeurs. Aucun script
existant n'est modifie.

Sorties : a42-partitions.csv, a42-stabilite.csv, a42-partitions-tierces.csv,
a42-contrastes.csv, a42-rennard.csv, a42-controles.csv.

Usage :
  .venv/bin/python analyses/a42_plancher.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl --tirages 4000
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import a42_commun as C


def _moy(v):
    v = np.asarray(v, float)
    v = v[~np.isnan(v)]
    return float(v.mean()) if len(v) else float("nan")


def preparer(paquet, lignes, seuil, refs):
    """Toutes les matrices d'un perimetre et d'un seuil, une seule fois.

    Les planchers et les scores de partition P_B et P_C sont des DESCRIPTEURS DE
    POPULATION calcules une fois sur les 1 052 humains de la vague 1, puis restreints au
    perimetre : c'est la regle de a34, et la raison est la meme, les recalculer sur 150
    personnes donnerait des cases de deux ou trois personnes. En revanche le seuil de
    minorite, les bornes de tercile et le SUPPORT DE MODALITE du controle de Rennard sont
    calcules sur le perimetre, comme le preenregistrement le dit.
    """
    y1 = paquet["y1"][lignes]
    y2 = paquet["y2"][lignes]
    mods = C.modalites_rares(y1, seuil)
    ok = C.observe(y1)
    rare_vrai = C.appartient(y1, mods) & ok

    stab = C.classes_stabilite(y1, y2)
    support = C.support_modalite(y1, y1, ok)

    planchers = {"item": refs["d_item"][lignes],
                 "segment": refs["d_seg"][lignes],
                 "humains vague 2": refs["h2"][lignes]}

    bornes, tvrai = {}, {}
    for nom_part, cle in (("P_B division de recensement", "d_div"),
                          ("P_C partition aleatoire", "d_alea")):
        score = refs[cle][lignes]
        b1, b2 = C.bornes_terciles(score, rare_vrai)
        bornes[nom_part] = (b1, b2)
        tvrai[nom_part] = C.terciles(score, b1, b2)

    return {"lignes": lignes, "y1": y1, "y2": y2, "mods": mods, "ok": ok,
            "rare_vrai": rare_vrai, "stab": stab, "support": support,
            "planchers": planchers, "bornes": bornes, "tvrai": tvrai}


def _reinjecter(mat, lignes, n_tot):
    """Replace un bloc de lignes dans une matrice pleine, pour lire les scores de population."""
    plein = np.empty((n_tot, mat.shape[1]), dtype=object)
    plein[:] = None
    plein[lignes] = mat
    return plein


def terciles_predits(pred, prep, nom_part, refs, paquet):
    """Tercile de la modalite PREDITE, memes bornes que les cellules reelles.

    Convention de a34 reprise telle quelle : sur une partition dont le score est une
    propriete de la MODALITE, la classe d'une cellule osee est celle de la modalite
    predite, sans quoi rappel et precision ne porteraient pas sur la meme partition et le
    F1 n'aurait pas de sens. Sur P_A, ou la classe est une propriete de la PERSONNE sur
    l'item, cette question ne se pose pas : la meme classe sert des deux cotes.
    """
    b1, b2 = prep["bornes"][nom_part]
    lignes = prep["lignes"]
    n_tot = refs["n_tot"]
    plein = _reinjecter(pred, lignes, n_tot)
    seg = refs["seg_div"] if nom_part.startswith("P_B") else refs["seg_alea"]
    score = C.frequence_segment(plein, refs["y1"], refs["ok_tot"], seg,
                                n_min=C.N_MIN_TIERS)[lignes]
    return C.terciles(score, b1, b2)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--tirages", type=int, default=4000)
    args = ap.parse_args()

    rng = np.random.default_rng(C.GRAINE)
    paquet = C.charger(args.cache, args.cache_foret, args.cache_a35)
    y1, y2, x, items = paquet["y1"], paquet["y2"], paquet["x"], paquet["items"]
    n_tot = len(paquet["ids"])
    controles = []

    testees = [m for m in C.TESTEES if m in paquet["M"]]
    absentes = [m for m in C.TESTEES if m not in paquet["M"]]
    controles.append({"controle": "methodes testees disponibles",
                      "valeur": float(len(testees)), "reference": float(len(C.TESTEES)),
                      "detail": ", ".join(absentes) if absentes else "aucune absente"})
    print(f"methodes testees : {len(testees)}/{len(C.TESTEES)}"
          + (f", absentes : {absentes}" if absentes else ""))

    # -------------------------------------------- references de population, 1 052 humains
    ok_tot = C.observe(y1)
    seg_fin, niveaux_fin = C.segment_fin(x, paquet["attributs"])
    seg_div, niveaux_div = C.segment_axe(x, paquet["attributs"])
    seg_alea, niveaux_alea = C.segment_placebo(n_tot)
    refs = {
        "n_tot": n_tot, "y1": y1, "ok_tot": ok_tot,
        "seg_div": seg_div, "seg_alea": seg_alea,
        "d_item": C.frequence_item(y1, y1, ok_tot),
        "d_seg": C.frequence_segment(y1, y1, ok_tot, seg_fin),
        "d_div": C.frequence_segment(y1, y1, ok_tot, seg_div, n_min=C.N_MIN_TIERS),
        "d_alea": C.frequence_segment(y1, y1, ok_tot, seg_alea, n_min=C.N_MIN_TIERS),
        "h2": C.rappel_vague2(y1, y2),
    }
    controles.append({"controle": "niveaux de census_division",
                      "valeur": float(len(niveaux_div)), "reference": 9.0,
                      "detail": ", ".join(niveaux_div)})
    controles.append({"controle": "cases du segment ideologie x genre x age",
                      "valeur": float(len(niveaux_fin)), "reference": 98.0, "detail": ""})
    controles.append({"controle": "groupes de la partition aleatoire placebo",
                      "valeur": float(len(niveaux_alea)),
                      "reference": float(C.N_GROUPES_PLACEBO), "detail": ""})

    per = C.perimetres(paquet)
    lignes_par_per = {"1052": per["1052"], "150": per["150"]}
    prep = {}
    for nom_per, lignes in lignes_par_per.items():
        for seuil in C.SEUILS:
            prep[(nom_per, seuil)] = preparer(paquet, lignes, seuil, refs)

    # -------------------------------------------- controles de protocole
    for nom_per, nom, cible in (("1052", "agents composite", 0.3069),
                                ("1052", "B1 argmax", 0.0580),
                                ("1052", "B3 foret", 0.0144),
                                ("150", "C3", 0.2195),
                                ("150", "C2", 0.1285)):
        p = prep[(nom_per, 0.10)]
        m = C.masques(paquet["M"][nom][p["lignes"]], p["y1"], p["mods"])
        v = m["juste"].sum() / max(p["rare_vrai"].sum(), 1)
        controles.append({"controle": f"rappel global {nom}, perimetre {nom_per}",
                          "valeur": float(v), "reference": cible, "detail": "a29, a34"})
        print(f"controle rappel {nom} {nom_per} : {v:.4f} contre {cible}")

    p = prep[("1052", 0.10)]
    for cle, nom_part in (("stabilite", None),):
        cov = (p["stab"][p["rare_vrai"]] >= 0).mean()
        controles.append({"controle": "couverture vague 2 sur cellules minoritaires, 1052",
                          "valeur": float(cov), "reference": 1.0, "detail": ""})
    for cle, nom in (("d_div", "P_B division"), ("d_alea", "P_C aleatoire")):
        cov = (~np.isnan(refs[cle][p["lignes"]][p["rare_vrai"]])).mean()
        controles.append({"controle": f"couverture du score {nom}, 1052",
                          "valeur": float(cov), "reference": 1.0, "detail": ""})

    # Controle arithmetique declare : ou tombent les raretes osees par B1 sur P_B ?
    for nom_part in ("P_B division de recensement", "P_C partition aleatoire"):
        mB1 = C.masques(paquet["M"]["B1 argmax"][p["lignes"]], p["y1"], p["mods"])
        tp = terciles_predits(paquet["M"]["B1 argmax"][p["lignes"]], p, nom_part, refs,
                              paquet)
        tot = mB1["rare_pred"].sum()
        for k in range(3):
            part = (mB1["rare_pred"] & (tp == k)).sum() / max(tot, 1)
            controles.append({
                "controle": f"part des raretes osees par B1 dans {C.TERCILES[k]}, {nom_part}",
                "valeur": float(part), "reference": 0.3333, "detail": f"{int(tot)} raretes osees"})

    # -------------------------------------------- mesures
    idx_boot = {nom_per: C.tirages_bootstrap(len(lignes), args.tirages, rng)
                for nom_per, lignes in lignes_par_per.items()}

    conditions_par_per = {
        "1052": [c for c in C.ORDRE if c in paquet["M"] and c not in ("C2", "C3")],
        "150": [c for c in C.ORDRE if c in paquet["M"]],
    }

    lignes_pa, lignes_tierces, cache = [], [], {}
    for (nom_per, seuil), p in prep.items():
        ib = idx_boot[nom_per]
        avec_ic = (seuil == 0.10)
        for nom in conditions_par_per[nom_per]:
            pred = paquet["M"][nom][p["lignes"]]
            m = C.masques(pred, p["y1"], p["mods"])

            # ---- P_A, la stabilite en vague 2
            for etiquette, sel in (("rarete stable", p["stab"] == 1),
                                   ("rarete instable", p["stab"] == 0),
                                   ("ensemble", np.ones_like(p["stab"], dtype=bool))):
                r = C.mesure_sur(p["rare_vrai"] & sel, m["rare_pred"] & sel,
                                 m["juste"], p["planchers"])
                cache[(nom_per, seuil, nom, "P_A", etiquette)] = r
                ligne = {"perimetre": nom_per, "seuil": seuil, "condition": nom,
                         "classe": etiquette, "cellules_minoritaires": r["cellules"],
                         "raretes_osees": r["raretes_osees"],
                         "rappel": r["rappel"], "precision": r["precision"], "f1": r["f1"]}
                if avec_ic:
                    _, lo, hi, _ = C.valeur_ic_p(r["_rappel"], ib)
                    ligne["rappel_ic_bas"], ligne["rappel_ic_haut"] = lo, hi
                    _, lo, hi, _ = C.valeur_ic_p(r["_precision"], ib)
                    ligne["precision_ic_bas"], ligne["precision_ic_haut"] = lo, hi
                for pl in C.PLANCHERS:
                    ligne[f"plancher_{pl}"] = r[f"plancher_{pl}"]
                    ligne[f"exces_{pl}"] = r[f"exces_{pl}"]
                    if avec_ic:
                        _, lo, hi, pp = C.valeur_ic_p(r[f"_exces_{pl}"], ib)
                        ligne[f"exces_{pl}_ic_bas"] = lo
                        ligne[f"exces_{pl}_ic_haut"] = hi
                        ligne[f"exces_{pl}_p"] = pp
                lignes_pa.append(ligne)

            # ---- P_B et P_C, les deux partitions par frequence dans un segment tiers
            for nom_part in ("P_B division de recensement", "P_C partition aleatoire"):
                tv = p["tvrai"][nom_part]
                tp = terciles_predits(pred, p, nom_part, refs, paquet)
                for k in list(range(3)) + [-9]:
                    et = "ensemble" if k == -9 else C.TERCILES[k]
                    selv = p["rare_vrai"] if k == -9 else (p["rare_vrai"] & (tv == k))
                    selp = m["rare_pred"] if k == -9 else (m["rare_pred"] & (tp == k))
                    r = C.mesure_sur(selv, selp, m["juste"], p["planchers"])
                    cache[(nom_per, seuil, nom, nom_part, et)] = r
                    ligne = {"perimetre": nom_per, "seuil": seuil, "partition": nom_part,
                             "tercile": et, "condition": nom,
                             "cellules_minoritaires": r["cellules"],
                             "raretes_osees": r["raretes_osees"], "rappel": r["rappel"],
                             "precision": r["precision"], "f1": r["f1"]}
                    for pl in C.PLANCHERS:
                        ligne[f"plancher_{pl}"] = r[f"plancher_{pl}"]
                        ligne[f"exces_{pl}"] = r[f"exces_{pl}"]
                    if avec_ic:
                        _, lo, hi, _ = C.valeur_ic_p(r["_rappel"], ib)
                        ligne["rappel_ic_bas"], ligne["rappel_ic_haut"] = lo, hi
                        _, lo, hi, pp = C.valeur_ic_p(r["_exces_segment"], ib)
                        ligne["exces_segment_ic_bas"] = lo
                        ligne["exces_segment_ic_haut"] = hi
                        ligne["exces_segment_p"] = pp
                    lignes_tierces.append(ligne)
        print(f"  mesures {nom_per}, seuil {seuil:.2f} terminees", flush=True)

    tab_pa = pd.DataFrame(lignes_pa)
    tab_tierces = pd.DataFrame(lignes_tierces)

    # -------------------------------------------- description des partitions
    desc = []
    for (nom_per, seuil), p in prep.items():
        for etiquette, sel in (("rarete stable", p["stab"] == 1),
                               ("rarete instable", p["stab"] == 0),
                               ("hors partition, vague 2 absente", p["stab"] == -1),
                               ("ensemble", np.ones_like(p["stab"], dtype=bool))):
            s = p["rare_vrai"] & sel
            desc.append({"perimetre": nom_per, "seuil": seuil, "partition": "P_A stabilite",
                         "classe": etiquette, "borne_basse": np.nan, "borne_haute": np.nan,
                         "cellules_minoritaires": int(s.sum()),
                         "items_distincts": int(s.any(axis=0).sum()),
                         "plancher_item": _moy(p["planchers"]["item"][s]),
                         "plancher_segment": _moy(p["planchers"]["segment"][s]),
                         "plancher_humains_vague_2": _moy(p["planchers"]["humains vague 2"][s]),
                         "support_median": float(np.nanmedian(p["support"][s]))
                         if s.sum() else np.nan})
        for nom_part in ("P_B division de recensement", "P_C partition aleatoire"):
            b1, b2 = p["bornes"][nom_part]
            tv = p["tvrai"][nom_part]
            for k in list(range(3)) + [-9]:
                et = "ensemble" if k == -9 else C.TERCILES[k]
                s = p["rare_vrai"] if k == -9 else (p["rare_vrai"] & (tv == k))
                desc.append({"perimetre": nom_per, "seuil": seuil, "partition": nom_part,
                             "classe": et, "borne_basse": b1, "borne_haute": b2,
                             "cellules_minoritaires": int(s.sum()),
                             "items_distincts": int(s.any(axis=0).sum()),
                             "plancher_item": _moy(p["planchers"]["item"][s]),
                             "plancher_segment": _moy(p["planchers"]["segment"][s]),
                             "plancher_humains_vague_2": _moy(
                                 p["planchers"]["humains vague 2"][s]),
                             "support_median": float(np.nanmedian(p["support"][s]))
                             if s.sum() else np.nan})
    tab_desc = pd.DataFrame(desc)

    # -------------------------------------------- controle de Rennard
    ren = []
    for nom_per, lignes in lignes_par_per.items():
        p = prep[(nom_per, 0.10)]
        ib = idx_boot[nom_per]
        mB1 = C.masques(paquet["M"]["B1 argmax"][p["lignes"]], p["y1"], p["mods"])
        for nom in conditions_par_per[nom_per]:
            pred = paquet["M"][nom][p["lignes"]]
            m = C.masques(pred, p["y1"], p["mods"])
            for n_min in C.SUPPORTS_RENNARD:
                sel = (p["stab"] == 1) & (p["support"] >= n_min)
                selv = p["rare_vrai"] & sel
                selp = m["rare_pred"] & sel
                r = C.mesure_sur(selv, selp, m["juste"], p["planchers"])
                rb = C.mesure_sur(selv, mB1["rare_pred"] & sel, mB1["juste"],
                                  p["planchers"])
                cache[(nom_per, "rennard", nom, n_min, "stable")] = r
                cache[(nom_per, "rennard", "B1 argmax", n_min, "stable")] = rb
                o, lo, hi, pp = C.contraste(*r["_rappel"], *rb["_rappel"], ib)
                ligne = {"perimetre": nom_per, "condition": nom, "support_minimal": n_min,
                         "cellules_minoritaires": r["cellules"], "rappel": r["rappel"],
                         "plancher_segment": r["plancher_segment"],
                         "exces_segment": r["exces_segment"],
                         "avantage_sur_B1": o, "avantage_ic_bas": lo,
                         "avantage_ic_haut": hi, "avantage_p": pp}
                _, lo, hi, pp = C.valeur_ic_p(r["_exces_segment"], ib)
                ligne["exces_segment_ic_bas"] = lo
                ligne["exces_segment_ic_haut"] = hi
                ligne["exces_segment_p"] = pp
                ren.append(ligne)
    tab_ren = pd.DataFrame(ren)

    # -------------------------------------------- contrastes declares
    contr = []

    def ajouter(famille, hypothese, nom, nom_per, comparaison, o, lo, hi, pp):
        contr.append({"famille": famille, "hypothese": hypothese, "condition": nom,
                      "perimetre": nom_per, "comparaison": comparaison, "difference": o,
                      "ic_bas": lo, "ic_haut": hi, "p_bootstrap": pp})

    # H1 : avantage sur B1 argmax, raretes STABLES
    for nom in testees:
        nom_per = C.PERIMETRE_NATUREL[nom]
        ib = idx_boot[nom_per]
        a = cache[(nom_per, 0.10, nom, "P_A", "rarete stable")]["_rappel"]
        b = cache[(nom_per, 0.10, C.COMPARATEUR, "P_A", "rarete stable")]["_rappel"]
        ajouter("primaire", "H1 avantage sur B1 argmax, raretes stables", nom, nom_per,
                f"{nom} contre {C.COMPARATEUR}, raretes stables",
                *C.contraste(*a, *b, ib))

    # H2 : exces sur le plancher de segment, raretes STABLES, les 13 plus B1
    for nom in testees + [C.COMPARATEUR]:
        nom_per = C.PERIMETRE_NATUREL.get(nom, "1052")
        ib = idx_boot[nom_per]
        a = cache[(nom_per, 0.10, nom, "P_A", "rarete stable")]["_exces_segment"]
        ajouter("primaire", "H2 exces sur plancher de segment, raretes stables", nom,
                nom_per, "exces contre zero, raretes stables", *C.valeur_ic_p(a, ib))

    # H3 : avantage sur STABLES moins avantage sur INSTABLES
    for nom in testees:
        nom_per = C.PERIMETRE_NATUREL[nom]
        ib = idx_boot[nom_per]
        a1 = cache[(nom_per, 0.10, nom, "P_A", "rarete stable")]["_rappel"]
        b1 = cache[(nom_per, 0.10, C.COMPARATEUR, "P_A", "rarete stable")]["_rappel"]
        a0 = cache[(nom_per, 0.10, nom, "P_A", "rarete instable")]["_rappel"]
        b0 = cache[(nom_per, 0.10, C.COMPARATEUR, "P_A", "rarete instable")]["_rappel"]
        ajouter("secondaire", "H3 avantage stables moins avantage instables", nom, nom_per,
                f"({nom} moins {C.COMPARATEUR}) stables moins instables",
                *C.difference_de_differences(a1, b1, a0, b0, ib))

    # H4 : gradient de l'exces sur plancher entre T3 et T1 de P_B
    for nom in testees + [C.COMPARATEUR]:
        nom_per = C.PERIMETRE_NATUREL.get(nom, "1052")
        ib = idx_boot[nom_per]
        part = "P_B division de recensement"
        a = cache[(nom_per, 0.10, nom, part, C.TERCILES[2])]["_exces_segment"]
        b = cache[(nom_per, 0.10, nom, part, C.TERCILES[0])]["_exces_segment"]
        ajouter("secondaire", "H4 gradient de l'exces sur plancher, T3 moins T1 de P_B",
                nom, nom_per, "T3 deductible contre T1 non deductible",
                *C.contraste(*a, *b, ib))

    # H5 : H1 apres retrait des modalites portees par moins de 20 personnes
    for nom in testees:
        nom_per = C.PERIMETRE_NATUREL[nom]
        ib = idx_boot[nom_per]
        a = cache[(nom_per, "rennard", nom, C.SUPPORT_TESTE, "stable")]["_rappel"]
        b = cache[(nom_per, "rennard", "B1 argmax", C.SUPPORT_TESTE, "stable")]["_rappel"]
        ajouter("tertiaire",
                f"H5 avantage sur B1, raretes stables, support >= {C.SUPPORT_TESTE}",
                nom, nom_per, f"{nom} contre {C.COMPARATEUR}, support >= {C.SUPPORT_TESTE}",
                *C.contraste(*a, *b, ib))

    ct = pd.DataFrame(contr)
    for fam in ("primaire", "secondaire", "tertiaire"):
        idx = ct.famille == fam
        if not idx.any():
            continue
        ct.loc[idx, "p_holm"] = C.holm(ct.loc[idx, "p_bootstrap"].values)
        ct.loc[idx, "p_bh"] = C.benjamini_hochberg(ct.loc[idx, "p_bootstrap"].values)
        ct.loc[idx, "tests_dans_la_famille"] = int(idx.sum())

    # -------------------------------------------- ecriture
    C.ecrire(tab_desc, "a42-partitions.csv")
    C.ecrire(tab_pa, "a42-stabilite.csv")
    C.ecrire(tab_tierces, "a42-partitions-tierces.csv")
    C.ecrire(ct, "a42-contrastes.csv")
    C.ecrire(tab_ren, "a42-rennard.csv")
    C.ecrire(pd.DataFrame(controles), "a42-controles.csv")

    # -------------------------------------------- affichage
    pd.set_option("display.width", 260)
    ordre = {c: i for i, c in enumerate(C.ORDRE)}
    for nom_per in ("1052", "150"):
        s = tab_pa[(tab_pa.perimetre == nom_per) & (tab_pa.seuil == 0.10)].copy()
        s["o"] = s.condition.map(ordre)
        print("\n" + "=" * 130)
        print(f"P_A stabilite en vague 2, perimetre {nom_per}, seuil 10 %")
        print("=" * 130)
        print(s.sort_values(["o", "classe"])[
            ["condition", "classe", "cellules_minoritaires", "rappel", "precision", "f1",
             "plancher_item", "plancher_segment", "exces_segment"]].round(4)
            .to_string(index=False))

    for nom_part in ("P_B division de recensement", "P_C partition aleatoire"):
        s = tab_tierces[(tab_tierces.perimetre == "1052") & (tab_tierces.seuil == 0.10)
                        & (tab_tierces.partition == nom_part)].copy()
        s["o"] = s.condition.map(ordre)
        piv = s.pivot_table(index=["o", "condition"], columns="tercile", values="rappel")
        print("\n" + "=" * 130)
        print(f"RAPPEL par tercile, {nom_part}, perimetre 1 052, seuil 10 %")
        print("=" * 130)
        print(piv.sort_index().round(4).to_string())

    print("\n" + "=" * 130)
    print("Contrastes declares et corrections pour tests multiples")
    print("=" * 130)
    c2 = ct.copy()
    c2["o"] = c2.condition.map(ordre)
    print(c2.sort_values(["famille", "hypothese", "o"])[
        ["famille", "hypothese", "condition", "perimetre", "difference", "ic_bas",
         "ic_haut", "p_bootstrap", "p_holm", "p_bh"]].round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Controle de Rennard, raretes stables")
    print("=" * 130)
    s = tab_ren[tab_ren.perimetre == "1052"].copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values(["o", "support_minimal"])[
        ["condition", "support_minimal", "cellules_minoritaires", "rappel",
         "plancher_segment", "exces_segment", "avantage_sur_B1", "avantage_ic_bas",
         "avantage_ic_haut"]].round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Controles de protocole")
    print("=" * 130)
    print(pd.DataFrame(controles).round(4).to_string(index=False))


if __name__ == "__main__":
    main()
