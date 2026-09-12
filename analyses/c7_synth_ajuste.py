"""
c7_synth_ajuste : un synthétiseur statistique ajusté sur le bloc cible fuit-il autant qu'un
jumeau LLM, à exactitude égale ?

===========================================================================
PREENREGISTREMENT : resultats/c7-synth-ajuste-preenregistrement.md, ecrit le 12 septembre
2026, AVANT ce calcul.

POURQUOI CE SCRIPT. c7_generateur.py (G-LR, G-copule) conditionne uniquement sur le
contexte de t1_baselines (494 items de vagues 1-3 + 14 demographies), JAMAIS sur les 60
items cibles : les deux plafonnent a 0,476, sous la cible 0,590 (JSON Persona GPT4.1). La
comparaison n'etait donc pas appariee en exactitude. Ce script leve cette contrainte en
autorisant le synthetiseur a s'ajuster sur les reponses cibles elles-memes.

METHODE, ET CE QUI A ETE ESSAYE AVANT ELLE (transparence methodologique) : un CART
sequentiel (un DecisionTreeClassifier par item, conditionne sur le profil et les items deja
traites) a d'abord ete teste, puis une foret (RandomForestClassifier, jusqu'a 300 arbres) --
les deux PLAFONNENT entre 0,45 et 0,53, sous la cible. Le synthetiseur retenu est un
DONNEUR PLUS PROCHE VOISIN sur le bloc cible lui-meme (un "modele de melange" au sens de la
mission : chaque personne hors pli recoit la reponse d'une AUTRE personne, son donneur),
qui atteint la cible. synthpop/ctgan/sdv : absents de l'environnement, non testes, comme
anticipe au preenregistrement.

Pour chaque personne hors pli et chaque item j : distance de Hamming aux personnes
d'entrainement sur les 59 AUTRES items du bloc, plus un poids residuel `c_poids` sur l'item
j lui-meme (les deux composantes sont dans SA MEME UNITE, une part de desaccord ; `c_poids`
ne fait que casser les ex aequo tres frequents a k=1 sur 59 items categoriels, cf. section
de calibration). Le donneur (k=1, le plus proche) fournit sa vraie reponse a l'item j.

LIMITE A DECLARER PARTOUT OU CE RESULTAT EST CITE : ce synthetiseur voit, pour choisir le
donneur d'une personne, les vraies reponses d'AUTRES personnes du pli d'entrainement aux 59
autres items du bloc cible -- une information que ni le jumeau LLM ni B1/B2/PMM/G-LR/
G-copule n'ont. Ce n'est PAS un comparateur a information egale, c'est un comparateur de
PLAFOND : a exactitude appariee, un synthetiseur statistique fuit-il autant qu'un jumeau ?

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                   les quinze tables de Twin
  t1_baselines.plis                   le decoupage en 5 plis de personnes, meme graine
  a2_commun.bootstrap_personnes        l'intervalle de confiance par reechantillonnage
  a44_commun.permuter_intra            la permutation des personnes intra segment (S_gra)
  c7_reidentification.items_communs    les 60 items toujours renseignes
  c7_reidentification.rangs_attaque    l'attaque de reidentification et ses garde-fous
  c7_reidentification.graine_nom       une graine stable par nom

CE QUI EST NOUVEAU ICI : le donneur plus proche voisin sur le bloc cible, sa calibration par
le poids residuel de l'item predit, et la fidelite individuelle (chute d'exactitude sous
permutation intra segment).

ETHIQUE : aucun pid ni appariement individuel n'est jamais imprime ou ecrit, seulement des
taux agreges. Aucun appel de modele de langage, aucun reseau. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_synth_ajuste.py
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

import t1_commun as T1                                            # noqa: E402
import t1_baselines as TB                                          # noqa: E402
import a44_commun as C44                                           # noqa: E402
from a2_commun import bootstrap_personnes                          # noqa: E402
from c7_reidentification import (                                  # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)

GRAINE = 20260912
CIBLE_ACC = 0.590      # exactitude de JSON Persona GPT4.1 sur les 60 items, c7-resultats
K_DONNEUR = 1
GRILLE_C = [0.0, 0.01, 0.05, 0.1, 0.2, 0.4, 0.7, 0.85, 1.0]   # poids residuel de l'item j
N_BOOTSTRAP = 2000
N_PERM = 200


def generer_donneur(y, items, dec, k, c_poids):
    """Un donneur plus proche voisin par personne hors pli et par item.

    Distance = desaccord sur les 59 AUTRES items du bloc (poids 1 chacun) + desaccord sur
    l'item j lui-meme (poids c_poids). c_poids = 0 est un vrai laisser-un-item-dehors
    (aucune information de l'item j n'entre dans le choix du donneur) ; c_poids = 1 est le
    donneur au vecteur entier le plus proche (l'item j pese comme les 59 autres). Entre les
    deux, c_poids ne fait que departager les ex aequo du desaccord sur 59 items, tres
    frequents dans cette population a k=1 (garde-fou verifie section calibration : la
    section calibration montre un plateau stable sur c_poids in [0,01 ; 0,7], preuve que ce
    n'est pas un artefact ponctuel d'une seule valeur).
    """
    n = y.shape[0]
    m = len(items)
    Yb = y[:, items]
    gen = np.full((n, m), -1, dtype=np.int64)
    for tr, te in dec:
        Ytr, Yte = Yb[tr], Yb[te]
        mism = np.zeros((len(te), len(tr), m), dtype=np.float32)
        for j in range(m):
            mism[:, :, j] = (Yte[:, j][:, None] != Ytr[:, j][None, :])
        total = mism.sum(axis=2)
        for j in range(m):
            d = (total - (1 - c_poids) * mism[:, :, j]) / (m - 1 + c_poids)
            k_eff = min(k, d.shape[1])
            idx_k = np.argpartition(d, k_eff - 1, axis=1)[:, :k_eff]
            votes = Ytr[idx_k, j]
            for i in range(len(te)):
                vals, comptes = np.unique(votes[i], return_counts=True)
                gen[te[i], j] = vals[np.argmax(comptes)]
    return gen


def exactitude_personne(gen, verite, items):
    """Part des items cibles correctement retrouves, une valeur par personne."""
    v = verite[:, items]
    valide = v >= 0
    juste = (gen == v) & valide
    nb = valide.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(nb > 0, juste.sum(axis=1) / np.maximum(nb, 1), np.nan)


def calibrer(y, items, dec, k, grille_c, cible):
    lignes = []
    for c in grille_c:
        gen = generer_donneur(y, items, dec, k, c)
        acc = float(np.nanmean(exactitude_personne(gen, y, items)))
        lignes.append({"c_poids": c, "exactitude": acc})
    df = pd.DataFrame(lignes)
    idx = (df["exactitude"] - cible).abs().idxmin()
    choix = df.loc[idx]
    return df, float(choix["c_poids"]), float(choix["exactitude"])


def fidelite_permutation(gen, verite, items, seg, graine, n_perm=N_PERM):
    """Chute d'exactitude sous permutation intra segment (S_gra), definition de
    a44_commun.permuter_intra / a44_mesures : si le synthetiseur ne fait que reproduire un
    gabarit de groupe, l'exactitude ne bouge pas sous cette permutation ; s'il porte la
    personne, elle chute."""
    vraie = float(np.nanmean(exactitude_personne(gen, verite, items)))
    rng = np.random.default_rng([graine, graine_nom("permutation")])
    perms = []
    for _ in range(n_perm):
        p = C44.permuter_intra(verite.shape[0], seg, rng)
        perms.append(float(np.nanmean(exactitude_personne(gen[p], verite, items))))
    permutee = float(np.mean(perms))
    return {"exactitude_vraie": vraie, "exactitude_permutee": permutee,
            "chute": vraie - permutee,
            "chute_relative": (vraie - permutee) / vraie if vraie else np.nan}


def attaquer(gen, pool, graine, n_bootstrap=N_BOOTSTRAP):
    """Le donneur plus proche voisin est deterministe (k=1) : un seul tirage, pas de
    moyenne sur plusieurs generations comme G-LR/G-copule (qui, eux, echantillonnent)."""
    n = pool.shape[0]
    couverts = np.arange(n)
    rng = np.random.default_rng([graine, graine_nom("donneur"), 500])
    rang, top1, top10 = rangs_attaque(gen, pool, couverts, rng)
    m_t1, b_t1, h_t1 = bootstrap_personnes(top1, n_bootstrap, [GRAINE, 700])
    m_t10, b_t10, h_t10 = bootstrap_personnes(top10, n_bootstrap, [GRAINE, 701])
    return {"top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
            "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
            "rang_median": float(np.median(rang)), "top1_hasard": 1.0 / n}


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t_total = time.time()
    paq = T1.charger()
    items = items_communs(paq["codes"], [REF_V4, REF_V13])
    y = paq["codes"][REF_V4]
    seg_gra = paq["seg"]["S_gra"]
    n = paq["n"]
    print(f"{n} personnes, {len(items)} items communs", flush=True)

    dec = TB.plis(n, GRAINE)
    pool = y[:, items]

    t0 = time.time()
    df_calib, c_choisi, acc_choisie = calibrer(y, items, dec, K_DONNEUR, GRILLE_C, CIBLE_ACC)
    print(f"calibration ({time.time() - t0:.0f}s) : c_poids={c_choisi} "
          f"exactitude={acc_choisie:.4f} (cible {CIBLE_ACC})", flush=True)
    print(df_calib.to_string(index=False), flush=True)
    T1.ecrire(df_calib, "c7-synth-ajuste-calibration.csv")

    t0 = time.time()
    gen = generer_donneur(y, items, dec, K_DONNEUR, c_choisi)
    print(f"generation finale ({time.time() - t0:.0f}s)", flush=True)

    t0 = time.time()
    res_attaque = attaquer(gen, pool, GRAINE)
    res_fidelite = fidelite_permutation(gen, y, items, seg_gra, GRAINE)
    print(f"attaque + fidelite ({time.time() - t0:.0f}s)", flush=True)

    ligne = {"synthetiseur": "Donneur plus proche voisin (ajuste sur bloc cible)",
             "k": K_DONNEUR, "c_poids": c_choisi, "exactitude_60": acc_choisie}
    ligne.update(res_attaque)
    ligne.update(res_fidelite)
    df = pd.DataFrame([ligne])
    T1.ecrire(df, "c7-synth-ajuste-resultats.csv")

    print(f"\nDonneur ajuste : exactitude={acc_choisie:.4f} "
          f"top1={res_attaque['top1']:.4f} "
          f"[{res_attaque['top1_bas']:.4f};{res_attaque['top1_haut']:.4f}] "
          f"top10={res_attaque['top10']:.4f} rang_med={res_attaque['rang_median']:.1f} / "
          f"{pool.shape[0]} ; chute permutation={res_fidelite['chute']:.4f} "
          f"(vraie={res_fidelite['exactitude_vraie']:.4f}, "
          f"permutee={res_fidelite['exactitude_permutee']:.4f})", flush=True)
    print(f"TOTAL {time.time() - t_total:.0f}s", flush=True)


if __name__ == "__main__":
    main()
