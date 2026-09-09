"""
a23_regime_de_validite : ou nos agents locaux battent ils quelque chose, et ou perdent ils ?

Statut : script d'analyse jetable, aucun appel de modele de langage, traces lues en lecture
seule. Aucun script existant n'est modifie ; tout est importe.

Ce que a5_evaluer donne deja : un chiffre global et un chiffre par famille thematique. Ce que
ce script ajoute, et qui manquait pour repondre a la question du regime de validite :

  1. l'exactitude ITEM PAR ITEM pour toutes les methodes, sur les memes 150 personnes et les
     memes 149 items, et le compte des items ou C2 et C3 sont en tete ;
  2. les ecarts APPARIES sur les personnes, avec intervalle bootstrap, globalement et famille
     par famille : un ecart de moyennes non apparie sur les memes 150 personnes est
     conservateur et masque les differences reelles ;
  3. la separation entre les 58 items des six familles thematiques et les 91 autres, qui dit
     si un avantage par famille est un effet de famille ou un effet d'items ;
  4. la concentration de l'argmax par item, cote modele et cote humains : c'est la version
     au niveau de la POPULATION de la quasi degenerescence que a18 mesure au niveau de
     l'APPEL.

Entree  : data/traces/a5-*.jsonl, data/traces/a5-personnes.csv, paquet OSF. Non versionnes.
Sortie  : resultats/a23-par-item.csv, resultats/a23-ecarts-apparies.csv,
          resultats/a23-concentration.csv, plus un tableau lisible sur la sortie standard.
          Aucune microdonnee n'y transite, ce sont des agregats par item ou par methode.

Usage :
  .venv/bin/python analyses/a23_regime_de_validite.py
  .venv/bin/python analyses/a23_regime_de_validite.py --cache /tmp/baselines.pkl
"""

import argparse
import collections
import os
import pickle
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_commun import est_manquant, exactitude_par_personne
from a2_baselines_gss import (CONDITIONS_LLM, FAMILLES, GRAINE, PREP, charger,
                              evaluer as evaluer_baselines, grille)
from a5_evaluer import lire_traces, moyenner_passes, en_matrices
from a5_agents_locaux_gss import TRACES, nomenclature

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

BASELINES = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax"]
ADVERSAIRES = ["B0 mode", "B1 argmax", "B2 argmax", "agents enquete", "agents composite",
               "agents entretien (v3)", "agents demographiques (v6)", "agents v7",
               "agents v8"]


def egal(a, b):
    return str(a).lower().strip() == str(b).lower().strip()


def masque_de(pred, verite):
    return np.array([[(p is not None) and (not est_manquant(v))
                      for p, v in zip(lp, lv)] for lp, lv in zip(pred, verite)])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="",
                    help="pickle des predictions de baselines, pour eviter de les recalculer")
    ap.add_argument("--bootstrap", type=int, default=2000)
    ap.add_argument("--graine", type=int, default=20260908)
    args = ap.parse_args()

    table = nomenclature()
    ids, items, y1, y2, x, _ = charger()
    index_personne = {p: i for i, p in enumerate(ids)}
    index_item = {c: j for j, c in enumerate(items)}

    tables, fichiers = lire_traces("")
    ech = pd.read_csv(os.path.join(TRACES, "a5-personnes.csv"))
    vus = set()
    for t in tables.values():
        vus |= {k[0] for k in t}
    personnes = [p for p in ech["pid"] if p in vus]
    lignes = [index_personne[p] for p in personnes]
    vus_items = set()
    for t in tables.values():
        vus_items |= {k[1] for k in t}
    items_ev = [c for c in items if c in vus_items]
    colonnes = [index_item[c] for c in items_ev]
    print(f"{len(personnes)} personnes, {len(items_ev)} items", flush=True)

    verite = y1[np.ix_(lignes, colonnes)]
    verite2 = y2[np.ix_(lignes, colonnes)]

    # --- matrices de predictions, une par methode -----------------------------------
    M = {}
    for condition in ["C2", "C3", "C3F"]:
        fusion, _ = moyenner_passes(tables, condition)
        if not fusion:
            continue
        M[condition], _ = en_matrices(fusion, personnes, items_ev, table)
    M["humains vague 2"] = verite2
    for libelle, fichier in CONDITIONS_LLM.items():
        chemin = os.path.join(PREP, fichier)
        if not os.path.exists(chemin):
            continue
        d = pd.read_csv(chemin)
        assert list(d["email"]) == ids, f"{fichier} n'est pas aligne sur charger()"
        M[libelle] = d[items_ev].values.astype(object)[lignes]

    if args.cache and os.path.exists(args.cache):
        pred_b = pickle.load(open(args.cache, "rb"))
    else:
        plis, blocs = grille(len(ids), len(items), GRAINE)
        pred_b = evaluer_baselines(items, y1, x, plis, blocs)
        if args.cache:
            pickle.dump(pred_b, open(args.cache, "wb"))
    for nom in BASELINES:
        M[nom] = pred_b[nom][np.ix_(lignes, colonnes)]

    # =================================================================================
    # 1. Exactitude par item
    # =================================================================================
    lignes_item = []
    for j, it in enumerate(items_ev):
        v = verite[:, j]
        ligne = {"item": it, "n": int(sum(not est_manquant(z) for z in v))}
        for nom, mat in M.items():
            p = mat[:, j]
            paires = [(a, b) for a, b in zip(p, v) if a is not None and not est_manquant(b)]
            ligne[nom] = float(np.mean([egal(a, b) for a, b in paires])) if paires else np.nan
        lignes_item.append(ligne)
    par_item = pd.DataFrame(lignes_item)
    famille_de = {i: nf for nf, membres in FAMILLES.items() for i in membres}
    par_item["famille"] = par_item["item"].map(lambda i: famille_de.get(i, "hors famille"))
    os.makedirs(SORTIE, exist_ok=True)
    par_item.to_csv(os.path.join(SORTIE, "a23-par-item.csv"), index=False,
                    float_format="%.6f")

    adversaires = [a for a in ADVERSAIRES if a in par_item.columns]
    print("\n" + "=" * 90)
    print("1. EXACTITUDE PAR ITEM : ou nos agents sont ils devant ?")
    print("=" * 90)
    for cible in ["C2", "C3"]:
        if cible not in par_item.columns:
            continue
        print(f"\n--- {cible} ---")
        for a in adversaires:
            gagne = int((par_item[cible] > par_item[a]).sum())
            egalite = int((par_item[cible] == par_item[a]).sum())
            print(f"  {cible} devant {a:<28} {gagne:>3} items sur {len(par_item)}"
                  f"  (egalites {egalite:>2}), ecart moyen par item "
                  f"{np.mean(par_item[cible] - par_item[a]):+.4f}")
        strict = par_item.apply(lambda r: all(r[cible] > r[a] for a in adversaires), axis=1)
        print(f"  {cible} strictement en tete des {len(adversaires) + 1} methodes "
              f"non humaines sur {int(strict.sum())} items")
        if strict.sum():
            print(par_item.loc[strict, ["item", "famille", cible, "B2 argmax",
                                        "agents enquete"]].to_string(index=False))

    # =================================================================================
    # 2. Ecarts apparies sur les personnes, avec bootstrap
    # =================================================================================
    rng = np.random.default_rng(args.graine)

    def acc_par_personne(nom, sous=None):
        mat, ver = M[nom], verite
        if sous is not None:
            mat, ver = mat[:, sous], ver[:, sous]
        return np.asarray(exactitude_par_personne(mat, ver, masque_de(mat, ver)), float)

    def ecart(a, b, sous=None):
        d = acc_par_personne(a, sous) - acc_par_personne(b, sous)
        d = d[~np.isnan(d)]
        tirages = d[rng.integers(0, len(d), (args.bootstrap, len(d)))].mean(axis=1)
        return (float(d.mean()), float(np.percentile(tirages, 2.5)),
                float(np.percentile(tirages, 97.5)))

    plafond = float(np.nanmean(acc_par_personne("humains vague 2")))
    print("\n" + "=" * 90)
    print(f"2. ECARTS APPARIES SUR LES PERSONNES, plafond humain {plafond:.4f}")
    print("=" * 90)
    couples = [("C2", "agents v8"), ("C3", "agents enquete"), ("C3", "agents composite"),
               ("C3", "agents entretien (v3)"), ("C3", "B0 mode"), ("C3", "B1 argmax"),
               ("C3", "B2 argmax"), ("C3", "C2"), ("C3", "agents v8"),
               ("C3", "agents demographiques (v6)"), ("C3", "agents v7"),
               ("C2", "agents demographiques (v6)"), ("C2", "B0 mode"),
               ("C2", "B1 argmax"), ("C2", "B2 argmax"), ("C2", "agents v7"),
               ("agents enquete", "B2 argmax"), ("agents composite", "B2 argmax")]
    sorties = []
    print(f"{'A':<22}{'B':<28}{'ecart pts':>10}{'IC 95%':>24}{'pts normalises':>16}")
    for a, b in couples:
        if a not in M or b not in M:
            continue
        m, lo, hi = ecart(a, b)
        sorties.append({"perimetre": "149 items", "A": a, "B": b, "ecart": m,
                        "ic_bas": lo, "ic_haut": hi, "ecart_normalise": m / plafond})
        print(f"{a:<22}{b:<28}{m * 100:>+9.2f} [{lo * 100:>+6.2f} ; {hi * 100:>+6.2f}]"
              f"{m / plafond * 100:>+15.2f}")

    print("\n--- par famille thematique, ecarts apparies ---")
    for nf, membres in FAMILLES.items():
        sous = [items_ev.index(i) for i in membres if i in items_ev]
        if not sous:
            continue
        print(f"\n  {nf} ({len(sous)} items)")
        for a, b in [("C3", "B2 argmax"), ("C3", "B1 argmax"), ("C3", "B0 mode"),
                     ("C3", "agents enquete"), ("C3", "agents composite"), ("C3", "C2")]:
            if a not in M or b not in M:
                continue
            m, lo, hi = ecart(a, b, sous)
            sorties.append({"perimetre": nf, "A": a, "B": b, "ecart": m,
                            "ic_bas": lo, "ic_haut": hi, "ecart_normalise": np.nan})
            marque = "  <- intervalle excluant zero" if (lo > 0 or hi < 0) else ""
            print(f"    {a} moins {b:<26}{m * 100:>+8.2f} "
                  f"[{lo * 100:>+6.2f} ; {hi * 100:>+6.2f}]{marque}")

    # 3. familles reunies contre hors famille
    membres = {i for v in FAMILLES.values() for i in v}
    dedans = [j for j, it in enumerate(items_ev) if it in membres]
    dehors = [j for j, it in enumerate(items_ev) if it not in membres]
    print(f"\n--- 3. les {len(dedans)} items de famille contre les {len(dehors)} autres ---")
    print(f"{'methode':<28}{'58 items de famille':>22}{'91 autres items':>20}")
    for nom in sorted(M, key=lambda n: -float(np.nanmean(acc_par_personne(n, dedans)))):
        a1 = float(np.nanmean(acc_par_personne(nom, dedans)))
        a2 = float(np.nanmean(acc_par_personne(nom, dehors)))
        sorties.append({"perimetre": "familles reunies", "A": nom, "B": "", "ecart": a1,
                        "ic_bas": np.nan, "ic_haut": np.nan, "ecart_normalise": np.nan})
        sorties.append({"perimetre": "hors famille", "A": nom, "B": "", "ecart": a2,
                        "ic_bas": np.nan, "ic_haut": np.nan, "ecart_normalise": np.nan})
        print(f"{nom:<28}{a1:>22.4f}{a2:>20.4f}")
    pd.DataFrame(sorties).to_csv(os.path.join(SORTIE, "a23-ecarts-apparies.csv"),
                                 index=False, float_format="%.6f")

    # =================================================================================
    # 4. Concentration de la population predite, item par item
    # =================================================================================
    print("\n" + "=" * 90)
    print("4. CONCENTRATION DE LA POPULATION PREDITE, item par item")
    print("   part de la modalite la plus predite ; version population de la quasi")
    print("   degenerescence que a18 mesure au niveau de l'appel")
    print("=" * 90)
    lignes_conc = []
    for nom, mat in M.items():
        parts = []
        for j in range(len(items_ev)):
            c = collections.Counter(str(v).lower().strip() for v in mat[:, j]
                                    if v is not None and not est_manquant(v))
            if c:
                parts.append(c.most_common(1)[0][1] / sum(c.values()))
        lignes_conc.append({"methode": nom, "part_mediane": float(np.median(parts)),
                            "items_au_dessus_de_90_pourcent": int(sum(p > 0.9 for p in parts)),
                            "n_items": len(parts)})
    # les humains de la vague 1 sont la reference
    parts = []
    for j in range(len(items_ev)):
        c = collections.Counter(str(v).lower().strip() for v in verite[:, j]
                                if not est_manquant(v))
        parts.append(c.most_common(1)[0][1] / sum(c.values()))
    lignes_conc.append({"methode": "humains vague 1", "part_mediane": float(np.median(parts)),
                        "items_au_dessus_de_90_pourcent": int(sum(p > 0.9 for p in parts)),
                        "n_items": len(parts)})
    conc = pd.DataFrame(lignes_conc).sort_values("part_mediane", ascending=False)
    conc.to_csv(os.path.join(SORTIE, "a23-concentration.csv"), index=False,
                float_format="%.4f")
    print(conc.to_string(index=False))

    print(f"\necrit dans {SORTIE} : a23-par-item.csv, a23-ecarts-apparies.csv, "
          "a23-concentration.csv")


if __name__ == "__main__":
    main()
