"""
i3b_surface : le tableau de surface d'attaque. Pour chaque fabricant, le deplacement
maximal de l'ecart entre camps et de trois marginales, atteignable sans depasser le seuil
de detection, a taille de flux donnee. C'est le prix de l'invisibilite.

===========================================================================
PREENREGISTREMENT : resultats/i3b-preenregistrement.md, section 8, ecrit le 8 septembre
2026 a 21 h 05 CEST, AVANT ce script et avant tout calcul de resultat.

Ce script ne calcule aucune statistique nouvelle. Il lit en colonnes les fichiers ecrits
par i3b_abaque.py et croise deux quantites que personne ne publie ensemble : a quel taux un
fabricant devient visible, et de combien il a deja deplace la mesure a ce taux.

ENTREES  : resultats/i3b-abaque.csv, i3b-abaque-extrapolee.csv,
           i3b-courbes-consequence.csv, i3b-meta.json
SORTIE   : resultats/i3b-surface-attaque.csv

Usage : .venv/bin/python analyses/i3b_surface.py
===========================================================================
"""

import argparse
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import i3b_commun as J

QUANTITES = ["polarisation", "marginale1", "marginale2", "marginale3"]
PLAFOND = 0.50      # le plus haut taux mesure ; au dela on n'extrapole pas la consequence


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sortie", default=J.SORTIE)
    args = ap.parse_args()

    ab = pd.read_csv(os.path.join(args.sortie, "i3b-abaque.csv"))
    ex = pd.read_csv(os.path.join(args.sortie, "i3b-abaque-extrapolee.csv"))
    cons = pd.read_csv(os.path.join(args.sortie, "i3b-courbes-consequence.csv"))
    meta = json.load(open(os.path.join(args.sortie, "i3b-meta.json")))
    noms_marg = {f"marginale{m['rang']}": m["item"] for m in meta["marginales"]}

    lignes = []
    tailles = sorted(ab.taille.unique())
    for source in sorted(ab.source.unique()):
        for taille in tailles + [5000]:
            if taille == 5000:
                d = ex[(ex.source == source) & (ex.taille == 5000)]
                if not len(d) or not d.courbe_stable_en_N.any():
                    lignes.append({"source": source, "taille": taille,
                                   "tau_detection": np.nan,
                                   "statut": "exige une seconde population"})
                    continue
                dd = d[d.courbe_stable_en_N]
                tau = float(np.nanmin(dd.tau_etoile_holm3.values)) \
                    if np.isfinite(dd.tau_etoile_holm3.values).any() else np.nan
                meilleure = (dd.loc[dd.tau_etoile_holm3.idxmin(), "statistique"]
                             if np.isfinite(dd.tau_etoile_holm3.values).any() else "")
                statut = "[PROBABLE], extrapolation"
                taille_courbe = 1052
            else:
                d = ab[(ab.source == source) & (ab.taille == taille)]
                v = d.groupby("statistique").tau_etoile_holm3.first()
                if not np.isfinite(v.values).any():
                    tau, meilleure = np.nan, ""
                else:
                    tau = float(np.nanmin(v.values))
                    meilleure = str(v.idxmin())
                statut = "[MESURE]"
                taille_courbe = taille
            jamais = not np.isfinite(tau)
            tau_lu = PLAFOND if jamais else min(float(tau), PLAFOND)
            ligne = {"source": source,
                     "famille": d.famille.iloc[0] if len(d) else "",
                     "taille": taille,
                     "tau_detection": tau, "statistique_qui_detecte": meilleure,
                     "jamais_detecte_sous_100_pour_cent": bool(jamais),
                     "taux_lu": tau_lu, "statut": statut}
            for q in QUANTITES:
                c = cons[(cons.source == source) & (cons.quantite == q)
                         & (cons.taille == taille_courbe)]
                if not len(c):
                    ligne[f"{q}_ecart_max"] = np.nan
                    continue
                a, b = float(c.courbe_a.iloc[0]), float(c.courbe_b.iloc[0])
                base = float(c.valeur_humaine.iloc[0])
                ecart = a * tau_lu + b * tau_lu ** 2
                ligne[f"{q}_humain"] = base
                ligne[f"{q}_ecart_max"] = ecart
                ligne[f"{q}_facteur_max"] = (base + ecart) / base if base else np.nan
                ligne[f"{q}_pourcent_max"] = 100.0 * ecart / base if base else np.nan
            lignes.append(ligne)

    out = pd.DataFrame(lignes)
    out.attrs["marginales"] = noms_marg
    J.ecrire(out, "i3b-surface-attaque.csv")

    print("\n=== surface d'attaque, N = 1052 ===", flush=True)
    v = out[(out.taille == 1052)].sort_values("tau_detection")
    cols = ["source", "tau_detection", "statistique_qui_detecte",
            "polarisation_pourcent_max", "marginale1_ecart_max",
            "marginale2_ecart_max", "marginale3_ecart_max"]
    print(v[cols].round(4).to_string(index=False), flush=True)
    print("\nmarginales :", noms_marg, flush=True)


if __name__ == "__main__":
    main()
