"""
r1_evaluer : les mesures et les tests de l'oracle des camps, sur les traces de r1.

Statut : script d'analyse jetable. Aucun appel de modele de langage : il lit les traces
JSONL ecrites par r1_oracle_camps.py et le referent humain, et rien d'autre. Aucun script
existant n'est modifie ; a2_baselines_gss, a5_agents_locaux_gss, a28_commun et a30_commun
sont importes tels quels.

Tolerant au partiel. Un run interrompu, un modele absent, une cellule rejetee : tout se lit
et le perimetre effectif est ecrit dans chaque tableau. Une cellule rejetee au parse n'est
jamais remplacee par une valeur par defaut, elle est retiree et comptee.

Ce qu'il calcule, dans les definitions figees par resultats/r1-preenregistrement.md :
  H1  unanimite   : Gini Simpson decrit contre reel, par camp et par item.
  H2a ecart       : distance de variation totale entre camps, decrite contre reelle.
  H2b ecart signe : position moyenne orientee, facteur d'amplification a la maniere de a38.
  H3  demandeur   : distance entre le portrait fait au journaliste et celui fait a
                    l'adversaire, contre le plancher de reinterrogation humaine.
  H4  derive      : correlation de rang avec la derive agregee de a37.
Plus les cinq criteres de chute de la section 7 du preenregistrement.

Entree  : data/traces/r1-*.jsonl, data/traces/r1-distributions-reelles.csv
          resultats/a37-orientation-items.csv, resultats/a37-gss-par-item.csv
Sortie  : resultats/r1-par-cellule.csv, r1-par-item-ecarts.csv, r1-identite.csv,
          r1-h1-unanimite.csv, r1-h2-ecart.csv, r1-h3-identite.csv, r1-h4-derive.csv,
          r1-controles.csv, r1-resume.md
          resultats/r1-figure-oracle.png et .svg

Usage :
  .venv/bin/python analyses/r1_evaluer.py
  .venv/bin/python analyses/r1_evaluer.py --suffixe smoke --sans-figure
"""

import argparse
import glob
import json
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

from a28_commun import holm
from r1_oracle_camps import (CAMPS, IDENTITES, MODELES, TRACES,
                            repartition_exemple)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260908
N_BOOT = 2000        # tirages de bootstrap, unite de reechantillonnage : l'item
N_PERM = 20000       # permutations de signe appariees par item
BANDE_NULLE = (0.95, 1.05)   # seuil de materialite du preenregistrement, section 6


# ---------------------------------------------------------------------------
# 1. Lecture
# ---------------------------------------------------------------------------

def lire_traces(suffixe):
    """Toutes les lignes de trace, tolerant aux fichiers partiels et aux lignes tronquees."""
    motif = os.path.join(TRACES, f"r1-*{'-' + suffixe if suffixe else ''}.jsonl")
    lignes = []
    for chemin in sorted(glob.glob(motif)):
        if not suffixe and "-smoke" in os.path.basename(chemin):
            continue
        with open(chemin, encoding="utf-8") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    lignes.append(json.loads(ligne))
                except json.JSONDecodeError:
                    continue   # derniere ligne d'un fichier interrompu en cours d'ecriture
    return lignes


def lire_referent(suffixe=""):
    """Distributions humaines par item, camp et vague, en vecteurs alignes sur les rangs."""
    chemin = os.path.join(TRACES, f"r1-distributions-reelles"
                                  f"{'-' + suffixe if suffixe else ''}.csv")
    if not os.path.exists(chemin):
        chemin = os.path.join(TRACES, "r1-distributions-reelles.csv")
    if not os.path.exists(chemin):
        sys.exit(f"referent humain absent : {chemin}. Lancer d'abord r1_oracle_camps.py")
    # keep_default_na=False : deux items du GSS ont une modalite qui s'ecrit litteralement
    # « None », `relig16*` et `granborn`. Lue avec les conventions par defaut de pandas,
    # cette modalite revient en NaN et ne correspond plus a la cle du dictionnaire de
    # distribution ecrit par le run. Le bug est un aller retour CSV, pas un defaut du run.
    d = pd.read_csv(chemin, keep_default_na=False, na_values=[""])
    for colonne in ("rang", "n", "effectif", "p"):
        d[colonne] = pd.to_numeric(d[colonne], errors="coerce")
    ref, options, effectifs = {}, {}, {}
    for (item, camp, vague), g in d.groupby(["item", "camp", "vague"], sort=False):
        g = g.sort_values("rang")
        ref[(item, camp, vague)] = g["p"].to_numpy(dtype=float)
        options[item] = list(g["modalite"])
        effectifs[(item, camp, vague)] = int(g["n"].iloc[0])
    return ref, options, effectifs


def lire_a37():
    """Orientation gauche droite et derive agregee des 149 items, lues telles quelles."""
    o = pd.read_csv(os.path.join(SORTIE, "a37-orientation-items.csv"))
    d = pd.read_csv(os.path.join(SORTIE, "a37-gss-par-item.csv"))
    sens = dict(zip(o["item"], o["sens_codeur_A"]))
    oriente = dict(zip(o["item"], o["oriente"].astype(bool)))
    strict = dict(zip(d["item"], d["retenu_strict"].astype(bool)))
    derive = dict(zip(d["item"], d["derive_agregee"]))
    return sens, oriente, strict, derive


# ---------------------------------------------------------------------------
# 2. Mesures elementaires
# ---------------------------------------------------------------------------

def gini_simpson(p):
    """1 - somme p^2, par substitution. Meme quantite des deux cotes de la comparaison.

    L'estimateur sans biais de a30 n'est pas employe ici pour la comparaison principale :
    il demande un effectif, et une distribution decrite par un modele n'en a pas. On
    compare donc deux estimateurs par substitution, et le controle sans biais du cote
    humain est rapporte a part dans r1-controles.csv.
    """
    p = np.asarray(p, dtype=float)
    return float(1.0 - np.sum(p * p))


def recopie_exemple(distribution):
    """Vrai si la distribution est, au chiffre pres, l'exemple factice de l'invite de relance.

    Critere de chute 2 du preenregistrement. L'exemple est recalcule par la fonction meme
    qui l'a produit dans le run, `repartition_exemple`, pour qu'aucune divergence ne puisse
    s'installer entre ce qui a ete montre au modele et ce qu'on cherche ici.

    Ce n'est pas une precaution theorique. Sur les premieres cellules relancees du run
    reel, trois sur quatre recopient l'exemple chiffre a la virgule pres, sur les items a
    beaucoup de modalites, `income` a douze et `attend` a neuf. Une cellule qui recopie
    l'exemple ne mesure pas ce que le modele croit d'un camp, elle mesure ce que nous lui
    avons montre. Elle sort des mesures, et le taux est publie.
    """
    p = np.array(list(distribution.values()), dtype=float)
    k = len(p)
    if k < 2:
        return False
    ex = np.array(repartition_exemple(k), dtype=float)
    ex = ex / ex.sum()
    return bool(np.allclose(p, ex, atol=1e-6))


def gini_simpson_sans_biais(p, n):
    """Estimateur sans biais de a30, `somme n_k (n_k - 1) / (N (N - 1))`, ecrit sur (p, N).

    Identite employee : avec p_k = n_k / N, l'estimateur sans biais vaut exactement
    N / (N - 1) fois l'estimateur par substitution. Il ne sert que de controle du cote
    humain : une distribution decrite par un modele n'a pas d'effectif, donc pas de
    version sans biais, et c'est pour cela que la comparaison principale se fait par
    substitution des deux cotes.
    """
    if not n or n < 2:
        return float("nan")
    return float(n / (n - 1.0) * gini_simpson(p))


def tv(p, q):
    """Distance de variation totale, la mesure de arXiv 2607.25292. Bornee dans [0, 1]."""
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    return float(0.5 * np.sum(np.abs(p - q)))


def position(p, sens):
    """Position moyenne sur l'echelle de nomenclature, orientee : haut = position de droite.

    Modalite de rang i sur K notee i / (K - 1), retournee si le sens de l'item est negatif.
    C'est la definition de a37_commun.position, recopiee ici sur un vecteur de probabilites
    au lieu d'une table de contingence.
    """
    p = np.asarray(p, dtype=float)
    k = len(p)
    if k < 2 or not np.isfinite(sens) or sens == 0:
        return float("nan")
    r = np.arange(k, dtype=float) / (k - 1.0)
    s = r if sens > 0 else 1.0 - r
    return float(np.sum(p * s))


# ---------------------------------------------------------------------------
# 3. Statistiques : bootstrap sur les items, permutation de signe appariee
# ---------------------------------------------------------------------------

def ic_ratio_des_moyennes(a, b, rng, n=N_BOOT):
    """Rapport des moyennes de deux series appariees par item, IC bootstrap sur les items.

    L'unite de reechantillonnage est l'item : les valeurs d'un meme item du cote decrit et
    du cote reel ne sont pas independantes, on tire donc les paires ensemble.
    """
    a, b = np.asarray(a, float), np.asarray(b, float)
    m = np.isfinite(a) & np.isfinite(b)
    a, b = a[m], b[m]
    if len(a) < 3 or not np.isfinite(b.mean()) or b.mean() == 0:
        return float("nan"), float("nan"), float("nan"), int(len(a))
    r = float(a.mean() / b.mean())
    idx = rng.integers(0, len(a), size=(n, len(a)))
    tirages = a[idx].mean(axis=1) / b[idx].mean(axis=1)
    tirages = tirages[np.isfinite(tirages)]
    if len(tirages) < 10:
        return r, float("nan"), float("nan"), int(len(a))
    return r, float(np.percentile(tirages, 2.5)), float(np.percentile(tirages, 97.5)), int(len(a))


def p_permutation_signe(d, rng, n=N_PERM):
    """p bilateral d'une difference appariee par item, par permutation de signe.

    Statistique : la moyenne des differences. Sous l'hypothese nulle d'echangeabilite du
    signe item par item, chaque difference peut changer de signe. Estimateur de Phipson et
    Smyth (b + 1) / (m + 1), qui ne rend jamais un p nul.
    """
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    if len(d) < 3:
        return float("nan")
    obs = abs(d.mean())
    signes = rng.choice([-1.0, 1.0], size=(n, len(d)))
    stat = np.abs((signes * d[None, :]).mean(axis=1))
    return float((int((stat >= obs - 1e-15).sum()) + 1.0) / (n + 1.0))


def spearman(u, v):
    u, v = np.asarray(u, float), np.asarray(v, float)
    m = np.isfinite(u) & np.isfinite(v)
    if m.sum() < 5:
        return float("nan")
    ru = pd.Series(u[m]).rank().to_numpy()
    rv = pd.Series(v[m]).rank().to_numpy()
    return float(np.corrcoef(ru, rv)[0, 1])


def p_permutation_correlation(u, v, rng, n=2000):
    """p bilateral d'une correlation de rang, par permutation d'une des deux series."""
    u, v = np.asarray(u, float), np.asarray(v, float)
    m = np.isfinite(u) & np.isfinite(v)
    u, v = u[m], v[m]
    if len(u) < 5:
        return float("nan")
    obs = abs(spearman(u, v))
    compte = 0
    for _ in range(n):
        if abs(spearman(u, rng.permutation(v))) >= obs - 1e-15:
            compte += 1
    return float((compte + 1.0) / (n + 1.0))


def poser_holm(lignes, cle_p="p", cle_sortie="p_holm"):
    """Holm a l'interieur d'une famille de tests, jamais entre familles.

    Les tests indecidables, ceux dont le p n'a pas pu etre calcule faute d'items, sont
    retires de la famille avant la correction et non comptes dans sa taille. Les laisser
    dedans avec un NaN ferait rendre a Holm des p corriges arbitraires, ce qui est
    exactement le genre d'erreur qu'un lecteur ne verrait pas.
    """
    for l in lignes:
        l[cle_sortie] = float("nan")
    index = [i for i, l in enumerate(lignes) if np.isfinite(l[cle_p])]
    if not index:
        return lignes
    corriges = holm(np.array([lignes[i][cle_p] for i in index], dtype=float))
    for i, pc in zip(index, corriges):
        lignes[i][cle_sortie] = float(pc)
    return lignes


def verdict(ratio, bas, haut, p_holm, seuil=0.05):
    """Lecture unique : signification, puis materialite, dans cet ordre."""
    if not np.isfinite(ratio) or not np.isfinite(p_holm):
        return "indecidable"
    if p_holm >= seuil:
        return "non significatif"
    if BANDE_NULLE[0] <= ratio <= BANDE_NULLE[1]:
        return "significatif mais nul en pratique"
    return "amplification" if ratio > 1 else "attenuation"


# ---------------------------------------------------------------------------
# 4. Construction du tableau par cellule
# ---------------------------------------------------------------------------

def par_cellule(traces, ref, options, sens, effectifs):
    """Une ligne par (modele, camp, identite, item) exploitable, plus les rejets."""
    lignes = []
    for t in traces:
        item, camp = t["item"], t["camp"]
        cle1, cle2 = (item, camp, "w1"), (item, camp, "w2")
        if cle1 not in ref:
            continue
        p1, p2 = ref[cle1], ref[cle2]
        n1 = effectifs.get(cle1, 0)
        base = {
            "modele": t["modele"], "cle_modele": t["cle_modele"],
            "camp": camp, "identite": t["identite"], "item": item,
            "famille": t.get("famille"), "n_modalites": t["n_modalites"],
            "rejet": bool(t["rejet"]), "n_tentatives": t.get("n_tentatives"),
            "motif_rejet": t.get("motif_rejet", ""),
        }
        if t["rejet"] or not t.get("distribution"):
            lignes.append(base)
            continue
        if t.get("n_tentatives", 1) > 1 and recopie_exemple(t["distribution"]):
            # Critere de chute 2, applique et non seulement rapporte : la cellule sort.
            base["rejet"] = True
            base["motif_rejet"] = "recopie du gabarit d'exemple de la relance"
            lignes.append(base)
            continue
        pd_ = np.array([t["distribution"][o] for o in options[item]], dtype=float)
        s = sens.get(item, 0)
        base.update({
            "gs_decrit": gini_simpson(pd_),
            "gs_reel_w1": gini_simpson(p1),
            "gs_reel_w1_sans_biais": gini_simpson_sans_biais(p1, n1),
            "gs_reel_w2": gini_simpson(p2),
            "tv_decrit_reel": tv(pd_, p1),
            "tv_plancher_w1_w2": tv(p1, p2),
            "pos_decrit": position(pd_, s),
            "pos_reel_w1": position(p1, s),
            "pos_reel_w2": position(p2, s),
            "p_decrit": json.dumps([round(float(v), 6) for v in pd_]),
        })
        lignes.append(base)
    return pd.DataFrame(lignes)


def par_item_ecarts(cel, ref, sens):
    """Une ligne par (modele, identite, item) : l'ecart entre les camps gauche et droite."""
    ok = cel[~cel["rejet"]].copy()
    lignes = []
    for (modele, cle, identite, item), g in ok.groupby(
            ["modele", "cle_modele", "identite", "item"], sort=False):
        pres = {r["camp"]: json.loads(r["p_decrit"]) for _, r in g.iterrows()}
        if "gauche" not in pres or "droite" not in pres:
            continue
        pg, pdte = np.array(pres["gauche"]), np.array(pres["droite"])
        rg1, rd1 = ref[(item, "gauche", "w1")], ref[(item, "droite", "w1")]
        rg2, rd2 = ref[(item, "gauche", "w2")], ref[(item, "droite", "w2")]
        s = sens.get(item, 0)
        lignes.append({
            "modele": modele, "cle_modele": cle, "identite": identite, "item": item,
            "tv_camps_decrit": tv(pg, pdte),
            "tv_camps_reel_w1": tv(rg1, rd1),
            "tv_camps_reel_w2": tv(rg2, rd2),
            "gap_signe_decrit": position(pdte, s) - position(pg, s),
            "gap_signe_reel_w1": position(rd1, s) - position(rg1, s),
            "gap_signe_reel_w2": position(rd2, s) - position(rg2, s),
        })
    return pd.DataFrame(lignes)


def par_item_identite(cel, ref):
    """Une ligne par (modele, camp, item) : l'effet de l'identite du demandeur."""
    ok = cel[~cel["rejet"]].copy()
    lignes = []
    for (modele, cle, camp, item), g in ok.groupby(
            ["modele", "cle_modele", "camp", "item"], sort=False):
        pres = {r["identite"]: json.loads(r["p_decrit"]) for _, r in g.iterrows()}
        if not set(IDENTITES) <= set(pres):
            continue
        lignes.append({
            "modele": modele, "cle_modele": cle, "camp": camp, "item": item,
            "tv_entre_identites": tv(pres["journaliste"], pres["adversaire"]),
            "tv_plancher_w1_w2": tv(ref[(item, camp, "w1")], ref[(item, camp, "w2")]),
        })
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 5. Les quatre familles de tests
# ---------------------------------------------------------------------------

def test_h1(cel, rng):
    """H1 : la dispersion interne decrite est elle plus faible que la reelle ?"""
    lignes = []
    ok = cel[~cel["rejet"]]
    for (modele, cle), gm in ok.groupby(["modele", "cle_modele"], sort=False):
        for camp in CAMPS:
            for identite in IDENTITES:
                g = gm[(gm["camp"] == camp) & (gm["identite"] == identite)]
                if len(g) < 3:
                    continue
                a, b = g["gs_decrit"].to_numpy(), g["gs_reel_w1"].to_numpy()
                r, bas, haut, n = ic_ratio_des_moyennes(a, b, rng)
                with np.errstate(divide="ignore", invalid="ignore"):
                    dlog = np.log(np.where(a > 0, a, np.nan)) - np.log(np.where(b > 0, b, np.nan))
                p = p_permutation_signe(dlog, rng)
                w2 = g["gs_reel_w2"].to_numpy()
                rp, _, _, _ = ic_ratio_des_moyennes(w2, b, rng)
                lignes.append({
                    "modele": modele, "cle_modele": cle, "camp": camp,
                    "identite": identite, "n_items": n,
                    "gs_decrit_moyen": float(np.nanmean(a)),
                    "gs_reel_moyen": float(np.nanmean(b)),
                    "ratio": r, "ic_bas": bas, "ic_haut": haut,
                    "ratio_plancher_w2_w1": rp,
                    "part_items_sous_1": float(np.mean(a < b)),
                    "p": p,
                })
    return pd.DataFrame(poser_holm(lignes))


def test_h2(ecarts, rng, oriente, strict):
    """H2a, l'ecart non signe ; H2b, l'ecart signe et son facteur d'amplification."""
    lignes_a, lignes_b = [], []
    for (modele, cle, identite), g in ecarts.groupby(
            ["modele", "cle_modele", "identite"], sort=False):
        a, b = g["tv_camps_decrit"].to_numpy(), g["tv_camps_reel_w1"].to_numpy()
        r, bas, haut, n = ic_ratio_des_moyennes(a, b, rng)
        with np.errstate(divide="ignore", invalid="ignore"):
            dlog = np.log(np.where(a > 0, a, np.nan)) - np.log(np.where(b > 0, b, np.nan))
        rp, _, _, _ = ic_ratio_des_moyennes(g["tv_camps_reel_w2"].to_numpy(), b, rng)
        lignes_a.append({
            "modele": modele, "cle_modele": cle, "identite": identite,
            "perimetre": "tous les items", "n_items": n,
            "ecart_decrit_moyen": float(np.nanmean(a)),
            "ecart_reel_moyen": float(np.nanmean(b)),
            "facteur": r, "ic_bas": bas, "ic_haut": haut,
            "facteur_plancher_w2_w1": rp, "p": p_permutation_signe(dlog, rng),
        })
        for nom_per, filtre in (("79 items orientes", oriente),
                                ("items retenus stricts", strict)):
            m = g["item"].map(lambda i: bool(filtre.get(i, False))).to_numpy()
            gg = g[m]
            if len(gg) < 3:
                continue
            a2 = gg["gap_signe_decrit"].to_numpy()
            b2 = gg["gap_signe_reel_w1"].to_numpy()
            r2, bas2, haut2, n2 = ic_ratio_des_moyennes(a2, b2, rng)
            rp2, _, _, _ = ic_ratio_des_moyennes(gg["gap_signe_reel_w2"].to_numpy(), b2, rng)
            lignes_b.append({
                "modele": modele, "cle_modele": cle, "identite": identite,
                "perimetre": nom_per, "n_items": n2,
                "ecart_decrit_moyen": float(np.nanmean(a2)),
                "ecart_reel_moyen": float(np.nanmean(b2)),
                "facteur": r2, "ic_bas": bas2, "ic_haut": haut2,
                "facteur_plancher_w2_w1": rp2,
                "p": p_permutation_signe(a2 - b2, rng),
            })
    lignes_a = poser_holm(lignes_a)
    # Holm par perimetre : les deux perimetres de H2b sont deux familles distinctes.
    sortie_b = []
    for per in {l["perimetre"] for l in lignes_b}:
        sortie_b += poser_holm([l for l in lignes_b if l["perimetre"] == per])
    a = pd.DataFrame(lignes_a)
    a["hypothese"] = "H2a, ecart non signe (TV entre camps)"
    b = pd.DataFrame(sortie_b)
    if len(b):
        b["hypothese"] = "H2b, ecart signe (position orientee)"
    return pd.concat([a, b], ignore_index=True) if len(b) else a


def test_h3(identite_tab, rng):
    """H3 : le portrait d'un camp depend il de l'identite du demandeur ?

    Le test ne porte que sur gauche et droite. Le centre n'a pas de camp adverse unique,
    sa cellule adversaire est fixee arbitrairement : elle est calculee, ecrite, et exclue
    du test, comme le preenregistrement l'annonce.
    """
    lignes = []
    for (modele, cle), gm in identite_tab.groupby(["modele", "cle_modele"], sort=False):
        for camp in ("gauche", "droite"):
            g = gm[gm["camp"] == camp]
            if len(g) < 3:
                continue
            a = g["tv_entre_identites"].to_numpy()
            b = g["tv_plancher_w1_w2"].to_numpy()
            r, bas, haut, n = ic_ratio_des_moyennes(a, b, rng)
            lignes.append({
                "modele": modele, "cle_modele": cle, "camp": camp, "n_items": n,
                "tv_entre_identites_moyenne": float(np.nanmean(a)),
                "plancher_humain_moyen": float(np.nanmean(b)),
                "rapport_au_plancher": r, "ic_bas": bas, "ic_haut": haut,
                "part_items_identiques": float(np.mean(a < 1e-9)),
                "part_items_au_dessus_du_plancher": float(np.mean(a > b)),
                "p": p_permutation_signe(a - b, rng),
            })
    return pd.DataFrame(poser_holm(lignes))


def test_h4(cel, ecarts, derive, rng):
    """H4 : l'effet est il plus fort sur les items a derive agregee marquee ?"""
    lignes = []
    ok = cel[~cel["rejet"]]
    for (modele, cle, identite), g in ok.groupby(
            ["modele", "cle_modele", "identite"], sort=False):
        gg = g.groupby("item", as_index=False).agg(
            gs_decrit=("gs_decrit", "mean"), gs_reel_w1=("gs_reel_w1", "mean"))
        d = gg["item"].map(lambda i: abs(derive.get(i, np.nan))).to_numpy()
        deficit = 1.0 - gg["gs_decrit"].to_numpy() / gg["gs_reel_w1"].to_numpy()
        lignes.append({
            "modele": modele, "cle_modele": cle, "identite": identite,
            "quantite": "deficit d'unanimite 1 - GS decrit / GS reel",
            "n_items": int(np.isfinite(d * deficit).sum()),
            "rho_spearman": spearman(d, deficit),
            "p": p_permutation_correlation(d, deficit, rng),
        })
    for (modele, cle, identite), g in ecarts.groupby(
            ["modele", "cle_modele", "identite"], sort=False):
        d = g["item"].map(lambda i: abs(derive.get(i, np.nan))).to_numpy()
        with np.errstate(divide="ignore", invalid="ignore"):
            amp = np.log(g["tv_camps_decrit"].to_numpy() / g["tv_camps_reel_w1"].to_numpy())
        amp = np.where(np.isfinite(amp), amp, np.nan)
        lignes.append({
            "modele": modele, "cle_modele": cle, "identite": identite,
            "quantite": "log amplification de l'ecart entre camps",
            "n_items": int(np.isfinite(d * amp).sum()),
            "rho_spearman": spearman(d, amp),
            "p": p_permutation_correlation(d, amp, rng),
        })
    sortie = []
    for q in {l["quantite"] for l in lignes}:
        sortie += poser_holm([l for l in lignes if l["quantite"] == q])
    return pd.DataFrame(sortie)


# ---------------------------------------------------------------------------
# 6. Les cinq criteres de chute
# ---------------------------------------------------------------------------

def controles(traces, cel, ecarts, effectifs, ref, options):
    """Section 7 du preenregistrement, verifiee mecaniquement, un verdict par critere."""
    lignes = []
    par_modele = {}
    for t in traces:
        par_modele.setdefault(t["cle_modele"], []).append(t)

    for cle, ts in sorted(par_modele.items()):
        n = len(ts)
        rejets = sum(1 for t in ts if t["rejet"])
        lignes.append({
            "critere": "1. taux de rejet de parse apres relance", "portee": cle,
            "valeur": rejets / n if n else float("nan"), "seuil": "> 0,25 : modele ecarte",
            "verdict": "chute" if n and rejets / n > 0.25 else "passe",
            "detail": f"{rejets} rejets sur {n} cellules",
        })
        # Critere 2 : recopie du gabarit d'exemple de la relance.
        relancees = [t for t in ts if t.get("n_tentatives", 1) > 1 and not t["rejet"]]
        copies = sum(1 for t in relancees if recopie_exemple(t["distribution"]))
        part = copies / len(relancees) if relancees else 0.0
        lignes.append({
            "critere": "2. recopie du gabarit d'exemple de la relance", "portee": cle,
            "valeur": part, "seuil": "> 0,05 des cellules relancees",
            "verdict": "chute, cellules retirees" if part > 0.05 else "passe",
            "detail": f"{copies} recopies sur {len(relancees)} cellules relancees, "
                      f"retirees des mesures",
        })
        # Critere 3 : le modele ignore-t-il le camp ?
        g = cel[(cel["cle_modele"] == cle) & (~cel["rejet"])]
        identiques, total = 0, 0
        for (identite, item), gg in g.groupby(["identite", "item"], sort=False):
            pres = {r["camp"]: r["p_decrit"] for _, r in gg.iterrows()}
            if "gauche" in pres and "droite" in pres:
                total += 1
                identiques += int(pres["gauche"] == pres["droite"])
        part3 = identiques / total if total else float("nan")
        lignes.append({
            "critere": "3. distribution identique d'un camp a l'autre", "portee": cle,
            "valeur": part3, "seuil": "> 0,90 des items : le modele ignore le camp",
            "verdict": "chute" if np.isfinite(part3) and part3 > 0.90 else "passe",
            "detail": f"{identiques} items identiques sur {total}",
        })

    # Critere 4 : etalonnage de l'echelle par les humains reinterroges.
    if len(ecarts):
        e = ecarts.drop_duplicates("item")
        f = (e["gap_signe_reel_w2"].mean() / e["gap_signe_reel_w1"].mean()
             if e["gap_signe_reel_w1"].mean() else float("nan"))
        lignes.append({
            "critere": "4. plancher humain, facteur w2 sur w1", "portee": "humains",
            "valeur": f, "seuil": "hors de [0,85 ; 1,15] : echelle non calibree",
            "verdict": "passe" if np.isfinite(f) and 0.85 <= f <= 1.15 else "chute",
            "detail": f"sur {len(e)} items apparies, ecart signe",
        })
    # Critere 5 : effectifs des camps, contre a30.
    attendus = {"gauche": 417, "centre": 303, "droite": 332}
    obtenus = {}
    for camp in CAMPS:
        v = {n for (i, c, w), n in effectifs.items() if c == camp and w == "w1"}
        obtenus[camp] = max(v) if v else 0
    conforme = all(obtenus[c] <= attendus[c] for c in CAMPS) and \
        all(obtenus[c] > 0 for c in CAMPS)
    lignes.append({
        "critere": "5. effectifs des camps contre a30-gss-par-camp.csv", "portee": "humains",
        "valeur": float(sum(obtenus.values())),
        "seuil": "effectif maximal par camp egal a 417 / 303 / 332",
        "verdict": "passe" if conforme and obtenus == attendus else "a verifier",
        "detail": f"obtenus {obtenus}, attendus {attendus}",
    })
    # Controle 6 : ecart entre les deux estimateurs de dispersion, cote humain.
    if len(cel) and "gs_reel_w1_sans_biais" in cel:
        h = cel.drop_duplicates(["item", "camp"])
        with np.errstate(invalid="ignore", divide="ignore"):
            ecart = (h["gs_reel_w1_sans_biais"] - h["gs_reel_w1"]) / h["gs_reel_w1"]
        m = float(np.nanmean(ecart.to_numpy()))
        lignes.append({
            "critere": "6. estimateur par substitution contre estimateur sans biais (a30)",
            "portee": "humains", "valeur": m,
            "seuil": "informatif : l'ecart relatif moyen doit rester sous 0,01",
            "verdict": "passe" if np.isfinite(m) and abs(m) < 0.01 else "a lire",
            "detail": f"ecart relatif moyen sur {len(h)} couples (item, camp)",
        })
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 7. Figure
# ---------------------------------------------------------------------------

FOND, ENCRE, ENCRE2, GRILLE = "#fcfcfb", "#0b0b0b", "#52514e", "#e2e1dd"
COULEUR_CAMP = {"gauche": "#2a78d6", "centre": "#8a8a86", "droite": "#c8412b"}
HUMAIN = "#1f7a52"


def style(ax):
    ax.set_facecolor(FOND)
    ax.grid(True, color=GRILLE, linewidth=0.8, zorder=0)
    ax.set_axisbelow(True)
    for cote in ("top", "right"):
        ax.spines[cote].set_visible(False)
    for cote in ("left", "bottom"):
        ax.spines[cote].set_color(ENCRE2)
    ax.tick_params(colors=ENCRE2, labelsize=8)


def figure(cel, ecarts, chemin_sans_extension):
    """Deux lignes : l'unanimite par camp, puis l'ecart entre camps. Le plancher est trace.

    Ligne 1, un point par item et par camp : dispersion interne decrite en ordonnee contre
    dispersion reelle en abscisse. Les points verts sont le plancher humain, vague 2 contre
    vague 1 : ils disent ce qu'un instrument parfait produit quand meme comme dispersion.
    Sous la premiere bissectrice, le modele rend le camp plus unanime qu'il n'est.
    Ligne 2, un point par item : ecart signe droite moins gauche, decrit contre reel. La
    pente du nuage EST le facteur d'amplification.
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    ok = cel[(~cel["rejet"]) & (cel["identite"] == "journaliste")]
    cles = [c for c in MODELES if c in set(ok["cle_modele"])]
    if not cles:
        return None
    fig, axes = plt.subplots(2, len(cles), figsize=(4.1 * len(cles), 7.6),
                             squeeze=False, facecolor=FOND)
    for col, cle in enumerate(cles):
        g = ok[ok["cle_modele"] == cle]
        nom = g["modele"].iloc[0]

        ax = axes[0][col]
        style(ax)
        ax.plot([0, 1], [0, 1], color=ENCRE, linewidth=1.0, zorder=2)
        h = g.drop_duplicates("item")
        ax.scatter(h["gs_reel_w1"], h["gs_reel_w2"], s=9, color=HUMAIN, alpha=0.45,
                   linewidths=0, zorder=3, label="plancher humain, vague 2")
        for camp in CAMPS:
            gg = g[g["camp"] == camp]
            ax.scatter(gg["gs_reel_w1"], gg["gs_decrit"], s=11, alpha=0.7, linewidths=0,
                       color=COULEUR_CAMP[camp], zorder=4, label=camp)
        ax.set_xlim(-0.02, 0.92)
        ax.set_ylim(-0.02, 0.92)
        ax.set_title(nom, fontsize=9.5, color=ENCRE)
        ax.set_xlabel("dispersion reelle du camp (Gini Simpson)", fontsize=8, color=ENCRE2)
        if col == 0:
            ax.set_ylabel("dispersion decrite par le modele", fontsize=8.5, color=ENCRE)
            ax.legend(fontsize=7, frameon=False, loc="upper left")

        ax = axes[1][col]
        style(ax)
        e = ecarts[(ecarts["cle_modele"] == cle) & (ecarts["identite"] == "journaliste")]
        lim = 0.9
        ax.plot([-lim, lim], [-lim, lim], color=ENCRE, linewidth=1.0, zorder=2)
        ax.axhline(0, color=GRILLE, linewidth=0.8, zorder=1)
        ax.axvline(0, color=GRILLE, linewidth=0.8, zorder=1)
        ax.scatter(e["gap_signe_reel_w1"], e["gap_signe_reel_w2"], s=9, color=HUMAIN,
                   alpha=0.45, linewidths=0, zorder=3, label="plancher humain, vague 2")
        ax.scatter(e["gap_signe_reel_w1"], e["gap_signe_decrit"], s=12, color="#7a3fa8",
                   alpha=0.75, linewidths=0, zorder=4, label="decrit par le modele")
        ax.set_xlim(-0.45, 0.75)
        ax.set_ylim(-0.45, 0.75)
        ax.set_xlabel("ecart reel droite moins gauche (position)", fontsize=8, color=ENCRE2)
        if col == 0:
            ax.set_ylabel("ecart decrit droite moins gauche", fontsize=8.5, color=ENCRE)
            ax.legend(fontsize=7, frameon=False, loc="upper left")

    fig.suptitle("r1. L'oracle des camps : ce que le modele dit de chaque camp, "
                 "contre la realite du GSS", fontsize=11, color=ENCRE, y=0.985)
    fig.text(0.5, 0.005,
             "Identite du demandeur : journaliste neutre. Sous la bissectrice, le modele "
             "rend le camp plus unanime qu'il n'est.",
             ha="center", fontsize=7.5, color=ENCRE2)
    fig.tight_layout(rect=[0, 0.02, 1, 0.965])
    for ext in ("png", "svg"):
        fig.savefig(f"{chemin_sans_extension}.{ext}", dpi=200, facecolor=FOND)
    plt.close(fig)
    return chemin_sans_extension


# ---------------------------------------------------------------------------
# 8. Resume lisible
# ---------------------------------------------------------------------------

def ligne_nombre(v, n=3):
    return "n. d." if v is None or not np.isfinite(v) else f"{v:.{n}f}".replace(".", ",")


def ecrire_resume(chemin, traces, cel, h1, h2, h3, h4, ctl, suffixe):
    n_total = len(traces)
    n_rejets = int(cel["rejet"].sum()) if len(cel) else 0
    n_parse = sum(1 for t in traces if t["rejet"])
    n_copies = n_rejets - n_parse
    lignes = [
        "# r1. Resume d'evaluation de l'oracle des camps",
        "",
        "Ecrit par `analyses/r1_evaluer.py`. Aucun appel de modele. Les definitions, les "
        "seuils et les corrections sont ceux de `resultats/r1-preenregistrement.md`, "
        "ecrit avant le premier appel.",
        "",
        (f"Perimetre lu : **{n_total} cellules** de trace"
         + (f", suffixe `{suffixe}`" if suffixe else "")
         + f", dont **{n_parse} rejets de parse** et **{n_copies} cellules retirees "
           f"pour recopie de l'exemple de relance** (critere de chute 2). "
           f"Perimetre exploite : **{n_total - n_rejets} cellules**, soit "
         + f"{(n_total - n_rejets) / n_total * 100:.1f}".replace(".", ",")
         + " pour cent.")
        if n_total else "Aucune cellule lue.",
        "",
        "## Criteres de chute",
        "",
        "| critere | portee | valeur | verdict |", "|---|---|---|---|",
    ]
    for _, r in ctl.iterrows():
        lignes.append(f"| {r['critere']} | {r['portee']} | {ligne_nombre(r['valeur'])} "
                      f"| {r['verdict']} |")
    lignes += ["", "## H1, l'unanimite decrite contre l'unanimite reelle", "",
               "Rapport `GS decrit / GS reel`. Sous 1, le modele rend le camp plus unanime "
               "qu'il n'est. Le plancher est le meme rapport entre les deux vagues humaines.",
               "",
               "| modele | camp | identite | GS decrit | GS reel | rapport | IC 95 % | "
               "plancher | p Holm | verdict |", "|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in h1.iterrows():
        lignes.append(
            f"| {r['modele']} | {r['camp']} | {r['identite']} | "
            f"{ligne_nombre(r['gs_decrit_moyen'])} | {ligne_nombre(r['gs_reel_moyen'])} | "
            f"**{ligne_nombre(r['ratio'])}** | [{ligne_nombre(r['ic_bas'])} ; "
            f"{ligne_nombre(r['ic_haut'])}] | {ligne_nombre(r['ratio_plancher_w2_w1'])} | "
            f"{ligne_nombre(r['p_holm'], 4)} | "
            f"{verdict(r['ratio'], r['ic_bas'], r['ic_haut'], r['p_holm'])} |")
    lignes += ["", "## H2, l'ecart entre camps", "",
               "| hypothese | modele | identite | perimetre | ecart decrit | ecart reel | "
               "facteur | IC 95 % | plancher | p Holm | verdict |",
               "|---|---|---|---|---|---|---|---|---|---|---|"]
    for _, r in h2.iterrows():
        lignes.append(
            f"| {r['hypothese']} | {r['modele']} | {r['identite']} | {r['perimetre']} | "
            f"{ligne_nombre(r['ecart_decrit_moyen'])} | {ligne_nombre(r['ecart_reel_moyen'])} | "
            f"**{ligne_nombre(r['facteur'])}** | [{ligne_nombre(r['ic_bas'])} ; "
            f"{ligne_nombre(r['ic_haut'])}] | "
            f"{ligne_nombre(r['facteur_plancher_w2_w1'])} | {ligne_nombre(r['p_holm'], 4)} | "
            f"{verdict(r['facteur'], r['ic_bas'], r['ic_haut'], r['p_holm'])} |")
    lignes += ["", "## H3, l'identite du demandeur", "",
               "Distance entre le portrait fait au journaliste et celui fait a un membre "
               "du camp adverse, contre le plancher de reinterrogation humaine. Le centre "
               "est exclu, comme annonce.", "",
               "| modele | camp | TV entre identites | plancher humain | rapport | "
               "IC 95 % | items identiques | p Holm |",
               "|---|---|---|---|---|---|---|---|"]
    for _, r in h3.iterrows():
        lignes.append(
            f"| {r['modele']} | {r['camp']} | "
            f"{ligne_nombre(r['tv_entre_identites_moyenne'])} | "
            f"{ligne_nombre(r['plancher_humain_moyen'])} | "
            f"**{ligne_nombre(r['rapport_au_plancher'])}** | "
            f"[{ligne_nombre(r['ic_bas'])} ; {ligne_nombre(r['ic_haut'])}] | "
            f"{ligne_nombre(r['part_items_identiques'])} | "
            f"{ligne_nombre(r['p_holm'], 4)} |")
    lignes += ["", "## H4, les items a derive marquee", "",
               "| modele | identite | quantite | rho de Spearman | n items | p Holm |",
               "|---|---|---|---|---|---|"]
    for _, r in h4.iterrows():
        lignes.append(f"| {r['modele']} | {r['identite']} | {r['quantite']} | "
                      f"**{ligne_nombre(r['rho_spearman'])}** | {int(r['n_items'])} | "
                      f"{ligne_nombre(r['p_holm'], 4)} |")
    lignes += ["", "## Ce que ce resume ne dit pas", "",
               "- Aucune croyance humaine de second ordre n'est mesuree ici : les items "
               "ANES ne sont pas dans ce run. La phrase « le modele exagere plus que les "
               "humains » est interdite.",
               "- Le facteur de H2b n'est pas celui de `a38` : perimetre d'items et mode "
               "different, seuls le signe et l'ordre de grandeur se comparent.",
               "- Rien ici ne porte hors du GSS, hors des Etats Unis, ni hors de ces trois "
               "modeles a cette quantification.", ""]
    # Un tableau sans ligne se lit comme un en tete orphelin. Sur un run partiel c'est le
    # cas normal, et il faut le dire au lecteur du matin plutot que de le laisser deviner.
    sortie, i = [], 0
    while i < len(lignes):
        sortie.append(lignes[i])
        if (lignes[i].startswith("|---") and
                (i + 1 >= len(lignes) or not lignes[i + 1].startswith("|"))):
            sortie.append("")
            sortie.append("Aucune ligne : le perimetre lu ne contient pas encore de quoi "
                          "calculer cette famille de tests.")
        i += 1
    with open(chemin, "w", encoding="utf-8") as fh:
        fh.write("\n".join(sortie))
    return chemin


# ---------------------------------------------------------------------------

def ecrire(df, nom, suffixe):
    os.makedirs(SORTIE, exist_ok=True)
    base, ext = os.path.splitext(nom)
    chemin = os.path.join(SORTIE, base + (("-" + suffixe) if suffixe else "") + ext)
    df.to_csv(chemin, index=False)
    print(f"  ecrit : {chemin} ({len(df)} lignes)", flush=True)
    return chemin


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suffixe", default="", help="lit les traces r1-*-<suffixe>.jsonl")
    ap.add_argument("--sans-figure", action="store_true")
    args = ap.parse_args()

    rng = np.random.default_rng(GRAINE)
    traces = lire_traces(args.suffixe)
    if not traces:
        sys.exit("aucune trace r1 lisible")
    print(f"{len(traces)} cellules lues", flush=True)
    ref, options, effectifs = lire_referent(args.suffixe)
    sens, oriente, strict, derive = lire_a37()

    cel = par_cellule(traces, ref, options, sens, effectifs)
    ecarts = par_item_ecarts(cel, ref, sens) if len(cel) else pd.DataFrame()
    ident = par_item_identite(cel, ref) if len(cel) else pd.DataFrame()

    ecrire(cel.drop(columns=["p_decrit"], errors="ignore"), "r1-par-cellule.csv", args.suffixe)
    if len(ecarts):
        ecrire(ecarts, "r1-par-item-ecarts.csv", args.suffixe)
    if len(ident):
        ecrire(ident, "r1-identite.csv", args.suffixe)

    h1 = test_h1(cel, rng)
    h2 = test_h2(ecarts, rng, oriente, strict) if len(ecarts) else pd.DataFrame()
    h3 = test_h3(ident, rng) if len(ident) else pd.DataFrame()
    h4 = test_h4(cel, ecarts, derive, rng) if len(ecarts) else pd.DataFrame()
    ctl = controles(traces, cel, ecarts, effectifs, ref, options)

    for df, nom in ((h1, "r1-h1-unanimite.csv"), (h2, "r1-h2-ecart.csv"),
                    (h3, "r1-h3-identite.csv"), (h4, "r1-h4-derive.csv"),
                    (ctl, "r1-controles.csv")):
        if len(df):
            ecrire(df, nom, args.suffixe)

    if not args.sans_figure and len(ecarts):
        base = os.path.join(SORTIE, "r1-figure-oracle" + (("-" + args.suffixe)
                                                          if args.suffixe else ""))
        if figure(cel, ecarts, base):
            print(f"  figure : {base}.png et .svg", flush=True)

    chemin = os.path.join(SORTIE, "r1-resume" + (("-" + args.suffixe) if args.suffixe else "")
                          + ".md")
    ecrire_resume(chemin, traces, cel, h1, h2, h3, h4, ctl, args.suffixe)
    print(f"  resume : {chemin}", flush=True)


if __name__ == "__main__":
    main()
