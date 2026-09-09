"""
a8_twin_items : Twin-2K-500 item par item, ou exactement le modele de langage gagne.

Repond a deux limites du rapport a2 :
  - section 5, hypothese explicitement etiquetee a verifier : "la cible de la vague 4 est
    faite d'experiences d'heuristiques et de biais, ou la reponse depend de la structure du
    probleme bien plus que de qui repond" ;
  - limite 5 : "un seul modele de langage sert de repere sur Twin. Le classement modele
    contre baseline pourrait bouger avec un autre modele." Les treize configurations
    publiees par les auteurs sont ici evaluees, pas deux.

Deux mesures de la part de variance expliquee sont produites par item, et elles servent a
tester l'hypothese ci dessus :
  - R2 de McFadden hors echantillon des demographies, calcule sur la loi predite par la
    regression logistique, rapporte a la loi marginale ;
  - le meme, a partir de la loi des k voisins.
Un item ou ces deux quantites sont proches de zero est un item que la personne n'explique
pas. Si l'hypothese de a2 est juste, c'est la que l'avantage du modele de langage se
concentre.

Entree  : data/twin2k500, dont les treize simulations telechargees par
          analyses/a8_telecharger_twin_llm.py.
Sortie  : resultats/a8-twin-par-bloc.csv, resultats/a8-twin-par-item.csv,
          resultats/a8-twin-correlations.csv.

Aucun appel de modele. Duree : environ cinq minutes.

Usage : .venv/bin/python analyses/a8_twin_items.py
"""

import time
from collections import Counter

import numpy as np
from scipy.stats import spearmanr
from sklearn.linear_model import LogisticRegression

import a8_commun as C
from a2_commun import (b0_marginale, b1_logistique, b2_voisins, distance_hamming, en_codes,
                       encodeur_demographies, est_manquant)

BLOC_MIN = 3          # au dessous, les blocs sont regroupes : un item ne fait pas un chiffre


def loi_marginale(y_train):
    obs = [v for v in y_train if not est_manquant(v)]
    n = len(obs)
    cpt = Counter(obs)
    return {mod: (c + 0.5) / (n + 0.5 * len(cpt)) for mod, c in cpt.items()}, len(cpt)


def loi_logistique(xt, y_train, xe):
    """Loi predite par la regression sur demographies, pour le R2 de McFadden.

    C'est le meme modele que b1_logistique de a2, avec les memes reglages ; seule la
    sortie change, on garde la loi au lieu de la classe la plus probable. La prediction
    publiee reste celle de b1_logistique, ce calcul ne sert qu'au diagnostic.
    """
    obs = np.array([not est_manquant(v) for v in y_train])
    if obs.sum() < 5:
        return None, None
    y = np.asarray(y_train, dtype=object)[obs]
    classes = list(dict.fromkeys(y))
    if len(classes) == 1:
        return None, None
    rang = {c: i for i, c in enumerate(classes)}
    modele = LogisticRegression(max_iter=2000, C=1.0)
    modele.fit(xt[obs], np.array([rang[v] for v in y]))
    return modele.predict_proba(xe), {c: i for i, c in enumerate(classes)}


def loi_voisins(distances, y_train, k):
    """Loi des k voisins, lissee, pour le R2 de McFadden du conditionnement par voisins."""
    y = np.asarray(y_train, dtype=object)
    obs = np.array([not est_manquant(v) for v in y])
    if obs.sum() < 1:
        return None, None
    d = distances[:, obs]
    y_obs = y[obs]
    classes = list(dict.fromkeys(y_obs))
    rang = {c: i for i, c in enumerate(classes)}
    k_eff = min(k, d.shape[1])
    ordre = np.argpartition(d, k_eff - 1, axis=1)[:, :k_eff]
    P = np.zeros((d.shape[0], len(classes)))
    for i in range(d.shape[0]):
        for v in y_obs[ordre[i]]:
            P[i, rang[v]] += 1
    P = (P + 0.5) / (k_eff + 0.5 * len(classes))
    return P, rang


def main():
    t0 = time.time()
    d0 = C.charger_twin()
    y, x, ctx = d0["y"], d0["x"], d0["ctx"]
    n, m = y.shape
    cibles, blocs_cible = d0["cibles"], d0["blocs_cibles"]
    plis = C.plis_twin(n)
    masque = np.array([[not est_manquant(v) for v in l] for l in y])
    codes = en_codes(ctx)
    rng = np.random.default_rng(C.GRAINE)

    pred = {nom: np.empty((n, m), dtype=object)
            for nom in ["B0 mode", "B1 argmax", "B2 argmax"]}
    ll_nul = np.zeros(m)
    ll_demo = np.zeros(m)
    ll_vois = np.zeros(m)
    n_ll = np.zeros(m)

    for i_pli, (tr, te) in enumerate(plis):
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        dist = distance_hamming(codes[te], codes[tr])
        for j in range(m):
            pred["B0 mode"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng, mode=True)[:, None]
            pred["B1 argmax"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
            pred["B2 argmax"][np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], C.K_A2, rng)[:, None]
            # Diagnostic : vraisemblance hors echantillon des trois lois.
            marg, _ = loi_marginale(y[tr, j])
            Pd, rd = loi_logistique(xt, y[tr, j], xe)
            Pv, rv = loi_voisins(dist, y[tr, j], C.K_A2)
            for i_local, i in enumerate(te):
                v = y[i, j]
                if est_manquant(v) or v not in marg:
                    continue
                n_ll[j] += 1
                ll_nul[j] += np.log(marg[v])
                ll_demo[j] += (np.log(Pd[i_local, rd[v]]) if Pd is not None and v in rd
                               else np.log(marg[v]))
                ll_vois[j] += (np.log(Pv[i_local, rv[v]]) if Pv is not None and v in rv
                               else np.log(marg[v]))
        print(f"  pli {i_pli + 1}/{len(plis)} termine", flush=True)

    llm = C.charger_llm_twin(d0)
    yn = C.cible_twin_numerique(d0)

    def exactitude_item(p, verite, mq):
        acc = np.full(m, np.nan)
        for j in range(m):
            sel = mq[:, j]
            if sel.sum() == 0:
                continue
            acc[j] = float((p[sel, j] == verite[sel, j]).mean())
        return acc

    accs = {nom: exactitude_item(p, y, masque) for nom, p in pred.items()}
    # Stabilite test retest de l'item : la meme personne, la meme question, deux semaines
    # plus tot. C'est le plafond de fidelite individuelle item par item, et la variable qui
    # separe le mieux les blocs de la vague 4.
    retest = exactitude_item(np.where(masque, d0["y_retest"], None), y, masque)
    for libelle, spec in llm.items():
        mq = masque & spec["personnes"][:, None]
        accs[libelle] = exactitude_item(spec["matrice"], yn, mq)

    with np.errstate(divide="ignore", invalid="ignore"):
        r2_demo = 1.0 - ll_demo / ll_nul
        r2_vois = 1.0 - ll_vois / ll_nul

    # ---- tableau par item
    par_item = []
    for j in range(m):
        d = {"item": cibles[j], "bloc": blocs_cible[cibles[j]],
             "n_reponses": int(masque[:, j].sum()),
             "n_modalites": len({v for v in y[:, j] if not est_manquant(v)}),
             "retest_humain": float(retest[j]),
             "r2_demographies": float(r2_demo[j]), "r2_voisins": float(r2_vois[j])}
        for nom, a in accs.items():
            d[nom] = float(a[j])
        par_item.append(d)
    C.ecrire_csv(par_item, "a8-twin-par-item.csv")

    # ---- tableau par bloc
    comptes = Counter(blocs_cible[c] for c in cibles)
    groupes = {}
    for j, c in enumerate(cibles):
        b = blocs_cible[c]
        cle = b if comptes[b] >= BLOC_MIN else "autres experiences (blocs a 1 ou 2 items)"
        groupes.setdefault(cle, []).append(j)
    groupes["tous les items"] = list(range(m))

    par_bloc = []
    for cle, cols in groupes.items():
        base = {"bloc": cle, "n_items": len(cols),
                "retest_humain_moyen": float(np.nanmean(retest[cols])),
                "r2_demographies_moyen": float(np.nanmean(r2_demo[cols])),
                "r2_voisins_moyen": float(np.nanmean(r2_vois[cols]))}
        for nom, p in pred.items():
            moy, bas, haut = C.exactitude_sur(p, y, cols, masque)
            par_bloc.append({**base, "methode": nom, "exactitude": moy,
                             "ic_bas": bas, "ic_haut": haut, "n_personnes": n})
        for libelle, spec in llm.items():
            mq = masque & spec["personnes"][:, None]
            moy, bas, haut = C.exactitude_sur(spec["matrice"], yn, cols, mq)
            par_bloc.append({**base, "methode": libelle, "exactitude": moy,
                             "ic_bas": bas, "ic_haut": haut,
                             "n_personnes": spec["n_personnes"]})
    C.ecrire_csv(par_bloc, "a8-twin-par-bloc.csv")

    # ---- correlations : l'avantage du modele contre ce que la personne explique
    correlations = []
    meilleure_baseline = np.fmax(accs["B1 argmax"], accs["B2 argmax"])
    for libelle in llm:
        avantage = accs[libelle] - meilleure_baseline
        ok = ~np.isnan(avantage) & ~np.isnan(r2_demo) & ~np.isnan(r2_vois)
        rd = spearmanr(avantage[ok], r2_demo[ok])
        rv = spearmanr(avantage[ok], r2_vois[ok])
        ra = spearmanr(avantage[ok], accs["B0 mode"][ok])
        rr = spearmanr(avantage[ok], retest[ok])
        correlations.append({
            "configuration": libelle, "n_items": int(ok.sum()),
            "avantage_moyen": float(np.nanmean(avantage)),
            "items_ou_le_modele_gagne": int((avantage[ok] > 0).sum()),
            "spearman_avantage_r2_demographies": float(rd.statistic),
            "p_demographies": float(rd.pvalue),
            "spearman_avantage_r2_voisins": float(rv.statistic),
            "p_voisins": float(rv.pvalue),
            "spearman_avantage_exactitude_B0": float(ra.statistic),
            "p_B0": float(ra.pvalue),
            "spearman_avantage_retest_humain": float(rr.statistic),
            "p_retest": float(rr.pvalue),
        })
    C.ecrire_csv(correlations, "a8-twin-correlations.csv")
    print(f"duree {time.time() - t0:.0f} s")


if __name__ == "__main__":
    main()
