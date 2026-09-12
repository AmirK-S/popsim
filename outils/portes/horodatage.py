#!/usr/bin/env python3
"""P6 — Methode v2 §1.2 : tout preenregistrement fusionne sur master a son `.ots`.

Fondement : `[prereg]` partie 3, et v1 §3 bis — sur 28 paires plan/resultat
verifiables, trois ont plan et resultat dans le MEME commit (ordre interne non
prouvable) et quatre ne sont pas versionnees. Sans horodatage par un tiers, le mot
« preenregistre » n'est pas attestable.

ETAT DE CETTE PORTE — a lire avant de s'y fier :

  * Controle (a) PRESENCE — pour chaque `*-preenregistrement.md` suivi par git,
    `preuves/<nom>.ots` existe et n'est pas vide. OPERATIONNEL : ne demande ni le
    binaire `ots`, ni le reseau.

  * Controle (b) VERIFICATION CRYPTOGRAPHIQUE — `ots verify` sur le recu, et
    correspondance entre le condensat horodate et le SHA du commit. NON OPERATIONNEL
    au 12/09/2026 : le binaire `ots` n'est pas installe sur cette machine, et sa
    verification exige un acces reseau a un calendrier, exclu du mandat courant.
    Installation : `pip install opentimestamps-client` (ou `brew install opentimestamps`),
    puis `ots stamp preuves/<nom>.ots` ; le hook post-commit du §1.2 l'appelle.
    Tant que `ots` est absent, (b) ne s'execute pas et le declare : la porte ne
    pretend PAS avoir verifie ce qu'elle n'a pas verifie.

Un `--exiger-ots` force l'echec si le binaire manque, pour le jour ou le socle
declare la chaine complete comme prerequis.

Usage :
    horodatage.py --depuis origin/master
    horodatage.py --tous --mode avertissement     # mesure de la dette
    horodatage.py --etat                          # dit seulement si ots est la
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import RACINE, Constat, abandon, git, git_dispo, resout_cibles  # noqa: E402

NOM = "P6 horodatage"
PREUVES = "preuves"
MOTIF = "*-preenregistrement*.md"
INSTALLATION = "pip install opentimestamps-client   # puis : ots stamp <fichier>"


def ots_dispo() -> str | None:
    chemin = shutil.which("ots")
    if not chemin:
        return None
    try:
        subprocess.run([chemin, "--version"], capture_output=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return chemin


def recu_attendu(preenreg: Path) -> Path:
    return RACINE / PREUVES / (preenreg.name + ".ots")


def controle_presence(constat: Constat, preenreg: Path) -> Path | None:
    recu = recu_attendu(preenreg)
    if not recu.exists():
        constat.viole(
            preenreg, 1,
            f"aucun recu d'horodatage : {PREUVES}/{recu.name} est absent",
            f"horodater le preenregistrement avant de le fusionner sur master : "
            f"`ots stamp {preenreg.relative_to(RACINE)}` puis deplacer le .ots dans "
            f"{PREUVES}/ ({INSTALLATION})",
        )
        return None
    if recu.stat().st_size == 0:
        constat.viole(recu, 1, "recu d'horodatage vide",
                      "regenerer le recu ; un fichier vide atteste d'une date fausse, "
                      "ce qui est pire que pas de recu")
        return None
    return recu


def controle_verification(constat: Constat, preenreg: Path, recu: Path, binaire: str) -> None:
    # `ots verify` sans `-f` suppose que le fichier horodate est a cote du recu,
    # meme nom sans « .ots ». Ici le recu vit dans preuves/ et le fichier dans
    # resultats/ : sans `-f`, la commande echoue TOUJOURS (« Could not open
    # target »), y compris sur un recu parfaitement valide. Il faut pointer
    # explicitement vers le fichier reellement horodate.
    res = subprocess.run([binaire, "verify", "-f", str(preenreg), str(recu)],
                         capture_output=True, text=True, timeout=120)
    if res.returncode != 0:
        constat.viole(recu, 1,
                      f"`ots verify` echoue : {(res.stderr or res.stdout).strip()[:160]}",
                      "le recu ne prouve pas la date annoncee ; regenerer ou retirer "
                      "la mention « preenregistre »")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--depuis")
    ap.add_argument("--fichier", nargs="*", default=[])
    ap.add_argument("--tous", action="store_true")
    ap.add_argument("--racine", default="resultats")
    ap.add_argument("--etat", action="store_true")
    ap.add_argument("--exiger-ots", action="store_true",
                    help="echouer si le binaire ots est absent")
    ap.add_argument("--verifier", action="store_true",
                    help="lancer aussi `ots verify` (exige ots + reseau)")
    ap.add_argument("--mode", choices=("bloquant", "avertissement"), default="bloquant")
    a = ap.parse_args(argv)

    binaire = ots_dispo()
    if a.etat:
        if binaire:
            print(f"[{NOM}] ots present : {binaire} — controle (b) disponible.")
            return 0
        print(f"[{NOM}] ots ABSENT — controle (b) NON OPERATIONNEL. "
              f"Installation : {INSTALLATION}")
        return 0

    constat = Constat(NOM, a.mode)
    if binaire is None:
        msg = (f"binaire `ots` absent : le controle (b) verification cryptographique est "
               f"NON OPERATIONNEL. Installation : {INSTALLATION}. Seule la presence du "
               f"recu est controlee.")
        if a.exiger_ots:
            return abandon(NOM, msg)
        constat.note(msg)
    elif a.verifier:
        constat.note(f"ots present ({binaire}) ; `ots verify` exige un acces reseau a un "
                     f"calendrier — hors mandat local, a ne lancer qu'explicitement")
    else:
        constat.note(f"ots present ({binaire}) mais --verifier non demande sur cet appel : "
                     f"le controle (b) VERIFICATION CRYPTOGRAPHIQUE est NON OPERATIONNEL "
                     f"pour cette invocation (seule la presence du recu est controlee)")

    if a.tous:
        if not git_dispo():
            return abandon(NOM, "git indisponible")
        suivis = git("ls-files", f"{a.racine}/{MOTIF}").splitlines()
        cibles = [RACINE / f for f in suivis if f.strip()]
    else:
        cibles = resout_cibles(a.fichier, a.depuis, MOTIF, a.racine)

    manquants = 0
    for c in cibles:
        recu = controle_presence(constat, c)
        if recu is None:
            manquants += 1
        elif a.verifier and binaire:
            controle_verification(constat, c, recu, binaire)

    constat.note(f"{len(cibles)} preenregistrement(s) controle(s), "
                 f"{manquants} sans recu .ots")
    return constat.conclure()


if __name__ == "__main__":
    raise SystemExit(main())
