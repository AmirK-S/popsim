#!/usr/bin/env python3
"""P4 — Methode v2 §1.2 et §1.4 : en-tete de statut, et retractation dans le meme commit.

Deux controles :

  (a) EN-TETE — tout fichier de `resultats/` porte l'en-tete du gabarit A2 :
      `statut:` valide, `mandat:`, `agent:`, `ecriture:`, `lecture_seule:`,
      `interdits:`, `cout_reel_usd:` ; et si `statut: retracte` ou `retracte_par:`,
      alors `fait_foi:` est obligatoire. Fondement : v1 §2.7, v2 §1.4.

  (b) RETRACTATION DANS LE MEME COMMIT — un commit qui ajoute, dans un fichier de
      `resultats/`, une ligne declarant un AUTRE fichier de `resultats/` refute,
      retracte ou perime, doit modifier ce fichier-la dans le MEME commit.
      Fondement : G3.1 de la v1, « absente » au 12/09 ; v2 §2, « un commit qui ecrit
      "refute" dans un audit sans modifier l'en-tete de l'audite echoue ». C'est le
      controle qui ferme les 6 minutes pendant lesquelles des rapports faux etaient
      publics sur GitHub (v1 §2.7).

PERIMETRE PAR DEFAUT : le diff (`--depuis`) ou des fichiers explicites. `--tous`
existe et mesure la dette : au 12/09, aucun des 321 rapports de resultats/ ne porte
d'en-tete A2. Rendre (a) bloquant sur tout l'arbre aujourd'hui fermerait le depot ;
il est bloquant sur les fichiers NOUVEAUX ou MODIFIES, ce qui est opposable sans
etre ingerable.

Usage :
    entetes.py --depuis origin/master
    entetes.py --fichier resultats/x-resultats.md
    entetes.py --tous --mode avertissement      # mesure de la dette
    entetes.py --retractation --depuis origin/master   # controle (b)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import (RACINE, Constat, abandon, commits, fichiers_du_commit,  # noqa: E402
                    git, git_dispo, lignes, normalise, resout_cibles)

NOM = "P4 entetes"

CLES_A2 = ("mandat", "agent", "ecriture", "lecture_seule", "interdits", "cout_reel_usd")
STATUTS_SIMPLES = {"courant", "provisoire"}
RE_STATUT = re.compile(r"^statut\s*:\s*(.+?)\s*$", re.I)
RE_PERIME = re.compile(r"^(perime_par|retracte_par)\s*:\s*(\S+)", re.I)
RE_FAIT_FOI = re.compile(r"^fait_foi\s*:\s*(\S+)", re.I)
FENETRE_ENTETE = 30

MOTS_INVALIDATION = ("refute", "refutee", "retracte", "retractee", "perime", "perimee",
                     "invalide", "invalidee", "abandonne", "abandonnee")
RE_FICHIER_RESULTATS = re.compile(r"[\w./-]*?([\w.-]+\.md)")


def controle_entete(constat: Constat, chemin: Path) -> None:
    if not chemin.exists():
        constat.viole(chemin, 1, "fichier absent", "verifier le chemin")
        return
    src = lignes(chemin)[:FENETRE_ENTETE]
    norm = [normalise(l) for l in src]

    statut = None
    ligne_statut = 0
    perime = None
    fait_foi = False
    for i, l in enumerate(src, start=1):
        n = norm[i - 1]
        m = RE_STATUT.match(n)
        if m and statut is None:
            statut, ligne_statut = m.group(1).strip(), i
        m = RE_PERIME.match(n)
        if m:
            perime = m.group(1)
        if RE_FAIT_FOI.match(n):
            fait_foi = True

    if statut is None and perime is None:
        constat.viole(chemin, 1,
                      f"aucune ligne « statut: » dans les {FENETRE_ENTETE} premieres lignes",
                      "poser l'en-tete du gabarit A2 (gabarits/entete.md) : statut, mandat, "
                      "agent, ecriture, lecture_seule, interdits, cout_reel_usd")
        return

    if statut is not None and statut not in STATUTS_SIMPLES and not statut.startswith(
            ("perime_par", "retracte_par")):
        constat.viole(chemin, ligne_statut, f"statut « {statut} » non reconnu",
                      "employer courant | provisoire | perime_par: <fichier> | "
                      "retracte_par: <fichier> (gabarit A2)")

    retracte = (perime == "retracte_par") or (statut or "").startswith("retracte")
    if retracte and not fait_foi:
        constat.viole(chemin, ligne_statut or 1,
                      "rapport retracte sans ligne « fait_foi: »",
                      "nommer le document qui fait foi a la place ; la retractation "
                      "n'efface rien mais elle doit dire ce qui remplace (v1 §2.7)")

    for cle in CLES_A2:
        if not any(n.startswith(cle + ":") for n in norm):
            constat.viole(chemin, 1, f"cle d'en-tete « {cle}: » absente",
                          f"ajouter « {cle}: … » (gabarit A2). Le perimetre d'ecriture "
                          f"declare est compare a git show --stat a chaque PR (v2 §1.4)")


def controle_retractation(constat: Constat, depuis: str, jusqu_a: str) -> None:
    for sha in commits(depuis, jusqu_a):
        touches = {c for _, c in fichiers_du_commit(sha)}
        touches_resultats = {c for c in touches if c.startswith("resultats/")}
        if not touches_resultats:
            continue
        diff = git("show", "--format=", "-U0", sha)
        for l in diff.splitlines():
            if not l.startswith("+") or l.startswith("+++"):
                continue
            n = normalise(l[1:])
            if not any(m in n for m in MOTS_INVALIDATION):
                continue
            for m in RE_FICHIER_RESULTATS.finditer(l[1:]):
                nom = m.group(1)
                candidat = f"resultats/{nom}"
                if not (RACINE / candidat).exists():
                    continue
                if candidat in touches:
                    continue
                constat.viole(
                    candidat, 1,
                    f"le commit {sha[:8]} declare ce rapport invalide "
                    f"(« {l[1:].strip()[:90]} ») sans toucher au fichier lui-meme",
                    "poser l'en-tete retracte_par:/fait_foi: DANS LE MEME COMMIT que "
                    "l'invalidation (G3.1 de la v1 ; v2 §2, retractation sans effacement)",
                )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--depuis")
    ap.add_argument("--jusqu-a", default="HEAD")
    ap.add_argument("--fichier", nargs="*", default=[])
    ap.add_argument("--tous", action="store_true")
    ap.add_argument("--retractation", action="store_true",
                    help="controle (b) seul, sur la plage de commits")
    ap.add_argument("--racine", default="resultats")
    ap.add_argument("--mode", choices=("bloquant", "avertissement"), default="bloquant")
    a = ap.parse_args(argv)

    constat = Constat(NOM, a.mode)

    if a.retractation:
        if not a.depuis:
            return abandon(NOM, "--retractation exige --depuis <ref>")
        if not git_dispo():
            return abandon(NOM, "git indisponible")
        try:
            controle_retractation(constat, a.depuis, a.jusqu_a)
        except RuntimeError as e:
            return abandon(NOM, str(e))
        return constat.conclure()

    if a.tous:
        cibles = sorted((RACINE / a.racine).glob("*.md"))
    else:
        cibles = resout_cibles(a.fichier, a.depuis, "*.md", a.racine)
        cibles = [c for c in cibles if a.racine in str(c)]

    for c in cibles:
        controle_entete(constat, c)
    constat.note(f"{len(cibles)} fichier(s) de resultats/ controle(s)")
    return constat.conclure()


if __name__ == "__main__":
    raise SystemExit(main())
