"""
c7_compromis_bits : le cout en bits par point d'exactitude varie par famille ; le cout en
bits par unite de fidelite individuelle est-il, lui, a peu pres constant ?

===========================================================================
PREENREGISTREMENT : resultats/c7-compromis-bits-preenregistrement.md, ecrit le
12 septembre 2026, AVANT ce fichier et avant tout calcul.

Concilie trois mesures deja publiees : le rho de c7_compromis.py (0,958, LLM et
statistiques confondus) ; le cout en bits par point d'exactitude de c7_bits.py (0,29-0,47
pour les jumeaux LLM, 0,068 pour B2, facteur 4-7) ; les generateurs statistiques de
c7_generateur, plafonnes a 0,476 d'exactitude, qui ne fuient qu'a 0,22-0,25 %.

AUCUN BIT N'EST RECALCULE ICI : resultats/c7-bits.csv est lu tel quel (colonnes `bits`,
`gain_pp`, `ratio_bits_par_pp`). La seule quantite nouvelle est le ratio 2, bits /
part_du_plancher_humain (t1-classement.csv, deja utilisee par c7_compromis.py), et la
comparaison de dispersion des deux ratios.

Aucun appel de modele de langage. Lecture seule sur resultats/. Aucun script existant
modifie.
Usage : .venv/bin/python analyses/c7_compromis_bits.py
===========================================================================
"""

import os
import sys

import numpy as np
import pandas as pd
from scipy import stats

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

sys.path.insert(0, os.path.join(RACINE, "analyses"))
import c7_reidentification as C7   # noqa: E402  (juste pour la liste des 8 configurations)

STATISTIQUES = ["B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]
NOMS_12 = C7.CONFIGURATIONS + STATISTIQUES
HUMAIN_BITS = "retest humain v1-3"
HUMAIN_FID = "humains vagues 1-3 (retest)"


def cv(x):
    x = np.asarray(x, dtype=float)
    x = x[~np.isnan(x)]
    return float(np.std(x, ddof=1) / np.mean(x)) if len(x) > 1 else np.nan


def main():
    print(__doc__.split("=" * 75)[1], flush=True)

    bits = pd.read_csv(os.path.join(SORTIE, "c7-bits.csv"))
    bits_twin = bits[bits.jeu == "Twin-2K-500"].set_index("predicteur")

    classement = pd.read_csv(os.path.join(SORTIE, "t1-classement.csv"))
    classement = classement[classement.segmentation == "S_gra"].set_index("condition")

    lignes = []
    for nom in NOMS_12 + [HUMAIN_FID]:
        cle_bits = HUMAIN_BITS if nom == HUMAIN_FID else nom
        b = bits_twin.loc[cle_bits]
        fid = float(classement.loc[nom, "part_du_plancher_humain"])
        gain_pp = float(b["gain_pp"])
        ratio1 = float(b["bits"]) / gain_pp if gain_pp > 0 else np.nan
        ratio2 = float(b["bits"]) / fid if abs(fid) > 1e-6 else np.nan
        lignes.append({
            "predicteur": nom,
            "groupe": ("humain" if nom == HUMAIN_FID else
                       "statistique" if nom in STATISTIQUES else "LLM"),
            "bits": float(b["bits"]), "gain_pp": gain_pp, "fidelite_plancher": fid,
            "ratio1_bits_par_pp": ratio1, "ratio2_bits_par_fidelite": ratio2,
        })
    df = pd.DataFrame(lignes)
    print(df.to_string(index=False), flush=True)

    df12 = df[df.predicteur != HUMAIN_FID]

    cv1 = cv(df12.ratio1_bits_par_pp)
    cv2 = cv(df12.ratio2_bits_par_fidelite)
    n1 = df12.ratio1_bits_par_pp.notna().sum()
    n2 = df12.ratio2_bits_par_fidelite.notna().sum()
    print(f"\nCV ratio1 (bits/point d'exactitude), n={n1} definis : {cv1:.4f}", flush=True)
    print(f"CV ratio2 (bits/fidelite), n={n2} definis : {cv2:.4f}", flush=True)
    print(f"facteur CV1/CV2 = {cv1 / cv2:.2f}", flush=True)

    # variante sans B0 tirage (ratio2 instable, denominateur proche de 0)
    sans_b0 = df12[df12.predicteur != "B0 tirage"]
    cv2_sans_b0 = cv(sans_b0.ratio2_bits_par_fidelite)
    print(f"CV ratio2 sans B0 tirage (denominateur quasi nul) : {cv2_sans_b0:.4f}, "
          f"facteur CV1/CV2 = {cv1 / cv2_sans_b0:.2f}", flush=True)

    # regression bits ~ fidelite sur les 12 + le retest humain, ordonnee a l'origine
    pente, ordonnee, r, p, err_pente = stats.linregress(df.fidelite_plancher, df.bits)
    print(f"\nRegression bits ~ fidelite (12 + retest humain) : pente={pente:.4f}, "
          f"ordonnee_origine={ordonnee:.4f}, r={r:.4f}, p={p:.4g}", flush=True)

    pente12, ordonnee12, r12, p12, _ = stats.linregress(
        df12.fidelite_plancher, df12.bits)
    print(f"Meme regression, 12 points seuls (sans le retest humain) : pente={pente12:.4f}, "
          f"ordonnee_origine={ordonnee12:.4f}, r={r12:.4f}", flush=True)

    df.to_csv(os.path.join(SORTIE, "c7-compromis-bits.csv"), index=False)
    print("\necrit : resultats/c7-compromis-bits.csv", flush=True)


if __name__ == "__main__":
    main()
