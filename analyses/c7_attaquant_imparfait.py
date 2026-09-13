"""
c7_attaquant_imparfait : que devient la reidentification quand l'attaquant n'a plus
les vraies reponses exactes ?

===========================================================================
PREENREGISTREMENT : resultats/c7-attaquant-imparfait-preenregistrement.md, ecrit le
13 septembre 2026, AVANT ce fichier et avant tout calcul, et commite seul.

LA QUESTION. L'attaque de c7_reidentification suppose que l'attaquant detient les vraies
reponses exactes des 2 058 candidats. Un attaquant reel a une base clients partielle,
perimee, mal saisie. Ce module degrade les donnees AUXILIAIRES de l'attaquant -- le pool
des humains vague 4 contre lequel la sortie de jumeau est appariee -- une dimension a la
fois, et mesure le taux a chaque niveau. La sortie de jumeau publiee, elle, n'est jamais
degradee : elle est publique par hypothese.

LE PIEGE DU BASSIN, deja paye deux fois dans ce projet. Le top-1 depend mecaniquement de
la taille du bassin (2,13 % a 2 058 personnes, 9,20 % a 200, 13,29 % a 120 pour la seule
baseline demographique). Ici le bassin est RIGOUREUSEMENT CONSTANT entre toutes les
conditions : memes personnes attaquees, meme pool de candidats, memes 60 items de depart.
Seule la QUALITE de l'information de l'attaquant varie. Et la baseline demographique est
recalculee dans CHAQUE condition, sur le pool EXACTEMENT AUSSI DEGRADE, avec les memes
masques et le meme bruit (memes graines) : comparer un top-1 degrade a une baseline non
degradee serait le meme piege sous un autre nom.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Ce script ne calcule,
n'imprime et n'ecrit JAMAIS l'identite ou le pid d'une personne retrouvee, ni aucune liste
d'appariements individuels. Seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                        les quinze tables de Twin
  t1_commun.ecrire                         l'ecriture d'un csv dans resultats/
  c7_reidentification.items_communs        les 60 items toujours renseignes
  c7_reidentification.rangs_attaque        l'attaque de reidentification elle-meme
  c7_reidentification.graine_nom           la graine stable par nom
  c7_reidentification.REF_V4 / DEMO        les constantes de reference
  c7_reidentification.N_BOOTSTRAP          2 000 tirages
  a2_commun.bootstrap_personnes            l'IC 95 % par reechantillonnage de personnes
  c7_controle_interpretabilite.controle_avant_interpretation
                                           le controle de fidelite prealable, applique a
                                           la condition NON degradee avant toute
                                           interpretation

CE QUI EST NOUVEAU ICI, et rien d'autre : les quatre degradations des donnees auxiliaires
(items partiels, reponses fausses, les deux combines, items les plus banals seulement) et
la recherche du point de rupture par rapport a la baseline du meme bassin.

REDUCTION DECLAREE AU PREENREGISTREMENT (section 9) : le nombre de tirages de departage des
ex aequo passe de 20 (c7_reidentification) a 5. Il ne sert qu'a casser les egalites de rang,
son effet sur un taux agrege est du troisieme ordre. Le bootstrap reste a 2 000, les
repetitions a 3.

Aucun appel de modele de langage, aucun reseau, aucune depense. Lecture seule sur data/.
Aucun script existant n'est modifie.

Usage (chaque volet tient en avant-plan) :
  .venv/bin/python analyses/c7_attaquant_imparfait.py --volet ref --cache <dir>
  .venv/bin/python analyses/c7_attaquant_imparfait.py --volet d1  --cache <dir>
  .venv/bin/python analyses/c7_attaquant_imparfait.py --volet d2  --cache <dir>
  .venv/bin/python analyses/c7_attaquant_imparfait.py --volet d3  --cache <dir>
  .venv/bin/python analyses/c7_attaquant_imparfait.py --volet d4  --cache <dir>
  .venv/bin/python analyses/c7_attaquant_imparfait.py --volet synthese --cache <dir>
===========================================================================
"""

import argparse
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from a2_commun import bootstrap_personnes                                # noqa: E402
from c7_reidentification import (                                        # noqa: E402
    DEMO, N_BOOTSTRAP, REF_V4, graine_nom, items_communs, rangs_attaque,
)
from c7_controle_interpretabilite import (                               # noqa: E402
    EchecControleInterpretabilite, controle_avant_interpretation,
)

GRAINE = 20260913
N_TIRAGES_LIENS = 5          # reduction declaree (preenregistrement section 9)
N_REPETITIONS = 3

CANDIDAT = "JSON Persona - GPT4.1"     # le plus fort de c7-resultats.md (top-1 20,68 %)

PARTS_ITEMS = [1.00, 0.75, 0.50, 0.25, 0.10]
TAUX_BRUIT = [0.00, 0.05, 0.10, 0.20, 0.30]
GRILLE_COMBINEE = [(p, q) for p in (0.75, 0.50, 0.25) for q in (0.10, 0.20, 0.30)]

SORTIE_CSV = "c7-attaquant-imparfait.csv"


# ---------------------------------------------------------------------------
# 1. Les degradations des donnees auxiliaires de l'attaquant
# ---------------------------------------------------------------------------

def masque_partiel(n_personnes, n_items, k, rng):
    """Masque booleen (n_personnes, n_items) avec EXACTEMENT k items connus par personne.

    Tirage independant par candidat -- une base clients n'a pas les memes champs pour tout
    le monde -- mais le MEME NOMBRE d'items pour tous. C'est le garde-fou preenregistre :
    le denominateur de la distance de Hamming est le nombre d'items renseignes des deux
    cotes, donc un masque de taille variable donnerait aux candidats a peu d'items un
    accord artificiellement eleve, et fabriquerait un effet qui n'est pas celui qu'on
    mesure. k constant elimine ce canal par construction.
    """
    if k >= n_items:
        return np.ones((n_personnes, n_items), dtype=bool)
    ordre = rng.random((n_personnes, n_items)).argsort(axis=1)
    m = np.zeros((n_personnes, n_items), dtype=bool)
    np.put_along_axis(m, ordre[:, :k], True, axis=1)
    return m


def marginales_par_item(pool):
    """Pour chaque item : les modalites observees et leurs effectifs chez les humains.

    Sert a tirer une reponse FAUSSE mais PLAUSIBLE : une donnee perimee ou mal saisie
    ressemble a une reponse que quelqu'un aurait pu donner, pas a du bruit uniforme.
    """
    tables = []
    for j in range(pool.shape[1]):
        col = pool[:, j]
        vals, cnt = np.unique(col[col >= 0], return_counts=True)
        tables.append((vals, cnt.astype(float)))
    return tables


def bruiter(pool, taux, tables, rng, connu=None):
    """Remplace une fraction `taux` des cellules CONNUES par une autre modalite.

    La valeur fausse est tiree dans la marginale empirique de l'item CONDITIONNEE A ETRE
    DIFFERENTE de la vraie. Seules les cellules connues (connu=True) peuvent etre fausses :
    on ne bruite pas une information que l'attaquant n'a pas. Le taux porte donc bien sur
    les reponses connues, comme le preenregistrement l'ecrit.
    """
    if taux <= 0:
        return pool.copy()
    out = pool.copy()
    dispo = (pool >= 0) if connu is None else ((pool >= 0) & connu)
    tire = rng.random(pool.shape) < taux
    a_corrompre = dispo & tire
    for j in range(pool.shape[1]):
        lignes = np.flatnonzero(a_corrompre[:, j])
        if len(lignes) == 0:
            continue
        vals, cnt = tables[j]
        if len(vals) < 2:
            continue                      # item constant : aucune autre modalite possible
        vraies = pool[lignes, j]
        for t in np.unique(vraies):
            sel = lignes[vraies == t]
            poids = cnt.copy()
            poids[vals == t] = 0.0
            s = poids.sum()
            if s <= 0:
                continue
            out[sel, j] = rng.choice(vals, size=len(sel), p=poids / s)
    return out


def entropies_items(pool):
    """Entropie de Shannon (bits) de la distribution des reponses humaines, par item.

    Sert a definir les items "les plus courants", ceux qu'on trouve dans n'importe quelle
    base commerciale : distribution la plus concentree = reponse la plus previsible =
    information la plus faible. Operationnalisation preenregistree du volet D4.
    """
    h = np.zeros(pool.shape[1])
    for j in range(pool.shape[1]):
        col = pool[:, j]
        _, cnt = np.unique(col[col >= 0], return_counts=True)
        p = cnt / cnt.sum()
        h[j] = float(-(p * np.log2(p)).sum())
    return h


def degrader(pool, part_items, taux_bruit, tables, rng, items_forces=None):
    """Le pool des donnees auxiliaires, degrade une fois.

    part_items : fraction des 60 items connue de l'attaquant (masque aleatoire par
        personne, k constant), ignoree si items_forces est fourni.
    items_forces : indices de colonnes que l'attaquant connait POUR TOUT LE MONDE
        (volet D4, items les plus banals) -- deterministe, aucun tirage.
    taux_bruit : fraction des reponses CONNUES qui est fausse.
    """
    n, p = pool.shape
    if items_forces is not None:
        connu = np.zeros((n, p), dtype=bool)
        connu[:, items_forces] = True
    else:
        connu = masque_partiel(n, p, int(round(part_items * p)), rng)
    deg = np.where(connu, pool, -1)
    return bruiter(deg, taux_bruit, tables, rng, connu=connu)


# ---------------------------------------------------------------------------
# 2. L'attaque, et la comparaison a la baseline du MEME bassin et de la MEME degradation
# ---------------------------------------------------------------------------

def attaquer(X, pool_deg, etiquette):
    """top-1 et top-10 de X contre pool_deg, IC bootstrap sur les personnes.

    X et pool_deg ont le meme nombre de lignes et la ligne i de X est le jumeau de la
    ligne i du pool : le bassin est le meme objet pour tout le monde, il n'y a pas de
    parametre permettant de le changer d'une condition a l'autre.
    """
    n = X.shape[0]
    rng = np.random.default_rng([GRAINE, graine_nom(etiquette)])
    _, top1, top10 = rangs_attaque(X, pool_deg, np.arange(n), rng,
                                   n_tirages=N_TIRAGES_LIENS)
    m1, b1, h1 = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP,
                                     graine=[GRAINE, graine_nom(etiquette), 1])
    m10, _, _ = bootstrap_personnes(top10, n_tirages=N_BOOTSTRAP,
                                    graine=[GRAINE, graine_nom(etiquette), 2])
    return {"top1": m1, "top1_bas": b1, "top1_haut": h1, "top10": m10,
            "hasard": 1.0 / n}


def frequences_modales(pool):
    """Frequence de la reponse MODALE, par item : la mesure directe de la banalite.

    AJOUT POST HOC, declare comme tel (voir resultats/c7-attaquant-imparfait-resultats.md
    section D4). Le preenregistrement operationnalisait "les items les plus courants" par
    l'entropie la plus basse ; le calcul a montre que sur Twin l'entropie classe surtout les
    items par NOMBRE DE MODALITES (un item binaire equilibre vaut 1,0 bit, un item a cinq
    modalites vaut jusqu'a 2,3 bits) et non par banalite de la reponse. La frequence modale
    mesure ce que le preenregistrement voulait dire : une reponse que presque tout le monde
    donne. Le volet preenregistre est rapporte tel quel ; celui-ci le complete, il ne le
    remplace pas.
    """
    f = np.zeros(pool.shape[1])
    for j in range(pool.shape[1]):
        col = pool[:, j]
        _, cnt = np.unique(col[col >= 0], return_counts=True)
        f[j] = float(cnt.max() / cnt.sum())
    return f


def n_modalites(pool):
    """Nombre de modalites observees par item, pour documenter le confondant ci-dessus."""
    return np.array([len(np.unique(pool[:, j][pool[:, j] >= 0]))
                     for j in range(pool.shape[1])])


def condition(X_cand, X_demo, pool, volet, part_items, taux_bruit, tables, items_forces,
              repetitions, etiquette_items=None):
    """Une condition de degradation : candidat et baseline sur le MEME pool degrade.

    Le point cle : le masque et le bruit sont tires UNE FOIS par repetition, et le MEME
    pool degrade sert au candidat et a la baseline demographique. La baseline n'est jamais
    une constante importee d'ailleurs, et elle subit exactement la meme perte d'information
    que le candidat.
    """
    lignes = []
    for r in range(repetitions):
        etiq = f"{volet}|p{part_items:.2f}|q{taux_bruit:.2f}|r{r}"
        rng = np.random.default_rng([GRAINE, graine_nom(etiq), 11])
        pool_deg = degrader(pool, part_items, taux_bruit, tables, rng,
                            items_forces=items_forces)
        k_connus = float(np.mean((pool_deg >= 0).sum(axis=1)))
        c = attaquer(X_cand, pool_deg, "cand|" + etiq)
        b = attaquer(X_demo, pool_deg, "base|" + etiq)
        lignes.append({
            "volet": volet, "part_items": part_items, "taux_bruit": taux_bruit,
            "items_forces": etiquette_items if items_forces is not None else "aleatoire",
            "repetition": r, "n_bassin": X_cand.shape[0],
            "items_connus_moyens": k_connus,
            "cand_top1": c["top1"], "cand_top1_bas": c["top1_bas"],
            "cand_top1_haut": c["top1_haut"], "cand_top10": c["top10"],
            "base_top1": b["top1"], "base_top1_bas": b["top1_bas"],
            "base_top1_haut": b["top1_haut"], "base_top10": b["top10"],
            "hasard": c["hasard"],
            "au_dessus_baseline": bool(c["top1_bas"] > b["top1_haut"]),
        })
        print(f"    r{r} : items connus {k_connus:.1f}/60 | candidat "
              f"{c['top1']*100:6.2f} % [{c['top1_bas']*100:.2f};{c['top1_haut']*100:.2f}] "
              f"| baseline {b['top1']*100:5.2f} % "
              f"[{b['top1_bas']*100:.2f};{b['top1_haut']*100:.2f}] | au-dessus = "
              f"{lignes[-1]['au_dessus_baseline']}", flush=True)
    return lignes


# ---------------------------------------------------------------------------
# 3. Chargement, bassin constant, et controle prealable
# ---------------------------------------------------------------------------

def preparer():
    """Le bassin, les items, les trois matrices. Appele identiquement par tous les volets,
    donc rigoureusement le meme bassin d'un volet a l'autre."""
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, "humains vagues 1-3 (retest)"])
    couv_c = (codes[CANDIDAT] >= 0).any(axis=1)
    couv_d = (codes[DEMO] >= 0).any(axis=1)
    couv_h = (codes[REF_V4][:, items] >= 0).all(axis=1)
    bassin = np.flatnonzero(couv_c & couv_d & couv_h)
    pool = codes[REF_V4][bassin][:, items]
    X_cand = codes[CANDIDAT][bassin][:, items]
    X_demo = codes[DEMO][bassin][:, items]
    return paq, bassin, items, pool, X_cand, X_demo


def chemin_cache(cache, volet):
    return os.path.join(cache, f"c7-attaquant-imparfait-{volet}.csv")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volet", required=True,
                    choices=["ref", "d1", "d2", "d3", "d4", "d4b", "d1b", "synthese"])
    ap.add_argument("--cache", required=True,
                    help="repertoire hors depot pour les csv partiels par volet")
    args = ap.parse_args()
    os.makedirs(args.cache, exist_ok=True)
    t0 = time.time()

    if args.volet == "synthese":
        return synthese(args.cache)

    print(__doc__.split("=" * 75)[1], flush=True)
    paq, bassin, items, pool, X_cand, X_demo = preparer()
    print(f"bassin constant : {len(bassin)} personnes, {len(items)} items, "
          f"candidat = {CANDIDAT}", flush=True)
    tables = marginales_par_item(pool)

    lignes = []

    if args.volet == "ref":
        # --- controle de fidelite prealable, sur la condition NON degradee ---
        print("\n=== controle prealable (c7_controle_interpretabilite), condition non "
              "degradee ===", flush=True)
        try:
            d = controle_avant_interpretation(bassin, items, X_cand, CANDIDAT, paq=paq)
            print(f"  PASSE : top-1 {d['candidat_top1']*100:.2f} % "
                  f"[{d['candidat_ic'][0]*100:.2f};{d['candidat_ic'][1]*100:.2f}] vs "
                  f"baseline {d['baseline_top1']*100:.2f} % "
                  f"[{d['baseline_ic'][0]*100:.2f};{d['baseline_ic'][1]*100:.2f}] "
                  f"sur {d['bassin']} personnes", flush=True)
            controle = "PASSE"
        except EchecControleInterpretabilite as exc:
            print("  ECHEC : rien ne sera interprete.\n" + str(exc), flush=True)
            controle = "ECHEC"
        pd.DataFrame([{"controle_prealable": controle}]).to_csv(
            chemin_cache(args.cache, "controle"), index=False)
        if controle != "PASSE":
            raise SystemExit("controle prealable en echec : aucun volet de degradation "
                             "ne doit etre interprete.")

        print("\n=== reference : donnees auxiliaires parfaites ===", flush=True)
        lignes += condition(X_cand, X_demo, pool, "reference", 1.00, 0.00, tables,
                            None, 1)

    elif args.volet == "d1":
        print("\n=== D1 : reponses partielles (tirage aleatoire) ===", flush=True)
        for p in PARTS_ITEMS[1:]:
            print(f"  part_items = {p:.0%}", flush=True)
            lignes += condition(X_cand, X_demo, pool, "D1_partiel", p, 0.00, tables,
                                None, N_REPETITIONS)

    elif args.volet == "d2":
        print("\n=== D2 : reponses bruitees (tous les items connus) ===", flush=True)
        for q in TAUX_BRUIT[1:]:
            print(f"  taux_bruit = {q:.0%}", flush=True)
            lignes += condition(X_cand, X_demo, pool, "D2_bruit", 1.00, q, tables,
                                None, N_REPETITIONS)

    elif args.volet == "d3":
        print("\n=== D3 : partiel ET bruite ===", flush=True)
        for p, q in GRILLE_COMBINEE:
            print(f"  part_items = {p:.0%}, taux_bruit = {q:.0%}", flush=True)
            lignes += condition(X_cand, X_demo, pool, "D3_combine", p, q, tables,
                                None, N_REPETITIONS)

    elif args.volet == "d4":
        h = entropies_items(pool)
        ordre = np.argsort(h)             # entropie croissante = items les plus banals
        print("\n=== D4 : seulement les items les plus courants (entropie la plus "
              "basse) ===", flush=True)
        print(f"  entropie des 60 items : min {h.min():.3f} bits, mediane "
              f"{np.median(h):.3f}, max {h.max():.3f}", flush=True)
        for p in PARTS_ITEMS[1:]:
            k = int(round(p * pool.shape[1]))
            forces = np.sort(ordre[:k])
            print(f"  k = {k} items banals (entropie moyenne "
                  f"{h[forces].mean():.3f} bits contre {h.mean():.3f} sur les 60)",
                  flush=True)
            lignes += condition(X_cand, X_demo, pool, "D4_items_banals", p, 0.00, tables,
                                forces, 1, etiquette_items="entropie_basse")

    elif args.volet == "d1b":
        # --- controle POST HOC, declare : items ALEATOIRES mais IDENTIQUES pour tous ---
        # D1 tire un masque different par candidat, D4/D4b imposent les memes items a tous.
        # Les deux differences sont confondues : "quels items" et "les memes pour tous".
        # Ce volet isole la seconde -- items tires au hasard, mais communs a tout le pool.
        # Sans lui, l'ecart D4 - D1 ne serait pas interpretable.
        print("\n=== D1b (POST HOC, controle) : items aleatoires IDENTIQUES pour tous "
              "===", flush=True)
        for p in PARTS_ITEMS[1:]:
            k = int(round(p * pool.shape[1]))
            print(f"  k = {k} items aleatoires communs", flush=True)
            for r in range(N_REPETITIONS):
                rng_i = np.random.default_rng([GRAINE, graine_nom(f"d1b|{k}|{r}"), 77])
                forces = np.sort(rng_i.choice(pool.shape[1], size=k, replace=False))
                lignes += condition(X_cand, X_demo, pool, "D1b_items_communs", p, 0.00,
                                    tables, forces, 1,
                                    etiquette_items="aleatoire_commun")

    elif args.volet == "d4b":
        # --- variante POST HOC, declaree : la banalite mesuree par la frequence modale ---
        f = frequences_modales(pool)
        nm = n_modalites(pool)
        h = entropies_items(pool)
        ordre = np.argsort(-f)            # frequence modale decroissante = plus banal
        print("\n=== D4b (POST HOC) : items les plus banals au sens de la frequence "
              "modale ===", flush=True)
        print(f"  frequence modale : min {f.min():.3f}, mediane {np.median(f):.3f}, "
              f"max {f.max():.3f}", flush=True)
        print(f"  nombre de modalites : min {nm.min()}, mediane {int(np.median(nm))}, "
              f"max {nm.max()}", flush=True)
        print(f"  correlation entropie / nombre de modalites : "
              f"{np.corrcoef(h, nm)[0, 1]:.3f} ; entropie / frequence modale : "
              f"{np.corrcoef(h, f)[0, 1]:.3f}", flush=True)
        for p in PARTS_ITEMS[1:]:
            k = int(round(p * pool.shape[1]))
            forces = np.sort(ordre[:k])
            print(f"  k = {k} items les plus banals (frequence modale moyenne "
                  f"{f[forces].mean():.3f} contre {f.mean():.3f} sur les 60)", flush=True)
            lignes += condition(X_cand, X_demo, pool, "D4b_frequence_modale", p, 0.00,
                                tables, forces, 1, etiquette_items="frequence_modale")

    df = pd.DataFrame(lignes)
    df.to_csv(chemin_cache(args.cache, args.volet), index=False)
    print(f"\n{args.volet} : {len(df)} lignes, {time.time() - t0:.0f} s", flush=True)


# ---------------------------------------------------------------------------
# 4. Synthese : agregation des repetitions et recherche du point de rupture
# ---------------------------------------------------------------------------

def agreger(df):
    """Une ligne par condition : moyenne des repetitions pour le taux, IC bootstrap de la
    repetition MEDIANE (regle preenregistree, section 4)."""
    cles = ["volet", "part_items", "taux_bruit", "items_forces"]
    sorties = []
    for cle, g in df.groupby(cles, sort=False):
        g = g.sort_values("cand_top1")
        med = g.iloc[len(g) // 2]
        sorties.append({
            "volet": cle[0], "part_items": cle[1], "taux_bruit": cle[2],
            "items": cle[3], "n_repetitions": len(g), "n_bassin": int(med.n_bassin),
            "items_connus_moyens": float(g.items_connus_moyens.mean()),
            "cand_top1": float(g.cand_top1.mean()),
            "cand_top1_bas": float(med.cand_top1_bas),
            "cand_top1_haut": float(med.cand_top1_haut),
            "cand_top10": float(g.cand_top10.mean()),
            "base_top1": float(g.base_top1.mean()),
            "base_top1_bas": float(med.base_top1_bas),
            "base_top1_haut": float(med.base_top1_haut),
            "hasard": float(med.hasard),
            "ratio_cand_base": float(g.cand_top1.mean() / g.base_top1.mean())
            if g.base_top1.mean() > 0 else np.nan,
            "au_dessus_baseline": bool(med.cand_top1_bas > med.base_top1_haut),
            "au_dessus_toutes_repetitions": bool(g.au_dessus_baseline.all()),
        })
    return pd.DataFrame(sorties)


def synthese(cache):
    parts = []
    for v in ("ref", "d1", "d1b", "d2", "d3", "d4", "d4b"):
        c = chemin_cache(cache, v)
        if os.path.exists(c):
            parts.append(pd.read_csv(c))
        else:
            print(f"volet manquant : {v}", flush=True)
    df = pd.concat(parts, ignore_index=True)
    agg = agreger(df)
    T1.ecrire(agg, SORTIE_CSV)

    pd.set_option("display.width", 200)
    print("\n=== toutes les conditions ===", flush=True)
    for _, r in agg.iterrows():
        print(f"{r.volet:16s} items={r.part_items:.2f} bruit={r.taux_bruit:.2f} "
              f"({r['items']:14s}) candidat={r.cand_top1*100:6.2f} % "
              f"[{r.cand_top1_bas*100:5.2f};{r.cand_top1_haut*100:5.2f}] "
              f"baseline={r.base_top1*100:5.2f} % "
              f"[{r.base_top1_bas*100:5.2f};{r.base_top1_haut*100:5.2f}] "
              f"ratio={r.ratio_cand_base:5.2f} au-dessus={r.au_dessus_baseline}",
              flush=True)

    # --- point de rupture, du moins degrade au plus degrade, regle preenregistree ---
    print("\n=== point de rupture (premiere condition ou l'IC candidat n'est plus "
          "strictement au-dessus de l'IC baseline) ===", flush=True)
    for volet, tri in (("D1_partiel", ["part_items"]),
                       ("D2_bruit", ["taux_bruit"]),
                       ("D4_items_banals", ["part_items"]),
                       ("D4b_frequence_modale", ["part_items"]),
                       ("D1b_items_communs", ["part_items"])):
        sous = agg[agg.volet == volet]
        if not len(sous):
            continue
        asc = (volet == "D2_bruit")
        sous = sous.sort_values(tri, ascending=asc)
        casse = sous[~sous.au_dessus_baseline]
        if len(casse):
            r = casse.iloc[0]
            print(f"  {volet:16s} rupture a items={r.part_items:.2f} "
                  f"bruit={r.taux_bruit:.2f} (candidat {r.cand_top1*100:.2f} %, "
                  f"baseline {r.base_top1*100:.2f} %)", flush=True)
        else:
            print(f"  {volet:16s} AUCUNE rupture dans la plage testee", flush=True)

    sous = agg[agg.volet == "D3_combine"].sort_values(["part_items", "taux_bruit"],
                                                      ascending=[False, True])
    casse = sous[~sous.au_dessus_baseline]
    if len(casse):
        r = casse.iloc[0]
        print(f"  D3_combine       rupture a items={r.part_items:.2f} "
              f"bruit={r.taux_bruit:.2f}", flush=True)
    else:
        print("  D3_combine       AUCUNE rupture dans la plage testee", flush=True)

    ref = agg[agg.volet == "reference"]
    if len(ref):
        r0 = float(ref.cand_top1.iloc[0])
        print(f"\nreference non degradee : candidat {r0*100:.2f} %, baseline "
              f"{float(ref.base_top1.iloc[0])*100:.2f} %, hasard "
              f"{float(ref.hasard.iloc[0])*100:.4f} %", flush=True)
        for _, r in agg[agg.volet != "reference"].iterrows():
            print(f"  {r.volet:16s} items={r.part_items:.2f} bruit={r.taux_bruit:.2f} : "
                  f"{r.cand_top1 / r0 * 100:5.1f} % du taux non degrade", flush=True)


if __name__ == "__main__":
    main()
