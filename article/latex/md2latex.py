#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
md2latex.py -- convertisseur Markdown -> LaTeX pour le gabarit PoPETs 2027.

CE QUE FAIT CE SCRIPT
----------------------
Lit `article/manuscrit.md` (lecture seule) et regenere quatre zones marquees
de `article/latex/main.tex` :

    % === GENERATED:ABSTRACT BEGIN ... END ===
    % === GENERATED:BODY BEGIN ... END ===       (sections 1-7, figures, tableaux)
    % === GENERATED:APPENDIX BEGIN ... END ===   (annexes, apres \\appendix)
    % === GENERATED:BACKMATTER BEGIN ... END ===  (ethics / openscience / ai)

Tout le reste de main.tex (preambule, metadonnees ACM, titre, \\maketitle,
\\appendix, \\begin{acks}, bibliographie) est laisse tel quel : ce script ne
touche jamais a ces parties a la main.

ZONE ANNEXE -- LE MARQUEUR, ET POURQUOI CELUI-LA
------------------------------------------------
L'appel a communications PoPETs 2027 exclut du decompte des 12 pages du corps
« any clearly-marked appendices », au meme titre que la bibliographie, les
remerciements et les trois sections obligatoires. Jusqu'ici ce script n'avait
pas de zone annexe : une section « Appendix » ecrite dans le manuscrit tombait
dans BODY, donc DANS le decompte -- exactement l'inverse du but (constat de
`resultats/decision-pagination-2026-09-13.md` §2, qui renvoyait l'ouverture de
cette zone au present script).

MARQUEUR : le titre de niveau 2 NON NUMEROTE `## Appendix`.

    ## 10. AI Use
    ...
    ## Appendix              <-- marqueur : n'emet rien lui-meme
    ## Threshold census ...  <-- devient \\section{} sous \\appendix  -> « A »
    ## Secondary tables ...  <-- -> « B »
    ## References            <-- toujours remplace par la bibliographie auto

Ce choix n'est pas arbitraire : le fichier source utilise DEJA le titre de
niveau 2 non numerote comme sentinelle de structure -- `## Abstract` et
`## References` sont, avant cette modification, les deux seuls `##` sans
numero du manuscrit, et tous deux sont reconnus par leur intitule et traites a
part (resume d'un cote, bibliographie automatique de l'autre). `## Appendix`
est la troisieme sentinelle de la meme famille, reconnue de la meme facon.
Aucune convention nouvelle n'est introduite, et une section d'annexe reste un
`##` ordinaire -- ce que `\\appendix` renumerote en lettres (A, B, C...) sans
que le Markdown ait a porter la lettre.

Deux garde-fous, dans l'esprit du reste du script (echouer bruyamment plutot
que deviner) :
  - les sections OBLIGATOIRES gardent la priorite sur le marqueur. `Abstract`,
    `References` et les sections numerotees 8, 9, 10 (ethics / open science /
    AI use) partent dans leur zone propre meme si elles suivent `## Appendix`.
    Un marqueur mal place ne peut donc pas faire disparaitre en silence une
    section que le gabarit exige ;
  - un marqueur present mais suivi d'aucune section produit une zone annexe
    vide : c'est signale sur stderr, pas devine.

L'absence de marqueur est un cas normal (manuscrit sans annexe) : la zone est
alors emise vide, sans avis.

Il copie aussi article/references.bib vers article/latex/references.bib
(source figee, jamais modifiee -- seule la copie locale est (re)ecrite), et
CHAQUE figure reellement referencee par le manuscrit depuis article/figures/
vers article/latex/figures/ (meme principe : source figee, seule la copie
locale utilisee par \\includegraphics est (re)ecrite). Ce second point corrige
un defaut trouve par l'audit du 12/09 : la bibliographie etait resynchronisee
a chaque execution mais pas les figures, si bien qu'une figure regeneree dans
article/figures/ pouvait rester perimee indefiniment dans
article/latex/figures/ sans qu'aucun signal n'apparaisse. Voir sync_figures()
plus bas pour le garde-fou associe (echec bruyant si une figure referencee est
introuvable, vide, ou si la copie ne reproduit pas exactement la source).

REJOUABLE : relancer `python3 md2latex.py` depuis n'importe quel repertoire
regenere main.tex a partir de l'etat courant de manuscrit.md. Aucune
dependance externe (bibliotheque standard uniquement) : choix delibere,
pandoc n'etant pas installe sur cette machine (voir le rapport pour la
justification complete de ce choix d'outil).

CE QUE CE SCRIPT NE FAIT PAS
-----------------------------
- Il n'invente aucune clef bibliographique : toute mention `[cle]` du
  manuscrit qui ne peut pas etre reliee a une entree de references.bib
  (directement ou via la table de correspondance ci-dessous, elle-meme
  issue de article/references-verification.md) est laissee visible dans
  le PDF sous la forme littérale "[[CITATION NON RESOLUE: cle]]" et
  reportee sur stderr -- jamais remplacee par une invention.
- Il ne modifie ni ne lit en ecriture aucun fichier hors de article/latex/.
- Il ne decide d'aucun choix editorial (ou couper si le corps depasse la
  limite, comment nommer l'\\Description{} des figures, etc.) : ces points
  sont signales sur stderr et dans le rapport, pas tranches ici.
"""

import os
import re
import sys
import shutil
import hashlib
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
MANUSCRIPT_PATH = os.path.normpath(os.path.join(HERE, "..", "manuscrit.md"))
BIB_SRC_PATH = os.path.normpath(os.path.join(HERE, "..", "references.bib"))
BIB_DST_PATH = os.path.join(HERE, "references.bib")
FIGURES_SRC_DIR = os.path.normpath(os.path.join(HERE, "..", "figures"))
MAIN_TEX_PATH = os.path.join(HERE, "main.tex")

# ---------------------------------------------------------------------------
# Table de correspondance clef-provisoire -> clef-finale du .bib.
# Source : article/references-verification.md, section "Controle croise avec
# le manuscrit" (13 ecarts, tous "meme travail, convention de mot-cle
# differente" sauf deux corrections de fond documentees dans ce meme
# fichier). Recopiee ici a la main -- si le manuscrit ou le .bib changent de
# convention de nommage, cette table devra etre mise a jour a la main aussi;
# le script ne la deduit pas automatiquement (deliberement : inventer une
# correspondance par ressemblance de nom serait exactement le risque que la
# mission demande d'eviter).
# ---------------------------------------------------------------------------
CITATION_RENAME = {
    "toubia2025twin": "toubia2025twin2k500",
    "park2024generative": "park2024agents",
    "taub2018dcap": "taub2018differential",
    "giomi2023anonymeter": "giomi2023unified",
    "ganev2024genlaw": "ganev2024regulatory",
    "argyle2023out": "argyle2023outofone",
    "byun2025kdd": "byun2025riskcontext",
    "adams2025iscience": "adams2025fidelity",
    "eckersley2010browser": "eckersley2010unique",
    "satml2025position": "zhang2024satml",
    "anon2026decoupling": "shafieinejad2026diffusion",
    "drechsler2024synthetic": "drechsler2024thirtyyears",
    "bowen2023synthetic": "hu2023microdata",
}

UNRESOLVED_CITATIONS = []  # liste de (clef, contexte) pour le rapport final
SPECIAL_CHARS_SEEN = {}    # caracteres non mappes rencontres en sortie (diagnostic)
REFERENCED_FIGURES = set() # chemins relatifs ("figures/xxx.png") reellement
                            # rencontres pendant le parcours du manuscrit (rempli
                            # par render_figure_block ci-dessous) -- sync_figures()
                            # copie EXACTEMENT cet ensemble, jamais une liste figee
                            # a l'ecriture de ce script, pour couvrir aussi une
                            # figure future non encore connue aujourd'hui.
PREDICTIONS_TABLE_RENDER_COUNT = 0  # nombre de fois render_predictions_table()
                                    # a ete appelee -- sert de garde-fou pour
                                    # la substitution automatique "Table N" ->
                                    # \ref{tab:predictions} (voir plus bas) :
                                    # cette substitution suppose qu'un seul
                                    # tableau existe dans le document.
OTHER_TABLE_RENDER_COUNT = 0        # idem pour render_witness_table() (ou tout
                                    # autre type de tableau) : si ce compteur
                                    # devient > 0, l'hypothese "un seul tableau"
                                    # ne tient plus et _convert_table_refs()
                                    # doit etre revisee (elle ne sait pas
                                    # aujourd'hui distinguer plusieurs cibles).

# ---------------------------------------------------------------------------
# Petite table de mots-nombres, utilisee UNIQUEMENT pour deriver la legende du
# tableau des predictions depuis le nombre reel de lignes (voir
# render_predictions_table). Corrige un defaut trouve par l'audit du 12/09 :
# la legende portait le mot "sixteen" ecrit en dur, alors que le tableau avait
# deja 17 lignes -- un ajout de ligne ulterieur (T2) n'avait pas ete repercute
# dans la legende, et regenerer main.tex depuis le Markdown ne le corrigeait
# jamais puisque le mot ne derivait pas du Markdown. Solution : ne plus jamais
# ecrire le compte en toutes lettres a la main, le calculer depuis
# `len(data)`. Bornee a 1-20 : au-dela, echouer bruyamment plutot que de
# revenir silencieusement a un chiffre (coherent avec le reste du script, voir
# render_figure_block()).
# ---------------------------------------------------------------------------
_NUMBER_WORDS = {
    1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
    8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve",
    13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
    17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
}


def _spell_number(n):
    word = _NUMBER_WORDS.get(n)
    if word is None:
        raise ValueError(
            "Nombre de lignes du tableau des predictions (%d) hors de la "
            "table de mots-nombres codee en dur (1-20) -- etendre "
            "_NUMBER_WORDS plutot que de revenir a un chiffre fixe dans la "
            "legende." % n
        )
    return word


def _convert_table_refs(text):
    """Remplace tout renvoi litteral "Table N" par un renvoi LaTeX automatique
    \\ref{tab:predictions}, qui se renumerote seul a la compilation.

    Defaut corrige (audit du 12/09) : le Markdown ecrit "Table N" en toutes
    lettres, recopie tel quel dans le .tex ; ce numero se desynchronise du
    numero reel compose par LaTeX des que le nombre ou l'ordre des tableaux
    change (deja arrive : le manuscrit disait "Table 3" pour un document qui
    ne contient qu'un seul tableau, donc "Table 1"). Tant qu'un seul tableau
    existe dans le document (garde par PREDICTIONS_TABLE_RENDER_COUNT /
    OTHER_TABLE_RENDER_COUNT dans main(), verifie apres coup), tout renvoi
    "Table N" du manuscrit designe forcement ce tableau -- la substitution est
    donc sans ambiguite. Si un second tableau est introduit un jour, cette
    fonction devra distinguer les cibles (le garde-fou dans main() previent
    plutot que de deviner silencieusement)."""
    return re.sub(r"\bTable\s+\d+\b", r"Table~\\ref{tab:predictions}", text)


def load_bib_keys(path):
    text = open(path, encoding="utf-8").read()
    return set(re.findall(r"@[A-Za-z]+\{\s*([A-Za-z0-9_:.\-]+)\s*,", text))


# ---------------------------------------------------------------------------
# Conversion d'un fragment de texte inline (paragraphe, cellule de tableau,
# legende de figure) vers du LaTeX. Strategie "proteger puis echapper" :
# 1) extraire les segments a code (`...`) et les citations [cle] et les
#    remplacer par des jetons opaques, pour que l'echappement generique qui
#    suit ne les abime pas ;
# 2) convertir gras/italique markdown ;
# 3) echapper les caracteres speciaux LaTeX restants (%, &, #, ~, ^, \, $) ;
# 4) convertir les symboles unicode (tirets, fleches, approx, kappa...) vers
#    leurs commandes LaTeX, en mode mathematique quand necessaire (verifie
#    par compilation, voir le rapport) ;
# 5) convertir q_i / a_j / q_j (les seules variables indicees en prose hors
#    blocs de code) en mode mathematique ;
# 6) convertir les guillemets droits en guillemets typographiques `` '' ;
# 7) restaurer les jetons proteges sous leur forme LaTeX finale.
# ---------------------------------------------------------------------------

_PLACEHOLDER_RE = re.compile(r"\uE000(\d+)\uE001")


def _protect(text, placeholders):
    """Remplace `code` et [cle(,cle)*] par des jetons opaques (PUA unicode,
    donc invisibles a toute regex ulterieure sur la ponctuation ASCII)."""

    def stash(value):
        idx = len(placeholders)
        placeholders.append(value)
        return "\uE000%d\uE001" % idx

    # blocs de code `...`
    def repl_code(m):
        raw = m.group(1)
        # allow_breaks=True partout : les identifiants/chemins longs
        # (noms de fichiers resultats/*.md, chemins article/figures/...)
        # apparaissent aussi bien en prose que dans les cellules de
        # tableau, et le meme debordement guette dans les deux cas.
        escaped = _escape_texttt(raw, allow_breaks=True)
        return stash("\\texttt{%s}" % escaped)

    text = re.sub(r"`([^`]+)`", repl_code, text)

    # citations [cle] ou [cle1, cle2, ...] -- uniquement des identifiants
    # alphanumeriques commencant par une lettre (exclut donc les intervalles
    # numeriques [21.5 ; 25.0] et les renvois internes [c7-xxx.md §1], qui
    # contiennent des points/tirets/le signe section et ne matchent pas).
    key_pat = r"[A-Za-z][A-Za-z0-9]*"
    bracket_pat = re.compile(r"\[(%s(?:,\s*%s)*)\]" % (key_pat, key_pat))

    def repl_cite(m):
        keys = [k.strip() for k in m.group(1).split(",")]
        resolved = []
        any_unresolved = False
        for k in keys:
            if k in BIB_KEYS:
                resolved.append(k)
            elif k in CITATION_RENAME and CITATION_RENAME[k] in BIB_KEYS:
                resolved.append(CITATION_RENAME[k])
            else:
                any_unresolved = True
                UNRESOLVED_CITATIONS.append((k, text[max(0, m.start() - 60):m.end() + 20]))
        if any_unresolved:
            return stash("\\textbf{[[CITATION NON RESOLUE: %s]]}" % ", ".join(keys))
        return stash("\\cite{%s}" % ",".join(resolved))

    text = bracket_pat.sub(repl_cite, text)
    return text


def _escape_texttt(raw, allow_breaks=False):
    # Dans un \texttt{}, on echappe les caracteres speciaux LaTeX mais on ne
    # touche a rien d'autre (les chemins/identifiants de fichiers n'ont pas
    # de gras/italique/citations a l'interieur).
    raw = raw.replace("\\", r"\textbackslash{}")
    raw = raw.replace("_", r"\_\allowbreak{}" if allow_breaks else r"\_")
    raw = raw.replace("%", r"\%")
    raw = raw.replace("&", r"\&")
    raw = raw.replace("#", r"\#")
    if allow_breaks:
        # BUG TROUVE PAR COMPILATION REELLE (pas suppose) : les identifiants
        # de fichiers longs (ex. "c7-attaquant-fort-resultats.md", ~31
        # caracteres) debordaient hors de leur colonne de Table 3 (§7.1) et
        # chevauchaient la marge des numeros de ligne du mode review, meme
        # apres avoir elargi la colonne -- \texttt desactive la
        # cesure automatique, donc un identifiant sans espace reste un seul
        # "mot" insecable. Insertion d'un point de coupure autorise (pas
        # force) apres chaque "-" et "/" : la colonne peut alors envelopper
        # la ligne a l'endroit naturel du tiret plutot que de deborder.
        raw = raw.replace("-", r"-\allowbreak{}")
        raw = raw.replace("/", r"/\allowbreak{}")
        # MEME CONSTAT, TROUVE PAR COMPILATION REELLE (2026-09-12, passage
        # mise en page finale) : les points de coupure ci-dessus ne
        # suffisaient pas pour un identifiant long depourvu de "-"/"/" dans
        # son dernier segment (ex. "resultats/c7-preenregistrement.md" --
        # apres coupure sur "/" et "-", il restait "preenregistrement.md"
        # comme seul bloc insecable, encore assez large pour deborder en fin
        # de colonne etroite). Overfull \hbox mesures : 32.65pt et 32.29pt
        # (main.log, section Open Science) avant cette correction.
        #
        # Premier essai rejete apres verification visuelle : un point de
        # coupure autorise APRES le point (".\allowbreak{}") deplacait bien
        # le debordement, mais au prix d'une coupure ".md" -> "." en fin de
        # ligne / "md" seul au debut de la suivante, qui separe l'extension
        # de son point -- pire visuellement que le debordement d'origine.
        # Coupure placee AVANT le point a la place : l'extension et son
        # point ("."+"md") restent un seul bloc sur la ligne suivante,
        # seul le nom de base peut se retrouver seul en fin de ligne
        # precedente -- verifie par rendu d'image, voir resultats/latex-
        # gabarit-2026-09-12.md.
        raw = raw.replace(".", r"\allowbreak{}.")
    return raw


_UNICODE_MATH_MAP = [
    ("\u2192", r"$\rightarrow$"),   # →
    ("\u2248", r"$\approx$"),        # ≈
    ("\u2265", r"$\geq$"),           # ≥
    ("\u2264", r"$\leq$"),           # ≤
    ("\u00d7", r"$\times$"),         # ×
    ("\u03ba", r"$\kappa$"),         # κ
    ("\u221e", r"$\infty$"),         # ∞
    ("\u00b7", r"$\cdot$"),          # · (middot, hors "10^-4" deja traite)
    ("\u03c1", r"$\rho$"),           # ρ (au cas ou)
]


_EXPOSANTS_UNICODE = {
    "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4",
    "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9",
    "⁻": "-", "⁺": "+",
}
_EXPOSANTS_RE = re.compile("[%s]+" % "".join(_EXPOSANTS_UNICODE))


def _convert_unicode_math(text):
    # Cas particulier repere manuellement (une seule occurrence dans la
    # legende de la Figure 1) : "4·10⁻⁴" en exposant unicode. Traite avant
    # la regle generale du middot pour eviter un $4$\cdot$10⁻⁴$ mal forme.
    text = text.replace("4\u00b710\u207b\u2074", r"$4\cdot10^{-4}$")

    # Exposants unicode, regle GENERALE (posee apres le cas particulier
    # ci-dessus, qui reste prioritaire).
    #
    # BUG TROUVE PAR COMPILATION REELLE (pas suppose) : le manuscrit porte
    # "p < 10\u207b\u2074" (bloc du \u00a75.1). U+207B et U+2074 n'etaient dans aucune
    # table, donc recopies tels quels dans le .tex ; pdflatex s'arretait
    # alors net -- "Unicode character (U+207B) not set up for use with LaTeX
    # ... Fatal error occurred, no output PDF file produced". Le diagnostic
    # SPECIAL_CHARS_SEEN les signalait bien en fin d'execution, mais sans
    # bloquer : le defaut ne se decouvrait qu'a la compilation suivante.
    # Traduits ici en exposant mathematique reel. Aucun chiffre n'est
    # modifie, seule la notation change.
    def _repl_exposant(m):
        return "$^{%s}$" % "".join(_EXPOSANTS_UNICODE[c] for c in m.group(0))

    text = re.sub(_EXPOSANTS_RE, _repl_exposant, text)

    # Signe moins unicode (U+2212), utilise dans le manuscrit pour les
    # nombres negatifs ("−0.133") : le mettre en mode mathematique pour
    # avoir un vrai signe moins typographique plutot qu'un trait d'union.
    text = re.sub(r"\u2212(\d)", r"$-\1$", text)

    for u, latex in _UNICODE_MATH_MAP:
        text = text.replace(u, latex)

    # tirets
    text = text.replace("\u2014", "---")  # em dash —
    text = text.replace("\u2013", "--")   # en dash –

    # Cas particulier : §8 et §9 renvoient a Ethical Considerations et Open
    # Science, deux sections du gabarit PoPETs (popets.sty, \specialcomment
    # ethics/openscience) rendues avec \section* -- donc SANS numero visible,
    # par convention du venue (a l'instar des Acknowledgments ACM). On ne
    # renumerote pas le gabarit standard PoPETs pour ces sections obligatoires
    # (ca romprait la convention du venue et le style vendu tel quel) ; a la
    # place, tout renvoi numerique "§8"/"§9" du manuscrit est traduit ici en
    # le nom de la section cible, en reutilisant \ethicsname/\osname deja
    # definis dans popets.sty -- si l'intitule change un jour, le renvoi
    # suit AVANT la regle generale "§N" -> "\S\,N" ci-dessous (qui,
    # sinon, consommerait "§8"/"§9" en premier) ; cette regle generale
    # reste inchangee pour toutes les autres sections (numerotees, elles).
    text = re.sub(r"\u00a7\s*8\b", r"\\ethicsname{}", text)
    text = re.sub(r"\u00a7\s*9\b", r"\\osname{}", text)

    # signe section : "§5.3" -> "\S\,5.3"
    text = re.sub(r"\u00a7\s*(\d)", r"\\S\\,\1", text)
    text = text.replace("\u00a7", r"\S{}")

    return text


def _convert_subscripts(text):
    # q_i, a_j, q_j (les seules variables indicees en prose hors backticks,
    # verifie par grep sur tout le manuscrit avant d'ecrire cette regle).
    # IMPORTANT : cette fonction s'applique APRES _escape_latex_specials
    # (qui a deja transforme "_" en "\_"), donc le motif recherche est
    # "lettre\_alnum", pas "lettre_alnum" -- sinon le "_" fraichement
    # reinsere par cette regle est lui-meme echappe au passage suivant,
    # produisant "$a\_{j}$" au lieu de "$a_{j}$" (bug trouve par
    # compilation reelle, voir le rapport).
    return re.sub(r"\b([A-Za-z])\\_([A-Za-z0-9]+)\b", r"$\1_{\2}$", text)


def _convert_quotes(text):
    # Guillemets droits -> guillemets typographiques LaTeX. Heuristique
    # simple : un " precede d'un debut de mot/espace/ouverture ouvre, un "
    # suivi d'un espace/ponctuation/fin ferme. Le manuscrit n'utilise que
    # des guillemets droits (verifie : aucun caractere U+201C/201D/2018/2019
    # trouve par le scan unicode prealable).
    def repl(m):
        return "``" if m.group(1) is None else "''"

    # alterne ouverture/fermeture en parcourant les occurrences dans l'ordre
    parts = text.split('"')
    if len(parts) == 1:
        return text
    out = parts[0]
    for i, part in enumerate(parts[1:]):
        out += "``" if i % 2 == 0 else "''"
        out += part
    return out


def _escape_latex_specials(text):
    # Echappement generique des caracteres speciaux LaTeX restant dans le
    # texte "brut" (hors segments proteges). Ordre important : backslash
    # d'abord serait dangereux ici car nos propres commandes generees plus
    # tard ($, \cite, etc.) ne sont pas encore inserees a ce stade (elles
    # restent dans des jetons proteges) -- donc aucun backslash "legitime"
    # n'existe encore dans le texte a ce point du pipeline.
    #
    # Espace insecable avant "%" : trouve par relecture des pages rendues
    # (pas du log) que "20.7 %" utilise un espace normal, donc coupable en
    # fin de ligne (le "%" isole en debut de ligne suivante). Corrige ici,
    # pour TOUTE occurrence chiffre+espace+% du document (prose et
    # tableaux passent tous deux par convert_inline) : mise en page
    # seulement, la valeur numerique et le symbole restent inchanges.
    text = re.sub(r"(\d) %", r"\1~%", text)
    text = text.replace("%", r"\%")
    text = text.replace("&", r"\&")
    text = text.replace("#", r"\#")
    text = text.replace("_", r"\_")  # les q_i/a_j/q_j sont deja convertis avant cet appel
    return text


def convert_inline(raw):
    placeholders = []
    # Renvois "Table N" -> \ref automatique. Fait AVANT _protect : la phrase
    # "Table N" n'apparait jamais a l'interieur d'un `code` ou d'une citation
    # [cle], donc aucun risque de heurter un jeton protege ; et le \ref{...}
    # insere ici ne contient aucun caractere que les etapes suivantes
    # (echappement %&#_ , symboles unicode, guillemets) ne modifient.
    raw = _convert_table_refs(raw)
    # Intervalles "[a ; b]" : les deux espaces autour du ";" sont, avant
    # cette etape, des espaces normaux -- une coupure de ligne peut donc
    # tomber entre "19.0" et ";", ou entre ";" et "22.4", ce qui casse
    # visuellement un intervalle de confiance en deux lignes (repere par
    # relecture des pages rendues, pas par le log). 84 occurrences dans le
    # manuscrit actuel, toutes de la forme exacte "[NUM ; NUM]" (verifie :
    # aucune ne contient de gras/italique a l'interieur des crochets).
    # Espaces rendus insecables des deux cotes du ";" ; aucun chiffre, aucun
    # caractere du texte n'est modifie.
    raw = re.sub(
        r"\[(-?[0-9][0-9.,]*) ; (-?[0-9][0-9.,]*)\]",
        r"[\1~;~\2]",
        raw,
    )
    text = _protect(raw, placeholders)

    # gras puis italique (markdown) -- apres protection du code/citations
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*([^\s*][^*]*?)\*(?!\*)", r"\\textit{\1}", text)

    # echappement des caracteres speciaux restants (transforme aussi les
    # underscores de q_i/a_j/q_j en "\_", repris juste apres)
    text = _escape_latex_specials(text)

    # variables indicees en prose (q_i, a_j, q_j), reperees sur la forme
    # deja echappee "lettre\_alnum" -- voir le commentaire dans la fonction
    text = _convert_subscripts(text)

    # symboles unicode -> commandes LaTeX (dont mode mathematique)
    text = _convert_unicode_math(text)

    # guillemets droits -> typographiques
    text = _convert_quotes(text)

    # restauration des segments proteges (texttt / cite)
    def restore(m):
        return placeholders[int(m.group(1))]

    text = _PLACEHOLDER_RE.sub(restore, text)

    # diagnostic : tout caractere non-ASCII qui subsiste et n'est pas une
    # lettre latine accentuee usuelle est suspect -- le signaler plutot que
    # de le laisser passer en silence (c'est exactement le risque que la
    # mission demande de couvrir).
    SAFE_ACCENTED = set("àâäéèêëîïôöùûüçÀÂÄÉÈÊËÎÏÔÖÙÛÜÇ")
    for ch in text:
        if ord(ch) > 127 and ch not in SAFE_ACCENTED:
            SPECIAL_CHARS_SEEN.setdefault(ch, 0)
            SPECIAL_CHARS_SEEN[ch] += 1

    return text


# ---------------------------------------------------------------------------
# Parsing du manuscrit
# ---------------------------------------------------------------------------

def strip_heading_number(title):
    """Retire un numero de tete du type '1.2 ' ou '7.1 ' ; laisse intact les
    titres sans numerotation numerique (ex. 'T1 --- Panel holder ...')."""
    return re.sub(r"^\d+(?:\.\d+)*\.?\s+", "", title).strip()


def parse_table_block(lines):
    """lines: liste de lignes brutes '|a|b|c|' (sans la ligne de separation
    '|---|---|'). Retourne une liste de lignes, chaque ligne une liste de
    cellules (texte brut, non converti)."""
    rows = []
    for line in lines:
        line = line.strip()
        if re.match(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?$", line):
            continue  # ligne de separation d'en-tete
        cells = [c.strip() for c in line.strip("|").split("|")]
        rows.append(cells)
    return rows


def render_witness_table(rows):
    """Table 5.1 : 3 colonnes (witness, mean rho, [p5;p95]), 8 lignes de
    donnees. Table pleine largeur non necessaire (colonne unique acmart) :
    on utilise `table` (pas table*), en resserrant sur les 3 colonnes."""
    global OTHER_TABLE_RENDER_COUNT
    OTHER_TABLE_RENDER_COUNT += 1
    header, *data = rows
    out = []
    out.append(r"\begin{table}[t]")
    out.append(r"  \small")
    out.append(r"  \caption{Corrected fingerprint-free witnesses matched on per-person accuracy (\S5.1; structure reproduced from \texttt{c7-nul-corrige-resultats.md} \S3).}")
    out.append(r"  \label{tab:witnesses}")
    # `table` (pas `table*`) : une seule colonne acmart (\columnwidth), donc
    # p{} dimensionnes sur \columnwidth et non \textwidth. \raggedright
    # pour eviter un debordement si un nom de construction est long (ex.
    # "N1b segment mode, Bernoulli").
    out.append(r"  \setlength{\tabcolsep}{3pt}")
    out.append(r"  \begin{tabular}{@{}>{\raggedright\arraybackslash}p{0.52\columnwidth}"
                r">{\raggedright\arraybackslash}p{0.16\columnwidth}"
                r">{\raggedright\arraybackslash}p{0.22\columnwidth}@{}}")
    out.append(r"    \toprule")
    out.append("    %s \\\\" % " & ".join(convert_inline(c) for c in header))
    out.append(r"    \midrule")
    for r in data:
        out.append("    %s \\\\" % " & ".join(convert_inline(c) for c in r))
    out.append(r"    \bottomrule")
    out.append(r"  \end{tabular}")
    out.append(r"\end{table}")
    return "\n".join(out)


def render_predictions_table(rows):
    """Tableau des predictions, §7.1 : N lignes x 4 colonnes (#, Prediction,
    Outcome, Source), N derive de `len(data)` (voir _spell_number : plus
    jamais ecrit en dur, apres le defaut "sixteen" trouve par l'audit du
    12/09 sur un tableau qui avait deja 17 lignes). Pleine largeur (table*)
    avec colonnes p{} dimensionnees pour eviter le debordement -- largeurs
    verifiees par compilation reelle (voir le rapport pour les iterations)."""
    global PREDICTIONS_TABLE_RENDER_COUNT
    PREDICTIONS_TABLE_RENDER_COUNT += 1
    header, *data = rows
    out = []
    out.append(r"\begin{table*}[t]")
    out.append(r"  \small")
    out.append(r"  \caption{The %s preregistered predictions and their outcomes (\S7.1).}" % _spell_number(len(data)))
    out.append(r"  \label{tab:predictions}")
    # Largeurs choisies puis VERIFIEES par compilation reelle (pas
    # supposees) : une premiere tentative (0.018/0.30/0.52/0.10, sans
    # reduire \tabcolsep) debordait dans la marge des numeros de ligne du
    # mode review sur la colonne Source, qui contient des noms de fichiers
    # `texttt` longs et non coupables (ex. c7-attaquant-fort-resultats.md).
    # Correction : \tabcolsep resserre + colonne Source elargie +
    # \raggedright pour autoriser un retour a la ligne propre plutot qu'un
    # unique mot trop large pour sa colonne.
    out.append(r"  \setlength{\tabcolsep}{3pt}")
    out.append(r"  \begin{tabular}{@{}>{\raggedright\arraybackslash}p{0.02\textwidth}"
                r">{\raggedright\arraybackslash}p{0.27\textwidth}"
                r">{\raggedright\arraybackslash}p{0.50\textwidth}"
                r">{\raggedright\arraybackslash}p{0.135\textwidth}@{}}")
    out.append(r"    \toprule")
    out.append("    %s \\\\" % " & ".join(convert_inline(c) for c in header))
    out.append(r"    \midrule")
    for r in data:
        out.append("    %s \\\\" % " & ".join(convert_inline(c) for c in r))
    out.append(r"    \bottomrule")
    out.append(r"  \end{tabular}")
    out.append(r"\end{table*}")
    return "\n".join(out)


FIGURE_FILES = {
    1: "figures/fig1-monde-ouvert.png",
    2: "figures/fig2-couplage.png",
}
FIGURE_LABELS = {
    1: "fig:monde-ouvert",
    2: "fig:couplage",
}


def render_figure_block(quote_lines):
    """quote_lines : lignes brutes du blockquote (deja depouillees du '> ')
    formant la legende complete de la figure (y compris la phrase
    'Data: ...' finale, exactement comme le squelette precedent le
    comptait). Detecte le numero de figure depuis '**Figure N --'."""
    full_text = " ".join(l.strip() for l in quote_lines if l.strip())
    m = re.match(r"\*\*Figure (\d)", full_text)
    if not m:
        # GARDE-FOU : tout bloc '>' du manuscrit est suppose etre une des
        # deux figures (aucun autre usage de blockquote n'existe au moment
        # ou ce script est ecrit). Si une revision future ajoute un
        # blockquote non-figure (une vraie citation, par exemple), ne PAS
        # deviner silencieusement quelle image utiliser -- echouer bruyamment
        # pour forcer une mise a jour de cette fonction plutot que d'inserer
        # la mauvaise figure sous la mauvaise legende.
        raise ValueError(
            "Bloc '>' rencontre qui ne commence pas par '**Figure N' : %r. "
            "render_figure_block() suppose que tout blockquote est une figure ; "
            "adapter le script si le manuscrit contient desormais un autre "
            "usage des blockquotes (ex. une citation)." % full_text[:120]
        )
    fig_no = int(m.group(1))
    if fig_no not in FIGURE_FILES:
        raise ValueError("Figure %d citee dans le manuscrit mais aucun fichier connu pour ce numero "
                          "(FIGURE_FILES ne connait que %s) -- ajouter l'entree manquante." % (fig_no, list(FIGURE_FILES)))
    path = FIGURE_FILES[fig_no]

    # CORRECTIF (relecture de rendu 2026-09-13, defaut 1) : le gabarit LaTeX
    # (\caption{...} dans un environnement figure) prefixe deja
    # automatiquement "Figure N : " au rendu -- si le texte de legende du
    # manuscrit commence LUI AUSSI par "**Figure N -- ...**", le rendu
    # affiche "Figure 1 : Figure 1 -- ..." en double. On retire ici ce
    # prefixe repete de la legende avant conversion (pas dans le manuscrit :
    # c'est un defaut du gabarit, pas du texte), en gardant le marqueur
    # gras '**' d'ouverture pour ne pas perdre la mise en gras du titre de
    # legende qui suit.
    full_text = re.sub(
        r"^\*\*Figure \d+\s*[—–-]+\s*", "**", full_text, count=1,
    )

    # CORRECTIF (relecture de rendu 2026-09-13, defaut 3) : une legende ne
    # doit jamais citer le chemin de son propre fichier image -- c'est un
    # detail de fabrication interne au depot, pas une information pour le
    # lecteur. Retire tout renvoi entre parentheses au nom de base du
    # fichier de LA figure courante (ex. "(`article/figures/fig2-
    # couplage.png`)"), ou qu'il apparaisse dans la legende, sans toucher a
    # aucun autre mot du texte.
    basename = os.path.basename(path)
    full_text = re.sub(
        r"\s*\(`[^`]*%s`\)" % re.escape(basename), "", full_text,
    )

    caption_latex = convert_inline(full_text)
    REFERENCED_FIGURES.add(path)
    label = FIGURE_LABELS[fig_no]
    out = []
    out.append(r"\begin{figure}[t]")
    out.append(r"  \centering")
    out.append(r"  \includegraphics[width=\linewidth,height=0.85\textheight,keepaspectratio]{%s}" % path)
    out.append(r"  \caption{%s}" % caption_latex)
    # DECISION SIGNALEE (voir rapport) : aucune description d'accessibilite
    # distincte de la legende n'existe dans le manuscrit ; on reutilise la
    # legende convertie comme \Description, plutot que d'en inventer une.
    out.append(r"  \Description{%s}" % caption_latex)
    out.append(r"  \label{%s}" % label)
    out.append(r"\end{figure}")
    out.append(r"\FloatBarrier")
    return "\n".join(out)


def paragraphs_to_latex(block_lines):
    """Convertit une sequence de lignes (paragraphes separes par des lignes
    vides, blocs '>' = figures, blocs '|' = tableaux) en une liste de
    fragments LaTeX (un \\section/subsection ne fait pas partie de ceci :
    c'est traite par l'appelant)."""
    fragments = []
    i = 0
    n = len(block_lines)
    para_buf = []

    def flush_para():
        if para_buf:
            text = " ".join(l.strip() for l in para_buf if l.strip())
            if text:
                fragments.append(convert_inline(text))
            para_buf.clear()

    while i < n:
        line = block_lines[i]
        if line.strip() == "":
            flush_para()
            i += 1
            continue
        if line.startswith(">"):
            flush_para()
            quote = []
            while i < n and block_lines[i].startswith(">"):
                quote.append(block_lines[i][1:].lstrip())
                i += 1
            fragments.append(render_figure_block(quote))
            continue
        if line.startswith("|"):
            flush_para()
            table_lines = []
            while i < n and block_lines[i].startswith("|"):
                table_lines.append(block_lines[i])
                i += 1
            rows = parse_table_block(table_lines)
            ncols = len(rows[0])
            if ncols == 3:
                fragments.append(render_witness_table(rows))
            elif ncols == 4:
                fragments.append(render_predictions_table(rows))
            else:
                raise ValueError("Table a %d colonnes non geree" % ncols)
            continue
        para_buf.append(line)
        i += 1
    flush_para()
    return fragments


def _sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def sync_figures():
    """Copie depuis article/figures/ (source figee, jamais modifiee ici) vers
    article/latex/figures/ (copie locale utilisee par \\includegraphics)
    CHAQUE figure listee dans REFERENCED_FIGURES, c'est-a-dire chaque figure
    effectivement rencontree pendant le parcours du manuscrit par
    render_figure_block() -- pas une liste de noms figee a l'ecriture de cette
    fonction, pour couvrir aussi une figure future pas encore connue
    aujourd'hui.

    Garde-fou (defaut trouve par l'audit du 12/09) : ce script resynchronisait
    deja references.bib a chaque execution, mais jamais les figures -- une
    figure regeneree dans article/figures/ pouvait donc rester perimee
    indefiniment dans article/latex/figures/ sans qu'aucun signal
    n'apparaisse, et le PDF compilait "normalement" sur une image obsolete.
    On echoue donc bruyamment (arret complet, aucun fichier laisse a moitie
    ecrit) si :
      - une figure referencee par le document est introuvable dans la source ;
      - la source ou la copie fait 0 octet (une figure peut se rendre en
        taille nulle sans qu'un simple comptage de taille de fichier ne le
        voie forcement a temps -- on verifie explicitement) ;
      - la copie ne reproduit pas exactement la source (empreinte SHA-256
        differente apres copie).
    Affiche, a chaque execution, la taille et l'empreinte SHA-256 de chaque
    figure copiee : une divergence future (figure perimee, copie tronquee)
    doit sauter aux yeux immediatement plutot que de se decouvrir a la
    compilation, ou pire, apres."""
    if not REFERENCED_FIGURES:
        sys.exit(
            "ERREUR : aucune figure referencee detectee dans le manuscrit -- "
            "arret plutot que de continuer en silence (verifier que ce n'est "
            "pas une regression du parseur de blockquotes/figures)."
        )
    print("--- Synchronisation des figures (source : %s) ---" % FIGURES_SRC_DIR, file=sys.stderr)
    for relpath in sorted(REFERENCED_FIGURES):
        basename = os.path.basename(relpath)
        src = os.path.join(FIGURES_SRC_DIR, basename)
        dst = os.path.join(HERE, relpath)
        if not os.path.isfile(src):
            sys.exit(
                "ERREUR : figure referencee par le manuscrit introuvable dans la "
                "source : %s (attendue pour %s dans main.tex). Arret -- pas de "
                "compilation sur une figure perimee ou manquante." % (src, relpath))
        src_size = os.path.getsize(src)
        if src_size == 0:
            sys.exit(
                "ERREUR : la figure source %s fait 0 octet -- arret plutot que "
                "de propager une figure vide dans le PDF." % src)
        src_hash = _sha256(src)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        try:
            shutil.copyfile(src, dst)
        except OSError as e:
            sys.exit("ERREUR : echec de copie de %s vers %s : %s" % (src, dst, e))
        if not os.path.isfile(dst):
            sys.exit(
                "ERREUR : copie de %s vers %s : fichier destination absent "
                "juste apres la copie." % (src, dst))
        dst_size = os.path.getsize(dst)
        dst_hash = _sha256(dst)
        if dst_size == 0 or dst_hash != src_hash:
            sys.exit(
                "ERREUR : copie de %s vers %s incomplete ou corrompue "
                "(taille source=%d dest=%d octets, empreinte source=%s "
                "dest=%s)." % (src, dst, src_size, dst_size, src_hash, dst_hash))
        print("  %-32s %8d octets  sha256=%s  -> %s" % (basename, dst_size, dst_hash, dst), file=sys.stderr)
    print("--- %d figure(s) synchronisee(s), toutes verifiees octet pour octet ---"
          % len(REFERENCED_FIGURES), file=sys.stderr)


_TITLE_LINE_RE = re.compile(r"^\\title\[[^\n]*\]\{[^\n]*\}[ \t]*$", re.MULTILINE)


def load_manuscript_title():
    """Lit la premiere ligne non vide de article/manuscrit.md (le titre H1,
    '# ...'), la convertit en LaTeX avec la meme fonction que le reste du
    contenu genere (accents, %, deux-points, guillemets...), et en derive un
    titre court pour l'en-tete de page acmart (\\title[court]{complet}).

    Defaut corrige (meme famille que le mot "sixteen" fige dans la legende du
    tableau, et que les figures non resynchronisees -- tous deux corriges par
    l'audit du 12/09) : le titre etait recopie a la main dans main.tex, en
    dehors des zones GENERATED, donc gele sur l'ancien titre a chaque
    reecriture du manuscrit sans qu'aucune regeneration ne le rattrape. Il
    derive maintenant de la meme source que le reste du document.

    GARDE-FOU : comme _spell_number() et sync_figures(), on echoue bruyamment
    (arret complet, aucun fichier touche) si la premiere ligne est absente,
    n'est pas un titre H1, ou est vide -- plutot que de retomber en silence
    sur un titre par defaut, ce qui est exactement le defaut ici corrige.

    Titre court : tout ce qui precede le premier ':' du titre complet --
    c'est la convention deja en usage dans ce document (l'ancien titre en dur
    suivait exactement ce decoupage : "Linkability of LLM Digital Twins"
    avant son ':'), rendue explicite et derivee ici plutot que recopiee a la
    main. Si le titre complet ne contient pas de ':', aucun raccourci n'en
    est tire par ressemblance ou troncature arbitraire (ce serait deviner) :
    le titre court est alors identique au titre complet, et un avis est
    imprime sur stderr pour signaler ce cas non ambigu mais moins courant.
    """
    text = open(MANUSCRIPT_PATH, encoding="utf-8").read()
    first_nonempty = None
    for line in text.split("\n"):
        if line.strip() != "":
            first_nonempty = line
            break
    if first_nonempty is None or not first_nonempty.startswith("# "):
        sys.exit(
            "ERREUR : titre introuvable -- la premiere ligne non vide de %s "
            "devrait etre un titre H1 ('# ...'), trouve : %r. Arret plutot "
            "que de retomber sur un titre par defaut." % (MANUSCRIPT_PATH, first_nonempty)
        )
    raw_title = first_nonempty[2:].strip()
    if not raw_title:
        sys.exit(
            "ERREUR : titre H1 vide en tete de %s -- arret plutot que de "
            "retomber sur un titre par defaut." % MANUSCRIPT_PATH
        )
    full_title = convert_inline(raw_title)
    if not full_title.strip():
        sys.exit(
            "ERREUR : le titre converti est vide (source : %r) -- arret "
            "plutot que d'ecrire un \\title{} vide dans main.tex." % raw_title
        )
    if ":" in full_title:
        short_title = full_title.split(":", 1)[0].strip()
    else:
        short_title = full_title
        print(
            "AVIS : titre sans ':' -- aucun titre court distinct n'en est "
            "derive, \\title[...] reprend le titre complet tel quel.",
            file=sys.stderr,
        )
    return short_title, full_title


# ---------------------------------------------------------------------------
# MARQUEUR DE ZONE ANNEXE. Voir l'en-tete du module pour la justification du
# choix : c'est le titre de niveau 2 NON NUMEROTE `## Appendix`, troisieme
# sentinelle de la meme famille que `## Abstract` et `## References`, qui sont
# deja reconnus par leur intitule et traites a part. Le marqueur n'emet rien :
# il dit seulement « a partir d'ici, on n'est plus dans le corps ».
# ---------------------------------------------------------------------------
APPENDIX_MARKER = "Appendix"

# Titres et numeros que le marqueur NE peut PAS capturer : ce sont les zones
# imposees par le gabarit PoPETs. Elles partent dans leur zone propre ou
# qu'elles se trouvent dans le fichier source, y compris apres le marqueur --
# un marqueur mal place ne doit jamais faire disparaitre en silence une
# section que le venue exige.
ZONES_RESERVEES_PAR_TITRE = {"Abstract", "References"}
ZONES_RESERVEES_PAR_NUMERO = {"8", "9", "10"}


def parse_sections(src):
    """Decoupe le manuscrit Markdown en sections de niveau 2, chacune portant
    ses sous-sections de niveau 3. Tout ce qui precede le premier '## ' (titre
    H1, ligne italique de metadonnees, '---') est ignore."""
    lines = src.split("\n")
    sections = []  # liste de dicts {title_raw, title, number, items:[...]}
    cur = None
    started = False
    for line in lines:
        m2 = re.match(r"^##\s+(.*)$", line)
        m3 = re.match(r"^###\s+(.*)$", line)
        if m2:
            started = True
            title_raw = m2.group(1).strip()
            num_match = re.match(r"^(\d+)\.?\s", title_raw)
            cur = {
                "title_raw": title_raw,
                "title": strip_heading_number(title_raw),
                "number": num_match.group(1) if num_match else None,
                "items": [],  # liste de ("para", [lines]) ou ("sub", title, [lines])
            }
            sections.append(cur)
            continue
        if not started:
            continue
        if m3 and cur is not None:
            cur["items"].append(("sub", strip_heading_number(m3.group(1).strip()), []))
            continue
        if line.strip() == "---":
            continue
        if cur is None:
            continue
        if cur["items"] and cur["items"][-1][0] == "sub":
            cur["items"][-1][2].append(line)
        else:
            if not cur["items"] or cur["items"][-1][0] != "para":
                cur["items"].append(("para", None, []))
            cur["items"][-1][2].append(line)
    return sections


def route_sections(sections):
    """Aiguille chaque section vers l'une des QUATRE zones generees et renvoie
    (abstract, body, appendix, backmatter), chacune une liste de fragments
    LaTeX.

    C'est ici, et nulle part ailleurs, que se decide ce qui compte dans les 12
    pages du corps : `body` seul est compte, `appendix` est emis apres
    \\appendix et en est exclu au titre des « clearly-marked appendices » de
    l'appel PoPETs 2027.

    Fonction pure (aucune lecture ni ecriture de fichier) : c'est ce qui rend
    la frontiere corps / annexe testable sans compiler, voir
    tests/latex/test_md2latex_annexe.py."""
    body_fragments = []
    appendix_fragments = []
    backmatter_fragments = []
    abstract_fragments = []
    marker_seen = False
    sections_after_marker = 0

    for sec in sections:
        title = sec["title"]
        number = sec["number"]

        # --- le marqueur lui-meme : bascule l'aiguillage, n'emet rien ---
        if not marker_seen and number is None and title == APPENDIX_MARKER:
            marker_seen = True
            continue

        # GARDE-FOU : une section imposee par le gabarit rencontree APRES le
        # marqueur part quand meme dans sa zone propre (les tests par titre /
        # par numero ci-dessous ont la priorite sur l'aiguillage annexe), mais
        # cela signale presque surement un marqueur mal place -- on le dit.
        # `References` est exclu de cet avis : la bibliographie ferme
        # legitimement le fichier source, donc apres les annexes, et elle est
        # de toute facon remplacee par la bibliographie automatique -- rien
        # ne peut s'y perdre.
        if marker_seen and (title in ZONES_RESERVEES_PAR_TITRE - {"References"}
                            or number in ZONES_RESERVEES_PAR_NUMERO):
            print(
                "AVIS : section reservee au gabarit (%r) rencontree APRES le "
                "marqueur d'annexe -- elle part dans sa zone propre, pas en "
                "annexe. Verifier la place du marqueur '## %s'."
                % (sec["title_raw"], APPENDIX_MARKER), file=sys.stderr)

        # rassemble le contenu direct (avant toute sous-section) + les
        # sous-sections, dans l'ordre
        direct_lines = []
        subsecs = []
        for kind, subtitle, body in sec["items"]:
            if kind == "para":
                direct_lines.extend(body)
                direct_lines.append("")
            else:
                subsecs.append((subtitle, body))

        if title == "Abstract":
            abstract_fragments.extend(paragraphs_to_latex(direct_lines))
            continue

        if title == "References":
            continue  # remplace par la bibliographie automatique (bibtex)

        if number == "8":
            backmatter_fragments.append("\\begin{ethics}")
            backmatter_fragments.extend(paragraphs_to_latex(direct_lines))
            for subtitle, body in subsecs:
                backmatter_fragments.append("\\textbf{%s}" % convert_inline(subtitle))
                backmatter_fragments.extend(paragraphs_to_latex(body))
            backmatter_fragments.append("\\end{ethics}")
            continue
        if number == "9":
            backmatter_fragments.append("\\begin{openscience}")
            # \sloppypar : cette section contient plusieurs chemins de
            # fichiers longs en \texttt (ex. "resultats/c7-argyle-
            # preenregistrement.md") juxtaposes dans une seule phrase enu-
            # merative. Meme avec les points de coupure de _escape_texttt
            # ci-dessus, une ligne restait Overfull de 32.65pt (mesure par
            # compilation reelle, verifiee par rendu d'image : le
            # debordement mange le blanc inter-colonnes sans chevaucher le
            # texte de la colonne voisine, mais reste plus large que
            # souhaitable). \sloppypar assouplit localement la tolerance de
            # justification (espaces inter-mots plus elastiques) au lieu de
            # laisser une boite deborder -- mise en page seulement, aucun
            # mot ni caractere du texte n'est modifie. Limite a cette seule
            # section pour ne pas relacher la justification ailleurs.
            backmatter_fragments.append("\\begin{sloppypar}")
            backmatter_fragments.extend(paragraphs_to_latex(direct_lines))
            for subtitle, body in subsecs:
                backmatter_fragments.append("\\textbf{%s}" % convert_inline(subtitle))
                backmatter_fragments.extend(paragraphs_to_latex(body))
            backmatter_fragments.append("\\end{sloppypar}")
            backmatter_fragments.append("\\end{openscience}")
            continue
        if number == "10":
            backmatter_fragments.append("\\begin{ai}")
            backmatter_fragments.extend(paragraphs_to_latex(direct_lines))
            for subtitle, body in subsecs:
                backmatter_fragments.append("\\textbf{%s}" % convert_inline(subtitle))
                backmatter_fragments.extend(paragraphs_to_latex(body))
            backmatter_fragments.append("\\end{ai}")
            continue

        # --- ANNEXE ou CORPS ---
        # Meme rendu (\section + \subsection) dans les deux cas ; seule la
        # zone de destination change. Sous \appendix, LaTeX renumerote ces
        # \section en lettres (A, B, C...) tout seul : le Markdown n'a pas a
        # porter la lettre, et l'ordre des sections d'annexe dans le fichier
        # source suffit a fixer leur lettre.
        cible = appendix_fragments if marker_seen else body_fragments
        if marker_seen:
            sections_after_marker += 1
        cible.append("\\section{%s}" % convert_inline(title))
        cible.extend(paragraphs_to_latex(direct_lines))
        for subtitle, body in subsecs:
            cible.append("\\subsection{%s}" % convert_inline(subtitle))
            cible.extend(paragraphs_to_latex(body))

    # GARDE-FOU : un marqueur pose mais suivi d'aucune section est presque
    # surement une erreur de redaction (marqueur place en dernier, ou section
    # d'annexe supprimee sans retirer le marqueur). On le signale plutot que
    # de rendre une zone annexe vide en silence -- sans echouer pour autant :
    # une zone annexe vide ne casse rien a la compilation, contrairement a une
    # figure manquante.
    if marker_seen and sections_after_marker == 0:
        print(
            "AVIS : marqueur d'annexe '## %s' trouve, mais aucune section ne "
            "le suit -- la zone GENERATED:APPENDIX est emise vide. Verifier "
            "que le marqueur n'est pas place apres la derniere annexe."
            % APPENDIX_MARKER, file=sys.stderr)

    return abstract_fragments, body_fragments, appendix_fragments, backmatter_fragments


def _splice(text, begin_marker, end_marker, new_inner, path):
    """Remplace le contenu entre deux marqueurs GENERATED. Echoue bruyamment
    si l'un des deux manque, plutot que d'ecrire main.tex sans la zone (une
    zone absente ne se verrait qu'au PDF -- ou, pour l'annexe, pas du tout :
    le document compilerait sans ses annexes, en silence)."""
    try:
        i = text.index(begin_marker) + len(begin_marker)
        j = text.index(end_marker, i)
    except ValueError:
        sys.exit(
            "ERREUR : zone generee introuvable dans %s -- marqueur manquant :\n"
            "  %s\n  %s\n"
            "Arret plutot que d'ecrire un main.tex ampute de cette zone."
            % (path, begin_marker, end_marker))
    return text[:i] + "\n" + new_inner + "\n" + text[j:]


def main():
    global BIB_KEYS
    BIB_KEYS = load_bib_keys(BIB_SRC_PATH)

    shutil.copyfile(BIB_SRC_PATH, BIB_DST_PATH)

    short_title, full_title = load_manuscript_title()

    src = open(MANUSCRIPT_PATH, encoding="utf-8").read()
    sections = parse_sections(src)
    (abstract_fragments, body_fragments,
     appendix_fragments, backmatter_fragments) = route_sections(sections)

    # A ce point, le parcours des sections a rempli REFERENCED_FIGURES via
    # chaque appel a render_figure_block() -- on synchronise maintenant les
    # figures AVANT de toucher a main.tex, pour qu'un echec (figure absente,
    # vide, ou copie corrompue) laisse main.tex intact plutot que de le
    # regenerer sur une base perimee.
    sync_figures()

    abstract_tex = "\n\n".join(abstract_fragments)
    body_tex = "\n\n".join(body_fragments)
    appendix_tex = "\n\n".join(appendix_fragments)
    backmatter_tex = "\n\n".join(backmatter_fragments)

    main_tex = open(MAIN_TEX_PATH, encoding="utf-8").read()

    # Titre : pas une zone GENERATED (le \title acmart doit rester sur sa
    # propre ligne, hors des trois zones marquees), donc substitution directe
    # de la ligne \title[...]{...} plutot qu'un splice entre marqueurs.
    # GARDE-FOU : si cette ligne n'existe plus (main.tex restructure), on
    # echoue bruyamment plutot que d'inserer un \title a l'aveugle quelque
    # part, ou de laisser silencieusement l'ancien titre en place.
    if not _TITLE_LINE_RE.search(main_tex):
        sys.exit(
            "ERREUR : aucune ligne \\title[...]{...} trouvee dans %s -- "
            "arret plutot que d'inserer le titre a l'aveugle ou de laisser "
            "l'ancien titre en place sans le signaler." % MAIN_TEX_PATH
        )
    new_title_line = "\\title[%s]{%s}" % (short_title, full_title)
    # repl est une fonction (pas une chaine) : re.sub n'interprete alors aucun
    # \1 / \g<...> dans la valeur de retour, donc les backslashes LaTeX du
    # titre converti (\%, \_, \S, etc.) passent tels quels, sans double
    # echappement.
    main_tex = _TITLE_LINE_RE.sub(lambda m: new_title_line, main_tex, count=1)

    def splice(text, zone, new_inner):
        return _splice(
            text,
            "%% === GENERATED:%s BEGIN (auto -- regenerated by md2latex.py, do not hand-edit) ===" % zone,
            "%% === GENERATED:%s END ===" % zone,
            new_inner,
            MAIN_TEX_PATH,
        )

    main_tex = splice(main_tex, "ABSTRACT", abstract_tex)
    main_tex = splice(main_tex, "BODY", body_tex)
    main_tex = splice(main_tex, "APPENDIX", appendix_tex)
    main_tex = splice(main_tex, "BACKMATTER", backmatter_tex)

    open(MAIN_TEX_PATH, "w", encoding="utf-8").write(main_tex)

    # ---- rapport de diagnostic sur stderr ----
    print("=== md2latex.py : rapport de conversion ===", file=sys.stderr)
    if UNRESOLVED_CITATIONS:
        print("CITATIONS NON RESOLUES (%d) :" % len(UNRESOLVED_CITATIONS), file=sys.stderr)
        for key, ctx in UNRESOLVED_CITATIONS:
            print("  - %r  (contexte: ...%s...)" % (key, ctx.replace("\n", " ")), file=sys.stderr)
    else:
        print("Toutes les citations du manuscrit ont ete reliees a une entree de references.bib.", file=sys.stderr)
    if SPECIAL_CHARS_SEEN:
        print("CARACTERES NON MAPPES SUBSISTANT EN SORTIE (a verifier avant depot) :", file=sys.stderr)
        for ch, cnt in sorted(SPECIAL_CHARS_SEEN.items(), key=lambda x: -x[1]):
            print("  - %r (U+%04X) x%d" % (ch, ord(ch), cnt), file=sys.stderr)
    else:
        print("Aucun caractere unicode non mappe detecte en sortie.", file=sys.stderr)
    if PREDICTIONS_TABLE_RENDER_COUNT == 1 and OTHER_TABLE_RENDER_COUNT == 0:
        print(
            "Renvois \"Table N\" -> \\ref{tab:predictions} : hypothese verifiee "
            "(un seul tableau dans le document).", file=sys.stderr)
    else:
        print(
            "ATTENTION : %d tableau(x) de predictions et %d autre(s) tableau(x) "
            "rendus -- l'hypothese \"un seul tableau\" de _convert_table_refs() "
            "ne tient plus. Tout renvoi \"Table N\" du manuscrit a ete remplace "
            "par \\ref{tab:predictions} SANS DISTINCTION -- verifier a la main "
            "que chaque renvoi cible bien le bon tableau, et adapter "
            "_convert_table_refs() pour distinguer les cibles."
            % (PREDICTIONS_TABLE_RENDER_COUNT, OTHER_TABLE_RENDER_COUNT), file=sys.stderr)
    # Frontiere corps / annexe : c'est le chiffre qui decide du respect de la
    # limite de 12 pages, donc il est imprime a chaque execution plutot que
    # d'etre a retrouver dans le .tex.
    n_annexes = sum(1 for f in appendix_fragments if f.startswith("\\section{"))
    if n_annexes:
        print(
            "Zone annexe : %d section(s) emise(s) apres \\appendix, HORS du "
            "decompte des 12 pages du corps (marqueur '## %s')."
            % (n_annexes, APPENDIX_MARKER), file=sys.stderr)
    else:
        print(
            "Zone annexe : vide (aucun marqueur '## %s' dans le manuscrit) -- "
            "tout le contenu hors sections obligatoires compte dans le corps."
            % APPENDIX_MARKER, file=sys.stderr)
    print("main.tex regenere : %s" % MAIN_TEX_PATH, file=sys.stderr)


if __name__ == "__main__":
    main()
