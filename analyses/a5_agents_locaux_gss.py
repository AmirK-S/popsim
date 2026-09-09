"""
a5_agents_locaux_gss : premier run d'agents locaux sur le GSS de l'archive OSF t6g7k.

Statut : script d'experience, pas du code de production. C'est le premier script du projet
qui produit NOS agents, et non une reanalyse des sorties de Stanford.

Ce qu'il fait. Pour chaque couple (personne, item cible), il construit un prompt, applique
le gabarit de conversation Qwen, envoie un seul passage avant a llama-server et lit la
distribution de probabilite du token de reponse. Il n'y a aucune generation de texte.

Le decoupage est repris EXACTEMENT de analyses/a2_baselines_gss.py, fonction grille(),
graine 20260903 : 5 plis de personnes et 5 blocs d'items. Chaque couple (personne, item)
est predit une fois, l'item est secret et les ~119 autres items forment le contexte. Nos
agents sont donc comparables cellule a cellule aux baselines B0, B1, B2 et aux conditions
d'agents de Stanford.

Conditions :
  C2   persona demographique seul, les 11 attributs de demographic_summary.csv en clair.
  C3   persona construit sur les reponses d'enquete, les ~119 items de contexte du bloc.
  C3F  meme persona que C3, mais le contexte est ampute de la FAMILLE thematique entiere
       de l'item cible, et c'est cette famille qui est predite. Meme regime que
       analyses/a8_familles.py, qui repond a la limite 7 de a2 : avec des blocs aleatoires,
       un item secret garde ses cousins thematiques dans le contexte et B2 en profite. Le
       rapport a8 montre que les agents composite de Stanford battent B2 des que la famille
       entiere sort du contexte. C3F est notre version de ce test. Six familles, 58 items,
       listes dans FAMILLES de a2_baselines_gss.py. Drapeau --familles.

La passe est un drapeau separe, --passe. La passe 1 presente les modalites dans l'ordre de
la nomenclature officielle, la passe 2 les presente dans l'ordre inverse : c'est la parade
au biais de position decrite en a3 section 3.4, et les deux passes se moyennent a
l'evaluation. La passe 2 n'est PAS dans la file de calcul de cette nuit, elle se lance
separement.

Scoring : traitement (a) de a3 section 3.4. Etiquettes courtes d'un token, lues a une
seule position, dans le meme contexte gauche pour toutes les modalites. Les identifiants
de tokens sont verifies distincts en encodant `prompt` puis `prompt + " A"`, jamais " A"
isole. La masse de probabilite portee par les K lettres avant renormalisation est
enregistree a chaque appel ; en dessous de 0,5 l'appel est marque rejete.

Entree  : data/osf-t6g7k-stanford, non versionne.
Sortie  : data/traces/a5-<condition>-p<passe>.jsonl, non versionne, une ligne par appel.
          data/traces/a5-personnes.csv, le sous echantillon retenu.
          data/traces/a5-run.log si lance par nohup.

Rien ne sort de la machine. Aucun appel API distant. La trace ne contient PAS la vraie
reponse de la personne : l'evaluation la relit dans data/, ce qui respecte la position par
defaut de METHODOLOGIE sur la publication des traces.

Usage :
  .venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C2,C3 --passe 1
  .venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --passe 2
  .venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --familles
  .venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C2 \\
      --personnes 3 --blocs 1 --suffixe smoke

Reprise : l'index unique est (condition, passe, pid, item). Une relance ne refait aucun
appel deja ecrit dans la trace.

Arret : `touch data/traces/STOP` arrete le run entre deux appels, trace fermee, resume
ecrit, code de sortie 0. Le fichier n'est pas efface par le script.
"""

import argparse
import datetime
import json
import math
import os
import socket
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_baselines_gss import charger, grille, FAMILLES, GRAINE, N_BLOCS, N_PLIS
from a3_banc_inference import MoteurLlama

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
QMASTER = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                               "question_master/gss/main.csv")
TRACES = os.path.join(RACINE, "data/traces")
MODELE = os.path.join(RACINE, "data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf")

# Journal du run et fichier d'arret. Lecon de la nuit du 8 au 9 septembre
# (JOURNAL-NUIT-2026-09-09.md, incident de 05:45 a 06:01) : le SIGINT n'a pas arrete le
# client, bloque dans un appel HTTP, et le SIGTERM n'a pas arrete le serveur ; il a fallu
# un kill -9 et une reprise a la main. La boucle relit donc ce fichier entre deux appels ;
# `touch data/traces/STOP` rend la machine sans trace tronquee. Le script ne l'efface
# jamais : celui qui l'a pose le retire, sinon le run suivant s'arreterait aussitot.
JOURNAL_RUN = os.path.join(TRACES, "a5-run.log")
FICHIER_ARRET = os.path.join(TRACES, "STOP")


def arret_demande():
    """Le fichier d'arret existe il ? Un stat par appel, rien devant un appel de modele."""
    return os.path.exists(FICHIER_ARRET)


def journaliser(message):
    """Ecrit dans le journal du run, quelle que soit la redirection de la sortie."""
    os.makedirs(TRACES, exist_ok=True)
    with open(JOURNAL_RUN, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()

# Etiquettes courtes, un token chacune. Treize suffisent : l'item cible le plus riche des
# 149 est `income`, a 12 modalites.
LETTRES = "ABCDEFGHIJKLM"

# Version du prompt, ecrite dans chaque ligne de trace. A incrementer des qu'un caractere
# du gabarit change, sinon deux runs incomparables se melangent dans le meme fichier.
VERSION_PROMPT = "a5-p1"

# Graine du sous echantillon de personnes. Distincte de la graine du decoupage, pour que
# changer la taille de l'echantillon ne change pas les plis.
GRAINE_ECHANTILLON = 20260907

MODELE_NOM = "Qwen3-4B-Instruct-2507"
QUANTIFICATION = "Q4_K_M"

# Seuil de rejet de a3 section 3.4. En dessous, la renormalisation fabriquerait une
# distribution a partir de presque rien.
SEUIL_MASSE = 0.5

CONSIGNE = ("Answer with a single capital letter, the label of the option you choose. "
            "Give no explanation and no other text.")

PREAMBULE = ("You are simulating one specific person answering a survey. "
             "Answer exactly as this person would answer, not as you would.")


# --------------------------------------------------------------------------------------
# 1. Nomenclature des questions et des modalites
# --------------------------------------------------------------------------------------

def nomenclature():
    """Libelle de question et ordre des modalites, lus dans question_master/gss/main.csv.

    L'ordre des modalites est celui du fichier officiel, jamais un ordre alphabetique ni
    l'ordre d'apparition dans les donnees. C'est lui qui fixe la correspondance
    lettre -> modalite, donc toute la lecture des resultats.

    Les identifiants de question sont en majuscules dans main.csv et en minuscules dans
    les fichiers de reponses. Les libelles de modalites sont capitalises dans main.csv et
    en minuscules dans les reponses. Les deux correspondances sont faites ici, une fois.
    """
    qm = pd.read_csv(QMASTER)
    table = {}
    for r in qm.itertuples():
        options = json.loads(r.Options)
        table[r._2.lower()] = {
            "question": r.Question,
            "options": options,
            "vers_canonique": {o.lower().strip(): o for o in options},
        }
    return table


def canoniser(nom, valeur, table):
    """Ramene une reponse observee a l'ecriture officielle de sa modalite."""
    if valeur is None or (isinstance(valeur, float) and math.isnan(valeur)):
        return None
    return table[nom]["vers_canonique"].get(str(valeur).lower().strip())


# --------------------------------------------------------------------------------------
# 2. Construction des prompts
# --------------------------------------------------------------------------------------

# Libelles lisibles des 11 attributs de demographic_summary.csv. Ecrits en clair dans le
# prompt systeme de C2, sans recodage ni abreviation.
ETIQUETTES_DEMOGRAPHIQUES = {
    "age": "Age",
    "census_division": "Census division",
    "political_ideology": "Political ideology",
    "political_party": "Political party",
    "education": "Education",
    "race": "Race",
    "ethnicity": "Ethnicity",
    "gender": "Gender",
    "income": "Household income",
    "neighborhood": "Neighborhood",
    "sexual_orientation": "Sexual orientation",
}


def systeme_c2(valeurs, attributs):
    """Prompt systeme de C2 : les 11 attributs demographiques, en clair.

    Les trois attributs incomplets gardent une modalite explicite plutot que d'etre
    omis, meme convention que a2 : omettre la ligne dirait au modele quelque chose de
    different de "non renseigne".
    """
    lignes = []
    for a, v in zip(attributs, valeurs):
        libelle = ETIQUETTES_DEMOGRAPHIQUES.get(a, a.replace("_", " ").capitalize())
        v = "not reported" if v in (None, "", "nan", "non renseigne") else v
        lignes.append(f"- {libelle}: {v}")
    return (PREAMBULE + "\n\nHere is what is known about this person:\n"
            + "\n".join(lignes) + "\n\n" + CONSIGNE)


def systeme_c3(indices_contexte, reponses, items, table):
    """Prompt systeme de C3 : les ~119 items de contexte, question et reponse en clair.

    Le bloc secret n'y figure pas, par construction du decoupage. C'est ce prompt qui
    porte tout le poids de calcul : il est identique pour les ~30 questions du meme
    bloc chez la meme personne, donc entierement servi par le cache de prefixe des le
    deuxieme appel, a condition que les appels se suivent.
    """
    lignes = []
    for j in indices_contexte:
        nom = items[j]
        rep = canoniser(nom, reponses[j], table)
        if rep is None:
            continue
        lignes.append(f"Q: {table[nom]['question']}\nA: {rep}")
    return (PREAMBULE + "\n\nHere is how this person answered other questions of the "
            "same survey.\n\n" + "\n\n".join(lignes) + "\n\n" + CONSIGNE)


def utilisateur(nom, table, inverse=False):
    """Bloc utilisateur : la question secrete et ses modalites etiquetees.

    inverse=True renverse l'ordre des modalites. C'est la seconde passe de C3, parade au
    biais de position. La correspondance lettre -> modalite change donc entre les deux
    passes, et c'est l'evaluateur qui les remet dans le meme repere avant de moyenner.
    """
    options = list(table[nom]["options"])
    if inverse:
        options = options[::-1]
    lignes = [f"Question. {table[nom]['question']}"]
    for i, o in enumerate(options):
        lignes.append(f"{LETTRES[i]}. {o}")
    return "\n".join(lignes), options


def gabarit_qwen(systeme, question):
    """Gabarit de conversation Qwen, applique a la main.

    Lecon de a3 section 4.5 : le gabarit n'est pas optionnel, et il doit se terminer
    SANS espace. Le prompt s'arrete sur `Answer:` et c'est le token " A" qui est score,
    pas le token "A". Avec un espace final, le modele hesite entre les deux et la masse
    de probabilite s'effondre.
    """
    return ("<|im_start|>system\n" + systeme + "<|im_end|>\n"
            "<|im_start|>user\n" + question + "<|im_end|>\n"
            "<|im_start|>assistant\nAnswer:")


# --------------------------------------------------------------------------------------
# 3. Le client serveur, etendu sans toucher a a3
# --------------------------------------------------------------------------------------

class MoteurA5(MoteurLlama):
    """MoteurLlama de a3, avec ce que le run a besoin de lire en plus.

    Rien n'est reecrit : le lancement du serveur, l'attente de disponibilite, l'arret et
    le transport HTTP sont ceux de a3. On ajoute la lecture des identifiants de tokens et
    la remontee des compteurs de cache, que passe_avant() de a3 ne renvoyait pas.
    """

    def tokeniser(self, texte):
        return self._poster("/tokenize", {"content": texte, "add_special": False})["tokens"]

    def tokens_des_lettres(self, prompt, n_lettres):
        """Identifiant du token de chaque lettre, dans CE contexte gauche precis.

        Methode imposee par a3 section 3.4 : on encode `prompt`, puis `prompt + " A"`, et
        on prend le token qui s'ajoute. On n'encode jamais " A" isolement, parce que la
        tokenisation depend du contexte gauche et donnerait souvent un autre decoupage.
        Retourne un dictionnaire lettre -> identifiant, et leve si deux lettres partagent
        un identifiant ou si l'ajout de la lettre a modifie le prefixe.
        """
        base = self.tokeniser(prompt)
        table = {}
        for lettre in LETTRES[:n_lettres]:
            etendu = self.tokeniser(prompt + " " + lettre)
            if etendu[:len(base)] != base:
                raise RuntimeError(f"l'ajout de ' {lettre}' a modifie le prefixe du prompt")
            if len(etendu) != len(base) + 1:
                raise RuntimeError(f"' {lettre}' n'est pas un token unique dans ce contexte "
                                   f"({len(etendu) - len(base)} tokens)")
            table[lettre] = etendu[len(base)]
        if len(set(table.values())) != len(table):
            raise RuntimeError(f"identifiants de tokens non distincts : {table}")
        return table, len(base)

    def scorer(self, prompt, n_probs=40):
        """Un passage avant, un seul token, temperature nulle, cache de prefixe actif.

        Renvoie la liste brute des top logprobs, avec identifiants de tokens quand le
        serveur les fournit, et les compteurs de temps et de cache.
        """
        debut = time.perf_counter()
        r = self._poster("/completion", {
            "prompt": prompt,
            "n_predict": 1,
            "n_probs": n_probs,
            "temperature": 0.0,
            "cache_prompt": True,
            "post_sampling_probs": False,
        })
        duree_ms = (time.perf_counter() - debut) * 1000.0
        t = r.get("timings", {})
        cps = r.get("completion_probabilities") or []
        top = cps[0].get("top_logprobs", []) if cps else []
        return {
            "top": top,
            "duree_ms": duree_ms,
            "tokens_prompt": r.get("tokens_evaluated"),
            "tokens_calcules": t.get("prompt_n"),
            "prompt_ms": t.get("prompt_ms"),
        }


def masse_des_lettres(top, ids_lettres, lettres):
    """Probabilite brute de chaque lettre, lue dans le top n renvoye par le serveur.

    On identifie la lettre par l'identifiant de token quand le serveur le donne, et par
    la chaine exacte " A" sinon. Jamais par un strip() : "A" colle et " A" precede d'une
    espace sont deux tokens differents et un seul des deux est celui qu'on a verifie.
    """
    par_id = {e["id"]: e for e in top if "id" in e}
    brut = {}
    for lettre in lettres:
        e = par_id.get(ids_lettres[lettre])
        if e is None:
            e = next((x for x in top if x.get("token") == " " + lettre), None)
        brut[lettre] = math.exp(e["logprob"]) if e is not None else 0.0
    return brut


# --------------------------------------------------------------------------------------
# 4. Sous echantillon de personnes
# --------------------------------------------------------------------------------------

def echantillon(ids, plis, par_pli, graine=GRAINE_ECHANTILLON):
    """Tire un sous echantillon stratifie sur les 5 plis du decoupage de a2.

    Stratifier sur les plis n'est pas cosmetique : les baselines B1 et B2 sont evaluees
    pli par pli, entrainees sur les autres. Un echantillon desequilibre donnerait a
    l'evaluation un melange de tailles d'entrainement selon la personne.
    """
    rng = np.random.default_rng(graine)
    retenus = []
    for i_pli, (_, te) in enumerate(plis):
        n = min(par_pli, len(te))
        for k in sorted(rng.choice(te, size=n, replace=False)):
            retenus.append({"pid": ids[k], "index": int(k), "pli": i_pli})
    return retenus


# --------------------------------------------------------------------------------------
# 5. Trace, index et reprise
# --------------------------------------------------------------------------------------

def chemin_trace(condition, passe, suffixe):
    nom = f"a5-{condition}-p{passe}"
    if suffixe:
        nom += "-" + suffixe
    return os.path.join(TRACES, nom + ".jsonl")


def index_existant(chemin):
    """Cle (pid, item) des appels deja ecrits. Une relance ne les refait pas.

    Les lignes tronquees par un arret brutal sont ignorees sans faire echouer la reprise :
    la derniere ligne d'un fichier interrompu en cours d'ecriture est souvent incomplete.
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
            fait.add((d["pid"], d["item"]))
    return fait


# --------------------------------------------------------------------------------------
# 6. Le run
# --------------------------------------------------------------------------------------

def groupes_familles(items):
    """Les six familles thematiques de a2, converties en indices de colonnes.

    Reprises telles quelles de FAMILLES dans a2_baselines_gss.py, pour que le regime
    d'ablation de C3F soit exactement celui de a8_familles.py et que les chiffres se
    comparent ligne a ligne. 58 items au total sur les 149.
    """
    index = {it: j for j, it in enumerate(items)}
    return [(nom, [index[i] for i in membres if i in index])
            for nom, membres in FAMILLES.items()]


def travaux(condition, retenus, items, blocs, y1, x, attributs, table):
    """Enumere les appels a faire, dans l'ordre qui maximise le cache de prefixe.

    C2 : le prompt systeme ne depend que de la personne. Les 149 questions se suivent sur
    le meme prefixe, donc un seul calcul de prefixe par personne.
    C3 : le prompt systeme depend de la personne ET du bloc secret. Les ~30 questions du
    bloc se suivent, donc cinq calculs de prefixe par personne.
    C3F : le prompt systeme depend de la personne ET de la famille cible. La famille
    entiere sort du contexte, qui compte alors 132 a 144 items selon la famille, et ce
    sont les 5 a 17 items de la famille qui sont predits. Six prefixes par personne pour
    58 appels seulement : c'est la condition la plus chere du lot par appel produit.

    Produit des tuples (personne, etiquette de groupe, index d'item, prompt systeme).
    """
    tous = np.arange(len(items))
    for p in retenus:
        if condition == "C2":
            sys_txt = systeme_c2(x[p["index"]], attributs)
            for i_bloc, bloc in enumerate(blocs):
                for j in bloc:
                    yield p, i_bloc, int(j), sys_txt
        elif condition == "C3F":
            for nom, cols in groupes_familles(items):
                contexte = np.setdiff1d(tous, cols)
                sys_txt = systeme_c3(contexte, y1[p["index"]], items, table)
                for j in cols:
                    yield p, nom, int(j), sys_txt
        else:
            for i_bloc, bloc in enumerate(blocs):
                contexte = np.setdiff1d(tous, bloc)
                sys_txt = systeme_c3(contexte, y1[p["index"]], items, table)
                for j in bloc:
                    yield p, i_bloc, int(j), sys_txt


def lancer(moteur, condition, passe, inverse, retenus, items, blocs, y1, x, attributs,
           table, fin_dure, suffixe, limite=None, journal_tous=200):
    """Execute une condition de bout en bout et ecrit la trace au fil de l'eau.

    Ecriture incrementale avec flush a chaque ligne : le script doit survivre a un arret
    brutal et reprendre exactement ou il s'etait arrete.
    """
    chemin = chemin_trace(condition, passe, suffixe)
    fait = index_existant(chemin)
    print(f"[{condition} passe {passe}] trace {chemin}, {len(fait)} appels deja faits",
          flush=True)

    ids_lettres_par_k = {}
    n_appels, n_rejets, n_absents = 0, 0, 0
    arret = False
    t0 = time.time()
    dernier_prefixe = None

    with open(chemin, "a", encoding="utf-8") as fh:
        for p, i_bloc, j, sys_txt in travaux(condition, retenus, items, blocs, y1, x,
                                             attributs, table):
            nom = items[j]
            if (p["pid"], nom) in fait:
                continue
            if arret_demande():
                # La trace est fermee et synchronisee par le bloc `with` en sortant d'ici,
                # le resume est ecrit par main() : la sortie est propre, code 0.
                arret = True
                message = (f"[{condition} passe {passe}] ARRET DEMANDE ({FICHIER_ARRET}), "
                           f"arret propre apres {n_appels} appels")
                print(message, flush=True)
                journaliser("ARRET DEMANDE " + message)
                break
            if time.time() >= fin_dure:
                print(f"[{condition} passe {passe}] fin dure atteinte, arret propre",
                      flush=True)
                break
            if limite is not None and n_appels >= limite:
                break

            bloc_user, options = utilisateur(nom, table, inverse=inverse)
            prompt = gabarit_qwen(sys_txt, bloc_user)
            k = len(options)
            lettres = LETTRES[:k]

            # Verification des identifiants de tokens : une fois par nombre de modalites,
            # sur le premier prompt rencontre. Le contexte gauche est le meme pour tous
            # les prompts, il se termine toujours par "Answer:".
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
                distribution = {options[i]: brut[l] / masse for i, l in enumerate(lettres)}
            else:
                distribution = {o: 1.0 / k for o in options}
            argmax = max(distribution, key=distribution.get)

            ligne = {
                "pid": p["pid"], "item": nom, "condition": condition, "passe": passe,
                "pli": p["pli"], "bloc": i_bloc,
                "version_prompt": VERSION_PROMPT,
                "modele": MODELE_NOM, "quantification": QUANTIFICATION,
                "ordre_modalites": "inverse" if inverse else "nomenclature",
                "duree_ms": round(r["duree_ms"], 2),
                "masse_lettres": masse,
                "rejet": rejet,
                "modalites_absentes": absentes,
                "distribution": distribution,
                "argmax": argmax,
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
                print(f"  {condition} p{passe} : {n_appels} appels, {debit:,.0f}/h, "
                      f"rejets {n_rejets}, "
                      f"{datetime.datetime.now():%H:%M:%S}".replace(",", " "), flush=True)
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    return {
        "condition": condition, "passe": passe, "appels": n_appels,
        "deja_faits": len(fait), "secondes": ecoule,
        "appels_par_heure": n_appels / ecoule * 3600 if n_appels else 0.0,
        "rejets": n_rejets, "appels_avec_modalite_absente": n_absents,
        "arret_demande": arret, "trace": chemin,
    }


# --------------------------------------------------------------------------------------

def port_libre(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) != 0


def premier_port_libre(depart=8099, essais=20):
    for p in range(depart, depart + essais):
        if port_libre(p):
            return p
    raise RuntimeError("aucun port libre trouve")


def heure_de_fin(texte):
    """Convertit 'HH:MM' en horodatage absolu, aujourd'hui ou demain selon l'heure."""
    h, m = (int(v) for v in texte.split(":"))
    maintenant = datetime.datetime.now()
    cible = maintenant.replace(hour=h, minute=m, second=0, microsecond=0)
    if cible <= maintenant:
        cible += datetime.timedelta(days=1)
    return cible.timestamp(), cible


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--conditions", default="C2,C3",
                    help="liste ordonnee parmi C2, C3 et C3F")
    ap.add_argument("--familles", action="store_true",
                    help="bascule C3 en C3F : le contexte est ampute de la famille "
                         "thematique entiere de l'item cible, et c'est cette famille qui "
                         "est predite. Regime de a8_familles.py, 6 familles et 58 items.")
    ap.add_argument("--passe", type=int, default=1, choices=(1, 2),
                    help="1 : modalites dans l'ordre de la nomenclature. "
                         "2 : ordre inverse, parade au biais de position (a3 3.4). "
                         "La passe 2 se lance separement, jamais dans la meme file.")
    ap.add_argument("--personnes", type=int, default=150,
                    help="taille du sous echantillon, reparti egalement sur les 5 plis")
    ap.add_argument("--blocs", type=int, default=N_BLOCS,
                    help="nombre de blocs d'items traites, 5 pour les 149 items")
    ap.add_argument("--fin", default="07:30", help="fin dure du calcul, heure locale")
    ap.add_argument("--suffixe", default="", help="suffixe de fichier, pour un smoke test")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal d'appels par condition, pour un smoke test")
    ap.add_argument("--port", type=int, default=0, help="0 pour choisir un port libre")
    ap.add_argument("--contexte", type=int, default=8192, help="tokens par slot")
    ap.add_argument("--parallele", type=int, default=8, help="-np, 8 en configuration a3")
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    if not os.path.exists(MODELE):
        sys.exit(f"modele introuvable : {MODELE}")

    fin_ts, fin_dt = heure_de_fin(args.fin)
    print(f"popsim a5, run d'agents locaux. Fin dure a {fin_dt:%Y-%m-%d %H:%M} "
          f"({(fin_ts - time.time()) / 3600:.2f} h)", flush=True)
    print(f"charge machine : {os.getloadavg()}", flush=True)

    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    plis, blocs = grille(len(ids), len(items), GRAINE)
    blocs = blocs[:args.blocs]
    par_pli = max(1, args.personnes // N_PLIS)
    retenus = echantillon(ids, plis, par_pli)
    n_items = sum(len(b) for b in blocs)
    n_familles = sum(len(cols) for _, cols in groupes_familles(items))
    print(f"{len(retenus)} personnes ({par_pli} par pli), {n_items} items par personne, "
          f"soit {len(retenus) * n_items} appels pour C2 et C3, "
          f"{len(retenus) * n_familles} pour C3F", flush=True)

    # Le sous echantillon est ecrit avant tout appel : c'est lui qui definit la population
    # sur laquelle l'evaluation restreindra les baselines et les conditions de Stanford.
    chemin_personnes = os.path.join(TRACES, "a5-personnes.csv")
    if not args.suffixe:
        pd.DataFrame(retenus).to_csv(chemin_personnes, index=False)
        print(f"echantillon ecrit : {chemin_personnes}", flush=True)

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
    codes = [c.strip() for c in args.conditions.split(",") if c.strip()]
    if args.familles:
        codes = ["C3F" if c == "C3" else c for c in codes]
    resume = []
    try:
        for code in codes:
            if code not in ("C2", "C3", "C3F"):
                sys.exit(f"condition inconnue : {code}")
            if time.time() >= fin_ts:
                print("fin dure atteinte avant le lancement de " + code, flush=True)
                break
            r = lancer(moteur, code, passe, inverse, retenus, items, blocs, y1, x,
                       attributs, table, fin_ts, args.suffixe, limite=args.limite)
            resume.append(r)
            print(f"[{code} passe {passe}] {r['appels']} appels en {r['secondes'] / 60:.1f} min, "
                  f"{r['appels_par_heure']:,.0f} appels/h, {r['rejets']} rejets"
                  .replace(",", " "), flush=True)
            if r.get("arret_demande"):
                # Le fichier d'arret vaut pour le run entier, pas pour une condition.
                print("ARRET DEMANDE, les conditions suivantes ne sont pas lancees",
                      flush=True)
                journaliser("ARRET DEMANDE, les conditions suivantes ne sont pas lancees")
                break
    finally:
        # Le serveur est arrete quoi qu'il arrive : un second run est en attente de la
        # machine et deux llama-server ne doivent jamais tourner en meme temps.
        moteur.arreter()
        print(f"serveur arrete. charge machine : {os.getloadavg()}", flush=True)

    chemin_resume = os.path.join(TRACES, f"a5-resume{'-' + args.suffixe if args.suffixe else ''}.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({"fin_dure": fin_dt.isoformat(), "port": port,
                   "modele": MODELE_NOM, "quantification": QUANTIFICATION,
                   "version_prompt": VERSION_PROMPT, "passe": passe,
                   "personnes": len(retenus), "items": n_items,
                   "conditions": resume}, fh, indent=2, ensure_ascii=False)
    print(f"resume ecrit : {chemin_resume}", flush=True)
    # Marqueur attendu par le run suivant, qui surveille la fin de ce processus.
    print(f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", flush=True)


if __name__ == "__main__":
    main()
