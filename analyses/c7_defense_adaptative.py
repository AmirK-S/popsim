"""
c7_defense_adaptative : existe-t-il une defense qui resiste a l'attaquant ADAPTATIF,
a un cout d'utilite acceptable ?

===========================================================================
PREENREGISTREMENT : resultats/c7-defense-adaptative-preenregistrement.md, ecrit et
COMMIS avant ce fichier et avant tout calcul de defense. Il fixe les sept familles de
candidats, l'attaquant adaptatif dedie de chacune, les criteres de protection et
d'utilite, les six predictions Q1-Q6, et le seuil du §6.4 en dessous duquel la
conclusion publiee est « nous n'avons pas trouve de remede ».

MOTIF. La nuit du 12 au 13 septembre a etabli que D4 s'effondre :
`resultats/audit-comparaison-dp-2026-09-13.md` (F1 : le multiensemble intra-segment est
republie a l'identique, 1 560 couples sur 1 560 ; F5 : le bloc de 20 items d'opinion
n'est pas touche) et `resultats/retractation-dp-d4-2026-09-13.md` (taux de tete sous
attaquant adaptatif 0,29 % [0,10 ; 0,53], et non 0,05 %). L'article mesure donc un
risque et laisse le praticien sans recours. Ce script cherche le recours, ou etablit
qu'il n'y en a pas parmi les candidats testes.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger / ecrire                     les tables Twin-2K-500, l'ecriture CSV
  a2_commun.bootstrap_personnes                  l'IC par reechantillonnage de personnes
  c7_reidentification.items_communs/rangs_attaque/graine_nom/REF_V4/REF_V13
                                                 l'attaque naive et ses garde-fous
  c7_mecanisme.items_achat                       les 40 indices du bloc d'achat
  c7_defense.defense_d4                          D4 telle qu'elle est publiee (reference)
  c7_defense.erreur_distribution/erreur_groupes/erreur_correlations
                                                 les trois composantes d'utilite, memes
                                                 definitions que c7-defense-courbe.csv
  c7_utilite_aval.analyse_a/analyse_b/analyse_c/signe_charges
                                                 les trois taches en aval, inchangees
  c7_attaquant_fort.scores_hors_pli/parametres/score_invariant/mesurer/plis
                                                 l'attaquant A-LLR hors pli et
                                                 l'invariant de segment S3
  c7_dp_zcdp.rho_depuis_eps_delta/sigma_gaussien/marginales_bruitees_gauss/echantillonner
                                                 la comptabilite zCDP et le generateur DP
  c7_controle_interpretabilite.controle_avant_interpretation
                                                 le controle de fidelite prealable

CE QUI EST NOUVEAU ICI, et rien d'autre :
  (1) les six familles de candidats E1 a E5 (permutation etendue, permutation JOINTE par
      blocs correles, agregation intra-segment par le mode et par representant tire,
      degradation partielle de fidelite, generateur DP a marginales CONDITIONNEES AU
      SEGMENT) ;
  (2) la strategie d'attaque C, « lien par le contenu » : une permutation ne cache que
      l'INDICE, jamais le CONTENU. C'est elle qui decide de la piste « reparer D4 par une
      permutation jointe » ;
  (3) l'assemblage protection x cout x nature de la garantie en une seule table.

ETHIQUE : aucun pid, aucun appariement individuel, aucune reponse individuelle n'est
imprime ni ecrit ; uniquement des taux agreges, des couts en points et des reglages de
mecanisme. Aucun appel de modele de langage, aucun reseau. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_defense_adaptative.py
===========================================================================
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                              # noqa: E402
from a2_commun import bootstrap_personnes                            # noqa: E402
from c7_reidentification import (                                    # noqa: E402
    items_communs, rangs_attaque, graine_nom, REF_V4, REF_V13,
)
from c7_mecanisme import items_achat                                 # noqa: E402
from c7_defense import (                                             # noqa: E402
    defense_d4, erreur_distribution, erreur_groupes, erreur_correlations,
)
from c7_utilite_aval import (                                        # noqa: E402
    analyse_a, analyse_b, analyse_c, signe_charges,
)
import c7_attaquant_fort as AF                                       # noqa: E402
import c7_dp_zcdp as DP                                              # noqa: E402
from c7_controle_interpretabilite import (                           # noqa: E402
    controle_avant_interpretation, EchecControleInterpretabilite,
)

GRAINE = 20260913
N_BOOTSTRAP = 2000
CIBLE = "JSON Persona - GPT4.1"
EPSILONS = [1.0, 3.0, 10.0, np.inf]
N_REPLICATS_DP_RISQUE = 2      # reduction declaree, preenregistrement §8
N_REPLICATS_DP_UTILITE = 5     # reduction declaree, preenregistrement §8
SEUIL_P1PCT = 0.01             # critere secondaire, preenregistrement §6.1


# ===========================================================================
# 1. LES MECANISMES DE DEFENSE
# ===========================================================================

def blocs_correles(x, n_blocs):
    """Partition des colonnes de x en n_blocs blocs d'items CORRELES.

    Agglomeration gloutonne : chaque item part seul, on fusionne a chaque tour les deux
    groupes dont la |correlation| moyenne inter-groupes est la plus forte, jusqu'a
    n_blocs groupes. Deterministe (aucun tirage) : la partition est une fonction du
    jumeau non protege, donc identique pour tous les reglages.
    """
    n_items = x.shape[1]
    if n_blocs >= n_items:
        return [np.array([j]) for j in range(n_items)]
    c = np.abs(pd.DataFrame(np.where(x >= 0, x, np.nan).astype(float)).corr().values)
    np.fill_diagonal(c, 0.0)
    c = np.nan_to_num(c)
    groupes = [[j] for j in range(n_items)]
    while len(groupes) > n_blocs:
        meilleur, ia, ib = -1.0, 0, 1
        for a in range(len(groupes)):
            for b in range(a + 1, len(groupes)):
                v = float(c[np.ix_(groupes[a], groupes[b])].mean())
                if v > meilleur:
                    meilleur, ia, ib = v, a, b
        groupes[ia] = groupes[ia] + groupes[ib]
        del groupes[ib]
    return [np.array(sorted(g)) for g in groupes]


def perm_jointe(x, seg, blocs, etiquette):
    """E2 : permutation JOINTE, bloc par bloc, a l'interieur de chaque segment.

    Les colonnes d'un meme bloc subissent LA MEME permutation de personnes : la
    structure de correlation intra-bloc est preservee exactement. Un bloc unique
    contenant tous les items revient a permuter les LIGNES ENTIERES.
    """
    rng = np.random.default_rng([GRAINE, 501, graine_nom(etiquette)])
    xd = x.copy()
    for g in np.unique(seg):
        if g < 0:
            continue
        membres = np.flatnonzero(seg == g)
        if len(membres) < 2:
            continue
        for bloc in blocs:
            ordre = rng.permutation(membres)
            xd[np.ix_(membres, bloc)] = x[np.ix_(ordre, bloc)]
    return xd


def perm_item_partielle(x, seg, lam, etiquette):
    """E1 / E4 : permutation intra-segment ITEM PAR ITEM d'une fraction lam des cellules.

    lam = 1 : tous les items de tous les membres sont permutes (E1, D4 etendue aux
    60 items). lam < 1 : dans chaque segment et pour chaque item, une fraction lam des
    membres est tiree et ses valeurs sont permutees ENTRE ELLES ; le reste ne bouge pas.
    Le multiensemble intra-segment est conserve a l'identique pour tout lam -- c'est
    justement ce que la strategie S3 exploite.
    """
    rng = np.random.default_rng([GRAINE, 502, graine_nom(etiquette)])
    xd = x.copy()
    for g in np.unique(seg):
        if g < 0:
            continue
        membres = np.flatnonzero(seg == g)
        if len(membres) < 2:
            continue
        for j in range(x.shape[1]):
            if lam >= 1.0:
                touches = membres
            else:
                masque = rng.random(len(membres)) < lam
                touches = membres[masque]
            if len(touches) < 2:
                continue
            xd[touches, j] = x[rng.permutation(touches), j]
    return xd


def groupes_intra_segment(seg, k, etiquette):
    """Partition du bassin en groupes de taille ~k, formes A L'INTERIEUR de chaque
    segment S_gra -- pour que l'agregation n'efface pas les ecarts entre segments.
    Un segment plus petit que k forme un seul groupe."""
    rng = np.random.default_rng([GRAINE, 503, graine_nom(etiquette), k])
    groupes = []
    for g in np.unique(seg):
        membres = np.flatnonzero(seg == g)
        if len(membres) == 0:
            continue
        ordre = rng.permutation(membres)
        groupes.extend(np.array_split(ordre, max(1, len(membres) // k)))
    return [g for g in groupes if len(g)]


def agreg_mode(x, groupes):
    """E3a : chaque membre recoit le MODE par item de son groupe.

    Le mode est une fonction SYMETRIQUE du multiensemble des membres : les |g| lignes
    publiees d'un groupe sont identiques. C'est ce qui fonde la garantie top-1 <= 1/k.
    """
    xd = x.copy()
    for gr in groupes:
        for j in range(x.shape[1]):
            v = x[gr, j]
            v = v[v >= 0]
            xd[gr, j] = np.bincount(v).argmax() if len(v) else -1
    return xd


def agreg_representant(x, groupes, etiquette):
    """E3b : chaque membre recoit la ligne d'UN membre tire uniformement dans son groupe.

    Les lignes publiees d'un groupe sont identiques elles aussi (meme garantie de
    symetrie), et chacune est une ligne REELLE : les correlations survivent. Prix a
    publier avec : le membre tire est republie verbatim.
    """
    rng = np.random.default_rng([GRAINE, 504, graine_nom(etiquette)])
    xd = x.copy()
    choisi = np.zeros(x.shape[0], dtype=bool)
    for gr in groupes:
        c = gr[rng.integers(0, len(gr))]
        choisi[c] = True
        xd[gr] = x[c]
    return xd, choisi


def dp_publication(x, k_items, seg, sigma, conditionne, rng):
    """E5 : jeu synthetique sous DP, mecanisme gaussien compose sous zCDP.

    conditionne = False : histogrammes marginaux par item (architecture de c7_dp_zcdp).
    conditionne = True  : histogrammes par (segment, item). Sous REMPLACEMENT d'une
    ligne, une personne ne contribue qu'a UN segment par item : la sensibilite L2 de
    l'histogramme conditionne vaut racine(2), exactement celle du marginal. Conditionner
    sur le segment, covariable publique, NE COUTE DONC RIEN AU BUDGET -- meme sigma,
    meme rho, meme epsilon.
    """
    n = x.shape[0]
    if not conditionne:
        probs = DP.marginales_bruitees_gauss(x, k_items, sigma, rng)
        return DP.echantillonner(probs, n, rng).astype(x.dtype)
    out = np.empty_like(x)
    marg = DP.marginales_bruitees_gauss(x, k_items, sigma, rng)
    for g in np.unique(seg):
        membres = np.flatnonzero(seg == g)
        if g < 0 or len(membres) == 0:
            if len(membres):
                out[membres] = DP.echantillonner(marg, len(membres), rng)
            continue
        probs_g = DP.marginales_bruitees_gauss(x[membres], k_items, sigma, rng)
        out[membres] = DP.echantillonner(probs_g, len(membres), rng)
    return out


# ===========================================================================
# 2. LES ATTAQUANTS
# ===========================================================================

def _resume(top1_par_personne, etiquette):
    m, b, h = bootstrap_personnes(top1_par_personne, n_tirages=N_BOOTSTRAP,
                                  graine=[GRAINE, 601, graine_nom(etiquette)])
    return {"top1": m, "bas": b, "haut": h, "par_personne": top1_par_personne}


def attaque_naive(X, pool, couverts, cols, etiquette):
    """N : accord de Hamming brut, l'attaque du depot, importee sans modification."""
    rng = np.random.default_rng([GRAINE, 600, graine_nom(etiquette)])
    _, top1, _ = rangs_attaque(X[:, cols], pool[:, cols], couverts, rng)
    return _resume(top1, etiquette)


def attaque_llr(X, pool, couverts, etiquette, cols=None):
    """L : A-LLR RECALIBRE sur la sortie defendue, parametres estimes hors pli.

    C'est ce recalibrage qui rend l'attaquant adaptatif au sens strict : a_j et q_j sont
    ceux de la PUBLICATION DEFENDUE, pas ceux du jumeau brut.
    """
    s = AF.scores_hors_pli(X, pool, couverts, etiquette, colonnes=cols)
    rng = np.random.default_rng([GRAINE, 602, graine_nom(etiquette)])
    _, top1, _ = AF.CS.rangs_depuis_accord(s, couverts, rng, AF.N_TIRAGES_LIENS)
    return _resume(top1, etiquette)


def attaque_s3(X, pool, couverts, cols, seg_c, seg_pool, etiquette):
    """S3 : invariants de segment. Le multiensemble intra-segment est conserve par toute
    permutation intra-segment ; l'attaquant l'exploite sans connaitre la permutation."""
    n_att = X.shape[0]
    s = np.zeros((n_att, pool.shape[0]))
    for pli in AF.plis(n_att, graine_nom(etiquette)):
        entr = np.setdiff1d(np.arange(n_att), pli)
        a, q = AF.parametres(X[entr][:, cols], pool[couverts[entr]][:, cols])
        s[pli] = AF.score_invariant(X[:, cols], X[pli][:, cols], seg_c, seg_pool,
                                    a, q, cols)
    rng = np.random.default_rng([GRAINE, 603, graine_nom(etiquette)])
    _, top1, _ = AF.CS.rangs_depuis_accord(s, couverts, rng, AF.N_TIRAGES_LIENS)
    return _resume(top1, etiquette)


def attaque_contenu(x_origine, pool, couverts, blocs, etiquette):
    """C : LIEN PAR LE CONTENU -- l'attaque dediee des permutations jointes.

    Une permutation intra-segment ne cache que l'INDICE : le contenu d'un bloc d'une
    personne est republie verbatim, ailleurs dans la publication. Un attaquant qui
    apparie par le contenu (et l'attaquant de ce depot apparie par le contenu, jamais
    par l'indice) ne perd donc rien. Operationnellement, le taux sur un bloc est le top-1
    obtenu en attaquant les colonnes de ce bloc sur le contenu D'ORIGINE : la permutation
    jointe ne le change pas. On renvoie le maximum sur les blocs, et la ligne
    « au moins un bloc », qui est le taux de la personne dont AU MOINS un bloc est
    retrouve au rang 1.
    """
    meilleurs = None
    au_moins_un = np.zeros(x_origine.shape[0])
    top_max = None
    for b, bloc in enumerate(blocs):
        r = attaque_naive(x_origine, pool, couverts, bloc, f"{etiquette}|bloc{b}")
        au_moins_un = np.maximum(au_moins_un, r["par_personne"])
        if top_max is None or r["top1"] > top_max["top1"]:
            top_max = r
        meilleurs = r if meilleurs is None else meilleurs
    r_union = _resume(au_moins_un, f"{etiquette}|union")
    return top_max, r_union


# ===========================================================================
# 3. L'UTILITE
# ===========================================================================

def trois_composantes(x_def40, x_base40, seg_c):
    ed = erreur_distribution(x_def40, x_base40)
    eg = erreur_groupes(x_def40, x_base40, seg_c, seg_c)
    ec = erreur_correlations(x_def40, x_base40)
    return ed, eg, ec, float(np.mean([ed, eg, ec]))


def taches_aval(x_def40, ref, genre, age65):
    """Les trois taches de c7_utilite_aval, rejouees sans une ligne reecrite, et
    comparees a la publication NON PROTEGEE (ref)."""
    ra = analyse_a(x_def40, genre)
    rb = analyse_b(x_def40, genre, age65)
    rc = analyse_c(x_def40.astype(float))

    tA = bool(ra["signe"] == ref["A"]["signe"] and ra["signif"] == ref["A"]["signif"])

    chgt = ((rb["signe"].values != ref["B"]["signe"].values) |
            (rb["signif"].values != ref["B"]["signif"].values))[1:]
    n_chgt = int(chgt.sum())
    tB = bool(n_chgt <= 1)

    delta_pc = abs(rc["part_pc1_pc2"] - ref["C"]["part_pc1_pc2"]) * 100
    flip = signe_charges(ref["C"]["charge_pc1"], rc["charge_pc1"]) * 100
    tC = bool(delta_pc <= 5.0 and flip <= 20.0)

    return {"tA_signe": int(ra["signe"]), "tA_signif": bool(ra["signif"]),
            "tA_preservee": tA,
            "tB_coefs_changes_sur_4": n_chgt, "tB_preservee": tB,
            "tC_delta_pc1_pc2_points": delta_pc,
            "tC_pct_charges_axe1_inversees": flip, "tC_preservee": tC,
            "n_taches_preservees": int(tA) + int(tB) + int(tC)}


# ===========================================================================
# 4. LE PROGRAMME
# ===========================================================================

def main(partie="tout"):
    """partie = 'tout' | 'non-dp' | 'dp'.

    Le decoupage n'a AUCUN effet sur les chiffres : toutes les graines sont derivees du
    nom de la condition, jamais d'un compteur d'execution, et le bassin est reconstruit
    a l'identique dans les deux moities. Il n'existe que parce que la consigne
    d'execution de cette passe interdit l'arriere-plan : 'non-dp' ecrit le CSV des
    candidats empiriques, 'dp' le relit et lui ajoute les lignes DP et la reference.
    """
    print(__doc__.split("=" * 75)[1][:1200], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]
    niveaux = paq["niveaux_seg"]["S_gra"]

    items = items_communs(codes, [REF_V4, REF_V13])
    i_achat = np.flatnonzero(np.isin(items, items_achat(paq)))
    i_opinion = np.flatnonzero(~np.isin(items, items_achat(paq)))
    toutes = np.arange(len(items))

    pool = codes[REF_V4][:, items]
    couverts = np.flatnonzero((codes[CIBLE] >= 0).any(axis=1))
    seg_c = seg_gra[couverts]
    x60 = codes[CIBLE][:, items][couverts]
    x40 = x60[:, i_achat]
    hum40 = pool[:, i_achat]
    k_items60 = paq["k_items"][items]
    n = len(couverts)

    print(f"\nbassin constant : {n} personnes, pool {pool.shape[0]} humains vague 4, "
          f"{len(items)} items communs ({len(i_achat)} achat, {len(i_opinion)} opinion)",
          flush=True)
    tailles = np.array([int((seg_c == g).sum()) for g in np.unique(seg_c) if g >= 0])
    print(f"segments S_gra : {len(tailles)}, taille mediane {int(np.median(tailles))}, "
          f"min {tailles.min()}, max {tailles.max()}", flush=True)

    # ---- genre / age, pour les taches en aval (repris de c7_utilite_aval) ----------
    genre_seg = np.array([niveaux[g].split("|")[0] for g in range(len(niveaux))])
    age_seg = np.array([niveaux[g].split("|")[2] for g in range(len(niveaux))])
    genre = (genre_seg[np.clip(seg_c, 0, None)] == "Male").astype(int)
    age65 = (age_seg[np.clip(seg_c, 0, None)] == "65+").astype(int)
    genre[seg_c < 0] = 0
    age65[seg_c < 0] = 0

    # ---- CONTROLE D'INTERPRETABILITE, avant toute interpretation -------------------
    print("\n=== Controle d'interpretabilite (bassin exactement attaque) ===", flush=True)
    baseline = {}
    try:
        d = controle_avant_interpretation(couverts, items, x60, f"{CIBLE}|60 items",
                                          paq=paq)
        baseline = d
        print(f"  PASSE : candidat {d['candidat_top1']*100:.2f} % "
              f"[{d['candidat_ic'][0]*100:.2f};{d['candidat_ic'][1]*100:.2f}] vs "
              f"baseline Demographics Only {d['baseline_top1']*100:.2f} % "
              f"[{d['baseline_ic'][0]*100:.2f};{d['baseline_ic'][1]*100:.2f}]", flush=True)
    except EchecControleInterpretabilite as exc:
        print("  ECHEC — rien de ce qui suit ne doit etre interprete.\n" + str(exc),
              flush=True)
        raise
    seuil_P = baseline["baseline_ic"][0]      # borne BASSE de l'IC de la baseline demo
    print(f"  critere P (preenregistrement §6.1) : borne haute de l'IC adaptatif "
          f"< {seuil_P*100:.3f} %", flush=True)

    # ---- reference non protegee, pour les taches en aval ---------------------------
    ref = {"A": analyse_a(x40, genre), "B": analyse_b(x40, genre, age65),
           "C": analyse_c(x40.astype(float))}
    c_ref = pd.DataFrame(np.where(x40 >= 0, x40, np.nan).astype(float)).corr().values
    iu = np.triu_indices(x40.shape[1], k=1)
    plancher_corr = float(np.nanmean(np.abs(c_ref[iu]))) * 100
    print(f"\nplancher de destruction des correlations (|corr| moyenne, "
          f"{len(iu[0])} paires) : {plancher_corr:.3f} points", flush=True)

    # ---- partitions en blocs correles, deterministes -------------------------------
    partitions = {B: (blocs_correles(x60, B) if B > 1 else [toutes])
                  for B in (1, 2, 5, 10)}
    for B, bl in partitions.items():
        print(f"  partition en {B} bloc(s) : tailles {[len(b) for b in bl]}", flush=True)

    # ===================================================================
    # Construction des candidats
    # ===================================================================
    # (code, famille, reglage, X60 publie, x60 d'origine pour la strategie C,
    #  blocs pour C, garantie, nature)
    candidats = []

    candidats.append(dict(
        code="A0", famille="aucune", reglage="jumeau non protege",
        X=x60, colonnes="60 items", origine=None, blocs=None, s3=False,
        garantie="SANS OBJET", nature="reference (aucune protection)"))

    x_d4 = x60.copy()
    x_d4[:, i_achat] = defense_d4(x40, seg_c)
    candidats.append(dict(
        code="D4tq", famille="permutation", reglage="D4 telle que publiee (40 items)",
        X=x_d4, colonnes="40 items d'achat", origine=None, blocs=None, s3=True,
        s1=i_opinion, garantie="AUCUNE",
        nature="observe seulement — aucune garantie formelle"))

    candidats.append(dict(
        code="E1", famille="permutation",
        reglage="item par item, intra-segment, 60 items",
        X=perm_item_partielle(x60, seg_c, 1.0, "E1"), colonnes="60 items",
        origine=None, blocs=None, s3=True, garantie="AUCUNE",
        nature="observe seulement — aucune garantie formelle"))

    for lam in (0.25, 0.50, 0.75):
        candidats.append(dict(
            code=f"E4(lambda={lam:.2f})", famille="fidelite",
            reglage=f"{int(lam*100)} % des cellules permutees intra-segment, 60 items",
            X=perm_item_partielle(x60, seg_c, lam, f"E4|{lam}"), colonnes="60 items",
            origine=None, blocs=None, s3=True, garantie="AUCUNE",
            nature="observe seulement — aucune garantie formelle"))

    for B in (1, 2, 5, 10):
        bl = partitions[B]
        candidats.append(dict(
            code=f"E2(B={B})", famille="permutation jointe",
            reglage=(f"{B} bloc(s) d'items correles, permutation JOINTE intra-segment, "
                     f"60 items" + (" (= lignes entieres)" if B == 1 else "")),
            X=perm_jointe(x60, seg_c, bl, f"E2|{B}"), colonnes="60 items",
            origine=x60, blocs=bl, s3=False, garantie="AUCUNE",
            nature="observe seulement — aucune garantie formelle"))

    for k in (2, 5, 10, 25):
        gr = groupes_intra_segment(seg_c, k, "E3")
        tg = np.array([len(g) for g in gr])
        candidats.append(dict(
            code=f"E3a(k={k})", famille="agregation",
            reglage=(f"mode par item sur groupes de taille ~{k} formes intra-segment "
                     f"({len(gr)} groupes, taille mediane {int(np.median(tg))})"),
            X=agreg_mode(x60, gr), colonnes="60 items", origine=None, blocs=None,
            s3=False, garantie=f"top-1 <= 1/{k} = {100.0/k:.2f} % (combinatoire)",
            nature=("GARANTI (combinatoire) : les |g| lignes publiees d'un groupe sont "
                    "identiques, un seul humain peut etre classe premier")))
        xr, choisi = agreg_representant(x60, gr, f"E3b|{k}")
        candidats.append(dict(
            code=f"E3b(k={k})", famille="agregation",
            reglage=(f"ligne d'un membre tire par groupe de taille ~{k} intra-segment "
                     f"({len(gr)} groupes, {int(choisi.sum())} personnes republiees "
                     f"verbatim)"),
            X=xr, colonnes="60 items", origine=None, blocs=None, s3=False,
            choisi=choisi,
            garantie=f"top-1 <= top-1(A0)/{k} (combinatoire, par symetrie d'echange)",
            nature=("GARANTI en moyenne (combinatoire) — mais 1 personne sur "
                    f"{k} est republiee VERBATIM : divulgation d'attribut totale "
                    "pour celle-la")))

    if partie == "dp":
        candidats = []
        print("\npartie 'dp' : les candidats empiriques sont relus du CSV existant.",
              flush=True)
    else:
        print(f"\n{len(candidats)} candidats non-DP construits.", flush=True)

    # ===================================================================
    # Mesure : protection (naif + adaptatif) et cout
    # ===================================================================
    lignes = []
    a0_par_personne = None
    if partie == "dp":
        ancien = pd.read_csv(os.path.join(T1.SORTIE, "c7-defense-adaptative.csv"))
        ancien = ancien[(ancien.bloc == "candidat")
                        & (ancien.famille != "confidentialite differentielle")]
        for col in ("tA_replicats_preserves", "tB_replicats_preserves",
                    "tC_replicats_preserves"):
            if col not in ancien.columns:
                ancien[col] = "tirage unique (reduction declaree §8)"
        lignes = ancien.to_dict("records")
        print(f"  {len(lignes)} lignes de candidats empiriques relues.", flush=True)

    for cand in candidats:
        code = cand["code"]
        X = cand["X"]
        print(f"\n--- {code} : {cand['reglage']} ---", flush=True)

        r_naif = attaque_naive(X, pool, couverts, toutes, f"{code}|N")
        print(f"  N   naif (Hamming)            top1={r_naif['top1']*100:.3f} % "
              f"[{r_naif['bas']*100:.3f} ; {r_naif['haut']*100:.3f}]", flush=True)
        if code == "A0":
            a0_par_personne = r_naif["par_personne"]

        strategies = {"N naif (Hamming)": r_naif}

        r_llr = attaque_llr(X, pool, couverts, f"{code}|L")
        strategies["L A-LLR recalibre sur la defense (hors pli)"] = r_llr
        print(f"  L   A-LLR recalibre           top1={r_llr['top1']*100:.3f} % "
              f"[{r_llr['bas']*100:.3f} ; {r_llr['haut']*100:.3f}]", flush=True)

        if cand.get("s1") is not None:
            r_s1 = attaque_llr(X, pool, couverts, f"{code}|S1", cols=cand["s1"])
            strategies["S1 colonnes intactes"] = r_s1
            print(f"  S1  colonnes intactes         top1={r_s1['top1']*100:.3f} % "
                  f"[{r_s1['bas']*100:.3f} ; {r_s1['haut']*100:.3f}]", flush=True)

        if cand.get("s3"):
            cols_s3 = i_achat if code == "D4tq" else toutes
            r_s3 = attaque_s3(X, pool, couverts, cols_s3, seg_c, seg_gra, f"{code}|S3")
            strategies["S3 invariants de segment"] = r_s3
            print(f"  S3  invariants de segment     top1={r_s3['top1']*100:.3f} % "
                  f"[{r_s3['bas']*100:.3f} ; {r_s3['haut']*100:.3f}]", flush=True)

        if cand.get("blocs") is not None:
            r_max, r_union = attaque_contenu(cand["origine"], pool, couverts,
                                             cand["blocs"], f"{code}|C")
            strategies["C lien par le contenu (meilleur bloc)"] = r_max
            strategies["C lien par le contenu (au moins un bloc)"] = r_union
            print(f"  C   lien par le contenu       meilleur bloc "
                  f"{r_max['top1']*100:.3f} % | au moins un bloc "
                  f"{r_union['top1']*100:.3f} %", flush=True)

        if cand.get("choisi") is not None and a0_par_personne is not None:
            ind = a0_par_personne * cand["choisi"].astype(float)
            r_c = _resume(ind, f"{code}|C")
            strategies["C lien par le contenu (membre republie verbatim)"] = r_c
            expo = (a0_par_personne[cand["choisi"]].mean()
                    if cand["choisi"].any() else np.nan)
            cand["taux_conditionnel_exposes"] = expo
            print(f"  C   contenu (membre republie) top1={r_c['top1']*100:.3f} % "
                  f"[{r_c['bas']*100:.3f} ; {r_c['haut']*100:.3f}] ; "
                  f"conditionnel aux personnes republiees : {expo*100:.2f} %", flush=True)

        nom_ad, r_ad = max(((k, v) for k, v in strategies.items()),
                           key=lambda kv: kv[1]["top1"])
        print(f"  => ADAPTATIF = {nom_ad} : {r_ad['top1']*100:.3f} % "
              f"[{r_ad['bas']*100:.3f} ; {r_ad['haut']*100:.3f}]", flush=True)

        x_def40 = X[:, i_achat]
        ed, eg, ec, ug = trois_composantes(x_def40, x40, seg_c)
        tch = taches_aval(x_def40, ref, genre, age65)
        passe_P = bool(r_ad["haut"] < seuil_P)
        lignes.append(dict(
            bloc="candidat", code=code, famille=cand["famille"],
            reglage=cand["reglage"], colonnes_couvertes=cand["colonnes"], n=n,
            n_pool=pool.shape[0],
            top1_naif=r_naif["top1"], top1_naif_bas=r_naif["bas"],
            top1_naif_haut=r_naif["haut"],
            top1_adaptatif=r_ad["top1"], top1_adaptatif_bas=r_ad["bas"],
            top1_adaptatif_haut=r_ad["haut"], strategie_adaptative=nom_ad,
            strategies_mesurees=" | ".join(f"{k} = {v['top1']*100:.3f} %"
                                            for k, v in strategies.items()),
            erreur_distribution=ed, erreur_groupes=eg, erreur_correlations=ec,
            utilite_globale=ug,
            plancher_correlations=plancher_corr,
            passe_P=passe_P, passe_P1pct=bool(r_ad["top1"] < SEUIL_P1PCT),
            seuil_P_borne_basse_baseline_demo=seuil_P,
            **tch,
            utilisable=bool(passe_P and tch["n_taches_preservees"] >= 1),
            tA_replicats_preserves="tirage unique (reduction declaree §8)",
            tB_replicats_preserves="tirage unique (reduction declaree §8)",
            tC_replicats_preserves="tirage unique (reduction declaree §8)",
            nature_de_la_protection=cand["nature"], borne_garantie=cand["garantie"],
            taux_conditionnel_exposes=cand.get("taux_conditionnel_exposes", np.nan),
            epsilon="SANS OBJET", replicat="tirage unique (reduction declaree §8)",
        ))

    if partie == "non-dp":
        T1.ecrire(pd.DataFrame(lignes), "c7-defense-adaptative.csv")
        print("\npartie 'non-dp' terminee ; relancer avec --dp pour les lignes DP.",
              flush=True)
        return

    # ===================================================================
    # E5 : la confidentialite differentielle, correctement implementee
    # ===================================================================
    print("\n=== E5 : DP gaussienne composee sous zCDP (delta = 1e-6) ===", flush=True)
    for conditionne in (False, True):
        archi = ("marginales conditionnees au segment" if conditionne
                 else "marginales d'item (architecture c7_dp_zcdp)")
        for eps in EPSILONS:
            nom_eps = DP.nom_eps(eps)
            rho = DP.rho_depuis_eps_delta(eps)
            sigma = DP.sigma_gaussien(rho, len(items))
            code = f"E5({'seg' if conditionne else 'marg'}, {nom_eps})"

            # utilite : 5 replicats ; risque : 2 replicats (reductions declarees §8)
            comps, taches = [], []
            Xs = []
            for r in range(N_REPLICATS_DP_UTILITE):
                rng = np.random.default_rng([GRAINE, 700, int(conditionne),
                                             graine_nom(nom_eps), r])
                Xr = dp_publication(x60, k_items60, seg_c, sigma, conditionne, rng)
                Xs.append(Xr)
                comps.append(trois_composantes(Xr[:, i_achat], x40, seg_c))
                taches.append(taches_aval(Xr[:, i_achat], ref, genre, age65))
            comps = np.array(comps)
            ed, eg, ec, ug = comps.mean(axis=0)

            naifs, ads, noms = [], [], []
            for r in range(N_REPLICATS_DP_RISQUE):
                rn = attaque_naive(Xs[r], pool, couverts, toutes, f"{code}|N|{r}")
                rl = attaque_llr(Xs[r], pool, couverts, f"{code}|L|{r}")
                naifs.append(rn)
                pick = max((("N naif (Hamming)", rn),
                            ("L A-LLR recalibre sur la defense (hors pli)", rl)),
                           key=lambda kv: kv[1]["top1"])
                noms.append(pick[0])
                ads.append(pick[1])
            m_naif = float(np.mean([r["top1"] for r in naifs]))
            m_ad = float(np.mean([r["top1"] for r in ads]))
            b_ad = float(min(r["bas"] for r in ads))
            h_ad = float(max(r["haut"] for r in ads))

            # Une tache n'est declaree preservee que si elle l'est sur TOUS les
            # replicats ; le compte par tache est publie a cote, pour qu'un « 4 sur 5 »
            # ne se lise pas comme un « 0 sur 5 ».
            tch = {k: (float(np.mean([t[k] for t in taches]))
                       if not isinstance(taches[0][k], bool)
                       else bool(all(t[k] for t in taches)))
                   for k in taches[0]}
            tch["n_taches_preservees"] = (int(tch["tA_preservee"])
                                          + int(tch["tB_preservee"])
                                          + int(tch["tC_preservee"]))
            compte = {f"{t}_replicats_preserves":
                      f"{int(sum(x[f'{t}_preservee'] for x in taches))}"
                      f"/{N_REPLICATS_DP_UTILITE}" for t in ("tA", "tB", "tC")}
            tch.update(compte)
            passe_P = bool(h_ad < seuil_P)
            print(f"  {code:44s} naif={m_naif*100:.3f} % adaptatif={m_ad*100:.3f} % "
                  f"[{b_ad*100:.3f} ; {h_ad*100:.3f}] | distrib={ed:.2f} "
                  f"groupes={eg:.2f} corr={ec:.2f} | taches={tch['n_taches_preservees']}/3 "
                  f"(A {compte['tA_replicats_preserves']}, B "
                  f"{compte['tB_replicats_preserves']}, C "
                  f"{compte['tC_replicats_preserves']} replicats)", flush=True)

            lignes.append(dict(
                bloc="candidat", code=code, famille="confidentialite differentielle",
                reglage=f"{archi} ; rho={rho:.4f} ; sigma={sigma:.3f}",
                colonnes_couvertes="60 items", n=n, n_pool=pool.shape[0],
                top1_naif=m_naif, top1_naif_bas=float(min(r["bas"] for r in naifs)),
                top1_naif_haut=float(max(r["haut"] for r in naifs)),
                top1_adaptatif=m_ad, top1_adaptatif_bas=b_ad, top1_adaptatif_haut=h_ad,
                strategie_adaptative=" / ".join(sorted(set(noms))),
                strategies_mesurees=(f"N = {m_naif*100:.3f} % ; "
                                     f"adaptatif (max N,L) = {m_ad*100:.3f} %"),
                erreur_distribution=ed, erreur_groupes=eg, erreur_correlations=ec,
                utilite_globale=ug, plancher_correlations=plancher_corr,
                passe_P=passe_P, passe_P1pct=bool(m_ad < SEUIL_P1PCT),
                seuil_P_borne_basse_baseline_demo=seuil_P,
                **tch,
                utilisable=bool(passe_P and tch["n_taches_preservees"] >= 1),
                nature_de_la_protection=(
                    "GARANTI (formel) : (eps, delta)-DP, delta = 1e-6, sous remplacement "
                    "d'une ligne, avec immunite au post-traitement. SEULE garantie "
                    "formelle de cette table. AUCUNE comparaison de cout avec un "
                    "mecanisme empirique n'est faite ni permise, dans aucun sens."),
                borne_garantie=f"({nom_eps}, delta=1e-6)-DP",
                taux_conditionnel_exposes=np.nan, epsilon=nom_eps,
                replicat=(f"{N_REPLICATS_DP_UTILITE} replicats (utilite), "
                          f"{N_REPLICATS_DP_RISQUE} (risque) — reductions declarees §8 ; "
                          "bornes = etendue sur replicats, PAS un IC"),
            ))

    # ===================================================================
    # Lignes de reference
    # ===================================================================
    lignes.append(dict(
        bloc="reference", code="baseline Demographics Only - GPT4.1-mini",
        famille="controle", reglage="recalculee par c7_controle_interpretabilite sur "
                                     "le bassin exactement attaque",
        colonnes_couvertes="60 items", n=n, n_pool=pool.shape[0],
        top1_naif=baseline["baseline_top1"], top1_naif_bas=baseline["baseline_ic"][0],
        top1_naif_haut=baseline["baseline_ic"][1],
        top1_adaptatif=np.nan, top1_adaptatif_bas=np.nan, top1_adaptatif_haut=np.nan,
        strategie_adaptative="SANS OBJET",
        strategies_mesurees="SANS OBJET",
        erreur_distribution=np.nan, erreur_groupes=np.nan, erreur_correlations=np.nan,
        utilite_globale=np.nan, plancher_correlations=plancher_corr,
        passe_P=False, passe_P1pct=False, seuil_P_borne_basse_baseline_demo=seuil_P,
        tA_signe=0, tA_signif=False, tA_preservee=False, tB_coefs_changes_sur_4=0,
        tB_preservee=False, tC_delta_pc1_pc2_points=np.nan,
        tC_pct_charges_axe1_inversees=np.nan, tC_preservee=False,
        n_taches_preservees=0, utilisable=False,
        tA_replicats_preserves="SANS OBJET", tB_replicats_preserves="SANS OBJET",
        tC_replicats_preserves="SANS OBJET",
        nature_de_la_protection="SANS OBJET — c'est le seuil du critere P",
        borne_garantie="SANS OBJET", taux_conditionnel_exposes=np.nan,
        epsilon="SANS OBJET", replicat="SANS OBJET",
    ))

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-defense-adaptative.csv")

    # ===================================================================
    # Verdict sur les predictions preenregistrees
    # ===================================================================
    print("\n" + "=" * 70, flush=True)
    print("VERDICT sur les predictions preenregistrees", flush=True)
    print("=" * 70, flush=True)
    c = df[df.bloc == "candidat"]
    util = c[c.utilisable]
    print(f"\ncandidats utilisables (passent P ET preservent >= 1 tache) : "
          f"{len(util)} / {len(c)}", flush=True)
    for _, r in util.iterrows():
        print(f"  {r.code:44s} adaptatif={r.top1_adaptatif*100:.3f} % "
              f"[{r.top1_adaptatif_bas*100:.3f};{r.top1_adaptatif_haut*100:.3f}] "
              f"taches A/B/C = {int(r.tA_preservee)}{int(r.tB_preservee)}"
              f"{int(r.tC_preservee)} | distrib={r.erreur_distribution:.2f} "
              f"groupes={r.erreur_groupes:.2f} corr={r.erreur_correlations:.2f}",
              flush=True)
    if len(util) == 0:
        print("  AUCUN. Le §6.4 du preenregistrement s'applique : la conclusion "
              "publiee est « nous n'avons pas trouve de remede ».", flush=True)

    def ligne(code):
        s = c[c.code == code]
        return s.iloc[0] if len(s) else None

    print("\n[Q1] gagnant attendu E3a(k>=10) :", flush=True)
    for k in (10, 25):
        r = ligne(f"E3a(k={k})")
        if r is not None:
            print(f"  E3a(k={k}) passe_P={bool(r.passe_P)} "
                  f"taches={int(r.n_taches_preservees)}/3 -> "
                  f"{'TENUE' if r.utilisable else 'REFUTEE'}", flush=True)
    print("\n[Q2] E2 (permutation jointe) refutee comme reparation :", flush=True)
    e2 = c[c.code.str.startswith("E2(")]
    print(f"  aucun E2 ne passe P : "
          f"{'Q2 TENUE' if not e2.passe_P.any() else 'Q2 REFUTEE'} ; "
          f"top-1 adaptatif de E2(B=1) = "
          f"{ligne('E2(B=1)').top1_adaptatif*100:.3f} % pour un cout total de "
          f"{ligne('E2(B=1)').utilite_globale:.3f} point", flush=True)
    print("\n[Q3] E4 : aucun lambda intermediaire ne passe P avec T-C :", flush=True)
    e4 = c[c.code.str.startswith("E4(")]
    ok3 = ((e4.passe_P) & (e4.tC_preservee)).any()
    print(f"  {'Q3 REFUTEE' if ok3 else 'Q3 TENUE'}", flush=True)
    print("\n[Q4] E5 passe P a tout eps ; le conditionnement au segment sauve T-A :",
          flush=True)
    e5 = c[c.code.str.startswith("E5(")]
    print(f"  E5 passe P partout : {bool(e5.passe_P.all())}", flush=True)
    for archi in ("marg", "seg"):
        s = e5[e5.code.str.contains(archi)]
        print(f"  architecture {archi} : erreur_groupes moyenne "
              f"{s.erreur_groupes.mean():.3f} ; T-A preservee sur "
              f"{int(s.tA_preservee.sum())}/{len(s)} reglages ; T-C sur "
              f"{int(s.tC_preservee.sum())}/{len(s)}", flush=True)
    print("\n[Q5] E1 protege mieux que D4tq mais ne preserve pas T-C :", flush=True)
    r1, rd = ligne("E1"), ligne("D4tq")
    print(f"  E1 adaptatif={r1.top1_adaptatif*100:.3f} % vs D4tq "
          f"{rd.top1_adaptatif*100:.3f} % ; E1 T-C preservee={bool(r1.tC_preservee)} -> "
          f"{'TENUE' if (r1.top1_adaptatif < rd.top1_adaptatif and not r1.tC_preservee) else 'REFUTEE'}",
          flush=True)
    print(f"\n[Q6] au moins un candidat utilisable : "
          f"{'TENUE' if len(util) else 'REFUTEE — §6.4 s applique'}", flush=True)

    print("\nRAPPEL. Les taux des familles E1, E2, E4 et de D4tq sont ceux des attaques "
          "que nous avons construites, contre des mecanismes SANS garantie : aucun "
          "n'est une borne. Seuls E3a, E3b (garantie combinatoire) et E5 (garantie "
          "formelle) portent une borne. Aucune superiorite d'un mecanisme empirique sur "
          "la confidentialite differentielle n'est revendiquee, dans aucun sens.",
          flush=True)


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "--tout"
    main({"--non-dp": "non-dp", "--dp": "dp"}.get(arg, "tout"))
