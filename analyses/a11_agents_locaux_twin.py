"""
a11_agents_locaux_twin : nos agents locaux sur Twin-2K-500, second run de la nuit.

Statut : script d'experience, pas du code de production. C'est le pendant Twin-2K-500 de
analyses/a5_agents_locaux_gss.py. Il se met en file DERRIERE le run a5 : il attend la fin
du processus a5 avant de lancer son propre llama-server, parce que la machine ne peut
porter qu'un seul serveur a la fois.

Ce qu'il fait. Pour chaque couple (personne, item de la vague 4), il construit un prompt,
applique le gabarit de conversation Qwen, envoie un seul passage avant a llama-server et
lit la distribution de probabilite du token de reponse. Aucune generation de texte.

Alignement sur a5, volontaire et total. Le client serveur (MoteurA5), le gabarit de
conversation (gabarit_qwen), le scoring par etiquettes courtes d'un token, la verification
des identifiants de tokens distincts, le seuil de rejet sur la masse des lettres, la
consigne, le preambule, la graine d'echantillonnage et le format de ligne de trace sont
IMPORTES de a5, pas recopies. L'evaluateur du matin lit les deux traces avec le meme code.

Conditions :
  C3-Twin  persona texte complet des vagues 1 a 3, colonne wave1_3_persona_text du fichier
           wave_persona_chunk_001.parquet. C'est l'analogue exact de la configuration
           default_gpt41mini des auteurs : meme information, meme personnes, meme cible.
           La comparaison est donc a modele egal d'information, notre Qwen3-4B local
           contre leur GPT-4.1-mini.
  C2-Twin  les 14 questions du bloc Demographics seules, rendues dans le format exact du
           persona texte. Analogue de demo_only_gpt41mini.

Decoupage repris EXACTEMENT de analyses/a2_baselines_twin.py, graine 20260903 : le
decoupage entree / evaluation est temporel et fourni par les auteurs, le contexte est la
vague 1 a 3 et la cible les 108 colonnes categorielles de la vague 4. Les 5 plis de
personnes de a2 servent uniquement a stratifier le sous echantillon, pour que l'evaluation
des baselines B1 et B2 se fasse a taille d'entrainement constante.

Verification faite avant le run : le persona des vagues 1 a 3 ne contient aucun libelle de
question de la vague 4. Verifie sur 40 personas et 71 libelles cibles distincts, zero
occurrence. C'est la meme verification que a2 section 2.2, refaite sur notre echantillon.

Scoring : traitement (a) de a3 section 3.4, importe de a5. Etiquettes courtes d'un token,
lues a une seule position, meme contexte gauche pour toutes les modalites. Identifiants de
tokens verifies distincts en encodant `prompt` puis `prompt + " A"`. La masse portee par
les K lettres avant renormalisation est tracee a chaque appel, seuil de rejet 0,5.

Entree  : data/twin2k500, non versionne.
Sortie  : data/traces/a11-<condition>-p<passe>.jsonl, une ligne par appel.
          data/traces/a11-personnes.csv, le sous echantillon retenu.
          data/traces/a11-personas-tokens.csv, longueur en tokens de chaque persona.
          data/traces/a11-run.log et a11-run.pid si lance par nohup.

Rien ne sort de la machine. La trace ne contient PAS la vraie reponse de la personne :
l'evaluation la relit dans data/, conformement a la position par defaut de METHODOLOGIE.

Usage :
  # smoke test, serveur dedie sur un port distinct, arrete tout de suite apres
  .venv/bin/python analyses/a11_agents_locaux_twin.py --personnes 3 --limite 25 \\
      --suffixe smoke --port 8199 --parallele 1

  # run complet de la nuit, en file derriere a5
  nohup .venv/bin/python analyses/a11_agents_locaux_twin.py --attendre-a5 \\
      > data/traces/a11-run.log 2>&1 &

Reprise : l'index unique est (condition, passe, pid, item). Une relance ne refait aucun
appel deja ecrit dans la trace.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Decoupage, cible, demographies et plis : exactement ceux de a2 sur Twin-2K-500.
from a2_baselines_twin import charger as charger_twin
from a2_baselines_twin import plis_personnes
from a2_baselines_twin import GRAINE as GRAINE_DECOUPAGE
from a2_baselines_twin import N_PLIS
from a2_commun import est_manquant

# Client serveur, gabarit, scoring, seuils, consignes, reprise : ceux de a5, importes et
# non recopies. Toute divergence de comportement entre les deux runs serait un artefact.
from a5_agents_locaux_gss import (CONSIGNE, GRAINE_ECHANTILLON, LETTRES, MODELE,
                                  MODELE_NOM, PREAMBULE, QUANTIFICATION, SEUIL_MASSE,
                                  MoteurA5, gabarit_qwen, heure_de_fin, index_existant,
                                  masse_des_lettres, port_libre, premier_port_libre)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data/traces")
PARQUET = os.path.join(RACINE, "data/twin2k500/wave_persona_chunk_001.parquet")

# Version du prompt, ecrite dans chaque ligne de trace. A incrementer des qu'un caractere
# du gabarit change, sinon deux runs incomparables se melangent dans le meme fichier.
VERSION_PROMPT = "a11-p1"

JEU = "twin2k500"

# Phrase d'introduction du persona. Reprise mot pour mot de systeme_c3 de a5, pour que la
# seule difference entre les deux jeux soit le corps du persona.
INTRO_C3 = "Here is how this person answered other questions of the same survey.\n\n"
INTRO_C2 = "Here is what is known about this person.\n\n"

# Les trois conditions, dans l'ordre ou elles doivent tourner.
CONDITIONS = ("C3b-Twin", "C2-Twin", "C3-Twin")

# Budget de tokens du persona tronque de C3b-Twin. Choisi sur la mesure du smoke test et
# non au jugement : le prefill du persona complet coute 348,8 s pour 27 638 tokens, celui
# des 10 240 premiers tokens 48,9 s, celui des 8 192 premiers 34,7 s, sur la meme machine
# et dans les memes conditions. Le cout n'est pas proportionnel a la longueur, il croit
# comme son carre, ce qui rend une troncature a 8 000 tokens dix fois moins chere qu'un
# persona complet et non trois fois moins chere. A 8 000 tokens on garde 42 des 173
# questions du persona median : le bloc Demographics en entier, le premier bloc de
# personnalite, et le debut des tests cognitifs.
BUDGET_C3B = 8000

# Minutes reservees a chaque condition qui suit celle en cours. C3-Twin est la derniere et
# prend ce qui reste ; C2-Twin est peu chere, environ 1 100 tokens de prefixe par personne.
RESERVE_PAR_CONDITION = {"C3b-Twin": 0, "C2-Twin": 40, "C3-Twin": 0}

# Marge de tokens reservee, dans le contexte du serveur, a tout ce qui n'est pas le
# persona : preambule, consigne, gabarit Qwen, libelle de la question et ses modalites,
# plus le token genere. Mesure hors ligne sur les 108 items : le bloc question va de 28 a
# 258 tokens, mediane 93, et le reste du gabarit pese environ 80 tokens. 1 500 laisse donc
# une marge de plus de cinq fois le pire cas.
MARGE_TOKENS = 1500

# Ordre de passage des blocs du catalogue a l'interieur d'une personne. Demande par le
# rapport a8, tache 4 : sur Twin, tout l'avantage de GPT-4.1-mini sur B2 vient des 40 items
# de preferences de prix, et il perd sur les blocs d'heuristiques et de biais. Le contraste
# entre ces deux familles est donc le premier resultat a securiser, y compris si le run est
# coupe par la fin dure. Le bloc des prix sert en outre de signal de contamination : si un
# modele local de 4 milliards de parametres y garde le meme avantage que GPT-4.1-mini, c'est
# que la connaissance des produits vient du pre entrainement et non du persona.
#
# Ce reordonnancement se fait A L'INTERIEUR d'une personne, jamais entre les personnes. La
# raison est chiffree : le prefixe de 27 500 tokens coute plusieurs minutes et n'est calcule
# qu'une fois par personne. Un ordre bloc majeur, qui passerait le bloc des prix sur les 150
# personnes avant de passer au bloc suivant, repaierait ce prefixe une fois par couple
# (personne, bloc), soit un facteur egal au nombre de passes sur la duree du run. Avec un
# ordre personne majeur, toute personne atteinte a ses 40 items de prix et ses 10 items
# d'heuristiques non experimentales avant tout le reste.
BLOCS_PRIORITAIRES = [
    "Product Preferences - Pricing",
    "Non-experimental heuristics and biases",
    "False consensus",
    "Probability matching vs. maximizing - Problem 1",
    "Probability matching vs. maximizing - Problem 2",
]

# Fichiers de suivi du run a5, dont ce script attend la fin avant de lancer son serveur.
PID_A5 = os.path.join(TRACES, "a5-run.pid")
LOG_A5 = os.path.join(TRACES, "a5-run.log")
MARQUEUR_A5 = "RUN TERMINE"


# --------------------------------------------------------------------------------------
# 1. Nomenclature des questions et des modalites, lue dans question_catalog.json
# --------------------------------------------------------------------------------------

def nomenclature(cibles, catalogue):
    """Libelle complet et ordre officiel des modalites pour chacun des 108 items cibles.

    Les questions de la vague 4 sont des experiences d'heuristiques et de biais : leur
    enonce EST l'experience. Le tronquer ou le resumer changerait la tache. Le libelle
    complet du catalogue est donc presente au modele tel quel, y compris les enonces de
    plusieurs centaines de mots des problemes d'Allais ou de la maladie asiatique.

    Deux formes d'item :
      - MC a reponse unique : les modalites sont Options, le code numerique du fichier de
        reponses est la position 1 fondee dans cette liste.
      - Matrix : une colonne de CSV par ligne de la matrice. Le libelle complet est
        l'enonce commun suivi de la ligne concernee, et les modalites sont Columns.
    L'ordre est celui du catalogue, jamais un ordre alphabetique ni l'ordre d'apparition
    dans les donnees : c'est lui qui fixe la correspondance lettre -> modalite -> code.
    """
    table = {}
    for col in cibles:
        q = catalogue[col]
        if q["QuestionType"] == "Matrix":
            rid = col.split("_", 1)[1] if "_" in col else None
            rangs = list(q.get("RowsID") or [])
            ligne = None
            if rid is not None and rid in rangs:
                ligne = q["Rows"][rangs.index(rid)]
            modalites = list(q["Columns"])
        else:
            ligne = None
            modalites = list(q["Options"])
        table[col] = {
            "question_id": q["QuestionID"],
            "question": (q.get("QuestionText") or "").strip(),
            "ligne": ligne,
            "modalites": modalites,
            "bloc": q["BlockName"].strip(),
            "type": q["QuestionType"],
        }
    return table


def utilisateur(col, table, inverse=False):
    """Bloc utilisateur : la question secrete et ses modalites etiquetees par des lettres.

    Retourne le texte, la liste ordonnee des modalites telles qu'elles sont presentees, et
    la liste des codes numeriques correspondants. Le code est la position dans l'ordre du
    catalogue, 1 fondee, c'est a dire exactement la valeur stockee dans wave4_response.csv.
    Il est transporte separement de l'ordre de presentation, pour que la passe 2, qui
    renverse les modalites, reste evaluable dans le meme repere.

    inverse=True renverse l'ordre de presentation. C'est la parade au biais de position de
    a3 section 3.4, meme convention que a5.
    """
    e = table[col]
    modalites = list(e["modalites"])
    codes = list(range(1, len(modalites) + 1))
    if inverse:
        modalites = modalites[::-1]
        codes = codes[::-1]
    lignes = [f"Question. {e['question']}"]
    if e["ligne"]:
        lignes.append(f"Item. {e['ligne']}")
    for i, m in enumerate(modalites):
        lignes.append(f"{LETTRES[i]}. {m}")
    return "\n".join(lignes), modalites, codes


# --------------------------------------------------------------------------------------
# 2. Les deux personas
# --------------------------------------------------------------------------------------

def rendre_demographies(persona_json):
    """Rend les 14 questions du bloc Demographics dans le format exact du persona texte.

    Le choix du format n'est pas neutre. Rendre les demographies sous une autre forme que
    celle du persona complet ferait varier deux choses a la fois entre C3-Twin et C2-Twin,
    la quantite d'information et sa mise en forme, et l'ecart mesure ne serait plus
    interpretable. On reprend donc mot pour mot le gabarit des auteurs :

        <enonce>
        Question Type: Single Choice
        Options:
          1 - <modalite>
          ...
        Answer: <code> - <modalite choisie>

    Verifie identique au prefixe demographique de wave1_3_persona_text, caractere pour
    caractere, sur l'ensemble des personnes retenues (voir verifier_rendu_demographies).
    """
    blocs = json.loads(persona_json)
    morceaux = []
    for b in blocs:
        if b.get("BlockName", "").strip() != "Demographics":
            continue
        for q in b.get("Questions", []):
            options = q.get("Options") or []
            rep = q.get("Answers") or {}
            pos, texte = rep.get("SelectedByPosition"), rep.get("SelectedText")
            lignes = [q["QuestionText"], "Question Type: Single Choice", "Options:"]
            lignes += [f"  {i + 1} - {o}" for i, o in enumerate(options)]
            lignes.append(f"Answer: {pos} - {texte}")
            morceaux.append("\n".join(lignes))
    return "\n\n".join(morceaux)


def tronquer_persona(texte, compter, budget=BUDGET_C3B):
    """Coupe le persona texte a un budget de tokens, sur une frontiere de question.

    La coupe se fait entre deux questions, jamais au milieu d'un enonce ni entre un enonce
    et sa reponse : un persona coupe en plein milieu d'une question apprendrait au modele
    une question sans reponse, ce qui n'est pas une information appauvrie mais une
    information fausse. Le texte des auteurs separe les questions par une ligne vide, ce
    qui donne la frontiere gratuitement.

    Un marqueur explicite est ajoute a la fin. Sans lui, le modele lit un questionnaire qui
    s'arrete sans raison et peut le prendre pour un abandon de la personne.

    Retourne le texte tronque, le nombre de questions gardees et le nombre total.
    """
    blocs = texte.split("\n\n")
    gardes, n = [], 0
    for b in blocs:
        k = compter(b + "\n\n")
        if n + k > budget:
            break
        gardes.append(b)
        n += k
    if len(gardes) == len(blocs):
        return texte, len(blocs), len(blocs)
    return ("\n\n".join(gardes)
            + "\n\n[Only the first part of this person's survey answers is shown here.]",
            len(gardes), len(blocs))


def verifier_rendu_demographies(texte_demo, persona_texte):
    """Le rendu des demographies est-il le prefixe exact du persona complet ?

    C'est la seule verification qui garantit que C2-Twin est bien C3-Twin ampute, et non
    une reformulation. En cas d'echec le run s'arrete : mieux vaut pas de chiffre qu'un
    chiffre dont l'ecart entre conditions vient de la mise en forme.
    """
    return persona_texte.startswith(texte_demo)


def systeme(condition, corps):
    """Prompt systeme, meme squelette que a5 : preambule, matiere, consigne.

    C'est ce bloc qui porte tout le poids de calcul en C3-Twin, environ 27 500 tokens. Il
    est identique pour les 108 questions de la meme personne, donc entierement servi par
    le cache de prefixe des le deuxieme appel, a condition que les appels se suivent. D'ou
    l'ordre d'enumeration de travaux() : personne par personne, jamais item par item.
    """
    intro = INTRO_C2 if condition == "C2-Twin" else INTRO_C3
    return PREAMBULE + "\n\n" + intro + corps + "\n\n" + CONSIGNE


# --------------------------------------------------------------------------------------
# 3. Sous echantillon de personnes
# --------------------------------------------------------------------------------------

def echantillon(pid, plis, disponibles, par_pli, graine=GRAINE_ECHANTILLON):
    """Tire un sous echantillon stratifie sur les 5 plis du decoupage de a2.

    Meme fonction que a5, a une restriction pres et elle doit etre dite : les personas
    texte des vagues 1 a 3 ne sont disponibles en local que pour les 294 personnes du
    fichier wave_persona_chunk_001.parquet, et non pour les 2 058 du jeu complet. Le
    tirage se fait donc parmi ces 294, qui se repartissent en 61, 56, 52, 62 et 63
    personnes sur les cinq plis. C'est un echantillon aleatoire d'un sous ensemble, ce qui
    est plus faible qu'un echantillon aleatoire du jeu complet, et le rapport le signale.

    Stratifier sur les plis n'est pas cosmetique : B1 et B2 sont evaluees pli par pli et
    entrainees sur les autres. Un echantillon desequilibre melangerait des tailles
    d'entrainement differentes selon la personne.
    """
    rng = np.random.default_rng(graine)
    par_pli_retenus = []
    for i_pli, (_, te) in enumerate(plis):
        candidats = np.array([k for k in te if pid[k] in disponibles])
        n = min(par_pli, len(candidats))
        par_pli_retenus.append([{"pid": int(pid[k]), "index": int(k), "pli": i_pli}
                                for k in sorted(rng.choice(candidats, size=n, replace=False))])
    # Ordre d'alternance entre les plis, et ce n'est pas cosmetique. Le run traite les
    # personnes dans l'ordre de cette liste et peut etre coupe par la fin dure : un ordre
    # pli par pli laisserait alors un echantillon entierement pris dans les deux premiers
    # plis, ce qui reduirait a deux le nombre de plis evalues pour B1 et B2. En alternant,
    # tout prefixe de la liste reste equilibre a une personne pres.
    retenus = []
    for rang in range(par_pli):
        for bloc in par_pli_retenus:
            if rang < len(bloc):
                retenus.append(bloc[rang])
    return retenus


def ordre_des_items(cibles, table):
    """Indices des items cibles, blocs prioritaires d'abord, ordre du catalogue ensuite.

    L'ordre est fixe, sans aleatoire : deux runs successifs interrogent les items dans la
    meme sequence, ce qui rend la reprise et la comparaison de deux nuits immediates.
    """
    rang = {b: i for i, b in enumerate(BLOCS_PRIORITAIRES)}
    indices = list(range(len(cibles)))
    return sorted(indices, key=lambda j: (rang.get(table[cibles[j]]["bloc"], len(rang)), j))


# --------------------------------------------------------------------------------------
# 4. Trace et reprise. Meme contrat que a5, index_existant est importe de la.
# --------------------------------------------------------------------------------------

def chemin_trace(condition, passe, suffixe):
    nom = f"a11-{condition}-p{passe}"
    if suffixe:
        nom += "-" + suffixe
    return os.path.join(TRACES, nom + ".jsonl")


# --------------------------------------------------------------------------------------
# 5. Le run
# --------------------------------------------------------------------------------------

def travaux(condition, retenus, cibles, masque, personas, ordre, items_max=None):
    """Enumere les appels a faire, dans l'ordre qui maximise le cache de prefixe.

    Personne par personne : le prompt systeme ne depend que de la personne, dans les deux
    conditions. Un seul calcul de prefixe par personne, puis les ~82 items s'enchainent
    sur le cache. Enumerer item par item couterait 108 prefixes de 27 500 tokens par
    personne au lieu d'un seul, soit un facteur cent sur la duree du run.

    Les cellules que la personne n'a pas vues ne sont pas interrogees. La vague 4 contient
    des experiences inter sujets, chaque personne ne voit qu'une condition, et 24,1 pour
    cent des cellules de la cible sont vides. a2 les exclut deja du numerateur et du
    denominateur ; les interroger ne changerait aucun chiffre et couterait un quart du run.
    """
    for p in retenus:
        corps = personas[p["pid"]][condition]
        sys_txt = systeme(condition, corps)
        n = 0
        for j in ordre:
            col = cibles[j]
            if not masque[p["index"], j]:
                continue
            if items_max is not None and n >= items_max:
                break
            n += 1
            yield p, col, sys_txt


def lancer(moteur, condition, passe, inverse, retenus, cibles, masque, personas, table,
           ordre, fin_dure, suffixe, limite=None, items_max=None, journal_tous=200):
    """Execute une condition de bout en bout et ecrit la trace au fil de l'eau.

    Ecriture incrementale avec flush a chaque ligne : le script doit survivre a un arret
    brutal et reprendre exactement ou il s'etait arrete.
    """
    chemin = chemin_trace(condition, passe, suffixe)
    fait = index_existant(chemin)
    a_faire = sum(1 for _ in travaux(condition, retenus, cibles, masque, personas, ordre,
                                     items_max))
    print(f"[{condition} passe {passe}] trace {chemin}, {a_faire} appels prevus, "
          f"{len(fait)} deja faits", flush=True)

    ids_lettres_par_k = {}
    n_appels, n_rejets, n_absents = 0, 0, 0
    t0 = time.time()

    with open(chemin, "a", encoding="utf-8") as fh:
        for p, col, sys_txt in travaux(condition, retenus, cibles, masque, personas, ordre,
                                       items_max):
            if (p["pid"], col) in fait:
                continue
            if time.time() >= fin_dure:
                print(f"[{condition} passe {passe}] fin dure atteinte, arret propre",
                      flush=True)
                break
            if limite is not None and n_appels >= limite:
                print(f"[{condition} passe {passe}] limite de {limite} appels atteinte",
                      flush=True)
                break

            bloc_user, modalites, codes = utilisateur(col, table, inverse=inverse)
            prompt = gabarit_qwen(sys_txt, bloc_user)
            k = len(modalites)
            lettres = LETTRES[:k]

            # Verification des identifiants de tokens : une fois par nombre de modalites,
            # sur le premier prompt rencontre. Le contexte gauche est le meme pour tous les
            # prompts, il se termine toujours par "Answer:".
            if k not in ids_lettres_par_k:
                ids_lettres_par_k[k], _ = moteur.tokens_des_lettres(prompt, k)
                print(f"  tokens verifies pour K={k} : {ids_lettres_par_k[k]}", flush=True)
            ids_lettres = ids_lettres_par_k[k]

            r = moteur.scorer(prompt)
            brut = masse_des_lettres(r["top"], ids_lettres, lettres)
            masse = sum(brut.values())
            absentes = [l for l, v in brut.items() if v == 0.0]
            if absentes:
                n_absents += 1
            rejet = masse < SEUIL_MASSE
            if rejet:
                n_rejets += 1

            if masse > 0:
                distribution = {modalites[i]: brut[l] / masse for i, l in enumerate(lettres)}
            else:
                distribution = {m: 1.0 / k for m in modalites}
            argmax = max(distribution, key=distribution.get)
            par_code = {str(codes[i]): distribution[m] for i, m in enumerate(modalites)}
            argmax_code = codes[modalites.index(argmax)]

            ligne = {
                "pid": p["pid"], "item": col, "condition": condition, "passe": passe,
                "pli": p["pli"], "bloc": 0,
                "jeu": JEU,
                "question_id": table[col]["question_id"],
                "bloc_catalogue": table[col]["bloc"],
                "version_prompt": VERSION_PROMPT.replace("p1", f"p{passe}"),
                "modele": MODELE_NOM, "quantification": QUANTIFICATION,
                "ordre_modalites": "inverse" if inverse else "nomenclature",
                "duree_ms": round(r["duree_ms"], 2),
                "masse_lettres": masse,
                "rejet": rejet,
                "modalites_absentes": absentes,
                "distribution": distribution,
                "argmax": argmax,
                "distribution_codes": par_code,
                "argmax_code": int(argmax_code),
                "tokens_prompt": r["tokens_prompt"],
                "tokens_calcules": r["tokens_calcules"],
                "prompt_ms": r["prompt_ms"],
            }
            fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            fh.flush()
            n_appels += 1

            if n_appels % journal_tous == 0:
                ecoule = time.time() - t0
                debit = n_appels / ecoule * 3600
                os.fsync(fh.fileno())
                reste = a_faire - len(fait) - n_appels
                print(f"  {condition} p{passe} : {n_appels} appels, {debit:,.0f}/h, "
                      f"rejets {n_rejets}, reste {reste}, "
                      f"{datetime.datetime.now():%H:%M:%S}".replace(",", " "), flush=True)
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    return {
        "condition": condition, "passe": passe, "appels": n_appels,
        "deja_faits": len(fait), "prevus": a_faire, "secondes": ecoule,
        "appels_par_heure": n_appels / ecoule * 3600 if n_appels else 0.0,
        "rejets": n_rejets, "appels_avec_modalite_absente": n_absents,
        "trace": chemin,
    }


# --------------------------------------------------------------------------------------
# 6. La file d'attente derriere a5
# --------------------------------------------------------------------------------------

def processus_vivant(pid):
    try:
        os.kill(pid, 0)
    except (OSError, ProcessLookupError):
        return False
    return True


def serveurs_llama():
    """Identifiants des llama-server en cours, quel que soit leur lanceur."""
    r = subprocess.run(["pgrep", "-f", "llama-server"], capture_output=True, text=True)
    return [int(x) for x in r.stdout.split() if x.strip().isdigit()]


def attendre_a5(delai_apparition_min=180, delai_marqueur_min=30, pause=30):
    """Attend que le run a5 soit fini avant de rendre la main.

    Trois etapes, dans cet ordre, parce qu'aucune des trois ne suffit seule :
      1. apparition de data/traces/a5-run.pid, puis extinction de ce processus ;
      2. apparition de la ligne "RUN TERMINE" dans data/traces/a5-run.log, qui est le
         marqueur imprime par a5 apres l'arret propre de son serveur ;
      3. disparition de tout processus llama-server, verifiee par pgrep.

    Si le fichier PID n'apparait jamais dans le delai, on ne force pas : on ne demarre que
    si aucun llama-server ne tourne. Deux serveurs sur cette machine, c'est 32 Gio de
    memoire unifiee partagee entre deux jeux de poids et deux caches KV, donc une mesure
    de debit fausse et un risque d'echec d'allocation.
    """
    t0 = time.time()
    pid = None
    print(f"file d'attente : surveillance de {PID_A5}", flush=True)
    while time.time() - t0 < delai_apparition_min * 60:
        if os.path.exists(PID_A5):
            try:
                pid = int(open(PID_A5).read().strip())
                break
            except ValueError:
                pass
        time.sleep(pause)

    if pid is None:
        print(f"a5-run.pid absent apres {delai_apparition_min} min", flush=True)
    else:
        print(f"a5 en cours, PID {pid}. Attente de sa fin.", flush=True)
        while processus_vivant(pid):
            time.sleep(pause)
        print(f"processus a5 {pid} termine a {datetime.datetime.now():%H:%M:%S}", flush=True)

        t1 = time.time()
        while time.time() - t1 < delai_marqueur_min * 60:
            if os.path.exists(LOG_A5):
                with open(LOG_A5, encoding="utf-8", errors="replace") as fh:
                    if MARQUEUR_A5 in fh.read():
                        print(f"marqueur '{MARQUEUR_A5}' vu dans a5-run.log", flush=True)
                        break
            time.sleep(pause)
        else:
            print(f"marqueur '{MARQUEUR_A5}' absent apres {delai_marqueur_min} min, "
                  "on continue sur la seule extinction du processus", flush=True)

    t2 = time.time()
    while time.time() - t2 < 10 * 60:
        restants = serveurs_llama()
        if not restants:
            print("aucun llama-server en cours, la machine est libre", flush=True)
            return True
        print(f"llama-server encore en cours : {restants}, attente", flush=True)
        time.sleep(pause)
    print("ATTENTION : un llama-server tourne toujours, run abandonne", flush=True)
    return False


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conditions", default=",".join(CONDITIONS),
                    help="liste ordonnee parmi C3b-Twin, C2-Twin et C3-Twin. L'ordre par "
                         "defaut n'est pas l'ordre de la question de recherche, c'est "
                         "l'ordre du risque : C3b-Twin, persona tronque a 8 000 tokens, "
                         "couvre les 150 personnes en moins de deux heures ; C2-Twin, les "
                         "demographies seules, en moins d'une heure ; C3-Twin, persona "
                         "complet de 27 500 tokens, prend ce qui reste. Mettre C3-Twin en "
                         "tete rendrait la nuit tout ou rien.")
    ap.add_argument("--budget-c3b", type=int, default=BUDGET_C3B,
                    help="budget de tokens du persona tronque de C3b-Twin")
    ap.add_argument("--passe", type=int, default=1, choices=(1, 2),
                    help="1 : modalites dans l'ordre du catalogue. "
                         "2 : ordre inverse, parade au biais de position (a3 3.4). "
                         "La passe 2 se lance separement, jamais dans la meme file.")
    ap.add_argument("--personnes", type=int, default=150,
                    help="taille du sous echantillon, reparti egalement sur les 5 plis")
    ap.add_argument("--fin", default="07:30", help="fin dure du calcul, heure locale")
    ap.add_argument("--reserve-min", type=int, default=35,
                    help="minutes reservees a la derniere condition. La condition "
                         "precedente s'arrete proprement a fin moins cette reserve, pour "
                         "qu'une nuit trop courte donne deux conditions sur moins de "
                         "personnes plutot qu'une seule condition complete. 35 minutes et "
                         "pas davantage : les deux conditions parcourent les personnes "
                         "dans le MEME ordre, donc les premieres minutes de C2-Twin "
                         "couvrent exactement les personnes que C3-Twin a eu le temps de "
                         "traiter. Ce qui deborde cette intersection n'ameliore pas la "
                         "comparaison, alors que le temps rendu a C3-Twin l'agrandit. "
                         "C2-Twin traite environ 10 000 appels a l'heure, soit 120 "
                         "personnes par heure, contre une vingtaine pour C3-Twin.")
    ap.add_argument("--suffixe", default="", help="suffixe de fichier, pour un smoke test")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal d'appels par condition, pour un smoke test")
    ap.add_argument("--items-max", type=int, default=None,
                    help="nombre maximal d'items interroges par personne. Sert au smoke "
                         "test : sans lui, une limite d'appels tomberait entierement sur "
                         "la premiere personne et ne mesurerait qu'un seul calcul de "
                         "prefixe, donc rien sur le cout reel du prefill.")
    ap.add_argument("--verifications-seules", action="store_true",
                    help="fait toutes les verifications hors ligne, echantillon, rendu "
                         "des demographies et contamination, puis s'arrete AVANT de "
                         "lancer le moindre serveur.")
    ap.add_argument("--port", type=int, default=0, help="0 pour choisir un port libre")
    ap.add_argument("--contexte", type=int, default=32768,
                    help="tokens par slot. 32768 couvre le persona le plus long "
                         "(28 007 tokens) plus la marge de 1 500")
    ap.add_argument("--parallele", type=int, default=1,
                    help="-np. 1 est la meilleure configuration mesuree en a3 4.7, et le "
                         "persona de 27 500 tokens interdit de toute facon de multiplier "
                         "les slots : le contexte est partage entre eux")
    ap.add_argument("--attendre-a5", action="store_true",
                    help="attendre la fin du run a5 avant de lancer le serveur")
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    if not os.path.exists(MODELE):
        sys.exit(f"modele introuvable : {MODELE}")
    if not os.path.exists(PARQUET):
        sys.exit(f"personas introuvables : {PARQUET}")

    with open(os.path.join(TRACES, f"a11-run{'-' + args.suffixe if args.suffixe else ''}.pid"),
              "w") as fh:
        fh.write(str(os.getpid()) + "\n")

    fin_ts, fin_dt = heure_de_fin(args.fin)
    print(f"popsim a11, agents locaux sur Twin-2K-500. "
          f"Fin dure a {fin_dt:%Y-%m-%d %H:%M} ({(fin_ts - time.time()) / 3600:.2f} h)",
          flush=True)
    print(f"charge machine : {os.getloadavg()}", flush=True)

    # ---------------------------------------------------------------- donnees et echantillon
    d = charger_twin()
    cibles = d["cibles"]
    y = d["y"]
    masque = np.array([[not est_manquant(v) for v in ligne] for ligne in y])
    table = nomenclature(cibles, d["catalogue"])
    ordre = ordre_des_items(cibles, table)
    plis = plis_personnes(len(d["pid"]), GRAINE_DECOUPAGE)

    personas_df = pd.read_parquet(
        PARQUET, columns=["pid", "wave1_3_persona_text", "wave1_3_persona_json"])
    disponibles = set(int(p) for p in personas_df["pid"])
    par_pli = max(1, args.personnes // N_PLIS)
    retenus = echantillon(d["pid"], plis, disponibles, par_pli)
    # Un echantillon plus petit que le nombre de plis ne peut pas etre equilibre : on
    # garde les premieres personnes du tirage stratifie, un pli chacune. Ce cas n'existe
    # que pour un smoke test, jamais pour un run de mesure.
    retenus = retenus[:args.personnes]
    index_pid = {int(r.pid): i for i, r in enumerate(personas_df.itertuples())}

    tete = [table[cibles[j]]["bloc"] for j in ordre[:60]]
    print("ordre des items : " + ", ".join(
        f"{b} x{tete.count(b)}" for b in dict.fromkeys(tete)) + ", puis le reste",
        flush=True)
    n_appels_prevus = int(sum(masque[p["index"]].sum() for p in retenus))
    print(f"{len(retenus)} personnes ({par_pli} par pli, tirees parmi les "
          f"{len(disponibles)} personas disponibles en local), {len(cibles)} items cibles, "
          f"{n_appels_prevus} appels par condition "
          f"(les cellules non vues par la personne ne sont pas interrogees)", flush=True)

    # ---------------------------------------------------------------- construction des personas
    personas = {}
    for p in retenus:
        r = personas_df.iloc[index_pid[p["pid"]]]
        texte = r["wave1_3_persona_text"]
        demo = rendre_demographies(r["wave1_3_persona_json"])
        if not verifier_rendu_demographies(demo, texte):
            sys.exit(f"pid {p['pid']} : le rendu des demographies n'est pas le prefixe "
                     "exact du persona complet, C2-Twin ne serait pas C3-Twin ampute")
        personas[p["pid"]] = {"C3-Twin": texte, "C2-Twin": demo}
    print(f"rendu des demographies verifie prefixe exact du persona sur les "
          f"{len(retenus)} personnes", flush=True)

    # Controle de contamination, refait sur notre echantillon : aucun libelle de question
    # de la vague 4 ne doit apparaitre dans le persona des vagues 1 a 3.
    libelles = {t["question"] for t in table.values() if len(t["question"]) > 40}
    fuites = [(p["pid"], q[:60]) for p in retenus for q in libelles
              if q[:80] in personas[p["pid"]]["C3-Twin"]]
    print(f"controle de contamination : {len(libelles)} libelles cibles distincts, "
          f"{len(fuites)} occurrence(s) dans les personas", flush=True)
    if fuites:
        sys.exit(f"le persona contient des questions de la vague 4 : {fuites[:5]}")

    # Le sous echantillon est ecrit AVANT le premier appel, et non a la fin. Il ne depend
    # d'aucun resultat, et c'est lui qui definit la population sur laquelle l'evaluation
    # restreindra les baselines et les conditions des auteurs : si le run est interrompu,
    # l'evaluateur doit quand meme savoir quelles personnes etaient prevues.
    chemin_personnes = os.path.join(
        TRACES, f"a11-personnes{'-' + args.suffixe if args.suffixe else ''}.csv")
    pd.DataFrame(retenus).to_csv(chemin_personnes, index=False)
    print(f"echantillon ecrit : {chemin_personnes}", flush=True)

    if args.verifications_seules:
        print("verifications seules : aucun serveur lance, arret ici", flush=True)
        return

    # ---------------------------------------------------------------- file d'attente
    if args.attendre_a5 and not attendre_a5():
        sys.exit("machine non liberee, aucun serveur lance")

    # Garde fou inconditionnel, et pas seulement sous --attendre-a5. Le script peut etre
    # lance par analyses/file_de_nuit.sh, qui sequence lui meme les travaux : dans ce cas
    # personne ne verifie a notre place. Un port libre ne prouve rien, un second serveur
    # peut tourner sur un autre port et se partager les 32 Gio de memoire unifiee, ce qui
    # fausse toute mesure de debit. C'est arrive cette nuit, la penalite mesuree est un
    # facteur 6 sur le debit du run concurrent.
    autres = serveurs_llama()
    if autres:
        sys.exit(f"un llama-server tourne deja (PID {autres}), aucun serveur lance. "
                 "Attendre sa fin, ou relancer avec --attendre-a5.")

    port = args.port or premier_port_libre()
    if not port_libre(port):
        sys.exit(f"le port {port} est occupe, un llama-server tourne peut etre deja")
    print(f"llama-server sur le port {port}, -np {args.parallele}, "
          f"-c {args.contexte * args.parallele}, KV q8_0", flush=True)

    moteur = MoteurA5(MODELE, contexte=args.contexte, parallele=args.parallele, port=port,
                      cache_kv_8bits=True)
    moteur.demarrer()
    print(f"serveur pret en {moteur.chargement_s:.1f} s", flush=True)

    passe = args.passe
    inverse = (passe == 2)
    resume, longueurs = [], []
    try:
        # ------------------------------------------------------------ longueur des personas
        # Mesure exacte, par le tokeniseur du serveur et non par une regle de trois sur le
        # nombre de caracteres. C'est elle qui commande le budget de prefill de la nuit et
        # la decision de tronquer ou non.
        budget = args.contexte - MARGE_TOKENS
        tronques = 0
        compter = lambda t: len(moteur.tokeniser(t))
        for p in retenus:
            n3 = len(moteur.tokeniser(personas[p["pid"]]["C3-Twin"]))
            n2 = len(moteur.tokeniser(personas[p["pid"]]["C2-Twin"]))
            texte_b, gardees, total_q = tronquer_persona(
                personas[p["pid"]]["C3-Twin"], compter, args.budget_c3b)
            personas[p["pid"]]["C3b-Twin"] = texte_b
            n3b = len(moteur.tokeniser(texte_b))
            coupe = n3 > budget
            if coupe:
                # Troncature documentee : on garde la tete du persona, qui commence par le
                # bloc Demographics, et on coupe la queue. Un marqueur explicite est
                # ajoute pour que le modele sache que la matiere est incomplete, et la
                # ligne de trace de chaque appel de cette personne le dira.
                texte = personas[p["pid"]]["C3-Twin"]
                lo, hi = 0, len(texte)
                while lo < hi:
                    mi = (lo + hi + 1) // 2
                    if len(moteur.tokeniser(texte[:mi])) <= budget - 40:
                        lo = mi
                    else:
                        hi = mi - 1
                personas[p["pid"]]["C3-Twin"] = (
                    texte[:lo] + "\n\n[The rest of this person's answers was truncated to "
                                 "fit the context window.]")
                tronques += 1
                print(f"  pid {p['pid']} tronque : {n3} tokens > budget {budget}",
                      flush=True)
                n3 = len(moteur.tokeniser(personas[p["pid"]]["C3-Twin"]))
            longueurs.append({"pid": p["pid"], "pli": p["pli"],
                              "tokens_c3": n3, "tokens_c3b": n3b, "tokens_c2": n2,
                              "questions_gardees_c3b": gardees, "questions_total": total_q,
                              "tronque_contexte": bool(coupe)})
        dl = pd.DataFrame(longueurs)
        chemin_long = os.path.join(
            TRACES, f"a11-personas-tokens{'-' + args.suffixe if args.suffixe else ''}.csv")
        dl.to_csv(chemin_long, index=False)
        print(f"longueur des personas, en tokens : C3-Twin min {dl.tokens_c3.min()}, "
              f"mediane {int(dl.tokens_c3.median())}, max {dl.tokens_c3.max()} ; "
              f"C3b-Twin mediane {int(dl.tokens_c3b.median())} "
              f"({int(dl.questions_gardees_c3b.median())} questions gardees sur "
              f"{int(dl.questions_total.median())}) ; "
              f"C2-Twin mediane {int(dl.tokens_c2.median())}. "
              f"{tronques} persona(s) coupe(s) par le contexte du serveur. "
              f"Ecrit : {chemin_long}", flush=True)

        # ------------------------------------------------------------ les conditions
        codes = [c.strip() for c in args.conditions.split(",") if c.strip()]
        for i, code in enumerate(codes):
            if code not in CONDITIONS:
                sys.exit(f"condition inconnue : {code}")
            if time.time() >= fin_ts:
                print("fin dure atteinte avant le lancement de " + code, flush=True)
                break
            # Toutes les conditions sauf la derniere s'arretent sur la reserve, pour que
            # la derniere ait de quoi tourner.
            # Chaque condition rend a celles qui la suivent le temps qu'il leur faut, et
            # pas davantage. Le plafond n'est pas la moitie du temps restant mais 30 pour
            # cent, et ce chiffre vient de la mesure : une personne coute environ 53
            # secondes en C3b-Twin contre 22 en C2-Twin. Les deux conditions parcourant les
            # personnes dans le meme ordre, la comparaison porte sur l'intersection, donc
            # sur la condition la plus lente. Un partage a parts egales donnerait a C2-Twin
            # deux fois plus de personnes qu'a C3b-Twin, dont la moitie ne servirait a rien.
            # Le partage 70 / 30 egalise a peu pres les deux couvertures.
            suivantes = codes[i + 1:]
            disponible = max(fin_ts - time.time(), 0.0)
            reserve = sum(RESERVE_PAR_CONDITION.get(c, 0) for c in suivantes) * 60
            reserve = min(reserve, disponible * 0.3)
            limite_temps = fin_ts - reserve
            if suivantes:
                print(f"[{code}] arret programme au plus tard a "
                      f"{datetime.datetime.fromtimestamp(limite_temps):%H:%M}, "
                      f"reserve de {reserve / 60:.0f} min pour {', '.join(suivantes)}",
                      flush=True)
            r = lancer(moteur, code, passe, inverse, retenus, cibles, masque, personas,
                       table, ordre, limite_temps, args.suffixe, limite=args.limite,
                       items_max=args.items_max)
            resume.append(r)
            print(f"[{code} passe {passe}] {r['appels']} appels en "
                  f"{r['secondes'] / 60:.1f} min, {r['appels_par_heure']:,.0f} appels/h, "
                  f"{r['rejets']} rejets".replace(",", " "), flush=True)
    finally:
        moteur.arreter()
        print(f"serveur arrete. charge machine : {os.getloadavg()}", flush=True)

    chemin_resume = os.path.join(
        TRACES, f"a11-resume{'-' + args.suffixe if args.suffixe else ''}.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({"fin_dure": fin_dt.isoformat(), "port": port,
                   "jeu": JEU, "modele": MODELE_NOM, "quantification": QUANTIFICATION,
                   "version_prompt": VERSION_PROMPT, "passe": passe,
                   "contexte": args.contexte, "parallele": args.parallele,
                   "personnes": len(retenus), "items": len(cibles),
                   "appels_prevus_par_condition": n_appels_prevus,
                   "budget_c3b": args.budget_c3b,
                   "personas_tokens": {
                       "c3_min": int(dl.tokens_c3.min()) if longueurs else None,
                       "c3_mediane": int(dl.tokens_c3.median()) if longueurs else None,
                       "c3_max": int(dl.tokens_c3.max()) if longueurs else None,
                       "c3b_mediane": int(dl.tokens_c3b.median()) if longueurs else None,
                       "c2_mediane": int(dl.tokens_c2.median()) if longueurs else None},
                   "conditions": resume}, fh, indent=2, ensure_ascii=False)
    print(f"resume ecrit : {chemin_resume}", flush=True)
    print(f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", flush=True)


if __name__ == "__main__":
    main()
