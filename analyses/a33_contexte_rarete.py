"""
a33_contexte_rarete : la fausse rarete vient elle d'un contexte insuffisant ?

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a33_commun, a31_commun, a31_mecanismes,
a29_commun, a28_commun, a25_commun, a25_mesures, a8_commun, a2_commun, a2_baselines_gss,
a5_evaluer et a5_agents_locaux_gss sont importes tels quels, memes graines, memes plis,
memes blocs, memes 149 items, memes personnes.

a31 laisse H5 indecidable et dit pourquoi : ses deux mesures de contexte, la rarete du
contexte de H5 et la rarete de la personne de H1b, sont numeriquement presque la meme
quantite, 0,0439 contre 0,0436 pour agents composite. Il faut une condition dont le
CONTEXTE varie a PERSONNE CONSTANTE. C3F est exactement cela et n'avait jamais ete
exploitee : meme modele, memes personnes, memes items, meme chaine de scoring que C3,
mais le contexte du prompt est ampute de la famille thematique entiere de l'item cible.

Le fait de structure a avoir en tete avant toute lecture, et qui est mesure en section 1
du rapport : l'amputation de C3F n'est pas une reduction de VOLUME. C3 voit 119 ou 120
items, les 149 moins son bloc secret ; C3F en voit 132 a 144, les 149 moins la famille.
C3F voit donc PLUS d'items que C3, et zero cousin thematique contre 8,7 en moyenne pour
C3. Ce qui est retire, c'est l'information la plus proche de la question, pas la
quantite d'information.

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT LES RESULTATS
===========================================================================
Perimetre declare : les 60 personnes completes de la trace C3F et les 58 items des six
familles thematiques de a2_baselines_gss, soit 3 480 cellules, restreintes aux cellules
dont la reponse de la vague 1 est observee ET que C3 et C3F predisent toutes les deux.
Toutes les conditions sont evaluees sur CES cellules la et sur aucune autre.

Seuil declare : 10 pour cent. Reference de minorite declaree : la population des 1 052
personnes du perimetre GSS, et non les 60 du perimetre. Motif ecrit avant execution : sur
60 personnes, un seuil de 10 pour cent porte sur six repondants et la rarete d'un segment
ideologique serait estimee sur huit personnes en moyenne. La variante calculee sur les
150 personnes du run et la variante a 20 pour cent sont rapportees comme sensibilites,
hors famille.

Unite d'analyse declaree : la FAUSSE RARETE, memes definitions que a29 et a31, c'est a
dire une cellule ou la methode predit une modalite minoritaire et ou la personne a en
realite donne une modalite majoritaire.

L'HYPOTHESE TESTEE, H5 de a31 : la fausse rarete vient d'un contexte insuffisant. La
condition C3F ampute le contexte a personne constante. Les deux predictions concurrentes
sont ecrites avant l'execution.

  SI H5 EST VRAIE : C3F pose PLUS de fausses raretes que C3 sur les memes cellules, et
  son rapport groupe sur personne est PLUS ELEVE, parce qu'un modele prive de
  l'information propre a la personne retombe sur la regularite de groupe meme sans
  etiquette demographique.

  SI H2 SEULE EST VRAIE, c'est a dire si la rarete de groupe est un effet de l'etiquette
  et non du manque d'information : le taux de fausses raretes et le rapport groupe sur
  personne ne bougent pas, et seule l'exactitude baisse.

Les sept contrastes declares, tous C3F MOINS C3, memes cellules, memes personnes.

  P1  exactitude argmax.
  P2  taux de fausses raretes, part des raretes osees posees sur une personne qui a
      repondu majoritairement.
  P3  rappel des cellules minoritaires.
  P4  precision des cellules minoritaires.
  P5  H1b, moyenne chez les fausses raretes du taux de reponses rares reelles de la
      PERSONNE hors de l'item.
  P6  H2b, moyenne chez les fausses raretes du taux de reponses rares reelles du SEGMENT
      ideologique de la personne sur cet item, calcule sans la personne.
  P7  H2a, part des fausses raretes dont la modalite predite est la modalite rare MODALE
      du segment, sur les items qui portent au moins deux modalites minoritaires.

  FAMILLE PRIMAIRE DECLAREE : P1 a P7, soit 7 tests, corriges par Holm, valide sans
  hypothese sur la dependance, ce qui est necessaire puisque les sept contrastes portent
  sur les memes personnes et les memes cellules. Benjamini Hochberg est rapporte a cote.

  FAMILLE SECONDAIRE DECLAREE : l'exces contre le TEMOIN AVEUGLE A LA PERSONNE, pour
  chacune des deux conditions et pour chacun des deux cotes, soit 4 tests, corriges
  separement par Holm. Le temoin est celui de a31 : il pose exactement le meme nombre de
  fausses raretes sur exactement les memes items, chez des personnes tirees au hasard
  parmi les repondants de l'item.

  N'ENTRENT DANS AUCUNE FAMILLE, et sont des descriptions : le rapport groupe sur
  personne, qui est un rapport de deux lifts dont aucun n'est teste directement, comme
  a31 section 8 l'interdit explicitement ; les lifts eux memes ; le seuil de 20 pour
  cent ; la reference de minorite calculee sur les 150 ; le detail par famille
  thematique ; la taille et la rarete du contexte reellement vu ; les quintiles ; la
  confiance et l'entropie des distributions ; le controle B2 famille retiree ; et toutes
  les lignes des conditions autres que C3 et C3F, qui sont des points de repere sur les
  memes cellules et non des tests.

  Tous les p sont des p de bootstrap apparie sur les PERSONNES, 4 000 tirages, lus sur la
  position de zero dans la distribution ; ils ne descendent jamais sous 1 / 4 000 =
  0,00025. Avec 7 tests le plancher de Holm vaut 0,00175, avec 4 tests il vaut 0,001. Le
  bootstrap porte sur les 60 personnes et jamais sur les cellules : deux reponses d'une
  meme personne ne sont pas independantes.
===========================================================================

Entree  : paquet OSF t6g7k, data/traces/a5-C3F-p1.jsonl, a5-C3-p1.jsonl, a5-C2-p1.jsonl,
          cache de matrices de a25 et cache de la foret aleatoire de a28.
Sortie  : resultats/a33-mesures.csv, a33-contrastes.csv, a33-leviers-personne-segment.csv,
          a33-par-famille.csv, a33-contexte.csv, a33-confiance.csv, a33-controles.csv,
          a33-cousins.csv, a33-sensibilites.csv.

Usage :
  .venv/bin/python analyses/a33_contexte_rarete.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 4000
"""

import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a33_commun as C
from a2_baselines_gss import FAMILLES
from a2_commun import profil_diversite


def lift_ic(num_v, den_v, num_t, den_t, idx_boot):
    """Lift sur le temoin aveugle et son intervalle bootstrap sur les personnes.

    Le lift n'est jamais teste, a31 section 8 point 6 l'interdit : les tests portent sur
    les valeurs et non sur les rapports a un temoin. L'intervalle sert uniquement a
    montrer au lecteur combien la quantite est mal determinee sur ce perimetre.
    """
    v, t = C.taux(num_v, den_v), C.taux(num_t, den_t)
    obs = v / t - 1.0 if (t and np.isfinite(v)) else np.nan
    dv, dt = den_v[idx_boot].sum(axis=1), den_t[idx_boot].sum(axis=1)
    nv, nt = num_v[idx_boot].sum(axis=1), num_t[idx_boot].sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        tir = (np.where(dv > 0, nv / np.maximum(dv, 1e-12), np.nan)
               / np.where(dt > 0, nt / np.maximum(dt, 1e-12), np.nan)) - 1.0
    return obs, tir


def mesures_condition(nom, cv, m, base, idx_boot, pmax=None):
    """Toutes les quantites d'une condition sur le perimetre apparie.

    base : masque des cellules retenues, identique pour toutes les conditions.
    m    : masques de a31_mecanismes.masques_condition, deja restreints au perimetre.
    """
    pred, verite = m["pred"], cv["verite"]
    dispo = C.observe(pred)
    ok_acc = base & dispo
    juste_acc = ok_acc & (pred == verite)
    num_acc, den_acc = C.par_personne(juste_acc, ok_acc)
    acc, acc_b, acc_h, _ = C.taux_ic(num_acc, den_acc, idx_boot)

    rare_pred = m["rare_pred"] & base
    juste = m["juste"] & base
    faux_maj = m["faux_maj"] & base
    faux_min = m["faux_min"] & base
    rare_vrai = cv["rare_vrai"] & base

    n_rp = C.par_personne(rare_pred, base)[0]
    n_rv = C.par_personne(rare_vrai, base)[0]
    n_ju = C.par_personne(juste, base)[0]
    n_fm = C.par_personne(faux_maj, base)[0]

    rappel, rap_b, rap_h, _ = C.taux_ic(n_ju, n_rv, idx_boot)
    prec, pre_b, pre_h, _ = C.taux_ic(n_ju, n_rp, idx_boot)
    tfr, tfr_b, tfr_h, _ = C.taux_ic(n_fm, n_rp, idx_boot)
    f1 = (2 * rappel * prec / (rappel + prec)) if (rappel and prec
                                                   and (rappel + prec) > 0) else 0.0

    ligne = {"condition": nom,
             "cellules": int(base.sum()),
             "cellules_predites": int(ok_acc.sum()),
             "refus": int((base & ~dispo).sum()),
             "exactitude": acc, "exactitude_ic_bas": acc_b, "exactitude_ic_haut": acc_h,
             "cellules_minoritaires_reelles": int(rare_vrai.sum()),
             "raretes_osees": int(rare_pred.sum()),
             "raretes_justes": int(juste.sum()),
             "fausses_raretes": int(faux_maj.sum()),
             "mauvaise_modalite_rare": int(faux_min.sum()),
             "rappel": rappel, "rappel_ic_bas": rap_b, "rappel_ic_haut": rap_h,
             "precision": prec, "precision_ic_bas": pre_b, "precision_ic_haut": pre_h,
             "f1": f1,
             "taux_fausses_raretes": tfr, "tfr_ic_bas": tfr_b, "tfr_ic_haut": tfr_h,
             "masse_predite": float(rare_pred.sum()) / max(int(base.sum()), 1),
             "masse_humaine": float(rare_vrai.sum()) / max(int(base.sum()), 1)}

    # Ecrasement de la variance sur les memes cellules : la part de diversite humaine
    # conservee et l'accord par paires, calcules par a2_commun.profil_diversite.
    div = profil_diversite(np.where(ok_acc, pred, None), np.where(base, verite, None))
    ligne["part_diversite_humaine"] = div["part_diversite_humaine"]
    ligne["accord_par_paires"] = div["accord_par_paires"]

    # H1b et H2b : valeur chez les fausses raretes, temoin aveugle a la personne, lift.
    tirages_lift = {}
    for cle, mat in (("personne", cv["r_personne"]),
                     ("segment", cv["r_segment"][C.AXE_PRINCIPAL])):
        num, den = C.moyenne_par_personne(faux_maj, mat)
        v, b, h, _ = C.taux_ic(num, den, idx_boot)
        tem = C.temoin_item(faux_maj, base, mat)
        num_t, den_t = C.temoin_par_personne(faux_maj, base, mat)
        lf, tir = lift_ic(num, den, num_t, den_t, idx_boot)
        tirages_lift[cle] = tir
        ligne[f"h_{cle}_valeur"] = v
        ligne[f"h_{cle}_ic_bas"] = b
        ligne[f"h_{cle}_ic_haut"] = h
        ligne[f"h_{cle}_temoin"] = tem
        ligne[f"h_{cle}_lift"] = lf
        fini = tir[np.isfinite(tir)]
        ligne[f"h_{cle}_lift_ic_bas"] = (float(np.percentile(fini, 2.5))
                                         if len(fini) else np.nan)
        ligne[f"h_{cle}_lift_ic_haut"] = (float(np.percentile(fini, 97.5))
                                          if len(fini) else np.nan)

    lp, ls = ligne["h_personne_lift"], ligne["h_segment_lift"]
    ligne["rapport_groupe_sur_personne"] = ls / lp if (np.isfinite(lp) and lp > 0) else np.nan
    with np.errstate(invalid="ignore", divide="ignore"):
        r = tirages_lift["segment"] / tirages_lift["personne"]
    r = r[np.isfinite(r)]
    ligne["rapport_ic_bas"] = float(np.percentile(r, 2.5)) if len(r) else np.nan
    ligne["rapport_ic_haut"] = float(np.percentile(r, 97.5)) if len(r) else np.nan

    # H2a : part des fausses raretes egales a la modale rare du segment.
    num, den = C.mesure_h2a(cv, {"faux_maj": faux_maj, "pred": pred}, C.AXE_PRINCIPAL,
                            cv["modale_seg"][C.AXE_PRINCIPAL])
    v, b, h, _ = C.taux_ic(num, den, idx_boot)
    ligne.update({"h2a_cellules": int(den.sum()), "h2a_valeur": v,
                  "h2a_ic_bas": b, "h2a_ic_haut": h})

    if pmax is not None:
        sel = faux_maj & ~np.isnan(pmax)
        ligne["p_max_moyen_fausses_raretes"] = (float(pmax[sel].mean())
                                                if sel.any() else np.nan)
    return ligne


def paires_contrastes(cv, ma, mb, base):
    """Les sept couples (numerateur, denominateur) par personne, pour A moins B."""
    out = {}

    def acc(m):
        dispo = C.observe(m["pred"])
        ok_acc = base & dispo
        return C.par_personne(ok_acc & (m["pred"] == cv["verite"]), ok_acc)

    out["P1 exactitude"] = (acc(ma), acc(mb))
    for cle, num_masque, den_masque in (
            ("P2 taux de fausses raretes", "faux_maj", "rare_pred"),
            ("P3 rappel des cellules minoritaires", "juste", None),
            ("P4 precision des cellules minoritaires", "juste", "rare_pred")):
        a = C.par_personne(ma[num_masque] & base,
                           (cv["rare_vrai"] & base) if den_masque is None
                           else ma[den_masque] & base)
        b = C.par_personne(mb[num_masque] & base,
                           (cv["rare_vrai"] & base) if den_masque is None
                           else mb[den_masque] & base)
        out[cle] = (a, b)
    out["P5 H1b rarete de la personne"] = (
        C.moyenne_par_personne(ma["faux_maj"] & base, cv["r_personne"]),
        C.moyenne_par_personne(mb["faux_maj"] & base, cv["r_personne"]))
    out["P6 H2b rarete du segment"] = (
        C.moyenne_par_personne(ma["faux_maj"] & base, cv["r_segment"][C.AXE_PRINCIPAL]),
        C.moyenne_par_personne(mb["faux_maj"] & base, cv["r_segment"][C.AXE_PRINCIPAL]))
    out["P7 H2a modale rare du segment"] = (
        C.mesure_h2a(cv, {"faux_maj": ma["faux_maj"] & base, "pred": ma["pred"]},
                     C.AXE_PRINCIPAL, cv["modale_seg"][C.AXE_PRINCIPAL]),
        C.mesure_h2a(cv, {"faux_maj": mb["faux_maj"] & base, "pred": mb["pred"]},
                     C.AXE_PRINCIPAL, cv["modale_seg"][C.AXE_PRINCIPAL]))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--tirages", type=int, default=4000)
    ap.add_argument("--graine", type=int, default=C.GRAINE)
    args = ap.parse_args()

    t0 = time.time()
    print(__doc__.split("=" * 75)[1])

    paquet = C.charger(args.cache, args.cache_foret)
    ids, items, y1 = paquet["ids"], paquet["items"], paquet["y1"]
    rng = np.random.default_rng(args.graine)
    seg_tous, _niveaux = C.segments_et_niveaux(paquet)
    print(f"{len(ids)} personnes, {len(items)} items", flush=True)

    controles = []

    # ------------------------------------------------------------------ C3F
    c3f = C.matrice_c3f(paquet)
    paquet["M"]["C3F"] = c3f["matrice"]
    lignes60 = c3f["lignes"]
    cols_fam, fam_index, noms_fam = C.colonnes_familles(items)
    print(f"C3F : {c3f['appels']} appels, {len(c3f['personnes'])} personnes completes, "
          f"{c3f['n_items']} items, {c3f['partielles']} personne(s) partielle(s) ecartee(s)",
          flush=True)
    controles.append({"controle": "personnes C3F completes retenues",
                      "valeur": len(c3f["personnes"]), "sur": 150})
    controles.append({"controle": "items de famille dans la trace C3F",
                      "valeur": c3f["n_items"], "sur": len(cols_fam)})
    controles.append({"controle": "personnes C3F partielles ecartees",
                      "valeur": c3f["partielles"], "sur": 1})

    # ------------------------------------------------------- B2 famille retiree
    print("B2 famille retiree, reconstruction a l'identique de a8_familles", flush=True)
    paquet["M"]["B2 famille retiree"] = C.b2_famille_retiree(paquet)

    # ------------------------------------------------------------------ confiances
    conf = C.confiances_c2_c3(paquet)
    conf["C3F"] = {"pmax": c3f["pmax"], "entropie": c3f["entropie"]}

    # ------------------------------------------------- covariables sur les 1 052
    toutes_lignes = np.arange(len(ids))
    cv_full = C.covariables(paquet, toutes_lignes, C.SEUIL, seg_tous)
    methodes = [m for m in C.ORDRE if m in paquet["M"]]
    mq_full = {nom: C.masques_condition(paquet, toutes_lignes, nom, cv_full)
               for nom in methodes}

    # Contexte reellement vu : hors du bloc secret pour C3, hors de la famille pour C3F.
    ctx_bloc = cv_full["ctx"]
    ctx_fam = C.rarete_contexte(cv_full["rare_vrai"], cv_full["ok"], fam_index)

    # ---------------------------------------------------------- perimetre apparie
    cv = C.sous_perimetre_cv(cv_full, lignes60, cols_fam)
    mq = {nom: C.sous_perimetre_mq(mq_full[nom], lignes60, cols_fam) for nom in methodes}
    ctx_bloc_p = ctx_bloc[np.ix_(lignes60, cols_fam)]
    ctx_fam_p = ctx_fam[np.ix_(lignes60, cols_fam)]
    conf_p = {k: {"pmax": v["pmax"][np.ix_(lignes60, cols_fam)],
                  "entropie": v["entropie"][np.ix_(lignes60, cols_fam)]}
              for k, v in conf.items()}

    base = cv["ok"] & C.observe(mq["C3"]["pred"]) & C.observe(mq["C3F"]["pred"])
    print(f"perimetre apparie : {base.shape[0]} personnes x {base.shape[1]} items, "
          f"{int(base.sum())} cellules retenues sur {base.size}", flush=True)
    controles.append({"controle": "cellules du perimetre apparie",
                      "valeur": int(base.sum()), "sur": int(base.size)})
    controles.append({"controle": "cellules ecartees, reponse vague 1 non observee",
                      "valeur": int((~cv["ok"]).sum()), "sur": int(base.size)})

    controles.append({"controle": "reference de minorite : items porteurs sur les 58",
                      "valeur": int(np.asarray([len(s) > 0 for s in cv["mods"]]).sum()),
                      "sur": len(cols_fam)})
    controles.append({"controle": "items a deux modalites minoritaires ou plus sur les 58",
                      "valeur": int(np.asarray([len(s) >= 2 for s in cv["mods"]]).sum()),
                      "sur": len(cols_fam)})
    controles.append({"controle": "P7 H2a evaluable : items multimodalites du perimetre",
                      "valeur": "non, 0 item", "sur": "test non evaluable, p = 1"})

    idx_boot = C.tirages_bootstrap(base.shape[0], args.tirages, rng)

    # ------------------------------------------------------------------- mesures
    lignes_mes = []
    for nom in methodes:
        lignes_mes.append(mesures_condition(
            nom, cv, mq[nom], base, idx_boot,
            pmax=conf_p[nom]["pmax"] if nom in conf_p else None))
    mes = pd.DataFrame(lignes_mes)

    # --------------------------------------------------------------- contrastes
    contr = []
    paires = paires_contrastes(cv, mq["C3F"], mq["C3"], base)
    for cle, (a, b) in paires.items():
        o, lo, hi, p = C.contraste(*a, *b, idx_boot)
        contr.append({"famille": "primaire", "test": cle,
                      "comparaison": "C3F moins C3, memes cellules",
                      "difference": o, "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p})

    for nom in ("C3F", "C3"):
        m = mq[nom]
        for cle, mat in (("H1b exces de rarete de la personne", cv["r_personne"]),
                         ("H2b exces de rarete du segment",
                          cv["r_segment"][C.AXE_PRINCIPAL])):
            num, den = C.moyenne_par_personne(m["faux_maj"] & base, mat)
            num_t, den_t = C.temoin_par_personne(m["faux_maj"] & base, base, mat)
            o, lo, hi, p = C.contraste(num, den, num_t, den_t, idx_boot)
            contr.append({"famille": "secondaire", "test": f"{nom} : {cle}",
                          "comparaison": "contre le temoin aveugle a la personne",
                          "difference": o, "ic_bas": lo, "ic_haut": hi,
                          "p_bootstrap": p})

    # Hors famille : les memes contrastes contre les humains reinterroges, descriptifs.
    for nom in ("C3F", "C3"):
        for cle, mat in (("H1b exces de rarete de la personne", cv["r_personne"]),
                         ("H2b exces de rarete du segment",
                          cv["r_segment"][C.AXE_PRINCIPAL])):
            a = C.moyenne_par_personne(mq[nom]["faux_maj"] & base, mat)
            b = C.moyenne_par_personne(mq["humains vague 2"]["faux_maj"] & base, mat)
            o, lo, hi, p = C.contraste(*a, *b, idx_boot)
            contr.append({"famille": "hors famille, description", "test": f"{nom} : {cle}",
                          "comparaison": "contre les humains vague 2",
                          "difference": o, "ic_bas": lo, "ic_haut": hi,
                          "p_bootstrap": p})

    # Post hoc, hors des deux familles declarees et signale comme tel partout : le taux de
    # fausses raretes rapporte a TOUTES les cellules et non aux seules raretes osees.
    # P2 rapporte les fausses raretes aux raretes osees, ce qui neutralise le fait qu'une
    # condition ose plus de raretes ; cette version la ne le neutralise pas.
    for cle, masque in (("fausses raretes par cellule", "faux_maj"),
                        ("raretes osees par cellule", "rare_pred")):
        a = C.par_personne(mq["C3F"][masque] & base, base)
        b = C.par_personne(mq["C3"][masque] & base, base)
        o, lo, hi, p = C.contraste(*a, *b, idx_boot)
        contr.append({"famille": "post hoc, hors famille", "test": cle,
                      "comparaison": "C3F moins C3, memes cellules",
                      "difference": o, "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p})

    ct = pd.DataFrame(contr)
    ct["p_holm"] = np.nan
    ct["p_bh"] = np.nan
    for libelle in ct.famille.unique():
        idx = ct[ct.famille == libelle].index
        ct.loc[idx, "p_holm"] = C.holm(ct.loc[idx, "p_bootstrap"].values)
        ct.loc[idx, "p_bh"] = C.benjamini_hochberg(ct.loc[idx, "p_bootstrap"].values)

    # ------------------------------------------------- leviers personne et segment
    lev = mes[["condition", "h_personne_lift", "h_segment_lift",
               "rapport_groupe_sur_personne", "fausses_raretes"]].copy()
    lev = lev.rename(columns={"h_personne_lift": "lift_personne",
                              "h_segment_lift": "lift_segment"})

    # ------------------------------------------------------------- par famille
    cousins_pre = C.cousins_en_contexte(items, cols_fam, fam_index, cv_full["bloc"])
    lignes_fam = []
    for k, nom_f in enumerate(list(FAMILLES.keys())):
        sel_cols = np.flatnonzero(fam_index[cols_fam] == k)
        if len(sel_cols) == 0:
            continue
        sous = np.zeros_like(base)
        sous[:, sel_cols] = True
        b_f = base & sous
        for nom in methodes:
            m = mq[nom]
            dispo = C.observe(m["pred"])
            ok_acc = b_f & dispo
            num, den = C.par_personne(ok_acc & (m["pred"] == cv["verite"]), ok_acc)
            v, lo, hi, _ = C.taux_ic(num, den, idx_boot)
            rp = m["rare_pred"] & b_f
            fm = m["faux_maj"] & b_f
            lignes_fam.append({
                "famille": nom_f, "n_items": len(sel_cols), "condition": nom,
                "cousins_vus_par_C3": float(
                    cousins_pre[cousins_pre.famille_index == k].cousins_vus_par_C3.mean()),
                "cellules": int(ok_acc.sum()), "exactitude": v,
                "ic_bas": lo, "ic_haut": hi,
                "raretes_osees": int(rp.sum()), "fausses_raretes": int(fm.sum()),
                "taux_fausses_raretes": (float(fm.sum()) / int(rp.sum())
                                         if rp.sum() else np.nan)})
    par_fam = pd.DataFrame(lignes_fam)

    # --------------------------------------------------------------- le contexte
    cousins = cousins_pre
    lignes_ctx = [
        {"condition": "C3", "contexte": "149 items moins le bloc secret",
         "items_contexte_moyen": float(cousins.items_contexte_C3.mean()),
         "cousins_de_famille_moyen": float(cousins.cousins_vus_par_C3.mean()),
         "rarete_du_contexte_moyenne": float(np.nanmean(ctx_bloc_p[base]))},
        {"condition": "C3F", "contexte": "149 items moins la famille entiere",
         "items_contexte_moyen": float(cousins.items_contexte_C3F.mean()),
         "cousins_de_famille_moyen": 0.0,
         "rarete_du_contexte_moyenne": float(np.nanmean(ctx_fam_p[base]))},
    ]
    ctx_tab = pd.DataFrame(lignes_ctx)

    # Quintiles de rarete du contexte REELLEMENT VU par chaque condition.
    lignes_quint = []
    for nom, ctx in (("C3", ctx_bloc_p), ("C3F", ctx_fam_p)):
        m = mq[nom]
        sel = (m["rare_pred"] & base) & ~np.isnan(ctx)
        if sel.sum() < 20:
            continue
        v = ctx[sel]
        bornes = np.quantile(ctx[base & ~np.isnan(ctx)], [0.2, 0.4, 0.6, 0.8])
        q = np.searchsorted(bornes, v, side="right")
        faux = (m["faux_maj"] & base)[sel]
        for k in range(5):
            mk = q == k
            lignes_quint.append({
                "condition": nom, "quintile": k + 1, "raretes_osees": int(mk.sum()),
                "rarete_contexte_moyenne": float(v[mk].mean()) if mk.any() else np.nan,
                "taux_fausses_raretes": float(faux[mk].mean()) if mk.any() else np.nan})
    quint = pd.DataFrame(lignes_quint)

    # ------------------------------------------------------------- confiance
    lignes_conf = []
    for nom in ("C2", "C3", "C3F"):
        if nom not in conf_p or nom not in mq:
            continue
        pmax, ent = conf_p[nom]["pmax"], conf_p[nom]["entropie"]
        m = mq[nom]
        for libelle, masque in (
                ("rarete non osee, cellule majoritaire", base & ~m["rare_pred"]),
                ("rarete juste", m["juste"] & base),
                ("fausse rarete", m["faux_maj"] & base),
                ("mauvaise modalite rare", m["faux_min"] & base)):
            sel = masque & ~np.isnan(pmax)
            n = int(sel.sum())
            lignes_conf.append({
                "condition": nom, "cellules": libelle, "n": n,
                "p_max_moyen": float(pmax[sel].mean()) if n else np.nan,
                "p_max_median": float(np.median(pmax[sel])) if n else np.nan,
                "part_p_max_sup_099": float((pmax[sel] > 0.99).mean()) if n else np.nan,
                "entropie_moyenne_bits": float(ent[sel].mean()) if n else np.nan})
    cfd = pd.DataFrame(lignes_conf)

    # ------------------------------------------------------------- sensibilites
    sens = []
    per150 = np.asarray(paquet["lignes150"])
    pos60 = np.array([int(np.flatnonzero(per150 == l)[0]) for l in lignes60])
    variantes = [("reference 1052, seuil 0.10", toutes_lignes, C.SEUIL, None),
                 ("reference 1052, seuil 0.20", toutes_lignes, 0.20, None),
                 ("reference 150, seuil 0.10", per150, C.SEUIL, pos60)]
    for libelle, lignes_ref, seuil, repositionne in variantes:
        cvv = (cv_full if (libelle.startswith("reference 1052") and seuil == C.SEUIL)
               else C.covariables(paquet, lignes_ref, seuil, seg_tous))
        lg = lignes60 if repositionne is None else repositionne
        cvs = C.sous_perimetre_cv(cvv, lg, cols_fam)
        mqs = {}
        for nom in ("C3", "C3F", "humains vague 2"):
            mm = C.masques_condition(paquet, lignes_ref, nom, cvv)
            mqs[nom] = C.sous_perimetre_mq(mm, lg, cols_fam)
        b = cvs["ok"] & C.observe(mqs["C3"]["pred"]) & C.observe(mqs["C3F"]["pred"])
        for nom in ("C3", "C3F", "humains vague 2"):
            m = mqs[nom]
            rp = m["rare_pred"] & b
            fm = m["faux_maj"] & b
            ju = m["juste"] & b
            rv = cvs["rare_vrai"] & b
            num_s, den_s = C.moyenne_par_personne(fm, cvs["r_segment"][C.AXE_PRINCIPAL])
            num_p, den_p = C.moyenne_par_personne(fm, cvs["r_personne"])
            t_s = C.temoin_item(fm, b, cvs["r_segment"][C.AXE_PRINCIPAL])
            t_p = C.temoin_item(fm, b, cvs["r_personne"])
            vs, vp = C.taux(num_s, den_s), C.taux(num_p, den_p)
            ls = vs / t_s - 1.0 if t_s else np.nan
            lp = vp / t_p - 1.0 if t_p else np.nan
            sens.append({
                "variante": libelle, "condition": nom,
                "cellules": int(b.sum()),
                "cellules_minoritaires_reelles": int(rv.sum()),
                "raretes_osees": int(rp.sum()), "fausses_raretes": int(fm.sum()),
                "taux_fausses_raretes": (float(fm.sum()) / int(rp.sum())
                                         if rp.sum() else np.nan),
                "rappel": float(ju.sum()) / int(rv.sum()) if rv.sum() else np.nan,
                "precision": float(ju.sum()) / int(rp.sum()) if rp.sum() else np.nan,
                "lift_personne": lp, "lift_segment": ls,
                "rapport_groupe_sur_personne": ls / lp if (np.isfinite(lp) and lp > 0)
                else np.nan})
    sensib = pd.DataFrame(sens)

    # -------------------------------------------- controle de reproduction de a8
    b2f = paquet["M"]["B2 famille retiree"]
    ok_all = C.observe(y1)
    sel = ok_all[:, cols_fam]
    juste_all = (b2f[:, cols_fam] == y1[:, cols_fam]) & sel
    acc_1052 = float(juste_all.sum()) / float(sel.sum())
    controles.append({"controle": "B2 famille retiree recalculee, exactitude sur les "
                                  "1 052 (a8 publie 0,662105)",
                      "valeur": round(acc_1052, 6), "sur": 1})
    a8 = pd.read_csv(os.path.join(C.SORTIE, "a8-familles-gss.csv"))
    ref = a8[(a8.famille == "toutes familles reunies")
             & (a8.methode == "B2 famille retiree (argmax)")]
    if not ref.empty:
        controles.append({"controle": "ecart a la valeur publiee de a8",
                          "valeur": round(acc_1052 - float(ref.exactitude.iloc[0]), 6),
                          "sur": 1})
    controles.append({"controle": "plis d'origine des 60 personnes de C3F",
                      "valeur": "0 et 1", "sur": "5 plis"})

    # Reconciliation avec l'addendum 06:25 de SYNTHESE-NUIT-2026-09-08.md, qui donne
    # C3F 0,5617 et une diversite conservee de 56,6 pour cent. Les deux chiffres sont
    # reproduits ici a l'identique en refaisant le calcul comme a5_evaluer le fait, puis
    # remesures sur le perimetre apparie de ce rapport, ou les deux cotes portent sur les
    # memes 60 personnes.
    from a2_commun import bootstrap_personnes, exactitude_par_personne, profil_diversite
    lignes150 = np.asarray(paquet["lignes150"])
    v150 = y1[lignes150][:, cols_fam]
    for nom in ("C3F", "C3"):
        p150 = paquet["M"][nom][lignes150][:, cols_fam]
        mq150 = np.array([[(a is not None) and (b is not None) and (str(b) == str(b))
                           for a, b in zip(la, lb)] for la, lb in zip(p150, v150)])
        acc = exactitude_par_personne(p150, v150, mq150)
        moy, _b, _h = bootstrap_personnes(acc)
        controles.append({
            "controle": f"{nom} sur 58 items, calcul de a5_evaluer, personnes du run",
            "valeur": round(float(moy), 4),
            "sur": f"{int((mq150.sum(axis=1) > 0).sum())} personnes predites"})
        controles.append({
            "controle": f"{nom} diversite conservee, calcul de a5_evaluer, "
                        f"predictions contre les 150 humains",
            "valeur": round(float(profil_diversite(p150, v150)["part_diversite_humaine"]), 4),
            "sur": 1})

    ctrl = pd.DataFrame(controles)

    # ------------------------------------------------------------------- ecriture
    C.ecrire(mes, "a33-mesures.csv")
    C.ecrire(ct, "a33-contrastes.csv")
    C.ecrire(lev, "a33-leviers-personne-segment.csv")
    C.ecrire(par_fam, "a33-par-famille.csv")
    C.ecrire(ctx_tab, "a33-contexte.csv")
    C.ecrire(quint, "a33-quintiles.csv")
    C.ecrire(cfd, "a33-confiance.csv")
    C.ecrire(sensib, "a33-sensibilites.csv")
    C.ecrire(cousins, "a33-cousins.csv")
    C.ecrire(ctrl, "a33-controles.csv")

    # ------------------------------------------------------------------ affichage
    pd.set_option("display.width", 250)
    ordre = {c: i for i, c in enumerate(C.ORDRE)}
    print("\n" + "=" * 130)
    print("Controles")
    print("=" * 130)
    print(ctrl.to_string(index=False))

    print("\n" + "=" * 130)
    print("Le contexte reellement vu")
    print("=" * 130)
    print(ctx_tab.round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Mesures sur le perimetre apparie, 60 personnes x 58 items, seuil 10 %")
    print("=" * 130)
    s = mes.copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values("o")[["condition", "cellules_predites", "exactitude",
                              "exactitude_ic_bas", "exactitude_ic_haut",
                              "raretes_osees", "raretes_justes", "fausses_raretes",
                              "rappel", "precision", "f1", "taux_fausses_raretes"]]
          .round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Le depart entre H1 et H2 sur le perimetre apparie")
    print("=" * 130)
    s = mes.copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values("o")[["condition", "fausses_raretes", "h_personne_valeur",
                              "h_personne_temoin", "h_personne_lift",
                              "h_segment_valeur", "h_segment_temoin", "h_segment_lift",
                              "rapport_groupe_sur_personne", "h2a_cellules",
                              "h2a_valeur"]].round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Contrastes declares et corrections pour tests multiples")
    print("=" * 130)
    print(ct[["famille", "test", "comparaison", "difference", "ic_bas", "ic_haut",
              "p_bootstrap", "p_holm", "p_bh"]].round(5).to_string(index=False))

    print("\n" + "=" * 130)
    print("Par famille thematique, C3F contre C3")
    print("=" * 130)
    s = par_fam[par_fam.condition.isin(["C3F", "C3", "B2 famille retiree", "B2 argmax",
                                        "B0 mode", "humains vague 2"])].copy()
    print(s.pivot_table(index="famille", columns="condition", values="exactitude")
          .round(4).to_string())

    print("\n" + "=" * 130)
    print("Quintiles de rarete du contexte reellement vu")
    print("=" * 130)
    print(quint.round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Confiance des distributions par type de cellule")
    print("=" * 130)
    print(cfd.round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Sensibilites")
    print("=" * 130)
    print(sensib.round(4).to_string(index=False))

    print(f"\nduree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
