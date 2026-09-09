"""
a25_contrastes : items sensibles au mode contre temoins negatifs, condition par condition.

Statut : script d'analyse jetable, aucun appel de modele de langage. Il ne lit que les
agregats par item ecrits par a25_mesures.py, jamais une microdonnee. Aucun script existant
n'est modifie.

Trois choses par couple (condition, metrique) :

  1. la difference de moyenne entre les items que NORC classe "Likely mode sensitive" et
     ceux qu'il classe "Less likely to be mode sensitive", avec un intervalle de confiance
     obtenu par reechantillonnage des ITEMS. L'intervalle par reechantillonnage des
     PERSONNES est calcule ailleurs, par a25_mesures.py, parce qu'il demande les matrices
     de reponses ; les deux sont rapportes cote a cote dans le rapport.
  2. un test de permutation des etiquettes sensible / temoin, qui ne suppose rien sur la
     forme de la distribution des ecarts par item. C'est le test decisif : il dit si la
     difference observee se distingue de ce qu'on obtiendrait en tirant au hasard 12 items
     parmi les 77.
  3. deux controles de composition. Les deux groupes n'ont ni le meme nombre de modalites
     ni la meme proportion d'items ordinaux, et la distance de distribution depend des
     deux. Le contraste est donc recalcule (a) sur les seuls items ordinaux, (b) en
     stratifiant par le couple (type, nombre de modalites) et en moyennant les differences
     intra strate ponderees par le nombre d'items sensibles de la strate.

Un quatrieme controle est produit par construction : la ligne "humains vague 2" est la
meme mesure appliquee aux memes humains reinterroges a deux semaines. Si le contraste y
est nul, l'instabilite test retest n'est pas plus forte sur les items sensibles et l'ecart
des agents ne peut pas etre impute a du bruit humain.

Entree  : resultats/a25-par-item-condition.csv
Sortie  : resultats/a25-contrastes.csv, resultats/a25-contrastes-controles.csv

Usage : .venv/bin/python analyses/a25_contrastes.py [--tirages 10000]
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

METRIQUES = ["distance", "ecart_desirabilite", "exactitude"]


def bootstrap_items(a, b, tirages, rng):
    """Intervalle de la difference de moyennes, items reechantillonnes dans chaque groupe."""
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan, np.nan
    ta = a[rng.integers(0, len(a), (tirages, len(a)))].mean(axis=1)
    tb = b[rng.integers(0, len(b), (tirages, len(b)))].mean(axis=1)
    d = ta - tb
    return float(a.mean() - b.mean()), float(np.percentile(d, 2.5)), float(np.percentile(d, 97.5))


def permutation(a, b, tirages, rng):
    """p bilateral du test de permutation des etiquettes sur la difference de moyennes."""
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) < 2 or len(b) < 2:
        return np.nan, np.nan
    obs = a.mean() - b.mean()
    pool = np.concatenate([a, b])
    n = len(a)
    idx = np.argsort(rng.random((tirages, len(pool))), axis=1)
    perm = pool[idx]
    stat = perm[:, :n].mean(axis=1) - perm[:, n:].mean(axis=1)
    p = float((np.abs(stat) >= abs(obs) - 1e-12).mean())
    return float(obs), p


def stratifie(d, groupe_a, groupe_b, metrique):
    """Difference moyenne intra strate (type, nombre de modalites), ponderee.

    Le poids d'une strate est son nombre d'items du groupe A. Les strates sans item dans
    l'un des deux groupes sont ecartees, et le nombre d'items conserves est rapporte.
    """
    num, den, gardes = 0.0, 0, 0
    for cle, sous in d.groupby(["type", "n_modalites"]):
        a = sous.loc[sous.classe_norc == groupe_a, metrique].dropna().values
        b = sous.loc[sous.classe_norc == groupe_b, metrique].dropna().values
        if len(a) == 0 or len(b) == 0:
            continue
        num += len(a) * (a.mean() - b.mean())
        den += len(a)
        gardes += len(a)
    return (num / den if den else np.nan), gardes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tirages", type=int, default=10000)
    ap.add_argument("--graine", type=int, default=20260908)
    args = ap.parse_args()

    par_item = pd.read_csv(os.path.join(SORTIE, "a25-par-item-condition.csv"))
    croisement = pd.read_csv(os.path.join(SORTIE, "a25-croisement.csv"))
    par_item = par_item.merge(
        croisement[["item", "n_modalites", "groupe_litterature"]], on="item", how="left")

    rng = np.random.default_rng(args.graine)
    lignes, controles = [], []

    for (per, cond), d in par_item.groupby(["perimetre", "condition"]):
        for metrique in METRIQUES:
            for groupe_a in ["sensible", "investiguer", "sensible+investiguer"]:
                if groupe_a == "sensible+investiguer":
                    a = d.loc[d.classe_norc.isin(["sensible", "investiguer"]), metrique].values
                else:
                    a = d.loc[d.classe_norc == groupe_a, metrique].values
                b = d.loc[d.classe_norc == "temoin", metrique].values
                moy, bas, haut = bootstrap_items(a, b, args.tirages, rng)
                _, p = permutation(a, b, args.tirages, rng)
                lignes.append({
                    "perimetre": per, "condition": cond, "metrique": metrique,
                    "groupe": groupe_a,
                    "n_items_groupe": int(np.sum(~np.isnan(a))),
                    "n_items_temoin": int(np.sum(~np.isnan(b))),
                    "moyenne_groupe": float(np.nanmean(a)) if len(a) else np.nan,
                    "moyenne_temoin": float(np.nanmean(b)) if len(b) else np.nan,
                    "difference": moy, "ic_items_bas": bas, "ic_items_haut": haut,
                    "p_permutation": p,
                })

            # controle 1 : items ordinaux seulement
            do = d[d.type == "ordinal"]
            a = do.loc[do.classe_norc == "sensible", metrique].values
            b = do.loc[do.classe_norc == "temoin", metrique].values
            moy_o, bas_o, haut_o = bootstrap_items(a, b, args.tirages, rng)
            _, p_o = permutation(a, b, args.tirages, rng)
            # controle 2 : stratification par type et nombre de modalites
            strat, gardes = stratifie(d, "sensible", "temoin", metrique)
            # controle 3 : ecart residualise du bruit humain test retest
            ref = par_item[(par_item.perimetre == per)
                           & (par_item.condition == "humains vague 2")][["item", metrique]]
            ref = ref.rename(columns={metrique: "ref"})
            dr = d.merge(ref, on="item", how="left")
            dr["residu"] = dr[metrique] - dr["ref"]
            ar = dr.loc[dr.classe_norc == "sensible", "residu"].values
            br = dr.loc[dr.classe_norc == "temoin", "residu"].values
            moy_r, bas_r, haut_r = bootstrap_items(ar, br, args.tirages, rng)
            _, p_r = permutation(ar, br, args.tirages, rng)

            # controle 4 : decoupage de la litterature au lieu de celui de NORC
            al = d.loc[d.groupe_litterature == "sensible litterature", metrique].values
            bl = d.loc[d.groupe_litterature == "temoin litterature", metrique].values
            moy_l, bas_l, haut_l = bootstrap_items(al, bl, args.tirages, rng)
            _, p_l = permutation(al, bl, args.tirages, rng)
            controles.append({
                "perimetre": per, "condition": cond, "metrique": metrique,
                "ordinaux_difference": moy_o, "ordinaux_ic_bas": bas_o,
                "ordinaux_ic_haut": haut_o, "ordinaux_p": p_o,
                "ordinaux_n_sensibles": int(np.sum(~np.isnan(a))),
                "stratifie_difference": strat, "stratifie_n_sensibles": gardes,
                "residualise_difference": moy_r, "residualise_ic_bas": bas_r,
                "residualise_ic_haut": haut_r, "residualise_p": p_r,
                "litterature_difference": moy_l, "litterature_ic_bas": bas_l,
                "litterature_ic_haut": haut_l, "litterature_p": p_l,
                "litterature_n_sensibles": int(np.sum(~np.isnan(al))),
            })

    t = pd.DataFrame(lignes)
    t.to_csv(os.path.join(SORTIE, "a25-contrastes.csv"), index=False, float_format="%.6f")
    c = pd.DataFrame(controles)
    c.to_csv(os.path.join(SORTIE, "a25-contrastes-controles.csv"), index=False,
             float_format="%.6f")

    pd.set_option("display.width", 220)
    for metrique in METRIQUES:
        print("\n" + "=" * 110)
        print(f"CONTRASTE sensible moins temoin, metrique {metrique}, perimetre 150")
        print("=" * 110)
        s = t[(t.metrique == metrique) & (t.groupe == "sensible") & (t.perimetre == 150)]
        print(s[["condition", "moyenne_groupe", "moyenne_temoin", "difference",
                 "ic_items_bas", "ic_items_haut", "p_permutation"]]
              .sort_values("difference", ascending=False).to_string(index=False))

    print(f"\necrit dans {SORTIE} : a25-contrastes.csv, a25-contrastes-controles.csv")


if __name__ == "__main__":
    main()
