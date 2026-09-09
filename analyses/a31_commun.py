"""
a31_commun : briques partagees par l'analyse du mecanisme de la mauvaise rarete, question
du 8 septembre 2026, "pourquoi la bonne personne recoit elle la mauvaise rarete ?".

Statut : script d'analyse jetable, aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie. Sont importes tels quels : a29_commun, et par
lui a28_commun, a25_commun, a25_mesures, a8_commun, a2_commun, a2_baselines_gss,
a5_evaluer et a5_agents_locaux_gss. Les matrices de prediction, les 1 052 personnes, les
149 items, les plis, les blocs, les graines, les 150 personnes du run local et la
definition des modalites minoritaires viennent de la, sans une ligne recopiee.

Ce module ne teste rien. Il construit les COVARIABLES de cellule dont les cinq hypotheses
ont besoin, et les outils de bootstrap qui les resument. Toutes les covariables sont
calculees sur les humains de la vague 1 EN LAISSANT DE COTE LA PERSONNE ELLE MEME, comme
a28 test 3 le fait pour le stereotype de segment : sans cette precaution une personne
contribuerait a definir la reference a laquelle on compare sa propre cellule.

Les covariables, une par mecanisme.

  1. deplacement (H1). Pour chaque cellule, la personne donne t elle une reponse
     minoritaire reelle sur un AUTRE item de la meme famille thematique ? Les six familles
     sont celles de a2_baselines_gss, 58 items sur 149 ; seuls les items qui portent au
     moins une modalite minoritaire peuvent servir, il en reste 21 repartis sur cinq
     familles. La cellule est declaree non evaluable si la personne n'a aucun autre item
     de la famille exploitable.
  2. rarete de groupe (H2). Deux covariables.
     2a. La modalite rare MODALE du segment de la personne, item par item, calculee sans
         la personne. Elle n'a de sens que sur les items qui portent au moins DEUX
         modalites minoritaires : sur les autres, predire une rarete c'est predire LA
         rarete, et l'egalite serait vraie par construction. Il en reste 19 sur 149.
     2b. Le taux de reponses rares reelles du segment de la personne sur cet item,
         calcule sans la personne. Il est defini partout et il dit si la fausse rarete
         tombe la ou le groupe est effectivement souvent rare.
  3. position (H3). Le rang de la modalite predite dans la nomenclature de
     question_master/gss/main.csv, et son caractere extreme, premiere ou derniere
     position. Pour les 71 items ordinaux, extreme veut dire bout d'echelle.
  4. confiance (H4). La probabilite maximale de la distribution rendue par le modele,
     lue dans data/traces/a5-C2-p1.jsonl et a5-C3-p1.jsonl. Disponible pour C2 et C3
     seulement : les conditions de Stanford ne publient pas de distribution.
  5. contexte (H5). Le taux de reponses rares reelles de la personne sur les items HORS
     du bloc secret de l'item considere. C'est litteralement le contexte de C3, les ~119
     items du prompt systeme, et litteralement le contexte de B2, les items sur lesquels
     la distance aux voisins est calculee. Pour C2, qui ne recoit que l'etiquette, et
     pour les conditions de Stanford, qui recoivent un entretien ou un questionnaire hors
     de ce decoupage, c'est une mesure de la richesse en raretes de la personne hors du
     bloc et non le contexte reellement vu : la limite est portee dans le rapport.

Convention de masque, reprise de a8 section 6 et de a29 sans changement : une cellule est
evaluable des que la vraie reponse de la vague 1 est observee ; une prediction refusee
compte comme non minoritaire.

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

import a29_commun as C29
from a2_baselines_gss import FAMILLES, GRAINE as GRAINE_GRILLE, grille
from a25_commun import ORDINAUX, sans_score

RACINE = C29.RACINE
SORTIE = C29.SORTIE

GRAINE = 20260908
SEUIL = 0.10

ORDRE_METHODES = C29.ORDRE_METHODES
LLM = C29.LLM
STAT = C29.STAT
AXES = C29.AXES
PERIMETRE_NATUREL = C29.PERIMETRE_NATUREL

charger = C29.charger
methodes_du_perimetre = C29.methodes_du_perimetre
perimetres = C29.perimetres
observe = C29.observe
appartient = C29.appartient
compter = C29.compter
tirages_bootstrap = C29.tirages_bootstrap
segments_et_niveaux = C29.segments_et_niveaux
spearman = C29.spearman
holm = C29.holm
benjamini_hochberg = C29.benjamini_hochberg
ecrire = C29.ecrire

# Axe declare pour le test de H2a. C'est le seul axe dont a1, a23, a28 test 3 et a29
# section 3.1 disent tous les quatre qu'il separe quelque chose ; les cinq autres sont
# rapportes a cote, sans test.
AXE_PRINCIPAL = "political_ideology"


# ---------------------------------------------------------------------------
# 1. Decoupages d'items : familles thematiques, blocs secrets, positions
# ---------------------------------------------------------------------------

def familles_par_item(items):
    """item -> nom de famille thematique, chaine vide hors des six familles de a2."""
    dedans = {i: nf for nf, membres in FAMILLES.items() for i in membres}
    return np.array([dedans.get(it, "") for it in items], dtype=object)


def blocs_par_item(n_personnes, items):
    """item -> indice du bloc secret, exactement le decoupage employe par le run a5.

    a5_agents_locaux_gss appelle a2_baselines_gss.grille avec la meme graine et la meme
    taille ; le bloc est aussi ecrit dans chaque ligne de trace, ce qui permet de verifier
    la concordance au lieu de la supposer (controle dans a31_mecanismes).
    """
    _, blocs = grille(n_personnes, len(items), GRAINE_GRILLE)
    out = np.full(len(items), -1, dtype=np.int32)
    for b, cols in enumerate(blocs):
        out[np.asarray(cols, dtype=int)] = b
    assert (out >= 0).all(), "un item n'appartient a aucun bloc"
    return out


def rangs_modalites(items, options):
    """item -> (dictionnaire modalite -> rang, nombre de modalites declarees)."""
    return {it: ({m: r for r, m in enumerate(options[it])}, len(options[it]))
            for it in items}


def items_ordinaux(items, options):
    """Meme regle qu'en a25 et a28 : dans ORDINAUX et sans modalite 'Inapplicable'."""
    return np.array([it in ORDINAUX and not any(sans_score(o) for o in options[it])
                     for it in items], dtype=bool)


def table_extremite(items, options):
    """Matrice item x modalite : la modalite est elle en premiere ou derniere position.

    Renvoie trois dictionnaires item -> ensemble de modalites : premiere, derniere,
    extreme, ou extreme est l'union des deux. Pour un item ordinal, extreme veut dire
    bout d'echelle ; pour un item nominal, extreme veut dire bout de la liste presentee,
    ce qui est le pendant lexical de la meme hypothese.
    """
    premiere, derniere = {}, {}
    for it in items:
        o = options[it]
        premiere[it] = {o[0]} if o else set()
        derniere[it] = {o[-1]} if len(o) > 1 else set()
    return premiere, derniere


# ---------------------------------------------------------------------------
# 2. Covariables de cellule
# ---------------------------------------------------------------------------

def rarete_famille(rare_vrai, ok, fam, porte_minorite):
    """H1a : la personne est elle rare AILLEURS dans la meme famille thematique ?

    rare_vrai, ok : matrices booleennes (personnes x items).
    fam           : vecteur des noms de famille par item.
    porte_minorite: vecteur booleen, l'item porte au moins une modalite minoritaire.

    Renvoie (deplace, valide), deux matrices booleennes. Seuls les items qui portent une
    modalite minoritaire entrent dans le calcul : un item sans modalite rare ne peut pas
    porter la rarete deplacee, et l'inclure gonflerait le denominateur sans rien pouvoir
    apporter au numerateur. Une cellule est valide si la personne dispose d'au moins un
    AUTRE item exploitable de la famille.
    """
    n, m = rare_vrai.shape
    deplace = np.zeros((n, m), dtype=bool)
    valide = np.zeros((n, m), dtype=bool)
    for nom in sorted({f for f in fam if f}):
        cols = np.flatnonzero((fam == nom) & porte_minorite)
        if len(cols) < 2:
            continue
        n_rare = rare_vrai[:, cols].sum(axis=1)
        n_ok = ok[:, cols].sum(axis=1)
        for j in cols:
            deplace[:, j] = (n_rare - rare_vrai[:, j]) > 0
            valide[:, j] = (n_ok - ok[:, j]) >= 1
    return deplace, valide


def rarete_personne(rare_vrai, ok):
    """H1b : taux de reponses rares reelles de la personne, hors de l'item considere.

    Le retrait de l'item lui meme est indispensable : sans lui, la covariable contiendrait
    la reponse qu'on cherche a expliquer, et toute methode qui vise juste paraitrait
    obeir a un mecanisme de deplacement.
    """
    n_rare = rare_vrai.sum(axis=1)[:, None]
    n_ok = ok.sum(axis=1)[:, None]
    den = n_ok - ok
    with np.errstate(invalid="ignore", divide="ignore"):
        return np.where(den > 0, (n_rare - rare_vrai) / np.maximum(den, 1), np.nan)


def rarete_segment(rare_vrai, ok, seg):
    """H2b : taux de reponses rares reelles du segment de la personne, sans la personne.

    seg : vecteur d'entiers de segment, -1 pour un segment inconnu. Une cellule dont le
    segment est inconnu, ou dont le segment ne compte aucune autre personne exploitable
    sur l'item, recoit NaN.
    """
    n, m = rare_vrai.shape
    out = np.full((n, m), np.nan)
    niveaux = [k for k in np.unique(seg) if k >= 0]
    for k in niveaux:
        lignes = np.flatnonzero(seg == k)
        if len(lignes) < 2:
            continue
        n_ok = ok[lignes].sum(axis=0).astype(float)
        n_rare = rare_vrai[lignes].sum(axis=0).astype(float)
        den = n_ok[None, :] - ok[lignes]
        num = n_rare[None, :] - rare_vrai[lignes]
        with np.errstate(invalid="ignore", divide="ignore"):
            out[lignes] = np.where(den > 0, num / np.maximum(den, 1.0), np.nan)
    return out


def modale_rare_segment(verite, ok, mods, seg, colonnes):
    """H2a : la modalite rare la plus frequente dans le segment, sans la personne.

    Renvoie une matrice objet (personnes x items) valant None hors des colonnes demandees,
    hors des segments inconnus, et partout ou le segment ne porte aucune reponse rare une
    fois la personne retiree. En cas d'egalite, la modalite la plus haute dans l'ordre de
    la nomenclature est retenue ; le choix est arbitraire mais deterministe, et il est
    rapporte.
    """
    n, m = verite.shape
    out = np.empty((n, m), dtype=object)
    out[:] = None
    for j in colonnes:
        rares = sorted(mods[j])
        if len(rares) < 2:
            continue
        rang = {mod: r for r, mod in enumerate(rares)}
        propre = np.array([rang.get(v, -1) if o else -1
                           for v, o in zip(verite[:, j], ok[:, j])], dtype=np.int64)
        for k in [x for x in np.unique(seg) if x >= 0]:
            lignes = np.flatnonzero(seg == k)
            base = np.zeros(len(rares), dtype=np.int64)
            vus = propre[lignes]
            for r in vus[vus >= 0]:
                base[r] += 1
            for i, r_propre in zip(lignes, vus):
                c = base if r_propre < 0 else base - np.eye(len(rares),
                                                            dtype=np.int64)[r_propre]
                if c.max() <= 0:
                    continue
                out[i, j] = rares[int(np.argmax(c))]
    return out


def modale_rare_population(verite, ok, mods, colonnes):
    """Meme chose, mais sans segment : la modalite rare modale de la population entiere.

    Elle sert a separer H2, la rarete du segment, de la simple rarete la plus courante de
    l'item. Sans ce temoin, une methode qui predirait toujours la modalite rare la plus
    frequente de la population paraitrait suivre l'etiquette.
    """
    n, m = verite.shape
    out = np.empty((n, m), dtype=object)
    out[:] = None
    for j in colonnes:
        rares = sorted(mods[j])
        if len(rares) < 2:
            continue
        rang = {mod: r for r, mod in enumerate(rares)}
        propre = np.array([rang.get(v, -1) if o else -1
                           for v, o in zip(verite[:, j], ok[:, j])], dtype=np.int64)
        base = np.zeros(len(rares), dtype=np.int64)
        for r in propre[propre >= 0]:
            base[r] += 1
        if base.max() <= 0:
            continue
        oeil = np.eye(len(rares), dtype=np.int64)
        for i, r_propre in enumerate(propre):
            c = base if r_propre < 0 else base - oeil[r_propre]
            if c.max() <= 0:
                continue
            out[i, j] = rares[int(np.argmax(c))]
    return out


def rarete_contexte(rare_vrai, ok, bloc):
    """H5 : taux de reponses rares reelles de la personne HORS du bloc secret de l'item.

    C'est exactement le contexte de C3, les ~119 items du prompt systeme, et celui de B2,
    les items qui servent a mesurer la distance aux voisins. L'item lui meme appartient a
    son bloc, il est donc retire par construction, ainsi que les 29 autres items du bloc :
    aucune information de la cellule expliquee ne rentre dans la covariable.
    """
    n, m = rare_vrai.shape
    n_bloc = int(bloc.max()) + 1
    tot_rare = rare_vrai.sum(axis=1).astype(float)
    tot_ok = ok.sum(axis=1).astype(float)
    out = np.full((n, m), np.nan)
    for b in range(n_bloc):
        cols = np.flatnonzero(bloc == b)
        r_b = rare_vrai[:, cols].sum(axis=1).astype(float)
        o_b = ok[:, cols].sum(axis=1).astype(float)
        den = tot_ok - o_b
        with np.errstate(invalid="ignore", divide="ignore"):
            v = np.where(den > 0, (tot_rare - r_b) / np.maximum(den, 1.0), np.nan)
        out[:, cols] = v[:, None]
    return out


def est_extreme(pred, items, options, premiere, derniere):
    """Deux matrices booleennes : modalite predite en premiere, en derniere position.

    Une cellule sans prediction, ou dont la prediction est hors nomenclature, est fausse
    dans les deux ; le compte des cellules hors nomenclature est renvoye pour controle,
    il doit rester nul.
    """
    n, m = pred.shape
    p1 = np.zeros((n, m), dtype=bool)
    pK = np.zeros((n, m), dtype=bool)
    hors = 0
    for j, it in enumerate(items):
        a, b, connues = premiere[it], derniere[it], set(options[it])
        col = pred[:, j]
        p1[:, j] = np.fromiter((v in a for v in col), dtype=bool, count=n)
        pK[:, j] = np.fromiter((v in b for v in col), dtype=bool, count=n)
        hors += sum(1 for v in col
                    if v is not None and isinstance(v, str) and v not in connues)
    return p1, pK, hors


# ---------------------------------------------------------------------------
# 3. Confiance du modele, C2 et C3 seulement
# ---------------------------------------------------------------------------

def confiances_locales(paquet, items):
    """p max, par cellule, pour C2 et C3, lues dans les traces du run a5.

    Renvoie condition -> matrice (150 x 149) de flottants, NaN si la cellule n'a pas de
    distribution. Le controle de coherence entre l'argmax de la distribution et la matrice
    de prediction employee partout ailleurs est fait par l'appelant : c'est l'erreur que
    a18 section 2.3 a trouvee dans sa premiere version, elle ne doit pas etre refaite.
    """
    from a5_evaluer import lire_traces, moyenner_passes, en_matrices
    from a5_agents_locaux_gss import TRACES, nomenclature

    table = nomenclature()
    tables, fichiers = lire_traces("")
    ech = pd.read_csv(os.path.join(TRACES, "a5-personnes.csv"))
    vus = set()
    for t in tables.values():
        vus |= {k[0] for k in t}
    personnes = [p for p in ech["pid"] if p in vus]

    sortie = {}
    for condition in ("C2", "C3"):
        fusion, passes = moyenner_passes(tables, condition)
        if not fusion:
            continue
        pred, dist = en_matrices(fusion, personnes, items, table)
        pmax = np.full(pred.shape, np.nan)
        entropie = np.full(pred.shape, np.nan)
        for i in range(pred.shape[0]):
            for j in range(pred.shape[1]):
                d = dist[i, j]
                if d:
                    q = np.array(list(d.values()), dtype=float)
                    pmax[i, j] = float(q.max())
                    q = q[q > 0]
                    entropie[i, j] = float(-(q * np.log2(q)).sum())
        sortie[condition] = {"pmax": pmax, "entropie": entropie, "argmax": pred,
                             "passes": passes, "personnes": personnes}
    # Les blocs, lus dans la trace elle meme : ils servent a verifier que le decoupage
    # recalcule par grille() est bien celui que le run a employe.
    # C3F ecrit le nom de la famille retiree a la place du numero de bloc ; cette
    # condition n'entre pas dans ce rapport et sa trace est ignoree ici.
    bloc_trace = {}
    for (cond, _passe), t in tables.items():
        if cond not in ("C2", "C3"):
            continue
        for (_pid, it), d in t.items():
            bloc_trace.setdefault(it, set()).add(int(d["bloc"]))
    return sortie, bloc_trace, fichiers


# ---------------------------------------------------------------------------
# 4. Bootstrap sur les personnes
# ---------------------------------------------------------------------------
#
# Toutes les mesures de ce dossier sont des rapports de sommes sur les cellules. En les
# reduisant a deux vecteurs par personne, un numerateur et un denominateur, le bootstrap
# sur les personnes devient une somme sur les indices tires, et le meme tirage sert a
# toutes les conditions, ce qui rend les contrastes apparies.

def par_personne(masque_num, masque_den, valeurs=None):
    """Numerateur et denominateur par personne pour un rapport de sommes.

    masque_den : cellules qui entrent dans le denominateur.
    masque_num : cellules qui entrent dans le numerateur, sous ensemble du denominateur.
    valeurs    : si fourni, le numerateur somme cette matrice au lieu de compter les
                 cellules, ce qui donne une moyenne au lieu d'une proportion. Les cellules
                 dont la valeur est NaN sont retirees des DEUX vecteurs, sinon la moyenne
                 serait biaisee par le denominateur.
    """
    den = np.asarray(masque_den, dtype=bool)
    if valeurs is None:
        num = np.asarray(masque_num, dtype=bool) & den
        return num.sum(axis=1).astype(float), den.sum(axis=1).astype(float)
    v = np.asarray(valeurs, dtype=float)
    den = den & np.asarray(masque_num, dtype=bool) & ~np.isnan(v)
    return np.where(den, v, 0.0).sum(axis=1), den.sum(axis=1).astype(float)


def moyenne_par_personne(masque, valeurs):
    """Numerateur et denominateur par personne pour une moyenne sur un jeu de cellules."""
    return par_personne(masque, masque, valeurs=valeurs)


def taux(num, den, idx=None):
    if idx is None:
        d = float(den.sum())
        return float(num.sum()) / d if d > 0 else np.nan
    d = den[idx].sum()
    return num[idx].sum() / d if d > 0 else np.nan


def taux_ic(num, den, idx_boot):
    """Valeur et intervalle a 95 pour cent, personnes reechantillonnees."""
    d = den[idx_boot].sum(axis=1)
    n = num[idx_boot].sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        tir = np.where(d > 0, n / np.maximum(d, 1e-12), np.nan)
    tir = tir[~np.isnan(tir)]
    return (taux(num, den),
            float(np.percentile(tir, 2.5)) if len(tir) else np.nan,
            float(np.percentile(tir, 97.5)) if len(tir) else np.nan,
            tir)


def contraste(num_a, den_a, num_b, den_b, idx_boot):
    """Difference de deux rapports de sommes, memes personnes tirees.

    Le p bilateral est lu sur la position de zero dans la distribution bootstrap, comme en
    a28 et a29. Il ne descend jamais sous 1 sur le nombre de tirages exploitables, ce qui
    evite d'ecrire p = 0 avant une correction pour tests multiples. Un contraste dont l'un
    des deux denominateurs est vide est declare non evaluable et recoit p = 1, choix
    conservateur : il ne peut pas creer de fausse decouverte et il n'allege pas la
    correction appliquee aux autres.
    """
    obs = taux(num_a, den_a) - taux(num_b, den_b)
    da, db = den_a[idx_boot].sum(axis=1), den_b[idx_boot].sum(axis=1)
    na, nb = num_a[idx_boot].sum(axis=1), num_b[idx_boot].sum(axis=1)
    with np.errstate(invalid="ignore", divide="ignore"):
        tir = (np.where(da > 0, na / np.maximum(da, 1e-12), np.nan)
               - np.where(db > 0, nb / np.maximum(db, 1e-12), np.nan))
    tir = tir[~np.isnan(tir)]
    if len(tir) == 0 or not np.isfinite(obs):
        return np.nan, np.nan, np.nan, 1.0
    p = 2.0 * min((tir <= 0).mean(), (tir >= 0).mean())
    return (float(obs), float(np.percentile(tir, 2.5)), float(np.percentile(tir, 97.5)),
            float(min(max(p, 1.0 / len(tir)), 1.0)))


def temoin_par_personne(masque_cible, masque_base, valeurs):
    """Temoin aveugle a la personne, appariee sur la composition en items.

    masque_cible : les cellules dont on veut expliquer la composition, en pratique les
                   fausses raretes d'une methode.
    masque_base  : les cellules qu'une methode aveugle a la personne pourrait atteindre
                   sur le meme item, en pratique les cellules evaluables ou la masse rare
                   humaine selon le mecanisme.
    valeurs      : la covariable, booleenne ou continue.

    Le temoin vaut, item par item, la moyenne de la covariable sur les cellules de base,
    puis la moyenne de ces moyennes ponderee par le nombre de cellules cibles de l'item.
    C'est la valeur qu'obtiendrait une methode qui placerait exactement le meme nombre de
    fausses raretes sur exactement les memes items, mais chez des personnes tirees au
    hasard parmi les repondants de l'item.

    Il est renvoye sous la forme d'un couple numerateur, denominateur par PERSONNE : le
    poids d'item est reparti sur les cellules de base de l'item, ce qui rend le temoin
    reechantillonnable sur les personnes exactement comme la quantite qu'il sert a juger.
    Les poids d'item sont ceux de l'echantillon observe et ne sont pas retires a chaque
    tirage : le bootstrap porte sur les personnes, jamais sur les items, comme partout
    dans ce dossier.
    """
    v = np.asarray(valeurs, dtype=float)
    cible = np.asarray(masque_cible, dtype=bool)
    base = np.asarray(masque_base, dtype=bool) & ~np.isnan(v)
    w_item = cible.sum(axis=0).astype(float)
    n_item = base.sum(axis=0).astype(float)
    with np.errstate(invalid="ignore", divide="ignore"):
        poids = np.where(n_item > 0, w_item / np.maximum(n_item, 1.0), 0.0)
    W = np.where(base, poids[None, :], 0.0)
    return (W * np.nan_to_num(v)).sum(axis=1), W.sum(axis=1)


def temoin_item(masque_cible, masque_base, valeurs):
    """Valeur ponctuelle du temoin aveugle, meme definition que temoin_par_personne."""
    num, den = temoin_par_personne(masque_cible, masque_base, valeurs)
    return taux(num, den)
