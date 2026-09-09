"""
a31_mecanismes : pourquoi la bonne personne recoit elle la mauvaise rarete ?

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a31_commun, a29_commun, a28_commun,
a25_commun, a25_mesures, a8_commun, a2_commun, a2_baselines_gss, a5_evaluer et
a5_agents_locaux_gss sont importes tels quels, memes graines, memes plis, memes blocs,
memes 149 items, memes personnes que a2, a8, a23, a25, a28 et a29.

a29 a etabli deux choses opposees. Les agents riches SAVENT qui sont les personnes a
reponses rares, correlation par personne 0,531 contre 0,732 chez les memes humains
reinterroges, quand un tirage aveugle est a zero. Et ils leur pretent souvent la MAUVAISE
rarete : quand agents composite ose une modalite minoritaire, 61,6 pour cent du temps la
personne a donne une reponse majoritaire sur cet item, contre 41,4 pour cent chez les
humains reinterroges ; et l'etiquette demographique aggrave, C2 a 0,194 de correlation
contre 0,410 pour C3. Ce script cherche le MECANISME de cette erreur, c'est a dire ce qui
distingue les cellules ou une methode place une fausse rarete.

Le fait de structure qu'il faut avoir en tete avant de lire quoi que ce soit, et qui est
mesure en section 0 du rapport : au seuil de 10 pour cent, 70 items sur 149 portent au
moins une modalite minoritaire, mais 19 seulement en portent au moins DEUX. Sur les 51
autres, predire une rarete c'est predire LA rarete de l'item : l'erreur ne peut pas etre
"la mauvaise modalite rare", elle est necessairement "la mauvaise personne". C'est la
raison arithmetique du taux de mauvaise minorite tres bas mesure en a29 section 1 point 4.

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT LES RESULTATS
===========================================================================
Perimetre declare : le perimetre naturel de chaque methode, soit les 1 052 personnes pour
les onze methodes qui les couvrent, et les 150 personnes du run local pour C2 et C3, avec
la reference de minorite calculee sur ces 150 personnes. Seuil declare : 10 pour cent.
Unite d'analyse declaree : la FAUSSE RARETE, c'est a dire une cellule ou la methode
predit une modalite minoritaire et ou la personne a en realite donne une modalite
majoritaire. C'est la quantite que a29 chiffre a 61,6 pour cent des raretes osees.

Les cinq mecanismes candidats, et la mesure de chacun.

  H1  DEPLACEMENT DE RARETE. La methode attribue la rarete a la bonne personne mais sur
      le mauvais item : la personne est reellement rare AILLEURS dans la meme famille
      thematique. Mesure H1a : part des fausses raretes dont la personne donne une
      reponse minoritaire reelle sur un autre item de la meme famille, parmi les fausses
      raretes evaluables, c'est a dire posees sur un item de famille qui porte une
      modalite minoritaire et dont la personne a au moins un autre item exploitable dans
      la famille. Six familles de a2_baselines_gss, 58 items, dont 21 portent une
      modalite minoritaire.
      TEST H1a : pour chacune des 13 methodes non humaines, cette part DIFFERE de celle
      des memes humains reinterroges. 13 tests, bilateraux.

  H2  RARETE DE GROUPE. La methode attribue la rarete typique de l'etiquette et non celle
      de la personne. Mesure H2a : parmi les fausses raretes posees sur les 19 items qui
      portent au moins deux modalites minoritaires, part de celles dont la modalite
      predite est la modalite rare MODALE du segment de la personne, calculee sur les
      humains de la vague 1 sans la personne elle meme.
      TEST H2a : pour chacune des 13 methodes, cette part DIFFERE de celle des memes
      humains reinterroges. 13 tests, bilateraux. Axe declare : l'ideologie politique,
      seul axe dont a1, a23, a28 test 3 et a29 section 3.1 disent tous les quatre qu'il
      separe. Les cinq autres axes sont rapportes a cote, sans test.

  H3  RARETE LEXICALE OU DE POSITION. La fausse rarete est une modalite de bout de liste,
      premiere ou derniere position dans la nomenclature de question_master, donc bout
      d'echelle pour les 71 items ordinaux, independamment de la personne. Mesure H3 :
      part des fausses raretes en position extreme.
      TEST H3 : pour chacune des 13 methodes, cette part DIFFERE de la part d'extremite
      des VRAIES raretes humaines, temoin appariee item par item sur la composition en
      items des fausses raretes de la methode. 13 tests, bilateraux.

  H4  SUR CONFIANCE. Les fausses raretes viennent des cellules ou le modele est le plus
      sur, signe qu'il substitue sa reponse a celle de la population, ce que a23 section
      1.4 documente item par item. Mesure H4 : part des cellules a p max superieur a 0,99,
      chez les fausses raretes et chez les raretes justes. C2 et C3 seulement, seules
      conditions dont la trace porte une distribution complete.
      TEST H4 : pour C2 et pour C3, cette part DIFFERE entre fausses raretes et raretes
      justes. 2 tests, bilateraux.

  H5  CONTEXTE INSUFFISANT. La fausse rarete tombe sur les personnes dont le contexte
      contient peu de reponses rares. Mesure H5 : taux de reponses rares reelles de la
      personne hors du bloc secret de l'item, soit les ~119 items du prompt systeme de C3
      et les items de distance de B2, moyenne chez les fausses raretes et chez les raretes
      justes.
      TEST H5 : pour chacune des 13 methodes, cette moyenne DIFFERE entre fausses raretes
      et raretes justes. 13 tests, bilateraux.

  FAMILLE PRIMAIRE DECLAREE : H1a union H2a union H3 union H5 union H4, soit 54 tests.
  Correction principale : Holm sur les 54. Elle controle le taux d'erreur par famille sans
  hypothese sur la dependance, ce qui est necessaire : les contrastes portent sur les
  memes personnes et les memes items. Correction secondaire rapportee a cote :
  Benjamini Hochberg sur les 54.

  Deux mesures complementaires, declarees ici et corrigees SEPAREMENT, parce qu'elles
  changent la nature de la question : elles ne comparent plus a un humain ni a un autre
  jeu de cellules, elles comparent a un TEMOIN AVEUGLE A LA PERSONNE, apparie item par
  item, qui poserait le meme nombre de fausses raretes sur les memes items chez des
  personnes tirees au hasard parmi les repondants.

  H1b  EXCES DE RARETE DE LA PERSONNE. Moyenne, chez les fausses raretes, du taux de
       reponses rares reelles de la personne hors de l'item, moins le temoin aveugle.
       13 tests.
  H2b  EXCES DE RARETE DU SEGMENT. Moyenne, chez les fausses raretes, du taux de reponses
       rares reelles du segment ideologique de la personne sur cet item, sans la personne,
       moins le temoin aveugle. 13 tests.

  FAMILLE SECONDAIRE DECLAREE : H1b union H2b, soit 26 tests, corrigee separement par
  Holm et par Benjamini Hochberg. La comparaison des deux exces, personne contre segment,
  est le depart entre H1 et H2 ; elle est lisible directement sur les deux colonnes.

  N'ENTRENT DANS AUCUNE FAMILLE, et sont rapportes comme des descriptions : le seuil de
  20 pour cent ; le perimetre 150 pour les onze methodes qui disposent du perimetre 1 052,
  echantillon emboite et non test independant ; les cinq axes autres que l'ideologie ; la
  version population de H2a, c'est a dire la modalite rare modale de la population entiere
  et non du segment ; le decoupage de H3 en premiere et derniere position separees ; la
  calibration de C2 et C3 sur les cellules rares ; les quintiles de rarete de contexte ;
  la variante de H1 etendue a tous les items hors famille ; et l'ordre d'importance des
  mecanismes, qui est une lecture des exces mesures et non un test.

  Tous les p sont des p de bootstrap apparie sur les PERSONNES, 4 000 tirages, lus sur la
  position de zero dans la distribution ; ils ne descendent jamais sous 1 / 4 000 =
  0,00025. Avec 54 tests, le plancher de Holm vaut donc 0,0135, ce qui laisse la
  correction decidable. Le bootstrap porte sur les personnes et non sur les cellules :
  deux reponses d'une meme personne ne sont pas independantes.
===========================================================================

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl, cache de matrices de a25 et cache de
          la foret aleatoire de a28.
Sortie  : resultats/a31-mecanismes.csv, a31-contrastes.csv, a31-h2-par-axe.csv,
          a31-h3-positions.csv, a31-h4-confiance.csv, a31-h5-quintiles.csv,
          a31-synthese-mecanismes.csv, a31-controles.csv.

Usage :
  .venv/bin/python analyses/a31_mecanismes.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 4000
"""

import argparse
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a31_commun as C
from a8_commun import modalites_minoritaires

MECANISMES = ["H1a deplacement dans la famille", "H2a rarete modale du segment",
              "H3 position extreme", "H5 rarete du contexte", "H4 sur confiance",
              "H1b exces de rarete de la personne", "H2b exces de rarete du segment"]


# ---------------------------------------------------------------------------

def covariables(paquet, lignes, seuil, seg_tous):
    """Toutes les covariables de cellule pour un perimetre et un seuil."""
    items = paquet["items"]
    verite = paquet["y1"][lignes]
    options = paquet["options"]
    mods = modalites_minoritaires(verite, seuil)
    ok = C.observe(verite)
    rare_vrai = C.appartient(verite, mods) & ok

    fam = C.familles_par_item(items)
    porte = np.array([len(s) > 0 for s in mods], dtype=bool)
    multi = np.array([len(s) >= 2 for s in mods], dtype=bool)
    bloc = C.blocs_par_item(len(paquet["ids"]), items)
    premiere, derniere = C.table_extremite(items, options)

    deplace, valide_fam = C.rarete_famille(rare_vrai, ok, fam, porte)
    r_personne = C.rarete_personne(rare_vrai, ok)
    ctx = C.rarete_contexte(rare_vrai, ok, bloc)
    cols_multi = np.flatnonzero(multi)

    seg = {a: seg_tous[a][lignes] for a in C.AXES}
    r_segment = {a: C.rarete_segment(rare_vrai, ok, seg[a]) for a in C.AXES}
    modale_seg = {a: C.modale_rare_segment(verite, ok, mods, seg[a], cols_multi)
                  for a in C.AXES}
    modale_pop = C.modale_rare_population(verite, ok, mods, cols_multi)

    ext1_vrai, extK_vrai, _ = C.est_extreme(verite, items, options, premiere, derniere)

    return {"verite": verite, "mods": mods, "ok": ok, "rare_vrai": rare_vrai,
            "fam": fam, "porte": porte, "multi": multi, "bloc": bloc,
            "premiere": premiere, "derniere": derniere, "options": options,
            "deplace": deplace, "valide_fam": valide_fam, "r_personne": r_personne,
            "ctx": ctx, "seg": seg, "r_segment": r_segment, "modale_seg": modale_seg,
            "modale_pop": modale_pop, "ext_vrai": ext1_vrai | extK_vrai,
            "ext1_vrai": ext1_vrai, "extK_vrai": extK_vrai, "items": items}


def masques_condition(paquet, lignes, nom, cv):
    """Les trois masques de a29 : rarete predite, rarete juste, fausse rarete."""
    pred = paquet["M"][nom][lignes]
    ok, rare_vrai = cv["ok"], cv["rare_vrai"]
    dispo = C.observe(pred)
    rare_pred = C.appartient(pred, cv["mods"]) & ok & dispo
    juste = rare_pred & (pred == cv["verite"])
    faux_maj = rare_pred & ~juste & ~rare_vrai
    faux_min = rare_pred & ~juste & rare_vrai
    return {"pred": pred, "rare_pred": rare_pred, "juste": juste,
            "faux_maj": faux_maj, "faux_min": faux_min}


def mesure_h1a(cv, mq):
    den = mq["faux_maj"] & cv["valide_fam"]
    return C.par_personne(cv["deplace"], den)


def mesure_h2a(cv, mq, axe, modale):
    ref = modale
    egal = np.zeros(mq["faux_maj"].shape, dtype=bool)
    den = mq["faux_maj"] & cv["multi"][None, :] & (ref != None)  # noqa: E711
    lignes, cols = np.nonzero(den)
    for i, j in zip(lignes, cols):
        egal[i, j] = mq["pred"][i, j] == ref[i, j]
    return C.par_personne(egal, den)


def mesure_h3(cv, mq):
    p1, pK, hors = C.est_extreme(mq["pred"], cv["items"], cv["options"],
                                 cv["premiere"], cv["derniere"])
    return C.par_personne(p1 | pK, mq["faux_maj"]), p1, pK, hors


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
    rng = np.random.default_rng(args.graine)
    per = C.perimetres(paquet)
    seg_tous, niveaux = C.segments_et_niveaux(paquet)
    items = paquet["items"]
    print(f"{len(paquet['ids'])} personnes, {len(items)} items, "
          f"{len(paquet['M'])} conditions", flush=True)

    # ------------------------------------------------------------------ controles
    controles = []
    conf, bloc_trace, fichiers = C.confiances_locales(paquet, items)
    bloc_calcule = C.blocs_par_item(len(paquet["ids"]), items)
    accord = sum(1 for j, it in enumerate(items)
                 if it in bloc_trace and bloc_trace[it] == {int(bloc_calcule[j])})
    controles.append({"controle": "bloc recalcule egal au bloc de la trace",
                      "valeur": accord, "sur": len(bloc_trace)})
    for cond, d in conf.items():
        lignes150 = np.asarray(paquet["lignes150"])
        m = paquet["M"][cond][lignes150]
        desaccord = int(sum(1 for a, b in zip(m.ravel(), d["argmax"].ravel())
                            if a != b))
        controles.append({"controle": f"argmax de la trace {cond} egal a la matrice a25",
                          "valeur": int(m.size - desaccord), "sur": int(m.size)})
    print("controles :", controles, flush=True)

    lignes_mes, lignes_contr, lignes_axe = [], [], []
    lignes_pos, lignes_conf, lignes_quint = [], [], []
    cache = {}

    for nom_per, lignes in per.items():
        methodes = C.methodes_du_perimetre(paquet, nom_per)
        idx_boot = C.tirages_bootstrap(len(lignes), args.tirages, rng)
        for seuil in (0.10, 0.20):
            cv = covariables(paquet, lignes, seuil, seg_tous)
            mq = {nom: masques_condition(paquet, lignes, nom, cv) for nom in methodes}
            if seuil == 0.10:
                cache[(nom_per, seuil)] = (cv, mq, idx_boot)

            for nom in methodes:
                m = mq[nom]
                n_faux = int(m["faux_maj"].sum())
                ligne_base = {"perimetre": nom_per, "seuil": seuil, "condition": nom,
                              "raretes_osees": int(m["rare_pred"].sum()),
                              "fausses_raretes": n_faux,
                              "raretes_justes": int(m["juste"].sum()),
                              "mauvaise_modalite_rare": int(m["faux_min"].sum())}

                # ---- H1a, deplacement dans la famille
                num, den = mesure_h1a(cv, m)
                v, b, h, _ = C.taux_ic(num, den, idx_boot)
                tem = C.temoin_item(m["faux_maj"] & cv["valide_fam"],
                                    cv["ok"] & cv["valide_fam"], cv["deplace"])
                num_j, den_j = C.par_personne(cv["deplace"],
                                              m["juste"] & cv["valide_fam"])
                lignes_mes.append({**ligne_base, "mecanisme": MECANISMES[0],
                                   "cellules": int(den.sum()), "valeur": v,
                                   "ic_bas": b, "ic_haut": h, "temoin": tem,
                                   "exces": v - tem if np.isfinite(v) else np.nan,
                                   "valeur_raretes_justes": C.taux(num_j, den_j),
                                   "cellules_justes": int(den_j.sum())})

                # ---- H2a, rarete modale du segment, six axes plus la population
                for axe in C.AXES:
                    num, den = mesure_h2a(cv, m, axe, cv["modale_seg"][axe])
                    v, b, h, _ = C.taux_ic(num, den, idx_boot)
                    lignes_axe.append({"perimetre": nom_per, "seuil": seuil,
                                       "condition": nom, "reference": axe,
                                       "cellules": int(den.sum()), "valeur": v,
                                       "ic_bas": b, "ic_haut": h})
                    if axe == C.AXE_PRINCIPAL:
                        principal = (num, den, v, b, h)
                num_p, den_p = mesure_h2a(cv, m, "population", cv["modale_pop"])
                vp, bp, hp, _ = C.taux_ic(num_p, den_p, idx_boot)
                lignes_axe.append({"perimetre": nom_per, "seuil": seuil,
                                   "condition": nom, "reference": "population entiere",
                                   "cellules": int(den_p.sum()), "valeur": vp,
                                   "ic_bas": bp, "ic_haut": hp})
                num, den, v, b, h = principal
                # temoin : tirer la modalite rare dans la masse rare de la population de
                # l'item revient a la probabilite que ce tirage tombe sur la modale du
                # segment ; il est estime en moyennant, item par item, la part de masse
                # rare portee par la modale du segment.
                tem = C.temoin_item(m["faux_maj"] & cv["multi"][None, :],
                                    cv["rare_vrai"] & cv["multi"][None, :],
                                    _egalite_modale(cv, C.AXE_PRINCIPAL))
                num_j, den_j = mesure_h2a(cv, {"faux_maj": m["juste"], "pred": m["pred"]},
                                          C.AXE_PRINCIPAL, cv["modale_seg"][C.AXE_PRINCIPAL])
                lignes_mes.append({**ligne_base, "mecanisme": MECANISMES[1],
                                   "cellules": int(den.sum()), "valeur": v,
                                   "ic_bas": b, "ic_haut": h, "temoin": tem,
                                   "exces": v - tem if np.isfinite(v) else np.nan,
                                   "valeur_raretes_justes": C.taux(num_j, den_j),
                                   "cellules_justes": int(den_j.sum())})

                # ---- H3, position extreme
                (num, den), p1, pK, hors = mesure_h3(cv, m)
                v, b, h, _ = C.taux_ic(num, den, idx_boot)
                tem = C.temoin_item(m["faux_maj"], cv["rare_vrai"], cv["ext_vrai"])
                num_j, den_j = C.par_personne(p1 | pK, m["juste"])
                lignes_mes.append({**ligne_base, "mecanisme": MECANISMES[2],
                                   "cellules": int(den.sum()), "valeur": v,
                                   "ic_bas": b, "ic_haut": h, "temoin": tem,
                                   "exces": v - tem if np.isfinite(v) else np.nan,
                                   "valeur_raretes_justes": C.taux(num_j, den_j),
                                   "cellules_justes": int(den_j.sum()),
                                   "hors_nomenclature": hors})
                n_f = max(int(m["faux_maj"].sum()), 1)
                lignes_pos.append({
                    "perimetre": nom_per, "seuil": seuil, "condition": nom,
                    "fausses_raretes": int(m["faux_maj"].sum()),
                    "part_premiere": float((p1 & m["faux_maj"]).sum()) / n_f,
                    "part_derniere": float((pK & m["faux_maj"]).sum()) / n_f,
                    "part_milieu": 1.0 - float(((p1 | pK) & m["faux_maj"]).sum()) / n_f,
                    "temoin_premiere": C.temoin_item(m["faux_maj"], cv["rare_vrai"],
                                                     cv["ext1_vrai"]),
                    "temoin_derniere": C.temoin_item(m["faux_maj"], cv["rare_vrai"],
                                                     cv["extK_vrai"])})

                # ---- H5, rarete du contexte
                num, den = C.moyenne_par_personne(m["faux_maj"], cv["ctx"])
                v, b, h, _ = C.taux_ic(num, den, idx_boot)
                num_j, den_j = C.moyenne_par_personne(m["juste"], cv["ctx"])
                tem = C.temoin_item(m["faux_maj"], cv["ok"], cv["ctx"])
                lignes_mes.append({**ligne_base, "mecanisme": MECANISMES[3],
                                   "cellules": int(den.sum()), "valeur": v,
                                   "ic_bas": b, "ic_haut": h, "temoin": tem,
                                   "exces": v - tem if np.isfinite(v) else np.nan,
                                   "valeur_raretes_justes": C.taux(num_j, den_j),
                                   "cellules_justes": int(den_j.sum())})

                # ---- H1b et H2b, exces contre le temoin aveugle a la personne
                for cle, mat, mec in (("personne", cv["r_personne"], MECANISMES[5]),
                                      ("segment",
                                       cv["r_segment"][C.AXE_PRINCIPAL], MECANISMES[6])):
                    num, den = C.moyenne_par_personne(m["faux_maj"], mat)
                    v, b, h, _ = C.taux_ic(num, den, idx_boot)
                    tem = C.temoin_item(m["faux_maj"], cv["ok"], mat)
                    num_j, den_j = C.moyenne_par_personne(m["juste"], mat)
                    lignes_mes.append({**ligne_base, "mecanisme": mec,
                                       "cellules": int(den.sum()), "valeur": v,
                                       "ic_bas": b, "ic_haut": h, "temoin": tem,
                                       "exces": v - tem if np.isfinite(v) else np.nan,
                                       "valeur_raretes_justes": C.taux(num_j, den_j),
                                       "cellules_justes": int(den_j.sum())})

                # ---- H4, sur confiance, C2 et C3 seulement
                if nom in conf and nom_per == "150":
                    pmax = conf[nom]["pmax"]
                    ent = conf[nom]["entropie"]
                    sur = pmax > 0.99
                    num, den = C.par_personne(sur, m["faux_maj"])
                    v, b, h, _ = C.taux_ic(num, den, idx_boot)
                    num_j, den_j = C.par_personne(sur, m["juste"])
                    lignes_mes.append({**ligne_base, "mecanisme": MECANISMES[4],
                                       "cellules": int(den.sum()), "valeur": v,
                                       "ic_bas": b, "ic_haut": h,
                                       "temoin": C.taux(*C.par_personne(
                                           sur, cv["ok"] & ~m["rare_pred"])),
                                       "exces": np.nan,
                                       "valeur_raretes_justes": C.taux(num_j, den_j),
                                       "cellules_justes": int(den_j.sum())})
                    if seuil == 0.10:
                        for libelle, masque in (("fausse rarete", m["faux_maj"]),
                                                ("rarete juste", m["juste"]),
                                                ("mauvaise modalite rare", m["faux_min"]),
                                                ("rarete non osee, cellule majoritaire",
                                                 cv["ok"] & ~m["rare_pred"])):
                            sel = masque & ~np.isnan(pmax)
                            n = int(sel.sum())
                            lignes_conf.append({
                                "condition": nom, "cellules": libelle, "n": n,
                                "p_max_moyen": float(pmax[sel].mean()) if n else np.nan,
                                "p_max_median": float(np.median(pmax[sel])) if n else np.nan,
                                "part_p_max_sup_099": float((pmax[sel] > 0.99).mean())
                                if n else np.nan,
                                "entropie_moyenne_bits": float(ent[sel].mean())
                                if n else np.nan})

            print(f"  perimetre {nom_per}, seuil {seuil:.2f} : fait "
                  f"({time.time() - t0:.0f} s)", flush=True)

    # ------------------------------------------------------- quintiles de contexte, H5
    for nom_per in ("1052", "150"):
        cv, mq, _ = cache[(nom_per, 0.10)]
        ctx = cv["ctx"]
        bornes = np.quantile(ctx[cv["ok"] & ~np.isnan(ctx)], [0.2, 0.4, 0.6, 0.8])
        for nom in mq:
            m = mq[nom]
            sel = m["rare_pred"] & ~np.isnan(ctx)
            if sel.sum() < 20:
                continue
            v = ctx[sel]
            q = np.searchsorted(bornes, v, side="right")
            faux = m["faux_maj"][sel]
            for k in range(5):
                mk = q == k
                lignes_quint.append({
                    "perimetre": nom_per, "condition": nom, "quintile": k + 1,
                    "raretes_osees": int(mk.sum()),
                    "taux_fausses_raretes": float(faux[mk].mean()) if mk.any() else np.nan,
                    "rarete_contexte_moyenne": float(v[mk].mean()) if mk.any() else np.nan})

    mes = pd.DataFrame(lignes_mes)
    axe = pd.DataFrame(lignes_axe)
    pos = pd.DataFrame(lignes_pos)
    cfd = pd.DataFrame(lignes_conf)
    qui = pd.DataFrame(lignes_quint)

    # ------------------------------------------------------------------- contrastes
    contr = []
    for nom, nom_per in C.PERIMETRE_NATUREL.items():
        cv, mq, idx_boot = cache[(nom_per, 0.10)]
        if nom not in mq:
            continue
        m, hum = mq[nom], mq["humains vague 2"]

        a = mesure_h1a(cv, m)
        b = mesure_h1a(cv, hum)
        o, lo, hi, p = C.contraste(*a, *b, idx_boot)
        contr.append({"famille": "primaire", "hypothese": MECANISMES[0],
                      "comparaison": "contre les humains vague 2", "condition": nom,
                      "perimetre": nom_per, "difference": o, "ic_bas": lo,
                      "ic_haut": hi, "p_bootstrap": p})

        a = mesure_h2a(cv, m, C.AXE_PRINCIPAL, cv["modale_seg"][C.AXE_PRINCIPAL])
        b = mesure_h2a(cv, hum, C.AXE_PRINCIPAL, cv["modale_seg"][C.AXE_PRINCIPAL])
        o, lo, hi, p = C.contraste(*a, *b, idx_boot)
        contr.append({"famille": "primaire", "hypothese": MECANISMES[1],
                      "comparaison": "contre les humains vague 2", "condition": nom,
                      "perimetre": nom_per, "difference": o, "ic_bas": lo,
                      "ic_haut": hi, "p_bootstrap": p})

        (num, den), _p1, _pK, _ = mesure_h3(cv, m)
        # temoin : les modalites rares REELLEMENT donnees par les humains sur les memes
        # items, ponderees pour reproduire la composition en items des fausses raretes.
        num_h, den_h = C.temoin_par_personne(m["faux_maj"], cv["rare_vrai"],
                                             cv["ext_vrai"].astype(float))
        o, lo, hi, p = C.contraste(num, den, num_h, den_h, idx_boot)
        contr.append({"famille": "primaire", "hypothese": MECANISMES[2],
                      "comparaison": "contre les vraies raretes humaines",
                      "condition": nom, "perimetre": nom_per, "difference": o,
                      "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p})

        a = C.moyenne_par_personne(m["faux_maj"], cv["ctx"])
        b = C.moyenne_par_personne(m["juste"], cv["ctx"])
        o, lo, hi, p = C.contraste(*a, *b, idx_boot)
        contr.append({"famille": "primaire", "hypothese": MECANISMES[3],
                      "comparaison": "fausses raretes contre raretes justes",
                      "condition": nom, "perimetre": nom_per, "difference": o,
                      "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p})

        if nom in conf:
            sur = conf[nom]["pmax"] > 0.99
            a = C.par_personne(sur, m["faux_maj"])
            b = C.par_personne(sur, m["juste"])
            o, lo, hi, p = C.contraste(*a, *b, idx_boot)
            contr.append({"famille": "primaire", "hypothese": MECANISMES[4],
                          "comparaison": "fausses raretes contre raretes justes",
                          "condition": nom, "perimetre": nom_per, "difference": o,
                          "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p})

        for mat, mec in ((cv["r_personne"], MECANISMES[5]),
                         (cv["r_segment"][C.AXE_PRINCIPAL], MECANISMES[6])):
            num, den = C.moyenne_par_personne(m["faux_maj"], mat)
            num_t, den_t = C.temoin_par_personne(m["faux_maj"], cv["ok"], mat)
            o, lo, hi, p = C.contraste(num, den, num_t, den_t, idx_boot)
            contr.append({"famille": "secondaire", "hypothese": mec,
                          "comparaison": "contre le temoin aveugle a la personne",
                          "condition": nom, "perimetre": nom_per, "difference": o,
                          "ic_bas": lo, "ic_haut": hi, "p_bootstrap": p})

    # Ablation C2 contre C3, POST HOC, hors des deux familles declarees. Elle n'y entre
    # pas parce qu'elle a ete ajoutee apres avoir vu que H2b separait les deux ; elle est
    # corrigee separement sur ses cinq tests et signalee comme post hoc partout.
    cv150, mq150, idx150 = cache[("150", 0.10)]
    if "C2" in mq150 and "C3" in mq150:
        a2, a3 = mq150["C2"], mq150["C3"]
        paires = [
            (MECANISMES[0], mesure_h1a(cv150, a2), mesure_h1a(cv150, a3)),
            (MECANISMES[1],
             mesure_h2a(cv150, a2, C.AXE_PRINCIPAL, cv150["modale_seg"][C.AXE_PRINCIPAL]),
             mesure_h2a(cv150, a3, C.AXE_PRINCIPAL, cv150["modale_seg"][C.AXE_PRINCIPAL])),
            (MECANISMES[2], mesure_h3(cv150, a2)[0], mesure_h3(cv150, a3)[0]),
            (MECANISMES[5],
             C.moyenne_par_personne(a2["faux_maj"], cv150["r_personne"]),
             C.moyenne_par_personne(a3["faux_maj"], cv150["r_personne"])),
            (MECANISMES[6],
             C.moyenne_par_personne(a2["faux_maj"],
                                    cv150["r_segment"][C.AXE_PRINCIPAL]),
             C.moyenne_par_personne(a3["faux_maj"],
                                    cv150["r_segment"][C.AXE_PRINCIPAL])),
        ]
        for mec, ua, ub in paires:
            o, lo, hi, p = C.contraste(*ua, *ub, idx150)
            contr.append({"famille": "post hoc, ablation", "hypothese": mec,
                          "comparaison": "C2 avec etiquette contre C3 sans etiquette",
                          "condition": "C2 moins C3", "perimetre": "150",
                          "difference": o, "ic_bas": lo, "ic_haut": hi,
                          "p_bootstrap": p})

    ct = pd.DataFrame(contr)
    ct["p_holm"] = np.nan
    ct["p_bh"] = np.nan
    for libelle in ("primaire", "secondaire", "post hoc, ablation"):
        idx = ct[ct.famille == libelle].index
        ct.loc[idx, "p_holm"] = C.holm(ct.loc[idx, "p_bootstrap"].values)
        ct.loc[idx, "p_bh"] = C.benjamini_hochberg(ct.loc[idx, "p_bootstrap"].values)

    # -------------------------------------------------------- synthese, ordre des exces
    syn = []
    d10 = mes[mes.seuil == 0.10]
    couples = list(C.PERIMETRE_NATUREL.items()) + [("humains vague 2", "1052"),
                                                   ("humains vague 2", "150")]
    for nom, nom_per in couples:
        g = d10[(d10.perimetre == nom_per) & (d10.condition == nom)]
        h = d10[(d10.perimetre == nom_per) & (d10.condition == "humains vague 2")]
        for mec in MECANISMES:
            a = g[g.mecanisme == mec]
            b = h[h.mecanisme == mec]
            if a.empty:
                continue
            syn.append({"perimetre": nom_per, "condition": nom, "mecanisme": mec,
                        "cellules": int(a.cellules.iloc[0]),
                        "valeur": float(a.valeur.iloc[0]),
                        "temoin": float(a.temoin.iloc[0]),
                        "exces": float(a.exces.iloc[0]),
                        "valeur_humains": float(b.valeur.iloc[0]) if not b.empty else np.nan,
                        "ecart_aux_humains": (float(a.valeur.iloc[0]) - float(b.valeur.iloc[0]))
                        if not b.empty else np.nan,
                        "valeur_raretes_justes": float(a.valeur_raretes_justes.iloc[0])})
    sy = pd.DataFrame(syn)
    with np.errstate(invalid="ignore", divide="ignore"):
        sy["lift"] = sy.valeur / sy.temoin

    # Le depart entre H1 et H2, lisible sur une ligne par condition : le meme exces,
    # rapporte a son propre temoin, du cote de la PERSONNE et du cote du SEGMENT.
    lev = []
    for nom_per in ("1052", "150"):
        g = sy[sy.perimetre == nom_per]
        for nom in sorted(set(g.condition)):
            a = g[(g.condition == nom) & (g.mecanisme == MECANISMES[5])]
            b = g[(g.condition == nom) & (g.mecanisme == MECANISMES[6])]
            if a.empty or b.empty:
                continue
            lp = float(a.lift.iloc[0]) - 1.0
            ls = float(b.lift.iloc[0]) - 1.0
            lev.append({"perimetre": nom_per, "condition": nom,
                        "lift_personne": lp, "lift_segment": ls,
                        "rapport_segment_sur_personne": ls / lp if lp > 0 else np.nan})
    lv = pd.DataFrame(lev)

    # Le levier de calibration, mesure et non suppose : que gagne t on a n'oser une
    # modalite rare qu'au dessus d'un seuil de confiance ? C2 et C3 seulement.
    seuils_conf = []
    cv150, mq150, _ = cache[("150", 0.10)]
    for nom in ("C2", "C3"):
        if nom not in conf or nom not in mq150:
            continue
        pmax = conf[nom]["pmax"]
        m = mq150[nom]
        rv = cv150["rare_vrai"]
        for s in (0.0, 0.5, 0.8, 0.9, 0.95, 0.99, 0.999):
            garde = m["rare_pred"] & (pmax >= s)
            juste = garde & m["juste"]
            n_pred = int(garde.sum())
            seuils_conf.append({
                "condition": nom, "seuil_p_max": s,
                "raretes_osees": n_pred,
                "raretes_justes": int(juste.sum()),
                "rappel": float(juste.sum()) / max(int(rv.sum()), 1),
                "precision": float(juste.sum()) / n_pred if n_pred else np.nan,
                "taux_fausses_raretes": float((garde & ~m["juste"] & ~rv).sum()) / n_pred
                if n_pred else np.nan,
                "masse_predite": n_pred / max(int(cv150["ok"].sum()), 1)})
    sc = pd.DataFrame(seuils_conf)
    if not sc.empty:
        sc["f1"] = np.where((sc.rappel + sc.precision) > 0,
                            2 * sc.rappel * sc.precision / (sc.rappel + sc.precision), 0.0)

    C.ecrire(lv, "a31-leviers-personne-segment.csv")
    C.ecrire(sc, "a31-leviers-seuil-confiance.csv")
    C.ecrire(mes, "a31-mecanismes.csv")
    C.ecrire(ct, "a31-contrastes.csv")
    C.ecrire(axe, "a31-h2-par-axe.csv")
    C.ecrire(pos, "a31-h3-positions.csv")
    C.ecrire(cfd, "a31-h4-confiance.csv")
    C.ecrire(qui, "a31-h5-quintiles.csv")
    C.ecrire(sy, "a31-synthese-mecanismes.csv")
    C.ecrire(pd.DataFrame(controles), "a31-controles.csv")

    # ---------------------------------------------------------------------- affichage
    pd.set_option("display.width", 250)
    ordre = {c: i for i, c in enumerate(C.ORDRE_METHODES)}
    for nom_per in ("1052", "150"):
        for mec in MECANISMES:
            s = d10[(d10.perimetre == nom_per) & (d10.mecanisme == mec)].copy()
            if s.empty:
                continue
            s["o"] = s.condition.map(ordre)
            print("\n" + "=" * 130)
            print(f"{mec}, perimetre {nom_per}, seuil 10 %")
            print("=" * 130)
            print(s.sort_values("o")[["condition", "fausses_raretes", "cellules",
                                      "valeur", "ic_bas", "ic_haut", "temoin", "exces",
                                      "valeur_raretes_justes"]]
                  .round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Contrastes et corrections pour tests multiples")
    print("=" * 130)
    c2 = ct.copy()
    c2["o"] = c2.condition.map(ordre)
    print(c2.sort_values(["famille", "hypothese", "o"])[
        ["famille", "hypothese", "condition", "perimetre", "difference", "ic_bas",
         "ic_haut", "p_bootstrap", "p_holm", "p_bh"]].round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("H2a par axe, perimetre 1 052, seuil 10 %")
    print("=" * 130)
    s = axe[(axe.perimetre == "1052") & (axe.seuil == 0.10)].copy()
    print(s.pivot_table(index="condition", columns="reference", values="valeur")
          .reindex([c for c in C.ORDRE_METHODES
                    if c in set(s.condition)]).round(3).to_string())

    print("\n" + "=" * 130)
    print("H3, position des fausses raretes")
    print("=" * 130)
    s = pos[(pos.seuil == 0.10)].copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values(["perimetre", "o"]).drop(columns="o").round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("H4, confiance de C2 et C3 par type de cellule")
    print("=" * 130)
    print(cfd.round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("H5, taux de fausses raretes par quintile de rarete du contexte")
    print("=" * 130)
    s = qui.copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values(["perimetre", "o", "quintile"]).drop(columns="o")
          .round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Le depart entre H1 et H2 : exces du cote de la personne contre exces du cote "
          "du segment")
    print("=" * 130)
    s = lv.copy()
    s["o"] = s.condition.map(ordre)
    print(s.sort_values(["perimetre", "o"]).drop(columns="o").round(4).to_string(index=False))

    print("\n" + "=" * 130)
    print("Levier de calibration : n'oser une rarete qu'au dessus d'un seuil de p max")
    print("=" * 130)
    print(sc.round(4).to_string(index=False))

    print(f"\nduree {time.time() - t0:.0f} s")


def _egalite_modale(cv, axe):
    """Matrice booleenne : la vraie reponse humaine est la modale rare de son segment.

    Elle sert de temoin a H2a : c'est la part de la masse rare reelle qui tombe deja sur
    la modalite rare modale du segment. Une methode qui tirerait sa modalite rare dans la
    masse rare de la population du meme item obtiendrait cette valeur la.
    """
    ref = cv["modale_seg"][axe]
    out = np.zeros(cv["ok"].shape, dtype=bool)
    lignes, cols = np.nonzero(cv["rare_vrai"] & cv["multi"][None, :] & (ref != None))  # noqa: E711
    for i, j in zip(lignes, cols):
        out[i, j] = cv["verite"][i, j] == ref[i, j]
    return out


if __name__ == "__main__":
    main()
