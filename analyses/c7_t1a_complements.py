"""
c7_t1a_complements : les cinq volets manquants de la tache T1a du plan de revision
du 13 septembre 2026 -- §1c, §1d, §1e, §1f, §1g.

===========================================================================
POST HOC, NON PREENREGISTRE. Ces cinq volets ont ete construits APRES le debut des
revisions, en reponse a une relecture adverse, puis prescrits par
resultats/plan-revision-2026-09-13.md §3 (tache T1a). Aucun plan ne les precedait : ils
sont post-hoc par rapport au preenregistrement d'origine de C7. Le fichier
resultats/c7-t1a-complements-preenregistrement.md documente donc un protocole ecrit
avant le premier calcul, mais pour des mesures choisies apres coup, et le dit en toutes
lettres. Cette mention doit suivre ces chiffres partout, manuscrit compris.

CE QUI EST DEJA FAIT AILLEURS, ET N'EST PAS REFAIT ICI : T1a §1a (courbe top-1 vs
nombre d'items) et §1b (Argyle sous A-LLR et monde ouvert) existent sur la branche
agent/mesures/temoins-relecture (commit 048a5d2), dans analyses/c7_temoins_relecture.py
et resultats/c7-temoins-relecture.csv. Aucune ligne de ce script n'est reimplementee,
modifiee ni recopiee ici ; aucune ligne de analyses/c7_reidentification.py non plus.

ETUDE DE RISQUE DE VIE PRIVEE sur des jeux deja publics (Twin-2K-500 ; archive Park et
al. ; Argyle, Busby, Fulda, Gubler, Rytting & Wingate 2023, Harvard Dataverse
doi:10.7910/DVN/JPV20K, licence CC0). Ce script ne calcule, n'imprime et n'ecrit JAMAIS
l'identite, le pid ou l'identifiant ANES d'une personne retrouvee, ni aucune liste
d'appariements individuels. Les tailles de classes d'ex aequo sortent en DISTRIBUTION
(mediane, quantiles, maximum), jamais personne par personne. Seuls des taux, des comptes
et des distributions agregees atteignent resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee ni modifiee :
  c7_argyle.charger / baseline_demographique / baseline_oracle /
      controle_avant_interpretation                le jeu 2023, ses deux baselines et
                                                   sa regle de decision
  a2_commun.distance_hamming / bootstrap_personnes / en_codes / b2_voisins
                                                   le score naif et l'IC par
                                                   reechantillonnage de PERSONNES
  c7_reidentification.items_communs / graine_nom / REF_V4 / REF_V13 / DEMO
                                                   les items communs et les graines
  c7_attaquant_fort.scores_hors_pli                l'attaquant FORT A-LLR, importe sans
                                                   modification -- la fonction meme qui
                                                   a produit 90,40 % et 23,23 %
  c7_monde_ouvert.marges_deux_regimes / roc_et_taux / compte_au_moins / pmm_depuis_demo
                                                   le protocole de monde ouvert et le
                                                   comparateur PMM k=10
  c7_fort_monde_ouvert_ic.charger_twin / charger_stanford
                                                   les chargeurs canoniques des deux
                                                   jeux du monde ouvert
  c7_stanford.charger_domaine / coder_categoriel_commun / accord_categoriel /
      rangs_depuis_accord                          l'archive Park et son score
  c7_controle_interpretabilite.controle_avant_interpretation
                                                   le controle canonique, appele AVANT
                                                   toute interpretation
  t1_commun.charger / ecrire                       les tables Twin et l'ecriture du CSV

CE QUI EST NOUVEAU ICI, et rien d'autre :
  §1c  Argyle : distribution des classes d'ex aequo au rang 1, top-1 sous les TROIS
       conventions de departage (en faveur / esperance uniforme / contre), intervalle
       exact de Clopper-Pearson, difference APPARIEE jumeau - B-demo, et top-1 de
       B-oracle. Plus, declare comme AJOUT hors du tableau du plan, la distribution des
       classes d'ex aequo de Twin a 60 items, que R1 geste 4 cite sans qu'aucun volet
       ne la produise.
  §1d  Park et Twin a FPR = 0,1 % et 1 % : TPR en fonction en ESCALIER (le plus grand
       TPR dont le FPR reste <= cible), faux positifs absolus, nombre de seuils a moins
       de 1,5 FP de la cible, etendue des TPR admissibles -- et la valeur publiee par
       np.interp a cote, pour que l'ecart se voie.
  §1e  Spearman n = 12 : bootstrap sur les PAIRES (et non sur les personnes a
       configurations figees), Fisher-z (Bonett-Wright), permutation.
  §1f  36,4 % : bootstrap en GRAPPES par configuration, bootstrap naif, etendue,
       ecart-type, sensibilite Monte-Carlo a la graine.
  §1g  La baseline demographique en MONDE OUVERT SOUS A-LLR, Park et Twin, deux FPR --
       le comparateur du chiffre de tete recevant enfin le meme traitement que la cible.

DEUX PIEGES FERMES PAR CONSTRUCTION, parce qu'ils ont deja coute a ce projet :
  1. BASSIN STRICTEMENT CONSTANT. Dans chaque volet, le bassin, le pool et les colonnes
     d'items sont calcules UNE FOIS et servent a toutes les conditions. Le top-1 en
     depend mecaniquement. Aucune condition ne re-tranche le bassin.
  2. BASELINE RECALCULEE DANS LA CONDITION EXACTE DE COMPARAISON. Aucune baseline n'est
     empruntee a un autre bassin, a un autre nombre d'items ni a une autre attaque. En
     §1g, la cible et le comparateur passent par le MEME chargeur, la MEME matrice de
     pool et la MEME attaque, dans le meme appel.
ET UN NOMMAGE QUI NE MELANGE PAS TROIS CHOSES : ic_bas/ic_haut est un bootstrap,
  ic_clopper_pearson_* un intervalle binomial exact, percentile_loi_nulle_* des
  percentiles d'une loi nulle. Un intervalle de confiance et les percentiles d'une loi
  nulle ne sont pas la meme chose.

Graine maitresse fixee. Aucun appel de modele de langage, aucune depense, aucun reseau,
aucune recherche web, aucune execution en arriere-plan. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_t1a_complements.py
===========================================================================
"""

import os
import sys

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd
from scipy import stats

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from a2_commun import (                                                  # noqa: E402
    distance_hamming, bootstrap_personnes, en_codes,
)
from c7_reidentification import (                                        # noqa: E402
    items_communs, graine_nom, REF_V4, REF_V13, DEMO,
)
from c7_attaquant_fort import scores_hors_pli, CIBLE_TWIN, CIBLE_STAN    # noqa: E402
from c7_monde_ouvert import (                                            # noqa: E402
    marges_deux_regimes, roc_et_taux, compte_au_moins, pmm_depuis_demo,
)
import c7_fort_monde_ouvert_ic as MO                                     # noqa: E402
import c7_stanford as CS                                                 # noqa: E402
import c7_argyle as AR                                                   # noqa: E402
import c7_controle_interpretabilite as CTL                               # noqa: E402

GRAINE = 20260913
N_BOOTSTRAP = 2000
N_BOOT_RHO = 20000
N_BOOT_GRAPPES = 20000
N_PERMUTATIONS = 10000
TOL = 1e-12
FPR_CIBLES = (0.001, 0.01)
GRAINES_SENSIBILITE = (1, 2, 3, 20260912, 20260913)

# Verifications de raccordement posees AVANT calcul (preenregistrement §7).
# Un ecart au-dela de la tolerance arrete le volet : ce n'est pas une cible a
# atteindre, c'est la preuve que le portage reproduit bien la chaine publiee.
RACCORDEMENT = {
    "Park GSS|monde ferme A-LLR": (0.9040, 5e-4),
    "Park GSS|tpr_fpr_1pct A-LLR": (0.6017, 5e-4),
    "Park GSS|tpr_fpr_0_1pct A-LLR": (0.4437, 5e-4),
    "Twin|monde ferme A-LLR": (0.2323, 5e-4),
    "Twin|tpr_fpr_1pct A-LLR": (0.0428, 5e-4),
    "Twin|tpr_fpr_0_1pct A-LLR": (0.0101, 5e-4),
    "rho Spearman 12 configurations": (0.9580, 5e-4),
    "moyenne 30 paires a 60 items": (0.36380, 5e-5),
    "temoin anti-artefact 30 paires": (0.00040, 5e-5),
}
_ecarts_raccordement = []


def verifier_raccordement(cle, valeur):
    """Compare a la valeur publiee et RAPPORTE l'ecart. Ne modifie jamais rien."""
    if cle not in RACCORDEMENT:
        return True
    attendu, tol = RACCORDEMENT[cle]
    ok = abs(float(valeur) - attendu) <= tol
    marque = "OK" if ok else "ECART"
    print(f"    [raccordement {marque}] {cle} : mesure {valeur:.6f}, "
          f"publie {attendu:.6f}", flush=True)
    if not ok:
        _ecarts_raccordement.append((cle, float(valeur), attendu))
    return ok


def ligne(volet, jeu, condition, attaque, mesure, valeur, bas=np.nan, haut=np.nan,
          **extra):
    d = {"volet": volet, "jeu": jeu, "condition": condition, "attaque": attaque,
         "mesure": mesure, "valeur": valeur, "ic_bas": bas, "ic_haut": haut}
    d.update(extra)
    return d


def ic_personnes(indic, cle):
    """IC 95 % bootstrap sur les PERSONNES. Graine derivee du nom de la mesure."""
    return bootstrap_personnes(np.asarray(indic, dtype=float),
                               n_tirages=N_BOOTSTRAP, graine=[GRAINE, graine_nom(cle)])


# ---------------------------------------------------------------------------
# Brique commune a §1c : les trois conventions de departage, sur UNE matrice de score
# ---------------------------------------------------------------------------

def conventions_de_departage(acc, vrai_idx):
    """Trois lectures de la MEME matrice de score, pas trois experiences.

    acc : (n_attaques, n_pool), score d'accord (plus grand = plus proche).
    vrai_idx : indice, dans le pool, de la vraie personne de chaque attaque.

    Renvoie, par personne, l'indicatrice top-1 sous chacune des trois conventions
    encadrantes, plus la taille de la classe d'ex aequo de tete. Aucune de ces
    quantites n'est ecrite ni imprimee personne par personne : seules leurs moyennes
    et leurs distributions sortent.
    """
    n = acc.shape[0]
    rangs = np.arange(n)
    vrai = acc[rangs, vrai_idx]
    meilleur = acc.max(axis=1)
    taille_classe = (acc >= meilleur[:, None] - TOL).sum(axis=1)
    dans_classe = vrai >= meilleur - TOL
    # en faveur de l'attaquant : compte des que rien n'est STRICTEMENT meilleur
    en_faveur = ((acc > vrai[:, None] + TOL).sum(axis=1) + 1) == 1
    # contre l'attaquant : compte seulement si la classe de tete est un singleton
    contre = (acc >= vrai[:, None] - TOL).sum(axis=1) == 1
    # esperance sous departage uniforme : la convention PUBLIEE
    uniforme = np.where(dans_classe, 1.0 / taille_classe, 0.0)
    return {"en_faveur": en_faveur.astype(float), "uniforme": uniforme,
            "contre": contre.astype(float), "taille_classe": taille_classe,
            "dans_classe": dans_classe}


def publier_classes(lignes, volet, jeu, condition, attaque, c, n_pool, **extra):
    """Distribution des classes d'ex aequo au rang 1, en agrege uniquement."""
    t = c["taille_classe"]
    commun = dict(n_attaques=len(t), n_pool=n_pool, hasard=1.0 / n_pool, **extra)
    mesures = [
        ("classe_tete_personnes_dans_la_classe", float(c["dans_classe"].sum())),
        ("classe_tete_part_personnes_dans_la_classe", float(c["dans_classe"].mean())),
        ("classe_tete_taille_mediane", float(np.median(t))),
        ("classe_tete_taille_moyenne", float(t.mean())),
        ("classe_tete_taille_q25", float(np.percentile(t, 25))),
        ("classe_tete_taille_q75", float(np.percentile(t, 75))),
        ("classe_tete_taille_q95", float(np.percentile(t, 95))),
        ("classe_tete_taille_max", float(t.max())),
        ("classe_tete_part_singletons", float((t == 1).mean())),
    ]
    for m, v in mesures:
        lignes.append(ligne(volet, jeu, condition, attaque, m, v, **commun))
    print(f"    classes d'ex aequo au rang 1 : {int(c['dans_classe'].sum())} personnes "
          f"sur {n_pool} dans la classe de tete ; taille mediane "
          f"{np.median(t):.0f}, moyenne {t.mean():.2f}, max {int(t.max())}, "
          f"singletons {(t == 1).mean()*100:.2f} %", flush=True)


# ---------------------------------------------------------------------------
# §1c -- Argyle 2023 : ex aequo, conventions encadrantes, B-oracle
# ---------------------------------------------------------------------------

def volet_1c(lignes):
    print("\n" + "=" * 78, flush=True)
    print("§1c  ARGYLE 2023 : classes d'ex aequo, conventions de departage, B-oracle",
          flush=True)
    print("=" * 78, flush=True)
    volet = "1c ex aequo et B-oracle (Argyle)"

    humains, jumeaux, _ids, noms, demo = AR.charger()
    # BASSIN UNIQUE, calcule une seule fois, partage par TOUTES les conditions.
    plein = (humains >= 0).all(axis=1)
    h = humains[plein]
    n = h.shape[0]
    vrai_idx = np.arange(n)
    print(f"  bassin unique : {n} personnes completes, {len(noms)} items, "
          f"hasard = {100.0/n:.4f} %", flush=True)

    # --- CONTROLE D'INTERPRETABILITE, AVANT TOUTE INTERPRETATION -------------
    print("\n  -- controle d'interpretabilite (c7_argyle, regle canonique) --",
          flush=True)
    for nom, X in jumeaux.items():
        try:
            d = AR.controle_avant_interpretation(h, demo, X[plein], nom)
            passe = True
        except AR.EchecControleInterpretabilite as exc:
            d, passe = exc.diagnostic, False
        lignes.append(ligne(
            volet, "Argyle 2023", nom, "naif (Hamming)",
            "controle_interpretabilite_passe", float(passe),
            d["candidat_ic"][0], d["candidat_ic"][1], n_pool=n, n_attaques=n,
            candidat_top1=d["candidat_top1"], baseline_top1=d["baseline_top1"],
            baseline_ic_bas=d["baseline_ic"][0], baseline_ic_haut=d["baseline_ic"][1],
            hasard=d["hasard"],
            note="baseline demographique recalculee par la fonction canonique sur CE "
                 "bassin ; aucune valeur de baseline ne lui est fournie"))
        print(f"    {nom:34s} {'PASSE' if passe else 'ECHEC'} : candidat "
              f"{d['candidat_top1']*100:.4f} % [{d['candidat_ic'][0]*100:.4f};"
              f"{d['candidat_ic'][1]*100:.4f}] vs baseline "
              f"{d['baseline_top1']*100:.4f} % [{d['baseline_ic'][0]*100:.4f};"
              f"{d['baseline_ic'][1]*100:.4f}]", flush=True)

    # --- LES TROIS CONDITIONS, SUR LE MEME BASSIN ET LE MEME POOL ------------
    conditions = {nom: X[plein] for nom, X in jumeaux.items()}
    conditions["B-demo (4 variables demographiques, LOO k=10)"] = \
        AR.baseline_demographique(h, demo)
    conditions["B-oracle (11 vraies reponses, LOO k=10)"] = \
        AR.baseline_oracle(h, demo)

    print("\n  -- top-1 sous les TROIS conventions de departage, meme matrice --",
          flush=True)
    indic = {}
    for nom, x in conditions.items():
        if x.shape != h.shape:
            raise SystemExit(f"{nom} : forme {x.shape}, bassin {h.shape}. "
                             "Le bassin ne serait plus constant entre conditions.")
        acc = 1.0 - distance_hamming(x, h)
        c = conventions_de_departage(acc, vrai_idx)
        indic[nom] = c
        commun = dict(n_attaques=n, n_pool=n, hasard=1.0 / n, n_items=len(noms))
        for cle, etiquette in (
                ("en_faveur", "top1_ex_aequo_en_faveur_de_l_attaquant"),
                ("uniforme", "top1_esperance_departage_uniforme_PUBLIE"),
                ("contre", "top1_ex_aequo_contre_l_attaquant")):
            m, b, hh = ic_personnes(c[cle], f"1c|{nom}|{cle}")
            lignes.append(ligne(volet, "Argyle 2023", nom, "naif (Hamming)",
                                etiquette, m, b, hh, **commun))
        publier_classes(lignes, volet, "Argyle 2023", nom, "naif (Hamming)", c, n,
                        n_items=len(noms))
        print(f"    {nom:44s} en faveur {c['en_faveur'].mean()*100:.4f} %  | "
              f"uniforme (publie) {c['uniforme'].mean()*100:.4f} %  | "
              f"contre {c['contre'].mean()*100:.4f} %", flush=True)

    # --- CLOPPER-PEARSON sur le jumeau principal, convention publiee ---------
    principal = list(jumeaux.keys())[0]
    t_twin = indic[principal]["uniforme"]
    succes = int(round(t_twin.sum()))
    bt = stats.binomtest(succes, n, 1.0 / n, alternative="greater")
    cp_bas, cp_haut = stats.binomtest(succes, n, 1.0 / n).proportion_ci(method="exact")
    lignes.append(ligne(
        volet, "Argyle 2023", principal, "naif (Hamming)",
        "top1_esperance_departage_uniforme_intervalle_exact", float(t_twin.mean()),
        n_attaques=n, n_pool=n, hasard=1.0 / n,
        ic_clopper_pearson_bas=float(cp_bas), ic_clopper_pearson_haut=float(cp_haut),
        succes_arrondis=succes, p_binomial_exact_superieur_au_hasard=float(bt.pvalue),
        note="intervalle binomial EXACT (Clopper-Pearson), PAS un bootstrap : colonnes "
             "ic_clopper_pearson_* distinctes de ic_bas/ic_haut"))
    print(f"\n    Clopper-Pearson ({succes} succes arrondis sur {n}) : "
          f"[{cp_bas*100:.4f} ; {cp_haut*100:.4f}] %   "
          f"p binomial exact (> hasard) = {bt.pvalue:.4g}", flush=True)

    # --- DIFFERENCE APPARIEE jumeau - B-demo, memes personnes ---------------
    nom_bdemo = "B-demo (4 variables demographiques, LOO k=10)"
    nom_orac = "B-oracle (11 vraies reponses, LOO k=10)"
    for cle in ("en_faveur", "uniforme", "contre"):
        d = indic[principal][cle] - indic[nom_bdemo][cle]
        m, b, hh = ic_personnes(d, f"1c|diff|{cle}")
        lignes.append(ligne(
            volet, "Argyle 2023", f"{principal} moins B-demo", "naif (Hamming)",
            f"difference_appariee_points_{cle}", m * 100.0, b * 100.0, hh * 100.0,
            n_attaques=n, n_pool=n, convention=cle,
            note="difference APPARIEE personne par personne, baseline recalculee sur "
                 "ce bassin ; en POINTS de pourcentage"))
        print(f"    difference appariee jumeau - B-demo ({cle:9s}) = "
              f"{m*100:+.4f} pt  IC95 [{b*100:+.4f} ; {hh*100:+.4f}]", flush=True)

    d_or = indic[principal]["uniforme"] - indic[nom_orac]["uniforme"]
    m, b, hh = ic_personnes(d_or, "1c|diff|oracle")
    lignes.append(ligne(
        volet, "Argyle 2023", f"{principal} moins B-oracle", "naif (Hamming)",
        "difference_appariee_points_uniforme", m * 100.0, b * 100.0, hh * 100.0,
        n_attaques=n, n_pool=n,
        note="R13 : le plus proche voisin qui detient les 11 memes vraies reponses"))
    print(f"    difference appariee jumeau - B-oracle (uniforme) = {m*100:+.4f} pt  "
          f"IC95 [{b*100:+.4f} ; {hh*100:+.4f}]", flush=True)
    return indic, principal, nom_bdemo, nom_orac, n


def volet_1c_bis_twin(lignes):
    """AJOUT DECLARE, hors du tableau §1c du plan.

    R1 geste 4 se termine par « a 60 items la classe mediane vaut 1 et la metrique est
    saine ». Cette phrase porte sur Twin-2K-500 a 60 items, pas sur Argyle, et AUCUN
    volet du plan ne la produit. Sans elle, la correction R1 geste 4 resterait a moitie
    non sourcee. Elle est donc mesuree ici, avec la MEME definition de classe d'ex
    aequo qu'au §1c, et signalee comme un ajout au plan.
    """
    print("\n" + "=" * 78, flush=True)
    print("§1c bis (AJOUT DECLARE)  TWIN-2K-500 A 60 ITEMS : classes d'ex aequo",
          flush=True)
    print("=" * 78, flush=True)
    volet = "1c bis ex aequo a 60 items (Twin, ajout hors plan)"

    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    n = pool.shape[0]
    couverts = np.flatnonzero((codes[CIBLE_TWIN] >= 0).any(axis=1))
    print(f"  bassin : {n} personnes, {len(items)} items communs, "
          f"{len(couverts)} jumeaux couverts", flush=True)

    # CONTROLE CANONIQUE, avant interpretation
    try:
        d = CTL.controle_avant_interpretation(couverts, items,
                                              codes[CIBLE_TWIN][couverts][:, items],
                                              CIBLE_TWIN, paq=paq)
        passe = True
    except CTL.EchecControleInterpretabilite as exc:
        d, passe = exc.diagnostic, False
    lignes.append(ligne(
        volet, "Twin-2K-500", CIBLE_TWIN, "naif (Hamming)",
        "controle_interpretabilite_passe", float(passe),
        d["candidat_ic"][0], d["candidat_ic"][1], n_pool=n, n_items=len(items),
        candidat_top1=d["candidat_top1"], baseline_top1=d["baseline_top1"],
        baseline_ic_bas=d["baseline_ic"][0], baseline_ic_haut=d["baseline_ic"][1],
        hasard=d["hasard"], note="fonction canonique du depot"))
    print(f"    controle {'PASSE' if passe else 'ECHEC'} : candidat "
          f"{d['candidat_top1']*100:.4f} % vs baseline "
          f"{d['baseline_top1']*100:.4f} %", flush=True)

    for nom, mat in ((CIBLE_TWIN, codes[CIBLE_TWIN]), (DEMO, codes[DEMO])):
        acc = 1.0 - distance_hamming(mat[couverts][:, items], pool)
        c = conventions_de_departage(acc, couverts)
        commun = dict(n_attaques=len(couverts), n_items=len(items))
        for cle, etiquette in (
                ("en_faveur", "top1_ex_aequo_en_faveur_de_l_attaquant"),
                ("uniforme", "top1_esperance_departage_uniforme_PUBLIE"),
                ("contre", "top1_ex_aequo_contre_l_attaquant")):
            m, b, hh = ic_personnes(c[cle], f"1cbis|{nom}|{cle}")
            lignes.append(ligne(volet, "Twin-2K-500", nom, "naif (Hamming)", etiquette,
                                m, b, hh, n_pool=n, hasard=1.0 / n, **commun))
        publier_classes(lignes, volet, "Twin-2K-500", nom, "naif (Hamming)", c, n,
                        n_items=len(items))
        print(f"    {nom:44s} en faveur {c['en_faveur'].mean()*100:.4f} %  | "
              f"uniforme {c['uniforme'].mean()*100:.4f} %  | "
              f"contre {c['contre'].mean()*100:.4f} %", flush=True)


# ---------------------------------------------------------------------------
# §1d et §1g -- le monde ouvert : un seul chargement par jeu, bassin constant
# ---------------------------------------------------------------------------

def escalier(marge_p, correct, marge_r, n):
    """Fonction ROC en escalier exacte : aucun tri instable, aucune interpolation.

    Renvoie, par FPR cible, le plus grand TPR dont le FPR reste <= cible, le nombre de
    faux positifs et de vraies detections ABSOLUS a ce seuil, le nombre de seuils
    distincts a moins de 1,5 faux positif de la cible, et l'etendue des TPR admissibles
    sur ces seuils.
    """
    seuils = np.unique(np.concatenate([marge_p, marge_r]))
    tp_tries = np.sort(marge_p[correct >= 0.5])
    fp_tries = np.sort(marge_r)
    tp_abs = compte_au_moins(tp_tries, seuils)
    fp_abs = compte_au_moins(fp_tries, seuils)
    tpr, fpr = tp_abs / n, fp_abs / n
    out = {}
    for cible in FPR_CIBLES:
        ok = fpr <= cible
        if not ok.any():
            out[cible] = None
            continue
        j = int(np.argmax(np.where(ok, tpr, -1.0)))
        proches = np.abs(fpr - cible) < 1.5 / n
        t = tpr[proches]
        out[cible] = {
            "tpr_escalier": float(tpr[j]), "fpr_atteint": float(fpr[j]),
            "fp_absolus": int(fp_abs[j]), "vraies_detections_absolues": int(tp_abs[j]),
            "granularite_un_fp": 1.0 / n,
            "n_seuils_a_moins_de_1_5_fp": int(proches.sum()),
            "tpr_admissible_min": float(t.min()) if proches.any() else np.nan,
            "tpr_admissible_max": float(t.max()) if proches.any() else np.nan,
            "tpr_admissible_etendue": float(t.max() - t.min()) if proches.any() else np.nan,
        }
    return out


def charger_park():
    """Bassin, pool et conditions de l'archive Park -- calcules UNE fois."""
    ordre, items, tables, _ = CS.charger_domaine("gss")
    codes = CS.coder_categoriel_commun(tables, items)
    pool = codes[CS.VAGUE1]
    n = pool.shape[0]
    vrai_idx = np.arange(n)
    # verification que le chargeur canonique du monde ouvert donne le MEME objet
    xr, pr, vr = MO.charger_stanford()
    if not (np.array_equal(codes[CIBLE_STAN], xr) and np.array_equal(pool, pr)
            and np.array_equal(vrai_idx, vr)):
        raise SystemExit("Park : le bassin differe de c7_fort_monde_ouvert_ic."
                         "charger_stanford. Tout le volet serait invalide.")
    demo = pd.read_csv(CS.DEMO_CSV).set_index("email").loc[ordre]
    demo_codes = en_codes(demo[["gender", "race", "age", "education"]]
                          .astype(str).to_numpy(dtype=object))
    pmm = pmm_depuis_demo(demo_codes, pool, np.random.default_rng([GRAINE, 31]))
    return {
        "jeu": "Park GSS", "pool": pool, "vrai_idx": vrai_idx, "n": n,
        "n_items": pool.shape[1], "etiquette_llr": "stan|llr",
        "accord": lambda x: CS.accord_categoriel(x, pool),
        "cible": (f"Meilleur agent ({CIBLE_STAN})", codes[CIBLE_STAN]),
        "comparateurs": [("comparateur demographique", codes[CS.DEMO_COND]),
                         ("PMM k=10 (ajout declare)", pmm)],
    }


def charger_twin():
    """Bassin, pool et conditions de Twin-2K-500 -- calcules UNE fois."""
    paq = T1.charger()
    codes = paq["codes"]
    items = items_communs(codes, [REF_V4, REF_V13])
    pool = codes[REF_V4][:, items]
    n = pool.shape[0]
    couverts = np.flatnonzero((codes[CIBLE_TWIN] >= 0).any(axis=1))
    xr, pr, cr = MO.charger_twin()
    if not (np.array_equal(codes[CIBLE_TWIN][:, items][couverts], xr)
            and np.array_equal(pool, pr) and np.array_equal(couverts, cr)):
        raise SystemExit("Twin : le bassin differe de c7_fort_monde_ouvert_ic."
                         "charger_twin. Tout le volet serait invalide.")
    demo_codes = en_codes(paq["demo"]["x"])
    pmm = pmm_depuis_demo(demo_codes, pool, np.random.default_rng([GRAINE, 32]))
    return {
        "jeu": "Twin", "pool": pool, "vrai_idx": couverts, "n": n,
        "n_items": len(items), "etiquette_llr": "twin|llr",
        "accord": lambda x: 1.0 - distance_hamming(x, pool),
        "cible": (CIBLE_TWIN, codes[CIBLE_TWIN][:, items][couverts]),
        "comparateurs": [("comparateur demographique", codes[DEMO][:, items][couverts]),
                         ("PMM k=10 (ajout declare)", pmm[couverts])],
    }


def mesurer_monde_ouvert(jd, nom, x, attaque, lignes, volet):
    """Une condition, une attaque, sur le bassin et le pool DEJA fixes par jd."""
    pool, vrai_idx, n = jd["pool"], jd["vrai_idx"], jd["n"]
    if x.shape[0] != len(vrai_idx) or x.shape[1] != pool.shape[1]:
        raise SystemExit(f"{jd['jeu']}/{nom} : forme {x.shape} incompatible avec le "
                         f"bassin ({len(vrai_idx)}, {pool.shape[1]}).")
    if attaque.startswith("A-LLR"):
        score = scores_hors_pli(x, pool, vrai_idx, f"{jd['etiquette_llr']}")
    else:
        score = jd["accord"](x)
    rng_f = np.random.default_rng([GRAINE, 41, graine_nom(nom + attaque)])
    _, t1, t10 = CS.rangs_depuis_accord(score, vrai_idx, rng_f, 20)
    m1, b1, h1 = ic_personnes(t1, f"mo|{jd['jeu']}|{nom}|{attaque}|top1")
    rng_o = np.random.default_rng([GRAINE, 42, graine_nom(nom + attaque)])
    mp, correct, mr = marges_deux_regimes(score, vrai_idx, rng_o)
    r = roc_et_taux(mp, correct, mr, n)
    esc = escalier(mp, correct, mr, n)

    commun = dict(n_attaques=len(vrai_idx), n_pool=n, n_items=jd["n_items"],
                  hasard=1.0 / n)
    lignes.append(ligne(volet, jd["jeu"], nom, attaque, "top1_monde_ferme", m1, b1, h1,
                        **commun))
    lignes.append(ligne(volet, jd["jeu"], nom, attaque, "auc_monde_ouvert",
                        float(r["auc"]), **commun))
    for cible in FPR_CIBLES:
        et = f"{cible*100:g}pct".replace(".", "_")
        pub = r["tpr_fpr_0_1pct"] if cible == 0.001 else r["tpr_fpr_1pct"]
        lignes.append(ligne(volet, jd["jeu"], nom, attaque,
                            f"tpr_a_fpr_{et}_np_interp_PUBLIE", float(pub),
                            fpr_cible=cible, **commun))
        e = esc[cible]
        if e is None:
            continue
        for k, v in e.items():
            lignes.append(ligne(volet, jd["jeu"], nom, attaque,
                                f"tpr_a_fpr_{et}_{k}", v, fpr_cible=cible, **commun))
    print(f"    {nom:32s} / {attaque:18s} ferme={m1*100:7.4f} % "
          f"[{b1*100:.4f};{h1*100:.4f}]  AUC={r['auc']:.4f}", flush=True)
    for cible in FPR_CIBLES:
        e = esc[cible]
        pub = r["tpr_fpr_0_1pct"] if cible == 0.001 else r["tpr_fpr_1pct"]
        if e is None:
            print(f"      FPR<={cible*100:g}% : aucun seuil admissible ; "
                  f"np.interp {pub*100:.4f} %", flush=True)
            continue
        print(f"      FPR<={cible*100:g}% : escalier {e['tpr_escalier']*100:7.4f} % "
              f"({e['fp_absolus']} FP abs., {e['vraies_detections_absolues']} vraies "
              f"det.) | np.interp {pub*100:7.4f} % | {e['n_seuils_a_moins_de_1_5_fp']} "
              f"seuils a <1,5 FP, TPR de {e['tpr_admissible_min']*100:.4f} a "
              f"{e['tpr_admissible_max']*100:.4f} %", flush=True)
    return {"top1": m1, "top1_bas": b1, "top1_haut": h1, "auc": r["auc"],
            "interp": {0.001: r["tpr_fpr_0_1pct"], 0.01: r["tpr_fpr_1pct"]},
            "escalier": esc}


def temoin_permutation(jd, nom, x, lignes, volet, n_perm=5):
    """Temoin de permutation : le lien personne-a-personne est casse, rien d'autre.

    Necessaire des lors qu'un comparateur cesse d'etre au bruit sous A-LLR : il faut
    pouvoir distinguer « ce comparateur porte vraiment de l'identite individuelle » de
    « le cablage fuit ». Les lignes du candidat sont permutees, le pool, les items,
    l'attaque, les plis et le protocole restant identiques. Si le top-1 s'effondre au
    hasard, le signal est reel ; s'il tient, c'est le cablage qui fuit.

    Ce sont des tirages d'une LOI NULLE. Les colonnes portent temoin_permutation_* et
    ne sont JAMAIS lues comme un intervalle de confiance.
    """
    pool, vrai_idx, n = jd["pool"], jd["vrai_idx"], jd["n"]
    rng = np.random.default_rng([GRAINE, 43, graine_nom(jd["jeu"] + nom)])
    vals = []
    for t in range(n_perm):
        s = scores_hors_pli(x[rng.permutation(x.shape[0])], pool, vrai_idx,
                            jd["etiquette_llr"])
        r = np.random.default_rng([GRAINE, 44, t])
        _, t1, _ = CS.rangs_depuis_accord(s, vrai_idx, r, 20)
        vals.append(float(t1.mean()))
    vals = np.asarray(vals)
    lignes.append(ligne(
        volet, jd["jeu"], nom, "A-LLR (hors pli)",
        "temoin_permutation_lignes_top1_monde_ferme", float(vals.mean()),
        n_attaques=len(vrai_idx), n_pool=n, n_items=jd["n_items"], hasard=1.0 / n,
        n_permutations=n_perm,
        temoin_permutation_min=float(vals.min()),
        temoin_permutation_max=float(vals.max()),
        note="tirages d'une LOI NULLE (lien personne-a-personne casse, tout le reste "
             "identique), PAS un intervalle de confiance"))
    print(f"      temoin de permutation ({n_perm} tirages) : top-1 A-LLR "
          f"{vals.mean()*100:.4f} % [{vals.min()*100:.4f}-{vals.max()*100:.4f}] "
          f"contre un hasard de {100.0/n:.4f} %", flush=True)


def volets_1d_1g(lignes):
    """§1d (la cible, valeur en escalier) et §1g (le comparateur sous A-LLR).

    Les deux volets partagent un SEUL chargement par jeu : c'est la seule facon de
    garantir que le comparateur de §1g est mesure sur exactement le bassin, le pool et
    les items de la cible de §1d. Le top-1 en depend mecaniquement.
    """
    print("\n" + "=" * 78, flush=True)
    print("§1d + §1g  MONDE OUVERT : valeur en escalier (cible) et comparateurs sous "
          "A-LLR", flush=True)
    print("=" * 78, flush=True)
    v1d = "1d TPR en escalier"
    v1g = "1g comparateurs en monde ouvert sous A-LLR"

    for charger in (charger_park, charger_twin):
        jd = charger()
        print(f"\n  --- {jd['jeu']} : {jd['n']} personnes, {jd['n_items']} items, "
              f"bassin unique partage par toutes les conditions ---", flush=True)
        nom_cible, x_cible = jd["cible"]

        print("  [cible]", flush=True)
        res_naif = mesurer_monde_ouvert(jd, nom_cible, x_cible, "naif (Hamming)",
                                        lignes, v1d)
        res_fort = mesurer_monde_ouvert(jd, nom_cible, x_cible, "A-LLR (hors pli)",
                                        lignes, v1d)
        verifier_raccordement(f"{jd['jeu']}|monde ferme A-LLR", res_fort["top1"])
        verifier_raccordement(f"{jd['jeu']}|tpr_fpr_1pct A-LLR", res_fort["interp"][0.01])
        verifier_raccordement(f"{jd['jeu']}|tpr_fpr_0_1pct A-LLR",
                              res_fort["interp"][0.001])
        temoin_permutation(jd, nom_cible, x_cible, lignes, v1d)

        print("  [comparateurs -- R15 : le meme traitement que la cible]", flush=True)
        for nom_c, x_c in jd["comparateurs"]:
            r_n = mesurer_monde_ouvert(jd, nom_c, x_c, "naif (Hamming)", lignes, v1g)
            r_f = mesurer_monde_ouvert(jd, nom_c, x_c, "A-LLR (hors pli)", lignes, v1g)
            temoin_permutation(jd, nom_c, x_c, lignes, v1g)
            # raccordement : le CSV publie donne ces comparateurs a 0,0000 % en naif
            for cible in FPR_CIBLES:
                et = f"{cible*100:g}pct".replace(".", "_")
                lignes.append(ligne(
                    v1g, jd["jeu"], nom_c, "naif -> A-LLR",
                    f"ecart_tpr_a_fpr_{et}_fort_moins_naif",
                    float(r_f["interp"][cible] - r_n["interp"][cible]),
                    fpr_cible=cible, n_pool=jd["n"], tpr_naif=r_n["interp"][cible],
                    tpr_fort=r_f["interp"][cible],
                    note="R15 : le comparateur n'avait jamais ete rejoue sous A-LLR"))
            # meme regle de decision qu'ailleurs, en MONDE FERME (seul endroit ou
            # l'indicatrice par personne existe), candidat et comparateur sous A-LLR
            passe = bool(res_fort["top1_bas"] > r_f["top1_haut"])
            lignes.append(ligne(
                v1g, jd["jeu"], f"{nom_cible} vs {nom_c}", "A-LLR (hors pli)",
                "controle_interpretabilite_passe", float(passe),
                res_fort["top1_bas"], res_fort["top1_haut"], n_pool=jd["n"],
                candidat_top1=res_fort["top1"], baseline_top1=r_f["top1"],
                baseline_ic_bas=r_f["top1_bas"], baseline_ic_haut=r_f["top1_haut"],
                hasard=1.0 / jd["n"],
                note="meme regle de decision que c7_controle_interpretabilite, "
                     "candidat ET comparateur sous la MEME attaque et le MEME bassin ; "
                     "en monde ferme, seul regime ou l'indicatrice par personne existe"))
            print(f"      controle (monde ferme, tous deux sous A-LLR) : "
                  f"{'PASSE' if passe else 'ECHEC'}", flush=True)


# ---------------------------------------------------------------------------
# §1e -- Spearman n = 12 : bootstrap sur les PAIRES
# ---------------------------------------------------------------------------

def volet_1e(lignes):
    print("\n" + "=" * 78, flush=True)
    print("§1e  SPEARMAN n = 12 : bootstrap sur les paires, Fisher-z, permutation",
          flush=True)
    print("=" * 78, flush=True)
    volet = "1e IC du Spearman a n = 12"

    d = pd.read_csv(os.path.join(T1.SORTIE, "c7-compromis.csv"))
    x = d["fidelite_plancher"].to_numpy(dtype=float)
    y = d["fuite_top1"].to_numpy(dtype=float)
    n = len(x)
    rho = float(stats.spearmanr(x, y).statistic)
    print(f"  {n} configurations ; rho observe = {rho:.6f}", flush=True)
    verifier_raccordement("rho Spearman 12 configurations", rho)
    commun = dict(n_paires=n, n_pool=np.nan)
    lignes.append(ligne(volet, "Twin-2K-500", "12 configurations", "-",
                        "rho_spearman_observe", rho, **commun))

    # publie : bootstrap sur les PERSONNES, les 12 configurations figees
    lignes.append(ligne(
        volet, "Twin-2K-500", "12 configurations", "-",
        "rho_ic_publie_bootstrap_sur_les_personnes",
        float(d["rho_spearman_fidelite_fuite"].iloc[0]),
        float(d["rho_ic_bas"].iloc[0]), float(d["rho_ic_haut"].iloc[0]), **commun,
        note="valeur PUBLIEE : reechantillonne les personnes A L'INTERIEUR de chaque "
             "configuration, les 12 configurations et l'axe de fidelite restant figes"))

    # (1) bootstrap sur les PAIRES : l'unite est la configuration
    rng = np.random.default_rng([GRAINE, 51])
    vals, degeneres = [], 0
    for _ in range(N_BOOT_RHO):
        i = rng.integers(0, n, n)
        if len(np.unique(i)) < 3:
            degeneres += 1
            continue
        with np.errstate(all="ignore"):
            r = stats.spearmanr(x[i], y[i]).statistic
        if np.isfinite(r):
            vals.append(float(r))
        else:
            degeneres += 1
    vals = np.asarray(vals)
    b, hh = np.percentile(vals, [2.5, 97.5])
    part_un = float((vals >= 1.0 - 1e-9).mean())
    lignes.append(ligne(
        volet, "Twin-2K-500", "12 configurations", "-",
        "rho_ic_bootstrap_sur_les_paires", rho, float(b), float(hh), **commun,
        n_tirages=N_BOOT_RHO, n_tirages_degeneres=degeneres,
        part_tirages_rho_egal_1=part_un,
        note="unite de reechantillonnage = la CONFIGURATION ; tirages degeneres "
             "(< 3 configurations distinctes) ecartes et comptes, jamais remplaces"))
    print(f"  bootstrap sur les paires : [{b:.4f} ; {hh:.4f}]  "
          f"({degeneres} tirages degeneres ecartes ; "
          f"{part_un*100:.2f} % des tirages donnent rho = 1,000)", flush=True)

    # (2) Fisher-z : Bonett-Wright (propre au Spearman) et version naive
    z = np.arctanh(rho)
    for etiq, se in (("bonett_wright", np.sqrt(1.06 / (n - 3))),
                     ("naif_1_sur_racine_n_moins_3", 1.0 / np.sqrt(n - 3))):
        lo, hi = np.tanh([z - 1.96 * se, z + 1.96 * se])
        lignes.append(ligne(volet, "Twin-2K-500", "12 configurations", "-",
                            f"rho_ic_fisher_z_{etiq}", rho, float(lo), float(hi),
                            ecart_type_z=float(se), **commun))
        print(f"  Fisher-z ({etiq:28s}) : [{lo:.4f} ; {hi:.4f}]", flush=True)

    # (3) permutation : une LOI NULLE, pas un intervalle de confiance
    rngp = np.random.default_rng([GRAINE, 52])
    nuls = np.empty(N_PERMUTATIONS)
    for k in range(N_PERMUTATIONS):
        nuls[k] = stats.spearmanr(x, rngp.permutation(y)).statistic
    p = (int((np.abs(nuls) >= abs(rho)).sum()) + 1) / (N_PERMUTATIONS + 1)
    q = np.percentile(nuls, [2.5, 50, 97.5])
    lignes.append(ligne(
        volet, "Twin-2K-500", "12 configurations", "-",
        "rho_permutation_p_bilateral", float(p), **commun,
        n_permutations=N_PERMUTATIONS,
        percentile_loi_nulle_2_5=float(q[0]), percentile_loi_nulle_50=float(q[1]),
        percentile_loi_nulle_97_5=float(q[2]),
        note="percentiles d'une LOI NULLE sous permutation -- ce ne sont PAS des "
             "bornes d'intervalle de confiance et ils ne sont pas dans ic_bas/ic_haut"))
    print(f"  permutation ({N_PERMUTATIONS} tirages) : p bilateral = {p:.5f} ; "
          f"loi nulle, percentiles 2,5/50/97,5 = "
          f"{q[0]:.4f} / {q[1]:.4f} / {q[2]:.4f}", flush=True)


# ---------------------------------------------------------------------------
# §1f -- Le 36,4 % : bootstrap en grappes par configuration
# ---------------------------------------------------------------------------

def volet_1f(lignes):
    print("\n" + "=" * 78, flush=True)
    print("§1f  36,4 % A 60 ITEMS : bootstrap en grappes par configuration", flush=True)
    print("=" * 78, flush=True)
    volet = "1f intervalle en grappes du 36,4 %"

    d = pd.read_csv(os.path.join(T1.SORTIE, "c7-transfert-voletA.csv"))
    s = d[(d.n_items == 60) & (d.config_x != DEMO) & (d.config_y != DEMO)] \
        .reset_index(drop=True)
    v = s["top1"].to_numpy(dtype=float)
    ctrl = float(s["top1_controle"].mean())
    cfg = sorted(set(s.config_x) | set(s.config_y))
    K = len(cfg)
    moy = float(v.mean())
    print(f"  {len(v)} paires ordonnees issues de {K} configurations ; "
          f"moyenne {moy*100:.4f} % ; temoin anti-artefact {ctrl*100:.4f} %", flush=True)
    verifier_raccordement("moyenne 30 paires a 60 items", moy)
    verifier_raccordement("temoin anti-artefact 30 paires", ctrl)

    commun = dict(n_paires=len(v), n_configurations=K, n_items=60)
    lignes.append(ligne(volet, "Twin-2K-500", "30 paires a 60 items", "naif (Hamming)",
                        "top1_moyen_sans_intervalle_PUBLIE", moy, **commun,
                        note="le seul chiffre du resume sans intervalle (R12)"))
    lignes.append(ligne(volet, "Twin-2K-500", "30 paires a 60 items", "naif (Hamming)",
                        "temoin_anti_artefact_moyen", ctrl, **commun))
    for m, val in (("top1_min", v.min()), ("top1_max", v.max()),
                   ("top1_q25", np.percentile(v, 25)),
                   ("top1_mediane", np.median(v)),
                   ("top1_q75", np.percentile(v, 75)),
                   ("top1_ecart_type", v.std(ddof=1)),
                   ("top1_etendue", v.max() - v.min())):
        lignes.append(ligne(volet, "Twin-2K-500", "30 paires a 60 items",
                            "naif (Hamming)", m, float(val), **commun))
    print(f"  etendue {v.min()*100:.3f} - {v.max()*100:.3f} % ; ecart-type "
          f"{v.std(ddof=1)*100:.3f} pts ; mediane {np.median(v)*100:.3f} %", flush=True)

    ci = {c: k for k, c in enumerate(cfg)}
    gx = s.config_x.map(ci).to_numpy()
    gy = s.config_y.map(ci).to_numpy()

    def boot_naif(graine):
        rr = np.random.default_rng([graine, 61])
        idx = rr.integers(0, len(v), (N_BOOT_GRAPPES, len(v)))
        return np.percentile(v[idx].mean(axis=1), [2.5, 97.5])

    def boot_grappes_x(graine):
        rr = np.random.default_rng([graine, 62])
        groupes = [np.flatnonzero(gx == k) for k in range(K)]
        out = np.empty(N_BOOT_GRAPPES)
        for t in range(N_BOOT_GRAPPES):
            out[t] = v[np.concatenate([groupes[j] for j in rr.integers(0, K, K)])].mean()
        return np.percentile(out, [2.5, 97.5])

    def boot_grappes_bi(graine):
        """Les DEUX extremites sont des grappes : on tire K configurations avec remise
        et on reconstruit toutes les paires ordonnees qu'elles engendrent (une paire
        est ponderee par le produit des multiplicites de ses deux bouts). C'est la
        seule definition qui traite la configuration comme l'unite independante des
        deux cotes, ce que le §5.4 du manuscrit exige lui-meme."""
        rr = np.random.default_rng([graine, 63])
        out = []
        for _ in range(N_BOOT_GRAPPES):
            cnt = np.bincount(rr.integers(0, K, K), minlength=K)
            w = cnt[gx] * cnt[gy]
            if w.sum():
                out.append(float(np.average(v, weights=w)))
        return np.percentile(out, [2.5, 97.5])

    definitions = [
        ("intervalle_bootstrap_naif_sur_les_paires", boot_naif,
         "ignore la dependance : chaque configuration apparait dans 10 des 30 paires"),
        ("intervalle_bootstrap_grappes_par_config_x", boot_grappes_x,
         "grappe = l'extremite d'attaque seulement ; sous-estime encore la dependance"),
        ("intervalle_bootstrap_grappes_deux_extremites", boot_grappes_bi,
         "A PUBLIER : la configuration est l'unite independante des DEUX cotes"),
    ]
    for nom, fonction, note in definitions:
        b, hh = fonction(GRAINE)
        lignes.append(ligne(volet, "Twin-2K-500", "30 paires a 60 items",
                            "naif (Hamming)", nom, moy, float(b), float(hh),
                            **commun, n_tirages=N_BOOT_GRAPPES, graine=GRAINE,
                            note=note))
        print(f"  {nom:48s} [{b*100:.2f} ; {hh*100:.2f}]", flush=True)

    # sensibilite Monte-Carlo declaree : a 6 grappes la loi est tres discrete
    bornes = np.array([boot_grappes_bi(g) for g in GRAINES_SENSIBILITE])
    lignes.append(ligne(
        volet, "Twin-2K-500", "30 paires a 60 items", "naif (Hamming)",
        "sensibilite_monte_carlo_grappes_deux_extremites", moy,
        float(bornes[:, 0].min()), float(bornes[:, 1].max()), **commun,
        n_graines=len(GRAINES_SENSIBILITE),
        borne_basse_min=float(bornes[:, 0].min()), borne_basse_max=float(bornes[:, 0].max()),
        borne_haute_min=float(bornes[:, 1].min()), borne_haute_max=float(bornes[:, 1].max()),
        note="enveloppe sur 5 graines : a 6 grappes la loi de reechantillonnage est "
             "tres discrete et les percentiles sautent. Aucune graine n'a ete choisie "
             "pour rapprocher un resultat de celui du relecteur"))
    print(f"  sensibilite a la graine (5 graines) : borne basse "
          f"{bornes[:,0].min()*100:.2f}-{bornes[:,0].max()*100:.2f} %, borne haute "
          f"{bornes[:,1].min()*100:.2f}-{bornes[:,1].max()*100:.2f} %", flush=True)


# ---------------------------------------------------------------------------

def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    lignes = []
    volet_1c(lignes)
    volet_1c_bis_twin(lignes)
    volets_1d_1g(lignes)
    volet_1e(lignes)
    volet_1f(lignes)

    T1.ecrire(pd.DataFrame(lignes), "c7-t1a-complements.csv")
    print("\n" + "=" * 78, flush=True)
    if _ecarts_raccordement:
        print("ECARTS DE RACCORDEMENT (rapportes tels quels, rien n'a ete ajuste) :",
              flush=True)
        for cle, mes, att in _ecarts_raccordement:
            print(f"  {cle} : mesure {mes:.6f} contre {att:.6f} publie", flush=True)
    else:
        print("Toutes les verifications de raccordement passent.", flush=True)
    print("RAPPEL : ces cinq volets sont POST HOC et NON PREENREGISTRES. Ils ont ete "
          "construits\napres le debut des revisions et ne comptent dans aucun "
          "denominateur de multiplicite\npreenregistre.", flush=True)


if __name__ == "__main__":
    main()
