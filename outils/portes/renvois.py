#!/usr/bin/env python3
"""P5 — Methode v2 §1.2 : tout renvoi `§N.M` vers un fichier du depot existe.

Fondement : v1 §2.4, trois renvois faux sur soixante. Un renvoi faux coute au
lecteur exactement ce que coute un chiffre faux, et il est silencieux.

Ce que la porte resout : un renvoi de la forme
    `fichier.md` §3.2      |     fichier.md, §3.2     |     manuscrit §7.1
c'est-a-dire un nom de fichier (ou un alias declare) suivi, dans la meme phrase,
d'un ou plusieurs `§N`, `§N.M`, `§N.M.K`.

Cible : le fichier doit porter un titre markdown dont la numerotation commence par
N.M. Sont acceptes « ## 3.2 … », « ### 3.2. … », « ## 3 bis … » pour `§3 bis`.

Ce que la porte NE resout PAS, et le dit : un `§N.M` sans fichier nomme dans la
meme phrase est un renvoi interne ; il est verifie contre le fichier courant
seulement si `--internes` est passe, parce que beaucoup de rapports renvoient au
manuscrit par defaut sans le nommer, et qu'un controle qui devine est un controle
qui accuse a tort (contribution propre de l'audit, v2 §6).

Usage :
    renvois.py --fichier resultats/article-synthese.md
    renvois.py --depuis origin/master
    renvois.py --tous resultats
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import RACINE, Constat, lignes, masque_code, normalise, resout_cibles  # noqa: E402

NOM = "P5 renvois"

ALIAS = {
    "manuscrit": "article/manuscrit.md",
    "synthese": "resultats/article-synthese.md",
    "article-synthese": "resultats/article-synthese.md",
    "methode": "METHODE.md",
    "v1": "METHODE.md",
    "autopsie": "resultats/autopsie-methode-2026-09-12.md",
}

RE_FICHIER = re.compile(r"`([\w./-]+\.md)`|\b([\w-]+\.md)\b")
RE_ALIAS = re.compile(r"\b(" + "|".join(ALIAS) + r")\b", re.I)
RE_SECTION = re.compile(r"§\s*(\d+(?:\.\d+)*)(\s*bis)?")
RE_TITRE = re.compile(r"^#{1,6}\s+(\d+(?:\.\d+)*)(\s*bis)?\b")

_cache: dict[str, set[str] | None] = {}


def sections_de(chemin: Path) -> set[str] | None:
    cle = str(chemin)
    if cle in _cache:
        return _cache[cle]
    if not chemin.exists():
        _cache[cle] = None
        return None
    secs: set[str] = set()
    src = lignes(chemin)
    code = masque_code(src)
    for i, l in enumerate(src):
        if code[i]:
            continue
        m = RE_TITRE.match(normalise(l).replace("#", "# ").replace("#  ", "# ")) \
            or RE_TITRE.match(l.strip())
        if m:
            base = m.group(1)
            secs.add(base + (" bis" if m.group(2) else ""))
            secs.add(base)
            # un renvoi §2.1 est valide si le fichier n'a qu'un titre « ## 2.1.3 »
            parts = base.split(".")
            for k in range(1, len(parts)):
                secs.add(".".join(parts[:k]))
    _cache[cle] = secs
    return secs


def resout_cible_fichier(phrase: str, courant: Path) -> tuple[Path, str] | None:
    m = RE_FICHIER.search(phrase)
    if m:
        nom = m.group(1) or m.group(2)
        if "/" in nom:
            for racine in (courant.parent, RACINE):
                p = racine / nom
                if p.exists():
                    return p, nom
            return None
        # Un nom nu est cherche d'abord a cote du fichier qui le cite, puis dans
        # les repertoires ou le depot range ses documents.
        for racine in (courant.parent, RACINE):
            for base in ("", "resultats/", "article/", "analyses/", "protocoles/"):
                p = racine / (base + nom)
                if p.exists():
                    return p, nom
        return None
    m = RE_ALIAS.search(phrase)
    if m:
        p = RACINE / ALIAS[m.group(1).lower()]
        if p.exists():
            return p, m.group(1)
    return None


def controle(constat: Constat, chemin: Path, internes: bool) -> int:
    src = lignes(chemin)
    code = masque_code(src)
    verifies = 0
    for i, brute in enumerate(src, start=1):
        if code[i - 1] or "§" not in brute:
            continue
        for phrase in re.split(r"(?<=[.;])\s+|\s*\|\s*", brute):
            renvois = list(RE_SECTION.finditer(phrase))
            if not renvois:
                continue
            cible = resout_cible_fichier(phrase, chemin)
            if cible is None:
                if not internes:
                    continue
                cible = (chemin, chemin.name)
            fichier, nom = cible
            secs = sections_de(fichier)
            if secs is None:
                continue
            for r in renvois:
                ref = r.group(1) + (" bis" if r.group(2) else "")
                verifies += 1
                if ref not in secs and r.group(1) not in secs:
                    constat.viole(
                        chemin, i,
                        f"renvoi « §{ref} » vers {nom} : ce fichier n'a aucune "
                        f"section {ref}",
                        f"corriger le numero, ou corriger le titre dans {nom} "
                        f"(v1 §2.4 : 3 renvois faux sur 60)",
                    )
    return verifies


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fichier", nargs="*", default=[])
    ap.add_argument("--depuis")
    ap.add_argument("--tous", nargs="?", const="resultats")
    ap.add_argument("--internes", action="store_true")
    ap.add_argument("--mode", choices=("bloquant", "avertissement"), default="bloquant")
    a = ap.parse_args(argv)

    constat = Constat(NOM, a.mode)
    if a.tous:
        cibles = sorted((RACINE / a.tous).glob("*.md"))
    else:
        cibles = resout_cibles(a.fichier, a.depuis, "*.md", "resultats")

    total = 0
    for c in cibles:
        if c.exists():
            total += controle(constat, c, a.internes)
    constat.note(f"{len(cibles)} fichier(s) lus, {total} renvoi(s) §N.M resolus vers un "
                 f"fichier nomme")
    return constat.conclure()


if __name__ == "__main__":
    raise SystemExit(main())
