"""
a43_peng : les quatre mesures de Peng et al. sur nos donnees, telles que a36 les definit.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Preenregistrement :
resultats/a43-preenregistrement.md, mesure M5.

Les quatre mesures, definitions de a36 section 2.1, sur les seuls items ordinaux :

  exactitude   1 - MAD, les valeurs etant des rangs normalises dans [0, 1], donc etendue
               1 ; une prediction absente recoit zero, convention severe de a29 et a39 ;
  correlation  correlation entre humains et jumeaux A TRAVERS LES PARTICIPANTS, un
               coefficient par item, moyenne par z de Fisher. C'est leur choix explicite
               contre celui de Park et al., qui correle a travers les questions ;
  Glass Delta  |moyenne_methode - moyenne_humains| / ecart_type_humains, un par item ;
  rapport      ecart_type(methode) / ecart_type(humains), un par item, sur l'echantillon
               apparie. Cette quatrieme mesure est celle de a39 ; a43 la recalcule par le
               meme chemin de sommes que les trois autres et verifie qu'elle redonne
               a39-ecarts-types.csv.

Toutes les incertitudes sont des bootstraps sur les PERSONNES, avec le meme tirage pour
toutes les conditions d'un perimetre.

Sortie  : resultats/a43-peng.csv, a43-peng-par-item.csv, a43-verification-a39.csv.

Usage :
  .venv/bin/python analyses/a43_peng.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a43_commun as C
import a39_commun as C39

N_MIN_ITEM = 30     # personnes appariees minimales pour qu'un item entre dans une mesure


def sommes_appariees(P, H, lignes):
    """Six sommes par personne et par item, sur l'echantillon apparie.

    Retourne un tableau (personnes, items, 6) : n, somme p, somme h, somme p^2,
    somme h^2, somme p*h. Une cellule n'entre que si la prediction ET la vraie reponse
    sont exploitables, comme dans a39_commun.rapport_ecarts_types.
    """
    p, h = P[lignes], H[lignes]
    ok = ~np.isnan(p) & ~np.isnan(h)
    pv = np.where(ok, np.nan_to_num(p), 0.0)
    hv = np.where(ok, np.nan_to_num(h), 0.0)
    return np.stack([ok.astype(float), pv, hv, pv * pv, hv * hv, pv * hv], axis=2)


def mesures_par_item(S, n_min=N_MIN_ITEM):
    """Correlation, Glass Delta et rapport d'ecarts types, item par item.

    S : tableau (items, 6) de sommes cumulees sur les personnes retenues.
    Les ecarts types sont sans biais, ddof = 1, comme dans a39.
    """
    n, sp, sh, spp, shh, sph = [S[..., k] for k in range(6)]
    assez = n >= n_min
    nn = np.maximum(n, 2.0)
    mp, mh = sp / nn, sh / nn
    with np.errstate(invalid="ignore", divide="ignore"):
        vp = (spp - nn * mp * mp) / (nn - 1.0)
        vh = (shh - nn * mh * mh) / (nn - 1.0)
        cov = (sph - nn * mp * mh) / (nn - 1.0)
        sdp, sdh = np.sqrt(np.maximum(vp, 0.0)), np.sqrt(np.maximum(vh, 0.0))
        r = np.where(assez & (sdp > 0) & (sdh > 0), cov / np.maximum(sdp * sdh, 1e-300),
                     np.nan)
        glass = np.where(assez & (sdh > 0), np.abs(mp - mh) / np.maximum(sdh, 1e-300),
                         np.nan)
        ratio = np.where(assez & (sdh > 0), sdp / np.maximum(sdh, 1e-300), np.nan)
    return {"r": r, "glass": glass, "ratio": ratio, "sd_pred": np.where(assez, sdp, np.nan),
            "sd_humain": np.where(assez, sdh, np.nan), "n": n}


def agreger(m):
    """Moyennes sur les items : z de Fisher pour la correlation, moyenne simple sinon."""
    r = m["r"][~np.isnan(m["r"])]
    z = np.arctanh(np.clip(r, -0.999999, 0.999999)) if len(r) else np.array([])
    return {
        "correlation": float(np.tanh(z.mean())) if len(z) else np.nan,
        "correlation_moyenne_brute": float(r.mean()) if len(r) else np.nan,
        "glass_delta": float(np.nanmean(m["glass"])),
        "rapport_ecarts_types": float(np.nanmean(m["ratio"])),
        "rapport_median": float(np.nanmedian(m["ratio"])),
        "n_items": int((~np.isnan(m["ratio"])).sum()),
        "items_sous_1": int(np.nansum(m["ratio"] < 1.0)),
        "correlations_positives": int(np.nansum(m["r"] > 0)),
    }


def poids_bootstrap(idx_boot, n):
    """Matrice (tirages, personnes) du nombre de fois ou chaque personne est tiree.

    Un bootstrap sur les personnes est une somme ponderee : le passer en produit
    matriciel evite 2 000 copies d'un tableau de 450 000 flottants.
    """
    W = np.zeros((len(idx_boot), n))
    for t, idx in enumerate(idx_boot):
        W[t] = np.bincount(idx, minlength=n)
    return W


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--bootstrap", type=int, default=C.BOOTSTRAP)
    args = ap.parse_args()

    paquet = C.charger(args.cache, args.cache_foret, args.cache_a35)
    ords, colonnes, rangs, H = C.preparer_valeurs(paquet)
    per = C.perimetres(paquet)

    lignes_out, lignes_item, verif = [], [], []
    for nom_per, lignes in per.items():
        n = len(lignes)
        ib = C.tirages_bootstrap(n, args.bootstrap)
        W = poids_bootstrap(ib, n)
        for cond in C.methodes_du_perimetre(paquet, nom_per):
            P = C.scores_methode(paquet, cond, colonnes, rangs)

            # --- exactitude 1 - MAD, prediction absente comptee zero
            sc = C39.scores_exactitude_ordinale(P, H)[lignes]
            masque = ~np.isnan(sc)
            num = np.where(masque, np.nan_to_num(sc), 0.0).sum(axis=1)
            den = masque.sum(axis=1).astype(float)
            exact = float(num.sum() / den.sum()) if den.sum() else np.nan
            tir_ex = (W @ num) / np.maximum(W @ den, 1e-12)
            ex_bas, ex_haut = C.ic(tir_ex)

            # --- les trois mesures par item
            S = sommes_appariees(P, H, lignes)
            m = mesures_par_item(S.sum(axis=0))
            agg = agreger(m)

            plat = S.reshape(n, -1)
            tir = {"correlation": np.empty(len(ib)), "glass_delta": np.empty(len(ib)),
                   "rapport_ecarts_types": np.empty(len(ib))}
            boot = (W @ plat).reshape(len(ib), len(ords), 6)
            for t in range(len(ib)):
                a = agreger(mesures_par_item(boot[t]))
                for k in tir:
                    tir[k][t] = a[k]

            ligne = {"perimetre": nom_per, "condition": cond,
                     "famille_condition": C.FAMILLE.get(cond, ""),
                     "exactitude": exact, "exactitude_ic_bas": ex_bas,
                     "exactitude_ic_haut": ex_haut,
                     "taux_refus": float(1.0 - (~np.isnan(P[lignes])).sum()
                                         / max((~np.isnan(H[lignes])).sum(), 1))}
            ligne.update(agg)
            for k, v in tir.items():
                b, h = C.ic(v)
                ligne[k + "_ic_bas"], ligne[k + "_ic_haut"] = b, h
            lignes_out.append(ligne)

            for j, it in enumerate(ords):
                lignes_item.append({"perimetre": nom_per, "condition": cond, "item": it,
                                    "correlation": m["r"][j], "glass_delta": m["glass"][j],
                                    "rapport_ecarts_types": m["ratio"][j],
                                    "sd_pred": m["sd_pred"][j],
                                    "sd_humain": m["sd_humain"][j], "n": int(m["n"][j])})
            print(f"  Peng {nom_per} {cond}", flush=True)

            # --- verification contre a39
            ref = C39.rapport_ecarts_types(P, H, lignes)
            ecart = np.nanmax(np.abs(ref["ratio"].values - m["ratio"]))
            verif.append({"perimetre": nom_per, "condition": cond,
                          "ecart_max_ratio_contre_a39_commun": float(ecart)})

    df = pd.DataFrame(lignes_out)
    C.ecrire(df, "a43-peng.csv")
    C.ecrire(pd.DataFrame(lignes_item), "a43-peng-par-item.csv")

    # comparaison ligne a ligne avec le CSV publie par a39, quand il existe
    chemin = os.path.join(C.SORTIE, "a39-ecarts-types.csv")
    if os.path.exists(chemin):
        a39 = pd.read_csv(chemin)
        for _, r in a39.iterrows():
            n = df[(df["perimetre"].astype(str) == str(r["perimetre"]))
                   & (df["condition"] == r["condition"])]
            if len(n):
                verif.append({"perimetre": r["perimetre"], "condition": r["condition"],
                              "a39_ratio_moyen": r["ratio_moyen"],
                              "a43_ratio_moyen": float(n.iloc[0]["rapport_ecarts_types"]),
                              "ecart": float(n.iloc[0]["rapport_ecarts_types"]
                                             - r["ratio_moyen"])})
    C.ecrire(pd.DataFrame(verif), "a43-verification-a39.csv")

    print()
    for nom_per in ("1052", "150"):
        print(f"=== perimetre {nom_per} ===")
        s = df[df["perimetre"] == nom_per]
        for cond in C.ORDRE_METHODES:
            b = s[s["condition"] == cond]
            if b.empty:
                continue
            r = b.iloc[0]
            print(f"  {cond:<28s} exact {r['exactitude']:.4f}  corr {r['correlation']:+.4f}"
                  f"  Glass {r['glass_delta']:.4f}  sd {r['rapport_ecarts_types']:.4f}")
        print()


if __name__ == "__main__":
    main()
