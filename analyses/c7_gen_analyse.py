"""
c7_gen_analyse : reidentification et exactitude des jumeaux QUE NOUS avons fabriques.

===========================================================================
PREENREGISTREMENT : resultats/c7-gen-preenregistrement.md, ecrit AVANT tout appel de
generation (analyses/c7_gen.py). Ce script n'appelle AUCUN modele, il lit uniquement
les traces deja ecrites dans data/traces/c7-gen/.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Aucun pid, aucun
`vrai_idx` n'est jamais imprime ni ecrit dans resultats/ : seuls des taux agreges en
sortent, sur `resultats/c7-gen-reidentification.csv` et `c7-gen-contamination.csv`.

CE QUI EST REPRIS TEL QUEL, SANS UNE LIGNE MODIFIEE :
  c7_reidentification.rangs_attaque   l'attaque de reidentification elle-meme
  c7_reidentification.items_communs  la selection des 60 items
  c7_reidentification.REF_V4          le nom de la cible
  a2_commun.distance_hamming, bootstrap_personnes

Usage : .venv/bin/python analyses/c7_gen_analyse.py
===========================================================================
"""

import glob
import json
import os
import sys
import zlib

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                             # noqa: E402
from c7_reidentification import items_communs, rangs_attaque, REF_V4  # noqa: E402
from a2_commun import bootstrap_personnes                           # noqa: E402

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data", "traces", "c7-gen")
SORTIE = os.path.join(RACINE, "resultats")
GRAINE = 20260912
N_BOOTSTRAP = 2000
N_TIRAGES_LIENS = 20

CONDITIONS = [
    ("llama31-8b", "R1", 0.0), ("llama31-8b", "R2", 0.0),
    ("qwen37-flash", "R1", 0.0), ("qwen37-flash", "R2", 0.0),
    ("deepseek-v4", "R1", 0.0), ("deepseek-v4", "R2", 0.0),
    ("qwen37-flash", "R1", 1.0),
]


def nom_trace(modele, recette, temperature):
    t = "t0" if float(temperature) == 0 else f"t{temperature}".replace(".", "p")
    return os.path.join(TRACES, f"c7-gen-{modele}-{recette}-{t}.jsonl")


def charger_items():
    return json.load(open(os.path.join(TRACES, "c7-gen-items.json"), encoding="utf-8"))


def construire_idx_mod(paq, items):
    """idx_mod[j] : valeur canonique (str) -> code entier, IDENTIQUE a celui qui a
    produit codes[REF_V4] (paq['modalites'] est deja cette liste triee)."""
    return {it["code_index"]: {m: k for k, m in enumerate(paq["modalites"][it["code_index"]])}
           for it in items}


def charger_condition(modele, recette, temperature, items, idx_mod, n_items):
    chemin = nom_trace(modele, recette, temperature)
    if not os.path.exists(chemin):
        return None
    lignes = [json.loads(l) for l in open(chemin, encoding="utf-8") if l.strip()]
    n = len(lignes)
    vec = np.full((n, n_items), -1, dtype=np.int16)
    vrai_idx = np.zeros(n, dtype=np.int64)
    taux_parse = np.zeros(n)
    for i, e in enumerate(lignes):
        vrai_idx[i] = e["vrai_idx"]
        taux_parse[i] = e.get("taux_parse", 0.0)
        for k, (j_str, val) in enumerate(e.get("codes", {}).items()):
            j = int(j_str)
            code = idx_mod.get(j, {}).get(str(val), -1)
            pos = next((p for p, it in enumerate(items) if it["code_index"] == j), None)
            if pos is not None:
                vec[i, pos] = code
    return vec, vrai_idx, taux_parse


def exactitude_propre(vec_test, pool, vrai_idx):
    """Part des items ou le jumeau retombe EXACTEMENT sur la vraie reponse de LA
    personne (pas de la reidentification : juste l'exactitude, item par item)."""
    vrai_vec = pool[vrai_idx]
    commun = (vec_test >= 0) & (vrai_vec >= 0)
    egal = (vec_test == vrai_vec) & commun
    n = commun.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, egal.sum(axis=1) / np.maximum(n, 1), np.nan)


def main():
    paq = T1.charger()
    items = charger_items()
    n_items = len(items)
    idx_mod = construire_idx_mod(paq, items)
    idx_codes = [it["code_index"] for it in items]
    pool_v4 = paq["codes"][REF_V4][:, idx_codes]
    n_pool = pool_v4.shape[0]

    lignes = []
    resume_pour_verdict = {}
    for modele, recette, temp in CONDITIONS:
        r = charger_condition(modele, recette, temp, items, idx_mod, n_items)
        if r is None:
            print(f"absent : {modele}/{recette}/t={temp}", flush=True)
            continue
        vec, vrai_idx, taux_parse = r
        graine_cle = zlib.crc32(f"{modele}|{recette}|{temp}".encode("utf-8"))
        rng = np.random.default_rng([GRAINE, graine_cle])
        rang, top1, top10 = rangs_attaque(vec, pool_v4, vrai_idx, rng, N_TIRAGES_LIENS)
        exact = exactitude_propre(vec, pool_v4, vrai_idx)
        m_t1, b_t1, h_t1 = bootstrap_personnes(top1, N_BOOTSTRAP, [GRAINE, 1])
        m_t10, b_t10, h_t10 = bootstrap_personnes(top10, N_BOOTSTRAP, [GRAINE, 2])
        m_ex, b_ex, h_ex = bootstrap_personnes(exact, N_BOOTSTRAP, [GRAINE, 3])
        ligne = {
            "modele": modele, "recette": recette, "temperature": temp,
            "n_attaques": vec.shape[0], "n_pool": n_pool,
            "taux_parse_moyen": float(np.mean(taux_parse)),
            "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
            "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
            "exactitude": m_ex, "exactitude_bas": b_ex, "exactitude_haut": h_ex,
            "rang_median": float(np.median(rang)),
            "top1_hasard": 1.0 / n_pool, "top10_hasard": min(10, n_pool) / n_pool,
        }
        lignes.append(ligne)
        resume_pour_verdict[(modele, recette, temp)] = ligne
        print(f"{modele}/{recette}/t={temp} : n={ligne['n_attaques']} "
              f"parse={ligne['taux_parse_moyen']:.3f} top1={m_t1:.4f} "
              f"[{b_t1:.4f};{h_t1:.4f}] top10={m_t10:.4f} exact={m_ex:.4f}", flush=True)

    df = pd.DataFrame(lignes)
    df.to_csv(os.path.join(SORTIE, "c7-gen-reidentification.csv"), index=False)

    # --- verdict des trois predictions preenregistrees ---
    modeles = ["llama31-8b", "qwen37-flash", "deepseek-v4"]
    r1_top1 = {m: resume_pour_verdict.get((m, "R1", 0.0), {}).get("top1", np.nan) for m in modeles}
    r2_top1 = {m: resume_pour_verdict.get((m, "R2", 0.0), {}).get("top1", np.nan) for m in modeles}
    pred1 = sum(v >= 0.10 for v in r1_top1.values() if not np.isnan(v)) >= 2
    pred2 = all(v < 0.03 for v in r2_top1.values() if not np.isnan(v))
    t0 = resume_pour_verdict.get(("qwen37-flash", "R1", 0.0), {}).get("top1", np.nan)
    t1 = resume_pour_verdict.get(("qwen37-flash", "R1", 1.0), {}).get("top1", np.nan)
    pred3 = bool(t0 and not np.isnan(t1) and t1 <= (2.0 / 3.0) * t0)
    verdict = {"pred1_r1_ge10pct_2sur3": bool(pred1), "r1_top1_par_modele": r1_top1,
              "pred2_r2_sous3pct_partout": bool(pred2), "r2_top1_par_modele": r2_top1,
              "pred3_temp1_reduit_dun_tiers": pred3, "top1_qwen_t0": t0, "top1_qwen_t1": t1}
    print("\nVERDICT :", json.dumps(verdict, indent=1), flush=True)
    with open(os.path.join(SORTIE, "c7-gen-verdict.json"), "w", encoding="utf-8") as fh:
        json.dump(verdict, fh, ensure_ascii=False, indent=1)

    # --- contamination ---
    chemin_ctl = os.path.join(TRACES, "c7-gen-contamination.jsonl")
    if os.path.exists(chemin_ctl):
        c = pd.DataFrame(json.loads(l) for l in open(chemin_ctl, encoding="utf-8") if l.strip())
        agg = c.groupby(["modele", "condition"])["verbatim_20plus"].mean().reset_index()
        agg.to_csv(os.path.join(SORTIE, "c7-gen-contamination.csv"), index=False)
        print("\ncontamination (taux de completion verbatim >=20 caracteres) :")
        print(agg.to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
