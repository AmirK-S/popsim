"""
a38_ampleurs : le score continu d'ampleur de mode par item, et sa couverture.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a2_baselines_gss, a25_commun, a28_commun et
a38_commun sont importes tels quels.

Ce script repond a la premiere question du cahier des charges de a38 : apparier les
ampleurs publiees par NORC et par l'atlas NBER aux 149 items de a2, et dire combien en ont
une et combien n'en ont pas. Il ne calcule aucun ecart agent contre humain.

Entree  : data/norc-mode/*.csv, produits par a38_extraire_norc.py.
Sortie  : resultats/a38-ampleurs-items.csv, resultats/a38-couverture.csv.

Usage :
  .venv/bin/python analyses/a38_ampleurs.py
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
import a38_commun as A38
from a2_baselines_gss import charger
from a25_commun import classe_norc


def main():
    ids, items, y1, y2, x, attributs = charger()
    classes = {it: classe_norc(it)[0] for it in items}

    ampleurs = A38.charger_ampleurs()
    inconnus = sorted(set(ampleurs.item) - set(items))
    if inconnus:
        print(f"ampleurs sans item correspondant, ignorees : {inconnus}")
    scores = A38.score_ampleur(ampleurs, items)

    lignes = []
    for it in items:
        s = scores[it]
        mesures = ampleurs[ampleurs.item == it]
        lignes.append({
            "item": it,
            "classe_norc": classes[it],
            "classe_comportement": A38.classe_comportement(it),
            "m1_mode": s["m1"], "m2_mode_plus_conception": s["m2"],
            "m3_toutes_sources": s["m3"],
            "rapport_retenu": s["rapport"], "famille_retenue": s["famille"],
            "n_mesures_disponibles": s["n_mesures"],
            "pole_endogroupe": (A38.POLE_ENDOGROUPE[it][0]
                                if it in A38.POLE_ENDOGROUPE else ""),
            "niveau_pole_endogroupe": (A38.POLE_ENDOGROUPE[it][1]
                                       if it in A38.POLE_ENDOGROUPE else ""),
            "source_pole_endogroupe": (A38.POLE_ENDOGROUPE[it][2]
                                       if it in A38.POLE_ENDOGROUPE else ""),
            "sources_ampleur": " ; ".join(
                f"{r.rapport} = {r.ampleur_points} points ({r.famille})"
                for _, r in mesures.iterrows()),
            "detail_ampleur": " ; ".join(str(r.detail) for _, r in mesures.iterrows()),
        })
    t = pd.DataFrame(lignes)
    A38.ecrire(t, "a38-ampleurs-items.csv")

    # ------------------------------------------------------------- couverture
    couv = []
    for nom, col in [("M1 ampleur de mode stricte", "m1_mode"),
                     ("M2 mode plus conception", "m2_mode_plus_conception"),
                     ("M3 toutes sources", "m3_toutes_sources")]:
        for cl in ["sensible", "investiguer", "temoin", "mixte", "non teste", "tous"]:
            sous = t if cl == "tous" else t[t.classe_norc == cl]
            couv.append({
                "score": nom, "classe_norc": cl, "items": len(sous),
                "avec_ampleur": int(sous[col].notna().sum()),
                "sans_ampleur": int(sous[col].isna().sum()),
                "mediane_ampleur": float(sous[col].median()) if sous[col].notna().any()
                                   else np.nan,
                "min_ampleur": float(sous[col].min()) if sous[col].notna().any() else np.nan,
                "max_ampleur": float(sous[col].max()) if sous[col].notna().any() else np.nan,
            })
    for nom, col in [("M1 ampleur de mode stricte", "m1_mode"),
                     ("M3 toutes sources", "m3_toutes_sources")]:
        for cl in ["comportement", "attitude", "auto evaluation"]:
            sous = t[t.classe_comportement == cl]
            couv.append({
                "score": nom, "classe_norc": f"[{cl}]", "items": len(sous),
                "avec_ampleur": int(sous[col].notna().sum()),
                "sans_ampleur": int(sous[col].isna().sum()),
                "mediane_ampleur": float(sous[col].median()) if sous[col].notna().any()
                                   else np.nan,
                "min_ampleur": float(sous[col].min()) if sous[col].notna().any() else np.nan,
                "max_ampleur": float(sous[col].max()) if sous[col].notna().any() else np.nan,
            })
    c = pd.DataFrame(couv)
    A38.ecrire(c, "a38-couverture.csv")

    pd.set_option("display.width", 200)
    print("\n" + "=" * 100)
    print("Couverture du score d'ampleur, 149 items")
    print("=" * 100)
    print(c.to_string(index=False))

    print("\n" + "=" * 100)
    print("Les 12 items sensibles de NORC, ampleur mesuree")
    print("=" * 100)
    s = t[t.classe_norc == "sensible"][
        ["item", "m1_mode", "m3_toutes_sources", "rapport_retenu", "famille_retenue",
         "classe_comportement"]]
    print(s.to_string(index=False))

    print("\n" + "=" * 100)
    print("Ampleurs par rapport")
    print("=" * 100)
    print(ampleurs.groupby(["rapport", "famille"]).agg(
        items=("item", "size"), mediane=("ampleur_points", "median"),
        mini=("ampleur_points", "min"), maxi=("ampleur_points", "max")).to_string())

    dedans, dehors = A38.items_camp(items)
    print(f"\npole d'endogroupe declare pour {len(dedans)} items sur {len(items)} ; "
          f"{len(dehors)} exclus faute de source.")


if __name__ == "__main__":
    main()
