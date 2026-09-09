"""
c1_previsibilite : question 4 du mois 1 du programme C version menages.

Deux choses.

  1. La personne au dela de la cohorte : la chute sous permutation intra cohorte de la
     previsibilite de l'anticipation du mois suivant, a partir de l'historique du menage
     contre les demographies seules. C'est a44 applique a i1, transporte du categoriel au
     continu et du changement d'opinion a l'anticipation macroeconomique.

  2. Qui bouge au choc : la part des menages qui revisent, previsible ou non au dela de la
     cohorte, et le nul a derive de i1 transpose au continu.

La permutation est celle de a44_commun.permuter_intra, dont la definition est reutilisee
sans retouche par c1_commun.permuter_prepare, qui tire EXACTEMENT la meme permutation a
graine egale (controle C6 de c1_decrire) en extrayant les groupes une seule fois. Elle est
appliquee a l'interieur du couple (mois cible, cohorte) : ce qui est conserve est la cohorte
ET le mois, ce qui est detruit est ce qui distingue un menage d'un autre dans la meme
cohorte le meme mois. Le mois cible est donne a tous les predicteurs, son index et sa
moyenne : la tendance agregee est offerte a chacun, seule la prediction a l'interieur du
mois et de la cohorte est notee.

Usage : .venv/bin/python analyses/c1_previsibilite.py [variable ...]
        .venv/bin/python analyses/c1_previsibilite.py assembler

Sorties : c1-previsibilite-synthese.csv, c1-previsibilite-par-variable.csv,
c1-qui-bouge-choc.csv, c1-nul-a-derive.csv. Aucune microdonnee.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

import c1_commun as C1

N_PLIS = 5
N_BOOT = 400          # ecart declare : 400 et non 1 000, cout de calcul
PREDICTEURS = ["P", "D", "H", "HD", "F"]
TEMOINS = ["T1", "T0b"]
TOUS = PREDICTEURS + TEMOINS

DESCRIPTION = {
    "P": "persistance seule, x(i, t)",
    "D": "demographies seules, ridge",
    "H": "historique du menage, ridge",
    "HD": "historique et demographies, ridge",
    "F": "foret sur historique et demographies",
    "T1": "temoin de cohorte, moyenne de la cohorte au mois cible hors pli",
    "T0b": "temoin de cohorte a plein echantillon, constant dans (mois, cohorte)",
}


# ---------------------------------------------------------------------------
# 1. Le tableau des couples (menage, mois) -> (menage, mois + 1)
# ---------------------------------------------------------------------------

def paires(df, v, bornes):
    """Un couple par menage et par mois ou le menage repond au mois t et au mois t + 1.

    Les colonnes d'historique ne regardent JAMAIS le mois cible : x_t, x_{t-1}, moyenne et
    ecart type du menage sur ses mois d'index strictement inferieur a t + 1, et le nombre
    de ces mois.
    """
    x = C1.winsoriser(pd.to_numeric(df[v], errors="coerce").to_numpy(dtype=float), bornes[v])
    d = pd.DataFrame({"userid": df["userid"].to_numpy().astype(np.int64),
                      "t": df["t"].to_numpy().astype(int),
                      "cohorte_code": df["cohorte_code"].to_numpy(),
                      "tenure": pd.to_numeric(df["tenure"], errors="coerce").to_numpy(),
                      "x": x})
    for c in C1.DEMOS:
        d[c] = df[c].to_numpy()
    d = d[np.isfinite(d["x"])].sort_values(["userid", "t"]).reset_index(drop=True)
    g = d.groupby("userid")["x"]
    d["hist_moy"] = g.transform(lambda s: s.expanding().mean())
    d["hist_ect"] = g.transform(lambda s: s.expanding().std())
    d["hist_n"] = g.cumcount() + 1
    d["x_prec"] = g.shift(1)
    # la cible est la valeur du menage au mois suivant, quel que soit l'ecart reel de mois ;
    # on n'accepte que les couples exactement consecutifs
    suiv = d[["userid", "t", "x"]].copy()
    suiv["t"] = suiv["t"] - 1
    suiv = suiv.rename(columns={"x": "y"})
    p = d.merge(suiv, on=["userid", "t"], how="inner")
    p["t_cible"] = p["t"] + 1
    return p.reset_index(drop=True)


def matrices(p):
    """Les blocs de colonnes.

    Le mois cible est donne a TOUS les predicteurs, sous deux colonnes : son index et la
    moyenne de la cible sur ce mois, calculee sur tout le perimetre. C'est la tendance
    agregee offerte a chacun, ce que le nul a derive de i1 donne a tout le monde ; seule la
    prediction a l'interieur du mois et de la cohorte est notee par la chute sous
    permutation. Deux colonnes plutot que soixante-neuf indicatrices : la foret mettait
    quatre minutes par variable avec les indicatrices et vingt secondes avec la moyenne, et
    l'information portee est la meme puisqu'elle est constante par mois.
    """
    mois = np.column_stack([
        p["t_cible"].to_numpy(dtype=float),
        p.groupby("t_cible")["y"].transform("mean").to_numpy(dtype=float),
    ])
    demo = pd.get_dummies(p[C1.DEMOS].astype(str), dummy_na=False).to_numpy(dtype=float)
    ten = np.nan_to_num(p["tenure"].to_numpy(dtype=float), nan=0.0)[:, None]
    hist = np.column_stack([
        p["x"].to_numpy(dtype=float),
        np.nan_to_num(p["x_prec"].to_numpy(dtype=float),
                      nan=float(np.nanmean(p["x"].to_numpy(dtype=float)))),
        p["hist_moy"].to_numpy(dtype=float),
        np.nan_to_num(p["hist_ect"].to_numpy(dtype=float), nan=0.0),
        p["hist_n"].to_numpy(dtype=float),
    ])
    return {"mois": mois, "demo": np.column_stack([demo, ten]), "hist": hist}


def scores_hors_pli(p, blocs, graine=C1.GRAINE):
    """Un score par couple et par predicteur, toujours estime hors du pli du menage."""
    n = len(p)
    y = p["y"].to_numpy(dtype=float)
    users = p["userid"].to_numpy()
    uniques = np.unique(users)
    rng = np.random.default_rng(graine)
    pli_menage = {u: k for u, k in zip(uniques, rng.integers(0, N_PLIS, size=len(uniques)))}
    pli = np.array([pli_menage[u] for u in users])

    X = {
        "D": np.column_stack([blocs["demo"], blocs["mois"]]),
        "H": np.column_stack([blocs["hist"], blocs["mois"]]),
        "HD": np.column_stack([blocs["hist"], blocs["demo"], blocs["mois"]]),
        "F": np.column_stack([blocs["hist"], blocs["demo"], blocs["mois"]]),
    }
    s = {m: np.full(n, np.nan) for m in TOUS}
    s["P"] = p["x"].to_numpy(dtype=float)          # persistance, aucun ajustement

    # T0b : la moyenne de la cohorte au mois cible, estimee sur TOUT le perimetre et non
    # hors pli, donc rigoureusement constante a l'interieur d'un couple (mois, cohorte),
    # qui est exactement le groupe dans lequel la permutation a lieu. Sa chute doit valoir
    # zero a la precision machine : c'est la verification d'implementation, lecon E3 de i1.
    # Un temoin constant par MOIS seulement donnerait un Spearman intra mois indefini ; le
    # temoin doit varier a l'interieur du mois pour etre notable, et etre constant a
    # l'interieur du groupe de permutation pour que sa chute soit exactement nulle.
    s["T0b"] = p.groupby(["t_cible", "cohorte_code"])["y"].transform("mean") \
                .to_numpy(dtype=float)

    for k in range(N_PLIS):
        tr, te = pli != k, pli == k
        if te.sum() == 0 or tr.sum() < 100:
            continue
        # T1 : moyenne de la cohorte au mois cible, estimee sur le pli d'entrainement,
        # repliee sur la moyenne du mois sous N_MIN_COHORTE menages.
        ent = p[tr]
        cle = ["t_cible", "cohorte_code"]
        agg = ent.groupby(cle)["y"].agg(["mean", "size"]).reset_index()
        agg = agg[agg["size"] >= C1.N_MIN_COHORTE]
        m_mois = ent.groupby("t_cible")["y"].mean()
        jointe = p.loc[te, cle].merge(agg, on=cle, how="left")
        val = jointe["mean"].to_numpy(dtype=float)
        repli = p.loc[te, "t_cible"].map(m_mois).to_numpy(dtype=float)
        s["T1"][te] = np.where(np.isfinite(val), val, repli)

        for m in ("D", "H", "HD"):
            mod = Ridge(alpha=1.0)
            mod.fit(X[m][tr], y[tr])
            s[m][te] = mod.predict(X[m][te])
        f = RandomForestRegressor(n_estimators=200, min_samples_leaf=20, n_jobs=4,
                                  random_state=C1.GRAINE + k)
        f.fit(X["F"][tr], y[tr])
        s["F"][te] = f.predict(X["F"][te])
    return s


# ---------------------------------------------------------------------------
# 2. Score agrege, permutation, bootstrap
# ---------------------------------------------------------------------------

def groupes(p):
    """Code entier du couple (mois cible, cohorte). La permutation se fait dedans."""
    cle = p["t_cible"].astype(np.int64) * 100000 + p["cohorte_code"].astype(np.int64)
    return pd.factorize(cle)[0].astype(np.int32)


class Contexte:
    """Le decoupage par mois cible, prepare une fois, et le Spearman par mois vectorise.

    Pourquoi cette classe existe. La quantite de verdict est une moyenne ponderee de
    correlations de Spearman calculees mois par mois, et elle est recalculee deux cent fois
    par predicteur pour la permutation et quatre cents fois de plus pour le bootstrap. La
    permutation preenregistree echange les menages a l'interieur du couple (mois, cohorte) :
    elle ne fait donc jamais sortir un menage de son mois, et **l'ensemble des rangs du
    score a l'interieur d'un mois est invariant sous permutation**. Les rangs peuvent donc
    etre calcules une seule fois par predicteur, et chaque permutation se reduit a un
    reindexage et a une somme par mois. Sans cela le calcul complet demandait trois heures.
    """

    def __init__(self, y, mois, poids_min=50):
        codes, inv = np.unique(mois, return_inverse=True)
        eff = np.bincount(inv)
        self.sel = (eff >= poids_min)[inv]
        _, self.m = np.unique(inv[self.sel], return_inverse=True)
        self.n_m = np.bincount(self.m).astype(float)
        # les indices de chaque mois, calcules UNE fois : les recalculer par
        # np.flatnonzero(m == k) a chaque appel coutait un balayage complet par mois.
        ordre = np.argsort(self.m, kind="mergesort")
        coupures = np.cumsum(self.n_m.astype(int))[:-1]
        self.idx = np.split(ordre, coupures)
        self.y = np.asarray(y, dtype=float)[self.sel]
        self.ry, self.ny = self.centrer(self.y)
        self.total = float(self.n_m.sum())

    def centrer(self, x):
        """Rangs par mois, centres par mois, et norme de chaque mois."""
        x = np.asarray(x, dtype=float)
        r = np.empty(len(x), dtype=float)
        for idx in self.idx:
            r[idx] = C1.rangs(x[idx])
        moy = np.bincount(self.m, weights=r) / self.n_m
        c = r - moy[self.m]
        norme = np.sqrt(np.bincount(self.m, weights=c * c))
        return c, norme

    def rho(self, rs, ns):
        """Moyenne ponderee des Spearman par mois, a partir des rangs centres deja calcules."""
        num = np.bincount(self.m, weights=self.ry * rs)
        with np.errstate(invalid="ignore", divide="ignore"):
            par_mois = np.where((self.ny > 0) & (ns > 0), num / (self.ny * ns), np.nan)
        ok = np.isfinite(par_mois)
        if not ok.any():
            return np.nan
        return float(np.sum(par_mois[ok] * self.n_m[ok]) / np.sum(self.n_m[ok]))

    def preparer_score(self, score):
        return self.centrer(np.asarray(score, dtype=float)[self.sel])


def tranches(mois, poids_min=50):
    """Indices des couples de chaque mois cible, calcules une seule fois.

    Les recalculer a chaque permutation et a chaque tirage de bootstrap coutait la moitie
    du temps de calcul.
    """
    ordre = np.argsort(mois, kind="mergesort")
    m = mois[ordre]
    coupures = np.flatnonzero(np.r_[True, m[1:] != m[:-1], True])
    out = []
    for a, b in zip(coupures[:-1], coupures[1:]):
        if b - a >= poids_min:
            out.append(ordre[a:b])
    return out


def rho_tranches(y, score, tr, rangs_y=None):
    """Spearman par mois puis moyenne ponderee par l'effectif du mois.

    rangs_y, s'il est fourni, evite de reclasser la cible a chaque permutation : elle ne
    change pas d'une permutation a l'autre.
    """
    num, den = 0.0, 0.0
    for k, idx in enumerate(tr):
        s = score[idx]
        if not np.all(np.isfinite(s)):
            s = s[np.isfinite(s)]
            if len(s) < 50:
                continue
        ry = rangs_y[k] if rangs_y is not None else C1.rangs(y[idx])
        rs = C1.rangs(score[idx])
        if rs.std() == 0 or ry.std() == 0:
            continue
        r = float(np.corrcoef(ry, rs)[0, 1])
        if np.isfinite(r):
            num += r * len(idx)
            den += len(idx)
    return num / den if den else np.nan


def rho_par_mois(y, score, mois, poids_min=50):
    """Version simple, conservee pour les appels ponctuels."""
    return rho_tranches(y, score, tranches(mois, poids_min))


def mesurer(p, s, n_perm=C1.N_PERMUTATIONS, n_boot=N_BOOT, graine=C1.GRAINE):
    y = p["y"].to_numpy(dtype=float)
    mois = p["t_cible"].to_numpy()
    g = groupes(p)
    users = p["userid"].to_numpy()
    rng = np.random.default_rng(graine)

    ctx = Contexte(y, mois)
    g_sel = g[ctx.sel]
    gr = C1.preparer_groupes(g_sel)
    n_sel = int(ctx.sel.sum())

    lignes = []
    for m in TOUS:
        rs, ns = ctx.preparer_score(s[m])
        rho = ctx.rho(rs, ns)
        tirages = np.array([ctx.rho(rs[C1.permuter_prepare(n_sel, gr, rng)], ns)
                            for _ in range(n_perm)])
        chute = rho - float(np.nanmean(tirages))
        lignes.append({"predicteur": m, "description": DESCRIPTION[m],
                       "rho": rho, "rho_permute": float(np.nanmean(tirages)),
                       "chute": chute,
                       "p_permutation_empirique": C1.p_empirique(rho, tirages),
                       "p_permutation_normal": C1.p_normal(rho, tirages),
                       "n_couples": int(len(y)), "n_menages": int(len(np.unique(users)))})

    # bootstrap sur les menages, permutation fraiche a chaque tirage
    uniq = np.unique(users)
    par_menage = {u: np.flatnonzero(users == u) for u in uniq}
    acc = {m: {"rho": [], "chute": []} for m in TOUS}
    for b in range(n_boot):
        ch = rng.choice(uniq, size=len(uniq), replace=True)
        idx = np.concatenate([par_menage[u] for u in ch])
        cb = Contexte(y[idx], mois[idx])
        gb = g[idx][cb.sel]
        perm = C1.permuter_prepare(len(gb), C1.preparer_groupes(gb), rng)
        for m in TOUS:
            rs, ns = cb.preparer_score(s[m][idx])
            r = cb.rho(rs, ns)
            rp = cb.rho(rs[perm], ns)
            acc[m]["rho"].append(r)
            acc[m]["chute"].append(r - rp)
        if (b + 1) % 100 == 0:
            print(f"    bootstrap {b + 1}/{n_boot}", flush=True)
    for ligne in lignes:
        a = acc[ligne["predicteur"]]
        lo, hi = C1.ic(a["rho"])
        clo, chi = C1.ic(a["chute"])
        ligne.update({"rho_ic_bas": lo, "rho_ic_haut": hi,
                      "chute_ic_bas": clo, "chute_ic_haut": chi})
    return lignes


# ---------------------------------------------------------------------------
# 3. Qui bouge au choc
# ---------------------------------------------------------------------------

def qui_bouge(df, v, bornes, t_choc, etiquette, n_perm=C1.N_PERMUTATIONS,
              n_boot=N_BOOT, graine=C1.GRAINE):
    """Revision au choc, previsible ou non au dela de la cohorte, plus le nul a derive."""
    x = C1.winsoriser(pd.to_numeric(df[v], errors="coerce").to_numpy(dtype=float), bornes[v])
    d = pd.DataFrame({"userid": df["userid"].to_numpy().astype(np.int64),
                      "t": df["t"].to_numpy().astype(int),
                      "cohorte_code": df["cohorte_code"].to_numpy(), "x": x})
    for c in C1.DEMOS:
        d[c] = df[c].to_numpy()
    d = d[np.isfinite(d["x"])]
    avant = list(range(t_choc - 3, t_choc))
    apres = list(range(t_choc, t_choc + 3))
    a = d[d["t"].isin(avant)].groupby("userid").agg(
        x_avant=("x", "mean"), n_avant=("x", "size"), sd_avant=("x", "std"),
        cohorte_code=("cohorte_code", "last"))
    for c in C1.DEMOS:
        a[c] = d[d["t"].isin(avant)].groupby("userid")[c].last()
    b = d[d["t"].isin(apres)].groupby("userid").agg(x_apres=("x", "mean"))
    # l'ecart type d'avant est calcule sur au plus trois mois ; il est complete par
    # l'historique complet anterieur au choc quand il existe
    hist = d[d["t"] < t_choc].groupby("userid")["x"].agg(["std", "size", "mean"])
    hist.columns = ["sd_hist", "n_hist", "moy_hist"]
    j = a.join(b, how="inner").join(hist, how="left").reset_index()
    j = j[np.isfinite(j["x_avant"]) & np.isfinite(j["x_apres"])]
    if len(j) < C1.N_MIN_CHOC:
        return None, None

    j["R"] = j["x_apres"] - j["x_avant"]
    seuil = float(np.median(np.abs(j["R"])))
    j["Y_rev"] = (np.abs(j["R"]) > seuil).astype(int)
    j["Y_dir"] = (j["R"] > 0).astype(int)

    demo = pd.get_dummies(j[C1.DEMOS].astype(str), dummy_na=False).to_numpy(dtype=float)
    hi = np.column_stack([
        j["x_avant"].to_numpy(dtype=float),
        np.nan_to_num(j["sd_avant"].to_numpy(dtype=float), nan=0.0),
        np.nan_to_num(j["sd_hist"].to_numpy(dtype=float), nan=0.0),
        np.nan_to_num(j["moy_hist"].to_numpy(dtype=float),
                      nan=float(j["x_avant"].mean())),
        np.nan_to_num(j["n_hist"].to_numpy(dtype=float), nan=1.0),
    ])
    jeux = {"V": np.nan_to_num(j["sd_hist"].to_numpy(dtype=float), nan=0.0)[:, None],
            "N": np.abs(j["x_avant"].to_numpy(dtype=float)
                        - float(j["x_avant"].mean()))[:, None],
            "L": -j["x_avant"].to_numpy(dtype=float)[:, None],
            "D": demo, "H": hi, "HD": np.column_stack([hi, demo])}
    descr = {"V": "volatilite passee du menage seule",
             "N": "ecart au niveau moyen avant le choc, seul",
             "L": "niveau d'avant le choc seul, signe, retour a la moyenne",
             "D": "demographies seules", "H": "historique du menage",
             "HD": "historique et demographies"}

    g = pd.factorize(j["cohorte_code"])[0].astype(np.int32)
    users = j["userid"].to_numpy()
    rng = np.random.default_rng(graine)
    pli = rng.integers(0, N_PLIS, size=len(j))

    lignes = []
    for cible in ("Y_rev", "Y_dir"):
        yv = j[cible].to_numpy()
        scores = {}
        for nom, X in jeux.items():
            sc = np.full(len(j), np.nan)
            if X.shape[1] == 1:
                sc = X[:, 0].astype(float)      # aucun ajustement, une colonne
            else:
                for k in range(N_PLIS):
                    tr, te = pli != k, pli == k
                    if te.sum() == 0 or len(np.unique(yv[tr])) < 2:
                        continue
                    f = RandomForestClassifier(n_estimators=200, min_samples_leaf=20,
                                               n_jobs=4, random_state=C1.GRAINE + k)
                    f.fit(X[tr], yv[tr])
                    sc[te] = f.predict_proba(X[te])[:, 1]
            scores[nom] = sc
        # temoin constant
        scores["T0b"] = np.zeros(len(j))
        descr["T0b"] = "temoin constant"
        for nom, sc in scores.items():
            auc = C1.auc(yv, sc)
            gr = C1.preparer_groupes(g)
            tir = np.array([C1.auc(yv, sc[C1.permuter_prepare(len(g), gr, rng)])
                            for _ in range(n_perm)])
            chute = auc - float(np.nanmean(tir))
            boot = []
            for _ in range(n_boot):
                idx = rng.integers(0, len(j), size=len(j))
                if len(np.unique(yv[idx])) < 2:
                    continue
                pp = C1.permuter_prepare(len(idx), C1.preparer_groupes(g[idx]), rng)
                boot.append(C1.auc(yv[idx], sc[idx]) - C1.auc(yv[idx], sc[idx][pp]))
            clo, chi = C1.ic(boot)
            lignes.append({"variable": v, "regle_choc": etiquette,
                           "mois_choc": C1.nom_mois(t_choc), "cible": cible,
                           "predicteur": nom, "description": descr[nom],
                           "n_menages": int(len(j)), "taux_de_base": float(yv.mean()),
                           "auc": auc, "auc_permutee": float(np.nanmean(tir)),
                           "chute": chute, "chute_ic_bas": clo, "chute_ic_haut": chi,
                           "p_permutation_normal": C1.p_normal(auc, tir),
                           "p_permutation_empirique": C1.p_empirique(auc, tir)})

    # nul a derive : les valeurs d'apres sont remelangees entre menages de la meme cohorte.
    # Les deux distributions marginales, avant et apres, et la derive par cohorte sont donc
    # conservees ; seul l'appariement des menages est detruit.
    derive = float(j["x_apres"].mean() - j["x_avant"].mean())
    sens = np.sign(derive) if derive != 0 else 1.0
    obs_sens = float((np.sign(j["R"]) == sens).mean())
    obs_ampleur = float(np.mean(np.abs(j["R"])))
    parts, ampleurs = [], []
    xa = j["x_apres"].to_numpy(dtype=float)
    gr2 = C1.preparer_groupes(g)
    for _ in range(50):
        perm = C1.permuter_prepare(len(g), gr2, rng)
        r = xa[perm] - j["x_avant"].to_numpy(dtype=float)
        parts.append(float((np.sign(r) == sens).mean()))
        ampleurs.append(float(np.mean(np.abs(r))))
    nul = {"variable": v, "regle_choc": etiquette, "mois_choc": C1.nom_mois(t_choc),
           "n_menages": int(len(j)), "derive_agregee": derive,
           "part_dans_le_sens_observee": obs_sens,
           "part_dans_le_sens_nul": float(np.mean(parts)),
           "exces_observe_sur_nul": obs_sens - float(np.mean(parts)),
           "ampleur_moyenne_observee": obs_ampleur,
           "ampleur_moyenne_nul": float(np.mean(ampleurs)),
           "ratio_ampleur": obs_ampleur / float(np.mean(ampleurs))
           if np.mean(ampleurs) else np.nan}
    return lignes, nul


# ---------------------------------------------------------------------------
# 4. Programme
# ---------------------------------------------------------------------------

def calculer(variables=None):
    """Calcule et met en cache les lignes brutes, variable par variable.

    Le cache par variable existe pour une raison pratique : le calcul complet dure une
    vingtaine de minutes et la session le lance en plusieurs fois. Il est deterministe,
    les graines sont fixes, et relancer avec la meme variable reecrit la meme ligne.
    """
    df = C1.charger(C1.PRIMAIRE)
    toutes = C1.VAR_PRIMAIRES + ["infl1_var", "infl1_point"]
    variables = variables or toutes
    bornes = C1.bornes_winsor(df, toutes)
    choc = pd.read_csv(C1.os.path.join(C1.SORTIE, "c1-choc-2025.csv"))
    t_prim = int(choc[choc["regle"].str.startswith("primaire")]["t"].iloc[0])
    t_sec = int(choc[choc["regle"].str.startswith("secondaire")]["t"].iloc[0])
    C1.os.makedirs(C1.CACHE, exist_ok=True)

    for v in variables:
        print(f"  {v} ...", flush=True)
        p = paires(df, v, bornes)
        print(f"    {len(p)} couples, {p['userid'].nunique()} menages", flush=True)
        s = scores_hors_pli(p, matrices(p))
        lignes = mesurer(p, s)
        for ligne in lignes:
            ligne["variable"] = v
            ligne["libelle"] = C1.LIBELLE[v]
        pd.DataFrame(lignes).to_csv(
            C1.os.path.join(C1.CACHE, f"prev-{v}.csv"), index=False)

        l_bouge, l_nul = [], []
        for cle, t in (("primaire, saut de moyenne", t_prim),
                       ("secondaire, saut d'IQR", t_sec)):
            res, nul = qui_bouge(df, v, bornes, t, cle)
            if res is None:
                continue
            l_bouge.extend(res)
            l_nul.append(nul)
        pd.DataFrame(l_bouge).to_csv(
            C1.os.path.join(C1.CACHE, f"bouge-{v}.csv"), index=False)
        pd.DataFrame(l_nul).to_csv(
            C1.os.path.join(C1.CACHE, f"nul-{v}.csv"), index=False)
        print(f"    {v} termine", flush=True)


def assembler():
    """Assemble les caches par variable, applique la correction pour tests multiples."""
    toutes = C1.VAR_PRIMAIRES + ["infl1_var", "infl1_point"]
    tab = pd.concat([pd.read_csv(C1.os.path.join(C1.CACHE, f"prev-{v}.csv"))
                     for v in toutes], ignore_index=True)

    # correction pour tests multiples sur la famille des variables x predicteurs
    fam = tab["predicteur"].isin(PREDICTEURS)
    p_norm = tab.loc[fam, "p_permutation_normal"].fillna(1.0).to_numpy()
    tab.loc[fam, "p_holm"] = C1.holm(p_norm)
    tab.loc[fam, "p_bh"] = C1.benjamini_hochberg(p_norm)
    tab["retenu_holm"] = tab["p_holm"] < 0.05
    C1.ecrire(tab[["variable", "libelle", "predicteur", "description", "n_couples",
                   "n_menages", "rho", "rho_ic_bas", "rho_ic_haut", "rho_permute",
                   "chute", "chute_ic_bas", "chute_ic_haut", "p_permutation_empirique",
                   "p_permutation_normal", "p_holm", "p_bh", "retenu_holm"]],
              "c1-previsibilite-par-variable.csv")

    synth = tab.groupby(["predicteur", "description"]).agg(
        rho_moyen=("rho", "mean"), chute_moyenne=("chute", "mean"),
        chute_min=("chute", "min"), chute_max=("chute", "max"),
        variables_retenues=("retenu_holm", "sum")).reset_index()
    synth = synth.sort_values("chute_moyenne", ascending=False)
    C1.ecrire(synth, "c1-previsibilite-synthese.csv")

    tb = pd.concat([pd.read_csv(C1.os.path.join(C1.CACHE, f"bouge-{v}.csv"))
                    for v in toutes], ignore_index=True)
    fam = tb["predicteur"] != "T0b"
    tb.loc[fam, "p_holm"] = C1.holm(
        tb.loc[fam, "p_permutation_normal"].fillna(1.0).to_numpy())
    tb["retenu_holm"] = tb["p_holm"] < 0.05
    C1.ecrire(tb, "c1-qui-bouge-choc.csv")
    C1.ecrire(pd.concat([pd.read_csv(C1.os.path.join(C1.CACHE, f"nul-{v}.csv"))
                         for v in toutes], ignore_index=True), "c1-nul-a-derive.csv")


def main():
    import sys
    args = sys.argv[1:]
    if args == ["assembler"]:
        assembler()
    else:
        calculer(args or None)
        if not args:
            assembler()
    print("c1_previsibilite termine")


if __name__ == "__main__":
    main()
