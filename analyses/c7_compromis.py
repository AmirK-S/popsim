"""
c7_compromis : la fuite de ré-identification est-elle le prix de la fidélité individuelle ?

===========================================================================
PREENREGISTREMENT : resultats/c7-compromis-preenregistrement.md, ecrit le 12 septembre 2026,
AVANT ce fichier et avant tout calcul de correlation ou de regression.

QUESTION : a travers les 8 configurations admissibles de Twin-2K-500 plus 4 reperes
statistiques (12 points), la fidelite individuelle (chute sous permutation intra-segment,
normalisee au plancher humain, `t1-classement.csv`) et la fuite de reidentification
(top-1, `analyses/c7_reidentification.py`) sont elles liees au point qu'on ne puisse pas
avoir l'une sans l'autre ?

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public. Aucune identite ni pid n'est jamais
imprime ou ecrit : uniquement des taux agreges et des rangs de configuration.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                les quinze tables de Twin
  t1_baselines.calculer            les quatre predicteurs statistiques (B0, B1, B2, PMM)
  c7_reidentification.items_communs, rangs_attaque, graine_nom
  a2_commun.bootstrap_personnes    (convention reprise, pas la fonction elle meme, pour le
                                    bootstrap joint sur les 12 points)

CE QUI EST NOUVEAU ICI : le calcul du top-1 de reidentification pour les 4 reperes
statistiques (jamais fait avant ce script), restreint aux 60 items communs pour limiter le
temps de calcul ; la correlation de Spearman entre fidelite et fuite sur les 12 points et
son IC par bootstrap joint des personnes ; la regression fuite ~ exactitude et le signe des
residus par groupe ; le controle style/fidelite via i3b_tau_etoile sur les 8 LLM seuls.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_compromis.py
===========================================================================
"""

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                        # noqa: E402
import t1_baselines as TB                      # noqa: E402
import c7_reidentification as C7               # noqa: E402
from a2_commun import bootstrap_personnes      # noqa: E402,F401

GRAINE = 20260911
N_BOOTSTRAP = 2000

STATISTIQUES = ["B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")


def ecrire(df, nom):
    p = os.path.join(SORTIE, nom)
    df.to_csv(p, index=False)
    print(f"ecrit {p}", flush=True)


def vecteur_dense(couverts, valeurs, n_total):
    """Un vecteur de longueur n_total, NaN hors couverture."""
    out = np.full(n_total, np.nan)
    out[couverts] = valeurs
    return out


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t0 = time.time()
    paq = T1.charger()
    codes = paq["codes"]
    n_total = paq["n"]
    items = C7.items_communs(codes, [C7.REF_V4, C7.REF_V13])
    print(f"{n_total} personnes, {len(items)} items communs, charge en "
          f"{time.time() - t0:.0f}s", flush=True)
    pool_v4 = codes[C7.REF_V4][:, items]

    # ------------------------------------------------------------------
    # 1. Top-1 des 8 configurations LLM admissibles, recalcule ici pour disposer du
    #    vecteur PAR PERSONNE (le csv existant n'a que les taux agreges).
    # ------------------------------------------------------------------
    vecteurs = {}   # nom -> vecteur dense (n_total,), NaN hors couverture
    moyennes = {}

    for nom in C7.CONFIGURATIONS:
        x = codes[nom][:, items]
        couverts = np.flatnonzero((codes[nom] >= 0).any(axis=1))
        rng = np.random.default_rng([GRAINE, C7.graine_nom(nom)])
        _, top1, _ = C7.rangs_attaque(x[couverts], pool_v4, couverts, rng)
        vecteurs[nom] = vecteur_dense(couverts, top1, n_total)
        moyennes[nom] = float(np.nanmean(top1))
        print(f"  LLM {nom} : top1={moyennes[nom]:.4f} (n={len(couverts)})", flush=True)

    # ------------------------------------------------------------------
    # 2. Les 4 reperes statistiques : jamais attaques avant ce script. Leurs codes
    #    viennent de t1_baselines.calculer, restreint aux 60 items communs pour limiter
    #    le calcul (paq passe une copie avec la cible deja decoupee sur `items`, calculer
    #    ne s'appuie que sur cette cible et sur les demographies/contexte, inchanges).
    # ------------------------------------------------------------------
    t0 = time.time()
    paq_slim = dict(paq)
    codes_slim = dict(paq["codes"])
    codes_slim[T1.REF] = paq["codes"][T1.REF][:, items]
    paq_slim["codes"] = codes_slim
    base = TB.calculer(paq_slim, avec_pmm=True)
    print(f"t1_baselines.calculer (60 items) : {time.time() - t0:.0f}s", flush=True)

    for nom in STATISTIQUES:
        x = base[nom]                                  # (n_total, 60), deja aligne
        couverts = np.arange(n_total)                  # les baselines couvrent tout le monde
        rng = np.random.default_rng([GRAINE, C7.graine_nom(nom)])
        _, top1, _ = C7.rangs_attaque(x[couverts], pool_v4, couverts, rng)
        vecteurs[nom] = vecteur_dense(couverts, top1, n_total)
        moyennes[nom] = float(np.nanmean(top1))
        print(f"  stat {nom} : top1={moyennes[nom]:.4f}", flush=True)

    # ------------------------------------------------------------------
    # 3. Fidelite et exactitude : deja calculees, `t1-classement.csv`, segment S_gra.
    # ------------------------------------------------------------------
    classement = pd.read_csv(os.path.join(SORTIE, "t1-classement.csv"))
    classement = classement[classement.segmentation == "S_gra"]
    noms_12 = C7.CONFIGURATIONS + STATISTIQUES
    lignes = []
    for nom in noms_12:
        row = classement[classement.condition == nom]
        assert len(row) == 1, f"{nom} absent de t1-classement.csv (S_gra)"
        row = row.iloc[0]
        groupe = "statistique" if nom in STATISTIQUES else (
            "demographie" if nom == C7.DEMO else "LLM")
        lignes.append({
            "configuration": nom,
            "groupe": groupe,
            "fidelite_plancher": float(row.part_du_plancher_humain),
            "exactitude": float(row.exactitude_vraie),
            "tau_etoile": float(row.i3b_tau_etoile_holm39_2058)
            if pd.notna(row.i3b_tau_etoile_holm39_2058) else np.nan,
            "fuite_top1": moyennes[nom],
        })
    df = pd.DataFrame(lignes)

    # ------------------------------------------------------------------
    # 4. Mesure primaire : Spearman(fidelite, fuite) sur les 12 points, IC par bootstrap
    #    joint des personnes (2000 tirages, meme convention que a2_commun.bootstrap_personnes,
    #    mais applique conjointement aux 12 vecteurs pour que chaque replicat produise un
    #    rho, et non un intervalle par point).
    # ------------------------------------------------------------------
    rho_obs, p_obs = stats.spearmanr(df.fidelite_plancher, df.fuite_top1)
    print(f"\nSpearman(fidelite, fuite) = {rho_obs:.4f} (p={p_obs:.4f}, n=12)", flush=True)

    rng_boot = np.random.default_rng(GRAINE)
    rhos = np.empty(N_BOOTSTRAP)
    for b in range(N_BOOTSTRAP):
        boot_means = np.empty(len(noms_12))
        for i, nom in enumerate(noms_12):
            v = vecteurs[nom]
            v = v[~np.isnan(v)]
            tirage = rng_boot.choice(v, size=len(v), replace=True)
            boot_means[i] = tirage.mean()
        r, _ = stats.spearmanr(df.fidelite_plancher.values, boot_means)
        rhos[b] = r
    rho_bas, rho_haut = np.percentile(rhos, [2.5, 97.5])
    print(f"IC 95% (bootstrap joint, {N_BOOTSTRAP} tirages) : [{rho_bas:.4f} ; "
          f"{rho_haut:.4f}]", flush=True)

    # ------------------------------------------------------------------
    # 5. Regression fuite ~ exactitude, residus par groupe.
    # ------------------------------------------------------------------
    pente, ordonnee, r_lin, p_lin, err = stats.linregress(df.exactitude, df.fuite_top1)
    df["fuite_predite"] = ordonnee + pente * df.exactitude
    df["residu"] = df.fuite_top1 - df.fuite_predite
    print(f"\nRegression fuite ~ exactitude : pente={pente:.4f}, r={r_lin:.4f}, "
          f"p={p_lin:.4f}", flush=True)
    print(df[["configuration", "groupe", "exactitude", "fuite_top1", "residu"]]
          .sort_values("residu").to_string(index=False), flush=True)

    residu_llm = df[df.groupe.isin(["LLM", "demographie"])].residu
    residu_stat = df[df.groupe == "statistique"].residu
    print(f"\nResidus : LLM/demographie min={residu_llm.min():.4f} "
          f"max={residu_llm.max():.4f}, tous positifs = "
          f"{bool((residu_llm > 0).all())}", flush=True)
    print(f"Residus : statistiques min={residu_stat.min():.4f} "
          f"max={residu_stat.max():.4f}, tous negatifs ou nuls = "
          f"{bool((residu_stat <= 0).all())}", flush=True)

    # ------------------------------------------------------------------
    # 6. Controle style vs fidelite : parmi les 8 LLM seuls, rang(residu, tau*).
    # ------------------------------------------------------------------
    huit = df[df.configuration.isin(C7.CONFIGURATIONS)]
    rho_style, p_style = stats.spearmanr(huit.residu, huit.tau_etoile)
    print(f"\nControle style (8 LLM seuls) : Spearman(residu, tau*) = {rho_style:.4f} "
          f"(p={p_style:.4f}, n={len(huit)})", flush=True)

    df["rho_spearman_fidelite_fuite"] = rho_obs
    df["rho_ic_bas"] = rho_bas
    df["rho_ic_haut"] = rho_haut
    df["regression_pente"] = pente
    df["regression_r"] = r_lin
    df["regression_p"] = p_lin
    df["rho_style_8llm"] = rho_style
    df["rho_style_8llm_p"] = p_style
    ecrire(df, "c7-compromis.csv")


if __name__ == "__main__":
    main()
