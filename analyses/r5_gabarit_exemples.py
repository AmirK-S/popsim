"""
r5_gabarit_exemples : le gabarit ChatML ET les trois exemples, sur le meme fichier de poids.

Statut : script d'experience, pas du code de production. Il joue la condition unique de
`resultats/r5-preenregistrement.md`, ecrite le 9 septembre 2026 a 09:50 et validee par
Amir le meme jour.

Ce qu'il fait. R4 a mesure « le format » comme un bloc : gabarit de conversation d'un cote,
completion a trois exemples de l'autre. Les deux composantes n'y sont pas separables. Cette
condition les separe :

  q4gab3   Qwen3-4B-Instruct-2507, LE MEME FICHIER GGUF que `q4` et que `q4nogab`,
           le gabarit ChatML de R1, ET les trois exemples de R4 places dans le tour
           utilisateur, juste avant la question. Meme invite systeme que `q4`, dans le
           tour systeme, comme en R1.

Les trois autres conditions du tableau ne sont pas rejouees : ce sont les traces deja
ecrites, `data/traces/r1-q4.jsonl` (R1), `r1-q4nogab-r4.jsonl` et `r1-q4base-r4.jsonl` (R4).
Elles sont copiees octet pour octet sous le suffixe `r5` pour que l'evaluateur voie les
quatre conditions dans le meme tableau, comme R4 l'avait fait pour `q4`.

Ce que ce run NE tranche PAS. Il ne dit rien de la contamination, rien d'un autre modele,
rien d'une autre famille de gabarit. Il compare trois formats d'invite sur un seul fichier
de poids, et rien d'autre.

Rien n'est recopie de `r1_oracle_camps.py` ni de `r4_oracle_socle.py` : leurs fonctions sont
importees et appelees. Le bloc des trois exemples est celui de R4, obtenu par `R4.prefixe`
et non retape, ce qui garantit qu'il est identique au caractere pres a celui que R4 a montre
a ses trois conditions. Aucun fichier existant du depot n'est modifie par ce script.

Relance et arret. `--sans-relance` est la conduite preenregistree de R5 et le defaut de ce
script : un echec de premiere tentative est un rejet, jamais rejoue, et le taux de rejet se
publie en tete du rapport. Motif, mesure en `r4-resultats.md` section 3.1 : en mode
completion la relance recopie son exemple chiffre 45 fois sur 45. `touch data/traces/STOP`
arrete le run entre deux appels, trace fermee, resume ecrit, code de sortie 0.

Entree  : data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf, non versionne.
          data/traces/r1-distributions-reelles.csv, le referent humain de R1, reutilise
          tel quel et jamais reecrit.
          data/traces/r1-q4.jsonl, r1-q4nogab-r4.jsonl, r1-q4base-r4.jsonl, pour la
          seule copie de comparaison, jamais modifiees.
Sortie  : data/traces/r5-q4gab3.jsonl, une ligne par appel, non versionne.
          data/traces/r5-smoke.jsonl et r5-smoke.log, l'essai a blanc, jamais melanges au run.
          data/traces/r5-resume.json, data/traces/r5-run.log (marqueur RUN TERMINE).
          resultats/r5-contrastes.csv, r5-tableau.csv, r5-rejets.csv.

Rien ne sort de la machine. Aucun appel distant.

Usage :
  .venv/bin/python analyses/r5_gabarit_exemples.py --verifier      # hors ligne, sans serveur
  .venv/bin/python analyses/r5_gabarit_exemples.py --smoke         # essai a blanc, 3 cellules
  .venv/bin/python analyses/r5_gabarit_exemples.py --fin 15:00     # le run, 894 cellules
  .venv/bin/python analyses/r5_gabarit_exemples.py --evaluer
  .venv/bin/python analyses/r5_gabarit_exemples.py --contrastes

Reprise : l'index unique est (version_prompt, item, camp, identite) dans le fichier de la
condition, mecanisme de R1 inchange. Une relance ne refait aucun appel deja ecrit.
"""

import argparse
import collections
import datetime
import hashlib
import json
import os
import shutil
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_oracle_camps as R1
import r4_oracle_socle as R4
from a2_baselines_gss import charger, FAMILLES
from a5_agents_locaux_gss import heure_de_fin, nomenclature, port_libre, premier_port_libre

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data/traces")
SORTIE = os.path.join(RACINE, "resultats")
GGUF = os.path.join(RACINE, "data/modeles/gguf")

# Suffixe de fichier de la seance. Il donne les copies r1-<cle>-r5.jsonl des conditions de
# comparaison, ce que r1_evaluer.py --suffixe r5 va chercher.
SUFFIXE = "r5"

# Version du gabarit d'invite. Elle DOIT differer de « r1-d1 » (R1) et de « r4-c3 » (R4) :
# trois formats d'invite ne se melangent pas dans un meme index de reprise, et la difference
# doit rester lisible ligne par ligne dans la trace.
VERSION_PROMPT = "r5-g3"

GABARIT = "chatml-3ex"

CLE = "q4gab3"

# Le referent humain de R1, reutilise tel quel. Meme empreinte que celle exigee par R4 :
# le critere de chute refuse de tourner si elle a bouge.
REFERENT = os.path.join(TRACES, "r1-distributions-reelles.csv")
REFERENT_SHA = R4.REFERENT_SHA

JOURNAL = os.path.join(TRACES, "r5-run.log")
JOURNAL_SMOKE = os.path.join(TRACES, "r5-smoke.log")

# Les trois conditions deja jouees, copiees pour l'evaluation commune. Aucun appel refait.
COMPARAISONS = {
    "q4": "r1-q4.jsonl",
    "q4nogab": "r1-q4nogab-r4.jsonl",
    "q4base": "r1-q4base-r4.jsonl",
}

ORDRE_CONDITIONS = ["q4", "q4nogab", "q4base", "q4gab3"]

LIBELLES = {
    "q4": "Qwen3-4B-Instruct-2507, gabarit ChatML, sans exemple",
    "q4nogab": "Qwen3-4B-Instruct-2507, completion a trois exemples, sans gabarit",
    "q4base": "Qwen3-4B-Base, completion a trois exemples",
    "q4gab3": "Qwen3-4B-Instruct-2507, gabarit ChatML ET trois exemples",
}


# --------------------------------------------------------------------------------------
# 1. Le registre du modele de r5
# --------------------------------------------------------------------------------------
# Meme fichier de poids que `q4` et que `q4nogab`, meme empreinte : c'est la condition pour
# que les trois contrastes tiennent les poids fixes et ne bougent que le format.

MODELES = {
    CLE: {
        "nom": "Qwen3-4B-Instruct-2507",
        "fichier": R4.MODELES["q4nogab"]["fichier"],
        "quantification": "Q4_K_M",
        "gabarit": GABARIT,
        "coupure_publiee": "aucune",
        "type": "instruit, gabarit de conversation ET trois exemples",
        "depot": R4.MODELES["q4nogab"]["depot"],
        "sha256": R4.MODELES["q4nogab"]["sha256"],
        "octets": R4.MODELES["q4nogab"]["octets"],
    },
}


# --------------------------------------------------------------------------------------
# 2. L'invite : le gabarit ChatML de R1, les exemples de R4 dans le tour utilisateur
# --------------------------------------------------------------------------------------

def bloc_exemples():
    """Le bloc des trois exemples de R4, au caractere pres, sans le texte systeme.

    `R4.prefixe(sys)` rend `sys + "\\n\\n" + <bloc des trois exemples>`. Appele avec un texte
    systeme vide, il rend donc `"\\n\\n" + <bloc>` : les deux premiers caracteres sont
    retires et ce qui reste est, octet pour octet, ce que R4 a montre a `q4nogab`,
    `q4base` et `q4hyb`. Rien n'est retape ici, pour qu'aucune divergence silencieuse ne
    puisse s'installer entre les exemples de R4 et ceux de R5.
    """
    p = R4.prefixe("")
    if not p.startswith("\n\n"):
        raise RuntimeError("R4.prefixe a change de forme : le bloc d'exemples n'est plus "
                           "extractible sans le recopier")
    return p[2:]


_gabarit_precedent = R1.gabarit          # deja la version chainee posee par R4


def gabarit(nom_gabarit, sys_txt, usr_txt):
    """Le gabarit ChatML de R1, avec les trois exemples inseres dans le tour utilisateur.

    Le tour systeme est celui de `q4`, inchange. Le tour utilisateur est celui de `q4`
    precede du bloc d'exemples de R4. La seule difference entre `q4gab3` et `q4` est donc
    l'insertion de ce bloc ; la seule difference entre `q4gab3` et `q4nogab` est l'habillage
    ChatML et la remontee du texte systeme dans son propre tour. C'est ce qui fait des trois
    contrastes des contrastes a une seule difference.
    """
    if nom_gabarit == GABARIT:
        return ("<|im_start|>system\n" + sys_txt + "<|im_end|>\n"
                "<|im_start|>user\n" + bloc_exemples() + usr_txt + "<|im_end|>\n"
                "<|im_start|>assistant\n")
    return _gabarit_precedent(nom_gabarit, sys_txt, usr_txt)


# Sequences d'arret : l'union de celles de `q4` et de celles de `q4nogab`, decidee et
# ecrite AVANT le premier appel. Sous ChatML un modele qui obeit ferme son tour par
# <|im_end|> et les separateurs d'exemple ne servent jamais ; ils sont la uniquement pour
# le cas ou les exemples entraineraient le modele a enchainer un quatrieme exemple, ce que
# R4 section 2.3 a mesure sur `q4hyb`. Une securite inerte dans le cas normal vaut mieux
# qu'un rejet evitable. L'essai a blanc verifie qu'elle est bien inerte, et le rapport le
# dit.
ARRETS = list(dict.fromkeys(R1.ARRETS["qwen-chatml"] + R4.ARRETS))


# Injection dans le module de R1, en memoire seulement. `R1.lancer()` appelle `gabarit()`,
# `ARRETS` et `chemin_trace()` par leur nom global : les remplacer ici suffit, et aucun
# fichier du depot n'est touche.
R1.gabarit = gabarit
R1.ARRETS[GABARIT] = ARRETS
for _cle, _info in MODELES.items():
    R1.MODELES.setdefault(_cle, _info)

_chemin_trace_precedent = R1.chemin_trace


def chemin_trace(cle, suffixe):
    """`data/traces/r5-q4gab3.jsonl` pour le run, `r5-smoke.jsonl` pour l'essai a blanc.

    La page de plan nomme ces deux fichiers. Le nom par defaut de R1 serait
    `r1-q4gab3-r5.jsonl` ; il est conserve pour toute autre cle, en particulier pour les
    copies des trois conditions de comparaison, que l'evaluateur lit sous ce nom la.
    """
    if cle in MODELES:
        return os.path.join(TRACES,
                            "r5-smoke.jsonl" if suffixe == "smoke" else f"r5-{cle}.jsonl")
    return _chemin_trace_precedent(cle, suffixe)


R1.chemin_trace = chemin_trace


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as fh:
        for bloc in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# --------------------------------------------------------------------------------------
# 3. La verification hors ligne, sans un seul appel de modele
# --------------------------------------------------------------------------------------

def verifier(items, table, bavard=True):
    """Tout ce qui peut etre verifie sans serveur. Rend la liste des defauts trouves."""
    defauts = []

    def dire(*a):
        if bavard:
            print(*a, flush=True)

    dire("=" * 78)
    dire("1. Le bloc d'exemples est celui de R4, au caractere pres")
    bloc = bloc_exemples()
    ref_bloc = R4.prefixe("x")[len("x") + 2:]
    dire(f"   {len(bloc)} caracteres, {bloc.count(R4.SEPARATEUR)} separateurs, "
         f"{len(R4.EXEMPLES)} exemples")
    if bloc != ref_bloc:
        defauts.append("le bloc d'exemples depend du texte systeme")
    if bloc.count(R4.SEPARATEUR) != len(R4.EXEMPLES) + 1:
        defauts.append("nombre de separateurs inattendu dans le bloc d'exemples")
    for ex in R4.EXEMPLES:
        if R4.bloc_exemple(ex) not in bloc:
            defauts.append("un exemple de R4 est absent du bloc")
    dire(f"   identique au bloc montre par R4 : {'oui' if bloc == ref_bloc else 'NON'}")

    dire("")
    dire("2. Le tour systeme et le tour utilisateur, contre ceux de q4")
    item = items[0]
    sys_txt = R1.systeme("gauche", "journaliste")
    usr_txt, opts = R1.utilisateur(item, "gauche", table)
    p_gab3 = gabarit(GABARIT, sys_txt, usr_txt)
    p_q4 = _gabarit_precedent("qwen-chatml", sys_txt, usr_txt)
    p_nogab = _gabarit_precedent(R4.GABARIT, sys_txt, usr_txt)
    # q4gab3 doit etre exactement q4 avec le bloc d'exemples insere avant le bloc question.
    attendu = p_q4.replace("<|im_start|>user\n", "<|im_start|>user\n" + bloc, 1)
    dire(f"   q4      : {len(p_q4)} caracteres")
    dire(f"   q4nogab : {len(p_nogab)} caracteres")
    dire(f"   q4gab3  : {len(p_gab3)} caracteres")
    if p_gab3 != attendu:
        defauts.append("q4gab3 n'est pas q4 plus le bloc d'exemples")
    dire("   q4gab3 == q4 + bloc d'exemples dans le tour utilisateur : "
         f"{'oui' if p_gab3 == attendu else 'NON'}")
    for balise in ("<|im_start|>system", "<|im_start|>user", "<|im_start|>assistant",
                   "<|im_end|>"):
        if balise not in p_gab3:
            defauts.append(f"balise ChatML absente : {balise}")
    if sys_txt not in p_gab3.split("<|im_start|>user")[0]:
        defauts.append("le texte systeme n'est pas dans le tour systeme")
    if not p_gab3.endswith("<|im_start|>assistant\n"):
        defauts.append("l'invite ne se termine pas par l'ouverture du tour assistant")

    dire("")
    dire("3. Les sequences d'arret")
    dire(f"   union : {ARRETS}")
    for a in R1.ARRETS["qwen-chatml"]:
        if a not in ARRETS:
            defauts.append(f"arret de q4 manquant : {a}")
    for a in R4.ARRETS:
        if a not in ARRETS:
            defauts.append(f"arret de q4nogab manquant : {a}")

    dire("")
    dire("4. Le referent humain de R1, reutilise tel quel")
    if not os.path.exists(REFERENT):
        defauts.append("referent humain absent")
        dire("   ABSENT")
    else:
        h = sha256(REFERENT)
        dire(f"   sha256 {h}")
        dire(f"   attendu {REFERENT_SHA}  ->  "
             f"{'identique' if h == REFERENT_SHA else 'DIFFERENT'}")
        if h != REFERENT_SHA:
            defauts.append("le referent humain a change depuis R1")

    dire("")
    dire("5. Le fichier de poids, le meme que q4 et q4nogab")
    info = MODELES[CLE]
    chemin = os.path.join(GGUF, info["fichier"])
    if not os.path.exists(chemin):
        defauts.append("fichier de poids absent")
        dire(f"   ABSENT : {chemin}")
    else:
        octets = os.path.getsize(chemin)
        h = sha256(chemin)
        ok = (octets == info["octets"]) and (h == info["sha256"])
        dire(f"   {octets} octets, sha256 {h[:16]}...  "
             f"{'conforme' if ok else 'NON CONFORME'}")
        if not ok:
            defauts.append("taille ou empreinte du fichier de poids non conforme")

    dire("")
    dire("6. Les trois traces de comparaison, presentes et lisibles")
    for cle, nom in COMPARAISONS.items():
        source = os.path.join(TRACES, nom)
        if not os.path.exists(source):
            defauts.append(f"{cle} : trace de comparaison absente ({nom})")
            dire(f"   {cle:8s} ABSENT : {source}")
            continue
        with open(source, encoding="utf-8") as fh:
            n = sum(1 for ligne in fh if ligne.strip())
        dire(f"   {cle:8s} {n} lignes, {nom}")
        if n != 894:
            defauts.append(f"{cle} : {n} lignes au lieu de 894")

    dire("")
    dire("7. Le plan de cellules")
    dire(f"   {len(items)} items, {len(R1.CAMPS)} camps, {len(R1.IDENTITES)} identites, "
         f"{len(items) * 3 * 2} cellules")
    if len(items) == 149 and len(items) * 3 * 2 != 894:
        defauts.append("le plan de cellules ne fait pas 894 cellules")

    dire("")
    dire("8. Les chemins de fichiers, run et essai a blanc separes")
    dire(f"   run   : {chemin_trace(CLE, '')}")
    dire(f"   smoke : {chemin_trace(CLE, 'smoke')}")
    dire(f"   journal du run   : {JOURNAL}")
    dire(f"   journal du smoke : {JOURNAL_SMOKE}")
    if chemin_trace(CLE, "") == chemin_trace(CLE, "smoke"):
        defauts.append("le run et l'essai a blanc partagent leur trace")
    if os.path.basename(chemin_trace(CLE, "")) != "r5-q4gab3.jsonl":
        defauts.append("la trace du run n'est pas r5-q4gab3.jsonl")

    dire("")
    dire("9. L'invite complete, une cellule reelle, telle qu'elle partira")
    dire("   " + "-" * 74)
    for ligne in p_gab3.split("\n"):
        dire("   | " + ligne)
    dire("   " + "-" * 74)
    dire(f"   {len(p_gab3)} caracteres, environ {len(p_gab3) // 4} tokens ; le prefixe "
         f"commun a un couple (camp, identite) en fait "
         f"{len(p_gab3) - len(usr_txt) - len('<|im_end|>\\n<|im_start|>assistant\\n')}")

    dire("")
    dire("=" * 78)
    if defauts:
        dire(f"{len(defauts)} DEFAUT(S) :")
        for d in defauts:
            dire("   - " + d)
    else:
        dire("aucun defaut. La verification hors ligne passe.")
    return defauts


# --------------------------------------------------------------------------------------
# 4. Le run
# --------------------------------------------------------------------------------------

def journaliser(message, chemin=None):
    os.makedirs(TRACES, exist_ok=True)
    with open(chemin or JOURNAL, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


def sonde_arrets(moteur, items, table, n_predict):
    """Une cellule, deux jeux d'arrets, pour voir si les separateurs servent a quelque chose.

    Deux appels supplementaires de l'essai a blanc, jamais du run. Ils repondent a la seule
    question que la page de plan laisse ouverte sur le format : sous ChatML, un modele a qui
    on montre trois exemples enchaine t il un quatrieme exemple ? Si l'arret rendu par le
    serveur est le token de fin de tour dans les deux cas et que les deux textes sont
    identiques, alors les separateurs d'exemple sont inertes et le contraste `q4gab3` contre
    `q4` ne bouge que d'une chose, les exemples.
    """
    item = items[0]
    sys_txt = R1.systeme("gauche", "journaliste")
    usr_txt, _ = R1.utilisateur(item, "gauche", table)
    prompt = gabarit(GABARIT, sys_txt, usr_txt)
    sortie = {}
    for nom, arrets in (("union", ARRETS), ("chatml seul", R1.ARRETS["qwen-chatml"])):
        r = moteur.decrire(prompt, n_predict, arrets)
        sortie[nom] = {"texte": r["texte"], "arret": r["arret"],
                       "tokens_generes": r["tokens_generes"]}
        print(f"   arrets « {nom} » : arret={r['arret']!r}, "
              f"{r['tokens_generes']} tokens generes", flush=True)
        print("      " + r["texte"].replace("\n", " | "), flush=True)
    sortie["identiques"] = sortie["union"]["texte"] == sortie["chatml seul"]["texte"]
    print(f"   les deux sorties sont identiques : {sortie['identiques']}", flush=True)
    return sortie


def run(items, table, familles_par_item, fin_ts, fin_dt, args, smoke=False):
    """Un seul serveur, une seule condition, trace ecrite au fil de l'eau."""
    suffixe = "smoke" if smoke else ""
    journal = JOURNAL_SMOKE if smoke else JOURNAL
    R1.JOURNAL_RUN = journal
    info = MODELES[CLE]
    depart = datetime.datetime.now()
    resume, moteur, sonde = None, None, None
    try:
        port = args.port or premier_port_libre()
        if not port_libre(port):
            sys.exit(f"le port {port} est occupe, un llama-server tourne peut etre deja")
        print(f"[{CLE}] {info['nom']} ({info['type']}), {info['quantification']}, "
              f"gabarit {info['gabarit']}, port {port}", flush=True)
        journaliser(f"lancement du serveur pour {CLE} ({info['nom']}) sur {port}", journal)
        moteur = R1.MoteurR1(os.path.join(GGUF, info["fichier"]),
                             contexte=args.contexte, parallele=args.parallele,
                             port=port, cache_kv_8bits=True)
        moteur.demarrer()
        print(f"[{CLE}] serveur pret en {moteur.chargement_s:.1f} s", flush=True)
        journaliser(f"[{CLE}] serveur pret en {moteur.chargement_s:.1f} s", journal)

        if smoke:
            print(f"[{CLE}] sonde des sequences d'arret, deux appels hors plan", flush=True)
            sonde = sonde_arrets(moteur, items, table, args.n_predict)

        resume = R1.lancer(moteur, CLE, info, items, table, familles_par_item,
                           R1.CAMPS, R1.IDENTITES, fin_ts, suffixe,
                           limite=args.limite, n_predict=args.n_predict,
                           sans_relance=args.sans_relance)
        resume["port"] = port
        resume["chargement_s"] = round(moteur.chargement_s, 1)
        resume["type"] = info["type"]
        resume["version_prompt"] = VERSION_PROMPT
        print(f"[{CLE}] {resume['cellules']} cellules en "
              f"{resume['secondes'] / 60:.1f} min, {resume['cellules_par_heure']:,.0f}/h, "
              f"{resume['rejets']} rejets, taux {resume['taux_rejet']:.4f}"
              .replace(",", " "), flush=True)
        journaliser(f"[{CLE}] termine : {resume['cellules']} cellules, "
                    f"{resume['cellules_par_heure']:.0f}/h, {resume['rejets']} rejets, "
                    f"taux de rejet {resume['taux_rejet']:.4f}, sans relance "
                    f"{args.sans_relance}", journal)
    except KeyboardInterrupt:
        journaliser("interrompu au clavier, arret propre", journal)
        raise
    except Exception as exc:
        print(f"[{CLE}] ECHEC : {type(exc).__name__} : {exc}", flush=True)
        journaliser(f"[{CLE}] ECHEC : {type(exc).__name__} : {exc}", journal)
        raise
    finally:
        if moteur is not None:
            moteur.arreter()
            print(f"[{CLE}] serveur arrete. charge {os.getloadavg()}", flush=True)
            journaliser("serveur arrete", journal)
        chemin = os.path.join(TRACES, "r5-resume" + ("-smoke" if smoke else "") + ".json")
        with open(chemin, "w", encoding="utf-8") as fh:
            json.dump({
                "depart": depart.isoformat(), "fin": datetime.datetime.now().isoformat(),
                "fin_dure": fin_dt.isoformat(), "version_prompt": VERSION_PROMPT,
                "gabarit": GABARIT, "suffixe": SUFFIXE, "essai_a_blanc": smoke,
                "sans_relance": args.sans_relance, "arrets": ARRETS,
                "n_predict": args.n_predict, "contexte": args.contexte,
                "parallele": args.parallele,
                "items": len(items), "conditions": [resume] if resume else [],
                "sonde_arrets": sonde,
                "exemples": R4.EXEMPLES,
            }, fh, indent=2, ensure_ascii=False)
        print(f"resume ecrit : {chemin}", flush=True)
        fin_message = (f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S} "
                       f"({resume['cellules'] if resume else 0} cellules)")
        print(fin_message, flush=True)
        journaliser(fin_message, journal)
    return resume


# --------------------------------------------------------------------------------------
# 5. L'evaluation : r1_evaluer.py --suffixe r5
# --------------------------------------------------------------------------------------

def copier_comparaisons():
    """Copie les trois conditions deja jouees sous le suffixe r5, octet pour octet.

    Aucun appel de modele n'est refait, aucune ligne n'est modifiee, les fichiers d'origine
    ne sont jamais touches. Elles existent pour que l'evaluateur voie les quatre conditions
    dans le meme tableau, exactement comme R4 l'avait fait pour la copie de `q4`.
    """
    faits = []
    for cle, nom in COMPARAISONS.items():
        source = os.path.join(TRACES, nom)
        cible = os.path.join(TRACES, f"r1-{cle}-{SUFFIXE}.jsonl")
        if not os.path.exists(source):
            print(f"condition {cle} absente : {source}", flush=True)
            continue
        if not (os.path.exists(cible) and sha256(cible) == sha256(source)):
            shutil.copyfile(source, cible)
        h = sha256(cible)
        print(f"copie {source} -> {cible}, sha256 {h}", flush=True)
        journaliser(f"copie de la condition {cle} : {cible}, sha256 {h}")
        faits.append(cible)
    return faits


def evaluer(argv_supplementaire=()):
    """Appelle r1_evaluer.main() avec --suffixe r5.

    Ce module a deja injecte `q4gab3` dans le registre de R1 ; l'evaluateur, qui lit ce
    registre pour sa figure, reconnait donc la condition. Les tableaux, eux, n'ont jamais eu
    besoin du registre.
    """
    import r1_evaluer
    copier_comparaisons()
    ancien = sys.argv
    sys.argv = ["r1_evaluer.py", "--suffixe", SUFFIXE] + list(argv_supplementaire)
    try:
        r1_evaluer.main()
    finally:
        sys.argv = ancien


# --------------------------------------------------------------------------------------
# 6. Les trois contrastes apparies de la page de plan
# --------------------------------------------------------------------------------------
# La quantite est celle des hypotheses : le facteur H2b, ecart signe entre camps decrit
# rapporte a l'ecart reel, sur les 79 items orientes, identite journaliste. C'est la
# quantite dont la page de plan cite les valeurs, `q4nogab` 0,727 et `q4` 0,245.
#
# Trois tests, et trois seulement, dans la famille de Holm :
#   T1  q4gab3 contre q4        : la marche que les exemples ajoutent au gabarit.
#   T2  q4gab3 contre q4nogab   : la marche que le gabarit retire aux exemples.
#   T3  q4gab3 contre le milieu : la position entre les deux, qui tranche le pari.
#
# Tout le reste (identite adverse, 65 items stricts, ratio H1, condition q4base) est
# descriptif, publie sans p corrige, et declare comme tel.

GRAINE = 20260909
N_BOOT = 2000
N_PERM = 20000
BANDE = 0.15          # la demi largeur des bandes H1 et H2 de la page de plan


def p_permutation_signe(d, rng, n=N_PERM):
    """p bilateral d'une difference appariee par item, permutation de signe, Phipson Smyth."""
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 3:
        return float("nan")
    obs = abs(d.mean())
    signes = rng.choice([-1.0, 1.0], size=(n, len(d)))
    stat = np.abs((signes * d[None, :]).mean(axis=1))
    return float((int((stat >= obs - 1e-15).sum()) + 1.0) / (n + 1.0))


def ic_difference_de_facteurs(a, b, ref, rng, n=N_BOOT):
    """IC bootstrap sur les items de (moyenne(a) - moyenne(b)) / moyenne(ref).

    Definition de `r4b_contrastes.py`, reprise sans changement pour que les chiffres de R5
    se lisent dans la meme unite que ceux de R4 section 2.1. L'unite de reechantillonnage
    est l'item ; les trois series sont tirees ensemble.
    """
    a, b, ref = (np.asarray(x, float) for x in (a, b, ref))
    m = np.isfinite(a) & np.isfinite(b) & np.isfinite(ref)
    a, b, ref = a[m], b[m], ref[m]
    if len(a) < 3 or ref.mean() == 0:
        return (float("nan"),) * 3 + (int(len(a)),)
    obs = float((a.mean() - b.mean()) / ref.mean())
    idx = rng.integers(0, len(a), size=(n, len(a)))
    t = (a[idx].mean(axis=1) - b[idx].mean(axis=1)) / ref[idx].mean(axis=1)
    t = t[np.isfinite(t)]
    return obs, float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5)), int(len(a))


def facteur(a, ref):
    a, ref = np.asarray(a, float), np.asarray(ref, float)
    return float(a.mean() / ref.mean())


def _table_h2b(eca, filtre, identite):
    """{condition : DataFrame indexe par item}, sur un perimetre d'items et une identite."""
    g = eca[eca["identite"] == identite]
    g = g[g["item"].map(lambda i: bool(filtre.get(i, False)))]
    return {c: g[g["cle_modele"] == c].set_index("item") for c in ORDRE_CONDITIONS
            if len(g[g["cle_modele"] == c])}


def contrastes(eca, cel, oriente, strict, rng):
    """Les trois tests de la page de plan, plus les quantites descriptives."""
    from a28_commun import holm

    lignes, principaux = [], []
    perimetres = (("79 items orientes", oriente), ("65 items retenus stricts", strict))
    for nom_per, filtre in perimetres:
        for identite in ("journaliste", "adversaire"):
            tab = _table_h2b(eca, filtre, identite)
            if CLE not in tab:
                continue
            # Perimetre apparie : un item sort du contraste si une des deux conditions
            # comparees le rejette. Page de plan, section « Relance ».
            for nom_test, cible in (("T1, q4gab3 contre q4", "q4"),
                                    ("T2, q4gab3 contre q4nogab", "q4nogab"),
                                    ("hors famille, q4gab3 contre q4base", "q4base")):
                if cible not in tab:
                    continue
                communs = sorted(set(tab[CLE].index) & set(tab[cible].index))
                if len(communs) < 3:
                    continue
                a = tab[CLE].loc[communs, "gap_signe_decrit"].to_numpy()
                b = tab[cible].loc[communs, "gap_signe_decrit"].to_numpy()
                ref = tab[CLE].loc[communs, "gap_signe_reel_w1"].to_numpy()
                dif, bas, haut, n = ic_difference_de_facteurs(a, b, ref, rng)
                ligne = {
                    "test": nom_test, "quantite": "facteur H2b, ecart signe entre camps",
                    "perimetre": nom_per, "identite": identite,
                    "condition_a": CLE, "condition_b": cible, "n_items": n,
                    "facteur_a": facteur(a, ref), "facteur_b": facteur(b, ref),
                    "difference_de_facteurs": dif, "ic_bas": bas, "ic_haut": haut,
                    "p": p_permutation_signe(a - b, rng),
                    "hors_bande_0_15": bool(np.isfinite(dif) and abs(dif) > BANDE),
                }
                lignes.append(ligne)
                if (nom_per == "79 items orientes" and identite == "journaliste"
                        and cible in ("q4", "q4nogab")):
                    principaux.append(ligne)

            # T3, la position entre les deux : contraste contre le milieu du segment.
            if "q4" in tab and "q4nogab" in tab:
                communs = sorted(set(tab[CLE].index) & set(tab["q4"].index)
                                 & set(tab["q4nogab"].index))
                if len(communs) >= 3:
                    a = tab[CLE].loc[communs, "gap_signe_decrit"].to_numpy()
                    b0 = tab["q4"].loc[communs, "gap_signe_decrit"].to_numpy()
                    b1 = tab["q4nogab"].loc[communs, "gap_signe_decrit"].to_numpy()
                    ref = tab[CLE].loc[communs, "gap_signe_reel_w1"].to_numpy()
                    milieu = 0.5 * (b0 + b1)
                    dif, bas, haut, n = ic_difference_de_facteurs(a, milieu, ref, rng)
                    # Position relative sur le segment q4 -> q4nogab, en facteurs.
                    x0, x1, xa = facteur(b0, ref), facteur(b1, ref), facteur(a, ref)
                    lam = (xa - x0) / (x1 - x0) if x1 != x0 else float("nan")
                    idx = rng.integers(0, len(a), size=(N_BOOT, len(a)))
                    t = ((a[idx].mean(axis=1) - b0[idx].mean(axis=1))
                         / (b1[idx].mean(axis=1) - b0[idx].mean(axis=1)))
                    t = t[np.isfinite(t)]
                    lam_bas = float(np.percentile(t, 2.5)) if len(t) > 10 else float("nan")
                    lam_haut = float(np.percentile(t, 97.5)) if len(t) > 10 else float("nan")
                    ligne = {
                        "test": "T3, q4gab3 contre le milieu de q4 et q4nogab",
                        "quantite": "facteur H2b, ecart signe entre camps",
                        "perimetre": nom_per, "identite": identite,
                        "condition_a": CLE, "condition_b": "milieu(q4, q4nogab)",
                        "n_items": n,
                        "facteur_a": xa, "facteur_b": 0.5 * (x0 + x1),
                        "difference_de_facteurs": dif, "ic_bas": bas, "ic_haut": haut,
                        "p": p_permutation_signe(a - milieu, rng),
                        "hors_bande_0_15": bool(np.isfinite(dif) and abs(dif) > BANDE),
                        "position_lambda": lam, "lambda_ic_bas": lam_bas,
                        "lambda_ic_haut": lam_haut,
                    }
                    lignes.append(ligne)
                    if nom_per == "79 items orientes" and identite == "journaliste":
                        principaux.append(ligne)

    # Le ratio H1, descriptif, meme forme de contraste.
    ok = cel[~cel["rejet"]]
    for camp in ("gauche", "centre", "droite"):
        for identite in ("journaliste", "adversaire"):
            g = ok[(ok["camp"] == camp) & (ok["identite"] == identite)]
            ta = g[g["cle_modele"] == CLE].set_index("item")
            if not len(ta):
                continue
            for cible in ("q4", "q4nogab", "q4base"):
                tb = g[g["cle_modele"] == cible].set_index("item")
                communs = sorted(set(ta.index) & set(tb.index))
                if len(communs) < 3:
                    continue
                a = ta.loc[communs, "gs_decrit"].to_numpy()
                b = tb.loc[communs, "gs_decrit"].to_numpy()
                ref = ta.loc[communs, "gs_reel_w1"].to_numpy()
                dif, bas, haut, n = ic_difference_de_facteurs(a, b, ref, rng)
                lignes.append({
                    "test": f"descriptif, ratio H1 camp {camp}, q4gab3 contre {cible}",
                    "quantite": "ratio H1, dispersion interne",
                    "perimetre": f"camp {camp}", "identite": identite,
                    "condition_a": CLE, "condition_b": cible, "n_items": n,
                    "facteur_a": facteur(a, ref), "facteur_b": facteur(b, ref),
                    "difference_de_facteurs": dif, "ic_bas": bas, "ic_haut": haut,
                    "p": p_permutation_signe(a - b, rng),
                    "hors_bande_0_15": bool(np.isfinite(dif) and abs(dif) > BANDE),
                })

    d = pd.DataFrame(lignes)
    d["p_holm"] = np.nan
    d["famille_de_holm"] = False
    if len(principaux) == 3:
        ps = holm([l["p"] for l in principaux])
        for l, pa in zip(principaux, ps):
            m = ((d["test"] == l["test"]) & (d["perimetre"] == l["perimetre"])
                 & (d["identite"] == l["identite"]))
            d.loc[m, "p_holm"] = float(pa)
            d.loc[m, "famille_de_holm"] = True
    else:
        print(f"ATTENTION : {len(principaux)} tests principaux au lieu de 3, "
              "Holm n'est pas applique", flush=True)
    return d


def tableau_conditions(eca, cel, oriente, strict, rng):
    """Le tableau des quatre conditions, sur les quantites du rapport."""
    lignes = []
    for nom_per, filtre in (("79 items orientes", oriente),
                            ("65 items retenus stricts", strict)):
        for identite in ("journaliste", "adversaire"):
            tab = _table_h2b(eca, filtre, identite)
            for cle in ORDRE_CONDITIONS:
                if cle not in tab:
                    continue
                g = tab[cle]
                a = g["gap_signe_decrit"].to_numpy()
                ref = g["gap_signe_reel_w1"].to_numpy()
                lignes.append({
                    "condition": cle, "libelle": LIBELLES[cle],
                    "quantite": "facteur H2b, ecart signe entre camps",
                    "perimetre": nom_per, "identite": identite, "n_items": len(g),
                    "valeur": facteur(a, ref),
                })
    ok = cel[~cel["rejet"]]
    for camp in ("gauche", "centre", "droite"):
        for identite in ("journaliste", "adversaire"):
            for cle in ORDRE_CONDITIONS:
                g = ok[(ok["camp"] == camp) & (ok["identite"] == identite)
                       & (ok["cle_modele"] == cle)]
                if not len(g):
                    continue
                lignes.append({
                    "condition": cle, "libelle": LIBELLES[cle],
                    "quantite": "ratio H1, dispersion interne",
                    "perimetre": f"camp {camp}", "identite": identite, "n_items": len(g),
                    "valeur": facteur(g["gs_decrit"].to_numpy(),
                                      g["gs_reel_w1"].to_numpy()),
                })
                lignes.append({
                    "condition": cle, "libelle": LIBELLES[cle],
                    "quantite": "erreur TV(decrit, reel) en part du plancher humain",
                    "perimetre": f"camp {camp}", "identite": identite, "n_items": len(g),
                    "valeur": float(g["tv_decrit_reel"].mean()
                                    / g["tv_plancher_w1_w2"].mean()),
                })
    return pd.DataFrame(lignes)


def rejets_par_condition():
    """Le taux de rejet de chaque condition, lu directement dans les traces.

    Trois quantites distinctes, qu'il ne faut jamais melanger : l'echec de PREMIERE
    tentative, comparable entre les quatre conditions ; le rejet APRES relance, qui n'existe
    que pour les trois conditions jouees avec relance ; et le retrait au critere de chute 2,
    la recopie de l'exemple de relance, qui ne peut pas exister sans relance.
    """
    lignes = []
    for cle in ORDRE_CONDITIONS:
        chemin = (chemin_trace(cle, "") if cle in MODELES
                  else os.path.join(TRACES, f"r1-{cle}-{SUFFIXE}.jsonl"))
        if not os.path.exists(chemin):
            continue
        n = premier = final = relances_ok = copies = 0
        motifs = collections.Counter()
        sans_relance = None
        for ligne in open(chemin, encoding="utf-8"):
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            n += 1
            sans_relance = d.get("sans_relance", False)
            tentatives = d.get("tentatives") or []
            if tentatives and tentatives[0].get("motif_rejet"):
                premier += 1
                motifs[tentatives[0]["motif_rejet"].split(" :")[0][:40]] += 1
            if d.get("rejet"):
                final += 1
            elif len(tentatives) > 1:
                relances_ok += 1
                if d.get("distribution") and R1_recopie(d["distribution"]):
                    copies += 1
        lignes.append({
            "condition": cle, "libelle": LIBELLES[cle], "sans_relance": bool(sans_relance),
            "cellules": n,
            "echecs_premiere_tentative": premier,
            "taux_premiere_tentative": premier / n if n else float("nan"),
            "rejets_finals": final, "taux_rejet_final": final / n if n else float("nan"),
            "relances_rattrapees": relances_ok,
            "recopies_de_l_exemple_de_relance": copies,
            "motifs": json.dumps(dict(motifs), ensure_ascii=False),
            "trace": os.path.basename(chemin),
        })
    return pd.DataFrame(lignes)


def R1_recopie(distribution):
    import r1_evaluer
    return r1_evaluer.recopie_exemple(distribution)


def lancer_contrastes():
    rng = np.random.default_rng(GRAINE)
    cel = pd.read_csv(os.path.join(SORTIE, f"r1-par-cellule-{SUFFIXE}.csv"))
    eca = pd.read_csv(os.path.join(SORTIE, f"r1-par-item-ecarts-{SUFFIXE}.csv"))
    o = pd.read_csv(os.path.join(SORTIE, "a37-orientation-items.csv"))
    dd = pd.read_csv(os.path.join(SORTIE, "a37-gss-par-item.csv"))
    oriente = dict(zip(o["item"], o["oriente"].astype(bool)))
    strict = dict(zip(dd["item"], dd["retenu_strict"].astype(bool)))

    con = contrastes(eca, cel, oriente, strict, rng)
    tab = tableau_conditions(eca, cel, oriente, strict, rng)
    rej = rejets_par_condition()

    for df, nom in ((con, "r5-contrastes"), (tab, "r5-tableau"), (rej, "r5-rejets")):
        chemin = os.path.join(SORTIE, f"{nom}.csv")
        df.to_csv(chemin, index=False)
        print(f"ecrit {chemin}  {len(df)} lignes", flush=True)

    pd.set_option("display.width", 220, "display.max_columns", 40)
    print("\n--- taux de rejet par condition ---")
    print(rej[["condition", "sans_relance", "cellules", "echecs_premiere_tentative",
               "taux_premiere_tentative", "rejets_finals", "taux_rejet_final",
               "recopies_de_l_exemple_de_relance"]].to_string(index=False))
    print("\n--- les trois tests, 79 items orientes, journaliste ---")
    m = con["famille_de_holm"]
    print(con[m][["test", "n_items", "facteur_a", "facteur_b", "difference_de_facteurs",
                  "ic_bas", "ic_haut", "hors_bande_0_15", "p", "p_holm",
                  "position_lambda" if "position_lambda" in con else "p"]]
          .to_string(index=False))
    print("\n--- facteur H2b des quatre conditions ---")
    print(tab[tab["quantite"] == "facteur H2b, ecart signe entre camps"]
          [["condition", "perimetre", "identite", "n_items", "valeur"]]
          .to_string(index=False))
    print("\n--- tous les contrastes ---")
    print(con[["test", "perimetre", "identite", "n_items", "facteur_a", "facteur_b",
               "difference_de_facteurs", "ic_bas", "ic_haut", "p", "p_holm"]]
          .to_string(index=False))
    return con, tab, rej


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--items", type=int, default=0,
                    help="0 pour les 149 items, n pour les n premiers")
    ap.add_argument("--fin", default="23:59", help="fin dure du calcul, heure locale")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal de cellules, pour l'essai a blanc")
    ap.add_argument("--n-predict", type=int, default=R1.N_PREDICT)
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--contexte", type=int, default=4096)
    ap.add_argument("--parallele", type=int, default=1,
                    help="-np. 1 comme en R1 et R4 : a3 4.3 mesure que -np 1 ne coute que "
                         "2 pour cent de debit et rend 8 Gio de memoire")
    ap.add_argument("--avec-relance", action="store_true",
                    help="retablit la relance de R1. Le defaut de R5 est sans relance, "
                         "conduite preenregistree.")
    ap.add_argument("--verifier", action="store_true",
                    help="verification hors ligne, aucun serveur, aucun appel")
    ap.add_argument("--smoke", action="store_true",
                    help="essai a blanc : 3 cellules dans data/traces/r5-smoke.jsonl")
    ap.add_argument("--evaluer", action="store_true",
                    help="appelle r1_evaluer.py --suffixe r5")
    ap.add_argument("--contrastes", action="store_true",
                    help="les trois contrastes apparies de la page de plan")
    ap.add_argument("--sans-figure", action="store_true")
    args = ap.parse_args()
    args.sans_relance = not args.avec_relance

    os.makedirs(TRACES, exist_ok=True)

    if args.evaluer:
        evaluer(["--sans-figure"] if args.sans_figure else [])
        return
    if args.contrastes:
        lancer_contrastes()
        return

    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    if args.items:
        items = items[:args.items]
    familles_par_item = {it: nom for nom, membres in FAMILLES.items() for it in membres}

    if args.verifier:
        defauts = verifier(items, table)
        sys.exit(1 if defauts else 0)

    chemin_poids = os.path.join(GGUF, MODELES[CLE]["fichier"])
    if not os.path.exists(chemin_poids):
        sys.exit(f"modele introuvable : {chemin_poids}")

    # Critere de chute : le referent humain de R1 doit etre celui de R1.
    if not os.path.exists(REFERENT):
        sys.exit(f"referent humain absent : {REFERENT}")
    h = sha256(REFERENT)
    if h != REFERENT_SHA:
        sys.exit(f"le referent humain a change : {h} au lieu de {REFERENT_SHA}. "
                 "Critere de chute, rien n'est publie.")

    if args.smoke:
        args.limite = args.limite or 3
    else:
        # Le run complet ne demarre que si le fichier GO existe : la page de plan doit
        # etre deposee hors de la machine avant le premier appel.
        go = os.path.join(TRACES, "GO-R5")
        if not os.path.exists(go):
            sys.exit(f"le fichier {go} n'existe pas : le run complet n'est pas autorise. "
                     "L'essai a blanc, lui, se lance avec --smoke.")

    R1.VERSION_PROMPT = VERSION_PROMPT
    journal = JOURNAL_SMOKE if args.smoke else JOURNAL
    R1.JOURNAL_RUN = journal

    fin_ts, fin_dt = heure_de_fin(args.fin)
    depart = datetime.datetime.now()
    n = len(items) * len(R1.CAMPS) * len(R1.IDENTITES)
    entete = (f"popsim r5, gabarit ChatML ET trois exemples"
              + (" [ESSAI A BLANC]" if args.smoke else "")
              + f". Depart {depart:%Y-%m-%d %H:%M:%S}, fin dure {fin_dt:%Y-%m-%d %H:%M} "
                f"({(fin_ts - time.time()) / 3600:.2f} h). Condition {CLE}. "
                f"Version d'invite {VERSION_PROMPT}, gabarit {GABARIT}, "
                f"sans relance {args.sans_relance}.")
    print(entete, flush=True)
    journaliser("DEBUT " + entete, journal)
    print(f"charge machine : {os.getloadavg()}", flush=True)

    defauts = verifier(items, table, bavard=False)
    if defauts:
        for d in defauts:
            journaliser("DEFAUT " + d, journal)
        sys.exit("la verification hors ligne echoue : " + " ; ".join(defauts))
    journaliser("verification hors ligne : aucun defaut", journal)

    print(f"{n} cellules au plan"
          + (f", limite a {args.limite}" if args.limite else ""), flush=True)
    print(f"referent humain reutilise : {REFERENT}, sha256 {h}", flush=True)

    run(items, table, familles_par_item, fin_ts, fin_dt, args, smoke=args.smoke)


if __name__ == "__main__":
    main()
