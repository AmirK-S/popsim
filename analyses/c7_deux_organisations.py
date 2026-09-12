"""
c7_deux_organisations : le temoin "deux organisations independantes" pour A7 (T2).

===========================================================================
PREENREGISTREMENT : resultats/c7-deux-organisations-preenregistrement.md, ecrit le
12 septembre 2026, AVANT tout appel payant. Plan de conception, ecrit avant ce fichier
et avant tout appel reseau : resultats/c7-temoin-deux-organisations-plan.md.

CE QUE CE SCRIPT FAIT. A7 (T2 du manuscrit) revendique qu'un jumeau publie par une
organisation peut etre reidentifie par comparaison avec un jumeau publie par une AUTRE
organisation de la meme personne. Le T2 deja publie n'oppose que des configurations
Twin-2K-500 de la MEME equipe, a partir des MEMES fichiers de persona sources. Ce script
construit deux pipelines de generation mutuellement independants — modele different,
gabarit de prompt different, format de persona different — a partir des memes reponses
brutes de 200 personnes de Twin-2K-500, puis rejoue l'attaque B<->C avec le code de mesure
deja publie, importe sans une ligne recopiee.

  Organisation B : deepseek/deepseek-v4-flash, persona en dossier JSON structure,
                   systeme + utilisateur (deux tours), sortie "identifiant: option".
  Organisation C : qwen/qwen-2.5-72b-instruct (Alibaba, fournisseur DeepInfra),
                   persona en biographie narrative en prose, un seul tour utilisateur,
                   sortie en liste de nombres separes par des virgules, sans identifiant.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                 les quinze tables de Twin, dont S_gra et les
                                     reponses brutes de demographie/contexte
  t1_commun._labels                 le fichier de libelles decodes des vagues 1-3
  c7_reidentification.items_communs les 60 items toujours renseignes (memes que le T2
                                     deja publie, pour rester comparable chiffre pour
                                     chiffre)
  c7_reidentification.rangs_attaque l'attaque de reidentification (rang, top1, top10),
                                     ordre des candidats melange, bruit i.i.d.
  c7_reidentification.rang_dans_segment  le controle anti-artefact sur S_gra
  c7_reidentification.graine_nom    une graine stable par nom de configuration
  a2_commun.distance_hamming        la distance de Hamming normalisee, masquage inclus
  a2_commun.bootstrap_personnes     l'intervalle de confiance par reechantillonnage
                                     de personnes

CE QUI EST NOUVEAU ICI : le tirage stratifie de 200 personnes, la construction des deux
personas (JSON structure / biographie narrative) a partir des reponses brutes, les deux
gabarits de prompt et leurs deux parseurs de sortie, le client HTTP minimal vers
OpenRouter (autonome, n'importe rien de r6_oracle_distant.py), et le calcul de la
baseline Demographics Only et du controle de segment RECALCULES sur le meme pool de 200
personnes (jamais la valeur publiee sur les 2 058 personnes).

DEVIATION DECLAREE #1 PAR RAPPORT AU PLAN (section 3) : le plan donne un exemple de gabarit
B ou l'organisation repond par "l'etiquette exacte d'une option". Ce script demande a la
place le NUMERO de l'option (1..k), pour les deux organisations, parce qu'un parseur par
motif de texte libre sur une etiquette anglaise recopiee ou paraphrasee est fragile (une
reformulation minime rendrait le parse informatif d'un signal qui n'est pas le signal
mesure) alors qu'un entier est sans ambiguite. La difference de STRUCTURE que le plan
veut proteger reste entiere : B repond une ligne par question prefixee d'un identifiant
("Q07: 3"), C repond une liste positionnelle sans aucun identifiant ("3, 1, 4, ...") ;
aucune convention de mise en forme commune entre B et C ne pourrait donc, a elle seule,
devenir le canal.

DEVIATION DECLAREE #2 (persona narrative, cf. commentaire dans persona_narrative) : le
plan illustre un paragraphe narratif qui restitue les reponses "sans etiquette de champ".
Rediger une phrase grammaticale distincte, sans jamais nommer le champ, pour chacun des
494 champs heterogenes de contexte est hors de portee du temps imparti (494 gabarits de
phrase differents) sans passer par un appel de modele supplementaire par personne, ce qui
doublerait le cout et le nombre d'appels. Le compromis : chaque reponse reste reperee par
l'identifiant du champ (QID), mais enchassee dans UNE seule phrase au fil, a la premiere
personne, les items separes par des virgules -- jamais un objet JSON, jamais d'accolades
ni de guillemets de cle. La structure reste mesurablement differente de celle de B (objet
JSON complet, gabarit systeme/utilisateur en deux tours) tout en restant a cout comparable.

DEVIATION DECLAREE #3 (format de sortie C, cf. commentaire dans prompt_c) : le premier
pilote reel (2 personnes) a montre qu'une reponse en UNE SEULE liste de 60 nombres
separes par des virgules, sans aucun repere par question -- l'exemple litteral du plan --
degenere systematiquement en boucle de repetition ("2,2,2,2,...") a partir d'une
vingtaine d'items, reproduit a l'identique sur trois modeles de trois fournisseurs
distincts testes en verification (qwen-2.5-72b, llama-3.3-70b, mistral-small-3.2) : un
defaut de FORMAT, pas du modele retenu. Le format final ancre chaque reponse sur sa
propre ligne par son numero brut ("60) 7"), ce qui fait disparaitre la boucle sans
rapprocher la structure de C de celle de B : jamais la lettre "Q", jamais les deux
points, jamais de tour systeme, persona narrative au lieu du dossier JSON.

ETHIQUE : aucun pid Twin-2K-500 n'est jamais imprime, trace ou ecrit dans une sortie
publique ; seul un index d'echantillon 0..199 identifie une personne dans les traces et
le CSV. Donnees d'entree deja publiques (Twin-2K-500) ; aucune sortie individuelle,
seuls des taux agreges et des IC sortent dans resultats/.

Depense : appel reseau reel vers OpenRouter, cout facture. Plafond dur de la tache :
1,00 USD. Arret interne si le cumul mesure (usage.cost annonce, jamais une estimation)
depasse ARRET_INTERNE_USD. Un HTTP 429 porteur d'un identifiant de generation arrete le
script immediatement (aucune relance improvisee, cf. mission) ; le fichier
data/traces/STOP, s'il existe, est aussi respecte en lecture seule avant chaque appel.

Sortie : resultats/c7-deux-organisations.csv, resultats/c7-deux-organisations-resultats.md,
         data/traces/c7-deux-organisations.jsonl (une ligne par appel reussi ou rejete).
Usage :
  .venv/bin/python analyses/c7_deux_organisations.py --essai 3   # pilote, 3 personnes
  .venv/bin/python analyses/c7_deux_organisations.py             # campagne, 200 personnes
===========================================================================
"""

import argparse
import datetime
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from decimal import Decimal

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                    # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes               # noqa: E402
from c7_reidentification import (                                          # noqa: E402
    items_communs, rangs_attaque, rang_dans_segment, graine_nom,
    REF_V4, REF_V13, DEMO, N_BOOTSTRAP, N_TIRAGES_LIENS,
)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
TRACES = os.path.join(RACINE, "data", "traces")
CATALOGUE_QUESTIONS = os.path.join(
    RACINE, "data", "twin2k500", "question_catalog_and_human_response_csv",
    "question_catalog.json")
MAPPING_WAVE4 = os.path.join(RACINE, "data", "twin2k500", "llm",
                              "wave4_formatted_to_catalog_mapping.json")

FICHIER_ARRET_GLOBAL = os.path.join(TRACES, "STOP")     # lecture seule uniquement
TRACE_JSONL = os.path.join(TRACES, "c7-deux-organisations.jsonl")

GRAINE = 20260912
N_PERSONNES = 200

MODELE_B = "deepseek/deepseek-v4-flash"
FOURNISSEUR_B = "DigitalOcean"
MAX_PRICE_B = {"prompt": 0.11, "completion": 0.22}     # $ / 1M jetons, convention OpenRouter

MODELE_C = "qwen/qwen-2.5-72b-instruct"
FOURNISSEUR_C = "DeepInfra"
MAX_PRICE_C = {"prompt": 0.60, "completion": 0.80}     # marge au dessus du prix catalogue

PLAFOND_DUR_USD = Decimal("1.00")           # plafond de la mission, jamais depasse
ARRET_INTERNE_USD = Decimal("0.90")         # marge de securite avant le plafond dur
MAX_TOKENS_B = 500      # "Q60: 5" x 60 lignes, ~6 jetons/ligne mesures au pilote + marge
MAX_TOKENS_C = 500      # "60) 7" x 60 lignes, meme ordre de grandeur que B
# Trouve au premier pilote (2 personnes, cf. resultats/c7-deux-organisations-resultats.md) :
# une reponse en UNE SEULE liste de 60 nombres separes par des virgules, sans aucun
# repere par question, degenere systematiquement en boucle de repetition ("2,2,2,...")
# a partir d'une vingtaine d'items -- reproduit a l'identique sur trois modeles de trois
# fournisseurs distincts (qwen, llama-3.3-70b, mistral-small-3.2), donc un defaut de
# FORMAT et non du modele. Le format C retenu (prompt_c, parser_c) ancre chaque reponse
# sur sa propre ligne par son numero brut, ce qui fait disparaitre la boucle sans
# reduire la difference de structure avec B (jamais la lettre « Q », jamais les deux
# points, jamais le tour systeme). Aucune penalite de repetition n'est donc necessaire ;
# EXTRA_C reste disponible mais vide, pour ne pas modifier le decodage sans raison.
EXTRA_C = None

BASE = "https://openrouter.ai/api/v1"


# ---------------------------------------------------------------------------------------
# 1. Client HTTP minimal, autonome (n'importe rien de r6_oracle_distant.py)
# ---------------------------------------------------------------------------------------

def cle_api():
    chemin = os.path.join(RACINE, ".env")
    if not os.path.exists(chemin):
        sys.exit(f"fichier absent : {chemin}")
    for ligne in open(chemin, encoding="utf-8"):
        if ligne.startswith("OPENROUTER_API_KEY="):
            v = ligne.split("=", 1)[1].strip().strip('"').strip("'")
            if v:
                return v
    sys.exit("OPENROUTER_API_KEY absente de .env")


def entetes(cle):
    return {"Authorization": "Bearer " + cle, "Content-Type": "application/json",
            "HTTP-Referer": "popsim", "X-Title": "popsim"}


def entetes_diagnostic(entetes_http):
    if entetes_http is None:
        return {}
    recus = {str(k).lower(): str(v).strip()[:512] for k, v in entetes_http.items()}
    familles = {"generation_id": ("x-generation-id", "x-openrouter-generation-id"),
                "request_id": ("x-request-id", "x-openrouter-request-id", "request-id")}
    out = {}
    for sortie, noms in familles.items():
        for nom in noms:
            if recus.get(nom):
                out[sortie] = recus[nom]
                break
    return out


class Arret429(SystemExit):
    pass


def appeler_chat(cle, modele, messages, fournisseur, max_price, max_tokens, timeout=180,
                 extra=None):
    """Un appel, aucune relance. Un 429 avec identifiant de generation arrete le script
    (protocole de rapprochement du projet, pas improvise ici, cf. docstring)."""
    charge = {
        "model": modele, "messages": messages, "temperature": 0.0,
        "max_tokens": max_tokens,
        "usage": {"include": True},
        "provider": {"order": [fournisseur], "allow_fallbacks": False,
                     "max_price": {k: float(v) for k, v in max_price.items()}},
    }
    if extra:
        charge.update(extra)
    donnees = json.dumps(charge).encode("utf-8")
    req = urllib.request.Request(BASE + "/chat/completions", data=donnees,
                                 headers=entetes(cle))
    debut = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            corps = json.loads(r.read().decode("utf-8"))
            entetes_reponse = r.headers
    except urllib.error.HTTPError as e:
        diag = entetes_diagnostic(e.headers)
        if e.code == 429:
            print(f"\nHTTP 429 recu. diagnostic (sans secret) : {diag}", flush=True)
            if diag.get("generation_id"):
                raise Arret429(
                    "HTTP 429 porteur d'un identifiant de generation "
                    f"({diag['generation_id']}) : arret immediat, protocole de "
                    "rapprochement du projet requis, non improvise ici.")
            raise Arret429("HTTP 429 sans identifiant de generation exploitable : "
                           "arret par prudence.")
        return {"erreur": f"HTTP {e.code}", "diagnostic": diag,
                "duree_ms": (time.perf_counter() - debut) * 1000.0}
    except Exception as e:
        return {"erreur": type(e).__name__, "duree_ms": (time.perf_counter() - debut) * 1000.0}
    duree = (time.perf_counter() - debut) * 1000.0
    if corps.get("error"):
        diag = entetes_diagnostic(entetes_reponse)
        return {"erreur": "erreur du fournisseur", "detail": corps["error"],
                "diagnostic": diag, "duree_ms": duree}
    choix = (corps.get("choices") or [{}])[0]
    usage = corps.get("usage") or {}
    message = choix.get("message") or {}
    return {
        "texte": message.get("content") or "",
        "raison": choix.get("finish_reason"),
        "fournisseur_reel": corps.get("provider"),
        "jetons_entree": usage.get("prompt_tokens"),
        "jetons_sortie": usage.get("completion_tokens"),
        "cout_annonce": usage.get("cost"),
        "duree_ms": duree,
    }


class Budget:
    def __init__(self, plafond, arret_interne):
        self.plafond = plafond
        self.arret_interne = arret_interne
        self.cumul = Decimal("0")
        self.n_appels = 0

    def verifier_avant_appel(self):
        if self.cumul >= self.arret_interne:
            sys.exit(f"arret interne de securite : cumul {self.cumul} USD >= "
                      f"{self.arret_interne} USD (plafond dur {self.plafond} USD)")

    def ajouter(self, cout_annonce):
        if cout_annonce is None:
            return
        c = Decimal(str(cout_annonce))
        self.cumul += c
        self.n_appels += 1
        if self.cumul >= self.plafond:
            sys.exit(f"PLAFOND DUR ATTEINT : {self.cumul} USD >= {self.plafond} USD, arret")


# ---------------------------------------------------------------------------------------
# 2. Banque des 60 items cibles, construite a partir du catalogue de questions
# ---------------------------------------------------------------------------------------

FR_QID = {
    "QID11": "région", "QID12": "sexe déclaré à la naissance", "QID13": "âge",
    "QID14": "niveau d'études", "QID15": "origine", "QID16": "citoyenneté",
    "QID17": "situation familiale", "QID18": "religion", "QID19": "pratique religieuse",
    "QID20": "parti", "QID21": "revenu du foyer", "QID22": "idéologie",
    "QID23": "taille du foyer", "QID24": "emploi",
}

RE_PRODUIT = re.compile(
    r"category:\s*(.*?)\.\s*Suppose.*?category:\s*(.*?)\.\s*The product is priced at:\s*"
    r"(\$[0-9.,]+)\.", re.DOTALL)


def _c2q(catalogue):
    out = {}
    for q in catalogue:
        for c in q.get("csv_columns", []):
            out.setdefault(c, q)
    return out


def construire_banque_items(paq):
    """Les 60 items cibles, dans l'ordre d'items_communs, avec texte et options en
    francais (le contenu substantiel des items -- politiques, produits, scenarios --
    reste dans son libelle d'origine, en anglais, pour ne pas introduire d'erreur de
    traduction sur le contenu qui est effectivement mesure)."""
    catalogue = json.load(open(CATALOGUE_QUESTIONS, encoding="utf-8"))
    c2q = _c2q(catalogue)
    mapping = json.load(open(MAPPING_WAVE4, encoding="utf-8"))
    col2cat = {e["formatted_column"]: e for e in mapping}

    idx_items = items_communs(paq["codes"], [REF_V4, REF_V13])
    cols = [paq["colonnes"][i] for i in idx_items]

    items = []
    for col in cols:
        catcol = col2cat[col]["catalog_csv_column"]
        q = c2q[catcol]
        if q["QuestionType"] == "Matrix":
            pos = q["csv_columns"].index(catcol)
            row = q["Rows"][pos]
            opts = list(q["Columns"])
            if q["QuestionID"] == "QID287":
                texte = f"Favorable ou opposé(e) à : {row}"
            elif q["QuestionID"] == "QID288":
                texte = f"Bénéfice de : {row} ?"
            elif q["QuestionID"] == "QID289":
                texte = f"Risque de : {row} ?"
            else:
                texte = row
        else:
            m = RE_PRODUIT.search(q["QuestionText"])
            if m:
                categorie, produit, prix = m.groups()
                texte = f"Achèterais-tu ceci ({categorie}) : {produit}, {prix} ?"
            else:
                texte = q["QuestionText"]
            opts = list(q["Options"])
        items.append({"col": col, "texte": texte, "options": opts})
    return idx_items, items


# ---------------------------------------------------------------------------------------
# 3. Persona : dossier JSON (organisation B) et biographie narrative (organisation C)
# ---------------------------------------------------------------------------------------

def charger_labels(paq):
    """Les libelles decodes des vagues 1-3, alignes sur paq['ids'] : t1_commun._labels,
    appelee telle quelle, sans une ligne recopiee."""
    return T1._labels(T1.RACINE_TWIN, paq["ids"])


def persona_champs(lab, i, colonnes):
    """{colonne: libelle texte} pour la personne d'index i, manquants explicites."""
    ligne = lab.iloc[i]
    out = {}
    for c in colonnes:
        v = ligne[c]
        out[c] = "non renseigné" if pd.isna(v) else str(v).strip()
    return out


def persona_json(champs):
    return json.dumps(champs, ensure_ascii=False, separators=(",", ":"))


def persona_narrative(champs, colonnes_demo):
    """Biographie en prose, aucune structure cle/valeur visible (pas d'accolade, pas de
    guillemet de cle, pas de deux-points de type JSON)."""
    intro = []
    for c in colonnes_demo:
        if c in champs:
            intro.append(f"ta {FR_QID.get(c, c)} déclarée est {champs[c]}")
    phrase_intro = ("Voici qui tu es : " + ", ".join(intro) + ".") if intro else ""

    # DEVIATION DECLAREE (cf. docstring, "persona narrative") : le plan illustre un
    # paragraphe qui restitue les 494 reponses "sans etiquette de champ". Ecrire une
    # phrase grammaticale distincte pour chacun des 494 champs heterogenes, sans jamais
    # nommer le champ, exigerait soit un gabarit ecrit a la main par question (494
    # questions de types tres divers, hors de portee du temps imparti), soit un appel de
    # modele supplementaire par personne pour reecrire la biographie (ce qui doublerait
    # le nombre d'appels et le cout, contrairement au plan section 1 : "un seul appel de
    # generation par personne et par organisation"). Le compromis retenu : chaque reponse
    # reste reperee par son identifiant de champ, mais enchassee dans UNE seule phrase
    # au fil, a la premiere personne, separee par des virgules -- jamais par un objet
    # JSON, jamais entre accolades ni guillemets de cle. C'est mesurablement distinct de
    # la structure de B (un objet JSON complet) tout en restant a cout comparable.
    reste = [c for c in champs if c not in colonnes_demo]
    clauses = [f"{c} : {champs[c]}" for c in reste]
    bloc = ("Voici par ailleurs, en vrac et dans mes propres mots, un rappel de ce que "
            "tu avais répondu à de nombreuses autres questions lors d'une enquête "
            "antérieure, sujet par sujet, sans autre mise en forme : "
            + ", ".join(clauses) + ".")
    return phrase_intro + "\n\n" + bloc


# ---------------------------------------------------------------------------------------
# 4. Les deux gabarits de prompt
# ---------------------------------------------------------------------------------------

SYSTEME_B = (
    "Tu es un simulateur de réponses d'enquête. On te donne un dossier JSON structuré "
    "décrivant une personne à partir de ses réponses à une enquête antérieure. À partir "
    "de ce seul dossier, tu dois prédire comment cette personne répondrait à une "
    "nouvelle liste de questions. Réponds à CHAQUE question par le NUMÉRO de "
    "l'option choisie (un entier), rien d'autre, une ligne par question, au format "
    "exact « IDENTIFIANT: numéro », préfixée par l'identifiant de question fourni. "
    "Aucune explication, aucune phrase, aucune question omise."
)


def blocs_questions(questions):
    """Regroupe les questions consecutives qui partagent le meme jeu d'options, pour
    n'imprimer la legende des options qu'une fois par bloc au lieu de 60 fois -- une
    economie de jetons pure (aucun effet sur le contenu mesure ni sur le format de
    sortie demande a chaque organisation). Les 60 items sont deja contigus par bloc
    (items_communs conserve l'ordre du catalogue), donc aucun tri n'est necessaire.
    Renvoie une liste de (legende, [(numero_global, texte), ...]).
    """
    blocs = []
    courant_opts, courant = None, []
    for k, it in enumerate(questions, start=1):
        opts = tuple(it["options"])
        if opts != courant_opts:
            if courant:
                blocs.append((courant_opts, courant))
            courant_opts, courant = opts, []
        courant.append((k, it["texte"]))
    if courant:
        blocs.append((courant_opts, courant))
    return blocs


def prompt_b(champs, questions):
    lignes_q = []
    for opts, membres in blocs_questions(questions):
        legende = "; ".join(f"{j+1}) {o}" for j, o in enumerate(opts))
        lignes_q.append(f"[Options pour les questions suivantes : {legende}]")
        for k, texte in membres:
            lignes_q.append(f"Q{k:02d}: {texte}")
    utilisateur = (
        "DOSSIER (JSON) :\n" + persona_json(champs) + "\n\n"
        "QUESTIONS :\n" + "\n".join(lignes_q) + "\n\n"
        "Réponds avec « identifiant: numéro » pour chacune, dans l'ordre donné, une "
        "ligne par question."
    )
    return [{"role": "system", "content": SYSTEME_B}, {"role": "user", "content": utilisateur}]


def prompt_c(champs, colonnes_demo, questions):
    bio = persona_narrative(champs, colonnes_demo)
    lignes_q = []
    for opts, membres in blocs_questions(questions):
        legende = " ".join(f"({j+1}) {o}" for j, o in enumerate(opts))
        lignes_q.append(f"(pour les questions qui suivent, les choix possibles sont : "
                         f"{legende})")
        for k, texte in membres:
            lignes_q.append(f"{k}) {texte}")
    # TROUVE AU PILOTE (cf. docstring, "deviation declaree #3") : une reponse en UNE
    # SEULE liste de 60 nombres separes par des virgules, sans aucun repere par
    # question, degenere systematiquement en boucle de repetition ("2,2,2,2,...") a
    # partir d'une vingtaine d'items -- reproduit a l'identique sur trois modeles de
    # trois fournisseurs distincts (qwen, llama-3.3-70b, mistral-small), donc un defaut
    # de FORMAT et non un defaut du modele choisi. Le format retenu ancre chaque reponse
    # sur sa propre ligne par son numero brut (jamais la lettre « Q » ni les deux points
    # du gabarit B) : cela suffit a faire disparaitre la boucle tout en restant une
    # structure de sortie mesurablement differente de celle de B.
    utilisateur = (
        "Mets-toi à la place de la personne suivante et réponds comme elle le ferait.\n\n"
        + bio + "\n\n"
        "Voici maintenant une série de courtes questions, numérotées de 1 à "
        f"{len(questions)}. Réponds à CHAQUE question sur sa PROPRE ligne, au format "
        "exact « numéro) numéro-de-l'option », par exemple « 1) 3 ». Une ligne par "
        "question, dans l'ordre, rien d'autre.\n\n" + "\n".join(lignes_q)
    )
    return [{"role": "user", "content": utilisateur}]


# ---------------------------------------------------------------------------------------
# 5. Parseurs de sortie, un par organisation, motifs disjoints
# ---------------------------------------------------------------------------------------

RE_LIGNE_B = re.compile(r"Q(\d+)\s*[:\-]\s*(\d+)")


def parser_b(texte, n_items):
    codes = np.full(n_items, -1, dtype=np.int32)
    for m in RE_LIGNE_B.finditer(texte or ""):
        k = int(m.group(1)) - 1
        v = int(m.group(2))
        if 0 <= k < n_items:
            codes[k] = v - 1
    return codes


RE_LIGNE_C = re.compile(r"(?<![A-Za-z])(\d+)\s*\)\s*(\d+)")


def parser_c(texte, n_items):
    """Motif disjoint de celui de B : « numero) numero », jamais « Qnumero: numero »."""
    codes = np.full(n_items, -1, dtype=np.int32)
    for m in RE_LIGNE_C.finditer(texte or ""):
        k = int(m.group(1)) - 1
        v = int(m.group(2))
        if 0 <= k < n_items:
            codes[k] = v - 1
    return codes


def borner_codes(codes, n_options_par_item):
    """-1 si le numero rendu est hors bornes des options offertes a cet item."""
    out = codes.copy()
    for j, k in enumerate(n_options_par_item):
        hors = (out[:, j] < 0) | (out[:, j] >= k)
        out[hors, j] = -1
    return out


# ---------------------------------------------------------------------------------------
# 6. Echantillon stratifie sur S_gra
# ---------------------------------------------------------------------------------------

def tirer_echantillon(seg, n, graine):
    rng = np.random.default_rng(graine)
    idx_valides = np.flatnonzero(seg >= 0)
    groupes = {}
    for i in idx_valides:
        groupes.setdefault(int(seg[i]), []).append(int(i))
    total = len(idx_valides)
    quotas_reels = {g: n * len(v) / total for g, v in groupes.items()}
    alloc = {g: int(np.floor(q)) for g, q in quotas_reels.items()}
    reste = n - sum(alloc.values())
    ordre_reste = sorted(groupes, key=lambda g: -(quotas_reels[g] - alloc[g]))
    for g in ordre_reste[:reste]:
        alloc[g] += 1
    choisi = set()
    for g, membres in groupes.items():
        k = min(alloc.get(g, 0), len(membres))
        if k > 0:
            sel = rng.choice(np.array(membres), size=k, replace=False)
            choisi.update(int(x) for x in sel)
    if len(choisi) < n:
        reste_pool = [i for i in idx_valides.tolist() if i not in choisi]
        rng.shuffle(reste_pool)
        for i in reste_pool:
            if len(choisi) >= n:
                break
            choisi.add(i)
    return np.array(sorted(choisi)[:n], dtype=int)


# ---------------------------------------------------------------------------------------
# 7. Trace brute, une ligne par appel
# ---------------------------------------------------------------------------------------

def ecrire_trace(ligne):
    os.makedirs(TRACES, exist_ok=True)
    with open(TRACE_JSONL, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def appels_deja_faits():
    """(sample_idx, org) deja ecrits avec succes dans la trace : reprise idempotente."""
    faits = set()
    if not os.path.exists(TRACE_JSONL):
        return faits
    for ligne in open(TRACE_JSONL, encoding="utf-8"):
        try:
            e = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if e.get("succes"):
            faits.add((e["sample_idx"], e["org"]))
    return faits


def relire_codes_depuis_trace(n_personnes, n_items):
    """Reconstruit X_B, X_C depuis la trace existante, pour reprendre sans rappeler."""
    XB = np.full((n_personnes, n_items), -1, dtype=np.int32)
    XC = np.full((n_personnes, n_items), -1, dtype=np.int32)
    if not os.path.exists(TRACE_JSONL):
        return XB, XC
    for ligne in open(TRACE_JSONL, encoding="utf-8"):
        try:
            e = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if not e.get("succes"):
            continue
        i = e["sample_idx"]
        codes = np.array(e["codes"], dtype=np.int32)
        if e["org"] == "B":
            XB[i] = codes
        else:
            XC[i] = codes
    return XB, XC


# ---------------------------------------------------------------------------------------
# 8. Boucle principale de generation
# ---------------------------------------------------------------------------------------

def generer(paq, echantillon, items, n_appels_max=None):
    idx_items, banque = items
    n_items = len(banque)
    n_options = [len(it["options"]) for it in banque]
    lab = charger_labels(paq)
    colonnes = paq["demo"]["colonnes_contexte"]
    colonnes_demo = set(paq["demo"]["colonnes_demo"])

    cle = cle_api()
    budget = Budget(PLAFOND_DUR_USD, ARRET_INTERNE_USD)
    deja = appels_deja_faits()
    XB, XC = relire_codes_depuis_trace(len(echantillon), n_items)
    # recharge le cumul deja depense depuis la trace, pour que la reprise reste sure
    if os.path.exists(TRACE_JSONL):
        for ligne in open(TRACE_JSONL, encoding="utf-8"):
            try:
                e = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            if e.get("succes") and e.get("cout_usd") is not None:
                budget.cumul += Decimal(str(e["cout_usd"]))
                budget.n_appels += 1
    print(f"cumul deja depense (reprise) : {budget.cumul} USD, {budget.n_appels} appels",
          flush=True)

    n_faits_ce_run = 0
    for local_i, pers_idx in enumerate(echantillon):
        if n_appels_max is not None and n_faits_ce_run >= n_appels_max:
            break
        champs = persona_champs(lab, int(pers_idx), colonnes)
        for org, modele, fournisseur, max_price, batir, parser, max_tok, extra in (
            ("B", MODELE_B, FOURNISSEUR_B, MAX_PRICE_B,
             lambda: prompt_b(champs, banque), lambda t: parser_b(t, n_items),
             MAX_TOKENS_B, None),
            ("C", MODELE_C, FOURNISSEUR_C, MAX_PRICE_C,
             lambda: prompt_c(champs, colonnes_demo, banque), lambda t: parser_c(t, n_items),
             MAX_TOKENS_C, EXTRA_C),
        ):
            if (local_i, org) in deja:
                continue
            if os.path.exists(FICHIER_ARRET_GLOBAL):
                sys.exit("data/traces/STOP present : arret propre, lecture seule.")
            budget.verifier_avant_appel()
            messages = batir()
            rep = appeler_chat(cle, modele, messages, fournisseur, max_price,
                               max_tok, extra=extra)
            horodatage = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
            if "erreur" in rep:
                ecrire_trace({"horodatage": horodatage, "sample_idx": local_i, "org": org,
                              "modele": modele, "succes": False, "erreur": rep})
                print(f"[{local_i}/{len(echantillon)}] {org} : ECHEC {rep.get('erreur')}",
                      flush=True)
                continue
            codes = parser(rep["texte"])
            codes = np.where((codes >= 0) & (codes < np.array(n_options)), codes, -1)
            budget.ajouter(rep.get("cout_annonce"))
            ecrire_trace({
                "horodatage": horodatage, "sample_idx": local_i, "org": org,
                "modele": modele, "succes": True, "raison": rep.get("raison"),
                "jetons_entree": rep.get("jetons_entree"),
                "jetons_sortie": rep.get("jetons_sortie"),
                "cout_usd": rep.get("cout_annonce"),
                "n_reponses_lues": int((codes >= 0).sum()),
                "codes": codes.tolist(),
                "texte_brut": rep["texte"][:4000],
            })
            if org == "B":
                XB[local_i] = codes
            else:
                XC[local_i] = codes
            n_faits_ce_run += 1
            print(f"[{local_i}/{len(echantillon)}] {org} : "
                  f"{int((codes >= 0).sum())}/{n_items} reponses lues, "
                  f"cout cumule {budget.cumul} USD", flush=True)
    return XB, XC, budget


# ---------------------------------------------------------------------------------------
# 9. Mesure, reprise telle quelle de c7_reidentification
# ---------------------------------------------------------------------------------------

def resume_taux(indic, graine):
    return bootstrap_personnes(indic, n_tirages=N_BOOTSTRAP, graine=graine)


def mesurer(paq, echantillon, idx_items, XB, XC):
    couverts = np.flatnonzero((XB >= 0).any(axis=1) & (XC >= 0).any(axis=1))
    n = len(couverts)
    print(f"{n} personnes couvertes des deux cotes (B et C) sur {len(echantillon)}",
          flush=True)
    seg_gra_ech = paq["seg"]["S_gra"][echantillon]

    rng_bc = np.random.default_rng([GRAINE, graine_nom("B<->C")])
    vrai = couverts  # identite : la personne locale i correspond a la colonne i du pool
    rang_f, top1_f, top10_f = rangs_attaque(XB[couverts], XC, couverts, rng_bc)
    rang_seg_f, top1_seg_f, taille_seg_f = rang_dans_segment(
        XB[couverts], couverts, XC, seg_gra_ech, rng_bc)

    rng_cb = np.random.default_rng([GRAINE, graine_nom("C<->B")])
    rang_r, top1_r, top10_r = rangs_attaque(XC[couverts], XB, couverts, rng_cb)
    rang_seg_r, top1_seg_r, taille_seg_r = rang_dans_segment(
        XC[couverts], couverts, XB, seg_gra_ech, rng_cb)

    # unite de reechantillonnage = la personne : chaque personne compte une fois, son
    # indicateur est la moyenne des deux sens de l'attaque (B->C et C->B).
    top1_sym = (top1_f + top1_r) / 2.0
    top10_sym = (top10_f + top10_r) / 2.0
    top1_seg_sym = (top1_seg_f + top1_seg_r) / 2.0
    rang_sym = (rang_f + rang_r) / 2.0
    rang_seg_sym = (rang_seg_f + rang_seg_r) / 2.0

    m_t1, b_t1, h_t1 = resume_taux(top1_sym, [GRAINE, 11])
    m_t10, b_t10, h_t10 = resume_taux(top10_sym, [GRAINE, 12])
    m_t1s, b_t1s, h_t1s = resume_taux(top1_seg_sym, [GRAINE, 13])

    ligne_bc = {
        "configuration": "B<->C (attaque symetrique, moyenne des deux sens)",
        "cible": "B<->C", "n_attaques": n, "n_pool": n,
        "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
        "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
        "rang_median": float(np.median(rang_sym)),
        "top1_hasard": 1.0 / n if n else float("nan"),
        "top10_hasard": min(10, n) / n if n else float("nan"),
        "top1_segment": m_t1s, "top1_segment_bas": b_t1s, "top1_segment_haut": h_t1s,
        "rang_segment_median": float(np.median(rang_seg_sym)),
        "taille_segment_mediane": float(np.median(
            np.concatenate([taille_seg_f[taille_seg_f > 0], taille_seg_r[taille_seg_r > 0]])))
        if (taille_seg_f > 0).any() or (taille_seg_r > 0).any() else float("nan"),
    }

    # --- baseline Demographics Only, recalculee sur le meme pool de 200, gratuite ---
    codes_demo = paq["codes"][DEMO][:, idx_items][echantillon]
    codes_v4 = paq["codes"][REF_V4][:, idx_items][echantillon]
    couverts_demo = np.flatnonzero((codes_demo >= 0).any(axis=1))
    rng_demo = np.random.default_rng([GRAINE, graine_nom(DEMO), 200])
    rang_d, top1_d, top10_d = rangs_attaque(
        codes_demo[couverts_demo], codes_v4, couverts_demo, rng_demo)
    rang_seg_d, top1_seg_d, taille_seg_d = rang_dans_segment(
        codes_demo[couverts_demo], couverts_demo, codes_v4, seg_gra_ech, rng_demo)
    m_t1d, b_t1d, h_t1d = resume_taux(top1_d, [GRAINE, 14])
    m_t10d, b_t10d, h_t10d = resume_taux(top10_d, [GRAINE, 15])
    m_t1sd, b_t1sd, h_t1sd = resume_taux(top1_seg_d, [GRAINE, 16])
    n_d = len(couverts_demo)
    ligne_demo = {
        "configuration": DEMO + " (pool=200, recalcule)", "cible": REF_V4,
        "n_attaques": n_d, "n_pool": len(echantillon),
        "top1": m_t1d, "top1_bas": b_t1d, "top1_haut": h_t1d,
        "top10": m_t10d, "top10_bas": b_t10d, "top10_haut": h_t10d,
        "rang_median": float(np.median(rang_d)),
        "top1_hasard": 1.0 / len(echantillon), "top10_hasard": min(10, len(echantillon)) / len(echantillon),
        "top1_segment": m_t1sd, "top1_segment_bas": b_t1sd, "top1_segment_haut": h_t1sd,
        "rang_segment_median": float(np.median(rang_seg_d)),
        "taille_segment_mediane": float(np.median(taille_seg_d[taille_seg_d > 0]))
        if (taille_seg_d > 0).any() else float("nan"),
    }

    return ligne_bc, ligne_demo, n


# ---------------------------------------------------------------------------------------
# 10. Verdict, critere preenregistre section 4 du preenregistrement
# ---------------------------------------------------------------------------------------

def intervalles_disjoints(bas1, haut1, bas2, haut2):
    return (haut1 < bas2) or (haut2 < bas1)


def verdict(ligne_bc, ligne_demo):
    top1, bas, haut = ligne_bc["top1"], ligne_bc["top1_bas"], ligne_bc["top1_haut"]
    seg_bas, seg_haut = ligne_bc["top1_segment_bas"], ligne_bc["top1_segment_haut"]
    demo_top1 = ligne_demo["top1"]
    non_recouvrement = intervalles_disjoints(bas, haut, seg_bas, seg_haut)
    au_moins_deux_fois_demo = top1 >= 2 * demo_top1
    survit = bool(non_recouvrement and au_moins_deux_fois_demo)
    return {
        "top1_bc": top1, "top1_bc_ic": (bas, haut),
        "top1_segment_ic": (seg_bas, seg_haut),
        "demo_top1_pool200": demo_top1,
        "non_recouvrement_segment": bool(non_recouvrement),
        "au_moins_deux_fois_demo": bool(au_moins_deux_fois_demo),
        "a7_survit": survit,
    }


# ---------------------------------------------------------------------------------------
# 11. main
# ---------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--essai", type=int, default=0,
                    help="ne generer que les N premieres personnes de l'echantillon "
                         "(pilote avant la campagne complete)")
    ap.add_argument("--n-personnes", type=int, default=N_PERSONNES)
    ap.add_argument("--mesurer-seulement", action="store_true",
                    help="ne pas appeler l'API, mesurer uniquement depuis la trace deja "
                         "ecrite")
    args = ap.parse_args()

    print("c7_deux_organisations : temoin deux organisations independantes (B<->C)",
          flush=True)
    paq = T1.charger()
    idx_items, banque = construire_banque_items(paq)
    print(f"{len(banque)} items cibles construits", flush=True)

    echantillon = tirer_echantillon(paq["seg"]["S_gra"], args.n_personnes, GRAINE)
    print(f"echantillon stratifie S_gra : {len(echantillon)} personnes, graine {GRAINE}",
          flush=True)

    n_appels_max = (2 * args.essai) if args.essai else None
    if not args.mesurer_seulement:
        XB, XC, budget = generer(paq, echantillon, (idx_items, banque),
                                  n_appels_max=n_appels_max)
        print(f"\ncout total mesure : {budget.cumul} USD sur {budget.n_appels} appels "
              "reussis", flush=True)
    else:
        XB, XC = relire_codes_depuis_trace(len(echantillon), len(banque))

    if args.essai:
        print("run pilote (--essai) : mesure non ecrite dans les fichiers finaux.",
              flush=True)
        n_ok_b = int((XB >= 0).any(axis=1).sum())
        n_ok_c = int((XC >= 0).any(axis=1).sum())
        print(f"personnes avec au moins une reponse lue : B={n_ok_b}, C={n_ok_c}",
              flush=True)
        return

    ligne_bc, ligne_demo, n = mesurer(paq, echantillon, idx_items, XB, XC)
    df = pd.DataFrame([ligne_bc, ligne_demo])
    chemin_csv = os.path.join(SORTIE, "c7-deux-organisations.csv")
    df.to_csv(chemin_csv, index=False)
    print(f"ecrit {chemin_csv}", flush=True)

    v = verdict(ligne_bc, ligne_demo)
    print("\n--- VERDICT ---")
    print(json.dumps(v, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
