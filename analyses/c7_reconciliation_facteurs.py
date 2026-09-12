"""
c7_reconciliation_facteurs : pourquoi le plan factoriel (mesure A) et le tri des paires
Twin (mesure B) se contredisent frontalement sur « que devient le canal inter-jumeaux
quand on change UN SEUL element du pipeline ? ».

===========================================================================
AUCUN APPEL RESEAU, AUCUN APPEL DE MODELE, AUCUNE DEPENSE. Lecture seule sur data/.
Aucun script existant n'est modifie. Sorties autorisees UNIQUEMENT :
  resultats/c7-reconciliation-facteurs.csv
  resultats/c7-reconciliation-facteurs-2026-09-12.md   (redige a la main a partir d'ici)

LE CONFLIT.
  Mesure A, resultats/c7-factoriel-resultats.md (analyses/c7_factoriel.py) :
    modele seul different  0,67 %  [0,00 ; 1,75]
    gabarit seul different 0,83 %  [0,00 ; 2,08]
    persona seul different 2,65 %  [0,50 ; 5,13]        n = 120, pool = 120
  Mesure B, resultats/moonshot-2026-09-12.md a partir de c7-transfert-voletA.csv :
    decodage seul          83,6 %
    gabarit seul           70,5 %
    raisonnement seul      37,3 %
    modele seul            15-19 %                       n = 2 058, pool = 2 058

CE QUE CE SCRIPT FAIT, ET RIEN D'AUTRE : il ramene les deux series sur UNE SEULE
echelle -- memes 120 personnes, meme bassin de 120, memes 60 items, meme attaque
symetrique, meme bootstrap -- puis il mesure separement la seule quantite qui distingue
les deux familles de jumeaux : leur fidelite individuelle a la personne reelle.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                      les tables Twin, S_gra, couvertures
  c7_reidentification.rangs_attaque      l'attaque (rang, top1, top10), ex aequo melanges
  c7_reidentification.rang_dans_segment  le controle de segment
  c7_reidentification.items_communs      les 60 items toujours renseignes
  c7_reidentification.graine_nom         graine stable par nom
  a2_commun.distance_hamming             la distance, via rangs_attaque
  a2_commun.bootstrap_personnes          l'IC 95 %
  c7_deux_organisations.tirer_echantillon / construire_banque_items / GRAINE
                                          l'echantillon stratifie bit a bit identique
Les matrices B, C (data/traces/c7-deux-organisations.jsonl) et M, G, P
(data/traces/c7-factoriel.jsonl) sont relues en LECTURE SEULE.

ETHIQUE : aucun pid, aucun appariement individuel n'est imprime ni ecrit. Seuls des
taux agreges sortent.
Usage : .venv/bin/python analyses/c7_reconciliation_facteurs.py
===========================================================================
"""

import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                              # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes         # noqa: E402
from c7_reidentification import (                                    # noqa: E402
    rangs_attaque, rang_dans_segment, graine_nom, REF_V4, DEMO, N_BOOTSTRAP,
)
from c7_deux_organisations import (                                  # noqa: E402
    tirer_echantillon, construire_banque_items, GRAINE,
)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
TRACES = os.path.join(RACINE, "data", "traces")
TRACE_ORGS = os.path.join(TRACES, "c7-deux-organisations.jsonl")
TRACE_FACT = os.path.join(TRACES, "c7-factoriel.jsonl")

N = 120                      # le pool commun impose par la mesure A

# Les paliers que la mesure B (moonshot) lit dans c7-transfert-voletA.csv, nommes ici
# par ce qui change reellement entre les deux configurations Twin.
PALIERS_TWIN = [
    ("decodage seul (T=0 vs temperature par defaut)",
     "Text Persona - GPT4.1-mini", "Text Persona (Default Temperature) - GPT4.1-mini"),
    ("gabarit seul (repetition des questions)",
     "Text Persona - GPT4.1-mini", "Text Persona (Repeating Questions) - GPT4.1-mini"),
    ("raisonnement seul (reasoning active)",
     "Text Persona - GPT4.1-mini", "Text Persona (Reasoning) - GPT4.1-mini"),
    ("modele seul (GPT4.1-mini vs Gemini-Flash2.5)",
     "Text Persona - GPT4.1-mini", "Text Persona - Gemini-Flash2.5"),
    ("format de persona seul (texte vs JSON, meme modele mini)",
     "Text Persona - GPT4.1-mini", "JSON Persona - GPT4.1-mini"),
]

CONFIGS_FIDELITE = [
    DEMO,
    "JSON Persona - GPT4.1",
    "JSON Persona - GPT4.1-mini",
    "Text Persona (Default Temperature) - GPT4.1-mini",
    "Text Persona (Reasoning) - GPT4.1-mini",
    "Text Persona (Repeating Questions) - GPT4.1-mini",
    "Text Persona - GPT4.1-mini",
    "Text Persona - Gemini-Flash2.5",
]


# ---------------------------------------------------------------------------
# 1. Relecture des traces payantes (lecture seule)
# ---------------------------------------------------------------------------

def relire(chemin, cle_condition, valeurs, n_personnes, n_items):
    """{valeur: matrice (n_personnes, n_items)} depuis un jsonl de trace."""
    X = {v: np.full((n_personnes, n_items), -1, dtype=np.int32) for v in valeurs}
    nlus = {v: np.zeros(n_personnes, dtype=int) for v in valeurs}
    for ligne in open(chemin, encoding="utf-8"):
        try:
            e = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if not e.get("succes"):
            continue
        v = e.get(cle_condition)
        i = e.get("sample_idx")
        if v not in X or i is None or i >= n_personnes:
            continue
        X[v][i] = np.array(e["codes"], dtype=np.int32)
        nlus[v][i] = int(e.get("n_reponses_lues", 0))
    return X, nlus


# ---------------------------------------------------------------------------
# 2. Les deux estimands, calcules exactement comme la mesure A les calcule
# ---------------------------------------------------------------------------

def attaque_sym(X, Y, seg, nom):
    """Attaque symetrique X<->Y sur un bassin egal a l'echantillon entier (identique a
    c7_factoriel.mesurer_condition : moyenne des deux sens, bootstrap sur les personnes).
    """
    couverts = np.flatnonzero((X >= 0).any(axis=1) & (Y >= 0).any(axis=1))
    n = len(couverts)
    if n < 5:
        return None
    rng_f = np.random.default_rng([GRAINE, graine_nom(f"{nom}|f")])
    _, t1_f, t10_f = rangs_attaque(X[couverts], Y, couverts, rng_f)
    _, t1s_f, _ = rang_dans_segment(X[couverts], couverts, Y, seg, rng_f)
    rng_r = np.random.default_rng([GRAINE, graine_nom(f"{nom}|r")])
    _, t1_r, t10_r = rangs_attaque(Y[couverts], X, couverts, rng_r)
    _, t1s_r, _ = rang_dans_segment(Y[couverts], couverts, X, seg, rng_r)

    t1 = (t1_f + t1_r) / 2.0
    t10 = (t10_f + t10_r) / 2.0
    t1s = (t1s_f + t1s_r) / 2.0
    m, b, h = bootstrap_personnes(t1, n_tirages=N_BOOTSTRAP, graine=[GRAINE, graine_nom(nom), 1])
    m10, _, _ = bootstrap_personnes(t10, n_tirages=N_BOOTSTRAP, graine=[GRAINE, graine_nom(nom), 2])
    ms, _, _ = bootstrap_personnes(t1s, n_tirages=N_BOOTSTRAP, graine=[GRAINE, graine_nom(nom), 3])
    return {"n": n, "top1": m, "top1_bas": b, "top1_haut": h, "top10": m10,
            "top1_segment": ms, "hasard": 1.0 / n}


def attaque_vers_humain(X, H, nom):
    """Un seul sens : le jumeau X attaque le bassin des humains reels H (meme pool)."""
    couverts = np.flatnonzero((X >= 0).any(axis=1))
    n = len(couverts)
    if n < 5:
        return None
    rng = np.random.default_rng([GRAINE, graine_nom(nom), 7])
    _, t1, t10 = rangs_attaque(X[couverts], H, couverts, rng)
    m, b, h = bootstrap_personnes(t1, n_tirages=N_BOOTSTRAP, graine=[GRAINE, graine_nom(nom), 4])
    m10, _, _ = bootstrap_personnes(t10, n_tirages=N_BOOTSTRAP, graine=[GRAINE, graine_nom(nom), 5])
    return {"n": n, "top1": m, "top1_bas": b, "top1_haut": h, "top10": m10,
            "hasard": 1.0 / H.shape[0]}


# ---------------------------------------------------------------------------
# 3. Decomposition de l'accord : plancher entre inconnus / accord au vrai jumeau
# ---------------------------------------------------------------------------

def decomposer_accord(X, Y, seg):
    """(accord au vrai jumeau, accord a un inconnu, accord a un inconnu du meme segment).

    Meme grandeur que c7_temoin_prompt : fraction d'items ou les deux jumeaux s'accordent,
    via 1 - distance_hamming (masquage des manquants inclus, fait par la distance elle-meme).
    """
    couverts = np.flatnonzero((X >= 0).any(axis=1) & (Y >= 0).any(axis=1))
    if len(couverts) < 5:
        return None
    accord = 1.0 - distance_hamming(X[couverts], Y[couverts])
    vrai = np.diag(accord)
    hors = accord.copy()
    np.fill_diagonal(hors, np.nan)
    plancher = np.nanmean(hors, axis=1)
    s = seg[couverts]
    meme_seg = np.full(len(couverts), np.nan)
    for i in range(len(couverts)):
        m = (s == s[i]) & (np.arange(len(couverts)) != i) & (s >= 0)
        if m.any():
            meme_seg[i] = np.nanmean(hors[i][m])
    return {"accord_vrai": float(np.mean(vrai)),
            "accord_inconnu": float(np.mean(plancher)),
            "accord_meme_segment": float(np.nanmean(meme_seg)),
            "apport_individuel_pts": float(np.mean(vrai) - np.nanmean(meme_seg)) * 100.0}


def degenerescence(X):
    """Diagnostic de degenerescence d'un generateur : combien de vecteurs de reponses
    distincts parmi les personnes, et l'accord moyen entre deux personnes differentes."""
    lignes = [tuple(r.tolist()) for r in X]
    accord = 1.0 - distance_hamming(X, X)
    hors = accord.copy()
    np.fill_diagonal(hors, np.nan)
    return {"n_vecteurs_distincts": len(set(lignes)),
            "accord_moyen_entre_personnes": float(np.nanmean(hors)),
            "items_lus_moyen": float((X >= 0).sum(axis=1).mean())}


# ---------------------------------------------------------------------------
# 4. main
# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    idx_items, banque = construire_banque_items(paq)
    n_items = len(banque)
    print(f"{n_items} items cibles (memes que les deux mesures)", flush=True)

    ech = tirer_echantillon(paq["seg"]["S_gra"], 200, GRAINE)[:N]
    seg = paq["seg"]["S_gra"][ech]
    print(f"echantillon commun : {len(ech)} personnes (identique a c7_factoriel)", flush=True)

    # --- jumeaux payes par nous (mesure A) ---
    XBC, nlus_bc = relire(TRACE_ORGS, "org", ["B", "C"], N, n_items)
    XMGP, nlus_mgp = relire(TRACE_FACT, "condition", ["M", "G", "P"], N, n_items)
    notres = {"B": XBC["B"], "C": XBC["C"], "M": XMGP["M"], "G": XMGP["G"], "P": XMGP["P"]}

    # --- jumeaux publies par l'equipe Twin (mesure B), memes 120 personnes ---
    twin = {c: paq["codes"][c][:, idx_items][ech] for c in CONFIGS_FIDELITE
            if c in paq["codes"]}
    humain = paq["codes"][REF_V4][:, idx_items][ech]

    lignes = []

    print("\n=== 1. DEGENERESCENCE DES GENERATEURS (120 personnes, 60 items) ===",
          flush=True)
    for nom, X in list(notres.items()) + list(twin.items()):
        d = degenerescence(X)
        print(f"{nom:52s} vecteurs distincts {d['n_vecteurs_distincts']:4d}/120  "
              f"accord entre personnes {d['accord_moyen_entre_personnes']:.3f}  "
              f"items lus {d['items_lus_moyen']:.1f}", flush=True)
        lignes.append({"bloc": "degenerescence", "serie": nom,
                       "n_vecteurs_distincts": d["n_vecteurs_distincts"],
                       "accord_entre_personnes": d["accord_moyen_entre_personnes"],
                       "items_lus_moyen": d["items_lus_moyen"]})

    print("\n=== 2. FIDELITE : le jumeau retrouve-t-il la VRAIE personne ? "
          "(pool = 120 humains v4) ===", flush=True)
    for nom, X in list(notres.items()) + list(twin.items()):
        r = attaque_vers_humain(X, humain, f"fid|{nom}")
        if r is None:
            continue
        print(f"{nom:52s} top1 {r['top1']*100:6.2f} % [{r['top1_bas']*100:5.2f} ; "
              f"{r['top1_haut']*100:5.2f}]  top10 {r['top10']*100:5.1f} %  "
              f"(hasard {r['hasard']*100:.2f} %)", flush=True)
        lignes.append({"bloc": "fidelite_vs_humain_pool120", "serie": nom, "n": r["n"],
                       "top1": r["top1"], "top1_bas": r["top1_bas"],
                       "top1_haut": r["top1_haut"], "top10": r["top10"],
                       "hasard": r["hasard"]})

    print("\n=== 3. MESURE A REPRODUITE : B<->{M,G,P} et B<->C, pool = 120 ===", flush=True)
    for nom, Y in (("B<->M", notres["M"]), ("B<->G", notres["G"]),
                   ("B<->P", notres["P"]), ("B<->C", notres["C"])):
        r = attaque_sym(notres["B"], Y, seg, nom)
        if r is None:
            continue
        print(f"{nom:52s} n={r['n']:3d}  top1 {r['top1']*100:6.2f} % "
              f"[{r['top1_bas']*100:5.2f} ; {r['top1_haut']*100:5.2f}]  "
              f"top10 {r['top10']*100:5.1f} %  (hasard {r['hasard']*100:.2f} %)", flush=True)
        lignes.append({"bloc": "mesureA_pool120", "serie": nom, "n": r["n"],
                       "top1": r["top1"], "top1_bas": r["top1_bas"],
                       "top1_haut": r["top1_haut"], "top10": r["top10"],
                       "top1_segment": r["top1_segment"], "hasard": r["hasard"]})

    print("\n=== 4. MESURE B RAMENEE A L'ECHELLE DE A : memes 120 personnes, "
          "pool = 120, attaque symetrique ===", flush=True)
    for etiquette, cx, cy in PALIERS_TWIN:
        if cx not in twin or cy not in twin:
            print(f"absente : {etiquette}", flush=True)
            continue
        r = attaque_sym(twin[cx], twin[cy], seg, etiquette)
        if r is None:
            continue
        print(f"{etiquette:52s} n={r['n']:3d}  top1 {r['top1']*100:6.2f} % "
              f"[{r['top1_bas']*100:5.2f} ; {r['top1_haut']*100:5.2f}]  "
              f"top10 {r['top10']*100:5.1f} %", flush=True)
        lignes.append({"bloc": "mesureB_pool120", "serie": etiquette, "n": r["n"],
                       "top1": r["top1"], "top1_bas": r["top1_bas"],
                       "top1_haut": r["top1_haut"], "top10": r["top10"],
                       "top1_segment": r["top1_segment"], "hasard": r["hasard"]})

    print("\n=== 5. BASELINE APPLICABLE, recalculee sur CE pool de 120 ===", flush=True)
    if DEMO in twin:
        r = attaque_vers_humain(twin[DEMO], humain, "baseline|demo")
        print(f"{'Demographics Only -> humains v4 (pool 120)':52s} "
              f"top1 {r['top1']*100:6.2f} % [{r['top1_bas']*100:5.2f} ; "
              f"{r['top1_haut']*100:5.2f}]", flush=True)
        lignes.append({"bloc": "baseline", "serie": "Demographics Only -> humains v4, pool 120",
                       "n": r["n"], "top1": r["top1"], "top1_bas": r["top1_bas"],
                       "top1_haut": r["top1_haut"], "hasard": r["hasard"]})
        # la baseline homogene a une comparaison jumeau<->jumeau : DEMO contre un jumeau
        for cible in ("Text Persona - GPT4.1-mini", "JSON Persona - GPT4.1"):
            if cible in twin:
                r2 = attaque_sym(twin[DEMO], twin[cible], seg, f"demo<->{cible}")
                if r2:
                    print(f"{'Demographics Only <-> ' + cible:52s} "
                          f"top1 {r2['top1']*100:6.2f} %", flush=True)
                    lignes.append({"bloc": "baseline", "serie": f"Demographics Only <-> {cible}, pool 120",
                                   "n": r2["n"], "top1": r2["top1"],
                                   "top1_bas": r2["top1_bas"], "top1_haut": r2["top1_haut"],
                                   "hasard": r2["hasard"]})

    print("\n=== 6. DECOMPOSITION DE L'ACCORD (plancher / segment / individu), "
          "pool 120 ===", flush=True)
    paires_dec = [("B<->C", notres["B"], notres["C"]),
                  ("B<->M", notres["B"], notres["M"]),
                  ("B<->G", notres["B"], notres["G"]),
                  ("B<->P", notres["B"], notres["P"])]
    for etiquette, cx, cy in PALIERS_TWIN:
        if cx in twin and cy in twin:
            paires_dec.append((etiquette, twin[cx], twin[cy]))
    for nom, X, Y in paires_dec:
        d = decomposer_accord(X, Y, seg)
        if d is None:
            continue
        print(f"{nom:52s} vrai {d['accord_vrai']*100:5.1f} %  "
              f"meme segment {d['accord_meme_segment']*100:5.1f} %  "
              f"inconnu {d['accord_inconnu']*100:5.1f} %  -> apport individuel "
              f"{d['apport_individuel_pts']:+5.1f} pts", flush=True)
        lignes.append({"bloc": "decomposition_accord", "serie": nom,
                       "accord_vrai": d["accord_vrai"],
                       "accord_meme_segment": d["accord_meme_segment"],
                       "accord_inconnu": d["accord_inconnu"],
                       "apport_individuel_pts": d["apport_individuel_pts"]})

    df = pd.DataFrame(lignes)
    chemin = os.path.join(SORTIE, "c7-reconciliation-facteurs.csv")
    df.to_csv(chemin, index=False)
    print(f"\necrit {chemin} ({len(df)} lignes)", flush=True)


if __name__ == "__main__":
    main()
