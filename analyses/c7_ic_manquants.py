"""
c7_ic_manquants : les intervalles de confiance manquants de la figure 2.

===========================================================================
CONSTAT : la figure 2 (fidelite contre fuite, 13 predicteurs) n'affiche des barres
d'erreur que pour 8 points sur 13, et seulement sur l'axe de la fuite. Manquent :

  - fuite (top-1)  : les quatre temoins statistiques (B0 tirage, B1 argmax, B2 argmax,
    PMM k=10) et le retest humain -- jamais dotes d'un IC dans c7-reidentification.csv,
    qui ne couvre que les 8 configurations LLM/demographie.
  - fidelite (chute sous permutation intra segment, normalisee au plancher humain) :
    AUCUN des 13 points n'a jamais eu d'IC sur cet axe. t1_mesures.py calcule un IC pour
    la "chute" brute (colonnes chute_ic_bas/haut de t1-chute-segmentations.csv, methode
    de sous-echantillonnage pivote), mais jamais pour le rapport normalise au plancher
    humain qui est la quantite tracee en figure 2.

CONVENTION REPRISE A L'IDENTIQUE, sans une ligne recopiee :
  a2_commun.bootstrap_personnes    reechantillonnage par personne avec remise, 2000
                                    tirages -- exactement ce qui a produit
                                    resultats/c7-reidentification.csv et, pour les 4
                                    temoins statistiques et le retest humain,
                                    resultats/c7-compromis-robustesse-points.csv
                                    (analyses/c7_compromis_robustesse.py, section 2-3).
  t1_mesures.chute                 vraie exactitude moins moyenne sous permutation
                                    intra segment -- appelee telle quelle, jamais
                                    modifiee, avec son propre N_PERM_IC (30) qui est deja
                                    la convention interne de ce fichier pour un calcul
                                    d'incertitude (par opposition a N_PERMUTATIONS=200,
                                    reserve au point central).
  c7_reidentification.rangs_attaque / items_communs / graine_nom
  t1_baselines.calculer            les cinq predicteurs statistiques, reproduits a
                                    l'identique (meme GRAINE, KFold deterministe).

CE QUI EST NOUVEAU ICI :
  1. Le vecteur top-1 par personne pour les 4 temoins statistiques et le retest humain
     (deja calcule dans c7_compromis_robustesse.py mais jamais transforme en IC publie) :
     bootstrap_personnes(top1, n_tirages=2000, graine=20260911), IDENTIQUE a la ligne de
     ce script qui imprime deja ces IC sans les ecrire dans un CSV.
  2. Un bootstrap par personne du rapport de fidelite normalise, pour les 13 predicteurs :
     numerateur (chute_relative de la condition) et denominateur (chute_relative du
     plancher humain, sur le meme perimetre) sont reechantillonnes INDEPENDAMMENT, chacun
     sur ses propres personnes -- exactement la convention deja ecrite dans
     c7_compromis_robustesse.rho_bootstrap ("chaque point reechantillonne
     independamment sur ses propres personnes"). Le plancher n'est calcule qu'une fois
     par taille de perimetre (2058 ou 1000), comme le fait deja t1_mesures.py pour le
     point central, et reutilise pour tous les predicteurs qui partagent ce perimetre.

COHERENCE : pour chaque point, le "vraie" recalcule ici sans reechantillonnage (idx =
identite) est verifie contre exactitude_vraie / fuite_top1 deja publies. Un ecart au-dela
de 1e-9 interrompt le script au lieu d'ecrire un resultat -- cf. mission, section 4.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_ic_manquants.py
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

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                        # noqa: E402
import t1_baselines as TB                      # noqa: E402
import t1_mesures as T1M                       # noqa: E402
import c7_reidentification as C7               # noqa: E402
from a2_commun import bootstrap_personnes      # noqa: E402

GRAINE = 20260911
N_BOOTSTRAP = 2000
STATISTIQUES = ["B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]
HUMAIN = "humains vagues 1-3 (retest)"
SEG_VERDICT = T1M.SEG_VERDICT     # "S_gra", declaree au preenregistrement t1 section 7
N_PERM_IC = T1M.N_PERM_IC         # 30, convention interne de t1_mesures.py pour un IC

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

TOL = 1e-9


# ---------------------------------------------------------------------------
# 1. Fuite (top-1) : les 4 temoins statistiques et le retest humain
# ---------------------------------------------------------------------------

def fuite_manquantes(paq):
    codes = paq["codes"]
    n_total = paq["n"]
    items = C7.items_communs(codes, [C7.REF_V4, C7.REF_V13])
    pool_v4 = codes[C7.REF_V4][:, items]

    paq_slim = dict(paq)
    codes_slim = dict(paq["codes"])
    codes_slim[T1.REF] = paq["codes"][T1.REF][:, items]
    paq_slim["codes"] = codes_slim
    t0 = time.time()
    base60 = TB.calculer(paq_slim, avec_pmm=True)
    print(f"  t1_baselines.calculer (60 items) : {time.time() - t0:.0f}s", flush=True)

    points = pd.read_csv(
        os.path.join(SORTIE, "c7-compromis-robustesse-points.csv")).set_index(
        "configuration")

    lignes = []
    for nom in STATISTIQUES:
        x = base60[nom]
        rng = np.random.default_rng([GRAINE, C7.graine_nom(nom)])
        _, top1, _ = C7.rangs_attaque(x, pool_v4, np.arange(n_total), rng)
        lignes.append(_ligne_fuite(nom, top1, points))

    x = codes[C7.REF_V13][:, items]
    couverts = np.flatnonzero((codes[C7.REF_V13] >= 0).any(axis=1))
    rng = np.random.default_rng([GRAINE, C7.graine_nom(HUMAIN)])
    _, top1, _ = C7.rangs_attaque(x[couverts], pool_v4, couverts, rng)
    lignes.append(_ligne_fuite(HUMAIN, top1, points))
    return lignes


def _ligne_fuite(nom, top1, points):
    m, bas, haut = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP, graine=GRAINE)
    ref = float(points.loc[nom, "fuite_top1"])
    ecart = abs(m - ref)
    assert ecart < TOL, (
        f"{nom} : fuite recalculee {m:.10f} != publiee {ref:.10f} "
        f"(ecart {ecart:.2e}) -- convention differente, arret.")
    print(f"  fuite {nom} : {m:.4f} [{bas:.4f};{haut:.4f}] (ecart au publie {ecart:.1e})",
          flush=True)
    return {"predicteur": nom, "axe": "fuite_top1", "point_central": ref,
            "ic_bas": bas, "ic_haut": haut,
            "methode": "bootstrap_personnes (a2_commun), reechantillonnage par "
                       "personne avec remise",
            "n_replications": N_BOOTSTRAP, "graine": GRAINE, "note": ""}


# ---------------------------------------------------------------------------
# 2. Fidelite (part du plancher humain) : les 13 predicteurs
# ---------------------------------------------------------------------------

def _chute_relative_boot(cd, y1, s, rng, n_tirages):
    """Bootstrap par personne (avec remise) de la chute relative (vraie-moyp)/vraie,
    calculee par t1_mesures.chute, non modifiee. Renvoie (vraie_identite, distribution)."""
    n = cd.shape[0]
    vraie0, perms0 = T1M.chute(cd, y1, s, N_PERM_IC, rng)
    dist = np.empty(n_tirages)
    for b in range(n_tirages):
        idx = rng.integers(0, n, size=n)
        vraie, perms = T1M.chute(cd[idx], y1[idx], s[idx], N_PERM_IC, rng)
        moyp = float(perms.mean())
        dist[b] = (vraie - moyp) / vraie if vraie else np.nan
    return vraie0, dist


def fidelite_manquantes(paq):
    codes = paq["codes"]
    y_ref = codes[T1.REF]
    seg_all = paq["seg"][SEG_VERDICT]

    t0 = time.time()
    base108 = TB.calculer(paq, avec_pmm=True)
    for nom, mat in base108.items():
        codes[nom] = mat
        paq["couverture"][nom] = np.arange(paq["n"])
    print(f"  t1_baselines.calculer (108 items) : {time.time() - t0:.0f}s", flush=True)

    per = T1.perimetres(paq)
    conditions = [c for c in codes if c != T1.REF]

    classement = pd.read_csv(os.path.join(SORTIE, "t1-classement.csv"))
    classement = classement[classement.segmentation == SEG_VERDICT].set_index(
        "condition")

    noms_13 = C7.CONFIGURATIONS + STATISTIQUES + [HUMAIN]

    # -- planchers, un par taille de perimetre, meme regle que t1_mesures.py --
    n_uniques = sorted({len(per[nom]) for nom in noms_13})
    planchers_lignes = {
        n_u: next(per[c] for c in conditions if len(per[c]) == n_u)
        for n_u in n_uniques}
    planchers_dist = {}
    for n_u, lignes_p in planchers_lignes.items():
        rng_p = np.random.default_rng([GRAINE, C7.graine_nom(f"plancher_{n_u}")])
        s_p = seg_all[lignes_p]
        cd_p = codes[T1.PLANCHER][lignes_p]
        y1_p = y_ref[lignes_p]
        vraie_p, dist_p = _chute_relative_boot(cd_p, y1_p, s_p, rng_p, N_BOOTSTRAP)
        planchers_dist[n_u] = dist_p
        print(f"  plancher n={n_u} : chute_relative={vraie_p:.4f}, "
              f"bootstrap [{np.nanpercentile(dist_p, 2.5):.4f};"
              f"{np.nanpercentile(dist_p, 97.5):.4f}]", flush=True)

    lignes_out = []
    for nom in noms_13:
        lignes_cond = per[nom]
        s = seg_all[lignes_cond]
        cd = codes[nom][lignes_cond]
        y1 = y_ref[lignes_cond]
        rng = np.random.default_rng([GRAINE, C7.graine_nom(f"{nom}_fidelite")])
        vraie0, dist_cond = _chute_relative_boot(cd, y1, s, rng, N_BOOTSTRAP)

        row = classement.loc[nom]
        vraie_pub = float(row.exactitude_vraie)
        chute_pub = float(row.chute)
        ecart = abs(vraie0 - vraie_pub)
        assert ecart < TOL, (
            f"{nom} : exactitude recalculee {vraie0:.10f} != publiee {vraie_pub:.10f} "
            f"(ecart {ecart:.2e}) -- convention differente, arret.")

        n_u = len(lignes_cond)
        dist_plancher = planchers_dist[n_u]
        ratio_boot = dist_cond / dist_plancher
        bas = float(np.nanpercentile(ratio_boot, 2.5))
        haut = float(np.nanpercentile(ratio_boot, 97.5))
        ref = float(row.part_du_plancher_humain)
        print(f"  fidelite {nom} : {ref:.4f} [{bas:.4f};{haut:.4f}] "
              f"(ecart exactitude au publie {ecart:.1e})", flush=True)
        lignes_out.append({
            "predicteur": nom, "axe": "fidelite_plancher", "point_central": ref,
            "ic_bas": bas, "ic_haut": haut,
            "methode": "bootstrap par personne (numerateur et denominateur "
                       "reechantillonnes independamment, meme convention que "
                       "c7_compromis_robustesse.rho_bootstrap), chute sous "
                       "permutation intra-segment (t1_mesures.chute, "
                       f"N_PERM_IC={N_PERM_IC}) normalisee au plancher humain",
            "n_replications": N_BOOTSTRAP, "graine": GRAINE, "note": ""})
    return lignes_out


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t0 = time.time()
    paq = T1.charger()
    print(f"{paq['n']} personnes, charge en {time.time() - t0:.0f}s", flush=True)

    print("\n--- 1. fuite (top-1), temoins statistiques et retest humain ---", flush=True)
    lignes_fuite = fuite_manquantes(paq)

    print("\n--- 2. fidelite (part du plancher humain), 13 predicteurs ---", flush=True)
    lignes_fidelite = fidelite_manquantes(paq)

    df = pd.DataFrame(lignes_fuite + lignes_fidelite)
    chemin = os.path.join(SORTIE, "c7-ic-manquants.csv")
    df.to_csv(chemin, index=False)
    print(f"\necrit {chemin}, {len(df)} lignes, {time.time() - t0:.0f}s au total",
          flush=True)


if __name__ == "__main__":
    main()
