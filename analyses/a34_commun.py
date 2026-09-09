"""
a34_commun : briques partagees par le test de la rarete DEDUCTIBLE, question du
8 septembre 2026, "l'avantage des modeles de langage sur les gens rares disparait il
quand la rarete est deductible de l'etiquette ?".

C'est le test 4 de la section (d) de `corpus/lecture-complete/03-baselines-statistiques-
extension-enquete.md`, celui qui est designe la comme "le seul du lot qui peut faire
tomber le rang 1 revise". Il oppose notre resultat (a28 section 3.4, a29, a31 : sur les
cellules minoritaires l'ordre des methodes s'inverse, les agents retrouvent 22 a 26 pour
cent des reponses rares, la regression 4,6 et la foret 0,8) a la contre preuve la plus
directe du corpus (von der Heyde, Haensch et Wenz 2025, T03-34 : sur le vote allemand
l'ecart entre la statistique et le modele de langage se CREUSE quand la categorie se
rarefie, 25 points de F1 sur l'AfD contre 11 sur la CDU).

L'hypothese qui reconcilie les deux : la statistique retrouve les raretes DEDUCTIBLES de
l'etiquette et rate les autres ; le modele de langage retrouve les deux, ou surtout les
non deductibles. Si le modele de langage ne retrouve que les deductibles, la these
"il garde les outliers" tombe.

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a31_commun, et par
lui a29_commun, a28_commun, a25_commun, a25_mesures, a8_commun, a2_commun,
a2_baselines_gss, a5_evaluer et a5_agents_locaux_gss. Les matrices de prediction, les
1 052 personnes, les 149 items, les plis, les blocs, les graines, les 150 personnes du run
local, la definition des modalites minoritaires et toute la machinerie de bootstrap sur
les personnes viennent de la, sans une ligne recopiee.

Ce module ne teste rien. Il construit LE SCORE DE DEDUCTIBILITE, la partition en terciles,
les planchers de bruit de cellule, et les compteurs par personne dont les tableaux ont
besoin.

  1. Le score de deductibilite logistique, D_logit. Pour une cellule (personne, item) et
     une modalite m, la probabilite hors pli que la regression logistique multinomiale sur
     les onze attributs demographiques attribue m a cette personne. C'est exactement le
     modele de `B1 argmax` : memes cinq plis sur les personnes de `a2_baselines_gss.grille`
     (graine 20260903), meme encodeur indicatrice ajuste sur le pli d'entrainement seul,
     meme `LogisticRegression(max_iter=2000, C=1.0)`. La seule difference avec
     `a2_commun.b1_logistique` est qu'on lit `predict_proba` au lieu de `predict` : le
     score de deductibilite est donc, litteralement, la confiance de l'adversaire
     statistique dans la modalite consideree. Une modalite absente du pli d'entrainement
     recoit zero, ce qui est la bonne valeur : elle est litteralement indeductible pour ce
     predicteur.
     C'est aussi la definition qui colle a von der Heyde : chez eux la regression
     multinomiale tourne sur exactement les memes variables que l'invite du modele.

  2. Le score de deductibilite par segment, D_seg. Frequence de la modalite dans le
     segment ideologie x genre x age de la personne, calculee sur les humains de la
     vague 1 EN LAISSANT DE COTE LA PERSONNE ELLE MEME. Sans ce retrait, la modalite
     qu'on cherche a expliquer entrerait dans le score qui doit l'expliquer. Un segment
     qui compte moins de N_MIN_SEGMENT autres repondants exploitables sur l'item donne
     NaN, et le taux de couverture est rapporte.
     Ce score est le pendant non parametrique du premier ; il est aussi, exactement, le
     PLANCHER DE BRUIT DE CELLULE demande par la lecture 01 section (d) point 5 : le
     rappel qu'obtiendrait une methode qui tire dans la marginale du segment de la
     personne. Les deux usages sont le meme calcul, et il faut le dire, parce que cela
     rend circulaire toute lecture de l'exces sur plancher a l'interieur d'une partition
     par D_seg. Le choix de la partition principale est fait et motive dans l'entete de
     `a34_deductibilite.py` : c'est D_seg, parce que D_logit est la confiance de
     `B1 argmax` elle meme et place par construction 100 pour cent des raretes osees par
     la regression dans le tercile deductible. Les deux partitions sont rapportees
     partout, avec cet avertissement des deux cotes.

  3. Le plancher d'item, D_item. Frequence de la modalite dans la population entiere,
     sans la personne. C'est l'esperance de rappel de `B0 tirage`, qui ne sait rien de
     personne : il sert de temoin de lecture, la valeur mesuree de `B0 tirage` doit s'en
     approcher.

  4. La partition en terciles. Les bornes sont les 33,3e et 66,7e percentiles du score
     sur les CELLULES MINORITAIRES REELLES du perimetre, seuil 10 pour cent. Les deux
     scores sont calcules une fois sur les 1 052 humains de la vague 1 : ce sont des
     descripteurs de population, et les recalculer sur 150 personnes donnerait des cases
     de segment d'une ou deux personnes. T1 est le
     tercile le moins deductible, T3 le plus deductible. Les memes bornes servent a
     classer les cellules ou une methode OSE une modalite minoritaire, via la
     deductibilite de la modalite PREDITE : sans cela precision et rappel ne seraient pas
     definis sur la meme partition et le F1 par tercile n'aurait pas de sens.

  5. Les compteurs par personne. Toutes les quantites du rapport sont des rapports de
     sommes sur les cellules ; elles sont reduites a un numerateur et un denominateur par
     personne, ce qui rend le bootstrap sur les PERSONNES immediat et les contrastes
     apparies, exactement comme en a31. Le bootstrap ne porte jamais sur les cellules :
     deux reponses d'une meme personne ne sont pas independantes.

Convention de masque, reprise de a8 section 6, de a29 et de a31 sans changement : une
cellule est evaluable des que la vraie reponse de la vague 1 est observee ; une prediction
refusee compte comme non minoritaire.

Aucune microdonnee n'est ecrite par ce module.
"""

import os
import sys

# Limite de quatre coeurs, posee avant l'import de numpy sinon elle est sans effet.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import a31_commun as C31
import a29_commun as C29
import a28_commun as C28
from a2_commun import est_manquant, encodeur_demographies
from a2_baselines_gss import GRAINE as GRAINE_GRILLE, grille
from a8_commun import modalites_minoritaires

RACINE = C31.RACINE
SORTIE = C31.SORTIE

GRAINE = 20260908
SEUIL = 0.10
SEUILS = [0.10, 0.20]

# Segment du score de deductibilite par segment. Trois axes, comme demande : l'ideologie,
# qui est le seul axe dont a1, a23, a28 test 3 et a29 section 3.1 disent tous les quatre
# qu'il separe quelque chose, plus le genre et l'age. 7 x 2 x 7 = 98 cases possibles pour
# 1 052 personnes, soit une dizaine de personnes par case : c'est fin, et c'est justement
# le regime ou le plancher de bruit de cellule de la lecture 01 doit etre calcule.
AXES_SEGMENT = ["political_ideology", "gender", "age"]
N_MIN_SEGMENT = 5

# Comparateur statistique declare pour les hypotheses H2 et H3. C'est le bon : von der
# Heyde oppose GPT-3.5 a une regression multinomiale sur exactement les memes variables
# que l'invite, ce que `B1 argmax` est chez nous. `B2 argmax` et `B3 foret` sont rapportes
# a cote, sans test declare.
COMPARATEUR = "B1 argmax"

ORDRE_METHODES = C31.ORDRE_METHODES
LLM = C31.LLM
STAT = C31.STAT
AXES = C31.AXES
PERIMETRE_NATUREL = C31.PERIMETRE_NATUREL
AXE_PRINCIPAL = C31.AXE_PRINCIPAL

charger = C31.charger
methodes_du_perimetre = C31.methodes_du_perimetre
perimetres = C31.perimetres
observe = C31.observe
appartient = C31.appartient
segments_et_niveaux = C31.segments_et_niveaux
tirages_bootstrap = C31.tirages_bootstrap
par_personne = C31.par_personne
moyenne_par_personne = C31.moyenne_par_personne
taux = C31.taux
taux_ic = C31.taux_ic
contraste = C31.contraste
temoin_par_personne = C31.temoin_par_personne
rarete_personne = C31.rarete_personne
rarete_segment = C31.rarete_segment
holm = C31.holm
benjamini_hochberg = C31.benjamini_hochberg
ecrire = C31.ecrire
spearman = C31.spearman

TERCILES = ["T1 non deductible", "T2 intermediaire", "T3 deductible"]


# ---------------------------------------------------------------------------
# 1. Le score de deductibilite logistique, hors pli
# ---------------------------------------------------------------------------

def probabilites_hors_pli(y1, x, plis, graine=GRAINE_GRILLE):
    """Probabilite hors pli de chaque modalite, item par item, personne par personne.

    Retourne une liste de longueur n_items ; l'element j est un couple
    (dictionnaire modalite -> colonne, matrice (n_personnes x n_modalites)). La ligne i
    de cette matrice est la distribution predite pour la personne i par une regression
    logistique qui ne l'a jamais vue.

    Le protocole est celui de `B1 argmax` a la lettre : memes plis, meme encodeur ajuste
    sur le seul pli d'entrainement, memes hyperparametres, meme regle de repli quand
    l'item porte moins de cinq observations ou une seule modalite. La verification que
    l'argmax de ces distributions reproduit bien la matrice `B1 argmax` employee par a2,
    a28, a29 et a31 est faite par l'appelant : c'est le controle de protocole du rapport.
    """
    from sklearn.linear_model import LogisticRegression

    n, m = y1.shape
    sortie = []
    for j in range(m):
        sortie.append(None)
    for j in range(m):
        # Modalites declarees, dans l'ordre d'apparition sur l'ensemble des personnes.
        # L'ordre ne sert qu'a indexer les colonnes, il n'entre dans aucun calcul.
        vues = [v for v in y1[:, j] if not est_manquant(v)]
        mods = list(dict.fromkeys(vues))
        index = {mod: k for k, mod in enumerate(mods)}
        sortie[j] = (index, np.full((n, len(mods)), np.nan))

    for i_pli, (tr, te) in enumerate(plis):
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        for j in range(m):
            index, P = sortie[j]
            obs = np.array([not est_manquant(v) for v in y1[tr, j]])
            if obs.sum() < 5:
                # Meme repli que b1_logistique : aucune prediction. La cellule sera
                # marquee non evaluable pour le score de deductibilite.
                continue
            cible = np.asarray(y1[tr, j], dtype=object)[obs]
            classes = list(dict.fromkeys(cible))
            P[te, :] = 0.0
            if len(classes) == 1:
                P[te, index[classes[0]]] = 1.0
                continue
            rang = {c: k for k, c in enumerate(classes)}
            modele = LogisticRegression(max_iter=2000, C=1.0)
            modele.fit(xt[obs], np.array([rang[v] for v in cible]))
            proba = modele.predict_proba(xe)
            for k, c in enumerate(modele.classes_):
                P[np.ix_(te, [index[classes[int(c)]]])] = proba[:, [k]]
        print(f"  deductibilite, pli {i_pli + 1}/{len(plis)} termine", flush=True)
    return sortie


def deductibilite(mat, tables):
    """Deductibilite logistique de la modalite portee par chaque cellule.

    mat    : matrice objet (personnes x items) de modalites, la verite ou une prediction.
    tables : sortie de probabilites_hors_pli.
    Renvoie une matrice de flottants, NaN la ou la cellule ne porte pas de modalite
    connue ou la ou la regression n'a pas pu etre ajustee.
    """
    n, m = mat.shape
    out = np.full((n, m), np.nan)
    for j in range(m):
        index, P = tables[j]
        col = mat[:, j]
        for i in range(n):
            v = col[i]
            if v is None or est_manquant(v):
                continue
            k = index.get(v)
            if k is None:
                continue
            out[i, j] = P[i, k]
    return out


def argmax_hors_pli(tables, n, m):
    """Modalite la plus probable hors pli, item par item : doit reproduire `B1 argmax`.

    C'est le controle de protocole. Si cette matrice ne coincide pas avec la matrice
    `B1 argmax` employee partout ailleurs, le score de deductibilite ne mesure pas la
    confiance de l'adversaire statistique et tout le rapport est faux.
    """
    out = np.empty((n, m), dtype=object)
    out[:] = None
    for j in range(m):
        index, P = tables[j]
        inverse = {k: mod for mod, k in index.items()}
        ok = ~np.isnan(P).all(axis=1)
        if not ok.any():
            continue
        idx = np.argmax(np.nan_to_num(P[ok], nan=-1.0), axis=1)
        out[ok, j] = np.array([inverse[int(k)] for k in idx], dtype=object)
    return out


# ---------------------------------------------------------------------------
# 2. Le score par segment, et les planchers de bruit de cellule
# ---------------------------------------------------------------------------

def segment_fin(x, attributs, axes=AXES_SEGMENT):
    """Segment croise ideologie x genre x age, vecteur d'entiers, -1 si un axe manque."""
    col = {a: i for i, a in enumerate(attributs)}
    brut = [[C28.norm(v) for v in x[:, col[a]]] for a in axes]
    libelles = []
    for i in range(x.shape[0]):
        vals = [b[i] for b in brut]
        if any((not v.strip()) or v == "non renseigne" for v in vals):
            libelles.append(None)
        else:
            libelles.append("|".join(vals))
    mods = sorted({v for v in libelles if v is not None})
    idx = {mod: k for k, mod in enumerate(mods)}
    return np.array([idx.get(v, -1) for v in libelles], dtype=np.int32), mods


def frequence_segment(mat, verite, ok, seg, n_min=N_MIN_SEGMENT):
    """Frequence de la modalite de la cellule dans le segment, sans la personne.

    mat    : matrice objet des modalites dont on veut la frequence (verite ou prediction).
    verite : matrice objet de la vague 1, qui fournit les effectifs.
    ok     : matrice booleenne des cellules evaluables.
    seg    : vecteur d'entiers de segment, -1 si inconnu.

    Le retrait de la personne porte sur les DEUX termes du rapport : son propre vote sort
    du numerateur s'il vaut la modalite consideree, et sort du denominateur s'il est
    observe. Une cellule dont le segment compte moins de n_min autres repondants
    exploitables sur l'item recoit NaN.
    """
    n, m = mat.shape
    out = np.full((n, m), np.nan)
    niveaux = [k for k in np.unique(seg) if k >= 0]
    for j in range(m):
        colv = verite[:, j]
        colo = ok[:, j]
        colm = mat[:, j]
        for k in niveaux:
            lignes = np.flatnonzero(seg == k)
            if len(lignes) < 2:
                continue
            cpt = {}
            n_obs = 0
            for i in lignes:
                if not colo[i]:
                    continue
                n_obs += 1
                cpt[colv[i]] = cpt.get(colv[i], 0) + 1
            for i in lignes:
                v = colm[i]
                if v is None or est_manquant(v):
                    continue
                num = cpt.get(v, 0)
                den = n_obs
                if colo[i]:
                    den -= 1
                    if colv[i] == v:
                        num -= 1
                if den < n_min:
                    continue
                out[i, j] = num / den
    return out


def frequence_item(mat, verite, ok):
    """Frequence de la modalite dans la population entiere, sans la personne.

    C'est l'esperance de rappel de `B0 tirage`, qui tire dans la marginale de l'item sans
    rien savoir de la personne. Elle sert de plancher le plus bas et de temoin de lecture.
    """
    n, m = mat.shape
    out = np.full((n, m), np.nan)
    for j in range(m):
        colv, colo, colm = verite[:, j], ok[:, j], mat[:, j]
        cpt = {}
        n_obs = 0
        for i in range(n):
            if not colo[i]:
                continue
            n_obs += 1
            cpt[colv[i]] = cpt.get(colv[i], 0) + 1
        for i in range(n):
            v = colm[i]
            if v is None or est_manquant(v):
                continue
            num, den = cpt.get(v, 0), n_obs
            if colo[i]:
                den -= 1
                if colv[i] == v:
                    num -= 1
            if den > 0:
                out[i, j] = num / den
    return out


# ---------------------------------------------------------------------------
# 3. Terciles
# ---------------------------------------------------------------------------

def bornes_terciles(score, masque):
    """33,3e et 66,7e percentiles du score sur les cellules du masque.

    Le score de deductibilite porte beaucoup d'ex aequo exacts a zero : une modalite
    absente du pli d'entrainement recoit exactement zero pour toutes les personnes du pli.
    Les bornes sont donc rapportees avec les effectifs reellement obtenus, et le rapport
    dit si la partition est equilibree ou non. Aucun bruit n'est ajoute pour departager
    les ex aequo : cela rendrait le tercile d'une cellule dependant d'une graine.
    """
    v = score[masque & ~np.isnan(score)]
    if len(v) == 0:
        return np.nan, np.nan
    return float(np.percentile(v, 100.0 / 3.0)), float(np.percentile(v, 200.0 / 3.0))


def terciles(score, b1, b2):
    """Matrice d'entiers 0, 1, 2 selon le tercile, -1 si le score est absent.

    Regle d'affectation : T1 si score <= b1, T3 si score > b2, T2 sinon. Le "inferieur ou
    egal" au premier seuil met le paquet d'ex aequo a zero dans T1, ce qui est le sens
    voulu : une modalite que la regression ne produit jamais est le cas le moins
    deductible qui soit.
    """
    t = np.full(score.shape, -1, dtype=np.int8)
    ok = ~np.isnan(score)
    t[ok & (score <= b1)] = 0
    t[ok & (score > b1) & (score <= b2)] = 1
    t[ok & (score > b2)] = 2
    return t


# ---------------------------------------------------------------------------
# 4. Masques de cellules par methode
# ---------------------------------------------------------------------------

def masques(pred, verite, mods):
    """Les quatre masques booleens dont tout le rapport se deduit.

    rare_vrai : la vraie reponse est une modalite minoritaire de l'item ;
    rare_pred : la methode predit une modalite minoritaire de l'item ;
    juste     : rare_pred et prediction egale a la verite ;
    faux_maj  : rare_pred et vraie reponse MAJORITAIRE, c'est a dire la fausse rarete de
                a31, l'unite d'analyse du point 4.
    Memes definitions qu'en a29 et a31, recalculees ici sur le sous perimetre demande.
    """
    ok = observe(verite)
    dispo = observe(pred)
    rare_vrai = appartient(verite, mods) & ok
    rare_pred = appartient(pred, mods) & ok & dispo
    juste = rare_pred & (pred == verite)
    faux_maj = rare_pred & ~juste & ~rare_vrai
    faux_min = rare_pred & ~juste & rare_vrai
    return {"ok": ok, "rare_vrai": rare_vrai, "rare_pred": rare_pred,
            "juste": juste, "faux_maj": faux_maj, "faux_min": faux_min}


def modalites_rares(verite, seuil, lignes=None):
    """Modalites minoritaires item par item, definition de a8 section 6, importee."""
    v = verite if lignes is None else verite[lignes]
    return modalites_minoritaires(v, seuil)


def p_contre_zero(tir):
    """p bilateral d'une distribution bootstrap contre zero, plancher a 1 sur n."""
    tir = np.asarray(tir, float)
    tir = tir[~np.isnan(tir)]
    if len(tir) == 0:
        return 1.0
    p = 2.0 * min((tir <= 0).mean(), (tir >= 0).mean())
    return float(min(max(p, 1.0 / len(tir)), 1.0))
