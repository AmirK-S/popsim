"""
a34_deductibilite : l'avantage des modeles de langage sur les gens rares disparait il
quand la rarete est DEDUCTIBLE de l'etiquette ?

C'est le test 4 de la section (d) de `corpus/lecture-complete/03-baselines-statistiques-
extension-enquete.md`, designe la comme "le seul du lot qui peut faire tomber le rang 1
revise". Il oppose a28 section 3.4, a29 et a31 (les agents retrouvent 22 a 31 pour cent
des reponses rares, la regression 5,8, la foret 1,4) a von der Heyde, Haensch et Wenz 2025
(T03-34 : sur le vote allemand l'ecart entre la statistique et le modele de langage se
CREUSE quand la categorie se rarefie).

Zero appel de modele de langage. Lecture seule sur data/. Quatre coeurs. Aucun script
existant n'est modifie : a34_commun, et par lui a31_commun, a29_commun, a28_commun,
a25_commun, a25_mesures, a8_commun, a2_commun, a2_baselines_gss, a5_evaluer et
a5_agents_locaux_gss, sont importes tels quels.

===========================================================================
LA FAMILLE D'HYPOTHESES, ECRITE AVANT LES TESTS
===========================================================================

AVERTISSEMENT D'HONNETETE, a lire avant la famille. Contrairement a a28, a29 et a31, ce
rapport NE REVENDIQUE PAS le pre enregistrement. La famille ci dessous a ete ecrite apres
une lecture descriptive des rappels par tercile, et c'est cette lecture qui a impose un
choix de partition principale plutot que l'autre, pour une raison arithmetique donnee au
point (b). Les p qui suivent sont donc des p de confirmation faible. Le fait est ecrit ici
et repete dans le rapport ; aucune formulation ne doit laisser croire l'inverse.

(a) PERIMETRE. Le perimetre naturel de chaque methode : les 1 052 personnes pour les onze
    methodes qui les couvrent, les 150 personnes du run local pour C2 et C3, avec la
    reference de minorite et les bornes de tercile recalculees sur ces 150. Seuil declare :
    10 pour cent. Le seuil de 20 pour cent est une robustesse hors famille.

(b) PARTITION PRINCIPALE : les terciles du score de deductibilite PAR SEGMENT, D_seg,
    frequence de la modalite dans le segment ideologie x genre x age de la personne,
    calculee sans la personne. Ce n'est pas le premier choix naturel, et voici pourquoi
    c'est le bon. Le score de deductibilite logistique D_logit est, par construction, la
    confiance de `B1 argmax` dans la modalite consideree ; or `B1 argmax` ne peut predire
    une modalite que si elle est la plus probable. Mesure : la plus petite valeur de
    D_logit parmi les 1 496 raretes que `B1 argmax` ose sur le perimetre 1 052 vaut 0,145,
    au dessus de la borne superieure du tercile, 0,105. AUTREMENT DIT, 100 POUR CENT DES
    RARETES OSEES PAR LA REGRESSION TOMBENT DANS LE TERCILE DEDUCTIBLE PAR DEFINITION, et
    son rappel dans les deux autres terciles est nul par arithmetique et non par mesure.
    Une partition sur D_logit ne peut donc pas arbitrer le desaccord : elle le tranche
    d'avance en faveur de la these. La partition sur D_seg n'a pas ce defaut : la
    regression y place 16,1 pour cent de ses raretes dans le tercile non deductible.
    D_logit est rapporte partout a cote, comme partition secondaire et descriptive, avec
    ce meme avertissement.
    Bornes : 33,3e et 66,7e percentiles du score sur les cellules minoritaires REELLES du
    perimetre. T1 est le tercile le moins deductible, T3 le plus deductible. Les memes
    bornes classent les cellules ou une methode OSE une modalite minoritaire, via la
    deductibilite de la modalite PREDITE, sans quoi rappel et precision ne porteraient pas
    sur la meme partition et le F1 par tercile n'aurait pas de sens.

(c) LES DEUX PREDICTIONS RIVALES, ecrites avant de tester.
    THESE (a28, a29, a31) : le rappel du modele de langage est le plus haut dans le tercile
    NON deductible relativement a la statistique, et l'ecart avec la statistique y est
    maximal.
    ADVERSE (von der Heyde) : l'ecart se concentre dans le tercile deductible et s'annule
    ailleurs.

    | | enonce | nombre de tests |
    |---|---|---|
    | H1 primaire | pour chacune des 13 methodes non humaines, le rappel minoritaire sur T3 differe de celui sur T1, partition D_seg, bilateral | 13 |
    | H2 primaire | pour chacune des 8 conditions a modele de langage, l'avantage de rappel sur `B1 argmax` est strictement positif sur T1, le tercile NON deductible | 8 |
    | H3 secondaire | pour chacune des 8 conditions a modele de langage, cet avantage sur T1 differe de celui sur T3, bilateral : positif = these, negatif = von der Heyde | 8 |
    | H4 secondaire | pour chacune des 13 methodes, le rappel EN EXCES du plancher de bruit de cellule differe encore entre T3 et T1, bilateral | 13 |

    FAMILLE PRIMAIRE : H1 union H2, 21 tests. FAMILLE SECONDAIRE : H3 union H4, 21 tests.
    Les deux familles sont corrigees SEPAREMENT par HOLM, valide sans hypothese sur la
    dependance, ce qui est necessaire puisque les contrastes portent sur les memes
    personnes et les memes items. BENJAMINI HOCHBERG est rapporte a cote.

    H2 est le test qui peut faire tomber la these : si l'avantage sur le tercile non
    deductible n'est pas positif, le modele de langage ne retrouve que les raretes que la
    statistique peut deduire, et la phrase "il garde les outliers" tombe.

    COMPARATEUR DECLARE : `B1 argmax`. C'est le bon, et c'est le seul defendable : von der
    Heyde oppose GPT-3.5 a une regression multinomiale sur exactement les memes variables
    que l'invite. `B2 argmax` et `B3 foret` sont rapportes a cote, sans test declare.

(d) PLANCHER DE BRUIT DE CELLULE, lecture 01 section (d) point 5. Une cellule de repondants
    rares est petite, et Rennard et Xypolopoulos demontrent qu'un audit qui ne controle pas
    la taille de cellule "redecouvre un effet contre stereotypique fallacieux". Le plancher
    employe ici est le rappel attendu sous un tirage dans la MARGINALE DU SEGMENT de la
    personne, c'est a dire la moyenne de D_seg sur les cellules minoritaires du tercile.
    Un second plancher, plus bas, est le tirage dans la marginale de l'item, esperance de
    `B0 tirage`. Tout rappel est rapporte AUSSI en exces du plancher de segment.
    Consequence a dire en clair : le plancher de segment et le score de partition D_seg
    sont le meme calcul, donc l'exces sur la partition D_seg est une quantite construite
    pour etre plate ; c'est la partition D_logit qui donne la lecture non circulaire de
    l'exces, et les deux sont rapportees.

(e) N'ENTRENT DANS AUCUNE FAMILLE, et sont des descriptions : toute la partition D_logit ;
    la precision et le F1 par tercile ; le seuil de 20 pour cent ; le perimetre 150 pour
    les onze methodes qui disposent du 1 052 ; le recalcul du rapport groupe sur personne
    de a31 par tercile, qui est une verification de provenance et non un test nouveau ; le
    contraste de groupe entre les conditions a modele de langage et les predicteurs
    statistiques, ajoute apres coup et signale comme tel ; la ligne `humains vague 2`, qui
    est un plafond de bruit et non une methode.

(f) BOOTSTRAP. Tous les p sont des p de bootstrap APPARIE SUR LES PERSONNES, lus sur la
    position de zero dans la distribution ; ils ne descendent jamais sous 1 sur le nombre
    de tirages. Le meme tirage sert a toutes les methodes, ce qui rend les contrastes
    apparies. Le bootstrap ne porte jamais sur les cellules : deux reponses d'une meme
    personne ne sont pas independantes.

Sorties : a34-terciles-description.csv, a34-par-tercile.csv, a34-planchers.csv,
a34-contrastes.csv, a34-leviers-par-tercile.csv, a34-contraste-de-groupe.csv,
a34-controles.csv.

Usage :
  .venv/bin/python analyses/a34_deductibilite.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --cache-deduct /tmp/a34-deductibilite.pkl \
      --tirages 4000
"""

import argparse
import os
import pickle
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import a34_commun as C
from a2_baselines_gss import GRAINE as GRAINE_GRILLE, grille


PARTITIONS = ["D_seg segment", "D_logit regression"]


def _moy(v):
    """Moyenne en ignorant les NaN, NaN si le tableau est vide, sans avertissement."""
    v = np.asarray(v, float)
    v = v[~np.isnan(v)]
    return float(v.mean()) if len(v) else float("nan")


# ---------------------------------------------------------------------------

def preparer(paquet, tables, lignes, seuil, refs):
    """Toutes les matrices d'un perimetre et d'un seuil, une seule fois.

    Les DEUX scores de deductibilite sont calcules une fois pour toutes sur les 1 052
    humains de la vague 1, puis restreints au perimetre : ce sont des descripteurs de
    population, comme la marginale d'un item, et non des parametres appris sur les
    personnes evaluees. Les recalculer sur 150 personnes donnerait des cases de segment
    d'une ou deux personnes et un score qui ne mesurerait plus rien. En revanche le seuil
    de minorite et les BORNES de tercile sont recalcules sur le perimetre, comme a29 et
    a31 le font pour le seuil.
    """
    y1 = paquet["y1"][lignes]
    x = paquet["x"][lignes]
    mods = C.modalites_rares(y1, seuil)
    ok = C.observe(y1)
    rare_vrai = C.appartient(y1, mods) & ok

    d_logit_vrai = refs["d_logit_vrai"][lignes]
    seg_fin = refs["seg_fin"]
    d_seg_vrai = refs["d_seg_vrai"][lignes]
    d_item_vrai = refs["d_item_vrai"][lignes]

    # Segmentation de a1 et a31, pour le recalcul du levier du point 4.
    seg_a31, _ = C.C28.segments(x, paquet["attributs"])
    r_personne = C.rarete_personne(rare_vrai, ok)
    r_segment = C.rarete_segment(rare_vrai, ok, seg_a31[C.AXE_PRINCIPAL])

    bornes = {}
    tvrai = {}
    for nom_part, score in (("D_seg segment", d_seg_vrai),
                            ("D_logit regression", d_logit_vrai)):
        b1, b2 = C.bornes_terciles(score, rare_vrai)
        bornes[nom_part] = (b1, b2)
        tvrai[nom_part] = C.terciles(score, b1, b2)

    return {"y1": y1, "x": x, "mods": mods, "ok": ok, "rare_vrai": rare_vrai,
            "d_logit": d_logit_vrai, "d_seg": d_seg_vrai, "d_item": d_item_vrai,
            "seg_fin": seg_fin, "seg_a31": seg_a31,
            "r_personne": r_personne, "r_segment": r_segment,
            "bornes": bornes, "tvrai": tvrai, "lignes": lignes}


def _reinjecter(mat, lignes, tables):
    """Replace un bloc de lignes dans une matrice pleine, pour indexer les tables.

    Les tables de probabilite sont indexees par la position dans les 1 052 ; une matrice
    restreinte a 150 lignes ne peut donc pas les lire directement. On reconstruit une
    matrice pleine ou seules les lignes du perimetre portent une valeur.
    """
    n = tables[0][1].shape[0]
    m = mat.shape[1]
    plein = np.empty((n, m), dtype=object)
    plein[:] = None
    plein[lignes] = mat
    return plein


def terciles_predits(pred, prep, nom_part, tables, refs):
    """Tercile de la modalite PREDITE, memes bornes que les cellules reelles.

    La deductibilite de la modalite predite est evaluee avec les memes references de
    population que celle de la modalite reelle : sans cela, une methode serait classee sur
    une echelle et jugee sur une autre.
    """
    b1, b2 = prep["bornes"][nom_part]
    lignes = prep["lignes"]
    plein = _reinjecter(pred, lignes, tables)
    if nom_part == "D_logit regression":
        score = C.deductibilite(plein, tables)[lignes]
    else:
        score = C.frequence_segment(plein, refs["y1"], refs["ok"],
                                    refs["seg_fin"])[lignes]
    return C.terciles(score, b1, b2), score


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-deduct", default="/tmp/a34-deductibilite.pkl")
    ap.add_argument("--tirages", type=int, default=4000)
    args = ap.parse_args()

    rng = np.random.default_rng(C.GRAINE)
    paquet = C.charger(args.cache, args.cache_foret)
    y1, x, items = paquet["y1"], paquet["x"], paquet["items"]
    n_tot = len(paquet["ids"])

    # ------------------------------------------------- 0. le score de deductibilite
    if args.cache_deduct and os.path.exists(args.cache_deduct):
        with open(args.cache_deduct, "rb") as f:
            tables = pickle.load(f)
        print(f"deductibilite relue de {args.cache_deduct}")
    else:
        plis, _ = grille(n_tot, len(items), GRAINE_GRILLE)
        tables = C.probabilites_hors_pli(y1, x, plis)
        if args.cache_deduct:
            with open(args.cache_deduct, "wb") as f:
                pickle.dump(tables, f)

    controles = []
    # Controle 1 : l'argmax des distributions hors pli reproduit `B1 argmax`.
    am = C.argmax_hors_pli(tables, y1.shape[0], y1.shape[1])
    b1m = paquet["M"]["B1 argmax"]
    okb = np.array([[not C.est_manquant(v) for v in l] for l in b1m])
    controles.append({"controle": "argmax hors pli = B1 argmax",
                      "valeur": float(((am == b1m) & okb).sum()),
                      "reference": float(okb.sum())})
    print("controle argmax :", int(((am == b1m) & okb).sum()), "/", int(okb.sum()))

    per = C.perimetres(paquet)
    lignes_par_per = {"1052": per["1052"], "150": per["150"]}

    # Les references de population, calculees une fois sur les 1 052 humains.
    ok_tot = C.observe(y1)
    seg_fin, niveaux_seg = C.segment_fin(x, paquet["attributs"])
    refs = {"y1": y1, "ok": ok_tot, "seg_fin": seg_fin,
            "d_logit_vrai": C.deductibilite(y1, tables),
            "d_seg_vrai": C.frequence_segment(y1, y1, ok_tot, seg_fin),
            "d_item_vrai": C.frequence_item(y1, y1, ok_tot)}
    controles.append({"controle": "cases de segment ideologie x genre x age non vides",
                      "valeur": float(len(niveaux_seg)), "reference": 98.0})

    prep = {}
    for nom_per, lignes in lignes_par_per.items():
        for seuil in C.SEUILS:
            prep[(nom_per, seuil)] = preparer(paquet, tables, lignes, seuil, refs)

    # Controle 2 : les rappels globaux reproduisent a28 section 3.4 et a29 section 1.
    for nom_per, nom, cible in (("1052", "agents composite", 0.3069),
                                ("1052", "B1 argmax", 0.0580),
                                ("1052", "B3 foret", 0.0144),
                                ("150", "C3", 0.2195),
                                ("150", "C2", 0.1285)):
        p = prep[(nom_per, 0.10)]
        m = C.masques(paquet["M"][nom][p["lignes"]], p["y1"], p["mods"])
        v = m["juste"].sum() / max(p["rare_vrai"].sum(), 1)
        controles.append({"controle": f"rappel global {nom}, perimetre {nom_per}",
                          "valeur": float(v), "reference": cible})
        print(f"controle rappel {nom} {nom_per} : {v:.4f} contre {cible}")

    # ------------------------------------------------- 1. description des terciles
    desc = []
    for (nom_per, seuil), p in prep.items():
        for nom_part in PARTITIONS:
            b1, b2 = p["bornes"][nom_part]
            t = p["tvrai"][nom_part]
            for k in range(3):
                sel = p["rare_vrai"] & (t == k)
                desc.append({
                    "perimetre": nom_per, "seuil": seuil, "partition": nom_part,
                    "tercile": C.TERCILES[k], "borne_basse": b1, "borne_haute": b2,
                    "cellules_minoritaires": int(sel.sum()),
                    "score_moyen": _moy(
                        (p["d_seg"] if nom_part == "D_seg segment"
                         else p["d_logit"])[sel]),
                    "plancher_segment": _moy(p["d_seg"][sel]),
                    "plancher_item": _moy(p["d_item"][sel]),
                    "items_distincts": int(len({j for j in np.flatnonzero(
                        sel.any(axis=0))})),
                })
            sel = p["rare_vrai"]
            desc.append({
                "perimetre": nom_per, "seuil": seuil, "partition": nom_part,
                "tercile": "ensemble", "borne_basse": b1, "borne_haute": b2,
                "cellules_minoritaires": int(sel.sum()),
                "score_moyen": _moy(
                    (p["d_seg"] if nom_part == "D_seg segment"
                     else p["d_logit"])[sel]),
                "plancher_segment": _moy(p["d_seg"][sel]),
                "plancher_item": _moy(p["d_item"][sel]),
                "items_distincts": int(sel.any(axis=0).sum()),
            })
    # Couverture du score de segment, et le fait arithmetique sur D_logit.
    p = prep[("1052", 0.10)]
    controles.append({"controle": "couverture D_seg sur cellules minoritaires, 1052",
                      "valeur": float((~np.isnan(p["d_seg"][p["rare_vrai"]])).mean()),
                      "reference": 1.0})
    mB1 = C.masques(paquet["M"]["B1 argmax"][p["lignes"]], p["y1"], p["mods"])
    dpred = C.deductibilite(
        _reinjecter(paquet["M"]["B1 argmax"][p["lignes"]], p["lignes"], tables), tables)
    v = dpred[p["lignes"]][mB1["rare_pred"]]
    controles.append({"controle": "min D_logit des raretes osees par B1 argmax",
                      "valeur": float(np.nanmin(v)),
                      "reference": float(p["bornes"]["D_logit regression"][1])})
    print(f"min D_logit des raretes osees par B1 : {np.nanmin(v):.4f} "
          f"contre borne haute {p['bornes']['D_logit regression'][1]:.4f}")

    # ------------------------------------------------- 2. mesures par tercile
    idx_boot = {}
    for nom_per, lignes in lignes_par_per.items():
        idx_boot[nom_per] = C.tirages_bootstrap(len(lignes), args.tirages, rng)

    mesures, cache_num = [], {}
    for (nom_per, seuil), p in prep.items():
        ib = idx_boot[nom_per]
        for nom in C.methodes_du_perimetre(paquet, nom_per):
            pred = paquet["M"][nom][p["lignes"]]
            m = C.masques(pred, p["y1"], p["mods"])
            for nom_part in PARTITIONS:
                tv = p["tvrai"][nom_part]
                tp, _score_pred = terciles_predits(pred, p, nom_part, tables, refs)
                for k in list(range(3)) + [-9]:
                    selv = p["rare_vrai"] if k == -9 else (p["rare_vrai"] & (tv == k))
                    selp = m["rare_pred"] if k == -9 else (m["rare_pred"] & (tp == k))
                    nr, dr = C.par_personne(m["juste"], selv)
                    npx, dpx = C.par_personne(m["juste"], selp)
                    rap, rb, rh, _ = C.taux_ic(nr, dr, ib)
                    pre, pb, ph, _ = C.taux_ic(npx, dpx, ib)
                    f1 = (2 * rap * pre / (rap + pre)
                          if np.isfinite(rap) and np.isfinite(pre) and (rap + pre) > 0
                          else (0.0 if np.isfinite(rap) else np.nan))
                    # plancher : cellules minoritaires du tercile dont D_seg existe
                    okp = selv & ~np.isnan(p["d_seg"])
                    npl, dpl = C.moyenne_par_personne(okp, p["d_seg"])
                    nit, dit_ = C.moyenne_par_personne(
                        selv & ~np.isnan(p["d_item"]), p["d_item"])
                    nre, dre = C.par_personne(m["juste"], okp)
                    exc_num = nre - npl
                    plancher = C.taux(npl, dpl)
                    rap_r = C.taux(nre, dre)
                    cle = (nom_per, seuil, nom, nom_part, k)
                    cache_num[cle] = {"rappel": (nr, dr), "precision": (npx, dpx),
                                      "exces": (exc_num, dre)}
                    mesures.append({
                        "perimetre": nom_per, "seuil": seuil, "partition": nom_part,
                        "tercile": "ensemble" if k == -9 else C.TERCILES[k],
                        "condition": nom,
                        "cellules_minoritaires": int(dr.sum()),
                        "raretes_osees": int(dpx.sum()),
                        "rappel": rap, "rappel_ic_bas": rb, "rappel_ic_haut": rh,
                        "precision": pre, "precision_ic_bas": pb,
                        "precision_ic_haut": ph, "f1": f1,
                        "plancher_segment": plancher,
                        "plancher_item": C.taux(nit, dit_),
                        "rappel_sur_cellules_a_plancher": rap_r,
                        "exces_sur_plancher": rap_r - plancher,
                    })
        print(f"  mesures {nom_per}, seuil {seuil:.2f} terminees", flush=True)

    mes = pd.DataFrame(mesures)

    # ------------------------------------------------- 3. contrastes declares
    contr = []

    def ajouter(famille, hypothese, nom, nom_per, comparaison, a, b, ib):
        o, lo, hi, pp = C.contraste(*a, *b, ib)
        contr.append({"famille": famille, "hypothese": hypothese, "condition": nom,
                      "perimetre": nom_per, "comparaison": comparaison,
                      "difference": o, "ic_bas": lo, "ic_haut": hi, "p_bootstrap": pp})

    for nom, nom_per in C.PERIMETRE_NATUREL.items():
        ib = idx_boot[nom_per]
        k_t1, k_t3 = 0, 2
        part = "D_seg segment"
        # H1 : rappel T3 contre T1
        a = cache_num[(nom_per, 0.10, nom, part, k_t3)]["rappel"]
        b = cache_num[(nom_per, 0.10, nom, part, k_t1)]["rappel"]
        ajouter("primaire", "H1 gradient de rappel T3 moins T1", nom, nom_per,
                "T3 deductible contre T1 non deductible", a, b, ib)
        # H4 : exces sur plancher, T3 contre T1
        a = cache_num[(nom_per, 0.10, nom, part, k_t3)]["exces"]
        b = cache_num[(nom_per, 0.10, nom, part, k_t1)]["exces"]
        ajouter("secondaire", "H4 gradient de l'exces sur plancher T3 moins T1", nom,
                nom_per, "T3 deductible contre T1 non deductible", a, b, ib)

    for nom in C.LLM:
        nom_per = C.PERIMETRE_NATUREL[nom]
        ib = idx_boot[nom_per]
        part = "D_seg segment"
        a = cache_num[(nom_per, 0.10, nom, part, 0)]["rappel"]
        b = cache_num[(nom_per, 0.10, C.COMPARATEUR, part, 0)]["rappel"]
        ajouter("primaire", "H2 avantage sur B1 argmax dans T1 non deductible", nom,
                nom_per, f"{nom} contre {C.COMPARATEUR}, T1", a, b, ib)

        # H3 : difference de differences, T1 moins T3. Elle demande un bootstrap sur
        # quatre rapports simultanement, il est fait a la main sur les memes tirages.
        na1, da1 = cache_num[(nom_per, 0.10, nom, part, 0)]["rappel"]
        nb1, db1 = cache_num[(nom_per, 0.10, C.COMPARATEUR, part, 0)]["rappel"]
        na3, da3 = cache_num[(nom_per, 0.10, nom, part, 2)]["rappel"]
        nb3, db3 = cache_num[(nom_per, 0.10, C.COMPARATEUR, part, 2)]["rappel"]

        def r(nu, de, idx=None):
            if idx is None:
                d = de.sum()
                return nu.sum() / d if d > 0 else np.nan
            d = de[idx].sum(axis=1)
            n_ = nu[idx].sum(axis=1)
            with np.errstate(invalid="ignore", divide="ignore"):
                return np.where(d > 0, n_ / np.maximum(d, 1e-12), np.nan)

        obs = ((r(na1, da1) - r(nb1, db1)) - (r(na3, da3) - r(nb3, db3)))
        tir = ((r(na1, da1, ib) - r(nb1, db1, ib))
               - (r(na3, da3, ib) - r(nb3, db3, ib)))
        tir = tir[~np.isnan(tir)]
        contr.append({"famille": "secondaire",
                      "hypothese": "H3 avantage dans T1 moins avantage dans T3",
                      "condition": nom, "perimetre": nom_per,
                      "comparaison": f"({nom} moins {C.COMPARATEUR}) T1 moins T3",
                      "difference": float(obs),
                      "ic_bas": float(np.percentile(tir, 2.5)) if len(tir) else np.nan,
                      "ic_haut": float(np.percentile(tir, 97.5)) if len(tir) else np.nan,
                      "p_bootstrap": C.p_contre_zero(tir)})

    ct = pd.DataFrame(contr)
    for fam in ("primaire", "secondaire"):
        idx = ct.famille == fam
        ct.loc[idx, "p_holm"] = C.holm(ct.loc[idx, "p_bootstrap"].values)
        ct.loc[idx, "p_bh"] = C.benjamini_hochberg(ct.loc[idx, "p_bootstrap"].values)
        ct.loc[idx, "tests_dans_la_famille"] = int(idx.sum())

    # ------------------------------------------------- 4. le levier de a31 par tercile
    lev = []
    for nom, nom_per in list(C.PERIMETRE_NATUREL.items()) + [("humains vague 2", "1052"),
                                                             ("humains vague 2", "150")]:
        p = prep[(nom_per, 0.10)]
        ib = idx_boot[nom_per]
        pred = paquet["M"][nom][p["lignes"]]
        m = C.masques(pred, p["y1"], p["mods"])
        for nom_part in PARTITIONS:
            tp, _ = terciles_predits(pred, p, nom_part, tables, refs)
            for k in list(range(3)) + [-9]:
                cible = m["faux_maj"] if k == -9 else (m["faux_maj"] & (tp == k))
                if cible.sum() < 20:
                    continue
                ligne = {"perimetre": nom_per, "condition": nom, "partition": nom_part,
                         "tercile": "ensemble" if k == -9 else C.TERCILES[k],
                         "fausses_raretes": int(cible.sum())}
                for cle, mat in (("personne", p["r_personne"]),
                                 ("groupe", p["r_segment"])):
                    num, den = C.moyenne_par_personne(cible, mat)
                    v, lo, hi, _ = C.taux_ic(num, den, ib)
                    num_t, den_t = C.temoin_par_personne(cible, p["ok"], mat)
                    tem = C.taux(num_t, den_t)
                    ligne[f"valeur_{cle}"] = v
                    ligne[f"temoin_{cle}"] = tem
                    ligne[f"lift_{cle}"] = (v / tem - 1.0) if tem and tem > 0 else np.nan
                lp, lg = ligne.get("lift_personne"), ligne.get("lift_groupe")
                ligne["rapport_groupe_sur_personne"] = (
                    lg / lp if (lp is not None and lg is not None
                                and np.isfinite(lp) and lp > 0) else np.nan)
                lev.append(ligne)
    lv = pd.DataFrame(lev)

    # ------------------------------------------------- 5. contraste de groupe, post hoc
    cg = []
    for nom_part in PARTITIONS:
        for k in list(range(3)) + [-9]:
            nom_t = "ensemble" if k == -9 else C.TERCILES[k]
            for nom_per in ("1052", "150"):
                s = mes[(mes.perimetre == nom_per) & (mes.seuil == 0.10)
                        & (mes.partition == nom_part) & (mes.tercile == nom_t)]
                a = s[s.condition.isin(C.LLM)]["rappel"].values
                b = s[s.condition.isin(C.STAT)]["rappel"].values
                if len(a) < 2 or len(b) < 2:
                    continue
                obs, pp = C.C28.permutation(a, b, 20000, rng)
                cg.append({"perimetre": nom_per, "partition": nom_part, "tercile": nom_t,
                           "moyenne_llm": float(np.nanmean(a)),
                           "moyenne_stat": float(np.nanmean(b)),
                           "difference": obs, "p_permutation": pp,
                           "n_llm": len(a), "n_stat": len(b)})
    cgd = pd.DataFrame(cg)

    # ------------------------------------------------- ecriture
    C.ecrire(pd.DataFrame(desc), "a34-terciles-description.csv")
    C.ecrire(mes, "a34-par-tercile.csv")
    C.ecrire(mes[["perimetre", "seuil", "partition", "tercile", "condition", "rappel",
                  "plancher_segment", "plancher_item",
                  "rappel_sur_cellules_a_plancher", "exces_sur_plancher"]],
             "a34-planchers.csv")
    C.ecrire(ct, "a34-contrastes.csv")
    C.ecrire(lv, "a34-leviers-par-tercile.csv")
    C.ecrire(cgd, "a34-contraste-de-groupe.csv")
    C.ecrire(pd.DataFrame(controles), "a34-controles.csv")

    # ------------------------------------------------- affichage
    pd.set_option("display.width", 250)
    ordre = {c: i for i, c in enumerate(C.ORDRE_METHODES)}
    for nom_part in PARTITIONS:
        for nom_per in ("1052", "150"):
            s = mes[(mes.perimetre == nom_per) & (mes.seuil == 0.10)
                    & (mes.partition == nom_part)].copy()
            if s.empty:
                continue
            s["o"] = s.condition.map(ordre)
            piv = s.pivot_table(index=["o", "condition"], columns="tercile",
                                values="rappel").sort_index()
            print("\n" + "=" * 120)
            print(f"RAPPEL par tercile, partition {nom_part}, perimetre {nom_per}, "
                  f"seuil 10 %")
            print("=" * 120)
            print(piv.round(4).to_string())

    print("\n" + "=" * 120)
    print("Contrastes declares et corrections pour tests multiples")
    print("=" * 120)
    c2 = ct.copy()
    c2["o"] = c2.condition.map(ordre)
    print(c2.sort_values(["famille", "hypothese", "o"])[
        ["famille", "hypothese", "condition", "perimetre", "difference", "ic_bas",
         "ic_haut", "p_bootstrap", "p_holm", "p_bh"]].round(4).to_string(index=False))

    print("\n" + "=" * 120)
    print("Levier groupe sur personne par tercile (recalcul de a31)")
    print("=" * 120)
    s = lv.copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values(["partition", "perimetre", "o", "tercile"])[
        ["partition", "perimetre", "condition", "tercile", "fausses_raretes",
         "lift_personne", "lift_groupe", "rapport_groupe_sur_personne"]]
        .round(4).to_string(index=False))

    print("\n" + "=" * 120)
    print("Contraste de groupe, post hoc")
    print("=" * 120)
    print(cgd.round(4).to_string(index=False))


if __name__ == "__main__":
    main()
