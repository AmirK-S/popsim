# Audit de l'affirmation « les 45 items les plus banals donnent 30,25 % » (13 septembre 2026)

statut: courant (section 0 = preenregistrement, ecrite et commitee SEULE avant tout calcul, non modifiee depuis)
mandat: attaquer l'affirmation D4 de la branche agent/mesures/attaquant-imparfait — selection post hoc, balayage cache, mecanisme, baseline, dependance a l'attaquant, controle d'interpretabilite
agent: Opus 5, Anthropic
ecriture: resultats/audit-items-banals-2026-09-13.md, analyses/c7_audit_items_banals.py, resultats/c7-audit-items-banals.csv
lecture_seule: tout le reste, y compris article/manuscrit.md et la branche auditee
interdits: appel paye, reseau, recherche web, commit sur master, fusion, arriere-plan
cout_reel_usd: 0.0

---

## 0. Préenregistrement, écrit avant le script et avant le moindre chiffre nouveau

### 0.1 Ce qui est audité

La branche `agent/mesures/attaquant-imparfait` établit, volet D4 :

> attaquant restreint aux 45 items les plus ordinaires → **30,25 %** [28,37 ; 32,19] de
> ré-identification top-1, contre **20,57 %** [18,91 ; 22,27] avec les 60 items et **12,91 %**
> avec 45 items tirés au hasard ; deux mesures de banalité concordent (r = −0,956) ; le
> confondant « mêmes items pour tous » est écarté (D1b, 12,52 %).

Cette affirmation arrange l'article (elle rend la menace plus réaliste et fait du 20,57 %
publié une sous-estimation). Elle est donc attaquée, pas confirmée.

### 0.2 Le défaut structurel suspecté

Dans `c7_attaquant_imparfait.py`, le critère de banalité (`entropies_items`, `frequences_modales`)
est calculé sur `pool` — **exactement la matrice des humains vague 4 qui sert ensuite de bassin de
candidats et de vérité pour mesurer le taux**. Les 45 items sont donc choisis sur les mêmes
personnes que celles sur lesquelles le taux est mesuré. Le volet D4 tourne en outre à
`repetitions = 1` : aucune variabilité n'est échantillonnée. Le seul test propre est **hors pli**.

### 0.3 Protocole (bassin rigoureusement constant, graine fixée)

Bassin de départ identique à celui audité : `preparer()` de la branche, 2 058 personnes,
60 items toujours renseignés, candidat `JSON Persona - GPT4.1`, baseline `Demographics Only -
GPT4.1-mini` **recalculée dans chaque condition sur exactement le même sous-ensemble d'items et
le même pool**. Réduction déclarée, identique à celle de la branche auditée : 5 tirages de
départage des ex æquo au lieu de 20 ; bootstrap 2 000.

- **V1 — hors pli.** Les 2 058 personnes sont coupées en deux moitiés A et B (permutation de
  graine fixe). Le classement de banalité est estimé sur les **réponses humaines de A seulement**,
  et le taux est mesuré **sur B seulement** (personnes attaquées = B, pool de candidats = B).
  Symétrique (B → A), les deux plis moyennés. Conditions mesurées sur le **même demi-bassin**,
  donc à taille de bassin constante : (a) 45 items banals choisis hors pli, (b) 45 items banals
  choisis **dans** le pli (réplique du défaut, pour isoler l'effet de la sélection), (c) 45 items
  aléatoires communs, (d) les 60 items.
- **V2 — balayage.** k ∈ {6, 10, 15, 20, 30, 40, 45, 50, 55, 60}, hors pli, critère entropie.
  Profil complet publié, pic identifié s'il existe.
- **V3 — nombre de modalités.** Même balayage, classement par **nombre de modalités croissant**
  (égalités départagées par une permutation de graine fixe, jamais par l'entropie), estimé hors
  pli lui aussi.
- **V4 — A-LLR.** Condition centrale (45 banals / 45 aléatoires communs / 60 items) rejouée sous
  l'attaquant fort A-LLR de `c7_attaquant_fort.scores_hors_pli`, importé sans réimplémentation,
  sur le bassin complet de 2 058. Baseline démographique également sous A-LLR.
- **V5 — contrôle d'interprétabilité.** `c7_controle_interpretabilite.controle_avant_interpretation`
  appliqué à la condition « 45 items banals » avant toute interprétation.

Aucune donnée individuelle n'est calculée, imprimée ou écrite : taux agrégés seuls.

### 0.4 Prédictions, et ce qui les réfute

| | prédiction | réfutée si |
|---|---|---|
| **P1** | L'entropie d'un item est une statistique de population très stable ; à n ≈ 1 029 par moitié, le classement hors pli sera presque identique au classement dans le pli. Le taux hors pli à k = 45 sera **à moins de 3 points** du taux dans le pli, et restera **au-dessus** du taux à 60 items sur le même demi-bassin. | écart hors pli / dans le pli > 3 points, **ou** le taux hors pli à k = 45 cesse d'être strictement au-dessus du taux à 60 items (IC bootstrap) |
| **P2** | Il **existe un pic** strictement à l'intérieur de la plage : le taux monte de k = 6 à un maximum situé entre k = 40 et k = 55, puis redescend vers 60. Publier la valeur du pic sans dire qu'on a balayé serait une sélection déguisée. | le profil est monotone croissant jusqu'à 60 (pas de pic), **ou** le maximum est atteint à k = 60 |
| **P3** | Le nombre de modalités est le vrai facteur : le classement par nombre de modalités croissant restitue **au moins 80 %** du gain (taux à k = 45 ≥ 27 % si le gain entropie vaut 30 %). | le classement par nombre de modalités restitue moins de 50 % du gain |
| **P4** | La baseline démographique **monte plus que proportionnellement** sur les items banals. Lecture (non une prédiction) du CSV audité : ratio candidat/baseline 5,93 à k = 45 banals contre 9,94 à 60 items et 9,84 à 45 aléatoires. Je prédis que ce **renversement de ratio survit hors pli** : ratio(45 banals) < ratio(60 items). | ratio(45 banals) ≥ ratio(60 items) hors pli |
| **P5** | A-LLR pondère les accords par leur rareté : il exploite déjà ce que Hamming gaspille. Je prédis que le gain des items banals **s'effondre** sous A-LLR : gain(45 banals − 60 items) sous A-LLR **inférieur à la moitié** du gain sous Hamming. | le gain sous A-LLR vaut au moins la moitié du gain sous Hamming |
| **P6** | Le contrôle d'interprétabilité **passe** à 45 items banals (30 % contre ~5 %, IC très écartés). | le contrôle échoue |

### 0.5 Critère de verdict, fixé d'avance

- **À retirer** si P1 est réfutée du côté « la sélection fait le résultat » (le gain disparaît hors
  pli), **ou** si sous A-LLR les 45 items banals ne font pas mieux que les 60 items.
- **À affaiblir**, avec reformulation obligatoire, si P1 tient mais qu'au moins une de ces choses
  est vraie : un pic existe dans le balayage (P2 confirmée → c'est un réglage), le ratio à la
  baseline se dégrade (P4 confirmée → l'avantage propre au jumeau rétrécit), ou le nombre de
  modalités suffit (P3 confirmée → l'énoncé « items banals » est faux, il faut écrire « items à
  peu de modalités »).
- **Publiable tel quel** seulement si : P1 tient, P2 réfutée (pas de pic), P4 réfutée (le ratio
  tient), P5 réfutée (le gain survit à A-LLR), P6 confirmée.

Je note d'avance que trois de mes six prédictions vont **contre** l'article et trois seulement
décrivent une stabilité technique. Les résultats de la section 1 et suivantes sont écrits après
exécution, sans modification de la présente section 0.

---

## 1. Ce qui est reproduit, et la structure réelle des 60 items

Script `analyses/c7_audit_items_banals.py`, données `resultats/c7-audit-items-banals.csv`.
Aucun appel de modèle, aucun réseau, coût 0,00 USD. Aucun identifiant, aucun appariement
individuel : taux agrégés seuls.

Le classement de banalité est reconstruit à l'identique fonctionnel et **reproduit les chiffres
de la branche auditée** : sur le bassin complet, 45 items à entropie la plus basse donnent
**30,24 %** sous Hamming (la branche publie 30,25 %), et le contrôle d'interprétabilité mesure
30,07 % ; les 60 items donnent 20,61 % (la branche publie 20,57 %) et le contrôle 20,73 %
(publié : 20,68 %). Les corrélations entre critères sont retrouvées : r(entropie, fréquence
modale) = −0,956, r(entropie, nombre de modalités) = **0,955**. Rien dans ce rapport ne repose
sur un désaccord de reproduction.

**Le fait décisif, que la branche auditée mentionne mais n'exploite pas.** La distribution du
nombre de modalités sur les 60 items n'est pas continue, elle est presque binaire :

| nombre de modalités | 2 | 4 | 5 | 7 |
|---|---|---|---|---|
| nombre d'items | **41** | 1 | 10 | 8 |

Les 45 items « les plus banals » retenus par l'entropie sont **41 items binaires, plus 4
items à 5 ou 7 modalités**. Les 15 écartés sont 14 items à 5 ou 7 modalités et 1 à 4 modalités.
Et les **40 premiers sont, exactement, 40 des 41 items binaires**. « Banalité », « entropie
basse » et « fréquence modale haute » ne sont pas trois mesures concordantes d'un même concept :
ce sont trois façons de retrouver la **partition binaire / non binaire** du questionnaire. La
concordance r = −0,956 avancée comme validation croisée ne valide rien — les deux mesures sont
calculées sur la même quantité sous-jacente.

## 2. V1 — le test hors pli : la sélection post hoc n'explique PAS le résultat

Items choisis sur une moitié des personnes, taux mesuré sur l'autre. Toutes les conditions sur
le **même demi-bassin** (1 029 personnes, pool de 1 029), baseline recalculée dans chaque
condition sur **exactement les mêmes colonnes**. Moyenne des deux plis.

| condition, k = 45 | top-1 candidat | IC 95 % | baseline (mêmes items) | ratio |
|---|---|---|---|---|
| entropie, **hors pli** | **35,65 %** | [32,84 ; 38,47] | 6,83 % | 5,22 |
| entropie, dans le pli (réplique du défaut) | 35,46 % | [32,58 ; 38,31] | 7,17 % | 4,94 |
| fréquence modale, hors pli | 36,79 % | [34,03 ; 39,70] | 6,92 % | 5,32 |
| fréquence modale, dans le pli | 37,23 % | [34,52 ; 40,20] | 6,65 % | 5,62 |
| 45 items aléatoires communs (10 tirages) | 16,85 % | [14,72 ; 19,06] | 2,61 % | 6,65 |
| les 60 items | 25,24 % | [22,60 ; 27,87] | 3,52 % | 7,28 |

**P1 confirmée, et c'était le point décisif : il n'y a pas de sélection sur la sortie.** L'écart
hors pli / dans le pli vaut **0,19 point** (35,65 contre 35,46), très en deçà du seuil de 3 points
préenregistré, et le recouvrement des 45 items retenus entre les deux moitiés est de 45/45. C'est
attendu : l'entropie d'un item est une statistique de population estimée sur 1 029 personnes, pas
une quantité ajustée au bruit. **L'angle « on a choisi les items qui marchent » est réfuté. Je
l'avais annoncé comme le point décisif et il ne tue pas le résultat.**

Une réserve tout de même sur la comparaison publiée : la branche compare 30,25 % à **12,91 %**
pour 45 items aléatoires, sur **3 répétitions**. Mes 10 tirages sur demi-bassin s'étalent de
13,3 % à 22,4 %, et un tirage supplémentaire sur bassin complet donne 8,79 %. La variance entre
jeux d'items aléatoires est énorme ; le contraste « 30,25 contre 12,91 » est vrai en direction,
mais son ampleur est un chiffre à ±5 points, pas une mesure.

## 3. V2 — le balayage : il y a un pic, et il n'est pas à 45

Contrôle d'interprétabilité appliqué avant cette section (V5, section 6) : **PASSE**.

Balayage hors pli du nombre d'items retenus, critère entropie, même demi-bassin partout :

| k | 6 | 10 | 15 | 20 | 30 | **40** | 45 | 50 | 55 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|
| top-1 | 0,8 | 2,6 | 7,1 | 13,3 | 25,3 | **36,4** | 35,4 | 32,9 | 29,1 | 25,2 |
| baseline | 0,4 | 0,8 | 1,5 | 2,2 | 4,4 | 6,9 | 6,9 | 5,8 | 4,2 | 3,4 |

**P2 confirmée.** Le profil est **non monotone, avec un maximum intérieur à k = 40** (36,37 %,
contre 35,42 % à k = 45 et 25,23 % à k = 60). Les IC de k = 40 et k = 45 se chevauchent : le pic
n'est pas tranché entre ces deux points, mais l'existence d'un maximum intérieur, elle, l'est
(k = 40 contre k = 55 et k = 60 sont séparés sans chevauchement).

Deux conséquences.

1. **Le 45 de la branche est un artefact de grille**, pas un résultat : il vient de
   `PARTS_ITEMS = 0.75` × 60, une fraction héritée des volets D1/D2 où elle n'avait aucun rapport
   avec la banalité. Aucune recherche du maximum n'a été faite, donc aucune sélection sur le pic
   n'a eu lieu — mais l'article ne peut pas publier « 45 items » comme s'il s'agissait d'un seuil
   signifiant.
2. **k = 40, le maximum, est exactement l'ensemble des items binaires.** Le profil ne décrit pas
   un compromis quantité/qualité d'information : il décrit l'entrée progressive des items à
   nombreuses modalités, qui dégradent le taux à mesure qu'on les rajoute.

Publier la valeur du maximum sans dire qu'un balayage a eu lieu serait une sélection déguisée.
Le balayage complet est donc publié ci-dessus, et le chiffre à retenir n'est pas un point mais
une **forme** : monter jusqu'aux items binaires, redescendre ensuite.

## 4. V3 — le vrai facteur est le nombre de modalités, pas la banalité

Même balayage, items classés par **nombre de modalités croissant**, égalités départagées par une
permutation aléatoire de graine fixe (jamais par l'entropie, sans quoi le test ne testerait rien).

| k | 6 | 10 | 15 | 20 | 30 | **40** | 45 | 50 | 55 | 60 |
|---|---|---|---|---|---|---|---|---|---|---|
| top-1, classement par n° de modalités | 0,9 | 3,6 | 8,6 | 14,5 | 24,0 | **36,0** | 35,5 | 33,7 | 29,7 | 25,2 |
| top-1, classement par entropie | 0,8 | 2,6 | 7,1 | 13,3 | 25,3 | **36,4** | 35,4 | 32,9 | 29,1 | 25,2 |

**P3 confirmée, largement au-delà de son seuil.** À k = 45, le gain sur les 60 items vaut
10,39 points avec le classement par nombre de modalités contre 10,41 points avec l'entropie :
**99,8 % du gain est restitué** par une variable qui ignore complètement la forme de la
distribution des réponses. Même pic, à k = 40, même profil, à moins d'un demi-point près sur
toute la plage.

L'énoncé « les items banals portent l'attaque » est donc **faux au sens où il sera lu**. Aucun
item de Twin n'est banal : la fréquence modale maximale vaut 0,621 (la branche le note
elle-même). Ce que mesure le volet D4, c'est : **un questionnaire binaire se ré-identifie mieux
qu'un questionnaire mixte, parce que le jumeau reproduit mal les items à 5 et 7 modalités.** Le
mécanisme avancé par la branche est le bon ; c'est sa dénomination qui ne l'est pas.

## 5. V4 — sous A-LLR, le gain survit, mais l'avantage sur la démographie s'effondre

Bassin complet (2 058), mêmes conditions, attaquant fort A-LLR de `c7_attaquant_fort`
(paramètres estimés hors pli), importé sans réimplémentation. Baseline démographique passée sous
A-LLR elle aussi.

| sous-ensemble | Hamming | baseline | ratio | A-LLR | baseline | ratio |
|---|---|---|---|---|---|---|
| 45 items « banals » | 30,24 % | 5,07 % | **5,96** | 31,49 % | 4,03 % | **7,81** |
| 45 items aléatoires communs | 8,79 % | 0,91 % | 9,63 | 12,39 % | 0,49 % | 25,50 |
| les 60 items | 20,61 % | 2,09 % | **9,87** | 23,28 % | 0,83 % | **28,18** |

**P5 réfutée.** Le gain des items binaires ne disparaît pas sous A-LLR : 8,21 points
(31,49 − 23,28) contre 9,63 points sous Hamming, soit **85 % du gain conservé**, très au-dessus
de la moitié que j'avais préenregistrée comme seuil. Le résultat n'est donc **pas** un simple
défaut de notre attaquant naïf. C'est une réfutation nette de mon angle 5.

**Mais P4 est confirmée, et c'est ici que l'affirmation auditée se casse.** La baseline
démographique monte **plus que proportionnellement** sur les items binaires : de 2,09 % à 5,07 %
sous Hamming (×2,4), et de 0,83 % à 4,03 % sous A-LLR (×4,9). Le rapport candidat/baseline —
le multiplicateur de risque proprement imputable au jumeau — **chute de 9,87 à 5,96 sous Hamming,
et de 28,2 à 7,8 sous A-LLR**, un facteur 3,6. Hors pli (section 2), même signe : 7,28 à 60 items
contre 5,22 à 45 items binaires.

Honnêtement, dans l'autre sens : l'**écart absolu** candidat − baseline, lui, augmente
(18,5 → 25,2 points sous Hamming, 22,5 → 27,5 sous A-LLR). Les deux métriques divergent, et les
deux doivent être rapportées. Traduction : sur un questionnaire binaire, **tout le monde
ré-identifie mieux, y compris un attaquant qui ne dispose que de la démographie**. Le jumeau
identifie plus de gens en nombre, mais il en identifie une part plus faible de ce que la seule
démographie identifiait déjà.

C'est ce qui invalide la seconde moitié de l'affirmation auditée : **« notre chiffre publié de
20,57 % sous-estime le risque réel » ne tient pas**. Le 20,57 % s'accompagne d'un multiplicateur
de ×9,9 sur la démographie ; le 30,25 % s'accompagne d'un ×6,0. Le chiffre le plus élevé est
celui qui démontre le moins.

## 6. V5 — le contrôle d'interprétabilité

`c7_controle_interpretabilite.controle_avant_interpretation`, appliqué sur exactement les
45 colonnes et exactement le bassin utilisés, baseline recalculée par la fonction elle-même :

- **45 items banals : PASSE** — candidat 30,07 % [28,19 ; 32,02] contre baseline 5,02 %.
- **60 items (référence) : PASSE** — candidat 20,73 % [19,13 ; 22,47] contre baseline 2,15 %.

**P6 confirmée.** Rien dans les sections 3 à 5 n'est interprété sans ce contrôle.

## 7. Mes prédictions préenregistrées, et ce qu'elles sont devenues

| | prédiction | mesure | verdict |
|---|---|---|---|
| P1 | hors pli à moins de 3 points du dans-le-pli, et au-dessus des 60 items | 0,19 point ; 35,65 % contre 25,24 % | **confirmée** |
| P2 | pic strictement intérieur, entre k = 40 et 55 | pic à k = 40 | **confirmée** |
| P3 | le nombre de modalités restitue ≥ 80 % du gain | 99,8 % | **confirmée** |
| P4 | ratio(45 banals) < ratio(60 items) hors pli | 5,22 contre 7,28 ; 5,96 contre 9,87 sur bassin complet ; 7,81 contre 28,18 sous A-LLR | **confirmée** |
| P5 | le gain s'effondre sous A-LLR (< la moitié) | 85 % du gain conservé | **réfutée** |
| P6 | le contrôle passe | PASSE | **confirmée** |

**Une prédiction sur six est réfutée, et c'est celle qui arrangeait mon audit** : j'attendais que
A-LLR détruise l'effet, il ne le détruit pas. Symétriquement, mon angle annoncé comme décisif —
la sélection post hoc — ne donne rien. L'affirmation auditée est plus solide que je ne l'ai
supposé sur ces deux points, et elle est fausse sur deux autres que je n'avais pas mis au premier
rang : sa dénomination et sa portée pour l'article.

## 8. Verdict

**À affaiblir et à reformuler. Ni publiable tel quel, ni à retirer.**

Critère préenregistré 0.5 : P1 tient et A-LLR ne tue pas l'effet → pas de retrait. P2, P3 et P4
sont confirmées → reformulation obligatoire sur les trois points.

Ce qui tient : un attaquant restreint aux items du questionnaire qui n'ont que deux modalités
ré-identifie à un taux **plus élevé** qu'avec l'ensemble des items ; le résultat est stable hors
pli, indépendant de la mesure de banalité employée, et il survit à un attaquant fort.

Ce qui ne tient pas : (a) le mot « banals » — il s'agit d'items **binaires**, et aucun item de
Twin n'est banal (fréquence modale max 0,621) ; (b) le chiffre « 45 items » — la courbe culmine
à k = 40, exactement l'ensemble des 41 items binaires, et 45 est un reste de la grille 0,75 des
volets précédents ; (c) l'inférence « donc notre 20,57 % sous-estime le risque » — sur les items
binaires, la baseline démographique monte davantage que le candidat, et le multiplicateur de
risque imputable au jumeau est divisé par 1,7 sous Hamming et par 3,6 sous A-LLR.

### La formulation exacte que l'article doit employer

> La composition du questionnaire pèse davantage que le nombre d'items. Parmi les 60 items
> toujours renseignés de Twin-2K-500, 41 n'ont que deux modalités et 19 en ont quatre à sept. Un
> attaquant restreint aux seuls items binaires ré-identifie **36,4 % [33,5 ; 39,2]** des
> répondants (sélection des items hors pli, mesure sur les 1 029 personnes non utilisées pour la
> sélection), contre 25,2 % [22,6 ; 27,9] avec les 60 items sur le même bassin : les items à
> nombreuses modalités, que le jumeau reproduit mal, entrent dans l'appariement comme du bruit.
> L'effet est de même signe sous l'attaquant fort A-LLR (31,5 % contre 23,3 % sur le bassin
> complet de 2 058). **Il ne doit pas se lire comme une aggravation de la menace.** Sur ces mêmes
> items binaires, la baseline démographique monte de 2,1 % à 5,1 % (de 0,8 % à 4,0 % sous A-LLR) :
> le multiplicateur de ré-identification imputable au jumeau **tombe de ×9,9 à ×6,0** sous Hamming
> et de ×28 à ×7,8 sous A-LLR, même si l'écart absolu, lui, augmente. Un questionnaire binaire est
> plus facile à ré-identifier **pour tout le monde**, y compris pour un attaquant qui ne dispose
> que de la démographie. Notre chiffre principal ne sous-estime donc pas le risque : il est
> mesuré sur le jeu d'items qui donne le contraste le plus net avec la démographie.

Interdit à l'article : le mot « banals » ou « ordinaires » pour désigner ces items ; le chiffre
« 30,25 % sur 45 items » présenté sans le balayage complet et sans sa baseline ; et toute phrase
du type « une base commerciale ordinaire suffit », que rien ici n'établit — ce qui est testé est
une propriété du **questionnaire Twin**, pas de ce que détient une base commerciale.

## 9. Limites de cet audit

- **Un seul découpage hors pli** (deux moitiés, une graine). Le recouvrement des items retenus
  étant de 45/45, un découpage répété ne changerait rien, mais ce n'est pas mesuré.
- **Le bassin change de taille entre volets** : 1 029 en V1–V3 (hors pli), 2 058 en V4–V5. Les
  comparaisons ne sont faites **qu'à l'intérieur** d'un volet ; aucun taux de V1–V3 n'est comparé
  à un taux de V4–V5.
- **Un seul jeu, un seul générateur** : Twin-2K-500, `JSON Persona - GPT4.1`. La structure
  41 binaires / 19 multi-modalités est une propriété de ce questionnaire ; rien n'est transposé à
  Park et al., et la section 8 ne doit pas l'être non plus.
- **La partition n'est pas manipulée expérimentalement.** Binaire contre multi-modalités est ici
  une variable observationnelle : ces 19 items diffèrent peut-être aussi par leur contenu (ce sont
  des échelles), et non seulement par leur nombre de modalités. Distinguer les deux demanderait de
  replier les échelles à 5 et 7 modalités en binaire et de remesurer — ce n'est pas fait ici.
- **Réduction déclarée** : 5 tirages de départage des ex æquo au lieu de 20, comme la branche
  auditée, pour que les chiffres lui soient comparables. Coût constaté sur la condition de
  référence : environ 0,1 point.
