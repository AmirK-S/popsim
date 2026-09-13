"""
c7_temoins_relecture : les deux temoins construits par la relecture hostile du 13
septembre 2026, REIMPLEMENTES ICI de facon independante.

===========================================================================
POST HOC, NON PREENREGISTRE. Il n'existe aucun preenregistrement anterieur a ces deux
mesures : elles ont ete construites par un relecteur adverse APRES lecture des
resultats, puis redemontrees ici. Le fichier
resultats/c7-temoins-relecture-preenregistrement.md documente donc une analyse deja
faite, et le dit en toutes lettres. Cette mention doit suivre ces chiffres partout,
manuscrit compris.

ETUDE DE RISQUE DE VIE PRIVEE sur deux jeux deja publics (Twin-2K-500 ; Argyle, Busby,
Fulda, Gubler, Rytting & Wingate 2023, Harvard Dataverse doi:10.7910/DVN/JPV20K,
licence CC0). Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identite, le pid ou
l'identifiant ANES d'une personne retrouvee, ni aucune liste d'appariements
individuels : seuls des taux agreges sortent dans resultats/.

DERIVATION INDEPENDANTE. Aucune ligne des scripts du relecteur (temoin_trajectoire.py,
temoin_argyle_fort.py, recalc_argyle.py, restes dans son scratchpad hors depot) n'a ete
lue ni recopiee. Seule la DESCRIPTION de ses deux temoins, dans
resultats/relecture-fond-2026-09-13.md sections D2 et D3, a servi de cahier des
charges. Les ecarts eventuels avec ses chiffres sont rapportes tels quels et ne sont
PAS alignes : deux derivations qui divergent sont une information.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / ecrire                       les tables Twin et l'ecriture des CSV
  a2_commun.bootstrap_personnes                     l'IC 95 % par reechantillonnage de
                                                     personnes
  c7_reidentification.items_communs / rangs_attaque / graine_nom / REF_V4 / REF_V13 / DEMO
                                                     l'attaquant NAIF et ses garde-fous
  c7_attaquant_fort.scores_hors_pli                 l'attaquant FORT A-LLR, parametres
                                                     estimes hors pli, importe sans
                                                     modification
  c7_stanford.rangs_depuis_accord                   le rang a partir d'une matrice de
                                                     score precalculee
  c7_monde_ouvert.marges_deux_regimes / roc_et_taux le protocole de monde ouvert
  c7_argyle.charger / baseline_demographique / controle_avant_interpretation
                                                     le jeu Argyle, sa baseline
                                                     demographique et son controle
  c7_controle_interpretabilite.controle_avant_interpretation
                                                     le controle de fidelite prealable
                                                     sur Twin, appele AVANT toute
                                                     interpretation

CE QUI EST NOUVEAU ICI, et rien d'autre :
  T1  le temoin a NOMBRE D'ITEMS APPARIE : top-1 en fonction de k items tires au hasard
      parmi les 60 communs de Twin, memes 2 058 personnes, meme modele, meme attaque,
      avec le controle d'interpretabilite rejoue A CHAQUE k.
  T2  le temoin de l'ATTAQUANT FORT SUR ARGYLE : A-LLR hors pli et monde ouvert
      (AUC, TPR a FPR fixe) portes sur le jeu de 2023, jamais faits.

LES DEUX TEMOINS TIRENT EN SENS OPPOSES et les deux sont rapportes : T1 affaiblit la
trajectoire d'un facteur ~15, T2 la renforce. Aucun des deux n'est retenu au detriment
de l'autre ; T1, l'affaiblissant, est rapporte en premier.

Aucun appel de modele de langage, aucune depense, aucun reseau. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_temoins_relecture.py
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

import t1_commun as T1                                                   # noqa: E402
from a2_commun import bootstrap_personnes, distance_hamming              # noqa: E402
from c7_reidentification import (                                        # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13, DEMO,
)
from c7_attaquant_fort import scores_hors_pli                            # noqa: E402
from c7_stanford import rangs_depuis_accord                              # noqa: E402
from c7_monde_ouvert import marges_deux_regimes, roc_et_taux             # noqa: E402
import c7_argyle as AR                                                   # noqa: E402
import c7_controle_interpretabilite as CTL                               # noqa: E402

GRAINE = 20260913
N_BOOTSTRAP = 2000

# REDUCTION DECLAREE : l'attaque naive du depot moyenne 20 tirages de depart des ex
# aequo (c7_reidentification.N_TIRAGES_LIENS). La courbe T1 lance 242 attaques ; a
# 20 tirages elle depasserait la demi-heure. Elle tourne donc a 5 tirages, et
# uniquement elle. T2, qui lance 8 attaques, garde les 20 tirages du depot.
N_TIRAGES_COURBE = 5
N_TIRAGES_T2 = 20

CIBLE_TWIN = "JSON Persona - GPT4.1"
K_ITEMS = [12, 20, 30, 40, 60]
N_TIRAGES_ITEMS = 30
N_TIRAGES_CTL_K12 = 5      # k = 12 porte la conclusion : le controle y est rejoue 5 fois


# ---------------------------------------------------------------------------
# Outils communs aux deux temoins
# ---------------------------------------------------------------------------

def ic(indic, cle):
    """IC 95 % bootstrap sur les PERSONNES, graine fixee et derivee du nom de la mesure."""
    return bootstrap_personnes(np.asarray(indic, dtype=float), n_tirages=N_BOOTSTRAP,
                               graine=[GRAINE, graine_nom(cle)])


def ligne(temoin, jeu, candidat, attaque, mesure, valeur, bas=np.nan, haut=np.nan,
          **extra):
    d = {"temoin": temoin, "jeu": jeu, "candidat": candidat, "attaque": attaque,
         "mesure": mesure, "valeur": valeur, "ic_bas": bas, "ic_haut": haut}
    d.update(extra)
    return d


# ---------------------------------------------------------------------------
# TEMOIN 1 (celui qui AFFAIBLIT) : nombre d'items apparie, a l'interieur de Twin
# ---------------------------------------------------------------------------

def temoin_items_apparies(lignes):
    """top-1 en fonction de k items tires au hasard parmi les 60 communs.

    Un seul jeu, une seule equipe, un seul modele, une seule attaque, les memes
    2 058 personnes et le meme pool : la SEULE chose qui change d'un point a l'autre
    de la courbe est le nombre d'items. Tout ce que la courbe montre est donc
    imputable au nombre d'items, et a rien d'autre.

    Pour chaque k < 60 : N_TIRAGES_ITEMS sous ensembles d'items tires sans remise.
    L'indicatrice top-1 de chaque personne est moyennee sur les tirages d'items AVANT
    le bootstrap : l'unite de reechantillonnage reste la personne, jamais le tirage
    d'items. La dispersion ENTRE tirages d'items est rapportee a part (elle ne mesure
    pas la meme chose qu'un IC sur les personnes, et les confondre est precisement le
    defaut D6 que la relecture reproche a l'article).
    """
    print("\n" + "=" * 75, flush=True)
    print("TEMOIN 1 (AFFAIBLISSANT) : nombre d'items apparie, Twin-2K-500", flush=True)
    print("=" * 75, flush=True)

    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool_tous = codes[REF_V4]
    n_pool = pool_tous.shape[0]
    couverts = np.arange(n_pool)          # les 2 058 personnes, jumeaux tous couverts
    print(f"{n_pool} personnes, {len(items)} items communs toujours renseignes", flush=True)

    candidats = {CIBLE_TWIN: codes[CIBLE_TWIN], "Demographics Only - GPT4.1-mini": codes[DEMO]}
    for nom, m in candidats.items():
        cov = int(((m >= 0).any(axis=1)).sum())
        if cov != n_pool:
            raise SystemExit(f"{nom} : {cov} jumeaux couverts sur {n_pool}, "
                             "l'appariement personne a personne n'est plus total.")

    rng_items = np.random.default_rng([GRAINE, 1])
    top1_par_k = {}

    for k in K_ITEMS:
        n_tir = 1 if k == len(items) else N_TIRAGES_ITEMS
        sous = [np.sort(rng_items.choice(items, size=k, replace=False))
                for _ in range(n_tir)] if k < len(items) else [items]
        for nom, mat in candidats.items():
            t1_pers = np.zeros(n_pool)
            t10_pers = np.zeros(n_pool)
            t1_par_tirage = []
            for i, cols in enumerate(sous):
                rng = np.random.default_rng([GRAINE, 2, k, i, graine_nom(nom)])
                _, t1, t10 = rangs_attaque(
                    mat[:, cols], pool_tous[:, cols], couverts, rng,
                    n_tirages=N_TIRAGES_T2 if n_tir == 1 else N_TIRAGES_COURBE)
                t1_pers += t1
                t10_pers += t10
                t1_par_tirage.append(float(t1.mean()))
            t1_pers /= n_tir
            t10_pers /= n_tir
            m1, b1, h1 = ic(t1_pers, f"T1|{k}|{nom}|top1")
            m10, b10, h10 = ic(t10_pers, f"T1|{k}|{nom}|top10")
            tir = np.array(t1_par_tirage)
            top1_par_k[(k, nom)] = (m1, b1, h1)
            commun = dict(k_items=k, n_tirages_items=n_tir, n_attaques=n_pool,
                          n_pool=n_pool)
            lignes.append(ligne(
                "T1 items apparies", "Twin-2K-500", nom, "naif (Hamming)", "top1",
                m1, b1, h1, tirages_min=float(tir.min()), tirages_max=float(tir.max()),
                tirages_ecart_type=float(tir.std(ddof=1)) if n_tir > 1 else np.nan,
                **commun))
            lignes.append(ligne(
                "T1 items apparies", "Twin-2K-500", nom, "naif (Hamming)", "top10",
                m10, b10, h10, **commun))
            print(f"  k={k:2d} {nom:34s} top1={m1*100:7.4f} % [{b1*100:.4f};{h1*100:.4f}]"
                  f"  etendue des {n_tir} tirages d'items : "
                  f"{tir.min()*100:.4f}-{tir.max()*100:.4f} %", flush=True)

        mj, bj, hj = top1_par_k[(k, CIBLE_TWIN)]
        mb, bb, hb = top1_par_k[(k, "Demographics Only - GPT4.1-mini")]
        lignes.append(ligne(
            "T1 items apparies", "Twin-2K-500", CIBLE_TWIN, "naif (Hamming)",
            "rapport_top1_sur_baseline_demo", mj / mb if mb else np.nan,
            k_items=k, n_tirages_items=n_tir, n_pool=n_pool,
            baseline_top1=mb, note="rapport de deux moyennes, sans IC (les deux "
                                   "estimateurs partagent les memes personnes)"))
        print(f"  k={k:2d} rapport jumeau / baseline demographique = {mj/mb:.2f}",
              flush=True)

    # --- le facteur que la relecture chiffre a 15,6 ---
    for nom in candidats:
        m12 = top1_par_k[(12, nom)][0]
        m60 = top1_par_k[(60, nom)][0]
        lignes.append(ligne(
            "T1 items apparies", "Twin-2K-500", nom, "naif (Hamming)",
            "facteur_12_vers_60_items", m60 / m12 if m12 else np.nan,
            top1_k12=m12, top1_k60=m60, n_pool=n_pool))
        print(f"  FACTEUR 12 -> 60 items, {nom} : x{m60/m12:.2f} "
              f"({m12*100:.4f} % -> {m60*100:.4f} %)", flush=True)

    # --- controle d'interpretabilite, rejoue A CHAQUE k, fonction canonique du depot ---
    print("\n--- controle d'interpretabilite (c7_controle_interpretabilite), par k ---",
          flush=True)
    # k = 12 porte la conclusion « la trajectoire survit au temoin » : un seul tirage
    # d'items y serait une preuve faible, puisque l'etendue entre tirages y couvre un
    # facteur 9. Le controle y est donc rejoue sur N_TIRAGES_CTL_K12 tirages
    # independants, et le nombre de tirages qui passent est rapporte.
    rng_ctl = np.random.default_rng([GRAINE, 3])
    for k in K_ITEMS:
        n_ctl = N_TIRAGES_CTL_K12 if k == 12 else 1
        passes = 0
        for i in range(n_ctl):
            cols = np.sort(rng_ctl.choice(items, size=k, replace=False)) \
                if k < len(items) else items
            X = codes[CIBLE_TWIN][:, cols]
            try:
                d = CTL.controle_avant_interpretation(np.arange(n_pool), cols, X,
                                                      f"{CIBLE_TWIN} k={k} t={i}",
                                                      paq=paq)
                passe = True
            except CTL.EchecControleInterpretabilite as exc:
                d = exc.diagnostic
                passe = False
            passes += passe
            lignes.append(ligne(
                "T1 items apparies", "Twin-2K-500", CIBLE_TWIN, "naif (Hamming)",
                "controle_interpretabilite_passe", float(passe),
                d["candidat_ic"][0], d["candidat_ic"][1], k_items=k, n_pool=n_pool,
                tirage_items=i, candidat_top1=d["candidat_top1"],
                baseline_top1=d["baseline_top1"],
                baseline_ic_bas=d["baseline_ic"][0],
                baseline_ic_haut=d["baseline_ic"][1], hasard=d["hasard"],
                note="fonction canonique du depot, baseline recalculee par elle "
                     "sur le meme bassin et les memes items"))
            print(f"  k={k:2d} t={i} {'PASSE' if passe else 'ECHEC'} : candidat "
                  f"{d['candidat_top1']*100:.4f} % [{d['candidat_ic'][0]*100:.4f};"
                  f"{d['candidat_ic'][1]*100:.4f}] vs baseline "
                  f"{d['baseline_top1']*100:.4f} % [{d['baseline_ic'][0]*100:.4f};"
                  f"{d['baseline_ic'][1]*100:.4f}]", flush=True)
        if n_ctl > 1:
            lignes.append(ligne(
                "T1 items apparies", "Twin-2K-500", CIBLE_TWIN, "naif (Hamming)",
                "controle_interpretabilite_part_de_tirages_qui_passent",
                passes / n_ctl, k_items=k, n_pool=n_pool, n_tirages_items=n_ctl))
            print(f"  k={k:2d} : {passes}/{n_ctl} tirages d'items passent le controle",
                  flush=True)

    return top1_par_k


# ---------------------------------------------------------------------------
# TEMOIN 2 (celui qui RENFORCE) : l'attaquant fort applique a Argyle 2023
# ---------------------------------------------------------------------------

def mesures_argyle(nom, score, vrai_idx, n_pool, attaque, lignes, temoin):
    """top-1, top-10 (monde ferme) et AUC / TPR a FPR fixe (monde ouvert) depuis une
    matrice de score deja calculee, quelle que soit l'attaque qui l'a produite."""
    n = score.shape[0]
    rng = np.random.default_rng([GRAINE, 5, graine_nom(nom + "|" + attaque)])
    _, t1, t10 = rangs_depuis_accord(score, vrai_idx, rng, N_TIRAGES_T2)
    m1, b1, h1 = ic(t1, f"T2|{nom}|{attaque}|top1")
    m10, b10, h10 = ic(t10, f"T2|{nom}|{attaque}|top10")
    rng_o = np.random.default_rng([GRAINE, 6, graine_nom(nom + "|" + attaque)])
    mp, correct, mr = marges_deux_regimes(score, vrai_idx, rng_o)
    r = roc_et_taux(mp, correct, mr, n)
    commun = dict(n_attaques=n, n_pool=n_pool, hasard=1.0 / n_pool)
    lignes.append(ligne(temoin, "Argyle 2023", nom, attaque, "top1", m1, b1, h1, **commun))
    lignes.append(ligne(temoin, "Argyle 2023", nom, attaque, "top10", m10, b10, h10,
                        **commun))
    for cle, mes in (("auc", "auc_monde_ouvert"),
                     ("tpr_fpr_0_1pct", "tpr_a_fpr_0_1pct"),
                     ("tpr_fpr_1pct", "tpr_a_fpr_1pct")):
        lignes.append(ligne(temoin, "Argyle 2023", nom, attaque, mes, float(r[cle]),
                            **commun))
    print(f"  {nom:34s} / {attaque:22s} top1={m1*100:7.4f} % "
          f"[{b1*100:.4f};{h1*100:.4f}]  top10={m10*100:6.4f} %  "
          f"AUC={r['auc']:.4f}  TPR@1%={r['tpr_fpr_1pct']*100:.4f} %  "
          f"TPR@0,1%={r['tpr_fpr_0_1pct']*100:.4f} %", flush=True)
    return m1


def temoin_argyle_fort(lignes):
    """L'attaquant fort A-LLR, et la metrique de monde ouvert, portes sur Argyle 2023.

    Les fonctions employees sont exactement celles qui ont produit les chiffres de
    tete sur Twin et sur Park : scores_hors_pli (A-LLR, parametres hors pli),
    marges_deux_regimes et roc_et_taux (monde ouvert). Rien n'est reimplemente ici :
    c'est precisement l'interet du temoin, la metrique du bout DROIT de la trajectoire
    appliquee au bout GAUCHE.
    """
    print("\n" + "=" * 75, flush=True)
    print("TEMOIN 2 (RENFORCANT) : attaquant fort A-LLR sur Argyle 2023", flush=True)
    print("=" * 75, flush=True)
    temoin = "T2 attaquant fort Argyle"

    humains, jumeaux, _ids, noms, demo = AR.charger()
    plein = (humains >= 0).all(axis=1)
    h = humains[plein]
    n = h.shape[0]
    vrai_idx = np.arange(n)
    print(f"{n} personnes completes, {len(noms)} items", flush=True)

    b_demo = AR.baseline_demographique(h, demo)
    cibles = {nom: X[plein] for nom, X in jumeaux.items()}
    cibles["B-demo (demographies seules, ce bassin)"] = b_demo

    print("\n-- monde ferme et monde ouvert, attaque NAIVE (rappel, meme protocole) --",
          flush=True)
    naif = {}
    for nom, x in cibles.items():
        naif[nom] = mesures_argyle(nom, 1.0 - distance_hamming(x, h), vrai_idx, n,
                                   "naif (Hamming)", lignes, temoin)

    print("\n-- monde ferme et monde ouvert, attaquant FORT A-LLR hors pli --", flush=True)
    fort = {}
    for nom, x in cibles.items():
        s = scores_hors_pli(x, h, vrai_idx, f"argyle|llr|{nom}")
        fort[nom] = mesures_argyle(nom, s, vrai_idx, n, "A-LLR (hors pli)", lignes,
                                   temoin)

    for nom in cibles:
        lignes.append(ligne(temoin, "Argyle 2023", nom, "naif -> A-LLR",
                            "gain_relatif_top1_fort_sur_naif",
                            (fort[nom] - naif[nom]) / naif[nom] if naif[nom] else np.nan,
                            n_pool=n, top1_naif=naif[nom], top1_fort=fort[nom]))

    # --- controle d'interpretabilite, avant toute interpretation, les deux attaques ---
    print("\n--- controle d'interpretabilite (regle de c7_argyle, identique a celle de "
          "c7_controle_interpretabilite) ---", flush=True)
    for nom, x in list(jumeaux.items()):
        try:
            d = AR.controle_avant_interpretation(h, demo, x[plein], nom)
            passe = True
        except AR.EchecControleInterpretabilite as exc:
            d = exc.diagnostic
            passe = False
        lignes.append(ligne(
            temoin, "Argyle 2023", nom, "naif (Hamming)",
            "controle_interpretabilite_passe", float(passe),
            d["candidat_ic"][0], d["candidat_ic"][1], n_pool=n,
            candidat_top1=d["candidat_top1"], baseline_top1=d["baseline_top1"],
            baseline_ic_bas=d["baseline_ic"][0], baseline_ic_haut=d["baseline_ic"][1],
            hasard=d["hasard"]))
        print(f"  {nom:34s} naif  {'PASSE' if passe else 'ECHEC'} : "
              f"{d['candidat_top1']*100:.4f} % [{d['candidat_ic'][0]*100:.4f};"
              f"{d['candidat_ic'][1]*100:.4f}] vs baseline "
              f"{d['baseline_top1']*100:.4f} % [{d['baseline_ic'][0]*100:.4f};"
              f"{d['baseline_ic'][1]*100:.4f}]", flush=True)

    # meme regle de decision, mais sous l'attaquant fort : IC du candidat strictement
    # au-dessus de l'IC de la baseline, la baseline etant A-LLR sur le MEME bassin.
    b_nom = "B-demo (demographies seules, ce bassin)"
    s_base = scores_hors_pli(b_demo, h, vrai_idx, f"argyle|llr|{b_nom}")
    rng = np.random.default_rng([GRAINE, 5, graine_nom(b_nom + "|A-LLR (hors pli)")])
    _, t1_base, _ = rangs_depuis_accord(s_base, vrai_idx, rng, N_TIRAGES_T2)
    mb, bb, hb = ic(t1_base, f"T2|{b_nom}|A-LLR (hors pli)|top1")
    for nom, x in list(jumeaux.items()):
        s = scores_hors_pli(x[plein], h, vrai_idx, f"argyle|llr|{nom}")
        rng = np.random.default_rng([GRAINE, 5, graine_nom(nom + "|A-LLR (hors pli)")])
        _, t1c, _ = rangs_depuis_accord(s, vrai_idx, rng, N_TIRAGES_T2)
        mc, bc, hc = ic(t1c, f"T2|{nom}|A-LLR (hors pli)|top1")
        passe = bool(bc > hb)
        lignes.append(ligne(
            temoin, "Argyle 2023", nom, "A-LLR (hors pli)",
            "controle_interpretabilite_passe", float(passe), bc, hc, n_pool=n,
            candidat_top1=mc, baseline_top1=mb, baseline_ic_bas=bb,
            baseline_ic_haut=hb, hasard=1.0 / n,
            note="meme regle de decision, candidat et baseline tous deux sous A-LLR"))
        print(f"  {nom:34s} A-LLR {'PASSE' if passe else 'ECHEC'} : "
              f"{mc*100:.4f} % [{bc*100:.4f};{hc*100:.4f}] vs baseline "
              f"{mb*100:.4f} % [{bb*100:.4f};{hb*100:.4f}]", flush=True)

    return naif, fort


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes = []
    top1_par_k = temoin_items_apparies(lignes)
    naif, fort = temoin_argyle_fort(lignes)

    # --- les deux temoins cote a cote, a 12 items, sans en choisir un ---
    print("\n" + "=" * 75, flush=True)
    print("LES DEUX TEMOINS COTE A COTE, A NOMBRE D'ITEMS APPARIE (12)", flush=True)
    print("=" * 75, flush=True)
    mj = top1_par_k[(12, CIBLE_TWIN)][0]
    mb = top1_par_k[(12, "Demographics Only - GPT4.1-mini")][0]
    nom_arg = "GPT-3 davinci (temp. principale)"
    ab = naif["B-demo (demographies seules, ce bassin)"]
    lignes.append({"temoin": "synthese", "jeu": "Twin-2K-500 vs Argyle 2023",
                   "candidat": f"{CIBLE_TWIN} vs {nom_arg}",
                   "attaque": "naif (Hamming)", "mesure": "rapport_a_la_baseline_12_items",
                   "valeur": np.nan, "ic_bas": np.nan, "ic_haut": np.nan,
                   "k_items": 12, "twin_top1": mj, "twin_baseline_top1": mb,
                   "twin_rapport": mj / mb, "argyle_top1": naif[nom_arg],
                   "argyle_baseline_top1": ab, "argyle_rapport": naif[nom_arg] / ab,
                   "contraste_twin_sur_argyle": mj / naif[nom_arg]})
    print(f"  Twin 2025, 12 items : {mj*100:.4f} % contre baseline {mb*100:.4f} % "
          f"-> rapport {mj/mb:.2f}", flush=True)
    print(f"  Argyle 2023, 12 items : {naif[nom_arg]*100:.4f} % contre baseline "
          f"{ab*100:.4f} % -> rapport {naif[nom_arg]/ab:.2f}", flush=True)
    print(f"  contraste 2023 -> aujourd'hui a items apparies : "
          f"x{mj/naif[nom_arg]:.1f}", flush=True)

    T1.ecrire(pd.DataFrame(lignes), "c7-temoins-relecture.csv")
    print("\nRAPPEL : ces deux temoins sont POST HOC et NON PREENREGISTRES.", flush=True)


if __name__ == "__main__":
    main()
