"""
c7_recette : la fuite de C7 tient-elle a la GRANULARITE de l'appel, a modele EGAL ?

===========================================================================
PREENREGISTREMENT : resultats/c7-recette-preenregistrement.md, ecrit AVANT tout appel
substantiel (seuls 5 appels de calibrage, cout mesure, precedent ce texte, exactement
comme pour c7_gen -- transparence de sequence documentee dans ce meme fichier).

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Aucun pid ni
`vrai_idx` n'est jamais imprime ni ecrit dans resultats/ : seuls des taux agreges en
sortent, dans resultats/c7-recette-reidentification.csv et c7-recette-resultats.md.

CE QUI EST REPRIS TEL QUEL, SANS UNE LIGNE MODIFIEE :
  c7_gen.charger_personnes / c7_gen.charger_items   memes 60 personnes, memes 60 items
                                                     que l'attaque C7 (graine 20260912)
  c7_gen.construire_prompt / c7_gen.parser_reponse  le format d'appel unique (recette R1)
  c7_gen.cle_api / c7_gen.entetes / c7_gen.appel_chat  le client OpenRouter
  c7_gen.Budget                                     le budget cumule fichier + thread-safe
  c7_reidentification.rangs_attaque / items_communs / REF_V4 / DEMO
  c7_gen_analyse.construire_idx_mod                 la table modalite -> code entier
  a2_commun.bootstrap_personnes                     l'intervalle par reechantillonnage

CE QUI EST NOUVEAU ICI : le second bras (un appel PAR ITEM), avec un prompt inspire de
la structure publiee par l'equipe Twin (persona + UNE question + reponse numerique
seule -- cf. leur notebook de simulation, doc/carnet public, paraphrase, pas une copie
verbatim), et l'analyse comparee des deux granularites a modele constant.

N'utilise NI le runner R6 (r6_oracle_distant.py), NI son registre, NI ses fichiers
GO/STOP. Cle lue via c7_gen.cle_api (donc .env), jamais imprimee. Ecrit UNIQUEMENT dans
data/traces/c7-recette/. Aucun LLM local. ARRET DUR a 1,00 USD cumules (usage.cost).
Concurrence <= 8 requetes simultanees. Aucun autre fichier c7_* n'est modifie.

Usage :
  .venv/bin/python analyses/c7_recette.py --etape calibrage
  .venv/bin/python analyses/c7_recette.py --etape lancer --condition unique --n 20
  .venv/bin/python analyses/c7_recette.py --etape lancer --condition item --n 20
  .venv/bin/python analyses/c7_recette.py --etape analyse
  .venv/bin/python analyses/c7_recette.py --etape cout
===========================================================================
"""

import argparse
import concurrent.futures
import json
import os
import re
import sys
import threading

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                              # noqa: E402
import c7_gen as G                                                   # noqa: E402
from c7_reidentification import rangs_attaque, REF_V4, DEMO           # noqa: E402
from c7_gen_analyse import construire_idx_mod                        # noqa: E402
from a2_commun import bootstrap_personnes                            # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data", "traces", "c7-recette")
SORTIE = os.path.join(RACINE, "resultats")
os.makedirs(TRACES, exist_ok=True)

STOP_FICHIER = os.path.join(TRACES, "STOP-C7RECETTE")
COUT_FICHIER = os.path.join(TRACES, "c7-recette-cout.json")
PLAFOND_USD = 1.00
GRAINE = 20260912          # meme graine que c7_gen : memes personnes, memes items
WORKERS_MAX = 8

MODELE_CLE = "gpt41mini"
MODELE = "openai/gpt-4.1-mini"   # meme classe que l'equipe Twin (GPT4.1-mini), le moins
                                 # cher disponible via OpenRouter pour cette classe

# --------------------------------------------------------------------------------------
# Prompt du bras "item" : un appel par question, persona + UNE question, reponse
# numerique seule -- structure inspiree de leur notebook public (paraphrase, pas de
# copie verbatim), pour se rapprocher au plus pres de leur granularite d'appel.
# --------------------------------------------------------------------------------------

SYSTEME_ITEM = (
    "Tu es un systeme expert charge de predire comment une personne reelle repondrait a "
    "une question de sondage. On te donne le profil de cette personne, une question et "
    "des instructions de format. Reponds comme repondrait cette personne, en respectant "
    "strictement le format demande."
)


def construire_prompt_item(profil_texte, item):
    opts = "; ".join(f"{k + 1}={o}" for k, o in enumerate(item["options"]))
    usr = (profil_texte + "\n\n---\n\nQuestion : " + item["question"] +
           "\nOptions : " + opts +
           "\n\nReponds UNIQUEMENT par le numero de l'option choisie (un seul chiffre "
           "ou nombre), sans aucun autre texte.")
    return [{"role": "system", "content": SYSTEME_ITEM}, {"role": "user", "content": usr}]


NOMBRE_RE = re.compile(r"\d{1,2}")


def parser_item(texte, n_options):
    if not texte:
        return None
    m = NOMBRE_RE.search(texte)
    if not m:
        return None
    k = int(m.group(0))
    return k if 1 <= k <= n_options else None


# --------------------------------------------------------------------------------------
# Traces
# --------------------------------------------------------------------------------------

def nom_trace(condition):
    return os.path.join(TRACES, f"c7-recette-{MODELE_CLE}-{condition}.jsonl")


def dejafaites_unique(chemin):
    vues = set()
    if os.path.exists(chemin):
        for ligne in open(chemin, encoding="utf-8"):
            if not ligne.strip():
                continue
            try:
                vues.add(json.loads(ligne)["vrai_idx"])
            except Exception:
                continue
    return vues


def dejafaites_item(chemin):
    vues = set()
    if os.path.exists(chemin):
        for ligne in open(chemin, encoding="utf-8"):
            if not ligne.strip():
                continue
            try:
                e = json.loads(ligne)
                vues.add((e["vrai_idx"], e["code_index"]))
            except Exception:
                continue
    return vues


# --------------------------------------------------------------------------------------
# Lancement
# --------------------------------------------------------------------------------------

def lancer_unique(personnes, items, workers, budget):
    cle = G.cle_api()
    chemin = nom_trace("unique")
    faites = dejafaites_unique(chemin)
    a_faire = [p for p in personnes if p["vrai_idx"] not in faites]
    print(f"unique : {len(faites)} deja faites, {len(a_faire)} restantes, "
          f"cumul actuel {budget.cumul:.4f} USD", flush=True)
    verrou_fh = threading.Lock()

    def tache(p):
        if budget.arrete():
            return None
        messages = G.construire_prompt("R1", p["r1_texte"], items)
        rep = G.appel_chat(cle, MODELE, messages, 0.0, max_tokens=750)
        cumul = budget.ajouter(rep.get("cout", 0.0))
        ligne = {"vrai_idx": p["vrai_idx"], "condition": "unique", "modele": MODELE_CLE,
                 "cout": rep.get("cout", 0.0), "cumul_usd": round(cumul, 6)}
        if "erreur" in rep:
            ligne["rejet"] = rep["erreur"]
            ligne["codes"] = {}
            ligne["taux_parse"] = 0.0
        else:
            codes, taux = G.parser_reponse(rep["texte"], items)
            ligne["codes"] = codes
            ligne["taux_parse"] = taux
        with verrou_fh:
            with open(chemin, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
                fh.flush()
        return ligne

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(tache, p) for p in a_faire]
        for f in concurrent.futures.as_completed(futs):
            f.result()
    print(f"unique termine, cumul = {budget.cumul:.4f} USD "
          f"(arrete={budget.arrete()})", flush=True)


def lancer_item(personnes, items, workers, budget):
    cle = G.cle_api()
    chemin = nom_trace("item")
    faites = dejafaites_item(chemin)
    taches = []
    for p in personnes:
        for it in items:
            if (p["vrai_idx"], it["code_index"]) not in faites:
                taches.append((p, it))
    print(f"item : {len(faites)} appels deja faits, {len(taches)} restants "
          f"({len(personnes)} personnes x {len(items)} items), "
          f"cumul actuel {budget.cumul:.4f} USD", flush=True)
    verrou_fh = threading.Lock()

    def tache(pair):
        p, it = pair
        if budget.arrete():
            return None
        messages = construire_prompt_item(p["r1_texte"], it)
        rep = G.appel_chat(cle, MODELE, messages, 0.0, max_tokens=20)
        cumul = budget.ajouter(rep.get("cout", 0.0))
        ligne = {"vrai_idx": p["vrai_idx"], "code_index": it["code_index"],
                 "condition": "item", "modele": MODELE_CLE,
                 "cout": rep.get("cout", 0.0), "cumul_usd": round(cumul, 6)}
        if "erreur" in rep:
            ligne["rejet"] = rep["erreur"]
            ligne["code"] = None
        else:
            k = parser_item(rep["texte"], len(it["options"]))
            ligne["code"] = str(k) if k is not None else None
        with verrou_fh:
            with open(chemin, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
                fh.flush()
        return ligne

    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = [ex.submit(tache, t) for t in taches]
        for f in concurrent.futures.as_completed(futs):
            f.result()
    print(f"item termine, cumul = {budget.cumul:.4f} USD "
          f"(arrete={budget.arrete()})", flush=True)


# --------------------------------------------------------------------------------------
# Calibrage : 5 appels reels (2 unique + 3 item), pour mesurer le cout et choisir N
# --------------------------------------------------------------------------------------

def calibrage(personnes, items, budget):
    cle = G.cle_api()
    couts_unique, couts_item = [], []
    for p in personnes[:2]:
        messages = G.construire_prompt("R1", p["r1_texte"], items)
        rep = G.appel_chat(cle, MODELE, messages, 0.0, max_tokens=750)
        budget.ajouter(rep.get("cout", 0.0))
        couts_unique.append(rep.get("cout", 0.0))
        print(f"calibrage unique : cout={rep.get('cout')}, erreur={rep.get('erreur')}",
              flush=True)
    p0 = personnes[0]
    for it in items[:3]:
        messages = construire_prompt_item(p0["r1_texte"], it)
        rep = G.appel_chat(cle, MODELE, messages, 0.0, max_tokens=20)
        budget.ajouter(rep.get("cout", 0.0))
        couts_item.append(rep.get("cout", 0.0))
        print(f"calibrage item : cout={rep.get('cout')}, texte={rep.get('texte')!r}, "
              f"erreur={rep.get('erreur')}", flush=True)

    cu = float(np.mean(couts_unique)) if couts_unique else float("nan")
    ci = float(np.mean(couts_item)) if couts_item else float("nan")
    print(f"\ncout moyen mesure : unique={cu:.6f} USD/appel, item={ci:.6f} USD/appel",
          flush=True)
    for n in (60, 40, 25, 20, 15, 10):
        total = n * (cu + len(items) * ci)
        print(f"  n={n:3d} -> cout estime total = {total:.4f} USD", flush=True)
    print(f"\ncumul apres calibrage = {budget.cumul:.4f} USD", flush=True)


# --------------------------------------------------------------------------------------
# Analyse : reidentification, deux conditions + Demographics Only en repere
# --------------------------------------------------------------------------------------

def _vec_depuis_unique(chemin, items, idx_mod):
    n_items = len(items)
    lignes = [json.loads(l) for l in open(chemin, encoding="utf-8") if l.strip()]
    n = len(lignes)
    vec = np.full((n, n_items), -1, dtype=np.int16)
    vrai_idx = np.zeros(n, dtype=np.int64)
    pos_de = {it["code_index"]: p for p, it in enumerate(items)}
    for i, e in enumerate(lignes):
        vrai_idx[i] = e["vrai_idx"]
        for j_str, val in e.get("codes", {}).items():
            j = int(j_str)
            pos = pos_de.get(j)
            if pos is not None:
                vec[i, pos] = idx_mod.get(j, {}).get(str(val), -1)
    return vec, vrai_idx


def _vec_depuis_item(chemin, items, idx_mod):
    n_items = len(items)
    pos_de = {it["code_index"]: p for p, it in enumerate(items)}
    par_personne = {}
    for l in open(chemin, encoding="utf-8"):
        if not l.strip():
            continue
        e = json.loads(l)
        par_personne.setdefault(e["vrai_idx"], {})[e["code_index"]] = e.get("code")
    vrai_idx = np.array(sorted(par_personne), dtype=np.int64)
    vec = np.full((len(vrai_idx), n_items), -1, dtype=np.int16)
    for i, v in enumerate(vrai_idx):
        for j, val in par_personne[v].items():
            if val is None:
                continue
            pos = pos_de.get(j)
            if pos is not None:
                vec[i, pos] = idx_mod.get(j, {}).get(str(val), -1)
    return vec, vrai_idx


def _resume(nom, vec, vrai_idx, pool, rng, lignes):
    couverts = np.flatnonzero((vec >= 0).any(axis=1))
    if len(couverts) == 0:
        print(f"{nom} : aucune attaque exploitable", flush=True)
        return
    rang, top1, top10 = rangs_attaque(vec[couverts], pool, vrai_idx[couverts], rng)
    m_t1, b_t1, h_t1 = bootstrap_personnes(top1, 2000, [GRAINE, 1, hash(nom) % 10000])
    m_t10, b_t10, h_t10 = bootstrap_personnes(top10, 2000, [GRAINE, 2, hash(nom) % 10000])
    taux_parse = float((vec[couverts] >= 0).mean())
    ligne = {"configuration": nom, "n_attaques": len(couverts), "n_pool": pool.shape[0],
             "taux_parse_moyen": taux_parse,
             "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
             "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
             "rang_median": float(np.median(rang)), "top1_hasard": 1.0 / pool.shape[0]}
    lignes.append(ligne)
    print(f"{nom} : n={len(couverts)} parse={taux_parse:.3f} top1={m_t1:.4f} "
          f"[{b_t1:.4f};{h_t1:.4f}] top10={m_t10:.4f} rang_med={np.median(rang):.1f} "
          f"/ {pool.shape[0]}", flush=True)


def analyse():
    paq = T1.charger()
    items = G.charger_items()
    idx_mod = construire_idx_mod(paq, items)
    idx_codes = [it["code_index"] for it in items]
    pool_v4 = paq["codes"][REF_V4][:, idx_codes]

    lignes = []
    rng = np.random.default_rng([GRAINE, 1])

    chemin_u = nom_trace("unique")
    if os.path.exists(chemin_u):
        vec_u, vi_u = _vec_depuis_unique(chemin_u, items, idx_mod)
        _resume("appel unique (60 items, 1 appel/personne)", vec_u, vi_u, pool_v4, rng, lignes)
    else:
        vi_u = np.array([], dtype=np.int64)

    chemin_i = nom_trace("item")
    if os.path.exists(chemin_i):
        vec_i, vi_i = _vec_depuis_item(chemin_i, items, idx_mod)
        _resume("appel par item (1 appel/question, comme Twin)", vec_i, vi_i, pool_v4, rng, lignes)
    else:
        vi_i = np.array([], dtype=np.int64)

    # Demographics Only, restreint aux memes personnes attaquees (repere a N egal)
    vi_ref = vi_u if len(vi_u) else vi_i
    if len(vi_ref):
        demo_codes = paq["codes"][DEMO][:, idx_codes]
        vec_demo = demo_codes[vi_ref]
        _resume(f"Demographics Only (repere, n={len(vi_ref)})", vec_demo, vi_ref, pool_v4, rng, lignes)

    df = pd.DataFrame(lignes)
    df.to_csv(os.path.join(SORTIE, "c7-recette-reidentification.csv"), index=False)
    print(f"\necrit : resultats/c7-recette-reidentification.csv ({len(df)} lignes)",
          flush=True)


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--etape", required=True,
                    choices=["calibrage", "lancer", "analyse", "cout"])
    ap.add_argument("--condition", choices=["unique", "item"])
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--workers", type=int, default=WORKERS_MAX)
    args = ap.parse_args()
    workers = min(args.workers, WORKERS_MAX)

    if args.etape == "cout":
        print(json.dumps({"cumul_usd": G.Budget(chemin=COUT_FICHIER, plafond=PLAFOND_USD).cumul},
                          indent=1))
        return

    budget = G.Budget(chemin=COUT_FICHIER, plafond=PLAFOND_USD)
    if os.path.exists(STOP_FICHIER):
        sys.exit(f"STOP present : {STOP_FICHIER}")

    if args.etape == "calibrage":
        personnes = G.charger_personnes()
        items = G.charger_items()
        calibrage(personnes, items, budget)
        return

    if args.etape == "lancer":
        if not args.condition:
            sys.exit("--condition requis pour --etape lancer")
        personnes = G.charger_personnes()[:args.n]
        items = G.charger_items()
        if args.condition == "unique":
            lancer_unique(personnes, items, workers, budget)
        else:
            lancer_item(personnes, items, workers, budget)
        return

    if args.etape == "analyse":
        analyse()


if __name__ == "__main__":
    main()
