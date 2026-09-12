#!/usr/bin/env python3
"""P3 — Methode v2 §1.2 : aucune formulation INTERDITE ne sort du depot.

`resultats/article-synthese.md` est la source unique de verite editoriale. Elle porte
32 occurrences de `INTERDIT :` (v1 §2.6), chacune enumerant des formulations proscrites.
La v1 conclut : « la liste des 32 interdits est grep-able, donc a un script d'une heure
de devenir opposable. Ce script n'est pas ecrit. » Ce fichier est ce script.

Extraction : dans chaque segment ouvert par `INTERDIT`, on retient les fragments entre
guillemets francais « … » ou droits " … ". Ce sont les seules formulations que la
synthese donne verbatim ; le reste des interdits est de la prose (« toute formulation
causale ») qu'aucun grep ne peut opposer — c'est dit franchement plutot que simule.

Comparaison : sur texte normalise (minuscules, sans accents, apostrophes et tirets
unifies, gras/italique retires, espaces tasses), pour qu'une recopie retypographiee
soit quand meme attrapee.

Exemptions : `outils/portes/interdits-exemptions.txt`, une formulation par ligne,
motif obligatoire apres ` # `. Sert au cas legitime ou le manuscrit CITE un interdit
pour le refuter. Une exemption est un aveu ecrit, pas un contournement silencieux.

Usage :
    interdits.py                                    # manuscrit + lettres, par defaut
    interdits.py --fichier article/manuscrit.md
    interdits.py --lister                           # affiche les formulations extraites
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from commun import RACINE, Constat, abandon, lignes, normalise  # noqa: E402

NOM = "P3 interdits"
SYNTHESE = RACINE / "resultats" / "article-synthese.md"
EXEMPTIONS = Path(__file__).resolve().parent / "interdits-exemptions.txt"

CIBLES_DEFAUT = [
    "article/manuscrit.md",
    "resultats/divulgation-responsable-brouillon.md",
    "resultats/ethique-section-brouillon.md",
]

RE_GUILLEMETS = re.compile(r"«\s*(.+?)\s*»|“\s*(.+?)\s*”")
RE_INTERDIT = re.compile(r"INTERDIT[^:]{0,40}:", re.I)
# Un segment INTERDIT s'arrete des qu'une formulation AUTORISEE reprend la main :
# sans cette coupure, la porte bannirait la phrase de remplacement qu'elle exige.
RE_FIN_SEGMENT = re.compile(r"autoris", re.I)

MOTS_MIN = 3
CARS_MIN = 15


def _paragraphes(src: list[str]) -> list[tuple[int, str]]:
    """[(ligne de debut, paragraphe joint)] — un INTERDIT peut courir sur 2 lignes."""
    out, debut, tampon = [], 0, []
    for i, l in enumerate(src, start=1):
        if l.strip():
            if not tampon:
                debut = i
            tampon.append(l.strip())
        elif tampon:
            out.append((debut, " ".join(tampon)))
            tampon = []
    if tampon:
        out.append((debut, " ".join(tampon)))
    return out


def pointe_la_ligne(src: list[str], debut: int, norm: str) -> int:
    """Ligne exacte ou commence la formulation, dans le paragraphe qui debute a `debut`.

    La comparaison se fait sur paragraphe joint ; sans ce recalage, le message
    nommerait la premiere ligne du paragraphe et enverrait le lecteur au mauvais
    endroit — un renvoi faux produit par la porte elle-meme.
    """
    tete = " ".join(norm.split()[:4])
    i = debut - 1
    while i < len(src) and src[i].strip():
        courant = normalise(src[i])
        joint = normalise(" ".join(x.strip() for x in src[i:i + 2]))
        if tete in courant or tete in joint or norm in joint:
            return i + 1
        i += 1
    return debut


def extrait_interdits(chemin: Path) -> list[tuple[int, str, str]]:
    """[(ligne_source, formulation_brute, formulation_normalisee)]"""
    out: list[tuple[int, str, str]] = []
    vus: set[str] = set()
    for debut, para in _paragraphes(lignes(chemin)):
        for m_int in RE_INTERDIT.finditer(para):
            segment = para[m_int.end():]
            fin = RE_FIN_SEGMENT.search(segment)
            if fin:
                segment = segment[:fin.start()]
            suivant = RE_INTERDIT.search(segment)
            if suivant:
                segment = segment[:suivant.start()]
            for m in RE_GUILLEMETS.finditer(segment):
                brut = (m.group(1) or m.group(2) or "").strip()
                norm = normalise(brut)
                if len(norm) < CARS_MIN or len(norm.split()) < MOTS_MIN:
                    continue
                if norm in vus:
                    continue
                vus.add(norm)
                out.append((debut, brut, norm))
    return out


def charge_exemptions() -> set[str]:
    if not EXEMPTIONS.exists():
        return set()
    ex = set()
    for l in lignes(EXEMPTIONS):
        l = l.strip()
        if not l or l.startswith("#"):
            continue
        formulation = l.split(" # ")[0]
        ex.add(normalise(formulation))
    return ex


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--fichier", nargs="*", default=[])
    ap.add_argument("--synthese", default=str(SYNTHESE))
    ap.add_argument("--lister", action="store_true")
    ap.add_argument("--mode", choices=("bloquant", "avertissement"), default="bloquant")
    a = ap.parse_args(argv)

    constat = Constat(NOM, a.mode)
    synthese = Path(a.synthese)
    if not synthese.is_absolute():
        synthese = RACINE / synthese
    if not synthese.exists():
        return abandon(NOM, f"source de verite absente : {synthese}")

    interdits = extrait_interdits(synthese)
    exemptions = charge_exemptions()
    if a.lister:
        for src, brut, _ in interdits:
            print(f"{synthese.name}:{src}: « {brut} »")
        print(f"[{NOM}] {len(interdits)} formulation(s) verbatim extraite(s).")
        return 0

    if not interdits:
        return abandon(NOM, "aucune formulation interdite extraite : la porte ne refuserait "
                            "jamais rien, ce qui est exactement le defaut que la v1 reproche")

    cibles = [Path(f) if Path(f).is_absolute() else RACINE / f
              for f in (a.fichier or CIBLES_DEFAUT)]
    cibles = [c for c in cibles if c.exists()]

    for cible in cibles:
        # Comparaison par paragraphe : une formulation coupee en fin de ligne doit
        # etre attrapee comme si elle tenait sur une ligne.
        src_cible = lignes(cible)
        for i, para in _paragraphes(src_cible):
            norm_ligne = normalise(para)
            if not norm_ligne:
                continue
            for src, brut, norm in interdits:
                if norm in norm_ligne and norm not in exemptions:
                    constat.viole(
                        cible, pointe_la_ligne(src_cible, i, norm),
                        f"formulation INTERDITE par {synthese.name}:{src} — « {brut} »",
                        "employer la formulation autorisee de la meme entree de "
                        "article-synthese.md, ou inscrire une exemption motivee dans "
                        "outils/portes/interdits-exemptions.txt",
                    )

    constat.note(f"{len(interdits)} formulation(s) interdite(s) verbatim extraite(s) de "
                 f"{synthese.name} ; {len(cibles)} fichier(s) de sortie controle(s) ; "
                 f"{len(exemptions)} exemption(s) declaree(s)")
    return constat.conclure()


if __name__ == "__main__":
    raise SystemExit(main())
