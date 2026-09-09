"""
a2_baselines_twin : les trois baselines sans modele de langage sur Twin-2K-500.

Statut : script d'exploration, pas du code de production. Meme protocole et memes
metriques que a2_baselines_gss, applique au jeu qui doit devenir le jeu principal du
projet. Toute divergence de chiffre entre les deux jeux vient donc des donnees et non de
la mesure, les deux scripts partagent a2_commun.

Entree  : depot Hugging Face LLM-Digital-Twin/Twin-2K-500, licence CC BY 4.0, non
          restreint. Fichiers telecharges par a2_telecharger_twin.py dans data/twin2k500 :
            question_catalog_and_human_response_csv/wave1_3_response.csv   2 058 x 761
            question_catalog_and_human_response_csv/wave4_response.csv     2 058 x 127
            question_catalog_and_human_response_csv/question_catalog.json  256 questions
            llm/*.csv  simulations publiees par les auteurs, servant de points de repere
Sortie  : resultats/a2_twin_resultats.json, plus un tableau lisible sur la sortie standard.

Aucun appel de modele. Duree : environ dix minutes sur un portable.

Usage : python3 analyses/a2_baselines_twin.py [--rapide]
"""

import json
import os
import sys
import time
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.model_selection import KFold

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a2_commun import (b0_marginale, b1_logistique, b2_voisins, bootstrap_personnes,
                       distance_hamming, en_codes, encodeur_demographies, est_manquant,
                       exactitude_par_personne, profil_diversite)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(RACINE, "data/twin2k500")
CSV = os.path.join(BASE, "question_catalog_and_human_response_csv")
LLM = os.path.join(BASE, "llm")
SORTIE = os.path.join(RACINE, "resultats")

N_PLIS = 5
K_VOISINS = 30
GRAINE = 20260903

# Familles retenues pour le regime des questions jamais posees. Ce sont les blocs du
# catalogue qui comptent assez d'items dans la vague 4 pour que le chiffre soit stable.
FAMILLES_JAMAIS_POSEES = [
    "Product Preferences - Pricing",
    "False consensus",
    "Non-experimental heuristics and biases",
    "Probability matching vs. maximizing - Problem 1",
]


# ---------------------------------------------------------------------------
# Chargement et description du jeu
# ---------------------------------------------------------------------------

def charger():
    """Prepare la cible, le contexte et les demographies.

    Decoupage, et c'est le point ou l'on triche sans le vouloir :
      - CIBLE : les colonnes de la vague 4 qui sont categorielles, c'est a dire de type
        MC a reponse unique ou Matrix. Les curseurs et les saisies libres sont exclus,
        l'exactitude exacte n'y a pas de sens.
      - CONTEXTE : les colonnes des vagues 1 a 3 qui ne sont PAS reposees en vague 4.
        Les 126 colonnes reposees sont retirees du contexte. Les garder reviendrait a
        donner a B2 la reponse anterieure de la personne a la question meme qu'on lui
        demande de predire, ce qui ne mesurerait plus que la stabilite test retest.
        Cette stabilite est mesuree a part, et sert de plafond.
      - DEMOGRAPHIES : les 14 questions du bloc Demographics des vagues 1 a 3.
    """
    catalogue = json.load(open(os.path.join(CSV, "question_catalog.json"), encoding="utf-8"))
    col_vers_question = {}
    for q in catalogue:
        for c in q.get("csv_columns", []):
            col_vers_question.setdefault(c, q)

    w13 = pd.read_csv(os.path.join(CSV, "wave1_3_response.csv"), low_memory=False)
    w4 = pd.read_csv(os.path.join(CSV, "wave4_response.csv"), low_memory=False)
    assert list(w13["pid"]) == list(w4["pid"]), "les deux fichiers ne sont pas alignes"

    def categorielle(c):
        q = col_vers_question.get(c)
        if q is None:
            return False
        if q["QuestionType"] == "Matrix":
            return True
        return (q["QuestionType"] == "MC"
                and q.get("Settings", {}).get("Selector") in ("SAVR", "SAHR"))

    cibles = [c for c in w4.columns if c != "pid" and categorielle(c)]
    reposees = [c for c in w4.columns if c != "pid" and c in w13.columns]
    contexte = [c for c in w13.columns
                if c != "pid" and c not in reposees and categorielle(c)]

    demo = [c for c in w13.columns
            if col_vers_question.get(c) is not None
            and col_vers_question[c]["BlockName"].strip() == "Demographics"]

    y = w4[cibles].values.astype(object)
    y_retest = w13[cibles].values.astype(object)
    ctx = w13[contexte].values.astype(object)
    x = w13[demo].fillna("non renseigne").astype(str).values
    blocs = {c: col_vers_question[c]["BlockName"].strip() for c in cibles}
    return {
        "pid": list(w13["pid"]), "cibles": cibles, "contexte": contexte, "demo": demo,
        "y": y, "y_retest": y_retest, "ctx": ctx, "x": x, "blocs_cibles": blocs,
        "catalogue": col_vers_question,
    }


# ---------------------------------------------------------------------------
# Protocole
# ---------------------------------------------------------------------------

def plis_personnes(n, graine=GRAINE):
    """Validation croisee a N_PLIS plis, l'unite de decoupage est la personne.

    Aucun decoupage sur les items n'est necessaire ici, contrairement au GSS : la
    separation entre entree et evaluation est temporelle et fournie par les auteurs, le
    contexte vient des vagues 1 a 3 et la cible de la vague 4.
    """
    kf = KFold(n_splits=N_PLIS, shuffle=True, random_state=graine)
    return [(tr, te) for tr, te in kf.split(np.arange(n))]


def evaluer(d, plis, k=K_VOISINS, graine=GRAINE):
    """Remplit une matrice de predictions par baseline, sur toutes les personnes."""
    y, x, ctx = d["y"], d["x"], d["ctx"]
    n, m = y.shape
    noms = ["B0 mode", "B0 tirage", "B1 argmax", "B1 tirage", "B2 argmax", "B2 tirage"]
    pred = {nom: np.empty((n, m), dtype=object) for nom in noms}
    rng = np.random.default_rng(graine)
    codes = en_codes(ctx)

    for i_pli, (tr, te) in enumerate(plis):
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        dist = distance_hamming(codes[te], codes[tr])
        for j in range(m):
            pred["B0 mode"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng, mode=True)[:, None]
            pred["B0 tirage"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng)[:, None]
            pred["B1 argmax"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
            pred["B1 tirage"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng, tirage=True)[:, None]
            pred["B2 argmax"][np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], k, rng)[:, None]
            pred["B2 tirage"][np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], k, rng, tirage=True)[:, None]
        print(f"  pli {i_pli + 1}/{len(plis)} termine", flush=True)
    return pred


def resumer(pred, y):
    """Exactitude, intervalle de confiance et diversite pour chaque baseline."""
    masque = np.array([[not est_manquant(v) for v in ligne] for ligne in y])
    lignes = []
    for nom, p in pred.items():
        # Une cellule non evaluable chez l'humain ne doit pas compter comme une erreur.
        p = np.where(masque, p, None)
        acc = exactitude_par_personne(p, y, masque)
        moy, bas, haut = bootstrap_personnes(acc)
        div = profil_diversite(p, y)
        lignes.append({
            "baseline": nom, "exactitude": moy, "ic_bas": bas, "ic_haut": haut,
            "part_diversite_humaine": div["part_diversite_humaine"],
            "accord_par_paires": div["accord_par_paires"],
        })
    return lignes


def courbe(d, tailles, n_tirages, k=K_VOISINS, graine=GRAINE):
    """Exactitude de B0, B1 et B2 selon le nombre de personnes d'entrainement."""
    y, x, ctx = d["y"], d["x"], d["ctx"]
    n, m = y.shape
    plis = plis_personnes(n, graine)
    codes = en_codes(ctx)
    rng = np.random.default_rng(graine + 1)
    masque = np.array([[not est_manquant(v) for v in ligne] for ligne in y])
    points = []
    for taille in tailles:
        a0, a1, a2 = [], [], []
        for tirage in range(n_tirages):
            tr_complet, te = plis[tirage % len(plis)]
            if taille > len(tr_complet):
                continue
            tr = rng.choice(tr_complet, size=taille, replace=False)
            enc = encodeur_demographies(x[tr])
            xt, xe = enc.transform(x[tr]), enc.transform(x[te])
            dist = distance_hamming(codes[te], codes[tr])
            p0 = np.empty((len(te), m), dtype=object)
            p1 = np.empty((len(te), m), dtype=object)
            p2 = np.empty((len(te), m), dtype=object)
            for j in range(m):
                p0[:, j] = b0_marginale(y[tr, j], len(te), rng, mode=True)
                p1[:, j] = b1_logistique(xt, y[tr, j], xe, rng)
                p2[:, j] = b2_voisins(dist, y[tr, j], k, rng)
            mt, v = masque[te], y[te]
            a0.append(np.nanmean(exactitude_par_personne(np.where(mt, p0, None), v, mt)))
            a1.append(np.nanmean(exactitude_par_personne(np.where(mt, p1, None), v, mt)))
            a2.append(np.nanmean(exactitude_par_personne(np.where(mt, p2, None), v, mt)))
        if a1:
            points.append({
                "n_entrainement": int(taille),
                "B0 mode": float(np.mean(a0)), "B0 mode ecart": float(np.std(a0)),
                "B1 argmax": float(np.mean(a1)), "B1 argmax ecart": float(np.std(a1)),
                "B2 argmax": float(np.mean(a2)), "B2 argmax ecart": float(np.std(a2)),
            })
            print(f"  n={taille:>4} B0={points[-1]['B0 mode']:.4f} "
                  f"B1={points[-1]['B1 argmax']:.4f} B2={points[-1]['B2 argmax']:.4f}", flush=True)
    return points


def jamais_posees(d):
    """Plancher sur les familles entierement retirees du corpus.

    Sur une famille jamais posee a personne, il n'existe aucune ligne d'entrainement :
    ni B1 ni B2 ne sont definies. Restent deux planchers, qu'il faut distinguer, car ils
    ne supposent pas la meme connaissance :
      - tirage uniforme sur les modalites, aucune information ;
      - modalite majoritaire, ce qui suppose de connaitre la marginale par ailleurs.
    """
    y, cibles, blocs = d["y"], d["cibles"], d["blocs_cibles"]
    index = {c: j for j, c in enumerate(cibles)}
    lignes = []
    for famille in FAMILLES_JAMAIS_POSEES:
        cols = [index[c] for c in cibles if blocs[c] == famille]
        if not cols:
            continue
        sous = y[:, cols]
        acc_mode, acc_unif, n_mod = [], [], []
        for j in range(sous.shape[1]):
            v = [x for x in sous[:, j] if not est_manquant(x)]
            if not v:
                continue
            cpt = Counter(v)
            acc_mode.append(cpt.most_common(1)[0][1] / len(v))
            acc_unif.append(sum((c / len(v)) * (1 / len(cpt)) for c in cpt.values()))
            n_mod.append(len(cpt))
        div = profil_diversite(sous, sous)
        lignes.append({
            "famille": famille, "n_items": len(cols),
            "modalites_moyennes": float(np.mean(n_mod)),
            "plancher_uniforme": float(np.mean(acc_unif)),
            "plafond_modalite_majoritaire": float(np.mean(acc_mode)),
            "accord_par_paires_humain": div["accord_par_paires"],
        })
    return lignes


# ---------------------------------------------------------------------------
# Points de reference : les simulations publiees par les auteurs
# ---------------------------------------------------------------------------

SIMULATIONS = {
    "GPT-4.1-mini, persona complet": "default_gpt41mini_llm.csv",
    "GPT-4.1-mini, demographies seules": "demo_only_gpt41mini_llm.csv",
}


def references_llm(d):
    """Exactitude des simulations des auteurs, sur exactement les memes items que nos baselines.

    Les fichiers de simulation portent un identifiant TWIN_ID et non le pid du catalogue.
    L'ordre par TWIN_ID croissant reproduit exactement l'ordre des pid : verifie en
    comparant colonne par colonne le fichier humain formate au catalogue, accord 1,0000
    sur les 108 items retenus. La comparaison est faite a l'interieur des fichiers
    formates, humains contre simules, donc dans un codage interne coherent.
    """
    chemin_mapping = os.path.join(LLM, "wave4_formatted_to_catalog_mapping.json")
    if not os.path.exists(chemin_mapping):
        return []
    mapping = json.load(open(chemin_mapping, encoding="utf-8"))
    cibles = set(d["cibles"])
    paires = [(m["formatted_column"], m["catalog_csv_column"]) for m in mapping
              if m["catalog_csv_column"] in cibles]
    colonnes = [f for f, _ in paires]

    humain = pd.read_csv(os.path.join(LLM, "default_gpt41mini_wave4.csv"), low_memory=False)
    humain = humain.iloc[1:].reset_index(drop=True)          # la premiere ligne est un libelle
    humain["tid"] = pd.to_numeric(humain["TWIN_ID"])
    b = humain[colonnes].apply(pd.to_numeric, errors="coerce").values
    masque = ~np.isnan(b)

    lignes = []
    for libelle, fichier in SIMULATIONS.items():
        chemin = os.path.join(LLM, fichier)
        if not os.path.exists(chemin):
            continue
        sim = pd.read_csv(chemin, low_memory=False).iloc[1:].reset_index(drop=True)
        sim["tid"] = pd.to_numeric(sim["TWIN_ID"])
        sim = sim.set_index("tid").loc[humain["tid"]]
        a = sim[colonnes].apply(pd.to_numeric, errors="coerce").values
        n = masque.sum(axis=1)
        acc = np.where(n > 0, ((a == b) & masque).sum(axis=1) / np.maximum(n, 1), np.nan)
        moy, bas, haut = bootstrap_personnes(acc)
        div = profil_diversite(a.astype(object), b.astype(object))
        lignes.append({
            "condition": libelle, "exactitude": moy, "ic_bas": bas, "ic_haut": haut,
            "part_diversite_humaine": div["part_diversite_humaine"],
            "accord_par_paires": div["accord_par_paires"],
        })
    return lignes


# ---------------------------------------------------------------------------

def main():
    rapide = "--rapide" in sys.argv
    os.makedirs(SORTIE, exist_ok=True)
    if not os.path.isdir(CSV):
        sys.exit(f"Dossier introuvable : {CSV}\n"
                 "Telecharger d'abord : python3 analyses/a2_telecharger_twin.py")

    t0 = time.time()
    d = charger()
    y = d["y"]
    n, m = y.shape
    print(f"{n} participants, {m} items cibles categoriels en vague 4, "
          f"{len(d['contexte'])} items de contexte en vagues 1 a 3, "
          f"{len(d['demo'])} questions demographiques")
    taux = np.mean([[est_manquant(v) for v in l] for l in y])
    print(f"taux de cellules non renseignees dans la cible : {taux:.3f} "
          "(experiences inter sujets, chaque personne ne voit qu'une condition)\n")

    masque = np.array([[not est_manquant(v) for v in l] for l in y])
    retest = exactitude_par_personne(np.where(masque, d["y_retest"], None), y, masque)
    r_moy, r_bas, r_haut = bootstrap_personnes(retest)
    print(f"consistance test retest humaine, vagues 1 a 3 contre vague 4 : "
          f"{r_moy:.4f} [{r_bas:.4f} ; {r_haut:.4f}]\n")

    print("baselines")
    plis = plis_personnes(n)
    pred = evaluer(d, plis)
    lignes = resumer(pred, y)
    print(f"\n{'baseline':<14}{'exactitude':>12}{'IC 95%':>22}"
          f"{'diversite conservee':>22}{'accord paires':>16}")
    for l in lignes:
        print(f"{l['baseline']:<14}{l['exactitude']:>12.4f}"
              f"{'[' + format(l['ic_bas'], '.4f') + ' ; ' + format(l['ic_haut'], '.4f') + ']':>22}"
              f"{l['part_diversite_humaine'] * 100:>21.1f}%{l['accord_par_paires'] * 100:>15.1f}%")

    print("\npoints de reference : simulations publiees par les auteurs, memes items")
    refs = references_llm(d)
    for r in refs:
        print(f"{r['condition']:<36}{r['exactitude']:>10.4f}"
              f"{'[' + format(r['ic_bas'], '.4f') + ' ; ' + format(r['ic_haut'], '.4f') + ']':>22}"
              f"{r['part_diversite_humaine'] * 100:>15.1f}%")

    print("\ncourbe de croisement")
    tailles = [50, 100, 200, 400, 800, 1200, 1646]
    points = courbe(d, tailles, 3 if rapide else 6)

    print("\nregime des questions jamais posees")
    familles = jamais_posees(d)
    print(f"{'famille':<48}{'items':>7}{'uniforme':>11}{'majoritaire':>13}")
    for f in familles:
        print(f"{f['famille']:<48}{f['n_items']:>7}"
              f"{f['plancher_uniforme'] * 100:>10.1f}%{f['plafond_modalite_majoritaire'] * 100:>12.1f}%")

    resultat = {
        "jeu": "Twin-2K-500, LLM-Digital-Twin/Twin-2K-500, CC BY 4.0",
        "n_participants": int(n), "n_items_cibles": int(m),
        "n_items_contexte": len(d["contexte"]),
        "questions_demographiques": d["demo"],
        "k_voisins": K_VOISINS, "n_plis": N_PLIS,
        "taux_cellules_non_renseignees_cible": float(taux),
        "test_retest_humain": {"exactitude": r_moy, "ic_bas": r_bas, "ic_haut": r_haut},
        "baselines": lignes,
        "references_llm": refs,
        "courbe": points,
        "questions_jamais_posees": familles,
    }
    chemin = os.path.join(SORTIE, "a2_twin_resultats.json")
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(resultat, fh, indent=2, ensure_ascii=False)
    print(f"\necrit : {chemin}  ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
