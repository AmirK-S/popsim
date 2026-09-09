"""
r3b_appariement : reparation du perimetre d'items des mesures de rarete de R3, et
plancher humain des quatre quantites publiees.

POURQUOI CE SCRIPT EXISTE. `r3_evaluer.py` restreint aux 58 items de famille
l'exactitude, les deux ratios de dispersion et la chute sous permutation (toutes passent
par `pred[:, colonnes]` ou recoivent `colonnes`). Il ne les restreint PAS pour la famille
de mesures de rarete de a29 et a31 : `mesurer()` appelle
`C44.groupe_sur_personne(pred, ...)` sur la matrice 149 colonnes entiere. Or les traces de
R3 (C3E, C2S) ne couvrent que les 58 items de famille, tandis que les traces de a5 (C3, C2)
en couvrent 149. Les quatre quantites `lift personne`, `lift segment`,
`groupe sur personne` et `rappel des rares` de `resultats/r3-contrastes.csv` comparent donc
un bras mesure sur 58 items a un bras mesure sur 149, et leur denominateur, le nombre de
cellules rares vraies, court sur les 149 items dans les deux cas.

Ce script recalcule exactement les memes quantites, avec les memes fonctions importees
sans retouche, apres avoir masque les predictions des deux bras hors des 58 items. Il
ajoute le bootstrap apparie sur les personnes que `r3-rarete.csv` n'a pas, et la ligne
`humains vague 2` comme plancher, sur les memes personnes et les memes cellules.

Il n'ecrit que des fichiers `r3b-*`. Aucun script existant n'est modifie, aucune trace
n'est reecrite, zero appel de modele de langage, lecture seule sur data/.

Importes tels quels :
  r3_evaluer   matrice_depuis_trace(), segmentations_r3(), contexte_perimetre(),
               sous_contexte(), mesurer(), mesures_rares(), chute_permutation(),
               p_dirige(), GRAINE, TRACES_R3, CONTRASTES.
  a44_commun   charger(), groupe_sur_personne(), holm(), benjamini_hochberg(), ecrire().
  a5_agents_locaux_gss  groupes_familles(), nomenclature().

Usage :
  .venv/bin/python analyses/r3b_appariement.py --tirages 2000
"""

import argparse
import os
import sys
import time
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import a44_commun as C44
import r3_evaluer as R3
from a5_agents_locaux_gss import TRACES, groupes_familles, nomenclature

SORTIE = C44.SORTIE
GRAINE = R3.GRAINE

# Les quatre quantites de rarete que r3_evaluer mesure hors du perimetre d'items, plus
# les deux comptages qui expliquent l'ecart.
CLES_RARETE = ["lift personne", "lift segment", "groupe sur personne",
               "rappel des rares"]

# Sens predit, repris mot pour mot de la page de plan par l'intermediaire de R3.SENS.
SENS_RARETE = {"lift personne": "aucun", "lift segment": "hausse",
               "groupe sur personne": "hausse", "rappel des rares": "aucun"}


def masquer(mat, colonnes):
    """La matrice de predictions, videe hors des colonnes du perimetre.

    None est la convention de a5_evaluer pour « cellule non predite » ; c'est celle que
    `C42.observe` et `C29.observe` lisent. Masquer revient donc a mettre les deux bras
    dans l'etat de couverture du bras le plus pauvre, ce qui est la seule facon de
    comparer deux traces de perimetres differents sur la meme definition de rarete.
    """
    out = np.empty_like(mat)
    out[:] = None
    out[:, colonnes] = mat[:, colonnes]
    return out


def mesures_de_rarete(pred, ctx, colonnes):
    """Les quantites de a29 et a31, calculees sur le perimetre d'items declare."""
    p = masquer(pred, colonnes)
    g = C44.groupe_sur_personne(p, ctx["cv"]["S_ideo"])
    out = {"lift personne": g["lift_personne"], "lift segment": g["lift_segment"],
           "groupe sur personne": g["groupe_sur_personne"],
           "rappel des rares": g["rappel_rares"],
           "raretes osees": float(g["raretes_osees"]),
           "fausses raretes": float(g["fausses_raretes"])}
    for classe in ("stable", "ensemble"):
        r = R3.mesures_rares(p, ctx, classe)
        for cle in ("rappel", "precision", "exces_segment", "exces_item"):
            out[f"{cle} ({classe})"] = r[cle]
        out[f"cellules ({classe})"] = float(r["cellules"])
    return out


def contraste_rarete(nom, avec, sans, paquet, infos, colonnes, segs, args):
    """Le contraste de rarete a perimetre d'items apparie, bootstrap sur les personnes."""
    lignes = np.array(sorted(set(infos[avec]["lignes"]) & set(infos[sans]["lignes"])))
    if len(lignes) < args.personnes_min:
        return [], []
    ctx = R3.contexte_perimetre(paquet, lignes, colonnes, segs)
    pa = paquet["M"][avec][lignes]
    pb = paquet["M"][sans][lignes]
    ph = paquet["M"]["humains vague 2"][lignes]

    ma = mesures_de_rarete(pa, ctx, colonnes)
    mb = mesures_de_rarete(pb, ctx, colonnes)
    mh = mesures_de_rarete(ph, ctx, colonnes)

    print(f"\n=== {nom} : {avec} contre {sans}, {len(lignes)} personnes, "
          f"{len(colonnes)} items, perimetre d'items APPARIE ===", flush=True)
    for cle in sorted(ma):
        print(f"  {cle:<26} {avec} {ma[cle]:>9.4f}   {sans} {mb[cle]:>9.4f}   "
              f"effet {ma[cle] - mb[cle]:>+9.4f}   humains {mh[cle]:>9.4f}", flush=True)

    n = len(lignes)
    rb = np.random.default_rng(GRAINE + 1)
    tirages = defaultdict(list)
    for t in range(args.tirages):
        idx = rb.integers(0, n, n)
        sc = R3.sous_contexte(ctx, idx)
        a = mesures_de_rarete(pa[idx], sc, colonnes)
        b = mesures_de_rarete(pb[idx], sc, colonnes)
        for cle in a:
            tirages[cle].append(a[cle] - b[cle])
        if args.pas and (t + 1) % args.pas == 0:
            print(f"    bootstrap {t + 1}/{args.tirages}", flush=True)

    lignes_tab, lignes_con = [], []
    for nom_cond, m in ((avec, ma), (sans, mb), ("humains vague 2", mh)):
        lignes_tab.append({"contraste": nom, "condition": nom_cond,
                           "personnes": n, "items": len(colonnes), **m})
    for cle in sorted(ma):
        sens = SENS_RARETE.get(cle, "aucun")
        bas, haut, p = R3.p_dirige(tirages[cle], sens)
        lignes_con.append({
            "contraste": nom, "avec": avec, "sans": sans, "mesure": cle,
            "sens_predit": sens, "personnes": n, "items": len(colonnes),
            "valeur_avec": ma[cle], "valeur_sans": mb[cle],
            "valeur_humains vague 2": mh[cle],
            "effet": ma[cle] - mb[cle], "ic_bas": bas, "ic_haut": haut,
            "p_bootstrap": p,
            "tirages": int(sum(1 for x in tirages[cle] if np.isfinite(x)))})
    return lignes_tab, lignes_con


def plancher_et_parts(paquet, infos, colonnes, segs, args):
    """Chute sous permutation et ratios, avec la ligne `humains vague 2` du perimetre.

    `r3-tableau.csv` publie les chutes de C3E, C3, C2 et C2S mais aucun plancher : la
    part du plancher humain de a44 n'est donc pas calculable sur ses chiffres. Cette
    fonction ajoute la ligne humaine, sur les MEMES personnes et les MEMES 58 items, ce
    qui est la seule reference que a44 section 5 accepte.
    """
    sorties = []
    for nom, avec, sans in (("H1", "C3E", "C3"), ("H2", "C2", "C2S")):
        lignes = np.array(sorted(set(infos[avec]["lignes"]) & set(infos[sans]["lignes"])))
        ctx = R3.contexte_perimetre(paquet, lignes, colonnes, segs)
        ref = {}
        for cond in (avec, sans, "humains vague 2"):
            rng = np.random.default_rng(GRAINE)
            m = R3.mesurer(masquer(paquet["M"][cond][lignes], colonnes), ctx, rng,
                           args.permutations)
            ref[cond] = m
        for cond in (avec, sans, "humains vague 2"):
            m = ref[cond]
            ligne = {"contraste": nom, "condition": cond, "personnes": len(lignes),
                     "items": len(colonnes), "exactitude": m["exactitude"]}
            for cle in ("S_ideo", "S_gra"):
                h = ref["humains vague 2"][f"chute relative {cle}"]
                ligne[f"chute {cle}"] = m[f"chute permutation {cle}"]
                ligne[f"chute relative {cle}"] = m[f"chute relative {cle}"]
                ligne[f"part du plancher humain {cle}"] = (
                    m[f"chute relative {cle}"] / h if h else np.nan)
                ligne[f"segments exploitables {cle}"] = m[f"segments exploitables {cle}"]
                ligne[f"ratio inter ({cle})"] = m[f"ratio inter ({cle})"]
                ligne[f"ratio intra ({cle})"] = m[f"ratio intra ({cle})"]
            sorties.append(ligne)
            print(f"  {nom} {cond:<18} exactitude {ligne['exactitude']:.4f}  "
                  f"part plancher S_ideo {ligne['part du plancher humain S_ideo']:.3f}  "
                  f"S_gra {ligne['part du plancher humain S_gra']:.3f}", flush=True)
    return sorties


def tailles_de_segments(infos, colonnes, segs):
    """Combien de cellules de segmentation la permutation a reellement a permuter.

    a44 permute a l'interieur de toutes les cellules ; `r3_evaluer.chute_permutation`
    ne rend NaN que si AUCUNE cellule n'atteint dix personnes. Sur 94 personnes et une
    segmentation genre x race x age a 38 cases, une seule cellule atteint dix : la
    quantite reste definie mais elle est portee par des cellules de trois a sept
    personnes, ou permuter est presque l'identite. Ce tableau le rend lisible.
    """
    out = []
    for nom, avec, sans in (("H1", "C3E", "C3"), ("H2", "C2", "C2S")):
        lignes = np.array(sorted(set(infos[avec]["lignes"]) & set(infos[sans]["lignes"])))
        for nom_seg in ("S_ideo", "S_gra"):
            s = segs[nom_seg][lignes]
            t = sorted([int((s == k).sum()) for k in np.unique(s) if k >= 0],
                       reverse=True)
            out.append({"contraste": nom, "personnes": len(lignes),
                        "segmentation": nom_seg, "cases non vides": len(t),
                        "cases >= 10 personnes": sum(1 for x in t if x >= 10),
                        "cases >= 5 personnes": sum(1 for x in t if x >= 5),
                        "taille max": t[0] if t else 0,
                        "personnes dans les cases >= 10":
                            sum(x for x in t if x >= 10),
                        "tailles": " ".join(str(x) for x in t)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--tirages", type=int, default=2000)
    ap.add_argument("--permutations", type=int, default=200)
    ap.add_argument("--personnes-min", type=int, default=30)
    ap.add_argument("--pas", type=int, default=500)
    ap.add_argument("--suffixe", default="")
    args = ap.parse_args()

    t0 = time.time()
    print("chargement du paquet (caches de a25, a28 et a35)", flush=True)
    paquet = C44.charger(args.cache, args.cache_foret, args.cache_a35)
    items = paquet["items"]
    colonnes = np.array(sorted({j for _n, cols in groupes_familles(items) for j in cols}))
    segs = R3.segmentations_r3(paquet)
    table = nomenclature()

    infos = {}
    couverture = []
    for nom, fichier, condition in R3.TRACES_R3:
        chemin = os.path.join(TRACES, fichier)
        info = R3.matrice_depuis_trace(paquet, chemin, condition, table, colonnes)
        if info is None:
            print(f"  trace absente : {chemin}", flush=True)
            continue
        paquet["M"][nom] = info["matrice"]
        infos[nom] = info
        m = info["matrice"][info["lignes"]]
        couverts = [j for j in range(len(items)) if np.any(m[:, j] is not None
                                                           or m[:, j] != None)]  # noqa
        couverts = [j for j in range(len(items)) if np.any(m[:, j] != None)]  # noqa: E711
        couverture.append({
            "condition": nom, "trace": fichier,
            "personnes completes": len(info["personnes"]),
            "items couverts": len(couverts),
            "items couverts hors des 58 familles":
                len(set(couverts) - set(colonnes.tolist())),
            "appels lus": info["appels"]})
        print(f"  {nom} : {len(info['personnes'])} personnes, "
              f"{len(couverts)} items couverts dont "
              f"{len(set(couverts) - set(colonnes.tolist()))} hors des 58 familles",
              flush=True)

    tab, con = [], []
    for nom, avec, sans, _quoi in R3.CONTRASTES:
        if avec in infos and sans in infos:
            a, b = contraste_rarete(nom, avec, sans, paquet, infos, colonnes, segs, args)
            tab += a
            con += b

    # Holm sur la seule famille que ce script ajoute : les quatre quantites de rarete,
    # par contraste. Elle n'est PAS preenregistree ; elle repare le perimetre d'items de
    # quantites qui l'etaient, et elle est publiee comme telle.
    for nom in {c["contraste"] for c in con}:
        sel = [c for c in con if c["contraste"] == nom and c["mesure"] in CLES_RARETE]
        ps = [c["p_bootstrap"] for c in sel]
        for c, ph, pb in zip(sel, C44.holm(ps), C44.benjamini_hochberg(ps)):
            c["p_holm (famille de reparation, non preenregistree)"] = ph
            c["p_bh"] = pb

    print("\n=== plancher humain et parts, memes personnes, memes 58 items ===",
          flush=True)
    parts = plancher_et_parts(paquet, infos, colonnes, segs, args)

    s = args.suffixe
    C44.ecrire(couverture, os.path.join(SORTIE, f"r3b-couverture-items{s}.csv"))
    C44.ecrire(tab, os.path.join(SORTIE, f"r3b-rarete-appariee{s}.csv"))
    C44.ecrire(con, os.path.join(SORTIE, f"r3b-contrastes-rarete{s}.csv"))
    C44.ecrire(parts, os.path.join(SORTIE, f"r3b-plancher-humain{s}.csv"))
    C44.ecrire(tailles_de_segments(infos, colonnes, segs),
               os.path.join(SORTIE, f"r3b-segments{s}.csv"))
    print(f"\nduree {time.time() - t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
