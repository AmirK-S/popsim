"""
r4b_contrastes : les contrastes apparies entre conditions de R4, et la part du format.

Statut : script d'analyse jetable. Aucun appel de modele. Il lit les tableaux ecrits par
`r1_evaluer.py --suffixe r4` et par `r4_oracle_socle.py --h4`, et rien d'autre. Aucun
script existant n'est modifie.

Ce qu'il calcule, dans les definitions figees par resultats/r1-preenregistrement.md
section 5 et resultats/r4-preenregistrement.md section 6 :

  1. Les contrastes apparies par item entre deux conditions, sur les deux quantites
     preenregistrees de H3 : le facteur d'amplification signe H2b (79 items orientes,
     puis 65 items retenus stricts) et le ratio de dispersion H1 (par camp).
     Les deux conditions partagent les items ; le referent humain est le meme fichier ;
     le denominateur du facteur est donc identique des deux cotes une fois le perimetre
     restreint aux items valides dans les deux conditions. La difference de facteurs vaut
     alors (moyenne_A - moyenne_B) / moyenne_reel, et le test apparie porte exactement sur
     la difference des quantites decrites par item.

  2. La part du format de H3 : (X_q4nogab - X_q4) / (X_q4base - X_q4), calculee seulement
     si l'IC de (X_q4base - X_q4) exclut zero, comme la page de plan l'impose.

  3. Le contraste de H4 entre conditions, apparie par (item, camp).

  4. Une sensibilite : tout est rejoue sur le perimetre commun aux quatre conditions.

Entree  : resultats/r1-par-cellule-r4.csv, r1-par-item-ecarts-r4.csv,
          r4-h4-par-cellule.csv, a37-orientation-items.csv, a37-gss-par-item.csv
Sortie  : resultats/r4b-contraste-h2b.csv, r4b-contraste-h1.csv, r4b-part-format.csv,
          r4b-contraste-h4.csv, r4b-sensibilite-perimetre.csv

Usage :
  .venv/bin/python analyses/r4b_contrastes.py
"""

import os
import sys

import numpy as np
import pandas as pd

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a28_commun import holm            # noqa: E402

GRAINE = 20260910
N_BOOT = 2000
N_PERM = 20000

CONDITIONS = {
    "q4": "Qwen3-4B-Instruct-2507, gabarit ChatML",
    "q4nogab": "Qwen3-4B-Instruct-2507, completion 3 exemples",
    "q4base": "Qwen3-4B-Base, completion 3 exemples",
    "q4hyb": "Qwen3-4B, completion 3 exemples",
}


# ---------------------------------------------------------------------------
# Statistiques, definitions de r1_evaluer recopiees a l'identique
# ---------------------------------------------------------------------------

def p_permutation_signe(d, rng, n=N_PERM):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 3:
        return float("nan")
    obs = abs(d.mean())
    signes = rng.choice([-1.0, 1.0], size=(n, len(d)))
    stat = np.abs((signes * d[None, :]).mean(axis=1))
    return float((int((stat >= obs - 1e-15).sum()) + 1.0) / (n + 1.0))


def ic_difference_de_facteurs(a, b, ref, rng, n=N_BOOT):
    """IC bootstrap sur les items de (moyenne(a) - moyenne(b)) / moyenne(ref).

    a et b sont la meme quantite decrite par deux conditions, ref la quantite reelle,
    les trois alignees item par item sur le perimetre commun. L'unite de
    reechantillonnage est l'item, les trois series sont tirees ensemble.
    """
    a, b, ref = (np.asarray(x, float) for x in (a, b, ref))
    m = np.isfinite(a) & np.isfinite(b) & np.isfinite(ref)
    a, b, ref = a[m], b[m], ref[m]
    if len(a) < 3 or ref.mean() == 0:
        return (float("nan"),) * 3 + (int(len(a)),)
    obs = float((a.mean() - b.mean()) / ref.mean())
    idx = rng.integers(0, len(a), size=(n, len(a)))
    t = (a[idx].mean(axis=1) - b[idx].mean(axis=1)) / ref[idx].mean(axis=1)
    t = t[np.isfinite(t)]
    return obs, float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5)), int(len(a))


def ic_moyenne(d, rng, n=N_BOOT):
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 3:
        return (float("nan"),) * 3 + (int(len(d)),)
    idx = rng.integers(0, len(d), size=(n, len(d)))
    t = d[idx].mean(axis=1)
    return (float(d.mean()), float(np.percentile(t, 2.5)),
            float(np.percentile(t, 97.5)), int(len(d)))


def facteur(a, ref):
    a, ref = np.asarray(a, float), np.asarray(ref, float)
    return float(a.mean() / ref.mean())


# ---------------------------------------------------------------------------
# Lecture
# ---------------------------------------------------------------------------

def lire():
    cel = pd.read_csv(os.path.join(SORTIE, "r1-par-cellule-r4.csv"))
    eca = pd.read_csv(os.path.join(SORTIE, "r1-par-item-ecarts-r4.csv"))
    h4 = pd.read_csv(os.path.join(SORTIE, "r4-h4-par-cellule.csv"))
    o = pd.read_csv(os.path.join(SORTIE, "a37-orientation-items.csv"))
    d = pd.read_csv(os.path.join(SORTIE, "a37-gss-par-item.csv"))
    oriente = dict(zip(o["item"], o["oriente"].astype(bool)))
    strict = dict(zip(d["item"], d["retenu_strict"].astype(bool)))
    return cel, eca, h4, oriente, strict


def perimetre_commun(eca, identite, filtre):
    """Items orientes presents dans les quatre conditions pour cette identite."""
    g = eca[eca["identite"] == identite]
    g = g[g["item"].map(lambda i: bool(filtre.get(i, False)))]
    ens = None
    for cle in CONDITIONS:
        s = set(g[g["cle_modele"] == cle]["item"])
        ens = s if ens is None else (ens & s)
    return ens


# ---------------------------------------------------------------------------
# 1. H2b, contraste apparie entre deux conditions
# ---------------------------------------------------------------------------

def contraste_h2b(eca, oriente, strict, rng, items_communs=None, etiquette="perimetre par paire"):
    lignes = []
    perimetres = (("79 items orientes", oriente), ("items retenus stricts", strict))
    paires = (("q4nogab", "q4", "F3, format seul, poids fixes"),
              ("q4base", "q4nogab", "F4, poids seuls, format fixe"),
              ("q4hyb", "q4", "hors famille, hybride contre instruit sous gabarit"),
              ("q4hyb", "q4nogab", "hors famille, hybride contre instruit 2507, format fixe"),
              ("q4base", "q4", "hors famille, socle contre instruit sous gabarit"))
    for nom_per, filtre in perimetres:
        for identite in ("journaliste", "adversaire"):
            g = eca[eca["identite"] == identite]
            g = g[g["item"].map(lambda i: bool(filtre.get(i, False)))]
            for ca, cb, famille in paires:
                ga = g[g["cle_modele"] == ca].set_index("item")
                gb = g[g["cle_modele"] == cb].set_index("item")
                communs = sorted(set(ga.index) & set(gb.index))
                if items_communs is not None:
                    communs = sorted(set(communs) & items_communs[(identite, nom_per)])
                if len(communs) < 3:
                    continue
                a = ga.loc[communs, "gap_signe_decrit"].to_numpy()
                b = gb.loc[communs, "gap_signe_decrit"].to_numpy()
                ref = ga.loc[communs, "gap_signe_reel_w1"].to_numpy()
                dif, bas, haut, n = ic_difference_de_facteurs(a, b, ref, rng)
                lignes.append({
                    "perimetre": nom_per, "etendue": etiquette, "identite": identite,
                    "condition_a": ca, "condition_b": cb, "famille": famille,
                    "n_items": n,
                    "facteur_a": facteur(a, ref), "facteur_b": facteur(b, ref),
                    "difference_de_facteurs": dif, "ic_bas": bas, "ic_haut": haut,
                    "p": p_permutation_signe(a - b, rng),
                })
    # Holm dans la famille preenregistree seulement : F3 et F4 comptent deux tests
    # chacune, le facteur H2b sur les 79 items orientes et le ratio H1 du camp de gauche,
    # en identite journaliste. Le second test est pose dans contraste_h1 ; ici on n'ecrit
    # que le p brut et l'appartenance, et poser_holm_familles fait la correction.
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 2. H1, contraste apparie entre deux conditions
# ---------------------------------------------------------------------------

def contraste_h1(cel, rng, items_communs_camp=None, etiquette="perimetre par paire"):
    lignes = []
    ok = cel[~cel["rejet"]]
    paires = (("q4nogab", "q4", "F3, format seul, poids fixes"),
              ("q4base", "q4nogab", "F4, poids seuls, format fixe"),
              ("q4hyb", "q4", "hors famille, hybride contre instruit sous gabarit"),
              ("q4hyb", "q4nogab", "hors famille, hybride contre instruit 2507, format fixe"),
              ("q4base", "q4", "hors famille, socle contre instruit sous gabarit"))
    for camp in ("gauche", "centre", "droite"):
        for identite in ("journaliste", "adversaire"):
            g = ok[(ok["camp"] == camp) & (ok["identite"] == identite)]
            for ca, cb, famille in paires:
                ga = g[g["cle_modele"] == ca].set_index("item")
                gb = g[g["cle_modele"] == cb].set_index("item")
                communs = sorted(set(ga.index) & set(gb.index))
                if items_communs_camp is not None:
                    communs = sorted(set(communs) & items_communs_camp[(camp, identite)])
                if len(communs) < 3:
                    continue
                a = ga.loc[communs, "gs_decrit"].to_numpy()
                b = gb.loc[communs, "gs_decrit"].to_numpy()
                ref = ga.loc[communs, "gs_reel_w1"].to_numpy()
                dif, bas, haut, n = ic_difference_de_facteurs(a, b, ref, rng)
                lignes.append({
                    "camp": camp, "etendue": etiquette, "identite": identite,
                    "condition_a": ca, "condition_b": cb, "famille": famille,
                    "n_items": n,
                    "ratio_a": facteur(a, ref), "ratio_b": facteur(b, ref),
                    "difference_de_ratios": dif, "ic_bas": bas, "ic_haut": haut,
                    "p": p_permutation_signe(a - b, rng),
                })
    return pd.DataFrame(lignes)


def poser_holm_familles(h2b, h1):
    """Holm dans F3 et F4, chacune deux tests : H2b 79 items orientes et H1 gauche,
    identite journaliste, comme la page de plan les definit. Tout le reste est declare
    hors famille et recoit un p brut seulement."""
    h2b = h2b.copy()
    h1 = h1.copy()
    h2b["p_holm"] = np.nan
    h1["p_holm"] = np.nan
    for cle_famille in ("F3, format seul, poids fixes", "F4, poids seuls, format fixe"):
        m2 = ((h2b["famille"] == cle_famille) & (h2b["identite"] == "journaliste")
              & (h2b["perimetre"] == "79 items orientes"))
        m1 = ((h1["famille"] == cle_famille) & (h1["identite"] == "journaliste")
              & (h1["camp"] == "gauche"))
        cles = ([("h2b", i) for i in h2b[m2].index] + [("h1", i) for i in h1[m1].index])
        ps = list(h2b.loc[m2, "p"]) + list(h1.loc[m1, "p"])
        for (table, idx), pa in zip(cles, holm(ps)):
            (h2b if table == "h2b" else h1).at[idx, "p_holm"] = float(pa)
    return h2b, h1


# ---------------------------------------------------------------------------
# 3. La part du format
# ---------------------------------------------------------------------------

def part_du_format(eca, cel, oriente, rng):
    """(X_nogab - X_q4) / (X_base - X_q4), avec la precaution preenregistree."""
    lignes = []
    jeux = []

    for identite in ("journaliste", "adversaire"):
        g = eca[(eca["identite"] == identite)]
        g = g[g["item"].map(lambda i: bool(oriente.get(i, False)))]
        tab = {c: g[g["cle_modele"] == c].set_index("item") for c in CONDITIONS}
        communs = sorted(set.intersection(*[set(t.index) for t in tab.values()]))
        jeux.append(("facteur H2b, 79 items orientes", identite,
                     {c: tab[c].loc[communs, "gap_signe_decrit"].to_numpy() for c in CONDITIONS},
                     tab["q4"].loc[communs, "gap_signe_reel_w1"].to_numpy()))

    ok = cel[~cel["rejet"]]
    for identite in ("journaliste", "adversaire"):
        for camp in ("gauche", "centre", "droite"):
            g = ok[(ok["camp"] == camp) & (ok["identite"] == identite)]
            tab = {c: g[g["cle_modele"] == c].set_index("item") for c in CONDITIONS}
            communs = sorted(set.intersection(*[set(t.index) for t in tab.values()]))
            jeux.append((f"ratio de dispersion H1, camp {camp}", identite,
                         {c: tab[c].loc[communs, "gs_decrit"].to_numpy() for c in CONDITIONS},
                         tab["q4"].loc[communs, "gs_reel_w1"].to_numpy()))

    for quantite, identite, val, ref in jeux:
        x_q4 = facteur(val["q4"], ref)
        x_nog = facteur(val["q4nogab"], ref)
        x_base = facteur(val["q4base"], ref)
        x_hyb = facteur(val["q4hyb"], ref)
        den, den_bas, den_haut, n = ic_difference_de_facteurs(
            val["q4base"], val["q4"], ref, rng)
        num, num_bas, num_haut, _ = ic_difference_de_facteurs(
            val["q4nogab"], val["q4"], ref, rng)
        exclut_zero = np.isfinite(den_bas) and (den_bas > 0 or den_haut < 0)
        part = num / den if exclut_zero and den != 0 else float("nan")
        # IC bootstrap de la part, publie seulement si le denominateur exclut zero
        part_bas = part_haut = float("nan")
        if exclut_zero:
            a, b, c0 = val["q4nogab"], val["q4base"], val["q4"]
            idx = rng.integers(0, n, size=(N_BOOT, n))
            num_t = a[idx].mean(axis=1) - c0[idx].mean(axis=1)
            den_t = b[idx].mean(axis=1) - c0[idx].mean(axis=1)
            t = num_t / den_t
            t = t[np.isfinite(t)]
            if len(t) > 10:
                part_bas = float(np.percentile(t, 2.5))
                part_haut = float(np.percentile(t, 97.5))
        lignes.append({
            "quantite": quantite, "identite": identite, "n_items": n,
            "X_q4_gabarit": x_q4, "X_q4nogab": x_nog, "X_q4base": x_base, "X_q4hyb": x_hyb,
            "numerateur_format": num, "num_ic_bas": num_bas, "num_ic_haut": num_haut,
            "denominateur_socle": den, "den_ic_bas": den_bas, "den_ic_haut": den_haut,
            "denominateur_exclut_zero": bool(exclut_zero),
            "part_du_format": part, "part_ic_bas": part_bas, "part_ic_haut": part_haut,
            "dans_la_bande_020_080": bool(np.isfinite(part) and 0.20 <= part <= 0.80),
        })
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 4. H4, contraste entre conditions
# ---------------------------------------------------------------------------

def contraste_h4(h4, rng):
    lignes = []
    paires = (("q4nogab", "q4", "format seul, poids fixes"),
              ("q4base", "q4nogab", "poids seuls, format fixe"),
              ("q4hyb", "q4nogab", "hybride contre instruit 2507, format fixe"),
              ("q4base", "q4", "socle contre instruit sous gabarit"),
              ("q4hyb", "q4", "hybride contre instruit sous gabarit"))
    for identite in ("journaliste", "adversaire"):
        g = h4[h4["identite"] == identite]
        for ca, cb, quoi in paires:
            ga = g[g["cle_modele"] == ca].set_index(["item", "camp"])
            gb = g[g["cle_modele"] == cb].set_index(["item", "camp"])
            communs = sorted(set(ga.index) & set(gb.index))
            if len(communs) < 3:
                continue
            a = ga.loc[communs, "difference"].to_numpy()
            b = gb.loc[communs, "difference"].to_numpy()
            m, bas, haut, n = ic_moyenne(a - b, rng)
            lignes.append({
                "identite": identite, "condition_a": ca, "condition_b": cb,
                "contraste": quoi, "n_cellules": n,
                "difference_moyenne_a": float(np.mean(a)),
                "difference_moyenne_b": float(np.mean(b)),
                "ecart": m, "ic_bas": bas, "ic_haut": haut,
                "p": p_permutation_signe(a - b, rng),
            })
    if not lignes:
        return pd.DataFrame()
    d = pd.DataFrame(lignes)
    # Holm dans la famille F5 preenregistree : les contrastes de H4 n'y sont pas ; ils
    # sont corriges entre eux, par identite, et declares hors famille preenregistree.
    d["p_holm"] = np.nan
    for identite, g in d.groupby("identite"):
        d.loc[g.index, "p_holm"] = holm(list(g["p"]))
    return d


def main():
    rng = np.random.default_rng(GRAINE)
    cel, eca, h4, oriente, strict = lire()

    h2b = contraste_h2b(eca, oriente, strict, rng)
    h1 = contraste_h1(cel, rng)
    h2b, h1 = poser_holm_familles(h2b, h1)

    part = part_du_format(eca, cel, oriente, rng)
    ch4 = contraste_h4(h4, rng)

    # sensibilite : perimetre strictement commun aux quatre conditions
    ic = {}
    for identite in ("journaliste", "adversaire"):
        ic[(identite, "79 items orientes")] = perimetre_commun(eca, identite, oriente)
        ic[(identite, "items retenus stricts")] = perimetre_commun(eca, identite, strict)
    ok = cel[~cel["rejet"]]
    icc = {}
    for camp in ("gauche", "centre", "droite"):
        for identite in ("journaliste", "adversaire"):
            g = ok[(ok["camp"] == camp) & (ok["identite"] == identite)]
            ens = None
            for cle in CONDITIONS:
                s = set(g[g["cle_modele"] == cle]["item"])
                ens = s if ens is None else (ens & s)
            icc[(camp, identite)] = ens
    h2b_s = contraste_h2b(eca, oriente, strict, rng, ic, "perimetre commun aux 4 conditions")
    h1_s = contraste_h1(cel, rng, icc, "perimetre commun aux 4 conditions")
    sens = pd.concat([
        h2b_s.assign(quantite="facteur H2b").rename(
            columns={"difference_de_facteurs": "difference", "facteur_a": "valeur_a",
                     "facteur_b": "valeur_b"}),
        h1_s.assign(quantite="ratio H1").rename(
            columns={"difference_de_ratios": "difference", "ratio_a": "valeur_a",
                     "ratio_b": "valeur_b"}),
    ], ignore_index=True)

    for df, nom in ((h2b, "r4b-contraste-h2b"), (h1, "r4b-contraste-h1"),
                    (part, "r4b-part-format"), (ch4, "r4b-contraste-h4"),
                    (sens, "r4b-sensibilite-perimetre")):
        chemin = os.path.join(SORTIE, f"{nom}.csv")
        df.to_csv(chemin, index=False)
        print(f"ecrit {chemin}  {len(df)} lignes")

    pd.set_option("display.width", 200, "display.max_columns", 40)
    print("\n--- H2b, 79 items orientes, journaliste ---")
    print(h2b[(h2b["perimetre"] == "79 items orientes")
              & (h2b["identite"] == "journaliste")][
        ["condition_a", "condition_b", "n_items", "facteur_a", "facteur_b",
         "difference_de_facteurs", "ic_bas", "ic_haut", "p", "p_holm"]].to_string(index=False))
    print("\n--- H1, camp gauche, journaliste ---")
    print(h1[(h1["camp"] == "gauche") & (h1["identite"] == "journaliste")][
        ["condition_a", "condition_b", "n_items", "ratio_a", "ratio_b",
         "difference_de_ratios", "ic_bas", "ic_haut", "p", "p_holm"]].to_string(index=False))
    print("\n--- part du format ---")
    print(part[["quantite", "identite", "n_items", "X_q4_gabarit", "X_q4nogab", "X_q4base",
                "X_q4hyb", "numerateur_format", "denominateur_socle",
                "denominateur_exclut_zero", "part_du_format", "part_ic_bas",
                "part_ic_haut"]].to_string(index=False))
    print("\n--- H4, contrastes ---")
    if len(ch4):
        print(ch4.to_string(index=False))


if __name__ == "__main__":
    main()
