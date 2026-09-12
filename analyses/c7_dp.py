"""
c7_dp : la fuite de reidentification survit-elle a un generateur sous confidentialite
differentielle (DP), le remede que l'ecole dominante opposera a nos defenses empiriques ?

===========================================================================
PREENREGISTREMENT : resultats/c7-dp-preenregistrement.md, ecrit le 12 septembre 2026,
AVANT ce fichier et avant tout calcul de defense DP.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                            les quinze tables de Twin
  c7_reidentification.items_communs/rangs_attaque/graine_nom/REF_V4/REF_V13
                                                l'attaque de reidentification, non modifiee
  a2_commun.bootstrap_personnes                 IC par reechantillonnage de personnes
  a44_commun.permuter_intra                     permutation des personnes intra segment
  a44_mesures.exactitude_codes                  exactitude par personne, codes entiers
  c7_mecanisme.items_achat                      les 40 indices du bloc d'achat
  c7_defense.risque / mesurer_utilite           memes mesures de risque et d'utilite que
                                                `c7-defense-courbe.csv`, pour superposition

CE QUI EST NOUVEAU ICI : un generateur synthetique sous confidentialite differentielle
(marginales par item bruitees, mecanisme de Laplace, PrivBayes degre 0 : aucune structure
de dependance entre items ni conditionnement par segment), sa variation en epsilon, et sa
comparaison a nos quatre defenses empiriques sur le meme graphique risque-utilite.

CE QUE CE MECANISME GARANTIT, PRECISEMENT : epsilon-DP pour la publication du VECTEUR DES
60 HISTOGRAMMES D'ITEM sur les 2 058 humains vague 4, au sens du mecanisme de Laplace
standard (sensibilite L1 = 2 par item sous remplacement d'une personne ; budget total
reparti a parts egales sur les 60 items ; composition SEQUENTIELLE BASIQUE, une borne
large, non la plus fine possible). L'echantillonnage synthetique n'utilise plus ensuite
que ces histogrammes deja bruites : par immunite au post-traitement, le jeu synthetique
publie herite de la meme garantie pour CETTE publication.

CE QUE CE MECANISME NE GARANTIT PAS : (1) aucune structure jointe -- les items sont tires
independamment, donc aucune correlation entre items ni ecart entre segments S_gra ne peut
survivre, quel que soit epsilon (plancher d'architecture, pas un effet de budget) ; (2) le
segment S_gra est traite comme une covariable publique non protegee, comme dans nos
defenses D1/D4 ; (3) aucune composition avec d'autres analyses de ce depot touchant les
memes 2 058 humains n'est comptabilisee, seule la publication de CE script l'est ; (4) ce
n'est ni PrivBayes complet (aucun graphe de dependances appris) ni une implementation
verifiee par une bibliotheque de reference (aucune n'est installee ; ecrite ici a la main
avec numpy, calcul de sensibilite documente dans marginales_bruitees ci-dessous).

ETHIQUE : aucun pid, aucun appariement individuel n'est jamais imprime ou ecrit ;
uniquement des taux agreges. Aucun appel de modele de langage. Lecture seule sur data/.
Usage : .venv/bin/python analyses/c7_dp.py
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

import t1_commun as T1                                          # noqa: E402
from a44_commun import permuter_intra                            # noqa: E402
from a44_mesures import exactitude_codes                          # noqa: E402
from c7_reidentification import (                                # noqa: E402
    items_communs, graine_nom, REF_V4, REF_V13,
)
from c7_mecanisme import items_achat                              # noqa: E402
from c7_defense import risque, mesurer_utilite, CIBLE              # noqa: E402

GRAINE = 20260912
EPSILONS = [0.5, 1.0, 3.0, 10.0, np.inf]
D4_UTILITE = 1.4666529969259292   # c7-defense-courbe.csv, D4_melange (repris, non recalcule)
D4_TOP1 = 0.0012633624878522838


# ---------------------------------------------------------------------------
# Le generateur DP : marginales par item, bruit de Laplace, tirage i.i.d.
# ---------------------------------------------------------------------------

def marginales_bruitees(x, k_items, epsilon_total, rng):
    """Histogramme par item sur x (n, n_items), bruit de Laplace independant.

    Sensibilite L1 = 2 par item (une personne remplacee deplace une unite d'une case a
    une autre). Budget reparti a parts egales sur les n_items items : composition
    sequentielle basique, epsilon_total = n_items * epsilon_item. epsilon_total = inf
    (temoin non prive) renvoie la marginale empirique, sans bruit.
    """
    n_items = x.shape[1]
    eps_item = np.inf if np.isinf(epsilon_total) else epsilon_total / n_items
    probs = []
    for j in range(n_items):
        k = int(k_items[j])
        valides = x[:, j]
        valides = valides[valides >= 0]
        compte = np.bincount(valides, minlength=k).astype(float)[:k]
        if np.isfinite(eps_item):
            compte = compte + rng.laplace(scale=2.0 / eps_item, size=k)
        compte = np.clip(compte, 0, None)
        s = compte.sum()
        probs.append(compte / s if s > 0 else np.full(k, 1.0 / k))
    return probs


def echantillonner(probs, n, rng):
    out = np.empty((n, len(probs)), dtype=np.int16)
    for j, p in enumerate(probs):
        out[:, j] = rng.choice(len(p), size=n, p=p)
    return out


def fidelite_individuelle(x_synth, verite, seg, rng):
    """Exactitude (a44_mesures.exactitude_codes) appariement reel moins appariement
    permute intra-segment (a44_commun.permuter_intra) : la part de la fidelite qui
    depasse le simple partage de segment. Attendue nulle par construction (tirage
    i.i.d. par item, aucun conditionnement individuel ni meme par segment)."""
    perm = permuter_intra(len(verite), seg, rng)
    acc_reel = float(np.nanmean(exactitude_codes(x_synth, verite)))
    acc_perm = float(np.nanmean(exactitude_codes(x_synth, verite[perm])))
    return (acc_reel - acc_perm) * 100, acc_reel * 100, acc_perm * 100


def main():
    print(__doc__.split("=" * 75)[1][:400], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]

    items = items_communs(codes, [REF_V4, REF_V13])
    idx_achat_abs = items_achat(paq)
    i_achat = np.flatnonzero(np.isin(items, idx_achat_abs))
    k_items60 = paq["k_items"][items]

    pool_v4 = codes[REF_V4][:, items]              # (2058, 60), entrainement DP, cible attaque
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))
    assert len(couverts) == pool_v4.shape[0], "CIBLE ne couvre pas toute la population"
    seg_c = seg_gra[couverts]

    twin_x40 = codes[CIBLE][:, items][couverts][:, i_achat]   # jumeau non protege, reference D1-D4
    hum40 = pool_v4[:, i_achat]

    print(f"{len(items)} items communs, {len(i_achat)} d'achat, "
          f"{pool_v4.shape[0]} humains vague 4", flush=True)

    lignes = []
    for eps in EPSILONS:
        nom = f"epsilon={eps}" if np.isfinite(eps) else "epsilon=infini (non prive)"
        rng = np.random.default_rng([GRAINE, graine_nom(nom)])
        probs = marginales_bruitees(pool_v4, k_items60, eps, rng)
        x_synth = echantillonner(probs, pool_v4.shape[0], rng)

        m, b, h = risque(x_synth, pool_v4, couverts, f"dp_{nom}")
        u = mesurer_utilite(x_synth[:, i_achat], twin_x40, hum40, seg_c, seg_gra)
        fid, acc_r, acc_p = fidelite_individuelle(x_synth, pool_v4, seg_gra, rng)

        lignes.append({"epsilon": nom, "n": pool_v4.shape[0],
                        "top1": m, "top1_bas": b, "top1_haut": h,
                        "fidelite_individuelle_points": fid,
                        "exactitude_reelle": acc_r, "exactitude_permutee": acc_p,
                        **u})
        print(f"{nom} : top1={m:.5f} [{b:.5f};{h:.5f}] "
              f"utilite_globale={u['utilite_globale']:.2f} "
              f"fidelite_individuelle={fid:+.3f} pts", flush=True)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-dp-resultats.csv")

    # superposition directe avec c7-defense-courbe.csv : meme forme de colonnes
    courbe_dp = df[["epsilon", "top1", "top1_bas", "top1_haut", "utilite_globale"]].copy()
    courbe_dp.insert(0, "defense", "DP_marginales")
    courbe_dp = courbe_dp.rename(columns={"epsilon": "reglage", "top1": "risque_top1",
                                           "utilite_globale": "perte_utilite_points"})
    courbe_def = pd.read_csv(os.path.join(T1.SORTIE, "c7-defense-courbe.csv"))
    combinee = pd.concat([courbe_def, courbe_dp], ignore_index=True)
    chemin = os.path.join(T1.SORTIE, "c7-dp-courbe-combinee.csv")
    combinee.to_csv(chemin, index=False)
    print(f"ecrit {chemin}, {len(combinee)} lignes (D1-D4 + DP)", flush=True)

    # verdict, critere preenregistre
    proches_d4 = df[np.abs(df.utilite_globale - D4_UTILITE) <= 5]
    if len(proches_d4):
        meilleur = proches_d4.loc[proches_d4.top1.idxmin()]
        print(f"\nau moins un epsilon a moins de 5 pts d'utilite de D4 : {meilleur.epsilon}, "
              f"top1={meilleur.top1:.5f} vs D4={D4_TOP1:.5f} "
              f"-> DP reduit-elle plus la fuite : {bool(meilleur.top1 < D4_TOP1)}", flush=True)
    else:
        ecart_min = float((df.utilite_globale - D4_UTILITE).min())
        print(f"\naucun epsilon a moins de 5 pts d'utilite de D4 (ecart minimal "
              f"{ecart_min:.2f} pts) -> DP dominee par D4 sur cette plage", flush=True)


if __name__ == "__main__":
    main()
