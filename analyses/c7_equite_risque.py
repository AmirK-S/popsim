"""
c7_equite_risque : la moyenne cache-t-elle une minorite exposee ?

===========================================================================
PREENREGISTREMENT : resultats/c7-equite-risque-preenregistrement.md, ecrit le
13 septembre 2026, AVANT ce fichier et avant tout calcul d'equite. Predictions P1-P5 et
critere de refutation (risque uniforme) y sont fixes.

LA QUESTION. Nous publions une moyenne : 20,7 % de top-1 en monde ferme sur Twin-2K-500.
Une moyenne de 20,7 % est compatible avec deux mondes opposes -- 20,7 % de chance pour
chacun, ou 21 % des personnes identifiees a coup sur et les autres jamais. Le second
monde n'est pas la meme etude.

ETUDE DE RISQUE DE VIE PRIVEE sur des jeux deja publics (Twin-2K-500, archive Park et
al.). Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identite, le pid, une reponse,
un segment nomme d'une personne, ni aucune liste d'appariements individuels. Aucun groupe
de moins de 20 personnes n'est imprime. Seuls des agregats sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / ecrire                 les quinze tables de Twin, l'ecriture CSV
  c7_reidentification.items_communs           les 60 items toujours renseignes
  c7_reidentification.rangs_attaque           L'ATTAQUE elle-meme, inchangee
  c7_reidentification.graine_nom              graine stable par nom
  c7_reidentification.REF_V4/REF_V13/DEMO/GRAINE/N_BOOTSTRAP
  a2_commun.bootstrap_personnes               IC par reechantillonnage de personnes
  c7_defense.defense_d4                       le melange intra-segment, memes graines
  c7_mecanisme.items_achat                    les 40 indices du bloc d'achat
  c7_stanford.charger_domaine / coder_categoriel_commun / accord_categoriel /
             rangs_depuis_accord / VAGUE1     la replication sur Park et al.
  c7_controle_interpretabilite.controle_avant_interpretation
                                              le controle de fidelite prealable, appele
                                              AVANT toute lecture d'equite

CE QUI EST NOUVEAU ICI, et rien d'autre :
  risque_a_bassin_constant   transformation deterministe du rang en probabilite de top-1
                             a taille de bassin FIXEE (le piege du depot : le top-1 depend
                             mecaniquement de la taille du bassin -- 2,13 % a 2 058, 13,29 %
                             a 120 pour la meme baseline. Comparer deux sous-groupes de
                             tailles differentes par leur top-1 intra-groupe mesurerait la
                             taille du groupe et non l'exposition.)
  gini / part_decile         les mesures de concentration
  bootstrap_statistique      IC ou la statistique d'inegalite est REESTIMEE dans chaque
                             tirage, pas un IC sur une statistique deja agregee
  les corrélats d'exposition et la decomposition de l'effet de D4 sur l'inegalite.

Aucun appel de modele de langage, aucune depense, aucun reseau, aucun arriere-plan.
Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_equite_risque.py
===========================================================================
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from scipy.special import gammaln
from scipy.stats import spearmanr

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                            # noqa: E402
from a2_commun import bootstrap_personnes                          # noqa: E402
from c7_reidentification import (                                  # noqa: E402
    items_communs, rangs_attaque, graine_nom,
    REF_V4, REF_V13, DEMO, GRAINE, N_BOOTSTRAP,
)
from c7_defense import defense_d4                                  # noqa: E402
from c7_mecanisme import items_achat                               # noqa: E402
import c7_stanford as CS                                           # noqa: E402
from c7_controle_interpretabilite import (                         # noqa: E402
    controle_avant_interpretation,
)

CIBLE = "JSON Persona - GPT4.1"     # le jumeau des chiffres publies
B_PRINCIPAL = 100                    # taille de bassin fixee, preenregistree
B_CONTROLE = 1000                    # sensibilite, preenregistree
N_BOOT_STAT = 1000                   # tirages pour les IC de Gini / part de decile
TAILLE_MIN_GROUPE = 20               # aucun groupe plus petit n'est imprime (garde-fou)


# ---------------------------------------------------------------------------
# 1. Le risque individuel a bassin constant
# ---------------------------------------------------------------------------

def risque_a_bassin_constant(rang, n_pool, b):
    """Probabilite que la vraie personne soit premiere dans un bassin de taille b.

    rang : le rang R_i rendu par c7_reidentification.rangs_attaque contre le bassin
    COMPLET de n_pool candidats (1 = identifiee). On pose c_i = R_i - 1, le nombre
    d'imposteurs qui la battent, et M = n_pool - 1 imposteurs au total. Le bassin de
    taille b est tire au hasard parmi eux, la vraie personne incluse : elle est premiere
    si et seulement si aucun des b-1 imposteurs tires ne la bat, soit

        p_i(b) = C(M - c_i, b - 1) / C(M, b - 1).

    POURQUOI CETTE QUANTITE ET PAS LE TOP-1. Le top-1 est binaire par personne : il n'a
    pas de distribution, donc pas de deciles. Et il depend mecaniquement de la taille du
    bassin, ce qui rend toute comparaison entre sous-groupes de tailles differentes une
    mesure de la taille du groupe. p_i(b) est une transformation DETERMINISTE ET MONOTONE
    du rang -- pas une nouvelle attaque -- qui est continue, vaut exactement le top-1
    observe quand b = n_pool, et est definie au MEME b pour tout le monde.

    c_i est reel (rang moyen sur les tirages de departage d'ex aequo) : les coefficients
    binomiaux passent donc par gammaln, en log, ce qui evite aussi tout debordement a
    n_pool = 2 058.
    """
    c = np.asarray(rang, dtype=float) - 1.0
    m = float(n_pool - 1)
    k = float(b - 1)
    if k <= 0:
        return np.ones_like(c)
    reste = m - c - k + 1.0                    # argument de gammaln, > 0 requis
    log_p = (gammaln(m - c + 1.0) - gammaln(np.maximum(reste, 1e-300))
             - gammaln(m + 1.0) + gammaln(m - k + 1.0))
    p = np.where(reste > 0, np.exp(np.clip(log_p, -700, 0.0)), 0.0)
    return np.clip(p, 0.0, 1.0)


# ---------------------------------------------------------------------------
# 2. Concentration
# ---------------------------------------------------------------------------

def gini(v):
    """Gini des risques individuels. 0 = tout le monde egalement expose, 1 = une seule
    personne porte tout le risque. Sur des valeurs positives, formule par tri."""
    x = np.sort(np.asarray(v, dtype=float))
    n = len(x)
    s = x.sum()
    if n == 0 or s <= 0:
        return np.nan
    i = np.arange(1, n + 1)
    return float((2.0 * (i * x).sum()) / (n * s) - (n + 1.0) / n)


def part_decile(v, q=0.10):
    """Part du risque TOTAL detenue par la fraction q la plus exposee.

    Le denominateur est la somme des risques individuels, c'est-a-dire le nombre attendu
    d'identifications. Sous uniformite stricte la reponse est q (10 %)."""
    x = np.asarray(v, dtype=float)
    n = len(x)
    if n == 0 or x.sum() <= 0:
        return np.nan
    k = max(1, int(round(q * n)))
    return float(np.sort(x)[::-1][:k].sum() / x.sum())


def deciles(v):
    """Risque moyen de chaque decile, du moins expose (D1) au plus expose (D10)."""
    x = np.sort(np.asarray(v, dtype=float))
    return [float(g.mean()) for g in np.array_split(x, 10)]


def bootstrap_statistique(valeurs, fonction, graine, n_tirages=N_BOOT_STAT):
    """IC 95 % ou la statistique d'inegalite est REESTIMEE dans chaque tirage.

    Reechantillonner les personnes puis recalculer le Gini n'est pas la meme chose que
    poser un IC autour d'un Gini deja calcule : la seconde operation n'a pas de sens.
    L'unite de reechantillonnage reste la personne, comme partout dans ce depot.
    """
    x = np.asarray(valeurs, dtype=float)
    rng = np.random.default_rng(graine)
    n = len(x)
    t = np.array([fonction(x[rng.integers(0, n, n)]) for _ in range(n_tirages)])
    t = t[~np.isnan(t)]
    if not len(t):
        return fonction(x), np.nan, np.nan
    return fonction(x), float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5))


def bootstrap_couple(a, b, fonction, graine, n_tirages=N_BOOT_STAT):
    """Meme chose pour une statistique de DEUX vecteurs alignes sur les memes personnes
    (part de succes concentree, correlation) : les deux sont reechantillonnes ensemble."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    rng = np.random.default_rng(graine)
    n = len(a)
    t = []
    for _ in range(n_tirages):
        j = rng.integers(0, n, n)
        t.append(fonction(a[j], b[j]))
    t = np.array(t, dtype=float)
    t = t[~np.isnan(t)]
    if not len(t):
        return fonction(a, b), np.nan, np.nan
    return fonction(a, b), float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5))


def part_succes_du_decile(risque, succes, q=0.10):
    """Part des top-1 REELLEMENT reussis (sur une AUTRE cible) detenue par la fraction q
    la plus exposee selon `risque` (estime, lui, sur la premiere cible).

    C'est la validation non circulaire du preenregistrement P3 : le classement vient d'un
    appariement, le succes compte est mesure contre une cible differente. Sous uniformite,
    la reponse est q.
    """
    r = np.asarray(risque, dtype=float)
    s = np.asarray(succes, dtype=float)
    if s.sum() <= 0:
        return np.nan
    k = max(1, int(round(q * len(r))))
    haut = np.argsort(-r)[:k]
    return float(s[haut].sum() / s.sum())


# ---------------------------------------------------------------------------
# 3. Corrélats observables (aucune donnee individuelle ne sort d'ici)
# ---------------------------------------------------------------------------

def atypicite(codes_humains):
    """Fraction des items ou la reponse de la personne DIFFERE du mode de la population.

    Caracteristique de la personne (ses propres reponses), pas du jumeau. Les items sont
    les 60 toujours renseignes : aucun manquant a gerer.
    """
    x = np.asarray(codes_humains)
    modes = np.array([np.bincount(col[col >= 0]).argmax() if (col >= 0).any() else -1
                      for col in x.T])
    return (x != modes[None, :]).mean(axis=1)


def coherence_test_retest(v4, v13):
    """Accord entre les reponses de la personne en vague 4 et en vagues 1-3, item par
    item : sa stabilite a elle. Une personne incoherente est-elle plus dure a retrouver ?"""
    return (np.asarray(v4) == np.asarray(v13)).mean(axis=1)


def moyennes_par_niveau(risque, seg, etiquette_axe, taille_min=TAILLE_MIN_GROUPE):
    """Risque moyen par niveau d'un axe demographique, a bassin CONSTANT.

    Le risque est deja p_i(B) : la taille du niveau n'entre plus dans la mesure. Les
    niveaux de moins de `taille_min` personnes sont ecartes, sans etre nommes ni comptes
    individuellement : publier un petit groupe expose serait l'exact contraire de l'objet
    de cet article. Les niveaux sont rendus ANONYMES (rang d'exposition), jamais nommes.
    """
    lignes = []
    for g in np.unique(seg):
        if g < 0:
            continue
        m = seg == g
        if m.sum() < taille_min:
            continue
        lignes.append({"axe": etiquette_axe, "n": int(m.sum()),
                       "risque_moyen": float(risque[m].mean())})
    if len(lignes) < 2:
        return lignes, np.nan
    vals = np.array([l["risque_moyen"] for l in lignes])
    ecart = float(vals.max() / vals.min()) if vals.min() > 0 else np.inf
    for rangl, l in enumerate(sorted(lignes, key=lambda d: -d["risque_moyen"])):
        l["rang_exposition"] = rangl + 1
    return lignes, ecart


# ---------------------------------------------------------------------------
# 4. Assemblage d'un bloc de mesures pour un vecteur de risque
# ---------------------------------------------------------------------------

def bloc_inegalite(nom, jeu, risque, b, suffixe_graine):
    g, g_bas, g_haut = bootstrap_statistique(risque, gini, [GRAINE, 301, graine_nom(suffixe_graine)])
    p10, p10_bas, p10_haut = bootstrap_statistique(
        risque, part_decile, [GRAINE, 302, graine_nom(suffixe_graine)])
    p1 = part_decile(risque, 0.01)
    d = deciles(risque)
    m, m_bas, m_haut = bootstrap_personnes(risque, n_tirages=N_BOOTSTRAP,
                                           graine=[GRAINE, 303, graine_nom(suffixe_graine)])
    return {
        "jeu": jeu, "mesure": nom, "bassin_b": b, "n_personnes": len(risque),
        "risque_moyen": m, "risque_moyen_bas": m_bas, "risque_moyen_haut": m_haut,
        "risque_median": float(np.median(risque)),
        "gini": g, "gini_bas": g_bas, "gini_haut": g_haut,
        "part_decile_sup": p10, "part_decile_sup_bas": p10_bas,
        "part_decile_sup_haut": p10_haut,
        "part_centile_sup": p1,
        "decile_1": d[0], "decile_5": d[4], "decile_9": d[8], "decile_10": d[9],
        "rapport_d10_sur_d5": float(d[9] / d[4]) if d[4] > 0 else np.inf,
        "frac_risque_sous_1pct": float(np.mean(np.asarray(risque) < 0.01)),
        "frac_risque_sur_50pct": float(np.mean(np.asarray(risque) > 0.50)),
        "frac_risque_sur_90pct": float(np.mean(np.asarray(risque) > 0.90)),
    }


# ---------------------------------------------------------------------------
# 5. Programme
# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes, lignes_seg, lignes_corr = [], [], []

    paq = T1.charger()
    codes = paq["codes"]
    n_total = paq["n"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool_v4 = codes[REF_V4][:, items]
    pool_v13 = codes[REF_V13][:, items]
    print(f"Twin : {n_total} personnes, {len(items)} items toujours renseignes", flush=True)

    x = codes[CIBLE][:, items]
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))
    print(f"cible : {CIBLE}, {len(couverts)} personnes couvertes", flush=True)

    # --- GARDE-FOU : le controle de fidelite prealable, AVANT toute lecture d'equite ---
    print("\n=== controle d'interpretabilite prealable (obligatoire) ===", flush=True)
    diag = controle_avant_interpretation(couverts, items, x[couverts], CIBLE, paq=paq)
    print(f"  {CIBLE} PASSE : top-1 {diag['candidat_top1']*100:.2f} % "
          f"[{diag['candidat_ic'][0]*100:.2f};{diag['candidat_ic'][1]*100:.2f}] vs "
          f"baseline {diag['baseline_top1']*100:.2f} % "
          f"[{diag['baseline_ic'][0]*100:.2f};{diag['baseline_ic'][1]*100:.2f}] "
          f"sur le bassin de {diag['bassin']} reellement attaque.", flush=True)

    # --- attaque, cible principale (v4) et cible de validation (v1-3) ---
    rng = np.random.default_rng([GRAINE, graine_nom(CIBLE)])
    rang_v4, top1_v4, _ = rangs_attaque(x[couverts], pool_v4, couverts, rng)
    rang_v13, top1_v13, _ = rangs_attaque(x[couverts], pool_v13, couverts, rng)

    r100 = risque_a_bassin_constant(rang_v4, n_total, B_PRINCIPAL)
    r1000 = risque_a_bassin_constant(rang_v4, n_total, B_CONTROLE)
    rcomplet = risque_a_bassin_constant(rang_v4, n_total, n_total)

    print(f"\ncontrole de coherence : p_i(B=N) moyen = {rcomplet.mean():.4f} "
          f"vs top-1 observe = {top1_v4.mean():.4f} (doivent coincider)", flush=True)

    for nom_r, r, b in (("risque nu (jumeau)", r100, B_PRINCIPAL),
                        ("risque nu (jumeau)", r1000, B_CONTROLE),
                        ("risque nu (jumeau)", rcomplet, n_total)):
        lignes.append(bloc_inegalite(nom_r, "Twin-2K-500", r, b, f"twin|{nom_r}|{b}"))
    for l in lignes:
        print(f"  B={l['bassin_b']:5d} moyenne={l['risque_moyen']:.4f} "
              f"mediane={l['risque_median']:.4f} Gini={l['gini']:.3f} "
              f"[{l['gini_bas']:.3f};{l['gini_haut']:.3f}] part D10={l['part_decile_sup']:.3f}",
              flush=True)

    # --- comparateur : la baseline demographique, meme bassin, memes items ---
    xd = codes[DEMO][:, items]
    cov_d = np.flatnonzero((codes[DEMO] >= 0).any(axis=1))
    rng_d = np.random.default_rng([GRAINE, graine_nom(DEMO)])
    rang_d, _, _ = rangs_attaque(xd[cov_d], pool_v4, cov_d, rng_d)
    r_demo = risque_a_bassin_constant(rang_d, n_total, B_PRINCIPAL)
    lignes.append(bloc_inegalite("baseline Demographics Only", "Twin-2K-500", r_demo,
                                 B_PRINCIPAL, "twin|demo"))

    # --- P3 : validation non circulaire (rang sur v4, succes compte sur v1-3) ---
    print("\n=== P3 : concentration validee sur une AUTRE cible ===", flush=True)
    ps, ps_bas, ps_haut = bootstrap_couple(
        r100, top1_v13, lambda a, b: part_succes_du_decile(a, b, 0.10),
        [GRAINE, 304])
    ps25, _, _ = bootstrap_couple(r100, top1_v13,
                                  lambda a, b: part_succes_du_decile(a, b, 0.25),
                                  [GRAINE, 305], n_tirages=1)
    print(f"  decile le plus expose selon v4 : {ps*100:.1f} % [{ps_bas*100:.1f};"
          f"{ps_haut*100:.1f}] des top-1 reussis contre v1-3 (uniformite = 10 %)",
          flush=True)
    lignes_corr.append({"jeu": "Twin-2K-500", "quantite": "part des top-1 v1-3 captee par "
                        "le decile le plus expose selon v4", "valeur": ps,
                        "ic_bas": ps_bas, "ic_haut": ps_haut, "attendu_si_uniforme": 0.10})
    lignes_corr.append({"jeu": "Twin-2K-500", "quantite": "part des top-1 v1-3 captee par "
                        "le quartile le plus expose selon v4", "valeur": ps25,
                        "ic_bas": np.nan, "ic_haut": np.nan, "attendu_si_uniforme": 0.25})

    # --- P4 : qui sont les plus exposes ---
    print("\n=== P4 : correlats de l'exposition (Spearman, IC bootstrap personnes) ===",
          flush=True)
    hum4 = codes[REF_V4][:, items][couverts]
    hum13 = codes[REF_V13][:, items][couverts]
    caracteristiques = {
        "atypicite des reponses (distance au mode)": atypicite(codes[REF_V4][:, items])[couverts],
        "nombre de reponses non manquantes (108 items)":
            (codes[REF_V4] >= 0).sum(axis=1)[couverts].astype(float),
        "coherence interne test-retest (v4 vs v1-3)": coherence_test_retest(hum4, hum13),
        "atypicite du JUMEAU (distance au mode des jumeaux)": atypicite(x)[couverts],
    }
    for nom_c, vec in caracteristiques.items():
        if np.nanstd(vec) < 1e-12:
            print(f"  {nom_c} : constante, ignoree", flush=True)
            continue
        rho, bas, haut = bootstrap_couple(
            r100, vec, lambda a, b: spearmanr(a, b).statistic,
            [GRAINE, 306, graine_nom(nom_c)])
        lignes_corr.append({"jeu": "Twin-2K-500", "quantite": f"Spearman risque ~ {nom_c}",
                            "valeur": rho, "ic_bas": bas, "ic_haut": haut,
                            "attendu_si_uniforme": 0.0})
        print(f"  rho = {rho:+.3f} [{bas:+.3f};{haut:+.3f}]  {nom_c}", flush=True)

    # --- segments demographiques, a bassin constant, groupes >= 20, jamais nommes ---
    print(f"\n=== segments demographiques (B={B_PRINCIPAL} fixe, groupes >= "
          f"{TAILLE_MIN_GROUPE}, niveaux anonymises) ===", flush=True)
    for axe in ("genre", "ethnicite", "age", "education", "ideologie politique"):
        if axe not in paq["seg_a6"]:
            continue
        segc = paq["seg_a6"][axe][couverts]
        lg, ecart = moyennes_par_niveau(r100, segc, axe)
        lignes_seg.extend(lg)
        if len(lg) >= 2:
            print(f"  {axe:22s} {len(lg)} niveaux retenus, rapport max/min du risque "
                  f"moyen = {ecart:.2f}", flush=True)

    # --- P5 : l'effet de la defense D4 sur l'INEGALITE ---
    print("\n=== P5 : la defense D4 (melange intra-segment) ===", flush=True)
    idx_achat_abs = items_achat(paq)
    i_achat = np.flatnonzero(np.isin(items, idx_achat_abs))
    seg_gra = paq["seg"]["S_gra"]
    x_cov = x[couverts]
    x_def = x_cov.copy()
    x_def[:, i_achat] = defense_d4(x_cov[:, i_achat], seg_gra[couverts])
    rng_def = np.random.default_rng([GRAINE, 200, graine_nom(CIBLE), graine_nom("D4")])
    rang_def, top1_def, _ = rangs_attaque(x_def, pool_v4, couverts, rng_def)
    r100_def = risque_a_bassin_constant(rang_def, n_total, B_PRINCIPAL)
    bloc_d4 = bloc_inegalite("apres defense D4", "Twin-2K-500", r100_def,
                             B_PRINCIPAL, "twin|d4")
    lignes.append(bloc_d4)
    r_def_complet = risque_a_bassin_constant(rang_def, n_total, n_total)
    lignes.append(bloc_inegalite("apres defense D4", "Twin-2K-500", r_def_complet,
                                 n_total, "twin|d4|complet"))

    # le test decisif preenregistre : le decile le plus expose AVANT D4, apres D4
    k = max(1, int(round(0.10 * len(r100))))
    haut_avant = np.argsort(-r100)[:k]
    masque_haut = np.zeros(len(r100), dtype=bool)
    masque_haut[haut_avant] = True
    ratio_avant = float(r100[masque_haut].mean() / r100[~masque_haut].mean())
    ratio_apres = float(r100_def[masque_haut].mean() / r100_def[~masque_haut].mean())
    reduction_haut = float(1.0 - r100_def[masque_haut].mean() / r100[masque_haut].mean())
    reduction_reste = float(1.0 - r100_def[~masque_haut].mean() / r100[~masque_haut].mean())
    print(f"  risque moyen B={B_PRINCIPAL} : {r100.mean():.4f} -> {r100_def.mean():.4f}",
          flush=True)
    print(f"  Gini (B={B_PRINCIPAL}) : {lignes[0]['gini']:.3f} -> {bloc_d4['gini']:.3f} "
          "-- la hausse est en partie mecanique : un Gini calcule sur une distribution "
          "ecrasee vers zero monte meme si la reduction est proportionnelle. Le test "
          "decisif est le rapport ci-dessous, pas ce Gini.", flush=True)
    print(f"  rapport decile le plus expose / reste : {ratio_avant:.2f} avant, "
          f"{ratio_apres:.2f} apres D4 (seuils preenregistres : > 3 = D4 laisse les plus "
          f"vulnerables relativement exposes ; < 1,5 = D4 egalise)", flush=True)
    print(f"  reduction relative du risque : {reduction_haut*100:.2f} % pour le decile le "
          f"plus expose, {reduction_reste*100:.2f} % pour les 90 % restants", flush=True)

    # D4 deplace-t-elle le risque, ou le reduit-elle la ou il etait ? Le decile le plus
    # expose APRES est-il le meme groupe de personnes qu'AVANT ? (agrege, aucun individu)
    haut_apres = np.argsort(-r100_def)[:k]
    recouvrement = float(len(np.intersect1d(haut_avant, haut_apres)) / k)
    print(f"  recouvrement des deciles les plus exposes avant / apres D4 : "
          f"{recouvrement*100:.1f} % (hasard = 10 %) -- au-dela de ce chiffre, D4 "
          f"deplace l'exposition vers d'autres personnes plutot qu'elle ne l'efface",
          flush=True)
    lignes_corr.append({"jeu": "Twin-2K-500",
                        "quantite": "recouvrement du decile le plus expose avant / apres D4",
                        "valeur": recouvrement, "ic_bas": np.nan, "ic_haut": np.nan,
                        "attendu_si_uniforme": 0.10})
    for nom_q, val in (("rapport decile expose / reste, avant D4", ratio_avant),
                       ("rapport decile expose / reste, apres D4", ratio_apres),
                       ("reduction relative du risque, decile le plus expose",
                        reduction_haut),
                       ("reduction relative du risque, 90 % restants", reduction_reste)):
        lignes_corr.append({"jeu": "Twin-2K-500", "quantite": nom_q, "valeur": val,
                            "ic_bas": np.nan, "ic_haut": np.nan,
                            "attendu_si_uniforme": np.nan})

    # --- replication : archive Park et al., bloc GSS ---
    print("\n=== replication : archive Park et al., bloc GSS ===", flush=True)
    try:
        _, items_p, tables_p, _ = CS.charger_domaine("gss")
        codes_p = CS.coder_categoriel_commun(tables_p, items_p)
        pool_p = codes_p[CS.VAGUE1]
        xp = codes_p["composite"]
        n_p = pool_p.shape[0]
        vrai_p = np.arange(n_p)
        rng_p = np.random.default_rng([GRAINE, graine_nom("park|composite")])
        rang_p, top1_p, _ = CS.rangs_depuis_accord(
            CS.accord_categoriel(xp, pool_p), vrai_p, rng_p)
        print(f"  {n_p} personnes, {len(items_p)} items, top-1 = {top1_p.mean():.4f}",
              flush=True)
        rp = risque_a_bassin_constant(rang_p, n_p, B_PRINCIPAL)
        lignes.append(bloc_inegalite("risque nu (jumeau)", "Park et al. GSS", rp,
                                     B_PRINCIPAL, "park|100"))
        lignes.append(bloc_inegalite("risque nu (jumeau)", "Park et al. GSS",
                                     risque_a_bassin_constant(rang_p, n_p, n_p), n_p,
                                     "park|complet"))
        atyp_p = atypicite(pool_p)
        rho, bas, haut = bootstrap_couple(rp, atyp_p,
                                          lambda a, b: spearmanr(a, b).statistic,
                                          [GRAINE, 307])
        lignes_corr.append({"jeu": "Park et al. GSS",
                            "quantite": "Spearman risque ~ atypicite des reponses "
                                        "(distance au mode)",
                            "valeur": rho, "ic_bas": bas, "ic_haut": haut,
                            "attendu_si_uniforme": 0.0})
        print(f"  Gini = {lignes[-2]['gini']:.3f}, part D10 = "
              f"{lignes[-2]['part_decile_sup']:.3f}, rho(atypicite) = {rho:+.3f} "
              f"[{bas:+.3f};{haut:+.3f}]", flush=True)
    except Exception as exc:                                  # noqa: BLE001
        print(f"  replication Park indisponible ({type(exc).__name__}: {exc}) -- "
              "l'absence est declaree, rien n'est extrapole.", flush=True)

    # --- sortie : un seul CSV, uniquement des agregats ---
    df = pd.DataFrame(lignes)
    df_seg = pd.DataFrame(lignes_seg)
    df_corr = pd.DataFrame(lignes_corr)
    for d, bloc in ((df, "inegalite"), (df_seg, "segments"), (df_corr, "correlats")):
        d.insert(0, "bloc", bloc)
    T1.ecrire(pd.concat([df, df_seg, df_corr], ignore_index=True), "c7-equite-risque.csv")

    # --- verdict contre le critere preenregistre de refutation ---
    principal = lignes[0]
    uniforme = bool(principal["gini"] < 0.20
                    and 0.10 <= principal["part_decile_sup"] <= 0.16)
    print(f"\nverdict preenregistre : Gini = {principal['gini']:.3f} (< 0,20 ?), "
          f"part D10 = {principal['part_decile_sup']:.3f} (dans [0,10 ; 0,16] ?) "
          f"-> risque uniforme = {uniforme}", flush=True)


if __name__ == "__main__":
    main()
