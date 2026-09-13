#!/usr/bin/env python3
"""P4 — Methode v2 §1.2 et §1.4 : en-tete de statut, et retractation dans le meme commit.

Deux controles :

  (a) EN-TETE — tout fichier de `resultats/` porte l'en-tete du gabarit A2 :
      `statut:` valide, `mandat:`, `agent:`, `ecriture:`, `lecture_seule:`,
      `interdits:`, `cout_reel_usd:` ; et si `statut: retracte` ou `retracte_par:`,
      alors `fait_foi:` est obligatoire. Fondement : v1 §2.7, v2 §1.4.

  (b) RETRACTATION DANS LE MEME COMMIT — un commit qui pose, dans un fichier de
      `resultats/`, le MARQUEUR canonique de retractation nommant un fichier de
      `resultats/`, doit poser l'en-tete de retractation dans ce fichier-la, dans le
      MEME commit. Fondement : G3.1 de la v1, « absente » au 12/09 ; v2 §2, « un commit
      qui declare un rapport invalide sans modifier l'en-tete de l'audite echoue ».
      C'est le controle qui ferme les 6 minutes pendant lesquelles des rapports faux
      etaient publics sur GitHub (v1 §2.7).

      La porte NE DEVINE PLUS l'invalidation dans la prose. Elle l'a fait jusqu'au
      12/09/2026 — un mot d'invalidation et un nom de fichier a proximite — et a
      produit quatre faux positifs en une journee : un renvoi §N attribue au mauvais
      fichier, un identifiant de registre CSV pris pour une declaration, un mot et un
      nom de fichier distants de 360 caracteres dans un meme paragraphe, et la phrase
      « ils ne sont pas invalides », lue comme une invalidation faute de savoir lire
      une negation. Le raffinement du vocabulaire ne pouvait pas fermer cette classe
      d'erreurs : tout document qui PARLE de retractation la declenchait. L'inference
      est donc remplacee par une declaration explicite (voir MARQUEUR ci-dessous).

PERIMETRE PAR DEFAUT : le diff (`--depuis`) ou des fichiers explicites. `--tous`
existe et mesure la dette : au 12/09, aucun des 321 rapports de resultats/ ne porte
d'en-tete A2. Rendre (a) bloquant sur tout l'arbre aujourd'hui fermerait le depot ;
il est bloquant sur les fichiers NOUVEAUX ou MODIFIES, ce qui est opposable sans
etre ingerable.

MARQUEUR — une retractation se DECLARE, elle ne se devine pas. Dans le rapport qui
invalide, une ligne entiere, a la colonne 0, exactement de cette forme :

    RETRACTE: resultats/<fichier>.md
    INVALIDE: resultats/<fichier>.md      (synonyme strict, meme effet)

Rien d'autre sur la ligne, un seul fichier par ligne, mot-cle en capitales, chemin
complet depuis la racine du depot. Aucune phrase francaise ne peut prendre cette
forme : c'est ce qui rend le faux positif impossible depuis la prose. Pour CITER le
marqueur sans le declencher — documentation, rapport qui parle de retractations —
il suffit de l'indenter ou de l'encadrer de backticks : la ligne ne commence alors
plus par le mot-cle. Un marqueur mal forme, ou nommant un fichier inexistant, fait
echouer la porte : une faute de frappe ne doit pas desarmer la regle en silence.

CE QUE CE DISPOSITIF NE PEUT PLUS ATTRAPER, et c'est assume : une invalidation
ecrite en prose SANS marqueur passe sans un mot. La regle n'est opposable qu'a qui
pose le marqueur. On echange une detection large et bruyante (4 faux positifs en une
journee, 4 PR bloquees a tort) contre une detection etroite et fiable. Le filet large
reste disponible, mais jamais bloquant : `--indice-prose` le rejoue en simples notes,
a l'usage d'un relecteur humain.

Usage :
    entetes.py --depuis origin/master
    entetes.py --fichier resultats/x-resultats.md
    entetes.py --tous --mode avertissement      # mesure de la dette
    entetes.py --retractation --depuis origin/master   # controle (b)
    entetes.py --retractation --depuis origin/master --indice-prose  # + notes
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
# Les deux etats intermediaires du §0 de marqueurs-canoniques-2026-09-13.md.
# Comme la retractation, ils exigent « fait_foi: » : un rapport amende ou borne
# doit dire quel document fait foi a sa place, sinon l'amendement n'est opposable
# a personne. Declaratif : la cle est lue, aucune prose n'est interpretee.
RE_AMENDE_BORNE = re.compile(r"^(amende_par|borne_par)\s*:\s*(\S+)", re.I)
RE_FAIT_FOI = re.compile(r"^fait_foi\s*:\s*(\S+)", re.I)
FENETRE_ENTETE = 30

# Le marqueur canonique : ligne entiere, colonne 0, mot-cle en capitales.
# La porte ne reconnait que cela. La prose ne la declenche plus jamais.
#
# TROIS ETATS, un marqueur chacun (recommandation (a) de
# resultats/marqueurs-canoniques-2026-09-13.md §6.2) :
#   RETRACTE:/INVALIDE:  l'affirmation est FAUSSE      -> retracte_par: / perime_par:
#   AMENDE:              la formulation change, le fait TIENT -> amende_par:
#   BORNE:               le fait tient dans un perimetre PLUS ETROIT -> borne_par:
# AMENDE: et BORNE: sont calques sur RETRACTE: a l'identique : meme forme de
# ligne, meme exigence de commit unique, meme refus du marqueur mal forme. Seule
# la cle d'en-tete exigee dans le fichier vise change. Aucune prose n'est lue,
# donc le faux positif reste impossible — au 13/09, ZERO ligne du depot commence
# par AMENDE: ou BORNE: : l'extension n'ajoute pas un signalement.
RE_MARQUEUR = re.compile(r"^(RETRACTE|INVALIDE|AMENDE|BORNE)\s*:(.*)$")
RE_CIBLE = re.compile(r"^resultats/[A-Za-z0-9._@+-]+\.md$")
# Ce qui, ajoute dans le fichier vise, vaut pose de l'etat — par marqueur.
RE_POSE = re.compile(r"^(statut\s*:\s*(retracte|perime)|retracte_par\s*:|perime_par\s*:)")
RE_POSE_AMENDE = re.compile(r"^amende_par\s*:")
RE_POSE_BORNE = re.compile(r"^borne_par\s*:")

# marqueur -> (regex de pose, cle a ecrire, adjectif, nom de l'etat, verbe)
_RETRACTE = (RE_POSE, "« retracte_par: <fichier> » (ou « perime_par: »)",
             "invalide", "retractation", "retracte")
ETATS = {
    "RETRACTE": _RETRACTE,
    "INVALIDE": _RETRACTE,
    "AMENDE": (RE_POSE_AMENDE, "« amende_par: <fichier> »",
               "amende", "amendement", "amende"),
    "BORNE": (RE_POSE_BORNE, "« borne_par: <fichier> »",
              "borne", "bornage", "borne"),
}

# Filet large de l'ancienne porte : conserve UNIQUEMENT pour --indice-prose,
# en notes non bloquantes. Ne rend jamais de verdict (4 faux positifs le 12/09).
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
    amende = None
    ligne_amende = 0
    fait_foi = False
    for i, l in enumerate(src, start=1):
        n = norm[i - 1]
        m = RE_STATUT.match(n)
        if m and statut is None:
            statut, ligne_statut = m.group(1).strip(), i
        m = RE_PERIME.match(n)
        if m:
            perime = m.group(1)
        m = RE_AMENDE_BORNE.match(n)
        if m and amende is None:
            amende, ligne_amende = m.group(1), i
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

    if amende and not fait_foi:
        constat.viole(chemin, ligne_amende,
                      f"rapport porteur de « {amende}: » sans ligne « fait_foi: »",
                      "nommer le document qui fait foi pour l'affirmation amendee ou "
                      "bornee : un amendement qui ne dit pas ou lire la version qui "
                      "tient n'est opposable a personne (gabarits/entete.md)")

    for cle in CLES_A2:
        if not any(n.startswith(cle + ":") for n in norm):
            constat.viole(chemin, 1, f"cle d'en-tete « {cle}: » absente",
                          f"ajouter « {cle}: … » (gabarit A2). Le perimetre d'ecriture "
                          f"declare est compare a git show --stat a chaque PR (v2 §1.4)")


def ajouts_du_commit(sha: str) -> dict[str, list[tuple[int, str]]]:
    """{chemin: [(no_ligne, texte)]} — les lignes AJOUTEES par un commit."""
    diff = git("show", "--format=", "-U0", "-m", "--first-parent", sha)
    out: dict[str, list[tuple[int, str]]] = {}
    fichier, no = "", 0
    for l in diff.splitlines():
        if l.startswith("+++"):
            # « +++ b/chemin » : on suit le fichier d'ou vient chaque ligne ajoutee.
            fichier = l[6:].strip() if l.startswith("+++ b/") else ""
        elif l.startswith("@@"):
            m = re.match(r"^@@+ .*?\+(\d+)", l)
            no = int(m.group(1)) if m else 0
        elif l.startswith("+") and fichier:
            out.setdefault(fichier, []).append((no, l[1:]))
            no += 1
    return out


def existe_au_commit(sha: str, chemin: str) -> bool:
    try:
        git("cat-file", "-e", f"{sha}:{chemin}")
        return True
    except RuntimeError:
        return False


def controle_retractation(constat: Constat, depuis: str, jusqu_a: str,
                          indice_prose: bool = False) -> None:
    for sha in commits(depuis, jusqu_a):
        touches = {c for _, c in fichiers_du_commit(sha)}
        if not any(c.startswith("resultats/") for c in touches):
            continue
        ajouts = ajouts_du_commit(sha)
        for source in sorted(ajouts):
            # Le marqueur se pose dans un RAPPORT : un .md de resultats/. Nulle part
            # ailleurs — ce qui met la documentation du marqueur hors d'atteinte.
            if not (source.startswith("resultats/") and source.endswith(".md")):
                continue
            for no, texte in ajouts[source]:
                m = RE_MARQUEUR.match(texte.rstrip())
                if not m:
                    continue
                mot, cible = m.group(1), m.group(2).strip()

                # Un marqueur mal ecrit n'est jamais ignore en silence : sans cela,
                # une faute de frappe desarmerait la regle sans que personne le sache.
                if not RE_CIBLE.match(cible):
                    constat.viole(
                        source, no,
                        f"marqueur « {mot}: » mal forme (« {cible[:60]} »)",
                        f"ecrire exactement « {mot}: resultats/<fichier>.md » : un seul "
                        "fichier, chemin complet, rien d'autre sur la ligne "
                        "(gabarits/entete.md). Pour citer le marqueur sans le declencher, "
                        "l'indenter ou l'encadrer de backticks")
                    continue

                if not existe_au_commit(sha, cible):
                    constat.viole(
                        source, no,
                        f"le marqueur « {mot}: {cible} » nomme un fichier introuvable "
                        f"au commit {sha[:8]}",
                        "corriger le chemin : une retractation qui vise un fichier "
                        "inexistant ne retracte rien")
                    continue

                re_pose, cle, adjectif, nom_etat, verbe = ETATS[mot]

                if cible not in touches:
                    constat.viole(
                        cible, 1,
                        f"le commit {sha[:8]} declare ce rapport {adjectif} "
                        f"(« {mot}: » dans {source}) sans toucher au fichier lui-meme",
                        f"poser {cle} et « fait_foi: <fichier> » DANS LE MEME COMMIT "
                        f"que le marqueur (G3.1 de la v1 ; v2 §2, retractation sans "
                        f"effacement)")
                    continue

                if not any(re_pose.match(normalise(t)) for _, t in ajouts.get(cible, [])):
                    constat.viole(
                        cible, 1,
                        f"le commit {sha[:8]} declare ce rapport {adjectif} "
                        f"(« {mot}: » dans {source}) et le touche, mais sans y poser "
                        f"l'en-tete de {nom_etat}",
                        f"ajouter {cle} et « fait_foi: <fichier> » dans l'en-tete du "
                        f"rapport vise : toucher le fichier ne {verbe} rien (v1 §2.7)")

        if indice_prose:
            indices_de_prose(constat, sha, ajouts, touches)


def indices_de_prose(constat: Constat, sha: str, ajouts: dict[str, list[tuple[int, str]]],
                     touches: set[str]) -> None:
    """Le filet large d'avant le marqueur, en NOTES, jamais bloquant.

    Il a produit quatre faux positifs en une journee ; il ne peut donc plus rendre
    de verdict. Il reste utile a un relecteur humain qui veut savoir si un commit
    a l'air d'invalider un rapport sans avoir pose le marqueur — c'est le seul
    rattrapage possible du faux negatif que le marqueur laisse passer.
    """
    for source in sorted(ajouts):
        if not (source.startswith("resultats/") and source.endswith(".md")):
            continue
        for no, texte in ajouts[source]:
            if RE_MARQUEUR.match(texte.rstrip()):
                continue
            n = normalise(texte)
            if not any(mot in n for mot in MOTS_INVALIDATION):
                continue
            for m in RE_FICHIER_RESULTATS.finditer(texte):
                candidat = f"resultats/{m.group(1)}"
                if candidat in touches or not existe_au_commit(sha, candidat):
                    continue
                constat.note(
                    f"indice (NON bloquant, souvent faux) : {source}:{no} parle "
                    f"d'invalidation pres de {candidat}, qui n'est pas touche par "
                    f"{sha[:8]}. Si c'est une vraie retractation, poser le marqueur.")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--depuis")
    ap.add_argument("--jusqu-a", default="HEAD")
    ap.add_argument("--fichier", nargs="*", default=[])
    ap.add_argument("--tous", action="store_true")
    ap.add_argument("--retractation", action="store_true",
                    help="controle (b) seul, sur la plage de commits")
    ap.add_argument("--indice-prose", action="store_true",
                    help="ajoute les indices de prose en NOTES non bloquantes "
                         "(l'ancien filet large, a l'usage d'un relecteur humain)")
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
            controle_retractation(constat, a.depuis, a.jusqu_a, a.indice_prose)
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
