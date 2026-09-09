"""
a43_polarite : robustesse NON PREENREGISTREE de la decomposition d'Ahn a l'orientation
des echelles.

Motif, ecrit apres coup et declare comme tel. La decomposition de a43_r2_demoyenne donne
un effet principal de personne tres faible. Or cet effet mesure la tendance d'une personne
a repondre haut sur le rang normalise, et le rang normalise suit l'ordre des modalites du
fichier de Stanford, qui n'a aucune raison de pointer dans le meme sens d'un item a
l'autre. Un jeu d'items dont les echelles pointent au hasard a un effet principal de
personne mecaniquement ecrase et une interaction personne x item mecaniquement gonflee.
Ce script mesure de combien.

Protocole, choisi pour eviter la circularite : les personnes sont coupees en deux moities
de graine fixe ; l'orientation de chaque item est estimee sur la MOITIE A, vague 1 seule,
par le signe de la correlation entre l'item et la moyenne des AUTRES items de la personne ;
la decomposition a deux occasions est ensuite refaite sur la MOITIE B avec ces
orientations. Les deux moities sont ensuite echangees et les deux resultats publies.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie.

Sortie  : resultats/a43-polarite.csv.

Usage :
  .venv/bin/python analyses/a43_polarite.py
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a43_commun as C


def orientations(H, lignes):
    """Signe de chaque item, estime sur les lignes fournies, vague 1 seule.

    Pour chaque item, la correlation entre sa valeur et la moyenne des AUTRES items de la
    meme personne. Le "autres items" evite qu'un item soit correle a lui meme par le biais
    de la moyenne. Un item de correlation nulle ou indefinie garde le signe positif.
    """
    A = H[lignes]
    ok = ~np.isnan(A)
    V = np.where(ok, np.nan_to_num(A), 0.0)
    s_tot = V.sum(axis=1, keepdims=True)
    n_tot = ok.sum(axis=1, keepdims=True).astype(float)
    signes = np.ones(A.shape[1])
    for j in range(A.shape[1]):
        autre_n = n_tot[:, 0] - ok[:, j]
        autre_s = s_tot[:, 0] - V[:, j]
        with np.errstate(invalid="ignore", divide="ignore"):
            moy = np.where(autre_n > 5, autre_s / np.maximum(autre_n, 1), np.nan)
        m = ok[:, j] & ~np.isnan(moy)
        if m.sum() < 30:
            continue
        u, v = A[m, j], moy[m]
        if u.std() == 0 or v.std() == 0:
            continue
        r = float(np.corrcoef(u, v)[0, 1])
        if r < 0:
            signes[j] = -1.0
    return signes


def appliquer(H, signes):
    """Retourne l'echelle des items de signe negatif : v devient 1 - v."""
    return np.where(signes[None, :] > 0, H, 1.0 - H)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    args = ap.parse_args()

    paquet = C.charger(args.cache, args.cache_foret, args.cache_a35)
    ords, colonnes, rangs, H = C.preparer_valeurs(paquet)
    H2 = C.scores_methode(paquet, "humains vague 2", colonnes, rangs)

    n = H.shape[0]
    rng = np.random.default_rng(C.GRAINE)
    perm = rng.permutation(n)
    moities = {"A": perm[: n // 2], "B": perm[n // 2:]}

    out = []
    d = C.decomposition(H, H2)
    d.update({"orientation": "aucune, ordre du fichier", "estimee_sur": "",
              "decomposee_sur": "les 1 052", "n_items_retournes": 0})
    out.append(d)
    for estim, evalu in (("A", "B"), ("B", "A")):
        s = orientations(H, moities[estim])
        d = C.decomposition(appliquer(H, s)[moities[evalu]],
                            appliquer(H2, s)[moities[evalu]])
        d.update({"orientation": "alignee sur la moyenne des autres items",
                  "estimee_sur": f"moitie {estim}", "decomposee_sur": f"moitie {evalu}",
                  "n_items_retournes": int((s < 0).sum())})
        out.append(d)
        d = C.decomposition(H[moities[evalu]], H2[moities[evalu]])
        d.update({"orientation": "aucune, ordre du fichier", "estimee_sur": "",
                  "decomposee_sur": f"moitie {evalu}", "n_items_retournes": 0})
        out.append(d)

    df = pd.DataFrame(out)
    C.ecrire(df, "a43-polarite.csv")
    print(df[["orientation", "estimee_sur", "decomposee_sur", "n_items_retournes",
              "part_personne", "part_item", "part_interaction", "part_transitoire",
              "rapport_interaction_personne"]].to_string(index=False))


if __name__ == "__main__":
    main()
