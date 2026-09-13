# C7 — T1a §1c à §1g : protocole écrit avant calcul, mesures écrites après coup

statut: courant
mandat: Produire les cinq volets manquants de la tache T1a du plan de revision du 13/09 (§1c classes d'ex aequo et conventions de departage sur Argyle + top-1 de B-oracle ; §1d TPR en escalier a FPR = 0,1 % sur Park et Twin ; §1e Spearman n = 12 sur les paires ; §1f 36,4 % en grappes par configuration ; §1g baseline demographique en monde ouvert sous A-LLR), avec bassin strictement constant entre conditions et baseline recalculee dans chaque condition de comparaison.
agent: mesures / T1a complements (§1c-§1g), 13/09
ecriture: analyses/c7_t1a_complements.py, resultats/c7-t1a-complements-preenregistrement.md, resultats/c7-t1a-complements-resultats.md, resultats/c7-t1a-complements.csv
lecture_seule: tout le reste du depot
interdits: appel de modele payant, reseau, recherche web, arriere-plan, commit sur master, fusion, modification d'un script existant, ecriture hors des quatre fichiers ci-dessus, toute ecriture dans article/
cout_reel_usd: 0.00

---

## 0. Avertissement liminaire — ce fichier n'est pas un préenregistrement au sens du dépôt

**Les cinq volets décrits ici sont POST HOC et NON PRÉENREGISTRÉS.**

Ils ont été conçus **après** le début des révisions, par des relecteurs hostiles qui avaient
déjà lu le PDF de soumission et ses résultats (`resultats/relecture-fond-2026-09-13.md`), puis
prescrits par `resultats/plan-revision-2026-09-13.md` §3, tâche T1a. Aucun plan ne les précédait.
Ils sont donc **post-hoc par rapport au préenregistrement d'origine** de C7.

Ce dépôt appelle « préenregistrement » un document écrit **avant le premier calcul**, et il en
fait un argument de crédibilité — quatorze prédictions réfutées sont tabulées dans le manuscrit
sur cette base. Introduire silencieusement, dans le même article, des mesures construites après
coup sous un nom qui laisse croire le contraire serait exactement le défaut que ce dispositif
prétend corriger.

Donc, en toutes lettres, **et à reproduire partout où ces chiffres apparaissent, manuscrit
compris** :

> **Les cinq volets de ce fichier sont post-hoc et non préenregistrés.** Ils ont été construits
> après avoir vu les résultats qu'ils mesurent, en réponse à une relecture adverse. Ils ne
> comptent dans aucun dénominateur de multiplicité préenregistré, ils ne peuvent réfuter aucune
> prédiction préenregistrée, et le manuscrit doit les présenter comme tels.

Ce que ce fichier fixe malgré tout, et qui garde une valeur : le protocole ci-dessous, les
graines et la règle d'arrêt (§7) sont écrits **avant le premier calcul** et commités dans un
commit séparé, antérieur à celui du script et des résultats. Ce qui n'est **pas** protégé —
le choix des mesures — est déclaré comme non protégé.

Décision de publication : option (a) de la décision D2 du plan de révision (§5). Cette décision
est prise en amont ; ce fichier l'exécute.

## 0 bis. Ce que ce fichier NE fait pas

**§1a (courbe top-1 vs k items) et §1b (Argyle sous A-LLR et monde ouvert) ne sont pas refaits
ici.** Ils existent déjà, sur la branche `agent/mesures/temoins-relecture` (commit 048a5d2) :
`analyses/c7_temoins_relecture.py` et `resultats/c7-temoins-relecture.csv`. Ce travail-ci est
strictement le **complément** §1c-§1g, et ne réimplémente, ne modifie et ne recopie aucune ligne
de ce script ni de `analyses/c7_reidentification.py`.

---

## 1. §1c — Argyle 2023 : ex æquo, conventions de départage encadrantes, B-oracle

**Ce que le plan prescrit** (T1a, ligne §1c) : « Argyle : distribution des classes d'ex aequo au
rang 1 ; top-1 sous les deux conventions encadrantes ; Clopper-Pearson ; différence appariée
jumeau − B-demo ; **top-1 de B-oracle** ». Sert R1 geste 4 et R13.

**Bassin.** `c7_argyle.charger()`, puis les seules personnes dont les **12** items sont tous
renseignés. Ce bassin est calculé **une fois** et sert à **toutes** les conditions de ce volet :
jumeaux, B-demo, B-oracle. Aucune condition ne re-tranche le bassin. C'est le piège qui a déjà
coûté deux erreurs à ce projet ; il est fermé ici par construction (une seule variable `h`).

**Conditions, toutes sur ce bassin et ce pool.**
- les trois jumeaux GPT-3 publiés par l'équipe Argyle ;
- **B-demo** = `c7_argyle.baseline_demographique` (quatre variables démographiques, imputation
  laisse-un-dehors, k = 10), **recalculée sur ce bassin** ;
- **B-oracle** = `c7_argyle.baseline_oracle` (les onze vraies réponses aux autres items,
  laisse-un-dehors, k = 10), **recalculée sur ce bassin**.

**Score.** Accord de Hamming, `1 − a2_commun.distance_hamming`, identique pour les trois
conditions. Aucune attaque différente d'une condition à l'autre.

**Les trois conventions de départage, sur la même matrice de score.** À 12 items binaires ou
quasi binaires, le score de tête est massivement ex æquo. Les trois valeurs sont trois lectures
de **la même** matrice, pas trois expériences :

| convention | définition opératoire |
|---|---|
| **en faveur de l'attaquant** | la vraie personne est comptée top-1 dès qu'elle est dans la classe de score maximal (rang optimiste = 1) |
| **espérance sous départage uniforme** | chaque personne compte 1/|classe| si elle est dans la classe de tête, 0 sinon — c'est la convention **publiée** |
| **contre l'attaquant** | la vraie personne n'est comptée top-1 que si sa classe de tête est un singleton (rang pessimiste = 1) |

**Distribution des classes d'ex æquo au rang 1.** Publiées : nombre de personnes dont la vraie
ligne appartient à la classe de tête ; taille médiane, moyenne, maximum et quantiles de cette
classe. Le maximum et la médiane sont ce que R1 geste 4 demande au lecteur de savoir.

**Clopper-Pearson.** Intervalle binomial exact sur le nombre de succès du jumeau principal sous
la convention publiée. **Nom de colonne : `ic_clopper_pearson_*`.** Ce n'est pas un bootstrap et
il ne sera jamais présenté comme tel.

**Différence appariée jumeau − B-demo.** Mêmes personnes, indicatrice par personne, différence
par personne, IC 95 % par bootstrap **sur les personnes** (`a2_commun.bootstrap_personnes`).
Un taux sans sa baseline appariée ne vaut rien : la baseline est recalculée dans cette condition
exacte, jamais empruntée.

**Complément explicitement hors du tableau §1c, et déclaré comme tel.** R1 geste 4 se termine par
« à 60 items la classe médiane vaut 1 et la métrique est saine ». Cette phrase porte sur
**Twin-2K-500 à 60 items**, pas sur Argyle, et aucun volet du plan ne la produit. Elle est donc
mesurée ici — distribution des classes d'ex æquo au rang 1 sur les 2 058 personnes de Twin aux
60 items communs, même définition qu'Argyle — et **signalée comme un ajout au plan**, sans quoi
la correction R1 geste 4 resterait à moitié non sourcée.

## 2. §1d — Park et Twin à FPR = 0,1 % : la valeur en escalier

**Ce que le plan prescrit** (T1a, ligne §1d) : « Park et Twin à FPR = 0,1 % : TPR en escalier,
nombre de FP absolus, nombre de seuils à moins de 1,5 FP, étendue des TPR admissibles ; **idem à
1 % pour montrer que ça tient** ». Sert R9.

**Bassin et score.** `c7_fort_monde_ouvert_ic.charger_stanford()` et `charger_twin()`, importés
sans modification — ce sont les chargeurs qui ont produit les chiffres publiés. Score A-LLR hors
pli : `c7_attaquant_fort.scores_hors_pli`, importée sans modification. Monde ouvert :
`c7_monde_ouvert.marges_deux_regimes` puis `roc_et_taux`, inchangées.

**Vérification de raccordement, posée avant calcul.** Le volet n'est interprété que si la
reproduction retombe sur les chiffres publiés : Park monde fermé 90,40 %, TPR@1 % 60,17 %,
TPR@0,1 % 44,37 % ; Twin 23,23 %, 4,28 %, 1,01 %. Écart au-delà de la deuxième décimale →
arrêt et remontée.

**Les quatre grandeurs par jeu et par FPR cible (0,1 % et 1 %).**
1. **TPR en escalier** = le plus grand TPR parmi les seuils dont le FPR est **≤ cible**. C'est la
   grandeur conservatrice ; elle ne dépend d'aucune interpolation ni d'aucun tri.
2. **Nombre de faux positifs absolus** au seuil retenu, et granularité d'un seul FP (1/n).
3. **Nombre de seuils distincts** dont le FPR est à moins de **1,5 faux positif** de la cible.
4. **Étendue des TPR admissibles** sur ces seuils : minimum, maximum, amplitude.

**Et la valeur publiée à côté**, celle de `np.interp`, pour que l'écart soit visible sans avoir à
le chercher.

## 3. §1e — Spearman n = 12 : bootstrap sur les paires

**Ce que le plan prescrit** (T1a, ligne §1e) : « Spearman n = 12 : bootstrap sur les **paires**,
Fisher-z, permutation ». Sert R10.

**Données.** `resultats/c7-compromis.csv`, colonnes `fidelite_plancher` et `fuite_top1`, les 12
configurations. Aucun recalcul de fidélité ni de fuite : le volet porte sur l'**unité de
rééchantillonnage**, pas sur les valeurs.

**Quatre quantités.**
1. rho observé (vérification de raccordement : doit retomber sur 0,9580) ;
2. **bootstrap sur les paires** : rééchantillonnage des 12 **configurations** avec remise,
   20 000 tirages, graine fixée ; percentiles 2,5 et 97,5. Les tirages dégénérés (moins de trois
   configurations distinctes, rho indéfini) sont **écartés et comptés**, jamais remplacés.
   Est aussi publiée la **part de tirages dont rho vaut exactement 1,000**, qui est le
   diagnostic de collage à la borne.
3. **Fisher-z**, avec l'écart-type de Bonett-Wright propre au Spearman,
   `sqrt(1,06/(n−3))`, et — pour que l'écart soit visible — la version naïve `1/sqrt(n−3)` ;
4. **permutation** : rho sous permutation aléatoire de l'axe de fuite, 10 000 permutations,
   p bilatéral avec la correction (compte + 1)/(B + 1).

**Nommage, non négociable.** Les percentiles de la loi de permutation sont une **loi nulle** ;
ils sont nommés `percentile_loi_nulle_*` et ne sont **jamais** appelés intervalle de confiance.
Les bornes du bootstrap sur les paires sont nommées `ic_bas` / `ic_haut`. Ce projet s'est déjà
trompé dessus.

## 4. §1f — Le 36,4 % : intervalle en grappes par configuration

**Ce que le plan prescrit** (T1a, ligne §1f) : « 36,4 % : bootstrap **en grappes par
configuration**, bootstrap naïf, étendue, écart-type ». Sert R12.

**Données.** `resultats/c7-transfert-voletA.csv`, lignes `n_items == 60`, en excluant les paires
dont l'une des extrémités est `Demographics Only - GPT4.1-mini` : il reste **30 paires ordonnées
issues de 6 configurations**, moyenne attendue 36,380 %, témoin anti-artefact attendu 0,040 %.
Vérification de raccordement : écart au-delà de la troisième décimale → arrêt.

**Le problème d'unité, et comment il est traité.** Une paire ordonnée (x, y) appartient à **deux**
configurations. Il n'existe donc pas une seule grappe évidente. Trois définitions sont calculées
et **toutes trois publiées**, la troisième étant celle que le plan désigne :

| définition | construction |
|---|---|
| naïf sur les paires | rééchantillonnage des 30 paires avec remise (l'intervalle qui ignore la dépendance) |
| grappes par extrémité d'attaque (`config_x`) | tirage de 6 configurations avec remise, on garde toutes les paires dont `config_x` est tirée |
| **grappes sur les deux extrémités** | tirage de 6 configurations avec remise ; chaque paire est pondérée par le produit des multiplicités de ses deux extrémités — c'est-à-dire toutes les paires ordonnées reconstructibles depuis le tirage |

La **troisième** est l'intervalle à publier : c'est la seule qui traite la configuration comme
l'unité indépendante des **deux** côtés, ce que le §5.4 du manuscrit exige lui-même pour la loi
de distance (« the independent unit is the configuration, not the pair »).

**Granularité Monte-Carlo déclarée d'avance.** À 6 grappes seulement, la loi de rééchantillonnage
est très discrète : les percentiles sautent de plusieurs dixièmes de point d'une graine à
l'autre. La sensibilité à la graine est donc **mesurée et publiée** (cinq graines), et l'intervalle
retenu est celui de la graine du dépôt. **Aucune graine ne sera choisie pour rapprocher un
résultat de celui du relecteur.**

**Aussi publiés** : minimum, maximum, écart-type et quartiles des 30 paires. Ne jamais publier la
moyenne nue d'une distribution qui court de 12 % à 84 % : c'est l'objet même de R12.

## 5. §1g — La baseline démographique en monde ouvert sous A-LLR

**Ce que le plan prescrit** (T1a, ligne §1g) : « baseline démographique en **monde ouvert sous
A-LLR** (Park et Twin, deux FPR) », portée depuis `analyses/c7_attaquant_fort.py`. Sert R15.

**Le défaut à combler.** `resultats/c7-monde-ouvert.csv` donne les comparateurs statistiques à
0,0000 % aux deux FPR — **sous l'attaque naïve uniquement**. La phrase du §5.3 « Statistical
comparators stay indistinguishable from noise at both FPRs » est donc établie contre une attaque
que l'article lui-même démontre faible sur ce jeu (65,51 → 90,40 %).

**Bassin strictement constant — c'est ici que le piège est le plus cher.** Pour chaque jeu, le
pool, l'ensemble des personnes attaquées et les colonnes d'items sont fixés **une seule fois**,
par le chargeur, et servent à la cible **comme** au comparateur. La cible et le comparateur sont
recalculés **dans le même appel**, l'un après l'autre, sur ces mêmes objets. Le top-1 en dépend
mécaniquement.

**Conditions par jeu.**
- **Park (Stanford)** : cible `Meilleur agent (composite)` ; comparateur démographique
  `codes_gss[DEMO_COND]` ; pool `codes_gss[VAGUE1]`, 1 052 personnes, 177 items.
- **Twin** : cible `JSON Persona - GPT4.1` ; comparateur démographique
  `Demographics Only - GPT4.1-mini` ; pool `humains vague 4` restreint aux items communs,
  2 058 personnes, 60 items.

**Attaques, les deux, sur les mêmes objets.**
- **naïve** (accord de Hamming), qui doit redonner les 0,0000 % de `c7-monde-ouvert.csv` — c'est
  la vérification de raccordement du volet ;
- **A-LLR hors pli** (`scores_hors_pli`, importée sans modification), pour la cible **et** pour
  le comparateur. C'est tout l'objet de R15 : le comparateur du chiffre de tête doit recevoir le
  même traitement que la cible.

**Mesures.** Monde fermé top-1 ; AUC ; TPR aux deux FPR par `np.interp` (comme publié) **et** en
escalier (comme §1d, puisque §1d établit que l'interpolation n'est pas identifiée à 0,1 %) ;
nombre de vraies détections absolues et de faux positifs absolus au seuil retenu.

**Ajout déclaré, au-delà du plan.** Le plan prescrit la seule baseline démographique. La phrase
du §5.3 dit « comparators » au pluriel, et `c7-monde-ouvert.csv` en porte **deux** : le
comparateur démographique et `PMM k=10`. Le second est donc traité à l'identique, et l'ajout est
signalé comme tel. Le coût est de quelques secondes.

**Règle de décision.** La même que partout dans ce projet : le candidat ne dépasse le comparateur
que si la borne basse de son IC 95 % bootstrap sur les personnes est **strictement** supérieure à
la borne haute de l'IC du comparateur recalculé sur le même bassin. Appliquée ici en monde fermé,
où l'indicatrice par personne existe. En monde ouvert la TPR à FPR fixe n'est pas une moyenne
d'indicatrices par personne : aucun IC bootstrap n'y est fabriqué, et les comptes absolus sont
publiés à la place.

## 6. Contrôle d'interprétabilité, avant toute interprétation

`analyses/c7_controle_interpretabilite.py` est la fonction canonique du dépôt. Elle ne prend
jamais de valeur de baseline en argument : elle la recalcule elle-même sur le même bassin et les
mêmes items. Elle est appelée **avant** toute interprétation de quelque volet que ce soit, et son
verdict est publié qu'il arrange ou non.

- **Twin à 60 items** (complément de §1c, et cible de §1g) :
  `c7_controle_interpretabilite.controle_avant_interpretation`, telle quelle.
- **Argyle** (§1c) : `c7_argyle.controle_avant_interpretation`, qui porte la même règle de
  décision pour un jeu qui n'est pas Twin.
- **§1g sous A-LLR** : la même règle de décision, candidat et comparateur tous deux sous A-LLR,
  écrite explicitement puisqu'aucune fonction canonique ne prend l'attaque en argument.
- **§1d, §1e, §1f** : ces trois volets ne comparent pas un candidat à une baseline — ils
  requalifient l'incertitude de grandeurs déjà publiées. Le contrôle d'interprétabilité n'y a pas
  d'objet, et cette absence est déclarée plutôt que maquillée par un appel décoratif.

## 7. Règle d'arrêt et traitement des écarts — posée avant toute comparaison

Le plan de révision annonce, pour §1c : 0,6052 % / 0,1350 % / 0,0466 %, classe de tête de
13 personnes sur 2 148, médiane 3, maximum 93, B-oracle 0,1399 %, différence appariée +0,044 pt
IC [−0,105 ; +0,197], Clopper-Pearson [0,0288 ; 0,4076]. Pour §1d : 50,19 % (Park, 1 FP absolu),
538 seuils, étendue 0,10-50,95 % ; Twin 1,26 % (2 FP), étendue 0,05-1,80 %. Pour §1e :
[0,749 ; 1,000], Fisher-z [0,848 ; 0,989], 13,8 % des tirages à rho = 1,000, permutation
p < 10⁻⁴. Pour §1f : [24,7 ; 55,9] en grappes, [30,2 ; 43,2] en naïf, étendue 11,9-83,6 %,
écart-type 18,6 pts.

**Ces valeurs ne sont pas des cibles.** La règle, posée ici avant le premier calcul :

1. Les chiffres publiés sont **les miens**, issus de `resultats/c7-t1a-complements.csv`, jamais
   recopiés du plan ni des rapports de relecture.
2. Tout écart est **rapporté comme écart**, avec l'hypothèse la plus plausible sur son origine.
   **Aucun paramètre, aucune graine, aucun protocole, aucun bassin ne sera modifié pour réduire
   un écart.**
3. Les seuls déclencheurs d'arrêt et de remontée au responsable :
   - une **vérification de raccordement** qui échoue (§1d : 90,40 / 60,17 / 44,37 / 23,23 / 4,28 /
     1,01 ; §1e : rho 0,9580 ; §1f : 36,380 % et témoin 0,040 % ; §1g : comparateurs à 0,0000 %
     sous l'attaque naïve) ;
   - un **renversement de sens** : le comparateur de §1g cesserait d'être au bruit sous A-LLR, ou
     la convention de départage la plus défavorable à l'attaquant placerait le jumeau Argyle
     au-dessus de sa baseline démographique.
   Un tel résultat ne serait pas publié sans arbitrage.
4. **Un volet irréalisable est déclaré irréalisable**, avec ce qu'il faudrait pour le produire.
   Aucun chiffre n'est fabriqué, aucun n'est recopié d'un rapport pour combler un trou. Ce projet
   a déjà publié un nombre non sourcé, puis l'a envoyé à un tiers.

## 8. Discipline de sortie

- Graine maîtresse **20260913**, fixée dans le code ; toute sous-graine dérivée par
  `graine_nom` (CRC32 stable, jamais `hash()`).
- **Aucune donnée individuelle n'est calculée, imprimée ou écrite** : ni identifiant, ni pid, ni
  identifiant ANES, ni liste d'appariements individuels. Seuls des taux, des comptes et des
  distributions agrégées sortent dans `resultats/`. Les tailles de classes d'ex æquo sont
  publiées en distribution (médiane, quantiles, maximum), jamais personne par personne.
- Colonnes du CSV nommées par ce qu'elles sont : `ic_bas`/`ic_haut` pour un bootstrap,
  `ic_clopper_pearson_*` pour un intervalle binomial exact, `percentile_loi_nulle_*` pour des
  percentiles d'une loi nulle. **Ces trois familles ne sont jamais mélangées.**
- Aucun appel de modèle de langage, aucune dépense, aucun réseau, aucune recherche web, aucune
  exécution en arrière-plan. Lecture seule sur `data/`. Aucun script existant modifié.
