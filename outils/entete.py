#!/usr/bin/env python3
"""Poser ou verifier l'en-tete du gabarit A2 (`gabarits/entete.md`) sur un fichier.

Pourquoi cet outil existe : la porte P4 (`outils/portes/entetes.py`) exige que
tout fichier de `resultats/` porte cet en-tete, et cinq agents d'affilee l'ont
oublie le 12/09 — chaque oubli a bloque une fusion, provoque un aller-retour,
et coute un agent de correction rien que pour reparer ca. Ce n'est pas un
probleme de discipline : poser l'en-tete a la main est un geste manuel, facile
a oublier, et rien ne le rendait evident. La regle du projet est que « les
regles nommees et outillees tiennent, les intentions cedent » : cet outil
outille le geste, il ne se contente pas de le rappeler.

Deux commandes, aucune ne devine de valeur a la place de l'agent :

    entete.py --poser <fichier> --mandat "..." --agent "..." --ecriture "..." \\
              --cout-reel-usd 0.00 [--statut courant] [--lecture-seule "..."] \\
              [--interdits "..."] [--cecite "..."] [--fait-foi <fichier>]

    entete.py --verifier <fichier>

`--poser` insere l'en-tete juste sous le titre (premiere ligne `# ...`), sans
toucher au reste du contenu. Il REFUSE de s'executer si le fichier porte deja
un en-tete (une ligne `statut:` dans les 30 premieres lignes) : il ne duplique
jamais, et ne remplace jamais silencieusement. Les champs sans defaut sur, cas
par cas (mandat, agent, ecriture, cout_reel_usd) sont obligatoires : l'outil
echoue bruyamment si l'un manque plutot que d'inventer une valeur — en
particulier `cout_reel_usd`, qui doit venir du grand livre, jamais d'un defaut
silencieux a 0.00 impose par l'outil lui-meme.

`--verifier` dit si l'en-tete est present et complet, sans jamais rien
modifier.

Codes de sortie (convention du projet, cf. `outils/portes/commun.py`) :
  0 : succes (en-tete pose, ou verification complete)
  1 : refus / echec de regle (en-tete deja present, champ manquant, en-tete
      absent ou incomplet a la verification)
  2 : impossible de s'executer (fichier introuvable, pas de titre a l'endroit
      attendu)
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FENETRE_ENTETE = 30  # meme fenetre que la porte P4 (outils/portes/entetes.py)

CLES_A2 = ("mandat", "agent", "ecriture", "lecture_seule", "interdits", "cout_reel_usd")

DEFAUT_LECTURE_SEULE = "tout le reste"
DEFAUT_INTERDITS = "appel payant sans GO, reseau, commit sur master, arriere-plan"
DEFAUT_STATUT = "courant"

RE_CLE = {cle: re.compile(rf"^\s*{cle}\s*:", re.I) for cle in CLES_A2}
RE_STATUT = re.compile(r"^\s*statut\s*:\s*(.+?)\s*$", re.I)
RE_FAIT_FOI = re.compile(r"^\s*fait_foi\s*:", re.I)


def echec(motif: str) -> int:
    print(f"[entete] ECHEC : {motif}", file=sys.stderr)
    return 1


def impossible(motif: str) -> int:
    print(f"[entete] IMPOSSIBLE D'EXECUTER : {motif}", file=sys.stderr)
    return 2


# --------------------------------------------------------------------------- #
# Lecture / detection                                                          #
# --------------------------------------------------------------------------- #

def fenetre(chemin: Path) -> list[str]:
    return chemin.read_text(encoding="utf-8", errors="replace").splitlines()[:FENETRE_ENTETE]


def entete_deja_present(lignes_src: list[str]) -> int | None:
    """Numero de ligne (1-based) de la premiere ligne « statut: », ou None."""
    for i, l in enumerate(lignes_src, start=1):
        if RE_STATUT.match(l):
            return i
    return None


def cles_manquantes(lignes_src: list[str]) -> list[str]:
    return [cle for cle in CLES_A2 if not any(RE_CLE[cle].match(l) for l in lignes_src)]


def statut_retracte(lignes_src: list[str]) -> bool:
    for l in lignes_src:
        m = RE_STATUT.match(l)
        if m:
            return m.group(1).strip().lower().startswith(("retracte", "retracte_par", "perime_par"))
    return False


def a_fait_foi(lignes_src: list[str]) -> bool:
    return any(RE_FAIT_FOI.match(l) for l in lignes_src)


# --------------------------------------------------------------------------- #
# --verifier                                                                   #
# --------------------------------------------------------------------------- #

def verifier(fichier: Path) -> int:
    if not fichier.exists():
        return impossible(f"fichier introuvable : {fichier}")

    lignes_src = fenetre(fichier)
    ligne_statut = entete_deja_present(lignes_src)
    if ligne_statut is None:
        return echec(
            f"{fichier} : aucun en-tete (pas de ligne « statut: » dans les "
            f"{FENETRE_ENTETE} premieres lignes). Poser avec : "
            f"outils/entete.py --poser {fichier} --mandat ... --agent ... "
            f"--ecriture ... --cout-reel-usd ..."
        )

    manquantes = cles_manquantes(lignes_src)
    if statut_retracte(lignes_src) and not a_fait_foi(lignes_src):
        manquantes = manquantes + ["fait_foi (obligatoire, statut retracte/perime)"]

    if manquantes:
        print(f"[entete] {fichier} : en-tete present (ligne {ligne_statut}) mais incomplet.")
        for cle in manquantes:
            print(f"[entete]   cle manquante : {cle}")
        return 1

    print(f"[entete] {fichier} : en-tete present (ligne {ligne_statut}) et complet.")
    return 0


# --------------------------------------------------------------------------- #
# --poser                                                                      #
# --------------------------------------------------------------------------- #

def construit_bloc(a: argparse.Namespace) -> list[str]:
    bloc = [f"statut: {a.statut}"]
    if a.fait_foi:
        bloc.append(f"fait_foi: {a.fait_foi}")
    bloc += [
        f"mandat: {a.mandat}",
        f"agent: {a.agent}",
        f"ecriture: {a.ecriture}",
        f"lecture_seule: {a.lecture_seule}",
        f"interdits: {a.interdits}",
    ]
    if a.cecite:
        bloc.append(f"cecite: {a.cecite}")
    bloc.append(f"cout_reel_usd: {a.cout_reel_usd}")
    return bloc


def poser(fichier: Path, a: argparse.Namespace) -> int:
    if not fichier.exists():
        return impossible(f"fichier introuvable : {fichier}")

    # --- champs obligatoires, aucune valeur inventee a la place -------------
    obligatoires = {
        "--mandat": a.mandat,
        "--agent": a.agent,
        "--ecriture": a.ecriture,
        "--cout-reel-usd": a.cout_reel_usd,
    }
    manquants = [nom for nom, val in obligatoires.items() if val is None or not val.strip()]
    if manquants:
        return echec(
            f"champ(s) obligatoire(s) manquant(s) pour poser l'en-tete sur {fichier} : "
            f"{', '.join(manquants)}. Aucune valeur par defaut ne sera inventee — "
            f"les fournir explicitement (gabarit A2, gabarits/entete.md)."
        )

    if a.statut.lower().startswith(("retracte", "retracte_par", "perime_par")) and not a.fait_foi:
        return echec(
            f"statut « {a.statut} » declare une retractation/peremption mais "
            f"--fait-foi (cle « fait_foi: ») est absent : nommer le document qui fait "
            f"foi a la place (v1 §2.7)."
        )

    texte_brut = fichier.read_text(encoding="utf-8", errors="replace")
    lignes_src = texte_brut.splitlines()

    # --- refus de dupliquer ---------------------------------------------------
    ligne_existante = entete_deja_present(lignes_src[:FENETRE_ENTETE])
    if ligne_existante is not None:
        return echec(
            f"{fichier} porte deja un en-tete (ligne « statut: » a la ligne "
            f"{ligne_existante}) — refus de le dupliquer. Verifier avec "
            f"--verifier, ou editer l'en-tete existant a la main s'il doit changer."
        )

    if not lignes_src:
        return impossible(f"{fichier} est vide : pas de titre sous lequel poser l'en-tete.")
    if not lignes_src[0].lstrip().startswith("#"):
        return impossible(
            f"{fichier} : la premiere ligne n'est pas un titre Markdown (« # ... »). "
            f"L'en-tete se pose sous le titre ; impossible de deviner ou l'inserer sans un titre."
        )

    bloc = construit_bloc(a)

    reste = lignes_src[1:]
    while reste and not reste[0].strip():
        reste = reste[1:]

    nouvelles_lignes = [lignes_src[0], "", *bloc, "", *reste]
    fichier.write_text("\n".join(nouvelles_lignes) + "\n", encoding="utf-8")

    print(f"[entete] {fichier} : en-tete pose (sous le titre, {len(bloc)} lignes).")
    for l in bloc:
        print(f"[entete]   {l}")
    return 0


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #

def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--poser", metavar="FICHIER", help="poser l'en-tete A2 sur ce fichier")
    mode.add_argument("--verifier", metavar="FICHIER",
                      help="dire si l'en-tete est present et complet, sans rien modifier")

    ap.add_argument("--statut", default=DEFAUT_STATUT)
    ap.add_argument("--mandat")
    ap.add_argument("--agent")
    ap.add_argument("--ecriture")
    ap.add_argument("--lecture-seule", dest="lecture_seule", default=DEFAUT_LECTURE_SEULE)
    ap.add_argument("--interdits", default=DEFAUT_INTERDITS)
    ap.add_argument("--cecite")
    ap.add_argument("--fait-foi", dest="fait_foi")
    ap.add_argument("--cout-reel-usd", dest="cout_reel_usd")

    a = ap.parse_args(argv)

    if a.verifier:
        return verifier(Path(a.verifier))
    return poser(Path(a.poser), a)


if __name__ == "__main__":
    raise SystemExit(main())
