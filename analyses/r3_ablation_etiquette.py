"""
r3_ablation_etiquette : la vraie ablation de l'etiquette, a un seul facteur.

Objection bloquante numero 1 de resultats/a45-relecture-adverse-2.md. La page de plan est
resultats/r3-preenregistrement.md, horodatee du 8 septembre 2026 a 22:30:01 CEST, ecrite
AVANT le moindre appel de modele de langage, et non modifiee ensuite.

Le probleme. C2 et C3 de a5 ne different pas par la presence de l'etiquette : C2 contient
les onze attributs demographiques et AUCUNE reponse de la personne, C3 contient les ~119
reponses et AUCUNE demographie. Les deux conditions echangent toute leur entree. Huit
textes du dossier appellent ce contraste une ablation de l'etiquette ; c'est faux.

Ce que ce script produit, sur les MEMES 150 personnes de data/traces/a5-personnes.csv, les
MEMES 58 items des six familles de a2, le MEME modele (Qwen3-4B-Instruct-2507 Q4_K_M), le
MEME gabarit, le MEME scoring par lettres et le MEME decoupage de contexte que C3 (blocs de
a2, l'item cible retire avec son bloc, cousins presents) :

  C3E   le prompt de C3 PLUS les 11 attributs demographiques de C2, ideologie et parti
        compris, ajoutes EN TETE du persona. C'est C3 avec l'etiquette.
        Contraste principal : C3E contre C3, trace a5-C3-p1.jsonl, memes cellules.
  C2S   le prompt de C2 SANS political_ideology ni political_party, les 9 autres
        attributs. Contraste : C2 (trace a5-C2-p1.jsonl) contre C2S. C'est l'analogue de
        v8 contre v6 chez Stanford.
  C3ES  C3 plus les 9 memes attributs, pour separer l'etiquette ideologique de l'etiquette
        demographique dans le regime riche. Ne tourne que si le temps reste.

AUCUN SCRIPT EXISTANT N'EST MODIFIE. Tout ce qui fait le prompt, le decoupage, le scoring
et le transport est importe :

  a5_agents_locaux_gss  systeme_c2(), systeme_c3(), utilisateur(), gabarit_qwen(),
                        nomenclature(), echantillon(), groupes_familles(), MoteurA5,
                        LETTRES, SEUIL_MASSE, TRACES, heure_de_fin(), port_libre(),
                        premier_port_libre(), PREAMBULE, CONSIGNE,
                        ETIQUETTES_DEMOGRAPHIQUES.
  r2_rares_apparie      serveurs_en_cours(), un_appel(), tokens_des_lettres(),
                        construire_prompt(), VARIANTES, MODELES, verdict_smoke(),
                        projeter(), sortie_est_deja(), N_SMOKE.
  a2_baselines_gss      charger(), grille(), FAMILLES, GRAINE, N_PLIS.

Les prompts de C3E et de C3ES ne sont pas reecrits : leur bloc demographique est le CORPS
EXACT de systeme_c2 et leur bloc de reponses le CORPS EXACT de systeme_c3, recolles. La
verification hors ligne le teste par egalite de chaines. C'est la seule maniere d'affirmer
que « seule l'etiquette bouge » sans repeter l'erreur que a45 vient de trouver.

Gabarit et variante de fin de prompt FIXES, jamais sondes : R2 sonde parce qu'il change de
modele ; R3 garde le modele de a5 et doit rester comparable caractere pour caractere aux
traces a5-C2-p1.jsonl et a5-C3-p1.jsonl. La variante est `answer`, le prompt s'arrete sur
`Answer:` sans espace final, c'est celle de a5 mot pour mot.

Budget. La fenetre va de l'arret de R2 (05:45) a la fin dure (08:00). Elle ne couvre pas
C3E en entier. Regle ecrite dans la page de plan section 3 : le run RESERVE a C2S le temps
que sa projection lui donne, majore de 15 pour cent, et fixe a C3E une fin intermediaire
egale a la fin dure moins cette reserve. Les personnes sont parcourues dans l'ordre de
a5-personnes.csv dans les trois conditions, donc une troncature coute des personnes
entieres et les perimetres sont emboites.

Entree  : data/osf-t6g7k-stanford, non versionne. data/traces/a5-personnes.csv.
Sortie  : data/traces/r3-<condition>-qwen4.jsonl, une ligne par appel, format de a5.
          data/traces/r3-run.log, r3-run.pid, r3-resume-qwen4.json, r3-smoke-qwen4.jsonl.

Rien ne sort de la machine. Aucun appel distant. La trace ne contient PAS la vraie reponse
de la personne : l'evaluateur la relit dans data/, position de METHODOLOGIE.

Reprise : l'index unique est (condition, pid, item), lu dans la trace. Une relance ne
refait aucun appel deja ecrit.

Usage :
  .venv/bin/python analyses/r3_ablation_etiquette.py --fin 08:00
  .venv/bin/python analyses/r3_ablation_etiquette.py --verification-seule
  .venv/bin/python analyses/r3_ablation_etiquette.py --conditions C2S --limite 20
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

from a2_baselines_gss import charger, grille, GRAINE, N_PLIS
from a5_agents_locaux_gss import (CONSIGNE, ETIQUETTES_DEMOGRAPHIQUES, LETTRES, PREAMBULE,
                                  SEUIL_MASSE, TRACES, MoteurA5, echantillon,
                                  groupes_familles, heure_de_fin, nomenclature,
                                  port_libre, premier_port_libre, systeme_c2, systeme_c3,
                                  utilisateur)
from r2_rares_apparie import (MODELES, N_SMOKE, VARIANTES, construire_prompt, projeter,
                              serveurs_en_cours, sortie_est_deja, tokens_des_lettres,
                              un_appel, verdict_smoke)

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Le modele de R3 n'est pas un drapeau : c'est celui de C2 et de C3, et il n'y a pas
# d'ablation possible si le modele change en meme temps que l'etiquette.
CLE_MODELE = "qwen4"
VARIANTE = "answer"

# Les deux lignes que C2S retire. Ce sont les deux etiquettes politiques ; l'ideologie
# est celle que a1, a38, a39 et a44 lisent, le parti est celle que a45 ajoute a la grille
# des neuf segmentations. Les retirer toutes les deux, et pas seulement l'ideologie,
# evite qu'un modele reconstruise l'une depuis l'autre : sur les 1 052 personnes du GSS,
# ideologie et parti sont fortement associes, et une ablation qui laisse le parti ne
# serait pas une ablation.
ETIQUETTES_RETIREES = ("political_ideology", "political_party")

GRAINE_ECHANTILLON = 20260907

# Marge sur la reserve de temps de C2S. Elle absorbe le ralentissement d'un debit mesure
# sur vingt appels et projete sur 8 700.
MARGE_RESERVE = 1.15
# Plafond de la reserve : C2S ne peut jamais prendre plus de cette part du budget, sinon
# une projection fausse tuerait H1 pour sauver H2.
PART_MAX_RESERVE = 0.45

_journal_fh = None


def journal(texte=""):
    """Ecrit sur la sortie standard ET dans data/traces/r3-run.log.

    Meme convention que R2 : le fichier est ouvert en ajout, et le second handle est
    ferme quand la file de nuit redirige deja la sortie standard vers ce meme fichier,
    pour qu'aucune ligne ne soit ecrite deux fois.
    """
    print(texte, flush=True)
    if _journal_fh is not None:
        _journal_fh.write(texte + "\n")
        _journal_fh.flush()


# ---------------------------------------------------------------------------
# 1. Les prompts, par recollage et jamais par reecriture
# ---------------------------------------------------------------------------

def corps(texte):
    """Retire le preambule et la consigne d'un prompt systeme de a5.

    a5 encadre tous ses prompts systeme par le meme PREAMBULE et la meme CONSIGNE. Pour
    fabriquer C3E il faut recoller le milieu de systeme_c2 et le milieu de systeme_c3
    dans une seule enveloppe. Cette fonction leve si l'enveloppe n'est pas celle
    attendue : si a5 changeait son preambule, R3 s'arreterait au lieu de produire
    silencieusement un prompt different de celui de la trace de reference.
    """
    debut, fin = PREAMBULE + "\n\n", "\n\n" + CONSIGNE
    if not texte.startswith(debut) or not texte.endswith(fin):
        raise RuntimeError("l'enveloppe de a5 a change : PREAMBULE ou CONSIGNE ne sont "
                           "plus aux extremites du prompt systeme")
    return texte[len(debut):len(texte) - len(fin)]


def sans_etiquettes(valeurs, attributs, retirees=ETIQUETTES_RETIREES):
    """Les memes attributs, prives des lignes retirees. Ordre conserve."""
    garde = [i for i, a in enumerate(attributs) if a not in retirees]
    return ([valeurs[i] for i in garde], [attributs[i] for i in garde])


def systeme_c2s(valeurs, attributs):
    """Prompt de C2 prive de l'ideologie et du parti. Neuf lignes, rien d'autre change.

    Il n'y a pas une ligne de mise en forme reecrite ici : c'est systeme_c2 de a5,
    appele sur neuf attributs au lieu de onze. Les neuf lignes conservees sont donc
    identiques caractere pour caractere a celles de la trace a5-C2-p1.jsonl.
    """
    v, a = sans_etiquettes(valeurs, attributs)
    return systeme_c2(v, a)


def systeme_c3e(valeurs, attributs, indices_contexte, reponses, items, table,
                toutes_etiquettes=True):
    """Prompt de C3 avec l'etiquette demographique en tete du persona.

    toutes_etiquettes=True  : les 11 attributs, ideologie et parti compris. C'est C3E.
    toutes_etiquettes=False : les 9 autres. C'est C3ES.

    Le bloc demographique est le corps exact de systeme_c2, le bloc de reponses le corps
    exact de systeme_c3. C'est ce recollage, et lui seul, qui autorise la phrase « a
    information de la personne constante, seule l'etiquette bouge ».
    """
    if toutes_etiquettes:
        demo = systeme_c2(valeurs, attributs)
    else:
        demo = systeme_c2s(valeurs, attributs)
    rep = systeme_c3(indices_contexte, reponses, items, table)
    return PREAMBULE + "\n\n" + corps(demo) + "\n\n" + corps(rep) + "\n\n" + CONSIGNE


# ---------------------------------------------------------------------------
# 2. Enumeration des appels
# ---------------------------------------------------------------------------

def colonnes_familles(items):
    """Les 58 colonnes des six familles de a2, triees. Memes items que R2."""
    return sorted({j for _nom, cols in groupes_familles(items) for j in cols})


def travaux_r3(condition, retenus, items, blocs, y1, x, attributs, table, cols_familles):
    """Enumere les appels, dans l'ordre qui maximise le cache de prefixe.

    C3E et C3ES : le prompt systeme depend de la personne ET du bloc secret, exactement
        comme C3 en a5. Cinq prefixes par personne, et seuls les items de FAMILLE du bloc
        sont predits, 58 au total au lieu de 149. C'est ce qui rend C3E et C3 apparies
        cellule a cellule sur les memes 58 items.
    C2S : le prompt systeme ne depend que de la personne. Un seul prefixe, court, puis
        les 58 items.

    Les personnes sont parcourues dans l'ordre de a5-personnes.csv : une troncature a la
    fin dure coute des personnes entieres, jamais des items, et les perimetres des trois
    conditions sont emboites.
    """
    tous = np.arange(len(items))
    cibles = set(cols_familles)
    for p in retenus:
        if condition in ("C3E", "C3ES"):
            complete = (condition == "C3E")
            for i_bloc, bloc in enumerate(blocs):
                dedans = [int(j) for j in bloc if int(j) in cibles]
                if not dedans:
                    continue
                contexte = np.setdiff1d(tous, bloc)
                sys_txt = systeme_c3e(x[p["index"]], attributs, contexte,
                                      y1[p["index"]], items, table,
                                      toutes_etiquettes=complete)
                for j in dedans:
                    yield p, i_bloc, j, sys_txt
        elif condition == "C2S":
            sys_txt = systeme_c2s(x[p["index"]], attributs)
            for j in cols_familles:
                yield p, 0, int(j), sys_txt
        else:
            raise SystemExit(f"condition inconnue : {condition}")


def chemin_trace(condition, suffixe=""):
    nom = f"r3-{condition}-{CLE_MODELE}"
    if suffixe:
        nom += "-" + suffixe
    return os.path.join(TRACES, nom + ".jsonl")


def index_existant(chemin):
    """Cle (pid, item) des appels deja ecrits. Une relance ne les refait pas.

    Les lignes tronquees par un arret brutal sont ignorees sans faire echouer la
    reprise : la derniere ligne d'un fichier interrompu en cours d'ecriture est souvent
    incomplete. Meme convention que a5 et R2.
    """
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
            if "pid" in d and "item" in d:
                fait.add((d["pid"], d["item"]))
    return fait


def personnes_completes(chemin, n_items_attendu=58):
    """Personnes dont les 58 cellules sont dans la trace. Sert au compte rendu."""
    compte = {}
    if not os.path.exists(chemin):
        return 0, 0
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            if "pid" in d:
                compte[d["pid"]] = compte.get(d["pid"], 0) + 1
    return (sum(1 for v in compte.values() if v >= n_items_attendu), len(compte))


# ---------------------------------------------------------------------------
# 3. Sonde de cout et smoke test
# ---------------------------------------------------------------------------

def mesurer_couts(moteur, spec, enumeration, items, table, n, condition, fh=None,
                  ids_par_k=None):
    """n appels reels, et les deux couts qui font une projection honnete.

    Deux postes et pas un : le prefixe de persona, paye une fois par prompt systeme
    nouveau, et l'appel servi par le cache. Les moyenner en un seul debit se trompe d'un
    facteur deux entre C3E, dont le prefixe pese ~8 s, et C2S, dont le prefixe est court.
    Le partage entre les deux postes se lit sur `tokens_calcules`, que llama-server
    remonte : au dessus de 500 tokens recalcules, le prefixe a ete paye.
    """
    masses, absents, prefixes, servis = [], 0, [], []
    ids_par_k = {} if ids_par_k is None else ids_par_k
    t0 = time.time()
    for p, groupe, j, sys_txt in enumeration:
        if len(masses) >= n:
            break
        nom = items[j]
        bloc_user, options = utilisateur(nom, table)
        prompt = construire_prompt(spec, sys_txt, bloc_user, VARIANTE)
        k = len(options)
        if k not in ids_par_k:
            ids_par_k[k], _ = tokens_des_lettres(moteur, prompt, k, VARIANTES[VARIANTE])
            journal(f"  tokens verifies pour K={k} : {ids_par_k[k]}")
        r = un_appel(moteur, VARIANTE, prompt, options, ids_par_k[k])
        masses.append(r["masse_lettres"])
        if r["modalites_absentes"]:
            absents += 1
        tc = r["tokens_calcules"] or 0
        (prefixes if tc > 500 else servis).append(r["duree_ms"])
        if fh is not None:
            fh.write(json.dumps({"pid": p["pid"], "item": nom, "condition": condition,
                                 "groupe": str(groupe), "variante": VARIANTE,
                                 "modele": spec["nom"], **r}, ensure_ascii=False) + "\n")
            fh.flush()
    return {
        "masses": masses, "absents": absents, "duree_s": time.time() - t0,
        "prefixes_payes": len(prefixes),
        "ms_prefixe_median": float(np.median(prefixes)) if prefixes else float("nan"),
        "ms_appel_servi_median": float(np.median(servis)) if servis else float("nan"),
    }


def smoke_test(moteur, spec, enumeration, items, table, n=N_SMOKE):
    """Vingt appels reels de C3E avant d'engager la nuit, dans une trace a part.

    Le verdict est celui de R2, importe tel quel : mediane des masses au dessus de 0,90,
    minimum au dessus de 0,50, moins de 25 pour cent d'appels a modalite absente. La
    trace de smoke test est un fichier distinct, elle ne se melange jamais a la trace du
    run.
    """
    chemin = chemin_trace("smoke")
    with open(chemin, "a", encoding="utf-8") as fh:
        c = mesurer_couts(moteur, spec, enumeration, items, table, n, "smoke", fh)
    ok, mesures, motif = verdict_smoke(c["masses"], c["absents"], n_attendu=n)
    mesures.update({k: v for k, v in c.items() if k != "masses"})
    mesures["trace"] = chemin
    return ok, mesures, motif


# ---------------------------------------------------------------------------
# 4. Le run
# ---------------------------------------------------------------------------

def lancer(moteur, spec, condition, retenus, items, blocs, y1, x, attributs, table,
           cols_familles, fin_ts, limite=None, journal_tous=200):
    """Execute une condition de bout en bout et ecrit la trace au fil de l'eau.

    Ecriture incrementale avec flush a chaque ligne et fsync tous les 200 appels : le
    script doit survivre a un arret brutal, et il est ecrit pour etre interrompu par
    SIGINT sans perdre une ligne.
    """
    chemin = chemin_trace(condition)
    fait = index_existant(chemin)
    journal(f"[{condition}] trace {chemin}, {len(fait)} appels deja faits")

    ids_par_k = {}
    n_appels, n_rejets, n_absents = 0, 0, 0
    personnes_vues = set()
    t0 = time.time()
    tronque = False

    with open(chemin, "a", encoding="utf-8") as fh:
        for p, groupe, j, sys_txt in travaux_r3(condition, retenus, items, blocs, y1, x,
                                                attributs, table, cols_familles):
            nom = items[j]
            if (p["pid"], nom) in fait:
                continue
            if time.time() >= fin_ts:
                journal(f"[{condition}] fin atteinte, arret propre")
                tronque = True
                break
            if limite is not None and n_appels >= limite:
                journal(f"[{condition}] limite de {limite} appels atteinte")
                tronque = True
                break

            bloc_user, options = utilisateur(nom, table)
            prompt = construire_prompt(spec, sys_txt, bloc_user, VARIANTE)
            k = len(options)
            if k not in ids_par_k:
                ids_par_k[k], _ = tokens_des_lettres(moteur, prompt, k,
                                                     VARIANTES[VARIANTE])
                journal(f"  tokens verifies pour K={k} : {ids_par_k[k]}")

            r = un_appel(moteur, VARIANTE, prompt, options, ids_par_k[k])
            if r["modalites_absentes"]:
                n_absents += 1
            if r["rejet"]:
                n_rejets += 1

            ligne = {
                "pid": p["pid"], "item": nom, "condition": condition, "passe": 1,
                "pli": p["pli"], "bloc": groupe,
                "version_prompt": f"r3-p1-{CLE_MODELE}-{VARIANTE}",
                "modele": spec["nom"], "quantification": spec["quantification"],
                "gabarit": spec["gabarit"], "variante_fin": VARIANTE,
                "ordre_modalites": "nomenclature",
                **r,
            }
            fh.write(json.dumps(ligne, ensure_ascii=False) + "\n")
            fh.flush()
            n_appels += 1
            personnes_vues.add(p["pid"])

            if n_appels % journal_tous == 0:
                ecoule = time.time() - t0
                os.fsync(fh.fileno())
                journal(f"  {condition} : {n_appels} appels, "
                        f"{n_appels / ecoule * 3600:,.0f}/h, rejets {n_rejets}, "
                        f"{len(personnes_vues)} personnes, "
                        f"{datetime.datetime.now():%H:%M:%S}".replace(",", " "))
        os.fsync(fh.fileno())

    ecoule = max(time.time() - t0, 1e-9)
    complets, touchees = personnes_completes(chemin, len(cols_familles))
    return {
        "condition": condition, "appels": n_appels, "deja_faits": len(fait),
        "secondes": ecoule, "tronque": tronque,
        "appels_par_heure": n_appels / ecoule * 3600 if n_appels else 0.0,
        "rejets": n_rejets, "appels_avec_modalite_absente": n_absents,
        "personnes_touchees": len(personnes_vues),
        "personnes_completes": complets, "personnes_dans_la_trace": touchees,
        "trace": chemin,
    }


# ---------------------------------------------------------------------------
# 5. Verification hors ligne, sans serveur
# ---------------------------------------------------------------------------

def verification_seule(args, spec, retenus, items, blocs, y1, x, attributs, table,
                       cols_familles):
    """Les dix verifications de la page de plan section 7. Aucun serveur n'est allume."""
    ok_global = True

    def dire(nom, ok, detail=""):
        nonlocal ok_global
        ok_global = ok_global and bool(ok)
        journal(f"  [{'ok' if ok else 'ECHEC'}] {nom}" + (f" : {detail}" if detail else ""))

    journal("\n--- 1. Echantillon et perimetre ---")
    chemin_personnes = os.path.join(TRACES, "a5-personnes.csv")
    if os.path.exists(chemin_personnes):
        ech = pd.read_csv(chemin_personnes)
        dire("echantillon identique a a5-personnes.csv",
             list(ech["pid"]) == [p["pid"] for p in retenus],
             f"{len(retenus)} personnes, {len(retenus) // N_PLIS} par pli")
    else:
        dire("a5-personnes.csv present", False, "fichier absent")
    dire("58 items de famille", len(cols_familles) == 58, f"{len(cols_familles)} items")
    repartition = [len([j for j in b if int(j) in set(cols_familles)]) for b in blocs]
    dire("repartition sur les cinq blocs", repartition == [10, 12, 14, 10, 12],
         str(repartition))
    dire("cinq prefixes par personne pour C3E", all(r > 0 for r in repartition),
         "aucun bloc sans item de famille")

    journal("\n--- 2. Les prompts, par egalite de chaines ---")
    p0 = retenus[0]
    tous = np.arange(len(items))
    bloc0 = blocs[0]
    contexte0 = np.setdiff1d(tous, bloc0)
    demo11 = systeme_c2(x[p0["index"]], attributs)
    rep = systeme_c3(contexte0, y1[p0["index"]], items, table)
    c3e = systeme_c3e(x[p0["index"]], attributs, contexte0, y1[p0["index"]], items, table)
    c3es = systeme_c3e(x[p0["index"]], attributs, contexte0, y1[p0["index"]], items, table,
                       toutes_etiquettes=False)
    c2s = systeme_c2s(x[p0["index"]], attributs)

    dire("C3E contient le corps exact de systeme_c2", corps(demo11) in c3e)
    dire("C3E contient le corps exact de systeme_c3", corps(rep) in c3e)
    dire("C3E est bien l'enveloppe de a5", c3e.startswith(PREAMBULE)
         and c3e.endswith(CONSIGNE))
    dire("C3E = preambule + demo + reponses + consigne, sans un caractere de plus",
         c3e == PREAMBULE + "\n\n" + corps(demo11) + "\n\n" + corps(rep) + "\n\n"
         + CONSIGNE)
    libelles = list(ETIQUETTES_DEMOGRAPHIQUES.values())
    manquants = [lib for lib in libelles if f"- {lib}: " not in c3e]
    dire("C3E porte les 11 libelles demographiques", not manquants,
         "manquants : " + ", ".join(manquants) if manquants else "les 11 sont presents")
    ordre = [c3e.index(f"- {lib}: ") for lib in libelles]
    dire("les 11 lignes sont dans l'ordre de a5", ordre == sorted(ordre))
    dire("le bloc demographique precede les reponses",
         c3e.index("Here is what is known about this person")
         < c3e.index("Here is how this person answered"))

    journal("\n--- 3. L'item cible et son bloc sont hors du prompt ---")
    cibles_bloc = [int(j) for j in bloc0 if int(j) in set(cols_familles)]
    fuites = []
    for j in cibles_bloc[:5]:
        q = table[items[j]]["question"]
        if f"Q: {q}\n" in c3e:
            fuites.append(items[j])
    dire("aucun item du bloc secret dans le contexte de C3E", not fuites,
         "fuites : " + ", ".join(fuites) if fuites else
         f"{len(cibles_bloc)} items cibles testes sur le premier bloc")
    n_qa = c3e.count("\nQ: ")
    dire("le contexte de C3E compte les items hors bloc", 100 <= n_qa <= 125,
         f"{n_qa} paires question reponse (attendu ~119 moins les manquantes)")
    dire("C3E et C3 ont le meme bloc de reponses",
         c3e.count("\nQ: ") == rep.count("\nQ: "))

    journal("\n--- 4. C2S, l'ablation dans le regime pauvre ---")
    dire("C2S ne contient pas Political ideology", "Political ideology" not in c2s)
    dire("C2S ne contient pas Political party", "Political party" not in c2s)
    dire("C2S a neuf lignes d'attributs", c2s.count("\n- ") == 9,
         f"{c2s.count(chr(10) + '- ')} lignes")
    lignes_c2 = [l for l in demo11.splitlines() if l.startswith("- ")]
    lignes_c2s = [l for l in c2s.splitlines() if l.startswith("- ")]
    attendues = [l for l in lignes_c2
                 if not l.startswith("- Political ideology:")
                 and not l.startswith("- Political party:")]
    dire("les neuf lignes de C2S sont celles de C2, caractere pour caractere",
         lignes_c2s == attendues)
    dire("C2S est C2 moins exactement deux lignes",
         len(lignes_c2) - len(lignes_c2s) == 2)
    dire("C2S ne contient aucune reponse d'enquete", "\nQ: " not in c2s)
    dire("C3ES ne contient ni ideologie ni parti",
         "Political ideology" not in c3es and "Political party" not in c3es)
    dire("C3ES contient bien les reponses", corps(rep) in c3es)

    journal("\n--- 5. Enumeration et volumes ---")
    for cond, attendu_pref in (("C3E", 5), ("C2S", 1), ("C3ES", 5)):
        enum = travaux_r3(cond, retenus[:2], items, blocs, y1, x, attributs, table,
                          cols_familles)
        vus = list(enum)
        prompts = {id(s) for _p, _g, _j, s in vus}
        par_personne = len(vus) // 2
        dire(f"{cond} : 58 appels par personne", par_personne == 58, f"{par_personne}")
        dire(f"{cond} : {attendu_pref} prompts systeme par personne",
             len(prompts) == attendu_pref * 2, f"{len(prompts) // 2}")
        items_vus = {items[j] for _p, _g, j, _s in vus}
        dire(f"{cond} : les items sont ceux des familles",
             items_vus == {items[j] for j in cols_familles})

    journal("\n--- 6. Reprise sur trace tronquee ---")
    essai = os.path.join(TRACES, "r3-essai-reprise.jsonl")
    with open(essai, "w", encoding="utf-8") as fh:
        fh.write(json.dumps({"pid": "X", "item": "abany", "condition": "C3E"}) + "\n")
        fh.write('{"pid": "Y", "item": "abde')          # ligne coupee
    fait = index_existant(essai)
    dire("l'index ignore la ligne tronquee", fait == {("X", "abany")}, str(fait))
    os.remove(essai)

    journal("\n--- 7. Fin dure, epoch avec le jour ---")
    ts, dt = heure_de_fin("08:00")
    dire("la fin dure est dans le futur", ts > time.time(),
         f"{dt:%Y-%m-%d %H:%M:%S}, dans {(ts - time.time()) / 3600:.2f} h")
    ts2, dt2 = heure_de_fin("00:01")
    dire("une heure deja passee bascule au lendemain", ts2 > time.time(),
         f"{dt2:%Y-%m-%d %H:%M:%S}")

    journal("\n--- 8. Verdict du smoke test sur des masses synthetiques ---")
    cas = [("bon", [0.99] * 20, 0, True),
           ("mediane basse", [0.80] * 20, 0, False),
           ("un minimum bas", [0.99] * 19 + [0.10], 0, False),
           ("trop de modalites absentes", [0.99] * 20, 8, False),
           ("pas assez d'appels", [0.99] * 5, 0, False)]
    for nom, masses, absents, attendu in cas:
        ok, _mes, motif = verdict_smoke(masses, absents, n_attendu=20)
        dire(f"verdict « {nom} »", ok == attendu, motif)

    journal("\n--- 9. Registre du modele et machine ---")
    dire("le fichier GGUF de a5 existe", os.path.exists(spec["fichier"]), spec["fichier"])
    dire("le modele est celui de C2 et C3", spec["nom"] == "Qwen3-4B-Instruct-2507",
         f"{spec['nom']} {spec['quantification']}, gabarit {spec['gabarit']}")
    dire("la variante de fin est celle de a5", VARIANTE == "answer",
         "le prompt s'arrete sur `Answer:` sans espace")
    pids = serveurs_en_cours()
    journal(f"  [info] llama-server en cours : {pids if pids else 'aucun'} "
            f"(le run refusera de demarrer s'il y en a un)")

    journal("\n--- 10. Traces de reference du contraste ---")
    for f in ("a5-C3-p1.jsonl", "a5-C2-p1.jsonl"):
        chemin = os.path.join(TRACES, f)
        dire(f"trace de reference {f}", os.path.exists(chemin),
             f"{os.path.getsize(chemin) / 1e6:.1f} Mo" if os.path.exists(chemin)
             else "absente")

    journal("\n--- Projection avec les couts mesures en a5 ---")
    # 5 P + 149 A = 109,8 s (C3, 22 350 appels en 274,5 min sur 150 personnes)
    # 6 P +  58 A =  77,7 s (C3F, 3 498 appels en 78,1 min sur 60,3 personnes)
    p_s, a_s = 8.62, 0.4477
    for cond, npref, cout_pref in (("C3E", 5, p_s), ("C3ES", 5, p_s), ("C2S", 1, 0.5)):
        par_personne = npref * cout_pref + 58 * (a_s if cond != "C2S" else 0.272)
        journal(f"  {cond} : {par_personne:.0f} s par personne, "
                f"{par_personne * 150 / 3600:.2f} h pour 150 personnes [ESTIMATION]")
    journal("  la projection sera refaite sur mesure au smoke test et par une sonde de "
            "six appels sur C2S, avant le premier appel utile")

    return ok_global


# ---------------------------------------------------------------------------

def main():
    global _journal_fh
    ap = argparse.ArgumentParser()
    ap.add_argument("--conditions", default="C3E,C2S,C3ES",
                    help="liste ordonnee parmi C3E, C2S, C3ES")
    ap.add_argument("--personnes", type=int, default=150)
    ap.add_argument("--fin", default="08:00", help="fin dure du calcul, heure locale")
    ap.add_argument("--port", type=int, default=0, help="0 pour choisir un port libre")
    ap.add_argument("--contexte", type=int, default=8192, help="tokens par slot")
    ap.add_argument("--parallele", type=int, default=8, help="-np, 8 en configuration a3")
    ap.add_argument("--verification-seule", action="store_true",
                    help="tout verifier sans allumer de serveur")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal d'appels par condition, pour un essai")
    ap.add_argument("--sans-cache-kv-8bits", action="store_true",
                    help="repli si le serveur refuse le cache KV quantifie")
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)
    nom_log = "r3-verification.log" if args.verification_seule else "r3-run.log"
    chemin_log = os.path.join(TRACES, nom_log)
    if not sortie_est_deja(chemin_log):
        _journal_fh = open(chemin_log, "a", encoding="utf-8")

    spec = MODELES[CLE_MODELE]
    journal("=" * 78)
    journal("popsim R3, la vraie ablation de l'etiquette, a un seul facteur.")
    journal(f"demarrage {datetime.datetime.now():%Y-%m-%d %H:%M:%S}, PID {os.getpid()}")
    journal("page de plan : resultats/r3-preenregistrement.md, "
            "8 septembre 2026 22:30:01 CEST")
    journal(f"modele : {spec['nom']} {spec['quantification']}, gabarit {spec['gabarit']}, "
            f"variante de fin {VARIANTE}, coupure publiee {spec['coupure_publiee']}")
    journal(f"charge machine : {os.getloadavg()}")

    # --------------------------------------------------- donnees et echantillon
    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    plis, blocs = grille(len(ids), len(items), GRAINE)
    par_pli = max(1, args.personnes // N_PLIS)
    retenus = echantillon(ids, plis, par_pli, graine=GRAINE_ECHANTILLON)

    chemin_personnes = os.path.join(TRACES, "a5-personnes.csv")
    if os.path.exists(chemin_personnes):
        ech = pd.read_csv(chemin_personnes)
        attendus = list(ech["pid"])
        obtenus = [p["pid"] for p in retenus]
        if attendus != obtenus:
            journal(f"ATTENTION : l'echantillon retire differe de {chemin_personnes}, "
                    f"le fichier fait foi")
            par_pid = {p["pid"]: p for p in retenus}
            retenus = [par_pid[p] if p in par_pid else
                       {"pid": r.pid, "index": int(r.index), "pli": int(r.pli)}
                       for p, r in zip(attendus, ech.itertuples())]
        else:
            journal(f"echantillon identique a {chemin_personnes} : {len(retenus)} "
                    f"personnes, {par_pli} par pli [CONTROLE]")

    cols_familles = colonnes_familles(items)
    journal(f"{len(retenus)} personnes, {len(cols_familles)} items de famille, "
            f"{len(retenus) * len(cols_familles)} appels par condition")

    if args.verification_seule:
        ok = verification_seule(args, spec, retenus, items, blocs, y1, x, attributs,
                                table, cols_familles)
        journal(f"\nVERIFICATION {'PASSEE' if ok else 'ECHOUEE'} "
                f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S}")
        sys.exit(0 if ok else 1)

    # --------------------------------------------------- un seul serveur a la fois
    pids = serveurs_en_cours()
    if pids:
        journal(f"arret : un llama-server tourne deja, PID {pids}. Deux serveurs sur ce "
                f"GPU s'effondrent mutuellement, facteur 9,5 mesure en a5 section 4.4.")
        sys.exit(1)
    if not os.path.exists(spec["fichier"]):
        journal(f"arret : modele introuvable, {spec['fichier']}")
        sys.exit(1)

    fin_ts, fin_dt = heure_de_fin(args.fin)
    journal(f"fin dure a {fin_dt:%Y-%m-%d %H:%M:%S} (epoch {int(fin_ts)}), dans "
            f"{(fin_ts - time.time()) / 3600:.2f} h")

    with open(os.path.join(TRACES, "r3-run.pid"), "w") as fh:
        fh.write(str(os.getpid()))

    port = args.port or premier_port_libre(depart=8300)
    if not port_libre(port):
        journal(f"arret : le port {port} est occupe")
        sys.exit(1)
    journal(f"llama-server sur le port {port}, -np {args.parallele}, "
            f"-c {args.contexte * args.parallele}, "
            f"KV {'f16' if args.sans_cache_kv_8bits else 'q8_0'}")

    moteur = MoteurA5(spec["fichier"], contexte=args.contexte, parallele=args.parallele,
                      port=port, cache_kv_8bits=not args.sans_cache_kv_8bits)
    try:
        moteur.demarrer()
    except RuntimeError as e:
        journal(f"le serveur n'a pas demarre avec le cache KV quantifie : {e}")
        journal("second essai sans cache KV quantifie")
        moteur = MoteurA5(spec["fichier"], contexte=args.contexte,
                          parallele=args.parallele, port=port, cache_kv_8bits=False)
        moteur.demarrer()
    journal(f"serveur pret en {moteur.chargement_s:.1f} s")

    codes = [c.strip() for c in args.conditions.split(",") if c.strip()]
    resume, projections, mes, sonde_c2s = [], {}, {}, {}
    try:
        # ------------------------------------------- smoke test integre, 20 appels
        journal(f"smoke test : {N_SMOKE} appels reels de C3E avant d'engager la nuit")
        enum = travaux_r3("C3E", retenus, items, blocs, y1, x, attributs, table,
                          cols_familles)
        ok, mes, motif = smoke_test(moteur, spec, enum, items, table)
        journal(f"  masse mediane {mes['masse_mediane']:.4f}, minimale "
                f"{mes['masse_minimale']:.4f}, modalites absentes "
                f"{mes['part_modalites_absentes']:.2f}, duree {mes['duree_s']:.0f} s")
        journal(f"  prefixe median {mes['ms_prefixe_median']:.0f} ms sur "
                f"{mes['prefixes_payes']} prefixes payes, appel servi par le cache "
                f"{mes['ms_appel_servi_median']:.0f} ms")
        journal(f"  {motif}")
        if not ok:
            journal("le run ne demarre pas. Le gabarit de a5 ne rend plus la masse "
                    "attendue, et une nuit d'appels serait du bruit renormalise.")
            sys.exit(2)

        # ------------------------------------------- sonde de cout de C2S, 6 appels
        # Le prompt de C2S est court : son prefixe ne coute pas celui de C3E, et le
        # projeter avec le cout mesure sur C3E donnerait une reserve trois fois trop
        # grande, qui mangerait H1 pour sauver H2.
        journal("sonde de cout de C2S : 6 appels, prompt court")
        enum_c2s = travaux_r3("C2S", retenus, items, blocs, y1, x, attributs, table,
                              cols_familles)
        with open(chemin_trace("smoke"), "a", encoding="utf-8") as fh:
            sonde_c2s = mesurer_couts(moteur, spec, enum_c2s, items, table, 6,
                                      "sonde-C2S", fh)
        journal(f"  C2S : prefixe median {sonde_c2s['ms_prefixe_median']:.0f} ms, "
                f"appel servi {sonde_c2s['ms_appel_servi_median']:.0f} ms")

        # ------------------------------------------- projections et partage du budget
        budget_h = (fin_ts - time.time()) / 3600.0
        # Le prompt de C2S fait 501 caracteres : son prefixe tient sous le seuil de 500
        # tokens recalcules qui distingue « prefixe paye » de « appel servi », et la
        # mediane des prefixes revient donc vide. Sans ce repli, la projection vaudrait
        # NaN, la reserve aussi, et la fin intermediaire de C3E deviendrait NaN, ce qui
        # ferait tourner C3E au dela de la fin dure : une comparaison a NaN est toujours
        # fausse. Le repli prend le cout d'un appel servi, qui majore le cout d'un
        # prefixe court.
        couts_c2s = dict(sonde_c2s)
        if not np.isfinite(couts_c2s.get("ms_prefixe_median", float("nan"))):
            couts_c2s["ms_prefixe_median"] = couts_c2s.get("ms_appel_servi_median",
                                                           float("nan"))
            journal("  prefixe de C2S non mesurable (prompt court) : repli sur le cout "
                    "d'un appel servi")
        projections["C3E"] = projeter(mes, len(retenus), 5, len(cols_familles))
        projections["C3ES"] = projeter(mes, len(retenus), 5, len(cols_familles))
        projections["C2S"] = projeter(couts_c2s, len(retenus), 1, len(cols_familles))
        for cond, pr in projections.items():
            journal(f"projection {cond} : {pr['secondes_par_personne']:.0f} s par "
                    f"personne, {pr['appels_par_heure']:,.0f} appels/h, "
                    f"{pr['heures_pour_toutes']:.2f} h pour {len(retenus)} personnes"
                    .replace(",", " "))

        reserve_h = 0.0
        if "C2S" in codes and "C3E" in codes:
            brute = projections["C2S"]["heures_pour_toutes"] * MARGE_RESERVE
            if np.isfinite(brute):
                reserve_h = min(brute, budget_h * PART_MAX_RESERVE)
            else:
                # Projection non mesurable : la reserve vaut la projection de la page de
                # plan, 0,7 h, plafonnee comme les autres. Elle n'est jamais NaN.
                reserve_h = min(0.7 * MARGE_RESERVE, budget_h * PART_MAX_RESERVE)
                journal("  projection de C2S non mesurable, reserve prise dans la page "
                        "de plan (0,7 h) [ESTIMATION]")
            journal(f"budget {budget_h:.2f} h. Reserve pour C2S : {reserve_h:.2f} h "
                    f"(projection x {MARGE_RESERVE}, plafond {PART_MAX_RESERVE:.0%} du "
                    f"budget). Regle de la page de plan section 3.")
        fins = {c: fin_ts for c in codes}
        if reserve_h > 0:
            fins["C3E"] = fin_ts - reserve_h * 3600.0
            journal(f"  fin intermediaire de C3E : "
                    f"{datetime.datetime.fromtimestamp(fins['C3E']):%H:%M:%S}")
        # Aucune fin ne peut etre NaN ni depasser la fin dure : une comparaison a NaN est
        # toujours fausse, et la boucle d'appels ne s'arreterait jamais.
        for c in list(fins):
            if not np.isfinite(fins[c]) or fins[c] > fin_ts:
                fins[c] = fin_ts
        sp = projections["C3E"]["secondes_par_personne"]
        if np.isfinite(sp) and sp > 0:
            couvertes = min(len(retenus),
                            int(max(fins.get("C3E", fin_ts) - time.time(), 0) / sp))
            journal(f"  C3E couvrira environ {couvertes} personnes sur {len(retenus)} "
                    f"[ESTIMATION]")

        # ------------------------------------------- la file
        for code in codes:
            if code not in ("C3E", "C2S", "C3ES"):
                journal(f"condition inconnue, ignoree : {code}")
                continue
            if time.time() >= fin_ts:
                journal(f"fin dure atteinte avant le lancement de {code}")
                break
            r = lancer(moteur, spec, code, retenus, items, blocs, y1, x, attributs,
                       table, cols_familles, min(fins.get(code, fin_ts), fin_ts),
                       limite=args.limite)
            resume.append(r)
            journal(f"[{code}] {r['appels']} appels en {r['secondes'] / 60:.1f} min, "
                    f"{r['appels_par_heure']:,.0f} appels/h, {r['rejets']} rejets, "
                    f"{r['personnes_completes']} personnes completes sur "
                    f"{r['personnes_dans_la_trace']} touchees".replace(",", " "))
    except KeyboardInterrupt:
        journal("SIGINT recu : arret propre demande. La trace est resumable.")
    finally:
        # Le serveur est arrete quoi qu'il arrive : deux llama-server ne doivent jamais
        # tourner en meme temps sur cette machine.
        try:
            moteur.arreter()
        except Exception as e:
            journal(f"arret du serveur : {e}")
        journal(f"serveur arrete. charge machine : {os.getloadavg()}")

    chemin_resume = os.path.join(TRACES, f"r3-resume-{CLE_MODELE}.json")
    with open(chemin_resume, "w", encoding="utf-8") as fh:
        json.dump({"fin_dure": fin_dt.isoformat(), "port": port,
                   "modele": spec["nom"], "quantification": spec["quantification"],
                   "gabarit": spec["gabarit"], "variante_fin": VARIANTE,
                   "etiquettes_retirees": list(ETIQUETTES_RETIREES),
                   "smoke": {k: v for k, v in mes.items() if k != "trace"},
                   "sonde_c2s": {k: v for k, v in sonde_c2s.items() if k != "masses"},
                   "projections": projections,
                   "personnes": len(retenus), "items": len(cols_familles),
                   "conditions": resume}, fh, indent=2, ensure_ascii=False, default=str)
    journal(f"resume ecrit : {chemin_resume}")
    journal(f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S}")


if __name__ == "__main__":
    main()
