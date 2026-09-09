"""
a20 : le transport de variance rejoue, avec les deux corrections que a17 exige.

Statut : script d'analyse, pas du code de production. Il existe pour qu'un tiers puisse
rejouer chaque chiffre de resultats/a20-transport-de-variance-v2.md en une commande.

CE QUI CHANGE PAR RAPPORT A a7
------------------------------
analyses/a7_transport_variance.py n'est PAS modifie. Il est importe tel quel : l'operateur
de transport, les scores de plausibilite, les lecteurs et le masque d'items viennent de lui,
et les estimateurs viennent toujours de a1. Deux choses seulement sont ajoutees.

1. OBJECTION 4 de a17 (relecture adverse, section 3.1). L'estimateur d'information mutuelle
   corrige par Miller Madow n'est pas invariant sous l'operateur. A lambda = 0, l'operateur
   force p(r|s) = p(r) exactement : l'information mutuelle EMPIRIQUE est nulle par
   construction, or l'estimateur rend -0,136 en unites de ratio, soit davantage que la demi
   largeur des intervalles publies par a7. La cause est identifiee : la correction de Miller
   Madow retranche une quantite calibree sur le bruit d'echantillonnage d'un tirage i.i.d.,
   alors que le transport SUPPRIME ce bruit en meme temps qu'il supprime le signal.

   Correctif implemente ici : le residu de permutation est RECALIBRE A CHAQUE LAMBDA, et deux
   nulles sont calculees, pas une, parce qu'elles ne disent pas la meme chose.

     residu A, "permutation seule"  : on permute les etiquettes de segment SUR LA POPULATION
                                      DEJA TRANSPORTEE. C'est la lecture litterale de la
                                      correction de a1. Elle re randomise le tableau croise
                                      et lui rend le bruit multinomial que le transport avait
                                      retire : elle ne peut donc PAS voir l'artefact.
     residu B, "permutation PUIS transport" : on permute les etiquettes de segment sur la
                                      population d'origine, PUIS on applique le meme
                                      transport au meme lambda avec ces etiquettes permutees.
                                      La nulle porte alors exactement la meme structure de
                                      quotas deterministes que la mesure. C'est la nulle
                                      appariee a la structure, et c'est celle qui corrige.

   Propriete de B, a verifier et verifiee : a lambda = 1 elle redonne exactement le residu de
   permutation de a1 (le transport est l'identite), et a lambda = 0 elle annule le terme inter
   estime. Le point important pour l'honnetete du rapport : a lambda = 0 cette annulation est
   VRAIE PAR CONSTRUCTION et n'est donc pas un test independant. Ce qui est teste, c'est le
   comportement aux lambdas intermediaires et l'effet sur les chiffres publies.

   Mesure principale : GINI SIMPSON, dont l'estimateur sans biais a un residu de permutation
   inferieur a 0,1 pour cent chez a1. L'entropie est conservee en mesure secondaire, avec le
   meme protocole de recalibration.

2. OBJECTION 5 de a17 (section 3.2). L'enonce d'impossibilite de a7 ("aucun operateur a somme
   constante ne peut atteindre (1,1)") est etabli sur deux mesures et tu sur la troisieme. Ici
   w (part du terme inter dans la dispersion totale HUMAINE), T (ratio de dispersion totale de
   la condition) et le plafond intra a inter nul, T / (1 - w), sont calcules pour les TROIS
   mesures, sur les 149 items ET sur les 70 items ordinaux, par condition et par axe. Puis le
   transport est REJOUE sous M3, sur les seuls items ordinaux, pour voir s'il atteint (1,1) la
   ou le plafond le permet, avec les criteres 2 (exactitude individuelle) et 3 (A6, la variance
   gagnee est elle informative) de a7.

CONVENTION D'IMPUTATION DU RESIDU, elle differe de a1 et il faut le dire
-----------------------------------------------------------------------
a1 retranche le residu du seul terme inter. Le total inter + intra n'est alors plus invariant,
ce qui casse l'identite T = w x ratio_inter + (1 - w) x ratio_intra sur laquelle repose toute
l'objection 5. Ici le residu est TRANSFERE : inter* = inter - residu, intra* = intra + residu.
Le total est invariant, l'identite tient exactement, et le ratio intra publie differe de celui
de a1 d'une quantite qui est imprimee et publiee dans a20-convention-residu.csv.

ENTREES : identiques a a7.
SORTIES, toutes dans resultats/
-------------------------------
  a20-figure-transport-v2.png et .svg
  a20-lambda0-controle.csv    verification (c) : le terme inter a lambda 0, brut et corrige
  a20-trajectoires.csv        balayage de lambda, ratios corriges, trois mesures
  a20-plafond.csv             objection 5 : w, T et plafond, 3 mesures x 2 jeux d'items
  a20-lambda-calibre.csv      lambda retenu par bloc, calibre avec l'estimateur corrige
  a20-avant-apres.csv         avant / apres au lambda calibre, intervalles bootstrap
  a20-par-axe.csv             effet sur les six axes
  a20-m3-ordinal.csv          le transport rejoue sous M3 sur les 70 items ordinaux
  a20-m3-critere-a6.csv       criteres 2 et 3 pour le run M3
  a20-dilatation-temoin.csv   le temoin a un seul bouton, avec estimateur corrige
  a20-convention-residu.csv   ce que change le transfert du residu vers le terme intra

Aucun appel de modele de langage. Quatre coeurs. data/traces/ n'est jamais lu ni ecrit.
Usage : .venv/bin/python analyses/a20_transport_variance_v2.py [--rapide]
"""

import os

# Un llama-server tourne sur la machine pour un autre chantier : on se limite a 4 coeurs.
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import argparse
import csv
import sys
import time

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from scipy.stats import spearmanr

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "analyses"))

# --- estimateurs de a1, importes tels quels, jamais modifies ----------------
from a1_double_distorsion import (AXES, agreger, compter, construire_index, decomposer,
                                  matrice_distance)
# --- l'operateur et l'outillage de a7, importes tels quels, jamais modifies -
from a7_transport_variance import (AGENTS, AXES_TRANSPORT, B2_A2, HUMAIN_CTRL, HUMAIN_REF,
                                   LAMBDAS, N_BLOCS, N_PLIS, charger, en_objets,
                                   masque_items, scores_voisins, transporter)
# --- estimateurs de a2, importes tels quels, jamais modifies ---------------
from a2_commun import bootstrap_personnes, exactitude_par_personne, profil_diversite

SORTIE_DEFAUT = os.path.join(RACINE, "resultats")
MESURES = ["entropie", "gini_simpson", "variance_ordinale"]
NOMS_MESURE = {"entropie": "M1 entropie", "gini_simpson": "M2 Gini Simpson",
               "variance_ordinale": "M3 variance ordinale"}
MESURE_PRINCIPALE = "gini_simpson"
GRAINE = 20260907
N_PERM = 40          # permutations par nulle, par condition x axe x lambda
JEUX_ITEMS = ["149 items", "70 items ordinaux"]


# ===========================================================================
# 1. Mesure a un seul axe, et residus de permutation par item
# ===========================================================================

class MesureurAxe:
    """Decompose la dispersion sur UN axe de segmentation, avec les estimateurs de a1.

    On ne construit l'index que pour l'axe demande, ce qui divise par six le cout du
    comptage : ce script fait quelques milliers de mesures de plus que a7, a cause des
    permutations, et le comptage devient le poste dominant.

    Sortie : dictionnaire mesure -> (inter, intra) en tableaux par ITEM, longueur n_items,
    deja mis a zero la ou la cellule n'est pas valide. Garder le detail par item est ce qui
    permet de reutiliser UNE serie de permutations pour n'importe quel sous ensemble d'items,
    donc pour la calibration par blocs comme pour l'evaluation.
    """

    def __init__(self, n_items, k_max, g_max, est_ordinal, valeurs_ordinales):
        self.n_items, self.k_max, self.g_max = n_items, k_max, g_max
        self.est_ordinal = est_ordinal
        self.valeurs_ordinales = valeurs_ordinales

    def par_item(self, x, seg_vec, axe_nom, lignes=None):
        idx, poubelle = construire_index(x, {axe_nom: seg_vec}, self.k_max, self.g_max,
                                         self.n_items, axes=[axe_nom])
        if lignes is None:
            lignes = np.arange(x.shape[0])
        cnt = compter(idx, lignes, poubelle, self.n_items, self.g_max, self.k_max, 1)
        dec = decomposer(cnt, self.valeurs_ordinales)
        out = {}
        for m, (inter, intra, valide) in dec.items():
            ok = valide[0] & (self.est_ordinal if m == "variance_ordinale"
                              else np.ones(self.n_items, dtype=bool))
            out[m] = (np.where(ok, inter[0], 0.0), np.where(ok, intra[0], 0.0))
        return out


def sommer(par_item, masque):
    """Somme les termes par item sur un masque d'items. Meme regle d'agregation que a1."""
    return {m: (float(v[0][masque].sum()), float(v[1][masque].sum()))
            for m, v in par_item.items()}


# ===========================================================================
# 2. Programme principal
# ===========================================================================

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--racine", default=os.path.join(RACINE, "data/osf-t6g7k-stanford"))
    ap.add_argument("--sortie", default=SORTIE_DEFAUT)
    ap.add_argument("--bootstrap", type=int, default=400)
    ap.add_argument("--permutations", type=int, default=N_PERM)
    ap.add_argument("--graine", type=int, default=GRAINE)
    ap.add_argument("--rapide", action="store_true")
    args = ap.parse_args()
    if args.rapide:
        args.bootstrap, args.permutations = 40, 6
    t0 = time.time()
    os.makedirs(args.sortie, exist_ok=True)

    options, ordinal, entetes, n_items, donnees, taux_nc, ids, seg, niveaux = \
        charger(args.racine)
    n = len(ids)
    garder = masque_items(entetes)
    items = np.where(garder)[0]
    est_ordinal = np.array([ordinal.get(q, False) for q in entetes])
    garder_ord = garder & est_ordinal
    items_ord = np.where(garder_ord)[0]
    k_par_item = np.array([len(options[q]) for q in entetes])
    k_max = int(k_par_item.max())
    g_max = int(max(len(niveaux[a]) for a in AXES))
    valeurs_ordinales = np.zeros((n_items, k_max))
    for j, q in enumerate(entetes):
        if est_ordinal[j] and k_par_item[j] > 1:
            valeurs_ordinales[j, :k_par_item[j]] = np.arange(k_par_item[j]) / \
                (k_par_item[j] - 1)

    MASQUES = {"149 items": garder, "70 items ordinaux": garder_ord}

    print("=" * 96)
    print("a20 : TRANSPORT DE VARIANCE, VERSION 2. Objections 4 et 5 de a17 corrigees.")
    print("=" * 96)
    print(f"{n} participants, {len(items)} items retenus, "
          f"{len(items_ord)} d'entre eux ordinaux")
    print(f"Mesure principale : {NOMS_MESURE[MESURE_PRINCIPALE]}. "
          f"Permutations par nulle : {args.permutations}. Bootstrap : {args.bootstrap}.")

    mes = MesureurAxe(n_items, k_max, g_max, est_ordinal, valeurs_ordinales)
    rng_perm = np.random.default_rng(args.graine + 101)
    perms = [rng_perm.permutation(n) for _ in range(args.permutations)]

    # --- decoupages, identiques a a7 --------------------------------------
    ordre = np.random.default_rng(args.graine).permutation(items)
    blocs = np.array_split(ordre, N_BLOCS)
    perm_pers = np.random.default_rng(args.graine + 1).permutation(np.arange(n))
    parts = np.array_split(perm_pers, N_PLIS)
    plis = [(np.sort(np.concatenate([parts[q] for q in range(N_PLIS) if q != p])),
             np.sort(parts[p])) for p in range(N_PLIS)]

    # ==================================================================
    # 3. Reference humaine : termes par item et residu de permutation
    # ==================================================================
    print("\n--- reference humaine, vague 1, et son residu de permutation ---")
    ref_item, ref_nul = {}, {}
    for a in AXES:
        ref_item[a] = mes.par_item(donnees[HUMAIN_REF], seg[a], a)
        acc = {m: np.zeros(n_items) for m in MESURES}
        for p in perms:
            pi = mes.par_item(donnees[HUMAIN_REF], seg[a][p], a)
            for m in MESURES:
                acc[m] += pi[m][0]
        ref_nul[a] = {m: acc[m] / len(perms) for m in MESURES}
    for a in AXES_TRANSPORT:
        for jeu, msk in MASQUES.items():
            for m in MESURES:
                obs = float(ref_item[a][m][0][msk].sum())
                nu = float(ref_nul[a][m][msk].sum())
                print(f"  {a:<19}{jeu:<18}{NOMS_MESURE[m]:<22}"
                      f"inter {obs:9.4f}  residu {nu:8.4f}  "
                      f"part {100 * nu / obs if obs else float('nan'):6.2f} %")

    def ref_termes(a, msk, m):
        """(inter*, intra*, total) humains, residu transfere vers le terme intra."""
        inter = float(ref_item[a][m][0][msk].sum())
        intra = float(ref_item[a][m][1][msk].sum())
        nu = float(ref_nul[a][m][msk].sum())
        return inter - nu, intra + nu, inter + intra

    # w : part du terme inter dans la dispersion totale HUMAINE.
    W = {}
    for a in AXES_TRANSPORT:
        for jeu, msk in MASQUES.items():
            for m in MESURES:
                i_, a_, t_ = ref_termes(a, msk, m)
                W[(a, jeu, m)] = i_ / t_ if t_ else float("nan")

    # ==================================================================
    # 4. Balayage de lambda, avec les deux nulles recalibrees a chaque lambda
    # ==================================================================
    print("\n" + "=" * 96)
    print("BALAYAGE DE LAMBDA. A chaque lambda, deux nulles :")
    print("  A = permutation des segments SUR la population transportee")
    print("  B = permutation PUIS transport au meme lambda (nulle appariee a la structure)")
    print("=" * 96)

    verite = donnees[HUMAIN_REF]
    verite_obj = en_objets(verite[:, items])
    masque_ev = np.zeros_like(verite, dtype=bool)
    masque_ev[:, items] = verite[:, items] >= 0
    exact_ref = {c: exactitude_par_personne(donnees[c], verite, masque_ev) for c in AGENTS}

    # scores de plausibilite pour la variante informee, calcul identique a a7
    print("\nCalcul des scores de plausibilite (voisins humains hors pli)...")
    scores = {}
    for c in AGENTS:
        scores[c] = scores_voisins(donnees[c], donnees[HUMAIN_REF], items, k_par_item,
                                   k_max, plis, blocs)
        print(f"  {c} fait, {time.time() - t0:.0f} s")

    def transport_naif(x0, seg_vec, lam, sous_items, decalage=7):
        return transporter(x0, seg_vec, lam, sous_items, k_par_item, scores=None,
                           rng=np.random.default_rng(args.graine + decalage))

    # obs_item[(c, axe, lam)]  : termes par item de la population transportee
    # nulA_item, nulB_item     : les deux residus, par item
    obs_item, nulA_item, nulB_item = {}, {}, {}
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            sv = seg[axe]
            for lam in LAMBDAS:
                xt = transport_naif(donnees[c], sv, lam, items)
                obs_item[(c, axe, lam)] = mes.par_item(xt, sv, axe)
                accA = {m: np.zeros(n_items) for m in MESURES}
                accB = {m: np.zeros(n_items) for m in MESURES}
                for ip, p in enumerate(perms):
                    svp = sv[p]
                    piA = mes.par_item(xt, svp, axe)
                    xb = transport_naif(donnees[c], svp, lam, items, decalage=7 + ip)
                    piB = mes.par_item(xb, svp, axe)
                    for m in MESURES:
                        accA[m] += piA[m][0]
                        accB[m] += piB[m][0]
                nulA_item[(c, axe, lam)] = {m: accA[m] / len(perms) for m in MESURES}
                nulB_item[(c, axe, lam)] = {m: accB[m] / len(perms) for m in MESURES}
            print(f"  {c} / {axe} : balaye avec les deux nulles, {time.time() - t0:.0f} s")

    def ratios_corriges(cle, msk, m, nul="B"):
        """(ratio inter*, ratio intra*, ratio total) pour un couple mesure x jeu d'items."""
        c, axe, lam = cle
        oi = obs_item[cle][m]
        inter = float(oi[0][msk].sum())
        intra = float(oi[1][msk].sum())
        table = nulB_item if nul == "B" else nulA_item
        nu = float(table[cle][m][msk].sum())
        ri_h, ra_h, t_h = ref_termes(axe, msk, m)
        return ((inter - nu) / ri_h if ri_h else float("nan"),
                (intra + nu) / ra_h if ra_h else float("nan"),
                (inter + intra) / t_h if t_h else float("nan"))

    lignes_traj = [["condition", "axe_transport", "lambda", "jeu_items", "mesure",
                    "inter_brut", "inter_nulA", "inter_nulB", "ratio_intra_brut",
                    "ratio_intra_corrige", "ratio_total"]]
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            for lam in LAMBDAS:
                cle = (c, axe, lam)
                for jeu, msk in MASQUES.items():
                    for m in MESURES:
                        if jeu == "149 items" and m == "variance_ordinale":
                            continue   # M3 ne porte que sur les items ordinaux
                        oi = obs_item[cle][m]
                        inter = float(oi[0][msk].sum())
                        intra = float(oi[1][msk].sum())
                        ri_h, ra_h, t_h = ref_termes(axe, msk, m)
                        brut = inter / (ri_h + float(ref_nul[axe][m][msk].sum()))
                        rA = ratios_corriges(cle, msk, m, "A")
                        rB = ratios_corriges(cle, msk, m, "B")
                        lignes_traj.append([
                            c, axe, f"{lam:.1f}", jeu, m, f"{brut:.4f}", f"{rA[0]:.4f}",
                            f"{rB[0]:.4f}", f"{intra / (ra_h - float(ref_nul[axe][m][msk].sum())):.4f}",
                            f"{rB[1]:.4f}", f"{rB[2]:.4f}"])
    with open(os.path.join(args.sortie, "a20-trajectoires.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_traj)

    # ==================================================================
    # 5. Verification (c) : le terme inter a lambda 0 tombe t il a zero ?
    # ==================================================================
    print("\n" + "=" * 96)
    print("VERIFICATION (c) : a lambda 0 l'operateur annule l'information mutuelle")
    print("EMPIRIQUE par construction. Un estimateur sans biais doit rendre zero.")
    print("=" * 96)
    print(f"{'condition':<26}{'axe':<19}{'jeu':<18}{'mesure':<22}"
          f"{'brut':>9}{'nulle A':>10}{'nulle B':>10}{'demi IC':>10}")
    lignes_l0 = [["condition", "axe_transport", "jeu_items", "mesure", "inter_brut",
                  "inter_corrige_nulA", "inter_corrige_nulB", "demi_largeur_ic95_bootstrap",
                  "zero_dans_ic_nulA", "zero_dans_ic_nulB"]]

    # demi largeur d'intervalle : bootstrap sur les personnes du terme inter a lambda 0.
    rng_b0 = np.random.default_rng(args.graine + 23)
    tirages_l0 = [rng_b0.integers(0, n, size=n)
                  for _ in range(min(args.bootstrap, 200))]
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            cle = (c, axe, 0.0)
            xt = transport_naif(donnees[c], seg[axe], 0.0, items)
            boots = {(jeu, m): [] for jeu in MASQUES for m in MESURES}
            for lg in tirages_l0:
                pi = mes.par_item(xt, seg[axe], axe, lignes=lg)
                pr = mes.par_item(donnees[HUMAIN_REF], seg[axe], axe, lignes=lg)
                for jeu, msk in MASQUES.items():
                    for m in MESURES:
                        den = float(pr[m][0][msk].sum())
                        boots[(jeu, m)].append(float(pi[m][0][msk].sum()) / den
                                               if den else float("nan"))
            for jeu, msk in MASQUES.items():
                for m in MESURES:
                    if jeu == "149 items" and m == "variance_ordinale":
                        continue
                    oi = obs_item[cle][m]
                    inter = float(oi[0][msk].sum())
                    ri_h, _, _ = ref_termes(axe, msk, m)
                    nuA = float(nulA_item[cle][m][msk].sum())
                    nuB = float(nulB_item[cle][m][msk].sum())
                    brut = inter / (ri_h + float(ref_nul[axe][m][msk].sum()))
                    vA, vB = (inter - nuA) / ri_h, (inter - nuB) / ri_h
                    v = np.asarray(boots[(jeu, m)], dtype=float)
                    v = v[np.isfinite(v)]
                    demi = float((np.percentile(v, 97.5) - np.percentile(v, 2.5)) / 2) \
                        if v.size >= 20 else float("nan")
                    lignes_l0.append([c, axe, jeu, m, f"{brut:.4f}", f"{vA:.4f}",
                                      f"{vB:.4f}", f"{demi:.4f}",
                                      "oui" if abs(vA) <= demi else "non",
                                      "oui" if abs(vB) <= demi else "non"])
                    print(f"{c:<26}{axe:<19}{jeu:<18}{NOMS_MESURE[m]:<22}"
                          f"{brut:>9.4f}{vA:>10.4f}{vB:>10.4f}{demi:>10.4f}")
    with open(os.path.join(args.sortie, "a20-lambda0-controle.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_l0)

    # --- pourquoi la nulle B ne rend pas zero sur le profil croise --------
    # L'operateur ne transporte pas un couple (item, segment) de moins de N_MIN_CELLULE
    # personnes. Sur un axe a 18 segments, cela laisse une part non negligeable de la
    # population hors du transport, et l'ecart entre segments qui subsiste a lambda 0
    # n'est PAS un artefact d'estimateur : c'est du signal reellement non transporte.
    # On le chiffre ici plutot que de le laisser passer pour un biais.
    print("\n--- couverture de l'operateur : cellules (item, segment) trop petites ---")
    lignes_cv = [["axe_transport", "n_segments", "n_cellules_possibles",
                  "n_cellules_transportees", "part_cellules", "part_population"]]
    for axe in AXES_TRANSPORT:
        sv = seg[axe]
        segments = [g for g in np.unique(sv) if g >= 0]
        tot_c = pris_c = 0
        tot_p = pris_p = 0
        for j in items:
            col = donnees[HUMAIN_REF][:, j]
            vg = (col >= 0) & (sv >= 0)
            if int(vg.sum()) < 2 * 20:
                continue
            for g in segments:
                n_s = int((vg & (sv == g)).sum())
                if n_s == 0:
                    continue
                tot_c += 1
                tot_p += n_s
                if n_s >= 20:
                    pris_c += 1
                    pris_p += n_s
        lignes_cv.append([axe, str(len(segments)), str(tot_c), str(pris_c),
                          f"{pris_c / tot_c:.4f}", f"{pris_p / tot_p:.4f}"])
        print(f"  {axe:<19}{len(segments):>3} segments, "
              f"{pris_c}/{tot_c} cellules transportees ({100 * pris_c / tot_c:.1f} %), "
              f"{100 * pris_p / tot_p:.1f} % de la population")
    with open(os.path.join(args.sortie, "a20-couverture-cellules.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_cv)

    # ==================================================================
    # 6. Objection 5 : w, T et le plafond intra, pour les trois mesures
    # ==================================================================
    print("\n" + "=" * 96)
    print("OBJECTION 5 : w, T et le plafond intra a inter nul, TROIS mesures, DEUX jeux")
    print("plafond = T / (1 - w). Au dessus de 1, le transport pur suffit.")
    print("=" * 96)
    print(f"{'condition':<26}{'axe':<19}{'jeu':<18}{'mesure':<22}"
          f"{'w':>8}{'T':>8}{'plafond':>9}{'intra l=0':>11}")
    lignes_pl = [["condition", "axe_transport", "jeu_items", "mesure", "w", "T",
                  "plafond_intra_a_inter_nul", "intra_mesure_a_lambda_0",
                  "plafond_au_dessus_de_1"]]
    plafonds = {}
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            for jeu, msk in MASQUES.items():
                for m in MESURES:
                    if jeu == "149 items" and m == "variance_ordinale":
                        continue
                    w = W[(axe, jeu, m)]
                    cle1 = (c, axe, 1.0)
                    oi = obs_item[cle1][m]
                    _, _, t_h = ref_termes(axe, msk, m)
                    T = (float(oi[0][msk].sum()) + float(oi[1][msk].sum())) / t_h
                    plaf = T / (1.0 - w)
                    intra0 = ratios_corriges((c, axe, 0.0), msk, m, "B")[1]
                    plafonds[(c, axe, jeu, m)] = (w, T, plaf, intra0)
                    lignes_pl.append([c, axe, jeu, m, f"{w:.4f}", f"{T:.4f}",
                                      f"{plaf:.4f}", f"{intra0:.4f}",
                                      "oui" if plaf > 1.0 else "non"])
                    print(f"{c:<26}{axe:<19}{jeu:<18}{NOMS_MESURE[m]:<22}"
                          f"{w:>8.4f}{T:>8.4f}{plaf:>9.4f}{intra0:>11.4f}")
    with open(os.path.join(args.sortie, "a20-plafond.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_pl)
    n_sup = sum(1 for k, v in plafonds.items()
                if k[3] == "variance_ordinale" and v[2] > 1.0)
    n_tot_m3 = sum(1 for k in plafonds if k[3] == "variance_ordinale")
    print(f"\nSous M3, plafond au dessus de 1 pour {n_sup} couples sur {n_tot_m3}.")

    # ==================================================================
    # 7. Calibration de lambda avec l'estimateur CORRIGE
    # ==================================================================
    print("\n" + "=" * 96)
    print("CALIBRATION DE LAMBDA, estimateur corrige par la nulle B, mesure principale")
    print(f"{NOMS_MESURE[MESURE_PRINCIPALE]}. Choisi sur 4 blocs d'items, applique au 5e.")
    print("=" * 96)

    def inter_calib(c, axe, lam, msk_calib, m, nul="B"):
        cle = (c, axe, lam)
        oi = obs_item[cle][m]
        inter = float(oi[0][msk_calib].sum())
        table = nulB_item if nul == "B" else nulA_item
        nu = float(table[cle][m][msk_calib].sum())
        ri_h, _, _ = ref_termes(axe, msk_calib, m)
        return (inter - nu) / ri_h if ri_h else float("nan")

    def calibrer(mesure, msk_global, blocs_locaux, nul="B"):
        out = {}
        lignes = [["condition", "axe_transport", "mesure_de_calibration", "bloc",
                   "lambda_retenu", "inter_calibration_avant", "inter_calibration_apres"]]
        for c in AGENTS:
            for axe in AXES_TRANSPORT:
                vec = np.ones(n_items)
                for b, bloc in enumerate(blocs_locaux):
                    msk = msk_global.copy()
                    msk[bloc] = False
                    av = inter_calib(c, axe, 1.0, msk, mesure, nul)
                    best, ecart, apres = 1.0, float("inf"), av
                    for lam in LAMBDAS:
                        r = inter_calib(c, axe, lam, msk, mesure, nul)
                        if abs(r - 1.0) < ecart:
                            best, ecart, apres = lam, abs(r - 1.0), r
                    vec[bloc] = best
                    lignes.append([c, axe, mesure, str(b), f"{best:.1f}",
                                   f"{av:.4f}", f"{apres:.4f}"])
                out[(c, axe)] = vec
                print(f"  {c:<26}{axe:<19}{mesure:<20}lambdas par bloc : "
                      + " ".join(f"{v:.1f}" for v in
                                 [out[(c, axe)][bl[0]] for bl in blocs_locaux]))
        return out, lignes

    lam_M2, lignes_lam = calibrer(MESURE_PRINCIPALE, garder, blocs)
    lam_M1, lignes_lam1 = calibrer("entropie", garder, blocs)
    blocs_ord = np.array_split(np.random.default_rng(args.graine).permutation(items_ord),
                               N_BLOCS)
    lam_M3, lignes_lam3 = calibrer("variance_ordinale", garder_ord, blocs_ord)
    with open(os.path.join(args.sortie, "a20-lambda-calibre.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_lam + lignes_lam1[1:] + lignes_lam3[1:])

    # ==================================================================
    # 8. Application, avant / apres, avec bootstrap
    # ==================================================================
    print("\n" + "=" * 96)
    print("AVANT / APRES au lambda calibre, avec le residu recalibre a chaque item")
    print("=" * 96)

    def residu_vecteur(c, axe, vec_lam, nul_table):
        """Residu par item quand lambda varie d'un item a l'autre : chaque item prend le
        residu mesure au lambda qui lui est applique."""
        out = {m: np.zeros(n_items) for m in MESURES}
        for lam in LAMBDAS:
            sel = np.isclose(vec_lam, lam)
            if not sel.any():
                continue
            for m in MESURES:
                out[m][sel] = nul_table[(c, axe, lam)][m][sel]
        return out

    # matrices transportees au lambda calibre, deux variantes, plus le temoin
    transportes, journaux = {}, {}
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            for variante in ["naive", "informee"]:
                jr = []
                xt = transporter(donnees[c], seg[axe], lam_M2[(c, axe)], items,
                                 k_par_item,
                                 scores=None if variante == "naive" else scores[c],
                                 rng=np.random.default_rng(args.graine + 13), journal=jr)
                transportes[(c, axe, variante)] = xt
                journaux[(c, axe, variante)] = jr

    # temoin de dilatation, mu calibre pour amener le ratio intra corrige a 1
    print("\nTEMOIN, dilatation pure vers la loi uniforme, mu calibre par bloc.")
    lignes_dil = [["condition", "axe", "mu_median", "mesure", "ratio_inter_avant",
                   "ratio_inter_apres", "ratio_intra_avant", "ratio_intra_apres",
                   "ratio_total_avant", "ratio_total_apres", "exactitude_apres",
                   "delta_exactitude", "delta_ic_bas", "delta_ic_haut",
                   "n_change", "n_reparation", "n_casse"]]
    mu_median = {}
    for c in AGENTS:
        for axe in AXES_TRANSPORT:
            vec_mu = np.ones(n_items)
            for bloc in blocs:
                msk = garder.copy()
                msk[bloc] = False
                best, ecart = 1.0, float("inf")
                for mu in LAMBDAS:
                    xd = transporter(donnees[c], seg[axe], mu, np.where(msk)[0],
                                     k_par_item, scores=None,
                                     rng=np.random.default_rng(args.graine + 19),
                                     vers="uniforme")
                    pi = mes.par_item(xd, seg[axe], axe)
                    _, ra_h, _ = ref_termes(axe, msk, MESURE_PRINCIPALE)
                    r = float(pi[MESURE_PRINCIPALE][1][msk].sum()) / ra_h
                    if abs(r - 1.0) < ecart:
                        best, ecart = mu, abs(r - 1.0)
                vec_mu[bloc] = best
            jr = []
            xd = transporter(donnees[c], seg[axe], vec_mu, items, k_par_item,
                             scores=scores[c],
                             rng=np.random.default_rng(args.graine + 19), journal=jr,
                             vers="uniforme")
            transportes[(c, axe, "dilatation")] = xd
            journaux[(c, axe, "dilatation")] = jr
            mu_median[(c, axe)] = float(np.median(vec_mu[items]))
            ex_ap = exactitude_par_personne(xd, verite, masque_ev)
            d_m, d_b, d_h_ = bootstrap_personnes(ex_ap - exact_ref[c], n_tirages=2000,
                                                 graine=args.graine)
            rep = sum(1 for (i, j, s_, d_) in jr
                      if verite[i, j] >= 0 and d_ == verite[i, j] and s_ != verite[i, j])
            cas = sum(1 for (i, j, s_, d_) in jr
                      if verite[i, j] >= 0 and s_ == verite[i, j] and d_ != verite[i, j])
            pid = mes.par_item(xd, seg[axe], axe)
            pia = mes.par_item(donnees[c], seg[axe], axe)
            for m in ["entropie", MESURE_PRINCIPALE]:
                nu_av = float(nulB_item[(c, axe, 1.0)][m][garder].sum())
                ri_h, ra_h, t_h = ref_termes(axe, garder, m)
                # la dilatation n'a pas de nulle appariee : on emploie la nulle A,
                # mesuree sur la population dilatee, et on le dit dans le rapport.
                accA = np.zeros(n_items)
                for p in perms[:max(4, args.permutations // 4)]:
                    accA += mes.par_item(xd, seg[axe][p], axe)[m][0]
                nu_ap = float(accA[garder].sum()) / max(4, args.permutations // 4)
                lignes_dil.append([
                    c, axe, f"{mu_median[(c, axe)]:.1f}", m,
                    f"{(float(pia[m][0][garder].sum()) - nu_av) / ri_h:.4f}",
                    f"{(float(pid[m][0][garder].sum()) - nu_ap) / ri_h:.4f}",
                    f"{(float(pia[m][1][garder].sum()) + nu_av) / ra_h:.4f}",
                    f"{(float(pid[m][1][garder].sum()) + nu_ap) / ra_h:.4f}",
                    f"{(float(pia[m][0][garder].sum()) + float(pia[m][1][garder].sum())) / t_h:.4f}",
                    f"{(float(pid[m][0][garder].sum()) + float(pid[m][1][garder].sum())) / t_h:.4f}",
                    f"{float(np.nanmean(ex_ap)):.4f}", f"{d_m:.4f}", f"{d_b:.4f}",
                    f"{d_h_:.4f}", str(len(jr)), str(rep), str(cas)])
            print(f"  {c:<26}{axe:<19}mu median {mu_median[(c, axe)]:.1f}, "
                  f"net reparation {rep - cas:+d}, {time.time() - t0:.0f} s")
    with open(os.path.join(args.sortie, "a20-dilatation-temoin.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_dil)

    # --- bootstrap sur les personnes, meme tirage pour toutes les conditions ----
    print(f"\nBootstrap : {args.bootstrap} tirages avec remise sur les {n} participants.")
    cles = [(HUMAIN_CTRL, None, None)] + [(c, None, None) for c in AGENTS] + \
        sorted(transportes.keys(), key=str)
    mat = {(HUMAIN_CTRL, None, None): donnees[HUMAIN_CTRL]}
    mat.update({(c, None, None): donnees[c] for c in AGENTS})
    mat.update(transportes)

    boot = {(k, a, jeu, m): ([], []) for k in cles for a in AXES_TRANSPORT
            for jeu in MASQUES for m in MESURES}
    boot_ref = {(a, jeu, m): ([], []) for a in AXES_TRANSPORT for jeu in MASQUES
                for m in MESURES}
    rng_b = np.random.default_rng(args.graine + 17)
    for b in range(args.bootstrap):
        lg = rng_b.integers(0, n, size=n)
        for a in AXES_TRANSPORT:
            pr = mes.par_item(donnees[HUMAIN_REF], seg[a], a, lignes=lg)
            for jeu, msk in MASQUES.items():
                for m in MESURES:
                    boot_ref[(a, jeu, m)][0].append(float(pr[m][0][msk].sum()))
                    boot_ref[(a, jeu, m)][1].append(float(pr[m][1][msk].sum()))
            for k in cles:
                pi = mes.par_item(mat[k], seg[a], a, lignes=lg)
                for jeu, msk in MASQUES.items():
                    for m in MESURES:
                        boot[(k, a, jeu, m)][0].append(float(pi[m][0][msk].sum()))
                        boot[(k, a, jeu, m)][1].append(float(pi[m][1][msk].sum()))
        if (b + 1) % max(1, args.bootstrap // 8) == 0:
            print(f"  {b + 1}/{args.bootstrap}  ({time.time() - t0:.0f} s)", flush=True)

    def recentrer(v, cible):
        v = np.asarray(v, dtype=float)
        fini = np.isfinite(v)
        if fini.sum() < 20:
            return v
        return v - np.mean(v[fini]) + cible

    def ic95(v):
        v = np.asarray(v, dtype=float)
        v = v[np.isfinite(v)]
        if v.size < 20:
            return float("nan"), float("nan")
        return float(np.percentile(v, 2.5)), float(np.percentile(v, 97.5))

    lignes_ap = [["condition", "axe_transport", "variante", "jeu_items", "mesure",
                  "lambda_median", "ratio_inter", "inter_ic_bas", "inter_ic_haut",
                  "ratio_intra", "intra_ic_bas", "intra_ic_haut", "ratio_total",
                  "exactitude", "exact_ic_bas", "exact_ic_haut", "delta_exactitude",
                  "delta_ic_bas", "delta_ic_haut", "diversite_conservee",
                  "accord_paires", "part_changee", "un_dans_ic_inter"]]
    resultats_ap = {}
    print(f"\n{'condition':<24}{'variante':<12}{'jeu':<17}{'mesure':<22}"
          f"{'inter*':>26}{'intra*':>24}{'total':>8}")
    for k in cles:
        c, axe, variante = k
        x = mat[k]
        ex = exactitude_par_personne(x, verite, masque_ev)
        e_m, e_b, e_h = bootstrap_personnes(ex, n_tirages=2000, graine=args.graine)
        if axe:
            d_m, d_b, d_h_ = bootstrap_personnes(ex - exact_ref[c], n_tirages=2000,
                                                 graine=args.graine)
            vec_lam = lam_M2[(c, axe)] if variante != "dilatation" else None
            lam_med = float(np.median(vec_lam[items])) if vec_lam is not None \
                else mu_median[(c, axe)]
        else:
            d_m = d_b = d_h_ = 0.0
            lam_med = 1.0
        pd_ = profil_diversite(en_objets(x[:, items]), verite_obj)
        base_c = donnees[c]
        chg = float(np.mean((x[:, items] != base_c[:, items]) & (base_c[:, items] >= 0))) \
            if axe else 0.0
        for a in AXES_TRANSPORT:
            if axe is not None and a != axe:
                continue
            pi = mes.par_item(x, seg[a], a)
            for jeu, msk in MASQUES.items():
                for m in MESURES:
                    if jeu == "149 items" and m == "variance_ordinale":
                        continue
                    inter = float(pi[m][0][msk].sum())
                    intra = float(pi[m][1][msk].sum())
                    if axe is None:
                        nu = float(nulB_item[(c, a, 1.0)][m][msk].sum()) \
                            if c in AGENTS else float(ref_nul[a][m][msk].sum())
                    elif variante == "dilatation":
                        nu = float(nulA_item[(c, a, 1.0)][m][msk].sum())
                    else:
                        rv = residu_vecteur(c, a, lam_M2[(c, a)], nulB_item)
                        nu = float(rv[m][msk].sum())
                    ri_h, ra_h, t_h = ref_termes(a, msk, m)
                    pi_r, pa_r = (inter - nu) / ri_h, (intra + nu) / ra_h
                    gl = (inter + intra) / t_h
                    bi = recentrer((np.array(boot[(k, a, jeu, m)][0]) - nu) /
                                   (np.array(boot_ref[(a, jeu, m)][0]) -
                                    float(ref_nul[a][m][msk].sum())), pi_r)
                    ba = recentrer((np.array(boot[(k, a, jeu, m)][1]) + nu) /
                                   (np.array(boot_ref[(a, jeu, m)][1]) +
                                    float(ref_nul[a][m][msk].sum())), pa_r)
                    i1, i2 = ic95(bi)
                    a1_, a2_ = ic95(ba)
                    resultats_ap[(k, a, jeu, m)] = (pi_r, i1, i2, pa_r, a1_, a2_, gl,
                                                    e_m, d_m, d_b, d_h_)
                    lignes_ap.append([c, axe or "aucun", variante or "aucune", jeu, m,
                                      f"{lam_med:.2f}", f"{pi_r:.4f}", f"{i1:.4f}",
                                      f"{i2:.4f}", f"{pa_r:.4f}", f"{a1_:.4f}",
                                      f"{a2_:.4f}", f"{gl:.4f}", f"{e_m:.4f}",
                                      f"{e_b:.4f}", f"{e_h:.4f}", f"{d_m:.4f}",
                                      f"{d_b:.4f}", f"{d_h_:.4f}",
                                      f"{pd_['part_diversite_humaine']:.4f}",
                                      f"{pd_['accord_par_paires']:.4f}", f"{chg:.4f}",
                                      "oui" if i1 <= 1.0 <= i2 else "non"])
                    if a == "political_ideology" and variante in (None, "informee"):
                        print(f"{c:<24}{(variante or 'avant'):<12}{jeu:<17}"
                              f"{NOMS_MESURE[m]:<22}"
                              f"{pi_r:>9.3f} [{i1:6.3f};{i2:6.3f}]"
                              f"{pa_r:>9.3f} [{a1_:5.3f};{a2_:5.3f}]{gl:>8.3f}")
    with open(os.path.join(args.sortie, "a20-avant-apres.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_ap)

    # --- ce que change la convention d'imputation du residu -----------------
    lignes_conv = [["condition", "axe", "jeu_items", "mesure", "moment",
                    "ratio_intra_convention_a1", "ratio_intra_convention_a20", "ecart_pct"]]
    for c in AGENTS:
        for a in AXES_TRANSPORT:
            for jeu, msk in MASQUES.items():
                for m in MESURES:
                    if jeu == "149 items" and m == "variance_ordinale":
                        continue
                    for moment, cle in (("avant", (c, a, 1.0)),):
                        oi = obs_item[cle][m]
                        intra = float(oi[1][msk].sum())
                        nu = float(nulB_item[cle][m][msk].sum())
                        ra_h_a1 = float(ref_item[a][m][1][msk].sum())
                        _, ra_h, _ = ref_termes(a, msk, m)
                        v1_ = intra / ra_h_a1
                        v2_ = (intra + nu) / ra_h
                        lignes_conv.append([c, a, jeu, m, moment, f"{v1_:.4f}",
                                            f"{v2_:.4f}",
                                            f"{100 * (v2_ - v1_) / v1_:+.2f}"])
    with open(os.path.join(args.sortie, "a20-convention-residu.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_conv)

    # ==================================================================
    # 9. Effet sur les six axes, nulle A (le transport ne fige pas ces axes la)
    # ==================================================================
    print("\n" + "=" * 96)
    print("EFFET SUR LES SIX AXES quand on ne corrige que sur un seul, "
          f"mesure {NOMS_MESURE[MESURE_PRINCIPALE]} corrigee")
    print("=" * 96)
    lignes_axe = [["condition", "axe_transport", "variante", "axe_mesure", "mesure",
                   "ratio_inter_avant", "ratio_inter_apres"]]
    n_perm_axe = max(4, args.permutations // 4)
    print(f"{'condition':<24}{'transport':<18}{'variante':<12}" +
          "".join(f"{a[:11]:>13}" for a in AXES))
    for c in AGENTS:
        av = {}
        for a in AXES:
            pi = mes.par_item(donnees[c], seg[a], a)
            acc = np.zeros(n_items)
            for p in perms[:n_perm_axe]:
                acc += mes.par_item(donnees[c], seg[a][p], a)[MESURE_PRINCIPALE][0]
            nu = float(acc[garder].sum()) / n_perm_axe
            ri_h, _, _ = ref_termes(a, garder, MESURE_PRINCIPALE)
            av[a] = (float(pi[MESURE_PRINCIPALE][0][garder].sum()) - nu) / ri_h
        print(f"{c:<24}{'avant':<18}{'-':<12}" + "".join(f"{av[a]:>13.2f}" for a in AXES))
        for axe in AXES_TRANSPORT:
            for variante in ["naive", "informee", "dilatation"]:
                x = transportes[(c, axe, variante)]
                ap = {}
                for a in AXES:
                    pi = mes.par_item(x, seg[a], a)
                    acc = np.zeros(n_items)
                    for p in perms[:n_perm_axe]:
                        acc += mes.par_item(x, seg[a][p], a)[MESURE_PRINCIPALE][0]
                    nu = float(acc[garder].sum()) / n_perm_axe
                    if a == axe and variante != "dilatation":
                        rv = residu_vecteur(c, axe, lam_M2[(c, axe)], nulB_item)
                        nu = float(rv[MESURE_PRINCIPALE][garder].sum())
                    ri_h, _, _ = ref_termes(a, garder, MESURE_PRINCIPALE)
                    ap[a] = (float(pi[MESURE_PRINCIPALE][0][garder].sum()) - nu) / ri_h
                    lignes_axe.append([c, axe, variante, a, MESURE_PRINCIPALE,
                                       f"{av[a]:.4f}", f"{ap[a]:.4f}"])
                print(f"{'':<24}{axe:<18}{variante:<12}" +
                      "".join(f"{ap[a]:>13.2f}" for a in AXES))
    with open(os.path.join(args.sortie, "a20-par-axe.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_axe)

    # ==================================================================
    # 10. Le transport rejoue SOUS M3, sur les 70 items ordinaux
    # ==================================================================
    print("\n" + "=" * 96)
    print("TRANSPORT SOUS M3, sur les 70 items ordinaux, lambda calibre sur M3 corrigee")
    print("Criteres 2 (exactitude) et 3 (A6) de a7.")
    print("=" * 96)
    masque_ev_ord = np.zeros_like(verite, dtype=bool)
    masque_ev_ord[:, items_ord] = verite[:, items_ord] >= 0
    exact_ref_ord = {c: exactitude_par_personne(donnees[c], verite, masque_ev_ord)
                     for c in AGENTS}
    d_h = matrice_distance(verite, garder_ord)
    iu = np.triu_indices(n, 1)
    d_h_v = d_h[iu]

    lignes_m3 = [["condition", "axe_transport", "variante", "lambda_median",
                  "ratio_inter_avant", "ratio_inter_apres", "inter_ic_bas",
                  "inter_ic_haut", "ratio_intra_avant", "ratio_intra_apres",
                  "intra_ic_bas", "intra_ic_haut", "ratio_total", "plafond",
                  "exactitude_70_avant", "exactitude_70_apres", "delta_70",
                  "delta_70_ic_bas", "delta_70_ic_haut", "exactitude_149_apres",
                  "delta_149", "delta_149_ic_bas", "delta_149_ic_haut",
                  "un_dans_ic_inter", "un_dans_ic_intra"]]
    lignes_a6 = [["condition", "axe_transport", "variante", "verite", "n_change",
                  "n_reparation", "n_casse", "net", "taux_reparation",
                  "spearman_avant", "spearman_apres"]]
    transp_m3, journ_m3 = {}, {}
    rng_b3 = np.random.default_rng(args.graine + 31)
    tirages_m3 = [rng_b3.integers(0, n, size=n) for _ in range(args.bootstrap)]
    print(f"\n{'condition':<24}{'axe':<19}{'variante':<11}{'lam':>5}"
          f"{'inter av':>10}{'inter ap':>24}{'intra ap':>24}{'plafond':>9}{'net A6':>9}")
    for c in AGENTS:
        d_av = matrice_distance(donnees[c], garder_ord)
        rho_av = float(spearmanr(d_h_v, d_av[iu])[0])
        for axe in AXES_TRANSPORT:
            vec = lam_M3[(c, axe)]
            rv = residu_vecteur(c, axe, vec, nulB_item)
            nu = float(rv["variance_ordinale"][garder_ord].sum())
            nu_av = float(nulB_item[(c, axe, 1.0)]["variance_ordinale"][garder_ord].sum())
            ri_h, ra_h, t_h = ref_termes(axe, garder_ord, "variance_ordinale")
            pia = mes.par_item(donnees[c], seg[axe], axe)
            av_i = (float(pia["variance_ordinale"][0][garder_ord].sum()) - nu_av) / ri_h
            av_a = (float(pia["variance_ordinale"][1][garder_ord].sum()) + nu_av) / ra_h
            plaf = plafonds[(c, axe, "70 items ordinaux", "variance_ordinale")][2]
            for variante in ["naive", "informee"]:
                jr = []
                xt = transporter(donnees[c], seg[axe], vec, items_ord, k_par_item,
                                 scores=None if variante == "naive" else scores[c],
                                 rng=np.random.default_rng(args.graine + 29), journal=jr)
                transp_m3[(c, axe, variante)] = xt
                journ_m3[(c, axe, variante)] = jr
                pi = mes.par_item(xt, seg[axe], axe)
                ap_i = (float(pi["variance_ordinale"][0][garder_ord].sum()) - nu) / ri_h
                ap_a = (float(pi["variance_ordinale"][1][garder_ord].sum()) + nu) / ra_h
                tot = (float(pi["variance_ordinale"][0][garder_ord].sum()) +
                       float(pi["variance_ordinale"][1][garder_ord].sum())) / t_h
                bi, ba = [], []
                for lg in tirages_m3:
                    p1 = mes.par_item(xt, seg[axe], axe, lignes=lg)
                    p0 = mes.par_item(donnees[HUMAIN_REF], seg[axe], axe, lignes=lg)
                    dh = float(p0["variance_ordinale"][0][garder_ord].sum())
                    dh_a = float(p0["variance_ordinale"][1][garder_ord].sum())
                    rh = float(ref_nul[axe]["variance_ordinale"][garder_ord].sum())
                    bi.append((float(p1["variance_ordinale"][0][garder_ord].sum()) - nu)
                              / (dh - rh))
                    ba.append((float(p1["variance_ordinale"][1][garder_ord].sum()) + nu)
                              / (dh_a + rh))
                i1, i2 = ic95(recentrer(bi, ap_i))
                a1_, a2_ = ic95(recentrer(ba, ap_a))
                ex70 = exactitude_par_personne(xt, verite, masque_ev_ord)
                ex149 = exactitude_par_personne(xt, verite, masque_ev)
                d70 = bootstrap_personnes(ex70 - exact_ref_ord[c], n_tirages=2000,
                                          graine=args.graine)
                d149 = bootstrap_personnes(ex149 - exact_ref[c], n_tirages=2000,
                                           graine=args.graine)
                lignes_m3.append([c, axe, variante, f"{float(np.median(vec[items_ord])):.2f}",
                                  f"{av_i:.4f}", f"{ap_i:.4f}", f"{i1:.4f}", f"{i2:.4f}",
                                  f"{av_a:.4f}", f"{ap_a:.4f}", f"{a1_:.4f}", f"{a2_:.4f}",
                                  f"{tot:.4f}", f"{plaf:.4f}",
                                  f"{float(np.nanmean(exact_ref_ord[c])):.4f}",
                                  f"{float(np.nanmean(ex70)):.4f}", f"{d70[0]:.4f}",
                                  f"{d70[1]:.4f}", f"{d70[2]:.4f}",
                                  f"{float(np.nanmean(ex149)):.4f}", f"{d149[0]:.4f}",
                                  f"{d149[1]:.4f}", f"{d149[2]:.4f}",
                                  "oui" if i1 <= 1.0 <= i2 else "non",
                                  "oui" if a1_ <= 1.0 <= a2_ else "non"])
                d_ap = matrice_distance(xt, garder_ord)
                rho_ap = float(spearmanr(d_h_v, d_ap[iu])[0])
                for nom_v, vv in (("vague1", donnees[HUMAIN_REF]),
                                  ("vague2", donnees[HUMAIN_CTRL])):
                    rep = cas = ntot = 0
                    for (i, j, r_src, r_dst) in jr:
                        t = vv[i, j]
                        if t < 0:
                            continue
                        ntot += 1
                        if r_dst == t and r_src != t:
                            rep += 1
                        elif r_src == t and r_dst != t:
                            cas += 1
                    lignes_a6.append([c, axe, variante, nom_v, str(ntot), str(rep),
                                      str(cas), str(rep - cas),
                                      f"{rep / ntot if ntot else float('nan'):.4f}",
                                      f"{rho_av:.4f}", f"{rho_ap:.4f}"])
                    if nom_v == "vague1":
                        net_v1 = rep - cas
                print(f"{c:<24}{axe:<19}{variante:<11}"
                      f"{float(np.median(vec[items_ord])):>5.1f}{av_i:>10.3f}"
                      f"{ap_i:>9.3f} [{i1:6.3f};{i2:6.3f}]"
                      f"{ap_a:>9.3f} [{a1_:5.3f};{a2_:5.3f}]{plaf:>9.3f}{net_v1:>9d}")
    with open(os.path.join(args.sortie, "a20-m3-ordinal.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_m3)
    with open(os.path.join(args.sortie, "a20-m3-critere-a6.csv"), "w", newline="",
              encoding="utf-8") as fh:
        csv.writer(fh).writerows(lignes_a6)

    # ==================================================================
    # 11. Figure
    # ==================================================================
    tracer(args.sortie, obs_item, nulA_item, nulB_item, ref_termes, ref_nul, ref_item,
           MASQUES, plafonds, lignes_m3, resultats_ap, lam_M2, items)
    print(f"\nTermine en {time.time() - t0:.0f} s. Fichiers dans {args.sortie}/")


def tracer(sortie, obs_item, nulA_item, nulB_item, ref_termes, ref_nul, ref_item,
           MASQUES, plafonds, lignes_m3, resultats_ap, lam_M2, items):
    """Quatre panneaux, un par question du rapport.

    a) le terme inter a lambda 0, brut et sous les deux nulles : l'objection 4 en image ;
    b) la trajectoire corrigee dans le plan (inter, intra), mesure principale ;
    c) la meme trajectoire sous M3 sur les 70 items ordinaux, ou le plafond depasse 1 ;
    d) le plafond intra a inter nul, par mesure et par jeu d'items : l'objection 5.
    """
    fig, axs = plt.subplots(2, 2, figsize=(14.6, 11.4))
    couleurs = ["#1b6ca8", "#c1553b", "#2f8f5b", "#7a4fa3"]
    marques = ["o", "s", "^", "D"]
    axe0 = "political_ideology"

    # --- a) l'objection 4 ------------------------------------------------
    ax = axs[0][0]
    largeur, ecart = 0.26, 0.0
    labels, brut_v, nA_v, nB_v = [], [], [], []
    for m, jeu in (("entropie", "149 items"), ("gini_simpson", "149 items"),
                   ("variance_ordinale", "70 items ordinaux")):
        msk = MASQUES[jeu]
        for c in AGENTS:
            cle = (c, axe0, 0.0)
            oi = obs_item[cle][m]
            inter = float(oi[0][msk].sum())
            ri_h, _, _ = ref_termes(axe0, msk, m)
            denom_brut = ri_h + float(ref_nul[axe0][m][msk].sum())
            labels.append(f"{NOMS_MESURE[m][:2]} {c.split('(')[0].strip()[7:]}")
            brut_v.append(inter / denom_brut)
            nA_v.append((inter - float(nulA_item[cle][m][msk].sum())) / ri_h)
            nB_v.append((inter - float(nulB_item[cle][m][msk].sum())) / ri_h)
    xpos = np.arange(len(labels))
    ax.bar(xpos - largeur, brut_v, largeur, color="#c1553b",
           label="estimateur de a7 (brut)")
    ax.bar(xpos, nA_v, largeur, color="#e0a458",
           label="nulle A, permutation seule")
    ax.bar(xpos + largeur, nB_v, largeur, color="#1b6ca8",
           label="nulle B, permutation puis transport :\nentre -0,001 et +0,001, soit zero")
    ax.scatter(xpos + largeur, nB_v, marker="o", s=26, color="#1b6ca8",
               edgecolors="k", linewidths=0.5, zorder=5)
    ax.axhline(0.0, color="0.2", lw=1.0)
    ax.set_xticks(xpos)
    ax.set_xticklabels(labels, rotation=68, ha="right", fontsize=7)
    ax.set_ylabel("Ratio inter estime a lambda = 0\n(la valeur vraie est 0)", fontsize=10)
    ax.set_title("a) Objection 4 : a lambda 0 l'operateur annule l'information mutuelle\n"
                 "empirique. L'estimateur de a7 rend -0,06 a -0,15. "
                 "Axe : ideologie.", fontsize=10.5)
    ax.legend(fontsize=8, loc="lower right")
    ax.grid(True, axis="y", color="0.9", lw=0.6)
    ax.set_axisbelow(True)

    # --- b) trajectoire corrigee, mesure principale ----------------------
    for col, (m, jeu, titre) in enumerate([
            (MESURE_PRINCIPALE, "149 items",
             "b) Trajectoire corrigee, M2 Gini Simpson, 149 items"),
            ("variance_ordinale", "70 items ordinaux",
             "c) Trajectoire corrigee, M3 variance ordinale, 70 items ordinaux")]):
        ax = axs[0][1] if col == 0 else axs[1][0]
        msk = MASQUES[jeu]
        for ic_, c in enumerate(AGENTS):
            xs, ys, xb, yb = [], [], [], []
            for lam in LAMBDAS:
                cle = (c, axe0, lam)
                oi = obs_item[cle][m]
                inter = float(oi[0][msk].sum())
                intra = float(oi[1][msk].sum())
                nu = float(nulB_item[cle][m][msk].sum())
                ri_h, ra_h, _ = ref_termes(axe0, msk, m)
                nu_h = float(ref_nul[axe0][m][msk].sum())
                xs.append((inter - nu) / ri_h)
                ys.append((intra + nu) / ra_h)
                # trajectoire de a7 : estimateur brut au numerateur ET au denominateur,
                # terme intra sans imputation du residu. C'est ce que a7 publie.
                xb.append(inter / (ri_h + nu_h))
                yb.append(intra / (ra_h - nu_h))
            ax.plot(xb, yb, ":", color="0.62", lw=1.1, zorder=1)
            ax.plot(xs, ys, "-", color=couleurs[ic_], lw=1.4, zorder=2)
            ax.scatter(xs, ys, marker=marques[ic_], s=46, color=couleurs[ic_],
                       edgecolors="k", linewidths=0.4, zorder=3, label=c)
            plaf = plafonds[(c, axe0, jeu, m)][2]
            ax.axhline(plaf, color=couleurs[ic_], lw=0.8, ls="--", alpha=0.6)
        ax.axhline(1.0, color="0.75", lw=0.8)
        ax.axvline(1.0, color="0.75", lw=0.8)
        ax.plot([1], [1], marker="*", ms=19, color="crimson", zorder=6)
        ax.annotate("humains vague 1", (1, 1), fontsize=8.5, xytext=(6, 6),
                    textcoords="offset points", color="crimson", ha="left")
        ax.set_xlim(-0.35, 3.35)
        ax.set_ylim(0.70, 1.09)
        ax.annotate("les agents demographiques (v8) partent de 8,1 hors cadre",
                    xy=(0.985, 0.02), xycoords="axes fraction", fontsize=7.5,
                    color="0.35", ha="right")
        # Le message central : meme quand le plafond depasse 1, la trajectoire ne passe
        # pas par (1, 1). Atteindre (1, 1) exigerait T = 1, et T vaut au mieux 0,95.
        ax.annotate("aucune trajectoire ne passe par (1, 1) :\n"
                    "cela exigerait un ratio de dispersion\ntotale T egal a 1, "
                    "or T vaut au mieux 0,95",
                    xy=(0.985, 0.63), xycoords="axes fraction", fontsize=7.8,
                    color="crimson", ha="right", va="top",
                    bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                              edgecolor="none", alpha=0.85))
        ax.set_xlabel("Ratio de dispersion ENTRE segments, residu recalibre a chaque lambda",
                      fontsize=9.5)
        ax.set_ylabel("Ratio de dispersion A L'INTERIEUR des segments", fontsize=9.5)
        ax.set_title(titre + "\ntirets horizontaux : plafond T / (1 - w) ; "
                     "pointille gris : trajectoire publiee par a7", fontsize=10.5)
        ax.grid(True, color="0.92", lw=0.6)
        ax.set_axisbelow(True)
        if col == 1:
            ax.legend(fontsize=8, loc="lower left", framealpha=0.95)

    # --- d) l'objection 5 : les plafonds ---------------------------------
    ax = axs[1][1]
    groupes = [("entropie", "149 items"), ("gini_simpson", "149 items"),
               ("entropie", "70 items ordinaux"), ("gini_simpson", "70 items ordinaux"),
               ("variance_ordinale", "70 items ordinaux")]
    largeur = 0.16
    for ic_, c in enumerate(AGENTS):
        vals, poss = [], []
        for ig, (m, jeu) in enumerate(groupes):
            for iaxe, axe in enumerate(AXES_TRANSPORT):
                vals.append(plafonds[(c, axe, jeu, m)][2])
                poss.append(ig * 1.0 + (ic_ - 1.5) * largeur +
                            (0.035 if iaxe else -0.035))
        ax.scatter(poss, vals, marker=marques[ic_], s=48, color=couleurs[ic_],
                   edgecolors="k", linewidths=0.4, label=AGENTS[ic_], zorder=3)
    ax.axhline(1.0, color="crimson", lw=1.2)
    ax.text(0.02, 1.005, "plafond = 1 : le transport pur suffit au dessus de cette ligne",
            transform=ax.get_yaxis_transform(), fontsize=8, color="crimson", va="bottom")
    ax.set_xticks(np.arange(len(groupes)))
    ax.set_xticklabels([f"{NOMS_MESURE[m][:2]}\n{jeu}" for m, jeu in groupes], fontsize=8)
    ax.set_ylabel("Plafond du ratio intra a terme inter nul, T / (1 - w)", fontsize=10)
    ax.set_title("d) Objection 5 : l'impossibilite depend de la mesure ET du jeu d'items\n"
                 "deux points par condition, un par axe de transport", fontsize=10.5)
    ax.legend(fontsize=8, loc="upper left")
    ax.grid(True, axis="y", color="0.92", lw=0.6)
    ax.set_axisbelow(True)

    fig.suptitle(
        "a20. Le transport de variance rejoue : residu de permutation recalibre a chaque "
        "lambda, et plafond calcule pour les trois mesures\n"
        "GSS, archive OSF t6g7k, 1052 participants, 149 items dont 70 ordinaux, "
        "estimateurs de a1, operateur de a7, axe de transport : ideologie politique",
        fontsize=11.5)
    fig.tight_layout(rect=[0, 0, 1, 0.955])
    for ext in ("png", "svg"):
        fig.savefig(os.path.join(sortie, f"a20-figure-transport-v2.{ext}"), dpi=175,
                    bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    main()
