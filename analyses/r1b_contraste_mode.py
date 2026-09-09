"""r1b. Le contraste des deux modes, sur la meme quantite et les memes items.

Aucun appel de modele. Lecture seule sur `data/traces/` et `resultats/`. Quatre coeurs.
Aucun fichier existant n'est modifie ; les sorties portent toutes le prefixe `r1b-`.

Pourquoi ce script existe. Le preenregistrement de r1 (section 9) interdit la comparaison
chiffree du facteur H2b au facteur 1,62 de `a38` : perimetre d'items different (79 contre
29), echelle differente (position de nomenclature contre score de desirabilite de `a25`),
mode different (description contre incarnation). Ce script leve les deux premieres
differences et laisse la troisieme, qui est la seule qui interesse :

  - il restreint r1 aux **29 items a pole de desirabilite declare** de `a38`, qui sont tous
    dans les 79 items orientes de `a37` [MESURE, verifie en tete d'execution] ;
  - il recalcule sur les distributions decrites de r1 **exactement la quantite de a38**,
    le score moyen de desirabilite de `a25` par camp, puis le facteur
    `(d_gauche - d_droite) decrit / (d_gauche - d_droite) reel` ;
  - il verifie que l'ecart humain retombe sur les 0,236063 publies par `a38` au perimetre
    1 052, ce qui est le controle de nomenclature du contraste.

Il produit aussi l'analyse de sensibilite des cellules retirees par le critere de chute 2 :
les 11 cellules de Qwen3-4B qui recopient l'exemple chiffre de l'invite de relance sont
remises dans les mesures, et H1, H2a et H2b sont recalculees avec elles.

Sorties :
  resultats/r1b-contraste-mode.csv        le facteur de a38 recalcule en mode description
  resultats/r1b-h2b-29-items.csv          H2b (position) restreinte aux 29 items de a38
  resultats/r1b-sensibilite-exclusions.csv  avec et sans les cellules retirees
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

import a25_commun as A25
import a25_mesures as A25M
import a38_commun as A38
import r1_evaluer as R1
from r1_oracle_camps import CAMPS, IDENTITES

RACINE = R1.RACINE
SORTIE = R1.SORTIE
GRAINE = 20260909


# ---------------------------------------------------------------------------
# 1. Le score de desirabilite de a25, applique a une distribution decrite
# ---------------------------------------------------------------------------

def table_desirabilite(items, options):
    """item -> (vecteur de scores aligne sur les rangs, masque des modalites qui en portent).

    Les fonctions employees sont celles de a25, importees et non recopiees, pour que la
    quantite calculee ici soit au bit pres celle que a38 calcule sur les agents.
    """
    opts25 = A25.options_par_item(RACINE)
    table = {}
    for it in items:
        rangs = [o.lower().strip() for o in options[it]]
        assert rangs == opts25[it], f"{it} : les modalites de r1 et de a25 divergent"
        scores, _, _ = A25.scores_desirabilite(it, opts25[it])
        if scores is None:
            continue
        vec = np.array([float(scores.get(o, 0.0)) for o in rangs])
        defini = np.array([o in scores for o in rangs], dtype=bool)
        table[it] = (vec, defini)
    return table


def desirabilite(p, vec, defini):
    d, _ = A25M.desirabilite_moyenne(np.asarray(p, float)[None, :], vec, defini)
    return float(d[0])


# ---------------------------------------------------------------------------
# 2. Le contraste des deux modes
# ---------------------------------------------------------------------------

def contraste_mode(traces, ref, options, rng):
    items29 = [it for it in sorted(A38.POLE_ENDOGROUPE) if it in options]
    table = table_desirabilite(items29, options)
    items29 = [it for it in items29 if it in table]

    # distributions decrites, cellules retenues seulement (critere de chute 2 applique)
    dec = {}
    for t in traces:
        it = t["item"]
        if it not in table or t["rejet"] or not t.get("distribution"):
            continue
        if t.get("n_tentatives", 1) > 1 and R1.recopie_exemple(t["distribution"]):
            continue
        p = np.array([t["distribution"][o] for o in options[it]], float)
        dec[(t["cle_modele"], t["modele"], t["identite"], t["camp"], it)] = p

    lignes = []
    modeles = sorted({(c, m) for c, m, _, _, _ in dec})
    for cle, modele in modeles:
        for identite in IDENTITES:
            a, b, bw2, gard = [], [], [], []
            for it in items29:
                vec, defini = table[it]
                kg = (cle, modele, identite, "gauche", it)
                kd = (cle, modele, identite, "droite", it)
                if kg not in dec or kd not in dec:
                    continue
                a.append(desirabilite(dec[kg], vec, defini)
                         - desirabilite(dec[kd], vec, defini))
                b.append(desirabilite(ref[(it, "gauche", "w1")], vec, defini)
                         - desirabilite(ref[(it, "droite", "w1")], vec, defini))
                bw2.append(desirabilite(ref[(it, "gauche", "w2")], vec, defini)
                           - desirabilite(ref[(it, "droite", "w2")], vec, defini))
                gard.append(it)
            if len(a) < 3:
                continue
            a, b, bw2 = np.array(a), np.array(b), np.array(bw2)
            r, bas, haut, n = R1.ic_ratio_des_moyennes(a, b, rng)
            rp, pbas, phaut, _ = R1.ic_ratio_des_moyennes(bw2, b, rng)
            lignes.append({
                "quantite": "score de desirabilite a25, facteur de a38",
                "mode": "description (r1)", "modele": modele, "cle_modele": cle,
                "identite": identite, "perimetre": "29 items a pole declare (a38)",
                "n_items": n,
                "ecart_decrit_moyen": float(a.mean()),
                "ecart_reel_moyen": float(b.mean()),
                "facteur": r, "ic_bas": bas, "ic_haut": haut,
                "facteur_plancher_w2_w1": rp,
                "plancher_ic_bas": pbas, "plancher_ic_haut": phaut,
                "p": R1.p_permutation_signe(a - b, rng),
            })
    return pd.DataFrame(R1.poser_holm(lignes)), items29, table


def h2b_29_items(ecarts, rng, items29):
    """H2b, la quantite de position de r1, restreinte aux 29 items de a38."""
    lignes = []
    garde = set(items29)
    for (modele, cle, identite), g in ecarts.groupby(
            ["modele", "cle_modele", "identite"], sort=False):
        gg = g[g["item"].isin(garde)]
        if len(gg) < 3:
            continue
        a = gg["gap_signe_decrit"].to_numpy()
        b = gg["gap_signe_reel_w1"].to_numpy()
        r, bas, haut, n = R1.ic_ratio_des_moyennes(a, b, rng)
        rp, _, _, _ = R1.ic_ratio_des_moyennes(gg["gap_signe_reel_w2"].to_numpy(), b, rng)
        lignes.append({
            "quantite": "position de nomenclature, facteur H2b de r1",
            "mode": "description (r1)", "modele": modele, "cle_modele": cle,
            "identite": identite, "perimetre": "29 items a pole declare (a38)",
            "n_items": n,
            "ecart_decrit_moyen": float(a.mean()), "ecart_reel_moyen": float(b.mean()),
            "facteur": r, "ic_bas": bas, "ic_haut": haut,
            "facteur_plancher_w2_w1": rp,
            "p": R1.p_permutation_signe(a - b, rng),
        })
    return pd.DataFrame(R1.poser_holm(lignes))


# ---------------------------------------------------------------------------
# 3. Sensibilite aux cellules retirees par le critere de chute 2
# ---------------------------------------------------------------------------

def par_cellule_sans_critere2(traces, ref, options, sens, effectifs):
    """Le meme tableau que r1_evaluer.par_cellule, mais le critere de chute 2 desarme.

    Les cellules qui recopient l'exemple chiffre de l'invite de relance sont conservees.
    C'est l'analyse de sensibilite, pas la mesure principale : le preenregistrement les
    exclut et cette exclusion reste la conduite publiee.
    """
    import json
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
        pd_ = np.array([t["distribution"][o] for o in options[item]], dtype=float)
        s = sens.get(item, 0)
        base.update({
            "gs_decrit": R1.gini_simpson(pd_),
            "gs_reel_w1": R1.gini_simpson(p1),
            "gs_reel_w1_sans_biais": R1.gini_simpson_sans_biais(p1, n1),
            "gs_reel_w2": R1.gini_simpson(p2),
            "tv_decrit_reel": R1.tv(pd_, p1),
            "tv_plancher_w1_w2": R1.tv(p1, p2),
            "pos_decrit": R1.position(pd_, s),
            "pos_reel_w1": R1.position(p1, s),
            "pos_reel_w2": R1.position(p2, s),
            "p_decrit": json.dumps([round(float(v), 6) for v in pd_]),
        })
        lignes.append(base)
    return pd.DataFrame(lignes)


def sensibilite(traces, ref, options, sens, effectifs, oriente, strict):
    sorties = []
    for etiquette, fabricant in (
            ("principal, critere 2 applique", R1.par_cellule),
            ("sensibilite, cellules recopiees gardees", par_cellule_sans_critere2)):
        rng = np.random.default_rng(GRAINE)
        cel = fabricant(traces, ref, options, sens, effectifs)
        ec = R1.par_item_ecarts(cel, ref, sens)
        h1 = R1.test_h1(cel, rng)
        h2 = R1.test_h2(ec, rng, oriente, strict)
        h1 = h1.assign(perimetre_analyse=etiquette, famille="H1")
        h2 = h2.assign(perimetre_analyse=etiquette, famille="H2")
        idt = R1.par_item_identite(cel, ref)
        h3 = R1.test_h3(idt, rng).assign(perimetre_analyse=etiquette, famille="H3")
        sorties += [h1, h2, h3]
    return pd.concat(sorties, ignore_index=True, sort=False)


# ---------------------------------------------------------------------------

def main():
    rng = np.random.default_rng(GRAINE)
    traces = R1.lire_traces("")
    ref, options, effectifs = R1.lire_referent()
    sens, oriente, strict, derive = R1.lire_a37()
    print(f"{len(traces)} cellules de trace lues")

    items29 = sorted(A38.POLE_ENDOGROUPE)
    dedans = [i for i in items29 if oriente.get(i, False)]
    print(f"items a pole declare de a38 : {len(items29)}, "
          f"dont orientes par a37 : {len(dedans)}")

    cm, items29, _ = contraste_mode(traces, ref, options, rng)
    reel = cm["ecart_reel_moyen"].dropna().unique()
    print(f"controle de nomenclature : ecart humain sur les 29 items = "
          f"{reel[0]:.6f} (a38 publie 0,236063 au perimetre 1 052)")
    R1.ecrire(cm, "r1b-contraste-mode.csv", "")

    cel = R1.par_cellule(traces, ref, options, sens, effectifs)
    ec = R1.par_item_ecarts(cel, ref, sens)
    R1.ecrire(h2b_29_items(ec, rng, items29), "r1b-h2b-29-items.csv", "")

    R1.ecrire(sensibilite(traces, ref, options, sens, effectifs, oriente, strict),
              "r1b-sensibilite-exclusions.csv", "")


if __name__ == "__main__":
    main()
