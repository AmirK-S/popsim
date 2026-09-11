"""
r6_oracle_distant : l'oracle des camps de R1, rejoue sur les modeles distants d'OpenRouter.

Statut : script d'experience, pas du code de production. Il joue le plan de
`resultats/r6-preenregistrement-v2.md` (9 septembre 2026, apres 13:05), qui remplace la v1,
avec l'inventaire de prix de `resultats/r6-inventaire-openrouter.md`.

UN SEUL MODE DE LECTURE, celui de R1. La v1 opposait « probabilites par lettre » et « dix
tirages a temperature un » ; la v2 a montre que le probleme etait mal pose :
`MoteurR1.decrire` ne lit aucune probabilite par jeton, il poste `temperature 0.0`,
`top_k 1`, `n_predict 150` et passe le texte au parse strict de `R1.parser`. R6 fait la
meme chose contre une API de conversation : temperature 0, un appel par cellule,
`max_tokens` 150, `R1.parser` importe et jamais recopie, aucune relance, aucune sequence
d'arret a la main (le texte est coupe par le parse).

Les deux formats d'invite, tous deux obtenus par appel des fonctions de R1 et de R5 et
jamais recopies. Si l'un de ces fichiers change, R6 change avec lui, et la ligne de trace
le declare par `version_prompt`.

  F1  `--plan f1`, format `q4`     : tour systeme de `R1.systeme`, tour utilisateur de
      `R1.utilisateur`. 149 items x 3 camps x 2 identites = 894 cellules.
  F2  `--plan f2`, format `q4gab3` : la meme, precedee dans le tour utilisateur du bloc des
      trois exemples de R4 tel que `R5.bloc_exemples` le rend. 79 items orientes de a37
      x 2 camps (gauche, droite) x 2 identites = 316 cellules.

L'habillage ChatML n'est pas applique a la main : sur une API de conversation c'est le
fournisseur qui l'applique a partir des memes deux textes. Que cette voie reproduise la
voie `/completion` de R1 est une mesure, pas une hypothese : elle est faite en local, a
zero euro, par `analyses/r6_voie_chat.py`, et publiee dans `resultats/r6-voie-chat.md`.

Raisonnement. C'est le seul poste qui peut faire exploser la facture (v2, point 7). R1
fixait `Reasoning: low` dans le gabarit harmony de gpt-oss-20b ; l'equivalent API est
`--raisonnement`, inscrit sur chaque ligne de trace, et les jetons de raisonnement factures
sont lus dans `usage.completion_tokens_details.reasoning_tokens`. Le defaut est `off`, la
desactivation EXPLICITE : ne rien envoyer laisse le modele raisonner : l'essai a blanc du
9 septembre a vu `nvidia/nemotron-3-super-120b-a12b:free` ecrire son raisonnement dans le
contenu et saturer les 150 jetons avant d'avoir repondu, dix fois sur dix. Le resume d'essai
porte la ligne « raisonnement desactive effectif », lue sur les jetons factures et non
supposee. Un modele qui refuse la desactivation se joue avec `--max-tokens` releve et
`--fin-seulement`, qui ne donne au parse que les dernieres lignes de la sortie ; les deux
sont inscrits dans la trace, et le cout du raisonnement reste dans le cumul.

Incidents de transport. Seuls les HTTP 429 sont rejoues, au plus trois fois apres
5, 20 et 60 secondes. STOP-R6 et le STOP global utilisateur sont relus avant chaque
tentative. La quatrieme erreur 429 dans une fenetre de vingt appels arrete le run entier.
Un 5xx, timeout ou corps invalide peut masquer une generation facturee : le marqueur
.en-cours bloque alors la reprise jusqu'a reconciliation. Aucun message externe brut
n'est journalise.

Depense. Le cout annonce alimente le budget ; le calcul par jetons est conserve comme
estimation distincte. Le payant passe par une transaction par cellule : verrou global,
GET /key et /credits frais, reservation durable, envoi unique et rapprochement. Sans
inventaire scelle, borne du dernier appel, fournisseur fixe, GO-R6 et empreinte conforme,
aucune generation payante ne part.

Arret R6 : `touch data/traces/STOP-R6` arrete ce run entre deux appels, trace fermee,
resume ecrit, code de sortie 0. Le STOP global `data/traces/STOP` reste aussi respecte en
lecture seule. Aucun de ces fichiers n'est cree ou efface par le script.

Reprise : l'index unique est (version_prompt, format, modele, item, camp, identite). Une
relance ne refait aucun appel deja ecrit. Une trace ancienne sans configuration complete,
tronquee ou marquee .en-cours exige une reconciliation avant reprise.

Relance : il n'y en a pas. Un echec de parse est un rejet, compte, jamais rejoue. C'est la
conduite de R5 section « Relance », etendue a R6 par la v2.

Trace : `data/traces/r6-<cle>.jsonl`, avec les cles de R1 (`version_prompt`, `cle_modele`,
`modele`, `quantification` recevant le fournisseur aval, `gabarit` valant `api-chat`,
`item`, `famille`, `camp`, `identite`, `n_modalites`, `rejet`, `motif_rejet`,
`distribution`), pour que `r1_evaluer.py --suffixe r6` les lise sans une ligne changee.

Entree  : .env, cle OPENROUTER_API_KEY, jamais imprimee, jamais versionnee.
          data/traces/r6-modeles-openrouter.json, le catalogue de prix.
          resultats/a37-orientation-items.csv, pour les 79 items orientes du plan F2.
Sortie  : data/traces/r6-<cle>.jsonl, r6-<cle>-resume.json, r6-run.log,
          r6-<cle>-non-jouees.jsonl, les cellules sans reponse, a rejouer,
          r6-essai-<cle>.json pour un essai.

Usage :
  .venv/bin/python analyses/r6_oracle_distant.py --catalogue     # GET /models seul
  .venv/bin/python analyses/r6_oracle_distant.py --solde         # GET /credits seul
  .venv/bin/python analyses/r6_oracle_distant.py --plan f1 --tirer-liste 40 \\
      --liste data/traces/r6-verif-cellules.txt         # tire la liste, aucun appel
  .venv/bin/python analyses/r6_oracle_distant.py --modele deepseek/deepseek-v4-flash \\
      --plan f1 --essai 10 --plafond 0.05
  .venv/bin/python analyses/r6_oracle_distant.py --modele deepseek/deepseek-v4-flash \\
      --plan f1 --plafond 0.10
"""

import argparse
import collections
import datetime
import json
import math
import fcntl
import glob
import hashlib
from decimal import Decimal
import os
import random
import sys
import time
import urllib.error
import urllib.request
from urllib.parse import urlencode, urlsplit

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# r5_gabarit_exemples remplace en memoire R1.gabarit et R1.chemin_trace. R6 n'appelle ni
# l'un ni l'autre : il ne prend de R5 que le bloc des trois exemples.
import r1_oracle_camps as R1
import r5_gabarit_exemples as R5
from a2_baselines_gss import FAMILLES
from a5_agents_locaux_gss import nomenclature

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data/traces")
SORTIE = os.path.join(RACINE, "resultats")

BASE = "https://openrouter.ai/api/v1"
CATALOGUE = os.path.join(TRACES, "r6-modeles-openrouter.json")
REGISTRE = os.path.join(TRACES, "r6-registre-global.jsonl")
REFERENT = os.path.join(TRACES, "r1-distributions-reelles.csv")
REFERENT_SHA = "ea7cd93e8eb3b34d279171ac9a202a0451554afc3d34c7a142dfce761391c811"
LIMITE_CLE_R6 = Decimal("4.40")
PASSES_LANCEMENT = ("campagne", "essai-1", "essai-2", "plancher")
PASSES_REGISTRE = PASSES_LANCEMENT + ("ancien-pilote",)
PASSES_PILOTE = ("essai-1", "essai-2")
PASSES_PLAFOND_MODELE = ("campagne", "plancher")
PASSES_COUT_MODELE = PASSES_PILOTE + PASSES_PLAFOND_MODELE
PLAFOND_PILOTE_USD = Decimal("0.02")
APPELS_PILOTE_MAX = 20
BORNE_APPEL_PILOTE_USD = Decimal("0.001")
MAX_TOKENS_PILOTE = 150
MAX_PROMPT_TOKENS_PILOTE = 600
MODELE_PILOTE = "deepseek/deepseek-v4-flash"
FOURNISSEUR_PILOTE = "DigitalOcean"
MAX_PRICE_PILOTE = {"prompt": Decimal("0.11"), "completion": Decimal("0.22")}

FICHIER_ARRET_GLOBAL = R1.FICHIER_ARRET              # data/traces/STOP, lecture seule
FICHIER_ARRET_R6 = os.path.join(TRACES, "STOP-R6")   # arrêt propre à R6
# Alias conservé pour les consommateurs historiques qui importent ce nom.
FICHIER_ARRET = FICHIER_ARRET_GLOBAL
FICHIER_GO = os.path.join(TRACES, "GO-R6")           # feu vert de depense, propre a R6
JOURNAL = os.path.join(TRACES, "r6-run.log")

# Le gabarit declare dans la trace : ce n'est plus un gabarit rendu a la main, c'est celui
# que le serveur applique. La v2 impose ce libelle pour que rien ne se confonde avec R1.
GABARIT = "api-chat"

# Les deux formats d'invite, et la version d'invite que chacun declare dans la trace.
FORMATS = {"q4": R1.VERSION_PROMPT, "q4gab3": R5.VERSION_PROMPT}

# Le plan de cellules de la v2. Le format cher n'est joue que la ou il est mesure.
PLANS = {
    "f1": {"format": "q4", "items": "tous", "camps": ["gauche", "centre", "droite"],
           "identites": list(R1.IDENTITES), "cellules": 894},
    "f2": {"format": "q4gab3", "items": "orientes", "camps": ["gauche", "droite"],
           "identites": list(R1.IDENTITES), "cellules": 316},
}

N_PREDICT = R1.N_PREDICT          # 150, comme R1
GRAINE_LISTE = 20260909

# Estimation d'appel de la v2, section « Plan de cellules » : 210 jetons d'entree et 20 de
# sortie sous gabarit seul, 641 et 19 avec les trois exemples. Elle ne sert qu'a refuser un
# appel qui ferait franchir le plafond, jamais a facturer.
JETONS_ESTIMES = {"q4": (210, 20), "q4gab3": (641, 19)}

# Reglages de raisonnement acceptes.
#   off     `{"enabled": false, "exclude": true}`, la desactivation explicite. C'est le
#           defaut depuis l'essai a blanc du 9 septembre : `aucun` n'envoyait rien, et
#           nvidia/nemotron-3-super-120b-a12b:free raisonnait alors dans le contenu et
#           saturait les 150 jetons avant d'avoir repondu, 165 jetons de raisonnement
#           factures sur 10 cellules sur 10 (data/traces/r6-nvidia-...-r6essai.jsonl).
#   none    `{"effort": "none", "exclude": true}`, l'autre orthographe de la desactivation ;
#           certains fournisseurs n'acceptent que celle la.
#   low     l'equivalent API du `Reasoning: low` que R1 fixait dans le gabarit harmony.
#   aucun   n'envoie aucun champ. A n'employer que sur un serveur qui refuse le parametre,
#           comme le llama-server local de la verification de voie : sur une API distante,
#           c'est laisser le modele raisonner par defaut.
RAISONNEMENTS = ("off", "none", "low", "minimal", "aucun")

# Codes HTTP qui disent « incident de transport, rejoue » et non « le modele a repondu ».
# Un 429 ou un 5xx n'est pas un rejet : rien n'a ete lu, il n'y a rien a parser.
# Un 5xx peut suivre une generation facturee : reconciliation avant tout rejeu.
CODES_REJOUABLES = (429,)

# Attentes croissantes entre deux tentatives d'une meme cellule, en secondes.
ATTENTES = (5, 20, 60)
SEUIL_429 = 3
FENETRE_429 = 20
# Amendement 429 : delai entre les deux sondes en lecture seule d'un 429 porteur d'un
# generation_id. La precedence archivee est d'environ neuf minutes.
DELAI_SONDE_429 = 540
TRANCHE_SONDE_429 = 10          # STOP relu toutes les dix secondes pendant l'attente
# Amendement 429 v2 (correctif adverse du 2026-09-11) : delai entre le 429 et la sonde 1.
# Sans lui, 3 a 6 appels anterieurs au 429 dont le reglement est retarde cote OpenRouter
# (retard observe en production : 15 a 40 s) peuvent regler entre les deux sondes, ce qui
# rend `total_usage_stable` faux et fait echouer a tort un 429 reellement non facture.
DELAI_AVANT_SONDE_429 = 120
PREUVE_NON_FACTURE_429 = "429-non-facture"   # prefixe de preuve des annulations automatiques

# Amendement 429 v2 : ancre stable par run (point A). Deux lectures /credits a 60 s
# d'ecart ; si le total_usage n'est pas identique aux deux lectures, jusqu'a cinq
# nouvelles tentatives (six au total), puis ancrage absent (ancienne regle pour ce run).
DELAI_ANCRE_429 = 60
TENTATIVES_ANCRE_429 = 6
# Tolerance du critere v2 (point B) : la derive d'arrondi observee entre deux lectures
# /credits est de l'ordre de 5e-10 USD par cellule (bien en dessous de 1e-6), et le cout
# minimal d'une generation reellement facturee (au moins le prompt) est de l'ordre de
# 1e-5 USD (donc 10 % de ce plancher, 1e-6, ne peut pas confondre une generation facturee
# avec un residu d'arrondi). Quand le registre ne connait encore aucun cout regle pour le
# modele, seul le plafond fixe de 1e-6 USD s'applique.
TOLERANCE_429_PLANCHER = Decimal("0.000001")


def tolerance_429(plus_petit_cout_regle):
    """Tolerance du critere v2 : min(1e-6 USD, 10 % du plus petit cout regle du modele)."""
    if plus_petit_cout_regle is not None and plus_petit_cout_regle > 0:
        return min(TOLERANCE_429_PLANCHER, plus_petit_cout_regle * Decimal("0.1"))
    return TOLERANCE_429_PLANCHER


# --------------------------------------------------------------------------------------
# 1. La cle, le catalogue, le solde
# --------------------------------------------------------------------------------------

def cle_api(chemin=None):
    """Lit OPENROUTER_API_KEY dans .env. La valeur n'est jamais imprimee ni tracee."""
    chemin = chemin or os.path.join(RACINE, ".env")
    if not os.path.exists(chemin):
        sys.exit(f"fichier absent : {chemin}")
    for ligne in open(chemin, encoding="utf-8"):
        if ligne.startswith("OPENROUTER_API_KEY="):
            v = ligne.split("=", 1)[1].strip().strip('"').strip("'")
            if v:
                return v
    sys.exit("OPENROUTER_API_KEY absente de .env")


def entetes(cle):
    """En tetes de toute requete. HTTP-Referer et X-Title identifient le projet."""
    return {
        "Authorization": "Bearer " + cle,
        "Content-Type": "application/json",
        "HTTP-Referer": "popsim",
        "X-Title": "popsim",
    }


def _lire(url, cle, charge=None, timeout=180, avec_entetes=False):
    """Un aller retour HTTP. Le message d'erreur ne contient jamais les en tetes."""
    donnees = json.dumps(charge).encode("utf-8") if charge is not None else None
    req = urllib.request.Request(url, data=donnees, headers=entetes(cle))
    with urllib.request.urlopen(req, timeout=timeout) as r:
        corps = json.loads(r.read().decode("utf-8"))
        return (corps, r.headers) if avec_entetes else corps


def entetes_erreur_non_secrets(entetes_http):
    """Extrait seulement les identifiants de diagnostic autorises d'une erreur HTTP."""
    if entetes_http is None:
        return {}
    recus = {str(k).lower(): str(v).strip()[:512] for k, v in entetes_http.items()}
    familles = {
        "generation_id": ("x-generation-id", "x-openrouter-generation-id"),
        "provider": ("x-provider", "x-openrouter-provider"),
        "request_id": ("x-request-id", "x-openrouter-request-id", "request-id"),
    }
    resultat = {}
    for sortie, noms in familles.items():
        for nom in noms:
            if recus.get(nom):
                resultat[sortie] = recus[nom]
                break
    return resultat


def journaliser_erreur_http_privee(statut, diagnostic, modele):
    """Persiste le diagnostic filtre avant de rendre l'incident au controleur."""
    dossier = os.path.join(TRACES, "reprise")
    os.makedirs(dossier, exist_ok=True)
    chemin = os.path.join(dossier, "r6-erreurs-http-privees.jsonl")
    ligne = {
        "horodatage": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
        "statut": statut,
        "modele": modele,
        "diagnostic_http": diagnostic,
        "correction": "instrumentale",
    }
    fd = os.open(chemin, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.chmod(chemin, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())
    return chemin


def catalogue(cle=None, rafraichir=False):
    """Catalogue des modeles : lecture du cache, ou GET /models si demande.

    GET /api/v1/models est une lecture, elle ne consomme aucun credit. Le cache evite de la
    refaire a chaque cellule et fige les prix du run dans un fichier relisible.
    """
    if rafraichir or not os.path.exists(CATALOGUE):
        d = _lire(BASE + "/models", cle or cle_api())
        os.makedirs(TRACES, exist_ok=True)
        with open(CATALOGUE, "w", encoding="utf-8") as fh:
            json.dump(d, fh)
        return d
    with open(CATALOGUE, encoding="utf-8") as fh:
        return json.load(fh)


def solde(cle=None):
    """GET /credits. Lecture seule, aucun credit consomme."""
    return _lire(BASE + "/credits", cle or cle_api())["data"]


def statut_cle(cle):
    """GET /key frais pour la cle qui sera effectivement utilisee."""
    return _lire(BASE + "/key", cle)


def solde_disponible(snapshot_credits):
    return dollars(snapshot_credits["total_credits"]) - dollars(snapshot_credits["total_usage"])


def prix(modele, cat):
    """(prix entree, prix sortie) en USD par jeton, et si le modele est gratuit."""
    for m in cat["data"]:
        if m["id"] == modele:
            p = m.get("pricing", {})
            entree = nombre_positif(p.get("prompt"))
            sortie = nombre_positif(p.get("completion"))
            return entree, sortie, (entree == 0.0 and sortie == 0.0)
    sys.exit(f"modele absent du catalogue OpenRouter : {modele}")


# --------------------------------------------------------------------------------------
# 2. Les invites, importees et jamais recopiees
# --------------------------------------------------------------------------------------

def invite(item, camp, identite, format_, table):
    """Les deux tours de conversation, et les modalites de l'item.

    Le tour systeme est `R1.systeme` mot pour mot. Le tour utilisateur est
    `R1.utilisateur` mot pour mot, precede pour `q4gab3` du bloc des trois exemples de R4
    tel que `R5.bloc_exemples` le rend, dans le meme ordre et sans separateur ajoute : la
    concatenation est celle de `R5.gabarit`.
    """
    if format_ not in FORMATS:
        sys.exit(f"format inconnu : {format_}. Connus : {', '.join(FORMATS)}")
    sys_txt = R1.systeme(camp, identite)
    usr_txt, options = R1.utilisateur(item, camp, table, rappel=False)
    if format_ == "q4gab3":
        usr_txt = R5.bloc_exemples() + usr_txt
    return [{"role": "system", "content": sys_txt},
            {"role": "user", "content": usr_txt}], options


def items_orientes():
    """Les 79 items orientes de a37, lus tels quels, dans l'ordre du fichier."""
    import pandas as pd
    o = pd.read_csv(os.path.join(SORTIE, "a37-orientation-items.csv"))
    return [str(i) for i, v in zip(o["item"], o["oriente"].astype(bool)) if v]


def plan_cellules(plan, tous_les_items, items_max=0):
    """(items, camps, identites, format) du plan demande."""
    p = PLANS[plan]
    items = tous_les_items if p["items"] == "tous" else [
        i for i in tous_les_items if i in set(items_orientes())]
    if items_max:
        items = items[:items_max]
    return items, list(p["camps"]), list(p["identites"]), p["format"]


def tirer_liste(items, camps, identites, n, graine=GRAINE_LISTE):
    """N cellules tirees d'avance, sans remise, dans un ordre fixe par la graine.

    La v2 exige que la liste des 40 cellules de verification et des 10 cellules d'essai
    soit ecrite AVANT le lancement : c'est ce que fait `--tirer-liste`.
    """
    toutes = [(c, i, it) for c, i, it in R1.cellules(items, camps, identites)]
    rng = random.Random(graine)
    return sorted(rng.sample(toutes, min(n, len(toutes))))


def ecrire_liste(cellules, chemin):
    with open(chemin, "w", encoding="utf-8") as fh:
        for camp, identite, item in cellules:
            fh.write(f"{item}\t{camp}\t{identite}\n")
    return chemin


def lire_liste(chemin):
    cellules = []
    for ligne in open(chemin, encoding="utf-8"):
        ligne = ligne.rstrip("\n")
        if not ligne.strip():
            continue
        item, camp, identite = ligne.split("\t")
        cellules.append((camp, identite, item))
    return cellules


# --------------------------------------------------------------------------------------
# 3. Le client HTTP
# --------------------------------------------------------------------------------------

class ClientChat:
    """Un appel, une reponse, aucune relance. Les erreurs HTTP sont des incidents.

    `base` est pointee sur OpenRouter pour le run, et sur le `llama-server` local pour la
    verification de la voie `chat` : le meme code sert les deux, ce qui est le seul moyen
    de verifier le client lui meme sans reseau.
    """

    def __init__(self, cle, base=BASE, timeout=180, raisonnement="off",
                 usage_inclus=True, fournisseur=None, max_price=None):
        self.cle = cle
        self.base = base
        self.timeout = timeout
        self.raisonnement = raisonnement
        self.usage_inclus = usage_inclus
        self.fournisseur = fournisseur
        self.max_price = max_price

    def charge_raisonnement(self):
        """Le champ `reasoning` envoye a OpenRouter, ou None.

        `off` envoie la desactivation explicite, `none` son autre orthographe. Ne rien
        envoyer laisse le modele raisonner par defaut : c'est ce qui a fait echouer
        l'essai a blanc du 9 septembre, et c'est pour cela que `aucun` n'est plus le
        reglage employe sur une API distante.
        """
        if self.raisonnement in (None, "aucun"):
            return None
        if self.raisonnement == "off":
            return {"enabled": False, "exclude": True}
        if self.raisonnement == "none":
            return {"effort": "none", "exclude": True}
        return {"effort": self.raisonnement, "exclude": True}

    def preparer_charge(self, modele, messages, n_predict=N_PREDICT):
        """Un appel de description, temperature 0, comme `MoteurR1.decrire`.

        Aucune sequence d'arret n'est envoyee : la v2 le decide, le texte est coupe par le
        parse. `top_k 1` de R1 n'existe pas sur les API fermees ; la temperature 0 en tient
        lieu et l'ecart est inscrit au registre.
        """
        charge = {
            "model": modele,
            "messages": messages,
            "temperature": 0.0,
            "max_tokens": n_predict,
        }
        r_raison = self.charge_raisonnement()
        if r_raison is not None:
            charge["reasoning"] = r_raison
        if self.usage_inclus:
            charge["usage"] = {"include": True}
        if self.fournisseur:
            # Fournisseur aval fixe, repli interdit : exigence du registre de la grille
            # (03-grille-d-audit.md, section 3.2), reprise par la v2 point 8.
            charge["provider"] = {"order": [self.fournisseur], "allow_fallbacks": False}
        if self.max_price is not None:
            charge.setdefault("provider", {})["max_price"] = {
                k: float(dollars(self.max_price[k])) for k in ("prompt", "completion")}
        return charge

    def empreinte_requete(self, modele, messages, n_predict=N_PREDICT):
        brut = json.dumps(self.preparer_charge(modele, messages, n_predict), sort_keys=True,
                          ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        return hashlib.sha256(brut).hexdigest()

    def decrire(self, modele, messages, n_predict=N_PREDICT):
        charge = self.preparer_charge(modele, messages, n_predict)
        debut = time.perf_counter()
        try:
            r, entetes_reponse = _lire(self.base + "/chat/completions", self.cle, charge,
                                       self.timeout, avec_entetes=True)
        except urllib.error.HTTPError as e:
            diagnostic = entetes_erreur_non_secrets(e.headers)
            journaliser_erreur_http_privee(e.code, diagnostic, modele)
            return {"erreur": f"HTTP {e.code}", "statut": e.code,
                    "diagnostic_http": diagnostic,
                    "cout_incertain": e.code not in (400, 401, 402, 403, 404, 422, 429),
                    "rejouable": e.code in CODES_REJOUABLES,
                    "duree_ms": (time.perf_counter() - debut) * 1000.0}
        except Exception as e:                       # reseau, delai, corps illisible
            return {"erreur": type(e).__name__, "statut": None,
                    "cout_incertain": True,
                    "rejouable": False,
                    "duree_ms": (time.perf_counter() - debut) * 1000.0}
        duree = (time.perf_counter() - debut) * 1000.0
        if not isinstance(r, dict):
            return {"erreur": "reponse invalide", "cout_incertain": True}
        if r.get("error"):
            # OpenRouter rend parfois un 200 dont le corps porte l'erreur du fournisseur
            # aval, code compris. On la traite comme le code HTTP correspondant.
            code = None
            if isinstance(r["error"], dict):
                try:
                    code = int(r["error"].get("code"))
                except (TypeError, ValueError):
                    code = None
            diagnostic = entetes_erreur_non_secrets(entetes_reponse)
            journaliser_erreur_http_privee(code, diagnostic, modele)
            return {"erreur": "erreur du fournisseur", "cout_incertain": True,
                    "statut": code, "rejouable": False,
                    "diagnostic_http": diagnostic,
                    "duree_ms": duree}
        choix = (r.get("choices") or [{}])[0]
        usage = r.get("usage") or {}
        details = usage.get("completion_tokens_details") or {}
        message = choix.get("message") or {}
        return {
            "texte": message.get("content") or "",
            "raison": choix.get("finish_reason"),
            "modele_renvoye": r.get("model"),
            "fournisseur": r.get("provider"),
            "identifiant": r.get("id"),
            "jetons_entree": usage.get("prompt_tokens"),
            "jetons_sortie": usage.get("completion_tokens"),
            "jetons_raisonnement": details.get("reasoning_tokens"),
            "cout_annonce": usage.get("cost"),
            "duree_ms": duree,
        }


# --------------------------------------------------------------------------------------
# 4. Le budget
# --------------------------------------------------------------------------------------

def nombre_positif(valeur):
    if isinstance(valeur, bool) or valeur is None:
        raise ValueError("montant/compte absent ou invalide")
    n = float(valeur)
    if not math.isfinite(n) or n < 0:
        raise ValueError("montant/compte non fini ou negatif")
    return n


class Budget:
    """Comptabilite par trace ; l'estimation n'est PAS une borne contractuelle."""

    def __init__(self, plafond, prix_entree, prix_sortie, jetons_estimes=(210, 20)):
        self.plafond = nombre_positif(plafond)
        self.prix_entree = nombre_positif(prix_entree)
        self.prix_sortie = nombre_positif(prix_sortie)
        self.jetons_estimes = jetons_estimes
        self.cumul = 0.0
        self.cumul_annonce = 0.0
        self.cout_max_appel = 0.0
        self.atteint = False

    def cout(self, jetons_entree, jetons_sortie):
        return ((jetons_entree or 0) * self.prix_entree
                + (jetons_sortie or 0) * self.prix_sortie)

    def estimation_appel(self):
        """Le pire des deux : l'estimation a priori de la v2, et le pire appel deja vu.

        C'est une estimation empirique, pas une garantie sur la facture suivante.
        Le payant distant reste bloque tant qu'une vraie borne n'est pas disponible.
        """
        return max(self.cout(*self.jetons_estimes), self.cout_max_appel)

    def place_pour_un_appel(self):
        return (self.cumul + self.estimation_appel()) <= self.plafond

    def ajouter(self, jetons_entree, jetons_sortie, cout_annonce=None):
        # Le cout annonce prime, y compris zero. Les jetons sont un repli explicite.
        if cout_annonce is not None:
            c = nombre_positif(cout_annonce)
        else:
            c = self.cout(nombre_positif(jetons_entree), nombre_positif(jetons_sortie))
        self.source = "annonce" if cout_annonce is not None else "estimation_jetons"
        self.cumul += c
        self.cout_max_appel = max(self.cout_max_appel, c)
        if cout_annonce is not None:
            try:
                self.cumul_annonce += float(cout_annonce)
            except (TypeError, ValueError):
                pass
        # `cumul > 0` : un run a cout nul (modele `:free`, serveur local) ne doit pas
        # s'arreter sur un plafond de 0 USD. Un modele payant, lui, est refuse avant son
        # premier appel par `place_pour_un_appel`, qui compte l'estimation.
        if self.cumul >= self.plafond and self.cumul > 0:
            self.atteint = True
        return c



# Decimal conserve les montants exacts ; aucun secret ni corps HTTP dans le registre.
def dollars(v):
    if isinstance(v, bool) or v is None:
        raise ValueError("montant absent")
    try:
        n = Decimal(str(v))
    except Exception:
        raise ValueError("montant invalide") from None
    if not n.is_finite() or n < 0:
        raise ValueError("montant non fini ou negatif")
    return n


def politique_pilote_legacy():
    return {"model": MODELE_PILOTE, "provider": FOURNISSEUR_PILOTE,
            "calls": APPELS_PILOTE_MAX, "total_cap": PLAFOND_PILOTE_USD,
            "call_cap": BORNE_APPEL_PILOTE_USD, "max_tokens": MAX_TOKENS_PILOTE,
            "max_prompt_tokens": MAX_PROMPT_TOKENS_PILOTE,
            "max_price": MAX_PRICE_PILOTE}


def erreurs_configuration_pilote(modele, fournisseur, essai, plafond, max_tokens,
                                 raisonnement, max_prompt_tokens, borne_appel, max_price,
                                 politique=None):
    """Valide une passe pilote contre une politique issue du manifeste scellé."""
    politique = politique or politique_pilote_legacy()
    erreurs = []
    if modele != politique["model"]:
        erreurs.append("modele pilote different du manifeste")
    if fournisseur != politique["provider"]:
        erreurs.append("fournisseur pilote different du manifeste")
    if essai != 10:
        erreurs.append("chaque passe pilote exige --essai 10")
    if dollars(plafond) != dollars(politique["total_cap"]):
        erreurs.append("--plafond pilote different du manifeste")
    if max_tokens != politique["max_tokens"]:
        erreurs.append("--max-tokens pilote different du manifeste")
    if raisonnement != "off":
        erreurs.append("--raisonnement off impose au pilote")
    if max_prompt_tokens != politique["max_prompt_tokens"]:
        erreurs.append("--max-prompt-tokens pilote different du manifeste")
    if dollars(borne_appel) != dollars(politique["call_cap"]):
        erreurs.append("--borne-appel pilote different du manifeste")
    prix_max = {k: dollars(max_price.get(k)) for k in ("prompt", "completion")}
    if any(prix_max[k] != dollars(politique["max_price"][k]) for k in prix_max):
        erreurs.append("provider.max_price pilote different du manifeste")
    return erreurs


def identite_campagne(modele, format_, version, item, camp, identite, passe="campagne"):
    """Le suffixe de fichier n'entre JAMAIS dans l'identite globale.

    Les seules repetitions autorisees sont celles du plan, avec une passe explicite.
    Changer max_tokens, fournisseur ou suffixe ne rachete pas une cellule.
    """
    if passe not in PASSES_REGISTRE:
        raise ValueError("passe hors plan")
    champs = [modele, format_, version, item, camp, identite, passe]
    if not all(isinstance(x, str) and x for x in champs):
        raise ValueError("identite incomplete")
    return json.dumps(champs, ensure_ascii=False, separators=(",", ":"))


class RegistreGlobal:
    """Journal append-only sous verrou exclusif campagne, tous modeles/formats/passes.

    Utiliser un SEUL chemin canonique pour R6. Le verrou couvre lecture, preflight,
    reservation et reconciliation ; aucun envoi n'est implemente dans cette classe.
    Un journal absent n'est jamais initialise silencieusement lors d'une reprise.
    """
    def __init__(self, chemin):
        self.chemin = os.fspath(chemin)

    def __enter__(self):
        self.verrou = open(self.chemin + ".lock", "a")
        try:
            fcntl.flock(self.verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.evenements = lignes_existantes(self.chemin)
            self.operations = {}
            self.import_complet = False
            for i, e in enumerate(self.evenements):
                if e.get("sequence") != i:
                    raise ValueError("sequence registre invalide")
                if i == 0:
                    if e.get("type") != "initialisation" or e.get("campagne") != "R6-v2":
                        raise ValueError("registre hors campagne")
                elif e.get("type") == "import-complet":
                    if self.import_complet:
                        raise ValueError("import deja scelle")
                    self.import_complet = True
                else:
                    self._appliquer(e)
            return self
        except BaseException:
            self.verrou.close()
            raise

    def __exit__(self, *args):
        self.verrou.close()

    def _appliquer(self, e):
        ident = e["identite"]
        # Validation du schema d'identite meme lors de la relecture.
        if identite_campagne(*json.loads(ident)) != ident:
            raise ValueError("identite registre invalide")
        montant = dollars(e["usd"])
        if e["type"] in ("reservation", "historique", "historique-incertain"):
            if ident in self.operations:
                raise ValueError("cellule deja engagee, suffixe sans effet")
            self.operations[ident] = dict(e, etat=e["type"], usd=montant)
        elif e["type"] == "reconciliation":
            if self.operations.get(ident, {}).get("etat") != "reservation":
                raise ValueError("reservation absente ou deja reconciliee")
            if not e.get("preuve"):
                raise ValueError("preuve de facturation requise")
            self.operations[ident] = dict(e, etat="reglee", usd=montant)
        elif e["type"] == "annulation":
            if self.operations.get(ident, {}).get("etat") != "reservation":
                raise ValueError("reservation absente ou deja terminee")
            if not e.get("preuve"):
                raise ValueError("preuve de non facturation requise")
            del self.operations[ident]
        else:
            raise ValueError("evenement inconnu")

    def _ecrire(self, e):
        if self.verrou.closed:
            raise ValueError("verrou requis")
        e = dict(e, sequence=len(self.evenements))
        with open(self.chemin, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(e, ensure_ascii=False, allow_nan=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
        self.evenements.append(e)

    def initialiser(self, inventaire, historique):
        """Import EXPLICITE apres audit : empreintes et identites/couts attribues.

        L'exhaustivite semantique de cet import doit encore etre certifiee par le parent.
        Cette primitive ne declare pas les anciennes traces reconciliees d'elle-meme.
        """
        if self.evenements:
            raise ValueError("registre deja initialise")
        for chemin, empreinte in inventaire.items():
            if hashlib.sha256(open(chemin, "rb").read()).hexdigest() != empreinte:
                raise ValueError("empreinte historique differente")
        # Valider tout l'import avant sa premiere ecriture.
        for ident, montant in historique.items():
            self._appliquer({"type": "historique", "identite": ident, "usd": str(montant)})
        self._ecrire({"type": "initialisation", "campagne": "R6-v2",
                      "inventaire": inventaire})
        for ident, montant in historique.items():
            self._ecrire({"type": "historique", "identite": ident, "usd": str(montant)})
        self._ecrire({"type": "import-complet"})
        self.import_complet = True

    def initialiser_evenements(self, inventaire, evenements):
        """Initialise depuis un inventaire explicite de traces deja achetees/tentees."""
        if self.evenements:
            raise ValueError("registre deja initialise")
        for chemin, empreinte in inventaire.items():
            if hashlib.sha256(open(chemin, "rb").read()).hexdigest() != empreinte:
                raise ValueError("empreinte historique differente")
        for e in evenements:
            self._appliquer(e)
        self._ecrire({"type": "initialisation", "campagne": "R6-v2",
                      "inventaire": inventaire})
        for e in evenements:
            self._ecrire(e)
        self._ecrire({"type": "import-complet"})
        self.import_complet = True

    def verifier_integrite(self, inventaire):
        if not self.import_complet or self.evenements[0]["inventaire"] != inventaire:
            raise ValueError("inventaire ancien absent, incomplet ou change")
        for chemin, empreinte in inventaire.items():
            if hashlib.sha256(open(chemin, "rb").read()).hexdigest() != empreinte:
                raise ValueError("trace historique alteree")

    def total(self):
        return sum((e["usd"] for e in self.operations.values()), Decimal("0"))

    def operations_pilote(self, modele=None):
        return [e for ident, e in self.operations.items()
                if json.loads(ident)[-1] in PASSES_PILOTE
                and (modele is None or json.loads(ident)[0] == modele)]

    def total_pilote(self, modele=None):
        return sum((e["usd"] for e in self.operations_pilote(modele)), Decimal("0"))

    def plafond_pilote_enregistre(self, modele):
        plafonds = set()
        for e in self.evenements:
            if e.get("type") != "reservation":
                continue
            champs = json.loads(e["identite"])
            if champs[0] != modele or champs[-1] not in PASSES_PILOTE:
                continue
            brut = e.get("plafond_pilote_usd")
            if brut is None and modele == MODELE_PILOTE:
                brut = PLAFOND_PILOTE_USD  # vingt appels historiques k5qfh
            plafond = dollars(brut)
            if plafond <= 0 or plafond > LIMITE_CLE_R6:
                raise ValueError("plafond pilote invalide dans le registre")
            plafonds.add(plafond)
        if len(plafonds) > 1:
            raise ValueError("plafonds pilote contradictoires pour le modele")
        return next(iter(plafonds), None)

    def operations_modele(self, modele):
        """Pilote, F1/F2 et plancher soumis au plafond partagé du modèle."""
        if not isinstance(modele, str) or not modele:
            raise ValueError("modele absent pour plafond cumulatif")
        return [e for ident, e in self.operations.items()
                if json.loads(ident)[0] == modele
                and json.loads(ident)[-1] in PASSES_COUT_MODELE]

    def total_modele(self, modele):
        return sum((e["usd"] for e in self.operations_modele(modele)), Decimal("0"))

    def total_reglee(self):
        """Amendement 429 v2 : somme de tous les couts reellement factures au registre.

        Toutes passes et tous modeles confondus : c'est cette somme, pas `total()` (qui
        retient aussi les reservations ouvertes a leur borne pessimiste), qui suit
        `total_usage` d'OpenRouter. Seule sa VARIATION entre l'ancrage et l'instant present
        sert au critere ; inclure l'import historique (constant pendant tout run vivant) ne
        change donc pas le delta calcule.
        """
        return sum((e["usd"] for e in self.operations.values()
                    if e["etat"] in ("reglee", "historique", "historique-incertain")),
                   Decimal("0"))

    def plus_petit_cout_regle(self, modele):
        """Amendement 429 v2 : plus petit cout reellement facture de CE modele, ou None."""
        couts = [e["usd"] for ident, e in self.operations.items()
                if e["etat"] == "reglee" and e["usd"] > 0 and json.loads(ident)[0] == modele]
        return min(couts) if couts else None

    def plafond_modele_enregistre(self, modele):
        """Retrouve la borne scellée dans les réservations F1/F2/plancher."""
        plafonds = set()
        for e in self.evenements:
            if e.get("type") != "reservation":
                continue
            champs = json.loads(e["identite"])
            if champs[0] != modele or champs[-1] not in PASSES_COUT_MODELE:
                continue
            # Les vingt réservations DeepSeek précèdent ce champ. Leur coût est inclus
            # par total_modele; le premier événement post-correction scelle le plafond.
            if e.get("plafond_modele_usd") is None and champs[-1] in PASSES_PILOTE:
                continue
            try:
                plafond = dollars(e.get("plafond_modele_usd"))
            except ValueError:
                raise ValueError("plafond modele absent ou invalide dans le registre") from None
            if plafond <= 0 or plafond > LIMITE_CLE_R6:
                raise ValueError("plafond modele hors limite globale")
            plafonds.add(plafond)
        if len(plafonds) > 1:
            raise ValueError("plafonds cumulatifs contradictoires pour le modele")
        return next(iter(plafonds), None)

    def composantes_budget(self, solde):
        """Bornes indépendantes avant la limite éventuelle de la clé distante."""
        reserves = sum((e["usd"] for e in self.operations.values()
                        if e["etat"] == "reservation"), Decimal("0"))
        global_restant = max(Decimal("0"), LIMITE_CLE_R6 - self.total())
        compte_restant = max(Decimal("0"), dollars(solde) - Decimal("1.50") - reserves)
        return {"global_restant": global_restant, "compte_apres_reserve": compte_restant,
                "reservations_ambigues": reserves}

    def restant(self, solde):
        # Les reservations ambigues sont retenues aussi cote solde, par prudence.
        c = self.composantes_budget(solde)
        return min(c["global_restant"], c["compte_apres_reserve"])

    def reserver(self, identite, borne_usd, solde, plafond_modele_usd=None, **provenance):
        if not self.import_complet:
            raise ValueError("import historique requis")
        if any(e["etat"] == "reservation" for e in self.operations.values()):
            raise ValueError("appel en cours ou ambigu : reconciliation avant envoi suivant")
        borne = dollars(borne_usd)
        champs_identite = json.loads(identite)
        modele, passe = champs_identite[0], champs_identite[-1]
        if passe in PASSES_PILOTE:
            plafond_pilote_brut = provenance.pop("plafond_pilote_usd", None)
            plafond_pilote = dollars(PLAFOND_PILOTE_USD if plafond_pilote_brut is None
                                     else plafond_pilote_brut)
            appels_pilote = provenance.pop("appels_pilote_max", APPELS_PILOTE_MAX)
            borne_pilote = dollars(provenance.pop("borne_pilote_max_usd",
                                                  BORNE_APPEL_PILOTE_USD))
            if type(appels_pilote) is not int or appels_pilote != 20:
                raise ValueError("pilote exige exactement vingt appels")
            if borne > borne_pilote:
                raise ValueError("borne unitaire pilote superieure au manifeste")
            plafond_existant = self.plafond_pilote_enregistre(modele)
            if plafond_existant is not None and plafond_existant != plafond_pilote:
                raise ValueError("plafond pilote different du registre")
            if len(self.operations_pilote(modele)) >= appels_pilote:
                raise ValueError("pilote modele limite a vingt appels")
            if self.total_pilote(modele) + borne > plafond_pilote:
                raise ValueError("plafond cumulatif pilote modele depasse")
            provenance["plafond_pilote_usd"] = str(plafond_pilote)
        if passe in PASSES_PLAFOND_MODELE or plafond_modele_usd is not None:
            plafond_modele = dollars(plafond_modele_usd)
            if plafond_modele <= 0 or plafond_modele > LIMITE_CLE_R6:
                raise ValueError("plafond cumulatif modele hors limite globale")
            plafond_existant = self.plafond_modele_enregistre(modele)
            if plafond_existant is not None and plafond_existant != plafond_modele:
                raise ValueError("plafond cumulatif modele different du registre")
            if self.total_modele(modele) + borne > plafond_modele:
                raise ValueError("plafond cumulatif modele depasse")
            provenance["plafond_modele_usd"] = str(plafond_modele)
        if borne <= 0 or borne > self.restant(solde):
            raise ValueError("reservation hors budget")
        if not provenance.get("empreinte_requete") or not provenance.get("fournisseur_impose"):
            raise ValueError("empreinte et fournisseur requis avant reservation")
        e = {"type": "reservation", "identite": identite, "usd": str(borne), **provenance}
        self._appliquer(e)
        self._ecrire(e)  # Persiste AVANT tout futur envoi, jamais libere au timeout.

    def reconcilier(self, identite, cout_usd, preuve):
        e = {"type": "reconciliation", "identite": identite,
             "usd": str(dollars(cout_usd)), "preuve": preuve}
        self._appliquer(e)
        self._ecrire(e)  # Un depassement reel est conserve, jamais tronque au plafond.

    def annuler(self, identite, preuve):
        e = {"type": "annulation", "identite": identite, "usd": "0", "preuve": preuve}
        self._appliquer(e)
        self._ecrire(e)


class ErreurPreflight(ValueError):
    """Refus avec branche stable et diagnostic financier dépourvu de secret."""
    def __init__(self, branche, message, diagnostic):
        super().__init__(message)
        self.branche = branche
        self.diagnostic = dict(diagnostic, branche=branche, autorise_generation=False)


def journaliser_preflight_prive(diagnostic, resultat, chemin=None):
    """Conserve les seules composantes non secrètes du contrôle sous verrou."""
    chemin = chemin or os.path.join(TRACES, "reprise", "r6-preflights-prives.jsonl")
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    ligne = {"horodatage": datetime.datetime.now().astimezone().isoformat(timespec="seconds"),
             "resultat": resultat, **diagnostic}
    fd = os.open(chemin, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    os.chmod(chemin, 0o600)
    with os.fdopen(fd, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(ligne, ensure_ascii=False, allow_nan=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def preflight_cle(snapshot_cle, solde, registre, inventaire, max_tokens, max_price,
                  borne_appel=None, max_prompt_tokens=None, passe=None, modele=None,
                  plafond_modele=None, politique_pilote=None):
    """Valide les gardes financieres a partir de snapshots pris sous le verrou."""
    if not isinstance(snapshot_cle, dict) or not isinstance(snapshot_cle.get("data"), dict):
        raise ErreurPreflight("snapshot_cle_invalide", "snapshot GET /key invalide", {})
    d = snapshot_cle["data"]
    try:
        solde_valide = dollars(solde)
    except ValueError:
        raise ErreurPreflight("solde_invalide", "solde disponible invalide", {
            "snapshot_cle_non_secret": {
                "limit": d.get("limit"), "limit_remaining": d.get("limit_remaining"),
                "limit_reset_is_null": d.get("limit_reset") is None,
            }}) from None
    diagnostic = {
        "snapshot_cle_non_secret": {
            "limit": d.get("limit"), "limit_remaining": d.get("limit_remaining"),
            "limit_reset_is_null": d.get("limit_reset") is None,
            "disabled": d.get("disabled") is True,
            "is_management_key": d.get("is_management_key") is True,
        },
        "solde_disponible_usd": str(solde_valide),
        "reserve_compte_usd": "1.50",
        "plafond_global_usd": str(LIMITE_CLE_R6),
        "passe": passe,
    }

    def refuser(branche, message):
        raise ErreurPreflight(branche, message, diagnostic)

    try:
        registre.verifier_integrite(inventaire)
    except ValueError as exc:
        refuser("integrite_registre", str(exc))
    if not isinstance(max_price, dict):
        refuser("prix_max_absent", "provider.max_price absent")
    if d.get("limit") is None:
        refuser("limite_cle_absente", "limit absente")
    if d.get("limit_remaining") is None:
        refuser("reste_cle_absent", "limit_remaining absent")
    try:
        limite = dollars(d.get("limit"))
    except ValueError:
        refuser("limite_cle_non_finie", "limit invalide ou non finie")
    try:
        restant_cle = dollars(d.get("limit_remaining"))
    except ValueError:
        refuser("reste_cle_non_fini", "limit_remaining invalide ou non fini")
    if "limit_reset" not in d:
        refuser("reset_cle_absent", "champ limit_reset absent")
    if d["limit_reset"] is not None:
        refuser("reset_cle_non_nul", "cle a limite renouvelable")
    if d.get("disabled") is True:
        refuser("cle_desactivee", "cle desactivee")
    if d.get("is_management_key") is True:
        refuser("cle_de_gestion", "cle de gestion interdite")
    if limite <= 0 or limite > LIMITE_CLE_R6:
        refuser("limite_cle_hors_plafond", "limit doit verifier 0 < limit <= 4.40")
    if restant_cle <= 0:
        refuser("reste_cle_epuise", "limit_remaining nul ou negatif")
    if restant_cle > limite:
        refuser("reste_cle_superieur_limite", "limit_remaining superieur a limit")
    composantes = registre.composantes_budget(solde)
    effectif = min(composantes["global_restant"],
                   composantes["compte_apres_reserve"], restant_cle)
    diagnostic["budget"] = {
        "global_restant_usd": str(composantes["global_restant"]),
        "compte_apres_reserve_usd": str(composantes["compte_apres_reserve"]),
        "key_limit_usd": str(limite),
        "key_limit_remaining_usd": str(restant_cle),
        "plafond_effectif_usd": str(effectif),
        "reservations_ambigues_usd": str(composantes["reservations_ambigues"]),
    }
    if type(max_tokens) is not int or max_tokens <= 0:
        refuser("max_tokens_invalide", "max_tokens entier positif requis")
    try:
        prix_plafonds = {k: dollars(max_price.get(k)) for k in ("prompt", "completion")}
    except ValueError:
        refuser("prix_max_invalide", "provider.max_price incomplet ou invalide")
    if any(e["etat"] == "reservation" for e in registre.operations.values()):
        refuser("reservation_non_reconciliee", "reservation non reconciliee")
    autorise = borne_appel is not None and max_prompt_tokens is not None
    if autorise:
        if type(max_prompt_tokens) is not int or max_prompt_tokens <= 0:
            refuser("max_prompt_tokens_invalide", "max_prompt_tokens entier positif requis")
        try:
            borne = dollars(borne_appel)
        except ValueError:
            refuser("borne_appel_invalide", "borne du dernier appel invalide")
        derivee = (dollars(max_prompt_tokens) * prix_plafonds["prompt"]
                   + dollars(max_tokens) * prix_plafonds["completion"]) / Decimal("1000000")
        diagnostic["borne_appel_usd"] = str(borne)
        diagnostic["borne_derivee_usd"] = str(derivee)
        if derivee <= 0:
            refuser("borne_derivee_non_positive", "borne derivee nulle ou negative")
        if borne <= 0 or borne < derivee:
            refuser("borne_appel_insuffisante", "borne du dernier appel insuffisante")
        if borne > effectif:
            refuser("plafond_effectif_insuffisant", "reservation pire appel hors plafond effectif")
        if passe in PASSES_PLAFOND_MODELE or plafond_modele is not None:
            if not isinstance(modele, str) or not modele:
                refuser("modele_plafond_absent", "modele requis pour plafond cumulatif")
            try:
                plafond_modele_valide = dollars(plafond_modele)
            except ValueError:
                refuser("plafond_modele_invalide", "plafond cumulatif modele invalide")
            if plafond_modele_valide <= 0 or plafond_modele_valide > LIMITE_CLE_R6:
                refuser("plafond_modele_invalide", "plafond cumulatif modele hors limite")
            try:
                plafond_existant = registre.plafond_modele_enregistre(modele)
            except ValueError as exc:
                refuser("plafond_modele_registre_invalide", str(exc))
            if plafond_existant is not None and plafond_existant != plafond_modele_valide:
                refuser("plafond_modele_change", "plafond cumulatif modele different du registre")
            total_modele = registre.total_modele(modele)
            diagnostic["budget_modele"] = {
                "modele": modele,
                "total_engage_usd": str(total_modele),
                "plafond_usd": str(plafond_modele_valide),
                "restant_avant_reservation_usd": str(max(Decimal("0"),
                                                         plafond_modele_valide - total_modele)),
            }
            if total_modele + borne > plafond_modele_valide:
                refuser("plafond_modele_insuffisant",
                        "reservation pire appel hors plafond cumulatif modele")
        if passe in PASSES_PILOTE:
            politique = politique_pilote or politique_pilote_legacy()
            if modele != politique["model"]:
                refuser("modele_pilote", "modele pilote different du manifeste")
            if max_tokens != politique["max_tokens"]:
                refuser("max_tokens_pilote", "max_tokens pilote different du manifeste")
            if max_prompt_tokens != politique["max_prompt_tokens"]:
                refuser("prompt_pilote", "max_prompt_tokens pilote different du manifeste")
            borne_max = dollars(politique["call_cap"])
            plafond_pilote = dollars(politique["total_cap"])
            if borne > borne_max:
                refuser("borne_unitaire_pilote", "borne unitaire pilote hors manifeste")
            if any(prix_plafonds[k] != dollars(politique["max_price"][k])
                   for k in prix_plafonds):
                refuser("prix_pilote", "provider.max_price pilote different du manifeste")
            if len(registre.operations_pilote(modele)) >= politique["calls"]:
                refuser("appels_pilote_epuises", "pilote modele limite a vingt appels")
            if registre.total_pilote(modele) + borne > plafond_pilote:
                refuser("budget_pilote_epuise", "plafond cumulatif pilote modele depasse")
    return {**diagnostic, "branche": "autorise" if autorise else "lecture_seule",
            "conditions_cle_valides": True, "autorise_generation": autorise,
            "budget_restant_usd": str(effectif),
            "limit_remaining_usd": str(restant_cle),
            "max_tokens": max_tokens,
            "provider": {"max_price": {k: str(v) for k, v in prix_plafonds.items()}},
            "borne_appel_usd": str(dollars(borne_appel)) if autorise else None,
            "pilote_cout_cumule_usd": str(registre.total_pilote(modele)),
            "pilote_appels_engages": len(registre.operations_pilote(modele))}


def verifier_referent(chemin=None, attendu=None):
    chemin = chemin or REFERENT
    attendu = attendu or REFERENT_SHA
    if hashlib.sha256(open(chemin, "rb").read()).hexdigest() != attendu:
        raise ValueError("empreinte du referent humain differente")


class TransactionPayante:
    """Une cellule : verrou global, lectures fraiches, reservation, envoi, facture."""
    def __init__(self, registre, inventaire, passe, borne_appel, max_prompt_tokens,
                 snapshot_cle=statut_cle, snapshot_solde=solde, plafond_modele=None,
                 politique_pilote=None, fichier_go=None, rapprochement_429=False):
        self.registre = registre
        # Amendement 429 : False (defaut) garde le comportement historique exact.
        self.rapprochement_429 = rapprochement_429 is True
        self.inventaire = inventaire
        self.passe = passe
        self.borne_appel = borne_appel
        self.max_prompt_tokens = max_prompt_tokens
        self.plafond_modele = plafond_modele
        self.politique_pilote = politique_pilote
        self.fichier_go = fichier_go or FICHIER_GO
        self.snapshot_cle = snapshot_cle
        self.snapshot_solde = snapshot_solde

    def appeler(self, client, modele, format_, version, item, camp, identite,
                messages, n_predict, marqueur):
        if self.passe in PASSES_PILOTE:
            politique = self.politique_pilote or politique_pilote_legacy()
            if (modele != politique["model"] or client.fournisseur != politique["provider"]
                    or client.raisonnement != "off"):
                raise ValueError("modele, fournisseur ou raisonnement pilote non conforme")
        ident = identite_campagne(modele, format_, version, item, camp, identite, self.passe)
        empreinte = client.empreinte_requete(modele, messages, n_predict)
        with RegistreGlobal(self.registre) as reg:
            if arret_demande() or not feu_vert(self.fichier_go):
                raise ValueError("STOP present ou GO-R6 absent sous verrou global")
            verifier_referent()
            snap_cle = self.snapshot_cle(client.cle)
            credits = self.snapshot_solde(client.cle)
            disponible = solde_disponible(credits)
            try:
                diag = preflight_cle(snap_cle, disponible, reg, self.inventaire,
                                      n_predict, client.max_price, self.borne_appel,
                                      self.max_prompt_tokens, self.passe, modele,
                                      self.plafond_modele, self.politique_pilote)
            except ErreurPreflight as exc:
                journaliser_preflight_prive(exc.diagnostic, "refuse")
                raise
            journaliser_preflight_prive(diag, "autorise")
            if not diag["autorise_generation"]:
                raise ValueError("preflight incomplet")
            provenance_pilote = {}
            if self.passe in PASSES_PILOTE:
                politique = self.politique_pilote or politique_pilote_legacy()
                provenance_pilote = {
                    "plafond_pilote_usd": str(politique["total_cap"]),
                    "appels_pilote_max": politique["calls"],
                    "borne_pilote_max_usd": str(politique["call_cap"]),
                }
            reg.reserver(ident, self.borne_appel, disponible,
                         plafond_modele_usd=self.plafond_modele,
                         empreinte_requete=empreinte,
                         fournisseur_impose=client.fournisseur,
                         max_tokens=n_predict,
                         provider_max_price={k: str(dollars(v))
                                             for k, v in client.max_price.items()},
                         **provenance_pilote)
            with open(marqueur, "x", encoding="utf-8") as fh:
                json.dump({"identite_globale": ident, "empreinte_requete": empreinte}, fh)
                fh.flush()
                os.fsync(fh.fileno())
            r = client.decrire(modele, messages, n_predict)
            r["empreinte_requete"] = empreinte
            r["fournisseur_impose"] = client.fournisseur
            if r.get("erreur"):
                if (r.get("statut") == 429
                        and (r.get("diagnostic_http") or {}).get("generation_id")):
                    r["cout_incertain"] = True
                    r["rejouable"] = False
                    if self.rapprochement_429:
                        r["rapprochement_429"] = {
                            "identite": ident,
                            "generation_id": r["diagnostic_http"]["generation_id"],
                            "disponible_avant": str(disponible),
                            "total_usage_avant": str(credits.get("total_usage")),
                        }
                if not r.get("cout_incertain"):
                    reg.annuler(ident, f"HTTP-{r.get('statut')}-sans-generation")
                return r
            if r.get("cout_annonce") is None:
                r.update(erreur="cout annonce absent", cout_incertain=True, rejouable=False)
                return r
            preuve = r.get("identifiant")
            if not preuve:
                r.update(erreur="identifiant de facture absent", cout_incertain=True,
                         rejouable=False)
                return r
            reg.reconcilier(ident, r["cout_annonce"], preuve)
            if r.get("fournisseur") != client.fournisseur:
                raise ValueError("fournisseur renvoye different du fournisseur impose")
            return r

    def _sonder_429(self, client, generation_id):
        """Une sonde en lecture seule (GET, jamais de POST) d'un 429 ambigu.

        Ne conserve que des statuts HTTP et le solde : ni cle, ni contenu de generation.
        """
        sonde = {"horodatage": datetime.datetime.now().astimezone().isoformat(
            timespec="seconds")}
        for nom, point in (("generation", "/generation"),
                           ("generation_content", "/generation/content")):
            url = client.base + point + "?" + urlencode({"id": generation_id})
            try:
                _lire(url, client.cle, timeout=client.timeout)
                sonde[nom] = {"statut_http": 200}
            except urllib.error.HTTPError as e:
                sonde[nom] = {"statut_http": e.code}
                e.close()
            except Exception as e:
                sonde[nom] = {"statut_http": None, "exception": type(e).__name__}
        try:
            credits = self.snapshot_solde(client.cle)
            sonde["credits"] = {"disponible": str(solde_disponible(credits)),
                                "total_usage": str(credits.get("total_usage"))}
        except Exception as e:
            sonde["credits"] = {"exception": type(e).__name__}
        return sonde

    def etablir_ancre_429(self, client, dormir):
        """Amendement 429 v2, point A : ancre stable par run, avant le premier POST.

        Deux lectures /credits a `DELAI_ANCRE_429` secondes d'ecart (STOP relu par
        tranches de `TRANCHE_SONDE_429` s). Si le total_usage est identique aux deux
        lectures d'une meme tentative, l'ancre est etablie et persistee ; sinon, jusqu'a
        `TENTATIVES_ANCRE_429 - 1` nouvelles tentatives. Rend None si l'ancrage reste
        instable, si STOP est demande pendant l'attente, ou sur exception : l'amendement
        429 est alors inactif pour ce run (ancienne regle, aucun rapprochement automatique,
        aucune sonde).
        """
        for _tentative in range(TENTATIVES_ANCRE_429):
            if arret_demande():
                return None
            try:
                c1 = self.snapshot_solde(client.cle)
            except Exception:
                continue
            horodatage = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
            restant = DELAI_ANCRE_429
            arrete = False
            while restant > 0:
                if arret_demande():
                    arrete = True
                    break
                tranche = min(TRANCHE_SONDE_429, restant)
                dormir(tranche)
                restant -= tranche
            if arrete:
                return None
            try:
                c2 = self.snapshot_solde(client.cle)
            except Exception:
                continue
            if str(c1.get("total_usage")) != str(c2.get("total_usage")):
                continue
            try:
                with RegistreGlobal(self.registre) as reg:
                    somme_reglee = str(reg.total_reglee())
            except Exception:
                continue
            ancre = {"horodatage": horodatage, "total_usage_ancre": str(c2.get("total_usage")),
                     "disponible_ancre": str(solde_disponible(c2)),
                     "somme_reglee_registre_ancre": somme_reglee}
            try:
                ancre["fichier_ancre"] = self._persister_ancre_429(ancre)
            except OSError:
                pass
            return ancre
        return None

    def _persister_ancre_429(self, ancre):
        horodatage = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
        dossier = os.path.join(TRACES, "reprise")
        os.makedirs(dossier, exist_ok=True)
        chemin = os.path.join(dossier, f"r6-ancre-429-{horodatage}.json")
        fd = os.open(chemin, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            os.chmod(chemin, 0o600)
            json.dump(dict(ancre, version="R6-ancre-429-1"), fh, ensure_ascii=False,
                      indent=2, allow_nan=False)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        return chemin

    def rapprocher_429(self, client, r, dormir):
        """Amendement 429 v2 : deux sondes en lecture seule, annulation si non facture prouve.

        Sequence reelle : DELAI_AVANT_SONDE_429 (120 s) entre le 429 et la sonde 1, puis
        DELAI_SONDE_429 (540 s) entre la sonde 1 et la sonde 2. Le premier delai laisse le
        temps aux appels anterieurs au 429 dont le reglement est retarde cote OpenRouter de
        tomber avant la sonde 1 plutot qu'entre les deux sondes (correctif adverse du
        2026-09-11).

        Critere (point B) : 404 sur /generation et /generation/content aux deux sondes ;
        total_usage identique entre les deux sondes (stabilite) ; et total_usage a la
        seconde sonde egal, a la tolerance pres, a l'ancre du run corrigee de la variation
        des couts REGLES au registre depuis l'ancrage. La reservation ambigue elle-meme
        n'est jamais reglee : elle est exclue de cette somme. Exige une ancre stable
        (`self.ancre_429`, etablie par `etablir_ancre_429` avant le premier POST du run) ;
        sans ancre, ancienne regle, aucune sonde.

        Point C : des que les deux sondes sont prises, la preuve est TOUJOURS ecrite
        (O_EXCL, 0600), que l'issue soit `non_facture` ou `indetermine`. Si STOP-R6 (ou
        STOP global) apparait pendant l'attente AVANT la sonde 1, aucune sonde n'est prise
        mais une preuve `indetermine` est tout de meme persistee (motif du refus garde).
        Si STOP apparait pendant l'attente ENTRE les deux sondes, aucune preuve n'est
        ecrite (les deux sondes n'ont pas ete prises).
        """
        if not self.rapprochement_429:
            return {"statut": "indetermine", "motif": "rapprochement_429 inactif"}
        avant = r.get("rapprochement_429") if isinstance(r, dict) else None
        champs = ("identite", "generation_id", "disponible_avant", "total_usage_avant")
        if not isinstance(avant, dict) or not all(
                isinstance(avant.get(k), str) and avant.get(k) for k in champs):
            return {"statut": "indetermine", "motif": "contexte avant appel absent"}
        ident, gid = avant["identite"], avant["generation_id"]
        resultat = {"statut": "indetermine", "identite": ident, "generation_id": gid,
                    "avant": {"disponible": avant["disponible_avant"],
                              "total_usage": avant["total_usage_avant"]}}
        # Un seul rapprochement automatique par identite, meme apres STOP ou crash.
        refus = self.motif_refus_rapprochement_429(ident)
        if refus:
            resultat["motif"] = refus
            return resultat
        ancre = getattr(self, "ancre_429", None)
        if not isinstance(ancre, dict) or not all(
                isinstance(ancre.get(k), str) and ancre.get(k) for k in
                ("total_usage_ancre", "disponible_ancre", "somme_reglee_registre_ancre")):
            resultat["motif"] = "ancre 429 absente ou instable pour ce run : ancienne regle"
            return resultat
        resultat["ancre"] = dict(ancre)
        resultat["horodatage_429"] = datetime.datetime.now().astimezone().isoformat(
            timespec="seconds")

        def ecrire_document(document, fd, cible):
            with os.fdopen(fd, "w", encoding="utf-8") as fh:
                os.chmod(cible, 0o600)
                json.dump(document, fh, ensure_ascii=False, indent=2, allow_nan=False)
                fh.write("\n")
                fh.flush()
                os.fsync(fh.fileno())

        def persister_arret_avant_sonde1(motif):
            resultat["motif"] = motif
            resultat["sondes"] = []
            dossier = os.path.join(TRACES, "reprise")
            horodatage_fichier = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
            chemin = os.path.join(dossier, f"r6-rapprochement-429-{horodatage_fichier}.json")
            document = {"version": "R6-amendement-429-v2", "identite": ident,
                        "generation_id": gid, "avant": resultat["avant"], "ancre": ancre,
                        "horodatage_429": resultat["horodatage_429"], "sondes": [],
                        "conclusion": "indetermine", "motif": motif}
            try:
                os.makedirs(dossier, exist_ok=True)
                fd = os.open(chemin, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            except OSError as e:
                resultat["motif"] = f"preuve non ecrite : {type(e).__name__}"
                return
            try:
                ecrire_document(document, fd, chemin)
            except Exception as e:
                resultat.update(motif=f"preuve incomplete : {type(e).__name__}",
                                fichier_preuve_incomplet=chemin)
                return
            resultat["fichier_preuve"] = chemin

        # Amendement 429 v2 (correctif adverse) : attente de DELAI_AVANT_SONDE_429 s avant
        # la sonde 1, pour laisser les appels anterieurs au 429 se regler au solde (retard
        # observe en production : 15 a 40 s). STOP-R6 relu par tranches de
        # TRANCHE_SONDE_429 s ; s'il apparait, issue indeterminee, sans aucune sonde, avec
        # une preuve persistee (sens sur : aucune annulation n'a pu avoir lieu).
        restant_avant = DELAI_AVANT_SONDE_429
        while True:
            if arret_demande():
                persister_arret_avant_sonde1(
                    "arret demande pendant l'attente avant la sonde 1")
                return resultat
            if restant_avant <= 0:
                break
            tranche = min(TRANCHE_SONDE_429, restant_avant)
            dormir(tranche)
            restant_avant -= tranche

        sondes = [self._sonder_429(client, gid)]
        # Attente par tranches : STOP-R6 (ou STOP global) relu entre deux tranches. S'il
        # apparait, issue indeterminee et arret, sans seconde sonde ni annulation ni preuve
        # (les deux sondes n'ont pas ete prises).
        restant = DELAI_SONDE_429
        while True:
            if arret_demande():
                resultat["sondes"] = sondes
                resultat["motif"] = "arret demande pendant l'attente entre les sondes"
                return resultat
            if restant <= 0:
                break
            tranche = min(TRANCHE_SONDE_429, restant)
            dormir(tranche)
            restant -= tranche
        sondes.append(self._sonder_429(client, gid))
        resultat["sondes"] = sondes

        def statut_404(s):
            return (s.get("generation", {}).get("statut_http") == 404
                    and s.get("generation_content", {}).get("statut_http") == 404)

        def usage(s):
            return s.get("credits", {}).get("total_usage")

        critere = {
            "enonce": ("404 sur /generation et /generation/content aux deux sondes ; "
                       "total_usage stable entre les deux sondes ; ecart entre le "
                       "total_usage a la seconde sonde et l'ancre corrigee de la variation "
                       "des couts regles au registre depuis l'ancrage, dans la tolerance"),
            "delai_sonde_s": DELAI_SONDE_429,
            "sondes_404": [statut_404(s) for s in sondes],
            "total_usage_sondes": [usage(s) for s in sondes],
        }
        stable = (all(critere["sondes_404"]) and usage(sondes[0]) is not None
                  and usage(sondes[0]) == usage(sondes[1]))
        critere["total_usage_stable"] = stable
        critere["rempli"] = False
        if stable:
            try:
                modele_ident = json.loads(ident)[0]
                with RegistreGlobal(self.registre) as reg:
                    somme_maintenant = reg.total_reglee()
                    plus_petit = reg.plus_petit_cout_regle(modele_ident)
                total_usage_sonde2 = dollars(usage(sondes[1]))
                total_usage_ancre = dollars(ancre["total_usage_ancre"])
                somme_ancre = dollars(ancre["somme_reglee_registre_ancre"])
            except Exception as e:
                critere["exception_calcul"] = type(e).__name__
            else:
                tolerance = tolerance_429(plus_petit)
                attendu = total_usage_ancre + (somme_maintenant - somme_ancre)
                ecart = abs(total_usage_sonde2 - attendu)
                critere.update(
                    somme_reglee_registre_maintenant=str(somme_maintenant),
                    total_usage_attendu_usd=str(attendu), ecart_usd=str(ecart),
                    tolerance_usd=str(tolerance), rempli=(ecart <= tolerance))
        resultat["critere"] = critere

        horodatage = datetime.datetime.now().strftime("%Y%m%dT%H%M%S%f")
        dossier = os.path.join(TRACES, "reprise")
        nom = f"r6-rapprochement-429-{horodatage}.json"
        chemin = os.path.join(dossier, nom)

        document_base = {"version": "R6-amendement-429-v2", "identite": ident,
                         "generation_id": gid, "avant": resultat["avant"], "ancre": ancre,
                         "horodatage_429": resultat["horodatage_429"], "sondes": sondes,
                         "critere": critere}

        if not critere["rempli"]:
            resultat["motif"] = "critere non rempli"
            document = dict(document_base, conclusion="indetermine", motif=resultat["motif"])
            try:
                os.makedirs(dossier, exist_ok=True)
                fd = os.open(chemin, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
                ecrire_document(document, fd, chemin)
            except OSError as e:
                resultat["motif"] = f"preuve non ecrite : {type(e).__name__}"
                return resultat
            except Exception as e:
                resultat.update(motif=f"preuve incomplete : {type(e).__name__}",
                                fichier_preuve_incomplet=chemin)
                return resultat
            resultat["fichier_preuve"] = chemin
            return resultat

        preuve = (f"{PREUVE_NON_FACTURE_429} generation_id={gid} "
                  f"sondes={sondes[0]['horodatage']},{sondes[1]['horodatage']} preuve={nom}")
        document = dict(document_base, conclusion="non_facture_provisoire",
                        annulation_registre={"preuve": preuve,
                                             "ordre": "preuve ecrite avant annulation"})

        # Ordre sur : 1) preuve `non_facture_provisoire` en O_EXCL, 2) annulation au
        # registre, 3) preuve reecrite en `non_facture` par remplacement atomique, 4) archive
        # du marqueur (faite par _lancer). Un echec a une etape laisse les suivantes
        # intactes : si l'annulation echoue, la preuve reste provisoire.
        try:
            os.makedirs(dossier, exist_ok=True)
            fd = os.open(chemin, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        except OSError as e:
            resultat["motif"] = f"preuve non ecrite : {type(e).__name__}"
            return resultat
        try:
            ecrire_document(document, fd, chemin)
        except Exception as e:
            resultat.update(motif=f"preuve incomplete : {type(e).__name__}",
                            fichier_preuve_incomplet=chemin)
            return resultat
        resultat["fichier_preuve"] = chemin
        try:
            with RegistreGlobal(self.registre) as reg:
                reg.annuler(ident, preuve)
        except Exception as e:
            resultat["motif"] = f"annulation impossible : {type(e).__name__}"
            return resultat
        # Annulation faite : la preuve devient definitive. Si la reecriture echoue, la
        # preuve reste provisoire et l'issue est indeterminee (arret, marqueur conserve).
        document["conclusion"] = "non_facture"
        temporaire = chemin + ".tmp"
        try:
            fd = os.open(temporaire, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            ecrire_document(document, fd, temporaire)
            os.replace(temporaire, chemin)
        except Exception as e:
            resultat["motif"] = (f"preuve finale non ecrite apres annulation : "
                                 f"{type(e).__name__}")
            return resultat
        resultat.update(statut="non_facture", preuve_registre=preuve, horodatage=horodatage)
        return resultat

    def motif_refus_rapprochement_429(self, ident, marqueur=None):
        """Motif de refus si un rapprochement automatique a deja servi pour cette identite.

        Lu sur le registre (toute annulation dont la preuve contient `429`, automatique
        `429-non-facture` ou manuelle) et, si le marqueur est donne, sur les archives
        `.en-cours.annule-*`. Un registre ou une archive illisible refuse aussi.
        """
        try:
            with RegistreGlobal(self.registre) as reg:
                evenements = list(reg.evenements)
        except Exception as e:
            return f"registre illisible avant rapprochement : {type(e).__name__}"
        for e in evenements:
            if e.get("type") != "annulation" or e.get("identite") != ident:
                continue
            texte = str(e.get("preuve", ""))
            if texte.startswith(PREUVE_NON_FACTURE_429):
                return "annulation 429-non-facture deja presente au registre pour cette identite"
            if "429" in texte:
                return "annulation 429 manuelle deja presente au registre pour cette identite"
        if marqueur:
            for archive in sorted(glob.glob(glob.escape(marqueur) + ".annule-*")):
                try:
                    with open(archive, encoding="utf-8") as fh:
                        contenu = json.load(fh)
                except Exception:
                    return "archive de marqueur illisible"
                if not isinstance(contenu, dict) or contenu.get("identite_globale") == ident:
                    return "archive .en-cours.annule-* deja presente pour cette identite"
        return None

    def preuves_429_registre(self):
        """Identite -> nom du fichier de preuve, pour les annulations 429-non-facture."""
        with RegistreGlobal(self.registre) as reg:
            evenements = list(reg.evenements)
        preuves = {}
        for e in evenements:
            texte = str(e.get("preuve", ""))
            if e.get("type") == "annulation" and texte.startswith(PREUVE_NON_FACTURE_429):
                noms = [x[len("preuve="):] for x in texte.split() if x.startswith("preuve=")]
                preuves[e["identite"]] = noms[-1] if noms else ""
        return preuves


def charger_import(chemin_manifeste):
    """Construit l'import scelle des traces nommees explicitement dans un manifeste."""
    manifeste = json.load(open(chemin_manifeste, encoding="utf-8"))
    if manifeste.get("version") != "R6-v2-import-1" or manifeste.get("exhaustif") is not True:
        raise ValueError("manifeste d'import non scelle ou non exhaustif")
    attendus = manifeste.get("attendus")
    if not isinstance(attendus, dict):
        raise ValueError("comptages attendus absents du manifeste")
    cout_incidents = manifeste.get("cout_incidents")
    if not isinstance(cout_incidents, dict):
        cout_incidents = {"observation": "inconnu", "borne_unitaire_usd": "0",
                          "fondement_borne": "non fourni"}
    if cout_incidents.get("observation") != "inconnu":
        raise ValueError("les incidents sans cout ne peuvent pas devenir un cout confirme")
    borne_incident = dollars(cout_incidents.get("borne_unitaire_usd"))
    if not cout_incidents.get("fondement_borne"):
        raise ValueError("fondement de borne des incidents absent")
    base = os.path.dirname(os.path.abspath(chemin_manifeste))
    inventaire, evenements = {}, []
    comptes = collections.Counter()
    for spec in manifeste.get("traces", []):
        chemin = spec["chemin"]
        chemin = chemin if os.path.isabs(chemin) else os.path.normpath(os.path.join(base, chemin))
        passe = spec["passe"]
        classe = spec.get("classe")
        if classe not in ("ancien-pilote", "passe-v2"):
            raise ValueError("classe protocolaire absente ou invalide")
        if ((classe == "ancien-pilote" and passe != "ancien-pilote")
                or (classe == "passe-v2" and passe not in PASSES_LANCEMENT)):
            raise ValueError("ancien pilote et vraies passes v2 confondus")
        contenu = open(chemin, "rb").read()
        empreinte_source = hashlib.sha256(contenu).hexdigest()
        if spec.get("sha256") != empreinte_source:
            raise ValueError("empreinte declaree de trace differente")
        inventaire[chemin] = empreinte_source
        lignes = lignes_existantes(chemin)
        comptes_trace = collections.Counter()
        for numero, d in enumerate(lignes, 1):
            ident = identite_campagne(d["modele"], d["format"], d["version_prompt"],
                                      d["item"], d["camp"], d["identite"], passe)
            brut = json.dumps(d, sort_keys=True, ensure_ascii=False,
                              separators=(",", ":")).encode("utf-8")
            provenance = {"identite": ident,
                           "empreinte_requete": hashlib.sha256(brut).hexdigest(),
                           "fournisseur_impose": d.get("fournisseur") or
                                                  d.get("quantification") or "inconnu-historique",
                           "classe_protocolaire": classe,
                           "source": chemin, "source_sha256": empreinte_source,
                           "ligne_source": numero}
            cout = d.get("cout_annonce_usd")
            if cout is None and d.get("erreur"):
                comptes_trace["incidents"] += 1
                if "cout_incidents" in manifeste:
                    evenements.append({"type": "historique-incertain",
                                       "usd": str(borne_incident),
                                       "cout_observe": "inconnu",
                                       "cout_reponse": "absent",
                                       "nature_usd": "borne",
                                       "fondement_borne": cout_incidents["fondement_borne"],
                                       **provenance})
                else:
                    evenements.append({"type": "reservation", "usd": "0", **provenance})
            else:
                comptes_trace["reponses"] += 1
                cout = d.get("cout_appel_usd") if cout is None else cout
                evenements.append({"type": "historique", "usd": str(dollars(cout)),
                                   "statut_cout": "confirme_par_reponse",
                                   **provenance})
        comptes_trace["lignes"] = len(lignes)
        for nom in ("lignes", "reponses", "incidents"):
            if comptes_trace[nom] != spec.get("attendus", {}).get(nom):
                raise ValueError(f"comptage {nom} different pour {chemin}")
            comptes[nom] += comptes_trace[nom]
    if not inventaire:
        raise ValueError("inventaire historique vide")
    for nom in ("lignes", "reponses", "incidents"):
        if comptes[nom] != attendus.get(nom):
            raise ValueError(f"comptage global {nom} different")
    if dollars(attendus.get("cout_annonce_reponses_usd")) != sum(
            (dollars(e["usd"]) for e in evenements if e["type"] == "historique"),
            Decimal("0")):
        raise ValueError("cout historique total different")
    if dollars(attendus.get("borne_incidents_total_usd", "0")) != sum(
            (dollars(e["usd"]) for e in evenements
             if e["type"] == "historique-incertain"), Decimal("0")):
        raise ValueError("borne totale des incidents differente")
    return inventaire, evenements


def autoriser_configuration_historique(chemin_trace_, chemin_manifeste, configuration):
    """Autorise une reprise ancienne seulement si le manifeste scelle sa configuration."""
    if not chemin_manifeste:
        return False
    # Valide d'abord l'inventaire entier, ses empreintes et ses comptages.
    charger_import(chemin_manifeste)
    manifeste = json.load(open(chemin_manifeste, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(chemin_manifeste))
    cible = os.path.abspath(chemin_trace_)
    for spec in manifeste["traces"]:
        chemin = spec["chemin"]
        chemin = chemin if os.path.isabs(chemin) else os.path.join(base, chemin)
        if os.path.abspath(os.path.normpath(chemin)) == cible:
            return (spec.get("classe") == "ancien-pilote"
                    and spec.get("configuration") == configuration)
    return False


def verifier_liste_manifeste(chemin_liste, chemin_manifeste):
    """Scelle la liste pre-tiree pour qu'une reprise ne change pas silencieusement de cellules."""
    manifeste = json.load(open(chemin_manifeste, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(chemin_manifeste))
    cible = os.path.abspath(chemin_liste)
    spec = None
    for candidate in (manifeste.get("liste_essai"), manifeste.get("liste_plancher")):
        if not isinstance(candidate, dict):
            continue
        declare = candidate.get("chemin")
        declare = declare if os.path.isabs(declare) else os.path.join(base, declare)
        if os.path.abspath(os.path.normpath(declare)) == cible:
            spec = candidate
            break
    if spec is None:
        raise ValueError("liste absente du manifeste ou chemin different")
    contenu = open(chemin_liste, "rb").read()
    if hashlib.sha256(contenu).hexdigest() != spec.get("sha256"):
        raise ValueError("empreinte de la liste d'essai differente")
    if len(lire_liste(chemin_liste)) != spec.get("cellules"):
        raise ValueError("comptage de la liste d'essai different")

# --------------------------------------------------------------------------------------
# 5. Trace, journal, reprise
# --------------------------------------------------------------------------------------

def cle_run(modele, format_, suffixe=""):
    court = modele.replace("/", "-").replace(":", "-")
    return f"{court}-{format_}" + (("-" + suffixe) if suffixe else "")


def chemin_trace(cle):
    return os.path.join(TRACES, f"r6-{cle}.jsonl")


def lignes_existantes(chemin):
    if not os.path.exists(chemin):
        return []
    with open(chemin, encoding="utf-8") as fh:
        lignes = fh.readlines()
    if lignes and not lignes[-1].endswith("\n"):
        raise ValueError("trace non terminee : reconciliation requise")
    try:
        return [json.loads(l) for l in lignes if l.strip()]
    except ValueError:
        raise ValueError("trace corrompue : reconciliation requise") from None


def index_existant(chemin):
    """Refuse une trace tronquee plutot que racheter une reponse potentielle."""
    fait = set()
    if not os.path.exists(chemin):
        return fait
    for d in lignes_existantes(chemin):
        fait.add((d.get("version_prompt"), d.get("format"), d.get("modele"),
                  d.get("item"), d.get("camp"), d.get("identite")))
    return fait


def journaliser(message, chemin=None):
    os.makedirs(TRACES, exist_ok=True)
    with open(chemin or JOURNAL, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


def fichier_arret_present():
    """Rend le marqueur d'arrêt présent, sans jamais le modifier."""
    for chemin in (FICHIER_ARRET_R6, FICHIER_ARRET_GLOBAL):
        if os.path.exists(chemin):
            return chemin
    return None


def arret_demande():
    return fichier_arret_present() is not None


def feu_vert(chemin=None):
    return os.path.exists(chemin or FICHIER_GO)


# --------------------------------------------------------------------------------------
# 6. Le run
# --------------------------------------------------------------------------------------

def appeler_avec_reprise(client, modele, messages, n_predict, attentes=ATTENTES,
                         journal=None, dormir=time.sleep):
    """Un appel, rejoue avec attente croissante sur les seuls incidents de transport.

    Un 429 ou un 5xx n'est pas un rejet : rien n'a ete lu, il n'y a rien a parser. La
    lecon vient de l'essai a blanc du 9 septembre, ou `google/gemma-4-31b-it:free` a rendu
    dix 429 « temporarily rate-limited upstream, shared pool » sur dix cellules et ou le
    client les a comptes comme dix rejets de format, ce qui etait faux.

    Rend (reponse, tentatives, incidents), ou `incidents` est la liste des erreurs de
    transport rencontrees pour cette cellule, y compris quand la derniere tentative
    aboutit.
    """
    incidents = []
    total = len(attentes) + 1
    for essai in range(total):
        if arret_demande():
            return {"erreur": "arret demande", "arret_demande": True}, essai, incidents
        r = client.decrire(modele, messages, n_predict)
        if not r.get("erreur"):
            return r, essai + 1, incidents
        incidents.append({"tentative": essai + 1, "statut": r.get("statut"),
                          "erreur": r["erreur"], "rejouable": bool(r.get("rejouable")),
                          "diagnostic_http": r.get("diagnostic_http", {})})
        if r.get("cout_incertain") or not r.get("rejouable") or essai == total - 1:
            return r, essai + 1, incidents
        attente = attentes[essai]
        message = (f"incident de transport {r.get('statut')}, tentative {essai + 1} sur "
                   f"{total}, attente {attente} s")
        print("  " + message, flush=True)
        journaliser(message, journal)
        if dormir is time.sleep:
            fin = time.monotonic() + attente
            while not arret_demande() and time.monotonic() < fin:
                dormir(min(0.25, max(0, fin - time.monotonic())))
        else:
            dormir(attente)
    return r, total, incidents


def texte_a_parser(texte, fin_seulement):
    """Le texte donne au parse. `fin_seulement > 0` n'en garde que les dernieres lignes.

    Defaut 0 : le texte entier, comme R1. L'option n'existe que pour un modele qui refuse
    de couper son raisonnement et l'ecrit en clair avant sa reponse ; elle est inscrite
    dans la trace, parce qu'elle change ce que le parse voit.
    """
    if not fin_seulement:
        return texte
    lignes = (texte or "").splitlines()
    return "\n".join(lignes[-fin_seulement:])


def lancer(client, modele, format_, table, cellules, budget, cle, transaction=None, **kwargs):
    if (budget.prix_entree or budget.prix_sortie) and urlsplit(client.base).hostname not in (
            "localhost", "127.0.0.1", "::1") and transaction is None:
        raise ValueError("payant bloque : transaction globale et gardes reelles requises")
    os.makedirs(TRACES, exist_ok=True)
    with open(chemin_trace(cle), "a", encoding="utf-8") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
        return _lancer(client, modele, format_, table, cellules, budget, cle,
                       transaction=transaction, **kwargs)


def _lancer(client, modele, format_, table, cellules, budget, cle, n_predict=N_PREDICT,
           limite=None, journal_tous=25, familles_par_item=None, journal=None,
           attentes=ATTENTES, pause=0.0, fin_seulement=0, dormir=time.sleep,
           transaction=None, manifeste_import=None):
    """Joue les cellules donnees et ecrit la trace au fil de l'eau.

    Ecriture incrementale avec flush a chaque ligne : le script doit survivre a un arret
    brutal et reprendre exactement ou il s'etait arrete.

    Trois issues par cellule, et jamais confondues :
      lue         le modele a repondu, `R1.parser` a lu une distribution ;
      rejet       le modele a repondu, le parse a refuse la reponse. C'est une mesure du
                  modele, elle entre dans `taux_rejet` ;
      non jouee   aucune reponse n'a ete recue apres les tentatives de reprise. Ce n'est
                  pas une mesure du modele : la cellule part dans le fichier
                  `r6-<cle>-non-jouees.jsonl`, elle n'entre NI dans la trace principale NI
                  dans `taux_rejet`, et la reprise sur index la rejouera telle quelle.
    """
    chemin = chemin_trace(cle)
    en_cours = chemin + ".en-cours"
    if os.path.exists(en_cours):
        raise ValueError("appel non reconcilie : reprise bloquee, ne pas supprimer le marqueur")
    precedentes = lignes_existantes(chemin)
    configuration = {"raisonnement": client.raisonnement, "fin_seulement": fin_seulement,
                     "max_tokens": n_predict, "base": client.base,
                     "fournisseur_impose": client.fournisseur,
                     "provider_max_price": client.max_price}
    ancienne_scellee = (bool(precedentes)
                        and autoriser_configuration_historique(
                            chemin, manifeste_import, configuration))
    for d in precedentes:
        configuration_incompatible = (
            d.get("configuration") != configuration
            and not (d.get("configuration") is None and ancienne_scellee))
        if d.get("erreur") or configuration_incompatible or (
                d.get("version_prompt"), d.get("format"), d.get("modele")) != (
                FORMATS[format_], format_, modele):
            raise ValueError("trace ancienne ou configuration differente : reconciliation requise")
    # Reconstituer les couts enregistres, jamais les repricer au catalogue du jour.
    budget.cumul = sum(nombre_positif(d["cout_appel_usd"]) for d in precedentes)
    budget.cumul_annonce = sum(nombre_positif(d["cout_annonce_usd"])
                               for d in precedentes if d.get("cout_annonce_usd") is not None)
    budget.cout_max_appel = max((d["cout_appel_usd"] for d in precedentes), default=0.0)
    budget.atteint = budget.cumul > 0 and budget.cumul >= budget.plafond
    cout_avant = budget.cumul
    chemin_non_jouees = os.path.join(TRACES, f"r6-{cle}-non-jouees.jsonl")
    fait = index_existant(chemin)
    deja_faites = len(fait)
    familles_par_item = familles_par_item or {}
    version_prompt = FORMATS[format_]
    print(f"[{cle}] trace {chemin}, {len(fait)} cellules deja faites", flush=True)

    n_cellules = n_rejets = n_non_jouees = n_incidents = n_tentees = 0
    # Amendement 429 : file consommee dans l'ordre ; une cellule rapprochee non facturee
    # est remise une seule fois en fin de file.
    file_cellules = collections.deque(cellules)
    rejouees_429 = set()
    rapproches_429 = 0
    motifs = collections.Counter()
    statuts = collections.Counter()
    latences, raisonnement = [], []
    arret = plafond = arret_seuil_429 = False
    fenetre_429 = collections.deque(maxlen=FENETRE_429)
    t0 = time.time()

    # Le fichier des cellules non jouees n'est ouvert qu'a la premiere : un run sans
    # incident ne laisse pas de fichier vide derriere lui.
    fnj = [None]

    def fichier_non_jouees():
        if fnj[0] is None:
            fnj[0] = open(chemin_non_jouees, "a", encoding="utf-8")
        return fnj[0]

    def ecrire_non_jouee(item, camp, identite, tentatives, r, incidents, extra=None):
        sortie_nj = fichier_non_jouees()
        sortie_nj.write(json.dumps({
            "version_prompt": version_prompt, "format": format_,
            "modele": modele, "cle_modele": cle,
            "item": item, "camp": camp, "identite": identite,
            "non_jouee": True, "tentatives": tentatives,
            "statut": r.get("statut"), "rejouable": bool(r.get("rejouable")),
            "erreur": r["erreur"], "incidents": incidents,
            "horodatage": datetime.datetime.now().isoformat(timespec="seconds"),
            **(extra or {}),
        }, ensure_ascii=False) + "\n")
        sortie_nj.flush()
        os.fsync(sortie_nj.fileno())

    # Amendement 429 : identite -> fichier de preuve, relu au registre pour qu'une
    # cellule rapprochee puis rejouee apres STOP porte aussi la trace du rapprochement.
    preuves_429 = {}
    if transaction is not None and getattr(transaction, "rapprochement_429", False):
        preuves_429 = transaction.preuves_429_registre()
        # Amendement 429 v2, point A : ancre remise a zero pour CETTE execution de
        # `lancer` ; etablie plus bas, au plus tard juste avant le premier POST reel.
        transaction.ancre_429 = None
    ancre_429_tentee = False

    with open(chemin, "a", encoding="utf-8") as fh:
        while file_cellules:
            camp, identite, item = file_cellules.popleft()
            if (version_prompt, format_, modele, item, camp, identite) in fait:
                continue
            if arret_demande():
                arret = True
                message = f"[{cle}] ARRET DEMANDE ({fichier_arret_present()}), arret propre"
                print(message, flush=True)
                journaliser(message, journal)
                break
            if transaction is None and not budget.place_pour_un_appel():
                plafond = True
                message = (f"PLAFOND ATTEINT [{cle}] cumul {budget.cumul:.6f} USD, "
                           f"plafond {budget.plafond:.6f} USD, arret net")
                print(message, flush=True)
                journaliser(message, journal)
                break
            # La limite compte les cellules TENTEES, pas seulement celles qui ont abouti :
            # `--essai 10` doit couter au plus dix cellules, meme si le fournisseur en
            # refuse la moitie.
            if limite is not None and n_tentees >= limite:
                break

            n_tentees += 1
            messages, options = invite(item, camp, identite, format_, table)
            if transaction is None:
                # Ecrit AVANT l'envoi, conserve si crash, timeout ou facture inconnue.
                with open(en_cours, "x", encoding="utf-8") as attente_fh:
                    json.dump({"item": item, "camp": camp, "identite": identite,
                               "configuration": configuration}, attente_fh)
                    attente_fh.flush()
                    os.fsync(attente_fh.fileno())
                r, tentatives, incidents = appeler_avec_reprise(
                    client, modele, messages, n_predict, attentes, journal, dormir)
            else:
                # Amendement 429 v2, point A : ancre etablie une seule fois par execution
                # de `lancer`, avant le tout premier POST reel de cette execution.
                if not ancre_429_tentee and getattr(transaction, "rapprochement_429", False):
                    ancre_429_tentee = True
                    transaction.ancre_429 = transaction.etablir_ancre_429(client, dormir)
                    if transaction.ancre_429 is None:
                        message = (f"[{cle}] ancrage 429 instable ou impossible : "
                                   f"amendement 429 inactif pour ce run (ancienne regle)")
                        print(message, flush=True)
                        journaliser(message, journal)
                    if arret_demande():
                        arret = True
                        message = (f"[{cle}] ARRET DEMANDE ({fichier_arret_present()}) "
                                   f"pendant l'ancrage 429, arret propre")
                        print(message, flush=True)
                        journaliser(message, journal)
                        break
                r = transaction.appeler(client, modele, format_, version_prompt, item,
                                         camp, identite, messages, n_predict, en_cours)
                tentatives, incidents = 1, []
            n_incidents += len(incidents)
            for inc in incidents:
                statuts[str(inc["statut"])] += 1
                fenetre_429.append(inc.get("statut") == 429)
            if incidents and not r.get("erreur"):
                fenetre_429.append(False)
            elif not incidents:
                fenetre_429.append(bool(r.get("erreur") and r.get("statut") == 429))
            seuil_429_depasse = sum(fenetre_429) > SEUIL_429

            if r.get("arret_demande"):
                os.remove(en_cours)
                arret = True
                break

            if r.get("erreur"):
                cellule = (camp, identite, item)
                if (r.get("cout_incertain") and r.get("rapprochement_429")
                        and transaction is not None and cellule not in rejouees_429):
                    ident_429 = r["rapprochement_429"].get("identite")
                    refus = transaction.motif_refus_rapprochement_429(ident_429, en_cours)
                    if refus:
                        rapprochement = {"statut": "indetermine", "motif": refus}
                    else:
                        rapprochement = transaction.rapprocher_429(client, r, dormir)
                    if rapprochement.get("statut") == "non_facture":
                        archive = en_cours + ".annule-" + rapprochement["horodatage"]
                        if os.path.exists(archive):
                            raise ValueError("archive de marqueur deja presente")
                        os.replace(en_cours, archive)   # archive, jamais supprime
                        rejouees_429.add(cellule)
                        preuves_429[ident_429] = os.path.basename(
                            rapprochement["fichier_preuve"])
                        rapproches_429 += 1
                        message = (f"[{cle}] 429 AMBIGU RAPPROCHE NON FACTURE {item}/{camp}/"
                                   f"{identite}, reservation annulee, marqueur archive, "
                                   f"cellule remise en fin de file (rejeu unique)")
                        print(message, flush=True)
                        journaliser(message, journal)
                        if seuil_429_depasse:
                            # La cellule remise en file ne serait ni dans la trace ni dans
                            # les non-jouees : elle est notee non jouee avant l'arret.
                            n_non_jouees += 1
                            ecrire_non_jouee(item, camp, identite, tentatives, r, incidents,
                                             {"rapprochement_429": {
                                                 "statut": "non_facture",
                                                 "fichier_preuve": preuves_429[ident_429]}})
                            arret = arret_seuil_429 = True
                            message = (f"[{cle}] ARRET SEUIL 429 : {sum(fenetre_429)} erreurs "
                                       f"sur {len(fenetre_429)} appels récents")
                            print(message, flush=True)
                            journaliser(message, journal)
                            break
                        file_cellules.append(cellule)
                        continue
                    message = (f"[{cle}] 429 ambigu {item}/{camp}/{identite} : rapprochement "
                               f"{rapprochement.get('statut')}, "
                               f"{rapprochement.get('motif', '')}, arret")
                    print(message, flush=True)
                    journaliser(message, journal)
                # Aucune reponse recue : ce n'est pas un rejet, c'est une cellule non
                # jouee. Elle sort de la trace principale et sera rejouee.
                n_non_jouees += 1
                ecrire_non_jouee(item, camp, identite, tentatives, r, incidents)
                message = (f"[{cle}] cellule NON JOUEE {item}/{camp}/{identite}, "
                           f"{tentatives} tentatives, statut {r.get('statut')}")
                print(message, flush=True)
                journaliser(message, journal)
                if r.get("cout_incertain"):
                    break
                os.remove(en_cours)
                if seuil_429_depasse:
                    arret = arret_seuil_429 = True
                    message = (f"[{cle}] ARRET SEUIL 429 : {sum(fenetre_429)} erreurs "
                               f"sur {len(fenetre_429)} appels récents")
                    print(message, flush=True)
                    journaliser(message, journal)
                    break
                if pause:
                    dormir(pause)
                continue

            distribution, somme, motif = R1.parser(
                texte_a_parser(r["texte"], fin_seulement), options)
            cout_cellule = budget.ajouter(r.get("jetons_entree"), r.get("jetons_sortie"),
                                          r.get("cout_annonce"))
            latences.append(r.get("duree_ms"))
            if r.get("jetons_raisonnement") is not None:
                raisonnement.append(r["jetons_raisonnement"])
            rejet = distribution is None
            if rejet:
                n_rejets += 1
                motifs[motif.split(" :")[0][:60]] += 1

            ligne = {
                # Les cles de R1, pour que r1_evaluer.py --suffixe r6 les lise telles quelles.
                "version_prompt": version_prompt,
                "cle_modele": cle, "modele": modele,
                "quantification": r.get("fournisseur"),   # le fournisseur aval, v2 point 8
                "gabarit": GABARIT,
                "item": item, "famille": familles_par_item.get(item, "hors famille"),
                "camp": camp, "identite": identite,
                "demandeur_camp": R1.ADVERSAIRE[camp] if identite == "adversaire" else None,
                "n_modalites": len(options), "options": options,
                "n_tentatives": 1, "sans_relance": True,
                "rejet": rejet, "rejets_cumules": n_rejets,
                "motif_rejet": motif if rejet else "",
                "somme_brute": None if somme != somme else round(somme, 4),
                "distribution": distribution,
                "tentatives": [{"rappel": False, "sortie_brute": r.get("texte", ""),
                                "duree_ms": round(r.get("duree_ms") or 0.0, 2),
                                "tokens_generes": r.get("jetons_sortie"),
                                "tokens_prompt": r.get("jetons_entree"),
                                "motif_rejet": motif,
                                "somme_brute": None if somme != somme else round(somme, 4)}],
                # Ce que R6 ajoute a R1.
                "format": format_,
                "configuration": configuration,
                "raisonnement": client.raisonnement,
                "fin_seulement": fin_seulement,
                "appels_de_transport": tentatives,
                "incidents_transport": incidents,
                "modele_renvoye": r.get("modele_renvoye"),
                "fournisseur": r.get("fournisseur"),
                "fournisseur_impose": r.get("fournisseur_impose"),
                "empreinte_requete": r.get("empreinte_requete"),
                "identifiant_appel": r.get("identifiant"),
                "raison_arret": r.get("raison"),
                "jetons_entree": r.get("jetons_entree"),
                "jetons_sortie": r.get("jetons_sortie"),
                "jetons_raisonnement": r.get("jetons_raisonnement"),
                "cout_appel_usd": round(cout_cellule, 10),
                "cout_source": budget.source,
                "cout_estime_jetons_usd": (budget.cout(r["jetons_entree"], r["jetons_sortie"])
                    if r.get("jetons_entree") is not None and r.get("jetons_sortie") is not None
                    else None),
                "cout_annonce_usd": r.get("cout_annonce"),
                "cout_cumule_usd": round(budget.cumul, 10),
                "cout_cumule_annonce_usd": round(budget.cumul_annonce, 10),
                "erreur": None,
            }
            if preuves_429 and transaction is not None:
                ident_ligne = identite_campagne(modele, format_, version_prompt, item, camp,
                                                identite, transaction.passe)
                if ident_ligne in preuves_429:
                    # Cellule rejouee apres un 429 rapproche non facture : le rapport doit
                    # pouvoir compter cet incident.
                    ligne["rapprochement_429"] = {"statut": "non_facture",
                                                  "fichier_preuve": preuves_429[ident_ligne]}
            fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            fh.flush()
            os.fsync(fh.fileno())
            os.remove(en_cours)
            fait.add((version_prompt, format_, modele, item, camp, identite))
            n_cellules += 1

            if seuil_429_depasse:
                arret = arret_seuil_429 = True
                message = (f"[{cle}] ARRET SEUIL 429 : {sum(fenetre_429)} erreurs "
                           f"sur {len(fenetre_429)} appels récents")
                print(message, flush=True)
                journaliser(message, journal)
                break

            if n_cellules % journal_tous == 0:
                os.fsync(fh.fileno())
                message = (f"[{cle}] {n_cellules} cellules, {n_rejets} rejets, "
                           f"{n_non_jouees} non jouees, {budget.cumul:.5f} USD, "
                           f"{camp}/{identite}")
                print(message, flush=True)
                journaliser(message, journal)
            if budget.atteint:
                plafond = True
                message = (f"PLAFOND ATTEINT [{cle}] cumul {budget.cumul:.6f} USD, "
                           f"plafond {budget.plafond:.6f} USD, arret net")
                print(message, flush=True)
                journaliser(message, journal)
                break
            if pause:
                dormir(pause)
        os.fsync(fh.fileno())
    if fnj[0] is not None:
        fnj[0].close()

    ecoule = max(time.time() - t0, 1e-9)
    lat = [x for x in latences if x is not None]
    # Le raisonnement est il vraiment coupe ? Trois reponses, jamais une supposition :
    # « oui » si le fournisseur compte les jetons de raisonnement et qu'ils sont tous nuls,
    # « non » s'il en compte au moins un, « inconnu » s'il ne les compte pas du tout.
    if not raisonnement or (len(raisonnement) < n_cellules and max(raisonnement) == 0):
        desactive = "inconnu, le fournisseur ne compte pas les jetons de raisonnement"
    elif max(raisonnement) > 0:
        desactive = "non"
    else:
        desactive = "oui"
    return {
        "cle": cle, "modele": modele, "format": format_,
        "version_prompt": version_prompt, "gabarit": GABARIT,
        "raisonnement": client.raisonnement,
        "raisonnement_desactive_effectif": desactive,
        "fin_seulement": fin_seulement,
        "cellules": n_cellules, "cellules_tentees": n_tentees,
        "deja_faites": deja_faites, "cellules_trace": len(fait), "rejets": n_rejets,
        "taux_rejet": round(n_rejets / n_cellules, 4) if n_cellules else 0.0,
        "motifs_de_rejet": dict(motifs),
        "erreurs_reseau": n_incidents,
        "statuts_reseau": dict(statuts),
        "non_jouees": n_non_jouees,
        "trace_non_jouees": chemin_non_jouees if n_non_jouees else None,
        "secondes": round(ecoule, 1),
        "latence_ms_moyenne": round(sum(lat) / len(lat), 1) if lat else None,
        "latence_ms_mediane": round(sorted(lat)[len(lat) // 2], 1) if lat else None,
        "jetons_raisonnement_moyens": (round(sum(raisonnement) / len(raisonnement), 2)
                                       if raisonnement else None),
        "jetons_raisonnement_max": max(raisonnement) if raisonnement else None,
        "cout_usd": round(budget.cumul, 10),
        "cout_annonce_usd": round(budget.cumul_annonce, 10),
        "cout_session_usd": round(budget.cumul - cout_avant, 10),
        "cout_par_cellule_usd": round((budget.cumul - cout_avant) / n_cellules, 10) if n_cellules else None,
        "reconciliation_requise": os.path.exists(en_cours),
        "limite_demandee": limite,
        "plafond_usd": budget.plafond, "plafond_atteint": plafond,
        "arret_demande": arret, "trace": chemin,
        "arret_seuil_429": arret_seuil_429,
        "erreurs_429_fenetre": sum(fenetre_429),
        "appels_fenetre_429": len(fenetre_429),
        "rapproches_429": rapproches_429,
    }


def resume_essai(resume, cle, cellules_du_plan):
    """Resume d'essai : cout reel par cellule, taux de rejet, latence, projection.

    Les quatre mesures d'arret de la v2 (cout par cellule, jetons de raisonnement, taux de
    rejet, latence et refus de debit) sont toutes ici, avec la projection sur le plan.
    """
    e = dict(resume)
    e["essai"] = True
    e["cellules_du_plan"] = cellules_du_plan
    # La ligne exigee apres l'essai a blanc du 9 septembre : elle est lue sur les jetons
    # factures, jamais deduite du parametre envoye.
    e["raisonnement_desactive_effectif"] = resume.get("raisonnement_desactive_effectif")
    e["essai_propre"] = bool(
        resume.get("cellules", 0) >= 10
        and resume.get("cellules") == resume.get("limite_demandee")
        and not resume.get("arret_demande") and not resume.get("plafond_atteint")
        and not resume.get("reconciliation_requise")
        and resume.get("taux_rejet", 1.0) <= 0.20
        and resume.get("non_jouees", 0) == 0
        and resume.get("raisonnement_desactive_effectif") == "oui")
    e["projection_plan_usd"] = (round(e["cout_par_cellule_usd"] * cellules_du_plan, 6)
                                 if e["cout_par_cellule_usd"] is not None else None)
    e["projection_plan_min"] = (round(e["secondes"] / e["cellules"] * cellules_du_plan / 60, 1)
                                if e["cellules"] else None)
    chemin = os.path.join(TRACES, f"r6-essai-{cle}.json")
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(e, fh, indent=2, ensure_ascii=False)
    return chemin, e


# --------------------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", help="identifiant OpenRouter, par exemple openai/gpt-5.6-luna")
    ap.add_argument("--plan", default="f1", choices=list(PLANS),
                    help="f1 : 894 cellules, gabarit seul. f2 : 316 cellules, gabarit "
                         "plus trois exemples, 79 items orientes, gauche et droite")
    ap.add_argument("--format", dest="format_", default=None, choices=list(FORMATS),
                    help="par defaut celui du plan")
    ap.add_argument("--items", type=int, default=0, help="n premiers items, pour un essai")
    ap.add_argument("--liste", default=None,
                    help="fichier de cellules tirees d'avance, une par ligne "
                         "item<tab>camp<tab>identite")
    ap.add_argument("--tirer-liste", type=int, default=0,
                    help="tire N cellules du plan, les ecrit dans --liste et sort. "
                         "Aucun appel de modele.")
    ap.add_argument("--max-tokens", type=int, default=N_PREDICT)
    ap.add_argument("--raisonnement", default="off", choices=list(RAISONNEMENTS),
                    help="off : desactivation explicite, le defaut. none : l'autre "
                         "orthographe. aucun : n'envoie rien, a reserver a un serveur "
                         "local qui refuse le parametre.")
    ap.add_argument("--fin-seulement", type=int, default=0,
                    help="ne donner au parse que les N dernieres lignes de la sortie. "
                         "0 par defaut, c'est a dire la sortie entiere, comme R1. A "
                         "n'employer que sur un modele qui refuse de couper son "
                         "raisonnement, avec --max-tokens releve.")
    ap.add_argument("--pause", type=float, default=0.0,
                    help="secondes d'attente entre deux cellules. 3.5 tient les 20 "
                         "requetes par minute du palier gratuit d'OpenRouter.")
    ap.add_argument("--plafond", type=float,
                    help="plafond dur en USD, obligatoire des qu'un appel part")
    ap.add_argument("--essai", type=int, default=0,
                    help="ne joue que N cellules et ecrit un resume de cout reel")
    ap.add_argument("--suffixe", default="")
    ap.add_argument("--fournisseur", default=None,
                    help="fournisseur aval impose, repli interdit")
    ap.add_argument("--max-price-prompt", default=None,
                    help="provider.max_price.prompt, USD par million de jetons")
    ap.add_argument("--max-price-completion", default=None,
                    help="provider.max_price.completion, USD par million de jetons")
    ap.add_argument("--max-prompt-tokens", type=int, default=None,
                    help="borne justifiee des jetons d'entree, obligatoire en payant")
    ap.add_argument("--borne-appel", default=None,
                    help="borne USD du dernier appel, frais compris")
    ap.add_argument("--plafond-modele", default=None,
                    help="plafond cumulatif USD partagé entre F1, F2 et plancher")
    ap.add_argument("--passe", choices=PASSES_LANCEMENT,
                    default=None, help="identite de passe globale, obligatoire en payant")
    ap.add_argument("--registre", default=REGISTRE)
    ap.add_argument("--manifeste-import", default=None,
                    help="inventaire exhaustif scelle des traces R6 existantes")
    ap.add_argument("--initialiser-registre", action="store_true",
                    help="importe le manifeste dans le registre et sort, aucun reseau")
    ap.add_argument("--catalogue", action="store_true",
                    help="GET /models, rafraichit le cache de prix, aucun appel de modele")
    ap.add_argument("--solde", action="store_true",
                    help="GET /credits, aucun appel de modele")
    args = ap.parse_args(argv)

    os.makedirs(TRACES, exist_ok=True)
    if args.initialiser_registre:
        if not args.manifeste_import:
            sys.exit("--initialiser-registre exige --manifeste-import")
        inventaire, evenements = charger_import(args.manifeste_import)
        with RegistreGlobal(args.registre) as reg:
            reg.initialiser_evenements(inventaire, evenements)
        print(f"registre initialise : {len(evenements)} operations, {len(inventaire)} traces")
        return 0

    if arret_demande() and not args.tirer_liste:
        sys.exit(f"fichier d'arret present : {fichier_arret_present()}. Aucun acces reseau.")

    if args.catalogue:
        cat = catalogue(rafraichir=True)
        print(f"catalogue rafraichi : {len(cat['data'])} modeles, {CATALOGUE}")
        return 0
    if args.solde:
        s = solde()
        reste = float(s["total_credits"]) - float(s["total_usage"])
        print(f"credits {s['total_credits']}, utilises {s['total_usage']:.6f}, "
              f"reste {reste:.6f} USD")
        return 0

    table = nomenclature()
    from a2_baselines_gss import charger
    _ids, tous_items, _y1, _y2, _x, _attributs = charger()
    items, camps, identites, format_plan = plan_cellules(args.plan, list(tous_items),
                                                         args.items)
    format_ = args.format_ or format_plan
    familles_par_item = {it: nom for nom, membres in FAMILLES.items() for it in membres}

    if args.tirer_liste:
        if not args.liste:
            sys.exit("--tirer-liste exige --liste, le fichier ou ecrire les cellules")
        cellules = tirer_liste(items, camps, identites, args.tirer_liste)
        ecrire_liste(cellules, args.liste)
        print(f"{len(cellules)} cellules tirees et ecrites : {args.liste}")
        return 0

    if not args.modele:
        sys.exit("--modele est obligatoire")
    if args.plafond is None:
        sys.exit("--plafond est obligatoire : aucun appel ne part sans plafond dur")
    if not math.isfinite(args.plafond) or not 0 <= args.plafond <= 4.50:
        sys.exit("--plafond doit etre fini et compris entre 0 et 4.50 USD")
    if args.max_tokens <= 0 or args.essai < 0 or args.fin_seulement < 0:
        sys.exit("limites de generation/essai invalides")

    if not os.path.exists(CATALOGUE):
        sys.exit(f"catalogue absent : {CATALOGUE}. Executer --catalogue separement.")
    cat = catalogue()
    p_entree, p_sortie, gratuit = prix(args.modele, cat)

    if not gratuit and not feu_vert():
        sys.exit(f"feu vert absent : {FICHIER_GO}. Aucun appel payant ne part tant que ce "
                 f"fichier n'existe pas. Les modeles :free passent sans lui.")
    if arret_demande():
        sys.exit(f"fichier d'arret present : {fichier_arret_present()}. Le retirer avant de lancer.")

    if not gratuit:
        manquants = [nom for nom, valeur in (
            ("--fournisseur", args.fournisseur),
            ("--max-price-prompt", args.max_price_prompt),
            ("--max-price-completion", args.max_price_completion),
            ("--max-prompt-tokens", args.max_prompt_tokens),
            ("--borne-appel", args.borne_appel), ("--passe", args.passe),
            ("--manifeste-import", args.manifeste_import)) if valeur is None]
        if manquants:
            sys.exit("gardes payantes incompletes : " + ", ".join(manquants))
        if args.raisonnement == "aucun":
            sys.exit("--raisonnement aucun interdit en payant")
        if args.passe in PASSES_COUT_MODELE and args.plafond_modele is None:
            sys.exit("--plafond-modele obligatoire pour campagne et plancher")
        if args.plafond_modele is not None:
            try:
                plafond_modele = dollars(args.plafond_modele)
            except ValueError:
                sys.exit("--plafond-modele doit etre fini et positif")
            if plafond_modele <= 0 or plafond_modele > LIMITE_CLE_R6:
                sys.exit("--plafond-modele doit verifier 0 < plafond <= 4.40")
        if args.passe in PASSES_PILOTE:
            erreurs_pilote = erreurs_configuration_pilote(
                args.modele, args.fournisseur, args.essai, args.plafond, args.max_tokens,
                args.raisonnement, args.max_prompt_tokens, args.borne_appel,
                {"prompt": args.max_price_prompt,
                 "completion": args.max_price_completion})
            if erreurs_pilote:
                sys.exit("gardes pilote : " + "; ".join(erreurs_pilote))

    cellules = (lire_liste(args.liste) if args.liste
                else list(R1.cellules(items, camps, identites)))
    if args.manifeste_import and args.liste:
        verifier_liste_manifeste(args.liste, args.manifeste_import)
    suffixe = args.suffixe or ("essai" if args.essai else "")
    cle_r = cle_run(args.modele, format_, suffixe)
    budget = Budget(args.plafond, p_entree, p_sortie, JETONS_ESTIMES[format_])
    transaction = None
    max_price = None
    if not gratuit:
        max_price = {"prompt": str(dollars(args.max_price_prompt)),
                     "completion": str(dollars(args.max_price_completion))}
        inventaire, _evenements = charger_import(args.manifeste_import)
        transaction = TransactionPayante(args.registre, inventaire, args.passe,
                                          args.borne_appel, args.max_prompt_tokens,
                                          plafond_modele=args.plafond_modele)
    cle = cle_api()
    client = ClientChat(cle, raisonnement=args.raisonnement, fournisseur=args.fournisseur,
                        max_price=max_price)

    s = None if transaction else solde(cle)
    reste = None if s is None else float(s["total_credits"]) - float(s["total_usage"])
    solde_entete = "relu sous verrou par cellule" if reste is None else f"{reste:.4f} USD"
    entete = (f"popsim r6, oracle distant. {args.modele}, plan {args.plan}, format "
              f"{format_}, raisonnement {args.raisonnement}, max_tokens "
              f"{args.max_tokens}, plafond {args.plafond:.4f} "
              f"USD, {'gratuit' if gratuit else 'payant'}, feu vert "
              f"{'present' if feu_vert() else 'absent'}, solde {solde_entete}")
    print(entete, flush=True)
    journaliser("DEBUT " + entete)
    print(f"{len(cellules)} cellules a jouer, prix {p_entree:.3e} / {p_sortie:.3e} USD "
          f"par jeton", flush=True)

    r = lancer(client, args.modele, format_, table, cellules, budget, cle_r,
               n_predict=args.max_tokens, limite=args.essai or None,
               familles_par_item=familles_par_item, pause=args.pause,
               fin_seulement=args.fin_seulement, transaction=transaction,
               manifeste_import=args.manifeste_import)
    r["solde_avant_usd"] = round(reste, 6) if reste is not None else None
    chemin_resume = os.path.join(TRACES, f"r6-{cle_r}-resume.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump(r, fh, indent=2, ensure_ascii=False)
    print(f"resume ecrit : {chemin_resume}", flush=True)
    if args.essai:
        cellules_projection = (PLANS[args.plan]["cellules"] if gratuit else
                                sum(p["cellules"] for p in PLANS.values()) + 40 + 20)
        c, e = resume_essai(r, cle_r, cellules_projection)
        print(f"essai : {e['cellules']} cellules lues, {e['taux_rejet']:.2%} de rejet "
              f"de parse, {e['non_jouees']} non jouees, {e['erreurs_reseau']} incidents "
              f"de transport {e['statuts_reseau'] or ''}, "
              f"{e['cout_par_cellule_usd']:.6f} USD par cellule, "
              f"latence mediane {e['latence_ms_mediane']} ms, "
              f"jetons de raisonnement {e['jetons_raisonnement_moyens']} "
              f"(max {e['jetons_raisonnement_max']}), "
              f"projection {e['projection_plan_usd']} USD", flush=True)
        print(f"raisonnement desactive effectif : "
              f"{e['raisonnement_desactive_effectif']}", flush=True)
        print(f"essai propre : {'oui' if e['essai_propre'] else 'non'}", flush=True)
        print(f"resume d'essai ecrit : {c}", flush=True)
    journaliser(f"RUN TERMINE [{cle_r}] {r['cellules']} cellules, {r['rejets']} rejets, "
                f"{r['non_jouees']} non jouees, {r['erreurs_reseau']} incidents, "
                f"{r['cout_usd']:.6f} USD")
    print(f"RUN TERMINE {r['cellules']} cellules, {r['rejets']} rejets, "
          f"{r['non_jouees']} non jouees, {r['erreurs_reseau']} incidents, "
          f"{r['cout_usd']:.6f} USD", flush=True)
    return 3 if r["reconciliation_requise"] else 2 if r["plafond_atteint"] else 0


if __name__ == "__main__":
    sys.exit(main())
