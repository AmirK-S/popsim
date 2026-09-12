"""
c7_factoriel : plan factoriel un-facteur-a-la-fois pour A7 (M / G / P).

===========================================================================
PREENREGISTREMENT : resultats/c7-factoriel-preenregistrement.md, ecrit le
12 septembre 2026, AVANT tout appel payant, AVANT ce fichier, et commite seul,
avant tout appel.

CE QUE CE SCRIPT FAIT. L'experience « deux organisations »
(analyses/c7_deux_organisations.py) a fait varier trois facteurs a la fois --
modele, gabarit de prompt, format de persona -- et mesure un effondrement du
canal inter-jumeaux (top-1 B<->C = 1,76 % [0,35 ; 3,63] sur n = 142). Ce
script isole lequel des trois facteurs porte ce signal, en changeant UNE SEULE
chose a la fois par rapport a l'organisation B :

  (M) modele different    : prompt_b (persona JSON, gabarit B) rejoue avec
                             MODELE_C au lieu de MODELE_B. Aucune nouvelle
                             fonction de gabarit.
  (G) gabarit different   : nouvelle fonction prompt_g, gabarit/format de
                             sortie de C (un tour utilisateur, sortie
                             « k) n ») applique au dossier JSON (persona_json,
                             la fonction de B), avec MODELE_B.
  (P) persona differente  : nouvelle fonction prompt_p, gabarit de B
                             (systeme+utilisateur, sortie « Qxx: n ») applique
                             a la biographie narrative (persona_narrative, la
                             fonction de C), avec MODELE_B.

CE QUI EST REPRIS TEL QUEL, sans une ligne recopiee, importe directement
depuis analyses/c7_deux_organisations.py (qui les importe lui-meme, sans
ligne recopiee, de t1_commun / a2_commun / c7_reidentification) :
  tirer_echantillon, GRAINE, N_PERSONNES, charger_labels, persona_champs,
  persona_json, persona_narrative, blocs_questions, SYSTEME_B, prompt_b,
  parser_b, parser_c, construire_banque_items, MODELE_B, MODELE_C,
  FOURNISSEUR_B, FOURNISSEUR_C, MAX_PRICE_B, MAX_PRICE_C, MAX_TOKENS_B,
  MAX_TOKENS_C, cle_api, appeler_chat, Arret429, Budget, borner_codes,
  items_communs, rangs_attaque, rang_dans_segment, graine_nom,
  bootstrap_personnes, REF_V4, REF_V13, DEMO, N_BOOTSTRAP, N_TIRAGES_LIENS.

Les trois deviations declarees dans c7_deux_organisations.py (reponse par
NUMERO, persona narrative reperee par QID, format de sortie C reecrit contre
la boucle de repetition) sont heritees automatiquement : aucune des fonctions
citees ci-dessus n'est reecrite ici.

ORGANISATION B RECYCLEE COMME BRAS COMMUN : les 143 reponses B deja reussies
dans data/traces/c7-deux-organisations.jsonl (couverture 100 %, index locaux
0..142 du meme echantillon stratifie) sont relues et reutilisees comme le
bras fixe de chacune des trois attaques symetriques B<->M, B<->G, B<->P.
Aucun nouvel appel B n'est fait ici. Ce fichier de trace n'est jamais modifie
(lecture seule).

Depense : appels reseau reels vers OpenRouter pour M, G, P uniquement. Plafond
dur de la tache : 1,00 USD. Arret interne si le cumul mesure (usage.cost
annonce, jamais une estimation) depasse ARRET_INTERNE_USD. Un HTTP 429 portant
un identifiant de generation arrete le script immediatement (protocole de
rapprochement du projet, non improvise ici) ; data/traces/STOP, s'il existe,
est respecte en lecture seule avant chaque appel.

Sortie : resultats/c7-factoriel.csv, resultats/c7-factoriel-resultats.md,
         data/traces/c7-factoriel.jsonl (une ligne par appel M/G/P reussi ou
         rejete).
Usage :
  .venv/bin/python analyses/c7_factoriel.py --essai 3    # pilote, 3 personnes
  .venv/bin/python analyses/c7_factoriel.py              # campagne, 120 personnes
===========================================================================
"""

import argparse
import datetime
import json
import os
import sys
from decimal import Decimal

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS",
           "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "4")

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import t1_commun as T1                                                    # noqa: E402
from a2_commun import bootstrap_personnes                                 # noqa: E402
from c7_reidentification import (                                          # noqa: E402
    items_communs, rangs_attaque, rang_dans_segment, graine_nom,
    REF_V4, DEMO, N_BOOTSTRAP,
)
from c7_deux_organisations import (                                        # noqa: E402
    tirer_echantillon, GRAINE, charger_labels, persona_champs,
    persona_json, persona_narrative, blocs_questions, SYSTEME_B,
    prompt_b, parser_b, parser_c, construire_banque_items,
    MODELE_B, MODELE_C, FOURNISSEUR_B, FOURNISSEUR_C,
    MAX_PRICE_B, MAX_PRICE_C, MAX_TOKENS_B, MAX_TOKENS_C,
    cle_api, appeler_chat, Arret429, Budget, borner_codes,
)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SORTIE = os.path.join(RACINE, "resultats")
TRACES = os.path.join(RACINE, "data", "traces")

FICHIER_ARRET_GLOBAL = os.path.join(TRACES, "STOP")                # lecture seule
TRACE_ORG_B_EXISTANTE = os.path.join(TRACES, "c7-deux-organisations.jsonl")  # lecture seule
TRACE_JSONL = os.path.join(TRACES, "c7-factoriel.jsonl")

N_PERSONNES_FACTORIEL = 120     # cf. preenregistrement section 3

PLAFOND_DUR_USD = Decimal("1.00")
ARRET_INTERNE_USD = Decimal("0.90")

# Bornes deja connues, citees telles quelles (cf. preenregistrement section 0) --------
BORNE_INTRA_EQUIPE_TOP1 = 0.3638          # c7-temoin-prompt-resultats.md
BORNE_TOUT_DIFFERENT = {                  # c7-deux-organisations-resultats.md, n=142
    "top1": 0.0176, "top1_bas": 0.0035, "top1_haut": 0.0363,
}


# ---------------------------------------------------------------------------------------
# 1. Nouveaux gabarits combinatoires : G (gabarit de C + persona JSON de B),
#    P (gabarit de B + persona narrative de C). M ne construit rien de nouveau : c'est
#    prompt_b rejoue avec un autre modele (cf. docstring).
# ---------------------------------------------------------------------------------------

def prompt_g(champs, questions):
    """Gabarit G : le style d'instructions et le format de sortie du gabarit C (un seul
    tour utilisateur, sortie une ligne par question « k) n », parser_c), applique au
    dossier JSON (persona_json, la meme fonction que B, jamais persona_narrative). Reprend
    verbatim le style d'instructions de prompt_c (c7_deux_organisations.py), seul le
    contenu du dossier change (JSON au lieu de biographie)."""
    lignes_q = []
    for opts, membres in blocs_questions(questions):
        legende = " ".join(f"({j+1}) {o}" for j, o in enumerate(opts))
        lignes_q.append(f"(pour les questions qui suivent, les choix possibles sont : "
                         f"{legende})")
        for k, texte in membres:
            lignes_q.append(f"{k}) {texte}")
    utilisateur = (
        "Mets-toi à la place de la personne suivante et réponds comme elle le ferait.\n\n"
        "Voici son dossier (JSON) :\n" + persona_json(champs) + "\n\n"
        "Voici maintenant une série de courtes questions, numérotées de 1 à "
        f"{len(questions)}. Réponds à CHAQUE question sur sa PROPRE ligne, au format "
        "exact « numéro) numéro-de-l'option », par exemple « 1) 3 ». Une ligne par "
        "question, dans l'ordre, rien d'autre.\n\n" + "\n".join(lignes_q)
    )
    return [{"role": "user", "content": utilisateur}]


def prompt_p(champs, colonnes_demo, questions):
    """Gabarit P : le gabarit systeme/utilisateur de B (SYSTEME_B, sortie « Qxx: n »,
    parser_b) applique a la biographie narrative (persona_narrative, la meme fonction que
    C, jamais persona_json). Reprend verbatim la structure d'instructions de prompt_b
    (c7_deux_organisations.py), seul le contenu du dossier change (biographie au lieu de
    JSON)."""
    bio = persona_narrative(champs, colonnes_demo)
    lignes_q = []
    for opts, membres in blocs_questions(questions):
        legende = "; ".join(f"{j+1}) {o}" for j, o in enumerate(opts))
        lignes_q.append(f"[Options pour les questions suivantes : {legende}]")
        for k, texte in membres:
            lignes_q.append(f"Q{k:02d}: {texte}")
    utilisateur = (
        "DOSSIER :\n" + bio + "\n\n"
        "QUESTIONS :\n" + "\n".join(lignes_q) + "\n\n"
        "Réponds avec « identifiant: numéro » pour chacune, dans l'ordre donné, une "
        "ligne par question."
    )
    return [{"role": "system", "content": SYSTEME_B}, {"role": "user", "content": utilisateur}]


# ---------------------------------------------------------------------------------------
# 2. Les trois conditions, decrites de facon uniforme
# ---------------------------------------------------------------------------------------

def construire_conditions(champs, colonnes_demo, banque):
    """Renvoie {nom_condition: (messages, modele, fournisseur, max_price, parser,
    max_tokens)}. M reutilise prompt_b tel quel avec MODELE_C ; G et P sont les
    combinaisons nouvelles ci-dessus, toutes deux avec MODELE_B."""
    return {
        "M": (prompt_b(champs, banque), MODELE_C, FOURNISSEUR_C, MAX_PRICE_C,
              parser_b, MAX_TOKENS_B),
        "G": (prompt_g(champs, banque), MODELE_B, FOURNISSEUR_B, MAX_PRICE_B,
              parser_c, MAX_TOKENS_C),
        "P": (prompt_p(champs, colonnes_demo, banque), MODELE_B, FOURNISSEUR_B,
              MAX_PRICE_B, parser_b, MAX_TOKENS_B),
    }


# ---------------------------------------------------------------------------------------
# 3. Relecture du bras B existant (lecture seule, jamais modifie)
# ---------------------------------------------------------------------------------------

def relire_org_b(n_personnes, n_items):
    XB = np.full((n_personnes, n_items), -1, dtype=np.int32)
    if not os.path.exists(TRACE_ORG_B_EXISTANTE):
        sys.exit(f"trace absente : {TRACE_ORG_B_EXISTANTE}")
    dispo = set()
    for ligne in open(TRACE_ORG_B_EXISTANTE, encoding="utf-8"):
        try:
            e = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if not e.get("succes") or e.get("org") != "B":
            continue
        i = e["sample_idx"]
        if i < n_personnes:
            XB[i] = np.array(e["codes"], dtype=np.int32)
            dispo.add(i)
    manquants = set(range(n_personnes)) - dispo
    if manquants:
        sys.exit(f"organisation B manquante dans la trace existante pour les index locaux "
                  f"{sorted(manquants)[:10]}... ({len(manquants)} manquants) : reduire "
                  f"--n-personnes ou completer la trace existante d'abord.")
    return XB


# ---------------------------------------------------------------------------------------
# 4. Trace brute, une ligne par appel
# ---------------------------------------------------------------------------------------

def ecrire_trace(ligne):
    os.makedirs(TRACES, exist_ok=True)
    with open(TRACE_JSONL, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
        fh.flush()
        os.fsync(fh.fileno())


def appels_deja_faits():
    faits = set()
    if not os.path.exists(TRACE_JSONL):
        return faits
    for ligne in open(TRACE_JSONL, encoding="utf-8"):
        try:
            e = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if e.get("succes"):
            faits.add((e["sample_idx"], e["condition"]))
    return faits


def relire_codes_depuis_trace(n_personnes, n_items):
    X = {c: np.full((n_personnes, n_items), -1, dtype=np.int32) for c in ("M", "G", "P")}
    if not os.path.exists(TRACE_JSONL):
        return X
    for ligne in open(TRACE_JSONL, encoding="utf-8"):
        try:
            e = json.loads(ligne)
        except json.JSONDecodeError:
            continue
        if not e.get("succes"):
            continue
        X[e["condition"]][e["sample_idx"]] = np.array(e["codes"], dtype=np.int32)
    return X


# ---------------------------------------------------------------------------------------
# 5. Boucle principale de generation : pour chaque personne, M puis G puis P
# ---------------------------------------------------------------------------------------

def generer(paq, echantillon, items, n_appels_max=None):
    idx_items, banque = items
    n_items = len(banque)
    n_options = [len(it["options"]) for it in banque]
    lab = charger_labels(paq)
    colonnes = paq["demo"]["colonnes_contexte"]
    colonnes_demo = set(paq["demo"]["colonnes_demo"])

    cle = cle_api()
    budget = Budget(PLAFOND_DUR_USD, ARRET_INTERNE_USD)
    deja = appels_deja_faits()
    X = relire_codes_depuis_trace(len(echantillon), n_items)
    if os.path.exists(TRACE_JSONL):
        for ligne in open(TRACE_JSONL, encoding="utf-8"):
            try:
                e = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            if e.get("succes") and e.get("cout_usd") is not None:
                budget.cumul += Decimal(str(e["cout_usd"]))
                budget.n_appels += 1
    print(f"cumul deja depense (reprise) : {budget.cumul} USD, {budget.n_appels} appels",
          flush=True)

    n_faits_ce_run = 0
    for local_i, pers_idx in enumerate(echantillon):
        if n_appels_max is not None and n_faits_ce_run >= n_appels_max:
            break
        champs = persona_champs(lab, int(pers_idx), colonnes)
        conditions = construire_conditions(champs, colonnes_demo, banque)
        for nom in ("M", "G", "P"):
            messages, modele, fournisseur, max_price, parser, max_tok = conditions[nom]
            if (local_i, nom) in deja:
                continue
            if os.path.exists(FICHIER_ARRET_GLOBAL):
                sys.exit("data/traces/STOP present : arret propre, lecture seule.")
            budget.verifier_avant_appel()
            rep = appeler_chat(cle, modele, messages, fournisseur, max_price, max_tok)
            horodatage = datetime.datetime.now().astimezone().isoformat(timespec="seconds")
            if "erreur" in rep:
                ecrire_trace({"horodatage": horodatage, "sample_idx": local_i,
                              "condition": nom, "modele": modele, "succes": False,
                              "erreur": rep})
                print(f"[{local_i}/{len(echantillon)}] {nom} : ECHEC {rep.get('erreur')}",
                      flush=True)
                continue
            codes = parser(rep["texte"], n_items)
            codes = np.where((codes >= 0) & (codes < np.array(n_options)), codes, -1)
            budget.ajouter(rep.get("cout_annonce"))
            ecrire_trace({
                "horodatage": horodatage, "sample_idx": local_i, "condition": nom,
                "modele": modele, "succes": True, "raison": rep.get("raison"),
                "jetons_entree": rep.get("jetons_entree"),
                "jetons_sortie": rep.get("jetons_sortie"),
                "cout_usd": rep.get("cout_annonce"),
                "n_reponses_lues": int((codes >= 0).sum()),
                "codes": codes.tolist(),
                "texte_brut": rep["texte"][:4000],
            })
            X[nom][local_i] = codes
            n_faits_ce_run += 1
            print(f"[{local_i}/{len(echantillon)}] {nom} : "
                  f"{int((codes >= 0).sum())}/{n_items} reponses lues, "
                  f"cout cumule {budget.cumul} USD", flush=True)
    return X, budget


# ---------------------------------------------------------------------------------------
# 6. Mesure : attaque symetrique B<->X, reprise telle quelle de c7_reidentification
# ---------------------------------------------------------------------------------------

def resume_taux(indic, graine):
    return bootstrap_personnes(indic, n_tirages=N_BOOTSTRAP, graine=graine)


def mesurer_condition(nom, paq, echantillon, XB, XX):
    couverts = np.flatnonzero((XB >= 0).any(axis=1) & (XX >= 0).any(axis=1))
    n = len(couverts)
    seg_gra_ech = paq["seg"]["S_gra"][echantillon]

    rng_f = np.random.default_rng([GRAINE, graine_nom(f"B<->{nom}")])
    rang_f, top1_f, top10_f = rangs_attaque(XB[couverts], XX, couverts, rng_f)
    rang_seg_f, top1_seg_f, taille_seg_f = rang_dans_segment(
        XB[couverts], couverts, XX, seg_gra_ech, rng_f)

    rng_r = np.random.default_rng([GRAINE, graine_nom(f"{nom}<->B")])
    rang_r, top1_r, top10_r = rangs_attaque(XX[couverts], XB, couverts, rng_r)
    rang_seg_r, top1_seg_r, taille_seg_r = rang_dans_segment(
        XX[couverts], couverts, XB, seg_gra_ech, rng_r)

    top1_sym = (top1_f + top1_r) / 2.0
    top10_sym = (top10_f + top10_r) / 2.0
    top1_seg_sym = (top1_seg_f + top1_seg_r) / 2.0
    rang_sym = (rang_f + rang_r) / 2.0
    rang_seg_sym = (rang_seg_f + rang_seg_r) / 2.0

    m_t1, b_t1, h_t1 = resume_taux(top1_sym, [GRAINE, graine_nom(nom), 11])
    m_t10, b_t10, h_t10 = resume_taux(top10_sym, [GRAINE, graine_nom(nom), 12])
    m_t1s, b_t1s, h_t1s = resume_taux(top1_seg_sym, [GRAINE, graine_nom(nom), 13])

    return {
        "condition": f"B<->{nom}", "n_attaques": n, "n_pool": n,
        "top1": m_t1, "top1_bas": b_t1, "top1_haut": h_t1,
        "top10": m_t10, "top10_bas": b_t10, "top10_haut": h_t10,
        "rang_median": float(np.median(rang_sym)),
        "top1_hasard": 1.0 / n if n else float("nan"),
        "top1_segment": m_t1s, "top1_segment_bas": b_t1s, "top1_segment_haut": h_t1s,
        "rang_segment_median": float(np.median(rang_seg_sym)),
        "taille_segment_mediane": float(np.median(
            np.concatenate([taille_seg_f[taille_seg_f > 0], taille_seg_r[taille_seg_r > 0]])))
        if (taille_seg_f > 0).any() or (taille_seg_r > 0).any() else float("nan"),
    }


def mesurer_demo(paq, echantillon, idx_items, n):
    """Demographics Only recalculee sur le pool des n personnes de cette campagne, meme
    methode que c7_deux_organisations.mesurer (importee en esprit, reprise ici car le
    pool differe : 120 personnes au lieu de 200)."""
    codes_demo = paq["codes"][DEMO][:, idx_items][echantillon[:n]]
    codes_v4 = paq["codes"][REF_V4][:, idx_items][echantillon[:n]]
    couverts_demo = np.flatnonzero((codes_demo >= 0).any(axis=1))
    seg_gra_ech = paq["seg"]["S_gra"][echantillon[:n]]
    rng_demo = np.random.default_rng([GRAINE, graine_nom(DEMO), n])
    rang_d, top1_d, top10_d = rangs_attaque(
        codes_demo[couverts_demo], codes_v4, couverts_demo, rng_demo)
    rang_seg_d, top1_seg_d, taille_seg_d = rang_dans_segment(
        codes_demo[couverts_demo], couverts_demo, codes_v4, seg_gra_ech, rng_demo)
    m_t1d, b_t1d, h_t1d = resume_taux(top1_d, [GRAINE, graine_nom(DEMO), 14, n])
    m_t10d, b_t10d, h_t10d = resume_taux(top10_d, [GRAINE, graine_nom(DEMO), 15, n])
    m_t1sd, b_t1sd, h_t1sd = resume_taux(top1_seg_d, [GRAINE, graine_nom(DEMO), 16, n])
    n_d = len(couverts_demo)
    return {
        "condition": DEMO + f" (pool={n}, recalcule)", "n_attaques": n_d, "n_pool": n,
        "top1": m_t1d, "top1_bas": b_t1d, "top1_haut": h_t1d,
        "top10": m_t10d, "top10_bas": b_t10d, "top10_haut": h_t10d,
        "rang_median": float(np.median(rang_d)),
        "top1_hasard": 1.0 / n, "top1_segment": m_t1sd,
        "top1_segment_bas": b_t1sd, "top1_segment_haut": h_t1sd,
        "rang_segment_median": float(np.median(rang_seg_d)),
        "taille_segment_mediane": float(np.median(taille_seg_d[taille_seg_d > 0]))
        if (taille_seg_d > 0).any() else float("nan"),
    }


# ---------------------------------------------------------------------------------------
# 7. Verdict, regles preenregistrees section 5
# ---------------------------------------------------------------------------------------

def porte_le_signal(ligne, top1_demo):
    return bool(ligne["top1_bas"] > BORNE_TOUT_DIFFERENT["top1_haut"]
                and ligne["top1"] >= 2 * top1_demo)


def verdict(lignes, top1_demo):
    porte = {nom: porte_le_signal(lignes[nom], top1_demo) for nom in ("M", "G", "P")}
    n_porte = sum(porte.values())
    if n_porte == 0:
        conclusion = "aucun facteur ne porte le signal seul (interaction)"
    elif n_porte == 1:
        (seul,) = [k for k, v in porte.items() if v]
        conclusion = f"le facteur {seul} porte le signal seul"
    else:
        conclusion = (f"plusieurs facteurs portent le signal seuls : "
                      f"{[k for k, v in porte.items() if v]}")
    return {"porte_le_signal": porte, "conclusion": conclusion,
            "top1_demo_pool": top1_demo,
            "borne_tout_different": BORNE_TOUT_DIFFERENT,
            "borne_intra_equipe": BORNE_INTRA_EQUIPE_TOP1}


# ---------------------------------------------------------------------------------------
# 8. main
# ---------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--essai", type=int, default=0,
                    help="ne generer que les N premieres personnes (pilote)")
    ap.add_argument("--n-personnes", type=int, default=N_PERSONNES_FACTORIEL)
    ap.add_argument("--mesurer-seulement", action="store_true")
    args = ap.parse_args()

    print("c7_factoriel : plan un-facteur-a-la-fois (M / G / P)", flush=True)
    paq = T1.charger()
    idx_items, banque = construire_banque_items(paq)
    print(f"{len(banque)} items cibles construits", flush=True)

    # meme graine, meme n=200 que c7_deux_organisations : echantillon identique bit a bit
    echantillon = tirer_echantillon(paq["seg"]["S_gra"], 200, GRAINE)
    echantillon = echantillon[:args.n_personnes]
    print(f"sous-echantillon : {len(echantillon)} personnes (index locaux 0..{len(echantillon)-1} "
          "du meme tirage stratifie S_gra que c7_deux_organisations)", flush=True)

    XB = relire_org_b(len(echantillon), len(banque))
    print(f"organisation B relue depuis la trace existante : "
          f"{int((XB >= 0).any(axis=1).sum())}/{len(echantillon)} personnes couvertes",
          flush=True)

    n_appels_max = (3 * args.essai) if args.essai else None
    if not args.mesurer_seulement:
        X, budget = generer(paq, echantillon, (idx_items, banque), n_appels_max=n_appels_max)
        print(f"\ncout total mesure : {budget.cumul} USD sur {budget.n_appels} appels "
              "reussis", flush=True)
    else:
        X = relire_codes_depuis_trace(len(echantillon), len(banque))

    if args.essai:
        print("run pilote (--essai) : mesure non ecrite dans les fichiers finaux.",
              flush=True)
        for nom in ("M", "G", "P"):
            n_ok = int((X[nom] >= 0).any(axis=1).sum())
            print(f"personnes avec au moins une reponse lue, {nom} : {n_ok}", flush=True)
        return

    lignes = {nom: mesurer_condition(nom, paq, echantillon, XB, X[nom])
              for nom in ("M", "G", "P")}
    n_reference = len(echantillon)
    ligne_demo = mesurer_demo(paq, echantillon, idx_items, n_reference)

    df = pd.DataFrame([lignes["M"], lignes["G"], lignes["P"], ligne_demo])
    chemin_csv = os.path.join(SORTIE, "c7-factoriel.csv")
    df.to_csv(chemin_csv, index=False)
    print(f"ecrit {chemin_csv}", flush=True)

    v = verdict(lignes, ligne_demo["top1"])
    print("\n--- VERDICT ---")
    print(json.dumps(v, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
