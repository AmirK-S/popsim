"""
c7_controle_interpretabilite : le controle de fidelite prealable, gratuit, qui aurait
du etre exige avant le premier appel paye de la nuit du 11 au 12 septembre 2026.

===========================================================================
CE QUI S'EST PASSE (voir resultats/c7-reconciliation-facteurs-2026-09-12.md, lu en
entier avant d'ecrire ce fichier). Deux experiences payantes de cette nuit (les chaines
B<->M, B<->G, B<->P du plan factoriel, et le temoin B<->C "deux organisations") ont
mesure un contraste entre jumeaux sans jamais verifier que leurs jumeaux portaient une
personne. Leurs jumeaux ne reidentifiaient la vraie personne, contre les 120 humains
reels du meme bassin, qu'a 0,0-0,8 % (hasard = 0,83 %), la ou les jumeaux publies par
l'equipe Twin, sur le meme bassin, atteignent 20-39 %. Tous les contrastes de la chaine A
comparaient donc deux generateurs de bruit : leur ecart de 0,5 point ne mesurait rien.
L'une de ces mesures a fonde une conclusion publiee et annoncee a deux equipes exterieures
avant d'etre suspendue.

Second piege, avere deux fois cette nuit : la baseline demographique depend fortement de
la taille du bassin (2,13 % a 2 058 personnes, 9,20 % a 200, 13,29 % a 120). Comparer un
top-1 a la baseline d'un AUTRE bassin suffit a inverser une conclusion (c'est exactement
l'erreur du moonshot, corrigee section 5 du rapport de reconciliation).

CE QUE CE MODULE FAIT, ET RIEN D'AUTRE : avant d'interpreter tout contraste entre
jumeaux, verifier que le pipeline candidat depasse SIGNIFICATIVEMENT (IC bootstrap non
chevauchants, pas une comparaison de points) la baseline Demographics Only en top-1
contre les humains reels, LA BASELINE ETANT TOUJOURS RECALCULEE SUR LE BASSIN
EXACTEMENT ATTAQUE PAR LE CANDIDAT -- jamais fournie par l'appelant, jamais une
constante. C'est le coeur du controle : rien n'empeche structurellement de comparer a
la baseline du mauvais bassin, sauf que cette fonction ne prend JAMAIS de valeur de
baseline en argument -- seulement les indices qui definissent le bassin, et elle
recalcule la baseline elle-meme sur ces memes indices.

REGLE DE DECISION RETENUE (justifiee dans
resultats/controle-interpretabilite-2026-09-12.md) : IC bootstrap a 95 % non
chevauchants entre le top-1 du candidat contre les humains reels et le top-1 de
Demographics Only - GPT4.1-mini contre les MEMES humains, sur le MEME bassin (memes
personnes, memes items, meme fonction d'attaque, meme bootstrap). Le candidat "passe"
seulement si la borne basse de son IC est strictement superieure a la borne haute de
l'IC de la baseline. C'est un test conservateur (il peut rejeter un candidat dont la
vraie superiorite existe mais dont les IC se recouvrent legerement) choisi precisement
parce que le sinistre de cette nuit est un FAUX POSITIF (une non-difference interpretee
comme un signal) : en cas de doute, ce controle doit refuser de laisser interpreter,
jamais l'inverse.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee :
  t1_commun.charger                              les tables Twin-2K-500
  c7_reidentification.rangs_attaque               l'attaque de reidentification
  c7_reidentification.graine_nom                  graine stable par nom
  c7_reidentification.REF_V4 / DEMO / N_BOOTSTRAP les constantes de reference
  a2_commun.bootstrap_personnes                   l'IC a 95 % par reechantillonnage
                                                   de personnes
  c7_reconciliation_facteurs.attaque_vers_humain  l'attaque + IC, deja cablee EXACTEMENT
                                                   comme l'arbitrage de cette nuit l'a
                                                   calculee (memes graines) -- reprise
                                                   pour que ce controle reproduise les
                                                   memes chiffres que l'arbitrage sur les
                                                   memes donnees, pas des chiffres proches
  c7_reconciliation_facteurs.relire               relecture des traces payees (jsonl)
  c7_deux_organisations.GRAINE / tirer_echantillon / construire_banque_items
                                                   l'echantillon stratifie, bit a bit
                                                   identique a celui de l'arbitrage

CE QUI EST NOUVEAU ICI : la fonction de controle elle-meme (controle_avant_interpretation),
qui assemble ces briques dans un seul appel qui echoue bruyamment (leve
EchecControleInterpretabilite) au lieu de rendre un chiffre qu'on pourrait ignorer.

Aucun appel de modele, aucune depense, aucune recherche web. Lecture seule sur data/.
Usage :
  .venv/bin/python analyses/c7_controle_interpretabilite.py
===========================================================================
"""

import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                              # noqa: E402
from c7_reidentification import REF_V4, DEMO                         # noqa: E402
from c7_reconciliation_facteurs import attaque_vers_humain, relire    # noqa: E402
from c7_deux_organisations import (                                   # noqa: E402
    GRAINE, tirer_echantillon, construire_banque_items,
)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data", "traces")
TRACE_ORGS = os.path.join(TRACES, "c7-deux-organisations.jsonl")
TRACE_FACT = os.path.join(TRACES, "c7-factoriel.jsonl")


class EchecControleInterpretabilite(RuntimeError):
    """Leve quand un pipeline candidat ne depasse pas significativement, sur le bassin
    qu'il attaque reellement, la baseline Demographics Only calculee sur ce meme bassin.

    Ne JAMAIS attraper cette exception pour continuer a interpreter le contraste qui
    en depend : elle signifie que ce contraste comparerait du bruit contre du bruit,
    exactement comme les chaines B<->M, B<->G, B<->P de cette nuit.
    """


def controle_avant_interpretation(indices_personnes, indices_items, codes_candidat,
                                   nom_candidat, paq=None):
    """Le controle a appeler AVANT d'interpreter un contraste entre jumeaux, et avant
    le premier appel paye qui en dependrait.

    indices_personnes : indices, DANS LA POPULATION COMPLETE Twin-2K-500, des personnes
        du bassin REELLEMENT attaque par le candidat. Sa longueur fixe la taille du
        bassin -- c'est le seul endroit ou le bassin se choisit, et c'est ce meme
        tableau qui sert a recalculer la baseline : impossible de fournir une baseline
        d'un autre bassin, il n'y a pas de parametre pour ca.
    indices_items : indices de colonnes, DANS L'ESPACE COMPLET DES ITEMS, des items
        reellement utilises pour le contraste candidat (typiquement les 60 items
        toujours renseignes de c7_reidentification.items_communs).
    codes_candidat : matrice (len(indices_personnes), len(indices_items)) des codes du
        jumeau candidat, alignee ligne a ligne sur indices_personnes (la ligne i est le
        jumeau de la personne indices_personnes[i]) et colonne a colonne sur
        indices_items. -1 pour un item manquant, comme partout ailleurs dans ce depot.
    nom_candidat : etiquette (str) pour la graine de reechantillonnage et le rapport.
    paq : le paquet deja charge par t1_commun.charger(), pour eviter de le relire a
        chaque appel dans une suite de tests ; None le recharge.

    Retourne un dict de diagnostic si le candidat passe. Leve
    EchecControleInterpretabilite sinon -- y compris si le candidat ou la baseline ont
    une couverture trop faible (< 5 personnes) pour que quoi que ce soit soit mesurable.
    """
    indices_personnes = np.asarray(indices_personnes, dtype=int)
    indices_items = np.asarray(indices_items, dtype=int)
    attendu = (len(indices_personnes), len(indices_items))
    if tuple(codes_candidat.shape) != attendu:
        raise ValueError(
            f"codes_candidat a la forme {tuple(codes_candidat.shape)}, attendu "
            f"{attendu} d'apres indices_personnes ({len(indices_personnes)} personnes) "
            f"et indices_items ({len(indices_items)} items) : le bassin ou les items ne "
            "correspondent pas a ce qui est reellement teste. Corriger avant tout "
            "controle -- un bassin mal aligne invaliderait le controle lui-meme.")

    paq = paq if paq is not None else T1.charger()
    for requis in (REF_V4, DEMO):
        if requis not in paq["codes"]:
            raise RuntimeError(f"'{requis}' absent des donnees chargees : "
                                "le controle est impossible sans cette reference.")

    # Le bassin humain ET la baseline sont tranches sur EXACTEMENT les memes indices que
    # le candidat : c'est ce qui rend impossible de comparer a la baseline d'un autre
    # bassin (le second piege identifie cette nuit).
    humains = paq["codes"][REF_V4][indices_personnes][:, indices_items]
    demo = paq["codes"][DEMO][indices_personnes][:, indices_items]

    r_candidat = attaque_vers_humain(codes_candidat, humains, f"fid|{nom_candidat}")
    r_baseline = attaque_vers_humain(demo, humains, "baseline|demo")

    if r_candidat is None:
        raise EchecControleInterpretabilite(
            f"'{nom_candidat}' : moins de 5 personnes couvertes sur ce bassin de "
            f"{len(indices_personnes)} -- rien n'est mesurable, a fortiori "
            "interpretable.")
    if r_baseline is None:
        raise EchecControleInterpretabilite(
            "Demographics Only - GPT4.1-mini est couvert par moins de 5 personnes sur "
            "ce bassin : la baseline elle-meme n'est pas calculable ici, donc rien ne "
            "peut etre valide sur ce bassin.")

    passe = bool(r_candidat["top1_bas"] > r_baseline["top1_haut"])

    diagnostic = {
        "candidat": nom_candidat,
        "bassin": len(indices_personnes),
        "n_items": len(indices_items),
        "candidat_top1": r_candidat["top1"],
        "candidat_ic": (r_candidat["top1_bas"], r_candidat["top1_haut"]),
        "baseline_top1": r_baseline["top1"],
        "baseline_ic": (r_baseline["top1_bas"], r_baseline["top1_haut"]),
        "hasard": r_candidat["hasard"],
        "passe": passe,
    }

    if not passe:
        exc = EchecControleInterpretabilite(
            f"'{nom_candidat}' NE PASSE PAS le controle de fidelite prealable.\n"
            f"  bassin reellement attaque : {diagnostic['bassin']} personnes, "
            f"{diagnostic['n_items']} items\n"
            f"  top-1 candidat            : {diagnostic['candidat_top1']*100:.2f} % "
            f"[{diagnostic['candidat_ic'][0]*100:.2f} ; "
            f"{diagnostic['candidat_ic'][1]*100:.2f}]\n"
            f"  baseline Demographics Only (meme bassin, recalculee ici) : "
            f"{diagnostic['baseline_top1']*100:.2f} % "
            f"[{diagnostic['baseline_ic'][0]*100:.2f} ; "
            f"{diagnostic['baseline_ic'][1]*100:.2f}]\n"
            f"  hasard (1 / bassin)       : {diagnostic['hasard']*100:.2f} %\n"
            "Les IC se chevauchent (ou le candidat est en dessous) : ce pipeline ne "
            "transporte pas d'information individuelle demontrable sur ce bassin. Tout "
            "contraste construit sur ces jumeaux comparerait du bruit contre du bruit, "
            "comme les chaines B<->M, B<->G, B<->P de la nuit du 11 au 12 septembre "
            "2026. NE PAS interpreter ce candidat, NE PAS payer l'etape suivante avant "
            "de corriger le generateur.")
        exc.diagnostic = diagnostic          # pour l'inspection programmatique (tests)
        raise exc

    return diagnostic


# ---------------------------------------------------------------------------
# Application retrospective aux experiences de cette nuit (section 5 de la mission).
# ---------------------------------------------------------------------------

def _bassin_120(paq):
    """Le meme bassin de 120 personnes que l'arbitrage : ech identique bit a bit a
    celui de c7_factoriel / c7_reconciliation_facteurs, memes 60 items communs."""
    idx_items, _ = construire_banque_items(paq)
    ech = tirer_echantillon(paq["seg"]["S_gra"], 200, GRAINE)[:120]
    return ech, idx_items


def main():
    print(__doc__.split("=" * 75)[1], flush=True)
    paq = T1.charger()
    ech, idx_items = _bassin_120(paq)
    n_items = len(idx_items)
    print(f"bassin retrospectif : {len(ech)} personnes, {n_items} items "
          f"(identique a l'arbitrage)\n", flush=True)

    resultats = []

    # --- les cinq jumeaux payes cette nuit : DOIVENT ECHOUER ---
    XBC, _ = relire(TRACE_ORGS, "org", ["B", "C"], 120, n_items)
    XMGP, _ = relire(TRACE_FACT, "condition", ["M", "G", "P"], 120, n_items)
    candidats_nuit = {"B": XBC["B"], "C": XBC["C"], "M": XMGP["M"],
                      "G": XMGP["G"], "P": XMGP["P"]}

    print("=== Jumeaux payes cette nuit (attendu : ECHEC) ===", flush=True)
    for nom, X in candidats_nuit.items():
        try:
            d = controle_avant_interpretation(ech, idx_items, X, nom, paq=paq)
            print(f"  {nom:20s} PASSE (inattendu) top1={d['candidat_top1']*100:.2f} %",
                  flush=True)
            resultats.append((nom, "nuit", True))
        except EchecControleInterpretabilite as exc:
            print(f"  {nom:20s} ECHEC (attendu)\n" +
                  "\n".join("      " + l for l in str(exc).splitlines()), flush=True)
            resultats.append((nom, "nuit", False))

    # --- des jumeaux publies par l'equipe Twin, memes bassin/items : DOIVENT PASSER ---
    CONFIGS_TWIN = ["JSON Persona - GPT4.1", "Text Persona - GPT4.1-mini"]
    print("\n=== Jumeaux publies par l'equipe Twin, meme bassin (attendu : PASSE) ===",
          flush=True)
    for nom in CONFIGS_TWIN:
        X = paq["codes"][nom][:, idx_items][ech]
        try:
            d = controle_avant_interpretation(ech, idx_items, X, nom, paq=paq)
            print(f"  {nom:32s} PASSE top1={d['candidat_top1']*100:.2f} % "
                  f"[{d['candidat_ic'][0]*100:.2f};{d['candidat_ic'][1]*100:.2f}] "
                  f"vs baseline {d['baseline_top1']*100:.2f} % "
                  f"[{d['baseline_ic'][0]*100:.2f};{d['baseline_ic'][1]*100:.2f}]",
                  flush=True)
            resultats.append((nom, "twin", True))
        except EchecControleInterpretabilite as exc:
            print(f"  {nom:32s} ECHEC (inattendu)\n" +
                  "\n".join("      " + l for l in str(exc).splitlines()), flush=True)
            resultats.append((nom, "twin", False))

    n_nuit_echoue = sum(1 for _, grp, ok in resultats if grp == "nuit" and not ok)
    n_twin_passe = sum(1 for _, grp, ok in resultats if grp == "twin" and ok)
    print(f"\nverdict retrospectif : {n_nuit_echoue}/5 jumeaux de la nuit arretes, "
          f"{n_twin_passe}/{len(CONFIGS_TWIN)} jumeaux Twin laisses passer.", flush=True)
    print("\nRAPPEL : passer ce controle ne demontre PAS qu'une experience est "
          "interpretable ; cela demontre seulement qu'elle n'est pas disqualifiee "
          "d'avance par un generateur qui ne porte aucune personne.", flush=True)


if __name__ == "__main__":
    main()
