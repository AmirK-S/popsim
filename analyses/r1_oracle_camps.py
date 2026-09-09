"""
r1_oracle_camps : l'oracle des camps. Ce que les modeles disent que pense chaque camp.

Statut : script d'experience, pas du code de production. Il produit le premier terme de la
comparaison a trois termes du programme A de MOONSHOTS.md : realite contre croyance du
modele. Le second terme, la croyance humaine de second ordre, exige les items de l'ANES et
n'est pas produit ici ; la structure de sortie lui laisse sa place (colonne `source` des
distributions, valeurs `reel_w1`, `reel_w2`, `modele`).

Ce qu'il fait. Pour chaque item du GSS, chaque camp d'ideologie et chaque identite de
demandeur, il demande a un modele local la repartition en pourcentages des reponses de ce
camp aux Etats Unis, avec les modalites exactes de la nomenclature. C'est la voie
« describe » de arXiv 2607.25292, jamais lancee dans ce dossier (a27, section 7.3 (a)) :
un appel par cellule, une generation de texte, et non la lecture d'une distribution de
token comme en a5.

Difference de nature avec a5, a ecrire dans tout rapport qui melange les deux. a5 fait
parler le modele A LA PLACE d'une personne et lit la probabilite d'un token de reponse.
Ici le modele parle DE un groupe et ecrit une distribution en clair. Les deux quantites
ne sont pas commensurables ; seul le referent humain, lui, est le meme.

Protocole, fixe avant le premier appel dans resultats/r1-preenregistrement.md :
  149 items x 3 camps x 2 identites x 3 modeles = 2 682 appels.
  Temperature 0, n_predict 150, un appel par cellule, un serveur par modele.
  Format de sortie contraint : une ligne par modalite, `LETTRE: pourcentage`, total 100.
  Parse strict, une relance avec rappel de format, puis rejet documente. Depuis le
  9 septembre 2026, `--sans-relance` supprime la relance (r5-preenregistrement.md section
  « Relance », apres la mesure de r4-resultats.md section 3.1) : le defaut, lui, reste le
  comportement d'origine, pour que R1 et R4 se rejouent au caractere pres.

Entree  : data/osf-t6g7k-stanford, non versionne (vagues 1 et 2, 1 052 personnes,
          149 items, nomenclature question_master/gss/main.csv).
          data/modeles/gguf/*.gguf, non versionne.
Sortie  : data/traces/r1-<cle modele>.jsonl, une ligne par appel, non versionne.
          data/traces/r1-distributions-reelles.csv, les distributions humaines par camp.
          data/traces/r1-resume.json.
          data/traces/r1-run.log recoit la ligne « RUN TERMINE » a la fin, quoi qu'il
          arrive, parce qu'un second run attend la machine.

Arret : `touch data/traces/STOP` arrete le run entre deux appels, trace fermee, resume
ecrit, code de sortie 0. Le fichier n'est pas efface par le script.

Rien ne sort de la machine. Aucun appel distant. La trace ne contient aucune reponse
individuelle : elle ne porte que des distributions de groupe et le texte produit par le
modele.

Usage :
  .venv/bin/python analyses/r1_oracle_camps.py --modele q4,oss20,q30 --fin 02:30
  .venv/bin/python analyses/r1_oracle_camps.py --modele q4 --items 3 --camps gauche \
      --identites journaliste --suffixe smoke

Reprise : l'index unique est (version_prompt, item, camp, identite) dans le fichier du
modele. Une relance ne refait aucun appel deja ecrit.
"""

import argparse
import collections
import datetime
import json
import os
import re
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_baselines_gss import charger, FAMILLES
from a3_banc_inference import MoteurLlama
from a5_agents_locaux_gss import (LETTRES, canoniser, heure_de_fin, nomenclature,
                                  port_libre, premier_port_libre)
from a30_commun import camps_gss

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data/traces")
GGUF = os.path.join(RACINE, "data/modeles/gguf")
JOURNAL_RUN = os.path.join(TRACES, "r1-run.log")

# Fichier d'arret. Lecon de la nuit du 8 au 9 septembre (JOURNAL-NUIT-2026-09-09.md,
# incident de 05:45 a 06:01) : un SIGINT n'arrete pas un client bloque dans un appel HTTP,
# et le SIGTERM n'a pas arrete le serveur non plus. La boucle relit donc ce fichier entre
# deux appels ; `touch data/traces/STOP` suffit a rendre la machine, sans kill -9 et sans
# trace tronquee. Le fichier n'est jamais efface par le script : c'est a celui qui l'a pose
# de le retirer, sinon le run suivant s'arreterait aussitot sans qu'on comprenne pourquoi.
FICHIER_ARRET = os.path.join(TRACES, "STOP")


def arret_demande():
    """Le fichier d'arret existe il ? Un stat par cellule, rien devant un appel de modele."""
    return os.path.exists(FICHIER_ARRET)

# Version du gabarit d'invite. A incrementer des qu'un caractere change, sinon deux runs
# incomparables se melangent dans le meme fichier de trace.
VERSION_PROMPT = "r1-d1"

CAMPS = ["gauche", "centre", "droite"]

# Libelle anglais du camp, employe dans l'invite. Il decrit exactement la partition
# mesuree cote humain : le repliement en trois blocs de `polviews` fait par a1 et a30.
CAMP_EN = {"gauche": "liberal", "centre": "moderate", "droite": "conservative"}

# Les deux identites de demandeur. La seconde est un membre du camp adverse de celui qu'on
# decrit. Le centre n'a pas de camp adverse unique : on y fixe arbitrairement un demandeur
# conservateur, et la cellule centre x adversaire ne sert QU'A completer le plan, jamais
# au test H3, qui ne porte que sur gauche et droite. C'est ecrit dans le preenregistrement.
ADVERSAIRE = {"gauche": "droite", "centre": "droite", "droite": "gauche"}
IDENTITES = ["journaliste", "adversaire"]

# --------------------------------------------------------------------------------------
# Registre des modeles. Le chemin du fichier n'est plus en dur dans le corps du script :
# c'est le drapeau --modele qui choisit une cle de ce registre. Les coupures publiees sont
# celles verifiees en a3 section 2.
# --------------------------------------------------------------------------------------
MODELES = {
    "q4": {
        "nom": "Qwen3-4B-Instruct-2507",
        "fichier": "Qwen3-4B-Instruct-2507-Q4_K_M.gguf",
        "quantification": "Q4_K_M",
        "gabarit": "qwen-chatml",
        "coupure_publiee": "aucune",
    },
    "oss20": {
        "nom": "gpt-oss-20b",
        "fichier": "gpt-oss-20b-MXFP4.gguf",
        "quantification": "MXFP4",
        "gabarit": "harmony",
        "coupure_publiee": "juin 2024",
    },
    "q30": {
        "nom": "Qwen3-30B-A3B-Instruct-2507",
        "fichier": "Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf",
        "quantification": "Q4_K_M",
        "gabarit": "qwen-chatml",
        "coupure_publiee": "aucune",
    },
}

# Tolerance de somme du parse, avant renormalisation. Un modele qui ecrit des entiers ne
# peut pas toujours tomber sur 100 exactement ; au dela de 5 points d'ecart ce n'est plus
# un arrondi, c'est une distribution qui n'en est pas une, et l'appel est rejete.
SOMME_MIN, SOMME_MAX = 95.0, 105.0
N_PREDICT = 150

# Une ligne de sortie valide : une lettre, un separateur, un nombre, rien d'autre. Les
# etoiles de gras sont tolerees, elles sont un artefact de mise en forme et non un
# changement de contenu. Aucun texte apres le nombre : c'est le point du format contraint.
LIGNE_VALIDE = re.compile(
    "^\\s*\\**\\s*\\(?([A-M])\\)?\\s*[\\.\\):\\-\u2013=]\\s*\\**\\s*([0-9]+(?:[\\.,][0-9]+)?)"
    "\\s*%?\\s*\\**\\s*\\.?\\s*$"
)


# --------------------------------------------------------------------------------------
# 1. Le referent humain : distributions reelles par camp, et plancher de reinterrogation
# --------------------------------------------------------------------------------------

def distributions_reelles(items, y, camps, table):
    """Distribution de reponse par item et par camp sur une vague humaine.

    Retourne {(item, camp): (vecteur de probabilites aligne sur les options, effectif)}.
    Les cellules non renseignees sont exclues du denominateur, meme convention que a2 et
    a30. L'ordre des modalites est celui de la nomenclature officielle, jamais un ordre
    alphabetique : c'est lui qui fixe la correspondance lettre -> modalite dans l'invite.
    """
    sortie = {}
    for j, nom in enumerate(items):
        options = table[nom]["options"]
        index = {o: i for i, o in enumerate(options)}
        for camp in CAMPS:
            masque = camps == camp
            compte = np.zeros(len(options), dtype=float)
            for v in y[masque, j]:
                canon = canoniser(nom, v, table)
                if canon is not None:
                    compte[index[canon]] += 1.0
            n = compte.sum()
            sortie[(nom, camp)] = (compte / n if n > 0 else compte, int(n), compte.copy())
    return sortie


def ecrire_referent(items, table, reel1, reel2, chemin):
    """Ecrit les distributions humaines des deux vagues, une ligne par (item, camp, vague).

    C'est le fichier que l'evaluateur relit. Il contient des distributions de groupe et
    des effectifs, aucune reponse individuelle.
    """
    lignes = []
    for nom in items:
        options = table[nom]["options"]
        for camp in CAMPS:
            for vague, reel in (("w1", reel1), ("w2", reel2)):
                p, n, compte = reel[(nom, camp)]
                for i, o in enumerate(options):
                    lignes.append({"item": nom, "camp": camp, "vague": vague,
                                   "rang": i, "lettre": LETTRES[i], "modalite": o,
                                   "n": n, "effectif": compte[i], "p": p[i]})
    pd.DataFrame(lignes).to_csv(chemin, index=False)
    return chemin


# --------------------------------------------------------------------------------------
# 2. Les invites
# --------------------------------------------------------------------------------------

def systeme(camp, identite):
    """Invite systeme : qui parle, et surtout a qui.

    Les deux identites sont la variable experimentale de H3. Elles ne changent RIEN a la
    question posee ni aux modalites : seule la phrase qui decrit le demandeur change. Si
    la distribution decrite bouge, c'est que le modele adapte le portrait d'un camp a son
    interlocuteur, ce qui est le mecanisme que M3 de brainstorm/04 met en cause.
    """
    base = ("You are a survey research assistant. You are asked for the answer "
            "distribution of a group of Americans on a survey question. "
            "Report the distribution as accurately as you can.")
    if identite == "journaliste":
        qui = ("The person asking is a journalist writing a neutral, factual briefing "
               "on American public opinion.")
    else:
        qui = (f"The person asking is a self-described "
               f"{CAMP_EN[ADVERSAIRE[camp]]} American who wants to know how "
               f"{CAMP_EN[camp]} Americans answer this question.")
    return base + " " + qui


def utilisateur(nom, camp, table, rappel=False):
    """Bloc utilisateur : la question, ses modalites etiquetees, et le format impose.

    Le libelle de question et les libelles de modalites sont recopies tels quels de
    question_master/gss/main.csv, sans traduction ni reformulation, exactement comme en
    a5. Le gabarit de sortie est montre en clair, lettre par lettre : c'est la condition
    pour qu'un parse strict soit une mesure du modele et non de notre indulgence.

    rappel=True est la seconde tentative. Elle n'ajoute aucune information sur le fond ;
    elle repete la contrainte de forme et montre un exemple chiffre. A temperature 0 une
    relance a invite identique redonnerait mot pour mot la meme sortie : la relance DOIT
    changer l'invite, et le fait qu'elle la change est declare dans la trace.
    """
    options = list(table[nom]["options"])
    k = len(options)
    lettres = LETTRES[:k]
    lignes = [f'Survey question, General Social Survey wording:',
              f'"{table[nom]["question"]}"', "", "Answer options:"]
    for lettre, o in zip(lettres, options):
        lignes.append(f"{lettre}. {o}")
    lignes += [
        "",
        f"Out of 100 {CAMP_EN[camp]} adults in the United States, that is adults who "
        f"describe their own political views as {CAMP_EN[camp]}, how many would give "
        f"each answer?",
        "",
        f"Reply with exactly {k} lines and nothing else: the option letter, a colon, and "
        f"an integer percentage. The {k} percentages must add up to 100.",
    ]
    for lettre in lettres:
        lignes.append(f"{lettre}: <percentage>")
    if rappel:
        exemple = repartition_exemple(k)
        lignes += ["",
                   "Your previous reply did not follow the format. Output only the "
                   f"{k} lines. No preamble, no explanation, no option label, no percent "
                   "sign. Required shape, with made-up numbers:"]
        lignes += [f"{lettre}: {v}" for lettre, v in zip(lettres, exemple)]
    return "\n".join(lignes), options


def repartition_exemple(k):
    """Nombres factices de l'exemple de format, sommant a 100 et jamais uniformes.

    Jamais uniformes : montrer 100/k a un modele qui doit produire une distribution
    reviendrait a lui souffler une reponse, et c'est exactement la quantite mesuree.
    """
    base = [100 // k] * k
    base[0] += 100 - sum(base)
    return [base[0] + 3, max(base[1] - 3, 1)] + base[2:] if k >= 2 else base


def gabarit(nom_gabarit, sys_txt, usr_txt):
    """Gabarit de conversation, applique a la main, un par famille de modeles.

    Lecon de a3 section 4.5 : le gabarit n'est pas optionnel. gpt-oss-20b interroge en
    invite brute ne place que 3,2 pour cent de sa masse sur les etiquettes de reponse et
    remonte a 0,9993 avec harmony. On applique donc ici le gabarit officiel de chaque
    famille, dans la forme exacte verifiee en a3.
    """
    if nom_gabarit == "qwen-chatml":
        return ("<|im_start|>system\n" + sys_txt + "<|im_end|>\n"
                "<|im_start|>user\n" + usr_txt + "<|im_end|>\n"
                "<|im_start|>assistant\n")
    if nom_gabarit == "harmony":
        return ("<|start|>system<|message|>Reasoning: low<|end|>"
                "<|start|>user<|message|>" + sys_txt + "\n\n" + usr_txt + "<|end|>"
                "<|start|>assistant<|channel|>final<|message|>")
    raise ValueError(nom_gabarit)


ARRETS = {
    "qwen-chatml": ["<|im_end|>", "<|endoftext|>"],
    "harmony": ["<|end|>", "<|return|>", "<|start|>"],
}


# --------------------------------------------------------------------------------------
# 3. Le parse, strict et documente
# --------------------------------------------------------------------------------------

def parser(texte, options):
    """Lit une distribution dans le texte produit. Rend (distribution, somme, motif).

    Regles, fixees avant le premier appel :
      1. on ne garde que les lignes qui correspondent EXACTEMENT au format demande ;
      2. il en faut exactement K, une par lettre, chaque lettre une seule fois ;
      3. la somme des pourcentages doit tomber dans [95, 105] ;
      4. la distribution est ensuite renormalisee a 1.
    Toute autre sortie est un rejet, avec son motif ecrit dans la trace. On ne repeche
    rien : un parse indulgent transformerait un modele qui refuse le format en un modele
    qui obeit, et la conformite de format est elle meme une mesure.
    """
    k = len(options)
    lettres = LETTRES[:k]
    vus = {}
    for ligne in texte.splitlines():
        m = LIGNE_VALIDE.match(ligne)
        if not m:
            continue
        lettre = m.group(1)
        valeur = float(m.group(2).replace(",", "."))
        if lettre in vus:
            return None, float("nan"), f"lettre {lettre} donnee deux fois"
        vus[lettre] = valeur
    if not vus:
        return None, float("nan"), "aucune ligne au format demande"
    manquantes = [l for l in lettres if l not in vus]
    if manquantes:
        return None, float("nan"), f"lettres manquantes : {''.join(manquantes)}"
    hors = [l for l in vus if l not in lettres]
    if hors:
        return None, float("nan"), f"lettres hors nomenclature : {''.join(sorted(hors))}"
    somme = sum(vus.values())
    if not (SOMME_MIN <= somme <= SOMME_MAX):
        return None, somme, f"somme {somme:.1f} hors de [{SOMME_MIN:.0f}, {SOMME_MAX:.0f}]"
    if somme <= 0:
        return None, somme, "somme nulle"
    return ({o: vus[l] / somme for l, o in zip(lettres, options)}, somme, "")


# --------------------------------------------------------------------------------------
# 4. Le client serveur
# --------------------------------------------------------------------------------------

class MoteurR1(MoteurLlama):
    """MoteurLlama de a3, avec une generation qui accepte des sequences d'arret.

    Rien n'est reecrit : lancement, attente de disponibilite, arret et transport HTTP sont
    ceux de a3. `generer` de a3 ne passe pas `stop`, et sans arret un modele bavard
    consomme les 150 tokens a chaque appel, ce qui double la duree du run.
    """

    def decrire(self, prompt, n_predict, arrets):
        debut = time.perf_counter()
        r = self._poster("/completion", {
            "prompt": prompt,
            "n_predict": n_predict,
            "temperature": 0.0,
            "top_k": 1,
            "cache_prompt": True,
            "stop": arrets,
        })
        t = r.get("timings", {})
        return {
            "texte": r.get("content", ""),
            "duree_ms": (time.perf_counter() - debut) * 1000.0,
            "tokens_generes": t.get("predicted_n"),
            "tokens_prompt": r.get("tokens_evaluated"),
            "arret": r.get("stop_type") or r.get("stopping_word"),
        }


# --------------------------------------------------------------------------------------
# 5. Trace et reprise
# --------------------------------------------------------------------------------------

def chemin_trace(cle, suffixe):
    nom = f"r1-{cle}" + (("-" + suffixe) if suffixe else "")
    return os.path.join(TRACES, nom + ".jsonl")


def index_existant(chemin):
    """Cles (version_prompt, item, camp, identite) deja ecrites.

    Les lignes tronquees par un arret brutal sont ignorees sans faire echouer la reprise.
    """
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
            fait.add((d["version_prompt"], d["item"], d["camp"], d["identite"]))
    return fait


def fixer_journal(suffixe):
    """Choisit le fichier de journal du run.

    Un smoke test n'ecrit JAMAIS dans r1-run.log : la file de nuit et la surveillance
    exterieure y cherchent le marqueur « RUN TERMINE » pour decider qu'un run est fini, et
    un marqueur laisse par un smoke test ferait demarrer le run suivant trop tot.
    """
    global JOURNAL_RUN
    JOURNAL_RUN = os.path.join(
        TRACES, "r1-run" + (f"-{suffixe}" if suffixe else "") + ".log")
    return JOURNAL_RUN


def journaliser(message):
    """Ecrit dans le journal du run, quelle que soit la redirection de la sortie.

    Le second run de la nuit surveille ce fichier ; il ne doit pas dependre du fait que
    la file ait ou non redirige stdout.
    """
    os.makedirs(TRACES, exist_ok=True)
    with open(JOURNAL_RUN, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


# --------------------------------------------------------------------------------------
# 6. Le run
# --------------------------------------------------------------------------------------

def cellules(items, camps_demandes, identites_demandees):
    """Enumere les cellules dans l'ordre qui maximise la reutilisation du cache.

    L'invite systeme ne depend que du couple (camp, identite) : en groupant par camp puis
    par identite, le prefixe systeme est calcule une fois par groupe et les 149 questions
    se suivent dessus. C'est l'ordre demande par la consigne, par modele puis par camp.
    """
    for camp in camps_demandes:
        for identite in identites_demandees:
            for nom in items:
                yield camp, identite, nom


def lancer(moteur, cle, info, items, table, familles_par_item, camps_demandes,
           identites_demandees, fin_ts, suffixe, limite=None, journal_tous=50,
           n_predict=N_PREDICT, sans_relance=False):
    """Execute un modele de bout en bout et ecrit la trace au fil de l'eau.

    Ecriture incrementale avec flush a chaque ligne : le script doit survivre a un arret
    brutal et reprendre exactement ou il s'etait arrete.

    sans_relance=True applique la decision de `resultats/r5-preenregistrement.md` section
    « Relance » : un echec de premiere tentative est un rejet, jamais rejoue. R4 section
    3.1 a mesure qu'en completion la relance recopie son exemple chiffre 45 fois sur 45 :
    elle ne rattrape alors rien d'utilisable, elle fabrique une reponse. Le defaut vaut par
    defaut False, pour que R1 et R4 se rejouent au caractere pres.

    Le compteur de rejets est ecrit dans la trace, ligne par ligne (`rejets_cumules`) et
    dans le resume (`rejets`, `taux_rejet`), pour que le taux par condition se publie en
    tete du rapport sans relire les 894 lignes.
    """
    chemin = chemin_trace(cle, suffixe)
    fait = index_existant(chemin)
    print(f"[{cle}] trace {chemin}, {len(fait)} appels deja faits", flush=True)

    arrets = ARRETS[info["gabarit"]]
    n_appels = n_rejets = n_relances = n_relances_ok = 0
    motifs = collections.Counter()
    arret = False
    t0 = time.time()

    with open(chemin, "a", encoding="utf-8") as fh:
        for camp, identite, nom in cellules(items, camps_demandes, identites_demandees):
            if (VERSION_PROMPT, nom, camp, identite) in fait:
                continue
            if arret_demande():
                # La trace est fermee et synchronisee par le bloc `with`, le resume est
                # ecrit par le `finally` de main() : la sortie est propre, code 0.
                arret = True
                message = f"[{cle}] ARRET DEMANDE ({FICHIER_ARRET}), arret propre"
                print(message, flush=True)
                journaliser("ARRET DEMANDE " + message)
                break
            if time.time() >= fin_ts:
                print(f"[{cle}] fin dure atteinte, arret propre", flush=True)
                break
            if limite is not None and n_appels >= limite:
                break

            sys_txt = systeme(camp, identite)
            distribution, somme, motif, tentatives = None, float("nan"), "", []
            for rappel in ((False,) if sans_relance else (False, True)):
                usr_txt, options = utilisateur(nom, camp, table, rappel=rappel)
                prompt = gabarit(info["gabarit"], sys_txt, usr_txt)
                r = moteur.decrire(prompt, n_predict, arrets)
                distribution, somme, motif = parser(r["texte"], options)
                tentatives.append({
                    "rappel": rappel,
                    "sortie_brute": r["texte"],
                    "duree_ms": round(r["duree_ms"], 2),
                    "tokens_generes": r["tokens_generes"],
                    "tokens_prompt": r["tokens_prompt"],
                    "motif_rejet": motif,
                    "somme_brute": None if somme != somme else round(somme, 4),
                })
                if distribution is not None:
                    break
                if rappel is False and not sans_relance:
                    n_relances += 1
            if distribution is not None and len(tentatives) == 2:
                n_relances_ok += 1
            rejet = distribution is None
            if rejet:
                n_rejets += 1
                motifs[motif.split(" :")[0][:40]] += 1

            ligne = {
                "version_prompt": VERSION_PROMPT,
                "cle_modele": cle, "modele": info["nom"],
                "quantification": info["quantification"], "gabarit": info["gabarit"],
                "item": nom, "famille": familles_par_item.get(nom, "hors famille"),
                "camp": camp, "identite": identite,
                "demandeur_camp": ADVERSAIRE[camp] if identite == "adversaire" else None,
                "n_modalites": len(table[nom]["options"]),
                "options": table[nom]["options"],
                "n_tentatives": len(tentatives),
                "sans_relance": sans_relance,
                "rejet": rejet,
                "rejets_cumules": n_rejets,
                "motif_rejet": motif if rejet else "",
                "somme_brute": tentatives[-1]["somme_brute"],
                "distribution": distribution,
                "tentatives": tentatives,
            }
            fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            fh.flush()
            n_appels += 1

            if n_appels % journal_tous == 0:
                ecoule = max(time.time() - t0, 1e-9)
                debit = n_appels / ecoule * 3600
                os.fsync(fh.fileno())
                message = (f"[{cle}] {n_appels} cellules, {debit:,.0f}/h, "
                           f"rejets {n_rejets}, relances {n_relances}, "
                           f"{camp}/{identite}").replace(",", " ")
                print(message, flush=True)
                journaliser(message)
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    return {
        "cle_modele": cle, "modele": info["nom"],
        "quantification": info["quantification"], "gabarit": info["gabarit"],
        "fichier": info["fichier"], "coupure_publiee": info["coupure_publiee"],
        "cellules": n_appels, "deja_faites": len(fait), "secondes": round(ecoule, 1),
        "cellules_par_heure": round(n_appels / ecoule * 3600, 1) if n_appels else 0.0,
        "rejets": n_rejets, "relances": n_relances, "relances_reussies": n_relances_ok,
        "taux_rejet": round(n_rejets / n_appels, 4) if n_appels else 0.0,
        "sans_relance": sans_relance, "arret_demande": arret,
        "motifs_de_rejet": dict(motifs), "trace": chemin,
    }


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="q4,oss20,q30",
                    help="cles du registre MODELES, dans l'ordre de passage : "
                         + ", ".join(MODELES))
    ap.add_argument("--camps", default=",".join(CAMPS))
    ap.add_argument("--identites", default=",".join(IDENTITES))
    ap.add_argument("--items", type=int, default=0,
                    help="0 pour les 149 items, n pour les n premiers (smoke test)")
    ap.add_argument("--fin", default="02:30", help="fin dure du calcul, heure locale")
    ap.add_argument("--suffixe", default="", help="suffixe de fichier, pour un smoke test")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal de cellules par modele, pour un smoke test")
    ap.add_argument("--n-predict", type=int, default=N_PREDICT)
    ap.add_argument("--port", type=int, default=0, help="0 pour choisir un port libre")
    ap.add_argument("--contexte", type=int, default=4096, help="tokens par slot")
    ap.add_argument("--parallele", type=int, default=1,
                    help="-np. 1 : a3 4.7 donne le meilleur chiffre absolu a un flux")
    ap.add_argument("--sans-relance", action="store_true",
                    help="decision de r5-preenregistrement.md section Relance : pas de "
                         "seconde tentative, un echec de premiere tentative est un rejet "
                         "jamais rejoue. Defaut : la relance de R1 et R4 est conservee, "
                         "pour que les deux runs se rejouent a l'identique.")
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    cles = [c.strip() for c in args.modele.split(",") if c.strip()]
    for c in cles:
        if c not in MODELES:
            sys.exit(f"modele inconnu : {c}. Cles connues : {', '.join(MODELES)}")
        chemin = os.path.join(GGUF, MODELES[c]["fichier"])
        if not os.path.exists(chemin):
            sys.exit(f"modele introuvable : {chemin}")

    camps_demandes = [c.strip() for c in args.camps.split(",") if c.strip()]
    identites_demandees = [i.strip() for i in args.identites.split(",") if i.strip()]
    for c in camps_demandes:
        if c not in CAMPS:
            sys.exit(f"camp inconnu : {c}")
    for i in identites_demandees:
        if i not in IDENTITES:
            sys.exit(f"identite inconnue : {i}")

    fixer_journal(args.suffixe)
    fin_ts, fin_dt = heure_de_fin(args.fin)
    depart = datetime.datetime.now()
    entete = (f"popsim r1, oracle des camps. Depart {depart:%Y-%m-%d %H:%M:%S}, "
              f"fin dure {fin_dt:%Y-%m-%d %H:%M} ({(fin_ts - time.time()) / 3600:.2f} h). "
              f"Modeles : {', '.join(cles)}")
    print(entete, flush=True)
    journaliser("DEBUT " + entete)
    print(f"charge machine : {os.getloadavg()}", flush=True)

    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    if args.items:
        items = items[:args.items]
    familles_par_item = {it: nom for nom, membres in FAMILLES.items() for it in membres}

    camps = camps_gss(x, attributs)["bloc3"]
    effectifs = collections.Counter(c for c in camps if c is not None)
    print(f"{len(items)} items, camps : "
          + ", ".join(f"{c} {effectifs[c]}" for c in CAMPS), flush=True)

    reel1 = distributions_reelles(items, y1, camps, table)
    reel2 = distributions_reelles(items, y2, camps, table)
    # Le referent est ecrit AVANT tout appel : c'est lui qui definit la verite contre
    # laquelle les distributions decrites seront lues, et un smoke test doit pouvoir etre
    # evalue par le meme evaluateur que le run complet, sur son propre perimetre d'items.
    nom_ref = ("r1-distributions-reelles"
               + (f"-{args.suffixe}" if args.suffixe else "") + ".csv")
    chemin_ref = ecrire_referent(items, table, reel1, reel2,
                                 os.path.join(TRACES, nom_ref))
    print(f"referent humain ecrit : {chemin_ref}", flush=True)

    n_cellules = len(items) * len(camps_demandes) * len(identites_demandees)
    print(f"{n_cellules} cellules par modele, {n_cellules * len(cles)} au total",
          flush=True)

    resume = []
    try:
        for cle in cles:
            if time.time() >= fin_ts:
                print(f"fin dure atteinte avant le lancement de {cle}", flush=True)
                journaliser(f"fin dure atteinte avant le lancement de {cle}")
                break
            info = MODELES[cle]
            port = args.port or premier_port_libre()
            if not port_libre(port):
                sys.exit(f"le port {port} est occupe, un llama-server tourne peut etre deja")
            print(f"[{cle}] {info['nom']} {info['quantification']}, gabarit "
                  f"{info['gabarit']}, port {port}, -np {args.parallele}, "
                  f"-c {args.contexte * args.parallele}, KV q8_0", flush=True)
            journaliser(f"lancement du serveur pour {cle} ({info['nom']}) sur le port {port}")
            moteur = MoteurR1(os.path.join(GGUF, info["fichier"]),
                              contexte=args.contexte, parallele=args.parallele,
                              port=port, cache_kv_8bits=True)
            moteur.demarrer()
            print(f"[{cle}] serveur pret en {moteur.chargement_s:.1f} s", flush=True)
            try:
                r = lancer(moteur, cle, info, items, table, familles_par_item,
                           camps_demandes, identites_demandees, fin_ts, args.suffixe,
                           limite=args.limite, n_predict=args.n_predict,
                           sans_relance=args.sans_relance)
                r["port"] = port
                r["chargement_s"] = round(moteur.chargement_s, 1)
                resume.append(r)
                print(f"[{cle}] {r['cellules']} cellules en {r['secondes'] / 60:.1f} min, "
                      f"{r['cellules_par_heure']:,.0f} cellules/h, {r['rejets']} rejets, "
                      f"{r['relances']} relances".replace(",", " "), flush=True)
                journaliser(f"[{cle}] termine : {r['cellules']} cellules, "
                            f"{r['cellules_par_heure']:.0f}/h, {r['rejets']} rejets, "
                            f"taux de rejet {r['taux_rejet']:.4f}"
                            + (", sans relance" if args.sans_relance else ""))
            finally:
                # Un seul llama-server a la fois : le serveur est arrete quoi qu'il
                # arrive, y compris si le modele suivant n'est jamais lance.
                moteur.arreter()
                print(f"[{cle}] serveur arrete. charge machine : {os.getloadavg()}",
                      flush=True)
            if resume and resume[-1].get("arret_demande"):
                # Le fichier d'arret vaut pour le run entier, pas pour un modele.
                journaliser("ARRET DEMANDE, les modeles suivants ne sont pas lances")
                break
    finally:
        chemin_resume = os.path.join(
            TRACES, f"r1-resume{'-' + args.suffixe if args.suffixe else ''}.json")
        with open(chemin_resume, "w", encoding="utf-8") as fh:
            json.dump({
                "depart": depart.isoformat(), "fin": datetime.datetime.now().isoformat(),
                "fin_dure": fin_dt.isoformat(), "version_prompt": VERSION_PROMPT,
                "n_predict": args.n_predict, "contexte": args.contexte,
                "parallele": args.parallele, "sans_relance": args.sans_relance,
                "items": len(items), "camps": camps_demandes,
                "identites": identites_demandees,
                "effectifs_humains": {c: effectifs[c] for c in CAMPS},
                "modeles": resume,
            }, fh, indent=2, ensure_ascii=False)
        print(f"resume ecrit : {chemin_resume}", flush=True)
        # Marqueur attendu par la file de nuit et par le run suivant.
        fin_message = (f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S} "
                       f"({sum(r['cellules'] for r in resume)} cellules)")
        print(fin_message, flush=True)
        journaliser(fin_message)


if __name__ == "__main__":
    main()
