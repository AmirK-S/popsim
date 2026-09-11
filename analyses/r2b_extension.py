"""
r2b_extension : porter la comparaison appariee R2 de 150 a 180 personnes.

Page de plan : resultats/r2b-preenregistrement.md, horodatee du 9 septembre 2026 a
13:19:38 CEST, ecrite AVANT le moindre appel de modele de langage de cette extension, et
non modifiee ensuite. Elle repond a la question 9 de DECISIONS-CONSOLIDEES-2026-09-09.md
(ligne 88), tranchee par defaut a oui : le contraste H1b contre PMM k=10 famille retiree
exige environ 176 personnes sous Holm (resultats/r2-resultats.md section 3.2) et R2 en a
couvert 150.

Ce que fait ce script. Il tire trente personnes de plus par la regle mecanique de
a21_extension_c2.echantillon_hors (stratification sur les cinq plis, vivier ampute des
150 deja jouees, graine fixe 20260908), puis rejoue sur elles la SEULE condition C3F, avec
gpt-oss-20b et son gabarit harmony, exactement comme R2. Six par pli, donc 180 au total,
quatre de marge au dessus du seuil de 176.

AUCUN SCRIPT EXISTANT N'EST MODIFIE. Tout est importe :
  r2_rares_apparie   MODELES, VARIANTES, construire_prompt, tokens_des_lettres, un_appel,
                     travaux_r2, verdict_smoke, smoke_test, projeter, serveurs_en_cours,
                     chemin_trace, index_existant, personnes_completes, GRAINE_ECHANTILLON
  a21_extension_c2   echantillon_hors, GRAINE_EXT
  a5_agents_locaux   MoteurA5, nomenclature, utilisateur, groupes_familles, heure_de_fin,
                     port_libre, premier_port_libre, TRACES
  a2_baselines_gss   charger, grille, GRAINE, N_PLIS

Ce qui change par rapport a r2_rares_apparie.py, et rien d'autre :
  1. la population : trente personnes NOUVELLES, disjointes des 150 par construction ;
  2. la condition : C3F seule, celle du contraste H1b ;
  3. -np 4 au lieu de 8 : gpt-oss-20b a huit slots a mis la machine a 14 Go de swap dans
     la nuit du 7 au 8 septembre 2026 ;
  4. trois regles d'arret que R2 n'avait pas : trois heures de run, swap au dessus de
     10 Go, et le fichier data/traces/STOP de analyses/README.md, qui manquait a
     r2_rares_apparie.py et dont l'absence a coute dix sept minutes de machine dans la
     nuit du 8 au 9 (SIGINT de 05:45 sans effet, kill -9 a 06:01) ;
  5. l'attente en boucle si un llama-server tourne deja : R2 sortait en erreur, ici on
     attend, et on ne tue JAMAIS le serveur d'un autre run.

La sonde de gabarit et le smoke test de vingt appels sont ceux de R2, importes tels quels.
La variante de fin de prompt retenue par R2 est `answer` ; si la sonde en choisissait une
autre ici, le run s'arreterait, parce qu'un changement de variante casserait
l'appariement avec les 150 personnes deja jouees.

Entree  : data/osf-t6g7k-stanford (non versionne), data/traces/a5-personnes.csv (lecture
          seule, definit les 150 a exclure).
Sortie  : data/traces/r2b-personnes-ext.csv   les 30 nouvelles personnes, ecrit avant tout appel
          data/traces/r2b-C3F-gptoss-ext.jsonl   la trace, 1 740 appels attendus
          data/traces/r2b-run.log              le journal, avec RUN TERMINE a la fin
          data/traces/r2b-memoire.csv          swap et charge, une ligne par minute
          data/traces/r2b-resume-gptoss.json   le resume de fin de run
          data/traces/r2b-smoke-gptoss.jsonl   les vingt appels du smoke test

Rien ne sort de la machine. Aucun appel distant. La trace ne contient PAS la vraie reponse
de la personne : l'evaluateur la relit dans data/.

Reprise : l'index unique est (pid, item), lu dans la trace. Une relance ne refait aucun
appel deja ecrit. L'ordre est personne par personne : une troncature coute des personnes
entieres, jamais des items.

Usage :
  .venv/bin/python analyses/r2b_extension.py --verification-seule
  .venv/bin/python analyses/r2b_extension.py --heures 3
"""

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

from a2_baselines_gss import charger, grille, GRAINE
from a5_agents_locaux_gss import (MoteurA5, TRACES, groupes_familles, nomenclature,
                                  port_libre, premier_port_libre, utilisateur)
from a21_extension_c2 import GRAINE_EXT, echantillon_hors
import r2_rares_apparie as R2

# --------------------------------------------------------------------------------------
# Constantes de la page de plan. Aucune n'est un reglage : chacune est ecrite dans
# resultats/r2b-preenregistrement.md et ne doit pas bouger sans que la page bouge.
# --------------------------------------------------------------------------------------

PAR_PLI = 6                      # 6 x 5 plis = 30 nouvelles personnes, total 180
N_CIBLE = 180                    # au dessus des 176 exiges par r2-resultats section 3.2
PLANCHER_LISIBILITE = 176        # sous ce total, le rapport ne conclut pas sur H1b
CONDITION = "C3F"                # la condition du contraste H1b, regime severe
CLE_MODELE = "gptoss"
VARIANTE_EXIGEE = "answer"       # celle que R2 a retenue ; en changer casserait l'appariement
HEURES_MAX = 3.0                 # regle d'arret 1
PERIODE_SONDE_S = 60

# Regle d'arret memoire. La version preenregistree, "swap utilise au dessus de 10 240 Mio",
# a fait feu a 13:25:26 le 9 septembre 2026, une minute apres le demarrage et avant le
# premier appel utile : le seul chargement du fichier de 11,3 Gio sur une machine de 32 Gio
# deja a 6,6 Go de swap franchissait le seuil. La mesure faite juste apres l'arret montre
# pourquoi l'instrument etait le mauvais : serveur arrete, aucun llama-server sur la
# machine, le compteur reste a 12 426 Mio alors que le compresseur retombe de 482 849 a
# 272 871 pages et que memory_pressure annonce 76 pour cent de memoire libre. `vm.swapusage
# used` mesure l'occupation du FICHIER d'echange, que macOS ne retrecit pas ; il ne
# redescend jamais et ne peut donc pas servir de garde fou.
# Le remplacement est ecrit et justifie dans resultats/r2b-amendement-regle-memoire.md,
# horodate du 9 septembre 2026 a 13:28:00 CEST, APRES le declenchement et AVANT la relance.
# Aucun contraste n'etait calcule a cet instant. C'est une regle d'exploitation de la
# machine, pas une regle d'inference : elle decide si le run tourne, jamais ce qu'il mesure.
PRESSION_LIBRE_MIN_PCT = 15.0    # memory_pressure, memoire libre systeme, critere 1
SWAP_DELTA_MAX_MIO = 4096.0      # croissance au dessus du plateau de chargement, critere 2
SWAP_PLAFOND_DUR_MIO = 24576.0   # 24 Go, dernier filet, critere 3

CHEMIN_PERSONNES_R2 = os.path.join(TRACES, "a5-personnes.csv")
CHEMIN_PERSONNES_EXT = os.path.join(TRACES, "r2b-personnes-ext.csv")
CHEMIN_TRACE = os.path.join(TRACES, "r2b-C3F-gptoss-ext.jsonl")
CHEMIN_MEMOIRE = os.path.join(TRACES, "r2b-memoire.csv")
CHEMIN_STOP = os.path.join(TRACES, "STOP")

_journal_fh = None
_arret_memoire = {"declenche": False, "swap_max": 0.0, "detail": ""}


def journal(texte=""):
    """Ecrit sur la sortie standard ET dans le journal du run.

    Meme discipline que R2 : si la sortie standard est deja ce fichier la, le second
    handle n'est pas ouvert, sinon chaque ligne serait ecrite deux fois et un lecteur
    pourrait croire que le run a fait deux fois le meme travail.
    """
    print(texte, flush=True)
    if _journal_fh is not None:
        _journal_fh.write(texte + "\n")
        _journal_fh.flush()


# --------------------------------------------------------------------------------------
# 1. La memoire : lire le swap, et poser l'arret au dessus de 10 Go
# --------------------------------------------------------------------------------------

def swap_mio():
    """Swap utilise, en Mio, lu dans sysctl vm.swapusage.

    Le format de macOS est `total = 8192,00M  used = 6672,19M  free = 1519,81M`, avec la
    virgule decimale de la locale francaise. La regexp accepte les deux separateurs :
    un point de bascule de locale ne doit pas rendre la sonde aveugle, ce qui ferait
    passer une machine a 14 Go de swap pour une machine saine.
    """
    try:
        r = subprocess.run(["sysctl", "vm.swapusage"], capture_output=True, text=True,
                           timeout=10)
    except (OSError, subprocess.SubprocessError):
        return float("nan")
    m = re.search(r"used\s*=\s*([0-9]+[.,]?[0-9]*)M", r.stdout)
    if not m:
        return float("nan")
    return float(m.group(1).replace(",", "."))


def pression_libre_pct():
    """Memoire libre systeme, en pour cent, telle que `memory_pressure` la calcule.

    C'est la seule des trois quantites de la regle amendee qui monte ET qui descend avec
    la charge : mesuree a 76 pour cent le 9 septembre a 13:26, serveur arrete, alors que
    le compteur de swap affichait encore 12 426 Mio. Renvoie NaN si la commande n'est pas
    lisible. Depuis la reprise du 10 septembre, une sonde illisible declenche un
    arret de precaution : aucun run sans garde memoire observable.
    """
    try:
        r = subprocess.run(["memory_pressure", "-Q"], capture_output=True, text=True,
                           timeout=20)
    except (OSError, subprocess.SubprocessError):
        return float("nan")
    m = re.search(r"free percentage:\s*([0-9]+)", r.stdout)
    return float(m.group(1)) if m else float("nan")


def sonde_memoire(arret_evt, plateau, chemin=CHEMIN_MEMOIRE, periode=PERIODE_SONDE_S):
    """Fil de fond : une ligne par minute, et pose STOP sur les trois criteres amendes.

    La sonde ne tue rien et n'envoie aucun signal. Elle pose le fichier d'arret, que la
    boucle d'appels relit entre deux appels : c'est la seule facon d'obtenir une trace
    fermee proprement, et c'est exactement la lecon de l'incident du 8 au 9 septembre,
    ou un SIGINT envoye a un processus bloque dans un appel HTTP n'a rien arrete.

    plateau : swap utilise releve une fois le serveur pret. La croissance est comptee a
    partir de la, et non a partir du depart : le fichier d'echange herite des autres
    agents n'est pas imputable a ce run, et le compteur ne redescend pas quand ils
    s'arretent.
    """
    neuf = not os.path.exists(chemin)
    with open(chemin, "a", encoding="utf-8") as fh:
        if neuf:
            fh.write("horodatage,swap_mio,delta_plateau_mio,libre_pct,charge_1min\n")
        while not arret_evt.is_set():
            s = swap_mio()
            libre = pression_libre_pct()
            c = os.getloadavg()[0]
            base = plateau.get("swap") if isinstance(plateau, dict) else plateau
            delta = s - base if np.isfinite(s) and base is not None else float("nan")
            fh.write(f"{datetime.datetime.now():%Y-%m-%dT%H:%M:%S},{s:.2f},"
                     f"{delta:.2f},{libre:.0f},{c:.2f}\n")
            fh.flush()
            if np.isfinite(s):
                _arret_memoire["swap_max"] = max(_arret_memoire["swap_max"], s)
            motif = ""
            if not np.isfinite(s) or not np.isfinite(libre):
                motif = "sonde memoire illisible, arret de precaution"
            elif libre < PRESSION_LIBRE_MIN_PCT:
                motif = (f"memoire libre systeme {libre:.0f} pour cent, sous le seuil "
                         f"{PRESSION_LIBRE_MIN_PCT:.0f} pour cent")
            elif np.isfinite(delta) and delta > SWAP_DELTA_MAX_MIO:
                motif = (f"swap {s:.0f} Mio, soit {delta:.0f} Mio au dessus du plateau de "
                         f"chargement {plateau:.0f} Mio, seuil {SWAP_DELTA_MAX_MIO:.0f}")
            elif np.isfinite(s) and s > SWAP_PLAFOND_DUR_MIO:
                motif = (f"swap {s:.0f} Mio au dessus du plafond dur "
                         f"{SWAP_PLAFOND_DUR_MIO:.0f} Mio")
            if motif and not _arret_memoire["declenche"]:
                _arret_memoire["declenche"] = True
                _arret_memoire["detail"] = motif
                poser_stop(f"r2b : {motif}")
            arret_evt.wait(periode)


def poser_stop(motif):
    """Pose data/traces/STOP. Le script ne l'efface JAMAIS : celui qui pose retire."""
    try:
        with open(CHEMIN_STOP, "a", encoding="utf-8") as fh:
            fh.write(f"{datetime.datetime.now():%Y-%m-%dT%H:%M:%S} {motif}\n")
    except OSError:
        pass


def stop_demande():
    return os.path.exists(CHEMIN_STOP)


class MoteurR2b(MoteurA5):
    """Memes requetes et poids ; STOP entre requetes, transport borne a 120 s."""

    def _poster(self, route, charge, timeout=120):
        if stop_demande() or _arret_memoire["declenche"]:
            raise RuntimeError("R2b : arret demande avant requete locale")
        return super()._poster(route, charge, timeout=min(timeout, 120))


# --------------------------------------------------------------------------------------
# 2. La machine : attendre, ne jamais tuer
# --------------------------------------------------------------------------------------

def attendre_la_machine(attente_max_min, pas_s=30):
    """Attend qu'aucun llama-server ne tourne. Ne tue jamais le serveur d'un autre run.

    Deux serveurs sur ce GPU s'effondrent mutuellement, facteur 9,5 mesure en a5
    section 4.4 ; et un serveur qui tourne appartient a un autre chantier, dont la trace
    serait perdue si on le tuait.
    """
    debut = time.time()
    prevenu = False
    while True:
        pids = R2.serveurs_en_cours()
        if not pids:
            if prevenu:
                journal(f"  machine libre apres {(time.time() - debut) / 60:.1f} min "
                        f"d'attente")
            return True
        if not prevenu:
            journal(f"un llama-server tourne deja, PID {pids}. Attente, jamais d'arret "
                    f"force. Plafond d'attente {attente_max_min} min.")
            prevenu = True
        if (time.time() - debut) / 60.0 > attente_max_min:
            journal(f"arret : la machine est restee occupee plus de {attente_max_min} min "
                    f"(PID {pids}). Aucun serveur n'a ete tue.")
            return False
        if stop_demande():
            journal("arret : data/traces/STOP pose pendant l'attente de la machine")
            return False
        time.sleep(pas_s)


# --------------------------------------------------------------------------------------
# 3. L'echantillon d'extension
# --------------------------------------------------------------------------------------

def tirer_extension(ids, plis, par_pli=PAR_PLI):
    """Les nouvelles personnes, par la regle mecanique de a21, graine fixe 20260908.

    La regle est ecrite dans la page de plan section 1 : meme stratification sur les cinq
    plis que a5.echantillon, vivier ampute des 150 deja jouees, graine 20260908, celle
    que a21_extension_c2 emploie deja pour le second echantillon de C2. Aucune personne
    n'est choisie a la main, et aucune n'est choisie sur une propriete de ses reponses :
    selectionner les gens qui portent des cellules rares stables reviendrait a choisir
    l'echantillon sur la variable de resultat.
    """
    if not os.path.exists(CHEMIN_PERSONNES_R2):
        sys.exit(f"echantillon de R2 introuvable : {CHEMIN_PERSONNES_R2}")
    ech0 = pd.read_csv(CHEMIN_PERSONNES_R2)
    index0 = {int(i) for i in ech0["index"]}
    pids0 = set(ech0["pid"])
    retenus = echantillon_hors(ids, plis, par_pli, index0, graine=GRAINE_EXT)
    pids = [p["pid"] for p in retenus]
    if set(pids) & pids0:
        sys.exit("ECHEC : l'extension recoupe les 150 personnes de R2")
    if len(set(pids)) != len(pids):
        sys.exit("ECHEC : doublons internes dans l'extension")
    return retenus, ech0


# --------------------------------------------------------------------------------------
# 4. La boucle d'appels, avec les trois regles d'arret
# --------------------------------------------------------------------------------------

def lancer(moteur, spec, variante, retenus, items, blocs, y1, table, cols_familles,
           fin_ts, chemin=CHEMIN_TRACE, journal_tous=100, limite=None):
    """Execute C3F sur les nouvelles personnes et ecrit la trace au fil de l'eau.

    Ecriture incrementale avec flush a chaque ligne et fsync tous les 100 appels : le
    script doit survivre a un arret brutal et reprendre exactement ou il s'etait arrete.
    Les trois conditions d'arret sont relues ENTRE deux appels, jamais pendant : c'est ce
    qui garantit une trace fermee sur une ligne entiere.
    """
    fait = R2.index_existant(chemin)
    journal(f"[{CONDITION}] trace {chemin}, {len(fait)} appels deja faits")

    ids_par_k = {}
    n_appels, n_rejets, n_absents = 0, 0, 0
    personnes_vues = set()
    t0 = time.time()
    motif_arret = ""

    with open(chemin, "a", encoding="utf-8") as fh:
        for p, groupe, j, sys_txt in R2.travaux_r2(CONDITION, retenus, items, blocs, y1,
                                                   table, cols_familles):
            nom = items[j]
            if (p["pid"], nom) in fait:
                continue
            if stop_demande():
                motif_arret = "ARRET DEMANDE : data/traces/STOP"
                if _arret_memoire["declenche"]:
                    motif_arret += f" ({_arret_memoire['detail']})"
                journal(f"[{CONDITION}] {motif_arret}")
                break
            if time.time() >= fin_ts:
                motif_arret = "fin dure atteinte (trois heures), arret propre"
                journal(f"[{CONDITION}] {motif_arret}")
                break
            if limite is not None and n_appels >= limite:
                motif_arret = f"limite d'essai de {limite} appels atteinte"
                journal(f"[{CONDITION}] {motif_arret}")
                break

            bloc_user, options = utilisateur(nom, table)
            prompt = R2.construire_prompt(spec, sys_txt, bloc_user, variante)
            k = len(options)
            if k not in ids_par_k:
                ids_par_k[k], _ = R2.tokens_des_lettres(moteur, prompt, k,
                                                        R2.VARIANTES[variante])
                journal(f"  tokens verifies pour K={k} : {ids_par_k[k]}")

            r = R2.un_appel(moteur, variante, prompt, options, ids_par_k[k])
            if r["modalites_absentes"]:
                n_absents += 1
            if r["rejet"]:
                n_rejets += 1

            # Format de ligne identique a R2, au champ `extension` pres, qui existe pour
            # qu'un lecteur de la trace sache d'ou vient la personne sans avoir a croiser
            # avec le CSV. Le lecteur de r2_evaluer ignore les champs qu'il ne connait pas.
            ligne = {
                "pid": p["pid"], "item": nom, "condition": CONDITION, "passe": 1,
                "pli": p["pli"], "bloc": groupe if isinstance(groupe, int) else str(groupe),
                "version_prompt": f"r2-p1-{CLE_MODELE}-{variante}",
                "modele": spec["nom"], "quantification": spec["quantification"],
                "gabarit": spec["gabarit"], "variante_fin": variante,
                "ordre_modalites": "nomenclature", "extension": "r2b",
                **r,
            }
            fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            fh.flush()
            n_appels += 1
            personnes_vues.add(p["pid"])

            if n_appels % journal_tous == 0:
                ecoule = time.time() - t0
                os.fsync(fh.fileno())
                journal(f"  {CONDITION} : {n_appels} appels, "
                        f"{n_appels / ecoule * 3600:,.0f}/h, rejets {n_rejets}, "
                        f"{len(personnes_vues)} personnes, swap "
                        f"{swap_mio():.0f} Mio, {datetime.datetime.now():%H:%M:%S}"
                        .replace(",", " "))
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    return {
        "condition": CONDITION, "appels": n_appels, "deja_faits": len(fait),
        "secondes": ecoule, "arret": motif_arret,
        "appels_par_heure": n_appels / ecoule * 3600 if n_appels else 0.0,
        "rejets": n_rejets, "appels_avec_modalite_absente": n_absents,
        "personnes_touchees": len(personnes_vues), "trace": chemin,
    }


# --------------------------------------------------------------------------------------
# 5. Verification hors ligne, sans serveur
# --------------------------------------------------------------------------------------

def verification_seule(args, spec, retenus, ech0, items, blocs, y1, table, cols_familles):
    ok_global = True

    def dire(nom, ok, detail=""):
        nonlocal ok_global
        ok_global = ok_global and ok
        journal(f"  [{'ok' if ok else 'ECHEC'}] {nom}" + (f" : {detail}" if detail else ""))

    journal("\n--- 1. L'echantillon d'extension ---")
    pids = [p["pid"] for p in retenus]
    dire("trente personnes", len(retenus) == PAR_PLI * 5, f"{len(retenus)}")
    par_pli = {}
    for p in retenus:
        par_pli[p["pli"]] = par_pli.get(p["pli"], 0) + 1
    dire("six par pli", set(par_pli.values()) == {PAR_PLI}, f"{sorted(par_pli.items())}")
    dire("disjoint des 150 de R2", not (set(pids) & set(ech0["pid"])))
    dire("total au dessus du seuil de 176",
         len(ech0) + len(retenus) >= PLANCHER_LISIBILITE,
         f"{len(ech0)} + {len(retenus)} = {len(ech0) + len(retenus)}")
    journal("  tirage reproductible : echantillon_hors(par_pli=6, graine="
            f"{GRAINE_EXT}) dans le complementaire des index de a5-personnes.csv")

    journal("\n--- 2. Enumeration des appels ---")
    n, prefixes, par_personne = 0, set(), {}
    for p, groupe, j, _s in R2.travaux_r2(CONDITION, retenus, items, blocs, y1, table,
                                          cols_familles):
        n += 1
        prefixes.add((p["pid"], str(groupe)))
        par_personne[p["pid"]] = par_personne.get(p["pid"], 0) + 1
    attendu = len(retenus) * len(cols_familles)
    dire("nombre d'appels", n == attendu, f"{n} contre {attendu} attendus")
    dire("appels par personne", set(par_personne.values()) == {len(cols_familles)},
         f"{sorted(set(par_personne.values()))}")
    dire("prefixes par personne", len(prefixes) / len(par_personne) == 6,
         f"{len(prefixes) / len(par_personne):.1f}")

    journal("\n--- 3. Le regime severe est bien dans les prompts ---")
    fam = dict(groupes_familles(items))
    fautes_cible, fautes_cousins, vus = 0, 0, 0
    for p, groupe, j, sys_txt in R2.travaux_r2(CONDITION, retenus[:2], items, blocs, y1,
                                               table, cols_familles):
        if table[items[j]]["question"] in sys_txt:
            fautes_cible += 1
        famille = next(nom for nom, cols in fam.items() if j in cols)
        cousins = [items[c] for c in fam[famille] if c != j]
        if sum(1 for c in cousins if table[c]["question"] in sys_txt) > 0:
            fautes_cousins += 1
        vus += 1
    dire("l'item cible est absent du contexte", fautes_cible == 0,
         f"{fautes_cible} fautes sur {vus} prompts")
    dire("aucun cousin dans le contexte", fautes_cousins == 0,
         f"{fautes_cousins} fautes sur {vus} prompts")

    journal("\n--- 4. Gabarit harmony, variante answer ---")
    p_ans = R2.construire_prompt(spec, "SYS", "USER", "answer")
    dire("gabarit harmony", spec["gabarit"] == "harmony", spec["gabarit"])
    dire("le prompt ne finit pas par une espace", not p_ans.endswith(" "),
         repr(p_ans[-16:]))
    dire("le prompt est celui de R2, caractere pour caractere",
         p_ans == R2.gabarit_harmony("SYS", "USER", "answer"))

    journal("\n--- 5. Longueur des prompts ---")
    longueurs = []
    for p, groupe, j, sys_txt in R2.travaux_r2(CONDITION, retenus[:3], items, blocs, y1,
                                               table, cols_familles):
        bloc_user, _o = utilisateur(items[j], table)
        longueurs.append(len(R2.construire_prompt(spec, sys_txt, bloc_user, "answer")))
    longueurs = np.array(longueurs)
    journal(f"  {longueurs.min()} a {longueurs.max()} caracteres, soit environ "
            f"{longueurs.min() // 4} a {longueurs.max() // 4} tokens")
    dire("le prompt tient dans le contexte du slot",
         longueurs.max() // 4 < args.contexte * 0.9,
         f"{longueurs.max() // 4} contre {args.contexte} tokens par slot")

    journal("\n--- 6. Les regles d'arret ---")
    s = swap_mio()
    dire("le swap est lisible", np.isfinite(s), f"{s:.0f} Mio utilises")
    dire("le swap est sous le plafond dur", np.isfinite(s) and s <= SWAP_PLAFOND_DUR_MIO,
         f"{s:.0f} contre {SWAP_PLAFOND_DUR_MIO:.0f} Mio")
    libre = pression_libre_pct()
    dire("la memoire libre systeme est lisible", np.isfinite(libre),
         f"{libre:.0f} pour cent")
    dire("la memoire libre systeme est au dessus du seuil",
         np.isfinite(libre) and libre >= PRESSION_LIBRE_MIN_PCT,
         f"{libre:.0f} contre {PRESSION_LIBRE_MIN_PCT:.0f} pour cent")
    dire("le fichier d'arret n'est pas deja pose", not stop_demande(), CHEMIN_STOP)
    dire("la fin dure est a trois heures", args.heures == HEURES_MAX, f"{args.heures} h")
    dire("np reduit a 4", args.parallele == 4, f"-np {args.parallele}")

    journal("\n--- 7. Machine et modele ---")
    pids_srv = R2.serveurs_en_cours()
    journal(f"  llama-server en cours : {pids_srv if pids_srv else 'aucun'}")
    journal(f"  charge machine : {os.getloadavg()}")
    dire("le modele est present", os.path.exists(spec["fichier"]),
         f"{os.path.getsize(spec['fichier']) / 2**30:.1f} Gio"
         if os.path.exists(spec["fichier"]) else spec["fichier"])

    journal("\n--- 8. Projection ---")
    debit = 1932.0  # mesure de R2 sur C3F gpt-oss, r2-resultats section 0
    journal(f"  debit mesure de R2 sur C3F gpt-oss : {debit:.0f} appels/h [MESURE]")
    journal(f"  {attendu} appels a ce debit : {attendu / debit:.2f} h, contre "
            f"{args.heures} h de budget [ESTIMATION]")
    dire("le budget de trois heures couvre le run", attendu / debit < args.heures,
         f"{attendu / debit:.2f} h")

    journal("\n" + ("VERIFICATION COMPLETE : tout passe" if ok_global
                    else "VERIFICATION COMPLETE : AU MOINS UN ECHEC"))
    return ok_global


# --------------------------------------------------------------------------------------

def main():
    global _journal_fh
    ap = argparse.ArgumentParser()
    ap.add_argument("--heures", type=float, default=HEURES_MAX,
                    help="fin dure, en heures depuis le demarrage ; 3 dans la page de plan")
    ap.add_argument("--port", type=int, default=0, help="0 pour choisir un port libre")
    ap.add_argument("--contexte", type=int, default=8192, help="tokens par slot")
    ap.add_argument("--parallele", type=int, default=4,
                    help="-np ; 4 et non 8, incident memoire du 7 au 8 septembre")
    ap.add_argument("--attente-max", type=float, default=180.0,
                    help="minutes d'attente si un llama-server tourne deja")
    ap.add_argument("--verification-seule", action="store_true")
    ap.add_argument("--retirer-stop", default=None, metavar="MOTIF",
                    help="retire data/traces/STOP en journalisant son contenu et ce motif ; "
                         "sans ce drapeau, un STOP pose fait sortir le script")
    ap.add_argument("--essai", type=int, default=None,
                    help="nombre maximal d'appels, pour un essai ; ecrit dans r2b-essai.log")
    ap.add_argument("--journal-memoire", default=CHEMIN_MEMOIRE,
                    help="journal memoire neuf pour une reprise, anciennes traces conservees")
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    if args.verification_seule:
        nom_log = "r2b-verification.log"
    elif args.essai:
        nom_log = "r2b-essai.log"
    else:
        nom_log = "r2b-run.log"
    chemin_log = os.path.join(TRACES, nom_log)
    if not R2.sortie_est_deja(chemin_log):
        _journal_fh = open(chemin_log, "a", encoding="utf-8")

    spec = R2.MODELES[CLE_MODELE]
    journal("=" * 78)
    journal("popsim R2b, extension de la comparaison appariee de 150 a 180 personnes.")
    journal(f"demarrage {datetime.datetime.now():%Y-%m-%d %H:%M:%S}, PID {os.getpid()}")
    journal("page de plan : resultats/r2b-preenregistrement.md, "
            "9 septembre 2026 13:19:38 CEST")
    journal(f"modele : {spec['nom']} {spec['quantification']}, gabarit {spec['gabarit']}, "
            f"coupure publiee {spec['coupure_publiee']}")
    journal(f"charge machine : {os.getloadavg()}, swap {swap_mio():.0f} Mio")

    # ------------------------------------------------------------ donnees et echantillon
    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    plis, blocs = grille(len(ids), len(items), GRAINE)
    retenus, ech0 = tirer_extension(ids, plis)
    cols_familles = sorted({j for _n, cols in groupes_familles(items) for j in cols})
    journal(f"{len(ech0)} personnes deja jouees en R2, {len(retenus)} nouvelles, "
            f"total {len(ech0) + len(retenus)} (seuil de la section 3.2 : "
            f"{PLANCHER_LISIBILITE})")
    journal(f"{len(cols_familles)} items de famille, "
            f"{len(retenus) * len(cols_familles)} appels")

    if args.verification_seule:
        ok = verification_seule(args, spec, retenus, ech0, items, blocs, y1, table,
                                cols_familles)
        journal(f"VERIFICATION TERMINEE {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        sys.exit(0 if ok else 1)

    # L'echantillon est ecrit AVANT tout appel, comme en a5 et en a21 : c'est lui qui
    # definit la population sur laquelle l'evaluation restreindra les baselines.
    attendu = pd.DataFrame(retenus)[["pid", "index", "pli"]]
    if os.path.exists(CHEMIN_PERSONNES_EXT):
        existant = pd.read_csv(CHEMIN_PERSONNES_EXT)[["pid", "index", "pli"]]
        if not existant.equals(attendu):
            sys.exit("echantillon existant different du tirage fixe : arret")
        journal("echantillon existant valide et conserve")
    else:
        attendu.to_csv(CHEMIN_PERSONNES_EXT, index=False)

    # ------------------------------------------------------------ les regles d'arret
    # Le fichier d'arret n'est jamais retire en silence : `analyses/README.md` pose la
    # regle « celui qui l'a pose le retire », et un retrait sans motif ecrit ferait
    # disparaitre l'arret demande par un autre chantier. Le motif est journalise.
    if stop_demande():
        if args.retirer_stop:
            with open(CHEMIN_STOP, encoding="utf-8") as fh:
                contenu = fh.read().strip()
            journal(f"retrait de {CHEMIN_STOP}. Contenu : {contenu!r}")
            journal(f"motif du retrait : {args.retirer_stop}")
            os.remove(CHEMIN_STOP)
        else:
            journal(f"arret : {CHEMIN_STOP} est deja pose. Le retirer avant de relancer, "
                    f"avec --retirer-stop suivi du motif.")
            sys.exit(1)
    s0 = swap_mio()
    libre0 = pression_libre_pct()
    if not np.isfinite(s0) or not np.isfinite(libre0):
        sys.exit("arret : sonde memoire illisible au depart")
    journal(f"memoire au depart : swap {s0:.0f} Mio, memoire libre systeme "
            f"{libre0:.0f} pour cent")
    if np.isfinite(libre0) and libre0 < PRESSION_LIBRE_MIN_PCT:
        journal(f"arret : memoire libre systeme deja a {libre0:.0f} pour cent, sous le "
                f"seuil {PRESSION_LIBRE_MIN_PCT:.0f}")
        sys.exit(1)
    if np.isfinite(s0) and s0 > SWAP_PLAFOND_DUR_MIO:
        journal(f"arret : swap deja a {s0:.0f} Mio, au dessus du plafond dur "
                f"{SWAP_PLAFOND_DUR_MIO:.0f}")
        sys.exit(1)
    if not os.path.exists(spec["fichier"]):
        journal(f"arret : modele introuvable, {spec['fichier']}")
        sys.exit(1)
    if not attendre_la_machine(args.attente_max):
        sys.exit(1)

    fin_ts = time.time() + args.heures * 3600.0
    journal(f"fin dure dans {args.heures:.1f} h, soit a "
            f"{datetime.datetime.fromtimestamp(fin_ts):%Y-%m-%d %H:%M:%S}")

    with open(os.path.join(TRACES, "r2b-run.pid"), "w") as fh:
        fh.write(str(os.getpid()))

    arret_evt = threading.Event()
    port = args.port or premier_port_libre(depart=8200)
    if not port_libre(port):
        journal(f"arret : le port {port} est occupe")
        sys.exit(1)
    journal(f"llama-server sur le port {port}, -np {args.parallele}, "
            f"-c {args.contexte * args.parallele}, KV q8_0")

    moteur = MoteurR2b(spec["fichier"], contexte=args.contexte, parallele=args.parallele,
                      port=port, cache_kv_8bits=True)
    resume, mes, variante = [], {}, VARIANTE_EXIGEE
    plateau_charge = {"swap": None}
    sonde = threading.Thread(target=sonde_memoire, args=(arret_evt, plateau_charge),
                             kwargs={"chemin": args.journal_memoire},
                             daemon=True)
    sonde.start()
    try:
        moteur.demarrer()
        # Le plateau est releve ICI, une fois le modele charge : c'est a partir de lui que
        # la croissance est imputee au run. Le relever avant le chargement compterait les
        # 5,9 Go que le seul fichier de 11,3 Gio pousse dans le swap, et rendrait le
        # critere aussi inutilisable que celui qu'il remplace.
        plateau = swap_mio()
        libre = pression_libre_pct()
        if (not np.isfinite(plateau) or not np.isfinite(libre)
                or libre < PRESSION_LIBRE_MIN_PCT or plateau > SWAP_PLAFOND_DUR_MIO
                or stop_demande() or _arret_memoire["declenche"]):
            raise RuntimeError("arret : garde memoire apres chargement")
        plateau_charge["swap"] = plateau
        journal(f"serveur pret en {moteur.chargement_s:.1f} s. Plateau de chargement : "
                f"swap {plateau:.0f} Mio, memoire libre systeme {libre:.0f} pour cent")
        journal(f"sonde memoire lancee, une ligne par minute dans {args.journal_memoire}. "
                f"Regle amendee (resultats/r2b-amendement-regle-memoire.md) : arret si la "
                f"memoire libre systeme passe sous {PRESSION_LIBRE_MIN_PCT:.0f} pour cent, "
                f"si le swap depasse le plateau de plus de {SWAP_DELTA_MAX_MIO:.0f} Mio "
                f"(soit {plateau + SWAP_DELTA_MAX_MIO:.0f} Mio), ou s'il depasse le "
                f"plafond dur de {SWAP_PLAFOND_DUR_MIO:.0f} Mio")

        # -------------------------------------------- sonde de gabarit, puis smoke test
        enum = R2.travaux_r2(CONDITION, retenus, items, blocs, y1, table, cols_familles)
        p0, g0, j0, sys0 = next(enum)
        bloc0, options0 = utilisateur(items[j0], table)
        variante, sondes = R2.sonder_variante(moteur, spec, sys0, bloc0, options0)
        journal(f"  variante de fin retenue : {variante}")
        if variante != VARIANTE_EXIGEE:
            journal(f"arret : la sonde retient '{variante}' alors que R2 a joue "
                    f"'{VARIANTE_EXIGEE}'. Changer de variante casserait l'appariement "
                    f"avec les 150 personnes deja jouees, et l'extension n'aurait plus "
                    f"de sens. Aucune ligne de trace utile n'a ete ecrite.")
            sys.exit(2)

        journal(f"smoke test : {R2.N_SMOKE} appels reels avant d'engager le run")
        enum = R2.travaux_r2(CONDITION, retenus, items, blocs, y1, table, cols_familles)
        ok, mes, motif = R2.smoke_test(moteur, spec, variante, enum, items, table, "r2b")
        journal(f"  masse mediane {mes['masse_mediane']:.4f}, minimale "
                f"{mes['masse_minimale']:.4f}, modalites absentes "
                f"{mes['part_modalites_absentes']:.2f}, duree {mes['duree_s']:.0f} s")
        journal(f"  {motif}")
        if not ok:
            journal("le run ne demarre pas. Aucune ligne de trace utile n'a ete ecrite.")
            sys.exit(2)

        pr = R2.projeter(mes, len(retenus), 6, len(cols_familles))
        journal(f"projection {CONDITION} : {pr['secondes_par_personne']:.0f} s par "
                f"personne, {pr['appels_par_heure']:,.0f} appels/h, "
                f"{pr['heures_pour_toutes']:.2f} h pour {len(retenus)} personnes"
                .replace(",", " "))

        # -------------------------------------------- le run
        r = lancer(moteur, spec, variante, retenus, items, blocs, y1, table,
                   cols_familles, fin_ts, limite=args.essai)
        r["variante_fin"] = variante
        complets, touchees = R2.personnes_completes(r["trace"], len(cols_familles))
        r["personnes_completes"] = complets
        r["total_personnes_completes"] = len(ech0) + complets
        resume.append(r)
        journal(f"[{CONDITION}] {r['appels']} appels en {r['secondes'] / 60:.1f} min, "
                f"{r['appels_par_heure']:,.0f} appels/h, {r['rejets']} rejets, "
                f"{complets} personnes completes sur {touchees} touchees, "
                f"total {len(ech0) + complets} avec R2".replace(",", " "))
        if len(ech0) + complets < PLANCHER_LISIBILITE:
            journal(f"ATTENTION : {len(ech0) + complets} personnes completes, sous le "
                    f"plancher de lisibilite {PLANCHER_LISIBILITE} de la page de plan. "
                    f"Le rapport ne conclura pas sur H1b.")
    finally:
        arret_evt.set()
        sonde.join(timeout=35)
        try:
            moteur.arreter()
        except Exception as e:
            journal(f"arret du serveur : {e}")
        journal(f"serveur arrete. charge {os.getloadavg()}, swap {swap_mio():.0f} Mio, "
                f"swap maximal observe {_arret_memoire['swap_max']:.0f} Mio")

    chemin_resume = os.path.join(TRACES, f"r2b-resume-{CLE_MODELE}.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({"page_de_plan": "resultats/r2b-preenregistrement.md",
                   "heures_max": args.heures, "port": port,
                   "parallele": args.parallele, "contexte": args.contexte,
                   "modele": spec["nom"], "quantification": spec["quantification"],
                   "gabarit": spec["gabarit"], "variante_fin": variante,
                   "graine_echantillon": GRAINE_EXT, "par_pli": PAR_PLI,
                   "personnes_r2": len(ech0), "personnes_extension": len(retenus),
                   "swap_depart_mio": s0, "swap_max_mio": _arret_memoire["swap_max"],
                   "libre_pct_depart": libre0,
                   "regle_memoire": "amendee, resultats/r2b-amendement-regle-memoire.md",
                   "seuil_libre_pct": PRESSION_LIBRE_MIN_PCT,
                   "seuil_delta_plateau_mio": SWAP_DELTA_MAX_MIO,
                   "plafond_dur_mio": SWAP_PLAFOND_DUR_MIO,
                   "arret_memoire": _arret_memoire["declenche"],
                   "detail_arret_memoire": _arret_memoire["detail"],
                   "smoke": {k: v for k, v in mes.items() if k != "trace"},
                   "items": len(cols_familles), "conditions": resume}, fh, indent=2,
                  ensure_ascii=False)
    journal(f"resume ecrit : {chemin_resume}")
    journal(f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")


if __name__ == "__main__":
    main()
