"""
c7_audit_contamination : la persona des vagues 1-3 contient-elle deja, EN LANGAGE NATUREL,
les reponses d'achat de la vague 4 ?

===========================================================================
PREENREGISTREMENT : resultats/audit-contamination-persona-2026-09-13.md, section 0, ecrite
et COMMITEE avant ce fichier et avant tout calcul (commit 97a3015). Les deux explications
concurrentes E1 (contamination semantique) / E2 (prevoyabilite differentielle), les
predictions P1-P7 et les criteres de refutation y sont fixes.

CE QUI EST ATTAQUE. L'audit `agent/audit/comparateur-conditionne` etablit que les 60 items
attaques sont TOUS de source wave4_Q_wave1_3_A et AUCUN de la persona (intersection nulle),
puis que le meilleur comparateur classique a entree egale plafonne a 0,45 % contre 20,66 %
pour le jumeau LLM -- tout l'ecart vivant dans les 40 items d'achat (33,2 % contre 0,06 %).
L'OBJECTION : cette disjonction est une disjonction d'IDENTIFIANTS DE QUESTIONS, pas de
CONTENU. La persona est de la prose. Si elle decrit marques, magasins, budget, categories
achetees, alors le jumeau ne devine rien : il LIT, et le comparateur « equitable » ne l'etait
pas -- il recevait 634 colonnes structurees sans pouvoir exploiter un contenu semantique
qu'un modele de langage lit sans effort.

L'EXPLICATION CONCURRENTE, innocente, a ne pas negliger au profit de la plus spectaculaire :
les comportements d'achat sont peut-etre simplement PLUS STABLES chez les humains eux-memes
que les reponses a des taches d'heuristiques et biais, largement du bruit de reponse. Ce
script la mesure directement par la stabilite test-retest v1-3 / v4 des deux familles.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / ecrire                   les quinze tables de Twin, l'ecriture CSV
  c7_reidentification.items_communs            les 60 items toujours renseignes
  c7_reidentification.rangs_attaque            L'ATTAQUE, inchangee, garde-fous compris
  c7_reidentification.graine_nom / REF_V4 / REF_V13 / DEMO
  a2_commun.distance_hamming / bootstrap_personnes
  c7_controle_interpretabilite.controle_avant_interpretation   le controle de fidelite

CE QUI EST NOUVEAU ICI, et rien d'autre :
  recouvrement_lexical    la couverture des jetons de contenu de chaque item attaque par le
                          vocabulaire de la persona -- libelles du catalogue ET prose
                          reellement donnee au modele (wave_persona_chunk_001.parquet)
  marques_dans_persona    le test decisif de E1 : les 40 marques citees en vague 4
                          apparaissent-elles dans la prose de persona ?
  S1 / S2 / S2s           comparateurs classiques SERVIS des predicteurs apparentes
  S3                      le controle « niveau seul » : permutation intra-personne des
                          reponses du jumeau, qui conserve le nombre de « oui » et detruit
                          le motif
  T+                      le temoin positif, sans lequel un resultat negatif ne vaut rien
  retest_par_item         accord brut et kappa de Cohen v1-3 / v4, par item, par bloc

ETHIQUE : etude de risque de vie privee sur un jeu deja public (Twin-2K-500). Ce script ne
calcule, n'imprime et n'ecrit JAMAIS un pid, un extrait de persona, une reponse ni un
appariement individuel. Les mesures lexicales ne sortent que sous forme de COMPTES AGREGES
portant sur des termes issus du CATALOGUE PUBLIC DES QUESTIONS -- jamais de termes extraits
de la prose des repondants. Aucun appel de modele de langage, aucun reseau, aucune depense,
aucun arriere-plan. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_audit_contamination.py
===========================================================================
"""

import json
import os
import re
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                    # noqa: E402
from a2_commun import bootstrap_personnes                                 # noqa: E402
from c7_reidentification import (                                         # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13, DEMO,
)
from c7_controle_interpretabilite import (                                # noqa: E402
    controle_avant_interpretation, EchecControleInterpretabilite,
)

GRAINE = 20260913
N_TIRAGES_LIENS = 20
N_BOOTSTRAP = 2000
N_PLIS = 5
K_SELECTION = 25          # colonnes de persona retenues par item pour S2 (reduction declaree)
MAX_MODALITES = 8         # binning des colonnes numeriques de la persona

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RACINE_TWIN = os.path.join(RACINE, "data", "twin2k500")
CATALOGUE = os.path.join(RACINE_TWIN, "question_catalog_and_human_response_csv",
                         "question_catalog.json")
REPONSES_V13 = os.path.join(RACINE_TWIN, "question_catalog_and_human_response_csv",
                            "wave1_3_response.csv")
MAPPING_V4 = os.path.join(RACINE_TWIN, "llm", "wave4_formatted_to_catalog_mapping.json")
PERSONA_PARQUET = os.path.join(RACINE_TWIN, "wave_persona_chunk_001.parquet")

SOURCE_PERSONA = "wave1_3_persona_json"
SOURCE_V4 = "wave4_Q_wave1_3_A"
LLM_REF = "JSON Persona - GPT4.1"

# Les QuestionID de persona portant, au sens le plus large defendable, sur la consommation,
# la depense, le budget ou le mode de vie. Liste DECLAREE et auditable, etablie en lisant
# les 171 libelles du catalogue public (section 1) -- c'est l'entree « servie sur un
# plateau » du comparateur S1. On y met tout ce qui peut de pres ou de loin gouverner un
# « acheteriez-vous ce produit a ce prix ? » : disposition a depenser, revenu, foyer,
# emploi, intention alimentaire, et TOUT le bloc des preferences economiques (aversion au
# risque, actualisation, equivalents certains), qui est la mesure de laboratoire du
# compromis prix / valeur.
QID_DEPENSE = ["QID31", "QID32", "QID33", "QID34"]      # tightwad-spendthrift + scenario
QID_MENAGE = ["QID21", "QID23", "QID24", "QID13", "QID14"]  # revenu, foyer, emploi, age, etude
QID_ALIMENTAIRE = ["QID148"]                             # « je mange moins pour maigrir »
BLOCS_ECO = ("Economic preferences",)                    # prefixe de BlockName

# Jetons trop generiques pour temoigner de quoi que ce soit : boilerplate d'enquete.
STOPLIST = set("""
a about after against all also am an and any are as at be because been before being below
between both but by can cannot could did do does doing down during each few for from
further had has have having he her here hers herself him himself his how i if in into is it
its itself just me more most my myself no nor not now of off on once only or other ought
our ours ourselves out over own please same she should so some such than that the their
theirs them themselves then there these they this those through to too under until up very
was we were what when where which while who whom why will with would you your yours
yourself yourselves question questions answer answers following option options select
choose indicate statement statements next section following consider suppose would could
number enter following best describes think people person persons one two three first
second may might also well much many list write down page task problem problems given
receive received amount amounts money dollars value values right wrong true false yes
""".split())


# ---------------------------------------------------------------------------
# 1. Ce que contient reellement la persona
# ---------------------------------------------------------------------------

def charger_catalogue():
    return json.load(open(CATALOGUE))


def partition_catalogue(cat):
    """La partition publiee des 256 QuestionID en persona / items de vague 4.

    Reprise a l'identique de l'audit `comparateur-conditionne` : le champ `source` du
    catalogue dit de quel objet du depot chaque question provient, le champ `csv_columns`
    donne les colonnes correspondantes. C'est la piece qui etablit, sans supposition, ce
    qui entre dans la persona.
    """
    col_p, col_4 = [], []
    for e in cat:
        cols = e.get("csv_columns") or []
        if e["source"] == SOURCE_PERSONA:
            col_p.extend(cols)
        elif e["source"] == SOURCE_V4:
            col_4.extend(cols)
    return col_p, col_4


def familles_persona(cat):
    """Les familles de questions dont la persona est faite, et le compte de colonnes.

    Renvoie un DataFrame agrege par BlockName : c'est la reponse factuelle a « qu'y a-t-il
    reellement dedans ? ». Aucune reponse de repondant n'intervient ici.
    """
    lignes = {}
    for e in cat:
        if e["source"] != SOURCE_PERSONA:
            continue
        b = e["BlockName"].strip()
        d = lignes.setdefault(b, {"bloc": b, "n_qid": 0, "n_colonnes": 0})
        d["n_qid"] += 1
        d["n_colonnes"] += len(e.get("csv_columns") or [])
    return pd.DataFrame(sorted(lignes.values(), key=lambda d: -d["n_colonnes"]))


def colonnes_consommation(cat):
    """Les colonnes de persona apparentees a la consommation, au sens le plus large.

    C'est l'entree de S1, « servie sur un plateau » : si la persona porte quoi que ce soit
    qui predise un « acheteriez-vous ce produit a ce prix ? », c'est la-dedans. La liste
    des QuestionID est declaree en tete de fichier et verifiable contre le catalogue.
    """
    vises = set(QID_DEPENSE) | set(QID_MENAGE) | set(QID_ALIMENTAIRE)
    cols, detail = [], []
    for e in cat:
        if e["source"] != SOURCE_PERSONA:
            continue
        eco = e["BlockName"].strip().startswith(BLOCS_ECO)
        if e["QuestionID"] in vises or eco:
            c = e.get("csv_columns") or []
            cols.extend(c)
            detail.append({"QuestionID": e["QuestionID"], "bloc": e["BlockName"].strip(),
                           "n_colonnes": len(c),
                           "famille": ("depense" if e["QuestionID"] in QID_DEPENSE else
                                       "menage_revenu" if e["QuestionID"] in QID_MENAGE else
                                       "alimentaire" if e["QuestionID"] in QID_ALIMENTAIRE
                                       else "preferences_economiques")})
    return cols, pd.DataFrame(detail)


# ---------------------------------------------------------------------------
# 2. Le recouvrement semantique, item par item
# ---------------------------------------------------------------------------

def jetons(texte):
    """Les jetons de contenu d'un texte : mots alphabetiques de 4 lettres au moins, hors
    boilerplate d'enquete. Meme regle exactement pour la persona et pour les items
    attaques, pour que la comparaison entre blocs soit symetrique."""
    mots = re.findall(r"[a-z]{4,}", texte.lower())
    return {m for m in mots if m not in STOPLIST}


def vocabulaire_persona(cat):
    """Deux vocabulaires : celui des LIBELLES des 171 questions de persona (catalogue
    public), et celui de la PROSE reellement donnee au modele.

    La prose n'est publiee localement que pour le chunk 001 (294 personnes sur 2 058) :
    reduction declaree au preenregistrement. On renvoie aussi, pour la prose, le compte de
    personas contenant chaque jeton, afin de pouvoir dire « ce terme apparait chez k / 294
    personas » sans jamais citer un extrait.
    """
    libelles = []
    for e in cat:
        if e["source"] != SOURCE_PERSONA:
            continue
        libelles.append(e.get("QuestionText") or "")
        for o in (e.get("Options") or []):
            libelles.append(str(o))
    voc_libelles = jetons(" ".join(libelles))

    textes = pd.read_parquet(PERSONA_PARQUET, columns=["wave1_3_persona_text"])
    textes = textes["wave1_3_persona_text"].astype(str).tolist()
    compte = {}
    for s in (jetons(t) for t in textes):
        for j in s:
            compte[j] = compte.get(j, 0) + 1
    return voc_libelles, compte, textes


def descripteurs_items(cat, noms_attaques):
    """Pour chaque item attaque : son libelle, son bloc, ses jetons de contenu, et -- pour
    les items d'achat -- la categorie de produit, le descriptif produit et la MARQUE.

    La marque est le premier groupe de mots capitalises du descriptif produit (« Land O
    Lakes », « Tylenol », « Purina »...). C'est le test decisif de E1 : une marque de
    vague 4 presente dans la persona serait de la contamination litterale.
    """
    mapping = {x["formatted_column"]: x["QuestionID"] for x in json.load(open(MAPPING_V4))}
    par_qid = {e["QuestionID"]: e for e in cat if e["source"] == SOURCE_V4}
    out = []
    for col in noms_attaques:
        e = par_qid.get(mapping.get(col, ""), None)
        if e is None:
            out.append({"item": col, "bloc_catalogue": "INCONNU", "jetons": set(),
                        "categorie": "", "produit": "", "marque": ""})
            continue
        txt = " ".join((e.get("QuestionText") or "").split())
        cat_prod = produit = marque = ""
        m = re.search(r"product category:\s*(.+?)\.\s*Suppose", txt)
        if m:
            cat_prod = m.group(1).strip()
        m = re.search(r"in that category:\s*(.+?)\.\s*The product is priced", txt)
        if m:
            produit = m.group(1).strip()
            mm = re.match(r"((?:[A-Z][\w'&.-]*\s+){0,3}[A-Z][\w'&.-]*)", produit)
            marque = (mm.group(1).strip() if mm else produit.split()[0])
        # les jetons de contenu de l'item, hors options (identiques pour les 40 achats)
        out.append({"item": col, "bloc_catalogue": e["BlockName"].strip(),
                    "jetons": jetons(txt), "categorie": cat_prod,
                    "produit": produit, "marque": marque})
    return out


def recouvrement(desc, voc_libelles, compte_prose, textes_prose, seuil_prose=1):
    """Couverture des jetons de contenu d'un item par le vocabulaire de la persona.

    Trois mesures par item, toutes appliquees A L'IDENTIQUE aux 40 items d'achat et aux
    20 items d'heuristiques -- c'est la symetrie qui rend la comparaison entre blocs
    interpretable, et elle est ce qui departe E1 de E2 :

    1. `couv_libelles` / `couv_prose` : fraction des jetons de contenu de l'item presents
       dans les LIBELLES des 171 questions de persona, puis dans la PROSE d'au moins
       `seuil_prose` persona. Mesure grossiere : elle sature sur du vocabulaire courant.

    2. `jetons_distinctifs` : les jetons de l'item qui n'apparaissent dans AUCUN des
       59 autres items attaques. Ce sont les jetons qui individualisent l'item -- la marque
       et le produit pour un item d'achat, « redwood », « linda », « sequoia » pour un item
       d'heuristiques. `distinctifs_dans_prose` compte ceux d'entre eux presents dans la
       persona. C'est LA mesure de recouvrement semantique : si la persona parlait des
       achats de la personne, les jetons distinctifs d'achat y seraient, et pas ceux des
       heuristiques.

    3. `marque_phrase_*` / `categorie_phrase_*` : la MARQUE et la CATEGORIE recherchees
       comme PHRASES ENTIERES. Une premiere version de ce script cherchait n'importe quel
       jeton de la marque : elle « trouvait » 32 marques sur 40, toutes par des mots
       courants (« extra », « great », « size », « original », « little ») presents dans le
       LIBELLE MEME des questions de persona. C'etait un artefact de mesure, pas une
       contamination ; la regle corrigee est declaree en section 2 du rapport avec les deux
       nombres.
    """
    voc_prose = {j for j, c in compte_prose.items() if c >= seuil_prose}
    bas = [t.lower() for t in textes_prose]
    compte_item = {}
    for d in desc:
        for j in d["jetons"]:
            compte_item[j] = compte_item.get(j, 0) + 1

    def personas_contenant(phrase):
        """Nombre de personas dont la prose contient la phrase, AUX FRONTIERES DE MOT.

        La recherche par sous-chaine nue faisait compter « ARM » (de ARM & HAMMER) chez
        294 personas sur 294, parce que « arm » est dans « warm » et « harm ». C'est le
        meme genre d'artefact que le comptage par jeton isole, et il est corrige ici.
        """
        if not phrase:
            return -1
        p = re.escape(phrase.lower().strip())
        motif = re.compile(r"(?<![a-z])" + p + r"(?![a-z])")
        return int(sum(1 for t in bas if motif.search(t)))

    for d in desc:
        t = d["jetons"]
        d["n_jetons"] = len(t)
        d["couv_libelles"] = (len(t & voc_libelles) / len(t)) if t else np.nan
        d["couv_prose"] = (len(t & voc_prose) / len(t)) if t else np.nan
        distinctifs = {j for j in t if compte_item[j] == 1}
        d["n_distinctifs"] = len(distinctifs)
        d["distinctifs_dans_libelles"] = len(distinctifs & voc_libelles)
        d["distinctifs_dans_prose"] = len(distinctifs & voc_prose)
        d["marque_phrase_personas"] = personas_contenant(d["marque"])
        d["categorie_phrase_personas"] = personas_contenant(d["categorie"])
        d["produit_phrase_personas"] = personas_contenant(d["produit"])
        # la regle naive, conservee pour que l'artefact soit verifiable et non cache
        if d["marque"]:
            mots = re.findall(r"[a-z]{3,}", d["marque"].lower())
            d["marque_jeton_naif_personas"] = int(max(
                [compte_prose.get(w, 0) for w in mots] or [0]))
        else:
            d["marque_jeton_naif_personas"] = -1
    return desc


# ---------------------------------------------------------------------------
# 3. Les comparateurs classiques SERVIS des bons predicteurs
# ---------------------------------------------------------------------------

def coder_colonne(serie):
    """Une colonne brute de wave1_3_response.csv en codes entiers, -1 pour manquant.

    Meme regle exactement que l'audit `comparateur-conditionne` (quantiles a
    MAX_MODALITES pour le numerique a queue longue, factorisation sinon), pour que mes
    comparateurs soient comparables aux siens colonne pour colonne.
    """
    s = serie
    if pd.api.types.is_numeric_dtype(s) and s.nunique(dropna=True) > MAX_MODALITES:
        try:
            q = pd.qcut(s, MAX_MODALITES, labels=False, duplicates="drop")
        except (ValueError, TypeError):
            q = pd.Series(np.full(len(s), np.nan), index=s.index)
        codes = q.to_numpy(dtype=float)
    else:
        codes = pd.factorize(s, use_na_sentinel=True)[0].astype(float)
        codes[codes < 0] = np.nan
    return np.where(np.isnan(codes), -1, codes).astype(np.int32)


def matrice_v13(ids, colonnes):
    """La matrice (personnes x colonnes) d'un sous-ensemble de wave1_3_response.csv,
    alignee ligne a ligne sur l'ordre des personnes de t1_commun.charger()."""
    brut = pd.read_csv(REPONSES_V13, low_memory=False).set_index("pid")
    gardees = [c for c in colonnes if c in brut.columns]
    brut = brut.reindex(index=pd.Index(ids, name="pid"))[gardees]
    mat = np.column_stack([coder_colonne(brut[c]) for c in gardees]).astype(np.int32)
    utile = np.array([len(np.unique(mat[:, j][mat[:, j] >= 0])) > 1
                      for j in range(mat.shape[1])])
    return mat[:, utile], [c for c, u in zip(gardees, utile) if u]


def info_mutuelle(X, y):
    """L'information mutuelle discrete de chaque colonne de X avec y, en nats.

    Calcul direct par table de contingence (bincount sur l'index joint) : exact sur des
    variables deja discretes, et des ordres de grandeur plus rapide que l'estimateur par
    plus proches voisins de sklearn, qui suppose du continu. Sert UNIQUEMENT a selectionner
    des colonnes, et toujours a l'interieur d'un pli d'entrainement.
    """
    n = len(y)
    ky = int(y.max()) + 1
    py = np.bincount(y, minlength=ky) / n
    out = np.zeros(X.shape[1])
    for j in range(X.shape[1]):
        x = X[:, j] + 1                       # -1 (manquant) devient une modalite 0
        kx = int(x.max()) + 1
        joint = np.bincount(x * ky + y, minlength=kx * ky).reshape(kx, ky) / n
        px = joint.sum(axis=1)
        denom = np.outer(px, py)
        nz = joint > 0
        out[j] = float(np.sum(joint[nz] * np.log(joint[nz] / denom[nz])))
    return out


def lois_conditionnelles(X, y, nom, k_selection=None):
    """Pour chaque item attaque, la loi predite HORS PLI a partir de l'entree X.

    Cinq plis : la loi predite pour une personne n'est JAMAIS ajustee sur elle-meme. Si
    k_selection est donne, les k colonnes de X de plus forte information mutuelle avec
    l'item sont choisies DANS LE PLI D'ENTRAINEMENT SEUL -- sans quoi la selection ferait
    fuiter la cible de la personne predite et gonflerait artificiellement le comparateur,
    c'est-a-dire exactement dans le sens qui m'arrangerait si je cherchais a confirmer E1.
    Renvoie la liste, item par item, des lois (n, k_item).
    """
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, KFold
    from sklearn.preprocessing import OneHotEncoder

    n, p = y.shape
    lois = []
    for j in range(p):
        cible = y[:, j]
        k = int(cible.max()) + 1
        proba = np.full((n, k), 1.0 / k)
        classes = np.unique(cible)
        if len(classes) < 2:
            lois.append(proba)
            continue
        compte = np.bincount(cible, minlength=k)
        strat = compte[classes].min() >= N_PLIS
        decoupe = (StratifiedKFold(N_PLIS, shuffle=True, random_state=GRAINE) if strat
                   else KFold(N_PLIS, shuffle=True, random_state=GRAINE))
        for tr, te in decoupe.split(X, cible if strat else None):
            cols = np.arange(X.shape[1])
            if k_selection is not None and X.shape[1] > k_selection:
                mi = info_mutuelle(X[tr], cible[tr])
                cols = np.argsort(-mi, kind="stable")[:k_selection]
            enc = OneHotEncoder(handle_unknown="ignore", min_frequency=10)
            Xtr = enc.fit_transform(X[np.ix_(tr, cols)].astype(str))
            Xte = enc.transform(X[np.ix_(te, cols)].astype(str))
            mod = LogisticRegression(max_iter=600, C=1.0)
            try:
                mod.fit(Xtr, cible[tr])
            except ValueError:
                continue
            proba[te] = 0.0
            proba[np.ix_(te, mod.classes_)] = mod.predict_proba(Xte)
        s = proba.sum(axis=1)
        proba[s <= 0] = 1.0 / k
        proba = proba / proba.sum(axis=1, keepdims=True)
        lois.append(proba)
    return lois


def argmax_lois(lois):
    return np.column_stack([l.argmax(axis=1) for l in lois]).astype(np.int32)


def tirage_lois(lois, rng):
    n = lois[0].shape[0]
    out = np.zeros((n, len(lois)), dtype=np.int32)
    for j, l in enumerate(lois):
        cum = np.cumsum(l, axis=1)
        u = rng.random((n, 1))
        out[:, j] = (u > cum).sum(axis=1).clip(0, l.shape[1] - 1)
    return out


def permuter_intra_personne(g, masque, rng):
    """Permute, chez chaque personne, ses reponses sur les items de `masque`.

    Conserve EXACTEMENT le nombre de « oui » de la personne et detruit le motif. C'est le
    controle qui separe la version faible de E1 (« la persona donne le niveau de depense »)
    de la version forte (« elle donne le motif produit par produit »).
    """
    out = g.copy()
    bloc = out[:, masque]
    for i in range(bloc.shape[0]):
        bloc[i] = rng.permutation(bloc[i])
    out[:, masque] = bloc
    return out


# ---------------------------------------------------------------------------
# 4. Mesure : bassin strictement constant, attaque importee
# ---------------------------------------------------------------------------

def mesurer(nom, gen, pool, items_locaux=None):
    """Top-1 / top-10 du generateur contre le pool, bassin entier, IC bootstrap.

    items_locaux restreint la mesure a un sous-ensemble de COLONNES ; le BASSIN DE
    PERSONNES ne bouge jamais : 2 058 attaques contre 2 058 candidats, quel que soit le
    bloc. C'est le garde-fou qui a deja coute trois erreurs a ce projet.
    """
    g = gen if items_locaux is None else gen[:, items_locaux]
    p = pool if items_locaux is None else pool[:, items_locaux]
    n = g.shape[0]
    rng = np.random.default_rng([GRAINE, graine_nom(nom)])
    rang, top1, top10 = rangs_attaque(g, p, np.arange(n), rng, n_tirages=N_TIRAGES_LIENS)
    m1, b1, h1 = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 1])
    m10, b10, h10 = bootstrap_personnes(top10, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 2])
    return {"mesure": "reidentification", "condition": nom, "n_attaques": n,
            "n_pool": p.shape[0], "n_items": g.shape[1],
            "exactitude": float(np.mean(g == p[np.arange(n)])),
            "top1": m1, "top1_bas": b1, "top1_haut": h1,
            "top10": m10, "top10_bas": b10, "top10_haut": h10,
            "rang_median": float(np.median(rang)), "top1_hasard": 1.0 / p.shape[0]}


def kappa_cohen(a, b):
    """Kappa de Cohen entre deux vecteurs de codes de meme longueur.

    Corrige l'accord du hasard : sans cette correction, un item binaire a 80/20 paraitrait
    « stable » a 68 % sans qu'aucune information individuelle ne circule. C'est la
    correction qui rend comparables les 40 items d'achat (binaires) et les 20 items
    d'heuristiques (jusqu'a plusieurs modalites).
    """
    k = int(max(a.max(), b.max())) + 1
    m = np.bincount(a * k + b, minlength=k * k).reshape(k, k).astype(float)
    n = m.sum()
    po = np.trace(m) / n
    pe = float(np.sum(m.sum(axis=0) * m.sum(axis=1))) / (n * n)
    return (po - pe) / (1 - pe) if pe < 1 else np.nan, po, pe


def stabilite_par_item(v13, v4, noms, est_achat):
    """Accord brut, accord de hasard et kappa v1-3 / v4, item par item.

    C'est la mesure DIRECTE de l'explication E2 : si les items d'heuristiques sont
    instables chez les humains eux-memes, aucun generateur ne peut les predire et la
    concentration de l'effet sur les achats n'a rien a voir avec une contamination.
    """
    lignes = []
    for j in range(v4.shape[1]):
        kap, po, pe = kappa_cohen(v13[:, j], v4[:, j])
        vals, cnt = np.unique(v4[:, j], return_counts=True)
        p = cnt / cnt.sum()
        lignes.append({"item": noms[j], "bloc": "achat" if est_achat[j] else "heuristiques",
                       "n_modalites": int(len(vals)),
                       "entropie_bits": float(-np.sum(p * np.log2(p))),
                       "taux_modal": float(p.max()),
                       "accord_retest": po, "accord_hasard": pe, "kappa_retest": kap})
    return pd.DataFrame(lignes)


def gain_normalise(gen, pool, taux_modal):
    """Gain d'exactitude au-dessus du taux modal, normalise par la marge disponible.

    (exactitude - taux modal) / (1 - taux modal), par item. Rend comparables des items
    binaires et des items a huit modalites : c'est la lecture par item qui ne depend pas
    de la non-linearite du top-1 vis-a-vis du nombre d'items.
    """
    acc = (gen == pool).mean(axis=0)
    return (acc - taux_modal) / np.maximum(1.0 - taux_modal, 1e-9)


# ---------------------------------------------------------------------------
def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t0 = time.time()
    lignes = []

    # --- section 1 : ce que contient la persona -----------------------------
    cat = charger_catalogue()
    col_p, col_4 = partition_catalogue(cat)
    fam = familles_persona(cat)
    print(f"[1] persona : {len(col_p)} colonnes, {len(col_4)} colonnes vague 4, "
          f"intersection {len(set(col_p) & set(col_4))}", flush=True)
    for _, r in fam.iterrows():
        print(f"    {r.bloc:<32} {r.n_qid:>4} QID  {r.n_colonnes:>4} colonnes", flush=True)
        lignes.append({"mesure": "famille_persona", "condition": r.bloc,
                       "n_qid": int(r.n_qid), "n_items": int(r.n_colonnes)})

    cols_conso, detail_conso = colonnes_consommation(cat)
    print(f"[1] colonnes de persona apparentees a la consommation (sens large) : "
          f"{len(cols_conso)} ; dont strictement 'depense/menage/alimentaire' : "
          f"{int(detail_conso[detail_conso.famille != 'preferences_economiques'].n_colonnes.sum())}",
          flush=True)
    for f, g in detail_conso.groupby("famille"):
        lignes.append({"mesure": "persona_consommation", "condition": f,
                       "n_qid": int(len(g)), "n_items": int(g.n_colonnes.sum())})
        print(f"    {f:<28} {len(g):>3} QID  {int(g.n_colonnes.sum()):>4} colonnes",
              flush=True)

    # --- donnees ------------------------------------------------------------
    paq = T1.charger()
    codes, ids, noms_items = paq["codes"], paq["ids"], list(paq["colonnes"])
    items = items_communs(codes, [REF_V4, REF_V13])
    noms_att = [noms_items[i] for i in items]
    est_achat = np.array([c.endswith("_Q295") for c in noms_att])
    pool = codes[REF_V4][:, items]
    v13 = codes[REF_V13][:, items]
    n = pool.shape[0]
    print(f"[1] bassin : {n} personnes, {len(items)} items, dont "
          f"{int(est_achat.sum())} d'achat et {int((~est_achat).sum())} d'heuristiques",
          flush=True)

    # --- section 2 : recouvrement semantique --------------------------------
    voc_lib, compte_prose, textes_prose = vocabulaire_persona(cat)
    n_personas = len(textes_prose)
    print(f"[2] vocabulaire persona : {len(voc_lib)} jetons de contenu dans les libelles ; "
          f"prose de {n_personas} personas (chunk 001, reduction declaree), "
          f"{len(compte_prose)} jetons distincts", flush=True)
    desc = recouvrement(descripteurs_items(cat, noms_att), voc_lib, compte_prose,
                        textes_prose)
    df_desc = pd.DataFrame([{k: v for k, v in d.items() if k != "jetons"} for d in desc])
    df_desc["bloc"] = np.where(est_achat, "achat", "heuristiques")
    for bloc, g in df_desc.groupby("bloc"):
        mq = g[g.marque_phrase_personas >= 0]
        lignes.append({"mesure": "recouvrement_semantique", "condition": bloc,
                       "n_items": int(len(g)),
                       "couv_libelles": float(g.couv_libelles.mean()),
                       "couv_prose": float(g.couv_prose.mean()),
                       "n_distinctifs": float(g.n_distinctifs.mean()),
                       "distinctifs_dans_libelles": int(g.distinctifs_dans_libelles.sum()),
                       "distinctifs_dans_prose": int(g.distinctifs_dans_prose.sum()),
                       "n_distinctifs_total": int(g.n_distinctifs.sum()),
                       "marques_phrase_trouvees": (int((mq.marque_phrase_personas > 0).sum())
                                                   if len(mq) else -1),
                       "categories_phrase_trouvees": (
                           int((mq.categorie_phrase_personas > 0).sum()) if len(mq) else -1),
                       "produits_phrase_trouves": (
                           int((mq.produit_phrase_personas > 0).sum()) if len(mq) else -1),
                       "marques_jeton_naif_trouvees": (
                           int((mq.marque_jeton_naif_personas > 0).sum()) if len(mq) else -1)})
        print(f"[2] bloc {bloc:<13} couverture libelles {g.couv_libelles.mean():.3f} ; "
              f"couverture prose {g.couv_prose.mean():.3f} ; jetons distinctifs "
              f"{int(g.n_distinctifs.sum())} dont {int(g.distinctifs_dans_prose.sum())} "
              f"dans la prose de persona", flush=True)
        if len(mq):
            print(f"    marques trouvees comme PHRASE : "
                  f"{int((mq.marque_phrase_personas > 0).sum())} / {len(mq)} ; "
                  f"categories comme phrase : "
                  f"{int((mq.categorie_phrase_personas > 0).sum())} / {len(mq)} ; "
                  f"produits comme phrase : "
                  f"{int((mq.produit_phrase_personas > 0).sum())} / {len(mq)} ; "
                  f"(regle naive par jeton, artefact : "
                  f"{int((mq.marque_jeton_naif_personas > 0).sum())} / {len(mq)})",
                  flush=True)
    # quels jetons distinctifs, precisement, la persona partage-t-elle avec chaque bloc ?
    # Ces jetons viennent du CATALOGUE PUBLIC des questions, jamais de la prose d'un
    # repondant : les imprimer n'expose aucune donnee individuelle.
    voc_prose = {j for j, c in compte_prose.items() if c >= 1}
    compte_item = {}
    for d in desc:
        for j in d["jetons"]:
            compte_item[j] = compte_item.get(j, 0) + 1
    for bloc, sel in (("achat", est_achat), ("heuristiques", ~est_achat)):
        part = sorted({j for d, k in zip(desc, sel) if k
                       for j in d["jetons"] if compte_item[j] == 1 and j in voc_prose})
        print(f"[2] jetons distinctifs du bloc {bloc} presents dans la persona "
              f"({len(part)}) : {', '.join(part[:40])}", flush=True)

    # --- section 3 : les comparateurs servis --------------------------------
    rng = np.random.default_rng([GRAINE, 7])
    persona_tout, _ = matrice_v13(ids, col_p)
    persona_conso, _ = matrice_v13(ids, cols_conso)
    aux_items, _ = matrice_v13(ids, col_4)      # entree du temoin positif T+
    print(f"[3] entrees : persona complete {persona_tout.shape}, "
          f"persona consommation {persona_conso.shape}, "
          f"auxiliaire items attaques (T+) {aux_items.shape} ({time.time()-t0:.0f} s)",
          flush=True)

    gens = {}
    print("[3] S1 servi sur un plateau (persona consommation)...", flush=True)
    lois_s1 = lois_conditionnelles(persona_conso, pool, "S1")
    gens["S1 servi : persona consommation (argmax)"] = argmax_lois(lois_s1)
    print(f"[3] S2 selection par item, {K_SELECTION} colonnes hors pli... "
          f"({time.time()-t0:.0f} s)", flush=True)
    lois_s2 = lois_conditionnelles(persona_tout, pool, "S2", k_selection=K_SELECTION)
    gens[f"S2 selection par item ({K_SELECTION} col. hors pli, argmax)"] = argmax_lois(lois_s2)
    gens[f"S2s selection par item ({K_SELECTION} col. hors pli, tirage)"] = tirage_lois(
        lois_s2, rng)
    print(f"[3] T+ temoin positif (reponses v1-3 aux items attaques)... "
          f"({time.time()-t0:.0f} s)", flush=True)
    lois_tp = lois_conditionnelles(aux_items, pool, "T+", k_selection=K_SELECTION)
    gens["T+ temoin positif : v1-3 aux items attaques (argmax)"] = argmax_lois(lois_tp)

    refs = {
        f"LLM {LLM_REF} (persona individuelle)": codes[LLM_REF][:, items],
        f"LLM {DEMO} (segment seul)": codes[DEMO][:, items],
        "Retest humain v1-3 aux items attaques": v13,
    }
    # S3 : le niveau seul. On permute, chez chaque personne, les reponses du jumeau sur le
    # bloc d'achat : le nombre de « oui » est conserve, le motif detruit.
    rng_perm = np.random.default_rng([GRAINE, 11])
    gens["S3 jumeau, motif detruit / niveau conserve"] = permuter_intra_personne(
        codes[LLM_REF][:, items], np.flatnonzero(est_achat), rng_perm)

    blocs = (("tous", None), ("items d'achat", np.flatnonzero(est_achat)),
             ("items d'heuristiques", np.flatnonzero(~est_achat)))
    resultats = {}
    for etiquette, masque in blocs:
        for nom, g in list(gens.items()) + list(refs.items()):
            r = mesurer(f"{nom} | {etiquette}", g, pool, items_locaux=masque)
            r["condition"] = nom
            r["bloc_items"] = etiquette
            lignes.append(r)
            resultats[(nom, etiquette)] = r
        print(f"[3] bloc « {etiquette} » mesure ({time.time()-t0:.0f} s)", flush=True)
        for nom, _ in list(gens.items()) + list(refs.items()):
            r = resultats[(nom, etiquette)]
            print(f"    {nom:<52} exact={r['exactitude']:.3f} "
                  f"top1={r['top1']:.4f} [{r['top1_bas']:.4f};{r['top1_haut']:.4f}]",
                  flush=True)

    # --- section 4 : stabilite test-retest ----------------------------------
    st = stabilite_par_item(v13, pool, noms_att, est_achat)
    for bloc, g in st.groupby("bloc"):
        lignes.append({"mesure": "stabilite_retest", "condition": bloc,
                       "n_items": int(len(g)),
                       "accord_retest": float(g.accord_retest.mean()),
                       "accord_hasard": float(g.accord_hasard.mean()),
                       "kappa_retest": float(g.kappa_retest.mean()),
                       "n_modalites": float(g.n_modalites.mean()),
                       "entropie_bits": float(g.entropie_bits.mean()),
                       "taux_modal": float(g.taux_modal.mean())})
        print(f"[4] bloc {bloc:<13} {len(g):>3} items, {g.n_modalites.mean():.1f} modalites, "
              f"{g.entropie_bits.mean():.2f} bits, accord retest {g.accord_retest.mean():.3f}, "
              f"kappa {g.kappa_retest.mean():.3f}", flush=True)

    taux_modal = st.taux_modal.to_numpy()
    for nom, g in list(gens.items()) + list(refs.items()):
        gn = gain_normalise(g, pool, taux_modal)
        for bloc, masque in (("achat", est_achat), ("heuristiques", ~est_achat)):
            lignes.append({"mesure": "gain_normalise", "condition": nom,
                           "bloc_items": bloc, "n_items": int(masque.sum()),
                           "gain_normalise": float(np.mean(gn[masque]))})
        print(f"[4] gain normalise {nom:<52} achat {np.mean(gn[est_achat]):+.4f} | "
              f"heuristiques {np.mean(gn[~est_achat]):+.4f}", flush=True)

    # fraction du plafond de retest recuperee par le jumeau, bloc par bloc
    for bloc in ("items d'achat", "items d'heuristiques"):
        plafond = resultats[("Retest humain v1-3 aux items attaques", bloc)]["top1"]
        jumeau = resultats[(f"LLM {LLM_REF} (persona individuelle)", bloc)]["top1"]
        frac = jumeau / plafond if plafond > 0 else np.nan
        lignes.append({"mesure": "fraction_plafond", "condition": bloc,
                       "top1": jumeau, "plafond_retest": plafond, "fraction": frac})
        print(f"[4] fraction du plafond de retest recuperee, {bloc} : "
              f"{jumeau:.4f} / {plafond:.4f} = {frac:.4f}", flush=True)

    # --- controle de fidelite, avant toute interpretation --------------------
    idx = np.arange(n)
    for nom, g in gens.items():
        try:
            d = controle_avant_interpretation(idx, items, g, nom, paq=paq)
            statut, detail = "passe", json.dumps(
                {k: (round(v, 6) if isinstance(v, float) else v)
                 for k, v in d.items() if isinstance(v, (int, float, str, bool))})
        except EchecControleInterpretabilite as e:
            statut, detail = "echoue", str(e)[:300]
        lignes.append({"mesure": "controle_interpretabilite", "condition": nom,
                       "controle_statut": statut, "controle_detail": detail})
        print(f"[5] controle {nom} : {statut}", flush=True)

    T1.ecrire(pd.DataFrame(lignes), "c7-audit-contamination.csv")

    # --- verdict preenregistre ----------------------------------------------
    print("\n===== VERDICT PREENREGISTRE =====", flush=True)
    m_achat = df_desc[(df_desc.bloc == "achat") & (df_desc.marque_phrase_personas >= 0)]
    # Critere (i) : un item d'achat compte comme « du meme objet » si la persona nomme sa
    # MARQUE, sa CATEGORIE ou son PRODUIT comme phrase entiere. Le comptage par jeton isole
    # est un artefact (mots courants du libelle des questions de persona) et n'est pas
    # retenu comme critere ; il reste imprime ci-dessus pour etre verifiable.
    n_marques = int(((m_achat.marque_phrase_personas > 0)
                     | (m_achat.categorie_phrase_personas > 0)
                     | (m_achat.produit_phrase_personas > 0)).sum()) if len(m_achat) else 0
    meilleur = max((resultats[(k, "items d'achat")] for k in gens
                    if k.startswith(("S1", "S2"))), key=lambda r: r["top1"])
    print(f"E1 critere (i) items d'achat dont la persona nomme marque, categorie ou "
          f"produit : {n_marques} (confirme si >= 5)", flush=True)
    print(f"E1 critere (ii) meilleur comparateur servi, bloc achat : "
          f"{meilleur['condition']} top1={meilleur['top1']:.4f} "
          f"[{meilleur['top1_bas']:.4f};{meilleur['top1_haut']:.4f}] "
          f"(confirme si borne basse >= 0,05)", flush=True)
    e1 = (n_marques >= 5) or (meilleur["top1_bas"] >= 0.05)
    tp = resultats[("T+ temoin positif : v1-3 aux items attaques (argmax)", "items d'achat")]
    print(f"P5 temoin positif, bloc achat : top1={tp['top1']:.4f} (P5 tenue si > 0,50)",
          flush=True)
    ka = st[st.bloc == "achat"].kappa_retest.mean()
    kh = st[st.bloc == "heuristiques"].kappa_retest.mean()
    print(f"P6 kappa retest achat {ka:.3f} contre heuristiques {kh:.3f} ; "
          f"rapport {ka / max(kh, 1e-9):.2f} (P6 tenue si >= 2)", flush=True)
    fa = [l for l in lignes if l.get("mesure") == "fraction_plafond"]
    f_ach = next(l["fraction"] for l in fa if l["condition"] == "items d'achat")
    f_heu = next(l["fraction"] for l in fa if l["condition"] == "items d'heuristiques")
    rap = f_ach / max(f_heu, 1e-12)
    print(f"P7 fraction du plafond recuperee : achat {f_ach:.4f}, heuristiques {f_heu:.4f}, "
          f"rapport {rap:.1f} (E2 explique TOUT si < 2 ; E2 insuffisante si >= 5)",
          flush=True)
    print(f"\nE1 (contamination) : {'CONFIRMEE' if e1 else 'REFUTEE'}", flush=True)
    if not e1:
        print("E2 (prevoyabilite differentielle) : "
              + ("l'emporte SEULE" if rap < 2 else
                 "explique une partie, PAS la totalite" if rap >= 5 else
                 "zone intermediaire, a discuter"), flush=True)
    if tp["top1"] <= 0.50:
        print("!! P5 ECHOUE : l'appareil ne retrouve pas le signal quand il est present, "
              "aucune conclusion negative n'est publiable depuis ce fichier.", flush=True)
    print(f"\ntermine en {time.time()-t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
