"""
c7_gen : la fuite de C7 survit-elle a des jumeaux QUE NOUS fabriquons ?

===========================================================================
PREENREGISTREMENT : resultats/c7-gen-preenregistrement.md, ecrit AVANT tout appel de
generation. Conception, mesures, comparateurs, predictions chiffrees et controle de
contamination y sont declares.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Aucun pid n'est
jamais imprime ni ecrit dans resultats/ ; seul l'indice de position interne (vrai_idx)
sert, jamais publie non plus. Seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                     les quinze tables de Twin
  c7_reidentification.items_communs     la selection des 60 items toujours renseignes
  c7_reidentification.REF_V4/REF_V13    les noms des deux cibles

CE QUI EST NOUVEAU ICI : la construction du profil riche (R1) et demographique (R2) a
partir de wave_persona_chunk_001.parquet, le prompt qui demande les 60 reponses d'un
coup, le client OpenRouter concurrent avec budget dur, et la sonde de contamination.

N'utilise NI le runner R6 (r6_oracle_distant.py), NI son registre, NI ses fichiers
GO/STOP. Cle lue directement dans .env, jamais imprimee. Ecrit uniquement dans
data/traces/c7-gen/. Aucun LLM local. ARRET DUR a 1,50 USD cumules (usage.cost annonce).

Usage :
  .venv/bin/python analyses/c7_gen.py --etape items
  .venv/bin/python analyses/c7_gen.py --etape personnes
  .venv/bin/python analyses/c7_gen.py --etape calibrage
  .venv/bin/python analyses/c7_gen.py --etape lancer --modele llama31-8b --recette R1 \
      --temperature 0 --n 200 --workers 12
  .venv/bin/python analyses/c7_gen.py --etape contamination
  .venv/bin/python analyses/c7_gen.py --etape cout
===========================================================================
"""

import argparse
import concurrent.futures
import fcntl
import json
import os
import random
import re
import sys
import threading
import time
import urllib.error
import urllib.request

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                            # noqa: E402
from c7_reidentification import items_communs, REF_V4, REF_V13     # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data", "traces", "c7-gen")
RACINE_TWIN = os.path.join(RACINE, "data", "twin2k500")
os.makedirs(TRACES, exist_ok=True)

BASE = "https://openrouter.ai/api/v1"
STOP_FICHIER = os.path.join(TRACES, "STOP-C7GEN")
COUT_FICHIER = os.path.join(TRACES, "c7-gen-cout.json")
PLAFOND_USD = 1.50
GRAINE = 20260912
N_PERSONNES = 200
TRONCATURE_R1_CHARS = 8000     # longueur fixe declaree du profil riche (risque : coupe
                               # potentiellement une question en cours de milieu de bloc)
N_TIRAGES_LIENS = 20
N_BOOTSTRAP = 2000

# Les trois modeles, familles distinctes, bon marche, choisis via GET /models le
# 2026-09-12. Coupures de connaissances et sources dans le preenregistrement section 5.
# openai/gpt-5-nano a ete essaye puis ecarte : HTTP 400 « Reasoning is mandatory for this
# endpoint and cannot be disabled », incompatible avec le raisonnement desactive impose
# a toutes les conditions. Remplace par deepseek/deepseek-v4-flash (raisonnement off
# verifie par un appel reel avant le run).
MODELES = {
    "llama31-8b": "meta-llama/llama-3.1-8b-instruct",   # Meta, coupure dec. 2023 (< mai 2025)
    "qwen37-flash": "qwen/qwen3.7-flash",                # Alibaba, coupure ~2026 (> mai 2025)
    "deepseek-v4": "deepseek/deepseek-v4-flash",         # DeepSeek, doc. publiee 2026-04-27 (> mai 2025)
}
MODELE_TEMPERATURE_1 = "qwen37-flash"   # la condition temp=1 x R1 supplementaire

RECETTES = ("R1", "R2")


# --------------------------------------------------------------------------------------
# 0. Cle API, lue uniquement ici, jamais importee de r6_oracle_distant.
# --------------------------------------------------------------------------------------

def cle_api():
    chemin = os.path.join(RACINE, ".env")
    if not os.path.exists(chemin):
        sys.exit(f"fichier absent : {chemin}")
    for ligne in open(chemin, encoding="utf-8"):
        if ligne.startswith("OPENROUTER_API_KEY="):
            v = ligne.split("=", 1)[1].strip().strip('"').strip("'")
            if v:
                return v
    sys.exit("OPENROUTER_API_KEY absente de .env")


def entetes(cle):
    return {"Authorization": "Bearer " + cle, "Content-Type": "application/json",
            "HTTP-Referer": "popsim", "X-Title": "popsim-c7-gen"}


# --------------------------------------------------------------------------------------
# 1. Les 60 items : question, sous-libelle, options -- depuis question_catalog.json
# --------------------------------------------------------------------------------------

def _charger_catalogue_et_mapping():
    csvd = os.path.join(RACINE_TWIN, "question_catalog_and_human_response_csv")
    cat = json.load(open(os.path.join(csvd, "question_catalog.json"), encoding="utf-8"))
    byqid = {e["QuestionID"]: e for e in cat}
    mapf = json.load(open(os.path.join(RACINE_TWIN, "llm",
                          "wave4_formatted_to_catalog_mapping.json"), encoding="utf-8"))
    m = {e["formatted_column"]: e for e in mapf}
    return byqid, m


def construire_items(chemin=None):
    """Les 60 items communs de C7 (repris via items_communs), avec question, sous
    libelle (matrices) et options, dans l'ordre de code_index (colonne dans les codes)."""
    chemin = chemin or os.path.join(TRACES, "c7-gen-items.json")
    paq = T1.charger()
    idx = items_communs(paq["codes"], [REF_V4, REF_V13])
    byqid, m = _charger_catalogue_et_mapping()
    items = []
    for j in idx:
        col = paq["colonnes"][j]
        e = m[col]
        qid, ccol = e["QuestionID"], e["catalog_csv_column"]
        q = byqid[qid]
        if q["QuestionType"] == "Matrix":
            k = q["csv_columns"].index(ccol)
            texte = q["QuestionText"].strip() + " -- " + q["Rows"][k].strip()
            options = q["Columns"]
        else:
            texte = q["QuestionText"].strip()
            options = q["Options"]
        items.append({"code_index": int(j), "colonne": col, "question": texte,
                     "options": options})
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(items, fh, ensure_ascii=False, indent=1)
    print(f"{len(items)} items ecrits dans {chemin}", flush=True)
    return items


def charger_items():
    chemin = os.path.join(TRACES, "c7-gen-items.json")
    if not os.path.exists(chemin):
        return construire_items(chemin)
    return json.load(open(chemin, encoding="utf-8"))


# --------------------------------------------------------------------------------------
# 2. Les 200 personnes : profil riche R1 (tronque) et demographique R2
# --------------------------------------------------------------------------------------

def _bloc_demographics(persona_json_str):
    j = json.loads(persona_json_str)
    blocs = [b for b in j if isinstance(b, dict) and b.get("BlockName") == "Demographics"]
    if not blocs:
        return ""
    lignes = []
    for q in blocs[0].get("Questions", []):
        rep = q.get("Answers", {}).get("SelectedText")
        if rep is None:
            continue
        lignes.append(f"{q['QuestionText'].strip()}\nReponse : {rep}")
    return "\n\n".join(lignes)


def construire_personnes(chemin=None):
    chemin = chemin or os.path.join(TRACES, "c7-gen-personnes.json")
    paq = T1.charger()
    pos = {p: i for i, p in enumerate(paq["ids"])}
    df = pd.read_parquet(os.path.join(RACINE_TWIN, "wave_persona_chunk_001.parquet"))
    df = df[df["pid"].astype(int).isin(pos)].reset_index(drop=True)
    rng = random.Random(GRAINE)
    pids = sorted(df["pid"].astype(int).tolist())
    tires = sorted(rng.sample(pids, min(N_PERSONNES, len(pids))))
    df = df.set_index(df["pid"].astype(int))
    personnes = []
    for pid in tires:
        ligne = df.loc[pid]
        r1 = str(ligne["wave1_3_persona_text"])[:TRONCATURE_R1_CHARS]
        r2 = _bloc_demographics(ligne["wave1_3_persona_json"])
        personnes.append({"vrai_idx": int(pos[pid]), "r1_texte": r1, "r2_texte": r2})
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(personnes, fh, ensure_ascii=False)
    print(f"{len(personnes)} personnes ecrites dans {chemin} "
          f"(sur {len(pids)} disposant d'un profil vagues 1-3 local)", flush=True)
    return personnes


def charger_personnes():
    chemin = os.path.join(TRACES, "c7-gen-personnes.json")
    if not os.path.exists(chemin):
        return construire_personnes(chemin)
    return json.load(open(chemin, encoding="utf-8"))


# --------------------------------------------------------------------------------------
# 3. Le prompt : les 60 reponses en un seul appel, format numerote strict
# --------------------------------------------------------------------------------------

CONSIGNE = (
    "Tu incarnes une personne reelle a partir des informations ci-dessous, et tu "
    "reponds AU SONDAGE comme cette personne y repondrait. Pour chacune des {n} "
    "questions numerotees, choisis UN SEUL numero d'option. "
    "Reponds STRICTEMENT par {n} lignes, une par question, au format exact :\n"
    "N) k\n"
    "ou N est le numero de la question et k le numero de l'option choisie. "
    "Aucun texte avant, apres, ou entre les lignes. Aucune explication."
)


def bloc_questions(items):
    morceaux = []
    for n, it in enumerate(items, start=1):
        opts = "; ".join(f"{k+1}={o}" for k, o in enumerate(it["options"]))
        morceaux.append(f"{n}) {it['question']}\nOptions : {opts}")
    return "\n\n".join(morceaux)


def construire_prompt(recette, profil_texte, items):
    sys_txt = CONSIGNE.format(n=len(items))
    if recette == "R1":
        contexte = ("Voici ce que cette personne a repondu a un questionnaire anterieur "
                   "(vagues 1 a 3), tel quel :\n\n" + profil_texte)
    elif recette == "R2":
        contexte = "Voici les seules informations demographiques connues sur cette personne :\n\n" + profil_texte
    else:
        raise ValueError("recette inconnue : " + recette)
    usr_txt = contexte + "\n\n---\n\n" + bloc_questions(items)
    return [{"role": "system", "content": sys_txt}, {"role": "user", "content": usr_txt}]


LIGNE_RE = re.compile(r"^\s*(\d{1,3})\s*[\).:\-]\s*(\d{1,2})\b")


def parser_reponse(texte, items):
    """Renvoie (dict code_index -> code_str, taux_parse) sur les items fournis."""
    par_n = {}
    for ligne in (texte or "").splitlines():
        m = LIGNE_RE.match(ligne)
        if not m:
            continue
        n, k = int(m.group(1)), int(m.group(2))
        if 1 <= n <= len(items):
            par_n.setdefault(n, k)
    codes = {}
    for n, it in enumerate(items, start=1):
        k = par_n.get(n)
        if k is not None and 1 <= k <= len(it["options"]):
            codes[it["code_index"]] = str(k)
    taux = len(codes) / len(items)
    return codes, taux


# --------------------------------------------------------------------------------------
# 4. Le budget cumule, partage entre threads, persistant entre relances
# --------------------------------------------------------------------------------------

class Budget:
    """Cumul partage entre THREADS (verrou local) et entre PROCESSUS (fcntl sur le
    fichier de cout) : plusieurs conditions peuvent tourner en parallele sans jamais
    perdre une mise a jour ni depasser silencieusement le plafond."""

    def __init__(self, chemin=COUT_FICHIER, plafond=PLAFOND_USD):
        self.chemin = chemin
        self.plafond = plafond
        self.verrou = threading.Lock()
        if not os.path.exists(self.chemin):
            with open(self.chemin, "w", encoding="utf-8") as fh:
                json.dump({"cumul": 0.0}, fh)
        self.cumul = self._lire_disque()

    def _lire_disque(self):
        with open(self.chemin, encoding="utf-8") as fh:
            fcntl.flock(fh, fcntl.LOCK_SH)
            try:
                return float(json.load(fh).get("cumul", 0.0))
            finally:
                fcntl.flock(fh, fcntl.LOCK_UN)

    def ajouter(self, cout):
        with self.verrou:
            with open(self.chemin, "r+", encoding="utf-8") as fh:
                fcntl.flock(fh, fcntl.LOCK_EX)
                try:
                    actuel = float(json.load(fh).get("cumul", 0.0))
                    actuel += max(0.0, float(cout or 0.0))
                    fh.seek(0)
                    fh.truncate()
                    json.dump({"cumul": actuel}, fh)
                    fh.flush()
                    os.fsync(fh.fileno())
                finally:
                    fcntl.flock(fh, fcntl.LOCK_UN)
            self.cumul = actuel
            return actuel

    def place(self):
        return self._lire_disque() < self.plafond

    def arrete(self):
        return os.path.exists(STOP_FICHIER) or not self.place()


# --------------------------------------------------------------------------------------
# 5. Le client OpenRouter : un appel, backoff sur 429/5xx, jamais de secret journalise
# --------------------------------------------------------------------------------------

def appel_chat(cle, modele, messages, temperature, max_tokens=750, tentatives=4):
    charge = {
        "model": modele, "messages": messages, "temperature": float(temperature),
        "max_tokens": max_tokens, "usage": {"include": True},
        "reasoning": {"enabled": False, "exclude": True},
    }
    donnees = json.dumps(charge).encode("utf-8")
    attente = 3
    for essai in range(tentatives):
        req = urllib.request.Request(BASE + "/chat/completions", data=donnees,
                                     headers=entetes(cle))
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                corps = json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            corps_err = e.read().decode("utf-8", "replace")[:300]
            if e.code in (429, 500, 502, 503, 504) and essai < tentatives - 1:
                time.sleep(attente)
                attente *= 3
                continue
            return {"erreur": f"HTTP {e.code}", "detail": corps_err, "cout": 0.0}
        except Exception as e:                                    # reseau, timeout
            if essai < tentatives - 1:
                time.sleep(attente)
                attente *= 3
                continue
            return {"erreur": type(e).__name__, "cout": 0.0}
        if corps.get("error"):
            return {"erreur": "erreur_fournisseur", "detail": str(corps["error"])[:300],
                    "cout": 0.0}
        choix = (corps.get("choices") or [{}])[0]
        usage = corps.get("usage") or {}
        message = choix.get("message") or {}
        return {"texte": message.get("content") or "",
                "cout": float(usage.get("cost") or 0.0),
                "jetons_entree": usage.get("prompt_tokens"),
                "jetons_sortie": usage.get("completion_tokens")}
    return {"erreur": "epuise", "cout": 0.0}


# --------------------------------------------------------------------------------------
# 6. Un run : une condition (modele, recette, temperature), N personnes, reprise
# --------------------------------------------------------------------------------------

def nom_trace(modele_cle, recette, temperature):
    t = "t0" if float(temperature) == 0 else f"t{temperature}".replace(".", "p")
    return os.path.join(TRACES, f"c7-gen-{modele_cle}-{recette}-{t}.jsonl")


def dejafaites(chemin):
    vues = set()
    if os.path.exists(chemin):
        for ligne in open(chemin, encoding="utf-8"):
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                vues.add(json.loads(ligne)["vrai_idx"])
            except Exception:
                continue
    return vues


def lancer_condition(modele_cle, recette, temperature, n, workers, budget=None):
    cle = cle_api()
    modele = MODELES[modele_cle]
    items = charger_items()
    personnes = charger_personnes()[:n]
    chemin = nom_trace(modele_cle, recette, temperature)
    faites = dejafaites(chemin)
    a_faire = [p for p in personnes if p["vrai_idx"] not in faites]
    budget = budget or Budget()
    print(f"{modele_cle}/{recette}/t={temperature} : {len(faites)} deja faites, "
          f"{len(a_faire)} restantes, cumul actuel {budget.cumul:.4f} USD", flush=True)
    verrou_fh = threading.Lock()

    def tache(p):
        if budget.arrete():
            return None
        messages = construire_prompt(recette, p[f"{recette.lower()}_texte"], items)
        rep = appel_chat(cle, modele, messages, temperature)
        cumul = budget.ajouter(rep.get("cout", 0.0))
        ligne = {"vrai_idx": p["vrai_idx"], "modele": modele_cle, "recette": recette,
                "temperature": temperature, "cout": rep.get("cout", 0.0),
                "cumul_usd": round(cumul, 6)}
        if "erreur" in rep:
            ligne["rejet"] = rep["erreur"]
            ligne["codes"] = {}
            ligne["taux_parse"] = 0.0
        else:
            codes, taux = parser_reponse(rep["texte"], items)
            ligne["codes"] = codes
            ligne["taux_parse"] = taux
            ligne["jetons_entree"] = rep.get("jetons_entree")
            ligne["jetons_sortie"] = rep.get("jetons_sortie")
        with verrou_fh:
            with open(chemin, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
                fh.flush()
        return ligne

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(tache, p) for p in a_faire]
        for f in concurrent.futures.as_completed(futs):
            f.result()

    if budget.arrete():
        print(f"ARRET : plafond {budget.plafond} USD atteint ou STOP-C7GEN present, "
              f"cumul = {budget.cumul:.4f} USD", flush=True)
    print(f"termine {modele_cle}/{recette}/t={temperature}, cumul = {budget.cumul:.4f} USD",
          flush=True)


# --------------------------------------------------------------------------------------
# 7. Sonde de contamination : completion verbatim, jeu reel vs questionnaire fictif
# --------------------------------------------------------------------------------------

QUESTIONNAIRE_FICTIF = (
    "Quelle est votre boisson favorite parmi les suivantes ?\n"
    "Question Type: Single Choice\nOptions:\n"
    "  1 - Infusion de baies de sureau glacee\n  2 - Nectar de fruit de la passion tiede\n"
    "  3 - Cafe a la cardamome frappe\n  4 - The au gingembre confit\n"
    "Answer: 2 - Nectar de fruit de la passion tiede\n\n"
    "A quelle frequence pratiquez-vous la sculpture sur bois flotte ?\n"
    "Question Type: Single Choice\nOptions:\n"
    "  1 - Jamais\n  2 - Rarement\n  3 - Parfois\n  4 - Souvent\n"
    "Answer: 3 - Parfois\n\n"
    "Quel est votre animal imaginaire prefere ?\n"
    "Question Type: Single Choice\nOptions:\n"
    "  1 - Griffon des dunes\n  2 - Loutre-dragon\n  3 - Lynx des brumes\n"
    "Answer: 1 - Griffon des dunes\n\n"
)

CONSIGNE_CONTAMINATION = (
    "Voici le debut exact d'un document. Continue-le VERBATIM, mot pour mot, comme si "
    "tu recopiais la suite exacte du document. Ne reformule rien. Si tu ne connais pas "
    "la suite exacte, ecris seulement : INCONNU."
)


def _sous_chaine_commune_max(a, b, min_len=20):
    """Longueur du plus long chevauchement entre le debut de b et une sous-chaine de a,
    a partir d'une fenetre glissante simple (suffisant pour une sonde, pas un aligneur)."""
    meilleur = 0
    for L in range(min(len(a), len(b)), min_len - 1, -1):
        if b[:L] and b[:L] in a:
            meilleur = L
            break
    return meilleur


def lancer_contamination(n_personnes=8, budget=None):
    cle = cle_api()
    personnes = charger_personnes()[:n_personnes]
    budget = budget or Budget()
    chemin = os.path.join(TRACES, "c7-gen-contamination.jsonl")
    faites = set()
    if os.path.exists(chemin):
        for ligne in open(chemin, encoding="utf-8"):
            try:
                e = json.loads(ligne)
                faites.add((e["vrai_idx"], e["modele"], e["condition"]))
            except Exception:
                pass

    lignes_a_faire = []
    for p in personnes:
        vrai = p["r1_texte"]
        coupe = min(600, len(vrai) // 2)
        extrait_vrai, suite_vraie = vrai[:coupe], vrai[coupe:coupe + 300]
        coupe_f = min(600, len(QUESTIONNAIRE_FICTIF) - 1)
        extrait_f = (QUESTIONNAIRE_FICTIF * 3)[:coupe_f]
        suite_f = (QUESTIONNAIRE_FICTIF * 3)[coupe_f:coupe_f + 300]
        for modele_cle, modele in MODELES.items():
            for cond, extrait, suite in (("reel", extrait_vrai, suite_vraie),
                                         ("fictif", extrait_f, suite_f)):
                if (p["vrai_idx"], modele_cle, cond) in faites:
                    continue
                lignes_a_faire.append((p["vrai_idx"], modele_cle, modele, cond, extrait, suite))

    print(f"{len(lignes_a_faire)} appels de contamination a faire "
          f"(cumul actuel {budget.cumul:.4f} USD)", flush=True)
    verrou_fh = threading.Lock()

    def tache(item):
        vrai_idx, modele_cle, modele, cond, extrait, suite = item
        if budget.arrete():
            return
        messages = [{"role": "system", "content": CONSIGNE_CONTAMINATION},
                    {"role": "user", "content": extrait}]
        rep = appel_chat(cle, modele, messages, 0.0, max_tokens=200)
        cumul = budget.ajouter(rep.get("cout", 0.0))
        texte = rep.get("texte", "") or ""
        chevauchement = _sous_chaine_commune_max(suite, texte)
        ligne = {"vrai_idx": vrai_idx, "modele": modele_cle, "condition": cond,
                "chevauchement_verbatim_chars": chevauchement,
                "verbatim_20plus": bool(chevauchement >= 20),
                "erreur": rep.get("erreur"), "cout": rep.get("cout", 0.0),
                "cumul_usd": round(cumul, 6)}
        with verrou_fh:
            with open(chemin, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
                fh.flush()

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(tache, lignes_a_faire))
    print(f"contamination terminee, cumul = {budget.cumul:.4f} USD", flush=True)


# --------------------------------------------------------------------------------------
# 8. CLI
# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--etape", required=True,
                   choices=["items", "personnes", "calibrage", "lancer",
                            "contamination", "cout"])
    ap.add_argument("--modele", choices=list(MODELES))
    ap.add_argument("--recette", choices=list(RECETTES))
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--n", type=int, default=N_PERSONNES)
    ap.add_argument("--workers", type=int, default=12)
    args = ap.parse_args()

    if args.etape == "items":
        construire_items()
    elif args.etape == "personnes":
        construire_personnes()
    elif args.etape == "calibrage":
        lancer_condition("llama31-8b", "R1", 0.0, 10, workers=5)
        chemin = nom_trace("llama31-8b", "R1", 0.0)
        taux = [json.loads(l)["taux_parse"] for l in open(chemin, encoding="utf-8")
               if l.strip()]
        print(f"taux de parse moyen sur {len(taux)} essais : "
              f"{sum(taux)/len(taux):.3f}" if taux else "aucun essai", flush=True)
    elif args.etape == "lancer":
        if not args.modele or not args.recette:
            sys.exit("--modele et --recette requis pour --etape lancer")
        lancer_condition(args.modele, args.recette, args.temperature, args.n, args.workers)
    elif args.etape == "contamination":
        lancer_contamination()
    elif args.etape == "cout":
        print(json.dumps({"cumul_usd": Budget().cumul}, indent=1))


if __name__ == "__main__":
    main()
