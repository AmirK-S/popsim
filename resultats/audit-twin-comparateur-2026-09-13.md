# Audit — le comparateur démographique de Twin-2K-500 : maigre par construction, ou réellement battu ?

statut: courant
mandat: Etablir depuis le code et les donnees sur quoi le comparateur demographique de Twin-2K-500 est conditionne, mesurer la fraction des 2 058 repondants seuls dans leur cellule demographique exacte et la comparer frontalement aux 98,86 % de Park, puis rejouer l'attaque A-LLR a bassin constant avec un comparateur ENRICHI d'autant d'attributs que Park en avait, pour trancher si le rapport de 29,88x s'effondre comme celui de Park ou tient.
agent: audit / Twin comparateur, 13/09
ecriture: analyses/c7_audit_twin_comparateur.py, resultats/audit-twin-comparateur-2026-09-13.md, resultats/c7-audit-twin-comparateur.csv
lecture_seule: tout le reste du depot
interdits: appel de modele paye, reseau, recherche web, arriere-plan, commit sur master, fusion, modification d'un script existant, toute ecriture dans article/manuscrit.md
cecite: Aucune verification reseau. Le paquet local `data/twin2k500` ne contient PAS les invites systeme par configuration : ce que recoit litteralement « Demographics Only - GPT4.1-mini » n'est donc pas verifiable ici, et le §1 le declare comme un angle mort nomme au lieu de le supposer. Les valeurs 23,2264 % / 0,7775 % / 29,88x / 98,86 % publiees par `audit-park-armement-egal-2026-09-13.md` ne servent qu'a la verification de raccordement ; aucune n'est recopiee dans un calcul.
cout_reel_usd: 0.00

---

> ## AVERTISSEMENT — POST HOC, NON PRÉENREGISTRÉ AU SENS DE C7
>
> Cet audit est déclenché **après** `audit-park-armement-egal-2026-09-13.md`, lui-même
> post-hoc. Le §0 ci-dessous fixe prédictions et critères de réfutation **avant le premier
> calcul**, mais pour une question **choisie après coup**. Il ne compte dans aucun
> dénominateur de multiplicité préenregistré et ne peut réfuter aucune prédiction
> préenregistrée d'origine.

---

## 0. PRÉENREGISTREMENT — écrit et commité avant le premier calcul

### 0.0 Ce que je savais déjà en écrivant ce préenregistrement

Déclaré pour que P2 ne soit pas lue comme une prédiction qu'elle n'est pas. **Avant**
d'écrire ce §0 j'ai lu `data/twin2k500/question_catalog_and_human_response_csv/question_catalog.json`
et compté les questions dont `BlockName` vaut `Demographics` : **quatorze**, `QID11` à
`QID24`. P2 est donc une **vérification de lecture**, pas une prédiction. Tout le reste du
§0 est écrit sans qu'aucun taux, aucune unicité et aucun rapport n'ait été calculé.

### 0.1 Conventions fixées d'avance

**Départage des ex æquo.** Convention reprise à l'identique de
`audit-park-armement-egal-2026-09-13.md` §0.1, pour que les deux audits soient comparables
chiffre à chiffre. Elle vaut **un facteur 1,32 sur Twin** sous l'attaque naïve et jusqu'à
130 ailleurs dans ce projet ; elle est donc fixée ici, avant tout calcul, et vaut pour
**toutes** les cellules, cible comme comparateurs :

- **Convention publiée, retenue pour tous les chiffres de tête** : espérance sous départage
  uniforme dans la classe d'ex æquo de tête, `1/|classe|` si la vraie personne est dans la
  classe de tête, 0 sinon. Calcul **exact et déterministe** (tolérance `1e-12`), jamais une
  moyenne de tirages.
- **Deux bornes encadrantes publiées à côté, pour chaque cellule** : `en_faveur` (compte dès
  que rien n'est strictement meilleur) et `contre` (compte seulement si la classe de tête
  est un singleton).

**Bassin strictement constant.** Un seul chargement de Twin. Mêmes personnes attaquées,
même pool de 2 058 candidats, mêmes colonnes d'items pour la cible et pour **chacun** des
comparateurs, enrichis compris. Conformité au chargeur canonique
`c7_fort_monde_ouvert_ic.charger_twin` vérifiée par assertion, arrêt si écart.

**Baseline.** Tout taux sort avec sa baseline recalculée dans **exactement** la condition où
elle sert : même bassin, mêmes items, même attaque, même convention de départage. Aucune
baseline n'est fournie en argument ni reprise d'un autre bassin.

**Contrôle d'interprétabilité** : `analyses/c7_controle_interpretabilite.py`, règle
inchangée — le candidat ne passe que si la borne basse de son IC est **strictement**
supérieure à la borne haute de l'IC du comparateur, les deux sous la **même** attaque et le
**même** bassin. Appliqué avant toute interprétation, contre **le comparateur le plus fort**,
pas contre le plus commode.

**Intervalles.** Bootstrap 2 000 sur les **personnes**, graine `20260913`. Pour les rapports
cible/comparateur : bootstrap **apparié**, les mêmes personnes rééchantillonnées
simultanément des deux côtés, 2 000 tirages.

**Aucune donnée individuelle** n'est calculée, imprimée ni écrite : ni identifiant, ni
appariement, ni cellule démographique d'une personne. Seuls des agrégats sortent.

### 0.2 Ce qu'« enrichir le comparateur » veut dire, fixé avant de mesurer

Le comparateur de Park est un **agent de langage** conditionné sur onze attributs. Twin ne
peut pas être traité de la même façon : rejouer un agent de langage coûterait un appel payé,
qui est interdit. Le comparateur enrichi est donc construit **sans modèle de langage**, à
partir des seuls attributs que le jeu offre à quiconque le télécharge, par la recette déjà
canonique du dépôt (`c7_monde_ouvert.pmm_depuis_demo`, plus proches voisins sur les
attributs, la personne elle-même exclue). C'est un **choix conservateur pour nous** : un
comparateur qui recopie les réponses réelles d'humains démographiquement voisins est au
moins aussi fort qu'un agent de langage nourri des mêmes attributs. Trois familles sont
construites, toutes sur le **même** bassin :

| famille | conditionnement | rôle |
|---|---|---|
| **D0** | le `Demographics Only - GPT4.1-mini` publié par l'équipe Twin | le comparateur actuel de l'article |
| **Dm** | voisins sur les **m premiers attributs démographiques**, m = 4, 8, 11, 14 | la montée en armement, m = 11 est l'égalité stricte avec Park |
| **D14+ctx** | voisins sur les 14 attributs **plus** les items de contexte des vagues 1-3 | la borne haute : tout ce que le jeu offre légitimement |

La **convention de départage, le bassin et l'attaque sont identiques** pour les trois.

### 0.3 Prédictions et critères de réfutation

| # | Prédiction (avant calcul) | Ce qui la réfute |
|---|---|---|
| **P1** | Je reproduis, indépendamment, le top-1 monde fermé de Twin à armement égal : cible **23,2264 % ± 0,50 pt**, comparateur `Demographics Only` **0,7775 % ± 0,20 pt**, rapport **29,88× ± 2,00**. | Un écart au-delà de ces tolérances. **Si P1 est réfutée je m'arrête là**, le livrable est cette non-reproduction, et je ne conclus rien d'autre. |
| **P2** | *(vérification, cf. §0.0)* Le bloc démographique disponible de Twin compte **quatorze** attributs, soit **plus** que les onze de Park, et couvre idéologie politique, parti, région, revenu, éducation, race, genre et âge. | Un compte différent de 14, ou l'absence d'idéologie ou de parti. Alors la thèse « Twin est maigre là où Park est riche » est vraie et l'article est en danger immédiat. |
| **P3** | La fraction des 2 058 répondants **seuls dans leur cellule démographique exacte** sur les quatorze attributs est **supérieure à 90 %**, donc du même ordre que les **98,86 %** de Park. Autrement dit : le bloc de quasi-identifiants **n'est pas** ce qui sépare les deux jeux. | Moins de **50 %**. Alors Twin est bien structurellement différent de Park, le comparateur y est maigre par construction, et le 29,88× est flatteur pour cette raison-là — ce qui est exactement le risque que cet audit cherche. |
| **P4** | **La question qui décide.** Comparateur enrichi à **onze attributs ou plus**, armé d'A-LLR, bassin constant : le rapport cible/comparateur sur Twin **reste au-dessus de 5,0×**. | Le rapport tombe **sous 5,0×**. |
| **P5** | Le meilleur comparateur enrichi reste **sous 5 %** de top-1 en monde fermé, là où celui de Park atteint 85,17 %. | Au-dessus de 5 %. |
| **P6** | *(l'inverse, pour être complet)* Le comparateur actuel de Twin n'est **pas** trop riche : il ne reçoit aucune réponse de vague 4 et son taux armé ne dépasse pas celui du meilleur comparateur enrichi. | `Demographics Only` **dépasse** tous les comparateurs enrichis. Alors il reçoit plus que des démographies, notre 29,88× est **conservateur**, et il faut le dire. |

### 0.4 Le seuil d'effondrement, déclaré avant de calculer

C'est la ligne que le mandat exige et c'est la seule qui décide :

- **rapport ≥ 5,0×** — Twin tient. La chute de Park n'est pas un défaut de notre méthode,
  c'est une propriété du jeu Park, et nous l'avons établi en **tentant** de reproduire la
  chute sur l'autre jeu et en échouant. C'est un argument plus fort qu'aujourd'hui.
- **2,0× ≤ rapport < 5,0×** — Twin est **entamé**. L'article doit publier le rapport réduit,
  pas le 29,88×, et dire dans la même phrase qu'un comparateur mieux armé le divise.
- **rapport < 2,0×** — **effondrement**. Twin ne vaut pas mieux que Park (qui tombe à
  1,06×). L'article perd son dernier jeu porteur et **doit l'écrire**. Aucune reformulation
  ne sauve la démonstration dans ce cas.

### 0.5 Règle d'arrêt et interdiction de conclure en faveur de l'article

Si P1 est réfutée, l'audit s'arrête au §1, sans tableau et sans interprétation.

**Aucune conclusion en faveur de l'article par défaut.** Si le rapport enrichi tombe sous
5,0×, le chiffre publié devient le rapport enrichi, jamais le 29,88×, et le §0.4 s'applique à
la lettre. Le comparateur retenu pour le rapport de tête est **le plus fort des comparateurs
mesurés**, pas le plus commode. Cinq conclusions ont été retirées dans la nuit du 12 au 13,
dont quatre flatteuses ; une sixième ne coûte rien.

### 0.6 Formulations interdites respectées

Les treize interdictions de `resultats/marqueurs-canoniques-2026-09-13.md` §3 (I1 à I12)
s'appliquent à ce rapport. Aucune n'est employée, ni en assertion ni en citation non
indentée.

---

## 1. Sur quoi le comparateur démographique de Twin est réellement conditionné

**Ce qui est établissable, et ce qui ne l'est pas.** Le paquet local `data/twin2k500`
contient les réponses des treize configurations et le texte des personas, **pas les invites
système par configuration**. Ce que reçoit littéralement `Demographics Only - GPT4.1-mini`
n'est donc **pas vérifiable ici**, et `t1-mesure-de-personne-twin.md` §14 point 1 nommait
déjà ce trou. Cet audit ne le comble pas ; il le **rend sans conséquence**, en mesurant
aussi des comparateurs dont le conditionnement est, lui, entièrement sous contrôle (§3).

Ce qui **est** établissable depuis les données : le bloc démographique que le jeu offre à
quiconque le télécharge. Ce sont les questions dont `BlockName` vaut `Demographics` dans
`question_catalog.json`, et c'est le bloc que le dépôt emploie déjà comme « démographies de
Twin » (`t1_commun.demographies_brutes`). Il en compte **quatorze**, `QID11` à `QID24` —
**trois de plus que les onze de Park** :

| | attribut | modalités | | attribut | modalités |
|---|---|---|---|---|---|
| `QID11` | région des États-Unis | 5 | `QID18` | religion | 12 |
| `QID12` | sexe assigné à la naissance | 2 | `QID19` | fréquentation religieuse | 6 |
| `QID13` | âge (tranches) | 4 | `QID20` | parti politique | 4 |
| `QID14` | niveau d'études | 6 | `QID21` | revenu familial | 5 |
| `QID15` | race ou origine | 5 | `QID22` | **idéologie politique** | 5 |
| `QID16` | citoyenneté | 2 | `QID23` | taille du foyer | 5 |
| `QID17` | statut marital | 6 | `QID24` | statut d'emploi | 7 |

Aucune de ces quatorze questions n'est reposée en vague 4 : aucune n'est donc parmi les 60
items attaqués (`twin-ab-audit-provenance-2026-09-11.md`, ligne 1 du tableau des
configurations). Le jeu offre en outre **494 items de contexte** des vagues 1 à 3, non
reposés en vague 4, disponibles pour toute personne construisant un comparateur.

**La granularité n'est pas la même des deux côtés, et elle joue contre Twin.** Park a moins
d'attributs mais plus fins : `ethnicity` à 21 modalités, `income` à 12, `census_division`
à 10, `age` à 7. Twin a plus d'attributs mais plus grossiers — son `age` tient en
**quatre** tranches. Le §2 montre que le résultat net va malgré tout dans l'autre sens.

**P2 est confirmée**, et elle l'est comme vérification de lecture, pas comme prédiction
(§0.0) : quatorze attributs, idéologie politique et parti compris. **La thèse « le
comparateur de Twin est maigre là où celui de Park était riche » est fausse sur son
premier terme.**

---

## 2. Le chiffre qui a tué Park, mesuré sur Twin : 99,71 % contre 98,86 %

Fraction des répondants **seuls dans leur cellule démographique exacte**. Park est
**recalculé ici même**, depuis `demographic_summary.csv` restreint aux 1 052 personnes du
bassin, pour que la comparaison soit frontale et non une citation.

| bloc | jeu | cellules | personnes seules | **part seules** | plafond `moyenne(1/\|cellule\|)` | taille max |
|---|---|---|---|---|---|---|
| **14 attributs, bloc complet** | Twin | 2 055 / 2 058 | 2 052 | **99,7085 %** | 99,8542 % | 2 |
| **11 attributs homologues de Park** | Twin | 2 038 | 2 021 | **98,2021 %** | 99,0282 % | 4 |
| **11 attributs réellement fournis** | Park | 1 046 / 1 052 | 1 040 | **98,8593 %** | 99,4297 % | — |
| cellule à 4 axes (genre × race × âge × éducation) | Twin | 182 | 29 | 1,4091 % | 8,8435 % | 89 |

Raccordement : **98,8593 %** reproduit contre les 98,86 % publiés, écart 0,0007 pt.

**P3 est confirmée, et au-delà de ce que j'avais écrit.** J'avais prédit « supérieure à
90 % » ; c'est **99,7085 %**, soit **0,85 point de plus que Park**. À onze attributs — le
compte exact de Park — Twin est à 98,2021 %, à 0,66 point en dessous ; à quatorze, il
passe devant. **Le « comparateur démographique » de Twin repose lui aussi sur un bloc de
quasi-identifiants, et il est au moins aussi identifiant que celui de Park.**

L'échelle cumulée montre où bascule l'unicité : 0,83 % à quatre attributs, 9,28 % à cinq,
25,61 % à sept, 61,52 % à huit, 90,91 % à dix, **97,91 % à onze**. Le laisse-un-de-côté ne
désigne aucun attribut vedette : la chute maximale est de **0,68 point** (`QID14`,
éducation), et retirer la citoyenneté, le statut marital ou le parti ne change **rien**
(0,00 pt). C'est la **conjonction** qui identifie — le mécanisme classique du
quasi-identifiant, exactement comme sur Park.

**Conséquence directe pour l'article** : la phrase « Twin n'a pas de bloc de
quasi-identifiants » serait fausse. Elle n'est écrite nulle part aujourd'hui ; elle ne doit
pas l'être demain.

---

## 3. Le test symétrique : que devient le 29,88× quand le comparateur est enrichi ?

Bassin strictement constant — 2 058 personnes, 2 058 candidats, les mêmes 60 items pour
toutes les lignes. Convention de départage uniforme exacte (§0.1). Sept comparateurs
construits **sans aucun modèle de langage**, par la recette canonique du dépôt, la personne
elle-même toujours exclue de la recherche de voisins.

| condition | conditionnement | attaque | top-1 monde fermé (IC 95 %) | bornes (contre / en faveur) | AUC | TPR @ 1 % FPR |
|---|---|---|---|---|---|---|
| **cible** JSON Persona - GPT4.1 | persona complète | naïve | 20,6940 % [19,06 ; 22,34] | 18,32 / 24,10 | 0,1494 | 2,9640 % |
| **cible** JSON Persona - GPT4.1 | persona complète | **A-LLR** | **23,2264 %** [21,38 ; 25,02] | 23,23 / 23,23 | 0,1769 | **4,2760 %** |
| **Demographics Only** (publié) | démographies, contenu non vérifiable | naïve | 2,1453 % [1,58 ; 2,80] | 1,80 / 2,67 | 0,0131 | 0,1944 % |
| **Demographics Only** (publié) | démographies, contenu non vérifiable | **A-LLR** | **0,7775 %** [0,44 ; 1,17] | 0,78 / 0,78 | 0,0051 | **0,0486 %** |
| enrichi PMM k=10 | 4 axes | **A-LLR** | 0,0486 % [0,00 ; 0,15] | — | 0,0000 | 0,0000 % |
| enrichi PMM k=10 | 8 premiers attributs | **A-LLR** | 0,0486 % [0,00 ; 0,19] | — | 0,0001 | 0,0000 % |
| **enrichi PMM k=10** | **11 attributs homologues de Park** | **A-LLR** | **0,0486 %** [0,00 ; 0,15] | — | 0,0000 | 0,0000 % |
| **enrichi PMM k=10** | **14 attributs, bloc complet** | **A-LLR** | **0,1458 %** [0,00 ; 0,34] | — | 0,0007 | 0,0486 % |
| enrichi MODE k=10 | 14 attributs | **A-LLR** | 0,0000 % | — | 0,0000 | 0,0000 % |
| enrichi DONNEUR k=1 | 14 attributs | **A-LLR** | 0,0000 % | — | 0,0000 | 0,0000 % |
| **enrichi PMM k=10** | **14 attributs + 494 items de contexte** | **A-LLR** | **0,0972 %** [0,00 ; 0,24] | — | 0,0006 | 0,0000 % |
| *(témoin)* PMM k=10 canonique | 14 attributs, autre graine | **A-LLR** | 0,2430 % [0,05 ; 0,49] | — | 0,0013 | 0,0000 % |

**Le résultat est net et il n'est pas celui que je redoutais : enrichir le comparateur de
Twin ne le renforce pas, et aucun comparateur enrichi n'approche celui qui est déjà
publié.** Les sept comparateurs enrichis tiennent entre **0,0000 %** et **0,2430 %** ; le
`Demographics Only` publié est à **0,7775 %**, soit au moins **trois fois** le meilleur
d'entre eux.

**Une réserve que je publie parce qu'elle est réelle.** À ces niveaux, les écarts **entre
comparateurs enrichis** ne sont pas résolus : 0,0486 % vaut **une** personne sur 2 058,
0,2430 % en vaut cinq. Le témoin canonique (0,2430 %) et ma reconstruction de la même
recette sur le même bloc (0,1458 %) ne diffèrent que par la graine. **Aucun classement
entre comparateurs enrichis n'est affirmé ici** ; ce qui est affirmé, c'est que tous sont
**d'un ordre de grandeur** sous le comparateur publié, et deux ordres sous la cible.

**Le rapport de tête est donc mesuré contre le comparateur le plus fort, et il ne bouge
pas** (règle du §0.5) :

| | comparateur retenu | rapport cible / comparateur | IC 95 % apparié | écart en points | contrôle d'interprétabilité |
|---|---|---|---|---|---|
| **A-LLR, monde fermé** | Demographics Only, 0,7775 % | **29,875×** | **[19,272 ; 54,225]** | **+22,45 pt** | **PASSE** |
| naïve, monde fermé | Demographics Only, 2,1453 % | 9,646× | [7,499 ; 12,954] | +18,55 pt | PASSE |
| A-LLR, TPR @ 1 % FPR | Demographics Only, 0,0486 % | **88,0×** | — | +4,23 pt | — |

Raccordement : **29,875×** contre les 29,88× publiés. Le contrôle d'interprétabilité passe
largement — 21,38 % contre 1,17 %, **20,2 points de marge**, là où Park passait avec 1,33.

**P1 confirmée** au chiffre près (23,2264 % / 0,7775 % / 29,875×, écarts 0,0000).
**P4 confirmée** : 29,875× reste au-dessus du seuil de tenue de 5,0×, et très au-dessus du
seuil d'effondrement de 2,0×. **P5 confirmée** : le meilleur comparateur, publié ou
enrichi, plafonne à 0,7775 %, contre 85,17 % sur Park.

**P6 est à moitié réfutée, et c'est la réponse à la question inverse du mandat.** J'avais
prédit que `Demographics Only` ne dépasserait aucun comparateur enrichi. Il les dépasse
**tous**. Le comparateur de Twin n'est donc pas trop riche au sens d'une fuite — il ne
reçoit aucune réponse de vague 4 — mais il est **le plus fort comparateur démographique que
nous sachions construire sur ce jeu**. Le 29,88× n'est pas flatté par un comparateur
commode : c'est le rapport contre le meilleur adversaire disponible. Il est, en ce sens,
**conservateur**.

---

## 4. Pourquoi Twin résiste là où Park tombe — le mécanisme, mesuré

Les deux jeux ont un bloc de quasi-identifiants de force comparable (§2). Ce qui les sépare
est **la décodabilité de ce bloc depuis les items attaqués**, et elle se mesure de deux
façons.

### 4.1 La part du plafond de cellule réellement atteinte

Le plafond est ce qu'atteindrait une attaque qui lirait **parfaitement** la cellule :
`moyenne(1/|cellule|)`.

| jeu | plafond de cellule | comparateur armé, atteint | **part du plafond réalisée** |
|---|---|---|---|
| **Park** | 99,4297 % | 85,1711 % | **85,66 %** |
| **Twin** | 99,8542 % | 0,7775 % | **0,7786 %** |

Plafonds identiques à un demi-point près ; réalisations séparées d'un facteur **110**. **Le
bloc est aussi identifiant des deux côtés ; sur Twin il n'est pas lisible dans les réponses.**

### 4.2 Les items attaqués portent-ils la démographie ?

Mesure identique à celle de `audit-park-armement-egal-2026-09-13.md` §5.2 : part de la
modalité majoritaire des items humains dans les groupes d'un attribut, contre des groupes
**aléatoires de même taille**.

| | écart maximal au témoin | attribut porteur |
|---|---|---|
| **Park** (11 attributs, 177 items) | **+4,91 pt** | `sexual_orientation`, puis +3,09 (`political_ideology`) |
| **Twin** (14 attributs, 60 items) | **+1,32 pt** | `QID11` (région), puis +1,09 (`QID18`), +1,03 (`QID16`) |

Sur Twin, deux attributs ont un écart **négatif** (`QID19` à −1,10 pt, `QID21` à −0,10 pt),
c'est-à-dire indiscernables du témoin. **Les 60 items de vague 4 de Twin — heuristiques,
biais, préférences économiques — ne portent presque pas la démographie**, là où les 177
items d'attitudes du bloc GSS de Park la portent quatre fois plus.

### 4.3 Ce qui amende l'audit de Park, et que je ne peux pas marquer moi-même

`audit-park-armement-egal-2026-09-13.md` §4 conclut : « Sur Twin, 60 items ne suffisent
pas : c'est l'unique raison pour laquelle la phrase du manuscrit y survit. » **Cette
attribution est trop étroite**, et ce rapport-ci la contredit à armement et à nombre
d'items égaux :

| | comparateur démographique armé, **à 60 items** | cible armée | rapport |
|---|---|---|---|
| **Park** (`c7-park-armement-egal.csv`, volet 4, k = 60) | **22,7424 %** | 53,8736 % | 2,3689× |
| **Twin** (ce rapport, volet 5, k = 60) | **0,7775 %** | 23,2264 % | 29,875× |

À **nombre d'items égal**, les deux comparateurs sont séparés d'un facteur 29. Le nombre
d'items n'est donc pas « l'unique raison » ; il est **une** des deux, l'autre étant la
teneur démographique des items (§4.2). Le bassin de Twin est deux fois plus grand, ce qui
joue dans le même sens mais ne rend pas compte d'un facteur 29.

**Je ne pose pas de marqueur canonique sur le rapport Park**, parce que son fichier ne fait
pas partie de mon périmètre d'écriture. L'état correct est **amendé** (la formulation
change, le fait — la chute de Park — tient entièrement), et la clé d'en-tête à poser serait
`amende_par: resultats/audit-twin-comparateur-2026-09-13.md`. **C'est un point à traiter au
moment de la fusion**, et il est nommé ici pour cette raison. Rien de la conclusion de
l'audit Park n'est retiré : les 85,17 %, les 98,86 % et le 1,06× sont reproduits ou
confirmés par ce rapport.

### 4.4 La courbe en items sur Twin

**Réduction déclarée** : 4 tirages d'items par *k* au lieu des 20 de la convention
`c7_stanford.N_TIRAGES_ITEMS`, grille à trois points. Motif : durée.

| items | comparateur armé (min–max sur tirages) | cible armée | rapport |
|---|---|---|---|
| 20 | 0,2794 % (0,1458–0,3401) | 3,2070 % | 11,48× |
| 40 | 0,8746 % (0,5345–1,5549) | 17,0675 % | 19,51× |
| 60 *(jeu entier, un seul « tirage »)* | 0,7775 % | 23,2264 % | **29,88×** |

**Aucune décroissance n'est affirmée entre 40 et 60 items** : la valeur à 60 items
(0,7775 %) tombe **à l'intérieur** de l'étendue des tirages à 40 items [0,5345 ; 1,5549].
Ce qui est affirmé, et qui est l'inverse exact de Park : sur Twin le **rapport croît** avec
le nombre d'items (11,48× → 19,51× → 29,88×), là où sur Park il **décroît** (5,02× → 1,06×).
Sur Twin, des items supplémentaires profitent à la cible, pas au comparateur.

---

## 5. La question qui décide — verdict

| | prédiction | verdict |
|---|---|---|
| **P1** | reproduction de 23,2264 % / 0,7775 % / 29,88× | **confirmée**, écarts 0,0000 / 0,0000 / 0,005 |
| **P2** | 14 attributs, plus que les 11 de Park | **confirmée** *(vérification, cf. §0.0)* |
| **P3** | > 90 % de personnes seules dans leur cellule | **confirmée au-delà** : 99,7085 %, contre 98,8593 % sur Park |
| **P4** | rapport enrichi ≥ 5,0× | **confirmée** : **29,875×** [19,272 ; 54,225], inchangé |
| **P5** | meilleur comparateur sous 5 % | **confirmée** : 0,7775 % publié, au plus 0,2430 % enrichi |
| **P6** | `Demographics Only` ne dépasse pas les enrichis | **à moitié réfutée** : il les dépasse tous ; le 29,88× en est **conservateur** |

**Le seuil d'effondrement du §0.4 n'est pas atteint, et il n'en est pas près.** Le rapport
reste à **29,875×**, contre un seuil de tenue de 5,0× et un seuil d'effondrement de 2,0×.
La borne basse de son IC apparié, **19,272×**, est encore au-dessus de neuf fois le seuil
d'effondrement.

**Ce qui rend ce verdict solide, c'est qu'il sort d'une tentative sérieuse de le détruire.**
L'audit n'a pas constaté que Twin diffère de Park ; il a **armé le comparateur de Twin
exactement comme celui de Park l'était** — onze attributs homologues, puis quatorze, puis
quatorze plus 494 items de contexte, sous trois recettes de construction dont une qui
recopie intégralement un humain réel voisin — et **l'attaque n'a pas décollé**. Le
comparateur a même perdu du terrain par rapport à celui que l'article emploie déjà.

**Ce qui reste une limite, et qui doit être publié comme telle :**

1. **Les comparateurs enrichis ne sont pas des agents de langage.** Rejouer un agent aurait
   coûté un appel payé, interdit. L'argument qui tient malgré cela est que le **seul** agent
   de langage conditionné sur les démographies présent dans le jeu — `Demographics Only -
   GPT4.1-mini` — est **dans le tableau**, et qu'il est le plus fort de tous. Ce qu'on ne
   peut pas exclure est qu'une **autre** architecture d'agent, sur les mêmes quatorze
   attributs, ferait mieux que 0,7775 %. Il faudrait qu'elle atteigne **11,6132 %**, soit
   **14,94 fois** le comparateur publié, pour ramener le rapport au seuil d'effondrement
   de 2,0×.
2. **Le contenu exact de l'invite de `Demographics Only` reste non vérifiable localement**
   (§1). C'est précisément pourquoi les comparateurs enrichis, dont le conditionnement est
   entièrement connu, ont été construits.
3. **Les écarts entre comparateurs enrichis ne sont pas résolus** (§3), et aucun classement
   entre eux n'est affirmé.
4. **Cet audit est post-hoc**, comme celui qu'il prolonge. Il ne compte dans aucun
   dénominateur de multiplicité préenregistré.

---

## 6. La phrase exacte que l'article doit écrire

À insérer avec la mention post-hoc, dans la section qui traite de Park :

> Park and Twin-2K-500 give opposite answers, and **not because one comparator is thinner
> than the other**. Both "demographics-only" conditions rest on a quasi-identifier block of
> comparable strength: the eleven attributes supplied to the Park agent leave **98.86 %** of
> its 1 052 respondents unique in their own sample, and the fourteen demographic questions
> Twin-2K-500 publishes leave **99.71 %** of its 2 058 respondents unique in theirs — 98.20 %
> when restricted to the eleven attributes homologous to Park's. What differs is whether the
> attacked items decode that block. On Park, a rarity-weighted likelihood attacker converts
> 177 items into **85.17 %** closed-world top-1, i.e. **85.66 %** of the ceiling that perfect
> cell recovery would allow; on Twin the same attacker, against a block that is if anything
> more identifying, reaches **0.78 %**, i.e. **0.78 %** of its own ceiling. Arming Twin's
> comparator does not close that gap: a k-nearest-donor comparator conditioned on the eleven
> Park-homologous attributes, on all fourteen, or on all fourteen plus 494 context items
> reaches **0.05 %**, **0.15 %** and **0.10 %** respectively, and a comparator that copies a
> demographically nearest real respondent in full reaches **0.00 %** — every one of them
> *below* the published Demographics Only condition (**0.78 %**), which therefore remains the
> strongest demographics-only comparator we can build on this dataset. The target-to-
> comparator ratio on Twin is accordingly unchanged at **29.88×** [19.27 ; 54.22] closed-world
> and **88.0×** at 1 % FPR. The mechanism is measurable: Twin's fourteen attributes shift the
> majority-response share of the attacked items by at most **+1.32 points** over same-size
> random groups, against **+4.91 points** on Park. **The Park collapse is a property of that
> corpus — many demographically loaded items published alongside a quasi-identifier block —
> not a defect of the attack, and we established this by trying to reproduce the collapse on
> the other dataset and failing.**
>
> *(Post-hoc, not preregistered; audit of 13 September 2026.)*

### 6.1 Trois gestes de rédaction

1. **Ne pas écrire que Twin est dépourvu de bloc de quasi-identifiants.** Il en a un, plus
   identifiant que celui de Park (99,71 % contre 98,86 %). L'argument de l'article ne repose
   pas là-dessus et ne doit pas prétendre le contraire.
2. **Ne pas attribuer la survie de Twin au seul nombre d'items.** À 60 items, le comparateur
   de Park atteint 22,7424 % et celui de Twin 0,7775 % : facteur 29 à armement et à nombre
   d'items égaux (§4.3).
3. **Publier la teneur démographique des items comme la variable qui décide**, avec sa
   mesure et son témoin. C'est elle qui rend un corpus vulnérable à une attaque qui n'a
   besoin d'aucun jumeau, et c'est un avertissement réutilisable au-delà de ces deux jeux.

---

## 7. Traçabilité

- Script : `analyses/c7_audit_twin_comparateur.py` — graine `20260913`, aucun appel de
  modèle, aucun réseau, lecture seule sur `data/`, aucun script existant modifié.
- Données : `resultats/c7-audit-twin-comparateur.csv`, **460 lignes**, colonnes
  (`volet`, `jeu`, `condition`, `attaque`, `mesure`, `valeur`, `ic_bas`, `ic_haut`, …).
  Volets : `1 inventaire du bloc`, `2 unicite`, `4 armement egal`,
  `4bis rapport et controle`, `5 courbe items`, `6 verdict`,
  `7 determination des items`.
- Valeurs de Park citées au §4.3 et au §4.1 : lues dans `resultats/c7-park-armement-egal.csv`
  (volet `4 courbe items`, `k_items = 60` ; volet `5bis bloc demographique reel`). L'unicité
  de Park est **recalculée** ici, pas citée.
- Aucune donnée individuelle n'est calculée, imprimée ni écrite : ni identifiant, ni
  appariement, ni cellule d'une personne. Seuls des taux et des distributions agrégées.
- Réductions déclarées : 4 tirages d'items par *k* au volet 5, grille à trois points.
  Aucune autre.
- Écarts de raccordement : **aucun** (Park 98,8593 % contre 98,86 % publié ; Twin
  23,2264 %, 0,7775 %, 29,875×).
- Durée du run : 45 secondes, un seul passage, aucune dépense.
