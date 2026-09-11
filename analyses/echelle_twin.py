"""
echelle_twin : la loi d'echelle plate, petit contre grand modele, sur Twin-2K-500.

Preenregistrement : resultats/echelle-preenregistrement.md, ecrit le 11 septembre 2026,
avant ce script et avant tout calcul. Idee 6 de resultats/idees-C-folles-2026-09-11.md.

CE QUE CE SCRIPT FAIT. Une seule paire admissible et non suspecte existe a meme invite
et deux tailles (resultats/twin-ab-audit-provenance-2026-09-11.md) : `JSON Persona -
GPT4.1` contre `JSON Persona - GPT4.1-mini`. La mini ne couvre que 1 000 personnes
(pid 1-1000) : tout est mesure sur ce perimetre commun, plancher humain recalcule dessus,
jamais sur les 2 058. Gemini-Flash2.5 est rapporte a part (autre famille, pas de jumeau
GPT4.1 non-mini sur son invite) a partir de resultats/t1-chute-segmentations.csv deja
calcule, sans recalcul.

CE QUI EST IMPORTE TEL QUEL, sans une ligne recopiee :
  t1_commun.charger, .exactitude_codes, .ic_bootstrap_moyenne, .ic_sous_echantillonnage
  t1_mesures.chute                 la chute d'exactitude sous permutation intra segment
  a44_commun.permuter_intra        la permutation employee par ic_sous_echantillonnage

CE QUI EST NOUVEAU ICI : la restriction au perimetre commun de la paire, et la
correlation ordinale intra-segment (troisieme mesure du preenregistrement), absente de
t1_mesures.

Aucun appel de modele. Lecture seule sur data/. Aucun script existant modifie.

Usage : .venv/bin/python analyses/echelle_twin.py [--boot-corr 300]
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np                              # noqa: E402
from scipy.stats import spearmanr                # noqa: E402

import t1_commun as C                            # noqa: E402
import a44_commun as C44                          # noqa: E402
from t1_mesures import chute, N_PERM_IC           # noqa: E402

GRAINE = C.GRAINE
SEG = "S_gra"
GPT41 = "JSON Persona - GPT4.1"
MINI = "JSON Persona - GPT4.1-mini"
GEMINI = "Text Persona - Gemini-Flash2.5"
GEMINI_MINI = "Text Persona - GPT4.1-mini"
N_MIN_CELLULE = 5


def mesures_condition(cd, y1, s, n, rng_seed):
    """Exactitude et chute/plancher pour une condition, sur le perimetre deja restreint.

    Reutilise telles quelles t1_mesures.chute pour la chute et t1_commun.ic_* pour les
    intervalles ; c'est exactement le motif de la boucle Q1-Q2-Q3 de t1_mesures.py.
    """
    exa = C.exactitude_codes(cd, y1)
    exa_moy, exa_bas, exa_haut = C.ic_bootstrap_moyenne(exa, graine=rng_seed)

    rng_p = np.random.default_rng(rng_seed + 1)
    vraie, perms = chute(cd, y1, s, C.N_PERMUTATIONS, rng_p)
    moyp = float(perms.mean())
    chute_abs = vraie - moyp
    chute_rel = chute_abs / vraie if vraie else np.nan

    def f(idx):
        r = np.random.default_rng(rng_seed + 2)
        v = float(np.nanmean(C.exactitude_codes(cd[idx], y1[idx])))
        pp = np.mean([float(np.nanmean(C.exactitude_codes(
            cd[idx][C44.permuter_intra(len(idx), s[idx], r)], y1[idx])))
            for _ in range(N_PERM_IC)])
        return v - pp

    cb, ch, _ = C.ic_sous_echantillonnage(f, n, chute_abs, graine=rng_seed)
    return {
        "exactitude": exa_moy, "exactitude_bas": exa_bas, "exactitude_haut": exa_haut,
        "chute": chute_abs, "chute_bas": cb, "chute_haut": ch,
        "chute_relative": chute_rel,
    }


def correlation_ordinale(cd, y1, s, items_ord):
    """Spearman prediction/humain, par item ordinal et par cellule S_gra (>= 5 des deux
    cotes), moyenne ponderee par les paires valides. Nouveau, cf. preenregistrement point 3.
    """
    cellules = np.unique(s[s >= 0])
    num, den = 0.0, 0
    for j in items_ord:
        vj, yj = cd[:, j], y1[:, j]
        valide = (vj >= 0) & (yj >= 0)
        if not valide.any():
            continue
        for g in cellules:
            m = valide & (s == g)
            k = int(m.sum())
            if k < N_MIN_CELLULE:
                continue
            rho = spearmanr(vj[m], yj[m]).statistic
            if np.isnan(rho):
                continue
            num += rho * k
            den += k
    return num / den if den else np.nan


def correlation_bootstrap(cd, y1, s, items_ord, n, b, graine):
    """IC a 95 % par tirage avec remise, personnes ET items ordinaux, independamment.
    Preenregistrement, section bootstrap."""
    rng = np.random.default_rng(graine)
    reps = np.empty(b)
    n_it = len(items_ord)
    for r in range(b):
        idx_p = rng.integers(0, n, size=n)
        idx_it = items_ord[rng.integers(0, n_it, size=n_it)]
        reps[r] = correlation_ordinale(cd[idx_p], y1[idx_p], s[idx_p], idx_it)
    return float(np.nanpercentile(reps, 2.5)), float(np.nanpercentile(reps, 97.5))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--boot-corr", type=int, default=300,
                     help="repliques du bootstrap personnes x items pour la correlation "
                          "ordinale (1000 au preenregistrement ; reduit ici pour le "
                          "temps de calcul, ecart declare dans le rapport)")
    args = ap.parse_args()
    t0 = time.time()

    paq = C.charger()
    perim = paq["couverture"][MINI]                     # 1 000 personnes, pid 1-1000
    assert set(perim.tolist()) <= set(paq["couverture"][GPT41].tolist()), \
        "le perimetre de la mini doit etre inclus dans celui du grand modele"

    y1 = paq["codes"][C.REF][perim]
    s = paq["seg"][SEG][perim]
    items_ord = np.flatnonzero(paq["est_ordinal"])
    n = len(perim)
    print(f"perimetre commun : {n} personnes, {len(items_ord)} items ordinaux sur "
          f"{len(paq['colonnes'])}", flush=True)

    lignes = []
    for label, nom, graine in [("GPT4.1", GPT41, GRAINE + 100),
                                ("GPT4.1-mini", MINI, GRAINE + 200),
                                ("plancher humain (retest)", C.PLANCHER, GRAINE + 300)]:
        cd = paq["codes"][nom][perim]
        m = mesures_condition(cd, y1, s, n, graine)
        rho = correlation_ordinale(cd, y1, s, items_ord)
        rho_bas, rho_haut = correlation_bootstrap(cd, y1, s, items_ord, n,
                                                   args.boot_corr, graine + 4)
        m.update({"condition": label, "correlation_ordinale": rho,
                  "correlation_bas": rho_bas, "correlation_haut": rho_haut})
        lignes.append(m)
        print(f"  {label} : exactitude {m['exactitude']:.4f}, chute {m['chute']:.4f}, "
              f"correlation {rho:.4f}, {time.time() - t0:.0f}s", flush=True)

    chute_rel_plancher = [l for l in lignes
                          if l["condition"] == "plancher humain (retest)"][0]["chute_relative"]
    for l in lignes:
        l["part_du_plancher_humain"] = (l["chute_relative"] / chute_rel_plancher
                                        if chute_rel_plancher else np.nan)
        l["n"] = n

    C.ecrire(lignes, "echelle-resultats.csv")

    # Gemini, autre famille : rapporte a part, sans recalcul, depuis t1 deja calcule.
    import pandas as pd
    t1 = pd.read_csv(os.path.join(C.SORTIE, "t1-chute-segmentations.csv"))
    g = t1[(t1["condition"].isin([GEMINI, GEMINI_MINI])) & (t1["segmentation"] == SEG)]
    g[["condition", "n", "exactitude_vraie", "chute_relative",
       "part_du_plancher_humain"]].to_csv(
        os.path.join(C.SORTIE, "echelle-gemini-a-part.csv"), index=False)

    print(f"termine, {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
