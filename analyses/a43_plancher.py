"""
a43_plancher : contraste NON PREENREGISTRE contre le plancher de bruit du demoyennage.

Motif, ecrit apres coup et declare comme tel. Retirer la MEME moyenne estimee des deux
cotes, humain et methode, injecte le bruit d'estimation de cette moyenne dans les deux
termes de la correlation, donc gonfle la correlation residuelle d'une quantite qui croit
quand la cellule qui sert a estimer la moyenne retrecit. Sur la moyenne d'item, estimee
sur environ mille repondants, c'est negligeable. Sur la moyenne de segment, estimee sur
une cinquantaine, ce ne l'est plus.

`B0 mode` donne la mesure directe de ce plancher : il predit une modalite constante par
item, il ne sait donc rien de la personne ni du segment, et tout ce qu'il obtient apres
retrait de la moyenne de segment est du bruit de demoyennage. Ce script teste chaque
methode contre lui, sur les MEMES tirages bootstrap, ce qui rend le contraste apparie.

Il ne recalcule rien : il relit les 2 000 tirages ecrits par a43_r2_demoyenne.py dans
/tmp/a43-tirages-r2.npy.

Statut : script d'analyse jetable, aucun appel de modele de langage. Aucun script existant
n'est modifie.

Sortie  : resultats/a43-plancher.csv.

Usage : .venv/bin/python analyses/a43_plancher.py
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a43_commun as C

VARIANTES = ["moyenne d'item", "moyenne d'item et de segment 18",
             "moyenne d'item et de segment 42"]
TEMOIN = "B0 mode"


def main():
    tir = np.load("/tmp/a43-tirages-r2.npy", allow_pickle=True).item()
    lignes = []
    for variante in VARIANTES:
        for perimetre in ("1052", "150"):
            ref = tir.get((perimetre, TEMOIN, variante))
            if ref is None:
                continue
            paires = [(c, v) for (p, c, v) in tir
                      if p == perimetre and v == variante and c != TEMOIN]
            ps, brut = [], []
            for cond, _ in paires:
                d = tir[(perimetre, cond, variante)] - ref
                b, h = C.ic(d)
                p = C.p_bilateral(d)
                ps.append(p)
                brut.append({"variante": variante, "perimetre": perimetre,
                             "condition": cond,
                             "plancher_r_temoin": float(np.nanmean(ref)),
                             "ecart_de_correlation": float(np.nanmean(d)),
                             "ic_bas": b, "ic_haut": h, "p": p})
            ph, pb = C.holm(np.array(ps)), C.benjamini_hochberg(np.array(ps))
            for k, ligne in enumerate(brut):
                ligne["p_holm"], ligne["p_bh"] = ph[k], pb[k]
                lignes.append(ligne)
    df = pd.DataFrame(lignes)
    C.ecrire(df, "a43-plancher.csv")
    for variante in VARIANTES:
        print(f"### {variante}")
        s = df[df["variante"] == variante]
        print(s[["perimetre", "condition", "plancher_r_temoin", "ecart_de_correlation",
                 "ic_bas", "ic_haut", "p_holm"]].to_string(index=False))
        print()


if __name__ == "__main__":
    main()
