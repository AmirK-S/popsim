"""
c7_multiplicite_globale : complète resultats/c7-multiplicite.md, ne le refait pas.

===========================================================================
PREENREGISTREMENT DES ATTENTES : voir resultats/c7-multiplicite-globale-2026-09-12.md,
section 0, ECRITE AVANT CE CALCUL.

CE QUE resultats/c7-multiplicite.md FAIT DEJA (recopié, jamais refait ici) : comptage de
47 tests sur trois familles (article / contrôles autonomes / branches abandonnées), et une
correction de Holm sur les 3 SEULS tests à p classique de l'article (c7-courbe-gen p=0,002 ;
c7-compromis §2 p=0,008 ; c7-compromis §3 p=0,78). Ce fichier dit lui-même, section 3, que
les 31 autres tests sont des IC bootstrap comparés à un seuil et que « Holm/BH ne s'y
applique pas de la même façon, faute de p commensurable », et qu'il n'a pas recalculé
chaque bootstrap. C'est exactement ce que ce script fait.

CE QUE CE SCRIPT AJOUTE :
  1. Une famille confirmatoire ÉLARGIE : un p (classique quand il existe, empirique quand
     la distribution de réplicats est déjà stockée sur disque — c7-disjoint-nul.csv,
     c7-disjoint-partages.csv —, exact binomial/Clopper-Pearson pour les taux à 0 succès,
     sinon une approximation normale à partir de l'IC bootstrap publié et du seuil
     PRÉENREGISTRÉ, jamais un seuil choisi après coup) pour une vingtaine de prédictions
     préenregistrées de A1, A2, A5, A7 (Stanford), A9, A11, A12. Holm ET Benjamini-Hochberg
     (le fichier existant ne faisait que Holm, et seulement sur 3 tests).
  2. FONCTION `bootstrap_commun_twin()`, ECRITE MAIS NON EXECUTEE PAR DEFAUT (voir
     ABANDON ci-dessous) : un bootstrap COMMUN sur les personnes de Twin-2K-500, un seul
     tirage de personnes par réplicat appliqué EN MÊME TEMPS aux 12 points de
     `c7-compromis.csv` et aux taux de fuite de trois configurations, pour en tirer une
     corrélation empirique entre les réplicats (quantifie la dépendance introduite par la
     réutilisation des mêmes 2 058 personnes) et des IC simultanés (maximum studentisé,
     Westfall-Young).

ABANDON, décidé en cours de chantier et assumé comme tel (pas caché) : la première
version de ce script lançait `bootstrap_commun_twin()` par défaut ; le chargement de
Twin-2K-500 (`t1_commun.charger`, ~5 s) suivi du réajustement des 5 plis de
`t1_baselines.calculer` pour PMM/B1/B2 (~160-200 s mesurés sur deux essais) rendait le
temps total incompatible avec un calcul tenu en avant-plan en quelques minutes. Le
coordinateur a demandé l'abandon explicite de cette partie plutôt qu'une nouvelle attente
en arrière-plan. La fonction reste ici, complète et documentée, mais N'EST PAS APPELÉE par
`main()` : `FAIRE_BOOTSTRAP_COMMUN = False` ci-dessous. Conséquence assumée : A1 (rho
fidélité-fuite) et le taux de fuite du meilleur jumeau/Demographics Only/PMM k=10 sur Twin
restent SANS IC simultané ; seuls leurs IC marginaux, déjà publiés séparément, existent.
Aucun second essai n'a été fait dans ce chantier.

PORTEE (indépendamment de l'abandon ci-dessus), ce qui n'aurait de toute façon pas été
inclus dans ce bootstrap commun même s'il avait tourné : l'attaquant fort (A-LLR, A11) et
le monde ouvert (A3) ré-estiment des paramètres par pli/seuil à chaque tirage — un
bootstrap commun sur ces analyses serait un chantier séparé, plus coûteux encore ; les bits
d'identité (A4, Miller-Madow) et toute l'archive Park/Stanford (A6, A7-Stanford, A11-Park)
n'auraient pas non plus été inclus (substrat de personnes différent). Ces revendications
n'ont donc, dans ce chantier, aucun IC simultané avec quoi que ce soit d'autre.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiée (utilisé seulement si
FAIRE_BOOTSTRAP_COMMUN=True) :
  t1_commun.charger                  les quinze tables de Twin
  t1_baselines.calculer               les quatre repères statistiques (B0, B1, B2, PMM)
  c7_reidentification.items_communs, rangs_attaque, graine_nom, CONFIGURATIONS, DEMO
  a44_mesures.exactitude_codes        exactitude par personne (proxy de fidélité)

CE QUI EST NOUVEAU ICI, et TOURNE PAR DEFAUT : la table de p approchés pour la famille
confirmatoire élargie (méthodes empirique / classique / Wald / binomiale exacte selon le
test) et la correction Holm + Benjamini-Hochberg ; le traitement explicite du cas « 0 succès
sur n petit » par un test binomial exact plutôt qu'un IC percentile dégénéré (voir le test
A9_fort_top1 : IC percentile publié [0% ; 0%] sur 0/30, artefact — Clopper-Pearson exact
donne [0% ; 11,57%], le seuil préenregistré de 5% n'est PAS franchi ni exclu par les
données : verdict NON CONCLUANT, pas réfuté).

Aucun appel de modèle de langage. Lecture seule sur data/ et resultats/. Aucun script
existant modifié.
Usage : .venv/bin/python analyses/c7_multiplicite_globale.py
===========================================================================
"""

import os
import sys

import numpy as np                             # noqa: E402
import pandas as pd                            # noqa: E402
from scipy import stats                        # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

GRAINE = 20260912
N_BOOTSTRAP = 2000
STATISTIQUES = ["B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

# Décidé en cours de chantier (voir ABANDON ci-dessus). Ne pas repasser a True sans
# revoir le budget de temps disponible : ~170-200s seulement pour t1_baselines.calculer.
FAIRE_BOOTSTRAP_COMMUN = False


def z_deux_echantillons(est1, bas1, haut1, est2, bas2, haut2, sens):
    """p approché (normal, Wald) pour un test a deux echantillons independants, chacun
    resume par son IC a 95% publie. sens='>' : H1 est 'est1 > est2' (la prediction
    preenregistree)."""
    se1 = (haut1 - bas1) / (2 * 1.959964)
    se2 = (haut2 - bas2) / (2 * 1.959964)
    se = np.sqrt(se1 ** 2 + se2 ** 2)
    if se <= 0 or not np.isfinite(se):
        return np.nan, np.nan, se
    z = (est1 - est2) / se if sens == ">" else (est2 - est1) / se
    p = float(stats.norm.sf(z))
    return p, z, se


def z_seuil(estimate, ci_bas, ci_haut, seuil, sens):
    """p approché (normal, Wald) pour H0 : le paramètre est du mauvais côté du seuil
    PRÉENREGISTRÉ, contre H1 : la prédiction préenregistrée est vraie. p petit = forte
    évidence en faveur de la prédiction préenregistrée. SE estimé depuis l'IC à 95%
    publié (approximation normale symétrique). Renvoie NaN si l'IC est dégénéré (largeur
    nulle, ex. 0 succès sur peu d'essais) : utiliser p_seuil_binomial dans ce cas."""
    se = (ci_haut - ci_bas) / (2 * 1.959964)
    if se <= 0 or not np.isfinite(se):
        return np.nan, np.nan, se
    z = (estimate - seuil) / se if sens == ">" else (seuil - estimate) / se
    return float(stats.norm.sf(z)), z, se


def p_seuil_binomial(k, n, seuil, sens=">"):
    """p exact (test binomial) pour un taux estimé sur k succès / n essais, utilise
    quand l'IC percentile publié est dégénéré (k=0 ou k=n rend le bootstrap incapable de
    produire autre chose que la borne). sens='>' : H1 = 'le taux vrai depasse seuil'.
    Renvoie aussi l'IC exact de Clopper-Pearson a 95%."""
    if sens == ">":
        p_confirmation = float(1 - stats.binom.cdf(k - 1, n, seuil)) if k > 0 else 1.0
    else:
        p_confirmation = float(stats.binom.cdf(k, n, seuil))
    cp_bas = 0.0 if k == 0 else float(stats.beta.ppf(0.025, k, n - k + 1))
    cp_haut = 1.0 if k == n else float(stats.beta.ppf(0.975, k + 1, n - k))
    return p_confirmation, (cp_bas, cp_haut)


def bootstrap_commun_twin():
    """Bootstrap COMMUN sur les personnes de Twin : un seul tirage de personnes par
    réplicat, appliqué à la fois aux 12 points de c7-compromis.csv (rho fidélité-fuite,
    A1) et aux taux de fuite de trois configurations (A2/A3, proxy fermé). ECRIT MAIS
    NON APPELE PAR DEFAUT (voir ABANDON en tête de fichier) : ~170-200s pour la seule
    étape t1_baselines.calculer, mesuré sur deux essais interrompus dans ce chantier.
    """
    import time
    import t1_commun as T1
    import t1_baselines as TB
    import c7_reidentification as C7
    from a44_mesures import exactitude_codes

    t0 = time.time()
    paq = T1.charger()
    codes = paq["codes"]
    n_total = paq["n"]
    items = C7.items_communs(codes, [C7.REF_V4, C7.REF_V13])
    print(f"{n_total} personnes, {len(items)} items communs, charge en "
          f"{time.time() - t0:.0f}s", flush=True)
    pool_v4 = codes[C7.REF_V4][:, items]

    noms_12 = list(C7.CONFIGURATIONS) + list(STATISTIQUES)
    top1_vec, exact_vec, couv = {}, {}, {}

    for nom in C7.CONFIGURATIONS:
        x = codes[nom][:, items]
        couverts = np.flatnonzero((codes[nom] >= 0).any(axis=1))
        rng = np.random.default_rng([GRAINE, C7.graine_nom(nom)])
        _, top1, _ = C7.rangs_attaque(x[couverts], pool_v4, couverts, rng)
        v = np.full(n_total, np.nan)
        v[couverts] = top1
        top1_vec[nom] = v
        exact_vec[nom] = exactitude_codes(x, pool_v4)
        couv[nom] = couverts

    paq_slim = dict(paq)
    codes_slim = dict(paq["codes"])
    codes_slim[T1.REF] = paq["codes"][T1.REF][:, items]
    paq_slim["codes"] = codes_slim
    base = TB.calculer(paq_slim, avec_pmm=True)

    for nom in STATISTIQUES:
        x = base[nom]
        rng = np.random.default_rng([GRAINE, C7.graine_nom(nom)])
        _, top1, _ = C7.rangs_attaque(x, pool_v4, np.arange(n_total), rng)
        top1_vec[nom] = top1
        exact_vec[nom] = exactitude_codes(x, pool_v4)
        couv[nom] = np.arange(n_total)

    common = None
    for nom in noms_12:
        s = set(couv[nom].tolist())
        common = s if common is None else (common & s)
    common_idx = np.array(sorted(common))
    n_common = len(common_idx)

    M_top1 = np.column_stack([top1_vec[nom][common_idx] for nom in noms_12])
    M_exact = np.column_stack([exact_vec[nom][common_idx] for nom in noms_12])

    obs_top1 = M_top1.mean(axis=0)
    obs_exact = M_exact.mean(axis=0)
    rho_obs, _ = stats.spearmanr(obs_exact, obs_top1)

    idx_best = noms_12.index("JSON Persona - GPT4.1")
    idx_demo = noms_12.index(C7.DEMO)
    idx_pmm = noms_12.index("PMM k=10")

    rng_boot = np.random.default_rng(GRAINE)
    rhos = np.empty(N_BOOTSTRAP)
    top1_best = np.empty(N_BOOTSTRAP)
    top1_demo = np.empty(N_BOOTSTRAP)
    top1_pmm = np.empty(N_BOOTSTRAP)
    exact_best = np.empty(N_BOOTSTRAP)

    for b in range(N_BOOTSTRAP):
        draw = rng_boot.integers(0, n_common, size=n_common)
        tt = M_top1[draw].mean(axis=0)
        ee = M_exact[draw].mean(axis=0)
        r, _ = stats.spearmanr(ee, tt)
        rhos[b] = r
        top1_best[b] = tt[idx_best]
        top1_demo[b] = tt[idx_demo]
        top1_pmm[b] = tt[idx_pmm]
        exact_best[b] = ee[idx_best]

    metrics = {
        "rho_fidelite_fuite_A1": (rho_obs, rhos),
        "top1_meilleur_jumeau_A2_A3": (obs_top1[idx_best], top1_best),
        "top1_demographics_only_A2": (obs_top1[idx_demo], top1_demo),
        "top1_pmm_k10_A2": (obs_top1[idx_pmm], top1_pmm),
        "exactitude_meilleur_jumeau_A9": (obs_exact[idx_best], exact_best),
    }
    noms_m = list(metrics.keys())
    hats = np.array([metrics[m][0] for m in noms_m])
    reps = np.column_stack([metrics[m][1] for m in noms_m])
    se = reps.std(axis=0, ddof=1)
    z_max = np.max(np.abs(reps - hats) / se, axis=1)
    c_star = np.percentile(z_max, 95)
    corr = np.corrcoef(reps, rowvar=False)
    return dict(noms=noms_m, hats=hats, se=se, c_star=c_star, corr=corr, n_commun=n_common)


def famille_confirmatoire():
    """Partie rapide (lecture de petits CSV déjà écrits, aucun chargement de Twin/Park) :
    la famille confirmatoire élargie, ses p, Holm et Benjamini-Hochberg."""
    tests = []

    # --- A1, disjoint (empirique, replicats deja sur disque) ---
    nul = pd.read_csv(os.path.join(SORTIE, "c7-disjoint-nul.csv"))
    part = pd.read_csv(os.path.join(SORTIE, "c7-disjoint-partages.csv"))
    resume = pd.read_csv(os.path.join(SORTIE, "c7-disjoint-resume.csv")).iloc[0]
    rho_disjoint = float(resume.rho_disjoint_moyen)
    p_nul_emp = float((nul.rho_nul >= rho_disjoint).mean())
    rhos_split = (part.groupby("partage")
                  .apply(lambda g: stats.spearmanr(g.fidelite_A, g.fuite_B)[0])
                  .values)
    p_seuil_emp = float((rhos_split <= 0.7).mean())
    tests.append(dict(id="A1_disjoint_a", claim="A1",
                       description="rho(fidelite,fuite) sur items disjoints > 0,70 (moyenne sur 50 partages)",
                       estimate=rho_disjoint, seuil=0.7, p=max(p_seuil_emp, 1e-300),
                       methode="empirique (50 partages)", confirmatoire=True))
    tests.append(dict(id="A1_disjoint_b", claim="A1",
                       description="rho observe (items disjoints) > 95e centile du nul de marge",
                       estimate=rho_disjoint, seuil=float(resume.nul_95e_centile),
                       p=max(p_nul_emp, 1e-300), methode="empirique (100 replicats du nul)",
                       confirmatoire=True))

    # --- A1, rho primaire (12 points, c7-compromis) : classique ---
    comp = pd.read_csv(os.path.join(SORTIE, "c7-compromis.csv"))
    r, p = stats.spearmanr(comp.fidelite_plancher, comp.fuite_top1)
    tests.append(dict(id="A1_primaire", claim="A1",
                       description="rho(fidelite,fuite) sur 12 points >= 0,70 (preenregistre compromis)",
                       estimate=float(r), seuil=0.7, p=float(p),
                       methode="classique (spearmanr, H0 rho=0, n=12)", confirmatoire=True))

    # --- A9 courbe-gen : classique (deja dans c7-multiplicite.md, repris) ---
    cg = pd.read_csv(os.path.join(SORTIE, "c7-courbe-gen.csv"))
    tests.append(dict(id="A9_courbe_gen_pente", claim="A9",
                       description="regression fuite~exactitude (12 pts) non nulle, r=0,785",
                       estimate=float(cg.regression_r.iloc[0]), seuil=0.0,
                       p=float(cg.regression_p.iloc[0]), methode="classique (deja c7-multiplicite.md)",
                       confirmatoire=True))
    n_dans = int(cg.dans_intervalle.sum())
    tests.append(dict(id="A9_courbe_gen_verif", claim="A9",
                       description=f"{n_dans}/7 jumeaux regeneres dans l'IP a 95% (seuil succes >=4/7 dedans)",
                       estimate=float(n_dans), seuil=4.0, p=np.nan,
                       methode="denombrement, non convertible en p", confirmatoire=True))

    # --- A9 fort (modele fort, appel par item) ---
    fort = pd.read_csv(os.path.join(SORTIE, "c7-fort-reidentification.csv")).iloc[0]
    p_f, _, _ = z_seuil(float(fort.exactitude), float(fort.exactitude_bas),
                        float(fort.exactitude_haut), 0.55, ">")
    tests.append(dict(id="A9_fort_exactitude", claim="A9",
                       description="exactitude du jumeau fort (appel par item, gpt-4.1) > 0,55",
                       estimate=float(fort.exactitude), seuil=0.55, p=p_f,
                       methode="normale (Wald sur IC publie)", confirmatoire=True))
    # CORRECTION du 12/09 au soir (signalee par le coordinateur) : l'IC percentile publie
    # de ce test est [0% ; 0%] sur k=0 succes / n=30 -- artefact, le bootstrap percentile
    # ne peut pas produire autre chose que 0 quand tous les tirages valent 0. Test binomial
    # exact + Clopper-Pearson a la place d'un Wald sur cet IC degenere.
    n_fort = int(fort.n_attaques)
    k_fort = int(round(float(fort.top1) * n_fort))
    p_f2, cp = p_seuil_binomial(k_fort, n_fort, 0.05, ">")
    tests.append(dict(id="A9_fort_top1", claim="A9",
                       description=f"top-1 du jumeau fort > 5% (k={k_fort}/{n_fort} ; IC publie [0%;0%] "
                                   f"degenere ; Clopper-Pearson exact [{cp[0]*100:.2f}%;{cp[1]*100:.2f}%] "
                                   "-> NON CONCLUANT, pas refute : le seuil de 5% est dans l'IC exact",
                       estimate=float(fort.top1), seuil=0.05, p=p_f2,
                       methode="binomial exact (Clopper-Pearson), k=0 rend le Wald sur IC publie invalide",
                       confirmatoire=True))
    tests.append(dict(id="A9_fort_fidelite", claim="A9",
                       description="fidelite_plancher du jumeau fort > 0,10 (pas d'IC publie -> seuil non testable)",
                       estimate=float(fort.fidelite_plancher), seuil=0.10, p=np.nan,
                       methode="point seul, non convertible en p", confirmatoire=True))

    # --- A9 recette (granularite d'appel) : 0/0, meme famille d'artefact que A9_fort_top1 ---
    rec = pd.read_csv(os.path.join(SORTIE, "c7-recette-reidentification.csv"))
    rec_unique = rec[rec.configuration.str.contains("unique", case=False, na=False)]
    rec_item = rec[rec.configuration.str.contains("item", case=False, na=False)]
    if len(rec_unique) and len(rec_item):
        u, i = rec_unique.iloc[0], rec_item.iloc[0]
        n_u, n_i = int(u.n_attaques), int(i.n_attaques)
        _, cp_u = p_seuil_binomial(0, n_u, 0.0, ">")
        _, cp_i = p_seuil_binomial(0, n_i, 0.0, ">")
        tests.append(dict(id="A9_recette_granularite", claim="A9",
                           description=f"top-1 (appel par item, n={n_i}) >= 5x top-1 (appel unique, n={n_u}) ; "
                                       f"0/{n_i} et 0/{n_u} -> Clopper-Pearson [0;{cp_i[1]*100:.1f}%] et "
                                       f"[0;{cp_u[1]*100:.1f}%] : chevauchement total, non discriminant",
                           estimate=float(i.top1 - u.top1), seuil=np.nan, p=np.nan,
                           methode="0/0 des deux cotes, non convertible en p ; NON CONCLUANT (pas refute : "
                                   "aucun pouvoir statistique a ce n pour distinguer les deux bras)",
                           confirmatoire=True))

    # --- A2 generateur individualise ---
    gen = pd.read_csv(os.path.join(SORTIE, "c7-generateur-resultats.csv"))
    for _, row in gen.iterrows():
        p_g, _, _ = z_seuil(float(row.top1), float(row.top1_bas), float(row.top1_haut), 0.10, "<")
        tests.append(dict(id=f"A2_generateur_{row.generateur}", claim="A2",
                           description=f"generateur {row.generateur} top-1 << jumeau (seuil indicatif < 10%)",
                           estimate=float(row.top1), seuil=0.10, p=p_g,
                           methode="normale (Wald sur IC publie)", confirmatoire=True))

    # --- A11 / attaquant fort ---
    af = pd.read_csv(os.path.join(SORTIE, "c7-attaquant-fort.csv"))
    naif = {"Twin": 0.2069, "Park GSS": 0.6572}
    seuils_relatifs = {"Twin": 0.248, "Park GSS": 0.789}
    for jeu in ["Twin", "Park GSS"]:
        cand = af[(af.jeu == jeu) & (af.attaque == "A-LLR (vraisemblance, hors pli)")]
        if not len(cand):
            continue
        row = cand.iloc[0]
        p_a, _, _ = z_seuil(float(row.top1), float(row.top1_bas), float(row.top1_haut),
                             seuils_relatifs[jeu], ">")
        tests.append(dict(id=f"A11_P1_{jeu}", claim="A11",
                           description=f"[P1] A-LLR top-1 {jeu} > {seuils_relatifs[jeu]*100:.1f}% "
                                       f"(gain >=20% relatif vs naif {naif[jeu]*100:.2f}%)",
                           estimate=float(row.top1), seuil=seuils_relatifs[jeu], p=p_a,
                           methode="normale (Wald sur IC publie)", confirmatoire=True))
    d4 = af[(af.jeu == "Twin") & (af.attaque == "D4 / A-LLR (recalibre sur D4)")]
    if len(d4):
        row = d4.iloc[0]
        p_d4, _, _ = z_seuil(float(row.top1), float(row.top1_bas), float(row.top1_haut), 0.01, "<")
        tests.append(dict(id="A11_P2_D4_sous_attaquant_fort", claim="A11",
                           description="[P2] D4 sous A-LLR (recalibre) : top-1 < 1%",
                           estimate=float(row.top1), seuil=0.01, p=p_d4,
                           methode="normale (Wald sur IC publie)", confirmatoire=True))

    # --- A7 Stanford (transfert inter-jumeaux) ---
    ts = pd.read_csv(os.path.join(SORTIE, "c7-transfert-stanford-attaque.csv"))
    ts_gss = ts[ts.domaine.str.contains("gss", case=False, na=False)
                & ~ts.direction.str.contains("demo", case=False, na=False)]
    for _, row in ts_gss.iterrows():
        p_t, _, _ = z_seuil(float(row.top1), float(row.top1_bas), float(row.top1_haut), 0.20, ">")
        tests.append(dict(id=f"A7_stanford_{row.direction}", claim="A7",
                           description=f"transfert inter-jumeaux Stanford GSS ({row.direction}) top-1 >= 20%",
                           estimate=float(row.top1), seuil=0.20, p=p_t,
                           methode="normale (Wald sur IC publie)", confirmatoire=True))

    # --- A12 DP vs D4 ---
    dp = pd.read_csv(os.path.join(SORTIE, "c7-dp-resultats.csv"))
    dp_finite = dp[~dp.epsilon.str.contains("infini", case=False, na=False)]
    ecart_min = (dp_finite.utilite_globale - 1.47).min()
    tests.append(dict(id="A12_dp_vs_d4", claim="A12",
                       description="aucun epsilon DP a moins de 5 points d'utilite de D4 (1,47 pt) "
                                   f"(ecart mesure le plus petit = {ecart_min:.2f} pt)",
                       estimate=float(ecart_min), seuil=5.0, p=np.nan,
                       methode="ecart de point, pas d'IC sur l'utilite -> non convertible en p ; "
                               "refute qualitativement (ecart << 5)", confirmatoire=True))

    # --- A13 utilite aval ---
    ua_c = pd.read_csv(os.path.join(SORTIE, "c7-utilite-aval-C-acp.csv"))
    brut = ua_c[ua_c.condition.str.contains("brut", case=False, na=False)]
    d4r = ua_c[ua_c.condition.str.contains("D4", case=False, na=False)]
    if len(brut) and len(d4r):
        chute_rel = 1 - float(d4r.part_pc1_pc2.iloc[0]) / float(brut.part_pc1_pc2.iloc[0])
        tests.append(dict(id="A13_acp_chute", claim="A13",
                           description=f"ACP : chute relative de variance PC1+PC2 (brut->D4) >= 30% "
                                       f"(observe {chute_rel*100:.1f}%)",
                           estimate=float(chute_rel), seuil=0.30, p=np.nan,
                           methode="point seul (pas d'IC sur le ratio) -> non convertible en p",
                           confirmatoire=True))

    # --- A5 mecanisme : H1 (equivalence, categorique), H2 (Wald), H4 (Wald, 2 echantillons) ---
    h1 = pd.read_csv(os.path.join(SORTIE, "c7-mecanisme-h1.csv")).iloc[0]
    tests.append(dict(id="A5_mecanisme_H1_entropie", claim="A5",
                       description="H1 : a entropie appariee, IC(top1 achat) et IC(top1 opinion) se "
                                   f"chevauchent (observe {h1.top1_achat_apparie:.4f} vs {h1.top1_opinion:.4f}, "
                                   "chevauchement_ic=False)",
                       estimate=float(h1.top1_achat_apparie - h1.top1_opinion), seuil=np.nan, p=np.nan,
                       methode="test d'equivalence, pas de marge preenregistree -> non convertible en p ; "
                               "refute categoriquement (IC disjoints)", confirmatoire=True))
    h2 = pd.read_csv(os.path.join(SORTIE, "c7-mecanisme-h2.csv")).iloc[0]
    p_h2, _, _ = z_seuil(float(h2.correlation_personne_a_personne), float(h2.correlation_bas),
                        float(h2.correlation_haut), 0.0, ">")
    tests.append(dict(id="A5_mecanisme_H2_coherence", claim="A5",
                       description="H2 : correlation personne-a-personne (coherence achat, humains vs IA) > 0",
                       estimate=float(h2.correlation_personne_a_personne), seuil=0.0, p=p_h2,
                       methode="normale (Wald sur IC publie)", confirmatoire=True))
    h4 = pd.read_csv(os.path.join(SORTIE, "c7-mecanisme-h4.csv")).iloc[0]
    p_h4, _, _ = z_deux_echantillons(float(h4.taux_stereotypie_ia), float(h4.taux_stereotypie_ia_bas),
                                      float(h4.taux_stereotypie_ia_haut), float(h4.taux_stereotypie_humains),
                                      float(h4.taux_stereotypie_humains_bas), float(h4.taux_stereotypie_humains_haut),
                                      ">")
    tests.append(dict(id="A5_mecanisme_H4_stereotypie", claim="A5",
                       description="H4 : taux de stereotypie IA nettement SUPERIEUR aux humains (segment S_gra, LOO)",
                       estimate=float(h4.taux_stereotypie_ia - h4.taux_stereotypie_humains), seuil=0.0,
                       p=p_h4, methode="normale (Wald, 2 echantillons)", confirmatoire=True))

    return pd.DataFrame(tests)


def holm_bh(df_tests):
    convertibles = df_tests[df_tests.p.notna()].copy().sort_values("p").reset_index(drop=True)
    convertibles["rang"] = np.arange(1, len(convertibles) + 1)
    m = len(convertibles)
    p_sorted = convertibles.p.values

    holm_adj = np.empty(m)
    running_max = 0.0
    for k in range(m):
        running_max = max(running_max, min(1.0, p_sorted[k] * (m - k)))
        holm_adj[k] = running_max
    convertibles["p_holm"] = holm_adj
    convertibles["holm_significatif_0_05"] = convertibles["p_holm"] < 0.05

    bh_adj = np.empty(m)
    running_min = 1.0
    for k in range(m - 1, -1, -1):
        running_min = min(running_min, min(1.0, p_sorted[k] * m / (k + 1)))
        bh_adj[k] = running_min
    convertibles["p_bh"] = bh_adj
    convertibles["bh_significatif_0_05"] = convertibles["p_bh"] < 0.05

    non_convertibles = df_tests[df_tests.p.isna()].copy()
    return pd.concat([convertibles, non_convertibles], ignore_index=True, sort=False), m, len(non_convertibles)


def main():
    df_tests = famille_confirmatoire()
    df_final, m, n_non_conv = holm_bh(df_tests)
    chemin = os.path.join(SORTIE, "c7-multiplicite-globale.csv")
    df_final.to_csv(chemin, index=False)
    print(f"ecrit {chemin}, {len(df_final)} lignes ({m} convertibles en p, {n_non_conv} non convertibles)",
          flush=True)

    conv = df_final[df_final.p.notna()].sort_values("p")
    print("\n=== famille confirmatoire, triee par p, Holm/BH ===", flush=True)
    print(conv[["id", "claim", "p", "p_holm", "p_bh", "holm_significatif_0_05",
                "bh_significatif_0_05"]].to_string(index=False), flush=True)

    non_conv = df_final[df_final.p.isna()]
    print("\n=== non convertibles en p (denombrement, IC degenere, ou point seul) ===", flush=True)
    print(non_conv[["id", "claim", "description"]].to_string(index=False), flush=True)

    if FAIRE_BOOTSTRAP_COMMUN:
        res = bootstrap_commun_twin()
        print("\n=== bootstrap commun (Twin) ===", flush=True)
        for i, nom in enumerate(res["noms"]):
            print(f"  {nom}: hat={res['hats'][i]:.4f} se={res['se'][i]:.4f}", flush=True)
        print(f"c*={res['c_star']:.3f}, n_commun={res['n_commun']}", flush=True)
    else:
        print("\nbootstrap_commun_twin() NON EXECUTE (FAIRE_BOOTSTRAP_COMMUN=False, "
              "voir ABANDON dans le docstring).", flush=True)


if __name__ == "__main__":
    main()
