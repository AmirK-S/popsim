"""
test_controle_interpretabilite : verifie c7_controle_interpretabilite sur des donnees
REELLES (les jumeaux payes cette nuit et les jumeaux publies par l'equipe Twin, deja sur
disque, aucun appel reseau) puis sur deux cas synthetiques declares comme tels, qui
testent uniquement les garde-fous d'alignement bassin/items et de couverture minimale.

CAS 1, DOIT ECHOUER : les cinq jumeaux du plan factoriel / temoin deux-organisations
(B, C, M, G, P), qui ne reidentifient la vraie personne qu'au taux du hasard.
CAS 2, DOIT PASSER : un jumeau publie par l'equipe Twin (JSON Persona - GPT4.1), qui la
reidentifie a 38,9 % contre 13,3 % de baseline sur le meme bassin de 120.
CAS 3 (retrospectif, informatif) : les huit configurations Twin de
c7-reconciliation-facteurs sur ce meme bassin de 120, pour montrer HONNETEMENT que la
regle IC-non-chevauchants, a bassin aussi petit, ne laisse pas passer tout ce qui est
au dessus de 20 % (cf. limite disutee dans le rapport) -- ce n'est pas un echec de ce
fichier de test, c'est une propriete du bassin choisi que le rapport doit divulguer.
CAS 4 (synthetique, declare) : garde-fous purs -- forme incoherente, couverture nulle.

Usage : .venv/bin/python analyses/test_controle_interpretabilite.py
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                   # noqa: E402
from c7_reconciliation_facteurs import relire, TRACE_ORGS, TRACE_FACT      # noqa: E402
from c7_controle_interpretabilite import (                                 # noqa: E402
    controle_avant_interpretation, EchecControleInterpretabilite, _bassin_120,
)

ECHECS = []
N_VERIFS = [0]


def verifie(libelle, condition):
    N_VERIFS[0] += 1
    print(("  OK    " if condition else "  ECHEC ") + libelle, flush=True)
    if not condition:
        ECHECS.append(libelle)


print("Chargement des donnees Twin-2K-500 (une seule fois pour toute la suite)...",
      flush=True)
paq = T1.charger()
ech, idx_items = _bassin_120(paq)
n_items = len(idx_items)
print(f"bassin de reference : {len(ech)} personnes, {n_items} items\n", flush=True)


# ---------------------------------------------------------------------------
# CAS 1 : DOIT ECHOUER -- les jumeaux payes cette nuit, au niveau du hasard.
# ---------------------------------------------------------------------------
print("=== CAS 1 (donnees reelles) : jumeaux de la nuit, DOIT ECHOUER ===", flush=True)
XBC, _ = relire(TRACE_ORGS, "org", ["B", "C"], 120, n_items)
XMGP, _ = relire(TRACE_FACT, "condition", ["M", "G", "P"], 120, n_items)
jumeaux_nuit = {"B": XBC["B"], "C": XBC["C"], "M": XMGP["M"], "G": XMGP["G"],
                "P": XMGP["P"]}

for nom, X in jumeaux_nuit.items():
    leve = False
    diag = None
    try:
        controle_avant_interpretation(ech, idx_items, X, nom, paq=paq)
    except EchecControleInterpretabilite as exc:
        leve = True
        diag = exc.diagnostic
    verifie(f"'{nom}' leve EchecControleInterpretabilite (jumeau de la nuit)", leve)
    if diag is not None:
        verifie(f"'{nom}' : le controle est bien refuse (passe=False)", diag["passe"] is False)
        verifie(f"'{nom}' : top-1 mesure ({diag['candidat_top1']*100:.2f} %) proche du "
                f"hasard ({diag['hasard']*100:.2f} %), tres en dessous de la baseline "
                f"({diag['baseline_top1']*100:.2f} %)",
                diag["candidat_top1"] < diag["hasard"] + 0.05)

# ---------------------------------------------------------------------------
# CAS 2 : DOIT PASSER -- un jumeau publie par l'equipe Twin, nettement fidele.
# ---------------------------------------------------------------------------
print("\n=== CAS 2 (donnees reelles) : jumeau Twin fidele, DOIT PASSER ===", flush=True)
NOM_BON = "JSON Persona - GPT4.1"
X_bon = paq["codes"][NOM_BON][:, idx_items][ech]
try:
    diag_bon = controle_avant_interpretation(ech, idx_items, X_bon, NOM_BON, paq=paq)
    verifie(f"'{NOM_BON}' passe le controle (top1={diag_bon['candidat_top1']*100:.2f} % "
            f"vs baseline {diag_bon['baseline_top1']*100:.2f} %)", diag_bon["passe"])
    verifie("'{}' : IC candidat entierement au dessus de l'IC baseline ({:.2f} > {:.2f})"
            .format(NOM_BON, diag_bon["candidat_ic"][0] * 100,
                    diag_bon["baseline_ic"][1] * 100),
            diag_bon["candidat_ic"][0] > diag_bon["baseline_ic"][1])
except EchecControleInterpretabilite:
    verifie(f"'{NOM_BON}' passe le controle", False)

# ---------------------------------------------------------------------------
# CAS 3, retrospectif et informatif : les huit configurations Twin sur ce meme bassin
# de 120. Non asserte pass/fail global -- sert a documenter honnetement ou la regle
# (IC non chevauchants) est franchie et ou elle ne l'est pas a ce bassin.
# ---------------------------------------------------------------------------
print("\n=== CAS 3 (informatif) : les huit configurations Twin, bassin=120 ===",
      flush=True)
CONFIGS_TWIN = [
    "Demographics Only - GPT4.1-mini", "JSON Persona - GPT4.1",
    "JSON Persona - GPT4.1-mini", "Text Persona (Default Temperature) - GPT4.1-mini",
    "Text Persona (Reasoning) - GPT4.1-mini",
    "Text Persona (Repeating Questions) - GPT4.1-mini", "Text Persona - GPT4.1-mini",
    "Text Persona - Gemini-Flash2.5",
]
n_passent = 0
for nom in CONFIGS_TWIN:
    if nom not in paq["codes"]:
        continue
    X = paq["codes"][nom][:, idx_items][ech]
    try:
        d = controle_avant_interpretation(ech, idx_items, X, nom, paq=paq)
        n_passent += 1
        print(f"  PASSE  {nom:52s} top1={d['candidat_top1']*100:5.2f} %", flush=True)
    except EchecControleInterpretabilite as exc:
        d = exc.diagnostic
        print(f"  ECHEC  {nom:52s} top1={d['candidat_top1']*100:5.2f} % "
              f"(baseline {d['baseline_top1']*100:5.2f} % "
              f"[{d['baseline_ic'][0]*100:.2f};{d['baseline_ic'][1]*100:.2f}])",
              flush=True)
print(f"  -> {n_passent}/{len(CONFIGS_TWIN) - 1} jumeaux non-demographiques passent a "
      "bassin=120 (Demographics Only exclu, il EST la baseline). Voir le rapport pour "
      "la limite que cela revele : a n=120 la baseline a un IC large, seuls les jumeaux "
      "nettement au dessus (~35-40 %) s'en separent sans ambiguite ; les jumeaux a "
      "20-30 % ne se separent pas tous a ce bassin precis, alors qu'ils s'en separeraient "
      "nettement a un bassin plus grand (baseline ~2 % a 2058 personnes).", flush=True)

# ---------------------------------------------------------------------------
# CAS 4, SYNTHETIQUE DECLARE : garde-fous purs, aucune donnee Twin impliquee.
# ---------------------------------------------------------------------------
print("\n=== CAS 4 (synthetique declare) : garde-fous d'alignement et de couverture ===",
      flush=True)

# 4a. forme incoherente entre indices_personnes/items et codes_candidat.
try:
    controle_avant_interpretation(ech, idx_items, np.zeros((5, 5), dtype=np.int32),
                                   "forme_fausse", paq=paq)
    verifie("forme incoherente : ValueError attendue", False)
except ValueError:
    verifie("forme incoherente (5x5 contre bassin 120x60) : ValueError levee", True)
except EchecControleInterpretabilite:
    verifie("forme incoherente : ValueError attendue (pas EchecControleInterpretabilite)",
            False)

# 4b. couverture nulle : un candidat entierement manquant (-1 partout) sur un tout petit
# bassin synthetique de 3 personnes -- ni le candidat ni la baseline ne peuvent
# atteindre le minimum de 5 personnes couvertes exige.
petit_bassin = ech[:3]
candidat_vide = np.full((3, n_items), -1, dtype=np.int32)
try:
    controle_avant_interpretation(petit_bassin, idx_items, candidat_vide,
                                   "candidat_synthetique_vide", paq=paq)
    verifie("candidat entierement manquant : EchecControleInterpretabilite attendue",
            False)
except EchecControleInterpretabilite:
    verifie("candidat entierement manquant sur bassin synthetique de 3 personnes : "
            "EchecControleInterpretabilite levee (couverture insuffisante)", True)


# ---------------------------------------------------------------------------
if ECHECS:
    print(f"\n{len(ECHECS)} ECHEC(S) sur {N_VERIFS[0]} verifications :")
    for e in ECHECS:
        print("  - " + e)
    sys.exit(1)
print(f"\nTOUT PASSE : {N_VERIFS[0]} verifications.")
