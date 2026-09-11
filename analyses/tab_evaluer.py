"""
tab_evaluer : l'evaluation du tournoi A vers B sur Twin-2K-500, ecrite AVANT tout calcul
de resultat et figee avec le preenregistrement resultats/tab-preenregistrement.md.

===========================================================================
SOURCE DE VERITE : resultats/tab-preenregistrement.md. Chaque constante renvoie a sa
section, notee « §N ». En cas de divergence, c'est la page qui fait foi.

GARDE. Le chargeur reel `charger_reel` refuse de lire la moindre donnee Twin :
  - si le fichier data/traces/GO-TAB est absent (feu vert donne apres depot OSF) ;
  - si le SHA-256 de resultats/tab-partition-items.csv differe de celui du §4.2 (H) ;
  et `executer` refuse, sans chargeur injecte, tout parametre different du prereg.
Les tests injectent un chargeur synthetique (`executer(chargeur=...)`) : ils n'ouvrent
aucune reponse de Twin.

ORDRE, celui du prereg :
  §8   controles C1 a C4, T et R, AVANT tout calcul de perte ; un echec au principal
       donne « non concluant » (H est verifie par la garde) ;
  §5   exa_A (Q1, a44_mesures.exactitude_codes sans modification), chute_A (Q2, S_gra,
       a44_commun.permuter_intra sans modification, P = 200), residu (Q3, polyfit de
       degre 1 sur les seules candidates), c_diag = argmax residu, c_exa = argmax exa_A,
       perte_B (Q4) ;
  §1   Delta_r, Delta ;
  §7   bootstrap conjoint personnes x unites, B = 1 000, P = 20, qui refait toute la
       selection ; les multiplicites deviennent des lignes et des colonnes repetees, ce
       qui laisse exactitude_codes inchangee ; permutation sur les identites distinctes ;
  §9   regle de chute R1 a R4, R3 par retrait de chacune des 14 familles ;
  §10  S1 a S8.

CONVENTIONS QUE LE PREREG NE FIXE PAS A LA LETTRE (declarees ; a trancher avant depot) :
  I1. Permutations partagees : pour une analyse ponctuelle, un generateur neuf
      default_rng(GRAINE_PERMUTATIONS) tire P permutations des personnes, appliquees a
      TOUTES les configurations et aux trois rotations. Au bootstrap, les P = 20
      permutations « par replicat » sont de meme partagees.
  I2. R porte sur les 7 candidates et les 5 adversaires, sans masque de tournoi, sur les
      2 058 personnes, comme t1.
  I3. S2 a S5 : estimation ponctuelle seule. S1 recoit son bootstrap et R3 (R1 a R4).
  I4. La regle de cout (§7) est evaluee separement pour chaque bootstrap (principal, S1),
      sur la duree reelle mesuree du processus.
  I5. Dans une analyse R3, une personne sans cellule dans un A_r ou un B_r rend la
      revendication « non concluante ».
  I6. La decision est ecrite dans tab-rotations.csv (lignes `decision`) ; le §13 ne lui
      donne pas de fichier propre.
  I7. S4 et S5 refont le choix avec la variante ; S7 et S8 sont mesurees sur le masque
      des 7 candidates.

Usage (reel, seulement apres depot OSF et creation de GO-TAB par le responsable) :
  .venv/bin/python analyses/tab_evaluer.py
Aucun appel reseau, aucun modele. Rien n'est ecrit sous data/.
===========================================================================
"""

import argparse
import csv
import dataclasses
import os
import sys
import time

_ICI = os.path.dirname(os.path.abspath(__file__))
_ANALYSES = os.environ.get("POPSIM_ANALYSES", _ICI)
for _p in (_ANALYSES, _ICI):                                  # _ICI finit en tete
    while _p in sys.path:
        sys.path.remove(_p)
    sys.path.insert(0, _p)

import numpy as np                    # noqa: E402

import t1_commun as C                 # noqa: E402  exactitude_codes, REF, PLANCHER
import a44_commun as C44              # noqa: E402  permuter_intra
import tab_partition as TP            # noqa: E402  sha256_fichier, lire_csv, verifier

RACINE = C.RACINE
GO_TAB = os.path.join(RACINE, "data", "traces", "GO-TAB")
PARTITION = os.path.join(RACINE, "resultats", "tab-partition-items.csv")
T1_CHUTE = os.path.join(RACINE, "resultats", "t1-chute-segmentations.csv")
SORTIE = os.path.join(RACINE, "resultats")

# ---------------------------------------------------------------------------
# Constantes du preenregistrement
# ---------------------------------------------------------------------------

SHA_PARTITION = "07b3de89cdce44c9644b54fa88f09c429f9874cc2342d7c23f36a1500b183b05"  # §4.2, H

GRAINE_PARTITION = 20260911                    # §4.1 point 7 et §5 « Graines »
GRAINE_PERMUTATIONS = GRAINE_PARTITION + 10    # §5 : permutations de l'estimation ponctuelle
GRAINE_BOOTSTRAP = GRAINE_PARTITION + 20       # §5 : bootstrap
GRAINE_ADVERSAIRES = 20260909                  # §5 et §6 : graine de t1 (t1_commun.GRAINE)
assert GRAINE_ADVERSAIRES == C.GRAINE

P_PERMUTATIONS = 200                 # §5 Q2
P_PERMUTATIONS_BOOTSTRAP = 20        # §7, par replicat
B_BOOTSTRAP = 1000                   # §7
B_BOOTSTRAP_REDUIT = 500             # §7, regle de cout
N_REPLICATS_PROJECTION = 20          # §7, projection apres 20 replicats
DUREE_MAX_PROJETEE_S = 6 * 3600      # §7, 6 heures sur 4 coeurs
PERCENTILES_IC = (2.5, 97.5)         # §7

N_ROTATIONS = 3                      # §1
SEUIL_R1 = -0.01                     # §9 R1 : Delta <= -0,01
SEUIL_C1_COUVERTURE_ITEM = 0.25      # §8 C1
SEUIL_C2_CELLULES_GARDEES = 0.99     # §8 C2
C3_CELLULES_MIN = 1                  # §8 C3
C3_CELLULES_PEU = 10                 # §8 C3
C3_PART_MAX_PEU = 0.01               # §8 C3
C4_UNITES_MIN = 10                   # §8 C4
SEUIL_T_TEMOIN = 0.005               # §8 T
SEUIL_R_REPRODUCTION = 1e-12         # §8 R
SEGMENTATION = "S_gra"               # §5 Q2 et §10

PID_MAX_PRINCIPAL = 2058             # §2 et §3 : pid 1 a 2 058
PID_MAX_S1 = 1000                    # §2 et §10 S1 : pid 1 a 1 000

REF = C.REF                          # §3 : « humains vague 4 »
PLANCHER = C.PLANCHER                # §6 S6 : « humains vagues 1-3 (retest) »

# §2, ordre de llm_specs/index.json ; le departage suit cet ordre.
ORDRE_INDEX = [
    "Demographics Only - GPT4.1-mini",
    "JSON Persona (Predicted Output) - GPT4.1",
    "JSON Persona (Predicted Output) - GPT4.1-mini",
    "JSON Persona - GPT4.1",
    "JSON Persona - GPT4.1-mini",
    "LLM Finetuning (500 training samples) - GPT4.1-mini",
    "Persona Summary - GPT4.1-mini",
    "Persona Summary - JSON Persona - GPT4.1-mini",
    "Text Persona (Default Temperature) - GPT4.1-mini",
    "Text Persona (Reasoning) - GPT4.1-mini",
    "Text Persona (Repeating Questions) - GPT4.1-mini",
    "Text Persona - GPT4.1-mini",
    "Text Persona - Gemini-Flash2.5",
]
CANDIDATES_PRINCIPAL = [                                   # §2, 7 configurations
    "Demographics Only - GPT4.1-mini",
    "JSON Persona - GPT4.1",
    "Text Persona (Default Temperature) - GPT4.1-mini",
    "Text Persona (Reasoning) - GPT4.1-mini",
    "Text Persona (Repeating Questions) - GPT4.1-mini",
    "Text Persona - GPT4.1-mini",
    "Text Persona - Gemini-Flash2.5",
]
JSON_MINI = "JSON Persona - GPT4.1-mini"
CANDIDATES_S1 = [c for c in ORDRE_INDEX if c in CANDIDATES_PRINCIPAL + [JSON_MINI]]  # §2, 8
CANDIDATES_S2 = [c for c in CANDIDATES_PRINCIPAL                                      # §10 S2
                 if c != "Demographics Only - GPT4.1-mini"]
DESCRIPTION_SEULE = ["Persona Summary - GPT4.1-mini",                                 # §2, S7
                     "Persona Summary - JSON Persona - GPT4.1-mini"]

ADVERSAIRES = ["B0 mode", "B0 tirage", "B1 argmax", "B2 argmax", "PMM k=10"]           # §6
TEMOINS = ["B0 mode", "B0 tirage"]                                                   # §8 T
PMM = "PMM k=10"                                                                     # §9 R4
ADVERSAIRES_S8 = ["B1 argmax", "B2 argmax", "PMM k=10"]                               # §10 S8
BORNES_S8 = ["B0 mode", "B0 tirage", "B1 argmax"]                                    # §10 S8

N_FAMILLES_ATTENDU = 14              # §4.1 point 4 et §9 R3

assert CANDIDATES_PRINCIPAL == [c for c in ORDRE_INDEX if c in set(CANDIDATES_PRINCIPAL)]
assert len(CANDIDATES_PRINCIPAL) == 7 and len(CANDIDATES_S1) == 8 and len(CANDIDATES_S2) == 6


@dataclasses.dataclass(frozen=True)
class Parametres:
    """Parametres d'execution. Les valeurs par defaut sont celles du prereg ; sans chargeur
    injecte, `executer` refuse toute autre valeur. Les tests les reduisent."""
    n_permutations: int = P_PERMUTATIONS
    n_permutations_bootstrap: int = P_PERMUTATIONS_BOOTSTRAP
    n_bootstrap: int = B_BOOTSTRAP
    n_bootstrap_reduit: int = B_BOOTSTRAP_REDUIT
    n_replicats_projection: int = N_REPLICATS_PROJECTION
    duree_max_projetee_s: float = DUREE_MAX_PROJETEE_S
    graine_permutations: int = GRAINE_PERMUTATIONS
    graine_bootstrap: int = GRAINE_BOOTSTRAP
    pid_max_principal: int = PID_MAX_PRINCIPAL
    pid_max_s1: int = PID_MAX_S1


class ErreurGarde(Exception):
    """Refus de lire les donnees reelles : GO-TAB absent, SHA faux, parametres alleges."""


class ErreurFuite(Exception):
    """Un item ou une unite passe de B a A, ou la partition ne couvre pas les items."""


class ErreurDonnees(Exception):
    """Donnees injectees incoherentes."""


# ---------------------------------------------------------------------------
# 1. Garde et chargement
# ---------------------------------------------------------------------------

def verifier_garde(chemin_go=None, chemin_partition=None):
    """Feu vert puis controle H. Leve ErreurGarde AVANT toute lecture de donnees Twin."""
    chemin_go = GO_TAB if chemin_go is None else chemin_go
    chemin_partition = PARTITION if chemin_partition is None else chemin_partition
    if not os.path.isfile(chemin_go):
        raise ErreurGarde(f"feu vert absent : {chemin_go}. Le preenregistrement doit etre "
                          "depose sur OSF avant la premiere execution.")
    if not os.path.isfile(chemin_partition):
        raise ErreurGarde(f"partition absente : {chemin_partition}")
    sha = TP.sha256_fichier(chemin_partition)
    if sha != SHA_PARTITION:
        raise ErreurGarde(f"SHA de la partition {sha} different du preenregistrement "
                          f"{SHA_PARTITION}")
    return sha


def _lire_reference_t1(chemin, n_attendu):
    """exactitude_vraie de t1 sous S_gra, sur le perimetre complet. Controle R."""
    out = {}
    with open(chemin, encoding="utf-8", newline="") as f:
        for l in csv.DictReader(f):
            if l["segmentation"] == SEGMENTATION and int(l["n"]) == n_attendu:
                out[l["condition"]] = float(l["exactitude_vraie"])
    return out


def _charger_twin_brut():
    """Seul point d'entree vers les reponses de Twin. Appele UNIQUEMENT apres la garde."""
    import t1_baselines as TB
    paq = C.charger()
    adv = TB.calculer(paq)
    # S6 (§6) : meme code, memes plis, cible remplacee par le retest des vagues 1 a 3,
    # dans une copie de paq ; t1_baselines.py n'est pas touche.
    paq6 = dict(paq)
    paq6["codes"] = dict(paq["codes"])
    paq6["codes"][REF] = paq["codes"][PLANCHER]
    adv6 = TB.calculer(paq6)
    return paq, adv, adv6


def charger_reel(chemin_go=None, chemin_partition=None, chemin_t1=None):
    """Chargeur des donnees reelles, precede de la garde (feu vert, puis H)."""
    chemin_partition = PARTITION if chemin_partition is None else chemin_partition
    verifier_garde(chemin_go, chemin_partition)
    partition = TP.lire_csv(chemin_partition)
    TP.verifier(partition)
    paq, adv, adv6 = _charger_twin_brut()
    pids = np.asarray(paq["ids"], dtype=np.int64)
    if len(pids) != PID_MAX_PRINCIPAL or not np.array_equal(
            pids, np.arange(1, PID_MAX_PRINCIPAL + 1)):
        raise ErreurDonnees("les pid de Twin ne sont pas exactement 1 a 2 058")
    configs = {c: paq["codes"][c] for c in ORDRE_INDEX if c in paq["codes"]}
    return {
        "pids": pids, "items": list(paq["colonnes"]), "verite": paq["codes"][REF],
        "configs": configs, "adversaires": adv, "adversaires_s6": adv6,
        "seg": np.asarray(paq["seg"][SEGMENTATION]), "val_ord": paq["val_ord"],
        "est_ordinal": np.asarray(paq["est_ordinal"], dtype=bool),
        "partition": partition,
        "reference_t1": _lire_reference_t1(chemin_t1 or T1_CHUTE, PID_MAX_PRINCIPAL),
    }


# ---------------------------------------------------------------------------
# 2. Structure : partition, rotations, fuite
# ---------------------------------------------------------------------------

CLES_DONNEES = ["pids", "items", "verite", "configs", "adversaires", "seg", "val_ord",
                "est_ordinal", "partition"]


def valider_donnees(d):
    manquants = [k for k in CLES_DONNEES if k not in d]
    if manquants:
        raise ErreurDonnees(f"cles absentes : {manquants}")
    n, m = d["verite"].shape
    if len(d["items"]) != m or len(d["pids"]) != n or len(d["seg"]) != n:
        raise ErreurDonnees("dimensions incoherentes entre verite, items, pids et seg")
    if d["val_ord"].shape[0] != m or len(d["est_ordinal"]) != m:
        raise ErreurDonnees("val_ord ou est_ordinal mal dimensionnes")
    k_max = d["val_ord"].shape[1]
    tables = [("verite", d["verite"])] + \
        [(f"config {k}", v) for k, v in d["configs"].items()] + \
        [(f"adversaire {k}", v) for k, v in d["adversaires"].items()] + \
        [(f"adversaire S6 {k}", v) for k, v in (d.get("adversaires_s6") or {}).items()]
    for nom, t in tables:
        if t.shape != (n, m):
            raise ErreurDonnees(f"{nom} : forme {t.shape}, {(n, m)} attendue")
        if t.min() < -1 or t.max() >= k_max:
            raise ErreurDonnees(f"{nom} : codes hors nomenclature")
    for c in CANDIDATES_S1 + DESCRIPTION_SEULE:
        if c not in d["configs"]:
            raise ErreurDonnees(f"configuration absente : {c}")
    for a in ADVERSAIRES:
        if a not in d["adversaires"]:
            raise ErreurDonnees(f"adversaire absent : {a}")


def structure_partition(partition, items, est_ordinal=None):
    """Bloc, unite et famille de chaque colonne des donnees. Leve ErreurFuite si un item
    figure deux fois (il serait a la fois dans B et dans A), si une unite indivisible est
    coupee entre blocs, ou si la partition et les donnees n'ont pas les memes items."""
    par_item = {}
    for l in partition:
        it = l["item"]
        if it in par_item:
            raise ErreurFuite(f"item {it!r} present deux fois dans la partition, blocs "
                              f"{par_item[it]['bloc_B']} et {l['bloc_B']} : fuite de B "
                              "vers A")
        par_item[it] = l
    if set(par_item) != set(items) or len(items) != len(set(items)):
        raise ErreurFuite("la partition et les donnees ne portent pas les memes items")
    bloc = np.array([int(par_item[it]["bloc_B"]) for it in items], dtype=int)
    if set(bloc.tolist()) != set(range(1, N_ROTATIONS + 1)):
        raise ErreurFuite(f"blocs {sorted(set(bloc.tolist()))}, 1 a {N_ROTATIONS} attendus")
    unite = np.array([par_item[it]["unite"] for it in items])
    bloc_de = {}
    for u, b in zip(unite, bloc):
        if bloc_de.setdefault(u, b) != b:
            raise ErreurFuite(f"unite {u} coupee entre les blocs {bloc_de[u]} et {b} : "
                              "fuite de contenu de B vers A")
    famille = np.array([par_item[it]["famille_analyse"] for it in items])
    if est_ordinal is not None:
        mx = np.array([par_item[it]["type"] == "ligne_matrice" for it in items])
        if not np.array_equal(mx, np.asarray(est_ordinal, dtype=bool)):
            raise ErreurDonnees("type de la partition different de est_ordinal")
    unites_bloc = {b: sorted(set(unite[bloc == b].tolist()))
                   for b in range(1, N_ROTATIONS + 1)}
    return {"bloc": bloc, "unite": unite, "famille": famille, "unites_bloc": unites_bloc,
            "familles": sorted(set(famille.tolist()))}


def verifier_rotation(poids_A, poids_B):
    """Aucun item de B_r ne peut porter de poids dans A_r."""
    fuite = (np.asarray(poids_A) > 0) & (np.asarray(poids_B) > 0)
    if fuite.any():
        raise ErreurFuite(f"{int(fuite.sum())} item(s) de B_r presents dans A_r")


def colonnes_rotations(struct, poids_items):
    """Pour chaque rotation r, les indices de colonnes de A_r et de B_r, REPETES selon le
    poids entier de chaque item (multiplicite bootstrap de son unite, 0 si retire)."""
    poids_items = np.asarray(poids_items, dtype=np.int64)
    j = np.arange(len(poids_items))
    out = []
    for r in range(1, N_ROTATIONS + 1):
        pB = np.where(struct["bloc"] == r, poids_items, 0)
        pA = np.where(struct["bloc"] != r, poids_items, 0)
        verifier_rotation(pA, pB)
        out.append((np.repeat(j, pA), np.repeat(j, pB)))
    return out


# ---------------------------------------------------------------------------
# 3. Tournoi : masque, perte, mesures, selection
# ---------------------------------------------------------------------------

def lignes_perimetre(d, pid_max):
    """§2 : les personnes de pid 1 a pid_max."""
    return np.flatnonzero((d["pids"] >= 1) & (d["pids"] <= pid_max))


def matrice_perte(P, Vm, M, est_ordinal, val_ord):
    """§5 Q4 : |v(pred) - v(vrai)| pour une ligne de matrice, 1[pred != vrai] pour un MC,
    1 pour une prediction absente ; 0 hors du masque (la cellule n'est pas comptee)."""
    jj = np.arange(P.shape[1])[None, :]
    d_ord = np.abs(val_ord[jj, np.where(P >= 0, P, 0)] -
                   val_ord[jj, np.where(Vm >= 0, Vm, 0)])
    d01 = (P != Vm).astype(np.float64)
    L = np.where(np.asarray(est_ordinal, dtype=bool)[None, :], d_ord, d01)
    L = np.where(P < 0, 1.0, L)
    return np.where(M, L, 0.0)


def preparer_tournoi(d, lignes, candidates, decrits):
    """§3 : masque = humain de vague 4 repond ET toutes les candidates repondent. Toutes
    les quantites, adversaires et descriptions comprises, sont calculees sur ce masque."""
    V = d["verite"][lignes]
    M = V >= 0
    for c in candidates:
        M = M & (d["configs"][c][lignes] >= 0)
    Vm = np.where(M, V, -1).astype(V.dtype)
    preds = {nom: mat[lignes] for nom, mat in decrits.items()}
    for c in candidates:
        preds[c] = d["configs"][c][lignes]
    pertes = {nom: matrice_perte(P, Vm, M, d["est_ordinal"], d["val_ord"])
              for nom, P in preds.items()}
    return {"lignes": lignes, "V_obs": V >= 0, "M": M, "Vm": Vm, "preds": preds,
            "pertes": pertes, "seg": np.asarray(d["seg"])[lignes],
            "candidates": list(candidates), "n": len(lignes)}


def permutations_identites(lignes_rep, seg, n_perm, rng):
    """§7 « Doublons et permutation » : la permutation porte sur les identites DISTINCTES
    tirees dans chaque cellule S_gra (a44_commun.permuter_intra, sans modification) ; chaque
    copie d'une identite recoit les reponses de la meme identite permutee et garde le poids
    de sa multiplicite. Pour lignes_rep = 0..n-1, c'est exactement la permutation de t1.
    Renvoie, pour chaque permutation, la ligne source des predictions de chaque copie."""
    u, inv = np.unique(lignes_rep, return_inverse=True)
    out = []
    for _ in range(n_perm):
        s = C44.permuter_intra(len(u), seg[u], rng)
        out.append(u[s][inv])
    return out


def _exactitude_moyenne(P, V):
    """§5 Q1 : a44_mesures.exactitude_codes par personne, puis moyenne sur les personnes
    qui ont au moins une cellule (nanmean)."""
    e = C.exactitude_codes(P, V)
    return float(np.nanmean(e)) if np.isfinite(e).any() else np.nan


def _perte_moyenne(L, M):
    """§5 Q4 : moyenne par personne sur ses cellules, puis sur les personnes qui en ont."""
    n = M.sum(axis=1)
    ok = n > 0
    if not ok.any():
        return np.nan
    return float(np.mean(L.sum(axis=1)[ok] / n[ok]))


def mesurer(T, lignes_rep, cols, noms, permutations=None, avec_perte=True):
    """exa_A, exa_B, chute_A, perte_A, perte_B par configuration et rotation.

    lignes_rep : lignes du tournoi, avec repetitions (multiplicites des personnes).
    cols : sortie de colonnes_rotations (colonnes repetees selon les unites tirees)."""
    Vm = T["Vm"][lignes_rep]
    M = T["M"][lignes_rep]
    out = {}
    for nom in noms:
        P = T["preds"][nom]
        Pr = P[lignes_rep]
        res = {k: np.full(N_ROTATIONS, np.nan)
               for k in ("exa_A", "exa_B", "chute_A", "perte_A", "perte_B")}
        Lr = T["pertes"][nom][lignes_rep] if avec_perte else None
        for r, (cA, cB) in enumerate(cols):
            res["exa_A"][r] = _exactitude_moyenne(Pr[:, cA], Vm[:, cA])
            if avec_perte:
                res["exa_B"][r] = _exactitude_moyenne(Pr[:, cB], Vm[:, cB])
                res["perte_B"][r] = _perte_moyenne(Lr[:, cB], M[:, cB])
                res["perte_A"][r] = _perte_moyenne(Lr[:, cA], M[:, cA])
            if permutations:
                VA = Vm[:, cA]
                perm = np.mean([_exactitude_moyenne(P[np.ix_(p, cA)], VA)
                                for p in permutations])
                res["chute_A"][r] = res["exa_A"][r] - perm      # §5 Q2, t1_mesures.chute
        out[nom] = res
    return out


VARIANTE_PRINCIPALE = {"diagnostic": "residu", "conventionnel": "exactitude",
                       "perte": "perte_B"}


def selectionner(mes, candidates, r, variante=None):
    """§5 : c_diag = argmax residu (Q3), c_exa = argmax exa_A. S3 : diagnostic = chute
    brute. S5 : conventionnel = argmin perte_A. Departage §2 : premiere dans l'ordre de
    l'index (np.argmax et np.argmin rendent la premiere occurrence)."""
    v = variante or VARIANTE_PRINCIPALE
    exa = np.array([mes[c]["exa_A"][r] for c in candidates])
    chute = np.array([mes[c]["chute_A"][r] for c in candidates])
    if v["diagnostic"] == "residu":
        a, b = np.polyfit(exa, chute, 1)
        critere = chute - (a * exa + b)
    elif v["diagnostic"] == "chute_brute":
        critere = chute
    else:
        raise ValueError(v["diagnostic"])
    i_diag = int(np.argmax(critere))
    if v["conventionnel"] == "exactitude":
        i_exa = int(np.argmax(exa))
    elif v["conventionnel"] == "perte_A":
        i_exa = int(np.argmin([mes[c]["perte_A"][r] for c in candidates]))
    else:
        raise ValueError(v["conventionnel"])
    return i_diag, i_exa, critere


def perte_notee(mes, nom, r, variante=None):
    """§5 Q4, ou S4 : 1 - exactitude categorielle B."""
    v = variante or VARIANTE_PRINCIPALE
    if v["perte"] == "perte_B":
        return float(mes[nom]["perte_B"][r])
    if v["perte"] == "un_moins_exa_B":
        return 1.0 - float(mes[nom]["exa_B"][r])
    raise ValueError(v["perte"])


def calculer_delta(mes, candidates, variante=None):
    """§1 : Delta_r = perte_B(c_diag) - perte_B(c_exa), exactement 0 si meme choix ;
    Delta = moyenne des trois."""
    rot = []
    for r in range(N_ROTATIONS):
        i_d, i_e, crit = selectionner(mes, candidates, r, variante)
        c_d, c_e = candidates[i_d], candidates[i_e]
        delta_r = 0.0 if i_d == i_e else \
            perte_notee(mes, c_d, r, variante) - perte_notee(mes, c_e, r, variante)
        rot.append({"rotation": r + 1, "c_diag": c_d, "c_exa": c_e, "delta_r": delta_r,
                    "critere_diag": dict(zip(candidates, crit.tolist()))})
    return float(np.mean([x["delta_r"] for x in rot])), rot


# ---------------------------------------------------------------------------
# 4. Controles du §8, avant toute perte
# ---------------------------------------------------------------------------

def _ligne_ctrl(analyse, controle, rotation, role, valeur, seuil, passe):
    return {"analyse": analyse, "controle": controle, "rotation": rotation, "role": role,
            "valeur": valeur, "seuil": seuil, "passe": bool(passe)}


def controles_structure(T, struct, analyse, avec_c3_c4=True, poids_items=None):
    """C1, C2, C3, C4 sur le masque du tournoi. Pour une analyse R3 (avec_c3_c4=False),
    seule la condition d'au moins une cellule par personne demeure (§8, dernier alinea)."""
    m = len(struct["bloc"])
    poids = np.ones(m, dtype=np.int64) if poids_items is None else poids_items
    cols = colonnes_rotations(struct, poids)
    n = T["n"]
    out = []
    for r, (cA, cB) in enumerate(cols):
        for role, cc in (("B", cB), ("A", cA)):
            M, Vo = T["M"][:, cc], T["V_obs"][:, cc]
            cellules = M.sum(axis=1)
            out.append(_ligne_ctrl(analyse, "C3 au moins une cellule par personne", r + 1,
                                   role, int(cellules.min()) if n else 0, C3_CELLULES_MIN,
                                   n > 0 and cellules.min() >= C3_CELLULES_MIN))
            if not avec_c3_c4:
                continue
            couv = M.sum(axis=0) / n
            out.append(_ligne_ctrl(analyse, "C1 couverture minimale d'un item", r + 1, role,
                                   float(couv.min()), SEUIL_C1_COUVERTURE_ITEM,
                                   couv.min() >= SEUIL_C1_COUVERTURE_ITEM))
            garde = M.sum() / max(int(Vo.sum()), 1)
            out.append(_ligne_ctrl(analyse, "C2 part des cellules humaines gardees", r + 1,
                                   role, float(garde), SEUIL_C2_CELLULES_GARDEES,
                                   garde >= SEUIL_C2_CELLULES_GARDEES))
            if role == "B":
                part = float((cellules < C3_CELLULES_PEU).mean())
                out.append(_ligne_ctrl(analyse, "C3 part des personnes a moins de 10 "
                                       "cellules", r + 1, role, part, C3_PART_MAX_PEU,
                                       part <= C3_PART_MAX_PEU))
        if avec_c3_c4:
            nu = len(struct["unites_bloc"][r + 1])
            out.append(_ligne_ctrl(analyse, "C4 unites indivisibles dans B", r + 1, "B", nu,
                                   C4_UNITES_MIN, nu >= C4_UNITES_MIN))
    return out


def controle_temoin(T, struct, analyse, perms):
    """T : chute A des deux temoins B0 inferieure a 0,005 en valeur absolue, par rotation.
    Aucune perte n'est calculee."""
    cols = colonnes_rotations(struct, np.ones(len(struct["bloc"]), dtype=np.int64))
    mes = mesurer(T, np.arange(T["n"]), cols, TEMOINS, perms, avec_perte=False)
    out = []
    for nom in TEMOINS:
        for r in range(N_ROTATIONS):
            v = float(mes[nom]["chute_A"][r])
            out.append(_ligne_ctrl(analyse, f"T chute A du temoin {nom}", r + 1, "A",
                                   abs(v), SEUIL_T_TEMOIN, abs(v) < SEUIL_T_TEMOIN))
    return out


def controle_reproduction(d, lignes, analyse):
    """R : exactitude sur les 108 items entiers et les 2 058 personnes, sans masque de
    tournoi, egale a exactitude_vraie de t1 sous S_gra a 1e-12 pres. Seul « passe » ou
    « echoue » est ecrit, jamais la valeur (§8)."""
    ref = d.get("reference_t1")
    passe = ref is not None
    ecart = 0.0
    for nom in CANDIDATES_PRINCIPAL + ADVERSAIRES:
        if not passe or nom not in ref:
            passe = False
            continue
        mat = d["configs"][nom] if nom in d["configs"] else d["adversaires"][nom]
        e = _exactitude_moyenne(mat[lignes], d["verite"][lignes])
        ecart = max(ecart, abs(e - ref[nom])) if np.isfinite(e) else np.inf
    passe = passe and ecart <= SEUIL_R_REPRODUCTION
    return [_ligne_ctrl(analyse, "R reproduction de l'exactitude de t1", "", "108 items",
                        "", SEUIL_R_REPRODUCTION, passe)]


# ---------------------------------------------------------------------------
# 5. Bootstrap conjoint, regle de chute, tournoi complet
# ---------------------------------------------------------------------------

def tirer_replicat(rng, T, struct, n_perm):
    """§7 : (1) les personnes avec remise ; (2) dans chaque bloc separement, autant
    d'unites que le bloc en contient, avec remise ; (3) A_r = unites tirees dans les deux
    autres blocs (colonnes_rotations). Puis les permutations d'identites distinctes."""
    n = T["n"]
    lignes_rep = rng.integers(0, n, size=n)
    poids = np.zeros(len(struct["bloc"]), dtype=np.int64)
    for b in range(1, N_ROTATIONS + 1):
        us = struct["unites_bloc"][b]
        compte = np.bincount(rng.integers(0, len(us), size=len(us)), minlength=len(us))
        for u, c in zip(us, compte):
            poids[struct["unite"] == u] = c
    perms = permutations_identites(lignes_rep, T["seg"], n_perm, rng)
    return lignes_rep, poids, perms


def bootstrap(T, struct, candidates, params, analyse, horloge=time.monotonic):
    """Refait toute la selection dans chaque replicat. Regle de cout du §7."""
    rng = np.random.default_rng(params.graine_bootstrap)
    b_cible, reduit, t0 = params.n_bootstrap, False, horloge()
    reps, k = [], 0
    while k < b_cible:
        lignes_rep, poids, perms = tirer_replicat(rng, T, struct,
                                                  params.n_permutations_bootstrap)
        mes = mesurer(T, lignes_rep, colonnes_rotations(struct, poids), candidates, perms)
        delta, rot = calculer_delta(mes, candidates)
        ligne = {"analyse": analyse, "replicat": k, "delta": delta}
        for x in rot:
            r = x["rotation"]
            ligne[f"delta_{r}"] = x["delta_r"]
            ligne[f"c_diag_{r}"] = x["c_diag"]
            ligne[f"c_exa_{r}"] = x["c_exa"]
        reps.append(ligne)
        k += 1
        if (k == params.n_replicats_projection and b_cible == params.n_bootstrap
                and b_cible > params.n_bootstrap_reduit):
            projection = (horloge() - t0) / k * b_cible
            if projection > params.duree_max_projetee_s:
                b_cible, reduit = params.n_bootstrap_reduit, True
    deltas = np.array([x["delta"] for x in reps])
    bas, haut = (float(v) for v in np.percentile(deltas, PERCENTILES_IC))
    coincidence = {r: float(np.mean([x[f"c_diag_{r}"] == x[f"c_exa_{r}"] for x in reps]))
                   for r in range(1, N_ROTATIONS + 1)}
    for x in reps:
        x["B_effectif"], x["B_reduit_regle_de_cout"] = b_cible, reduit
    return {"replicats": reps, "ic_bas": bas, "ic_haut": haut, "B": b_cible,
            "reduit": reduit, "coincidence": coincidence}


def regle_de_chute(delta, ic_haut, familles, perte_pmm, perte_diag):
    """§9. La revendication survit si et seulement si R1 ET R2 ET R3 ET non R4."""
    r1 = bool(delta <= SEUIL_R1)
    r2 = bool(ic_haut < 0)
    r3 = all(v["delta"] < 0 for v in familles.values())
    affaiblis = sorted(f for f, v in familles.items() if SEUIL_R1 < v["delta"] < 0)
    r4_ferme = all(perte_pmm[r] <= perte_diag[r] for r in range(N_ROTATIONS))
    survit = r1 and r2 and r3 and not r4_ferme
    return {"statut": "survit" if survit else "ferme", "R1": r1, "R2": r2, "R3": r3,
            "R4_ferme": bool(r4_ferme), "affaibli_sans": affaiblis}


def analyser_tournoi(d, struct, analyse, pid_max, candidates, params, decrits,
                     avec_R=False, avec_regle=True, horloge=time.monotonic):
    """Un tournoi complet : controles, estimation ponctuelle, R3, bootstrap, regle."""
    lignes = lignes_perimetre(d, pid_max)
    T = preparer_tournoi(d, lignes, candidates, decrits)
    un = np.ones(len(struct["bloc"]), dtype=np.int64)
    perms = permutations_identites(np.arange(T["n"]), T["seg"], params.n_permutations,
                                   np.random.default_rng(params.graine_permutations))
    ctrl = controles_structure(T, struct, analyse)
    if all(c["passe"] for c in ctrl):
        ctrl += controle_temoin(T, struct, analyse, perms)
    if avec_R:
        ctrl += controle_reproduction(d, lignes, analyse)
    res = {"analyse": analyse, "n": T["n"], "candidates": list(candidates),
           "controles": ctrl, "T": T}
    if not all(c["passe"] for c in ctrl):
        res["decision"] = {"statut": "non concluant", "motif": "controle bloquant"}
        return res

    noms = list(candidates) + [k for k in decrits if k not in candidates]
    mes = mesurer(T, np.arange(T["n"]), colonnes_rotations(struct, un), noms, perms)
    delta, rot = calculer_delta(mes, candidates)
    res.update({"mesures": mes, "delta": delta, "rotations": rot})
    if not avec_regle:
        return res

    familles, ctrl_f = {}, []
    for f in struct["familles"]:
        poids = (struct["famille"] != f).astype(np.int64)
        c_f = controles_structure(T, struct, f"{analyse} sans {f}", avec_c3_c4=False,
                                  poids_items=poids)
        ctrl_f += c_f
        mes_f = mesurer(T, np.arange(T["n"]), colonnes_rotations(struct, poids),
                        candidates, perms)
        d_f, rot_f = calculer_delta(mes_f, candidates)
        familles[f] = {"delta": d_f, "rotations": rot_f,
                       "condition_cellule": all(c["passe"] for c in c_f)}
    res["familles"], res["controles_familles"] = familles, ctrl_f

    res["bootstrap"] = bootstrap(T, struct, candidates, params, analyse, horloge)
    perte_pmm = [float(mes[PMM]["perte_B"][r]) for r in range(N_ROTATIONS)]
    perte_diag = [float(mes[x["c_diag"]]["perte_B"][r]) for r, x in enumerate(rot)]
    if not all(v["condition_cellule"] for v in familles.values()):
        res["decision"] = {"statut": "non concluant",
                           "motif": "personne sans cellule dans une analyse R3 (I5)"}
    else:
        res["decision"] = regle_de_chute(delta, res["bootstrap"]["ic_haut"], familles,
                                         perte_pmm, perte_diag)
    res["decision"].update({"delta": delta, "ic_bas": res["bootstrap"]["ic_bas"],
                            "ic_haut": res["bootstrap"]["ic_haut"],
                            "perte_B_PMM": perte_pmm, "perte_B_c_diag": perte_diag})
    return res


# ---------------------------------------------------------------------------
# 6. Analyses secondaires (§10)
# ---------------------------------------------------------------------------

def secondaires(d, struct, principal, params, horloge=time.monotonic):
    mes, cand, rot = principal["mesures"], principal["candidates"], principal["rotations"]
    out = {}
    for nom, variante in (
            ("S3", dict(VARIANTE_PRINCIPALE, diagnostic="chute_brute")),
            ("S4", dict(VARIANTE_PRINCIPALE, perte="un_moins_exa_B")),
            ("S5", dict(VARIANTE_PRINCIPALE, conventionnel="perte_A"))):
        delta, r = calculer_delta(mes, cand, variante)
        out[nom] = {"delta": delta, "rotations": r}

    s2 = analyser_tournoi(d, struct, "S2", params.pid_max_principal, CANDIDATES_S2, params,
                          dict(d["adversaires"]), avec_regle=False, horloge=horloge)
    out["S2"] = {k: s2.get(k) for k in ("delta", "rotations", "controles", "decision",
                                         "mesures")}

    perte_diag = [float(mes[x["c_diag"]]["perte_B"][r]) for r, x in enumerate(rot)]
    if d.get("adversaires_s6"):
        s6 = {"perte_B_c_diag": perte_diag}
        for a in ADVERSAIRES:
            s6[f"perte_B_{a}_t1"] = [float(v) for v in mes[a]["perte_B"]]
            s6[f"perte_B_{a}_S6"] = [float(v) for v in mes["S6 " + a]["perte_B"]]
        s6["R4_ferme_S6"] = all(s6[f"perte_B_{PMM}_S6"][r] <= perte_diag[r]
                                for r in range(N_ROTATIONS))
        out["S6"] = s6

    out["S7"] = {nom: {k: [float(v) for v in mes[nom][k]]
                       for k in ("exa_A", "chute_A", "perte_B")}
                 for nom in DESCRIPTION_SEULE}

    coinc = principal["bootstrap"]["coincidence"]
    s8 = []
    for r, x in enumerate(rot):
        exa = [mes[a]["exa_A"][r] for a in ADVERSAIRES_S8]
        meilleur = ADVERSAIRES_S8[int(np.argmax(exa))]
        ligne = {"rotation": r + 1, "delta_r": x["delta_r"], "c_diag": x["c_diag"],
                 "c_exa": x["c_exa"], "part_coincidence_bootstrap": coinc[r + 1],
                 "meilleur_adversaire_par_exa_A": meilleur,
                 "perte_B_meilleur_adversaire": float(mes[meilleur]["perte_B"][r])}
        for b in BORNES_S8:
            ligne[f"perte_B_borne_{b}"] = float(mes[b]["perte_B"][r])
        s8.append(ligne)
    out["S8"] = s8
    return out


# ---------------------------------------------------------------------------
# 7. Sorties
# ---------------------------------------------------------------------------

def _fmt(v):
    if isinstance(v, (list, tuple)):
        return ";".join(_fmt(x) for x in v)
    if isinstance(v, (bool, np.bool_)):
        return "vrai" if v else "faux"
    if isinstance(v, (float, np.floating)):
        return repr(float(v))
    return str(v)


def _ecrire_csv(chemin, lignes):
    champs = []
    for l in lignes:
        for k in l:
            if k not in champs:
                champs.append(k)
    with open(chemin, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=champs or ["vide"], restval="",
                           lineterminator="\n")
        w.writeheader()
        for l in lignes:
            w.writerow({k: _fmt(v) for k, v in l.items()})
    return chemin


def _lignes_rotations(res):
    lignes = []
    if "mesures" in res:
        cand = res["candidates"]
        for r, x in enumerate(res["rotations"]):
            for nom, m in res["mesures"].items():
                lignes.append({
                    "analyse": res["analyse"], "rotation": r + 1, "configuration": nom,
                    "role": "candidate" if nom in cand else "hors selection",
                    "exa_A": m["exa_A"][r], "chute_A": m["chute_A"][r],
                    "res_A": x["critere_diag"][nom] if nom in cand else "",
                    "perte_B": m["perte_B"][r], "c_diag": x["c_diag"], "c_exa": x["c_exa"],
                    "delta_r": x["delta_r"], "delta": res["delta"]})
    if res.get("decision"):
        lignes.append(dict({"analyse": res["analyse"], "role": "decision"},
                           **res["decision"]))
    return lignes


def ecrire_sorties(resultat, sortie):
    _verifier_sortie(sortie)
    os.makedirs(sortie, exist_ok=True)
    p, s1, sec = resultat["principal"], resultat["S1"], resultat["secondaires"]
    ctrl = p["controles"] + s1["controles"] + p.get("controles_familles", []) + \
        s1.get("controles_familles", []) + (sec.get("S2") or {}).get("controles", [])
    rot = _lignes_rotations(p) + _lignes_rotations(s1)
    rot.append({"analyse": "lecture", "role": "decision", "statut": resultat["lecture"]})
    boot = (p.get("bootstrap") or {}).get("replicats", []) + \
        (s1.get("bootstrap") or {}).get("replicats", [])
    fam = []
    for res in (p, s1):
        for f, v in (res.get("familles") or {}).items():
            ligne = {"analyse": res["analyse"], "famille_retiree": f, "delta": v["delta"],
                     "strictement_negative": v["delta"] < 0,
                     "affaibli": SEUIL_R1 < v["delta"] < 0,
                     "condition_cellule": v["condition_cellule"]}
            for x in v["rotations"]:
                ligne[f"delta_{x['rotation']}"] = x["delta_r"]
                ligne[f"c_diag_{x['rotation']}"] = x["c_diag"]
                ligne[f"c_exa_{x['rotation']}"] = x["c_exa"]
            fam.append(ligne)
    secl = [{"analyse": "S1", "rotation": "", "cle": "statut",
             "valeur": s1.get("decision", {}).get("statut", "")}]
    for nom in ("S2", "S3", "S4", "S5"):
        if nom not in sec:
            continue
        if sec[nom].get("rotations"):
            secl.append({"analyse": nom, "rotation": "", "cle": "delta",
                         "valeur": sec[nom]["delta"]})
            for x in sec[nom]["rotations"]:
                for k in ("c_diag", "c_exa", "delta_r"):
                    secl.append({"analyse": nom, "rotation": x["rotation"], "cle": k,
                                 "valeur": x[k]})
        else:
            secl.append({"analyse": nom, "rotation": "", "cle": "statut",
                         "valeur": (sec[nom].get("decision") or {}).get("statut", "")})
    for k, v in sec.get("S6", {}).items():
        secl.append({"analyse": "S6", "rotation": "", "cle": k, "valeur": v})
    for nom, q in sec.get("S7", {}).items():
        for k, v in q.items():
            secl.append({"analyse": "S7", "rotation": "", "cle": f"{nom} | {k}",
                         "valeur": v})
    for l in sec.get("S8", []):
        for k, v in l.items():
            if k != "rotation":
                secl.append({"analyse": "S8", "rotation": l["rotation"], "cle": k,
                             "valeur": v})
    return [_ecrire_csv(os.path.join(sortie, n), l) for n, l in (
        ("tab-controles.csv", ctrl), ("tab-rotations.csv", rot),
        ("tab-bootstrap.csv", boot), ("tab-familles.csv", fam),
        ("tab-secondaires.csv", secl))]


def _verifier_sortie(sortie):
    data = os.path.realpath(os.path.join(RACINE, "data"))
    cible = os.path.realpath(sortie)
    if cible == data or cible.startswith(data + os.sep):
        raise ErreurGarde("aucune ecriture sous data/")


# ---------------------------------------------------------------------------
# 8. Execution
# ---------------------------------------------------------------------------

def executer(chargeur=None, params=None, sortie=None, ecrire=True, horloge=time.monotonic):
    """Toute l'evaluation. Sans chargeur injecte, lit les donnees reelles apres la garde
    et refuse des parametres differents de ceux du prereg."""
    params = Parametres() if params is None else params
    sortie = SORTIE if sortie is None else sortie
    _verifier_sortie(sortie)
    if chargeur is None:
        if params != Parametres():
            raise ErreurGarde("parametres differents du preenregistrement : refus sur les "
                              "donnees reelles")
        chargeur = charger_reel
    d = chargeur()
    valider_donnees(d)
    struct = structure_partition(d["partition"], d["items"], d["est_ordinal"])
    if len(struct["familles"]) != N_FAMILLES_ATTENDU:
        raise ErreurDonnees(f"{len(struct['familles'])} familles d'analyse, "
                            f"{N_FAMILLES_ATTENDU} attendues")

    decrits = dict(d["adversaires"])
    for k, v in (d.get("adversaires_s6") or {}).items():
        decrits["S6 " + k] = v
    for c in DESCRIPTION_SEULE:
        decrits[c] = d["configs"][c]
    principal = analyser_tournoi(d, struct, "principal", params.pid_max_principal,
                                 CANDIDATES_PRINCIPAL, params, decrits, avec_R=True,
                                 horloge=horloge)
    s1 = analyser_tournoi(d, struct, "S1", params.pid_max_s1, CANDIDATES_S1, params,
                          dict(d["adversaires"]), horloge=horloge)
    sec = secondaires(d, struct, principal, params, horloge) \
        if "bootstrap" in principal else {}

    st_p, st_1 = principal["decision"]["statut"], s1["decision"]["statut"]
    lecture = "survit, fragile au perimetre" if (st_p == "survit" and st_1 == "ferme") \
        else st_p
    resultat = {"principal": principal, "S1": s1, "secondaires": sec, "lecture": lecture,
                "parametres": dataclasses.asdict(params)}
    if ecrire:
        resultat["fichiers"] = ecrire_sorties(resultat, sortie)
    return resultat


def main(argv=None):
    ap = argparse.ArgumentParser(description="tab : evaluation preenregistree")
    ap.add_argument("--sortie", default=SORTIE)
    args = ap.parse_args(argv)
    try:
        res = executer(sortie=args.sortie)
    except (ErreurGarde, ErreurFuite, ErreurDonnees, TP.ErreurPartition) as e:
        print(f"REFUS : {e}", file=sys.stderr)
        return 2
    for nom in ("principal", "S1"):
        print(f"{nom} : {res[nom]['decision']}")
    print(f"lecture : {res['lecture']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
