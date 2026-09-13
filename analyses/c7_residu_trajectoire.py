"""
c7_residu_trajectoire : le residu de ~10x de la trajectoire est-il reel ou un artefact ?

===========================================================================
PREENREGISTREMENT : resultats/c7-residu-trajectoire-preenregistrement.md, ecrit AVANT
toute mesure d'attaque nouvelle. Les seules grandeurs qui y figurent et qui viennent de
ce script sont des statistiques sur les REPONSES HUMAINES seules (bassin, manquants,
modalites, entropie, V de Cramer, items effectifs, accord test-retest) : aucune colonne
de jumeau n'a ete lue avant l'ecriture du preenregistrement.

LA QUESTION. resultats/relecture-fond-2026-09-13.md D3 a montre qu'a nombre d'items
BRUT apparie (12), le contraste 2023 -> 2025 tombe de ~150x a ~10x et le rapport a la
baseline demographique de 1,5 a 4,3. Ce residu est-il reel, ou fabrique par un artefact
que le nombre brut d'items n'apparie pas ? Six artefacts candidats sont testes :
  A1 items EFFECTIFS (redondance entre items), A2 taille du bassin, A3 plafond de
  fiabilite humaine, A4 nature des items (modalites, entropie), A5 non-reponse,
  A6 population. A3 (cote ANES) et A6 ne sont pas neutralisables : c'est dit, pas
  contourne.

ETUDE DE RISQUE DE VIE PRIVEE sur deux jeux deja publics (Twin-2K-500 ; Argyle, Busby,
Fulda, Gubler, Rytting & Wingate 2023, Harvard Dataverse doi:10.7910/DVN/JPV20K, CC0).
Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identifiant d'une personne
retrouvee ni aucune liste d'appariements individuels : seuls des taux agreges sortent
dans resultats/c7-residu-trajectoire.csv.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                                   les tables Twin-2K-500
  c7_reidentification.items_communs                   les 60 items toujours renseignes
  c7_reidentification.rangs_attaque / resume_taux     l'attaque et l'IC de reference
  c7_reidentification.graine_nom / REF_V4 / REF_V13 / DEMO
  a2_commun.distance_hamming                          la distance masquee
  c7_bits.entropie_item                               l'entropie d'un item (Miller-Madow)
  c7_argyle.charger / baseline_demographique / baseline_oracle / cramer_v /
      items_effectifs / attaquer / controle_avant_interpretation / _imputer_loo
  c7_controle_interpretabilite.controle_avant_interpretation   le controle cote Twin

CE QUI EST NOUVEAU ICI, et rien d'autre :
  1. le tirage de sous-ensembles d'items avec MESURE de n_eff et de l'entropie sur le
     sous-ensemble reellement tire (jamais extrapoles par la formule),
  2. l'APPARIEMENT PAR REJET : on ne choisit pas un k, on garde les sous-ensembles dont
     l'information effective mesuree tombe dans une bande etroite autour de la cible
     Argyle -- c'est ce qui distingue ce rapport du temoin a "12 items bruts",
  3. le double bootstrap (personnes x tirages d'items), pour que l'IC publie contienne
     la variance du tirage d'items, que le temoin de relecture-fond ne publiait pas,
  4. les trois conventions de departage des ex aequo (defaut D9 de relecture-fond),
     calculees a chaque regime au lieu d'une seule.

Aucun appel de modele de langage, aucune depense, aucun reseau. Lecture seule sur data/.
Usage :
  .venv/bin/python analyses/c7_residu_trajectoire.py structure   # humains seuls (A4, A5)
  .venv/bin/python analyses/c7_residu_trajectoire.py mesure      # tout le reste
===========================================================================
"""

import os
import sys
import csv

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                               # noqa: E402
from a2_commun import distance_hamming                               # noqa: E402
from c7_reidentification import (                                     # noqa: E402
    items_communs, rangs_attaque, resume_taux, graine_nom,
    REF_V4, REF_V13, DEMO, N_BOOTSTRAP,
)
from c7_bits import entropie_item                                     # noqa: E402
import c7_argyle as ARG                                               # noqa: E402
import c7_controle_interpretabilite as CTRL                           # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260913
CIBLE_TWIN = "JSON Persona - GPT4.1"     # le meme jumeau que le temoin de relecture-fond
N_TIRAGES_ITEMS = 30                     # tirages de sous-ensembles d'items
N_BOOT_DOUBLE = 2000                     # double bootstrap personnes x tirages d'items

# REDUCTIONS DECLAREES (mission : tout en avant-plan, toute reduction annoncee).
# Les etapes 5 a 7 rejouent, sous-ensemble par sous-ensemble, des attaques completes
# (rangs_attaque a 20 melanges d'ex aequo + bootstrap a 2 000 tirages) et des imputeurs
# laisse-un-dehors en O(p n^2). A 30 sous-ensembles par regime elles depassaient l'heure.
# Elles sont donc calculees sur un ECHANTILLON des sous-ensembles apparies -- les memes
# que ceux de l'etape 4, dans l'ordre du tirage, sans selection -- et sur 5 tirages de
# bassin au lieu de 20. Les etapes 1 a 4, qui portent le verdict, ne sont pas reduites.
N_TIRAGES_BASSIN = 5                     # sous-echantillons de bassin (A2), reduit de 20
N_SOUS_ENSEMBLES_LOURDS = 5              # sous-ensembles rejoues aux etapes 5 et 7

ETAT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "__pycache__",
                    "c7_residu_trajectoire_etat.npz")

# Grille de la courbe. k = 60 n'a qu'un seul sous-ensemble possible.
KS = [4, 5, 6, 7, 8, 10, 12, 16, 20, 30, 40, 60]


# ---------------------------------------------------------------------------
# 1. Top-1 sur un sous-ensemble d'items, avec LES TROIS conventions d'ex aequo.
#
# La convention "esperance" (1 / taille de la classe d'ex aequo de tete) est exactement
# ce que c7_reidentification.rangs_attaque estime par 20 melanges aleatoires du depart ;
# elle est calculee ici en forme fermee, sans melange, parce que la courbe demande des
# centaines d'attaques. Les regimes apparies, eux, sont RE-mesures avec rangs_attaque
# lui-meme (section 5), pour verifier que la forme fermee et le melange coincident.
#
# Les deux conventions encadrantes repondent au defaut D9 de relecture-fond : a faible
# nombre d'items, les classes d'ex aequo sont grandes et le taux publie est une
# convention, pas une mesure. Les publier toutes les trois est le seul honnete.
# ---------------------------------------------------------------------------

def top1_trois_conventions(x, pool, sel):
    """(esperance, favorable, defavorable, taille de classe), par personne.

    x : codes du candidat (n, p) ; pool : humains (n, p) ; sel : indices de colonnes.
    La vraie personne de la ligne i est la ligne i du pool (alignement Twin standard).
    """
    accord = 1.0 - distance_hamming(x[:, sel], pool[:, sel])
    n = accord.shape[0]
    vrai = accord[np.arange(n), np.arange(n)]
    meilleur = accord.max(axis=1)
    taille = (accord >= meilleur[:, None] - 1e-12).sum(axis=1)
    dans = vrai >= meilleur - 1e-12
    esp = np.where(dans, 1.0 / taille, 0.0)
    fav = dans.astype(float)
    defav = np.where(dans & (taille == 1), 1.0, 0.0)
    return esp, fav, defav, taille


# ---------------------------------------------------------------------------
# 2. Double bootstrap : personnes ET tirages d'items.
#
# NOUVEAU. a2_commun.bootstrap_personnes reechantillonne les personnes seules ; il
# suffit quand le jeu d'items est fixe. Ici le jeu d'items est lui-meme tire au hasard,
# et la dispersion entre tirages est ENORME a faible k (le temoin de relecture-fond
# annoncait 1,323 % avec des tirages entre 0,50 et 3,16 %). Publier un IC qui ignore
# cette source d'incertitude serait publier un intervalle trop etroit d'un facteur
# plusieurs. On reechantillonne donc les deux axes.
# ---------------------------------------------------------------------------

def double_bootstrap(mat_num, mat_den=None, graine=0, n=N_BOOT_DOUBLE):
    """mat_num : (n_tirages_items, n_personnes) d'indicatrices top-1.

    Retourne (point, bas, haut) du taux moyen, ou du RAPPORT taux_num/taux_den si
    mat_den est fourni (le rapport est reechantillonne conjointement, jamais comme un
    quotient de deux IC independants).
    """
    rng = np.random.default_rng([GRAINE, int(graine)])
    r, m = mat_num.shape
    point = float(mat_num.mean())
    if mat_den is not None:
        d0 = float(mat_den.mean())
        point = point / d0 if d0 > 0 else np.nan
    tirs = np.empty(n)
    for b in range(n):
        ir = rng.integers(0, r, r)
        ip = rng.integers(0, m, m)
        a = mat_num[np.ix_(ir, ip)].mean()
        if mat_den is None:
            tirs[b] = a
        else:
            d = mat_den[np.ix_(ir, ip)].mean()
            tirs[b] = a / d if d > 0 else np.nan
    bas, haut = np.nanpercentile(tirs, [2.5, 97.5])
    return point, float(bas), float(haut)


# ---------------------------------------------------------------------------
# 3. Structure d'un sous-ensemble d'items : items effectifs et entropie MESURES.
#
# La matrice complete des V de Cramer entre les 60 items Twin est calculee UNE fois ;
# la moyenne sur le sous-bloc d'un sous-ensemble est, par definition, le V moyen de ce
# sous-ensemble. Aucune extrapolation par la formule n_eff = k/(1+(k-1)V) a partir du
# V des 60 items : c'est le V du sous-ensemble tire qui est utilise.
# ---------------------------------------------------------------------------

def matrice_cramer(humains):
    p = humains.shape[1]
    M = np.full((p, p), np.nan)
    for i in range(p):
        for j in range(i + 1, p):
            M[i, j] = M[j, i] = ARG.cramer_v(humains[:, i], humains[:, j])
    return M


def structure_sous_ensemble(M_cramer, entropies, sel):
    k = len(sel)
    bloc = M_cramer[np.ix_(sel, sel)]
    vs = bloc[np.triu_indices(k, 1)]
    vs = vs[~np.isnan(vs)]
    vbar = float(np.mean(vs)) if len(vs) else 0.0
    neff = k / (1.0 + (k - 1) * vbar)
    h_tot = float(np.sum(entropies[sel]))
    h_moy = h_tot / k
    return {"k": k, "vbar": vbar, "neff": neff, "h_total": h_tot,
            "h_moyen": h_moy, "bits_effectifs": neff * h_moy}


# ---------------------------------------------------------------------------
# 4. Appariement PAR REJET sur l'information effective mesuree.
#
# NOUVEAU, et c'est le coeur du rapport. Apparier "12 items contre 12 items" n'apparie
# rien : les 12 items ANES valent 4,31 items effectifs, 12 items Twin en valent ~6,3.
# On tire donc des sous-ensembles Twin de k variable et on ne GARDE que ceux dont la
# grandeur d'appariement mesuree tombe dans une bande etroite autour de la valeur
# Argyle. Aucune interpolation, aucun modele : des sous-ensembles reellement apparies.
# ---------------------------------------------------------------------------

def tirer_apparie(M_cramer, entropies, critere, cible, tol_rel, rng,
                  n_voulu=N_TIRAGES_ITEMS, k_min=2, k_max=60, essais_max=40000):
    gardes = []
    p = M_cramer.shape[0]
    for _ in range(essais_max):
        if len(gardes) >= n_voulu:
            break
        k = int(rng.integers(k_min, k_max + 1))
        sel = np.sort(rng.choice(p, size=k, replace=False))
        s = structure_sous_ensemble(M_cramer, entropies, sel)
        if abs(s[critere] - cible) <= tol_rel * cible:
            gardes.append((sel, s))
    return gardes


# ---------------------------------------------------------------------------
# 5. Etape "structure" : humains seuls, des deux cotes (A4, A5).
# ---------------------------------------------------------------------------

def structure():
    print("=== TWIN-2K-500, humains seuls ===", flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    h = codes[REF_V4][:, items]
    r = codes[REF_V13][:, items]
    ent = np.array([entropie_item(h[h[:, j] >= 0, j]) for j in range(h.shape[1])])
    mods = np.array([len(np.unique(h[h[:, j] >= 0, j])) for j in range(h.shape[1])])
    print(f"bassin {h.shape[0]}, items communs {len(items)}")
    print(f"manquants sur ces items : {100 * (h < 0).mean():.4f} %")
    print(f"modalites : mediane {np.median(mods):.0f}, min {mods.min()}, max {mods.max()}")
    print(f"entropie totale {ent.sum():.2f} bits, moyenne/item {ent.mean():.3f}")
    ok = (h >= 0) & (r >= 0)
    print(f"accord test-retest humain (vagues 1-3 vs vague 4) : {100*(h[ok]==r[ok]).mean():.2f} %")
    M = matrice_cramer(h)
    tout = np.arange(len(items))
    print("structure des 60 items :", structure_sous_ensemble(M, ent, tout))

    print("\n=== ARGYLE 2023, humains seuls ===", flush=True)
    ha, _, _, noms, demo = ARG.charger()
    plein = (ha >= 0).all(axis=1)
    a = ha[plein]
    ent_a = np.array([entropie_item(a[:, j]) for j in range(a.shape[1])])
    mods_a = np.array([len(np.unique(a[:, j])) for j in range(a.shape[1])])
    print(f"bassin {a.shape[0]} (sur {ha.shape[0]} lignes), items {a.shape[1]}")
    print(f"manquants sur le bassin retenu : {100*(a < 0).mean():.4f} %")
    print(f"lignes ecartees pour au moins un manquant : {100*(1-plein.mean()):.2f} %")
    print(f"modalites : mediane {np.median(mods_a):.0f}, min {mods_a.min()}, max {mods_a.max()}")
    print(f"entropie totale {ent_a.sum():.2f} bits, moyenne/item {ent_a.mean():.3f}")
    vbar, neff, npaires = ARG.items_effectifs(a)
    print(f"V de Cramer moyen {vbar:.4f} ({npaires} paires), items effectifs {neff:.2f}")
    print(f"bits effectifs = {neff * ent_a.mean():.2f}")
    print("accord test-retest humain : NON MESURABLE (l'ANES 2016 ne remesure pas "
          "les memes items sur les memes personnes)")


# ---------------------------------------------------------------------------
# 6. Etape "mesure" : la courbe, les regimes apparies, le controle, A2, A3.
# ---------------------------------------------------------------------------

def mesure():
    lignes = []   # pour le CSV

    def ajouter(**kw):
        lignes.append(kw)

    rng = np.random.default_rng(GRAINE)

    # ---- 6.1 Cote Argyle : les references d'appariement, recalculees ici -------
    print("=== 1. ARGYLE : references d'appariement et controle ===", flush=True)
    ha, jumeaux_a, _, noms_a, demo_a = ARG.charger()
    plein = (ha >= 0).all(axis=1)
    A = ha[plein]
    n_a = A.shape[0]
    ent_a = np.array([entropie_item(A[:, j]) for j in range(A.shape[1])])
    vbar_a, neff_a, _ = ARG.items_effectifs(A)
    bits_eff_a = neff_a * ent_a.mean()
    print(f"bassin {n_a}, 12 items, n_eff = {neff_a:.3f}, H = {ent_a.sum():.2f} bits, "
          f"bits effectifs = {bits_eff_a:.3f}", flush=True)

    dm_a = ARG.baseline_demographique(A, demo_a)
    or_a = ARG.baseline_oracle(A, demo_a)
    ref_a = {}
    for etiq, X in [(f"jumeau GPT-3 (temp. principale)", jumeaux_a["GPT-3 davinci (temp. principale)"]),
                    ("B-demo", dm_a), ("B-oracle", or_a)]:
        x = X[plein] if X.shape[0] == ha.shape[0] else X
        res = ARG.attaquer(x, A, f"argyle|{etiq}")
        ref_a[etiq] = res
        print(f"  {etiq:32s} top-1 {res['top1']*100:7.4f} % "
              f"[{res['top1_bas']*100:.4f};{res['top1_haut']*100:.4f}]", flush=True)
        ajouter(jeu="argyle-2023", regime="12 items bruts (bassin complet)",
                candidat=etiq, k_items=12, neff=round(neff_a, 3),
                bits_effectifs=round(bits_eff_a, 3), bassin=n_a,
                top1=res["top1"], top1_bas=res["top1_bas"], top1_haut=res["top1_haut"],
                hasard=res["hasard"])

    a_passe = ref_a["jumeau GPT-3 (temp. principale)"]["top1_bas"] > ref_a["B-demo"]["top1_haut"]
    print(f"  CONTROLE D'INTERPRETABILITE cote Argyle : "
          f"{'PASSE' if a_passe else 'ECHEC (IC chevauchants)'}", flush=True)
    rapport_a = ref_a["jumeau GPT-3 (temp. principale)"]["top1"] / ref_a["B-demo"]["top1"]
    print(f"  rapport jumeau / B-demo : {rapport_a:.2f}  (non interpretable si ECHEC)",
          flush=True)

    # ---- 6.2 Cote Twin : preparation ------------------------------------------
    print("\n=== 2. TWIN : preparation ===", flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    n_t = pool.shape[0]
    X_twin = codes[CIBLE_TWIN][:, items]
    X_demo = codes[DEMO][:, items]
    X_ret = codes[REF_V13][:, items]                 # plafond humain (A3, cote Twin)
    ent_t = np.array([entropie_item(pool[pool[:, j] >= 0, j]) for j in range(pool.shape[1])])
    print("matrice des V de Cramer (60x60) ...", flush=True)
    M_t = matrice_cramer(pool)
    print(f"bassin {n_t}, {len(items)} items, structure = "
          f"{structure_sous_ensemble(M_t, ent_t, np.arange(len(items)))}", flush=True)

    CANDIDATS = [(CIBLE_TWIN, X_twin), ("Demographics Only", X_demo),
                 ("plafond humain (retest v1-3)", X_ret)]

    # ---- 6.3 La courbe : top-1 en fonction de k, de n_eff, des bits ------------
    print("\n=== 3. TWIN : courbe top-1 vs information ===", flush=True)
    print(f"{'k':>3} {'neff':>6} {'bits_eff':>8} | "
          f"{'jumeau %':>9} {'IC 95 %':>18} | {'demo %':>8} | {'rapport':>7} "
          f"{'IC rapport':>16} | {'plafond %':>9} | {'classe ex aequo':>15}", flush=True)
    for k in KS:
        nrep = 1 if k == len(items) else N_TIRAGES_ITEMS
        sels = ([np.arange(len(items))] if k == len(items)
                else [np.sort(rng.choice(len(items), size=k, replace=False))
                      for _ in range(nrep)])
        st = [structure_sous_ensemble(M_t, ent_t, s) for s in sels]
        mats, tailles = {}, []
        for nom, X in CANDIDATS:
            m = np.empty((nrep, n_t))
            for i, s in enumerate(sels):
                esp, _, _, tl = top1_trois_conventions(X, pool, s)
                m[i] = esp
                if nom == CIBLE_TWIN:
                    tailles.append(np.median(tl))
            mats[nom] = m
        p_j, b_j, h_j = double_bootstrap(mats[CIBLE_TWIN], graine=graine_nom(f"j{k}"))
        p_d, b_d, h_d = double_bootstrap(mats["Demographics Only"], graine=graine_nom(f"d{k}"))
        p_c, b_c, h_c = double_bootstrap(mats["plafond humain (retest v1-3)"],
                                          graine=graine_nom(f"c{k}"))
        p_r, b_r, h_r = double_bootstrap(mats[CIBLE_TWIN], mats["Demographics Only"],
                                          graine=graine_nom(f"r{k}"))
        neff_m = float(np.mean([s["neff"] for s in st]))
        be_m = float(np.mean([s["bits_effectifs"] for s in st]))
        print(f"{k:3d} {neff_m:6.2f} {be_m:8.2f} | {p_j*100:9.4f} "
              f"[{b_j*100:7.4f};{h_j*100:7.4f}] | {p_d*100:8.4f} | {p_r:7.2f} "
              f"[{b_r:6.2f};{h_r:6.2f}] | {p_c*100:9.4f} | {np.mean(tailles):15.1f}",
              flush=True)
        for nom, (p, b, h) in [(CIBLE_TWIN, (p_j, b_j, h_j)),
                               ("Demographics Only", (p_d, b_d, h_d)),
                               ("plafond humain (retest v1-3)", (p_c, b_c, h_c))]:
            ajouter(jeu="twin-2k-500", regime=f"courbe k={k}", candidat=nom, k_items=k,
                    neff=round(neff_m, 3), bits_effectifs=round(be_m, 3), bassin=n_t,
                    top1=p, top1_bas=b, top1_haut=h, hasard=1.0 / n_t)
        ajouter(jeu="twin-2k-500", regime=f"courbe k={k}", candidat="rapport jumeau/demo",
                k_items=k, neff=round(neff_m, 3), bits_effectifs=round(be_m, 3),
                bassin=n_t, top1=p_r, top1_bas=b_r, top1_haut=h_r, hasard=np.nan)

    # ---- 6.4 Les regimes apparies (M1 a M4) -----------------------------------
    print("\n=== 4. TWIN : regimes APPARIES a Argyle (tirage par rejet) ===", flush=True)
    regimes = [
        ("M1 items bruts = 12", None, None, None),
        ("M2 items effectifs = %.2f" % neff_a, "neff", neff_a, 0.03),
        ("M3 bits effectifs = %.2f" % bits_eff_a, "bits_effectifs", bits_eff_a, 0.03),
        ("M4 entropie brute = %.1f bits" % ent_a.sum(), "h_total", float(ent_a.sum()), 0.03),
    ]
    resultats_regimes = {}
    for nom_reg, critere, cible, tol in regimes:
        if critere is None:
            sels = [np.sort(rng.choice(len(items), size=12, replace=False))
                    for _ in range(N_TIRAGES_ITEMS)]
            st = [structure_sous_ensemble(M_t, ent_t, s) for s in sels]
        else:
            gardes = tirer_apparie(M_t, ent_t, critere, cible, tol, rng)
            if len(gardes) < 5:
                print(f"  {nom_reg} : seulement {len(gardes)} sous-ensembles apparies "
                      "trouves -- regime NON mesurable, declare tel quel.", flush=True)
                continue
            sels = [g[0] for g in gardes]
            st = [g[1] for g in gardes]
        nrep = len(sels)
        ks = [len(s) for s in sels]
        mats = {}
        conv = {}
        for nom, X in CANDIDATS:
            me = np.empty((nrep, n_t)); mf = np.empty((nrep, n_t)); md = np.empty((nrep, n_t))
            for i, s in enumerate(sels):
                e, f, d, _ = top1_trois_conventions(X, pool, s)
                me[i], mf[i], md[i] = e, f, d
            mats[nom] = me
            conv[nom] = (float(mf.mean()), float(md.mean()))
        p_j, b_j, h_j = double_bootstrap(mats[CIBLE_TWIN], graine=graine_nom("j" + nom_reg))
        p_d, b_d, h_d = double_bootstrap(mats["Demographics Only"],
                                          graine=graine_nom("d" + nom_reg))
        p_c, b_c, h_c = double_bootstrap(mats["plafond humain (retest v1-3)"],
                                          graine=graine_nom("c" + nom_reg))
        p_r, b_r, h_r = double_bootstrap(mats[CIBLE_TWIN], mats["Demographics Only"],
                                          graine=graine_nom("r" + nom_reg))
        passe = b_j > h_d
        print(f"\n  {nom_reg}  ({nrep} sous-ensembles, k de {min(ks)} a {max(ks)}, "
              f"n_eff mesure {np.mean([s['neff'] for s in st]):.2f}, "
              f"bits eff. {np.mean([s['bits_effectifs'] for s in st]):.2f})", flush=True)
        print(f"    jumeau {CIBLE_TWIN:24s} {p_j*100:8.4f} % [{b_j*100:.4f};{h_j*100:.4f}]"
              f"   (ex aequo favorable {conv[CIBLE_TWIN][0]*100:.4f} %, "
              f"defavorable {conv[CIBLE_TWIN][1]*100:.4f} %)", flush=True)
        print(f"    Demographics Only               {p_d*100:8.4f} % [{b_d*100:.4f};{h_d*100:.4f}]"
              f"   (ex aequo favorable {conv['Demographics Only'][0]*100:.4f} %, "
              f"defavorable {conv['Demographics Only'][1]*100:.4f} %)", flush=True)
        print(f"    rapport sous convention FAVORABLE    "
              f"{conv[CIBLE_TWIN][0]/conv['Demographics Only'][0]:6.2f} ; "
              f"sous convention DEFAVORABLE "
              f"{conv[CIBLE_TWIN][1]/conv['Demographics Only'][1] if conv['Demographics Only'][1] else float('nan'):6.2f}",
              flush=True)
        print(f"    plafond humain (retest)         {p_c*100:8.4f} % [{b_c*100:.4f};{h_c*100:.4f}]",
              flush=True)
        print(f"    rapport jumeau / demo           {p_r:8.2f}   [{b_r:.2f};{h_r:.2f}]",
              flush=True)
        print(f"    CONTROLE D'INTERPRETABILITE     {'PASSE' if passe else 'ECHEC (IC chevauchants)'}",
              flush=True)
        resultats_regimes[nom_reg] = {
            "p_j": p_j, "b_j": b_j, "h_j": h_j, "p_d": p_d, "p_r": p_r,
            "b_r": b_r, "h_r": h_r, "passe": passe, "p_c": p_c,
            "sels": sels, "ks": ks, "st": st,
        }
        for nom, (p, b, h) in [(CIBLE_TWIN, (p_j, b_j, h_j)),
                               ("Demographics Only", (p_d, b_d, h_d)),
                               ("plafond humain (retest v1-3)", (p_c, b_c, h_c)),
                               ("rapport jumeau/demo", (p_r, b_r, h_r))]:
            ajouter(jeu="twin-2k-500", regime=nom_reg, candidat=nom,
                    k_items=float(np.mean(ks)),
                    neff=round(float(np.mean([s["neff"] for s in st])), 3),
                    bits_effectifs=round(float(np.mean([s["bits_effectifs"] for s in st])), 3),
                    bassin=n_t, top1=p, top1_bas=b, top1_haut=h, hasard=1.0 / n_t)

    # ---- 6.4bis Sauvegarde de l'etat, pour que l'etape lourde tourne en avant-plan --
    etat = {}
    for i, (nom_reg, r) in enumerate(resultats_regimes.items()):
        etat[f"nom_{i}"] = np.array([nom_reg])
        for j, s in enumerate(r["sels"][:N_SOUS_ENSEMBLES_LOURDS]):
            etat[f"sel_{i}_{j}"] = s
        etat[f"pj_{i}"] = np.array([r["p_j"]])
        etat[f"pc_{i}"] = np.array([r["p_c"]])
    etat["n_regimes"] = np.array([len(resultats_regimes)])
    os.makedirs(os.path.dirname(ETAT), exist_ok=True)
    np.savez(ETAT, **etat)
    _ecrire_csv(lignes, mode="w")
    print(f"\nEtat sauvegarde. Lancer maintenant :\n"
          f"  .venv/bin/python analyses/c7_residu_trajectoire.py controles", flush=True)


def _ecrire_csv(lignes, mode="w"):
    chemin = os.path.join(SORTIE, "c7-residu-trajectoire.csv")
    champs = ["jeu", "regime", "candidat", "k_items", "neff", "bits_effectifs",
              "bassin", "top1", "top1_bas", "top1_haut", "hasard"]
    with open(chemin, mode, newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs)
        if mode == "w":
            w.writeheader()
        for l in lignes:
            w.writerow({c: l.get(c, "") for c in champs})
    print(f"{len(lignes)} lignes ecrites ({mode}) dans {chemin}", flush=True)


def controles():
    """Etapes 5, 6 et 7 : controle officiel, taille du bassin (A2), plafond (A3).

    Separees de `mesure` uniquement pour que chaque commande tienne en avant-plan ;
    elles relisent les MEMES sous-ensembles apparies, sauvegardes par `mesure`.
    """
    lignes = []

    def ajouter(**kw):
        lignes.append(kw)

    if not os.path.exists(ETAT):
        raise SystemExit("Lancer d'abord : c7_residu_trajectoire.py mesure")
    e = np.load(ETAT, allow_pickle=False)
    n_reg = int(e["n_regimes"][0])
    resultats_regimes = {}
    for i in range(n_reg):
        nom = str(e[f"nom_{i}"][0])
        sels = [e[f"sel_{i}_{j}"] for j in range(N_SOUS_ENSEMBLES_LOURDS)
                if f"sel_{i}_{j}" in e]
        resultats_regimes[nom] = {"sels": sels, "ks": [len(s) for s in sels],
                                  "p_j": float(e[f"pj_{i}"][0]),
                                  "p_c": float(e[f"pc_{i}"][0])}

    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    n_t = pool.shape[0]
    X_twin = codes[CIBLE_TWIN][:, items]
    X_demo = codes[DEMO][:, items]

    ha, jumeaux_a, _, _, demo_a = ARG.charger()
    plein = (ha >= 0).all(axis=1)
    A = ha[plein]
    n_a = A.shape[0]
    ent_a = np.array([entropie_item(A[:, j]) for j in range(A.shape[1])])
    neff_a, bits_eff_a = ARG.items_effectifs(A)[1], None
    bits_eff_a = neff_a * ent_a.mean()
    dm_a = ARG.baseline_demographique(A, demo_a)
    or_a = ARG.baseline_oracle(A, demo_a)
    ref_a = {
        "jumeau": ARG.attaquer(jumeaux_a["GPT-3 davinci (temp. principale)"][plein], A,
                                "argyle|jumeau"),
        "B-oracle": ARG.attaquer(or_a, A, "argyle|oracle"),
    }

    # ---- 6.5 Le controle officiel, sur un echantillon de sous-ensembles ---------
    print("\n=== 5. Controle d'interpretabilite OFFICIEL "
          "(c7_controle_interpretabilite, sous-ensemble par sous-ensemble) ===", flush=True)
    idx_pers = np.arange(n_t)
    for nom_reg, r in resultats_regimes.items():
        passes = 0
        for s in r["sels"]:
            cols = items[s]
            try:
                CTRL.controle_avant_interpretation(idx_pers, cols,
                                                    codes[CIBLE_TWIN][:, cols],
                                                    f"{CIBLE_TWIN} | {nom_reg}", paq=paq)
                passes += 1
            except CTRL.EchecControleInterpretabilite:
                pass
        frac = passes / len(r["sels"])
        print(f"  {nom_reg:34s} {passes}/{len(r['sels'])} sous-ensembles passent "
              f"({frac*100:.0f} %)", flush=True)
        ajouter(jeu="twin-2k-500", regime=nom_reg, candidat="controle : fraction qui passe",
                k_items=float(np.mean(r["ks"])), neff=np.nan, bits_effectifs=np.nan,
                bassin=n_t, top1=frac, top1_bas=np.nan, top1_haut=np.nan, hasard=np.nan)

    # ---- 6.6 A2 : taille du bassin --------------------------------------------
    print("\n=== 6. A2 : taille du bassin ===", flush=True)
    for n_cible in (2058, 1500, 1052):
        # Cote Twin, au regime M2 s'il existe, sinon M1.
        cle = next((c for c in resultats_regimes if c.startswith("M2")), None) or \
              next(iter(resultats_regimes))
        sels = resultats_regimes[cle]["sels"][:N_TIRAGES_BASSIN]
        rj, rd = [], []
        for i, s in enumerate(sels):
            sub = np.sort(np.random.default_rng([GRAINE, n_cible, i]).choice(
                n_t, size=min(n_cible, n_t), replace=False))
            e_j, _, _, _ = top1_trois_conventions(X_twin[sub], pool[sub], s)
            e_d, _, _, _ = top1_trois_conventions(X_demo[sub], pool[sub], s)
            rj.append(e_j.mean()); rd.append(e_d.mean())
        mj, md = float(np.mean(rj)), float(np.mean(rd))
        print(f"  Twin  N={n_cible:5d} ({cle}) : jumeau {mj*100:7.4f} %, "
              f"demo {md*100:7.4f} %, rapport {mj/md if md else np.nan:5.2f}", flush=True)
        ajouter(jeu="twin-2k-500", regime=f"A2 bassin N={n_cible} ({cle})",
                candidat="rapport jumeau/demo", k_items=float(np.mean(
                    [len(s) for s in sels])), neff=np.nan, bits_effectifs=np.nan,
                bassin=min(n_cible, n_t), top1=mj / md if md else np.nan,
                top1_bas=np.nan, top1_haut=np.nan, hasard=1.0 / min(n_cible, n_t))

    for n_cible in (2058, 1500, 1052):
        rj, rd = [], []
        for i in range(N_TIRAGES_BASSIN):
            sub = np.sort(np.random.default_rng([GRAINE, 77, n_cible, i]).choice(
                n_a, size=min(n_cible, n_a), replace=False))
            Asub = A[sub]
            xj = jumeaux_a["GPT-3 davinci (temp. principale)"][plein][sub]
            dsub = ARG.baseline_demographique(Asub, demo_a)
            e_j, _, _, _ = top1_trois_conventions(xj, Asub, np.arange(12))
            e_d, _, _, _ = top1_trois_conventions(dsub, Asub, np.arange(12))
            rj.append(e_j.mean()); rd.append(e_d.mean())
        mj, md = float(np.mean(rj)), float(np.mean(rd))
        print(f"  Argyle N={n_cible:5d} (12 items)    : jumeau {mj*100:7.4f} %, "
              f"demo {md*100:7.4f} %, rapport {mj/md if md else np.nan:5.2f}", flush=True)
        ajouter(jeu="argyle-2023", regime=f"A2 bassin N={n_cible}",
                candidat="rapport jumeau/demo", k_items=12, neff=round(neff_a, 3),
                bits_effectifs=round(bits_eff_a, 3), bassin=min(n_cible, n_a),
                top1=mj / md if md else np.nan, top1_bas=np.nan, top1_haut=np.nan,
                hasard=1.0 / min(n_cible, n_a))

    # ---- 6.7 A3 : plafond, et B-oracle des deux cotes --------------------------
    print("\n=== 7. A3 : plafond de fiabilite humaine et B-oracle ===", flush=True)
    print("  Twin : accord test-retest humain mesurable ; ANES 2016 : NON MESURABLE "
          "(pas de remesure des memes items).", flush=True)
    # Le jumeau est RE-mesure sur EXACTEMENT les memes sous-ensembles que l'oracle et
    # avec la MEME convention d'ex aequo : comparer un jumeau moyenne sur 30 tirages a
    # un oracle moyenne sur 5 melangerait deux echantillons d'items et fausserait le
    # rapport (l'erreur a ete faite une fois dans ce script, elle est corrigee ici).
    for nom_reg, r in resultats_regimes.items():
        sels = r["sels"][:N_TIRAGES_BASSIN]
        ors, jus, rets = [], [], []
        for s in sels:
            # _imputer_loo rend deja une matrice restreinte aux colonnes du
            # sous-ensemble : l'attaque se fait donc sur arange(k), pas sur s.
            oracle = ARG._imputer_loo(pool[:, s], lambda j: np.ones(len(s), dtype=bool))
            e, _, _, _ = top1_trois_conventions(oracle, pool[:, s], np.arange(len(s)))
            ors.append(e.mean())
            ej, _, _, _ = top1_trois_conventions(X_twin, pool, s)
            jus.append(ej.mean())
            er, _, _, _ = top1_trois_conventions(codes[REF_V13][:, items], pool, s)
            rets.append(er.mean())
        mo, mj, mr = float(np.mean(ors)), float(np.mean(jus)), float(np.mean(rets))
        print(f"  {nom_reg:34s} jumeau {mj*100:7.4f} % ; B-oracle {mo*100:7.4f} % ; "
              f"plafond retest {mr*100:7.4f} % ; jumeau/oracle = "
              f"{mj/mo if mo else np.nan:5.2f} ; jumeau/plafond = "
              f"{mj/mr if mr else np.nan:5.2f}", flush=True)
        ajouter(jeu="twin-2k-500", regime=nom_reg + " (memes sous-ensembles)",
                candidat="B-oracle", k_items=float(np.mean(r["ks"])), neff=np.nan,
                bits_effectifs=np.nan, bassin=n_t, top1=mo, top1_bas=np.nan,
                top1_haut=np.nan, hasard=1.0 / n_t)
        ajouter(jeu="twin-2k-500", regime=nom_reg + " (memes sous-ensembles)",
                candidat="rapport jumeau/B-oracle", k_items=float(np.mean(r["ks"])),
                neff=np.nan, bits_effectifs=np.nan, bassin=n_t,
                top1=mj / mo if mo else np.nan, top1_bas=np.nan, top1_haut=np.nan,
                hasard=np.nan)
    # Cote Argyle, meme convention d'ex aequo en forme fermee que ci-dessus.
    xj_a = jumeaux_a["GPT-3 davinci (temp. principale)"][plein]
    ej, _, _, _ = top1_trois_conventions(xj_a, A, np.arange(12))
    eo, _, _, _ = top1_trois_conventions(or_a, A, np.arange(12))
    ed, _, _, _ = top1_trois_conventions(dm_a, A, np.arange(12))
    j_a, o_a, d_a = float(ej.mean()), float(eo.mean()), float(ed.mean())
    print(f"  {'Argyle 12 items (bassin complet)':34s} jumeau {j_a*100:7.4f} % ; "
          f"B-oracle {o_a*100:7.4f} % ; B-demo {d_a*100:7.4f} % ; jumeau/oracle = "
          f"{j_a/o_a if o_a else np.nan:5.2f} ; jumeau/demo = "
          f"{j_a/d_a if d_a else np.nan:5.2f}", flush=True)
    ajouter(jeu="argyle-2023", regime="12 items bruts (meme convention ex aequo)",
            candidat="rapport jumeau/B-oracle", k_items=12, neff=round(neff_a, 3),
            bits_effectifs=round(bits_eff_a, 3), bassin=n_a,
            top1=j_a / o_a if o_a else np.nan, top1_bas=np.nan, top1_haut=np.nan,
            hasard=np.nan)
    ajouter(jeu="argyle-2023", regime="12 items bruts (bassin complet)",
            candidat="B-oracle", k_items=12, neff=round(neff_a, 3),
            bits_effectifs=round(bits_eff_a, 3), bassin=n_a, top1=o_a,
            top1_bas=ref_a["B-oracle"]["top1_bas"],
            top1_haut=ref_a["B-oracle"]["top1_haut"], hasard=1.0 / n_a)

    _ecrire_csv(lignes, mode="a")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "mesure"
    if cmd == "structure":
        structure()
    elif cmd == "controles":
        controles()
    elif cmd == "mesure":
        mesure()
    else:
        raise SystemExit("usage : c7_residu_trajectoire.py [structure|mesure|controles]")
