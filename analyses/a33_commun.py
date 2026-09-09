"""
a33_commun : briques partagees par l'exploitation de la condition C3F, question du
8 septembre 2026, "la fausse rarete vient elle d'un contexte insuffisant ?".

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a31_commun,
a31_mecanismes, et par eux a29_commun, a28_commun, a25_commun, a25_mesures, a8_commun,
a2_commun, a2_baselines_gss, a5_evaluer et a5_agents_locaux_gss. Les 1 052 personnes,
les 149 items, les plis, les blocs, les graines, les covariables de cellule, le temoin
aveugle a la personne et le bootstrap apparie sur les personnes viennent de la, sans une
ligne recopiee.

Ce module porte quatre choses et rien d'autre.

  1. La matrice de prediction de C3F, lue dans data/traces/a5-C3F-p1.jsonl par les
     fonctions de a5_evaluer, exactement comme a25_mesures lit C2 et C3. C3F est la
     condition ou le contexte du prompt est ampute de la FAMILLE thematique entiere de
     l'item cible, et ou c'est cette famille qui est predite. Elle a tourne de 05:02 a
     06:20 le 8 septembre et s'est arretee sur la fin dure : 60 personnes completes sur
     150, 58 items, 3 480 cellules.

  2. Le perimetre apparie : les 60 personnes completes de C3F et les 58 items des six
     familles de a2_baselines_gss. C3, C2, les baselines et les six conditions de
     Stanford sont restreintes AUX MEMES cellules. C'est la seule facon de faire varier
     le contexte a personne constante, ce que a31 section 10 point 3 designe comme la
     mesure manquante.

  3. Les covariables de cellule, calculees par a31_mecanismes.covariables sur les 1 052
     humains de la vague 1 puis restreintes au perimetre. Le motif du choix est ecrit
     dans le rapport : sur 60 personnes, la rarete d'un segment ideologique serait
     estimee sur huit personnes en moyenne, ce qui la rendrait inutilisable. La reference
     de minorite est donc celle de la population du perimetre 1 052, et la variante
     calculee sur les 150 personnes du run est rapportee comme sensibilite.

  4. La rarete du contexte REELLEMENT VU par chaque condition. Elle differe d'une
     condition a l'autre et c'est tout l'objet du rapport :
       - C3  voit les 149 items moins le bloc secret de 29 ou 30 items, soit 119 ou 120
             items, dont les cousins de famille qui ne sont pas tombes dans le meme bloc ;
       - C3F voit les 149 items moins la famille entiere de l'item, soit 132 a 144 items,
             et aucun cousin de famille.
     C3F voit donc PLUS d'items que C3 et MOINS de cousins. Ce n'est pas une reduction de
     volume, c'est une ablation ciblee de l'information la plus proche. Les deux mesures
     sont produites ici et le rapport ne les confond pas.

  5. Le controle B2 famille retiree. Le script analyses/a8_familles.py ne permet pas de
     restreindre son calcul a un sous ensemble de personnes : sa fonction gss() rend des
     agregats sur les 1 052 et ne rend aucune matrice. La prediction est donc reconstruite
     ici a partir des memes primitives importees telles quelles, a2_commun.en_codes,
     distance_hamming et b2_voisins, avec les memes plis, le meme K et la meme graine que
     a8_commun. b2_voisins en mode argmax ne consomme pas le generateur aleatoire, la
     reconstruction est donc exacte et ne depend pas de l'ordre des tirages de a8. Le
     controle de reproduction sur les 1 052 personnes est ecrit dans a33-controles.csv :
     il doit redonner le 0,6621 de a8-familles-gss.csv.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import sys

# Limite de quatre coeurs, posee avant l'import de numpy sinon elle est sans effet.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a31_commun as C31
import a31_mecanismes as M31
from a2_baselines_gss import FAMILLES
from a2_commun import b2_voisins, distance_hamming, en_codes
import a8_commun as C8

RACINE = C31.RACINE
SORTIE = C31.SORTIE

GRAINE = 20260908
SEUIL = 0.10
AXE_PRINCIPAL = C31.AXE_PRINCIPAL

# Ordre d'affichage stable dans tous les tableaux de a33. C3F est la condition nouvelle,
# C3 son temoin apparie, les autres sont des points de repere sur les memes cellules.
ORDRE = ["C3F", "C3", "C2", "agents composite", "agents enquete", "agents entretien (v3)",
         "agents demographiques (v6)", "agents v7", "agents v8", "B0 mode", "B0 tirage",
         "B1 argmax", "B2 argmax", "B2 famille retiree", "B3 foret", "humains vague 2"]


# ---------------------------------------------------------------------------
# 1. C3F : matrice de prediction et distributions
# ---------------------------------------------------------------------------

def matrice_c3f(paquet):
    """Matrice 1 052 x 149 de C3F, None hors des cellules effectivement predites.

    Renvoie aussi la liste ordonnee des personnes completes, le nombre de personnes
    partielles ecartees, et les matrices de p max et d'entropie lues dans la trace.
    """
    from a5_evaluer import lire_traces, moyenner_passes, en_matrices
    from a5_agents_locaux_gss import TRACES, nomenclature

    ids, items = paquet["ids"], paquet["items"]
    index_personne = {p: i for i, p in enumerate(ids)}
    table = nomenclature()
    tables, _ = lire_traces("")
    if ("C3F", 1) not in tables:
        raise SystemExit("aucune trace C3F dans data/traces")

    compte = {}
    for (pid, _it) in tables[("C3F", 1)]:
        compte[pid] = compte.get(pid, 0) + 1
    n_items_c3f = len({it for (_p, it) in tables[("C3F", 1)]})
    complets = {p for p, n in compte.items() if n == n_items_c3f}

    ech = pd.read_csv(os.path.join(TRACES, "a5-personnes.csv"))
    personnes = [p for p in ech["pid"] if p in complets]
    partielles = len(compte) - len(complets)

    fusion, _passes = moyenner_passes(tables, "C3F")
    pred, dist = en_matrices(fusion, personnes, items, table)

    plein = np.empty((len(ids), len(items)), dtype=object)
    plein[:] = None
    lignes = [index_personne[p] for p in personnes]
    plein[np.ix_(lignes, list(range(len(items))))] = pred

    pmax = np.full((len(ids), len(items)), np.nan)
    ent = np.full((len(ids), len(items)), np.nan)
    for a, i in enumerate(lignes):
        for j in range(len(items)):
            d = dist[a, j]
            if d:
                q = np.array(list(d.values()), dtype=float)
                pmax[i, j] = float(q.max())
                q = q[q > 0]
                ent[i, j] = float(-(q * np.log2(q)).sum())
    return {"matrice": plein, "personnes": personnes, "lignes": np.array(lignes),
            "partielles": partielles, "pmax": pmax, "entropie": ent,
            "appels": len(tables[("C3F", 1)]), "n_items": n_items_c3f}


def confiances_c2_c3(paquet):
    """p max et entropie de C2 et C3, sur les 1 052 lignes, NaN hors des 150 du run."""
    conf, _bloc_trace, _f = C31.confiances_locales(paquet, paquet["items"])
    lignes150 = np.asarray(paquet["lignes150"])
    sortie = {}
    for cond, d in conf.items():
        pmax = np.full((len(paquet["ids"]), len(paquet["items"])), np.nan)
        ent = np.full_like(pmax, np.nan)
        pmax[lignes150] = d["pmax"]
        ent[lignes150] = d["entropie"]
        sortie[cond] = {"pmax": pmax, "entropie": ent, "argmax": d["argmax"]}
    return sortie


# ---------------------------------------------------------------------------
# 2. Perimetre apparie et decoupages d'items
# ---------------------------------------------------------------------------

def colonnes_familles(items):
    """Indices des 58 items de famille, et vecteur item -> indice de famille.

    Les items hors famille recoivent l'indice 6, qui n'est jamais une cible : il sert
    uniquement a ce que rarete_contexte de a31_commun puisse etre appelee telle quelle
    avec un decoupage par famille au lieu d'un decoupage par bloc.
    """
    index = {it: j for j, it in enumerate(items)}
    fam_index = np.full(len(items), len(FAMILLES), dtype=np.int32)
    cols, noms = [], {}
    for k, (nom, membres) in enumerate(FAMILLES.items()):
        for it in membres:
            if it in index:
                fam_index[index[it]] = k
                cols.append(index[it])
                noms[index[it]] = nom
    cols = np.array(sorted(cols), dtype=int)
    return cols, fam_index, noms


def cousins_en_contexte(items, cols_fam, fam_index, bloc):
    """Pour chaque item de famille, le nombre de cousins presents dans le contexte de C3.

    C3 retire le bloc secret entier : un cousin tombe dans le meme bloc que la cible est
    donc absent du contexte de C3 lui aussi. C3F retire la famille entiere : aucun cousin
    n'est present, par construction. Cette table est ce qui rend l'ablation quantitative.
    """
    lignes = []
    for j in cols_fam:
        f = fam_index[j]
        freres = np.flatnonzero((fam_index == f) & (np.arange(len(items)) != j))
        meme_bloc = int((bloc[freres] == bloc[j]).sum())
        lignes.append({"item": items[j], "famille_index": int(f),
                       "taille_famille": int(len(freres) + 1),
                       "cousins_total": int(len(freres)),
                       "cousins_dans_le_bloc_secret": meme_bloc,
                       "cousins_vus_par_C3": int(len(freres) - meme_bloc),
                       "cousins_vus_par_C3F": 0,
                       "items_contexte_C3": int(len(items) - (bloc == bloc[j]).sum()),
                       "items_contexte_C3F": int(len(items) - (fam_index == f).sum())})
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 3. Restriction des covariables et des masques au perimetre
# ---------------------------------------------------------------------------

_MATRICES_CV = ("verite", "ok", "rare_vrai", "deplace", "valide_fam", "r_personne",
                "ctx", "ext_vrai", "ext1_vrai", "extK_vrai", "modale_pop")
_VECTEURS_ITEM = ("mods", "fam", "porte", "multi", "bloc", "items")


def sous_perimetre_cv(cv, lignes, cols):
    """Restreint un paquet de covariables de a31_mecanismes a (lignes, cols)."""
    out = {}
    for cle in _MATRICES_CV:
        out[cle] = cv[cle][np.ix_(lignes, cols)]
    for cle in _VECTEURS_ITEM:
        v = cv[cle]
        out[cle] = [v[j] for j in cols] if isinstance(v, list) else np.asarray(v)[cols]
    out["seg"] = {a: cv["seg"][a][lignes] for a in cv["seg"]}
    out["r_segment"] = {a: cv["r_segment"][a][np.ix_(lignes, cols)] for a in cv["r_segment"]}
    out["modale_seg"] = {a: cv["modale_seg"][a][np.ix_(lignes, cols)]
                         for a in cv["modale_seg"]}
    out["premiere"], out["derniere"], out["options"] = (cv["premiere"], cv["derniere"],
                                                        cv["options"])
    return out


def sous_perimetre_mq(mq, lignes, cols):
    """Restreint un paquet de masques de condition de a31_mecanismes a (lignes, cols)."""
    return {cle: mat[np.ix_(lignes, cols)] for cle, mat in mq.items()}


# ---------------------------------------------------------------------------
# 4. B2 famille retiree, reconstruite a l'identique
# ---------------------------------------------------------------------------

def b2_famille_retiree(paquet, verbeux=True):
    """Predit les 58 items de famille en retirant la famille entiere du contexte.

    Reprise exacte de la boucle "B2 famille" de analyses/a8_familles.py, avec les
    primitives importees telles quelles et le meme K. b2_voisins en mode argmax ne
    consomme pas le generateur aleatoire : la matrice obtenue ne depend donc pas de
    l'ordre des tirages de a8, et le controle de reproduction le verifie sur les 1 052.
    """
    ids, items, y1 = paquet["ids"], paquet["items"], paquet["y1"]
    n, m = y1.shape
    plis, _blocs = C8.grille_gss(n, m)
    codes = en_codes(y1)
    index = {it: j for j, it in enumerate(items)}
    familles = {nom: [index[i] for i in membres if i in index]
                for nom, membres in FAMILLES.items()}
    rng = np.random.default_rng(C8.GRAINE)

    pred = np.empty((n, m), dtype=object)
    pred[:] = None
    for i_pli, (tr, te) in enumerate(plis):
        for _nom, cols in familles.items():
            contexte = np.setdiff1d(np.arange(m), cols)
            d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
            for j in cols:
                pred[np.ix_(te, [j])] = b2_voisins(d, y1[tr, j], C8.K_A2, rng)[:, None]
        if verbeux:
            print(f"  B2 famille retiree, pli {i_pli + 1}/{len(plis)}", flush=True)
    return pred


# ---------------------------------------------------------------------------
# 5. Reexports commodes
# ---------------------------------------------------------------------------

charger = C31.charger
observe = C31.observe
appartient = C31.appartient
par_personne = C31.par_personne
moyenne_par_personne = C31.moyenne_par_personne
temoin_par_personne = C31.temoin_par_personne
temoin_item = C31.temoin_item
taux = C31.taux
taux_ic = C31.taux_ic
contraste = C31.contraste
tirages_bootstrap = C31.tirages_bootstrap
segments_et_niveaux = C31.segments_et_niveaux
holm = C31.holm
benjamini_hochberg = C31.benjamini_hochberg
ecrire = C31.ecrire
rarete_contexte = C31.rarete_contexte
covariables = M31.covariables
masques_condition = M31.masques_condition
mesure_h2a = M31.mesure_h2a
mesure_h1a = M31.mesure_h1a
