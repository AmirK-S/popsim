"""
c1_dispersion : question 2 du mois 1 du programme C version menages.

Par mois, la dispersion inter menages de chaque anticipation, decomposee en inter cohortes
et intra cohorte, en variance corrigee du biais d'echantillonnage fini et en mesures
robustes ; sa trajectoire de 2020 a 2025 ; et le choc de 2025, defini depuis les donnees par
la regle preenregistree.

Sorties : c1-dispersion-mensuelle.csv, c1-choc-2025.csv, c1-avant-apres-choc.csv,
c1-dispersion-ordinales.csv, c1-dispersion-cohortes-alternatives.csv. Aucune microdonnee.
"""

import numpy as np
import pandas as pd

import c1_commun as C1


def mensuelle(df, bornes, variables, colonne_cohorte="cohorte_code", etiquette="age x edu x rev"):
    """Une ligne par mois et par variable."""
    lignes = []
    for t, d in df.groupby("t"):
        g = d[colonne_cohorte].to_numpy()
        for v in variables:
            x_brut = pd.to_numeric(d[v], errors="coerce").to_numpy(dtype=float)
            x_w = C1.winsoriser(x_brut, bornes[v])
            dec = C1.decomposition(x_w, g)
            rob = C1.robustes(x_brut, g)
            ok = np.isfinite(x_brut)
            lignes.append({
                "t": int(t), "mois": C1.nom_mois(int(t)), "variable": v,
                "cohorte": etiquette,
                "n": int(ok.sum()),
                "n_cohortes": dec["n_cohortes"],
                "moyenne": float(np.mean(x_w[np.isfinite(x_w)])) if ok.any() else np.nan,
                "mediane": float(np.median(x_brut[ok])) if ok.any() else np.nan,
                "variance_totale": dec["intra"] + dec["inter"],
                "variance_intra": dec["intra"],
                "variance_inter": dec["inter"],
                "variance_inter_brute": dec["inter_brut"],
                "part_inter": dec["part_inter"],
                "ecart_type": np.sqrt(max(dec["intra"] + dec["inter"], 0.0)),
                **rob,
            })
    return pd.DataFrame(lignes)


def choc(mens, variable_reference="infl1"):
    """Regle primaire et regle secondaire du preenregistrement section 4.2.

    Primaire : le mois de janvier a octobre 2025 qui maximise |moyenne(t) - moyenne(t-1)|
    de la variable de reference. Secondaire : le mois qui maximise le saut de l'ecart
    interquartile. Les deux sont publies, la primaire seule est utilisee.
    """
    d = mens[mens["variable"] == variable_reference].sort_values("t").reset_index(drop=True)
    d["saut_moyenne"] = d["moyenne"].diff()
    d["saut_iqr"] = d["iqr_total"].diff()
    fenetre = d[(d["t"] >= (2025 - 2013) * 12) & (d["t"] <= (2025 - 2013) * 12 + 9)]
    i_moy = fenetre["saut_moyenne"].abs().idxmax()
    i_iqr = fenetre["saut_iqr"].abs().idxmax()
    lignes = []
    for cle, i in (("primaire, saut de moyenne", i_moy), ("secondaire, saut d'IQR", i_iqr)):
        lignes.append({"regle": cle, "variable": variable_reference,
                       "t": int(d.loc[i, "t"]), "mois": d.loc[i, "mois"],
                       "moyenne": d.loc[i, "moyenne"],
                       "saut_moyenne": d.loc[i, "saut_moyenne"],
                       "iqr": d.loc[i, "iqr_total"],
                       "saut_iqr": d.loc[i, "saut_iqr"]})
    # la fenetre entiere est publiee, pour que le choix de la regle soit verifiable
    for _, r in fenetre.iterrows():
        lignes.append({"regle": "fenetre 2025, pour verification", "variable": variable_reference,
                       "t": int(r["t"]), "mois": r["mois"], "moyenne": r["moyenne"],
                       "saut_moyenne": r["saut_moyenne"], "iqr": r["iqr_total"],
                       "saut_iqr": r["saut_iqr"]})
    return pd.DataFrame(lignes), int(d.loc[i_moy, "t"])


def avant_apres(df, mens, t_choc, bornes, variables):
    """Les trois mois avant et les trois mois a partir du choc, declares section 4.2."""
    avant = list(range(t_choc - 3, t_choc))
    apres = list(range(t_choc, t_choc + 3))
    lignes = []
    for v in variables:
        for cle, fen in (("avant", avant), ("apres", apres)):
            d = df[df["t"].isin(fen)]
            x_brut = pd.to_numeric(d[v], errors="coerce").to_numpy(dtype=float)
            x_w = C1.winsoriser(x_brut, bornes[v])
            g = d["cohorte_code"].to_numpy()
            dec = C1.decomposition(x_w, g)
            rob = C1.robustes(x_brut, g)
            lignes.append({"variable": v, "fenetre": cle,
                           "mois": " ".join(C1.nom_mois(t) for t in fen),
                           "n": dec["n"], "n_menages": int(d["userid"].nunique()),
                           "moyenne": float(np.nanmean(x_w)),
                           "mediane": float(np.nanmedian(x_brut)),
                           "variance_totale": dec["intra"] + dec["inter"],
                           "variance_intra": dec["intra"],
                           "variance_inter": dec["inter"],
                           "part_inter": dec["part_inter"], **rob})
    t = pd.DataFrame(lignes)
    piv = t.pivot(index="variable", columns="fenetre")
    out = []
    for v in variables:
        a, b = piv.loc[v, (slice(None), "avant")], piv.loc[v, (slice(None), "apres")]
        a.index, b.index = a.index.get_level_values(0), b.index.get_level_values(0)
        out.append({
            "variable": v,
            "n_avant": a["n"], "n_apres": b["n"],
            "moyenne_avant": a["moyenne"], "moyenne_apres": b["moyenne"],
            "delta_moyenne": b["moyenne"] - a["moyenne"],
            "iqr_avant": a["iqr_total"], "iqr_apres": b["iqr_total"],
            "ratio_iqr": b["iqr_total"] / a["iqr_total"] if a["iqr_total"] else np.nan,
            "variance_avant": a["variance_totale"], "variance_apres": b["variance_totale"],
            "ratio_variance": b["variance_totale"] / a["variance_totale"]
            if a["variance_totale"] else np.nan,
            "part_inter_avant": a["part_inter"], "part_inter_apres": b["part_inter"],
            "delta_part_inter": b["part_inter"] - a["part_inter"],
            "iqr_intra_avant": a["iqr_intra_median"], "iqr_intra_apres": b["iqr_intra_median"],
            "ratio_iqr_intra": b["iqr_intra_median"] / a["iqr_intra_median"]
            if a["iqr_intra_median"] else np.nan,
        })
    return t, pd.DataFrame(out)


def ordinales(df):
    """Les deux variables ordinales par le Gini-Simpson a biais corrige de a44.

    Aucune variance n'est calculee sur une echelle a cinq modalites : c'est la dispersion
    categorielle de a1, a35 et a44 qui est utilisee, sans une ligne reimplementee.
    """
    lignes = []
    for t, d in df.groupby("t"):
        codes = np.stack([pd.to_numeric(d[v], errors="coerce").fillna(0).astype(int).to_numpy() - 1
                          for v in C1.VAR_ORDINALES], axis=1).astype(np.int32)
        codes[codes < 0] = -1
        seg = d["cohorte_code"].to_numpy().astype(np.int32)
        colonnes = np.arange(codes.shape[1])
        res = C1.C44.dispersion(codes, seg, 5, colonnes)
        tot = res["inter"] + res["intra"]
        lignes.append({"t": int(t), "mois": C1.nom_mois(int(t)),
                       "variables": " et ".join(C1.VAR_ORDINALES),
                       "n": int(len(d)), "n_items": res["n_items"],
                       "gini_inter": res["inter"], "gini_intra": res["intra"],
                       "part_inter": res["inter"] / tot if tot else np.nan})
    return pd.DataFrame(lignes)


def cohortes_alternatives(df, bornes):
    """Sensibilite : les trois segmentations secondaires declarees section 3."""
    out = []
    variantes = {
        "age seul": ("_AGE_CAT",),
        "edu x revenu": ("_EDU_CAT", "_HH_INC_CAT"),
        "region": ("_REGION_CAT",),
    }
    for nom, cols in variantes.items():
        d = df.copy()
        d["_alt"] = pd.factorize(C1.cohorte(d, cols))[0].astype(np.int32)
        m = mensuelle(d, bornes, C1.VAR_PRIMAIRES, colonne_cohorte="_alt", etiquette=nom)
        out.append(m.groupby("variable").agg(
            part_inter_mediane=("part_inter", "median"),
            part_inter_min=("part_inter", "min"),
            part_inter_max=("part_inter", "max"),
            n_cohortes_median=("n_cohortes", "median")).assign(cohorte=nom).reset_index())
    m0 = mensuelle(df, bornes, C1.VAR_PRIMAIRES)
    out.append(m0.groupby("variable").agg(
        part_inter_mediane=("part_inter", "median"),
        part_inter_min=("part_inter", "min"),
        part_inter_max=("part_inter", "max"),
        n_cohortes_median=("n_cohortes", "median")).assign(
            cohorte="age x edu x rev (primaire)").reset_index())
    return pd.concat(out, ignore_index=True)


def main():
    df = C1.charger(C1.PRIMAIRE)
    df17 = C1.charger(["2017-2019"])
    variables = C1.VAR_PRIMAIRES + ["infl1_var", "infl1_point"]
    bornes = C1.bornes_winsor(df, variables)

    mens = mensuelle(df, bornes, variables)
    # 2017-2019 en descriptif seulement, memes bornes de winsorisation
    mens17 = mensuelle(df17, bornes, variables)
    mens17["perimetre"] = "descriptif 2017-2019"
    mens["perimetre"] = "primaire 2020-2025"
    C1.ecrire(pd.concat([mens17, mens], ignore_index=True), "c1-dispersion-mensuelle.csv")

    tab_choc, t_choc = choc(mens)
    C1.ecrire(tab_choc, "c1-choc-2025.csv")
    t_sec = int(tab_choc[tab_choc["regle"].str.startswith("secondaire")]["t"].iloc[0])
    print(f"choc primaire : {C1.nom_mois(t_choc)}, secondaire : {C1.nom_mois(t_sec)}")

    # Les deux regles designent deux mois differents. La primaire porte le verdict comme
    # declare ; la secondaire est publiee entierement a cote, jamais substituee.
    details, resumes = [], []
    for cle, t in (("primaire, saut de moyenne", t_choc), ("secondaire, saut d'IQR", t_sec)):
        d, r = avant_apres(df, mens, t, bornes, variables)
        d["regle"], r["regle"] = cle, cle
        d["mois_choc"], r["mois_choc"] = C1.nom_mois(t), C1.nom_mois(t)
        details.append(d)
        resumes.append(r)
    C1.ecrire(pd.concat(details, ignore_index=True), "c1-avant-apres-choc-detail.csv")
    C1.ecrire(pd.concat(resumes, ignore_index=True), "c1-avant-apres-choc.csv")

    C1.ecrire(ordinales(df), "c1-dispersion-ordinales.csv")
    C1.ecrire(cohortes_alternatives(df, bornes), "c1-dispersion-cohortes-alternatives.csv")
    print("c1_dispersion termine")


if __name__ == "__main__":
    main()
