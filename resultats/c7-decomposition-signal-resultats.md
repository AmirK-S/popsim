# C7, décomposition du signal de ré-identification en population / segment / personne — résultats (13 septembre 2026)

statut: courant
mandat: Trancher l'objection R4 de `resultats/relecture-post-nuit-2026-09-13.md` — quelle part des 20,7 % de ré-identification est une propriété de *cette personne*, plutôt qu'une structure de population qu'un modèle de langage reproduit bien sur un bloc produit × prix. Décomposer le taux en trois niveaux, construire le témoin à segment constant, et rendre le verdict contre le seuil préenregistré.
agent: Claude Opus 5, Anthropic — sous-agent décomposition du signal
ecriture: analyses/c7_decomposition_signal.py, resultats/c7-decomposition-signal-preenregistrement.md, resultats/c7-decomposition-signal-resultats.md, resultats/c7-decomposition-signal.csv
lecture_seule: tout le reste du dépôt
interdits: appel payant, réseau, recherche web, arrière-plan, commit sur master, fusion, écriture dans article/manuscrit.md, impression de tout identifiant / réponse / appariement individuel
cecite: je n'ai pas lu article/manuscrit.md (propriété d'un autre agent) ; je n'ai pas pu lire le *prompt* exact de la configuration « Demographics Only » — l'archive publie ses sorties, pas son gabarit d'entrée —, ce qui borne la section 3 et y est déclaré ; je ne sais pas si « items d'achat » et « items binaires » désignent la même partition, un autre agent l'examine et je n'affirme rien sur la cause de la concentration
cout_reel_usd: 0.00

---

## 0. Le verdict, en tête, avant tout détail

**Le seuil décisif préenregistré n'est pas franchi, et il ne l'est pas de peu.** À segment
constant — pool de candidats restreint au propre segment de la cible —, le jumeau JSON Persona
GPT-4.1 retrouve **sa** personne plutôt qu'une autre personne du **même** segment avec une AUC
de **0,9076** [0,8990 ; 0,9150], contre 0,50 pour l'absence de trace. Le seuil sous lequel
j'avais préenregistré que l'article devait changer de nature était une borne basse à 0,55.
L'avantage ne disparaît pas à segment constant ; il n'en perd presque rien.

**Et la mécanique que le relecteur propose est mesurée nulle.** Un vecteur de réponses
**humain réel**, celui d'une autre personne — donc une structure de dépendance inter-items
parfaitement réaliste, et zéro information sur la cible — obtient un top-1 de **0,00 %**
[0,00 ; 0,00] et une AUC à segment constant de **0,4995** [0,4868 ; 0,5124]. Le réalisme de la
structure des réponses, à lui seul, n'identifie personne. C'est le témoin le plus dur qu'on
puisse opposer à l'objection, et il est exactement au hasard.

**Mais une prédiction préenregistrée est réfutée, et c'est le résultat le plus utile du
document.** Le jumeau « Demographics Only » n'est **pas** l'objet de groupe que l'objection
suppose. Le bloc *Demographics* du catalogue compte 14 questions dont les réponses jointes
prennent **2 055 valeurs distinctes pour 2 058 personnes** : c'est un quasi-identifiant, pas
un segment. Ses 2,15 % ne peuvent donc pas être portés au crédit du niveau segment sans
surestimer massivement celui-ci — et l'article ne doit plus le présenter comme un jumeau « qui
ne contient par construction aucune information individuelle ».

---

## 1. Le bassin, la convention, et ce qui est tenu constant

**Bassin strictement constant partout** : 2 058 personnes attaquées, 2 058 candidats, les
60 items de `c7_reidentification.items_communs` (dont 40 de suffixe `_Q295`), attaque
`rangs_attaque` importée sans réimplémentation, graine **20260913**, IC par bootstrap sur les
**personnes** (2 000 tirages). Hasard top-1 = 1/2 058 = **0,0486 %**.

**Segmentation S_gra** (genre × ethnicité × âge, la lecture principale du dépôt) : **40
segments**, aucune personne non affectée, tailles de 1 à 259, taille médiane **pondérée par
les personnes** de 124. **Un** segment est un singleton : la personne qui s'y trouve n'a aucun
rival et est exclue des agrégats à segment constant, qui portent donc sur **2 057** personnes.
C'est écrit au CSV (`n_avec_rival`).

**Une valeur du préenregistrement est ici légèrement différente, et je le déclare plutôt que
de la réécrire.** Le §1 du préenregistrement annonce `E[1/|S_gra|]` = **1,944 %**, moyenne
prise sur les 2 058 personnes. Le calcul du présent rapport exclut la personne du segment
singleton, pour laquelle `1/|seg|` vaut 1 et qui n'a de toute façon aucun rival : la même
espérance sur les 2 057 personnes restantes vaut **1,896 %**. Aucun chiffre du
préenregistrement n'est corrigé ; c'est le périmètre qui change. Le sens du changement joue
**en faveur** de l'article — un plafond de segment plus bas fait une marche de segment plus
petite — et c'est pourquoi il ne sert de headline nulle part : la part publiée au §5 est celle
de l'attribution la plus **défavorable** (2,153 %), qui ne dépend pas de cette valeur. Avec
1,944 % au lieu de 1,896 %, la part personne de cette ligne passe de 90,8 % à 90,6 % sur
l'échelle des taux : le verdict ne bouge pas.

**Convention d'ex æquo, déclarée.** Tous les top-1 emploient la convention du dépôt : départ
aléatoire moyenné sur 20 tirages, graine fixée. Le dépôt a mesuré que cette convention vaut un
facteur **1,32 sur Twin** et jusqu'à **130** sur d'autres jeux
(`c7-residu-trajectoire-resultats.md` §7) ; aucun top-1 n'est publié ici sans elle.
**L'AUC à segment constant compte les ex æquo une demi-unité** et ne dépend d'aucun tirage,
d'aucune graine et d'aucune convention : c'est pourquoi c'est elle, et non le top-1, qui porte
le verdict.

**Contrôle d'interprétabilité.** `c7_controle_interpretabilite.controle_avant_interpretation`
a été appelé avant toute interprétation, baseline recalculée par la fonction sur le bassin
réellement attaqué. Le jumeau persona **passe**. Les trois générateurs de plancher (marginales
de population, vecteur humain d'une autre personne, vecteur humain du même segment)
**échouent** — ce n'est pas un incident, c'est leur définition : ce sont des planchers, et un
plancher qui passerait le contrôle ne serait pas un plancher.

## 2. Les trois niveaux

Toutes les lignes : mêmes 2 058 personnes, mêmes 60 items, même attaque.

| niveau | condition | top-1 [IC 95 %] | AUC à segment constant [IC 95 %] |
|---|---|---|---|
| — | hasard (1 / 2 058) | 0,0486 % | 0,500 par définition |
| **population** | marginales indépendantes de population | **0,000 %** [0,000 ; 0,000] | **0,5003** [0,4875 ; 0,5120] |
| **population** | **vecteur humain réel d'une autre personne** | **0,000 %** [0,000 ; 0,000] | **0,4995** [0,4868 ; 0,5124] |
| *(rappel, autre branche)* | meilleur générateur classique conditionné au segment | 0,1535 % | non mesuré |
| **segment** | vecteur humain réel d'une autre personne **du même segment** | **0,146 %** [0,000 ; 0,340] | **0,4847** [0,4719 ; 0,4967] |
| **segment** | plafond théorique d'un attaquant qui connaît le segment, `E[1/\|S_gra\|]` | **1,896 %** | — |
| *(contesté, §3)* | jumeau « Demographics Only - GPT4.1-mini » | **2,153 %** [1,584 ; 2,779] | **0,7509** [0,7396 ; 0,7628] |
| **personne** | **jumeau JSON Persona - GPT4.1** | **20,668 %** [19,045 ; 22,376] | **0,9076** [0,8990 ; 0,9150] |
| *(plafond)* | retest humain vagues 1-3 aux items attaqués | 81,630 % [79,913 ; 83,236] | 0,9917 [0,9892 ; 0,9938] |

**Le plancher de population est nul, sous les deux formes.** Ni un générateur sans aucune
structure de dépendance, ni un vecteur humain réel — qui a, par construction, la structure de
dépendance exacte d'un humain — ne dépassent le hasard. Les deux sont à 0,000 % de top-1 et à
AUC 0,50 à segment constant. **La capacité à produire des corrélations inter-items réalistes
ne ré-identifie personne.**

**La marche du segment est petite.** Ajouter au vecteur humain réel la contrainte d'appartenir
au **bon** segment le porte de 0,000 % à **0,146 %** [0,000 ; 0,340] — trois personnes sur
2 058, un IC qui contient encore zéro, et une AUC à segment constant de 0,4847, toujours
indistinguable de l'absence de trace. Un attaquant qui connaîtrait parfaitement le segment et
tirerait au hasard dedans plafonnerait à **1,896 %**.

**La marche de la personne est ce qui reste, et c'est presque tout.** De 0,146 % (ou, au plus
favorable au segment, de 1,896 %) à **20,668 %**.

## 3. Ce que « Demographics Only » a réellement reçu — ma prédiction P3 est réfutée

J'avais préenregistré que ce jumeau, censé n'avoir vu que le segment, serait **au hasard à
segment constant** (AUC dans [0,48 ; 0,52]). **Il ne l'est pas** : **0,7509** [0,7396 ; 0,7628]
sous S_gra, et **0,7364** [0,7240 ; 0,7486] sous la segmentation de robustesse S_fin. Il
distingue nettement sa personne des autres membres de son propre segment. Ma prédiction est
réfutée, franchement, et voici pourquoi.

Le bloc *Demographics* du catalogue Twin compte **14 questions**. Leurs réponses jointes
prennent **2 055 valeurs distinctes pour 2 058 personnes** ; le voisin démographique le plus
proche d'une personne partage, en médiane, **11 de ces 14 réponses**, pas 14. Contre ce voisin
le plus proche, le jumeau Demographics Only conserve une AUC de **0,7340** [0,7162 ; 0,7529],
là où les trois planchers restent au hasard (0,5046 / 0,4971 / 0,5012).

**Conséquence, et elle est opposable.** Un conditionnement qui sépare 2 055 personnes sur
2 058 n'est pas une appartenance de groupe : c'est un **quasi-identifiant individuel**. Le
jumeau « Demographics Only » appartient donc au **niveau personne**, à son barreau le plus
bas — la trace portée par des attributs quasi identifiants plutôt que par les réponses passées
de l'individu. **La prémisse de l'objection R4 — « un objet qui ne contient par construction
aucune information individuelle » — est fausse sur les données.** Les vrais objets sans
information individuelle sont ceux du §2, et ils sont au hasard.

**Ce que je n'ai pas pu vérifier, et qui borne ce paragraphe.** L'archive publie les *sorties*
de cette configuration, pas son gabarit de *prompt* : je ne peux pas affirmer que les
14 questions du bloc *Demographics* sont exactement celles qui lui ont été passées. Ce que
j'établis est plus faible et suffit : **quel que soit son prompt, ce jumeau discrimine à
l'intérieur des deux segmentations du dépôt, donc son entrée est strictement plus fine qu'un
segment démographique.** Le reste de ce rapport n'en dépend pas : le §2 et le §4 n'utilisent
jamais ce jumeau comme niveau segment.

## 4. Le témoin qui tranche : à segment constant

La question du relecteur, posée exactement : *le jumeau d'une personne retrouve-t-il cette
personne mieux qu'il ne retrouve une autre personne du même segment ?* Toute l'information de
segment est tenue constante par construction ; ce qui subsiste ne peut plus en être une.

| condition | top-1 **dans le segment** | AUC à segment constant [IC 95 %] |
|---|---|---|
| hasard intra-segment | 1,896 % | 0,500 |
| vecteur humain réel d'une autre personne | 1,753 % | **0,4995** [0,4868 ; 0,5124] |
| vecteur humain réel d'une autre personne du même segment | 0,097 % | **0,4847** [0,4719 ; 0,4967] |
| jumeau Demographics Only | 13,986 % | 0,7509 [0,7396 ; 0,7628] |
| **jumeau JSON Persona - GPT4.1** | **45,579 %** | **0,9076** [0,8990 ; 0,9150] |
| retest humain vagues 1-3 | 91,509 % | 0,9917 [0,9892 ; 0,9938] |

**L'avantage ne disparaît pas à segment constant.** L'AUC du jumeau persona est à **0,9076**,
sa borne basse à 0,8990, très au-dessus du seuil décisif préenregistré (0,55) et très
au-dessus de 0,50. Son top-1 **à l'intérieur du segment** est de 45,6 % contre un hasard
intra-segment de 1,9 % — mais ce chiffre-là dépend de la convention d'ex æquo déclarée au §1,
et c'est l'AUC, qui n'en dépend pas, qui rend le verdict.

**Comparaison appariée, personne par personne, contre l'objet sans réponses passées.** Écart
d'AUC à segment constant entre le jumeau persona et le jumeau Demographics Only, apparié sur
les mêmes 2 057 personnes : **+0,1566** [+0,1434 ; +0,1699]. Même en accordant au niveau
non-personnel tout ce que le jumeau Demographics Only obtient — attribution que le §3 montre
être trop généreuse —, il reste un avantage individuel strictement positif, dont l'IC est loin
de zéro.

## 5. La part réellement attribuable à la personne — et pourquoi il faut publier l'échelle

Les deux échelles étaient fixées avant calcul. Aucune n'est canonique ; publier l'une sans
l'autre serait un choix fait après avoir vu le résultat.

| niveau segment retenu | part **population** | part **segment** | **part personne**, échelle des taux | **part personne**, échelle des bits |
|---|---|---|---|---|
| vecteur humain du même segment (0,146 %) | 0,24 % | 0,47 % | **99,3 %** | **81,8 %** (7,15 bits sur 8,73) |
| plafond théorique `E[1/\|S_gra\|]` (1,896 %) | 0,24 % | 8,95 % | **90,8 %** | **39,5 %** (3,45 bits sur 8,73) |
| jumeau Demographics Only (2,153 %) — *l'attribution la plus défavorable à l'article* | 0,24 % | 10,18 % | **89,6 %** | **37,4 %** (3,26 bits sur 8,73) |

**Le chiffre à publier est celui de la ligne la plus défavorable**, parce que c'est la seule
qu'un relecteur hostile acceptera : **même en portant au crédit du niveau non-personnel les
2,15 % entiers d'un jumeau dont le §3 établit que l'entrée est quasi identifiante, la part
attribuable à la personne vaut 89,6 % du taux** — 18,5 points sur 20,7.

**Et le même calcul donne 37,4 % sur l'échelle des bits d'identité, où le niveau
non-personnel pèse donc *plus* que la personne.** Ce n'est pas une contradiction : un taux et
un log-rapport ne mesurent pas la même chose, et la part dépend de l'échelle exactement comme
elle en dépendrait pour n'importe quelle décomposition multiplicative. **La conséquence pour
l'article est ferme : aucune part ne doit être publiée sans son échelle.** Sur la lecture la
plus défendable du niveau segment — un objet réellement de groupe, §2 — les deux échelles
s'accordent et donnent 99,3 % et 81,8 %.

**Ni le seuil décisif D ni le seuil secondaire S du préenregistrement ne sont franchis**
(part des taux 89,6 % > 50 %, part des bits 37,4 % > 20 %, borne basse de l'AUC 0,8990 > 0,55).

## 6. Les deux familles d'items : la décomposition n'est pas la même, et pas comme je l'avais prédit

| | top-1 jumeau persona | AUC à segment constant, jumeau persona | écart apparié contre le jumeau sans réponses passées |
|---|---|---|---|
| 40 items `_Q295` | **33,163 %** [31,244 ; 35,139] | **0,9181** [0,9097 ; 0,9259] | **+0,1484** [+0,1344 ; +0,1621] |
| 20 items hors `_Q295` | **0,255 %** [0,073 ; 0,467] | **0,6147** [0,6014 ; 0,6265] | **+0,0840** [+0,0709 ; +0,0980] |

J'avais préenregistré (P5) que sur les 20 items hors `_Q295` l'AUC à segment constant du jumeau
persona ne serait **pas** distinguable de 0,50. **Elle l'est** : 0,6147, IC [0,6014 ; 0,6265],
qui exclut 0,50 largement. **Ma prédiction est réfutée sur ce point**, et le fait est plus
intéressant que la prédiction.

**Ce que cela change.** Que « tout l'effet vive dans les 40 items » est un énoncé sur le
**top-1**, pas sur la localisation de l'information de personne. Sur le top-1, les deux
familles sont séparées par deux ordres de grandeur (33,2 % contre 0,26 %). À segment constant,
**les deux familles portent un signal de personne strictement positif**, et l'écart apparié
contre l'objet sans réponses passées reste hors de zéro sur les deux (+0,148 et +0,084). Les
20 items hors `_Q295` ne suffisent pas à désigner une personne parmi 2 058 ; ils suffisent à
la distinguer de ses voisins de segment.

Les planchers sont au hasard sur les deux familles (AUC 0,4841 à 0,5066), ce qui montre que
cette différence n'est pas un artefact du nombre d'items.

**Une échelle est inutilisable sur cette lecture, et je le déclare plutôt que de la taire.**
Sur les 20 items hors `_Q295`, le jumeau Demographics Only tombe **sous le hasard** en top-1
(0,0024 % contre 0,0486 %) : le log-rapport au hasard y devient négatif et la part sur
l'échelle des bits n'a plus de sens (elle sort à 281 %). Elle n'est pas publiée pour cette
famille, et elle figure au CSV avec cette réserve.

**Ce que je n'affirme pas.** Rien sur la **cause** de la concentration en top-1. Un autre
agent examine si « items d'achat » et « items binaires » désignent la même partition ; je
n'anticipe pas son verdict, et le découpage employé ici est celui, vérifiable, du suffixe de
colonne `_Q295`.

## 7. Le bilan des prédictions préenregistrées

| | prédiction | issue |
|---|---|---|
| **P1** | part personne, échelle des taux, > 85 % | **tenue** — 89,6 % sous l'attribution la plus défavorable |
| **P2** | part personne, échelle des bits, entre 30 % et 45 %, et inférieure au segment | **tenue** — 37,4 % sous la même attribution (mais 81,8 % sous la lecture du §2, et je le dis) |
| **P3** | jumeau Demographics Only au hasard à segment constant | **RÉFUTÉE** — 0,7509 [0,7396 ; 0,7628] ; c'est le résultat le plus utile du document (§3) |
| **P4** | jumeau persona à AUC ≥ 0,80 et top-1 intra ≥ 25 % | **tenue** — 0,9076 et 45,6 % |
| **P5** | achat ≥ 0,85 **et** hors achat indistinguable de 0,50 | **à moitié réfutée** — 0,9181 tenue ; 0,6147 réfute la seconde moitié (§6) |

Cinq prédictions, une réfutée, une réfutée pour moitié, aucune réécrite après coup.

## 8. Ce que ce rapport n'établit pas

1. **Le prompt exact de « Demographics Only » n'est pas lisible dans l'archive** (§3). Ce que
   j'établis — son entrée est plus fine que les deux segmentations du dépôt — ne dépend pas de
   ce prompt, mais l'identification des 14 questions du bloc *Demographics* comme son entrée,
   elle, en dépend et reste une lecture.
2. **Un seul jeu.** Tout ce document porte sur Twin-2K-500. Le témoin à segment constant n'est
   pas construit ici pour Park, où le conditionnement est d'une autre nature et où le
   comparateur à même entrée n'est pas constructible sur données publiques
   (`audit-comparateur-conditionne-2026-09-13.md` §1).
3. **Une seule configuration de jumeau** pour le niveau personne (JSON Persona GPT-4.1).
4. **La décomposition reste une attribution, pas une causalité.** Le témoin à segment constant
   établit qu'il reste un avantage individuel quand le segment est tenu fixe ; il n'explique
   pas par quel mécanisme le jumeau le produit, et §6 ne dit rien de la cause.
5. **Les planchers bornent par le bas.** Que mes générateurs de plancher soient au hasard ne
   prouve pas qu'aucun générateur de population n'y arriverait — seulement qu'un vecteur
   humain réel, qui est la forme la plus favorable de l'objection, n'y arrive pas.

## 9. La phrase exacte que l'article doit écrire pour répondre à l'objection

> Nous décomposons le taux de ré-identification en trois niveaux, à bassin, items et attaque
> strictement constants (2 058 personnes, 60 items). Un vecteur de réponses humain réel
> emprunté à une autre personne — donc doté d'une structure de dépendance inter-items
> parfaitement réaliste et d'aucune information sur la cible — ré-identifie 0,00 %
> [0,00 ; 0,00] des personnes, et ne distingue pas sa cible d'une autre personne du même
> segment démographique (AUC 0,4995 [0,4868 ; 0,5124], où 0,500 signifie aucune trace) ;
> lui imposer d'appartenir au bon segment le porte à 0,146 % [0,000 ; 0,340] et à une AUC de
> 0,4847 [0,4719 ; 0,4967]. Le réalisme de génération et l'appartenance de segment
> n'identifient donc personne. Le jumeau conditionné sur la persona atteint 20,7 %
> [19,0 ; 22,4], et surtout conserve son avantage lorsque le segment est tenu constant :
> AUC 0,9076 [0,8990 ; 0,9150], soit 45,6 % de top-1 à l'intérieur du segment de la cible
> contre 1,9 % attendus au hasard, sous la convention de départage des ex æquo déclarée en
> annexe. Même en portant au crédit du niveau non individuel la totalité des 2,15 %
> [1,57 ; 2,77] du jumeau « Demographics Only » — attribution trop généreuse, puisque les
> 14 questions démographiques dont il dispose prennent 2 055 valeurs distinctes pour
> 2 058 personnes et constituent donc un quasi-identifiant et non un groupe —, la part du
> taux attribuable à la personne reste de 89,6 %. Sur l'échelle des bits d'identité, la même
> attribution donne 37,4 % : nous publions les deux, parce qu'une part de ce type n'a pas de
> sens sans son échelle.

---

*Données : `resultats/c7-decomposition-signal.csv`. Script :
`analyses/c7_decomposition_signal.py`. Préenregistrement :
`resultats/c7-decomposition-signal-preenregistrement.md`, commité avant le premier calcul.*
