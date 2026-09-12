"""
c7_courbe_gen : nos jumeaux regeneres tombent-ils sur la courbe fidelite/fuite ?

===========================================================================
PREENREGISTREMENT : resultats/c7-courbe-gen-preenregistrement.md, ecrit AVANT ce script
et avant tout calcul.

QUESTION : le mystere de « recette » (nos jumeaux fuient 0-0,83 % contre 20,7 % chez
l'autre equipe, resultats/c7-gen-resultats.md) se dissout-il si on place nos 7 jumeaux
regeneres sur la courbe fidelite/fuite deja etablie sur 12 points
(resultats/c7-compromis.csv, rho = 0,958) ? S'ils tombent dans l'intervalle de prediction
de cette courbe, leur faible fuite s'explique entierement par leur faible fidelite.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public. Aucun pid, aucun identifiant
individuel : uniquement des taux agreges.

CE QUI EST REPRIS TEL QUEL, sans une ligne modifiee :
  t1_mesures.chute               la chute d'exactitude sous permutation intra-segment
  c7_gen_analyse.charger_condition, nom_trace, charger_items, construire_idx_mod, CONDITIONS
                                  le chargement des traces c7-gen (memes 60 items, memes
                                  conditions que le preenregistrement c7-gen)
  c7_reidentification.graine_nom la graine stable a partir d'un nom de condition
  t1_commun.charger               les quinze tables de Twin (segment S_gra, plancher humain)

CE QUI EST NOUVEAU ICI : la fidelite individuelle (chute normalisee au plancher humain) de
chacun de nos 7 jumeaux regeneres, jamais calculee avant ce script (c7_gen_analyse ne
calcule que la fuite et l'exactitude brute) ; la regression fuite ~ fidelite sur les 12
points de c7-compromis et son intervalle de prediction a 95 % ; la position de nos 7
points par rapport a cet intervalle.

La fuite (top-1) n'est PAS recalculee : elle est reprise telle quelle de
resultats/c7-gen-reidentification.csv, deja produite par c7_reidentification.rangs_attaque
non modifie (economie de calcul, meme methode, memes graines).

Aucun appel de modele de langage. Lecture seule sur data/ et resultats/. Aucun script
existant modifie.
Usage : .venv/bin/python analyses/c7_courbe_gen.py
===========================================================================
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                              # noqa: E402
from t1_mesures import chute                                        # noqa: E402
from c7_reidentification import graine_nom                          # noqa: E402
from c7_gen_analyse import (                                        # noqa: E402
    CONDITIONS, charger_condition, charger_items, construire_idx_mod,
)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
GRAINE = 20260912
N_PERMUTATIONS = 200
SEG_VERDICT = "S_gra"


def fidelite_condition(vec, vrai_idx, y_v4_full, y_planch_full, seg_full, cle):
    """(fidelite_plancher, exactitude) d'une condition : chute sous permutation
    intra-segment, normalisee a la meme chute mesuree sur le plancher humain
    (memes personnes, memes 60 items, meme segmentation)."""
    y1 = y_v4_full[vrai_idx]
    s = seg_full[vrai_idx]
    y_planch = y_planch_full[vrai_idx]

    rng1 = np.random.default_rng([GRAINE, graine_nom(cle)])
    vraie, perms = chute(vec, y1, s, N_PERMUTATIONS, rng1)
    moyp = float(perms.mean())
    chute_relative = (vraie - moyp) / vraie if vraie else np.nan

    rng2 = np.random.default_rng([GRAINE, graine_nom(cle), 1])
    vraie_p, perms_p = chute(y_planch, y1, s, N_PERMUTATIONS, rng2)
    moyp_p = float(perms_p.mean())
    cr_planch = (vraie_p - moyp_p) / vraie_p if vraie_p else np.nan

    fidelite = (chute_relative / cr_planch
                if cr_planch and abs(cr_planch) > 1e-12 else np.nan)
    return fidelite, float(vraie)


def intervalle_prediction(x_ref, y_ref, x0, alpha=0.05):
    """Regression lineaire y ~ x sur les points de reference ; prediction ponctuelle et
    intervalle de prediction (pas de confiance) a x0, formule standard (Wasserman,
    All of Statistics, section 13.2)."""
    n = len(x_ref)
    pente, ordonnee, r, p, _ = stats.linregress(x_ref, y_ref)
    y_hat_ref = ordonnee + pente * x_ref
    resid = y_ref - y_hat_ref
    s2 = float(np.sum(resid ** 2) / (n - 2))
    xbar = float(np.mean(x_ref))
    sxx = float(np.sum((x_ref - xbar) ** 2))
    t_crit = stats.t.ppf(1 - alpha / 2, df=n - 2)

    y0 = ordonnee + pente * x0
    se_pred = np.sqrt(s2 * (1 + 1.0 / n + (x0 - xbar) ** 2 / sxx))
    bas, haut = y0 - t_crit * se_pred, y0 + t_crit * se_pred
    return {"pente": pente, "ordonnee": ordonnee, "r": r, "p": p,
            "y_predit": y0, "ic_bas": bas, "ic_haut": haut}


def main():
    print(__doc__.split("=" * 75)[1], flush=True)

    paq = T1.charger()
    items = charger_items()
    idx_mod = construire_idx_mod(paq, items)
    idx_codes = [it["code_index"] for it in items]
    n_items = len(items)

    y_v4_full = paq["codes"][T1.REF][:, idx_codes]
    y_planch_full = paq["codes"][T1.PLANCHER][:, idx_codes]
    seg_full = paq["seg"][SEG_VERDICT]

    fuite = pd.read_csv(os.path.join(SORTIE, "c7-gen-reidentification.csv"))

    lignes = []
    for modele, recette, temp in CONDITIONS:
        r = charger_condition(modele, recette, temp, items, idx_mod, n_items)
        if r is None:
            print(f"absent : {modele}/{recette}/t={temp}", flush=True)
            continue
        vec, vrai_idx, _ = r
        cle = f"{modele}|{recette}|{temp}"
        fidelite, exact = fidelite_condition(vec, vrai_idx, y_v4_full, y_planch_full,
                                              seg_full, cle)

        row_f = fuite[(fuite.modele == modele) & (fuite.recette == recette)
                      & (fuite.temperature == temp)]
        assert len(row_f) == 1, f"fuite absente pour {cle}"
        row_f = row_f.iloc[0]
        lignes.append({
            "configuration": f"{modele}/{recette}/t{temp:g}",
            "n_attaques": int(vec.shape[0]),
            "fidelite_plancher": fidelite,
            "exactitude": exact,
            "fuite_top1": float(row_f.top1),
            "fuite_top1_bas": float(row_f.top1_bas),
            "fuite_top1_haut": float(row_f.top1_haut),
        })
        print(f"{cle} : fidelite={fidelite:.4f} exactitude={exact:.4f} "
              f"fuite={row_f.top1:.4f}", flush=True)

    df = pd.DataFrame(lignes)

    # ------------------------------------------------------------------
    # Courbe de reference : les 12 points de c7-compromis.csv (fidelite -> fuite).
    # ------------------------------------------------------------------
    ref = pd.read_csv(os.path.join(SORTIE, "c7-compromis.csv"))
    x_ref = ref.fidelite_plancher.values
    y_ref = ref.fuite_top1.values

    rho_ref, p_ref = stats.spearmanr(x_ref, y_ref)
    print(f"\nRappel, 12 points de c7-compromis : Spearman(fidelite, fuite) = "
          f"{rho_ref:.4f} (p={p_ref:.4f})", flush=True)

    preds, dedans = [], []
    for _, row in df.iterrows():
        if pd.isna(row.fidelite_plancher):
            preds.append({"y_predit": np.nan, "ic_bas": np.nan, "ic_haut": np.nan,
                          "pente": np.nan, "ordonnee": np.nan, "r": np.nan, "p": np.nan})
            dedans.append(np.nan)
            continue
        ip = intervalle_prediction(x_ref, y_ref, row.fidelite_plancher)
        preds.append(ip)
        dedans.append(bool(ip["ic_bas"] <= row.fuite_top1 <= ip["ic_haut"]))

    df["fuite_predite"] = [p["y_predit"] for p in preds]
    df["ic95_bas"] = [p["ic_bas"] for p in preds]
    df["ic95_haut"] = [p["ic_haut"] for p in preds]
    df["residu"] = df.fuite_top1 - df.fuite_predite
    df["dans_intervalle"] = dedans
    df["sous_borne_basse"] = df.fuite_top1 < df.ic95_bas
    df["regression_pente"] = preds[0]["pente"] if preds else np.nan
    df["regression_r"] = preds[0]["r"] if preds else np.nan
    df["regression_p"] = preds[0]["p"] if preds else np.nan
    df["rho_reference_12pts"] = rho_ref

    print("\n" + df[["configuration", "fidelite_plancher", "fuite_top1",
                      "fuite_predite", "ic95_bas", "ic95_haut", "residu",
                      "dans_intervalle"]].to_string(index=False), flush=True)

    n_valides = int(df.dans_intervalle.notna().sum())
    n_dedans = int(df.dans_intervalle.sum(skipna=True))
    n_sous = int(df.sous_borne_basse.sum(skipna=True))
    print(f"\ndans l'intervalle de prediction : {n_dedans}/{n_valides} ; "
          f"nettement sous la borne basse : {n_sous}/{n_valides}", flush=True)
    verdict = ("dissoute" if n_dedans >= 5 else
               "mystere confirme" if n_sous >= 4 else "indetermine")
    print(f"verdict (seuils preenregistres) : {verdict}", flush=True)

    df.to_csv(os.path.join(SORTIE, "c7-courbe-gen.csv"), index=False)
    print(f"\necrit {os.path.join(SORTIE, 'c7-courbe-gen.csv')}", flush=True)


if __name__ == "__main__":
    main()
