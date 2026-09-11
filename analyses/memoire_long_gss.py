"""
memoire_long_gss : la persistance ("elle repondra comme la derniere fois") contre le
jumeau IA, a des horizons ou les gens changent vraiment : deux et quatre ans, sur le
panel GSS de NORC (data/gss-panel), et non les deux semaines de Twin-2K-500 mesurees
dans resultats/memoire-resultats.md.

Statut : script d'experience, pas du code de production. Protocole fixe AVANT le premier
appel dans resultats/memoire-long-preenregistrement.md.

Ce qu'il fait. Pour environ 400 personnes des panels a trois vagues (2006-2010,
2008-2012, 2010-2014), il construit un profil a partir de la vague 1 SEULE (11 attributs
demographiques + reponses aux items autres que les 20 cibles), puis demande au modele
local, pour chacun des 20 items cibles et chacun des deux horizons (+2 ans, +4 ans), la
lettre de la reponse que cette personne donnerait. Un seul appel par (personne, item,
horizon) ; le profil ne change pas entre les deux horizons, ce qui maximise la reutilisation
du cache de prefixe de llama.cpp (systeme identique pour les 40 appels d'une personne).

Le client HTTP et le parse sont ceux de analyses/r1_oracle_camps.py (MoteurR1, gabarit(),
ARRETS, registre MODELES), adaptes ici a une reponse d'une seule lettre plutot qu'une
distribution en pourcentages.

Selection des 20 items cibles : sur METADONNEES SEULES (famille thematique de FAMILLES,
ordre alphabetique, presence des colonnes Stata aux trois vagues dans les trois panels),
AVANT tout calcul de changement humain. Voir choisir_items().

Vie privee : le GSS est une enquete publique, aucune identite n'est stockee. La trace ne
contient PAS la vraie reponse de la personne (vague 1, 2 ou 3) : seule la reponse du
modele y figure, comme en a5. L'evaluation (analyses/memoire_long_analyse.py) relit le
panel separement pour noter.

Entree  : data/gss-panel/*.dta, non versionne (voir data/gss-panel/PROVENANCE.md).
          data/osf-t6g7k-stanford/figure2/data/question_master/gss/main.csv, pour le
          libelle des questions et l'ordre officiel des modalites (nomenclature() de a5).
          data/modeles/gguf/*.gguf, non versionne.
Sortie  : data/traces/memoire-long/ml-<cle modele>.jsonl, une ligne par appel.
          data/traces/memoire-long/ml-echantillon.csv, les personnes retenues.
          data/traces/memoire-long/ml-items.csv, les 20 items cibles et leur famille.
          data/traces/memoire-long/ml-resume.json.
          data/traces/memoire-long/ml-run.log recoit "RUN TERMINE" a la fin, quoi qu'il
          arrive.

Arret : `touch data/traces/memoire-long/STOP` arrete le run entre deux appels, trace
fermee, resume ecrit, code de sortie 0. Le fichier n'est pas efface par le script.

Usage :
  .venv/bin/python analyses/memoire_long_gss.py --modele oss20 --fin 08:00
  .venv/bin/python analyses/memoire_long_gss.py --modele oss20 --personnes 3 --items 2 \\
      --suffixe smoke --limite 10

Reprise : l'index unique est (version_prompt, panel, ligne, item, horizon). Une relance ne
refait aucun appel deja ecrit dans la trace du modele.
"""

import argparse
import collections
import datetime
import json
import os
import re
import sys
import time

import numpy as np
import pandas as pd
import pyreadstat

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_baselines_gss import FAMILLES
from a5_agents_locaux_gss import (LETTRES, canoniser, heure_de_fin, nomenclature,
                                  port_libre, premier_port_libre)
from a12_retest_delai import PANELS as PANELS_A12
from a12_retest_delai import colonnes_vague, items_stanford, noms_gss
from r1_oracle_camps import ARRETS, MODELES, MoteurR1, gabarit

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PANEL_DIR = os.path.join(RACINE, "data", "gss-panel")
TRACES = os.path.join(RACINE, "data/traces/memoire-long")
GGUF = os.path.join(RACINE, "data/modeles/gguf")
JOURNAL_RUN = os.path.join(TRACES, "ml-run.log")
FICHIER_ARRET = os.path.join(TRACES, "STOP")

VERSION_PROMPT = "ml-d1"

# Les trois panels a trois vagues sur les memes personnes, ecart de 2 ans entre vagues.
# Le panel 2016-2020 est exclu : ses deux cohortes (2016 et 2018) ne partagent aucune
# personne, voir le commentaire de a12_retest_delai.PANELS.
PANELS = {k: v for k, v in PANELS_A12.items() if k != "2016-2020"}

# 11 attributs demographiques de la vague 1, cle Stata (sans suffixe de vague) et libelle
# lisible. Choisis pour couvrir les memes dimensions que ETIQUETTES_DEMOGRAPHIQUES de a5,
# adaptees aux variables reellement presentes dans les panels GSS (verifie par lecture des
# metadonnees Stata, cf. resultats/memoire-long-preenregistrement.md).
DEMOGRAPHIES = [
    ("age", "Age"), ("sex", "Sex"), ("race", "Race"),
    ("degree", "Highest educational degree"), ("region", "Census region"),
    ("income06", "Household income"), ("partyid", "Political party affiliation"),
    ("polviews", "Political ideology"), ("marital", "Marital status"),
    ("relig", "Religious preference"), ("wrkstat", "Labor force status"),
]

# Valeurs de Stata considerees comme non renseignees une fois les libelles de valeur
# appliques (apply_value_formats=True) : ce sont les manquants etendus (.d, .i, .n, .r).
MANQUANT_PANEL = {"dk", "iap", "na", "nap", "not applicable", "don't know", "no answer",
                  "refused", ""}

MIN_ITEMS_CONTEXTE = 60   # une personne compte si au moins 60 items de contexte sont vus
MIN_ITEMS_CIBLES = 10     # et au moins 10 des 20 items cibles, aux trois vagues
N_PERSONNES = 400
N_PAR_FAMILLE = 4         # au plus 4 items cibles par famille thematique
N_ITEMS_CIBLES = 20
GRAINE_ECHANTILLON = 20260911

N_PREDICT = 8             # une lettre, tres peu de tokens necessaires
SOMME_HORIZONS = (2, 4)   # annees ecoulees depuis la vague 1


def arret_demande():
    return os.path.exists(FICHIER_ARRET)


def journaliser(message):
    os.makedirs(TRACES, exist_ok=True)
    with open(JOURNAL_RUN, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


def est_manquant_panel(v):
    if v is None:
        return True
    if isinstance(v, float) and np.isnan(v):
        return True
    return str(v).strip().lower() in MANQUANT_PANEL


# --------------------------------------------------------------------------------------
# 1. Metadonnees des panels : colonnes disponibles par item et par vague, sans lire les
#    donnees. Sert a choisir les 20 items cibles avant tout calcul de changement.
# --------------------------------------------------------------------------------------

def colonnes_panel(nom_panel):
    """Colonnes d'un fichier Stata, sans lire les donnees : un seul appel metadataonly
    par panel. Rend {nom en minuscules -> nom original}, meme convention que
    a12_retest_delai.charger_panel : la casse du fichier Stata n'est pas garantie."""
    _, meta = pyreadstat.read_dta(os.path.join(PANEL_DIR, PANELS[nom_panel]["fichier"]),
                                  metadataonly=True, encoding="latin1")
    return {c.lower(): c for c in meta.column_names}


def item_disponible_partout(item, colonnes_par_panel):
    """Vrai si l'item a au moins une colonne Stata a CHAQUE vague de CHAQUE panel."""
    for nom_panel, cfg in PANELS.items():
        colonnes = colonnes_par_panel[nom_panel]
        for suf in cfg["vagues"].values():
            if not colonnes_vague(item, suf, colonnes):
                return False
    return True


def choisir_items(items, colonnes_par_panel):
    """Les 20 items cibles, sur metadonnees seules : famille thematique, ordre
    alphabetique, disponibilite Stata aux trois vagues des trois panels. Fixe AVANT tout
    calcul de changement humain (resultats/memoire-long-preenregistrement.md).
    """
    eligibles = sorted(it for it in items if item_disponible_partout(it, colonnes_par_panel))
    par_famille = {it: nom for nom, membres in FAMILLES.items() for it in membres}

    retenus = []
    for nom_famille in FAMILLES:
        membres = sorted(it for it in eligibles if par_famille.get(it) == nom_famille)
        retenus += membres[:N_PAR_FAMILLE]
        if len(retenus) >= N_ITEMS_CIBLES:
            break
    if len(retenus) < N_ITEMS_CIBLES:
        hors_famille = sorted(it for it in eligibles if it not in par_famille
                              and it not in retenus)
        retenus += hors_famille[:N_ITEMS_CIBLES - len(retenus)]
    retenus = retenus[:N_ITEMS_CIBLES]
    return retenus, {it: par_famille.get(it, "hors famille") for it in retenus}


# --------------------------------------------------------------------------------------
# 2. Chargement des panels avec libelles de valeur appliques (pour des prompts lisibles)
# --------------------------------------------------------------------------------------

def charger_panel_libelle(nom_panel, items_contexte, items_cibles):
    """Charge un panel, libelles de valeur appliques, pour les items de contexte, les
    items cibles et les attributs demographiques, aux trois vagues.

    Retourne un DataFrame index par la ligne d'origine (colonne 'ligne'), avec une colonne
    par (variable, annee) sous la forme "var@annee", deja passee par est_manquant_panel
    (None si non renseignee).
    """
    cfg = PANELS[nom_panel]
    colonnes = colonnes_panel(nom_panel)
    besoin, plan_ctx, plan_cible, plan_demo = set(), {}, {}, {}
    for annee, suf in cfg["vagues"].items():
        plan_ctx[annee] = {}
        for it in items_contexte:
            cols = colonnes_vague(it, suf, colonnes)
            if cols:
                plan_ctx[annee][it] = cols
                besoin.update(colonnes[c] for c in cols)
        plan_cible[annee] = {}
        for it in items_cibles:
            cols = colonnes_vague(it, suf, colonnes)
            if cols:
                plan_cible[annee][it] = cols
                besoin.update(colonnes[c] for c in cols)
        plan_demo[annee] = {}
        for var, _ in DEMOGRAPHIES:
            col = var + suf
            if col in colonnes:
                plan_demo[annee][var] = col
                besoin.add(colonnes[col])

    df, meta = pyreadstat.read_dta(
        os.path.join(PANEL_DIR, cfg["fichier"]), usecols=sorted(besoin),
        encoding="latin1", apply_value_formats=True, formats_as_category=True)
    df.columns = [c.lower() for c in df.columns]

    # Fusion des versions de ballot colonne par colonne (premiere version renseignee),
    # vectorisee avec pandas : une boucle iterrows() serait trop lente sur ~5000 lignes
    # x 150 items. Les colonnes sont assemblees dans un dict puis passees a pd.DataFrame
    # une seule fois : les assigner une a une sur un DataFrame deja construit fragmente
    # son bloc interne et ralentit chaque assignation suivante.
    colonnes_out = {"ligne": df.index.values}
    for annee in cfg["vagues"]:
        for it, cols in plan_ctx[annee].items():
            colonnes_out[f"ctx::{it}@{annee}"] = fusion_colonnes(df, cols)
        for it, cols in plan_cible[annee].items():
            colonnes_out[f"cible::{it}@{annee}"] = fusion_colonnes(df, cols)
        for var, col in plan_demo[annee].items():
            colonnes_out[f"demo::{var}@{annee}"] = df[col].astype(object).where(
                df[col].notna(), None)
    resultat = pd.DataFrame(colonnes_out)
    return resultat, plan_ctx, plan_cible, plan_demo


def fusion_colonnes(df, cols):
    """Premiere colonne renseignee parmi plusieurs versions de ballot, valeurs deja
    passees par les libelles Stata. Rend une Series d'objets Python (str ou None)."""
    out = pd.Series([None] * len(df), index=df.index, dtype=object)
    for c in cols:
        col = df[c].astype(object)
        manquant_out = out.isna()
        candidat = col.where(col.notna(), None)
        candidat_ok = candidat.apply(lambda v: not est_manquant_panel(v))
        out = out.where(~(manquant_out & candidat_ok), candidat)
    return out


# --------------------------------------------------------------------------------------
# 3. Echantillon de personnes
# --------------------------------------------------------------------------------------

def echantillonner(nom_panel, table, items_contexte, items_cibles, n_cible, rng):
    """Personnes eligibles : au moins MIN_ITEMS_CONTEXTE items de contexte et
    MIN_ITEMS_CIBLES items cibles renseignes aux TROIS vagues. Tire n_cible parmi elles.
    """
    annees = sorted(PANELS[nom_panel]["vagues"])

    def compte_present_3_vagues(prefixe, items):
        ok = pd.Series(0, index=table.index)
        for it in items:
            present = pd.Series(True, index=table.index)
            for a in annees:
                col = f"{prefixe}::{it}@{a}"
                if col not in table.columns:
                    present = pd.Series(False, index=table.index)
                    break
                present &= table[col].notna()
            ok += present.astype(int)
        return ok

    n_ctx = compte_present_3_vagues("ctx", items_contexte)
    n_cib = compte_present_3_vagues("cible", items_cibles)
    eligible = table[(n_ctx >= MIN_ITEMS_CONTEXTE) & (n_cib >= MIN_ITEMS_CIBLES)]
    n = min(n_cible, len(eligible))
    if n == 0:
        return eligible.iloc[0:0]
    idx = rng.choice(eligible.index.values, size=n, replace=False)
    return eligible.loc[sorted(idx)]


# --------------------------------------------------------------------------------------
# 4. Construction des invites
# --------------------------------------------------------------------------------------

PREAMBULE = ("You are simulating one specific real person who took part in a long-running "
             "survey (the General Social Survey). Answer exactly as this person would "
             "answer, not as you would.")


def systeme_profil(ligne, items_contexte, table, annee1):
    """Profil fixe de la personne : demographies + reponses de la vague 1 aux items de
    contexte. Ne depend PAS de l'horizon : c'est ce qui permet au cache de prefixe de
    llama.cpp de servir les 40 appels d'une personne sur un seul calcul de prefixe.
    """
    demo_lignes = []
    for var, libelle in DEMOGRAPHIES:
        v = ligne.get(f"demo::{var}@{annee1}")
        demo_lignes.append(f"- {libelle}: {v if v else 'not reported'}")

    ctx_lignes = []
    for it in items_contexte:
        v = ligne.get(f"ctx::{it}@{annee1}")
        if v is None:
            continue
        rep = canoniser(it, v, table)
        if rep is None:
            rep = v
        ctx_lignes.append(f"Q: {table[it]['question']}\nA: {rep}")

    return (PREAMBULE + "\n\nDemographics of this person, as recorded then:\n"
            + "\n".join(demo_lignes)
            + "\n\nHow this person answered other questions of the same survey wave:\n\n"
            + "\n\n".join(ctx_lignes))


def utilisateur(nom, table, horizon_ans, annee_cible):
    """Bloc utilisateur : l'horizon, la question cible, ses modalites, et le format.

    L'horizon est ici, pas dans le profil systeme : le profil (vague 1 seule) reste
    identique pour les deux horizons de la meme personne, seul ce bloc change.
    """
    options = list(table[nom]["options"])
    k = len(options)
    lettres = LETTRES[:k]
    lignes = [
        f"It is now approximately {horizon_ans} years later ({annee_cible}). This same "
        "person is answering a new wave of the same survey. People's views can shift over "
        "years even when their demographics stay similar ; answer as you believe this "
        "specific person would answer NOW, not as they answered before.",
        "",
        f'Survey question, General Social Survey wording: "{table[nom]["question"]}"',
        "", "Answer options:",
    ]
    for lettre, o in zip(lettres, options):
        lignes.append(f"{lettre}. {o}")
    lignes += [
        "",
        "Reply with exactly one line: the single capital letter of your answer, nothing "
        "else. No explanation, no percentage, no repeated letter.",
    ]
    return "\n".join(lignes), options


# --------------------------------------------------------------------------------------
# 5. Le parse, strict : une seule lettre
# --------------------------------------------------------------------------------------

LIGNE_LETTRE = re.compile(r"^\s*\**\s*\(?([A-M])\)?\s*[\.\):\-]?\s*\**\.?\s*$")


def parser_lettre(texte, options):
    """Lit une seule lettre dans le texte produit. Rend (modalite, lettre, motif).

    Regles, fixees avant le premier appel : on ne garde que les lignes non vides qui
    correspondent EXACTEMENT au format demande ; il en faut exactement une, dans la
    nomenclature de l'item. Toute autre sortie est un rejet, motif ecrit dans la trace.
    """
    k = len(options)
    lettres_valides = set(LETTRES[:k])
    vues = []
    for ligne in texte.splitlines():
        ligne = ligne.strip()
        if not ligne:
            continue
        m = LIGNE_LETTRE.match(ligne)
        if m:
            vues.append(m.group(1))
    if not vues:
        return None, None, "aucune ligne au format demande"
    lettre = vues[0]
    if len(set(vues)) > 1:
        return None, None, f"lettres differentes selon la ligne : {sorted(set(vues))}"
    if lettre not in lettres_valides:
        return None, None, f"lettre {lettre} hors nomenclature ({k} modalites)"
    return options[LETTRES.index(lettre)], lettre, ""


# --------------------------------------------------------------------------------------
# 6. Trace et reprise
# --------------------------------------------------------------------------------------

def chemin_trace(cle, suffixe):
    nom = f"ml-{cle}" + (("-" + suffixe) if suffixe else "")
    return os.path.join(TRACES, nom + ".jsonl")


def index_existant(chemin):
    fait = set()
    if not os.path.exists(chemin):
        return fait
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            fait.add((d["version_prompt"], d["panel"], d["ligne"], d["item"], d["horizon_ans"]))
    return fait


# --------------------------------------------------------------------------------------
# 7. Le run
# --------------------------------------------------------------------------------------

def cellules_personne(items_cibles):
    for it in items_cibles:
        for h in SOMME_HORIZONS:
            yield it, h


def lancer(moteur, cle, info, personnes_par_panel, items_contexte, items_cibles, familles,
           table, fin_ts, suffixe, limite=None, journal_tous=50):
    chemin = chemin_trace(cle, suffixe)
    fait = index_existant(chemin)
    print(f"[{cle}] trace {chemin}, {len(fait)} appels deja faits", flush=True)

    arrets = ARRETS[info["gabarit"]]
    n_appels = n_rejets = 0
    motifs = collections.Counter()
    arret = False
    t0 = time.time()

    with open(chemin, "a", encoding="utf-8") as fh:
        for nom_panel, (table_p, annees) in personnes_par_panel.items():
            annee1 = annees[0]
            for _, ligne in table_p.iterrows():
                sys_txt = None  # calcule au premier item non deja fait, une fois
                for it, h in cellules_personne(items_cibles):
                    cle_idx = (VERSION_PROMPT, nom_panel, int(ligne["ligne"]), it, h)
                    if cle_idx in fait:
                        continue
                    if arret_demande():
                        arret = True
                        message = f"[{cle}] ARRET DEMANDE ({FICHIER_ARRET}), arret propre"
                        print(message, flush=True)
                        journaliser("ARRET DEMANDE " + message)
                        break
                    if time.time() >= fin_ts:
                        print(f"[{cle}] fin dure atteinte, arret propre", flush=True)
                        arret = "fin_dure"
                        break
                    if limite is not None and n_appels >= limite:
                        arret = "limite"
                        break

                    if sys_txt is None:
                        sys_txt = systeme_profil(ligne, items_contexte, table, annee1)
                    annee_cible = annee1 + h
                    usr_txt, options = utilisateur(it, table, h, annee_cible)
                    prompt = gabarit(info["gabarit"], sys_txt, usr_txt)
                    r = moteur.decrire(prompt, N_PREDICT, arrets)
                    reponse, lettre, motif = parser_lettre(r["texte"], options)
                    rejet = reponse is None
                    if rejet:
                        n_rejets += 1
                        motifs[motif[:40]] += 1

                    fh.write(json.dumps({
                        "version_prompt": VERSION_PROMPT, "cle_modele": cle,
                        "modele": info["nom"], "quantification": info["quantification"],
                        "panel": nom_panel, "ligne": int(ligne["ligne"]), "item": it,
                        "famille": familles.get(it, "hors famille"),
                        "horizon_ans": h, "annee_baseline": annee1,
                        "annee_cible": annee_cible, "n_modalites": len(options),
                        "rejet": rejet, "motif_rejet": motif,
                        "sortie_brute": r["texte"], "reponse_modele": reponse,
                        "lettre": lettre, "duree_ms": round(r["duree_ms"], 2),
                        "tokens_generes": r["tokens_generes"],
                        "tokens_prompt": r["tokens_prompt"],
                    }, ensure_ascii=False) + "\n")
                    fh.flush()
                    n_appels += 1
                    if n_appels % journal_tous == 0:
                        ecoule = max(time.time() - t0, 1e-9)
                        debit = n_appels / ecoule * 3600
                        os.fsync(fh.fileno())
                        message = (f"[{cle}] {n_appels} cellules, {debit:,.0f}/h, "
                                   f"rejets {n_rejets}, {nom_panel}").replace(",", " ")
                        print(message, flush=True)
                        journaliser(message)
                if arret:
                    break
            if arret:
                break
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    return {
        "cle_modele": cle, "modele": info["nom"], "cellules": n_appels,
        "deja_faites": len(fait), "secondes": round(ecoule, 1),
        "cellules_par_heure": round(n_appels / ecoule * 3600, 1) if n_appels else 0.0,
        "rejets": n_rejets,
        "taux_rejet": round(n_rejets / n_appels, 4) if n_appels else 0.0,
        "arret_demande": arret if isinstance(arret, str) else bool(arret),
        "motifs_de_rejet": dict(motifs), "trace": chemin,
    }


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="oss20", help="cle du registre MODELES (r1)")
    ap.add_argument("--personnes", type=int, default=N_PERSONNES)
    ap.add_argument("--items", type=int, default=0,
                    help="0 pour les 20 items choisis, n pour les n premiers (smoke test)")
    ap.add_argument("--fin", default="10:00", help="fin dure du calcul, heure locale")
    ap.add_argument("--suffixe", default="", help="suffixe de fichier, pour un smoke test")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal de cellules au total, pour un smoke test")
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--contexte", type=int, default=8192, help="tokens par slot")
    ap.add_argument("--parallele", type=int, default=1)
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    if args.modele not in MODELES:
        sys.exit(f"modele inconnu : {args.modele}. Cles connues : {', '.join(MODELES)}")
    info = MODELES[args.modele]
    chemin_modele = os.path.join(GGUF, info["fichier"])
    if not os.path.exists(chemin_modele):
        sys.exit(f"modele introuvable : {chemin_modele}")

    depart = datetime.datetime.now()
    fin_ts, fin_dt = heure_de_fin(args.fin)
    print(f"popsim memoire_long_gss. Depart {depart:%Y-%m-%d %H:%M:%S}, fin dure "
          f"{fin_dt:%Y-%m-%d %H:%M} ({(fin_ts - time.time()) / 3600:.2f} h). "
          f"Modele : {args.modele}", flush=True)
    journaliser(f"DEBUT modele={args.modele} fin={fin_dt.isoformat()}")

    table = nomenclature()
    tous_items = items_stanford()
    print(f"{len(tous_items)} items GSS disponibles (liste Stanford, hors demographies "
          "qui fuiraient le profil)", flush=True)

    print("lecture des metadonnees Stata des trois panels...", flush=True)
    colonnes_par_panel = {nom: colonnes_panel(nom) for nom in PANELS}
    items_cibles, familles = choisir_items(tous_items, colonnes_par_panel)
    if args.items:
        items_cibles = items_cibles[:args.items]
    items_contexte = [it for it in tous_items if it not in items_cibles]
    print(f"{len(items_cibles)} items cibles : {items_cibles}", flush=True)
    print(f"{len(items_contexte)} items de contexte (vague 1 seule)", flush=True)

    if not args.suffixe:
        pd.DataFrame([{"item": it, "famille": familles.get(it, "hors famille")}
                     for it in items_cibles]).to_csv(
            os.path.join(TRACES, "ml-items.csv"), index=False)

    rng = np.random.default_rng(GRAINE_ECHANTILLON)
    n_par_panel = max(1, args.personnes // len(PANELS))
    personnes_par_panel = {}
    lignes_echantillon = []
    for nom_panel in PANELS:
        print(f"chargement de {nom_panel}...", flush=True)
        table_p, plan_ctx, plan_cible, plan_demo = charger_panel_libelle(
            nom_panel, items_contexte, items_cibles)
        retenus = echantillonner(nom_panel, table_p, items_contexte, items_cibles,
                                  n_par_panel, rng)
        annees = sorted(PANELS[nom_panel]["vagues"])
        personnes_par_panel[nom_panel] = (retenus, annees)
        for l in retenus["ligne"].tolist():
            lignes_echantillon.append({"panel": nom_panel, "ligne": int(l)})
        print(f"  {len(retenus)} personnes retenues sur {len(table_p)}", flush=True)

    if not args.suffixe:
        pd.DataFrame(lignes_echantillon).to_csv(
            os.path.join(TRACES, "ml-echantillon.csv"), index=False)

    total_personnes = sum(len(t) for t, _ in personnes_par_panel.values())
    n_cellules = total_personnes * len(items_cibles) * len(SOMME_HORIZONS)
    print(f"{total_personnes} personnes, {n_cellules} appels prevus pour {args.modele}",
          flush=True)

    port = args.port or premier_port_libre()
    if not port_libre(port):
        sys.exit(f"le port {port} est occupe, un llama-server tourne peut etre deja")
    print(f"[{args.modele}] {info['nom']} {info['quantification']}, port {port}, "
          f"-np {args.parallele}, -c {args.contexte * args.parallele}, KV q8_0", flush=True)
    journaliser(f"lancement du serveur pour {args.modele} sur le port {port}")

    moteur = MoteurR1(chemin_modele, contexte=args.contexte, parallele=args.parallele,
                      port=port, cache_kv_8bits=True)
    moteur.demarrer()
    print(f"serveur pret en {moteur.chargement_s:.1f} s", flush=True)

    resume = None
    try:
        resume = lancer(moteur, args.modele, info, personnes_par_panel, items_contexte,
                        items_cibles, familles, table, fin_ts, args.suffixe,
                        limite=args.limite)
        resume["port"] = port
        resume["chargement_s"] = round(moteur.chargement_s, 1)
        print(f"[{args.modele}] {resume['cellules']} cellules en "
              f"{resume['secondes'] / 60:.1f} min, {resume['cellules_par_heure']:,.0f}/h, "
              f"{resume['rejets']} rejets, taux {resume['taux_rejet']:.4f}"
              .replace(",", " "), flush=True)
        journaliser(f"[{args.modele}] termine : {resume['cellules']} cellules, "
                    f"taux de rejet {resume['taux_rejet']:.4f}")
    finally:
        moteur.arreter()
        print(f"serveur arrete. charge machine : {os.getloadavg()}", flush=True)
        chemin_resume = os.path.join(
            TRACES, f"ml-resume{'-' + args.suffixe if args.suffixe else ''}.json")
        with open(chemin_resume, "w", encoding="utf-8") as fh:
            json.dump({
                "depart": depart.isoformat(), "fin": datetime.datetime.now().isoformat(),
                "fin_dure": fin_dt.isoformat(), "version_prompt": VERSION_PROMPT,
                "modele": args.modele, "personnes": total_personnes,
                "items_cibles": items_cibles, "familles": familles,
                "horizons": list(SOMME_HORIZONS), "resultat": resume,
            }, fh, indent=2, ensure_ascii=False)
        print(f"resume ecrit : {chemin_resume}", flush=True)
        fin_message = (f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S} "
                       f"({resume['cellules'] if resume else 0} cellules)")
        print(fin_message, flush=True)
        journaliser(fin_message)


if __name__ == "__main__":
    main()
