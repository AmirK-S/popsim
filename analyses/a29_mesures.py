"""
a29_mesures : les minorites gardees sont elles les bonnes personnes ?

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a2_commun, a8_commun, a25_commun et
a28_commun sont importes tels quels, memes graines, memes plis, memes 149 items, memes
personnes que a2, a8, a23, a25 et a28.

La phrase a defendre, arretee dans ARBITRAGE.md, dit : "les methodes classiques simulent
une societe sans minorites ; les modeles de langage en gardent la moitie, mais pas les
bonnes personnes". Le debut de la phrase est etabli par a8 section 6 et par a28 section
3.4. Ce script teste la FIN de la phrase, et separe trois choses que le rappel seul
confond :

  1. garder la MASSE minoritaire au niveau de la population, item par item ;
  2. attribuer cette masse aux BONNES PERSONNES, mesure par la correlation par personne
     entre le taux de reponses rares reelles et le taux de reponses rares predites ;
  3. attribuer, a la bonne personne, la BONNE minorite, mesure par la precision et par la
     decomposition des erreurs de minorite en deux : minorite predite a une personne
     majoritaire sur l'item, et minorite predite a une personne minoritaire mais pas la
     bonne modalite.

Une methode peut garder la masse minoritaire en la mettant aux mauvais endroits. C'est
exactement ce que B0 tirage fait par construction, et c'est pour cela qu'il sert de
temoin negatif dans tous les tableaux : il reproduit 100 pour cent de la masse humaine
sans savoir quoi que ce soit de qui que ce soit.

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT LES RESULTATS
===========================================================================
Perimetre declare : le perimetre naturel de chaque methode, soit les 1 052 personnes pour
les onze methodes qui les couvrent, et les 150 personnes du run local pour C2 et C3, avec
la reference de minorite calculee sur ces 150 personnes. Seuil declare : 10 pour cent.

  H1  primaire, precision. Pour chacune des 13 methodes non humaines, la precision sur
      les cellules minoritaires est INFERIEURE a celle des memes humains reinterroges.
      13 tests, bootstrap apparie sur les personnes.
  H2  primaire, bonnes personnes. Pour chacune des 13 methodes, la correlation par
      personne entre taux de rares reelles et taux de rares predites est INFERIEURE a
      celle des memes humains reinterroges, qui donnent le plafond. 13 tests.

  Famille primaire declaree : H1 union H2, soit 26 tests.
  Correction principale : Holm sur les 26. Elle controle le taux d'erreur par famille
  sans hypothese sur la dependance, ce qui est necessaire : les 26 contrastes portent sur
  les memes personnes et les memes items.
  Correction secondaire rapportee a cote : Benjamini Hochberg sur les 26.

  H3  secondaire. Pour chacune des 13 methodes, la correlation par personne est
      STRICTEMENT POSITIVE, c'est a dire que la methode ne distribue pas la rarete au
      hasard entre les gens. 13 tests.
  H4  secondaire. Pour chacune des 13 methodes, le rappel minoritaire sur les 12 items
      juges sensibles au mode par NORC DIFFERE de celui des 65 items temoins. 13 tests,
      bilateral.

  Famille secondaire declaree : H3 union H4, soit 26 tests, corrigee separement par Holm
  et par Benjamini Hochberg.

  N'ENTRENT PAS dans les familles, et sont rapportes comme des descriptions : le seuil de
  20 pour cent, qui est une robustesse ; le perimetre 150 pour les onze methodes qui
  disposent du perimetre 1 052, qui est un echantillon emboite et non un test
  independant ; le F1, le taux de fausses minorites et la masse predite, qui se deduisent
  des quantites testees ; la correlation par item entre masse humaine et masse predite ;
  le contraste de groupe entre les huit conditions a modele de langage et les cinq
  predicteurs statistiques, ajoute apres coup et signale comme tel ; toute la question des
  profils, traitee par a29_profils.py, qui est descriptive de bout en bout.
===========================================================================

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl, cache de matrices de a25 et cache de
          la foret aleatoire de a28.
Sortie  : resultats/a29-minorites-global.csv, a29-correlation-personne.csv,
          a29-par-item.csv, a29-masse-item.csv, a29-items-sensibles.csv,
          a29-contrastes.csv.

Usage :
  .venv/bin/python analyses/a29_mesures.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 2000 --permutations 200
"""

import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a29_commun as C
from a8_commun import modalites_minoritaires


def table_globale(paquet, lignes, methodes, mods, idx_boot):
    """Rappel, precision, F1 et taux de fausses minorites, une ligne par methode."""
    verite = paquet["y1"][lignes]
    out, comptes = [], {}
    for nom in methodes:
        pred = paquet["M"][nom][lignes]
        c = C.compter(pred, verite, mods)
        comptes[nom] = c
        a = C.agreger(c)
        ic, _ = C.bootstrap_agregats(c, idx_boot)
        out.append({
            "condition": nom,
            "cellules": int(c["n_eval"].sum()),
            "cellules_minoritaires": int(c["n_rare_vrai"].sum()),
            "cellules_predites_minoritaires": int(c["n_rare_pred"].sum()),
            "minorites_justes": int(c["n_juste"].sum()),
            "minorites_a_personne_majoritaire": int(c["n_faux_maj"].sum()),
            "minorites_mauvaise_modalite": int(c["n_faux_min"].sum()),
            "taux_refus": float(c["n_refus"].sum() / max(c["n_eval"].sum(), 1)),
            **a, **ic})
    return pd.DataFrame(out), comptes


def table_correlation(comptes, methodes, idx_boot, permutations, rng):
    out, vecteurs = [], {}
    for nom in methodes:
        d, u, v, tir = C.correlation_personne(comptes[nom], idx_boot, permutations, rng)
        vecteurs[nom] = (u, v)
        out.append({"condition": nom, **d,
                    "personnes": int((~np.isnan(u) & ~np.isnan(v)).sum()),
                    "taux_rares_reelles_moyen": float(np.nanmean(u)),
                    "taux_rares_predites_moyen": float(np.nanmean(v))})
    return pd.DataFrame(out), vecteurs


def table_par_item(paquet, lignes, methodes, mods, seuil):
    """Masse minoritaire humaine et predite item par item, plus le rappel par item."""
    items = paquet["items"]
    verite = paquet["y1"][lignes]
    ok = C.observe(verite)
    rare_vrai = C.appartient(verite, mods) & ok
    cl = C.classes_norc(items)
    out = []
    for nom in methodes:
        pred = paquet["M"][nom][lignes]
        dispo = C.observe(pred)
        rare_pred = C.appartient(pred, mods) & ok & dispo
        juste = rare_pred & (pred == verite)
        for j, it in enumerate(items):
            n = int(ok[:, j].sum())
            if n == 0:
                continue
            rv = int(rare_vrai[:, j].sum())
            out.append({
                "condition": nom, "item": it, "classe_norc": cl[it], "seuil": seuil,
                "n": n,
                "masse_humaine": rv / n,
                "masse_predite": int(rare_pred[:, j].sum()) / n,
                "cellules_minoritaires": rv,
                "minorites_justes": int(juste[:, j].sum()),
                "cellules_predites_minoritaires": int(rare_pred[:, j].sum()),
                "rappel_item": (int(juste[:, j].sum()) / rv) if rv else np.nan,
            })
    return pd.DataFrame(out)


def table_sensibles(paquet, comptes, methodes, idx_boot):
    """Rappel et precision sur les 12 items sensibles de NORC contre les 65 temoins."""
    items = paquet["items"]
    col = {cl: C.colonnes_classe(items, cl) for cl in ("sensible", "temoin")}
    out, restreints = [], {}
    for nom in methodes:
        restreints[nom] = {}
        for cl, cols in col.items():
            c = C.restreindre(comptes[nom], cols)
            restreints[nom][cl] = c
            a = C.agreger(c)
            ic, _ = C.bootstrap_agregats(c, idx_boot)
            out.append({"condition": nom, "classe_norc": cl, "n_items": len(cols),
                        "cellules": int(c["n_eval"].sum()),
                        "cellules_minoritaires": int(c["n_rare_vrai"].sum()),
                        **a, **ic})
    return pd.DataFrame(out), restreints


def bootstrap_items_sensibles(items_t, nom_per, methodes, tirages, rng):
    """Contraste sensibles contre temoins, ITEMS reechantillonnes dans chaque classe.

    Hors famille declaree, robustesse. Le contraste de H4 oppose deux ensembles d'items
    differents, l'un de 12 items et l'autre de 65 : son incertitude porte donc aussi sur
    le tirage des items, que le bootstrap sur les personnes ne voit pas. Le rappel groupe
    est recalcule a chaque tirage a partir des comptes par item, ce qui garde la
    ponderation par le nombre de cellules minoritaires.
    """
    d = items_t[(items_t.perimetre == nom_per) & (items_t.seuil == 0.10)]
    out = []
    for nom in methodes:
        g = d[d.condition == nom]
        parts = {}
        for cl in ("sensible", "temoin"):
            h = g[g.classe_norc == cl]
            parts[cl] = (h.minorites_justes.values.astype(float),
                         h.cellules_minoritaires.values.astype(float))

        def rappel(cl, idx=None):
            j, r = parts[cl]
            if idx is not None:
                j, r = j[idx], r[idx]
            return j.sum() / r.sum() if r.sum() > 0 else np.nan

        obs = rappel("sensible") - rappel("temoin")
        tir = np.empty(tirages)
        for t in range(tirages):
            ia = rng.integers(0, len(parts["sensible"][0]), len(parts["sensible"][0]))
            ib = rng.integers(0, len(parts["temoin"][0]), len(parts["temoin"][0]))
            tir[t] = rappel("sensible", ia) - rappel("temoin", ib)
        tir = tir[~np.isnan(tir)]
        p = (2.0 * min((tir <= 0).mean(), (tir >= 0).mean())
             if len(tir) else 1.0)
        out.append({"perimetre": nom_per, "condition": nom, "difference": obs,
                    "ic_items_bas": float(np.percentile(tir, 2.5)) if len(tir) else np.nan,
                    "ic_items_haut": float(np.percentile(tir, 97.5)) if len(tir) else np.nan,
                    "p_bootstrap_items": float(min(max(p, 1.0 / max(len(tir), 1)), 1.0))})
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--tirages", type=int, default=2000)
    ap.add_argument("--permutations", type=int, default=200)
    ap.add_argument("--graine", type=int, default=C.GRAINE)
    args = ap.parse_args()

    t0 = time.time()
    print(__doc__.split("=" * 75)[1])
    paquet = C.charger(args.cache, args.cache_foret)
    rng = np.random.default_rng(args.graine)
    per = C.perimetres(paquet)
    print(f"{len(paquet['ids'])} personnes, {len(paquet['items'])} items, "
          f"{len(paquet['M'])} conditions", flush=True)

    globales, correlations, par_item, sensibles = [], [], [], []
    comptes_tout, vecteurs_tout, restreints_tout, idx_tout = {}, {}, {}, {}

    for nom_per, lignes in per.items():
        methodes = C.methodes_du_perimetre(paquet, nom_per)
        idx_boot = C.tirages_bootstrap(len(lignes), args.tirages, rng)
        idx_tout[nom_per] = idx_boot
        verite = paquet["y1"][lignes]
        for seuil in C.SEUILS:
            mods = modalites_minoritaires(verite, seuil)
            g, comptes = table_globale(paquet, lignes, methodes, mods, idx_boot)
            g["perimetre"], g["seuil"] = nom_per, seuil
            globales.append(g)
            comptes_tout[(nom_per, seuil)] = comptes

            perm = args.permutations if seuil == 0.10 else 0
            k, vecteurs = table_correlation(comptes, methodes, idx_boot, perm, rng)
            k["perimetre"], k["seuil"] = nom_per, seuil
            correlations.append(k)
            vecteurs_tout[(nom_per, seuil)] = vecteurs

            d = table_par_item(paquet, lignes, methodes, mods, seuil)
            d["perimetre"] = nom_per
            par_item.append(d)

            if seuil == 0.10:
                s, restreints = table_sensibles(paquet, comptes, methodes, idx_boot)
                s["perimetre"] = nom_per
                sensibles.append(s)
                restreints_tout[nom_per] = restreints
            print(f"  perimetre {nom_per}, seuil {seuil:.2f} : fait "
                  f"({time.time() - t0:.0f} s)", flush=True)

    glob = pd.concat(globales, ignore_index=True)
    corr = pd.concat(correlations, ignore_index=True)
    items_t = pd.concat(par_item, ignore_index=True)
    sens = pd.concat(sensibles, ignore_index=True)
    plafond = sens[sens.condition == "humains vague 2"].set_index(
        ["perimetre", "classe_norc"])["rappel"]
    sens["rappel_humain_de_la_classe"] = [
        plafond.get((r.perimetre, r.classe_norc), np.nan) for r in sens.itertuples()]
    sens["rappel_normalise"] = sens.rappel / sens.rappel_humain_de_la_classe

    # ----------------------------------------------------------------- contrastes
    contrastes = []
    for nom in C.PERIMETRE_NATUREL:
        nom_per = C.PERIMETRE_NATUREL[nom]
        idx_boot = idx_tout[nom_per]
        ca = comptes_tout[(nom_per, 0.10)][nom]
        ch = comptes_tout[(nom_per, 0.10)]["humains vague 2"]
        o, b, h, p = C.contraste_agregat(ca, ch, "precision", idx_boot)
        contrastes.append({"hypothese": "H1 precision contre humains", "condition": nom,
                           "perimetre": nom_per, "difference": o, "ic_bas": b,
                           "ic_haut": h, "p_bootstrap": p})
        o, b, h, p = C.contraste_correlations(ca, ch, idx_boot)
        contrastes.append({"hypothese": "H2 correlation contre humains", "condition": nom,
                           "perimetre": nom_per, "difference": o, "ic_bas": b,
                           "ic_haut": h, "p_bootstrap": p})

        u, v = vecteurs_tout[(nom_per, 0.10)][nom]
        tir = np.array([C.spearman(u[i], v[i]) for i in idx_boot])
        r = C.spearman(u, v)
        contrastes.append({"hypothese": "H3 correlation contre zero", "condition": nom,
                           "perimetre": nom_per, "difference": r,
                           "ic_bas": float(np.nanpercentile(tir, 2.5)),
                           "ic_haut": float(np.nanpercentile(tir, 97.5)),
                           "p_bootstrap": C.p_contre_zero(tir)})

        rs = restreints_tout[nom_per][nom]
        o, b, h, p = C.contraste_agregat(rs["sensible"], rs["temoin"], "rappel", idx_boot)
        contrastes.append({"hypothese": "H4 rappel sensibles contre temoins",
                           "condition": nom, "perimetre": nom_per, "difference": o,
                           "ic_bas": b, "ic_haut": h, "p_bootstrap": p})

    ct = pd.DataFrame(contrastes)
    ct["p_holm"] = np.nan
    ct["p_bh"] = np.nan
    for libelle, familles in (("primaire", ["H1 precision contre humains",
                                            "H2 correlation contre humains"]),
                              ("secondaire", ["H3 correlation contre zero",
                                              "H4 rappel sensibles contre temoins"])):
        idx = ct[ct.hypothese.isin(familles)].index
        ct.loc[idx, "p_holm"] = C.holm(ct.loc[idx, "p_bootstrap"].values)
        ct.loc[idx, "p_bh"] = C.benjamini_hochberg(ct.loc[idx, "p_bootstrap"].values)
        ct.loc[idx, "famille"] = libelle

    # contraste de groupe, POST HOC, hors famille : les huit conditions a modele de
    # langage contre les cinq predicteurs statistiques, sur la correlation par personne
    post = []
    for nom_per in ("1052", "150"):
        k = corr[(corr.perimetre == nom_per) & (corr.seuil == 0.10)]
        a = k[k.condition.isin(C.LLM)]["rho_spearman"].values
        b = k[k.condition.isin(C.STAT)]["rho_spearman"].values
        obs, p = C28_permutation(a, b, 20000, np.random.default_rng(args.graine))
        post.append({"perimetre": nom_per, "mesure": "correlation par personne",
                     "moyenne_langage": float(np.nanmean(a)),
                     "moyenne_statistique": float(np.nanmean(b)),
                     "difference": obs, "p_permutation": p,
                     "n_langage": len(a), "n_statistique": len(b)})
    # contraste de groupe sur H4, POST HOC lui aussi
    for nom_per in ("1052", "150"):
        d = ct[(ct.hypothese == "H4 rappel sensibles contre temoins")
               & (ct.perimetre == nom_per)]
        a = d[d.condition.isin(C.LLM)]["difference"].values
        b = d[d.condition.isin(C.STAT)]["difference"].values
        if len(a) < 2 or len(b) < 2:
            continue
        obs, p = C28_permutation(a, b, 20000, np.random.default_rng(args.graine))
        post.append({"perimetre": nom_per,
                     "mesure": "rappel sensibles moins temoins",
                     "moyenne_langage": float(np.nanmean(a)),
                     "moyenne_statistique": float(np.nanmean(b)),
                     "difference": obs, "p_permutation": p,
                     "n_langage": len(a), "n_statistique": len(b)})
    pg = pd.DataFrame(post)

    # robustesse : le meme contraste avec les ITEMS reechantillonnes
    rob = pd.concat([bootstrap_items_sensibles(
        items_t, nom_per, C.methodes_du_perimetre(paquet, nom_per), args.tirages,
        np.random.default_rng(args.graine + 1)) for nom_per in ("1052", "150")],
        ignore_index=True)

    # ----------------------------------------------------------- masse par item
    masse = []
    for (nom_per, seuil), _ in comptes_tout.items():
        d = items_t[(items_t.perimetre == nom_per) & (items_t.seuil == seuil)]
        for nom, g in d.groupby("condition"):
            ok = g.cellules_minoritaires > 0
            masse.append({
                "condition": nom, "perimetre": nom_per, "seuil": seuil,
                "items": int(len(g)),
                "rho_masse_item": C.spearman(g.masse_humaine.values, g.masse_predite.values),
                "r_masse_item": C.pearson(g.masse_humaine.values, g.masse_predite.values),
                "rapport_masse_moyen": float(g.masse_predite.sum() / g.masse_humaine.sum())
                if g.masse_humaine.sum() > 0 else np.nan,
                "items_masse_predite_nulle": int((g.masse_predite == 0).sum()),
                "items_a_minorite": int(ok.sum()),
            })
    ms = pd.DataFrame(masse)

    C.ecrire(glob, "a29-minorites-global.csv")
    C.ecrire(corr, "a29-correlation-personne.csv")
    C.ecrire(items_t, "a29-par-item.csv")
    C.ecrire(ms, "a29-masse-item.csv")
    C.ecrire(sens, "a29-items-sensibles.csv")
    C.ecrire(ct, "a29-contrastes.csv")
    C.ecrire(pg, "a29-contraste-de-groupe.csv")
    C.ecrire(rob, "a29-sensibles-bootstrap-items.csv")

    # ---------------------------------------------------------------- affichage
    pd.set_option("display.width", 250)
    ordre = {c: i for i, c in enumerate(C.ORDRE_METHODES)}
    for nom_per in ("1052", "150"):
        print("\n" + "=" * 140)
        print(f"Rappel, precision et fausses minorites, perimetre {nom_per}, seuil 10 %")
        print("=" * 140)
        s = glob[(glob.perimetre == nom_per) & (glob.seuil == 0.10)].copy()
        s["o"] = s.condition.map(ordre)
        print(s.sort_values("o")[
            ["condition", "cellules_minoritaires", "rappel", "precision", "f1",
             "taux_fausses_minorites", "taux_mauvaise_minorite", "masse_predite",
             "masse_humaine", "taux_refus"]].round(4).to_string(index=False))

    for nom_per in ("1052", "150"):
        print("\n" + "=" * 140)
        print(f"Correlation par personne, rares reelles contre rares predites, "
              f"perimetre {nom_per}, seuil 10 %")
        print("=" * 140)
        s = corr[(corr.perimetre == nom_per) & (corr.seuil == 0.10)].copy()
        s["o"] = s.condition.map(ordre)
        cols = ["condition", "rho_spearman", "ic_bas", "ic_haut", "r_pearson",
                "taux_rares_reelles_moyen", "taux_rares_predites_moyen"]
        if "temoin_permutation" in s.columns:
            cols += ["temoin_permutation", "temoin_p975"]
        print(s.sort_values("o")[cols].round(4).to_string(index=False))

    print("\n" + "=" * 140)
    print("Contrastes et corrections pour tests multiples")
    print("=" * 140)
    ct2 = ct.copy()
    ct2["o"] = ct2.condition.map(ordre)
    print(ct2.sort_values(["hypothese", "o"])[
        ["hypothese", "condition", "perimetre", "difference", "ic_bas", "ic_haut",
         "p_bootstrap", "p_holm", "p_bh"]].round(4).to_string(index=False))

    print("\n" + "=" * 140)
    print("Items sensibles au mode contre temoins, seuil 10 %")
    print("=" * 140)
    s = sens.copy()
    s["o"] = s.condition.map(ordre)
    piv = s.pivot_table(index=["perimetre", "condition"], columns="classe_norc",
                        values=["rappel", "precision", "masse_predite"])
    print(piv.round(4).to_string())

    print("\n" + "=" * 140)
    print("Robustesse H4 : memes contrastes, ITEMS reechantillonnes, hors famille")
    print("=" * 140)
    r2 = rob.copy()
    r2["o"] = r2.condition.map(ordre)
    print(r2.sort_values(["perimetre", "o"]).drop(columns="o").round(4).to_string(index=False))

    print("\n" + "=" * 140)
    print("Contraste de groupe, POST HOC, hors famille declaree")
    print("=" * 140)
    print(pg.round(4).to_string(index=False))

    print(f"\nduree {time.time() - t0:.0f} s")


def C28_permutation(a, b, tirages, rng):
    """Permutation des etiquettes de methode, reprise de a28_commun.permutation."""
    import a28_commun as C28
    return C28.permutation(a, b, tirages, rng)


if __name__ == "__main__":
    main()
