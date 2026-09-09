"""
r2_evaluer : evaluation de R2, la comparaison appariee sur les gens rares en regime severe.

Verrou 1 de MODELE-DU-MONDE.md section 10.5. La famille d'hypotheses, les seuils, les
planchers et les criteres de chute sont ecrits dans resultats/r2-preenregistrement.md,
HORODATE DU 8 SEPTEMBRE 2026 A 22:05:00 CEST, AVANT LE MOINDRE APPEL DE MODELE DE LANGAGE.
Ce fichier n'est pas modifie ensuite. Rappel de la famille, pour que le script en porte
lui aussi la trace :

  F1 primaire     7 tests  H1a exces de rappel sur le plancher de SEGMENT, raretes
                           STABLES des 58 items de famille, dirige ;
                           H1b avantage de rappel sur chacune des 6 methodes du regime
                           severe, memes cellules, dirige.
  F2 secondaire   7 tests  H2a et H2b, les memes contrastes sur la PRECISION.
  F3 tertiaire    7 tests  H3a exactitude par personne contre les 6 methodes severes,
                           bilateral ; H3b contre C3F Qwen3-4B sur les personnes
                           communes, bilateral.
  F4 quaternaire  8 tests  H4a diversite conservee contre les 4 methodes a TIRAGE ;
                           H4b ecart absolu a 1 du ratio intra contre les memes,
                           bilateral. H4c chute sous permutation intra camp, descriptif.

  Familles corrigees SEPAREMENT par Holm, Benjamini Hochberg rapporte a cote. Tous les p
  sont des p de bootstrap APPARIE SUR LES PERSONNES, memes tirages pour toutes les
  methodes, plancher a 1 sur le nombre de tirages. Un contraste a denominateur vide
  recoit p = 1, convention conservatrice de a29, a31, a34 et a42.

Zero appel de modele de langage : ce script ne fait que relire des traces. Lecture seule
sur data/. AUCUN SCRIPT EXISTANT N'EST MODIFIE. Sont importes tels quels :

  a41_commun      les six methodes du regime severe, par construire_severe(), qui appelle
                  a35_familles.imputer_par_famille et a33_commun.b2_famille_retiree ; les
                  versions vectorisees de la dispersion, de l'entropie et de l'accord ;
                  le bootstrap sur les personnes ; les contrastes.
  a42_commun      la partition P_A, c'est a dire la stabilite en vague 2, et mesure_sur(),
                  qui donne rappel, precision et exces sur plancher par personne.
  a34_commun      le plancher de bruit de cellule, frequence_segment(), et le segment
                  ideologie x genre x age.
  a35_commun      exactitude(), diversite(), sommes_dispersion().
  a28_commun      le codage des matrices et les segmentations de a1.
  a44_commun      permuter_intra(), pour la chute sous permutation intra camp.
  a5_evaluer      moyenner_passes() et en_matrices(), pour lire les traces JSONL sans en
                  reecrire le format.

Ce que ce script ajoute et qui n'existe nulle part ailleurs : le croisement des deux
instruments. a42 mesure les raretes STABLES sur les 149 items, hors regime severe. a41
mesure le regime severe sur les 58 items de famille, toutes raretes confondues. La case
"raretes stables x 58 items de famille x regime severe" n'est dans aucun fichier de
resultats/, et c'est la case du verrou 1.

Tolerance au partiel : le run de nuit peut etre tronque a 08:00. Chaque condition est
evaluee sur SES personnes completes, c'est a dire celles dont les 58 cellules sont dans
la trace, et la couverture est ecrite en tete de chaque tableau. Les methodes
statistiques sont restreintes aux memes personnes, ce qui est tout l'objet du rapport.

Entree  : data/traces/r2-C3F-<modele>.jsonl, r2-C3-<modele>.jsonl, a5-C3F-p1.jsonl,
          caches /tmp/a25-matrices.pkl, /tmp/a28-foret.npy, /tmp/a35-methodes.pkl,
          /tmp/a41-severe.pkl.
Sortie  : resultats/r2-couverture.csv, r2-tableau.csv, r2-contrastes.csv,
          r2-permutation.csv, r2-controles.csv.

Usage :
  .venv/bin/python analyses/r2_evaluer.py --tirages 4000
  .venv/bin/python analyses/r2_evaluer.py --essai-sur-a5   (test hors ligne, trace a5)
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
import a41_commun as C41
import a42_commun as C42
import a44_commun as C44
from a5_agents_locaux_gss import TRACES, nomenclature
from a5_evaluer import en_matrices, moyenner_passes

SORTIE = C41.SORTIE
SEUIL = 0.10

# Dossier ou les traces sont lues. Il est un drapeau, --racine-traces, pour qu'un essai
# sur une trace synthetique ne puisse jamais ecrire ni lire dans data/traces et polluer
# l'index de reprise du run de nuit.
DOSSIER_TRACES = TRACES

# Les six methodes du regime severe, telles que a41 les nomme. Ce sont les seules
# methodes du dossier qui perdent la famille thematique entiere de leur contexte, donc
# les seules qui puissent etre comparees a C3F sans que la comparaison soit biaisee.
SEVERE = list(C41.SEVERE)

# Les quatre methodes a TIRAGE du regime severe. a41 section 7 : c'est le seul adversaire
# qui compte, une methode d'esperance etant le cas d'ecole de l'ecrasement chez van
# Buuren. H4 ne porte que sur elles.
TIRAGE = ["E2 famille retiree (tirage)", "PMM k=10 famille retiree",
          "B2 famille retiree (tirage)"]

# Reperes affiches, jamais testes : ils ne sont pas dans le regime severe, ou ils sont
# une identite.
REPERES = ["humains vague 2", "B3 foret", "B0 mode", "B0 tirage", "B1 argmax"]

# Traces lues. Le nom de condition porte le modele : deux modeles sur la meme condition
# ne doivent jamais se retrouver dans la meme colonne.
TRACES_R2 = [
    ("C3F gpt-oss-20b", "r2-C3F-gptoss.jsonl", "C3F"),
    ("C3 gpt-oss-20b", "r2-C3-gptoss.jsonl", "C3"),
    ("C3F Qwen3-30B", "r2-C3F-qwen30.jsonl", "C3F"),
    ("C3 Qwen3-30B", "r2-C3-qwen30.jsonl", "C3"),
    ("C3F Qwen3-4B", "a5-C3F-p1.jsonl", "C3F"),
]


# ---------------------------------------------------------------------------
# 1. Lecture des traces, sans reecrire le format de a5
# ---------------------------------------------------------------------------

def lire_trace(chemin):
    """Charge une trace JSONL, indexee par (condition, passe) comme a5_evaluer.

    Les doublons sont ecrases par la derniere occurrence : une relance apres arret
    brutal peut reecrire la ligne coupee en deux. La cle est (pid, item), celle de
    l'index unique du run. Les lignes tronquees sont ignorees sans faire echouer la
    lecture.
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


def matrice_depuis_trace(paquet, chemin, condition, table_nomenclature, n_items_cible):
    """Matrice 1 052 x 149, None hors des cellules effectivement predites.

    Meme construction que a33_commun.matrice_c3f, generalisee au nom de fichier et a la
    condition, parce que a33 lit `a5-C*-p*.jsonl` par glob et ne verrait pas nos traces.
    Renvoie aussi les personnes COMPLETES, c'est a dire celles dont les n_items_cible
    cellules sont presentes, et le compte des partielles.
    """
    ids, items = paquet["ids"], paquet["items"]
    index_personne = {p: i for i, p in enumerate(ids)}
    tables = lire_trace(chemin)
    cles = [(c, p) for (c, p) in tables if c == condition]
    if not cles:
        return None
    compte = defaultdict(int)
    for (c, p) in cles:
        for (pid, _it) in tables[(c, p)]:
            compte[pid] += 1
    n_vus = len({it for (c, p) in cles for (_pid, it) in tables[(c, p)]})
    n_passes = len(cles)
    complets = [pid for pid, n in compte.items() if n >= n_items_cible * n_passes]

    ech = pd.read_csv(os.path.join(TRACES, "a5-personnes.csv"))
    personnes = [p for p in ech["pid"] if p in set(complets)]
    if not personnes:
        return None
    fusion, passes = moyenner_passes(tables, condition)
    pred, dist = en_matrices(fusion, personnes, items, table_nomenclature)

    plein = np.empty((len(ids), len(items)), dtype=object)
    plein[:] = None
    lignes = [index_personne[p] for p in personnes]
    plein[np.ix_(lignes, list(range(len(items))))] = pred
    return {"matrice": plein, "personnes": personnes, "lignes": np.array(lignes),
            "partielles": len(compte) - len(complets), "items_vus": n_vus,
            "passes": passes, "appels": sum(len(tables[c]) for c in cles),
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
# 2. Preparation d'un perimetre
# ---------------------------------------------------------------------------

def references_population(paquet):
    """Planchers et scores, calcules UNE FOIS sur les 1 052 humains de la vague 1.

    Regle de a34 reprise par a42 : ce sont des descripteurs de population. Les
    recalculer sur 60 ou 150 personnes donnerait des cases de segment d'une ou deux
    personnes, et le plancher deviendrait du bruit.
    """
    y1, y2, x = paquet["y1"], paquet["y2"], paquet["x"]
    ok_tot = C42.observe(y1)
    seg_fin, niveaux = C42.segment_fin(x, paquet["attributs"])
    return {
        "ok_tot": ok_tot, "n_segments": len(niveaux),
        "d_item": C42.frequence_item(y1, y1, ok_tot),
        "d_seg": C42.frequence_segment(y1, y1, ok_tot, seg_fin),
        "h2": C42.rappel_vague2(y1, y2),
    }


def preparer(paquet, lignes, refs, definition_mods="perimetre"):
    """Masques, partition P_A et planchers pour un perimetre de personnes.

    definition_mods : "perimetre" applique le seuil de 10 pour cent aux personnes du
    perimetre, ce que fait a42 ; "population" l'applique aux 1 052, ce que fait a41. Les
    deux sont calculees et publiees, parce qu'elles ne donnent pas le meme ensemble de
    cellules quand le perimetre est petit, et qu'aucune des deux n'est plus juste que
    l'autre : l'une definit la rarete dans l'echantillon mesure, l'autre dans la
    population de reference.
    """
    y1 = paquet["y1"][lignes]
    y2 = paquet["y2"][lignes]
    if definition_mods == "perimetre":
        mods = C42.modalites_rares(y1, SEUIL)
    else:
        mods = C42.modalites_rares(paquet["y1"], SEUIL)
    ok = C42.observe(y1)
    rare_vrai = C42.appartient(y1, mods) & ok
    stab = C42.classes_stabilite(y1, y2)
    planchers = {"item": refs["d_item"][lignes],
                 "segment": refs["d_seg"][lignes],
                 "humains vague 2": refs["h2"][lignes]}
    return {"lignes": lignes, "y1": y1, "y2": y2, "mods": mods, "ok": ok,
            "rare_vrai": rare_vrai, "stab": stab, "planchers": planchers}


def restreindre(masque, colonnes):
    """Masque booleen mis a zero hors des colonnes retenues.

    C'est ainsi que le perimetre d'items entre dans les mesures : les definitions de
    rarete et de stabilite restent celles de a42, calculees sur tous les items, et seule
    la selection des cellules jugees change. Restreindre les matrices elles memes
    changerait le seuil de rarete, ce qui n'est pas ce que la page de plan declare.
    """
    out = np.zeros_like(masque, dtype=bool)
    out[:, colonnes] = masque[:, colonnes]
    return out


# ---------------------------------------------------------------------------
# 3. Mesures d'une methode sur un perimetre
# ---------------------------------------------------------------------------

def mesures_rares(pred, prep, colonnes, classe):
    """Rappel, precision et exces sur les trois planchers, sur une classe de P_A.

    classe : "stable", "instable" ou "ensemble". Les couples (numerateur, denominateur)
    par personne sont ceux de a42_commun.mesure_sur, ce qui rend tous les contrastes
    apparies : le meme tirage de personnes sert a toutes les methodes.
    """
    m = C42.masques(pred, prep["y1"], prep["mods"])
    sel = {"stable": prep["stab"] == 1, "instable": prep["stab"] == 0,
           "ensemble": np.ones_like(prep["stab"], dtype=bool)}[classe]
    selv = restreindre(prep["rare_vrai"] & sel, colonnes)
    selp = restreindre(m["rare_pred"] & sel, colonnes)
    juste = restreindre(m["juste"], colonnes)
    return C42.mesure_sur(selv, selp, juste, prep["planchers"])


def mesures_structure(paquet, nom, lignes, colonnes, codes_nom, codes_lib, seg,
                      k_max_nom, k_max_lib):
    """Exactitude par personne, diversite conservee, accord, ratios intra et inter."""
    y1 = paquet["y1"]
    mat = y1 if nom == "_humains" else paquet["M"][nom]
    acc = C41.exactitude(mat, y1, lignes, colonnes)
    s = C41.sommes_dispersion_rapide(codes_nom[nom], seg, k_max_nom, colonnes)
    h = C41.sommes_dispersion_rapide(codes_nom["_humains"], seg, k_max_nom, colonnes)
    hh, _ = C41.entropie_accord_rapide(codes_lib["_humains"], colonnes, k_max_lib)
    hp, ap = C41.entropie_accord_rapide(codes_lib[nom], colonnes, k_max_lib)
    div, acp = C41.diversite_rapide(hp, ap, hh)
    return {"acc": acc,
            "exactitude": float(np.nanmean(acc)),
            "diversite": div, "accord": acp,
            "intra": s["intra"] / h["intra"] if h["intra"] else np.nan,
            "inter": s["inter"] / h["inter"] if h["inter"] else np.nan}


def bootstrap_structure(paquet, methodes, lignes, colonnes, codes_nom, codes_lib, seg,
                        k_max_nom, k_max_lib, idx_boot, accs, pas=250):
    """Distributions bootstrap de l'exactitude, de la diversite et des ratios.

    Meme forme que a41_commun.bootstrap_quantites : pour chaque tirage de personnes,
    toutes les quantites sont recalculees pour toutes les methodes sur le MEME tirage.
    C'est ce qui rend les contrastes apparies.
    """
    ch_nom = codes_nom["_humains"]
    ch_lib = codes_lib["_humains"]
    cles = ["exactitude", "intra", "inter", "diversite", "accord"]
    dist = {nom: {c: np.empty(len(idx_boot)) for c in cles} for nom in methodes}
    for t, idx in enumerate(idx_boot):
        h = C41.sommes_dispersion_rapide(ch_nom[idx], seg[idx], k_max_nom, colonnes)
        hh, _ = C41.entropie_accord_rapide(ch_lib[idx], colonnes, k_max_lib)
        for nom in methodes:
            s = C41.sommes_dispersion_rapide(codes_nom[nom][idx], seg[idx], k_max_nom,
                                             colonnes)
            hp, ap = C41.entropie_accord_rapide(codes_lib[nom][idx], colonnes, k_max_lib)
            div, acp = C41.diversite_rapide(hp, ap, hh)
            d = dist[nom]
            d["exactitude"][t] = np.nanmean(accs[nom][idx])
            d["intra"][t] = s["intra"] / h["intra"] if h["intra"] else np.nan
            d["inter"][t] = s["inter"] / h["inter"] if h["inter"] else np.nan
            d["diversite"][t] = div
            d["accord"][t] = acp
        if pas and (t + 1) % pas == 0:
            print(f"    bootstrap structure {t + 1}/{len(idx_boot)}", flush=True)
    return dist


# ---------------------------------------------------------------------------
# 4. H4c, la chute sous permutation intra camp
# ---------------------------------------------------------------------------

def segmentations_permutation(paquet):
    """Les segmentations sous lesquelles la permutation intra groupe est mesuree.

    S_fin et S_ideo sont exactement celles de a44_mesures, importees de
    a44_commun.segmentations : bloc d'ideologie x genre x age, et les sept niveaux bruts
    d'ideologie. S_camp est le camp a trois niveaux, gauche, droite, centre, annonce dans
    la page de plan ; c'est la regle mecanique de a1 appliquee par a44_commun sur le
    libelle, et elle est ajoutee parce que sur 60 a 150 personnes les deux premieres
    donnent des groupes trop petits pour que la permutation veuille dire quelque chose.
    """
    seg, _niveaux = C44.segmentations(paquet)
    col = {a: i for i, a in enumerate(paquet["attributs"])}
    brut = [C28.norm(v) for v in paquet["x"][:, col["political_ideology"]]]
    camps = [C44._bloc_ideologie(v) for v in brut]
    mods = sorted(set(camps))
    idx = {m: k for k, m in enumerate(mods)}
    return {"S_fin": seg["S_fin"], "S_ideo": seg["S_ideo"],
            "S_camp": np.array([idx[v] for v in camps], dtype=np.int32)}


def chute_permutation(paquet, nom, lignes, colonnes, seg_camp, n_permutations, rng,
                      n_min_camp=10):
    """Exactitude perdue quand on permute les personnes a l'interieur de leur camp.

    Quantite de a44 section 5, transposee au perimetre de R2. Si un agent est un gabarit
    de groupe, les reponses sont echangeables entre personnes du meme camp et
    l'exactitude ne bouge pas ; s'il porte la personne, elle chute.

    Declaree DESCRIPTIVE dans la page de plan, et non calculable sous n_min_camp
    personnes par groupe : sur un perimetre de 60 personnes, un groupe de moins de dix
    individus rend la permutation presque l'identite et la chute mesuree serait un
    artefact de taille. Renvoie NaN dans ce cas, jamais zero.
    """
    mat = paquet["y1"] if nom == "_humains" else paquet["M"][nom]
    pred = mat[np.ix_(lignes, colonnes)]
    verite = paquet["y1"][np.ix_(lignes, colonnes)]
    seg = seg_camp[lignes]
    tailles = [int((seg == k).sum()) for k in np.unique(seg) if k >= 0]
    if not tailles or max(tailles) < n_min_camp:
        return {"exactitude": np.nan, "exactitude_permutee": np.nan, "chute": np.nan,
                "chute_relative": np.nan, "camps_exploitables": 0,
                "taille_camp_max": max(tailles) if tailles else 0}
    base = float(np.nanmean(C44.exactitude(pred, verite)))
    tirs = []
    for _ in range(n_permutations):
        perm = C44.permuter_intra(len(lignes), seg, rng)
        tirs.append(float(np.nanmean(C44.exactitude(pred[perm], verite))))
    permutee = float(np.mean(tirs))
    return {"exactitude": base, "exactitude_permutee": permutee,
            "chute": base - permutee,
            "chute_relative": (base - permutee) / base if base else np.nan,
            "camps_exploitables": int(sum(1 for t in tailles if t >= n_min_camp)),
            "taille_camp_max": max(tailles)}


# ---------------------------------------------------------------------------
# 5. Le corps de l'evaluation
# ---------------------------------------------------------------------------

def evaluer_condition(paquet, refs, nom_llm, info, colonnes, args, controles,
                      definition_mods="perimetre"):
    """Toutes les mesures et tous les contrastes pour une condition de modele de langage.

    Les methodes statistiques sont restreintes aux personnes de CETTE condition : c'est
    tout l'objet de R2, et c'est ce que a41 section 5 appelle la comparaison appariee.
    """
    lignes = info["lignes"]
    n = len(lignes)
    print(f"\n=== {nom_llm} : {n} personnes completes, {len(colonnes)} items, "
          f"definition des raretes sur le {definition_mods} ===", flush=True)

    prep = preparer(paquet, lignes, refs, definition_mods)
    methodes = [nom_llm] + [m for m in SEVERE if m in paquet["M"]] \
        + [m for m in REPERES if m in paquet["M"]]
    absentes = [m for m in SEVERE + REPERES if m not in paquet["M"]]
    if absentes:
        controles.append({"controle": f"methodes absentes du paquet, {nom_llm}",
                          "valeur": float(len(absentes)), "reference": 0.0,
                          "detail": ", ".join(absentes)})

    items, options = paquet["items"], paquet["options"]
    seg_tous, _ = C28.segments(paquet["x"], paquet["attributs"])
    seg = seg_tous[C41.AXE_PRINCIPAL][lignes]
    k_items = [len(options[it]) for it in items]
    k_max_nom = max(k_items)

    codes_nom = {"_humains": C28.coder(paquet["y1"], lignes, items, options)}
    for nom in methodes:
        codes_nom[nom] = C28.coder(paquet["M"][nom], lignes, items, options)
    brut = {"_humains": paquet["y1"][lignes]}
    brut.update({nom: paquet["M"][nom][lignes] for nom in methodes})
    codes_lib, k_max_lib = C41.codes_libres(brut, colonnes)

    # ------------------------------------------------------------------ mesures
    rng = np.random.default_rng(C41.GRAINE_A41)
    idx_boot = C41.tirages(n, args.tirages, rng)

    struct, accs, rares = {}, {}, {}
    for nom in methodes:
        s = mesures_structure(paquet, nom, lignes, colonnes, codes_nom, codes_lib, seg,
                              k_max_nom, k_max_lib)
        accs[nom] = s.pop("acc")
        struct[nom] = s
        rares[nom] = {c: mesures_rares(paquet["M"][nom][lignes], prep, colonnes, c)
                      for c in ("stable", "instable", "ensemble")}

    dist = bootstrap_structure(paquet, methodes, lignes, colonnes, codes_nom, codes_lib,
                               seg, k_max_nom, k_max_lib, idx_boot, accs)

    # ------------------------------------------------------------------ tableau
    lignes_tab = []
    for nom in methodes:
        r = rares[nom]["stable"]
        e = rares[nom]["ensemble"]
        v_rap, lo_rap, hi_rap, _ = C42.taux_ic(r["_rappel"][0], r["_rappel"][1], idx_boot)
        v_pre, lo_pre, hi_pre, _ = C42.taux_ic(r["_precision"][0], r["_precision"][1],
                                               idx_boot)
        v_exc, lo_exc, hi_exc, tir = C42.taux_ic(r["_exces_segment"][0],
                                                 r["_exces_segment"][1], idx_boot)
        lignes_tab.append({
            "condition_llm": nom_llm, "definition_raretes": definition_mods,
            "personnes": n, "items": len(colonnes), "methode": nom,
            "regime_severe": C41.FAMILLE_RETIREE.get(nom, "voir a41"),
            "conditionnement": C41.CONDITIONNEMENT.get(nom, ""),
            "exactitude": struct[nom]["exactitude"],
            "exactitude_ic_bas": float(np.percentile(dist[nom]["exactitude"], 2.5)),
            "exactitude_ic_haut": float(np.percentile(dist[nom]["exactitude"], 97.5)),
            "diversite_conservee": struct[nom]["diversite"],
            "accord_par_paires": struct[nom]["accord"],
            "ratio_intra": struct[nom]["intra"], "ratio_inter": struct[nom]["inter"],
            "cellules_rares_stables": r["cellules"],
            "raretes_stables_osees": r["raretes_osees"],
            "rappel_stables": v_rap, "rappel_stables_ic_bas": lo_rap,
            "rappel_stables_ic_haut": hi_rap,
            "precision_stables": v_pre, "precision_stables_ic_bas": lo_pre,
            "precision_stables_ic_haut": hi_pre,
            "f1_stables": r["f1"],
            "plancher_segment": r["plancher_segment"],
            "exces_segment_stables": v_exc, "exces_segment_ic_bas": lo_exc,
            "exces_segment_ic_haut": hi_exc,
            "exces_segment_p": C42.p_contre_zero(tir),
            "rappel_instables": rares[nom]["instable"]["rappel"],
            "rappel_ensemble": e["rappel"], "cellules_rares_ensemble": e["cellules"],
        })

    # ------------------------------------------------------------------ contrastes
    contrastes = []

    def ajouter(famille, hypothese, adversaire, quantite, d, lo, hi, p, signe):
        contrastes.append({
            "condition_llm": nom_llm, "definition_raretes": definition_mods,
            "personnes": n, "famille": famille, "hypothese": hypothese,
            "adversaire": adversaire, "quantite": quantite,
            "difference_llm_moins_adversaire": d, "ic_bas": lo, "ic_haut": hi,
            "p_bootstrap": p, "signe_attendu": signe})

    # F1 : le rappel des raretes stables
    r_llm = rares[nom_llm]["stable"]
    d, lo, hi, p = C42.valeur_ic_p(r_llm["_exces_segment"], idx_boot)
    ajouter("F1 primaire", "H1a", "plancher de segment", "exces de rappel, stables",
            d, lo, hi, p, "positif")
    for adv in [m for m in SEVERE if m in paquet["M"]]:
        ra = rares[adv]["stable"]
        d, lo, hi, p = C42.contraste(r_llm["_rappel"][0], r_llm["_rappel"][1],
                                     ra["_rappel"][0], ra["_rappel"][1], idx_boot)
        ajouter("F1 primaire", "H1b", adv, "rappel, raretes stables", d, lo, hi, p,
                "positif")

    # F2 : la precision.
    # H2a est mesuree comme un exces sur le plancher de segment restreint aux cellules
    # OSEES par la methode : c'est la precision qu'obtiendrait un tirage dans le segment
    # sur exactement les memes cellules. mesure_sur() ne la fournit pas, parce que a42 ne
    # teste que le rappel ; elle est construite ici avec les memes briques.
    num_pl, den_pl = C42.moyenne_par_personne(
        restreindre(C42.masques(paquet["M"][nom_llm][lignes], prep["y1"],
                                prep["mods"])["rare_pred"] & (prep["stab"] == 1),
                    colonnes),
        prep["planchers"]["segment"])
    d, lo, hi, p = C42.contraste(r_llm["_precision"][0], r_llm["_precision"][1],
                                 num_pl, den_pl, idx_boot)
    ajouter("F2 secondaire", "H2a", "plancher de segment sur les cellules osees",
            "precision, raretes stables", d, lo, hi, p, "positif")
    for adv in [m for m in SEVERE if m in paquet["M"]]:
        ra = rares[adv]["stable"]
        d, lo, hi, p = C42.contraste(r_llm["_precision"][0], r_llm["_precision"][1],
                                     ra["_precision"][0], ra["_precision"][1], idx_boot)
        ajouter("F2 secondaire", "H2b", adv, "precision, raretes stables", d, lo, hi, p,
                "positif")

    # F3 : l'exactitude
    for adv in [m for m in SEVERE if m in paquet["M"]]:
        d, lo, hi, p = C41.contraste(dist, nom_llm, adv, "exactitude")
        ajouter("F3 tertiaire", "H3a", adv, "exactitude par personne", d, lo, hi, p,
                "bilateral")

    # F4 : la structure
    for adv in [m for m in TIRAGE if m in paquet["M"]]:
        d, lo, hi, p = C41.contraste(dist, nom_llm, adv, "diversite")
        ajouter("F4 quaternaire", "H4a", adv, "diversite conservee", d, lo, hi, p,
                "bilateral")
    for adv in [m for m in TIRAGE if m in paquet["M"]]:
        d, lo, hi, p = C41.contraste_proximite(dist, nom_llm, adv, "intra")
        ajouter("F4 quaternaire", "H4b", adv, "ecart absolu a 1 du ratio intra",
                d, lo, hi, p, "bilateral, negatif = plus proche de 1")

    return lignes_tab, contrastes, {"dist": dist, "rares": rares, "prep": prep,
                                    "idx_boot": idx_boot, "methodes": methodes,
                                    "lignes": lignes, "accs": accs}


# ---------------------------------------------------------------------------
# 6. H3b, les conditions de modele de langage comparees entre elles
# ---------------------------------------------------------------------------

def contrastes_croises(paquet, refs, presentes, colonnes, args, n_min=10):
    """Comparaisons appariees entre conditions de modele de langage.

    Restreintes aux PERSONNES COMMUNES aux deux conditions, sur les memes 58 items :
    c'est la seule facon de comparer deux modeles ou deux regimes sans melanger un effet
    de methode et un effet d'echantillon. Deux quantites, l'exactitude par personne et le
    rappel des raretes stables. Sous n_min personnes communes, le couple est declare non
    evaluable et n'est pas ecrit.
    """
    out = []
    for i, (nom_a, info_a) in enumerate(presentes):
        for nom_b, info_b in presentes[i + 1:]:
            communes = np.array(sorted(set(info_a["lignes"].tolist())
                                       & set(info_b["lignes"].tolist())))
            if len(communes) < n_min:
                continue
            prep = preparer(paquet, communes, refs, "perimetre")
            rng = np.random.default_rng(C41.GRAINE_A41)
            idx = C41.tirages(len(communes), args.tirages, rng)
            acc_a = C41.exactitude(paquet["M"][nom_a], paquet["y1"], communes, colonnes)
            acc_b = C41.exactitude(paquet["M"][nom_b], paquet["y1"], communes, colonnes)
            d_tir = np.array([np.nanmean(acc_a[k]) - np.nanmean(acc_b[k]) for k in idx])
            d_tir = d_tir[~np.isnan(d_tir)]
            out.append({
                "condition_a": nom_a, "condition_b": nom_b,
                "personnes_communes": len(communes), "quantite": "exactitude",
                "difference_a_moins_b": float(np.nanmean(acc_a) - np.nanmean(acc_b)),
                "ic_bas": float(np.percentile(d_tir, 2.5)) if len(d_tir) else np.nan,
                "ic_haut": float(np.percentile(d_tir, 97.5)) if len(d_tir) else np.nan,
                "p_bootstrap": C42.p_contre_zero(d_tir) if len(d_tir) else 1.0})
            ra = mesures_rares(paquet["M"][nom_a][communes], prep, colonnes, "stable")
            rb = mesures_rares(paquet["M"][nom_b][communes], prep, colonnes, "stable")
            d, lo, hi, p = C42.contraste(ra["_rappel"][0], ra["_rappel"][1],
                                         rb["_rappel"][0], rb["_rappel"][1], idx)
            out.append({
                "condition_a": nom_a, "condition_b": nom_b,
                "personnes_communes": len(communes),
                "quantite": "rappel des raretes stables",
                "difference_a_moins_b": d, "ic_bas": lo, "ic_haut": hi,
                "p_bootstrap": p, "cellules_rares_stables": ra["cellules"]})
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--cache-a41", default="/tmp/a41-severe.pkl")
    ap.add_argument("--tirages", type=int, default=4000)
    ap.add_argument("--permutations", type=int, default=200)
    ap.add_argument("--essai-sur-a5", action="store_true",
                    help="test hors ligne : n'evalue que la trace C3F Qwen3-4B de a5, "
                         "avec peu de tirages, pour verifier le script sans le run")
    ap.add_argument("--suffixe", default="", help="suffixe des fichiers de sortie")
    ap.add_argument("--racine-traces", default=TRACES,
                    help="dossier des traces ; sert aux essais sur trace synthetique")
    args = ap.parse_args()

    global DOSSIER_TRACES
    DOSSIER_TRACES = args.racine_traces

    if args.essai_sur_a5:
        args.tirages = min(args.tirages, 400)
        args.permutations = min(args.permutations, 50)

    t0 = time.time()
    controles = []

    # ------------------------------------------------------------------ chargement
    print("chargement du paquet et des six methodes du regime severe")
    paquet = C41.charger_paquet(args.cache, args.cache_foret, args.cache_a35)
    C41.construire_severe(paquet, cache=args.cache_a41)
    colonnes, familles = C41.colonnes_familles(paquet["items"])
    print(f"{len(familles)} familles, {len(colonnes)} items, "
          f"{len(paquet['ids'])} personnes dans le paquet")

    manquantes = [m for m in SEVERE if m not in paquet["M"]]
    controles.append({"controle": "methodes du regime severe importables",
                      "valeur": float(len(SEVERE) - len(manquantes)),
                      "reference": float(len(SEVERE)),
                      "detail": ", ".join(manquantes) if manquantes
                      else "les six sont importables de a35_familles et a33_commun"})
    controles.append({
        "controle": "ce qui n'est PAS importable dans le regime severe",
        "valeur": 6.0, "reference": 6.0,
        "detail": "les six conditions de Stanford gardent les items cousins dans leur "
                  "invite (a8 errata E1) ; elles ne peuvent pas etre replacees en regime "
                  "severe sans relancer leur pipeline, et ne sont donc ni testees ni "
                  "affichees comme adversaires"})

    refs = references_population(paquet)
    controles.append({"controle": "cases du segment ideologie x genre x age",
                      "valeur": float(refs["n_segments"]), "reference": 98.0,
                      "detail": "plancher de bruit de cellule de a34, importe"})

    table_nomenclature = nomenclature()

    # ------------------------------------------------------------------ traces
    presentes = []
    for nom_llm, fichier, condition in TRACES_R2:
        if args.essai_sur_a5 and nom_llm != "C3F Qwen3-4B":
            continue
        chemin = os.path.join(DOSSIER_TRACES, fichier)
        info = matrice_depuis_trace(paquet, chemin, condition, table_nomenclature,
                                    len(colonnes))
        if info is None:
            controles.append({"controle": f"trace {fichier}", "valeur": 0.0,
                              "reference": 1.0,
                              "detail": "absente ou sans personne complete"})
            print(f"  trace absente ou vide : {chemin}")
            continue
        paquet["M"][nom_llm] = info["matrice"]
        info["registre"] = registre_modeles(chemin)
        presentes.append((nom_llm, info))
        print(f"  {nom_llm} : {len(info['personnes'])} personnes completes, "
              f"{info['partielles']} partielles, {info['appels']} appels, "
              f"{info['items_vus']} items, registre {info['registre']}")

    if not presentes:
        raise SystemExit("aucune trace exploitable : rien a evaluer")

    couverture = []
    for nom_llm, info in presentes:
        couverture.append({
            "condition": nom_llm, "trace": os.path.basename(info["chemin"]),
            "personnes_completes": len(info["personnes"]),
            "personnes_partielles": info["partielles"],
            "appels_lus": info["appels"], "items_distincts": info["items_vus"],
            "passes": len(info["passes"]),
            **{k: v for k, v in (info["registre"] or {}).items()}})
    C41.ecrire(pd.DataFrame(couverture), f"r2-couverture{args.suffixe}.csv")

    # ------------------------------------------------------------------ evaluation
    tab, con = [], []
    for nom_llm, info in presentes:
        for definition in ("perimetre", "population"):
            t, c, _ctx = evaluer_condition(paquet, refs, nom_llm, info, colonnes, args,
                                           controles, definition)
            tab += t
            con += c

    tab = pd.DataFrame(tab)
    con = pd.DataFrame(con)

    # ------------------------------------------- correction par famille, Holm et BH
    con["p_holm"] = np.nan
    con["p_bh"] = np.nan
    primaire = con["definition_raretes"] == "perimetre"
    for (cond, fam), bloc in con[primaire].groupby(["condition_llm", "famille"]):
        p = bloc["p_bootstrap"].to_numpy(dtype=float)
        con.loc[bloc.index, "p_holm"] = C41.holm(p)
        con.loc[bloc.index, "p_bh"] = C41.benjamini_hochberg(p)
    controles.append({
        "controle": "correction pour tests multiples",
        "valeur": float(primaire.sum()), "reference": float(primaire.sum()),
        "detail": "Holm et Benjamini Hochberg appliques famille par famille sur la "
                  "definition de rarete du perimetre, qui est la definition declaree ; "
                  "la definition sur population est publiee sans correction, comme "
                  "sensibilite"})

    # ------------------------------------------- H3b, les modeles entre eux
    croises = contrastes_croises(paquet, refs, presentes, colonnes, args)
    if len(croises):
        C41.ecrire(croises, f"r2-croises{args.suffixe}.csv")

    # ------------------------------------------- H4c, la chute sous permutation
    perm = []
    segs = segmentations_permutation(paquet)
    rng = np.random.default_rng(C41.GRAINE_A41)
    for nom_llm, info in presentes:
        lignes = info["lignes"]
        for nom_seg, seg_camp in segs.items():
            for nom in [nom_llm] + [m for m in SEVERE if m in paquet["M"]] + \
                    ["humains vague 2"]:
                r = chute_permutation(paquet, nom, lignes, colonnes, seg_camp,
                                      args.permutations, rng)
                perm.append({"condition_llm": nom_llm, "personnes": len(lignes),
                             "segmentation": nom_seg, "methode": nom, **r})
    perm = pd.DataFrame(perm)

    C41.ecrire(tab, f"r2-tableau{args.suffixe}.csv")
    C41.ecrire(con, f"r2-contrastes{args.suffixe}.csv")
    C41.ecrire(perm, f"r2-permutation{args.suffixe}.csv")
    C41.ecrire(pd.DataFrame(controles), f"r2-controles{args.suffixe}.csv")

    # ------------------------------------------------------------------ lecture
    for nom_llm, _info in presentes:
        sous = tab[(tab.condition_llm == nom_llm)
                   & (tab.definition_raretes == "perimetre")]
        print(f"\n### {nom_llm}, raretes stables des {len(colonnes)} items de famille")
        print(sous[["methode", "exactitude", "rappel_stables", "precision_stables",
                    "plancher_segment", "exces_segment_stables", "diversite_conservee",
                    "ratio_intra", "cellules_rares_stables"]]
              .to_string(index=False, float_format=lambda v: f"{v:.4f}"))
        cs = con[(con.condition_llm == nom_llm)
                 & (con.definition_raretes == "perimetre")]
        print(f"\n### {nom_llm}, contrastes")
        print(cs[["famille", "hypothese", "adversaire",
                  "difference_llm_moins_adversaire", "ic_bas", "ic_haut", "p_holm"]]
              .to_string(index=False, float_format=lambda v: f"{v:.4f}"))

    print(f"\nduree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
