# Renvois internes et notes bibliographiques : nettoyage avant dépôt

statut: courant
mandat: traiter les 48 (en réalité 50) renvois `[c7-xxx-resultats.md §N]` imprimés dans le corps du PDF et les notes bibliographiques internes de `article/references.bib`, signalés au §12.5 de `resultats/latex-gabarit-2026-09-12.md`, sans changer aucun chiffre ni aucune affirmation
agent: Claude Sonnet 5, Anthropic
ecriture: article/manuscrit.md, article/references.bib, resultats/renvois-internes-2026-09-12.md
lecture_seule: tout le reste
interdits: appel payant sans GO, réseau, commit sur master, arrière-plan
cecite: je n'ai pas recompilé `article/latex/main.tex` en place — ce répertoire est modifié en ce moment même par un autre agent (`git status` en tête de session le montrait déjà modifié dans l'arbre de travail partagé) et reste hors de mon périmètre d'écriture. J'ai vérifié le compte de pages dans une copie isolée du répertoire de compilation, sous mon répertoire scratch, construite à partir de l'état exact de `article/latex/` au moment où j'ai commencé (donc potentiellement légèrement en aval de la version que l'autre agent finira par committer) — la mécanique de conversion elle-même n'a pas été touchée par mon travail.
cout_reel_usd: 0

## 1. Ce qui a déclenché ce travail

`resultats/latex-gabarit-2026-09-12.md` §12.5 signalait, en fin de finalisation du PDF de
soumission, deux défauts de forme trouvés en vérifiant le rendu (pas le Markdown) : (1) des
renvois internes `[c7-xxx-resultats.md §N]` imprimés tels quels dans le corps, exposant
l'arborescence de fichiers internes du dépôt dans un article qui doit rester anonyme et fini ;
(2) 7 des 13 notes `note={}` de `article/references.bib` qui sont des annotations de vérification
interne (parfois en français) plutôt que des précisions bibliographiques.

## 2. Les renvois internes : 50 trouvés, pas 48

Un comptage exhaustif par expression régulière (`\[[^\[\]]*\.md[^\[\]]*\]` sur
`article/manuscrit.md`) trouve **50** occurrences, pas 48. L'écart n'est pas expliqué par une
erreur de méthode de ma part que j'aurais pu identifier : le rapport du §12.5 dit lui-même que
le manuscrit a été modifié entre deux passes par un autre agent au cours de la même session ; ces
deux renvois supplémentaires sont probablement apparus après la dernière relecture qui a produit
le chiffre 48. Je traite les 50, pas seulement 48.

**Vérification individuelle des 50** (voir le détail ligne par ligne dans l'historique de
`git diff` de ce commit) : chacun d'entre eux, sans exception, se trouve à la fin d'une phrase
qui **étaye une affirmation quantitative ou méthodologique** avec un fichier d'analyse du dépôt
(mesure, script, journal de reconciliation) — aucun n'est purement interne (note à nous-mêmes
sans rapport avec le texte), et aucun ne désigne une section du présent article (ces renvois-là
existent déjà séparément, sous la forme `(§5.4)` etc., et n'ont pas été touchés). Le critère de
la mission — « que gagne le lecteur ? » — donne donc la même réponse pour les 50 : ils doivent
pointer vers quelque chose d'accessible, pas disparaître silencieusement.

**Décision appliquée aux 50** : suppression du chemin de fichier individuel dans le corps
(aucune affirmation touchée, seule la forme du renvoi change), et ajout d'une phrase générique
unique dans la section 9 « Availability » (hors limite des 12 pages, donc sans coût de place) :

> **Underlying analyses.** Every quantitative claim in this paper corresponds to a dated analysis
> script and result file under `resultats/` in this repository, organised to mirror the paper's
> own section numbering; individual file names are not cited in the text, to keep the manuscript
> readable.

C'est la formulation générique que la mission demandait plutôt que « quarante-huit [maintenant
cinquante] chemins de fichiers » : le lecteur apprend que chaque chiffre est traçable et où
chercher, sans voir la mécanique de travail interne (dates, noms de fichiers `c7-*`) dans le
corps du texte.

Aucun des 50 ne tombait dans les deux autres catégories prévues par la mission (« ne sert qu'à
nous » ou « désigne une section du présent article ») : je n'ai donc rien simplement effacé sans
compensation, et rien converti en renvoi `§N` interne.

## 3. Notes bibliographiques : les 7 signalées, retirées ; les 6 autres, intactes

Les 7 notes identifiées au §12.5 comme des annotations de vérification interne ont été retirées
du champ `note={}` de leur entrée respective dans `article/references.bib` (rien d'autre touché
dans ces entrées — auteurs, titre, année, doi, eprint restent identiques) :

- `shafieinejad2026diffusion` — note retirée (identifiait la clé provisoire utilisée avant
  vérification ; sans objet pour le lecteur, l'entrée finale est déjà correcte).
- `gouweleeuw1998pram` — note retirée. **Information à conserver pour nous, pas pour le
  lecteur** : la note disait « aucun DOI retrouvé ; référence vérifiée via le texte intégral
  (scb.se), à confirmer avant dépôt ». Ce point reste un TODO réel et ouvert (déjà signalé
  ailleurs : `article/manuscrit.md` §References et `article/references-verification.md`) — il ne
  disparaît pas du dossier, seulement de la bibliographie imprimée, ce qui est la bonne place
  pour une note « à confirmer avant dépôt » qui n'a rien à faire dans un dépôt soumis.
- `drechsler2024thirtyyears` — note retirée (documentait une correction d'identifiant déjà
  reflétée dans les champs `eprint` de l'entrée finale ; aucune perte pour le lecteur).
- `hu2023microdata` — note retirée (documentait une correction d'ordre des auteurs déjà reflétée
  dans le champ `author` de l'entrée finale ; aucune perte).
- `dwork2015robust` — note retirée (documentait une correction d'identifiant ; l'absence de champ
  `eprint` sur cette entrée, contrairement à la plupart des autres, indique déjà au lecteur
  qu'elle est citée via les actes FOCS plutôt que via arXiv).
- `guepin2023synthetic` — note retirée (documentait une correction de coauteurs déjà reflétée
  dans le champ `author` de l'entrée finale ; aucune perte).
- `aapor2026responsibleai` — note retirée. Elle mêlait une précision possiblement utile
  (mandat du AAPOR Task Force, adopté par le AAPOR Executive Council) et une note de vérification
  interne (date de création du PDF confirmée par métadonnées) ; par prudence je l'ai retirée en
  bloc plutôt que de la retailler, conformément à la consigne « si l'information mérite d'être
  conservée pour nous, mets-la dans ton rapport, pas dans la bibliographie » — donc consignée ici
  seulement : ce rapport AAPOR est bien un document de tâche officiel, commandité et validé par
  l'Executive Council de l'AAPOR, pas une opinion isolée.

Les 6 autres notes (`chen2026syntheticusers`, `park2024agents`, `peng2026funhouse`,
`das2024blind`, `zhang2024satml`, `bun2014fingerprinting`) sont des précisions bibliographiques
usuelles en anglais (statut de preprint, titre de version antérieure, double publication, nature
de « position paper ») — laissées inchangées, comme demandé.

**Contrôle final** : `grep -o 'note={[^}]*}' article/references.bib` ne renvoie plus que ces 6
notes ; aucune n'est en français. Les seules mentions en français restantes dans le fichier sont
des commentaires `%` d'en-tête (documentation du fichier, jamais typesetés par BibTeX) — hors du
périmètre de la consigne, qui vise les notes imprimées.

## 4. Les 42 clés se résolvent toujours

Extraction automatique de toutes les clés citées entre crochets dans `article/manuscrit.md`
(motif `[clé1, clé2]`, en excluant les renvois de fichiers `.md` et les intervalles numériques
`[a ; b]`) contre les 47 clés de `article/references.bib` : **42 clés citées, 0 manquante**. Les
5 entrées non citées formellement (`ahn2026itemmean`, `wang2026digitaltwins`,
`chen2026syntheticusers`, `choi2026beyondmean`, `guan2024zakmia`) sont un état antérieur déjà
connu (mentionnées en prose sans clé `\cite{}` formelle, ou vérification de veille
d'antériorité) — je n'y ai pas touché, hors de mon mandat. Le script `md2latex.py`, rejoué sur
une copie isolée avec le manuscrit corrigé, confirme indépendamment 0 citation non résolue et 0
caractère Unicode non mappé.

## 5. Compte de pages : vérifié, inchangé, marge toujours nulle

Recompilation complète (`python3 md2latex.py` puis
`pdflatex → bibtex → pdflatex → pdflatex`) dans une copie isolée du répertoire de compilation
(pas dans `article/latex/` lui-même, hors de mon périmètre d'écriture et actuellement modifié par
un autre agent) : **15 pages au total, « Ethical Considerations » commence toujours page 12,
page rendue et regardée (pas seulement chercher le mot dans le texte extrait)** — la page 12
contient encore la fin de §7.3 et tout §7.4 avant que la section obligatoire ne commence, donc le
corps est encore et toujours **12 pages sur 12**, comme avant ce travail. J'ai reconstruit en
parallèle, dans le même environnement, le PDF de l'état d'avant mes modifications (commit
`04ae7b6`) : identique — 15 pages, « Ethical Considerations » page 12. **Le retrait des 50
renvois n'a ni fait déborder, ni gagné de page** ; il a seulement réduit le nombre de mots à
l'intérieur d'une pagination qui ne bouge pas.

## 6. Solde net en mots

Corps du manuscrit (Résumé à la fin de §7.4, avant « Ethics Considerations ») :
- avant : 11 577 mots
- après : 11 503 mots
- **solde net : −74 mots** (aucune phrase raccourcie sur le fond ; uniquement les 50 chemins de
  fichiers retirés du texte, à raison d'un à quatre mots chacun selon le nom de fichier).

La phrase générique ajoutée en section 9 (« Underlying analyses… ») ne compte pas dans ce solde :
elle se trouve après « Ethics Considerations », donc hors de la limite des 12 pages.

## 7. Rien qui ferait perdre une information au lecteur

Aucun des 50 renvois retirés ne portait, dans son chemin de fichier ou son numéro de section, une
information que le lecteur perdrait : le nom de fichier interne (`c7-attaquant-fort-resultats.md
§N`) n'est significatif que pour nous, jamais pour un lecteur externe sans accès au dépôt de
travail — c'est précisément le problème signalé au §12.5. Le seul point où une information
méritait d'être préservée plutôt que simplement supprimée est la note `gouweleeuw1998pram`
(absence de DOI, à confirmer) : signalé au §3 ci-dessus, pas perdu.
