"""Test hors ligne du client R6, avec un faux serveur HTTP local.

AUCUN appel distant, AUCUNE cle d'API lue, AUCUN octet ecrit dans data/. Le faux serveur
tourne sur 127.0.0.1 et rend des reponses programmees au format d'OpenRouter ; tout ce que
le test verifie est de la lecture, du comptage, de la comptabilite et de l'ecriture de
trace, dans un dossier temporaire efface a la fin.

Ce qu'il protege, et pourquoi il existe :
  1. les deux formats d'invite sont bien ceux de q4 et de q4gab3, obtenus par appel des
     fonctions de R1 et de R5, jamais recopies ;
  2. la lecture est celle de R1 et rien d'autre : temperature 0, un appel par cellule,
     `R1.parser` importe, aucune sequence d'arret envoyee, aucune relance ;
  3. le plafond en USD est dur : au depassement le run s'arrete net et ecrit
     « PLAFOND ATTEINT » dans son journal, y compris quand le cout reel depasse
     l'estimation a priori de la page v2 ;
  4. `data/traces/STOP` arrete le run entre deux cellules, trace fermee et relisible ;
  5. la reprise ne rejoue jamais une cellule deja ecrite ;
  6. le feu vert `data/traces/GO-R6` existe et se lit ;
  7. le reglage de raisonnement part bien dans la requete et se retrouve dans la trace ;
  8. la trace porte les cles que `r1_evaluer.py` lit, le fournisseur aval, les jetons
     factures, le cout annonce retenu pour le plafond et le cumul ;
  9. le plan de cellules de la v2 fait bien 894 et 316 cellules ;
 10. l'essai de N cellules ecrit son resume de cout reel, de rejets et de latence.

Usage : .venv/bin/python analyses/test_r6_client.py
"""

import json
import os
import shutil
import subprocess
import sys
import tempfile
import threading
from unittest.mock import patch
from urllib.parse import urlsplit
from http.server import BaseHTTPRequestHandler, HTTPServer

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "analyses"))

import r1_oracle_camps as R1
import r5_gabarit_exemples as R5
import r6_oracle_distant as R6

# Une regression du routage des tests doit echouer avant tout acces externe.
_urlopen = R6.urllib.request.urlopen

def seulement_local(req, *args, **kwargs):
    if urlsplit(req.full_url).hostname != "127.0.0.1":
        raise AssertionError("reseau externe interdit dans les tests")
    return _urlopen(req, *args, **kwargs)

R6.urllib.request.urlopen = seulement_local
R6.cle_api = lambda *a, **kw: (_ for _ in ()).throw(AssertionError("lecture secret interdite"))

TMP = tempfile.mkdtemp(prefix="r6test-")
R6.TRACES = TMP
R6.JOURNAL = os.path.join(TMP, "r6-run.log")
R6.FICHIER_ARRET_GLOBAL = os.path.join(TMP, "STOP")
R6.FICHIER_ARRET_R6 = os.path.join(TMP, "STOP-R6")
R6.FICHIER_ARRET = R6.FICHIER_ARRET_GLOBAL
R6.FICHIER_GO = os.path.join(TMP, "GO-R6")

ITEMS = ["item_a", "item_b", "item_c", "item_d"]
TABLE = {n: {"question": "Q " + n, "options": ["Yes", "No"]} for n in ITEMS}

BON = "A: 60\nB: 40"
MAUVAIS = "Sure! Here is the distribution you asked for."


# --------------------------------------------------------------------------------------
# 1. Le faux serveur : le contrat de reponse d'OpenRouter, et rien de plus
# --------------------------------------------------------------------------------------

class Scenario:
    def __init__(self):
        self.textes = [BON]         # rendus a la suite, le dernier se repete
        self.jetons = (300, 20)
        self.raisonnement = 0
        self.codes = []             # codes HTTP a rendre a la suite, 200 pour repondre
        self.appels = 0
        self.requetes = []
        self.au_ieme_appel = {}
        self.entetes_erreur = {}
        self.erreur_corps = None

    def suivant(self):
        i = self.appels
        self.appels += 1
        f = self.au_ieme_appel.get(self.appels)
        if f:
            f()
        return self.textes[min(i, len(self.textes) - 1)]


SCENARIO = Scenario()


class Faux(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        charge = json.loads(self.rfile.read(n).decode("utf-8"))
        SCENARIO.requetes.append({"charge": charge, "entetes": dict(self.headers)})
        if SCENARIO.erreur_corps is not None:
            SCENARIO.appels += 1
            corps = json.dumps({"error": {"message": "upstream", "code":
                                           SCENARIO.erreur_corps}}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            for nom, valeur in SCENARIO.entetes_erreur.items():
                self.send_header(nom, valeur)
            self.send_header("Content-Length", str(len(corps)))
            self.end_headers()
            self.wfile.write(corps)
            return
        if SCENARIO.codes:
            code = SCENARIO.codes.pop(0)
            if code != 200:
                SCENARIO.appels += 1
                corps = json.dumps({"error": {"message": "temporarily rate-limited "
                                              "upstream, shared pool", "code": code}}
                                   ).encode("utf-8")
                self.send_response(code)
                self.send_header("Content-Type", "application/json")
                for nom, valeur in SCENARIO.entetes_erreur.items():
                    self.send_header(nom, valeur)
                self.send_header("Content-Length", str(len(corps)))
                self.end_headers()
                self.wfile.write(corps)
                return
        corps = {
            "id": "gen-test", "model": charge["model"], "provider": "FauxFournisseur",
            "choices": [{"message": {"role": "assistant", "content": SCENARIO.suivant()},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": SCENARIO.jetons[0],
                      "completion_tokens": SCENARIO.jetons[1],
                      "completion_tokens_details": {"reasoning_tokens": SCENARIO.raisonnement},
                      "cost": SCENARIO.cout},
        }
        donnees = json.dumps(corps).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(donnees)))
        self.end_headers()
        self.wfile.write(donnees)


serveur = HTTPServer(("127.0.0.1", 0), Faux)
threading.Thread(target=serveur.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{serveur.server_address[1]}/api/v1"


# --------------------------------------------------------------------------------------

ok = True


def verifie(nom, condition, detail=""):
    global ok
    condition = bool(condition)
    ok = ok and condition
    print(("  OK   " if condition else "  RATE ") + nom + (("  " + detail) if detail else ""))


DORMI = []


def dormir(secondes):
    """Le sommeil des reprises, enregistre et jamais dormi : le test doit rester rapide."""
    DORMI.append(secondes)


def joue(cle, format_="q4", plafond=1.0, tarif=(1e-6, 2e-6), limite=None, items=ITEMS,
         camps=("gauche",), identites=("journaliste",), raisonnement="off", base=BASE,
         attentes=R6.ATTENTES, fin_seulement=0, pause=0.0):
    client = R6.ClientChat("fausse-cle", base=base, timeout=10, raisonnement=raisonnement)
    budget = R6.Budget(plafond, tarif[0], tarif[1], R6.JETONS_ESTIMES[format_])
    cellules = list(R1.cellules(list(items), list(camps), list(identites)))
    r = R6.lancer(client, "faux/modele", format_, TABLE, cellules, budget, cle,
                  n_predict=40, limite=limite, journal_tous=10_000, attentes=attentes,
                  pause=pause, fin_seulement=fin_seulement, dormir=dormir)
    chemin = R6.chemin_trace(cle)
    lignes = ([json.loads(l) for l in open(chemin, encoding="utf-8")]
              if os.path.exists(chemin) else [])
    return r, lignes


def non_jouees(cle):
    chemin = os.path.join(R6.TRACES, f"r6-{cle}-non-jouees.jsonl")
    if not os.path.exists(chemin):
        return []
    return [json.loads(l) for l in open(chemin, encoding="utf-8")]


def remise_a_zero(textes=None, jetons=(300, 20), raisonnement=0, codes=None):
    SCENARIO.textes = list(textes or [BON])
    SCENARIO.jetons = jetons
    SCENARIO.raisonnement = raisonnement
    SCENARIO.codes = list(codes or [])
    SCENARIO.appels = 0
    SCENARIO.cout = 0.000123
    SCENARIO.requetes = []
    SCENARIO.au_ieme_appel = {}
    SCENARIO.entetes_erreur = {}
    SCENARIO.erreur_corps = None
    DORMI.clear()


# --------------------------------------------------------------------------------------
print("1. Les deux formats d'invite viennent de R1 et de R5, sans recopie")
msg_q4, options = R6.invite("item_a", "droite", "journaliste", "q4", TABLE)
msg_g3, _ = R6.invite("item_a", "droite", "journaliste", "q4gab3", TABLE)
attendu_sys = R1.systeme("droite", "journaliste")
attendu_usr = R1.utilisateur("item_a", "droite", TABLE)[0]
verifie("tour systeme identique a R1.systeme", msg_q4[0]["content"] == attendu_sys)
verifie("tour utilisateur identique a R1.utilisateur", msg_q4[1]["content"] == attendu_usr)
verifie("q4gab3 = bloc des trois exemples de R5 puis l'invite de q4",
        msg_g3[1]["content"] == R5.bloc_exemples() + attendu_usr)
verifie("q4gab3 et q4 partagent le meme tour systeme",
        msg_g3[0]["content"] == msg_q4[0]["content"])
verifie("les modalites remontent avec l'invite", options == ["Yes", "No"])
verifie("les deux formats declarent deux versions d'invite distinctes",
        R6.FORMATS["q4"] != R6.FORMATS["q4gab3"])
verifie("aucune balise ChatML dans les textes envoyes",
        "<|im_start|>" not in msg_g3[1]["content"] and "<|im_start|>" not in msg_q4[0]["content"])

print("2. Un seul mode de lecture : celui de R1")
remise_a_zero([BON])
r, lignes = joue("lecture1")
charge = SCENARIO.requetes[0]["charge"]
verifie("temperature 0", charge["temperature"] == 0.0)
verifie("max_tokens 40 transmis", charge["max_tokens"] == 40)
verifie("aucune sequence d'arret envoyee", "stop" not in charge)
verifie("aucun logprob demande", "logprobs" not in charge and "top_logprobs" not in charge)
verifie("un appel par cellule, 4 cellules", r["cellules"] == 4 and SCENARIO.appels == 4,
        f"{r['cellules']}/{SCENARIO.appels}")
verifie("distribution lue par le parse de R1",
        lignes[0]["distribution"] == {"Yes": 0.6, "No": 0.4}, str(lignes[0]["distribution"]))
verifie("meme resultat que R1.parser appele directement",
        lignes[0]["distribution"] == R1.parser(BON, ["Yes", "No"])[0])
verifie("aucun rejet", r["rejets"] == 0)

remise_a_zero([MAUVAIS])
r, lignes = joue("lecture2", limite=2)
verifie("un texte illisible est un rejet", r["rejets"] == 2 and r["taux_rejet"] == 1.0)
verifie("un rejet n'est jamais rejoue : 2 appels pour 2 cellules", SCENARIO.appels == 2,
        str(SCENARIO.appels))
verifie("le motif de rejet est celui de R1",
        lignes[0]["motif_rejet"] == R1.parser(MAUVAIS, ["Yes", "No"])[2],
        lignes[0]["motif_rejet"])
verifie("sans_relance vrai dans la trace", lignes[0]["sans_relance"] is True)

print("3. La trace porte les cles de R1 et les ajouts de R6")
remise_a_zero([BON], jetons=(300, 20), raisonnement=7)
r, lignes = joue("trace1", limite=1)
l = lignes[0]
for k in ("version_prompt", "cle_modele", "modele", "quantification", "gabarit", "item",
          "famille", "camp", "identite", "n_modalites", "rejet", "motif_rejet",
          "distribution", "n_tentatives"):
    verifie(f"cle R1 presente : {k}", k in l)
verifie("gabarit declare api-chat", l["gabarit"] == "api-chat")
verifie("quantification recoit le fournisseur aval", l["quantification"] == "FauxFournisseur")
verifie("fournisseur amont trace", l["fournisseur"] == "FauxFournisseur")
verifie("version d'invite = celle de R1 pour q4", l["version_prompt"] == R1.VERSION_PROMPT)
verifie("jetons factures traces", l["jetons_entree"] == 300 and l["jetons_sortie"] == 20)
verifie("jetons de raisonnement traces", l["jetons_raisonnement"] == 7)
cout = 0.000123
verifie("cout annonce retenu pour le plafond", abs(l["cout_appel_usd"] - cout) < 1e-12,
        str(l["cout_appel_usd"]))
verifie("cout annonce par le fournisseur trace aussi", l["cout_annonce_usd"] == 0.000123)
verifie("cumul present", abs(l["cout_cumule_usd"] - cout) < 1e-12)
verifie("raisonnement inscrit dans la trace", l["raisonnement"] == "off")

print("4. Le raisonnement : desactivation explicite, et verification sur la reponse")
verifie("le defaut du client est la desactivation explicite",
        R6.ClientChat("x").raisonnement == "off")
remise_a_zero([BON])
r, _ = joue("raison1", limite=1, raisonnement="off")
verifie("off envoie enabled false et exclude true",
        SCENARIO.requetes[0]["charge"]["reasoning"] == {"enabled": False, "exclude": True},
        str(SCENARIO.requetes[0]["charge"].get("reasoning")))
remise_a_zero([BON])
joue("raison1b", limite=1, raisonnement="none")
verifie("none envoie effort none et exclude true",
        SCENARIO.requetes[0]["charge"]["reasoning"] == {"effort": "none", "exclude": True},
        str(SCENARIO.requetes[0]["charge"].get("reasoning")))
remise_a_zero([BON])
joue("raison2", limite=1, raisonnement="low")
verifie("low envoie effort low",
        SCENARIO.requetes[0]["charge"]["reasoning"] == {"effort": "low", "exclude": True})
remise_a_zero([BON])
joue("raison3", limite=1, raisonnement="aucun")
verifie("aucun n'envoie rien, a reserver au serveur local",
        "reasoning" not in SCENARIO.requetes[0]["charge"])

# La desactivation se verifie sur la reponse, jamais sur le parametre envoye. C'est ce que
# l'essai a blanc du 9 septembre a manque : `aucun` etait passe, le modele raisonnait, et
# 165 jetons de raisonnement etaient factures a chaque cellule.
remise_a_zero([BON], raisonnement=0)
r, _ = joue("raison4", limite=2, raisonnement="off")
verifie("raisonnement desactive effectif : oui quand les jetons sont nuls",
        r["raisonnement_desactive_effectif"] == "oui",
        r["raisonnement_desactive_effectif"])
remise_a_zero([BON], raisonnement=165)
r, lignes = joue("raison5", limite=2, raisonnement="off")
verifie("raisonnement desactive effectif : non des qu'un jeton est facture",
        r["raisonnement_desactive_effectif"] == "non",
        r["raisonnement_desactive_effectif"])
verifie("le maximum de jetons de raisonnement est publie",
        r["jetons_raisonnement_max"] == 165)
verifie("les jetons de raisonnement restent dans le cumul de cout",
        lignes[0]["jetons_sortie"] == 20)


class SansCompte(Faux):
    """Un fournisseur qui ne compte pas les jetons de raisonnement."""

    def do_POST(self):
        n = int(self.headers.get("Content-Length", 0))
        charge = json.loads(self.rfile.read(n).decode("utf-8"))
        SCENARIO.requetes.append({"charge": charge, "entetes": dict(self.headers)})
        corps = json.dumps({
            "id": "gen-test", "model": charge["model"], "provider": "SansCompte",
            "choices": [{"message": {"content": SCENARIO.suivant()},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 300, "completion_tokens": 20},
        }).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)


serveur3 = HTTPServer(("127.0.0.1", 0), SansCompte)
threading.Thread(target=serveur3.serve_forever, daemon=True).start()
remise_a_zero([BON])
r, _ = joue("raison6", limite=1,
            base=f"http://127.0.0.1:{serveur3.server_address[1]}/api/v1")
verifie("raisonnement desactive effectif : inconnu quand rien n'est compte",
        r["raisonnement_desactive_effectif"].startswith("inconnu"),
        r["raisonnement_desactive_effectif"])

print("4b. --fin-seulement ne donne au parse que la fin de la sortie")
# Un raisonnement en clair qui contient lui meme une ligne au format demande : c'est le
# seul cas ou le parse strict de R1 ne suffit plus, et le seul qui justifie --fin-seulement.
BAVARD = "We need to answer.\nA: 30\nLet me think again.\nA: 60\nB: 40"
remise_a_zero([BAVARD])
r, lignes = joue("fin1", limite=1, fin_seulement=0)
verifie("sortie entiere : le raisonnement bavard fait rejeter la cellule",
        lignes[0]["rejet"] is True, lignes[0]["motif_rejet"])
remise_a_zero([BAVARD])
r, lignes = joue("fin2", limite=1, fin_seulement=2)
verifie("deux dernieres lignes : la distribution se lit",
        lignes[0]["distribution"] == {"Yes": 0.6, "No": 0.4},
        str(lignes[0]["distribution"]))
verifie("fin_seulement inscrit dans la trace", lignes[0]["fin_seulement"] == 2)
verifie("usage inclus demande", SCENARIO.requetes[0]["charge"]["usage"] == {"include": True})
# urllib normalise la casse des noms d'en tete ; HTTP les declare insensibles a la casse,
# la comparaison se fait donc en minuscules.
_recus = {k.lower(): v for k, v in SCENARIO.requetes[0]["entetes"].items()}
verifie("en tetes HTTP-Referer et X-Title a popsim",
        _recus.get("http-referer") == "popsim" and _recus.get("x-title") == "popsim",
        str({k: v for k, v in _recus.items() if k in ("http-referer", "x-title")}))
verifie("la cle d'API part en Bearer et n'est jamais tracee",
        _recus.get("authorization", "").startswith("Bearer "))

print("5. Plafond dur en USD")
# 1 000 jetons d'entree a 1e-6 : 0,001 USD par cellule, presque cinq fois l'estimation a
# priori de la v2 (210 jetons). Le plafond doit tenir quand meme.
remise_a_zero([BON], jetons=(1000, 0))
SCENARIO.cout = None
r, lignes = joue("plafond1", plafond=0.0025)
verifie("le plafond arrete le run", r["plafond_atteint"] is True)
verifie("2 cellules jouees sur 4", r["cellules"] == 2, str(r["cellules"]))
verifie("le cumul ne depasse jamais le plafond", r["cout_usd"] <= 0.0025 + 1e-12,
        str(r["cout_usd"]))
verifie("PLAFOND ATTEINT ecrit dans le journal",
        "PLAFOND ATTEINT" in open(R6.JOURNAL, encoding="utf-8").read())

print("6. Fichier d'arret R6 dédié et STOP global utilisateur en lecture seule")
remise_a_zero([BON])
r7_temoin = os.path.join(TMP, "R7-ACTIF")
with open(r7_temoin, "w") as fh:
    fh.write("euler-actif\n")
SCENARIO.au_ieme_appel = {2: lambda: open(R6.FICHIER_ARRET_R6, "w").close()}
r, lignes = joue("stop1")
verifie("arret demande signale", r["arret_demande"] is True)
verifie("2 cellules ecrites puis arret propre", r["cellules"] == 2, str(r["cellules"]))
verifie("trace relisible en entier", len(lignes) == 2)
verifie("ARRET DEMANDE ecrit dans le journal",
        "ARRET DEMANDE" in open(R6.JOURNAL, encoding="utf-8").read())
verifie("le script n'efface pas STOP-R6", os.path.exists(R6.FICHIER_ARRET_R6))
verifie("STOP-R6 ne modifie pas le témoin R7",
        open(r7_temoin).read() == "euler-actif\n"
        and not os.path.exists(R6.FICHIER_ARRET_GLOBAL))

print("7. Reprise sur trace existante")
os.remove(R6.FICHIER_ARRET_R6)
remise_a_zero([BON])
r2, lignes2 = joue("stop1")
verifie("les 2 cellules manquantes sont jouees, pas les 2 deja faites",
        r2["cellules"] == 2 and r2["deja_faites"] == 2,
        f"{r2['cellules']}/{r2['deja_faites']}")
verifie("la trace complete compte 4 cellules", len(lignes2) == 4)
verifie("aucune cellule en double",
        len({(l["item"], l["camp"], l["identite"]) for l in lignes2}) == 4)
remise_a_zero([BON])
r3, _ = joue("stop1")
verifie("une troisieme relance ne rejoue rien et n'appelle rien",
        r3["cellules"] == 0 and SCENARIO.appels == 0, str(r3["cellules"]))

print("8. Feu vert GO-R6")
verifie("feu vert absent au depart", R6.feu_vert() is False)
open(R6.FICHIER_GO, "w").close()
verifie("feu vert present une fois pose", R6.feu_vert() is True)
os.remove(R6.FICHIER_GO)
verifie("un modele gratuit a une estimation d'appel nulle",
        R6.Budget(1.0, 0.0, 0.0).estimation_appel() == 0.0)

print("9. Un 429 est un incident de transport, jamais un rejet de parse")
# Le defaut du 9 septembre : le client comptait un 429 comme un rejet de format, et
# google/gemma-4-31b-it:free sortait a 100 pour cent de rejets alors qu'il n'avait rien
# repondu. Un rejet est un echec de parse sur une reponse RECUE.
remise_a_zero([BON], codes=[429, 429, 200])
r, lignes = joue("reprise1", limite=1)
verifie("la cellule est rejouee et finit par aboutir",
        r["cellules"] == 1 and r["rejets"] == 0, f"{r['cellules']}/{r['rejets']}")
verifie("3 tentatives pour une cellule", lignes[0]["appels_de_transport"] == 3,
        str(lignes[0]["appels_de_transport"]))
verifie("les attentes croissent : 5 puis 20 s", DORMI == [5, 20], str(DORMI))
verifie("2 incidents comptes a part", r["erreurs_reseau"] == 2, str(r["erreurs_reseau"]))
verifie("le taux de rejet reste nul", r["taux_rejet"] == 0.0)
verifie("les statuts sont comptes", r["statuts_reseau"] == {"429": 2},
        str(r["statuts_reseau"]))
verifie("les incidents sont inscrits sur la ligne de la cellule",
        len(lignes[0]["incidents_transport"]) == 2
        and lignes[0]["incidents_transport"][0]["statut"] == 429)
verifie("aucune cellule non jouee", r["non_jouees"] == 0 and non_jouees("reprise1") == [])

remise_a_zero([BON], codes=[429, 429, 429, 200, 200])
r, lignes = joue("seuil429-trois", limite=2, items=ITEMS[:2])
verifie("trois 429 sur une fenetre de vingt restent dans le seuil du plan",
        not r["arret_seuil_429"] and r["cellules"] == 2 and SCENARIO.appels == 5
        and r["appels_fenetre_429"] == 5,
        f"{r['erreurs_429_fenetre']}/{r['appels_fenetre_429']}")

remise_a_zero([BON], codes=[429] * 8)
r, lignes = joue("reprise2", items=ITEMS[:2])
verifie("la quatrieme 429 franchit le seuil 3 sur 20 et arrete le run entier",
        r["non_jouees"] == 1 and r["cellules"] == 0 and r["arret_seuil_429"]
        and r["erreurs_429_fenetre"] == 4 and r["appels_fenetre_429"] == 4,
        f"{r['non_jouees']}/{r['cellules']}/{r['erreurs_429_fenetre']}")
verifie("aucun rejet de parse", r["rejets"] == 0 and r["taux_rejet"] == 0.0)
verifie("aucune tentative de la cellule suivante", r["erreurs_reseau"] == 4
        and SCENARIO.appels == 4, f"{r['erreurs_reseau']}/{SCENARIO.appels}")
verifie("les seules attentes sont 5, 20, 60", DORMI == [5, 20, 60], str(DORMI))
nj = non_jouees("reprise2")
verifie("la cellule non jouee est ecrite dans son propre fichier", len(nj) == 1)
verifie("elles portent non_jouee et le statut", nj[0]["non_jouee"] is True
        and nj[0]["statut"] == 429 and nj[0]["tentatives"] == 4)
verifie("la trace principale reste vide de ces cellules", lignes == [])
verifie("un incident de transport ne coute rien au budget", r["cout_usd"] == 0.0)

remise_a_zero([BON])
r2, lignes2 = joue("reprise2", items=ITEMS[:2])
verifie("la reprise rejoue les cellules non jouees",
        r2["cellules"] == 2 and r2["deja_faites"] == 0,
        f"{r2['cellules']}/{r2['deja_faites']}")
verifie("elles sont maintenant lues", len(lignes2) == 2 and not lignes2[0]["rejet"])

print("9b. Un code non rejouable n'est pas rejoue")
remise_a_zero([BON], codes=[400, 400])
SCENARIO.entetes_erreur = {
    "X-Generation-Id": "gen-erreur-test",
    "X-Provider": "FournisseurTest",
    "X-Request-Id": "req-erreur-test",
    "Authorization": "secret-a-ne-jamais-journaliser",
}
r, lignes = joue("err400", limite=1)
verifie("400 : une seule tentative", r["erreurs_reseau"] == 1, str(r["erreurs_reseau"]))
verifie("400 : cellule non jouee, pas rejet", r["non_jouees"] == 1 and r["rejets"] == 0)
verifie("400 : aucune attente", DORMI == [], str(DORMI))
verifie("400 : le statut est consigne", non_jouees("err400")[0]["statut"] == 400)
diag = non_jouees("err400")[0]["incidents"][0]["diagnostic_http"]
verifie("identifiants HTTP non secrets conserves sur erreur", diag == {
    "generation_id": "gen-erreur-test", "provider": "FournisseurTest",
    "request_id": "req-erreur-test"}, str(diag))
journal_http = os.path.join(TMP, "reprise", "r6-erreurs-http-privees.jsonl")
contenu_http = open(journal_http, encoding="utf-8").read()
verifie("journal HTTP prive ecrit avant la sortie", "gen-erreur-test" in contenu_http)
verifie("journal HTTP prive limite au proprietaire",
        os.stat(journal_http).st_mode & 0o777 == 0o600)
verifie("entete secret hors liste jamais journalise",
        "secret-a-ne-jamais-journaliser" not in contenu_http)

remise_a_zero([BON])
SCENARIO.erreur_corps = 502
SCENARIO.entetes_erreur = {"X-Generation-Id": "gen-erreur-corps",
                           "X-Request-Id": "req-erreur-corps"}
r, _ = joue("err-corps-502", limite=1)
diag_corps = non_jouees("err-corps-502")[0]["incidents"][0]["diagnostic_http"]
verifie("erreur fournisseur dans un HTTP 200 conserve aussi les identifiants",
        r["reconciliation_requise"] and diag_corps == {
            "generation_id": "gen-erreur-corps", "request_id": "req-erreur-corps"},
        str(diag_corps))

print("10. Le plan de cellules de la v2, et la liste tiree d'avance")
verifie("F1 declare 894 cellules", R6.PLANS["f1"]["cellules"] == 894)
verifie("F2 declare 316 cellules", R6.PLANS["f2"]["cellules"] == 316)
verifie("F1 en format gabarit seul", R6.PLANS["f1"]["format"] == "q4")
verifie("F2 en gabarit plus trois exemples", R6.PLANS["f2"]["format"] == "q4gab3")
verifie("F2 ne joue que gauche et droite", R6.PLANS["f2"]["camps"] == ["gauche", "droite"])
faux_items = [f"i{n:03d}" for n in range(149)]
n_f1 = len(list(R1.cellules(faux_items, R6.PLANS["f1"]["camps"], R6.PLANS["f1"]["identites"])))
n_f2 = len(list(R1.cellules(faux_items[:79], R6.PLANS["f2"]["camps"],
                            R6.PLANS["f2"]["identites"])))
verifie("F1 fait bien 894 cellules a l'enumeration", n_f1 == 894, str(n_f1))
verifie("F2 fait bien 316 cellules a l'enumeration", n_f2 == 316, str(n_f2))
liste = R6.tirer_liste(faux_items, R6.PLANS["f1"]["camps"], R6.PLANS["f1"]["identites"], 40)
verifie("40 cellules tirees, toutes distinctes",
        len(liste) == 40 and len(set(liste)) == 40)
verifie("le tirage est reproductible a graine fixe",
        liste == R6.tirer_liste(faux_items, R6.PLANS["f1"]["camps"],
                                R6.PLANS["f1"]["identites"], 40))
chemin_liste = os.path.join(TMP, "liste.txt")
R6.ecrire_liste(liste, chemin_liste)
verifie("la liste ecrite se relit a l'identique", R6.lire_liste(chemin_liste) == liste)

print("11. Resume d'essai")
remise_a_zero([BON], jetons=(300, 20), raisonnement=3)
r, lignes = joue("essai1", limite=2)
chemin, e = R6.resume_essai(r, "essai1", 894)
verifie("resume d'essai ecrit", os.path.exists(chemin))
verifie("cout par cellule reel", abs(e["cout_par_cellule_usd"] - 0.000123) < 1e-12,
        str(e["cout_par_cellule_usd"]))
verifie("projection sur les 894 cellules du plan",
        abs(e["projection_plan_usd"] - round(e["cout_par_cellule_usd"] * 894, 6)) < 1e-9,
        str(e["projection_plan_usd"]))
verifie("taux de rejet dans le resume", e["taux_rejet"] == 0.0)
verifie("latence mesuree", e["latence_ms_mediane"] is not None)
verifie("jetons de raisonnement moyens mesures", e["jetons_raisonnement_moyens"] == 3.0)
verifie("la ligne raisonnement desactive effectif est dans le resume d'essai",
        "raisonnement_desactive_effectif" in e)
verifie("elle vaut non quand des jetons de raisonnement sont factures",
        e["raisonnement_desactive_effectif"] == "non",
        str(e["raisonnement_desactive_effectif"]))
verifie("l'essai n'est pas declare propre dans ce cas", e["essai_propre"] is False)
remise_a_zero([BON], jetons=(300, 20), raisonnement=0)
r, _ = joue("essai2", limite=2)
_, e2 = R6.resume_essai(r, "essai2", 894)
verifie("essai incomplet (2/10) ne donne pas de feu vert",
        e2["essai_propre"] is False and e2["raisonnement_desactive_effectif"] == "oui")
verifie("les incidents de transport sont dans le resume d'essai",
        "erreurs_reseau" in e2 and "non_jouees" in e2)

print("12. Regressions de l'audit du 10 septembre")

def refuse(nom, action):
    try:
        action()
    except (ValueError, BlockingIOError):
        verifie(nom, True)
    else:
        verifie(nom, False)

for invalide in (float("nan"), float("inf"), -1, None, True):
    refuse("budget invalide refuse", lambda v=invalide: R6.Budget(v, 0, 0))
refuse("tarif absent refuse", lambda: R6.prix("x", {"data": [{"id": "x"}]}))
b = R6.Budget(1, 1e-6, 2e-6)
verifie("cout annonce superieur aux jetons compte", b.ajouter(1, 1, 0.4) == 0.4)
verifie("cout annonce nul respecte", b.ajouter(1, 1, 0) == 0)
refuse("usage absent ne devient pas un cout nul", lambda: b.ajouter(None, None))
refuse("cout NaN refuse", lambda: b.ajouter(1, 1, float("nan")))

remise_a_zero()
r, _ = joue("budget-reprise", limite=2)
remise_a_zero()
r, lignes = joue("budget-reprise", plafond=0.0004)
verifie("reprise garde le cumul et arrete avant nouvel appel",
        SCENARIO.appels == 0 and abs(r["cout_usd"] - 0.000246) < 1e-12)
refuse("changement de max/raisonnement refuse",
       lambda: joue("budget-reprise", raisonnement="low"))
remise_a_zero()
r, lignes = joue("doublons", items=["item_a", "item_a"])
verifie("doublon dans la meme liste jamais rachete", SCENARIO.appels == 1 and len(lignes) == 1)
with open(R6.chemin_trace("tronquee"), "w") as fh:
    fh.write('{"item":')
refuse("trace tronquee bloque avant reseau", lambda: joue("tronquee"))

remise_a_zero(codes=[429, 200])
def stop_pendant_attente(s):
    open(R6.FICHIER_ARRET_R6, "w").close()
with patch(__name__ + ".dormir", stop_pendant_attente):
    r, lignes = joue("stop-retry", limite=1)
verifie("STOP pendant backoff interdit la deuxieme tentative",
        SCENARIO.appels == 1 and r["arret_demande"] and not lignes)
os.remove(R6.FICHIER_ARRET_R6)

remise_a_zero(codes=[503, 200])
r, lignes = joue("cout-incertain")
verifie("503 : un appel, aucun rejet, reconciliation imposee",
        SCENARIO.appels == 1 and r["reconciliation_requise"] and not lignes)
refuse("503 bloque aussi la reprise", lambda: joue("cout-incertain"))
remise_a_zero()
with patch.object(R6, "_lire", side_effect=TimeoutError("secret-a-ne-pas-tracer")):
    r, _ = joue("timeout")
verifie("timeout conserve le marqueur et masque le message",
        r["reconciliation_requise"] and "secret-a-ne-pas-tracer" not in
        open(os.path.join(TMP, "r6-timeout-non-jouees.jsonl")).read())
refuse("timeout ne se rejoue pas", lambda: joue("timeout"))
remise_a_zero()
SCENARIO.cout = None
SCENARIO.jetons = (None, None)
refuse("usage absent bloque", lambda: joue("usage-absent"))
verifie("marqueur conserve quand cout absent",
        os.path.exists(R6.chemin_trace("usage-absent") + ".en-cours"))
refuse("cout absent bloque reprise", lambda: joue("usage-absent"))

remise_a_zero()
with patch.object(R6, "_lire", side_effect=KeyboardInterrupt):
    try:
        joue("crash")
    except KeyboardInterrupt:
        pass
refuse("interruption apres envoi bloque reprise", lambda: joue("crash"))
with open(R6.chemin_trace("verrou"), "a") as verrou:
    R6.fcntl.flock(verrou, R6.fcntl.LOCK_EX | R6.fcntl.LOCK_NB)
    refuse("deux runs sur meme trace interdits", lambda: joue("verrou"))
refuse("payant distant bloque meme sans STOP",
       lambda: joue("payant", base=R6.BASE))
with patch.object(R6, "catalogue", return_value={"data": [{
        "id": "fixture/payant", "pricing": {"prompt": "0.000001",
                                               "completion": "0.000002"}}]}):
    try:
        R6.main(["--modele", "fixture/payant", "--plafond", "1"])
    except SystemExit as e:
        verifie("GO absent bloque le CLI payant avant lecture de cle", "feu vert absent" in str(e))
with open(R6.FICHIER_ARRET_R6, "w") as fh:
    fh.write("signal-r6\n")
with patch.object(R6, "catalogue", side_effect=AssertionError("reseau interdit")):
    try:
        R6.main(["--catalogue"])
    except SystemExit as e:
        verifie("STOP-R6 bloque le CLI avant tout reseau", "STOP-R6" in str(e))
verifie("STOP-R6 seulement lu, contenu intact",
        open(R6.FICHIER_ARRET_R6).read() == "signal-r6\n")
os.remove(R6.FICHIER_ARRET_R6)
with open(R6.FICHIER_ARRET_GLOBAL, "w") as fh:
    fh.write("signal-utilisateur\n")
with patch.object(R6, "catalogue", side_effect=AssertionError("reseau interdit")):
    try:
        R6.main(["--catalogue"])
    except SystemExit as e:
        verifie("STOP CLI precede catalogue et lecture de cle", "arret" in str(e))
verifie("STOP global seulement lu, contenu intact",
        open(R6.FICHIER_ARRET_GLOBAL).read() == "signal-utilisateur\n")
os.remove(R6.FICHIER_ARRET_GLOBAL)
verifie("1210 campagne + 40 repetitions + 20 essais = 1270",
        R6.PLANS["f1"]["cellules"] + R6.PLANS["f2"]["cellules"] + 40 + 20 == 1270)

print("13. Registre global et preflight hors ligne, aucun lancement")
ledger = os.path.join(TMP, "campagne-r6.jsonl")
ancien = os.path.join(TMP, "ancien.jsonl")
with open(ancien, "w") as fh:
    fh.write("historique temoin\n")
inventaire = {ancien: R6.hashlib.sha256(open(ancien, "rb").read()).hexdigest()}
id1 = R6.identite_campagne("m1", "q4", "v1", "a", "gauche", "journaliste")
id2 = R6.identite_campagne("m2", "q4gab3", "v2", "a", "gauche", "journaliste")
snapshot = {"data": {"limit": 4, "limit_remaining": 4, "limit_reset": None}}
with R6.RegistreGlobal(ledger) as reg:
    refuse("registre vide ne permet pas reservation", lambda: reg.reserver(id1, 1, 6))
    reg.initialiser(inventaire, {id1: "0.10"})
    verifie("budget global 4.40 compte historique et reserve",
            reg.restant("5.931371505") == R6.Decimal("4.30"))
    refuse("verrou global tous modeles", lambda: R6.RegistreGlobal(ledger).__enter__())
    diagnostic = R6.preflight_cle(snapshot, "5.931371505", reg, inventaire, 150,
                                  {"prompt": "1", "completion": "2"})
    verifie("preflight conforme ne lance ni autorise generation",
            diagnostic["conditions_cle_valides"] and not diagnostic["autorise_generation"])
    for mauvaise in (None, float("nan"), float("inf"), -1, 0):
        refuse("limit_remaining absent, non fini ou épuise",
            lambda x=mauvaise: R6.preflight_cle({"data": dict(snapshot["data"], limit_remaining=x)},
                "5.931371505", reg, inventaire, 150, {"prompt": 1, "completion": 2}))
    diagnostic_cle_large = R6.preflight_cle(
        {"data": dict(snapshot["data"], limit="4.40", limit_remaining="4.40")},
        "5.931371505", reg, inventaire, 150, {"prompt": 1, "completion": 2})
    verifie("reste de clé plus haut ne force pas à financer tout le plafond",
            diagnostic_cle_large["budget"]["plafond_effectif_usd"] == "4.30")
    for mauvaise in (None, float("nan"), float("inf"), 0, "4.401"):
        refuse("limit doit être fini et dans ]0, 4.40]",
            lambda x=mauvaise: R6.preflight_cle(
                {"data": dict(snapshot["data"], limit=x)}, "5.931371505", reg,
                inventaire, 150, {"prompt": 1, "completion": 2}))
    branches_cle = []
    for modif in ({"limit": None}, {"limit_remaining": float("inf")},
                  {"limit": 4, "limit_remaining": "4.01"}, {"limit_reset": "daily"}):
        try:
            R6.preflight_cle({"data": dict(snapshot["data"], **modif)},
                             "5.931371505", reg, inventaire, 150,
                             {"prompt": 1, "completion": 2})
        except R6.ErreurPreflight as exc:
            branches_cle.append(exc.branche)
    verifie("branches exactes pour clé absente, non finie, incohérente et reset",
            branches_cle == ["limite_cle_absente", "reste_cle_non_fini",
                              "reste_cle_superieur_limite", "reset_cle_non_nul"])
    snapshot_sans_reset = {"data": {k: v for k, v in snapshot["data"].items()
                                      if k != "limit_reset"}}
    branche_reset_absent = None
    try:
        R6.preflight_cle(snapshot_sans_reset, "5.931371505", reg, inventaire, 150,
                         {"prompt": 1, "completion": 2})
    except R6.ErreurPreflight as exc:
        branche_reset_absent = exc.branche
    verifie("champ limit_reset absent refusé explicitement",
            branche_reset_absent == "reset_cle_absent")
    refuse("reset periodique refuse", lambda: R6.preflight_cle(
        {"data": dict(snapshot["data"], limit_reset="daily")}, 6, reg, inventaire,
        150, {"prompt": 1, "completion": 2}))
    refuse("prix de routage incomplet refuse", lambda: R6.preflight_cle(
        snapshot, 6, reg, inventaire, 150, {"prompt": 1}))
    refuse("inventaire omis refuse", lambda: reg.verifier_integrite({}))
    refuse("ancienne cellule ne se rachete pas", lambda: reg.reserver(id1, 1, 6))
    reg.reserver(id2, "0.25", "5.931371505", plafond_modele_usd="1.00",
                 empreinte_requete="a" * 64,
                 fournisseur_impose="Fixture")
    verifie("reservation ajoutee au global", reg.total() == R6.Decimal("0.35"))
with R6.RegistreGlobal(ledger) as reg:
    verifie("reservation ambigue survit reprise", reg.operations[id2]["etat"] == "reservation")
    refuse("aucun autre modele tant que cout ambigu", lambda: reg.reserver(id1, 1, 6))
    refuse("preflight bloque si appel ambigu", lambda: R6.preflight_cle(
        snapshot, 6, reg, inventaire, 150, {"prompt": 1, "completion": 2}))
    refuse("reconciliation sans preuve refusee", lambda: reg.reconcilier(id2, 0, ""))
    reg.reconcilier(id2, "0.30", "facture-fixture-1")
    verifie("cout reel au dela reservation conserve", reg.total() == R6.Decimal("0.40"))
    refuse("nouveau suffixe ne libere pas identite reglee", lambda: reg.reserver(id2, 1, 6))
with R6.RegistreGlobal(ledger) as reg:
    branche_sans_limite = None
    try:
        R6.preflight_cle(
            {"data": {"usage": 0, "limit": None, "limit_remaining": None,
                      "limit_reset": None, "is_management_key": False}},
            "5.931371505", reg, inventaire, 150, {"prompt": 1, "completion": 2})
    except R6.ErreurPreflight as exc:
        branche_sans_limite = exc.branche
    verifie("clé sans limite finie refusée avec branche exacte",
            branche_sans_limite == "limite_cle_absente")

print("14. Import historique scelle et transaction payante entierement factice")
diagnostic_ok = None
with R6.RegistreGlobal(ledger) as reg:
    diagnostic_ok = R6.preflight_cle(snapshot, "5.931371505", reg, inventaire, 150,
                                     {"prompt": 1, "completion": 2}, "0.01", 1000)
verifie("borne complete rend le preflight autorisant",
        diagnostic_ok["autorise_generation"] and diagnostic_ok["borne_appel_usd"] == "0.01")
with R6.RegistreGlobal(ledger) as reg:
    refuse("borne inferieure au calcul max_tokens/max_price refusee", lambda: R6.preflight_cle(
        snapshot, "5.931371505", reg, inventaire, 150,
        {"prompt": 10, "completion": 20}, "0.0001", 1000))

trace_import = os.path.join(TMP, "trace-a-importer.jsonl")
historique_lu = {
    "modele": "fixture/modele", "format": "q4", "version_prompt": R6.FORMATS["q4"],
    "item": "item_a", "camp": "gauche", "identite": "journaliste",
    "fournisseur": "FauxFournisseur", "cout_annonce_usd": 0.02,
    "cout_appel_usd": 0.02, "erreur": None,
}
historique_ambigu = dict(historique_lu, item="item_b", cout_annonce_usd=None,
                         cout_appel_usd=0, erreur="incident historique")
with open(trace_import, "w") as fh:
    fh.write(json.dumps(historique_lu) + "\n")
    fh.write(json.dumps(historique_ambigu) + "\n")
manifest = os.path.join(TMP, "import-r6.json")
with open(manifest, "w") as fh:
    json.dump({"version": "R6-v2-import-1", "exhaustif": True,
               "attendus": {"lignes": 2, "reponses": 1, "incidents": 1,
                             "cout_annonce_reponses_usd": "0.02"},
               "traces": [{"chemin": trace_import, "passe": "ancien-pilote",
                            "classe": "ancien-pilote",
                            "sha256": R6.hashlib.sha256(open(trace_import, "rb").read()).hexdigest(),
                            "attendus": {"lignes": 2, "reponses": 1, "incidents": 1}}]}, fh)
inventaire_import, evenements_import = R6.charger_import(manifest)
ledger_cli = os.path.join(TMP, "registre-cli.jsonl")
verifie("CLI initialise le registre sans lire de cle ni faire de reseau",
        R6.main(["--initialiser-registre", "--manifeste-import", manifest,
                 "--registre", ledger_cli]) == 0 and os.path.exists(ledger_cli))
ledger_import = os.path.join(TMP, "registre-import.jsonl")
with R6.RegistreGlobal(ledger_import) as reg:
    reg.initialiser_evenements(inventaire_import, evenements_import)
    verifie("migration conserve cout, fournisseur et empreinte source",
            reg.total() == R6.Decimal("0.02") and
            all(e.get("fournisseur_impose") == "FauxFournisseur" for e in reg.operations.values()) and
            all(e.get("source_sha256") for e in reg.operations.values()))
    verifie("incident historique sans cout reste ambigu",
            any(e["etat"] == "reservation" for e in reg.operations.values()))
    refuse("incident migre bloque tout nouvel achat", lambda: reg.reserver(
        R6.identite_campagne("autre", "q4", "v", "x", "gauche", "journaliste"),
        0.01, 6, empreinte_requete="b" * 64, fournisseur_impose="Fixture"))

manifest_borne = os.path.join(TMP, "import-r6-borne.json")
with open(manifest_borne, "w") as fh:
    json.dump({"version": "R6-v2-import-1", "exhaustif": True,
               "attendus": {"lignes": 2, "reponses": 1, "incidents": 1,
                             "cout_annonce_reponses_usd": "0.02",
                             "borne_incidents_total_usd": "0"},
               "cout_incidents": {"observation": "inconnu", "borne_unitaire_usd": "0",
                                  "fondement_borne": "modele :free du catalogue local"},
               "traces": [{"chemin": trace_import, "passe": "ancien-pilote",
                            "classe": "ancien-pilote",
                            "sha256": R6.hashlib.sha256(open(trace_import, "rb").read()).hexdigest(),
                            "attendus": {"lignes": 2, "reponses": 1, "incidents": 1}}]}, fh)
_inventaire_borne, evenements_bornes = R6.charger_import(manifest_borne)
verifie("incident garde cout inconnu et borne distincte sans fausse preuve par la cle actuelle",
        len(evenements_bornes) == 2
        and any(e["type"] == "historique-incertain" and e.get("cout_observe") == "inconnu"
                and e.get("nature_usd") == "borne" for e in evenements_bornes))

ledger_tx = os.path.join(TMP, "registre-transaction.jsonl")
with R6.RegistreGlobal(ledger_tx) as reg:
    reg.initialiser_evenements(inventaire, [])
max_price = {"prompt": "1", "completion": "2"}
client_tx = R6.ClientChat("cle-factice", base=BASE, fournisseur="FauxFournisseur",
                          max_price=max_price)
lectures = []
def cle_fraiche(_cle):
    lectures.append("key")
    return {"data": {"limit": 4.4, "limit_remaining": 4.4, "limit_reset": None}}
def solde_frais(_cle):
    lectures.append("credits")
    return {"total_credits": 155, "total_usage": 149.068628495}
transaction = R6.TransactionPayante(ledger_tx, inventaire, "campagne", "0.002", 1000,
                                     cle_fraiche, solde_frais, plafond_modele="1.00")
referent_factice = os.path.join(TMP, "referent.csv")
with open(referent_factice, "w") as fh:
    fh.write("referent factice\n")
sha_ref = R6.hashlib.sha256(open(referent_factice, "rb").read()).hexdigest()
open(R6.FICHIER_GO, "w").close()
remise_a_zero([BON], jetons=(300, 20), raisonnement=0)
with patch.object(R6, "REFERENT", referent_factice), patch.object(R6, "REFERENT_SHA", sha_ref):
    budget_tx = R6.Budget(4.5, 1e-6, 2e-6)
    rtx = R6.lancer(client_tx, "fixture/modele-payant", "q4", TABLE,
                    [("gauche", "journaliste", "item_a")], budget_tx, "transaction-ok",
                    n_predict=40, transaction=transaction)
verifie("transaction lit GET /key puis solde frais sous garde", lectures == ["key", "credits"])
charge_tx = SCENARIO.requetes[-1]["charge"]
verifie("max_tokens et provider.max_price partent dans la requete",
        charge_tx["max_tokens"] == 40 and charge_tx["provider"]["max_price"] ==
        {"prompt": 1.0, "completion": 2.0})
ligne_tx = json.loads(open(R6.chemin_trace("transaction-ok")).readline())
verifie("trace porte empreinte et fournisseur impose",
        len(ligne_tx["empreinte_requete"]) == 64 and
        ligne_tx["fournisseur_impose"] == "FauxFournisseur")
with R6.RegistreGlobal(ledger_tx) as reg:
    operation_tx = next(iter(reg.operations.values()))
    verifie("reservation rapprochee par identifiant de facture",
            operation_tx["etat"] == "reglee" and operation_tx["preuve"] == "gen-test")
preflight_log = os.path.join(TMP, "reprise", "r6-preflights-prives.jsonl")
diag_trace = json.loads(open(preflight_log).readlines()[-1])
verifie("snapshot non secret et branche exacte conservés sur autorisation",
        diag_trace["branche"] == "autorise"
        and diag_trace["snapshot_cle_non_secret"]["limit_remaining"] == 4.4
        and "authorization" not in json.dumps(diag_trace).lower())

ledger_refus_effectif = os.path.join(TMP, "registre-refus-effectif.jsonl")
with R6.RegistreGlobal(ledger_refus_effectif) as reg:
    reg.initialiser_evenements(inventaire, [])
def cle_trop_basse(_cle):
    return {"data": {"limit": 4.4, "limit_remaining": "0.0005", "limit_reset": None}}
transaction_refus = R6.TransactionPayante(
    ledger_refus_effectif, inventaire, "campagne", "0.002", 1000,
    cle_trop_basse, solde_frais, plafond_modele="1.00")
appels_avant_refus = SCENARIO.appels
branche_refus = None
with patch.object(R6, "verifier_referent", lambda: None):
    try:
        transaction_refus.appeler(
            client_tx, "fixture/modele-payant", "q4", R6.FORMATS["q4"],
            "item_refus", "gauche", "journaliste",
            R6.invite("item_a", "gauche", "journaliste", "q4", TABLE)[0], 40,
            os.path.join(TMP, "refus-effectif.en-cours"))
    except R6.ErreurPreflight as exc:
        branche_refus = exc.branche
verifie("plafond effectif insuffisant donne une branche précise",
        branche_refus == "plafond_effectif_insuffisant")
verifie("refus de plafond effectif précède réservation et POST",
        SCENARIO.appels == appels_avant_refus
        and not os.path.exists(os.path.join(TMP, "refus-effectif.en-cours")))
diag_refus = json.loads(open(preflight_log).readlines()[-1])
verifie("snapshot non secret du refus est persisté en privé",
        diag_refus["resultat"] == "refuse"
        and diag_refus["branche"] == "plafond_effectif_insuffisant"
        and diag_refus["budget"]["key_limit_remaining_usd"] == "0.0005")

ledger_ambigu = os.path.join(TMP, "registre-ambigu.jsonl")
with R6.RegistreGlobal(ledger_ambigu) as reg:
    reg.initialiser_evenements(inventaire, [])
transaction_ambigu = R6.TransactionPayante(ledger_ambigu, inventaire, "campagne", "0.002",
                                            1000, cle_fraiche, solde_frais,
                                            plafond_modele="1.00")
remise_a_zero([BON], jetons=(300, 20), raisonnement=0)
SCENARIO.cout = None
with patch.object(R6, "verifier_referent", lambda: None):
    ramb = R6.lancer(client_tx, "fixture/autre-payant", "q4", TABLE,
                     [("gauche", "journaliste", "item_c")],
                     R6.Budget(4.5, 1e-6, 2e-6), "transaction-ambigu",
                     n_predict=40, transaction=transaction_ambigu)
with R6.RegistreGlobal(ledger_ambigu) as reg:
    verifie("cout annonce absent conserve reservation globale et bloque",
            ramb["reconciliation_requise"] and
            any(e["etat"] == "reservation" for e in reg.operations.values()))
os.remove(R6.FICHIER_GO)
lectures_avant = len(lectures)
refuse("GO absent bloque avant toute lecture fraiche", lambda: transaction.appeler(
    client_tx, "fixture/modele-payant", "q4", R6.FORMATS["q4"], "item_d", "gauche",
    "journaliste", *R6.invite("item_d", "gauche", "journaliste", "q4", TABLE)[:1],
    40, os.path.join(TMP, "jamais-cree.en-cours")))
verifie("aucun GET quand GO manque", len(lectures) == lectures_avant)

print("15. Garde cumulative des vingt appels pilote et absence de double paiement")
verifie("configuration CLI exacte du pilote acceptée hors ligne",
        R6.erreurs_configuration_pilote(
            R6.MODELE_PILOTE, R6.FOURNISSEUR_PILOTE, 10, "0.02", 150, "off", 600,
            "0.001", {"prompt": "0.11", "completion": "0.22"}) == [])
verifie("configuration CLI plus large refusée hors ligne",
        len(R6.erreurs_configuration_pilote(
            R6.MODELE_PILOTE, R6.FOURNISSEUR_PILOTE, 10, "0.021", 151, "low", 601,
            "0.0011", {"prompt": "0.111", "completion": "0.221"})) == 6)
ledger_pilote = os.path.join(TMP, "registre-pilote.jsonl")
with R6.RegistreGlobal(ledger_pilote) as reg:
    reg.initialiser_evenements(inventaire, [])
    refuse("borne pilote unitaire supérieure à 0.001 refusée", lambda: reg.reserver(
        R6.identite_campagne(R6.MODELE_PILOTE, "q4", "v", "hors-borne", "gauche",
                             "journaliste", "essai-1"),
        "0.0011", 10, empreinte_requete="c" * 64,
        fournisseur_impose=R6.FOURNISSEUR_PILOTE))
    for i in range(20):
        passe = "essai-1" if i < 10 else "essai-2"
        ident_p = R6.identite_campagne(R6.MODELE_PILOTE, "q4", "v", f"p{i}",
                                       "gauche", "journaliste", passe)
        reg.reserver(ident_p, "0.001", 10, empreinte_requete=f"{i:064x}",
                     fournisseur_impose=R6.FOURNISSEUR_PILOTE)
        reg.reconcilier(ident_p, "0.001", f"facture-pilote-{i}")
    verifie("vingt appels des deux passes cumulent exactement 0.02 USD",
            len(reg.operations_pilote()) == 20
            and reg.total_pilote() == R6.Decimal("0.020"))
    refuse("vingt-et-unième appel pilote refusé sous verrou", lambda: reg.reserver(
        R6.identite_campagne(R6.MODELE_PILOTE, "q4", "v", "p20", "gauche",
                             "journaliste", "essai-2"),
        "0.001", 10, empreinte_requete="d" * 64,
        fournisseur_impose=R6.FOURNISSEUR_PILOTE))

ledger_pilote_preflight = os.path.join(TMP, "registre-pilote-preflight.jsonl")
with R6.RegistreGlobal(ledger_pilote_preflight) as reg:
    reg.initialiser_evenements(inventaire, [])
    diag_cas_reel = R6.preflight_cle(
        {"data": {"limit": "4.40", "limit_remaining": "4.40", "limit_reset": None}},
        "5.778549", reg, inventaire, 150,
        {"prompt": "0.11", "completion": "0.22"}, "0.001", 600, "essai-1",
        R6.MODELE_PILOTE)
    verifie("cas observé finance le pire appel sans exiger les 4.40 USD",
            diag_cas_reel["autorise_generation"]
            and diag_cas_reel["budget"]["plafond_effectif_usd"] == "4.278549")
    diag_p = R6.preflight_cle(snapshot, 6, reg, inventaire, 150,
                              {"prompt": "0.11", "completion": "0.22"},
                              "0.001", 600, "essai-1", R6.MODELE_PILOTE)
    verifie("preflight pilote accepte max_tokens 150 et publie cumul zéro",
            diag_p["autorise_generation"]
            and diag_p["pilote_cout_cumule_usd"] == "0"
            and diag_p["pilote_appels_engages"] == 0)
    refuse("max_tokens 151 refusé au pilote", lambda: R6.preflight_cle(
        snapshot, 6, reg, inventaire, 151,
        {"prompt": "0.11", "completion": "0.22"},
        "0.001", 600, "essai-1", R6.MODELE_PILOTE))
    refuse("prix maximal supérieur à la borne pilote refusé", lambda: R6.preflight_cle(
        snapshot, 6, reg, inventaire, 150,
        {"prompt": "0.111", "completion": "0.22"},
        "0.001", 600, "essai-1", R6.MODELE_PILOTE))
    branche_derivee_nulle = None
    try:
        R6.preflight_cle(snapshot, 6, reg, inventaire, 150,
                         {"prompt": "0", "completion": "0"},
                         "0.001", 600, "essai-1", R6.MODELE_PILOTE)
    except R6.ErreurPreflight as exc:
        branche_derivee_nulle = exc.branche
    verifie("prix maximaux nuls refusent une borne dérivée non positive",
            branche_derivee_nulle == "borne_derivee_non_positive")

ledger_429_payant = os.path.join(TMP, "registre-429-payant.jsonl")
with R6.RegistreGlobal(ledger_429_payant) as reg:
    reg.initialiser_evenements(inventaire, [])
transaction_429 = R6.TransactionPayante(ledger_429_payant, inventaire, "campagne", "0.002",
                                         1000, cle_fraiche, solde_frais,
                                         plafond_modele="1.00")
remise_a_zero(codes=[429])
SCENARIO.entetes_erreur = {"X-Generation-Id": "gen-429-potentiellement-facturee"}
open(R6.FICHIER_GO, "w").close()
with patch.object(R6, "verifier_referent", lambda: None):
    r429 = R6.lancer(client_tx, "fixture/payant-429", "q4", TABLE,
                     [("gauche", "journaliste", "item_d")],
                     R6.Budget(4.4, 1e-6, 2e-6), "transaction-429",
                     n_predict=40, transaction=transaction_429)
with R6.RegistreGlobal(ledger_429_payant) as reg:
    verifie("429 payante avec generation_id garde réservation et marqueur ambigus",
            r429["reconciliation_requise"]
            and any(e["etat"] == "reservation" for e in reg.operations.values()))
appels_avant_reprise = SCENARIO.appels
refuse("reprise ambiguë ne peut pas doubler le paiement", lambda: R6.lancer(
    client_tx, "fixture/payant-429", "q4", TABLE,
    [("gauche", "journaliste", "item_d")], R6.Budget(4.4, 1e-6, 2e-6),
    "transaction-429", n_predict=40, transaction=transaction_429))
verifie("aucun second POST après échec payant ambigu", SCENARIO.appels == appels_avant_reprise)
os.remove(R6.FICHIER_GO)

incomplet = os.path.join(TMP, "import-incomplet.jsonl")
with open(incomplet, "w") as fh:
    fh.write(json.dumps({"sequence": 0, "type": "initialisation",
                         "campagne": "R6-v2", "inventaire": inventaire}) + "\n")
with R6.RegistreGlobal(incomplet) as reg:
    refuse("import interrompu ne libere aucun budget", lambda: reg.reserver(id2, 1, 6))
    refuse("preflight refuse import interrompu", lambda: R6.preflight_cle(
        snapshot, 6, reg, inventaire, 150, {"prompt": 1, "completion": 2}))
with open(ancien, "a") as fh:
    fh.write("alteration")
with R6.RegistreGlobal(ledger) as reg:
    refuse("integrite historique verifiee", lambda: reg.verifier_integrite(inventaire))
with open(ledger, "a") as fh:
    fh.write('{"sequence":')
refuse("registre tronque bloque reprise", lambda: R6.RegistreGlobal(ledger).__enter__())

print("16. Plafond cumulatif par modele : atomicite, reprise et entrees adverses")
ledger_modele = os.path.join(TMP, "registre-plafond-modele.jsonl")
ancien_modele = os.path.join(TMP, "ancien-plafond-modele.jsonl")
with open(ancien_modele, "w") as fh:
    fh.write("historique plafond modele\n")
inventaire_modele = {
    ancien_modele: R6.hashlib.sha256(open(ancien_modele, "rb").read()).hexdigest()}
modele_cap = "fixture/modele-cap"
id_cap_f1 = R6.identite_campagne(modele_cap, "q4", "v", "cap-f1", "gauche",
                                 "journaliste", "campagne")
id_cap_f2 = R6.identite_campagne(modele_cap, "q4gab3", "v", "cap-f2", "gauche",
                                 "journaliste", "campagne")
id_cap_floor = R6.identite_campagne(modele_cap, "q4", "v", "cap-floor", "gauche",
                                    "journaliste", "plancher")
with R6.RegistreGlobal(ledger_modele) as reg:
    reg.initialiser_evenements(inventaire_modele, [])
    branche_nan = None
    try:
        R6.preflight_cle(snapshot, 6, reg, inventaire_modele, 150,
                         {"prompt": "1", "completion": "2"}, "0.01", 1000,
                         "campagne", modele_cap, float("nan"))
    except R6.ErreurPreflight as exc:
        branche_nan = exc.branche
    verifie("NaN refuse par le preflight du plafond modele",
            branche_nan == "plafond_modele_invalide")
    refuse("NaN refuse aussi par la reservation atomique", lambda: reg.reserver(
        id_cap_f1, "0.01", 6, plafond_modele_usd=float("nan"),
        empreinte_requete="e" * 64, fournisseur_impose="Fixture"))
    reg.reserver(id_cap_f1, "0.03", 6, plafond_modele_usd="0.05",
                 empreinte_requete="f" * 64, fournisseur_impose="Fixture")
    reg.reconcilier(id_cap_f1, "0.03", "facture-cap-f1")
    verifie("F1 compte dans le plafond partage", reg.total_modele(modele_cap) ==
            R6.Decimal("0.03"))
    code_enfant = (
        "import sys; sys.path.insert(0, sys.argv[1]); import r6_oracle_distant as r; "
        "\ntry:\n r.RegistreGlobal(sys.argv[2]).__enter__()\n"
        "except BlockingIOError:\n raise SystemExit(0)\n"
        "except BaseException:\n raise SystemExit(2)\n"
        "raise SystemExit(1)\n")
    enfant = subprocess.run([sys.executable, "-c", code_enfant,
                             os.path.join(RACINE, "analyses"), ledger_modele],
                            capture_output=True, text=True)
    verifie("un concurrent ne peut ni relire ni reserver sous le verrou",
            enfant.returncode == 0, enfant.stderr.strip())

with R6.RegistreGlobal(ledger_modele) as reg:
    verifie("reprise reconstruit le total et le plafond du modele",
            reg.total_modele(modele_cap) == R6.Decimal("0.03")
            and reg.plafond_modele_enregistre(modele_cap) == R6.Decimal("0.05"))
    refuse("F2 qui ferait depasser le plafond est refuse", lambda: reg.reserver(
        id_cap_f2, "0.0201", 6, plafond_modele_usd="0.05",
        empreinte_requete="1" * 64, fournisseur_impose="Fixture"))
    refuse("un plafond different ne peut pas etre injecte a la reprise", lambda: reg.reserver(
        id_cap_f2, "0.01", 6, plafond_modele_usd="0.06",
        empreinte_requete="2" * 64, fournisseur_impose="Fixture"))
    reg.reserver(id_cap_floor, "0.02", 6, plafond_modele_usd="0.05",
                 empreinte_requete="3" * 64, fournisseur_impose="Fixture")
    reg.reconcilier(id_cap_floor, "0.02", "facture-cap-floor")
    verifie("F1 et plancher partagent exactement le plafond",
            reg.total_modele(modele_cap) == R6.Decimal("0.05"))
    longueur_avant = len(reg.evenements)
    refuse("double reservation d'une identite reglee refusee", lambda: reg.reserver(
        id_cap_f1, "0.001", 6, plafond_modele_usd="0.05",
        empreinte_requete="4" * 64, fournisseur_impose="Fixture"))
    verifie("double reservation refusee sans ecriture ledger",
            len(reg.evenements) == longueur_avant)

transaction_cap = R6.TransactionPayante(
    ledger_modele, inventaire_modele, "campagne", "0.002", 1000,
    cle_fraiche, solde_frais, plafond_modele="0.05")
appels_avant_cap = SCENARIO.appels
branche_cap = None
open(R6.FICHIER_GO, "w").close()
with patch.object(R6, "verifier_referent", lambda: None):
    try:
        transaction_cap.appeler(
            client_tx, modele_cap, "q4", R6.FORMATS["q4"], "item_cap", "gauche",
            "journaliste", R6.invite("item_a", "gauche", "journaliste", "q4", TABLE)[0],
            40, os.path.join(TMP, "cap-refus.en-cours"))
    except R6.ErreurPreflight as exc:
        branche_cap = exc.branche
verifie("plafond modele plein donne une branche stable avant POST",
        branche_cap == "plafond_modele_insuffisant"
        and SCENARIO.appels == appels_avant_cap
        and not os.path.exists(os.path.join(TMP, "cap-refus.en-cours")))
os.remove(R6.FICHIER_GO)

# Le plafond d'un modèle couvre aussi les 20 appels pilote, anciens ou futurs.
ledger_scope = os.path.join(TMP, "registre-plafond-modele-pilote.jsonl")
modele_scope = "fixture/modele-pilote-dans-cap"
id_scope_pilot = R6.identite_campagne(
    modele_scope, "q4", "v", "pilot", "gauche", "journaliste", "essai-1")
id_scope_campaign = R6.identite_campagne(
    modele_scope, "q4", "v", "campaign", "gauche", "journaliste", "campagne")
with R6.RegistreGlobal(ledger_scope) as reg:
    reg.initialiser_evenements(inventaire_modele, [])
    reg.reserver(id_scope_pilot, "0.001", 6, plafond_modele_usd="0.005",
                 plafond_pilote_usd="0.02", appels_pilote_max=20,
                 borne_pilote_max_usd="0.001", empreinte_requete="5" * 64,
                 fournisseur_impose="Fixture")
    reg.reconcilier(id_scope_pilot, "0.001", "facture-pilote-futur")
    reg.reserver(id_scope_campaign, "0.004", 6, plafond_modele_usd="0.005",
                 empreinte_requete="6" * 64, fournisseur_impose="Fixture")
    reg.reconcilier(id_scope_campaign, "0.004", "facture-campagne")
    verifie("pilote futur et campagne partagent le plafond modele",
            reg.total_modele(modele_scope) == R6.Decimal("0.005"))
with R6.RegistreGlobal(ledger_scope) as reg:
    verifie("reprise ledger conserve le cumul pilote plus campagne",
            reg.total_modele(modele_scope) == R6.Decimal("0.005")
            and reg.plafond_modele_enregistre(modele_scope) == R6.Decimal("0.005"))
    refuse("depassement apres cout pilote refuse", lambda: reg.reserver(
        R6.identite_campagne(modele_scope, "q4", "v", "floor", "gauche",
                             "journaliste", "plancher"),
        "0.001", 6, plafond_modele_usd="0.005",
        empreinte_requete="7" * 64, fournisseur_impose="Fixture"))

ledger_historical_scope = os.path.join(TMP, "registre-plafond-historique-pilote.jsonl")
historique_pilote = {"type": "historique", "identite": id_scope_pilot, "usd": "0.001",
                    "empreinte_requete": "8" * 64,
                    "fournisseur_impose": "Fixture"}
with R6.RegistreGlobal(ledger_historical_scope) as reg:
    reg.initialiser_evenements(inventaire_modele, [historique_pilote])
with R6.RegistreGlobal(ledger_historical_scope) as reg:
    verifie("cout pilote historique entre dans le plafond sans reecriture",
            reg.total_modele(modele_scope) == R6.Decimal("0.001"))
    refuse("historique pilote peut faire depasser une future campagne", lambda: reg.reserver(
        id_scope_campaign, "0.0041", 6, plafond_modele_usd="0.005",
        empreinte_requete="9" * 64, fournisseur_impose="Fixture"))

serveur.shutdown()
serveur3.shutdown()
shutil.rmtree(TMP, ignore_errors=True)
print(("\nTOUT PASSE" if ok else "\nAU MOINS UN TEST RATE")
      + f", dossier temporaire efface : {TMP}")
sys.exit(0 if ok else 1)
