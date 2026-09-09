"""
a23_axes_ic : intervalles de confiance bootstrap PAR AXE sur les ratios inter et intra.

Motif. a18_decomposition_traces.py publie les ratios par axe SANS intervalle : son bootstrap
ne porte que sur l'agregat des six axes. Or la question ouverte principale du chantier est de
savoir si le controle de la vague 2 passe SUR L'AXE IDEOLOGIE a 150 personnes, et un point
sans intervalle ne repond pas a cette question.

Ce script ne modifie pas a18. Il recopie sa preparation de banc telle quelle, lignes 411 a
606 du fichier d'origine, puis remplace le bloc de bootstrap agrege par un bootstrap par axe :
memes 50 permutations pour la correction residuelle, memes 1 000 tirages recentres sur
l'estimation ponctuelle, meme graine. Sur les axes, le resultat ponctuel est identique a celui
de a18 par construction ; seuls les intervalles sont nouveaux.

Aucun appel de modele de langage, traces lues en lecture seule.

Sortie : resultats/a23-axes-ic.csv, plus un tableau lisible sur la sortie standard.

Usage :
  .venv/bin/python analyses/a23_axes_ic.py
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a18_decomposition_traces import *          # noqa: F401,F403
from a18_decomposition_traces import (AXES, MESURES, REFERENCE, STANFORD, OSF, PREP,
                                      TRACES, CONDITIONS_LLM, Banc, agreger2,
                                      charger_traces, coder, compter_frac, decomposer,
                                      decomposer_frac, masse_valide, personnes_completes,
                                      _degenerer)
from a1_double_distorsion import (lire_nomenclature, lire_demographies, normaliser,
                                  construire_index, compter)
from a2_baselines_gss import charger
from a5_evaluer import en_matrices

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class _Args:
    suffixe = ""
    bootstrap = 1000
    permutations = 50
    graine = 20260908
    n_min = 30
    seg_min = 8
    couverture = 0.98
    sortie = os.path.join(RACINE, "resultats")


args = _Args()
os.makedirs(args.sortie, exist_ok=True)
rng = np.random.default_rng(args.graine)
journal = {}

print("=" * 100)
print("a18 : DECOMPOSITION INTER ET INTRA DES TRACES a5, C2 CONTRE C3")
print("=" * 100)

# --- donnees de reference -----------------------------------------------------
options, ordinal = lire_nomenclature(OSF)
ids, items, y1, y2, x_dem, attributs = charger()
index_personne = {p: i for i, p in enumerate(ids)}
index_item = {c: j for j, c in enumerate(items)}
seg, niveaux = lire_demographies(OSF, ids)
est_ordinal = np.array([ordinal.get(q.lower(), False) for q in items])
print(f"{len(ids)} personnes dans le corpus, {len(items)} items cibles, "
      f"{int(est_ordinal.sum())} ordinaux")

# --- traces ---------------------------------------------------------------------
presents, fichiers, table_nom = charger_traces(args.suffixe, None, items, index_item)
print("\ntraces lues en LECTURE SEULE :")
for f in fichiers:
    print(f"  {f}")
couverture = {}
for c, d in presents.items():
    complets = personnes_completes(d["fusion"], set(items), args.couverture)
    couverture[c] = complets
    print(f"  {c} : {d['n_appels']} appels, {len(d['pids'])} personnes touchees, "
          f"{len(complets)} personnes couvertes a {args.couverture:.0%}, "
          f"{len(d['items'] & set(items))} items")
journal["traces"] = {c: {"appels": d["n_appels"], "personnes_touchees": len(d["pids"]),
                         "personnes_completes": len(couverture[c])}
                     for c, d in presents.items()}

# Population commune : les personnes de l'echantillon du run couvertes par TOUTES les
# conditions presentes. C'est le seul choix qui rende C2 et C3 comparables.
ech = pd.read_csv(os.path.join(TRACES, "a5-personnes.csv"))
ordre_ech = [p for p in ech["pid"]]
commun = set(ordre_ech)
for c in presents:
    commun &= couverture[c]
personnes = [p for p in ordre_ech if p in commun]
if not personnes:
    sys.exit("aucune personne complete dans les traces, rien a mesurer")
lignes = [index_personne[p] for p in personnes]

# Items : ceux vus dans toutes les conditions presentes.
items_vus = set(items)
for c, d in presents.items():
    items_vus &= d["items"]
items_ev = [c for c in items if c in items_vus]
colonnes = [index_item[c] for c in items_ev]
print(f"\npopulation commune : {len(personnes)} personnes, {len(items_ev)} items, "
      f"soit {len(personnes) * len(items_ev)} cellules par condition")
journal["population"] = {"n_personnes": len(personnes), "n_items": len(items_ev),
                         "conditions_presentes": sorted(presents)}

n_min = args.n_min
if len(personnes) < n_min:
    n_min = max(5, len(personnes))
    print(f"AVERTISSEMENT : moins de {args.n_min} personnes, seuil d'item abaisse "
          f"a {n_min}. Les termes inter sont alors tres bruites.")
journal["n_min"] = n_min

# --- matrices de reponses, toutes conditions ------------------------------------
verite = y1[np.ix_(lignes, colonnes)]
verite2 = y2[np.ix_(lignes, colonnes)]
brut = {REFERENCE: verite, "humains vague 2": verite2}
for libelle, fichier in CONDITIONS_LLM.items():
    chemin = os.path.join(PREP, fichier)
    if not os.path.exists(chemin):
        continue
    d = pd.read_csv(chemin)
    assert list(d["email"]) == ids, f"{fichier} n'est pas aligne sur charger()"
    brut[libelle] = d[items_ev].values.astype(object)[lignes]

distributions = {}
for c, d in presents.items():
    pred, dist = en_matrices(d["fusion"], personnes, items_ev, table_nom)
    brut[c] = pred
    distributions[c] = dist

codes = {nom: coder(m, items_ev, options) for nom, m in brut.items()}
masque = masse_valide(codes, codes[REFERENCE])
print(f"cellules exploitables par toutes les conditions : {int(masque.sum())} "
      f"sur {masque.size} ({100 * masque.mean():.2f} pour cent)")
journal["cellules_exploitables"] = int(masque.sum())
for nom, x in codes.items():
    codes[nom] = np.where(masque, x, -1).astype(np.int16)

banc = Banc(lignes, colonnes, items_ev, seg, niveaux, options, n_min)
noms = [REFERENCE, "humains vague 2"] + sorted(presents) + \
       [s for s in STANFORD if s in brut]

# --- tenseurs de distributions ---------------------------------------------------
# P[i, j, k] pour chaque condition. Les humains et Stanford sont degeneres : masse 1
# sur la modalite donnee. C'est ce qui rend le controle de degenerescence possible.
def tenseur_degenere(x):
    P = np.zeros((banc.n, banc.J, banc.k_max))
    ii, jj = np.where(x >= 0)
    P[ii, jj, x[ii, jj]] = 1.0
    return P

P = {nom: tenseur_degenere(codes[nom]) for nom in noms}
for c in presents:
    Q = np.zeros((banc.n, banc.J, banc.k_max))
    for j, it in enumerate(items_ev):
        liste = [normaliser(o) for o in options[it.lower()]]
        pos = {m: k for k, m in enumerate(liste)}
        for i in range(banc.n):
            d = distributions[c][i][j]
            if d is None or not masque[i, j]:
                continue
            for mod, p in d.items():
                k = pos.get(normaliser(str(mod)))
                if k is not None:
                    Q[i, j, k] += p
    s = Q.sum(axis=2, keepdims=True)
    Q = np.where(s > 0, Q / np.where(s > 0, s, 1.0), 0.0)
    P[c] = Q

valide_cell = masque.astype(np.float64)

# ================================================================================
# CONTROLE 1 : la version distributionnelle degeneree redonne la version ponctuelle
# ================================================================================
print("\n" + "=" * 100)
print("CONTROLE DE DEGENERESCENCE")
print("Les humains n'ont pas de distribution. Alimente par leurs Dirac, le chemin")
print("distributionnel doit redonner le chemin ponctuel de a1 au bit pres.")
print("=" * 100)
lignes_ctrl = [["condition", "mesure", "terme", "voie_ponctuelle_a1",
                "voie_distributionnelle", "ecart_absolu"]]
pire = 0.0
for nom in [REFERENCE, "humains vague 2"] + [s for s in STANFORD if s in brut][:2]:
    idx, poubelle = banc.index_point(codes[nom])
    c_pt = banc.compter_point(idx, poubelle, np.arange(banc.n))
    dec_pt = decomposer(c_pt, banc._faux_ordinal, n_min=n_min)
    c_fr = compter_frac(P[nom], valide_cell, banc.W)
    dec_fr = decomposer_frac(c_fr, n_min=n_min)
    a_pt = agreger2({m: dec_pt[m] for m in MESURES}, banc.masque_items)
    a_fr = agreger2(dec_fr, banc.masque_items)
    for m in MESURES:
        for t, lib in ((0, "inter"), (1, "intra")):
            e = abs(a_pt[m][t] - a_fr[m][t])
            pire = max(pire, e)
            lignes_ctrl.append([nom, m, lib, f"{a_pt[m][t]:.10f}",
                                f"{a_fr[m][t]:.10f}", f"{e:.3e}"])
print(f"ecart maximal entre les deux voies sur les conditions ponctuelles : {pire:.3e}")
if pire > 1e-9:
    sys.exit("CONTROLE ECHOUE : les deux voies ne coincident pas sur des reponses "
             "ponctuelles. Aucun chiffre distributionnel n'est publiable.")
print("CONTROLE PASSE. La voie distributionnelle est une generalisation exacte.")
journal["controle_degenerescence_ecart_max"] = pire
with open(os.path.join(args.sortie, "a18-controle-degenerescence.csv"), "w",
          newline="", encoding="utf-8") as fh:
    csv.writer(fh).writerows(lignes_ctrl)

# ================================================================================
# 5. La decomposition, deux versions
# ================================================================================
# Un "jeu" est un couple (libelle affiche, fonction qui rend la table de comptage a
# partir d'un vecteur de poids bootstrap). Les conditions ponctuelles passent par
# a1.compter, nos deux conditions passent en plus par la voie fractionnaire.
# T[libelle] est le tenseur (n, J, K) employe par TOUTES les mesures pour ce libelle :
# decomposition, permutation, bootstrap, mesure de Chen, dispersion totale. Le durcir
# ici une fois et pour toutes evite qu'une voie lise la distribution la ou une autre
# lit l'argmax, ce qui a ete une erreur reelle de la premiere version de ce script.
T = {}
jeux = []
index_pt = {}
for nom in noms:
    idx, poubelle = banc.index_point(codes[nom])
    index_pt[nom] = (idx, poubelle)
    lib = nom if nom not in presents else f"{nom} argmax"
    T[lib] = _degenerer(P[nom]) if nom in presents else P[nom]
    jeux.append((lib, nom, "argmax"))
for c in sorted(presents):
    T[f"{c} distribution"] = P[c]
    jeux.append((f"{c} distribution", c, "distribution"))

# Controle : le durcissement du tenseur redonne bien la matrice d'argmax de la trace.
for c in sorted(presents):
    d = _degenerer(P[c])
    rec = np.where(d.sum(axis=2) > 0, np.argmax(d, axis=2), -1)
    att = np.where(masque, codes[c], -1)
    ecart = int(((rec != att) & (att >= 0)).sum())
    if ecart:
        sys.exit(f"{ecart} cellules ou l'argmax du tenseur de {c} differe de "
                 "l'argmax enregistre dans la trace. Chaine de lecture incoherente.")
print("controle : l'argmax du tenseur de distributions coincide avec celui de la "
      "trace sur toutes les cellules.")

def dec_de(lib, poids=None, seg_perm=None):
    W = banc.W if seg_perm is None else seg_perm
    return decomposer_frac(compter_frac(T[lib], valide_cell, W, poids), n_min=n_min)

# ---------------------------------------------------------------------------------------
# Point, permutation et bootstrap, PAR AXE. Meme algorithme que a18, axe par axe.
# ---------------------------------------------------------------------------------------

def dec_de(lib, poids=None, seg_perm=None):
    W = banc.W if seg_perm is None else seg_perm
    return decomposer_frac(compter_frac(T[lib], valide_cell, W, poids), n_min=n_min)


libs = [l for l, _, _ in jeux]
dec_point = {lib: dec_de(lib) for lib in libs}
obs_axe = {lib: {a: agreger2(dec_point[lib], banc.masque_items, axes_gardes=[i])
                 for i, a in enumerate(AXES)} for lib in libs}

nul_axe = {lib: {a: {m: [] for m in MESURES} for a in AXES} for lib in libs}
for _ in range(args.permutations):
    perm = rng.permutation(banc.n)
    Wp = [w[perm] for w in banc.W]
    for lib in libs:
        d = dec_de(lib, seg_perm=Wp)
        for i, a in enumerate(AXES):
            ag = agreger2(d, banc.masque_items, axes_gardes=[i])
            for m in MESURES:
                nul_axe[lib][a][m].append(ag[m][0])
nul_axe = {lib: {a: {m: float(np.mean(v)) for m, v in dd.items()} for a, dd in d.items()}
           for lib, d in nul_axe.items()}
point_axe = {lib: {a: {m: (obs_axe[lib][a][m][0] - nul_axe[lib][a][m],
                           obs_axe[lib][a][m][1]) for m in MESURES} for a in AXES}
             for lib in libs}
print("correction residuelle par permutation faite", flush=True)

tir = {lib: {a: {m: ([], []) for m in MESURES} for a in AXES} for lib in libs}
for b in range(args.bootstrap):
    sel = rng.integers(0, banc.n, size=banc.n)
    poids = np.bincount(sel, minlength=banc.n).astype(np.float64)
    for lib in libs:
        d = dec_de(lib, poids=poids)
        for i, a in enumerate(AXES):
            ag = agreger2(d, banc.masque_items, axes_gardes=[i])
            for m in MESURES:
                tir[lib][a][m][0].append(ag[m][0])
                tir[lib][a][m][1].append(ag[m][1])
    if (b + 1) % 250 == 0:
        print(f"  bootstrap {b + 1}/{args.bootstrap}", flush=True)


def recentrer(v, cible):
    v = np.asarray(v, dtype=float)
    f = np.isfinite(v)
    return v if f.sum() < 20 else v - v[f].mean() + cible


def ic(v):
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    if v.size < 20:
        return float("nan"), float("nan")
    return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))


boot = {lib: {a: {m: (recentrer(tir[lib][a][m][0], point_axe[lib][a][m][0]),
                      recentrer(tir[lib][a][m][1], point_axe[lib][a][m][1]))
                  for m in MESURES} for a in AXES} for lib in libs}

sorties = []
for lib in libs:
    for a in AXES:
        for m in MESURES:
            lo, hi = ic(boot[lib][a][m][0] / boot[REFERENCE][a][m][0])
            lo2, hi2 = ic(boot[lib][a][m][1] / boot[REFERENCE][a][m][1])
            sorties.append({
                "condition": lib, "axe": a, "mesure": m,
                "inter_humain_vague1": point_axe[REFERENCE][a][m][0],
                "ratio_inter": point_axe[lib][a][m][0] / point_axe[REFERENCE][a][m][0],
                "inter_ic_bas": lo, "inter_ic_haut": hi,
                "p_sup": float(np.mean(boot[lib][a][m][0] > boot[REFERENCE][a][m][0])),
                "ratio_intra": point_axe[lib][a][m][1] / point_axe[REFERENCE][a][m][1],
                "intra_ic_bas": lo2, "intra_ic_haut": hi2,
            })
df = pd.DataFrame(sorties)
chemin = os.path.join(args.sortie, "a23-axes-ic.csv")
df.to_csv(chemin, index=False, float_format="%.4f")

for m in MESURES:
    print("\n" + "=" * 96)
    print(f"RATIO INTER PAR AXE AVEC INTERVALLE BOOTSTRAP, mesure {m}")
    print("=" * 96)
    print(f"{'condition':<26}{'axe':<20}{'inter humain':>13}{'ratio':>8}{'IC 95%':>22}{'P(sup)':>9}")
    for _, r in df[df.mesure == m].iterrows():
        print(f"{r['condition']:<26}{r['axe']:<20}{r['inter_humain_vague1']:>13.2f}"
              f"{r['ratio_inter']:>8.2f} [{r['inter_ic_bas']:>7.2f} ; {r['inter_ic_haut']:>7.2f}]"
              f"{r['p_sup']:>9.2f}")
print(f"\necrit : {chemin}")
