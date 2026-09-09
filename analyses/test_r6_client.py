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
     factures, le cout calcule au prix de l'inventaire et le cumul ;
  9. le plan de cellules de la v2 fait bien 894 et 316 cellules ;
 10. l'essai de N cellules ecrit son resume de cout reel, de rejets et de latence.

Usage : .venv/bin/python analyses/test_r6_client.py
"""

import json
import os
import shutil
import sys
import tempfile
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "analyses"))

import r1_oracle_camps as R1
import r5_gabarit_exemples as R5
import r6_oracle_distant as R6

TMP = tempfile.mkdtemp(prefix="r6test-")
R6.TRACES = TMP
R6.JOURNAL = os.path.join(TMP, "r6-run.log")
R6.FICHIER_ARRET = os.path.join(TMP, "STOP")
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
        self.appels = 0
        self.requetes = []
        self.au_ieme_appel = {}

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
        corps = {
            "id": "gen-test", "model": charge["model"], "provider": "FauxFournisseur",
            "choices": [{"message": {"role": "assistant", "content": SCENARIO.suivant()},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": SCENARIO.jetons[0],
                      "completion_tokens": SCENARIO.jetons[1],
                      "completion_tokens_details": {"reasoning_tokens": SCENARIO.raisonnement},
                      "cost": 0.000123},
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


def joue(cle, format_="q4", plafond=1.0, tarif=(1e-6, 2e-6), limite=None, items=ITEMS,
         camps=("gauche",), identites=("journaliste",), raisonnement="low", base=BASE):
    client = R6.ClientChat("fausse-cle", base=base, timeout=10, raisonnement=raisonnement)
    budget = R6.Budget(plafond, tarif[0], tarif[1], R6.JETONS_ESTIMES[format_])
    cellules = list(R1.cellules(list(items), list(camps), list(identites)))
    r = R6.lancer(client, "faux/modele", format_, TABLE, cellules, budget, cle,
                  n_predict=40, limite=limite, journal_tous=10_000)
    lignes = [json.loads(l) for l in open(R6.chemin_trace(cle), encoding="utf-8")]
    return r, lignes


def remise_a_zero(textes=None, jetons=(300, 20), raisonnement=0):
    SCENARIO.textes = list(textes or [BON])
    SCENARIO.jetons = jetons
    SCENARIO.raisonnement = raisonnement
    SCENARIO.appels = 0
    SCENARIO.requetes = []
    SCENARIO.au_ieme_appel = {}


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
cout = 300 * 1e-6 + 20 * 2e-6
verifie("cout calcule au prix de l'inventaire", abs(l["cout_appel_usd"] - cout) < 1e-12,
        str(l["cout_appel_usd"]))
verifie("cout annonce par le fournisseur trace aussi", l["cout_annonce_usd"] == 0.000123)
verifie("cumul present", abs(l["cout_cumule_usd"] - cout) < 1e-12)
verifie("raisonnement inscrit dans la trace", l["raisonnement"] == "low")

print("4. Le reglage de raisonnement part dans la requete")
remise_a_zero([BON])
joue("raison1", limite=1, raisonnement="low")
verifie("effort low envoye",
        SCENARIO.requetes[0]["charge"]["reasoning"] == {"effort": "low", "exclude": True},
        str(SCENARIO.requetes[0]["charge"].get("reasoning")))
remise_a_zero([BON])
joue("raison2", limite=1, raisonnement="off")
verifie("raisonnement desactive",
        SCENARIO.requetes[0]["charge"]["reasoning"] == {"enabled": False, "exclude": True})
remise_a_zero([BON])
joue("raison3", limite=1, raisonnement="aucun")
verifie("aucun champ envoye quand le serveur n'en veut pas",
        "reasoning" not in SCENARIO.requetes[0]["charge"])
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
r, lignes = joue("plafond1", plafond=0.0025)
verifie("le plafond arrete le run", r["plafond_atteint"] is True)
verifie("2 cellules jouees sur 4", r["cellules"] == 2, str(r["cellules"]))
verifie("le cumul ne depasse jamais le plafond", r["cout_usd"] <= 0.0025 + 1e-12,
        str(r["cout_usd"]))
verifie("PLAFOND ATTEINT ecrit dans le journal",
        "PLAFOND ATTEINT" in open(R6.JOURNAL, encoding="utf-8").read())

print("6. Fichier d'arret data/traces/STOP")
remise_a_zero([BON])
SCENARIO.au_ieme_appel = {2: lambda: open(R6.FICHIER_ARRET, "w").close()}
r, lignes = joue("stop1")
verifie("arret demande signale", r["arret_demande"] is True)
verifie("2 cellules ecrites puis arret propre", r["cellules"] == 2, str(r["cellules"]))
verifie("trace relisible en entier", len(lignes) == 2)
verifie("ARRET DEMANDE ecrit dans le journal",
        "ARRET DEMANDE" in open(R6.JOURNAL, encoding="utf-8").read())
verifie("le script n'efface pas le fichier d'arret", os.path.exists(R6.FICHIER_ARRET))

print("7. Reprise sur trace existante")
os.remove(R6.FICHIER_ARRET)
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

print("9. Une erreur HTTP est un rejet compte, jamais rejoue")


class FauxErreur(Faux):
    def do_POST(self):
        corps = b'{"error":{"message":"rate limited"}}'
        self.send_response(429)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(corps)))
        self.end_headers()
        self.wfile.write(corps)


serveur2 = HTTPServer(("127.0.0.1", 0), FauxErreur)
threading.Thread(target=serveur2.serve_forever, daemon=True).start()
r, lignes = joue("err1", items=ITEMS[:2],
                 base=f"http://127.0.0.1:{serveur2.server_address[1]}/api/v1")
verifie("2 cellules rejetees", r["rejets"] == 2, str(r["rejets"]))
verifie("l'erreur est ecrite dans la trace", "429" in (lignes[0]["erreur"] or ""),
        str(lignes[0]["erreur"]))
verifie("un appel en erreur ne coute rien au budget", r["cout_usd"] == 0.0)

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
verifie("cout par cellule reel", abs(e["cout_par_cellule_usd"] - (300e-6 + 40e-6)) < 1e-12,
        str(e["cout_par_cellule_usd"]))
verifie("projection sur les 894 cellules du plan",
        abs(e["projection_plan_usd"] - round(e["cout_par_cellule_usd"] * 894, 6)) < 1e-9,
        str(e["projection_plan_usd"]))
verifie("taux de rejet dans le resume", e["taux_rejet"] == 0.0)
verifie("latence mesuree", e["latence_ms_mediane"] is not None)
verifie("jetons de raisonnement moyens mesures", e["jetons_raisonnement_moyens"] == 3.0)

serveur.shutdown()
serveur2.shutdown()
shutil.rmtree(TMP, ignore_errors=True)
print(("\nTOUT PASSE" if ok else "\nAU MOINS UN TEST RATE")
      + f", dossier temporaire efface : {TMP}")
sys.exit(0 if ok else 1)
