"""
a30_structure : la structure interne des camps, volet 2 de a30.

Quatre mesures, toutes calculees a effectif egal entre camps, parce que trois d'entre
elles croissent mecaniquement avec le nombre de personnes.

  1. Patrons de reponses distincts. Sur un jeu de dix items, combien de combinaisons
     differentes existent reellement dans le camp ? C'est la mesure de 05-29 (19 patrons
     contre 340), portee ici sur des camps humains et non sur des agents.
  2. Dimensions. Analyse en composantes principales sur les items ordinaux, camp par
     camp : part de variance de la premiere composante, et nombre de composantes pour
     atteindre la moitie de la variance. Moins la premiere composante explique, plus le
     camp a besoin de plusieurs axes pour etre decrit.
  3. Sous groupes. k moyennes sur les memes items, k de 2 a 8, choix par la silhouette.
     Rappel de a1 section 5 : sur ces donnees la silhouette est faible en valeur absolue,
     ce qui est un resultat sur les donnees et pas un defaut de la methode.
  4. Correlation entre l'axe economique et l'axe social a l'interieur de chaque camp.
     La these libertaires contre autoritaires predit une correlation plus faible a
     droite. Cible humaine de la litterature, toute population confondue : 0,30 (05-03).

FAMILLE D'HYPOTHESES, ECRITE AVANT LES RESULTATS
------------------------------------------------
S1 : le camp de droite produit plus de patrons distincts que le camp de gauche, a
     effectif et jeu d'items identiques.
S2 : la premiere composante explique une part plus faible de la variance a droite.
S3 : le nombre de sous groupes retenu par la silhouette est plus grand a droite.
S4 : la correlation entre axe economique et axe social est plus faible a droite.
Quatre tests, corriges par Holm dans une famille de quatre.

LIMITE STRUCTURELLE, A LIRE AVANT LES CHIFFRES DE S4
-----------------------------------------------------
Les camps sont definis par l'ideologie declaree, et les deux scores correlent avec
l'ideologie. Restreindre a un camp restreint donc l'etendue des deux scores, ce qui
abaisse mecaniquement la correlation, et pas de la meme quantite dans les trois camps.
L'ecart type de chaque score dans chaque camp est rapporte a cote de la correlation,
faute de quoi le chiffre n'est pas interpretable.

SORTIES : resultats/a30-structure-patrons.csv, a30-structure-dimensions.csv,
          a30-structure-clusters.csv, a30-structure-axes.csv

Usage : .venv/bin/python analyses/a30_structure.py
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a30_commun as C  # noqa: E402
from a30_humains_gss import charger_gss  # noqa: E402
from a25_commun import ORDINAUX, sans_score, options_par_item  # noqa: E402

CAMPS = ["gauche", "centre", "droite"]


def apparie(a, b, n_boot, rng):
    """Difference moyenne appariee, IC bootstrap et p par inversion de signe.

    a et b sont deux vecteurs de meme longueur, apparies tirage a tirage (meme jeu
    d'items, meme sous echantillon). Le test d'inversion de signe est le test exact de
    permutation pour un plan apparie.
    """
    d = np.asarray(a, dtype=float) - np.asarray(b, dtype=float)
    n = len(d)
    bt = rng.choice(d, size=(n_boot, n), replace=True).mean(axis=1)
    signes = rng.choice([-1.0, 1.0], size=(n_boot, n))
    nul = (signes * d[None, :]).mean(axis=1)
    p = (int((np.abs(nul) >= abs(d.mean()) - 1e-12).sum()) + 1) / (n_boot + 1)
    return (float(d.mean()), float(np.percentile(bt, 2.5)),
            float(np.percentile(bt, 97.5)), p)


# ---------------------------------------------------------------------------
# 1. Patrons de reponses distincts
# ---------------------------------------------------------------------------

def patrons(codes, masques, items_idx, taille, tirages, rng, k_items=10, jeux=200):
    """Nombre moyen de patrons distincts par camp, a effectif et items identiques.

    Une cellule vide est traitee comme une modalite a part entiere : l'ignorer
    obligerait a ne garder que les personnes completes sur les dix items, ce qui
    selectionnerait differemment les trois camps.
    """
    lignes = []
    dispo = np.asarray(items_idx)
    for t in range(jeux):
        sel = rng.choice(dispo, size=min(k_items, len(dispo)), replace=False)
        sous = codes[:, sel]
        # Un entier unique par patron, base K+1 pour loger la modalite « vide ».
        base = int(sous.max()) + 2
        cle = np.zeros(len(sous), dtype=object)
        for j in range(sous.shape[1]):
            cle = cle * base + (sous[:, j] + 1)
        for nom, m in masques.items():
            idx = np.flatnonzero(m)
            if len(idx) < taille:
                continue
            for _ in range(tirages):
                s = rng.choice(idx, size=taille, replace=False)
                lignes.append({"jeu": t, "camp": nom,
                               "patrons": len(np.unique(cle[s]))})
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 2 et 3. Dimensions et sous groupes
# ---------------------------------------------------------------------------

def matrice_ordinale(codes, items, ks, options):
    """Matrice reelle sur les seuls items ordinaux, codes ramenes dans [0, 1]."""
    garde = [j for j, it in enumerate(items)
             if it in ORDINAUX and not any(sans_score(o) for o in options[it])]
    X = codes[:, garde].astype(float)
    X[X < 0] = np.nan
    for c, j in enumerate(garde):
        if ks[j] > 1:
            X[:, c] /= (ks[j] - 1)
    return X, [items[j] for j in garde]


def _imputer(X):
    """Remplace les manquants par la moyenne de l'item, calculee dans le sous echantillon."""
    Y = X.copy()
    mu = np.nanmean(Y, axis=0)
    mu = np.where(np.isfinite(mu), mu, 0.0)
    idx = np.where(np.isnan(Y))
    Y[idx] = np.take(mu, idx[1])
    return Y


def dimensions_et_clusters(X, masques, taille, tirages, rng, k_max=8):
    """Part de variance de la premiere composante, nombre d'axes, meilleur k, silhouette."""
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_score
    lignes = []
    for nom, m in masques.items():
        idx = np.flatnonzero(m)
        if len(idx) < taille:
            continue
        for t in range(tirages):
            s = rng.choice(idx, size=taille, replace=False)
            Y = _imputer(X[s])
            Y = Y - Y.mean(axis=0)
            sd = Y.std(axis=0)
            Y = Y[:, sd > 1e-9] / sd[sd > 1e-9]
            # Valeurs propres de la matrice de correlation, via la decomposition en
            # valeurs singulieres : plus stable que la diagonalisation directe.
            val = np.linalg.svd(Y, compute_uv=False) ** 2
            val = val / val.sum()
            n50 = int(np.searchsorted(np.cumsum(val), 0.50) + 1)
            n80 = int(np.searchsorted(np.cumsum(val), 0.80) + 1)
            meilleur_k, meilleure_s = np.nan, -np.inf
            sils = {}
            for k in range(2, k_max + 1):
                lab = KMeans(n_clusters=k, n_init=4, random_state=int(rng.integers(1e9))
                             ).fit_predict(Y)
                sc = float(silhouette_score(Y, lab))
                sils[k] = sc
                if sc > meilleure_s:
                    meilleure_s, meilleur_k = sc, k
            lignes.append({"camp": nom, "tirage": t, "var_pc1": float(val[0]),
                           "var_pc2": float(val[1]), "n_axes_50": n50, "n_axes_80": n80,
                           "meilleur_k": meilleur_k, "silhouette": meilleure_s,
                           **{f"sil_k{k}": v for k, v in sils.items()}})
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 4. Axe economique contre axe social
# ---------------------------------------------------------------------------

def scores_axes(codes, items, ks, camps7):
    """Score economique et score social par personne, meme combinaison pour tout le monde.

    Chaque axe est la premiere composante principale de son bloc d'items, estimee sur
    l'echantillon complet et non camp par camp : c'est la seule facon d'obtenir deux
    variables comparables d'un camp a l'autre. Le signe est fixe une fois pour toutes en
    orientant la composante positivement avec l'ideologie declaree en sept points, ce qui
    ne change aucune valeur absolue de correlation.
    """
    ordre = {it: j for j, it in enumerate(items)}
    out = {}
    for nom, liste in (("economique", C.AXE_ECONOMIQUE), ("social", C.AXE_SOCIAL)):
        cols = [ordre[i] for i in liste if i in ordre]
        X = codes[:, cols].astype(float)
        X[X < 0] = np.nan
        for c, j in enumerate(cols):
            if ks[j] > 1:
                X[:, c] /= (ks[j] - 1)
        Y = _imputer(X)
        Y = (Y - Y.mean(axis=0))
        sd = Y.std(axis=0)
        Y = Y[:, sd > 1e-9] / sd[sd > 1e-9]
        u, s, vt = np.linalg.svd(Y, full_matrices=False)
        score = u[:, 0] * s[0]
        ok = np.array([v is not None for v in camps7])
        rang = np.array([C.GSS_POINTS7.index(v) if v in C.GSS_POINTS7 else np.nan
                         for v in camps7], dtype=float)
        r = np.corrcoef(score[ok], rang[ok])[0, 1]
        out[nom] = score * (1.0 if r > 0 else -1.0)
        out[nom + "_n_items"] = len(cols)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tirages", type=int, default=100)
    ap.add_argument("--jeux", type=int, default=200)
    ap.add_argument("--boot", type=int, default=1000)
    args = ap.parse_args()
    rng = np.random.default_rng(C.GRAINE)

    ids, items, codes1, codes2, ks, camps, cellules, x, attributs = charger_gss()
    options = options_par_item(C.RACINE)
    masques = {c: (camps["bloc3"] == c) for c in CAMPS}
    taille = int(min(m.sum() for m in masques.values()))
    print(f"effectif commun aux trois camps : {taille}", flush=True)

    resume = []

    # ------------------------------------------------------------- 1. patrons
    tg = C.mesures(C.Indicatrice(codes1, ks).tables(
        C.poids_plein(masques["gauche"])))["n"][0]
    retenus = [j for j in range(len(items)) if tg[j] >= C.N_MIN_ITEM]
    dfp = patrons(codes1, masques, retenus, taille, 1, rng, 10, args.jeux)
    C.ecrire(dfp, "a30-structure-patrons.csv")
    piv = dfp.pivot_table(index="jeu", columns="camp", values="patrons")
    print("patrons distincts sur dix items, moyenne sur "
          f"{args.jeux} jeux d'items, {taille} personnes par camp :", flush=True)
    print(piv.mean().to_string(), flush=True)
    e, bas, haut, p = apparie(piv["droite"].values, piv["gauche"].values, args.boot, rng)
    resume.append({"test": "S1 patrons distincts, droite moins gauche",
                   "gauche": float(piv["gauche"].mean()),
                   "centre": float(piv["centre"].mean()),
                   "droite": float(piv["droite"].mean()), "ecart": e,
                   "ic_bas": bas, "ic_haut": haut, "p": p})

    # --------------------------------------------- 2 et 3. dimensions, clusters
    X, items_ord = matrice_ordinale(codes1, items, ks, options)
    print(f"{X.shape[1]} items ordinaux retenus pour l'ACP et le partitionnement",
          flush=True)
    dfd = dimensions_et_clusters(X, masques, taille, args.tirages, rng)
    C.ecrire(dfd, "a30-structure-dimensions.csv")
    agg = dfd.groupby("camp")[["var_pc1", "var_pc2", "n_axes_50", "n_axes_80",
                               "meilleur_k", "silhouette"]].mean()
    print(agg.to_string(), flush=True)
    C.ecrire(agg.reset_index(), "a30-structure-clusters.csv")
    for nom, col in [("S2 part de variance de la premiere composante", "var_pc1"),
                     ("S3 nombre de sous groupes retenu", "meilleur_k")]:
        a = dfd.loc[dfd["camp"] == "droite", col].values.astype(float)
        b = dfd.loc[dfd["camp"] == "gauche", col].values.astype(float)
        n = min(len(a), len(b))
        e, bas, haut, p = apparie(a[:n], b[:n], args.boot, rng)
        resume.append({"test": nom + " (droite moins gauche)",
                       "gauche": float(b.mean()),
                       "centre": float(dfd.loc[dfd["camp"] == "centre", col].mean()),
                       "droite": float(a.mean()), "ecart": e,
                       "ic_bas": bas, "ic_haut": haut, "p": p})

    # -------------------------------------------------------------- 4. axes
    sc = scores_axes(codes1, items, ks, camps["points7"])
    lignes = []
    for c in CAMPS:
        m = masques[c]
        e, s = sc["economique"][m], sc["social"][m]
        r = float(np.corrcoef(e, s)[0, 1])
        bt = np.empty(args.boot)
        for t in range(args.boot):
            i = rng.integers(0, m.sum(), m.sum())
            bt[t] = np.corrcoef(e[i], s[i])[0, 1]
        lignes.append({"camp": c, "n": int(m.sum()), "r_econ_social": r,
                       "ic_bas": float(np.percentile(bt, 2.5)),
                       "ic_haut": float(np.percentile(bt, 97.5)),
                       "et_economique": float(e.std()), "et_social": float(s.std()),
                       "n_items_econ": sc["economique_n_items"],
                       "n_items_social": sc["social_n_items"]})
    tout = np.corrcoef(sc["economique"], sc["social"])[0, 1]
    lignes.append({"camp": "population entiere", "n": len(ids), "r_econ_social": float(tout),
                   "ic_bas": np.nan, "ic_haut": np.nan,
                   "et_economique": float(sc["economique"].std()),
                   "et_social": float(sc["social"].std()),
                   "n_items_econ": sc["economique_n_items"],
                   "n_items_social": sc["social_n_items"]})
    dfa = pd.DataFrame(lignes)
    C.ecrire(dfa, "a30-structure-axes.csv")
    print(dfa.to_string(index=False), flush=True)

    # Difference de deux correlations mesurees sur deux groupes disjoints : bootstrap
    # independant sur les personnes de chaque camp, et p bilateral par permutation de
    # l'etiquette de camp entre les deux camps reunis.
    eg, sg = sc["economique"][masques["gauche"]], sc["social"][masques["gauche"]]
    ed, sd_ = sc["economique"][masques["droite"]], sc["social"][masques["droite"]]
    bt = np.empty(args.boot)
    for t in range(args.boot):
        i = rng.integers(0, len(ed), len(ed))
        j = rng.integers(0, len(eg), len(eg))
        bt[t] = np.corrcoef(ed[i], sd_[i])[0, 1] - np.corrcoef(eg[j], sg[j])[0, 1]
    et = np.concatenate([ed, eg])
    st = np.concatenate([sd_, sg])
    obs = np.corrcoef(ed, sd_)[0, 1] - np.corrcoef(eg, sg)[0, 1]
    nul = np.empty(args.boot)
    for t in range(args.boot):
        pm = rng.permutation(len(et))
        a1, a2 = pm[:len(ed)], pm[len(ed):]
        nul[t] = (np.corrcoef(et[a1], st[a1])[0, 1]
                  - np.corrcoef(et[a2], st[a2])[0, 1])
    p4 = (int((np.abs(nul) >= abs(obs)).sum()) + 1) / (args.boot + 1)
    resume.append({"test": "S4 correlation economique / social (droite moins gauche)",
                   "gauche": dfa.loc[dfa["camp"] == "gauche", "r_econ_social"].iloc[0],
                   "centre": dfa.loc[dfa["camp"] == "centre", "r_econ_social"].iloc[0],
                   "droite": dfa.loc[dfa["camp"] == "droite", "r_econ_social"].iloc[0],
                   "ecart": float(obs), "ic_bas": float(np.percentile(bt, 2.5)),
                   "ic_haut": float(np.percentile(bt, 97.5)), "p": p4})

    # ----------------------------------------------------- 5. Twin, patrons seulement
    # Sur Twin on ne porte que la mesure de patrons distincts. L'ACP et le
    # partitionnement demandent un codage ordinal, et le catalogue des auteurs ne declare
    # pas l'ordre des modalites hors des matrices de personnalite : les transposer
    # ici reviendrait a inventer une echelle.
    import a9_commun as T
    itw = T.table_items()
    w13 = T.charger_humains("1_3")
    colsw = [c for c in itw.index
             if c in w13.columns and itw.at[c, "domaine"] != "demographies"]
    codesw, ksw = C.coder_numerique(w13, colsw)
    campsw = C.camps_twin(w13)
    masquesw = {c: (campsw["bloc3"] == c) for c in CAMPS}
    taillew = int(min(m.sum() for m in masquesw.values()))
    indw = C.Indicatrice(codesw, ksw)
    nw = C.mesures(indw.tables(C.poids_plein(masquesw["gauche"])))["n"][0]
    retenusw = [j for j in range(len(colsw)) if nw[j] >= C.N_MIN_ITEM]
    dfpw = patrons(codesw, masquesw, retenusw, taillew, 1, rng, 10, args.jeux)
    dfpw["jeu_de_donnees"] = "Twin-2K-500"
    C.ecrire(dfpw, "a30-structure-patrons-twin.csv")
    pivw = dfpw.pivot_table(index="jeu", columns="camp", values="patrons")
    e, bas, haut, p = apparie(pivw["droite"].values, pivw["gauche"].values,
                              args.boot, rng)
    print(f"Twin, patrons distincts sur dix items, {taillew} personnes par camp :",
          flush=True)
    print(pivw.mean().to_string(), flush=True)
    resume.append({"test": "S1 bis patrons distincts sur Twin, droite moins gauche",
                   "gauche": float(pivw["gauche"].mean()),
                   "centre": float(pivw["centre"].mean()),
                   "droite": float(pivw["droite"].mean()), "ecart": e,
                   "ic_bas": bas, "ic_haut": haut, "p": p})

    dfr = pd.DataFrame(resume)
    ok = dfr["p"].notna()
    dfr.loc[ok, "p_holm"] = C.holm(dfr.loc[ok, "p"].values)
    C.ecrire(dfr, "a30-structure-resume.csv")
    print(dfr.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
