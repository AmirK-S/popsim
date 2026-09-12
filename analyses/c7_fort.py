"""
c7_fort : la fuite de C7 revient-elle avec un modele FORT et un appel PAR ITEM ?

===========================================================================
PREENREGISTREMENT : resultats/c7-fort-preenregistrement.md, ecrit AVANT tout appel
payant (aucun calibrage n'a precede ce texte, contrairement a c7_recette).

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Aucun pid ni
`vrai_idx` n'est jamais imprime ni ecrit dans resultats/ : seuls des taux agreges en
sortent, dans resultats/c7-fort-reidentification.csv et c7-fort-resultats.md.

CE QUI EST REPRIS TEL QUEL, SANS UNE LIGNE MODIFIEE :
  c7_gen.charger_personnes / c7_gen.charger_items      memes 60 personnes/items que C7
  c7_gen.cle_api / c7_gen.appel_chat / c7_gen.Budget    client OpenRouter, budget partage
  c7_recette.SYSTEME_ITEM / construire_prompt_item /    la recette "un appel par item",
    parser_item                                         inspiree de la structure Twin
  c7_reidentification.rangs_attaque / items_communs /   l'attaque de reidentification
    REF_V4 / REF_V13
  c7_gen_analyse.construire_idx_mod / exactitude_propre la table modalite->code, l'exactitude
  a2_commun.bootstrap_personnes                         l'IC par reechantillonnage de personnes
  t1_commun.charger (T1.REF, T1.PLANCHER, seg S_gra)    segmentation et plancher humain
  t1_mesures.chute                                      la chute sous permutation intra-segment

CE QUI EST NOUVEAU ICI : le modele fort (openai/gpt-4.1, classe Twin) applique a la
recette "item" deja codee par c7_recette, et la fidelite individuelle (chute sous
permutation intra-segment S_gra, normalisee au plancher humain sur le meme perimetre,
convention de resultats/c7-compromis.csv).

N'utilise NI le runner R6, NI son registre, NI ses fichiers GO/STOP. Cle lue via
c7_gen.cle_api (donc .env), jamais imprimee. Ecrit UNIQUEMENT dans data/traces/c7-fort/.
Aucun LLM local. ARRET DUR a 5,00 USD cumules (usage.cost). Concurrence <= 8 requetes
simultanees. Aucun autre fichier c7_* modifie.

Usage :
  .venv/bin/python analyses/c7_fort.py --etape calibrage
  .venv/bin/python analyses/c7_fort.py --etape test3
  .venv/bin/python analyses/c7_fort.py --etape lancer --n 30
  .venv/bin/python analyses/c7_fort.py --etape analyse
  .venv/bin/python analyses/c7_fort.py --etape cout
===========================================================================
"""

import argparse
import concurrent.futures
import json
import os
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
from c7_recette import SYSTEME_ITEM, construire_prompt_item, parser_item  # noqa: E402,F401
from c7_reidentification import rangs_attaque, REF_V4, REF_V13, items_communs  # noqa: E402
from c7_gen_analyse import construire_idx_mod, exactitude_propre     # noqa: E402
from a2_commun import bootstrap_personnes                            # noqa: E402
from t1_mesures import chute                                         # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data", "traces", "c7-fort")
SORTIE = os.path.join(RACINE, "resultats")
os.makedirs(TRACES, exist_ok=True)

STOP_FICHIER = os.path.join(TRACES, "STOP-C7FORT")
COUT_FICHIER = os.path.join(TRACES, "c7-fort-cout.json")
PLAFOND_USD = 5.00
GRAINE = 20260912          # meme graine que c7_gen/c7_recette : memes personnes, memes items
WORKERS_MAX = 8
N_MIN = 25
N_CIBLE = 30

MODELE_CLE = "gpt41-fort"
MODELE = "openai/gpt-4.1"   # classe Twin (JSON Persona GPT4.1), le plus fort que le
                            # budget permet ; voir c7-fort-preenregistrement.md section
                            # taille pour l'estimation ex ante du cout.


# --------------------------------------------------------------------------------------
# Traces
# --------------------------------------------------------------------------------------

def nom_trace():
    return os.path.join(TRACES, f"c7-fort-{MODELE_CLE}-item.jsonl")


def dejafaites(chemin):
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
# Lancement (identique dans l'esprit a c7_recette.lancer_item, modele different)
# --------------------------------------------------------------------------------------

def lancer_item(personnes, items, workers, budget):
    cle = G.cle_api()
    chemin = nom_trace()
    faites = dejafaites(chemin)
    taches = []
    for p in personnes:
        for it in items:
            if (p["vrai_idx"], it["code_index"]) not in faites:
                taches.append((p, it))
    print(f"item/{MODELE_CLE} : {len(faites)} appels deja faits, {len(taches)} restants "
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
    print(f"item/{MODELE_CLE} termine, cumul = {budget.cumul:.4f} USD "
          f"(arrete={budget.arrete()})", flush=True)


# --------------------------------------------------------------------------------------
# Calibrage : 5 appels reels, pour mesurer le cout et confirmer/ajuster N
# --------------------------------------------------------------------------------------

def calibrage(personnes, items, budget):
    cle = G.cle_api()
    p0 = personnes[0]
    couts = []
    for it in items[:5]:
        messages = construire_prompt_item(p0["r1_texte"], it)
        rep = G.appel_chat(cle, MODELE, messages, 0.0, max_tokens=20)
        budget.ajouter(rep.get("cout", 0.0))
        couts.append(rep.get("cout", 0.0))
        print(f"calibrage item : cout={rep.get('cout')}, texte={rep.get('texte')!r}, "
              f"erreur={rep.get('erreur')}", flush=True)
    c = float(np.mean(couts)) if couts else float("nan")
    print(f"\ncout moyen mesure : {c:.6f} USD/appel (n=5)", flush=True)
    for n in (40, 30, 25, 20):
        total = n * len(items) * c
        print(f"  n={n:3d} -> cout estime total = {total:.4f} USD", flush=True)
    print(f"\ncumul apres calibrage = {budget.cumul:.4f} USD", flush=True)


def test3(personnes, items, budget):
    """3 personnes x 60 items = 180 appels, pour verifier le parse et le cout reel
    avant le lancement complet, comme l'exige la conception (etape 2)."""
    lancer_item(personnes[:3], items, WORKERS_MAX, budget)
    chemin = nom_trace()
    lignes = [json.loads(l) for l in open(chemin, encoding="utf-8")
              if l.strip() and json.loads(l)["vrai_idx"] in
              {p["vrai_idx"] for p in personnes[:3]}]
    n_parse = sum(1 for l in lignes if l.get("code") is not None)
    print(f"\ntest3 : {len(lignes)} lignes, taux de parse = {n_parse/len(lignes):.3f}, "
          f"cumul = {budget.cumul:.4f} USD", flush=True)


# --------------------------------------------------------------------------------------
# Analyse : exactitude, fidelite (chute sous permutation intra-segment), fuite
# --------------------------------------------------------------------------------------

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


def analyse(n_declare):
    paq = T1.charger()
    items = G.charger_items()
    idx_mod = construire_idx_mod(paq, items)
    idx_codes = [it["code_index"] for it in items]
    pool_v4 = paq["codes"][REF_V4][:, idx_codes]

    chemin = nom_trace()
    if not os.path.exists(chemin):
        sys.exit(f"pas de trace : {chemin}")
    vec, vrai_idx = _vec_depuis_item(chemin, items, idx_mod)
    couverts = np.flatnonzero((vec >= 0).any(axis=1))
    if len(couverts) == 0:
        sys.exit("aucune attaque exploitable")
    vec_c, vrai_c = vec[couverts], vrai_idx[couverts]
    n = len(couverts)

    # 1. exactitude
    exa = exactitude_propre(vec_c, pool_v4, vrai_c)
    m_exa, b_exa, h_exa = bootstrap_personnes(exa, 2000, [GRAINE, 1])
    taux_parse = float((vec_c >= 0).mean())

    # 2. fuite (top-1, top-10)
    rng = np.random.default_rng([GRAINE, 2])
    rang, top1, top10 = rangs_attaque(vec_c, pool_v4, vrai_c, rng)
    m_t1, b_t1, h_t1 = bootstrap_personnes(top1, 2000, [GRAINE, 3])
    m_t10, b_t10, h_t10 = bootstrap_personnes(top10, 2000, [GRAINE, 4])

    # 3. fidelite : chute sous permutation intra-segment S_gra, normalisee au plancher
    #    humain recalcule sur EXACTEMENT les memes personnes/items/segmentation.
    y_ref_60 = paq["codes"][T1.REF][:, idx_codes]
    y1 = y_ref_60[vrai_c]
    s = paq["seg"]["S_gra"][vrai_c]
    rng_f = np.random.default_rng([GRAINE, 5])
    vraie, perms = chute(vec_c, y1, s, 200, rng_f)
    chute_rel = (vraie - perms.mean()) / vraie if vraie else np.nan

    cd_plancher = paq["codes"][T1.PLANCHER][:, idx_codes][vrai_c]
    rng_p = np.random.default_rng([GRAINE, 6])
    vraie_p, perms_p = chute(cd_plancher, y1, s, 200, rng_p)
    chute_rel_p = (vraie_p - perms_p.mean()) / vraie_p if vraie_p else np.nan
    fidelite_plancher = (chute_rel / chute_rel_p
                         if chute_rel_p and abs(chute_rel_p) > 1e-12 else np.nan)

    print(f"n_attaques={n} (declare n={n_declare}), taux_parse={taux_parse:.3f}",
          flush=True)
    print(f"exactitude = {m_exa:.4f} [{b_exa:.4f} ; {h_exa:.4f}]", flush=True)
    print(f"fidelite (chute relative) = {chute_rel:.4f}, plancher humain = "
          f"{chute_rel_p:.4f}, part du plancher = {fidelite_plancher:.4f}", flush=True)
    print(f"top1 = {m_t1:.4f} [{b_t1:.4f} ; {h_t1:.4f}]  top10 = {m_t10:.4f} "
          f"[{b_t10:.4f} ; {h_t10:.4f}]  rang_median = {np.median(rang):.1f} / "
          f"{pool_v4.shape[0]}", flush=True)

    df = pd.DataFrame([{
        "configuration": f"C7-fort ({MODELE}, item)", "n_attaques": n,
        "n_declare": n_declare, "n_pool": pool_v4.shape[0], "taux_parse_moyen": taux_parse,
        "exactitude": m_exa, "exactitude_bas": b_exa, "exactitude_haut": h_exa,
        "fidelite_chute_relative": chute_rel,
        "fidelite_chute_relative_plancher_humain": chute_rel_p,
        "fidelite_plancher": fidelite_plancher,
        "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
        "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
        "rang_median": float(np.median(rang)), "top1_hasard": 1.0 / pool_v4.shape[0]}])
    chemin_csv = os.path.join(SORTIE, "c7-fort-reidentification.csv")
    df.to_csv(chemin_csv, index=False)
    print(f"\necrit : {chemin_csv}", flush=True)


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--etape", required=True,
                    choices=["calibrage", "test3", "lancer", "analyse", "cout"])
    ap.add_argument("--n", type=int, default=N_CIBLE)
    ap.add_argument("--workers", type=int, default=WORKERS_MAX)
    args = ap.parse_args()
    workers = min(args.workers, WORKERS_MAX)

    if args.etape == "cout":
        print(json.dumps({"cumul_usd": G.Budget(chemin=COUT_FICHIER,
                                                 plafond=PLAFOND_USD).cumul}, indent=1))
        return

    budget = G.Budget(chemin=COUT_FICHIER, plafond=PLAFOND_USD)
    if os.path.exists(STOP_FICHIER):
        sys.exit(f"STOP present : {STOP_FICHIER}")

    if args.etape == "calibrage":
        personnes = G.charger_personnes()
        items = G.charger_items()
        calibrage(personnes, items, budget)
        return

    if args.etape == "test3":
        personnes = G.charger_personnes()
        items = G.charger_items()
        test3(personnes, items, budget)
        return

    if args.etape == "lancer":
        if args.n < N_MIN:
            sys.exit(f"--n doit etre >= {N_MIN} (minimum preenregistre)")
        personnes = G.charger_personnes()[:args.n]
        items = G.charger_items()
        lancer_item(personnes, items, workers, budget)
        return

    if args.etape == "analyse":
        analyse(args.n)


if __name__ == "__main__":
    main()
