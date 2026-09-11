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
     repetitions), pour le meilleur jumeau riche de C7, Demographics Only et ce PMM.
  3. L'extrapolation par deux modeles simples declares au preenregistrement (loi
     puissance, loi logarithmique), le modele de Pitman-Yor de Rocher/Hendrickx/de
     Montjoye 2025 ayant ete juge hors de portee fiable dans le temps imparti (section 2
     du preenregistrement) : SES DEUX PARAMETRES DEMANDENT DES FONCTIONS DIGAMMA INVERSES
     ET DES RAPPORTS DE GAMMA QUE NOUS N'AVONS PAS PU VERIFIER CONTRE L'ARTICLE ORIGINAL
     (paywall pendant la fenetre de calcul). L'extrapolation qui suit est DECLAREE
     INDICATIVE, pas une preuve.

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
K_PMM = 5
N_PLIS_PMM = 5
N_EXTRAPOLATION = [10_000, 100_000, 1_000_000]
N_BOOTSTRAP_EXTRAPOLATION = 500


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


def extrapoler(df_config, graine):
    """Ajuste puissance ET log sur les 6 points mesures (les deux sont gardes et
    rapportes, pas seulement le gagnant), choisit le modele retenu par CV LOO, extrapole
    a N_EXTRAPOLATION avec IC par reechantillonnage : a chaque tirage, chaque point
    d'ancrage est perturbe dans sa propre bande de confiance (loi normale, ecart type
    approx = (haut-bas)/(2*1.96)), les deux modeles sont reajustes, puis evalues aux N
    d'extrapolation. Percentile 2,5-97,5 sur ces tirages = l'IC rapporte pour chacun.

    Le clip a 0 sur predire_log rend visible, plutot que masque, le mode d'echec connu
    d'un modele lineaire en log(N) extrapole loin hors de son domaine ajuste : au-dela du
    N ou a - b*log(N) croise zero, la prediction est nulle par construction, pas un signal
    substantif. C'est precisement pourquoi l'extrapolation est declaree indicative.
    """
    n_vals = df_config["n_pool"].to_numpy(dtype=float)
    y_vals = df_config["top1"].to_numpy(dtype=float)
    se = (df_config["top1_haut"] - df_config["top1_bas"]).to_numpy(dtype=float) / (2 * 1.96)
    se = np.clip(se, 1e-5, None)

    err = {nom: cv_loo(n_vals, y_vals, aj, pr) for nom, (aj, pr) in MODELES.items()}
    retenu = min(err, key=err.get)

    rng = np.random.default_rng(graine)
    tirages = {nom: {n: [] for n in N_EXTRAPOLATION} for nom in MODELES}
    for _ in range(N_BOOTSTRAP_EXTRAPOLATION):
        y_pert = np.clip(rng.normal(y_vals, se), 1e-6, 1.0)
        for nom, (aj, pr) in MODELES.items():
            try:
                a, b = aj(n_vals, y_pert)
            except Exception:
                continue
            for n in N_EXTRAPOLATION:
                tirages[nom][n].append(float(np.clip(pr(n, a, b), 0.0, 1.0)))

    out = {"cv_erreur_puissance": err["puissance"], "cv_erreur_log": err["log"],
           "modele_retenu": retenu}
    for nom, (aj, pr) in MODELES.items():
        a0, b0 = aj(n_vals, y_vals)
        for n in N_EXTRAPOLATION:
            vals = np.array(tirages[nom][n]) if tirages[nom][n] else np.array([pr(n, a0, b0)])
            out[f"{nom}_pred_{n}"] = float(np.clip(pr(n, a0, b0), 0.0, 1.0))
            out[f"{nom}_pred_{n}_bas"] = float(np.percentile(vals, 2.5))
            out[f"{nom}_pred_{n}_haut"] = float(np.percentile(vals, 97.5))
            if nom == retenu:
                out[f"pred_{n}"] = out[f"{nom}_pred_{n}"]
                out[f"pred_{n}_bas"] = out[f"{nom}_pred_{n}_bas"]
                out[f"pred_{n}_haut"] = out[f"{nom}_pred_{n}_haut"]
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
    print(f"{n_total} personnes, {len(items)} items communs", flush=True)

    print("\n--- construction du comparateur PMM k=5 (demographies) ---", flush=True)
    pmm = pmm_demographies(paq, codes[REF_V4], items)

    configs = {
        RICHE: codes[RICHE][:, items],
        DEMO: codes[DEMO][:, items],
        PMM_NOM: pmm,
    }

    print("\n--- courbe empirique, top-1 par taille de pool ---", flush=True)
    df = courbe(configs, pool_v4, rng_racine=1)
    T1.ecrire(df, "c7-echelle.csv")

    print("\n--- extrapolation (modeles declares, pas le Pitman-Yor de l'article) ---",
          flush=True)
    lignes_extra = []
    for nom in configs:
        sous = df[df.configuration == nom]
        res = extrapoler(sous, graine=[GRAINE, graine_nom(nom)])
        res["configuration"] = nom
        lignes_extra.append(res)
        print(f"{nom} : modele retenu = {res['modele_retenu']} "
              f"(CV puissance={res['cv_erreur_puissance']:.6f}, "
              f"CV log={res['cv_erreur_log']:.6f})", flush=True)
        for n in N_EXTRAPOLATION:
            print(f"    N={n} : top1 = {res[f'pred_{n}']*100:.3f} % "
                  f"[{res[f'pred_{n}_bas']*100:.3f} ; {res[f'pred_{n}_haut']*100:.3f}]",
                  flush=True)
    df_extra = pd.DataFrame(lignes_extra)
    T1.ecrire(df_extra, "c7-echelle-extrapolation.csv")

    try:
        figure(df, os.path.join(T1.SORTIE, "c7-echelle.png"))
    except Exception as e:
        print(f"figure non produite : {e}", flush=True)

    print("\n--- rapport au comparateur demographique, a chaque N d'extrapolation ---",
          flush=True)
    riche_row = df_extra[df_extra.configuration == RICHE].iloc[0]
    demo_row = df_extra[df_extra.configuration == DEMO].iloc[0]
    for n in N_EXTRAPOLATION:
        ratio = riche_row[f"pred_{n}"] / demo_row[f"pred_{n}"] if demo_row[f"pred_{n}"] > 0 else float("inf")
        print(f"N={n} : ratio riche/demo = {ratio:.1f}", flush=True)


if __name__ == "__main__":
    main()
