"""
c7_argyle : la reidentification tient-elle sur un TROISIEME jeu reel, independant ?

===========================================================================
PREENREGISTREMENT : resultats/c7-argyle-preenregistrement.md, ecrit AVANT toute
mesure d'attaque. La partie "preparation" de ce script (etape 1, humains seuls :
taille du bassin, V de Cramer moyen, items effectifs) alimente la PREDICTION et
tourne donc avant le preenregistrement ; elle ne touche AUCUNE colonne _gpt3.
L'etape 2 (controle) et l'etape 3 (attaque) ne tournent qu'apres.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Argyle, Busby, Fulda, Gubler,
Rytting & Wingate 2023, Harvard Dataverse doi:10.7910/DVN/JPV20K, licence CC0).
Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identifiant ANES (V160001_orig)
d'une personne retrouvee, ni aucune liste d'appariements individuels. Seuls des taux
agreges sortent dans resultats/c7-argyle.csv.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  c7_reidentification.rangs_attaque   l'attaque (rang, top1, top10), ex aequo melanges
  c7_reidentification.resume_taux     l'IC 95 % bootstrap sur les personnes
  c7_reidentification.graine_nom      graine stable par nom
  c7_reidentification.N_BOOTSTRAP     2 000 tirages
  a2_commun.distance_hamming          la distance de Hamming masquee (via rangs_attaque)
  a2_commun.bootstrap_personnes       l'IC (via resume_taux)
  c7_bits.rangs_tous_tirages          les rangs non moyennes, pour les bits d'identite
  c7_bits.bits_et_ic                  les bits d'identite (bornage dyadique + Miller-Madow)
  c7_bits.entropie_item               l'entropie d'un item (Miller-Madow)

CE QUI EST NOUVEAU ICI, et rien d'autre : la lecture et le recodage du jeu Argyle
(mise des reponses humaines et des reponses GPT-3 sur une meme echelle de codes,
crosswalk verifie dans le code de generation publie par les auteurs), la baseline
demographique recalculee SUR LE BASSIN REELLEMENT ATTAQUE, et le controle
d'interpretabilite transpose a ce jeu (meme regle de decision que
c7_controle_interpretabilite : IC bootstrap 95 % non chevauchants).

POURQUOI LE CONTROLE N'EST PAS APPELE DIRECTEMENT.
analyses/c7_controle_interpretabilite.controle_avant_interpretation est cable sur
Twin-2K-500 (t1_commun.charger, REF_V4, DEMO) : il ne peut pas s'appliquer a un jeu
qui n'est pas Twin. La REGLE DE DECISION y est reprise a l'identique et son garde-fou
central est preserve : la fonction de controle ci-dessous ne prend JAMAIS de valeur de
baseline en argument, seulement les indices qui definissent le bassin, et elle
recalcule la baseline elle-meme sur ces memes indices.

Aucun appel de modele de langage, aucune depense. Lecture seule sur data/argyle-2023/.
Usage :
  .venv/bin/python analyses/c7_argyle.py preparation   # etape 1, humains seuls
  .venv/bin/python analyses/c7_argyle.py mesure        # etapes 2 et 3
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

from a2_commun import distance_hamming                              # noqa: E402
from c7_reidentification import (                                    # noqa: E402
    rangs_attaque, resume_taux, graine_nom,
)
from c7_bits import rangs_tous_tirages, bits_et_ic, entropie_item    # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOSSIER = os.path.join(RACINE, "data", "argyle-2023")
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260912
N_REPETITIONS = 20          # tirages de sous-bassin, comme c7_echelle
N_ANCRE = 1052              # bassin de l'ancre Stanford, pour comparer sans extrapoler

# Les trois versions de jumeaux GPT-3 publiees par l'equipe Argyle (meme personnes).
FICHIERS = {
    "GPT-3 davinci (temp. principale)": "anesgpt3_task3.csv",
    "GPT-3 davinci (temp. 0.01)": "anesgpt3_task3_temp001.csv",
    "GPT-3 davinci (temp. 1.0)": "anesgpt3_task3_temp10.csv",
}

# ---------------------------------------------------------------------------
# 1. Crosswalk humain <-> jumeau.
#
# Verifie ligne a ligne dans GPT3_OtherModels_DataGenerationCode.pdf, section 1.10
# ("Study 3"), dictionnaire `questions` : pour chaque variable, les CLES du champ
# 'vals' sont les codes ANES et c'est cette cle qui est ecrite dans la colonne _gpt3
# (`coded_response = valnum`). Les deux cotes sont donc deja sur la meme echelle,
# SAUF education (le 'vals' de l'education est plusieurs-vers-un : "high school" pour
# V161270 1 a 9, "some college" pour 10 a 12, etc. ; strcompare retient le DERNIER
# code correspondant, d'ou les seules valeurs 9, 12, 13, 16 observees cote GPT-3) et
# votechoice (ANES 3/4/5 = "someone else", code 42 cote GPT-3).
#
# 'demo' marque les quatre variables demographiques, celles dont dispose la baseline.
# ---------------------------------------------------------------------------
ITEMS = [
    # (nom, colonne humaine, colonne jumelle, codes humains valides, demographique ?)
    ("gender",             "V161342",  "gender_gpt3",             (1, 2),             True),
    ("race",               "V161310x", "race_gpt3",               (1, 2, 3, 5),       True),
    ("age",                "V161267",  "age_gpt3",                None,               True),
    ("education",          "V161270",  "education_gpt3",          None,               True),
    ("church_goer",        "V161244",  "church_goer_gpt3",        (1, 2),             False),
    ("patriotism",         "V162125x", "patriotism_gpt3",         (1, 2, 3, 4, 5, 6, 7), False),
    ("discuss_politics",   "V162174",  "discuss_politics_gpt3",   (1, 2),             False),
    ("political_interest", "V162256",  "political_interest_gpt3", (1, 2, 3, 4),       False),
    ("ideology",           "V161126",  "ideology_gpt3",           (1, 2, 3, 4, 5, 6, 7), False),
    ("pid7",               "V161158x", "pid7_gpt3",               (1, 2, 3, 4, 5, 6, 7), False),
    ("voted_2016",         "V162031x", "voted_2016_gpt3",         (0, 1),             False),
    ("votechoice_2016",    "V162062x", "votechoice_2016_gpt3",    None,               False),
]

BANDES_EDUCATION = [(1, 9, 0), (10, 12, 1), (13, 13, 2), (14, 16, 3)]
EDUCATION_GPT3 = {9: 0, 12: 1, 13: 2, 16: 3}
VOTECHOICE_HUMAIN = {1: 1, 2: 2, 3: 3, 4: 3, 5: 3}
VOTECHOICE_GPT3 = {1: 1, 2: 2, 42: 3}


def _recoder_humain(nom, serie, codes_valides):
    """Reponses humaines -> codes communs ; -1 pour manquant ou hors champ."""
    v = serie.to_numpy()
    out = np.full(len(v), -1, dtype=np.int64)
    if nom == "education":
        for bas, haut, code in BANDES_EDUCATION:
            out[(v >= bas) & (v <= haut)] = code
    elif nom == "votechoice_2016":
        for brut, code in VOTECHOICE_HUMAIN.items():
            out[v == brut] = code
    elif nom == "age":
        ok = (v > 0) & (v < 120)
        out[ok] = v[ok]
    else:
        for code in codes_valides:
            out[v == code] = code
    return out


def _recoder_jumeau(nom, serie):
    """Reponses GPT-3 -> memes codes communs ; -1 pour non parse (deja -1 a la source)."""
    v = serie.to_numpy()
    out = np.full(len(v), -1, dtype=np.int64)
    if nom == "education":
        for brut, code in EDUCATION_GPT3.items():
            out[v == brut] = code
    elif nom == "votechoice_2016":
        for brut, code in VOTECHOICE_GPT3.items():
            out[v == brut] = code
    elif nom == "age":
        ok = (v > 0) & (v < 120)
        out[ok] = v[ok]
    else:
        ok = v >= 0
        out[ok] = v[ok]
    return out


def charger():
    """(humains, {nom_jumeau: matrice}, identifiants, noms d'items, masque demographique).

    Les identifiants ne servent QU'A verifier l'alignement ligne a ligne entre les trois
    fichiers ; ils ne sont jamais ecrits ni imprimes individuellement.
    """
    principal = pd.read_csv(os.path.join(DOSSIER, "anesgpt3_task3.csv"))
    ids = principal["V160001_orig"].to_numpy()
    if len(np.unique(ids)) != len(ids):
        raise RuntimeError("V160001_orig n'est pas unique : l'appariement serait ambigu.")

    noms = [it[0] for it in ITEMS]
    demo = np.array([it[4] for it in ITEMS], dtype=bool)
    humains = np.stack(
        [_recoder_humain(nom, principal[col_h], codes)
         for nom, col_h, _, codes, _ in ITEMS], axis=1)

    jumeaux = {}
    for etiquette, fichier in FICHIERS.items():
        d = pd.read_csv(os.path.join(DOSSIER, fichier))
        if not np.array_equal(d["V160001_orig"].to_numpy(), ids):
            raise RuntimeError(
                f"{fichier} n'est pas aligne ligne a ligne sur anesgpt3_task3.csv : "
                "l'appariement individuel ne peut pas etre suppose.")
        jumeaux[etiquette] = np.stack(
            [_recoder_jumeau(nom, d[col_g]) for nom, _, col_g, _, _ in ITEMS], axis=1)

    return humains, jumeaux, ids, noms, demo


# ---------------------------------------------------------------------------
# 2. Baseline demographique, TOUJOURS recalculee sur le bassin reellement attaque.
# ---------------------------------------------------------------------------

def _imputer_loo(humains, contexte_pour, k=10):
    """Imputeur statistique laisse-un-item-dehors, exactement le protocole d'Argyle.

    Pour CHAQUE item j, l'item j est retire du contexte, les k plus proches voisins
    sont cherches sur le contexte restant (meme distance de Hamming que l'attaque,
    la personne elle-meme toujours exclue), et j est impute par leur mode. Aucun
    item n'est donc jamais recopie depuis la verite de la personne attaquee : la
    tautologie est exclue par construction, du cote de la baseline comme du cote du
    jumeau GPT-3 (qui, lui aussi, ne voyait jamais la reponse qu'on lui demandait).

    contexte_pour(j) -> masque booleen des colonnes visibles pour predire j.

    Entree : le bassin DEJA tranche. Aucun parametre de baseline n'est accepte
    d'ailleurs : la baseline est un calcul sur ces lignes-la et rien d'autre.
    """
    n, p = humains.shape
    sortie = np.full((n, p), -1, dtype=np.int64)
    for j in range(p):
        ctx = contexte_pour(j)
        ctx = ctx & (np.arange(p) != j)
        if not ctx.any():
            continue
        dist = distance_hamming(humains[:, ctx], humains[:, ctx])
        np.fill_diagonal(dist, np.inf)
        voisins = np.argsort(dist, axis=1, kind="stable")[:, :k]
        col = humains[:, j]
        vois_vals = col[voisins]                       # (n, k)
        for i in range(n):
            vals = vois_vals[i][vois_vals[i] >= 0]
            if len(vals):
                u, c = np.unique(vals, return_counts=True)
                sortie[i, j] = u[np.argmax(c)]
    return sortie


def baseline_demographique(humains, demo, k=10):
    """B-demo : l'attaquant qui ne connait QUE les quatre variables demographiques.

    Analogue direct de "Demographics Only - GPT4.1-mini" de Twin : son information
    se limite au profil demographique. C'est la baseline du CONTROLE.
    """
    return _imputer_loo(humains, lambda j: demo.copy(), k=k)


def baseline_oracle(humains, demo, k=10):
    """B-oracle : le comparateur apparie au confondu, preenregistre.

    Le jumeau GPT-3 d'Argyle n'est pas un jumeau "persona" : pour chaque item, il a
    lu les ONZE VRAIES reponses de la personne aux autres items (entretien
    laisse-un-dehors, cf. build_interview / human_readable_omit dans le code de
    generation des auteurs). B-oracle est l'imputeur statistique qui dispose
    exactement de la meme information. Il repond a la seule question qui reste
    interpretable dans ce format : GPT-3 apporte-t-il quelque chose qu'un
    appariement au plus proche voisin sur les memes 11 reponses n'apporte pas ?
    """
    tous = np.ones(humains.shape[1], dtype=bool)
    return _imputer_loo(humains, lambda j: tous.copy(), k=k)


# ---------------------------------------------------------------------------
# 3. Attaque + IC, exactement les fonctions de C7.
# ---------------------------------------------------------------------------

def attaquer(x, humains, nom):
    """top-1, top-10, rang median du jumeau x contre le bassin humain (meme pool)."""
    couverts = np.flatnonzero((x >= 0).any(axis=1))
    if len(couverts) < 5:
        return None
    rng = np.random.default_rng([GRAINE, graine_nom(nom), 7])
    rang, t1, t10 = rangs_attaque(x[couverts], humains, couverts, rng)
    m1, b1, h1 = resume_taux(t1, [GRAINE, graine_nom(nom), 1])
    m10, b10, h10 = resume_taux(t10, [GRAINE, graine_nom(nom), 2])
    return {"n": len(couverts), "n_pool": humains.shape[0],
            "top1": m1, "top1_bas": b1, "top1_haut": h1,
            "top10": m10, "top10_bas": b10, "top10_haut": h10,
            "rang_median": float(np.median(rang)),
            "hasard": 1.0 / humains.shape[0]}


class EchecControleInterpretabilite(RuntimeError):
    """Meme semantique que dans c7_controle_interpretabilite : ne jamais attraper pour
    continuer a interpreter. Le jumeau ne porte pas de personne demontrable."""


def controle_avant_interpretation(humains_bassin, demo, codes_candidat, nom):
    """Regle de decision reprise a l'identique de c7_controle_interpretabilite :
    IC bootstrap 95 % du candidat STRICTEMENT au-dessus de l'IC de la baseline
    demographique recalculee sur CE bassin. Aucune valeur de baseline n'est acceptee
    en argument."""
    if codes_candidat.shape != humains_bassin.shape:
        raise ValueError("candidat et bassin ne sont pas alignes.")
    r_c = attaquer(codes_candidat, humains_bassin, f"fid|{nom}")
    r_b = attaquer(baseline_demographique(humains_bassin, demo), humains_bassin,
                   "baseline|demo")
    if r_c is None or r_b is None:
        raise EchecControleInterpretabilite(f"{nom} : couverture insuffisante.")
    passe = bool(r_c["top1_bas"] > r_b["top1_haut"])
    diag = {"candidat": nom, "bassin": humains_bassin.shape[0],
            "n_items": humains_bassin.shape[1],
            "candidat_top1": r_c["top1"], "candidat_ic": (r_c["top1_bas"], r_c["top1_haut"]),
            "baseline_top1": r_b["top1"], "baseline_ic": (r_b["top1_bas"], r_b["top1_haut"]),
            "hasard": r_c["hasard"], "passe": passe}
    if not passe:
        exc = EchecControleInterpretabilite(
            f"'{nom}' NE PASSE PAS le controle de fidelite prealable.\n"
            f"  bassin : {diag['bassin']} personnes, {diag['n_items']} items\n"
            f"  top-1 candidat : {diag['candidat_top1']*100:.2f} % "
            f"[{diag['candidat_ic'][0]*100:.2f};{diag['candidat_ic'][1]*100:.2f}]\n"
            f"  baseline demographique (meme bassin, recalculee ici) : "
            f"{diag['baseline_top1']*100:.2f} % "
            f"[{diag['baseline_ic'][0]*100:.2f};{diag['baseline_ic'][1]*100:.2f}]")
        exc.diagnostic = diag
        raise exc
    return diag


# ---------------------------------------------------------------------------
# 4. Dependance entre items : V de Cramer moyen et items effectifs (formule H2 de
#    resultats/c7-anomalie-park-2026-09-12.md, reprise telle quelle).
# ---------------------------------------------------------------------------

def cramer_v(a, b, n_min=20):
    ok = (a >= 0) & (b >= 0)
    if ok.sum() < n_min:
        return np.nan
    x, y = a[ok], b[ok]
    ux, uy = np.unique(x), np.unique(y)
    if len(ux) < 2 or len(uy) < 2:
        return np.nan
    tab = np.zeros((len(ux), len(uy)))
    ix = {v: i for i, v in enumerate(ux)}
    iy = {v: i for i, v in enumerate(uy)}
    for xi, yi in zip(x, y):
        tab[ix[xi], iy[yi]] += 1
    n = tab.sum()
    att = np.outer(tab.sum(axis=1), tab.sum(axis=0)) / n
    with np.errstate(invalid="ignore", divide="ignore"):
        chi2 = np.nansum(np.where(att > 0, (tab - att) ** 2 / att, 0.0))
    return float(np.sqrt((chi2 / n) / (min(len(ux), len(uy)) - 1)))


def items_effectifs(humains):
    p = humains.shape[1]
    vs = [cramer_v(humains[:, i], humains[:, j])
          for i in range(p) for j in range(i + 1, p)]
    vs = [v for v in vs if not np.isnan(v)]
    vbar = float(np.mean(vs))
    return vbar, p / (1.0 + (p - 1) * vbar), len(vs)


# ---------------------------------------------------------------------------
# Etape 1 : preparation (humains seuls). Alimente la PREDICTION preenregistree.
# ---------------------------------------------------------------------------

def preparation():
    humains, jumeaux, ids, noms, demo = charger()
    print(f"fichier principal : {humains.shape[0]} lignes, {len(noms)} items apparies")
    print(f"identifiants ANES uniques : {len(np.unique(ids))}")
    print(f"les 3 fichiers de jumeaux sont alignes ligne a ligne sur V160001_orig : oui")

    plein = (humains >= 0).all(axis=1)
    print(f"\npersonnes valides sur les 12 items humains : {plein.sum()}")
    for j, nom in enumerate(noms):
        print(f"  {nom:20s} valides={int((humains[:, j] >= 0).sum()):5d} "
              f"modalites={len(np.unique(humains[humains[:, j] >= 0, j])):3d} "
              f"entropie={entropie_item(humains[humains[:, j] >= 0, j]):.2f} bits")

    h = humains[plein]
    vbar, neff, npaires = items_effectifs(h)
    ent = float(sum(entropie_item(h[:, j]) for j in range(h.shape[1])))
    print(f"\n--- entrees de la prediction (humains seuls, aucune colonne _gpt3 lue) ---")
    print(f"bassin complet          : {h.shape[0]}")
    print(f"paires d'items utilisees: {npaires}")
    print(f"V de Cramer moyen       : {vbar:.4f}")
    print(f"items effectifs (12)    : {neff:.2f}")
    print(f"entropie humaine totale : {ent:.2f} bits")


# ---------------------------------------------------------------------------
# Etapes 2 et 3 : controle puis mesure. Ne tournent qu'apres le preenregistrement.
# ---------------------------------------------------------------------------

def mesure():
    humains, jumeaux, ids, noms, demo = charger()
    plein = (humains >= 0).all(axis=1)
    h = humains[plein]
    n = h.shape[0]
    print(f"bassin complet : {n} personnes, {len(noms)} items\n")

    lignes = []

    # --- Etape 2 : CONTROLE D'INTERPRETABILITE, avant toute interpretation ---
    print("=== Controle d'interpretabilite (bassin complet) ===")
    controle = {}
    for etiquette, X in jumeaux.items():
        x = X[plein]
        try:
            d = controle_avant_interpretation(h, demo, x, etiquette)
            print(f"  {etiquette:34s} PASSE  top-1={d['candidat_top1']*100:.2f} % "
                  f"[{d['candidat_ic'][0]*100:.2f};{d['candidat_ic'][1]*100:.2f}]  vs "
                  f"baseline {d['baseline_top1']*100:.2f} % "
                  f"[{d['baseline_ic'][0]*100:.2f};{d['baseline_ic'][1]*100:.2f}]")
            controle[etiquette] = d
        except EchecControleInterpretabilite as exc:
            print(f"  {etiquette:34s} ECHEC\n" +
                  "\n".join("      " + l for l in str(exc).splitlines()))
            controle[etiquette] = getattr(exc, "diagnostic", {"passe": False})

    if not any(d.get("passe") for d in controle.values()):
        print("\nAUCUN jumeau ne passe le controle : l'analyse d'interpretation s'arrete "
              "ici, conformement au preenregistrement. Seuls des DESCRIPTIFS sont encore "
              "ecrits (bits, accord par item, sensibilite au sous-ensemble d'items) : ils "
              "documentent l'echec, ils n'interpretent aucun contraste.")
        lignes = [{"etape": "controle", "candidat": k,
                   **{kk: vv for kk, vv in v.items() if kk != "candidat"}}
                  for k, v in controle.items()]

        ent = float(sum(entropie_item(h[:, j]) for j in range(h.shape[1])))
        fixes = {"B-demo (demographies seules, ce bassin)":
                 baseline_demographique(h, demo),
                 "B-oracle (11 vraies reponses, ce bassin)": baseline_oracle(h, demo)}
        for etiquette, X in list(jumeaux.items()) + [(e, None) for e in fixes]:
            x = fixes[etiquette] if X is None else X[plein]
            r = attaquer(x, h, f"desc|{etiquette}")
            couverts = np.flatnonzero((x >= 0).any(axis=1))
            rng = np.random.default_rng([GRAINE, graine_nom(etiquette), 11])
            rangs = rangs_tous_tirages(1.0 - distance_hamming(x[couverts], h),
                                       couverts, rng)
            bits, bbas, bhaut = bits_et_ic(
                rangs, n, [GRAINE, graine_nom(etiquette), 12])[:3]
            accord = float(np.mean([(x[x[:, j] >= 0, j] == h[x[:, j] >= 0, j]).mean()
                                    for j in range(h.shape[1])]))
            lignes.append({"etape": "descriptif", "candidat": etiquette, "n_pool": n,
                           "n_items": h.shape[1], "top1": r["top1"],
                           "top1_bas": r["top1_bas"], "top1_haut": r["top1_haut"],
                           "top10": r["top10"], "rang_median": r["rang_median"],
                           "hasard": r["hasard"], "bits": bits, "bits_bas": bbas,
                           "bits_haut": bhaut, "bits_normalises": bits / ent,
                           "accord_moyen_par_item": accord})
            print(f"  {etiquette:42s} bits={bits:.3f} [{bbas:.3f};{bhaut:.3f}] "
                  f"bits_norm={bits/ent:.4f} accord/item={accord*100:.1f} %")

        # Sensibilite declaree : l'echec tient-il a l'age (73 modalites, appariement a
        # l'annee exacte) ? Sous-ensembles d'items, meme regle, meme bassin.
        print("\n--- sensibilite au sous-ensemble d'items (post hoc, declare) ---")
        sous = [("11 items, sans age", np.array([x != "age" for x in noms])),
                ("8 items d'attitude seuls", ~demo)]
        for etiq, garder in sous:
            hs, ds = h[:, garder], demo[garder]
            rb = attaquer(baseline_demographique(hs, ds), hs, f"s|b|{etiq}") \
                if ds.any() else None
            for e, X in jumeaux.items():
                r = attaquer(X[plein][:, garder], hs, f"s|{e}|{etiq}")
                passe = bool(rb is not None and r["top1_bas"] > rb["top1_haut"])
                lignes.append({"etape": f"sensibilite:{etiq}", "candidat": e,
                               "n_pool": n, "n_items": int(garder.sum()),
                               "top1": r["top1"], "top1_bas": r["top1_bas"],
                               "top1_haut": r["top1_haut"], "top10": r["top10"],
                               "rang_median": r["rang_median"], "hasard": r["hasard"],
                               "baseline_top1": rb["top1"] if rb else np.nan,
                               "controle_passe": passe})
                print(f"  [{etiq}] {e:34s} top1={r['top1']*100:.2f} % "
                      f"[{r['top1_bas']*100:.2f};{r['top1_haut']*100:.2f}] "
                      f"{'PASSE' if passe else 'ECHEC'}")
            if rb:
                lignes.append({"etape": f"sensibilite:{etiq}",
                               "candidat": "B-demo", "n_pool": n,
                               "n_items": int(garder.sum()), "top1": rb["top1"],
                               "top1_bas": rb["top1_bas"], "top1_haut": rb["top1_haut"]})
            ro = attaquer(baseline_oracle(hs, ds), hs, f"s|o|{etiq}")
            lignes.append({"etape": f"sensibilite:{etiq}", "candidat": "B-oracle",
                           "n_pool": n, "n_items": int(garder.sum()),
                           "top1": ro["top1"], "top1_bas": ro["top1_bas"],
                           "top1_haut": ro["top1_haut"]})
            print(f"  [{etiq}] {'B-oracle':34s} top1={ro['top1']*100:.2f} % "
                  f"[{ro['top1_bas']*100:.2f};{ro['top1_haut']*100:.2f}]")

        vbar, neff, _ = items_effectifs(h)
        lignes.append({"etape": "structure", "candidat": "items", "n_pool": n,
                       "n_items": h.shape[1], "cramer_v_moyen": vbar,
                       "items_effectifs": neff, "entropie_humaine_bits": ent})
        pd.DataFrame(lignes).to_csv(os.path.join(SORTIE, "c7-argyle.csv"), index=False)
        print("\necrit : resultats/c7-argyle.csv")
        return

    # --- Etape 3 : mesure, bassin complet puis bassin d'ancre N=1052 ---
    b_demo = baseline_demographique(h, demo)
    b_oracle = baseline_oracle(h, demo)
    fixes = {"B-demo (demographies seules, ce bassin)": b_demo,
             "B-oracle (11 vraies reponses, ce bassin)": b_oracle}
    cibles = dict(jumeaux)
    print("\n=== Attaque, bassin complet ===")
    for etiquette, X in list(cibles.items()) + [(e, None) for e in fixes]:
        x = fixes[etiquette] if X is None else X[plein]
        r = attaquer(x, h, f"complet|{etiquette}")
        rng = np.random.default_rng([GRAINE, graine_nom(etiquette), 11])
        couverts = np.flatnonzero((x >= 0).any(axis=1))
        accord = 1.0 - distance_hamming(x[couverts], h)
        rangs = rangs_tous_tirages(accord, couverts, rng)
        bits, bbas, bhaut, _ = bits_et_ic(rangs, n, [GRAINE, graine_nom(etiquette), 12])
        ent = float(sum(entropie_item(h[:, j]) for j in range(h.shape[1])))
        lignes.append({"bassin": "complet", "n_pool": n, "candidat": etiquette,
                       "n_attaques": r["n"], "top1": r["top1"],
                       "top1_bas": r["top1_bas"], "top1_haut": r["top1_haut"],
                       "top10": r["top10"], "top10_bas": r["top10_bas"],
                       "top10_haut": r["top10_haut"],
                       "rang_median": r["rang_median"], "hasard": r["hasard"],
                       "bits": bits, "bits_bas": bbas, "bits_haut": bhaut,
                       "bits_normalises": bits / ent,
                       "bits_par_item": bits / h.shape[1]})
        print(f"  {etiquette:34s} top-1={r['top1']*100:.2f} % "
              f"[{r['top1_bas']*100:.2f};{r['top1_haut']*100:.2f}]  "
              f"top-10={r['top10']*100:.2f} %  rang_med={r['rang_median']:.0f}/{n}  "
              f"bits={bits:.2f}  bits_norm={bits/ent:.4f}")

    print(f"\n=== Attaque, bassin ramene a N={N_ANCRE} ({N_REPETITIONS} tirages) ===")
    rng_ech = np.random.default_rng([GRAINE, 77])
    tirages = [rng_ech.choice(n, size=N_ANCRE, replace=False)
               for _ in range(N_REPETITIONS)]
    constructeurs = {"B-demo (demographies seules, ce bassin)": baseline_demographique,
                     "B-oracle (11 vraies reponses, ce bassin)": baseline_oracle}
    for etiquette, X in list(cibles.items()) + [(e, None) for e in fixes]:
        t1s, t10s, rangs_med = [], [], []
        for ech in tirages:
            hb = h[ech]
            xb = constructeurs[etiquette](hb, demo) if X is None else X[plein][ech]
            r = attaquer(xb, hb, f"ancre|{etiquette}")
            t1s.append(r["top1"]); t10s.append(r["top10"]); rangs_med.append(r["rang_median"])
        m1, b1, h1 = resume_taux(np.array(t1s), [GRAINE, graine_nom(etiquette), 21])
        m10, b10, h10 = resume_taux(np.array(t10s), [GRAINE, graine_nom(etiquette), 22])
        lignes.append({"bassin": f"ancre N={N_ANCRE}", "n_pool": N_ANCRE,
                       "candidat": etiquette, "n_attaques": N_ANCRE,
                       "top1": m1, "top1_bas": b1, "top1_haut": h1,
                       "top10": m10, "top10_bas": b10, "top10_haut": h10,
                       "rang_median": float(np.median(rangs_med)),
                       "hasard": 1.0 / N_ANCRE})
        print(f"  {etiquette:34s} top-1={m1*100:.2f} % [{b1*100:.2f};{h1*100:.2f}]  "
              f"top-10={m10*100:.2f} %  rang_med={np.median(rangs_med):.0f}/{N_ANCRE}")

    for etiquette, d in controle.items():
        lignes.append({"bassin": "controle", "candidat": etiquette,
                       "n_pool": d.get("bassin"), "top1": d.get("candidat_top1"),
                       "top1_bas": d.get("candidat_ic", (np.nan, np.nan))[0],
                       "top1_haut": d.get("candidat_ic", (np.nan, np.nan))[1],
                       "controle_passe": d.get("passe")})

    vbar, neff, _ = items_effectifs(h)
    lignes.append({"bassin": "structure", "candidat": "items", "n_pool": n,
                   "cramer_v_moyen": vbar, "items_effectifs": neff,
                   "n_items": h.shape[1]})

    pd.DataFrame(lignes).to_csv(os.path.join(SORTIE, "c7-argyle.csv"), index=False)
    print(f"\necrit : resultats/c7-argyle.csv")


if __name__ == "__main__":
    quoi = sys.argv[1] if len(sys.argv) > 1 else "preparation"
    if quoi == "preparation":
        preparation()
    elif quoi == "mesure":
        mesure()
    else:
        raise SystemExit("usage : c7_argyle.py [preparation|mesure]")
