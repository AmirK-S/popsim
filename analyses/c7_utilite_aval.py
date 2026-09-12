"""
c7_utilite_aval : que casse D4 dans une analyse concrete de chercheur ?

===========================================================================
PREENREGISTREMENT : resultats/c7-utilite-aval-preenregistrement.md, ecrit le 12
septembre 2026, AVANT ce fichier et avant tout calcul.

QUESTION. c7_defense.py mesure le cout de D4 (melange intra-segment S_gra) en erreurs
abstraites (distribution, ecarts entre groupes, correlations). Un statisticien demandera
une question plus concrete : qu'est-ce que ca casse dans une analyse qu'il ferait
vraiment ? Ce script rejoue TROIS analyses typiques (comparaison de groupes, regression,
ACP) sur humains vague 4, jumeau brut, jumeau D4, et mesure si la CONCLUSION change
(signe, significativite), pas seulement une moyenne d'erreurs.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                          les quinze tables de Twin, seg S_gra
  a2_commun.bootstrap_personnes                IC par reechantillonnage de personnes
  c7_reidentification.items_communs/REF_V4     les 60 items communs, le pool humain
  c7_mecanisme.items_achat                     les 40 indices du bloc d'achat
  c7_defense.defense_d4                        la defense elle-meme (aucune reecriture)

CE QUI EST NOUVEAU ICI : les trois analyses concretes (A comparaison de groupes, B
regression MCO, C ACP), rejouees sur les trois conditions, et les mesures de conclusion
(signe, significativite, comparaison a l'ecart deja present jumeau brut/humains).

ETHIQUE : aucun pid ni appariement individuel n'est jamais imprime ou ecrit ; uniquement
des coefficients agreges sur les 2 058 personnes.
Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_utilite_aval.py
===========================================================================
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                   # noqa: E402
from a2_commun import bootstrap_personnes                 # noqa: E402
from c7_reidentification import items_communs, REF_V4, REF_V13  # noqa: E402
from c7_mecanisme import items_achat                       # noqa: E402
from c7_defense import defense_d4                           # noqa: E402

GRAINE = 20260912
N_BOOTSTRAP = 2000
CIBLE = "JSON Persona - GPT4.1"
SEUIL_T = 1.96


# ---------------------------------------------------------------------------
# A. Comparaison de groupes : ecart de proportion Hommes - Femmes sur l'item 1_Q295
# ---------------------------------------------------------------------------

def analyse_a(x, genre):
    y = x[:, 0].astype(float)
    h, f = y[genre == 1], y[genre == 0]
    diff = float(h.mean() - f.mean())
    rng = np.random.default_rng([GRAINE, 1])

    def tirage(idx):
        g = genre[idx]
        v = y[idx]
        return v[g == 1].mean() - v[g == 0].mean()

    n = len(y)
    reps = np.array([tirage(rng.integers(0, n, n)) for _ in range(N_BOOTSTRAP)])
    bas, haut = np.percentile(reps, [2.5, 97.5])
    return {"diff_H_F": diff, "ic_bas": float(bas), "ic_haut": float(haut),
            "signif": bool(bas > 0 or haut < 0), "signe": int(np.sign(diff))}


# ---------------------------------------------------------------------------
# B. Regression MCO : 5_Q295 ~ genre + age65 + 1_Q295 + 2_Q295
# ---------------------------------------------------------------------------

def analyse_b(x, genre, age65):
    y = x[:, 4].astype(float)
    X = np.column_stack([np.ones(len(y)), genre, age65, x[:, 0], x[:, 1]]).astype(float)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    residus = y - X @ beta
    n, k = X.shape
    sigma2 = float(residus @ residus) / (n - k)
    cov = sigma2 * np.linalg.inv(X.T @ X)
    se = np.sqrt(np.diag(cov))
    t = beta / se
    noms = ["intercept", "genre_H", "age_65+", "achat_1_Q295", "achat_2_Q295"]
    return pd.DataFrame({"variable": noms, "coef": beta, "se": se, "t": t,
                          "signif": np.abs(t) > SEUIL_T, "signe": np.sign(beta).astype(int)})


# ---------------------------------------------------------------------------
# C. ACP sur les 40 items d'achat : part de variance des deux premiers axes
# ---------------------------------------------------------------------------

def analyse_c(x):
    xs = (x - x.mean(axis=0)) / x.std(axis=0, ddof=0).clip(min=1e-9)
    _, s, vt = np.linalg.svd(xs, full_matrices=False)
    var = (s ** 2) / (s ** 2).sum()
    charge1 = vt[0]
    return {"part_pc1": float(var[0]), "part_pc2": float(var[1]),
            "part_pc1_pc2": float(var[0] + var[1]), "charge_pc1": charge1}


def signe_charges(a, b):
    """Fraction des 40 loadings du premier axe qui changent de signe, apres recalage
    d'orientation (l'ACP ne fixe pas le signe global d'un axe)."""
    if np.dot(a, b) < 0:
        b = -b
    return float(np.mean(np.sign(a) != np.sign(b)))


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]
    niveaux = paq["niveaux_seg"]["S_gra"]
    genre_seg = np.array([niveaux[g].split("|")[0] if g >= 0 else "" for g in range(len(niveaux))])
    age_seg = np.array([niveaux[g].split("|")[2] if g >= 0 else "" for g in range(len(niveaux))])

    items = items_communs(codes, [REF_V4, REF_V13])
    idx_achat_abs = items_achat(paq)
    achat_mask = np.isin(items, idx_achat_abs)
    i_achat = np.flatnonzero(achat_mask)

    pool_v4 = codes[REF_V4][:, items]
    x_cible = codes[CIBLE][:, items]
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))
    seg_c = seg_gra[couverts]

    hum40 = pool_v4[:, i_achat]
    x40 = x_cible[couverts][:, i_achat]
    x40_d4 = defense_d4(x40, seg_c)
    assert (x40_d4 >= 0).all() and (hum40 >= 0).all(), "item d'achat manquant : inattendu"

    def genre_age(seg):
        g = (genre_seg[np.clip(seg, 0, None)] == "Male").astype(int)
        a = (age_seg[np.clip(seg, 0, None)] == "65+").astype(int)
        g[seg < 0] = 0
        a[seg < 0] = 0
        return g, a

    genre_hum, age_hum = genre_age(seg_gra)
    genre_tw, age_tw = genre_age(seg_c)

    conditions = [
        ("humains", hum40, genre_hum, age_hum),
        ("jumeau_brut", x40, genre_tw, age_tw),
        ("jumeau_D4", x40_d4, genre_tw, age_tw),
    ]

    lignes_a, lignes_b, lignes_c = [], [], []
    resultats_b = {}
    resultats_c = {}
    for nom, x, genre, age in conditions:
        ra = analyse_a(x, genre)
        lignes_a.append({"condition": nom, **ra})

        rb = analyse_b(x, genre, age)
        rb.insert(0, "condition", nom)
        lignes_b.append(rb)
        resultats_b[nom] = rb

        rc = analyse_c(x)
        lignes_c.append({"condition": nom, "part_pc1": rc["part_pc1"],
                          "part_pc2": rc["part_pc2"], "part_pc1_pc2": rc["part_pc1_pc2"]})
        resultats_c[nom] = rc

        print(f"{nom} : A diff_H_F={ra['diff_H_F']:+.4f} signif={ra['signif']} | "
              f"C part_pc1+2={rc['part_pc1_pc2']:.4f}", flush=True)

    df_a = pd.DataFrame(lignes_a)
    df_b = pd.concat(lignes_b, ignore_index=True)
    df_c = pd.DataFrame(lignes_c)
    T1.ecrire(df_a, "c7-utilite-aval-A-groupes.csv")
    T1.ecrire(df_b, "c7-utilite-aval-B-regression.csv")
    T1.ecrire(df_c, "c7-utilite-aval-C-acp.csv")

    # --- mesures de conclusion : signe/significativite, brut vs humains vs D4 ---
    def compare_b(c1, c2):
        r1, r2 = resultats_b[c1], resultats_b[c2]
        chgt = (r1["signe"].values != r2["signe"].values) | (r1["signif"].values != r2["signif"].values)
        return chgt[1:]  # sans l'intercept

    chgt_brut_hum = compare_b("humains", "jumeau_brut")
    chgt_d4_brut = compare_b("jumeau_brut", "jumeau_D4")
    chgt_d4_hum = compare_b("humains", "jumeau_D4")
    noms_var = resultats_b["humains"]["variable"].values[1:]

    charges_flip_brut = signe_charges(resultats_c["humains"]["charge_pc1"],
                                       resultats_c["jumeau_brut"]["charge_pc1"])
    charges_flip_d4 = signe_charges(resultats_c["jumeau_brut"]["charge_pc1"],
                                     resultats_c["jumeau_D4"]["charge_pc1"])
    charges_flip_d4_hum = signe_charges(resultats_c["humains"]["charge_pc1"],
                                         resultats_c["jumeau_D4"]["charge_pc1"])

    ecart_pc_brut_hum = resultats_c["humains"]["part_pc1_pc2"] - resultats_c["jumeau_brut"]["part_pc1_pc2"]
    ecart_pc_d4_brut = resultats_c["jumeau_brut"]["part_pc1_pc2"] - resultats_c["jumeau_D4"]["part_pc1_pc2"]
    ecart_pc_d4_hum = resultats_c["humains"]["part_pc1_pc2"] - resultats_c["jumeau_D4"]["part_pc1_pc2"]

    resume = {
        "A_signe_diff_hum": lignes_a[0]["signe"], "A_signe_brut": lignes_a[1]["signe"],
        "A_signe_D4": lignes_a[2]["signe"],
        "B_variables": list(noms_var),
        "B_pct_change_brut_vs_hum": float(np.mean(chgt_brut_hum) * 100),
        "B_pct_change_D4_vs_brut": float(np.mean(chgt_d4_brut) * 100),
        "B_pct_change_D4_vs_hum": float(np.mean(chgt_d4_hum) * 100),
        "C_pct_pc1_pc2_hum": resultats_c["humains"]["part_pc1_pc2"] * 100,
        "C_pct_pc1_pc2_brut": resultats_c["jumeau_brut"]["part_pc1_pc2"] * 100,
        "C_pct_pc1_pc2_D4": resultats_c["jumeau_D4"]["part_pc1_pc2"] * 100,
        "C_ecart_points_brut_vs_hum": ecart_pc_brut_hum * 100,
        "C_ecart_points_D4_vs_brut": ecart_pc_d4_brut * 100,
        "C_ecart_points_D4_vs_hum": ecart_pc_d4_hum * 100,
        "C_pct_loadings_pc1_inversees_brut_vs_hum": charges_flip_brut * 100,
        "C_pct_loadings_pc1_inversees_D4_vs_brut": charges_flip_d4 * 100,
        "C_pct_loadings_pc1_inversees_D4_vs_hum": charges_flip_d4_hum * 100,
    }
    print("\nRESUME :", flush=True)
    for k, v in resume.items():
        print(f"  {k} = {v}", flush=True)
    pd.Series(resume).to_json(os.path.join(T1.SORTIE, "c7-utilite-aval-resume.json"),
                               force_ascii=False, indent=2)
    print(f"ecrit {os.path.join(T1.SORTIE, 'c7-utilite-aval-resume.json')}", flush=True)


if __name__ == "__main__":
    main()
