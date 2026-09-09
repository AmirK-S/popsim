"""
t2_camps : volet 3 de T2. Le camp le moins varie est il celui qui bouge le moins, et ou
se recrutent les changeurs ?

Preenregistrement : resultats/t2-preenregistrement.md, section 5.

a30 etablit que la gauche est le camp le moins varie des trois sur les 149 items du GSS
transversal. Ce script demande si le camp le moins varie est aussi celui qui bouge le
moins, sur les panels. C'est une transposition : les camps de a30 sont mesures sur les
1 052 participants de l'echantillon transversal de Stanford, ceux d'ici sur les 4 683
personnes des panels. Ce ne sont pas les memes gens.

Sorties : t2-camps.csv, t2-changeurs-deciles.csv, t2-controles-volet3.csv.
Aucune microdonnee.

Usage : .venv/bin/python analyses/t2_camps.py
"""

import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t2_commun as T2


def _moy_ponderee(W, x, poids):
    """Moyenne ponderee par personne, sur les personnes de poids non nul."""
    w = W * poids[None, :]
    return (w @ np.nan_to_num(x, nan=0.0)) / np.maximum(w.sum(axis=1), 1e-9)


def calculer():
    t0 = time.time()
    lignes, deciles, controles = [], [], []
    rng = np.random.default_rng(T2.GRAINE)

    for perimetre, delai in (("4ans", "quatre ans"), ("2ans", "deux ans")):
        paquet = T2.charger(perimetre)
        items = paquet["items"]
        est_ord = T2.items_ordinaux(items)
        garde_ord, V = T2.valeurs_ordinales(paquet, est_ord)
        reel = T2.amplitude_reelle(paquet, V, garde_ord)
        n = paquet["n"]
        W = T2.poids_bootstrap(n, T2.N_BOOTSTRAP, rng)
        ancrages = {"ideologie declaree (polviews)": T2.axes(paquet)["camp"],
                    "parti (partyid)": T2.parti(paquet)}
        nul = T2.nul_amplitude(paquet, "panel", T2.N_REPLICATS_NUL, rng, V, garde_ord)

        for nom_ancrage, camp in ancrages.items():
            base = reel["n_eval"]
            for c in sorted(set(camp)):
                m = camp == c
                if m.sum() < T2.MIN_GROUPE:
                    continue
                poids = np.where(m, base, 0.0)
                taux = _moy_ponderee(W, reel["taux"], poids)
                poids_o = np.where(m, reel["n_ord"], 0.0)
                dist = _moy_ponderee(W, reel["ord"], poids_o)
                rap = (_moy_ponderee(W, reel["taux"], poids)
                       / np.maximum(_moy_ponderee(W, nul["taux_nul"], poids), 1e-12))
                lo, hi = T2.ic(taux[1:])
                lo2, hi2 = T2.ic(dist[1:])
                lo3, hi3 = T2.ic(rap[1:])
                lignes.append({
                    "perimetre": perimetre, "delai": delai, "ancrage": nom_ancrage,
                    "camp": c, "n_personnes": int(m.sum()),
                    "taux_de_changement": float(taux[0]), "ic_bas": lo, "ic_haut": hi,
                    "distance_ordinale": float(dist[0]),
                    "distance_ic_bas": lo2, "distance_ic_haut": hi2,
                    "rapport_reel_sur_nul": float(rap[0]),
                    "rapport_ic_bas": lo3, "rapport_ic_haut": hi3})

            # --- ou se recrutent les changeurs ---------------------------------
            # decile superieur et inferieur du taux de changement individuel, calcules
            # sur les personnes qui ont au moins 20 items evaluables (seuil de a12, deja
            # applique a l'assemblage du perimetre).
            t = reel["taux"]
            q90, q10 = np.percentile(t, 90), np.percentile(t, 10)
            haut, bas = t >= q90, t <= q10
            for c in sorted(set(camp)):
                m = camp == c
                if m.sum() < T2.MIN_GROUPE:
                    continue
                part = m.mean()
                ph = (m & haut).sum() / max(haut.sum(), 1)
                pb = (m & bas).sum() / max(bas.sum(), 1)
                # bootstrap sur les personnes du rapport de representation
                rh, rb = [], []
                for b in range(1, T2.N_BOOTSTRAP + 1):
                    w = W[b]
                    pw = (w * m).sum() / w.sum()
                    hw = (w * m * haut).sum() / max((w * haut).sum(), 1e-9)
                    bw = (w * m * bas).sum() / max((w * bas).sum(), 1e-9)
                    rh.append(hw / max(pw, 1e-9))
                    rb.append(bw / max(pw, 1e-9))
                lo, hi = T2.ic(rh)
                lo2, hi2 = T2.ic(rb)
                deciles.append({
                    "perimetre": perimetre, "delai": delai, "ancrage": nom_ancrage,
                    "camp": c, "part_de_la_population": part,
                    "part_du_decile_haut": ph,
                    "sur_representation_haut": ph / max(part, 1e-9),
                    "haut_ic_bas": lo, "haut_ic_haut": hi,
                    "part_du_decile_bas": pb,
                    "sur_representation_bas": pb / max(part, 1e-9),
                    "bas_ic_bas": lo2, "bas_ic_haut": hi2})
        print(f"  {perimetre} fait, {time.time() - t0:.0f} s", flush=True)

    df = pd.DataFrame(lignes)
    # contraste maximal entre camps, perimetre primaire, ancrage ideologique
    s = df[(df.perimetre == "4ans") & (df.ancrage.str.startswith("ideologie"))
           & (df.camp != "non renseigne")]
    controles.append({"controle": "ecart maximal entre camps sur le taux de changement",
                      "obtenu": float(s.taux_de_changement.max() - s.taux_de_changement.min()),
                      "camp_le_plus_bas": s.loc[s.taux_de_changement.idxmin(), "camp"],
                      "camp_le_plus_haut": s.loc[s.taux_de_changement.idxmax(), "camp"]})
    T2.ecrire(df, "t2-camps.csv")
    T2.ecrire(deciles, "t2-changeurs-deciles.csv")
    T2.ecrire(controles, "t2-controles-volet3.csv")
    print(f"volet 3 termine en {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    calculer()
