"""
c7_loi_distance : le taux de liaison entre deux jumeaux d'une meme personne est-il une
fonction decroissante d'une DISTANCE ENTRE LES PIPELINES qui les ont produits ?

===========================================================================
PREENREGISTREMENT : resultats/c7-loi-distance-preenregistrement.md, ecrit le
12 septembre 2026 AVANT ce fichier et AVANT tout calcul de paire. La distance (section 1
du preenregistrement), le tableau des descripteurs (section 3), les exclusions (section 2),
la regle de decision et les predictions par jeu (section 5) y sont figes.

ETUDE DE RISQUE DE VIE PRIVEE sur deux jeux deja publics (Twin-2K-500 ; archive Park et al.,
OSF t6g7k). Ce script ne calcule, n'imprime et n'ecrit JAMAIS l'identite, le pid ou
l'identifiant participant_XXXX d'une personne retrouvee, ni aucun appariement individuel.
Seuls des taux agreges sortent dans resultats/.

AUCUN APPEL RESEAU, AUCUN APPEL DE MODELE, AUCUNE DEPENSE, AUCUNE GENERATION DE JUMEAU.
Lecture seule sur data/. Aucun script existant n'est modifie.
Sorties autorisees UNIQUEMENT : resultats/c7-loi-distance.csv,
resultats/c7-loi-distance-resultats.md (redige a la main a partir de cette sortie).

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                              les tables Twin-2K-500
  c7_reidentification.rangs_attaque              l'attaque de reidentification (Hamming,
                                                  ex aequo departages, candidats melanges)
  c7_reidentification.items_communs              les items toujours renseignes
  c7_reidentification.graine_nom / REF_V4 / REF_V13 / DEMO / N_BOOTSTRAP
  a2_commun.bootstrap_personnes                  l'IC 95 % par reechantillonnage de personnes
  c7_controle_interpretabilite.controle_avant_interpretation
                                                  le controle de fidelite prealable,
                                                  ELIMINATOIRE (section 6 du preenregistrement)
  c7_stanford.charger_domaine / coder_categoriel_commun / accord_categoriel /
             rangs_depuis_accord / VAGUE1 / DEMO_COND
                                                  le bloc GSS de l'archive Park et al.

CE QUI EST NOUVEAU ICI, et rien d'autre :
  - le tableau des descripteurs de pipeline et la distance d (Hamming sur descripteurs) ;
  - l'attaque symetrique a bassin et items CONSTANTS entre toutes les paires d'un jeu ;
  - le bootstrap conjoint sur les personnes, qui propage l'incertitude jusqu'au rho ;
  - la transposition declaree du controle de fidelite a l'archive Park et al. ;
  - la correlation partielle de rang a fidelite controlee (test A du preenregistrement).

Usage : .venv/bin/python analyses/c7_loi_distance.py
===========================================================================
"""

import itertools
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from scipy.stats import rankdata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                    # noqa: E402
import c7_stanford as S                                                    # noqa: E402
from a2_commun import bootstrap_personnes                                  # noqa: E402
from c7_reidentification import (                                          # noqa: E402
    rangs_attaque, items_communs, graine_nom, REF_V4, REF_V13, DEMO, N_BOOTSTRAP,
)
from c7_controle_interpretabilite import (                                 # noqa: E402
    controle_avant_interpretation, EchecControleInterpretabilite,
)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
GRAINE = 20260912
N_BOOT_RHO = 2000


# ---------------------------------------------------------------------------
# 1. LA DISTANCE : descripteurs figes au preenregistrement, section 3.
#    Aucune sortie de jumeau, aucun accord, aucun taux n'entre ici.
# ---------------------------------------------------------------------------

DESCRIPTEURS = ["modele", "gabarit", "decodage", "raisonnement", "format_persona",
                "bloc_demo", "bloc_enquete", "bloc_entretien", "bloc_autodesc"]

PIPELINES_TWIN = {
    "Demographics Only - GPT4.1-mini": dict(
        modele="gpt41-mini", gabarit="standard", decodage="T0", raisonnement="non",
        format_persona="champs", bloc_demo=1, bloc_enquete=0, bloc_entretien=0,
        bloc_autodesc=0),
    "JSON Persona - GPT4.1": dict(
        modele="gpt41", gabarit="standard", decodage="T0", raisonnement="non",
        format_persona="json", bloc_demo=1, bloc_enquete=1, bloc_entretien=0,
        bloc_autodesc=0),
    "Text Persona - GPT4.1-mini": dict(
        modele="gpt41-mini", gabarit="standard", decodage="T0", raisonnement="non",
        format_persona="texte", bloc_demo=1, bloc_enquete=1, bloc_entretien=0,
        bloc_autodesc=0),
    "Text Persona (Default Temperature) - GPT4.1-mini": dict(
        modele="gpt41-mini", gabarit="standard", decodage="defaut", raisonnement="non",
        format_persona="texte", bloc_demo=1, bloc_enquete=1, bloc_entretien=0,
        bloc_autodesc=0),
    "Text Persona (Reasoning) - GPT4.1-mini": dict(
        modele="gpt41-mini", gabarit="standard", decodage="T0", raisonnement="oui",
        format_persona="texte", bloc_demo=1, bloc_enquete=1, bloc_entretien=0,
        bloc_autodesc=0),
    "Text Persona (Repeating Questions) - GPT4.1-mini": dict(
        modele="gpt41-mini", gabarit="repetition", decodage="T0", raisonnement="non",
        format_persona="texte", bloc_demo=1, bloc_enquete=1, bloc_entretien=0,
        bloc_autodesc=0),
    "Text Persona - Gemini-Flash2.5": dict(
        modele="gemini-flash2.5", gabarit="standard", decodage="T0", raisonnement="non",
        format_persona="texte", bloc_demo=1, bloc_enquete=1, bloc_entretien=0,
        bloc_autodesc=0),
}

# Park et al., bloc GSS : modele, gabarit, decodage, raisonnement et format de rendu sont
# identiques partout (une equipe, un harnais) -> ces cinq descripteurs valent 0 partout et
# ne peuvent creer aucun gradient. Seuls les quatre blocs d'information varient.
_PARK_CONST = dict(modele="gpt4o", gabarit="standard", decodage="defaut",
                   raisonnement="non", format_persona="texte")
PIPELINES_PARK = {
    "demographique": dict(_PARK_CONST, bloc_demo=1, bloc_enquete=0, bloc_entretien=0,
                          bloc_autodesc=0),
    "persona": dict(_PARK_CONST, bloc_demo=0, bloc_enquete=0, bloc_entretien=0,
                    bloc_autodesc=1),
    "enquete": dict(_PARK_CONST, bloc_demo=0, bloc_enquete=1, bloc_entretien=0,
                    bloc_autodesc=0),
    "entretien": dict(_PARK_CONST, bloc_demo=0, bloc_enquete=0, bloc_entretien=1,
                      bloc_autodesc=0),
    "composite": dict(_PARK_CONST, bloc_demo=0, bloc_enquete=1, bloc_entretien=1,
                      bloc_autodesc=0),
}


def distance_pipeline(p, q):
    """d(P, Q) = nombre de descripteurs sur lesquels les deux pipelines different.

    Hamming entiere sur les neuf descripteurs de la section 1 du preenregistrement, poids
    egaux, calculee UNIQUEMENT a partir des metadonnees publiees par l'equipe d'origine.
    """
    return int(sum(1 for k in DESCRIPTEURS if p[k] != q[k]))


def descripteurs_differents(p, q):
    return "+".join(k for k in DESCRIPTEURS if p[k] != q[k]) or "aucun"


# ---------------------------------------------------------------------------
# 2. Attaque symetrique, bassin et items constants
# ---------------------------------------------------------------------------

def top1_symetrique_hamming(X, Y, nom):
    """Vecteur par personne du top-1 symetrique entre deux jeux de codes alignes.

    X et Y sont (n, m), la ligne i de chacun etant le jumeau de la MEME personne i, et le
    bassin de candidats est la population entiere des n lignes de l'autre configuration :
    bassin et items sont donc identiques pour toutes les paires d'un jeu, ce que la mission
    exige (le taux en depend mecaniquement). Moyenne des deux sens, via rangs_attaque.
    """
    n = X.shape[0]
    vrai = np.arange(n)
    _, t1_f, _ = rangs_attaque(X, Y, vrai, np.random.default_rng(
        [GRAINE, graine_nom(nom + "|aller")]))
    _, t1_r, _ = rangs_attaque(Y, X, vrai, np.random.default_rng(
        [GRAINE, graine_nom(nom + "|retour")]))
    return (t1_f + t1_r) / 2.0


def top1_symetrique_accord(A_xy, A_yx, nom):
    """Idem, mais a partir de deux matrices d'accord deja calculees (bloc GSS de Park)."""
    n = A_xy.shape[0]
    vrai = np.arange(n)
    _, t1_f, _ = S.rangs_depuis_accord(A_xy, vrai, np.random.default_rng(
        [GRAINE, graine_nom(nom + "|aller")]))
    _, t1_r, _ = S.rangs_depuis_accord(A_yx, vrai, np.random.default_rng(
        [GRAINE, graine_nom(nom + "|retour")]))
    return (t1_f + t1_r) / 2.0


# ---------------------------------------------------------------------------
# 3. Statistique : rho de Spearman, IC bootstrap conjoint, partielle a fidelite controlee
# ---------------------------------------------------------------------------

def spearman(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    ra, rb = rankdata(a), rankdata(b)
    if np.std(ra) < 1e-12 or np.std(rb) < 1e-12:
        return np.nan
    return float(np.corrcoef(ra, rb)[0, 1])


def spearman_partiel(x, y, z):
    """Correlation partielle de rang entre x et y, a z controle (formule standard sur les
    correlations de Spearman). Test A du preenregistrement : z = fidelite de la paire."""
    rxy, rxz, ryz = spearman(x, y), spearman(x, z), spearman(y, z)
    den = np.sqrt(max(1e-12, (1 - rxz ** 2) * (1 - ryz ** 2)))
    return float((rxy - rxz * ryz) / den)


def ic_rho_bootstrap(indicateurs, d, fid, n_personnes, graine):
    """IC 95 % de rho (brut et partiel) par bootstrap sur les PERSONNES.

    Les MEMES personnes sont retirees simultanement pour toutes les paires du jeu : la
    correlation entre paires (elles partagent les memes individus) est donc prise en
    compte, au lieu d'etre ignoree par un bootstrap paire par paire.
    `indicateurs` : (n_paires, n_personnes), top-1 par personne pour chaque paire.
    """
    rng = np.random.default_rng(graine)
    M = np.asarray(indicateurs)
    rhos, rhos_p = [], []
    for _ in range(N_BOOT_RHO):
        idx = rng.integers(0, n_personnes, n_personnes)
        taux = M[:, idx].mean(axis=1)
        rhos.append(spearman(d, taux))
        rhos_p.append(spearman_partiel(d, taux, fid))
    rhos = np.array(rhos, float)
    rhos_p = np.array(rhos_p, float)
    return (float(np.nanpercentile(rhos, 2.5)), float(np.nanpercentile(rhos, 97.5)),
            float(np.nanpercentile(rhos_p, 2.5)), float(np.nanpercentile(rhos_p, 97.5)))


def verdict_jeu(rho, bas, haut):
    """Regle de decision preenregistree, section 5."""
    if not np.isfinite(rho):
        return "non calculable"
    if rho > -0.20:
        return "REFUTEE (plate)"
    if rho <= -0.50 and not (bas <= 0 <= haut):
        return "SOUTENUE"
    return "INDECISE"


# ---------------------------------------------------------------------------
# 4. Twin-2K-500
# ---------------------------------------------------------------------------

def bloc_twin(lignes):
    print("\n" + "=" * 78, flush=True)
    print("TWIN-2K-500", flush=True)
    print("=" * 78, flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    configs = list(PIPELINES_TWIN)
    manquantes = [c for c in configs if c not in codes]
    if manquantes:
        raise RuntimeError(f"configurations absentes des donnees : {manquantes}")

    # Bassin et items CONSTANTS : les items sont ceux renseignes a 100 % chez TOUTES les
    # configurations retenues et chez les deux references humaines -> un seul jeu d'items
    # pour toutes les paires (preenregistrement section 4).
    items = items_communs(codes, [REF_V4, REF_V13] + configs)
    n = paq["n"]
    ech = np.arange(n)
    print(f"bassin constant : {n} personnes | items constants : {len(items)}", flush=True)

    # --- controle d'interpretabilite, ELIMINATOIRE, avant toute paire ---
    print("\n--- controle d'interpretabilite (eliminatoire) ---", flush=True)
    retenues, fidelite = [], {}
    for c in configs:
        X = codes[c][:, items]
        try:
            diag = controle_avant_interpretation(ech, items, X, c, paq=paq)
            retenues.append(c)
            fidelite[c] = diag["candidat_top1"]
            print(f"  PASSE   {c:52s} top1 vs humains {diag['candidat_top1']*100:6.2f} % "
                  f"[{diag['candidat_ic'][0]*100:.2f};{diag['candidat_ic'][1]*100:.2f}] "
                  f"| baseline {diag['baseline_top1']*100:.2f} % "
                  f"[{diag['baseline_ic'][0]*100:.2f};{diag['baseline_ic'][1]*100:.2f}]",
                  flush=True)
            lignes.append({"jeu": "Twin-2K-500", "bloc": "controle", "serie": c,
                           "passe": 1, "fidelite_top1": diag["candidat_top1"],
                           "fidelite_bas": diag["candidat_ic"][0],
                           "fidelite_haut": diag["candidat_ic"][1],
                           "baseline_top1": diag["baseline_top1"],
                           "baseline_bas": diag["baseline_ic"][0],
                           "baseline_haut": diag["baseline_ic"][1],
                           "n_pool": n, "n_items": len(items)})
        except EchecControleInterpretabilite as exc:
            d = getattr(exc, "diagnostic", None)
            print(f"  EXCLUE  {c:52s} " + (
                f"top1 vs humains {d['candidat_top1']*100:6.2f} % "
                f"[{d['candidat_ic'][0]*100:.2f};{d['candidat_ic'][1]*100:.2f}] "
                f"| baseline {d['baseline_top1']*100:.2f} % "
                f"[{d['baseline_ic'][0]*100:.2f};{d['baseline_ic'][1]*100:.2f}]"
                if d else str(exc).splitlines()[0]), flush=True)
            fidelite[c] = d["candidat_top1"] if d else np.nan
            lignes.append({"jeu": "Twin-2K-500", "bloc": "controle", "serie": c,
                           "passe": 0,
                           "fidelite_top1": d["candidat_top1"] if d else np.nan,
                           "fidelite_bas": d["candidat_ic"][0] if d else np.nan,
                           "fidelite_haut": d["candidat_ic"][1] if d else np.nan,
                           "baseline_top1": d["baseline_top1"] if d else np.nan,
                           "n_pool": n, "n_items": len(items)})
    print(f"  -> {len(retenues)}/{len(configs)} configurations retenues", flush=True)

    # --- les paires ---
    print("\n--- paires (attaque symetrique, bassin et items constants) ---", flush=True)
    return _paires(lignes, "Twin-2K-500", PIPELINES_TWIN, retenues, configs, fidelite,
                   lambda a, b: top1_symetrique_hamming(
                       codes[a][:, items], codes[b][:, items], f"twin|{a}|{b}"),
                   n, len(items))


# ---------------------------------------------------------------------------
# 5. Park et al., bloc GSS
# ---------------------------------------------------------------------------

def controle_park(codes, items_idx, cond, nom):
    """Transposition DECLAREE (preenregistrement section 6) du controle de fidelite a
    l'archive Park : la fonction Twin est cablee sur REF_V4/DEMO et ne peut pas etre
    appelee ici, mais la REGLE est la meme, sur les memes briques -- IC bootstrap non
    chevauchants entre le top-1 du candidat contre les humains de vague 1 et celui de la
    condition `demographique` contre LES MEMES humains, MEME bassin, MEMES items.
    La baseline est recalculee ici sur le bassin reellement attaque, jamais fournie.
    """
    pool = codes[S.VAGUE1][:, items_idx]
    n = pool.shape[0]
    out = {}
    for etiquette, table in (("candidat", codes[cond][:, items_idx]),
                             ("baseline", codes[S.DEMO_COND][:, items_idx])):
        a = S.accord_categoriel(table, pool)
        _, t1, _ = S.rangs_depuis_accord(a, np.arange(n), np.random.default_rng(
            [GRAINE, graine_nom(f"park|{nom}|{etiquette}")]))
        m, b, h = bootstrap_personnes(t1, n_tirages=N_BOOTSTRAP,
                                      graine=[GRAINE, graine_nom(f"park|{nom}|{etiquette}|ic")])
        out[etiquette] = (m, b, h)
    passe = bool(out["candidat"][1] > out["baseline"][2])
    return passe, out["candidat"], out["baseline"]


def bloc_park(lignes, items_stricts=True, etiquette_jeu="Park et al. (GSS)"):
    print("\n" + "=" * 78, flush=True)
    print(f"{etiquette_jeu}  (regle d'items : "
          f"{'100 % renseignes partout, PREENREGISTREE' if items_stricts else 'tous les items, manquants masques par la distance -- POST HOC'})",
          flush=True)
    print("=" * 78, flush=True)
    ordre, items, tables, typ = S.charger_domaine("gss")
    conditions = list(PIPELINES_PARK)
    # On ne code que les tables reellement utilisees (vague 1 + les cinq conditions) :
    # v8 est ecartee au preenregistrement (non documentee), la vague 2 n'intervient pas.
    tables_utiles = {S.VAGUE1: tables[S.VAGUE1]}
    tables_utiles.update({c: tables[c] for c in conditions})
    codes = S.coder_categoriel_commun(tables_utiles, items)
    n = len(ordre)

    # Items CONSTANTS : renseignes a 100 % chez la vague 1 et chez TOUTES les conditions.
    # Variante POST HOC (items_stricts=False) : tous les items, les rares cellules
    # manquantes etant deja masquees par a2_commun.distance_hamming comme partout ailleurs
    # dans ce depot. Le jeu d'items reste le MEME pour toutes les paires dans les deux cas.
    if items_stricts:
        plein = np.ones(len(items), dtype=bool)
        for k in codes:
            plein &= (codes[k] >= 0).all(axis=0)
        items_idx = np.flatnonzero(plein)
    else:
        items_idx = np.arange(len(items))
    print(f"bassin constant : {n} personnes | items constants : {len(items_idx)} "
          f"sur {len(items)}", flush=True)

    print("\n--- controle d'interpretabilite (regle transposee, eliminatoire) ---",
          flush=True)
    retenues, fidelite = [], {}
    for c in conditions:
        passe, cand, base = controle_park(codes, items_idx, c, c)
        fidelite[c] = cand[0]
        print(f"  {'PASSE ' if passe else 'EXCLUE'}  {c:16s} top1 vs humains v1 "
              f"{cand[0]*100:6.2f} % [{cand[1]*100:.2f};{cand[2]*100:.2f}] | baseline "
              f"{base[0]*100:.2f} % [{base[1]*100:.2f};{base[2]*100:.2f}]", flush=True)
        if passe:
            retenues.append(c)
        lignes.append({"jeu": etiquette_jeu, "bloc": "controle", "serie": c,
                       "passe": int(passe), "fidelite_top1": cand[0],
                       "fidelite_bas": cand[1], "fidelite_haut": cand[2],
                       "baseline_top1": base[0], "baseline_bas": base[1],
                       "baseline_haut": base[2], "n_pool": n, "n_items": len(items_idx)})
    print(f"  -> {len(retenues)}/{len(conditions)} conditions retenues", flush=True)

    def mesure(a, b):
        X, Y = codes[a][:, items_idx], codes[b][:, items_idx]
        return top1_symetrique_accord(S.accord_categoriel(X, Y),
                                      S.accord_categoriel(Y, X), f"park|{a}|{b}")

    print("\n--- paires (attaque symetrique, bassin et items constants) ---", flush=True)
    return _paires(lignes, etiquette_jeu, PIPELINES_PARK, retenues, conditions,
                   fidelite, mesure, n, len(items_idx))


# ---------------------------------------------------------------------------
# 6. Le coeur commun aux deux jeux
# ---------------------------------------------------------------------------

def _paires(lignes, jeu, pipelines, retenues, toutes, fidelite, mesurer, n, n_items):
    """Toutes les paires non ordonnees, celles du test principal (deux configurations
    retenues) et celles rapportees a part (au moins une exclue par le controle)."""
    d_list, taux_list, fid_list, indic, etiquettes = [], [], [], [], []
    for a, b in itertools.combinations(toutes, 2):
        principale = (a in retenues) and (b in retenues)
        t1 = mesurer(a, b)
        m, bas, haut = bootstrap_personnes(
            t1, n_tirages=N_BOOTSTRAP, graine=[GRAINE, graine_nom(f"{jeu}|{a}|{b}")])
        d = distance_pipeline(pipelines[a], pipelines[b])
        fid = float(np.sqrt(max(fidelite.get(a, np.nan), 0)
                            * max(fidelite.get(b, np.nan), 0)))
        marque = " " if principale else "*"
        print(f" {marque}d={d}  {m*100:6.2f} % [{bas*100:5.2f};{haut*100:5.2f}]  "
              f"{a[:34]:34s} <-> {b[:34]:34s}  ({descripteurs_differents(pipelines[a], pipelines[b])})",
              flush=True)
        lignes.append({"jeu": jeu, "bloc": "paire" if principale else "paire_hors_controle",
                       "serie": f"{a} <-> {b}", "d": d,
                       "descripteurs_differents": descripteurs_differents(
                           pipelines[a], pipelines[b]),
                       "top1": m, "top1_bas": bas, "top1_haut": haut,
                       "fidelite_geom_paire": fid, "n_pool": n, "n_items": n_items,
                       "hasard": 1.0 / n})
        if principale:
            d_list.append(d)
            taux_list.append(m)
            fid_list.append(fid)
            indic.append(t1)
            etiquettes.append(f"{a} <-> {b}")

    if len(d_list) < 3:
        print(f"\n{jeu} : moins de 3 paires principales, aucune relation calculable.",
              flush=True)
        return None

    d_arr = np.array(d_list, float)
    taux_arr = np.array(taux_list, float)
    fid_arr = np.array(fid_list, float)
    rho = spearman(d_arr, taux_arr)
    rho_p = spearman_partiel(d_arr, taux_arr, fid_arr)
    bas, haut, bas_p, haut_p = ic_rho_bootstrap(
        indic, d_arr, fid_arr, n, [GRAINE, graine_nom(f"rho|{jeu}")])
    v = verdict_jeu(rho, bas, haut)

    print(f"\n{jeu} : {len(d_list)} paires principales, d de {int(d_arr.min())} a "
          f"{int(d_arr.max())}", flush=True)
    print(f"  rho(d, top1)              = {rho:+.3f}  IC95 [{bas:+.3f} ; {haut:+.3f}]  "
          f"-> {v}", flush=True)
    print(f"  rho partiel (fidelite ctl) = {rho_p:+.3f}  IC95 [{bas_p:+.3f} ; {haut_p:+.3f}]",
          flush=True)
    print(f"  rho(fidelite, top1)        = {spearman(fid_arr, taux_arr):+.3f}   "
          f"rho(d, fidelite) = {spearman(d_arr, fid_arr):+.3f}", flush=True)

    print("  dispersion intra-niveau (test B) :", flush=True)
    for niveau in sorted(set(d_list)):
        sel = taux_arr[d_arr == niveau]
        print(f"    d={niveau} : n={len(sel)}  moyenne {sel.mean()*100:6.2f} %  "
              f"etendue {sel.min()*100:.2f}-{sel.max()*100:.2f} %  "
              f"ecart-type {sel.std(ddof=0)*100:.2f} pts", flush=True)
        lignes.append({"jeu": jeu, "bloc": "dispersion_par_d", "serie": f"d={niveau}",
                       "d": niveau, "n_paires": len(sel), "top1": float(sel.mean()),
                       "top1_bas": float(sel.min()), "top1_haut": float(sel.max()),
                       "ecart_type_pts": float(sel.std(ddof=0) * 100)})

    lignes.append({"jeu": jeu, "bloc": "relation", "serie": "rho de Spearman(d, top1)",
                   "n_paires": len(d_list), "rho": rho, "rho_bas": bas, "rho_haut": haut,
                   "rho_partiel": rho_p, "rho_partiel_bas": bas_p,
                   "rho_partiel_haut": haut_p,
                   "rho_fidelite_top1": spearman(fid_arr, taux_arr),
                   "rho_d_fidelite": spearman(d_arr, fid_arr),
                   "verdict": v, "n_pool": n, "n_items": n_items})
    return {"jeu": jeu, "rho": rho, "bas": bas, "haut": haut, "rho_p": rho_p,
            "bas_p": bas_p, "haut_p": haut_p, "verdict": v, "n_paires": len(d_list)}


# ---------------------------------------------------------------------------
# 6 bis. POST HOC, declare comme tel : la composition des axes.
# ---------------------------------------------------------------------------

REF_TWIN = "Text Persona - GPT4.1-mini"


def composition_axes(lignes):
    """POST HOC (non preenregistre). Le comptage d non pondere echoue (section 5,
    critere 3) parce qu'a d fixe les taux s'etalent enormement. Question naturelle
    suivante : l'effet de DEUX changements se deduit-il des effets de chacun pris
    seul ?

    Non circulaire au sens ou la calibration n'utilise QUE les paires a un seul axe
    (reference <-> reference + un axe) et la prediction porte sur des paires qui
    n'entrent pas dans la calibration : effet(A et B) predit = effet(A) x effet(B),
    modele multiplicatif (degradations independantes). Aucune constante n'est ajustee
    sur les paires predites.
    """
    print("\n" + "=" * 78, flush=True)
    print("POST HOC (non preenregistre) : les axes se composent-ils ?", flush=True)
    print("=" * 78, flush=True)
    paires = {}
    for r in lignes:
        if r.get("jeu") == "Twin-2K-500" and r.get("bloc") == "paire":
            a, b = r["serie"].split(" <-> ")
            paires[frozenset((a, b))] = r["top1"]

    # calibration : les seules paires reference <-> reference + un axe
    effet = {}
    for cle, t in paires.items():
        a, b = tuple(cle)
        if REF_TWIN not in (a, b):
            continue
        autre = b if a == REF_TWIN else a
        if distance_pipeline(PIPELINES_TWIN[a], PIPELINES_TWIN[b]) == 1:
            axe = descripteurs_differents(PIPELINES_TWIN[a], PIPELINES_TWIN[b])
            effet[autre] = (axe, t)
    print(f"calibration sur {len(effet)} paires a un seul axe, ancrees sur "
          f"« {REF_TWIN} » :", flush=True)
    for c, (axe, t) in sorted(effet.items(), key=lambda kv: -kv[1][1]):
        print(f"    {axe:16s} effet = {t*100:6.2f} %", flush=True)

    print("\nprediction hors calibration (paires a deux axes, aucune constante ajustee) :",
          flush=True)
    obs, pre = [], []
    for a, b in itertools.combinations(sorted(effet), 2):
        t = paires.get(frozenset((a, b)))
        if t is None:
            continue
        p = effet[a][1] * effet[b][1]
        obs.append(t)
        pre.append(p)
        print(f"    {effet[a][0]:14s} x {effet[b][0]:14s} predit {p*100:6.2f} %  "
              f"observe {t*100:6.2f} %  rapport observe/predit "
              f"{t/p if p > 0 else np.nan:5.2f}", flush=True)
        lignes.append({"jeu": "Twin-2K-500", "bloc": "posthoc_composition",
                       "serie": f"{effet[a][0]} x {effet[b][0]}",
                       "top1": t, "top1_predit_multiplicatif": p,
                       "rapport_observe_predit": t / p if p > 0 else np.nan})
    if len(obs) >= 3:
        obs, pre = np.array(obs), np.array(pre)
        mae = float(np.mean(np.abs(obs - pre)) * 100)
        rho = spearman(pre, obs)
        print(f"\n  erreur absolue moyenne {mae:.2f} pts | rho de rang "
              f"predit/observe {rho:+.3f} | rapport median "
              f"{float(np.median(obs / pre)):.2f} (1,00 = composition exacte)", flush=True)
        lignes.append({"jeu": "Twin-2K-500", "bloc": "posthoc_composition_resume",
                       "serie": "modele multiplicatif calibre sur les paires a un axe",
                       "n_paires": len(obs), "mae_pts": mae, "rho": rho,
                       "rapport_median": float(np.median(obs / pre))})


# ---------------------------------------------------------------------------
# 7. main
# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes = []
    res_twin = bloc_twin(lignes)
    res_park = bloc_park(lignes)

    print("\n" + "=" * 78, flush=True)
    print("VERDICT (regle de decision preenregistree, section 5)", flush=True)
    print("=" * 78, flush=True)
    for r in (res_twin, res_park):
        if r is None:
            continue
        print(f"  {r['jeu']:22s} n={r['n_paires']:3d}  rho={r['rho']:+.3f} "
              f"[{r['bas']:+.3f};{r['haut']:+.3f}]  {r['verdict']}  |  "
              f"partiel {r['rho_p']:+.3f} [{r['bas_p']:+.3f};{r['haut_p']:+.3f}]",
              flush=True)
    if res_twin and res_park:
        meme_signe = np.sign(res_twin["rho"]) == np.sign(res_park["rho"])
        replique = (res_twin["verdict"] == "SOUTENUE"
                    and res_park["verdict"] == "SOUTENUE" and meme_signe)
        inversion = np.isfinite(res_twin["rho"]) and np.isfinite(res_park["rho"]) \
            and not meme_signe
        print(f"\n  meme signe entre jeux : {meme_signe}", flush=True)
        print(f"  REPLICATION (les deux SOUTENUE, meme signe) : {replique}", flush=True)
        print(f"  INVERSION entre jeux (critere de refutation 2) : {inversion}", flush=True)
        fort = (res_twin["rho_p"] <= -0.30
                and not (res_twin["bas_p"] <= 0 <= res_twin["haut_p"]))
        print(f"  H au sens fort sur Twin (rho partiel <= -0,30, IC excluant 0, "
              f"test A) : {fort}", flush=True)

    # --- POST HOC declares : sensibilite a la regle d'items sur Park, composition ---
    res_park_large = bloc_park(lignes, items_stricts=False,
                               etiquette_jeu="Park et al. (GSS) POST HOC 177 items")
    if res_park_large:
        print(f"\n  POST HOC Park 177 items : rho={res_park_large['rho']:+.3f} "
              f"[{res_park_large['bas']:+.3f};{res_park_large['haut']:+.3f}] "
              f"{res_park_large['verdict']} | partiel {res_park_large['rho_p']:+.3f}",
              flush=True)
    composition_axes(lignes)

    df = pd.DataFrame(lignes)
    chemin = os.path.join(SORTIE, "c7-loi-distance.csv")
    df.to_csv(chemin, index=False)
    print(f"\necrit {chemin} ({len(df)} lignes)", flush=True)


if __name__ == "__main__":
    main()
