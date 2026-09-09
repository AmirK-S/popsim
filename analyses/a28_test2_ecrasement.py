"""
a28_test2_ecrasement : test decisif de l'idee de rang 2, "la simulation efface ce qui
n'est pas deductible de l'etiquette". Reponse mesuree a l'adversaire Ku 2026.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a1_double_distorsion n'est pas importe, ses
deux estimateurs sont recopies dans a28_commun en version item par item, avec la meme
correction de biais.

L'objection de Ku 2026, corpus/01 : une foret aleatoire supervisee ecrase la dispersion
autant qu'un modele de langage, rapport de 0,72 contre 0,67 a 0,85, donc l'ecrasement est
une propriete de la tache de prediction et non du langage. Le present script ne conteste
pas l'amplitude, il conteste la FORME.

  Ecrasement uniforme : le rapport de dispersion intra groupe est le meme sur tous les
  items, a l'erreur pres. C'est ce qu'une methode statistique doit produire, puisqu'elle
  applique le meme retrecissement partout.
  Ecrasement selectif : le rapport est plus bas sur les items ou l'etiquette explique le
  moins la reponse chez les humains. C'est ce que la these predit du modele de langage :
  il restitue ce qui se deduit de l'etiquette et efface le reste.

Deux quantites par methode :
  1. la correlation de rang entre le rapport de dispersion intra par item et la part de
     variance humaine expliquee par la segmentation, avec intervalle bootstrap sur les
     items. Prediction de la these : positive pour les modeles de langage, nulle pour les
     predicteurs statistiques.
  2. la dispersion du rapport intra entre items : ecart type, ecart interquartile et
     coefficient de variation. Prediction de la these : faible pour les predicteurs
     statistiques, forte pour les modeles de langage.

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT LES RESULTATS
===========================================================================
  H5  Pour chacune des 13 methodes non humaines, la correlation de rang entre le rapport
      de dispersion intra par item et la part expliquee humaine par item est positive.
      Segmentation principale : le profil croise genre x race x bloc d'ideologie de a1.
      Mesure de dispersion : indice de Gini Simpson, estimateur sans biais.
      Perimetre 1 052 pour les onze methodes qui le permettent, perimetre 150 pour les
      treize, C2 et C3 comprises. Le test declare porte sur le perimetre 150, qui est le
      seul ou toutes les methodes coexistent. 13 tests.
  H6  Pour chacune des 13 methodes non humaines, l'ecart type du rapport intra entre
      items est plus grand chez les huit conditions a modele de langage que chez les cinq
      predicteurs statistiques. Ce n'est pas un test par methode mais un contraste entre
      deux groupes de methodes : 1 test, par permutation des etiquettes de methode.

  Famille declaree : H5 union H6, soit 14 tests. Correction principale : Holm.
  Correction secondaire rapportee a cote : Benjamini Hochberg.
  N'entrent PAS dans la famille : les axes de segmentation autres que le profil croise,
  la mesure d'entropie, et le perimetre 1 052, tous rapportes comme des controles.
===========================================================================

Une methode est nouvelle et une seule : la foret aleatoire sur demographies, "B3 foret",
definie dans a28_commun. C'est l'adversaire nomme par Ku 2026, replante chez nous avec le
protocole de a2, memes plis et memes graines.

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl.
Sortie  : resultats/a28-t2-dispersion-item.csv, a28-t2-selectivite.csv,
          a28-t2-uniformite.csv.

Usage :
  .venv/bin/python analyses/a28_test2_ecrasement.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 20000
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C

# Un item dont la dispersion intra humaine est presque nulle produit un rapport instable
# qui dominerait toutes les moyennes. Le seuil est descriptif, il porte sur les humains
# seuls, et le nombre d'items ecartes est rapporte.
SEUIL_DISPERSION_HUMAINE = 0.05


def dispersions(paquet, lignes, conditions, axe, n_min=30):
    """Dispersion intra et inter par item, pour les humains et pour chaque methode."""
    items, options = paquet["items"], paquet["options"]
    seg_tous, _ = C.segments(paquet["x"], paquet["attributs"])
    seg = seg_tous[axe][lignes]
    k = {it: len(options[it]) for it in items}

    codes_h = C.coder(paquet["y1"], lignes, items, options)
    ref = {}
    for j, it in enumerate(items):
        ref[it] = C.dispersion_item(codes_h[:, j], seg, k[it], n_min)

    out = []
    for cond in conditions:
        codes = C.coder(paquet["M"][cond], lignes, items, options)
        for j, it in enumerate(items):
            d = C.dispersion_item(codes[:, j], seg, k[it], n_min)
            h = ref[it]
            valide = (not np.isnan(h["gs_intra"])
                      and h["gs_intra"] >= SEUIL_DISPERSION_HUMAINE)
            out.append({
                "axe": axe, "condition": cond, "item": it,
                "n_cellules": d["n"],
                "gs_intra_humain": h["gs_intra"], "gs_total_humain": h["gs_total"],
                "part_expliquee_humaine": (h["gs_inter"] / h["gs_total"]
                                           if h["gs_total"] and h["gs_total"] > 1e-9
                                           else np.nan),
                "nmi_humaine": (h["h_inter"] / h["h_total"]
                                if h["h_total"] and h["h_total"] > 1e-9 else np.nan),
                "gs_intra_methode": d["gs_intra"],
                "ratio_intra": (d["gs_intra"] / h["gs_intra"]
                                if valide and d["gs_intra"] is not None else np.nan),
                "item_retenu": bool(valide),
            })
    return pd.DataFrame(out)


def dispersions_demi_echantillon(paquet, lignes, conditions, axe, rng, n_min=20):
    """Controle contre l'artefact de denominateur partage.

    Le probleme. La part expliquee humaine vaut 1 - D_intra(humain) / D_total(humain), et
    le rapport intra vaut D_intra(methode) / D_intra(humain). Les deux quantites portent
    donc le MEME D_intra(humain), l'une au numerateur d'une soustraction et l'autre au
    denominateur. Toute erreur d'echantillonnage sur ce terme cree une correlation
    positive entre les deux, sans qu'aucune methode n'ait rien fait de selectif. C'est
    exactement le motif qui fait grimper `B0 tirage` a 0,56 : cette baseline reproduit la
    dispersion TOTALE, donc son rapport vaut mecaniquement 1 / (1 - part expliquee).

    Le controle. Les personnes sont coupees en deux moities tirees une fois pour toutes.
    La part expliquee est estimee sur la moitie A, le rapport intra sur la moitie B. Les
    deux estimations ne partagent plus aucune cellule, et la correlation residuelle est
    alors une correlation entre items et non un artefact de bruit commun.
    """
    items, options = paquet["items"], paquet["options"]
    seg_tous, _ = C.segments(paquet["x"], paquet["attributs"])
    k = {it: len(options[it]) for it in items}
    ordre = rng.permutation(len(lignes))
    a_idx, b_idx = lignes[ordre[::2]], lignes[ordre[1::2]]

    seg_a, seg_b = seg_tous[axe][a_idx], seg_tous[axe][b_idx]
    ch_a = C.coder(paquet["y1"], a_idx, items, options)
    ch_b = C.coder(paquet["y1"], b_idx, items, options)
    ref_a, ref_b = {}, {}
    for j, it in enumerate(items):
        ref_a[it] = C.dispersion_item(ch_a[:, j], seg_a, k[it], n_min)
        ref_b[it] = C.dispersion_item(ch_b[:, j], seg_b, k[it], n_min)

    out = []
    for cond in conditions:
        codes = C.coder(paquet["M"][cond], b_idx, items, options)
        for j, it in enumerate(items):
            d = C.dispersion_item(codes[:, j], seg_b, k[it], n_min)
            ha, hb = ref_a[it], ref_b[it]
            valide = (not np.isnan(hb["gs_intra"])
                      and hb["gs_intra"] >= SEUIL_DISPERSION_HUMAINE
                      and not np.isnan(ha["gs_total"]) and ha["gs_total"] > 1e-9)
            out.append({
                "axe": axe, "condition": cond, "item": it,
                "part_expliquee_moitie_a": (ha["gs_inter"] / ha["gs_total"]
                                            if valide else np.nan),
                "ratio_intra_moitie_b": (d["gs_intra"] / hb["gs_intra"]
                                         if valide else np.nan),
                "item_retenu": bool(valide),
            })
    return pd.DataFrame(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--tirages", type=int, default=20000)
    ap.add_argument("--graine", type=int, default=20260908)
    args = ap.parse_args()

    paquet = C.charger_tout(args.cache, args.cache_foret)
    rng = np.random.default_rng(args.graine)
    print(__doc__.split("=" * 75)[1])

    toutes = [c for c in C.ORDRE_METHODES if c in paquet["M"]]
    perimetres = {"150": paquet["lignes150"],
                  "1052": np.arange(len(paquet["ids"]))}

    tables = []
    for nom_per, lignes in perimetres.items():
        conds = toutes if nom_per == "150" else [c for c in toutes
                                                 if c not in ("C2", "C3")]
        for axe in C.AXES:
            d = dispersions(paquet, lignes, conds, axe)
            d["perimetre"] = nom_per
            tables.append(d)
        print(f"  perimetre {nom_per} : fait", flush=True)
    disp = pd.concat(tables, ignore_index=True)
    C.ecrire(disp, "a28-t2-dispersion-item.csv")

    n_ret = disp[(disp.perimetre == "150") & (disp.axe == "profil croise")
                 & (disp.condition == "B1 argmax")].item_retenu.sum()
    n_tot = disp[(disp.perimetre == "150") & (disp.axe == "profil croise")
                 & (disp.condition == "B1 argmax")].shape[0]
    print(f"\nitems retenus sur le perimetre 150, profil croise : {n_ret} sur {n_tot} "
          f"(dispersion intra humaine au moins {SEUIL_DISPERSION_HUMAINE})")

    # ------------------------------------------------------- H5, la selectivite
    lignes_s = []
    for (nom_per, axe, cond), d in disp.groupby(["perimetre", "axe", "condition"]):
        d = d[d.item_retenu]
        for nom_x, col in [("part expliquee Gini Simpson", "part_expliquee_humaine"),
                           ("information mutuelle normalisee", "nmi_humaine")]:
            r, bas, haut, n = C.bootstrap_correlation(
                d[col].values, d["ratio_intra"].values, 2000, rng)
            # p bilateral par permutation des items
            u, v = d[col].values, d["ratio_intra"].values
            ok = ~np.isnan(u) & ~np.isnan(v)
            u, v = u[ok], v[ok]
            p = np.nan
            if len(u) >= 6:
                obs, _ = C.spearman(u, v)
                tir = np.array([C.spearman(u, rng.permutation(v))[0]
                                for _ in range(min(args.tirages, 10000))])
                p = ((np.abs(tir) >= abs(obs) - 1e-12).sum() + 1.0) / (len(tir) + 1.0)
            lignes_s.append({
                "perimetre": nom_per, "axe": axe, "condition": cond,
                "mesure_x": nom_x, "rho_spearman": r, "ic_items_bas": bas,
                "ic_items_haut": haut, "n_items": n, "p_permutation": p,
                "ratio_intra_median": float(np.nanmedian(d["ratio_intra"])),
                "ratio_intra_moyen": float(np.nanmean(d["ratio_intra"])),
            })
    select = pd.DataFrame(lignes_s)

    # correction sur la famille declaree : H5 sur le perimetre 150, profil croise,
    # part expliquee Gini Simpson, methodes non humaines
    masque = ((select.perimetre == "150") & (select.axe == "profil croise")
              & (select.mesure_x == "part expliquee Gini Simpson")
              & (select.condition != "humains vague 2") & select.p_permutation.notna())
    idx = select[masque].index
    select["p_holm"] = np.nan
    select["p_bh"] = np.nan
    select.loc[idx, "p_holm"] = C.holm(select.loc[idx, "p_permutation"].values)
    select.loc[idx, "p_bh"] = C.benjamini_hochberg(select.loc[idx, "p_permutation"].values)
    C.ecrire(select, "a28-t2-selectivite.csv")

    # ------------------------------------------------------- H6, l'uniformite
    lignes_u = []
    for (nom_per, axe, cond), d in disp.groupby(["perimetre", "axe", "condition"]):
        v = d.loc[d.item_retenu, "ratio_intra"].dropna().values
        if len(v) < 5:
            continue
        q1, q3 = np.percentile(v, [25, 75])
        lignes_u.append({
            "perimetre": nom_per, "axe": axe, "condition": cond, "n_items": len(v),
            "ratio_moyen": float(v.mean()), "ratio_median": float(np.median(v)),
            "ecart_type": float(v.std(ddof=1)), "iqr": float(q3 - q1),
            "coefficient_variation": float(v.std(ddof=1) / v.mean()) if v.mean() else np.nan,
            "q10": float(np.percentile(v, 10)), "q90": float(np.percentile(v, 90)),
        })
    unif = pd.DataFrame(lignes_u)

    # contraste declare : ecart type du rapport, huit conditions LLM contre cinq
    # predicteurs statistiques, perimetre 150, profil croise
    u = unif[(unif.perimetre == "150") & (unif.axe == "profil croise")]
    a = u[u.condition.isin(C.LLM)].ecart_type.values
    b = u[u.condition.isin(C.STAT)].ecart_type.values
    obs, p_h6 = C.permutation(a, b, args.tirages, rng)
    print(f"\nH6, ecart type du rapport intra, perimetre 150, profil croise :")
    print(f"  huit conditions a modele de langage : moyenne {a.mean():.4f}")
    print(f"  cinq predicteurs statistiques       : moyenne {b.mean():.4f}")
    print(f"  difference {obs:+.4f}, p de permutation {p_h6:.4f}")
    # Controle post hoc, non pre enregistre : l'ecart type du rapport depend du niveau du
    # rapport, et les methodes ne sont pas au meme niveau. Le meme contraste est donc
    # refait sur le coefficient de variation, qui est sans echelle. `B0 mode` y est une
    # aberration lisible, son rapport moyen valant 0,03.
    a_cv = u[u.condition.isin(C.LLM)].coefficient_variation.values
    b_cv = u[u.condition.isin(C.STAT)].coefficient_variation.values
    obs_cv, p_cv = C.permutation(a_cv, b_cv, args.tirages, rng)
    b_cv2 = u[u.condition.isin([c for c in C.STAT if c != "B0 mode"])]\
        .coefficient_variation.values
    obs_cv2, p_cv2 = C.permutation(a_cv, b_cv2, args.tirages, rng)
    print(f"  controle sans echelle, coefficient de variation : "
          f"LLM {a_cv.mean():.3f} contre stat {b_cv.mean():.3f}, "
          f"difference {obs_cv:+.3f}, p {p_cv:.4f}")
    print(f"  meme controle sans B0 mode : stat {b_cv2.mean():.3f}, "
          f"difference {obs_cv2:+.3f}, p {p_cv2:.4f}")

    unif["h6_difference_llm_moins_stat"] = np.nan
    unif["h6_p_permutation"] = np.nan
    unif["h6cv_difference"] = np.nan
    unif["h6cv_p"] = np.nan
    unif["h6cv_difference_sans_b0mode"] = np.nan
    unif["h6cv_p_sans_b0mode"] = np.nan
    m = (unif.perimetre == "150") & (unif.axe == "profil croise")
    unif.loc[m, "h6_difference_llm_moins_stat"] = obs
    unif.loc[m, "h6_p_permutation"] = p_h6
    unif.loc[m, "h6cv_difference"] = obs_cv
    unif.loc[m, "h6cv_p"] = p_cv
    unif.loc[m, "h6cv_difference_sans_b0mode"] = obs_cv2
    unif.loc[m, "h6cv_p_sans_b0mode"] = p_cv2
    C.ecrire(unif, "a28-t2-uniformite.csv")

    # ------------------------------------- controle du denominateur partage (demi echantillon)
    lignes_d = []
    for nom_per, lignes in perimetres.items():
        conds = toutes if nom_per == "150" else [c for c in toutes
                                                 if c not in ("C2", "C3")]
        dd = dispersions_demi_echantillon(
            paquet, lignes, conds, "profil croise",
            np.random.default_rng(args.graine))
        for cond, g in dd.groupby("condition"):
            g = g[g.item_retenu]
            r, bas, haut, n = C.bootstrap_correlation(
                g["part_expliquee_moitie_a"].values, g["ratio_intra_moitie_b"].values,
                2000, rng)
            lignes_d.append({"perimetre": nom_per, "condition": cond,
                             "rho_spearman": r, "ic_items_bas": bas,
                             "ic_items_haut": haut, "n_items": n})
    demi = pd.DataFrame(lignes_d)
    C.ecrire(demi, "a28-t2-demi-echantillon.csv")

    # ------------------------------------------------------------------ affichage
    pd.set_option("display.width", 240)
    for nom_per in ["150", "1052"]:
        print("\n" + "=" * 120)
        print(f"H5, perimetre {nom_per}, profil croise : rapport intra x part expliquee humaine")
        print("=" * 120)
        s = select[(select.perimetre == nom_per) & (select.axe == "profil croise")
                   & (select.mesure_x == "part expliquee Gini Simpson")].copy()
        s["ordre"] = s.condition.map({c: i for i, c in enumerate(C.ORDRE_METHODES)})
        print(s.sort_values("ordre")[
            ["condition", "ratio_intra_median", "rho_spearman", "ic_items_bas",
             "ic_items_haut", "n_items", "p_permutation", "p_holm", "p_bh"]]
            .to_string(index=False))

    print("\n" + "=" * 120)
    print("H6, perimetre 150, profil croise : uniformite de l'ecrasement")
    print("=" * 120)
    s = u.copy()
    s["ordre"] = s.condition.map({c: i for i, c in enumerate(C.ORDRE_METHODES)})
    print(s.sort_values("ordre")[
        ["condition", "n_items", "ratio_moyen", "ratio_median", "ecart_type", "iqr",
         "coefficient_variation", "q10", "q90"]].to_string(index=False))

    print("\n" + "=" * 120)
    print("Controle : la correlation par axe de segmentation, perimetre 150")
    print("=" * 120)
    piv = select[(select.perimetre == "150")
                 & (select.mesure_x == "part expliquee Gini Simpson")].pivot(
        index="condition", columns="axe", values="rho_spearman")
    print(piv.reindex([c for c in C.ORDRE_METHODES if c in piv.index]).round(3).to_string())


if __name__ == "__main__":
    main()
