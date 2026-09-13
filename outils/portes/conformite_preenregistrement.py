#!/usr/bin/env python3
"""P9 — conformite au preenregistrement : le run a-t-il execute le plan ?

NUMEROTATION : le mandat l'appelait « P7 », deja pris par `outils/rendu_registre.py`.
Voir l'en-tete de `coherence_csv.py` (P8) pour le detail.

LE DEFAUT QU'ELLE FERME
-----------------------
`resultats/c7-nul-corrige-preenregistrement.md` §5 prescrivait **100 replicats**.
Le run s'est arrete a **20**, par un defaut implicite du script :

    int(os.environ.get("NREP", "20"))

Le chiffre (rho 0,974 [0,950 ; 0,993]) a ete publie au tableau 1, cite comme
temoin principal par trois rapports, et **envoye a un tiers**. Il a fallu un audit
commande a la main pour le voir. Les six portes existantes verifient qu'une
grandeur est declaree au registre ; **aucune ne compare le nombre de replicats
effectif a celui qui est prescrit**. Deux entiers, une comparaison : c'est tout
ce qu'il fallait.

CE QU'ELLE CONTROLE — deux entiers, jamais une phrase
-----------------------------------------------------
Deux colonnes de plus au registre :

  * `preenregistrement`      chemin du plan qui prescrit (ou `ABSENT`) ;
  * `n_replicats_prescrit`   l'entier prescrit, RECOPIE A LA MAIN depuis le plan
                             par qui declare la grandeur.

Puis, pour chaque ligne de statut `courant` ou `provisoire` :

  (a) `n_replicats_prescrit` est un entier > 0, ou `ABSENT`/vide ;
  (b) si un entier est prescrit, `n_replicats` doit etre un entier COMPARABLE —
      un entier nu. « 1 passe ; 20 tirages de departage » n'est pas comparable :
      la porte le refuse au lieu de deviner lequel des deux nombres compter ;
  (c) `n_replicats` == `n_replicats_prescrit`. Une inegalite dans les DEUX sens
      est signalee : un run trop court n'execute pas le plan, un run plus long
      non plus (il change la loi nulle simulee) ;
  (d) le fichier nomme par `preenregistrement` existe dans le depot.

POURQUOI LE CHIFFRE PRESCRIT EST RECOPIE A LA MAIN, ET NON EXTRAIT DU PLAN
--------------------------------------------------------------------------
Extraire « 100 replicats » du §5 d'un preenregistrement redige en francais
reviendrait a lire de la prose pour en inferer une intention — precisement ce qui
a coute quatre faux positifs a P4 le 12/09 et neuf notes fausses sur dix au filet
`--indice-prose` le 13/09. « 100 replicats par configuration, soit 1200 tirages »
contient deux entiers et un piege. La porte exige donc une **declaration**, comme
la retractation exige un marqueur : le chiffre prescrit est recopie par un humain
ou un agent qui a lu le plan, et la porte ne compare que des entiers declares.

COMPORTEMENT AVANT MIGRATION — la porte ne peut pas bloquer un depot non migre
-------------------------------------------------------------------------------
Au 13/09/2026 le registre a douze colonnes et n'en porte aucune des deux. La
porte le **constate en note et sort en 0** : elle ne signale rien, ne bloque rien,
et dit ce qu'il manque. `--exiger-colonnes` inverse ce choix pour le jour ou la
migration est faite ; c'est cet appel-la qui ira en CI.

Usage :
    conformite_preenregistrement.py
    conformite_preenregistrement.py --exiger-colonnes
    conformite_preenregistrement.py --registre <chemin> --mode avertissement
    conformite_preenregistrement.py --procedure-migration
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import RACINE, Constat  # noqa: E402

NOM = "P9 conformite_preenregistrement"
REGISTRE = RACINE / "resultats" / "registre-chiffres.csv"

COL_PREENREG = "preenregistrement"
COL_PRESCRIT = "n_replicats_prescrit"
COL_EFFECTIF = "n_replicats"
ABSENTS = ("", "ABSENT", "SANS OBJET", "-")
STATUTS_VIVANTS = {"courant", "provisoire"}

RE_ENTIER_NU = re.compile(r"^\d+$")

PROCEDURE = """\
PROCEDURE DE MIGRATION — deux colonnes au registre (P9)

Cette porte ne peut pas ecrire dans resultats/registre-chiffres.csv : le fichier
appartient a une autre branche en cours. La migration ci-dessous est a appliquer
par l'agent proprietaire du registre, ou par une passe ulterieure.

1. AJOUTER LES DEUX COLONNES EN FIN D'EN-TETE, dans cet ordre, apres `statut` :

       …,csv_source,statut,preenregistrement,n_replicats_prescrit

   En fin de ligne, jamais au milieu : toute insertion intercalaire casserait
   les lectures positionnelles et rendrait le diff illisible.

2. RENSEIGNER CHAQUE LIGNE. Trois valeurs possibles pour `n_replicats_prescrit` :
     * un entier   — recopie a la main depuis le plan, qui est nomme par
                     `preenregistrement` ;
     * ABSENT      — aucun plan ne prescrit de nombre de replicats ;
     * (vide)      — equivalent a ABSENT.
   `preenregistrement` porte le chemin du plan depuis la racine, ou ABSENT.

   Les deux lignes qui motivent cette porte, a titre d'exemple :
     rho-nul-marge-appariee-12conf        -> resultats/c7-nul-corrige-preenregistrement.md, 100
       (n_replicats = 20 : la porte SE FERME, et c'est le but — cette ligne est
        deja `retracte`, elle est donc hors perimetre ; la migration la renseigne
        pour la tracabilite)
     rho-nul-marge-appariee-12conf-n100   -> resultats/c7-nul-corrige-preenregistrement.md, 100
       (n_replicats = 100 : la porte passe)

3. METTRE A JOUR LA LISTE DE COLONNES DE P2. `outils/portes/registre_chiffres.py`
   exigeait un en-tete EXACTEMENT egal aux douze colonnes du §1.3 : il accepte
   desormais ces douze colonnes comme PREFIXE, suivies des colonnes optionnelles
   declarees dans COLONNES_OPTIONNELLES (les deux ci-dessus y figurent). Aucune
   action n'est requise a l'etape 3 : elle est faite, et c'est ce qui rend la
   migration du CSV possible sans casser P2 au meme commit.

4. PASSER LA PORTE EN MODE EXIGEANT, une fois le CSV migre :

       python3 outils/portes/conformite_preenregistrement.py --exiger-colonnes

   C'est cet appel qui va en CI. Tant que l'etape 2 n'est pas faite, l'appel sans
   --exiger-colonnes sort en 0 avec une note : la porte ne bloque pas un depot
   qu'elle ne peut pas encore controler.

5. NE PAS AUTOMATISER L'ETAPE 2. Le chiffre prescrit se lit dans une phrase
   francaise ; c'est un humain ou un agent qui le recopie, pas une expression
   reguliere. Voir l'en-tete de cette porte.
"""


def controle(constat: Constat, chemin: Path, exiger_colonnes: bool,
             compteur: dict[str, int]) -> bool:
    """Rend False si les colonnes manquent (et que ce n'est pas une violation)."""
    if not chemin.exists():
        constat.viole(chemin, 1, "registre absent",
                      "resultats/registre-chiffres.csv est la source des grandeurs")
        return True
    with chemin.open(encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        entete = [c.strip() for c in (lecteur.fieldnames or [])]
        manquantes = [c for c in (COL_PREENREG, COL_PRESCRIT) if c not in entete]
        if manquantes:
            if exiger_colonnes:
                constat.viole(chemin, 1,
                              f"colonne(s) {manquantes} absente(s) du registre",
                              "appliquer la procedure de migration : "
                              "conformite_preenregistrement.py --procedure-migration")
                return True
            constat.note(
                f"colonne(s) {manquantes} absente(s) : la porte ne controle RIEN "
                f"et ne bloque rien. Appliquer la migration "
                f"(--procedure-migration), puis --exiger-colonnes.")
            return False
        if COL_EFFECTIF not in entete:
            constat.viole(chemin, 1, f"colonne « {COL_EFFECTIF} » absente",
                          "c'est une des douze colonnes du §1.3")
            return True

        for n, ligne in enumerate(lecteur, start=2):
            ident = (ligne.get("id") or "").strip()
            if not ident or ident.startswith("#"):
                continue
            statut = (ligne.get("statut") or "").strip()
            if statut not in STATUTS_VIVANTS:
                compteur["hors_perimetre"] += 1
                continue

            prescrit = (ligne.get(COL_PRESCRIT) or "").strip()
            plan = (ligne.get(COL_PREENREG) or "").strip()

            if prescrit.upper() in ABSENTS:
                compteur["sans_prescription"] += 1
                continue
            if not RE_ENTIER_NU.match(prescrit) or int(prescrit) <= 0:
                constat.viole(chemin, n,
                              f"« {ident} » : n_replicats_prescrit = "
                              f"« {prescrit[:40]} » n'est pas un entier > 0",
                              "un entier nu recopie du plan, ou ABSENT. La porte "
                              "ne devine pas un nombre dans une phrase")
                continue
            prescrit_i = int(prescrit)

            if plan.upper() in ABSENTS:
                constat.viole(chemin, n,
                              f"« {ident} » prescrit {prescrit_i} replicats sans "
                              f"nommer le plan qui le prescrit",
                              "renseigner preenregistrement: resultats/<plan>.md ; "
                              "une prescription sans plan n'est opposable a personne")
            elif not (RACINE / plan).exists():
                constat.viole(chemin, n,
                              f"« {ident} » nomme un preenregistrement introuvable : "
                              f"{plan}",
                              "corriger le chemin depuis la racine du depot")

            effectif = (ligne.get(COL_EFFECTIF) or "").strip()
            if not RE_ENTIER_NU.match(effectif):
                constat.viole(chemin, n,
                              f"« {ident} » prescrit {prescrit_i} replicats mais "
                              f"n_replicats = « {effectif[:50]} » n'est pas un "
                              f"entier comparable",
                              "ecrire le nombre de replicats comme un entier nu ; "
                              "les precisions de methode vont dans « graine » ou "
                              "« methode_ic ». La porte refuse de choisir un nombre "
                              "dans une enumeration")
                continue
            compteur["compares"] += 1
            effectif_i = int(effectif)
            if effectif_i < prescrit_i:
                constat.viole(chemin, n,
                              f"« {ident} » : run a {effectif_i} replicats alors que "
                              f"{plan or 'le plan'} en prescrit {prescrit_i}",
                              "rejouer aux replicats prescrits, ou amender le plan "
                              "AVANT de publier. C'est le defaut du 13/09 : "
                              "NREP par defaut a 20 au lieu des 100 prescrits, "
                              "chiffre publie puis envoye a un tiers")
            elif effectif_i > prescrit_i:
                constat.viole(chemin, n,
                              f"« {ident} » : run a {effectif_i} replicats alors que "
                              f"{plan or 'le plan'} en prescrit {prescrit_i}",
                              "un run plus long que le plan n'est pas le plan : "
                              "amender le preenregistrement et le dire, ou ramener "
                              "le run au nombre prescrit")
    return True


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--registre", default=str(REGISTRE))
    ap.add_argument("--exiger-colonnes", action="store_true",
                    help="echouer si les deux colonnes ne sont pas encore migrees")
    ap.add_argument("--procedure-migration", action="store_true",
                    help="imprimer la procedure de migration et sortir")
    ap.add_argument("--mode", choices=("bloquant", "avertissement"), default="bloquant")
    a = ap.parse_args(argv)

    if a.procedure_migration:
        print(PROCEDURE)
        return 0

    constat = Constat(NOM, a.mode)
    compteur = {"compares": 0, "sans_prescription": 0, "hors_perimetre": 0}
    chemin = Path(a.registre)
    if not chemin.is_absolute():
        chemin = RACINE / chemin
    migre = controle(constat, chemin, a.exiger_colonnes, compteur)
    if migre:
        constat.note(f"{compteur['compares']} grandeur(s) comparee(s) au plan ; "
                     f"{compteur['sans_prescription']} sans prescription declaree ; "
                     f"{compteur['hors_perimetre']} hors perimetre (retracte)")
    return constat.conclure()


if __name__ == "__main__":
    raise SystemExit(main())
