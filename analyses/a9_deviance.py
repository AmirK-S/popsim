"""
a9_deviance : A10, le trait de deviance existe-t-il sur Twin-2K-500 ?

Hypothese testee : il existe une propension individuelle a devier du mode de son
groupe demographique, stable d'un domaine a l'autre.

Aucun appel de modele de langage. Les sorties LLM lues sont celles deja calculees et
publiees par les auteurs de Twin-2K-500. Aucune microdonnee n'est ecrite : seuls des
tableaux agreges partent dans resultats/.

Usage : .venv/bin/python analyses/a9_deviance.py
"""

import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a9_commun as A  # noqa: E402

GRAINE = 20260907
RES = A.RACINE / "resultats"
DOMAINES = [d for d in A.ORDRE_DOMAINES]


# ---------------------------------------------------------------------------
# Outils statistiques
# ---------------------------------------------------------------------------

def cor(x, y, methode="pearson"):
    s = pd.concat([pd.Series(x), pd.Series(y)], axis=1).dropna()
    if len(s) < 30:
        return np.nan, len(s)
    return float(s.iloc[:, 0].corr(s.iloc[:, 1], method=methode)), len(s)


def cor_partielle(x, y, controles):
    """Correlation de Pearson entre x et y, une fois les controles retires des deux."""
    d = pd.concat([pd.Series(x).rename("x"), pd.Series(y).rename("y"), controles], axis=1).dropna()
    if len(d) < 50:
        return np.nan, len(d)
    C = np.column_stack([np.ones(len(d)), d[controles.columns].to_numpy(dtype=float)])
    res = {}
    for v in ("x", "y"):
        z = d[v].to_numpy(dtype=float)
        beta, *_ = np.linalg.lstsq(C, z, rcond=None)
        res[v] = z - C @ beta
    return float(np.corrcoef(res["x"], res["y"])[0, 1]), len(d)


def ic_bootstrap_cor(x, y, n=2000, graine=GRAINE, methode="pearson"):
    s = pd.concat([pd.Series(x), pd.Series(y)], axis=1).dropna()
    if len(s) < 30:
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(graine)
    a = s.iloc[:, 0].to_numpy()
    b = s.iloc[:, 1].to_numpy()
    tir = []
    for _ in range(n):
        i = rng.integers(0, len(a), len(a))
        sa, sb = pd.Series(a[i]), pd.Series(b[i])
        tir.append(sa.corr(sb, method=methode))
    tir = np.array(tir, dtype=float)
    return (float(pd.Series(a).corr(pd.Series(b), method=methode)),
            float(np.nanpercentile(tir, 2.5)), float(np.nanpercentile(tir, 97.5)))


def split_half(dev, cols, n_splits=50, graine=GRAINE, n_min=3):
    """Fiabilite de la deviance individuelle sur un ensemble d'items, par moities.

    Retourne la correction de Spearman-Brown moyenne sur n_splits partages aleatoires.
    """
    rng = np.random.default_rng(graine)
    cols = list(cols)
    if len(cols) < 6:
        return np.nan
    rs = []
    for _ in range(n_splits):
        p = rng.permutation(len(cols))
        a = [cols[i] for i in p[: len(cols) // 2]]
        b = [cols[i] for i in p[len(cols) // 2:]]
        sa = dev[a].mean(axis=1).where(dev[a].notna().sum(axis=1) >= n_min)
        sb = dev[b].mean(axis=1).where(dev[b].notna().sum(axis=1) >= n_min)
        r, _ = cor(sa, sb)
        if not np.isnan(r):
            rs.append(2 * r / (1 + r))
    return float(np.mean(rs)) if rs else np.nan


def centrer_par_item(dev):
    """Retire a chaque item son taux de deviance moyen.

    Sans cela, un score individuel agrege depend du sous ensemble d'items que la
    personne a vu. C'est un vrai risque ici : les experiences d'economie
    comportementale sont en inter sujets, chaque personne ne voit qu'une condition,
    et deux personnes tirees dans des conditions de difficulte differente auraient
    une deviance differente sans aucune difference individuelle.
    """
    return dev - dev.mean(axis=0)


def score_centre(dev, cols, n_min=5):
    sub = centrer_par_item(dev[cols])
    return sub.mean(axis=1).where(sub.notna().sum(axis=1) >= n_min)


def part_premier_facteur(mat):
    """Part de variance expliquee par la premiere composante d'une matrice de correlation."""
    m = mat.dropna(how="all").dropna(axis=1, how="all")
    m = np.array(m.fillna(0.0).to_numpy(dtype=float), copy=True)
    np.fill_diagonal(m, 1.0)
    vp = np.linalg.eigvalsh(m)[::-1]
    return float(vp[0] / len(vp)), float(vp[0]), float(vp[1])


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------

def main():
    RES.mkdir(exist_ok=True)
    cat = A.charger_catalogue()
    items = A.table_items(cat)
    w13 = A.charger_humains("1_3", cat)
    w4 = A.charger_humains("4", cat)
    seg = A.construire_segments(w13)

    items_utiles = items[items["domaine"].isin(DOMAINES)]
    cols13 = [c for c in items_utiles.index if c in w13.columns]
    cols4 = [c for c in items_utiles.index if c in w4.columns]
    print(f"[info] {len(cols13)} items vagues 1-3, {len(cols4)} items vague 4, "
          f"{len(w13)} personnes")

    # -- 1. Deviance humaine, vagues 1 a 3, une segmentation apres l'autre ---------
    dev_par_seg = {}
    for nom in list(A.SEGMENTS) + ["population"]:
        dev_par_seg[nom] = A.deviance_items(w13[cols13], seg[nom], taille_min=15)
        print(f"[info] deviance calculee, segmentation {nom}")

    lignes = []
    for nom, dev in dev_par_seg.items():
        dom = A.agreger_par_domaine(dev, items_utiles)
        for d in dom.columns:
            s = dom[d].dropna()
            lignes.append(dict(segmentation=nom, domaine=d, n_personnes=len(s),
                               n_items=int((items_utiles["domaine"] == d).sum()),
                               taux_deviance_moyen=round(float(s.mean()), 4),
                               ecart_type=round(float(s.std(ddof=1)), 4),
                               p10=round(float(s.quantile(.10)), 4),
                               p90=round(float(s.quantile(.90)), 4)))
    pd.DataFrame(lignes).to_csv(RES / "a9-deviance-niveaux.csv", index=False)

    # -- 2. Matrice domaine x domaine, fiabilite, facteur unique -------------------
    principal = "profil_croise"
    sorties_mat = []
    fiab_rows = []
    for nom in ["profil_croise", "ideologie", "population"]:
        dev = dev_par_seg[nom]
        dom = A.agreger_par_domaine(dev, items_utiles)
        fiab = {}
        for d in dom.columns:
            cols = [c for c in dev.columns if items_utiles.at[c, "domaine"] == d]
            fiab[d] = split_half(dev, cols)
            fiab_rows.append(dict(segmentation=nom, domaine=d, n_items=len(cols),
                                  fiabilite_split_half=round(fiab[d], 4)
                                  if not np.isnan(fiab[d]) else ""))
        mat = dom.corr(method="pearson", min_periods=100)
        matd = mat.copy()
        for a in mat.columns:
            for b in mat.columns:
                if a != b and not np.isnan(fiab.get(a, np.nan)) and not np.isnan(fiab.get(b, np.nan)):
                    den = np.sqrt(max(fiab[a], 1e-6) * max(fiab[b], 1e-6))
                    matd.loc[a, b] = mat.loc[a, b] / den
        dom_c = pd.DataFrame({d: score_centre(dev, [c for c in dev.columns
                                                    if items_utiles.at[c, "domaine"] == d])
                              for d in dom.columns})
        for a in mat.columns:
            for b in mat.columns:
                if a >= b:
                    continue
                r, n = cor(dom[a], dom[b])
                rs, _ = cor(dom[a], dom[b], "spearman")
                rc, _ = cor(dom_c[a], dom_c[b])
                sorties_mat.append(dict(segmentation=nom, domaine_a=a, domaine_b=b, n=n,
                                        r_pearson=round(r, 4), r_spearman=round(rs, 4),
                                        r_centre_item=round(rc, 4),
                                        r_desattenue=round(float(matd.loc[a, b]), 4)))
        if nom == principal:
            part, vp1, vp2 = part_premier_facteur(mat)
            part_d, vp1d, vp2d = part_premier_facteur(matd)
            facteur = pd.DataFrame([
                dict(matrice="brute", n_domaines=len(mat), part_premier_facteur=round(part, 4),
                     valeur_propre_1=round(vp1, 4), valeur_propre_2=round(vp2, 4),
                     r_moyen=round(float(mat.where(~np.eye(len(mat), dtype=bool)).stack().mean()), 4)),
                dict(matrice="desattenuee", n_domaines=len(matd), part_premier_facteur=round(part_d, 4),
                     valeur_propre_1=round(vp1d, 4), valeur_propre_2=round(vp2d, 4),
                     r_moyen=round(float(matd.where(~np.eye(len(matd), dtype=bool)).stack().mean()), 4)),
            ])
            dom_principal = dom

    pd.DataFrame(sorties_mat).to_csv(RES / "a9-deviance-correlations-domaines.csv", index=False)
    pd.DataFrame(fiab_rows).to_csv(RES / "a9-deviance-fiabilite.csv", index=False)

    # -- 3. Temoin de permutation : plancher de bruit ------------------------------
    rng = np.random.default_rng(GRAINE)
    dev = dev_par_seg[principal]
    perm_r = []
    for _ in range(20):
        d2 = dev.copy()
        for d in DOMAINES:
            cols = [c for c in dev.columns if items_utiles.at[c, "domaine"] == d]
            if not cols:
                continue
            idx = rng.permutation(len(d2))
            d2[cols] = dev[cols].to_numpy()[idx]
        dom2 = A.agreger_par_domaine(d2, items_utiles)
        m2 = dom2.corr(min_periods=100)
        perm_r.append(float(m2.where(~np.eye(len(m2), dtype=bool)).stack().mean()))
    facteur["r_moyen_permutation"] = round(float(np.mean(perm_r)), 4)
    facteur["r_permutation_p95"] = round(float(np.percentile(perm_r, 95)), 4)
    facteur.to_csv(RES / "a9-deviance-un-facteur.csv", index=False)

    # -- 4. Controles : consistance test retest, style de reponse ------------------
    communs = [c for c in cols4 if c in w13.columns]
    a13 = w13[communs]
    a4 = w4[communs]
    dispo = a13.notna() & a4.notna()
    identique = (a13 == a4) & dispo
    consistance = (identique.sum(axis=1) / dispo.sum(axis=1).replace(0, np.nan))

    # Style de reponse extreme et acquiescement, sur les matrices Likert a 5 modalites
    # ou plus des vagues 1 a 3, hors items reposes en vague 4.
    likert = [c for c in cols13 if items_utiles.at[c, "type"] == "matrice" and c not in communs]
    nmod = w13[likert].max()
    likert5 = [c for c in likert if nmod[c] >= 5]
    L = w13[likert5]
    maxi = L.max()
    extremes = ((L.eq(1)) | (L.eq(maxi, axis=1))).sum(axis=1) / L.notna().sum(axis=1)
    milieu = (L.eq((maxi + 1) / 2, axis=1)).sum(axis=1) / L.notna().sum(axis=1)
    acquiescement = (L.gt((maxi + 1) / 2, axis=1)).sum(axis=1) / L.notna().sum(axis=1)
    non_reponse = w13[cols13].isna().mean(axis=1)

    controles = pd.DataFrame({"consistance": consistance, "style_extreme": extremes,
                              "style_milieu": milieu, "acquiescement": acquiescement,
                              "non_reponse": non_reponse})

    lignes = []
    dev_moyenne = dom_principal.mean(axis=1)
    for nom_c in controles.columns:
        r, ic1, ic2 = ic_bootstrap_cor(dev_moyenne, controles[nom_c])
        lignes.append(dict(variable=nom_c, cible="deviance_moyenne_6_domaines",
                           r=round(r, 4), ic95_bas=round(ic1, 4), ic95_haut=round(ic2, 4)))
    for d in dom_principal.columns:
        for nom_c in ("consistance", "style_extreme"):
            r, n = cor(dom_principal[d], controles[nom_c])
            lignes.append(dict(variable=nom_c, cible=f"deviance_{d}", r=round(r, 4),
                               ic95_bas="", ic95_haut=""))
    pd.DataFrame(lignes).to_csv(RES / "a9-deviance-controles.csv", index=False)

    # Matrice inter domaines partialisee
    lignes = []
    jeux = {"aucun": None,
            "consistance": controles[["consistance"]],
            "consistance_style": controles[["consistance", "style_extreme", "style_milieu",
                                            "acquiescement", "non_reponse"]]}
    for nom_j, ctrl in jeux.items():
        for a in dom_principal.columns:
            for b in dom_principal.columns:
                if a >= b:
                    continue
                if ctrl is None:
                    r, n = cor(dom_principal[a], dom_principal[b])
                else:
                    r, n = cor_partielle(dom_principal[a], dom_principal[b], ctrl)
                lignes.append(dict(controle=nom_j, domaine_a=a, domaine_b=b, n=n,
                                   r=round(r, 4)))
    part_ctrl = pd.DataFrame(lignes)
    part_ctrl.to_csv(RES / "a9-deviance-correlations-partielles.csv", index=False)

    # -- 5. Stabilite test retest de la deviance ----------------------------------
    dev13_rep = A.deviance_items(w13[communs], seg[principal], taille_min=15)
    dev4_rep = A.deviance_items(w4[communs], seg[principal], taille_min=15)
    lignes = []
    for d in ["attitudes", "heuristiques_biais", "prix", "TOUS"]:
        cols = communs if d == "TOUS" else [c for c in communs if items_utiles.at[c, "domaine"] == d]
        if len(cols) < 5:
            continue
        s13 = dev13_rep[cols].mean(axis=1).where(dev13_rep[cols].notna().sum(axis=1) >= 5)
        s4 = dev4_rep[cols].mean(axis=1).where(dev4_rep[cols].notna().sum(axis=1) >= 5)
        r, ic1, ic2 = ic_bootstrap_cor(s13, s4)
        fiab = split_half(dev13_rep, cols)
        lignes.append(dict(domaine=d, n_items=len(cols),
                           taux_vagues1_3=round(float(s13.mean()), 4),
                           taux_vague4=round(float(s4.mean()), 4),
                           r_retest=round(r, 4), ic95_bas=round(ic1, 4), ic95_haut=round(ic2, 4),
                           fiabilite_interne=round(fiab, 4) if not np.isnan(fiab) else "",
                           r_retest_desattenue=round(r / fiab, 4)
                           if fiab and not np.isnan(fiab) and fiab > 0 else ""))
    pd.DataFrame(lignes).to_csv(RES / "a9-deviance-retest.csv", index=False)

    # -- 6. Deviance calculee sur les seuls items stables de la personne ----------
    # Neutralise le confondu mecanique : un repondant instable devie plus par construction.
    stable = identique.where(dispo)
    dev13_stable = dev13_rep.where(stable == 1)
    dev13_instable = dev13_rep.where(stable == 0)
    s_stable = dev13_stable.mean(axis=1).where(dev13_stable.notna().sum(axis=1) >= 10)
    s_instable = dev13_instable.mean(axis=1).where(dev13_instable.notna().sum(axis=1) >= 10)

    lignes = []
    for d in ["personnalite", "cognitif", "economique"]:
        cols = [c for c in dev.columns if items_utiles.at[c, "domaine"] == d]
        cible = dev[cols].mean(axis=1).where(dev[cols].notna().sum(axis=1) >= 5)
        r1, n1 = cor(s_stable, cible)
        r2, n2 = cor(s_instable, cible)
        r3, _ = cor_partielle(s_stable, cible, controles[["consistance"]])
        lignes.append(dict(domaine_cible=d,
                           r_avec_deviance_items_stables=round(r1, 4), n=n1,
                           r_avec_deviance_items_instables=round(r2, 4),
                           r_items_stables_partialise_consistance=round(r3, 4)))
    lignes.append(dict(domaine_cible="_moyennes",
                       r_avec_deviance_items_stables=round(float(s_stable.mean()), 4),
                       n=int(s_stable.notna().sum()),
                       r_avec_deviance_items_instables=round(float(s_instable.mean()), 4),
                       r_items_stables_partialise_consistance=""))
    pd.DataFrame(lignes).to_csv(RES / "a9-deviance-items-stables.csv", index=False)

    # -- 7. Les agents ont-ils un trait de deviance ? ------------------------------
    configs = A.configs_llm_disponibles()
    dom_h4 = A.agreger_par_domaine(dev4_rep, items_utiles)
    lignes, lignes_dom = [], []
    for nom, fichier in sorted(configs.items()):
        try:
            llm = A.charger_llm(fichier)
        except Exception as e:  # fichier absent ou format inattendu
            print(f"[avert] {nom} illisible : {e}")
            continue
        colsl = [c for c in cols4 if c in llm.columns]
        idx = llm.index.intersection(w4.index)
        llm = llm.loc[idx, colsl]
        segl = seg[principal].reindex(idx)
        dev_int = A.deviance_items(llm, segl, taille_min=15)          # mode des agents
        mode_h = {}
        dev_ext = pd.DataFrame(np.nan, index=llm.index, columns=colsl)
        # reference externe : mode humain du segment, meme regle de taille minimale
        dev_h_ref = A.deviance_items(w4.loc[:, colsl], seg[principal], taille_min=15)
        for c in colsl:
            tab = pd.crosstab(seg[principal], w4[c])
            if tab.empty:
                continue
            m = tab.idxmax(axis=1)
            grands = tab.sum(axis=1) >= 15
            ref = segl.map(m).where(segl.map(grands).fillna(False))
            mode_h[c] = ref
            dev_ext[c] = (llm[c] != ref).astype(float).where(llm[c].notna() & ref.notna())

        # Le mode des agents coincide-t-il avec le mode des humains, cellule par cellule ?
        acc, tot = 0, 0
        for c in colsl:
            th = pd.crosstab(seg[principal], w4[c])
            ta = pd.crosstab(segl, llm[c])
            if th.empty or ta.empty:
                continue
            grandes = [g for g in th.index if th.loc[g].sum() >= 15 and g in ta.index
                       and ta.loc[g].sum() >= 15]
            for g in grandes:
                tot += 1
                acc += int(th.loc[g].idxmax() == ta.loc[g].idxmax())
        accord_mode = acc / tot if tot else float("nan")

        for etiq, dv in (("interne", dev_int), ("externe", dev_ext)):
            dm = A.agreger_par_domaine(dv, items_utiles)
            glob = dm.mean(axis=1)
            glob_h = dom_h4.reindex(glob.index).mean(axis=1)
            r, ic1, ic2 = ic_bootstrap_cor(glob, glob_h, n=1000)
            rs, _ = cor(glob, glob_h, "spearman")
            # Version centree par item : neutralise la composition du sous ensemble
            # d'items vu par la personne, et son temoin par permutation des agents.
            gc = score_centre(dv, list(dv.columns), n_min=20)
            gch = score_centre(dev4_rep.reindex(dv.index), colsl, n_min=20)
            rc, nc = cor(gc, gch)
            rng_p = np.random.default_rng(GRAINE)
            perm = []
            for _ in range(200):
                perm.append(cor(pd.Series(rng_p.permutation(gc.to_numpy()), index=gc.index),
                                gch)[0])
            temoin = float(np.nanpercentile(np.abs(np.array(perm, dtype=float)), 95))
            fiab_a = split_half(dv, list(dv.columns))
            fiab_h = split_half(dev4_rep.reindex(glob.index), colsl)
            lignes.append(dict(configuration=nom, reference=etiq, n_personnes=len(idx),
                               taux_deviance_agent=round(float(glob.mean()), 4),
                               taux_deviance_humain=round(float(glob_h.mean()), 4),
                               r_agent_humain=round(r, 4), ic95_bas=round(ic1, 4),
                               ic95_haut=round(ic2, 4),
                               rho_spearman=round(rs, 4),
                               r_centre_item=round(rc, 4), n_centre=nc,
                               accord_mode_agent_humain=round(accord_mode, 4),
                               n_cellules_mode=tot,
                               temoin_permutation_p95=round(temoin, 4),
                               fiabilite_agent=round(fiab_a, 4) if not np.isnan(fiab_a) else "",
                               fiabilite_humain=round(fiab_h, 4) if not np.isnan(fiab_h) else "",
                               r_desattenue=round(r / np.sqrt(fiab_a * fiab_h), 4)
                               if fiab_a and fiab_h and fiab_a > 0 and fiab_h > 0 else ""))
            if etiq == "interne":
                for a in dm.columns:
                    for b in dm.columns:
                        if a >= b:
                            continue
                        rr, nn = cor(dm[a], dm[b])
                        lignes_dom.append(dict(configuration=nom, domaine_a=a, domaine_b=b,
                                               n=nn, r=round(rr, 4)))
        print(f"[info] configuration {nom} traitee")

    # meme matrice inter domaines pour les humains sur les memes items
    for a in dom_h4.columns:
        for b in dom_h4.columns:
            if a >= b:
                continue
            rr, nn = cor(dom_h4[a], dom_h4[b])
            lignes_dom.append(dict(configuration="HUMAINS_vague4", domaine_a=a, domaine_b=b,
                                   n=nn, r=round(rr, 4)))

    pd.DataFrame(lignes).to_csv(RES / "a9-deviance-llm.csv", index=False)
    pd.DataFrame(lignes_dom).to_csv(RES / "a9-deviance-llm-domaines.csv", index=False)
    print("[ok] tableaux ecrits dans resultats/")


if __name__ == "__main__":
    main()
