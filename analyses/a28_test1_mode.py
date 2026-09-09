"""
a28_test1_mode : test decisif de l'idee de rang 1, "la simulation devie la ou les humains
se surveillent". Version durcie de a25.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. a25_commun, a25_mesures, a2_commun,
a2_baselines_gss et a28_commun sont importes tels quels.

Ce que a25 laissait ouvert et que ce script ferme, dans l'ordre du cahier des charges :

  (a) correction pour tests multiples, sur une famille d'hypotheses fixee AVANT d'avoir
      regarde les resultats et ecrite ci dessous ;
  (b) la version continue du croisement : un score de sensibilite par item, construit a
      partir des classes ordonnees de NORC et des ampleurs publiees de corpus/04, correle
      a l'ecart agent contre humain item par item, avec intervalle bootstrap sur les items ;
  (c) robustesse : retrait un a un des quatre items nominaux qui portent l'effet ;
  (d) stratification par type d'item, binaire, nominal a trois modalites et plus, ordinal
      a trois modalites et plus ;
  (e) le meme contraste sur la DISPERSION, rapport d'entropie agent sur humain par item,
      et non plus seulement sur la distance de distribution. La question ajoutee est :
      la simulation efface t elle plus de variete sur les items sensibles ?

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT LES RESULTATS
===========================================================================
Elle est ecrite ici, dans le code, et recopiee telle quelle dans le rapport. La dette
etait ouverte depuis a17 ; elle se solde en nommant ce qui est teste et en comptant tout
ce qui est teste.

  H1  (primaire, metrique de distance). Pour chacune des 13 methodes non humaines, la
      distance moyenne entre population simulee et population humaine est plus grande sur
      les 12 items que NORC classe "likely mode sensitive" que sur ses 65 temoins
      negatifs. Perimetre 150. 13 tests.
  H2  (primaire, metrique de dispersion). Pour chacune des 13 methodes non humaines, le
      rapport d'entropie agent sur humain est plus BAS sur les 12 items sensibles que sur
      les 65 temoins. Perimetre 150. 13 tests.
  H3  (secondaire, version continue). Pour chacune des 13 methodes non humaines, la
      correlation de rang entre le score de sensibilite par item et la distance par item
      est positive. Score NORC ordinal. Perimetre 150. 13 tests.
  H4  (secondaire, sens de l'ecart). Pour chacune des 13 methodes non humaines, le
      deplacement vers le pole socialement desirable est plus grand sur les 12 items
      sensibles que sur les temoins. Perimetre 150. 13 tests.

  Famille declaree : H1 union H2 union H3 union H4, soit 52 tests. Correction principale :
  Holm sur les 52, qui controle le taux d'erreur par famille sans hypothese de dependance.
  Correction secondaire rapportee a cote : Benjamini Hochberg sur les 52, qui controle le
  taux de fausses decouvertes mais suppose une dependance positive non verifiee ici.
  Les p par sous famille de 13 sont aussi donnes, pour le lecteur qui juge H1 seule
  digne d'etre pre enregistree.

  N'entrent PAS dans la famille, et sont rapportes comme des descriptions :
  la ligne "humains vague 2", qui est un temoin negatif et non une hypothese ; les
  analyses de robustesse (c) et (d), qui sont conditionnelles a H1 ; les correlations sur
  les scores de litterature et composite, qui sont exploratoires ; le perimetre 1 052,
  qui est une replication sur un echantillon emboite et non un test independant.
===========================================================================

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl, resultats/a25-croisement.csv.
Sortie  : resultats/a28-t1-par-item.csv, a28-t1-contrastes.csv, a28-t1-continu.csv,
          a28-t1-robustesse.csv, a28-t1-strates.csv, a28-t1-scores-items.csv.

Usage :
  .venv/bin/python analyses/a28_test1_mode.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 50000
"""

import argparse
import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C
from a2_commun import est_manquant
from a25_commun import ORDINAUX, options_par_item, sans_score, scores_desirabilite
from a25_mesures import desirabilite_moyenne, distance

# ---------------------------------------------------------------------------
# (b) Le score de sensibilite par item
# ---------------------------------------------------------------------------
#
# Deux composantes, declarees separement et jamais fusionnees en douce.
#
# S1, classes ordonnees de NORC : temoin 0, a investiguer 1, sensible 2. C'est la version
# continue la plus proche de ce que a25 testait en categoriel. Elle couvre 90 items sur
# 149 ; les items "mixte" et "non teste" sont hors mesure.
#
# S2, ampleur publiee, en points de pourcentage d'ecart entre ce qui est declare et ce qui
# est cache ou observe. Chaque valeur vient d'une mesure de corpus/04 et porte sa source.
# Regle stricte : quand la litterature de corpus/04 n'a pas mesure le domaine, la valeur
# est absente, PAS zero. Zero est reserve aux domaines ou la litterature a cherche et n'a
# rien trouve, ce qui est un resultat et non une lacune. C'est ce qui rend la couverture
# de S2 plus faible que celle de S1, et le rapport le dit.
#
# S3, composite : moyenne des rangs normalises de S1 et de S2, sur les items ou les deux
# existent. C'est la mesure la plus exigeante et la moins couverte.

AMPLEURS = {
    # (points, niveau, source)
    "religion": (10.0, "[PROBABLE]",
                 "Presser et Stinson 1998, corpus 04-13 : un tiers de pratique "
                 "hebdomadaire en moins sans enqueteur, soit environ 10 points sur la "
                 "base americaine ; NORC 04-18 confirme la direction"),
    "vote declare": (15.8, "[CONFIRME]",
                     "Ansolabehere et Hersh 2012, corpus 04-20 : 84,3 pour cent declare "
                     "contre 68,5 valide"),
    "choix de candidat": (0.0, "[CONFIRME]",
                          "Coppock 2017 corpus 04-30 et AAPOR 2021 corpus 04-31 : aucun "
                          "electeur cache detecte. Zero est ici un resultat mesure"),
    "attitude raciale": (13.5, "[CONFIRME]",
                         "Berinsky 1999, corpus 04-19 : 13,5 points de soutien en trop a "
                         "l'integration scolaire apres correction"),
    "immigration": (10.0, "[CONFIRME]",
                    "Bursztyn, Egorov et Fiorin 2020, corpus 04-27 : 30 pour cent en "
                    "prive contre 20 en public"),
    "hostilite envers les gays": (10.0, "[PROBABLE]",
                                  "Coffman, Coffman et Ericson 2017, corpus 04-21 : la "
                                  "desapprobation d'un manager gay augmente de 67 pour "
                                  "cent sous le voile ; conversion en points faite par "
                                  "nous sur une base d'environ 15 pour cent"),
    "mariage entre personnes de meme sexe": (0.0, "[CONFIRME]",
                                             "Lax, Phillips et Stollwerk 2016, corpus "
                                             "04-22 : aucune preuve de desirabilite. Zero "
                                             "est ici un resultat mesure"),
    "conduite sexuelle": (6.0, "[PROBABLE]",
                          "Gnambs et Kaspar 2015, corpus 04-14 : Omega = 1,29 sur les "
                          "comportements sexuels ; Tourangeau et Yan 2007, corpus 04-03"),
    "satisfaction et bien etre": (5.5, "[PROBABLE]",
                                  "Pew 2015, corpus 04-15 : ecart moyen de 5,5 points sur "
                                  "60 questions, les plus gros ecarts du panneau etant sur "
                                  "la satisfaction, 18 et 14 points"),
    "discrimination percue": (13.0, "[HYPOTHESE]",
                              "Pew 2015, corpus 04-15 : 12 a 15 points sur les items de "
                              "discrimination percue. Nos items portent sur la "
                              "discrimination inverse, le transfert est une hypothese"),
    "revenu et statut": (8.0, "[PROBABLE]",
                         "Tourangeau et Yan 2007, corpus 04-03 : le revenu est un item "
                         "sensible classique ; Kreuter, Presser et Tourangeau 2008, "
                         "corpus 04-11 : 25 points sur un fait scolaire embarrassant et "
                         "une non reponse a l'item multipliee par sept au telephone"),
    "chomage passe": (5.0, "[HYPOTHESE]",
                      "Kreuter et al. 2008, corpus 04-11 : les faits stigmatises sont "
                      "sous declares en presence d'un enqueteur ; ampleur transposee"),
    "drogues, opinion": (2.0, "[HYPOTHESE]",
                         "Gnambs et Kaspar 2015 mesurent Omega = 1,17 sur le "
                         "COMPORTEMENT ; l'opinion sur la legalisation est bien moins "
                         "exposee, valeur basse assumee"),
    "tolerance politique": (4.0, "[HYPOTHESE]",
                            "Tourangeau et Yan 2007, corpus 04-03 : les items de "
                            "tolerance sont sur declares du cote tolerant ; aucune "
                            "ampleur publiee par item"),
    "roles de genre": (4.0, "[HYPOTHESE]",
                       "NORC 04-18 note des reponses plus extremes sur le web pour les "
                       "items de femmes au travail ; aucune ampleur chiffree"),
    "punition corporelle": (5.0, "[HYPOTHESE]",
                            "fait devenu stigmatise ; aucune mesure publiee dans corpus/04"),
}

DOMAINE = {
    **{it: "religion" for it in ["attend", "pray", "reborn", "savesoul", "postlife",
                                 "bible"]},
    "vote16": "vote declare",
    "pres16": "choix de candidat", "if16who": "choix de candidat",
    **{it: "attitude raciale" for it in ["racdif1", "racdif2", "racdif3", "racdif4",
                                         "spkrac/y", "colrac", "librac/y", "natrace/y",
                                         "racwork", "wlthblks", "wlthwhts", "wlthhsps"]},
    "letin1a": "immigration",
    **{it: "hostilite envers les gays" for it in ["homosex", "spkhomo/y", "colhomo",
                                                  "libhomo/y"]},
    "marhomo": "mariage entre personnes de meme sexe",
    **{it: "conduite sexuelle" for it in ["xmarsex", "xmovie", "pillok", "sexeduc",
                                          "pornlaw"]},
    **{it: "satisfaction et bien etre" for it in ["happy", "hapmar", "satfin", "satjob",
                                                  "life", "health", "finalter", "parsol"]},
    **{it: "discrimination percue" for it in ["discaff", "discaffw", "discaffm"]},
    **{it: "revenu et statut" for it in ["income", "incom16", "finrela", "class"]},
    "unemp": "chomage passe",
    "grass": "drogues, opinion",
    **{it: "tolerance politique" for it in ["spkath/y", "colath", "spkcom/y", "colcom/y",
                                            "libcom/y"]},
    **{it: "roles de genre" for it in ["fefam", "fepresch", "fechld", "fehire", "fepol"]},
    "spanking": "punition corporelle",
}

CLASSE_ORDINALE = {"temoin": 0.0, "investiguer": 1.0, "sensible": 2.0}

# Les quatre items nominaux dont a25 montre qu'ils portent l'essentiel du contraste.
QUATRE_NOMINAUX = ["spkrac/y", "polabuse/y", "polattak/y", "vote16"]


def scores_sensibilite(items, classes):
    """Construit S1, S2 et S3 item par item, et renvoie le tableau declaratif."""
    lignes = []
    for it in items:
        cl = classes[it]
        s1 = CLASSE_ORDINALE.get(cl, np.nan)
        dom = DOMAINE.get(it)
        if dom is None:
            s2, niveau, source = np.nan, "", "domaine non mesure par corpus/04"
        else:
            s2, niveau, source = AMPLEURS[dom]
        lignes.append({"item": it, "classe_norc": cl, "s1_norc": s1,
                       "domaine": dom or "", "s2_points": s2,
                       "niveau_s2": niveau, "source_s2": source})
    t = pd.DataFrame(lignes)
    # S3 : moyenne des rangs normalises, sur les items ou S1 et S2 existent.
    from scipy.stats import rankdata
    ok = t.s1_norc.notna() & t.s2_points.notna()
    t["s3_composite"] = np.nan
    if ok.sum() >= 4:
        r1 = rankdata(t.loc[ok, "s1_norc"].values)
        r2 = rankdata(t.loc[ok, "s2_points"].values)
        n = ok.sum()
        t.loc[ok, "s3_composite"] = 0.5 * ((r1 - 1) / (n - 1) + (r2 - 1) / (n - 1))
    return t


# ---------------------------------------------------------------------------
# Mesures par item
# ---------------------------------------------------------------------------

def mesurer(paquet, lignes, conditions):
    """Distance, rapport d'entropie et sens de l'ecart, par condition et par item."""
    items, y1, M, options = (paquet["items"], paquet["y1"], paquet["M"],
                             paquet["options"])
    codage = {}
    for it in items:
        opts = options[it]
        ordinal = it in ORDINAUX and not any(sans_score(o) for o in opts)
        sc, _, _ = scores_desirabilite(it, opts)
        index = {o: k for k, o in enumerate(opts)}
        vec = np.zeros(len(opts))
        defini = np.zeros(len(opts))
        if sc:
            for o, v in sc.items():
                vec[index[o]] = v
                defini[index[o]] = 1.0
        codage[it] = (index, vec, defini, ordinal)

    def compte(mat, j, it):
        index = codage[it][0]
        c = np.zeros(len(options[it]))
        for v in mat[lignes, j]:
            if v is None or est_manquant(v):
                continue
            k = index.get(C.norm(v))
            if k is not None:
                c[k] += 1
        return c

    out = []
    for j, it in enumerate(items):
        ch = compte(y1, j, it)
        if ch.sum() == 0:
            continue
        ph = ch / ch.sum()
        _, vec, defini, ordinal = codage[it]
        h_hum = C._h_mm(ch)
        dh, _ = desirabilite_moyenne(ph[None, :], vec, defini)
        for cond in conditions:
            cs = compte(M[cond], j, it)
            if cs.sum() == 0:
                continue
            ps = cs / cs.sum()
            h_sim = C._h_mm(cs)
            ds, masse = desirabilite_moyenne(ps[None, :], vec, defini)
            out.append({
                "condition": cond, "item": it,
                "n_cellules": int(cs.sum()),
                "distance": float(distance(ps[None, :], ph[None, :], ordinal)[0]),
                "entropie_humaine": float(h_hum), "entropie_simulee": float(h_sim),
                "ratio_entropie": float(h_sim / h_hum) if h_hum > 1e-9 else np.nan,
                "ecart_desirabilite": (float(ds[0] - dh[0]) if defini.sum()
                                       else np.nan),
            })
    return pd.DataFrame(out)


def contraste(d, metrique, groupe_a, groupe_b, tirages, rng):
    a = d.loc[d.classe_norc == groupe_a, metrique].values
    b = d.loc[d.classe_norc == groupe_b, metrique].values
    _, bas, haut = C.bootstrap_items(a, b, min(tirages, 10000), rng)
    _, p = C.permutation(a, b, tirages, rng)
    # La difference brute est toujours rapportee, meme quand une strate n'a qu'un seul
    # item : c'est le cas de la strate nominale a trois modalites et plus, qui ne contient
    # que vote16. L'intervalle et le p, eux, restent absents, et le rapport le dit.
    with np.errstate(invalid="ignore"):
        brut = (float(np.nanmean(a)) - float(np.nanmean(b))
                if np.sum(~np.isnan(a)) and np.sum(~np.isnan(b)) else np.nan)
    return {
        "moyenne_groupe": float(np.nanmean(a)) if np.sum(~np.isnan(a)) else np.nan,
        "moyenne_temoin": float(np.nanmean(b)) if np.sum(~np.isnan(b)) else np.nan,
        "n_groupe": int(np.sum(~np.isnan(a))), "n_temoin": int(np.sum(~np.isnan(b))),
        "difference": brut, "ic_items_bas": bas, "ic_items_haut": haut,
        "p_permutation": p,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--tirages", type=int, default=50000)
    ap.add_argument("--graine", type=int, default=20260908)
    args = ap.parse_args()

    paquet = C.charger_tout(args.cache, args.cache_foret)
    items, options = paquet["items"], paquet["options"]
    classes = C.classes_items(items)
    types = {it: C.type_item(it, options) for it in items}
    rng = np.random.default_rng(args.graine)

    print(__doc__.split("=" * 75)[1])

    # ------------------------------------------------------------ scores d'items
    scores = scores_sensibilite(items, classes)
    scores["type"] = scores.item.map(types)
    C.ecrire(scores, "a28-t1-scores-items.csv")
    print("\ncouverture des trois scores de sensibilite :")
    print(f"  S1 NORC ordinal        : {int(scores.s1_norc.notna().sum())} items sur {len(items)}")
    print(f"  S2 ampleur publiee     : {int(scores.s2_points.notna().sum())} items sur {len(items)}")
    print(f"  S3 composite           : {int(scores.s3_composite.notna().sum())} items sur {len(items)}")

    # ------------------------------------------------------------- mesures
    toutes = [c for c in C.ORDRE_METHODES if c in paquet["M"]]
    non_humaines = [c for c in toutes if c != "humains vague 2"]
    par_item = {}
    for nom_per, lignes in [("150", paquet["lignes150"]),
                            ("1052", np.arange(len(paquet["ids"])))]:
        conds = toutes if nom_per == "150" else [c for c in toutes if c not in ("C2", "C3")]
        d = mesurer(paquet, lignes, conds)
        d["perimetre"] = nom_per
        d["classe_norc"] = d.item.map(classes)
        d["type"] = d.item.map(types)
        par_item[nom_per] = d
        print(f"  perimetre {nom_per} : {len(d)} couples condition x item", flush=True)
    tout_item = pd.concat(par_item.values(), ignore_index=True)
    C.ecrire(tout_item, "a28-t1-par-item.csv")

    # ------------------------------------------------- H1, H2, H4 : les contrastes
    lignes = []
    for nom_per, d in par_item.items():
        for cond, dd in d.groupby("condition"):
            for hyp, metrique in [("H1 distance", "distance"),
                                  ("H2 dispersion", "ratio_entropie"),
                                  ("H4 desirabilite", "ecart_desirabilite")]:
                r = contraste(dd, metrique, "sensible", "temoin", args.tirages, rng)
                lignes.append({"perimetre": nom_per, "hypothese": hyp,
                               "condition": cond, "metrique": metrique, **r})
            # la classe adjacente, en description et non en test
            r = contraste(dd, "distance", "investiguer", "temoin", args.tirages, rng)
            lignes.append({"perimetre": nom_per, "hypothese": "descriptif investiguer",
                           "condition": cond, "metrique": "distance", **r})
    contrastes = pd.DataFrame(lignes)

    # ------------------------------------------------- H3 : la version continue
    lignes_c = []
    for nom_per, d in par_item.items():
        sc = scores.set_index("item")
        for cond, dd in d.groupby("condition"):
            dd = dd.set_index("item")
            for nom_s, col in [("S1 NORC ordinal", "s1_norc"),
                               ("S2 ampleur publiee", "s2_points"),
                               ("S3 composite", "s3_composite")]:
                for metrique in ["distance", "ratio_entropie"]:
                    u = sc.loc[dd.index, col].values
                    v = dd[metrique].values
                    r, bas, haut, n = C.bootstrap_correlation(u, v, 2000, rng)
                    lignes_c.append({
                        "perimetre": nom_per, "condition": cond, "score": nom_s,
                        "metrique": metrique, "rho_spearman": r,
                        "ic_items_bas": bas, "ic_items_haut": haut, "n_items": n,
                    })
    continu = pd.DataFrame(lignes_c)

    # p bilateral par permutation des items pour H3, score S1, metrique distance
    for i, r in continu.iterrows():
        if not (r.score == "S1 NORC ordinal" and r.metrique == "distance"):
            continue
        d = par_item[r.perimetre]
        dd = d[d.condition == r.condition].set_index("item")
        u = scores.set_index("item").loc[dd.index, "s1_norc"].values
        v = dd["distance"].values
        ok = ~np.isnan(u) & ~np.isnan(v)
        u, v = u[ok], v[ok]
        obs, _ = C.spearman(u, v)
        tir = np.empty(min(args.tirages, 20000))
        for t in range(len(tir)):
            tir[t], _ = C.spearman(u, rng.permutation(v))
        continu.loc[i, "p_permutation"] = ((np.abs(tir) >= abs(obs) - 1e-12).sum() + 1.0) \
            / (len(tir) + 1.0)

    # ------------------------------------------------- (a) corrections
    famille = []
    for _, r in contrastes[(contrastes.perimetre == "150")
                           & (contrastes.condition != "humains vague 2")
                           & (contrastes.hypothese.str.startswith("H"))].iterrows():
        famille.append({"hypothese": r.hypothese, "condition": r.condition,
                        "p": r.p_permutation, "statistique": r.difference})
    for _, r in continu[(continu.perimetre == "150")
                        & (continu.condition != "humains vague 2")
                        & (continu.score == "S1 NORC ordinal")
                        & (continu.metrique == "distance")].iterrows():
        famille.append({"hypothese": "H3 continu", "condition": r.condition,
                        "p": r.p_permutation, "statistique": r.rho_spearman})
    fam = pd.DataFrame(famille)
    fam = fam[fam.p.notna()].reset_index(drop=True)
    fam["p_holm_famille_complete"] = C.holm(fam.p.values)
    fam["p_bh_famille_complete"] = C.benjamini_hochberg(fam.p.values)
    fam["p_holm_sous_famille"] = np.nan
    fam["p_bh_sous_famille"] = np.nan
    for h, idx in fam.groupby("hypothese").groups.items():
        idx = list(idx)
        fam.loc[idx, "p_holm_sous_famille"] = C.holm(fam.loc[idx, "p"].values)
        fam.loc[idx, "p_bh_sous_famille"] = C.benjamini_hochberg(fam.loc[idx, "p"].values)
    C.ecrire(fam, "a28-t1-corrections.csv")

    contrastes = contrastes.merge(
        fam.rename(columns={"p": "p_verif"})[
            ["hypothese", "condition", "p_holm_famille_complete",
             "p_bh_famille_complete", "p_holm_sous_famille", "p_bh_sous_famille"]],
        on=["hypothese", "condition"], how="left")
    C.ecrire(contrastes, "a28-t1-contrastes.csv")
    C.ecrire(continu, "a28-t1-continu.csv")

    # ------------------------------------------------- contraste de groupe, post hoc
    #
    # Ce contraste n'est PAS dans la famille declaree en tete de ce script. Il est ajoute
    # apres coup, parce que la revendication de a25 ne portait pas sur une condition mais
    # sur un motif : les huit conditions a modele de langage d'un cote, les baselines
    # statistiques de l'autre. Tester ce motif directement demande une permutation des
    # etiquettes de METHODE et non des etiquettes d'item. Il est rapporte comme un
    # resultat exploratoire, et la correction pour tests multiples ne s'y applique pas.
    lignes_g = []
    for hyp, source, col in [("H1 distance", contrastes, "difference"),
                             ("H2 dispersion", contrastes, "difference"),
                             ("H4 desirabilite", contrastes, "difference")]:
        s = source[(source.perimetre == "150") & (source.hypothese == hyp)]
        a = s[s.condition.isin(C.LLM)][col].values
        b = s[s.condition.isin(C.STAT)][col].values
        obs, p = C.permutation(a, b, args.tirages, rng)
        lignes_g.append({"quantite": hyp, "moyenne_llm": float(np.nanmean(a)),
                         "moyenne_statistique": float(np.nanmean(b)),
                         "difference": obs, "p_permutation_methodes": p,
                         "n_llm": len(a), "n_stat": len(b)})
    for nom_s in ["S1 NORC ordinal", "S2 ampleur publiee", "S3 composite"]:
        s = continu[(continu.perimetre == "150") & (continu.metrique == "distance")
                    & (continu.score == nom_s)]
        a = s[s.condition.isin(C.LLM)].rho_spearman.values
        b = s[s.condition.isin(C.STAT)].rho_spearman.values
        obs, p = C.permutation(a, b, args.tirages, rng)
        lignes_g.append({"quantite": f"H3 continu, {nom_s}",
                         "moyenne_llm": float(np.nanmean(a)),
                         "moyenne_statistique": float(np.nanmean(b)),
                         "difference": obs, "p_permutation_methodes": p,
                         "n_llm": len(a), "n_stat": len(b)})
    groupes = pd.DataFrame(lignes_g)
    C.ecrire(groupes, "a28-t1-contraste-de-groupe.csv")
    print("\n" + "=" * 118)
    print("Contraste de groupe, post hoc : huit conditions a modele de langage contre "
          "cinq predicteurs statistiques")
    print("=" * 118)
    print(groupes.to_string(index=False))

    # ------------------------------------------------- (c) robustesse au retrait
    lignes_r = []
    d150 = par_item["150"]
    retraits = [("aucun", [])] + [(it, [it]) for it in QUATRE_NOMINAUX] \
        + [("les quatre nominaux", QUATRE_NOMINAUX)] \
        + [(it, [it]) for it in sorted(
            d150.loc[d150.classe_norc == "sensible", "item"].unique())
           if it not in QUATRE_NOMINAUX]
    for nom_r, retire in retraits:
        for cond, dd in d150.groupby("condition"):
            dd = dd[~dd.item.isin(retire)]
            for metrique in ["distance", "ratio_entropie"]:
                r = contraste(dd, metrique, "sensible", "temoin", 10000, rng)
                lignes_r.append({"retrait": nom_r, "condition": cond,
                                 "metrique": metrique, **r})
    robustesse = pd.DataFrame(lignes_r)
    C.ecrire(robustesse, "a28-t1-robustesse.csv")

    # ------------------------------------------------- (d) stratification par type
    lignes_s = []
    for cond, dd in d150.groupby("condition"):
        for t in sorted(dd.type.unique()):
            ds = dd[dd.type == t]
            for metrique in ["distance", "ratio_entropie"]:
                r = contraste(ds, metrique, "sensible", "temoin", 10000, rng)
                lignes_s.append({"condition": cond, "type": t, "metrique": metrique, **r})
    strates = pd.DataFrame(lignes_s)
    C.ecrire(strates, "a28-t1-strates.csv")

    # ------------------------------------------------------------------ affichage
    pd.set_option("display.width", 240)
    for hyp, metrique in [("H1 distance", "distance"),
                          ("H2 dispersion", "ratio_entropie"),
                          ("H4 desirabilite", "ecart_desirabilite")]:
        print("\n" + "=" * 118)
        print(f"{hyp}, perimetre 150, sensible moins temoin")
        print("=" * 118)
        s = contrastes[(contrastes.perimetre == "150")
                       & (contrastes.hypothese == hyp)].copy()
        s["ordre"] = s.condition.map({c: i for i, c in enumerate(C.ORDRE_METHODES)})
        print(s.sort_values("ordre")[
            ["condition", "moyenne_groupe", "moyenne_temoin", "difference",
             "ic_items_bas", "ic_items_haut", "p_permutation",
             "p_holm_sous_famille", "p_bh_sous_famille",
             "p_holm_famille_complete", "p_bh_famille_complete"]].to_string(index=False))

    print("\n" + "=" * 118)
    print("H3, version continue, perimetre 150, correlation de rang score x distance")
    print("=" * 118)
    s = continu[(continu.perimetre == "150") & (continu.metrique == "distance")].copy()
    s["ordre"] = s.condition.map({c: i for i, c in enumerate(C.ORDRE_METHODES)})
    print(s.sort_values(["score", "ordre"])[
        ["score", "condition", "rho_spearman", "ic_items_bas", "ic_items_haut",
         "n_items", "p_permutation"]].to_string(index=False))

    print("\n" + "=" * 118)
    print("Robustesse : contraste de distance apres retrait d'items sensibles")
    print("=" * 118)
    piv = robustesse[robustesse.metrique == "distance"].pivot(
        index="condition", columns="retrait", values="difference")
    cols = ["aucun"] + QUATRE_NOMINAUX + ["les quatre nominaux"]
    piv = piv[[c for c in cols if c in piv.columns]]
    piv = piv.reindex([c for c in C.ORDRE_METHODES if c in piv.index])
    print(piv.round(4).to_string())

    print("\n" + "=" * 118)
    print("Stratification par type d'item, contraste de distance")
    print("=" * 118)
    piv = strates[strates.metrique == "distance"].pivot(
        index="condition", columns="type", values="difference")
    piv = piv.reindex([c for c in C.ORDRE_METHODES if c in piv.index])
    print(piv.round(4).to_string())
    piv2 = strates[strates.metrique == "distance"].pivot(
        index="condition", columns="type", values="n_groupe")
    print("\nnombre d'items sensibles par strate :")
    print(piv2.reindex([c for c in C.ORDRE_METHODES if c in piv2.index]).to_string())


if __name__ == "__main__":
    main()
