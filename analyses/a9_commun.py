"""
a9_commun : briques partagees par les scripts a9 (deviance et incoherence sur Twin-2K-500).

Statut : script d'exploration, pas du code de production. Aucun appel de modele de langage.
Aucune microdonnee n'est ecrite hors de data/ : les scripts a9 n'ecrivent que des tableaux
agreges dans resultats/.

Ce module fournit :
  - la lecture du catalogue de questions et le classement des colonnes en domaines,
  - la lecture des reponses humaines (vagues 1 a 3, vague 4) et des sorties LLM des auteurs,
  - la construction des segments demographiques,
  - la deviance au mode du segment, calculee en laissant la personne hors du mode,
  - alpha de Cronbach et les matrices de correlation inter items.

Dependances : numpy, pandas. Sciences dures uniquement, zero reseau.
"""

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
TWIN = RACINE / "data" / "twin2k500"
CSV = TWIN / "question_catalog_and_human_response_csv"
LLM = TWIN / "llm"

# La machine fait tourner un llama-server en parallele : on se limite a 4 coeurs.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")


# ---------------------------------------------------------------------------
# Catalogue et classement des colonnes en domaines
# ---------------------------------------------------------------------------

# Blocs du catalogue -> domaine d'analyse. Tout bloc non liste et non demographique
# tombe dans "heuristiques_biais", ce qui correspond aux experiences d'economie
# comportementale, une par bloc, presentees en inter sujets.
DOMAINE_PAR_BLOC = {
    "Personality": "personnalite",
    "Cognitive tests": "cognitif",
    "Economic preferences": "economique",
    "Product Preferences - Pricing": "prix",
    "False consensus": "attitudes",
    "Demographics": "demographies",
    "Forward Flow": "exclu",
    "Economic preferences - intro": "exclu",
}

ORDRE_DOMAINES = ["personnalite", "cognitif", "economique", "prix",
                  "heuristiques_biais", "attitudes"]


def charger_catalogue():
    """Les 256 entrees du catalogue Qualtrics, telles que fournies par les auteurs."""
    with open(CSV / "question_catalog.json") as f:
        return json.load(f)


def table_items(catalogue=None):
    """Une ligne par colonne de CSV exploitable, avec son domaine et son type.

    Sont retenues les colonnes categorielles : choix unique (SAVR, SAHR), matrices
    (Likert, Bipolar), et les questions a choix multiple (MAVR, MAHR) reconstituees
    en une seule colonne par question. Sont ecartes les curseurs (valeurs continues)
    et les saisies libres, ou l'egalite exacte n'a pas de sens.
    """
    catalogue = catalogue or charger_catalogue()
    lignes = []
    for q in catalogue:
        bloc = q.get("BlockName", "").strip()
        domaine = DOMAINE_PAR_BLOC.get(bloc, "heuristiques_biais")
        if domaine == "exclu":
            continue
        typ = q["QuestionType"]
        sel = (q.get("Settings") or {}).get("Selector")
        if typ == "MC" and sel in ("SAVR", "SAHR"):
            for c in q["csv_columns"]:
                lignes.append((c, q["QuestionID"], bloc, domaine, "choix_unique", None))
        elif typ == "MC" and sel in ("MAVR", "MAHR"):
            # Reconstitution : une colonne synthetique par question, cf. colonnes_mavr.
            lignes.append((q["QuestionID"] + "__mavr", q["QuestionID"], bloc, domaine,
                           "choix_multiple_reconstitue", None))
        elif typ == "Matrix":
            rows = q.get("Rows") or []
            for i, c in enumerate(q["csv_columns"]):
                lignes.append((c, q["QuestionID"], bloc, domaine, "matrice",
                               rows[i] if i < len(rows) else None))
        # Slider et TE : ecartes.
    t = pd.DataFrame(lignes, columns=["colonne", "qid", "bloc", "domaine", "type", "libelle"])
    return t.drop_duplicates("colonne").set_index("colonne")


def colonnes_mavr(catalogue=None):
    """Pour chaque question a choix multiple, la liste de ses colonnes indicatrices."""
    catalogue = catalogue or charger_catalogue()
    d = {}
    for q in catalogue:
        sel = (q.get("Settings") or {}).get("Selector")
        if q["QuestionType"] == "MC" and sel in ("MAVR", "MAHR"):
            d[q["QuestionID"]] = q["csv_columns"]
    return d


# ---------------------------------------------------------------------------
# Lecture des reponses
# ---------------------------------------------------------------------------

def _reconstituer_mavr(df, catalogue=None):
    """Ramene chaque question a choix multiple a une colonne unique.

    Convention : la position la plus elevee parmi les options cochees. C'est la
    cotation habituelle de l'inventaire de depression de Beck, qui represente vingt
    et une des vingt deux questions concernees ; 91,3 pour cent des reponses concernees
    ne cochent qu'une option, la convention ne joue donc que sur une minorite de cellules.
    """
    ajouts = {}
    for qid, cols in colonnes_mavr(catalogue).items():
        cols = [c for c in cols if c in df.columns]
        if not cols:
            continue
        bloc = df[cols].notna().to_numpy()
        pos = np.arange(1, len(cols) + 1)
        ajouts[qid + "__mavr"] = np.where(bloc.any(axis=1), (bloc * pos).max(axis=1), np.nan)
    if ajouts:
        df = pd.concat([df, pd.DataFrame(ajouts, index=df.index)], axis=1)
    return df


def charger_humains(vague, catalogue=None):
    """Reponses humaines en codes numeriques, index pid. vague vaut '1_3' ou '4'."""
    f = CSV / ("wave1_3_response.csv" if vague == "1_3" else "wave4_response.csv")
    df = pd.read_csv(f, low_memory=False).set_index("pid")
    return _reconstituer_mavr(df, catalogue)


def _mapping_llm():
    with open(LLM / "wave4_formatted_to_catalog_mapping.json") as f:
        m = json.load(f)
    return {e["formatted_column"]: e["catalog_csv_column"] for e in m}


CONFIGS_LLM = {
    # nom court -> fichier. Sorties deja calculees par les auteurs de Twin-2K-500.
    "gpt41mini_defaut": "default_gpt41mini_llm.csv",
    "gpt41mini_demo_seules": "demo_only_gpt41mini_llm.csv",
    "gpt41mini_demo_seules_spec": "spec_demo_only_gpt41mini.csv",
    "gpt41mini_texte": "spec_texte_gpt41mini.csv",
    "gpt41mini_texte_temp_defaut": "spec_texte_temp_defaut_gpt41mini.csv",
    "gpt41mini_texte_raisonnement": "spec_texte_raisonnement_gpt41mini.csv",
    "gpt41mini_texte_repetition": "spec_texte_repetition_gpt41mini.csv",
    "gpt41mini_json": "spec_json_gpt41mini.csv",
    "gpt41mini_json_predout": "spec_json_predout_gpt41mini.csv",
    "gpt41mini_resume": "spec_resume_gpt41mini.csv",
    "gpt41mini_resume_json": "spec_resume_json_gpt41mini.csv",
    "gpt41mini_finetune500": "spec_finetune500_gpt41mini.csv",
    "gpt41_json": "spec_json_gpt41.csv",
    "gpt41_json_predout": "spec_json_predout_gpt41.csv",
    "gemini_flash25_texte": "spec_texte_gemini_flash25.csv",
}

FICHIER_HUMAIN_FORMAT_LLM = "default_gpt41mini_wave4.csv"


def charger_llm(fichier):
    """Sortie LLM au format vague 4 des auteurs, renommee vers les colonnes du catalogue.

    La deuxieme ligne du fichier porte le libelle de la question et non une reponse :
    elle est sautee. Les codes sont ceux du CSV numerique des auteurs.
    """
    d = pd.read_csv(LLM / fichier, skiprows=[1], low_memory=False)
    d = d.rename(columns={"TWIN_ID": "pid"})
    f2c = _mapping_llm()
    garde = ["pid"] + [c for c in d.columns if c in f2c]
    d = d[garde].rename(columns=f2c)
    d["pid"] = pd.to_numeric(d["pid"], errors="coerce")
    d = d.dropna(subset=["pid"]).set_index("pid")
    d.index = d.index.astype(int)
    return d.apply(pd.to_numeric, errors="coerce")


def configs_llm_disponibles():
    return {k: v for k, v in CONFIGS_LLM.items() if (LLM / v).exists()}


# ---------------------------------------------------------------------------
# Segments demographiques
# ---------------------------------------------------------------------------

SEGMENTS = {
    "genre": ["QID12"],
    "age": ["QID13"],
    "education": ["QID14"],
    "ethnicite": ["QID15"],
    "ideologie": ["QID22"],
    "profil_croise": ["QID12", "QID13", "QID22"],
}


def construire_segments(w13):
    """Etiquette de segment par personne, une colonne par segmentation.

    Le profil croise est genre x age x ideologie politique, soit 40 cellules pour
    2 058 personnes. Les cellules trop petites sont neutralisees a l'usage par le
    parametre taille_min de deviance_items, elles ne sont pas fusionnees ici.
    """
    out = pd.DataFrame(index=w13.index)
    for nom, cols in SEGMENTS.items():
        manquant = w13[cols].isna().any(axis=1)
        lab = w13[cols].astype("Int64").astype(str).agg("|".join, axis=1)
        out[nom] = lab.where(~manquant)
    out["population"] = "tous"
    return out


# ---------------------------------------------------------------------------
# Deviance au mode du segment
# ---------------------------------------------------------------------------

def deviance_items(reponses, segment, taille_min=15):
    """Indicatrice, par personne et par item : reponse differente du mode de son segment.

    Le mode est calcule en retirant la personne elle meme du comptage, faute de quoi
    un individu isole dans une petite cellule serait mecaniquement son propre mode et
    ne devierait jamais. En cas d'egalite entre deux modalites, la modalite de code le
    plus petit l'emporte ; c'est arbitraire mais sans effet mesurable, les egalites
    representent moins d'un pour mille des cellules sur ce jeu.

    reponses : DataFrame personnes x items, codes numeriques, NaN pour un manquant.
    segment  : Series alignee sur l'index de reponses, etiquette de segment.
    taille_min : nombre minimal de repondants dans la cellule (personne comprise) pour
                 que la comparaison soit calculee ; sinon NaN.
    Retour : DataFrame de meme forme, valeurs dans {0, 1} ou NaN.
    """
    seg = segment.reindex(reponses.index)
    codes_seg, cellules = pd.factorize(seg, use_na_sentinel=True)
    n_cell = len(cellules)
    sortie = pd.DataFrame(np.nan, index=reponses.index, columns=reponses.columns)
    if n_cell == 0:
        return sortie

    for col in reponses.columns:
        v = reponses[col].to_numpy(dtype=float)
        ok = (~np.isnan(v)) & (codes_seg >= 0)
        if ok.sum() < taille_min:
            continue
        vals = v[ok]
        mods, idx_mod = np.unique(vals, return_inverse=True)
        n_mod = len(mods)
        if n_mod < 2:
            sortie.loc[ok, col] = 0.0
            continue
        cell_ok = codes_seg[ok]
        tab = np.zeros((n_cell, n_mod), dtype=np.int64)
        np.add.at(tab, (cell_ok, idx_mod), 1)
        taille = tab.sum(axis=1)
        lignes = tab[cell_ok].astype(np.int64)
        lignes[np.arange(len(vals)), idx_mod] -= 1
        mode_loo = lignes.argmax(axis=1)
        dev = (mode_loo != idx_mod).astype(float)
        dev[taille[cell_ok] < taille_min] = np.nan
        sortie.loc[ok, col] = dev
    return sortie


def agreger_par_domaine(dev, items, n_min=5):
    """Taux de deviance par personne et par domaine.

    n_min : nombre minimal d'items renseignes dans le domaine pour qu'une personne
    recoive un score ; sinon NaN.
    """
    out = {}
    for dom in ORDRE_DOMAINES:
        cols = [c for c in dev.columns if items.at[c, "domaine"] == dom] if len(items) else []
        if not cols:
            continue
        sub = dev[cols]
        n = sub.notna().sum(axis=1)
        m = sub.mean(axis=1)
        out[dom] = m.where(n >= n_min)
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------
# Psychometrie
# ---------------------------------------------------------------------------

def alpha_cronbach(X):
    """Alpha de Cronbach sur une matrice personnes x items, lignes completes seulement.

    Retourne (alpha, k, n) ou k est le nombre d'items et n le nombre de repondants
    ayant repondu a tous les items.
    """
    Z = np.asarray(X, dtype=float)
    Z = Z[~np.isnan(Z).any(axis=1)]
    n, k = Z.shape
    if n < 10 or k < 2:
        return np.nan, k, n
    var_items = Z.var(axis=0, ddof=1)
    var_total = Z.sum(axis=1).var(ddof=1)
    if var_total <= 0:
        return np.nan, k, n
    return float(k / (k - 1) * (1 - var_items.sum() / var_total)), k, n


def matrice_correlation(df):
    """Correlations de Pearson paire a paire, sur les observations completes de la paire."""
    return df.corr(method="pearson", min_periods=30)


def paires(mat):
    """Vecteur des correlations hors diagonale, avec le nom des deux items."""
    cols = list(mat.columns)
    a, b, r = [], [], []
    for i in range(len(cols)):
        for j in range(i + 1, len(cols)):
            a.append(cols[i]); b.append(cols[j]); r.append(mat.iat[i, j])
    return pd.DataFrame({"item_a": a, "item_b": b, "r": r})


# ---------------------------------------------------------------------------
# BFI-44 : cles de cotation canoniques, verifiees contre les libelles du catalogue
# ---------------------------------------------------------------------------

BFI44 = {
    "extraversion": [1, -6, 11, 16, -21, 26, -31, 36],
    "agreabilite": [-2, 7, -12, 17, 22, -27, 32, -37, 42],
    "conscience": [3, -8, 13, -18, -23, 28, 33, 38, -43],
    "nevrosisme": [4, -9, 14, 19, -24, 29, -34, 39],
    "ouverture": [5, 10, 15, 20, 25, 30, -35, 40, -41, 44],
}


def cle_bfi():
    """Retourne {colonne: (facette, signe)} pour les 44 items du BFI, colonnes QID25_i."""
    d = {}
    for facette, items in BFI44.items():
        for it in items:
            d[f"QID25_{abs(it)}"] = (facette, -1 if it < 0 else 1)
    return d


def stat_desc(x):
    x = pd.Series(x).dropna()
    return dict(n=int(len(x)), moyenne=float(x.mean()), et=float(x.std(ddof=1)),
                p10=float(x.quantile(0.10)), mediane=float(x.median()),
                p90=float(x.quantile(0.90)))
