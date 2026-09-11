"""
memoire_long_api : le meme protocole que memoire_long_gss.py (persistance contre jumeau
IA, panel GSS, horizons +2 et +4 ans), rejoue sur 4 modeles distants d'OpenRouter au lieu
du modele local gpt-oss-20b.

Statut : script d'experience, pas du code de production. Protocole decrit dans
resultats/memoire-long-preenregistrement.md, addendum API dans
resultats/memoire-long-addendum-api-2026-09-11.md (ecrit AVANT le premier appel de ce
script).

Invite et parse : IMPORTES de analyses/memoire_long_gss.py (systeme_profil, utilisateur,
parser_lettre), jamais recopies. Le tour systeme et le tour utilisateur sont envoyes tels
quels comme messages "system"/"user" d'une API de conversation ; l'habillage de gabarit
(ChatML, harmony...) est laisse au fournisseur, comme dans analyses/r6_oracle_distant.py.

Echantillon : LES MEMES PERSONNES que le run local. Ce script reproduit d'abord
l'echantillon complet par defaut de memoire_long_gss.py (memes ~133 personnes par panel,
graine 20260911, meme sequence d'appels a numpy), puis prend un sous-ensemble deterministe
(les N premieres par panel, triees par identifiant de ligne, aucun tirage supplementaire)
pour limiter le cout. Les 20 items cibles sont choisis par la meme fonction
(choisir_items), sur metadonnees seules : identiques par construction.

Cout : compteur cumule PARTAGE entre les 4 processus modele (un fichier JSON verrouille
par flock, data/traces/memoire-long-api/cout-cumule.json), lu avant chaque appel et mis a
jour avec le usage.cost reellement facture par OpenRouter. ARRET DUR au plafond (2,00 USD
par defaut pour l'etude entiere) : verifie DANS chaque tache du pool, juste avant l'appel
HTTP (pas seulement a la soumission, qui precede de loin l'execution reelle sur un pool de
plusieurs milliers de taches) ; une cellule sautee pour cause de plafond n'est PAS ecrite
dans la trace (elle reste a refaire a la prochaine reprise, contrairement a un rejet de
parse). Un fichier STOP (data/traces/memoire-long-api/STOP) est depose des que le plafond
est atteint, et `touch` de ce meme fichier arrete aussi tous les processus entre deux
appels.

Transport : client concurrent (~16 requetes simultanees, ThreadPoolExecutor), backoff sur
429 et 5xx (5 tentatives au plus, delai croissant + gigue). Aucune relance sur un echec de
parse : un echec est un rejet, compte, jamais rejoue (comme R1/R5/R6).

Entree  : data/gss-panel/*.dta (lecture seule). .env, OPENROUTER_API_KEY, lue par
          r6_oracle_distant.cle_api(), jamais imprimee.
Sortie  : data/traces/memoire-long-api/ml-<cle>.jsonl (une ligne par appel),
          ml-echantillon.csv, ml-items.csv (memes schemas que memoire_long_gss.py),
          ml-resume-<cle>.json, ml-api-run.log, cout-cumule.json.

Usage :
  .venv/bin/python analyses/memoire_long_api.py --modele gpt41nano --personnes 10 \\
      --suffixe smoke --limite 40 --plafond 0.05
  .venv/bin/python analyses/memoire_long_api.py --modele mistral-nemo --personnes 120
"""

import argparse
import collections
import datetime
import fcntl
import json
import os
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from memoire_long_gss import (GRAINE_ECHANTILLON, N_PERSONNES,  # noqa: E402
                               N_PREDICT, PANELS, SOMME_HORIZONS, VERSION_PROMPT,
                               cellules_personne, charger_panel_libelle, choisir_items,
                               colonnes_panel, echantillonner, index_existant,
                               parser_lettre, systeme_profil, utilisateur)
from a5_agents_locaux_gss import nomenclature  # noqa: E402
from a12_retest_delai import items_stanford  # noqa: E402
from r6_oracle_distant import BASE, cle_api, entetes  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data/traces/memoire-long-api")
JOURNAL_RUN = os.path.join(TRACES, "ml-api-run.log")
FICHIER_ARRET = os.path.join(TRACES, "STOP")
FICHIER_COUT = os.path.join(TRACES, "cout-cumule.json")
FICHIER_VERROU = os.path.join(TRACES, "cout.lock")

PLAFOND_DEFAUT = 2.00      # USD, plafond DUR de l'etude API entiere (les 4 modeles)
TENTATIVES_MAX = 5
CODES_REJOUABLES = (429, 500, 502, 503, 504)

N_PAR_PANEL_API_DEFAUT = 40    # 40 x 3 panels = 120 personnes par defaut

# Registre des 4 modeles API, familles distinctes. Choisis pour leur cout REEL mesure
# (5 appels par candidat, voir l'addendum) : gpt-4.1-mini/Gemini Flash/Claude Haiku sont
# 10 a 50x plus chers a ce volume d'appels (~9600 cellules/modele) et depasseraient le
# plafond a eux seuls.
MODELES_API = {
    "gpt41nano": {"modele": "openai/gpt-4.1-nano", "famille": "OpenAI"},
    "mistral-nemo": {"modele": "mistralai/mistral-nemo", "famille": "Mistral"},
    "llama31-8b": {"modele": "meta-llama/llama-3.1-8b-instruct", "famille": "Meta"},
    "nova-micro": {"modele": "amazon/nova-micro-v1", "famille": "Amazon"},
}

ITEMS_CONTEXTE_COURANTS = None   # rempli par main(), lu par les taches du pool


def arret_demande():
    return os.path.exists(FICHIER_ARRET)


def deposer_stop(motif):
    os.makedirs(TRACES, exist_ok=True)
    if not os.path.exists(FICHIER_ARRET):
        with open(FICHIER_ARRET, "w", encoding="utf-8") as fh:
            fh.write(motif + "\n")


def journaliser(message):
    os.makedirs(TRACES, exist_ok=True)
    with open(JOURNAL_RUN, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


# --------------------------------------------------------------------------------------
# 1. Comptabilite du cout, PARTAGEE entre les 4 processus modele (flock sur un fichier)
# --------------------------------------------------------------------------------------

def _lire_cout_sans_verrou():
    if not os.path.exists(FICHIER_COUT):
        return {"total_usd": 0.0, "par_modele": {}}
    try:
        with open(FICHIER_COUT, encoding="utf-8") as fh:
            d = json.load(fh)
            d.setdefault("total_usd", 0.0)
            d.setdefault("par_modele", {})
            return d
    except (json.JSONDecodeError, OSError):
        return {"total_usd": 0.0, "par_modele": {}}


def cout_total_courant():
    os.makedirs(TRACES, exist_ok=True)
    fd = os.open(FICHIER_VERROU, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, "r+", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            return _lire_cout_sans_verrou()["total_usd"]
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


def ajouter_cout(cle_modele, montant_usd):
    """Ajoute un cout reellement facture au registre partage. Rend le nouveau total."""
    montant_usd = float(montant_usd or 0.0)
    os.makedirs(TRACES, exist_ok=True)
    fd = os.open(FICHIER_VERROU, os.O_CREAT | os.O_RDWR, 0o600)
    with os.fdopen(fd, "r+", encoding="utf-8") as fh:
        fcntl.flock(fh.fileno(), fcntl.LOCK_EX)
        try:
            d = _lire_cout_sans_verrou()
            d["total_usd"] = float(d["total_usd"]) + montant_usd
            d["par_modele"][cle_modele] = float(d["par_modele"].get(cle_modele, 0.0)) \
                + montant_usd
            tmp = FICHIER_COUT + f".tmp{os.getpid()}"
            with open(tmp, "w", encoding="utf-8") as sortie:
                json.dump(d, sortie, indent=2)
                sortie.flush()
                os.fsync(sortie.fileno())
            os.replace(tmp, FICHIER_COUT)
            return d["total_usd"]
        finally:
            fcntl.flock(fh.fileno(), fcntl.LOCK_UN)


# --------------------------------------------------------------------------------------
# 2. Echantillon : reproduit l'echantillon complet par defaut du run local, puis sous
#    echantillonne deterministe (les N premieres personnes par panel).
# --------------------------------------------------------------------------------------

def echantillon_api(items_contexte, items_cibles, n_par_panel_api):
    rng = np.random.default_rng(GRAINE_ECHANTILLON)
    n_par_panel_local = max(1, N_PERSONNES // len(PANELS))
    personnes_par_panel = {}
    lignes_echantillon = []
    for nom_panel in PANELS:
        table_p, _, _, _ = charger_panel_libelle(nom_panel, items_contexte, items_cibles)
        # meme appel, meme ordre, meme rng que memoire_long_gss.main() par defaut : les
        # personnes tirees sont EXACTEMENT celles du run local a ~400 personnes.
        retenus_complet = echantillonner(nom_panel, table_p, items_contexte, items_cibles,
                                         n_par_panel_local, rng)
        sous = retenus_complet.head(n_par_panel_api)
        annees = sorted(PANELS[nom_panel]["vagues"])
        personnes_par_panel[nom_panel] = (sous, annees)
        for l in sous["ligne"].tolist():
            lignes_echantillon.append({"panel": nom_panel, "ligne": int(l)})
        print(f"  {nom_panel} : {len(sous)}/{len(retenus_complet)} personnes retenues "
              "(sous-ensemble deterministe du run local)", flush=True)
    return personnes_par_panel, lignes_echantillon


# --------------------------------------------------------------------------------------
# 3. L'appel HTTP : messages bruts (pas de gabarit), backoff 429/5xx, cout facture
# --------------------------------------------------------------------------------------

def preparer_charge(modele, messages, n_predict):
    return {
        "model": modele,
        "messages": messages,
        "temperature": 0.0,
        "max_tokens": n_predict,
        "reasoning": {"enabled": False, "exclude": True},
        "usage": {"include": True},
    }


def appeler_api(cle, modele, messages, n_predict=N_PREDICT, tentatives_max=TENTATIVES_MAX):
    """Un appel de description, avec backoff sur 429/5xx. Rend un dict avec au moins
    'texte' (chaine vide si echec definitif) et 'erreur' (None si succes)."""
    charge = preparer_charge(modele, messages, n_predict)
    donnees = json.dumps(charge).encode("utf-8")
    for tentative in range(1, tentatives_max + 1):
        debut = time.perf_counter()
        try:
            req = urllib.request.Request(BASE + "/chat/completions", data=donnees,
                                         headers=entetes(cle))
            with urllib.request.urlopen(req, timeout=180) as r:
                corps = json.loads(r.read().decode("utf-8"))
            duree_ms = (time.perf_counter() - debut) * 1000.0
            if corps.get("error"):
                statut = None
                if isinstance(corps["error"], dict):
                    try:
                        statut = int(corps["error"].get("code"))
                    except (TypeError, ValueError):
                        statut = None
                if statut in CODES_REJOUABLES and tentative < tentatives_max:
                    time.sleep(min(30, 2 ** tentative) + random.uniform(0, 1))
                    continue
                return {"texte": "", "erreur": f"erreur fournisseur {statut}",
                        "duree_ms": duree_ms}
            choix = (corps.get("choices") or [{}])[0]
            usage = corps.get("usage") or {}
            message = choix.get("message") or {}
            return {
                "texte": message.get("content") or "", "erreur": None,
                "modele_renvoye": corps.get("model"), "fournisseur": corps.get("provider"),
                "tokens_prompt": usage.get("prompt_tokens"),
                "tokens_generes": usage.get("completion_tokens"),
                "cout_usd": usage.get("cost"), "duree_ms": duree_ms,
                "tentatives": tentative,
            }
        except urllib.error.HTTPError as e:
            duree_ms = (time.perf_counter() - debut) * 1000.0
            if e.code in CODES_REJOUABLES and tentative < tentatives_max:
                time.sleep(min(30, 2 ** tentative) + random.uniform(0, 1))
                continue
            return {"texte": "", "erreur": f"HTTP {e.code}", "duree_ms": duree_ms}
        except Exception as e:                     # reseau, delai, corps illisible
            duree_ms = (time.perf_counter() - debut) * 1000.0
            if tentative < tentatives_max:
                time.sleep(min(30, 2 ** tentative) + random.uniform(0, 1))
                continue
            return {"texte": "", "erreur": type(e).__name__, "duree_ms": duree_ms}
    return {"texte": "", "erreur": "tentatives epuisees", "duree_ms": 0.0}


# --------------------------------------------------------------------------------------
# 4. Le run : file de cellules, ThreadPoolExecutor, ecriture serialisee par verrou local
# --------------------------------------------------------------------------------------

def chemin_trace(cle_modele, suffixe):
    nom = f"ml-{cle_modele}" + (("-" + suffixe) if suffixe else "")
    return os.path.join(TRACES, nom + ".jsonl")


def lancer(cle, cle_modele, modele_info, personnes_par_panel, items_cibles, familles,
           table, suffixe, plafond, parallele, limite=None, journal_tous=100):
    modele_api = modele_info["modele"]
    chemin = chemin_trace(cle_modele, suffixe)
    fait = index_existant(chemin)
    print(f"[{cle_modele}] {modele_api} ({modele_info['famille']}), trace {chemin}, "
          f"{len(fait)} appels deja faits, plafond {plafond:.2f} USD", flush=True)
    return _executer(cle, cle_modele, modele_api, personnes_par_panel, items_cibles,
                     familles, table, fait, chemin, plafond, parallele, limite,
                     journal_tous)


def _executer(cle, cle_modele, modele_api, personnes_par_panel, items_cibles, familles,
             table, fait, chemin, plafond, parallele, limite, journal_tous):
    """Soumet toutes les cellules restantes au pool ; chaque tache verifie ELLE-MEME le
    plafond/le fichier STOP juste avant d'appeler l'API (pas seulement a la soumission,
    qui precede de loin l'execution reelle sur un pool de plusieurs milliers de taches).
    Une cellule sautee pour cause de plafond n'est PAS ecrite dans la trace : elle reste
    a refaire a la prochaine reprise, contrairement a un rejet de parse."""
    verrou_ecriture = threading.Lock()
    n_soumis = n_rejets = n_sautees = 0
    motifs = collections.Counter()
    t0 = time.time()
    fh = open(chemin, "a", encoding="utf-8")

    def ecrire(d):
        with verrou_ecriture:
            fh.write(json.dumps(d, ensure_ascii=False) + "\n")
            fh.flush()

    def travail(nom_panel, sys_txt, annee1, it, h, ligne_num):
        if arret_demande() or cout_total_courant() >= plafond:
            return None
        annee_cible = annee1 + h
        usr_txt, options = utilisateur(it, table, h, annee_cible)
        messages = [{"role": "system", "content": sys_txt},
                    {"role": "user", "content": usr_txt}]
        r = appeler_api(cle, modele_api, messages)
        if r.get("erreur"):
            reponse, lettre, motif = None, None, r["erreur"]
        else:
            reponse, lettre, motif = parser_lettre(r["texte"], options)
        return {
            "version_prompt": VERSION_PROMPT, "cle_modele": cle_modele,
            "modele": modele_api, "famille": familles.get(it, "hors famille"),
            "fournisseur": r.get("fournisseur"), "panel": nom_panel,
            "ligne": ligne_num, "item": it, "horizon_ans": h,
            "annee_baseline": annee1, "annee_cible": annee_cible,
            "n_modalites": len(options), "rejet": reponse is None,
            "motif_rejet": motif or "", "sortie_brute": r.get("texte", ""),
            "reponse_modele": reponse, "lettre": lettre,
            "duree_ms": round(r.get("duree_ms", 0.0), 2),
            "tokens_prompt": r.get("tokens_prompt"),
            "tokens_generes": r.get("tokens_generes"),
            "cout_usd": r.get("cout_usd"),
        }

    arret_soumission = None
    with ThreadPoolExecutor(max_workers=parallele) as ex:
        futures = []
        for nom_panel, (table_p, annees) in personnes_par_panel.items():
            annee1 = annees[0]
            for _, ligne in table_p.iterrows():
                ligne_num = int(ligne["ligne"])
                cellules_restantes = [
                    (it, h) for it, h in cellules_personne(items_cibles)
                    if (VERSION_PROMPT, nom_panel, ligne_num, it, h) not in fait]
                if not cellules_restantes:
                    continue
                sys_txt = systeme_profil(ligne, ITEMS_CONTEXTE_COURANTS, table, annee1)
                for it, h in cellules_restantes:
                    if limite is not None and n_soumis >= limite:
                        arret_soumission = "limite"
                        break
                    futures.append(ex.submit(travail, nom_panel, sys_txt, annee1, it, h,
                                             ligne_num))
                    n_soumis += 1
                if arret_soumission:
                    break
            if arret_soumission:
                break

        n_traitees = 0
        for fut in as_completed(futures):
            d = fut.result()
            if d is None:
                n_sautees += 1
                continue
            ecrire(d)
            n_traitees += 1
            if d["cout_usd"]:
                nouveau_total = ajouter_cout(cle_modele, d["cout_usd"])
                if nouveau_total >= plafond:
                    deposer_stop(f"plafond {plafond:.2f} USD atteint ({nouveau_total:.4f})")
            if d["rejet"]:
                n_rejets += 1
                motifs[str(d["motif_rejet"])[:40]] += 1
            if n_traitees % journal_tous == 0:
                message = (f"[{cle_modele}] {n_traitees} cellules ecrites, "
                           f"{n_sautees} sautees, rejets {n_rejets}, cout etude "
                           f"{cout_total_courant():.4f} USD")
                print(message, flush=True)
                journaliser(message)

    fh.close()
    ecoule = max(time.time() - t0, 1e-9)
    n_ecrites = n_soumis - n_sautees
    return {
        "cle_modele": cle_modele, "modele": modele_api, "cellules_soumises": n_soumis,
        "cellules_ecrites": n_ecrites, "cellules_sautees_plafond": n_sautees,
        "deja_faites": len(fait), "secondes": round(ecoule, 1),
        "rejets": n_rejets, "taux_rejet": round(n_rejets / max(n_ecrites, 1), 4),
        "arret": arret_soumission or ("plafond_ou_stop" if n_sautees else None),
        "motifs_de_rejet": dict(motifs), "trace": chemin,
        "cout_cumule_etude": cout_total_courant(),
    }


def main():
    global ITEMS_CONTEXTE_COURANTS
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", required=True, choices=sorted(MODELES_API),
                    help="cle du registre MODELES_API")
    ap.add_argument("--personnes", type=int, default=N_PAR_PANEL_API_DEFAUT * len(PANELS))
    ap.add_argument("--items", type=int, default=0)
    ap.add_argument("--suffixe", default="")
    ap.add_argument("--limite", type=int, default=None)
    ap.add_argument("--parallele", type=int, default=16)
    ap.add_argument("--plafond", type=float, default=PLAFOND_DEFAUT)
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    modele_info = MODELES_API[args.modele]
    cle = cle_api()

    print(f"popsim memoire_long_api. modele {args.modele} -> {modele_info['modele']} "
          f"({modele_info['famille']}), plafond etude {args.plafond:.2f} USD, "
          f"cout deja cumule {cout_total_courant():.4f} USD", flush=True)
    journaliser(f"DEBUT modele={args.modele} ({modele_info['modele']})")

    if arret_demande():
        sys.exit(f"fichier STOP present ({FICHIER_ARRET}), arret avant tout appel")
    if cout_total_courant() >= args.plafond:
        sys.exit("plafond deja atteint pour l'etude, arret avant tout appel")

    table = nomenclature()
    tous_items = items_stanford()
    colonnes_par_panel = {nom: colonnes_panel(nom) for nom in PANELS}
    items_cibles, familles = choisir_items(tous_items, colonnes_par_panel)
    if args.items:
        items_cibles = items_cibles[:args.items]
    items_contexte = [it for it in tous_items if it not in items_cibles]
    ITEMS_CONTEXTE_COURANTS = items_contexte
    print(f"{len(items_cibles)} items cibles (identiques au run local) : {items_cibles}",
          flush=True)

    chemin_items = os.path.join(TRACES, "ml-items.csv")
    if not args.suffixe and not os.path.exists(chemin_items):
        tmp = chemin_items + f".tmp{os.getpid()}"
        pd.DataFrame([{"item": it, "famille": familles.get(it, "hors famille")}
                     for it in items_cibles]).to_csv(tmp, index=False)
        os.replace(tmp, chemin_items)

    n_par_panel_api = max(1, args.personnes // len(PANELS))
    personnes_par_panel, lignes_echantillon = echantillon_api(items_contexte, items_cibles,
                                                              n_par_panel_api)
    total_personnes = sum(len(t) for t, _ in personnes_par_panel.values())
    n_cellules = total_personnes * len(items_cibles) * len(SOMME_HORIZONS)
    print(f"{total_personnes} personnes, {n_cellules} cellules prevues pour "
          f"{args.modele}", flush=True)

    chemin_ech = os.path.join(TRACES, "ml-echantillon.csv")
    if not args.suffixe and not os.path.exists(chemin_ech):
        tmp = chemin_ech + f".tmp{os.getpid()}"
        pd.DataFrame(lignes_echantillon).to_csv(tmp, index=False)
        os.replace(tmp, chemin_ech)

    resume = lancer(cle, args.modele, modele_info, personnes_par_panel, items_cibles,
                    familles, table, args.suffixe, args.plafond, args.parallele,
                    limite=args.limite)
    print(f"[{args.modele}] {resume['cellules_ecrites']}/{resume['cellules_soumises']} "
          f"cellules ecrites en {resume['secondes'] / 60:.1f} min, {resume['rejets']} "
          f"rejets, taux {resume['taux_rejet']:.4f}, cout cumule etude "
          f"{resume['cout_cumule_etude']:.4f} USD", flush=True)
    journaliser(f"[{args.modele}] termine : {resume['cellules_ecrites']} cellules, "
                f"taux de rejet {resume['taux_rejet']:.4f}, arret={resume['arret']}")

    chemin_resume = os.path.join(
        TRACES, f"ml-resume-{args.modele}{'-' + args.suffixe if args.suffixe else ''}.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({
            "modele_cle": args.modele, "modele_api": modele_info["modele"],
            "famille": modele_info["famille"], "fin": datetime.datetime.now().isoformat(),
            "version_prompt": VERSION_PROMPT, "personnes": total_personnes,
            "items_cibles": items_cibles, "horizons": list(SOMME_HORIZONS),
            "plafond_usd": args.plafond, "resultat": resume,
        }, fh, indent=2, ensure_ascii=False)
    print(f"resume ecrit : {chemin_resume}", flush=True)
    fin_message = (f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S} "
                   f"modele={args.modele} ({resume['cellules_ecrites']} cellules)")
    print(fin_message, flush=True)
    journaliser(fin_message)


if __name__ == "__main__":
    main()
