"""
t2_amplitude : volet 2 de T2. Le nul a derive de C1, « il bouge deux fois trop »,
transporte sur les panels GSS.

Preenregistrement : resultats/t2-preenregistrement.md, section 4.

Le temoin est celui de c1-anticipations-sce.md section 6.3, transpose : la vague
d'arrivee est remelangee entre les personnes du meme panel (N1) ou du meme panel et du
meme segment ideologie x age x education (N2). Les deux marginales et la derive du
groupe de permutation sont conservees exactement, l'appariement des personnes est
detruit. On compare alors l'AMPLITUDE des changements individuels, et non leur sens.

Sorties : t2-amplitude.csv, t2-amplitude-par-famille.csv, t2-ordinaux.csv,
t2-controles-volet2.csv. Aucune microdonnee.

Usage : .venv/bin/python analyses/t2_amplitude.py
"""

import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t2_commun as T2
from a2_baselines_gss import FAMILLES


def _rapport(reel, nul, n_ref, W):
    """Rapport des moyennes ponderees par les personnes, avec bootstrap.

    reel, nul : valeur par personne. n_ref : denominateur d'items par personne, sert de
    poids d'agregation (une personne qui voit plus d'items pese plus, comme dans a12).
    """
    ok = np.isfinite(reel) & np.isfinite(nul) & (n_ref > 0)
    w = W[:, ok] * n_ref[ok][None, :]
    r = (w @ reel[ok]) / np.maximum(w.sum(axis=1), 1e-9)
    q = (w @ nul[ok]) / np.maximum(w.sum(axis=1), 1e-9)
    rap = r / np.maximum(q, 1e-12)
    lo, hi = T2.ic(rap[1:])
    return {"reel": float(r[0]), "nul": float(q[0]), "rapport": float(rap[0]),
            "ic_bas": lo, "ic_haut": hi, "n_personnes": int(ok.sum())}


def calculer():
    t0 = time.time()
    controles = []
    lignes = []
    lignes_fam = []
    lignes_ord = []
    rng = np.random.default_rng(T2.GRAINE)

    for perimetre, delai in (("4ans", "quatre ans"), ("2ans", "deux ans")):
        paquet = T2.charger(perimetre)
        items = paquet["items"]
        est_ord = T2.items_ordinaux(items)
        garde_ord, V = T2.valeurs_ordinales(paquet, est_ord)
        n = paquet["n"]
        if perimetre == "4ans":
            for j in np.flatnonzero(garde_ord):
                k = paquet["k_par_item"][j]
                v = V[j, :k]
                lignes_ord.append({"item": items[j], "n_modalites": int(k),
                                   "code_min": float(np.nanmin(v)),
                                   "code_max": float(np.nanmax(v)),
                                   "codes_consecutifs":
                                       bool(np.allclose(np.sort(v), np.arange(np.nanmin(v),
                                                                              np.nanmin(v) + k)))})
        reel = T2.amplitude_reelle(paquet, V, garde_ord)
        W = T2.poids_bootstrap(n, T2.N_BOOTSTRAP, rng)
        for variante, nom in (("panel", "N1, remelange dans le panel"),
                              ("segment", "N2, remelange dans le segment")):
            nul = T2.nul_amplitude(paquet, variante, T2.N_REPLICATS_NUL, rng, V, garde_ord)
            controles.append({"controle": f"marginale conservee, {perimetre}, {variante}",
                              "attendu": 0.0, "obtenu": nul["ecart_marginale"],
                              "passe": nul["ecart_marginale"] == 0.0})
            for quant, r_, n_, den in (
                    ("nombre d'items changes", reel["taux"], nul["taux_nul"], reel["n_eval"]),
                    ("distance ordinale", reel["ord"], nul["ord_nul"], reel["n_ord"])):
                d = _rapport(r_, n_, den, W)
                d.update({"perimetre": perimetre, "delai": delai, "variante": nom,
                          "quantite": quant, "decoupe": "ensemble", "cle": "tout"})
                lignes.append(d)
                # par panel
                for pan in sorted(set(paquet["panel"].astype(str))):
                    m = paquet["panel"].astype(str) == pan
                    dd = _rapport(np.where(m, r_, np.nan), np.where(m, n_, np.nan), den, W)
                    dd.update({"perimetre": perimetre, "delai": delai, "variante": nom,
                               "quantite": quant, "decoupe": "panel", "cle": pan})
                    lignes.append(dd)
                # par camp
                camp = T2.axes(paquet)["camp"]
                for c in sorted(set(camp)):
                    m = camp == c
                    if m.sum() < T2.MIN_GROUPE:
                        continue
                    dd = _rapport(np.where(m, r_, np.nan), np.where(m, n_, np.nan), den, W)
                    dd.update({"perimetre": perimetre, "delai": delai, "variante": nom,
                               "quantite": quant, "decoupe": "camp", "cle": c})
                    lignes.append(dd)
            print(f"  {perimetre} {variante} fait, {time.time() - t0:.0f} s", flush=True)

            # --- par famille d'items, sur le seul nombre d'items changes ---------
            if variante == "panel":
                ca, cb, ok = paquet["c_a"], paquet["c_b"], paquet["ok"]
                for fam, membres in FAMILLES.items():
                    cols = [k for k, it in enumerate(items) if it in membres]
                    if len(cols) < 3:
                        continue
                    sub_ok = ok[:, cols]
                    nev = sub_ok.sum(axis=1).astype(float)
                    nch = ((ca[:, cols] != cb[:, cols]) & sub_ok).sum(axis=1).astype(float)
                    r_ = np.where(nev > 0, nch / np.maximum(nev, 1), np.nan)
                    # taux nul de la personne sur ce sous ensemble d'items
                    nn = (nul["chg_par_item"][:, cols] * sub_ok).sum(axis=1)
                    n_ = np.where(nev > 0, nn / np.maximum(nev * T2.N_REPLICATS_NUL, 1), np.nan)
                    d = _rapport(r_, n_, nev, W)
                    d.update({"perimetre": perimetre, "delai": delai, "famille": fam,
                              "n_items": len(cols)})
                    lignes_fam.append(d)

    T2.ecrire(lignes, "t2-amplitude.csv")
    T2.ecrire(lignes_fam, "t2-amplitude-par-famille.csv")
    T2.ecrire(lignes_ord, "t2-ordinaux.csv")
    T2.ecrire(controles, "t2-controles-volet2.csv")
    print(f"volet 2 termine en {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    calculer()
