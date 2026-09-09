"""
a21_evaluer_ext : evaluation de C2 sur l'UNION des 300 personnes, 150 de a5 et 150 de a21.

Pourquoi un script de plus. Les deux scripts d'evaluation existants ne savent pas faire
l'union, et la consigne interdit de les modifier :

  a5_evaluer.lire_traces(suffixe) lit SOIT les traces sans suffixe, SOIT celles d'un
  suffixe donne, jamais les deux. Le filtre est explicite : sans suffixe il ne garde que
  les fichiers dont le nom porte deux tirets, ce qui exclut a5-C2-p1-ext.jsonl.

  a18_decomposition_traces.main() lit en dur data/traces/a5-personnes.csv pour definir sa
  population, et passe le meme suffixe unique a lire_traces.

Ce que fait ce script, sans toucher a l'un ni a l'autre. Il appelle lire_traces DEUX fois,
fusionne les deux dictionnaires sur la cle (condition, passe), et fait l'union des deux
fichiers de population. Tout le reste est importe :

  de a5_evaluer   : moyenner_passes, en_matrices, resumer, ligne_texte,
                    mesures_distributionnelles
  de a18          : coder, masse_valide, Banc, compter_frac, decomposer_frac, agreger2,
                    _degenerer, MESURES
  de a1           : AXES, lire_nomenclature, lire_demographies, decomposer
  de a2           : charger, CONDITIONS_LLM, PREP

Aucune formule n'est reecrite. Les ratios inter et intra sont donc ceux de a18, avec la
meme correction residuelle par permutation, le meme bootstrap recentre sur les personnes
et la meme statistique P(sup).

Ce qu'il ajoute, et c'est la raison d'etre du chantier. La question ouverte de a18
section 12 est : le terme inter est il estimable a 150 personnes ? Le juge est le controle
de la vague 2, qui doit tomber au voisinage de 1 sur chaque axe. Le script mesure donc la
MEME chose sur trois populations et les met cote a cote :

  150 d'origine     ce que a18 publie aujourd'hui
  150 d'extension   un second echantillon independant, meme protocole
  300 union         la population du papier si l'extension aboutit

Si le controle vague 2 se resserre autour de 1 en passant de 150 a 300 sur le genre, la
race et l'education, ces axes redeviennent publiables. Sinon, la reponse a Simon est que
le probleme n'est pas la taille d'echantillon mais l'estimateur.

Entree  : data/traces/a5-C2-p1.jsonl, data/traces/a5-C2-p1-ext.jsonl,
          data/traces/a5-personnes.csv, data/traces/a5-personnes-ext.csv. Lecture seule.
Sortie  : resultats/a21-extension-c2.json et deux CSV, plus un tableau sur stdout.

Usage :
  .venv/bin/python analyses/a21_evaluer_ext.py
  .venv/bin/python analyses/a21_evaluer_ext.py --rapide
  .venv/bin/python analyses/a21_evaluer_ext.py --sans-decomposition
"""

import os
import sys

# Quatre coeurs, meme consigne qu'en a18 : un run de modele peut tourner sur la meme
# machine et deux calculs qui la saturent s'effondrent mutuellement.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "VECLIB_MAXIMUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "4")

import argparse
import csv
import json

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a1_double_distorsion import AXES, decomposer, lire_demographies, lire_nomenclature, normaliser
from a2_baselines_gss import CONDITIONS_LLM, PREP, charger
from a2_commun import bootstrap_personnes, exactitude_par_personne
from a5_agents_locaux_gss import TRACES, nomenclature
from a5_evaluer import (en_matrices, ligne_texte, lire_traces, mesures_distributionnelles,
                        moyenner_passes, resumer)
from a18_decomposition_traces import (MESURES, Banc, _degenerer, agreger2, coder,
                                      compter_frac, decomposer_frac, masse_valide)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OSF = os.path.join(RACINE, "data/osf-t6g7k-stanford")
SORTIE = os.path.join(RACINE, "resultats")
REFERENCE = "humains vague 1"
CONDITION = "C2"


# --------------------------------------------------------------------------------------
# 1. Union des traces et des populations
# --------------------------------------------------------------------------------------

def lire_union(suffixes=("", "ext")):
    """Fusionne plusieurs appels a a5_evaluer.lire_traces sur la cle (condition, passe).

    Les deux traces portent des personnes disjointes par construction (a21 tire dans le
    complementaire), la fusion ne peut donc pas ecraser une cellule. Le recouvrement est
    verifie et rapporte : s'il n'est pas nul, quelque chose ne va pas dans l'echantillon.
    """
    tables, fichiers, recouvrement = {}, [], 0
    for s in suffixes:
        try:
            t, f = lire_traces(s)
        except SystemExit:
            continue
        if not t:
            continue
        fichiers += f
        for cle, d in t.items():
            deja = tables.setdefault(cle, {})
            recouvrement += len(set(deja) & set(d))
            deja.update(d)
    return tables, fichiers, recouvrement


def population(fichiers_csv, vus):
    """Union ordonnee des fichiers d'echantillon, restreinte aux personnes vues."""
    ordre, connus = [], set()
    for chemin in fichiers_csv:
        if not os.path.exists(chemin):
            continue
        for p in pd.read_csv(chemin)["pid"]:
            if p not in connus:
                connus.add(p)
                ordre.append(p)
    return [p for p in ordre if p in vus], ordre


def personnes_completes(fusion, items, seuil):
    """Personnes dont la trace couvre au moins `seuil` des items. Copie de a18."""
    par_pid = {}
    for (pid, it) in fusion:
        if it in items:
            par_pid[pid] = par_pid.get(pid, 0) + 1
    return {p for p, c in par_pid.items() if c >= seuil * len(items)}


# --------------------------------------------------------------------------------------
# 2. La decomposition, sur une population donnee
# --------------------------------------------------------------------------------------

def decomposition(lignes, colonnes, items_ev, seg, niveaux, options, codes, tenseurs,
                  masque, n_min, rng, n_boot, n_perm, controle=False):
    """Ratios inter et intra, global et par axe, avec correction de permutation.

    Formules et discipline reprises telles quelles de a18 :
      - le terme inter obtenu sous permutation des etiquettes de segment est soustrait ;
      - le bootstrap est fait sur les personnes, recentre de facon additive sur
        l'estimation ponctuelle, et sert a estimer la forme et non le centre ;
      - P(sup) est la part des tirages ou le terme inter depasse celui des humains, seule
        statistique qui reste lisible quand le denominateur bootstrap approche zero.
    """
    banc = Banc(lignes, colonnes, items_ev, seg, niveaux, options, n_min)
    valide_cell = masque.astype(np.float64)
    noms = list(tenseurs)

    if controle:
        # Controle de degenerescence de a18 : alimente par des Dirac, la voie
        # fractionnaire doit redonner la voie ponctuelle de a1 au bit pres.
        pire = 0.0
        for nom in [REFERENCE, "humains vague 2"]:
            idx, poubelle = banc.index_point(codes[nom])
            c_pt = banc.compter_point(idx, poubelle, np.arange(banc.n))
            dec_pt = decomposer(c_pt, banc._faux_ordinal, n_min=n_min)
            dec_fr = decomposer_frac(compter_frac(tenseurs[nom], valide_cell, banc.W),
                                     n_min=n_min)
            a_pt = agreger2({m: dec_pt[m] for m in MESURES}, banc.masque_items)
            a_fr = agreger2(dec_fr, banc.masque_items)
            for m in MESURES:
                for t in (0, 1):
                    pire = max(pire, abs(a_pt[m][t] - a_fr[m][t]))
        print(f"  controle de degenerescence : ecart maximal {pire:.3e}")
        if pire > 1e-9:
            sys.exit("CONTROLE ECHOUE : les deux voies ne coincident pas.")
        print("  CONTROLE PASSE.")

    def dec_de(nom, poids=None, W=None):
        return decomposer_frac(
            compter_frac(tenseurs[nom], valide_cell, W or banc.W, poids), n_min=n_min)

    dec_point = {nom: dec_de(nom) for nom in noms}
    obs = {nom: agreger2(dec_point[nom], banc.masque_items) for nom in noms}
    obs_axe = {nom: {a: agreger2(dec_point[nom], banc.masque_items, axes_gardes=[i])
                     for i, a in enumerate(AXES)} for nom in noms}

    nul = {nom: {m: [] for m in MESURES} for nom in noms}
    nul_axe = {nom: {a: {m: [] for m in MESURES} for a in AXES} for nom in noms}
    for _ in range(n_perm):
        perm = rng.permutation(banc.n)
        Wp = [w[perm] for w in banc.W]
        for nom in noms:
            d = dec_de(nom, W=Wp)
            ag = agreger2(d, banc.masque_items)
            for m in MESURES:
                nul[nom][m].append(ag[m][0])
            for i, a in enumerate(AXES):
                ag_a = agreger2(d, banc.masque_items, axes_gardes=[i])
                for m in MESURES:
                    nul_axe[nom][a][m].append(ag_a[m][0])
    nul = {nom: {m: float(np.mean(v)) for m, v in d.items()} for nom, d in nul.items()}
    nul_axe = {nom: {a: {m: float(np.mean(v)) for m, v in d.items()}
                     for a, d in dd.items()} for nom, dd in nul_axe.items()}

    point = {nom: {m: (obs[nom][m][0] - nul[nom][m], obs[nom][m][1]) for m in MESURES}
             for nom in noms}
    point_axe = {nom: {a: {m: (obs_axe[nom][a][m][0] - nul_axe[nom][a][m],
                               obs_axe[nom][a][m][1]) for m in MESURES} for a in AXES}
                 for nom in noms}
    ref, ref_axe = point[REFERENCE], point_axe[REFERENCE]

    tir = {nom: {m: [] for m in MESURES} for nom in noms}
    for b in range(n_boot):
        sel = rng.integers(0, banc.n, size=banc.n)
        poids = np.bincount(sel, minlength=banc.n).astype(np.float64)
        for nom in noms:
            ag = agreger2(dec_de(nom, poids=poids), banc.masque_items)
            for m in MESURES:
                tir[nom][m].append(ag[m][0])
    def recentrer(v, cible):
        v = np.asarray(v, dtype=float)
        f = np.isfinite(v)
        return v if f.sum() < 20 else v - v[f].mean() + cible
    boot = {nom: {m: recentrer(tir[nom][m], point[nom][m][0]) for m in MESURES}
            for nom in noms}
    signe = {nom: {m: float(np.mean(boot[nom][m] > boot[REFERENCE][m]))
                   for m in MESURES} for nom in noms}

    return {
        "n": banc.n, "J": banc.J, "cellules": int(masque.sum()),
        "ratios": {nom: {m: (point[nom][m][0] / ref[m][0] if ref[m][0] else float("nan"),
                             point[nom][m][1] / ref[m][1] if ref[m][1] else float("nan"))
                         for m in MESURES} for nom in noms},
        "total": {nom: {m: ((point[nom][m][0] + point[nom][m][1])
                            / (ref[m][0] + ref[m][1])) for m in MESURES} for nom in noms},
        "p_sup": signe,
        "denominateur_axe": {a: ref_axe[a]["entropie"][0] for a in AXES},
        "ratios_axe": {nom: {a: (point_axe[nom][a]["entropie"][0] / ref_axe[a]["entropie"][0]
                                 if ref_axe[a]["entropie"][0] else float("nan"))
                             for a in AXES} for nom in noms},
    }


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap", type=int, default=1000)
    ap.add_argument("--permutations", type=int, default=50)
    ap.add_argument("--graine", type=int, default=20260908)
    ap.add_argument("--n-min", type=int, default=30)
    ap.add_argument("--couverture", type=float, default=0.98)
    ap.add_argument("--rapide", action="store_true",
                    help="bootstrap 100 et 15 permutations, pour un essai")
    ap.add_argument("--sans-decomposition", action="store_true",
                    help="exactitude, diversite et accord seulement")
    ap.add_argument("--sortie", default=os.path.join(SORTIE, "a21-extension-c2.json"))
    args = ap.parse_args()
    if args.rapide:
        args.bootstrap, args.permutations = 100, 15
    rng = np.random.default_rng(args.graine)

    print("=" * 100)
    print("a21 : C2 SUR L'UNION DES 300 PERSONNES")
    print("=" * 100)

    options, ordinal = lire_nomenclature(OSF)
    table_nom = nomenclature()
    ids, items, y1, y2, x_dem, attributs = charger()
    index_personne = {p: i for i, p in enumerate(ids)}
    index_item = {c: j for j, c in enumerate(items)}
    seg, niveaux = lire_demographies(OSF, ids)

    tables, fichiers, recouvrement = lire_union()
    if not tables:
        sys.exit("aucune trace lue")
    print("\ntraces lues en LECTURE SEULE :")
    for f in fichiers:
        print(f"  {f}")
    print(f"cellules presentes dans les deux traces a la fois : {recouvrement}")
    if recouvrement:
        print("AVERTISSEMENT : les deux echantillons se recouvrent, ce qui ne devrait "
              "pas arriver. La derniere trace lue l'emporte.")

    fusion, passes = moyenner_passes(tables, CONDITION)
    if not fusion:
        sys.exit(f"aucune cellule pour {CONDITION}")
    complets = personnes_completes(fusion, set(items), args.couverture)
    vus = {k[0] for k in fusion}
    csvs = [os.path.join(TRACES, "a5-personnes.csv"),
            os.path.join(TRACES, "a5-personnes-ext.csv")]
    _, ordre_ech = population(csvs, vus)
    ech0 = set(pd.read_csv(csvs[0])["pid"]) if os.path.exists(csvs[0]) else set()
    ech1 = set(pd.read_csv(csvs[1])["pid"]) if os.path.exists(csvs[1]) else set()

    personnes = [p for p in ordre_ech if p in complets]
    items_vus = {k[1] for k in fusion} & set(items)
    items_ev = [c for c in items if c in items_vus]
    colonnes = [index_item[c] for c in items_ev]
    lignes = [index_personne[p] for p in personnes]
    print(f"\n{len(fusion)} cellules {CONDITION}, passes {passes}")
    print(f"{len(vus)} personnes touchees, {len(complets)} couvertes a "
          f"{args.couverture:.0%}, {len(items_ev)} items")
    print(f"population evaluee : {len(personnes)} personnes, dont "
          f"{len([p for p in personnes if p in ech0])} du premier echantillon et "
          f"{len([p for p in personnes if p in ech1])} de l'extension")
    if not personnes:
        sys.exit("aucune personne complete, rien a mesurer")

    verite = y1[np.ix_(lignes, colonnes)]
    verite2 = y2[np.ix_(lignes, colonnes)]
    retest = exactitude_par_personne(verite2, verite)
    plafond, pl_bas, pl_haut = bootstrap_personnes(retest)
    print(f"plafond humain test retest de ces personnes : {plafond:.4f} "
          f"[{pl_bas:.4f} ; {pl_haut:.4f}]")

    resultats = {"n_personnes": len(personnes), "n_items": len(items_ev),
                 "n_premier_echantillon": len([p for p in personnes if p in ech0]),
                 "n_extension": len([p for p in personnes if p in ech1]),
                 "plafond_humain": plafond, "traces": [os.path.basename(f) for f in fichiers],
                 "conditions": [], "distributions": {}, "decomposition": {}}

    # --- exactitude, diversite, accord par paires -------------------------------------
    pred, dist = en_matrices(fusion, personnes, items_ev, table_nom)
    brut = {REFERENCE: verite, "humains vague 2": verite2, CONDITION: pred}
    entete = (f"{'condition':<30}{'exactitude':>10}{'IC 95%':>22}{'normalise':>12}"
              f"{'diversite':>13}{'accord':>10}")
    print("\nEXACTITUDE, DIVERSITE ET ACCORD PAR PAIRES, memes personnes et memes items")
    print(entete)
    l = resumer(f"{CONDITION} ({len(passes)} passe)", pred, verite, plafond)
    resultats["conditions"].append(l)
    print(ligne_texte(l))
    l = resumer("humains vague 2", verite2, verite, plafond)
    resultats["conditions"].append(l)
    print(ligne_texte(l))
    for libelle, fichier in CONDITIONS_LLM.items():
        chemin = os.path.join(PREP, fichier)
        if not os.path.exists(chemin):
            continue
        d = pd.read_csv(chemin)
        assert list(d["email"]) == ids, f"{fichier} n'est pas aligne sur charger()"
        p = d[items_ev].values.astype(object)[lignes]
        brut[libelle] = p
        l = resumer(libelle, p, verite, plafond)
        resultats["conditions"].append(l)
        print(ligne_texte(l))

    m = mesures_distributionnelles(dist, verite)
    resultats["distributions"][CONDITION] = m
    if m:
        print(f"\nmesures distributionnelles de {CONDITION}, {m['n_cellules']} cellules")
        print(f"  exactitude esperee : {m['exactitude_esperee']:.4f}")
        print(f"  entropie moyenne par appel : {m['entropie_moyenne_bits']:.4f} bits "
              f"sur {m['entropie_maximale_moyenne_bits']:.4f}, soit "
              f"{m['part_entropie_maximale'] * 100:.1f} %")
        print(f"  part des appels a p max > 0,99 : "
              f"{m['part_cellules_quasi_certaines'] * 100:.1f} %")
        print(f"  ecart de calibration attendu : {m['ecart_de_calibration_attendu']:.4f}")

    if args.sans_decomposition:
        ecrire(resultats, args.sortie)
        return

    # --- decomposition inter et intra --------------------------------------------------
    codes_all = {nom: coder(mat, items_ev, options) for nom, mat in brut.items()}
    masque_all = masse_valide(codes_all, codes_all[REFERENCE])
    codes_all = {nom: np.where(masque_all, x, -1).astype(np.int16)
                 for nom, x in codes_all.items()}
    print(f"\ncellules exploitables par toutes les conditions : {int(masque_all.sum())} "
          f"sur {masque_all.size} ({100 * masque_all.mean():.2f} pour cent)")

    k_max = int(max(len(options[q.lower()]) for q in items_ev))

    def tenseurs_pour(sous_lignes_locales):
        """Tenseurs (n, J, K) restreints aux lignes locales demandees."""
        sel = np.array(sous_lignes_locales, dtype=int)
        T, C = {}, {}
        for nom, x in codes_all.items():
            xs = x[sel]
            P = np.zeros((len(sel), len(items_ev), k_max))
            ii, jj = np.where(xs >= 0)
            P[ii, jj, xs[ii, jj]] = 1.0
            T[nom] = P
            C[nom] = xs
        # C2 en version distributionnelle, puis durcie pour la version argmax.
        Q = np.zeros((len(sel), len(items_ev), k_max))
        for jl, it in enumerate(items_ev):
            pos = {normaliser(o): k for k, o in enumerate(options[it.lower()])}
            for il, i in enumerate(sel):
                d = dist[i][jl]
                if d is None or not masque_all[i, jl]:
                    continue
                for mod, p in d.items():
                    k = pos.get(normaliser(str(mod)))
                    if k is not None:
                        Q[il, jl, k] += p
        s = Q.sum(axis=2, keepdims=True)
        Q = np.where(s > 0, Q / np.where(s > 0, s, 1.0), 0.0)
        T[CONDITION] = _degenerer(Q)
        T[f"{CONDITION} distribution"] = Q
        C[f"{CONDITION} distribution"] = C[CONDITION]
        # Controle de a18 : l'argmax du tenseur doit redonner l'argmax de la trace.
        rec = np.where(T[CONDITION].sum(axis=2) > 0, np.argmax(T[CONDITION], axis=2), -1)
        att = C[CONDITION]
        ecart = int(((rec != att) & (att >= 0)).sum())
        if ecart:
            sys.exit(f"{ecart} cellules ou l'argmax du tenseur differe de la trace")
        return T, C

    sous_populations = [
        ("150 d'origine", [i for i, p in enumerate(personnes) if p in ech0]),
        ("150 d'extension", [i for i, p in enumerate(personnes) if p in ech1]),
        ("300 union", list(range(len(personnes)))),
    ]

    lignes_csv = [["population", "n", "condition", "mesure", "ratio_inter",
                   "p_sup", "ratio_intra", "ratio_total"]]
    lignes_axe = [["population", "n", "condition"] + AXES]
    for libelle, loc in sous_populations:
        if len(loc) < 10:
            print(f"\n[{libelle}] moins de 10 personnes, saute")
            continue
        print("\n" + "=" * 100)
        print(f"POPULATION : {libelle}, {len(loc)} personnes")
        print("=" * 100)
        T, C = tenseurs_pour(loc)
        sous_lignes = [lignes[i] for i in loc]
        # Une graine par sous population, et non un flux commun : les trois populations
        # doivent recevoir la meme suite de permutations et de tirages, sinon une partie
        # de l'ecart entre elles vient du generateur et non de l'echantillon.
        rng = np.random.default_rng(args.graine)
        n_min = args.n_min if len(loc) >= args.n_min else max(5, len(loc))
        r = decomposition(sous_lignes, colonnes, items_ev, seg, niveaux, options, C, T,
                          masque_all[np.array(loc, dtype=int)], n_min, rng,
                          args.bootstrap, args.permutations,
                          controle=(libelle == "300 union"))
        resultats["decomposition"][libelle] = r
        print(f"\n{'condition':<30}{'inter':>10}{'P(sup)':>9}{'intra':>10}{'total':>9}"
              "   (entropie)")
        for nom in r["ratios"]:
            e = r["ratios"][nom]["entropie"]
            print(f"{nom:<30}{e[0]:>10.3f}{r['p_sup'][nom]['entropie']:>9.2f}"
                  f"{e[1]:>10.3f}{r['total'][nom]['entropie']:>9.3f}")
            for mes in MESURES:
                v = r["ratios"][nom][mes]
                lignes_csv.append([libelle, len(loc), nom, mes, f"{v[0]:.4f}",
                                   f"{r['p_sup'][nom][mes]:.4f}", f"{v[1]:.4f}",
                                   f"{r['total'][nom][mes]:.4f}"])
        print(f"\nRATIO INTER PAR AXE, mesure entropie")
        print(f"{'condition':<30}" + "".join(f"{a[:12]:>14}" for a in AXES))
        print(f"{'DENOMINATEUR, inter humain':<30}"
              + "".join(f"{r['denominateur_axe'][a]:>14.2f}" for a in AXES)
              + "   <- bits")
        for nom in r["ratios_axe"]:
            print(f"{nom:<30}"
                  + "".join(f"{r['ratios_axe'][nom][a]:>14.2f}" for a in AXES))
            lignes_axe.append([libelle, len(loc), nom]
                              + [f"{r['ratios_axe'][nom][a]:.4f}" for a in AXES])

    # --- le juge : le controle de la vague 2 se resserre t il ? ------------------------
    print("\n" + "=" * 100)
    print("LE CONTROLE DE LA VAGUE 2 PAR AXE, LES TROIS POPULATIONS COTE A COTE")
    print("Il doit tomber au voisinage de 1. La ou il n'y tombe pas, l'axe n'est pas")
    print("publiable, et c'est une propriete de la taille d'echantillon (a18 section 11).")
    print("=" * 100)
    print(f"{'population':<20}{'n':>5}" + "".join(f"{a[:12]:>14}" for a in AXES))
    for libelle, r in resultats["decomposition"].items():
        v = r["ratios_axe"].get("humains vague 2", {})
        print(f"{libelle:<20}{r['n']:>5}"
              + "".join(f"{v.get(a, float('nan')):>14.2f}" for a in AXES))
    print(f"\n{'ecart absolu a 1':<20}")
    for libelle, r in resultats["decomposition"].items():
        v = r["ratios_axe"].get("humains vague 2", {})
        print(f"{libelle:<20}{r['n']:>5}"
              + "".join(f"{abs(v.get(a, float('nan')) - 1):>14.2f}" for a in AXES))

    os.makedirs(SORTIE, exist_ok=True)
    for nom, contenu in (("a21-decomposition.csv", lignes_csv),
                         ("a21-ratios-par-axe.csv", lignes_axe)):
        with open(os.path.join(SORTIE, nom), "w", newline="", encoding="utf-8") as fh:
            csv.writer(fh).writerows(contenu)
        print(f"ecrit : {os.path.join(SORTIE, nom)}")
    ecrire(resultats, args.sortie)


def ecrire(resultats, chemin):
    os.makedirs(os.path.dirname(chemin), exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(resultats, fh, indent=2, ensure_ascii=False, default=float)
    print(f"ecrit : {chemin}")


if __name__ == "__main__":
    main()
