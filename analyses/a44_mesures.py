"""
a44_mesures : le generateur nul conditionnellement independant de Yuan, applique aux
seize populations du dossier.

===========================================================================
PREENREGISTREMENT : resultats/a44-preenregistrement.md, ecrit le 8 septembre 2026 a
15 h 46 CEST, AVANT ce script et avant tout calcul. Les quantites, les segmentations, la
famille de tests, le nombre de replicats, la quantite primaire du verdict et les six
predictions y sont figes. Ce script ne fait que les executer.

QUESTION POSEE
--------------
Yuan (arXiv 2607.02368 v3) montre qu'un signal de groupe dans les sorties d'un modele est
entierement reproduit par un generateur qui tire chaque reponse independamment dans la
distribution du groupe. Notre gonflement inter, 8,16 pour C2 sur l'axe ideologie et 5,9
pour v8, et notre ecrasement intra, 0,365 pour C2, sont ils reproduits de la meme facon ?

SORTIES, toutes dans resultats/
-------------------------------
  a44-controles.csv        les deux controles bloquants et la reproduction de a31 et a29
  a44-quantites.csv        les sept quantites, population contre son generateur nul
  a44-verdicts.csv         le verdict par condition sur la quantite primaire Q5
  a44-permutation.csv      les trois proprietes de Yuan transposees
  a44-rarete.csv           Q6 et Q7 en detail
  et un resume imprime sur la sortie standard.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/a44_mesures.py --replicats 200 --bootstrap 1000
===========================================================================
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np

import a44_commun as C


def rng_replicat(id_cond, id_seg, r):
    """Graine reproductible d'un replicat nul, fonction de la condition, de la
    segmentation et du numero de replicat, jamais de l'ordre d'execution."""
    return np.random.default_rng([C.GRAINE, id_cond, id_seg, r])


def exactitude_codes(pred, verite):
    """Exactitude par personne sur codes entiers.

    Une cellule compte au denominateur des que la verite humaine est observee ; une
    prediction absente ou hors nomenclature vaut -1 et compte comme fausse. C'est la
    convention de a2 et de a29, et l'egalite avec a2_commun.exactitude_par_personne est
    verifiee dans les controles.
    """
    den = verite >= 0
    juste = den & (pred == verite)
    n = den.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, juste.sum(axis=1) / np.maximum(n, 1), np.nan)


def reassignation_codes(pred, verite, seg):
    """Exactitude sous le meilleur appariement des personnes a l'interieur du segment.

    Analogue de RO-BTSP de Yuan, avec la reserve ecrite au preenregistrement section 6 :
    le realignement de Yuan est tire au hasard, celui ci est optimise sur les donnees. Il
    borne par le haut ce qu'un gabarit de groupe atteint en choisissant son alignement
    apres coup. Descriptif, il ne fonde aucun verdict.
    """
    from scipy.optimize import linear_sum_assignment
    ok = verite >= 0
    total, compte = 0.0, 0
    for k in np.unique(seg):
        if k < 0:
            continue
        li = np.flatnonzero(seg == k)
        if len(li) < 2:
            continue
        p, v, o = pred[li], verite[li], ok[li]
        gain = np.zeros((len(li), len(li)))
        for a in range(len(li)):
            gain[:, a] = ((p == v[a][None, :]) & o[a][None, :]).sum(axis=1) \
                / max(int(o[a].sum()), 1)
        r, c = linear_sum_assignment(-gain)
        total += gain[r, c].sum()
        compte += len(li)
    return total / compte if compte else np.nan


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--replicats", type=int, default=C.N_REPLICATS)
    ap.add_argument("--bootstrap", type=int, default=C.N_BOOTSTRAP)
    ap.add_argument("--permutations", type=int, default=C.N_PERMUTATIONS)
    args = ap.parse_args()

    t0 = time.time()
    print(__doc__.split("=" * 75)[1], flush=True)
    paquet = C.charger(args.cache, args.cache_foret, args.cache_a35)
    items, options = paquet["items"], paquet["options"]
    alpha = C.alphabet(items, options)
    k_items = np.array([len(options[it]) for it in items], dtype=np.int32)
    k_max = int(k_items.max())
    colonnes = np.arange(len(items))
    seg_tous, niveaux = C.segmentations(paquet)
    l150 = np.asarray(paquet["lignes150"])
    per = {"1052": np.arange(len(paquet["ids"])), "150": l150}
    sous_ens = C.sous_ensembles_items(len(items))

    conditions = [c for c in C.TOUTES if c in paquet["M"]]
    print(f"{len(paquet['ids'])} personnes, {len(items)} items, "
          f"{len(conditions)} conditions ; absentes : {paquet['absentes'] or 'aucune'}",
          flush=True)

    # --------------------------------------------------------------- codage
    codes, hors = {}, {}
    for nom in conditions:
        codes[nom], hors[nom] = C.coder(paquet["M"][nom], alpha)

    controles = []
    for nom in conditions:
        controles.append({"controle": "part de cellules hors nomenclature",
                          "objet": nom, "valeur": round(hors[nom], 6), "seuil": 0.005,
                          "passe": bool(hors[nom] < 0.005)})

    # controle : l'exactitude sur codes egale celle de a2 sur les chaines
    ecart_exact = 0.0
    for nom in conditions:
        a = np.nanmean(exactitude_codes(codes[nom][per["1052"]],
                                        codes["humains vague 1"][per["1052"]]))
        b = np.nanmean(C.exactitude(paquet["M"][nom], paquet["M"]["humains vague 1"]))
        ecart_exact = max(ecart_exact, abs(a - b))
    controles.append({"controle": "exactitude sur codes egale a celle de a2 sur chaines",
                      "objet": "toutes conditions", "valeur": round(ecart_exact, 9),
                      "seuil": 1e-6, "passe": bool(ecart_exact < 1e-6)})

    # --------------------------------------------- controle bloquant 2, invariance
    rng = np.random.default_rng(C.GRAINE)
    pire = 0.0
    for nom in conditions:
        for nom_seg in ("S_fin", "S_ideo"):
            lignes = per[C.PERIMETRE[nom]]
            s = seg_tous[nom_seg][lignes]
            cd = codes[nom][lignes]
            avant = C.dispersion(cd, s, k_max, colonnes)["inter"]
            p = C.permuter_intra(len(lignes), s, rng)
            apres = C.dispersion(cd[p], s, k_max, colonnes)["inter"]
            pire = max(pire, abs(avant - apres))
    controles.append({"controle": "ratio inter invariant sous permutation intra segment",
                      "objet": "toutes conditions x deux segmentations",
                      "valeur": float(pire), "seuil": 1e-12, "passe": bool(pire < 1e-12)})

    # --------------------------------------------- controle bloquant 1, marginales
    #
    # Le preenregistrement demande que le nul redonne les marginales PAR ITEM ET PAR
    # SEGMENT, ecart MOYEN inferieur a 0,01. C'est ce qui est calcule ici, sur les couples
    # (item, segment) que la regle de repli n'a pas touches, puisque sur les autres le nul
    # tire par construction dans la marginale de l'item et non dans celle du segment.
    # L'effet du repli sur la marginale d'item est mesure a part et publie : c'est une
    # limite reelle du dispositif sur le perimetre a 150 personnes, pas un controle.
    ecarts_seg, ecarts_item, cumules = [], [], {}
    replis = []
    n_ctrl = max(1, min(100, args.replicats))
    for i_c, nom in enumerate(conditions):
        lignes = per[C.PERIMETRE[nom]]
        cd = codes[nom][lignes]
        for i_s, nom_seg in enumerate(("S_fin", "S_ideo")):
            s = seg_tous[nom_seg][lignes]
            cum, rep, tot = C.lois_par_segment(cd, s, k_items)
            cumules[(nom, nom_seg)] = cum
            acc = np.stack([C.tirer_nul(cd, s, cum, rng_replicat(i_c, i_s, r))
                            for r in range(n_ctrl)])       # (n_ctrl, n, m)
            e_seg, e_item = [], []
            for j in range(len(items)):
                ok = cd[:, j] >= 0
                if ok.sum() < C.N_MIN_ITEM:
                    continue
                col_nul = acc[:, :, j]
                p_vrai = np.bincount(cd[ok, j], minlength=k_items[j]) / ok.sum()
                p_nul = (np.bincount(col_nul[:, ok].ravel(), minlength=k_items[j])
                         / (ok.sum() * n_ctrl))
                e_item.append(float(np.abs(p_vrai - p_nul).mean()))
                for k in np.unique(s[s >= 0]):
                    m = ok & (s == k)
                    if m.sum() < C.N_MIN_SEGMENT:
                        continue          # segment replie, le nul n'y suit pas le segment
                    q_v = np.bincount(cd[m, j], minlength=k_items[j]) / m.sum()
                    q_n = (np.bincount(col_nul[:, m].ravel(), minlength=k_items[j])
                           / (m.sum() * n_ctrl))
                    e_seg.append(float(np.abs(q_v - q_n).mean()))
            replis.append({
                "condition": nom, "segmentation": nom_seg,
                "perimetre": C.PERIMETRE[nom],
                "couples_item_segment": tot, "replis_marginale": rep,
                "part_repliee": round(rep / max(tot, 1), 4),
                "ecart_moyen_marginale_segment": float(np.mean(e_seg)) if e_seg else
                np.nan,
                "ecart_moyen_marginale_item": float(np.mean(e_item)) if e_item else
                np.nan})
            ecarts_seg += e_seg
            ecarts_item += e_item
    moy_seg = float(np.mean(ecarts_seg))
    controles.append({"controle": "marginale item x segment du nul egale a celle de la "
                                  "condition, ecart moyen",
                      "objet": f"couples non replies, {n_ctrl} replicats",
                      "valeur": round(moy_seg, 6), "seuil": 0.01,
                      "passe": bool(moy_seg < 0.01)})
    controles.append({"controle": "effet du repli sur la marginale d'item, ecart moyen",
                      "objet": "descriptif, pas un controle",
                      "valeur": round(float(np.mean(ecarts_item)), 6), "seuil": np.nan,
                      "passe": True})

    for c in controles:
        if not c["passe"]:
            print("CONTROLE ECHOUE :", c, flush=True)
    C.ecrire(controles, "a44-controles.csv")
    C.ecrire(replis, "a44-replis-segments.csv")
    if not all(c["passe"] for c in controles if c["controle"].startswith(
            ("ratio inter invariant", "marginale item x segment",
             "exactitude sur codes"))):
        sys.exit("un controle bloquant a echoue, rien n'est publie au dela")
    print(f"controles passes, {time.time() - t0:.0f}s", flush=True)

    # ------------------------------------------------------------- Q6 et Q7
    cv = {}
    for nom_per, lignes in per.items():
        cv[nom_per] = C.covariables_rarete(paquet["M"]["humains vague 1"][lignes],
                                           seg_tous["political_ideology"][lignes])

    # ------------------------------------------------- boucle principale
    lignes_q, lignes_rar = [], []
    for i_c, nom in enumerate(conditions):
        nom_per = C.PERIMETRE[nom]
        lignes = per[nom_per]
        cd = codes[nom][lignes]
        y1 = codes["humains vague 1"][lignes]
        for i_s, nom_seg in enumerate(("S_fin", "S_ideo")):
            s = seg_tous[nom_seg][lignes]
            s_ideo = seg_tous["S_ideo"][lignes]
            cum = cumules[(nom, nom_seg)]

            reel = {}
            r_app = C.ratios(cd, y1, s, k_max, colonnes)
            r_ideo = C.ratios(cd, y1, s_ideo, k_max, colonnes)
            reel["Q1 ratio inter, axe du nul"] = r_app["inter"]
            reel["Q2 ratio intra, axe du nul"] = r_app["intra"]
            reel["Q1b ratio inter, axe ideologie"] = r_ideo["inter"]
            reel["Q2b ratio intra, axe ideologie"] = r_ideo["intra"]
            reel["Q3 patrons distincts"] = C.patrons_distincts(cd, sous_ens)[0]
            reel["Q4 correlation inter items"] = C.correlation_items(cd, colonnes)[0]
            reel["Q5 correlation residualisee"] = C.correlation_items(cd, colonnes, s)[0]
            g = C.groupe_sur_personne(paquet["M"][nom][lignes], cv[nom_per])
            reel["Q6 rapport groupe sur personne"] = g["groupe_sur_personne"]
            reel["Q7 rappel des cellules rares"] = g["rappel_rares"]

            acc = {k: [] for k in reel}
            acc_lift = {"lift_personne": [], "lift_segment": []}
            for r in range(args.replicats):
                nul = C.tirer_nul(cd, s, cum, rng_replicat(i_c, i_s, r))
                ra = C.ratios(nul, y1, s, k_max, colonnes)
                ri = C.ratios(nul, y1, s_ideo, k_max, colonnes)
                acc["Q1 ratio inter, axe du nul"].append(ra["inter"])
                acc["Q2 ratio intra, axe du nul"].append(ra["intra"])
                acc["Q1b ratio inter, axe ideologie"].append(ri["inter"])
                acc["Q2b ratio intra, axe ideologie"].append(ri["intra"])
                acc["Q3 patrons distincts"].append(C.patrons_distincts(nul, sous_ens)[0])
                acc["Q4 correlation inter items"].append(
                    C.correlation_items(nul, colonnes)[0])
                acc["Q5 correlation residualisee"].append(
                    C.correlation_items(nul, colonnes, s)[0])
                if r < 50:            # Q6 et Q7 : 50 replicats, cf. rapport section 3
                    gn = C.groupe_sur_personne(
                        C.decoder(nul, options, items), cv[nom_per])
                    acc["Q6 rapport groupe sur personne"].append(
                        gn["groupe_sur_personne"])
                    acc["Q7 rappel des cellules rares"].append(gn["rappel_rares"])
                    acc_lift["lift_personne"].append(gn["lift_personne"])
                    acc_lift["lift_segment"].append(gn["lift_segment"])

            for q, v in reel.items():
                t = np.array([z for z in acc[q] if np.isfinite(z)], dtype=float)
                moy = float(t.mean()) if len(t) else np.nan
                sd = float(t.std(ddof=1)) if len(t) > 1 else np.nan
                lignes_q.append({
                    "perimetre": nom_per, "segmentation": nom_seg, "condition": nom,
                    "quantite": q, "reel": v, "nul_moyenne": moy,
                    "nul_bas": float(np.percentile(t, 2.5)) if len(t) else np.nan,
                    "nul_haut": float(np.percentile(t, 97.5)) if len(t) else np.nan,
                    "nul_ecart_type": sd, "replicats": int(len(t)),
                    "d": v - moy if np.isfinite(moy) else np.nan,
                    "z": ((v - moy) / sd) if (np.isfinite(sd) and sd > 0) else np.nan,
                    "part_reproduite": (moy / v) if (np.isfinite(moy) and v not in
                                                     (0, np.nan) and v != 0) else np.nan})

            lignes_rar.append({
                "perimetre": nom_per, "segmentation": nom_seg, "condition": nom,
                "lift_personne": g["lift_personne"], "lift_segment": g["lift_segment"],
                "groupe_sur_personne": g["groupe_sur_personne"],
                "rappel_rares": g["rappel_rares"],
                "fausses_raretes": g["fausses_raretes"],
                "raretes_osees": g["raretes_osees"],
                "nul_lift_personne": float(np.nanmean(acc_lift["lift_personne"])),
                "nul_lift_segment": float(np.nanmean(acc_lift["lift_segment"])),
                "nul_groupe_sur_personne": float(np.nanmean(
                    [z for z in acc["Q6 rapport groupe sur personne"]
                     if np.isfinite(z)])),
                "nul_rappel_rares": float(np.nanmean(
                    acc["Q7 rappel des cellules rares"]))})
        print(f"  {nom} mesure, {time.time() - t0:.0f}s", flush=True)

    # ---------------------------------------------- bootstrap sur les personnes
    print("bootstrap sur les personnes", flush=True)
    boot = {}
    rng_b = np.random.default_rng(C.GRAINE + 1)
    idx_boot = {k: rng_b.integers(0, len(v), (args.bootstrap, len(v)))
                for k, v in per.items()}
    for i_c, nom in enumerate(conditions):
        nom_per = C.PERIMETRE[nom]
        lignes = per[nom_per]
        cd, y1 = codes[nom][lignes], codes["humains vague 1"][lignes]
        for i_s, nom_seg in enumerate(("S_fin", "S_ideo")):
            s = seg_tous[nom_seg][lignes]
            s_ideo = seg_tous["S_ideo"][lignes]
            cum = cumules[(nom, nom_seg)]
            tir = {q: [] for q in ("Q1 ratio inter, axe du nul",
                                   "Q2 ratio intra, axe du nul",
                                   "Q1b ratio inter, axe ideologie",
                                   "Q4 correlation inter items",
                                   "Q5 correlation residualisee")}
            for b in range(args.bootstrap):
                ix = idx_boot[nom_per][b]
                nul = C.tirer_nul(cd, s, cum, rng_replicat(i_c, i_s, b % args.replicats))
                cdb, nub, y1b = cd[ix], nul[ix], y1[ix]
                sb, sib = s[ix], s_ideo[ix]
                ra, rn = (C.ratios(cdb, y1b, sb, k_max, colonnes),
                          C.ratios(nub, y1b, sb, k_max, colonnes))
                ri, rin = (C.ratios(cdb, y1b, sib, k_max, colonnes),
                           C.ratios(nub, y1b, sib, k_max, colonnes))
                tir["Q1 ratio inter, axe du nul"].append(ra["inter"] - rn["inter"])
                tir["Q2 ratio intra, axe du nul"].append(ra["intra"] - rn["intra"])
                tir["Q1b ratio inter, axe ideologie"].append(ri["inter"] - rin["inter"])
                tir["Q4 correlation inter items"].append(
                    C.correlation_items(cdb, colonnes)[0]
                    - C.correlation_items(nub, colonnes)[0])
                tir["Q5 correlation residualisee"].append(
                    C.correlation_items(cdb, colonnes, sb)[0]
                    - C.correlation_items(nub, colonnes, sb)[0])
            for q, v in tir.items():
                boot[(nom_per, nom_seg, nom, q)] = C.ic_percentile(v)
        print(f"  {nom} bootstrap, {time.time() - t0:.0f}s", flush=True)

    for ligne in lignes_q:
        cle = (ligne["perimetre"], ligne["segmentation"], ligne["condition"],
               ligne["quantite"])
        b, h, p = boot.get(cle, (np.nan, np.nan, np.nan))
        ligne["d_ic_bas"], ligne["d_ic_haut"], ligne["p"] = b, h, p
    C.ecrire(lignes_q, "a44-quantites.csv")
    C.ecrire(lignes_rar, "a44-rarete.csv")

    # ------------------------------------------------------------- verdicts
    famille = [l for l in lignes_q
               if l["quantite"] == "Q5 correlation residualisee"
               and l["segmentation"] == "S_fin"
               and l["condition"] in C.CONDITIONS]
    p_ajuste = C.holm([l["p"] for l in famille])
    p_bh = C.benjamini_hochberg([l["p"] for l in famille])
    verdicts = []
    for l, pa, pb in zip(famille, p_ajuste, p_bh):
        for nom_seg in ("S_fin", "S_ideo"):
            m = [z for z in lignes_q
                 if z["condition"] == l["condition"] and z["segmentation"] == nom_seg
                 and z["quantite"] == "Q5 correlation residualisee"][0]
            if nom_seg == "S_fin":
                verdict = ("gabarit de groupe" if not np.isfinite(m["d_ic_bas"])
                           or (m["d_ic_bas"] <= 0 <= m["d_ic_haut"])
                           else ("porteur de personne" if m["d_ic_bas"] > 0
                                 else "anti structure"))
            else:
                verdict = ""
            verdicts.append({
                "condition": l["condition"], "perimetre": l["perimetre"],
                "segmentation": nom_seg, "Q5_reel": m["reel"],
                "Q5_nul": m["nul_moyenne"], "d": m["d"], "z": m["z"],
                "d_ic_bas": m["d_ic_bas"], "d_ic_haut": m["d_ic_haut"],
                "p": m["p"], "p_holm": pa if nom_seg == "S_fin" else np.nan,
                "p_bh": pb if nom_seg == "S_fin" else np.nan,
                "verdict": verdict})
    C.ecrire(verdicts, "a44-verdicts.csv")

    # ----------------------------------------- les trois proprietes de Yuan
    print("permutation intra segment", flush=True)
    rng_p = np.random.default_rng(C.GRAINE + 2)
    lignes_perm = []
    for nom in conditions:
        nom_per = C.PERIMETRE[nom]
        lignes = per[nom_per]
        cd, y1 = codes[nom][lignes], codes["humains vague 1"][lignes]
        vraie = float(np.nanmean(exactitude_codes(cd, y1)))
        for nom_seg in ("S_fin", "S_ideo"):
            s = seg_tous[nom_seg][lignes]
            perms = []
            for _ in range(args.permutations):
                p = C.permuter_intra(len(lignes), s, rng_p)
                perms.append(float(np.nanmean(exactitude_codes(cd[p], y1))))
            perms = np.array(perms)
            opt = reassignation_codes(cd, y1, s)
            lignes_perm.append({
                "condition": nom, "perimetre": nom_per, "segmentation": nom_seg,
                "exactitude_vraie": vraie,
                "exactitude_permutee": float(perms.mean()),
                "permutee_bas": float(np.percentile(perms, 2.5)),
                "permutee_haut": float(np.percentile(perms, 97.5)),
                "chute": vraie - float(perms.mean()),
                "chute_relative": (vraie - float(perms.mean())) / vraie if vraie else
                np.nan,
                "exactitude_reassignation_optimale": opt,
                "part_recuperee_par_reassignation":
                    ((opt - float(perms.mean())) / (vraie - float(perms.mean())))
                    if abs(vraie - float(perms.mean())) > 1e-9 else np.nan,
                "permutations": args.permutations})
        print(f"  {nom} permutation, {time.time() - t0:.0f}s", flush=True)
    C.ecrire(lignes_perm, "a44-permutation.csv")

    print(f"\ntermine en {time.time() - t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
