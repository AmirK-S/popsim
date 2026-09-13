"""
c7_decomposition_signal : les 20,7 % sont-ils une trace de personne, ou une structure
de population qu'un modele de langage reproduit bien ?

===========================================================================
PREENREGISTREMENT : resultats/c7-decomposition-signal-preenregistrement.md, ecrit et
commite le 13 septembre 2026 AVANT ce fichier et avant tout calcul de decomposition.

CE QU'ON ATTAQUE. L'objection R4 de resultats/relecture-post-nuit-2026-09-13.md : un
jumeau conditionne sur le seul segment demographique, qui n'a jamais vu l'individu,
atteint deja 2,15 %. Une part inconnue des 20,7 % pourrait donc n'etre pas une trace de
personne mais une structure de population. La decomposition personne / segment /
population existe pour le canal entre jumeaux ; elle n'existe pas pour l'attaque qui
porte le titre de l'article.

ETUDE DE RISQUE DE VIE PRIVEE sur un jeu deja public (Twin-2K-500). Ce script ne calcule,
n'imprime et n'ecrit JAMAIS l'identite ou le pid d'une personne retrouvee, ni aucune
liste d'appariements individuels. Seuls des taux agreges et des tailles de segment
sortent dans resultats/.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                        les quinze tables de Twin, dont le segment S_gra
  c7_reidentification.items_communs        les 60 items toujours renseignes
  c7_reidentification.rangs_attaque        l'attaque de reidentification elle meme
  c7_reidentification.rang_dans_segment    le rang a pool restreint au segment
  c7_reidentification.graine_nom           graine stable par nom
  c7_reidentification.REF_V4 / REF_V13 / DEMO / N_BOOTSTRAP
  a2_commun.distance_hamming               la distance, masquage deja fait
  a2_commun.bootstrap_personnes            l'IC a 95 % par reechantillonnage de personnes
  c7_controle_interpretabilite.controle_avant_interpretation

CE QUI EST NOUVEAU ICI :
  1. Les deux planchers de population que l'objection appelle : un generateur a marginales
     independantes (aucune structure de dependance) et un VECTEUR HUMAIN REEL d'une autre
     personne (structure de dependance parfaitement realiste, zero information sur la
     cible). Le second est la forme la plus dure de l'objection : si le realisme de la
     structure de dependance suffisait a identifier, ce generateur la identifierait.
  2. Le plafond de segment E[1/|S_gra|], et son incarnation : un vecteur humain reel d'une
     autre personne DU MEME SEGMENT.
  3. Le temoin a segment constant : AUC intra-segment, la probabilite que le jumeau de la
     personne i s'accorde mieux avec i qu'avec un rival j du meme segment, ex aequo comptes
     une demi-unite. 0,5 = aucune trace de personne. Cette quantite NE DEPEND D'AUCUNE
     CONVENTION DE DEPARTAGE, contrairement au top-1.
  4. Le controle d'echangeabilite : verifier sur les sorties elles-memes que le jumeau
     Demographics Only ne porte pas d'information individuelle.

CONVENTION D'EX AEQUO, DECLAREE. Les top-1 emploient la convention du depot : depart
aleatoire moyenne sur 20 tirages, graine fixee (c7_reidentification.rangs_attaque). Le
depot a mesure que la convention vaut un facteur 1,32 sur Twin et jusqu'a 130 ailleurs
(c7-residu-trajectoire-resultats.md, section 7) : aucun top-1 n'est publie sans elle.
L'AUC intra-segment, elle, compte les ex aequo une demi-unite et ne depend d'aucun tirage.

Aucun appel de modele de langage. Lecture seule sur data/. Aucun script existant modifie.
Usage : .venv/bin/python analyses/c7_decomposition_signal.py
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

import t1_commun as T1                                          # noqa: E402
from a2_commun import distance_hamming, bootstrap_personnes      # noqa: E402
from c7_reidentification import (                                # noqa: E402
    items_communs, rangs_attaque, rang_dans_segment, graine_nom,
    REF_V4, REF_V13, DEMO, N_BOOTSTRAP,
)
import c7_controle_interpretabilite as CTL                       # noqa: E402

GRAINE = 20260913
LLM_REF = "JSON Persona - GPT4.1"
SEG_PRINCIPAL = "S_gra"          # genre x ethnicite x age, la lecture principale du depot
SEG_ROBUSTESSE = "S_fin"         # bloc d'ideologie x genre x age


# ---------------------------------------------------------------------------
# Les generateurs de plancher : population, puis population + segment
# ---------------------------------------------------------------------------

def gen_marginales_population(pool, rng):
    """N1a : chaque item tire independamment dans sa marginale de population.

    Aucune structure de dependance entre items, aucune information de segment, aucune
    information individuelle. C'est le plancher le plus nu.
    """
    n, p = pool.shape
    out = np.empty_like(pool)
    for j in range(p):
        col = pool[:, j]
        obs = col[col >= 0]
        out[:, j] = rng.choice(obs, size=n, replace=True) if len(obs) else -1
    return out


def _derangement(groupes, rng):
    """Pour chaque personne, l'index d'une AUTRE personne du meme groupe.

    groupes : etiquette de groupe par personne (un seul groupe = population entiere).
    Repare les points fixes en echangeant avec un voisin du meme groupe, ce qui garantit
    qu'aucune personne ne se recoit elle-meme.
    """
    n = len(groupes)
    don = np.arange(n)
    for g in np.unique(groupes):
        idx = np.flatnonzero(groupes == g)
        if len(idx) < 2:
            don[idx] = idx           # groupe singleton : rien a permuter, signale en aval
            continue
        perm = rng.permutation(idx)
        fixes = np.flatnonzero(perm == idx)
        for f in fixes:               # echange avec le suivant dans le groupe
            autre = (f + 1) % len(idx)
            perm[f], perm[autre] = perm[autre], perm[f]
        don[idx] = perm
    return don


def gen_humain_autre(pool, rng, groupes=None):
    """N1b / N2a : le vecteur de reponses REEL d'une AUTRE personne.

    groupes=None : tiree dans la population entiere -> structure de dependance
    parfaitement realiste (c'est un humain), zero information sur la cible.
    groupes=segment : tiree dans le meme segment -> structure realiste ET segment correct.
    """
    g = np.zeros(pool.shape[0], dtype=np.int32) if groupes is None else groupes
    don = _derangement(g, rng)
    return pool[don], don


# ---------------------------------------------------------------------------
# Le temoin qui tranche : a segment constant, sans convention de departage
# ---------------------------------------------------------------------------

def auc_intra_segment(vec_test, pool, vrai_idx, seg):
    """P(accord(jumeau_i, personne_i) > accord(jumeau_i, rival_j du meme segment)).

    Les ex aequo comptent une demi-unite : aucune convention de departage, aucun tirage,
    aucune graine n'intervient. 0,5 = le jumeau ne distingue PAS sa personne d'une autre
    personne du meme segment, c'est-a-dire aucune trace de personne.

    Renvoie, par personne attaquee : l'AUC intra-segment, et la taille de son segment.
    Les personnes dont le segment compte moins de deux membres recoivent NaN (elles
    n'ont pas de rival) et sont exclues des agregats, ce qui est signale dans le CSV.
    """
    n = vec_test.shape[0]
    auc = np.full(n, np.nan)
    taille = np.zeros(n, dtype=int)
    seg_vrai = seg[vrai_idx]
    for g in np.unique(seg_vrai):
        if g < 0:
            continue
        membres = np.flatnonzero(seg_vrai == g)      # lignes de vec_test
        idx_seg = np.flatnonzero(seg == g)            # colonnes du pool
        if len(idx_seg) < 2:
            continue
        accord = 1.0 - distance_hamming(vec_test[membres], pool[idx_seg])
        pos = np.searchsorted(idx_seg, vrai_idx[membres])
        propre = accord[np.arange(len(membres)), pos]
        mieux = accord < propre[:, None]
        egal = accord == propre[:, None]
        # la colonne de la personne elle-meme est retiree du denominateur
        mieux[np.arange(len(membres)), pos] = False
        egal[np.arange(len(membres)), pos] = False
        n_rivaux = len(idx_seg) - 1
        auc[membres] = (mieux.sum(axis=1) + 0.5 * egal.sum(axis=1)) / n_rivaux
        taille[membres] = len(idx_seg)
    return auc, taille


def rival_demographique(X_demo):
    """Pour chaque personne, le rival demographiquement LE PLUS PROCHE (hors elle-meme).

    X_demo : les 14 reponses du bloc Demographics du catalogue, en chaines. Le rival est
    l'autre personne qui partage le plus de ces 14 reponses. C'est la forme la plus dure
    du temoin : si le jumeau segment-seul ne fait que de la demographie, il ne doit pas
    savoir distinguer sa personne de son voisin demographique le plus proche.
    Renvoie l'index du rival et le nombre de reponses demographiques partagees.
    """
    n = X_demo.shape[0]
    codes = np.zeros(X_demo.shape, dtype=np.int32)
    for j in range(X_demo.shape[1]):
        _, codes[:, j] = np.unique(X_demo[:, j], return_inverse=True)
    rival = np.zeros(n, dtype=int)
    partage = np.zeros(n, dtype=int)
    for i in range(n):
        acc = (codes == codes[i]).sum(axis=1)
        acc[i] = -1
        rival[i] = int(np.argmax(acc))
        partage[i] = int(acc[rival[i]])
    return rival, partage


def auc_rival_unique(x, pool, rival):
    """AUC contre UN SEUL rival apparie : 0,5 = le jumeau ne distingue pas sa personne
    de ce rival-la. Ex aequo comptes une demi-unite ; aucune convention de departage."""
    n = pool.shape[0]
    accord_propre = np.zeros(n)
    accord_rival = np.zeros(n)
    for i in range(n):
        a = x[i]
        for cible, sortie in ((pool[i], accord_propre), (pool[rival[i]], accord_rival)):
            commun = (a >= 0) & (cible >= 0)
            sortie[i] = (a[commun] == cible[commun]).mean() if commun.any() else 0.0
    return ((accord_propre > accord_rival) + 0.5 * (accord_propre == accord_rival))


def echangeabilite(x, seg):
    """Le jumeau porte-t-il une information individuelle, ou seulement de groupe ?

    Trois diagnostics agreges, aucune donnee individuelle :
      - part de vecteurs de reponses DISTINCTS parmi les jumeaux ;
      - distance de Hamming moyenne entre deux jumeaux du MEME segment ;
      - la meme entre deux jumeaux de segments DIFFERENTS.
    Un objet conditionne sur le seul segment doit etre plus homogene a l'interieur d'un
    segment qu'entre segments (il a bien recu le segment) sans pour autant distinguer
    ses membres (c'est l'AUC intra-segment qui le mesure).
    """
    n = x.shape[0]
    distinct = len({tuple(r.tolist()) for r in x}) / n
    d = distance_hamming(x, x)
    meme = seg[:, None] == seg[None, :]
    hors_diag = ~np.eye(n, dtype=bool)
    return {
        "part_vecteurs_distincts": float(distinct),
        "hamming_moyen_meme_segment": float(d[meme & hors_diag].mean()),
        "hamming_moyen_autre_segment": float(d[(~meme) & hors_diag].mean()),
    }


# ---------------------------------------------------------------------------
# Mesure d'une condition sur un bloc d'items
# ---------------------------------------------------------------------------

def mesurer(nom, x, pool, seg, rng, graine_ic):
    n = pool.shape[0]
    vrai = np.arange(n)
    rang, top1, top10 = rangs_attaque(x, pool, vrai, rng)
    rang_s, top1_s, taille_s = rang_dans_segment(x, vrai, pool, seg, rng)
    auc, taille_auc = auc_intra_segment(x, pool, vrai, seg)
    ok = ~np.isnan(auc)

    m_t1, b_t1, h_t1 = bootstrap_personnes(top1, N_BOOTSTRAP, [GRAINE, graine_ic, 1])
    m_t10, b_t10, h_t10 = bootstrap_personnes(top10, N_BOOTSTRAP, [GRAINE, graine_ic, 2])
    m_ts, b_ts, h_ts = bootstrap_personnes(top1_s[ok], N_BOOTSTRAP, [GRAINE, graine_ic, 3])
    m_a, b_a, h_a = bootstrap_personnes(auc[ok], N_BOOTSTRAP, [GRAINE, graine_ic, 4])

    exact = float(np.mean((x == pool)[(x >= 0) & (pool >= 0)]))
    return {
        "condition": nom, "n_attaques": int(n), "n_pool": int(n),
        "n_items": int(pool.shape[1]), "exactitude": exact,
        "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
        "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
        "rang_median": float(np.median(rang)),
        "top1_hasard": 1.0 / n,
        "top1_intra_segment": m_ts, "top1_intra_segment_bas": b_ts,
        "top1_intra_segment_haut": h_ts,
        "rang_intra_segment_median": float(np.median(rang_s[ok])),
        "hasard_intra_segment": float(np.mean(1.0 / taille_auc[ok])),
        "auc_intra_segment": m_a, "auc_intra_segment_bas": b_a,
        "auc_intra_segment_haut": h_a,
        "n_avec_rival": int(ok.sum()),
        "taille_segment_mediane": float(np.median(taille_auc[ok])),
    }, auc


# ---------------------------------------------------------------------------

def parts(t_personne, t_segment, t_hasard):
    """Les deux echelles preenregistrees. Aucune n'est canonique : les deux sont publiees."""
    taux = (t_personne - t_segment) / t_personne
    bits_total = np.log2(t_personne / t_hasard)
    bits_seg = np.log2(t_segment / t_hasard)
    return {
        "part_personne_echelle_taux": float(taux),
        "part_segment_echelle_taux": float((t_segment - t_hasard) / t_personne),
        "part_population_echelle_taux": float(t_hasard / t_personne),
        "bits_total": float(bits_total),
        "bits_segment": float(bits_seg),
        "bits_personne": float(bits_total - bits_seg),
        "part_personne_echelle_bits": float((bits_total - bits_seg) / bits_total),
        "part_segment_echelle_bits": float(bits_seg / bits_total),
    }


def main():
    t0 = time.time()
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    codes = paq["codes"]
    seg = paq["seg"][SEG_PRINCIPAL]
    seg_rob = paq["seg"][SEG_ROBUSTESSE]
    n = paq["n"]

    items = items_communs(codes, [REF_V4, REF_V13])
    noms_items = [paq["colonnes"][i] for i in items]
    est_achat = np.array([c.endswith("_Q295") for c in noms_items])
    print(f"[1] bassin : {n} personnes, {len(items)} items, dont "
          f"{int(est_achat.sum())} de suffixe _Q295 ; segmentation {SEG_PRINCIPAL} : "
          f"{len(np.unique(seg[seg >= 0]))} segments", flush=True)

    pool_plein = codes[REF_V4][:, items]

    # --- les generateurs de plancher, construits une fois sur les 60 items -------
    rng = np.random.default_rng([GRAINE, 1])
    g_marg = gen_marginales_population(pool_plein, rng)
    g_autre, _ = gen_humain_autre(pool_plein, np.random.default_rng([GRAINE, 2]))
    g_autre_seg, _ = gen_humain_autre(pool_plein, np.random.default_rng([GRAINE, 3]),
                                      groupes=seg)

    conditions = {
        "N1a marginales independantes de population": g_marg,
        "N1b vecteur humain reel d'une autre personne (population)": g_autre,
        "N2a vecteur humain reel d'une autre personne du meme segment": g_autre_seg,
        "N2b jumeau Demographics Only (segment seul)": codes[DEMO][:, items],
        "N3 jumeau JSON Persona - GPT4.1 (persona individuelle)": codes[LLM_REF][:, items],
        "plafond : retest humain vagues 1-3": codes[REF_V13][:, items],
    }

    blocs = [("tous", np.arange(len(items)))]
    if est_achat.any() and (~est_achat).any():
        blocs.append(("items d'achat", np.flatnonzero(est_achat)))
        blocs.append(("items hors achat", np.flatnonzero(~est_achat)))

    lignes = []
    aucs = {}
    for etiquette, sel in blocs:
        pool = pool_plein[:, sel]
        for nom, x in conditions.items():
            r, auc = mesurer(nom, x[:, sel], pool, seg,
                             np.random.default_rng([GRAINE, graine_nom(nom + etiquette)]),
                             graine_nom(nom + etiquette) % 100000)
            r["bloc_items"] = etiquette
            r["segmentation"] = SEG_PRINCIPAL
            lignes.append(r)
            aucs[(etiquette, nom)] = auc
            print(f"  [{etiquette:<17}] {nom:<58} top1={r['top1']*100:6.3f} % "
                  f"t1_intra={r['top1_intra_segment']*100:6.3f} % "
                  f"AUC_intra={r['auc_intra_segment']:.4f} "
                  f"[{r['auc_intra_segment_bas']:.4f};{r['auc_intra_segment_haut']:.4f}]",
                  flush=True)
        print(f"  ... {time.time()-t0:.0f} s", flush=True)

    # --- robustesse : la meme chose sous une AUTRE segmentation -----------------
    print(f"[2] robustesse sous {SEG_ROBUSTESSE} ({time.time()-t0:.0f} s)", flush=True)
    for nom in ("N2b jumeau Demographics Only (segment seul)",
                "N3 jumeau JSON Persona - GPT4.1 (persona individuelle)"):
        x = conditions[nom]
        auc, taille = auc_intra_segment(x, pool_plein, np.arange(n), seg_rob)
        ok = ~np.isnan(auc)
        m, b, h = bootstrap_personnes(auc[ok], N_BOOTSTRAP, [GRAINE, 77])
        lignes.append({"condition": nom, "bloc_items": "tous",
                       "segmentation": SEG_ROBUSTESSE, "n_items": len(items),
                       "n_attaques": n, "n_pool": n,
                       "auc_intra_segment": m, "auc_intra_segment_bas": b,
                       "auc_intra_segment_haut": h, "n_avec_rival": int(ok.sum()),
                       "taille_segment_mediane": float(np.median(taille[ok])),
                       "hasard_intra_segment": float(np.mean(1.0 / taille[ok]))})
        print(f"  {nom:<58} AUC_intra({SEG_ROBUSTESSE})={m:.4f} [{b:.4f};{h:.4f}]",
              flush=True)

    # --- comparaison appariee persona contre segment-seul, par personne ---------
    print(f"[3] comparaison appariee a segment constant ({time.time()-t0:.0f} s)",
          flush=True)
    for etiquette, _sel in blocs:
        a = aucs[(etiquette, "N3 jumeau JSON Persona - GPT4.1 (persona individuelle)")]
        b_ = aucs[(etiquette, "N2b jumeau Demographics Only (segment seul)")]
        ok = (~np.isnan(a)) & (~np.isnan(b_))
        m, lo, hi = bootstrap_personnes(a[ok] - b_[ok], N_BOOTSTRAP, [GRAINE, 88])
        lignes.append({"condition": "ecart apparie AUC intra-segment "
                                    "(persona moins segment-seul)",
                       "bloc_items": etiquette, "segmentation": SEG_PRINCIPAL,
                       "n_avec_rival": int(ok.sum()),
                       "auc_intra_segment": m, "auc_intra_segment_bas": lo,
                       "auc_intra_segment_haut": hi})
        print(f"  [{etiquette:<17}] ecart apparie = {m:+.4f} [{lo:+.4f};{hi:+.4f}]",
              flush=True)

    # --- le temoin le plus dur : rival demographiquement le plus proche ---------
    # Verification de ce que « Demographics Only » a REELLEMENT recu. Le bloc
    # Demographics du catalogue compte 14 questions ; si leurs reponses jointes
    # distinguent presque chaque personne, alors ce jumeau n'est PAS un objet de groupe
    # et son taux ne peut pas etre attribue au niveau segment. Le nombre de cellules
    # demographiques distinctes est ecrit au CSV, c'est un agregat, pas une donnee
    # individuelle.
    print(f"[3 bis] rival demographique le plus proche ({time.time()-t0:.0f} s)",
          flush=True)
    dem = T1.demographies_brutes(paq)
    X_demo = dem["x"]
    cellules = len({tuple(r) for r in X_demo})
    rival, partage = rival_demographique(X_demo)
    print(f"  bloc Demographics : {X_demo.shape[1]} questions, {cellules} cellules "
          f"distinctes pour {n} personnes ; rival median partageant "
          f"{int(np.median(partage))} / {X_demo.shape[1]} reponses", flush=True)
    lignes.append({"condition": "diagnostic du bloc Demographics",
                   "bloc_items": "rival_demographique", "segmentation": "demographies",
                   "n_questions_demographiques": int(X_demo.shape[1]),
                   "n_cellules_demographiques_distinctes": int(cellules),
                   "n_attaques": n,
                   "partage_demographique_median": float(np.median(partage))})
    for nom in conditions:
        v = auc_rival_unique(conditions[nom], pool_plein, rival)
        m, lo, hi = bootstrap_personnes(v, N_BOOTSTRAP, [GRAINE, graine_nom(nom), 9])
        lignes.append({"condition": nom, "bloc_items": "rival_demographique",
                       "segmentation": "plus proche voisin demographique",
                       "n_items": len(items), "n_attaques": n,
                       "auc_intra_segment": m, "auc_intra_segment_bas": lo,
                       "auc_intra_segment_haut": hi})
        print(f"  {nom:<58} AUC(rival demo) = {m:.4f} [{lo:.4f};{hi:.4f}]", flush=True)

    # --- echangeabilite : de quoi le jumeau segment-seul est-il fait ? ----------
    print(f"[4] echangeabilite ({time.time()-t0:.0f} s)", flush=True)
    for nom in ("N2b jumeau Demographics Only (segment seul)",
                "N3 jumeau JSON Persona - GPT4.1 (persona individuelle)",
                "plafond : retest humain vagues 1-3"):
        d = echangeabilite(conditions[nom][:, np.arange(len(items))], seg)
        d.update({"condition": nom, "bloc_items": "echangeabilite",
                  "segmentation": SEG_PRINCIPAL, "n_items": len(items)})
        lignes.append(d)
        print(f"  {nom:<58} distincts={d['part_vecteurs_distincts']:.4f} "
              f"d_meme_seg={d['hamming_moyen_meme_segment']:.4f} "
              f"d_autre_seg={d['hamming_moyen_autre_segment']:.4f}", flush=True)

    # --- la decomposition en parts, sur les deux echelles preenregistrees -------
    df = pd.DataFrame(lignes)
    base = df[(df.bloc_items == "tous") & (df.segmentation == SEG_PRINCIPAL)]

    def val(c, col="top1"):
        s = base[base.condition == c]
        return float(s[col].iloc[0])

    t_pers = val("N3 jumeau JSON Persona - GPT4.1 (persona individuelle)")
    t_seg = val("N2b jumeau Demographics Only (segment seul)")
    t_seg_h = val("N2a vecteur humain reel d'une autre personne du meme segment")
    t_hasard = 1.0 / n
    plafond_seg = float(base[base.condition.str.startswith("N3")]
                        .hasard_intra_segment.iloc[0])

    for etiquette_seg, valeur_seg in (("jumeau segment-seul", t_seg),
                                      ("vecteur humain du meme segment", t_seg_h),
                                      ("plafond theorique E[1/|segment|]", plafond_seg)):
        p = parts(t_pers, valeur_seg, t_hasard)
        p.update({"condition": f"decomposition (niveau segment = {etiquette_seg})",
                  "bloc_items": "decomposition", "segmentation": SEG_PRINCIPAL,
                  "top1": t_pers, "niveau_segment_utilise": valeur_seg,
                  "top1_hasard": t_hasard})
        lignes.append(p)
        print(f"  segment = {etiquette_seg:<34} part personne : "
              f"taux {p['part_personne_echelle_taux']*100:.1f} % / "
              f"bits {p['part_personne_echelle_bits']*100:.1f} % "
              f"({p['bits_personne']:.2f} bits sur {p['bits_total']:.2f})", flush=True)

    # --- controle d'interpretabilite, AVANT toute interpretation ---------------
    print(f"[5] controle d'interpretabilite ({time.time()-t0:.0f} s)", flush=True)
    for nom in ("N3 jumeau JSON Persona - GPT4.1 (persona individuelle)",
                "N2a vecteur humain reel d'une autre personne du meme segment",
                "N1b vecteur humain reel d'une autre personne (population)",
                "N1a marginales independantes de population"):
        statut, detail = "passe", ""
        try:
            CTL.controle_avant_interpretation(np.arange(n), items,
                                              conditions[nom], nom, paq=paq)
        except Exception as e:                      # noqa: BLE001
            statut, detail = "echoue", str(e)[:400]
        lignes.append({"condition": nom, "bloc_items": "controle_interpretabilite",
                       "segmentation": SEG_PRINCIPAL,
                       "controle_statut": statut, "controle_detail": detail})
        print(f"  {nom:<58} {statut}", flush=True)

    T1.ecrire(pd.DataFrame(lignes), "c7-decomposition-signal.csv")
    print(f"[fin] {time.time()-t0:.0f} s", flush=True)


if __name__ == "__main__":
    main()
