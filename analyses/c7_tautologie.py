"""
c7_tautologie : a exactitude par personne tenue rigoureusement constante, la fuite
varie-t-elle encore selon la STRUCTURE des erreurs ?

===========================================================================
PREENREGISTREMENT : resultats/c7-tautologie-preenregistrement.md, ecrit le 12 septembre
2026, AVANT ce fichier et avant tout calcul.

OBJECTION TRANCHEE ICI : « un jumeau plus exact ressemble plus a la personne, donc il est
forcement plus reconnaissable ; vous n'avez mesure que de l'exactitude renommee en vie
privee ». Le nul de marge de c7_disjoint.py (Bernoulli a la seule marge d'exactitude
CONDITIONNELLE, aucune structure au-dela) renforce deja cette objection (rho 0,984,
au-dessus du rho observe 0,969). Ce script durcit le controle : quatre predicteurs
synthetiques dont le vecteur d'exactitude par personne est identique AU BIT PRES (pas
seulement en esperance), qui ne different que par QUELS items portent la bonne reponse.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                  les quinze tables de Twin
  c7_reidentification.items_communs  les 60 items toujours renseignes
  c7_reidentification.graine_nom     une graine stable par nom de condition
  a2_commun.distance_hamming         la distance de Hamming normalisee, masquage deja fait
  a2_commun.bootstrap_personnes      l'intervalle de confiance par reechantillonnage
  c7_bits.entropie_item              l'entropie Miller-Madow d'un item (rareté de population)
  c7_bits.rangs_tous_tirages         le rang du vrai repondant, tirages de departage gardes
  c7_bits.bits_et_ic                 les bits d'identite (borne dyadique), IC bootstrap 2000

CE QUI EST NOUVEAU ICI : les quatre constructions de predicteurs a exactitude appariee
(hasard, concentre sur les items frequents, concentre sur les items rares, errreurs
correlees entre personnes via un ordre fixe), le remplissage des items faux par tirage
dans la marginale empirique de l'item hors la vraie modalite, et le garde-fou qui verifie
l'egalite bit a bit de l'exactitude realisee entre les quatre conditions avant de rapporter
quoi que ce soit.

ETHIQUE : aucun pid ni appariement individuel n'est jamais imprime ou ecrit, seulement des
taux agreges. Aucun appel de modele de langage, aucun reseau. Lecture seule sur data/.
Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_tautologie.py
===========================================================================
"""

import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                             # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes          # noqa: E402
from c7_reidentification import items_communs, graine_nom, REF_V4, REF_V13  # noqa: E402
from c7_bits import entropie_item, rangs_tous_tirages, bits_et_ic, mode_item  # noqa: E402

GRAINE = 20260912
REF_TWIN = "JSON Persona - GPT4.1"     # jumeau vedette, sert uniquement a fournir k_i
N_REP = 5              # replicats de remplissage aleatoire des items faux
N_TIRAGES_LIENS = 20   # tirages de departage des ex aequo par replicat
N_BOOTSTRAP = 2000

CONDITIONS = ["hasard", "concentre_frequents", "concentre_rares", "correle_entre_personnes"]
LIBELLES = {
    "hasard": "(a) hasard, independant entre personnes",
    "concentre_frequents": "(b) erreurs concentrees sur les items frequents (exact = rare)",
    "concentre_rares": "(c) erreurs concentrees sur les items rares (exact = frequent)",
    "correle_entre_personnes": "(d) erreurs correlees entre personnes (ordre fixe, hors rarete)",
}


def valeurs_fausses(pool, rng):
    """Une valeur par cellule, tiree dans la marginale empirique de l'item sur toute la
    population, REJETEE si elle egale la vraie modalite de la personne (rejet puis
    retirage, jusqu'a ce qu'aucune cellule ne coincide). Meme algorithme pour les quatre
    conditions : c'est le remplissage des items FAUX, jamais la regle de choix des items
    exacts, qui varie entre conditions."""
    n, m = pool.shape
    out = np.empty((n, m), dtype=pool.dtype)
    for j in range(m):
        col = pool[:, j]
        vals, comptes = np.unique(col, return_counts=True)
        if len(vals) < 2:
            raise AssertionError(f"item {j} : une seule modalite observee, "
                                  f"aucune valeur fausse possible")
        p = comptes / comptes.sum()
        tirage = rng.choice(vals, size=n, p=p)
        collision = tirage == col
        while collision.any():
            tirage[collision] = rng.choice(vals, size=int(collision.sum()), p=p)
            collision = tirage == col
        out[:, j] = tirage
    return out


def masque_hasard(k, m, rng):
    """Sous-ensemble uniforme au hasard de taille k[i] parmi les m items, tire
    independamment pour chaque personne (scores aleatoires, rang par ligne)."""
    n = len(k)
    scores = rng.random((n, m))
    rang = np.argsort(np.argsort(scores, axis=1), axis=1)   # 0 = plus petit score
    return rang >= (m - k)[:, None]


def masque_par_ordre(k, rang_ordre):
    """Les k[i] items exacts sont les derniers de l'ordre donne (rang_ordre[j] = position
    de l'item j dans cet ordre, 0..m-1). Deterministe, meme ordre pour tout le monde :
    utilise pour (b)/(c) avec l'ordre d'entropie, et pour (d) avec un ordre fixe tire au
    hasard une seule fois, sans lien avec l'entropie."""
    m = len(rang_ordre)
    return (rang_ordre[None, :] >= (m - k)[:, None])


def construire_predicteur(condition, pool, k, rang_freq, rang_d, rep, graine_base):
    """Le vecteur de 60 reponses par personne pour une condition et un replicat donnes,
    avec exactement k[i] items exacts. Renvoie (query, masque_exact).

    OU `pool` (= y_ref, la verite) INTERVIENT, ET POURQUOI CE N'EST PAS UNE FUITE DE
    CONCEPTION : sur les positions ou masque=True, query = pool (recopie de la vraie
    valeur). C'est necessaire et non contournable : « k[i] items exacts » signifie par
    definition, sur ces positions, valeur predite = valeur vraie. Aucune construction ne
    peut atteindre une exactitude CHOISIE par personne sans, sur les positions choisies
    exactes, ecrire la vraie valeur — ce n'est pas different de ce que fait n'importe quel
    predicteur reel des qu'il devine juste. Les quatre conditions font EXACTEMENT la meme
    lecture de pool sur les positions exactes ; seule la regle qui CHOISIT ces positions
    (aleatoire, rare, frequente, ordre fixe) differe, et c'est la variable manipulee ici.
    Sur les positions ou masque=False, la valeur vient de `valeurs_fausses`, tiree dans la
    marginale de l'item sur toute la population (jamais de la valeur de cette personne)."""
    nom_g = graine_nom(condition)
    rng_faux = np.random.default_rng([graine_base, nom_g, rep, 1])
    faux = valeurs_fausses(pool, rng_faux)

    if condition == "hasard":
        rng_choix = np.random.default_rng([graine_base, nom_g, rep, 2])
        masque = masque_hasard(k, pool.shape[1], rng_choix)
    elif condition == "concentre_frequents":
        # items FAUX = les moins rares (basse entropie) -> exact = rangs hauts (rares)
        masque = masque_par_ordre(k, rang_freq)
    elif condition == "concentre_rares":
        # items FAUX = les plus rares (haute entropie) -> exact = rangs bas (frequents)
        # equivalent a masque_par_ordre avec l'ordre inverse de l'entropie
        m = len(rang_freq)
        rang_inverse = (m - 1) - rang_freq
        masque = masque_par_ordre(k, rang_inverse)
    elif condition == "correle_entre_personnes":
        masque = masque_par_ordre(k, rang_d)
    else:
        raise ValueError(condition)

    query = np.where(masque, pool, faux)
    return query, masque


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    t0 = time.time()
    paq = T1.charger()
    codes = paq["codes"]
    n_total = paq["n"]

    items = items_communs(codes, [REF_V4, REF_V13])
    m = len(items)
    print(f"{n_total} personnes, {m} items communs, {time.time()-t0:.0f}s", flush=True)

    pool = codes[REF_V4][:, items]                 # verite ET pool des candidats
    n = pool.shape[0]

    # --- k_i : emprunte au jumeau reel, jamais recalcule ni modifie ensuite ---
    x_twin = codes[REF_TWIN][:, items]
    couverture = (x_twin >= 0).mean()
    if couverture < 1.0:
        print(f"ATTENTION : couverture {REF_TWIN} = {couverture:.4f} < 1, "
              f"manquant traite comme faux (denominateur fixe 60)", flush=True)
    correct_twin = (x_twin >= 0) & (x_twin == pool)
    k = correct_twin.sum(axis=1).astype(np.int64)   # entre 0 et 60, par personne
    exactitude_ref = k / m
    print(f"k_i emprunte a {REF_TWIN} : exactitude moyenne {exactitude_ref.mean():.4f}, "
          f"mediane {np.median(exactitude_ref):.4f}, min/max {k.min()}/{k.max()} sur {m}",
          flush=True)

    # --- rarete des items : entropie Miller-Madow sur toute la population ---
    entropies = np.array([entropie_item(pool[:, j]) for j in range(m)])
    rang_freq = np.argsort(np.argsort(entropies))   # 0 = entropie la + basse (frequent)
    print(f"entropie par item : min={entropies.min():.3f}, med={np.median(entropies):.3f}, "
          f"max={entropies.max():.3f} bits", flush=True)

    # --- ordre fixe pour (d), tire une seule fois, independant de l'entropie ---
    rng_ordre_d = np.random.default_rng([GRAINE, graine_nom("ordre_d")])
    ordre_d = rng_ordre_d.permutation(m)
    rang_d = np.argsort(ordre_d)
    rho_rang_d_entropie = float(np.corrcoef(rang_d, rang_freq)[0, 1])
    print(f"ordre fixe (d) : correlation (Pearson, rang) avec l'ordre d'entropie = "
          f"{rho_rang_d_entropie:.3f} (attendu proche de 0)", flush=True)

    # ------------------------------------------------------------------
    # construction + garde-fou d'exactitude bit a bit
    # ------------------------------------------------------------------
    exactitudes_realisees = {}
    rangs_par_condition = {}     # (n, N_REP * N_TIRAGES_LIENS)
    top1_par_condition = {}      # (n,) moyenne sur les replicats
    top10_par_condition = {}

    for cond in CONDITIONS:
        t_c = time.time()
        rangs_rep = []
        top1_rep = []
        top10_rep = []
        acc_rep = []
        for r in range(N_REP):
            query, masque = construire_predicteur(cond, pool, k, rang_freq, rang_d, r, GRAINE)

            # garde-fou 1 : l'exactitude REALISEE (recalculee sur les valeurs, pas sur le
            # masque suppose) doit egaler k a l'entier pres, pour CE replicat.
            acc_realisee = (query == pool).sum(axis=1)
            if not np.array_equal(acc_realisee, k):
                ou = np.flatnonzero(acc_realisee != k)[:5]
                raise AssertionError(
                    f"GARDE-FOU ROMPU : condition={cond}, replicat={r} : l'exactitude "
                    f"realisee ne colle pas a k_i pour {int((acc_realisee != k).sum())} "
                    f"personnes (ex. indices {ou.tolist()}, "
                    f"realise={acc_realisee[ou].tolist()}, attendu={k[ou].tolist()}). "
                    f"Arret immediat, aucun resultat rapporte.")
            acc_rep.append(acc_realisee)

            rng_tir = np.random.default_rng([GRAINE, graine_nom(cond), r, 3])
            accord = 1.0 - distance_hamming(query, pool)
            vrai_idx = np.arange(n)
            rangs = rangs_tous_tirages(accord, vrai_idx, rng_tir, n_tirages=N_TIRAGES_LIENS)
            rangs_rep.append(rangs)
            top1_rep.append((rangs == 1).mean(axis=1))
            top10_rep.append((rangs <= 10).mean(axis=1))

        exactitudes_realisees[cond] = np.mean(acc_rep, axis=0)   # constant sur les replicats
        rangs_par_condition[cond] = np.hstack(rangs_rep)
        top1_par_condition[cond] = np.mean(top1_rep, axis=0)
        top10_par_condition[cond] = np.mean(top10_rep, axis=0)
        print(f"  {LIBELLES[cond]} : construit et attaque en {time.time()-t_c:.0f}s",
              flush=True)

    # garde-fou 2 : egalite bit a bit de l'exactitude realisee ENTRE les quatre conditions
    ref = exactitudes_realisees[CONDITIONS[0]]
    for cond in CONDITIONS[1:]:
        if not np.array_equal(exactitudes_realisees[cond], ref):
            raise AssertionError(
                f"GARDE-FOU ROMPU : l'exactitude realisee de '{cond}' differe de celle de "
                f"'{CONDITIONS[0]}' (devrait etre bit a bit identique). Arret immediat, "
                f"aucun resultat rapporte.")
    print(f"\nGARDE-FOU VERIFIE : exactitude par personne identique au bit pres entre les "
          f"quatre conditions (et egale a k_i emprunte a {REF_TWIN}).", flush=True)

    # ------------------------------------------------------------------
    # mesures : top1, top10 (bootstrap sur personnes), rang median, bits
    # ------------------------------------------------------------------
    lignes = []
    for cond in CONDITIONS:
        top1_m, top1_bas, top1_haut = bootstrap_personnes(
            top1_par_condition[cond], N_BOOTSTRAP, [GRAINE, graine_nom(cond), 10])
        top10_m, top10_bas, top10_haut = bootstrap_personnes(
            top10_par_condition[cond], N_BOOTSTRAP, [GRAINE, graine_nom(cond), 11])
        rangs_cond = rangs_par_condition[cond]
        rang_median = float(np.median(rangs_cond.mean(axis=1)))

        bits_pt, bits_bas, bits_haut, bits_plug, top1_verif, rang_med_verif = bits_et_ic(
            rangs_cond, n_pool=n, graine=[GRAINE, graine_nom(cond), 99])

        lignes.append({
            "condition": cond, "libelle": LIBELLES[cond],
            "appariement_exactitude": True,
            "n_attaques": n, "n_pool": n,
            "exactitude_moyenne": float(exactitudes_realisees[cond].mean() / m),
            "top1": top1_m, "top1_bas": top1_bas, "top1_haut": top1_haut,
            "top10": top10_m, "top10_bas": top10_bas, "top10_haut": top10_haut,
            "rang_median": rang_median,
            "top1_hasard": 1.0 / n, "top10_hasard": min(10, n) / n,
            "bits": bits_pt, "bits_bas": bits_bas, "bits_haut": bits_haut,
            "bits_plugin": bits_plug,
            "top1_verif_bits": top1_verif,
        })
        print(f"{LIBELLES[cond]} : top1={top1_m:.4f} [{top1_bas:.4f};{top1_haut:.4f}] "
              f"top10={top10_m:.4f} rang_med={rang_median:.1f}/{n} "
              f"bits={bits_pt:.3f} [{bits_bas:.3f};{bits_haut:.3f}]", flush=True)

    # ------------------------------------------------------------------
    # temoin supplementaire, AJOUTE APRES ALERTE (avenant du preenregistrement) :
    # modalite modale par item sur toute la population, LE MEME vecteur pour tout le
    # monde. Ne recopie JAMAIS la reponse d'un individu pour construire SA PROPRE ligne ;
    # il ne lit y_ref d'une personne que par sa contribution (1/2058e) a la modalite
    # majoritaire de population, convention deja utilisee sans reserve ailleurs dans ce
    # depot pour B0/B0 mode. Son exactitude n'est PAS calee sur k_i : mesuree telle quelle.
    # ------------------------------------------------------------------
    print("\n--- temoin sans lecture individuelle de la cible (avenant) ---", flush=True)
    query_mode = mode_item(pool)                       # vecteur constant, importe tel quel
    acc_mode = (query_mode == pool).sum(axis=1)
    print(f"temoin_mode_global : exactitude naturelle (non calee) = "
          f"{(acc_mode / m).mean():.4f}, mediane {np.median(acc_mode / m):.4f}", flush=True)

    rng_tir_mode = np.random.default_rng([GRAINE, graine_nom("temoin_mode_global"), 3])
    accord_mode = 1.0 - distance_hamming(query_mode, pool)
    rangs_mode = rangs_tous_tirages(accord_mode, np.arange(n), rng_tir_mode,
                                     n_tirages=N_TIRAGES_LIENS)
    top1_mode_pers = (rangs_mode == 1).mean(axis=1)
    top10_mode_pers = (rangs_mode <= 10).mean(axis=1)
    top1_mode, top1_mode_bas, top1_mode_haut = bootstrap_personnes(
        top1_mode_pers, N_BOOTSTRAP, [GRAINE, graine_nom("temoin_mode_global"), 10])
    top10_mode, top10_mode_bas, top10_mode_haut = bootstrap_personnes(
        top10_mode_pers, N_BOOTSTRAP, [GRAINE, graine_nom("temoin_mode_global"), 11])
    bits_mode_pt, bits_mode_bas, bits_mode_haut, bits_mode_plug, _, _ = bits_et_ic(
        rangs_mode, n_pool=n, graine=[GRAINE, graine_nom("temoin_mode_global"), 99])

    lignes.append({
        "condition": "temoin_mode_global",
        "libelle": "(e) temoin hors appariement : modalite modale de population, "
                   "AUCUNE lecture de la cible pour construire sa propre ligne",
        "appariement_exactitude": False,
        "n_attaques": n, "n_pool": n,
        "exactitude_moyenne": float((acc_mode / m).mean()),
        "top1": top1_mode, "top1_bas": top1_mode_bas, "top1_haut": top1_mode_haut,
        "top10": top10_mode, "top10_bas": top10_mode_bas, "top10_haut": top10_mode_haut,
        "rang_median": float(np.median(rangs_mode.mean(axis=1))),
        "top1_hasard": 1.0 / n, "top10_hasard": min(10, n) / n,
        "bits": bits_mode_pt, "bits_bas": bits_mode_bas, "bits_haut": bits_mode_haut,
        "bits_plugin": bits_mode_plug, "top1_verif_bits": float((rangs_mode == 1).mean()),
    })
    print(f"temoin_mode_global : top1={top1_mode:.4f} [{top1_mode_bas:.4f};"
          f"{top1_mode_haut:.4f}] top10={top10_mode:.4f} bits={bits_mode_pt:.3f}",
          flush=True)

    df = pd.DataFrame(lignes)
    T1.ecrire(df, "c7-tautologie.csv")

    # ------------------------------------------------------------------
    # verdict, regle de decision preenregistree section 4
    # ------------------------------------------------------------------
    t1 = {r["condition"]: r["top1"] for r in lignes}
    t1_bas = {r["condition"]: r["top1_bas"] for r in lignes}
    t1_haut = {r["condition"]: r["top1_haut"] for r in lignes}

    b, d = t1["concentre_frequents"], t1["correle_entre_personnes"]
    ratio_b_d = b / d if d > 0 else float("inf")
    ic_disjoints = t1_bas["concentre_frequents"] > t1_haut["correle_entre_personnes"]

    tous = [t1[c] for c in CONDITIONS]
    ecart_global = (max(tous) / min(tous)) if min(tous) > 0 else float("inf")
    tous_recouvrent = all(
        not (t1_bas[c1] > t1_haut[c2] or t1_bas[c2] > t1_haut[c1])
        for i, c1 in enumerate(CONDITIONS) for c2 in CONDITIONS[i + 1:]
    )

    print(f"\n--- verdict (regle preenregistree, section 4) ---", flush=True)
    print(f"top1(b)={b:.4f}, top1(d)={d:.4f}, ratio b/d={ratio_b_d:.2f}, "
          f"IC disjoints={ic_disjoints}", flush=True)
    print(f"ecart global max/min sur les quatre conditions = {ecart_global:.2f}", flush=True)

    if ecart_global < 2.0 and tous_recouvrent:
        print("VERDICT : tautologie VALIDEE — les quatre conditions se recouvrent aux IC "
              "pres, l'exactitude par personne suffit a tout expliquer.", flush=True)
    elif ratio_b_d >= 3.0 and ic_disjoints:
        print("VERDICT : tautologie REFUTEE sur ce terrain — a exactitude strictement "
              "egale, la fuite depend fortement de quels items sont exacts (b >> d).",
              flush=True)
    else:
        print("VERDICT : mixte — rapporter l'ordre de grandeur sans trancher "
              "binairement (voir section 4 du preenregistrement).", flush=True)

    print(f"\nTOTAL {time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
