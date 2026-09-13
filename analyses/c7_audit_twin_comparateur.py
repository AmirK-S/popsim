"""
c7_audit_twin_comparateur : le comparateur demographique de Twin est-il maigre par
construction, ou reellement battu ?

===========================================================================
PREENREGISTREMENT : resultats/audit-twin-comparateur-2026-09-13.md section 0,
ECRIT ET COMMITE AVANT ce fichier et avant le premier calcul. Predictions P1 a P6,
criteres de refutation, conventions de departage des ex aequo, definition du
comparateur ENRICHI, seuil d'effondrement (rapport < 2,0x), regle d'arret.

LA QUESTION. audit-park-armement-egal-2026-09-13.md a montre que le « comparateur
demographique » de Park est conditionne sur ONZE attributs qui rendent 98,86 % des
1 052 repondants uniques dans leur cellule, et qu'a armement egal le rapport
cible/comparateur y tombe a 1,06x. Personne n'a fait le meme examen sur Twin-2K-500,
seul jeu qui porte encore l'article avec un rapport annonce de 29,88x. Si le
comparateur de Twin est MAIGRE la ou celui de Park etait riche, notre meilleur chiffre
est flatteur par construction. Ce script tente de reproduire la chute sur Twin.

ETUDE DE RISQUE DE VIE PRIVEE sur des jeux deja publics (Twin-2K-500, archive Park et al.).
Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identifiant d'une personne, ni un
appariement individuel, ni la cellule demographique d'une personne : seuls des taux et
des distributions agregees sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / ecrire          les tables Twin, les 14 questions du bloc
                                      Demographics et les 494 items de contexte
  c7_reidentification.items_communs / graine_nom / REF_V4 / REF_V13 / DEMO
                                      les 60 items toujours renseignes de Twin
  c7_attaquant_fort.scores_hors_pli   l'attaquant fort A-LLR, hors pli, non modifie
  c7_monde_ouvert.marges_deux_regimes / roc_et_taux / compte_au_moins / pmm_depuis_demo
                                      le protocole de monde ouvert et la recette PMM
  c7_fort_monde_ouvert_ic.charger_twin  le chargeur canonique, utilise comme ASSERTION
  c7_stanford.charger_domaine / DEMO_CSV  le bloc demographique reel de Park, pour la
                                      comparaison frontale des unicites
  a2_commun.distance_hamming / bootstrap_personnes / en_codes / b2_voisins
  c7_controle_interpretabilite        la regle de decision (IC disjoints)

CE QUI EST NOUVEAU ICI, et rien d'autre :
  1. l'inventaire du bloc demographique REELLEMENT disponible sur Twin (volet 1) ;
  2. l'unicite de cellule sur Twin, bloc complet, echelle cumulee et laisse-un-de-cote,
     face a celle de Park recalculee ici meme (volet 2) ;
  3. les comparateurs ENRICHIS : echelle d'attributs, trois recettes, et le bloc
     demographie + contexte (volet 3) ;
  4. le tableau a armement egal et les rapports apparies (volet 4) ;
  5. la courbe du comparateur enrichi arme en fonction du nombre d'items (volet 5).

Aucun appel de modele de langage, aucune depense, aucun reseau. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_audit_twin_comparateur.py
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
from a2_commun import (                                                  # noqa: E402
    distance_hamming, bootstrap_personnes, en_codes, b2_voisins,
)
from c7_reidentification import (                                        # noqa: E402
    items_communs, graine_nom, REF_V4, REF_V13, DEMO,
)
from c7_attaquant_fort import scores_hors_pli, CIBLE_TWIN                # noqa: E402
from c7_monde_ouvert import (                                            # noqa: E402
    marges_deux_regimes, roc_et_taux, compte_au_moins, pmm_depuis_demo, K_PMM,
)
import c7_fort_monde_ouvert_ic as MO                                     # noqa: E402
import c7_stanford as CS                                                 # noqa: E402

GRAINE = 20260913
N_BOOTSTRAP = 2000
TOL = 1e-12
FPR_CIBLES = (0.001, 0.01)

# Volet 5. REDUCTION DECLAREE : 4 tirages d'items par k au lieu des 20 de la convention
# c7_stanford.N_TIRAGES_ITEMS, et une grille a trois points. Motif : duree.
KS_ITEMS = (20, 40, 60)
N_TIRAGES_ITEMS = 4

# Les onze attributs de Twin homologues des onze de Park, fixes au preenregistrement 0.2.
# Park : age, census_division, political_ideology, political_party, education, race,
# ethnicity, gender, income, neighborhood, sexual_orientation.
# Twin n'a ni quartier ni orientation sexuelle ni ethnicite separee de la race : les deux
# substituts sont declares ici et nommes au rapport, ils ne sont pas choisis apres coup.
PARK_HOMOLOGUE = [
    "QID13",   # age                 <- age
    "QID11",   # region              <- census_division
    "QID22",   # ideologie politique <- political_ideology
    "QID20",   # parti               <- political_party
    "QID14",   # education           <- education
    "QID15",   # race ou origine     <- race (+ ethnicity, confondues dans Twin)
    "QID12",   # sexe                <- gender
    "QID21",   # revenu              <- income
    "QID18",   # religion            <- SUBSTITUT de neighborhood
    "QID24",   # emploi              <- SUBSTITUT de sexual_orientation
    "QID17",   # statut marital      <- onziemme attribut, pour egaliser le COMPTE
]
# Analogue exact de la cellule a quatre axes preenregistree par l'audit Park.
QUATRE_AXES = ["QID12", "QID15", "QID13", "QID14"]   # genre, race, age, education

RACCORDEMENT = {
    "Twin|cible|A-LLR|top1_ferme": (0.232264, 0.0050),
    "Twin|Demographics Only|A-LLR|top1_ferme": (0.007775, 0.0020),
    "Twin|rapport cible/Demographics Only|A-LLR": (29.88, 2.00),
    "Park|bloc 11 attributs|part_seules": (0.9886, 0.0050),
}
_ecarts = []


def raccorder(cle, valeur):
    if cle not in RACCORDEMENT:
        return None
    attendu, tol = RACCORDEMENT[cle]
    ok = abs(float(valeur) - attendu) <= tol
    print(f"    [raccordement {'OK   ' if ok else 'ECART'}] {cle} : "
          f"mesure {valeur:.6f}, publie {attendu:.6f}, ecart "
          f"{abs(valeur - attendu):.6f} (tol {tol})", flush=True)
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
# 1. Departage des ex aequo : EXACT, trois conventions (preenregistrement 0.1)
# ---------------------------------------------------------------------------

def departage_exact(score, vrai_idx):
    n = score.shape[0]
    r = np.arange(n)
    vrai = score[r, vrai_idx]
    meilleur = score.max(axis=1)
    taille = (score >= meilleur[:, None] - TOL).sum(axis=1)
    dans = vrai >= meilleur - TOL
    return {"uniforme": np.where(dans, 1.0 / taille, 0.0),
            "en_faveur": dans.astype(float),
            "contre": ((score >= vrai[:, None] - TOL).sum(axis=1) == 1).astype(float),
            "taille_classe": taille}


def escalier(marge_p, correct, marge_r, n):
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
# 2. Chargement : UN bassin, partage par la cible et par TOUS les comparateurs
# ---------------------------------------------------------------------------

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
        raise SystemExit("Twin : bassin different du chargeur canonique. Audit invalide.")
    demo_x = paq["demo"]["x"]                       # (2058, 14) chaines, deja sans manquant
    cols_demo = list(paq["demo"]["colonnes_demo"])
    demo_codes = en_codes(demo_x)
    ctx_codes = en_codes(np.asarray(paq["demo"]["ctx"], dtype=object))
    return {"jeu": "Twin", "pool": pool, "vrai_idx": couverts, "n": n,
            "n_items": len(items), "items": items, "llr": "twin|llr",
            "demo_codes": demo_codes, "cols_demo": cols_demo, "ctx_codes": ctx_codes,
            "n_ctx": ctx_codes.shape[1],
            "accord": lambda x, p: 1.0 - distance_hamming(x, p),
            "cible": (f"cible : {CIBLE_TWIN}", codes[CIBLE_TWIN][:, items][couverts]),
            "demo_only": ("comparateur demographique (Demographics Only)",
                          codes[DEMO][:, items][couverts])}


def score_de(jd, x, attaque, colonnes=None):
    if attaque.startswith("A-LLR"):
        return scores_hors_pli(x, jd["pool"], jd["vrai_idx"], jd["llr"],
                               colonnes=colonnes)
    pool = jd["pool"] if colonnes is None else jd["pool"][:, colonnes]
    xx = x if colonnes is None else x[:, colonnes]
    return jd["accord"](xx, pool)


# ---------------------------------------------------------------------------
# 3. Les comparateurs ENRICHIS (preenregistrement 0.2)
# ---------------------------------------------------------------------------

def voisins_depuis_bloc(bloc_codes, pool, rng, k=K_PMM, tirage=True):
    """Recette canonique pmm_depuis_demo, generalisee a un bloc d'attributs quelconque.

    La personne elle-meme est TOUJOURS exclue de la recherche de voisins (diagonale a
    l'infini), exactement comme dans c7_monde_ouvert.pmm_depuis_demo.
    """
    dist = distance_hamming(bloc_codes, bloc_codes)
    np.fill_diagonal(dist, np.inf)
    out = np.zeros((bloc_codes.shape[0], pool.shape[1]), dtype=pool.dtype)
    for j in range(pool.shape[1]):
        out[:, j] = b2_voisins(dist, pool[:, j], k, rng, tirage=tirage)
    return out


def donneur_unique(bloc_codes, pool):
    """Comparateur « donneur » : le voisin demographique le plus proche, recopie en entier.

    Deterministe (ex aequo departages par le plus petit indice, convention declaree).
    C'est la recette qui conserve le MIEUX les modalites rares, donc a priori la plus
    dangereuse sous un attaquant pondere par la rarete.
    """
    dist = distance_hamming(bloc_codes, bloc_codes)
    np.fill_diagonal(dist, np.inf)
    return pool[np.argmin(dist, axis=1)]


# ---------------------------------------------------------------------------
# 4. Une cellule du tableau a armement egal
# ---------------------------------------------------------------------------

def cellule(jd, nom, x, attaque, lignes, volet, cle_racc=None, court=False):
    vrai_idx, n = jd["vrai_idx"], jd["n"]
    if x.shape[0] != len(vrai_idx) or x.shape[1] != jd["pool"].shape[1]:
        raise SystemExit(f"{jd['jeu']}/{nom} : forme {x.shape} hors bassin.")
    score = score_de(jd, x, attaque)
    d = departage_exact(score, vrai_idx)
    m_u, b_u, h_u = ic(d["uniforme"], f"{nom}|{attaque}|uniforme")
    m_f, b_f, h_f = ic(d["en_faveur"], f"{nom}|{attaque}|en_faveur")
    m_c, b_c, h_c = ic(d["contre"], f"{nom}|{attaque}|contre")

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
    L(ligne(volet, jd["jeu"], nom, attaque, "classe_tete_taille_mediane",
            float(np.median(d["taille_classe"])), **commun))
    L(ligne(volet, jd["jeu"], nom, attaque, "auc_monde_ouvert", float(r["auc"]), **commun))
    for c in FPR_CIBLES:
        et = f"{c*100:g}pct".replace(".", "_")
        pub = r["tpr_fpr_0_1pct"] if c == 0.001 else r["tpr_fpr_1pct"]
        L(ligne(volet, jd["jeu"], nom, attaque, f"tpr_a_fpr_{et}_np_interp", float(pub),
                fpr_cible=c, **commun))
        e = esc[c]
        if e is None:
            continue
        for k, v in e.items():
            L(ligne(volet, jd["jeu"], nom, attaque, f"tpr_a_fpr_{et}_{k}", v,
                    fpr_cible=c, **commun))

    print(f"    {nom:52s} / {attaque:16s} ferme={m_u*100:7.4f} % "
          f"[{b_u*100:.3f};{h_u*100:.3f}]  (bornes {m_c*100:.3f} / {m_f*100:.3f})  "
          f"AUC={r['auc']:.4f}", flush=True)
    if not court:
        for c in FPR_CIBLES:
            e = esc[c]
            if e is None:
                print(f"      FPR<={c*100:g}% : aucun seuil", flush=True)
            else:
                print(f"      FPR<={c*100:g}% : escalier {e['tpr_escalier']*100:7.4f} % "
                      f"({e['fp_absolus']} FP, {e['vraies_detections_absolues']} vraies)",
                      flush=True)
    if cle_racc:
        raccorder(cle_racc, m_u)
    return {"indic": d["uniforme"], "top1": m_u, "bas": b_u, "haut": h_u,
            "auc": float(r["auc"]),
            "tpr": {c: (esc[c]["tpr_escalier"] if esc[c] else 0.0) for c in FPR_CIBLES}}


def rapport_apparie(a, b, cle):
    va, vb = np.asarray(a, float), np.asarray(b, float)
    rng = np.random.default_rng([GRAINE, 51, graine_nom(cle)])
    nn = len(va)
    idx = rng.integers(0, nn, size=(N_BOOTSTRAP, nn))
    ma, mb = va[idx].mean(axis=1), vb[idx].mean(axis=1)
    rr = np.where(mb > 0, ma / np.maximum(mb, 1e-12), np.nan)
    diff = ma - mb
    return {"rapport": float(va.mean() / vb.mean()) if vb.mean() > 0 else np.inf,
            "rapport_bas": float(np.nanpercentile(rr, 2.5)),
            "rapport_haut": float(np.nanpercentile(rr, 97.5)),
            "ecart_points": float(va.mean() - vb.mean()),
            "ecart_bas": float(np.percentile(diff, 2.5)),
            "ecart_haut": float(np.percentile(diff, 97.5))}


# ---------------------------------------------------------------------------
# 5. Unicite d'un bloc d'attributs
# ---------------------------------------------------------------------------

def unicite(bloc_codes):
    """(n cellules, n seules, part seules, plafond moyenne(1/|cellule|), tailles)."""
    cles = [tuple(r.tolist()) for r in bloc_codes]
    comptes = pd.Series(cles).value_counts()
    t = np.array([comptes[c] for c in cles], dtype=float)
    return (int(len(comptes)), int((t == 1).sum()), float((t == 1).mean()),
            float(np.mean(1.0 / t)), t)


def volet_unicite(jd, lignes):
    """Volet 2 : l'unicite de cellule sur Twin, face a celle de Park recalculee ici.

    AUCUNE cellule d'aucune personne n'est imprimee ni ecrite : seules la distribution
    des tailles et les parts agregees sortent.
    """
    print("\n" + "=" * 78, flush=True)
    print("VOLET 2 — unicite des cellules demographiques : Twin face a Park", flush=True)
    print("=" * 78, flush=True)
    volet = "2 unicite"
    dc, cols = jd["demo_codes"], jd["cols_demo"]
    n = dc.shape[0]
    L = lignes.append
    mods = [int(len(np.unique(dc[:, j]))) for j in range(dc.shape[1])]

    for j, c in enumerate(cols):
        L(ligne(volet, "Twin", f"attribut {c}", "-", "n_modalites", float(mods[j]),
                n_pool=n))
    print(f"  bloc COMPLET de Twin : {len(cols)} attributs "
          f"({', '.join(f'{c}({m})' for c, m in zip(cols, mods))})", flush=True)

    blocs = {"bloc complet Twin (14 attributs)": list(range(len(cols))),
             "bloc homologue de Park (11 attributs)":
                 [cols.index(c) for c in PARK_HOMOLOGUE if c in cols],
             "cellule a 4 axes (genre x race x age x education)":
                 [cols.index(c) for c in QUATRE_AXES if c in cols]}
    part_complet = None
    for nom, idx in blocs.items():
        if len(idx) == 0:
            continue
        nc, ns, ps, plaf, t = unicite(dc[:, idx])
        if nom.startswith("bloc complet"):
            part_complet = ps
        commun = dict(n_pool=n, n_axes=len(idx),
                      axes="+".join(cols[i] for i in idx))
        for m, v in (("n_cellules_distinctes", float(nc)),
                     ("n_personnes_seules_dans_leur_cellule", float(ns)),
                     ("part_personnes_seules_dans_leur_cellule", ps),
                     ("plafond_cellule_seule_moyenne_un_sur_taille", plaf),
                     ("taille_cellule_mediane", float(np.median(t))),
                     ("taille_cellule_max", float(t.max()))):
            L(ligne(volet, "Twin", nom, "-", m, v, **commun))
        print(f"    {nom:50s} : {nc:5d} cellules, {ns:5d}/{n} seules "
              f"({ps*100:6.2f} %), plafond {plaf*100:6.2f} %, "
              f"taille mediane {np.median(t):.0f}, max {t.max():.0f}", flush=True)

    # echelle cumulee : combien d'attributs suffisent a rendre les gens uniques ?
    print("  echelle cumulee (part de personnes seules, k premiers attributs) :",
          flush=True)
    for k in range(1, len(cols) + 1):
        nck, nsk, psk, plafk, _ = unicite(dc[:, :k])
        L(ligne(volet, "Twin", f"{k} premiers attributs", "-",
                "part_personnes_seules_dans_leur_cellule", psk, n_cellules=float(nck),
                plafond=plafk, n_axes=k, axes="+".join(cols[:k]), n_pool=n))
        print(f"    k={k:2d} : {psk*100:6.2f} %  (plafond {plafk*100:6.2f} %)", flush=True)

    # laisse-un-de-cote sur le bloc complet
    print("  laisse-un-de-cote (part de personnes seules quand l'attribut est retire) :",
          flush=True)
    for j, c in enumerate(cols):
        garde = [i for i in range(len(cols)) if i != j]
        _, _, psj, plafj, _ = unicite(dc[:, garde])
        L(ligne(volet, "Twin", f"bloc sans {c}", "-",
                "part_personnes_seules_dans_leur_cellule", psj, plafond=plafj,
                attribut_retire=c, n_pool=n, chute_points=(part_complet - psj)))
        print(f"    sans {c:8s} : {psj*100:6.2f} %  "
              f"(chute {(part_complet - psj)*100:+6.2f} pt)", flush=True)

    # ---- Park, recalcule ici meme pour que la comparaison soit frontale ----
    print("  Park (archive Park et al., bloc GSS), RECALCULE ici :", flush=True)
    ordre, _, _, _ = CS.charger_domaine("gss")
    demo_p = pd.read_csv(CS.DEMO_CSV).set_index("email").loc[ordre]
    axes_p = [c for c in demo_p.columns if c != "email"]
    dcp = en_codes(demo_p[axes_p].astype(str).to_numpy(dtype=object))
    ncp, nsp, psp, plafp, tp = unicite(dcp)
    mods_p = [int(len(np.unique(dcp[:, j]))) for j in range(dcp.shape[1])]
    commun_p = dict(n_pool=int(dcp.shape[0]), n_axes=len(axes_p),
                    axes="+".join(axes_p),
                    modalites="x".join(str(m) for m in mods_p))
    for m, v in (("n_cellules_distinctes", float(ncp)),
                 ("n_personnes_seules_dans_leur_cellule", float(nsp)),
                 ("part_personnes_seules_dans_leur_cellule", psp),
                 ("plafond_cellule_seule_moyenne_un_sur_taille", plafp),
                 ("taille_cellule_mediane", float(np.median(tp)))):
        L(ligne(volet, "Park GSS", f"bloc complet fourni a l'agent ({len(axes_p)})",
                "-", m, v, **commun_p))
    print(f"    {len(axes_p)} attributs ({', '.join(f'{c}({m})' for c, m in zip(axes_p, mods_p))})",
          flush=True)
    print(f"    {ncp} cellules, {nsp}/{dcp.shape[0]} seules ({psp*100:.2f} %), "
          f"plafond {plafp*100:.2f} %", flush=True)
    raccorder("Park|bloc 11 attributs|part_seules", psp)
    return part_complet, psp


# ---------------------------------------------------------------------------
# 6. Volet 5 : courbe du comparateur enrichi arme en fonction du nombre d'items
# ---------------------------------------------------------------------------

def volet_items(jd, lignes, conditions):
    print("\n" + "=" * 78, flush=True)
    print(f"VOLET 5 — Twin : taux ARME en fonction du nombre d'items retenus "
          f"(bassin constant, {N_TIRAGES_ITEMS} tirages par k, REDUCTION DECLAREE)",
          flush=True)
    print("=" * 78, flush=True)
    volet = "5 courbe items"
    n_items = jd["n_items"]
    rng = np.random.default_rng([GRAINE, 61])
    for k in KS_ITEMS:
        k = min(k, n_items)
        tirages = ([np.arange(n_items)] if k == n_items
                   else [np.sort(rng.choice(n_items, k, replace=False))
                         for _ in range(N_TIRAGES_ITEMS)])
        par_cond = {}
        for nom, x in conditions:
            vf, vn = [], []
            for col in tirages:
                vf.append(departage_exact(score_de(jd, x, "A-LLR", colonnes=col),
                                          jd["vrai_idx"])["uniforme"].mean())
                vn.append(departage_exact(score_de(jd, x, "naif", colonnes=col),
                                          jd["vrai_idx"])["uniforme"].mean())
            for att, vv in (("A-LLR (hors pli)", vf), ("naif (Hamming)", vn)):
                v = np.asarray(vv, dtype=float)
                lignes.append(ligne(
                    volet, jd["jeu"], nom, att, "top1_ferme_uniforme_moyenne_tirages",
                    float(v.mean()), float(v.min()), float(v.max()), k_items=k,
                    n_tirages_items=len(tirages), n_pool=jd["n"], hasard=1.0 / jd["n"],
                    note="ic_bas/ic_haut = min/max sur les tirages d'items, PAS un IC"))
            par_cond[nom] = (float(np.mean(vf)), float(np.mean(vn)))
        nc, nb = conditions[0][0], conditions[1][0]
        rap = par_cond[nc][0] / par_cond[nb][0] if par_cond[nb][0] > 0 else np.inf
        lignes.append(ligne(volet, jd["jeu"], "rapport cible / comparateur enrichi",
                            "A-LLR (hors pli)", "rapport_top1_ferme", float(rap),
                            k_items=k, n_pool=jd["n"]))
        print(f"  k={k:3d} items : comparateur enrichi arme {par_cond[nb][0]*100:7.4f} % "
              f"(naif {par_cond[nb][1]*100:6.4f} %) | cible armee "
              f"{par_cond[nc][0]*100:7.4f} % (naif {par_cond[nc][1]*100:6.4f} %) | "
              f"rapport {rap:6.2f}x", flush=True)


# ---------------------------------------------------------------------------
# 6bis. Volet 7 : les items attaques portent-ils la demographie ?
# ---------------------------------------------------------------------------

def volet_determination(jd, lignes):
    """Part de la modalite majoritaire des items humains dans les groupes d'un attribut,
    contre des groupes ALEATOIRES de meme taille. Mesure identique a celle de
    audit-park-armement-egal §5.2, pour que les deux jeux soient lisibles cote a cote.

    C'est le mecanisme : un bloc de quasi-identifiants n'est decodable depuis les items
    attaques que si ces items sont determines par la demographie. Aucune valeur
    individuelle n'est imprimee ni ecrite.
    """
    print("\n" + "=" * 78, flush=True)
    print("VOLET 7 — les 60 items attaques portent-ils la demographie de Twin ?",
          flush=True)
    print("=" * 78, flush=True)
    volet = "7 determination des items"
    dc, cols, pool = jd["demo_codes"], jd["cols_demo"], jd["pool"]
    n = dc.shape[0]
    rngp = np.random.default_rng([GRAINE, 72])
    pire = None
    for j, a in enumerate(cols):
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
        lignes.append(ligne(volet, jd["jeu"], f"items humains | {a}", "-",
                            "part_modalite_majoritaire", mo, temoin_aleatoire=mt,
                            ecart_points=(mo - mt),
                            n_modalites=int(len(np.unique(col_a))), n_pool=n))
        if pire is None or (mo - mt) > pire[1]:
            pire = (a, mo - mt)
        print(f"    {a:8s} : {mo*100:5.2f} % contre temoin {mt*100:5.2f} % "
              f"(ecart {(mo-mt)*100:+5.2f} pt)", flush=True)
    print(f"  ecart MAXIMAL sur les 14 attributs : {pire[0]} a {pire[1]*100:+.2f} pt",
          flush=True)
    lignes.append(ligne(volet, jd["jeu"], "ecart maximal sur les 14 attributs", "-",
                        "ecart_points_max", float(pire[1]), attribut=pire[0], n_pool=n,
                        note="a comparer aux +4,91 pt de Park (sexual_orientation), "
                             "audit-park-armement-egal-2026-09-13 §5.2"))
    return pire


# ---------------------------------------------------------------------------
# 7. main
# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes = []
    jd = charger_twin()
    print("\n" + "=" * 78, flush=True)
    print(f"Twin : {jd['n']} personnes, {jd['n_items']} items, "
          f"{len(jd['cols_demo'])} attributs demographiques, {jd['n_ctx']} items de "
          f"contexte ; bassin unique partage par TOUTES les conditions", flush=True)
    print("=" * 78, flush=True)

    # ---- VOLET 1 : inventaire du bloc, ecrit avant tout taux ----
    volet1 = "1 inventaire du bloc"
    lignes.append(ligne(volet1, "Twin", "bloc demographique disponible", "-",
                        "n_attributs", float(len(jd["cols_demo"])),
                        axes="+".join(jd["cols_demo"]), n_pool=jd["n"],
                        n_items_contexte=jd["n_ctx"],
                        note="questions dont BlockName vaut Demographics dans "
                             "question_catalog.json ; aucune n'est reposee en vague 4"))

    # ---- VOLET 2 : unicite ----
    part_twin, part_park = volet_unicite(jd, lignes)

    # ---- VOLET 3 : construction des comparateurs enrichis ----
    print("\n" + "=" * 78, flush=True)
    print("VOLET 3 — construction des comparateurs enrichis (aucun modele de langage)",
          flush=True)
    print("=" * 78, flush=True)
    dc, cols = jd["demo_codes"], jd["cols_demo"]
    pool = jd["pool"]
    cv = jd["vrai_idx"]
    comparateurs = [jd["demo_only"]]

    echelle = [("4 axes (genre x race x age x education)",
                [cols.index(c) for c in QUATRE_AXES if c in cols]),
               ("8 premiers attributs", list(range(8))),
               ("11 attributs homologues de Park",
                [cols.index(c) for c in PARK_HOMOLOGUE if c in cols]),
               ("14 attributs, bloc complet", list(range(len(cols))))]
    for nom, idx in echelle:
        rng = np.random.default_rng([GRAINE, 81, graine_nom(nom)])
        x = voisins_depuis_bloc(dc[:, idx], pool, rng, K_PMM, tirage=True)
        comparateurs.append((f"enrichi PMM k=10 | {nom} ({len(idx)})", x[cv]))
        print(f"  construit : PMM k=10 sur {nom} ({len(idx)} attributs)", flush=True)

    idx_full = list(range(len(cols)))
    rng = np.random.default_rng([GRAINE, 82])
    comparateurs.append(("enrichi MODE k=10 | 14 attributs",
                         voisins_depuis_bloc(dc[:, idx_full], pool, rng, K_PMM,
                                             tirage=False)[cv]))
    print("  construit : MODE k=10 sur les 14 attributs", flush=True)
    comparateurs.append(("enrichi DONNEUR k=1 | 14 attributs",
                         donneur_unique(dc[:, idx_full], pool)[cv]))
    print("  construit : DONNEUR k=1 sur les 14 attributs", flush=True)

    bloc_dc = np.concatenate([dc, jd["ctx_codes"]], axis=1)
    rng = np.random.default_rng([GRAINE, 83])
    comparateurs.append((f"enrichi PMM k=10 | 14 attributs + {jd['n_ctx']} items de "
                         f"contexte", voisins_depuis_bloc(bloc_dc, pool, rng, K_PMM,
                                                          tirage=True)[cv]))
    print(f"  construit : PMM k=10 sur 14 attributs + {jd['n_ctx']} items de contexte",
          flush=True)

    # temoin canonique du depot, pour raccordement de recette
    rng = np.random.default_rng([GRAINE, 32])
    comparateurs.append(("(temoin) PMM k=10 canonique c7_monde_ouvert",
                         pmm_depuis_demo(dc, pool, rng)[cv]))

    # ---- VOLET 4 : tableau a armement egal ----
    print("\n" + "=" * 78, flush=True)
    print("VOLET 4 — tableau a armement egal, bassin strictement constant", flush=True)
    print("=" * 78, flush=True)
    volet = "4 armement egal"
    nom_cible, x_cible = jd["cible"]
    print("  [cible]", flush=True)
    r_cible_n = cellule(jd, nom_cible, x_cible, "naif (Hamming)", lignes, volet)
    r_cible_f = cellule(jd, nom_cible, x_cible, "A-LLR (hors pli)", lignes, volet,
                        "Twin|cible|A-LLR|top1_ferme")

    print("  [comparateurs, meme bassin, meme attaque, meme convention]", flush=True)
    res = {}
    for nom_c, x_c in comparateurs:
        racc = ("Twin|Demographics Only|A-LLR|top1_ferme"
                if nom_c.startswith("comparateur demographique") else None)
        rn = cellule(jd, nom_c, x_c, "naif (Hamming)", lignes, volet, court=True)
        rf = cellule(jd, nom_c, x_c, "A-LLR (hors pli)", lignes, volet, racc, court=True)
        res[nom_c] = (rn, rf)

    print("\n  [rapports apparies et controle d'interpretabilite]", flush=True)
    meilleur = None
    for nom_c, (rn, rf) in res.items():
        for att, rc, kb in (("naif (Hamming)", r_cible_n, rn),
                            ("A-LLR (hors pli)", r_cible_f, rf)):
            r = rapport_apparie(rc["indic"], kb["indic"], f"{nom_c}|{att}")
            passe = bool(rc["bas"] > kb["haut"])
            lignes.append(ligne(
                "4bis rapport et controle", jd["jeu"], f"{nom_cible} vs {nom_c}", att,
                "rapport_top1_ferme", r["rapport"], r["rapport_bas"], r["rapport_haut"],
                ecart_points=r["ecart_points"], ecart_bas=r["ecart_bas"],
                ecart_haut=r["ecart_haut"], cible_top1=rc["top1"],
                cible_ic_bas=rc["bas"], cible_ic_haut=rc["haut"],
                comparateur_top1=kb["top1"], comparateur_ic_bas=kb["bas"],
                comparateur_ic_haut=kb["haut"],
                controle_interpretabilite_passe=float(passe), n_pool=jd["n"],
                note="bootstrap APPARIE ; controle = regle de "
                     "c7_controle_interpretabilite (IC disjoints), meme attaque, "
                     "meme bassin"))
            rap_tpr = (rc["tpr"][0.01] / kb["tpr"][0.01]
                       if kb["tpr"][0.01] > 0 else np.inf)
            lignes.append(ligne(
                "4bis rapport et controle", jd["jeu"], f"{nom_cible} vs {nom_c}", att,
                "rapport_tpr_a_fpr_1pct_escalier", float(rap_tpr),
                cible_tpr=rc["tpr"][0.01], comparateur_tpr=kb["tpr"][0.01],
                n_pool=jd["n"]))
            print(f"    [{att:16s}] {nom_c:52s} rapport {r['rapport']:8.3f}x "
                  f"[{r['rapport_bas']:7.3f};{r['rapport_haut']:8.3f}] ; ecart "
                  f"{r['ecart_points']*100:+7.2f} pt ; controle "
                  f"{'PASSE' if passe else 'ECHEC'} ; TPR@1% {rap_tpr:7.2f}x", flush=True)
            if att.startswith("A-LLR") and nom_c.startswith("comparateur demographique"):
                raccorder("Twin|rapport cible/Demographics Only|A-LLR", r["rapport"])
        if not nom_c.startswith("(temoin)"):
            if meilleur is None or rf["top1"] > meilleur[1]["top1"]:
                meilleur = (nom_c, rf, res[nom_c][0])

    # le rapport de tete est celui contre le comparateur LE PLUS FORT (preenr. 0.5)
    nom_m, rf_m, _ = meilleur
    r_m = rapport_apparie(r_cible_f["indic"], rf_m["indic"], f"TETE|{nom_m}")
    passe_m = bool(r_cible_f["bas"] > rf_m["haut"])
    lignes.append(ligne(
        "6 verdict", jd["jeu"], f"{nom_cible} vs COMPARATEUR LE PLUS FORT", "A-LLR (hors pli)",
        "rapport_top1_ferme_DE_TETE", r_m["rapport"], r_m["rapport_bas"],
        r_m["rapport_haut"], comparateur_retenu=nom_m, cible_top1=r_cible_f["top1"],
        comparateur_top1=rf_m["top1"], cible_ic_bas=r_cible_f["bas"],
        cible_ic_haut=r_cible_f["haut"], comparateur_ic_bas=rf_m["bas"],
        comparateur_ic_haut=rf_m["haut"], ecart_points=r_m["ecart_points"],
        controle_interpretabilite_passe=float(passe_m), n_pool=jd["n"],
        seuil_effondrement=2.0, seuil_tenue=5.0,
        note="comparateur LE PLUS FORT parmi tous ceux mesures, temoin exclu ; "
             "seuils du preenregistrement 0.4"))
    print(f"\n  >>> COMPARATEUR LE PLUS FORT : {nom_m} a {rf_m['top1']*100:.4f} %", flush=True)
    print(f"  >>> RAPPORT DE TETE : {r_m['rapport']:.3f}x "
          f"[{r_m['rapport_bas']:.3f};{r_m['rapport_haut']:.3f}] ; "
          f"seuil de tenue 5,0x ; seuil d'effondrement 2,0x ; controle "
          f"{'PASSE' if passe_m else 'ECHEC'}", flush=True)

    # ---- VOLET 5 : courbe items, cible contre le comparateur le plus fort ----
    x_m = dict(comparateurs)[nom_m]
    volet_items(jd, lignes, [(nom_cible, x_cible), (nom_m, x_m)])

    # ---- VOLET 7 : les items attaques portent-ils la demographie ? ----
    volet_determination(jd, lignes)

    lignes.append(ligne("6 verdict", "comparaison frontale", "part seules dans leur "
                        "cellule exacte", "-", "Twin_bloc_complet", part_twin,
                        park_bloc_complet=part_park,
                        ecart_points=(part_twin - part_park)))

    # Part du plafond de cellule reellement atteinte : la contraste structurel de tete.
    _, _, _, plaf_twin, _ = unicite(jd["demo_codes"])
    lignes.append(ligne("6 verdict", jd["jeu"], "part du plafond de cellule atteinte",
                        "A-LLR (hors pli)", "top1_sur_plafond",
                        float(rf_m["top1"] / plaf_twin), plafond=plaf_twin,
                        top1_comparateur=rf_m["top1"], comparateur_retenu=nom_m,
                        n_pool=jd["n"],
                        note="Park : 0,851711 / 0,994300 = 85,66 % du plafond, "
                             "audit-park-armement-egal-2026-09-13 §5.3"))
    print(f"\n  >>> part du plafond de cellule atteinte par le comparateur le plus fort : "
          f"{rf_m['top1'] / plaf_twin * 100:.4f} % (plafond {plaf_twin*100:.2f} %)",
          flush=True)

    T1.ecrire(lignes, "c7-audit-twin-comparateur.csv")
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
