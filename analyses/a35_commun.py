"""
a35_commun : briques partagees par a35, "le modele de langage comme methode d'imputation".

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a2_commun,
a2_baselines_gss, a8_commun, a8_copule, a25_commun, a25_mesures, a28_commun, a29_commun,
a31_commun, a31_mecanismes. Les 1 052 personnes, les 149 items, les cinq plis, les cinq
blocs, les graines, les 150 personnes du run local, la definition des modalites
minoritaires et les estimateurs de dispersion viennent de la, sans une ligne recopiee.

Ce module porte quatre choses et rien d'autre.

  1. Les methodes d'imputation nouvelles, toutes construites sur le MEME decoupage que a2 :
     cinq plis sur les personnes, cinq blocs d'items, chaque couple (personne, item)
     predit exactement une fois, contexte = les 119 autres items plus les 11 attributs
     demographiques. Ce sont :
       E1  imputation par esperance : regression logistique multinomiale regularisee sur
           le contexte et les demographies, modalite la plus probable. C'est la
           "regression imputation" de van Buuren, celle dont le manuel dit qu'elle ecrase
           la dispersion residuelle et gonfle les associations.
       E2  imputation par tirage : le MEME modele, tirage dans la distribution predite.
           C'est la "stochastic regression imputation" de van Buuren, le correctif connu.
       PMM appariement sur moyenne predite, k donneurs. Le modele est le meme ; la valeur
           imputee est la valeur OBSERVEE d'un donneur tire parmi les k dont la prediction
           est la plus proche de celle du receveur.
       HD  hot deck par plus proche voisin, tirage parmi les k voisins. C'est exactement
           `B2 tirage` de a2, decline a plusieurs k.
       IM  imputation multiple : m tirages independants de E2, plus la modalite modale des
           m, plus les regles de Rubin sur les marginales.
     La copule gaussienne de a8 est reprise par import de a8_copule, sur ses 70 items
     ordinaux, avec le retrecissement 0,20 que a8 a retenu aux cinq plis.

  2. Le tableau a quatre cases : exactitude par personne, ratios inter et intra de a1 en
     Gini Simpson sans biais, ratio de dispersion totale, diversite conservee et accord
     par paires de a0, rappel et precision minoritaires de a29, rapport groupe sur
     personne de a31.

  3. Le bootstrap sur les PERSONNES, applique au meme tirage pour toutes les methodes, ce
     qui rend les contrastes apparies. Deux reponses d'une meme personne ne sont pas
     independantes : un bootstrap sur les cellules donnerait un intervalle faussement
     etroit.

  4. Une version vectorisee de la decomposition de dispersion, employee UNIQUEMENT dans
     la boucle de bootstrap pour des raisons de temps. Elle est verifiee contre
     a28_commun.dispersion_item sur l'echantillon complet, item par item, et l'ecart
     maximal est rapporte dans le rapport. Les valeurs ponctuelles publiees viennent de
     a28_commun.dispersion_item et non de cette version.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import pickle
import sys

# Limite de quatre coeurs, posee avant l'import de numpy sinon elle est sans effet.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a28_commun as C28
import a29_commun as C29
from a2_baselines_gss import GRAINE, charger, grille
from a2_commun import (accord_par_paires, b2_voisins, bootstrap_personnes,
                       distance_hamming, en_codes, entropie, est_manquant,
                       exactitude_par_personne)
from a8_commun import modalites_minoritaires

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

GRAINE_A35 = 20260908
LAMBDA_COPULE = 0.20          # retrecissement retenu par a8 aux cinq plis
SEUIL_MINORITE = 0.10
AXE_PRINCIPAL = "political_ideology"
AXE_SECONDAIRE = "profil croise"

ecrire = C28.ecrire
holm = C28.holm
benjamini_hochberg = C28.benjamini_hochberg


# ---------------------------------------------------------------------------
# Nomenclature des methodes
# ---------------------------------------------------------------------------
# Chaque methode porte trois etiquettes : sa FAMILLE au sens de la statistique d'enquete,
# son REGIME (esperance, c'est a dire predicteur ponctuel, ou tirage), et son
# CONDITIONNEMENT, c'est a dire ce que la methode sait de la personne. Le conditionnement
# est ce qui rend deux methodes comparables ou non : opposer une methode qui ne voit que
# onze attributs a une methode qui voit 119 reponses n'a pas de sens, et le tableau le
# signale au lieu de le cacher.

FAMILLE = {
    "B0 mode": "marginale",
    "B0 tirage": "marginale",
    "B1 argmax": "regression sur demographies",
    "B1 tirage": "regression sur demographies",
    "B3 foret": "foret sur demographies",
    "E1 regression contexte argmax": "regression sur contexte",
    "E2 regression contexte tirage": "regression sur contexte",
    "PMM k=5": "appariement sur moyenne predite",
    "PMM k=10": "appariement sur moyenne predite",
    "IM m=10 mode des m": "imputation multiple",
    "hot deck k=5 tirage": "hot deck",
    "hot deck k=10 tirage": "hot deck",
    "B2 argmax": "hot deck",
    "B2 tirage": "hot deck",
    "copule argmax": "copule gaussienne",
    "copule tirage": "copule gaussienne",
}

REGIME = {
    "B0 mode": "esperance", "B0 tirage": "tirage",
    "B1 argmax": "esperance", "B1 tirage": "tirage",
    "B3 foret": "esperance",
    "E1 regression contexte argmax": "esperance",
    "E2 regression contexte tirage": "tirage",
    "PMM k=5": "tirage", "PMM k=10": "tirage",
    "IM m=10 mode des m": "esperance",
    "hot deck k=5 tirage": "tirage", "hot deck k=10 tirage": "tirage",
    "B2 argmax": "esperance", "B2 tirage": "tirage",
    "copule argmax": "esperance", "copule tirage": "tirage",
}

CONDITIONNEMENT = {
    "B0 mode": "rien", "B0 tirage": "rien",
    "B1 argmax": "11 demographies", "B1 tirage": "11 demographies",
    "B3 foret": "11 demographies",
    "E1 regression contexte argmax": "119 items et 11 demographies",
    "E2 regression contexte tirage": "119 items et 11 demographies",
    "PMM k=5": "119 items et 11 demographies",
    "PMM k=10": "119 items et 11 demographies",
    "IM m=10 mode des m": "119 items et 11 demographies",
    "hot deck k=5 tirage": "119 items", "hot deck k=10 tirage": "119 items",
    "B2 argmax": "119 items", "B2 tirage": "119 items",
    "copule argmax": "les autres items ordinaux",
    "copule tirage": "les autres items ordinaux",
}

# Les huit conditions a modele de langage, reprises de a28 sans changement.
LLM = list(C28.LLM)
for _c in LLM:
    FAMILLE[_c] = "modele de langage"
    REGIME[_c] = "modele de langage"
CONDITIONNEMENT.update({
    "agents composite": "entretien et questionnaire",
    "agents entretien (v3)": "entretien",
    "agents enquete": "questionnaire",
    "agents demographiques (v6)": "etiquette demographique",
    "agents v7": "persona",
    "agents v8": "etiquette demographique",
    "C2": "etiquette demographique",
    "C3": "119 items, sans etiquette",
})
FAMILLE["humains vague 2"] = "humains"
REGIME["humains vague 2"] = "humains"
CONDITIONNEMENT["humains vague 2"] = "la personne elle meme"

# Ordre d'affichage stable dans tous les tableaux de a35.
ORDRE = [
    "humains vague 2",
    "agents composite", "agents entretien (v3)", "agents enquete",
    "agents demographiques (v6)", "agents v7", "agents v8", "C2", "C3",
    "E1 regression contexte argmax", "B2 argmax", "IM m=10 mode des m",
    "B3 foret", "B1 argmax", "B0 mode", "copule argmax",
    "E2 regression contexte tirage", "PMM k=5", "PMM k=10",
    "hot deck k=5 tirage", "hot deck k=10 tirage", "B2 tirage",
    "B1 tirage", "B0 tirage", "copule tirage",
]

# Les couples "meme modele, deux regimes" sur lesquels porte le theoreme d'imputation.
COUPLES = [
    ("marginale", "B0 mode", "B0 tirage"),
    ("regression sur demographies", "B1 argmax", "B1 tirage"),
    ("regression sur contexte", "E1 regression contexte argmax",
     "E2 regression contexte tirage"),
    ("hot deck k=30", "B2 argmax", "B2 tirage"),
]
COUPLE_COPULE = ("copule gaussienne", "copule argmax", "copule tirage")


# ---------------------------------------------------------------------------
# 1. Chargement
# ---------------------------------------------------------------------------

def charger_paquet(cache, cache_foret):
    """Paquet de a28, plus les deux baselines de tirage que a25 ne charge pas.

    a25_mesures ne met que quatre baselines dans son dictionnaire, mais son cache en
    contient six : `B1 tirage` et `B2 tirage` y sont, calculees par le meme appel a
    a2_baselines_gss.evaluer, avec les memes plis et la meme graine. On les relit du
    cache plutot que de les recalculer, pour qu'aucun tirage ne differe de a2.
    """
    paquet = C28.charger_tout(cache, cache_foret)
    if cache and os.path.exists(cache):
        brut = pickle.load(open(cache, "rb"))
        for nom in ("B1 tirage", "B2 tirage"):
            if nom in brut and nom not in paquet["M"]:
                paquet["M"][nom] = brut[nom]
    paquet["y2"] = paquet["M"]["humains vague 2"]
    return paquet


def texte(mat):
    """Matrice objet -> matrice de chaines, les manquants portant la modalite "nr"."""
    return np.array([[("nr" if est_manquant(v) else str(v)) for v in ligne]
                     for ligne in mat], dtype=object)


# ---------------------------------------------------------------------------
# 2. Les methodes d'imputation nouvelles
# ---------------------------------------------------------------------------

def _fit_item(Xt, Xe, y_tr, force):
    """Ajuste une multinomiale sur un item et renvoie (classes, proba_test, proba_train).

    Renvoie (None, None, None) si l'item n'a pas au moins deux modalites observees dans
    le pli d'entrainement. force est l'inverse de la penalite, le C de scikit-learn.
    """
    obs = np.array([not est_manquant(v) for v in y_tr])
    if obs.sum() < 5:
        return None, None, None, None
    yv = np.asarray(y_tr, dtype=object)[obs]
    classes = list(dict.fromkeys(yv))
    if len(classes) == 1:
        return classes, None, None, obs
    rang = {c: i for i, c in enumerate(classes)}
    modele = LogisticRegression(max_iter=1000, C=force)
    modele.fit(Xt[obs], np.array([rang[v] for v in yv]))
    # modele.classes_ est trie ; on remet les colonnes dans l'ordre de `classes`.
    ordre = np.argsort(modele.classes_)
    p_te = modele.predict_proba(Xe)[:, ordre]
    p_tr = modele.predict_proba(Xt[obs])[:, ordre]
    return classes, p_te, p_tr, obs


def choisir_force(y1, x, plis, blocs, grille_c, graine=GRAINE_A35, n_items=30):
    """Choix de la penalite par validation interne au pli d'entrainement du pli 0.

    Le pli de test n'est jamais regarde. On coupe le pli d'entrainement du pli 0 en deux,
    on ajuste sur une moitie et on mesure l'exactitude sur l'autre, pour n_items items
    tires au hasard, et on retient le C qui maximise cette exactitude. C'est plus propre
    que le choix du k de B2 dans a2, qui avait ete fait sur un pli de test.
    """
    rng = np.random.default_rng(graine)
    tr, _ = plis[0]
    coupe = rng.permutation(len(tr))
    a, b = tr[coupe[: len(tr) // 2]], tr[coupe[len(tr) // 2:]]
    m = y1.shape[1]
    scores = {c: [0.0, 0.0] for c in grille_c}
    for bloc in blocs:
        ctx = np.setdiff1d(np.arange(m), bloc)
        Z = np.concatenate([texte(y1[:, ctx]), x.astype(object)], axis=1)
        enc = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
        enc.fit(Z[a])
        Xa, Xb = enc.transform(Z[a]), enc.transform(Z[b])
        cibles = rng.choice(bloc, size=min(n_items // len(blocs) + 1, len(bloc)),
                            replace=False)
        for j in cibles:
            verite = y1[b, j]
            ok = np.array([not est_manquant(v) for v in verite])
            if ok.sum() < 20:
                continue
            for c in grille_c:
                classes, p_te, _, _ = _fit_item(Xa, Xb, y1[a, j], c)
                if classes is None:
                    continue
                if p_te is None:
                    pred = np.array([classes[0]] * len(b), dtype=object)
                else:
                    pred = np.array([classes[i] for i in p_te.argmax(axis=1)],
                                    dtype=object)
                scores[c][0] += float((pred[ok] == np.asarray(verite, dtype=object)[ok]).sum())
                scores[c][1] += float(ok.sum())
    detail = {c: (v[0] / v[1] if v[1] else np.nan) for c, v in scores.items()}
    meilleur = max(detail, key=lambda c: detail[c])
    return meilleur, detail


def imputations_regression(y1, x, plis, blocs, force, k_pmm=(5, 10), m_im=10,
                           graine=GRAINE_A35):
    """E1, E2, PMM et imputation multiple, en un seul passage de regressions.

    Toutes ces methodes partagent le meme modele d'imputation : une multinomiale
    regularisee de l'item cible sur le contexte et les demographies. Elles ne different
    que par ce qu'on fait de la distribution predite.

      E1  : sa modalite la plus probable.
      E2  : un tirage dans cette distribution ; c'est aussi l'imputation numero 1 de IM.
      PMM : la valeur OBSERVEE d'un donneur tire parmi les k donneurs dont le vecteur de
            probabilites predites est le plus proche, au sens euclidien, de celui du
            receveur. Pour un item binaire cette distance est une fonction monotone de
            l'ecart des moyennes predites : la regle coincide alors avec l'appariement
            sur moyenne predite classique. Pour un item a plus de deux modalites, la
            moyenne predite n'est pas definie sans hypothese d'ordre ; le vecteur de
            probabilites est la generalisation retenue, et elle est declaree ici.
      IM  : m tirages independants de E2, plus la modalite modale des m.

    Retourne un dictionnaire nom -> matrice objet (personnes x items), plus la liste des
    m matrices d'imputation multiple sous la cle "_im".
    """
    n, m = y1.shape
    rng = np.random.default_rng(graine)
    noms = ["E1 regression contexte argmax", "E2 regression contexte tirage",
            "IM m=10 mode des m"] + [f"PMM k={k}" for k in k_pmm]
    out = {nom: np.empty((n, m), dtype=object) for nom in noms}
    im = [np.empty((n, m), dtype=object) for _ in range(m_im)]

    for i_pli, (tr, te) in enumerate(plis):
        for bloc in blocs:
            ctx = np.setdiff1d(np.arange(m), bloc)
            Z = np.concatenate([texte(y1[:, ctx]), x.astype(object)], axis=1)
            enc = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
            enc.fit(Z[tr])
            Xt, Xe = enc.transform(Z[tr]), enc.transform(Z[te])
            for j in bloc:
                classes, p_te, p_tr, obs = _fit_item(Xt, Xe, y1[tr, j], force)
                if classes is None:
                    continue
                if p_te is None:
                    seul = np.array([classes[0]] * len(te), dtype=object)
                    for nom in noms:
                        out[nom][np.ix_(te, [j])] = seul[:, None]
                    for t in range(m_im):
                        im[t][np.ix_(te, [j])] = seul[:, None]
                    continue
                cl = np.asarray(classes, dtype=object)
                out["E1 regression contexte argmax"][np.ix_(te, [j])] = \
                    cl[p_te.argmax(axis=1)][:, None]
                tirages = np.empty((m_im, len(te)), dtype=object)
                for t in range(m_im):
                    idx = np.array([rng.choice(len(cl), p=p) for p in p_te])
                    tirages[t] = cl[idx]
                    im[t][np.ix_(te, [j])] = cl[idx][:, None]
                out["E2 regression contexte tirage"][np.ix_(te, [j])] = tirages[0][:, None]
                # mode des m imputations, egalites tranchees par le premier tirage
                mode = np.empty(len(te), dtype=object)
                for i in range(len(te)):
                    vals, cpt = np.unique(tirages[:, i].astype(str), return_counts=True)
                    mode[i] = vals[cpt.argmax()]
                out["IM m=10 mode des m"][np.ix_(te, [j])] = mode[:, None]
                # PMM : donneurs = personnes du pli d'entrainement observees sur l'item
                donneurs = np.asarray(y1[tr, j], dtype=object)[obs]
                d2 = (((p_te[:, None, :] - p_tr[None, :, :]) ** 2).sum(axis=2))
                for k in k_pmm:
                    keff = min(k, d2.shape[1])
                    prox = np.argpartition(d2, keff - 1, axis=1)[:, :keff]
                    choix = rng.integers(0, keff, size=len(te))
                    out[f"PMM k={k}"][np.ix_(te, [j])] = \
                        donneurs[prox[np.arange(len(te)), choix]][:, None]
        print(f"  regressions, pli {i_pli + 1}/{len(plis)} termine", flush=True)
    out["_im"] = im
    return out


def hot_deck(y1, plis, blocs, ks=(5, 10), graine=GRAINE_A35):
    """Hot deck par plus proche voisin, tirage parmi les k voisins, a plusieurs k.

    Meme distance et meme fonction de tirage que `B2 tirage` de a2, importee et non
    recopiee : seul le nombre de donneurs change. k = 30 n'est pas recalcule ici, il est
    relu du cache de a2 sous le nom `B2 tirage`.
    """
    n, m = y1.shape
    codes = en_codes(y1)
    rng = np.random.default_rng(graine + 1)
    out = {f"hot deck k={k} tirage": np.empty((n, m), dtype=object) for k in ks}
    for i_pli, (tr, te) in enumerate(plis):
        for bloc in blocs:
            ctx = np.setdiff1d(np.arange(m), bloc)
            d = distance_hamming(codes[np.ix_(te, ctx)], codes[np.ix_(tr, ctx)])
            for j in bloc:
                for k in ks:
                    out[f"hot deck k={k} tirage"][np.ix_(te, [j])] = \
                        b2_voisins(d, y1[tr, j], k, rng, tirage=True)[:, None]
        print(f"  hot deck, pli {i_pli + 1}/{len(plis)} termine", flush=True)
    return out


def copule(paquet, plis, lam=LAMBDA_COPULE, graine=GRAINE_A35):
    """Copule gaussienne de a8, rejouee ici pour disposer de sa matrice de predictions.

    a8_copule ecrit un CSV d'agregats mais ne conserve pas ses predictions ; on rappelle
    ses fonctions, sans les modifier, pour obtenir les deux matrices. Le retrecissement
    n'est pas revalide : a8 a retenu 0,20 aux cinq plis, la valeur est reprise et le fait
    est ecrit ici et dans le rapport.

    Retourne les deux matrices sur 1 052 x 149, remplies de None hors des items ordinaux,
    et la liste des colonnes couvertes.
    """
    import a8_commun as C8
    import a8_copule as CP

    g = C8.charger_gss()
    gardes, _ = CP.items_ordinaux_utilisables(g)
    cols = [g["items"].index(it) for it in gardes]
    y = np.array([[str(v).strip().lower() for v in ligne]
                  for ligne in g["y1"][:, cols]], dtype=object)
    ordres = [[str(o).strip().lower() for o in g["options"][it.lower()]] for it in gardes]
    n, m = y.shape
    rng_bl = np.random.default_rng(C8.GRAINE)
    blocs = np.array_split(rng_bl.permutation(m), C8.N_BLOCS)

    pa = np.empty((n, m), dtype=object)
    pt = np.empty((n, m), dtype=object)
    for tr, te in plis:
        a, b = CP.copule_pli(y[tr], y[te], ordres, blocs, lam)
        pa[te] = a
        pt[te] = b

    n_tot, m_tot = paquet["y1"].shape
    arg = np.full((n_tot, m_tot), None, dtype=object)
    tir = np.full((n_tot, m_tot), None, dtype=object)
    arg[:, cols] = pa
    tir[:, cols] = pt
    return {"copule argmax": arg, "copule tirage": tir}, cols, gardes


# ---------------------------------------------------------------------------
# 3. Le tableau a quatre cases
# ---------------------------------------------------------------------------

def exactitude(pred, verite, lignes, colonnes):
    """Exactitude par personne sur un perimetre de personnes et d'items."""
    p = pred[np.ix_(lignes, colonnes)]
    v = verite[np.ix_(lignes, colonnes)]
    return exactitude_par_personne(p, v)


def diversite(pred, verite, lignes, colonnes):
    """Diversite conservee et accord par paires, definitions de a0 reprises par a2.

    La comparaison est faite en minuscules apres retrait des espaces de bord, comme le
    codage de a1 et de a25 : sans cela la copule, qui rend ses modalites en minuscules,
    aurait une entropie calculee sur un alphabet different de celui des humains.
    """
    p = pred[np.ix_(lignes, colonnes)]
    v = verite[np.ix_(lignes, colonnes)]
    somme_p, somme_h, accords = 0.0, 0.0, []
    for j in range(p.shape[1]):
        cv = [C28.norm(z) for z in v[:, j] if not est_manquant(z)]
        cp = [C28.norm(z) for z in p[:, j] if not est_manquant(z)]
        eh, ep = entropie(cv), entropie(cp)
        if eh is None or ep is None:
            continue
        somme_h += eh
        somme_p += ep
        a = accord_par_paires(cp)
        if a is not None:
            accords.append(a)
    return {"part_diversite_humaine": somme_p / somme_h if somme_h else np.nan,
            "accord_par_paires": float(np.mean(accords)) if accords else np.nan}


def sommes_dispersion(codes, seg, k_items, colonnes, n_min=30):
    """Somme sur les items des trois termes de Gini Simpson, estimateur de a1.

    On somme les termes plutot que de moyenner des rapports item par item : c'est la
    regle de a1_double_distorsion.agreger, et elle evite qu'un item a dispersion humaine
    presque nulle domine la moyenne par un rapport instable.
    """
    tot = intra = inter = 0.0
    n_ret = 0
    for j in colonnes:
        d = C28.dispersion_item(codes[:, j], seg, k_items[j], n_min)
        if np.isnan(d["gs_total"]) or np.isnan(d["gs_intra"]):
            continue
        tot += d["gs_total"]
        intra += d["gs_intra"]
        inter += d["gs_inter"]
        n_ret += 1
    return {"total": tot, "intra": intra, "inter": inter, "n_items": n_ret}


def sommes_dispersion_rapide(codes, seg, k_max, colonnes, n_min=30):
    """Version vectorisee de sommes_dispersion, employee dans le bootstrap seulement.

    Elle calcule les memes trois quantites que a28_commun.dispersion_item, avec les memes
    estimateurs sans biais, mais en une seule passe sur toutes les colonnes. Sa seule
    raison d'etre est le temps : la version item par item coute environ 0,3 seconde par
    tirage bootstrap et par methode, ce qui rendrait impossible un bootstrap de 400
    tirages sur vingt cinq methodes. Elle est verifiee contre la version de reference sur
    l'echantillon complet, et l'ecart maximal est publie dans le rapport.
    """
    sub = codes[:, colonnes]
    n, m = sub.shape
    g = int(seg.max()) + 1 if seg.size and seg.max() >= 0 else 1
    ok = (sub >= 0) & (seg[:, None] >= 0)
    c = np.zeros((m, g, k_max), dtype=np.float64)
    ii, jj = np.nonzero(ok)
    np.add.at(c, (jj, seg[ii], sub[ii, jj]), 1.0)

    n_k = c.sum(axis=1)                     # (m, k)
    n_g = c.sum(axis=2)                     # (m, g)
    N = n_k.sum(axis=1)                     # (m,)
    valide = N >= n_min

    den = np.where(N > 1.0, N * (N - 1.0), np.nan)
    gs_total = 1.0 - (n_k * (n_k - 1.0)).sum(axis=1) / den

    den_g = np.where(n_g > 1.0, n_g * (n_g - 1.0), np.nan)
    gs_g = 1.0 - (c * (c - 1.0)).sum(axis=2) / den_g
    poids = np.where(n_g >= 2.0, n_g, 0.0)
    s_poids = poids.sum(axis=1)
    gs_intra = np.where(s_poids > 0,
                        (poids * np.nan_to_num(gs_g)).sum(axis=1)
                        / np.where(s_poids > 0, s_poids, 1.0), np.nan)

    bon = valide & ~np.isnan(gs_total) & ~np.isnan(gs_intra)
    tot = float(gs_total[bon].sum())
    intra = float(gs_intra[bon].sum())
    return {"total": tot, "intra": intra, "inter": tot - intra,
            "n_items": int(bon.sum())}


def minorites(pred, verite, mods, lignes, colonnes):
    """Rappel, precision et F1 minoritaires, definitions de a29 reprises sans retouche."""
    p = pred[np.ix_(lignes, colonnes)]
    v = verite[np.ix_(lignes, colonnes)]
    sous = [mods[j] for j in colonnes]
    c = C29.compter(p, v, sous)
    a = C29.agreger(c)
    return c, a


# ---------------------------------------------------------------------------
# 4. Bootstrap sur les personnes
# ---------------------------------------------------------------------------

def tirages(n, b, rng):
    """Indices de b tirages bootstrap de n personnes avec remise, partages par toutes
    les methodes pour que les contrastes soient apparies."""
    return rng.integers(0, n, (b, n))


def p_bilateral(distribution):
    """p bilateral lu sur la position de zero dans une distribution bootstrap.

    Il ne descend jamais sous 1 / nombre de tirages, ce qui evite d'ecrire p = 0 apres
    une correction pour tests multiples. Convention identique a a28, a29 et a31.
    """
    d = np.asarray(distribution, float)
    d = d[~np.isnan(d)]
    if len(d) == 0:
        return 1.0
    p = 2.0 * min((d <= 0).mean(), (d >= 0).mean())
    return float(min(max(p, 1.0 / len(d)), 1.0))
