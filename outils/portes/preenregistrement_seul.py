#!/usr/bin/env python3
"""P1 — Methode v2 §1.2 : le preenregistrement est commis seul, et il est complet.

Deux controles independants, tous deux opposables :

  (a) COMMIT SEUL — tout commit qui AJOUTE un fichier `*-preenregistrement.md`
      n'ajoute et ne modifie rien d'autre. Fondement : v1 §2.3 et G0.1
      (« preenregistrement commis seul, script absent du depot a ce commit »),
      controle « fait une fois, non cable ».

  (b) PAP COMPLET — le fichier porte les huit sections du gabarit A1 et les cinq
      cles d'en-tete. Fondement : v2 §2.1, Brodeur et al. 2024 — le
      preenregistrement seul n'a aucun effet mesurable, seul un plan d'analyse
      complet en a un. Sans la section « Instrument », P1 refuse le fichier.

Usage :
    preenregistrement_seul.py --depuis origin/master       # controles (a) et (b) sur le diff
    preenregistrement_seul.py --fichier resultats/x-preenregistrement.md   # (b) seul
    preenregistrement_seul.py --tous                       # (b) sur tout resultats/
    [--mode avertissement] pour rapporter sans bloquer
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import (RACINE, Constat, abandon, commits, fichiers_du_commit,  # noqa: E402
                    git_dispo, lignes, normalise, resout_cibles)

NOM = "P1 preenregistrement_seul"
MOTIF_PREENREG = "*-preenregistrement*.md"

# Gabarit A1 : (numero de section, mots-cles dont AU MOINS UN doit figurer dans le titre)
SECTIONS_A1 = [
    (1, ("question", "refuterait", "refute")),
    (2, ("instrument",)),
    (3, ("famille de tests", "famille")),
    (4, ("prediction",)),
    (5, ("regle de decision", "decision")),
    (6, ("parametres figes", "parametres")),
    (7, ("clause de reduction", "reduction")),
    (8, ("clause",)),
]

CLES_ENTETE = ("statut", "famille", "rang", "commit_parent", "horodatage_ots")

# La section 2 doit prouver qu'on a vu l'instrument echouer (v2 §2.1 point 2, regle G0.5).
MOTIFS_VU_ECHOUER = ("vu echouer", "vu echouer sur", "a echoue sur", "echec observe",
                     "fait echouer")


def controle_commit_seul(constat: Constat, depuis: str, jusqu_a: str) -> None:
    for sha in commits(depuis, jusqu_a):
        fichiers = fichiers_du_commit(sha)
        ajouts_preenreg = [c for st, c in fichiers
                           if st == "A" and Path(c).match(MOTIF_PREENREG)]
        if not ajouts_preenreg:
            continue
        autres = [f"{st} {c}" for st, c in fichiers
                  if not (st == "A" and Path(c).match(MOTIF_PREENREG))]
        if len(ajouts_preenreg) > 1:
            constat.viole(
                ajouts_preenreg[0], 1,
                f"le commit {sha[:8]} ajoute {len(ajouts_preenreg)} preenregistrements a la fois",
                "un preenregistrement par commit (v1 §2.3, G0.1)",
            )
        if autres:
            constat.viole(
                ajouts_preenreg[0], 1,
                f"le commit {sha[:8]} ajoute un preenregistrement ET touche : "
                + ", ".join(autres[:6]) + ("…" if len(autres) > 6 else ""),
                "detacher ces fichiers dans un commit separe ; le preenregistrement "
                "est commis SEUL, avant tout calcul (v1 §2.3, G0.1)",
            )


def controle_pap(constat: Constat, chemin: Path) -> None:
    if not chemin.exists():
        constat.viole(chemin, 1, "fichier absent", "verifier le chemin")
        return
    src = lignes(chemin)
    norm = [normalise(l) for l in src]
    texte_norm = " ".join(norm)

    # (b1) cles d'en-tete du gabarit A1
    entete = norm[:25]
    for cle in CLES_ENTETE:
        if not any(l.startswith(cle + ":") for l in entete):
            constat.viole(
                chemin, 1,
                f"cle d'en-tete « {cle}: » absente des 25 premieres lignes",
                f"ajouter « {cle}: … » en tete, gabarit A1 (gabarits/preenregistrement.md)",
            )

    # (b2) les huit sections
    titres = [(i + 1, norm[i]) for i, l in enumerate(src) if l.lstrip().startswith("#")]
    for numero, mots in SECTIONS_A1:
        trouve = False
        for _, titre in titres:
            t = titre.lstrip("# ").strip()
            if re.match(rf"^{numero}\b", t) and any(m in t for m in mots):
                trouve = True
                break
            if any(m in t for m in mots) and re.search(rf"\b{numero}\b", t):
                trouve = True
                break
        if not trouve:
            constat.viole(
                chemin, 1,
                f"section A1 n°{numero} introuvable (attendu un titre « ## {numero}. … » "
                f"contenant {' ou '.join(mots)})",
                "reprendre le gabarit gabarits/preenregistrement.md ; sans la section 2 "
                "« Instrument » le fichier est refuse (v2 §2.1)",
            )

    # (b3) la section Instrument doit declarer un cas ou le controle a ete vu echouer
    if not any(m in texte_norm for m in MOTIFS_VU_ECHOUER):
        constat.viole(
            chemin, 1,
            "la section « Instrument » ne declare aucun cas ou le controle a ete VU ECHOUER",
            "ecrire « vu echouer sur : <fichier de test / cas> » — regle G0.5 de la v1 : "
            "un controle qu'on n'a jamais vu echouer n'est pas un controle",
        )

    # (b4) la clause « aucun appel n'a eu lieu »
    if "aucun appel" not in texte_norm:
        constat.viole(
            chemin, 1,
            "clause « Aucun appel n'a eu lieu » absente",
            "ajouter la clause 8 du gabarit A1 (declaration d'anteriorite au calcul)",
        )


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--depuis", help="reference git : controle le diff depuis cette reference")
    ap.add_argument("--jusqu-a", default="HEAD")
    ap.add_argument("--fichier", nargs="*", default=[])
    ap.add_argument("--tous", action="store_true",
                    help="controle PAP sur tous les preenregistrements de resultats/")
    ap.add_argument("--racine", default="resultats")
    ap.add_argument("--mode", choices=("bloquant", "avertissement"), default="bloquant")
    a = ap.parse_args(argv)

    constat = Constat(NOM, a.mode)

    if a.depuis:
        if not git_dispo():
            return abandon(NOM, "git indisponible, le controle (a) ne peut pas s'executer")
        try:
            controle_commit_seul(constat, a.depuis, a.jusqu_a)
        except RuntimeError as e:
            return abandon(NOM, str(e))

    if a.tous:
        cibles = sorted((RACINE / a.racine).glob(MOTIF_PREENREG))
    else:
        cibles = resout_cibles(a.fichier, a.depuis, MOTIF_PREENREG, a.racine)

    for c in cibles:
        controle_pap(constat, c)

    if not cibles and not a.depuis:
        constat.note("aucun preenregistrement cible ; preciser --fichier, --depuis ou --tous")
    else:
        constat.note(f"{len(cibles)} preenregistrement(s) controle(s) pour completude PAP")

    return constat.conclure()


if __name__ == "__main__":
    raise SystemExit(main())
