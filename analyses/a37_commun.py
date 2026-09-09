"""
a37_commun : briques partagees par les scripts a37, « notre 1,12 est il l'effet de
consensus liberal, et que fait la simulation du modele generatif de Brandt et Sleegers ».

Statut : script d'analyse jetable. Aucun appel de modele de langage, lecture seule sur
data/. Aucun script existant n'est modifie ; a30_commun, a2_baselines_gss, a2_commun,
a25_commun, a28_commun et a9_commun sont importes tels quels.

CE QUE CE MODULE PORTE
----------------------
  1. L'orientation gauche droite de chaque item, item par item, ecrite a la lecture du
     libelle, avec un niveau de certitude et une justification (codeur A).
  2. Un second codeur, entierement automatique et qui ne lit aucun libelle (codeur B) :
     le pole gauche d'un item est celui que le camp de gauche endosse le plus. Le taux
     d'accord entre les deux codeurs est une sortie du rapport.
  3. La derive agregee d'un item : la position moyenne de l'echantillon sur l'echelle de
     l'item, ramenee au point neutre de l'item, et orientee gauche vers droite.
     Convention : D > 0 veut dire que l'echantillon penche a DROITE sur cet item.
  4. Un temoin « position seule » : la dispersion qu'un camp aurait si sa seule propriete
     etait sa position moyenne. C'est la distribution de dispersion maximale a position
     donnee (maximum d'entropie a moyenne fixee). Il sert a repondre a la question
     « que reste t il du 1,12 une fois la derive controlee ».
  5. La regression du logarithme du rapport de dispersion sur la derive, avec intervalles
     de bootstrap sur les personnes et test de permutation de l'etiquette de camp.

CONVENTION DE SIGNE, ECRITE UNE FOIS POUR TOUTES
------------------------------------------------
Un item recoit un score par modalite dans [0, 1] : 0 au pole de gauche, 1 au pole de
droite. Le champ `sens` vaut +1 si l'ordre des modalites declare dans question_master va
du pole de gauche vers le pole de droite, et -1 s'il va dans l'autre sens. Le point
neutre d'un item est 0,5 : c'est la modalite mediane pour un item a nombre impair de
modalites (« about right », « about the same »), et le partage a parts egales pour un
item binaire.

La derive agregee vaut D = moyenne du score sur l'echantillon entier moins 0,5.
  D > 0 : la majorite penche a droite sur cet item (peine de mort, police).
  D < 0 : la majorite penche a gauche sur cet item (avortement, libertes civiles).

Le modele de Brandt et Sleegers predit alors une PENTE NEGATIVE de log(rapport de
dispersion droite sur gauche) sur D : la ou l'opinion penche a gauche, la gauche est
pres du consensus et la droite s'en ecarte de facon variee, donc le rapport depasse 1 ;
la ou l'opinion penche a droite, c'est l'inverse.
"""

import os
import sys

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import a30_commun as C  # noqa: E402
from a25_commun import sans_score  # noqa: E402

RACINE = C.RACINE
SORTIE = C.SORTIE
GRAINE = 20260908
N_BOOT = 1000
N_PERM = 2000


# ---------------------------------------------------------------------------
# 1. Codeur A : l'orientation gauche droite lue sur le libelle
# ---------------------------------------------------------------------------
#
# Format : item -> (sens, niveau, justification).
#   sens +1 : l'ordre des modalites de question_master va du pole de GAUCHE vers le pole
#             de DROITE. sens -1 : l'inverse.
#   niveau  : [CONFIRME] la direction est celle d'une echelle standardisee de la science
#             politique americaine, employee telle quelle dans la litterature du GSS
#             (echelle d'avortement, echelle de tolerance de Stouffer, echelle de roles de
#             genre, peine de mort, immigration, explications de l'ecart racial) ;
#             [PROBABLE] la direction est donnee sans ambiguite par le libelle et par
#             l'alignement partisan documente du sujet ;
#             [HYPOTHESE] la direction est deduite du sujet seul et pourrait se discuter.
#
# Un item absent de cette table n'a AUCUNE orientation gauche droite et sort de toutes les
# analyses de derive. C'est le cas de tous les faits biographiques, de tous les items de
# bien etre, de confiance interpersonnelle, de perception de richesse, de pratique
# religieuse, et des trois items de tolerance envers le raciste, ou les deux normes
# s'opposent et ou le pole de gauche n'est pas defini (voir a25_commun, meme decision).
#
# Regle uniforme sur la batterie de depenses : « too little » est le pole de gauche, sauf
# pour la defense nationale ou c'est « too much ». La regle est appliquee a l'identique
# aux dix sept items, y compris a ceux dont le contenu est faiblement ideologique, qui
# recoivent le niveau [HYPOTHESE] et sortent de l'analyse de sensibilite stricte.

_DEP_FORT = ["natenvir/y", "natheal/y", "natcity/y", "natdrug/y", "nateduc/y",
             "natrace/y", "nataid/y", "natfare/y", "natsoc", "natmass", "natchld",
             "natenrgy"]
_DEP_FAIBLE = ["natspac/y", "natroad", "natpark", "natsci"]

ORIENTATION = {
    # --- depenses publiques ------------------------------------------------
    **{it: (+1, "[PROBABLE]",
            "regle uniforme de la batterie nat* : « too little » est le pole de gauche ; "
            "sujet dont l'alignement partisan est documente")
       for it in _DEP_FORT},
    **{it: (+1, "[HYPOTHESE]",
            "meme regle uniforme, mais le sujet est faiblement ideologique ; "
            "exclu de l'analyse de sensibilite stricte")
       for it in _DEP_FAIBLE},
    "natarms/y": (-1, "[PROBABLE]",
                  "seule exception a la regle : sur la defense nationale, « too much » "
                  "est le pole de gauche"),
    # --- avortement, echelle standard --------------------------------------
    **{it: (+1, "[CONFIRME]",
            "echelle d'avortement du GSS : « yes » est le pole de gauche")
       for it in ["abdefect", "abnomore", "abhlth", "abpoor", "abrape", "absingle",
                  "abany"]},
    # --- roles de genre, echelle standard ----------------------------------
    "fechld": (+1, "[CONFIRME]",
               "echelle de roles de genre : approuver « une mere qui travaille peut "
               "etablir une relation aussi chaleureuse » est le pole egalitaire"),
    "fepresch": (-1, "[CONFIRME]",
                 "approuver « un enfant d'age prescolaire souffre » est le pole "
                 "traditionnel, donc l'ordre va de droite a gauche"),
    "fefam": (-1, "[CONFIRME]",
              "approuver « il vaut bien mieux que l'homme soit dehors et la femme au "
              "foyer » est le pole traditionnel"),
    "fepol": (-1, "[CONFIRME]",
              "approuver « les hommes sont mieux faits pour la politique » est le pole "
              "traditionnel"),
    "fehire": (+1, "[PROBABLE]",
               "approuver l'effort special d'embauche des femmes est le pole de gauche"),
    # --- tolerance politique, echelle de Stouffer --------------------------
    "spkath/y": (+1, "[CONFIRME]", "echelle de Stouffer : autoriser est le pole de gauche"),
    "colath": (+1, "[CONFIRME]", "echelle de Stouffer"),
    "spkcom/y": (+1, "[PROBABLE]", "echelle de Stouffer, cible communiste"),
    "colcom/y": (-1, "[PROBABLE]",
                 "« yes, fired » vient en premier, donc l'ordre va de droite a gauche"),
    "libcom/y": (-1, "[PROBABLE]", "« remove » vient en premier"),
    "spkhomo/y": (+1, "[CONFIRME]", "echelle de Stouffer, cible homosexuelle"),
    "colhomo": (+1, "[CONFIRME]", "echelle de Stouffer, cible homosexuelle"),
    "libhomo/y": (-1, "[CONFIRME]", "« remove » vient en premier"),
    # --- ordre, police, justice --------------------------------------------
    "cappun": (-1, "[CONFIRME]",
               "peine de mort : « favor » est le pole de droite et vient en premier"),
    "courts": (+1, "[PROBABLE]",
               "« too harshly » est le pole de gauche, « not harshly enough » celui de "
               "droite"),
    "polhitok/y": (-1, "[PROBABLE]",
                   "approuver un coup porte par un policier est le pole de droite"),
    "polabuse/y": (-1, "[PROBABLE]", "meme raisonnement, cible qui a insulte le policier"),
    "polattak/y": (-1, "[HYPOTHESE]",
                   "meme famille, mais approuver quand le citoyen frappe le policier "
                   "n'est pas une position de droite marquee ; exclu du strict"),
    "gunlaw": (+1, "[CONFIRME]",
               "permis de police avant achat d'arme : « favor » est le pole de gauche"),
    "grass": (+1, "[CONFIRME]", "legalisation du cannabis : « legal » est le pole de gauche"),
    # --- moeurs -------------------------------------------------------------
    "homosex": (-1, "[CONFIRME]",
                "« always wrong » vient en premier, donc l'ordre va de droite a gauche"),
    "marhomo": (+1, "[CONFIRME]",
                "mariage entre personnes de meme sexe : « strongly agree » est le pole "
                "de gauche"),
    "xmarsex": (-1, "[PROBABLE]", "permissivite sexuelle : « always wrong » en premier"),
    "pillok": (+1, "[PROBABLE]",
               "contraception disponible pour les adolescents : approuver est le pole de "
               "gauche"),
    "sexeduc": (+1, "[CONFIRME]",
                "education sexuelle a l'ecole : « favor » est le pole de gauche"),
    "pornlaw": (-1, "[PROBABLE]",
                "l'ordre va de l'interdiction totale a l'absence de loi, donc de droite "
                "a gauche"),
    "divlaw": (+1, "[PROBABLE]",
               "divorce plus facile est le pole de gauche et vient en premier"),
    "spanking": (-1, "[PROBABLE]",
                 "approuver la fessee est le pole traditionnel et vient en premier"),
    "prayer": (+1, "[PROBABLE]",
               "approuver l'arret de la Cour supreme qui interdit la priere obligatoire "
               "a l'ecole est le pole de gauche"),
    # --- fin de vie ---------------------------------------------------------
    "letdie1": (+1, "[PROBABLE]",
                "autoriser le medecin a mettre fin a la vie : « yes » est le pole "
                "permissif, associe a la gauche sur les enquetes americaines"),
    **{it: (+1, "[HYPOTHESE]",
            "droit de mettre fin a sa vie : « yes » traite comme le pole permissif, mais "
            "l'alignement partisan de ces quatre items est faible et conteste ; "
            "exclu de l'analyse de sensibilite stricte")
       for it in ["suicide1", "suicide2", "suicide3", "suicide4"]},
    # --- race, immigration --------------------------------------------------
    "racdif1": (+1, "[CONFIRME]",
                "explication de l'ecart racial par la discrimination : « yes » est le "
                "pole de gauche"),
    "racdif2": (-1, "[CONFIRME]",
                "explication par une capacite innee : « yes » est le pole de droite"),
    "racdif3": (+1, "[PROBABLE]",
                "explication par le manque d'education et de chances : pole de gauche"),
    "racdif4": (-1, "[CONFIRME]",
                "explication par le manque de volonte : « yes » est le pole de droite"),
    "letin1a": (+1, "[CONFIRME]",
                "nombre d'immigrants : « increased a lot » est le pole de gauche et "
                "vient en premier"),
    "discaff": (-1, "[PROBABLE]",
                "croire probable qu'un Blanc soit ecarte au profit d'un Noir est le pole "
                "de droite et vient en premier"),
    "discaffw": (+1, "[PROBABLE]",
                 "croire probable qu'une femme soit ecartee est le pole de gauche"),
    "discaffm": (-1, "[PROBABLE]",
                 "croire probable qu'un homme soit ecarte est le pole de droite"),
    # --- economie -----------------------------------------------------------
    "tax": (-1, "[PROBABLE]",
            "« too high » est le pole de droite et vient en premier"),
    "getahead": (-1, "[PROBABLE]",
                 "« hard work most important » est le pole de droite et vient en premier"),
    # --- confiance dans les institutions ------------------------------------
    # La direction depend de l'institution, elle n'est pas uniforme sur la batterie.
    "conarmy": (-1, "[PROBABLE]", "confiance dans l'armee : pole de droite en premier"),
    "conbus": (-1, "[PROBABLE]",
               "confiance dans les grandes entreprises : pole de droite en premier"),
    "conclerg": (-1, "[PROBABLE]",
                 "confiance dans la religion organisee : pole de droite en premier"),
    "conlabor": (+1, "[PROBABLE]",
                 "confiance dans les syndicats : pole de gauche en premier"),
    "conpress": (+1, "[PROBABLE]", "confiance dans la presse : pole de gauche en premier"),
    "consci": (+1, "[PROBABLE]",
               "confiance dans la communaute scientifique : pole de gauche en premier"),
    "coneduc": (+1, "[HYPOTHESE]",
                "confiance dans l'education, direction moins nette ; exclu du strict"),
    "confed": (+1, "[HYPOTHESE]",
               "confiance dans l'executif federal, direction dependante de qui gouverne "
               "en 2022 ; exclu du strict"),
    "confinan": (-1, "[HYPOTHESE]", "confiance dans la finance ; exclu du strict"),
    "conjudge": (-1, "[HYPOTHESE]",
                 "confiance dans la Cour supreme apres 2022 ; exclu du strict"),
    "conmedic": (+1, "[HYPOTHESE]", "confiance dans la medecine ; exclu du strict"),
}

# Les items volontairement laisses sans orientation, avec la raison. Sert au tableau de
# protocole : un lecteur doit pouvoir verifier qu'aucun item n'a ete oublie par accident.
SANS_ORIENTATION = {
    "spkrac/y": "deux normes s'opposent, le pole de gauche n'est pas defini (a25 : aucune)",
    "colrac": "idem spkrac/y",
    "librac/y": "idem spkrac/y",
    "conlegis": "confiance dans le Congres, direction non definie",
    "contv": "confiance dans la television, direction non definie",
    "pres16": "choix de candidat : c'est la variable de camp elle meme, pas une position",
    "if16who": "idem pres16",
    "vote16": "participation declaree, un fait et non une position",
    "attend": "pratique religieuse, un comportement et non une position de politique publique",
    "pray": "idem attend", "reborn": "idem attend", "savesoul": "idem attend",
    "bible": "croyance religieuse, hors du champ des positions de politique publique",
    "postlife": "idem bible", "jew": "appartenance religieuse, un fait",
    "relig16*": "idem", "jew16*": "idem", "spjew": "idem", "spfund": "idem",
    "owngun": "possession d'arme, un fait", "hunt1": "chasse, un fait",
    "uswary": "anticipation d'un evenement, pas une position",
    "aged": "cohabitation intergenerationnelle, pas d'alignement gauche droite",
    "trust": "confiance interpersonnelle", "fair": "idem trust", "helpful": "idem trust",
    "wlthwhts": "perception de richesse d'un groupe, pas une position",
    "wlthblks": "idem", "wlthhsps": "idem",
    "racwork": "composition du lieu de travail, un fait",
    "class": "auto classement social, un fait declare",
    "news": "consommation d'information, un comportement",
    "xmovie": "comportement prive", "compuse*": "equipement", "webmob": "equipement",
    "usewww*": "equipement", "othlang": "competence declaree",
    "granborn": "fait biographique", "uscitzn*": "fait", "fucitzn": "fait",
    "mnthsusa": "fait", "income": "fait", "incom16": "fait", "finrela": "fait",
    "satfin": "bien etre", "finalter": "bien etre", "parsol": "bien etre",
    "kidssol": "anticipation", "happy": "bien etre", "hapmar": "bien etre",
    "satjob": "bien etre", "life": "bien etre", "health": "etat de sante",
    "joblose": "anticipation", "jobfind": "anticipation",
    "richwork": "preference de travail, pas d'alignement gauche droite",
    "unemp": "fait biographique", "union1": "appartenance, un fait",
    "wrkstat": "fait", "evwork": "fait", "wrkgovt1": "fait", "wrkgovt2": "fait",
    "partfull": "fait", "wksub1": "fait", "wksup1": "fait", "spdeg*": "fait",
    "mobile16": "fait", "dwelown16": "fait", "divorced": "fait", "posslq/y": "fait",
}


# ---------------------------------------------------------------------------
# 2. Twin-2K-500 : orientation des dix items d'attitudes politiques
# ---------------------------------------------------------------------------
#
# QID287, matrice de dix politiques publiques sur la meme echelle a cinq points,
# 1 « strongly oppose » a 5 « strongly support ». Huit des dix sont des politiques
# progressistes formulees a l'endroit : soutenir est le pole de gauche, donc l'ordre
# numerique croissant va de droite a gauche, sens -1. Deux sont formulees a l'envers
# (expulsions, bons pour remplacer Medicare) : soutenir est le pole de droite, sens +1.

ORIENTATION_TWIN = {
    "QID287_1": (-1, "[CONFIRME]", "taxe carbone : soutenir est le pole de gauche"),
    "QID287_2": (-1, "[CONFIRME]",
                 "40 pour cent des depenses d'energie propre aux communautes pauvres"),
    "QID287_3": (-1, "[CONFIRME]", "electricite sans carbone en 2035, investissement federal"),
    "QID287_4": (-1, "[CONFIRME]", "Medicare for All"),
    "QID287_5": (-1, "[CONFIRME]", "option publique d'assurance sante"),
    "QID287_6": (-1, "[CONFIRME]", "voie vers la citoyennete pour les sans papiers"),
    "QID287_7": (-1, "[CONFIRME]", "conge parental paye obligatoire"),
    "QID287_10": (-1, "[CONFIRME]", "impot de 2 pour cent sur les patrimoines de plus de 50 M$"),
    "QID287_11": (+1, "[CONFIRME]",
                  "augmenter les expulsions : soutenir est le pole de DROITE, item "
                  "formule a l'envers"),
    "QID287_12": (+1, "[CONFIRME]",
                  "bons de sante prives en remplacement de Medicare : soutenir est le "
                  "pole de DROITE, item formule a l'envers"),
}


# ---------------------------------------------------------------------------
# 3. Scores par modalite et derive agregee
# ---------------------------------------------------------------------------

def scores_gss(items, options, orientation=None):
    """Matrice de scores (J, kmax), 0 au pole de gauche et 1 au pole de droite.

    Renvoie aussi le masque des items orientes, le niveau de certitude et le nombre de
    modalites utiles. Un item dont la liste de modalites contient une modalite
    « inapplicable » est refuse : cette modalite n'a pas de place sur l'echelle et le
    point neutre ne serait plus 0,5.
    """
    orientation = ORIENTATION if orientation is None else orientation
    J = len(items)
    kmax = max(len(options[it]) for it in items)
    S = np.full((J, kmax), np.nan, dtype=np.float64)
    oriente = np.zeros(J, dtype=bool)
    niveaux, sens_a, justifs = [], [], []
    for j, it in enumerate(items):
        e = orientation.get(it)
        opts = options[it]
        if e is None:
            niveaux.append(""), sens_a.append(0), justifs.append(
                SANS_ORIENTATION.get(it, "non oriente"))
            continue
        sens, niveau, justif = e
        assert not any(sans_score(o) for o in opts), \
            f"{it} : modalite inapplicable, orientation refusee"
        K = len(opts)
        assert K >= 2, it
        r = np.arange(K, dtype=np.float64) / (K - 1.0)
        S[j, :K] = r if sens > 0 else 1.0 - r
        oriente[j] = True
        niveaux.append(niveau), sens_a.append(sens), justifs.append(justif)
    return S, oriente, np.array(sens_a), np.array(niveaux, dtype=object), \
        np.array(justifs, dtype=object)


def scores_generiques(ks, sens):
    """Meme chose quand les modalites sont des codes numeriques ordonnes (Twin).

    ks : nombre de modalites par item. sens : +1 ou -1 par item, 0 si non oriente.
    """
    J = len(ks)
    kmax = int(max(ks))
    S = np.full((J, kmax), np.nan, dtype=np.float64)
    for j in range(J):
        if sens[j] == 0:
            continue
        K = int(ks[j])
        r = np.arange(K, dtype=np.float64) / max(K - 1.0, 1.0)
        S[j, :K] = r if sens[j] > 0 else 1.0 - r
    return S


def derive(tables, S):
    """Derive agregee par item : position moyenne moins le point neutre 0,5.

    tables : (B, J, K) tables de contingence. S : (J, K) scores, NaN hors modalites.
    Retourne (B, J). Positif = l'echantillon penche a DROITE sur cet item.
    """
    Sz = np.nan_to_num(S, nan=0.0)[None, :, :]
    valide = np.isfinite(S)[None, :, :]
    num = (tables * Sz * valide).sum(axis=2)
    den = (tables * valide).sum(axis=2)
    with np.errstate(divide="ignore", invalid="ignore"):
        return num / np.where(den > 0, den, np.nan) - 0.5


def position(tables, S):
    """Position moyenne brute (sans retrancher 0,5), utile pour le temoin de position."""
    return derive(tables, S) + 0.5


# ---------------------------------------------------------------------------
# 4. Codeur B, automatique, qui ne lit aucun libelle
# ---------------------------------------------------------------------------

def codeur_empirique(ind, masque_gauche, masque_droite, ks):
    """Oriente chaque item par le camp qui endosse le plus les premieres modalites.

    Le rang moyen declare est calcule dans chaque camp ; si le camp de gauche a le rang
    moyen le plus bas, l'ordre declare va de gauche a droite, sens +1, sinon -1.
    Aucun libelle n'est lu : c'est un codeur entierement automatique, dont le seul defaut
    est d'etre construit sur les memes donnees, ce qui est declare dans le rapport.
    """
    J, kmax = ind.J, ind.k
    R = np.full((J, kmax), np.nan)
    for j in range(J):
        K = int(ks[j])
        R[j, :K] = np.arange(K, dtype=np.float64) / max(K - 1.0, 1.0)
    pg = position(ind.tables(C.poids_plein(masque_gauche)), R)[0]
    pdte = position(ind.tables(C.poids_plein(masque_droite)), R)[0]
    ecart = pdte - pg
    sens = np.where(ecart > 0, 1, -1)
    return sens.astype(int), ecart


# ---------------------------------------------------------------------------
# 5. Temoin « position seule » : dispersion maximale a position donnee
# ---------------------------------------------------------------------------

def maxent_gs(m, s, tol=1e-10, iters=200):
    """Gini Simpson de la loi de dispersion maximale sur s de moyenne m.

    p_k proportionnel a exp(theta s_k), theta resolu par bissection. C'est le temoin de
    position : la dispersion qu'un camp aurait si sa seule propriete etait sa position
    moyenne, et rien d'autre. Pour un item binaire, la moyenne determine entierement la
    loi et le temoin coincide exactement avec la mesure : c'est le point de fond du
    rapport, la dispersion d'un item binaire EST sa position.
    """
    s = np.asarray(s, dtype=np.float64)
    s = s[np.isfinite(s)]
    if len(s) < 2 or not np.isfinite(m):
        return np.nan
    lo, hi = s.min(), s.max()
    if not (lo + tol < m < hi - tol):
        return 0.0

    def moy(th):
        z = th * s
        z = z - z.max()
        p = np.exp(z)
        p /= p.sum()
        return float(p @ s), p

    a, b = -500.0, 500.0
    for _ in range(iters):
        c = 0.5 * (a + b)
        mm, _ = moy(c)
        if mm < m:
            a = c
        else:
            b = c
        if b - a < 1e-12:
            break
    _, p = moy(0.5 * (a + b))
    return float(1.0 - (p * p).sum())


def maxent_gs_vectorise(pos, S, iters=120):
    """Meme temoin, vectorise sur (B, J) positions et (J, K) scores.

    Bissection simultanee sur theta pour tous les items et tous les tirages. Les entrees
    hors de l'etendue de l'echelle, ou les items non orientes, rendent NaN.
    """
    S = np.asarray(S, dtype=np.float64)
    valide = np.isfinite(S)
    Sz = np.nan_to_num(S, nan=0.0)
    lo = np.where(valide.any(axis=1), np.nanmin(np.where(valide, S, np.inf), axis=1), np.nan)
    hi = np.where(valide.any(axis=1), np.nanmax(np.where(valide, S, -np.inf), axis=1), np.nan)
    pos = np.asarray(pos, dtype=np.float64)
    a = np.full(pos.shape, -500.0)
    b = np.full(pos.shape, 500.0)
    V = valide[None, :, :]
    SS = Sz[None, :, :]
    def loi(c):
        z = np.where(V, c[:, :, None] * SS, -np.inf)
        zmax = z.max(axis=2, keepdims=True)
        zmax = np.where(np.isfinite(zmax), zmax, 0.0)
        p = np.where(V, np.exp(z - zmax), 0.0)
        return p / np.maximum(p.sum(axis=2, keepdims=True), 1e-300)

    for _ in range(iters):
        c = 0.5 * (a + b)
        m = (loi(c) * SS).sum(axis=2)
        plus_bas = m < pos
        a = np.where(plus_bas, c, a)
        b = np.where(plus_bas, b, c)
    p = loi(0.5 * (a + b))
    gs = 1.0 - (p * p).sum(axis=2)
    hors = (pos <= lo[None, :] + 1e-10) | (pos >= hi[None, :] - 1e-10)
    gs = np.where(hors, 0.0, gs)
    return np.where(np.isfinite(pos) & valide.any(axis=1)[None, :], gs, np.nan)


def gs_temoin(tables, S, iters=120):
    """Temoin de position, mis a la meme echelle que l'estimateur employe partout ailleurs.

    a30 mesure la dispersion par l'estimateur de Gini Simpson SANS BIAIS,
    somme n_k (n_k - 1) / (N (N - 1)), qui vaut N / (N - 1) fois l'estimateur naif
    1 - somme p^2. Le temoin de position est construit sur une loi, donc sur l'estimateur
    naif. Sans ce facteur, la comparaison entre le temoin et la mesure porterait une
    difference constante de correction de petit echantillon, et non une difference de
    structure. Le facteur est applique item par item avec l'effectif reellement observe
    sur cet item dans ce camp.
    """
    N = (tables * np.isfinite(S)[None, :, :]).sum(axis=2)
    gs = maxent_gs_vectorise(position(tables, S), S, iters)
    corr = np.where(N > 1.0, N / (N - 1.0), np.nan)
    return gs * corr


def gs_temoin_position(tables, S, ks):
    """Gini Simpson du temoin de position, item par item. tables : (1, J, K)."""
    pos = position(tables, S)[0]
    out = np.full(len(ks), np.nan)
    for j in range(len(ks)):
        if not np.isfinite(pos[j]) or not np.isfinite(S[j]).any():
            continue
        out[j] = maxent_gs(pos[j], S[j, :int(ks[j])])
    return out


# ---------------------------------------------------------------------------
# 6. Regression et bootstrap sur les personnes
# ---------------------------------------------------------------------------

def ols(x, y):
    """Moindres carres simples. Retourne pente, ordonnee a l'origine, R2, n."""
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    ok = np.isfinite(x) & np.isfinite(y)
    n = int(ok.sum())
    if n < 3:
        return np.nan, np.nan, np.nan, n
    xx, yy = x[ok], y[ok]
    vx = xx.var()
    if vx <= 0:
        return np.nan, np.nan, np.nan, n
    pente = float(np.cov(xx, yy, bias=True)[0, 1] / vx)
    const = float(yy.mean() - pente * xx.mean())
    resid = yy - (const + pente * xx)
    r2 = float(1.0 - resid.var() / yy.var()) if yy.var() > 0 else np.nan
    return pente, const, r2, n


def spearman(u, v):
    """Correlation de rang, sur les paires finies."""
    u = np.asarray(u, dtype=float)
    v = np.asarray(v, dtype=float)
    ok = np.isfinite(u) & np.isfinite(v)
    if ok.sum() < 4:
        return np.nan
    ru = pd.Series(u[ok]).rank().to_numpy()
    rv = pd.Series(v[ok]).rank().to_numpy()
    return float(np.corrcoef(ru, rv)[0, 1])


def poids_bootstrap_global(n, b, rng):
    """Bootstrap sur les personnes de l'echantillon ENTIER, forme (b, n).

    Un seul tirage sert a la fois a la derive agregee (calculee sur tout le monde) et aux
    deux camps (obtenus en multipliant par le masque du camp). Reechantillonner les deux
    camps separement, comme le fait a30, casserait le lien entre l'abscisse et
    l'ordonnee de la regression, qui viennent des memes personnes.
    """
    mult = rng.multinomial(n, np.full(n, 1.0 / n), size=b).astype(np.float32)
    return mult


def ratios_et_derive(ind, w_tous, w_gauche, w_droite, S, mesure="gs"):
    """Pour chaque tirage : derive agregee, dispersion des deux camps, log du rapport."""
    d = derive(ind.tables(w_tous), S)
    mg = C.mesures(ind.tables(w_gauche))[mesure]
    md = C.mesures(ind.tables(w_droite))[mesure]
    with np.errstate(divide="ignore", invalid="ignore"):
        lr = np.log(md / mg)
    lr[~np.isfinite(lr)] = np.nan
    return d, mg, md, lr


def regression_bootstrap(ind, masque_gauche, masque_droite, S, garde, rng,
                         n_boot=N_BOOT, mesure="gs"):
    """Pente, ordonnee et R2 avec intervalle de bootstrap sur les personnes."""
    n = ind.n
    mg = np.asarray(masque_gauche, dtype=np.float32)
    md = np.asarray(masque_droite, dtype=np.float32)
    tous = np.ones(n, dtype=np.float32)

    d0, vg0, vd0, lr0 = ratios_et_derive(ind, tous[None, :], mg[None, :], md[None, :], S)
    x0, y0 = d0[0], lr0[0]
    x0 = np.where(garde, x0, np.nan)
    y0 = np.where(garde, y0, np.nan)
    pente, const, r2, n_it = ols(x0, y0)
    rho = spearman(x0, y0)

    W = poids_bootstrap_global(n, n_boot, rng)
    d, _, _, lr = ratios_et_derive(ind, W, W * mg[None, :], W * md[None, :], S)
    pentes, consts, r2s = [], [], []
    for t in range(n_boot):
        xt = np.where(garde, d[t], np.nan)
        yt = np.where(garde, lr[t], np.nan)
        p_, c_, r_, _ = ols(xt, yt)
        pentes.append(p_), consts.append(c_), r2s.append(r_)
    pentes = np.array(pentes, dtype=float)
    consts = np.array(consts, dtype=float)
    r2s = np.array(r2s, dtype=float)

    def ic(v):
        v = v[np.isfinite(v)]
        if len(v) < 10:
            return np.nan, np.nan
        return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))

    return {"pente": pente, "pente_ic_bas": ic(pentes)[0], "pente_ic_haut": ic(pentes)[1],
            "ordonnee": const, "ordonnee_ic_bas": ic(consts)[0],
            "ordonnee_ic_haut": ic(consts)[1],
            "ratio_a_derive_nulle": float(np.exp(const)) if np.isfinite(const) else np.nan,
            "r2": r2, "r2_ic_bas": ic(r2s)[0], "r2_ic_haut": ic(r2s)[1],
            "spearman": rho, "n_items": n_it,
            "_pentes_boot": pentes, "_consts_boot": consts,
            "_x": x0, "_y": y0}


def p_permutation_pente(ind, masque_gauche, masque_droite, S, garde, pente_obs, rng,
                        n_perm=N_PERM):
    """Test de permutation de l'etiquette de camp sur la pente.

    La derive agregee est une quantite de l'echantillon entier : elle ne bouge pas quand
    on permute l'etiquette de camp. Seule l'ordonnee bouge. L'hypothese nulle est donc
    exactement « la dispersion relative des deux camps ne depend pas de la derive de
    l'item », ce qui est l'hypothese que le modele de Brandt et Sleegers rejette.
    Estimateur de Phipson et Smyth, jamais nul.
    """
    tous = np.ones(ind.n, dtype=np.float32)
    d0 = derive(ind.tables(tous[None, :]), S)[0]
    x0 = np.where(garde, d0, np.nan)
    pa, pb = C.poids_permutation(np.asarray(masque_droite, dtype=bool),
                                 np.asarray(masque_gauche, dtype=bool), n_perm, rng)
    with np.errstate(divide="ignore", invalid="ignore"):
        lr = np.log(C.mesures(ind.tables(pa))["gs"] / C.mesures(ind.tables(pb))["gs"])
    lr[~np.isfinite(lr)] = np.nan
    stat = []
    for t in range(n_perm):
        p_, _, _, _ = ols(x0, np.where(garde, lr[t], np.nan))
        stat.append(p_)
    stat = np.array(stat, dtype=float)
    stat = stat[np.isfinite(stat)]
    if len(stat) < 10 or not np.isfinite(pente_obs):
        return np.nan
    ge = int((np.abs(stat) >= abs(pente_obs) - 1e-12).sum())
    return float((ge + 1.0) / (len(stat) + 1.0))


def p_bootstrap_bilateral(v):
    """p bilateral tire d'une distribution de bootstrap d'une difference.

    Plancher a 1 / (B + 1) pour ne jamais ecrire p egale zero, meme convention que le
    Phipson et Smyth employe ailleurs dans le dossier.
    """
    v = np.asarray(v, dtype=float)
    v = v[np.isfinite(v)]
    if len(v) < 10:
        return np.nan
    q = min((v <= 0).mean(), (v >= 0).mean())
    return float(max(2.0 * q, 1.0 / (len(v) + 1.0)))


def coder_echelle_fixe(dfs, colonnes, modalites):
    """Code plusieurs tableaux sur une echelle DECLAREE, la meme pour tous.

    a30 emploie coder_numerique_commun, qui construit la table des modalites a partir des
    valeurs rencontrees. Sur les dix items de QID287, deux configurations d'agents
    ecrivent des valeurs hors de l'echelle a cinq points (6 pour `gpt41mini_resume`, 6 a 9
    pour `gpt41mini_resume_json`) : la table commune passe alors a neuf modalites et le
    score de position n'a plus de sens, puisque les rangs ne sont plus ceux de l'echelle.
    Ici l'echelle est imposee, et toute reponse hors echelle est comptee comme manquante.
    Le nombre de reponses hors echelle est renvoye et rapporte.
    """
    index = {m: i for i, m in enumerate(modalites)}
    K = len(modalites)
    sorties, hors = [], []
    for d in dfs:
        codes = np.full((len(d), len(colonnes)), -1, dtype=np.int32)
        n_hors = 0
        for j, c in enumerate(colonnes):
            v = pd.to_numeric(d[c], errors="coerce").to_numpy(dtype=float)
            for i, x in enumerate(v):
                if x != x:
                    continue
                k = index.get(x)
                if k is None:
                    n_hors += 1
                else:
                    codes[i, j] = k
        sorties.append(codes)
        hors.append(n_hors)
    return sorties, np.full(len(colonnes), K, dtype=int), hors


def ecrire(df, nom):
    return C.ecrire(df, nom)
