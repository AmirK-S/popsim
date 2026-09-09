"""
a12_retest_delai : la consistance test retest du GSS a deux ans et a quatre ans,
mesuree sur les panels de NORC, avec la definition de Stanford.

Statut : script d'exploration, pas du code de production. Aucun appel de modele.

Question. Stanford normalise ses scores de fidelite par la consistance test retest des
memes personnes a **deux semaines**, 79,53 pour cent. Les panels du GSS reinterrogent les
memes personnes a **deux ou quatre ans**. Un denominateur mesure a deux ans est
mecaniquement plus petit, donc plus flatteur pour le numerateur. Ce script mesure de
combien.

Definition employee, la meme des deux cotes : egalite exacte de la modalite entre les deux
passations, moyennee d'abord sur les items renseignes chez une personne, puis sur les
personnes. C'est la definition qui reproduit le 0,795253 du champ
`p_wave1__p_wave2__accuracy` de l'archive OSF.

Entrees :
  data/gss-panel/*.dta                    panels NORC, voir PROVENANCE.md
  data/osf-t6g7k-stanford/figure2/...     archive de replication Stanford

Sorties, toutes agregees, aucune microdonnee :
  resultats/a12-appariement-items.csv
  resultats/a12-retest-item.csv
  resultats/a12-retest-individu.csv
  resultats/a12-synthese-delais.csv
  resultats/a12-normalisation.csv
  resultats/a12-items-stables-instables.csv

Usage : .venv/bin/python analyses/a12_retest_delai.py
"""

import os
import sys
from collections import Counter

import numpy as np
import pandas as pd
import pyreadstat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a2_commun import est_manquant, exactitude_par_personne  # noqa: E402
from a2_baselines_gss import FAMILLES  # noqa: E402  familles thematiques, reprises telles quelles

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANEL = os.path.join(RACINE, "data", "gss-panel")
PREP = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                            "new_analysis_summaries/gss_filtered/preparation")
QMASTER = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                               "question_master/gss/main.csv")
INDIV = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                             "new_analysis_summaries/gss_filtered/analysis/individual_level.csv")
SORTIE = os.path.join(RACINE, "resultats")

# Liste d'exclusion de Stanford, recopiee a l'identique de analyses/a2_baselines_gss.py
# pour que les 149 items soient exactement les memes des deux cotes.
EXCLUS_STANFORD = {q.lower() for q in [
    "BORN", "DEGREE*", "DWELOWN", "EDUC*", "FAMDIF16", "HISPANIC", "MADEG*", "MAEDUC*",
    "MARITAL", "MARTYPE*", "MAWRKGRW", "PADEG*", "PAEDUC*", "PARTYID", "RACE*", "REG16",
    "RELIG*", "RELPERSN", "RVISITOR", "SEX*", "SPEDUC*", "SPRTPRSN", "SPWRKSTA",
    "VETYEARS", "VISITORS", "WIDOWED", "ZODIAC"]}
FUITE_DEMOGRAPHIQUE = ["polviews"]

# Les quatre panels. Pour chacun : fichier, suffixe de colonne par annee d'enquete,
# et les paires de vagues avec leur ecart en annees.
PANELS = {
    "2006-2010": {
        "fichier": "GSS_panel06w123_R6a - Stata.dta",
        "vagues": {2006: "_1", 2008: "_2", 2010: "_3"},
        "paires": [(2006, 2008, 2), (2008, 2010, 2), (2006, 2010, 4)],
    },
    "2008-2012": {
        "fichier": "GSS_panel08w123_R6 - stata.dta",
        "vagues": {2008: "_1", 2010: "_2", 2012: "_3"},
        "paires": [(2008, 2010, 2), (2010, 2012, 2), (2008, 2012, 4)],
    },
    "2010-2014": {
        "fichier": "GSS_panel2010w123_R6 - stata.dta",
        "vagues": {2010: "_1", 2012: "_2", 2014: "_3"},
        "paires": [(2010, 2012, 2), (2012, 2014, 2), (2010, 2014, 4)],
    },
    # Panel 2016-2020 : deux cohortes distinctes, pas trois vagues sur les memes gens.
    # La cohorte 2016 (n = 2867) est reinterrogee en 2020, soit quatre ans.
    # La cohorte 2018 (n = 2348) est reinterrogee en 2020, soit deux ans.
    # Personne n'est interroge en 2016 puis en 2018 : verifie sur les champs year_1a et
    # year_1b, mutuellement exclusifs.
    "2016-2020": {
        "fichier": "gss2020panel_r1a.dta",
        "vagues": {2016: "_1a", 2018: "_1b", 2020: "_2"},
        "paires": [(2018, 2020, 2), (2016, 2020, 4)],
    },
}

MIN_ITEMS_INDIVIDU = 20   # une personne compte si au moins 20 items sont evaluables
MIN_PAIRES_ITEM = 100     # un item compte si au moins 100 personnes l'ont vu deux fois


# ---------------------------------------------------------------------------
# 1. Les 149 items, et leur nom cote GSS
# ---------------------------------------------------------------------------

def items_stanford():
    """Les 149 items cibles de a2, dans l'ordre des colonnes de l'archive."""
    w1 = pd.read_csv(os.path.join(PREP, "p_wave1_summary.csv"))
    items = [c for c in w1.columns if c != "email" and c.lower() not in EXCLUS_STANFORD]
    return [c for c in items if c not in FUITE_DEMOGRAPHIQUE]


def noms_gss(item):
    """Traduit un nom de colonne de l'archive en noms de variables GSS.

    Deux conventions de l'archive, lisibles dans question_master/gss/main.csv :
      - le suffixe "/y" designe un item pose en deux versions de ballot, par exemple
        NATSPAC et NATSPACY, que Stanford fusionne en une seule cible. On rend les deux
        noms, ils seront fusionnes dans cet ordre.
      - l'asterisque final est un marqueur de l'archive, pas un joker : il est retire.
    """
    it = item.lower()
    if it.endswith("/y"):
        return [it[:-2], it[:-2] + "y"]
    if it.endswith("*"):
        return [it[:-1]]
    return [it]


def colonnes_vague(item, suffixe, colonnes):
    """Noms de colonnes reellement presents dans le panel pour cet item a cette vague."""
    return [n + suffixe for n in noms_gss(item) if (n + suffixe) in colonnes]


# ---------------------------------------------------------------------------
# 2. Lecture d'un panel et fusion des versions de ballot
# ---------------------------------------------------------------------------

def serie_fusionnee(df, noms):
    """Une colonne unique a partir des versions de ballot : la premiere renseignee.

    Retourne aussi le vecteur indiquant quelle version a fourni la valeur, ce qui
    permet de mesurer combien de personnes changent de version entre deux vagues.
    """
    if len(noms) == 1:
        return df[noms[0]].values, np.where(df[noms[0]].notna().values, 0, -1)
    v = df[noms[0]].values.copy()
    src = np.where(df[noms[0]].notna().values, 0, -1)
    for k, n in enumerate(noms[1:], start=1):
        remplir = pd.isna(v) & df[n].notna().values
        v = np.where(remplir, df[n].values, v)
        src = np.where(remplir, k, src)
    return v, src


def charger_panel(nom, items):
    """Charge un panel et renvoie, par vague, la matrice personnes x items et la source."""
    cfg = PANELS[nom]
    _, meta = pyreadstat.read_dta(os.path.join(PANEL, cfg["fichier"]),
                                  metadataonly=True, encoding="latin1")
    colonnes = {c.lower(): c for c in meta.column_names}
    besoin, plan = set(), {}
    for annee, suf in cfg["vagues"].items():
        plan[annee] = {}
        for it in items:
            cols = colonnes_vague(it, suf, colonnes)
            if cols:
                plan[annee][it] = cols
                besoin.update(colonnes[c] for c in cols)
    df, _ = pyreadstat.read_dta(os.path.join(PANEL, cfg["fichier"]),
                                usecols=sorted(besoin), encoding="latin1")
    df.columns = [c.lower() for c in df.columns]
    mat, src = {}, {}
    for annee in cfg["vagues"]:
        m = np.full((len(df), len(items)), np.nan, dtype=object)
        s = np.full((len(df), len(items)), -1, dtype=np.int8)
        for j, it in enumerate(items):
            cols = plan[annee].get(it)
            if cols:
                v, q = serie_fusionnee(df, cols)
                m[:, j] = v
                s[:, j] = q
        mat[annee] = m
        src[annee] = s
    return mat, src, plan, len(df)


# ---------------------------------------------------------------------------
# 3. La mesure, avec la definition de Stanford
# ---------------------------------------------------------------------------

def masque_valide(m):
    """Cellule exploitable : ni NaN, ni marqueur de manquant. DK, IAP et NA sont des
    manquants etendus de Stata et arrivent deja en NaN via pyreadstat."""
    return np.array([[not est_manquant(v) for v in ligne] for ligne in m])


def consistance(m_a, m_b, cols=None):
    """Consistance test retest entre deux passations.

    cols, s'il est fourni, restreint le calcul a un sous ensemble d'items. C'est ce qui
    permet de comparer Stanford et le panel sur exactement la meme liste d'items.

    Retourne : exactitude par personne (NaN si moins de MIN_ITEMS_INDIVIDU items
    evaluables), accord par item, et effectifs.
    """
    ok = masque_valide(m_a) & masque_valide(m_b)
    if cols is not None:
        garde = np.zeros(ok.shape[1], dtype=bool)
        garde[list(cols)] = True
        ok &= garde
    egal = (m_a == m_b) & ok
    n_par_personne = ok.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        par_personne = np.where(n_par_personne >= MIN_ITEMS_INDIVIDU,
                                egal.sum(axis=1) / np.maximum(n_par_personne, 1), np.nan)
    n_par_item = ok.sum(axis=0)
    with np.errstate(invalid="ignore", divide="ignore"):
        par_item = np.where(n_par_item >= MIN_PAIRES_ITEM,
                            egal.sum(axis=0) / np.maximum(n_par_item, 1), np.nan)
    return par_personne, par_item, n_par_personne, n_par_item


def accord_de_hasard(colonne):
    """Indice de Simpson de la marginale : accord attendu si les deux passations
    etaient independantes et de meme distribution. Sert a dire si un ecart de
    consistance entre deux jeux vient du delai ou du nombre de modalites."""
    obs = [v for v in colonne if not est_manquant(v)]
    if len(obs) < 2:
        return np.nan
    n = len(obs)
    return sum((k / n) ** 2 for k in Counter(obs).values())


# ---------------------------------------------------------------------------
# 4. Le cote Stanford : deux semaines, sur exactement les memes 149 items
# ---------------------------------------------------------------------------

def stanford(items):
    w1 = pd.read_csv(os.path.join(PREP, "p_wave1_summary.csv"))
    w2 = pd.read_csv(os.path.join(PREP, "p_wave2_summary.csv"))
    assert list(w1["email"]) == list(w2["email"])
    y1 = w1[items].values.astype(object)
    y2 = w2[items].values.astype(object)
    par_personne = exactitude_par_personne(y2, y1)
    ok = masque_valide(y1) & masque_valide(y2)
    par_item = ((y1 == y2) & ok).sum(axis=0) / np.maximum(ok.sum(axis=0), 1)
    return y1, y2, par_personne, par_item


def conditions_llm(items):
    """Exactitude brute des quatre conditions d'agents sur les memes 149 items."""
    w1 = pd.read_csv(os.path.join(PREP, "p_wave1_summary.csv"))
    y1 = w1[items].values.astype(object)
    fichiers = {
        "agents composite": "composite_agents_summary.csv",
        "agents entretien (v3)": "gss_v3_summary.csv",
        "agents enquete": "survey_agents_summary.csv",
        "agents demographiques (v6)": "gss_v6_summary.csv",
    }
    out = {}
    for libelle, f in fichiers.items():
        d = pd.read_csv(os.path.join(PREP, f))
        p = d[items].values.astype(object)
        out[libelle] = float(np.nanmean(exactitude_par_personne(p, y1)))
    return out


# ---------------------------------------------------------------------------
# 5. Programme
# ---------------------------------------------------------------------------

def main():
    os.makedirs(SORTIE, exist_ok=True)
    items = items_stanford()
    qm = pd.read_csv(QMASTER)
    libelles = dict(zip(qm["Question ID"].str.lower(), qm["Question"]))
    n_modalites_st = dict(zip(qm["Question ID"].str.lower(),
                              qm["Options"].fillna("[]").str.count(",") + 1))
    print(f"{len(items)} items cibles, identiques a ceux de a2.")

    y1, y2, st_personne, st_item = stanford(items)
    print(f"Stanford, deux semaines, 149 items : {np.nanmean(st_personne):.6f}")
    ref = pd.read_csv(INDIV)["p_wave1__p_wave2__accuracy"].mean()
    print(f"  controle, champ p_wave1__p_wave2__accuracy, 177 items : {ref:.6f}")

    hasard_st = np.array([accord_de_hasard(y1[:, j]) for j in range(len(items))])
    nmod_st = np.array([len({v for v in y1[:, j] if not est_manquant(v)})
                        for j in range(len(items))])

    # --- les panels
    lignes_app, lignes_item, lignes_ind = [], [], []
    resume = {}
    matrices = {}
    for nom in PANELS:
        mat, src, plan, n_lignes = charger_panel(nom, items)
        matrices[nom] = mat
        annees = list(PANELS[nom]["vagues"])
        for it in items:
            lignes_app.append({
                "item": it, "panel": nom,
                "variables_gss": "+".join(noms_gss(it)),
                "vagues_trouvees": sum(1 for a in annees if it in plan[a]),
                "colonnes": ";".join("|".join(plan[a].get(it, [])) for a in annees),
            })
        for a, b, ecart in PANELS[nom]["paires"]:
            pp, pi, npp, npi = consistance(mat[a], mat[b])
            n_pers = int(np.isfinite(pp).sum())
            n_items_ok = int(np.isfinite(pi).sum())
            cle = (nom, f"{a}-{b}", ecart)
            resume[cle] = {
                "moyenne_individus": float(np.nanmean(pp)),
                "moyenne_items": float(np.nanmean(pi)),
                "ecart_type_individus": float(np.nanstd(pp, ddof=1)),
                "n_personnes": n_pers, "n_items": n_items_ok,
                "items_par_personne_median": float(np.median(npp[np.isfinite(pp)]))
                if n_pers else np.nan,
            }
            # changement de version de ballot entre les deux vagues
            chg = ((src[a] >= 0) & (src[b] >= 0) & (src[a] != src[b])).sum()
            tot = ((src[a] >= 0) & (src[b] >= 0)).sum()
            resume[cle]["part_ballot_change"] = float(chg / tot) if tot else np.nan
            for j, it in enumerate(items):
                if np.isfinite(pi[j]):
                    lignes_item.append({
                        "item": it, "panel": nom, "paire": f"{a}-{b}",
                        "ecart_annees": ecart, "n_paires": int(npi[j]),
                        "consistance": float(pi[j]),
                        "hasard_panel": accord_de_hasard(mat[a][:, j]),
                        "n_modalites_panel": len({v for v in mat[a][:, j]
                                                  if not est_manquant(v)}),
                    })
            q = np.nanpercentile(pp, [10, 25, 50, 75, 90]) if n_pers else [np.nan] * 5
            lignes_ind.append({
                "panel": nom, "paire": f"{a}-{b}", "ecart_annees": ecart,
                "n_personnes": n_pers, "moyenne": resume[cle]["moyenne_individus"],
                "ecart_type": resume[cle]["ecart_type_individus"],
                "min": float(np.nanmin(pp)) if n_pers else np.nan,
                "p10": q[0], "p25": q[1], "mediane": q[2], "p75": q[3], "p90": q[4],
                "max": float(np.nanmax(pp)) if n_pers else np.nan,
                # part calculee sur les seules personnes evaluables, pas sur les lignes
                # du fichier : la plupart des lignes d'un panel n'ont pas de seconde
                # passation et valent NaN.
                "part_sous_70pc": float(np.mean(pp[np.isfinite(pp)] < 0.70))
                if n_pers else np.nan,
            })
            print(f"{nom} {a}->{b} ({ecart} ans) : {resume[cle]['moyenne_individus']:.4f} "
                  f"sur {n_pers} personnes, {n_items_ok} items")

    pd.DataFrame(lignes_app).to_csv(os.path.join(SORTIE, "a12-appariement-items.csv"),
                                    index=False)
    t_item = pd.DataFrame(lignes_item)
    t_item.to_csv(os.path.join(SORTIE, "a12-retest-item.csv"), index=False)

    # ligne Stanford dans le tableau par individu
    lignes_ind.insert(0, {
        "panel": "Stanford (archive OSF)", "paire": "vague1-vague2",
        "ecart_annees": 2 / 52, "n_personnes": int(np.isfinite(st_personne).sum()),
        "moyenne": float(np.nanmean(st_personne)),
        "ecart_type": float(np.nanstd(st_personne, ddof=1)),
        "min": float(np.nanmin(st_personne)),
        "p10": float(np.nanpercentile(st_personne, 10)),
        "p25": float(np.nanpercentile(st_personne, 25)),
        "mediane": float(np.nanpercentile(st_personne, 50)),
        "p75": float(np.nanpercentile(st_personne, 75)),
        "p90": float(np.nanpercentile(st_personne, 90)),
        "max": float(np.nanmax(st_personne)),
        "part_sous_70pc": float(np.mean(st_personne < 0.70)),
    })
    pd.DataFrame(lignes_ind).to_csv(os.path.join(SORTIE, "a12-retest-individu.csv"),
                                    index=False)

    # --- synthese par delai, tous panels confondus
    syn = []
    syn.append({"denominateur": "deux semaines (Stanford, 149 items)", "ecart_annees": 2 / 52,
                "source": "archive OSF t6g7k", "n_personnes": len(st_personne),
                "consistance": float(np.nanmean(st_personne))})
    for ecart in (2, 4):
        cles = [c for c in resume if c[2] == ecart]
        # moyenne ponderee par le nombre de personnes
        num = sum(resume[c]["moyenne_individus"] * resume[c]["n_personnes"] for c in cles)
        den = sum(resume[c]["n_personnes"] for c in cles)
        syn.append({"denominateur": f"{ecart} ans (panels GSS, mise en commun)",
                    "ecart_annees": ecart,
                    "source": "+".join(sorted({c[0] for c in cles})),
                    "n_personnes": den, "consistance": num / den})
    for (nom, paire, ecart), v in resume.items():
        syn.append({"denominateur": f"{nom} {paire}", "ecart_annees": ecart,
                    "source": nom, "n_personnes": v["n_personnes"],
                    "consistance": v["moyenne_individus"]})
    t_syn = pd.DataFrame(syn)
    t_syn.to_csv(os.path.join(SORTIE, "a12-synthese-delais.csv"), index=False)

    # --- recalcul des scores normalises
    bruts = conditions_llm(items)
    print("\nscores bruts sur les 149 items :", {k: round(v, 4) for k, v in bruts.items()})
    denoms = {r["denominateur"]: r["consistance"]
              for _, r in t_syn.iterrows() if r["denominateur"].startswith(("deux semaines", "2 ans", "4 ans"))}
    lignes_norm = []
    d2s = denoms["deux semaines (Stanford, 149 items)"]
    for cond, brut in bruts.items():
        ligne = {"condition": cond, "score_brut": brut}
        for lib, d in denoms.items():
            ligne[f"norm [{lib}]"] = brut / d
        ligne["ecart_2ans_moins_2sem_points"] = 100 * (brut / denoms["2 ans (panels GSS, mise en commun)"] - brut / d2s)
        ligne["ecart_4ans_moins_2sem_points"] = 100 * (brut / denoms["4 ans (panels GSS, mise en commun)"] - brut / d2s)
        lignes_norm.append(ligne)
    t_norm = pd.DataFrame(lignes_norm)
    t_norm.to_csv(os.path.join(SORTIE, "a12-normalisation.csv"), index=False)
    print("\n", t_norm.to_string(index=False))

    # --- item par item : stable a deux semaines, instable a deux ans
    ref2 = (t_item[t_item["ecart_annees"] == 2]
            .groupby("item")
            .apply(lambda g: pd.Series({
                "consistance_2ans": np.average(g["consistance"], weights=g["n_paires"]),
                "n_paires_2ans": g["n_paires"].sum(),
                "hasard_panel": np.average(g["hasard_panel"], weights=g["n_paires"]),
                "n_modalites_panel": g["n_modalites_panel"].max()}),
                include_groups=False))
    ref4 = (t_item[t_item["ecart_annees"] == 4]
            .groupby("item")
            .apply(lambda g: pd.Series({
                "consistance_4ans": np.average(g["consistance"], weights=g["n_paires"]),
                "n_paires_4ans": g["n_paires"].sum()}), include_groups=False))
    comp = pd.DataFrame({
        "item": items,
        "libelle": [str(libelles.get(it, ""))[:110] for it in items],
        "consistance_2sem": st_item,
        "hasard_stanford": hasard_st,
        "n_modalites_stanford": nmod_st,
        "n_modalites_master": [n_modalites_st.get(it, np.nan) for it in items],
    }).set_index("item").join(ref2).join(ref4).reset_index()
    comp["delta_2sem_moins_2ans"] = comp["consistance_2sem"] - comp["consistance_2ans"]
    comp["delta_2sem_moins_4ans"] = comp["consistance_2sem"] - comp["consistance_4ans"]
    comp["delta_hasard"] = comp["hasard_stanford"] - comp["hasard_panel"]
    comp = comp.sort_values("delta_2sem_moins_2ans", ascending=False)
    comp.to_csv(os.path.join(SORTIE, "a12-items-stables-instables.csv"), index=False)

    d = comp.dropna(subset=["consistance_2ans"])
    print(f"\n{len(d)} items apparies et mesures aux deux delais.")
    print(f"correlation de rang 2 semaines / 2 ans : "
          f"{d['consistance_2sem'].corr(d['consistance_2ans'], method='spearman'):.3f}")
    print(f"correlation de Pearson : "
          f"{d['consistance_2sem'].corr(d['consistance_2ans']):.3f}")
    print(f"delta moyen : {d['delta_2sem_moins_2ans'].mean():.4f}, "
          f"ecart type {d['delta_2sem_moins_2ans'].std():.4f}, "
          f"min {d['delta_2sem_moins_2ans'].min():.4f}, "
          f"max {d['delta_2sem_moins_2ans'].max():.4f}")
    print("\nles dix plus gros ecarts (stables a deux semaines, instables a deux ans) :")
    print(d.head(10)[["item", "consistance_2sem", "consistance_2ans",
                      "delta_2sem_moins_2ans"]].to_string(index=False))
    print("\nles dix plus faibles ecarts :")
    print(d.tail(10)[["item", "consistance_2sem", "consistance_2ans",
                      "delta_2sem_moins_2ans"]].to_string(index=False))

    print("\nparts de ballot change par paire :")
    for k, v in resume.items():
        print(f"  {k[0]} {k[1]} : {v['part_ballot_change']:.4f}")

    # ------------------------------------------------------------------
    # 6. Le noyau commun : la seule comparaison honnete
    #
    # Le 79,50 pour cent de Stanford porte sur 149 items, les panels n'en apparient que
    # 124 a 131. Une part de l'ecart pourrait donc venir de la liste d'items et non du
    # delai. On refait tout sur les items mesures dans les onze paires de panel a la
    # fois, cote panel et cote Stanford.
    # ------------------------------------------------------------------
    # Attention, deux panels differents portent la meme etiquette de paire, par exemple
    # 2008-2010 existe dans le panel 2006-2010 et dans le panel 2008-2012. La cle doit
    # donc combiner le panel et la paire.
    t_item["cle_paire"] = t_item["panel"] + " " + t_item["paire"]
    mesures = t_item.groupby("item")["cle_paire"].nunique()
    n_paires_total = sum(len(PANELS[p]["paires"]) for p in PANELS)
    noyau = [it for it in items if mesures.get(it, 0) == n_paires_total]
    idx_noyau = [items.index(it) for it in noyau]
    print(f"\nnoyau commun : {len(noyau)} items mesures dans les {n_paires_total} paires.")

    st_pp_noyau = exactitude_par_personne(y2[:, idx_noyau], y1[:, idx_noyau])
    d_noyau = {"deux semaines": float(np.nanmean(st_pp_noyau))}
    detail_noyau = [{"denominateur": "deux semaines (Stanford)", "ecart_annees": 2 / 52,
                     "source": "archive OSF t6g7k", "n_items": len(noyau),
                     "n_personnes": len(st_pp_noyau),
                     "consistance": d_noyau["deux semaines"]}]
    for ecart in (2, 4):
        num, den = 0.0, 0
        for nom in PANELS:
            for a, b, e in PANELS[nom]["paires"]:
                if e != ecart:
                    continue
                pp, _, _, _ = consistance(matrices[nom][a], matrices[nom][b], idx_noyau)
                n = int(np.isfinite(pp).sum())
                num += float(np.nanmean(pp)) * n
                den += n
                detail_noyau.append({"denominateur": f"{nom} {a}-{b}", "ecart_annees": ecart,
                                     "source": nom, "n_items": len(noyau), "n_personnes": n,
                                     "consistance": float(np.nanmean(pp))})
        d_noyau[f"{ecart} ans"] = num / den
        detail_noyau.append({"denominateur": f"{ecart} ans (mise en commun)",
                             "ecart_annees": ecart, "source": "quatre panels",
                             "n_items": len(noyau), "n_personnes": den,
                             "consistance": num / den})
    pd.DataFrame(detail_noyau).to_csv(os.path.join(SORTIE, "a12-noyau-commun.csv"),
                                      index=False)
    print("denominateurs sur le noyau commun :",
          {k: round(v, 4) for k, v in d_noyau.items()})

    bruts_noyau = {}
    fichiers = {"agents composite": "composite_agents_summary.csv",
                "agents entretien (v3)": "gss_v3_summary.csv",
                "agents enquete": "survey_agents_summary.csv",
                "agents demographiques (v6)": "gss_v6_summary.csv"}
    for libelle, f in fichiers.items():
        p = pd.read_csv(os.path.join(PREP, f))[noyau].values.astype(object)
        bruts_noyau[libelle] = float(np.nanmean(
            exactitude_par_personne(p, y1[:, idx_noyau])))
    lignes_n = []
    for cond, brut in bruts_noyau.items():
        l = {"condition": cond, "n_items": len(noyau), "score_brut": brut}
        for lib, dd in d_noyau.items():
            l[f"norm [{lib}]"] = brut / dd
        l["ecart_2ans_moins_2sem_points"] = 100 * (brut / d_noyau["2 ans"]
                                                   - brut / d_noyau["deux semaines"])
        l["ecart_4ans_moins_2sem_points"] = 100 * (brut / d_noyau["4 ans"]
                                                   - brut / d_noyau["deux semaines"])
        lignes_n.append(l)
    t_nn = pd.DataFrame(lignes_n)
    t_nn.to_csv(os.path.join(SORTIE, "a12-normalisation-noyau.csv"), index=False)
    print("\n", t_nn.to_string(index=False))

    # ------------------------------------------------------------------
    # 7. Le delai touche t il tous les types d'items de la meme facon ?
    # ------------------------------------------------------------------
    fam = {}
    for nom, membres in FAMILLES.items():
        fam.update({m: nom for m in membres})
    comp["famille"] = comp["item"].map(fam).fillna("hors famille")
    g = (comp.dropna(subset=["consistance_2ans"])
         .groupby("famille")
         .agg(n_items=("item", "size"),
              c_2sem=("consistance_2sem", "mean"),
              c_2ans=("consistance_2ans", "mean"),
              c_4ans=("consistance_4ans", "mean"),
              delta_2ans=("delta_2sem_moins_2ans", "mean"),
              delta_4ans=("delta_2sem_moins_4ans", "mean"),
              hasard_st=("hasard_stanford", "mean"),
              hasard_panel=("hasard_panel", "mean"))
         .sort_values("delta_2ans", ascending=False).reset_index())
    g.to_csv(os.path.join(SORTIE, "a12-familles.csv"), index=False)
    print("\npar famille thematique :")
    print(g.to_string(index=False))

    # Le delai est il uniforme ? Regression de la perte sur la stabilite a deux semaines.
    dd = comp.dropna(subset=["consistance_2ans"])
    pente = np.polyfit(dd["consistance_2sem"], dd["delta_2sem_moins_2ans"], 1)
    print(f"\nperte a deux ans = {pente[0]:.3f} x stabilite a deux semaines "
          f"+ {pente[1]:.3f}  (n = {len(dd)})")
    print("correlation perte / stabilite a deux semaines : "
          f"{dd['consistance_2sem'].corr(dd['delta_2sem_moins_2ans']):.3f}")
    print("correlation perte / nombre de modalites (panel) : "
          f"{dd['n_modalites_panel'].corr(dd['delta_2sem_moins_2ans']):.3f}")
    print("correlation hasard Stanford / hasard panel : "
          f"{dd['hasard_stanford'].corr(dd['hasard_panel']):.3f}, "
          f"ecart moyen {dd['delta_hasard'].mean():.4f}")

    # ------------------------------------------------------------------
    # 8. L'echantillon Stanford est il plus stable que le panel NORC ?
    #
    # Deux points suffisent a caler une droite en logarithme du delai, c'est le modele
    # le plus pauvre qui reste defendable : la perte de consistance ralentit avec le
    # temps. On extrapole a deux semaines et on compare a ce que Stanford observe.
    # Le modele est grossier, l'extrapolation porte sur deux ordres de grandeur ; ce
    # qui est interpretable est le signe et l'ordre de grandeur de l'ecart, pas sa valeur.
    # ------------------------------------------------------------------
    e = comp.dropna(subset=["consistance_2ans", "consistance_4ans"]).copy()
    pente_log = (e["consistance_4ans"] - e["consistance_2ans"]) / np.log(2.0)
    e["pente_par_log_annee"] = pente_log
    e["extrapolation_2sem"] = e["consistance_2ans"] + pente_log * (np.log(2 / 52) - np.log(2))
    e["extrapolation_bornee"] = e["extrapolation_2sem"].clip(upper=1.0)
    e["residu_stanford"] = e["consistance_2sem"] - e["extrapolation_bornee"]
    e[["item", "libelle", "consistance_2sem", "consistance_2ans", "consistance_4ans",
       "pente_par_log_annee", "extrapolation_2sem", "extrapolation_bornee",
       "residu_stanford"]].sort_values("residu_stanford").to_csv(
        os.path.join(SORTIE, "a12-extrapolation.csv"), index=False)
    print(f"\nextrapolation logarithmique a deux semaines, {len(e)} items :")
    print(f"  moyenne extrapolee (bornee a 1) : {e['extrapolation_bornee'].mean():.4f}")
    print(f"  moyenne observee chez Stanford  : {e['consistance_2sem'].mean():.4f}")
    print(f"  residu moyen : {e['residu_stanford'].mean():+.4f}, "
          f"mediane {e['residu_stanford'].median():+.4f}, "
          f"part d'items ou Stanford est au dessus : "
          f"{(e['residu_stanford'] > 0).mean():.3f}")
    print(f"  items au dessus de 1 avant bornage : "
          f"{(e['extrapolation_2sem'] > 1).sum()}")

    # ------------------------------------------------------------------
    # 9. Intervalles de confiance sur les trois denominateurs, noyau commun
    # ------------------------------------------------------------------
    from a2_commun import bootstrap_personnes
    lignes_ic = []
    m, b, h = bootstrap_personnes(st_pp_noyau)
    lignes_ic.append({"denominateur": "deux semaines", "n_items": len(noyau),
                      "n_personnes": int(np.isfinite(st_pp_noyau).sum()),
                      "consistance": m, "ic_bas": b, "ic_haut": h})
    for ecart in (2, 4):
        toutes = []
        for nom in PANELS:
            for a, bb, ee in PANELS[nom]["paires"]:
                if ee != ecart:
                    continue
                pp, _, _, _ = consistance(matrices[nom][a], matrices[nom][bb], idx_noyau)
                toutes.append(pp[np.isfinite(pp)])
        v = np.concatenate(toutes)
        m, b, h = bootstrap_personnes(v)
        lignes_ic.append({"denominateur": f"{ecart} ans", "n_items": len(noyau),
                          "n_personnes": len(v), "consistance": m,
                          "ic_bas": b, "ic_haut": h})
    t_ic = pd.DataFrame(lignes_ic)
    t_ic.to_csv(os.path.join(SORTIE, "a12-denominateurs-ic.csv"), index=False)
    print("\n", t_ic.to_string(index=False))


if __name__ == "__main__":
    main()
