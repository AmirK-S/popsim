"""a19 : effet de l'item `income` sur les baselines de a2 (objection 2.2 de a17).

Deux variantes, aucune modification des scripts existants, memes graines :

  A. protocole de a2 inchange (149 items cibles), score restreint aux 148 items
     hors `income` : isole l'effet de denominateur.
  B. protocole rejoue sur 148 items, `income` retire de la cible ET du contexte
     de B2 : isole l'effet complet.

Les conditions d'agents sont recalculees sur les memes jeux d'items.

Usage : .venv/bin/python analyses/a19_income.py
"""
import csv
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a2_baselines_gss as A2
from a2_commun import exactitude_par_personne, bootstrap_personnes

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")


def scores(pred, y, colonnes):
    acc = exactitude_par_personne(pred[:, colonnes], y[:, colonnes])
    return bootstrap_personnes(acc)


def main():
    ids, items, y1, y2, x, attributs = A2.charger()
    n, m = y1.shape
    j_inc = items.index("income")
    print(f"{n} personnes, {m} items cibles de a2, `income` en position {j_inc}")
    print(f"`income` est un attribut donne a B1 : {'income' in attributs}")

    hors = np.array([j for j in range(m) if j != j_inc])
    tous = np.arange(m)

    lignes = [["variante", "n_items", "methode", "exactitude", "ic_bas", "ic_haut"]]

    # --- variante A : predictions de a2, score sur 149 puis 148 items ------
    print("\nvariante A : protocole de a2 (149 items), score restreint")
    plis, blocs = A2.grille(n, m)
    pred = A2.evaluer(items, y1, x, plis, blocs)
    for nom in ["B1 argmax", "B2 argmax", "B0 mode"]:
        for lib, col in [("A 149 items", tous), ("A 148 items (score seul)", hors)]:
            moy, bas, haut = scores(pred[nom], y1, col)
            print(f"  {lib:<28}{nom:<12}{moy:.4f} [{bas:.4f} ; {haut:.4f}]")
            lignes.append([lib, len(col), nom, f"{moy:.4f}", f"{bas:.4f}", f"{haut:.4f}"])
    # retest humain, meme traitement
    for lib, col in [("A 149 items", tous), ("A 148 items (score seul)", hors)]:
        moy, bas, haut = scores(y2, y1, col)
        print(f"  {lib:<28}{'retest humain':<12}{moy:.4f} [{bas:.4f} ; {haut:.4f}]")
        lignes.append([lib, len(col), "retest humain", f"{moy:.4f}", f"{bas:.4f}", f"{haut:.4f}"])
    # conditions d'agents
    for libelle, fichier in A2.CONDITIONS_LLM.items():
        chemin = os.path.join(A2.PREP, fichier)
        if not os.path.exists(chemin):
            continue
        p = pd.read_csv(chemin)[items].values.astype(object)
        for lib, col in [("A 149 items", tous), ("A 148 items (score seul)", hors)]:
            moy, bas, haut = scores(p, y1, col)
            lignes.append([lib, len(col), libelle, f"{moy:.4f}", f"{bas:.4f}", f"{haut:.4f}"])
            if lib.startswith("A 148"):
                print(f"  {lib:<28}{libelle:<28}{moy:.4f}")

    # --- variante B : protocole rejoue sur 148 items ----------------------
    print("\nvariante B : protocole rejoue sur 148 items, income hors cible et hors contexte")
    items_b = [q for q in items if q != "income"]
    y1b = y1[:, hors]
    mb = len(items_b)
    plis_b, blocs_b = A2.grille(n, mb)
    pred_b = A2.evaluer(items_b, y1b, x, plis_b, blocs_b)
    colb = np.arange(mb)
    for nom in ["B1 argmax", "B2 argmax", "B0 mode"]:
        moy, bas, haut = scores(pred_b[nom], y1b, colb)
        print(f"  B 148 items (rejoue)  {nom:<12}{moy:.4f} [{bas:.4f} ; {haut:.4f}]")
        lignes.append(["B 148 items (rejoue)", mb, nom, f"{moy:.4f}", f"{bas:.4f}", f"{haut:.4f}"])

    with open(os.path.join(SORTIE, "a19-income-baselines.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes)
    print("\necrit : resultats/a19-income-baselines.csv")


if __name__ == "__main__":
    main()
