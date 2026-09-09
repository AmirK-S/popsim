#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Veille bibliographique du projet popsim.

Un script rejouable en une commande. Il interroge l'API arXiv et l'API OpenAlex
sur les sept themes de la cartographie (corpus/00-GRILLE.md), memorise ce qu'il a
deja vu dans data/veille/etat.json, et ne rapporte que les nouveautes.

Zero appel de modele de langage. Les resumes sont les resumes d'origine tronques,
jamais reecrits.

Usage :
    .venv/bin/python analyses/veille.py
    .venv/bin/python analyses/veille.py --depuis 2026-06-01
    .venv/bin/python analyses/veille.py --tout
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_CORPUS = RACINE / "corpus"
FICHIER_ETAT = RACINE / "data" / "veille" / "etat.json"
DOSSIER_RAPPORTS = RACINE / "resultats"

# Premiere execution : on rattrape l'ete 2026.
DEPART_DEFAUT = "2026-06-01"
# Les executions suivantes repartent de la derniere, moins une marge. Les depots
# publient avec du retard et une v2 peut sortir apres coup : sans marge on rate.
# Le doublon ne coute rien, il est ecarte par identifiant.
MARGE_JOURS = 7

CATEGORIES_ARXIV = [
    "cs.CL",
    "cs.CY",
    "cs.AI",
    "stat.AP",
    "econ.GN",
    "physics.soc-ph",
]

COURRIEL_POLI = "amirksmain@gmail.com"
AGENT = "popsim-veille/1.0 (recherche academique; %s)" % COURRIEL_POLI

# Revues visees hors arXiv, identifiants de source OpenAlex.
REVUES_OPENALEX = {
    "S125754415": "PNAS",
    "S2764866340": "Nature Human Behaviour",
    "S29331042": "Political Analysis",
    "S135539873": "Public Opinion Quarterly",
    "S9536269": "Sociological Methods and Research",
    "S95650557": "Journal of Politics",
}


# ---------------------------------------------------------------------------
# Les sept themes de la grille et leurs mots cles de rattachement
# ---------------------------------------------------------------------------

THEMES = {
    "01": {
        "titre": "Simulation d'individus et de populations par LLM, fidelite",
        "fichier": "01-simulation-individus-populations.md",
        "cles": [
            "silicon sampling", "silicon sample", "synthetic respondent",
            "simulated respondent", "survey respondent", "digital twin",
            "generative agent", "persona", "simulate human", "simulating human",
            "human subject", "social simulation", "agent-based", "replicate study",
            "predict survey", "interview", "population simulation", "surrogate",
        ],
    },
    "02": {
        "titre": "Homogeneite, variance, stereotypes, correctifs",
        "fichier": "02-homogeneite-variance-correctifs.md",
        "cles": [
            "homogeneity", "homogenization", "homogenisation", "diversity collapse",
            "variance", "within-group", "between-group", "stereotype", "caricature",
            "flatten", "flattening", "heterogeneity", "misportrayal", "overrepresent",
            "underrepresent", "distributional fidelity", "dispersion", "variability",
            "essentializ", "portrayal",
        ],
    },
    "03": {
        "titre": "Baselines statistiques contre LLM, extension d'enquete",
        "fichier": "03-baselines-statistiques-extension-enquete.md",
        "cles": [
            "baseline", "regression", "multilevel", "poststratification", "mrp",
            "imputation", "matrix completion", "missing data", "prediction accuracy",
            "benchmark", "augment survey", "survey augmentation", "nonresponse",
            "weighting", "inference with synthetic", "design-based", "estimator",
        ],
    },
    "04": {
        "titre": "Desirabilite sociale, effets de mode, opinions cachees",
        "fichier": "04-desirabilite-sociale-opinions-cachees.md",
        "cles": [
            "social desirability", "sensitive question", "preference falsification",
            "self-censorship", "list experiment", "mode effect", "interviewer effect",
            "sensitive topic", "anonymity", "self-report bias", "sincere", "taboo",
            "hidden opinion", "reporting bias", "acquiescence", "self-presentation",
        ],
    },
    "05": {
        "titre": "Structure des attitudes, heterogeneite ideologique, incoherence",
        "fichier": "05-structure-attitudes-heterogeneite-ideologique.md",
        "cles": [
            "attitude network", "belief network", "belief system", "ideological",
            "ideology", "constraint", "polarization", "polarisation", "liberal",
            "conservative", "left-right", "partisan", "issue position", "asymmetr",
            "attitude structure", "opinion structure", "moral foundation",
            "dimensionality of opinion", "network analysis of attitudes",
        ],
    },
    "06": {
        "titre": "Alignement (RLHF), diversite, refus, le dicible",
        "fichier": "06-alignement-diversite-dicible.md",
        "cles": [
            "rlhf", "alignment", "aligned model", "instruction tuning",
            "instruction-tuned", "mode collapse", "diversity", "refusal", "sycophan",
            "preference optimization", "dpo", "reward model", "temperature",
            "creativity", "entropy collapse", "typicality", "safety training",
            "guardrail", "steerability", "opinion distribution",
        ],
    },
    "07": {
        "titre": "Contamination, memorisation, dates de coupure",
        "fichier": "07-contamination-memorisation-coupure.md",
        "cles": [
            "contamination", "memorization", "memorisation", "cutoff",
            "knowledge cutoff", "training data", "leakage", "data leakage",
            "extraction attack", "verbatim", "benchmark contamination", "pretraining corpus",
            "temporal generalization", "recall of training",
        ],
    },
}


# ---------------------------------------------------------------------------
# Requetes
# ---------------------------------------------------------------------------
# Chaque requete arXiv : (libelle, expression de recherche, theme suggere).
# L'expression est combinee avec le filtre de categories.

REQUETES_ARXIV = [
    ("silicon samples", '"silicon sampling" OR "silicon sample" OR "silicon samples"', "01"),
    ("silicon sampling political science", '"silicon sampling" AND (public opinion OR electorate OR voting OR "political science")', "05"),
    ("LLM survey simulation", '("language model" OR LLM) AND ("survey response" OR "survey responses" OR "survey simulation")', "01"),
    ("digital twin survey", '"digital twin" AND (survey OR respondent OR questionnaire OR human)', "01"),
    ("persona simulation respondents", '(persona OR personas) AND (respondent OR respondents OR survey OR questionnaire)', "01"),
    ("simulated participants replication", '("simulated participants" OR "synthetic participants" OR "synthetic respondents" OR "simulated respondents")', "01"),
    ("homogenization diversity LLM opinions", '("language model" OR LLM) AND (homogenization OR homogeneity OR "diversity collapse" OR homogenisation) AND (opinion OR opinions OR attitude)', "02"),
    ("between-group within-group variance LLM", '("within-group" OR "between-group" OR "within group variance") AND ("language model" OR LLM OR persona)', "02"),
    ("stereotype amplification persona", '(stereotype OR stereotypes OR caricature) AND (persona OR personas OR "role-play" OR roleplay)', "02"),
    ("misportrayal sous-populations", '(misportrayal OR misrepresentation OR flattening) AND (subgroup OR subpopulation OR demographic) AND ("language model" OR LLM)', "02"),
    ("baselines statistiques extension enquete", '(survey OR questionnaire) AND ("multilevel regression" OR poststratification OR "matrix completion" OR imputation) AND ("language model" OR LLM)', "03"),
    ("inference avec donnees synthetiques", '("synthetic data" OR "synthetic labels") AND (inference OR estimator OR "confidence interval" OR "valid inference")', "03"),
    ("social desirability LLM", '("social desirability" OR "socially desirable") AND ("language model" OR LLM OR persona OR survey)', "04"),
    ("survey mode effects", '("mode effect" OR "mode effects" OR "interviewer effect" OR "self-administered") AND (survey OR questionnaire OR respondent)', "04"),
    ("preference falsification questions sensibles", '("preference falsification" OR "sensitive questions" OR "list experiment" OR "self-censorship")', "04"),
    ("attitude network polarization", '("attitude network" OR "attitude networks" OR "belief network" OR "belief networks") AND (polarization OR polarisation OR ideology OR opinion)', "05"),
    ("ideological heterogeneity", '("ideological heterogeneity" OR "ideological constraint" OR "belief system") AND (opinion OR attitude OR survey)', "05"),
    ("belief network liberals conservatives", '(liberals OR conservatives OR "left-wing" OR "right-wing") AND (network OR structure) AND (attitude OR attitudes OR belief OR beliefs)', "05"),
    ("asymetrie droite gauche diversite d'opinion", '(asymmetry OR asymmetric) AND (liberal OR conservative OR partisan) AND (opinion OR attitude OR diversity)', "05"),
    ("RLHF diversity collapse", '(RLHF OR "reinforcement learning from human feedback" OR "preference optimization") AND (diversity OR "mode collapse" OR entropy)', "06"),
    ("mode collapse alignment", '("mode collapse" OR "distribution collapse" OR "typicality bias") AND (alignment OR aligned OR "instruction tuning" OR "instruction-tuned")', "06"),
    ("opinions exprimees et refus", '("language model" OR LLM) AND (refusal OR "opinion distribution" OR steerability OR "expressed opinion")', "06"),
    ("data contamination survey benchmark", '("data contamination" OR "benchmark contamination" OR "test set contamination" OR "training data contamination" OR "data leakage") AND (benchmark OR survey OR evaluation OR dataset)', "07"),
    ("memorisation et date de coupure", '("knowledge cutoff" OR "training cutoff" OR "temporal generalization" OR "verbatim memorization")', "07"),
]

# Requetes OpenAlex : (libelle, recherche titre et resume, theme suggere).
REQUETES_OPENALEX = [
    ('silicon samples', '"silicon sampling" OR "silicon samples"', "01"),
    ('repondants synthetiques', '"synthetic respondents" OR "simulated respondents" OR "synthetic participants"', "01"),
    ('LLM et repondants d\'enquete', '"large language model" AND survey respondents', "01"),
    ('jumeau numerique d\'enquete', '"digital twin" AND survey', "01"),
    ('personas et simulation', '"LLM personas" OR "persona prompting"', "01"),
    ('homogeneite et variance', '"language model" AND (homogenization OR "within-group variance")', "02"),
    ('stereotypes et personas', 'stereotype AND persona AND "language model"', "02"),
    ('desirabilite sociale', '"social desirability" AND "language model"', "04"),
    ('effets de mode d\'enquete', '"mode effects" AND survey', "04"),
    ('reseau d\'attitudes et polarisation', '"attitude network" OR "belief network"', "05"),
    ('heterogeneite ideologique', '"ideological heterogeneity" OR "ideological constraint"', "05"),
    ('alignement et diversite', 'RLHF AND diversity', "06"),
    ('contamination des donnees', '"data contamination" AND benchmark', "07"),
    ('opinion publique et LLM', '"large language model" AND public opinion', "05"),
]


# ---------------------------------------------------------------------------
# Filtre de pertinence
# ---------------------------------------------------------------------------
# Les requetes ramenent large, c'est voulu : mieux vaut trop que rater. Ce filtre
# ecarte ensuite ce qui n'a rien a voir avec le projet. Il est volontairement
# permissif, calibre pour privilegier le rappel sur la precision, et il est
# desactivable par --sans-filtre. Ce qu'il ecarte n'entre PAS dans etat.json,
# donc un filtre assoupli plus tard fera reapparaitre ces entrees.

ANCRES = [
    # Le vocabulaire propre au projet. Une seule de ces expressions suffit a
    # retenir l'entree, elles ne veulent rien dire ailleurs.
    "silicon sampling", "silicon subject", "silicon persona",
    "synthetic respondent", "simulated respondent", "synthetic participant",
    "simulated participant", "survey respondent", "human respondent",
    "human surrogate", "surrogate respondent", "surrogate expert",
    "llm persona", "persona prompting", "persona attribute", "demographic persona",
    "synthetic persona", "persona panel",
    "opinion poll", "attitude network", "social desirability",
    "preference falsification", "list experiment", "survey mode",
    "general social survey", "world values survey", "american national election",
    "opinion distribution", "population opinion", "human simulation",
    "simulate human", "simulating human", "simulates human", "social simulation",
    "synthetic population", "algorithmic fidelity", "survey replication",
    "survey simulation", "political attitude", "ideological constraint",
    "ideological heterogeneity", "identity essentialism",
    "stereotype amplification", "survey augmentation", "opinion diversity",
    "digital twin of human",
    # Theme 07 : ces expressions sont techniques, elles n'ont pas besoin de
    # contexte social pour appartenir au corpus.
    "benchmark contamination", "data contamination", "test set contamination",
    "training data contamination", "knowledge cutoff", "verbatim memorization",
    "verbatim memorisation", "training data extraction", "memorization of training",
    "temporal generalization", "training cutoff",
]

PAIRES = [
    (["silicon sample", "silicon samples"],
     ["survey", "respondent", "opinion", "persona", "language model", "llm",
      "social", "consumer", "marketing", "synthetic"]),
    (["persona", "personas"],
     ["survey", "respondent", "opinion", "attitude", "demographic", "stereotype",
      "identity", "sociodemograph", "political", "personality", "census",
      "population", "cultural value"]),
    (["digital twin", "digital twins"],
     ["respondent", "survey", "psychometric", "opinion", "attitude", "persona",
      "citizen", "questionnaire", "personality", "human behavior", "human behaviour"]),
    (["belief network", "belief networks", "attitude networks", "opinion network"],
     ["opinion", "attitude", "political", "ideolog", "polariz", "polaris",
      "survey", "moral", "public"]),
    (["mode collapse", "diversity collapse", "distribution collapse",
      "entropy collapse", "typicality bias", "homogenization", "homogenisation"],
     ["language model", "llm", "alignment", "rlhf", "persona", "generative",
      "output", "response", "opinion"]),
    (["diversity", "output diversity", "response diversity", "cultural alignment",
      "flatten", "flattening", "collapse"],
     ["opinion", "attitude", "persona", "cultur", "demographic", "sociodemograph",
      "population", "survey", "respondent", "moral value", "political"]),
    (["data contamination", "benchmark contamination", "test set contamination",
      "data leakage", "memorization", "memorisation", "knowledge cutoff",
      "training cutoff", "verbatim", "temporal generalization"],
     ["benchmark", "evaluation", "language model", "llm", "survey", "corpus",
      "pretraining", "training data"]),
    (["within-group", "between-group", "within group variance",
      "between group variance", "response variance", "variance of responses",
      "heterogeneity", "dispersion", "variability"],
     ["persona", "respondent", "opinion", "attitude", "survey", "sociodemograph",
      "demographic", "simulated", "synthetic"]),
    (["questionnaire", "respondents", "poll", "polling", "census", "panel study",
      "survey data", "survey item", "survey question"],
     ["persona", "simulat", "synthetic", "agent-based", "language model", "llm"]),
    (["opinion", "opinions", "attitude", "attitudes", "ideolog", "partisan",
      "polarization", "polarisation", "moral foundation", "political value",
      "political values", "cultural value", "cultural values", "public attitude"],
     ["language model", "llm", "gpt", "persona", "simulat", "synthetic",
      "alignment", "rlhf", "generative"]),
]

# Domaines hors sujet. Ecartes seulement si aucune ancre n'est presente.
ANTI = [
    "patient", "clinical", "radiolog", "oncolog", "cancer", "surgeon", "surgical",
    "nursing", "sepsis", "medical diagnosis", "clinical diagnosis", "molecul",
    "nanomaterial", "semiconductor", "wafer", "photovoltaic", "battery",
    "composite material", "wireless", "vanet", "intrusion detection", "malware",
    "cybersecurity", "eeg", "protein", "supply chain", "construction industry",
    "construction project", "construction site", "underwater", "arrhythmia",
    "endometriosis", "crop yield", "traffic flow", "power grid", "manufacturing",
    "drug discovery", "genomic", "astronom", "quantum", "industrial system",
    "industrial process", "mobile robot", "robotic", "jailbreak",
    "code generation", "software engineering", "text-to-sql", "autonomous driving",
    "medical education", "medical imaging", "dental", "seismic", "remote sensing",
    "deepfake", "monocrystal", "laser ablation", "mathematical reasoning",
    "water resources", "energy consumption forecast",
]

# Deuxieme barriere : le texte doit vraiment parler d'humains interroges.
HUMAIN = [
    "survey", "surveys", "questionnaire", "respondent", "respondents", "poll",
    "opinion", "opinions", "attitude", "attitudes", "belief", "beliefs",
    "persona", "personas", "demographic", "sociodemograph",     "political", "ideolog", "partisan", "voter", "electorate", "census",
    "population", "participants", "human subjects", "social science", "sociolog",
    "psycholog", "personality", "values", "culture", "cultural", "identity",
    "stereotype", "public", "citizens", "panel", "interview", "gss", "anes",
    "polarization", "polarisation", "moral", "self-report", "human behavior",
    "human behaviour", "social attitudes", "worldview",
]
SEUIL_HUMAIN = 4

# Ancres moins sures : elles ne suffisent pas seules, elles demandent le seuil humain.
ANCRES_MOLLES = [
            ]


# ---------------------------------------------------------------------------
# Utilitaires
# ---------------------------------------------------------------------------

def normaliser(texte: str) -> str:
    """Minuscules, sans accents, sans ponctuation, espaces simples."""
    if not texte:
        return ""
    texte = unicodedata.normalize("NFKD", texte)
    texte = "".join(c for c in texte if not unicodedata.combining(c))
    texte = texte.lower()
    texte = re.sub(r"[^a-z0-9]+", " ", texte)
    return re.sub(r"\s+", " ", texte).strip()


def tronquer_resume(resume: str, largeur: int = 108, lignes: int = 3) -> str:
    """Le resume d'origine, ramene a trois lignes. Aucune reecriture."""
    if not resume:
        return "(resume absent de la source)"
    plat = re.sub(r"\s+", " ", resume).strip()
    limite = largeur * lignes - 8
    tronque = len(plat) > limite
    if tronque:
        coupe = plat[:limite]
        espace = coupe.rfind(" ")
        if espace > limite * 0.6:
            coupe = coupe[:espace]
        plat = coupe.rstrip(" ,;:.") + " [...]"
    mots = plat.split(" ")
    sorties, courante = [], ""
    for mot in mots:
        if courante and len(courante) + 1 + len(mot) > largeur:
            sorties.append(courante)
            courante = mot
        else:
            courante = (courante + " " + mot).strip()
    if courante:
        sorties.append(courante)
    return "\n".join(sorties[:lignes])


DOSSIER_CACHE = FICHIER_ETAT.parent / "cache"
DUREE_CACHE = 6 * 3600  # six heures, de quoi rejouer une session sans retaper les API


class LimiteAtteinte(RuntimeError):
    """L'API repond 429. On arrete de la solliciter pour cette execution."""


def _chemin_cache(url: str) -> Path:
    import hashlib
    return DOSSIER_CACHE / (hashlib.sha1(url.encode("utf-8")).hexdigest() + ".bin")


def http_get(url: str, essais: int = 3, pause: float = 3.0, cache: bool = True) -> bytes:
    """Un GET poli, avec cache local.

    Le cache sert deux choses : rejouer le script dans la journee sans retaper les
    API, et continuer a repondre quand une API nous limite. Il est dans data/,
    donc jamais versionne."""
    fichier = _chemin_cache(url)
    if cache and fichier.exists() and (time.time() - fichier.stat().st_mtime) < DUREE_CACHE:
        return fichier.read_bytes()

    derniere = None
    limite = False
    for tentative in range(essais):
        requete = urllib.request.Request(url, headers={"User-Agent": AGENT})
        try:
            with urllib.request.urlopen(requete, timeout=60) as reponse:
                contenu = reponse.read()
            if cache:
                DOSSIER_CACHE.mkdir(parents=True, exist_ok=True)
                fichier.write_bytes(contenu)
            return contenu
        except urllib.error.HTTPError as err:
            derniere = err
            if err.code == 429:
                limite = True
                break
            time.sleep(pause * (tentative + 1))
        except (urllib.error.URLError, TimeoutError) as err:
            derniere = err
            time.sleep(pause * (tentative + 1))

    if cache and fichier.exists():
        # Reponse perimee plutot que rien, on le dira dans le rapport.
        return fichier.read_bytes()
    if limite:
        raise LimiteAtteinte("429 sur %s" % url)
    raise RuntimeError("echec reseau sur %s : %s" % (url, derniere))


def rattacher_theme(titre: str, resume: str, suggere: str) -> str:
    """Rattache une entree a un theme du corpus par mots cles.

    On compte des mots cles DISTINCTS, pas des occurrences : sinon un papier qui
    repete quinze fois « persona » atterrit toujours au theme 01, meme quand il
    porte sur l'ecrasement de la variance. Le titre pese trois fois le resume.
    """
    titre_n = normaliser(titre)
    resume_n = normaliser(resume or "")
    scores = {}
    for identifiant, theme in THEMES.items():
        dans_titre = 0
        dans_resume = 0
        for cle in theme["cles"]:
            cle_n = normaliser(cle)
            if not cle_n:
                continue
            if cle_n in titre_n:
                dans_titre += 1
            elif cle_n in resume_n:
                dans_resume += 1
        scores[identifiant] = 3.0 * dans_titre + 1.0 * dans_resume
    if suggere in scores:
        scores[suggere] += 1.0
    meilleur = max(scores.items(), key=lambda paire: (paire[1], paire[0] == suggere))
    if meilleur[1] <= 1.0:
        return suggere
    return meilleur[0]


_CACHE_FILTRE = {}


def _listes_normalisees():
    if not _CACHE_FILTRE:
        _CACHE_FILTRE["dures"] = [(x, normaliser(x)) for x in ANCRES]
        _CACHE_FILTRE["molles"] = [(x, normaliser(x)) for x in ANCRES_MOLLES]
        _CACHE_FILTRE["paires"] = [
            (i, [(a, normaliser(a)) for a in A], [(b, normaliser(b)) for b in B])
            for i, (A, B) in enumerate(PAIRES)
        ]
        _CACHE_FILTRE["anti"] = [(x, normaliser(x)) for x in ANTI]
        _CACHE_FILTRE["humain"] = [normaliser(x) for x in HUMAIN]
    return _CACHE_FILTRE


def est_pertinent(entree: dict, seuil: int = SEUIL_HUMAIN) -> tuple:
    """Le tri grossier entre ce qui touche au projet et ce qui n'y touche pas.

    Trois barrieres, dans cet ordre : une liste de domaines hors sujet, une liste
    d'ancres non ambigues qui suffisent seules, puis des paires de termes qui ne
    valent que si le texte parle assez d'humains interroges. Rend un couple
    (retenu, raison).
    """
    listes = _listes_normalisees()
    texte = normaliser(entree["titre"] + " " + entree["titre"] + " " + (entree.get("resume") or ""))
    for brut, cle in listes["anti"]:
        if cle in texte:
            return False, "hors sujet : %s" % brut
    for brut, cle in listes["dures"]:
        if cle in texte:
            return True, "ancre : %s" % brut
    compte_humain = sum(1 for cle in listes["humain"] if cle in texte)
    for brut, cle in listes["molles"]:
        if cle in texte and compte_humain >= seuil:
            return True, "ancre faible : %s" % brut
    for rang, groupe_a, groupe_b in listes["paires"]:
        touche_a = [brut for brut, cle in groupe_a if cle in texte]
        touche_b = [brut for brut, cle in groupe_b if cle in texte]
        if touche_a and touche_b and compte_humain >= seuil:
            return True, "paire %d : %s et %s" % (rang, touche_a[0], touche_b[0])
    return False, "aucun rattachement, %d marqueurs humains" % compte_humain


# ---------------------------------------------------------------------------
# Index du corpus deja cartographie
# ---------------------------------------------------------------------------

def charger_index_corpus() -> dict:
    """Identifiants arXiv, DOI et texte normalise des fichiers de corpus, lecture complete comprise."""
    index = {"arxiv": set(), "doi": set(), "texte": "", "fichiers": 0}
    morceaux = []
    chemins = sorted(DOSSIER_CORPUS.glob("0[1-7]-*.md")) + sorted(
        (DOSSIER_CORPUS / "lecture-complete").glob("0[1-9]-*.md"))
    for chemin in chemins:
        brut = chemin.read_text(encoding="utf-8", errors="replace")
        index["fichiers"] += 1
        for trouve in re.findall(r"(?:arxiv|arXiv)[\s:/]*(?:abs/)?(\d{4}\.\d{4,5})", brut):
            index["arxiv"].add(trouve)
        for trouve in re.findall(r"10\.\d{4,9}/[^\s\)\]\|,;\"']+", brut):
            index["doi"].add(trouve.rstrip(".,;").lower())
        morceaux.append(normaliser(brut))
    index["texte"] = " ".join(morceaux)
    return index


def est_dans_corpus(entree: dict, index: dict) -> bool:
    if entree.get("arxiv_id") and entree["arxiv_id"] in index["arxiv"]:
        return True
    doi = (entree.get("doi") or "").lower().replace("https://doi.org/", "")
    if doi and doi in index["doi"]:
        return True
    titre = normaliser(entree.get("titre", ""))
    if len(titre) >= 25 and titre in index["texte"]:
        return True
    return False


# ---------------------------------------------------------------------------
# Sources
# ---------------------------------------------------------------------------

NS = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

# Ce qui s'est mal passe pendant l'execution, pour le dire dans le rapport.
ETAT_SOURCES = {"openalex_limite": False, "openalex_echecs": [], "arxiv_echecs": []}


def interroger_arxiv(libelle: str, expression: str, theme: str,
                     depuis: date, par_requete: int = 100, verbeux: bool = True) -> list:
    filtre_cat = " OR ".join("cat:%s" % c for c in CATEGORIES_ARXIV)
    recherche = "(%s) AND (%s)" % (filtre_cat, expression)
    parametres = urllib.parse.urlencode({
        "search_query": recherche,
        "start": 0,
        "max_results": par_requete,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    url = "https://export.arxiv.org/api/query?" + parametres
    try:
        brut = http_get(url)
    except (RuntimeError, LimiteAtteinte) as err:
        ETAT_SOURCES["arxiv_echecs"].append(libelle)
        print("  ! arXiv, requete « %s » : %s" % (libelle, err), file=sys.stderr)
        return []
    try:
        racine = ET.fromstring(brut)
    except ET.ParseError as err:
        print("  ! arXiv, reponse illisible pour « %s » : %s" % (libelle, err), file=sys.stderr)
        return []

    entrees = []
    for noeud in racine.findall("atom:entry", NS):
        lien = (noeud.findtext("atom:id", default="", namespaces=NS) or "").strip()
        correspondance = re.search(r"abs/(\d{4}\.\d{4,5})(v\d+)?", lien)
        if not correspondance:
            continue
        arxiv_id = correspondance.group(1)
        publie = (noeud.findtext("atom:published", default="", namespaces=NS) or "")[:10]
        maj = (noeud.findtext("atom:updated", default="", namespaces=NS) or "")[:10]
        reference = maj if maj > publie else publie
        if reference and reference < depuis.isoformat():
            continue
        auteurs = [
            (a.findtext("atom:name", default="", namespaces=NS) or "").strip()
            for a in noeud.findall("atom:author", NS)
        ]
        categorie = ""
        noeud_cat = noeud.find("arxiv:primary_category", NS)
        if noeud_cat is not None:
            categorie = noeud_cat.get("term", "")
        titre = re.sub(r"\s+", " ", noeud.findtext("atom:title", default="", namespaces=NS)).strip()
        resume = noeud.findtext("atom:summary", default="", namespaces=NS) or ""
        entrees.append({
            "cle": "arxiv:" + arxiv_id,
            "arxiv_id": arxiv_id,
            "doi": "",
            "titre": titre,
            "auteurs": auteurs,
            "date": reference,
            "date_soumission": publie,
            "source": "arXiv %s" % categorie if categorie else "arXiv",
            "url": "https://arxiv.org/abs/%s" % arxiv_id,
            "resume": resume,
            "requetes": [libelle],
            "theme_suggere": theme,
        })
    if verbeux:
        print("  arXiv  %-46s %3d retenues" % (libelle[:46], len(entrees)))
    return entrees


def _entree_openalex(oeuvre: dict, libelle: str, theme: str) -> dict | None:
    titre = (oeuvre.get("title") or "").strip()
    if not titre:
        return None
    source = ((oeuvre.get("primary_location") or {}).get("source") or {})
    nom_source = source.get("display_name") or "source inconnue"
    doi = (oeuvre.get("doi") or "").replace("https://doi.org/", "")
    auteurs = [
        (a.get("author") or {}).get("display_name", "")
        for a in (oeuvre.get("authorships") or [])
    ]
    # OpenAlex ne rend pas le resume en clair, il rend un index inverse.
    resume = ""
    index_inverse = oeuvre.get("abstract_inverted_index")
    if index_inverse:
        positions = {}
        for mot, places in index_inverse.items():
            for place in places:
                positions[place] = mot
        resume = " ".join(positions[k] for k in sorted(positions))
    identifiant = oeuvre.get("id", "").split("/")[-1]
    return {
        "cle": "doi:" + doi.lower() if doi else "openalex:" + identifiant,
        "arxiv_id": "",
        "doi": doi,
        "titre": re.sub(r"\s+", " ", titre),
        "auteurs": [a for a in auteurs if a],
        "date": oeuvre.get("publication_date") or "",
        "date_soumission": oeuvre.get("publication_date") or "",
        "source": nom_source,
        "url": oeuvre.get("doi") or oeuvre.get("id", ""),
        "resume": resume,
        "requetes": [libelle],
        "theme_suggere": theme,
    }


def interroger_openalex(libelle: str, recherche: str, theme: str,
                        depuis: date, filtre_revues: str | None = None,
                        par_page: int = 50, verbeux: bool = True) -> list:
    filtres = [
        "from_publication_date:%s" % depuis.isoformat(),
        "title_and_abstract.search:%s" % recherche,
    ]
    if filtre_revues:
        filtres.append("primary_location.source.id:%s" % filtre_revues)
    else:
        filtres.append("primary_location.source.type:journal")
    parametres = urllib.parse.urlencode({
        "filter": ",".join(filtres),
        "per-page": par_page,
        "sort": "publication_date:desc",
        "mailto": COURRIEL_POLI,
    })
    url = "https://api.openalex.org/works?" + parametres
    if ETAT_SOURCES["openalex_limite"]:
        return []
    try:
        brut = http_get(url, essais=2, pause=8.0)
        charge = json.loads(brut)
    except LimiteAtteinte:
        ETAT_SOURCES["openalex_limite"] = True
        print("  ! OpenAlex nous limite (429). Les requetes OpenAlex restantes sont "
              "abandonnees pour cette execution, le rapport le dira.", file=sys.stderr)
        return []
    except (RuntimeError, json.JSONDecodeError) as err:
        ETAT_SOURCES["openalex_echecs"].append(libelle)
        print("  ! OpenAlex, requete « %s » : %s" % (libelle, err), file=sys.stderr)
        return []
    entrees = []
    for oeuvre in charge.get("results", []):
        entree = _entree_openalex(oeuvre, libelle, theme)
        if entree:
            entrees.append(entree)
    if verbeux:
        print("  OpenAlex %-44s %3d retenues" % (libelle[:44], len(entrees)))
    return entrees


def interroger_semantic_scholar(libelle: str, recherche: str, theme: str,
                                depuis: date, verbeux: bool = True) -> list:
    """Appoint facultatif. L'API publique sans cle refuse souvent, on passe outre."""
    parametres = urllib.parse.urlencode({
        "query": recherche,
        "limit": 20,
        "fields": "title,abstract,publicationDate,authors,externalIds,venue,url",
    })
    url = "https://api.semanticscholar.org/graph/v1/paper/search?" + parametres
    try:
        charge = json.loads(http_get(url, essais=1, pause=2.0))
    except Exception:
        if verbeux:
            print("  Semantic Scholar indisponible sans cle, requete « %s » ignoree" % libelle[:40])
        return []

    entrees = []
    for papier in charge.get("data", []) or []:
        parution = papier.get("publicationDate") or ""
        if not parution or parution < depuis.isoformat():
            continue
        externes = papier.get("externalIds") or {}
        arxiv_id = externes.get("ArXiv") or ""
        doi = (externes.get("DOI") or "")
        cle = "arxiv:" + arxiv_id if arxiv_id else ("doi:" + doi.lower() if doi else None)
        if not cle:
            continue
        entrees.append({
            "cle": cle,
            "arxiv_id": arxiv_id,
            "doi": doi,
            "titre": re.sub(r"\s+", " ", papier.get("title") or ""),
            "auteurs": [a.get("name", "") for a in (papier.get("authors") or [])],
            "date": parution,
            "date_soumission": parution,
            "source": papier.get("venue") or "Semantic Scholar",
            "url": papier.get("url") or "",
            "resume": papier.get("abstract") or "",
            "requetes": [libelle],
            "theme_suggere": theme,
        })
    return entrees


# ---------------------------------------------------------------------------
# Etat
# ---------------------------------------------------------------------------

def charger_etat() -> dict:
    if FICHIER_ETAT.exists():
        try:
            return json.loads(FICHIER_ETAT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("! etat.json illisible, on repart de zero", file=sys.stderr)
    return {"version": 1, "derniere_execution": None, "executions": [], "vus": {}}


def ecrire_etat(etat: dict) -> None:
    FICHIER_ETAT.parent.mkdir(parents=True, exist_ok=True)
    FICHIER_ETAT.write_text(
        json.dumps(etat, ensure_ascii=False, indent=1, sort_keys=True),
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Rapport
# ---------------------------------------------------------------------------

MOTS_ALERTE_RESEAU = [
    "attitude network", "attitude networks", "belief network", "belief networks",
    "opinion network", "opinion networks", "psychological network",
    "network of attitudes", "network of beliefs", "attitudinal network",
]
MOTS_ALERTE_RESEAU_FAIBLE = ["network analysis", "network model", "network structure"]
# Faux amis : ces reseaux la ne sont pas des reseaux d'attitudes.
MOTS_ALERTE_FAUX_AMIS = [
    "bayesian network", "neural network", "deep belief network", "social network analysis",
    "graph neural", "convolutional", "transformer network",
]
MOTS_ALERTE_CAMPS = [
    "liberal", "conservative", "left-wing", "right-wing", "democrat", "republican",
    "partisan", "left and right", "ideological", "political camp", "political spectrum",
    "political belief", "political opinion", "political attitude", "political ideology",
    "political polarization", "political polarisation", "leftist", "rightist", "voter",
]
MOTS_ALERTE_DIVERSITE = [
    "diversity", "heterogeneity", "variance", "dispersion", "polarization",
    "polarisation", "structure", "constraint", "connectedness",
]
MOTS_ALERTE_ATTITUDE = ["attitude", "belief", "opinion", "ideolog", "value"]


def est_alerte(entree: dict) -> bool:
    """L'alerte que Amir a demandee : diversite d'opinion droite contre gauche,
    lue par reseau d'attitudes. On elargit volontairement au voisinage, un faux
    positif se lit en dix secondes, un rate coute une lecture de plus."""
    texte = normaliser(entree["titre"] + " " + (entree.get("resume") or ""))
    # « Belief network » designe aussi un reseau bayesien. Sans mention explicite
    # d'un reseau d'attitudes, un faux ami suffit a ecarter l'entree.
    faux_ami = any(normaliser(m) in texte for m in MOTS_ALERTE_FAUX_AMIS)
    explicite = any(normaliser(m) in texte for m in
                    ["attitude network", "attitude networks", "network of attitudes",
                     "attitudinal network", "opinion network"])
    if faux_ami and not explicite:
        return False
    reseau = any(normaliser(m) in texte for m in MOTS_ALERTE_RESEAU)
    if not reseau:
        faible = any(normaliser(m) in texte for m in MOTS_ALERTE_RESEAU_FAIBLE)
        attitude = any(normaliser(m) in texte for m in MOTS_ALERTE_ATTITUDE)
        reseau = faible and attitude
    if not reseau:
        return False
    camps = any(normaliser(m) in texte for m in MOTS_ALERTE_CAMPS)
    diversite = any(normaliser(m) in texte for m in MOTS_ALERTE_DIVERSITE)
    return camps or diversite


def alerte_camps(entree: dict) -> bool:
    """Vrai quand l'entree oppose explicitement des camps politiques."""
    texte = normaliser(entree["titre"] + " " + (entree.get("resume") or ""))
    return any(normaliser(m) in texte for m in MOTS_ALERTE_CAMPS)


def bloc_entree(entree: dict, manque: bool) -> str:
    auteurs = entree.get("auteurs") or []
    if len(auteurs) > 4:
        liste = ", ".join(auteurs[:4]) + " et al."
    else:
        liste = ", ".join(auteurs) or "auteurs non fournis par la source"
    marque = " **[ABSENT DU CORPUS]**" if manque else ""
    alerte = " **[ALERTE reseau d'attitudes]**" if est_alerte(entree) else ""
    lignes = [
        "#### %s%s%s" % (entree["titre"], marque, alerte),
        "",
        "- Auteurs : %s" % liste,
        "- Date : %s%s" % (
            entree.get("date") or "inconnue",
            "" if not entree.get("date_soumission")
            or entree["date_soumission"] == entree.get("date")
            else " (revision ; premiere soumission le %s)" % entree["date_soumission"]),
        "- Source : %s" % entree.get("source", ""),
        "- URL : %s" % entree.get("url", ""),
        "- Requetes qui l'ont trouve : %s" % ", ".join(sorted(set(entree.get("requetes", [])))),
        "",
        "Resume d'origine, tronque :",
        "",
        "```",
        tronquer_resume(entree.get("resume", "")),
        "```",
        "",
    ]
    return "\n".join(lignes)


def ecrire_rapport(chemin: Path, nouveautes: list, index: dict,
                   depuis: date, tout: bool, etat_avant: str | None,
                   brutes: int = 0, ecartees: int = 0) -> None:
    manques = [e for e in nouveautes if not est_dans_corpus(e, index)]
    alertes = [e for e in nouveautes if est_alerte(e)]
    par_theme = {}
    for entree in nouveautes:
        par_theme.setdefault(entree["theme"], []).append(entree)

    lignes = []
    lignes.append("# Veille popsim, rapport du %s" % date.today().isoformat())
    lignes.append("")
    lignes.append("Produit par `analyses/veille.py`. Sources interrogees : API arXiv "
                  "(categories %s) et API OpenAlex (revues). Zero appel de modele de langage : "
                  "les resumes sont les resumes d'origine tronques, pas des reecritures."
                  % ", ".join(CATEGORIES_ARXIV))
    lignes.append("")
    lignes.append("- Fenetre : depuis le %s" % depuis.isoformat())
    lignes.append("- Execution precedente : %s" % (etat_avant or "aucune, premiere execution"))
    lignes.append("- Mode : %s" % ("tout relister" if tout else "nouveautes seulement"))
    lignes.append("- Entrees ramenees par les requetes : %d, retenues par le filtre de pertinence : %d, "
                  "ecartees comme hors sujet : %d" % (brutes, brutes - ecartees, ecartees))
    lignes.append("- Entrees rapportees : %d" % len(nouveautes))
    lignes.append("- Dont absentes des sept fichiers de corpus : %d" % len(manques))
    lignes.append("- Requetes : %d sur arXiv, %d sur OpenAlex, plus un balayage des six revues visees"
                  % (len(REQUETES_ARXIV), len(REQUETES_OPENALEX)))
    lignes.append("")

    if ETAT_SOURCES["openalex_limite"] or ETAT_SOURCES["openalex_echecs"] or ETAT_SOURCES["arxiv_echecs"]:
        lignes.append("> **Avertissement de couverture.** Ce rapport est incomplet.")
        if ETAT_SOURCES["openalex_limite"]:
            lignes.append("> OpenAlex a repondu 429 et les requetes restantes ont ete abandonnees : "
                          "les revues hors arXiv sont sous representees ici. Relancer plus tard.")
        for libelle in ETAT_SOURCES["openalex_echecs"]:
            lignes.append("> Requete OpenAlex en echec : %s" % libelle)
        for libelle in ETAT_SOURCES["arxiv_echecs"]:
            lignes.append("> Requete arXiv en echec : %s" % libelle)
        lignes.append("")

    lignes.append("## 1. Les manques de la cartographie")
    lignes.append("")
    lignes.append("Entrees qui ne figurent dans AUCUN des sept fichiers de corpus, "
                  "comparaison par identifiant arXiv, par DOI et par titre normalise. "
                  "L'index de comparaison contient %d identifiants arXiv et %d DOI "
                  "tires de %d fichiers." % (len(index["arxiv"]), len(index["doi"]), index["fichiers"]))
    lignes.append("")
    if not manques:
        lignes.append("Aucune. Tout ce qui est sorti sur la fenetre est deja cartographie.")
        lignes.append("")
    else:
        lignes.append("| # | date | titre | source | theme | URL |")
        lignes.append("| --- | --- | --- | --- | --- | --- |")
        for rang, entree in enumerate(sorted(manques, key=lambda e: e["date"], reverse=True), 1):
            lignes.append("| %d | %s | %s | %s | %s | %s |" % (
                rang, entree["date"], entree["titre"].replace("|", "/"),
                entree["source"].replace("|", "/"), entree["theme"], entree["url"]))
        lignes.append("")

    lignes.append("## 2. Alerte demandee : diversite d'opinion droite contre gauche par reseau d'attitudes")
    lignes.append("")
    if not alertes:
        lignes.append("Rien sur la fenetre qui croise reseau d'attitudes ou reseau de croyances "
                      "avec une comparaison entre camps politiques ou une mesure de diversite.")
        lignes.append("")
    else:
        lignes.append("Les entrees marquees CAMPS opposent explicitement des positions "
                      "politiques, ce sont celles a lire en premier.")
        lignes.append("")
        for entree in sorted(alertes, key=lambda e: (alerte_camps(e), e["date"]), reverse=True):
            statut = "absent du corpus" if not est_dans_corpus(entree, index) else "deja dans le corpus"
            marque = "**CAMPS** " if alerte_camps(entree) else "voisinage "
            lignes.append("- %s**%s** (%s, %s, theme %s, %s) %s" % (
                marque, entree["titre"], entree["date"], entree["source"],
                entree["theme"], statut, entree["url"]))
        lignes.append("")

    lignes.append("## 3. Les entrees classees par theme")
    lignes.append("")
    for identifiant in sorted(THEMES):
        entrees = sorted(par_theme.get(identifiant, []), key=lambda e: e["date"], reverse=True)
        lignes.append("### Theme %s. %s" % (identifiant, THEMES[identifiant]["titre"]))
        lignes.append("")
        lignes.append("Fichier de corpus : `corpus/%s`. Entrees : %d."
                      % (THEMES[identifiant]["fichier"], len(entrees)))
        lignes.append("")
        if not entrees:
            lignes.append("Rien de nouveau sur ce theme.")
            lignes.append("")
            continue
        for entree in entrees:
            lignes.append(bloc_entree(entree, not est_dans_corpus(entree, index)))

    lignes.append("## 4. Ce que ce rapport ne couvre pas")
    lignes.append("")
    lignes.append("- Les prepublications hors arXiv (SSRN, OSF, PsyArXiv) ne sont pas interrogees, "
                  "leurs API demandent un compte.")
    lignes.append("- Semantic Scholar est appele en appoint et repond souvent 429 sans cle, "
                  "son absence ne bloque pas l'execution.")
    lignes.append("- OpenAlex indexe la date de publication, pas la date de mise en ligne, "
                  "une revue lente peut donc apparaitre en retard.")
    lignes.append("- Le rattachement au theme est fait par mots cles, pas par lecture. "
                  "Il indique ou ranger, il ne dispense pas de lire.")
    lignes.append("- Le filtre de pertinence est lexical, calibre pour rater le moins possible "
                  "plutot que pour etre propre. Il laisse donc passer du bruit, et il peut "
                  "ecarter a tort un papier dont le resume n'emploie aucun des termes attendus. "
                  "Ce qu'il ecarte n'entre pas dans etat.json : `--sans-filtre` le fait ressortir.")
    lignes.append("")

    chemin.parent.mkdir(parents=True, exist_ok=True)
    chemin.write_text("\n".join(lignes), encoding="utf-8")


# ---------------------------------------------------------------------------
# Programme principal
# ---------------------------------------------------------------------------

def main() -> int:
    analyseur = argparse.ArgumentParser(
        description="Veille bibliographique popsim, arXiv et OpenAlex, sans modele de langage.")
    analyseur.add_argument("--depuis", metavar="AAAA-MM-JJ",
                           help="force la date de depart de la fenetre")
    analyseur.add_argument("--tout", action="store_true",
                           help="relister tout ce que trouvent les requetes, y compris le deja vu")
    analyseur.add_argument("--rapport", metavar="CHEMIN",
                           help="chemin du rapport, par defaut resultats/veille-AAAA-MM-JJ.md")
    analyseur.add_argument("--sans-etat", action="store_true",
                           help="ne pas ecrire etat.json, pour un essai")
    analyseur.add_argument("--sans-filtre", action="store_true",
                           help="ne pas appliquer le filtre de pertinence, tout garder")
    analyseur.add_argument("--semantic-scholar", action="store_true",
                           help="tenter aussi l'API publique Semantic Scholar")
    arguments = analyseur.parse_args()

    etat = charger_etat()
    etat_avant = etat.get("derniere_execution")

    if arguments.depuis:
        try:
            depuis = date.fromisoformat(arguments.depuis)
        except ValueError:
            print("Date invalide : %s, format attendu AAAA-MM-JJ" % arguments.depuis, file=sys.stderr)
            return 2
    elif etat_avant:
        depuis = date.fromisoformat(etat_avant[:10]) - timedelta(days=MARGE_JOURS)
    else:
        depuis = date.fromisoformat(DEPART_DEFAUT)

    print("Veille popsim, fenetre depuis le %s%s" % (depuis.isoformat(), ", mode tout" if arguments.tout else ""))
    print("Etat : %s" % (etat_avant or "aucune execution precedente"))
    print("Requetes arXiv : %d, requetes OpenAlex : %d" % (len(REQUETES_ARXIV), len(REQUETES_OPENALEX)))
    print("")

    brutes = []
    print("Interrogation d'arXiv")
    for libelle, expression, theme in REQUETES_ARXIV:
        brutes.extend(interroger_arxiv(libelle, expression, theme, depuis))
        time.sleep(3.0)  # arXiv demande une requete toutes les trois secondes
    print("")

    print("Interrogation d'OpenAlex")
    for libelle, recherche, theme in REQUETES_OPENALEX:
        brutes.extend(interroger_openalex(libelle, recherche, theme, depuis))
        time.sleep(1.5)  # OpenAlex renvoie 429 si on tape trop vite
    # Balayage des six revues visees, sans mot cle restrictif.
    filtre = "|".join(REVUES_OPENALEX)
    balayages = [
        ("six revues, intelligence artificielle",
         '"large language model" OR "artificial intelligence" OR "generative AI"', "01"),
        ("six revues, opinion et attitudes",
         '"public opinion" OR "survey responses" OR "attitude networks" OR "ideological polarization"', "05"),
    ]
    for libelle, terme, theme_defaut in balayages:
        brutes.extend(interroger_openalex(libelle, terme, theme_defaut,
                                          depuis, filtre_revues=filtre))
        time.sleep(1.5)
    print("")

    if arguments.semantic_scholar:
        print("Interrogation de Semantic Scholar (appoint)")
        for libelle, recherche, theme in REQUETES_OPENALEX[:4]:
            brutes.extend(interroger_semantic_scholar(libelle, recherche, theme, depuis))
            time.sleep(2.0)
        print("")

    # Fusion des doublons entre requetes et entre sources.
    fusionnees = {}
    par_titre = {}
    for entree in brutes:
        cle = entree["cle"]
        titre_n = normaliser(entree["titre"])
        if cle in fusionnees:
            fusionnees[cle]["requetes"].extend(entree["requetes"])
            continue
        if titre_n and len(titre_n) > 25 and titre_n in par_titre:
            fusionnees[par_titre[titre_n]]["requetes"].extend(entree["requetes"])
            continue
        fusionnees[cle] = entree
        if titre_n:
            par_titre[titre_n] = cle

    toutes = list(fusionnees.values())
    if arguments.sans_filtre:
        uniques = toutes
        ecartees = []
    else:
        uniques, ecartees = [], []
        for entree in toutes:
            retenu, raison = est_pertinent(entree)
            entree["raison_filtre"] = raison
            (uniques if retenu else ecartees).append(entree)
    print("Filtre de pertinence : %d entrees brutes, %d retenues, %d ecartees"
          % (len(toutes), len(uniques), len(ecartees)))
    print("")

    deja_vus = set(etat.get("vus", {}))
    if arguments.tout:
        nouveautes = uniques
    else:
        nouveautes = [e for e in uniques if e["cle"] not in deja_vus]

    index = charger_index_corpus()
    for entree in nouveautes:
        entree["theme"] = rattacher_theme(entree["titre"], entree.get("resume", ""),
                                          entree["theme_suggere"])

    manques = [e for e in nouveautes if not est_dans_corpus(e, index)]
    alertes = [e for e in nouveautes if est_alerte(e)]

    print("Resultat")
    print("  entrees distinctes trouvees : %d" % len(uniques))
    print("  deja vues lors d'une execution precedente : %d" % (len(uniques) - len([e for e in uniques if e["cle"] not in deja_vus])))
    print("  NOUVEAUTES rapportees : %d" % len(nouveautes))
    print("  absentes des sept fichiers de corpus : %d" % len(manques))
    print("  alertes reseau d'attitudes : %d" % len(alertes))

    if nouveautes:
        chemin = Path(arguments.rapport) if arguments.rapport else (
            DOSSIER_RAPPORTS / ("veille-%s.md" % date.today().isoformat()))
        if not chemin.is_absolute():
            chemin = RACINE / chemin
        ecrire_rapport(chemin, nouveautes, index, depuis, arguments.tout, etat_avant,
                       len(toutes), len(ecartees))
        try:
            affiche = chemin.relative_to(RACINE)
        except ValueError:
            affiche = chemin
        print("  rapport ecrit : %s" % affiche)
        for entree in sorted(manques, key=lambda e: e["date"], reverse=True)[:10]:
            print("    manque  %s  %s  (%s)" % (entree["date"], entree["titre"][:78], entree["theme"]))
    else:
        print("  rien de nouveau, aucun rapport ecrit, le rapport precedent reste valable")

    if not arguments.sans_etat:
        maintenant = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
        vus = etat.setdefault("vus", {})
        for entree in uniques:
            if entree["cle"] not in vus:
                vus[entree["cle"]] = {
                    "titre": entree["titre"],
                    "date": entree["date"],
                    "source": entree["source"],
                    "url": entree["url"],
                    "vu_le": maintenant,
                }
        # Point important : si une source a flanche, on ne fait PAS avancer la date
        # de derniere execution. Sinon la fenetre mal couverte serait perdue pour
        # toujours, et c'est exactement comme cela qu'on rate un papier.
        complete = not (ETAT_SOURCES["openalex_limite"]
                        or ETAT_SOURCES["openalex_echecs"]
                        or ETAT_SOURCES["arxiv_echecs"])
        if complete:
            etat["derniere_execution"] = maintenant
        etat.setdefault("executions", []).append({
            "quand": maintenant,
            "depuis": depuis.isoformat(),
            "trouvees": len(uniques),
            "nouveautes": len(nouveautes),
            "manques": len(manques),
            "couverture_complete": complete,
            "openalex_limite": ETAT_SOURCES["openalex_limite"],
            "requetes_en_echec": ETAT_SOURCES["openalex_echecs"] + ETAT_SOURCES["arxiv_echecs"],
        })
        ecrire_etat(etat)
        print("  etat mis a jour : %s (%d identifiants memorises)"
              % (FICHIER_ETAT.relative_to(RACINE), len(etat["vus"])))
        if not complete:
            print("  ATTENTION : couverture incomplete pour cette execution.")
            if ETAT_SOURCES["openalex_limite"]:
                print("    OpenAlex a repondu 429, les revues hors arXiv manquent.")
            for libelle in ETAT_SOURCES["openalex_echecs"] + ETAT_SOURCES["arxiv_echecs"]:
                print("    requete en echec : %s" % libelle)
            print("    la date de derniere execution n'a PAS avance : la prochaine "
                  "execution reprendra la meme fenetre. Relancer plus tard.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
