"""
a2_commun : briques partagees par les scripts de baselines sans modele de langage.

Statut : script d'exploration, pas du code de production. Ce module existe pour qu'une
seule definition de l'exactitude et de la diversite serve aux deux jeux de donnees, et
qu'un ecart de chiffre entre GSS et Twin-2K-500 ne vienne jamais d'une metrique qui a
diverge en cours de route.

Entree  : matrices de reponses categorielles, une ligne par personne, une colonne par item.
          Les valeurs sont des chaines en clair ou des entiers ; les manquants sont None.
Sortie  : trois predicteurs (B0, B1, B2), l'exactitude par personne avec intervalle de
          confiance par bootstrap, et le couple entropie / accord par paires repris a
          l'identique de analyses/a0_diversite_osf.py.

Aucun appel de modele. Dependances : numpy, pandas, scikit-learn.
"""

import math
from collections import Counter

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

# Valeurs traitees comme non renseignees, memes conventions que a0.
MANQUANT = {"", "<not recorded>", "nan", "NA", "None", None}


def est_manquant(v):
    """Vrai si la cellule ne porte pas de reponse exploitable."""
    if v is None:
        return True
    if isinstance(v, float) and math.isnan(v):
        return True
    return v in MANQUANT


# ---------------------------------------------------------------------------
# Mesures de diversite, reprises telles quelles de a0_diversite_osf.py
# ---------------------------------------------------------------------------

def entropie(valeurs):
    """Entropie de Shannon en bits de la distribution des reponses a un item."""
    valeurs = [v for v in valeurs if not est_manquant(v)]
    if not valeurs:
        return None
    n = len(valeurs)
    return -sum((k / n) * math.log2(k / n) for k in Counter(valeurs).values())


def accord_par_paires(valeurs, n_min=50):
    """Probabilite que deux repondants tires sans remise donnent la meme reponse.

    Indice de Simpson. 50 pour cent veut dire qu'une paire au hasard est d'accord une
    fois sur deux. Plus il est haut, plus la population predite est homogene.
    """
    valeurs = [v for v in valeurs if not est_manquant(v)]
    n = len(valeurs)
    if n < n_min:
        return None
    return sum(k * (k - 1) for k in Counter(valeurs).values()) / (n * (n - 1))


def profil_diversite(pred, verite):
    """Compare la dispersion des predictions a celle des humains, item par item.

    pred et verite sont deux tableaux objets de meme forme (personnes x items).
    Retourne la part de la diversite humaine conservee, en rapportant la somme des
    entropies predites a la somme des entropies humaines sur les memes items, et
    l'accord par paires moyen des predictions.
    """
    n_items = pred.shape[1]
    somme_pred, somme_hum, accords = 0.0, 0.0, []
    for j in range(n_items):
        colonne_v = [v for v in verite[:, j] if not est_manquant(v)]
        colonne_p = [v for v in pred[:, j] if not est_manquant(v)]
        e_h, e_p = entropie(colonne_v), entropie(colonne_p)
        if e_h is None or e_p is None:
            continue
        somme_hum += e_h
        somme_pred += e_p
        a = accord_par_paires(colonne_p)
        if a is not None:
            accords.append(a)
    return {
        "part_diversite_humaine": somme_pred / somme_hum if somme_hum else float("nan"),
        "entropie_moyenne": somme_pred / n_items,
        "accord_par_paires": float(np.mean(accords)) if accords else float("nan"),
    }


# ---------------------------------------------------------------------------
# Exactitude par personne et intervalle de confiance
# ---------------------------------------------------------------------------

def exactitude_par_personne(pred, verite, masque=None):
    """Part des items secrets correctement predits, une valeur par personne.

    masque, s'il est fourni, indique les cellules a prendre en compte. Les personnes
    sans aucune cellule evaluable recoivent NaN et sont exclues des agregations.
    """
    if masque is None:
        masque = np.array([[not est_manquant(v) for v in ligne] for ligne in verite])
    juste = (pred == verite) & masque
    n = masque.sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(n > 0, juste.sum(axis=1) / np.maximum(n, 1), np.nan)


def bootstrap_personnes(valeurs, n_tirages=2000, graine=0):
    """Intervalle de confiance a 95 pour cent, reechantillonnage sur les participants.

    L'unite de reechantillonnage est la personne et non la reponse : deux reponses
    d'un meme individu ne sont pas independantes, un bootstrap sur les cellules
    donnerait un intervalle faussement etroit.
    """
    v = np.asarray(valeurs, dtype=float)
    v = v[~np.isnan(v)]
    if len(v) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(graine)
    tirages = rng.choice(v, size=(n_tirages, len(v)), replace=True).mean(axis=1)
    return float(v.mean()), float(np.percentile(tirages, 2.5)), float(np.percentile(tirages, 97.5))


# ---------------------------------------------------------------------------
# B0 : plancher absolu, tirage dans la distribution marginale observee
# ---------------------------------------------------------------------------

def b0_marginale(y_train, n_test, rng, mode=False):
    """Predit sans aucune information sur l'individu.

    y_train : reponses observees sur les personnes d'entrainement pour cet item.
    mode=True renvoie toujours la modalite majoritaire, ce qui maximise l'exactitude
    et annule la diversite. mode=False tire dans la marginale, ce qui conserve la
    diversite marginale et perd de l'exactitude. Les deux sont rapportes : leur ecart
    est la mesure directe du compromis exactitude contre dispersion.
    """
    obs = [v for v in y_train if not est_manquant(v)]
    if not obs:
        return np.array([None] * n_test, dtype=object)
    if mode:
        maj = Counter(obs).most_common(1)[0][0]
        return np.array([maj] * n_test, dtype=object)
    modalites, effectifs = zip(*Counter(obs).items())
    p = np.array(effectifs, dtype=float) / sum(effectifs)
    return np.array(rng.choice(modalites, size=n_test, p=p), dtype=object)


# ---------------------------------------------------------------------------
# B1 : regression logistique multinomiale sur les seules demographies
# ---------------------------------------------------------------------------

def encodeur_demographies(x_train):
    """Encodage indicatrice des attributs demographiques, ajuste sur l'entrainement seul.

    handle_unknown='ignore' evite qu'une modalite vue seulement en test fasse echouer
    la prediction. Ajuster l'encodeur sur l'ensemble complet serait une fuite legere
    mais reelle, on ne le fait pas.
    """
    enc = OneHotEncoder(handle_unknown="ignore", sparse_output=False)
    enc.fit(x_train)
    return enc


def b1_logistique(x_train_enc, y_train, x_test_enc, rng, tirage=False):
    """Une regression logistique multinomiale par item, entrainee sur les demographies.

    tirage=False renvoie la classe la plus probable, ce qui est le reglage de la
    litterature et celui qui produit les 0,622 du GSS. tirage=True echantillonne dans
    la distribution predite : meme modele, exactitude plus faible, diversite conservee.
    """
    obs = np.array([not est_manquant(v) for v in y_train])
    if obs.sum() < 5:
        return np.array([None] * len(x_test_enc), dtype=object)
    y = np.asarray(y_train, dtype=object)[obs]
    # Les modalites sont indexees par des entiers avant l'appel a scikit-learn, puis
    # retablies telles quelles. Passer par des chaines ferait rentrer 3.0 et sortir "3.0",
    # qui ne serait jamais compte juste sur un jeu code en nombres.
    classes = list(dict.fromkeys(y))
    if len(classes) == 1:
        return np.array([classes[0]] * len(x_test_enc), dtype=object)
    rang = {c: i for i, c in enumerate(classes)}
    modele = LogisticRegression(max_iter=2000, C=1.0)
    modele.fit(x_train_enc[obs], np.array([rang[v] for v in y]))
    if not tirage:
        idx = modele.predict(x_test_enc)
    else:
        proba = modele.predict_proba(x_test_enc)
        idx = modele.classes_[[rng.choice(len(modele.classes_), p=p) for p in proba]]
    return np.array([classes[i] for i in idx], dtype=object)


# ---------------------------------------------------------------------------
# B2 : les k plus proches voisins sur les questions connues
# ---------------------------------------------------------------------------

def en_codes(matrice):
    """Convertit une matrice de reponses en clair en codes entiers, -1 pour un manquant.

    Le codage est fait colonne par colonne sur l'ensemble des personnes. C'est une
    operation sans apprentissage : elle ne transporte aucune information d'une personne
    a l'autre et ne constitue donc pas une fuite. Elle sert uniquement a rendre le calcul
    de distance vectorisable, il devient une centaine de fois plus rapide.
    """
    m = np.asarray(matrice, dtype=object)
    codes = np.full(m.shape, -1, dtype=np.int32)
    for j in range(m.shape[1]):
        table = {}
        for i in range(m.shape[0]):
            v = m[i, j]
            if not est_manquant(v):
                codes[i, j] = table.setdefault(v, len(table))
    return codes


def distance_hamming(codes_test, codes_train):
    """Distance de Hamming normalisee entre chaque personne test et chaque personne train.

    Entree : deux matrices de codes entiers produites par en_codes, -1 pour un manquant.
    Les cellules manquantes d'un cote ou de l'autre sont ignorees ; le denominateur est
    le nombre d'items renseignes chez les deux personnes. Retourne une matrice
    (n_test, n_train) de distances dans [0, 1].
    """
    d = np.ones((codes_test.shape[0], codes_train.shape[0]))
    dispo_train = codes_train >= 0
    for i in range(codes_test.shape[0]):
        a = codes_test[i]
        commun = (a >= 0) & dispo_train
        egal = (codes_train == a) & commun
        n = commun.sum(axis=1)
        with np.errstate(invalid="ignore", divide="ignore"):
            d[i] = np.where(n > 0, 1.0 - egal.sum(axis=1) / np.maximum(n, 1), 1.0)
    return d


def b2_voisins(distances, y_train, k, rng, tirage=False):
    """Predit un item a partir des reponses des k personnes les plus proches.

    Les voisins sont cherches uniquement parmi les personnes d'entrainement, sur les
    seuls items de contexte. L'item predit ne participe jamais au calcul de distance.
    tirage=True tire dans la distribution des k voisins au lieu de prendre leur mode.
    """
    y = np.asarray(y_train, dtype=object)
    obs = np.array([not est_manquant(v) for v in y])
    if obs.sum() < 1:
        return np.array([None] * distances.shape[0], dtype=object)
    d = distances[:, obs]
    y_obs = y[obs]
    k_eff = min(k, d.shape[1])
    ordre = np.argpartition(d, k_eff - 1, axis=1)[:, :k_eff]
    sortie = np.empty(distances.shape[0], dtype=object)
    for i in range(distances.shape[0]):
        votes = Counter(y_obs[ordre[i]])
        if tirage:
            modalites, effectifs = zip(*votes.items())
            p = np.array(effectifs, dtype=float) / sum(effectifs)
            sortie[i] = rng.choice(modalites, p=p)
        else:
            sortie[i] = votes.most_common(1)[0][0]
    return sortie
