"""
r4_oracle_socle : l'oracle des camps sur le modele socle, et la part du format d'invite.

Statut : script d'experience, pas du code de production. Il repond a la question 4 de
`resultats/r1-oracle-des-camps.md` (« Faut il un modele socle dans le lot ? ») et a la
ligne « un modele socle » du tableau 5.3 de `resultats/r1-resultats.md`.

Ce qu'il fait, et ce qu'il ne fait pas. Il rejoue EXACTEMENT le plan de cellules de r1
(149 items du GSS x 3 camps x 2 identites de demandeur, mode « describe ») sur deux
conditions nouvelles, plus une troisieme conditionnelle :

  q4base   Qwen3-4B-Base, un modele SOCLE, en completion a trois exemples ;
  q4nogab  Qwen3-4B-Instruct-2507, LE MEME FICHIER GGUF que la condition q4 de r1,
           en completion a trois exemples, sans gabarit de conversation ;
  q4hyb    Qwen3-4B, l'instruit APPARIE au socle selon a27 section 4.4, meme format.

La quatrieme condition de la comparaison, q4 sous gabarit ChatML, n'est pas rejouee :
ce sont les 894 cellules deja ecrites dans data/traces/r1-q4.jsonl.

Le contraste q4nogab contre q4 tient les poids fixes et ne change que le format : il
mesure ce que le format d'invite porte a lui seul. a27 section 4.4 mesure chez les auteurs
de 2607.25292 que ce seul changement vaut 0,081 de distance de variation totale, « du meme
ordre que l'ecart base contre instruct de la famille Llama, 0,15 », soit la moitie. Sans
cette condition, tout l'ecart socle contre instruit serait attribue aux poids, et la
moitie serait fausse.

Ce que ce run NE tranche PAS : la contamination. Un socle a lu le meme internet qu'un
instruit. Il separe « le post entrainement fabrique le portrait » de « le portrait est
deja dans les poids » ; il ne separe pas « le modele a lu le sondage » du reste. Seule la
mesure --h4 s'attaque a la seconde, et seulement par un signe indirect.

Relance et arret : `--sans-relance` est transmis a r1_oracle_camps.lancer() et supprime la
seconde tentative (r5-preenregistrement.md section « Relance ») ; le defaut conserve le
comportement de la nuit du 8 au 9, pour que R4 se rejoue au caractere pres. `touch
data/traces/STOP` arrete le run entre deux appels, trace fermee, resume ecrit, code 0.

Rien n'est recopie de r1_oracle_camps.py : ses fonctions sont importees et appelees. Le
seul ajout est un gabarit de plus, « completion-3ex », injecte dans son registre en
memoire. Aucun fichier existant du depot n'est modifie.

Page de plan : resultats/r4-preenregistrement.md, ecrite AVANT le premier appel.

Entree  : data/modeles/gguf/*.gguf, non versionne.
          data/traces/r1-distributions-reelles.csv, le referent humain de r1, reutilise
          tel quel et jamais reecrit.
          data/gss-panel/gss2020panel_r1a.dta, pour --h4 seulement.
Sortie  : data/traces/r1-<cle>-r4.jsonl, une ligne par appel, non versionne.
          data/traces/r1-q4-r4.jsonl, copie octet pour octet de r1-q4.jsonl.
          data/traces/r4-resume.json, data/traces/r4-run.log.
          resultats/r4-h4-restitution.csv, pour --h4.

Rien ne sort de la machine. Aucun appel distant.

Usage :
  .venv/bin/python analyses/r4_oracle_socle.py --verifier          # hors ligne, sans serveur
  .venv/bin/python analyses/r4_oracle_socle.py --modele q4base,q4nogab,q4hyb --fin 10:00
  .venv/bin/python analyses/r4_oracle_socle.py --evaluer
  .venv/bin/python analyses/r4_oracle_socle.py --h4

Reprise : l'index unique est (version_prompt, item, camp, identite) dans le fichier du
modele, mecanisme de r1 inchange. Une relance ne refait aucun appel deja ecrit.
"""

import argparse
import collections
import datetime
import hashlib
import json
import os
import shutil
import sys
import time

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import r1_oracle_camps as R1
from a2_baselines_gss import charger, FAMILLES
from a5_agents_locaux_gss import (LETTRES, heure_de_fin, nomenclature, port_libre,
                                  premier_port_libre)
from a30_commun import GSS_BLOC3

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRACES = os.path.join(RACINE, "data/traces")
SORTIE = os.path.join(RACINE, "resultats")
GGUF = os.path.join(RACINE, "data/modeles/gguf")
PANEL = os.path.join(RACINE, "data/gss-panel")

# Suffixe de fichier de toute la seance. Il donne data/traces/r1-<cle>-r4.jsonl, ce qui
# est exactement ce que r1_evaluer.py --suffixe r4 va chercher, sans une modification de
# l'evaluateur.
SUFFIXE = "r4"

# Version du gabarit d'invite. Elle DOIT differer de « r1-d1 » : deux formats d'invite ne
# se melangent pas dans un meme index de reprise, et la difference doit rester lisible
# ligne par ligne dans la trace.
VERSION_PROMPT = "r4-c3"

GABARIT = "completion-3ex"

# Le referent humain de r1, reutilise tel quel. Son empreinte au lancement de r4 ; le
# critere de chute 6 refuse de tourner si elle a bouge.
REFERENT = os.path.join(TRACES, "r1-distributions-reelles.csv")
REFERENT_SHA = "ea7cd93e8eb3b34d279171ac9a202a0451554afc3d34c7a142dfce761391c811"

JOURNAL = os.path.join(TRACES, "r4-run.log")


# --------------------------------------------------------------------------------------
# 1. Le registre des modeles de r4
# --------------------------------------------------------------------------------------
# Les cles sont ajoutees au registre de r1 EN MEMOIRE, jamais dans le fichier
# r1_oracle_camps.py, qui n'est pas modifie. Sans cet ajout, la figure de r1_evaluer.py
# ignore les cles qu'elle ne connait pas et ne trace rien ; les tableaux, eux, les
# traitent normalement.

MODELES = {
    "q4base": {
        "nom": "Qwen3-4B-Base",
        "fichier": "Qwen3-4B-Base.Q4_K_M.gguf",
        "quantification": "Q4_K_M",
        "gabarit": GABARIT,
        "coupure_publiee": "aucune",
        "type": "socle",
        "depot": "mradermacher/Qwen3-4B-Base-GGUF",
        "sha256": "a7eb1d92eaf34e116f8b522aeeaf4072e66d69b5b10676e0cb7cd9e11889bed6",
        "octets": 2497280736,
    },
    "q4nogab": {
        "nom": "Qwen3-4B-Instruct-2507",
        "fichier": "Qwen3-4B-Instruct-2507-Q4_K_M.gguf",
        "quantification": "Q4_K_M",
        "gabarit": GABARIT,
        "coupure_publiee": "aucune",
        "type": "instruit, sans gabarit de conversation",
        "depot": "unsloth/Qwen3-4B-Instruct-2507-GGUF",
        "sha256": "3605803b982cb64aead44f6c1b2ae36e3acdb41d8e46c8a94c6533bc4c67e597",
        "octets": 2497281120,
    },
    "q4hyb": {
        "nom": "Qwen3-4B",
        "fichier": "Qwen3-4B-Q4_K_M.gguf",
        "quantification": "Q4_K_M",
        "gabarit": GABARIT,
        "coupure_publiee": "aucune",
        "type": "instruit apparie au socle (a27 4.4)",
        "depot": "Qwen/Qwen3-4B-GGUF",
        "sha256": "7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5",
        "octets": 2497280256,
    },
}

ORDRE = ["q4base", "q4nogab", "q4hyb"]


# --------------------------------------------------------------------------------------
# 2. L'invite du socle : completion a trois exemples, sans gabarit de conversation
# --------------------------------------------------------------------------------------
# Protocole de 2607.25292, lu en a27 section 4.4 : « Base models do not reliably follow
# zero-shot instructions, so we use a 3-shot in-context format for V0 on the base model:
# three (Q, A) example pairs followed by the test question ». Leurs exemples sont choisis
# hors du support de la tache testee, pour enseigner le format sans enseigner une reponse.
#
# Les trois exemples ci dessous, figes dans resultats/r4-preenregistrement.md section 3.2 :
#   - aucun item du GSS, aucune enquete reelle : « Millbrook Town Panel » est invente ;
#   - aucun camp politique, aucun nombre reel de camp, les mots liberal, conservative et
#     moderate n'y apparaissent pas ;
#   - trois valeurs de K differentes, 3, 6 et 2, pour enseigner « exactement K lignes » et
#     non « toujours trois lignes » ; les items du GSS vont de K = 2 a K = 12 ;
#   - aucun vecteur uniforme, aucune collision avec repartition_exemple() de r1, dont
#     l'invite de relance se sert.
#
# L'ecart assume avec 2607.25292 : leurs exemples sont hors du support au sens fort, une
# lettre, un entier, une couleur. Les miens gardent la FORME de la tache, un bloc de
# question suivi d'une distribution sur K lettres, parce que c'est cette forme la, avec son
# K variable, qu'il faut enseigner. Ils n'en gardent rien du contenu. Le risque residuel
# est mesure par le critere de chute 2 bis, verifier_recopie_exemples().

SEPARATEUR = "----"

EXEMPLES = [
    {
        "question": ("How often do you use the public library in your neighborhood: "
                     "often, sometimes, or never?"),
        "options": ["Often", "Sometimes", "Never"],
        "reponse": [17, 46, 37],
    },
    {
        "question": "Which of these did you last have for breakfast?",
        "options": ["Toast", "Porridge", "Eggs", "Fruit", "Cereal", "Nothing at all"],
        "reponse": [22, 9, 14, 11, 27, 17],
    },
    {
        "question": "Do you own a bicycle?",
        "options": ["Yes", "No"],
        "reponse": [43, 57],
    },
]

POPULATION_EXEMPLE = "adults in the fictional town of Millbrook"
ENQUETE_EXEMPLE = "Millbrook Town Panel"

# Sans sequences d'arret, un socle enchaine un quatrieme exemple et consomme les 150
# tokens a chaque appel.
ARRETS = ["\n" + SEPARATEUR, "\nSurvey question", "<|endoftext|>", "<|im_end|>",
          "<|im_start|>"]


def bloc_exemple(ex):
    """Un exemple, dans la forme exacte du bloc utilisateur de r1, question inventee.

    La mise en page est celle de r1_oracle_camps.utilisateur() au caractere pres : meme
    en tete, meme liste de modalites, meme phrase de denombrement, meme phrase de format,
    meme gabarit `LETTRE: <percentage>`. Seuls le nom de l'enquete, la population et le
    contenu changent. C'est ce qui fait que le format enseigne est bien celui qui est
    demande ensuite.
    """
    k = len(ex["options"])
    lettres = LETTRES[:k]
    lignes = ["Survey question, " + ENQUETE_EXEMPLE + " wording:",
              '"' + ex["question"] + '"', "", "Answer options:"]
    for lettre, o in zip(lettres, ex["options"]):
        lignes.append(f"{lettre}. {o}")
    lignes += [
        "",
        f"Out of 100 {POPULATION_EXEMPLE}, how many would give each answer?",
        "",
        f"Reply with exactly {k} lines and nothing else: the option letter, a colon, and "
        f"an integer percentage. The {k} percentages must add up to 100.",
    ]
    for lettre in lettres:
        lignes.append(f"{lettre}: <percentage>")
    lignes.append("")
    for lettre, v in zip(lettres, ex["reponse"]):
        lignes.append(f"{lettre}: {v}")
    return "\n".join(lignes)


def prefixe(sys_txt):
    """Le prefixe commun a toutes les cellules d'un couple (camp, identite).

    Il ne depend que de sys_txt, donc il est calcule une fois par groupe de 149 questions
    et entierement servi par le cache de prefixe du serveur, exactement comme en r1.
    """
    morceaux = [sys_txt, "",
                "Here are three worked examples of the required answer format. "
                "They are about unrelated topics.", "", SEPARATEUR, ""]
    for ex in EXEMPLES:
        morceaux += [bloc_exemple(ex), "", SEPARATEUR, ""]
    # Une ligne vide de plus apres le dernier separateur : entre deux exemples il y en a
    # une, et le bloc de la vraie question doit se presenter exactement comme eux.
    morceaux.append("")
    return "\n".join(morceaux)


_gabarit_r1 = R1.gabarit


def gabarit(nom_gabarit, sys_txt, usr_txt):
    """Le gabarit de r1, plus la completion a trois exemples.

    Le texte systeme de r1 et son bloc utilisateur sont repris AU CARACTERE PRES ; seule
    leur mise en forme change. En gabarit de conversation ils occupent deux tours ; ici ils
    sont mis a plat, le systeme en tete comme dans une conversation, le bloc utilisateur en
    dernier, la generation juste apres une ligne vide, comme dans les trois exemples.
    """
    if nom_gabarit == GABARIT:
        return prefixe(sys_txt) + usr_txt + "\n\n"
    return _gabarit_r1(nom_gabarit, sys_txt, usr_txt)


# Injection dans le module de r1, en memoire seulement. r1_oracle_camps.lancer() appelle
# gabarit() et ARRETS par leur nom global : les remplacer ici suffit, et le fichier de r1
# n'est pas touche.
R1.gabarit = gabarit
R1.ARRETS[GABARIT] = ARRETS
for _cle, _info in MODELES.items():
    R1.MODELES.setdefault(_cle, _info)


# --------------------------------------------------------------------------------------
# 3. Les criteres de chute propres a r4
# --------------------------------------------------------------------------------------

def vecteurs_exemples():
    """{K : vecteur de pourcentages de l'exemple de ce K}, pour le critere 2 bis."""
    return {len(ex["options"]): list(ex["reponse"]) for ex in EXEMPLES}


def recopie_exemple_3ex(distribution, options, tolerance=0.005):
    """La distribution decrite est elle le vecteur de l'exemple a trois coups de meme K ?

    Meme forme que recopie_exemple() de r1_evaluer : on compare la distribution
    renormalisee au vecteur de l'exemple, lui aussi renormalise. Rend False si aucun
    exemple ne partage le K de l'item.
    """
    if not distribution:
        return False
    vecteurs = vecteurs_exemples()
    k = len(options)
    if k not in vecteurs:
        return False
    cible = np.array(vecteurs[k], dtype=float)
    cible = cible / cible.sum()
    obtenu = np.array([distribution.get(o, np.nan) for o in options], dtype=float)
    if not np.all(np.isfinite(obtenu)):
        return False
    return bool(np.max(np.abs(obtenu - cible)) <= tolerance)


def compter_recopies(chemin):
    """Taux de recopie des exemples a trois coups dans un fichier de trace.

    Rend un compte par K, plus le total. Le preenregistrement fixe la conduite : pour
    K >= 3 la cellule sort et le taux est publie, et au dela de 5 pour cent le run du
    modele n'est pas interprete ; pour K = 2 le vecteur [43, 57] est une reponse
    plausible, les cellules ne sortent pas et le taux est publie a cote du taux de base
    mesure sur les memes items dans la condition q4 sous gabarit.
    """
    par_k = collections.Counter()
    total_k = collections.Counter()
    if not os.path.exists(chemin):
        return par_k, total_k
    with open(chemin, encoding="utf-8") as fh:
        for ligne in fh:
            ligne = ligne.strip()
            if not ligne:
                continue
            try:
                d = json.loads(ligne)
            except json.JSONDecodeError:
                continue
            k = d.get("n_modalites")
            total_k[k] += 1
            if d.get("distribution") and recopie_exemple_3ex(d["distribution"],
                                                             d["options"]):
                par_k[k] += 1
    return par_k, total_k


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as fh:
        for bloc in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloc)
    return h.hexdigest()


# --------------------------------------------------------------------------------------
# 4. La verification hors ligne, sans un seul appel de modele
# --------------------------------------------------------------------------------------

def verifier(items, table, familles_par_item, bavard=True):
    """Tout ce qui peut etre verifie sans serveur. Rend la liste des defauts trouves."""
    defauts = []

    def dire(*a):
        if bavard:
            print(*a, flush=True)

    dire("=" * 78)
    dire("1. Les trois exemples a trois coups")
    vecteurs = vecteurs_exemples()
    for ex in EXEMPLES:
        k = len(ex["options"])
        s = sum(ex["reponse"])
        uniforme = len(set(ex["reponse"])) == 1
        collision = ex["reponse"] == R1.repartition_exemple(k)
        dire(f"   K={k:2d}  somme={s:3d}  uniforme={uniforme}  "
             f"collision avec l'exemple de relance de r1={collision}  {ex['reponse']}")
        if s != 100:
            defauts.append(f"exemple K={k} : somme {s} au lieu de 100")
        if uniforme:
            defauts.append(f"exemple K={k} : vecteur uniforme")
        if collision:
            defauts.append(f"exemple K={k} : collision avec repartition_exemple({k})")
    if len(vecteurs) != len(EXEMPLES):
        defauts.append("deux exemples partagent le meme K")
    texte_exemples = " ".join(bloc_exemple(ex) for ex in EXEMPLES).lower()
    for mot in ("liberal", "conservative", "moderate", "american", "democrat",
                "republican", "general social survey"):
        if mot in texte_exemples:
            defauts.append(f"le mot « {mot} » apparait dans les exemples")
    noms_items = {it.lower().replace("/y", "") for it in items}
    for mot in texte_exemples.replace('"', " ").split():
        if mot.strip(".,?:") in noms_items:
            defauts.append(f"un nom d'item du GSS apparait dans les exemples : {mot}")
    dire("   aucun mot politique, aucun nom d'item du GSS : "
         f"{'oui' if not defauts else 'NON'}")

    dire("")
    dire("2. Le referent humain de r1, reutilise tel quel")
    if not os.path.exists(REFERENT):
        defauts.append("referent humain absent")
        dire("   ABSENT")
    else:
        h = sha256(REFERENT)
        dire(f"   {REFERENT}")
        dire(f"   sha256 {h}")
        dire(f"   attendu {REFERENT_SHA}  ->  "
             f"{'identique' if h == REFERENT_SHA else 'DIFFERENT'}")
        if h != REFERENT_SHA:
            defauts.append("le referent humain a change depuis r1")

    dire("")
    dire("3. Les fichiers de poids, taille et empreinte")
    for cle in ORDRE:
        info = MODELES[cle]
        chemin = os.path.join(GGUF, info["fichier"])
        if not os.path.exists(chemin):
            dire(f"   {cle:8s} ABSENT : {chemin}")
            defauts.append(f"{cle} : fichier de poids absent")
            continue
        octets = os.path.getsize(chemin)
        h = sha256(chemin)
        ok = (octets == info["octets"]) and (h == info["sha256"])
        dire(f"   {cle:8s} {octets} octets, sha256 {h[:16]}...  "
             f"{'conforme' if ok else 'NON CONFORME'}")
        if not ok:
            defauts.append(f"{cle} : taille ou empreinte non conforme")

    dire("")
    dire("4. Le plan de cellules")
    dire(f"   {len(items)} items, {len(R1.CAMPS)} camps, {len(R1.IDENTITES)} identites, "
         f"{len(ORDRE)} modeles")
    dire(f"   {len(items) * 3 * 2} cellules par modele, "
         f"{len(items) * 3 * 2 * len(ORDRE)} au total")
    ks = collections.Counter(len(table[it]["options"]) for it in items)
    dire(f"   K des items : min {min(ks)}, max {max(ks)}, "
         f"repartition {dict(sorted(ks.items()))}")
    couverts = sorted(vecteurs_exemples())
    dire(f"   K couverts par un exemple : {couverts} ; "
         f"items concernes par le critere 2 bis : "
         f"{sum(n for k, n in ks.items() if k in couverts)} sur {len(items)}")

    dire("")
    dire("5. Le parse, sur des sorties fabriquees")
    options3 = table[items[0]]["options"]
    essais = [
        ("format demande", "\n".join(f"{l}: {v}" for l, v in
                                     zip(LETTRES, [30, 45, 25][:len(options3)])), True),
        ("etoiles de gras", "\n".join(f"**{l}:** {v}" for l, v in
                                      zip(LETTRES, [30, 45, 25][:len(options3)])), True),
        ("une lettre manquante", "A: 50\nB: 50", len(options3) == 2),
        ("somme hors bande", "\n".join(f"{l}: 10" for l in LETTRES[:len(options3)]),
         len(options3) == 10),
        ("bavardage", "Here is the distribution:\nA: 30\nB: 45\nC: 25\nHope this helps.",
         len(options3) == 3),
    ]
    for nom, texte, attendu_ok in essais:
        d, s, motif = R1.parser(texte, options3)
        obtenu_ok = d is not None
        marque = "ok" if obtenu_ok == attendu_ok else "ECART"
        dire(f"   {nom:24s} -> {'parse' if obtenu_ok else 'rejet'} "
             f"({motif or 'aucun motif'}) [{marque}]")
        if obtenu_ok != attendu_ok:
            defauts.append(f"parse inattendu sur l'essai « {nom} »")

    dire("")
    dire("6. Le critere 2 bis, sur des distributions fabriquees")
    for ex in EXEMPLES:
        k = len(ex["options"])
        item = next((it for it in items if len(table[it]["options"]) == k), None)
        if item is None:
            dire(f"   K={k} : aucun item du GSS n'a ce K")
            continue
        opts = table[item]["options"]
        v = np.array(ex["reponse"], dtype=float)
        v = v / v.sum()
        copie = {o: float(x) for o, x in zip(opts, v)}
        autre = {o: 1.0 / k for o in opts}
        a = recopie_exemple_3ex(copie, opts)
        b = recopie_exemple_3ex(autre, opts)
        dire(f"   K={k:2d} item {item:12s} : recopie detectee={a}, uniforme detecte={b}")
        if not a or b:
            defauts.append(f"critere 2 bis defaillant sur K={k}")

    dire("")
    dire("7. L'invite complete, une cellule reelle, telle qu'elle partira")
    item = items[0]
    sys_txt = R1.systeme("gauche", "adversaire")
    usr_txt, opts = R1.utilisateur(item, "gauche", table)
    p = gabarit(GABARIT, sys_txt, usr_txt)
    dire("   " + "-" * 74)
    for ligne in p.split("\n"):
        dire("   | " + ligne)
    dire("   " + "-" * 74)
    dire(f"   {len(p)} caracteres, environ {len(p) // 4} tokens ; "
         f"le prefixe commun en fait {len(prefixe(sys_txt))}, "
         f"soit {100 * len(prefixe(sys_txt)) // len(p)} pour cent servis par le cache")
    dire(f"   sequences d'arret : {ARRETS}")
    if p.count(SEPARATEUR) != len(EXEMPLES) + 1:
        defauts.append("nombre de separateurs inattendu dans l'invite")
    if not p.endswith("\n\n"):
        defauts.append("l'invite ne se termine pas par une ligne vide")

    dire("")
    dire("8. L'invite de relance, la meme qu'en r1")
    usr_r, _ = R1.utilisateur(item, "gauche", table, rappel=True)
    dire("   " + usr_r.split("\n")[-len(opts) - 1].strip())
    dire(f"   exemple chiffre de la relance pour K={len(opts)} : "
         f"{R1.repartition_exemple(len(opts))}")

    dire("")
    dire("9. Les cles de modele injectees dans le registre de r1")
    dire(f"   registre r1 apres injection : {sorted(R1.MODELES)}")
    for cle in ORDRE:
        if cle not in R1.MODELES:
            defauts.append(f"{cle} absent du registre de r1")

    dire("")
    dire("=" * 78)
    if defauts:
        dire(f"{len(defauts)} DEFAUT(S) :")
        for d in defauts:
            dire("   - " + d)
    else:
        dire("aucun defaut. La verification hors ligne passe.")
    return defauts


# --------------------------------------------------------------------------------------
# 5. Le run
# --------------------------------------------------------------------------------------

def journaliser(message):
    os.makedirs(TRACES, exist_ok=True)
    with open(JOURNAL, "a", encoding="utf-8") as fh:
        fh.write(f"{datetime.datetime.now():%Y-%m-%d %H:%M:%S} {message}\n")
        fh.flush()


# Critere de chute 1 bis, ajoute a la page de plan le 2026-09-09 a 00:05, AVANT tout
# appel de modele. Le run de r4 n'a pas de smoke test contre un serveur vivant, parce
# qu'aucun serveur ne peut etre lance ce soir : R2 puis R3 puis la file 4 occupent le GPU
# jusqu'au matin. La sonde ci dessous remplace ce smoke test manquant. Elle passe les
# SONDE premieres cellules d'un modele, puis regarde le taux de rejet. Au dela de
# SEUIL_SONDE, le modele est arrete la : son taux d'echec de format est publie, ce que le
# critere 1 prescrit deja, et les vingt minutes de sa place vont au modele suivant. En
# dessous, le meme modele reprend exactement ou il s'etait arrete, par le mecanisme de
# reprise de r1, qui ne refait aucun appel deja ecrit.
SONDE = 60
SEUIL_SONDE = 0.50


def _fusionner(a, b):
    """Deux passages du meme modele, la sonde puis le reste, en un seul enregistrement."""
    if a is None:
        return b
    if b is None:
        return a
    c = dict(b)
    for cle in ("cellules", "rejets", "relances", "relances_reussies"):
        c[cle] = a.get(cle, 0) + b.get(cle, 0)
    c["taux_rejet"] = round(c["rejets"] / c["cellules"], 4) if c["cellules"] else 0.0
    c["arret_demande"] = bool(a.get("arret_demande") or b.get("arret_demande"))
    c["secondes"] = round(a.get("secondes", 0.0) + b.get("secondes", 0.0), 1)
    c["deja_faites"] = a.get("deja_faites", 0)
    c["cellules_par_heure"] = (round(c["cellules"] / c["secondes"] * 3600, 1)
                               if c["secondes"] else 0.0)
    motifs = collections.Counter(a.get("motifs_de_rejet", {}))
    motifs.update(b.get("motifs_de_rejet", {}))
    c["motifs_de_rejet"] = dict(motifs)
    return c


def run(cles, items, table, familles_par_item, fin_ts, fin_dt, args):
    """Un serveur a la fois, un modele apres l'autre, trace ecrite au fil de l'eau.

    Un modele qui echoue a demarrer ou qui explose en cours de route ne fait pas tomber
    les suivants : la boucle attrape l'exception, la journalise et passe au modele
    d'apres. Sans cela, un socle que llama-server refuserait de charger emporterait avec
    lui les deux conditions instruites, et il ne resterait rien de la nuit.
    """
    resume = []
    depart = datetime.datetime.now()
    try:
        for cle in cles:
            if time.time() >= fin_ts:
                journaliser(f"fin dure atteinte avant le lancement de {cle}")
                print(f"fin dure atteinte avant le lancement de {cle}", flush=True)
                break
            info = MODELES[cle]
            port = args.port or premier_port_libre()
            if not port_libre(port):
                sys.exit(f"le port {port} est occupe, un llama-server tourne peut etre deja")
            print(f"[{cle}] {info['nom']} ({info['type']}), {info['quantification']}, "
                  f"gabarit {info['gabarit']}, port {port}", flush=True)
            journaliser(f"lancement du serveur pour {cle} ({info['nom']}) sur {port}")
            moteur = None
            try:
                moteur = R1.MoteurR1(os.path.join(GGUF, info["fichier"]),
                                     contexte=args.contexte, parallele=1,
                                     port=port, cache_kv_8bits=True)
                moteur.demarrer()
                print(f"[{cle}] serveur pret en {moteur.chargement_s:.1f} s", flush=True)

                # La sonde, critere de chute 1 bis.
                sonde = R1.lancer(moteur, cle, info, items, table, familles_par_item,
                                  R1.CAMPS, R1.IDENTITES, fin_ts, SUFFIXE,
                                  limite=min(SONDE, args.limite or SONDE),
                                  n_predict=args.n_predict,
                                  sans_relance=args.sans_relance)
                taux = sonde["rejets"] / sonde["cellules"] if sonde["cellules"] else 0.0
                print(f"[{cle}] sonde : {sonde['cellules']} cellules, "
                      f"{sonde['rejets']} rejets, taux {taux:.3f}", flush=True)
                journaliser(f"[{cle}] sonde : {sonde['cellules']} cellules, "
                            f"{sonde['rejets']} rejets, taux {taux:.3f}, "
                            f"seuil {SEUIL_SONDE}")
                r = sonde
                if sonde.get("arret_demande"):
                    pass
                elif taux > SEUIL_SONDE and sonde["cellules"] >= SONDE:
                    print(f"[{cle}] CRITERE 1 BIS : taux de rejet {taux:.3f} au dessus de "
                          f"{SEUIL_SONDE} sur les {SONDE} premieres cellules. Le modele "
                          f"est arrete, son taux d'echec est publie, la place va au "
                          f"suivant.", flush=True)
                    journaliser(f"[{cle}] CRITERE 1 BIS : arret sur taux de rejet "
                                f"{taux:.3f}")
                    r["arret_critere_1bis"] = True
                elif args.limite is None or args.limite > SONDE:
                    reste = R1.lancer(moteur, cle, info, items, table, familles_par_item,
                                      R1.CAMPS, R1.IDENTITES, fin_ts, SUFFIXE,
                                      limite=(None if args.limite is None
                                              else args.limite - SONDE),
                                      n_predict=args.n_predict,
                                      sans_relance=args.sans_relance)
                    r = _fusionner(sonde, reste)
                    r["arret_critere_1bis"] = False

                r["port"] = port
                r["chargement_s"] = round(moteur.chargement_s, 1)
                r["type"] = info["type"]
                r["taux_rejet_sonde"] = round(taux, 4)
                par_k, total_k = compter_recopies(R1.chemin_trace(cle, SUFFIXE))
                r["recopies_exemple_3ex"] = {str(k): int(v) for k, v in par_k.items()}
                r["cellules_par_k"] = {str(k): int(v) for k, v in total_k.items()}
                resume.append(r)
                print(f"[{cle}] {r['cellules']} cellules en {r['secondes'] / 60:.1f} min, "
                      f"{r['cellules_par_heure']:,.0f}/h, {r['rejets']} rejets, "
                      f"{r['relances']} relances, "
                      f"{sum(par_k.values())} recopies d'exemple".replace(",", " "),
                      flush=True)
                journaliser(f"[{cle}] termine : {r['cellules']} cellules, "
                            f"{r['cellules_par_heure']:.0f}/h, {r['rejets']} rejets, "
                            f"{sum(par_k.values())} recopies d'exemple a trois coups")
            except KeyboardInterrupt:
                journaliser(f"[{cle}] interrompu au clavier, arret propre")
                raise
            except Exception as exc:
                # Un modele perdu ne doit pas emporter les autres.
                print(f"[{cle}] ECHEC : {type(exc).__name__} : {exc}", flush=True)
                journaliser(f"[{cle}] ECHEC : {type(exc).__name__} : {exc}")
                resume.append({"cle_modele": cle, "modele": info["nom"],
                               "type": info["type"], "echec": f"{type(exc).__name__}: {exc}",
                               "cellules": 0, "rejets": 0, "relances": 0,
                               "secondes": 0.0, "cellules_par_heure": 0.0})
            finally:
                if moteur is not None:
                    moteur.arreter()
                print(f"[{cle}] serveur arrete. charge {os.getloadavg()}", flush=True)
            if resume and resume[-1].get("arret_demande"):
                # Fichier d'arret pose pendant le run : les modeles suivants ne sont pas
                # lances, la trace et le resume sont deja ecrits, la sortie est en code 0.
                journaliser("ARRET DEMANDE, les modeles suivants ne sont pas lances")
                print("ARRET DEMANDE, les modeles suivants ne sont pas lances", flush=True)
                break
    finally:
        chemin = os.path.join(TRACES, "r4-resume.json")
        with open(chemin, "w", encoding="utf-8") as fh:
            json.dump({
                "depart": depart.isoformat(), "fin": datetime.datetime.now().isoformat(),
                "fin_dure": fin_dt.isoformat(), "version_prompt": VERSION_PROMPT,
                "gabarit": GABARIT, "suffixe": SUFFIXE,
                "sans_relance": args.sans_relance,
                "n_predict": args.n_predict, "contexte": args.contexte,
                "items": len(items), "modeles": resume,
                "exemples": EXEMPLES,
            }, fh, indent=2, ensure_ascii=False)
        print(f"resume ecrit : {chemin}", flush=True)
        fin_message = (f"RUN TERMINE {datetime.datetime.now():%Y-%m-%d %H:%M:%S} "
                       f"({sum(r['cellules'] for r in resume)} cellules)")
        print(fin_message, flush=True)
        journaliser(fin_message)
    return resume


# --------------------------------------------------------------------------------------
# 6. L'evaluation : r1_evaluer.py, sans une modification
# --------------------------------------------------------------------------------------

def copier_condition_q4():
    """Copie octet pour octet data/traces/r1-q4.jsonl vers r1-q4-r4.jsonl.

    Declaree dans la page de plan section 7. Elle existe pour que l'evaluateur voie les
    quatre conditions dans le meme tableau et applique Holm sur une famille commune
    plutot que sur deux runs separes. Aucun appel de modele n'est refait, aucune ligne
    n'est modifiee, le fichier d'origine n'est jamais touche.
    """
    source = os.path.join(TRACES, "r1-q4.jsonl")
    cible = os.path.join(TRACES, "r1-q4-r4.jsonl")
    if not os.path.exists(source):
        print(f"condition q4 absente : {source}", flush=True)
        return None
    if os.path.exists(cible) and sha256(cible) == sha256(source):
        print(f"copie deja a jour : {cible}", flush=True)
        return cible
    shutil.copyfile(source, cible)
    h = sha256(source)
    print(f"copie {source} -> {cible}, sha256 {h}", flush=True)
    journaliser(f"copie de la condition q4 : {cible}, sha256 {h}")
    return cible


def evaluer(argv_supplementaire=()):
    """Appelle r1_evaluer.main() avec --suffixe r4, sans modifier son fichier."""
    import r1_evaluer
    copier_condition_q4()
    ancien = sys.argv
    sys.argv = ["r1_evaluer.py", "--suffixe", SUFFIXE] + list(argv_supplementaire)
    try:
        r1_evaluer.main()
    finally:
        sys.argv = ancien


# --------------------------------------------------------------------------------------
# 7. H4 : plus proche des marginales nationales publiees, ou de notre echantillon ?
# --------------------------------------------------------------------------------------
# Referent national : les vagues 2016 et 2018 du panel GSS 2016-2020, qui sont deux
# echantillons nationaux de probabilite du GSS, ponderes par wtssall. C'est la source dont
# le GSS Data Explorer publie les tableaux croises. Aucun telechargement, aucun appel.
#
# Ce que le test ne dit pas : il ne dit pas que le modele a lu le GSS Data Explorer, et il
# ne compare a aucune donnee Pew, dont rien n'est sur la machine.

VAGUES_NATIONALES = [("_1a", 2016), ("_1b", 2018)]
SEUIL_APPARIEMENT = 0.99
MIN_PAR_CAMP = 100


def _camp_panel(v):
    """Repliement en trois blocs, regle GSS_BLOC3 de a30.

    Le panel ecrit « moderate, middle of the road » la ou l'archive de Stanford ecrit
    « moderate ». C'est la seule normalisation faite, et elle est ecrite ici.
    """
    if v is None or (isinstance(v, float) and not np.isfinite(v)):
        return None
    s = str(v).strip().lower()
    if s.startswith("moderate"):
        s = "moderate"
    return GSS_BLOC3.get(s)


def marginales_nationales(items, table):
    """Distributions nationales ponderees par item et par camp, sur les vagues 2016 et 2018.

    Rend (distributions, diagnostic) ou distributions est {(item, camp): vecteur} aligne
    sur l'ordre de la nomenclature, et diagnostic un DataFrame par item.
    """
    import pyreadstat
    import a12_retest_delai as A12
    from a5_agents_locaux_gss import canoniser

    chemin = os.path.join(PANEL, "gss2020panel_r1a.dta")
    _, meta = pyreadstat.read_dta(chemin, metadataonly=True, encoding="latin1")
    colonnes = {c.lower(): c for c in meta.column_names}

    plan, besoin = {}, set()
    for suf, _annee in VAGUES_NATIONALES:
        plan[suf] = {}
        for it in items:
            cols = A12.colonnes_vague(it, suf, colonnes)
            if cols:
                plan[suf][it] = [c.lower() for c in cols]
                besoin.update(colonnes[c] for c in cols)
        for c in (f"polviews{suf}", f"wtssall{suf}"):
            if c in colonnes:
                besoin.add(colonnes[c])

    df, _ = pyreadstat.read_dta(chemin, usecols=sorted(besoin), encoding="latin1",
                                apply_value_formats=True, formats_as_category=False)
    df.columns = [c.lower() for c in df.columns]

    poids_total = collections.defaultdict(float)   # (item, camp, modalite)
    apparie = collections.Counter()                # item
    etiquete = collections.Counter()               # item
    effectif = collections.defaultdict(float)      # (item, camp)

    for suf, _annee in VAGUES_NATIONALES:
        camps = np.array([_camp_panel(v) for v in df.get(f"polviews{suf}",
                                                         pd.Series([np.nan] * len(df)))],
                         dtype=object)
        w = df[f"wtssall{suf}"].to_numpy(dtype=float) if f"wtssall{suf}" in df else \
            np.ones(len(df))
        w = np.where(np.isfinite(w), w, 0.0)
        for it, cols in plan[suf].items():
            v, _ = A12.serie_fusionnee(df, cols)
            for i in range(len(df)):
                camp = camps[i]
                if camp is None or w[i] <= 0:
                    continue
                x = v[i]
                if x is None or (isinstance(x, float) and not np.isfinite(x)):
                    continue
                etiquete[it] += 1
                canon = canoniser(it, x, table)
                if canon is None:
                    continue
                apparie[it] += 1
                poids_total[(it, camp, canon)] += w[i]
                effectif[(it, camp)] += w[i]

    distributions, lignes = {}, []
    for it in items:
        if etiquete[it] == 0:
            continue
        part = apparie[it] / etiquete[it]
        n_min = min(effectif.get((it, c), 0.0) for c in R1.CAMPS)
        retenu = (part >= SEUIL_APPARIEMENT) and (n_min >= MIN_PAR_CAMP)
        lignes.append({"item": it, "n_etiquete": etiquete[it],
                       "part_appariee": part, "n_pondere_min_par_camp": n_min,
                       "retenu": retenu})
        if not retenu:
            continue
        for camp in R1.CAMPS:
            options = table[it]["options"]
            vecteur = np.array([poids_total.get((it, camp, o), 0.0) for o in options],
                               dtype=float)
            s = vecteur.sum()
            if s > 0:
                distributions[(it, camp)] = vecteur / s
    return distributions, pd.DataFrame(lignes)


def h4(argv_supplementaire=()):
    """Le test de restitution, et son controle de puissance."""
    import r1_evaluer as EV

    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()

    print("construction des marginales nationales, vagues 2016 et 2018 du panel GSS",
          flush=True)
    nat, diag = marginales_nationales(items, table)
    chemin_diag = os.path.join(SORTIE, "r4-h4-perimetre.csv")
    diag.to_csv(chemin_diag, index=False)
    retenus = sorted({it for it, _ in nat})
    print(f"{len(diag)} items dans le panel, {len(retenus)} retenus "
          f"(appariement >= {SEUIL_APPARIEMENT}, au moins {MIN_PAR_CAMP} personnes "
          f"ponderees par camp) ; perimetre ecrit dans {chemin_diag}", flush=True)
    if not retenus:
        print("perimetre vide : H4 n'est pas calculable", flush=True)
        return

    ref, options, effectifs = EV.lire_referent(SUFFIXE)
    traces = EV.lire_traces(SUFFIXE)
    print(f"{len(traces)} lignes de trace lues", flush=True)

    lignes = []
    for t in traces:
        it, camp = t["item"], t["camp"]
        if t["rejet"] or not t.get("distribution"):
            continue
        if (it, camp) not in nat:
            continue
        if (it, camp, "w1") not in ref:
            continue
        opts = options[it]
        p_dec = np.array([t["distribution"][o] for o in opts], dtype=float)
        p_ech = ref[(it, camp, "w1")]
        p_nat = nat[(it, camp)]
        lignes.append({
            "cle_modele": t["cle_modele"], "modele": t["modele"],
            "camp": camp, "identite": t["identite"], "item": it,
            "tv_decrit_echantillon": EV.tv(p_dec, p_ech),
            "tv_decrit_national": EV.tv(p_dec, p_nat),
            "tv_echantillon_national": EV.tv(p_ech, p_nat),
        })
    cel = pd.DataFrame(lignes)
    if cel.empty:
        print("aucune cellule exploitable : H4 n'est pas calculable", flush=True)
        return
    cel["difference"] = cel["tv_decrit_echantillon"] - cel["tv_decrit_national"]
    chemin_cel = os.path.join(SORTIE, "r4-h4-par-cellule.csv")
    cel.to_csv(chemin_cel, index=False)

    rng = np.random.default_rng(EV.GRAINE if hasattr(EV, "GRAINE") else 20260908)
    resultats = []
    for (cle, modele, identite), g in cel.groupby(
            ["cle_modele", "modele", "identite"], sort=False):
        par_item = g.groupby("item", sort=False)["difference"].mean()
        d = par_item.to_numpy(dtype=float)
        moyenne = float(np.mean(d))
        tirages = np.array([np.mean(rng.choice(d, size=len(d), replace=True))
                            for _ in range(2000)])
        bas, haut = np.percentile(tirages, [2.5, 97.5])
        p = EV.p_permutation_signe(d, rng)
        ecart_referents = float(np.median(
            g.groupby("item", sort=False)["tv_echantillon_national"].mean()))
        erreur = float(np.median(
            g.groupby("item", sort=False)["tv_decrit_echantillon"].mean()))
        puissance = ecart_referents >= 0.25 * erreur
        resultats.append({
            "cle_modele": cle, "modele": modele, "identite": identite,
            "n_items": len(d),
            "difference_moyenne": moyenne, "ic_bas": float(bas), "ic_haut": float(haut),
            "p": p,
            "mediane_tv_echantillon_national": ecart_referents,
            "mediane_tv_decrit_echantillon": erreur,
            "rapport_de_puissance": ecart_referents / erreur if erreur else float("nan"),
            "test_a_de_la_puissance": puissance,
        })
    tab = pd.DataFrame(resultats)
    for identite, g in tab.groupby("identite", sort=False):
        sous = EV.poser_holm(g.to_dict("records"))
        for r in sous:
            tab.loc[(tab["cle_modele"] == r["cle_modele"]) &
                    (tab["identite"] == identite), "p_holm"] = r["p_holm"]
    chemin = os.path.join(SORTIE, "r4-h4-restitution.csv")
    tab.to_csv(chemin, index=False)
    print(tab.to_string(index=False), flush=True)
    print(f"ecrit : {chemin}", flush=True)
    if not tab["test_a_de_la_puissance"].all():
        print("ATTENTION : le controle de puissance preenregistre echoue sur au moins une "
              "condition. Les deux referents sont trop proches l'un de l'autre pour "
              "qu'un modele puisse les distinguer ; le resultat est NON CONCLUANT et ne "
              "doit jamais etre lu comme une absence d'effet.", flush=True)


# --------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--modele", default=",".join(ORDRE),
                    help="cles, dans l'ordre de passage : " + ", ".join(ORDRE))
    ap.add_argument("--items", type=int, default=0,
                    help="0 pour les 149 items, n pour les n premiers (smoke test)")
    ap.add_argument("--fin", default="10:00", help="fin dure du calcul, heure locale")
    ap.add_argument("--limite", type=int, default=None,
                    help="nombre maximal de cellules par modele, pour un smoke test")
    ap.add_argument("--n-predict", type=int, default=R1.N_PREDICT)
    ap.add_argument("--port", type=int, default=0)
    ap.add_argument("--contexte", type=int, default=4096)
    ap.add_argument("--sans-relance", action="store_true",
                    help="transmis a r1_oracle_camps.lancer : plus de seconde tentative, "
                         "un echec de premiere tentative est un rejet jamais rejoue "
                         "(r5-preenregistrement.md section Relance, apres r4-resultats.md "
                         "section 3.1, ou la relance recopie son exemple 45 fois sur 45 en "
                         "completion). Defaut : comportement de la nuit du 8 au 9.")
    ap.add_argument("--verifier", action="store_true",
                    help="verification hors ligne, aucun serveur, aucun appel")
    ap.add_argument("--evaluer", action="store_true",
                    help="appelle r1_evaluer.py --suffixe r4")
    ap.add_argument("--h4", action="store_true",
                    help="le test de restitution contre les marginales nationales")
    ap.add_argument("--sans-figure", action="store_true")
    args = ap.parse_args()

    os.makedirs(TRACES, exist_ok=True)

    if args.evaluer:
        evaluer(["--sans-figure"] if args.sans_figure else [])
        return
    if args.h4:
        h4()
        return

    table = nomenclature()
    ids, items, y1, y2, x, attributs = charger()
    if args.items:
        items = items[:args.items]
    familles_par_item = {it: nom for nom, membres in FAMILLES.items() for it in membres}

    if args.verifier:
        defauts = verifier(items, table, familles_par_item)
        sys.exit(1 if defauts else 0)

    cles = [c.strip() for c in args.modele.split(",") if c.strip()]
    for c in cles:
        if c not in MODELES:
            sys.exit(f"modele inconnu : {c}. Cles connues : {', '.join(ORDRE)}")
        chemin = os.path.join(GGUF, MODELES[c]["fichier"])
        if not os.path.exists(chemin):
            sys.exit(f"modele introuvable : {chemin}")

    # Critere de chute 6 : le referent humain de r1 doit etre celui de r1.
    if not os.path.exists(REFERENT):
        sys.exit(f"referent humain absent : {REFERENT}")
    h = sha256(REFERENT)
    if h != REFERENT_SHA:
        sys.exit(f"le referent humain a change : {h} au lieu de {REFERENT_SHA}. "
                 "Critere de chute 6, rien n'est publie.")

    # La version d'invite de r4, posee dans le module de r1 avant tout appel : c'est elle
    # qui va dans la trace et dans l'index de reprise.
    R1.VERSION_PROMPT = VERSION_PROMPT
    R1.JOURNAL_RUN = JOURNAL

    fin_ts, fin_dt = heure_de_fin(args.fin)
    depart = datetime.datetime.now()
    entete = (f"popsim r4, l'oracle des camps sur le modele socle. "
              f"Depart {depart:%Y-%m-%d %H:%M:%S}, fin dure {fin_dt:%Y-%m-%d %H:%M} "
              f"({(fin_ts - time.time()) / 3600:.2f} h). Modeles : {', '.join(cles)}. "
              f"Version d'invite {VERSION_PROMPT}, gabarit {GABARIT}.")
    print(entete, flush=True)
    journaliser("DEBUT " + entete)
    print(f"charge machine : {os.getloadavg()}", flush=True)

    defauts = verifier(items, table, familles_par_item, bavard=False)
    if defauts:
        for d in defauts:
            journaliser("DEFAUT " + d)
        sys.exit("la verification hors ligne echoue : " + " ; ".join(defauts))
    journaliser("verification hors ligne : aucun defaut")

    n = len(items) * len(R1.CAMPS) * len(R1.IDENTITES)
    print(f"{n} cellules par modele, {n * len(cles)} au total", flush=True)
    print(f"referent humain reutilise : {REFERENT}, sha256 {h}", flush=True)

    run(cles, items, table, familles_par_item, fin_ts, fin_dt, args)


if __name__ == "__main__":
    main()
