"""
a46b_tableaux : lecture d'interpretation du run composition a46 et de son evaluation.

Aucun appel de modele de langage. Lecture seule sur data/traces/ et sur les tableaux
a46-*.csv deja ecrits. Aucun fichier existant du depot n'est modifie ; tout ce qui sort
porte le prefixe `a46b`.

CE QU'IL FAIT
-------------
1. Le tableau par item, par modele, par ancrage et par identite : les trois termes, les
   deux bases de realite, les trois ecarts, les deux exagerations et leur rapport.
2. Les cellules de taux de base, et le contraste camp moins population (H4).
3. L'effet de l'identite du demandeur (H3) et l'effet de l'ancrage (question de methode).
4. La puissance honnete du plan preenregistre : le p minimal atteignable par une
   permutation de signe bilaterale a n items, avant et apres Holm.
5. Les quatre criteres de chute de la page de plan, evalues.
6. Le pont r1 : union1 et reborn mesures par deux instruments.
7. Le retrecissement vers l'uniforme de r1 confronte aux compositions.

Sorties : resultats/a46b-*.csv
Usage   : .venv/bin/python analyses/a46b_tableaux.py
"""

import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a46_commun as C  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
TRACES = os.path.join(RACINE, "data", "traces")
N_BOOT = 2000
N_PERM = 20000
BANDE_NULLE = (0.90, 1.11)

ORDRE = ["dem_black", "dem_union", "dem_aa", "dem_lgb",
         "rep_evang", "rep_rich", "rep_old", "rep_south"]
MODELES = ["q4", "oss20", "q30"]
NOM_LONG = {"q4": "Qwen3-4B", "oss20": "gpt-oss-20b", "q30": "Qwen3-30B-A3B"}


def ic_bootstrap_moyenne(x, rng, n=N_BOOT):
    x = np.asarray(x, float)
    x = x[np.isfinite(x)]
    if len(x) < 2:
        return (float(x.mean()) if len(x) else np.nan), np.nan, np.nan
    idx = rng.integers(0, len(x), size=(n, len(x)))
    t = x[idx].mean(axis=1)
    return float(x.mean()), float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5))


def p_signe(d, rng, n=N_PERM):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 2:
        return float("nan")
    obs = abs(d.mean())
    s = rng.choice([-1.0, 1.0], size=(n, len(d)))
    stat = np.abs((s * d[None, :]).mean(axis=1))
    return float((int((stat >= obs - 1e-15).sum()) + 1.0) / (n + 1.0))


def p_minimal_signe(n):
    """p bilateral le plus petit qu'une permutation de signe a n items puisse rendre.

    Toutes les 2^n configurations de signe sont equiprobables ; la statistique observee
    est atteinte au moins par la configuration identite et par son opposee. Le p exact
    plancher vaut donc 2 / 2^n, et l'estimateur de Phipson et Smyth le releve encore.
    """
    if n < 1:
        return np.nan
    return 2.0 / (2 ** n)


# --------------------------------------------------------------------------------------


def charger():
    trois = pd.read_csv(os.path.join(SORTIE, "a46-trois-termes.csv"))
    tests = pd.read_csv(os.path.join(SORTIE, "a46-trois-termes-tests.csv"))
    gss = pd.read_csv(os.path.join(SORTIE, "a46-composition-gss-2024.csv"))
    hum = pd.read_csv(os.path.join(SORTIE, "a46-ahler-sood-items.csv"))
    traces = []
    for m in MODELES:
        p = os.path.join(TRACES, f"a46-composition-{m}.jsonl")
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                traces += [json.loads(l) for l in fh if l.strip()]
    return trois, tests, gss, hum, pd.DataFrame(traces)


def table_par_item(trois):
    """Une ligne par (item, modele, ancrage, identite), camp decrit par Ahler et Sood."""
    c = trois[trois["source_modele"].str.startswith("run composition")].copy()
    c = c[c["ancrage"] != "population"]
    c = c[c["camp_est_celui_decrit_par_ahler_sood"]].copy()
    c["ecart_modele_moins_reel_gss_points"] = c["croyance_modele"] - c["realite_gss2024"]
    c["ecart_modele_moins_reel_as_points"] = (c["croyance_modele"]
                                              - c["realite_ahler_sood_anes2012"])
    c["ecart_humain_moins_reel_as_points"] = (c["croyance_humaine"]
                                              - c["realite_ahler_sood_anes2012"])
    c["ecart_modele_moins_humain_points"] = c["croyance_modele"] - c["croyance_humaine"]
    # Variantes de base declarees APRES COUP, robustesse de direction seulement.
    c["rapport_exagerations_base_as_commune"] = np.where(
        c["croyance_humaine"] > 0,
        c["croyance_modele"] / c["croyance_humaine"], np.nan)
    c["rapport_exagerations_base_gss_commune"] = c["rapport_exagerations_base_as_commune"]
    c["item_ordre"] = c["item_as"].map({k: i for i, k in enumerate(ORDRE)})
    cols = ["item_ordre", "item_as", "groupe", "parti_as", "camp", "cle_modele", "modele",
            "ancrage", "identite",
            "realite_ahler_sood_anes2012", "realite_gss2024",
            "croyance_humaine", "croyance_modele",
            "ecart_humain_moins_reel_as_points", "ecart_modele_moins_reel_as_points",
            "ecart_modele_moins_reel_gss_points", "ecart_modele_moins_humain_points",
            "exageration_humaine_ratio_as", "exageration_modele_ratio_as",
            "exageration_modele_ratio_gss",
            "rapport_des_exagerations_base_propre",
            "rapport_des_exagerations_cible_commune"]
    return c.sort_values(["item_ordre", "cle_modele", "ancrage", "identite"])[cols]


def table_taux_de_base(trois, gss):
    """H4 : le taux de base du modele, et le contraste camp moins population."""
    base = trois[(trois["ancrage"] == "population")].copy()
    base = base[["item_as", "groupe", "cle_modele", "modele", "croyance_modele",
                 "realite_gss2024", "realite_ahler_sood_anes2012"]]
    base = base.rename(columns={"croyance_modele": "modele_population",
                                "realite_gss2024": "reel_population_gss"})
    camp = trois[(trois["source_modele"].str.startswith("run composition"))
                 & (trois["ancrage"] != "population")
                 & (trois["camp_est_celui_decrit_par_ahler_sood"])].copy()
    lignes = []
    for _, b in base.iterrows():
        sous = camp[(camp["item_as"] == b["item_as"])
                    & (camp["cle_modele"] == b["cle_modele"])]
        for _, r in sous.iterrows():
            lignes.append({
                "item_as": b["item_as"], "groupe": b["groupe"],
                "cle_modele": b["cle_modele"], "modele": b["modele"],
                "ancrage": r["ancrage"], "identite": r["identite"], "camp": r["camp"],
                "modele_population": b["modele_population"],
                "reel_population_gss": b["reel_population_gss"],
                "modele_camp": r["croyance_modele"],
                "reel_camp_gss": r["realite_gss2024"],
                "contraste_modele_points": r["croyance_modele"] - b["modele_population"],
                "contraste_reel_points": r["realite_gss2024"] - b["reel_population_gss"],
                "exces_taux_de_base_points": (b["modele_population"]
                                              - b["reel_population_gss"]),
            })
    d = pd.DataFrame(lignes)
    if not d.empty:
        d["signe_concordant"] = (np.sign(d["contraste_modele_points"])
                                 == np.sign(d["contraste_reel_points"]))
        d["item_ordre"] = d["item_as"].map({k: i for i, k in enumerate(ORDRE)})
        d = d.sort_values(["item_ordre", "cle_modele", "ancrage", "identite"])
        d = d.drop(columns=["item_ordre"])
    return d


def table_identite(par_item, rng):
    """H3 : ecart absolu entre la valeur donnee au journaliste et a l'adversaire."""
    lignes = []
    piv = par_item.pivot_table(index=["item_as", "cle_modele", "modele", "ancrage"],
                               columns="identite", values="croyance_modele")
    piv = piv.reset_index()
    if "journaliste" not in piv or "adversaire" not in piv:
        return pd.DataFrame(), pd.DataFrame()
    piv["ecart_points"] = piv["adversaire"] - piv["journaliste"]
    piv["ecart_absolu_points"] = piv["ecart_points"].abs()
    for (cle, ancrage), g in piv.groupby(["cle_modele", "ancrage"]):
        m, bas, haut = ic_bootstrap_moyenne(g["ecart_absolu_points"], rng)
        ms, bs, hs = ic_bootstrap_moyenne(g["ecart_points"], rng)
        lignes.append({
            "cle_modele": cle, "modele": NOM_LONG.get(cle, cle), "ancrage": ancrage,
            "n_items": int(g["ecart_points"].notna().sum()),
            "n_items_identiques": int((g["ecart_points"] == 0).sum()),
            "ecart_absolu_moyen_points": m, "ic_bas": bas, "ic_haut": haut,
            "ecart_signe_moyen_points": ms, "signe_ic_bas": bs, "signe_ic_haut": hs,
            "ecart_max_points": float(g["ecart_absolu_points"].max()),
        })
    return pd.DataFrame(lignes), piv


def table_ancrage(par_item, rng):
    """Parti contre ideologie, a item, modele et identite fixes."""
    piv = par_item.pivot_table(index=["item_as", "cle_modele", "identite"],
                               columns="ancrage", values="croyance_modele").reset_index()
    if "parti" not in piv or "ideologie" not in piv:
        return pd.DataFrame(), pd.DataFrame()
    piv["ecart_points"] = piv["parti"] - piv["ideologie"]
    piv["ecart_absolu_points"] = piv["ecart_points"].abs()
    lignes = []
    for cle, g in piv.groupby("cle_modele"):
        m, bas, haut = ic_bootstrap_moyenne(g["ecart_absolu_points"], rng)
        ms, bs, hs = ic_bootstrap_moyenne(g["ecart_points"], rng)
        lignes.append({
            "cle_modele": cle, "modele": NOM_LONG.get(cle, cle),
            "n_couples": int(g["ecart_points"].notna().sum()),
            "n_identiques": int((g["ecart_points"] == 0).sum()),
            "ecart_absolu_moyen_points": m, "ic_bas": bas, "ic_haut": haut,
            "ecart_signe_moyen_points_parti_moins_ideologie": ms,
            "signe_ic_bas": bs, "signe_ic_haut": hs,
        })
    return pd.DataFrame(lignes), piv


def table_verdict(tests):
    """Le verdict preenregistre, cellule par cellule, avec la puissance honnete."""
    t = tests[tests["source_modele"].str.startswith("run composition")].copy()
    t["p_minimal_atteignable"] = t["n_items"].map(p_minimal_signe)
    t["p_minimal_apres_holm"] = t["p_minimal_atteignable"] * t["taille_famille"]
    t["seuil_atteignable"] = t["p_minimal_apres_holm"] < 0.05
    t["direction_ponctuelle"] = np.where(
        t["rapport_des_moyennes"] > 1.11, "le modele exagere plus",
        np.where(t["rapport_des_moyennes"] < 0.90, "le modele exagere moins",
                 "dans la bande de nullite pratique"))
    cols = ["quantite", "cle_modele", "modele", "ancrage", "identite", "camp",
            "n_items", "items", "rapport_des_moyennes", "rapport_ic_bas",
            "rapport_ic_haut", "rapport_geometrique", "p_permutation", "p_holm",
            "taille_famille", "verdict", "p_minimal_atteignable",
            "p_minimal_apres_holm", "seuil_atteignable", "direction_ponctuelle"]
    return t[cols].sort_values(["quantite", "cle_modele", "ancrage", "identite", "camp"])


def test_groupe(par_item, rng, label, col_a, col_b, groupes):
    """Test de permutation de signe sur log(a) - log(b), groupes libres.

    NON PREENREGISTRE quand `groupes` ne contient pas le camp : la page de plan teste
    camp par camp, quatre items. Le regroupement des huit items est declare ici comme
    une lecture de puissance, jamais comme le test principal.
    """
    lignes = []
    for cles, g in par_item.groupby(groupes, sort=False):
        a = g[col_a].to_numpy(float)
        b = g[col_b].to_numpy(float)
        m = np.isfinite(a) & np.isfinite(b) & (a > 0) & (b > 0)
        n_exclus = int((~m).sum())
        aa, bb = a[m], b[m]
        if len(aa) == 0:
            continue
        d = np.log(aa) - np.log(bb)
        p = p_signe(d, rng)
        moy, bas, haut = ic_bootstrap_moyenne(d, rng)
        lignes.append({
            "lecture": label,
            **{k: v for k, v in zip(groupes if isinstance(groupes, list) else [groupes],
                                    cles if isinstance(cles, tuple) else (cles,))},
            "n_items": int(len(aa)), "n_items_exclus_valeur_nulle": n_exclus,
            "items": ",".join(sorted(g.loc[m, "item_as"].tolist())),
            "rapport_geometrique": float(np.exp(moy)),
            "ic_bas": float(np.exp(bas)), "ic_haut": float(np.exp(haut)),
            "p_permutation": p,
            "p_minimal_atteignable": p_minimal_signe(len(aa)),
        })
    return pd.DataFrame(lignes)


def table_points(par_item, rng):
    """La comparaison en POINTS, qui survit aux valeurs nulles du gpt-oss.

    Le rapport de logarithmes exclut toute cellule ou le modele a repondu zero. Comme
    zero est la reponse la plus eloignee de la croyance humaine par le bas, cette
    exclusion penche du cote « le modele exagere ». La lecture en points garde tout.
    NON PREENREGISTREE, declaree comme telle.
    """
    lignes = []
    for (cle, ancrage, identite, camp), g in par_item.groupby(
            ["cle_modele", "ancrage", "identite", "camp"], sort=False):
        d = (g["ecart_modele_moins_reel_as_points"].to_numpy(float)
             - g["ecart_humain_moins_reel_as_points"].to_numpy(float))
        moy, bas, haut = ic_bootstrap_moyenne(d, rng)
        lignes.append({
            "cle_modele": cle, "modele": NOM_LONG.get(cle, cle), "ancrage": ancrage,
            "identite": identite, "camp": camp, "n_items": int(len(d)),
            "ecart_des_exagerations_points": moy, "ic_bas": bas, "ic_haut": haut,
            "p_permutation": p_signe(d, rng),
            "p_minimal_atteignable": p_minimal_signe(len(d)),
        })
    return pd.DataFrame(lignes)


def table_criteres(traces, trois, gss):
    """Les quatre criteres de chute de la page de plan, evalues un par un."""
    lignes = []
    for m in MODELES:
        t = traces[traces["cle_modele"] == m]
        n = len(t)
        rejets = int(t["rejet"].sum())
        lignes.append({"critere": "1. plus de 25 % de rejets apres relance",
                       "cle_modele": m, "modele": NOM_LONG[m],
                       "valeur": f"{rejets}/{n} = {100.0*rejets/n:.1f} %",
                       "seuil": "25 %",
                       "declenche": bool(100.0 * rejets / n > 25.0)})
    camp = trois[(trois["source_modele"].str.startswith("run composition"))
                 & (trois["ancrage"] != "population")
                 & (trois["camp_est_celui_decrit_par_ahler_sood"])]
    for m in MODELES:
        g = camp[camp["cle_modele"] == m]["croyance_modele"]
        vc = g.value_counts()
        part = float(vc.iloc[0]) / len(g) if len(g) else np.nan
        lignes.append({"critere": "2. une valeur constante dans plus de 75 % des cellules",
                       "cle_modele": m, "modele": NOM_LONG[m],
                       "valeur": (f"valeur modale {vc.index[0]:.0f} dans "
                                  f"{vc.iloc[0]}/{len(g)} = {100*part:.1f} % ; "
                                  f"{g.nunique()} valeurs distinctes sur {len(g)}"),
                       "seuil": "75 %", "declenche": bool(part > 0.75)})
    base = trois[trois["ancrage"] == "population"]
    for m in MODELES:
        b = base[base["cle_modele"] == m].set_index("item_as")["croyance_modele"]
        g = camp[camp["cle_modele"] == m]
        egal = 0
        total = 0
        for item in ORDRE:
            if item not in b.index:
                continue
            sous = g[g["item_as"] == item]["croyance_modele"]
            if not len(sous):
                continue
            total += 1
            if bool((sous == b.loc[item]).all()):
                egal += 1
        part = egal / total if total else np.nan
        lignes.append({"critere": "3. taux de base identique a la valeur du camp sur plus "
                                  "de 75 % des groupes",
                       "cle_modele": m, "modele": NOM_LONG[m],
                       "valeur": f"{egal}/{total} groupes",
                       "seuil": "75 %", "declenche": bool(part > 0.75)})
    eff = gss[(gss["variante"] == "principale") & (gss["item_as"] == "dem_black")]
    detail = "; ".join(f"{r['partition']}/{r['camp']} n={int(r['n_classes'])}"
                       for _, r in eff.iterrows())
    attendu = {("ideologie", "gauche"): 417, ("ideologie", "centre"): 303,
               ("ideologie", "droite"): 332, ("parti", "gauche"): 496,
               ("parti", "centre"): 164, ("parti", "droite"): 367}
    ok = all(int(eff[(eff["partition"] == p) & (eff["camp"] == c)]["n_classes"].iloc[0]) == n
             for (p, c), n in attendu.items()
             if len(eff[(eff["partition"] == p) & (eff["camp"] == c)]))
    lignes.append({"critere": "4. la realite du GSS ne se recalcule pas sur les effectifs "
                              "de camp de r1",
                   "cle_modele": "", "modele": "",
                   "valeur": detail, "seuil": "417/303/332 et 496/164/367",
                   "declenche": bool(not ok)})
    return pd.DataFrame(lignes)


def table_pont_r1(trois):
    """union1 et reborn mesures par deux instruments : r1 et la question directe."""
    r1 = trois[trois["source_modele"].str.startswith("traces r1")].copy()
    comp = trois[(trois["source_modele"].str.startswith("run composition"))
                 & (trois["ancrage"] == "ideologie")].copy()
    lignes = []
    for _, r in r1.iterrows():
        sous = comp[(comp["item_as"] == r["item_as"])
                    & (comp["cle_modele"] == r["cle_modele"])
                    & (comp["camp"] == r["camp"])
                    & (comp["identite"] == r["identite"])]
        lignes.append({
            "item_as": r["item_as"], "item_gss": r["item_gss"],
            "cle_modele": r["cle_modele"], "modele": r["modele"],
            "camp": r["camp"], "identite": r["identite"],
            "reel_gss2024": r["realite_gss2024"],
            "croyance_humaine": r["croyance_humaine"],
            "modele_via_r1_distribution": r["croyance_modele"],
            "modele_via_question_directe": (float(sous["croyance_modele"].iloc[0])
                                            if len(sous) else np.nan),
        })
    d = pd.DataFrame(lignes)
    if not d.empty:
        d["ecart_entre_instruments_points"] = (d["modele_via_question_directe"]
                                               - d["modele_via_r1_distribution"])
    return d


def table_retrecissement(par_item, trois):
    """La regle de r1, p_decrit = alpha p_reel + (1 - alpha) uniforme, sur K = 2.

    Sur une question de composition, la partition est binaire, appartenir ou non : le
    point fixe d'une regle de retrecissement vers l'uniforme est donc 50 pour cent et
    non 34. On rapporte l'alpha implicite de chaque cellule, alpha = (decrit - 50) /
    (reel - 50), et on le compare a l'alpha median de r1 a K = 2, 0,758 tous modeles.
    """
    d = par_item.copy()
    d["alpha_implicite_k2"] = ((d["croyance_modele"] - 50.0)
                               / (d["realite_gss2024"] - 50.0))
    base = trois[trois["ancrage"] == "population"].copy()
    base["alpha_implicite_k2"] = ((base["croyance_modele"] - 50.0)
                                  / (base["realite_gss2024"] - 50.0))
    base = base[["item_as", "cle_modele", "modele", "croyance_modele",
                 "realite_gss2024", "alpha_implicite_k2"]]
    base["ancrage"] = "population"
    base["identite"] = "journaliste"
    base["camp"] = "ensemble"
    cols = ["item_as", "cle_modele", "modele", "ancrage", "identite", "camp",
            "realite_gss2024", "croyance_modele", "alpha_implicite_k2"]
    out = pd.concat([d[cols], base[cols]], ignore_index=True)
    out["item_ordre"] = out["item_as"].map({k: i for i, k in enumerate(ORDRE)})
    return out.sort_values(["item_ordre", "cle_modele", "ancrage", "identite"]).drop(
        columns=["item_ordre"])


def main():
    rng = np.random.default_rng(20260909)
    trois, tests, gss, hum, traces = charger()

    par_item = table_par_item(trois)
    C.ecrire(par_item, "a46b-par-item.csv")

    tb = table_taux_de_base(trois, gss)
    C.ecrire(tb, "a46b-taux-de-base.csv")

    ident, ident_brut = table_identite(par_item, rng)
    C.ecrire(ident, "a46b-identite.csv")

    anc, anc_brut = table_ancrage(par_item, rng)
    C.ecrire(anc, "a46b-ancrage.csv")

    verd = table_verdict(tests)
    C.ecrire(verd, "a46b-verdict-cellule.csv")

    # Lectures de puissance, NON PREENREGISTREES : les huit items ensemble.
    pool = pd.concat([
        test_groupe(par_item, rng, "base propre, 8 items groupes",
                    "exageration_modele_ratio_gss", "exageration_humaine_ratio_as",
                    ["cle_modele", "ancrage", "identite"]),
        test_groupe(par_item, rng, "cible commune, 8 items groupes",
                    "croyance_modele", "croyance_humaine",
                    ["cle_modele", "ancrage", "identite"]),
        test_groupe(par_item, rng, "base ANES commune, 8 items groupes",
                    "exageration_modele_ratio_as", "exageration_humaine_ratio_as",
                    ["cle_modele", "ancrage", "identite"]),
    ], ignore_index=True)
    C.ecrire(pool, "a46b-tests-groupes.csv")

    pts = table_points(par_item, rng)
    C.ecrire(pts, "a46b-points.csv")

    crit = table_criteres(traces, trois, gss)
    C.ecrire(crit, "a46b-criteres-de-chute.csv")

    pont = table_pont_r1(trois)
    C.ecrire(pont, "a46b-pont-r1.csv")

    retr = table_retrecissement(par_item, trois)
    C.ecrire(retr, "a46b-retrecissement.csv")

    # Puissance : le p minimal atteignable, par n items et par taille de famille.
    puiss = pd.DataFrame([
        {"n_items": n, "p_minimal_bilateral": p_minimal_signe(n),
         "p_minimal_apres_holm_famille_2": min(1.0, 2 * p_minimal_signe(n)),
         "atteint_0_05_seul": p_minimal_signe(n) < 0.05,
         "atteint_0_05_famille_2": min(1.0, 2 * p_minimal_signe(n)) < 0.05}
        for n in range(1, 13)])
    C.ecrire(puiss, "a46b-puissance.csv")

    print("--- par item, moyenne sur les deux ancrages et les deux identites ---")
    ag = par_item.groupby(["item_as", "cle_modele"]).agg(
        reel_as=("realite_ahler_sood_anes2012", "first"),
        reel_gss=("realite_gss2024", "mean"),
        humain=("croyance_humaine", "first"),
        modele=("croyance_modele", "mean")).reset_index()
    ag["item_ordre"] = ag["item_as"].map({k: i for i, k in enumerate(ORDRE)})
    print(ag.sort_values(["item_ordre", "cle_modele"]).to_string(index=False))
    print()
    print("--- criteres de chute ---")
    print(crit.to_string(index=False))
    print()
    print("--- puissance ---")
    print(puiss.to_string(index=False))
    print()
    print("--- tests groupes, 8 items, NON PREENREGISTRES ---")
    print(pool.to_string(index=False))
    print()
    print("--- points, NON PREENREGISTRE ---")
    print(pts.to_string(index=False))
    print()
    print("--- identite ---")
    print(ident.to_string(index=False))
    print()
    print("--- ancrage ---")
    print(anc.to_string(index=False))


if __name__ == "__main__":
    main()
