"""
c7_park_armement_egal : a armement egal, que reste-t-il au jumeau sur Park ?

===========================================================================
PREENREGISTREMENT : resultats/audit-park-armement-egal-2026-09-13.md section 0,
ECRIT ET COMMITE AVANT ce fichier et avant le premier calcul. Predictions P1 a P5,
criteres de refutation, conventions de departage des ex aequo, regle d'arret.

ETUDE DE RISQUE DE VIE PRIVEE sur des jeux deja publics (archive Park et al., Twin-2K-500).
Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identifiant d'une personne, ni un
appariement individuel, ni la cellule demographique d'une personne : seuls des taux et
des distributions agregees sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  c7_stanford.charger_domaine / coder_categoriel_commun / accord_categoriel
                                      le bloc GSS de l'archive Park et son codage commun
  c7_stanford.rangs_depuis_accord     la variante a 20 tirages, pour le SEUL raccordement
  c7_attaquant_fort.scores_hors_pli   l'attaquant fort A-LLR, hors pli, non modifie
  c7_monde_ouvert.marges_deux_regimes / roc_et_taux / compte_au_moins / pmm_depuis_demo
                                      le protocole de monde ouvert, non modifie
  c7_fort_monde_ouvert_ic.charger_twin / charger_stanford
                                      les chargeurs canoniques, utilises comme ASSERTION
  c7_reidentification.items_communs / graine_nom / REF_V4 / REF_V13 / DEMO
                                      les 60 items toujours renseignes de Twin, la graine
  c7_controle_interpretabilite.EchecControleInterpretabilite / la regle de decision
  a2_commun.distance_hamming / bootstrap_personnes / en_codes
  t1_commun.charger / ecrire

CE QUI EST NOUVEAU ICI, et rien d'autre :
  1. la reproduction INDEPENDANTE de 85,17 % / 29,09 % (chemin de mesure reecrit) ;
  2. le departage EXACT des ex aequo (trois conventions, deterministe) applique a TOUTES
     les cellules du tableau a armement egal ;
  3. le bootstrap APPARIE du rapport cible / comparateur ;
  4. la courbe du comparateur ARME en fonction du nombre d'items retenus sur Park ;
  5. la structure des cellules demographiques de Park (unicite, plafond de cellule,
     taux par taille de cellule) -- ce que le comparateur exploite reellement.

Aucun appel de modele de langage, aucune depense, aucun reseau. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_park_armement_egal.py
===========================================================================
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes, en_codes    # noqa: E402
from c7_reidentification import (                                        # noqa: E402
    items_communs, graine_nom, REF_V4, REF_V13, DEMO,
)
from c7_attaquant_fort import scores_hors_pli, CIBLE_TWIN, CIBLE_STAN    # noqa: E402
from c7_monde_ouvert import (                                            # noqa: E402
    marges_deux_regimes, roc_et_taux, compte_au_moins, pmm_depuis_demo,
)
import c7_fort_monde_ouvert_ic as MO                                     # noqa: E402
import c7_stanford as CS                                                 # noqa: E402

GRAINE = 20260913
N_BOOTSTRAP = 2000
TOL = 1e-12
FPR_CIBLES = (0.001, 0.01)

# Grille du volet 4, prescrite par le mandat. n_tirages REDUIT de 20 (convention
# c7_stanford.N_TIRAGES_ITEMS) a 8 : declare au rapport, motif = duree.
KS_ITEMS = (20, 40, 60, 100, 177)
N_TIRAGES_ITEMS = 8

# Valeurs publiees par agent/mesures/t1a-complements, utilisees UNIQUEMENT comme
# verification de raccordement. Aucune n'entre dans un calcul.
RACCORDEMENT = {
    "Park GSS|comparateur demographique|A-LLR|top1_ferme": (0.851711, 0.0050),
    "Park GSS|comparateur demographique|A-LLR|tpr_1pct": (0.290875, 0.0100),
    "Park GSS|comparateur demographique|naif|top1_ferme": (0.022433, 0.0050),
    "Park GSS|cible|A-LLR|top1_ferme": (0.903992, 0.0050),
    "Park GSS|cible|A-LLR|tpr_1pct": (0.601711, 0.0100),
    "Twin|cible|A-LLR|top1_ferme": (0.232264, 0.0050),
    "Twin|comparateur demographique|A-LLR|top1_ferme": (0.007775, 0.0050),
}
_ecarts = []


def raccorder(cle, valeur):
    if cle not in RACCORDEMENT:
        return None
    attendu, tol = RACCORDEMENT[cle]
    ok = abs(float(valeur) - attendu) <= tol
    print(f"    [raccordement {'OK   ' if ok else 'ECART'}] {cle} : "
          f"mesure {valeur:.6f}, publie {attendu:.6f}, ecart "
          f"{abs(valeur - attendu)*100:.4f} pt (tol {tol*100:.2f} pt)", flush=True)
    if not ok:
        _ecarts.append((cle, float(valeur), attendu))
    return ok


def ligne(volet, jeu, condition, attaque, mesure, valeur, bas=np.nan, haut=np.nan, **e):
    d = {"volet": volet, "jeu": jeu, "condition": condition, "attaque": attaque,
         "mesure": mesure, "valeur": valeur, "ic_bas": bas, "ic_haut": haut}
    d.update(e)
    return d


def ic(indic, cle):
    return bootstrap_personnes(np.asarray(indic, dtype=float), N_BOOTSTRAP,
                               [GRAINE, graine_nom(cle)])


# ---------------------------------------------------------------------------
# 1. Departage des ex aequo : EXACT, trois conventions, sur UNE matrice de score
# ---------------------------------------------------------------------------

def departage_exact(score, vrai_idx):
    """Trois lectures deterministes de la MEME matrice de score.

    uniforme  : 1/|classe de tete| si la vraie personne y est, 0 sinon. C'est
                l'ESPERANCE du tirage aleatoire d'ex aequo, sans bruit de Monte-Carlo.
                Convention retenue pour tous les chiffres de tete (preenregistrement 0.1).
    en_faveur : compte des que rien n'est STRICTEMENT meilleur (borne haute).
    contre    : compte seulement si la classe de tete est un singleton (borne basse).
    """
    n = score.shape[0]
    r = np.arange(n)
    vrai = score[r, vrai_idx]
    meilleur = score.max(axis=1)
    taille = (score >= meilleur[:, None] - TOL).sum(axis=1)
    dans = vrai >= meilleur - TOL
    en_faveur = dans.astype(float)
    contre = ((score >= vrai[:, None] - TOL).sum(axis=1) == 1).astype(float)
    uniforme = np.where(dans, 1.0 / taille, 0.0)
    return {"uniforme": uniforme, "en_faveur": en_faveur, "contre": contre,
            "taille_classe": taille}


def escalier(marge_p, correct, marge_r, n):
    """TPR en escalier exact aux FPR cibles : aucun seuil interpole."""
    seuils = np.unique(np.concatenate([marge_p, marge_r]))
    tp = compte_au_moins(np.sort(marge_p[correct >= 0.5]), seuils)
    fp = compte_au_moins(np.sort(marge_r), seuils)
    tpr, fpr = tp / n, fp / n
    out = {}
    for c in FPR_CIBLES:
        ok = fpr <= c
        if not ok.any():
            out[c] = None
            continue
        j = int(np.argmax(np.where(ok, tpr, -1.0)))
        out[c] = {"tpr_escalier": float(tpr[j]), "fpr_atteint": float(fpr[j]),
                  "fp_absolus": int(fp[j]),
                  "vraies_detections_absolues": int(tp[j]),
                  "granularite_un_fp": 1.0 / n}
    return out


# ---------------------------------------------------------------------------
# 2. Chargement : UN bassin par jeu, partage par la cible et par le comparateur
# ---------------------------------------------------------------------------

def charger_park():
    ordre, items, tables, _ = CS.charger_domaine("gss")
    codes = CS.coder_categoriel_commun(tables, items)
    pool = codes[CS.VAGUE1]
    n = pool.shape[0]
    vrai_idx = np.arange(n)
    xr, pr, vr = MO.charger_stanford()
    if not (np.array_equal(codes[CIBLE_STAN], xr) and np.array_equal(pool, pr)
            and np.array_equal(vrai_idx, vr)):
        raise SystemExit("Park : bassin different du chargeur canonique. Volet invalide.")
    demo = pd.read_csv(CS.DEMO_CSV).set_index("email").loc[ordre]
    demo_codes = en_codes(demo[["gender", "race", "age", "education"]]
                          .astype(str).to_numpy(dtype=object))
    # Le bloc COMPLET reellement fourni a l'agent « demographique » (v6) : toutes les
    # colonnes de demographic_summary.csv hors la cle de jointure. Il ne sert qu'a
    # mesurer l'unicite ; il n'entre dans aucun score.
    axes = [c for c in demo.columns if c != "email"]
    demo_complet = en_codes(demo[axes].astype(str).to_numpy(dtype=object))
    pmm = pmm_depuis_demo(demo_codes, pool, np.random.default_rng([GRAINE, 31]))
    return {"jeu": "Park GSS", "pool": pool, "vrai_idx": vrai_idx, "n": n,
            "n_items": pool.shape[1], "llr": "stan|llr", "demo_codes": demo_codes,
            "demo_complet": demo_complet, "axes_demo": axes,
            "accord": lambda x, p: CS.accord_categoriel(x, p),
            "cible": (f"cible : meilleur agent ({CIBLE_STAN})", codes[CIBLE_STAN]),
            "comparateurs": [("comparateur demographique", codes[CS.DEMO_COND]),
                             ("PMM k=10", pmm)]}


def charger_twin():
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    n = pool.shape[0]
    couverts = np.flatnonzero((codes[CIBLE_TWIN] >= 0).any(axis=1))
    xr, pr, cr = MO.charger_twin()
    if not (np.array_equal(codes[CIBLE_TWIN][:, items][couverts], xr)
            and np.array_equal(pool, pr) and np.array_equal(couverts, cr)):
        raise SystemExit("Twin : bassin different du chargeur canonique. Volet invalide.")
    demo_codes = en_codes(paq["demo"]["x"])
    pmm = pmm_depuis_demo(demo_codes, pool, np.random.default_rng([GRAINE, 32]))
    return {"jeu": "Twin", "pool": pool, "vrai_idx": couverts, "n": n,
            "n_items": len(items), "llr": "twin|llr", "demo_codes": demo_codes,
            "accord": lambda x, p: 1.0 - distance_hamming(x, p),
            "cible": (f"cible : {CIBLE_TWIN}", codes[CIBLE_TWIN][:, items][couverts]),
            "comparateurs": [("comparateur demographique",
                              codes[DEMO][:, items][couverts]),
                             ("PMM k=10", pmm[couverts])]}


def score_de(jd, x, attaque, colonnes=None):
    pool = jd["pool"] if colonnes is None else jd["pool"][:, colonnes]
    xx = x if colonnes is None else x[:, colonnes]
    if attaque.startswith("A-LLR"):
        return scores_hors_pli(x, jd["pool"], jd["vrai_idx"], jd["llr"],
                               colonnes=colonnes)
    return jd["accord"](xx, pool)


# ---------------------------------------------------------------------------
# 3. Une cellule du tableau a armement egal
# ---------------------------------------------------------------------------

def cellule(jd, nom, x, attaque, lignes, volet, cle_racc=None):
    """Une condition, une attaque, sur le bassin DEJA fixe. Renvoie tout le necessaire."""
    vrai_idx, n = jd["vrai_idx"], jd["n"]
    if x.shape[0] != len(vrai_idx) or x.shape[1] != jd["pool"].shape[1]:
        raise SystemExit(f"{jd['jeu']}/{nom} : forme {x.shape} hors bassin.")
    score = score_de(jd, x, attaque)

    d = departage_exact(score, vrai_idx)
    m_u, b_u, h_u = ic(d["uniforme"], f"{jd['jeu']}|{nom}|{attaque}|uniforme")
    m_f, b_f, h_f = ic(d["en_faveur"], f"{jd['jeu']}|{nom}|{attaque}|en_faveur")
    m_c, b_c, h_c = ic(d["contre"], f"{jd['jeu']}|{nom}|{attaque}|contre")

    # variante a 20 tirages, pour le seul raccordement a la chaine publiee
    rng_f = np.random.default_rng([GRAINE, 41, graine_nom(nom + attaque)])
    _, t1_mc, _ = CS.rangs_depuis_accord(score, vrai_idx, rng_f, 20)
    m_mc, b_mc, h_mc = ic(t1_mc, f"{jd['jeu']}|{nom}|{attaque}|mc20")

    rng_o = np.random.default_rng([GRAINE, 42, graine_nom(nom + attaque)])
    mp, correct, mr = marges_deux_regimes(score, vrai_idx, rng_o)
    r = roc_et_taux(mp, correct, mr, n)
    esc = escalier(mp, correct, mr, n)

    commun = dict(n_attaques=len(vrai_idx), n_pool=n, n_items=jd["n_items"],
                  hasard=1.0 / n)
    L = lignes.append
    L(ligne(volet, jd["jeu"], nom, attaque, "top1_ferme_uniforme_PUBLIE", m_u, b_u, h_u,
            **commun))
    L(ligne(volet, jd["jeu"], nom, attaque, "top1_ferme_borne_en_faveur", m_f, b_f, h_f,
            **commun))
    L(ligne(volet, jd["jeu"], nom, attaque, "top1_ferme_borne_contre", m_c, b_c, h_c,
            **commun))
    L(ligne(volet, jd["jeu"], nom, attaque, "top1_ferme_mc20_raccordement", m_mc, b_mc,
            h_mc, **commun))
    L(ligne(volet, jd["jeu"], nom, attaque, "classe_tete_taille_mediane",
            float(np.median(d["taille_classe"])), **commun))
    L(ligne(volet, jd["jeu"], nom, attaque, "classe_tete_part_singletons",
            float((d["taille_classe"] == 1).mean()), **commun))
    L(ligne(volet, jd["jeu"], nom, attaque, "auc_monde_ouvert", float(r["auc"]), **commun))
    for c in FPR_CIBLES:
        et = f"{c*100:g}pct".replace(".", "_")
        pub = r["tpr_fpr_0_1pct"] if c == 0.001 else r["tpr_fpr_1pct"]
        L(ligne(volet, jd["jeu"], nom, attaque, f"tpr_a_fpr_{et}_np_interp",
                float(pub), fpr_cible=c, **commun))
        e = esc[c]
        if e is None:
            continue
        for k, v in e.items():
            L(ligne(volet, jd["jeu"], nom, attaque, f"tpr_a_fpr_{et}_{k}", v,
                    fpr_cible=c, **commun))

    print(f"    {nom:34s} / {attaque:16s} ferme={m_u*100:7.4f} % "
          f"[{b_u*100:.2f};{h_u*100:.2f}]  (bornes {m_c*100:.2f} / {m_f*100:.2f})  "
          f"AUC={r['auc']:.4f}", flush=True)
    for c in FPR_CIBLES:
        e, pub = esc[c], (r["tpr_fpr_0_1pct"] if c == 0.001 else r["tpr_fpr_1pct"])
        if e is None:
            print(f"      FPR<={c*100:g}% : aucun seuil ; np.interp {pub*100:.4f} %",
                  flush=True)
        else:
            print(f"      FPR<={c*100:g}% : escalier {e['tpr_escalier']*100:7.4f} % "
                  f"({e['fp_absolus']} FP, {e['vraies_detections_absolues']} vraies) | "
                  f"np.interp {pub*100:7.4f} %", flush=True)
    if cle_racc:
        raccorder(f"{cle_racc}|top1_ferme", m_u)
        raccorder(f"{cle_racc}|tpr_1pct", r["tpr_fpr_1pct"])
    return {"indic": d["uniforme"], "top1": m_u, "bas": b_u, "haut": h_u,
            "auc": r["auc"], "tpr": {c: (esc[c]["tpr_escalier"] if esc[c] else 0.0)
                                     for c in FPR_CIBLES},
            "interp": {0.001: r["tpr_fpr_0_1pct"], 0.01: r["tpr_fpr_1pct"]}}


def rapport_apparie(a, b, cle):
    """Rapport a/b avec IC par bootstrap APPARIE sur les personnes (memes tirages)."""
    va, vb = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng([GRAINE, 51, graine_nom(cle)])
    n = len(va)
    idx = rng.integers(0, n, size=(N_BOOTSTRAP, n))
    ma, mb = va[idx].mean(axis=1), vb[idx].mean(axis=1)
    ok = mb > 0
    rr = np.where(ok, ma / np.maximum(mb, 1e-12), np.nan)
    point = float(va.mean() / vb.mean()) if vb.mean() > 0 else np.inf
    diff = ma - mb
    return {"rapport": point,
            "rapport_bas": float(np.nanpercentile(rr, 2.5)),
            "rapport_haut": float(np.nanpercentile(rr, 97.5)),
            "ecart_points": float(va.mean() - vb.mean()),
            "ecart_bas": float(np.percentile(diff, 2.5)),
            "ecart_haut": float(np.percentile(diff, 97.5))}


def temoin_permutation(jd, nom, x, lignes, volet, n_perm=5):
    """Lien personne-a-personne casse, tout le reste identique."""
    rng = np.random.default_rng([GRAINE, 43, graine_nom(jd["jeu"] + nom)])
    vals = []
    for _ in range(n_perm):
        s = scores_hors_pli(x[rng.permutation(x.shape[0])], jd["pool"], jd["vrai_idx"],
                            jd["llr"])
        vals.append(float(departage_exact(s, jd["vrai_idx"])["uniforme"].mean()))
    v = np.asarray(vals)
    lignes.append(ligne(volet, jd["jeu"], nom, "A-LLR (hors pli)",
                        "temoin_permutation_top1_ferme", float(v.mean()),
                        n_pool=jd["n"], hasard=1.0 / jd["n"], n_permutations=n_perm,
                        temoin_min=float(v.min()), temoin_max=float(v.max()),
                        note="tirages d'une LOI NULLE, PAS un intervalle de confiance"))
    print(f"      temoin de permutation ({n_perm}) : {v.mean()*100:.4f} % "
          f"[{v.min()*100:.4f}-{v.max()*100:.4f}] contre hasard {100.0/jd['n']:.4f} %",
          flush=True)


# ---------------------------------------------------------------------------
# 4. Volet : courbe du comparateur ARME en fonction du nombre d'items (Park)
# ---------------------------------------------------------------------------

def volet_items(jd, lignes):
    print("\n" + "=" * 78, flush=True)
    print(f"VOLET 4 — {jd['jeu']} : taux ARME en fonction du nombre d'items retenus "
          f"(bassin constant, {N_TIRAGES_ITEMS} tirages d'items par k)", flush=True)
    print("=" * 78, flush=True)
    volet = "4 courbe items"
    n_items = jd["n_items"]
    conditions = [jd["cible"], jd["comparateurs"][0]]
    rng = np.random.default_rng([GRAINE, 61])
    for k in KS_ITEMS:
        k = min(k, n_items)
        tirages = ([np.arange(n_items)] if k == n_items
                   else [np.sort(rng.choice(n_items, k, replace=False))
                         for _ in range(N_TIRAGES_ITEMS)])
        par_cond = {}
        for nom, x in conditions:
            vals_fort, vals_naif = [], []
            for col in tirages:
                s_f = score_de(jd, x, "A-LLR", colonnes=col)
                vals_fort.append(departage_exact(s_f, jd["vrai_idx"])["uniforme"].mean())
                s_n = score_de(jd, x, "naif", colonnes=col)
                vals_naif.append(departage_exact(s_n, jd["vrai_idx"])["uniforme"].mean())
            for att, vv in (("A-LLR (hors pli)", vals_fort), ("naif (Hamming)", vals_naif)):
                v = np.asarray(vv, dtype=float)
                lignes.append(ligne(
                    volet, jd["jeu"], nom, att, "top1_ferme_uniforme_moyenne_tirages",
                    float(v.mean()), float(v.min()), float(v.max()),
                    k_items=k, n_tirages_items=len(tirages), n_pool=jd["n"],
                    hasard=1.0 / jd["n"],
                    note="ic_bas/ic_haut = min/max sur les tirages d'items, PAS un IC"))
            par_cond[nom] = (float(np.mean(vals_fort)), float(np.mean(vals_naif)))
        nc, nb = conditions[0][0], conditions[1][0]
        rap = par_cond[nc][0] / par_cond[nb][0] if par_cond[nb][0] > 0 else np.inf
        lignes.append(ligne(volet, jd["jeu"], "rapport cible / comparateur",
                            "A-LLR (hors pli)", "rapport_top1_ferme", float(rap),
                            k_items=k, n_pool=jd["n"]))
        print(f"  k={k:4d} items : comparateur arme {par_cond[nb][0]*100:7.4f} % "
              f"(naif {par_cond[nb][1]*100:6.4f} %) | cible armee "
              f"{par_cond[nc][0]*100:7.4f} % (naif {par_cond[nc][1]*100:6.4f} %) | "
              f"rapport {rap:5.2f}x", flush=True)


# ---------------------------------------------------------------------------
# 5. Volet : ce que le comparateur demographique exploite reellement
# ---------------------------------------------------------------------------

def volet_structure(jd, lignes, indic_arme, indic_naif):
    """Structure des cellules demographiques et concentration du succes arme.

    AUCUNE cellule d'aucune personne n'est imprimee ni ecrite : seules la distribution
    des tailles de cellule et des moyennes par TRANCHE de taille sortent.
    """
    print("\n" + "=" * 78, flush=True)
    print(f"VOLET 5 — {jd['jeu']} : ce que le comparateur demographique exploite",
          flush=True)
    print("=" * 78, flush=True)
    volet = "5 structure demographique"
    dc = jd["demo_codes"]
    cles = [tuple(r.tolist()) for r in dc]
    comptes = pd.Series(cles).value_counts()
    taille = np.array([comptes[c] for c in cles], dtype=float)

    n = len(taille)
    n_seules = int((taille == 1).sum())
    plafond = float(np.mean(1.0 / taille))
    n_axes = dc.shape[1]
    n_cellules = int(len(comptes))
    modalites = [int(len(np.unique(dc[:, j]))) for j in range(n_axes)]

    commun = dict(n_pool=jd["n"], n_axes_demographiques=n_axes,
                  modalites_par_axe="x".join(str(m) for m in modalites))
    L = lignes.append
    L(ligne(volet, jd["jeu"], "cellules demographiques", "-",
            "n_cellules_distinctes", float(n_cellules), **commun))
    L(ligne(volet, jd["jeu"], "cellules demographiques", "-",
            "n_personnes_seules_dans_leur_cellule", float(n_seules), **commun))
    L(ligne(volet, jd["jeu"], "cellules demographiques", "-",
            "part_personnes_seules_dans_leur_cellule", n_seules / n, **commun))
    L(ligne(volet, jd["jeu"], "cellules demographiques", "-",
            "taille_cellule_mediane", float(np.median(taille)), **commun))
    L(ligne(volet, jd["jeu"], "cellules demographiques", "-",
            "taille_cellule_moyenne", float(taille.mean()), **commun))
    L(ligne(volet, jd["jeu"], "cellules demographiques", "-",
            "taille_cellule_max", float(taille.max()), **commun))
    L(ligne(volet, jd["jeu"], "cellules demographiques", "-",
            "plafond_cellule_seule_moyenne_un_sur_taille", plafond, **commun))
    print(f"  {n_cellules} cellules distinctes sur {n} personnes "
          f"({'x'.join(str(m) for m in modalites)} modalites) ; "
          f"{n_seules} personnes ({n_seules/n*100:.2f} %) SEULES dans leur cellule ; "
          f"taille mediane {np.median(taille):.0f}, max {taille.max():.0f}", flush=True)
    print(f"  plafond d'une attaque qui ne lirait QUE la cellule : "
          f"moyenne(1/|cellule|) = {plafond*100:.4f} %", flush=True)

    # concentration du succes arme par tranche de taille de cellule
    tranches = [(1, 1), (2, 2), (3, 5), (6, 10), (11, 10**9)]
    for lo, hi in tranches:
        m = (taille >= lo) & (taille <= hi)
        if not m.any():
            continue
        et = f"taille {lo}" if lo == hi else (f"taille {lo}+" if hi > 10**8
                                             else f"taille {lo}-{hi}")
        for nom_i, indic in (("A-LLR (hors pli)", indic_arme),
                             ("naif (Hamming)", indic_naif)):
            v = np.asarray(indic, float)[m]
            mv, bv, hv = ic(v, f"{jd['jeu']}|tranche|{et}|{nom_i}")
            L(ligne(volet, jd["jeu"], f"comparateur demographique, cellule {et}", nom_i,
                    "top1_ferme_uniforme", mv, bv, hv, n_personnes=int(m.sum()),
                    n_pool=jd["n"], taille_cellule_min=lo,
                    taille_cellule_max=(np.nan if hi > 10**8 else hi)))
        print(f"    cellule {et:12s} : {int(m.sum()):4d} personnes, "
              f"comparateur arme {np.asarray(indic_arme, float)[m].mean()*100:7.4f} %, "
              f"naif {np.asarray(indic_naif, float)[m].mean()*100:6.4f} %", flush=True)

    # Le succes arme est-il lie a la rarete de la cellule ? correlation de rang.
    from scipy import stats
    rho = stats.spearmanr(taille, np.asarray(indic_arme, float))
    L(ligne(volet, jd["jeu"], "comparateur demographique", "A-LLR (hors pli)",
            "spearman_taille_cellule_vs_top1", float(rho.statistic),
            p_value=float(rho.pvalue), n_pool=jd["n"],
            note="negatif = le succes se concentre sur les cellules rares"))
    print(f"  Spearman(taille de cellule, top-1 arme) = {rho.statistic:+.4f} "
          f"(p = {rho.pvalue:.2e})", flush=True)

    # Determination des items par la demographie : part de la modalite majoritaire
    # dans la cellule, moyennee sur les items et les personnes (pool humain reel).
    pool = jd["pool"]
    parts = []
    for cle_c, taille_c in comptes.items():
        if taille_c < 2:
            continue
        idx = np.flatnonzero(np.array([c == cle_c for c in cles]))
        sous = pool[idx]
        for j in range(sous.shape[1]):
            col = sous[:, j]
            col = col[col >= 0]
            if len(col) < 2:
                continue
            parts.append(np.bincount(col).max() / len(col))
    part_maj = float(np.mean(parts)) if parts else np.nan
    # reference : meme quantite sur des groupes de MEME TAILLE tires au hasard
    rngp = np.random.default_rng([GRAINE, 71])
    parts_h = []
    for cle_c, taille_c in comptes.items():
        if taille_c < 2:
            continue
        idx = rngp.choice(n, int(taille_c), replace=False)
        sous = pool[idx]
        for j in range(sous.shape[1]):
            col = sous[:, j]
            col = col[col >= 0]
            if len(col) < 2:
                continue
            parts_h.append(np.bincount(col).max() / len(col))
    part_h = float(np.mean(parts_h)) if parts_h else np.nan
    L(ligne(volet, jd["jeu"], "items humains", "-",
            "part_modalite_majoritaire_dans_la_cellule", part_maj,
            temoin_groupes_aleatoires_meme_taille=part_h, n_pool=jd["n"],
            note="ecart au temoin = part de l'item reellement determinee par la demographie"))
    print(f"  part de la modalite majoritaire dans la cellule : {part_maj*100:.2f} % "
          f"contre {part_h*100:.2f} % sur des groupes aleatoires de meme taille "
          f"(ecart {(part_maj - part_h)*100:+.2f} pt)", flush=True)


def _unicite(codes_bloc):
    """(n cellules, n personnes seules, part seules, plafond moyenne(1/|cellule|))."""
    cles = [tuple(r.tolist()) for r in codes_bloc]
    comptes = pd.Series(cles).value_counts()
    t = np.array([comptes[c] for c in cles], dtype=float)
    return int(len(comptes)), int((t == 1).sum()), float((t == 1).mean()), \
        float(np.mean(1.0 / t)), t


def volet_bloc_demographique(jd, lignes, indic_arme):
    """Le bloc REELLEMENT fourni a l'agent « demographique », et son unicite.

    Le comparateur de Park n'est pas « genre x race x age x education » : c'est un agent
    conditionne sur TOUTES les colonnes de demographic_summary.csv. Ce volet mesure
    l'unicite de ce bloc, celle de chaque sous-bloc laisse-un-de-cote, et la part de
    chaque item humain reellement determinee par chaque attribut. Aucune valeur
    individuelle n'est imprimee ni ecrite.
    """
    print("\n" + "=" * 78, flush=True)
    print(f"VOLET 5bis — {jd['jeu']} : le bloc demographique REELLEMENT fourni a l'agent",
          flush=True)
    print("=" * 78, flush=True)
    volet = "5bis bloc demographique reel"
    dc, axes = jd["demo_complet"], jd["axes_demo"]
    n = dc.shape[0]
    pool = jd["pool"]
    L = lignes.append

    nc, ns, ps, plaf, t_full = _unicite(dc)
    mods = [int(len(np.unique(dc[:, j]))) for j in range(dc.shape[1])]
    commun = dict(n_pool=jd["n"], n_axes=len(axes),
                  axes="+".join(axes), modalites="x".join(str(m) for m in mods))
    for m, v in (("n_cellules_distinctes", float(nc)),
                 ("n_personnes_seules_dans_leur_cellule", float(ns)),
                 ("part_personnes_seules_dans_leur_cellule", ps),
                 ("plafond_cellule_seule_moyenne_un_sur_taille", plaf),
                 ("taille_cellule_mediane", float(np.median(t_full)))):
        L(ligne(volet, jd["jeu"], "bloc complet fourni a l'agent", "-", m, v, **commun))
    print(f"  bloc COMPLET ({len(axes)} attributs : {', '.join(axes)})", flush=True)
    print(f"    {nc} cellules pour {n} personnes ; {ns} personnes ({ps*100:.2f} %) "
          f"SEULES dans leur cellule ; plafond moyenne(1/|cellule|) = {plaf*100:.2f} % ; "
          f"taille mediane {np.median(t_full):.0f}", flush=True)
    L(ligne(volet, jd["jeu"], "comparateur demographique arme", "A-LLR (hors pli)",
            "top1_ferme_uniforme", float(np.mean(indic_arme)),
            plafond_bloc_complet=plaf, n_pool=jd["n"],
            note="a comparer au plafond du bloc complet : au-dessus = A-LLR fait plus "
                 "que relire la cellule ; au-dessous = il ne fait que la relire"))

    # sous-blocs cumules : combien d'attributs suffisent a rendre les gens uniques ?
    for k in range(1, len(axes) + 1):
        nck, nsk, psk, plafk, _ = _unicite(dc[:, :k])
        L(ligne(volet, jd["jeu"], f"{k} premiers attributs", "-",
                "part_personnes_seules_dans_leur_cellule", psk,
                n_cellules=float(nck), plafond=plafk, n_axes=k,
                axes="+".join(axes[:k]), n_pool=jd["n"]))
    # laisse-un-de-cote : quel attribut porte l'unicite ?
    print("  laisse-un-de-cote (part de personnes seules quand l'attribut est retire) :",
          flush=True)
    for j, a in enumerate(axes):
        garde = [i for i in range(len(axes)) if i != j]
        _, nsj, psj, plafj, _ = _unicite(dc[:, garde])
        L(ligne(volet, jd["jeu"], f"bloc sans « {a} »", "-",
                "part_personnes_seules_dans_leur_cellule", psj,
                plafond=plafj, attribut_retire=a, n_pool=jd["n"],
                chute_points=(ps - psj)))
        print(f"    sans {a:20s} : {psj*100:6.2f} %  (chute {(ps-psj)*100:+6.2f} pt)",
              flush=True)

    # determination des items humains par chaque attribut, contre un temoin de meme forme
    print("  part de la modalite majoritaire des items humains, par attribut "
          "(contre groupes aleatoires de meme taille) :", flush=True)
    rngp = np.random.default_rng([GRAINE, 72])
    for j, a in enumerate(axes):
        col_a = dc[:, j]
        p_obs, p_tem = [], []
        for g in np.unique(col_a):
            idx = np.flatnonzero(col_a == g)
            if len(idx) < 2:
                continue
            idx_t = rngp.choice(n, len(idx), replace=False)
            for sous, acc in ((pool[idx], p_obs), (pool[idx_t], p_tem)):
                for c in range(sous.shape[1]):
                    v = sous[:, c]
                    v = v[v >= 0]
                    if len(v) >= 2:
                        acc.append(np.bincount(v).max() / len(v))
        mo, mt = float(np.mean(p_obs)), float(np.mean(p_tem))
        L(ligne(volet, jd["jeu"], f"items humains | « {a} »", "-",
                "part_modalite_majoritaire", mo, temoin_aleatoire=mt,
                ecart_points=(mo - mt), n_modalites=int(len(np.unique(col_a))),
                n_pool=jd["n"]))
        print(f"    {a:20s} : {mo*100:5.2f} % contre temoin {mt*100:5.2f} % "
              f"(ecart {(mo-mt)*100:+5.2f} pt)", flush=True)


# ---------------------------------------------------------------------------
# 6. main
# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes = []
    resultats = {}

    for charger, racc_jeu in ((charger_park, "Park GSS"), (charger_twin, "Twin")):
        jd = charger()
        print("\n" + "=" * 78, flush=True)
        print(f"{jd['jeu']} : {jd['n']} personnes, {jd['n_items']} items, "
              f"bassin unique partage par toutes les conditions", flush=True)
        print("=" * 78, flush=True)
        nom_cible, x_cible = jd["cible"]
        res = {}
        print("  [cible]", flush=True)
        res[("cible", "naif")] = cellule(jd, nom_cible, x_cible, "naif (Hamming)",
                                        lignes, "2 armement egal")
        res[("cible", "fort")] = cellule(jd, nom_cible, x_cible, "A-LLR (hors pli)",
                                        lignes, "2 armement egal",
                                        f"{racc_jeu}|cible|A-LLR")
        temoin_permutation(jd, nom_cible, x_cible, lignes, "2 armement egal")

        print("  [comparateurs, meme bassin, meme attaque, meme convention]", flush=True)
        for nom_c, x_c in jd["comparateurs"]:
            cle = (f"{racc_jeu}|{nom_c}" if nom_c == "comparateur demographique"
                   else None)
            rn = cellule(jd, nom_c, x_c, "naif (Hamming)", lignes, "2 armement egal",
                         f"{cle}|naif" if cle else None)
            rf = cellule(jd, nom_c, x_c, "A-LLR (hors pli)", lignes, "2 armement egal",
                         f"{cle}|A-LLR" if cle else None)
            temoin_permutation(jd, nom_c, x_c, lignes, "2 armement egal")
            if nom_c == "comparateur demographique":
                res[("comp", "naif")], res[("comp", "fort")] = rn, rf

            # --- rapport et controle d'interpretabilite, sous CHAQUE attaque ---
            for att, kc, kb in (("naif (Hamming)", ("cible", "naif"), rn),
                                ("A-LLR (hors pli)", ("cible", "fort"), rf)):
                rc = res[kc]
                r = rapport_apparie(rc["indic"], kb["indic"],
                                    f"{jd['jeu']}|{nom_c}|{att}")
                passe = bool(rc["bas"] > kb["haut"])
                lignes.append(ligne(
                    "3 rapport et controle", jd["jeu"],
                    f"{nom_cible} vs {nom_c}", att, "rapport_top1_ferme",
                    r["rapport"], r["rapport_bas"], r["rapport_haut"],
                    ecart_points=r["ecart_points"], ecart_bas=r["ecart_bas"],
                    ecart_haut=r["ecart_haut"], cible_top1=rc["top1"],
                    cible_ic_bas=rc["bas"], cible_ic_haut=rc["haut"],
                    comparateur_top1=kb["top1"], comparateur_ic_bas=kb["bas"],
                    comparateur_ic_haut=kb["haut"],
                    controle_interpretabilite_passe=float(passe), n_pool=jd["n"],
                    note="bootstrap APPARIE sur les personnes ; controle = regle de "
                         "c7_controle_interpretabilite (IC disjoints), les deux "
                         "conditions sous la MEME attaque et le MEME bassin"))
                rap_tpr = (rc["tpr"][0.01] / kb["tpr"][0.01]
                           if kb["tpr"][0.01] > 0 else np.inf)
                lignes.append(ligne(
                    "3 rapport et controle", jd["jeu"],
                    f"{nom_cible} vs {nom_c}", att, "rapport_tpr_a_fpr_1pct_escalier",
                    float(rap_tpr), cible_tpr=rc["tpr"][0.01],
                    comparateur_tpr=kb["tpr"][0.01], n_pool=jd["n"]))
                print(f"      [{att}] rapport cible/{nom_c} = {r['rapport']:.3f}x "
                      f"[{r['rapport_bas']:.3f};{r['rapport_haut']:.3f}] ; "
                      f"ecart {r['ecart_points']*100:+.2f} pt "
                      f"[{r['ecart_bas']*100:+.2f};{r['ecart_haut']*100:+.2f}] ; "
                      f"controle {'PASSE' if passe else 'ECHEC'} ; "
                      f"rapport TPR@1% = {rap_tpr:.2f}x", flush=True)
        resultats[jd["jeu"]] = (jd, res)

    jd_park, res_park = resultats["Park GSS"]
    volet_items(jd_park, lignes)
    volet_structure(jd_park, lignes, res_park[("comp", "fort")]["indic"],
                    res_park[("comp", "naif")]["indic"])
    volet_bloc_demographique(jd_park, lignes, res_park[("comp", "fort")]["indic"])

    T1.ecrire(lignes, "c7-park-armement-egal.csv")
    print("\n" + "=" * 78, flush=True)
    if _ecarts:
        print("ECARTS DE RACCORDEMENT (a reporter tels quels) :", flush=True)
        for c, v, a in _ecarts:
            print(f"  {c} : mesure {v:.6f}, publie {a:.6f}", flush=True)
    else:
        print("Raccordement : toutes les valeurs publiees sont reproduites dans la "
              "tolerance preenregistree.", flush=True)


if __name__ == "__main__":
    main()
