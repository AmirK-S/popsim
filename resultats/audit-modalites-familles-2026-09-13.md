# Audit : « famille d'items » et « nombre de modalités » sont-elles la même partition ? (13 septembre 2026)

statut: courant
note_statut: section 0 = préenregistrement, écrite et commitée SEULE avant tout calcul de ré-identification, non modifiée depuis
mandat: Recouper deux résultats de la même nuit — le facteur de la ré-identification est le nombre de modalités (audit-items-banals) et tout l'effet vit dans les 40 items d'achat (audit-contamination-persona) — pour établir si les deux variables désignent la même partition, et si non, laquelle porte l'effet.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_audit_modalites_familles.py, resultats/audit-modalites-familles-2026-09-13.md, resultats/c7-audit-modalites-familles.csv
lecture_seule: tout le reste du dépôt
interdits: appel payant, réseau, recherche web, arrière-plan, commit sur master, fusion, écriture dans article/manuscrit.md, impression de toute donnée individuelle
cecite: les branches non fusionnées dans integration/nuit-2026-09-13 ; la prose de persona (non nécessaire ici) ; les jeux autres que Twin-2K-500
cout_reel_usd: 0.00

---

## 0. Préenregistrement, écrit et commité AVANT tout calcul de ré-identification

### 0.1 Le recoupement

Deux rapports de la nuit, produits par deux agents qui ne se sont pas parlé.

**A — `resultats/audit-items-banals-2026-09-13.md`.** Sur les 60 items toujours renseignés de
Twin, le vrai facteur de la ré-identification est le **nombre de modalités** : le classement par
nombre de modalités croissant restitue **99,8 %** du gain obtenu par le classement par entropie.
41 items sont binaires, 19 ont 4 à 7 modalités. Le balayage culmine à k = 40 (**36,4 %** hors pli)
contre 25,2 % avec les 60 items.

**B — `resultats/audit-contamination-persona-2026-09-13.md`.** Tout l'effet du jumeau vit dans
les **40 items d'achat** (33,2 %) et pas dans les **20 items d'heuristiques** (0,24 %, sous le
comparateur classique servi à 0,51 %). Contamination sémantique et prévisibilité différentielle
sont toutes deux écartées, et le rapport conclut que « le mécanisme de cette concentration reste
inexpliqué ».

**L'objection.** Le rapport B publie lui-même, dans son tableau de la section 4, « modalités par
item : 2,0 (achat) contre 5,6 (heuristiques) ». Le rapport A publie « 41 items binaires sur 60 ».
Arithmétiquement, 40 × 2,0 = 80 et 41 binaires impliquent qu'**au plus un** item d'heuristiques
est binaire. Les deux partitions ne sont donc pas seulement corrélées : elles sont, à un item
près, **identiques**. Si c'est le cas, le « mécanisme inexpliqué » de B est peut-être déjà nommé
par A, et l'article doit changer de formulation.

**Ce qui est déjà acquis avant tout calcul, et que je ne revendique pas comme découverte.** Le
tableau croisé famille × modalités est **dérivable des deux rapports publiés** par la seule
arithmétique ci-dessus. Je le vérifie sur les données (section 1), mais c'est une vérification,
pas une mesure nouvelle, et rien dans ce rapport n'en dépend comme d'un résultat propre. Les
prédictions ci-dessous portent **exclusivement** sur des mesures que je n'ai pas encore faites.

### 0.2 Les trois issues, fixées d'avance

- **Issue A — partition confondue, question indécidable.** Le tableau croisé est diagonal ou
  quasi diagonal, et **aucune** manipulation ne permet de séparer les deux variables. L'article
  doit alors écrire exactement cela : les deux descriptions sont empiriquement indiscernables sur
  ce jeu, et aucune donnée de Twin ne peut les départager. C'est un livrable de pleine valeur —
  « indiscernable » n'est pas « inexpliqué ».
- **Issue B — c'est le nombre de modalités.** Recoder les items d'heuristiques en binaire fait
  monter leur taux vers celui des items d'achat ; la famille n'ajoute rien.
- **Issue C — c'est bien la famille.** Le recodage en binaire laisse les items d'heuristiques au
  plancher. Le nombre de modalités est alors un **corrélat** de la partition, pas sa cause, et le
  mystère de B est réel.

### 0.3 Protocole, et les deux pièges que ce projet a déjà manqués trois fois

**Bassin strictement constant.** Le bassin de `c7_audit_items_banals.preparer()`, repris sans
réimplémentation : 2 058 personnes, candidat `JSON Persona - GPT4.1`, baseline
`Demographics Only - GPT4.1-mini` **recalculée dans chaque condition sur exactement les mêmes
colonnes et le même pool**. Attaque `c7_reidentification.rangs_attaque`, importée telle quelle.

**Nombre d'items apparié entre conditions.** Le top-1 dépend mécaniquement du nombre d'items
*et* de leur nature. Toute comparaison de la section 3 se fait à **20 items** de part et d'autre.
Les 40 items d'achat ne sont donc jamais comparés directement aux 20 items d'heuristiques : ils
sont ramenés à 20 par tirage (10 tirages, moyenne et étendue publiées).

Graine 20260913. Réduction déclarée, identique à celle des deux branches recoupées : 5 tirages de
départage des ex æquo au lieu de 20 ; bootstrap 2 000 personnes.
`c7_controle_interpretabilite.controle_avant_interpretation` appelé avant toute interprétation,
sur les colonnes natives réellement en jeu. Aucune donnée individuelle n'est calculée, imprimée
ou écrite : taux agrégés seuls.

**V1 — le tableau croisé.** Famille (achat / heuristiques, par le suffixe `_Q295` du catalogue,
règle de B reprise telle quelle) × nombre de modalités observées. V de Cramér. Identification
nominale des cases hors diagonale.

**V2 — le recoupement des deux rapports.** L'ensemble « 40 premiers items du classement par
nombre de modalités » de A est-il, ou non, l'ensemble des 40 items d'achat de B ? Si oui, les
chiffres 36,4 % et 33,2 % mesurent la même chose sur le même ensemble.

**V3 — décidabilité observationnelle.** Ré-identification mesurée dans chaque case du croisement,
à bassin constant et à 20 items partout. Si une case est vide ou tient en un item, la question
n'est pas décidable observationnellement et il faut manipuler.

**V4 — le test propre, manipulation du nombre de modalités à famille constante.**
- **V4a — dichotomisation des 20 items d'heuristiques.** Deux règles déclarées d'avance :
  (i) *mode contre non-mode* (réponse modale humaine vague 4 = 1, tout le reste = 0) ;
  (ii) *coupure à la médiane* pour les items ordinaux (codes ≤ médiane = 0, sinon 1), règle (i)
  pour les items non ordinaux. La règle est estimée sur les **réponses humaines** et appliquée à
  l'identique au jumeau et au pool. Variante hors pli déclarée : règle estimée sur une moitié des
  personnes, taux mesuré sur l'autre.
- **V4b — dégradation symétrique des items d'achat, sans fabriquer de données.** On ne peut pas
  ajouter des modalités factices à un item binaire. On peut en revanche **apparier les 40 items
  d'achat deux à deux** en 20 items composites à 4 modalités (le couple de réponses observées
  devient une modalité unique). L'information est **exactement conservée** — la transformation
  est bijective — seul le **grain de la métrique** change : un désaccord sur un seul des deux
  sous-items coûte désormais autant qu'un désaccord sur les deux. C'est la manipulation du nombre
  de modalités à information constante. Appariement par permutation de graine fixe, 5 appariements
  différents, moyenne publiée.

**V5 — les autres variables confondues avec la famille.** Position dans le questionnaire (rang de
colonne au catalogue), longueur du libellé, taux de non-réponse, entropie par item, kappa
test-retest par item. Deux lectures : (i) leur écart entre familles ; (ii) leur corrélation avec
le gain normalisé par item **à l'intérieur du bloc d'achat**, où la famille et le nombre de
modalités sont tous deux constants — c'est le seul endroit où ces variables peuvent parler seules.

### 0.4 Prédictions, et ce qui les réfute

| | prédiction | réfutée si |
|---|---|---|
| **P1** | Le tableau croisé est quasi diagonal : les 40 items d'achat sont tous binaires, et **au plus deux** des 20 items d'heuristiques le sont. V de Cramér > 0,90. | plus de deux items d'heuristiques binaires, **ou** au moins un item d'achat non binaire |
| **P2** | Le recouvrement entre « les 40 items à plus faible nombre de modalités » de A et « les 40 items d'achat » de B est d'**au moins 39 sur 40**. Les deux rapports mesurent le même ensemble. | recouvrement inférieur à 39/40 |
| **P3** | La question n'est **pas** décidable observationnellement : au moins une case du croisement contient moins de 5 items, donc aucun contraste à nombre d'items apparié ne peut y être mesuré. | les quatre cases contiennent chacune ≥ 5 items |
| **P4** | **C'est la prédiction centrale, et elle va contre le confort de l'article.** Le recodage en binaire des 20 items d'heuristiques (V4a) fait **monter** leur taux d'au moins un facteur 10 (de 0,24 % vers ≥ 2,4 %) et le fait **passer au-dessus** de la baseline démographique recalculée sur les mêmes colonnes. Autrement dit : **issue B**, le nombre de modalités est le facteur, et le mystère de B se dissout. | le taux des items d'heuristiques binarisés reste sous 2,4 %, **ou** ne passe pas au-dessus de la baseline (borne basse de l'IC sous la borne haute de la baseline) — auquel cas c'est **issue C** |
| **P5** | La dégradation symétrique (V4b) **fait chuter** le taux des items d'achat d'au moins 30 % en relatif par rapport aux 40 items natifs, à information pourtant identique. | chute inférieure à 10 % en relatif |
| **P6** | Le taux de non-réponse est **structurellement nul** sur les 60 items (ils sont choisis comme toujours renseignés) : ce confondant est exclu par construction, pas par mesure. Parmi les autres, **aucune** ne corrèle au gain normalisé par item à l'intérieur du bloc d'achat à \|r\| > 0,40. | une variable dépasse \|r\| = 0,40 à l'intérieur du bloc d'achat |
| **P7** | Le contrôle d'interprétabilité **passe** sur les 20 items d'achat et **échoue** sur les 20 items d'heuristiques natifs (le jumeau y est sous la baseline, B l'établit déjà). Son verdict sur les items d'heuristiques binarisés est le résultat de P4 et n'est pas prédit séparément. | le contrôle échoue sur les items d'achat, ou passe sur les items d'heuristiques natifs |

### 0.5 Critère de verdict, fixé d'avance

- **Issue B (le nombre de modalités)** si P4 est confirmée. L'article doit alors retirer
  « le mécanisme reste inexpliqué » et écrire que la concentration est un effet du grain de
  réponse, pas de la famille d'items.
- **Issue C (la famille)** si P4 est réfutée, c'est-à-dire si les items d'heuristiques binarisés
  restent au plancher. Le mystère de B est alors réel, mais il est **mieux borné** qu'avant : le
  nombre de modalités est exclu comme explication.
- **Issue A (indécidable)** si, et seulement si, V4a et V4b sont tous deux inexploitables — par
  exemple si le recodage détruit tant d'information que la comparaison ne signifie plus rien, ou
  si le contrôle d'interprétabilité échoue partout, y compris du côté achat.
- **Issue mixte, à déclarer telle quelle** si P4 est réfutée mais P5 confirmée : le nombre de
  modalités agirait alors dans un seul sens (en ajouter nuit, en retirer ne répare pas), ce qui
  n'est ni B ni C et doit être écrit comme tel.

Je note d'avance que ma prédiction centrale P4 **dissout** un mystère que l'article présente
comme une découverte, et que c'est une bonne nouvelle pour l'article et non une mauvaise : un
mécanisme nommé vaut mieux qu'un mécanisme ouvert. Je note aussi que c'est la prédiction que je
suis le plus susceptible de perdre, parce que le recodage en binaire **détruit de l'information**
et pourrait faire baisser le taux pour cette seule raison — la section 4 devra distinguer les
deux effets. Les sections 1 et suivantes sont écrites après exécution, sans modification de la
présente section 0.

---

## 1. Le tableau croisé : la partition est la même, à un item près

Script `analyses/c7_audit_modalites_familles.py`, données `resultats/c7-audit-modalites-familles.csv`.
Bassin 2 058 personnes, 60 items, candidat `JSON Persona - GPT4.1`. Aucun appel de modèle,
aucun réseau, coût 0,00 USD. Aucune donnée individuelle : taux agrégés seuls.

| famille \ nombre de modalités | **2** | 4 | 5 | 7 | total |
|---|---:|---:|---:|---:|---:|
| **items d'achat** | **40** | 0 | 0 | 0 | 40 |
| **items d'heuristiques** | **1** | 1 | 10 | 8 | 20 |
| total | 41 | 1 | 10 | 8 | 60 |

**V de Cramér = 0,963.** Les 40 items d'achat sont **tous** à deux modalités ; **un seul** des
20 items d'heuristiques l'est, et il porte un nom : *Denominator neglect*. **P1 est confirmée.**

Replié en 2 × 2 — (achat / heuristiques) × (deux modalités / plus de deux) —, le tableau donne
`[[40, 0], [1, 19]]` : **deux cases sur quatre contiennent moins de cinq items**, dont une vide.
**P3 est confirmée : la question n'est pas décidable observationnellement.** Aucun contraste à
nombre d'items apparié ne peut être construit dans une case qui tient en un item. Ce point est
décisif pour la suite : il interdit la voie observationnelle et **oblige** à manipuler.

**P2 est confirmée.** Les 40 items de plus faible nombre de modalités — l'ensemble sur lequel le
balayage du rapport A culmine — recoupent les 40 items d'achat du rapport B à **39 sur 40**. Les
deux rapports de la nuit mesurent, à un item près, **le même ensemble de colonnes**. Le « 36,4 %
à k = 40 » de A et le « 33,2 % sur les 40 items d'achat » de B ne sont pas deux résultats : c'est
le même, vu deux fois. (Les deux valeurs diffèrent parce que A mesure hors pli sur un demi-bassin
de 1 029 et B sur le bassin entier de 2 058 ; elles ne doivent pas être comparées entre elles.
Sur mon bassin unique de 2 058, les 40 items d'achat donnent **33,00 % [30,98 ; 35,06]**.)

**Ce que ce tableau établit, et ce qu'il n'établit pas.** Il établit que « famille d'items » et
« nombre de modalités » sont, sur Twin-2K-500, **empiriquement indiscernables par observation**.
Il n'établit pas laquelle porte l'effet — et il n'autorise pas non plus à déclarer la question
indécidable, parce qu'une variable observationnellement confondue peut être **manipulée**.
C'est ce que fait la section 2.

## 2. Le test propre : le nombre de modalités, manipulé dans les deux sens

Toutes les conditions ci-dessous sont mesurées sur le **même bassin de 2 058 personnes**, avec la
baseline démographique **recalculée dans chaque condition sur exactement les mêmes colonnes et le
même pool**, et **à 20 items partout**. Les 40 items d'achat ne sont jamais comparés bruts aux
20 items d'heuristiques.

| condition, **k = 20 items partout** | modalités | entropie | top-1 candidat | IC 95 % | baseline | IC baseline |
|---|---:|---:|---:|---|---:|---|
| 20 items d'heuristiques, natifs | 5,6 | 2,06 bits | **0,23 %** | [0,05 ; 0,45] | 0,02 % | [0,00 ; 0,06] |
| 20 items d'heuristiques **dichotomisés au mode** | **2,0** | **0,93 bit** | **0,16 %** | [0,02 ; 0,33] | 0,04 % | [0,00 ; 0,12] |
| 20 items d'heuristiques **coupés à la médiane** | **2,0** | **0,93 bit** | **0,12 %** | [0,02 ; 0,23] | 0,09 % | [0,01 ; 0,20] |
| 20 items d'achat (moyenne de 10 tirages) | 2,0 | 0,99 bit | **11,37 %** | étendue 10,54 – 11,82 | ≈ 1,75 % | |
| 20 items d'achat **appariés en position** | 2,0 | 0,99 bit | **10,96 %** | [9,76 ; 12,26] | 1,87 % | [1,36 ; 2,40] |
| **20 composites d'achat à 4 modalités** (moyenne de 5 appariements) | **4,0** | | **27,26 %** | 26,68 – 28,00 | ≈ 4,45 % | |
| *(hors appariement, pour raccorder aux chiffres publiés)* 40 items d'achat | 2,0 | | 33,00 % | [30,98 ; 35,06] | 6,04 % | [5,08 ; 7,04] |
| *(hors appariement)* les 60 items | | | 20,76 % | [19,14 ; 22,49] | 2,21 % | [1,64 ; 2,87] |

### 2.1 V4a — dichotomiser les items d'heuristiques ne les fait pas monter

**P4, ma prédiction centrale, est RÉFUTÉE, et c'est la prédiction qui arrangeait tout le monde.**
J'avais préenregistré que ramener les 20 items d'heuristiques à deux modalités ferait monter leur
taux d'un facteur 10 au moins, dissolvant le mystère de B. Le taux ne monte pas : il passe de
**0,23 % à 0,16 %** (dichotomisation au mode) ou **0,12 %** (coupure à la médiane). Les trois
intervalles se chevauchent largement : **la manipulation ne fait rien**. Hors pli — règle estimée
sur une moitié des personnes, taux mesuré sur l'autre — même verdict : 0,22 % en moyenne des deux
plis, contre 0,36 % pour les mêmes items natifs sur les mêmes demi-bassins.

Et le point qui rend la réfutation dure plutôt que faible : **après dichotomisation, les items
d'heuristiques sont appariés aux items d'achat sur les trois variables à la fois** — 20 items
contre 20, deux modalités contre deux, et **0,93 bit d'entropie contre 0,99**. À ce triple
appariement, ils ré-identifient **0,16 %** contre **11,37 %**, soit un facteur **73**. Le nombre
de modalités et l'entropie sont donc **exclus** : on les a égalisés, et l'écart est resté entier.

Une réserve, que j'avais annoncée au préenregistrement : dichotomiser **détruit de
l'information** (2,06 bits → 0,93). Un taux qui baisse pourrait n'être que cela. C'est pourquoi
le verdict ne repose pas sur la baisse, qui n'est pas significative, mais sur la **comparaison à
appariement triple** ci-dessus, et sur le test symétrique de la section suivante, qui manipule le
nombre de modalités **sans perte d'information**.

### 2.2 V4b — ajouter des modalités aux items d'achat coûte peu

Les 40 items d'achat sont recomposés deux à deux en **20 items composites à 4 modalités** : le
couple de réponses observées devient une modalité unique. La transformation est **bijective**,
l'information est **exactement conservée** ; seul le grain de la métrique change — un désaccord
sur un seul des deux sous-items coûte désormais autant qu'un désaccord sur les deux.

Le taux passe de **33,00 %** (40 items natifs) à **27,26 %** (20 composites), soit une chute
relative de **17,4 %**. Les intervalles ne se chevauchent pas : l'effet est réel. Mais
**P5 est RÉFUTÉE** — j'avais préenregistré une chute d'au moins 30 %.

Et surtout : **un jeu d'items à 4 modalités ré-identifie encore 27,3 %, quand un jeu d'items à
2 modalités du bloc d'heuristiques ré-identifie 0,16 %.** Un facteur **175**, dans le sens
contraire à celui que l'hypothèse du nombre de modalités exige. Si le nombre de modalités était
le facteur, l'ordre serait : composites (4) < heuristiques dichotomisés (2). L'ordre observé est
l'inverse, et de deux ordres de grandeur.

**Conclusion des deux tests, dans les deux sens : le nombre de modalités a un effet réel mais de
second ordre — environ −17 % en relatif quand on le double — et il ne rend compte d'aucune part
appréciable de la concentration.**

## 3. Les autres variables confondues avec la famille

**P6 est RÉFUTÉE**, et c'est une bonne chose : elle a fait sortir un confondant réel que je
n'attendais pas.

| variable | items d'achat | items d'heuristiques | r avec le gain du jumeau, **à l'intérieur** du bloc d'achat | idem, **à l'intérieur** du bloc d'heuristiques |
|---|---:|---:|---:|---:|
| nombre de modalités | 2,0 | 5,6 | — (constant) | +0,44 via l'entropie |
| entropie par item | 0,990 bit | 2,064 bits | +0,367 | +0,445 |
| kappa test-retest | 0,672 | 0,389 | +0,204 | +0,130 |
| **taux de non-réponse** | **0,000** | **0,000** | — (constant nul) | — (constant nul) |
| position au catalogue | 195 – 234 | 171 – 192 | **−0,507** | −0,293 |
| longueur du libellé | 307 car. (267 – 359) | 114 car. (30 – 634) | −0,155 | **−0,418** |

**Le taux de non-réponse est exclu par construction, pas par mesure.** Les 60 items sont choisis
comme toujours renseignés (`c7_reidentification.items_communs`) : il vaut exactement zéro
partout. Ce confondant ne pouvait pas exister sur ce jeu d'items, et il faut le dire ainsi plutôt
que de le présenter comme un test passé.

**La position dans le questionnaire est un confondant réel, et parfait.** Les deux blocs
**n'ont aucun recouvrement de position** : les items d'heuristiques occupent les rangs 171 à 192
du catalogue, les items d'achat les rangs 195 à 234. La position est donc, elle aussi, une
description exacte de la partition. Pire : **à l'intérieur** du bloc d'achat, elle corrèle à
−0,507 avec le gain du jumeau par item — le jumeau se dégrade mesurablement à mesure que la
batterie d'achats avance. **C'est un résultat nouveau, qui n'appartient à aucun des deux rapports
recoupés**, et qui mérite d'être vérifié pour lui-même.

Mais il n'explique pas la concentration. Les **20 items d'achat appariés en position** sur les
20 items d'heuristiques — les plus proches voisins par rang de catalogue, donc les items d'achat
les plus précoces — ré-identifient **10,96 % [9,76 ; 12,26]**, statistiquement indiscernable des
11,37 % des tirages au hasard. La pente interne au bloc existe ; elle est deux ordres de grandeur
trop faible pour produire un facteur 48.

**Ce qui reste non exclu, et qu'il faut écrire.** La **longueur du libellé** (307 caractères
contre 114) est confondue avec la famille au même titre que le reste, et je ne peux pas
l'apparier sans réécrire le questionnaire : elle reste une explication ouverte. Le **kappa
test-retest** (0,672 contre 0,389) reste lui aussi une différence réelle — le rapport B a déjà
établi qu'un facteur de stabilité de 1,73 ne produit pas un facteur 29 sur la fraction de plafond
récupérée, et rien ici ne le contredit.

## 4. Le contrôle d'interprétabilité, et une précision sur le rapport B

`controle_avant_interpretation`, appelé sur les colonnes natives réellement en jeu, bassin de
2 058, baseline recalculée par la fonction elle-même :

- **20 items d'heuristiques : PASSE** — candidat 0,25 % [0,07 ; 0,47] contre baseline 0,00 %.
- **40 items d'achat : PASSE** — candidat 33,10 % [31,20 ; 35,08] contre baseline 6,01 %.
- **les 60 items : PASSE** — candidat 20,71 % [19,06 ; 22,39] contre baseline 2,15 %.

**P7 est RÉFUTÉE** : j'avais prédit un échec du côté des items d'heuristiques. Il n'y a pas
échec, et la raison mérite d'être écrite parce qu'elle touche la formulation du rapport B.
Le rapport B écrit que sur les items d'heuristiques le jumeau (0,24 %) est **sous le comparateur
classique (0,51 %)** : c'est le **générateur classique conditionné** de l'audit voisin. Face à la
baseline `Demographics Only` recalculée sur ces mêmes 20 colonnes (0,00 %), le jumeau est
**au-dessus**. Les deux énoncés sont vrais et ne portent pas sur la même référence. L'article doit
nommer laquelle il invoque : le contraste « le jumeau ne dépasse pas le comparateur » tient
contre le générateur conditionné, pas contre la baseline démographique.

Noter aussi que les conditions **dichotomisées** de la section 2.1 ne passent pas le contrôle :
elles ne sont donc **pas interprétées** comme des mesures de risque. Elles servent uniquement à
établir une **absence de montée**, ce qui ne demande pas que la condition soit interprétable —
seulement que la comparaison soit appariée, ce qu'elle est.

## 5. Mes prédictions préenregistrées, et ce qu'elles sont devenues

| | prédiction | mesure | verdict |
|---|---|---|---|
| P1 | croisé quasi diagonal, V de Cramér > 0,90 | 40/0 et 1/19 ; V = 0,963 | **confirmée** |
| P2 | recouvrement A ∩ B ≥ 39/40 | 39/40 | **confirmée** |
| P3 | indécidable observationnellement | deux cases sur quatre sous 5 items | **confirmée** |
| P4 | **la dichotomisation fait monter les items d'heuristiques (× 10, au-dessus de la baseline)** | 0,23 % → 0,16 % ; aucune montée | **RÉFUTÉE** |
| P5 | les composites chutent de ≥ 30 % | −17,4 % | **RÉFUTÉE** |
| P6 | aucun confondant interne au bloc d'achat à \|r\| > 0,40 | position : −0,507 | **RÉFUTÉE** |
| P7 | le contrôle échoue sur les items d'heuristiques | il passe | **RÉFUTÉE** |

**Quatre prédictions sur sept sont réfutées, dont ma prédiction centrale, et c'est elle qui
arrangeait l'article** : j'attendais que le recodage dissolve le mystère et fournisse un mécanisme
nommé. Il ne le dissout pas. Les trois confirmées sont des vérifications arithmétiques du
recoupement, dérivables des deux rapports publiés — elles ne sont pas des découvertes et ce
rapport ne les présente pas comme telles.

## 6. Verdict : issue C, mais « la famille » n'est pas davantage une explication

**Issue C est réalisée : ce n'est pas le nombre de modalités.** Le critère préenregistré 0.5 est
appliqué tel quel — P4 réfutée, P5 réfutée, donc ni issue B ni issue mixte.

Il faut cependant être précis sur ce que « issue C » vaut. Dire « c'est la famille d'items »
n'explique rien : « famille » est le **nom du résidu**, pas un mécanisme. Ce que cet audit ajoute
au dossier est donc négatif et borné — mais c'est une addition réelle :

**Sont désormais exclus par un test à appariement, et non par argument :**

1. le **nombre de modalités** — égalisé à 2 des deux côtés, l'écart reste d'un facteur 73 ; et
   porté à 4 du côté achat, le taux reste 175 fois supérieur ;
2. l'**entropie par item** — égalisée à ≈ 0,93 bit contre 0,99, même résultat ;
3. la **position dans le questionnaire** — appariée par plus proche voisin, 10,96 % contre 0,23 % ;
4. le **taux de non-réponse** — nul par construction sur les 60 items.

**Restent ouverts :** la longueur du libellé (non appariable sans réécrire le questionnaire), le
kappa test-retest (réel mais insuffisant, déjà établi par B), et le contenu même des questions.

**Ce que ce rapport amende chez les deux rapports recoupés.** Aucun des deux n'est rétracté ;
tous deux voient une clause causale bornée.

- `resultats/audit-items-banals-2026-09-13.md` §4 écrit : « un questionnaire binaire se
  ré-identifie mieux qu'un questionnaire mixte, **parce que le jumeau reproduit mal les items à
  5 et 7 modalités** ». La clause causale, après « parce que », est **réfutée** : ramener ces
  items à deux modalités ne répare rien. Le fait descriptif du §4 tient entièrement ; c'est son
  explication qui tombe. Son en-tête devrait recevoir `amende_par: resultats/audit-modalites-familles-2026-09-13.md`
  et le statut `provisoire` — je ne le pose pas moi-même, ce fichier ne m'étant pas ouvert
  en écriture.
- `resultats/audit-contamination-persona-2026-09-13.md` §5 écrit « le mécanisme de cette
  concentration reste inexpliqué ». Le fait tient ; la formulation est à remplacer par celle de
  la section 7, qui dit ce qui est exclu au lieu de laisser croire que rien ne l'est. Son en-tête
  devrait recevoir le même `amende_par:`, posé par qui a ce fichier en écriture.

## 7. La phrase exacte que l'article doit écrire à la place de « le mécanisme reste inexpliqué »

> Les deux descriptions possibles de ce contraste recouvrent presque exactement la même partition
> des 60 items : les 40 items d'achat ont tous **deux modalités**, et un seul des 20 items
> d'heuristiques en a deux (V de Cramér 0,96). Par observation, « famille d'items » et « nombre
> de modalités » sont indiscernables ; une manipulation les sépare. Ramenés à deux modalités par
> dichotomisation, les 20 items d'heuristiques ré-identifient **0,16 % [0,02 ; 0,33]** des
> répondants, contre 0,23 % [0,05 ; 0,45] à leur grain natif — et **11,4 %** pour 20 items
> d'achat, à nombre d'items, nombre de modalités et entropie appariés (0,93 bit contre 0,99).
> Symétriquement, les 40 items d'achat recomposés en 20 items à quatre modalités, à information
> exactement conservée, ré-identifient encore **27,3 % [25,4 ; 29,8]**. Le nombre de modalités a
> donc un effet réel mais de second ordre — environ −17 % en relatif lorsqu'on le double — et il
> ne rend pas compte de la concentration. N'en rendent compte ni la position dans le
> questionnaire (20 items d'achat appariés en position : 11,0 %), ni le taux de non-réponse (nul
> par construction sur ces items), ni l'entropie. **Le mécanisme de cette concentration reste
> ouvert, mais il est borné : ni la contamination sémantique, ni la fuite du seul niveau de
> dépense, ni le bruit de réponse des items d'heuristiques, ni le nombre de modalités, ni
> l'entropie, ni la position dans le questionnaire n'en rendent compte.**

Interdit à l'article, en plus des treize formulations de `resultats/marqueurs-canoniques-2026-09-13.md` :
écrire que la concentration **s'explique** par le nombre de modalités ou par la famille d'items —
la première est réfutée, la seconde est le nom du résidu et non un mécanisme ; et présenter le
recoupement des deux rapports comme deux confirmations indépendantes, alors qu'ils mesurent le
même ensemble de colonnes à 39 items sur 40.

## 8. Limites de cet audit

- **Un seul jeu, un seul générateur** : Twin-2K-500, `JSON Persona - GPT4.1`. La structure
  40 items d'achat binaires / 20 items d'heuristiques à plusieurs modalités est une propriété de
  **ce** questionnaire ; rien n'est transposé ailleurs.
- **La longueur du libellé n'est pas appariée**, faute de pouvoir la manipuler sans réécrire les
  questions. C'est le principal confondant qui survit à cet audit.
- **La dichotomisation détruit de l'information** (2,06 → 0,93 bit). C'est pourquoi le verdict
  ne repose pas sur la baisse observée, mais sur la comparaison à appariement triple et sur le
  test symétrique V4b, qui manipule le nombre de modalités à information constante.
- **Les composites à 4 modalités ne montent pas à 5 ou 7.** Apparier trois items donnerait 8
  modalités et 13 items, ce qui casserait l'appariement du nombre d'items ; l'effet du nombre de
  modalités est donc mesuré sur le pas 2 → 4 seulement, et extrapolé pour rien au-delà.
- **La corrélation position / gain à l'intérieur du bloc d'achat (−0,507)** est mesurée sur
  40 items et n'est pas préenregistrée : c'est une observation à vérifier pour elle-même, pas un
  résultat de ce mandat.
- **Réduction déclarée** : 5 tirages de départage des ex æquo au lieu de 20, identique aux deux
  branches recoupées, pour que les chiffres leur soient comparables ; bootstrap 2 000.
