"""
a8_copule : la copule gaussienne comme baseline supplementaire sur le GSS.

Repond a la limite 8 du rapport a2 : "aucune copule gaussienne n'a ete construite, alors
que la passation la cite comme egalant 37 modeles. B2 en est un substitut non parametrique,
pas un equivalent."

Principe. Chaque item ordinal est vu comme la discretisation d'une variable latente
normale. Les seuils viennent de la marginale estimee sur le pli d'entrainement, la matrice
de correlation latente est estimee sur les scores normaux du meme pli, et la prediction est
la loi conditionnelle du latent cible sachant les latents des items de contexte. Rien de
tout cela ne regarde le pli de test.

Limite assumee, ecrite ici pour ne pas etre decouverte plus tard : la correlation latente
est estimee par la correlation de Pearson des scores normaux, qui approche la correlation
polychorique sans l'estimer par maximum de vraisemblance. C'est l'approximation usuelle,
elle sous estime legerement les correlations fortes.

Les items nominaux n'ont pas d'ordre, donc pas de seuil : la copule ne les couvre pas. Elle
est restreinte aux items ordinaux, reperes par `question_master/gss/groups/categorical.csv`,
colonne "Categorical" a N. Toutes les methodes comparees ici sont recalculees sur ces
memes items, sans quoi l'ecart viendrait du denominateur.

Entree  : data/osf-t6g7k-stanford.
Sortie  : resultats/a8-copule-gss.csv.

Aucun appel de modele. Duree : environ deux minutes.

Usage : .venv/bin/python analyses/a8_copule.py
"""

import time

import numpy as np
from scipy.stats import norm
from sklearn.model_selection import KFold

import a8_commun as C
from a2_commun import (b0_marginale, b1_logistique, b2_voisins, distance_hamming, en_codes,
                       encodeur_demographies, est_manquant)

GRILLE_LAMBDA = [0.01, 0.05, 0.10, 0.20, 0.40]


def items_ordinaux_utilisables(g):
    """Items ordinaux dont toutes les modalites observees figurent dans les options.

    La comparaison est faite en minuscules : le fichier de reponses est en minuscules, le
    question_master en capitales initiales. Un item dont une modalite observee n'apparait
    pas dans la liste d'options n'a pas d'ordre connu et sort de la copule.
    """
    gardes, ecartes = [], []
    for it in g["ordinaux"]:
        options = [str(o).strip().lower() for o in g["options"].get(it.lower(), [])]
        j = g["items"].index(it)
        observees = {str(v).strip().lower() for v in g["y1"][:, j] if not est_manquant(v)}
        if len(options) >= 2 and observees <= set(options):
            gardes.append(it)
        else:
            ecartes.append(it)
    return gardes, ecartes


def seuils_et_scores(y_train_col, ordre):
    """Seuils latents et scores normaux d'un item, estimes sur le pli d'entrainement.

    Retourne la liste des modalites de probabilite non nulle dans l'ordre de l'echelle,
    leurs seuils cumules dans l'espace latent, et l'esperance du latent dans chaque
    intervalle, qui sert de valeur numerique a la modalite.
    """
    v = [str(x).strip().lower() for x in y_train_col if not est_manquant(x)]
    n = len(v)
    effectifs = {m: 0 for m in ordre}
    for x in v:
        if x in effectifs:
            effectifs[x] += 1
    mods = [m for m in ordre if effectifs[m] > 0]
    p = np.array([effectifs[m] / n for m in mods])
    cum = np.clip(np.cumsum(p)[:-1], 1e-6, 1 - 1e-6)
    taus = np.concatenate([[-np.inf], norm.ppf(cum), [np.inf]])
    dens = norm.pdf(taus)
    dens[0] = 0.0
    dens[-1] = 0.0
    scores = (dens[:-1] - dens[1:]) / p
    return mods, taus, scores, p


def copule_pli(y_tr, y_te, ordres, blocs, lam):
    """Predit les items d'un pli de test par loi conditionnelle gaussienne.

    y_tr, y_te : matrices (personnes x items ordinaux) de chaines.
    ordres     : ordre de l'echelle par item.
    blocs      : decoupage des items en blocs ; le bloc courant est la cible, le reste est
                 le contexte disponible sur la personne testee. Meme regle que B2 dans a2.
    lam        : retrecissement de la matrice de correlation, (1 - lam) R + lam I.
    """
    m = y_tr.shape[1]
    tables = [seuils_et_scores(y_tr[:, j], ordres[j]) for j in range(m)]
    z_tr = np.zeros(y_tr.shape)
    z_te = np.zeros(y_te.shape)
    for j, (mods, taus, scores, _) in enumerate(tables):
        table = {mo: scores[i] for i, mo in enumerate(mods)}
        defaut = float(np.mean(scores))
        z_tr[:, j] = [table.get(str(x).strip().lower(), defaut) for x in y_tr[:, j]]
        z_te[:, j] = [table.get(str(x).strip().lower(), defaut) for x in y_te[:, j]]
    R = np.corrcoef(z_tr, rowvar=False)
    R = np.nan_to_num(R, nan=0.0)
    R = (1 - lam) * R + lam * np.eye(m)

    pred_argmax = np.empty(y_te.shape, dtype=object)
    pred_tirage = np.empty(y_te.shape, dtype=object)
    rng = np.random.default_rng(C.GRAINE)
    for bloc in blocs:
        ctx = np.setdiff1d(np.arange(m), bloc)
        A = np.linalg.inv(R[np.ix_(ctx, ctx)])
        Zc = z_te[:, ctx]
        for j in bloc:
            r = R[j, ctx]
            poids = A @ r
            mu = Zc @ poids
            var = max(1.0 - float(r @ poids), 1e-3)
            sd = np.sqrt(var)
            mods, taus, _, _ = tables[j]
            bornes = (taus[None, :] - mu[:, None]) / sd
            cdf = norm.cdf(bornes)
            proba = np.clip(cdf[:, 1:] - cdf[:, :-1], 1e-12, None)
            proba /= proba.sum(axis=1, keepdims=True)
            idx = proba.argmax(axis=1)
            pred_argmax[:, j] = [mods[i] for i in idx]
            tir = np.array([rng.choice(len(mods), p=pp) for pp in proba])
            pred_tirage[:, j] = [mods[i] for i in tir]
    return pred_argmax, pred_tirage


def main():
    t0 = time.time()
    g = C.charger_gss()
    gardes, ecartes = items_ordinaux_utilisables(g)
    print(f"{len(g['items'])} items cibles, {len(g['ordinaux'])} ordinaux au question_master, "
          f"{len(gardes)} retenus pour la copule")
    if ecartes:
        print(f"ecartes faute d'ordre exploitable : {', '.join(ecartes)}")

    cols = [g["items"].index(it) for it in gardes]
    y_complet = g["y1"]
    y = np.array([[str(v).strip().lower() for v in ligne] for ligne in y_complet[:, cols]],
                 dtype=object)
    ordres = [[str(o).strip().lower() for o in g["options"][it.lower()]] for it in gardes]
    n, m = y.shape
    plis, _ = C.grille_gss(n, len(g["items"]))
    rng_bl = np.random.default_rng(C.GRAINE)
    blocs = np.array_split(rng_bl.permutation(m), C.N_BLOCS)

    pred_arg = np.empty((n, m), dtype=object)
    pred_tir = np.empty((n, m), dtype=object)
    lambdas = []
    for i_pli, (tr, te) in enumerate(plis):
        # Choix du retrecissement par validation interne au pli d'entrainement.
        kf = KFold(n_splits=2, shuffle=True, random_state=C.GRAINE + i_pli)
        scores = {lam: 0.0 for lam in GRILLE_LAMBDA}
        for itr, ival in kf.split(tr):
            a, b = tr[itr], tr[ival]
            for lam in GRILLE_LAMBDA:
                p, _ = copule_pli(y[a], y[b], ordres, blocs, lam)
                scores[lam] += float((p == y[b]).mean())
        lam = max(GRILLE_LAMBDA, key=lambda l: scores[l])
        lambdas.append(lam)
        pa, pt = copule_pli(y[tr], y[te], ordres, blocs, lam)
        pred_arg[te] = pa
        pred_tir[te] = pt
        print(f"  pli {i_pli + 1}/{len(plis)} : retrecissement retenu {lam}", flush=True)

    # Les autres methodes, recalculees sur exactement les memes items.
    codes = en_codes(y_complet)
    x = g["x"]
    mtot = y_complet.shape[1]
    plis_c, blocs_c = C.grille_gss(n, mtot)
    rng = np.random.default_rng(C.GRAINE)
    autres = {nom: np.empty((n, mtot), dtype=object)
              for nom in ["B0 mode", "B0 tirage", "B1 argmax", "B1 tirage",
                          "B2 argmax", "B2 tirage"]}
    for tr, te in plis_c:
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        for j in cols:
            autres["B0 mode"][np.ix_(te, [j])] = b0_marginale(y_complet[tr, j], len(te), rng, mode=True)[:, None]
            autres["B0 tirage"][np.ix_(te, [j])] = b0_marginale(y_complet[tr, j], len(te), rng)[:, None]
            autres["B1 argmax"][np.ix_(te, [j])] = b1_logistique(xt, y_complet[tr, j], xe, rng)[:, None]
            autres["B1 tirage"][np.ix_(te, [j])] = b1_logistique(xt, y_complet[tr, j], xe, rng, tirage=True)[:, None]
        for bloc in blocs_c:
            contexte = np.setdiff1d(np.arange(mtot), bloc)
            d = distance_hamming(codes[np.ix_(te, contexte)], codes[np.ix_(tr, contexte)])
            for j in bloc:
                if j in set(cols):
                    autres["B2 argmax"][np.ix_(te, [j])] = b2_voisins(d, y_complet[tr, j], C.K_A2, rng)[:, None]
                    autres["B2 tirage"][np.ix_(te, [j])] = b2_voisins(d, y_complet[tr, j], C.K_A2, rng, tirage=True)[:, None]

    lignes = []

    def ajouter(nom, pred, verite):
        moy, bas, haut = C.exactitude_sur(pred, verite, list(range(pred.shape[1])))
        div = C.diversite_sur(pred, verite, list(range(pred.shape[1])))
        lignes.append({
            "methode": nom, "n_items": pred.shape[1], "exactitude": moy,
            "ic_bas": bas, "ic_haut": haut,
            "part_diversite_humaine": div["part_diversite_humaine"],
            "accord_par_paires": div["accord_par_paires"],
        })

    ajouter("copule gaussienne (argmax)", pred_arg, y)
    ajouter("copule gaussienne (tirage)", pred_tir, y)
    for nom, mat in autres.items():
        ajouter(nom, mat[:, cols], y_complet[:, cols])
    for libelle, mat in C.charger_agents_gss(g["items"]).items():
        ajouter(libelle, mat[:, cols], y_complet[:, cols])
    ajouter("humains reinterroges", g["y2"][:, cols], y_complet[:, cols])

    for l in lignes:
        print(f"{l['methode']:<34}{l['exactitude']:>9.4f}"
              f"{l['part_diversite_humaine'] * 100:>10.1f}%{l['accord_par_paires'] * 100:>10.1f}%")
    C.ecrire_csv(lignes, "a8-copule-gss.csv")
    C.ecrire_csv([{"pli": i + 1, "retrecissement": l} for i, l in enumerate(lambdas)],
                 "a8-copule-retrecissement.csv")
    print(f"duree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
