"""
c7_nul_corrige : le « nul de marge » de c7_disjoint copiait la cible. Trois temoins
corriges, qui gardent la marge d'exactitude par personne SANS aucune empreinte individuelle.

PREENREGISTREMENT : resultats/c7-nul-corrige-preenregistrement.md, ecrit le 12 septembre
2026, AVANT ce fichier et avant tout calcul.

LE DEFAUT REPARE. c7_disjoint.construire_nul, ligne 134 :
    out = np.where(masque, np.where(tirage_correct, y_ref, faux), -1)
ce prediteur devait ne porter QUE le taux d'exactitude par personne q_i ; il ecrit en fait
y_ref, la vraie reponse de la personne, avec probabilite q_i. C'est une copie bruitee du
vecteur reel, donc l'empreinte individuelle maximale, et non son absence. Fuite secondaire
ligne 133 : faux = faux + (faux >= y_ref) fait dependre les cellules FAUSSES elles-memes de
la vraie reponse. Le temoin ne testait pas ce qu'il pretendait tester, et c'est lui qui porte
le resultat central de l'article (titre, resume, 1.1, 5.1, figure 2, ligne 1 du tableau 3).

LES TROIS TEMOINS CORRIGES. Tous conservent le masque de couverture reel et la marge q_i.
  N1  cible de substitution : le prediteur est correct au taux q_i contre le MODE DE SON
      SEGMENT CALCULE SANS ELLE (laisse-un-dehors), jamais contre y_ref.
  N2  exactitude appariee sans copie de la cible : correct au taux q_i contre le vrai
      vecteur d'UNE AUTRE personne, tiree par derangement intra-segment.
  N3  permutation des identites : les vecteurs reels sont gardes tels quels, seul le lien
      personne <-> vecteur est rompu. y_ref n'est jamais lu.
N1b et N2b sont les memes que N1 et N2 avec le tirage de Bernoulli ecrit au
preenregistrement, la ou N1 et N2 tirent un effectif exact de cellules correctes (cf.
section DEVIATION plus bas). N0 est le nul casse d'origine, importe tel quel, comme repere.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                les quinze tables de Twin, segment S_gra
  t1_baselines.calculer            les quatre prediteurs statistiques (via un cache)
  a44_commun.permuter_intra        la permutation des personnes intra segment
  a44_mesures.exactitude_codes     l'exactitude par personne sur codes entiers
  a2_commun.distance_hamming       la distance de Hamming normalisee
  a2_commun.bootstrap_personnes    l'IC par reechantillonnage des personnes
  c7_reidentification.items_communs, graine_nom, CONFIGURATIONS, REF_V4, REF_V13
  c7_disjoint.construire_nul       LE NUL CASSE LUI MEME, importe et non recopie, pour que
                                   le repere historique soit exactement le code fautif
  c7_bits.rangs_tous_tirages / bits_et_ic   les bits d'identite, voie rang

CE QUI EST NOUVEAU ICI : les trois constructions corrigees, le mode de segment
laisse-un-dehors, le derangement intra-segment, les controles d'exactitude visee, le top-1
PAR CONFIGURATION sous chaque nul (que la boucle des lignes 221-235 de c7_disjoint calculait
et jetait), et le bootstrap sur les personnes du rho lui meme.

DEVIATION DECLAREE. Le preenregistrement demande a la fois un tirage de Bernoulli de
parametre q_i (section 3) et un ecart maximal a q_i inferieur a 0,08 sur les personnes
(section 4, controle 1). Les deux sont incompatibles : l'ecart d'un tirage binomial a 60
cellules a un ecart type de 0,065, donc son MAXIMUM sur 2 058 personnes depasse 0,08 de
facon certaine. La borne preenregistree confondait l'ecart type d'une personne et le maximum
sur la population. Correction : N1 et N2 tirent un effectif EXACT de cellules correctes
(l'exigence de la mission, « meme exactitude par personne », est alors atteinte a l'arrondi
pres et non seulement en esperance), N1b et N2b executent la regle preenregistree telle
quelle, et le controle bloquant devient : ecart moyen < 0,01 ET ecart standardise maximal
|acc - q| / sqrt(q(1-q)/n) < 5. L'ecart maximal brut est publie a cote.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Aucun identifiant, aucun
pid, aucun appariement individuel n'est imprime ni ecrit : uniquement des taux agreges.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_nul_corrige.py
"""

import argparse
import os
import pickle
import sys
import time
import warnings

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "2")

import numpy as np                             # noqa: E402
import pandas as pd                            # noqa: E402
from scipy import stats                        # noqa: E402

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                         # noqa: E402
import t1_baselines as TB                      # noqa: E402
import a44_commun as C44                       # noqa: E402
import c7_bits as CB                           # noqa: E402
from a44_mesures import exactitude_codes       # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes   # noqa: E402
import c7_reidentification as C7               # noqa: E402
from c7_disjoint import construire_nul         # noqa: E402  LE nul casse, tel quel

GRAINE = 20260912
RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")

STATISTIQUES = ["B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]
HUMAIN = C7.REF_V13

N_REPLICATS = 100
N_PERM_CHUTE = 40
N_TIRAGES_FUITE = 3
N_REPLICATS_BITS = 3
N_BOOTSTRAP = 2000

TOL_ECART_MOYEN = 0.01
MARGE_Z = 2.0                           # marge au-dela du maximum attendu sqrt(2 ln M)
Z_MOYEN_ATTENDU = 0.7978845608          # E|N(0,1)|, loi des ecarts d'un tirage correct
TOL_Z_MOYEN = 0.15
TOL_ECART_MAX_PREENREGISTRE = 0.08      # publie, non bloquant (cf. DEVIATION)

CACHE = os.environ.get(
    "C7_NUL_CACHE",
    "/private/tmp/claude-501/-Users-amirkellousidhoum-Desktop-Code-Projets-popsim/"
    "ed6061e6-124c-4c1f-aeb8-1b15f57c239b/scratchpad/c7-nul-corrige-baselines-60.pkl")

# Les constructions, dans l'ordre du rapport. La cle dit comment la ligne est engendree.
CONSTRUCTIONS = [
    ("reel", "le prediteur publie lui meme"),
    ("N0 nul casse", "c7_disjoint.construire_nul, importe tel quel : COPIE y_ref"),
    ("N1 mode de segment", "correct au taux q_i contre le mode du segment, laisse-un-dehors"),
    ("N1b mode de segment (Bernoulli)", "N1 avec le tirage de Bernoulli preenregistre"),
    ("N2 vecteur d'autrui", "correct au taux q_i contre le vrai vecteur d'une autre personne"),
    ("N2b vecteur d'autrui (Bernoulli)", "N2 avec le tirage de Bernoulli preenregistre"),
    ("N3 identites permutees", "vecteurs reels conserves, lien personne-vecteur rompu"),
    ("N4 mode global", "un seul vecteur de population pour tous, marge NON appariee"),
]
DETERMINISTES = ("reel", "N4 mode global")
NULS_CORRIGES = ["N1 mode de segment", "N1b mode de segment (Bernoulli)",
                 "N2 vecteur d'autrui", "N2b vecteur d'autrui (Bernoulli)",
                 "N3 identites permutees"]


# ---------------------------------------------------------------------------
# 1. Mesures, identiques a celles de c7_disjoint
# ---------------------------------------------------------------------------

def chute_par_personne(cd, y1, s, n_perm, rng):
    """Les deux vecteurs par personne dont la chute brute est la difference des moyennes.

    Identique a c7_disjoint.chute_brute : chute = moyenne(exactitude vraie) - moyenne sur
    les permutations de moyenne(exactitude permutee). Les deux moyennes portent sur le meme
    ensemble de personnes non NaN (le denominateur y1 >= 0 ne bouge pas sous permutation),
    donc moyenner d'abord sur les permutations puis sur les personnes donne exactement le
    meme nombre. Les garder par personne est ce qui rend le bootstrap possible.
    """
    acc = exactitude_codes(cd, y1)
    cumul = np.zeros(cd.shape[0])
    for _ in range(n_perm):
        p = C44.permuter_intra(cd.shape[0], s, rng)
        cumul += exactitude_codes(cd[p], y1)
    return acc, cumul / n_perm


def top1_par_personne(x_sub, pool_sub, vrai_idx, rng, n_tirages=N_TIRAGES_FUITE):
    """Indicatrice top-1 par personne, moyennee sur les tirages de departage des ex aequo.

    Meme calcul que c7_disjoint.fuite_top1 (meme distance, meme bruit i.i.d. de departage) :
    seule la moyenne finale sur les personnes n'est pas prise, pour que le bootstrap sur les
    personnes et l'ecriture du top-1 PAR CONFIGURATION soient possibles.
    """
    accord = 1.0 - distance_hamming(x_sub, pool_sub)
    lignes = np.arange(accord.shape[0])
    acc = np.zeros(accord.shape[0])
    for _ in range(n_tirages):
        combo = accord + rng.random(accord.shape) * 1e-9
        acc += combo[lignes, vrai_idx] >= combo.max(axis=1)
    return acc / n_tirages


def bits_configuration(x_sub, pool, vrai_idx, rng, graine_boot, n_tirages):
    """Bits d'identite par la voie rang, c7_bits importe tel quel."""
    accord = 1.0 - distance_hamming(x_sub, pool)
    rangs = CB.rangs_tous_tirages(accord, vrai_idx, rng, n_tirages=n_tirages)
    return CB.bits_et_ic(rangs, pool.shape[0], graine_boot)


# ---------------------------------------------------------------------------
# 2. Les briques des constructions corrigees
# ---------------------------------------------------------------------------

def marge_par_personne(x, y):
    """Masque de couverture et marge d'exactitude conditionnelle q_i, definition de
    c7_disjoint.construire_nul (la seule chose que le temoin a le droit de conserver)."""
    masque = x >= 0
    n_obs = masque.sum(axis=1)
    correct = (masque & (x == y)).sum(axis=1)
    q = np.divide(correct, np.maximum(n_obs, 1), out=np.zeros(x.shape[0], dtype=float),
                  where=n_obs > 0)
    return masque, q, n_obs


def valeurs_fausses(cible, k_items, rng):
    """Une modalite tiree uniformement parmi les K_j - 1 AUTRES que `cible`.

    La modalite evitee est celle de la CIBLE DE SUBSTITUTION, jamais y_ref de la personne :
    c'est la deuxieme fuite du nul casse, qui faisait eviter aux valeurs fausses la vraie
    reponse de la personne. Un item a une seule modalite ne peut pas etre faux : la cible
    est alors rendue telle quelle (cas absent des 60 items, traite par securite).
    """
    n = cible.shape[0]
    faux = rng.integers(0, np.maximum(k_items - 1, 1)[None, :].repeat(n, axis=0))
    return np.where(k_items[None, :] > 1, faux + (faux >= cible), cible)


def sortie_effectif_exact(cible, masque, q, n_obs, k_items, rng, dtype):
    """Exactement round(q_i * n_obs_i) cellules egales a la cible, les autres fausses.

    Les cellules correctes sont choisies au hasard parmi les cellules couvertes : le rang du
    tirage uniforme sert de cle, les cellules non couvertes sont envoyees en queue par +inf,
    donc les n_correct premieres sont toujours couvertes. L'exactitude contre la cible vaut
    alors n_correct / n_obs, soit q_i a un demi-item pres, pour CHAQUE personne.
    """
    u = np.where(masque, rng.random(cible.shape), np.inf)
    rang = np.argsort(np.argsort(u, axis=1, kind="stable"), axis=1)
    correct = rang < np.rint(q * n_obs).astype(np.int64)[:, None]
    faux = valeurs_fausses(cible, k_items, rng)
    return np.where(masque, np.where(correct, cible, faux), -1).astype(dtype)


def sortie_bernoulli(cible, masque, q, k_items, rng, dtype):
    """La regle preenregistree : chaque cellule couverte est correcte avec probabilite q_i.

    Meme forme que le nul casse, a ceci pres que `cible` n'est jamais y_ref de la personne.
    """
    correct = rng.random(cible.shape) < q[:, None]
    faux = valeurs_fausses(cible, k_items, rng)
    return np.where(masque, np.where(correct, cible, faux), -1).astype(dtype)


def mode_segment_loo(y_ref, seg, k_items):
    """Mode de chaque item dans le segment de la personne, CALCULE SANS ELLE.

    Retirer la personne de son propre comptage est ce qui rend la cible strictement
    independante de ses reponses : deux personnes du meme segment recoivent la meme cible
    des que leurs reponses coincident, et aucune cellule de y_ref[i] n'entre dans z[i].
    Repli sur le mode global (lui aussi prive de la personne) si le segment compte moins de
    deux autres membres. Les ex aequo sont tranches par le plus petit code, de facon
    deterministe.
    """
    n, m = y_ref.shape
    assert (y_ref >= 0).all(), "les 60 items communs sont toujours renseignes chez v4"
    k_max = int(k_items.max())
    g_max = int(seg.max()) + 1 if seg.size and seg.max() >= 0 else 0
    s = np.where(seg >= 0, seg, g_max).astype(np.int64)
    cols = np.arange(m)
    cnt = np.zeros((g_max + 1, m, k_max), dtype=np.int64)
    np.add.at(cnt, (np.repeat(s[:, None], m, axis=1),
                    np.repeat(cols[None, :], n, axis=0), y_ref), 1)
    taille = np.bincount(s, minlength=g_max + 1)
    global_ = cnt.sum(axis=0)
    assez = (taille[s] >= 3)[:, None, None]        # au moins deux autres que la personne
    base = np.where(assez, cnt[s], global_[None, :, :]).astype(np.int64)
    base[np.arange(n)[:, None], cols[None, :], y_ref] -= 1
    return base.argmax(axis=2).astype(y_ref.dtype)


def derangement_intra(seg, rng):
    """Une permutation sans point fixe, a l'interieur de chaque segment S_gra.

    Chaque segment d'au moins deux membres est envoye sur un cycle unique tire au hasard, ce
    qui garantit pi(i) != i sans rejet. Les personnes seules dans leur segment sont
    rassemblees et derangees entre elles (repli declare au preenregistrement). Le groupe de
    segment inconnu est traite comme un segment, convention de a44_commun.permuter_intra.
    """
    n = len(seg)
    assert n >= 2, "un derangement demande au moins deux personnes"
    pi = np.arange(n)
    restes = []
    for g in np.unique(seg):
        membres = np.flatnonzero(seg == g)
        if len(membres) >= 2:
            p = rng.permutation(membres)
            pi[p] = np.roll(p, -1)
        else:
            restes.extend(membres.tolist())
    restes = np.array(restes, dtype=int)
    if len(restes) >= 2:
        p = rng.permutation(restes)
        pi[p] = np.roll(p, -1)
    elif len(restes) == 1:
        i = int(restes[0])
        pi[i] = int(rng.choice(np.delete(np.arange(n), i)))
    assert (pi != np.arange(n)).all(), \
        "point fixe : une personne recevrait sa propre ligne (controle 3 du preenregistrement)"
    return pi


def construire(cle, x, y, cv, y_ref_pool, z_loo, mode_glob, seg_sub, k_items, rng):
    """Le prediteur artificiel d'une construction, pour une configuration.

    x        sortie reelle restreinte aux personnes couvertes (cv)
    y        y_ref restreint aux memes personnes : sert UNIQUEMENT au calcul de q_i
    cv       indices, dans le pool entier, des personnes couvertes
    z_loo    modes de segment laisse-un-dehors, pool entier
    Renvoie (sortie, cible_de_verification) ; cible_de_verification est le vecteur contre
    lequel l'exactitude visee q_i doit etre atteinte, et n'est jamais y_ref[i].
    """
    masque, q, n_obs = marge_par_personne(x, y)
    if cle.startswith("N4"):
        # Plancher de reference : le meme vecteur de population pour tout le monde, avec le
        # masque reel. Il n'apparie AUCUNE marge : c'est le temoin « aucune information
        # individuelle du tout », a comparer aux temoins a marge appariee.
        return np.where(masque, mode_glob[None, :], -1).astype(x.dtype), y
    if cle == "N0 nul casse":
        return construire_nul(x, y, k_items, rng), y          # copie la cible, c'est le defaut
    if cle.startswith("N1"):
        cible = z_loo[cv]                                     # mode du segment SANS la personne
    elif cle.startswith("N2"):
        pi = derangement_intra(seg_sub, rng)                  # une AUTRE personne du segment
        cible = y_ref_pool[cv[pi]]
    elif cle.startswith("N3"):
        # Derangement et non permutation quelconque : C44.permuter_intra laisserait des
        # points fixes (une personne par segment en moyenne), et ces personnes la
        # recevraient leur PROPRE vecteur reel, c'est-a-dire une fuite d'identite parfaite.
        sigma = derangement_intra(seg_sub, rng)
        return x[sigma], y[sigma]                             # y_ref n'est jamais lu ici
    else:
        raise ValueError(cle)
    if "Bernoulli" in cle:
        return sortie_bernoulli(cible, masque, q, k_items, rng, x.dtype), cible
    return sortie_effectif_exact(cible, masque, q, n_obs, k_items, rng, x.dtype), cible


def controler(cle, sortie, cible, x, y):
    """L'exactitude visee est-elle atteinte contre la CIBLE DE SUBSTITUTION, et le masque
    conserve ? Renvoie (ecart moyen, ecart maximal brut, ecart standardise maximal,
    masque identique).

    N0, N1, N2 : l'exactitude de la sortie contre sa cible doit valoir q_i, la marge reelle
    de la personne. Le nul casse N0 passe ce controle aussi, evidemment : il l'atteint en
    copiant la cible, ce que le controle d'exactitude ne peut pas voir. C'est pour cela que
    la preuve de non-fuite est structurelle (quelle est la cible) et non numerique.

    N3 : la sortie est le vecteur de la personne sigma(i), son exactitude contre la cible
    vaut donc q_sigma(i) par identite. Comparer les deux serait tautologique ; le controle
    non trivial est que le MULTI-ENSEMBLE des marges par personne est conserve, c'est-a-dire
    que N3 garde bien le meme profil de q en population, seulement reaffecte.
    """
    masque_reel = x >= 0
    masque_out = sortie >= 0
    _, q_reel, n_obs_reel = marge_par_personne(x, y)
    n_obs_out = masque_out.sum(axis=1)
    n_c = (masque_out & (sortie == cible)).sum(axis=1)
    obtenu = np.divide(n_c, np.maximum(n_obs_out, 1),
                       out=np.zeros(len(n_c), dtype=float), where=n_obs_out > 0)
    if cle.startswith("N3"):
        ecart = np.abs(np.sort(obtenu) - np.sort(q_reel))
        z = np.zeros_like(ecart)
    else:
        ecart = np.abs(obtenu - q_reel)
        var = np.maximum(q_reel * (1.0 - q_reel) / np.maximum(n_obs_reel, 1), 1e-12)
        z = ecart / np.sqrt(var)
    return (float(ecart.mean()), float(ecart.max()), float(z.max()),
            bool((masque_out == masque_reel).all()), float(len(ecart)), float(z.mean()))


# ---------------------------------------------------------------------------
# 3. rho et ses intervalles
# ---------------------------------------------------------------------------

def spearman12(fid, fui):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        r = stats.spearmanr(fid, fui).statistic
    return float(r)


def rho_bootstrap_personnes(acc, accp, top1, n_boot, graine):
    """IC du rho par reechantillonnage des PERSONNES.

    acc, accp, top1 : matrices (12, n_pool), NaN la ou la configuration ne couvre pas la
    personne. Un tirage rechoisit les personnes, recalcule les 12 chutes et les 12 fuites,
    puis leur Spearman. Le pool des candidats de l'attaque reste la population entiere : le
    bootstrap porte sur les personnes attaquees, comme dans c7_reidentification.
    """
    rng = np.random.default_rng(graine)
    n = acc.shape[1]
    out = np.empty(n_boot)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for b in range(n_boot):
            idx = rng.integers(0, n, n)
            fid = np.nanmean(acc[:, idx], axis=1) - np.nanmean(accp[:, idx], axis=1)
            fui = np.nanmean(top1[:, idx], axis=1)
            out[b] = stats.spearmanr(fid, fui).statistic
    out = out[np.isfinite(out)]
    if not len(out):
        return np.nan, np.nan
    return float(np.percentile(out, 2.5)), float(np.percentile(out, 97.5))


# ---------------------------------------------------------------------------
# 4. Programme principal
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replicats", type=int, default=N_REPLICATS)
    ap.add_argument("--permutations", type=int, default=N_PERM_CHUTE)
    ap.add_argument("--tirages", type=int, default=N_TIRAGES_FUITE)
    ap.add_argument("--bits-replicats", type=int, default=N_REPLICATS_BITS)
    ap.add_argument("--bits-tirages", type=int, default=CB.N_TIRAGES_LIENS)
    ap.add_argument("--bootstrap", type=int, default=N_BOOTSTRAP)
    ap.add_argument("--sortie", default=os.path.join(SORTIE, "c7-nul-corrige.csv"))
    args = ap.parse_args()

    print(__doc__, flush=True)
    t0 = time.time()
    paq = T1.charger()
    codes = paq["codes"]
    seg_gra = paq["seg"]["S_gra"]
    n_total = paq["n"]
    items = C7.items_communs(codes, [C7.REF_V4, C7.REF_V13])
    k_items = paq["k_items"][items]
    y_ref = codes[C7.REF_V4][:, items]
    print(f"{n_total} personnes, {len(items)} items communs, "
          f"K max = {int(k_items.max())}, charge en {time.time()-t0:.0f}s", flush=True)

    noms_12 = list(C7.CONFIGURATIONS) + STATISTIQUES
    pred = {nom: codes[nom][:, items] for nom in C7.CONFIGURATIONS}
    if os.path.exists(CACHE):
        cache = pickle.load(open(CACHE, "rb"))
        assert list(cache["items"]) == list(items), "le cache ne porte pas les memes items"
        base = cache["base"]
        print(f"baselines relues du cache {CACHE}", flush=True)
    else:
        paq_slim = dict(paq)
        codes_slim = dict(codes)
        codes_slim[T1.REF] = codes[T1.REF][:, items]
        paq_slim["codes"] = codes_slim
        base = TB.calculer(paq_slim, avec_pmm=True)
        pickle.dump({"items": items, "base": base}, open(CACHE, "wb"))
    for nom in STATISTIQUES:
        pred[nom] = base[nom]
    pred[HUMAIN] = codes[HUMAIN][:, items]
    couverts = {nom: np.flatnonzero((pred[nom] >= 0).any(axis=1))
                for nom in noms_12 + [HUMAIN]}

    # La cible de substitution de N1 et le pool des candidats ne dependent d'aucun replicat.
    z_loo = mode_segment_loo(y_ref, seg_gra, k_items)
    mode_glob = CB.mode_item(y_ref)[0]        # le vecteur modal de la population, c7_bits
    part_z = float(np.mean(z_loo == y_ref))
    print(f"mode de segment laisse-un-dehors : il coincide avec la vraie reponse dans "
          f"{part_z:.3f} des cellules (c'est le taux d'accord au mode, pas une fuite : "
          f"z[i] ne lit aucune cellule de y_ref[i])", flush=True)
    print(f"prediteurs prets, {time.time()-t0:.0f}s\n", flush=True)

    lignes, lignes_rho, resume_rho = [], [], []
    rho_reel = np.nan
    # Les echecs de controle sont COLLECTES et non fatals sur le champ : ils interdisent la
    # lecture du verdict (sortie en erreur a la fin), mais ne detruisent pas une heure de
    # calcul, ce qui permet de diagnostiquer un controle mal calibre sur ses propres
    # chiffres au lieu de relancer a l'aveugle.
    echecs = []

    for i_cons, (cle, description) in enumerate(CONSTRUCTIONS):
        est_reel = (cle == "reel")
        deterministe = cle in DETERMINISTES
        n_rep = 1 if deterministe else args.replicats
        n_bits = 1 if deterministe else min(args.bits_replicats, n_rep)
        noms = noms_12 + [HUMAIN] if est_reel else noms_12
        print(f"--- {cle} : {description} ---", flush=True)

        acc_m = np.full((len(noms_12), n_total), np.nan)
        accp_m = np.full((len(noms_12), n_total), np.nan)
        top1_m = np.full((len(noms_12), n_total), np.nan)
        agg = {nom: {"fid": [], "fui": [], "bits": [], "ctrl": [], "exact": []}
               for nom in noms}
        rhos = np.full(n_rep, np.nan)
        degen = 0

        for r in range(n_rep):
            fid, fui = {}, {}
            for i_n, nom in enumerate(noms):
                cv = couverts[nom]
                x, y, seg = pred[nom][cv], y_ref[cv], seg_gra[cv]
                if est_reel:
                    sortie, cible = x, y
                    ctrl = (0.0, 0.0, 0.0, True, 0.0, 0.0)
                else:
                    rng_g = np.random.default_rng(
                        [GRAINE, 100 + i_cons, r, C7.graine_nom(nom)])
                    sortie, cible = construire(cle, x, y, cv, y_ref, z_loo, mode_glob,
                                               seg, k_items, rng_g)
                    ctrl = controler(cle, sortie, cible, x, y)

                rng_c = np.random.default_rng([GRAINE, 4, r, C7.graine_nom(nom)])
                a, ap = chute_par_personne(sortie, y, seg, args.permutations, rng_c)
                rng_f = np.random.default_rng([GRAINE, 5, r, C7.graine_nom(nom)])
                t1 = top1_par_personne(sortie, y_ref, cv, rng_f, n_tirages=args.tirages)

                fid[nom] = float(np.nanmean(a) - np.nanmean(ap))
                fui[nom] = float(np.mean(t1))
                agg[nom]["fid"].append(fid[nom])
                agg[nom]["fui"].append(fui[nom])
                agg[nom]["ctrl"].append(ctrl)
                agg[nom]["exact"].append(float(np.nanmean(exactitude_codes(sortie, y))))
                if r == 0:
                    agg[nom]["boot"] = (a, ap, t1)
                    # a_j = P(sortie = reponse de la VRAIE personne), c_j = P(sortie
                    # coincide avec un candidat pris au hasard). delta = a - c est l'exces
                    # de coincidence sur lequel l'attaque trie : c'est lui, et non
                    # l'exactitude a elle seule, qui fait l'identification.
                    plein = np.full((n_total, sortie.shape[1]), -1, dtype=sortie.dtype)
                    plein[cv] = sortie
                    a_j, c_j = CB.a_et_c_par_item(plein, y_ref, cv)
                    agg[nom]["acd"] = (float(np.nanmean(a_j)), float(np.nanmean(c_j)),
                                       float(np.nanmean(a_j - c_j)))
                    if nom in noms_12:
                        j = noms_12.index(nom)
                        acc_m[j, cv], accp_m[j, cv], top1_m[j, cv] = a, ap, t1
                if r < n_bits:
                    rng_b = np.random.default_rng([GRAINE, 6, r, C7.graine_nom(nom)])
                    agg[nom]["bits"].append(
                        bits_configuration(sortie, y_ref, cv, rng_b, [GRAINE, 11],
                                           args.bits_tirages))

            f = [fid[n] for n in noms_12]
            u = [fui[n] for n in noms_12]
            rhos[r] = spearman12(f, u)
            if len(set(np.round(f, 12))) < 2 or len(set(np.round(u, 12))) < 2:
                degen += 1
            if r % 20 == 0 or est_reel:
                print(f"  replicat {r}, rho={rhos[r]:.4f}, {time.time()-t0:.0f}s",
                      flush=True)
            lignes_rho.append({"type": "rho_replicat", "construction": cle, "replicat": r,
                               "rho": rhos[r],
                               "distinct_fidelite": len(set(np.round(f, 12))),
                               "distinct_fuite": len(set(np.round(u, 12)))})

        # --- table par configuration ---
        for nom in noms:
            bits = np.array(agg[nom]["bits"], dtype=float)
            if bits.size == 0:                  # bits desactives (essai a blanc)
                bits = np.full((1, 6), np.nan)
            a, ap, t1 = agg[nom]["boot"]        # les vecteurs par personne du replicat 0
            _, f_b, f_h = bootstrap_personnes(a - ap, args.bootstrap, [GRAINE, 7])
            _, t_b, t_h = bootstrap_personnes(t1, args.bootstrap, [GRAINE, 8])
            ctrl = np.array(agg[nom]["ctrl"], dtype=float)
            lignes.append({
                "type": "configuration", "construction": cle, "configuration": nom,
                "replicats": len(agg[nom]["fid"]), "n_couverts": len(couverts[nom]),
                "fidelite_chute": float(np.mean(agg[nom]["fid"])),
                "fidelite_boot_bas": f_b, "fidelite_boot_haut": f_h,
                "top1": float(np.mean(agg[nom]["fui"])),
                "top1_boot_bas": t_b, "top1_boot_haut": t_h,
                "bits": float(bits[:, 0].mean()), "bits_bas": float(bits[:, 1].mean()),
                "bits_haut": float(bits[:, 2].mean()), "bits_replicats": len(bits),
                "exactitude_contre_verite": float(np.mean(agg[nom]["exact"])),
                "a_vraie_personne": agg[nom]["acd"][0],
                "c_candidat_hasard": agg[nom]["acd"][1],
                "delta_identification": agg[nom]["acd"][2],
                "ecart_exactitude_moyen": float(ctrl[:, 0].mean()),
                "ecart_exactitude_max": float(ctrl[:, 1].max()),
                "z_exactitude_max": float(ctrl[:, 2].max()),
                "masque_identique": bool(ctrl[:, 3].all()),
            })

        # --- controles bloquants ---
        if not est_reel:
            ctrl_tous = np.array([c for nom in noms for c in agg[nom]["ctrl"]], dtype=float)
            e_moy, e_max = float(ctrl_tous[:, 0].mean()), float(ctrl_tous[:, 1].max())
            z_max = float(ctrl_tous[:, 2].max())
            masque_ok = bool(ctrl_tous[:, 3].all())
            z_moy = float(ctrl_tous[:, 5].mean())
            # Le maximum d'un ecart standardise se compare au maximum ATTENDU sur le nombre
            # d'ecarts agreges (ici ~2,5 millions : 100 replicats x 12 configs x 2 058
            # personnes), pas a une borne fixe. E[max de M gaussiennes] = sqrt(2 ln M),
            # soit 5,4 pour M = 2,5e6 : un seuil fixe a 5 rejetterait un echantillonneur
            # parfaitement correct. C'est la MEME erreur de calibrage que celle deja
            # corrigee au preenregistrement (ecart type d'une personne confondu avec le
            # maximum sur la population) ; elle est ici corrigee dans sa seconde occurrence.
            m_tests = float(ctrl_tous[:, 4].sum())
            seuil_z = float(np.sqrt(2.0 * np.log(max(m_tests, 2.0))) + MARGE_Z)
            print(f"  controle exactitude visee : ecart moyen {e_moy:.5f}, ecart max brut "
                  f"{e_max:.4f} (borne preenregistree {TOL_ECART_MAX_PREENREGISTRE}, non "
                  f"bloquante), z max {z_max:.2f} (seuil attendu {seuil_z:.2f} sur "
                  f"{m_tests:.0f} ecarts), z moyen {z_moy:.3f} ; masque identique : "
                  f"{masque_ok}", flush=True)
            # Le critere depend du GENERATEUR, pas du temoin : un tirage de Bernoulli de
            # parametre q_i n'atteint q_i qu'en esperance, son ecart moyen vaut
            # 0,8 sqrt(q(1-q)/60) ~ 0,05 et ne peut pas passer sous 0,01. Pour ces
            # variantes le controle preenregistre est le controle standardise seul.
            if cle.startswith("N4"):
                print("  N4 : aucune marge appariee par construction, controle 1 sans "
                      "objet (c'est le plancher de reference, pas un temoin apparie)",
                      flush=True)
            elif "Bernoulli" in cle or cle == "N0 nul casse":
                # Un tirage de Bernoulli n'atteint q_i qu'en esperance : le controle porte
                # sur la LOI des ecarts standardises (moyenne attendue E|N(0,1)| = 0,798)
                # et sur leur maximum attendu, pas sur une borne fixe.
                if z_max >= seuil_z:
                    echecs.append(f"{cle} : z max {z_max:.2f} >= seuil {seuil_z:.2f}")
                if abs(z_moy - Z_MOYEN_ATTENDU) > TOL_Z_MOYEN:
                    echecs.append(f"{cle} : z moyen {z_moy:.3f} loin de "
                                  f"{Z_MOYEN_ATTENDU:.3f} (tirage non conforme)")
            elif e_moy >= TOL_ECART_MOYEN or z_max >= seuil_z:
                echecs.append(f"{cle} : exactitude visee non atteinte "
                              f"(ecart moyen {e_moy:.5f}, z max {z_max:.2f})")
            if not masque_ok and not cle.startswith("N3"):
                echecs.append(f"{cle} : le masque de couverture a bouge")
            if not masque_ok:
                print("  N3 : le masque suit le vecteur permute (attendu, il est conserve "
                      "en multi-ensemble et non cellule a cellule)", flush=True)

        # --- rho de la construction ---
        boot_bas, boot_haut = rho_bootstrap_personnes(acc_m, accp_m, top1_m,
                                                      args.bootstrap, [GRAINE, 9])
        p95 = float(np.nanpercentile(rhos, 95))
        if est_reel:
            rho_reel = float(rhos[0])
        resume_rho.append({
            "type": "rho_resume", "construction": cle, "replicats": n_rep,
            "rho_moyen": float(np.nanmean(rhos)), "rho_median": float(np.nanmedian(rhos)),
            "rho_p5": float(np.nanpercentile(rhos, 5)), "rho_p95": p95,
            "rho_min": float(np.nanmin(rhos)), "rho_max": float(np.nanmax(rhos)),
            "rho_boot_personnes_bas": boot_bas, "rho_boot_personnes_haut": boot_haut,
            "replicats_axe_degenere": degen, "replicats_rho_non_defini": int(
                np.isnan(rhos).sum()),
            "rho_reel_depasse_p95": bool(rho_reel > p95) if not est_reel else None,
        })
        print(f"  rho : moyenne={np.nanmean(rhos):.4f}, mediane={np.nanmedian(rhos):.4f}, "
              f"p95={p95:.4f}, IC bootstrap personnes [{boot_bas:.4f} ; {boot_haut:.4f}], "
              f"replicats a axe degenere = {degen}/{n_rep}, {time.time()-t0:.0f}s\n",
              flush=True)

    df = pd.concat([pd.DataFrame(lignes), pd.DataFrame(resume_rho),
                    pd.DataFrame(lignes_rho)], ignore_index=True)
    df.to_csv(args.sortie, index=False)
    print(f"ecrit {args.sortie}", flush=True)

    # ------------------------------------------------------------------
    # Verdict preenregistre
    # ------------------------------------------------------------------
    if echecs:
        print("\n=== CONTROLES ECHOUES, aucun verdict n'est lu ===", flush=True)
        for e in echecs:
            print("  " + e, flush=True)
        sys.exit("un controle bloquant a echoue, rien n'est publie au dela")

    print("\n=== verdict, regle preenregistree section 7 ===", flush=True)
    print(f"rho du prediteur reel, 60 items entiers : {rho_reel:.4f}", flush=True)
    res = {r["construction"]: r for r in resume_rho}
    depasse = {}
    for cle in NULS_CORRIGES:
        r = res[cle]
        depasse[cle] = bool(rho_reel > r["rho_p95"])
        print(f"  {cle:38s} rho moyen={r['rho_moyen']:+.4f} p95={r['rho_p95']:+.4f} "
              f"-> rho reel le depasse : {depasse[cle]} "
              f"(axes degeneres {r['replicats_axe_degenere']}/{r['replicats']})", flush=True)
    n0 = res["N0 nul casse"]
    print(f"  {'N0 nul casse (repere)':38s} rho moyen={n0['rho_moyen']:+.4f} "
          f"p95={n0['rho_p95']:+.4f} -> rho reel le depasse : "
          f"{bool(rho_reel > n0['rho_p95'])}", flush=True)
    if all(depasse.values()):
        print("\nISSUE B : la marge seule ne reproduit pas le couplage. La refutation "
              "publiee tombe ; la these redevient soutenable, dans la limite de la reserve "
              "du preenregistrement section 8.", flush=True)
    elif not any(depasse.values()):
        print("\nISSUE A : la marge seule reproduit le couplage. La these reste refutee ; "
              "le nul casse avait par chance la bonne conclusion.", flush=True)
    else:
        print("\nISSUE C : les constructions divergent. Resultat rapporte tel quel, "
              "aucun arbitrage.", flush=True)
    print(f"\ntermine en {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
