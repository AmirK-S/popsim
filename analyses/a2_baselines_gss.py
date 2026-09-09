"""
a2_baselines_gss : les trois baselines sans modele de langage sur le GSS de l'archive OSF.

Statut : script d'exploration, pas du code de production. Il repond a une seule question,
celle du test existentiel du projet : quel score faut il depasser pour qu'un modele de
langage serve a quelque chose au niveau individuel.

Entree  : paquet de replication OSF t6g7k, non versionne.
          figure2/data/new_analysis_summaries/gss_filtered/preparation/p_wave1_summary.csv
          et p_wave2_summary.csv, 1 052 participants et 177 items, reponses en clair.
          figure3/data/demographic_summary.csv, 11 attributs demographiques.
Sortie  : resultats/a2_gss_resultats.json, imprime aussi un tableau lisible sur la sortie
          standard. La figure de la courbe de croisement est tracee par a2_figures.py.

Aucun appel de modele. Duree : environ trois a cinq minutes sur un portable.

Usage : python3 analyses/a2_baselines_gss.py [--rapide]
        --rapide reduit le nombre de tirages de la courbe de croisement.
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
PREP = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure2/data/"
                            "new_analysis_summaries/gss_filtered/preparation")
DEMOG = os.path.join(RACINE, "data/osf-t6g7k-stanford/figure3/data/demographic_summary.csv")
SORTIE = os.path.join(RACINE, "resultats")

# Liste d'exclusion de Stanford, recopiee de
# figure2/code/source/new_analysis/analyze_gss_filtered.py. Ce sont les items du GSS qui
# reprennent une information deja fournie a l'agent, donc hors evaluation. Les
# asterisques font partie des noms de colonnes, ce ne sont pas des jokers.
EXCLUS_STANFORD = {q.lower() for q in [
    "BORN", "DEGREE*", "DWELOWN", "EDUC*", "FAMDIF16", "HISPANIC", "MADEG*", "MAEDUC*",
    "MARITAL", "MARTYPE*", "MAWRKGRW", "PADEG*", "PAEDUC*", "PARTYID", "RACE*", "REG16",
    "RELIG*", "RELPERSN", "RVISITOR", "SEX*", "SPEDUC*", "SPRTPRSN", "SPWRKSTA",
    "VETYEARS", "VISITORS", "WIDOWED", "ZODIAC"]}

# Item verifie identique a un attribut demographique : polviews reproduit exactement
# political_ideology sur les 1 052 participants. Le laisser dans la cible donnerait a B1
# un item gratuit. Il est retire de la cible principale et le cout de ce retrait est
# rapporte separement.
FUITE_DEMOGRAPHIQUE = ["polviews"]

# Familles thematiques du GSS, definies par lecture du libelle des 150 items retenus.
# Elles servent au regime des questions jamais posees : on retire la famille entiere du
# corpus, cible et contexte, et on regarde ce qu'il reste comme plancher.
FAMILLES = {
    "depenses publiques (nat*)": ["natspac/y", "natenvir/y", "natheal/y", "natcity/y",
                                  "natdrug/y", "nateduc/y", "natrace/y", "natarms/y",
                                  "nataid/y", "natfare/y", "natroad", "natsoc", "natmass",
                                  "natpark", "natchld", "natsci", "natenrgy"],
    "confiance dans les institutions (con*)": ["conarmy", "conbus", "conclerg", "coneduc",
                                               "confed", "confinan", "conjudge", "conlabor",
                                               "conlegis", "conmedic", "conpress", "consci",
                                               "contv"],
    "avortement (ab*)": ["abdefect", "abnomore", "abhlth", "abpoor", "abrape", "absingle",
                         "abany"],
    "libertes civiles (spk/col/lib)": ["spkath/y", "colath", "spkrac/y", "colrac",
                                       "librac/y", "spkcom/y", "colcom/y", "libcom/y",
                                       "spkhomo/y", "colhomo", "libhomo/y"],
    "fin de vie (suicide/letdie)": ["letdie1", "suicide1", "suicide2", "suicide3", "suicide4"],
    "roles de genre (fe*)": ["fehire", "fechld", "fepresch", "fefam", "fepol"],
}

N_PLIS = 5           # plis sur les personnes
N_BLOCS = 5          # blocs d'items : chaque item est secret exactement une fois
K_VOISINS = 30       # nombre de voisins de B2, choisi par balayage (voir rapport)
GRAINE = 20260903


# ---------------------------------------------------------------------------
# Chargement
# ---------------------------------------------------------------------------

def charger():
    """Charge les deux vagues humaines et les demographies, alignees sur le meme index.

    Retourne : identifiants, liste des items cibles, matrice vague 1, matrice vague 2,
    tableau des demographies.
    """
    w1 = pd.read_csv(os.path.join(PREP, "p_wave1_summary.csv"))
    w2 = pd.read_csv(os.path.join(PREP, "p_wave2_summary.csv"))
    dem = pd.read_csv(DEMOG)
    assert list(w1["email"]) == list(w2["email"]), "les deux vagues ne sont pas alignees"
    dem = dem.set_index("email").loc[w1["email"]].reset_index()

    items = [c for c in w1.columns if c != "email" and c.lower() not in EXCLUS_STANFORD]
    items = [c for c in items if c not in FUITE_DEMOGRAPHIQUE]

    # Les demographies incompletes sont conservees avec une modalite explicite plutot
    # que supprimees : perdre 17 pour cent des participants pour trois colonnes serait
    # une perte d'information plus grave que la modalite "non renseigne".
    attributs = [c for c in dem.columns if c != "email"]
    x = dem[attributs].fillna("non renseigne").astype(str).values

    return list(w1["email"]), items, w1[items].values.astype(object), \
        w2[items].values.astype(object), x, attributs


# ---------------------------------------------------------------------------
# Protocole d'evaluation
# ---------------------------------------------------------------------------

def grille(n_personnes, n_items, graine=GRAINE):
    """Construit le decoupage croise personnes x items.

    Deux decoupages simultanes et independants :
      - les personnes sont reparties en N_PLIS plis ; a chaque tour un pli est en test
        et les autres servent a entrainer. Aucune reponse d'une personne test n'entre
        dans l'estimation d'un parametre.
      - les items sont repartis en N_BLOCS blocs ; a chaque tour un bloc est secret et
        les autres forment le contexte disponible sur la personne test.
    Chaque couple (personne, item) est donc predit exactement une fois, ce qui permet de
    remplir une matrice de predictions de meme forme que la verite et d'y appliquer
    ensuite la mesure de diversite de a0.
    """
    kf = KFold(n_splits=N_PLIS, shuffle=True, random_state=graine)
    plis = [(tr, te) for tr, te in kf.split(np.arange(n_personnes))]
    rng = np.random.default_rng(graine)
    ordre = rng.permutation(n_items)
    blocs = np.array_split(ordre, N_BLOCS)
    return plis, blocs


# Attributs politiques declares. Verification faite : l'agent demographique de
# l'archive n'obtient que 19,96 pour cent sur polviews, en dessous meme de la modalite
# majoritaire a 28,80 pour cent, alors que cet item est identique a political_ideology.
# Deduction, et c'est une deduction : sa persona ne contenait pas l'orientation politique.
# On mesure donc aussi une variante de B1 privee de ces deux attributs, pour que la
# comparaison avec cet agent porte sur un conditionnement comparable.
ATTRIBUTS_POLITIQUES = ["political_ideology", "political_party"]


def b1_variante_sans_politique(items, y, x, attributs, plis, graine=GRAINE):
    """B1 entrainee sur les seules demographies de recensement, hors politique."""
    garde = [i for i, a in enumerate(attributs) if a not in ATTRIBUTS_POLITIQUES]
    xs = x[:, garde]
    n, m = y.shape
    pred = np.empty((n, m), dtype=object)
    rng = np.random.default_rng(graine)
    for tr, te in plis:
        enc = encodeur_demographies(xs[tr])
        xt, xe = enc.transform(xs[tr]), enc.transform(xs[te])
        for j in range(m):
            pred[np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
    return pred


def evaluer(items, y, x, plis, blocs, k=K_VOISINS, graine=GRAINE):
    """Remplit une matrice de predictions par baseline sur toute la grille.

    Retourne un dictionnaire nom de baseline -> matrice (personnes x items).
    """
    n, m = y.shape
    noms = ["B0 mode", "B0 tirage", "B1 argmax", "B1 tirage", "B2 argmax", "B2 tirage"]
    pred = {nom: np.empty((n, m), dtype=object) for nom in noms}
    rng = np.random.default_rng(graine)
    codes = en_codes(y)

    for i_pli, (tr, te) in enumerate(plis):
        # B0 et B1 n'utilisent aucun item de contexte : leur prediction ne depend pas du
        # bloc secret, on les calcule donc une fois par pli, pour les 150 items.
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        for j in range(m):
            pred["B0 mode"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng, mode=True)[:, None]
            pred["B0 tirage"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng)[:, None]
            pred["B1 argmax"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
            pred["B1 tirage"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng, tirage=True)[:, None]

        # B2 depend du bloc secret, puisque le contexte est l'ensemble des autres blocs.
        for bloc in blocs:
            contexte = np.setdiff1d(np.arange(m), bloc)
            d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
            for j in bloc:
                pred["B2 argmax"][np.ix_(te, [j])] = b2_voisins(d, y[tr, j], k, rng)[:, None]
                pred["B2 tirage"][np.ix_(te, [j])] = b2_voisins(d, y[tr, j], k, rng, tirage=True)[:, None]
        print(f"  pli {i_pli + 1}/{len(plis)} termine", flush=True)
    return pred


def resumer(pred, y_verite, y_reference):
    """Exactitude, intervalle de confiance et diversite, pour chaque baseline."""
    lignes = []
    for nom, p in pred.items():
        acc = exactitude_par_personne(p, y_verite)
        moy, bas, haut = bootstrap_personnes(acc)
        div = profil_diversite(p, y_reference)
        lignes.append({
            "baseline": nom, "exactitude": moy, "ic_bas": bas, "ic_haut": haut,
            "part_diversite_humaine": div["part_diversite_humaine"],
            "accord_par_paires": div["accord_par_paires"],
        })
    return lignes


# ---------------------------------------------------------------------------
# Courbe de croisement
# ---------------------------------------------------------------------------

def courbe(items, y, x, tailles, n_tirages, k=K_VOISINS, graine=GRAINE):
    """Performance de B1 et B2 en fonction du nombre de personnes servant a entrainer.

    Le pli de test est fixe et ne change jamais de taille : seul le corpus
    d'entrainement varie. Sans cela, une courbe montante confondrait l'effet de la
    taille d'entrainement avec la variance d'un test qui retrecit.
    """
    n, m = y.shape
    plis, blocs = grille(n, m, graine)
    rng = np.random.default_rng(graine + 1)
    codes = en_codes(y)
    points = []
    for taille in tailles:
        acc_b1, acc_b2, acc_b0 = [], [], []
        for tirage in range(n_tirages):
            tr_complet, te = plis[tirage % len(plis)]
            if taille > len(tr_complet):
                continue
            tr = rng.choice(tr_complet, size=taille, replace=False)
            enc = encodeur_demographies(x[tr])
            xt, xe = enc.transform(x[tr]), enc.transform(x[te])
            p1 = np.empty((len(te), m), dtype=object)
            p2 = np.empty((len(te), m), dtype=object)
            p0 = np.empty((len(te), m), dtype=object)
            for j in range(m):
                p1[:, j] = b1_logistique(xt, y[tr, j], xe, rng)
                p0[:, j] = b0_marginale(y[tr, j], len(te), rng, mode=True)
            for bloc in blocs:
                contexte = np.setdiff1d(np.arange(m), bloc)
                d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
                for j in bloc:
                    p2[:, j] = b2_voisins(d, y[tr, j], k, rng)
            v = y[te]
            acc_b0.append(np.nanmean(exactitude_par_personne(p0, v)))
            acc_b1.append(np.nanmean(exactitude_par_personne(p1, v)))
            acc_b2.append(np.nanmean(exactitude_par_personne(p2, v)))
        if acc_b1:
            points.append({
                "n_entrainement": int(taille),
                "B0 mode": float(np.mean(acc_b0)), "B0 mode ecart": float(np.std(acc_b0)),
                "B1 argmax": float(np.mean(acc_b1)), "B1 argmax ecart": float(np.std(acc_b1)),
                "B2 argmax": float(np.mean(acc_b2)), "B2 argmax ecart": float(np.std(acc_b2)),
            })
            print(f"  n={taille:>4} B0={points[-1]['B0 mode']:.4f} "
                  f"B1={points[-1]['B1 argmax']:.4f} B2={points[-1]['B2 argmax']:.4f}", flush=True)
    return points


# ---------------------------------------------------------------------------
# Regime des questions jamais posees
# ---------------------------------------------------------------------------

def jamais_posees(items, y):
    """Plancher sur une famille entierement retiree du corpus.

    Une question jamais posee n'a ni cible d'entrainement ni voisin informatif : B1 et
    B2 ne sont pas definies, elles n'ont aucune ligne pour apprendre. Deux planchers
    subsistent, et il faut les distinguer :
      - le tirage uniforme sur les modalites declarees, seul plancher legitime si on ne
        sait rien de la question ;
      - la modalite majoritaire, qui suppose de connaitre la marginale par une autre
        enquete. C'est l'adversaire reel d'un modele de langage sur ce terrain, car un
        modele a lui aussi lu ces marginales quelque part.
    """
    index = {it: j for j, it in enumerate(items)}
    lignes = []
    for nom, membres in FAMILLES.items():
        cols = [index[i] for i in membres if i in index]
        if not cols:
            continue
        sous = y[:, cols]
        acc_mode, acc_unif, n_mod = [], [], []
        for j in range(sous.shape[1]):
            v = [x for x in sous[:, j] if not est_manquant(x)]
            cpt = Counter(v)
            acc_mode.append(cpt.most_common(1)[0][1] / len(v))
            acc_unif.append(sum((c / len(v)) * (1 / len(cpt)) for c in cpt.values()))
            n_mod.append(len(cpt))
        div = profil_diversite(sous, sous)
        lignes.append({
            "famille": nom, "n_items": len(cols),
            "modalites_moyennes": float(np.mean(n_mod)),
            "plancher_uniforme": float(np.mean(acc_unif)),
            "plafond_modalite_majoritaire": float(np.mean(acc_mode)),
            "accord_par_paires_humain": div["accord_par_paires"],
        })
    return lignes


# ---------------------------------------------------------------------------
# Points de reference : les agents de langage de l'archive, sur exactement les memes items
# ---------------------------------------------------------------------------

CONDITIONS_LLM = {
    "agents composite": "composite_agents_summary.csv",
    "agents entretien (v3)": "gss_v3_summary.csv",
    "agents enquete": "survey_agents_summary.csv",
    "agents demographiques (v6)": "gss_v6_summary.csv",
    "agents v7": "gss_v7_summary.csv",
    "agents v8": "gss_v8_summary.csv",
}


def references_llm(items, y1):
    """Recalcule l'exactitude des conditions d'agents sur les memes 149 items que nos baselines.

    Sans cela la comparaison serait faussee : les scores publies portent sur 150 items,
    les notres sur 149 puisque polviews a ete retire pour cause de fuite demographique.
    Un ecart de 0,7 point viendrait alors du denominateur et non de la methode.
    """
    lignes = []
    for libelle, fichier in CONDITIONS_LLM.items():
        chemin = os.path.join(PREP, fichier)
        if not os.path.exists(chemin):
            continue
        d = pd.read_csv(chemin)
        p = d[items].values.astype(object)
        acc = exactitude_par_personne(p, y1)
        moy, bas, haut = bootstrap_personnes(acc)
        div = profil_diversite(p, y1)
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
    if not os.path.isdir(PREP):
        sys.exit(f"Dossier introuvable : {PREP}\n"
                 "Reconstituer : curl -L -o data/replication.rar https://osf.io/download/s2u7c/")

    t0 = time.time()
    ids, items, y1, y2, x, attributs = charger()
    n, m = y1.shape
    print(f"{n} participants, {m} items cibles apres exclusions, "
          f"{len(attributs)} attributs demographiques")
    print(f"attributs : {', '.join(attributs)}\n")

    # Reference humaine : la meme personne reinterrogee deux semaines plus tard. C'est le
    # denominateur de normalisation employe par Stanford, 79,53 pour cent sur les 150 items.
    retest = exactitude_par_personne(y2, y1)
    r_moy, r_bas, r_haut = bootstrap_personnes(retest)
    print(f"consistance test retest humaine : {r_moy:.4f} [{r_bas:.4f} ; {r_haut:.4f}]\n")

    print("baselines sur la grille complete")
    plis, blocs = grille(n, m)
    pred = evaluer(items, y1, x, plis, blocs)
    lignes = resumer(pred, y1, y1)

    print(f"\n{'baseline':<14}{'exactitude':>12}{'IC 95%':>22}"
          f"{'diversite conservee':>22}{'accord paires':>16}")
    for l in lignes:
        print(f"{l['baseline']:<14}{l['exactitude']:>12.4f}"
              f"{'[' + format(l['ic_bas'], '.4f') + ' ; ' + format(l['ic_haut'], '.4f') + ']':>22}"
              f"{l['part_diversite_humaine'] * 100:>21.1f}%{l['accord_par_paires'] * 100:>15.1f}%")

    print("\nvariante : B1 privee des deux attributs politiques")
    pv = b1_variante_sans_politique(items, y1, x, attributs, plis)
    acc_pv = exactitude_par_personne(pv, y1)
    pv_moy, pv_bas, pv_haut = bootstrap_personnes(acc_pv)
    div_pv = profil_diversite(pv, y1)
    print(f"B1 recensement seul  {pv_moy:.4f} [{pv_bas:.4f} ; {pv_haut:.4f}]  "
          f"diversite {div_pv['part_diversite_humaine'] * 100:.1f}%")

    print("\npoints de reference : agents de langage de l'archive, memes items")
    refs = references_llm(items, y1)
    for r in refs:
        print(f"{r['condition']:<28}{r['exactitude']:>10.4f}"
              f"{'[' + format(r['ic_bas'], '.4f') + ' ; ' + format(r['ic_haut'], '.4f') + ']':>22}"
              f"{r['part_diversite_humaine'] * 100:>21.1f}%{r['accord_par_paires'] * 100:>15.1f}%")

    print("\ncourbe de croisement")
    tailles = [50, 100, 150, 200, 300, 400, 600, 841]
    n_tirages = 3 if rapide else 6
    points = courbe(items, y1, x, tailles, n_tirages)

    print("\nregime des questions jamais posees")
    familles = jamais_posees(items, y1)
    print(f"{'famille':<40}{'items':>7}{'uniforme':>11}{'majoritaire':>13}")
    for f in familles:
        print(f"{f['famille']:<40}{f['n_items']:>7}"
              f"{f['plancher_uniforme'] * 100:>10.1f}%{f['plafond_modalite_majoritaire'] * 100:>12.1f}%")

    resultat = {
        "jeu": "OSF t6g7k, GSS filtre",
        "n_participants": int(n), "n_items_cibles": int(m),
        "attributs_demographiques": attributs,
        "items_retires_pour_fuite": FUITE_DEMOGRAPHIQUE,
        "k_voisins": K_VOISINS, "n_plis": N_PLIS, "n_blocs_items": N_BLOCS,
        "test_retest_humain": {"exactitude": r_moy, "ic_bas": r_bas, "ic_haut": r_haut},
        "baselines": lignes,
        "b1_sans_politique": {
            "exactitude": pv_moy, "ic_bas": pv_bas, "ic_haut": pv_haut,
            "part_diversite_humaine": div_pv["part_diversite_humaine"],
            "accord_par_paires": div_pv["accord_par_paires"],
        },
        "references_llm": refs,
        "courbe": points,
        "questions_jamais_posees": familles,
    }
    chemin = os.path.join(SORTIE, "a2_gss_resultats.json")
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(resultat, fh, indent=2, ensure_ascii=False)
    print(f"\necrit : {chemin}  ({time.time() - t0:.0f} s)")


if __name__ == "__main__":
    main()
