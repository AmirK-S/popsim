"""
a21_extension_c2 : extension de la condition C2 a 150 personnes supplementaires.

Motif. Le rapport a18 section 11 point 2 etablit que le terme inter de la decomposition
n'est pas estimable a 55 personnes, et probablement pas non plus a 150 : le controle de la
vague 2 sort a 1,167 avec un intervalle qui deborde des deux cotes, et il ne passe pas sur
le genre, la race et l'education. Doubler l'echantillon de C2 est la premiere des trois
issues proposees a Simon (a18 section 12 question 1). A 300 personnes, C2 se compare a v8
et a v6 sur la meme population, avec un denominateur humain deux fois mieux estime.

Ce que fait ce script. Rien de neuf sur le fond : il rejoue EXACTEMENT le run C2 passe 1 de
analyses/a5_agents_locaux_gss.py, avec les memes fonctions importees et non recopiees, sur
150 personnes qui ne sont pas dans data/traces/a5-personnes.csv.

  chargement  : a5 importe a2_baselines_gss.charger et grille, graine 20260903
  prompts     : a5.systeme_c2, a5.utilisateur, a5.gabarit_qwen
  moteur      : a5.MoteurA5, heritant de a3.MoteurLlama
  scoring     : a5.masse_des_lettres, seuil de rejet a5.SEUIL_MASSE
  trace       : a5.lancer, format de ligne identique, index de reprise a5.index_existant
  boucle      : a5.travaux, ordre personne par personne puis bloc par bloc

Aucune ligne de ces fonctions n'est reecrite ici. Le seul apport du fichier est le tirage
du second echantillon et la discipline de lancement.

Fichiers. Le script n'ecrit QUE deux fichiers neufs et ne touche a aucun fichier existant
de data/traces/ :
  data/traces/a5-personnes-ext.csv    les 150 nouvelles personnes, colonnes pid, index, pli
  data/traces/a5-C2-p1-ext.jsonl      la trace, index de reprise sur ce seul fichier
  data/traces/a5-resume-ext.json      le resume de fin de run

Le suffixe "ext" a une consequence voulue sur les outils d'aval. a5_evaluer.lire_traces
sans suffixe ne ramasse que les fichiers dont le nom porte exactement deux tirets :
"a5-C2-p1.jsonl" en a deux, "a5-C2-p1-ext.jsonl" en a trois. L'evaluation du matin et la
decomposition a18 par defaut ne verront donc PAS cette trace et resteront sur les 150
personnes d'origine. C'est analyses/a21_evaluer_ext.py qui fait l'union des deux.

Discipline de lancement. a5 section 4.4 mesure un facteur 9,5 sur le debit quand deux
llama-server coexistent sur cette machine. Le script refuse donc de demarrer son serveur
tant que pgrep voit un llama-server, et attend par pauses de 30 secondes jusqu'a la limite
passee en argument. Le serveur est arrete dans un finally, comme dans a5.

Usage :
  .venv/bin/python analyses/a21_extension_c2.py --verification-seule
  .venv/bin/python analyses/a21_extension_c2.py --fin 07:30 --attente-max 240

Sortie : journal sur stdout, la file de nuit le redirige vers data/traces/a5-ext.log.
Derniere ligne du run : RUN TERMINE, meme marqueur que a5.
"""

import argparse
import datetime
import json
import os
import subprocess
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from a2_baselines_gss import charger, grille, GRAINE, N_BLOCS, N_PLIS
from a5_agents_locaux_gss import (MODELE, MODELE_NOM, QUANTIFICATION, TRACES,
                                  VERSION_PROMPT, MoteurA5, chemin_trace, gabarit_qwen,
                                  heure_de_fin, index_existant, lancer, nomenclature,
                                  port_libre, premier_port_libre, systeme_c2, travaux,
                                  utilisateur)

# Graine du second echantillon. Distincte de la graine du decoupage (20260903) et de celle
# du premier echantillon (20260907, a5.GRAINE_ECHANTILLON) : les plis ne bougent pas, et
# les 150 nouvelles personnes ne peuvent pas retomber sur les 150 premieres puisqu'elles
# sont tirees dans le complementaire.
GRAINE_EXT = 20260908

SUFFIXE_EXT = "ext"
CONDITION = "C2"
PASSE = 1

CHEMIN_PERSONNES = os.path.join(TRACES, "a5-personnes.csv")
CHEMIN_PERSONNES_EXT = os.path.join(TRACES, "a5-personnes-ext.csv")


# --------------------------------------------------------------------------------------
# 1. Le second echantillon
# --------------------------------------------------------------------------------------

def echantillon_hors(ids, plis, par_pli, exclus_index, graine=GRAINE_EXT):
    """Tire un second echantillon stratifie, dans le COMPLEMENTAIRE du premier.

    Copie de la logique de a5.echantillon, avec un seul changement : les indices deja
    retenus par le premier echantillon sont retires du vivier de chaque pli avant le
    tirage. La stratification est la meme, 30 personnes par pli sur les 5 plis de a2, pour
    la meme raison qu'en a5 : B1 et B2 sont evaluees pli par pli et entrainees sur les
    autres, un echantillon desequilibre melangerait des tailles d'entrainement.

    Le tirage dans le complementaire rend l'intersection avec le premier echantillon vide
    par construction, et non par verification a posteriori. La verification est faite
    quand meme, en --verification-seule.
    """
    rng = np.random.default_rng(graine)
    retenus = []
    for i_pli, (_, te) in enumerate(plis):
        vivier = np.array([k for k in te if int(k) not in exclus_index], dtype=int)
        n = min(par_pli, len(vivier))
        if n < par_pli:
            print(f"  AVERTISSEMENT : pli {i_pli}, seulement {n} personnes disponibles "
                  f"hors du premier echantillon", flush=True)
        for k in sorted(rng.choice(vivier, size=n, replace=False)):
            retenus.append({"pid": ids[k], "index": int(k), "pli": i_pli})
    return retenus


def lire_premier_echantillon():
    """Les 150 personnes du run a5, lues en LECTURE SEULE."""
    if not os.path.exists(CHEMIN_PERSONNES):
        sys.exit(f"echantillon d'origine introuvable : {CHEMIN_PERSONNES}. "
                 "L'extension n'a de sens que si le premier run a ecrit sa population.")
    ech = pd.read_csv(CHEMIN_PERSONNES)
    return ech, set(ech["pid"]), {int(v) for v in ech["index"]}


# --------------------------------------------------------------------------------------
# 2. Discipline de lancement : un seul llama-server a la fois
# --------------------------------------------------------------------------------------

def llama_server_present():
    """Vrai si un llama-server tourne sur la machine, quel qu'en soit le proprietaire.

    a5 section 4.4 : deux serveurs d'inference simultanes ne se partagent pas le GPU de
    cette machine, ils s'effondrent mutuellement, facteur 9,5 mesure. C'est la seule
    raison de cette fonction.
    """
    r = subprocess.run(["pgrep", "-f", "llama-server"], capture_output=True, text=True)
    pids = [l for l in r.stdout.split() if l.strip()]
    return len(pids) > 0, pids


def attendre_machine_libre(limite_minutes, fin_ts, pause=30):
    """Attend que plus aucun llama-server ne tourne. Rend le temps d'attente en secondes.

    Sort en erreur si la limite est atteinte, ou si la fin dure du calcul est atteinte
    pendant l'attente : demarrer un run qui n'a plus de budget n'a pas d'interet.
    """
    t0 = time.time()
    limite = limite_minutes * 60.0
    premier = True
    while True:
        present, pids = llama_server_present()
        if not present:
            if not premier:
                print(f"machine libre apres {(time.time() - t0) / 60:.1f} min d'attente",
                      flush=True)
            return time.time() - t0
        if premier:
            print(f"un llama-server tourne deja (PID {' '.join(pids)}). "
                  f"Attente par pauses de {pause} s, limite {limite_minutes} min.",
                  flush=True)
            premier = False
        if time.time() - t0 >= limite:
            sys.exit(f"limite d'attente de {limite_minutes} min atteinte, un llama-server "
                     "tourne toujours. Rien n'a ete lance, rien n'a ete ecrit dans la "
                     "trace.")
        if time.time() >= fin_ts:
            sys.exit("fin dure atteinte pendant l'attente de la machine. Rien n'a ete "
                     "lance.")
        attendu = int(time.time() - t0)
        if attendu % 300 < pause:
            print(f"  toujours occupe apres {attendu // 60} min, PID {' '.join(pids)}",
                  flush=True)
        time.sleep(pause)


# --------------------------------------------------------------------------------------
# 3. Verification sans serveur
# --------------------------------------------------------------------------------------

def premier_prompt(personne, items, blocs, y1, x, attributs, table):
    """Le tout premier prompt que a5 construirait pour cette personne en C2.

    On passe par a5.travaux, donc par le meme generateur, le meme ordre et le meme
    systeme_c2 que le run reel. Rien n'est reconstruit a la main ici : si le prompt de
    a5 change d'un caractere, celui ci change du meme caractere.
    """
    for p, i_bloc, j, sys_txt in travaux("C2", [personne], items, blocs, y1, x,
                                         attributs, table):
        bloc_user, options = utilisateur(items[j], table, inverse=False)
        return {"item": items[j], "bloc": i_bloc, "systeme": sys_txt,
                "utilisateur": bloc_user, "options": options,
                "prompt": gabarit_qwen(sys_txt, bloc_user)}
    return None


def comparer_caractere(a, b):
    """Position du premier caractere different, et nombre de lignes differentes."""
    n = min(len(a), len(b))
    premier = next((i for i in range(n) if a[i] != b[i]), None)
    if premier is None and len(a) != len(b):
        premier = n
    la, lb = a.split("\n"), b.split("\n")
    diff = [i for i in range(max(len(la), len(lb)))
            if (la[i] if i < len(la) else None) != (lb[i] if i < len(lb) else None)]
    return premier, diff, la, lb


def verifier(retenus, ech0, pids0, index0, items, blocs, y1, x, attributs, table,
             ids, deja_faits):
    """Le mode --verification-seule. Aucun appel de modele, aucun serveur."""
    print("=" * 90)
    print("a21 : VERIFICATION SANS SERVEUR DE L'EXTENSION DE C2")
    print("=" * 90)

    # --- 1. disjonction ---------------------------------------------------------------
    pids_ext = [p["pid"] for p in retenus]
    idx_ext = {p["index"] for p in retenus}
    inter_pid = pids0 & set(pids_ext)
    inter_idx = index0 & idx_ext
    print(f"\n1. Disjonction des deux echantillons")
    print(f"   premier echantillon  : {len(pids0)} personnes, {len(index0)} index")
    print(f"   second echantillon   : {len(pids_ext)} personnes, {len(idx_ext)} index")
    print(f"   pid en double        : {len(inter_pid)}")
    print(f"   index en double      : {len(inter_idx)}")
    print(f"   doublons internes    : {len(pids_ext) - len(set(pids_ext))}")
    if inter_pid or inter_idx or len(pids_ext) != len(set(pids_ext)):
        sys.exit("ECHEC : les deux echantillons ne sont pas disjoints.")
    print("   VERIFICATION PASSEE : intersection vide.")

    par_pli = {}
    for p in retenus:
        par_pli[p["pli"]] = par_pli.get(p["pli"], 0) + 1
    print(f"   stratification       : " + ", ".join(f"pli {k} : {v}"
                                                    for k, v in sorted(par_pli.items())))
    print(f"   union des deux       : {len(pids0 | set(pids_ext))} personnes distinctes")

    # --- 2. prompts -------------------------------------------------------------------
    print(f"\n2. Prompts C2 des 3 premieres nouvelles personnes, compares caractere pour")
    print( "   caractere a celui que a5 construit pour une personne de reference.")
    index_par_pid = {p: i for i, p in enumerate(ids)}
    ref_pid = ech0["pid"].iloc[0]
    ref = {"pid": ref_pid, "index": index_par_pid[ref_pid],
           "pli": int(ech0["pli"].iloc[0])}
    p_ref = premier_prompt(ref, items, blocs, y1, x, attributs, table)
    print(f"   reference : {ref_pid}, premier echantillon, item {p_ref['item']}, "
          f"{len(p_ref['prompt'])} caracteres")

    ok = True
    for p in retenus[:3]:
        pr = premier_prompt(p, items, blocs, y1, x, attributs, table)
        meme_item = pr["item"] == p_ref["item"]
        meme_user = pr["utilisateur"] == p_ref["utilisateur"]
        pos, diff, la, lb = comparer_caractere(p_ref["systeme"], pr["systeme"])
        # Les seules lignes autorisees a differer sont les lignes d'attribut, et
        # seulement sur la valeur : l'etiquette avant les deux points doit etre la meme.
        etiquettes_ok = all(la[i].split(":")[0] == lb[i].split(":")[0]
                            and la[i].startswith("- ") for i in diff
                            if i < len(la) and i < len(lb))
        memes_lignes = len(la) == len(lb)
        print(f"\n   {p['pid']} (index {p['index']}, pli {p['pli']}), item {pr['item']}, "
              f"{len(pr['prompt'])} caracteres")
        print(f"     meme item cible que la reference        : {meme_item}")
        print(f"     bloc utilisateur identique au caractere : {meme_user}")
        print(f"     meme nombre de lignes de systeme        : {memes_lignes} "
              f"({len(la)} contre {len(lb)})")
        print(f"     premier caractere different             : position {pos} "
              f"sur {len(p_ref['systeme'])}")
        print(f"     lignes differentes                      : {len(diff)} "
              f"sur {len(la)}, toutes des lignes d'attribut : {etiquettes_ok}")
        print(f"     preambule identique                     : "
              f"{la[0] == lb[0] and la[1] == lb[1]}")
        print(f"     consigne finale identique               : {la[-1] == lb[-1]}")
        for i in diff[:3]:
            print(f"       ligne {i:>2} reference : {la[i]}")
            print(f"       ligne {i:>2} nouvelle  : {lb[i]}")
        if len(diff) > 3:
            print(f"       ... {len(diff) - 3} autres lignes d'attribut")
        ok = ok and meme_item and meme_user and memes_lignes and etiquettes_ok

    if not ok:
        sys.exit("ECHEC : un prompt de l'extension ne se ramene pas au gabarit de a5.")
    print("\n   VERIFICATION PASSEE : hors les valeurs demographiques, les prompts sont")
    print("   identiques caractere pour caractere a celui de a5. Meme preambule, meme")
    print("   consigne, meme bloc utilisateur, meme gabarit Qwen, fin sans espace.")

    # --- 3. volume --------------------------------------------------------------------
    n_items = sum(len(b) for b in blocs)
    total = len(retenus) * n_items
    reste = total - deja_faits
    print(f"\n3. Volume de calcul")
    print(f"   personnes          : {len(retenus)}")
    print(f"   items par personne : {n_items}")
    print(f"   appels prevus      : {total}")
    print(f"   deja dans la trace : {deja_faits}")
    print(f"   appels a faire     : {reste}")
    for debit in (16700, 11000, 7400, 4900):
        print(f"   a {debit:>6} appels/h : {reste / debit:.2f} h")
    print(f"\n   trace visee : {chemin_trace(CONDITION, PASSE, SUFFIXE_EXT)}")
    print(f"   modele {MODELE_NOM} {QUANTIFICATION}, version de prompt {VERSION_PROMPT}")
    print("\nVERIFICATION TERMINEE. Aucun serveur lance, aucun appel de modele, "
          "aucune trace existante modifiee.")


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--personnes", type=int, default=150,
                    help="taille du second echantillon, repartie sur les 5 plis")
    ap.add_argument("--blocs", type=int, default=N_BLOCS,
                    help="nombre de blocs d'items, 5 pour les 149 items")
    ap.add_argument("--fin", default="07:30", help="fin dure du calcul, heure locale")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal d'appels, pour un essai")
    ap.add_argument("--port", type=int, default=0, help="0 pour choisir un port libre")
    ap.add_argument("--contexte", type=int, default=8192, help="tokens par slot")
    ap.add_argument("--parallele", type=int, default=8, help="-np, 8 en configuration a3")
    ap.add_argument("--attente-max", type=int, default=240,
                    help="minutes d'attente maximales si un llama-server tourne deja")
    ap.add_argument("--verification-seule", action="store_true",
                    help="construit l'echantillon et les prompts, ne lance aucun serveur")
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    fin_ts, fin_dt = heure_de_fin(args.fin)

    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    plis, blocs = grille(len(ids), len(items), GRAINE)
    blocs = blocs[:args.blocs]

    ech0, pids0, index0 = lire_premier_echantillon()
    par_pli = max(1, args.personnes // N_PLIS)
    retenus = echantillon_hors(ids, plis, par_pli, index0)

    # L'echantillon est ecrit avant tout appel, comme en a5 : c'est lui qui definit la
    # population sur laquelle l'evaluation restreindra baselines et conditions de
    # Stanford. a5-personnes.csv n'est jamais ouvert en ecriture par ce script.
    pd.DataFrame(retenus).to_csv(CHEMIN_PERSONNES_EXT, index=False)
    print(f"second echantillon ecrit : {CHEMIN_PERSONNES_EXT} ({len(retenus)} lignes)",
          flush=True)

    chemin = chemin_trace(CONDITION, PASSE, SUFFIXE_EXT)
    deja = index_existant(chemin)

    if args.verification_seule:
        verifier(retenus, ech0, pids0, index0, items, blocs, y1, x, attributs, table,
                 ids, len(deja))
        return

    n_items = sum(len(b) for b in blocs)
    print(f"popsim a21, extension de C2. Fin dure a {fin_dt:%Y-%m-%d %H:%M} "
          f"({(fin_ts - time.time()) / 3600:.2f} h)", flush=True)
    print(f"charge machine : {os.getloadavg()}", flush=True)
    print(f"{len(retenus)} nouvelles personnes ({par_pli} par pli), {n_items} items, "
          f"soit {len(retenus) * n_items} appels, {len(deja)} deja dans la trace",
          flush=True)

    attente = attendre_machine_libre(args.attente_max, fin_ts)

    port = args.port or premier_port_libre()
    if not port_libre(port):
        sys.exit(f"le port {port} est occupe, un llama-server tourne peut etre deja")
    if not os.path.exists(MODELE):
        sys.exit(f"modele introuvable : {MODELE}")
    print(f"llama-server sur le port {port}, -np {args.parallele}, "
          f"-c {args.contexte * args.parallele}, KV q8_0", flush=True)

    moteur = MoteurA5(MODELE, contexte=args.contexte, parallele=args.parallele, port=port,
                      cache_kv_8bits=True)
    moteur.demarrer()
    print(f"serveur pret en {moteur.chargement_s:.1f} s", flush=True)

    resume = []
    try:
        r = lancer(moteur, CONDITION, PASSE, False, retenus, items, blocs, y1, x,
                   attributs, table, fin_ts, SUFFIXE_EXT, limite=args.limite)
        resume.append(r)
        print(f"[{CONDITION} passe {PASSE}] {r['appels']} appels en "
              f"{r['secondes'] / 60:.1f} min, {r['appels_par_heure']:,.0f} appels/h, "
              f"{r['rejets']} rejets".replace(",", " "), flush=True)
    finally:
        # Meme discipline que a5 : le serveur est arrete quoi qu'il arrive, un autre run
        # peut attendre la machine et deux llama-server s'effondrent mutuellement.
        moteur.arreter()
        print(f"serveur arrete. charge machine : {os.getloadavg()}", flush=True)

    chemin_resume = os.path.join(TRACES, "a5-resume-ext.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({"fin_dure": fin_dt.isoformat(), "port": port,
                   "modele": MODELE_NOM, "quantification": QUANTIFICATION,
                   "version_prompt": VERSION_PROMPT, "passe": PASSE,
                   "graine_echantillon": GRAINE_EXT,
                   "personnes": len(retenus), "items": n_items,
                   "attente_machine_s": round(attente, 1),
                   "echantillon": os.path.basename(CHEMIN_PERSONNES_EXT),
                   "conditions": resume}, fh, indent=2, ensure_ascii=False)
    print(f"resume ecrit : {chemin_resume}", flush=True)
    print(f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S}", flush=True)


if __name__ == "__main__":
    main()
