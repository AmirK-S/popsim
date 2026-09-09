"""
a5_evaluer : evaluation des agents locaux du run a5, avec les instruments de a0, a1 et a2.

Statut : script d'evaluation, pas du code de production. Il ne fait aucun appel de modele :
il relit les traces JSONL ecrites par analyses/a5_agents_locaux_gss.py et les compare a la
verite terrain, aux baselines sans modele de langage et aux conditions d'agents de Stanford.

Le point de methode. Tout est restreint aux MEMES personnes et aux MEMES items que le run.
Comparer nos 150 personnes aux 1 052 personnes de a2 melangerait un effet de methode et un
effet d'echantillon. Les baselines B0, B1 et B2 sont donc recalculees ici sur le decoupage
de a2, puis restreintes aux lignes de notre sous echantillon : chaque personne evaluee est
bien en test, et les baselines qui apprennent le font sur les autres personnes du corpus.

Ce qui est calcule, pour chaque condition :
  - exactitude par personne sur les items secrets, argmax de la distribution, avec
    intervalle de confiance a 95 pour cent par bootstrap sur les personnes (a2_commun) ;
  - exactitude normalisee par le plafond humain test retest DE CES personnes, jamais par la
    moyenne des 1 052 : normaliser par une moyenne de population masquerait l'heterogeneite
    des personnes tirees ;
  - diversite conservee et accord par paires (a2_commun.profil_diversite).

Ce que nous pouvons calculer et que les points de reference ne permettent pas, parce que
nous avons la distribution complete et pas seulement un point :
  - exactitude esperee : probabilite moyenne attribuee a la vraie reponse. Un agent qui
    hesite entre deux modalites et tombe juste par argmax n'est pas au meme endroit qu'un
    agent certain et juste ;
  - calibration : fiabilite par decile de confiance, plus l'ecart de calibration attendu ;
  - entropie moyenne de la distribution par appel, en bits, avec l'entropie maximale
    correspondante. C'est la mesure d'ecrasement de la variance au niveau de l'appel, que
    ni Stanford ni les baselines ne peuvent fournir.

Un tableau PAR FAMILLE thematique est produit en plus du chiffre global, pour toutes les
methodes : nos C2, C3 et C3F, B0 mode, B0 tirage, B1 argmax, B2 argmax, les humains de la
vague 2 et les six conditions de Stanford. Motif, tache 2 de a8-baselines-durcies.md : avec
des blocs aleatoires, un item secret garde ses cousins thematiques dans le contexte et B2 en
profite ; quand la famille entiere sort du contexte, les agents composite de Stanford battent
B2. Le chiffre global masque donc l'endroit ou un modele de langage sert a quelque chose. Le
plafond humain est recalcule famille par famille. Sortie : resultats/a5-familles.csv.

Entree  : data/traces/a5-*.jsonl et data/traces/a5-personnes.csv, non versionnes.
Sortie  : resultats/a5_resultats.json, resultats/a5-familles.csv, et un tableau lisible sur
          la sortie standard. Aucune microdonnee n'y transite, ce sont des agregats.

Usage :
  .venv/bin/python analyses/a5_evaluer.py
  .venv/bin/python analyses/a5_evaluer.py --suffixe smoke --sortie resultats/a5_smoke.json
"""

import argparse
import glob
import json
import math
import os
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_commun import (bootstrap_personnes, est_manquant, exactitude_par_personne,
                       profil_diversite)
from a2_baselines_gss import (CONDITIONS_LLM, FAMILLES, GRAINE, PREP, charger,
                              evaluer as evaluer_baselines, grille)
from a5_agents_locaux_gss import TRACES, canoniser, nomenclature

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

# Deciles de confiance pour la table de calibration. Un agent bien calibre qui dit 0,7 a
# raison sept fois sur dix ; l'ecart moyen entre ces deux colonnes est l'ECE.
BORNES_DECILES = np.linspace(0.0, 1.0, 11)


# --------------------------------------------------------------------------------------
# 1. Lecture des traces
# --------------------------------------------------------------------------------------

def lire_traces(suffixe=""):
    """Charge toutes les traces a5 disponibles, indexees par (condition, passe).

    Les doublons sont ecrases par la derniere occurrence : une relance apres arret brutal
    peut reecrire la ligne coupee en deux. La cle est (pid, item), celle de l'index unique
    du run.
    """
    motif = f"a5-C*-p*{'-' + suffixe if suffixe else ''}.jsonl"
    fichiers = sorted(glob.glob(os.path.join(TRACES, motif)))
    if suffixe == "":
        # Sans suffixe, ne pas ramasser les traces de smoke test ni de mesure de debit.
        fichiers = [f for f in fichiers
                    if os.path.basename(f).count("-") == 2]
    tables = defaultdict(dict)
    for chemin in fichiers:
        with open(chemin, encoding="utf-8") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    d = json.loads(ligne)
                except json.JSONDecodeError:
                    continue
                tables[(d["condition"], d["passe"])][(d["pid"], d["item"])] = d
    return tables, fichiers


def moyenner_passes(tables, condition):
    """Moyenne les distributions des deux passes d'une meme condition, cellule a cellule.

    Les deux passes presentent les modalites dans deux ordres opposes ; la lettre n'a donc
    pas le meme sens de l'une a l'autre. La trace enregistre la distribution SUR LES
    MODALITES et non sur les lettres, ce qui remet les deux passes dans le meme repere
    avant de les moyenner. C'est tout l'interet de ne pas stocker des lettres.

    Renvoie un dictionnaire (pid, item) -> {"distribution": ..., "duree_ms", "masse", ...}
    et la liste des passes effectivement presentes.
    """
    passes = sorted(p for (c, p) in tables if c == condition)
    if not passes:
        return {}, []
    fusion = {}
    cles = set()
    for p in passes:
        cles |= set(tables[(condition, p)].keys())
    for cle in cles:
        dists, masses, durees, rejets = [], [], [], []
        for p in passes:
            d = tables[(condition, p)].get(cle)
            if d is None:
                continue
            dists.append(d["distribution"])
            masses.append(d["masse_lettres"])
            durees.append(d["duree_ms"])
            rejets.append(bool(d["rejet"]))
        if not dists:
            continue
        modalites = list(dists[0].keys())
        moyenne = {m: float(np.mean([d.get(m, 0.0) for d in dists])) for m in modalites}
        s = sum(moyenne.values())
        if s > 0:
            moyenne = {m: v / s for m, v in moyenne.items()}
        fusion[cle] = {
            "distribution": moyenne,
            "argmax": max(moyenne, key=moyenne.get),
            "masse_lettres": float(np.mean(masses)),
            "duree_ms": float(np.sum(durees)),
            "rejet": any(rejets),
            "n_passes": len(dists),
        }
    return fusion, passes


# --------------------------------------------------------------------------------------
# 2. Mise en matrice, au format attendu par a2_commun
# --------------------------------------------------------------------------------------

def en_matrices(fusion, personnes, items, table):
    """Construit la matrice de predictions argmax et la matrice des distributions.

    Les modalites de la trace sont ecrites dans la casse officielle de main.csv, la verite
    terrain est en minuscules dans les fichiers de reponses. Tout est ramene ici a la
    casse des fichiers de reponses, pour que l'egalite de chaine de a2_commun soit valide.
    """
    pred = np.empty((len(personnes), len(items)), dtype=object)
    dist = np.empty((len(personnes), len(items)), dtype=object)
    for i, p in enumerate(personnes):
        for j, it in enumerate(items):
            d = fusion.get((p, it))
            if d is None:
                pred[i, j] = None
                dist[i, j] = None
            else:
                pred[i, j] = d["argmax"].lower().strip()
                dist[i, j] = {k.lower().strip(): v for k, v in d["distribution"].items()}
    return pred, dist


def mesures_distributionnelles(dist, verite):
    """Exactitude esperee, entropie moyenne et table de calibration.

    exactitude esperee : moyenne sur les cellules de la probabilite attribuee a la vraie
    modalite. Elle est bornee par l'exactitude argmax et lui est presque toujours
    inferieure ; l'ecart entre les deux mesure a quel point l'agent hesite.

    entropie : en bits, avec l'entropie maximale de la question, log2(K). Le rapport des
    deux dit combien de la dispersion possible l'agent conserve, appel par appel. C'est la
    version au niveau de l'appel de l'ecrasement de variance que a0 mesure au niveau de la
    population.

    calibration : pour chaque decile de la probabilite maximale, la frequence reelle de
    bonne reponse. L'ecart de calibration attendu (ECE) est la moyenne ponderee des ecarts
    absolus entre confiance moyenne et exactitude reelle.
    """
    conf, juste, ent, ent_max, esperee = [], [], [], [], []
    for i in range(dist.shape[0]):
        for j in range(dist.shape[1]):
            d = dist[i, j]
            v = verite[i, j]
            if d is None or est_manquant(v):
                continue
            p_vraie = d.get(str(v).lower().strip(), 0.0)
            esperee.append(p_vraie)
            pm = max(d.values())
            conf.append(pm)
            juste.append(1.0 if max(d, key=d.get) == str(v).lower().strip() else 0.0)
            ent.append(-sum(q * math.log2(q) for q in d.values() if q > 0))
            ent_max.append(math.log2(len(d)) if len(d) > 1 else 0.0)
    if not conf:
        return {}
    conf, juste = np.array(conf), np.array(juste)
    deciles = []
    ece = 0.0
    for b in range(10):
        bas, haut = BORNES_DECILES[b], BORNES_DECILES[b + 1]
        sel = (conf > bas) & (conf <= haut) if b > 0 else (conf >= bas) & (conf <= haut)
        n = int(sel.sum())
        if n == 0:
            continue
        c, a = float(conf[sel].mean()), float(juste[sel].mean())
        deciles.append({"decile": f"{bas:.1f}-{haut:.1f}", "n": n,
                        "confiance_moyenne": c, "exactitude_reelle": a, "ecart": a - c})
        ece += n / len(conf) * abs(a - c)
    return {
        "n_cellules": int(len(conf)),
        "exactitude_esperee": float(np.mean(esperee)),
        "entropie_moyenne_bits": float(np.mean(ent)),
        "entropie_maximale_moyenne_bits": float(np.mean(ent_max)),
        "part_entropie_maximale": float(np.mean(ent) / np.mean(ent_max)) if np.mean(ent_max) else float("nan"),
        "part_cellules_quasi_certaines": float(np.mean(conf > 0.99)),
        "ecart_de_calibration_attendu": float(ece),
        "calibration_par_decile": deciles,
    }


# --------------------------------------------------------------------------------------
# 3. Resume d'une condition
# --------------------------------------------------------------------------------------

def resumer(nom, pred, verite, plafond, colonnes=None):
    """Exactitude, IC bootstrap, normalisation, diversite et accord par paires.

    colonnes restreint le calcul a un sous ensemble d'items, ce qui sert au tableau par
    famille. Le masque exclut les cellules non predites : sans lui, une condition qui ne
    couvre pas tous les items (C3F ne couvre que les 58 items des six familles, un run
    tronque par la fin dure ne couvre pas toutes les personnes) verrait ses cellules
    absentes comptees comme des erreurs.
    """
    if colonnes is not None:
        pred, verite = pred[:, colonnes], verite[:, colonnes]
    masque = np.array([[(p is not None) and (not est_manquant(v))
                        for p, v in zip(lp, lv)] for lp, lv in zip(pred, verite)])
    if masque.sum() == 0:
        return None
    acc = exactitude_par_personne(pred, verite, masque)
    moy, bas, haut = bootstrap_personnes(acc)
    div = profil_diversite(pred, verite)
    return {
        "condition": nom,
        "n_cellules": int(masque.sum()),
        "exactitude": moy, "ic_bas": bas, "ic_haut": haut,
        "normalise": moy / plafond if plafond else float("nan"),
        "part_diversite_humaine": div["part_diversite_humaine"],
        "accord_par_paires": div["accord_par_paires"],
    }


def ligne_texte(l):
    ic = f"[{l['ic_bas']:.4f} ; {l['ic_haut']:.4f}]"
    return (f"{l['condition']:<26}{l['exactitude']:>10.4f}{ic:>22}"
            f"{l['normalise'] * 100:>11.1f}%{l['part_diversite_humaine'] * 100:>13.1f}%"
            f"{l['accord_par_paires'] * 100:>10.1f}%")


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suffixe", default="",
                    help="suffixe des traces a lire, par exemple smoke ou debit")
    ap.add_argument("--personnes", default="",
                    help="csv du sous echantillon ; par defaut data/traces/a5-personnes.csv, "
                         "ou a defaut les personnes presentes dans les traces")
    ap.add_argument("--sortie", default=os.path.join(SORTIE, "a5_resultats.json"))
    ap.add_argument("--sans-baselines", action="store_true",
                    help="saute le recalcul de B0, B1 et B2, qui prend quelques minutes")
    args = ap.parse_args()

    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    index_personne = {p: i for i, p in enumerate(ids)}
    index_item = {c: j for j, c in enumerate(items)}

    tables, fichiers = lire_traces(args.suffixe)
    if not tables:
        sys.exit(f"aucune trace lue dans {TRACES} (suffixe '{args.suffixe}')")
    print("traces lues :")
    for f in fichiers:
        print(f"  {f}")
    for (c, p), t in sorted(tables.items()):
        print(f"  {c} passe {p} : {len(t)} appels")

    # Population evaluee. Le fichier du run fait foi ; sinon on prend ce que les traces
    # contiennent, ce qui est le cas d'un smoke test.
    chemin_personnes = args.personnes or os.path.join(TRACES, "a5-personnes.csv")
    vus = set()
    for t in tables.values():
        vus |= {k[0] for k in t}
    if os.path.exists(chemin_personnes) and not args.suffixe:
        ech = pd.read_csv(chemin_personnes)
        personnes = [p for p in ech["pid"] if p in vus]
    else:
        personnes = [p for p in ids if p in vus]
    lignes_p = [index_personne[p] for p in personnes]

    # Items evalues : ceux qui apparaissent dans les traces. Sur un run tronque par la
    # fin dure, ce n'est pas forcement les 149.
    vus_items = set()
    for t in tables.values():
        vus_items |= {k[1] for k in t}
    items_ev = [c for c in items if c in vus_items]
    colonnes = [index_item[c] for c in items_ev]
    print(f"\n{len(personnes)} personnes evaluees, {len(items_ev)} items")

    verite = y1[np.ix_(lignes_p, colonnes)]
    verite2 = y2[np.ix_(lignes_p, colonnes)]

    # Plafond humain : la consistance test retest DE CES personnes, sur CES items.
    retest = exactitude_par_personne(verite2, verite)
    plafond, pl_bas, pl_haut = bootstrap_personnes(retest)
    print(f"plafond humain test retest de ces personnes : {plafond:.4f} "
          f"[{pl_bas:.4f} ; {pl_haut:.4f}]\n")

    resultats = {
        "n_personnes": len(personnes), "n_items": len(items_ev),
        "plafond_humain": {"exactitude": plafond, "ic_bas": pl_bas, "ic_haut": pl_haut},
        "traces": [os.path.basename(f) for f in fichiers],
        "conditions_a5": [], "distributions_a5": {},
        "baselines": [], "references": [], "par_famille": [],
    }
    # Matrices conservees pour le tableau par famille. Cle : nom de methode.
    matrices = {}

    entete = (f"{'condition':<26}{'exactitude':>10}{'IC 95%':>22}{'normalise':>12}"
              f"{'diversite':>13}{'accord':>10}")

    # --- nos agents ---------------------------------------------------------------
    print("nos agents locaux")
    print(entete)
    for condition in ["C2", "C3", "C3F"]:
        fusion, passes = moyenner_passes(tables, condition)
        if not fusion:
            continue
        pred, dist = en_matrices(fusion, personnes, items_ev, table)
        nom = f"{condition} ({len(passes)} passe{'s' if len(passes) > 1 else ''})"
        l = resumer(nom, pred, verite, plafond)
        masses = np.array([d["masse_lettres"] for d in fusion.values()])
        l["masse_lettres_mediane"] = float(np.median(masses))
        l["appels_rejetes"] = int(sum(1 for d in fusion.values() if d["rejet"]))
        l["duree_ms_mediane"] = float(np.median([d["duree_ms"] for d in fusion.values()]))
        resultats["conditions_a5"].append(l)
        matrices[condition] = pred
        print(ligne_texte(l))
        resultats["distributions_a5"][condition] = mesures_distributionnelles(dist, verite)

        # Chaque passe seule, pour voir si l'inversion de l'ordre des modalites change le
        # resultat. Si les deux passes different beaucoup, le biais de position est reel
        # et la moyenne des deux n'est pas un detail cosmetique.
        if len(passes) > 1:
            for p in passes:
                sous = {k: {"distribution": v["distribution"], "argmax": v["argmax"],
                            "masse_lettres": v["masse_lettres"], "duree_ms": v["duree_ms"],
                            "rejet": v["rejet"]}
                        for k, v in tables[(condition, p)].items()}
                pr, _ = en_matrices(sous, personnes, items_ev, table)
                lp = resumer(f"{condition} passe {p} seule", pr, verite, plafond)
                resultats["conditions_a5"].append(lp)
                print(ligne_texte(lp))

    # --- humains vague 2 et conditions de Stanford ---------------------------------
    print("\npoints de reference, memes personnes et memes items")
    print(entete)
    l = resumer("humains vague 2", verite2, verite, plafond)
    resultats["references"].append(l)
    matrices["humains vague 2"] = verite2
    print(ligne_texte(l))
    for libelle, fichier in CONDITIONS_LLM.items():
        chemin = os.path.join(PREP, fichier)
        if not os.path.exists(chemin):
            continue
        d = pd.read_csv(chemin)
        assert list(d["email"]) == ids, f"{fichier} n'est pas aligne sur l'index de charger()"
        p = d[items_ev].values.astype(object)[lignes_p]
        l = resumer(libelle, p, verite, plafond)
        resultats["references"].append(l)
        matrices[libelle] = p
        print(ligne_texte(l))

    # --- baselines sans modele de langage ------------------------------------------
    if not args.sans_baselines:
        print("\nbaselines sans modele de langage, memes personnes et memes items")
        print("  (recalculees sur le decoupage de a2, puis restreintes a ces personnes ;")
        print("   chaque personne evaluee est en test, l'apprentissage se fait sur les autres)")
        plis, blocs = grille(len(ids), len(items), GRAINE)
        pred_b = evaluer_baselines(items, y1, x, plis, blocs)
        print(entete)
        for nom in ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax"]:
            p = pred_b[nom][np.ix_(lignes_p, colonnes)]
            l = resumer(nom, p, verite, plafond)
            resultats["baselines"].append(l)
            matrices[nom] = p
            print(ligne_texte(l))

    # --- par famille thematique ------------------------------------------------------
    # Motif, tache 2 de resultats/a8-baselines-durcies.md : avec des blocs aleatoires, un
    # item secret garde ses cousins thematiques dans le contexte et B2 en profite. Quand la
    # famille entiere sort du contexte, les agents composite de Stanford battent B2. Le
    # chiffre global masque donc l'endroit ou un modele de langage sert a quelque chose,
    # et il faut regarder famille par famille.
    #
    # Attention a la lecture. Nos C2 et C3, comme B0, B1 et B2 ci dessus, sont ici en
    # decoupage par BLOCS ALEATOIRES, celui du run : les cousins de l'item secret sont
    # restes dans le contexte. Seule la condition C3F, si elle a tourne, est en regime
    # famille retiree. La comparaison stricte avec a8_familles.py porte sur C3F contre
    # "B2 famille retiree", qui n'est pas recalculee ici et se lit dans a8-familles-gss.csv.
    familles_cols = {}
    for nom_f, membres in FAMILLES.items():
        cols = [items_ev.index(i) for i in membres if i in items_ev]
        if cols:
            familles_cols[nom_f] = cols

    if familles_cols and matrices:
        print("\npar famille thematique, memes personnes")
        entete_f = (f"{'methode':<26}{'items':>6}{'exactitude':>12}{'normalise':>11}"
                    f"{'diversite':>12}{'accord':>10}")
        for nom_f, cols in familles_cols.items():
            # Plafond humain propre a la famille : la consistance test retest de ces
            # personnes sur ces items la, pas la moyenne sur les 149.
            retest_f = exactitude_par_personne(verite2[:, cols], verite[:, cols])
            plafond_f, _, _ = bootstrap_personnes(retest_f)
            print(f"\n  {nom_f} ({len(cols)} items), plafond humain {plafond_f:.4f}")
            print("  " + entete_f)
            for methode, mat in matrices.items():
                l = resumer(methode, mat, verite, plafond_f, colonnes=cols)
                if l is None:
                    continue
                l["famille"] = nom_f
                l["n_items"] = len(cols)
                l["plafond_humain_famille"] = plafond_f
                resultats["par_famille"].append(l)
                print(f"  {methode:<26}{len(cols):>6}{l['exactitude']:>12.4f}"
                      f"{l['normalise'] * 100:>10.1f}%{l['part_diversite_humaine'] * 100:>11.1f}%"
                      f"{l['accord_par_paires'] * 100:>9.1f}%")
        if resultats["par_famille"]:
            chemin_f = os.path.join(SORTIE, "a5-familles.csv")
            os.makedirs(SORTIE, exist_ok=True)
            pd.DataFrame(resultats["par_famille"]).to_csv(chemin_f, index=False,
                                                          float_format="%.6f")
            print(f"\necrit : {chemin_f}")

    # --- ce que seules les distributions permettent ---------------------------------
    print("\nmesures distributionnelles, propres a nos agents")
    for condition, m in resultats["distributions_a5"].items():
        if not m:
            continue
        print(f"\n  {condition} sur {m['n_cellules']} cellules")
        print(f"    exactitude esperee (probabilite de la vraie reponse) : "
              f"{m['exactitude_esperee']:.4f}")
        print(f"    entropie moyenne par appel : {m['entropie_moyenne_bits']:.4f} bits "
              f"sur un maximum moyen de {m['entropie_maximale_moyenne_bits']:.4f}, "
              f"soit {m['part_entropie_maximale'] * 100:.1f} %")
        print(f"    part des appels quasi certains (p max > 0,99) : "
              f"{m['part_cellules_quasi_certaines'] * 100:.1f} %")
        print(f"    ecart de calibration attendu : {m['ecart_de_calibration_attendu']:.4f}")
        print(f"    {'decile':<12}{'n':>8}{'confiance':>12}{'exactitude':>12}{'ecart':>10}")
        for d in m["calibration_par_decile"]:
            print(f"    {d['decile']:<12}{d['n']:>8}{d['confiance_moyenne']:>12.4f}"
                  f"{d['exactitude_reelle']:>12.4f}{d['ecart']:>10.4f}")

    os.makedirs(os.path.dirname(args.sortie), exist_ok=True)
    with open(args.sortie, "w", encoding="utf-8") as fh:
        json.dump(resultats, fh, indent=2, ensure_ascii=False)
    print(f"\necrit : {args.sortie}")


if __name__ == "__main__":
    main()
