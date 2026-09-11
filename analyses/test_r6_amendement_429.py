"""Amendement 429 de R6 : rapprochement en lecture seule d'un 429 ambigu, hors réseau.

Serveur HTTP loopback fixture, registre et traces temporaires, `dormir` factice. Aucun
appel externe, aucune écriture sous data/. Couvre les scénarios (a) à (f) de la
spécification et les défauts D1 à D6, (i), (ii), (iii) de la revue adverse.

Usage : .venv/bin/python analyses/test_r6_amendement_429.py
"""

import glob
import hashlib
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import threading
from decimal import Decimal
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlsplit

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analyses"))
import r6_oracle_distant as R6
import r6_runner_campagnes as RUN


MODELE = "deepseek/deepseek-v4-flash"
CLE = "sk-fixture-secret-ne-pas-publier"
# Valeurs livrées dans le code, capturées avant toute injection par les tests.
CHEMIN_SCELLE_CODE = RUN.AMENDEMENT_429_CHEMIN
SHA_SCELLE_CODE = RUN.AMENDEMENT_429_SHA256
TEXTE_GENERATION = "A: 60\nB: 40"
ECHECS = []
N_VERIFS = [0]


def verifie(libelle, condition):
    N_VERIFS[0] += 1
    print(("  OK   " if condition else "  ECHEC ") + libelle, flush=True)
    if not condition:
        ECHECS.append(libelle)


def attend_erreur(libelle, fn, fragment, types=(ValueError, BlockingIOError)):
    try:
        fn()
    except types as exc:
        verifie(libelle, fragment in str(exc) or fragment == type(exc).__name__)
        return exc
    verifie(libelle + " (aucune erreur levée)", False)
    return None


class Etat:
    posts = []
    gets = []
    plan_posts = []
    statut_generation = 404
    statut_contenu = 404
    stop_a_post = None
    stop_texte = None


class Serveur(BaseHTTPRequestHandler):
    def log_message(self, *_args):
        pass

    def _json(self, code, corps, entetes=None):
        brut = json.dumps(corps).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(brut)))
        for k, v in (entetes or {}).items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(brut)

    def do_POST(self):
        taille = int(self.headers.get("Content-Length", "0"))
        charge = json.loads(self.rfile.read(taille))
        Etat.posts.append(charge)
        n = len(Etat.posts)
        if Etat.stop_a_post == n:
            with open(R6.FICHIER_ARRET_R6, "w", encoding="utf-8") as fh:
                fh.write(Etat.stop_texte)
        action = Etat.plan_posts[n - 1] if n - 1 < len(Etat.plan_posts) else "ok"
        if action == "429":
            self._json(429, {"error": {"code": 429, "message": "rate limited"}},
                       {"X-Generation-Id": f"gen-fixture-429-{n}"})
            return
        if action == "429-sans-id":
            self._json(429, {"error": {"code": 429, "message": "rate limited"}})
            return
        fournisseur = ("AutreProvider" if action == "ok-autre-fournisseur"
                       else charge["provider"]["order"][0])
        self._json(200, {
            "id": f"gen-fixture-ok-{n}", "model": charge["model"], "provider": fournisseur,
            "choices": [{"message": {"content": TEXTE_GENERATION}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 100, "completion_tokens": 10,
                      "completion_tokens_details": {"reasoning_tokens": 0}, "cost": 0.0001},
        })

    def do_GET(self):
        Etat.gets.append(self.path)
        chemin = urlsplit(self.path).path
        if chemin.endswith("/generation/content"):
            code = Etat.statut_contenu
        elif chemin.endswith("/generation"):
            code = Etat.statut_generation
        else:
            code = 500
        if code == 200:
            self._json(200, {"data": {"id": "gen", "total_cost": 0.0001,
                                      "output": {"completion": TEXTE_GENERATION}}})
        else:
            self._json(code, {"error": {"code": code, "message": "fixture"}})


def remise(plan_posts, statut_generation=404, statut_contenu=404):
    Etat.posts.clear()
    Etat.gets.clear()
    Etat.plan_posts = list(plan_posts)
    Etat.statut_generation = statut_generation
    Etat.statut_contenu = statut_contenu
    Etat.stop_a_post = None
    Etat.stop_texte = None


def sha(chemin):
    return hashlib.sha256(open(chemin, "rb").read()).hexdigest()


def ecrire_json(chemin, valeur):
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(valeur, fh, ensure_ascii=False, indent=2)


class Credits:
    """Snapshot /credits factice ; `changer_a` modifie total_usage à partir du n-ième appel."""
    def __init__(self, changer_a=None):
        self.appels = 0
        self.changer_a = changer_a

    def __call__(self, _cle):
        self.appels += 1
        if self.changer_a is not None and self.appels >= self.changer_a:
            return {"total_credits": 10, "total_usage": "0.0001"}
        return {"total_credits": 10, "total_usage": 0}


class CreditsParAppel:
    """Snapshot /credits factice v2 : valeur explicite par numéro d'appel (1-based).

    `valeurs` associe un numéro d'appel à un `total_usage` ; tout appel non listé reçoit
    `defaut`. Permet de placer précisément une variation de solde à un appel donné
    (ancrage, avant-appel, sonde 1 ou sonde 2) sans dépendre de l'ordre réel des appels.
    """
    def __init__(self, valeurs, defaut="0", total_credits=10):
        self.appels = 0
        self.valeurs = dict(valeurs)
        self.defaut = defaut
        self.total_credits = total_credits

    def __call__(self, _cle):
        self.appels += 1
        return {"total_credits": self.total_credits,
                "total_usage": self.valeurs.get(self.appels, self.defaut)}


class CreditsAlterne:
    """Snapshot /credits factice v2 : total_usage change à chaque appel, jamais stable."""
    def __init__(self):
        self.appels = 0

    def __call__(self, _cle):
        self.appels += 1
        return {"total_credits": 10,
                "total_usage": "0" if self.appels % 2 else "0.000001"}


class CreditsExceptionAppel:
    """Snapshot /credits factice v2 : lève une exception à un numéro d'appel donné."""
    def __init__(self, seuil_exception):
        self.appels = 0
        self.seuil_exception = seuil_exception

    def __call__(self, _cle):
        self.appels += 1
        if self.appels == self.seuil_exception:
            raise OSError("reseau indisponible (fixture)")
        return {"total_credits": 10, "total_usage": "0"}


def total_reglee_sans_verrou(chemin):
    """Rejoue le registre SANS prendre son verrou (lecture seule, hors flock).

    Nécessaire car `snapshot_solde` (donc la fabrique `CreditsAvecRetard`) est parfois
    appelé PENDANT que `TransactionPayante.appeler` détient déjà le verrou du même
    registre (`RegistreGlobal.__enter__` utilise `flock` non réentrant : un second
    `with RegistreGlobal(...)` dans le même processus lèverait `BlockingIOError`).
    Reproduit exactement la logique de `RegistreGlobal._appliquer`/`total_reglee`.
    """
    operations = {}
    for i, e in enumerate(R6.lignes_existantes(chemin)):
        if i == 0 or e.get("type") == "import-complet":
            continue
        ident = e["identite"]
        montant = R6.dollars(e["usd"])
        if e["type"] in ("reservation", "historique", "historique-incertain"):
            operations[ident] = dict(e, etat=e["type"], usd=montant)
        elif e["type"] == "reconciliation":
            operations[ident] = dict(e, etat="reglee", usd=montant)
        elif e["type"] == "annulation":
            operations.pop(ident, None)
    return sum((e["usd"] for e in operations.values()
                if e["etat"] in ("reglee", "historique", "historique-incertain")),
               Decimal("0"))


class CreditsAvecRetard:
    """Snapshot /credits factice : reflète `total_reglee()` du registre réel, mais avec un
    retard simulé (`retard` s d'horloge simulée) depuis le premier instant où ce total
    devient non nul — modélise le retard de règlement côté OpenRouter pour un appel
    ANTÉRIEUR déjà réglé à notre registre (retard observé en production : 15 à 40 s),
    indépendant du numéro ou de l'ordre de nos propres appels /credits. Couvre les
    scénarios L1/L2 de la revue adverse du 2026-09-11 et le correctif
    `DELAI_AVANT_SONDE_429`. Lit le registre SANS verrou (voir
    `total_reglee_sans_verrou`) : `snapshot_solde` est parfois appelé alors que
    `appeler` détient déjà le verrou du même registre.
    """
    def __init__(self, ledger, horloge, retard, total_credits=10):
        self.ledger, self.horloge, self.retard = ledger, horloge, retard
        self.total_credits = total_credits
        self.appels = 0
        self.instant_reglement = None

    def __call__(self, _cle):
        self.appels += 1
        reel = total_reglee_sans_verrou(self.ledger)
        if reel != Decimal(0) and self.instant_reglement is None:
            self.instant_reglement = self.horloge[0]
        if (self.instant_reglement is not None
                and self.horloge[0] - self.instant_reglement >= self.retard):
            visible = reel
        else:
            visible = Decimal(0)
        return {"total_credits": self.total_credits, "total_usage": str(visible)}


def dormir_horloge(horloge, tranches):
    """`dormir` factice qui avance une horloge simulée partagée avec `CreditsAvecRetard`."""
    def _dormir(secondes):
        tranches.append(secondes)
        horloge[0] += secondes
    return _dormir


def cle_fixture(_cle):
    return {"data": {"limit": 4.4, "limit_remaining": 4.4, "limit_reset": None}}


def environnement(dossier):
    R6.TRACES = os.path.join(dossier, "traces")
    R6.SORTIE = os.path.join(dossier, "resultats")
    R6.FICHIER_ARRET_R6 = os.path.join(R6.TRACES, "STOP-R6")
    R6.FICHIER_ARRET_GLOBAL = os.path.join(R6.TRACES, "STOP")
    R6.JOURNAL = os.path.join(R6.TRACES, "run.log")
    os.makedirs(os.path.join(R6.TRACES, "reprise"))
    old = os.path.join(dossier, "old.jsonl")
    open(old, "w").close()
    imported = os.path.join(dossier, "import.json")
    ecrire_json(imported, {
        "version": "R6-v2-import-1", "exhaustif": True,
        "attendus": {"lignes": 0, "reponses": 0, "incidents": 0,
                     "cout_annonce_reponses_usd": "0", "borne_incidents_total_usd": "0"},
        "cout_incidents": {"observation": "inconnu", "borne_unitaire_usd": "0",
                           "fondement_borne": "fixture"},
        "traces": [{"chemin": old, "passe": "ancien-pilote", "classe": "ancien-pilote",
                    "sha256": sha(old), "attendus": {"lignes": 0, "reponses": 0, "incidents": 0}}],
    })
    inventory, _ = R6.charger_import(imported)
    ledger = os.path.join(dossier, "ledger.jsonl")
    with R6.RegistreGlobal(ledger) as reg:
        reg.initialiser_evenements(inventory, [])
    return imported, inventory, ledger


def preparer(nom, rapprochement=True, credits=None):
    dossier = os.path.join(TMP, nom)
    imported, inventory, ledger = environnement(dossier)
    go = os.path.join(dossier, "GO-R6")
    open(go, "w").close()
    credits = credits or Credits()
    transaction = R6.TransactionPayante(ledger, inventory, "campagne", "0.001", 600,
                                         cle_fixture, credits, plafond_modele="0.06",
                                         fichier_go=go, rapprochement_429=rapprochement)
    captures = []
    appeler = transaction.appeler

    def espion(*a, **k):
        r = appeler(*a, **k)
        captures.append(json.loads(json.dumps(r)))
        return r

    transaction.appeler = espion
    return {"imported": imported, "ledger": ledger, "transaction": transaction,
            "captures": captures, "credits": credits}


def jouer(ctx, cellules, cle, dormir=None):
    dormeur = []
    resultat = R6.lancer(CLIENT, MODELE, "q4", TABLE, cellules,
                         R6.Budget("0.01", 0.11 / 1_000_000, 0.22 / 1_000_000), cle,
                         n_predict=150, transaction=ctx["transaction"],
                         manifeste_import=ctx["imported"], dormir=dormir or dormeur.append)
    return resultat, dormeur


def ident(item, camp="gauche", identite="journaliste"):
    return R6.identite_campagne(MODELE, "q4", R6.FORMATS["q4"], item, camp, identite,
                                "campagne")


def evenements(ledger):
    with R6.RegistreGlobal(ledger) as reg:
        return list(reg.evenements), dict(reg.operations)


def preuves_ecrites():
    return glob.glob(os.path.join(R6.TRACES, "reprise", "r6-rapprochement-429-*.json"))


def non_jouees(cle):
    chemin = os.path.join(R6.TRACES, f"r6-{cle}-non-jouees.jsonl")
    return [json.loads(l) for l in open(chemin)] if os.path.exists(chemin) else []


TMP = tempfile.mkdtemp(prefix="r6-amendement-429-")
SERVEUR = HTTPServer(("127.0.0.1", 0), Serveur)
threading.Thread(target=SERVEUR.serve_forever, daemon=True).start()
BASE = f"http://127.0.0.1:{SERVEUR.server_address[1]}/api/v1"
R6.verifier_referent = lambda: None
CLIENT = R6.ClientChat(CLE, base=BASE, raisonnement="off", fournisseur="DigitalOcean",
                       max_price={"prompt": "0.11", "completion": "0.22"})
TABLE = {"item_a": {"question": "Fixture A", "options": ["A", "B"]},
         "item_b": {"question": "Fixture B", "options": ["A", "B"]},
         "item_c": {"question": "Fixture C", "options": ["A", "B"]}}
CELLULE_A = ("gauche", "journaliste", "item_a")
CELLULE_B = ("droite", "adversaire", "item_b")
TRANCHES_AVANT_SONDE1 = [R6.TRANCHE_SONDE_429] * (R6.DELAI_AVANT_SONDE_429
                                                  // R6.TRANCHE_SONDE_429)
TRANCHES_ENTRE_SONDES = [R6.TRANCHE_SONDE_429] * (R6.DELAI_SONDE_429 // R6.TRANCHE_SONDE_429)
TRANCHES = TRANCHES_AVANT_SONDE1 + TRANCHES_ENTRE_SONDES
ANNULER_ORIGINAL = R6.RegistreGlobal.annuler
# Amendement 429 v2 : l'ancre (point A) est etablie AVANT le premier POST de chaque
# execution de `lancer`, et consomme donc, elle aussi, des tranches d'attente de
# `dormir` avant tout le reste. Mise a zero ici pour que les scenarios (a)-(f) et D1-D6,
# qui ne testent PAS l'ancrage lui-meme, gardent EXACTEMENT leurs anciennes assertions sur
# `dormeur`/`TRANCHES` (l'ancrage n'ajoute alors aucune tranche : deux lectures /credits
# immediates, sans attente). L'ancrage reel (delai, tentatives, instabilite, persistance)
# est teste separement plus bas, ou `R6.DELAI_ANCRE_429` est restaure temporairement.
R6.DELAI_ANCRE_429 = 0
DELAI_ANCRE_429_REEL = 60

try:
    verifie("DELAI_AVANT_SONDE_429 = 120 s puis DELAI_SONDE_429 = 540 s, relus par tranches "
            "de 10 s",
            R6.DELAI_AVANT_SONDE_429 == 120 and R6.DELAI_SONDE_429 == 540
            and R6.TRANCHE_SONDE_429 == 10 and sum(TRANCHES) == 660)

    print("(a) 429 ambigu, deux sondes 404/404, solde inchangé : annulation et rejeu unique")
    ctx = preparer("a")
    remise(["429", "ok", "ok"])
    cle = "fixture-a"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    observe = {}
    conclusions_a_l_annulation = []

    def annuler_espion(self, identite, preuve):
        # D4 : au moment de l'annulation, la preuve existe déjà et le marqueur n'est pas
        # encore archivé.
        observe["preuve_deja_ecrite"] = bool(preuves_ecrites())
        observe["marqueur_encore_actif"] = os.path.exists(en_cours)
        conclusions_a_l_annulation.extend(
            json.load(open(p, encoding="utf-8")).get("conclusion") for p in preuves_ecrites())
        return ANNULER_ORIGINAL(self, identite, preuve)

    R6.RegistreGlobal.annuler = annuler_espion
    try:
        res, dormeur = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    finally:
        R6.RegistreGlobal.annuler = ANNULER_ORIGINAL
    lignes = R6.lignes_existantes(R6.chemin_trace(cle))
    evts, ops = evenements(ctx["ledger"])
    annulations = [e for e in evts if e.get("type") == "annulation"]
    verifie("un seul POST supplémentaire (3 POST pour 2 cellules)", len(Etat.posts) == 3)
    verifie("quatre GET de sonde, tous en lecture sur /generation et /generation/content",
            len(Etat.gets) == 4 and all("/generation" in g and "id=gen-fixture-429-1" in g
                                        for g in Etat.gets))
    verifie("attente de 120 s puis 540 s en tranches de 10 s", dormeur == TRANCHES)
    verifie("r porte le contexte avant appel",
            ctx["captures"][0].get("rapprochement_429") == {
                "identite": ident("item_a"), "generation_id": "gen-fixture-429-1",
                "disponible_avant": "10", "total_usage_avant": "0"})
    verifie("rapproches_429 == 1, aucune non jouée, trace complète",
            res["rapproches_429"] == 1 and res["non_jouees"] == 0
            and res["cellules"] == 2 and not res["reconciliation_requise"])
    verifie("trace : deux lignes sans erreur, la cellule rejouée en fin de file",
            [x["item"] for x in lignes] == ["item_b", "item_a"]
            and all(x["erreur"] is None for x in lignes))
    verifie("aucun fichier non-jouées",
            not os.path.exists(os.path.join(R6.TRACES, f"r6-{cle}-non-jouees.jsonl")))
    verifie("une annulation au registre, preuve courte avec 429-non-facture et generation_id",
            len(annulations) == 1 and annulations[0]["identite"] == ident("item_a")
            and annulations[0]["preuve"].startswith("429-non-facture")
            and "gen-fixture-429-1" in annulations[0]["preuve"]
            and CLE not in annulations[0]["preuve"])
    verifie("la cellule rejouée est ensuite réglée, les deux opérations réglées",
            ops[ident("item_a")]["etat"] == "reglee"
            and ops[ident("item_b", "droite", "adversaire")]["etat"] == "reglee")
    archives = glob.glob(en_cours + ".annule-*")
    verifie("marqueur archivé (non supprimé), marqueur actif absent",
            len(archives) == 1 and not os.path.exists(en_cours)
            and json.load(open(archives[0]))["identite_globale"] == ident("item_a"))
    preuves = preuves_ecrites()
    verifie("un fichier de preuve en 0600", len(preuves) == 1
            and stat.S_IMODE(os.stat(preuves[0]).st_mode) == 0o600)
    texte_preuve = open(preuves[0], encoding="utf-8").read() if preuves else "{}"
    doc = json.loads(texte_preuve)
    verifie("preuve : sondes, critère, conclusion non_facture",
            doc.get("conclusion") == "non_facture" and len(doc.get("sondes", [])) == 2
            and doc["critere"]["rempli"] is True
            and all(s["generation"]["statut_http"] == 404
                    and s["generation_content"]["statut_http"] == 404
                    and s["credits"] == {"disponible": "10", "total_usage": "0"}
                    for s in doc["sondes"]))
    verifie("preuve sans clé ni contenu de génération",
            CLE not in texte_preuve and "A: 60" not in texte_preuve)
    verifie("preuve : horodatages du 429, de la sonde 1 et de la sonde 2",
            isinstance(doc.get("horodatage_429"), str) and bool(doc["horodatage_429"])
            and isinstance(doc["sondes"][0].get("horodatage"), str)
            and isinstance(doc["sondes"][1].get("horodatage"), str)
            and doc["horodatage_429"] <= doc["sondes"][0]["horodatage"]
            <= doc["sondes"][1]["horodatage"])
    verifie("horodatage commun à l'archive du marqueur et au fichier de preuve",
            bool(archives) and archives[0].rsplit(".annule-", 1)[1]
            in os.path.basename(preuves[0]))
    verifie("D4 : preuve écrite AVANT l'annulation, marqueur archivé APRÈS",
            observe == {"preuve_deja_ecrite": True, "marqueur_encore_actif": True})
    verifie("revue (b) : preuve non_facture_provisoire à l'annulation, non_facture ensuite",
            conclusions_a_l_annulation == ["non_facture_provisoire"]
            and doc.get("conclusion") == "non_facture")
    verifie("revue (b) : aucun fichier temporaire de réécriture laissé",
            not glob.glob(os.path.join(R6.TRACES, "reprise", "r6-rapprochement-429-*.tmp")))
    verifie("la preuve du registre nomme le fichier de preuve",
            bool(preuves) and f"preuve={os.path.basename(preuves[0])}" in annulations[0]["preuve"])
    verifie("(ii) la ligne rejouée porte rapprochement_429, les autres non",
            lignes[1].get("rapprochement_429") == {
                "statut": "non_facture", "fichier_preuve": os.path.basename(preuves[0])}
            and "rapprochement_429" not in lignes[0])
    verifie("rapprochement journalisé",
            "RAPPROCHE NON FACTURE" in open(R6.JOURNAL, encoding="utf-8").read())

    for nom, libelle, credits, statut_gen in (
            ("b", "(b) solde modifié à la seconde sonde", Credits(changer_a=3), 404),
            ("c", "(c) /generation répond 200", Credits(), 200)):
        print(libelle + " : réservation et marqueur conservés, arrêt")
        ctx = preparer(nom, credits=credits)
        remise(["429", "ok"], statut_generation=statut_gen)
        cle = "fixture-" + nom
        res, dormeur = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
        en_cours = R6.chemin_trace(cle) + ".en-cours"
        evts, ops = evenements(ctx["ledger"])
        verifie(nom + " : un seul POST, arrêt avant la cellule suivante", len(Etat.posts) == 1)
        verifie(nom + " : deux sondes effectuées (4 GET, attente complète)",
                len(Etat.gets) == 4 and dormeur == TRANCHES)
        verifie(nom + " : aucune annulation, réservation ouverte",
                not any(e.get("type") == "annulation" for e in evts)
                and ops[ident("item_a")]["etat"] == "reservation")
        verifie(nom + " : marqueur conservé, aucune archive",
                os.path.exists(en_cours) and not glob.glob(en_cours + ".annule-*"))
        verifie(nom + " : reconciliation_requise, une non jouée, rapproches_429 == 0",
                res["reconciliation_requise"] and res["non_jouees"] == 1
                and res["rapproches_429"] == 0 and res["cellules"] == 0)
        # v2, point C : la preuve est TOUJOURS écrite dès que les deux sondes sont prises,
        # même en échec ; ici conclusion `indetermine`, jamais `non_facture`.
        preuves = preuves_ecrites()
        doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
        verifie(nom + " : une preuve écrite, conclusion indéterminée, critère non rempli",
                len(preuves) == 1 and doc.get("conclusion") == "indetermine"
                and doc.get("motif") == "critere non rempli"
                and doc["critere"]["rempli"] is False and "ancre" in doc
                and len(doc.get("sondes", [])) == 2)
        if nom == "b":
            verifie("b : snapshot /credits lu cinq fois (ancrage x2, avant, sonde 1, sonde 2)",
                    ctx["credits"].appels == 5)
            verifie("b : total_usage stable entre les sondes, écart hors tolérance",
                    doc["critere"]["total_usage_stable"] is True
                    and Decimal(doc["critere"]["ecart_usd"]) > Decimal(doc["critere"]["tolerance_usd"]))
        else:
            verifie("c : /generation à 200 rend les sondes non conformes (404 attendu)",
                    doc["critere"]["sondes_404"] == [False, False]
                    and doc["critere"]["total_usage_stable"] is False)

    print("(d) rapprochement_429=False : comportement actuel exact")
    ctx = preparer("d", rapprochement=False)
    remise(["429", "ok"])
    cle = "fixture-d"
    res, dormeur = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    evts, ops = evenements(ctx["ledger"])
    verifie("d : zéro GET de sonde, dormir jamais appelé", Etat.gets == [] and dormeur == [])
    verifie("d : r sans champ rapprochement_429, cout_incertain et non rejouable",
            "rapprochement_429" not in ctx["captures"][0]
            and ctx["captures"][0]["cout_incertain"] is True
            and ctx["captures"][0]["rejouable"] is False)
    verifie("d : arrêt, réservation ouverte, marqueur conservé",
            len(Etat.posts) == 1 and ops[ident("item_a")]["etat"] == "reservation"
            and os.path.exists(en_cours) and res["reconciliation_requise"]
            and res["non_jouees"] == 1 and res["rapproches_429"] == 0)
    verifie("d : /credits lu une seule fois", ctx["credits"].appels == 1)
    verifie("d : ligne non jouée au format historique (aucun champ ajouté)",
            set(non_jouees(cle)[0]) == {
                "version_prompt", "format", "modele", "cle_modele", "item", "camp",
                "identite", "non_jouee", "tentatives", "statut", "rejouable", "erreur",
                "incidents", "horodatage"})
    inactif = ctx["transaction"].rapprocher_429(CLIENT, ctx["captures"][0], dormeur.append)
    verifie("d : rapprocher_429 inactif ne fait rien",
            inactif["statut"] == "indetermine" and Etat.gets == [] and dormeur == []
            and not any(e.get("type") == "annulation" for e in evenements(ctx["ledger"])[0]))

    print("(e) le rejeu reçoit à nouveau un 429 ambigu : arrêt sans second rapprochement")
    ctx = preparer("e")
    remise(["429", "429", "ok"])
    cle = "fixture-e"
    res, dormeur = jouer(ctx, [CELLULE_A], cle)
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    evts, ops = evenements(ctx["ledger"])
    verifie("e : deux POST, un seul rapprochement (4 GET, une attente)",
            len(Etat.posts) == 2 and len(Etat.gets) == 4 and dormeur == TRANCHES)
    verifie("e : une annulation, seconde réservation ouverte",
            sum(e.get("type") == "annulation" for e in evts) == 1
            and ops[ident("item_a")]["etat"] == "reservation")
    verifie("e : premier marqueur archivé, second conservé",
            len(glob.glob(en_cours + ".annule-*")) == 1 and os.path.exists(en_cours))
    verifie("e : arrêt, une non jouée, rapproches_429 == 1",
            res["reconciliation_requise"] and res["non_jouees"] == 1
            and res["rapproches_429"] == 1 and res["cellules"] == 0)

    print("(v2-1) coût d'un appel ANTÉRIEUR réglé pendant la fenêtre : critère rempli")
    # Cause 1 du 2026-09-11 : le solde met plusieurs appels à se régler. Deux cellules
    # précédentes se règlent (0,0001 USD chacune) mais /credits ne le reflète qu'à partir
    # de la sonde 1 (appel #6). L'ancienne règle (égalité stricte à l'avant-appel PAR
    # CELLULE) aurait échoué ; le critère v2 (ancre + variation des coûts RÉGLÉS au
    # registre) doit réussir car il suit le registre, pas une lecture ponctuelle.
    ctx = preparer("v2-1", credits=CreditsParAppel({6: "0.0002", 7: "0.0002"}))
    cle = "fixture-v2-1"
    item_c = ("centre", "journaliste", "item_c")
    remise(["ok", "ok", "429", "ok"])
    res, dormeur = jouer(ctx, [CELLULE_B, item_c, CELLULE_A], cle)
    verifie("(v2-1) les trois cellules aboutissent, la rapprochée rejouée, aucun arrêt",
            res["rapproches_429"] == 1 and res["cellules"] == 3
            and not res["reconciliation_requise"] and ctx["credits"].appels == 8)
    preuves = preuves_ecrites()
    doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
    verifie("(v2-1) preuve : ancre à 0, deux coûts réglés depuis l'ancre, critère rempli",
            doc.get("conclusion") == "non_facture" and doc["critere"]["rempli"] is True
            and doc["ancre"]["total_usage_ancre"] == "0"
            and doc["ancre"]["somme_reglee_registre_ancre"] == "0"
            and doc["critere"]["somme_reglee_registre_maintenant"] == "0.0002"
            and doc["critere"]["total_usage_attendu_usd"] == "0.0002"
            and doc["critere"]["ecart_usd"] == "0.0000")

    print("(v2-2) dépense hors registre de 2e-6 : indéterminé malgré l'ancre")
    ctx = preparer("v2-2", credits=CreditsParAppel({4: "0.000002", 5: "0.000002"}))
    cle = "fixture-v2-2"
    remise(["429", "ok"])
    res, dormeur = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    preuves = preuves_ecrites()
    doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
    verifie("(v2-2) sondes stables (404/404, usage identique) mais écart hors tolérance",
            len(preuves) == 1 and doc.get("conclusion") == "indetermine"
            and doc["critere"]["total_usage_stable"] is True
            and doc["critere"]["rempli"] is False
            and Decimal(doc["critere"]["ecart_usd"]) == Decimal("0.000002")
            and Decimal(doc["critere"]["ecart_usd"]) > Decimal(doc["critere"]["tolerance_usd"]))
    verifie("(v2-2) arrêt, réservation ouverte, aucune annulation",
            res["reconciliation_requise"] and res["rapproches_429"] == 0
            and evenements(ctx["ledger"])[1][ident("item_a")]["etat"] == "reservation")

    print("(v2-3) le coût plausible de la génération ambiguë (1,6e-5) apparaît : indéterminé")
    ctx = preparer("v2-3", credits=CreditsParAppel({4: "0.000016", 5: "0.000016"}))
    cle = "fixture-v2-3"
    remise(["429", "ok"])
    res, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    preuves = preuves_ecrites()
    doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
    verifie("(v2-3) écart de la taille d'une génération facturée : indéterminé, jamais annulé",
            len(preuves) == 1 and doc.get("conclusion") == "indetermine"
            and doc["critere"]["total_usage_stable"] is True
            and Decimal(doc["critere"]["ecart_usd"]) == Decimal("0.000016")
            and res["reconciliation_requise"] and res["rapproches_429"] == 0)

    print("(v2-4) règlement d'un appel ANTÉRIEUR retardé de 30 s après le 429 : non facturé")
    # Défaut bloquant de la revue adverse du 2026-09-11 (scénarios L1/L2) : le solde met
    # 15 à 40 s à refléter un appel déjà réglé à NOTRE registre. Sans le correctif
    # DELAI_AVANT_SONDE_429, ce règlement tombe entre la sonde 1 (immédiate) et la
    # sonde 2, rend `total_usage_stable` faux, et un 429 réellement non facturé finit en
    # `indetermine` (voir le scénario L1 plus bas). Avec les 120 s d'attente AVANT la
    # sonde 1, ce même règlement tombe avant la sonde 1 : les deux sondes le voient de
    # façon stable, et le critère (ancre + variation du registre) le reconnaît comme
    # portant sur la cellule B, pas sur la cellule ambiguë A.
    horloge_v24 = [0.0]
    tranches_v24 = []
    dossier_v24 = os.path.join(TMP, "v2-4")
    ledger_v24 = os.path.join(dossier_v24, "ledger.jsonl")
    ctx = preparer("v2-4", credits=CreditsAvecRetard(ledger_v24, horloge_v24, 30))
    cle = "fixture-v2-4"
    remise(["ok", "429", "ok"])
    res, _ = jouer(ctx, [CELLULE_B, CELLULE_A], cle,
                   dormir=dormir_horloge(horloge_v24, tranches_v24))
    preuves = preuves_ecrites()
    doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
    verifie("(v2-4) sondes stables (règlement antérieur déjà visible avant la sonde 1)",
            len(preuves) == 1 and doc.get("conclusion") == "non_facture"
            and doc["critere"]["total_usage_stable"] is True
            and doc["critere"]["rempli"] is True and tranches_v24 == TRANCHES)
    verifie("(v2-4) rejeu unique de la cellule ambiguë, aucune reconciliation forcée",
            res["rapproches_429"] == 1 and res["cellules"] == 2
            and not res["reconciliation_requise"])

    print("(v2-4 bis) même règlement antérieur retardé de plus de 120 s : tombe entre les "
          "sondes, indéterminé (sens sûr)")
    horloge_v24b = [0.0]
    dossier_v24b = os.path.join(TMP, "v2-4-bis")
    ledger_v24b = os.path.join(dossier_v24b, "ledger.jsonl")
    ctx = preparer("v2-4-bis", credits=CreditsAvecRetard(ledger_v24b, horloge_v24b, 150))
    cle = "fixture-v2-4-bis"
    remise(["ok", "429"])
    res, _ = jouer(ctx, [CELLULE_B, CELLULE_A], cle, dormir=dormir_horloge(horloge_v24b, []))
    preuves = preuves_ecrites()
    doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
    verifie("(v2-4 bis) le règlement (150 s > 120 s) n'apparaît qu'à la sonde 2 : instable",
            len(preuves) == 1 and doc.get("conclusion") == "indetermine"
            and doc["critere"]["total_usage_stable"] is False
            and doc["critere"]["total_usage_sondes"][0] == "0"
            and Decimal(doc["critere"]["total_usage_sondes"][1]) > 0
            and res["reconciliation_requise"] and res["rapproches_429"] == 0)

    print("(L1) sans le correctif (sonde 1 immédiate) : le même 429 non facturé finit à "
          "tort en indéterminé — démonstration du défaut corrigé ci-dessus")
    horloge_l1 = [0.0]
    tranches_l1 = []
    dossier_l1 = os.path.join(TMP, "l1-sans-correctif")
    ledger_l1 = os.path.join(dossier_l1, "ledger.jsonl")
    ctx = preparer("l1-sans-correctif", credits=CreditsAvecRetard(ledger_l1, horloge_l1, 30))
    cle = "fixture-l1"
    remise(["ok", "429"])
    ancien_delai_avant = R6.DELAI_AVANT_SONDE_429
    R6.DELAI_AVANT_SONDE_429 = 0
    try:
        res, _ = jouer(ctx, [CELLULE_B, CELLULE_A], cle,
                       dormir=dormir_horloge(horloge_l1, tranches_l1))
    finally:
        R6.DELAI_AVANT_SONDE_429 = ancien_delai_avant
    preuves = preuves_ecrites()
    doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
    verifie("(L1) sonde 1 immédiate (t=0) : règlement à 30 s invisible, sonde 2 (t=540) le "
            "voit -> instable, indéterminé (le défaut motivant le correctif)",
            len(preuves) == 1 and doc.get("conclusion") == "indetermine"
            and doc["critere"]["total_usage_stable"] is False
            and tranches_l1 == TRANCHES_ENTRE_SONDES
            and res["reconciliation_requise"] and res["rapproches_429"] == 0)

    print("(v2-5) ancrage instable six fois : ancienne règle, aucune sonde")
    ctx = preparer("v2-5", credits=CreditsAlterne())
    R6.DELAI_ANCRE_429 = DELAI_ANCRE_429_REEL
    try:
        dormeur5 = []
        ancre = ctx["transaction"].etablir_ancre_429(CLIENT, dormeur5.append)
        tranches_par_tentative = DELAI_ANCRE_429_REEL // R6.TRANCHE_SONDE_429
        verifie("(v2-5) ancre absente après six tentatives instables",
                ancre is None and ctx["credits"].appels == 2 * R6.TENTATIVES_ANCRE_429)
        verifie("(v2-5) six tentatives complètes, chacune attendue en tranches de 10 s",
                dormeur5 == [R6.TRANCHE_SONDE_429] * (tranches_par_tentative
                                                       * R6.TENTATIVES_ANCRE_429))
        verifie("(v2-5) aucun fichier d'ancre persisté (ancrage jamais établi)",
                not glob.glob(os.path.join(R6.TRACES, "reprise", "r6-ancre-429-*.json")))

        ctx2 = preparer("v2-5-integration", credits=CreditsAlterne())
        cle2 = "fixture-v2-5-integration"
        remise(["429", "ok"])
        res, _ = jouer(ctx2, [CELLULE_A, CELLULE_B], cle2)
    finally:
        R6.DELAI_ANCRE_429 = 0
    verifie("(v2-5) intégration : ancienne règle -> zéro sonde, arrêt, aucune preuve",
            Etat.gets == [] and not preuves_ecrites()
            and res["reconciliation_requise"] and res["rapproches_429"] == 0
            and res["non_jouees"] == 1)
    verifie("(v2-5) intégration : ancrage instable journalisé",
            "amendement 429 inactif pour ce run" in open(R6.JOURNAL, encoding="utf-8").read())

    print("(v2-6) exception réseau pendant la lecture /credits d'une sonde : indéterminé")
    ctx = preparer("v2-6", credits=CreditsExceptionAppel(4))
    cle = "fixture-v2-6"
    remise(["429", "ok"])
    res, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    preuves = preuves_ecrites()
    doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
    verifie("(v2-6) preuve écrite avec le type d'exception de la sonde en échec",
            len(preuves) == 1 and doc.get("conclusion") == "indetermine"
            and doc["sondes"][0]["credits"].get("exception") == "OSError"
            and doc["critere"]["total_usage_stable"] is False)
    verifie("(v2-6) arrêt propre, réservation ouverte, aucune annulation automatique",
            res["reconciliation_requise"] and res["rapproches_429"] == 0
            and evenements(ctx["ledger"])[1][ident("item_a")]["etat"] == "reservation")

    verifie("(v2-7) une preuve a bien été écrite pour chacun des échecs v2 ci-dessus (b, c, "
            "v2-2, v2-3, v2-4 bis, L1, v2-6)",
            True)  # vérifié individuellement à chaque scénario

    print("D2 STOP entre rapprochement et rejeu, reprise, nouveau 429 : aucune 2e annulation")
    ctx = preparer("d2")
    remise(["429", "ok", "429", "ok"])
    Etat.stop_a_post = 2
    Etat.stop_texte = "stop\n"
    cle = "fixture-d2"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    r1, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    verifie("D2 : premier run rapproche A puis s'arrête sur STOP avant le rejeu",
            r1["rapproches_429"] == 1 and r1["arret_demande"] and r1["cellules"] == 1)
    os.remove(R6.FICHIER_ARRET_R6)
    Etat.stop_a_post = None
    gets_avant = len(Etat.gets)
    r2, dormeur2 = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    evts, ops = evenements(ctx["ledger"])
    verifie("D2 : reprise, 429 sur A refusé au rapprochement (zéro GET, aucune attente)",
            len(Etat.gets) == gets_avant and dormeur2 == [] and len(Etat.posts) == 3)
    verifie("D2 : une seule annulation automatique sur A, réservation ouverte, marqueur gardé",
            sum(e.get("type") == "annulation" and e["identite"] == ident("item_a")
                for e in evts) == 1
            and ops[ident("item_a")]["etat"] == "reservation" and os.path.exists(en_cours))
    verifie("D2 : arrêt, non jouée écrite, rapproches_429 == 0",
            r2["reconciliation_requise"] and r2["non_jouees"] == 1 and r2["rapproches_429"] == 0)
    verifie("D2 : motif du refus journalisé",
            "deja presente au registre" in open(R6.JOURNAL, encoding="utf-8").read())

    print("D2 bis STOP entre rapprochement et rejeu, reprise réussie : ligne annotée")
    ctx = preparer("d2-reprise-ok")
    remise(["429", "ok", "ok"])
    Etat.stop_a_post = 2
    Etat.stop_texte = "stop\n"
    cle = "fixture-d2-ok"
    jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    os.remove(R6.FICHIER_ARRET_R6)
    Etat.stop_a_post = None
    r2, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    lignes = R6.lignes_existantes(R6.chemin_trace(cle))
    preuves = preuves_ecrites()
    verifie("D2 bis : A rejouée à la reprise, trace B puis A, A porte rapprochement_429",
            r2["cellules"] == 1 and [x["item"] for x in lignes] == ["item_b", "item_a"]
            and len(preuves) == 1
            and lignes[1].get("rapprochement_429", {}).get("fichier_preuve")
            == os.path.basename(preuves[0]))

    print("D2 ter archive .en-cours.annule-* existante pour l'identité : refus")
    ctx = preparer("d2-archive")
    remise(["429"])
    cle = "fixture-d2-archive"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    ecrire_json(en_cours + ".annule-20260911T000000000000",
                {"identite_globale": ident("item_a"), "empreinte_requete": "a" * 64})
    res, dormeur = jouer(ctx, [CELLULE_A], cle)
    verifie("D2 ter : zéro GET, arrêt, réservation ouverte",
            Etat.gets == [] and dormeur == [] and res["reconciliation_requise"]
            and evenements(ctx["ledger"])[1][ident("item_a")]["etat"] == "reservation")
    ctx = preparer("d2-archive-autre")
    remise(["429", "ok"])
    cle = "fixture-d2-archive-autre"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    ecrire_json(en_cours + ".annule-20260911T000000000000",
                {"identite_globale": ident("item_z"), "empreinte_requete": "a" * 64})
    res, _ = jouer(ctx, [CELLULE_A], cle)
    verifie("D2 ter : archive d'une autre identité sans effet (rapprochement effectué)",
            res["rapproches_429"] == 1 and len(Etat.gets) == 4)

    print("D4 preuve impossible à écrire : ni annulation ni archive, arrêt sans exception")
    ctx = preparer("d4")
    remise(["429", "ok"])
    cle = "fixture-d4"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    open_original = os.open

    def open_casse(chemin, drapeaux, *a, **k):
        if "r6-rapprochement-429-" in str(chemin):
            raise PermissionError("disque")
        return open_original(chemin, drapeaux, *a, **k)

    os.open = open_casse
    try:
        res, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    finally:
        os.open = open_original
    evts, ops = evenements(ctx["ledger"])
    verifie("D4 : aucune annulation, réservation ouverte, marqueur actif, aucune archive",
            not any(e.get("type") == "annulation" for e in evts)
            and ops[ident("item_a")]["etat"] == "reservation"
            and os.path.exists(en_cours) and not glob.glob(en_cours + ".annule-*"))
    verifie("D4 : arrêt propre (reconciliation_requise, une non jouée, un POST)",
            res["reconciliation_requise"] and res["non_jouees"] == 1 and len(Etat.posts) == 1)

    print("D4 bis annulation impossible après preuve : marqueur et réservation gardés")
    ctx = preparer("d4-annulation")
    remise(["429", "ok"])
    cle = "fixture-d4-annulation"
    en_cours = R6.chemin_trace(cle) + ".en-cours"

    def annuler_casse(self, identite, preuve):
        raise ValueError("registre en panne")

    R6.RegistreGlobal.annuler = annuler_casse
    try:
        res, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    finally:
        R6.RegistreGlobal.annuler = ANNULER_ORIGINAL
    evts, ops = evenements(ctx["ledger"])
    verifie("D4 bis : preuve présente, aucune annulation, marqueur actif, aucune archive",
            len(preuves_ecrites()) == 1 and ops[ident("item_a")]["etat"] == "reservation"
            and os.path.exists(en_cours) and not glob.glob(en_cours + ".annule-*")
            and res["reconciliation_requise"] and res["rapproches_429"] == 0)
    verifie("revue (b) : annulation échouée, la preuve reste non_facture_provisoire",
            [json.load(open(p, encoding="utf-8")).get("conclusion") for p in preuves_ecrites()]
            == ["non_facture_provisoire"])

    print("revue (b) réécriture finale impossible après annulation : preuve provisoire, arrêt")
    ctx = preparer("d4-reecriture")
    remise(["429", "ok"])
    cle = "fixture-d4-reecriture"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    replace_original = os.replace

    def replace_casse(source, cible, *a, **k):
        if "r6-rapprochement-429-" in str(cible):
            raise PermissionError("disque")
        return replace_original(source, cible, *a, **k)

    os.replace = replace_casse
    try:
        res, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle)
    finally:
        os.replace = replace_original
    evts, ops = evenements(ctx["ledger"])
    verifie("revue (b) : annulation au registre, preuve restée non_facture_provisoire",
            sum(e.get("type") == "annulation" for e in evts) == 1
            and [json.load(open(p, encoding="utf-8")).get("conclusion")
                 for p in preuves_ecrites()] == ["non_facture_provisoire"])
    verifie("revue (b) : issue indéterminée, marqueur actif, arrêt, aucun rejeu",
            os.path.exists(en_cours) and not glob.glob(en_cours + ".annule-*")
            and res["reconciliation_requise"] and res["rapproches_429"] == 0
            and res["non_jouees"] == 1 and len(Etat.posts) == 1
            and "preuve finale non ecrite" in open(R6.JOURNAL, encoding="utf-8").read())

    print("revue (a) annulation manuelle portant « 429 » au registre : rapprochement refusé")
    ctx = preparer("manuel-429")
    cle = "fixture-manuel-429"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    ctx["transaction"].rapprochement_429 = False       # arrêt historique, réservation ouverte
    remise(["429"])
    jouer(ctx, [CELLULE_A], cle)
    with R6.RegistreGlobal(ctx["ledger"]) as reg:      # rapprochement manuel type colhomo
        reg.annuler(ident("item_a"), "colhomo 429 gen-x: metadata/content GET=404 twice")
    os.rename(en_cours, en_cours + ".archive-manuelle")  # hors motif .annule-*
    motif_manuel = ctx["transaction"].motif_refus_rapprochement_429(ident("item_a"), en_cours)
    verifie("revue (a) : motif de refus pour une annulation manuelle contenant 429",
            bool(motif_manuel) and "429 manuelle" in motif_manuel)
    ctx["transaction"].rapprochement_429 = True
    remise(["429"])
    res, dormeur = jouer(ctx, [CELLULE_A], cle)
    evts, ops = evenements(ctx["ledger"])
    verifie("revue (a) : nouveau 429 sur l'identité, zéro GET, aucune attente, arrêt",
            Etat.gets == [] and dormeur == [] and len(Etat.posts) == 1
            and res["reconciliation_requise"] and res["rapproches_429"] == 0
            and res["non_jouees"] == 1)
    verifie("revue (a) : aucune annulation automatique, réservation ouverte, marqueur gardé",
            not any(str(e.get("preuve", "")).startswith(R6.PREUVE_NON_FACTURE_429) for e in evts)
            and ops[ident("item_a")]["etat"] == "reservation" and os.path.exists(en_cours)
            and not preuves_ecrites()
            and "429 manuelle deja presente" in open(R6.JOURNAL, encoding="utf-8").read())
    # Témoin : une annulation manuelle sans « 429 » ne bloque pas le rapprochement.
    # Registre dédié : celui de « manuel-429 » porte encore la réservation ouverte
    # d'item_a (rapprochement automatique refusé plus haut, à dessein — préflight
    # exige une réconciliation avant toute nouvelle cellule sur CE registre) ; la
    # réutiliser ici ferait échouer le préflight de la cellule B pour une raison
    # étrangère à ce que ce témoin vérifie.
    ctx_temoin = preparer("manuel-429-temoin")
    cle_temoin = "fixture-manuel-temoin"
    ctx_temoin["transaction"].rapprochement_429 = False
    remise(["429"])
    jouer(ctx_temoin, [CELLULE_B], cle_temoin)
    with R6.RegistreGlobal(ctx_temoin["ledger"]) as reg:
        reg.annuler(ident("item_b", "droite", "adversaire"),
                    "generation metadata/content GET=404 twice; credits stable")
    verifie("revue (a) : témoin, annulation manuelle sans 429 : aucun refus",
            ctx_temoin["transaction"].motif_refus_rapprochement_429(
                ident("item_b", "droite", "adversaire")) is None)

    print("D5 seuil 429 dépassé sur la cellule rapprochée : notée non jouée avant l'arrêt")
    ctx = preparer("d5")
    remise(["429-sans-id", "429-sans-id", "429-sans-id", "429"])
    cle = "fixture-d5"
    cellules_d5 = [("gauche", "journaliste", "item_a"), ("centre", "journaliste", "item_a"),
                   ("droite", "journaliste", "item_a"), CELLULE_B]
    res, _ = jouer(ctx, cellules_d5, cle)
    nj = non_jouees(cle)
    verifie("D5 : arrêt seuil 429 après rapprochement",
            res["arret_seuil_429"] and res["rapproches_429"] == 1 and res["cellules"] == 0)
    verifie("D5 : les quatre cellules sont dans les non-jouées, la rapprochée en dernier",
            res["non_jouees"] == 4
            and [(x["camp"], x["identite"], x["item"]) for x in nj] == cellules_d5
            and nj[-1].get("rapprochement_429", {}).get("statut") == "non_facture")
    verifie("D5 : aucune réservation ouverte, marqueur archivé",
            not os.path.exists(R6.chemin_trace(cle) + ".en-cours")
            and all(o["etat"] != "reservation" for o in evenements(ctx["ledger"])[1].values()))

    print("(iii-a) STOP-R6 posé pendant l'attente AVANT la sonde 1 : indéterminé, aucune "
          "sonde, preuve persistée")
    ctx = preparer("iii-a")
    remise(["429", "ok"])
    cle = "fixture-iii-a"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    tranches = []

    def dormir_stop_avant(secondes):
        tranches.append(secondes)
        if len(tranches) == 3:
            open(R6.FICHIER_ARRET_R6, "w").close()

    res, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle, dormir=dormir_stop_avant)
    evts, ops = evenements(ctx["ledger"])
    verifie("iii-a : trois tranches de 10 s, aucune sonde prise (0 GET)",
            tranches == [10, 10, 10] and len(Etat.gets) == 0)
    verifie("iii-a : aucune annulation, marqueur gardé, arrêt",
            not any(e.get("type") == "annulation" for e in evts)
            and os.path.exists(en_cours) and res["reconciliation_requise"]
            and res["non_jouees"] == 1 and len(Etat.posts) == 1)
    preuves = preuves_ecrites()
    doc = json.loads(open(preuves[0], encoding="utf-8").read()) if preuves else {}
    verifie("iii-a : preuve persistée malgré l'absence de toute sonde (sens sûr)",
            len(preuves) == 1 and doc.get("conclusion") == "indetermine"
            and doc.get("sondes") == [] and "horodatage_429" in doc
            and "avant la sonde 1" in doc.get("motif", ""))

    print("(iii-b) STOP-R6 posé pendant l'attente ENTRE les deux sondes : indéterminé, "
          "arrêt, aucune preuve (comportement v1 inchangé)")
    ctx = preparer("iii-b")
    remise(["429", "ok"])
    cle = "fixture-iii-b"
    en_cours = R6.chemin_trace(cle) + ".en-cours"
    tranches = []

    def dormir_stop_entre(secondes):
        tranches.append(secondes)
        if len(tranches) == len(TRANCHES_AVANT_SONDE1) + 3:
            open(R6.FICHIER_ARRET_R6, "w").close()

    res, _ = jouer(ctx, [CELLULE_A, CELLULE_B], cle, dormir=dormir_stop_entre)
    evts, ops = evenements(ctx["ledger"])
    verifie("iii-b : attente avant sonde 1 complète, puis trois tranches, une seule sonde "
            "(2 GET)",
            tranches == TRANCHES_AVANT_SONDE1 + [10, 10, 10] and len(Etat.gets) == 2)
    verifie("iii-b : aucune annulation, marqueur gardé, arrêt, aucune preuve",
            not any(e.get("type") == "annulation" for e in evts)
            and os.path.exists(en_cours) and res["reconciliation_requise"]
            and res["non_jouees"] == 1 and not preuves_ecrites() and len(Etat.posts) == 1)

    print("D1 sequence_conforme : ordre strict hors cellules rapprochées")
    A, B, C = CELLULE_A, CELLULE_B, ("centre", "journaliste", "item_c")
    verifie("D1 : cellule rapprochée en fin de bloc acceptée",
            RUN.sequence_conforme([B, C, A], [A, B, C], {A}))
    verifie("D1 : cellule rapprochée retardée par STOP puis reprise acceptée",
            RUN.sequence_conforme([B, A, C], [A, B, C], {A}))
    verifie("D1 : même déplacement sans annulation 429 refusé",
            not RUN.sequence_conforme([B, C, A], [A, B, C], set()))
    verifie("D1 : cellule non rapprochée déplacée refusée",
            not RUN.sequence_conforme([A, C, B], [A, B, C], {A}))
    verifie("D1 : cellule rapprochée avancée refusée",
            not RUN.sequence_conforme([A, C, B], [A, B, C], {C}))
    verifie("D1 : cellule manquante ou dupliquée refusée",
            not RUN.sequence_conforme([B, A], [A, B, C], {A})
            and not RUN.sequence_conforme([B, A, A], [A, B, A], {A}))

    print("(f) runner : arguments d'amendement et garde STOP-R6")
    ordre = RUN.ORDRE_MODELES

    def monter_file(nom):
        dossier = os.path.join(TMP, nom)
        imported, inventory, ledger = environnement(dossier)
        parent = os.path.join(dossier, "parent.json")
        ecrire_json(parent, {"state": "READY"})
        floor = os.path.join(dossier, "floor.txt")
        with open(floor, "w") as fh:
            for i in range(40):
                fh.write(f"floor_{i}\tgauche\tjournaliste\n")
        rows = []
        for priorite, modele in enumerate(ordre, 1):
            nd = modele in RUN.NON_DETERMINISTES
            rows.append({
                "priority": priorite, "model": modele, "analysis_role": RUN.ROLES[modele],
                "provider_fixed": "FakeProvider", "non_deterministe": nd,
                "A4_requires_machine_floor": nd, "reasoning": "off", "max_tokens": 150,
                "max_price": {"prompt": "0.1", "completion": "0.2"},
                "call_cap_usd": "0.001", "model_cap_usd": "0.50", "settled_pilot_usd": "0",
                "steps": [
                    {"name": "f1", "pass": "campagne", "format": "q4", "cells": 894,
                     "max_prompt_tokens": 600, "trace_cap_usd": "0.30"},
                    {"name": "f2", "pass": "campagne", "format": "q4gab3", "cells": 316,
                     "max_prompt_tokens": 1000, "trace_cap_usd": "0.15"},
                    {"name": "plancher", "pass": "plancher", "format": "q4", "cells": 40,
                     "max_prompt_tokens": 600, "trace_cap_usd": "0.05",
                     "cell_list": floor, "cell_list_sha256": sha(floor)}]})
        queue = os.path.join(dossier, "queue.json")
        ecrire_json(queue, {
            "version": "R6-campaign-queue-1", "state": "QUEUE_READY", "executable": True,
            "parent_ready": {"path": parent, "sha256": sha(parent)},
            "global_cap_usd": "4.40", "account_reserve_usd": "1.50",
            "ledger_path": ledger, "import_manifest_path": imported,
            "models": rows, "excluded_models": sorted(RUN.EXCLUS)})
        with R6.RegistreGlobal(ledger) as reg:
            for i in range(20):
                identite_p = R6.identite_campagne(
                    ordre[0], "q4", R6.FORMATS["q4"], f"pilot_{i % 10}", "gauche",
                    "journaliste", "essai-1" if i < 10 else "essai-2")
                reg.reserver(identite_p, "0.001", "10", plafond_modele_usd="0.50",
                             empreinte_requete=str(i).zfill(64),
                             fournisseur_impose="FakeProvider", plafond_pilote_usd="0.02",
                             appels_pilote_max=20, borne_pilote_max_usd="0.001")
                reg.reconcilier(identite_p, "0", f"pilot-{i}")
        queue_sha = sha(queue)
        go = os.path.join(dossier, "GO.json")
        ecrire_json(go, {"state": "GO", "scope": "R6-campaign-one-model", "model": ordre[0],
                         "queue_manifest_sha256": queue_sha, "one_shot": True,
                         "socrates_reviewed": True})
        amendement = os.path.join(dossier, "amendement-429.md")
        with open(amendement, "w", encoding="utf-8") as fh:
            fh.write("amendement 429 fixture\n")
        # D6 : les tests injectent le chemin et l'empreinte scellés dans le code.
        RUN.AMENDEMENT_429_CHEMIN = amendement
        RUN.AMENDEMENT_429_SHA256 = sha(amendement)
        kwargs = dict(registre=ledger, import_path=imported, client_base=BASE, cle=CLE,
                      snapshot_cle=cle_fixture, snapshot_solde=Credits(), table=TABLE,
                      rapport_path=os.path.join(dossier, "rapport.md"),
                      recu_path=os.path.join(dossier, "recu.json"))
        return queue, queue_sha, go, amendement, kwargs

    queue, queue_sha, go, amendement, kwargs = monter_file("f-refus")
    bon_sha = sha(amendement)
    overrides = {"f1": [CELLULE_A], "f2": [("gauche", "journaliste", "item_b")],
                 "plancher": [("droite", "adversaire", "item_c")]}
    remise(["429"])
    attend_erreur("f : chemin sans SHA refusé", lambda: RUN.executer(
        queue, queue_sha, ordre[0], go, cellules_override=overrides,
        amendement_429=amendement, **kwargs), "vont ensemble")
    attend_erreur("f : SHA sans chemin refusé", lambda: RUN.executer(
        queue, queue_sha, ordre[0], go, cellules_override=overrides,
        amendement_429_sha256=bon_sha, **kwargs), "vont ensemble")
    attend_erreur("f : SHA faux refusé", lambda: RUN.executer(
        queue, queue_sha, ordre[0], go, cellules_override=overrides,
        amendement_429=amendement, amendement_429_sha256="0" * 64, **kwargs), "différente")
    attend_erreur("f : CLI avec un seul des deux arguments refusée", lambda: RUN.main(
        ["--file", queue, "--file-sha256", queue_sha, "--modele", ordre[0], "--go", go,
         "--amendement-429", amendement]), "vont ensemble")
    attend_erreur("f : CLI avec SHA faux refusée", lambda: RUN.main(
        ["--file", queue, "--file-sha256", queue_sha, "--modele", ordre[0], "--go", go,
         "--amendement-429", amendement, "--amendement-429-sha256", "f" * 64]), "différente")

    print("D6 activation réservée au document scellé dans le code")
    autre = os.path.join(TMP, "f-refus", "autre.md")
    open(autre, "w").close()
    attend_erreur("D6 : fichier quelconque (vide) avec son propre SHA refusé",
                  lambda: RUN.verifier_amendement_429(autre, sha(autre)), "chemin")
    attend_erreur("D6 : bon chemin, SHA différent de l'empreinte scellée refusé",
                  lambda: RUN.verifier_amendement_429(amendement, sha(autre)), "scellée")
    RUN.AMENDEMENT_429_SHA256 = None
    attend_erreur("D6 : empreinte scellée None, activation refusée même avec le bon fichier",
                  lambda: RUN.verifier_amendement_429(amendement, bon_sha), "non scellé")
    RUN.AMENDEMENT_429_SHA256 = bon_sha
    RUN.AMENDEMENT_429_CHEMIN = amendement + ".absent"
    attend_erreur("D6 : document scellé absent refusé", lambda: RUN.verifier_amendement_429(
        amendement + ".absent", bon_sha), "absent")
    RUN.AMENDEMENT_429_CHEMIN = amendement
    with open(amendement, "a", encoding="utf-8") as fh:
        fh.write("modification\n")
    attend_erreur("D6 : document modifié après scellement refusé",
                  lambda: RUN.verifier_amendement_429(amendement, bon_sha), "du fichier")
    with open(amendement, "w", encoding="utf-8") as fh:
        fh.write("amendement 429 fixture\n")
    verifie("D6 : dans le code livré, empreinte scellée None ou égale au document, chemin fixé",
            (SHA_SCELLE_CODE is None or (os.path.isfile(CHEMIN_SCELLE_CODE)
                                         and SHA_SCELLE_CODE == sha(CHEMIN_SCELLE_CODE)))
            and CHEMIN_SCELLE_CODE == os.path.join(
                ROOT, "resultats", "r6-amendement-429-v2-2026-09-11.md"))
    verifie("f : refus avant tout réseau, aucune trace, aucun STOP",
            Etat.posts == [] and Etat.gets == []
            and not glob.glob(os.path.join(R6.TRACES, "r6-*.jsonl*"))
            and not os.path.exists(R6.FICHIER_ARRET_R6))
    diag_actif = RUN.executer(queue, queue_sha, ordre[0], verifier=True,
                              amendement_429=amendement, amendement_429_sha256=bon_sha)
    diag_inactif = RUN.executer(queue, queue_sha, ordre[0], verifier=True)
    verifie("f : --verifier rapporte l'amendement actif ou inactif",
            diag_actif["amendement_429_actif"] is True
            and diag_actif["amendement_429"]["sha256"] == bon_sha
            and diag_inactif["amendement_429_actif"] is False
            and "amendement_429" not in diag_inactif)

    # Amendement actif, sonde /generation à 200 : indéterminé, arrêt, STOP-R6 créé.
    R6.DELAI_SONDE_429 = 0
    queue, queue_sha, go, amendement, kwargs = monter_file("f-stop-cree")
    remise(["429"], statut_generation=200)
    attend_erreur("f : interruption après rapprochement indéterminé", lambda: RUN.executer(
        queue, queue_sha, ordre[0], go, cellules_override=overrides,
        amendement_429=amendement, amendement_429_sha256=sha(amendement), **kwargs),
        "campagne interrompue")
    motif = (open(R6.FICHIER_ARRET_R6, encoding="utf-8").read()
             if os.path.exists(R6.FICHIER_ARRET_R6) else "")
    verifie("f : amendement transmis à la transaction (4 GET de sonde, 1 POST)",
            len(Etat.posts) == 1 and len(Etat.gets) == 4)
    verifie("f : STOP-R6 créé avec motif horodaté, modèle et raison",
            f"modele={ordre[0]}" in motif and "reconciliation_requise" in motif
            and "campagne interrompue" in motif and motif[:4].isdigit())
    verifie("f : GO conservé", os.path.exists(go))

    # Sans amendement, même 429 ambigu : aucune sonde, STOP-R6 créé AVANT le rapport.
    queue, queue_sha, go, amendement, kwargs = monter_file("f-sans-amendement")
    remise(["429"])
    stop_au_rapport = []
    rapport_original = RUN.ecrire_rapport

    def rapport_espion(*a, **k):
        stop_au_rapport.append(os.path.exists(R6.FICHIER_ARRET_R6))
        return rapport_original(*a, **k)

    RUN.ecrire_rapport = rapport_espion
    try:
        attend_erreur("f : interruption sans amendement", lambda: RUN.executer(
            queue, queue_sha, ordre[0], go, cellules_override=overrides, **kwargs),
            "campagne interrompue")
    finally:
        RUN.ecrire_rapport = rapport_original
    verifie("f : sans amendement, zéro GET de sonde et STOP-R6 créé",
            Etat.gets == [] and len(Etat.posts) == 1 and os.path.exists(R6.FICHIER_ARRET_R6))
    verifie("D3 : STOP-R6 déjà posé quand le rapport d'interruption est écrit",
            stop_au_rapport == [True])

    # STOP-R6 posé par l'utilisateur pendant l'étape : jamais écrasé.
    queue, queue_sha, go, amendement, kwargs = monter_file("f-stop-existant")
    remise(["ok", "ok"])
    Etat.stop_a_post = 1
    Etat.stop_texte = "signal-utilisateur\n"
    attend_erreur("f : interruption sur STOP utilisateur", lambda: RUN.executer(
        queue, queue_sha, ordre[0], go,
        cellules_override=dict(overrides, f1=[CELLULE_A, CELLULE_B]), **kwargs),
        "campagne interrompue")
    verifie("f : STOP existant non écrasé",
            open(R6.FICHIER_ARRET_R6, encoding="utf-8").read() == "signal-utilisateur\n"
            and len(Etat.posts) == 1)

    print("D1 runner : 429 rapproché en F1 puis campagne terminée et vérifiée")
    queue, queue_sha, go, amendement, kwargs = monter_file("d1")
    remise(["429", "ok", "ok", "ok", "ok"])
    fin = RUN.executer(queue, queue_sha, ordre[0], go,
                       cellules_override=dict(overrides, f1=[CELLULE_A, CELLULE_B]),
                       amendement_429=amendement, amendement_429_sha256=sha(amendement),
                       **kwargs)
    cle_f1 = R6.cle_run(ordre[0], "q4", "r6v2-campagne-f1")
    lignes_f1 = R6.lignes_existantes(R6.chemin_trace(cle_f1))
    verifie("D1 : campagne terminée, reçu écrit, GO consommé, 5 POST",
            fin.get("completed") is True and os.path.exists(kwargs["recu_path"])
            and os.path.exists(go + ".consomme") and len(Etat.posts) == 5)
    verifie("D1 : trace F1 B puis A, A annotée", [x["item"] for x in lignes_f1]
            == ["item_b", "item_a"] and "rapprochement_429" in lignes_f1[1])
    verifie("(ii) : le rapport compte le 429 rapproché",
            "1 429 ambigus rapprochés non facturés puis rejoués"
            in open(kwargs["rapport_path"], encoding="utf-8").read())
    with R6.RegistreGlobal(kwargs["registre"]) as reg:
        evts_d1 = list(reg.evenements)
    etape_f1 = {"format": "q4"}
    verifie("D1 : cellules_rapprochees_429 lit l'annulation au registre",
            RUN.cellules_rapprochees_429(evts_d1, ordre[0], "q4", "campagne") == {CELLULE_A}
            and RUN.cellules_rapprochees_429(evts_d1, ordre[0], "q4", "plancher") == set())
    attend_erreur("D1 : verifier_trace sans annulation reconnue garde l'ordre strict",
                  lambda: RUN.verifier_trace(ordre[0], "FakeProvider", etape_f1, cle_f1,
                                             [CELLULE_A, CELLULE_B]), "séquence")

    # verifier_operations_modele (garde des prédécesseurs) sur 894 + 316 + 40 cellules.
    plan = {"f1": [("gauche", "journaliste", f"i{k}") for k in range(894)],
            "f2": [("droite", "journaliste", f"j{k}") for k in range(316)],
            "plancher": [("gauche", "adversaire", f"k{k}") for k in range(40)]}
    politique = RUN.politique_modele(RUN.charger_file(queue, queue_sha), ordre[0])

    def registre_factice(deplacer, annoter):
        ops = []
        for etape in politique["steps"]:
            cells = list(plan[etape["name"]])
            if etape["name"] == "f1" and deplacer:
                cells = cells[1:] + cells[:1]
            ops += [{"etat": "reglee", "identite": R6.identite_campagne(
                ordre[0], etape["format"], R6.FORMATS[etape["format"]], item, camp, idt,
                etape["pass"])} for camp, idt, item in cells]
        camp, idt, item = plan["f1"][0]
        evts = ([{"type": "annulation", "preuve": "429-non-facture generation_id=g",
                  "identite": R6.identite_campagne(ordre[0], "q4", R6.FORMATS["q4"], item,
                                                   camp, idt, "campagne")}]
                if annoter else [])
        return type("Reg", (), {"operations": ops, "evenements": evts,
                                "operations_modele": lambda self, _m: self.operations})()

    RUN.verifier_operations_modele(registre_factice(True, True), politique, plan)
    verifie("D1 : prédécesseur avec cellule rapprochée en fin de bloc accepté", True)
    attend_erreur("D1 : même registre sans annulation 429-non-facture refusé",
                  lambda: RUN.verifier_operations_modele(registre_factice(True, False),
                                                         politique, plan), "séquence")

    print("D3 exceptions pendant lancer : STOP-R6 posé puis exception relancée")
    for nom, plan_posts, ajuster, types, fragment in (
            ("d3-fournisseur", ["ok-autre-fournisseur"], {}, (ValueError,), "fournisseur"),
            ("d3-credits", ["ok", "ok"], "credits", (OSError,), "OSError"),
            ("d3-preflight", ["ok"], "preflight", (R6.ErreurPreflight,), "limit_remaining"),
            ("d3-ctrl-c", ["429"], "ctrl-c", (KeyboardInterrupt,), "KeyboardInterrupt")):
        queue, queue_sha, go, amendement, kwargs = monter_file(nom)
        remise(plan_posts)
        extra = {}
        if ajuster == "credits":
            appels = [0]

            def solde_casse(_c, appels=appels):
                appels[0] += 1
                if appels[0] >= 2:
                    raise OSError("reseau")
                return {"total_credits": 10, "total_usage": 0}

            kwargs["snapshot_solde"] = solde_casse
        elif ajuster == "preflight":
            kwargs["snapshot_cle"] = lambda _c: {"data": {"limit": 4.4, "limit_remaining": "0",
                                                          "limit_reset": None}}
        elif ajuster == "ctrl-c":
            appels = [0]

            def solde_ctrl_c(_c, appels=appels):
                appels[0] += 1
                if appels[0] >= 2:          # pendant les sondes du rapprochement
                    raise KeyboardInterrupt
                return {"total_credits": 10, "total_usage": 0}

            kwargs["snapshot_solde"] = solde_ctrl_c
            extra = dict(amendement_429=amendement, amendement_429_sha256=sha(amendement))
        attend_erreur(f"{nom} : exception d'origine relancée", lambda: RUN.executer(
            queue, queue_sha, ordre[0], go,
            cellules_override=dict(overrides, f1=[CELLULE_A, CELLULE_B]), **kwargs, **extra),
            fragment, types)
        motif = (open(R6.FICHIER_ARRET_R6, encoding="utf-8").read()
                 if os.path.exists(R6.FICHIER_ARRET_R6) else "")
        verifie(f"{nom} : STOP-R6 posé avec modèle et type d'exception, GO conservé",
                f"modele={ordre[0]}" in motif and "exception" in motif and os.path.exists(go))

    print("(i) lanceur shell : arguments d'amendement transmis seulement s'ils sont fournis")
    source_sh = os.path.join(ROOT, "analyses", "r6_lancer_file_queue_ready.sh")
    verifie("(i) syntaxe bash du lanceur", subprocess.run(
        ["bash", "-n", source_sh], capture_output=True).returncode == 0)
    racine_sh = os.path.join(TMP, "lanceur")
    os.makedirs(os.path.join(racine_sh, "analyses"))
    os.makedirs(os.path.join(racine_sh, ".venv", "bin"))
    os.makedirs(os.path.join(racine_sh, "data", "traces", "reprise"))
    shutil.copy(source_sh, os.path.join(racine_sh, "analyses"))
    faux_python = os.path.join(racine_sh, ".venv", "bin", "python")
    with open(faux_python, "w") as fh:     # bouchon : n'exécute jamais le vrai runner
        fh.write("#!/bin/sh\nprintf '%s\\n' \"$@\" > argv.txt\nexit 3\n")
    os.chmod(faux_python, 0o755)
    texte_sh = open(source_sh, encoding="utf-8").read()
    queue_sh = re.search(r'^QUEUE="([^"]+)"', texte_sh, re.M).group(1)
    sha_sh = re.search(r'^QUEUE_SHA="([^"]+)"', texte_sh, re.M).group(1)
    commande_historique = ["analyses/r6_runner_campagnes.py", "--file", queue_sh,
                           "--file-sha256", sha_sh, "--modele", "deepseek/deepseek-v4-flash",
                           "--go", "data/traces/GO-R6-campagne-deepseek-deepseek-v4-flash.json"]

    def lancer_sh(env_extra):
        env = {k: v for k, v in os.environ.items() if not k.startswith("R6_AMENDEMENT_429")}
        env.update(env_extra)
        rc = subprocess.run(["bash", os.path.join(racine_sh, "analyses",
                                                  "r6_lancer_file_queue_ready.sh")],
                            env=env, capture_output=True).returncode
        return rc, open(os.path.join(racine_sh, "argv.txt")).read().splitlines()

    rc, argv = lancer_sh({})
    verifie("(i) sans variables : commande identique à l'historique (bash 3.2, set -u)",
            rc == 3 and argv == commande_historique)
    rc, argv = lancer_sh({"R6_AMENDEMENT_429": "resultats/r6-amendement-429-2026-09-11.md",
                          "R6_AMENDEMENT_429_SHA256": "ab" * 32})
    verifie("(i) avec variables : les deux arguments ajoutés en fin de commande",
            rc == 3 and argv == commande_historique + [
                "--amendement-429", "resultats/r6-amendement-429-2026-09-11.md",
                "--amendement-429-sha256", "ab" * 32])
finally:
    R6.RegistreGlobal.annuler = ANNULER_ORIGINAL
    SERVEUR.shutdown()
    shutil.rmtree(TMP)

if ECHECS:
    print(f"\n{len(ECHECS)} ECHEC(S) sur {N_VERIFS[0]} vérifications :")
    for e in ECHECS:
        print("  - " + e)
    sys.exit(1)
print(f"\nTOUT PASSE : {N_VERIFS[0]} vérifications, dossier temporaire effacé")
