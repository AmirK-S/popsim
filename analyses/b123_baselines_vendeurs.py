"""
b123_baselines_vendeurs : ce que les baselines gratuites obtiennent sur les metriques
vitrines des vendeurs de repondants synthetiques.

Statut : script d'analyse jetable. Aucun appel de modele de langage, aucun LLM local.
Lecture seule sur data/. Preenregistrement : resultats/b123-preenregistrement.md, ecrit
avant ce fichier et avant tout calcul.

CE QUI EST REUTILISE : analyses/a6_double_distorsion_hors_gss.charger_twin et
.lire_formatte pour la liste des 108 items categoriels de Twin-2K-500 et la lecture
brute (non codee) des deux tables humaines. Rien d'autre n'est importe : la lecture des
panels GSS (pyreadstat) et les quatre metriques sont ecrites ici, neuves.

Entrees : data/gss-panel/GSS_panel08w123_R6 - stata.dta, GSS_panel2010w123_R6 - stata.dta
          data/twin2k500/llm_specs/humains_wave1_3.csv, humains_wave4.csv
Sorties : resultats/b123-gss.csv, resultats/b123-twin.csv, resultats/b123-resume.csv

Usage : .venv/bin/python analyses/b123_baselines_vendeurs.py
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
import pyreadstat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a6_double_distorsion_hors_gss as A6  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANEL = os.path.join(RACINE, "data", "gss-panel")
RACINE_TWIN = os.path.join(RACINE, "data", "twin2k500")
SORTIE = os.path.join(RACINE, "resultats")

FICHIER_08 = "GSS_panel08w123_R6 - stata.dta"
FICHIER_10 = "GSS_panel2010w123_R6 - stata.dta"
N_MIN_COHORTE = 200
K_MIN, K_MAX = 2, 7
GRAINE = 20260911

# Chiffres-vitrines des vendeurs, cites dans resultats/idees-B-industrie-2026-09-11.md
# section 1. Cle : (metrique, jeu vise par le vendeur, valeur, source).
VITRINES = [
    ("1-MAE", "Electric Twin", 0.955,
     "electrictwin.com/blog/how-accurate-are-synthetic-audiences"),
    ("1-MAE (94-95%)", "Kantar", 0.945, "kantar.com, boosting synthetique"),
    ("Recouvrement 1-TV", "Artificial Societies", 0.86, "societies.ai/how-accurate-are-ai-personas"),
    ("Similarite KS", "PyMC Labs/SSR (Colgate)", 0.85, "arXiv 2510.08338"),
    ("Spearman median", "Aaru (EY Global Wealth)", 0.90, "aaru.com/case-studies/ey-wealth-research"),
]


# ---------------------------------------------------------------------------
# 1. Les quatre metriques, sur des vecteurs de proportions alignes sur K options
# ---------------------------------------------------------------------------

def un_moins_mae(p, q):
    return float(1.0 - np.mean(np.abs(p - q)))


def un_moins_tv(p, q):
    return float(1.0 - 0.5 * np.sum(np.abs(p - q)))


def un_moins_ks(p, q):
    """1 - distance de Kolmogorov-Smirnov entre CDF sur options ORDONNEES."""
    return float(1.0 - np.max(np.abs(np.cumsum(p) - np.cumsum(q))))


def spearman(p, q):
    k = len(p)
    if k < 2 or np.allclose(p, p[0]) or np.allclose(q, q[0]):
        return float("nan")
    rp = pd.Series(p).rank().to_numpy()
    rq = pd.Series(q).rank().to_numpy()
    if np.std(rp) == 0 or np.std(rq) == 0:
        return float("nan")
    return float(np.corrcoef(rp, rq)[0, 1])


def metriques_item(p, q, ordinal):
    """p = predit, q = verite, tous deux des vecteurs de proportions sur K options."""
    out = {"1-MAE": un_moins_mae(p, q), "1-TV": un_moins_tv(p, q),
           "spearman": spearman(p, q)}
    out["KS"] = un_moins_ks(p, q) if ordinal else float("nan")
    return out


# ---------------------------------------------------------------------------
# 2. GSS : deux cohortes distinctes, panels NORC 2008 et 2010, vague 1
# ---------------------------------------------------------------------------

def charger_cohortes_gss():
    _, m8 = pyreadstat.read_dta(os.path.join(PANEL, FICHIER_08),
                                metadataonly=True, encoding="latin1")
    _, m10 = pyreadstat.read_dta(os.path.join(PANEL, FICHIER_10),
                                 metadataonly=True, encoding="latin1")
    c8 = {c.lower(): c for c in m8.column_names if c.lower().endswith("_1")}
    c10 = {c.lower(): c for c in m10.column_names if c.lower().endswith("_1")}
    base8 = {c[:-2] for c in c8}
    base10 = {c[:-2] for c in c10}
    communs = sorted(base8 & base10)

    d8, _ = pyreadstat.read_dta(
        os.path.join(PANEL, FICHIER_08), usecols=[c8[b + "_1"] for b in communs],
        encoding="latin1", apply_value_formats=True, formats_as_category=False)
    d10, _ = pyreadstat.read_dta(
        os.path.join(PANEL, FICHIER_10), usecols=[c10[b + "_1"] for b in communs],
        encoding="latin1", apply_value_formats=True, formats_as_category=False)
    d8.columns = [c.lower()[:-2] for c in d8.columns]
    d10.columns = [c.lower()[:-2] for c in d10.columns]

    # sexe, pour la baseline B2 ; formats appliques comme les items.
    sx8, _ = pyreadstat.read_dta(os.path.join(PANEL, FICHIER_08), usecols=[c8["sex_1"]],
                                 encoding="latin1", apply_value_formats=True)
    sx10, _ = pyreadstat.read_dta(os.path.join(PANEL, FICHIER_10), usecols=[c10["sex_1"]],
                                  encoding="latin1", apply_value_formats=True)
    d8["_sexe"] = sx8.iloc[:, 0].astype(str)
    d10["_sexe"] = sx10.iloc[:, 0].astype(str)
    return d8, d10, communs


def item_retenu(s8, s10):
    v8 = s8.dropna().astype(str)
    v10 = s10.dropna().astype(str)
    v8, v10 = v8[v8 != "nan"], v10[v10 != "nan"]
    if len(v8) < N_MIN_COHORTE or len(v10) < N_MIN_COHORTE:
        return None
    k = len(set(v8.unique()) | set(v10.unique()))
    if not (K_MIN <= k <= K_MAX):
        return None
    return v8, v10


def proportions(vals, modalites):
    c = vals.value_counts()
    n = len(vals)
    return np.array([c.get(m, 0) / n for m in modalites], dtype=float)


def baselines_gss(rng):
    d8, d10, communs = charger_cohortes_gss()
    lignes = []
    items_ok = []
    for b in communs:
        r = item_retenu(d8[b], d10[b])
        if r is None:
            continue
        v8, v10 = r
        try:
            modalites = sorted(set(v8.unique()) | set(v10.unique()), key=float)
        except ValueError:
            modalites = sorted(set(v8.unique()) | set(v10.unique()))
        p_uniforme = np.full(len(modalites), 1.0 / len(modalites))
        p_autre = proportions(d8[b].dropna().astype(str), modalites)   # B1 : cohorte 2008
        p_verite = proportions(d10[b].dropna().astype(str), modalites)  # cible : cohorte 2010

        # B2 : marge par sexe de la cohorte 2008, reponderee par la composition par sexe
        # de la cohorte 2010 (poids observes, pas d'hypothese sur leur stabilite).
        poids10 = d10["_sexe"].value_counts(normalize=True)
        p_sous = np.zeros(len(modalites))
        for sx, w in poids10.items():
            sous8 = d8.loc[d8["_sexe"] == sx, b].dropna().astype(str)
            if len(sous8) >= 30:
                p_sous += w * proportions(sous8, modalites)
            else:
                p_sous += w * p_autre
        items_ok.append((b, modalites, p_autre, p_verite))
        for nom, p in [("B0 uniforme", p_uniforme), ("B1 autre cohorte", p_autre),
                       ("B2 sous-echantillon (sexe)", p_sous)]:
            m = metriques_item(p, p_verite, ordinal=False)
            lignes.append({"jeu": "GSS", "item": b, "k": len(modalites),
                           "baseline": nom, **m})

    # Sensibilite : item permute (meme k) et camp inverse, appliques a B1.
    par_k = {}
    for b, mods, p_autre, p_verite in items_ok:
        par_k.setdefault(len(mods), []).append((b, p_autre, p_verite))
    for k, grp in par_k.items():
        if len(grp) < 2:
            continue
        idx = rng.permutation(len(grp))
        decale = np.roll(idx, 1)
        for i, (b, p_autre, p_verite) in enumerate(grp):
            b_autre, p_autre_permute, _ = grp[decale[i]]
            if b_autre == b:
                continue
            m = metriques_item(p_autre_permute, p_verite, ordinal=False)
            lignes.append({"jeu": "GSS", "item": b, "k": k,
                           "baseline": "BAD item permute", **m})
            m2 = metriques_item(p_autre[::-1], p_verite, ordinal=False)
            lignes.append({"jeu": "GSS", "item": b, "k": k,
                           "baseline": "BAD camp inverse", **m2})
    print(f"GSS : {len(items_ok)} items retenus (k in [{K_MIN},{K_MAX}], "
          f"N >= {N_MIN_COHORTE} par cohorte)")
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 3. Twin-2K-500 : humains vagues 1-3 (persistance) contre verite vague 4
# ---------------------------------------------------------------------------

def baselines_twin(rng):
    jeux, alertes = A6.charger_twin(RACINE_TWIN)
    if not jeux:
        print("Twin indisponible :", alertes)
        return pd.DataFrame()
    base = jeux[0]
    colonnes, est_ordinal = base["items"], base["est_ordinal"]
    dossier = os.path.join(RACINE_TWIN, "llm_specs")
    tab_v4 = A6.lire_formatte(os.path.join(dossier, "humains_wave4.csv"), colonnes)
    tab_v13 = A6.lire_formatte(os.path.join(dossier, "humains_wave1_3.csv"), colonnes)
    ids = sorted(set(tab_v4) & set(tab_v13))

    lignes = []
    items_ok = []
    for j, item in enumerate(colonnes):
        v4 = [tab_v4[i][j] for i in ids if tab_v4[i][j] != ""]
        v13 = [tab_v13[i][j] for i in ids if tab_v13[i][j] != ""]
        if len(v4) < N_MIN_COHORTE or len(v13) < N_MIN_COHORTE:
            continue
        modalites = sorted(set(v4) | set(v13))
        k = len(modalites)
        if not (K_MIN <= k <= K_MAX):
            continue
        p_uniforme = np.full(k, 1.0 / k)
        p_persist = proportions(pd.Series(v13), modalites)
        p_verite = proportions(pd.Series(v4), modalites)
        items_ok.append((item, modalites, p_persist, p_verite, bool(est_ordinal[j])))
        for nom, p in [("B0 uniforme", p_uniforme), ("B1 persistance", p_persist)]:
            m = metriques_item(p, p_verite, ordinal=est_ordinal[j])
            lignes.append({"jeu": "Twin-2K-500", "item": item, "k": k,
                           "baseline": nom, **m})

    par_k = {}
    for item, mods, p_persist, p_verite, ordi in items_ok:
        par_k.setdefault(len(mods), []).append((item, p_persist, p_verite, ordi))
    for k, grp in par_k.items():
        if len(grp) < 2:
            continue
        idx = rng.permutation(len(grp))
        decale = np.roll(idx, 1)
        for i, (item, p_persist, p_verite, ordi) in enumerate(grp):
            item_autre, p_permute, _, _ = grp[decale[i]]
            if item_autre == item:
                continue
            m = metriques_item(p_permute, p_verite, ordinal=ordi)
            lignes.append({"jeu": "Twin-2K-500", "item": item, "k": k,
                           "baseline": "BAD item permute", **m})
            m2 = metriques_item(p_persist[::-1], p_verite, ordinal=ordi)
            lignes.append({"jeu": "Twin-2K-500", "item": item, "k": k,
                           "baseline": "BAD camp inverse", **m2})
    print(f"Twin-2K-500 : {len(items_ok)} items retenus sur {len(colonnes)}")
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 4. Resume et sortie
# ---------------------------------------------------------------------------

def resumer(df):
    lignes = []
    for (jeu, baseline), g in df.groupby(["jeu", "baseline"], sort=False):
        lignes.append({
            "jeu": jeu, "baseline": baseline, "n_items": g["item"].nunique(),
            "1-MAE_mediane": g["1-MAE"].median(), "1-TV_mediane": g["1-TV"].median(),
            "KS_mediane": g["KS"].median(), "spearman_median": g["spearman"].median(),
            "spearman_ge90_pct_k3plus": float(
                (g.loc[g["k"] >= 3, "spearman"] >= 0.9).mean() * 100)
            if (g["k"] >= 3).any() else float("nan"),
        })
    return pd.DataFrame(lignes)


def main():
    os.makedirs(SORTIE, exist_ok=True)
    rng = np.random.default_rng(GRAINE)

    gss = baselines_gss(rng)
    twin = baselines_twin(rng)
    gss.to_csv(os.path.join(SORTIE, "b123-gss.csv"), index=False)
    twin.to_csv(os.path.join(SORTIE, "b123-twin.csv"), index=False)

    tout = pd.concat([gss, twin], ignore_index=True)
    resume = resumer(tout)
    resume.to_csv(os.path.join(SORTIE, "b123-resume.csv"), index=False)
    pd.set_option("display.width", 160)
    print("\n", resume.round(4).to_string(index=False))

    print("\nchiffres-vitrines vises :")
    for m, vendeur, val, src in VITRINES:
        print(f"  {m:<22}{vendeur:<28}{val:.3f}  ({src})")


if __name__ == "__main__":
    main()
