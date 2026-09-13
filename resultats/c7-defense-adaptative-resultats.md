# Une défense qui tienne sous attaquant adaptatif — vingt-six candidats, six critères, un levier

statut: courant
mandat: Chercher une défense qui tienne contre un attaquant adaptatif à un coût d'utilité acceptable, après l'effondrement de D4 ; mesurer chaque candidat contre son attaquant adaptatif dédié, séparer ce qui est garanti de ce qui est seulement observé, et conclure — y compris « aucun remède » si c'est le cas
agent: Claude Opus 5, Anthropic — sous-agent défense adaptative
ecriture: analyses/c7_defense_adaptative.py, resultats/c7-defense-adaptative-preenregistrement.md, resultats/c7-defense-adaptative-resultats.md, resultats/c7-defense-adaptative.csv
lecture_seule: tout le reste
interdits: appel payant, réseau, recherche web, commit sur master, fusion, arrière-plan, toute modification de article/manuscrit.md (un autre agent en est propriétaire)
cecite: je n'ai pas lu article/manuscrit.md ni resultats/article-synthese.md ; je n'ai mesuré que Twin-2K-500 et la seule configuration `JSON Persona - GPT4.1`, jamais Park et al. ; je n'ai pas mis en œuvre d'adversaire à connaissance latérale ; je n'ai mesuré aucun monde ouvert et aucune composition entre publications
cout_reel_usd: 0.00

Préenregistrement : `resultats/c7-defense-adaptative-preenregistrement.md`, **écrit et commis
avant** `analyses/c7_defense_adaptative.py` et avant tout calcul de défense.
Fait foi pour tout chiffre de ce rapport : `resultats/c7-defense-adaptative.csv`.

---

## 0. La réponse, en dix lignes

**Oui, il existe un levier, et ce n'est pas une réparation de D4.** La famille des
permutations — celle dont D4 fait partie — est un cul-de-sac, et la mesure le dit de la
manière la plus nette possible : une permutation **jointe** des lignes entières coûte
**0,000 point** d'utilité et laisse la réidentification à **20,8 % [19,1 ; 22,5]**, c'est-à-dire
au niveau non protégé. Le seul candidat qui passe le critère de protection préenregistré, porte
une **borne valable contre tout attaquant**, et ne republie pas l'histogramme intra-segment,
est l'**agrégation intra-segment par le mode**, à k = 5 ou k = 10 : top-1 adaptatif
**0,52 % [0,27 ; 0,83]** et **0,22 % [0,07 ; 0,40]**, sous la garantie combinatoire
`top-1 ≤ 1/k`. Son prix est lourd et il doit être écrit avec elle : **13,2 et 19,8 points**
d'erreur sur les écarts entre segments, quand l'écart entier entre le jumeau et les humains
vaut 2,17 points sur cette même composante. La confidentialité différentielle passe le critère
de protection à **tout** epsilon — **y compris à eps = ∞**, ce qui dit que c'est l'architecture
et non le budget qui protège — mais **aucune** des trois tâches en aval ne survit sous aucun de
ses réglages, et la clause explicite du §6.4 du préenregistrement s'applique : ce passage ne
compte pas comme remède.

---

## 1. Le protocole, et ce qui le rend opposable

**Bassin constant** : 2 058 personnes couvertes par `JSON Persona - GPT4.1`, pool de 2 058
humains vague 4, monde fermé, 60 items communs (40 d'achat, 20 d'opinion), 40 segments S_gra
de taille médiane 23. Graine 20260913, dérivée par nom de condition. Aucune donnée
individuelle imprimée ni écrite.

**Contrôle d'interprétabilité passé avant toute interprétation**
(`c7_controle_interpretabilite.controle_avant_interpretation`, baseline recalculée par le
module sur le bassin exactement attaqué) : candidat **20,65 % [18,96 ; 22,34]** contre baseline
`Demographics Only - GPT4.1-mini` **2,15 % [1,59 ; 2,79]**. **PASSE.**

**Critère de protection P, préenregistré** : la borne **haute** de l'IC du top-1 sous attaquant
adaptatif doit être **strictement inférieure à 1,586 %**, borne **basse** de l'IC de cette
baseline. En clair : publier le jumeau défendu ne doit pas identifier plus que les démographies
publiques n'identifient déjà. Le seuil est lu dans le dépôt, il n'a pas été choisi.

**Chaque candidat est mesuré sous l'attaque naïve ET sous un attaquant adaptatif dédié**, et le
taux publié est le **maximum** sur les stratégies, la stratégie gagnante étant nommée au CSV.
Les cinq stratégies (N naïf, L A-LLR **recalibré sur la sortie défendue** et estimé hors pli,
S1 colonnes intactes, S3 invariants de segment, **C lien par le contenu**) sont définies au §4
du préenregistrement, **avant** toute mesure.

**La stratégie C est nouvelle ici et c'est elle qui décide de la piste 1.** Elle tient en une
phrase : *une permutation ne cache que l'indice, jamais le contenu ; l'attaquant apparie par le
contenu.* Elle a été écrite avant de mesurer, précisément parce qu'un candidat sans attaquant
dédié ne compte pas.

**Réductions déclarées d'avance** (§8 du préenregistrement, aucune choisie après coup) : un seul
tirage de permutation par réglage des familles E1/E2/E4 ; 5 réplicats d'utilité et 2 de risque
pour la DP ; un seul jeu et une seule configuration de jumeau.

---

## 2. Le tableau, protection et coût — les 26 candidats

Top-1 en pourcent, monde fermé. Les trois composantes en points, jumeau défendu contre jumeau
non protégé. **Plancher de destruction des corrélations : 4,317** — une valeur de 4,3 ou plus
sur cette colonne signifie « toute la structure détruite », jamais « coût modéré ».

| candidat | naïf | **adaptatif [IC]** | stratégie gagnante | distrib. | groupes | corrél. | A/B/C | P | garantie |
|---|---|---|---|---|---|---|---|---|---|
| **A0** non protégé | 20,717 | **22,643** [20,89 ; 24,54] | L | 0 | 0 | 0 | ●●● | non | — |
| **D4tq** (publiée, 40 items) | 0,151 | **0,243** [0,05 ; 0,49] | L | 0,00 | 0,00 | 4,40 | ●○○ | oui | aucune |
| **E1** item/item, 60 items | 0,075 | **0,078** [0,05 ; 0,11] | S3 | 0,00 | 0,00 | 4,42 | ●○○ | oui | aucune |
| **E4** λ = 0,25 | 9,427 | **9,427** [8,24 ; 10,67] | N | 0,00 | 0,00 | 2,20 | ●○● | non | aucune |
| **E4** λ = 0,50 | 2,242 | **2,242** [1,66 ; 2,85] | N | 0,00 | 0,00 | 3,34 | ●○● | non | aucune |
| **E4** λ = 0,75 | 0,517 | **0,517** [0,25 ; 0,81] | N | 0,00 | 0,00 | 4,15 | ●○● | oui | aucune |
| **E2** B = 1 (lignes entières) | 0,413 | **20,819** [19,08 ; 22,49] | **C** | 0,00 | 0,00 | **0,00** | ●●● | non | aucune |
| **E2** B = 2 | 0,326 | **33,397** [31,57 ; 35,24] | **C** | 0,00 | 0,00 | **0,00** | ●●● | non | aucune |
| **E2** B = 5 | 0,224 | **10,899** [9,82 ; 12,04] | **C** | 0,00 | 0,00 | 2,88 | ●●● | non | aucune |
| **E2** B = 10 | 0,097 | **2,388** [2,15 ; 2,64] | **C** | 0,00 | 0,00 | 3,78 | ●○○ | non | aucune |
| **E3a** k = 2 | 3,550 | **3,550** [2,83 ; 4,33] | N | 23,41 | 6,81 | 2,23 | ●○● | non | ≤ 50 % |
| **E3a** k = 5 | 0,520 | **0,520** [0,27 ; 0,83] | N | 4,38 | 13,23 | 4,03 | ●○● | **oui** | **≤ 20 %** |
| **E3a** k = 10 | 0,219 | **0,219** [0,07 ; 0,40] | N | 5,82 | 19,81 | 6,02 | ●○● | **oui** | **≤ 10 %** |
| **E3a** k = 25 | 0,126 | **0,126** [0,02 ; 0,26] | N | 18,42 | 25,33 | 10,48 | ○●○ | **oui** | **≤ 4 %** |
| **E3b** k = 2 | 10,433 | **10,433** [9,24 ; 11,72] | N | 1,02 | 6,28 | 1,73 | ○●● | non | ≤ A0/2 |
| **E3b** k = 5 | 4,043 | **4,043** [3,25 ; 4,92] | N | 1,91 | 13,11 | 3,65 | ○●● | non | ≤ A0/5 |
| **E3b** k = 10 | 2,544 | **2,544** [1,90 ; 3,20] | N | 2,35 | 20,94 | 5,47 | ○○● | non | ≤ A0/10 |
| **E3b** k = 25 | 1,217 | **1,217** [0,76 ; 1,68] | N | 5,07 | 29,97 | 9,15 | ○○○ | non | ≤ A0/25 |
| **E5** marg, eps = 1 | 0,078 | **0,078** [0,00 ; 0,34] | N | 1,82 | 2,53 | 4,50 | ○○○ | oui | **DP formelle** |
| **E5** marg, eps = 3 | 0,077 | **0,077** [0,00 ; 0,25] | N | 0,96 | 2,52 | 4,54 | ○○○ | oui | **DP formelle** |
| **E5** marg, eps = 10 | 0,052 | **0,097** [0,00 ; 0,34] | L | 0,85 | 2,43 | 4,52 | ○○○ | oui | **DP formelle** |
| **E5** marg, **eps = ∞ (témoin)** | 0,139 | **0,139** [0,00 ; 0,44] | N | 0,87 | 2,78 | 4,57 | ○○○ | oui | **aucune** |
| **E5** seg, eps = 1 | 0,070 | **0,070** [0,00 ; 0,22] | N | 5,09 | 22,73 | 6,92 | ○○○ | oui | **DP formelle** |
| **E5** seg, eps = 3 | 0,047 | **0,047** [0,00 ; 0,17] | N | 2,79 | 19,60 | 5,05 | ○○○ | oui | **DP formelle** |
| **E5** seg, eps = 10 | 0,117 | **0,117** [0,00 ; 0,34] | N | 1,26 | 12,41 | 4,50 | ○○○ | oui | **DP formelle** |
| **E5** seg, **eps = ∞ (témoin)** | 0,094 | **0,094** [0,00 ; 0,26] | N | 0,77 | 4,23 | 4,40 | ○○○ | oui | **aucune** |

A/B/C = les trois tâches en aval de `analyses/c7_utilite_aval.py`, rejouées sans une ligne
réécrite et comparées à **A0** : ● préservée, ○ perdue. Critères au §6.2 du préenregistrement.
Pour E5, une tâche n'est déclarée préservée que si elle l'est sur **les 5 réplicats** ; le
compte par réplicat est au CSV.

**Yardstick à garder sous les yeux, et sans lequel les colonnes de coût ne se lisent pas.**
L'écart entier entre le jumeau non protégé et les humains vague 4 vaut **3,118** points de
distribution, **2,173** sur les écarts entre segments, **5,775** sur les corrélations
(`registre-chiffres.csv`, lignes `dp-zcdp-ecart-humains-jumeau-*`). Une défense qui coûte
13 ou 20 points sur les écarts entre segments éloigne donc la publication du jumeau de
**six à neuf fois** ce qui sépare déjà le jumeau des humains.

---

## 3. Ce que chaque piste du mandat a donné

### 3.1 Piste 1 — réparer D4. **Un cul-de-sac, et la mesure le dit sans ambiguïté.**

**Comment j'attaquerais une permutation jointe, écrit avant de mesurer :** je ne chercherais
pas à reconstituer la permutation. Une permutation ne déplace que l'**indice** ; le **contenu**
du bloc d'une personne est republié verbatim, quelque part. J'appareillerais chaque dossier
humain au contenu publié, sans jamais me demander à quelle ligne il a atterri — ce qui est
exactement ce que fait l'attaquant de ce dépôt, qui n'a jamais utilisé l'indice.

**Résultat.** À bloc unique — permutation des **lignes entières** intra-segment — le coût
d'utilité est **0,000 point sur les trois composantes** (valeur exacte 3,3 × 10⁻¹⁵ : les
tableaux publiés sont, en tant qu'ensembles, **identiques**) et le top-1 adaptatif vaut
**20,819 % [19,08 ; 22,49]**, soit le niveau non protégé. À deux blocs, il vaut **33,397 %
[31,57 ; 35,24]**, c'est-à-dire **au-dessus** du taux non protégé sous attaque naïve (20,7 %) :
la partition en blocs corrélés isole le bloc des 40 items d'achat, et l'attaquant qui choisit
son bloc attaque le plus identifiant des deux.

**La permutation jointe corrige donc le défaut F1** — le multi-ensemble intra-segment n'est plus
republié item par item — **au prix exact de rendre la publication transparente**. Aucun réglage
de B ne passe P. **Q2 est tenue.**

**Et l'autre moitié de la piste 1 ?** Étendre D4 aux 60 items (E1) referme bien le trou F5 : le
top-1 adaptatif passe de **0,243 %** à **0,078 % [0,051 ; 0,107]**, et la stratégie gagnante
devient S3, les invariants de segment — c'est-à-dire **le défaut F1 lui-même**. E1 n'est pas un
remède, c'est D4 avec sa fuite latérale bouchée : ses « 0,00 » de distribution et de groupes
sont la republication exacte de l'histogramme intra-segment, et **la seule tâche qu'elle
préserve (T-A) est préservée par cette même construction**. Autrement dit, **l'unique utilité
que E1 conserve est exactement la quantité dont la conservation exacte est la fuite.**
**Q5 est tenue.**

### 3.2 Piste 2 — agréger. **C'est là qu'est le levier, et c'est le seul endroit.**

**Comment j'attaquerais une agrégation, écrit avant de mesurer :** les membres d'un groupe
reçoivent la **même** ligne publiée ; les groupes sont donc lisibles dans la publication. Je
retrouverais le groupe, puis je tirerais au hasard dedans. Et si la ligne publiée est celle d'un
membre réel (E3b), je n'aurais pas à tirer : ce membre-là est republié verbatim, la stratégie C
s'applique.

**E3a (mode par item, groupes formés à l'intérieur des segments).** Le mode est une fonction
**symétrique** du multi-ensemble des membres : les |g| lignes publiées d'un groupe sont
**identiques**, tout attaquant attribue donc le **même** classement d'humains aux k membres, et
un seul humain peut être premier. Donc **au plus 1 des k membres a son humain au rang 1** :
`top-1 ≤ 1/k`, **pour tout attaquant, sans hypothèse**. C'est une garantie combinatoire.
Mesuré : k = 5 → **0,520 % [0,27 ; 0,83]**, k = 10 → **0,219 % [0,07 ; 0,40]**, k = 25 →
**0,126 % [0,02 ; 0,26]**. Les trois passent P ; k = 2 (3,550 %) ne le passe pas.

**Le coût est le vrai sujet.** À k = 5 : 4,38 points de distribution et **13,23 sur les écarts
entre segments** ; à k = 10 : 5,82 et **19,81** ; à k = 25 : 18,42 et 25,33. Rapportés au
yardstick du §2, ces chiffres disent que l'agrégation **détruit les statistiques de groupe
qu'elle était censée sauver**, et cela bien qu'elle forme ses groupes **à l'intérieur** des
segments. Ce qui survit n'est pas ce qu'on attendait : la **structure de corrélation entre
items** tient remarquablement (0,0 % puis 2,5 % des charges du premier axe d'ACP inversées à
k = 5 et k = 10, contre **45 %** pour D4), et le contraste hommes-femmes d'un item garde signe
et significativité. La régression (T-B) ne survit à aucun k.

**E3b (une ligne réelle tirée par groupe) est réfutée, et pour une raison d'équité.** Aucun k ne
passe P (k = 25 : 1,217 % [0,76 ; 1,68], au-dessus du seuil 1,586 % par sa borne haute). Et la
protection y est une **moyenne, pas un plancher** : la personne republiée verbatim est
réidentifiée à **21,0 % (k = 2), 20,6 % (k = 5), 25,9 % (k = 10), 29,6 % (k = 25)**. Un
mécanisme qui divise le taux moyen par k en exposant totalement une personne sur k n'est pas une
défense, c'est une loterie.

### 3.3 Piste 3 — dégrader la fidélité individuelle. **Q3 est réfutée, mais le résultat ne se vend pas.**

La courbe, en permutant intra-segment une fraction λ des cellules sur les 60 items :
λ = 0,25 → **9,43 %** ; λ = 0,50 → **2,24 %** ; λ = 0,75 → **0,52 %** ; λ = 1 → **0,078 %**. La
protection n'arrive que dans le dernier quart : il faut détruire les trois quarts de la
correspondance individuelle pour descendre sous le seuil.

**J'avais prédit qu'aucun λ intermédiaire ne passerait P en préservant T-C. C'est faux :
λ = 0,75 passe P (0,517 % [0,25 ; 0,81]) et préserve T-A et T-C** (10 % des charges de l'axe 1
inversées, contre 45 % pour D4). **Q3 est réfutée.**

**Trois réserves, et elles comptent plus que la réfutation.** (a) Le coût sur les corrélations
vaut **4,15** pour un plancher de destruction de **4,317** : la matrice de corrélation est
détruite, et T-C survit seulement parce que le **premier axe** d'ACP est plus robuste que la
matrice — mon critère T-C, tel que préenregistré, est donc **un test plus faible** que
« corrélations préservées », et je le dis plutôt que d'en tirer avantage. (b) E4 conserve
**exactement** le multi-ensemble intra-segment, pour tout λ : le défaut F1 de D4 est intact, et
ses « 0,00 » de distribution et de groupes sont la même republication. (c) Elle n'a **aucune
garantie**.

### 3.4 Piste 4 — la confidentialité différentielle. **Elle passe la protection partout, et c'est le témoin qui l'explique.**

Mécanisme gaussien composé sous zCDP, δ = 1e-6, repris de `analyses/c7_dp_zcdp.py` sans une
ligne réécrite. Top-1 adaptatif de **0,047 % à 0,139 %** selon les réglages — soit le hasard
(1/2058 = 0,049 %). **Le témoin eps = ∞, sans aucune confidentialité, passe P exactement comme
eps = 1.** C'est l'architecture — un générateur qui tire chaque item indépendamment n'a aucune
correspondance un-à-un à fuir — et non le budget, qui produit ce taux. Cette ligne est le
contrôle que la nuit précédente avait dans ses données sans le lire ; elle est ici en tête.

**À quel eps devient-elle utilisable ? La question ne se pose pas dans ces termes sur ces
données.** Entre eps = 3 et eps = ∞, l'erreur de distribution passe de 0,96 à 0,87 point : la
contribution du budget est de l'ordre de un dixième de point, conforme aux lignes
`dp-zcdp-contribution-budget-*` du registre. Ce qui limite l'utilité n'est pas epsilon, c'est
l'architecture du générateur.

**J'avais prédit que conditionner les marginales sur le segment sauverait les écarts entre
groupes sans rien coûter au budget. La moitié « budget » est exacte — sous remplacement d'une
ligne, une personne ne contribue qu'à un segment par item, la sensibilité L2 reste √2, donc
même rho, même sigma, même epsilon. La moitié « utilité » est réfutée, et franchement :**
l'erreur sur les écarts entre segments **empire**, de 2,43-2,78 à 12,41-22,73 points, et elle
empire **même à eps = ∞** (4,23 contre 2,78). La raison est la taille d'échantillon, pas la
confidentialité : 2 058 personnes réparties sur 40 segments de taille médiane 23 donnent, par
segment et par item, un bruit d'échantillonnage qui **gonfle** la dispersion entre segments plus
qu'il ne restitue le signal. **Q4 est tenue sur sa première moitié, réfutée sur la seconde.**
Le constat publiable est : *sur ces données, la contrainte mordante d'un générateur DP
conditionné n'est pas le budget, c'est le nombre de personnes par segment.*

**Et la clause du §6.4 s'applique.** **Aucune** des trois tâches ne survit sur les 5 réplicats,
sous aucun eps, sous aucune des deux architectures. T-A survit sur 2 ou 3 réplicats sur 5 dans
l'architecture marginale — c'est un tirage à pile ou face, pas une préservation ; T-C survit sur
**0 réplicat sur 5 partout**. La DP **passe P sans être un remède**, exactement pour la raison
que le préenregistrement avait anticipée : un mécanisme qui protège parce qu'il ne publie plus
rien d'individuel n'est un remède que si une tâche nommée survit.

**Ce qui n'est pas dit, et ne le sera pas.** Aucune supériorité, dans aucun sens, d'un mécanisme
empirique sur la confidentialité différentielle. Une garantie formelle et une mesure empirique
ne se comparent pas sur le seul coût (interdiction I12 de
`resultats/marqueurs-canoniques-2026-09-13.md`). La DP est le **seul** mécanisme de ce tableau
qui tienne contre un attaquant que nous n'avons pas imaginé.

---

## 4. Garanti contre observé — la colonne à ne jamais perdre en route

| mécanisme | ce qui est **garanti** | ce qui est seulement **observé** |
|---|---|---|
| **E5 (DP)** | (eps, δ)-DP, δ = 1e-6, sous remplacement d'une ligne, avec immunité au post-traitement. **Seule garantie formelle du tableau.** | les trois composantes de coût, et le fait qu'aucune tâche ne survit |
| **E3a(k)** | `top-1 ≤ 1/k`, **contre tout attaquant, sans hypothèse** — par symétrie du mode sur le multi-ensemble des membres. Garantie **combinatoire**, qui borne la **réidentification** et **rien d'autre** : elle ne dit rien de la divulgation d'attribut au niveau du groupe. | 0,520 % / 0,219 % / 0,126 % aux trois k, et tout le coût |
| **E3b(k)** | `top-1 ≤ top-1(A0)/k`, par symétrie d'échange — une **moyenne**, jamais un plancher individuel | les taux, et l'exposition de 21 à 30 % des personnes republiées verbatim |
| **D4tq, E1, E2, E4** | **rien. Aucune garantie, d'aucune sorte.** | tout : ce sont les taux des attaques que nous avons construites, contre les mécanismes que nous avons construits. Aucun n'est une borne, et le meilleur attaquant mesuré n'est pas le meilleur attaquant possible. |

---

## 5. Les prédictions préenregistrées, et laquelle est réfutée

| # | prédiction | verdict |
|---|---|---|
| **Q1** | gagnant attendu E3a(k ≥ 10), sans préserver T-C | **tenue sur le gagnant, réfutée sur la clause jointe** : E3a(k = 10) passe P et est utilisable, mais **T-C survit** (2,5 % de charges inversées), contrairement à ce que j'attendais ; c'est T-B, la régression, qui tombe |
| **Q2** | la permutation jointe est un cul-de-sac | **tenue**, et par une marge qui ne laisse pas de place au doute (0,000 point de coût, 20,8 à 33,4 % de fuite) |
| **Q3** | aucun λ intermédiaire ne passe P avec T-C | **RÉFUTÉE** : λ = 0,75 passe P et préserve T-A et T-C. Voir les trois réserves du §3.3 |
| **Q4** | la DP passe P à tout eps ; le conditionnement au segment sauve les écarts de groupe | **tenue sur la première moitié, RÉFUTÉE sur la seconde** : le conditionnement **dégrade** les écarts de groupe, et jusqu'à eps = ∞ |
| **Q5** | E1 protège mieux que D4tq sans préserver T-C | **tenue** (0,078 % contre 0,243 %, T-C perdue) |
| **Q6** | au moins un candidat est utilisable | **tenue** — donc la clause « aucun remède » du §6.4 **ne s'applique pas**, et ce rapport ne l'écrit pas |

**Deux prédictions sur six sont réfutées, une troisième l'est à moitié.** Les trois réfutations
vont toutes dans le même sens : **la structure de corrélation entre items survit mieux que je ne
l'avais prévu, et les statistiques de groupe survivent bien moins.** C'est l'inverse de
l'intuition qui gouverne D4, dont tout l'argument de vente était de préserver exactement les
statistiques de groupe.

---

## 6. Les six candidats mécaniquement « utilisables », et la seule lecture honnête qu'on peut en faire

Le critère préenregistré (passe P **et** préserve ≥ 1 tâche) en retient six : D4tq, E1,
E4(λ = 0,75), E3a(k = 5), E3a(k = 10), E3a(k = 25). **Ce compte de six est mécaniquement exact
et substantiellement trompeur, et le préenregistrement ne l'avait pas anticipé — je le note
comme une limite de mes propres critères, pas comme une raison d'en changer après coup.**

Trois des six — **D4tq, E1, E4(λ = 0,75)** — appartiennent à la famille des permutations
intra-segment item par item. Pour toutes les trois, la seule tâche préservée par construction
(T-A, le contraste entre groupes) **l'est parce que le multi-ensemble intra-segment est republié
à l'identique**. C'est le défaut F1, inchangé. Leur « utilité préservée » est la fuite, comme
elle l'était pour D4. **Aucune des trois ne doit être recommandée** : ce sont des variantes
mieux réglées du mécanisme dont l'article vient de retirer la recommandation.

Restent **E3a(k = 5)** et **E3a(k = 10)**. Elles sont les seules à cumuler : une **borne valable
contre tout attaquant**, un passage de P, une tâche préservée qui ne l'est **pas** par
construction (T-C, la structure de corrélation entre items), et **aucune** republication de
l'histogramme intra-segment. C'est le levier, et il n'y en a pas d'autre dans ce tableau.
Son domaine d'emploi est étroit et doit être nommé : **analyses de structure entre items sur le
jeu agrégé** — et rien qui exige une statistique de groupe exacte, ni aucune régression.
E3a(k = 25) protège davantage encore (0,126 %) mais perd T-C et coûte 18,4 points de
distribution : au-delà de k = 10, le mécanisme cesse de publier quoi que ce soit d'exploitable.

---

## 7. La phrase exacte que l'article doit écrire

Pour le §8 (défenses recommandées), en remplacement d'une recommandation de la famille D4 :

> We searched for a defense that survives an adaptive attacker, preregistering twenty-six
> candidates, a dedicated adaptive attacker for each, and the threshold below which we would
> report that no remedy was found. **Shuffling is a dead end, and our own measurement is the
> clearest statement of why**: a joint within-segment shuffle of whole rows costs **0.000 points**
> on all three utility components and leaves closed-world top-1 at **20.8 % [19.1 ; 22.5]** — a
> permutation hides the index, never the content, and the attack links by content. Extending
> item-wise shuffling to all sixty items does lower the rate (0.243 % → **0.078 %
> [0.051 ; 0.107]**), but the winning strategy then becomes the within-segment invariant itself,
> and the only downstream task such a mechanism preserves is preserved *by* the exact
> republication that is the leak. **The one lever we found is aggregation**: publishing, for each
> person, the per-item mode of a group of k formed inside their demographic segment brings
> adaptive top-1 to **0.52 % [0.27 ; 0.83]** at k = 5 and **0.22 % [0.07 ; 0.40]** at k = 10,
> under a guarantee that holds against *any* attacker — the k members of a group receive an
> identical published row, so at most one of them can have their true respondent ranked first,
> hence **top-1 ≤ 1/k**. This is a combinatorial bound on re-identification only; it says nothing
> about group-level attribute disclosure, and it is not a formal privacy guarantee. **Its price
> must be stated with it**: 13.2 and 19.8 points of error on between-segment differences at k = 5
> and k = 10, against a gap between the twin and the real humans of 2.17 points on that same
> component. What survives is inter-item correlational structure (2.5 % of first-axis PCA
> loadings flipped at k = 10, against 45 % for within-segment shuffling); what does not survive
> is regression, at any k. **Differential privacy, correctly implemented, clears our protection
> criterion at every epsilon we tested — and so does the eps = ∞ control with no privacy at all,
> which is how we know the protection comes from the architecture and not from the budget. But
> under our preregistered criterion none of the three downstream tasks survives it at any
> epsilon, under either a marginal or a segment-conditioned architecture; conditioning on the
> segment costs nothing in budget (the L2 sensitivity is unchanged) yet makes between-segment
> error worse, because with 2 058 respondents across 40 segments the binding constraint is
> people per segment, not epsilon.** We claim no superiority of any empirical mechanism over
> differential privacy, in either direction: a formal guarantee and an empirical measurement do
> not compare on cost alone. And for every mechanism in this table other than differential
> privacy and aggregation, no rate we report is a bound — they are the rates of the attacks we
> built.

**La phrase qui reconnaîtrait qu'aucun remède n'a été trouvé n'a pas lieu d'être écrite :** la
prédiction Q6 est tenue et le §6.4 du préenregistrement ne s'applique pas. Elle était prête, et
c'est ce qui donne sa valeur au fait de ne pas avoir eu à s'en servir.

---

## 8. Ce que ce rapport ne dit pas

- **Aucun adversaire à connaissance latérale n'a été mis en œuvre.** La conséquence « qui connaît
  les |g| − 1 autres membres d'un segment reconstitue la cible » reste vraie par construction et
  non mesurée, pour E1, E2, E4 comme pour D4.
- **Aucun monde ouvert, aucune composition** entre publications successives, **aucune divulgation
  d'attribut** mesurée finement — sauf les deux constats structurels du §4.
- **Un seul jeu, une seule configuration de jumeau.** Rien ici ne vaut pour Park et al.
- **La garantie `top-1 ≤ 1/k` de E3a borne la réidentification, pas la vie privée.** Un groupe de
  k personnes dont on publie le mode divulgue le mode ; c'est une divulgation d'attribut au
  niveau du groupe, et elle n'est pas bornée par 1/k.
- **Les critères d'utilité T-A, T-B, T-C sont ceux que j'ai préenregistrés**, et T-C s'est révélé
  plus faible que son nom ne le suggère (§3.3). Je publie le verdict tel qu'il tombe sous ces
  critères, et la réserve avec.

**Portes du dépôt, état réel.** P1 préenregistrement, P3 interdits, P4 en-têtes, P5 renvois,
P8 cohérence CSV : **OK**. **P6 horodatage : ÉCHEC**, et il est déclaré plutôt que contourné —
`preuves/c7-defense-adaptative-preenregistrement.md.ots` n'existe pas parce que `ots stamp`
exige le réseau, interdit dans cette passe. L'horodatage doit être posé par un opérateur
disposant du réseau **avant toute fusion sur master**. Jusque-là, l'antériorité du
préenregistrement ne repose que sur l'historique git : commit **3e3f128**, qui ne contient que
le préenregistrement et précède tout commit de mesure de cette branche.
