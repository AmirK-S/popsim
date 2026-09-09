"""
r2_rares_apparie : la comparaison appariee sur les gens rares, en regime severe.

Verrou 1 de MODELE-DU-MONDE.md section 10.5. La page de plan est
resultats/r2-preenregistrement.md, horodatee du 8 septembre 2026 a 22:05:00 CEST, ecrite
AVANT le moindre appel de modele de langage, et non modifiee ensuite.

Ce que fait ce script. Il rejoue la condition C3F de a5 (le contexte perd la famille
thematique entiere de l'item cible, et c'est cette famille qui est predite) puis la
condition C3 (le contexte garde les cousins) sur les MEMES 150 personnes et les MEMES
58 items de famille, avec un modele plus gros dont la coupure est publiee, gpt-oss-20b
MXFP4, juin 2024. C'est la seule comparaison du dossier ou le regime severe est impose
des deux cotes a la fois : aux methodes statistiques par a35_familles, au jumeau de
langage par le retrait de la famille de son invite.

AUCUN SCRIPT EXISTANT N'EST MODIFIE. Tout ce qui fait le prompt, le decoupage et le
scoring est importe de analyses/a5_agents_locaux_gss.py : nomenclature(), systeme_c3(),
utilisateur(), echantillon(), groupes_familles(), gabarit_qwen(), MoteurA5, LETTRES,
SEUIL_MASSE, heure_de_fin(), port_libre(), premier_port_libre(). a5 met son chemin de
modele en dur, lignes 81 et 95 ; ici le modele est un drapeau, --modele, et le gabarit de
conversation suit le modele. La seule fonction de a5 reecrite ici est la lecture des
lettres, parce qu'elle suppose chez a5 que la lettre est precedee d'une espace, ce qui
n'est vrai que pour une des deux variantes de fin de prompt.

Ce qui change par rapport a a5, et rien d'autre :
  1. le modele, et donc le gabarit de conversation (harmony pour gpt-oss, Qwen sinon) ;
  2. le perimetre d'items de C3 : les 58 items de famille seulement, pour que C3 et C3F
     soient apparies cellule a cellule ;
  3. un smoke test integre de 20 appels au demarrage, qui arrete le run si la masse de
     probabilite portee par les lettres est trop basse ;
  4. un refus de demarrer si un llama-server tourne deja sur la machine.

Le point 3 n'est pas une precaution de principe. a3 section 4.5 mesure que gpt-oss-20b
interroge sans son gabarit ne place que 3,2 pour cent de sa masse sur les lettres de
reponse, et 99,93 pour cent des qu'on le lui applique. Une nuit entiere d'appels a
3,2 pour cent de masse serait une nuit perdue et un fichier de bruit renormalise. Le
point 4 vaut un facteur 9,5 sur le debit, mesure en a5 section 4.4.

Conditions :
  C3F  contexte = les 149 items moins TOUTE la famille de l'item cible, 132 a 144 items,
       et ce sont les 5 a 17 items de la famille qui sont predits. Six prefixes par
       personne, 58 appels. Regime de a8_familles.py et de a35_familles.py.
  C3   contexte = les 119 items du bloc de a2, cousins compris. Cinq prefixes par
       personne, et seuls les items de famille du bloc sont predits, 58 au total.

Entree  : data/osf-t6g7k-stanford, non versionne. data/traces/a5-personnes.csv s'il
          existe, sinon le meme echantillon est retire de la meme graine.
Sortie  : data/traces/r2-<condition>-<modele>.jsonl, une ligne par appel, meme format
          que a5. data/traces/r2-run.log, r2-run.pid, r2-resume-<modele>.json,
          r2-smoke-<modele>.jsonl.

Rien ne sort de la machine. Aucun appel distant. La trace ne contient PAS la vraie
reponse de la personne : l'evaluateur la relit dans data/, position de METHODOLOGIE.

Reprise : l'index unique est (condition, pid, item), lu dans la trace. Une relance ne
refait aucun appel deja ecrit. L'ordre est personne par personne : une troncature a
08:00 coute des personnes entieres, jamais des items.

Usage :
  .venv/bin/python analyses/r2_rares_apparie.py --fin 08:00
  .venv/bin/python analyses/r2_rares_apparie.py --modele qwen30 --fin 08:00
  .venv/bin/python analyses/r2_rares_apparie.py --verification-seule
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

from a2_baselines_gss import charger, grille, GRAINE, N_BLOCS, N_PLIS
from a5_agents_locaux_gss import (LETTRES, SEUIL_MASSE, TRACES, MoteurA5, echantillon,
                                  gabarit_qwen, groupes_familles, heure_de_fin,
                                  nomenclature, port_libre, premier_port_libre,
                                  systeme_c3, utilisateur)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GGUF = os.path.join(RACINE, "data/modeles/gguf")

# ---------------------------------------------------------------------------
# Registre des modeles. La coupure est celle que l'auteur PUBLIE, jamais une
# coupure verifiee : a3 section 2 rappelle que personne ne les a auditees.
# ---------------------------------------------------------------------------
MODELES = {
    "gptoss": {
        "fichier": os.path.join(GGUF, "gpt-oss-20b-MXFP4.gguf"),
        "nom": "gpt-oss-20b",
        "quantification": "MXFP4",
        "gabarit": "harmony",
        "coupure_publiee": "juin 2024",
        "source_coupure": "arXiv 2508.10925, carte de modele OpenAI",
    },
    "qwen30": {
        "fichier": os.path.join(GGUF, "Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf"),
        "nom": "Qwen3-30B-A3B-Instruct-2507",
        "quantification": "Q4_K_M",
        "gabarit": "qwen",
        "coupure_publiee": "aucune",
        "source_coupure": "carte de modele, rapport technique et documentation muets",
    },
    "qwen4": {
        "fichier": os.path.join(GGUF, "Qwen3-4B-Instruct-2507-Q4_K_M.gguf"),
        "nom": "Qwen3-4B-Instruct-2507",
        "quantification": "Q4_K_M",
        "gabarit": "qwen",
        "coupure_publiee": "aucune",
        "source_coupure": "carte de modele, rapport technique et documentation muets",
    },
}

# Le seuil du smoke test est BEAUCOUP plus haut que le seuil de rejet par appel de a5,
# qui vaut 0,50. Motif : un appel isole peut tomber bas sans que le protocole soit en
# panne, alors qu'une mediane basse sur vingt appels signale un gabarit faux, et c'est
# exactement la panne que a3 section 4.5 a prise sur le fait.
SEUIL_SMOKE_MEDIANE = 0.90
SEUIL_SMOKE_MINIMUM = 0.50
PART_ABSENTES_MAX = 0.25
N_SMOKE = 20

GRAINE_ECHANTILLON = 20260907

_journal_fh = None


def journal(texte=""):
    """Ecrit sur la sortie standard ET dans data/traces/r2-run.log.

    Le fichier est ouvert en ajout : une reprise apres arret brutal ne perd pas le
    journal du premier passage, et la file de nuit surveille la ligne RUN TERMINE dans
    ce fichier quel que soit le mode de lancement.

    La file de nuit redirige deja la sortie standard vers ce meme fichier. Quand c'est
    le cas, le second handle est ferme au demarrage et chaque ligne n'est ecrite qu'une
    fois : sans cette verification le journal serait double, et un lecteur pourrait
    croire que le run a fait deux fois le meme travail.
    """
    print(texte, flush=True)
    if _journal_fh is not None:
        _journal_fh.write(texte + "\n")
        _journal_fh.flush()


def sortie_est_deja(chemin):
    """La sortie standard est elle deja ce fichier la ? Compare inode et peripherique."""
    try:
        a = os.fstat(sys.stdout.fileno())
        b = os.stat(chemin)
    except (OSError, ValueError):
        return False
    return (a.st_dev, a.st_ino) == (b.st_dev, b.st_ino)


# ---------------------------------------------------------------------------
# 1. La machine : un seul llama-server a la fois
# ---------------------------------------------------------------------------

def serveurs_en_cours():
    """PID des llama-server en cours, par NOM de processus et non par ligne de commande.

    pgrep -f attraperait le script de surveillance de la file de nuit, dont la ligne de
    commande contient la chaine `llama-server`, et le run refuserait de demarrer pour
    rien. pgrep -x ne regarde que le nom de l'executable.
    """
    r = subprocess.run(["pgrep", "-x", "llama-server"], capture_output=True, text=True)
    return [int(p) for p in r.stdout.split() if p.strip().isdigit()]


# ---------------------------------------------------------------------------
# 2. Gabarits de conversation
# ---------------------------------------------------------------------------
#
# Deux variantes de fin de prompt, et le choix entre elles est MESURE au demarrage, pas
# suppose. a3 section 4.5 : le gabarit ne doit pas se terminer par une espace, sinon le
# modele hesite entre le token "D" et le token " D" et la masse tombe de 0,999 a 0,84.
# La variante "answer" est celle de a5 mot pour mot, le prompt s'arrete sur `Answer:` et
# c'est le token " A" qui est score. La variante "brut" s'arrete sur l'ouverture du tour
# assistant et c'est le token "A", sans espace, qui est score : c'est la forme exacte du
# gabarit harmony reproduit en a3 section 4.5.

VARIANTES = {"answer": " ", "brut": ""}


def gabarit_harmony(systeme, question, variante="answer"):
    """Gabarit harmony de gpt-oss, reproduit de a3 section 4.5.

    Le persona et la question sont dans le meme tour utilisateur, comme dans la mesure
    de a3 : c'est cette forme la qui a donne 0,9993 de masse, et changer la repartition
    entre tours changerait le prompt sans qu'aucune mesure ne le couvre.
    """
    fin = "Answer:" if variante == "answer" else ""
    return ("<|start|>system<|message|>Reasoning: low<|end|>\n"
            "<|start|>user<|message|>" + systeme + "\n\n" + question + "<|end|>\n"
            "<|start|>assistant<|channel|>final<|message|>" + fin)


def gabarit_qwen_variante(systeme, question, variante="answer"):
    """Gabarit Qwen. En variante `answer`, identique caractere pour caractere a a5."""
    if variante == "answer":
        return gabarit_qwen(systeme, question)
    return ("<|im_start|>system\n" + systeme + "<|im_end|>\n"
            "<|im_start|>user\n" + question + "<|im_end|>\n"
            "<|im_start|>assistant\n")


def construire_prompt(spec, systeme, question, variante):
    if spec["gabarit"] == "harmony":
        return gabarit_harmony(systeme, question, variante)
    return gabarit_qwen_variante(systeme, question, variante)


def tokens_des_lettres(moteur, prompt, n_lettres, prefixe):
    """Identifiant du token de chaque lettre, dans CE contexte gauche precis.

    Meme methode que MoteurA5.tokens_des_lettres, avec le prefixe en parametre : on
    encode `prompt`, puis `prompt + prefixe + lettre`, et on prend le token qui s'ajoute.
    On n'encode jamais la lettre isolement, parce que la tokenisation depend du contexte
    gauche. Leve si l'ajout modifie le prefixe, si la lettre fait plus d'un token, ou si
    deux lettres partagent un identifiant.
    """
    base = moteur.tokeniser(prompt)
    table = {}
    for lettre in LETTRES[:n_lettres]:
        etendu = moteur.tokeniser(prompt + prefixe + lettre)
        if etendu[:len(base)] != base:
            raise RuntimeError(f"l'ajout de '{prefixe}{lettre}' a modifie le prefixe")
        if len(etendu) != len(base) + 1:
            raise RuntimeError(f"'{prefixe}{lettre}' n'est pas un token unique dans ce "
                               f"contexte ({len(etendu) - len(base)} tokens)")
        table[lettre] = etendu[len(base)]
    if len(set(table.values())) != len(table):
        raise RuntimeError(f"identifiants de tokens non distincts : {table}")
    return table, len(base)


def masse_des_lettres_prefixe(top, ids_lettres, lettres, prefixe):
    """masse_des_lettres de a5, avec le repli par chaine adapte au prefixe choisi.

    La lettre est identifiee par l'identifiant de token quand le serveur le donne, et
    par la chaine exacte sinon. Jamais par un strip() : "A" colle et " A" precede d'une
    espace sont deux tokens differents et un seul des deux est celui qu'on a verifie. Le
    repli par chaine doit donc suivre la variante de fin de prompt : " A" en variante
    `answer`, "A" en variante `brut`. C'est la seule difference avec a5, et elle existe
    parce que a5 ne connait qu'une variante.
    """
    par_id = {e["id"]: e for e in top if "id" in e}
    brut = {}
    for lettre in lettres:
        e = par_id.get(ids_lettres[lettre])
        if e is None:
            e = next((x for x in top if x.get("token") == prefixe + lettre), None)
        brut[lettre] = float(np.exp(e["logprob"])) if e is not None else 0.0
    return brut


# ---------------------------------------------------------------------------
# 3. Enumeration des appels
# ---------------------------------------------------------------------------

def travaux_r2(condition, retenus, items, blocs, y1, table, cols_familles):
    """Enumere les appels, dans l'ordre qui maximise le cache de prefixe.

    C3F : le prompt systeme depend de la personne ET de la famille cible. Six prefixes
          par personne, 58 appels utiles. C'est la condition la plus chere par appel
          produit, et c'est celle que le regime severe impose.
    C3  : le prompt systeme depend de la personne ET du bloc secret, exactement comme en
          a5. Cinq prefixes par personne, mais seuls les items de FAMILLE du bloc sont
          predits, soit 58 appels au total au lieu de 149. C'est ce qui rend C3 et C3F
          apparies cellule a cellule.

    Produit des tuples (personne, etiquette de groupe, index d'item, prompt systeme).
    """
    tous = np.arange(len(items))
    cibles = set(cols_familles)
    for p in retenus:
        if condition == "C3F":
            for nom, cols in groupes_familles(items):
                contexte = np.setdiff1d(tous, cols)
                sys_txt = systeme_c3(contexte, y1[p["index"]], items, table)
                for j in cols:
                    yield p, nom, int(j), sys_txt
        elif condition == "C3":
            for i_bloc, bloc in enumerate(blocs):
                dedans = [int(j) for j in bloc if int(j) in cibles]
                if not dedans:
                    continue
                contexte = np.setdiff1d(tous, bloc)
                sys_txt = systeme_c3(contexte, y1[p["index"]], items, table)
                for j in dedans:
                    yield p, i_bloc, j, sys_txt
        else:
            raise SystemExit(f"condition inconnue : {condition}")


def chemin_trace(condition, cle_modele, suffixe=""):
    nom = f"r2-{condition}-{cle_modele}"
    if suffixe:
        nom += "-" + suffixe
    return os.path.join(TRACES, nom + ".jsonl")


def index_existant(chemin):
    """Cle (pid, item) des appels deja ecrits. Une relance ne les refait pas.

    Les lignes tronquees par un arret brutal sont ignorees sans faire echouer la
    reprise : la derniere ligne d'un fichier interrompu en cours d'ecriture est souvent
    incomplete. Meme convention que a5.
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
            if "pid" in d and "item" in d:
                fait.add((d["pid"], d["item"]))
    return fait


# ---------------------------------------------------------------------------
# 4. Le verdict du smoke test, fonction pure pour etre testable hors ligne
# ---------------------------------------------------------------------------

def verdict_smoke(masses, parts_absentes, n_attendu=N_SMOKE):
    """Le run peut il continuer ? Trois criteres, tous ecrits dans la page de plan.

    masses         : masse de probabilite portee par les K lettres, avant renormalisation.
    parts_absentes : nombre d'appels ou au moins une modalite manquait du top 40.

    Renvoie (verdict booleen, dictionnaire de mesures, motif lisible).
    """
    m = np.asarray([x for x in masses if np.isfinite(x)], dtype=float)
    mesures = {
        "appels": int(len(m)),
        "masse_mediane": float(np.median(m)) if len(m) else float("nan"),
        "masse_minimale": float(m.min()) if len(m) else float("nan"),
        "masse_moyenne": float(m.mean()) if len(m) else float("nan"),
        "part_modalites_absentes": (float(parts_absentes) / len(m)) if len(m) else 1.0,
        "seuil_mediane": SEUIL_SMOKE_MEDIANE,
        "seuil_minimum": SEUIL_SMOKE_MINIMUM,
        "part_absentes_max": PART_ABSENTES_MAX,
    }
    if len(m) < n_attendu:
        return False, mesures, (f"arret : masse non mesurable, {len(m)} appels exploitables "
                                f"sur {n_attendu} attendus")
    if mesures["masse_mediane"] < SEUIL_SMOKE_MEDIANE:
        return False, mesures, (f"arret : masse mediane {mesures['masse_mediane']:.4f} "
                                f"sous le seuil {SEUIL_SMOKE_MEDIANE}")
    if mesures["masse_minimale"] < SEUIL_SMOKE_MINIMUM:
        return False, mesures, (f"arret : masse minimale {mesures['masse_minimale']:.4f} "
                                f"sous le seuil de rejet {SEUIL_SMOKE_MINIMUM}")
    if mesures["part_modalites_absentes"] > PART_ABSENTES_MAX:
        return False, mesures, (f"arret : masse repartie hors des lettres, "
                                f"{mesures['part_modalites_absentes']:.2f} d'appels a "
                                f"modalite absente du top 40")
    return True, mesures, "smoke test passe"


# ---------------------------------------------------------------------------
# 5. Un appel, et la ligne de trace
# ---------------------------------------------------------------------------

def un_appel(moteur, variante, prompt, options, ids_lettres):
    """Un passage avant, la lecture des lettres, la renormalisation. Scoring de a5."""
    prefixe = VARIANTES[variante]
    k = len(options)
    lettres = LETTRES[:k]
    r = moteur.scorer(prompt)
    brut = masse_des_lettres_prefixe(r["top"], ids_lettres, lettres, prefixe)
    masse = float(sum(brut.values()))
    absentes = [l for l, v in brut.items() if v == 0.0]
    if masse > 0:
        distribution = {options[i]: brut[l] / masse for i, l in enumerate(lettres)}
    else:
        distribution = {o: 1.0 / k for o in options}
    return {
        "duree_ms": round(r["duree_ms"], 2),
        "masse_lettres": masse,
        "rejet": masse < SEUIL_MASSE,
        "modalites_absentes": absentes,
        "distribution": distribution,
        "argmax": max(distribution, key=distribution.get),
        "tokens_prompt": r["tokens_prompt"],
        "tokens_calcules": r["tokens_calcules"],
        "prompt_ms": r["prompt_ms"],
    }


# ---------------------------------------------------------------------------
# 6. Le smoke test integre
# ---------------------------------------------------------------------------

def sonder_variante(moteur, spec, sys_txt, bloc_user, options):
    """Mesure la masse des deux variantes de fin de prompt et retient la meilleure.

    La variante `answer` est celle de a5 ; elle est conservee des qu'elle atteint le
    seuil, pour que le prompt reste comparable a la trace Qwen3-4B existante. La
    variante `brut` n'est retenue que si `answer` echoue et qu'elle fait mieux. Les deux
    masses sont ecrites dans le journal quel que soit le choix.
    """
    mesures = {}
    for variante in ("answer", "brut"):
        try:
            prompt = construire_prompt(spec, sys_txt, bloc_user, variante)
            ids, _ = tokens_des_lettres(moteur, prompt, len(options),
                                        VARIANTES[variante])
            r = un_appel(moteur, variante, prompt, options, ids)
            mesures[variante] = r["masse_lettres"]
        except Exception as e:
            mesures[variante] = float("nan")
            journal(f"  sonde {variante} : echec, {e}")
    journal(f"  sonde de gabarit : answer {mesures.get('answer', float('nan')):.4f}, "
            f"brut {mesures.get('brut', float('nan')):.4f}")
    a = mesures.get("answer", float("nan"))
    b = mesures.get("brut", float("nan"))
    if np.isfinite(a) and a >= SEUIL_SMOKE_MEDIANE:
        return "answer", mesures
    if np.isfinite(b) and (not np.isfinite(a) or b > a):
        return "brut", mesures
    return "answer", mesures


def smoke_test(moteur, spec, variante, enumeration, items, table, cle_modele,
               n=N_SMOKE):
    """Vingt appels reels, ecrits dans une trace a part, avant d'engager la nuit.

    La trace de smoke test est un fichier distinct : elle ne doit jamais se melanger a
    la trace du run, parce que la variante de gabarit peut y changer d'un essai a
    l'autre. Elle sert aussi a projeter le debit, en separant les appels qui paient un
    prefixe complet de ceux que le cache sert.
    """
    chemin = chemin_trace("smoke", cle_modele)
    masses, absents, durees, prefixes, servis = [], 0, [], [], []
    ids_par_k = {}
    t0 = time.time()
    with open(chemin, "a", encoding="utf-8") as fh:
        for p, groupe, j, sys_txt in enumeration:
            if len(masses) >= n:
                break
            nom = items[j]
            bloc_user, options = utilisateur(nom, table)
            prompt = construire_prompt(spec, sys_txt, bloc_user, variante)
            k = len(options)
            if k not in ids_par_k:
                ids_par_k[k], _ = tokens_des_lettres(moteur, prompt, k,
                                                     VARIANTES[variante])
                journal(f"  tokens verifies pour K={k} : {ids_par_k[k]}")
            r = un_appel(moteur, variante, prompt, options, ids_par_k[k])
            masses.append(r["masse_lettres"])
            if r["modalites_absentes"]:
                absents += 1
            durees.append(r["duree_ms"])
            tc = r["tokens_calcules"] or 0
            (prefixes if tc > 500 else servis).append(r["duree_ms"])
            fh.write(json.dumps({"pid": p["pid"], "item": nom, "condition": "smoke",
                                 "groupe": str(groupe), "variante": variante,
                                 "modele": spec["nom"], **r}, ensure_ascii=False) + "\n")
            fh.flush()
    duree = time.time() - t0
    ok, mesures, motif = verdict_smoke(masses, absents, n_attendu=n)
    mesures["duree_s"] = duree
    mesures["prefixes_payes"] = len(prefixes)
    mesures["ms_prefixe_median"] = float(np.median(prefixes)) if prefixes else float("nan")
    mesures["ms_appel_servi_median"] = float(np.median(servis)) if servis else float("nan")
    mesures["trace"] = chemin
    return ok, mesures, motif


def projeter(mesures, n_personnes, n_prefixes_par_personne, n_appels_par_personne):
    """Duree projetee d'une condition, a partir des deux couts mesures au smoke test.

    Deux postes et pas un : le prefixe de persona, qui pese 57 pour cent du temps en a5
    section 4.1, et l'appel servi par le cache. Les moyenner en un seul debit donne un
    chiffre qui se trompe d'un facteur deux selon la condition.
    """
    mp = mesures.get("ms_prefixe_median")
    ma = mesures.get("ms_appel_servi_median")
    if not (mp and np.isfinite(mp)):
        mp = float("nan")
    if not (ma and np.isfinite(ma)):
        ma = mesures.get("duree_s", float("nan")) * 1000.0 / max(mesures.get("appels", 1), 1)
    par_personne = (n_prefixes_par_personne * mp + n_appels_par_personne * ma) / 1000.0
    return {
        "secondes_par_personne": par_personne,
        "heures_pour_toutes": par_personne * n_personnes / 3600.0,
        "appels_par_heure": (n_appels_par_personne * 3600.0 / par_personne
                             if par_personne > 0 else float("nan")),
    }


# ---------------------------------------------------------------------------
# 7. Le run
# ---------------------------------------------------------------------------

def lancer(moteur, spec, variante, condition, retenus, items, blocs, y1, table,
           cols_familles, fin_ts, cle_modele, limite=None, journal_tous=200):
    """Execute une condition de bout en bout et ecrit la trace au fil de l'eau.

    Ecriture incrementale avec flush a chaque ligne et fsync tous les 200 appels : le
    script doit survivre a un arret brutal et reprendre exactement ou il s'etait arrete.
    """
    chemin = chemin_trace(condition, cle_modele)
    fait = index_existant(chemin)
    journal(f"[{condition}] trace {chemin}, {len(fait)} appels deja faits")

    ids_par_k = {}
    n_appels, n_rejets, n_absents = 0, 0, 0
    personnes_vues = set()
    t0 = time.time()
    tronque = False

    with open(chemin, "a", encoding="utf-8") as fh:
        for p, groupe, j, sys_txt in travaux_r2(condition, retenus, items, blocs, y1,
                                                table, cols_familles):
            nom = items[j]
            if (p["pid"], nom) in fait:
                continue
            if time.time() >= fin_ts:
                journal(f"[{condition}] fin dure atteinte, arret propre")
                tronque = True
                break
            if limite is not None and n_appels >= limite:
                journal(f"[{condition}] limite de {limite} appels atteinte")
                tronque = True
                break

            bloc_user, options = utilisateur(nom, table)
            prompt = construire_prompt(spec, sys_txt, bloc_user, variante)
            k = len(options)
            if k not in ids_par_k:
                ids_par_k[k], _ = tokens_des_lettres(moteur, prompt, k,
                                                     VARIANTES[variante])
                journal(f"  tokens verifies pour K={k} : {ids_par_k[k]}")

            r = un_appel(moteur, variante, prompt, options, ids_par_k[k])
            if r["modalites_absentes"]:
                n_absents += 1
            if r["rejet"]:
                n_rejets += 1

            ligne = {
                "pid": p["pid"], "item": nom, "condition": condition, "passe": 1,
                "pli": p["pli"], "bloc": groupe if isinstance(groupe, int) else str(groupe),
                "version_prompt": f"r2-p1-{cle_modele}-{variante}",
                "modele": spec["nom"], "quantification": spec["quantification"],
                "gabarit": spec["gabarit"], "variante_fin": variante,
                "ordre_modalites": "nomenclature",
                **r,
            }
            fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            fh.flush()
            n_appels += 1
            personnes_vues.add(p["pid"])

            if n_appels % journal_tous == 0:
                ecoule = time.time() - t0
                os.fsync(fh.fileno())
                journal(f"  {condition} : {n_appels} appels, "
                        f"{n_appels / ecoule * 3600:,.0f}/h, rejets {n_rejets}, "
                        f"{len(personnes_vues)} personnes, "
                        f"{datetime.datetime.now():%H:%M:%S}".replace(",", " "))
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    return {
        "condition": condition, "appels": n_appels, "deja_faits": len(fait),
        "secondes": ecoule, "tronque": tronque,
        "appels_par_heure": n_appels / ecoule * 3600 if n_appels else 0.0,
        "rejets": n_rejets, "appels_avec_modalite_absente": n_absents,
        "personnes_touchees": len(personnes_vues), "trace": chemin,
    }


def personnes_completes(chemin, n_items_attendu=58):
    """Personnes dont les 58 cellules sont dans la trace. Sert au compte rendu."""
    compte = {}
    if not os.path.exists(chemin):
        return 0, 0
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            if "pid" in d:
                compte[d["pid"]] = compte.get(d["pid"], 0) + 1
    return (sum(1 for v in compte.values() if v >= n_items_attendu), len(compte))


# ---------------------------------------------------------------------------
# 8. Verification hors ligne, sans serveur
# ---------------------------------------------------------------------------

def verification_seule(args, spec, retenus, items, blocs, y1, table, cols_familles):
    """Tout ce qui peut se verifier sans allumer un serveur, et rien de plus.

    Ce mode existe parce que la machine est occupee par un autre run jusque vers 01:00
    et que la regle du projet est qu'un seul llama-server tourne a la fois. Il verifie
    l'enumeration, le regime severe des prompts, la reprise, le gabarit, le verdict du
    smoke test et le calcul de la fin dure.
    """
    ok_global = True

    def dire(nom, ok, detail=""):
        nonlocal ok_global
        ok_global = ok_global and ok
        journal(f"  [{'ok' if ok else 'ECHEC'}] {nom}" + (f" : {detail}" if detail else ""))

    journal("\n--- 1. Enumeration des appels ---")
    for condition in ("C3F", "C3"):
        n, prefixes, par_personne = 0, set(), {}
        for p, groupe, j, sys_txt in travaux_r2(condition, retenus, items, blocs, y1,
                                                table, cols_familles):
            n += 1
            prefixes.add((p["pid"], str(groupe)))
            par_personne[p["pid"]] = par_personne.get(p["pid"], 0) + 1
        attendu = len(retenus) * len(cols_familles)
        dire(f"{condition} : nombre d'appels", n == attendu, f"{n} contre {attendu} attendus")
        dire(f"{condition} : appels par personne",
             set(par_personne.values()) == {len(cols_familles)},
             f"{sorted(set(par_personne.values()))}")
        n_pref = len(prefixes) / max(len(par_personne), 1)
        dire(f"{condition} : prefixes par personne",
             n_pref == (6 if condition == "C3F" else 5), f"{n_pref:.1f}")

    journal("\n--- 2. Le regime severe est bien dans les prompts ---")
    fam = dict(groupes_familles(items))
    for condition, attendu_cousins in (("C3F", False), ("C3", True)):
        vus = 0
        fautes_cible, fautes_cousins = 0, 0
        for p, groupe, j, sys_txt in travaux_r2(condition, retenus[:2], items, blocs, y1,
                                                table, cols_familles):
            cible = table[items[j]]["question"]
            if cible in sys_txt:
                fautes_cible += 1
            famille = next(nom for nom, cols in fam.items() if j in cols)
            cousins = [items[c] for c in fam[famille] if c != j]
            presents = sum(1 for c in cousins if table[c]["question"] in sys_txt)
            if condition == "C3F" and presents > 0:
                fautes_cousins += 1
            if condition == "C3" and presents == 0 and len(cousins) > 3:
                fautes_cousins += 1
            vus += 1
        dire(f"{condition} : l'item cible est absent du contexte", fautes_cible == 0,
             f"{fautes_cible} fautes sur {vus} prompts")
        dire(f"{condition} : cousins {'presents' if attendu_cousins else 'absents'}",
             fautes_cousins == 0, f"{fautes_cousins} fautes sur {vus} prompts")

    journal("\n--- 3. Longueur des prompts ---")
    for condition in ("C3F", "C3"):
        longueurs = []
        for p, groupe, j, sys_txt in travaux_r2(condition, retenus[:3], items, blocs, y1,
                                                table, cols_familles):
            bloc_user, options = utilisateur(items[j], table)
            longueurs.append(len(construire_prompt(spec, sys_txt, bloc_user, "answer")))
        longueurs = np.array(longueurs)
        journal(f"  {condition} : {longueurs.min()} a {longueurs.max()} caracteres, "
                f"soit environ {longueurs.min() // 4} a {longueurs.max() // 4} tokens")
        dire(f"{condition} : le prompt tient dans le contexte du slot",
             longueurs.max() // 4 < args.contexte * 0.9,
             f"{longueurs.max() // 4} contre {args.contexte} tokens par slot")

    journal("\n--- 4. Gabarits ---")
    for cle, sp in MODELES.items():
        p_ans = construire_prompt(sp, "SYS", "USER", "answer")
        p_brut = construire_prompt(sp, "SYS", "USER", "brut")
        dire(f"{cle} : la variante answer ne finit pas par une espace",
             not p_ans.endswith(" "), repr(p_ans[-12:]))
        dire(f"{cle} : la variante brut ne finit pas par une espace",
             not p_brut.endswith(" "), repr(p_brut[-12:]))
    dire("le gabarit Qwen d'ici est celui de a5, caractere pour caractere",
         construire_prompt(MODELES["qwen4"], "SYS", "USER", "answer")
         == gabarit_qwen("SYS", "USER"))
    journal("  gabarit harmony, variante answer, fin du prompt :")
    journal("    " + repr(construire_prompt(MODELES["gptoss"], "S", "Q", "answer")[-64:]))

    journal("\n--- 5. Reprise sur une trace synthetique ---")
    faux = os.path.join(TRACES, "r2-verification-synthetique.jsonl")
    enum = list(travaux_r2("C3F", retenus[:2], items, blocs, y1, table, cols_familles))
    with open(faux, "w", encoding="utf-8") as fh:
        for p, groupe, j, _s in enum[:70]:
            fh.write(json.dumps({"pid": p["pid"], "item": items[j], "condition": "C3F",
                                 "distribution": {"a": 1.0}}) + "\n")
        fh.write('{"pid": "participant_XXXX", "item": "tronq')  # ligne coupee volontaire
    fait = index_existant(faux)
    dire("l'index de reprise lit les lignes entieres", len(fait) == 70, f"{len(fait)}")
    dire("l'index de reprise ignore la ligne tronquee sans echouer",
         ("participant_XXXX", "tronq") not in fait)
    restants = [1 for p, g, j, _s in enum if (p["pid"], items[j]) not in fait]
    dire("une relance ne referait que les appels manquants",
         len(restants) == len(enum) - 70, f"{len(restants)} sur {len(enum)}")
    os.remove(faux)

    journal("\n--- 6. Verdict du smoke test, sur des masses synthetiques ---")
    cas = [
        ("gabarit correct, masse 0,999", [0.999] * 20, 0, True),
        ("gpt-oss sans gabarit, masse 0,032", [0.032] * 20, 0, False),
        ("gabarit avec espace finale, masse 0,84", [0.84] * 20, 0, False),
        ("un seul appel bas sur vingt", [0.999] * 19 + [0.40], 0, False),
        ("masse mediane juste au seuil", [0.90] * 20, 0, True),
        ("modalites absentes du top 40", [0.95] * 20, 8, False),
        ("appels manquants", [0.999] * 12, 0, False),
    ]
    for nom, masses, absents, attendu in cas:
        ok, mes, motif = verdict_smoke(masses, absents, n_attendu=20)
        dire(f"verdict : {nom}", ok == attendu, motif)

    journal("\n--- 7. Fin dure, en epoch avec le jour ---")
    ts, dt = heure_de_fin(args.fin)
    dire("la fin dure est dans le futur", ts > time.time(),
         f"{dt:%Y-%m-%d %H:%M}, dans {(ts - time.time()) / 3600:.2f} h")

    journal("\n--- 8. Machine ---")
    pids = serveurs_en_cours()
    journal(f"  llama-server en cours : {pids if pids else 'aucun'}")
    journal(f"  charge machine : {os.getloadavg()}")
    for cle, sp in MODELES.items():
        dire(f"modele present : {cle}", os.path.exists(sp["fichier"]),
             sp["fichier"] if not os.path.exists(sp["fichier"]) else
             f"{os.path.getsize(sp['fichier']) / 2**30:.1f} Gio")

    journal("\n--- 9. Projection de debit, a partir des mesures de a3 et de a5 ---")
    # a5-familles.log : C3F sur Qwen3-4B, 2 688 appels par heure, machine a charge 1,4.
    # a3 section 5.1 : gpt-oss-20b fait 9 569 appels par heure en regime etabli contre
    # 18 060 pour Qwen3-4B, et son prefill est de 492 tokens par seconde contre 790.
    ratio = 9569.0 / 18060.0
    debit_projete = 2688.0 * ratio
    journal(f"  C3F Qwen3-4B mesure : 2 688 appels/h [MESURE, a5-familles.log]")
    journal(f"  rapport gpt-oss sur Qwen3-4B en regime etabli : {ratio:.2f} [MESURE, a3 5.1]")
    journal(f"  C3F gpt-oss projete : {debit_projete:,.0f} appels/h, "
            f"soit {8700 / debit_projete:.1f} h pour 150 personnes [ESTIMATION]"
            .replace(",", " "))
    journal(f"  la projection sera refaite sur mesure au smoke test, et le nombre de "
            f"personnes couvertes ecrit dans le journal")

    journal("\n" + ("VERIFICATION COMPLETE : tout passe" if ok_global
                    else "VERIFICATION COMPLETE : AU MOINS UN ECHEC"))
    return ok_global


# ---------------------------------------------------------------------------

def main():
    global _journal_fh
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="gptoss", choices=sorted(MODELES),
                    help="gptoss par defaut ; qwen30 est le repli documente")
    ap.add_argument("--conditions", default="C3F,C3",
                    help="liste ordonnee ; C3F d'abord, c'est le regime severe")
    ap.add_argument("--personnes", type=int, default=150)
    ap.add_argument("--fin", default="08:00", help="fin dure du calcul, heure locale")
    ap.add_argument("--port", type=int, default=0, help="0 pour choisir un port libre")
    ap.add_argument("--contexte", type=int, default=8192, help="tokens par slot")
    ap.add_argument("--parallele", type=int, default=8, help="-np, 8 en configuration a3")
    ap.add_argument("--verification-seule", action="store_true",
                    help="tout verifier sans allumer de serveur, machine occupee")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal d'appels par condition, pour un essai")
    ap.add_argument("--sans-cache-kv-8bits", action="store_true",
                    help="repli si le serveur refuse le cache KV quantifie")
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    nom_log = "r2-verification.log" if args.verification_seule else "r2-run.log"
    chemin_log = os.path.join(TRACES, nom_log)
    if not sortie_est_deja(chemin_log):
        _journal_fh = open(chemin_log, "a", encoding="utf-8")

    spec = MODELES[args.modele]
    journal("=" * 78)
    journal(f"popsim R2, la comparaison appariee sur les gens rares, regime severe.")
    journal(f"demarrage {datetime.datetime.now():%Y-%m-%d %H:%M:%S}, PID {os.getpid()}")
    journal(f"page de plan : resultats/r2-preenregistrement.md, 8 septembre 2026 22:05:00 CEST")
    journal(f"modele : {spec['nom']} {spec['quantification']}, gabarit {spec['gabarit']}, "
            f"coupure publiee {spec['coupure_publiee']}")
    journal(f"charge machine : {os.getloadavg()}")

    # --------------------------------------------------- donnees et echantillon
    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    plis, blocs = grille(len(ids), len(items), GRAINE)
    par_pli = max(1, args.personnes // N_PLIS)
    retenus = echantillon(ids, plis, par_pli, graine=GRAINE_ECHANTILLON)

    # Le sous echantillon de a5 est relu s'il existe, jamais reecrit : c'est lui qui
    # definit la population sur laquelle l'evaluation restreindra les baselines, et le
    # rejouer d'une autre graine casserait l'appariement avec la trace Qwen3-4B.
    chemin_personnes = os.path.join(TRACES, "a5-personnes.csv")
    if os.path.exists(chemin_personnes):
        ech = pd.read_csv(chemin_personnes)
        attendus = list(ech["pid"])
        obtenus = [p["pid"] for p in retenus]
        if attendus != obtenus:
            journal(f"ATTENTION : l'echantillon retire differe de {chemin_personnes}, "
                    f"le fichier fait foi")
            index_par_pid = {p["pid"]: p for p in retenus}
            retenus = [index_par_pid[p] if p in index_par_pid else
                       {"pid": r.pid, "index": int(r.index), "pli": int(r.pli)}
                       for p, r in zip(attendus, ech.itertuples())]
        else:
            journal(f"echantillon identique a {chemin_personnes} : "
                    f"{len(retenus)} personnes, {par_pli} par pli [CONTROLE]")

    cols_familles = sorted({j for _nom, cols in groupes_familles(items) for j in cols})
    journal(f"{len(retenus)} personnes, {len(cols_familles)} items de famille, "
            f"{len(retenus) * len(cols_familles)} appels par condition")

    if args.verification_seule:
        ok = verification_seule(args, spec, retenus, items, blocs, y1, table, cols_familles)
        journal(f"VERIFICATION TERMINEE {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        sys.exit(0 if ok else 1)

    # --------------------------------------------------- un seul serveur a la fois
    pids = serveurs_en_cours()
    if pids:
        journal(f"arret : un llama-server tourne deja, PID {pids}. Deux serveurs sur ce "
                f"GPU s'effondrent mutuellement, facteur 9,5 mesure en a5 section 4.4.")
        sys.exit(1)
    if not os.path.exists(spec["fichier"]):
        journal(f"arret : modele introuvable, {spec['fichier']}")
        sys.exit(1)

    fin_ts, fin_dt = heure_de_fin(args.fin)
    journal(f"fin dure a {fin_dt:%Y-%m-%d %H:%M:%S} (epoch {int(fin_ts)}), dans "
            f"{(fin_ts - time.time()) / 3600:.2f} h")

    with open(os.path.join(TRACES, "r2-run.pid"), "w") as fh:
        fh.write(str(os.getpid()))

    port = args.port or premier_port_libre(depart=8200)
    if not port_libre(port):
        journal(f"arret : le port {port} est occupe")
        sys.exit(1)
    journal(f"llama-server sur le port {port}, -np {args.parallele}, "
            f"-c {args.contexte * args.parallele}, "
            f"KV {'f16' if args.sans_cache_kv_8bits else 'q8_0'}")

    moteur = MoteurA5(spec["fichier"], contexte=args.contexte, parallele=args.parallele,
                      port=port, cache_kv_8bits=not args.sans_cache_kv_8bits)
    try:
        moteur.demarrer()
    except RuntimeError as e:
        journal(f"le serveur n'a pas demarre avec le cache KV quantifie : {e}")
        journal("second essai sans cache KV quantifie")
        moteur = MoteurA5(spec["fichier"], contexte=args.contexte,
                          parallele=args.parallele, port=port, cache_kv_8bits=False)
        moteur.demarrer()
    journal(f"serveur pret en {moteur.chargement_s:.1f} s")

    resume, projections = [], {}
    codes = [c.strip() for c in args.conditions.split(",") if c.strip()]
    try:
        # ------------------------------------------- smoke test integre, 20 appels
        enum_smoke = travaux_r2("C3F", retenus, items, blocs, y1, table, cols_familles)
        p0, g0, j0, sys0 = next(enum_smoke)
        bloc0, options0 = utilisateur(items[j0], table)
        variante, sondes = sonder_variante(moteur, spec, sys0, bloc0, options0)
        journal(f"  variante de fin retenue : {variante} "
                f"(le prompt s'arrete sur "
                f"{'Answer:' if variante == 'answer' else 'le tour assistant'})")

        journal(f"smoke test : {N_SMOKE} appels reels avant d'engager la nuit")
        enum_smoke = travaux_r2("C3F", retenus, items, blocs, y1, table, cols_familles)
        ok, mes, motif = smoke_test(moteur, spec, variante, enum_smoke, items, table,
                                    args.modele)
        journal(f"  masse mediane {mes['masse_mediane']:.4f}, minimale "
                f"{mes['masse_minimale']:.4f}, modalites absentes "
                f"{mes['part_modalites_absentes']:.2f}, duree {mes['duree_s']:.0f} s")
        journal(f"  prefixe median {mes['ms_prefixe_median']:.0f} ms sur "
                f"{mes['prefixes_payes']} prefixes payes, appel servi par le cache "
                f"{mes['ms_appel_servi_median']:.0f} ms")
        journal(f"  {motif}")
        if not ok:
            journal("le run ne demarre pas. Repli documente : relancer avec "
                    "--modele qwen30. Aucune ligne de trace utile n'a ete ecrite.")
            sys.exit(2)

        # ------------------------------------------- projection, avant les appels
        budget_h = (fin_ts - time.time()) / 3600.0
        for condition, n_pref in (("C3F", 6), ("C3", 5)):
            pr = projeter(mes, len(retenus), n_pref, len(cols_familles))
            projections[condition] = pr
            journal(f"projection {condition} : {pr['secondes_par_personne']:.0f} s par "
                    f"personne, {pr['appels_par_heure']:,.0f} appels/h, "
                    f"{pr['heures_pour_toutes']:.1f} h pour {len(retenus)} personnes"
                    .replace(",", " "))
        reste = budget_h
        for condition in codes:
            pr = projections.get(condition)
            if not pr:
                continue
            couvertes = min(len(retenus), int(reste * 3600 / pr["secondes_par_personne"]))
            journal(f"  budget restant {reste:.2f} h : {condition} couvre environ "
                    f"{couvertes} personnes sur {len(retenus)} [ESTIMATION]")
            reste = max(0.0, reste - pr["heures_pour_toutes"])

        # ------------------------------------------- la file
        for code in codes:
            if code not in ("C3F", "C3"):
                journal(f"condition inconnue, ignoree : {code}")
                continue
            if time.time() >= fin_ts:
                journal(f"fin dure atteinte avant le lancement de {code}")
                break
            r = lancer(moteur, spec, variante, code, retenus, items, blocs, y1, table,
                       cols_familles, fin_ts, args.modele, limite=args.limite)
            r["variante_fin"] = variante
            complets, touchees = personnes_completes(r["trace"], len(cols_familles))
            r["personnes_completes"] = complets
            resume.append(r)
            journal(f"[{code}] {r['appels']} appels en {r['secondes'] / 60:.1f} min, "
                    f"{r['appels_par_heure']:,.0f} appels/h, {r['rejets']} rejets, "
                    f"{complets} personnes completes sur {touchees} touchees"
                    .replace(",", " "))
    finally:
        # Le serveur est arrete quoi qu'il arrive : la file de nuit attend la machine et
        # deux llama-server ne doivent jamais tourner en meme temps.
        try:
            moteur.arreter()
        except Exception as e:
            journal(f"arret du serveur : {e}")
        journal(f"serveur arrete. charge machine : {os.getloadavg()}")

    chemin_resume = os.path.join(TRACES, f"r2-resume-{args.modele}.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({"fin_dure": fin_dt.isoformat(), "port": port,
                   "modele": spec["nom"], "quantification": spec["quantification"],
                   "gabarit": spec["gabarit"], "coupure_publiee": spec["coupure_publiee"],
                   "variante_fin": variante, "sondes_de_gabarit": sondes,
                   "smoke": {k: v for k, v in mes.items() if k != "trace"},
                   "projections": projections,
                   "personnes": len(retenus), "items": len(cols_familles),
                   "conditions": resume}, fh, indent=2, ensure_ascii=False)
    journal(f"resume ecrit : {chemin_resume}")
    journal(f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")


if __name__ == "__main__":
    main()
