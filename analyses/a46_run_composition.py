"""
a46_run_composition : le run court « composition ». A LANCER AU MATIN OU LA NUIT SUIVANTE.

Volet 5 de a46. C'est le SEUL script de a46 qui appelle un modele. Il n'a jamais ete
execute au moment ou il est ecrit : il est pose pret, avec son mode `--simulation` qui
exerce tout sauf le transport HTTP, et sa page de plan est
`resultats/a46-preenregistrement-composition.md`, ecrite et horodatee avant lui.

CE QU'IL FAIT
-------------
Il lit `resultats/a46-prompts-composition.csv`, produit par a46_prompts_composition.py, et
envoie chaque invite a chaque modele, une fois. 40 cellules par modele, 120 appels pour
trois modeles, quelques minutes au debit mesure en r1 (environ 3 000 cellules par heure
sur q4). Il ecrit `data/traces/a46-composition-<cle modele>.jsonl`, une ligne par appel,
au format que `a46_trois_termes.py` lit deja.

TOUT EST REPRIS DE r1, ET RIEN N'EST REECRIT
--------------------------------------------
Le lanceur de serveur, le gabarit de conversation par famille, les sequences d'arret, le
registre des modeles et les parametres d'appel sont importes de `r1_oracle_camps` tels
quels. Un seul `llama-server` a la fois, arret dans un `finally`, temperature 0, top_k 1,
cache de prefixe actif. Reprise par cle de cellule : une relance ne refait aucun appel
deja ecrit.

CE QUI CHANGE, ET POURQUOI
--------------------------
La sortie attendue n'est pas une distribution mais un entier. Le parse est donc different,
et il est aussi strict : la sortie doit contenir exactement un nombre entier de 0 a 100 et
rien d'autre. Une relance et une seule, avec un rappel de format qui ne montre AUCUN
chiffre d'exemple. C'est une lecon directe de r1 : l'invite de relance de r1 montrait une
repartition factice, et trois des quatre premieres cellules relancees l'ont recopiee a la
virgule pres. Sur une sortie a un seul nombre, montrer un exemple chiffre reviendrait a
souffler la reponse.

Usage :
  .venv/bin/python analyses/a46_run_composition.py --simulation      # aucun appel
  .venv/bin/python analyses/a46_run_composition.py --modele q4,oss20,q30 --fin 07:00
"""

import argparse
import collections
import datetime
import json
import os
import re
import sys
import time

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a46_commun as C  # noqa: E402
from a5_agents_locaux_gss import heure_de_fin, premier_port_libre  # noqa: E402
from r1_oracle_camps import (ARRETS, GGUF, MODELES, MoteurR1, gabarit)  # noqa: E402

VERSION_PROMPT = "a46-c1"
N_PREDICT = 24

# Dossier de trace. Il est une variable et non une constante pour une seule raison : le
# mode --simulation ne doit RIEN ecrire dans data/traces/, ou dorment les traces d'un run
# reel. Un essai a blanc qui salit le dossier du run serait pire que pas d'essai du tout.
TRACES_RUN = C.TRACES


def journal_chemin():
    return os.path.join(TRACES_RUN, "a46-composition-run.log")


# Une sortie valide : un entier de 0 a 100, seul sur sa ligne, gras et signe pourcent
# toleres, aucun texte apres. Rien d'autre n'est repeche.
SORTIE_VALIDE = re.compile(r"^\s*\**\s*([0-9]{1,3})\s*%?\s*\**\s*\.?\s*$")

RAPPEL = ("Your previous reply did not follow the format. Output only one line "
          "containing a single whole number between 0 and 100. No words, no percent "
          "sign, no explanation.")


def parser(texte):
    """Rend (valeur, motif). Strict : une seule ligne au format, un entier de 0 a 100.

    Les lignes vides sont ignorees. S'il reste plus d'une ligne, c'est un rejet : un
    modele qui ecrit deux nombres n'a pas repondu a la question, il en a propose deux, et
    en choisir un serait notre choix et non le sien.
    """
    lignes = [l for l in texte.splitlines() if l.strip()]
    if not lignes:
        return None, "sortie vide"
    if len(lignes) > 1:
        return None, f"{len(lignes)} lignes non vides au lieu d'une"
    m = SORTIE_VALIDE.match(lignes[0])
    if not m:
        return None, "la ligne n'est pas un entier seul"
    v = int(m.group(1))
    if not (0 <= v <= 100):
        return None, f"valeur {v} hors de [0, 100]"
    return float(v), ""


def journaliser(message):
    os.makedirs(TRACES_RUN, exist_ok=True)
    with open(journal_chemin(), "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


def chemin_trace(cle):
    return os.path.join(TRACES_RUN, f"a46-composition-{cle}.jsonl")


def index_existant(chemin):
    """Cles de cellule deja ecrites. Une ligne tronquee ne fait pas echouer la reprise."""
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
            fait.add((d.get("version_prompt"), d.get("cle_cellule")))
    return fait


def lancer(moteur, cle, info, plan, fin_ts, n_predict=N_PREDICT, simulation=None):
    """Execute un modele de bout en bout, ecriture incrementale avec flush a chaque ligne.

    `simulation`, si elle est fournie, est une fonction (prompt, rappel) -> texte. Elle
    remplace le transport HTTP et permet d'exercer le parse, la trace et la reprise sans
    aucun appel de modele.
    """
    chemin = chemin_trace(cle)
    fait = index_existant(chemin)
    arrets = ARRETS[info["gabarit"]]
    n_appels = n_rejets = n_relances = 0
    motifs = collections.Counter()
    t0 = time.time()

    with open(chemin, "a", encoding="utf-8") as fh:
        for _, r in plan.iterrows():
            if (VERSION_PROMPT, r["cle_cellule"]) in fait:
                continue
            if time.time() >= fin_ts:
                print(f"[{cle}] fin dure atteinte, arret propre", flush=True)
                break
            valeur, motif, tentatives = None, "", []
            for rappel in (False, True):
                usr = r["utilisateur"] + (("\n\n" + RAPPEL) if rappel else "")
                prompt = gabarit(info["gabarit"], r["systeme"], usr)
                if simulation is not None:
                    texte = simulation(prompt, rappel)
                    sortie = {"texte": texte, "duree_ms": 0.0,
                              "tokens_generes": None, "tokens_prompt": None}
                else:
                    sortie = moteur.decrire(prompt, n_predict, arrets)
                valeur, motif = parser(sortie["texte"])
                tentatives.append({
                    "rappel": rappel, "sortie_brute": sortie["texte"],
                    "duree_ms": round(sortie["duree_ms"], 2),
                    "tokens_generes": sortie["tokens_generes"],
                    "tokens_prompt": sortie["tokens_prompt"],
                    "motif_rejet": motif,
                })
                if valeur is not None:
                    break
                if rappel is False:
                    n_relances += 1
            rejet = valeur is None
            if rejet:
                n_rejets += 1
                motifs[motif[:40]] += 1
            ligne = {
                "version_prompt": VERSION_PROMPT,
                "cle_cellule": r["cle_cellule"],
                "cle_modele": cle, "modele": info["nom"],
                "quantification": info["quantification"], "gabarit": info["gabarit"],
                "item_as": r["item_as"], "groupe": r["groupe"],
                "groupe_en": r["groupe_en"], "parti_as": r["parti_as"],
                "role": r["role"], "ancrage": r["ancrage"], "camp": r["camp"],
                "identite": r["identite"], "variante": "principale",
                "n_tentatives": len(tentatives),
                "rejet": rejet, "motif_rejet": motif if rejet else "",
                "valeur": valeur,
                "tentatives": tentatives,
            }
            fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            fh.flush()
            n_appels += 1
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    return {"cle_modele": cle, "modele": info["nom"], "cellules": n_appels,
            "deja_faites": len(fait), "rejets": n_rejets, "relances": n_relances,
            "secondes": round(ecoule, 1), "motifs_de_rejet": dict(motifs),
            "trace": chemin}


def simulation_de_controle():
    """Sortie factice pour le mode --simulation : exerce le parse et ses trois rejets.

    Elle rend, en tournant : un entier propre, une phrase bavarde (rejet, puis relance
    reussie), et deux nombres sur deux lignes (rejet des deux tentatives). Le but n'est
    pas d'imiter un modele, c'est de verifier que la trace, la reprise et le compte des
    rejets se comportent comme prevu avant qu'on brule des appels reels.
    """
    etat = {"n": 0}
    cas = ["42", "I think about 30% of them are, but it varies.", "30\n40"]

    def rendre(prompt, rappel):
        if rappel:
            return "37"
        etat["n"] += 1
        return cas[(etat["n"] - 1) % 3]

    return rendre


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="q4,oss20,q30")
    ap.add_argument("--fin", default="07:00", help="fin dure du calcul, heure locale")
    ap.add_argument("--n-predict", type=int, default=N_PREDICT)
    ap.add_argument("--contexte", type=int, default=4096)
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--simulation", action="store_true",
                    help="aucun appel de modele : exerce le parse, la trace et la reprise")
    ap.add_argument("--traces", default=None,
                    help="dossier de trace ; obligatoire avec --simulation, pour que "
                         "l'essai a blanc n'ecrive jamais dans data/traces/")
    args = ap.parse_args()

    global TRACES_RUN
    if args.simulation and not args.traces:
        sys.exit("--simulation exige --traces vers un dossier de brouillon : un essai a "
                 "blanc n'ecrit jamais dans data/traces/")
    if args.traces:
        TRACES_RUN = args.traces
        os.makedirs(TRACES_RUN, exist_ok=True)

    chemin_plan = os.path.join(C.SORTIE, "a46-prompts-composition.csv")
    if not os.path.exists(chemin_plan):
        sys.exit("a46-prompts-composition.csv absent. Lancer d'abord "
                 "analyses/a46_prompts_composition.py")
    plan = pd.read_csv(chemin_plan)

    cles = [c.strip() for c in args.modele.split(",") if c.strip()]
    for c in cles:
        if c not in MODELES:
            sys.exit(f"modele inconnu : {c}. Cles connues : {', '.join(MODELES)}")
        if not args.simulation:
            f = os.path.join(GGUF, MODELES[c]["fichier"])
            if not os.path.exists(f):
                sys.exit(f"modele introuvable : {f}")

    fin_ts, fin_dt = heure_de_fin(args.fin)
    entete = (f"popsim a46, run composition. Depart {datetime.datetime.now():%Y-%m-%d %H:%M:%S}, "
              f"fin dure {fin_dt:%Y-%m-%d %H:%M}. {len(plan)} cellules par modele, "
              f"modeles : {', '.join(cles)}"
              + (" [SIMULATION, aucun appel]" if args.simulation else ""))
    print(entete, flush=True)
    journaliser("DEBUT " + entete)

    resumes = []
    for cle in cles:
        info = MODELES[cle]
        if args.simulation:
            resumes.append(lancer(None, cle, info, plan, fin_ts, args.n_predict,
                                  simulation=simulation_de_controle()))
            continue
        port = args.port or premier_port_libre(8099)
        moteur = MoteurR1(os.path.join(GGUF, info["fichier"]),
                          contexte=args.contexte, parallele=1, port=port,
                          cache_kv_8bits=True)
        print(f"[{cle}] {info['nom']} {info['quantification']}, gabarit "
              f"{info['gabarit']}, port {port}", flush=True)
        try:
            moteur.demarrer()
            resumes.append(lancer(moteur, cle, info, plan, fin_ts, args.n_predict))
        finally:
            moteur.arreter()

    chemin_resume = os.path.join(TRACES_RUN, "a46-composition-resume.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({"version_prompt": VERSION_PROMPT, "simulation": args.simulation,
                   "modeles": resumes}, fh, ensure_ascii=False, indent=1)
    for r in resumes:
        print(f"[{r['cle_modele']}] {r['cellules']} cellules, {r['rejets']} rejets, "
              f"{r['relances']} relances, {r['secondes']} s -> {r['trace']}", flush=True)
    journaliser("RUN TERMINE " + json.dumps(
        [{k: v for k, v in r.items() if k != "motifs_de_rejet"} for r in resumes],
        ensure_ascii=False))
    print("\nEvaluation : .venv/bin/python analyses/a46_trois_termes.py")


if __name__ == "__main__":
    main()
