#!/usr/bin/env python3
"""
c7_pilote_regeneration : chiffrer, puis (si et seulement si la configuration du bras de
titre est reconstituable) regenerer deux fois la meme configuration sur le meme bassin.

Preenregistrement : `resultats/c7-pilote-regeneration-preenregistrement.md`, commis AVANT
le premier appel payant.

POURQUOI CE SCRIPT EXISTE
-------------------------
`agent/mesures/variance-generation` a etabli que 99,07 % de la variabilite du taux de
re-identification vient de la configuration de generation et 0,93 % des personnes, alors
que les intervalles publies sont des bootstraps SUR LES PERSONNES. Aucune condition ne
possede deux executions. Le chiffre de titre (20,6803 %, bras `JSON Persona - GPT4.1`) est
un tirage unique, et c'est le maximum des huit bras admissibles. Une seule grandeur est
cherchee : l'ecart entre deux executions de la MEME configuration.

CE QUE CE SCRIPT NE PEUT PAS FAIRE, ET POURQUOI C'EST ECRIT ICI
---------------------------------------------------------------
Le bras `JSON Persona - GPT4.1` n'a PAS ete produit par ce depot. C'est un jeu de jumeaux
telecharge tel quel depuis `LLM-Digital-Twin/Twin-2K-500` (cf. `a8_telecharger_twin_llm.py`
l.33-47). Le paquet local ne contient ni invite, ni message systeme, ni code de generation
(`twin-ab-audit-provenance-2026-09-11.md`). La configuration amont publique ne publie
qu'UNE configuration (`text_simulation/configs/openai_config.yaml` du depot
`tianyipeng-lab/Digital-Twin-Simulation`) : `gpt-4.1-mini-2025-04-14`, temperature 0.0,
et un pipeline persona->TEXTE. Ce n'est ni le bon modele, ni le bon format de persona, et
sa temperature contredit celle de l'article (0,7 par defaut).

=> La classe `ConfigBras` ci-dessous est donc une RECONSTRUCTION APPROCHEE, declaree comme
telle par son champ `reconstitue=False`. Elle sert a CHIFFRER le cout (etape 0), pas a
pretendre reproduire le bras. Le cout, lui, ne depend pas du libelle de l'invite : il
depend de la taille d'entree, du tarif et du nombre d'appels, tous trois etablis.

DEPENSE
-------
Fournisseur : OpenRouter, cle `OPENROUTER_API_KEY` lue dans `.env` par
`r6_oracle_distant.cle_api`, jamais imprimee. Le worktree n'ayant pas de `.env`, `--env`
pointe explicitement le depot principal.

Trois couches, comme le reste du depot (METHODE.md §2.11) :
  1. Plafonds declares au preenregistrement et LUS ICI (PLAFOND_DUR_USD, ARRET_INTERNE_USD,
     PLAFOND_ETAPE0_USD).
  2. Grand livre `data/traces/c7-pilote-regeneration/cout-cumule.json` sous `fcntl.flock`,
     valable entre threads et entre processus ; fichier STOP des que le plafond est atteint.
  3. Cout de reference `usage.cost` annonce par OpenRouter, JAMAIS une estimation ; recoupe
     par la variation de `total_usage` sur `GET /credits` lue avant et apres.

CONFIDENTIALITE
---------------
Aucune prose personnelle n'est ecrite nulle part : la persona n'est que COMPTEE (caracteres,
jetons). La trace ne porte que pid, compteurs, cout, et la reponse du modele. Aucun
appariement individuel, aucun taux par personne n'est imprime.

Usage :
  .venv/bin/python analyses/c7_pilote_regeneration.py --etape 0 --personnes 5
  .venv/bin/python analyses/c7_pilote_regeneration.py --chiffrage-seul     # zero appel
"""

from __future__ import annotations

import argparse
import dataclasses
import datetime
import fcntl
import json
import os
import sys
import time
import urllib.error
import urllib.request

import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from r6_oracle_distant import cle_api  # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(RACINE, "data")
TRACES = os.path.join(DATA, "traces", "c7-pilote-regeneration")
LEDGER = os.path.join(TRACES, "cout-cumule.json")
FICHIER_ARRET = os.path.join(TRACES, "STOP")
JOURNAL = os.path.join(TRACES, "run.log")
PARQUET = os.path.join(DATA, "twin2k500", "wave_persona_chunk_001.parquet")

BASE = "https://openrouter.ai/api/v1"

# --- Plafonds : ceux du preenregistrement, lus ici et nulle part ailleurs ---------------
PLAFOND_MANDAT_USD = 60.00       # plafond absolu du mandat, jamais franchi
PLAFOND_DUR_USD = 25.00          # plafond dur de ce script
ARRET_INTERNE_USD = 22.50        # marge : on s'arrete avant le plafond dur
PLAFOND_ETAPE0_USD = 2.00        # etape 0 (chiffrage sur 5 personnes)

# --- Tarif catalogue, UNIQUEMENT pour la projection AVANT appel -------------------------
# Releve sur GET /models au moment de l'execution (voir `tarif_catalogue`). Ces valeurs de
# repli ne servent jamais a declarer un cout constate : celui-la vient de `usage.cost`.
MODELE_ID = "openai/gpt-4.1"
PRIX_REPLI = {"prompt": 2.00e-6, "completion": 8.00e-6}  # USD par jeton

ATTENTES = (2, 4, 8, 16, 32)
MAX_TENTATIVES = 5

# Message systeme : la SEULE invite publiee en amont (openai_config.yaml). Elle n'est pas
# celle du bras de titre — voir le docstring. Recopiee verbatim pour que la reconstruction
# soit inspectable, pas pour pretendre qu'elle est la bonne.
SYSTEME_AMONT = (
    "You are an AI assistant. Your task is to answer the 'New Survey Question' as if you "
    "are the person described in the 'Persona Profile' (which consists of their past "
    "survey responses). \nAdhere to the persona by being consistent with their previous "
    "answers and stated characteristics. \nFollow all instructions provided for the new "
    "question carefully regarding the format of your answer."
)


@dataclasses.dataclass(frozen=True)
class ConfigBras:
    """Configuration de generation. `reconstitue` dit si elle fait foi."""

    nom: str
    modele: str
    temperature: float
    max_tokens: int
    systeme: str
    format_persona: str
    reconstitue: bool
    motif_non_reconstitue: str = ""


# La configuration du bras de titre, telle qu'on peut l'approcher — et pas mieux.
BRAS_TITRE = ConfigBras(
    nom="JSON Persona - GPT4.1",
    modele=MODELE_ID,
    temperature=0.0,
    max_tokens=16384,
    systeme=SYSTEME_AMONT,
    format_persona="wave1_3_persona_json",
    reconstitue=False,
    motif_non_reconstitue=(
        "Le depot ne contient ni invite ni code de generation (sorties formatees seulement). "
        "Le depot amont public ne publie qu'une configuration, pour gpt-4.1-mini en persona "
        "TEXTE, et sa temperature (0,0) contredit celle de l'article (0,7 par defaut). "
        "Aucune source ne fait correspondre l'etiquette 'JSON Persona - GPT4.1' a une "
        "configuration precise. La temperature est precisement le parametre qui gouverne la "
        "grandeur cherchee par ce pilote."
    ),
)


def journaliser(message: str) -> None:
    os.makedirs(TRACES, exist_ok=True)
    ligne = f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}"
    with open(JOURNAL, "a", encoding="utf-8") as fh:
        fh.write(ligne + "\n")
    print(ligne, flush=True)


# ---------------------------------------------------------------------------------------
# 1. Grand livre, verrouille entre threads et entre processus
# ---------------------------------------------------------------------------------------

def _verrouiller():
    os.makedirs(TRACES, exist_ok=True)
    fd = os.open(LEDGER + ".lock", os.O_CREAT | os.O_RDWR, 0o600)
    fcntl.flock(fd, fcntl.LOCK_EX)
    return fd


def _deverrouiller(fd) -> None:
    fcntl.flock(fd, fcntl.LOCK_UN)
    os.close(fd)


def lire_cout_cumule() -> float:
    if not os.path.exists(LEDGER):
        return 0.0
    try:
        with open(LEDGER, encoding="utf-8") as fh:
            return float(json.load(fh).get("total_usd", 0.0))
    except (json.JSONDecodeError, OSError, TypeError, ValueError):
        return 0.0


def ajouter_cout(delta_usd: float) -> float:
    fd = _verrouiller()
    try:
        total = lire_cout_cumule() + max(float(delta_usd or 0.0), 0.0)
        with open(LEDGER, "w", encoding="utf-8") as fh:
            json.dump({"total_usd": total, "maj": datetime.datetime.now().isoformat()}, fh)
        return total
    finally:
        _deverrouiller(fd)


def poser_arret(raison: str) -> None:
    os.makedirs(TRACES, exist_ok=True)
    if not os.path.exists(FICHIER_ARRET):
        with open(FICHIER_ARRET, "w", encoding="utf-8") as fh:
            fh.write(raison + "\n")
    journaliser(f"ARRET POSE : {raison}")


def arret_demande(plafond: float) -> bool:
    return os.path.exists(FICHIER_ARRET) or lire_cout_cumule() >= plafond


# ---------------------------------------------------------------------------------------
# 2. Lecture du compteur OpenRouter (gratuite, lecture seule)
# ---------------------------------------------------------------------------------------

def lire_credits(cle: str) -> dict:
    req = urllib.request.Request(BASE + "/credits", headers=_entetes(cle))
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode("utf-8")).get("data", {})


def tarif_catalogue(cle: str, modele_id: str) -> dict:
    """Prix par jeton releve sur GET /models. Sert a la PROJECTION, jamais au constat."""
    try:
        req = urllib.request.Request(BASE + "/models", headers=_entetes(cle))
        with urllib.request.urlopen(req, timeout=30) as r:
            corps = json.loads(r.read().decode("utf-8"))
        for m in corps.get("data", []):
            if m.get("id") == modele_id:
                p = m.get("pricing", {})
                return {"prompt": float(p.get("prompt", 0.0)),
                        "completion": float(p.get("completion", 0.0)),
                        "source": "GET /models"}
    except (urllib.error.URLError, OSError, ValueError, KeyError) as e:
        journaliser(f"tarif_catalogue : repli sur les prix codes ({type(e).__name__})")
    return dict(PRIX_REPLI, source="repli code en dur")


# ---------------------------------------------------------------------------------------
# 3. Construction de l'entree : persona JSON + questions de vague 4 sans reponse
# ---------------------------------------------------------------------------------------

def blocs_sans_reponse(brut: str) -> str:
    """Retire toute reponse des blocs de vague 4. Ne renvoie QUE des questions."""
    blocs = json.loads(brut)
    for bloc in blocs:
        for q in bloc.get("Questions", []):
            q.pop("Answers", None)
    return json.dumps(blocs, ensure_ascii=False)


def construire_entree(ligne: pd.Series, config: ConfigBras) -> tuple[str, str]:
    """Renvoie (systeme, utilisateur). La prose n'est jamais journalisee, seulement comptee."""
    persona = ligne[config.format_persona]
    questions = blocs_sans_reponse(ligne["wave4_Q_wave1_3_A"])
    utilisateur = (
        "Persona Profile (the person's past survey responses, JSON):\n"
        f"{persona}\n\n"
        "New Survey Questions (JSON blocks, answers removed):\n"
        f"{questions}\n\n"
        "Answer every question as this person would. Return a single JSON object mapping "
        "each QuestionID to its answer, using exactly the response options provided. "
        "Do not omit any question."
    )
    return config.systeme, utilisateur


# ---------------------------------------------------------------------------------------
# 4. Le client : un appel, reprise sur 429 et 5xx
# ---------------------------------------------------------------------------------------

def _entetes(cle: str) -> dict:
    return {"Authorization": "Bearer " + cle, "Content-Type": "application/json",
            "HTTP-Referer": "popsim", "X-Title": "popsim"}


def appeler(cle: str, config: ConfigBras, sys_txt: str, usr_txt: str, timeout: int = 300) -> dict:
    charge = {
        "model": config.modele,
        "messages": [{"role": "system", "content": sys_txt},
                     {"role": "user", "content": usr_txt}],
        "temperature": config.temperature,
        "max_tokens": config.max_tokens,
        "usage": {"include": True},
    }
    req = urllib.request.Request(BASE + "/chat/completions",
                                 data=json.dumps(charge).encode("utf-8"),
                                 headers=_entetes(cle))
    debut = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            corps = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            detail = json.loads(e.read().decode("utf-8", "replace"))
        except (json.JSONDecodeError, OSError):
            detail = {}
        return {"erreur": f"HTTP {e.code}", "statut": e.code,
                "duree_ms": (time.perf_counter() - debut) * 1000.0,
                "motif": str(detail.get("error"))[:300]}
    except Exception as e:                                     # reseau, delai
        return {"erreur": type(e).__name__, "statut": None,
                "duree_ms": (time.perf_counter() - debut) * 1000.0, "motif": str(e)[:300]}

    duree = (time.perf_counter() - debut) * 1000.0
    if corps.get("error"):
        return {"erreur": "erreur_fournisseur", "statut": None, "duree_ms": duree,
                "motif": str(corps["error"])[:300]}
    usage = corps.get("usage") or {}
    choix = (corps.get("choices") or [{}])[0]
    return {
        "texte": (choix.get("message") or {}).get("content") or "",
        "jetons_prompt": int(usage.get("prompt_tokens") or 0),
        "jetons_completion": int(usage.get("completion_tokens") or 0),
        "cout_usd": float(usage.get("cost") or 0.0),
        "cout_mesure": usage.get("cost") is not None,
        "fournisseur": corps.get("provider"),
        "generation_id": corps.get("id"),
        "duree_ms": duree,
    }


def appeler_avec_reprise(cle: str, config: ConfigBras, sys_txt: str, usr_txt: str) -> dict:
    for tentative in range(MAX_TENTATIVES):
        r = appeler(cle, config, sys_txt, usr_txt)
        if "erreur" not in r:
            return r
        rejouable = r.get("statut") in (429, 500, 502, 503, 504) or r.get("statut") is None
        if not rejouable or tentative == MAX_TENTATIVES - 1:
            return r
        attente = ATTENTES[min(tentative, len(ATTENTES) - 1)]
        journaliser(f"  reprise dans {attente}s ({r['erreur']})")
        time.sleep(attente)
    return r


# ---------------------------------------------------------------------------------------
# 5. Etape 0 : chiffrer sur N personnes, puis extrapoler
# ---------------------------------------------------------------------------------------

def chiffrage_a_priori(df: pd.DataFrame, config: ConfigBras, prix: dict, n: int) -> dict:
    """Projection AVANT tout appel : taille d'entree mesuree, cout projete au catalogue."""
    tailles, tailles_q = [], []
    for _, ligne in df.head(n).iterrows():
        s, u = construire_entree(ligne, config)
        tailles.append(len(s) + len(u))
        tailles_q.append(len(blocs_sans_reponse(ligne["wave4_Q_wave1_3_A"])))
    moy = sum(tailles) / len(tailles)
    # 1 jeton ~ 4 caracteres : approximation declaree, remplacee par la mesure apres appel.
    jetons = moy / 4.0
    return {
        "n_chiffre": n,
        "caracteres_entree_moyens": moy,
        "caracteres_questions_moyens": sum(tailles_q) / len(tailles_q),
        "jetons_entree_estimes": jetons,
        "appels_par_personne": 1,
        "prix_prompt_par_jeton": prix["prompt"],
        "prix_completion_par_jeton": prix["completion"],
        "source_prix": prix["source"],
        "cout_projete_par_personne": jetons * prix["prompt"] + 4000 * prix["completion"],
    }


def etape0(cle: str, df: pd.DataFrame, config: ConfigBras, n: int, prix: dict) -> dict:
    """N personnes reellement appelees, cout CONSTATE (usage.cost), jamais estime."""
    os.makedirs(TRACES, exist_ok=True)
    trace = os.path.join(TRACES, "etape0.jsonl")
    lignes, echecs = [], 0

    for _, ligne in df.head(n).iterrows():
        if arret_demande(PLAFOND_ETAPE0_USD):
            journaliser("etape 0 interrompue : plafond atteint ou STOP present")
            break
        pid = int(ligne["pid"])
        sys_txt, usr_txt = construire_entree(ligne, config)
        r = appeler_avec_reprise(cle, config, sys_txt, usr_txt)
        if "erreur" in r:
            echecs += 1
            journaliser(f"  pid {pid} : ECHEC {r['erreur']} {r.get('motif','')[:120]}")
            continue
        total = ajouter_cout(r["cout_usd"])
        enr = {
            "pid": pid,
            "caracteres_entree": len(sys_txt) + len(usr_txt),
            "jetons_prompt": r["jetons_prompt"],
            "jetons_completion": r["jetons_completion"],
            "cout_usd": r["cout_usd"],
            "cout_mesure": r["cout_mesure"],
            "fournisseur": r["fournisseur"],
            "caracteres_reponse": len(r["texte"]),
            "duree_ms": r["duree_ms"],
        }
        lignes.append(enr)
        with open(trace, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(enr, ensure_ascii=False) + "\n")
        journaliser(f"  pid {pid} : {r['jetons_prompt']} jetons entree, "
                    f"{r['jetons_completion']} sortie, {r['cout_usd']:.10f} USD "
                    f"(cumul {total:.10f})")
        if total >= ARRET_INTERNE_USD:
            poser_arret(f"arret interne atteint : {total:.10f} USD")
            break

    if not lignes:
        return {"n_reussis": 0, "n_echecs": echecs}

    n_ok = len(lignes)
    cout_total = sum(l["cout_usd"] for l in lignes)
    par_personne = cout_total / n_ok
    return {
        "n_reussis": n_ok,
        "n_echecs": echecs,
        "cout_total_usd": cout_total,
        "cout_par_personne_usd": par_personne,
        "jetons_prompt_moyens": sum(l["jetons_prompt"] for l in lignes) / n_ok,
        "jetons_completion_moyens": sum(l["jetons_completion"] for l in lignes) / n_ok,
        "caracteres_entree_moyens": sum(l["caracteres_entree"] for l in lignes) / n_ok,
        "tous_couts_mesures": all(l["cout_mesure"] for l in lignes),
        "extrapolation_150": par_personne * 150,
        "extrapolation_2058": par_personne * 2058,
    }


# ---------------------------------------------------------------------------------------
# 6. Entree en matiere
# ---------------------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--etape", type=int, default=0, choices=[0])
    ap.add_argument("--personnes", type=int, default=5)
    ap.add_argument("--env", default=os.path.join(RACINE, ".env"),
                    help="chemin du .env portant OPENROUTER_API_KEY (jamais imprimee)")
    ap.add_argument("--chiffrage-seul", action="store_true",
                    help="projection uniquement, zero appel payant")
    args = ap.parse_args()

    if not os.path.exists(PARQUET):
        print(f"donnees absentes : {PARQUET}", file=sys.stderr)
        return 2

    df = pd.read_parquet(PARQUET).sort_values("pid").reset_index(drop=True)
    config = BRAS_TITRE

    journaliser("=" * 78)
    journaliser(f"bras vise : {config.nom} | modele {config.modele} | "
                f"temperature {config.temperature} | max_tokens {config.max_tokens}")
    if not config.reconstitue:
        journaliser("AVERTISSEMENT : configuration NON RECONSTITUEE. "
                    + config.motif_non_reconstitue)

    if args.chiffrage_seul:
        prix = dict(PRIX_REPLI, source="repli code en dur (aucun appel)")
        proj = chiffrage_a_priori(df, config, prix, args.personnes)
        print(json.dumps(proj, indent=2, ensure_ascii=False))
        return 0

    cle = cle_api(args.env)

    avant = lire_credits(cle)
    usage_avant = float(avant.get("total_usage", 0.0))
    journaliser(f"total_usage avant : {usage_avant!r}")

    prix = tarif_catalogue(cle, config.modele)
    proj = chiffrage_a_priori(df, config, prix, args.personnes)
    journaliser("projection avant appel : " + json.dumps(proj, ensure_ascii=False))

    reel = etape0(cle, df, config, args.personnes, prix)

    apres = lire_credits(cle)
    usage_apres = float(apres.get("total_usage", 0.0))
    journaliser(f"total_usage apres : {usage_apres!r}")

    resume = {
        "bras": config.nom,
        "configuration_reconstituee": config.reconstitue,
        "motif": config.motif_non_reconstitue,
        "modele": config.modele,
        "temperature": config.temperature,
        "projection": proj,
        "constate": reel,
        "total_usage_avant": usage_avant,
        "total_usage_apres": usage_apres,
        "delta_compteur_usd": usage_apres - usage_avant,
        "grand_livre_usd": lire_cout_cumule(),
        "plafond_mandat_usd": PLAFOND_MANDAT_USD,
    }
    with open(os.path.join(TRACES, "etape0-resume.json"), "w", encoding="utf-8") as fh:
        json.dump(resume, fh, indent=2, ensure_ascii=False)
    print(json.dumps(resume, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
