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
sont lus dans `usage.completion_tokens_details.reasoning_tokens`.

Depense. Zero appel payant tant que `data/traces/GO-R6` n'existe pas. Un modele dont les
deux prix du catalogue sont nuls (les `:free`, et le serveur local) passe sans ce feu vert,
mais reste soumis au plafond. Le plafond `--plafond` est en USD et il est dur : au
depassement, le script ecrit « PLAFOND ATTEINT » dans son journal et s'arrete net. Le cout
de chaque appel est calcule au prix de l'inventaire (catalogue `GET /api/v1/models`, en
cache dans `data/traces/r6-modeles-openrouter.json`) a partir du champ `usage` renvoye par
OpenRouter, et le cumul est ecrit sur chaque ligne de trace, a cote du cout que le
fournisseur annonce lui meme.

Arret : `touch data/traces/STOP` arrete le run entre deux appels, trace fermee, resume
ecrit, code de sortie 0. Le fichier n'est jamais efface par le script.

Reprise : l'index unique est (version_prompt, format, modele, item, camp, identite). Une
relance ne refait aucun appel deja ecrit.

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
import os
import random
import sys
import time
import urllib.error
import urllib.request

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

FICHIER_ARRET = R1.FICHIER_ARRET                     # data/traces/STOP, celui de R1
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

# Reglages de raisonnement acceptes. `low` est l'equivalent API du `Reasoning: low` que R1
# fixait dans le gabarit harmony ; `off` desactive le raisonnement quand le modele le
# permet ; `aucun` n'envoie aucun champ, pour les serveurs qui refusent le parametre.
RAISONNEMENTS = ("low", "minimal", "off", "aucun")


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


def _lire(url, cle, charge=None, timeout=180):
    """Un aller retour HTTP. Le message d'erreur ne contient jamais les en tetes."""
    donnees = json.dumps(charge).encode("utf-8") if charge is not None else None
    req = urllib.request.Request(url, data=donnees, headers=entetes(cle))
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


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


def prix(modele, cat):
    """(prix entree, prix sortie) en USD par jeton, et si le modele est gratuit."""
    for m in cat["data"]:
        if m["id"] == modele:
            p = m.get("pricing", {})
            entree = float(p.get("prompt", 0) or 0)
            sortie = float(p.get("completion", 0) or 0)
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
    """Un appel, une reponse, aucune relance. Les erreurs HTTP sont des rejets comptes.

    `base` est pointee sur OpenRouter pour le run, et sur le `llama-server` local pour la
    verification de la voie `chat` : le meme code sert les deux, ce qui est le seul moyen
    de verifier le client lui meme sans reseau.
    """

    def __init__(self, cle, base=BASE, timeout=180, raisonnement="low",
                 usage_inclus=True, fournisseur=None):
        self.cle = cle
        self.base = base
        self.timeout = timeout
        self.raisonnement = raisonnement
        self.usage_inclus = usage_inclus
        self.fournisseur = fournisseur

    def charge_raisonnement(self):
        if self.raisonnement in (None, "aucun"):
            return None
        if self.raisonnement == "off":
            return {"enabled": False, "exclude": True}
        return {"effort": self.raisonnement, "exclude": True}

    def decrire(self, modele, messages, n_predict=N_PREDICT):
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
        debut = time.perf_counter()
        try:
            r = _lire(self.base + "/chat/completions", self.cle, charge, self.timeout)
        except urllib.error.HTTPError as e:
            corps = e.read().decode("utf-8", "replace")[:400]
            return {"erreur": f"HTTP {e.code} : {corps}",
                    "duree_ms": (time.perf_counter() - debut) * 1000.0}
        except Exception as e:                       # reseau, delai, corps illisible
            return {"erreur": f"{type(e).__name__} : {e}",
                    "duree_ms": (time.perf_counter() - debut) * 1000.0}
        duree = (time.perf_counter() - debut) * 1000.0
        if r.get("error"):
            return {"erreur": f"erreur du fournisseur : {str(r['error'])[:400]}",
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

class Budget:
    """Plafond dur en USD. Il ne se depasse pas : au depassement, le run s'arrete net."""

    def __init__(self, plafond, prix_entree, prix_sortie, jetons_estimes=(210, 20)):
        self.plafond = float(plafond)
        self.prix_entree = prix_entree
        self.prix_sortie = prix_sortie
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

        Sans cela, un modele qui coute trois fois l'estimation ferait franchir le plafond
        avant qu'on s'en apercoive : le plafond serait mou.
        """
        return max(self.cout(*self.jetons_estimes), self.cout_max_appel)

    def place_pour_un_appel(self):
        return (self.cumul + self.estimation_appel()) <= self.plafond

    def ajouter(self, jetons_entree, jetons_sortie, cout_annonce=None):
        c = self.cout(jetons_entree, jetons_sortie)
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


# --------------------------------------------------------------------------------------
# 5. Trace, journal, reprise
# --------------------------------------------------------------------------------------

def cle_run(modele, format_, suffixe=""):
    court = modele.replace("/", "-").replace(":", "-")
    return f"{court}-{format_}" + (("-" + suffixe) if suffixe else "")


def chemin_trace(cle):
    return os.path.join(TRACES, f"r6-{cle}.jsonl")


def index_existant(chemin):
    """Cellules deja ecrites. Une ligne tronquee ne fait pas echouer la reprise."""
    fait = set()
    if not os.path.exists(chemin):
        return fait
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            fait.add((d.get("version_prompt"), d.get("format"), d.get("modele"),
                      d.get("item"), d.get("camp"), d.get("identite")))
    return fait


def journaliser(message, chemin=None):
    os.makedirs(TRACES, exist_ok=True)
    with open(chemin or JOURNAL, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


def arret_demande():
    return os.path.exists(FICHIER_ARRET)


def feu_vert():
    return os.path.exists(FICHIER_GO)


# --------------------------------------------------------------------------------------
# 6. Le run
# --------------------------------------------------------------------------------------

def lancer(client, modele, format_, table, cellules, budget, cle, n_predict=N_PREDICT,
           limite=None, journal_tous=25, familles_par_item=None, journal=None):
    """Joue les cellules donnees et ecrit la trace au fil de l'eau.

    Ecriture incrementale avec flush a chaque ligne : le script doit survivre a un arret
    brutal et reprendre exactement ou il s'etait arrete.
    """
    chemin = chemin_trace(cle)
    fait = index_existant(chemin)
    familles_par_item = familles_par_item or {}
    version_prompt = FORMATS[format_]
    print(f"[{cle}] trace {chemin}, {len(fait)} cellules deja faites", flush=True)

    n_cellules = n_rejets = 0
    motifs = collections.Counter()
    latences, raisonnement = [], []
    arret = plafond = False
    t0 = time.time()

    with open(chemin, "a", encoding="utf-8") as fh:
        for camp, identite, item in cellules:
            if (version_prompt, format_, modele, item, camp, identite) in fait:
                continue
            if arret_demande():
                arret = True
                message = f"[{cle}] ARRET DEMANDE ({FICHIER_ARRET}), arret propre"
                print(message, flush=True)
                journaliser(message, journal)
                break
            if not budget.place_pour_un_appel():
                plafond = True
                message = (f"PLAFOND ATTEINT [{cle}] cumul {budget.cumul:.6f} USD, "
                           f"plafond {budget.plafond:.6f} USD, arret net")
                print(message, flush=True)
                journaliser(message, journal)
                break
            if limite is not None and n_cellules >= limite:
                break

            messages, options = invite(item, camp, identite, format_, table)
            r = client.decrire(modele, messages, n_predict)
            if r.get("erreur"):
                distribution, somme, motif = None, float("nan"), r["erreur"]
                cout_cellule = 0.0
            else:
                distribution, somme, motif = R1.parser(r["texte"], options)
                cout_cellule = budget.ajouter(r.get("jetons_entree"),
                                              r.get("jetons_sortie"),
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
                "raisonnement": client.raisonnement,
                "modele_renvoye": r.get("modele_renvoye"),
                "fournisseur": r.get("fournisseur"),
                "identifiant_appel": r.get("identifiant"),
                "raison_arret": r.get("raison"),
                "jetons_entree": r.get("jetons_entree"),
                "jetons_sortie": r.get("jetons_sortie"),
                "jetons_raisonnement": r.get("jetons_raisonnement"),
                "cout_appel_usd": round(cout_cellule, 10),
                "cout_annonce_usd": r.get("cout_annonce"),
                "cout_cumule_usd": round(budget.cumul, 10),
                "cout_cumule_annonce_usd": round(budget.cumul_annonce, 10),
                "erreur": r.get("erreur"),
            }
            fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            fh.flush()
            n_cellules += 1

            if n_cellules % journal_tous == 0:
                os.fsync(fh.fileno())
                message = (f"[{cle}] {n_cellules} cellules, {n_rejets} rejets, "
                           f"{budget.cumul:.5f} USD, {camp}/{identite}")
                print(message, flush=True)
                journaliser(message, journal)
            if budget.atteint:
                plafond = True
                message = (f"PLAFOND ATTEINT [{cle}] cumul {budget.cumul:.6f} USD, "
                           f"plafond {budget.plafond:.6f} USD, arret net")
                print(message, flush=True)
                journaliser(message, journal)
                break
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    lat = [x for x in latences if x is not None]
    return {
        "cle": cle, "modele": modele, "format": format_,
        "version_prompt": version_prompt, "gabarit": GABARIT,
        "raisonnement": client.raisonnement,
        "cellules": n_cellules, "deja_faites": len(fait), "rejets": n_rejets,
        "taux_rejet": round(n_rejets / n_cellules, 4) if n_cellules else 0.0,
        "motifs_de_rejet": dict(motifs),
        "secondes": round(ecoule, 1),
        "latence_ms_moyenne": round(sum(lat) / len(lat), 1) if lat else None,
        "latence_ms_mediane": round(sorted(lat)[len(lat) // 2], 1) if lat else None,
        "jetons_raisonnement_moyens": (round(sum(raisonnement) / len(raisonnement), 2)
                                       if raisonnement else None),
        "cout_usd": round(budget.cumul, 10),
        "cout_annonce_usd": round(budget.cumul_annonce, 10),
        "cout_par_cellule_usd": round(budget.cumul / n_cellules, 10) if n_cellules else 0.0,
        "plafond_usd": budget.plafond, "plafond_atteint": plafond,
        "arret_demande": arret, "trace": chemin,
    }


def resume_essai(resume, cle, cellules_du_plan):
    """Resume d'essai : cout reel par cellule, taux de rejet, latence, projection.

    Les quatre mesures d'arret de la v2 (cout par cellule, jetons de raisonnement, taux de
    rejet, latence et refus de debit) sont toutes ici, avec la projection sur le plan.
    """
    e = dict(resume)
    e["essai"] = True
    e["cellules_du_plan"] = cellules_du_plan
    e["projection_plan_usd"] = round(e["cout_par_cellule_usd"] * cellules_du_plan, 6)
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
    ap.add_argument("--raisonnement", default="low", choices=list(RAISONNEMENTS))
    ap.add_argument("--plafond", type=float,
                    help="plafond dur en USD, obligatoire des qu'un appel part")
    ap.add_argument("--essai", type=int, default=0,
                    help="ne joue que N cellules et ecrit un resume de cout reel")
    ap.add_argument("--suffixe", default="")
    ap.add_argument("--fournisseur", default=None,
                    help="fournisseur aval impose, repli interdit")
    ap.add_argument("--catalogue", action="store_true",
                    help="GET /models, rafraichit le cache de prix, aucun appel de modele")
    ap.add_argument("--solde", action="store_true",
                    help="GET /credits, aucun appel de modele")
    args = ap.parse_args(argv)

    os.makedirs(TRACES, exist_ok=True)

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
    if args.plafond < 0:
        sys.exit("--plafond doit etre positif ou nul")

    cle = cle_api()
    cat = catalogue(cle)
    p_entree, p_sortie, gratuit = prix(args.modele, cat)

    if not gratuit and not feu_vert():
        sys.exit(f"feu vert absent : {FICHIER_GO}. Aucun appel payant ne part tant que ce "
                 f"fichier n'existe pas. Les modeles :free passent sans lui.")
    if arret_demande():
        sys.exit(f"fichier d'arret present : {FICHIER_ARRET}. Le retirer avant de lancer.")

    cellules = (lire_liste(args.liste) if args.liste
                else list(R1.cellules(items, camps, identites)))
    suffixe = args.suffixe or ("essai" if args.essai else "")
    cle_r = cle_run(args.modele, format_, suffixe)
    budget = Budget(args.plafond, p_entree, p_sortie, JETONS_ESTIMES[format_])
    client = ClientChat(cle, raisonnement=args.raisonnement, fournisseur=args.fournisseur)

    s = solde(cle)
    reste = float(s["total_credits"]) - float(s["total_usage"])
    entete = (f"popsim r6, oracle distant. {args.modele}, plan {args.plan}, format "
              f"{format_}, raisonnement {args.raisonnement}, plafond {args.plafond:.4f} "
              f"USD, {'gratuit' if gratuit else 'payant'}, feu vert "
              f"{'present' if feu_vert() else 'absent'}, solde {reste:.4f} USD")
    print(entete, flush=True)
    journaliser("DEBUT " + entete)
    print(f"{len(cellules)} cellules a jouer, prix {p_entree:.3e} / {p_sortie:.3e} USD "
          f"par jeton", flush=True)

    r = lancer(client, args.modele, format_, table, cellules, budget, cle_r,
               n_predict=args.max_tokens, limite=args.essai or None,
               familles_par_item=familles_par_item)
    r["solde_avant_usd"] = round(reste, 6)
    chemin_resume = os.path.join(TRACES, f"r6-{cle_r}-resume.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump(r, fh, indent=2, ensure_ascii=False)
    print(f"resume ecrit : {chemin_resume}", flush=True)
    if args.essai:
        c, e = resume_essai(r, cle_r, PLANS[args.plan]["cellules"])
        print(f"essai : {e['cellules']} cellules, {e['taux_rejet']:.2%} de rejet, "
              f"{e['cout_par_cellule_usd']:.6f} USD par cellule, "
              f"latence mediane {e['latence_ms_mediane']} ms, "
              f"jetons de raisonnement {e['jetons_raisonnement_moyens']}, "
              f"projection {e['projection_plan_usd']:.4f} USD", flush=True)
        print(f"resume d'essai ecrit : {c}", flush=True)
    journaliser(f"RUN TERMINE [{cle_r}] {r['cellules']} cellules, {r['rejets']} rejets, "
                f"{r['cout_usd']:.6f} USD")
    print(f"RUN TERMINE {r['cellules']} cellules, {r['rejets']} rejets, "
          f"{r['cout_usd']:.6f} USD", flush=True)
    return 2 if r["plafond_atteint"] else 0


if __name__ == "__main__":
    sys.exit(main())
