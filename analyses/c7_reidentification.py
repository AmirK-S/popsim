"""
c7_reidentification : le jumeau ne predit pas la personne, la retrouve-t-il ?

===========================================================================
PREENREGISTREMENT : resultats/c7-preenregistrement.md, ecrit le 11 septembre 2026,
AVANT ce fichier et avant tout calcul d'appariement.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Ce script ne calcule,
n'imprime et n'ecrit JAMAIS l'identite ou le pid d'une personne retrouvee, ni aucune liste
d'appariements individuels. Seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger              les quinze tables de Twin, dont le segment S_gra
  a2_commun.distance_hamming     la distance de Hamming normalisee, masquage deja fait
  a2_commun.bootstrap_personnes  l'intervalle de confiance par reechantillonnage de personnes

CE QUI EST NOUVEAU ICI : l'attaque de reidentification elle meme (rang du vrai repondant
parmi 2 058), la restriction aux 60 items toujours renseignes, le controle sur les motifs de
manquants seuls, et le rang a l'interieur du segment S_gra.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_reidentification.py
===========================================================================
"""

import os
import sys
import zlib

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                   # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes  # noqa: E402

GRAINE = 20260911
N_TIRAGES_LIENS = 20     # tirages aleatoires pour departager les ex aequo de rang
N_BOOTSTRAP = 2000

REF_V4 = "humains vague 4"
REF_V13 = "humains vagues 1-3 (retest)"
DEMO = "Demographics Only - GPT4.1-mini"

# Les huit configurations admissibles de twin-ab-audit-provenance-2026-09-11.md.
CONFIGURATIONS = [
    DEMO,
    "JSON Persona - GPT4.1",
    "JSON Persona - GPT4.1-mini",
    "Text Persona (Default Temperature) - GPT4.1-mini",
    "Text Persona (Reasoning) - GPT4.1-mini",
    "Text Persona (Repeating Questions) - GPT4.1-mini",
    "Text Persona - GPT4.1-mini",
    "Text Persona - Gemini-Flash2.5",
]


def items_communs(codes, refs):
    """Les colonnes remplies a 100 pour cent chez toutes les references donnees.

    Choisir ces colonnes elimine par construction toute variation de motif de manquants :
    humains comme jumeaux y sont toujours renseignes, le masque ne peut donc servir
    d'empreinte sur ce sous ensemble (garde fou du preenregistrement, section 1).
    """
    plein = np.ones(codes[refs[0]].shape[1], dtype=bool)
    for r in refs:
        plein &= (codes[r] >= 0).all(axis=0)
    return np.flatnonzero(plein)


def rangs_attaque(vec_test, pool, vrai_idx, rng, n_tirages=N_TIRAGES_LIENS):
    """Rang du vrai repondant pour chaque ligne de vec_test contre TOUT le pool.

    Le pool reste la population entiere (2 058 humains, ou le sous pool d'un segment) :
    seules les personnes attaquees (vec_test) peuvent etre un sous ensemble (ex. les 1 000
    jumeaux de JSON Persona mini), jamais le pool des candidats, conformement au
    preenregistrement section 1. vrai_idx donne, pour chaque ligne de vec_test, la colonne
    du pool qui est la vraie personne. L'ORDRE DES CANDIDATS EST MELANGE avant tout calcul
    de rang (bruit aleatoire i.i.d. sur les scores d'accord), pour qu'aucun raccourci
    d'index ne puisse imiter une identification (garde fou preenregistre). Renvoie, par
    personne : rang moyen sur les tirages de depart (1 = meilleur), et indicatrices
    top-1 / top-10 moyennees sur les memes tirages.
    """
    n = vec_test.shape[0]
    dist = distance_hamming(vec_test, pool)          # (n_test, n_pool), deja masque
    accord = 1.0 - dist
    top1 = np.zeros(n)
    top10 = np.zeros(n)
    rang = np.zeros(n)
    for t in range(n_tirages):
        bruit = rng.random(accord.shape) * 1e-9      # depart aleatoire des ex aequo
        ordre = np.argsort(-(accord + bruit), axis=1, kind="stable")
        place = np.argsort(ordre, axis=1)             # place[i, j] = rang de j pour i
        vrai = place[np.arange(n), vrai_idx] + 1
        top1 += (vrai == 1)
        top10 += (vrai <= 10)
        rang += vrai
    return rang / n_tirages, top1 / n_tirages, top10 / n_tirages


def rang_dans_segment(vec_test, vrai_idx, pool, seg, rng, n_tirages=N_TIRAGES_LIENS):
    """Meme rang, mais le pool de chaque personne est restreint a son propre segment S_gra.

    seg est le segment de CHAQUE MEMBRE DU POOL (population entiere) ; vrai_idx donne la
    position de la vraie personne dans ce pool. Les personnes attaquees sont groupees par
    le segment de leur vraie identite, pour que le calcul reste vectorise.
    """
    n = vec_test.shape[0]
    top1 = np.zeros(n)
    rang = np.zeros(n)
    taille = np.zeros(n, dtype=int)
    seg_vrai = seg[vrai_idx]
    for g in np.unique(seg_vrai):
        if g < 0:
            continue
        membres = np.flatnonzero(seg_vrai == g)       # indices dans vec_test / vrai_idx
        idx_seg = np.flatnonzero(seg == g)             # indices dans le pool entier
        if len(idx_seg) < 2:
            continue
        pos_vraie = np.searchsorted(idx_seg, vrai_idx[membres])
        r, t1, _ = rangs_attaque(vec_test[membres], pool[idx_seg], pos_vraie, rng, n_tirages)
        rang[membres] = r
        top1[membres] = t1
        taille[membres] = len(idx_seg)
    return rang, top1, taille


def graine_nom(nom):
    """Un entier stable pour une chaine, contrairement a hash() qui varie d'un
    interpreteur a l'autre (PYTHONHASHSEED) : la reproductibilite l'exige."""
    return zlib.crc32(nom.encode("utf-8"))


def resume_taux(indic, graine):
    m, bas, haut = bootstrap_personnes(indic, n_tirages=N_BOOTSTRAP, graine=graine)
    return m, bas, haut


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]
    n_total = paq["n"]
    print(f"{n_total} personnes, {codes[REF_V4].shape[1]} items", flush=True)

    items = items_communs(codes, [REF_V4, REF_V13])
    print(f"{len(items)} items communs (toujours renseignes, humains v4 et v1-3)", flush=True)

    pool_v4 = codes[REF_V4][:, items]
    pool_v13 = codes[REF_V13][:, items]

    lignes = []
    for nom in CONFIGURATIONS:
        if nom not in codes:
            print(f"absente : {nom}", flush=True)
            continue
        x = codes[nom][:, items]
        couverts = np.flatnonzero((codes[nom] >= 0).any(axis=1))
        n_c = len(couverts)
        rng = np.random.default_rng([GRAINE, graine_nom(nom)])

        for cible_nom, pool in ((REF_V4, pool_v4), (REF_V13, pool_v13)):
            rang, top1, top10 = rangs_attaque(x[couverts], pool, couverts, rng)
            rang_seg, top1_seg, taille_seg = rang_dans_segment(
                x[couverts], couverts, pool, seg_gra, rng)
            m_t1, b_t1, h_t1 = resume_taux(top1, [GRAINE, 1])
            m_t10, b_t10, h_t10 = resume_taux(top10, [GRAINE, 2])
            m_t1s, b_t1s, h_t1s = resume_taux(top1_seg, [GRAINE, 3])
            lignes.append({
                "configuration": nom, "cible": cible_nom, "n_attaques": n_c,
                "n_pool": pool.shape[0],
                "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
                "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
                "rang_median": float(np.median(rang)),
                "top1_hasard": 1.0 / pool.shape[0],
                "top10_hasard": min(10, pool.shape[0]) / pool.shape[0],
                "top1_segment": m_t1s, "top1_segment_bas": b_t1s, "top1_segment_haut": h_t1s,
                "rang_segment_median": float(np.median(rang_seg)),
                "taille_segment_mediane": float(np.median(taille_seg[taille_seg > 0]))
                if (taille_seg > 0).any() else np.nan,
            })
            print(f"{nom} / {cible_nom} : top1={m_t1:.4f} [{b_t1:.4f};{h_t1:.4f}] "
                  f"top10={m_t10:.4f} rang_med={np.median(rang):.1f} / {pool.shape[0]}",
                  flush=True)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-reidentification.csv")

    # --- controle : attaque sur les motifs de manquants seuls, 108 items, aucune valeur ---
    print("\n--- controle motifs de manquants seuls ---", flush=True)
    presence_v4 = (codes[REF_V4] >= 0).astype(np.int32)
    lignes_ctl = []
    for nom in [DEMO, "Text Persona - GPT4.1-mini", "JSON Persona - GPT4.1-mini"]:
        if nom not in codes:
            continue
        pres_x = (codes[nom] >= 0).astype(np.int32)
        couverts = np.flatnonzero((codes[nom] >= 0).any(axis=1))
        rng = np.random.default_rng([GRAINE, 99, graine_nom(nom)])
        rang, top1, top10 = rangs_attaque(pres_x[couverts], presence_v4, couverts, rng)
        m_t1, b_t1, h_t1 = resume_taux(top1, [GRAINE, 4])

        # hasard conditionnel : moyenne de 1 / taille du groupe de motif identique, sur v4
        cles = [tuple(r.tolist()) for r in presence_v4]
        compte = pd.Series(cles).value_counts()
        tailles = np.array([compte[tuple(r.tolist())] for r in presence_v4[couverts]])
        hasard_cond = float(np.mean(1.0 / tailles))

        lignes_ctl.append({"configuration": nom, "n_attaques": len(couverts),
                           "top1_motifs_seuls": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
                           "top1_hasard_global": 1.0 / n_total,
                           "top1_hasard_conditionnel_taille_groupe": hasard_cond})
        print(f"{nom} : top1 motifs seuls = {m_t1:.4f}, hasard global = {1/n_total:.4f}, "
              f"hasard conditionnel (taille de groupe) = {hasard_cond:.4f}", flush=True)
    T1.ecrire(pd.DataFrame(lignes_ctl), "c7-controle-motifs-manquants.csv")

    # --- verdict, critere preenregistre section 6 ---
    riches = df[(df.configuration != DEMO) & (df.cible == REF_V4)]
    demo_row = df[(df.configuration == DEMO) & (df.cible == REF_V4)]
    demo_top1 = float(demo_row.top1.iloc[0]) if len(demo_row) else np.nan
    if len(riches):
        meilleur = riches.loc[riches.top1.idxmax()]
        on_fonce = bool(meilleur.top1 >= 0.10 and meilleur.top1 >= 2 * demo_top1)
        print(f"\nmeilleur jumeau riche : {meilleur.configuration}, top1={meilleur.top1:.4f} "
              f"vs Demographics Only={demo_top1:.4f} -> on fonce = {on_fonce}", flush=True)


if __name__ == "__main__":
    main()
