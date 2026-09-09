"""
a11_evaluer_twin : evaluation des traces d'agents locaux sur Twin-2K-500.

Statut : script d'evaluation, pas du code de production. Il ne fait aucun appel de modele.
Il lit les traces produites par analyses/a11_agents_locaux_twin.py, les compare a la verite
terrain de la vague 4, et met dans le meme tableau nos conditions locales, les baselines
sans modele de langage de a2, les simulations publiees par les auteurs et le plafond humain.

Population d'evaluation. Toutes les methodes sont restreintes aux MEMES personnes et aux
MEMES cellules : les personnes de data/traces/a11-personnes.csv effectivement couvertes par
les traces, et les cellules ou la personne a reellement repondu en vague 4. La vague 4
comporte des experiences inter sujets, chaque personne ne voit qu'une condition, et une
cellule vide n'est jamais comptee comme une erreur. C'est la convention de a2 section 3.2.

Ce qui est rapporte, methode par methode :
  - exactitude par personne, avec intervalle de confiance a 95 pour cent par bootstrap sur
    les PERSONNES et non sur les cellules ;
  - exactitude normalisee par le plafond test retest DE CES PERSONNES, jamais par la
    moyenne publiee sur les 2 058 ;
  - diversite conservee et accord par paires, definitions de a2_commun, elles memes reprises
    de a0_diversite_osf ;
  - pour nos conditions seulement, qui produisent une distribution complete et pas seulement
    un argmax : exactitude esperee en tirage, confiance moyenne, ecart de calibration et
    erreur de calibration esperee.

Entree  : data/traces/a11-*.jsonl et a11-personnes.csv, data/twin2k500.
Sortie  : resultats/a11_twin_resultats.json et un tableau sur la sortie standard.

Usage :
  .venv/bin/python analyses/a11_evaluer_twin.py
  .venv/bin/python analyses/a11_evaluer_twin.py --suffixe smoke
  .venv/bin/python analyses/a11_evaluer_twin.py --sans-baselines   # rapide, traces seules
"""

import argparse
import glob
import json
import os
import re
import sys
from collections import Counter, defaultdict

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_baselines_twin import charger as charger_twin
from a2_baselines_twin import plis_personnes, K_VOISINS, LLM, SIMULATIONS
from a2_baselines_twin import GRAINE as GRAINE_DECOUPAGE
from a2_commun import (b0_marginale, b1_logistique, b2_voisins, bootstrap_personnes,
                       distance_hamming, en_codes, encodeur_demographies, est_manquant,
                       exactitude_par_personne, profil_diversite)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data/traces")
SORTIE = os.path.join(RACINE, "resultats")

CONDITIONS = ["C3b-Twin", "C2-Twin", "C3-Twin"]
N_BINS_CALIBRATION = 10


# --------------------------------------------------------------------------------------
# 1. Lecture des traces
# --------------------------------------------------------------------------------------

def lire_traces(condition, suffixe=""):
    """Lit toutes les passes disponibles d'une condition et les moyenne.

    Une passe est un ordre de presentation des modalites. La passe 1 presente l'ordre du
    catalogue, la passe 2 l'ordre inverse : c'est la parade au biais de position de a3
    section 3.4. Les deux passes ne sont comparables que dans le repere des CODES de
    modalite, pas dans celui des lettres, puisque la correspondance lettre vers modalite
    change d'une passe a l'autre. C'est pour cela que la trace transporte
    `distribution_codes` : ici on moyenne les distributions code par code.

    Retourne un dictionnaire (pid, item) -> {"p": {code: proba}, "passes": n,
    "masse": masse moyenne, "rejet": vrai si une passe au moins est rejetee}.
    """
    motif = os.path.join(TRACES, f"a11-{condition}-p*.jsonl")
    # Le motif large attraperait aussi les traces suffixees. On ne garde que celles dont
    # le nom correspond exactement a la variante demandee : melanger un smoke test de
    # trois personnes avec le run de la nuit fausserait toutes les moyennes.
    attendu = re.compile(rf"^a11-{re.escape(condition)}-p\d+"
                         + (rf"-{re.escape(suffixe)}" if suffixe else "") + r"\.jsonl$")
    fichiers = sorted(f for f in glob.glob(motif)
                      if attendu.match(os.path.basename(f)))
    brut = defaultdict(list)
    lignes_illisibles = 0
    for chemin in fichiers:
        with open(chemin, encoding="utf-8") as fh:
            for ligne in fh:
                ligne = ligne.strip()
                if not ligne:
                    continue
                try:
                    d = json.loads(ligne)
                except json.JSONDecodeError:
                    # Derniere ligne d'un fichier interrompu en cours d'ecriture.
                    lignes_illisibles += 1
                    continue
                brut[(d["pid"], d["item"])].append(d)

    sortie = {}
    for cle, appels in brut.items():
        # Une relance peut avoir reecrit un appel ; on garde la derniere occurrence de
        # chaque passe, jamais la moyenne d'un doublon avec lui meme.
        par_passe = {a.get("passe", 1): a for a in appels}
        cumul = defaultdict(float)
        for a in par_passe.values():
            for code, p in a["distribution_codes"].items():
                cumul[int(code)] += p / len(par_passe)
        sortie[cle] = {
            "p": dict(cumul),
            "passes": len(par_passe),
            "masse": float(np.mean([a["masse_lettres"] for a in par_passe.values()])),
            "rejet": any(a["rejet"] for a in par_passe.values()),
        }
    return sortie, fichiers, lignes_illisibles


# --------------------------------------------------------------------------------------
# 2. Mise des traces au format matriciel de a2
# --------------------------------------------------------------------------------------

def matrices_condition(trace, pids, cibles, y, masque):
    """Construit, pour une condition, les matrices alignees sur la cible de a2.

    Retourne :
      pred    : matrice objet des codes predits par argmax, None hors couverture ;
      p_vraie : probabilite attribuee a la VRAIE reponse de la personne, NaN hors couverture,
                c'est l'exactitude esperee si l'on tirait dans la distribution predite ;
      p_argmax: probabilite de la modalite predite, c'est la confiance du modele ;
      couvert : masque des cellules effectivement tracees ET renseignees chez l'humain.

    Le code predit est compare au code de wave4_response.csv, qui est la position 1 fondee
    de la modalite dans l'ordre du catalogue. C'est le meme repere des deux cotes.
    """
    n, m = len(pids), len(cibles)
    pred = np.full((n, m), None, dtype=object)
    p_vraie = np.full((n, m), np.nan)
    p_argmax = np.full((n, m), np.nan)
    couvert = np.zeros((n, m), dtype=bool)
    for i, pid in enumerate(pids):
        for j, col in enumerate(cibles):
            e = trace.get((pid, col))
            if e is None or not masque[i, j]:
                continue
            code = max(e["p"], key=e["p"].get)
            pred[i, j] = float(code)
            p_argmax[i, j] = e["p"][code]
            vrai = y[i, j]
            if not est_manquant(vrai):
                p_vraie[i, j] = e["p"].get(int(float(vrai)), 0.0)
            couvert[i, j] = True
    return pred, p_vraie, p_argmax, couvert


# --------------------------------------------------------------------------------------
# 3. Metriques
# --------------------------------------------------------------------------------------

def resume_methode(nom, pred, y, masque, plafond, p_vraie=None, p_argmax=None,
                   graine=0, information=None):
    """Exactitude, IC bootstrap sur les personnes, normalisation, diversite, calibration.

    Le denominateur de la normalisation est le plafond test retest DES MEMES PERSONNES,
    passe en argument. Normaliser par une moyenne publiee sur une autre population serait
    la faute que METHODOLOGIE interdit explicitement : nommer qui est predit, par rapport
    a quoi on normalise, et quelle erreur humaine sert de plancher.
    """
    p = np.where(masque, pred, None)
    acc = exactitude_par_personne(p, y, masque)
    moy, bas, haut = bootstrap_personnes(acc, graine=graine)
    div = profil_diversite(p, np.where(masque, y, None))
    ligne = {
        "methode": nom,
        "information": information,
        "n_personnes": int(np.sum(~np.isnan(acc))),
        "n_cellules": int(masque.sum()),
        "exactitude": moy, "ic_bas": bas, "ic_haut": haut,
        "normalise": moy / plafond if plafond else float("nan"),
        "part_diversite_humaine": div["part_diversite_humaine"],
        "accord_par_paires": div["accord_par_paires"],
    }
    if p_vraie is not None:
        v = p_vraie[masque]
        c = p_argmax[masque]
        v, c = v[~np.isnan(v)], c[~np.isnan(c)]
        ligne["exactitude_esperee_tirage"] = float(np.mean(v)) if len(v) else float("nan")
        ligne["confiance_moyenne"] = float(np.mean(c)) if len(c) else float("nan")
        ligne["ecart_calibration"] = ligne["confiance_moyenne"] - moy
    return ligne


def exactitude_par_bloc(pred, y, masque, cibles, blocs):
    """Exactitude par bloc du catalogue, au niveau de la cellule.

    Pourquoi la cellule et non la personne, contrairement au chiffre global. La plupart des
    blocs de la vague 4 ne comptent qu'un seul item, et plusieurs sont inter sujets : une
    moyenne par personne y serait une moyenne de zero ou un, et son intervalle n'aurait
    aucun sens. Le chiffre par bloc est donc une part de cellules justes, et il n'est pas
    directement comparable au chiffre global par personne. Les deux sont publies separement
    et jamais melanges.

    L'enjeu est celui de la tache 4 du rapport a8 : sur Twin, tout l'avantage de
    GPT-4.1-mini sur B2 vient des 40 items de preferences de prix, et il perd sur les blocs
    d'heuristiques et de biais. Le bloc des prix se lit aussi comme un signal de
    contamination : la connaissance du prix d'un produit n'est pas une propriete de la
    personne simulee, c'est une propriete du pre entrainement du modele.
    """
    par_bloc = defaultdict(lambda: [0, 0, set()])
    for j, col in enumerate(cibles):
        b = blocs[col]
        sel = masque[:, j]
        if not sel.any():
            continue
        justes = int(((pred[:, j] == y[:, j]) & sel).sum())
        par_bloc[b][0] += justes
        par_bloc[b][1] += int(sel.sum())
        par_bloc[b][2].add(col)
    return {b: {"n_items": len(v[2]), "n_cellules": v[1],
                "exactitude": v[0] / v[1] if v[1] else float("nan")}
            for b, v in sorted(par_bloc.items())}


def calibration(p_argmax, juste, n_bins=N_BINS_CALIBRATION):
    """Diagramme de fiabilite sur la modalite predite, et erreur de calibration esperee.

    Chaque cellule apporte un couple (confiance, succes). Les cellules sont rangees en
    tranches de confiance ; dans une tranche bien calibree, la confiance moyenne egale la
    part de reponses justes. L'ECE est la moyenne des ecarts absolus, ponderee par
    l'effectif des tranches.
    """
    c = p_argmax[~np.isnan(p_argmax)]
    j = juste[~np.isnan(p_argmax)].astype(float)
    if len(c) == 0:
        return [], float("nan")
    bornes = np.linspace(0.0, 1.0, n_bins + 1)
    tranches, ece = [], 0.0
    for b in range(n_bins):
        sel = (c >= bornes[b]) & (c < bornes[b + 1] if b < n_bins - 1 else c <= 1.0)
        if sel.sum() == 0:
            continue
        conf, exact = float(c[sel].mean()), float(j[sel].mean())
        tranches.append({"borne_basse": float(bornes[b]), "borne_haute": float(bornes[b + 1]),
                         "n": int(sel.sum()), "confiance": conf, "exactitude": exact})
        ece += sel.sum() / len(c) * abs(conf - exact)
    return tranches, float(ece)


# --------------------------------------------------------------------------------------
# 4. Baselines de a2, restreintes aux personnes evaluees
# --------------------------------------------------------------------------------------

def baselines_restreintes(d, plis, index_evalues, graine=GRAINE_DECOUPAGE):
    """Recalcule B0, B1 et B2 en ne predisant que pour les personnes evaluees.

    L'entrainement reste celui de a2 : pour chaque pli, le modele voit les quatre autres
    plis en entier, soit 1 646 personnes, et ne predit que les personnes de notre
    echantillon qui appartiennent au pli de test. C'est exactement la meme quantite
    d'information d'entrainement que dans a2 ; seule la population evaluee est restreinte.

    Les variantes `tirage` de B0, B1 et B2 sont stochastiques. Leurs chiffres ne
    reproduiront donc pas au centieme ceux de a2 sur les 2 058 personnes, meme graine :
    le flux aleatoire n'est pas consomme dans le meme ordre. Les variantes `argmax` sont
    deterministes et se comparent directement.
    """
    y, x, ctx = d["y"], d["x"], d["ctx"]
    n, m = y.shape
    noms = ["B0 mode", "B0 tirage", "B1 argmax", "B1 tirage", "B2 argmax", "B2 tirage"]
    pred = {nom: np.full((n, m), None, dtype=object) for nom in noms}
    rng = np.random.default_rng(graine)
    codes = en_codes(ctx)
    a_evaluer = set(index_evalues)

    for i_pli, (tr, te) in enumerate(plis):
        te = np.array([k for k in te if k in a_evaluer])
        if len(te) == 0:
            continue
        enc = encodeur_demographies(x[tr])
        xt, xe = enc.transform(x[tr]), enc.transform(x[te])
        dist = distance_hamming(codes[te], codes[tr])
        for j in range(m):
            pred["B0 mode"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng, mode=True)[:, None]
            pred["B0 tirage"][np.ix_(te, [j])] = b0_marginale(y[tr, j], len(te), rng)[:, None]
            pred["B1 argmax"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng)[:, None]
            pred["B1 tirage"][np.ix_(te, [j])] = b1_logistique(xt, y[tr, j], xe, rng, tirage=True)[:, None]
            pred["B2 argmax"][np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], K_VOISINS, rng)[:, None]
            pred["B2 tirage"][np.ix_(te, [j])] = b2_voisins(dist, y[tr, j], K_VOISINS, rng, tirage=True)[:, None]
        print(f"  pli {i_pli + 1}/{len(plis)} : {len(te)} personnes evaluees", flush=True)
    return pred


# --------------------------------------------------------------------------------------
# 5. Simulations publiees par les auteurs, restreintes aux memes personnes
# --------------------------------------------------------------------------------------

def predictions_llm(d, pids_evalues):
    """Exactitude de GPT-4.1-mini, configurations default et demo_only, memes personnes.

    Difference assumee avec a2, et elle va dans le sens de la comparabilite. a2 evaluait
    les simulations des auteurs sur toutes les cellules renseignees du fichier formate,
    donc sur un masque a elles. Ici les simulations sont ramenees dans l'espace des 108
    colonnes du catalogue et evaluees sur EXACTEMENT le meme masque que nos conditions et
    que les baselines : memes personnes, memes cellules. Sans cela, un run local interrompu
    serait compare a un GPT-4.1-mini evalue sur davantage de cellules.

    Le passage d'un codage a l'autre est verifie et non suppose : la fonction renvoie la
    part de cellules ou l'humain formate et le catalogue disent la meme chose sur NOS
    personnes. a2 l'a mesuree a 1,0000 sur les 2 058, et un ecart signalerait un
    desalignement de colonnes.

    Retourne un dictionnaire libelle -> matrice de codes predits, alignee sur
    (personnes evaluees, 108 colonnes cibles), et le controle d'alignement.
    """
    chemin_mapping = os.path.join(LLM, "wave4_formatted_to_catalog_mapping.json")
    if not os.path.exists(chemin_mapping):
        return {}, None
    mapping = json.load(open(chemin_mapping, encoding="utf-8"))
    cibles = list(d["cibles"])
    rang_cible = {c: j for j, c in enumerate(cibles)}
    paires = [(m["formatted_column"], m["catalog_csv_column"]) for m in mapping
              if m["catalog_csv_column"] in rang_cible]
    colonnes = [f for f, _ in paires]
    colonnes_catalogue = [c for _, c in paires]

    humain = pd.read_csv(os.path.join(LLM, "default_gpt41mini_wave4.csv"), low_memory=False)
    humain = humain.iloc[1:].reset_index(drop=True)      # la premiere ligne est un libelle
    humain["tid"] = pd.to_numeric(humain["TWIN_ID"])
    humain = humain.set_index("tid")
    manquants = [p for p in pids_evalues if p not in humain.index]
    if manquants:
        print(f"  ATTENTION : {len(manquants)} personne(s) absente(s) des fichiers de "
              f"simulation des auteurs, elles seront comptees comme non predites", flush=True)
    presents = [p for p in pids_evalues if p in humain.index]
    hum = humain.loc[presents]
    b = hum[colonnes].apply(pd.to_numeric, errors="coerce").values

    # Controle d'alignement avec le catalogue, sur les memes personnes et colonnes.
    rang_pid = {int(p): i for i, p in enumerate(d["pid"])}
    idx = [rang_pid[p] for p in presents]
    cat = np.array([[d["y"][i, rang_cible[c]] for c in colonnes_catalogue] for i in idx],
                   dtype=object)
    comparables = (~np.isnan(b)) & np.array([[not est_manquant(v) for v in l] for l in cat])
    accord = float(((b == cat.astype(float)) & comparables).sum() / max(comparables.sum(), 1))

    rang_present = {p: i for i, p in enumerate(presents)}
    sorties = {}
    for libelle, fichier in SIMULATIONS.items():
        chemin = os.path.join(LLM, fichier)
        if not os.path.exists(chemin):
            continue
        sim = pd.read_csv(chemin, low_memory=False).iloc[1:].reset_index(drop=True)
        sim["tid"] = pd.to_numeric(sim["TWIN_ID"])
        sim = sim.set_index("tid").loc[presents]
        a = sim[colonnes].apply(pd.to_numeric, errors="coerce").values
        pred = np.full((len(pids_evalues), len(cibles)), None, dtype=object)
        for i, p in enumerate(pids_evalues):
            if p not in rang_present:
                continue
            k = rang_present[p]
            for c, col in enumerate(colonnes_catalogue):
                v = a[k, c]
                if not np.isnan(v):
                    pred[i, rang_cible[col]] = float(v)
        sorties[libelle] = pred
    return sorties, accord


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--suffixe", default="", help="suffixe des traces, ex. smoke")
    ap.add_argument("--conditions", default="C3b-Twin,C2-Twin",
                    help="conditions a evaluer. Toutes les methodes sont restreintes a "
                         "l'intersection des personnes couvertes par les conditions "
                         "demandees. Si le run de la nuit a ete coupe et que C2-Twin "
                         "couvre plus de personnes que C3-Twin, passer une seule "
                         "condition donne son chiffre sur toute sa population, au prix "
                         "de la comparabilite entre les deux. Par defaut C3b-Twin et "
                         "C2-Twin, qui sont les deux conditions que la nuit couvre "
                         "largement. Ajouter C3-Twin ramene TOUTES les methodes a la "
                         "population de C3-Twin, qui sera la plus petite : c'est la "
                         "comparaison juste, sur moins de personnes.")
    ap.add_argument("--sans-baselines", action="store_true",
                    help="saute B0, B1, B2 et les references des auteurs. Utile pour "
                         "verifier une trace de smoke test en quelques secondes.")
    ap.add_argument("--couverture-min", type=float, default=0.0,
                    help="part minimale de cellules tracees pour qu'une personne entre "
                         "dans l'evaluation. 0 accepte toute personne partiellement "
                         "couverte, ce qui est le bon reglage pour un run interrompu, a "
                         "condition de lire la colonne n_cellules.")
    args = ap.parse_args()
    os.makedirs(SORTIE, exist_ok=True)

    # -------------------------------------------------------------- donnees et echantillon
    d = charger_twin()
    cibles, y_tot = d["cibles"], d["y"]
    rang_pid = {int(p): i for i, p in enumerate(d["pid"])}

    chemin_personnes = os.path.join(
        TRACES, f"a11-personnes{'-' + args.suffixe if args.suffixe else ''}.csv")
    if not os.path.exists(chemin_personnes):
        sys.exit(f"echantillon introuvable : {chemin_personnes}")
    ech = pd.read_csv(chemin_personnes)
    pids_ech = [int(p) for p in ech["pid"]]

    # -------------------------------------------------------------- traces
    demandees = [c.strip() for c in args.conditions.split(",") if c.strip()]
    inconnues = [c for c in demandees if c not in CONDITIONS]
    if inconnues:
        sys.exit(f"condition inconnue : {inconnues}")
    traces, fichiers, illisibles = {}, {}, 0
    for c in demandees:
        t, f, n = lire_traces(c, args.suffixe)
        traces[c], fichiers[c] = t, f
        illisibles += n
        pids_vus = {k[0] for k in t}
        print(f"{c} : {len(f)} fichier(s), {len(t)} appels uniques, "
              f"{len(pids_vus)} personnes", flush=True)
    if illisibles:
        print(f"{illisibles} ligne(s) de trace illisibles, ignorees", flush=True)

    # Population evaluee : les personnes de l'echantillon couvertes par TOUTES les
    # conditions tracees. Comparer nos deux conditions sur deux populations differentes
    # ferait passer un effet de composition pour un effet de condition.
    conditions_presentes = [c for c in demandees if traces[c]]
    if not conditions_presentes:
        sys.exit("aucune trace lisible")
    pids_par_condition = [{k[0] for k in traces[c]} for c in conditions_presentes]
    pids = sorted(set(pids_ech).intersection(*pids_par_condition))
    if not pids:
        sys.exit("aucune personne commune a toutes les conditions tracees")
    idx = [rang_pid[p] for p in pids]
    y = y_tot[idx]
    y_retest = d["y_retest"][idx]
    masque_humain = np.array([[not est_manquant(v) for v in l] for l in y])

    # Cellules retenues : renseignees chez l'humain ET tracees dans toutes les conditions.
    couverts = []
    for c in conditions_presentes:
        _, _, _, cv = matrices_condition(traces[c], pids, cibles, y, masque_humain)
        couverts.append(cv)
    masque = masque_humain & np.logical_and.reduce(couverts)
    part = masque.sum(axis=1) / np.maximum(masque_humain.sum(axis=1), 1)
    garde = part >= args.couverture_min
    if not garde.all():
        pids = [p for p, g in zip(pids, garde) if g]
        idx = [rang_pid[p] for p in pids]
        y, y_retest = y_tot[idx], d["y_retest"][idx]
        masque_humain = np.array([[not est_manquant(v) for v in l] for l in y])
        couverts = [matrices_condition(traces[c], pids, cibles, y, masque_humain)[3]
                    for c in conditions_presentes]
        masque = masque_humain & np.logical_and.reduce(couverts)

    print(f"\npopulation evaluee : {len(pids)} personnes, {int(masque.sum())} cellules "
          f"communes a toutes les conditions, soit "
          f"{masque.sum() / max(masque_humain.sum(), 1) * 100:.1f} pour cent des cellules "
          f"renseignees de ces personnes", flush=True)
    print(f"repartition par pli : "
          f"{dict(Counter(int(r.pli) for r in ech.itertuples() if int(r.pid) in set(pids)))}",
          flush=True)

    # -------------------------------------------------------------- plafond humain
    retest = exactitude_par_personne(np.where(masque, y_retest, None), y, masque)
    plafond, pl_bas, pl_haut = bootstrap_personnes(retest, graine=0)
    div_retest = profil_diversite(np.where(masque, y_retest, None), np.where(masque, y, None))
    print(f"plafond test retest de CES personnes : {plafond:.4f} "
          f"[{pl_bas:.4f} ; {pl_haut:.4f}]\n", flush=True)

    predictions = {"retest humain (plafond)": np.where(masque, y_retest, None)}
    lignes = [{
        "methode": "retest humain (plafond)",
        "information": "la meme personne, deux semaines plus tot",
        "n_personnes": int(np.sum(~np.isnan(retest))), "n_cellules": int(masque.sum()),
        "exactitude": plafond, "ic_bas": pl_bas, "ic_haut": pl_haut, "normalise": 1.0,
        "part_diversite_humaine": div_retest["part_diversite_humaine"],
        "accord_par_paires": div_retest["accord_par_paires"],
    }]

    # -------------------------------------------------------------- nos conditions
    calibrations, qualite = {}, {}
    for c in conditions_presentes:
        pred, p_vraie, p_argmax, _ = matrices_condition(traces[c], pids, cibles, y,
                                                        masque_humain)
        info = {"C3-Twin": "persona texte complet vagues 1 a 3, 27 500 tokens",
                "C3b-Twin": "persona tronque a 8 000 tokens, 42 questions sur 173",
                "C2-Twin": "14 questions demographiques"}[c]
        nom = f"{c} (Qwen3-4B local)"
        predictions[nom] = pred
        ligne = resume_methode(nom, pred, y, masque, plafond,
                               p_vraie=p_vraie, p_argmax=p_argmax, information=info)
        juste = np.where(masque, pred == y, np.nan).astype(float)
        tranches, ece = calibration(np.where(masque, p_argmax, np.nan), juste)
        ligne["ece"] = ece
        calibrations[c] = tranches
        passes = sorted({e["passes"] for e in traces[c].values()})
        rejets = sum(1 for e in traces[c].values() if e["rejet"])
        masses = np.array([e["masse"] for e in traces[c].values()])
        qualite[c] = {"passes_par_appel": passes, "appels_rejetes": rejets,
                      "masse_min": float(masses.min()), "masse_mediane": float(np.median(masses)),
                      "masse_moyenne": float(masses.mean())}
        print(f"{c} : masse des lettres mediane {np.median(masses):.4f}, "
              f"minimum {masses.min():.4f}, {rejets} appel(s) sous le seuil 0,5", flush=True)
        lignes.append(ligne)

    # -------------------------------------------------------------- baselines et references
    accord_formate = None
    if not args.sans_baselines:
        print("\nbaselines sans modele de langage, entrainement complet, evaluation "
              "restreinte", flush=True)
        plis = plis_personnes(len(d["pid"]), GRAINE_DECOUPAGE)
        pred_b = baselines_restreintes(d, plis, idx)
        for nom, p in pred_b.items():
            info = ("marginale de l'item" if nom.startswith("B0")
                    else "14 questions demographiques" if nom.startswith("B1")
                    else "494 items de contexte vagues 1 a 3")
            predictions[nom] = p[idx]
            lignes.append(resume_methode(nom, p[idx], y, masque, plafond, information=info))

        print("\nsimulations publiees par les auteurs, memes personnes et memes cellules",
              flush=True)
        refs, accord_formate = predictions_llm(d, pids)
        if accord_formate is not None:
            print(f"  controle d'alignement humain formate contre catalogue : "
                  f"{accord_formate:.4f}", flush=True)
        for libelle, p in refs.items():
            info = ("persona texte complet vagues 1 a 3" if "complet" in libelle
                    else "14 questions demographiques")
            predictions[libelle] = p
            lignes.append(resume_methode(libelle, p, y, masque, plafond, information=info))

    # -------------------------------------------------------------- exactitude par bloc
    blocs_par_col = {c: d["catalogue"][c]["BlockName"].strip() for c in cibles}
    par_bloc = {nom: exactitude_par_bloc(np.where(masque, p, None), y, masque, cibles,
                                         blocs_par_col)
                for nom, p in predictions.items()}
    # Les blocs a une seule question sont trop bruites pour etre lus un par un : le tableau
    # affiche les blocs d'au moins trois items, le JSON garde tout.
    gros = [b for b in sorted({b for v in par_bloc.values() for b in v})
            if max((v.get(b, {}).get("n_items", 0) for v in par_bloc.values()), default=0) >= 3]
    ordre_affichage = [b for b in ["Product Preferences - Pricing",
                                   "Non-experimental heuristics and biases",
                                   "False consensus",
                                   "Probability matching vs. maximizing - Problem 1",
                                   "Probability matching vs. maximizing - Problem 2"]
                       if b in gros] + [b for b in gros if b not in (
                           "Product Preferences - Pricing",
                           "Non-experimental heuristics and biases",
                           "False consensus",
                           "Probability matching vs. maximizing - Problem 1",
                           "Probability matching vs. maximizing - Problem 2")]

    # -------------------------------------------------------------- sortie
    lignes.sort(key=lambda l: -l["exactitude"])
    print(f"\n{'methode':<30}{'exactitude':>12}{'IC 95%':>22}{'normalise':>11}"
          f"{'diversite':>11}{'paires':>9}{'n':>6}")
    for l in lignes:
        print(f"{l['methode']:<30}{l['exactitude']:>12.4f}"
              f"{'[' + format(l['ic_bas'], '.4f') + ' ; ' + format(l['ic_haut'], '.4f') + ']':>22}"
              f"{l['normalise'] * 100:>10.1f}%{l['part_diversite_humaine'] * 100:>10.1f}%"
              f"{l['accord_par_paires'] * 100:>8.1f}%{l['n_personnes']:>6}")

    if ordre_affichage:
        print("\nexactitude par bloc du catalogue, au niveau de la CELLULE, donc non "
              "comparable\nau chiffre global qui est une moyenne par personne. Le bloc des "
              "prix est le bloc\nde contamination possible : la connaissance du prix d'un "
              "produit n'appartient pas\na la personne simulee.")
        codes = {b: f"b{i + 1}" for i, b in enumerate(ordre_affichage)}
        print("")
        for b in ordre_affichage:
            n = max((v.get(b, {}).get("n_items", 0) for v in par_bloc.values()), default=0)
            print(f"  {codes[b]:<4}{n:>3} items   {b}")
        entete = "".join(f"{codes[b]:>9}" for b in ordre_affichage)
        print(f"\n{'methode':<30}{entete}")
        for l in lignes:
            v = par_bloc.get(l["methode"], {})
            cells = "".join(
                (f"{v[b]['exactitude'] * 100:>8.1f}%" if b in v else f"{'-':>9}")
                for b in ordre_affichage)
            print(f"{l['methode']:<30}{cells}")

    print(f"\n{'condition':<30}{'exact. esperee':>15}{'confiance':>11}{'ecart':>9}{'ECE':>8}")
    for l in lignes:
        if "exactitude_esperee_tirage" in l:
            print(f"{l['methode']:<30}{l['exactitude_esperee_tirage']:>15.4f}"
                  f"{l['confiance_moyenne']:>11.4f}{l['ecart_calibration']:>+9.4f}"
                  f"{l.get('ece', float('nan')):>8.4f}")

    resultat = {
        "jeu": "Twin-2K-500, LLM-Digital-Twin/Twin-2K-500, CC BY 4.0",
        "suffixe": args.suffixe,
        "conditions_evaluees": conditions_presentes,
        "fichiers_traces": fichiers,
        "personnes_evaluees": pids,
        "n_personnes": len(pids), "n_items": len(cibles),
        "n_cellules_evaluees": int(masque.sum()),
        "plafond_test_retest": {"exactitude": plafond, "ic_bas": pl_bas, "ic_haut": pl_haut},
        "qualite_des_appels": qualite,
        "calibration": calibrations,
        "controle_alignement_formate_catalogue": accord_formate,
        "resultats": lignes,
        "exactitude_par_bloc": par_bloc,
    }
    chemin = os.path.join(SORTIE,
                          f"a11_twin_resultats{'-' + args.suffixe if args.suffixe else ''}.json")
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(resultat, fh, indent=2, ensure_ascii=False, default=float)
    print(f"\necrit : {chemin}")


if __name__ == "__main__":
    main()
