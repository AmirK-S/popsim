#!/usr/bin/env python3
"""Rendu du manuscrit depuis le registre de chiffres — Methode v2 §1.3.

Le §1.3 impose que le manuscrit ne contienne AUCUNE valeur numerique tapee a la
main : il cite `{{R:id}}`, et ce script substitue depuis
`resultats/registre-chiffres.csv`. La porte P2 (`outils/portes/registre_chiffres.py`)
verifie l'absence de chiffres en dur ; ce script est la moitie qui rend le texte
lisible. Sans lui, le dispositif du §1.3 n'est pas utilisable.

GRAMMAIRE DES RENVOIS
---------------------
    {{R:id}}            -> la colonne `valeur`, VERBATIM
    {{R:id.champ}}      -> la colonne `champ`, VERBATIM
                           champ ∈ valeur, ic_bas, ic_haut, methode_ic,
                                   n_replicats, graine, script, commit,
                                   csv_source, grandeur
    {{R:id.ic}}         -> composite « [<ic_bas> ; <ic_haut>] »

Le rendu est une substitution VERBATIM de la chaine du CSV : le registre porte la
graphie publiee (« 20.7 », « 0.13 »), jamais un flottant a reformater. C'est
volontaire, et c'est le point : le meme top-1 portait trois graphies en v1
(`v1 §2.6`). Une grandeur = un id = une graphie. Le script ne fait aucun arrondi,
aucune conversion de separateur decimal, aucun formatage conditionnel — s'il en
faisait, la graphie cesserait d'etre gouvernee par le registre.

ECHECS BRUYANTS
---------------
Le rendu s'arrete (code 1) — il ne rend RIEN de partiel — si :
  1. un `id` cite est absent du registre ;
  2. la ligne citee porte `statut: retracte` ;
  3. un champ OBLIGATOIRE de la ligne citee est vide ;
  4. le champ demande est vide ;
  5. le champ demande vaut `ABSENT` (un `ABSENT` rendu dans le manuscrit serait
     une affirmation fausse presentee comme une valeur ; c'est exactement ce que
     le registre existe pour empecher) ;
  6. le nom de champ demande n'existe pas ;
  7. le registre est malforme (colonnes du §1.3 absentes, `id` en double).

CODES DE SORTIE (convention commune aux portes)
    0  rendu produit, ou verification sans probleme
    1  au moins un probleme : rien n'est rendu
    2  le script n'a pas pu s'executer (fichier absent, registre illisible)
    Un code 2 n'est PAS un succes.

USAGE
    rendu_registre.py --fichier article/manuscrit.md --sortie /tmp/rendu.md
    rendu_registre.py --fichier article/manuscrit.md            # -> stdout
    rendu_registre.py --fichier article/manuscrit.md --verifier  # ne rend rien
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RACINE / "outils" / "portes"))

# Schema du §1.3 : une seule definition, partagee avec la porte P2. Si les deux
# divergeaient, le registre passerait la porte et casserait le rendu.
from registre_chiffres import COLONNES, OBLIGATOIRES, STATUTS  # noqa: E402

NOM = "rendu_registre"
REGISTRE = RACINE / "resultats" / "registre-chiffres.csv"

RE_RENVOI = re.compile(r"\{\{R:([A-Za-z0-9_.\-]+)\}\}")
CHAMPS_RENDABLES = set(COLONNES) - {"id", "statut"}
CHAMPS_COMPOSITES = {"ic"}
MARQUE_ABSENT = "ABSENT"


class Probleme(Exception):
    """Une raison de ne rien rendre du tout."""


# --------------------------------------------------------------------------- #
# Registre                                                                     #
# --------------------------------------------------------------------------- #

def charge(chemin: Path) -> dict[str, dict[str, str]]:
    if not chemin.exists():
        raise FileNotFoundError(chemin)
    with chemin.open(encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        entete = [c.strip() for c in (lecteur.fieldnames or [])]
        if entete != COLONNES:
            raise Probleme(
                f"{chemin} : en-tete {entete} au lieu des colonnes du §1.3 "
                f"({','.join(COLONNES)})"
            )
        registre: dict[str, dict[str, str]] = {}
        for n, ligne in enumerate(lecteur, start=2):
            ident = (ligne.get("id") or "").strip()
            if not ident or ident.startswith("#"):
                continue
            if ident in registre:
                raise Probleme(
                    f"{chemin}:{n}: id « {ident} » deja utilise ligne "
                    f"{registre[ident]['_ligne']} — deux mesures differentes "
                    f"recoivent deux id differents (v2 §1.3)"
                )
            ligne = {k: (v or "").strip() for k, v in ligne.items() if k}
            ligne["_ligne"] = str(n)
            registre[ident] = ligne
    return registre


# --------------------------------------------------------------------------- #
# Resolution d'un renvoi                                                       #
# --------------------------------------------------------------------------- #

def decoupe(renvoi: str) -> tuple[str, str]:
    """« id.champ » -> (id, champ) ; « id » -> (id, "valeur").

    Un `id` peut contenir des points. On ne coupe que si le dernier segment est
    un nom de champ connu : ainsi `twin.top1` reste un id, tandis que
    `twin.top1.ic_bas` demande le champ `ic_bas` de l'id `twin.top1`.
    """
    if "." in renvoi:
        tete, _, queue = renvoi.rpartition(".")
        if tete and (queue in CHAMPS_RENDABLES or queue in CHAMPS_COMPOSITES):
            return tete, queue
    return renvoi, "valeur"


def resout(renvoi: str, registre: dict[str, dict[str, str]],
           ou: str) -> tuple[str | None, list[str]]:
    """Rend (texte, problemes). `texte` est None des qu'il y a un probleme."""
    ident, champ = decoupe(renvoi)
    ennuis: list[str] = []

    if ident not in registre:
        # Cas frequent : un nom de champ mal orthographie. `decoupe` n'a pas
        # reconnu la queue, elle est donc restee collee a l'id. On le dit
        # plutot que d'accuser l'id d'etre absent.
        tete, _, queue = ident.rpartition(".")
        if tete in registre:
            return None, [
                f"{ou}: {{{{R:{renvoi}}}}} — champ « {queue} » INCONNU pour l'id "
                f"« {tete} » ; champs rendables : "
                f"{', '.join(sorted(CHAMPS_RENDABLES))}, plus le composite « ic »."]
        proches = [c for c in registre if c.startswith(ident[:12])][:3]
        indice = f" — id proches : {', '.join(proches)}" if proches else ""
        return None, [f"{ou}: {{{{R:{renvoi}}}}} — id « {ident} » ABSENT du "
                      f"registre{indice}. Ajouter la grandeur dans "
                      f"resultats/registre-chiffres.csv avec son script, son "
                      f"commit et son CSV source (v2 §1.3)."]

    ligne = registre[ident]
    n = ligne["_ligne"]

    statut = ligne.get("statut", "")
    if statut == "retracte":
        return None, [f"{ou}: {{{{R:{renvoi}}}}} renvoie a une ligne RETRACTEE "
                      f"(registre ligne {n}) — citer l'id qui fait foi a la "
                      f"place ; une ligne retractee n'est jamais rendue."]
    if statut not in STATUTS:
        ennuis.append(f"{ou}: {{{{R:{renvoi}}}}} — statut « {statut} » inconnu "
                      f"(registre ligne {n}) ; attendu {sorted(STATUTS)}.")

    for col in OBLIGATOIRES:
        if not ligne.get(col):
            ennuis.append(f"{ou}: {{{{R:{renvoi}}}}} — champ obligatoire "
                          f"« {col} » VIDE pour « {ident} » (registre ligne {n}) ; "
                          f"une grandeur sans script ni CSV source n'est pas "
                          f"publiable (v2 §1.3).")

    if champ in CHAMPS_COMPOSITES:
        morceaux = {"ic": ("ic_bas", "ic_haut")}[champ]
        valeurs = []
        for col in morceaux:
            v = ligne.get(col, "")
            if not v:
                ennuis.append(f"{ou}: {{{{R:{renvoi}}}}} — « {col} » VIDE "
                              f"(registre ligne {n}).")
            elif v.upper() == MARQUE_ABSENT or v.upper().startswith(MARQUE_ABSENT):
                ennuis.append(f"{ou}: {{{{R:{renvoi}}}}} — « {col} » vaut ABSENT "
                              f"(registre ligne {n}) : cette grandeur n'a pas "
                              f"d'intervalle etabli. Rendre « ABSENT » dans le "
                              f"manuscrit serait publier une valeur fausse ; "
                              f"etablir l'intervalle, ou ne pas citer .ic.")
            valeurs.append(v)
        if ennuis:
            return None, ennuis
        return f"[{valeurs[0]} ; {valeurs[1]}]", []

    if champ not in CHAMPS_RENDABLES:
        return None, [f"{ou}: {{{{R:{renvoi}}}}} — champ « {champ} » inconnu ; "
                      f"champs rendables : {', '.join(sorted(CHAMPS_RENDABLES))}, "
                      f"plus le composite « ic »."]

    texte = ligne.get(champ, "")
    if not texte:
        ennuis.append(f"{ou}: {{{{R:{renvoi}}}}} — champ « {champ} » VIDE pour "
                      f"« {ident} » (registre ligne {n}).")
    elif texte.upper() == MARQUE_ABSENT or texte.upper().startswith(MARQUE_ABSENT):
        ennuis.append(f"{ou}: {{{{R:{renvoi}}}}} — champ « {champ} » vaut ABSENT "
                      f"(registre ligne {n}) : la provenance n'a pas ete etablie. "
                      f"Rendre « ABSENT » dans un texte publie serait pire que "
                      f"ne rien rendre ; etablir le champ, ou retirer le renvoi.")
    if ennuis:
        return None, ennuis
    return texte, []


# --------------------------------------------------------------------------- #
# Rendu d'un fichier                                                           #
# --------------------------------------------------------------------------- #

def rend(source: str, registre: dict[str, dict[str, str]],
         nom_fichier: str) -> tuple[str | None, list[str], int]:
    ennuis: list[str] = []
    compte = 0
    sortie: list[str] = []
    for i, brute in enumerate(source.splitlines(keepends=True), start=1):
        def remplace(m: re.Match) -> str:
            nonlocal compte
            compte += 1
            texte, pb = resout(m.group(1), registre, f"{nom_fichier}:{i}")
            if pb:
                ennuis.extend(pb)
                return m.group(0)
            return texte or ""
        sortie.append(RE_RENVOI.sub(remplace, brute))
    if ennuis:
        return None, ennuis, compte
    return "".join(sortie), [], compte


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fichier", required=True, help="fichier a rendre")
    ap.add_argument("--registre", default=str(REGISTRE))
    ap.add_argument("--sortie", help="fichier de sortie (defaut : stdout)")
    ap.add_argument("--verifier", action="store_true",
                    help="ne rend rien ; signale les problemes et sort 1 s'il y en a")
    a = ap.parse_args(argv)

    chemin = Path(a.fichier)
    if not chemin.is_absolute():
        chemin = RACINE / chemin
    chemin_reg = Path(a.registre)
    if not chemin_reg.is_absolute():
        chemin_reg = RACINE / chemin_reg

    if not chemin.exists():
        print(f"[{NOM}] IMPOSSIBLE D'EXECUTER : fichier absent : {chemin}",
              file=sys.stderr)
        return 2
    try:
        registre = charge(chemin_reg)
    except FileNotFoundError as e:
        print(f"[{NOM}] IMPOSSIBLE D'EXECUTER : registre absent : {e}",
              file=sys.stderr)
        return 2
    except Probleme as e:
        print(f"[{NOM}] ECHEC : {e}", file=sys.stderr)
        return 1

    texte, ennuis, compte = rend(
        chemin.read_text(encoding="utf-8"), registre, a.fichier)

    if ennuis:
        for e in ennuis:
            print(f"[{NOM}] {e}", file=sys.stderr)
        print(f"[{NOM}] ECHEC : {len(ennuis)} probleme(s) sur {compte} renvoi(s). "
              f"RIEN n'a ete rendu — un rendu partiel publierait un manuscrit "
              f"dont on croirait les chiffres verifies.", file=sys.stderr)
        return 1

    if a.verifier:
        print(f"[{NOM}] OK — {compte} renvoi(s) {{{{R:id}}}} resolu(s) dans "
              f"{a.fichier} ; {len(registre)} grandeur(s) au registre. "
              f"Mode --verifier : rien n'a ete ecrit.")
        return 0

    if a.sortie:
        Path(a.sortie).write_text(texte or "", encoding="utf-8")
        print(f"[{NOM}] OK — {compte} renvoi(s) rendu(s) -> {a.sortie}")
    else:
        sys.stdout.write(texte or "")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
