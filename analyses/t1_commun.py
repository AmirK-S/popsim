"""
t1_commun : briques partagees par la replication de la mesure de personne sur
Twin-2K-500.

===========================================================================
CHANTIER t1, 9 septembre 2026.

PREENREGISTREMENT : resultats/t1-preenregistrement.md, ecrit le 9 septembre 2026 a
01 h 08 CEST, AVANT ce fichier et avant tout calcul de resultat.

CE QUE t1 FAIT. a44 a mesure sur le GSS la chute d'exactitude sous permutation des
personnes a l'interieur de leur segment, et en a fait la quantite qui separe le gabarit de
groupe du porteur de personne. a47 a montre que le chiffre depend de la segmentation. a45,
point 10 de sa section des limites, ecrit que la replication sur Twin n'existe pas et que
c'est la premiere chose qu'un relecteur demandera. t1 la fait : 2 058 personnes,
108 items de la vague 4, treize configurations d'agents produites par une autre equipe.

CE QUE t1 NE FAIT PAS. Aucun appel de modele de langage. Aucune simulation nouvelle.
Aucun script existant modifie. Lecture seule sur data/. Rien du GSS n'est recalcule.

CE QUI EST IMPORTE TEL QUEL, sans une ligne recopiee :
  a44_commun.permuter_intra        la permutation des personnes intra segment
  a44_commun.lois_par_segment      les lois du generateur nul et son repli
  a44_commun.tirer_nul             un replicat du generateur nul
  a44_commun.holm                  la correction de Holm
  a44_mesures.exactitude_codes     l'exactitude par personne sur codes entiers
  a44_mesures.reassignation_codes  l'appariement hongrois intra segment
  a1_double_distorsion.construire_index / compter / decomposer / agreger
                                   la chaine de dispersion de a1, employee par a6
  a6_double_distorsion_hors_gss.charger_twin / bloc_ideologie_twin
                                   le chargeur de Twin et la regle des trois blocs
  i3b_twin.charger_twin_commun     les quinze tables dans UNE nomenclature commune
  i3b_commun.ic_pivote             l'intervalle par sous echantillonnage pivote
  a2_commun.*                      les predicteurs statistiques

CE QUI EST NOUVEAU ICI : les quatre segmentations de Twin, le branchement du generateur
nul de a44 sur la chaine de a1, et la transposition de PMM au plan temporel de Twin.
===========================================================================
"""

import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ[_v] = "4"

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a6_double_distorsion_hors_gss as A6      # noqa: E402
import i3b_twin as T3                           # noqa: E402
import i3b_commun as J                          # noqa: E402
import a44_commun as C44                        # noqa: E402
from a44_mesures import exactitude_codes, reassignation_codes  # noqa: E402,F401
from a1_double_distorsion import (              # noqa: E402
    construire_index, compter, decomposer, agreger,
)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
RACINE_TWIN = os.path.join(RACINE, "data", "twin2k500")

GRAINE = 20260909
N_REPLICATS = 200            # replicats du generateur nul
N_PERMUTATIONS = 200         # permutations des personnes intra segment
N_PERM_A1 = 30               # permutations d'etiquettes de segment, population
N_PERM_A1_NUL = 10           # idem, par replicat nul
N_SOUS = 200                 # sous echantillons pour l'IC pivote
N_BOOTSTRAP = 1000           # bootstrap avec remise, exactitude seulement
SEUIL_REPLI = 0.30           # au dela, la ligne du nul est declaree non lisible
SEUIL_GABARIT = 0.15         # part du plancher humain
SEUIL_PERSONNE = 0.40

REF = "humains vague 4"                     # la verite
PLANCHER = "humains vagues 1-3 (retest)"    # le plancher humain

# Les treize configurations, dans l'ordre de llm_specs/index.json.
STATISTIQUES = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]
TEMOINS = ["B0 mode", "B0 tirage"]

ETIQUETTE = {
    "humains vague 4": "humains v4 (verite)",
    "humains vagues 1-3 (retest)": "humains v1-3 (plancher)",
    "Demographics Only - GPT4.1-mini": "Demographics Only",
    "JSON Persona (Predicted Output) - GPT4.1": "JSON PredOut 4.1",
    "JSON Persona (Predicted Output) - GPT4.1-mini": "JSON PredOut mini",
    "JSON Persona - GPT4.1": "JSON Persona 4.1",
    "JSON Persona - GPT4.1-mini": "JSON Persona mini",
    "LLM Finetuning (500 training samples) - GPT4.1-mini": "Finetuning 500",
    "Persona Summary - GPT4.1-mini": "Persona Summary",
    "Persona Summary - JSON Persona - GPT4.1-mini": "Summary + JSON",
    "Text Persona (Default Temperature) - GPT4.1-mini": "Text temp. defaut",
    "Text Persona (Reasoning) - GPT4.1-mini": "Text raisonnement",
    "Text Persona (Repeating Questions) - GPT4.1-mini": "Text repetition",
    "Text Persona - GPT4.1-mini": "Text Persona mini",
    "Text Persona - Gemini-Flash2.5": "Text Persona Gemini",
    "B0 mode": "B0 mode", "B0 tirage": "B0 tirage",
    "B1 argmax": "B1 argmax", "B2 argmax": "B2 argmax", "PMM k=10": "PMM k=10",
}

# Les deux configurations dont le controle de masque de i3b echoue, ecart E4 de i3b.
MASQUE_DOUTEUX = ["JSON Persona (Predicted Output) - GPT4.1-mini",
                  "JSON Persona (Predicted Output) - GPT4.1"]


# ---------------------------------------------------------------------------
# 1. Chargement
# ---------------------------------------------------------------------------

def charger(racine=RACINE_TWIN):
    """Les quinze tables de Twin dans une nomenclature commune, plus tout le materiel
    de mesure : segmentations, valeurs ordinales, demographies brutes, contexte.

    i3b_twin.charger_twin_commun est appelee telle quelle. a6.charger_twin est appelee
    une seconde fois pour recuperer `est_ordinal` et les six axes de a6 sans les
    reconstruire, ce qui coute quatre secondes et evite toute divergence de definition.
    """
    paq = T3.charger_twin_commun(racine)
    jeux, _ = A6.charger_twin(racine)
    base = jeux[0]
    assert list(base["items"]) == list(paq["colonnes"]), \
        "l'ordre des items de a6 et de i3b differe, tout le reste serait faux"

    paq["est_ordinal"] = base["est_ordinal"]
    paq["axes_a6"] = base["axes"]
    paq["seg_a6"] = {a: base["seg"][a].astype(np.int32) for a in base["axes"]}
    paq["niveaux_a6"] = base["niveaux"]

    # Valeurs ordinales dans [0, 1], meme regle que a6 : seuls les items de type Matrix
    # portent un ordre, et il est celui de la nomenclature commune.
    k_max = int(max(len(m) for m in paq["modalites"]))
    val_ord = np.zeros((len(paq["colonnes"]), k_max))
    for j, m in enumerate(paq["modalites"]):
        if paq["est_ordinal"][j] and len(m) > 1:
            val_ord[j, :len(m)] = np.arange(len(m)) / (len(m) - 1)
    paq["k_max"] = k_max
    paq["val_ord"] = val_ord
    paq["garder"] = np.ones(len(paq["colonnes"]), dtype=bool)

    paq["seg"], paq["niveaux_seg"] = segmentations(paq, racine)
    paq["demo"] = demographies_brutes(paq, racine)
    return paq


def _labels(racine, ids):
    """Le fichier de libelles des vagues 1 a 3, aligne sur l'ordre des ids de Twin."""
    p = os.path.join(racine, "question_catalog_and_human_response_csv",
                     "wave1_3_response_label.csv")
    d = pd.read_csv(p, low_memory=False)
    d = d.set_index("pid")
    return d.reindex(ids)


def _coder_cle(cle):
    """Une liste de chaines devient un vecteur de segments, -1 pour vide. Regle de a6."""
    mods = sorted({v for v in cle if v.strip() != ""})
    idx = {m: k for k, m in enumerate(mods)}
    return np.array([idx.get(v, -1) for v in cle], dtype=np.int32), mods


def segmentations(paq, racine=RACINE_TWIN):
    """Les quatre segmentations declarees au preenregistrement section 4.

    S_ideo  : QID22, ideologie a cinq niveaux. Analogue exact du `S_ideo` du GSS.
    S_fin   : bloc d'ideologie x genre x age, fine et CONTENANT l'ideologie.
    S_gra   : genre x ethnicite x age, fine et SANS ideologie. C'est la lecture que
              a47 E2 impose comme principale sur le GSS.
    S_parti : QID20, parti a quatre niveaux. Twin l'a, le GSS de a44 ne l'avait pas.
    """
    lab = _labels(racine, paq["ids"])

    def col(q):
        return [("" if pd.isna(v) else str(v).strip()) for v in lab[q].values]

    genre, ethnie, age = col("QID12"), col("QID15"), col("QID13")
    ideo, parti = col("QID22"), col("QID20")
    bloc = [A6.bloc_ideologie_twin(v) if v else "" for v in ideo]

    seg, niv = {}, {}
    seg["S_ideo"], niv["S_ideo"] = _coder_cle(ideo)
    seg["S_parti"], niv["S_parti"] = _coder_cle(parti)
    seg["S_fin"], niv["S_fin"] = _coder_cle(
        [f"{b}|{g}|{a}" if b and g and a else "" for b, g, a in zip(bloc, genre, age)])
    seg["S_gra"], niv["S_gra"] = _coder_cle(
        [f"{g}|{e}|{a}" if g and e and a else "" for g, e, a in zip(genre, ethnie, age)])
    return seg, niv


def demographies_brutes(paq, racine=RACINE_TWIN):
    """Les quatorze questions du bloc Demographics et les 494 items de contexte.

    CONTEXTE : les colonnes categorielles des vagues 1 a 3 qui ne sont PAS reposees en
    vague 4. Decoupage de a2_baselines_twin, repris sans changement : garder les colonnes
    reposees donnerait au predicteur la reponse anterieure de la personne a la question
    meme qu'on lui demande de predire.
    """
    csvd = os.path.join(racine, "question_catalog_and_human_response_csv")
    cat = json.load(open(os.path.join(csvd, "question_catalog.json"), encoding="utf-8"))
    c2q = {}
    for q in cat:
        for c in q.get("csv_columns", []):
            c2q.setdefault(c, q)
    w13 = pd.read_csv(os.path.join(csvd, "wave1_3_response.csv"), low_memory=False)
    w4 = pd.read_csv(os.path.join(csvd, "wave4_response.csv"), low_memory=False)
    assert list(w13["pid"]) == list(w4["pid"])
    assert list(w13["pid"]) == list(paq["ids"]), \
        "l'ordre des personnes de a2 et de a6 differe"

    def categorielle(c):
        q = c2q.get(c)
        if q is None:
            return False
        if q["QuestionType"] == "Matrix":
            return True
        return (q["QuestionType"] == "MC"
                and q.get("Settings", {}).get("Selector") in ("SAVR", "SAHR"))

    reposees = {c for c in w4.columns if c != "pid" and c in w13.columns}
    contexte = [c for c in w13.columns
                if c != "pid" and c not in reposees and categorielle(c)]
    demo = [c for c in w13.columns
            if c2q.get(c) is not None
            and c2q[c]["BlockName"].strip() == "Demographics"]
    return {"x": w13[demo].fillna("non renseigne").astype(str).values,
            "ctx": w13[contexte].values.astype(object),
            "colonnes_demo": demo, "colonnes_contexte": contexte}


# ---------------------------------------------------------------------------
# 2. Perimetres
# ---------------------------------------------------------------------------

def perimetres(paq):
    """A chaque condition, les lignes sur lesquelles elle est mesuree.

    Regle de a6 et interdit 4 de a44 : une configuration qui ne couvre pas les 2 058
    sujets est mesuree sur les siens, avec le plancher humain recalcule sur les memes
    personnes. Aucune valeur absolue n'est comparee d'un perimetre a l'autre.
    """
    out = {}
    for nom, cv in paq["couverture"].items():
        out[nom] = np.asarray(cv, dtype=int)
    return out


# ---------------------------------------------------------------------------
# 3. La chaine de dispersion de a1, branchee sur un axe
# ---------------------------------------------------------------------------

def chaine_a1(codes, seg_axes, axes, paq, n_perm=0, rng=None, axes_gardes=None,
              mesure="entropie"):
    """(inter, intra) apres correction par permutation des etiquettes de segment.

    C'est exactement la chaine de a1 employee par a6 : construire_index, compter,
    decomposer, agreger, puis soustraction de la moyenne des permutations. Rien n'est
    reecrit ; seul l'appel est ici.

    ATTENTION, convention de a6 reproduite a la lettre : la correction par permutation ne
    s'applique qu'au terme INTER. C'est ce que fait `a6.analyser`, ligne
    `point = {c: {m: (observe[c][m][0] - nul[c][m], observe[c][m][1]) ...}` : le second
    element du couple, le terme intra, n'est pas corrige. La raison est dans a1 : sous
    permutation des etiquettes de segment, l'information mutuelle doit valoir zero et ce
    qui subsiste est du biais d'estimation ; le terme intra, lui, tend vers la dispersion
    totale et sa permutation ne mesure aucun biais.
    """
    n_items = codes.shape[1]
    k_max, val_ord = paq["k_max"], paq["val_ord"]
    est_ord, garder = paq["est_ordinal"], paq["garder"]
    g_max = int(max(int(seg_axes[a].max()) + 1 for a in axes))
    lignes = np.arange(codes.shape[0])

    def mesurer(sg):
        idx, pb = construire_index(codes, sg, k_max, g_max, n_items, axes=axes)
        d = decomposer(compter(idx, lignes, pb, n_items, g_max, k_max, len(axes)),
                       val_ord)
        return agreger(d, garder, est_ord, axes_gardes=axes_gardes)[mesure]

    inter, intra = mesurer(seg_axes)
    if n_perm and rng is not None:
        vi = []
        for _ in range(n_perm):
            p = rng.permutation(codes.shape[0])
            vi.append(mesurer({a: seg_axes[a][p] for a in axes})[0])
        inter -= float(np.mean(vi))
    return float(inter), float(intra)


# ---------------------------------------------------------------------------
# 4. Intervalles
# ---------------------------------------------------------------------------

def ic_bootstrap_moyenne(valeurs, b=N_BOOTSTRAP, graine=GRAINE):
    """Bootstrap avec remise sur les personnes. ADMISSIBLE UNIQUEMENT pour une moyenne
    par personne, cf. preenregistrement section 7 et le controle de i3b sur le biais du
    tirage avec remise."""
    v = np.asarray(valeurs, dtype=float)
    v = v[np.isfinite(v)]
    if not len(v):
        return np.nan, np.nan, np.nan
    rng = np.random.default_rng(graine)
    t = rng.choice(v, size=(b, len(v)), replace=True).mean(axis=1)
    return float(v.mean()), float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5))


def ic_sous_echantillonnage(fonction, n, centre, s=N_SOUS, part=0.5, graine=GRAINE):
    """IC a 95 pour cent par sous echantillonnage pivote, avec correction de population
    finie. i3b_commun.ic_pivote et i3b_commun.correction_population_finie sont appelees
    telles quelles.

    fonction(idx) -> valeur, ou idx est un vecteur d'indices de personnes.
    """
    rng = np.random.default_rng(graine)
    m = max(int(round(part * n)), 2)
    tirages = []
    for _ in range(s):
        idx = np.sort(rng.permutation(n)[:m])
        tirages.append(fonction(idx))
    echelle = np.sqrt(m / n) * J.correction_population_finie(m, n)
    bas, haut, et = J.ic_pivote(tirages, centre=centre, echelle=echelle)
    return bas, haut, et


def ecrire(lignes, nom):
    chemin = os.path.join(SORTIE, nom)
    pd.DataFrame(lignes).to_csv(chemin, index=False)
    print(f"ecrit {chemin}, {len(lignes)} lignes", flush=True)
    return chemin


def holm(p):
    return C44.holm(p)
