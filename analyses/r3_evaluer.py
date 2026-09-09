"""
r3_evaluer : evaluation de R3, la vraie ablation de l'etiquette, a un seul facteur.

La famille d'hypotheses, les mesures, les corrections et les criteres de chute sont
ecrits dans resultats/r3-preenregistrement.md, HORODATE DU 8 SEPTEMBRE 2026 A 22:30:01
CEST, avant le moindre appel de modele de langage. Rappel de la famille, pour que le
script en porte lui aussi la trace :

  F1  5 tests  H1a chute sous permutation intra segment, C3E contre C3, sous DEUX
               segmentations, dirigee vers la BAISSE ; H1b ratio inter, dirigee vers la
               hausse ; H1c rarete de groupe sur personne, dirigee vers la hausse ;
               H1d exactitude par personne, dirigee vers la hausse.
  F2  5 tests  H2a ratio inter sur l'axe ideologie, C2 contre C2S, dirigee vers la
               baisse quand l'ideologie sort ; H2b chute sous permutation sous les deux
               segmentations ; H2c rarete de groupe sur personne ; H2d exactitude,
               bilaterale.
  F3  1 test   H3 l'effet des deux lignes politiques est plus grand que celui des neuf
               autres attributs, dans le regime riche.

  Familles corrigees SEPAREMENT par Holm, Benjamini Hochberg rapporte a cote. Tous les p
  sont des p de bootstrap APPARIE SUR LES PERSONNES, memes tirages pour les deux termes
  d'un contraste, plancher a 1 sur le nombre de tirages. Le rappel des raretes stables
  est publie hors famille, declare secondaire et sous puissant par la page de plan.

Zero appel de modele de langage : ce script ne fait que relire des traces. Lecture seule
sur data/. AUCUN SCRIPT EXISTANT N'EST MODIFIE. Sont importes tels quels :

  a44_commun   permuter_intra(), exactitude(), alphabet(), coder(), ratios(),
               segmentations(), covariables_rarete(), groupe_sur_personne(), holm(),
               benjamini_hochberg(), ic_percentile(), ecrire(), charger().
  a31_commun   par l'intermediaire de a44_commun.groupe_sur_personne, c'est la
               definition de a31 section 2.3 qui est employee, sans retouche.
  a42_commun   classes_stabilite() (la partition P_A), modalites_rares(), observe(),
               appartient(), masques(), mesure_sur(), frequence_item(),
               frequence_segment(), rappel_vague2(), segment_fin().
  a2_commun    exactitude_par_personne(), est_manquant().
  a5_evaluer   moyenner_passes() et en_matrices(), pour lire les traces JSONL sans en
               reecrire le format.

Ce que ce script ajoute et qui n'existe nulle part ailleurs : le contraste a UN facteur.
Tout le dossier compare C2 a C3, c'est a dire deux conditions qui echangent toute leur
entree. Ici, les deux termes de chaque contraste different d'un bloc de texte et de rien
d'autre, sur les MEMES personnes et les MEMES cellules.

Tolerance au partiel. Le run de nuit est tronque a 08:00 et C3E ne couvrira pas les 150
personnes. Chaque contraste est evalue sur les personnes COMPLETES DANS LES DEUX
conditions comparees, et la couverture est ecrite en tete de chaque tableau. Une
condition absente ne fait pas echouer le script : son contraste est simplement declare
non teste, jamais non rejete.

Entree  : data/traces/r3-C3E-qwen4.jsonl, r3-C2S-qwen4.jsonl, r3-C3ES-qwen4.jsonl,
          a5-C3-p1.jsonl, a5-C2-p1.jsonl ; caches /tmp/a25-matrices.pkl,
          /tmp/a28-foret.npy, /tmp/a35-methodes.pkl.
Sortie  : resultats/r3-couverture.csv, r3-tableau.csv, r3-contrastes.csv,
          r3-permutation.csv, r3-rarete.csv, r3-controles.csv.

Usage :
  .venv/bin/python analyses/r3_evaluer.py --tirages 2000
  .venv/bin/python analyses/r3_evaluer.py --essai-sur-a5   (test hors ligne, sans R3)
"""

import argparse
import json
import os
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import a28_commun as C28
import a42_commun as C42
import a44_commun as C44
from a2_commun import exactitude_par_personne
from a5_agents_locaux_gss import TRACES, groupes_familles, nomenclature
from a5_evaluer import en_matrices, moyenner_passes

SORTIE = C44.SORTIE
SEUIL = C44.SEUIL_RARE
GRAINE = 20260909

# Les conditions lues. (nom affiche, fichier, nom de condition DANS la trace).
# C2 et C3 sont les traces existantes de a5 : elles couvrent les 149 items et 150
# personnes, et R3 les restreint aux 58 items de famille. Aucune d'elles n'est reecrite.
TRACES_R3 = [
    ("C3E", "r3-C3E-qwen4.jsonl", "C3E"),
    ("C2S", "r3-C2S-qwen4.jsonl", "C2S"),
    ("C3ES", "r3-C3ES-qwen4.jsonl", "C3ES"),
    ("C3", "a5-C3-p1.jsonl", "C3"),
    ("C2", "a5-C2-p1.jsonl", "C2"),
]

# (nom, condition AVEC l'etiquette, condition SANS, ce que le contraste isole).
# La convention de signe est fixee ici et vaut pour tout le fichier : l'effet est
# toujours « avec l'etiquette moins sans l'etiquette ».
CONTRASTES = [
    ("H1", "C3E", "C3", "les 11 attributs ajoutes a 119 reponses"),
    ("H2", "C2", "C2S", "l'ideologie et le parti dans le regime pauvre"),
    ("H3a", "C3E", "C3ES", "l'ideologie et le parti dans le regime riche"),
    ("H3b", "C3ES", "C3", "les neuf autres attributs dans le regime riche"),
]

# Sens predit par la these du dossier, ecrit dans la page de plan section 4. `baisse`
# veut dire que l'effet attendu de l'etiquette est negatif, `hausse` positif, `aucun`
# que le test est bilateral.
SENS = {
    "chute permutation S_ideo": "baisse",
    "chute permutation S_gra": "baisse",
    "ratio inter (S_ideo)": "hausse",
    "ratio inter (S_gra)": "hausse",
    "ratio intra (S_ideo)": "aucun",
    "ratio intra (S_gra)": "aucun",
    "groupe sur personne": "hausse",
    "rappel des rares": "aucun",
    "exactitude": "hausse",
}

# Mesures qui entrent dans les familles corrigees par Holm, dans l'ordre de la page de
# plan. Le reste est publie sans correction et declare descriptif.
FAMILLE_F1 = ["chute permutation S_ideo", "chute permutation S_gra",
              "ratio inter (S_gra)", "groupe sur personne", "exactitude"]
FAMILLE_F2 = ["ratio inter (S_ideo)", "chute permutation S_ideo",
              "chute permutation S_gra", "groupe sur personne", "exactitude"]


# ---------------------------------------------------------------------------
# 1. Lecture des traces, sans reecrire le format de a5
# ---------------------------------------------------------------------------

def lire_trace(chemin):
    """Charge une trace JSONL, indexee par (condition, passe) comme a5_evaluer.

    Les doublons sont ecrases par la derniere occurrence : une relance apres arret brutal
    peut reecrire une ligne coupee en deux. Les lignes tronquees sont ignorees sans faire
    echouer la lecture, ce qui est indispensable ici : la trace de C3E sera coupee en
    plein vol par la fin dure de 08:00.
    """
    tables = defaultdict(dict)
    if not os.path.exists(chemin):
        return tables
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            if "pid" not in d or "distribution" not in d:
                continue
            tables[(d["condition"], d.get("passe", 1))][(d["pid"], d["item"])] = d
    return tables


def matrice_depuis_trace(paquet, chemin, condition, table_nomenclature, items_cible):
    """Matrice 1 052 x 149, None hors des cellules effectivement predites.

    Meme construction que r2_evaluer, avec le perimetre d'items en parametre : une
    personne est COMPLETE quand ses cellules sur les 58 items de famille sont toutes
    presentes. Les traces de a5 couvrent les 149 items ; la completude est jugee sur les
    58, ce qui est exactement la restriction que la page de plan declare.
    """
    ids, items = paquet["ids"], paquet["items"]
    index_personne = {p: i for i, p in enumerate(ids)}
    noms_cibles = {items[j] for j in items_cible}
    tables = lire_trace(chemin)
    cles = [(c, p) for (c, p) in tables if c == condition]
    if not cles:
        return None
    compte = defaultdict(int)
    for c in cles:
        for (pid, it) in tables[c]:
            if it in noms_cibles:
                compte[pid] += 1
    n_passes = len(cles)
    complets = {pid for pid, n in compte.items() if n >= len(noms_cibles) * n_passes}

    chemin_ech = os.path.join(TRACES, "a5-personnes.csv")
    ech = pd.read_csv(chemin_ech)
    personnes = [p for p in ech["pid"] if p in complets]
    if not personnes:
        return None
    fusion, passes = moyenner_passes(tables, condition)
    pred, _dist = en_matrices(fusion, personnes, items, table_nomenclature)

    plein = np.empty((len(ids), len(items)), dtype=object)
    plein[:] = None
    lignes = [index_personne[p] for p in personnes]
    plein[np.ix_(lignes, list(range(len(items))))] = pred
    return {"matrice": plein, "personnes": personnes, "lignes": np.array(lignes),
            "partielles": len(compte) - len(complets),
            "appels": sum(len(tables[c]) for c in cles), "passes": passes,
            "chemin": chemin}


def registre_modeles(chemin):
    """Modele, quantification, gabarit et variante lus dans la trace elle meme.

    Le registre n'est pas recopie a la main : il est relu du fichier, ce qui garantit
    qu'il decrit le run et non l'intention du run.
    """
    if not os.path.exists(chemin):
        return {}
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            return {k: d.get(k) for k in ("modele", "quantification", "gabarit",
                                          "variante_fin", "version_prompt")}
    return {}


# ---------------------------------------------------------------------------
# 2. Les deux segmentations exigees par a45
# ---------------------------------------------------------------------------

def segmentations_r3(paquet):
    """S_ideo, l'axe publie par a44, et S_gra, genre x race x age, SANS ideologie.

    a45 objection 2 : la chute sous permutation de a44 n'est mesuree qu'a l'interieur de
    la variable que l'invite contient, et sous une segmentation sans ideologie de meme
    finesse `v8` passe de 0,072 a 0,266 du plancher humain. Les deux sont donc publiees
    cote a cote, et aucun verdict n'est retenu si le signe change de l'une a l'autre.

    S_gra est construit exactement comme S_fin de a44_commun, en remplacant le bloc
    d'ideologie par la race : meme normalisation C28.norm, meme convention -1 pour les
    valeurs non renseignees, meme tri des modalites.
    """
    seg, _niveaux = C44.segmentations(paquet)
    col = {a: i for i, a in enumerate(paquet["attributs"])}
    brut = {a: [C28.norm(v) for v in paquet["x"][:, col[a]]]
            for a in ("gender", "race", "age")}
    gra = [f"{g}|{r}|{a}" for g, r, a in zip(brut["gender"], brut["race"], brut["age"])]
    mods = sorted({v for v in gra if v.strip() and "non renseigne" not in v})
    idx = {m: k for k, m in enumerate(mods)}
    return {"S_ideo": seg["S_ideo"],
            "S_gra": np.array([idx.get(v, -1) for v in gra], dtype=np.int32)}


def chute_permutation(pred, verite, seg, n_permutations, rng, n_min=10):
    """Exactitude perdue quand on permute les personnes a l'interieur de leur segment.

    Quantite de a44 section 5. Si une condition est un gabarit de groupe, les reponses
    sont echangeables entre personnes du meme segment et l'exactitude ne bouge pas ; si
    elle porte la personne, elle chute.

    Renvoie NaN, jamais zero, quand aucun segment n'atteint n_min personnes : sur un
    perimetre de 80 personnes, un segment de moins de dix individus rend la permutation
    presque l'identite, et la chute mesuree serait un artefact de taille.
    """
    tailles = [int((seg == k).sum()) for k in np.unique(seg) if k >= 0]
    if not tailles or max(tailles) < n_min:
        return {"exactitude": np.nan, "exactitude_permutee": np.nan, "chute": np.nan,
                "chute_relative": np.nan, "segments_exploitables": 0,
                "taille_segment_max": max(tailles) if tailles else 0}
    base = float(np.nanmean(exactitude_par_personne(pred, verite)))
    tirs = [float(np.nanmean(exactitude_par_personne(pred[C44.permuter_intra(
        len(pred), seg, rng)], verite))) for _ in range(n_permutations)]
    permutee = float(np.mean(tirs))
    return {"exactitude": base, "exactitude_permutee": permutee,
            "chute": base - permutee,
            "chute_relative": (base - permutee) / base if base else np.nan,
            "segments_exploitables": int(sum(1 for t in tailles if t >= n_min)),
            "taille_segment_max": max(tailles)}


# ---------------------------------------------------------------------------
# 3. Les mesures d'une condition sur un jeu de lignes
# ---------------------------------------------------------------------------

def contexte_perimetre(paquet, lignes, colonnes, segs):
    """Tout ce qui ne depend que de la verite humaine, calcule une fois par perimetre.

    Les planchers de a42 restent des descripteurs de POPULATION : ils sont calcules sur
    les 1 052 humains de la vague 1 puis restreints aux lignes, regle de a34 reprise par
    a42. Les recalculer sur 80 personnes donnerait des cases de segment d'une ou deux
    personnes et le plancher deviendrait du bruit.
    """
    y1_tot, y2_tot = paquet["y1"], paquet["M"]["humains vague 2"]
    ok_tot = C42.observe(y1_tot)
    seg_fin, _niv = C42.segment_fin(paquet["x"], paquet["attributs"])
    d_item = C42.frequence_item(y1_tot, y1_tot, ok_tot)
    d_seg = C42.frequence_segment(y1_tot, y1_tot, ok_tot, seg_fin)
    h2 = C42.rappel_vague2(y1_tot, y2_tot)

    y1 = y1_tot[lignes]
    y2 = y2_tot[lignes]
    mods = C42.modalites_rares(y1, SEUIL)
    ok = C42.observe(y1)
    rare_vrai = C42.appartient(y1, mods) & ok
    stab = C42.classes_stabilite(y1, y2)

    alpha = C44.alphabet(paquet["items"], paquet["options"])
    k_max = int(max(len(paquet["options"][it]) for it in paquet["items"]))
    codes_h, _hors = C44.coder(y1_tot, alpha)

    return {
        "lignes": lignes, "colonnes": colonnes, "y1": y1, "verite": y1,
        "mods": mods, "ok": ok, "rare_vrai": rare_vrai, "stab": stab,
        "planchers": {"item": d_item[lignes], "segment": d_seg[lignes],
                      "humains vague 2": h2[lignes]},
        "alpha": alpha, "k_max": k_max, "codes_h": codes_h[lignes],
        "segs": {k: v[lignes] for k, v in segs.items()},
        "cv": {k: C44.covariables_rarete(y1, segs[k][lignes]) for k in segs},
    }


def restreindre(masque, colonnes):
    """Masque booleen mis a zero hors des colonnes retenues.

    C'est ainsi que le perimetre d'items entre dans les mesures de rarete : les
    definitions de rarete et de stabilite restent celles de a42, calculees sur tous les
    items, et seule la selection des cellules jugees change.
    """
    out = np.zeros_like(masque, dtype=bool)
    out[:, colonnes] = masque[:, colonnes]
    return out


def sous_contexte(ctx, idx):
    """Le contexte restreint a un tirage bootstrap de lignes. Les mods ne bougent pas.

    Retirer et remettre les modalites rares a chaque tirage ferait bouger la definition
    de la rarete avec l'echantillon, et le contraste ne comparerait plus les memes
    cellules d'une condition a l'autre.
    """
    cv = {}
    for k, c in ctx["cv"].items():
        cv[k] = {"verite": c["verite"][idx], "mods": c["mods"], "ok": c["ok"][idx],
                 "rare_vrai": c["rare_vrai"][idx], "r_personne": c["r_personne"][idx],
                 "r_segment": c["r_segment"][idx]}
    return {**ctx, "y1": ctx["y1"][idx], "verite": ctx["verite"][idx],
            "ok": ctx["ok"][idx], "rare_vrai": ctx["rare_vrai"][idx],
            "stab": ctx["stab"][idx], "codes_h": ctx["codes_h"][idx],
            "planchers": {k: v[idx] for k, v in ctx["planchers"].items()},
            "segs": {k: v[idx] for k, v in ctx["segs"].items()}, "cv": cv}


def mesurer(pred, ctx, rng, n_permutations, avec_permutation=True):
    """Toutes les quantites de la page de plan section 5, pour une condition.

    pred : matrice des predictions restreinte aux lignes du perimetre, 149 colonnes. La
    restriction aux 58 items se fait par `colonnes`, jamais en coupant la matrice, pour
    que les definitions de rarete restent celles de a42.
    """
    colonnes = ctx["colonnes"]
    out = {}

    p58 = pred[:, colonnes]
    v58 = ctx["verite"][:, colonnes]
    out["exactitude"] = float(np.nanmean(exactitude_par_personne(p58, v58)))

    codes_p, hors = C44.coder(pred, ctx["alpha"])
    out["part_hors_nomenclature"] = float(hors)
    for nom_seg, seg in ctx["segs"].items():
        r = C44.ratios(codes_p, ctx["codes_h"], seg, ctx["k_max"], colonnes)
        cle = "S_ideo" if nom_seg == "S_ideo" else "S_gra"
        out[f"ratio inter ({cle})"] = r["inter"]
        out[f"ratio intra ({cle})"] = r["intra"]
        out[f"items retenus ({cle})"] = r["n_items"]

    g = C44.groupe_sur_personne(pred, ctx["cv"]["S_ideo"])
    out["groupe sur personne"] = g["groupe_sur_personne"]
    out["lift personne"] = g["lift_personne"]
    out["lift segment"] = g["lift_segment"]
    out["rappel des rares"] = g["rappel_rares"]
    out["fausses raretes"] = g["fausses_raretes"]

    if avec_permutation:
        for nom_seg, seg in ctx["segs"].items():
            cle = "S_ideo" if nom_seg == "S_ideo" else "S_gra"
            c = chute_permutation(p58, v58, seg, n_permutations, rng)
            out[f"chute permutation {cle}"] = c["chute"]
            out[f"chute relative {cle}"] = c["chute_relative"]
            out[f"segments exploitables {cle}"] = c["segments_exploitables"]
    return out


def mesures_rares(pred, ctx, classe="stable"):
    """Rappel, precision et exces sur les trois planchers, sur une classe de P_A.

    Les couples (numerateur, denominateur) par personne sont ceux de
    a42_commun.mesure_sur : le meme tirage de personnes sert aux deux conditions, ce qui
    rend le contraste apparie.
    """
    colonnes = ctx["colonnes"]
    m = C42.masques(pred, ctx["y1"], ctx["mods"])
    sel = {"stable": ctx["stab"] == 1, "instable": ctx["stab"] == 0,
           "ensemble": np.ones_like(ctx["stab"], dtype=bool)}[classe]
    selv = restreindre(ctx["rare_vrai"] & sel, colonnes)
    selp = restreindre(m["rare_pred"] & sel, colonnes)
    juste = restreindre(m["juste"], colonnes)
    return C42.mesure_sur(selv, selp, juste, ctx["planchers"])


# ---------------------------------------------------------------------------
# 4. Les contrastes, apparies sur les personnes
# ---------------------------------------------------------------------------

def p_dirige(tirages, sens):
    """p de bootstrap, unilateral quand la page de plan declare un sens.

    Convention : les tirages sont ceux de l'effet « avec l'etiquette moins sans ». Pour
    un sens `hausse`, le p unilateral est la part des tirages sous zero ; pour `baisse`,
    la part au dessus ; pour `aucun`, le p bilateral de a44_commun.ic_percentile. Le
    plancher est 1 sur le nombre de tirages : un p de zero n'existe pas dans un
    bootstrap, et l'ecrire serait mentir sur la resolution.
    """
    t = np.asarray([x for x in tirages if np.isfinite(x)], dtype=float)
    if not len(t):
        return np.nan, np.nan, 1.0
    bas, haut = float(np.percentile(t, 2.5)), float(np.percentile(t, 97.5))
    if sens == "hausse":
        p = float((t <= 0).mean())
    elif sens == "baisse":
        p = float((t >= 0).mean())
    else:
        return C44.ic_percentile(t)
    return bas, haut, float(min(max(p, 1.0 / len(t)), 1.0))


def contraste(nom, avec, sans, paquet, infos, colonnes, segs, args, controles):
    """Un contraste a un facteur : memes personnes, memes cellules, un bloc de texte."""
    lignes = np.array(sorted(set(infos[avec]["lignes"]) & set(infos[sans]["lignes"])))
    if len(lignes) < args.personnes_min:
        return [], [], {"contraste": nom, "avec": avec, "sans": sans,
                        "personnes_communes": len(lignes), "teste": False,
                        "motif": f"moins de {args.personnes_min} personnes communes"}

    ctx = contexte_perimetre(paquet, lignes, colonnes, segs)
    pa = paquet["M"][avec][lignes]
    pb = paquet["M"][sans][lignes]
    rng = np.random.default_rng(GRAINE)
    ma = mesurer(pa, ctx, rng, args.permutations)
    rng = np.random.default_rng(GRAINE)
    mb = mesurer(pb, ctx, rng, args.permutations)

    print(f"\n=== {nom} : {avec} contre {sans}, {len(lignes)} personnes communes, "
          f"{len(colonnes)} items ===", flush=True)
    for cle in SENS:
        if cle in ma:
            print(f"  {cle:<28} {avec} {ma[cle]:>9.4f}   {sans} {mb[cle]:>9.4f}   "
                  f"effet {ma[cle] - mb[cle]:>+9.4f}", flush=True)

    # -------------------------------------------------- bootstrap apparie
    n = len(lignes)
    rb = np.random.default_rng(GRAINE + 1)
    idx_boot = [rb.integers(0, n, n) for _ in range(args.tirages)]
    tirages = defaultdict(list)
    cles_legeres = [c for c in SENS if not c.startswith("chute")]
    for t, idx in enumerate(idx_boot):
        sc = sous_contexte(ctx, idx)
        r1 = np.random.default_rng(GRAINE + 2)
        r2 = np.random.default_rng(GRAINE + 2)
        a = mesurer(pa[idx], sc, r1, 0, avec_permutation=False)
        b = mesurer(pb[idx], sc, r2, 0, avec_permutation=False)
        for c in cles_legeres:
            tirages[c].append(a.get(c, np.nan) - b.get(c, np.nan))
        if args.pas and (t + 1) % args.pas == 0:
            print(f"    bootstrap {t + 1}/{args.tirages}", flush=True)

    # La chute sous permutation coute une permutation par tirage : elle a son propre
    # nombre de tirages, plus petit, et son propre nombre de permutations, declares en
    # ligne de commande et ecrits dans le tableau des controles.
    rp = np.random.default_rng(GRAINE + 3)
    idx_perm = [rp.integers(0, n, n) for _ in range(args.tirages_permutation)]
    for t, idx in enumerate(idx_perm):
        sc = sous_contexte(ctx, idx)
        for cle_seg, seg in sc["segs"].items():
            cle = "S_ideo" if cle_seg == "S_ideo" else "S_gra"
            r1 = np.random.default_rng(GRAINE + 4 + t)
            r2 = np.random.default_rng(GRAINE + 4 + t)
            ca = chute_permutation(pa[idx][:, colonnes], sc["verite"][:, colonnes], seg,
                                   args.permutations_bootstrap, r1)
            cb = chute_permutation(pb[idx][:, colonnes], sc["verite"][:, colonnes], seg,
                                   args.permutations_bootstrap, r2)
            tirages[f"chute permutation {cle}"].append(ca["chute"] - cb["chute"])

    lignes_tab = []
    for nom_cond, m in ((avec, ma), (sans, mb)):
        lignes_tab.append({"contraste": nom, "condition": nom_cond,
                           "personnes": len(lignes), "items": len(colonnes),
                           **{k: v for k, v in m.items()}})

    lignes_con = []
    for cle, sens in SENS.items():
        if cle not in ma:
            continue
        t = tirages.get(cle, [])
        bas, haut, p = p_dirige(t, sens)
        lignes_con.append({
            "contraste": nom, "avec": avec, "sans": sans, "mesure": cle,
            "sens_predit": sens, "personnes": len(lignes),
            "valeur_avec": ma[cle], "valeur_sans": mb[cle],
            "effet": ma[cle] - mb[cle], "ic_bas": bas, "ic_haut": haut,
            "p_bootstrap": p, "tirages": len(t)})

    # -------------------------------------------------- rarete, hors famille
    lignes_rar = []
    for classe in ("stable", "ensemble"):
        ra = mesures_rares(pa, ctx, classe)
        rbb = mesures_rares(pb, ctx, classe)
        for cle in ("rappel", "precision", "exces_segment", "exces_item",
                    "exces_humains vague 2"):
            if cle not in ra:
                continue
            lignes_rar.append({
                "contraste": nom, "avec": avec, "sans": sans, "classe_PA": classe,
                "mesure": cle, "valeur_avec": ra[cle], "valeur_sans": rbb[cle],
                "effet": ra[cle] - rbb[cle],
                "cellules": ra.get("cellules"), "personnes": len(lignes)})

    controles.append({
        "controle": f"cellules rares stables, {nom}",
        "valeur": float(mesures_rares(pa, ctx, "stable")["cellules"]),
        "reference": 78.0,
        "detail": "R2 annonce 31 cellules sur 60 personnes et ~78 sur 150 ; en dessous "
                  "de 40 les contrastes de rarete sont declares sous puissants"})

    couverture = {"contraste": nom, "avec": avec, "sans": sans,
                  "personnes_communes": len(lignes), "teste": True, "motif": ""}
    return lignes_tab + lignes_con, lignes_rar, couverture


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--tirages", type=int, default=2000)
    ap.add_argument("--tirages-permutation", type=int, default=200)
    ap.add_argument("--permutations", type=int, default=200)
    ap.add_argument("--permutations-bootstrap", type=int, default=20)
    ap.add_argument("--personnes-min", type=int, default=30)
    ap.add_argument("--pas", type=int, default=500)
    ap.add_argument("--suffixe", default="")
    ap.add_argument("--racine-traces", default=TRACES)
    ap.add_argument("--essai-sur-a5", action="store_true",
                    help="test hors ligne sans R3 : n'utilise que les traces C2 et C3 de "
                         "a5, restreintes aux 58 items, avec un placebo C3 contre C3 dont "
                         "l'effet doit etre exactement nul, et le contraste connu C2 "
                         "contre C3")
    args = ap.parse_args()

    if args.essai_sur_a5:
        args.tirages = min(args.tirages, 200)
        args.tirages_permutation = min(args.tirages_permutation, 30)
        args.permutations = min(args.permutations, 50)
        args.pas = 100

    t0 = time.time()
    controles = []

    print("chargement du paquet (caches de a25, a28 et a35)", flush=True)
    paquet = C44.charger(args.cache, args.cache_foret, args.cache_a35)
    items = paquet["items"]
    colonnes = np.array(sorted({j for _n, cols in groupes_familles(items) for j in cols}))
    controles.append({"controle": "items de famille", "valeur": float(len(colonnes)),
                      "reference": 58.0,
                      "detail": "six familles de a2_baselines_gss, memes items que R2"})
    segs = segmentations_r3(paquet)
    for nom_seg, seg in segs.items():
        controles.append({"controle": f"cases de {nom_seg}",
                          "valeur": float(len({int(v) for v in seg if v >= 0})),
                          "reference": np.nan,
                          "detail": "S_ideo : sept niveaux d'ideologie (a44). S_gra : "
                                    "genre x race x age, SANS ideologie (a45 objection 2)"})
    table = nomenclature()

    # ---------------------------------------------------------------- traces
    traces = list(TRACES_R3)
    contrastes = list(CONTRASTES)
    if args.essai_sur_a5:
        traces = [t for t in traces if t[0] in ("C2", "C3")]
        traces.append(("C3 bis", "a5-C3-p1.jsonl", "C3"))
        contrastes = [("PLACEBO", "C3 bis", "C3", "la meme trace lue deux fois, "
                                                  "l'effet doit etre exactement nul"),
                      ("REFERENCE", "C2", "C3", "le contraste de conditionnement connu, "
                                                "qui n'est PAS une ablation")]

    infos, couverture = {}, []
    for nom, fichier, condition in traces:
        chemin = os.path.join(args.racine_traces, fichier)
        info = matrice_depuis_trace(paquet, chemin, condition, table, colonnes)
        if info is None:
            print(f"  trace absente ou sans personne complete : {chemin}", flush=True)
            controles.append({"controle": f"trace {fichier}", "valeur": 0.0,
                              "reference": 1.0, "detail": "absente ou vide"})
            continue
        paquet["M"][nom] = info["matrice"]
        info["registre"] = registre_modeles(chemin)
        infos[nom] = info
        couverture.append({"condition": nom, "trace": fichier,
                           "personnes_completes": len(info["personnes"]),
                           "personnes_partielles": info["partielles"],
                           "appels_lus": info["appels"], "passes": len(info["passes"]),
                           **(info["registre"] or {})})
        print(f"  {nom} : {len(info['personnes'])} personnes completes sur les 58 items, "
              f"{info['partielles']} partielles, {info['appels']} appels lus, "
              f"registre {info['registre']}", flush=True)

    if not infos:
        raise SystemExit("aucune trace exploitable : rien a evaluer")

    # Controle de lecture : la matrice relue de la trace coincide avec celle que le
    # dossier a deja construite pour la meme condition. Il ne peut pas passer pour C3E,
    # qui n'existe nulle part ailleurs, mais il valide le chemin de lecture sur C2 et C3.
    for nom in ("C2", "C3"):
        if nom in infos and nom in paquet["M"]:
            a = paquet["M"][nom][infos[nom]["lignes"]][:, colonnes]
            controles.append({
                "controle": f"lecture de la trace {nom} coherente",
                "valeur": float(np.mean([v is not None for v in a.ravel()])),
                "reference": 1.0,
                "detail": "part de cellules non vides sur les 58 items apres relecture "
                          "de la trace par le chemin de r3_evaluer"})

    tab, con, rar, couv_c = [], [], [], []
    for nom, avec, sans, _quoi in contrastes:
        if avec not in infos or sans not in infos:
            couv_c.append({"contraste": nom, "avec": avec, "sans": sans,
                           "personnes_communes": 0, "teste": False,
                           "motif": "condition absente ; NON TESTE, jamais non rejete"})
            print(f"\n{nom} : {avec} ou {sans} absent, contraste NON TESTE", flush=True)
            continue
        blocs, blocs_rar, couvc = contraste(nom, avec, sans, paquet, infos, colonnes,
                                            segs, args, controles)
        for b in blocs:
            (con if "mesure" in b else tab).append(b)
        rar += blocs_rar
        couv_c.append(couvc)

    con = pd.DataFrame(con)
    if len(con):
        con["p_holm"] = np.nan
        con["p_bh"] = np.nan
        for nom_f, famille, mesures in (("F1", "H1", FAMILLE_F1),
                                        ("F2", "H2", FAMILLE_F2),
                                        ("F3", "H3a", ["chute permutation S_gra"])):
            bloc = con[(con.contraste == famille) & (con.mesure.isin(mesures))]
            if not len(bloc):
                continue
            p = bloc["p_bootstrap"].to_numpy(dtype=float)
            con.loc[bloc.index, "p_holm"] = C44.holm(p)
            con.loc[bloc.index, "p_bh"] = C44.benjamini_hochberg(p)
            con.loc[bloc.index, "famille"] = nom_f
        controles.append({
            "controle": "correction pour tests multiples",
            "valeur": float(con["p_holm"].notna().sum()), "reference": 11.0,
            "detail": "Holm par famille, F1 (5 tests), F2 (5 tests), F3 (1 test), "
                      "exactement comme la page de plan section 6 ; le reste est "
                      "descriptif et publie sans correction"})

    controles.append({"controle": "tirages du bootstrap apparie",
                      "valeur": float(args.tirages), "reference": 2000.0,
                      "detail": f"{args.tirages_permutation} tirages et "
                                f"{args.permutations_bootstrap} permutations pour la "
                                f"chute ; {args.permutations} permutations pour "
                                f"l'estimation ponctuelle"})

    suf = args.suffixe
    C44.ecrire(pd.DataFrame(couverture), f"r3-couverture{suf}.csv")
    C44.ecrire(pd.DataFrame(couv_c), f"r3-contrastes-couverture{suf}.csv")
    if tab:
        C44.ecrire(pd.DataFrame(tab), f"r3-tableau{suf}.csv")
    if len(con):
        C44.ecrire(con, f"r3-contrastes{suf}.csv")
        perm = con[con.mesure.str.startswith("chute")]
        C44.ecrire(perm, f"r3-permutation{suf}.csv")
    if rar:
        C44.ecrire(pd.DataFrame(rar), f"r3-rarete{suf}.csv")
    C44.ecrire(pd.DataFrame(controles), f"r3-controles{suf}.csv")

    if len(con):
        print("\n### contrastes, effet = avec l'etiquette moins sans")
        cols = ["contraste", "mesure", "sens_predit", "valeur_avec", "valeur_sans",
                "effet", "ic_bas", "ic_haut", "p_bootstrap", "p_holm"]
        print(con[cols].to_string(index=False,
                                  float_format=lambda v: f"{v:.4f}"))
    print(f"\nduree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
