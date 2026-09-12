#!/usr/bin/env python3
"""P2 — Methode v2 §1.2 et §1.3 : aucun chiffre publie qui ne vienne du registre.

Trois controles :

  (a) INTEGRITE DU REGISTRE — resultats/registre-chiffres.csv a les douze colonnes
      du §1.3, aucun `id` en double, aucune ligne sans `script`/`commit`/`csv_source`,
      `statut` dans {courant, retracte, provisoire}, et toute ligne `retracte` cite
      la reference qui la remplace.

  (b) RENVOIS RESOLUS — tout `{{R:id}}` d'un fichier de sortie designe un `id`
      existant et de statut non `retracte`.

  (c) CHIFFRES EN DUR — aucun nombre a DEUX DECIMALES OU PLUS n'apparait hors motif
      `{{R:id}}` dans les fichiers de sortie. Fondement : v1 §2.6, le meme top-1 de
      20,7 % portait quatre intervalles incompatibles et trois graphies ; fait 6 de
      la v2, git ne voit pas les conflits semantiques.

Le controle (c) a un cout de migration reel sur un manuscrit deja ecrit. Il se lance
donc aussi en `--mode avertissement`, qui compte les valeurs refusees sans bloquer.

Exclusions du controle (c), volontairement etroites et listees ici parce qu'une
exclusion large rendrait la porte inoffensive :
  - blocs de code ``` et spans `…`         (ce ne sont pas des chiffres de prose)
  - DOI `10.xxxx/…` et identifiants arXiv  (ce ne sont pas des mesures)
  - le contenu meme d'un `{{R:id}}`
  - les lignes portant le commentaire `<!-- P2-exempt: <motif> -->`

Usage :
    registre_chiffres.py --fichier article/manuscrit.md --mode avertissement
    registre_chiffres.py --depuis origin/master
    registre_chiffres.py --registre-seul
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import (RACINE, Constat, abandon, lignes, masque_code,  # noqa: E402
                    sans_code_inline)

NOM = "P2 registre_chiffres"
REGISTRE = RACINE / "resultats" / "registre-chiffres.csv"

COLONNES = ["id", "grandeur", "valeur", "ic_bas", "ic_haut", "methode_ic",
            "n_replicats", "graine", "script", "commit", "csv_source", "statut"]
STATUTS = {"courant", "retracte", "provisoire"}
OBLIGATOIRES = ("id", "grandeur", "valeur", "script", "csv_source")

RE_RENVOI = re.compile(r"\{\{R:([A-Za-z0-9_.\-]+)\}\}")
# Deux decimales ou plus, virgule ou point decimal.
RE_NOMBRE = re.compile(r"(?<![\w.,])\d{1,3}(?:[  ]\d{3})*[.,]\d{2,}(?![\w])")
RE_DOI = re.compile(r"10\.\d{4,9}/\S+")
RE_ARXIV = re.compile(r"(?:arxiv[:\s]*)?\b\d{4}\.\d{4,5}(?:v\d+)?\b", re.I)
RE_EXEMPT = re.compile(r"<!--\s*P2-exempt")


def charge_registre(constat: Constat, chemin: Path = REGISTRE) -> dict[str, dict]:
    if not chemin.exists():
        constat.viole(chemin, 1, "registre absent",
                      "creer resultats/registre-chiffres.csv avec les 12 colonnes du §1.3")
        return {}
    with chemin.open(encoding="utf-8", newline="") as f:
        lecteur = csv.DictReader(f)
        entete = [c.strip() for c in (lecteur.fieldnames or [])]
        if entete != COLONNES:
            constat.viole(chemin, 1,
                          f"en-tete {entete} au lieu des colonnes du §1.3",
                          f"retablir exactement : {','.join(COLONNES)}")
            return {}
        registre: dict[str, dict] = {}
        for n, ligne in enumerate(lecteur, start=2):
            ident = (ligne.get("id") or "").strip()
            if not ident or ident.startswith("#"):
                continue
            if ident in registre:
                constat.viole(chemin, n, f"id « {ident} » deja utilise ligne "
                                         f"{registre[ident]['_ligne']}",
                              "deux mesures differentes recoivent deux id differents, "
                              "et un id ne sert jamais deux fois (v2 §1.3)")
                continue
            for col in OBLIGATOIRES:
                if not (ligne.get(col) or "").strip():
                    constat.viole(chemin, n, f"colonne « {col} » vide pour l'id « {ident} »",
                                  "renseigner, ou retirer la ligne : une grandeur sans "
                                  "script ni CSV source n'est pas publiable (v2 §1.3)")
            statut = (ligne.get("statut") or "").strip()
            # ABSENT est la seule facon de declarer un champ introuvable. Une grandeur
            # dont le CSV source ou la graine sont ABSENT ne peut pas etre « courant » :
            # c'est exactement le champ dont l'absence a produit 31,15 vs 31,62 %
            # (v1 §4.3, v2 §1.3).
            absents = [c for c in ("csv_source", "graine", "n_replicats", "script")
                       if (ligne.get(c) or "").strip().upper() == "ABSENT"]
            if absents and statut == "courant":
                constat.viole(chemin, n,
                              f"« {ident} » declare {absents} ABSENT mais porte statut courant",
                              "passer la ligne a « provisoire » tant que la graine, le "
                              "nombre de replicats et le CSV source ne sont pas etablis "
                              "(v1 §4.3 : 31,15 vs 31,62 %)")
            if statut not in STATUTS:
                constat.viole(chemin, n, f"statut « {statut} » inconnu pour « {ident} »",
                              f"employer l'un de {sorted(STATUTS)}")
            if statut == "retracte" and "->" not in (ligne.get("grandeur") or "") \
                    and not (ligne.get("commit") or "").strip():
                constat.viole(chemin, n, f"ligne retractee « {ident} » sans reference de "
                                         "remplacement",
                              "une ligne n'est jamais supprimee ; elle passe a retracte AVEC "
                              "la reference qui fait foi (v2 §1.3)")
            ligne["_ligne"] = n
            registre[ident] = ligne
    return registre


def controle_fichier(constat: Constat, chemin: Path, registre: dict[str, dict],
                     compteur: dict[str, int]) -> None:
    if not chemin.exists():
        constat.viole(chemin, 1, "fichier absent", "verifier le chemin")
        return
    src = lignes(chemin)
    en_code = masque_code(src)
    for i, brute in enumerate(src, start=1):
        if en_code[i - 1] or RE_EXEMPT.search(brute):
            continue

        # (b) renvois {{R:id}}
        for m in RE_RENVOI.finditer(brute):
            ident = m.group(1)
            compteur["renvois"] += 1
            if ident not in registre:
                constat.viole(chemin, i, f"renvoi {{{{R:{ident}}}}} absent du registre",
                              "ajouter la grandeur dans resultats/registre-chiffres.csv "
                              "avec son script, son commit et son CSV source")
            elif (registre[ident].get("statut") or "").strip() == "retracte":
                constat.viole(chemin, i, f"renvoi {{{{R:{ident}}}}} vers une ligne RETRACTEE",
                              "citer l'id qui fait foi a la place")

        # (c) chiffres en dur
        ligne = sans_code_inline(brute)
        ligne = RE_RENVOI.sub(lambda m: " " * len(m.group(0)), ligne)
        ligne = RE_DOI.sub(lambda m: " " * len(m.group(0)), ligne)
        ligne = RE_ARXIV.sub(lambda m: " " * len(m.group(0)), ligne)
        for m in RE_NOMBRE.finditer(ligne):
            compteur["en_dur"] += 1
            constat.viole(
                chemin, i,
                f"nombre en dur « {m.group(0)} » hors motif {{{{R:id}}}} "
                f"(col. {m.start() + 1})",
                "declarer la grandeur dans le registre et citer {{R:<id>}} ; "
                "le manuscrit ne tape jamais une valeur (v2 §1.3)",
            )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fichier", nargs="*", default=[])
    ap.add_argument("--depuis", help="controler les fichiers de sortie modifies depuis ce ref")
    ap.add_argument("--registre", default=str(REGISTRE))
    ap.add_argument("--registre-seul", action="store_true",
                    help="controle (a) uniquement")
    ap.add_argument("--mode", choices=("bloquant", "avertissement"), default="bloquant")
    a = ap.parse_args(argv)

    constat = Constat(NOM, a.mode)
    chemin_reg = Path(a.registre)
    if not chemin_reg.is_absolute():
        chemin_reg = RACINE / chemin_reg
    registre = charge_registre(constat, chemin_reg)
    constat.note(f"registre : {len(registre)} grandeur(s) declaree(s)")

    if a.registre_seul:
        return constat.conclure()

    cibles: list[Path] = []
    if a.fichier:
        cibles = [Path(f) if Path(f).is_absolute() else RACINE / f for f in a.fichier]
    elif a.depuis:
        from commun import fichiers_modifies, git_dispo
        if not git_dispo():
            return abandon(NOM, "git indisponible")
        for f in fichiers_modifies(a.depuis):
            p = RACINE / f
            if p.exists() and p.suffix in (".md", ".tex"):
                cibles.append(p)

    compteur = {"renvois": 0, "en_dur": 0}
    for c in cibles:
        controle_fichier(constat, c, registre, compteur)
    if cibles:
        constat.note(f"{len(cibles)} fichier(s) de sortie lus ; "
                     f"{compteur['renvois']} renvoi(s) {{{{R:id}}}}, "
                     f"{compteur['en_dur']} nombre(s) en dur a >= 2 decimales")
    return constat.conclure()


if __name__ == "__main__":
    raise SystemExit(main())
