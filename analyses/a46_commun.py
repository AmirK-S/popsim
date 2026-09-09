"""
a46_commun : briques partagees du volet « croyance humaine de second ordre ».

Statut : script d'analyse jetable. Aucun appel de modele de langage. Lecture seule sur
data/traces/. Aucun fichier existant du depot n'est modifie.

Ce module porte trois choses, et rien d'autre :

  1. Le registre des huit items de composition d'Ahler et Sood 2018, avec le libelle
     exact de leur question, le parti decrit, la realite que les auteurs citent et la
     source de cette realite. C'est un registre, pas un calcul : chaque valeur est lue
     dans les fichiers de replication, jamais retapee de memoire.
  2. Les definitions de groupe cote GSS 2024, c'est a dire la regle qui dit, pour
     chacun des huit groupes, quelles personnes des 1 052 du jeu de Stanford en font
     partie. Chaque definition porte son degre de confiance et son ecart declare a la
     definition d'Ahler et Sood.
  3. Les outils communs : intervalle de Wilson sur une proportion, bootstrap sur les
     items, permutation de signe, et la lecture tolerante des traces r1.

Entree  : data/ahler-sood-pcomp/*.dta
          data/osf-t6g7k-stanford/figure2/data/new_analysis_summaries/gss_filtered/
              preparation/p_wave1_summary.csv et p_wave2_summary.csv
          data/osf-t6g7k-stanford/figure3/data/demographic_summary.csv
          data/traces/r1-*.jsonl, data/traces/r1-distributions-reelles.csv (lecture seule)

Dependances : numpy, pandas.
"""

import glob
import json
import math
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
TRACES = os.path.join(RACINE, "data/traces")
AS = os.path.join(RACINE, "data/ahler-sood-pcomp")
PREP = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                            "new_analysis_summaries/gss_filtered/preparation")
DEMOG = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure3/data/demographic_summary.csv")

GRAINE = 20260909
N_BOOT = 2000
N_PERM = 20000

CAMPS_IDEO = ["gauche", "centre", "droite"]
CAMPS_PARTI = ["gauche", "centre", "droite"]

# Repliements repris a l'identique de a30_commun, pour qu'aucune divergence de camp ne
# s'installe entre a30, r1 et a46. Recopies et non importes : a30_commun charge des
# dependances lourdes dont ce module n'a pas besoin.
GSS_BLOC3 = {
    "extremely liberal": "gauche", "liberal": "gauche", "slightly liberal": "gauche",
    "moderate": "centre",
    "slightly conservative": "droite", "conservative": "droite",
    "extremely conservative": "droite",
}
GSS_PARTI3 = {
    "strong democrat": "gauche", "not very strong democrat": "gauche",
    "independent, close to democrat": "gauche",
    "independent (neither)": "centre",
    "independent, close to republican": "droite",
    "not very strong republican": "droite", "strong republican": "droite",
}

# --------------------------------------------------------------------------------------
# 1. Le registre d'Ahler et Sood
# --------------------------------------------------------------------------------------
# `realite_as` et `realite_as_et` ne sont PAS retapees : elles sont lues dans
# fig_1_data.dta par charger_ahler_sood(). Les valeurs arrondies employees par les auteurs
# eux memes dans leurs calculs d'erreur relative (lignes 160 a 167 de
# 01_pcomp_replication_main.do) sont dans `realite_as_arrondie`, parce que c'est ce nombre
# la, et pas la valeur a six decimales, qui produit les erreurs relatives publiees.

ITEMS_AS = {
    "dem_black": {
        "parti_as": "Democratic", "groupe": "Black",
        "question_en": "What percentage of Democratic Party supporters are Black?",
        "realite_as_arrondie": 24.0,
        "source_realite_as": "ANES 2012, dem_racecps_black, ponderee, parmi pid_3 == Dem",
    },
    "dem_union": {
        "parti_as": "Democratic", "groupe": "Union",
        "question_en": "What percentage of Democratic Party supporters are union members?",
        "realite_as_arrondie": 10.5,
        "source_realite_as": "ANES 2012, dem_unionwho_r == 1, ponderee, parmi pid_3 == Dem",
    },
    "dem_aa": {
        "parti_as": "Democratic", "groupe": "Atheist/Agnostic",
        "question_en": ("What percentage of Democratic Party supporters are atheist "
                        "or agnostic?"),
        "realite_as_arrondie": 8.7,
        "source_realite_as": ("Pew Religious Landscape 2014, calcul des auteurs "
                              "(0,73 x 5,7) / 48, pas une enquete de leur main"),
    },
    "dem_lgb": {
        "parti_as": "Democratic", "groupe": "LGB",
        "question_en": ("What percentage of Democratic Party supporters are gay, lesbian "
                        "or bisexual?"),
        "realite_as_arrondie": 6.3,
        "source_realite_as": "ANES 2012, orientn_rgay recodee, ponderee, parmi pid_3 == Dem",
    },
    "rep_evang": {
        "parti_as": "Republican", "groupe": "Evangelical",
        "question_en": ("What percentage of Republican Party supporters are evangelical "
                        "Christians?"),
        "realite_as_arrondie": 34.3,
        "source_realite_as": ("Pew Religious Landscape 2014, evangeliques blancs, "
                              "calcul des auteurs, pas une enquete de leur main"),
    },
    "rep_rich": {
        "parti_as": "Republican", "groupe": "$250K+ Income",
        "question_en": ("What percentage of Republican Party supporters earn over "
                        "$250,000 per year?"),
        "realite_as_arrondie": 2.2,
        "source_realite_as": ("ANES 2012, inc_incgroup_pre == 28, ponderee, "
                              "parmi pid_3 == Rep"),
    },
    "rep_old": {
        "parti_as": "Republican", "groupe": "Age 65+",
        "question_en": ("What percentage of Republican Party supporters are 65 years "
                        "or older?"),
        "realite_as_arrondie": 21.3,
        "source_realite_as": "ANES 2012, dem_agegrp_iwdate >= 11, ponderee, parmi pid_3 == Rep",
    },
    "rep_south": {
        "parti_as": "Republican", "groupe": "Southern",
        "question_en": "What percentage of Republican Party supporters are Southerners?",
        "realite_as_arrondie": 35.7,
        "source_realite_as": ("ANES 2012, 13 Etats declares sudistes a 50 pour cent et "
                              "plus par une enquete FiveThirtyEight, ponderee, "
                              "parmi pid_3 == Rep"),
    },
}

ORDRE_AS = ["dem_black", "dem_union", "dem_aa", "dem_lgb",
            "rep_evang", "rep_rich", "rep_old", "rep_south"]


# --------------------------------------------------------------------------------------
# 2. Les definitions de groupe cote GSS 2024
# --------------------------------------------------------------------------------------
# Chaque entree dit d'ou vient l'information (`source` : "demographie" = colonne de
# demographic_summary, "item" = colonne de p_wave1_summary, donc une question posee),
# la regle d'appartenance, la confiance de l'appariement conceptuel a Ahler et Sood, et
# l'ecart declare. `dispo_r1` dit si le run r1 a deja demande cet item aux modeles : c'est
# la colonne qui decide de ce que le matin peut calculer sans un seul appel de plus.

def _norm(v):
    return str(v).strip().lower()


DEFS_GSS = {
    "dem_black": [
        {"variante": "principale", "source": "demographie", "colonne": "demo_race",
         "regle": lambda d: d["demo_race"].map(_norm) == "black",
         "confiance": "elevee", "dispo_r1": False,
         "ecart": ("race* est exclue de la cible des 149 items par la liste de Stanford ; "
                   "la variable demographique est declaree, pas posee comme item")},
    ],
    "dem_union": [
        {"variante": "principale", "source": "item", "colonne": "union1",
         "regle": lambda d: d["union1"].map(_norm).isin(
             {"you belong", "you and spouse or partner belong"}),
         "confiance": "elevee", "dispo_r1": True,
         "ecart": ("union1 demande l'appartenance du repondant OU de son conjoint ; la "
                   "variante principale ne compte que le repondant, ce qui est la "
                   "quantite d'Ahler et Sood")},
        {"variante": "large", "source": "item", "colonne": "union1",
         "regle": lambda d: ~d["union1"].map(_norm).str.startswith("neither"),
         "confiance": "moyenne", "dispo_r1": True,
         "ecart": "compte aussi le foyer dont seul le conjoint est syndique"},
    ],
    "dem_aa": [
        {"variante": "principale", "source": "item", "colonne": "relig*",
         "regle": lambda d: d["relig*"].map(_norm) == "none",
         "confiance": "faible", "dispo_r1": False,
         "ecart": ("« aucune religion » n'est pas « athee ou agnostique » : le GSS ne "
                   "pose pas la question d'Ahler et Sood, et relig* est de toute facon "
                   "exclue des 149 items")},
        {"variante": "stricte", "source": "item", "colonne": "relig*",
         "regle": lambda d: (d["relig*"].map(_norm) == "none")
                            & (d["attend"].map(_norm) == "never"),
         "confiance": "faible", "dispo_r1": False,
         "ecart": "sans religion et n'assistant jamais a un office ; borne inferieure"},
    ],
    "dem_lgb": [
        {"variante": "principale", "source": "demographie", "colonne": "demo_sexual_orientation",
         "regle": lambda d: d["demo_sexual_orientation"].map(_norm).isin(
             {"gay or lesbian", "bisexual"}),
         "confiance": "elevee", "dispo_r1": False,
         "ecart": "18 pour cent de non renseigne, exclus du denominateur"},
        {"variante": "large", "source": "demographie", "colonne": "demo_sexual_orientation",
         "regle": lambda d: d["demo_sexual_orientation"].map(_norm).isin(
             {"gay or lesbian", "bisexual", "pansexual", "asexual",
              "other sexual orientation"}),
         "confiance": "moyenne", "dispo_r1": False,
         "ecart": "ajoute pansexuel, asexuel et autre, que la question d'Ahler et Sood ignore"},
    ],
    "rep_evang": [
        {"variante": "principale", "source": "item", "colonne": "reborn",
         "regle": lambda d: d["reborn"].map(_norm) == "yes",
         "confiance": "moyenne", "dispo_r1": True,
         "ecart": ("« ne de nouveau » n'est pas « evangelique » : la question du GSS ne "
                   "porte pas sur la denomination, et Ahler et Sood citent les "
                   "evangeliques BLANCS")},
        {"variante": "stricte", "source": "item", "colonne": "reborn",
         "regle": lambda d: (d["reborn"].map(_norm) == "yes")
                            & (d["relig*"].map(_norm) == "protestant"),
         "confiance": "moyenne", "dispo_r1": False,
         "ecart": "ne de nouveau et protestant ; plus proche du sens usuel d'evangelique"},
    ],
    "rep_rich": [
        {"variante": "principale", "source": "demographie", "colonne": "demo_income",
         "regle": lambda d: d["demo_income"].map(_norm) == "$250,000 or more",
         "confiance": "elevee", "dispo_r1": False,
         "ecart": ("l'item income des 149 plafonne a « $25000 or more », une echelle des "
                   "annees 1970 : il ne peut pas porter le seuil de 250 000 dollars. "
                   "Seule la demographie declaree le porte")},
        {"variante": "large", "source": "demographie", "colonne": "demo_income",
         "regle": lambda d: d["demo_income"].map(_norm).isin(
             {"$250,000 or more", "$200,000 to $249,999"}),
         "confiance": "moyenne", "dispo_r1": False,
         "ecart": "seuil abaisse a 200 000 dollars"},
    ],
    "rep_old": [
        {"variante": "principale", "source": "demographie", "colonne": "demo_age",
         "regle": lambda d: d["demo_age"].map(_norm).isin({"65 - 74", "75 or more"}),
         "confiance": "elevee", "dispo_r1": False,
         "ecart": "tranches d'age declarees, pas d'age exact"},
    ],
    "rep_south": [
        {"variante": "principale", "source": "demographie", "colonne": "demo_census_division",
         "regle": lambda d: d["demo_census_division"].map(_norm).isin(
             {"south atlantic", "e. sou. central", "w. sou. central"}),
         "confiance": "moyenne", "dispo_r1": False,
         "ecart": ("region du recensement (Sud) contre la liste de 13 Etats d'Ahler et "
                   "Sood : le recensement ajoute OK, WV, DE et MD")},
    ],
}


# --------------------------------------------------------------------------------------
# 3. Chargement
# --------------------------------------------------------------------------------------

def charger_ahler_sood():
    """Les cinq tableaux d'Ahler et Sood utiles ici, lus tels quels.

    Retourne (yougov, alt, affect, extremity, fig1). fig1 porte la perception moyenne
    ponderee et la realite citee, telles que le code de replication les a produites.
    """
    lire = lambda f: pd.read_stata(os.path.join(AS, f), convert_categoricals=False)
    return (lire("pcomp_yougov_data.dta"), lire("alt_exps_data.dta"),
            lire("affect_exp_data.dta"), lire("extremity_exp_data.dta"),
            lire("fig_1_data.dta"))


def charger_gss():
    """Les 1 052 personnes du GSS de Stanford : items vague 1 et 2, demographies, camps.

    Retourne un DataFrame d'une ligne par personne, avec toutes les colonnes d'items de
    la vague 1, toutes les colonnes de demographie, et deux colonnes de camp,
    `camp_ideo` et `camp_parti`, aux repliements de a30.
    """
    w1 = pd.read_csv(os.path.join(PREP, "p_wave1_summary.csv"))
    dem = pd.read_csv(DEMOG).set_index("email").loc[w1["email"]].reset_index()
    # Les colonnes de demographie prennent le prefixe `demo_`. Sans lui, `income` existe
    # des deux cotes, l'item du GSS a douze tranches plafonnant a 25 000 dollars et
    # l'attribut declare a douze tranches montant a 250 000, et pandas rendrait les deux
    # sous le meme nom. Ce n'est pas une precaution de style : c'est exactement l'item ou
    # la confusion changerait la realite de rep_rich.
    dem = dem.drop(columns=["email"]).add_prefix("demo_")
    d = pd.concat([w1, dem], axis=1)
    d["camp_ideo"] = d["demo_political_ideology"].map(_norm).map(GSS_BLOC3)
    d["camp_parti"] = d["demo_political_party"].map(_norm).map(GSS_PARTI3)
    return d


def lire_referent_r1():
    """Distributions humaines par item, camp d'ideologie et vague, telles que r1 les a ecrites.

    Lecture seule. keep_default_na=False pour la meme raison qu'en r1_evaluer : deux items
    du GSS ont une modalite qui s'ecrit litteralement « None ».
    """
    chemin = os.path.join(TRACES, "r1-distributions-reelles.csv")
    if not os.path.exists(chemin):
        return None
    d = pd.read_csv(chemin, keep_default_na=False, na_values=[""])
    for c in ("rang", "n", "effectif", "p"):
        d[c] = pd.to_numeric(d[c], errors="coerce")
    return d


def lire_traces_r1():
    """Toutes les lignes de trace r1 exploitables. Tolerant au partiel et au tronque.

    Un run interrompu, un modele absent, une derniere ligne coupee en cours d'ecriture :
    tout se lit et le perimetre effectif est rendu avec le tableau.
    """
    lignes = []
    for chemin in sorted(glob.glob(os.path.join(TRACES, "r1-*.jsonl"))):
        if "-smoke" in os.path.basename(chemin):
            continue
        with open(chemin, encoding="utf-8") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    lignes.append(json.loads(ligne))
                except json.JSONDecodeError:
                    continue
    return lignes


def lire_traces_composition(motif="a46-composition-*.jsonl"):
    """Traces du run « composition », s'il a eu lieu. Rend une liste vide sinon.

    C'est la seule porte par laquelle le troisieme terme entre pour les six groupes que
    r1 ne couvre pas. Tant que le run n'a pas tourne, tout le reste se calcule quand meme
    et les colonnes du modele restent vides.
    """
    lignes = []
    for chemin in sorted(glob.glob(os.path.join(TRACES, motif))):
        with open(chemin, encoding="utf-8") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    lignes.append(json.loads(ligne))
                except json.JSONDecodeError:
                    continue
    return lignes


# --------------------------------------------------------------------------------------
# 4. Outils statistiques
# --------------------------------------------------------------------------------------

def wilson(k, n, z=1.96):
    """Intervalle de Wilson a 95 pour cent sur une proportion, en pourcentage.

    Wilson et non Wald : plusieurs des huit groupes sont rares dans certains camps, et
    l'intervalle de Wald y sort de [0, 1] ou se reduit a zero, ce qui donnerait une
    fausse precision exactement la ou la mesure est la plus fragile.
    """
    if n is None or n <= 0:
        return float("nan"), float("nan"), float("nan")
    p = k / n
    d = 1.0 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    demi = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return 100.0 * p, 100.0 * max(centre - demi, 0.0), 100.0 * min(centre + demi, 1.0)


def ic_moyenne(x, rng, n=N_BOOT):
    """IC bootstrap a 95 pour cent d'une moyenne, unite de reechantillonnage : la ligne."""
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    if len(x) < 3:
        return (float(x.mean()) if len(x) else float("nan")), float("nan"), float("nan")
    idx = rng.integers(0, len(x), size=(n, len(x)))
    t = x[idx].mean(axis=1)
    return float(x.mean()), float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5))


def ic_ratio_des_moyennes(a, b, rng, n=N_BOOT):
    """Rapport des moyennes de deux series appariees, IC bootstrap sur les paires.

    Les paires sont tirees ensemble : la valeur humaine et la valeur du modele sur un
    meme item ne sont pas independantes, elles partagent la meme realite au denominateur.
    """
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    a, b = a[m], b[m]
    if len(a) < 3 or b.mean() == 0:
        return float("nan"), float("nan"), float("nan"), int(len(a))
    r = float(a.mean() / b.mean())
    idx = rng.integers(0, len(a), size=(n, len(a)))
    t = a[idx].mean(axis=1) / b[idx].mean(axis=1)
    t = t[np.isfinite(t)]
    if len(t) < 10:
        return r, float("nan"), float("nan"), int(len(a))
    return r, float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5)), int(len(a))


def p_permutation_signe(d, rng, n=N_PERM):
    """p bilateral d'une difference appariee, par permutation de signe.

    Estimateur de Phipson et Smyth (b + 1) / (m + 1), qui ne rend jamais un p nul.
    Meme test qu'en r1_evaluer et en a30, pour que les nombres se lisent ensemble.
    """
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 3:
        return float("nan")
    obs = abs(d.mean())
    signes = rng.choice([-1.0, 1.0], size=(n, len(d)))
    stat = np.abs((signes * d[None, :]).mean(axis=1))
    return float((int((stat >= obs - 1e-15).sum()) + 1.0) / (n + 1.0))


def holm(p):
    """Correction de Holm. Recopiee de a28_commun pour ne rien importer de lourd."""
    p = np.asarray(p, dtype=float)
    m = len(p)
    ordre = np.argsort(p)
    out = np.empty(m, dtype=float)
    courant = 0.0
    for rang, i in enumerate(ordre):
        v = (m - rang) * p[i]
        courant = max(courant, v)
        out[i] = min(courant, 1.0)
    return out


def poser_holm(lignes, cle_p="p", cle_sortie="p_holm"):
    """Holm a l'interieur d'une famille, les tests indecidables retires avant correction."""
    for l in lignes:
        l[cle_sortie] = float("nan")
    index = [i for i, l in enumerate(lignes) if np.isfinite(l.get(cle_p, float("nan")))]
    if not index:
        return lignes
    corriges = holm(np.array([lignes[i][cle_p] for i in index], dtype=float))
    for i, pc in zip(index, corriges):
        lignes[i][cle_sortie] = float(pc)
    return lignes


def ecrire(df, nom):
    """Ecrit un tableau dans resultats/ et rend son chemin. Ne touche a rien d'autre."""
    chemin = os.path.join(SORTIE, nom)
    df.to_csv(chemin, index=False)
    return chemin
