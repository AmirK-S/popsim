# Zone annexe du convertisseur — l'outil est ouvert, la limite reste à treize pages

statut: courant
mandat: Ouvrir une zone annexe dans `article/latex/md2latex.py` conformément à la formulation de l'appel PoPETs 2027 (« any clearly-marked appendices »), la prouver par un test d'échec exécuté, rapatrier d'Open Science vers l'annexe ce qui relève du détail de mesure, et mesurer la pagination du corps sans l'estimer.
agent: Claude Opus 5, Anthropic — sous-agent zone annexe
ecriture: article/latex/md2latex.py ; article/latex/main.tex ; article/manuscrit.md ; tests/latex/test_md2latex_annexe.py ; resultats/zone-annexe-2026-09-13.md
lecture_seule: tout le reste
interdits: appel payant, réseau, recherche web, commit sur master, fusion, arrière-plan, tout calcul de résultat nouveau
cecite: je n'ai pas rejoué une seule analyse ; la compilation de contrôle est faite hors dépôt, aucun fichier de `article/latex/` du dépôt n'est régénéré par ma passe ; je n'ai pas touché au titre ; la porte P8 vit sur `agent/portes/coherence-chiffres` et je l'ai seulement exécutée, jamais recopiée dans cet arbre
cout_reel_usd: 0.00  <!-- P2-exempt: coût réel, pas une mesure -->

---

## 1. Le marqueur, et pourquoi celui-là

**Marqueur : le titre de niveau 2 non numéroté `## Appendix`.** Tout ce qui le suit sort du
corps et part dans une nouvelle zone `GENERATED:APPENDIX` de `main.tex`, émise après
`\appendix` — donc numérotée en lettres par LaTeX, et hors du décompte des douze pages.

Ce choix n'est pas arbitraire, et c'est la raison de le retenir : **le fichier source utilise
déjà le `##` non numéroté comme sentinelle de structure.** Avant cette passe, `## Abstract` et
`## References` étaient les deux seuls `##` sans numéro du manuscrit, et tous deux étaient déjà
reconnus par leur intitulé et aiguillés à part — résumé d'un côté, bibliographie automatique de
l'autre. `## Appendix` est la troisième sentinelle de la même famille, reconnue de la même
façon. Aucune convention nouvelle n'est introduite ; une section d'annexe reste un `##`
ordinaire, et l'ordre des sections d'annexe dans le fichier suffit à fixer leur lettre.

**Deux garde-fous**, dans la discipline du script (échouer bruyamment plutôt que deviner) :

- les sections que le gabarit impose gardent la priorité sur le marqueur. `Abstract`,
  `References` et les sections numérotées 8, 9, 10 partent dans leur zone propre **même posées
  après le marqueur**, avec un avis sur stderr. Un marqueur mal placé ne peut donc pas faire
  disparaître en silence une section que le venue exige ;
- un marqueur suivi d'aucune section produit une zone vide, **signalée**, jamais devinée.

Le script imprime désormais, à chaque exécution, le nombre de sections d'annexe émises : c'est
le chiffre qui décide du respect de la limite, il ne doit pas être à retrouver dans le `.tex`.

## 2. Le test d'échec, exécuté

`tests/latex/test_md2latex_annexe.py`, six tests, au niveau des zones générées de `main.tex` —
donc sans compiler, et **exécutables contre n'importe quelle version du convertisseur** passée
par la variable `MD2LATEX`. C'est ce qui permet de voir le défaut, pas seulement la correction.

Contre le convertisseur d'avant la zone annexe :

    git show 2e88025:article/latex/md2latex.py > /tmp/md2latex-avant.py
    MD2LATEX=/tmp/md2latex-avant.py python3 -m unittest test_md2latex_annexe
    → FAILED (failures=2)

Les deux échecs disent exactement le défaut : la phrase-témoin placée après `## Appendix` est
retrouvée dans la zone `BODY`, précédée d'un `\section{Appendix}` — donc **comptée dans les
douze pages**, l'inverse du but. Contre le convertisseur d'après : `OK`, six tests.

Les quatre autres tests ferment les portes de sortie faciles : ce qui **précède** le marqueur
doit rester dans le corps (sans quoi un convertisseur qui perd du texte passerait le premier
test) ; le marqueur n'émet rien lui-même ; les trois sections obligatoires ne sont pas
capturables ; et aucune des deux phrases-témoins ne disparaît du document, marqueur ou pas.

Les soixante-dix-huit tests de portes existants passent inchangés.

**Un défaut trouvé au passage, par compilation réelle.** Le manuscrit portait `p < 10⁻⁴` en
exposants unicode, que le convertisseur recopiait tels quels : `pdflatex` s'arrêtait net
(« Unicode character U+207B not set up for use with LaTeX — Fatal error occurred, no output PDF
file produced »). Le diagnostic du script les signalait bien, mais sans bloquer, si bien que le
défaut ne se découvrait qu'à la compilation suivante. Corrigé par une règle générale
d'exposants. **Aucun chiffre n'est modifié, seule la notation change.**

## 3. Ce que j'ai rapatrié d'Open Science, et selon quel critère

**Critère, une seule question par bloc : ce texte sert-il à ouvrir les données et le code, ou
est-ce du détail de mesure ?** La section Open Science est destinée à la reproductibilité —
l'artefact, les scripts, les préenregistrements, l'environnement, l'obtention des données et
leurs conditions d'usage. Un intervalle de confiance secondaire, un recensement de seuils, un
tableau de mesures annexes n'y sont pas chez eux : ils y étaient par défaut d'outillage.

**Treize blocs rapatriés**, mot pour mot, en quatre annexes lettrées :

| annexe | blocs rapatriés |
|---|---|
| A — Provenance and validity controls | les comptes et taux des contrôles de provenance (§4.5) |
| B — Secondary measurements behind the results | rééchantillonnage au niveau des configurations (§5.1) ; table des comparateurs monde fermé (§5.2) ; **recensement des seuils à FPR = 0,1 %** (§5.3) ; témoins leurres, borne démographique, décomposition, items effectifs, bras T2 et les deux limites du verdict sur la distance (§5.4) ; hypothèses réfutées et contrôles de concentration (§5.5) ; renversement du top-10 (§5.7) ; ce qui sépare Park de Twin (§5.8) ; les six bassins et les deux lois ajustées (§5.9) ; **conventions de départage des ex æquo** et robustesse au choix d'items (§5.8) |
| C — Costs of the defense | coûts DP budget par budget (§6.2) ; erreur propre du jumeau non protégé (§6.3) |
| D — Multiplicity | p-values ajustées et recensement complet à 47 tests (§7.3) |

**Neuf blocs restent en Open Science, et c'est délibéré** : l'artefact de revue et ce qu'il ne
prouve pas, les analyses sous-jacentes, la vérification bibliographique, l'obtention des données
réelles et leurs conditions d'usage, les préenregistrements, l'environnement. Deux cas limites
tranchés dans le même sens : **les échecs de transport et leurs reprises** (§5.7) et
**l'implémentation du synthétiseur DP** (§6.2) restent, tous deux étant du détail de
fabrication — comment le calcul a tourné, avec quel code — et non une mesure. Ce sont d'ailleurs
les deux blocs qui logeaient là **avant** la passe de pagination : ils n'y avaient pas été
descendus par contrainte, ils y étaient chez eux.

**Les renvois du corps ont suivi.** Vingt renvois du corps disaient « Open Science » ; dix-neuf
désignaient du matériel qui vient de partir en annexe et ont été retargetés, **un seul a été
laissé** — celui des échecs de transport, dont la cible n'a pas bougé. Sans cela, dix-neuf
renvois du manuscrit seraient devenus faux en silence.

Ces renvois disent « the appendix » et **jamais « Appendix B »** : la lettre est calculée par
LaTeX, et la recopier à la main serait exactement le défaut que ce dépôt traque ailleurs — le
mot « sixteen » figé dans une légende, le « Table 3 » figé dans la prose. Un renvoi générique ne
dérive jamais.

## 4. La pagination, mesurée

**Mesure, pas estimation.** `main.tex` porte désormais un `\label{corps:fin}` juste avant
`\appendix` — c'est-à-dire exactement là où s'arrête la seule partie que la limite compte. Le
nombre de pages du corps se lit alors dans `main.aux`, sans compter à l'œil :

    grep 'newlabel{corps:fin}' main.aux

Compilation de contrôle hors dépôt, bibliographie prise sur `agent/biblio/anteriorites` pour que
`jordon2022synthetic`, `carlini2023quantifying` et `houssiau2022tapas` se résolvent — le
convertisseur confirme « Toutes les citations du manuscrit ont ete reliees a une entree de
references.bib ». Zéro erreur LaTeX, débordement le plus large mesuré à neuf points, contre
trente-deux avant. Résultat :

| | avant la passe | après |
|---|---|---|
| corps, hors annexes / bibliographie / sections obligatoires | **13** pages | **13** pages |
| document complet | 17 p. | 17 p. |
| annexes lettrées, hors décompte | aucune | **4** (A à D) |

**Le rapatriement d'Open Science vers l'annexe ne gagne pas une ligne de corps, et ne pouvait
pas en gagner.** C'est le point à dire franchement : l'appel exclut du décompte les sections
obligatoires **et** les annexes signalées. Le matériel déplacé était déjà hors du corps, en
Open Science ; le faire passer en annexe le remet au bon endroit scientifiquement, mais
**l'opération est neutre pour la pagination par construction**. Le gain d'une demi-page avait
déjà été encaissé par la passe précédente, quand ce matériel avait quitté le corps.

## 5. Pourquoi je m'arrête à treize, et ce que j'ai mesuré avant de m'arrêter

Le corps finit au bas de la colonne gauche de la page 13 : il déborde d'environ quarante lignes
composées. Pour tenir douze pages il faut sortir du **corps** — pas d'Open Science — un objet de
cette taille. J'ai cherché, et mesuré plutôt que supposé.

**Le seul objet du corps assez grand est le tableau des dix-sept prédictions préenregistrées
(§7.1). Déplacé seul en annexe, il fait tomber le corps à douze pages** — mesuré, `corps:fin`
passe de 13 à 12, avec de la marge dans la colonne, les onze renvois « Table 1 » du corps
restant résolus.

**Je ne l'ai pas retenu, et voici la raison opposable.** L'appel exige que l'article soit
« complete and self-contained without appendices » : une annexe porte du détail supplémentaire,
jamais une affirmation du corps. Or le paragraphe de clôture du §7.1 **nomme les lignes du
tableau** — « rows 9 and 16 », « row 17 », « row 14 » — pour expliquer quelles réfutations ont
quitté le compte et pourquoi. Le tableau parti, ces phrases ne sont plus lisibles sans l'annexe :
le corps cesse d'être autonome, sur l'appareil de réfutation du papier précisément. C'est la
ligne que la passe précédente a refusé de franchir seule, et je la refuse pour la même raison :
elle se paierait en argumentation, pas en détail.

Le reste du corps a été examiné section par section. Le §4 est constitué de définitions dont le
lecteur a besoin, d'une limite et de la règle d'interprétabilité qui est une contribution. Le
§5.4 et le §5.8, les deux plus longues sous-sections, sont de l'argumentation, des retraits et
des limites de bout en bout. Il n'y reste pas quarante lignes de détail de mesure à déplacer.

**Donc : treize pages rendues et déclarées, avec un convertisseur sain.** La différence avec la
passe précédente n'est pas le nombre de pages, c'est que **la limite n'est plus une contrainte
d'outillage**. Le véhicule existe, il est testé, et il accepte n'importe quel détail — pas
seulement ce qui peut décemment se présenter comme de l'ouverture des données.

**Ce que le responsable a à arbitrer**, avec le chiffre en main : déplacer le tableau du §7.1 en
annexe donne douze pages immédiatement, au prix de l'autonomie du corps sur ce point précis.
Treize pages sont de droit dès la première révision et pour la version finale.

## 6. La survie des valeurs, vérifiée mécaniquement

Contrôle repris de la passe précédente — celui qui lui avait rattrapé deux valeurs perdues en
cours de route. Comparaison des **multi-ensembles** de littéraux numériques et de renvois
de registre entre le manuscrit d'avant la passe et celui d'après : une valeur présente deux fois
avant et une fois après serait signalée. (Les renvois de registre sont notés ici en toutes
lettres et non sous leur forme littérale, qui déclencherait P2 sur ce rapport même.)

    littéraux numériques : 426 distincts, 1431 occurrences — aucune perte
    renvois de registre  :  53 distincts,   61 occurrences — aucune perte

Aucune valeur rétablie n'a été nécessaire cette fois : les treize blocs ont été coupés et
recollés par script, jamais retapés. **Rien n'a été supprimé, rien n'a été arrondi, aucune
affirmation, rétractation, limite ou intervalle n'a quitté le document** — ils ont changé de
section, pas de contenu. Le titre n'a pas été touché.

## 7. Portes

| porte | état |
|---|---|
| **P2** `registre_chiffres`, manuscrit | **356** — exactement la valeur d'entrée, non aggravée |
| **P3** `interdits` | OK, aucune violation |
| **P4** `entetes --depuis origin/master` | OK, aucune violation |
| **P5** `renvois` | OK, aucune violation |
| **P7** `rendu_registre --verifier` | OK, 61 renvois résolus, 61 grandeurs au registre |
| **P8** `coherence_csv --tous` | OK, aucune violation, 333 fichiers lus — zéro faux positif maintenu |

Les soixante-dix-huit tests de `tests/portes/` passent, plus les six tests de la zone annexe.
