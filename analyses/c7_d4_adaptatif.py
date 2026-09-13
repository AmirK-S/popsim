"""
c7_d4_adaptatif : ce que D4 protege vraiment, mesure sous un attaquant qui choisit
ses colonnes, et ce que ses deux « 0,0 » d'utilite republient.

===========================================================================
MOTIF. L'audit `resultats/audit-comparaison-dp-2026-09-13.md` etablit deux choses
(F1 et F5) que le depot n'avait mesurees que partiellement :

  F1 — `c7_defense.defense_d4` permute chaque item INDEPENDAMMENT a l'interieur de
       chaque segment. Le multiensemble des reponses a l'item j dans le segment g est
       donc conserve a l'identique : D4 republie exactement l'histogramme intra-segment.
       Les `erreur_distribution = 0,0` et `erreur_groupes = 0,0` publies sont cette
       republication, pas une utilite preservee a bon compte.

  F5 — un attaquant qui CHOISIT ses colonnes et ecarte le bloc brouille attaque les 20
       items d'opinion, que D4 ne touche jamais. Le top-1 de 0,13 % mesure un attaquant
       contraint aux 60 items ; ce n'est pas le taux de D4 sous le meilleur attaquant
       mesure.

CE FICHIER NE REJOUE PAS LES CONCLUSIONS DE L'AUDIT : il les remesure dans le depot,
avec les fonctions du depot, une graine fixee et un bassin CONSTANT entre conditions,
pour que le chiffre a publier ait un script, un CSV et un intervalle.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                                les tables Twin-2K-500
  c7_reidentification.items_communs/rangs_attaque/graine_nom/REF_V4/REF_V13
                                                   l'attaque et ses garde-fous
  c7_mecanisme.items_achat                         les 40 indices du bloc d'achat
  c7_defense.defense_d4                            LA defense telle qu'elle est publiee
  a2_commun.bootstrap_personnes                    l'IC par reechantillonnage de personnes
  c7_controle_interpretabilite.controle_avant_interpretation
                                                   le controle prealable, sur le bassin
                                                   EXACTEMENT attaque, jeu d'items par
                                                   jeu d'items

CE QUI EST NOUVEAU ICI, et rien d'autre :
  (1) le controle de conservation du multiensemble intra-segment, couple par couple ;
  (2) le top-1 de la publication D4 et du jumeau non protege sous trois choix de
      colonnes (60 items, 40 achat seuls, 20 opinion seuls), meme bassin, meme attaque,
      meme bootstrap ;
  (3) la variance du top-1 sur 10 tirages de permutation D4 (le chiffre publie est un
      tirage unique) ;
  (4) la part des cellules dont la valeur est LISIBLE dans la sortie D4 seule, sans
      aucune connaissance laterale (multiensemble degenere dans le segment).

ETHIQUE : aucun pid, aucun appariement individuel, aucune reponse individuelle n'est
imprime ni ecrit ; uniquement des taux agreges. Aucun appel de modele de langage,
aucun reseau. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_d4_adaptatif.py
===========================================================================
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                              # noqa: E402
from a2_commun import bootstrap_personnes                            # noqa: E402
from c7_reidentification import (                                    # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)
from c7_mecanisme import items_achat                                 # noqa: E402
import c7_defense as D                                               # noqa: E402
from c7_controle_interpretabilite import (                           # noqa: E402
    controle_avant_interpretation, EchecControleInterpretabilite,
)

GRAINE = 20260913
N_BOOTSTRAP = 2000
N_REPLICATS_D4 = 10
CIBLE = D.CIBLE


# ---------------------------------------------------------------------------
# (1) Conservation du multiensemble intra-segment : F1, verifiee couple par couple
# ---------------------------------------------------------------------------

def conservation_multiensemble(x40, x40_def, seg_c):
    """Pour chaque (segment, item) : le multiensemble publie est-il celui d'origine ?"""
    couples = 0
    conserves = 0
    for g in np.unique(seg_c):
        if g < 0:
            continue
        membres = np.flatnonzero(seg_c == g)
        if len(membres) < 2:
            continue
        for j in range(x40.shape[1]):
            couples += 1
            if np.array_equal(np.sort(x40[membres, j]), np.sort(x40_def[membres, j])):
                conserves += 1
    return couples, conserves


def cellules_lisibles(x40_def, seg_c):
    """Part des cellules dont la valeur est determinee par la sortie D4 SEULE.

    Si, dans un segment, toutes les reponses publiees a l'item j valent la meme
    modalite, alors la reponse de chaque membre a cet item est connue de quiconque lit
    la publication, sans aucune connaissance laterale, sans reconstruire la permutation.
    C'est le cas degenere du fait etabli en F1 ; il ne suppose aucun adversaire informe.
    """
    n_cellules = 0
    n_lisibles = 0
    par_personne = np.zeros(x40_def.shape[0])
    for g in np.unique(seg_c):
        if g < 0:
            continue
        membres = np.flatnonzero(seg_c == g)
        if len(membres) < 2:
            continue
        for j in range(x40_def.shape[1]):
            vals = x40_def[membres, j]
            valides = vals[vals >= 0]
            n_cellules += len(valides)
            if len(valides) and len(np.unique(valides)) == 1:
                n_lisibles += len(valides)
                par_personne[membres] += 1
    return n_cellules, n_lisibles, par_personne


# ---------------------------------------------------------------------------
# (2) L'attaque, a colonnes choisies. Bassin et pool CONSTANTS entre conditions.
# ---------------------------------------------------------------------------

def top1_sur_colonnes(x_publie, pool, couverts, colonnes, etiquette):
    """Top-1 monde ferme en n'utilisant QUE `colonnes`. Pool = population entiere."""
    rng = np.random.default_rng([GRAINE, 300, graine_nom(CIBLE), graine_nom(etiquette)])
    _, top1, _ = rangs_attaque(x_publie[:, colonnes], pool[:, colonnes], couverts, rng)
    m, b, h = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP,
                                  graine=[GRAINE, 301, graine_nom(etiquette)])
    return m, b, h, top1


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]

    items = items_communs(codes, [REF_V4, REF_V13])
    idx_achat_abs = items_achat(paq)
    achat_mask = np.isin(items, idx_achat_abs)
    i_achat = np.flatnonzero(achat_mask)
    i_opinion = np.flatnonzero(~achat_mask)

    pool_v4 = codes[REF_V4][:, items]
    x_cible = codes[CIBLE][:, items]
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))
    seg_c = seg_gra[couverts]
    x60 = x_cible[couverts]
    x40 = x60[:, i_achat]
    x20 = x60[:, i_opinion]

    print(f"bassin : {len(couverts)} personnes, {len(items)} items communs "
          f"({len(i_achat)} achat, {len(i_opinion)} opinion) ; pool = {len(pool_v4)}",
          flush=True)
    tailles = np.array([int((seg_c == g).sum()) for g in np.unique(seg_c) if g >= 0])
    print(f"segments S_gra sur le bassin : {len(tailles)}, taille mediane "
          f"{int(np.median(tailles))}, min {tailles.min()}, max {tailles.max()}",
          flush=True)

    # --- Controle prealable, jeu d'items par jeu d'items, sur le bassin exact ---
    print("\n=== Controle d'interpretabilite (c7_controle_interpretabilite) ===",
          flush=True)
    jeux = [("60 items", np.arange(len(items))),
            ("40 items d'achat", i_achat),
            ("20 items d'opinion", i_opinion)]
    controle = {}
    for nom, cols in jeux:
        try:
            d = controle_avant_interpretation(couverts, items[cols], x60[:, cols],
                                              f"{CIBLE}|{nom}", paq=paq)
            controle[nom] = True
            print(f"  {nom:20s} PASSE  candidat {d['candidat_top1']*100:.2f} % "
                  f"[{d['candidat_ic'][0]*100:.2f};{d['candidat_ic'][1]*100:.2f}] "
                  f"vs baseline demo {d['baseline_top1']*100:.2f} % "
                  f"[{d['baseline_ic'][0]*100:.2f};{d['baseline_ic'][1]*100:.2f}]",
                  flush=True)
        except EchecControleInterpretabilite as exc:
            controle[nom] = False
            print(f"  {nom:20s} ECHEC — ce jeu d'items ne porte pas d'information "
                  f"individuelle demontrable ; son top-1 est mesure mais NE DOIT PAS "
                  f"etre interprete comme une fuite.\n" +
                  "\n".join("      " + l for l in str(exc).splitlines()), flush=True)

    # --- La publication D4, telle qu'elle est publiee (meme graine que c7_defense) ---
    x40_d4 = D.defense_d4(x40, seg_c)
    x60_d4 = x60.copy()
    x60_d4[:, i_achat] = x40_d4

    # --- (1) F1 : conservation du multiensemble ---
    couples, conserves = conservation_multiensemble(x40, x40_d4, seg_c)
    print(f"\n=== F1, conservation du multiensemble intra-segment ===\n"
          f"  {conserves} / {couples} couples segment x item conserves a l'identique "
          f"({100.0 * conserves / couples:.1f} %)", flush=True)

    n_cel, n_lis, par_pers = cellules_lisibles(x40_d4, seg_c)
    print(f"  cellules dont la valeur est lisible dans la sortie D4 SEULE "
          f"(multiensemble degenere) : {n_lis} / {n_cel} "
          f"({100.0 * n_lis / n_cel:.2f} %) ; "
          f"mediane par personne {int(np.median(par_pers))} items sur 40 ; "
          f"personnes avec au moins un item lisible : "
          f"{100.0 * (par_pers > 0).mean():.1f} %", flush=True)

    # --- (2) Le top-1, a colonnes choisies ---
    print("\n=== Top-1 monde ferme, l'attaquant choisit ses colonnes ===", flush=True)
    lignes = []
    for publication, X in (("jumeau non protege", x60), ("D4 (publie)", x60_d4)):
        for nom, cols in jeux:
            etiq = f"{publication}|{nom}"
            m, b, h, _ = top1_sur_colonnes(X, pool_v4, couverts, cols, etiq)
            lignes.append({
                "publication": publication, "colonnes_attaquees": nom,
                "n_colonnes": len(cols), "n": len(couverts), "n_pool": len(pool_v4),
                "top1": m, "top1_bas": b, "top1_haut": h,
                "controle_interpretabilite": "passe" if controle.get(nom) else "echec",
                "replicat_permutation_d4": "publie (graine c7_defense 20260911, 104)",
            })
            print(f"  {publication:20s} / {nom:20s} top1={m*100:.3f} % "
                  f"[{b*100:.3f} ; {h*100:.3f}]", flush=True)

    # --- (3) Variance sur les tirages de permutation D4 ---
    print(f"\n=== {N_REPLICATS_D4} tirages de permutation D4 (le chiffre publie est un "
          f"tirage unique) ===", flush=True)
    for nom, cols in jeux:
        vals = []
        for r in range(N_REPLICATS_D4):
            rng_p = np.random.default_rng([GRAINE, 400, r])
            xr = x40.copy()
            for g in np.unique(seg_c):
                if g < 0:
                    continue
                membres = np.flatnonzero(seg_c == g)
                if len(membres) < 2:
                    continue
                for j in range(x40.shape[1]):
                    xr[membres, j] = x40[rng_p.permutation(membres), j]
            X = x60.copy()
            X[:, i_achat] = xr
            m, _, _, _ = top1_sur_colonnes(X, pool_v4, couverts, cols,
                                           f"D4|replicat{r}|{nom}")
            vals.append(m)
        vals = np.array(vals)
        lignes.append({
            "publication": "D4 (10 replicats de permutation)",
            "colonnes_attaquees": nom, "n_colonnes": len(cols), "n": len(couverts),
            "n_pool": len(pool_v4),
            "top1": float(vals.mean()), "top1_bas": float(vals.min()),
            "top1_haut": float(vals.max()),
            "controle_interpretabilite": "passe" if controle.get(nom) else "echec",
            "replicat_permutation_d4": (f"moyenne sur {N_REPLICATS_D4} tirages ; "
                                        f"bornes = etendue, PAS un IC ; "
                                        f"ecart-type {vals.std(ddof=1)*100:.4f} pt"),
        })
        print(f"  {nom:20s} moyenne={vals.mean()*100:.3f} % "
              f"etendue [{vals.min()*100:.3f} ; {vals.max()*100:.3f}] "
              f"ecart-type={vals.std(ddof=1)*100:.4f} pt", flush=True)

    # --- (4) Les invariants, en clair ---
    lignes.append({
        "publication": "D4 (publie)", "colonnes_attaquees": "INVARIANT — multiensemble",
        "n_colonnes": len(i_achat), "n": len(couverts), "n_pool": len(pool_v4),
        "top1": float("nan"), "top1_bas": float("nan"), "top1_haut": float("nan"),
        "controle_interpretabilite": "sans objet",
        "replicat_permutation_d4": (
            f"{conserves}/{couples} couples segment x item conserves a l'identique ; "
            f"{n_lis}/{n_cel} cellules ({100.0*n_lis/n_cel:.2f} %) lisibles dans la "
            f"sortie seule ; un adversaire connaissant les |g|-1 autres membres d'un "
            f"segment reconstitue les 40 reponses de la cible avec certitude, par "
            f"construction (taille mediane de segment {int(np.median(tailles))})"),
    })

    T1.ecrire(lignes, "c7-d4-adaptatif.csv")
    print("\nRAPPEL : ce fichier ne mesure PAS un epsilon. D4 n'offre aucune garantie "
          "formelle ; les taux ci-dessus sont ceux d'attaques particulieres, et le "
          "meilleur attaquant mesure n'est pas le meilleur attaquant possible.",
          flush=True)


if __name__ == "__main__":
    main()
