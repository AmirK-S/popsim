"""
c7_dp_zcdp : remesure du cout d'un generateur synthetique sous confidentialite
differentielle, avec le mecanisme GAUSSIEN compose sous zCDP et une reference
APPARIEE -- les deux corrections que l'audit `resultats/audit-comparaison-dp-2026-09-13.md`
a portees contre `analyses/c7_dp.py` (constats F3 et F4).

===========================================================================
POURQUOI CE SCRIPT EXISTE

L'audit du 13/09 a produit, dans son §8, un texte de remplacement pour le §6.2 du
manuscrit. La passe T5 a refuse d'y ecrire cinq grandeurs -- 0,9-1,0 ; 2,7-2,9 ;
0,1-0,3 ; 4,50-4,55 ; 0,09 % -- parce qu'elles venaient de scripts jetables hors
depot (audit, §Tracabilite) et n'existaient dans aucun CSV. Le refus etait juste :
ce depot a deja publie un chiffre non source puis l'a envoye a un tiers.

Ce script reconstruit ces mesures dans le depot, a graine fixee et avec replicats,
et ecrit `resultats/c7-dp-zcdp.csv`. Il ne recopie aucune valeur du §8 : les valeurs
du §8 sont ici des valeurs ATTENDUES, comparees a la fin, et c'est le run qui fait
foi en cas d'ecart.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                             les quinze tables de Twin
  c7_reidentification.items_communs/graine_nom/REF_V4/REF_V13
  c7_mecanisme.items_achat                      les 40 indices du bloc d'achat
  c7_defense.erreur_distribution/erreur_groupes/erreur_correlations/mesurer_utilite
                                                MEMES metriques que c7-defense-courbe.csv
  c7_defense.risque / CIBLE                     meme attaque top-1, meme bootstrap

CE QUI CHANGE PAR RAPPORT A `analyses/c7_dp.py` -- exactement deux choses :

 (1) MECANISME. c7_dp.py bruite chaque histogramme d'item par Laplace, budget
     reparti a parts egales sur les 60 items sous COMPOSITION SEQUENTIELLE BASIQUE
     (eps_item = eps/60, echelle 2/eps_item). Ici : mecanisme GAUSSIEN, composition
     sous zCDP (Bun & Steinke). Pour un histogramme d'item, sensibilite L2 sous
     REMPLACEMENT d'une personne = sqrt(2) (une unite quitte une case et entre dans
     une autre) ; le mecanisme gaussien d'ecart-type sigma satisfait
     rho_item = Delta2^2 / (2 sigma^2) ; les 60 items composent additivement en rho,
     donc rho_total = 60 * rho_item. La conversion zCDP -> (eps, delta) employee est
     la borne standard eps = rho + 2 sqrt(rho ln(1/delta)), inversee en
     rho = (sqrt(eps + ln(1/delta)) - sqrt(ln(1/delta)))^2, avec delta = 1e-6.
     A eps = 3 cela donne rho = 0,147 et sigma = 20,2, contre un ecart-type effectif
     de Laplace de 56,6 au meme eps : 2,8 fois moins de bruit. Rien d'exotique.

 (2) REFERENCE APPARIEE. c7_dp.py ajuste le generateur sur `pool_v4` (les 2 058
     HUMAINS, ligne 148) et note son utilite contre `twin_x40` (le JUMEAU, ligne 152).
     D4, lui, est le jumeau permute note contre le jumeau. La DP se voyait donc
     facturer l'ecart humains<->jumeau. Ici le generateur est ajuste sur le JUMEAU,
     le meme objet que D4 protege, et note contre le jumeau. La colonne `reference`
     du CSV porte les DEUX mesures pour chaque tirage : la mesure appariee, et la
     mesure desapparie contre les humains, conservee comme TEMOIN -- c'est elle qui
     rend le desappariement visible dans le fichier au lieu d'etre a demontrer.

LE POINT DE CONTROLE eps = infini N'EST PAS OPTIONNEL. C'est le meme generateur
SANS AUCUN BRUIT. Il etait deja present dans `c7-dp-resultats.csv` et personne ne
l'a lu avant de conclure : il montre que le cout mesure est celui de l'hypothese
d'independance entre items (PrivBayes degre 0), pas celui de la confidentialite.
La contribution marginale du budget est la difference composante(eps) - composante(inf),
calculee ici par appariement de replicat a replicat (meme indice de replicat, memes
tirages d'echantillonnage) et publiee avec son etendue.

CE QUE CE MECANISME GARANTIT : (eps, delta)-DP pour la publication du vecteur des
60 histogrammes d'item sur les 2 058 lignes du jumeau, sous remplacement d'une ligne,
delta = 1e-6, par immunite au post-traitement pour le jeu synthetique echantillonne.

CE QU'IL NE GARANTIT PAS -- identique a c7_dp.py, et il faut le redire : aucune
structure jointe (items tires independamment : aucune correlation, aucun ecart entre
segments ne peut survivre, quel que soit eps -- plancher d'architecture) ; le segment
S_gra est traite comme covariable publique ; aucune composition avec les autres
analyses du depot n'est comptabilisee ; ce n'est pas une bibliotheque de reference
verifiee (aucune n'est installee), la comptabilite zCDP est ecrite ici a la main et
documentee ligne a ligne ci-dessous.

CE QUE CE SCRIPT NE FAIT PAS, ET NE DOIT PAS FAIRE : classer D4 et la DP. Le but de
la mesure est de rendre opposable une phrase qui dit que NOTRE implementation de
reference etait trop faible, et de combien. Aucune ligne de sortie ne compare les
deux mecanismes.

ETHIQUE : aucun pid, aucune reponse individuelle, aucun appariement individuel n'est
imprime ou ecrit ; uniquement des grandeurs agregees. Aucun appel de modele de
langage, aucun acces reseau. Lecture seule sur data/.

Usage : .venv/bin/python analyses/c7_dp_zcdp.py
===========================================================================
"""

import math
import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                          # noqa: E402
from c7_reidentification import (                               # noqa: E402
    items_communs, graine_nom, REF_V4, REF_V13,
)
from c7_mecanisme import items_achat                            # noqa: E402
from c7_defense import (                                        # noqa: E402
    CIBLE, risque, erreur_distribution, erreur_groupes, erreur_correlations,
)

GRAINE = 20260913
DELTA = 1e-6
EPSILONS = [1.0, 3.0, 10.0, np.inf]      # eps=1 pour la borne basse du §8, inf = temoin
N_REPLICATS = 10                          # audit F7 : 10 graines, avec etendue
N_REPLICATS_RISQUE = 10

# Valeurs annoncees par le §8 de l'audit, SANS SOURCE OPPOSABLE. Elles ne sont
# jamais utilisees dans un calcul : uniquement comparees au run a la fin.
ATTENDU_S8 = {
    ("distribution", 1.0): 1.754, ("groupes", 1.0): 2.627, ("correlations", 1.0): 4.506,
    ("distribution", 3.0): 0.997, ("groupes", 3.0): 2.932, ("correlations", 3.0): 4.549,
    ("distribution", 10.0): 0.923, ("groupes", 10.0): 2.673, ("correlations", 10.0): 4.603,
    ("distribution", np.inf): 0.837,
}
ATTENDU_TOP1_EPS3_PCT = 0.085     # §8 « 0,09 % », F5 table : 0,085 %
ATTENDU_SIGMA_EPS3 = 20.2
ATTENDU_SIGMA_LAPLACE_EPS3 = 56.6


# ---------------------------------------------------------------------------
# Comptabilite zCDP : eps, delta -> rho -> sigma
# ---------------------------------------------------------------------------

def rho_depuis_eps_delta(eps, delta=DELTA):
    """rho tel que rho-zCDP implique (eps, delta)-DP, borne standard inversee.

    eps(rho) = rho + 2 sqrt(rho ln(1/delta)) est croissante en rho ; poser
    u = sqrt(rho) donne u^2 + 2 u sqrt(L) - eps = 0 avec L = ln(1/delta), d'ou
    u = sqrt(eps + L) - sqrt(L) et rho = u^2. eps infini -> rho infini (aucune
    contrainte, mecanisme non prive)."""
    if not np.isfinite(eps):
        return np.inf
    L = math.log(1.0 / delta)
    return (math.sqrt(eps + L) - math.sqrt(L)) ** 2


def sigma_gaussien(rho_total, n_items, sensibilite_l2=math.sqrt(2.0)):
    """Ecart-type du bruit gaussien par case d'histogramme.

    Les n_items requetes composent additivement en zCDP : rho_item = rho_total/n_items.
    Le mecanisme gaussien de sensibilite L2 = Delta2 et d'ecart-type sigma satisfait
    rho_item = Delta2^2/(2 sigma^2), d'ou sigma = Delta2 sqrt(n_items/(2 rho_total)).
    Sensibilite L2 = sqrt(2) sous REMPLACEMENT d'une personne (une unite quitte une
    case, une unite entre dans une autre) -- meme modele de voisinage que c7_dp.py,
    qui prenait L1 = 2 pour Laplace."""
    if not np.isfinite(rho_total):
        return 0.0
    return sensibilite_l2 * math.sqrt(n_items / (2.0 * rho_total))


def sigma_laplace_equivalent(eps, n_items, sensibilite_l1=2.0):
    """Ecart-type EFFECTIF du bruit de c7_dp.py au meme eps, pour le rapport de bruit.

    Laplace d'echelle b a pour ecart-type b sqrt(2) ; c7_dp.py pose b = L1/eps_item
    avec eps_item = eps/n_items (composition sequentielle basique)."""
    if not np.isfinite(eps):
        return 0.0
    return (sensibilite_l1 * n_items / eps) * math.sqrt(2.0)


# ---------------------------------------------------------------------------
# Generateur : marginales par item bruitees au gaussien, tirage i.i.d.
# ---------------------------------------------------------------------------

def marginales_bruitees_gauss(x, k_items, sigma, rng):
    """Histogramme par item sur x (n, n_items), bruit gaussien i.i.d. d'ecart-type
    sigma sur chaque case, puis troncature a zero et renormalisation (post-traitement,
    sans cout de confidentialite). sigma = 0 -> marginale empirique exacte (temoin)."""
    n_items = x.shape[1]
    probs = []
    for j in range(n_items):
        k = int(k_items[j])
        valides = x[:, j]
        valides = valides[valides >= 0]
        compte = np.bincount(valides, minlength=k).astype(float)[:k]
        if sigma > 0:
            compte = compte + rng.normal(scale=sigma, size=k)
        compte = np.clip(compte, 0, None)
        s = compte.sum()
        probs.append(compte / s if s > 0 else np.full(k, 1.0 / k))
    return probs


def echantillonner(probs, n, rng):
    out = np.empty((n, len(probs)), dtype=np.int16)
    for j, p in enumerate(probs):
        out[:, j] = rng.choice(len(p), size=n, p=p)
    return out


def trois_composantes(x_def40, x_ref40, seg_def, seg_ref):
    ed = erreur_distribution(x_def40, x_ref40)
    eg = erreur_groupes(x_def40, x_ref40, seg_def, seg_ref)
    ec = erreur_correlations(x_def40, x_ref40)
    return {"erreur_distribution": ed, "erreur_groupes": eg,
            "erreur_correlations": ec,
            "utilite_globale": float(np.mean([ed, eg, ec]))}


def nom_eps(eps):
    return f"eps={eps:g}" if np.isfinite(eps) else "eps=infini (temoin, aucun bruit)"


def main():
    print(__doc__.split("=" * 75)[1][:700], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]

    items = items_communs(codes, [REF_V4, REF_V13])
    idx_achat_abs = items_achat(paq)
    i_achat = np.flatnonzero(np.isin(items, idx_achat_abs))
    k_items60 = paq["k_items"][items]
    n_items = len(items)

    pool_v4 = codes[REF_V4][:, items]                     # 2 058 humains vague 4
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))
    assert len(couverts) == pool_v4.shape[0], "CIBLE ne couvre pas toute la population"
    seg_c = seg_gra[couverts]

    twin60 = codes[CIBLE][:, items][couverts]             # AJUSTEMENT ici (correction F3)
    twin40 = twin60[:, i_achat]                           # reference APPARIEE
    hum40 = pool_v4[:, i_achat]                           # reference desapparie (temoin)
    n = twin60.shape[0]

    print(f"\n{n_items} items communs, {len(i_achat)} d'achat, {n} lignes ; "
          f"bassin constant (les {n} personnes couvertes par {CIBLE})", flush=True)

    # ---- ecart humains<->jumeau : la facture que F3 imputait a tort a la DP -------
    ecart_ref = trois_composantes(twin40, hum40, seg_c, seg_gra)
    print(f"ecart humains<->jumeau (ce que le desappariement facturait) : "
          f"distribution={ecart_ref['erreur_distribution']:.3f} "
          f"groupes={ecart_ref['erreur_groupes']:.3f} "
          f"correlations={ecart_ref['erreur_correlations']:.3f}", flush=True)

    # ---- plancher de destruction des correlations (audit F8) ---------------------
    c_ref = pd.DataFrame(np.where(twin40 >= 0, twin40, np.nan).astype(float)).corr().values
    iu = np.triu_indices(twin40.shape[1], k=1)
    plancher_corr = float(np.nanmean(np.abs(c_ref[iu]))) * 100
    print(f"plancher de destruction des correlations (|corr| moyenne, "
          f"{len(iu[0])} paires) : {plancher_corr:.3f}", flush=True)

    lignes = []
    brut = {}          # (eps, reference, composante) -> liste des replicats

    for eps in EPSILONS:
        nom = nom_eps(eps)
        rho = rho_depuis_eps_delta(eps)
        sigma = sigma_gaussien(rho, n_items)
        sig_lap = sigma_laplace_equivalent(eps, n_items)
        rapport = (sig_lap / sigma) if sigma > 0 else float("nan")
        print(f"\n{nom} : rho={rho:.4f} sigma_gauss={sigma:.3f} "
              f"sigma_laplace_c7_dp={sig_lap:.3f} rapport={rapport:.2f}x", flush=True)

        for r in range(N_REPLICATS):
            rng = np.random.default_rng([GRAINE, graine_nom(nom), r])
            probs = marginales_bruitees_gauss(twin60, k_items60, sigma, rng)
            x_synth = echantillonner(probs, n, rng)
            s40 = x_synth[:, i_achat]

            for ref_nom, x_ref, seg_ref in (
                    ("jumeau (apparie, objet protege par D4)", twin40, seg_c),
                    ("humains v4 (desapparie, temoin F3)", hum40, seg_gra)):
                c = trois_composantes(s40, x_ref, seg_c, seg_ref)
                for comp, val in (("distribution", c["erreur_distribution"]),
                                  ("groupes", c["erreur_groupes"]),
                                  ("correlations", c["erreur_correlations"]),
                                  ("moyenne_trois", c["utilite_globale"])):
                    brut.setdefault((eps, ref_nom, comp), []).append(val)
                lignes.append({
                    "bloc": "replicat", "mecanisme": "gaussien zCDP (delta=1e-6)",
                    "epsilon": nom, "rho_zcdp": rho, "sigma_bruit": sigma,
                    "reference": ref_nom, "stat": "valeur", "replicat": r,
                    "graine": f"[{GRAINE}, crc32({nom}), {r}]", "n": n,
                    "grandeur": "trois composantes d'utilite (points)",
                    "erreur_distribution": c["erreur_distribution"],
                    "erreur_groupes": c["erreur_groupes"],
                    "erreur_correlations": c["erreur_correlations"],
                    "moyenne_trois": c["utilite_globale"],
                    "valeur": np.nan, "bas": np.nan, "haut": np.nan,
                })

        for ref_nom in ("jumeau (apparie, objet protege par D4)",
                        "humains v4 (desapparie, temoin F3)"):
            res = {}
            for comp in ("distribution", "groupes", "correlations", "moyenne_trois"):
                v = np.array(brut[(eps, ref_nom, comp)], dtype=float)
                res[comp] = (float(v.mean()), float(v.std(ddof=1)),
                             float(v.min()), float(v.max()))
            for stat, i_s in (("moyenne", 0), ("ecart_type", 1), ("min", 2), ("max", 3)):
                lignes.append({
                    "bloc": "resume", "mecanisme": "gaussien zCDP (delta=1e-6)",
                    "epsilon": nom, "rho_zcdp": rho, "sigma_bruit": sigma,
                    "reference": ref_nom, "stat": stat, "replicat": f"{N_REPLICATS} replicats",
                    "graine": f"[{GRAINE}, crc32({nom}), 0..{N_REPLICATS - 1}]", "n": n,
                    "grandeur": "trois composantes d'utilite (points)",
                    "erreur_distribution": res["distribution"][i_s],
                    "erreur_groupes": res["groupes"][i_s],
                    "erreur_correlations": res["correlations"][i_s],
                    "moyenne_trois": res["moyenne_trois"][i_s],
                    "valeur": np.nan, "bas": np.nan, "haut": np.nan,
                })
            if ref_nom.startswith("jumeau"):
                print(f"  APPARIE : distribution={res['distribution'][0]:.3f}"
                      f"+-{res['distribution'][1]:.3f}  "
                      f"groupes={res['groupes'][0]:.3f}+-{res['groupes'][1]:.3f}  "
                      f"correlations={res['correlations'][0]:.3f}"
                      f"+-{res['correlations'][1]:.3f}", flush=True)
            else:
                print(f"  temoin desapparie : distribution={res['distribution'][0]:.3f}  "
                      f"groupes={res['groupes'][0]:.3f}  "
                      f"correlations={res['correlations'][0]:.3f}", flush=True)

    # ---- contribution marginale du budget : composante(eps) - composante(inf) -----
    # Appariee replicat a replicat : meme indice r, donc memes tirages d'echantillonnage
    # une fois le bruit retire. C'est la grandeur qui dit ce que la confidentialite
    # coute VRAIMENT, une fois l'architecture payee.
    ref_app = "jumeau (apparie, objet protege par D4)"
    print("\ncontribution marginale du budget de confidentialite "
          "(composante(eps) - composante(eps=infini), appariee par replicat) :", flush=True)
    for eps in [e for e in EPSILONS if np.isfinite(e)]:
        for comp in ("distribution", "groupes", "correlations", "moyenne_trois"):
            v = np.array(brut[(eps, ref_app, comp)], dtype=float)
            v0 = np.array(brut[(np.inf, ref_app, comp)], dtype=float)
            d = v - v0
            lignes.append({
                "bloc": "contribution_marginale_budget",
                "mecanisme": "gaussien zCDP (delta=1e-6)",
                "epsilon": nom_eps(eps), "rho_zcdp": rho_depuis_eps_delta(eps),
                "sigma_bruit": sigma_gaussien(rho_depuis_eps_delta(eps), n_items),
                "reference": ref_app, "stat": "moyenne (min ; max) sur replicats apparies",
                "replicat": f"{N_REPLICATS} replicats apparies",
                "graine": f"[{GRAINE}, crc32(...), 0..{N_REPLICATS - 1}]", "n": n,
                "grandeur": f"contribution marginale du budget, composante {comp} (points)",
                "erreur_distribution": np.nan, "erreur_groupes": np.nan,
                "erreur_correlations": np.nan, "moyenne_trois": np.nan,
                "valeur": float(d.mean()), "bas": float(d.min()), "haut": float(d.max()),
            })
            if comp != "moyenne_trois":
                print(f"  eps={eps:g} {comp:<13} : {d.mean():+.3f} "
                      f"[{d.min():+.3f} ; {d.max():+.3f}]", flush=True)

    # ---- plancher de destruction des correlations, et ecart humains<->jumeau ------
    lignes.append({
        "bloc": "reference", "mecanisme": "SANS OBJET (grandeur du jumeau)",
        "epsilon": "SANS OBJET", "rho_zcdp": np.nan, "sigma_bruit": np.nan,
        "reference": "jumeau non protege", "stat": "valeur", "replicat": "deterministe",
        "graine": "SANS OBJET (deterministe)", "n": n,
        "grandeur": f"plancher de destruction des correlations : |corr| moyenne sur les "
                    f"{len(iu[0])} paires des 40 items d'achat du jumeau (points). "
                    f"Tout mecanisme qui detruit toute correlation obtient cette note.",
        "erreur_distribution": np.nan, "erreur_groupes": np.nan,
        "erreur_correlations": np.nan, "moyenne_trois": np.nan,
        "valeur": plancher_corr, "bas": np.nan, "haut": np.nan,
    })
    for comp, val in (("distribution", ecart_ref["erreur_distribution"]),
                      ("groupes", ecart_ref["erreur_groupes"]),
                      ("correlations", ecart_ref["erreur_correlations"])):
        lignes.append({
            "bloc": "reference", "mecanisme": "SANS OBJET (ecart entre references)",
            "epsilon": "SANS OBJET", "rho_zcdp": np.nan, "sigma_bruit": np.nan,
            "reference": "humains v4 contre jumeau", "stat": "valeur",
            "replicat": "deterministe", "graine": "SANS OBJET (deterministe)", "n": n,
            "grandeur": f"ecart humains<->jumeau, composante {comp} (points) : la facture "
                        f"que le desappariement de c7_dp.py imputait a la DP",
            "erreur_distribution": np.nan, "erreur_groupes": np.nan,
            "erreur_correlations": np.nan, "moyenne_trois": np.nan,
            "valeur": val, "bas": np.nan, "haut": np.nan,
        })

    # ---- rapport de bruit gaussien zCDP vs Laplace composition basique ------------
    for eps in [e for e in EPSILONS if np.isfinite(e)]:
        rho = rho_depuis_eps_delta(eps)
        sg = sigma_gaussien(rho, n_items)
        sl = sigma_laplace_equivalent(eps, n_items)
        lignes.append({
            "bloc": "mecanisme", "mecanisme": "gaussien zCDP vs Laplace composition basique",
            "epsilon": nom_eps(eps), "rho_zcdp": rho, "sigma_bruit": sg,
            "reference": "SANS OBJET (grandeur analytique)", "stat": "valeur",
            "replicat": "deterministe (formule fermee)",
            "graine": "SANS OBJET (deterministe)", "n": n,
            "grandeur": f"ecart-type du bruit par case : gaussien zCDP {sg:.3f} contre "
                        f"Laplace effectif de analyses/c7_dp.py {sl:.3f} ; "
                        f"valeur portee = le rapport (fois moins de bruit au meme eps)",
            "erreur_distribution": np.nan, "erreur_groupes": np.nan,
            "erreur_correlations": np.nan, "moyenne_trois": np.nan,
            "valeur": sl / sg, "bas": np.nan, "haut": np.nan,
        })

    # ---- risque : top-1 monde ferme, meme attaque et meme bootstrap que partout ---
    print(f"\ntop-1 monde ferme ({N_REPLICATS_RISQUE} replicats, meme attaque naive par "
          f"accord de Hamming, bootstrap 2000 personnes) :", flush=True)
    for eps in EPSILONS:
        nom = nom_eps(eps)
        rho = rho_depuis_eps_delta(eps)
        sigma = sigma_gaussien(rho, n_items)
        taux = []
        for r in range(N_REPLICATS_RISQUE):
            rng = np.random.default_rng([GRAINE, graine_nom(nom), r])
            probs = marginales_bruitees_gauss(twin60, k_items60, sigma, rng)
            x_synth = echantillonner(probs, n, rng)
            m, b, h = risque(x_synth, pool_v4, couverts, f"zcdp_{nom}_r{r}")
            taux.append((m, b, h))
            lignes.append({
                "bloc": "risque", "mecanisme": "gaussien zCDP (delta=1e-6)",
                "epsilon": nom, "rho_zcdp": rho, "sigma_bruit": sigma,
                "reference": "pool des 2058 humains vague 4", "stat": "valeur",
                "replicat": r, "graine": f"[{GRAINE}, crc32({nom}), {r}]", "n": n,
                "grandeur": "top-1 monde ferme du jeu synthetique DP, en pourcent",
                "erreur_distribution": np.nan, "erreur_groupes": np.nan,
                "erreur_correlations": np.nan, "moyenne_trois": np.nan,
                "valeur": m * 100, "bas": b * 100, "haut": h * 100,
            })
        t = np.array(taux)
        lignes.append({
            "bloc": "risque", "mecanisme": "gaussien zCDP (delta=1e-6)",
            "epsilon": nom, "rho_zcdp": rho, "sigma_bruit": sigma,
            "reference": "pool des 2058 humains vague 4",
            "stat": "moyenne sur replicats ; bornes = min du bas et max du haut",
            "replicat": f"{N_REPLICATS_RISQUE} replicats",
            "graine": f"[{GRAINE}, crc32({nom}), 0..{N_REPLICATS_RISQUE - 1}]", "n": n,
            "grandeur": "top-1 monde ferme du jeu synthetique DP, en pourcent",
            "erreur_distribution": np.nan, "erreur_groupes": np.nan,
            "erreur_correlations": np.nan, "moyenne_trois": np.nan,
            "valeur": float(t[:, 0].mean() * 100), "bas": float(t[:, 1].min() * 100),
            "haut": float(t[:, 2].max() * 100),
        })
        print(f"  {nom} : {t[:, 0].mean() * 100:.3f} % "
              f"[{t[:, 1].min() * 100:.3f} ; {t[:, 2].max() * 100:.3f}] "
              f"(hasard = {100.0 / n:.3f} %)", flush=True)

    # ---- TEMOIN DE DESAPPARIEMENT SUR LE RISQUE ---------------------------------
    # Le §8 annonce 0,09 % pour la DP a eps=3. Ce chiffre vient d'un generateur ajuste
    # sur les HUMAINS (l'architecture livree, F3 non corrige) et attaque contre les
    # HUMAINS. Le notre est ajuste sur le JUMEAU et attaque contre les humains : par
    # construction il ne peut rien fuir des humains. Les deux ne mesurent pas la meme
    # chose. On mesure ici le second cas pour dire d'ou vient l'ecart, sans le publier
    # comme une grandeur du §6.2.
    print("\nTEMOIN : generateur ajuste sur les HUMAINS (F3 non corrige), meme "
          "mecanisme gaussien zCDP, attaque contre les humains :", flush=True)
    for eps in (3.0, np.inf):
        nom = nom_eps(eps)
        rho = rho_depuis_eps_delta(eps)
        sigma = sigma_gaussien(rho, n_items)
        taux = []
        for r in range(N_REPLICATS_RISQUE):
            rng = np.random.default_rng([GRAINE, 77, graine_nom(nom), r])
            probs = marginales_bruitees_gauss(pool_v4, k_items60, sigma, rng)
            x_synth = echantillonner(probs, n, rng)
            m, b, h = risque(x_synth, pool_v4, couverts, f"zcdp_hum_{nom}_r{r}")
            taux.append((m, b, h))
        t = np.array(taux)
        lignes.append({
            "bloc": "risque_temoin_ajuste_humains", "mecanisme": "gaussien zCDP (delta=1e-6)",
            "epsilon": nom, "rho_zcdp": rho, "sigma_bruit": sigma,
            "reference": "ajuste sur les humains v4 (F3 NON corrige), attaque contre eux",
            "stat": "moyenne sur replicats ; bornes = min du bas et max du haut",
            "replicat": f"{N_REPLICATS_RISQUE} replicats",
            "graine": f"[{GRAINE}, 77, crc32({nom}), 0..{N_REPLICATS_RISQUE - 1}]", "n": n,
            "grandeur": "TEMOIN, NE PAS PUBLIER : top-1 monde ferme du generateur ajuste "
                        "sur les humains, pour situer le 0,09 % du §8 de l'audit",
            "erreur_distribution": np.nan, "erreur_groupes": np.nan,
            "erreur_correlations": np.nan, "moyenne_trois": np.nan,
            "valeur": float(t[:, 0].mean() * 100), "bas": float(t[:, 1].min() * 100),
            "haut": float(t[:, 2].max() * 100),
        })
        print(f"  {nom} : {t[:, 0].mean() * 100:.3f} % "
              f"[{t[:, 1].min() * 100:.3f} ; {t[:, 2].max() * 100:.3f}] "
              f"(hasard = {100.0 / n:.3f} %)", flush=True)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-dp-zcdp.csv")

    # ---- confrontation au §8 de l'audit : le run fait foi ------------------------
    print("\n" + "=" * 70)
    print("CONFRONTATION AU §8 DE L'AUDIT (valeurs du §8 sans source opposable ;")
    print("en cas d'ecart, c'est CE run qui fait foi)")
    print("=" * 70, flush=True)
    for (comp, eps), attendu in ATTENDU_S8.items():
        v = np.array(brut[(eps, ref_app, comp)], dtype=float)
        dedans = v.min() <= attendu <= v.max()
        print(f"  {nom_eps(eps):<34} {comp:<13} run {v.mean():.3f} "
              f"[{v.min():.3f} ; {v.max():.3f}]  §8 {attendu:.3f}  "
              f"ecart {v.mean() - attendu:+.3f}  "
              f"{'dans l etendue' if dedans else 'HORS ETENDUE'}", flush=True)
    sg3 = sigma_gaussien(rho_depuis_eps_delta(3.0), n_items)
    sl3 = sigma_laplace_equivalent(3.0, n_items)
    print(f"  sigma gaussien eps=3 : run {sg3:.3f}  §8 {ATTENDU_SIGMA_EPS3}")
    print(f"  sigma Laplace eps=3  : run {sl3:.3f}  §8 {ATTENDU_SIGMA_LAPLACE_EPS3}")
    print(f"  (top-1 eps=3 : §8 annonce {ATTENDU_TOP1_EPS3_PCT} % ; "
          f"voir le bloc risque ci-dessus)", flush=True)

    # ---- garde-fou anti-desappariement ------------------------------------------
    # Si la mesure appariee etait encore contaminee par l'ecart humains<->jumeau, la
    # composante distribution appariee serait du meme ordre que cet ecart. Elle doit
    # etre NETTEMENT en dessous. Ce n'est pas un test d'hypothese : c'est un temoin.
    d_app = float(np.mean(brut[(np.inf, ref_app, "distribution")]))
    d_des = float(np.mean(brut[(np.inf, "humains v4 (desapparie, temoin F3)",
                                "distribution")]))
    print(f"\nGARDE-FOU desappariement (temoin eps=infini, composante distribution) :")
    print(f"  appariee {d_app:.3f}  desapparie {d_des:.3f}  "
          f"ecart humains<->jumeau {ecart_ref['erreur_distribution']:.3f}")
    if d_app >= d_des:
        print("  ALERTE : la mesure appariee n'est pas plus basse que la desapparie, "
              "le desappariement subsisterait.", flush=True)
    else:
        print("  la mesure appariee est bien en dessous de la desapparie : "
              "le desappariement de F3 est retire.", flush=True)


if __name__ == "__main__":
    main()
