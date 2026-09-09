"""
a8_commun : briques partagees par les scripts de durcissement des baselines a2.

Statut : script d'exploration, pas du code de production. Ce module ne redefinit aucune
metrique : il importe a2_commun et se contente de charger les donnees, de reconstruire
exactement le decoupage de a2 (graine 20260903, 5 plis de personnes, 5 blocs d'items) et
d'ajouter ce que a2 n'avait pas, c'est a dire le repere ordinal du GSS, les treize
simulations de Twin-2K-500 alignees sur le catalogue, et les mesures sur les modalites
minoritaires.

Entree  : data/osf-t6g7k-stanford et data/twin2k500, non versionnes.
Sortie  : rien par lui meme. Les scripts a8_*.py ecrivent dans resultats/a8-*.csv.

Aucun appel de modele. Le nombre de fils de calcul est limite a quatre : une autre
session occupe la machine.
"""

import os

# Limite de quatre coeurs, posee avant l'import de numpy sinon elle est sans effet.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import ast
import json
import sys
from collections import Counter

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a2_commun import (bootstrap_personnes, est_manquant, exactitude_par_personne,  # noqa: E402
                       profil_diversite)
import a2_baselines_gss as G  # noqa: E402
import a2_baselines_twin as T  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
GRAINE = G.GRAINE          # 20260903, identique a a2
N_PLIS = G.N_PLIS          # 5
N_BLOCS = G.N_BLOCS        # 5
K_A2 = G.K_VOISINS         # 30, le k choisi sur le pli de test dans a2

QM = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/question_master/gss")


# ---------------------------------------------------------------------------
# GSS
# ---------------------------------------------------------------------------

def charger_gss():
    """Charge le GSS exactement comme a2, plus le repere ordinal du question_master.

    `groups/categorical.csv` porte une colonne "Categorical " a Y ou N. Y designe un item
    nominal, N un item ordinal : verifie sur les libelles, les NAT* et CON* sont a N et
    portent des echelles "too little / about right / too much", les items binaires
    d'opinion sont a Y. Le champ Options de `main.csv` donne l'ordre des modalites, qui
    est l'ordre de l'echelle et sert au codage ordinal de la copule.
    """
    ids, items, y1, y2, x, attributs = G.charger()
    cat = pd.read_csv(os.path.join(QM, "groups", "categorical.csv"))
    cat.columns = [c.strip() for c in cat.columns]
    est_nominal = {str(r["Question ID"]).strip().lower(): str(r["Categorical"]).strip().upper()
                   for _, r in cat.iterrows()}
    principal = pd.read_csv(os.path.join(QM, "main.csv"))
    options = {}
    for _, r in principal.iterrows():
        try:
            options[str(r["Question ID"]).strip().lower()] = list(ast.literal_eval(r["Options"]))
        except Exception:
            continue
    ordinaux = [it for it in items if est_nominal.get(it.strip().lower()) == "N"]
    return {
        "ids": ids, "items": items, "y1": y1, "y2": y2, "x": x, "attributs": attributs,
        "ordinaux": ordinaux, "options": options,
    }


def grille_gss(n, m):
    """Le decoupage de a2, rejoue a l'identique : memes plis, memes blocs d'items."""
    return G.grille(n, m, GRAINE)


AGENTS_GSS = dict(G.CONDITIONS_LLM)


def charger_agents_gss(items):
    """Matrices de reponses des conditions d'agents de l'archive, memes items que nous."""
    sorties = {}
    for libelle, fichier in AGENTS_GSS.items():
        chemin = os.path.join(G.PREP, fichier)
        if not os.path.exists(chemin):
            continue
        sorties[libelle] = pd.read_csv(chemin)[items].values.astype(object)
    return sorties


# ---------------------------------------------------------------------------
# Twin-2K-500
# ---------------------------------------------------------------------------

def charger_twin():
    """Charge Twin-2K-500 exactement comme a2."""
    return T.charger()


def plis_twin(n):
    return T.plis_personnes(n, GRAINE)


# Les treize configurations publiees par les auteurs, telechargees par
# a8_telecharger_twin_llm.py. `spec_texte_gpt41mini.csv` est le meme fichier que le
# `default_gpt41mini_llm.csv` de a2 : verifie par empreinte MD5, 32692ebe... des deux
# cotes. `spec_demo_only_gpt41mini.csv` est de meme le fichier demographies seules de a2.
SPECS_TWIN = {
    "GPT-4.1-mini, persona texte": "spec_texte_gpt41mini.csv",
    "GPT-4.1-mini, persona texte, temperature par defaut": "spec_texte_temp_defaut_gpt41mini.csv",
    "GPT-4.1-mini, persona texte, raisonnement": "spec_texte_raisonnement_gpt41mini.csv",
    "GPT-4.1-mini, persona texte, questions repetees": "spec_texte_repetition_gpt41mini.csv",
    "GPT-4.1-mini, persona JSON": "spec_json_gpt41mini.csv",
    "GPT-4.1-mini, persona JSON, sortie predite": "spec_json_predout_gpt41mini.csv",
    "GPT-4.1-mini, resume de persona": "spec_resume_gpt41mini.csv",
    "GPT-4.1-mini, resume plus persona JSON": "spec_resume_json_gpt41mini.csv",
    "GPT-4.1-mini, affine sur 500 exemples": "spec_finetune500_gpt41mini.csv",
    "GPT-4.1-mini, demographies seules": "spec_demo_only_gpt41mini.csv",
    "GPT-4.1, persona JSON": "spec_json_gpt41.csv",
    "GPT-4.1, persona JSON, sortie predite": "spec_json_predout_gpt41.csv",
    "Gemini-Flash-2.5, persona texte": "spec_texte_gemini_flash25.csv",
}


def charger_llm_twin(d):
    """Aligne les simulations publiees sur les colonnes du catalogue et sur l'ordre des pid.

    Deux verifications faites avant d'ecrire cette fonction, et elles conditionnent tout
    ce qui suit :
      - le fichier humain formate trie par TWIN_ID croissant a exactement la meme liste de
        pid, dans le meme ordre, que le catalogue ; egalite testee element par element ;
      - sur les 108 items cibles, les valeurs du fichier humain formate et celles du
        catalogue coincident, accord 1,0000 et memes cellules manquantes.
    La simulation peut donc etre lue comme une matrice (personnes x items) dans le meme
    repere que nos baselines, ce qui autorise la comparaison item par item.
    """
    mapping = json.load(open(os.path.join(T.LLM, "wave4_formatted_to_catalog_mapping.json"),
                             encoding="utf-8"))
    cibles = list(d["cibles"])
    rang = {c: j for j, c in enumerate(cibles)}
    paires = [(m["formatted_column"], m["catalog_csv_column"]) for m in mapping
              if m["catalog_csv_column"] in rang]
    pid = list(d["pid"])
    place = {p: i for i, p in enumerate(pid)}
    sorties = {}
    for libelle, fichier in SPECS_TWIN.items():
        chemin = os.path.join(T.LLM, fichier)
        if not os.path.exists(chemin):
            continue
        sim = pd.read_csv(chemin, low_memory=False).iloc[1:].reset_index(drop=True)
        sim["tid"] = pd.to_numeric(sim["TWIN_ID"])
        sim = sim.sort_values("tid").reset_index(drop=True)
        # Trois configurations sur treize ne couvrent pas les 2 058 personnes : le modele
        # affine exclut ses 500 exemples d'entrainement, une variante JSON s'arrete a
        # 1 000 personnes, une autre en perd huit. On garde la personne manquante hors
        # denominateur au lieu de la compter comme une erreur, et on rapporte la
        # couverture avec chaque score.
        lignes = [place[t] for t in sim["tid"] if t in place]
        assert len(lignes) == len(sim), f"identifiants inconnus dans {fichier}"
        personnes = np.zeros(len(pid), dtype=bool)
        personnes[lignes] = True
        mat = np.full((len(pid), len(cibles)), np.nan)
        for f, c in paires:
            if f in sim.columns:
                mat[lignes, rang[c]] = pd.to_numeric(sim[f], errors="coerce").values
        sorties[libelle] = {"matrice": mat.astype(object), "personnes": personnes,
                            "n_personnes": int(personnes.sum())}
    return sorties


def cible_twin_numerique(d):
    """Cible de la vague 4 coercee en nombres, meme repere que les simulations."""
    y = d["y"]
    out = np.full(y.shape, np.nan)
    for j in range(y.shape[1]):
        out[:, j] = pd.to_numeric(pd.Series(y[:, j]), errors="coerce").values
    return out.astype(object)


# ---------------------------------------------------------------------------
# Modalites minoritaires
# ---------------------------------------------------------------------------

def modalites_minoritaires(verite, seuil):
    """Pour chaque item, l'ensemble des modalites dont la part humaine est sous le seuil.

    La part est calculee sur l'ensemble des repondants observes de l'item, ce qui est une
    description de la population et non un parametre appris : aucune prediction n'en
    depend, elle sert uniquement a etiqueter les cellules a examiner.
    """
    sets = []
    for j in range(verite.shape[1]):
        v = [x for x in verite[:, j] if not est_manquant(x)]
        n = len(v)
        if n == 0:
            sets.append(set())
            continue
        cpt = Counter(v)
        sets.append({mod for mod, c in cpt.items() if c / n < seuil})
    return sets


def mesures_minorites(pred, verite, minoritaires, masque=None):
    """Rappel, precision et masse sur les modalites minoritaires.

    - rappel : part des cellules dont la vraie reponse est minoritaire qui sont bien
      predites. C'est l'exactitude restreinte a ces cellules.
    - precision : parmi les cellules ou la methode predit une modalite minoritaire, part
      des cellules justes.
    - masse predite : part de toutes les cellules evaluables ou la methode predit une
      modalite minoritaire, a comparer a la masse humaine, qui est la part des cellules
      dont la vraie reponse est minoritaire.
    Une methode peut donc avoir un rappel nul et une masse nulle, ce qui est le cas de
    toute methode qui repond systematiquement la modalite majoritaire.
    """
    if masque is None:
        masque = np.array([[not est_manquant(v) for v in ligne] for ligne in verite])
    n_min_vrai = n_min_juste = 0
    n_min_pred = n_min_pred_juste = 0
    n_cellules = 0
    for j in range(verite.shape[1]):
        mods = minoritaires[j]
        for i in range(verite.shape[0]):
            if not masque[i, j]:
                continue
            n_cellules += 1
            v, p = verite[i, j], pred[i, j]
            juste = (p == v)
            if v in mods:
                n_min_vrai += 1
                n_min_juste += juste
            if (not est_manquant(p)) and p in mods:
                n_min_pred += 1
                n_min_pred_juste += juste
    return {
        "cellules": n_cellules,
        "cellules_minoritaires": n_min_vrai,
        "rappel_minoritaire": n_min_juste / n_min_vrai if n_min_vrai else float("nan"),
        "precision_minoritaire": n_min_pred_juste / n_min_pred if n_min_pred else float("nan"),
        "masse_minoritaire_predite": n_min_pred / n_cellules if n_cellules else float("nan"),
        "masse_minoritaire_humaine": n_min_vrai / n_cellules if n_cellules else float("nan"),
    }


# ---------------------------------------------------------------------------
# Sorties
# ---------------------------------------------------------------------------

def ecrire_csv(lignes, nom):
    """Ecrit un tableau agrege dans resultats/. Aucune microdonnee n'y transite."""
    os.makedirs(SORTIE, exist_ok=True)
    chemin = os.path.join(SORTIE, nom)
    pd.DataFrame(lignes).to_csv(chemin, index=False, float_format="%.6f")
    print(f"ecrit : {chemin}")
    return chemin


def exactitude_sur(pred, verite, colonnes, masque=None):
    """Exactitude par personne restreinte a un sous ensemble d'items, avec IC bootstrap."""
    p = pred[:, colonnes]
    v = verite[:, colonnes]
    m = None if masque is None else masque[:, colonnes]
    acc = exactitude_par_personne(p, v, m)
    return bootstrap_personnes(acc, graine=GRAINE)


def diversite_sur(pred, verite, colonnes):
    return profil_diversite(pred[:, colonnes], verite[:, colonnes])
