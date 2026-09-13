# C7 — T1a §1c à §1g : résultats des cinq volets manquants — UN ÉNONCÉ BORNÉ le 13 septembre 2026

statut: provisoire
borne_par: resultats/c7-residu-trajectoire-resultats.md
fait_foi: resultats/c7-residu-trajectoire-resultats.md (pour le §2 « la dégénérescence frappe exactement le bout gauche » seulement ; le reste de ce rapport n'est pas visé)
mandat: Produire les cinq volets manquants de la tache T1a du plan de revision du 13/09 (§1c a §1g), avec bassin strictement constant entre conditions et baseline recalculee dans chaque condition de comparaison, et livrer la fiche de report des chiffres qui debloquent R1 geste 4, R9, R10, R12 et R15.
agent: mesures / T1a complements (§1c-§1g), 13/09
ecriture: analyses/c7_t1a_complements.py, resultats/c7-t1a-complements-preenregistrement.md, resultats/c7-t1a-complements-resultats.md, resultats/c7-t1a-complements.csv
lecture_seule: tout le reste du depot
interdits: appel de modele payant, reseau, recherche web, arriere-plan, commit sur master, fusion, modification d'un script existant, toute ecriture dans article/
cecite: Aucune verification reseau. Les valeurs annoncees par le plan de revision et par les rapports de relecture n'ont servi qu'a la verification de raccordement ; aucune n'a ete recopiee. Le statut des annexes dans le decompte des 12 pages PoPETs 2027 n'est pas verifie et ne l'est pas ici.
cout_reel_usd: 0.00

> ## BORNÉ, le 13/09/2026 — « la dégénérescence frappe exactement le bout gauche » vaut à items BRUTS, pas à information appariée
>
> **État : BORNÉ.** Fait foi : `resultats/c7-residu-trajectoire-resultats.md`, §7.
>
> Le §2 ci-dessous (§1c bis, « Twin à 60 items : la métrique y est saine ») conclut que la
> classe d'ex æquo médiane vaut 1 à 60 items, que le contraste entre conventions de
> départage n'y vaut qu'un facteur **1,32**, contre un facteur **13** à 12 items sur
> Argyle, et que **« la dégénérescence frappe exactement le bout gauche de la trajectoire
> — c'est vérifié, pas supposé »**.
>
> C'est vrai, et c'est vrai **à 60 items bruts seulement**. Une fois l'information
> effective appariée entre les deux bouts, le bout **droit** dégénère aussi, et plus fort
> que le gauche : à M2 la classe d'ex æquo de tête compte 11,5 candidats en médiane, et le
> taux publié de 0,341 % est un point à l'intérieur d'une plage de **facteur 130** fixée
> par la seule convention de départage (0,032 % à 4,193 % selon la convention ;
> `c7-residu-trajectoire-resultats.md` §7).
>
> **Interdit à partir d'ici :** présenter la dégénérescence des ex æquo comme une
> propriété **asymétrique** de la trajectoire, ou comme un argument qui disqualifie le
> bout gauche sans toucher le bout droit. À information appariée, les deux bouts en
> dépendent, et c'est le *rapport à la baseline* qui résiste (2,53 en espérance), pas le
> taux nu.
>
> **Le reste de ce rapport n'est pas visé** : §1c, §1d, §1e, §1f, §1g et la fiche de
> report du §7 ne sont pas touchés par ce bornage.

---

> ## AVERTISSEMENT — POST HOC, NON PRÉENREGISTRÉ
>
> **Les cinq volets de ce fichier ont été produits APRÈS le début des révisions**, en
> réponse à une relecture adverse, puis prescrits par
> `resultats/plan-revision-2026-09-13.md` §3 (tâche T1a). Ils sont donc **post-hoc par
> rapport au préenregistrement d'origine de C7**. Le fichier
> `resultats/c7-t1a-complements-preenregistrement.md` fixe leur protocole **avant le
> premier calcul** — mais pour des mesures **choisies après coup**, et il le dit.
>
> Ils ne comptent dans **aucun dénominateur de multiplicité préenregistré**, ils ne
> peuvent **réfuter aucune prédiction préenregistrée**, et le manuscrit doit les
> présenter comme tels. **Ne les présentez jamais comme préenregistrés.**

> ## ⚠ REMONTÉE AU RESPONSABLE — §1g déclenche la règle d'arrêt
>
> **Sur l'archive Park, le comparateur démographique ne reste PAS au bruit sous
> l'attaquant fort.** Sous A-LLR il atteint **85,17 %** de top-1 en monde fermé et
> **29,09 %** de TPR à 1 % de FPR, contre 2,24 % et 0,00 % sous l'attaque naïve. La
> phrase du §5.3 « *Statistical comparators stay indistinguishable from noise at both
> FPRs* » est **fausse sur Park sous l'attaque que l'article met en avant**.
>
> C'est exactement le cas prévu par R15 (« si le comparateur ne reste pas au bruit,
> c'est une mauvaise nouvelle qu'il vaut mieux découvrir avant le comité ») et par la
> règle d'arrêt §7.3 du préenregistrement (« renversement de sens »). **La mesure est
> publiée ; la décision de rédaction ne m'appartient pas.** Détail en §5, formulations
> candidates en §7.
>
> **Sur Twin, la phrase tient** : le comparateur démographique reste à 0,0000 % à
> 0,1 % de FPR et à 0,0486 % — une seule personne — à 1 % de FPR.

## 0. Ce qui a été produit, et ce qui ne l'a pas été

| volet du plan | état | sert |
|---|---|---|
| §1a courbe top-1 vs nombre d'items | **déjà fait ailleurs**, non refait ici — branche `agent/mesures/temoins-relecture`, commit 048a5d2 | R1 geste 2 |
| §1b Argyle sous A-LLR et monde ouvert | **déjà fait ailleurs**, idem | R1 geste 3 |
| **§1c** ex æquo, conventions encadrantes, B-oracle | **produit** | R1 geste 4, **R13** |
| **§1c bis** classes d'ex æquo de Twin à 60 items | **produit — ajout déclaré, hors du tableau du plan** (voir §8) | R1 geste 4 |
| **§1d** TPR en escalier à FPR = 0,1 % et 1 % | **produit** | R9 |
| **§1e** Spearman n = 12, bootstrap sur les paires | **produit** | R10 |
| **§1f** 36,4 % en grappes par configuration | **produit** | R12 |
| **§1g** comparateurs en monde ouvert sous A-LLR | **produit — et il renverse le sens de R15** | R15 |

**Aucun volet n'a été déclaré irréalisable.** Les cinq sont produits, sur données locales,
sans réseau et sans dépense. Le coût total est de **3 min 53 s** de calcul local.

**Toutes les vérifications de raccordement passent**, à la tolérance posée avant calcul :
Park monde fermé A-LLR 90,3992 % (publié 90,40), TPR@1 % 60,1711 % (60,17), TPR@0,1 %
44,3722 % (44,37) ; Twin 23,2264 % (23,23), 4,2760 % (4,28), 1,0113 % (1,01) ; rho de
Spearman 0,958042 (0,9580) ; moyenne des 30 paires 36,3796 % (36,380) ; témoin
anti-artefact 0,0402 % (0,040). Le portage reproduit donc bien les chaînes publiées, et
ce qui suit porte sur ce que ces chiffres autorisent à dire, pas sur les chiffres
eux-mêmes.

Source de toutes les valeurs ci-dessous : `resultats/c7-t1a-complements.csv`, 394 lignes,
produit par `analyses/c7_t1a_complements.py`.

---

## 1. §1c — Argyle 2023 : les trois conventions de départage, et B-oracle

**Bassin unique, partagé par toutes les conditions** : 2 148 personnes dont les 12 items
sont tous renseignés, hasard = 0,0466 %. Jumeaux, B-demo et B-oracle attaquent **le même
pool**, avec **le même score** (accord de Hamming). Les trois conventions sont trois
lectures de **la même matrice**, pas trois expériences.

### 1.1 Le top-1 dépend de la convention d'un facteur 13

| condition | ex æquo **en faveur** | **espérance uniforme** (publié) | ex æquo **contre** |
|---|---|---|---|
| **GPT-3 davinci (temp. principale)** | **0,6052 %** [0,3259 ; 0,9777] | **0,1350 %** [0,0450 ; 0,2691] | **0,0466 %** [0,0000 ; 0,1397] |
| GPT-3 davinci (temp. 0,01) | 0,4655 % [0,1862 ; 0,7914] | 0,0992 % [0,0366 ; 0,1696] | 0,0000 % |
| GPT-3 davinci (temp. 1,0) | 0,4655 % [0,1862 ; 0,7914] | 0,0901 % [0,0139 ; 0,2149] | 0,0466 % [0,0000 ; 0,1862] |
| **B-demo** (4 variables démographiques, LOO k=10) | 0,5121 % [0,2328 ; 0,8380] | 0,0913 % [0,0211 ; 0,2032] | 0,0466 % [0,0000 ; 0,1397] |
| **B-oracle** (11 vraies réponses, LOO k=10) | 0,7914 % [0,4190 ; 1,1639] | **0,1399 %** [0,0750 ; 0,2183] | 0,0000 % |

Intervalles : **bootstrap 95 % sur les personnes**, 2 000 tirages, graine fixée.

Les trois valeurs du jumeau principal — **0,6052 % / 0,1350 % / 0,0466 %** — reproduisent
à la quatrième décimale celles que le plan cite comme attendues. **0,0466 % est exactement
le hasard** (1/2 148).

### 1.2 Les classes d'ex æquo, et pourquoi la dégénérescence frappe le bout gauche

| condition | personnes dans la classe de tête | taille médiane | moyenne | max | part de singletons |
|---|---|---|---|---|---|
| GPT-3 davinci (temp. principale) | **13** sur 2 148 | **3** | 5,65 | **93** | 28,54 % |
| GPT-3 davinci (temp. 0,01) | 10 | 2 | 4,20 | 38 | 37,20 % |
| GPT-3 davinci (temp. 1,0) | 10 | 3 | 6,61 | 105 | 28,58 % |
| B-demo | 11 | 3 | 5,93 | 47 | 30,87 % |
| B-oracle | 17 | 3 | 6,37 | 49 | 27,00 % |

**13 personnes sur 2 148, médiane 3, maximum 93** : identique aux valeurs attendues.

### 1.3 Le test exact, et la différence appariée qui décide

Convention publiée, jumeau principal : 3 succès attendus arrondis sur 2 148.

- **Clopper-Pearson (intervalle binomial exact, PAS un bootstrap)** : **[0,0288 % ;
  0,4076 %]**, colonnes `ic_clopper_pearson_bas` / `ic_clopper_pearson_haut`.
- p binomial exact (jumeau > hasard) : **0,080**. Non significatif.

**Différence appariée jumeau − B-demo, mêmes personnes, baseline recalculée sur ce bassin**,
en points de pourcentage :

| convention | différence appariée | IC 95 % bootstrap sur les personnes |
|---|---|---|
| en faveur de l'attaquant | +0,0931 pt | [−0,3259 ; +0,5121] |
| **espérance uniforme (publiée)** | **+0,0437 pt** | **[−0,1163 ; +0,1907]** |
| contre l'attaquant | +0,0000 pt | [−0,1397 ; +0,1397] |

**Les trois intervalles contiennent zéro.** C'est le fait qui fonde R1 geste 1 : la phrase
défendable n'est pas « au niveau du hasard » — qui n'est vraie que sous une convention sur
trois — mais **« indistinguable de la baseline démographique recalculée sur le même
bassin »**, qui survit aux trois.

Le **contrôle d'interprétabilité canonique** (`c7_argyle.controle_avant_interpretation`,
qui recalcule lui-même la baseline sur ce bassin) **échoue pour les trois jumeaux GPT-3**,
comme attendu : candidat 0,1443 % [0,0512 ; 0,2677] contre baseline 0,1001 %
[0,0163 ; 0,2258], IC chevauchants.

### 1.4 B-oracle, et ce que ça fait à R13

**B-oracle atteint 0,1399 % [0,0750 ; 0,2183]**, contre **0,1350 % [0,0450 ; 0,2691]** pour
le jumeau. Différence appariée jumeau − B-oracle : **−0,0049 pt, IC [−0,1311 ; +0,1366]**.

**Égalité, à l'intérieur du bruit de départage.** Le plus proche voisin qui détient les
onze mêmes vraies réponses n'identifie pas mieux que le jumeau GPT-3 — il porte plus de
bits (0,342 contre 0,094, §5.8 du manuscrit). « Identifies 3.6 times better » est vrai en
bits et faux en top-1 : c'est exactement R13.

---

## 2. §1c bis — Twin à 60 items : la métrique y est saine (ajout déclaré)

**Ce volet n'est pas dans le tableau T1a du plan.** Il est produit parce que R1 geste 4 se
termine par « à 60 items la classe médiane vaut 1 et la métrique est saine », et
qu'**aucun volet du plan ne produit ce chiffre**. Sans lui, la dernière phrase de R1
geste 4 resterait non sourcée. Même définition de classe d'ex æquo qu'au §1c.

Bassin : 2 058 personnes, 60 items communs, 2 058 jumeaux couverts. Le **contrôle
canonique** (`c7_controle_interpretabilite`) **passe** : candidat 20,6948 % contre
baseline 2,1526 %.

| condition | classe médiane | moyenne | max | singletons | en faveur | uniforme | contre |
|---|---|---|---|---|---|---|---|
| JSON Persona - GPT4.1 | **1** | 1,48 | 11 | **71,33 %** | 24,1011 % | 20,6940 % | 18,3188 % |
| Demographics Only - GPT4.1-mini | **1** | 1,54 | 9 | 66,47 % | 2,6725 % | 2,1453 % | 1,7979 % |

**La classe médiane vaut bien 1 à 60 items.** Et le contraste entre conventions y est
d'un facteur **1,32** (24,10 / 18,32), contre un facteur **13** à 12 items sur Argyle
(0,6052 / 0,0466). **La dégénérescence frappe exactement le bout gauche de la
trajectoire** — c'est vérifié, pas supposé.

---

## 3. §1d — La valeur en escalier : le 44,37 % n'est pas identifié

Fonction ROC en escalier exacte : le plus grand TPR dont le FPR reste ≤ cible. Aucun tri
instable, aucune interpolation.

### 3.1 À FPR = 0,1 % — la grandeur n'est pas identifiée

| jeu | escalier | FP absolus | vraies détections | `np.interp` (publié) | seuils à < 1,5 FP | étendue admissible |
|---|---|---|---|---|---|---|
| **Park** (A-LLR) | **50,1901 %** | **1** | 528 | 44,3722 % | **538** | **0,0951 % – 50,9506 %** (50,86 pts) |
| **Twin** (A-LLR) | **1,2634 %** | **2** | 26 | 1,0113 % | 39 | **0,0486 % – 1,7979 %** (1,75 pt) |

Sur Park, **538 seuils distincts** tombent à moins de 1,5 faux positif de la cible, et
leur TPR s'étale sur **50,86 points**. Le 44,37 % publié est la sortie de `np.interp` sur
un axe des abscisses où des centaines de valeurs de FPR sont identiques : la valeur
dépend de l'implémentation du tri. **Écrire « estimation très instable » est trop faible :
la grandeur n'est pas identifiée par les données à ce FPR.**

### 3.2 À FPR = 1 % — tout tient, et c'est le chiffre à mettre en avant

| jeu | escalier | FP absolus | `np.interp` (publié) | seuils à < 1,5 FP | étendue admissible |
|---|---|---|---|---|---|
| **Park** (A-LLR) | **60,1711 %** | 10 | 60,1711 % | 7 | 59,9810 % – 60,3612 % (**0,38 pt**) |
| **Twin** (A-LLR) | **4,2760 %** | 20 | 4,2760 % | 4 | 4,2760 % – 4,3246 % (**0,05 pt**) |

**Escalier et interpolation coïncident à la quatrième décimale sur les deux jeux.** Les
deux chiffres de tête sont solides ; R9 ne les touche pas.

Pour mémoire, sous l'attaque naïve : Park 8,3650 % en escalier à 0,1 % (contre 8,4738 %
publié, 23 seuils, étendue 0,0951-10,4563 %) et 20,1521 % à 1 % ; Twin 0,9232 % et
2,9640 %.

---

## 4. §1e — L'IC du Spearman fige les douze méthodes

12 configurations, `c7-compromis.csv`. rho observé **0,958042** (raccordement OK).

| intervalle | valeur | ce qu'il rééchantillonne |
|---|---|---|
| **publié** | [0,9301 ; 0,9930] | les **personnes** à l'intérieur de chaque configuration, les 12 configurations et l'axe de fidélité figés |
| **bootstrap sur les paires** | **[0,7491 ; 1,0000]** | les **configurations** — la source dominante, et la seule sur laquelle porte « across 12 heterogeneous methods » |
| Fisher-z, Bonett-Wright `sqrt(1,06/(n−3))` | [0,8480 ; 0,9889] | approximation analytique, propre au Spearman |
| Fisher-z, naïf `1/sqrt(n−3)` | [0,8533 ; 0,9885] | approximation analytique, sous-estime pour un Spearman |

**13,96 % des 20 000 tirages du bootstrap sur paires donnent rho exactement 1,000** : à
n = 12 l'estimateur colle à sa borne. Aucun tirage n'a été écarté comme dégénéré.

**Permutation** (10 000 tirages) : p bilatéral = **1,0 × 10⁻⁴** — la plus petite valeur
atteignable à 10 000 permutations, donc **p < 10⁻⁴** est la lecture correcte. Percentiles
de la **loi nulle** 2,5 / 50 / 97,5 = **−0,5734 / 0,0000 / +0,5874**, colonnes
`percentile_loi_nulle_*`. **Ce ne sont pas des bornes d'intervalle de confiance et elles
ne sont pas dans `ic_bas`/`ic_haut`.**

Le verdict survit : l'ordre est massivement non nul. Ce qui ne survit pas, c'est la
lecture « l'observé est bien encadré » quand la bande de l'observé et la bande du nul ne
rééchantillonnent pas la même chose.

---

## 5. §1f — Le 36,4 % : l'unité indépendante est la configuration

30 paires ordonnées issues de **6 configurations**, 60 items. Moyenne **36,3796 %**,
témoin anti-artefact **0,0402 %** (raccordements OK).

**Dispersion** : minimum **11,912 %**, médiane 31,149 %, maximum **83,576 %**,
écart-type **18,565 points**, étendue 71,66 points.

| intervalle | valeur | ce qu'il traite comme indépendant |
|---|---|---|
| bootstrap naïf sur les paires | [30,15 ; 43,30] | la paire — **faux** : chaque configuration apparaît dans 10 des 30 paires |
| grappes par `config_x` seulement | [30,77 ; 41,07] | l'extrémité d'attaque — sous-estime encore la dépendance |
| **grappes sur les deux extrémités** | **[24,68 ; 56,47]** | **la configuration, des deux côtés** — à publier |

La troisième est la seule qui applique au chiffre du résumé la règle que le §5.4 énonce
lui-même pour la loi de distance : « *the independent unit is the configuration, not the
pair* ». Elle est **2,4 fois plus large** que le bootstrap naïf.

**Sensibilité Monte-Carlo, déclarée** : à 6 grappes la loi de rééchantillonnage est très
discrète. Sur 5 graines, la borne basse va de 24,41 à 24,68 % et la borne haute de 55,92
à 56,47 %. L'intervalle retenu est celui de la graine du dépôt ; **aucune graine n'a été
choisie pour rapprocher un résultat de celui du relecteur**, et l'enveloppe est publiée
dans le CSV (`sensibilite_monte_carlo_grappes_deux_extremites`).

---

## 6. §1g — Le comparateur sous A-LLR : la mauvaise nouvelle, et elle est solide

**Bassin strictement constant** : pour chaque jeu, le pool, les personnes attaquées et
les colonnes d'items sont fixés **une fois** par le chargeur canonique et servent à la
cible **comme** aux comparateurs, dans le même appel. La conformité au chargeur de
`c7_fort_monde_ouvert_ic` est vérifiée par assertion dans le code.

### 6.1 Park (archive Park et al., bloc GSS) — 1 052 personnes, 177 items

| condition | attaque | top-1 monde fermé | AUC | TPR @ 1 % FPR (escalier) | TPR @ 0,1 % FPR (escalier) |
|---|---|---|---|---|---|
| **cible** Meilleur agent (composite) | naïve | 65,4658 % [62,43 ; 68,24] | 0,5524 | 20,1521 % | 8,3650 % |
| **cible** Meilleur agent (composite) | **A-LLR** | **90,3992 %** [88,50 ; 92,11] | 0,8479 | **60,1711 %** | 50,1901 % |
| comparateur **démographique** | naïve | 2,2433 % [1,41 ; 3,16] | 0,0127 | **0,0000 %** | **0,0000 %** |
| comparateur **démographique** | **A-LLR** | **85,1711 %** [83,08 ; 87,26] | **0,7394** | **29,0875 %** | **17,0152 %** |
| PMM k=10 *(ajout déclaré)* | naïve | 0,5703 % | 0,0022 | 0,0000 % | 0,0000 % |
| PMM k=10 *(ajout déclaré)* | **A-LLR** | 1,0456 % [0,48 ; 1,71] | 0,0052 | **0,0000 %** | **0,0000 %** |

**Le comparateur démographique passe de 0,0000 % à 29,09 % de TPR à 1 % de FPR dès qu'on
l'arme de la même attaque que la cible.** La phrase du §5.3 est fausse sur Park.

**Ce n'est pas un artefact de câblage — c'est vérifié.** Témoin de permutation (5 tirages,
lignes du candidat permutées, pool / items / attaque / plis inchangés) : le top-1 A-LLR
du comparateur démographique retombe à **0,0951 %**, soit **exactement le hasard**
(1/1 052). Le signal est donc une **identité individuelle réelle**, que l'attaquant fort
extrait des 177 items et que l'attaque naïve laissait entièrement sur la table.

**Le contrôle d'interprétabilité passe encore**, mais de justesse : 88,50 % (borne basse
de la cible) contre 87,26 % (borne haute du comparateur), **1,24 point de marge**, là où
l'attaque naïve donnait 62,43 contre 3,16. **Le rapport cible / comparateur tombe de 29×
à 1,06× en monde fermé, et de ∞ à 2,07× à 1 % de FPR.**

### 6.2 Twin-2K-500 — 2 058 personnes, 60 items

| condition | attaque | top-1 monde fermé | AUC | TPR @ 1 % FPR (escalier) | TPR @ 0,1 % FPR (escalier) |
|---|---|---|---|---|---|
| **cible** JSON Persona - GPT4.1 | naïve | 20,7021 % [19,06 ; 22,45] | 0,1490 | 2,9640 % | 0,9232 % |
| **cible** JSON Persona - GPT4.1 | **A-LLR** | **23,2264 %** [21,52 ; 24,98] | 0,1769 | **4,2760 %** | 1,2634 % |
| comparateur **démographique** | naïve | 2,1040 % [1,54 ; 2,73] | 0,0128 | 0,1944 % | 0,0972 % |
| comparateur **démographique** | **A-LLR** | 0,7775 % [0,44 ; 1,17] | 0,0051 | **0,0486 %** (1 personne) | **0,0000 %** |
| PMM k=10 *(ajout déclaré)* | **A-LLR** | 0,2430 % | 0,0013 | **0,0000 %** | **0,0000 %** |

**Sur Twin la phrase tient, et se renforce même** : le comparateur démographique, armé de
l'attaquant fort, **descend** de 2,10 % à 0,78 % en monde fermé et de 0,1944 % à 0,0486 %
à 1 % de FPR. Rapport cible / comparateur à 1 % de FPR : **88×**.

Témoins de permutation sur Twin : 0,0194 % (cible), 0,0583 % et 0,0389 % (comparateurs),
contre un hasard de 0,0486 %. Tout est au bruit, comme il se doit.

### 6.3 Pourquoi les deux jeux divergent, et ce que ça implique

L'écart est cohérent : Park porte **177 items** contre 60 pour Twin. Un attaquant à
vraisemblance pondérée par la rareté accumule, sur 177 items, assez de signal
démographique faible par item pour ré-identifier — même quand le candidat ne « porte »
aucune personne au sens de l'accord brut. C'est **un résultat sur l'attaque**, pas sur le
générateur, et il coupe dans les deux sens :

- il **affaiblit** la lecture « le jumeau fuit au-delà de ce que la démographie donne »
  sur Park, où la marge s'effondre ;
- il **renforce** la thèse générale de l'article — le risque de liaison est réel même
  sans jumeau LLM, dès qu'on arme correctement l'attaquant ;
- il **ne touche pas** Twin-2K-500, où la séparation cible / comparateur est intacte.

**La décision de rédaction appartient au responsable** (voir §7, R15).

---

## 7. FICHE DE REPORT POUR LE MANUSCRIT

**Pour la passe T5. Je n'ai touché à aucun fichier de `article/`.**
Toutes les valeurs viennent de `resultats/c7-t1a-complements.csv`. Chaque ligne du CSV est
identifiée par le triplet (`volet`, `condition`, `mesure`) ; la colonne `attaque` sépare
naïf et A-LLR. **Chaque insertion doit être accompagnée de la mention post-hoc.**

---

### R1 geste 4 — Les conventions de départage encadrantes  ✅ débloqué

**Chiffres** : en faveur **0,6052 %** [0,3259 ; 0,9777] · espérance uniforme, publiée
**0,1350 %** [0,0450 ; 0,2691] · contre **0,0466 %** [0,0000 ; 0,1397] = exactement le
hasard. Classe de tête : **13 personnes sur 2 148**, médiane **3**, maximum **93**.
À 60 items sur Twin : classe médiane **1**, 71,33 % de singletons, maximum 11.

**Colonnes du CSV** — volet `1c ex aequo et B-oracle (Argyle)`, condition
`GPT-3 davinci (temp. principale)`, mesures `top1_ex_aequo_en_faveur_de_l_attaquant`,
`top1_esperance_departage_uniforme_PUBLIE`, `top1_ex_aequo_contre_l_attaquant` (valeurs
en `valeur`, bornes en `ic_bas`/`ic_haut`) ; `classe_tete_personnes_dans_la_classe`,
`classe_tete_taille_mediane`, `classe_tete_taille_max`. Pour les 60 items : volet
`1c bis ex aequo a 60 items (Twin, ajout hors plan)`, condition `JSON Persona - GPT4.1`,
mesure `classe_tete_taille_mediane`.

**Formulation prête à insérer (§5.8) :**

> Below 1 %, the top-1 rate on the 2023 corpus is fixed by the tie-breaking convention,
> not by the data: ties resolved in the attacker's favour give 0.61 % [0.33 ; 0.98],
> the uniform-draw expectation we report gives 0.135 % [0.045 ; 0.269], and ties resolved
> against the attacker give 0.047 % [0.000 ; 0.140] — exactly chance for a pool of 2,148.
> The leading tie class holds 13 of the 2,148 people, with a median of 3 candidates and
> a maximum of 93. At 60 items the median tie class is 1 and the measure is well behaved:
> the degeneracy is specific to the left-hand end of the trajectory.
> *(Post-hoc, not preregistered; T1a §1c and §1c bis.)*

---

### R9 — Le 44,37 % n'est pas identifié  ✅ débloqué

**Chiffres** — Park, FPR = 0,1 % : escalier **50,19 %** sur **1** faux positif absolu
(528 vraies détections) ; **538 seuils** à moins de 1,5 FP de la cible ; étendue
admissible **0,10 % – 50,95 %**, soit **50,86 points**. Twin, FPR = 0,1 % : escalier
**1,26 %** sur **2** FP absolus ; 39 seuils ; étendue **0,05 % – 1,80 %**.
À 1 % de FPR : Park **60,17 %** (10 FP, 7 seuils, étendue **0,38 pt**), Twin **4,28 %**
(20 FP, 4 seuils, étendue **0,05 pt**) — escalier et interpolation coïncident.

**Colonnes du CSV** — volet `1d TPR en escalier`, jeu `Park GSS` / `Twin`, attaque
`A-LLR (hors pli)`, avec `fpr_cible` = 0.001 ou 0.01, mesures
`tpr_a_fpr_0_1pct_tpr_escalier`, `tpr_a_fpr_0_1pct_fp_absolus`,
`tpr_a_fpr_0_1pct_n_seuils_a_moins_de_1_5_fp`, `tpr_a_fpr_0_1pct_tpr_admissible_min` /
`_max`, `tpr_a_fpr_0_1pct_np_interp_PUBLIE` (et les mêmes en `tpr_a_fpr_1pct_*`).

**Formulation prête à insérer (§5.3), option « escalier » recommandée par D3 :**

> At FPR = 0.1 % the quantity is **not identified by the data**: the threshold rests on a
> single absolute false positive on Park and two on Twin. The conservative step-function
> value — the largest TPR whose FPR stays at or below the target — is 50.19 % on Park and
> 1.26 % on Twin; 538 distinct thresholds on Park sit within 1.5 false positives of the
> target, and their TPRs span 0.10 % to 50.95 %. We therefore report no point estimate at
> this FPR. At FPR = 1 % the same construction is stable: 60.17 % on Park (10 absolute
> false positives, 7 nearby thresholds, a 0.38-point span) and 4.28 % on Twin (20, 4,
> 0.05 point). The headline figures are the ones at 1 % FPR.
> *(Post-hoc, not preregistered; T1a §1d.)*

**Propagation obligatoire** : la figure 1 grave « 44.4 % » et « 0.9 % ». Tâche T6.

---

### R10 — L'IC du Spearman fige les douze méthodes  ✅ débloqué

**Chiffres** : rho = **0,9580**. Bootstrap sur les **paires** **[0,749 ; 1,000]** contre
[0,930 ; 0,993] publié (bootstrap sur les personnes). Fisher-z (Bonett-Wright)
**[0,848 ; 0,989]**. **13,96 %** des tirages donnent rho = 1,000. Permutation : **p <
10⁻⁴** ; percentiles de la loi nulle **[−0,573 ; +0,587]**.

**Colonnes du CSV** — volet `1e IC du Spearman a n = 12`, mesures
`rho_spearman_observe`, `rho_ic_bootstrap_sur_les_paires` (bornes en `ic_bas`/`ic_haut`,
part en `part_tirages_rho_egal_1`), `rho_ic_publie_bootstrap_sur_les_personnes`,
`rho_ic_fisher_z_bonett_wright`, `rho_permutation_p_bilateral` (percentiles de la loi
nulle en `percentile_loi_nulle_2_5` / `_50` / `_97_5`, **jamais** dans `ic_bas`).

**Formulation prête à insérer (§5.1 et §4.3) :**

> Spearman 0.958 over the 12 configurations. The interval we previously reported,
> [0.930 ; 0.993], resamples **people within each configuration** and holds the 12
> configurations fixed; it is conditional on this set of methods and does not generalise.
> Resampling the **configurations** — the unit the claim is about — gives [0.749 ; 1.000],
> with 13.9 % of draws at exactly 1.000, and a Fisher-z approximation gives
> [0.848 ; 0.989]. A permutation test rejects independence at p < 10⁻⁴.
> *(Post-hoc, not preregistered; T1a §1e.)*

**Et amender la règle du §4.3** : « All intervals are 95 % bootstrap confidence intervals
unless stated » est fausse telle qu'écrite — voir aussi R11.

---

### R12 — Le 36,4 % sans intervalle  ✅ débloqué

**Chiffres** : moyenne **36,38 %** sur **30 paires ordonnées issues de 6 configurations**.
Intervalle **en grappes par configuration : [24,7 ; 56,5]**. Bootstrap naïf sur les paires
[30,2 ; 43,3]. Étendue **11,9 % – 83,6 %**, médiane 31,1 %, écart-type **18,6 points**.

**Colonnes du CSV** — volet `1f intervalle en grappes du 36,4 %`, mesures
`intervalle_bootstrap_grappes_deux_extremites` (bornes en `ic_bas`/`ic_haut`),
`intervalle_bootstrap_naif_sur_les_paires`, `top1_min`, `top1_max`, `top1_ecart_type`,
`top1_mediane`, et l'enveloppe Monte-Carlo dans
`sensibilite_monte_carlo_grappes_deux_extremites`.

**Formulation prête à insérer (résumé et §5.4) :**

> 36.4 % top-1 at 60 common items on Twin-2K-500, 95 % CI [24.7 ; 56.5] clustered by
> configuration — the independent unit is the configuration, not the pair, as elsewhere in
> this paper: the 30 ordered pairs come from 6 configurations. Individual pairs range from
> 11.9 % to 83.6 % (SD 18.6 points), so the mean should not be read as a typical value.
> *(Interval post-hoc, not preregistered; T1a §1f.)*

---

### R15 — La baseline en monde ouvert sous A-LLR  ⚠ débloqué, MAIS renverse le sens

**Chiffres** — comparateur démographique sous **A-LLR**, même bassin et même pool que la
cible : **Park** monde fermé **85,17 %** [83,08 ; 87,26], AUC 0,739, TPR@1 % **29,09 %**,
TPR@0,1 % **17,02 %** (contre 2,24 % / 0,0000 % / 0,0000 % sous l'attaque naïve).
**Twin** monde fermé **0,78 %** [0,44 ; 1,17], AUC 0,005, TPR@1 % **0,0486 %** (une
personne), TPR@0,1 % **0,0000 %**. PMM k=10 reste à 0,0000 % partout.
Témoin de permutation sous A-LLR : **0,0951 % sur Park = exactement le hasard** — le
signal est réel, ce n'est pas un défaut de câblage.

**Colonnes du CSV** — volet `1g comparateurs en monde ouvert sous A-LLR`, conditions
`comparateur demographique` et `PMM k=10 (ajout declare)`, attaque `A-LLR (hors pli)`,
mesures `top1_monde_ferme`, `auc_monde_ouvert`, `tpr_a_fpr_1pct_tpr_escalier`,
`tpr_a_fpr_0_1pct_tpr_escalier`, `ecart_tpr_a_fpr_1pct_fort_moins_naif`, et le témoin
`temoin_permutation_lignes_top1_monde_ferme`.

**La phrase actuelle du §5.3 doit partir** : « *Statistical comparators stay
indistinguishable from noise at both FPRs* » est vraie sous l'attaque naïve seulement, et
**fausse sur Park sous A-LLR**, qui est l'attaque du chiffre de tête.

**Formulation prête à insérer — recommandée, dit la vérité entière :**

> Replayed under the same strong attack as the target, the comparators do not behave alike
> on the two archives. On Twin-2K-500 the demographic comparator stays at noise under
> A-LLR — 0.00 % TPR at 0.1 % FPR and 0.05 % (one person) at 1 % FPR, below its own naive
> value — so the 4.28 % figure stands clear of it. On the Park archive it does not: armed
> with A-LLR, a demographics-only comparator reaches 85.17 % closed-world top-1 and
> 29.09 % TPR at 1 % FPR, against 2.24 % and 0.00 % under the naive attack. A permutation
> control returns it to chance (0.095 % on a pool of 1,052), so this is genuine individual
> signal that 177 items make available to a rarity-weighted attacker, not an artefact.
> The 60.17 % we report on Park is therefore roughly twice its properly-armed demographic
> comparator, not infinitely above a silent one. A k-nearest-neighbour comparator (PMM
> k=10) stays at 0.00 % on both archives under both attacks.
> *(Post-hoc, not preregistered; T1a §1g.)*

**Décision réservée au responsable, et elle n'est pas cosmétique.** Cette formulation
coûte ~55 mots au lieu des +20 budgétés en §4 du plan, et elle réduit la portée du
chiffre de tête de Park. Trois options, par honnêteté décroissante :
**(a)** la formulation ci-dessus, entière ; **(b)** la même, en reléguant le détail Park
en Open Science (hors décompte) et en gardant dans le corps la seule phrase « on Park the
demographic comparator is not at noise once armed with the same attack (§Open Science) » ;
**(c)** restreindre la phrase du §5.3 à Twin et ne rien dire de Park — **je ne la
recommande pas** : c'est le comparateur du chiffre de tête, et le comité peut refaire ce
calcul en quelques minutes avec les scripts publiés.

---

### R13 — bonus, débloqué par §1c (le plan le rattache à §1c, pas R15)

**Chiffres** : B-oracle **0,1399 %** [0,0750 ; 0,2183] contre jumeau **0,1350 %**
[0,0450 ; 0,2691] ; différence appariée **−0,0049 pt**, IC [−0,1311 ; +0,1366].

**Colonnes du CSV** — volet `1c ex aequo et B-oracle (Argyle)`, condition
`B-oracle (11 vraies reponses, LOO k=10)`, mesure
`top1_esperance_departage_uniforme_PUBLIE` ; différence appariée dans la condition
`GPT-3 davinci (temp. principale) moins B-oracle`, mesure
`difference_appariee_points_uniforme`.

**Formulation prête à insérer (résumé, §1.1 et tableau du §5.8) :**

> a nearest neighbour holding the same eleven true answers **carries 3.6 times more
> identity bits**. In top-1 the two are level: 0.140 % [0.075 ; 0.218] for that neighbour
> against 0.135 % [0.045 ; 0.269] for the twin, a paired difference of −0.005 points
> [−0.131 ; +0.137]. Both sit at the noise level of this corpus.
> *(Top-1 of B-oracle post-hoc, not preregistered; T1a §1c.)*

---

## 8. Divergences entre le plan et ce qui a été produit

Toutes signalées, aucune corrigée en silence.

1. **§1c sert R1 et R13, pas R15.** Le tableau T1a du plan rattache §1c à « R1, R13 », et
   R15 à §1g. Le mandat qui m'a été transmis rattachait §1c à « R1 geste 4 et R15 ».
   **J'ai suivi le plan**, qui fait foi : le top-1 de B-oracle sert R13 (« 3,6× est en
   bits »), et R15 est servi par §1g seul.

2. **« Les deux conventions encadrantes » du plan, mais trois valeurs citées.** Le tableau
   T1a dit « top-1 sous les **deux** conventions encadrantes » ; R1 geste 4 cite **trois**
   valeurs (0,6052 / 0,1350 / 0,0466). La valeur du milieu n'est pas une convention
   encadrante : c'est la convention **publiée**. **Les trois sont produites**, et le CSV
   les distingue par le suffixe `_PUBLIE`.

3. **R15 affirme que le CSV donne la baseline à 0,0000 % « aux deux FPR » : vrai sur Park,
   faux sur Twin.** `c7-monde-ouvert.csv` donne le comparateur démographique de Twin à
   **0,0983 %** et **0,1981 %**, pas à zéro (ligne `Twin,Demographics Only - GPT4.1-mini`).
   Ma reproduction retombe exactement dessus (0,0972 % et 0,1944 % en escalier ; 0,0983 %
   et 0,1981 % par `np.interp`). Le constat de R15 reste juste — le comparateur n'avait
   jamais été rejoué sous A-LLR — mais **le « 0,0000 % aux deux FPR » ne vaut que pour
   Park**.

4. **R1 geste 4 cite « à 60 items la classe médiane vaut 1 » qu'aucun volet ne produit.**
   Le tableau T1a n'a pas de volet pour cette phrase. Elle est produite ici en **§1c bis**
   et signalée comme **ajout hors plan**. Sans elle, R1 geste 4 serait à moitié non sourcé
   — et ce dépôt a déjà publié un nombre non sourcé.

5. **§1g étendu à PMM k=10.** Le plan ne prescrit que la baseline démographique ; la
   phrase du §5.3 dit « comparators » au pluriel et `c7-monde-ouvert.csv` en porte deux.
   L'ajout est signalé dans le CSV par la condition `PMM k=10 (ajout declare)`.

6. **§1f : la définition de la grappe n'est pas donnée par le plan.** Une paire ordonnée
   appartient à **deux** configurations ; « bootstrap en grappes par configuration » ne
   désigne donc pas une construction unique. **Trois** définitions sont calculées et
   publiées, celle à retenir étant nommée dans le CSV. L'intervalle obtenu, [24,68 ;
   56,47], encadre celui du relecteur ([24,7 ; 55,9]) à la granularité Monte-Carlo près,
   qui est mesurée et publiée.

7. **§1e : le plan ne dit pas quelle version de Fisher-z.** La valeur du relecteur
   ([0,848 ; 0,989]) correspond à l'écart-type de Bonett-Wright `sqrt(1,06/(n−3))`, propre
   au Spearman. **Les deux versions sont publiées** ; la naïve donne [0,853 ; 0,989].
   Aucun paramètre n'a été ajusté : les deux sortent du même calcul.

8. **Écarts numériques résiduels avec le plan, tous inférieurs au bruit de graine** et
   rapportés tels quels, sans ajustement : différence appariée +0,0437 pt
   [−0,1163 ; +0,1907] contre « +0,044, IC [−0,105 ; +0,197] » ; part des tirages à
   rho = 1,000 de 13,96 % contre 13,8 % ; bootstrap naïf du 36,4 % [30,15 ; 43,30] contre
   [30,2 ; 43,2]. **Aucune graine, aucun paramètre, aucun bassin n'a été modifié pour
   réduire un écart.**

## 9. Ce que ce travail ne couvre pas

- **§1a et §1b** ne sont pas refaits ici : branche `agent/mesures/temoins-relecture`,
  commit 048a5d2, non fusionnée.
- **Aucun fichier de `article/`** n'est touché. La passe T5 applique la fiche de report.
- **R9 impose la régénération de la figure 1** (tâche T6, dépend de la décision D3) et
  la correction de `resultats/article-synthese.md` §A3/§A11 et
  `resultats/c7-attaquant-fort-resultats.md`, qui sont **hors de mon périmètre
  d'écriture** et sont signalés au responsable.
- Le statut des annexes dans le décompte des 12 pages PoPETs 2027 n'est pas vérifié.
- **La décision de rédaction sur R15 n'est pas prise ici.** La mesure l'est.
