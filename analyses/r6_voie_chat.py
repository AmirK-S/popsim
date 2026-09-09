"""
r6_voie_chat : la voie `chat` reproduit elle la voie `/completion` de R1 ? Mesure locale.

Statut : script d'experience, pas du code de production. Il joue l'etage 0 de
`resultats/r6-preenregistrement-v2.md`, section « Modeles et fournisseurs » : la
verification locale, a zero euro, qui conditionne tout appel payant de R6.

Le probleme. R1, R4 et R5 ont parle a `llama-server` par `/completion`, avec le gabarit
ChatML rendu a la main dans `R1.gabarit`. Les API distantes n'acceptent pas ce gabarit :
elles prennent deux tours de conversation et appliquent leur propre gabarit cote serveur.
Si les deux voies ne donnent pas la meme distribution, comparer un modele distant a `q4`
de R1 compare deux protocoles et non deux modeles.

Ce qu'il fait. Sur le MEME fichier de poids que R1 (`Qwen3-4B-Instruct-2507-Q4_K_M.gguf`),
un seul `llama-server`, configuration de a3 section 4.7 (contexte 4096, `-np 1`, cache KV
q8_0, tout sur le GPU), il joue 40 cellules tirees d'avance du plan F1 par trois voies :

  trace    la distribution deja ecrite dans `data/traces/r1-q4.jsonl` le 9 septembre ;
  compl    la voie de R1 rejouee maintenant : `/completion`, gabarit ChatML rendu a la main
           par `R1.gabarit`, `R1.parser` ;
  chat     la voie des API : `/v1/chat/completions` du meme serveur, deux tours de
           conversation, gabarit applique par le serveur, jouee par le CLIENT DE R6
           (`r6_oracle_distant.ClientChat` et `r6_oracle_distant.lancer`) avec sa
           `base_url` pointee sur 127.0.0.1. Aucun octet ne sort de la machine.

Les 40 cellules sont tirees et ecrites AVANT le lancement dans
`data/traces/r6-verif-cellules.txt`, comme la v2 l'exige.

Seuil preenregistre : **au moins 38 distributions identiques sur 40** entre `compl` et
`chat`. En dessous, la voie `chat` est inscrite au registre comme un protocole distinct,
« gabarit serveur », et aucune comparaison directe entre R6 et R1 n'est ecrite.

Entree  : data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf, non versionne.
          data/traces/r1-q4.jsonl, lue et jamais modifiee.
Sortie  : data/traces/r6-verif-cellules.txt, la liste des 40 cellules.
          data/traces/r6-verif/r6-voie-chat-compl.jsonl, la voie /completion rejouee.
          data/traces/r6-verif/r6-Qwen3-4B-Instruct-2507-q4-voiechat.jsonl, la voie chat,
          ecrite par le client de R6 lui meme. Sous dossier voulu : r1_evaluer.py ne
          descend pas dans les sous dossiers, une trace de verification locale n'entre
          donc jamais dans les mesures d'un run distant.
          data/traces/r6-voie-chat.json, le resume chiffre.
          resultats/r6-voie-chat.md, le rapport.

Un seul llama-server a la fois : le script attend si un `llama-server` tourne deja, il ne
le tue jamais, et il arrete le sien dans un `finally`.

Arret : `touch data/traces/STOP` arrete la boucle entre deux cellules.

Usage :
  .venv/bin/python analyses/r6_voie_chat.py --tirer          # tire la liste, aucun appel
  .venv/bin/python analyses/r6_voie_chat.py                  # la mesure, environ 3 min
"""

import argparse
import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_oracle_camps as R1
import r6_oracle_distant as R6
from a2_baselines_gss import charger, FAMILLES
from a5_agents_locaux_gss import nomenclature, port_libre, premier_port_libre

RACINE = R6.RACINE
TRACES = R6.TRACES
SORTIE = R6.SORTIE
GGUF = os.path.join(RACINE, "data/modeles/gguf")

CLE_LOCALE = "q4"
INFO = R1.MODELES[CLE_LOCALE]
NOM_MODELE = INFO["nom"]

VERIF = os.path.join(TRACES, "r6-verif")
LISTE = os.path.join(TRACES, "r6-verif-cellules.txt")
TRACE_COMPL = os.path.join(VERIF, "r6-voie-chat-compl.jsonl")
TRACE_R1 = os.path.join(TRACES, "r1-q4.jsonl")
RESUME = os.path.join(TRACES, "r6-voie-chat.json")
RAPPORT = os.path.join(SORTIE, "r6-voie-chat.md")

N_CELLULES = 40
SEUIL = 38
TOLERANCE = 1e-9


# --------------------------------------------------------------------------------------

def un_seul_serveur(attente_max=1800):
    """Attend qu'aucun llama-server ne tourne. Ne tue jamais celui d'un autre run."""
    debut = time.time()
    while True:
        r = subprocess.run(["pgrep", "-x", "llama-server"], capture_output=True, text=True)
        if r.returncode != 0:
            return True
        if time.time() - debut > attente_max:
            sys.exit("un llama-server tourne depuis plus de 30 minutes, abandon")
        print("un llama-server tourne deja, attente de 30 s", flush=True)
        time.sleep(30)


def lire_trace_r1(chemin=TRACE_R1):
    """(item, camp, identite) -> distribution ecrite par R1, cellules non rejetees."""
    par_cellule = {}
    if not os.path.exists(chemin):
        sys.exit(f"trace de R1 absente : {chemin}")
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            par_cellule[(d["item"], d["camp"], d["identite"])] = d
    return par_cellule


def tirer(items):
    """Les 40 cellules, tirees a graine fixe dans le plan F1, ecrites avant tout appel."""
    p = R6.PLANS["f1"]
    cellules = R6.tirer_liste(items, p["camps"], p["identites"], N_CELLULES)
    R6.ecrire_liste(cellules, LISTE)
    return cellules


def identiques(a, b, options):
    """Deux distributions sont elles la meme, modalite par modalite ?"""
    if a is None or b is None:
        return a is None and b is None
    return all(abs(float(a[o]) - float(b[o])) <= TOLERANCE for o in options)


def tv(a, b, options):
    if a is None or b is None:
        return None
    return 0.5 * sum(abs(float(a[o]) - float(b[o])) for o in options)


# --------------------------------------------------------------------------------------

def jouer_completion(moteur, cellules, table, familles_par_item):
    """La voie de R1, rejouee maintenant : gabarit a la main, /completion, R1.parser."""
    arrets = R1.ARRETS[INFO["gabarit"]]
    sorties = {}
    with open(TRACE_COMPL, "w", encoding="utf-8") as fh:
        for n, (camp, identite, item) in enumerate(cellules, 1):
            if R6.arret_demande():
                print("ARRET DEMANDE, voie /completion interrompue", flush=True)
                break
            sys_txt = R1.systeme(camp, identite)
            usr_txt, options = R1.utilisateur(item, camp, table, rappel=False)
            # Le gabarit d'origine de R1, pas celui que R5 injecte : R5 ne remplace
            # `R1.gabarit` que pour sa propre cle `chatml-3ex`, et delegue le reste.
            prompt = R1.gabarit(INFO["gabarit"], sys_txt, usr_txt)
            r = moteur.decrire(prompt, R1.N_PREDICT, arrets)
            distribution, somme, motif = R1.parser(r["texte"], options)
            sorties[(item, camp, identite)] = {"distribution": distribution,
                                               "options": options, "motif": motif}
            fh.write(json.dumps({
                "version_prompt": R1.VERSION_PROMPT, "cle_modele": "q4-voiecompl",
                "modele": NOM_MODELE, "quantification": INFO["quantification"],
                "gabarit": INFO["gabarit"], "item": item,
                "famille": familles_par_item.get(item, "hors famille"),
                "camp": camp, "identite": identite,
                "demandeur_camp": R1.ADVERSAIRE[camp] if identite == "adversaire" else None,
                "n_modalites": len(options), "options": options,
                "n_tentatives": 1, "sans_relance": True,
                "rejet": distribution is None, "motif_rejet": motif,
                "somme_brute": None if somme != somme else round(somme, 4),
                "distribution": distribution,
                "duree_ms": round(r["duree_ms"], 2),
                "tokens_prompt": r["tokens_prompt"], "tokens_generes": r["tokens_generes"],
            }, ensure_ascii=False) + "\n")
            fh.flush()
            if n % 10 == 0:
                print(f"  /completion : {n} / {len(cellules)}", flush=True)
    return sorties


def jouer_chat(port, cellules, table, familles_par_item):
    """La voie des API, jouee par le client de R6 lui meme, pointe sur 127.0.0.1.

    La trace part dans `data/traces/r6-verif/`, un sous dossier, et non a la racine de
    `data/traces/`. Motif : `r1_evaluer.py --suffixe r6` ramasse `data/traces/r6-*.jsonl`
    sans descendre dans les sous dossiers ; une trace de verification locale entrerait
    sinon dans les mesures d'un run distant, ou elle n'a rien a faire.
    """
    client = R6.ClientChat("locale-sans-cle", base=f"http://127.0.0.1:{port}/v1",
                           timeout=300, raisonnement="aucun", usage_inclus=False)
    budget = R6.Budget(0.0, 0.0, 0.0, R6.JETONS_ESTIMES["q4"])
    cle = "Qwen3-4B-Instruct-2507-q4-voiechat"
    traces_avant, journal_avant = R6.TRACES, R6.JOURNAL
    R6.TRACES = VERIF
    R6.JOURNAL = os.path.join(VERIF, "r6-voie-chat.log")
    os.makedirs(VERIF, exist_ok=True)
    try:
        chemin = R6.chemin_trace(cle)
        if os.path.exists(chemin):
            os.remove(chemin)                   # la mesure se rejoue en entier ou pas
        r = R6.lancer(client, NOM_MODELE, "q4", table, cellules, budget, cle,
                      n_predict=R1.N_PREDICT, journal_tous=10,
                      familles_par_item=familles_par_item)
    finally:
        R6.TRACES, R6.JOURNAL = traces_avant, journal_avant
    sorties = {}
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            d = json.loads(ligne)
            sorties[(d["item"], d["camp"], d["identite"])] = {
                "distribution": d["distribution"], "options": d["options"],
                "motif": d["motif_rejet"]}
    return sorties, r, chemin


# --------------------------------------------------------------------------------------

def comparer(cellules, trace_r1, compl, chat):
    """Une ligne par cellule, et les trois comptes d'identite."""
    lignes = []
    for camp, identite, item in cellules:
        k = (item, camp, identite)
        t = trace_r1.get(k)
        d_trace = t.get("distribution") if t else None
        options = (t or {}).get("options") or (compl.get(k) or {}).get("options") \
            or (chat.get(k) or {}).get("options")
        d_compl = (compl.get(k) or {}).get("distribution")
        d_chat = (chat.get(k) or {}).get("distribution")
        lignes.append({
            "item": item, "camp": camp, "identite": identite,
            "n_modalites": len(options) if options else None,
            "rejet_trace": d_trace is None, "rejet_compl": d_compl is None,
            "rejet_chat": d_chat is None,
            "chat_egale_compl": identiques(d_chat, d_compl, options) if options else None,
            "chat_egale_trace": identiques(d_chat, d_trace, options) if options else None,
            "compl_egale_trace": identiques(d_compl, d_trace, options) if options else None,
            "tv_chat_compl": tv(d_chat, d_compl, options) if options else None,
            "tv_chat_trace": tv(d_chat, d_trace, options) if options else None,
            "motif_chat": (chat.get(k) or {}).get("motif", ""),
        })
    return lignes


def moyenne(valeurs):
    v = [x for x in valeurs if x is not None]
    return sum(v) / len(v) if v else None


def ecrire_rapport(res, lignes, chemin=RAPPORT):
    n = res["n_cellules"]
    verdict = ("PASSE" if res["chat_egale_compl"] >= SEUIL else "NE PASSE PAS")
    desaccords = [l for l in lignes if l["chat_egale_compl"] is False]
    with open(chemin, "w", encoding="utf-8") as fh:
        e = fh.write
        e("# r6, etage 0. La voie `chat` reproduit elle la voie `/completion` de R1 ?\n\n")
        e(f"Mesure du {res['date']}, en local, sur `{NOM_MODELE}` "
          f"{INFO['quantification']}, un seul `llama-server`, configuration de a3 section "
          f"4.7 (contexte {res['contexte']}, `-np {res['parallele']}`, cache KV q8_0). "
          f"Zero appel distant, zero euro. Verification exigee par "
          f"`resultats/r6-preenregistrement-v2.md`, etage 0, avant tout appel payant.\n\n")

        e("## Ce qui est compare\n\n")
        e(f"{n} cellules du plan F1, tirees a graine fixe {R6.GRAINE_LISTE} avant le "
          f"lancement et ecrites dans `data/traces/r6-verif-cellules.txt`. Chaque cellule "
          f"est jouee par trois voies, sur le meme fichier de poids et la meme invite, "
          f"construite par `R1.systeme` et `R1.utilisateur` et jamais recopiee.\n\n")
        e("| voie | transport | gabarit | lecture |\n|---|---|---|---|\n")
        e("| `trace` | deja ecrite le 9 septembre | ChatML rendu a la main par `R1.gabarit` "
          "| `R1.parser` |\n")
        e("| `compl` | `/completion`, rejouee maintenant | ChatML rendu a la main par "
          "`R1.gabarit` | `R1.parser` |\n")
        e("| `chat` | `/v1/chat/completions`, client de R6 | applique par le serveur | "
          "`R1.parser` |\n\n")

        e("## Resultat\n\n")
        e("| comparaison | distributions identiques | sur | taux |\n|---|---|---|---|\n")
        for cle, libelle in (("chat_egale_compl", "`chat` contre `compl`"),
                             ("chat_egale_trace", "`chat` contre `trace` de R1"),
                             ("compl_egale_trace", "`compl` contre `trace` de R1")):
            e(f"| {libelle} | {res[cle]} | {n} | "
              f"{res[cle] / n:.3f} |\n")
        e("\n")
        e(f"Distance de variation totale moyenne entre `chat` et `compl` : "
          f"{res['tv_chat_compl_moyenne']:.6f} ; maximum "
          f"{res['tv_chat_compl_max']:.6f}.\n\n")
        e(f"Rejets de parse : {res['rejets_trace']} dans la trace de R1, "
          f"{res['rejets_compl']} en `compl`, {res['rejets_chat']} en `chat`.\n\n")

        e("## Verdict contre le seuil de la v2\n\n")
        e(f"Seuil preenregistre : au moins **{SEUIL} sur {n}** distributions identiques "
          f"entre `compl` et `chat`. Mesure : **{res['chat_egale_compl']} sur {n}**. "
          f"**{verdict}.**\n\n")
        if verdict == "PASSE":
            e("La voie `chat` est donc lisible comme la voie de R1 : les distributions de "
              "R6 se comparent directement a `q4`, `q4nogab`, `q4base` et `q4gab3` sans "
              "colonne de protocole supplementaire.\n\n")
        else:
            e("La voie `chat` est donc inscrite au registre comme un protocole distinct, "
              "« gabarit serveur ». Aucune comparaison directe entre une distribution de "
              "R6 et une distribution de R1 n'est ecrite sans cette mention.\n\n")

        if desaccords:
            e(f"### Les {len(desaccords)} cellules en desaccord\n\n")
            e("| item | camp | identite | K | TV | rejet chat |\n|---|---|---|---|---|---|\n")
            for l in desaccords:
                e(f"| `{l['item']}` | {l['camp']} | {l['identite']} | {l['n_modalites']} | "
                  f"{'' if l['tv_chat_compl'] is None else format(l['tv_chat_compl'], '.4f')} "
                  f"| {'oui' if l['rejet_chat'] else 'non'} |\n")
            e("\n")

        e("## Cout en temps\n\n")
        e(f"Chargement du serveur {res['chargement_s']:.1f} s. Voie `compl` "
          f"{res['secondes_compl']:.1f} s pour {n} cellules. Voie `chat` "
          f"{res['secondes_chat']:.1f} s. Total de la seance "
          f"{res['secondes_total']:.1f} s, soit {res['secondes_total'] / 60:.1f} min. "
          f"Zero euro : aucun appel distant.\n\n")
        e(f"Latence mediane de la voie `chat` : {res['latence_chat_ms']} ms par cellule.\n\n")

        e("## Ce que je n'ai pas pu verifier\n\n")
        e("1. **Que le gabarit applique par `llama-server` est celui qu'appliquent les "
          "fournisseurs distants.** La mesure porte sur un serveur local qui lit le gabarit "
          "embarque dans le fichier GGUF de Qwen. OpenAI, Anthropic, Google et xAI "
          "appliquent le leur, qu'aucune API ne rend lisible. Ce qui est verifie ici est "
          "que le CLIENT de R6 et la mise en deux tours de conversation ne cassent rien ; "
          "ce n'est pas une verification du gabarit de chaque fournisseur.\n")
        e("2. **Le determinisme des API distantes a temperature 0.** Il est mesure ici sur "
          "un serveur local, ou il est acquis. La v2 prevoit pour cela le plancher machine "
          "des 40 memes cellules rejouees sur chaque modele payant ; il n'est pas joue par "
          "ce script.\n")
        e("3. **Que les 40 cellules representent les 894.** Elles sont tirees a graine "
          "fixe dans le plan complet, sans stratification par nombre de modalites ni par "
          "camp. Un desaccord concentre sur les items a K eleve ne se verrait pas "
          "forcement a cet effectif.\n")
        e("4. **Le format `q4gab3`.** La verification porte sur F1, gabarit seul. F2 place "
          "les trois exemples dans le tour utilisateur ; rien ne dit qu'un gabarit serveur "
          "les traite comme le fait la concatenation de R5, et ce script ne le mesure "
          "pas.\n")
        e("5. **Le comportement du client sous erreur 429 et sous limite de debit.** Le "
          "serveur local n'en produit aucune ; seul le faux serveur de "
          "`analyses/test_r6_client.py` couvre ce chemin.\n\n")

        e("## Questions ouvertes pour Simon\n\n")
        e("1. Le seuil de 38 sur 40 a ete pose avant la mesure, sans modele d'erreur. "
          "Faut il le lire comme un test binaire, ou publier plutot la distance de "
          "variation totale moyenne entre voies a cote de chaque quantite, comme la v2 le "
          "fait deja pour le plancher machine ?\n")
        e("2. Si la voie `chat` diverge sur les items a beaucoup de modalites, la reponse "
          "est elle de retirer ces items du perimetre comparatif, ou de publier deux "
          "colonnes de protocole ?\n")
        e("3. La v2 interdit toute reformulation d'invite. Un modele distant qui refuse le "
          "format sur plus de deux cellules sur dix est retire du panel. Est ce le bon "
          "arbitrage pour le papier, ou faut il publier le taux de refus de format comme "
          "une mesure a part entiere, ce qu'il est ?\n")
        e("4. Le meme fichier de poids servi par un fournisseur distant peut etre quantifie "
          "autrement. La ligne de registre porte le champ `provider` ; suffit elle, ou "
          "faut il refuser les modeles ouverts dont la quantification aval n'est pas "
          "publiee ?\n")
    return chemin


# --------------------------------------------------------------------------------------

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tirer", action="store_true",
                    help="tire les 40 cellules, les ecrit, et sort. Aucun appel.")
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--contexte", type=int, default=4096)
    ap.add_argument("--parallele", type=int, default=1)
    args = ap.parse_args(argv)

    os.makedirs(TRACES, exist_ok=True)
    os.makedirs(VERIF, exist_ok=True)
    table = nomenclature()
    _ids, items, _y1, _y2, _x, _attributs = charger()
    familles_par_item = {it: nom for nom, membres in FAMILLES.items() for it in membres}

    cellules = tirer(list(items))
    print(f"{len(cellules)} cellules tirees et ecrites : {LISTE}", flush=True)
    if args.tirer:
        return 0

    if R6.arret_demande():
        sys.exit(f"fichier d'arret present : {R6.FICHIER_ARRET}. Le retirer avant.")
    chemin_modele = os.path.join(GGUF, INFO["fichier"])
    if not os.path.exists(chemin_modele):
        sys.exit(f"modele introuvable : {chemin_modele}")

    trace_r1 = lire_trace_r1()
    manquantes = [c for c in cellules if (c[2], c[0], c[1]) not in trace_r1]
    if manquantes:
        sys.exit(f"{len(manquantes)} cellules tirees absentes de {TRACE_R1}")

    un_seul_serveur()
    port = args.port or premier_port_libre()
    if not port_libre(port):
        sys.exit(f"le port {port} est occupe")

    t0 = time.time()
    moteur = R1.MoteurR1(chemin_modele, contexte=args.contexte, parallele=args.parallele,
                         port=port, cache_kv_8bits=True)
    print(f"lancement de llama-server sur le port {port}", flush=True)
    moteur.demarrer()
    print(f"serveur pret en {moteur.chargement_s:.1f} s", flush=True)
    try:
        t1 = time.time()
        compl = jouer_completion(moteur, cellules, table, familles_par_item)
        t2 = time.time()
        chat, resume_chat, chemin_chat = jouer_chat(port, cellules, table,
                                                    familles_par_item)
        t3 = time.time()
    finally:
        # Un seul llama-server a la fois : il est arrete quoi qu'il arrive.
        moteur.arreter()
        print(f"serveur arrete. charge machine : {os.getloadavg()}", flush=True)

    lignes = comparer(cellules, trace_r1, compl, chat)
    n = len(lignes)
    res = {
        "date": time.strftime("%Y-%m-%d %H:%M"),
        "modele": NOM_MODELE, "quantification": INFO["quantification"],
        "fichier": INFO["fichier"], "contexte": args.contexte,
        "parallele": args.parallele, "port": port,
        "n_cellules": n, "seuil": SEUIL,
        "chat_egale_compl": sum(1 for l in lignes if l["chat_egale_compl"]),
        "chat_egale_trace": sum(1 for l in lignes if l["chat_egale_trace"]),
        "compl_egale_trace": sum(1 for l in lignes if l["compl_egale_trace"]),
        "rejets_trace": sum(1 for l in lignes if l["rejet_trace"]),
        "rejets_compl": sum(1 for l in lignes if l["rejet_compl"]),
        "rejets_chat": sum(1 for l in lignes if l["rejet_chat"]),
        "tv_chat_compl_moyenne": moyenne([l["tv_chat_compl"] for l in lignes]) or 0.0,
        "tv_chat_compl_max": max([l["tv_chat_compl"] for l in lignes
                                  if l["tv_chat_compl"] is not None] or [0.0]),
        "tv_chat_trace_moyenne": moyenne([l["tv_chat_trace"] for l in lignes]) or 0.0,
        "chargement_s": moteur.chargement_s,
        "secondes_compl": t2 - t1, "secondes_chat": t3 - t2, "secondes_total": t3 - t0,
        "latence_chat_ms": resume_chat.get("latence_ms_mediane"),
        "trace_chat": chemin_chat, "trace_compl": TRACE_COMPL, "liste": LISTE,
        "cellules": lignes,
    }
    with open(RESUME, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    chemin = ecrire_rapport(res, lignes)
    print(f"\nchat contre compl : {res['chat_egale_compl']} / {n} identiques "
          f"(seuil {SEUIL})", flush=True)
    print(f"chat contre trace R1 : {res['chat_egale_trace']} / {n}", flush=True)
    print(f"compl contre trace R1 : {res['compl_egale_trace']} / {n}", flush=True)
    print(f"TV moyenne chat contre compl : {res['tv_chat_compl_moyenne']:.6f}", flush=True)
    print(f"resume : {RESUME}\nrapport : {chemin}", flush=True)
    return 0 if res["chat_egale_compl"] >= SEUIL else 1


if __name__ == "__main__":
    sys.exit(main())
