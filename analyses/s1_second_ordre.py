"""
s1_second_ordre : la croyance de second ordre sur des OPINIONS, trois termes.

Statut : script d'analyse jetable. **Aucun appel de modele de langage.** Il lit des fichiers
deja presents sur le disque et rien d'autre. Aucun fichier existant du depot n'est modifie.

Question, fixee par resultats/s1-preenregistrement.md, horodate 2026-09-09 12:02:16 CEST :
quand un modele decrit ce que le public soutient, ressemble t il a la realite, a la
caricature du camp qu'il incarne, ou a celle du camp adverse ?

Les quatre termes, tous en points de pourcentage sur 0 a 100 :
  R(j)        realite      part des humains de la vague 4 favorables a l'enonce j (QID287 en
                           modalite 4 ou 5).
  H(j, c)     caricature   moyenne de QID290 vague 4 chez les humains du camp c.
  M(j, c, m)  modele       moyenne de QID290 chez les jumeaux du modele m dont la personne
                           source est du camp c.
  P(j, c)     plancher     ecart absolu moyen d'une meme personne du camp c entre sa
                           reponse QID290 de la vague 1 a 3 et celle de la vague 4.

Entree  : data/twin2k500/question_catalog_and_human_response_csv/{wave1_3,wave4}_response.csv
          data/twin2k500/question_catalog_and_human_response_csv/question_catalog.json
          data/twin2k500/llm_specs/*.csv, 13 configurations plus deux fichiers humains
Sortie  : resultats/s1-termes-humains.csv, s1-par-enonce.csv, s1-cellules.csv,
          s1-tests.csv, s1-amplification.csv, s1-controles.csv

Usage : .venv/bin/python analyses/s1_second_ordre.py
"""

import hashlib
import itertools
import json
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from a28_commun import holm
from a30_commun import TWIN_BLOC3, TWIN_PARTI3

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TWIN = os.path.join(RACINE, "data/twin2k500")
CSV = os.path.join(TWIN, "question_catalog_and_human_response_csv")
SPECS = os.path.join(TWIN, "llm_specs")
SORTIE = os.path.join(RACINE, "resultats")

GRAINE = 20260909
N_BOOT = 10000          # bootstrap sur les enonces
N_BOOT_PERS = 2000      # bootstrap de controle sur les personnes
BANDE = (0.95, 1.05)    # bande de non materialite
SEUIL_PARSE = 0.10      # critere de chute 1
EFFECTIF_MIN = 50       # critere de chute 4

# Les dix enonces. Suffixes de colonne du catalogue, dans l'ordre du questionnaire.
SUFFIXES = ["1", "2", "3", "4", "5", "6", "7", "10", "11", "12"]
# Colonnes de la mise en forme employee par les fichiers de simulation.
FMT_SELF = [f"False Cons. self _{i}" for i in range(1, 11)]
FMT_AUTRES = [f"False cons. others _{s}" for s in SUFFIXES]

OPPOSE = {"gauche": "droite", "droite": "gauche"}


# ---------------------------------------------------------------------------
# 1. Lecture
# ---------------------------------------------------------------------------

def empreinte(chemin):
    with open(chemin, "rb") as fh:
        return hashlib.md5(fh.read()).hexdigest()


def libelles_enonces():
    """Le texte des dix enonces, lu dans le catalogue, jamais retape."""
    with open(os.path.join(CSV, "question_catalog.json"), encoding="utf-8") as fh:
        cat = json.load(fh)
    q = {e["QuestionID"]: e for e in cat}
    stmts = dict(zip(q["QID290"]["StatementsID"], q["QID290"]["Statements"]))
    rows = dict(zip(q["QID287"]["RowsID"], q["QID287"]["Rows"]))
    return [stmts[s] for s in SUFFIXES], [rows[s] for s in SUFFIXES]


def lire_humains():
    """Les deux vagues humaines, avec les camps. Une ligne par personne."""
    c287 = [f"QID287_{s}" for s in SUFFIXES]
    c290 = [f"QID290_{s}" for s in SUFFIXES]
    w13 = pd.read_csv(os.path.join(CSV, "wave1_3_response.csv"),
                      usecols=["pid", "QID20", "QID22"] + c287 + c290, low_memory=False)
    w4 = pd.read_csv(os.path.join(CSV, "wave4_response.csv"),
                     usecols=["pid"] + c287 + c290, low_memory=False)
    w13 = w13.sort_values("pid").reset_index(drop=True)
    w4 = w4.sort_values("pid").reset_index(drop=True)
    if not (w13["pid"].to_numpy() == w4["pid"].to_numpy()).all():
        sys.exit("les deux vagues ne portent pas les memes identifiants")
    camps = {
        "ideologie": np.array([TWIN_BLOC3.get(v if v == v else None) for v in w13["QID22"]],
                              dtype=object),
        "parti": np.array([TWIN_PARTI3.get(v if v == v else None) for v in w13["QID20"]],
                          dtype=object),
    }
    return {
        "pid": w13["pid"].to_numpy(),
        "camps": camps,
        "soutien_w4": w4[c287].to_numpy(dtype=float),     # 1 a 5
        "second_w4": w4[c290].to_numpy(dtype=float),      # 0 a 100
        "second_w13": w13[c290].to_numpy(dtype=float),
        "soutien_w13": w13[c287].to_numpy(dtype=float),
    }


def lire_modeles():
    """Les configurations de simulation, dedupliquees par contenu.

    Deux pieges de nommage sont leves ici, comme annonce en section 3.2 de la page de plan :
    un fichier de `llm/` est en realite le fichier humain de la vague 4, et un autre est un
    doublon d'une configuration deja listee. On lit donc `llm_specs/`, dont les noms portent
    les libelles des auteurs, on ecarte les deux fichiers humains, et on verifie qu'aucun
    contenu ne se repete.
    """
    fichiers = sorted(f for f in os.listdir(SPECS) if f.endswith(".csv")
                      and not f.startswith("humains_"))
    vus, sorties = {}, []
    for nom in fichiers:
        chemin = os.path.join(SPECS, nom)
        h = empreinte(chemin)
        if h in vus:
            sorties.append({"configuration": nom[:-4], "doublon_de": vus[h], "md5": h})
            continue
        vus[h] = nom[:-4]
        d = pd.read_csv(chemin, low_memory=False, skiprows=[1])
        d = d[d["TWIN_ID"] != "TWIN_ID"].copy()
        d["pid"] = pd.to_numeric(d["TWIN_ID"], errors="coerce")
        d = d.dropna(subset=["pid"])
        autres = np.array(d[FMT_AUTRES].apply(pd.to_numeric, errors="coerce"),
                          dtype=float, copy=True)
        soi = np.array(d[FMT_SELF].apply(pd.to_numeric, errors="coerce"),
                       dtype=float, copy=True)
        autres[(autres < 0) | (autres > 100)] = np.nan
        soi[(soi < 1) | (soi > 5)] = np.nan
        sorties.append({
            "configuration": nom[:-4], "md5": h, "doublon_de": "",
            "pid": d["pid"].to_numpy(dtype=int), "autres": autres, "soi": soi,
        })
    return sorties


# ---------------------------------------------------------------------------
# 2. Statistiques
# ---------------------------------------------------------------------------

def ic_moyenne_items(v, rng, n=N_BOOT):
    """Moyenne sur les enonces et son intervalle de percentile, reechantillonnage d'enonces."""
    v = np.asarray(v, dtype=float)
    bon = np.isfinite(v)
    if bon.sum() < 2:
        return float("nan"), float("nan"), float("nan")
    v = v[bon]
    idx = rng.integers(0, len(v), size=(n, len(v)))
    tir = v[idx].mean(axis=1)
    return float(v.mean()), float(np.percentile(tir, 2.5)), float(np.percentile(tir, 97.5))


def ic_rapport_items(a, b, rng, n=N_BOOT):
    """Rapport des moyennes de deux series appariees par enonce, IC bootstrap sur enonces."""
    a, b = np.asarray(a, dtype=float), np.asarray(b, dtype=float)
    bon = np.isfinite(a) & np.isfinite(b)
    if bon.sum() < 2 or b[bon].mean() == 0:
        return float("nan"), float("nan"), float("nan")
    a, b = a[bon], b[bon]
    idx = rng.integers(0, len(a), size=(n, len(a)))
    den = b[idx].mean(axis=1)
    tir = np.where(den != 0, a[idx].mean(axis=1) / np.where(den == 0, 1.0, den), np.nan)
    return float(a.mean() / b.mean()), float(np.nanpercentile(tir, 2.5)), \
        float(np.nanpercentile(tir, 97.5))


def p_signe_exacte(d):
    """p bilaterale d'un test de signe apparie, par enumeration exacte des 2^J patrons.

    Avec dix enonces, 1 024 patrons : l'enumeration est exacte et la plus petite p
    atteignable vaut 2 / 1 024 = 0,00195. Le plan a donc de la puissance a son seuil de
    0,05, ce qui n'etait pas le cas des quatre items de a46.
    """
    d = np.asarray(d, dtype=float)
    d = d[np.isfinite(d)]
    J = len(d)
    if J < 2:
        return float("nan"), 0
    obs = abs(d.mean())
    signes = np.array(list(itertools.product([1.0, -1.0], repeat=J)))
    tir = np.abs((signes * d).mean(axis=1))
    return float((tir >= obs - 1e-12).mean()), J


def moyenne_camp(mat, masque):
    """Moyenne par enonce sur les lignes du masque, en ignorant les valeurs manquantes."""
    if masque.sum() == 0:
        return np.full(mat.shape[1], np.nan)
    with np.errstate(invalid="ignore"):
        return np.nanmean(mat[masque], axis=0)


# ---------------------------------------------------------------------------
# 3. Calcul
# ---------------------------------------------------------------------------

def main():
    rng = np.random.default_rng(GRAINE)
    os.makedirs(SORTIE, exist_ok=True)
    stmts, rows = libelles_enonces()
    hum = lire_humains()
    modeles = lire_modeles()
    controles = []

    # --- termes humains, ancrage par ancrage -------------------------------
    reel = (np.isin(hum["soutien_w4"], (4.0, 5.0)).mean(axis=0) * 100.0)
    reel_large = (np.isin(hum["soutien_w4"], (3.0, 4.0, 5.0)).mean(axis=0) * 100.0)
    ecart_retest = np.abs(hum["second_w13"] - hum["second_w4"])

    termes, H, P = [], {}, {}
    for ancrage, lab in hum["camps"].items():
        for camp in ("gauche", "centre", "droite"):
            m = (lab == camp)
            H[(ancrage, camp)] = moyenne_camp(hum["second_w4"], m)
            P[(ancrage, camp)] = moyenne_camp(ecart_retest, m)
            for j, s in enumerate(SUFFIXES):
                termes.append({
                    "ancrage": ancrage, "camp": camp, "enonce": s, "libelle": stmts[j],
                    "n_personnes": int(m.sum()),
                    "reel_soutien_4ou5": reel[j], "reel_soutien_3a5": reel_large[j],
                    "croyance_humaine": H[(ancrage, camp)][j],
                    "plancher_retest": P[(ancrage, camp)][j],
                    "reel_du_camp_4ou5": float(
                        np.isin(hum["soutien_w4"][m], (4.0, 5.0)).mean() * 100.0)
                    if m.sum() else float("nan"),
                })
    pd.DataFrame(termes).to_csv(os.path.join(SORTIE, "s1-termes-humains.csv"),
                                index=False)

    # ecart de perception humain entre camps, par ancrage
    ecart_h = {}
    for ancrage in hum["camps"]:
        ecart_h[ancrage] = H[(ancrage, "gauche")] - H[(ancrage, "droite")]

    # critere de chute 5 : le plancher ecrase t il l'ecart entre camps ?
    for ancrage in hum["camps"]:
        pl = np.nanmean([P[(ancrage, "gauche")], P[(ancrage, "droite")]])
        eg = float(np.nanmean(np.abs(ecart_h[ancrage])))
        controles.append({"bloc": "critere de chute 5", "ancrage": ancrage,
                          "plancher_moyen": pl, "ecart_humain_moyen": eg,
                          "resolution": "oui" if eg > pl else "non"})

    # --- cellules modele x camp -------------------------------------------
    lignes_cell, lignes_item, tests, ampli = [], [], [], []
    for mod in modeles:
        nom = mod["configuration"]
        if mod.get("doublon_de"):
            controles.append({"bloc": "doublon", "configuration": nom,
                              "doublon_de": mod["doublon_de"], "md5": mod["md5"]})
            continue
        autres, soi = mod["autres"], mod["soi"]
        taux = float(np.isnan(autres).mean())
        chute = taux > SEUIL_PARSE
        controles.append({"bloc": "parse", "configuration": nom, "n_lignes": len(mod["pid"]),
                          "taux_non_parse": taux,
                          "chute_critere_1": "oui" if chute else "non"})
        if chute:
            continue
        # alignement des camps sur la personne source
        pos = pd.Series(np.arange(len(hum["pid"])), index=hum["pid"])
        idx = pos.reindex(mod["pid"]).to_numpy()
        ok = np.isfinite(idx)
        idx_ok = idx[ok].astype(int)
        for ancrage, lab in hum["camps"].items():
            lab_mod = lab[idx_ok]
            A = autres[ok]
            S = soi[ok]
            M = {}
            for camp in ("gauche", "centre", "droite"):
                m = (lab_mod == camp)
                M[camp] = moyenne_camp(A, m)
                n_c = int(m.sum())
                if n_c == 0:
                    continue
                d_reel = np.abs(M[camp] - reel)
                d_endo = np.abs(M[camp] - H[(ancrage, camp)])
                oppose = OPPOSE.get(camp)
                d_exo = (np.abs(M[camp] - H[(ancrage, oppose)]) if oppose
                         else np.full(len(SUFFIXES), np.nan))
                soutien_sim = np.isin(S[m], (4.0, 5.0)).mean(axis=0) * 100.0
                for j, s in enumerate(SUFFIXES):
                    lignes_item.append({
                        "configuration": nom, "ancrage": ancrage, "camp": camp,
                        "enonce": s, "libelle": stmts[j], "n_personnes": n_c,
                        "modele_second_ordre": M[camp][j],
                        "reel": reel[j], "croyance_humaine_endo": H[(ancrage, camp)][j],
                        "croyance_humaine_exo": (H[(ancrage, oppose)][j] if oppose
                                                 else float("nan")),
                        "d_reel": d_reel[j], "d_endo": d_endo[j], "d_exo": d_exo[j],
                        "plancher": P[(ancrage, camp)][j],
                        "modele_soutien_simule": soutien_sim[j],
                    })
                mr, br, hr = ic_moyenne_items(d_reel, rng)
                mn, bn, hn = ic_moyenne_items(d_endo, rng)
                mx, bx, hx = ic_moyenne_items(d_exo, rng)
                mp, bp, hp = ic_moyenne_items(P[(ancrage, camp)], rng)
                lignes_cell.append({
                    "configuration": nom, "ancrage": ancrage, "camp": camp,
                    "n_personnes": n_c,
                    "effectif_suffisant": "oui" if n_c >= EFFECTIF_MIN else "non",
                    "D_reel": mr, "D_reel_bas": br, "D_reel_haut": hr,
                    "D_endo": mn, "D_endo_bas": bn, "D_endo_haut": hn,
                    "D_exo": mx, "D_exo_bas": bx, "D_exo_haut": hx,
                    "plancher": mp, "plancher_bas": bp, "plancher_haut": hp,
                })
                if n_c < EFFECTIF_MIN or camp == "centre":
                    continue
                # H1 : D_endo contre D_reel
                r, rb, rh = ic_rapport_items(d_endo, d_reel, rng)
                p, J = p_signe_exacte(d_endo - d_reel)
                tests.append({"famille": "F1 H1 endo contre reel", "configuration": nom,
                              "ancrage": ancrage, "camp": camp, "n_enonces": J,
                              "quantite": "D_endo / D_reel", "valeur": r,
                              "ic_bas": rb, "ic_haut": rh, "p_brute": p,
                              "sens_predit": "rapport inferieur a 1"})
                # H3 : plus pres de la caricature de gauche que de celle de droite
                dg = np.abs(M[camp] - H[(ancrage, "gauche")])
                dd = np.abs(M[camp] - H[(ancrage, "droite")])
                r3, r3b, r3h = ic_rapport_items(dg, dd, rng)
                p3, _ = p_signe_exacte(dg - dd)
                tests.append({"famille": "F3 H3 lentille", "configuration": nom,
                              "ancrage": ancrage, "camp": camp, "n_enonces": J,
                              "quantite": "d_gauche / d_droite", "valeur": r3,
                              "ic_bas": r3b, "ic_haut": r3h, "p_brute": p3,
                              "sens_predit": "rapport inferieur a 1"})
                # H4 : D_reel contre le plancher
                r4, r4b, r4h = ic_rapport_items(d_reel, P[(ancrage, camp)], rng)
                p4, _ = p_signe_exacte(d_reel - P[(ancrage, camp)])
                tests.append({"famille": "F4 H4 plancher", "configuration": nom,
                              "ancrage": ancrage, "camp": camp, "n_enonces": J,
                              "quantite": "D_reel / plancher", "valeur": r4,
                              "ic_bas": r4b, "ic_haut": r4h, "p_brute": p4,
                              "sens_predit": "rapport superieur a 1"})
                # H5, controle de premier ordre, sans test
                controles.append({
                    "bloc": "H5 premier ordre", "configuration": nom, "ancrage": ancrage,
                    "camp": camp,
                    "soutien_simule_moyen": float(np.nanmean(soutien_sim)),
                    "soutien_reel_moyen": float(np.nanmean(reel)),
                    "soutien_reel_du_camp": float(
                        np.isin(hum["soutien_w4"][hum["camps"][ancrage] == camp],
                                (4.0, 5.0)).mean() * 100.0),
                })
            # H2 : amplification de l'ecart entre camps
            if np.isfinite(M.get("gauche", np.nan)).any() and \
               np.isfinite(M.get("droite", np.nan)).any():
                gm = np.abs(M["gauche"] - M["droite"])
                gh = np.abs(ecart_h[ancrage])
                a, ab, ah = ic_rapport_items(gm, gh, rng)
                pa, J = p_signe_exacte(gm - gh)
                ampli.append({"configuration": nom, "ancrage": ancrage,
                              "ecart_modele": float(np.nanmean(gm)),
                              "ecart_humain": float(np.nanmean(gh)),
                              "amplification": a, "ic_bas": ab, "ic_haut": ah,
                              "p_brute": pa,
                              "materiel": "non" if (BANDE[0] <= a <= BANDE[1]) else "oui"})
                tests.append({"famille": "F2 H2 amplification", "configuration": nom,
                              "ancrage": ancrage, "camp": "gauche contre droite",
                              "n_enonces": J, "quantite": "ecart modele / ecart humain",
                              "valeur": a, "ic_bas": ab, "ic_haut": ah, "p_brute": pa,
                              "sens_predit": "rapport superieur a 1"})

    # --- Holm par famille --------------------------------------------------
    t = pd.DataFrame(tests)
    if len(t):
        t["p_holm"] = np.nan
        for fam, g in t.groupby("famille"):
            bon = g["p_brute"].notna()
            t.loc[g.index[bon], "p_holm"] = holm(g.loc[bon, "p_brute"].to_numpy())
        t["materiel"] = np.where(
            t["valeur"].between(BANDE[0], BANDE[1]), "non", "oui")
    t.to_csv(os.path.join(SORTIE, "s1-tests.csv"), index=False)
    pd.DataFrame(lignes_cell).to_csv(os.path.join(SORTIE, "s1-cellules.csv"), index=False)
    pd.DataFrame(lignes_item).to_csv(os.path.join(SORTIE, "s1-par-enonce.csv"), index=False)
    pd.DataFrame(ampli).to_csv(os.path.join(SORTIE, "s1-amplification.csv"), index=False)

    # --- controle : bootstrap sur les personnes ---------------------------
    for ancrage, lab in hum["camps"].items():
        for camp in ("gauche", "droite"):
            m = np.where(lab == camp)[0]
            if len(m) < EFFECTIF_MIN:
                continue
            tir = np.empty(N_BOOT_PERS)
            for b in range(N_BOOT_PERS):
                s = rng.choice(m, size=len(m), replace=True)
                tir[b] = np.nanmean(hum["second_w4"][s])
            controles.append({
                "bloc": "bootstrap personnes, croyance humaine", "ancrage": ancrage,
                "camp": camp, "n_personnes": len(m),
                "moyenne": float(np.nanmean(hum["second_w4"][m])),
                "ic_bas": float(np.percentile(tir, 2.5)),
                "ic_haut": float(np.percentile(tir, 97.5))})
    # sensibilite du seuil de soutien
    controles.append({"bloc": "sensibilite seuil de soutien",
                      "reel_moyen_4ou5": float(reel.mean()),
                      "reel_moyen_3a5": float(reel_large.mean())})

    # --- EXPLORATOIRE, ajoute apres le declenchement du critere de chute 5 -------------
    # Le critere 5 compare un bruit individuel, l'ecart d'une personne a elle meme d'une
    # vague a l'autre, a un contraste de groupe, l'ecart entre deux moyennes de camp. Les
    # deux quantites ne sont pas commensurables : la moyenne d'un camp de n personnes a une
    # dispersion de l'ordre de P / racine(n), pas de P. Le critere, tel qu'il est ecrit,
    # teste donc le mauvais bruit. On publie ici la version de groupe, qui est la quantite
    # reellement employee par H1, H3 et H4 : le deplacement de la MOYENNE du camp entre les
    # deux vagues. Ce bloc est exploratoire et n'est le chiffre de tete de rien.
    for ancrage, lab in hum["camps"].items():
        for camp in ("gauche", "centre", "droite"):
            m = (lab == camp)
            if m.sum() < EFFECTIF_MIN:
                continue
            h13 = moyenne_camp(hum["second_w13"], m)
            h4 = moyenne_camp(hum["second_w4"], m)
            controles.append({
                "bloc": "exploratoire, plancher de groupe", "ancrage": ancrage,
                "camp": camp, "n_personnes": int(m.sum()),
                "plancher_groupe": float(np.nanmean(np.abs(h13 - h4))),
                "erreur_type_moyenne_camp": float(
                    np.nanmean(np.nanstd(hum["second_w4"][m], axis=0)) / np.sqrt(m.sum())),
                "plancher_individuel": float(np.nanmean(P[(ancrage, camp)])),
                "ecart_humain_entre_camps": float(np.nanmean(np.abs(ecart_h[ancrage]))),
            })
    # --- EXPLORATOIRE : la meme amplification, mais sur le PREMIER ordre ---------------
    # H5 comparait des niveaux. On compare ici des ecarts entre camps, dans la meme forme
    # que H2, pour savoir si l'amplification du second ordre est un simple report de
    # l'amplification du premier. Bloc exploratoire, jamais un chiffre de tete.
    prem = []
    for ancrage, lab in hum["camps"].items():
        mg, md = (lab == "gauche"), (lab == "droite")
        rg = np.isin(hum["soutien_w4"][mg], (4.0, 5.0)).mean(axis=0) * 100.0
        rd = np.isin(hum["soutien_w4"][md], (4.0, 5.0)).mean(axis=0) * 100.0
        gh1 = np.abs(rg - rd)
        for mod in modeles:
            if mod.get("doublon_de") or float(np.isnan(mod["autres"]).mean()) > SEUIL_PARSE:
                continue
            pos = pd.Series(np.arange(len(hum["pid"])), index=hum["pid"])
            idx = pos.reindex(mod["pid"]).to_numpy()
            ok = np.isfinite(idx)
            lm = lab[idx[ok].astype(int)]
            S = mod["soi"][ok]
            sg = np.isin(S[lm == "gauche"], (4.0, 5.0)).mean(axis=0) * 100.0
            sd = np.isin(S[lm == "droite"], (4.0, 5.0)).mean(axis=0) * 100.0
            gm1 = np.abs(sg - sd)
            a1, a1b, a1h = ic_rapport_items(gm1, gh1, rng)
            p1, _ = p_signe_exacte(gm1 - gh1)
            prem.append({"configuration": mod["configuration"], "ancrage": ancrage,
                         "ecart_modele_premier_ordre": float(np.nanmean(gm1)),
                         "ecart_reel_premier_ordre": float(np.nanmean(gh1)),
                         "amplification_premier_ordre": a1, "ic_bas": a1b, "ic_haut": a1h,
                         "p_brute": p1})
    pd.DataFrame(prem).to_csv(
        os.path.join(SORTIE, "s1-amplification-premier-ordre.csv"), index=False)

    pd.DataFrame(controles).to_csv(os.path.join(SORTIE, "s1-controles.csv"), index=False)

    print(f"configurations lues : {len(modeles)}")
    print(f"cellules : {len(lignes_cell)}  tests : {len(t)}  amplifications : {len(ampli)}")
    print(f"sorties dans {SORTIE}")


if __name__ == "__main__":
    main()
