"""
a35_imputation : le modele de langage place parmi les methodes d'imputation, sur les
memes cellules, avec le tableau a quatre cases.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a2_commun, a2_baselines_gss, a8_commun,
a8_copule, a25_commun, a25_mesures, a28_commun, a29_commun, a31_commun et a31_mecanismes
sont importes tels quels, memes graines, memes plis, memes 149 items, memes personnes.

La question, formulee par la lecture complete du corpus (theme 02 section D.5, theme 03
section (b) et (d)) : la double distorsion n'est pas une propriete des modeles de langage,
c'est un theoreme d'imputation. Van Buuren l'ecrit en deux phrases, "regression imputation
artificially strengthens the relations in the data" et "regression imputation is a recipe
for false positive and spurious relations", et il donne le correctif, la regression
STOCHASTIQUE, qui "preserves not only the regression weights, but also the correlation
between variables", parce qu'elle TIRE au lieu de predire. La these du projet devient donc
une these de POSITION : ou se place un agent de langage entre les methodes d'esperance,
qui gagnent en exactitude et ecrasent la dispersion, et les methodes de tirage, qui
preservent la dispersion et perdent en exactitude ?

===========================================================================
LA FAMILLE D'HYPOTHESES, FIXEE AVANT LES RESULTATS
===========================================================================
Perimetre declare : les 1 052 personnes et les 149 items de a2, decoupage identique, cinq
plis sur les personnes et cinq blocs d'items, chaque couple (personne, item) predit
exactement une fois, contexte = les 119 autres items et les 11 attributs demographiques.
Pour C2 et C3, qui n'existent que sur 150 personnes, le perimetre naturel est ces 150
personnes, et toutes les methodes auxquelles elles sont comparees y sont restreintes.
Mesure de dispersion declaree : indice de Gini Simpson, estimateur sans biais de a1,
segmentation principale l'ideologie politique, segmentation secondaire le profil croise
genre x race x bloc d'ideologie. Seuil de minorite declare : 10 pour cent.

  H1  PRIMAIRE, le theoreme d'imputation sur nos cellules. Pour chacun des quatre couples
      "meme modele, deux regimes" (marginale, regression sur demographies, regression sur
      contexte, hot deck k = 30) et chacune des trois quantites (exactitude, ratio intra,
      ratio inter), la valeur en mode TIRAGE DIFFERE de la valeur en mode ARGMAX.
      Bilateral, 12 tests.
      Signes attendus, ecrits avant execution d'apres van Buuren : exactitude PLUS BASSE
      en tirage, ratio intra PLUS HAUT en tirage, ratio inter PLUS BAS en tirage. Un signe
      inverse est un resultat CONTRE la prediction et il est signale comme tel. Le cas de
      la marginale est declare a part : elle ne conditionne sur rien, son terme inter est
      nul dans les deux regimes, et la prediction sur le ratio inter n'a pas de sens pour
      elle. Le test est quand meme execute et compte dans la famille.

  H2  SECONDAIRE, la position du modele de langage. Pour chacune des huit conditions a
      modele de langage, deux tests : (a) son ratio intra DIFFERE de celui de
      `E1 regression contexte argmax`, l'imputation par esperance de reference ; (b) son
      ratio intra DIFFERE de celui de `E2 regression contexte tirage`, l'imputation par
      tirage de reference. Bilateral, 16 tests.
      Signes attendus si la these de position tient : ratio intra SUPERIEUR a celui de E1
      et INFERIEUR a celui de E2, c'est a dire strictement entre les deux.

  Famille primaire declaree : H1, 12 tests. Famille secondaire declaree : H2, 16 tests.
  Correction principale sur chaque famille : Holm, valide sans hypothese sur la dependance,
  ce qui est necessaire puisque tous les contrastes portent sur les memes personnes et les
  memes items. Correction secondaire rapportee a cote : Benjamini Hochberg.
  Tous les p sont des p de bootstrap APPARIE SUR LES PERSONNES, lus sur la position de
  zero dans la distribution ; ils ne descendent jamais sous 1 / nombre de tirages.

  N'ENTRENT DANS AUCUNE FAMILLE, et sont rapportes comme des descriptions : la copule
  gaussienne et son couple de regimes, qui ne portent que sur 70 items ordinaux et n'ont
  donc pas le meme denominateur ; le ratio de dispersion totale ; la diversite conservee
  et l'accord par paires ; le rappel, la precision et le F1 minoritaires ; le rapport
  groupe sur personne de a31 ; les regles de Rubin sur les marginales ; le front de Pareto ;
  la segmentation par profil croise ; le perimetre 150 pour les methodes qui disposent du
  perimetre 1 052 ; les contrastes descriptifs entre la meilleure condition a modele de
  langage et les methodes d'imputation voisines du front, ajoutes APRES avoir lu le front
  et signales comme tels partout ou ils apparaissent ; et la comparaison des methodes qui
  ne recoivent pas le meme conditionnement, qui est signalee partout ou elle apparait.
===========================================================================

Entree  : paquet OSF t6g7k, data/traces/a5-*.jsonl, cache de matrices de a25 et cache de
          la foret aleatoire de a28.
Sortie  : resultats/a35-tableau-quatre-cases.csv, a35-couples-regime.csv,
          a35-position-llm.csv, a35-ordinaux-copule.csv, a35-rubin-marginales.csv,
          a35-front-pareto.csv, a35-verification-dispersion.csv, a35-choix-penalite.csv,
          a35-groupe-sur-personne.csv, a35-contrastes-descriptifs.csv.

Usage :
  .venv/bin/python analyses/a35_imputation.py --cache /tmp/a25-matrices.pkl \
      --cache-foret /tmp/a28-foret.npy --tirages 1000 --tirages-dispersion 400
"""

import argparse
import os
import pickle
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
import a29_commun as C29
import a35_commun as C
from a2_baselines_gss import GRAINE, grille
from a2_commun import est_manquant
from a8_commun import modalites_minoritaires

GRILLE_PENALITE = [0.003, 0.01, 0.03, 0.1, 0.3, 1.0]


# ---------------------------------------------------------------------------

def construire(paquet, args):
    """Ajoute au dictionnaire de matrices les methodes d'imputation nouvelles."""
    y1, x = paquet["y1"], paquet["x"]
    n, m = y1.shape
    plis, blocs = grille(n, m, GRAINE)

    if args.cache_a35 and os.path.exists(args.cache_a35):
        neuf = pickle.load(open(args.cache_a35, "rb"))
        print(f"methodes nouvelles relues du cache {args.cache_a35}")
    else:
        t0 = time.time()
        force, detail = C.choisir_force(y1, x, plis, blocs, GRILLE_PENALITE)
        print(f"penalite retenue par validation interne au pli d'entrainement : C = {force}")
        for c, v in detail.items():
            print(f"    C = {c:<6} exactitude interne {v:.4f}")
        neuf = C.imputations_regression(y1, x, plis, blocs, force)
        neuf.update(C.hot_deck(y1, plis, blocs))
        cop, cols_ord, items_ord = C.copule(paquet, plis)
        neuf.update(cop)
        neuf["_meta"] = {"force": force, "detail_force": detail,
                         "colonnes_ordinales": cols_ord, "items_ordinaux": items_ord}
        print(f"  construction terminee en {time.time() - t0:.0f} s")
        if args.cache_a35:
            pickle.dump(neuf, open(args.cache_a35, "wb"))

    meta = neuf.pop("_meta")
    im = neuf.pop("_im")
    for nom, mat in neuf.items():
        paquet["M"][nom] = mat
    return meta, im


def methodes_disponibles(paquet, nom_per, avec_copule=False):
    """Methodes a rapporter sur un perimetre, dans l'ordre d'affichage de a35.

    La copule est exclue par defaut : elle ne couvre que 70 des 149 items, ses cellules
    nominales sont vides, et la faire figurer dans un tableau a 149 items lui donnerait
    une exactitude et une dispersion calculees sur un autre denominateur. Elle n'apparait
    que dans le tableau restreint aux 70 items ordinaux.
    """
    toutes = [c for c in C.ORDRE if c in paquet["M"]]
    if not avec_copule:
        toutes = [c for c in toutes if not c.startswith("copule")]
    if nom_per == "1052":
        return [c for c in toutes if c not in ("C2", "C3")]
    return toutes


# ---------------------------------------------------------------------------
# Le tableau a quatre cases
# ---------------------------------------------------------------------------

def tableau(paquet, lignes, nom_per, colonnes, mods, codes, seg_axes, k_items,
            idx_boot, ref_humain, groupe_personne):
    """Une ligne par methode : exactitude, ratios, diversite, minorites."""
    y1 = paquet["y1"]
    out = []
    for nom in methodes_disponibles(paquet, nom_per):
        pred = paquet["M"][nom]
        acc = C.exactitude(pred, y1, lignes, colonnes)
        with np.errstate(invalid="ignore"):
            tir = np.nanmean(acc[idx_boot], axis=1)
        moy, bas, haut = (np.nanmean(acc), *np.percentile(tir, [2.5, 97.5]))
        div = C.diversite(pred, y1, lignes, colonnes)
        _, mn = C.minorites(pred, y1, mods, lignes, colonnes)
        ligne = {
            "perimetre": nom_per, "methode": nom, "famille": C.FAMILLE[nom],
            "regime": C.REGIME[nom], "conditionnement": C.CONDITIONNEMENT[nom],
            "exactitude": float(moy), "ic_bas": float(bas), "ic_haut": float(haut),
            "exactitude_normalisee": float(moy) / ref_humain if ref_humain else np.nan,
            "part_diversite_humaine": div["part_diversite_humaine"],
            "accord_par_paires": div["accord_par_paires"],
            "rappel_minoritaire": mn["rappel"], "precision_minoritaire": mn["precision"],
            "f1_minoritaire": mn["f1"], "masse_predite": mn["masse_predite"],
            "rapport_groupe_sur_personne": groupe_personne.get((nom_per, nom), np.nan),
        }
        for axe in (C.AXE_PRINCIPAL, C.AXE_SECONDAIRE):
            s = C.sommes_dispersion(codes[nom][lignes], seg_axes[axe][lignes],
                                    k_items, colonnes)
            h = C.sommes_dispersion(codes["_humains"][lignes], seg_axes[axe][lignes],
                                    k_items, colonnes)
            suf = "ideologie" if axe == C.AXE_PRINCIPAL else "profil"
            ligne[f"ratio_intra_{suf}"] = s["intra"] / h["intra"] if h["intra"] else np.nan
            ligne[f"ratio_inter_{suf}"] = s["inter"] / h["inter"] if h["inter"] else np.nan
            ligne[f"ratio_total_{suf}"] = s["total"] / h["total"] if h["total"] else np.nan
            ligne[f"n_items_dispersion_{suf}"] = s["n_items"]
        out.append(ligne)
        print(f"    {nom:<34} exactitude {ligne['exactitude']:.4f} "
              f"intra {ligne['ratio_intra_ideologie']:.3f} "
              f"inter {ligne['ratio_inter_ideologie']:.3f}", flush=True)
    return pd.DataFrame(out)


def bootstrap_quantites(paquet, lignes, colonnes, codes, seg, k_max, idx_disp,
                        methodes):
    """Distributions bootstrap des trois quantites testees, tirages partages.

    Pour chaque tirage de personnes, l'exactitude, le ratio intra et le ratio inter sont
    recalcules pour toutes les methodes sur le MEME tirage. C'est ce qui rend les
    contrastes apparies : la difference entre deux methodes ne porte plus la variance de
    l'echantillon de personnes, seulement celle de l'ecart.
    """
    y1 = paquet["y1"]
    acc = {}
    for nom in methodes:
        acc[nom] = C.exactitude(paquet["M"][nom], y1, lignes, colonnes)
    ch = codes["_humains"][lignes]
    cm = {nom: codes[nom][lignes] for nom in methodes}
    sg = seg[lignes]

    dist = {nom: {"exactitude": np.empty(len(idx_disp)),
                  "intra": np.empty(len(idx_disp)),
                  "inter": np.empty(len(idx_disp))} for nom in methodes}
    for t, idx in enumerate(idx_disp):
        h = C.sommes_dispersion_rapide(ch[idx], sg[idx], k_max, colonnes)
        for nom in methodes:
            s = C.sommes_dispersion_rapide(cm[nom][idx], sg[idx], k_max, colonnes)
            d = dist[nom]
            d["exactitude"][t] = np.nanmean(acc[nom][idx])
            d["intra"][t] = s["intra"] / h["intra"] if h["intra"] else np.nan
            d["inter"][t] = s["inter"] / h["inter"] if h["inter"] else np.nan
        if (t + 1) % 100 == 0:
            print(f"    bootstrap dispersion {t + 1}/{len(idx_disp)}", flush=True)
    return dist


def contraste(dist, a, b, cle):
    """Difference a moins b d'une quantite, son intervalle et son p bilateral."""
    d = dist[a][cle] - dist[b][cle]
    d = d[~np.isnan(d)]
    if len(d) == 0:
        return np.nan, np.nan, np.nan, 1.0
    return (float(d.mean()), float(np.percentile(d, 2.5)),
            float(np.percentile(d, 97.5)), C.p_bilateral(d))


# ---------------------------------------------------------------------------
# Regles de Rubin sur les marginales
# ---------------------------------------------------------------------------

def rubin(paquet, im, lignes, colonnes, single):
    """Couverture de la marginale humaine par trois protocoles d'imputation.

    L'estimand est, pour chaque item et chaque modalite, la proportion de la population
    qui la choisit. Trois estimateurs sont compares.

      esperance   : une seule imputation, la modalite la plus probable. L'intervalle est
                    l'intervalle binomial usuel, celui qu'un analyste calculerait sur un
                    fichier complete sans se demander d'ou vient le remplissage.
      tirage      : une seule imputation stochastique, meme intervalle binomial.
      Rubin m = 10: m imputations stochastiques, mise en commun par les regles de Rubin,
                    Q barre = moyenne des estimations, T = W barre + (1 + 1/m) B, degres
                    de liberte de Rubin 1987.

    La quantite lue est la COUVERTURE : la part des couples (item, modalite) dont
    l'intervalle contient la vraie proportion humaine. Une couverture nominale vaut 95
    pour cent. C'est la mesure qui dit si un fichier complete est utilisable pour une
    inference, et c'est celle qu'un institut d'etudes comprend.
    """
    from scipy import stats

    y1 = paquet["y1"]
    n = len(lignes)
    m_im = len(im)
    out = []
    for j in colonnes:
        vrai = [C28.norm(v) for v in y1[lignes, j] if not est_manquant(v)]
        if len(vrai) < 30:
            continue
        mods = sorted(set(vrai))
        p_vrai = {mo: vrai.count(mo) / len(vrai) for mo in mods}
        # proportions par imputation
        parts = np.zeros((m_im, len(mods)))
        for t in range(m_im):
            col = [C28.norm(v) for v in im[t][lignes, j] if not est_manquant(v)]
            if not col:
                continue
            for a, mo in enumerate(mods):
                parts[t, a] = col.count(mo) / len(col)
        for nom, mat in single.items():
            col = [C28.norm(v) for v in mat[lignes, j] if not est_manquant(v)]
            if not col:
                continue
            for a, mo in enumerate(mods):
                q = col.count(mo) / len(col)
                se = np.sqrt(max(q * (1 - q), 1e-12) / n)
                lo, hi = q - 1.96 * se, q + 1.96 * se
                out.append({"protocole": nom, "item": paquet["items"][j],
                            "modalite": mo, "p_humain": p_vrai[mo], "estimation": q,
                            "demi_largeur": 1.96 * se,
                            "couvre": bool(lo <= p_vrai[mo] <= hi)})
        for a, mo in enumerate(mods):
            q = parts[:, a]
            qbar = float(q.mean())
            w = float(np.mean(q * (1 - q) / n))
            b = float(q.var(ddof=1)) if m_im > 1 else 0.0
            T = w + (1 + 1 / m_im) * b
            if b > 0:
                r = (1 + 1 / m_im) * b / max(w, 1e-15)
                df = (m_im - 1) * (1 + 1 / r) ** 2
            else:
                df = 1e6
            crit = float(stats.t.ppf(0.975, max(df, 1.0)))
            demi = crit * np.sqrt(max(T, 0.0))
            out.append({"protocole": f"Rubin m={m_im}", "item": paquet["items"][j],
                        "modalite": mo, "p_humain": p_vrai[mo], "estimation": qbar,
                        "demi_largeur": demi,
                        "couvre": bool(abs(qbar - p_vrai[mo]) <= demi)})
    return pd.DataFrame(out)


# ---------------------------------------------------------------------------
# Rapport groupe sur personne, machinerie de a31 rejouee sur les methodes nouvelles
# ---------------------------------------------------------------------------

def groupe_sur_personne(paquet, per, seg_tous):
    """lift segment sur lift personne, definition de a31, pour toutes les methodes.

    a31 mesure, chez les FAUSSES raretes d'une methode, deux exces : celui du taux de
    raretes reelles de la PERSONNE hors de l'item, et celui du taux de raretes reelles de
    son SEGMENT sur l'item. Chacun est rapporte a son propre temoin aveugle a la personne.
    Le rapport des deux exces relatifs dit si la methode pose ses fausses raretes la ou la
    personne est effectivement souvent rare, ou la ou son groupe l'est. Rien n'est
    recopie : covariables et masques viennent de a31_mecanismes, les agregateurs de
    a31_commun.
    """
    import a31_commun as C31
    import a31_mecanismes as M31

    out = {}
    for nom_per, lignes in per.items():
        cv = M31.covariables(paquet, lignes, C.SEUIL_MINORITE, seg_tous)
        for nom in methodes_disponibles(paquet, nom_per):
            m = M31.masques_condition(paquet, lignes, nom, cv)
            if m["faux_maj"].sum() < 20:
                out[(nom_per, nom)] = np.nan
                continue
            lifts = {}
            for cle, mat in (("personne", cv["r_personne"]),
                             ("segment", cv["r_segment"][C.AXE_PRINCIPAL])):
                num, den = C31.moyenne_par_personne(m["faux_maj"], mat)
                v = C31.taux(num, den)
                tem = C31.temoin_item(m["faux_maj"], cv["ok"], mat)
                lifts[cle] = (v / tem - 1.0) if tem and np.isfinite(v) else np.nan
            lp, ls = lifts["personne"], lifts["segment"]
            out[(nom_per, nom)] = ls / lp if (np.isfinite(lp) and lp > 0) else np.nan
    return out


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", default="/tmp/a25-matrices.pkl")
    ap.add_argument("--cache-foret", default="/tmp/a28-foret.npy")
    ap.add_argument("--cache-a35", default="/tmp/a35-methodes.pkl")
    ap.add_argument("--tirages", type=int, default=1000)
    ap.add_argument("--tirages-dispersion", type=int, default=400)
    ap.add_argument("--graine", type=int, default=C.GRAINE_A35)
    args = ap.parse_args()

    t_debut = time.time()
    print(__doc__.split("=" * 75)[1])

    paquet = C.charger_paquet(args.cache, args.cache_foret)
    meta, im = construire(paquet, args)
    items, options = paquet["items"], paquet["options"]
    y1 = paquet["y1"]
    n, m = y1.shape
    colonnes = list(range(m))
    cols_ord = meta["colonnes_ordinales"]

    seg_tous, _ = C28.segments(paquet["x"], paquet["attributs"])
    k_items = [len(options[it]) for it in items]
    k_max = max(k_items)
    print("\ncodage des matrices sur la nomenclature de question_master")
    codes = {"_humains": C28.coder(y1, np.arange(n), items, options)}
    for nom in [c for c in C.ORDRE if c in paquet["M"]]:
        codes[nom] = C28.coder(paquet["M"][nom], np.arange(n), items, options)

    # ---- verification de la version vectorisee contre la version de reference
    ver = []
    for axe in (C.AXE_PRINCIPAL, C.AXE_SECONDAIRE):
        for nom in ("_humains", "E1 regression contexte argmax",
                    "E2 regression contexte tirage", "agents composite"):
            a = C.sommes_dispersion(codes[nom], seg_tous[axe], k_items, colonnes)
            b = C.sommes_dispersion_rapide(codes[nom], seg_tous[axe], k_max, colonnes)
            ver.append({"axe": axe, "matrice": nom, "n_items_reference": a["n_items"],
                        "n_items_vectorise": b["n_items"],
                        "ecart_total": abs(a["total"] - b["total"]),
                        "ecart_intra": abs(a["intra"] - b["intra"]),
                        "ecart_inter": abs(a["inter"] - b["inter"])})
    ver = pd.DataFrame(ver)
    C.ecrire(ver, "a35-verification-dispersion.csv")
    print(f"ecart maximal entre les deux implementations : "
          f"{ver[['ecart_total', 'ecart_intra', 'ecart_inter']].values.max():.2e}")

    C.ecrire(pd.DataFrame([{"penalite": c, "exactitude_interne": v}
                           for c, v in meta["detail_force"].items()]),
             "a35-choix-penalite.csv")

    per = {"1052": np.arange(n), "150": np.asarray(paquet["lignes150"])}
    rng = np.random.default_rng(args.graine)

    print("\nrapport groupe sur personne, machinerie de a31")
    gsp = groupe_sur_personne(paquet, per, seg_tous)

    tables, dists, idx_par_perimetre = [], {}, {}
    for nom_per, lignes in per.items():
        print(f"\ntableau a quatre cases, perimetre {nom_per}")
        idx_boot = C.tirages(len(lignes), args.tirages, rng)
        idx_disp = idx_boot[: args.tirages_dispersion]
        acc_h = C.exactitude(paquet["M"]["humains vague 2"], y1, lignes, colonnes)
        ref = float(np.nanmean(acc_h))
        mods_per = modalites_minoritaires(y1[lignes], C.SEUIL_MINORITE)
        t = tableau(paquet, lignes, nom_per, colonnes, mods_per, codes, seg_tous,
                    k_items, idx_boot, ref, gsp)
        tables.append(t)
        idx_par_perimetre[nom_per] = idx_disp
        print(f"  bootstrap sur {args.tirages_dispersion} tirages, axe ideologie")
        dists[nom_per] = bootstrap_quantites(
            paquet, lignes, colonnes, codes, seg_tous[C.AXE_PRINCIPAL], k_max,
            idx_disp, methodes_disponibles(paquet, nom_per))
    tab = pd.concat(tables, ignore_index=True)
    C.ecrire(tab, "a35-tableau-quatre-cases.csv")

    # ---- H1, le theoreme d'imputation
    print("\nH1, famille primaire : douze contrastes de regime")
    lignes_h1 = []
    attendu = {"exactitude": "tirage plus bas", "intra": "tirage plus haut",
               "inter": "tirage plus bas"}
    for libelle, arg, tir in C.COUPLES:
        for cle in ("exactitude", "intra", "inter"):
            d, b, h, p = contraste(dists["1052"], tir, arg, cle)
            lignes_h1.append({"famille": "H1 primaire", "couple": libelle,
                              "quantite": cle, "argmax": arg, "tirage": tir,
                              "difference_tirage_moins_argmax": d, "ic_bas": b,
                              "ic_haut": h, "p_bootstrap": p,
                              "signe_attendu": attendu[cle],
                              "signe_observe": ("tirage plus haut" if d > 0
                                                else "tirage plus bas"),
                              "conforme": bool((d > 0) == (cle == "intra"))})
    h1 = pd.DataFrame(lignes_h1)
    h1["p_holm"] = C.holm(h1.p_bootstrap.values)
    h1["p_bh"] = C.benjamini_hochberg(h1.p_bootstrap.values)

    # ---- couple de la copule, hors famille, 70 items ordinaux
    print("hors famille : le couple de la copule, sur ses 70 items ordinaux")
    d_cop = bootstrap_quantites(paquet, per["1052"], cols_ord, codes,
                                seg_tous[C.AXE_PRINCIPAL], k_max,
                                idx_par_perimetre["1052"],
                                [C.COUPLE_COPULE[1], C.COUPLE_COPULE[2]])
    for cle in ("exactitude", "intra", "inter"):
        d, b, h, p = contraste(d_cop, C.COUPLE_COPULE[2], C.COUPLE_COPULE[1], cle)
        lignes_h1.append({"famille": "hors famille, 70 items ordinaux",
                          "couple": C.COUPLE_COPULE[0], "quantite": cle,
                          "argmax": C.COUPLE_COPULE[1], "tirage": C.COUPLE_COPULE[2],
                          "difference_tirage_moins_argmax": d, "ic_bas": b,
                          "ic_haut": h, "p_bootstrap": p,
                          "signe_attendu": attendu[cle],
                          "signe_observe": ("tirage plus haut" if d > 0
                                            else "tirage plus bas"),
                          "conforme": bool((d > 0) == (cle == "intra")),
                          "p_holm": np.nan, "p_bh": np.nan})
    h1 = pd.concat([h1, pd.DataFrame(lignes_h1[-3:])], ignore_index=True)
    C.ecrire(h1, "a35-couples-regime.csv")

    # ---- H2, la position du modele de langage
    print("\nH2, famille secondaire : seize contrastes de position")
    lignes_h2 = []
    for cond in C.LLM:
        nom_per = "150" if cond in ("C2", "C3") else "1052"
        if cond not in dists[nom_per]:
            continue
        for ref_nom, sens in (("E1 regression contexte argmax", "au dessus de E1"),
                              ("E2 regression contexte tirage", "en dessous de E2")):
            d, b, h, p = contraste(dists[nom_per], cond, ref_nom, "intra")
            lignes_h2.append({"famille": "H2 secondaire", "condition": cond,
                              "perimetre": nom_per, "reference": ref_nom,
                              "difference_condition_moins_reference": d,
                              "ic_bas": b, "ic_haut": h, "p_bootstrap": p,
                              "signe_attendu": sens,
                              "conforme": bool((d > 0) == (ref_nom.startswith("E1")))})
    h2 = pd.DataFrame(lignes_h2)
    h2["p_holm"] = C.holm(h2.p_bootstrap.values)
    h2["p_bh"] = C.benjamini_hochberg(h2.p_bootstrap.values)
    C.ecrire(h2, "a35-position-llm.csv")

    # ---- contrastes descriptifs autour du front, hors famille
    print("\nhors famille : contrastes descriptifs autour du front de Pareto")
    desc = []
    for a, b in (("E1 regression contexte argmax", "agents composite"),
                 ("IM m=10 mode des m", "agents composite"),
                 ("PMM k=10", "agents composite"),
                 ("PMM k=10", "E1 regression contexte argmax"),
                 ("B2 argmax", "E1 regression contexte argmax")):
        for cle in ("exactitude", "intra", "inter"):
            d, lo, hi, p = contraste(dists["1052"], a, b, cle)
            desc.append({"famille": "hors famille, descriptif", "methode_a": a,
                         "methode_b": b, "quantite": cle,
                         "difference_a_moins_b": d, "ic_bas": lo, "ic_haut": hi,
                         "p_bootstrap": p})
    C.ecrire(pd.DataFrame(desc), "a35-contrastes-descriptifs.csv")

    # ---- sous ensemble ordinal, toutes les methodes sur les 70 items de la copule
    print("\nsous ensemble des 70 items ordinaux, toutes les methodes")
    ord_lignes = []
    acc_h = C.exactitude(paquet["M"]["humains vague 2"], y1, per["1052"], cols_ord)
    ref_ord = float(np.nanmean(acc_h))
    for nom in methodes_disponibles(paquet, "1052", avec_copule=True):
        pred = paquet["M"][nom]
        acc = C.exactitude(pred, y1, per["1052"], cols_ord)
        div = C.diversite(pred, y1, per["1052"], cols_ord)
        s = C.sommes_dispersion(codes[nom], seg_tous[C.AXE_PRINCIPAL], k_items, cols_ord)
        hh = C.sommes_dispersion(codes["_humains"], seg_tous[C.AXE_PRINCIPAL],
                                 k_items, cols_ord)
        ord_lignes.append({
            "methode": nom, "famille": C.FAMILLE[nom], "regime": C.REGIME[nom],
            "exactitude": float(np.nanmean(acc)),
            "exactitude_normalisee": float(np.nanmean(acc)) / ref_ord,
            "part_diversite_humaine": div["part_diversite_humaine"],
            "accord_par_paires": div["accord_par_paires"],
            "ratio_intra_ideologie": s["intra"] / hh["intra"] if hh["intra"] else np.nan,
            "ratio_inter_ideologie": s["inter"] / hh["inter"] if hh["inter"] else np.nan,
            "ratio_total_ideologie": s["total"] / hh["total"] if hh["total"] else np.nan})
    C.ecrire(pd.DataFrame(ord_lignes), "a35-ordinaux-copule.csv")

    # ---- regles de Rubin
    print("\nregles de Rubin sur les marginales")
    single = {"esperance (une imputation)": paquet["M"]["E1 regression contexte argmax"],
              "tirage (une imputation)": paquet["M"]["E2 regression contexte tirage"]}
    rb = rubin(paquet, im, per["1052"], colonnes, single)
    res = (rb.groupby("protocole")
             .agg(couples=("couvre", "size"), couverture=("couvre", "mean"),
                  demi_largeur_moyenne=("demi_largeur", "mean"),
                  biais_absolu_moyen=("estimation", lambda s: np.nan))
             .reset_index())
    rb["biais_absolu"] = (rb.estimation - rb.p_humain).abs()
    res["biais_absolu_moyen"] = [rb[rb.protocole == p].biais_absolu.mean()
                                 for p in res.protocole]
    C.ecrire(res, "a35-rubin-marginales.csv")
    print(res.to_string(index=False))

    # ---- front de Pareto
    print("\nfront de Pareto, exactitude et deux dimensions de structure")
    t10 = tab[tab.perimetre == "1052"].copy()
    t150 = tab[(tab.perimetre == "150") & (tab.methode.isin(["C2", "C3"]))].copy()
    pf = pd.concat([t10, t150], ignore_index=True)
    pf = pf[pf.methode != "humains vague 2"].copy()
    # Trois criteres a maximiser : l'exactitude, la proximite de 1 du ratio intra, la
    # proximite de 1 du ratio inter. Une methode est dominee si une autre fait au moins
    # aussi bien sur les trois et strictement mieux sur au moins un.
    pf["proximite_intra"] = -(pf.ratio_intra_ideologie - 1.0).abs()
    pf["proximite_inter"] = -(pf.ratio_inter_ideologie - 1.0).abs()
    crit = pf[["exactitude", "proximite_intra", "proximite_inter"]].values
    domine = np.zeros(len(pf), dtype=bool)
    for i in range(len(pf)):
        for j in range(len(pf)):
            if i == j:
                continue
            if np.all(crit[j] >= crit[i] - 1e-12) and np.any(crit[j] > crit[i] + 1e-12):
                domine[i] = True
                break
    pf["sur_le_front"] = ~domine
    C.ecrire(pf[["perimetre", "methode", "famille", "regime", "conditionnement",
                 "exactitude", "ratio_intra_ideologie", "ratio_inter_ideologie",
                 "proximite_intra", "proximite_inter", "sur_le_front"]],
             "a35-front-pareto.csv")
    print(pf[pf.sur_le_front][["methode", "regime", "exactitude",
                               "ratio_intra_ideologie",
                               "ratio_inter_ideologie"]].to_string(index=False))

    C.ecrire(pd.DataFrame([{"perimetre": k[0], "methode": k[1],
                            "rapport_groupe_sur_personne": v}
                           for k, v in gsp.items()]),
             "a35-groupe-sur-personne.csv")

    print(f"\nduree totale {time.time() - t_debut:.0f} s")


if __name__ == "__main__":
    main()
