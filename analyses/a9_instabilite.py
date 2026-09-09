"""
a9_instabilite : tache 3, la structure de l'instabilite humaine reelle entre vagues.

Sur les 108 items categoriels reposes en vague 4, on decrit qui change, sur quels items,
et vers quoi. La comparaison se fait contre trois modeles de bruit qui, tous, reproduisent
le meme taux de changement global : bruit uniforme, bruit marginal, bruit adjacent. C'est
la base d'un correctif d'injection d'incoherence structuree.

Aucun appel de modele de langage. Sorties agregees dans resultats/.

Usage : .venv/bin/python analyses/a9_instabilite.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a9_commun as A  # noqa: E402

RES = A.RACINE / "resultats"
GRAINE = 20260907

# Items ordinaux a echelle explicite : le pas de changement y a un sens.
ORDINAUX = ([f"QID287_{i}" for i in ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]]
            + [f"QID288_{i}" for i in range(1, 5)]
            + [f"QID289_{i}" for i in range(1, 5)])


def main():
    RES.mkdir(exist_ok=True)
    cat = A.charger_catalogue()
    items = A.table_items(cat)
    w13 = A.charger_humains("1_3", cat)
    w4 = A.charger_humains("4", cat)

    cols = [c for c in items.index if c in w4.columns and c in w13.columns
            and items.at[c, "domaine"] in A.ORDRE_DOMAINES]
    a, b = w13[cols], w4[cols]
    dispo = a.notna() & b.notna()
    change = ((a != b) & dispo)

    # -- 1. Qui change : distribution individuelle contre modele homogene -------
    n_i = dispo.sum(axis=1)
    p_i = (change.sum(axis=1) / n_i.replace(0, np.nan)).dropna()
    p_bar = float(change.sum().sum() / dispo.sum().sum())
    n_moy = float(n_i[n_i > 0].mean())
    var_obs = float(p_i.var(ddof=1))
    var_binom = p_bar * (1 - p_bar) / n_moy
    # Part de la variance individuelle qui n'est pas du bruit d'echantillonnage.
    var_vraie = max(var_obs - var_binom, 0.0)

    # -- 2. Sur quels items : dispersion des taux item par item ----------------
    p_j = (change.sum() / dispo.sum().replace(0, np.nan)).dropna()
    ent = pd.Series({c: A.entropie_col(w13[c]) for c in p_j.index}) \
        if hasattr(A, "entropie_col") else None
    if ent is None:
        ent = pd.Series({c: _entropie(w13[c]) for c in p_j.index})
    n_mod = pd.Series({c: int(w13[c].dropna().nunique()) for c in p_j.index})

    lignes = [dict(mesure="taux de changement global", valeur=round(p_bar, 4),
                   detail=f"{int(change.sum().sum())} changements sur "
                          f"{int(dispo.sum().sum())} cellules, {len(cols)} items"),
              dict(mesure="taux de stabilite global", valeur=round(1 - p_bar, 4),
                   detail="a comparer au plancher de 0.7953 du GSS a deux semaines"),
              dict(mesure="ecart type inter personnes du taux de changement",
                   valeur=round(float(p_i.std(ddof=1)), 4),
                   detail=f"n = {len(p_i)} personnes, {n_moy:.1f} items en moyenne"),
              dict(mesure="ecart type attendu si toutes les personnes etaient identiques",
                   valeur=round(float(np.sqrt(var_binom)), 4),
                   detail="modele binomial homogene au meme taux global"),
              dict(mesure="part de la variance inter personnes non imputable au tirage",
                   valeur=round(var_vraie / var_obs, 4) if var_obs else "",
                   detail="1 moins variance binomiale sur variance observee"),
              dict(mesure="ecart type inter items du taux de changement",
                   valeur=round(float(p_j.std(ddof=1)), 4),
                   detail=f"{len(p_j)} items, min {p_j.min():.3f}, max {p_j.max():.3f}"),
              dict(mesure="correlation taux de changement de l'item / entropie de l'item",
                   valeur=round(float(p_j.corr(ent)), 4),
                   detail="plus un item divise, plus il est instable"),
              dict(mesure="correlation taux de changement / nombre de modalites",
                   valeur=round(float(p_j.corr(n_mod)), 4), detail="")]

    # -- 3. Vers quoi : la reponse hors mode est-elle moins stable ? ------------
    mode_item = w13[cols].mode(dropna=True).iloc[0]
    au_mode = a.eq(mode_item, axis=1) & dispo
    p_change_mode = float((change & au_mode).sum().sum() / au_mode.sum().sum())
    p_change_hors = float((change & ~au_mode & dispo).sum().sum()
                          / (dispo & ~au_mode).sum().sum())
    # Parmi les changements, la nouvelle reponse est-elle le mode de l'item ?
    vers_mode = (change & b.eq(mode_item, axis=1)).sum().sum() / change.sum().sum()
    # Reference : proportion attendue si la nouvelle reponse etait tiree dans la
    # marginale de l'item, en excluant la reponse anterieure.
    attendu = []
    for c in cols:
        marg = w13[c].value_counts(normalize=True)
        m = mode_item[c]
        sel = change[c] & dispo[c]
        if sel.sum() == 0 or m not in marg.index:
            continue
        anc = a.loc[sel, c]
        pm = np.where(anc == m, 0.0, marg[m] / (1 - anc.map(marg).fillna(0)))
        attendu.append(pd.Series(pm, index=anc.index))
    attendu_mode = float(pd.concat(attendu).mean()) if attendu else np.nan

    lignes += [dict(mesure="probabilite de changer quand la reponse initiale est le mode",
                    valeur=round(p_change_mode, 4), detail=""),
               dict(mesure="probabilite de changer quand la reponse initiale n'est pas le mode",
                    valeur=round(p_change_hors, 4),
                    detail="l'ecart mesure le confondu entre deviance et instabilite"),
               dict(mesure="part des changements qui aboutissent au mode de l'item",
                    valeur=round(float(vers_mode), 4), detail=""),
               dict(mesure="part attendue sous tirage dans la marginale",
                    valeur=round(attendu_mode, 4),
                    detail="regression vers le mode si l'observe depasse l'attendu")]
    pd.DataFrame(lignes).to_csv(RES / "a9-instabilite-resume.csv", index=False)

    # -- 4. De combien de crans : observe contre trois modeles de bruit ---------
    ordinaux = [c for c in ORDINAUX if c in cols]
    rng = np.random.default_rng(GRAINE)
    obs, m_unif, m_marg, m_adj = [], [], [], []
    for c in ordinaux:
        sel = change[c] & dispo[c]
        if sel.sum() < 30:
            continue
        anc = a.loc[sel, c].to_numpy(dtype=float)
        nouv = b.loc[sel, c].to_numpy(dtype=float)
        obs.append(np.abs(nouv - anc))
        mods = np.sort(w13[c].dropna().unique().astype(float))
        marg = w13[c].value_counts(normalize=True)
        for x in anc:
            autres = mods[mods != x]
            if len(autres) == 0:
                continue
            m_unif.append(abs(rng.choice(autres) - x))
            pw = np.array([marg.get(v, 0.0) for v in autres], dtype=float)
            pw = pw / pw.sum() if pw.sum() > 0 else np.ones(len(autres)) / len(autres)
            m_marg.append(abs(rng.choice(autres, p=pw) - x))
            adj = autres[np.abs(autres - x) == np.abs(autres - x).min()]
            m_adj.append(abs(rng.choice(adj) - x))
    obs = np.concatenate(obs)

    def distrib(v, kmax=6):
        v = np.asarray(v, dtype=float)
        return pd.Series({k: float((v == k).mean()) for k in range(1, kmax + 1)})

    d = pd.DataFrame({"observe": distrib(obs), "bruit_uniforme": distrib(m_unif),
                      "bruit_marginal": distrib(m_marg), "bruit_adjacent": distrib(m_adj)})
    d.index.name = "ampleur_du_changement_en_crans"
    d = d.round(4)
    for m in ("bruit_uniforme", "bruit_marginal", "bruit_adjacent"):
        d.loc["distance_totale_a_l_observe", m] = round(
            float(0.5 * (d[m][:6] - d["observe"][:6]).abs().sum()), 4)
    d.loc["distance_totale_a_l_observe", "observe"] = 0.0
    d.loc["ampleur_moyenne", :] = [round(float(np.mean(x)), 4)
                                   for x in (obs, m_unif, m_marg, m_adj)]
    d.to_csv(RES / "a9-instabilite-ampleur.csv")

    # -- 5. Taux de changement item par item, pour le correctif ----------------
    tab = pd.DataFrame({"item": p_j.index,
                        "domaine": [items.at[c, "domaine"] for c in p_j.index],
                        "n_paires": dispo.sum()[p_j.index].to_numpy(),
                        "taux_changement": p_j.round(4).to_numpy(),
                        "n_modalites": n_mod[p_j.index].to_numpy(),
                        "entropie_bits": ent[p_j.index].round(4).to_numpy()})
    tab.sort_values("taux_changement", ascending=False).to_csv(
        RES / "a9-instabilite-par-item.csv", index=False)

    par_dom = tab.groupby("domaine").agg(
        n_items=("item", "size"), taux_moyen=("taux_changement", "mean"),
        taux_min=("taux_changement", "min"), taux_max=("taux_changement", "max"),
        entropie_moyenne=("entropie_bits", "mean")).round(4)
    par_dom.to_csv(RES / "a9-instabilite-par-domaine.csv")
    print(par_dom)
    print("[ok] tableaux ecrits dans resultats/")


def _entropie(serie):
    v = serie.dropna()
    if len(v) == 0:
        return np.nan
    p = v.value_counts(normalize=True).to_numpy()
    return float(-(p * np.log2(p)).sum())


if __name__ == "__main__":
    main()
