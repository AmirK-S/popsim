"""Runner scellé des pilotes R6 payants, deux passes des dix mêmes cellules.

Le runner ne crée jamais de GO et ne retire jamais STOP-R6. En mode vérification il ne lit
ni clé ni réseau. En exécution, il exige un manifeste READY hashé et un GO JSON propre au
modèle, gardé par verrou et consommé seulement lorsque les deux passes sont complètes.
"""

import argparse
import fcntl
import hashlib
import json
import os
import sys
from decimal import Decimal

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import r6_oracle_distant as R6


def sha256(chemin):
    h = hashlib.sha256()
    with open(chemin, "rb") as fh:
        for bloc in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(bloc)
    return h.hexdigest()


def charger_manifeste(chemin, empreinte):
    calculee = sha256(chemin)
    if not empreinte or calculee != empreinte:
        raise ValueError("empreinte du manifeste PREPARE/READY differente")
    d = json.load(open(chemin, encoding="utf-8"))
    if not str(d.get("version", "")).startswith("R6-campaign-readiness-"):
        raise ValueError("version de manifeste readiness inconnue")
    if not isinstance(d.get("panel"), list):
        raise ValueError("panel absent du manifeste")
    return d, calculee


def politique_modele(manifeste, modele):
    lignes = [x for x in manifeste["panel"] if x.get("model") == modele]
    if len(lignes) != 1:
        raise ValueError("modele absent ou duplique dans le manifeste")
    ligne = lignes[0]
    proposition = ligne.get("provider_proposal")
    pilote = ligne.get("pilot_plan")
    if not isinstance(proposition, dict) or not proposition.get(
            "required_payload_parameters_supported"):
        raise ValueError("modele non compatible avec la charge R6 inchangee")
    verification_seule = bool(
        modele == R6.MODELE_PILOTE and ligne.get("pilot_complete") is True
        and isinstance(pilote, dict) and pilote.get("verification_only") is True)
    if not isinstance(pilote, dict) or (not pilote.get("required") and not verification_seule):
        raise ValueError("aucun nouveau pilote autorise pour ce modele")
    if pilote.get("cells_per_pass") != 10 or pilote.get("passes") != ["essai-1", "essai-2"]:
        raise ValueError("plan pilote different de deux fois dix")
    if pilote.get("reasoning") != "off" or pilote.get("max_tokens") != 150:
        raise ValueError("charge pilote differente du protocole")
    fournisseur = proposition.get("provider_name")
    if not fournisseur or ligne.get("provider_fixed") != fournisseur:
        raise ValueError("fournisseur unique non fige")
    politique = {
        "model": modele,
        "provider": fournisseur,
        "calls": 20,
        "total_cap": R6.dollars(pilote.get("pilot_total_cap_usd")),
        "call_cap": R6.dollars(pilote.get("reserved_call_usd")),
        "model_cap": R6.dollars(ligne.get("prepared_model_spend_cap_usd")),
        "max_tokens": 150,
        "max_prompt_tokens": pilote.get("max_prompt_tokens"),
        "max_price": {
            "prompt": R6.dollars(pilote.get("max_price_prompt_usd_per_million")),
            "completion": R6.dollars(
                pilote.get("max_price_completion_usd_per_million")),
        },
        "cell_list": pilote.get("cell_list"),
        "cell_list_sha256": pilote.get("cell_list_sha256"),
        "verification_only": verification_seule,
    }
    if politique["total_cap"] <= 0 or politique["total_cap"] > R6.LIMITE_CLE_R6:
        raise ValueError("plafond pilote hors budget global")
    if politique["model_cap"] <= 0 or politique["model_cap"] > R6.LIMITE_CLE_R6:
        raise ValueError("plafond modele hors budget global")
    if (politique["call_cap"] <= 0
            or politique["call_cap"] * politique["calls"] != politique["total_cap"]):
        raise ValueError("reservation et plafond pilote incoherents")
    if politique["max_prompt_tokens"] != 600:
        raise ValueError("borne de prompt pilote differente")
    if not politique["cell_list"] or sha256(politique["cell_list"]) != politique[
            "cell_list_sha256"]:
        raise ValueError("liste des dix cellules differente")
    return politique


def verifier_go(chemin, modele, empreinte_manifeste):
    d = json.load(open(chemin, encoding="utf-8"))
    attendu = {"state": "GO", "scope": "R6-pilot-one-model", "model": modele,
               "prepare_manifest_sha256": empreinte_manifeste, "one_shot": True}
    if any(d.get(k) != v for k, v in attendu.items()):
        raise ValueError("GO one-shot absent, different ou hors modele")
    return d


def verifier_deja_consomme(registre, inventaire, modele):
    with R6.RegistreGlobal(registre) as reg:
        reg.verifier_integrite(inventaire)
        return len(reg.operations_pilote(modele)), reg.total_pilote(modele)


def verifier_identite_passes(modele, cles):
    ensembles = []
    for cle in cles:
        lignes = R6.lignes_existantes(R6.chemin_trace(cle))
        if len(lignes) != 10:
            raise ValueError("passe pilote incomplete")
        ensembles.append([(x["item"], x["camp"], x["identite"]) for x in lignes])
        if any(x.get("modele") != modele for x in lignes):
            raise ValueError("modele renvoye dans une trace differente")
    if ensembles[0] != ensembles[1] or len(set(ensembles[0])) != 10:
        raise ValueError("les deux passes ne portent pas les dix memes cellules ordonnees")


def executer(manifeste_path, manifeste_sha, modele, go_path=None, verifier=False,
             registre=None, import_path=None, client_base=None, cle=None,
             snapshot_cle=None, snapshot_solde=None, table=None):
    manifeste, empreinte = charger_manifeste(manifeste_path, manifeste_sha)
    politique = politique_modele(manifeste, modele)
    garde = manifeste.get("pilot_runner_guard")
    if not isinstance(garde, dict):
        raise ValueError("configuration du runner absente du manifeste")
    registre = registre or garde.get("ledger_path")
    import_path = import_path or garde.get("import_manifest_path")
    if not isinstance(registre, str) or not registre:
        raise ValueError("ledger pilote absent du manifeste")
    if not isinstance(import_path, str) or not import_path:
        raise ValueError("manifeste d'import absent du manifeste readiness")
    inventaire, _ = R6.charger_import(import_path)
    engages, cout = verifier_deja_consomme(registre, inventaire, modele)
    diagnostic = {"model": modele, "provider": politique["provider"],
                  "pilot_operations": engages, "pilot_cost_usd": str(cout),
                  "model_cap_usd": str(politique["model_cap"]),
                  "mode": "verification-hors-reseau" if politique["verification_only"]
                          else "pilote-prepare",
                  "manifest_sha256": empreinte, "executable": False}
    if verifier:
        return diagnostic
    if manifeste.get("state") != "READY" or manifeste.get("executable") is not True:
        raise ValueError("manifeste PREPARE non executable")
    if politique["verification_only"]:
        raise ValueError("pilote DeepSeek deja consomme; verification hors reseau seulement")
    if engages >= 20:
        raise ValueError("GO refuse : pilote modele deja consomme")
    if R6.arret_demande():
        raise ValueError("STOP present; aucun pilote")
    if not go_path or not os.path.exists(go_path):
        raise ValueError("GO one-shot modele absent")

    verrou_path = go_path + ".lock"
    with open(verrou_path, "a") as verrou:
        fcntl.flock(verrou, fcntl.LOCK_EX | fcntl.LOCK_NB)
        verifier_go(go_path, modele, empreinte)
        if R6.arret_demande():
            raise ValueError("STOP present; aucun pilote")
        cellules = R6.lire_liste(politique["cell_list"])
        if len(cellules) != 10:
            raise ValueError("liste pilote ne contient pas dix cellules")
        table = table or R6.nomenclature()
        cle_api = cle if cle is not None else R6.cle_api()
        base = client_base or R6.BASE
        max_price = {k: str(v) for k, v in politique["max_price"].items()}
        client = R6.ClientChat(cle_api, base=base, raisonnement="off",
                               fournisseur=politique["provider"], max_price=max_price)
        cles = []
        for numero, passe in enumerate(("essai-1", "essai-2"), 1):
            if R6.arret_demande():
                raise ValueError("STOP present entre les passes")
            suffixe = ("r6v2-" + modele.replace("/", "-").replace(":", "-")
                       + f"-essai{numero}")
            cle_trace = R6.cle_run(modele, "q4", suffixe)
            cles.append(cle_trace)
            transaction = R6.TransactionPayante(
                registre, inventaire, passe, str(politique["call_cap"]),
                politique["max_prompt_tokens"],
                snapshot_cle or R6.statut_cle, snapshot_solde or R6.solde,
                plafond_modele=str(politique["model_cap"]),
                politique_pilote=politique, fichier_go=go_path)
            budget = R6.Budget(str(politique["total_cap"]),
                               float(politique["max_price"]["prompt"]) / 1_000_000,
                               float(politique["max_price"]["completion"]) / 1_000_000,
                               R6.JETONS_ESTIMES["q4"])
            resultat = R6.lancer(
                client, modele, "q4", table, cellules, budget, cle_trace,
                n_predict=150, limite=10, transaction=transaction,
                manifeste_import=import_path)
            if resultat.get("reconciliation_requise") or resultat.get("arret_demande"):
                raise ValueError("pilote interrompu; GO conserve pour reprise exacte")
        verifier_identite_passes(modele, cles)
        consomme = go_path + ".consomme"
        if os.path.exists(consomme):
            raise ValueError("archive GO deja presente")
        os.replace(go_path, consomme)
        diagnostic.update(executable=True, completed=True, traces=cles,
                          go_consumed_to=consomme)
        return diagnostic


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifeste", required=True)
    ap.add_argument("--manifeste-sha256", required=True)
    ap.add_argument("--modele", required=True)
    ap.add_argument("--go")
    ap.add_argument("--verifier", action="store_true")
    args = ap.parse_args(argv)
    resultat = executer(args.manifeste, args.manifeste_sha256, args.modele,
                        args.go, args.verifier)
    print(json.dumps(resultat, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
