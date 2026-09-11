"""
c7_generateur : un generateur statistique individualise fuit-il autant qu'un jumeau LLM,
a exactitude egale ?

===========================================================================
PREENREGISTREMENT : resultats/c7-generateur-preenregistrement.md, ecrit le 12 septembre 2026,
AVANT ce calcul.

OBJECTION TRANCHEE ICI (cf. resultats/c7-contre-examen-2026-09-11.md) : PMM et B2 sont des
PREDICTEURS, qui tendent vers le mode, pas des GENERATEURS individualises. Un relecteur peut
dire que tout generateur conditionne sur la personne identifierait autant que le jumeau. Ce
script construit deux generateurs individualises, les calibre a l'exactitude du jumeau LLM sur
les 60 items de l'attaque (~0,59), et rejoue l'attaque de reidentification dessus.

GENERATEURS, tous conditionnes sur le meme contexte que t1_baselines (494 items de contexte
des vagues 1-3 + 14 demographies), JAMAIS sur les items cibles de vague 4 :
  G-LR      regression logistique multinomiale par item, TIRAGE dans la distribution predite
            (temperature T), au lieu de l'argmax de B1/B2/PMM. C'est la difference cle.
  G-copule  memes probabilites conditionnelles par item que G-LR, mais les 60 tirages d'une
            meme personne sont correles par une copule gaussienne (scores normaux par rang,
            correlation estimee sur le pli d'entrainement seul), pour reproduire la structure
            de dependance entre items en plus de la marginale personnalisee.
  CART sequentiel (synthpop) : absent de l'environnement Python (`synthpop`, `copulas` non
            installes) -> non teste, comme prevu au point 1 de la mission.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                les quinze tables de Twin
  t1_baselines.plis                le decoupage en 5 plis de personnes, meme graine
  c7_reidentification.items_communs   les 60 items toujours renseignes
  c7_reidentification.rangs_attaque   l'attaque de reidentification et ses garde-fous
  c7_reidentification.graine_nom      une graine stable par nom
  a2_commun.bootstrap_personnes       l'intervalle de confiance par reechantillonnage

CE QUI EST NOUVEAU ICI : les deux generateurs individualises, le balayage de temperature pour
caler l'exactitude sur celle du jumeau, la copule gaussienne par pli.

ETHIQUE : aucun pid ni appariement individuel n'est jamais imprime ou ecrit, seulement des
taux agreges. Aucun appel de modele de langage, aucun reseau. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_generateur.py
===========================================================================
"""

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from scipy.stats import norm
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                            # noqa: E402
import t1_baselines as TB                                          # noqa: E402
from a2_commun import bootstrap_personnes, est_manquant             # noqa: E402
from c7_reidentification import (                                  # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)

GRAINE = 20260912
CIBLE_ACC = 0.590     # exactitude sur 60 items de JSON Persona GPT4.1, c7-contre-examen
GRILLE_T = [0.02, 0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.6, 0.8, 1.0, 1.5, 2.0, 3.0]
N_REP_CALIB = 2        # tirages de generation par point de la grille, calibration
N_REP_FINAL = 5         # tirages de generation pour le resultat rapporte
N_BOOTSTRAP = 2000


def _texte(mat):
    """Une matrice objet en chaines, un manquant devenant une modalite explicite. Meme
    convention triviale que t1_baselines._texte / a35_commun.texte, recopiee ici en trois
    lignes plutot qu'importee d'un module prive."""
    out = np.empty(mat.shape, dtype=object)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            v = mat[i, j]
            out[i, j] = "manquant" if est_manquant(v) else str(v)
    return out


def construire_Z(paq):
    """Le meme vecteur de conditionnement que PMM dans t1_baselines : contexte des vagues
    1-3 (494 items, jamais reposes en vague 4) + 14 demographies. Jamais les items cibles."""
    x, ctx = paq["demo"]["x"], paq["demo"]["ctx"]
    return np.concatenate([_texte(ctx), x.astype(object)], axis=1)


def ajuster_items(paq, items, dec):
    """Une regression logistique multinomiale par item et par pli (hors echantillon), sur
    Z. Renvoie les probabilites predites pour TOUTE la population (proba) et leur
    couverture, dans l'espace commun k_max de paq. Rien n'est encore echantillonne ici :
    c'est la seule brique partagee par G-LR et G-copule."""
    y = paq["codes"][REF_V4]
    n, k_max = paq["n"], paq["k_max"]
    Z = construire_Z(paq)
    proba = np.zeros((n, len(items), k_max))
    couverture = np.zeros((n, len(items)), dtype=bool)
    for tr, te in dec:
        enc = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
        enc.fit(Z[tr])
        Zt, Ze = enc.transform(Z[tr]), enc.transform(Z[te])
        for jj, j in enumerate(items):
            col = y[tr, j]
            obs = col >= 0
            if obs.sum() < 5:
                continue
            classes = np.unique(col[obs])
            if len(classes) == 1:
                proba[te, jj, classes[0]] = 1.0
                couverture[te, jj] = True
                continue
            mod = LogisticRegression(max_iter=1000, C=1.0)
            mod.fit(Zt[obs], col[obs])
            p = mod.predict_proba(Ze)
            for k_local, c in enumerate(mod.classes_):
                proba[te, jj, c] = p[:, k_local]
            couverture[te, jj] = True
    return proba, couverture


def scores_normaux(col):
    """Un vecteur de codes entiers sans manquant devient des scores normaux par rang
    (regle du milieu de bloc pour les ex aequo) : la brique standard d'une copule gaussienne
    sur des variables discretes (transformation normale par rang, ou NORTA)."""
    n = len(col)
    valeurs, inverse, comptes = np.unique(col, return_inverse=True, return_counts=True)
    cum = np.concatenate(([0], np.cumsum(comptes)))
    milieu = (cum[:-1] + cum[1:] + 1) / 2.0
    u = milieu[inverse] / (n + 1)
    return norm.ppf(u)


def correlations_par_pli(y, items, dec, reg=0.02):
    """La correlation (60x60) entre les scores normaux des items, estimee sur le pli
    d'ENTRAINEMENT seul (jamais sur les personnes attaquees de ce pli), regularisee vers
    l'identite pour une factorisation de Cholesky stable."""
    Ls = []
    for tr, _ in dec:
        Z = np.column_stack([scores_normaux(y[tr, j]) for j in items])
        R = np.corrcoef(Z, rowvar=False)
        R = (1 - reg) * R + reg * np.eye(R.shape[0])
        Ls.append(np.linalg.cholesky(R))
    return Ls


def _poids(p, idx, T):
    """Les poids de tirage sur les classes de support idx, temperature T. T -> 0 degenere
    vers l'argmax (utile seulement pour situer le plafond, jamais rapporte comme generateur)."""
    if T <= 1e-6:
        w = np.zeros(len(idx))
        w[np.argmax(p[idx])] = 1.0
        return w
    logw = np.log(p[idx]) / T
    logw -= logw.max()
    w = np.exp(logw)
    return w / w.sum()


def echantillonner_independant(proba, couverture, T, rng):
    """G-LR : un tirage independant par item dans la distribution predite (temperature T).
    C'est la difference cle avec B1/B2/PMM, qui renvoient tous l'argmax."""
    n, m, _ = proba.shape
    out = np.full((n, m), -1, dtype=np.int64)
    for i in range(n):
        for j in range(m):
            if not couverture[i, j]:
                continue
            p = proba[i, j]
            idx = np.flatnonzero(p > 0)
            w = _poids(p, idx, T)
            out[i, j] = idx[rng.choice(len(idx), p=w)]
    return out


def echantillonner_copule(proba, couverture, fold_id, Ls, T, rng):
    """G-copule : memes probabilites personnalisees que G-LR, mais les 60 tirages d'une
    meme personne partagent une meme copule gaussienne (Ls[pli]), inversee item par item
    via la CDF personnalisee (temperature T)."""
    n, m, _ = proba.shape
    out = np.full((n, m), -1, dtype=np.int64)
    for i in range(n):
        L = Ls[fold_id[i]]
        u = norm.cdf(L @ rng.standard_normal(m))
        for j in range(m):
            if not couverture[i, j]:
                continue
            p = proba[i, j]
            idx = np.flatnonzero(p > 0)
            w = _poids(p, idx, T)
            pos = min(int(np.searchsorted(np.cumsum(w), u[j], side="right")), len(idx) - 1)
            out[i, j] = idx[pos]
    return out


def exactitude_personne(gen, verite, items):
    """Part des 60 items cibles correctement retrouves, une valeur par personne."""
    v = verite[:, items]
    valide = v >= 0
    juste = (gen == v) & valide
    n = valide.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, juste.sum(axis=1) / np.maximum(n, 1), np.nan)


def calibrer(nom, generer_fn, verite, items, cible, grille, graine, n_rep=N_REP_CALIB):
    """Balaie la grille de temperatures, releve l'exactitude moyenne (n_rep tirages par
    point), et choisit le T dont l'exactitude est la plus proche de la cible. Si le plafond
    du generateur (T le plus bas de la grille) reste sous la cible, ce T minimal est choisi
    par construction (le plus proche), et l'ecart doit etre rapporte tel quel."""
    lignes = []
    for T in grille:
        accs = []
        for r in range(n_rep):
            rng = np.random.default_rng([graine, graine_nom(nom), r, int(T * 1000)])
            gen = generer_fn(T, rng)
            accs.append(float(np.nanmean(exactitude_personne(gen, verite, items))))
        lignes.append({"generateur": nom, "T": T, "exactitude": float(np.mean(accs))})
    df = pd.DataFrame(lignes)
    idx = (df["exactitude"] - cible).abs().idxmin()
    choix = df.loc[idx]
    return df, float(choix["T"]), float(choix["exactitude"])


def attaquer(nom, gen_list, pool, graine, n_bootstrap=N_BOOTSTRAP):
    """Rejoue c7_reidentification.rangs_attaque sur n_rep tirages de generation
    independants, moyenne le rang/top1/top10 par personne sur ces tirages (pour lisser le
    bruit d'echantillonnage du generateur), puis l'IC par bootstrap sur les personnes."""
    n = pool.shape[0]
    couverts = np.arange(n)
    top1s, top10s, rangs = [], [], []
    for r, gen in enumerate(gen_list):
        rng = np.random.default_rng([graine, graine_nom(nom), 500, r])
        rang, top1, top10 = rangs_attaque(gen, pool, couverts, rng)
        top1s.append(top1)
        top10s.append(top10)
        rangs.append(rang)
    top1_m, top10_m, rang_m = np.mean(top1s, axis=0), np.mean(top10s, axis=0), np.mean(rangs, axis=0)
    m_t1, b_t1, h_t1 = bootstrap_personnes(top1_m, n_bootstrap, [GRAINE, 700, graine_nom(nom)])
    m_t10, b_t10, h_t10 = bootstrap_personnes(top10_m, n_bootstrap, [GRAINE, 701, graine_nom(nom)])
    return {
        "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
        "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
        "rang_median": float(np.median(rang_m)), "top1_hasard": 1.0 / n,
    }


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t_total = time.time()
    paq = T1.charger()
    items = items_communs(paq["codes"], [REF_V4, REF_V13])
    y = paq["codes"][REF_V4]
    n = paq["n"]
    print(f"{n} personnes, {len(items)} items communs, {time.time() - t_total:.0f}s", flush=True)

    dec = TB.plis(n, GRAINE)
    fold_id = np.full(n, -1, dtype=int)
    for f, (_, te) in enumerate(dec):
        fold_id[te] = f

    t0 = time.time()
    proba, couverture = ajuster_items(paq, items, dec)
    print(f"probabilites ajustees ({time.time() - t0:.0f}s), "
          f"couverture moyenne {couverture.mean():.4f}", flush=True)

    t0 = time.time()
    Ls = correlations_par_pli(y, items, dec)
    print(f"correlations par pli ({time.time() - t0:.0f}s)", flush=True)

    pool = y[:, items]

    def gen_lr(T, rng):
        return echantillonner_independant(proba, couverture, T, rng)

    def gen_cop(T, rng):
        return echantillonner_copule(proba, couverture, fold_id, Ls, T, rng)

    t0 = time.time()
    df_lr, T_lr, acc_lr = calibrer("G-LR", gen_lr, y, items, CIBLE_ACC, GRILLE_T, GRAINE)
    df_cop, T_cop, acc_cop = calibrer("G-copule", gen_cop, y, items, CIBLE_ACC, GRILLE_T, GRAINE)
    print(f"calibration ({time.time() - t0:.0f}s) : G-LR T={T_lr} exactitude={acc_lr:.4f} ; "
          f"G-copule T={T_cop} exactitude={acc_cop:.4f} (cible {CIBLE_ACC})", flush=True)
    T1.ecrire(pd.concat([df_lr, df_cop], ignore_index=True), "c7-generateur-calibration.csv")

    t0 = time.time()
    gens_lr = [gen_lr(T_lr, np.random.default_rng([GRAINE, 900, r])) for r in range(N_REP_FINAL)]
    gens_cop = [gen_cop(T_cop, np.random.default_rng([GRAINE, 901, r])) for r in range(N_REP_FINAL)]
    res_lr = attaquer("G-LR", gens_lr, pool, GRAINE)
    res_cop = attaquer("G-copule", gens_cop, pool, GRAINE)
    print(f"attaque ({time.time() - t0:.0f}s)", flush=True)

    lignes = []
    for nom, T, acc, res in [("G-LR", T_lr, acc_lr, res_lr), ("G-copule", T_cop, acc_cop, res_cop)]:
        ligne = {"generateur": nom, "T_calibre": T, "exactitude_60": acc}
        ligne.update(res)
        lignes.append(ligne)
        print(f"{nom} : exactitude={acc:.4f} top1={res['top1']:.4f} "
              f"[{res['top1_bas']:.4f};{res['top1_haut']:.4f}] top10={res['top10']:.4f} "
              f"rang_med={res['rang_median']:.1f} / {pool.shape[0]}", flush=True)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-generateur-resultats.csv")
    print(f"TOTAL {time.time() - t_total:.0f}s", flush=True)


if __name__ == "__main__":
    main()
