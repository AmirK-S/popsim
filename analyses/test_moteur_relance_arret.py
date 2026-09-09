"""Test du mecanisme de relance et du fichier d'arret, avec de fausses sorties de modele.

AUCUN appel de modele, AUCUN llama-server, aucun octet ecrit dans data/. Le faux moteur
rend des chaines programmees ; tout ce que le test verifie est du comptage et de
l'ecriture de trace, dans un dossier temporaire qui est efface a la fin.

Ce qu'il protege, et pourquoi il existe :
  1. le defaut de `r1_oracle_camps.lancer()` est inchange, donc R1 et R4 se rejouent au
     caractere pres (relance a invite modifiee, comptage des relances reussies) ;
  2. `--sans-relance` fait exactement ce que dit `resultats/r5-preenregistrement.md`
     section « Relance » : un echec de premiere tentative est un rejet, jamais rejoue, et
     l'exemple chiffre de la relance n'est plus jamais montre au modele, ce qui etait la
     cause des 45 recopies sur 45 mesurees en `resultats/r4-resultats.md` section 3.1 ;
  3. le compteur de rejets est bien ecrit dans la trace, ligne par ligne, et le taux de
     rejet dans le resume, pour qu'il se publie en tete du rapport ;
  4. `data/traces/STOP` arrete `r1_oracle_camps.py` et `a5_agents_locaux_gss.py` entre
     deux appels, trace fermee et relisible, reprise possible, code de sortie 0.

Usage : .venv/bin/python analyses/test_moteur_relance_arret.py
"""
import json, os, sys, tempfile, shutil

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RACINE, "analyses"))
import r1_oracle_camps as R1

TMP = tempfile.mkdtemp(prefix="r1test-")
R1.TRACES = TMP
R1.JOURNAL_RUN = os.path.join(TMP, "r1-run.log")
R1.FICHIER_ARRET = os.path.join(TMP, "STOP")

ITEMS = ["item_a", "item_b", "item_c"]
TABLE = {n: {"question": "Q " + n, "options": ["Yes", "No"]} for n in ITEMS}
INFO = {"nom": "faux", "quantification": "Q4", "gabarit": "qwen-chatml",
        "fichier": "faux.gguf", "coupure_publiee": "aucune"}

BON = "A: 60\nB: 40"
MAUVAIS = "Sure! Here is the distribution you asked for."


class FauxMoteur:
    """Rend des sorties programmees. Aucun reseau, aucun processus."""
    def __init__(self, sorties):
        self.sorties = list(sorties)
        self.prompts = []

    def decrire(self, prompt, n_predict, arrets):
        self.prompts.append(prompt)
        texte = self.sorties.pop(0) if self.sorties else BON
        return {"texte": texte, "duree_ms": 1.0, "tokens_generes": 5,
                "tokens_prompt": 10, "arret": "eos"}


def joue(cle, sorties, sans_relance, limite=2):
    moteur = FauxMoteur(sorties)
    r = R1.lancer(moteur, cle, INFO, ITEMS, TABLE, {}, ["gauche"], ["journaliste"],
                  fin_ts=1e18, suffixe="test", limite=limite, journal_tous=10_000,
                  n_predict=8, sans_relance=sans_relance)
    lignes = [json.loads(l) for l in open(R1.chemin_trace(cle, "test"), encoding="utf-8")]
    return moteur, r, lignes


ok = True
def verifie(nom, condition, detail=""):
    global ok
    ok = ok and condition
    print(("  OK   " if condition else "  RATE ") + nom + (("  " + detail) if detail else ""))


print("1. Defaut, comportement d'origine conserve")
# cellule 1 : premiere tentative mauvaise, relance bonne. cellule 2 : les deux mauvaises.
m, r, lignes = joue("c_defaut", [MAUVAIS, BON, MAUVAIS, MAUVAIS], sans_relance=False)
verifie("4 appels de modele pour 2 cellules", len(m.prompts) == 4, f"{len(m.prompts)}")
verifie("2 relances comptees", r["relances"] == 2, str(r["relances"]))
verifie("1 relance reussie", r["relances_reussies"] == 1, str(r["relances_reussies"]))
verifie("1 rejet", r["rejets"] == 1, str(r["rejets"]))
verifie("taux de rejet 0,5", r["taux_rejet"] == 0.5, str(r["taux_rejet"]))
verifie("cellule 1 : 2 tentatives, non rejetee",
        lignes[0]["n_tentatives"] == 2 and not lignes[0]["rejet"])
verifie("cellule 2 : 2 tentatives, rejetee",
        lignes[1]["n_tentatives"] == 2 and lignes[1]["rejet"])
verifie("la relance change bien l'invite", m.prompts[0] != m.prompts[1])
verifie("l'invite de relance montre l'exemple chiffre",
        "did not follow the format" in m.prompts[1])
verifie("sans_relance faux dans la trace", lignes[0]["sans_relance"] is False)

print("2. --sans-relance : un echec est un rejet, jamais rejoue")
m, r, lignes = joue("c_sans", [MAUVAIS, MAUVAIS], sans_relance=True)
verifie("2 appels de modele pour 2 cellules", len(m.prompts) == 2, f"{len(m.prompts)}")
verifie("0 relance", r["relances"] == 0, str(r["relances"]))
verifie("2 rejets", r["rejets"] == 2, str(r["rejets"]))
verifie("taux de rejet 1,0", r["taux_rejet"] == 1.0, str(r["taux_rejet"]))
verifie("aucune invite de relance envoyee",
        all("did not follow the format" not in p for p in m.prompts))
verifie("1 seule tentative par ligne",
        all(l["n_tentatives"] == 1 for l in lignes))
verifie("compteur de rejets dans la trace, 1 puis 2",
        [l["rejets_cumules"] for l in lignes] == [1, 2],
        str([l["rejets_cumules"] for l in lignes]))
verifie("sans_relance vrai dans la trace", all(l["sans_relance"] is True for l in lignes))
verifie("aucun arret demande", r["arret_demande"] is False)

print("3. --sans-relance ne touche pas les cellules qui passent du premier coup")
m, r, lignes = joue("c_ok", [BON, BON], sans_relance=True)
verifie("0 rejet, 2 appels", r["rejets"] == 0 and len(m.prompts) == 2)
verifie("distributions lues", lignes[0]["distribution"] == {"Yes": 0.6, "No": 0.4},
        str(lignes[0]["distribution"]))

print("4. Fichier d'arret : sortie propre entre deux appels")
open(R1.FICHIER_ARRET, "w").close()
m, r, lignes = joue("c_stop", [BON] * 6, sans_relance=False, limite=3)
verifie("aucun appel de modele apres la pose du fichier", len(m.prompts) == 0,
        f"{len(m.prompts)}")
verifie("arret_demande vrai", r["arret_demande"] is True)
journal = open(R1.JOURNAL_RUN, encoding="utf-8").read()
verifie("« ARRET DEMANDE » dans le journal", "ARRET DEMANDE" in journal)
os.remove(R1.FICHIER_ARRET)

print("5. Arret en cours de route, apres une cellule ecrite")
cle = "c_stop2"
moteur = FauxMoteur([BON] * 10)
_decrire = moteur.decrire
appels = {"n": 0}
def decrire_puis_poser(prompt, n_predict, arrets):
    appels["n"] += 1
    if appels["n"] == 1:
        open(R1.FICHIER_ARRET, "w").close()   # le fichier est pose pendant le premier appel
    return _decrire(prompt, n_predict, arrets)
moteur.decrire = decrire_puis_poser
r = R1.lancer(moteur, cle, INFO, ITEMS, TABLE, {}, ["gauche"], ["journaliste"],
              fin_ts=1e18, suffixe="test", limite=3, journal_tous=10_000, n_predict=8)
lignes = [json.loads(l) for l in open(R1.chemin_trace(cle, "test"), encoding="utf-8")]
verifie("1 seule cellule ecrite puis arret", len(lignes) == 1, str(len(lignes)))
verifie("la ligne ecrite est complete et relisible", lignes[0]["item"] == "item_a")
verifie("arret_demande vrai", r["arret_demande"] is True)
verifie("reprise possible : la cle est indexee",
        (R1.VERSION_PROMPT, "item_a", "gauche", "journaliste")
        in R1.index_existant(R1.chemin_trace(cle, "test")))
os.remove(R1.FICHIER_ARRET)

print("6. Le module de r4 s'importe et injecte son gabarit sans rien casser")
import r4_oracle_socle as R4
verifie("--sans-relance present dans r4",
        "--sans-relance" in open(os.path.join(RACINE, "analyses/r4_oracle_socle.py")).read())
verifie("le gabarit de completion de r4 est bien injecte dans r1",
        R1.gabarit is R4.gabarit)
INFO_R4 = dict(INFO, gabarit=R4.GABARIT)
moteur = FauxMoteur([MAUVAIS])
r = R1.lancer(moteur, "c_r4", INFO_R4, ITEMS, TABLE, {}, ["gauche"], ["journaliste"],
              fin_ts=1e18, suffixe="test", limite=1, journal_tous=10_000, n_predict=8,
              sans_relance=True)
verifie("en completion, une seule tentative et un rejet",
        len(moteur.prompts) == 1 and r["rejets"] == 1, f"{len(moteur.prompts)} appel(s)")
verifie("l'invite est bien celle a trois exemples de r4",
        "Millbrook" in moteur.prompts[0])
verifie("aucune recopie possible : l'exemple chiffre de la relance n'est jamais montre",
        "did not follow the format" not in moteur.prompts[0])

print("7. a5_agents_locaux_gss : le fichier d'arret, meme mecanisme")
import a5_agents_locaux_gss as A5
A5.TRACES = TMP
A5.JOURNAL_RUN = os.path.join(TMP, "a5-run.log")
A5.FICHIER_ARRET = R1.FICHIER_ARRET

FAUX_TRAVAUX = [({"pid": 1, "pli": 0}, 0, 0, "systeme"),
                ({"pid": 2, "pli": 0}, 0, 0, "systeme")]
A5.travaux = lambda *a, **k: iter(FAUX_TRAVAUX)


class FauxMoteurA5:
    """Faux client de scoring : rend une masse de lettres, aucun reseau."""
    def __init__(self):
        self.n = 0

    def tokens_des_lettres(self, prompt, n_lettres):
        return {l: i for i, l in enumerate("ABCDEFGHIJKLM"[:n_lettres])}, None

    def scorer(self, prompt, n_probs=40):
        self.n += 1
        if self.n == 1:
            open(A5.FICHIER_ARRET, "w").close()  # pose pendant le premier appel
        return {"top": [], "duree_ms": 1.0, "tokens_prompt": 5, "tokens_calcules": 1,
                "prompt_ms": 1.0}


m5 = FauxMoteurA5()
r5 = A5.lancer(m5, "C2", 1, False, [], ITEMS, [[0]], None, None, None, TABLE,
               fin_dure=1e18, suffixe="test", limite=None, journal_tous=10_000)
verifie("a5 : un seul appel, puis arret entre deux appels", m5.n == 1, str(m5.n))
verifie("a5 : arret_demande vrai", r5["arret_demande"] is True)
verifie("a5 : « ARRET DEMANDE » dans a5-run.log",
        "ARRET DEMANDE" in open(A5.JOURNAL_RUN, encoding="utf-8").read())
verifie("a5 : la ligne ecrite avant l'arret est relisible",
        len(open(A5.chemin_trace("C2", 1, "test"), encoding="utf-8").readlines()) == 1)
os.remove(A5.FICHIER_ARRET)

shutil.rmtree(TMP)
print("\n" + ("TOUS LES TESTS PASSENT" if ok else "AU MOINS UN TEST A RATE"))
sys.exit(0 if ok else 1)
