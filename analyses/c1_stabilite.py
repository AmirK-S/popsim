"""
c1_stabilite : question 3 du mois 1 du programme C version menages.

Le plancher de reinterrogation. La SCE reinterroge le meme menage jusqu'a douze mois de
suite : c'est le retest gratuit dont le dossier a fait son differentiateur (a12, a44), ici
sur des variables continues et a onze delais au lieu de trois.

Deux quantites, preenregistrement section 4.3 :
  - la correlation de retest a delai k, k de 1 a 11 mois, apres retrait de la moyenne du
    mois de chaque cote, pour que la derive agregee n'alimente pas la correlation ;
  - la part stable, decomposition menage / residu par analyse de variance sans biais, et sa
    verification non circulaire par le croisement des mois pairs et des mois impairs.

Sorties : c1-retest-par-delai.csv, c1-part-stable.csv. Aucune microdonnee.
"""

import numpy as np
import pandas as pd

import c1_commun as C1


def centrer_par_mois(df, v, bornes):
    """La variable, winsorisee, moins la moyenne de son mois. Renvoie un DataFrame reduit."""
    x = C1.winsoriser(pd.to_numeric(df[v], errors="coerce").to_numpy(dtype=float), bornes[v])
    d = pd.DataFrame({"userid": df["userid"].to_numpy(), "t": df["t"].to_numpy(),
                      "cohorte_code": df["cohorte_code"].to_numpy(), "x": x})
    d = d[np.isfinite(d["x"])]
    d["x_c"] = d["x"] - d.groupby("t")["x"].transform("mean")
    return d


def retest_par_delai(d, k_max=11, n_boot=200, graine=C1.GRAINE):
    """Correlation de Spearman entre x(i, t) et x(i, t + k), pour k de 1 a k_max.

    L'unite de reechantillonnage du bootstrap est le MENAGE, pas le couple : un menage
    fournit jusqu'a onze couples et ils ne sont pas independants.
    """
    rng = np.random.default_rng(graine)
    index = {(int(u), int(t)): i for i, (u, t) in
             enumerate(zip(d["userid"].to_numpy(), d["t"].to_numpy()))}
    xc = d["x_c"].to_numpy()
    users = d["userid"].to_numpy()
    lignes = []
    for k in range(1, k_max + 1):
        a, b, u = [], [], []
        for i, (uu, tt) in enumerate(zip(users, d["t"].to_numpy())):
            j = index.get((int(uu), int(tt) + k))
            if j is not None:
                a.append(xc[i]); b.append(xc[j]); u.append(int(uu))
        if len(a) < 100:
            lignes.append({"delai_mois": k, "n_couples": len(a), "n_menages": 0,
                           "rho": np.nan, "ic_bas": np.nan, "ic_haut": np.nan})
            continue
        a, b, u = np.array(a), np.array(b), np.array(u)
        rho = C1.spearman(a, b)
        # bootstrap sur les menages
        uniques = np.unique(u)
        par_menage = {uu: np.flatnonzero(u == uu) for uu in uniques}
        tirages = []
        for _ in range(n_boot):
            ch = rng.choice(uniques, size=len(uniques), replace=True)
            idx = np.concatenate([par_menage[c] for c in ch])
            tirages.append(C1.spearman(a[idx], b[idx]))
        lo, hi = C1.ic(tirages)
        lignes.append({"delai_mois": k, "n_couples": len(a), "n_menages": len(uniques),
                       "rho": rho, "ic_bas": lo, "ic_haut": hi})
    return lignes


def part_stable(d, n_min_obs=3, n_boot=200, graine=C1.GRAINE):
    """Decomposition menage / residu sur les valeurs centrees par mois.

    Analyse de variance a un facteur aleatoire, estimateur sans biais :
      sigma_entre^2 = (MS_entre - MS_intra) / n_0,  n_0 = (N - somme n_i^2 / N) / (I - 1)
      sigma_intra^2 = MS_intra
    part_stable = sigma_entre^2 / (sigma_entre^2 + sigma_intra^2). Elle peut sortir
    negative sur un estimateur sans biais ; elle est alors publiee negative.
    """
    g = d.groupby("userid")["x_c"]
    n_i = g.size()
    garde = n_i[n_i >= n_min_obs].index
    dd = d[d["userid"].isin(garde)]
    if len(dd) < 100:
        return {"n_menages": 0}
    y = dd["x_c"].to_numpy()
    u = dd["userid"].to_numpy()
    cles, inv = np.unique(u, return_inverse=True)
    n = len(y)
    I = len(cles)
    eff = np.bincount(inv)
    moy = np.bincount(inv, weights=y) / eff
    grand = y.mean()
    ss_entre = float(np.sum(eff * (moy - grand) ** 2))
    ss_intra = float(np.sum((y - moy[inv]) ** 2))
    ms_entre = ss_entre / max(I - 1, 1)
    ms_intra = ss_intra / max(n - I, 1)
    n0 = (n - np.sum(eff ** 2) / n) / max(I - 1, 1)
    s_entre = (ms_entre - ms_intra) / n0
    s_intra = ms_intra
    denom = s_entre + s_intra
    part = s_entre / denom if denom > 0 else np.nan

    # verification non circulaire : mois pairs contre mois impairs
    dd = dd.copy()
    dd["pair"] = dd["t"] % 2
    piv = dd.groupby(["userid", "pair"])["x_c"].mean().unstack()
    piv = piv.dropna()
    rho_pi = C1.spearman(piv[0].to_numpy(), piv[1].to_numpy()) if len(piv) > 30 else np.nan

    # bootstrap sur les menages pour la part stable
    rng = np.random.default_rng(graine)
    par_menage = {c: np.flatnonzero(inv == k) for k, c in enumerate(cles)}
    tirages = []
    for _ in range(n_boot):
        ch = rng.choice(cles, size=len(cles), replace=True)
        idx = np.concatenate([par_menage[c] for c in ch])
        yy = y[idx]
        gg = np.repeat(np.arange(len(ch)), [len(par_menage[c]) for c in ch])
        e2 = np.bincount(gg)
        m2 = np.bincount(gg, weights=yy) / e2
        n2, I2 = len(yy), len(ch)
        mse = float(np.sum(e2 * (m2 - yy.mean()) ** 2)) / max(I2 - 1, 1)
        msi = float(np.sum((yy - m2[gg]) ** 2)) / max(n2 - I2, 1)
        nn0 = (n2 - np.sum(e2 ** 2) / n2) / max(I2 - 1, 1)
        se = (mse - msi) / nn0
        tirages.append(se / (se + msi) if (se + msi) > 0 else np.nan)
    lo, hi = C1.ic(tirages)
    # La correlation pairs / impairs porte sur des MOYENNES d'environ n/(2I) mois chacune,
    # elle est donc mecaniquement plus haute que la fidelite d'une observation isolee. La
    # formule de Spearman et Brown la ramene a une observation ; c'est cette valeur ramenee
    # qui est comparable a part_stable, et l'ecart publie est celui la.
    k = max(n / I / 2.0, 1.0)
    rho_1 = (rho_pi / (k - (k - 1) * rho_pi)) if np.isfinite(rho_pi) and rho_pi > 0 else np.nan
    return {"n_menages": I, "n_observations": n, "obs_par_menage": n / I,
            "sigma2_entre": s_entre, "sigma2_intra": s_intra,
            "part_stable": part, "ic_bas": lo, "ic_haut": hi,
            "rho_pairs_impairs": rho_pi, "k_spearman_brown": k,
            "rho_pairs_impairs_ramene": rho_1,
            "ecart_deux_estimateurs": abs(part - rho_1) if np.isfinite(rho_1) else np.nan}


def main():
    df = C1.charger(C1.PRIMAIRE)
    variables = C1.VAR_PRIMAIRES + ["infl1_var", "infl1_point"]
    bornes = C1.bornes_winsor(df, variables)

    l_retest, l_stable = [], []
    for v in variables:
        d = centrer_par_mois(df, v, bornes)
        print(f"  {v} : {len(d)} observations, {d['userid'].nunique()} menages", flush=True)
        for ligne in retest_par_delai(d):
            ligne["variable"] = v
            ligne["libelle"] = C1.LIBELLE[v]
            l_retest.append(ligne)
        s = part_stable(d)
        s["variable"] = v
        s["libelle"] = C1.LIBELLE[v]
        l_stable.append(s)

    C1.ecrire(pd.DataFrame(l_retest)[["variable", "libelle", "delai_mois", "n_couples",
                                      "n_menages", "rho", "ic_bas", "ic_haut"]],
              "c1-retest-par-delai.csv")
    C1.ecrire(pd.DataFrame(l_stable), "c1-part-stable.csv")
    print("c1_stabilite termine")


if __name__ == "__main__":
    main()
