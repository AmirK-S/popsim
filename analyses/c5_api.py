"""
c5_api : c5_formulation.py rejoue sur quatre modeles distants d'OpenRouter, une famille
chacun, AVANT que les resultats du run local (gpt-oss-20b, Qwen3-30B) ne soient connus.

Statut : script d'experience, pas du code de production. Il joue EXACTEMENT le meme
protocole que `c5_formulation.py` (invite, gabarit de sortie, parse) sur des modeles
payants au lieu d'un `llama-server` local. Rien n'est recopie de `c5_formulation.py` :
`formes`, `charger_personas`, `systeme`, `utilisateur`, `effet_humain_wave1`, `parser`,
`OPTIONS`, `N_PREDICT`, `GRAINE_PERSONAS`, `GRAINE_TEST`, `VERSION_PROMPT` et
`index_existant` sont importes tels quels. Seuls le transport HTTP (une API de
conversation au lieu d'un `/completion` local) et le comptage de cout sont nouveaux.

Preenregistrement : `resultats/c5-addendum-api-2026-09-11.md`, ecrit et commis avant le
premier appel de generation de cette etude.

Modeles, quatre familles, raisonnement desactive (`reasoning: {enabled: false}`), meme
temperature 0 que `MoteurR1.decrire` :
  gpt4o-mini          openai/gpt-4o-mini
  gemini-flash-lite   google/gemini-2.5-flash-lite
  claude-haiku        anthropic/claude-3-haiku
  llama-70b           meta-llama/llama-3.3-70b-instruct

Cle : `.env`, `OPENROUTER_API_KEY`, lue par `r6_oracle_distant.cle_api`, jamais imprimee.

Cout : plafond dur 2,00 USD, PARTAGE entre les quatre modeles (ils peuvent tourner en
quatre processus a la fois). Le grand livre `data/traces/c5-api/cout-cumule.json` est mis
a jour sous verrou fichier (`fcntl.flock`, valable entre threads et entre processus) apres
chaque appel ; des qu'il atteint le plafond, `data/traces/c5-api/STOP` est pose et plus
aucun appel n'est soumis, dans ce processus comme dans les trois autres. Le cout de
reference est `usage.cost` (mesure par OpenRouter) ; a defaut (fournisseur qui ne le rend
pas), estimation par jetons x prix du catalogue au moment du choix des modeles.

Concurrence : `ThreadPoolExecutor`, 16 appels a la fois par processus (`--parallele`).
Transport : 5 tentatives au plus par appel, attente croissante (2, 4, 8, 16, 32 s) sur
HTTP 429 et 5xx et sur les erreurs reseau ; toute autre erreur HTTP est un rejet immediat,
jamais rejoue. Le fournisseur aval renvoye (`response.provider`) est note sur chaque ligne.

Trace : `data/traces/c5-api/c5-api-<cle>[-<suffixe>].jsonl`, memes champs que la trace de
`c5_formulation.py` (donc lue sans changement par `c5_analyse.py --dossier
data/traces/c5-api`), plus `modele_api`, `famille`, `fournisseur`, `cout_usd`. Reprise sur
le meme index (version_prompt, pid, forme) : une relance ne refait aucun appel deja ecrit.

Arret : `touch data/traces/c5-api/STOP` arrete tous les modeles entre deux vagues d'appels,
trace fermee, resume ecrit, code de sortie 0. Le plafond de cout pose le meme fichier.

Usage :
  .venv/bin/python analyses/c5_api.py --modele llama-70b --test           # 10 x 22 = 220
  .venv/bin/python analyses/c5_api.py --modele gpt4o-mini,gemini-flash-lite,claude-haiku,llama-70b
"""

import argparse
import concurrent.futures
import datetime
import fcntl
import json
import os
import sys
import threading
import time
import urllib.error
import urllib.request

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from c5_formulation import (GRAINE_PERSONAS, GRAINE_TEST, N_PREDICT, OPTIONS,
                             VERSION_PROMPT, charger_personas, effet_humain_wave1,
                             formes, index_existant, parser, systeme, utilisateur)
from r6_oracle_distant import cle_api

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data/traces/c5-api")
FICHIER_ARRET = os.path.join(TRACES, "STOP")
LEDGER = os.path.join(TRACES, "cout-cumule.json")
JOURNAL_RUN = os.path.join(TRACES, "c5-api-run.log")

BASE = "https://openrouter.ai/api/v1"
PLAFOND_USD = 2.00

# Prix de repli, USD par jeton, releves sur GET /models le 11 septembre 2026, employes
# UNIQUEMENT quand `usage.cost` est absent de la reponse.
API_MODELES = {
    "gpt4o-mini": {"id": "openai/gpt-4o-mini", "nom": "GPT-4o mini", "famille": "OpenAI",
                   "prix_prompt": 0.00000015, "prix_completion": 0.0000006},
    "gemini-flash-lite": {"id": "google/gemini-2.5-flash-lite",
                           "nom": "Gemini 2.5 Flash Lite", "famille": "Google",
                           "prix_prompt": 0.0000001, "prix_completion": 0.0000004},
    "claude-haiku": {"id": "anthropic/claude-3-haiku", "nom": "Claude 3 Haiku",
                      "famille": "Anthropic", "prix_prompt": 0.00000025,
                      "prix_completion": 0.00000125},
    "llama-70b": {"id": "meta-llama/llama-3.3-70b-instruct",
                  "nom": "Llama 3.3 70B Instruct", "famille": "Meta",
                  "prix_prompt": 0.0000001, "prix_completion": 0.00000032},
}

ATTENTES = (2, 4, 8, 16, 32)
MAX_TENTATIVES = 5


def journaliser(message):
    os.makedirs(TRACES, exist_ok=True)
    with open(JOURNAL_RUN, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


# --------------------------------------------------------------------------------------
# 1. Le grand livre de cout, partage entre threads et entre processus (fcntl.flock)
# --------------------------------------------------------------------------------------

def _verrouiller():
    os.makedirs(TRACES, exist_ok=True)
    fd = os.open(LEDGER + ".lock", os.O_CREAT | os.O_RDWR, 0o600)
    fcntl.flock(fd, fcntl.LOCK_EX)
    return fd


def _deverrouiller(fd):
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)


def lire_cout_cumule():
    if not os.path.exists(LEDGER):
        return 0.0
    try:
        with open(LEDGER, encoding="utf-8") as fh:
            return float(json.load(fh).get("total_usd", 0.0))
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return 0.0


def ajouter_cout(delta_usd):
    """Ajoute delta_usd au grand livre partage. Renvoie le nouveau total, verrouille."""
    fd = _verrouiller()
    try:
        total = lire_cout_cumule() + max(float(delta_usd or 0.0), 0.0)
        with open(LEDGER, "w", encoding="utf-8") as fh:
            json.dump({"total_usd": total,
                       "maj": datetime.datetime.now().isoformat()}, fh)
        return total
    finally:
        _deverrouiller(fd)


def poser_arret(raison):
    os.makedirs(TRACES, exist_ok=True)
    if not os.path.exists(FICHIER_ARRET):
        with open(FICHIER_ARRET, "w", encoding="utf-8") as fh:
            fh.write(raison + "\n")


def arret_demande():
    return os.path.exists(FICHIER_ARRET) or lire_cout_cumule() >= PLAFOND_USD


# --------------------------------------------------------------------------------------
# 2. Le client HTTP : un appel, puis la reprise sur 429 et 5xx
# --------------------------------------------------------------------------------------

def _entetes(cle):
    return {"Authorization": "Bearer " + cle, "Content-Type": "application/json",
            "HTTP-Referer": "popsim", "X-Title": "popsim"}


def appeler(cle, modele_id, sys_txt, usr_txt, n_predict=N_PREDICT, timeout=60):
    charge = {
        "model": modele_id,
        "messages": [{"role": "system", "content": sys_txt},
                     {"role": "user", "content": usr_txt}],
        "temperature": 0.0,
        "max_tokens": n_predict,
        "reasoning": {"enabled": False, "exclude": True},
        "usage": {"include": True},
    }
    donnees = json.dumps(charge).encode("utf-8")
    req = urllib.request.Request(BASE + "/chat/completions", data=donnees,
                                  headers=_entetes(cle))
    debut = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            corps = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            corps_err = json.loads(e.read().decode("utf-8", "replace"))
        except (json.JSONDecodeError, OSError):
            corps_err = {}
        return {"erreur": f"HTTP {e.code}", "statut": e.code,
                "duree_ms": (time.perf_counter() - debut) * 1000.0,
                "motif": str(corps_err.get("error"))[:300]}
    except Exception as e:                                    # reseau, delai
        return {"erreur": type(e).__name__, "statut": None,
                "duree_ms": (time.perf_counter() - debut) * 1000.0, "motif": str(e)[:300]}
    duree = (time.perf_counter() - debut) * 1000.0
    if corps.get("error"):
        return {"erreur": "erreur_fournisseur", "statut": None, "duree_ms": duree,
                 "motif": str(corps["error"])[:300]}
    choix = (corps.get("choices") or [{}])[0]
    usage = corps.get("usage") or {}
    message = choix.get("message") or {}
    return {
        "texte": message.get("content") or "",
        "fournisseur": corps.get("provider"),
        "modele_renvoye": corps.get("model"),
        "jetons_entree": usage.get("prompt_tokens"),
        "jetons_sortie": usage.get("completion_tokens"),
        "cout": usage.get("cost"),
        "duree_ms": duree,
    }


def appeler_avec_reprise(cle, modele_id, sys_txt, usr_txt, n_predict=N_PREDICT):
    """5 tentatives au plus, attente croissante, uniquement sur 429/5xx/reseau."""
    dernier = None
    for tentative in range(MAX_TENTATIVES):
        r = appeler(cle, modele_id, sys_txt, usr_txt, n_predict)
        dernier = r
        if "erreur" not in r:
            return r
        statut = r.get("statut")
        rejouable = statut == 429 or statut is None or (statut is not None
                                                          and 500 <= statut < 600)
        if not rejouable or tentative == MAX_TENTATIVES - 1:
            return r
        time.sleep(ATTENTES[min(tentative, len(ATTENTES) - 1)])
    return dernier


# --------------------------------------------------------------------------------------
# 3. Une cellule : un appel, un parse, une ligne de trace, un ajout au grand livre
# --------------------------------------------------------------------------------------

def cout_estime(info, jetons_entree, jetons_sortie):
    if jetons_entree is None or jetons_sortie is None:
        return 0.0
    return jetons_entree * info["prix_prompt"] + jetons_sortie * info["prix_completion"]


def tache(cle_val, cle_modele, info, p, paire, version, var, libelle):
    sys_txt = systeme(p)
    usr_txt = utilisateur(libelle)
    r = appeler_avec_reprise(cle_val, info["id"], sys_txt, usr_txt)

    if "erreur" in r:
        distribution, somme = None, float("nan")
        motif = f"{r['erreur']} : {r.get('motif', '')}"[:300]
        cout, jent, jsor, fournisseur, texte = 0.0, None, None, None, ""
    else:
        texte = r["texte"]
        distribution, somme, motif = parser(texte, OPTIONS)
        jent, jsor = r.get("jetons_entree"), r.get("jetons_sortie")
        cout = r.get("cout")
        if cout is None:
            cout = cout_estime(info, jent, jsor)
        fournisseur = r.get("fournisseur")

    rejet = distribution is None
    ligne = {
        "version_prompt": VERSION_PROMPT, "cle_modele": cle_modele, "modele": info["nom"],
        "modele_api": info["id"], "famille": info["famille"], "fournisseur": fournisseur,
        "pid": p["pid"], "camp": p["camp"], "paire": paire, "version_forme": version,
        "forme": var, "libelle": libelle,
        "tokens_generes": jsor, "tokens_prompt": jent, "cout_usd": cout,
        "sortie_brute": texte, "rejet": rejet, "motif_rejet": motif if rejet else "",
        "somme_brute": None if somme != somme else round(somme, 4),
        "distribution": distribution,
    }
    total = ajouter_cout(cout)
    return ligne, total


# --------------------------------------------------------------------------------------
# 4. Le run d'un modele : vagues de `--parallele` appels, arret propre au plafond/STOP
# --------------------------------------------------------------------------------------

def chemin_trace(cle_modele, suffixe):
    nom = f"c5-api-{cle_modele}" + (("-" + suffixe) if suffixe else "")
    return os.path.join(TRACES, nom + ".jsonl")


def lancer(cle_modele, personas, les_formes, suffixe="", parallele=16, limite=None):
    info = API_MODELES[cle_modele]
    chemin = chemin_trace(cle_modele, suffixe)
    fait = index_existant(chemin)
    cle_val = cle_api()

    a_faire = [(p, paire, version, var, libelle)
               for p in personas
               for paire, version, var, libelle in les_formes
               if (VERSION_PROMPT, p["pid"], var) not in fait]
    if limite is not None:
        a_faire = a_faire[:limite]
    message = (f"[{cle_modele}] {len(fait)} deja faits, {len(a_faire)} a faire, "
               f"trace {chemin}")
    print(message, flush=True)
    journaliser(message)

    n_appels = n_rejets = 0
    arret = False
    t0 = time.time()
    verrou_fh = threading.Lock()

    with open(chemin, "a", encoding="utf-8") as fh:
        with concurrent.futures.ThreadPoolExecutor(max_workers=parallele) as ex:
            index_courant = 0
            en_vol = {}
            while index_courant < len(a_faire) or en_vol:
                if not arret and arret_demande():
                    arret = True
                    message = f"[{cle_modele}] ARRET (STOP ou plafond), plus rien soumis"
                    print(message, flush=True)
                    journaliser(message)
                while (not arret and len(en_vol) < parallele * 2
                       and index_courant < len(a_faire)):
                    args = a_faire[index_courant]
                    index_courant += 1
                    fut = ex.submit(tache, cle_val, cle_modele, info, *args)
                    en_vol[fut] = True
                if not en_vol:
                    break
                termines, _ = concurrent.futures.wait(
                    list(en_vol), return_when=concurrent.futures.FIRST_COMPLETED)
                for fut in termines:
                    del en_vol[fut]
                    ligne, total = fut.result()
                    with verrou_fh:
                        fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
                        fh.flush()
                    n_appels += 1
                    if ligne["rejet"]:
                        n_rejets += 1
                    if total >= PLAFOND_USD:
                        poser_arret(f"plafond {PLAFOND_USD:.2f} USD atteint (cle "
                                    f"{cle_modele})")
                    if n_appels % 100 == 0:
                        message = (f"[{cle_modele}] {n_appels}/{len(a_faire)} appels, "
                                   f"cout cumule (toutes cles) {total:.4f} USD, "
                                   f"rejets {n_rejets}")
                        print(message, flush=True)
                        journaliser(message)
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    resume = {
        "cle_modele": cle_modele, "modele": info["nom"], "trace": chemin,
        "appels": n_appels, "deja_faits": len(fait), "rejets": n_rejets,
        "taux_rejet": round(n_rejets / n_appels, 4) if n_appels else 0.0,
        "secondes": round(ecoule, 1),
        "appels_par_heure": round(n_appels / ecoule * 3600, 1) if n_appels else 0.0,
        "arret_par_plafond_ou_stop": os.path.exists(FICHIER_ARRET),
        "cout_cumule_usd": round(lire_cout_cumule(), 4),
    }
    message = (f"[{cle_modele}] {n_appels} appels en {ecoule / 60:.1f} min, "
               f"{n_rejets} rejets, cout cumule {resume['cout_cumule_usd']:.4f} USD")
    print(message, flush=True)
    journaliser(message)
    return resume


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default=",".join(API_MODELES),
                    help="cles de API_MODELES, separees par des virgules")
    ap.add_argument("--personas", type=int, default=100,
                    help="personas PAR CAMP ; 100 donne les 300 du preenregistrement")
    ap.add_argument("--test", action="store_true",
                    help="10 personas de test, tirees hors de l'echantillon de 300, "
                         "jamais melangees a l'analyse finale")
    ap.add_argument("--suffixe", default="")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal d'appels par modele, pour un smoke test")
    ap.add_argument("--parallele", type=int, default=16)
    args = ap.parse_args()

    cles = [c.strip() for c in args.modele.split(",") if c.strip()]
    for c in cles:
        if c not in API_MODELES:
            sys.exit(f"modele inconnu : {c}. Cles connues : {', '.join(API_MODELES)}")

    os.makedirs(TRACES, exist_ok=True)
    if arret_demande():
        sys.exit(f"arret deja demande ({FICHIER_ARRET} present ou plafond deja atteint) "
                  ": retire le fichier avant de relancer, si c'est voulu.")

    humain = effet_humain_wave1()
    humain.to_csv(os.path.join(TRACES, "c5-effet-humain.csv"), index=False)

    les_formes = formes()
    if args.test:
        production = charger_personas(100, GRAINE_PERSONAS)
        ids_production = [p["pid"] for p in production]
        personas = charger_personas(4, GRAINE_TEST, exclure=ids_production)[:10]
        suffixe = args.suffixe or "test"
    else:
        personas = charger_personas(args.personas, GRAINE_PERSONAS)
        suffixe = args.suffixe

    chemin_personas = os.path.join(
        TRACES, f"c5-personas{'-' + suffixe if suffixe else ''}.csv")
    if not os.path.exists(chemin_personas):
        pd.DataFrame(personas).to_csv(chemin_personas, index=False)
    print(f"{len(personas)} personas, {len(les_formes)} formes, "
          f"{len(personas) * len(les_formes)} appels prevus par modele", flush=True)

    resumes = []
    for cle_modele in cles:
        if arret_demande():
            print(f"arret demande, {cle_modele} non lance", flush=True)
            break
        resumes.append(lancer(cle_modele, personas, les_formes, suffixe=suffixe,
                               parallele=args.parallele, limite=args.limite))

    chemin_resume = os.path.join(
        TRACES, f"c5-api-resume{'-' + suffixe if suffixe else ''}.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({"modeles": resumes,
                    "cout_cumule_usd": round(lire_cout_cumule(), 4)}, fh, indent=2,
                   ensure_ascii=False)
    print(f"resume ecrit : {chemin_resume}", flush=True)


if __name__ == "__main__":
    main()
