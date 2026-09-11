"""
c5_formulation : onze paires de formulation du GSS, jouees sur 300 personas locaux.

Statut : script d'experience, pas du code de production. Il joue le protocole de
`resultats/c5-preenregistrement.md`, ecrit AVANT le premier appel de modele.

Ce qu'il fait. Le GSS a onze paires d'items en split ballot (`nat*` contre `nat*y`) sur les
depenses publiques : meme question cadre, un seul mot de l'item change ("welfare" contre
"assistance to the poor", etc.). Chez les humains cinq paires sont nulles et six ne le sont
pas (section 1 du preenregistrement, verifie sur `GSS_panel2010w123_R6 - stata.dta`, vague
1). Pour chacun de 300 personas tires de cette meme vague (demographie et camp seulement,
aucune reponse de sondage en contexte), le modele lit chacune des 22 formes et rend une
distribution de probabilite sur les trois modalites ("too little", "about right",
"too much"). L'effet de formulation simule d'une paire est la moyenne sur les 300 personas
de "too much" a la forme historique moins la forme Y ; il se compare point par point a
l'effet humain de la meme paire.

Reutilisation deliberee de `r1_oracle_camps.py` : le registre `MODELES`, le rendu de
gabarit par famille (`gabarit`), les sequences d'arret (`ARRETS`), le parse strict
lettre + pourcentage (`parser`, regex `LIGNE_VALIDE`, tolerance de somme 95-105) et le
client HTTP (`MoteurR1.decrire`) sont importes tels quels, jamais recopies. Seules les
invites (persona au lieu de camp) et les items (les 22 formes nat* au lieu des 149 items
Stanford) sont nouveaux.

Difference avec R1 : R1 demande une distribution de GROUPE ("100 adultes conservateurs").
Ici la meme grammaire de sortie est appliquee a UNE personne : le modele dit la probabilite
que CETTE personne donne chaque reponse. Les deux quantites ne sont commensurables qu'a
travers la moyenne sur 300 personas, jamais cellule a cellule.

Entree  : data/gss-panel/GSS_panel2010w123_R6 - stata.dta, vague 1 (colonnes *_1).
          data/modeles/gguf/*.gguf, non versionne.
Sortie  : data/traces/c5/c5-<cle modele>.jsonl, une ligne par appel.
          data/traces/c5/c5-personas.csv, les 300 personas retenus (et les 20 de test avec
          suffixe smoke), ecrits avant tout appel.
          data/traces/c5/c5-effet-humain.csv, l'effet humain des onze paires (section 1
          du preenregistrement, recalcule ici a l'identique pour que le rapport ne
          dependee que d'un seul calcul).
          data/traces/c5/c5-resume.json, data/traces/c5/c5-run.log (marqueur RUN TERMINE).

Rien ne sort de la machine. Aucun appel distant.

Arret : `touch data/traces/c5/STOP` arrete le run entre deux appels, trace fermee, resume
ecrit, code de sortie 0. Dedie a C5, distinct du fichier d'arret partage
`data/traces/STOP` des autres runs.

Usage :
  .venv/bin/python analyses/c5_formulation.py --modele oss20 --test --fin 23:59
  .venv/bin/python analyses/c5_formulation.py --modele oss20,q30 --fin 07:30
"""

import argparse
import datetime
import json
import os
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a5_agents_locaux_gss import heure_de_fin, port_libre, premier_port_libre
from r1_oracle_camps import ARRETS, CAMP_EN, MODELES, MoteurR1, gabarit, parser

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GGUF = os.path.join(RACINE, "data/modeles/gguf")
PANEL = os.path.join(RACINE, "data/gss-panel/GSS_panel2010w123_R6 - stata.dta")
TRACES = os.path.join(RACINE, "data/traces/c5")

FICHIER_ARRET = os.path.join(TRACES, "STOP")
JOURNAL_RUN = os.path.join(TRACES, "c5-run.log")

VERSION_PROMPT = "c5-p1"
LETTRES = "ABC"
OPTIONS = ["too little", "about right", "too much"]
N_PREDICT = 150

GRAINE_PERSONAS = 20260911
GRAINE_TEST = 20260912

# --------------------------------------------------------------------------------------
# 1. Les onze paires : nom de variable GSS et libelle d'item, forme historique et forme Y.
#    Libelles recopies de la nomenclature officielle du GSS (Rasinski 1989, Smith 1987) ;
#    seul l'item change entre les deux formes, la question cadre est identique.
# --------------------------------------------------------------------------------------

PREAMBULE_QUESTION = (
    "We are faced with many problems in this country, none of which can be solved "
    "easily or inexpensively. I'm going to name some of these problems, and for each "
    "one I'd like you to tell me whether you think we're spending too much money on "
    "it, too little money, or about the right amount."
)

# paire -> {"hist": (variable, libelle), "y": (variable, libelle)}
PAIRES = {
    "natspac": {"hist": ("natspac", "space exploration program"),
                "y": ("natspacy", "space exploration")},
    "natenvir": {"hist": ("natenvir", "improving and protecting the environment"),
                 "y": ("natenviy", "the environment")},
    "natheal": {"hist": ("natheal", "improving and protecting the nation's health"),
                "y": ("nathealy", "health")},
    "natcity": {"hist": ("natcity", "solving the problems of the big cities"),
                "y": ("natcityy", "assistance to big cities")},
    "natdrug": {"hist": ("natdrug", "dealing with drug addiction"),
                "y": ("natdrugy", "drug rehabilitation")},
    "nateduc": {"hist": ("nateduc", "improving the nation's education system"),
                "y": ("nateducy", "education")},
    "natrace": {"hist": ("natrace", "improving the conditions of Blacks"),
                "y": ("natracey", "assistance to Blacks")},
    "natarms": {"hist": ("natarms", "the military, armaments, and defense"),
                "y": ("natarmsy", "national defense")},
    "nataid": {"hist": ("nataid", "foreign aid"),
               "y": ("nataidy", "assistance to other countries")},
    "natfare": {"hist": ("natfare", "welfare"),
                "y": ("natfarey", "assistance to the poor")},
    "natcrime": {"hist": ("natcrime", "halting the rising crime rate"),
                 "y": ("natcrimy", "law enforcement")},
}

# Les cinq paires nulles chez les humains, section 1 du preenregistrement.
PAIRES_NULLES = ["natspac", "natenvir", "natdrug", "nateduc", "natarms"]


def formes():
    """Les 22 formes a jouer, (paire, version, variable GSS, libelle)."""
    sortie = []
    for paire, d in PAIRES.items():
        for version in ("hist", "y"):
            var, libelle = d[version]
            sortie.append((paire, version, var, libelle))
    return sortie


# --------------------------------------------------------------------------------------
# 2. Effet humain, vague 1, recalcule a l'identique de la section 1 du preenregistrement.
# --------------------------------------------------------------------------------------

def effet_humain_wave1(chemin=PANEL):
    """Effet de formulation humain par paire : % 'too much' forme historique moins Y.

    Code GSS : 1 too little, 2 about right, 3 too much. IC95 sur une difference de deux
    proportions independantes (les deux formes sont assignees a des personnes distinctes).
    """
    df = pd.read_stata(chemin, convert_categoricals=False)
    lignes = []
    for paire, d in PAIRES.items():
        va, _ = d["hist"]
        vb, _ = d["y"]
        ca = df[f"{va}_1"]
        cb = df[f"{vb}_1"]
        na, nb = int(ca.notna().sum()), int(cb.notna().sum())
        pa = float((ca == 3).sum()) / na * 100.0
        pb = float((cb == 3).sum()) / nb * 100.0
        effet = pa - pb
        se = np.sqrt(pa * (100 - pa) / na + pb * (100 - pb) / nb)
        ic95 = 1.96 * se
        lignes.append({"paire": paire, "pct_too_much_hist": round(pa, 2), "n_hist": na,
                        "pct_too_much_y": round(pb, 2), "n_y": nb,
                        "effet_humain": round(effet, 2), "ic95": round(ic95, 2),
                        "nul": paire in PAIRES_NULLES})
    return pd.DataFrame(lignes)


# --------------------------------------------------------------------------------------
# 3. Personas : demographie et camp, vague 1, aucune reponse de sondage en contexte.
# --------------------------------------------------------------------------------------

COLONNES_PERSONA = ["id", "age", "sex", "race", "region", "educ", "marital", "relig",
                    "partyid", "polviews", "income06"]

ETIQUETTES = {"age": "Age", "sex": "Sex", "race": "Race", "region": "Census region",
              "educ": "Years of education", "marital": "Marital status",
              "relig": "Religious preference", "partyid": "Party identification",
              "polviews": "Political views", "income06": "Household income"}


def camp_de_polviews(pv):
    if pv != pv or pv is None:
        return None
    if pv <= 3:
        return "gauche"
    if pv == 4:
        return "centre"
    return "droite"


def charger_personas(n_par_camp, graine, exclure=(), chemin=PANEL):
    """Tire un sous echantillon stratifie sur le camp derive de `polviews`, vague 1.

    `exclure` retire des identifiants deja tires ailleurs : c'est ce qui garantit que les
    20 personas du test ne recoupent jamais les 300 du run complet (regle de l'etape 3
    de la reprise du 10 septembre : les personas de test sont exclues de l'analyse).
    """
    cols = [f"{c}_1" for c in COLONNES_PERSONA]
    # `columns=` restreint la lecture a ces variables : le fichier contient au moins une
    # colonne hors de cette liste (hhtype_1) dont les libelles de valeur ne sont pas
    # uniques, ce qui casse `convert_categoricals=True` sur le fichier entier.
    sous_brut = pd.read_stata(chemin, convert_categoricals=False, columns=cols)
    sous_lisible = pd.read_stata(chemin, convert_categoricals=True, columns=cols)
    camp = sous_brut["polviews_1"].apply(camp_de_polviews)
    complet = sous_brut.notna().all(axis=1) & camp.notna()
    complet &= ~sous_brut["id_1"].isin(set(exclure))

    rng = np.random.default_rng(graine)
    personas = []
    for c in ("gauche", "centre", "droite"):
        idx = sous_brut.index[complet & (camp == c)]
        n = min(n_par_camp, len(idx))
        tires = sorted(rng.choice(idx, size=n, replace=False))
        for i in tires:
            p = {"pid": int(sous_brut.loc[i, "id_1"]), "camp": c}
            for colonne in COLONNES_PERSONA[1:]:
                if colonne in ("age", "educ"):
                    p[colonne] = int(sous_brut.loc[i, f"{colonne}_1"])
                else:
                    # Stata melange majuscules et minuscules selon le libelle de valeur
                    # d'origine (ex. "widowed" mais "STRONG DEMOCRAT") ; .title() uniformise
                    # sans changer le sens, pour ne pas laisser la casse trahir au modele
                    # quelle variable a ete recodee a la main.
                    p[colonne] = str(sous_lisible.loc[i, f"{colonne}_1"]).strip().title()
            personas.append(p)
    return personas


def systeme(persona):
    """Invite systeme : demographie et camp d'un seul persona, comme a5 systeme_c2."""
    lignes = [f"- {ETIQUETTES[c]}: {persona[c]}" for c in COLONNES_PERSONA[1:]]
    return ("You are simulating one specific person answering a survey. Answer exactly "
            "as this person would answer, not as you would.\n\n"
            "Here is what is known about this person:\n" + "\n".join(lignes))


def utilisateur(libelle):
    """Bloc utilisateur : la question GSS, le libelle de l'item, et le format impose.

    Grammaire de sortie identique a `r1_oracle_camps.utilisateur` (lettre, deux points,
    pourcentage entier, trois lignes sommant a 100), pour que `parser` s'applique sans
    modification.
    """
    lignes = ['Survey question, General Social Survey wording:',
              f'"{PREAMBULE_QUESTION} Are we spending too much, too little, or about '
              f'the right amount on {libelle}?"', "", "Answer options:"]
    for lettre, o in zip(LETTRES, OPTIONS):
        lignes.append(f"{lettre}. {o}")
    lignes += [
        "",
        "Estimate, for this specific person, the percentage chance they would give each "
        "answer.",
        "",
        "Reply with exactly 3 lines and nothing else: the option letter, a colon, and "
        "an integer percentage. The 3 percentages must add up to 100.",
        "A: <percentage>", "B: <percentage>", "C: <percentage>",
    ]
    return "\n".join(lignes)


# --------------------------------------------------------------------------------------
# 4. Trace, index et reprise
# --------------------------------------------------------------------------------------

def arret_demande():
    return os.path.exists(FICHIER_ARRET)


def journaliser(message):
    os.makedirs(TRACES, exist_ok=True)
    with open(JOURNAL_RUN, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


def chemin_trace(cle, suffixe):
    nom = f"c5-{cle}" + (("-" + suffixe) if suffixe else "")
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
            fait.add((d["version_prompt"], d["pid"], d["forme"]))
    return fait


# --------------------------------------------------------------------------------------
# 5. Le run
# --------------------------------------------------------------------------------------

def lancer(moteur, cle, info, personas, les_formes, fin_ts, suffixe, limite=None,
           journal_tous=100, n_predict=N_PREDICT):
    chemin = chemin_trace(cle, suffixe)
    fait = index_existant(chemin)
    print(f"[{cle}] trace {chemin}, {len(fait)} appels deja faits", flush=True)

    arrets = ARRETS[info["gabarit"]]
    n_appels = n_rejets = 0
    arret = False
    t0 = time.time()

    with open(chemin, "a", encoding="utf-8") as fh:
        for p in personas:
            sys_txt = systeme(p)
            for paire, version, var, libelle in les_formes:
                if (VERSION_PROMPT, p["pid"], var) in fait:
                    continue
                if arret_demande():
                    arret = True
                    message = f"[{cle}] ARRET DEMANDE ({FICHIER_ARRET}), arret propre"
                    print(message, flush=True)
                    journaliser("ARRET DEMANDE " + message)
                    break
                if time.time() >= fin_ts:
                    print(f"[{cle}] fin dure atteinte, arret propre", flush=True)
                    break
                if limite is not None and n_appels >= limite:
                    break

                usr_txt = utilisateur(libelle)
                prompt = gabarit(info["gabarit"], sys_txt, usr_txt)
                r = moteur.decrire(prompt, n_predict, arrets)
                distribution, somme, motif = parser(r["texte"], OPTIONS)
                rejet = distribution is None
                if rejet:
                    n_rejets += 1

                ligne = {
                    "version_prompt": VERSION_PROMPT, "cle_modele": cle,
                    "modele": info["nom"], "quantification": info["quantification"],
                    "gabarit": info["gabarit"],
                    "pid": p["pid"], "camp": p["camp"],
                    "paire": paire, "version_forme": version, "forme": var,
                    "libelle": libelle,
                    "duree_ms": round(r["duree_ms"], 2),
                    "tokens_generes": r["tokens_generes"],
                    "tokens_prompt": r["tokens_prompt"],
                    "sortie_brute": r["texte"],
                    "rejet": rejet, "rejets_cumules": n_rejets,
                    "motif_rejet": motif if rejet else "",
                    "somme_brute": None if somme != somme else round(somme, 4),
                    "distribution": distribution,
                }
                fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
                fh.flush()
                n_appels += 1

                if n_appels % journal_tous == 0:
                    ecoule = max(time.time() - t0, 1e-9)
                    debit = n_appels / ecoule * 3600
                    os.fsync(fh.fileno())
                    message = (f"[{cle}] {n_appels} appels, {debit:,.0f}/h, "
                               f"rejets {n_rejets}").replace(",", " ")
                    print(message, flush=True)
                    journaliser(message)
            else:
                continue
            break
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    return {
        "cle_modele": cle, "modele": info["nom"], "quantification": info["quantification"],
        "gabarit": info["gabarit"], "fichier": info["fichier"],
        "appels": n_appels, "deja_faits": len(fait), "secondes": round(ecoule, 1),
        "appels_par_heure": round(n_appels / ecoule * 3600, 1) if n_appels else 0.0,
        "duree_moyenne_ms": round(ecoule * 1000 / n_appels, 1) if n_appels else None,
        "rejets": n_rejets, "taux_rejet": round(n_rejets / n_appels, 4) if n_appels else 0.0,
        "arret_demande": arret, "trace": chemin,
    }


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default="oss20,q30",
                    help="cles du registre MODELES, dans l'ordre de passage")
    ap.add_argument("--personas", type=int, default=100,
                    help="personas PAR CAMP ; 100 donne les 300 du preenregistrement")
    ap.add_argument("--test", action="store_true",
                    help="20 personas de test, tirees hors du sous echantillon de 300, "
                         "jamais melangees a l'analyse finale")
    ap.add_argument("--fin", default="07:30", help="fin dure du calcul, heure locale")
    ap.add_argument("--suffixe", default="", help="suffixe de fichier, pour un smoke test")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal d'appels par modele, pour un smoke test")
    ap.add_argument("--n-predict", type=int, default=N_PREDICT)
    ap.add_argument("--port", type=int, default=0, help="0 pour choisir un port libre")
    ap.add_argument("--contexte", type=int, default=4096, help="tokens par slot")
    ap.add_argument("--parallele", type=int, default=1)
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    cles = [c.strip() for c in args.modele.split(",") if c.strip()]
    for c in cles:
        if c not in MODELES:
            sys.exit(f"modele inconnu : {c}. Cles connues : {', '.join(MODELES)}")
        chemin = os.path.join(GGUF, MODELES[c]["fichier"])
        if not os.path.exists(chemin):
            sys.exit(f"modele introuvable : {chemin}")

    fin_ts, fin_dt = heure_de_fin(args.fin)
    depart = datetime.datetime.now()
    print(f"popsim c5, formulation nat*. Depart {depart:%Y-%m-%d %H:%M:%S}, fin dure "
          f"{fin_dt:%Y-%m-%d %H:%M} ({(fin_ts - time.time()) / 3600:.2f} h). "
          f"Modeles : {', '.join(cles)}", flush=True)
    journaliser(f"DEBUT modeles={cles} test={args.test} personas_par_camp={args.personas}")

    humain = effet_humain_wave1()
    humain.to_csv(os.path.join(TRACES, "c5-effet-humain.csv"), index=False)
    print("effet humain (vague 1) recalcule, ecrit dans c5-effet-humain.csv", flush=True)

    les_formes = formes()
    if args.test:
        # Les 300 personas de production sont tirees d'abord : c'est leur ensemble
        # d'identifiants qui definit l'exclusion des personas de test.
        production = charger_personas(100, GRAINE_PERSONAS)
        ids_production = [p["pid"] for p in production]
        personas = charger_personas(7, GRAINE_TEST, exclure=ids_production)[:20]
        suffixe = args.suffixe or "smoke"
    else:
        personas = charger_personas(args.personas, GRAINE_PERSONAS)
        suffixe = args.suffixe

    chemin_personas = os.path.join(
        TRACES, f"c5-personas{'-' + suffixe if suffixe else ''}.csv")
    pd.DataFrame(personas).to_csv(chemin_personas, index=False)
    print(f"{len(personas)} personas ecrites : {chemin_personas}", flush=True)
    n_appels_prevus = len(personas) * len(les_formes)
    print(f"{len(les_formes)} formes par persona, {n_appels_prevus} appels par modele",
          flush=True)

    resume = []
    try:
        for cle in cles:
            if time.time() >= fin_ts:
                print(f"fin dure atteinte avant le lancement de {cle}", flush=True)
                break
            info = MODELES[cle]
            port = args.port or premier_port_libre()
            if not port_libre(port):
                sys.exit(f"le port {port} est occupe, un llama-server tourne peut etre deja")
            print(f"[{cle}] {info['nom']} {info['quantification']}, gabarit "
                  f"{info['gabarit']}, port {port}", flush=True)
            moteur = MoteurR1(os.path.join(GGUF, info["fichier"]),
                              contexte=args.contexte, parallele=args.parallele,
                              port=port, cache_kv_8bits=True)
            moteur.demarrer()
            print(f"[{cle}] serveur pret en {moteur.chargement_s:.1f} s", flush=True)
            try:
                r = lancer(moteur, cle, info, personas, les_formes, fin_ts, suffixe,
                           limite=args.limite, n_predict=args.n_predict)
                r["port"] = port
                r["chargement_s"] = round(moteur.chargement_s, 1)
                resume.append(r)
                print(f"[{cle}] {r['appels']} appels en {r['secondes'] / 60:.1f} min, "
                      f"{r['appels_par_heure']:,.0f} appels/h, {r['rejets']} rejets, "
                      f"{r['duree_moyenne_ms']} ms/appel".replace(",", " "), flush=True)
                journaliser(f"[{cle}] termine : {r['appels']} appels, "
                            f"taux de rejet {r['taux_rejet']:.4f}")
            finally:
                moteur.arreter()
                print(f"[{cle}] serveur arrete. charge machine : {os.getloadavg()}",
                      flush=True)
            if resume and resume[-1].get("arret_demande"):
                journaliser("ARRET DEMANDE, les modeles suivants ne sont pas lances")
                break
    finally:
        chemin_resume = os.path.join(
            TRACES, f"c5-resume{'-' + suffixe if suffixe else ''}.json")
        with open(chemin_resume, "w", encoding="utf-8") as fh:
            json.dump({
                "depart": depart.isoformat(), "fin": datetime.datetime.now().isoformat(),
                "fin_dure": fin_dt.isoformat(), "version_prompt": VERSION_PROMPT,
                "test": args.test, "personas": len(personas), "formes": len(les_formes),
                "n_predict": args.n_predict, "modeles": resume,
            }, fh, indent=2, ensure_ascii=False)
        print(f"resume ecrit : {chemin_resume}", flush=True)
        fin_message = (f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S} "
                       f"({sum(r['appels'] for r in resume)} appels)")
        print(fin_message, flush=True)
        journaliser(fin_message)


if __name__ == "__main__":
    main()
