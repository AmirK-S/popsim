"""
c7_transfert : la fuite de C7 traverse-t-elle les configurations, et les vagues ?

===========================================================================
PREENREGISTREMENT : resultats/c7-transfert-preenregistrement.md, ecrit le 12 septembre
2026, AVANT ce fichier et avant tout calcul.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Ce script ne calcule,
n'imprime et n'ecrit JAMAIS l'identite ou le pid d'une personne, ni aucune liste
d'appariements individuels. Seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL DE analyses/c7_reidentification.py, sans une ligne recopiee :
  rangs_attaque    le rang du vrai repondant contre un bassin, ex aequo departages par
                   tirage aleatoire, candidats melanges avant tout calcul de rang
  graine_nom       un entier stable a partir d'une chaine (reproductible, insensible a
                   PYTHONHASHSEED)
  resume_taux      la moyenne et l'IC 95 pour cent par a2_commun.bootstrap_personnes

analyses/c7_reidentification.py importe lui-meme a2_commun.distance_hamming (la distance
de Hamming normalisee) : c'est donc elle qui fait tout le travail de comparaison ici aussi,
seulement invoquee via rangs_attaque, jamais reecrite.

CE QUI EST NOUVEAU ICI : le VOLET A (transfert entre les 8 configurations admissibles,
matrice de 56 paires dirigees, perimetres inegaux geres explicitement) et le CONTROLE
ANTI-ARTEFACT (un decoy de meme segment demographique S_gra remplace la vraie cible). Le
VOLET B (transfert vers les humains de vagues 1-3 sur des items differents) est verifie
ici puis abandonne : voir `vérifier_volet_b()` et le préenregistrement.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_transfert.py
===========================================================================
"""

import itertools
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                            # noqa: E402
import c7_reidentification as C7                                   # noqa: E402
import a2_commun as A2                                              # noqa: E402
from c7_reidentification import rangs_attaque, graine_nom, resume_taux  # noqa: E402

GRAINE = 20260912
N_BOOTSTRAP = 2000
MIN_ATTAQUES = 5     # en dessous, une paire est jugee non exploitable et ecartee
MIN_ITEMS = 5

CONFIGURATIONS = C7.CONFIGURATIONS
DEMO = C7.DEMO


# ---------------------------------------------------------------------------
# Volet B : verification de faisabilite (aucun calcul d'attaque ensuite)
# ---------------------------------------------------------------------------

def verifier_volet_b(paq):
    """Confirme, sans lancer d'attaque, que le volet B est infaisable ici.

    `paq["colonnes"]` est la nomenclature commune des 108 items de vague 4, sur laquelle
    TOUTES les configurations (humaines ou jumelles) sont codees, y compris
    `humains vagues 1-3 (retest)` qui est un retest de CES MEMES 108 items (memes noms de
    colonnes), pas des items differents. Les items de vague 1-3 reellement non reposes en
    vague 4 sont `paq["demo"]["colonnes_contexte"]` (t1_commun.demographies_brutes) : par
    construction (`contexte = [c for c in w13.columns if c not in reposees ...]`), cet
    ensemble EXCLUT toute colonne de vague 4. L'intersection avec les 108 items que le
    jumeau a jamais renseignes est donc necessairement vide : aucune colonne commune,
    aucune distance de Hamming calculable entre une sortie de jumeau et cette source.
    """
    items_v4 = set(paq["colonnes"])
    items_contexte = set(paq["demo"]["colonnes_contexte"])
    commun = items_v4 & items_contexte
    ctx = paq["demo"]["ctx"]
    renseigne = np.array([[not A2.est_manquant(v) for v in ligne] for ligne in ctx])
    n_personnes_contexte = int((renseigne.any(axis=1)).sum())
    print(f"volet B : {len(items_v4)} items vague 4 (jumeaux), "
          f"{len(items_contexte)} items de contexte vagues 1-3 (humains, non reposes), "
          f"{len(commun)} items communs aux deux -> "
          f"{'FAISABLE' if len(commun) >= MIN_ITEMS else 'INFAISABLE'}", flush=True)
    print(f"volet B : {n_personnes_contexte} personnes avec au moins un item de contexte "
          f"renseigne (a titre indicatif, la question ne se pose plus si 0 item commun)",
          flush=True)
    return len(commun)


# ---------------------------------------------------------------------------
# Volet A : transfert entre les 8 configurations, toutes paires dirigees
# ---------------------------------------------------------------------------

def items_pair(codes, x_nom, y_nom, attaques_idx, pool_idx):
    """Colonnes remplies a 100 pour cent chez les attaques (config X) ET chez tout le
    bassin (config Y). Generalise `items_communs` de c7_reidentification au cas ou les
    deux configurations n'ont pas le meme perimetre de couverture (ex. JSON Persona mini,
    1 000 personnes seulement)."""
    plein_x = (codes[x_nom][attaques_idx] >= 0).all(axis=0)
    plein_y = (codes[y_nom][pool_idx] >= 0).all(axis=0)
    return np.flatnonzero(plein_x & plein_y)


def tirer_decoys(attaques_idx, pool_idx, seg, rng):
    """Pour chaque personne attaquee, un decoy : une AUTRE personne du meme segment
    S_gra, presente dans le bassin. -1 si aucun decoy possible (segment inconnu, ou
    seule la personne elle-meme occupe son segment dans ce bassin)."""
    seg_pool = seg[pool_idx]
    seg_att = seg[attaques_idx]
    decoys = np.full(len(attaques_idx), -1, dtype=np.int64)
    for g in np.unique(seg_att):
        if g < 0:
            continue
        membres = np.flatnonzero(seg_att == g)
        candidats_g = pool_idx[seg_pool == g]
        for m in membres:
            candidats = candidats_g[candidats_g != attaques_idx[m]]
            if len(candidats):
                decoys[m] = rng.choice(candidats)
    return decoys


def attaque_paire(codes, seg, x_nom, y_nom, couverture, rng):
    """Une ligne de la matrice du volet A : attaque reelle X -> Y, plus son controle
    anti-artefact (decoy de meme segment)."""
    cov_x, cov_y = couverture[x_nom], couverture[y_nom]
    attaques_idx = np.intersect1d(cov_x, cov_y)
    pool_idx = cov_y
    if len(attaques_idx) < MIN_ATTAQUES or len(pool_idx) < MIN_ATTAQUES:
        return None
    items = items_pair(codes, x_nom, y_nom, attaques_idx, pool_idx)
    if len(items) < MIN_ITEMS:
        return {"config_x": x_nom, "config_y": y_nom, "n_attaques": len(attaques_idx),
                "n_pool": len(pool_idx), "n_items": len(items), "top1": np.nan}

    vec_test = codes[x_nom][attaques_idx][:, items]
    pool = codes[y_nom][pool_idx][:, items]
    vrai_idx = np.searchsorted(pool_idx, attaques_idx)

    g1 = graine_nom(f"{x_nom}|{y_nom}|reel")
    rang, top1, top10 = rangs_attaque(vec_test, pool, vrai_idx,
                                       np.random.default_rng([GRAINE, g1]))
    m_t1, b_t1, h_t1 = resume_taux(top1, [GRAINE, g1, 1])
    m_t10, b_t10, h_t10 = resume_taux(top10, [GRAINE, g1, 2])

    decoys = tirer_decoys(attaques_idx, pool_idx, seg, rng)
    valide = decoys >= 0
    if valide.sum() >= MIN_ATTAQUES:
        g2 = graine_nom(f"{x_nom}|{y_nom}|controle")
        vrai_idx_ctrl = np.searchsorted(pool_idx, decoys[valide])
        _, top1_c, top10_c = rangs_attaque(vec_test[valide], pool, vrai_idx_ctrl,
                                            np.random.default_rng([GRAINE, g2]))
        m_t1c, b_t1c, h_t1c = resume_taux(top1_c, [GRAINE, g2, 1])
        m_t10c, _, _ = resume_taux(top10_c, [GRAINE, g2, 2])
    else:
        m_t1c = b_t1c = h_t1c = m_t10c = np.nan

    n_pool = len(pool_idx)
    return {
        "config_x": x_nom, "config_y": y_nom,
        "n_attaques": len(attaques_idx), "n_pool": n_pool, "n_items": len(items),
        "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
        "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
        "rang_median": float(np.median(rang)),
        "hasard_top1": 1.0 / n_pool, "hasard_top10": min(10, n_pool) / n_pool,
        "top1_controle": m_t1c, "top1_controle_bas": b_t1c, "top1_controle_haut": h_t1c,
        "top10_controle": m_t10c, "n_controle": int(valide.sum()),
    }


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]
    couverture = paq["couverture"]

    print("\n--- volet B : verification de faisabilite ---", flush=True)
    verifier_volet_b(paq)

    print("\n--- volet A : 56 paires dirigees parmi les 8 configurations ---", flush=True)
    rng_decoys = np.random.default_rng([GRAINE, 7])
    lignes = []
    for x_nom, y_nom in itertools.permutations(CONFIGURATIONS, 2):
        ligne = attaque_paire(codes, seg_gra, x_nom, y_nom, couverture, rng_decoys)
        if ligne is None:
            print(f"ecartee (trop peu de personnes) : {x_nom} -> {y_nom}", flush=True)
            continue
        lignes.append(ligne)
        if np.isfinite(ligne.get("top1", np.nan)):
            print(f"{x_nom} -> {y_nom} : top1={ligne['top1']:.4f} "
                  f"[{ligne['top1_bas']:.4f};{ligne['top1_haut']:.4f}] "
                  f"controle={ligne['top1_controle']:.4f} "
                  f"rang_med={ligne['rang_median']:.1f}/{ligne['n_pool']}", flush=True)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-transfert-voletA.csv")

    # --- resume pour le rapport, aucun identifiant, seulement des agregats ---
    exploitables = df[df.top1.notna()]
    riches = [c for c in CONFIGURATIONS if c != DEMO]
    paires_riches = exploitables[exploitables.config_x.isin(riches)
                                 & exploitables.config_y.isin(riches)]
    paires_demo = exploitables[(exploitables.config_x == DEMO)
                                | (exploitables.config_y == DEMO)]

    print("\n--- resume volet A ---", flush=True)
    if len(paires_riches):
        m = paires_riches.top1.mean()
        mc = paires_riches.top1_controle.mean()
        meilleure = paires_riches.loc[paires_riches.top1.idxmax()]
        pire = paires_riches.loc[paires_riches.top1.idxmin()]
        print(f"top1 moyen, paires riches (n={len(paires_riches)}) : {m:.4f}", flush=True)
        print(f"top1 moyen, controle intra-segment (paires riches) : {mc:.4f}", flush=True)
        print(f"meilleure paire riche : {meilleure.config_x} -> {meilleure.config_y}, "
              f"top1={meilleure.top1:.4f}", flush=True)
        print(f"pire paire riche : {pire.config_x} -> {pire.config_y}, "
              f"top1={pire.top1:.4f}", flush=True)
    if len(paires_demo):
        print(f"top1 moyen, paires avec Demographics Only (n={len(paires_demo)}) : "
              f"{paires_demo.top1.mean():.4f}", flush=True)


if __name__ == "__main__":
    main()
