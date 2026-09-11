"""
c7_echelle : le top-1 de reidentification (C7) tient-il a l'echelle d'un panel national ?

===========================================================================
PREENREGISTREMENT : resultats/c7-echelle-preenregistrement.md, ecrit le 12 septembre 2026,
AVANT ce fichier et avant tout calcul.

Reponse a l'objection prevvisible sur resultats/c7-resultats.md (top-1 = 20,7 % sur 2 058
candidats) : « a l'echelle d'un panel national, ce taux s'effondre ». Etude de risque de
vie privee sur Twin-2K-500, deja public. Aucune identite ni pid n'est jamais imprime,
ecrit ou publie : seuls des taux agreges sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                  les quinze tables de Twin
  a2_commun.distance_hamming         la distance de Hamming normalisee
  a2_commun.bootstrap_personnes      l'intervalle de confiance par reechantillonnage
  a2_commun.encodeur_demographies    l'encodage indicatrice des demographies
  c7_reidentification.items_communs les 60 items toujours renseignes
  c7_reidentification.rangs_attaque  le rang du vrai repondant, ordre des candidats permute

CE QUI EST NOUVEAU ICI :
  1. Un comparateur statistique PMM k=5 sur les demographies (appariement sur moyenne
     predite, 5 plis de personnes, regression multinomiale par item), construit ici car
     aucun PMM Twin n'existe deja ailleurs dans le depot (le PMM de a35_commun est calcule
     sur le GSS, un autre jeu). Meme esprit que a35 : le donneur est une personne
     OBSERVEE, jamais une valeur inventee.
  2. La courbe de top-1 par taille de pool sous-echantillonnee (N = 50 a 2058, 20
     repetitions), pour le meilleur jumeau riche de C7, Demographics Only, ce PMM, et le
     plafond humain (l'auto-attaque vagues 1-3 contre vague 4, meme pipeline).
  3. Un DIAGNOSTIC de non-identifiabilite, pas une extrapolation : deux modeles simples
     (loi puissance, loi log) ajustes sur les 6 points mesures, compares par CV LOO
     DANS le domaine mesure, puis evalues cote a cote a environ 2x le plus grand N
     mesure (~4000) pour montrer a quel point ils divergent deja a cette distance
     modeste. AUCUNE valeur au-dela de ~4000 n'est calculee ni rapportee : un examen
     critique independant (12 septembre 2026, addendum au preenregistrement) a juge
     l'extrapolation a 10 000/100 000/1 000 000 indefendable, la loi log gagnante en CV
     s'effondrant vers zero des N ~ 30 000. Le modele de Pitman-Yor de Rocher/Hendrickx/de
     Montjoye 2025 n'a toujours pas ete implemente (formule non verifiable de facon fiable
     dans le temps imparti) : limite assumee, pas un detail.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_echelle.py
===========================================================================
"""

import os
import sys
import zlib

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np                # noqa: E402
import pandas as pd                # noqa: E402
from sklearn.linear_model import LogisticRegression  # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                             # noqa: E402
from a2_commun import bootstrap_personnes, encodeur_demographies   # noqa: E402
from c7_reidentification import items_communs, rangs_attaque, REF_V4, REF_V13, DEMO  # noqa: E402

GRAINE = 20260911
N_VALEURS = [50, 100, 250, 500, 1000, 2058]
N_REPETITIONS = 20
N_TIRAGES_LIENS = 3     # reduit de 20 (C7) a 3 : le cout scale en N^2, 20 x N x config
RICHE = "JSON Persona - GPT4.1"
PMM_NOM = "PMM k=5 (demographies)"
PLAFOND_NOM = "retest humain (plafond, vagues 1-3)"
K_PMM = 5
N_PLIS_PMM = 5
# Diagnostic de non-identifiabilite seulement (section 3), PAS une extrapolation :
# le plafond fixe par le contre-examen du 12 septembre 2026, ~2x le plus grand N mesure.
N_DIVERGENCE = 4000


def graine_nom(nom):
    """Un entier stable pour une chaine, contrairement a hash() qui varie d'un
    interpreteur a l'autre (PYTHONHASHSEED) : la reproductibilite l'exige. Meme fonction
    que c7_reidentification.graine_nom, redefinie ici pour ne rien importer de prive."""
    return zlib.crc32(nom.encode("utf-8"))


# ---------------------------------------------------------------------------
# 1. Comparateur statistique nouveau : PMM sur les demographies, 5 plis
# ---------------------------------------------------------------------------

def pmm_demographies(paq, codes_v4, items, k=K_PMM, n_plis=N_PLIS_PMM, graine=GRAINE):
    """Un jumeau statistique par appariement sur moyenne predite (PMM), sur les seules
    demographies (memes 14 questions que ce que Demographics Only recoit), 5 plis de
    personnes pour qu'aucune personne ne serve de donneur a elle-meme.

    Pour chaque item : regression logistique multinomiale des demographies vers l'item,
    ajustee sur le pli d'entrainement ; le donneur d'une personne du pli de test est tiree
    parmi les k personnes d'entrainement dont le vecteur de probabilites predites est le
    plus proche du sien (distance euclidienne), et la valeur imputee est la valeur
    OBSERVEE de ce donneur, jamais une valeur inventee. Retourne une matrice
    (n_personnes, len(items)) de memes codes entiers que codes_v4.
    """
    x = paq["demo"]["x"]
    n = codes_v4.shape[0]
    rng = np.random.default_rng([graine, 7])
    plis = np.array_split(rng.permutation(n), n_plis)
    out = np.full((n, len(items)), -1, dtype=np.int32)
    for i_pli in range(n_plis):
        te = plis[i_pli]
        tr = np.concatenate([plis[j] for j in range(n_plis) if j != i_pli])
        enc = encodeur_demographies(x[tr])
        Xt, Xe = enc.transform(x[tr]), enc.transform(x[te])
        for jj, j in enumerate(items):
            y = codes_v4[tr, j]
            obs = y >= 0
            if obs.sum() < 2 * k:
                out[te, jj] = codes_v4[rng.choice(tr[obs], size=len(te)), j] if obs.any() else -1
                continue
            classes = np.unique(y[obs])
            if len(classes) < 2:
                out[te, jj] = classes[0] if len(classes) else -1
                continue
            rang = {c: i for i, c in enumerate(classes)}
            modele = LogisticRegression(max_iter=1000, C=1.0)
            modele.fit(Xt[obs], np.array([rang[v] for v in y[obs]]))
            p_tr = np.zeros((obs.sum(), len(classes)))
            p_tr[:, modele.classes_] = modele.predict_proba(Xt[obs])
            p_te = np.zeros((len(te), len(classes)))
            p_te[:, modele.classes_] = modele.predict_proba(Xe)
            d2 = ((p_te[:, None, :] - p_tr[None, :, :]) ** 2).sum(axis=2)
            keff = min(k, d2.shape[1])
            prox = np.argpartition(d2, keff - 1, axis=1)[:, :keff]
            choix = rng.integers(0, keff, size=len(te))
            donneurs_tr = np.flatnonzero(obs)
            out[te, jj] = y[donneurs_tr[prox[np.arange(len(te)), choix]]]
        print(f"  PMM, pli {i_pli + 1}/{n_plis} termine", flush=True)
    return out


# ---------------------------------------------------------------------------
# 2. Courbe empirique : top-1 par taille de pool sous-echantillonnee
# ---------------------------------------------------------------------------

def top1_sous_pool(x, pool, n_pool, n_rep, rng, n_tirages=N_TIRAGES_LIENS):
    """n_rep valeurs de top-1 moyen, chacune sur un sous-pool aleatoire de taille n_pool
    tire sans remise dans les 2058 humains. Les personnes attaquees sont les membres du
    sous-pool eux-memes (elles y sont necessairement, puisque c'est leur propre cible) :
    c'est la lecture standard « taille de la base candidate » d'un risque de reidentification.
    """
    n_total = pool.shape[0]
    reps = np.empty(n_rep)
    for r in range(n_rep):
        idx = rng.choice(n_total, size=n_pool, replace=False)
        _, top1, _ = rangs_attaque(x[idx], pool[idx], np.arange(n_pool), rng, n_tirages)
        reps[r] = float(top1.mean())
    return reps


def courbe(configs, pool, rng_racine):
    lignes = []
    for nom, x in configs.items():
        for n_pool in N_VALEURS:
            rng = np.random.default_rng([GRAINE, rng_racine, n_pool, graine_nom(nom)])
            reps = top1_sous_pool(x, pool, n_pool, N_REPETITIONS, rng)
            m, bas, haut = bootstrap_personnes(reps, n_tirages=2000, graine=[GRAINE, n_pool])
            lignes.append({"configuration": nom, "n_pool": n_pool, "top1": m,
                            "top1_bas": bas, "top1_haut": haut,
                            "top1_hasard": 1.0 / n_pool, "n_repetitions": N_REPETITIONS})
            print(f"{nom} / N={n_pool} : top1={m:.4f} [{bas:.4f};{haut:.4f}]", flush=True)
    return pd.DataFrame(lignes)


# ---------------------------------------------------------------------------
# 3. Extrapolation : deux modeles simples declares, pas le Pitman-Yor de l'article
# ---------------------------------------------------------------------------

def ajuster_puissance(n_vals, y_vals):
    """log(y) = log(a) + b*log(n), moindres carres. y borne dans ]0, 1] par construction
    empirique (jamais 0 exactement dans nos donnees)."""
    logn, logy = np.log(n_vals), np.log(np.clip(y_vals, 1e-6, None))
    b, loga = np.polyfit(logn, logy, 1)
    return np.exp(loga), b


def predire_puissance(n, a, b):
    return a * np.power(n, b)


def ajuster_log(n_vals, y_vals):
    """y = a - b*log(n), moindres carres."""
    logn = np.log(n_vals)
    b_neg, a = np.polyfit(logn, y_vals, 1)
    return a, -b_neg


def predire_log(n, a, b):
    return a - b * np.log(n)


def cv_loo(n_vals, y_vals, ajuster, predire):
    """Validation croisee leave-one-out sur les points mesures : erreur quadratique
    moyenne quand chaque point est prediit par un modele ajuste sur les 5 autres."""
    erreurs = []
    for i in range(len(n_vals)):
        mask = np.arange(len(n_vals)) != i
        a, b = ajuster(n_vals[mask], y_vals[mask])
        pred = predire(n_vals[i], a, b)
        erreurs.append((pred - y_vals[i]) ** 2)
    return float(np.mean(erreurs))


MODELES = {"puissance": (ajuster_puissance, predire_puissance),
           "log": (ajuster_log, predire_log)}


def diagnostic_divergence(df_config, n_verif=N_DIVERGENCE):
    """PAS une extrapolation : un diagnostic de non-identifiabilite.

    Ajuste puissance et log sur les 6 points MESURES (50 a 2058), rapporte la qualite
    d'ajustement DANS ce domaine par CV LOO, puis evalue les deux formes cote a cote a
    n_verif (~2x le plus grand N mesure, jamais plus loin) pour exposer, sans la
    dissimuler sous un choix de modele, l'ampleur de leur desaccord des qu'on sort, meme
    un peu, du domaine mesure. Aucune valeur au-dela de n_verif n'est calculee ici.
    """
    n_vals = df_config["n_pool"].to_numpy(dtype=float)
    y_vals = df_config["top1"].to_numpy(dtype=float)

    err = {nom: cv_loo(n_vals, y_vals, aj, pr) for nom, (aj, pr) in MODELES.items()}
    out = {"cv_erreur_puissance": err["puissance"], "cv_erreur_log": err["log"],
           "modele_gagnant_cv_intra_domaine": min(err, key=err.get),
           "n_verif_divergence": n_verif}
    preds = {}
    for nom, (aj, pr) in MODELES.items():
        a0, b0 = aj(n_vals, y_vals)
        preds[nom] = float(np.clip(pr(n_verif, a0, b0), 0.0, 1.0))
        out[f"{nom}_pred_n_verif"] = preds[nom]
    out["divergence_absolue_n_verif"] = abs(preds["puissance"] - preds["log"])
    out["divergence_ratio_n_verif"] = (preds["puissance"] / preds["log"]
                                        if preds["log"] > 1e-12 else float("inf"))
    return out


# ---------------------------------------------------------------------------
# 4. Figure
# ---------------------------------------------------------------------------

def figure(df, chemin):
    fig, ax = plt.subplots(figsize=(7, 4.5))
    for nom, sous in df.groupby("configuration"):
        sous = sous.sort_values("n_pool")
        ax.errorbar(sous["n_pool"], sous["top1"] * 100,
                    yerr=[(sous["top1"] - sous["top1_bas"]) * 100,
                          (sous["top1_haut"] - sous["top1"]) * 100],
                    marker="o", capsize=3, label=nom)
    ax.set_xscale("log")
    ax.set_xlabel("taille du pool de candidats (N, echelle log)")
    ax.set_ylabel("top-1 (%)")
    ax.set_title("Reidentification C7 : top-1 selon la taille du pool")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(chemin, dpi=140)
    print(f"ecrit {chemin}", flush=True)


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    n_total = paq["n"]

    items = items_communs(codes, [REF_V4, REF_V13])
    pool_v4 = codes[REF_V4][:, items]
    pool_v13 = codes[REF_V13][:, items]
    print(f"{n_total} personnes, {len(items)} items communs", flush=True)

    print("\n--- construction du comparateur PMM k=5 (demographies) ---", flush=True)
    pmm = pmm_demographies(paq, codes[REF_V4], items)

    configs = {
        RICHE: codes[RICHE][:, items],
        DEMO: codes[DEMO][:, items],
        PMM_NOM: pmm,
        # Plafond : la personne elle-meme, vue a travers ses reponses vagues 1-3, attaque
        # le pool de vague 4. Meme pipeline, memes 60 items : la borne haute que le
        # contre-examen du 11 septembre 2026 rapporte a 81,6 % sur le pool complet.
        PLAFOND_NOM: pool_v13,
    }

    print("\n--- courbe empirique, top-1 par taille de pool (resultat principal) ---",
          flush=True)
    df = courbe(configs, pool_v4, rng_racine=1)
    T1.ecrire(df, "c7-echelle.csv")

    print("\n--- diagnostic de non-identifiabilite (PAS une extrapolation) ---", flush=True)
    lignes_diag = []
    for nom in [RICHE, DEMO, PMM_NOM]:
        sous = df[df.configuration == nom]
        res = diagnostic_divergence(sous)
        res["configuration"] = nom
        lignes_diag.append(res)
        print(f"{nom} : gagnant CV intra-domaine = {res['modele_gagnant_cv_intra_domaine']} "
              f"(CV puissance={res['cv_erreur_puissance']:.6f}, "
              f"CV log={res['cv_erreur_log']:.6f}) ; a N={N_DIVERGENCE} : "
              f"puissance={res['puissance_pred_n_verif']*100:.3f} %, "
              f"log={res['log_pred_n_verif']*100:.3f} % "
              f"(ratio {res['divergence_ratio_n_verif']:.2f})", flush=True)
    df_diag = pd.DataFrame(lignes_diag)
    T1.ecrire(df_diag, "c7-echelle-diagnostic.csv")

    try:
        figure(df, os.path.join(T1.SORTIE, "c7-echelle.png"))
    except Exception as e:
        print(f"figure non produite : {e}", flush=True)

    print("\n--- rapport riche/demo, sur la courbe MESUREE seulement ---", flush=True)
    for n in N_VALEURS:
        r = df[(df.configuration == RICHE) & (df.n_pool == n)].top1.iloc[0]
        d = df[(df.configuration == DEMO) & (df.n_pool == n)].top1.iloc[0]
        print(f"N={n} : ratio riche/demo = {r / d:.1f}", flush=True)

    print("\n--- normalisation par le plafond humain (retest vagues 1-3) ---", flush=True)
    for n in N_VALEURS:
        p = df[(df.configuration == PLAFOND_NOM) & (df.n_pool == n)].top1.iloc[0]
        for nom in [RICHE, DEMO, PMM_NOM]:
            v = df[(df.configuration == nom) & (df.n_pool == n)].top1.iloc[0]
            print(f"N={n}, {nom} : {v*100:.2f} % = {v / p * 100:.1f} % du plafond "
                  f"({p*100:.1f} %)", flush=True)


if __name__ == "__main__":
    main()
