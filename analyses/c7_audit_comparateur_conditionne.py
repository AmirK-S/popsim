"""
c7_audit_comparateur_conditionne : les generateurs classiques ont-ils ete compares au
jumeau LLM a information d'entree egale ?

===========================================================================
PREENREGISTREMENT : resultats/audit-comparateur-conditionne-2026-09-13.md, section 0,
ecrite et COMMITEE avant ce fichier et avant tout calcul de comparateur (commit c87cebd).
Predictions P2-P5 et critere de refutation de l'audit lui-meme y sont fixes.

CE QUI EST ATTAQUE. Sur la branche agent/mesures/controle-generateur, un agent etablit
qu'aucun generateur synthetique classique ne depasse 0,15 % de reidentification sur Twin,
contre 20,7 % pour le jumeau LLM, et conclut que « ce que nous mesurons n'est pas la fuite
generique des donnees synthetiques ». Objection : ses quatre generateurs G0-G3 ne sont
conditionnes que sur le SEGMENT DEMOGRAPHIQUE, alors que le jumeau LLM est construit a
partir des reponses passees de la personne elle meme. Si c'est exact, la comparaison oppose
un generateur qui a vu l'individu a des generateurs qui ne l'ont jamais vu.

LE FAIT, ETABLI EN SECTION 1 AVANT TOUT COMPARATEUR. Le catalogue de Twin-2K-500 partitionne
ses 256 QuestionID en deux sources DISJOINTES : wave1_3_persona_json (171 QuestionID,
634 colonnes CSV), sur laquelle le jumeau est conditionne, et wave4_Q_wave1_3_A
(85 QuestionID, 126 colonnes CSV), d'ou sortent les 60 items attaques. Le conditionnement
individuel est donc CONFIRME -- l'objection a raison sur sa premisse -- mais il est
DISJOINT des items attaques : le jumeau n'a jamais vu les reponses qu'on lui reproche de
laisser fuir. Les deux faits sont vrais en meme temps et ce script mesure ce qu'il en reste.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / ecrire                   les quinze tables de Twin, l'ecriture CSV
  c7_reidentification.items_communs            les 60 items toujours renseignes
  c7_reidentification.rangs_attaque            L'ATTAQUE, inchangee, garde-fous compris
  c7_reidentification.graine_nom / REF_V4 / REF_V13 / DEMO
  a2_commun.distance_hamming                   la distance de Hamming normalisee, masquee
  a2_commun.bootstrap_personnes                l'IC a 95 % par reechantillonnage de personnes
  c7_controle_interpretabilite.controle_avant_interpretation   le controle de fidelite

CE QUI EST NOUVEAU ICI, et rien d'autre :
  persona_individuelle   la matrice des 634 colonnes vagues 1-3 HORS items repetes, codee
                         categoriellement. C'est, colonne pour colonne, l'entree du jumeau.
  K1 / K10               donneur au plus proche voisin sur la persona (1 et 10 voisins),
                         la personne elle meme toujours exclue du don.
  K2a / K2s              modele conditionnel par item ajuste sur la persona, HORS PLI,
                         en argmax puis en tirage dans la loi predite.
  la lecture par bloc d'items (40 items d'achat contre 20 autres) et le recadrage du
  « plafond » : les 81,6 % de l'attaquant « reponses passees » utilisent les reponses
  v1-3 AUX ITEMS ATTAQUES, qui sont hors persona -- ce n'est pas le plafond de l'entree
  du jumeau mais celui d'un auxiliaire different.

ETHIQUE : etude de risque de vie privee sur un jeu deja public (Twin-2K-500). Ce script ne
calcule, n'imprime et n'ecrit JAMAIS un pid, une identite, une reponse ni un appariement
individuel : seuls des taux agreges sortent dans resultats/. Aucun appel de modele de
langage, aucun reseau, aucune depense, aucun arriere-plan. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_audit_comparateur_conditionne.py
===========================================================================
"""

import json
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                    # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes               # noqa: E402
from c7_reidentification import (                                         # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13, DEMO,
)
from c7_controle_interpretabilite import (                                # noqa: E402
    controle_avant_interpretation, EchecControleInterpretabilite,
)

GRAINE = 20260913
N_TIRAGES_LIENS = 20      # ex aequo, comme c7_reidentification
N_BOOTSTRAP = 2000
N_PLIS = 5                # plis hors echantillon du modele conditionnel
N_COMPOSANTES = 60        # composantes de la persona one-hot pour K2 (reduction declaree)
K_VOISINS = 10            # voisins de K10
MAX_MODALITES = 8         # binning des colonnes numeriques de la persona

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RACINE_TWIN = os.path.join(RACINE, "data", "twin2k500")
CATALOGUE = os.path.join(RACINE_TWIN, "question_catalog_and_human_response_csv",
                         "question_catalog.json")
REPONSES_V13 = os.path.join(RACINE_TWIN, "question_catalog_and_human_response_csv",
                            "wave1_3_response.csv")
MAPPING_V4 = os.path.join(RACINE_TWIN, "llm", "wave4_formatted_to_catalog_mapping.json")

SOURCE_PERSONA = "wave1_3_persona_json"    # ce sur quoi le jumeau est conditionne
SOURCE_V4 = "wave4_Q_wave1_3_A"            # d'ou sortent les items attaques

LLM_REF = "JSON Persona - GPT4.1"          # le jumeau des chiffres publies


# ---------------------------------------------------------------------------
# 1. LE FAIT : de quoi le jumeau est il construit ?
# ---------------------------------------------------------------------------

def partition_catalogue():
    """La partition des 256 QuestionID du catalogue en persona / items de vague 4.

    Le catalogue publie par l'equipe Twin porte, pour chaque QuestionID, un champ `source`
    qui dit de quel objet du depot la question provient, et un champ `csv_columns` qui donne
    les colonnes correspondantes de wave1_3_response.csv / wave4_response.csv. C'est LA
    PIECE : elle etablit, sans supposition, ce qui entre dans la persona et ce qui n'y entre
    pas. Renvoie (colonnes_persona, colonnes_v4, compte_qid_persona, compte_qid_v4).
    """
    cat = json.load(open(CATALOGUE))
    col_p, col_4, n_p, n_4 = [], [], 0, 0
    for e in cat:
        cols = e.get("csv_columns") or []
        if e["source"] == SOURCE_PERSONA:
            col_p.extend(cols)
            n_p += 1
        elif e["source"] == SOURCE_V4:
            col_4.extend(cols)
            n_4 += 1
    return col_p, col_4, n_p, n_4


def verifier_disjonction(noms_items, items_attaques):
    """Les 60 items attaques viennent ils tous de la source de vague 4, jamais de la persona ?

    Les tables de t1_commun portent les noms « formates » de responses_wave4_formatted.csv ;
    le mapping publie par l'equipe Twin les ramene aux QuestionID du catalogue. On verifie
    que les 60 items attaques ont TOUS pour source wave4_Q_wave1_3_A, c'est a dire qu'AUCUN
    n'est dans la persona. Renvoie un dict de diagnostic.
    """
    mapping = {x["formatted_column"]: x["QuestionID"] for x in json.load(open(MAPPING_V4))}
    cat = json.load(open(CATALOGUE))
    source_de = {e["QuestionID"]: e["source"] for e in cat}
    attaques = [noms_items[i] for i in items_attaques]
    srcs = [source_de.get(mapping.get(c, ""), "INCONNU") for c in attaques]
    return {
        "n_items_attaques": len(attaques),
        "retrouves_dans_mapping": sum(1 for c in attaques if c in mapping),
        "de_source_vague4": sum(1 for s in srcs if s == SOURCE_V4),
        "de_source_persona": sum(1 for s in srcs if s == SOURCE_PERSONA),
    }


def coder_colonne(serie):
    """Une colonne brute de wave1_3_response.csv en codes entiers, -1 pour manquant.

    Les colonnes textuelles sont factorisees. Les colonnes numeriques a plus de
    MAX_MODALITES valeurs distinctes sont decoupees en MAX_MODALITES quantiles : c'est la
    seule facon de les faire entrer dans une distance de Hamming, et la perte est declaree
    (une reponse continue devient un rang grossier). Ce codage est applique a la persona
    seulement -- jamais aux items attaques, qui gardent le codage de t1_commun.
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
    out = np.where(np.isnan(codes), -1, codes).astype(np.int32)
    return out


def persona_individuelle(ids, colonnes_persona):
    """La matrice (n_personnes, n_colonnes_persona) de l'entree individuelle du jumeau.

    Alignee ligne a ligne sur `ids`, l'ordre des personnes de t1_commun.charger(), pour que
    la ligne i de la persona et la ligne i des items attaques soient la MEME personne.
    Aucune valeur n'est imprimee : seules des formes et des taux de remplissage le sont.
    """
    brut = pd.read_csv(REPONSES_V13, low_memory=False)
    brut = brut.set_index("pid")
    gardees = [c for c in colonnes_persona if c in brut.columns]
    brut = brut.reindex(index=pd.Index(ids, name="pid"))[gardees]
    mat = np.column_stack([coder_colonne(brut[c]) for c in gardees]).astype(np.int32)
    # on jette les colonnes constantes ou vides : elles ne portent aucune information et
    # diluent la distance de Hamming sans rien y ajouter.
    utile = np.array([len(np.unique(mat[:, j][mat[:, j] >= 0])) > 1
                      for j in range(mat.shape[1])])
    return mat[:, utile], [c for c, u in zip(gardees, utile) if u]


# ---------------------------------------------------------------------------
# 2. Les generateurs classiques conditionnes sur LA MEME entree individuelle
# ---------------------------------------------------------------------------

def voisins_persona(persona):
    """L'ordre des voisins de chaque personne dans l'espace de la persona, elle exclue.

    distance_hamming de a2_commun est appelee telle quelle : elle gere deja le masquage des
    cellules non renseignees (-1). La diagonale est mise a l'infini, ce qui EXCLUT la
    personne d'elle meme du don -- sans quoi K1 recopierait la personne et mesurerait la
    memorisation parfaite au lieu d'un generateur.
    """
    d = distance_hamming(persona, persona)
    np.fill_diagonal(d, np.inf)
    return np.argsort(d, axis=1, kind="stable"), d


def generer_K1(y, ordre):
    """Le vecteur vague 4 ENTIER du plus proche voisin dans l'espace de la persona.

    C'est le comparateur le plus direct de l'objection : un generateur sans aucune IA, qui
    a vu exactement la meme information individuelle que le jumeau, et qui s'en sert de la
    facon la plus agressive possible -- en donnant le dossier complet du sosie.
    """
    return y[ordre[:, 0], :]


def generer_K10(y, ordre, k=K_VOISINS):
    """Vote modal par item des k plus proches voisins sur la persona.

    Plus lisse que K1, et generalement plus exact : c'est la version « bien faite » du
    donneur, celle qu'un praticien construirait.
    """
    n, p = y.shape
    out = np.zeros((n, p), dtype=y.dtype)
    vois = ordre[:, :k]
    for j in range(p):
        bloc = y[vois, j]                                   # (n, k)
        m = bloc.max() + 1
        compte = np.zeros((n, m), dtype=np.int32)
        for c in range(k):
            compte[np.arange(n), bloc[:, c]] += 1
        out[:, j] = compte.argmax(axis=1)
    return out


def lois_conditionnelles(persona, y, rng):
    """Pour chaque item attaque, la loi predite HORS PLI a partir de la seule persona.

    Regression logistique multinomiale sur les N_COMPOSANTES premieres composantes de la
    persona mise en indicatrices (reduction declaree : la persona brute fait plusieurs
    milliers d'indicatrices pour 2 058 personnes, un modele par item y surajusterait sans
    rien predire hors pli). Cinq plis : la loi predite pour une personne n'est JAMAIS
    ajustee sur elle meme. Renvoie la liste, item par item, des lois (n, k_item).
    """
    from sklearn.decomposition import TruncatedSVD
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, KFold
    from sklearn.preprocessing import OneHotEncoder

    enc = OneHotEncoder(handle_unknown="ignore", min_frequency=10)
    X = enc.fit_transform(persona.astype(str))
    svd = TruncatedSVD(n_components=min(N_COMPOSANTES, X.shape[1] - 1),
                       random_state=GRAINE)
    Z = svd.fit_transform(X)
    Z = (Z - Z.mean(axis=0)) / (Z.std(axis=0) + 1e-9)

    n, p = y.shape
    lois = []
    for j in range(p):
        cible = y[:, j]
        k = int(cible.max()) + 1
        proba = np.full((n, k), 1.0 / k)
        classes_utiles = np.unique(cible)
        if len(classes_utiles) < 2:
            lois.append(proba)
            continue
        compte = np.bincount(cible, minlength=k)
        # StratifiedKFold exige au moins N_PLIS exemplaires de chaque classe presente.
        strat = compte[classes_utiles].min() >= N_PLIS
        decoupe = (StratifiedKFold(N_PLIS, shuffle=True, random_state=GRAINE) if strat
                   else KFold(N_PLIS, shuffle=True, random_state=GRAINE))
        for tr, te in decoupe.split(Z, cible if strat else None):
            mod = LogisticRegression(max_iter=400, C=1.0)
            try:
                mod.fit(Z[tr], cible[tr])
            except ValueError:
                continue
            proba[te] = 0.0
            proba[np.ix_(te, mod.classes_)] = mod.predict_proba(Z[te])
        lignes = proba.sum(axis=1)
        vides = lignes <= 0
        proba[vides] = 1.0 / k
        proba = proba / proba.sum(axis=1, keepdims=True)
        lois.append(proba)
    return lois


def generer_K2a(lois):
    """Argmax de la loi conditionnelle : le predicteur, pas encore un generateur."""
    return np.column_stack([l.argmax(axis=1) for l in lois]).astype(np.int32)


def generer_K2s(lois, rng):
    """Tirage dans la loi conditionnelle : le vrai generateur synthetique conditionne.

    C'est la forme qui se compare le plus honnetement au jumeau LLM, lequel echantillonne
    lui aussi une reponse au lieu de rendre un argmax.
    """
    n = lois[0].shape[0]
    out = np.zeros((n, len(lois)), dtype=np.int32)
    for j, l in enumerate(lois):
        cum = np.cumsum(l, axis=1)
        u = rng.random((n, 1))
        out[:, j] = (u > cum).sum(axis=1).clip(0, l.shape[1] - 1)
    return out


# ---------------------------------------------------------------------------
# 3. Mesure : bassin strictement constant, attaque importee
# ---------------------------------------------------------------------------

def mesurer(nom, gen, pool, items_locaux=None):
    """Le top-1 / top-10 du generateur `gen` contre `pool`, bassin entier, IC bootstrap.

    items_locaux restreint la mesure a un sous ensemble de COLONNES (lecture par bloc
    d'items) ; le BASSIN DE PERSONNES, lui, ne bouge jamais : 2 058 attaques contre
    2 058 candidats, quel que soit le bloc. C'est le garde fou qui a deja coute deux
    erreurs a ce projet.
    """
    g = gen if items_locaux is None else gen[:, items_locaux]
    p = pool if items_locaux is None else pool[:, items_locaux]
    n = g.shape[0]
    rng = np.random.default_rng([GRAINE, graine_nom(nom)])
    rang, top1, top10 = rangs_attaque(g, p, np.arange(n), rng, n_tirages=N_TIRAGES_LIENS)
    m1, b1, h1 = bootstrap_personnes(top1, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 1])
    m10, b10, h10 = bootstrap_personnes(top10, n_tirages=N_BOOTSTRAP, graine=[GRAINE, 2])
    exact = float(np.mean(g == p[np.arange(n)]))
    return {"generateur": nom, "n_attaques": n, "n_pool": p.shape[0],
            "n_items": g.shape[1], "exactitude": exact,
            "top1": m1, "top1_bas": b1, "top1_haut": h1,
            "top10": m10, "top10_bas": b10, "top10_haut": h10,
            "rang_median": float(np.median(rang)),
            "top1_hasard": 1.0 / p.shape[0]}


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t0 = time.time()

    # --- section 1 : le fait ------------------------------------------------
    col_p, col_4, n_qid_p, n_qid_4 = partition_catalogue()
    print(f"[1] catalogue : {n_qid_p} QuestionID de source {SOURCE_PERSONA} "
          f"({len(col_p)} colonnes CSV) ; {n_qid_4} QuestionID de source {SOURCE_V4} "
          f"({len(col_4)} colonnes CSV) ; intersection des colonnes = "
          f"{len(set(col_p) & set(col_4))}", flush=True)

    paq = T1.charger()
    codes, ids, noms_items = paq["codes"], paq["ids"], list(paq["colonnes"])
    items = items_communs(codes, [REF_V4, REF_V13])
    diag = verifier_disjonction(noms_items, items)
    print(f"[1] items attaques : {diag}", flush=True)

    persona, cols_gardees = persona_individuelle(ids, col_p)
    remplissage = float((persona >= 0).mean())
    print(f"[1] persona individuelle : {persona.shape[0]} personnes x "
          f"{persona.shape[1]} colonnes informatives (sur {len(col_p)} du catalogue), "
          f"remplissage {remplissage:.3f}", flush=True)

    pool = codes[REF_V4][:, items]
    y = pool.copy()
    n = pool.shape[0]

    # bloc d'items : achat contre le reste (lecture de robustesse, bassin inchange)
    # Les 40 items d'achat de Twin sont les colonnes `<rang>_Q295` (QID295, bloc
    # « Product Preferences - Pricing » du catalogue) : « acheteriez vous ce produit a ce
    # prix ? ». Les 20 autres sont les experiences d'heuristiques et biais. Le decoupage
    # est fait sur le suffixe de colonne, pas sur un libelle, pour qu'il soit verifiable.
    est_achat = np.array([c.endswith("_Q295")
                          for c in [noms_items[i] for i in items]])
    print(f"[1] items d'achat detectes par nom : {int(est_achat.sum())} / {len(items)}",
          flush=True)

    # --- section 2 : les comparateurs equitables ----------------------------
    rng = np.random.default_rng([GRAINE, 7])
    print(f"[2] voisins sur la persona... ({time.time()-t0:.0f} s)", flush=True)
    ordre, _d = voisins_persona(persona)
    gens = {
        "K1 plus proche voisin persona": generer_K1(y, ordre),
        f"K{K_VOISINS} vote modal voisins persona": generer_K10(y, ordre),
    }
    print(f"[2] modele conditionnel hors pli... ({time.time()-t0:.0f} s)", flush=True)
    lois = lois_conditionnelles(persona, y, rng)
    gens["K2a modele conditionnel persona (argmax)"] = generer_K2a(lois)
    gens["K2s modele conditionnel persona (tirage)"] = generer_K2s(lois, rng)

    # les references, MEME bassin, MEMES items, MEME attaque
    refs = {
        f"LLM {LLM_REF} (persona individuelle)": codes[LLM_REF][:, items],
        f"LLM {DEMO} (segment seul)": codes[DEMO][:, items],
        "Retest humain v1-3 aux items attaques (hors persona)": codes[REF_V13][:, items],
    }

    lignes = []
    for nom, g in list(gens.items()) + list(refs.items()):
        r = mesurer(nom, g, pool)
        r["bloc_items"] = "tous"
        r["conditionnement"] = ("persona individuelle" if nom.startswith(("K1", "K10", "K2"))
                                else "reference")
        lignes.append(r)
        print(f"  {nom:<52} exact={r['exactitude']:.3f} "
              f"top1={r['top1']:.4f} [{r['top1_bas']:.4f};{r['top1_haut']:.4f}] "
              f"top10={r['top10']:.4f}", flush=True)

    # --- section 3 : lecture par bloc d'items, bassin de personnes inchange --
    if est_achat.any() and (~est_achat).any():
        for etiquette, masque in (("items d'achat", np.flatnonzero(est_achat)),
                                  ("items hors achat", np.flatnonzero(~est_achat))):
            for nom, g in list(gens.items()) + list(refs.items()):
                r = mesurer(nom + " | " + etiquette, g, pool, items_locaux=masque)
                r["generateur"] = nom
                r["bloc_items"] = etiquette
                r["conditionnement"] = ("persona individuelle"
                                        if nom.startswith(("K1", "K10", "K2"))
                                        else "reference")
                lignes.append(r)
            print(f"[3] bloc « {etiquette} » ({len(masque)} items) mesure", flush=True)

    # --- section 4 : le controle de fidelite, avant toute interpretation -----
    idx = np.arange(n)
    for nom, g in gens.items():
        try:
            d = controle_avant_interpretation(idx, items, g, nom, paq=paq)
            statut, detail = "passe", json.dumps(
                {k: (round(v, 6) if isinstance(v, float) else v)
                 for k, v in d.items() if isinstance(v, (int, float, str, bool))})
        except EchecControleInterpretabilite as e:
            statut, detail = "echoue", str(e)[:300]
        lignes.append({"generateur": nom, "bloc_items": "controle_interpretabilite",
                       "conditionnement": "persona individuelle",
                       "controle_statut": statut, "controle_detail": detail})
        print(f"[4] controle {nom} : {statut}", flush=True)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-audit-comparateur-conditionne.csv")

    # --- verdict preenregistre ---------------------------------------------
    tous = df[(df.bloc_items == "tous")]
    eq = tous[tous.conditionnement == "persona individuelle"]
    llm = tous[tous.generateur.str.startswith(f"LLM {LLM_REF}")]
    if len(eq) and len(llm):
        best = eq.loc[eq.top1.idxmax()]
        l = llm.iloc[0]
        print(f"\nmeilleur comparateur equitable : {best.generateur}, "
              f"top1={best.top1:.4f} [{best.top1_bas:.4f};{best.top1_haut:.4f}]", flush=True)
        print(f"jumeau LLM : top1={l.top1:.4f} [{l.top1_bas:.4f};{l.top1_haut:.4f}]",
              flush=True)
        if best.top1_bas >= l.top1_haut:
            issue = "(c) le jumeau fuit MOINS que le comparateur equitable"
        elif best.top1_bas >= 0.05:
            issue = "(b) fuite comparable : P3 REFUTEE, enonce a affaiblir"
        else:
            issue = "(a) la specificite LLM tient : P3 tenue"
        print(f"ISSUE : {issue}", flush=True)
        print(f"rapport LLM / meilleur equitable = "
              f"{l.top1 / max(best.top1, 1e-12):.1f}x "
              f"(publie contre G0-G3 de segment : {l.top1 / 0.0015354713313896:.0f}x)",
              flush=True)
    print(f"\ntermine en {time.time()-t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
