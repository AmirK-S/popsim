"""Fonctions partagees par les six portes de la Methode v2 (§1.2).

Aucune dependance hors bibliotheque standard. Aucun appel reseau, aucun appel paye.

Convention commune a toutes les portes :
  - code de sortie 0  : rien a signaler
  - code de sortie 1  : au moins une violation (la porte se ferme)
  - code de sortie 2  : la porte n'a pas pu s'executer (fichier absent, git indisponible).
    Un code 2 n'est PAS un succes : en CI il doit faire echouer le job au meme titre qu'un 1.

Chaque message de violation porte : <chemin>:<ligne>: <constat> -> <ce qu'il faut corriger>.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
from pathlib import Path

RACINE = Path(__file__).resolve().parents[2]


# --------------------------------------------------------------------------- #
# Sortie                                                                       #
# --------------------------------------------------------------------------- #

class Constat:
    """Accumule les violations et decide du code de sortie."""

    def __init__(self, nom_porte: str, mode: str = "bloquant") -> None:
        self.nom = nom_porte
        self.mode = mode  # "bloquant" | "avertissement"
        self.violations: list[str] = []
        self.notes: list[str] = []

    def viole(self, fichier, ligne: int, constat: str, correction: str) -> None:
        chemin = _relatif(fichier)
        self.violations.append(f"{chemin}:{ligne}: {constat} -> {correction}")

    def note(self, texte: str) -> None:
        self.notes.append(texte)

    def conclure(self, limite_affichage: int = 60) -> int:
        for n in self.notes:
            print(f"[{self.nom}] note : {n}")
        if not self.violations:
            print(f"[{self.nom}] OK — aucune violation.")
            return 0
        for v in self.violations[:limite_affichage]:
            print(f"[{self.nom}] {v}")
        reste = len(self.violations) - limite_affichage
        if reste > 0:
            print(f"[{self.nom}] … et {reste} autres violations non affichees.")
        if self.mode == "avertissement":
            print(
                f"[{self.nom}] AVERTISSEMENT : {len(self.violations)} violation(s). "
                f"Mode avertissement — la porte ne bloque pas (code 0)."
            )
            return 0
        print(f"[{self.nom}] ECHEC : {len(self.violations)} violation(s). La porte se ferme.")
        return 1


def abandon(nom_porte: str, motif: str) -> int:
    print(f"[{nom_porte}] IMPOSSIBLE D'EXECUTER : {motif}", file=sys.stderr)
    return 2


def _relatif(fichier) -> str:
    p = Path(fichier)
    try:
        return str(p.resolve().relative_to(RACINE))
    except ValueError:
        return str(p)


# --------------------------------------------------------------------------- #
# Texte                                                                        #
# --------------------------------------------------------------------------- #

def normalise(texte: str) -> str:
    """Minuscules, sans accents, apostrophes et guillemets unifies, espaces tasses.

    Sert a comparer une formulation interdite a un texte qui a pu etre recopie
    avec une autre typographie. Ne sert jamais a produire du texte.
    """
    texte = unicodedata.normalize("NFD", texte)
    texte = "".join(c for c in texte if unicodedata.category(c) != "Mn")
    texte = texte.lower()
    texte = texte.replace("’", "'").replace("‘", "'")
    texte = texte.replace("«", '"').replace("»", '"')
    texte = texte.replace("“", '"').replace("”", '"')
    texte = texte.replace("–", "-").replace("—", "-").replace("−", "-")
    texte = texte.replace(" ", " ").replace(" ", " ")
    # Le gras/italic markdown est retire, mais PAS le souligne : `lecture_seule`,
    # `commit_parent`, `cout_reel_usd` sont des cles d'en-tete dont l'underscore
    # fait partie du nom.
    texte = re.sub(r"\*+|`", "", texte)
    texte = re.sub(r"\s+", " ", texte)
    return texte.strip()


def lignes(chemin: Path) -> list[str]:
    return chemin.read_text(encoding="utf-8", errors="replace").splitlines()


_FENCE = re.compile(r"^\s*(```|~~~)")


def masque_code(lignes_src: list[str]) -> list[bool]:
    """True pour chaque ligne situee dans un bloc de code clos par ``` ou ~~~."""
    dedans = False
    out = []
    for l in lignes_src:
        if _FENCE.match(l):
            dedans = not dedans
            out.append(True)  # la ligne de cloture elle-meme est du code
            continue
        out.append(dedans)
    return out


_CODE_INLINE = re.compile(r"`[^`]*`")


def sans_code_inline(ligne: str) -> str:
    """Remplace le contenu des spans `...` par des espaces (positions conservees)."""
    return _CODE_INLINE.sub(lambda m: " " * len(m.group(0)), ligne)


# --------------------------------------------------------------------------- #
# Git                                                                          #
# --------------------------------------------------------------------------- #

def git(*args: str) -> str:
    res = subprocess.run(
        ["git", "-C", str(RACINE), *args],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} : {res.stderr.strip()}")
    return res.stdout


def git_dispo() -> bool:
    try:
        git("rev-parse", "--git-dir")
        return True
    except (RuntimeError, FileNotFoundError):
        return False


def commits(depuis: str, jusqu_a: str = "HEAD") -> list[str]:
    sortie = git("rev-list", "--reverse", f"{depuis}..{jusqu_a}")
    return [s for s in sortie.split() if s]


def fichiers_du_commit(sha: str) -> list[tuple[str, str]]:
    """[(statut, chemin)] pour un commit : A ajout, M modification, D suppression."""
    sortie = git("show", "--name-status", "--format=", "-m", "--first-parent", sha)
    out = []
    for l in sortie.splitlines():
        if not l.strip():
            continue
        parts = l.split("\t")
        if len(parts) >= 2:
            out.append((parts[0][0], parts[-1]))
    return out


def fichiers_modifies(depuis: str, jusqu_a: str = "HEAD") -> list[str]:
    sortie = git("diff", "--name-only", f"{depuis}...{jusqu_a}")
    return [s for s in sortie.splitlines() if s.strip()]


def dernier_commit_de(chemin: str) -> str | None:
    try:
        s = git("log", "-1", "--format=%h", "--", chemin).strip()
        return s or None
    except RuntimeError:
        return None


# --------------------------------------------------------------------------- #
# Selection de fichiers                                                        #
# --------------------------------------------------------------------------- #

def resout_cibles(args_fichiers: list[str], depuis: str | None, motif: str,
                  racine_defaut: str) -> list[Path]:
    """Trois modes de selection, dans cet ordre de priorite :

    1. des chemins explicites          (--fichier a.md b.md)
    2. le diff depuis une reference    (--depuis origin/master)
    3. tout l'arbre sous racine_defaut (--tous)
    """
    if args_fichiers:
        return [Path(f) if Path(f).is_absolute() else RACINE / f for f in args_fichiers]
    if depuis:
        cibles = []
        for f in fichiers_modifies(depuis):
            p = RACINE / f
            if p.exists() and p.match(motif):
                cibles.append(p)
        return cibles
    return sorted((RACINE / racine_defaut).glob(motif))
