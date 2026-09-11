"""
c7_defense : peut-on reduire la fuite de reidentification sans detruire l'utilite ?

===========================================================================
PREENREGISTREMENT : resultats/c7-defense-preenregistrement.md, ecrit le 12 septembre
2026, AVANT ce fichier et avant tout calcul de defense.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                        les quinze tables de Twin
  a2_commun.bootstrap_personnes             IC par reechantillonnage de personnes
  c7_reidentification.items_communs/rangs_attaque/graine_nom/REF_V4/REF_V13
                                            l'attaque de reidentification et ses garde-fous
  c7_mecanisme.items_achat                  les 40 indices du bloc Product Preferences - Pricing

CE QUI EST NOUVEAU ICI : les quatre familles de defense (D1 agregation, D2 bruit,
D3 retrait, D4 melange intra-segment), appliquees UNIQUEMENT aux sorties du jumeau
`JSON Persona - GPT4.1` sur les 40 items d'achat (jamais aux humains, jamais aux 20
items d'opinion), et les trois mesures d'utilite (distribution par item, ecarts entre
segments S_gra, correlations entre items) comparees au jumeau non protege et aux humains.

ETHIQUE : aucun pid ni appariement individuel n'est jamais imprime ou ecrit ; uniquement
des taux agreges et des reglages de defense.
Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_defense.py
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

import t1_commun as T1                                        # noqa: E402
from a2_commun import bootstrap_personnes                      # noqa: E402
from c7_reidentification import (                              # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)
from c7_mecanisme import items_achat                            # noqa: E402

GRAINE = 20260911
N_BOOTSTRAP = 2000
CIBLE = "JSON Persona - GPT4.1"
PERTE_RETRAIT_TOTAL = 100.0    # sentinelle : plus aucune donnee publiee sur le bloc


# ---------------------------------------------------------------------------
# Defenses, toutes appliquees aux 40 codes d'achat du jumeau (n_couverts, 40), -1 manquant
# ---------------------------------------------------------------------------

def defense_d1(x40, k):
    """Mode du groupe (partition aleatoire de taille ~k) publie pour tous ses membres."""
    n, n_items = x40.shape
    rng = np.random.default_rng([GRAINE, 101, k])
    ordre = rng.permutation(n)
    groupes = np.array_split(ordre, max(1, n // k))
    xd = x40.copy()
    for g in groupes:
        for j in range(n_items):
            valides = x40[g, j][x40[g, j] >= 0]
            xd[g, j] = np.bincount(valides).argmax() if len(valides) else -1
    return xd


def defense_d2(x40, p):
    """Proportion p des cellules remplacee par un tirage dans la marginale du jumeau."""
    n, n_items = x40.shape
    rng = np.random.default_rng([GRAINE, 102, int(round(p * 100))])
    xd = x40.copy()
    remplace = rng.random((n, n_items)) < p
    for j in range(n_items):
        valides = x40[:, j][x40[:, j] >= 0]
        if not len(valides):
            continue
        m = remplace[:, j]
        if m.any():
            xd[m, j] = rng.choice(valides, size=int(m.sum()))
    return xd


def defense_d3_garder(x40, m):
    """m items gardes au hasard par personne (sur 40), le reste marque manquant."""
    n, n_items = x40.shape
    rng = np.random.default_rng([GRAINE, 103, m])
    bruit = rng.random((n, n_items))
    seuil = np.sort(bruit, axis=1)[:, m - 1:m]
    return np.where(bruit <= seuil, x40, -1)


def defense_d4(x40, seg_c):
    """Permutation des reponses entre personnes du meme segment S_gra, item par item."""
    rng = np.random.default_rng([GRAINE, 104])
    xd = x40.copy()
    for g in np.unique(seg_c):
        if g < 0:
            continue
        membres = np.flatnonzero(seg_c == g)
        if len(membres) < 2:
            continue
        for j in range(x40.shape[1]):
            xd[membres, j] = x40[rng.permutation(membres), j]
    return xd


def toutes_les_defenses(x40, seg_c):
    specs = []
    for k in (2, 5, 10, 25):
        specs.append(("D1_agregation", f"k={k}", defense_d1(x40, k)))
    for p in (0.05, 0.10, 0.25, 0.50):
        specs.append(("D2_bruit", f"p={int(p * 100)}%", defense_d2(x40, p)))
    specs.append(("D3_retrait", "bloc entier supprime", np.full_like(x40, -1)))
    for m in (5, 10, 20):
        specs.append(("D3_retrait", f"{m}/40 items gardes", defense_d3_garder(x40, m)))
    specs.append(("D4_melange", "permutation intra-segment", defense_d4(x40, seg_c)))
    return specs


# ---------------------------------------------------------------------------
# Utilite : trois erreurs en points, jumeau defendu contre une reference
# ---------------------------------------------------------------------------

def _valide(v):
    return np.where(v >= 0, v, np.nan).astype(float)


def erreur_distribution(x_def, x_ref):
    m_def = np.nanmean(_valide(x_def), axis=0)
    m_ref = np.nanmean(_valide(x_ref), axis=0)
    return float(np.nanmean(np.abs(m_def - m_ref))) * 100


def erreur_groupes(x_def, x_ref, seg_def, seg_ref):
    def moyennes_segment(x, seg):
        vals = []
        for g in np.unique(seg):
            if g < 0:
                continue
            m = seg == g
            if m.sum() < 2:
                continue
            vals.append(np.nanmean(_valide(x[m]), axis=0))
        if len(vals) < 2:
            return np.full(x.shape[1], np.nan)
        return np.nanstd(np.stack(vals, axis=0), axis=0)
    e_def = moyennes_segment(x_def, seg_def)
    e_ref = moyennes_segment(x_ref, seg_ref)
    return float(np.nanmean(np.abs(e_def - e_ref))) * 100


def erreur_correlations(x_def, x_ref):
    c_def = pd.DataFrame(_valide(x_def)).corr().values
    c_ref = pd.DataFrame(_valide(x_ref)).corr().values
    iu = np.triu_indices(x_def.shape[1], k=1)
    return float(np.nanmean(np.abs(c_def[iu] - c_ref[iu]))) * 100


def mesurer_utilite(x_def, x_base, x_hum, seg_c, seg_hum):
    if not (x_def >= 0).any():
        return {"erreur_distribution": np.nan, "erreur_groupes": np.nan,
                "erreur_correlations": np.nan, "utilite_globale": PERTE_RETRAIT_TOTAL,
                "erreur_distribution_hum": np.nan, "erreur_groupes_hum": np.nan,
                "erreur_correlations_hum": np.nan, "utilite_globale_hum": PERTE_RETRAIT_TOTAL}
    ed = erreur_distribution(x_def, x_base)
    eg = erreur_groupes(x_def, x_base, seg_c, seg_c)
    ec = erreur_correlations(x_def, x_base)
    edh = erreur_distribution(x_def, x_hum)
    egh = erreur_groupes(x_def, x_hum, seg_c, seg_hum)
    ech = erreur_correlations(x_def, x_hum)
    return {"erreur_distribution": ed, "erreur_groupes": eg, "erreur_correlations": ec,
            "utilite_globale": float(np.mean([ed, eg, ec])),
            "erreur_distribution_hum": edh, "erreur_groupes_hum": egh,
            "erreur_correlations_hum": ech,
            "utilite_globale_hum": float(np.mean([edh, egh, ech]))}


def risque(x_def_60, pool_v4, couverts, suffixe):
    rng = np.random.default_rng([GRAINE, 200, graine_nom(CIBLE), graine_nom(suffixe)])
    _, top1, _ = rangs_attaque(x_def_60, pool_v4, couverts, rng)
    return bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 201, graine_nom(suffixe)])


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]

    items = items_communs(codes, [REF_V4, REF_V13])
    idx_achat_abs = items_achat(paq)
    achat_mask = np.isin(items, idx_achat_abs)
    i_achat = np.flatnonzero(achat_mask)
    i_opinion = np.flatnonzero(~achat_mask)
    print(f"{len(items)} items communs : {len(i_achat)} achat, {len(i_opinion)} opinion",
          flush=True)

    pool_v4 = codes[REF_V4][:, items]
    x_cible = codes[CIBLE][:, items]
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))
    seg_c = seg_gra[couverts]

    x40 = x_cible[couverts][:, i_achat]
    x20 = x_cible[couverts][:, i_opinion]
    hum40 = pool_v4[:, i_achat]

    def assembler(x40_def):
        out = np.empty((len(couverts), len(items)), dtype=x_cible.dtype)
        out[:, i_achat] = x40_def
        out[:, i_opinion] = x20
        return out

    lignes = []

    m, b, h = risque(assembler(x40), pool_v4, couverts, "aucune")
    lignes.append({
        "defense": "aucune", "reglage": "jumeau non protege", "n": len(couverts),
        "top1": m, "top1_bas": b, "top1_haut": h,
        "erreur_distribution": 0.0, "erreur_groupes": 0.0, "erreur_correlations": 0.0,
        "utilite_globale": 0.0,
        "erreur_distribution_hum": erreur_distribution(x40, hum40),
        "erreur_groupes_hum": erreur_groupes(x40, hum40, seg_c, seg_gra),
        "erreur_correlations_hum": erreur_correlations(x40, hum40),
        "utilite_globale_hum": np.nan,
    })
    print(f"aucune defense : top1={m:.4f} [{b:.4f};{h:.4f}]", flush=True)

    for famille, reglage, x40_def in toutes_les_defenses(x40, seg_c):
        nom = f"{famille}:{reglage}"
        m, b, h = risque(assembler(x40_def), pool_v4, couverts, nom)
        u = mesurer_utilite(x40_def, x40, hum40, seg_c, seg_gra)
        lignes.append({"defense": famille, "reglage": reglage, "n": len(couverts),
                        "top1": m, "top1_bas": b, "top1_haut": h, **u})
        print(f"{nom} : top1={m:.4f} [{b:.4f};{h:.4f}] "
              f"utilite_globale={u['utilite_globale']:.2f}", flush=True)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-defense-resultats.csv")

    courbe = df[["defense", "reglage", "top1", "top1_bas", "top1_haut",
                 "utilite_globale"]].copy()
    courbe = courbe.rename(columns={"top1": "risque_top1",
                                     "utilite_globale": "perte_utilite_points"})
    chemin_csv = os.path.join(T1.SORTIE, "c7-defense-courbe.csv")
    courbe.to_csv(chemin_csv, index=False)
    print(f"ecrit {chemin_csv}, {len(courbe)} lignes", flush=True)

    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        fig, ax = plt.subplots(figsize=(7, 5))
        couleurs = {"D1_agregation": "C0", "D2_bruit": "C1", "D3_retrait": "C2",
                    "D4_melange": "C3", "aucune": "k"}
        for fam in courbe["defense"].unique():
            sub = courbe[courbe.defense == fam]
            ax.scatter(sub.risque_top1 * 100, sub.perte_utilite_points,
                       label=fam, color=couleurs.get(fam, "gray"))
        ax.axvline(1.0, color="grey", linestyle=":", linewidth=1)
        ax.set_xlabel("risque : top-1 de reidentification (%)")
        ax.set_ylabel("perte d'utilite (points, vs jumeau non protege)")
        ax.set_title("Compromis risque-utilite, defenses sur le bloc d'achat")
        ax.legend()
        fig.tight_layout()
        chemin_png = os.path.join(T1.SORTIE, "c7-defense-courbe.png")
        fig.savefig(chemin_png, dpi=150)
        print(f"ecrit {chemin_png}", flush=True)
    except ImportError:
        print("matplotlib absent, figure non produite", flush=True)


if __name__ == "__main__":
    main()
