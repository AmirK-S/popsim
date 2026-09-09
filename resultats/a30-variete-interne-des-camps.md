# a30. La variete interne des camps : la droite est elle plus variee que la gauche ?

## Errata du 9 septembre 2026

Correction apportee a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md` section 7.2, signalee par
`resultats/a47-errata-2.md` section 4. **Le corps du rapport n'est pas reecrit** ; l'errata
cite la phrase d'origine, donne la correction et donne la preuve. Aucun recalcul, aucun
appel de modele de langage.

### E1. Section 7.3 : l'unanimite est une quantite de gabarit, et le rapport ne le porte pas. Objection a45 numero 7.2.

**Phrase d'origine.** « **Le camp de gauche de C2 est litteralement unanime sur trois
familles de sujets.** Gini Simpson de 0,0045 sur les sept items d'avortement, et de **0,000
exactement** sur les onze items de libertes civiles et les cinq items de fin de vie [...]
**le chiffre a publier est le zero au denominateur.** »

**Correction.** Le fait et la lecon sur le denominateur restent entiers. Ce qui manque est
la classe de la quantite : l'unanimite, et plus generalement le Gini Simpson d'un camp sur
un item, est une **fonctionnelle de la seule table (camp, modalite)**. Elle est exactement
invariante sous permutation des personnes a l'interieur de leur camp, donc une **quantite de
gabarit** au sens du critere de Yuan que `resultats/a44-generateur-nul.md` applique au reste
du dossier. a44 le reconnait explicitement pour ce rapport, « elle rend le camp de gauche
litteralement unanime, Gini Simpson 0,000 (a30) : **oui par construction**, une marginale de
segment degeneree donne un nul degenere » [a44 section 9.2] ; **a30 ne porte pas ce
classement**, et c'est ce que cet errata ajoute.

**Ce que cela change a la redaction.** L'unanimite de C2, le rapport de 1,122 chez les
humains et les ecarts par famille de sujets ne se publient jamais seuls : ils se publient a
cote d'une quantite de personne, la chute d'exactitude sous permutation intra segment, et du
plancher humain. Ils autorisent une affirmation sur les **marges d'un camp**, jamais sur les
personnes simulees prises une a une : un generateur sans aucune structure individuelle les
reproduit.

**Reserve de regime de decodage.** L'unanimite de C2 est mesuree en argmax et ne l'a jamais
ete en regime de tirage, alors que les traces le permettent ; `a35-couples-regime.csv`
montre que le passage a l'echantillonnage remonte le ratio intra de 0,36 a 0,43 selon les
familles. [PROBABLE]

---

Seance du 8 septembre 2026. Aucun appel de modele de langage, lecture seule sur `data/`,
quatre coeurs, environ une minute de calcul pour l'ensemble. Aucun fichier existant n'a
ete modifie.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu
dans une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## Reponse en une ligne

**Amir a raison sur le fait et tort sur l'enonce.** [MESURE] Chez les vrais humains du
GSS, la dispersion interne du camp de droite vaut **1,122 fois** celle du camp de gauche,
intervalle [1,100 ; 1,145], et ce rapport survit a tout ce qu'on lui oppose : changement
de mesure, changement d'ancrage, egalisation des effectifs, appariement demographique
exact, et reinterrogation des memes personnes deux semaines plus tard. Mais **le centre
n'est pas distinguable de la droite** (0,989 [0,973 ; 1,005]) : l'enonce exact n'est pas
« la droite est plus variee », c'est **« la gauche est le camp le moins varie des
trois »**. Et l'ecart n'est pas general : il vaut **2,47 sur l'avortement**, 1,43 sur les
libertes civiles, 1,25 sur les roles de genre, **0,93 sur la fin de vie** et **0,97 sur
les questions economiques personnelles**. Sur Twin-2K-500 le meme rapport global tombe a
**1,020**, et il vaut **0,988 sur les 275 items de personnalite** : hors du politique et
du moral, l'asymetrie disparait ou change de signe. Enfin, les simulations **n'effacent
pas cet ecart, elles l'exagerent** : les six conditions de Stanford donnent 1,12 a 1,35
la ou les humains donnent 1,12, et l'etiquette ideologique aggrave l'exageration (C2
1,367 contre C3 1,154 sur les memes 150 personnes).

---

## 0. Ce qui a ete mesure, et sur quoi

| | GSS | Twin-2K-500 |
|---|---|---|
| personnes | 1 052 | 2 058 |
| items d'analyse | 149 categoriels, liste de a2 et a28 | 609 categoriels des vagues 1 a 3, hors 14 demographies ; 108 reposes en vague 4 |
| camps, ideologie | `political_ideology`, 7 points repliee en 3 blocs : gauche 417, centre 303, droite 332 | `QID22`, 5 points repliee en 3 blocs : gauche 909, centre 582, droite 567 |
| camps, parti | `political_party`, 7 points repliee en 3, « other party » ecarte : gauche 496, centre 164, droite 367 | `QID20` : gauche 847, centre 609, droite 540 |
| controle temporel | vague 2, memes personnes a deux semaines | vague 4, memes personnes, 108 items |
| simulations | 6 conditions de Stanford, C2, C3, 5 predicteurs statistiques | 15 fichiers, 13 configurations distinctes |

[MESURE] Le repliement en trois blocs est la regle mecanique de `a1` sur le libelle,
recopiee sans changement. Les camps partisans emploient le repliement standard de la
science politique americaine, les « independants proches de » comptes avec le parti dont
ils se disent proches.

---

## 1. Famille d'hypotheses, ecrite avant de regarder le moindre resultat

Elle figure en tete de chaque script, et elle n'a pas ete revisee apres coup.

**Volet 1, la variete brute.**
H1, un test : le rapport droite sur gauche de la dispersion interne agregee depasse 1.
H2, neuf tests sur le GSS et six sur Twin : ce rapport depasse 1 dans chaque famille de sujets.
H3, 149 tests sur le GSS et 609 sur Twin : il depasse 1 item par item.
H4, trois tests : il survit au changement d'ancrage (parti), a l'egalisation des effectifs, et a l'appariement demographique exact.
H5, un test : la vague de reinterrogation donne la meme chose.
H6, deux tests : le centre n'est pas le camp le plus varie.

**Volet 2, la structure.**
S1 : plus de patrons de reponses distincts a droite, a effectif et items identiques.
S2 : premiere composante principale expliquant une part plus faible a droite.
S3 : plus de sous groupes retenus par la silhouette a droite.
S4 : correlation entre axe economique et axe social plus faible a droite.

**Volet 3, les simulations.**
A1 : le rapport droite sur gauche des agents differe de celui des humains.
A2 : l'ecrasement est plus fort dans le camp le plus varie, c'est a dire a droite.
A3 : l'etiquette ideologique dans l'invite change ce rapport.

**Volet ajoute en cours de seance, la geometrie a la ResIN.**
R1 : chez les humains, le sous graphe republicain est plus dense que le democrate.
R2 : la forme est stable d'une vague a l'autre.
R3 : les agents ramenent ce rapport de densite vers 1.

**Correction pour tests multiples.** Holm a l'interieur de chaque famille de tests, prise
separement, plus Benjamini Hochberg en second sur les grandes familles d'items. Les
familles ne sont jamais fusionnees, et une famille a un seul test n'est pas corrigee.

---

## 2. Protocole

**Deux mesures de dispersion, les memes qu'en `a1` et `a28`.** Indice de Gini Simpson
avec l'estimateur sans biais, somme n_k (n_k moins 1) sur N (N moins 1), et entropie de
Shannon corrigee par Miller Madow. La premiere est la mesure principale : elle est sans
biais, donc la difference de taille entre camps ne la fausse pas. La seconde est le
controle, et sa correction n'etant qu'au premier ordre, elle recoit en plus un controle
de rarefaction.

**Un moteur unique.** Toutes les operations demandees reviennent a recompter les
modalites d'un item sur un sous ensemble pondere de personnes. Le module `a30_commun`
precalcule une matrice indicatrice (personnes x items x modalites) aplatie ; un jeu de B
poids donne les B tables de contingence en un produit matriciel. Le bootstrap sur les
personnes, la permutation d'etiquette de camp, la rarefaction et l'appariement
demographique sont quatre jeux de poids differents et rien d'autre.

**Intervalles.** Bootstrap sur les personnes, jamais sur les cellules : les 149 reponses
d'un individu ne sont pas independantes. Les deux camps sont reechantillonnes
independamment dans le meme tirage, 1 000 tirages, percentiles a 2,5 et 97,5 pour cent.

**Tests.** Permutation de l'etiquette de camp, effectifs conserves, statistique
bilaterale sur le logarithme du rapport, estimateur de Phipson et Smyth (b plus 1) sur
(m plus 1) qui ne rend jamais un p nul. 2 000 permutations pour les tests globaux,
20 000 pour les tests item par item, sans quoi un p corrige par Holm sur 149 ou 609 tests
ne pourrait pas descendre sous 0,05 pour une raison de resolution et non de fait.

**Familles de sujets du GSS.** Les six familles thematiques de `a2_baselines_gss` reprises
sans changement (58 items), puis les 91 items restants classes a la lecture du libelle en
trois categories et non deux : attitude sociale (41), attitude economique (15), et hors
axe (35). La troisieme categorie existe parce que forcer « avez vous un ordinateur » dans
un des deux axes fabriquerait de la variete la ou il n'y a qu'un fait personnel. Le
classement complet est dans `a30-gss-classement-items.csv`, item par item, verifiable.

**Ce qui a ete repris et non reecrit.** `a2_commun` pour la notion de cellule manquante,
`a2_baselines_gss.charger` et `FAMILLES`, `a25_commun` pour la nomenclature et la liste
des items ordinaux, `a25_mesures.matrices` et `a28_commun.charger_tout` pour les matrices
de prediction, `a28_commun.holm` et `benjamini_hochberg`, `a9_commun` pour Twin. Aucun de
ces fichiers n'a ete touche.

---

## 3. Volet 1, les humains du GSS

### 3.1 Le fait principal

`a30-gss-global.csv`, `a30-gss-par-camp.csv`.

| test | valeur droite | valeur gauche | rapport | intervalle | p |
|---|---|---|---|---|---|
| **H1, Gini Simpson** | 0,5093 | 0,4538 | **1,1225** | [1,1006 ; 1,1447] | 0,0005 |
| H1 bis, entropie | 1,2632 | 1,1388 | 1,1092 | [1,0880 ; 1,1281] | 0,0005 |
| H4a, ancrage parti | 0,5084 | 0,4646 | 1,0943 | [1,0748 ; 1,1140] | 0,0005 |
| H5, vague 2, controle | 0,5071 | 0,4559 | 1,1123 | [1,0880 ; 1,1376] | 0,0005 |
| **H6a, centre / gauche** | 0,5039 | 0,4538 | **1,1106** | [1,0863 ; 1,1304] | 0,0005 |
| **H6b, centre / droite** | 0,5039 | 0,5093 | **0,9894** | [0,9733 ; 1,0049] | 0,137 |

[MESURE] **La droite est plus variee que la gauche, de 12,2 pour cent.** Le p de
permutation est a la resolution du test, 1 sur 2 001, dans une famille d'un seul test.

[MESURE] **Mais le centre l'est autant que la droite.** Le rapport centre sur droite
vaut 0,989 et son intervalle contient 1. L'enonce correct est donc : la gauche est le
camp le moins varie des trois, et non la droite le plus varie. C'est une correction de
fond, pas de forme : « la droite est plus heterogene » suggere une propriete du
conservatisme, « la gauche est plus homogene » suggere une propriete du consensus de
gauche, et c'est la seconde que les donnees soutiennent.

### 3.2 Le gradient en sept points

`a30-gss-par-camp.csv`. Dispersion interne agregee sur les 149 items.

| niveau declare | n | Gini Simpson |
|---|---|---|
| extremely liberal | 119 | **0,4258** |
| liberal | 200 | 0,4512 |
| slightly liberal | 98 | 0,4752 |
| moderate | 303 | 0,5039 |
| slightly conservative | 94 | 0,5035 |
| conservative | 177 | 0,5000 |
| extremely conservative | 61 | **0,5107** |

[MESURE] **Le gradient est monotone sur la moitie gauche et plat sur la moitie droite.**
De « extremement liberal » a « modere », la dispersion monte de facon reguliere, plus 18
pour cent. De « modere » a « extremement conservateur », elle ne bouge plus, plus 1,4
pour cent, et l'ordre interne n'est meme pas monotone. Ce n'est donc pas une asymetrie
entre deux camps, c'est **un cone qui se referme d'un seul cote**. Le contraste extreme
contre extreme vaut 1,199 [1,135 ; 1,253], le contraste modere contre modere 1,060
[1,020 ; 1,097] : plus on va vers le pole, plus l'ecart grandit, et il grandit parce que
le pole de gauche se resserre.

### 3.3 Ou l'ecart se loge, et ou il s'inverse

`a30-gss-par-famille.csv`, p corriges par Holm dans une famille de neuf tests.

| famille | items | gauche | droite | rapport | intervalle | p Holm |
|---|---|---|---|---|---|---|
| **avortement** | 7 | 0,160 | 0,396 | **2,469** | [2,042 ; 3,059] | 0,0045 |
| **libertes civiles** | 11 | 0,275 | 0,394 | **1,432** | [1,314 ; 1,550] | 0,0045 |
| **roles de genre** | 5 | 0,535 | 0,668 | **1,249** | [1,204 ; 1,291] | 0,0045 |
| **depenses publiques** | 17 | 0,463 | 0,568 | **1,225** | [1,181 ; 1,273] | 0,0045 |
| autres, social | 41 | 0,482 | 0,526 | 1,092 | [1,063 ; 1,121] | 0,0045 |
| **autres, hors axe** | 35 | 0,422 | 0,452 | **1,073** | [1,044 ; 1,099] | 0,0045 |
| confiance dans les institutions | 13 | 0,544 | 0,571 | 1,049 | [1,018 ; 1,081] | 0,0045 |
| **autres, economique** | 15 | 0,629 | 0,613 | **0,974** | [0,955 ; 0,992] | 0,0100 |
| fin de vie | 5 | 0,378 | 0,352 | 0,932 | [0,844 ; 1,015] | 0,083 |

[MESURE] **L'ecart est un fait moral, pas un fait ideologique general.** Sur les sept
items d'avortement, la gauche est presque unanime, 0,160 de Gini Simpson, la droite est
partagee, 0,396. Sur les cinq items de fin de vie et les quinze items economiques
personnels, c'est la gauche qui est la plus variee.

[MESURE] **Le plancher non attitudinal vaut 1,073.** Sur les 35 items qui ne sont pas des
attitudes du tout, employe ou non, divorce ou non, acces a internet, chasse, la droite est
deja 7,3 pour cent plus variee. Une partie de cet ecart est de la composition sociale que
notre appariement ne retire pas, et une partie est reelle : l'item `hunt1`, la chasse,
donne a lui seul un rapport de 3,44, ce qui est un fait de mode de vie et non un artefact.
Le bon exces attitudinal est donc a lire au dessus de ce plancher : **2,30 fois le
plancher pour l'avortement, 1,33 pour les libertes civiles, et 1,05 seulement pour le
rapport global.**

[MESURE] **La vague 2 reproduit le classement famille par famille**, ecart maximal 0,14
sur l'avortement (2,469 contre 2,326), et l'ordre des neuf familles est identique.

### 3.4 Item par item, et l'asymetrie n'est pas totale

`a30-gss-par-item.csv`, 149 tests, 20 000 permutations.

[MESURE] 94 items sur 149 donnent un rapport superieur a 1, mediane 1,057. Apres Holm,
**61 items sont significativement en faveur de la droite et 21 en faveur de la gauche** ;
apres Benjamini Hochberg, 71 contre 26.

Les dix items les plus asymetriques de chaque cote :

| en faveur de la droite | rapport | | en faveur de la gauche | rapport |
|---|---|---|---|---|
| `abrape` avortement apres viol | 5,64 | | `nataid/y` aide etrangere | 0,44 |
| `sexeduc` education sexuelle a l'ecole | 4,82 | | `suicide2` suicide, faillite | 0,51 |
| `libhomo/y` livre d'un homosexuel en bibliotheque | 4,43 | | `suicide3` suicide, deshonneur | 0,56 |
| `abdefect` avortement, malformation | 3,95 | | `postlife` vie apres la mort | 0,57 |
| `spkhomo/y` conference d'un homosexuel | 3,51 | | `cappun` peine de mort | 0,63 |
| `hunt1` chasse | 3,44 | | `courts` severite des tribunaux | 0,65 |
| `colhomo` enseignant homosexuel | 3,29 | | `xmarsex` adultere | 0,66 |
| `fepol` les femmes en politique | 3,09 | | `suicide4` suicide, fatigue de vivre | 0,70 |
| `abhlth` avortement, sante | 2,99 | | `polhitok/y` coup porte par un policier | 0,73 |
| `natenvir/y` depenses environnement | 2,65 | | `union1` syndicat | 0,74 |

[MESURE] La lecture est lisible : **la droite est divisee sur ce sur quoi la gauche a un
consensus moral acquis** (avortement, droits des homosexuels, roles de genre,
environnement), et **la gauche est divisee sur ce sur quoi la droite a un consensus
d'ordre acquis** (peine de mort, severite des tribunaux, violence policiere, adultere,
suicide, vie apres la mort). Ce n'est pas une asymetrie de temperament, c'est une carte
de qui a deja tranche quoi.

### 3.5 Les quatre controles

`a30-gss-appariement.csv`.

| controle | mesure | taille | rapport | intervalle |
|---|---|---|---|---|
| rarefaction a effectif egal, 332 par camp | Gini Simpson | 332 | 1,1224 | [1,1130 ; 1,1316] |
| rarefaction a effectif egal | entropie | 332 | 1,1092 | [1,1012 ; 1,1172] |
| **appariement genre x race x age x education** | Gini Simpson | 281 | **1,1329** | [1,1243 ; 1,1409] |
| appariement genre x race x age x education | entropie | 281 | 1,1178 | [1,1104 ; 1,1255] |

[MESURE] **Aucun des deux controles ne fait tomber l'effet, et l'appariement le fait
legerement monter**, de 1,122 a 1,133. La difference de variete n'est donc pas une
difference de composition sur ces quatre attributs : c'est l'inverse, la composition
demographique masquait un peu l'ecart.

[MESURE] Le changement d'ancrage coute 2,5 points : 1,122 avec l'ideologie declaree,
1,094 avec le parti. [PROBABLE] Une partie de cette baisse est l'effet attendu de la
fiabilite : `polviews` a une fiabilite de 0,66 et `partyid` de 0,84 ([CONFIRME],
corpus/05, 05-06). Une variable de segmentation plus fiable classe mieux les gens, donc
elle devrait au contraire **augmenter** l'ecart mesure si l'ecart etait reel et attenue
par l'erreur de classement. Le fait qu'elle le diminue veut dire que **l'ideologie
declaree et l'identification partisane ne decoupent pas la meme chose**, et que l'ecart
tient un peu plus a l'etiquette symbolique qu'a l'appartenance partisane. C'est
exactement ce que 05-03 predit ([CONFIRME], corpus/05 : les auteurs attribuent le
debordement de quadrant a la desirabilite differentielle des deux etiquettes).

---

## 4. Volet 1 bis, les humains de Twin-2K-500

`a30-twin-global.csv`, `a30-twin-par-bloc.csv`, `a30-twin-appariement.csv`.

| test | rapport | intervalle | p |
|---|---|---|---|
| H1, 609 items, Gini Simpson | **1,0204** | [1,0092 ; 1,0304] | 0,0005 |
| H1 bis, entropie | 1,0205 | [1,0089 ; 1,0302] | 0,0010 |
| H4a, ancrage parti | 1,0229 | [1,0104 ; 1,0332] | 0,0010 |
| H6a, centre / gauche | 1,0235 | [1,0124 ; 1,0333] | 0,0005 |
| H6b, centre / droite | 1,0031 | [0,9915 ; 1,0149] | 0,599 |
| cinq points, tres conservateur / tres liberal | 1,0467 | [1,0219 ; 1,0620] | 0,0005 |
| cinq points, conservateur / liberal | 1,0093 | [0,9963 ; 1,0221] | 0,134 |
| H5a, vagues 1 a 3, 108 items reposes | 1,0643 | [1,0529 ; 1,0751] | 0,0005 |
| **H5b, vague 4, memes 108 items, controle** | **1,0681** | [1,0571 ; 1,0772] | 0,0005 |

Par bloc du catalogue :

| bloc | items | gauche | droite | rapport | intervalle | p Holm |
|---|---|---|---|---|---|---|
| **attitudes politiques** | 10 | 0,579 | 0,747 | **1,290** | [1,262 ; 1,319] | 0,003 |
| cognitif | 50 | 0,415 | 0,465 | 1,120 | [1,077 ; 1,163] | 0,003 |
| economique | 176 | 0,331 | 0,347 | 1,048 | [1,013 ; 1,081] | 0,010 |
| heuristiques et biais | 58 | 0,566 | 0,593 | 1,047 | [1,028 ; 1,062] | 0,003 |
| prix | 40 | 0,484 | 0,497 | 1,026 | [1,016 ; 1,035] | 0,003 |
| **personnalite** | 275 | 0,690 | 0,681 | **0,988** | [0,978 ; 0,997] | 0,010 |

[MESURE] **Sur Twin le rapport global tombe a 1,020 et il change de signe sur la
personnalite.** La raison est arithmetique : 275 des 609 items sont des items de
personnalite, ou l'asymetrie est nulle ou inverse, et 10 seulement sont des attitudes
politiques, ou elle vaut 1,290. Le chiffre global de Twin n'est pas comparable a celui du
GSS, dont les 149 items sont majoritairement attitudinaux. **Comparer les deux jeux sur
leur chiffre global serait une faute ; il faut les comparer bloc a bloc.**

[MESURE] Bloc a bloc, la coherence des deux jeux est bonne : 1,290 sur les attitudes
politiques de Twin contre 1,225 sur les depenses publiques et 1,092 sur les autres
attitudes sociales du GSS. Le contenu de `QID287`, dix politiques publiques concretes,
est du meme registre que la batterie `nat*`.

[MESURE] Les controles passent : rarefaction 1,021, appariement demographique 1,029, la
vague 4 reproduit la vague 1 a 0,4 point pres (1,068 contre 1,064). Item par item, 609
tests : 46 significatifs a droite et 41 a gauche apres Holm, 116 contre 101 apres
Benjamini Hochberg. **Sur Twin l'asymetrie item par item est presque equilibree.**

---

## 5. Volet 2, la structure interne des camps

`a30-structure-resume.csv`, `a30-structure-axes.csv`, `a30-structure-dimensions.csv`.
Tout est calcule a effectif egal, 303 personnes par camp sur le GSS, 100 tirages ou 200
jeux d'items selon la mesure, correction de Holm dans une famille de cinq tests.

| test | gauche | centre | droite | ecart droite moins gauche | intervalle | p Holm |
|---|---|---|---|---|---|---|
| **S1, patrons distincts sur dix items, GSS** | 238,9 | 266,8 | **269,0** | **+30,1** | [26,5 ; 34,0] | 0,005 |
| S1 bis, patrons distincts, Twin, 567 par camp | 507,9 | 514,9 | 512,7 | +4,8 | [2,4 ; 7,3] | 0,005 |
| **S2, part de variance de la premiere composante** | 0,1135 | 0,0874 | **0,1014** | **-0,0121** | [-0,0130 ; -0,0111] | 0,005 |
| S3, nombre de sous groupes retenu | 2,0 | 2,0 | 2,0 | 0,0 | [0 ; 0] | 1,00 |
| **S4, correlation economique x social** | **0,447** | **0,134** | **0,311** | **-0,136** | [-0,263 ; -0,003] | 0,005 |

[MESURE] **S1 confirme.** Sur dix items tires au hasard et 303 personnes par camp, le
camp de droite produit 269 combinaisons de reponses distinctes, la gauche 239, soit
**12,6 pour cent de patrons en plus**, exactement l'ordre de grandeur du rapport de
dispersion. Le centre est a 267, encore une fois indistinguable de la droite. Sur Twin
l'ecart existe mais vaut moins de 1 pour cent.

[MESURE] **S2 confirme, faiblement.** La premiere composante principale des 71 items
ordinaux explique 11,35 pour cent de la variance a gauche et 10,14 pour cent a droite. Il
faut 13,4 composantes a gauche et 13,3 a droite pour atteindre la moitie de la variance :
**l'ecart de dimensionnalite est reel sur la premiere composante et nul des qu'on cumule.**
Il ne faut pas ecrire « la droite a plus de dimensions ».

[MESURE] **S3 est refute, et proprement.** Le nombre de sous groupes retenu par la
silhouette vaut 2 dans les trois camps, dans 100 tirages sur 100. Et la silhouette est
plus **haute** a gauche, 0,078, qu'a droite, 0,059, ou au centre, 0,049. La gauche est
donc legerement plus separable en deux blocs que la droite. Les valeurs restent tres
basses en absolu, ce qui redit ce que `a1` section 5 avait deja mesure : sur ces donnees,
il n'y a pas d'amas.

[MESURE] **S4 confirme, et c'est le resultat le plus interessant du volet 2.** La
correlation entre le score economique et le score social vaut **0,447 a gauche** et
**0,311 a droite**, ecart -0,136, intervalle [-0,263 ; -0,003], p de permutation 0,002.
C'est exactement le sens predit par la these libertaires contre autoritaires, et c'est
exactement ce que 05-03 mesure ([CONFIRME], corpus/05 : « les liberaux declares ont une
relation plus forte entre leurs dimensions economique et sociale que les conservateurs
declares »). Sur la population entiere la correlation vaut 0,533, plus haute que le 0,30
de la litterature, ce qui est attendu puisque notre axe economique se reduit a la
batterie de depenses publiques et a l'impot.

**Le controle qui rend ce chiffre lisible.** Restreindre a un camp restreint l'etendue
des scores et abaisse mecaniquement la correlation. Ici la restriction joue **contre** le
resultat : l'ecart type du score economique vaut 1,59 a gauche et **2,16 a droite**,
celui du score social 1,81 a gauche et **2,66 a droite**. La droite a plus d'etendue sur
les deux axes et malgre cela une correlation plus faible. La difference n'est donc pas un
artefact de restriction d'etendue.

[MESURE] Le centre est un cas a part : correlation 0,134 [0,014 ; 0,252], soit une quasi
independance des deux axes. Les moderes ne sont pas des gens qui se placent au milieu des
deux axes, ce sont des gens dont les deux axes ne communiquent pas.

---

## 6. Volet ajoute, la geometrie du reseau d'attitudes a la ResIN

Demande en cours de seance, a partir de `resultats/a32-papier-diversite-droite.md`.
Methode recopiee de la section 2 de ce rapport : noeud egale modalite de reponse, arete
egale phi entre indicatrices, paires du meme item exclues, phi negatifs ramenes a zero.
Support : `QID287` de Twin, dix items sur la meme echelle a cinq points, 50 noeuds, camps
partisans `QID20`, 540 republicains contre 847 democrates. Ni disposition a ressorts ni
ACP de rotation : elles ne servent dans les papiers d'origine qu'a produire l'image dont
l'asymetrie est constatee a l'oeil, et n'entrent dans aucune quantite mesuree.

`a30-resin-twin-noeuds.csv`, `a30-resin-twin-densites.csv`.

### 6.1 Le partage des noeuds chiffre ce que le papier constate a l'oeil

[MESURE] **33 des 50 modalites sont plus endossees par les republicains, 17 par les
democrates**, taux d'endossement rapporte a l'effectif de chaque camp. **Huit des dix
modalites « ni l'un ni l'autre » tombent du cote republicain.**

[CONFIRME] Luders, Carpentras et Quayle ecrivent, sans le chiffrer, que l'amas democrate
« contenait presque exclusivement des attitudes extremes » et l'amas republicain « une
gamme plus large allant du desaccord modere a l'accord maximal », et Chen et ses
coauteurs notent que les positions neutres sont absorbees du cote republicain.

[MESURE] **Ces deux observations visuelles sont reproduites et chiffrees ici pour la
premiere fois sur ce jeu : 33 contre 17, et 8 modalites neutres sur 10 du cote
republicain.** C'est, a ma connaissance de ce dossier, la seule mesure numerique existante
de l'affirmation d'origine, et elle va dans le sens d'Amir.

### 6.2 La densite des sous graphes va dans l'autre sens

Densites moyennes sur 200 tirages a effectifs egaux, 540 personnes par camp.

| condition | partage des noeuds | densite droite | densite gauche | rapport droite / gauche | intervalle |
|---|---|---|---|---|---|
| **humains vagues 1 a 3** | brut, 33 contre 17 | 0,079 | 0,147 | **0,540** | [0,531 ; 0,549] |
| humains vagues 1 a 3 | **egalise, 17 contre 17** | 0,131 | 0,147 | **0,894** | [0,874 ; 0,914] |
| humains vagues 1 a 3 | sans les neutres | 0,105 | 0,181 | 0,580 | [0,567 ; 0,593] |
| **humains vague 4, controle** | egalise | 0,139 | 0,149 | **0,935** | [0,912 ; 0,955] |
| gpt41mini defaut | egalise | 0,227 | 0,281 | **0,808** | [0,800 ; 0,815] |
| **gpt41mini demo seules** | egalise | 0,061 | 0,244 | **0,251** | [0,248 ; 0,255] |
| gpt41mini json | egalise | 0,253 | 0,367 | 0,691 | [0,686 ; 0,697] |
| gpt41mini finetune500 | egalise | 0,186 | 0,289 | 0,644 | [0,621 ; 0,673] |

[MESURE] **R1 est refute sur ce jeu.** Le sous graphe republicain est **moins** dense que
le democrate, quel que soit le partage : 0,540 en brut, 0,894 a nombre de noeuds egal,
0,580 sans les modalites neutres. Les trois intervalles excluent 1. Chen et ses coauteurs
trouvent l'inverse sur l'ANES de 2000 a 2020, sauf en 2020 ([CONFIRME] par le rapport
a32). Notre mesure est sur 2024, une seule matrice de dix items et un echantillon
Prolific : elle ne contredit pas leur serie, elle ajoute un point qui ressemble a leur
2020.

[MESURE] **La moitie du 0,540 brut est un artefact de taille de sous graphe.** Passer de
33 contre 17 noeuds a 17 contre 17 fait remonter le rapport de 0,540 a 0,894. Le piege
signale dans `a32` est reel et il est massif : **toute densite de sous graphe partisan
publiee sans nombre de noeuds egalise est ininterpretable.**

[MESURE] **R2 est confirme.** La vague 4, memes personnes, donne 0,935 contre 0,894 en
vagues 1 a 3, soit un plancher de bruit d'environ 0,04 sur ce rapport. Toute difference
inferieure a 0,04 ne doit pas etre commentee.

[MESURE] **R3 est refute, et de facon spectaculaire.** La prediction etait que les agents
ramenent le rapport vers 1. Aucune configuration ne le fait : la meilleure, gpt41mini
defaut, donne 0,808 contre 0,894 chez les humains, soit **plus loin de 1**, et la
configuration nourrie des seules demographies donne **0,251**, sept fois le plancher de
bruit en dessous de la valeur humaine. Elle y arrive en n'employant jamais **12 des 50
modalites**.

[MESURE] Un second fait, secondaire mais net : **les agents produisent des reseaux
d'attitudes beaucoup plus denses que les humains dans les deux camps**, 0,281 contre
0,147 a gauche pour gpt41mini defaut. C'est la contrepartie geometrique de l'exces de
coherence deja mesure en `a9` (alpha de 0,872 chez les humains a 0,967 chez les agents
sur la batterie d'attitudes politiques).

### 6.3 Les deux mesures ne disent pas la meme chose, et c'est le point

[MESURE] Sur les memes dix items de `QID287`, la dispersion interne donne un rapport
droite sur gauche de **1,290** (la droite est plus variee) et la densite de reseau un
rapport de **0,894** (la droite est moins liee). Il n'y a pas de contradiction :
**la droite repond de facon plus dispersee et moins coherente, la gauche de facon plus
concentree et plus systematique.** [PROBABLE] C'est la meme chose vue deux fois, une
gauche qui a un systeme de croyances serre et une droite qui a un ensemble de positions
plus lache.

---

## 7. Volet 3, les simulations

`a30-agents-gss.csv`, `a30-agents-gss-150.csv`, `a30-agents-twin.csv`,
`a30-agents-contrastes.csv`, `a30-agents-gss-familles.csv`.

### 7.1 La simulation exagere l'ecart, elle ne l'efface pas

GSS, 1 052 personnes, 149 items, memes camps et meme estimateur qu'en section 3.

| condition | rapport droite / gauche | intervalle | ecrasement gauche | ecrasement droite |
|---|---|---|---|---|
| **humains vague 1** | **1,1225** | [1,1001 ; 1,1463] | 1,000 | 1,000 |
| humains vague 2, plancher de bruit | 1,1123 | [1,0865 ; 1,1373] | 1,005 | 0,996 |
| agents composite | 1,1973 | [1,1615 ; 1,2361] | 0,815 | 0,870 |
| agents entretien (v3) | 1,2633 | [1,2081 ; 1,3119] | 0,713 | 0,803 |
| **agents enquete** | **1,3471** | [1,2985 ; 1,3896] | 0,725 | 0,870 |
| agents demographiques (v6), sans etiquette | 1,1685 | [1,1273 ; 1,2104] | 0,646 | 0,673 |
| agents persona (v7) | 1,1209 | [1,0576 ; 1,1858] | 0,658 | 0,657 |
| agents demographiques (v8), avec etiquette | 1,2568 | [1,1820 ; 1,3272] | 0,492 | 0,551 |
| B1 regression logistique | 1,1599 | [1,1229 ; 1,1968] | 0,653 | 0,675 |
| B2 plus proches voisins | 1,3551 | [1,2983 ; 1,4166] | 0,491 | 0,593 |
| B3 foret aleatoire | 1,1733 | [1,1316 ; 1,2147] | 0,418 | 0,437 |
| B0 tirage dans la marginale | 1,0007 | [0,9930 ; 1,0080] | 1,118 | 0,997 |
| B0 mode | 1,0799 | [0,9954 ; 1,1719] | 0,041 | 0,040 |

[MESURE] **A1 est confirme et A2 est refute.** Onze conditions sur douze donnent un
rapport superieur ou egal a celui des humains ; cinq ont un intervalle qui ne contient
pas la valeur humaine de 1,1225. Et l'ecrasement est **systematiquement plus faible a
droite qu'a gauche** dans dix cas sur douze : la simulation rabote plus fort le camp qui
avait deja le moins de variete.

[MESURE] Le seul point d'egalite est `agents persona (v7)`, 1,121 [1,058 ; 1,186], et
c'est aussi la condition qui n'a recu aucune information individuelle : elle reproduit le
rapport humain parce qu'elle ne reproduit rien d'autre.

[MESURE] Le temoin `B0 tirage` tombe exactement ou il doit tomber, 1,0007 : un predicteur
qui tire dans la marginale de la population entiere donne la meme distribution dans les
deux camps, donc un rapport de 1. Cela valide la mesure : elle detecte bien l'absence de
structure de camp quand il n'y en a pas.

### 7.2 Le mecanisme n'est pas le meme selon la condition

Perte absolue de dispersion par rapport aux humains, en points de Gini Simpson :

| condition | perte a gauche | perte a droite | difference |
|---|---|---|---|
| agents enquete | 0,1247 | 0,0661 | **+0,059** |
| agents entretien (v3) | 0,1301 | 0,1005 | +0,030 |
| agents composite | 0,0838 | 0,0663 | +0,017 |
| agents v8 | 0,2304 | 0,2286 | +0,002 |
| agents demographiques (v6) | 0,1606 | 0,1667 | -0,006 |
| B1 regression logistique | 0,1573 | 0,1654 | -0,008 |
| B3 foret aleatoire | 0,2643 | 0,2870 | -0,023 |

[MESURE] **Deux mecanismes distincts, et il ne faut pas les confondre.** Pour les trois
conditions riches en information sur la personne (enquete, entretien, composite), la
gauche perd davantage **en valeur absolue** : l'agent detruit specifiquement la variete de
gauche. Pour les conditions demographiques et pour les predicteurs statistiques, la perte
absolue est egale ou plus forte a droite, et l'amplification du rapport n'est qu'un effet
de plancher, une reduction a peu pres proportionnelle qui frappe plus durement le camp
qui partait de plus bas.

[PROBABLE] La phrase defendable est donc : **un agent qui recoit de l'information
individuelle sur la personne detruit selectivement la variete du camp de gauche ; un
predicteur qui ne recoit qu'une etiquette ecrase les deux camps a peu pres egalement et
amplifie le rapport par arithmetique.**

### 7.3 Par famille de sujets, l'exageration devient caricature

Rapports droite sur gauche, GSS, `a30-agents-gss-familles.csv`, colonne `perimetre`
egale « 1052 personnes ». C2 et C3 n'existent pas sur ce perimetre, ils sont dans le
tableau suivant.

| famille | humains v1 | humains v2 | composite | entretien | enquete | v6 sans etiquette | **v8 avec etiquette** |
|---|---|---|---|---|---|---|---|
| **avortement** | 2,47 | 2,33 | 3,10 | 7,51 | 3,95 | 2,10 | **25,9** |
| libertes civiles | 1,43 | 1,40 | 1,82 | 4,39 | 2,11 | 1,86 | **9,00** |
| roles de genre | 1,25 | 1,24 | 1,32 | 1,76 | 1,77 | 1,19 | 1,87 |
| depenses publiques | 1,23 | 1,22 | 1,55 | 1,45 | 2,14 | 1,16 | 1,99 |
| autres, social | 1,09 | 1,08 | 1,19 | 1,25 | 1,32 | 1,20 | 1,27 |
| autres, hors axe | 1,07 | 1,05 | 0,99 | 1,03 | 1,06 | 1,09 | 0,80 |
| confiance institutions | 1,05 | 1,06 | 0,98 | 0,93 | 1,08 | 1,02 | 0,78 |
| autres, economique | 0,97 | 0,96 | 0,97 | 0,99 | 1,03 | 1,02 | 1,10 |
| fin de vie | 0,93 | 0,97 | 1,23 | 1,52 | 1,03 | 1,02 | 0,93 |

Sur les memes 150 personnes, seul perimetre ou C2 et C3 existent, 63 a gauche et 42 a
droite. Le tableau donne la dispersion du camp de gauche a cote du rapport, parce que
c'est elle qui porte tout :

| famille | humains, gauche | **C2**, gauche | **C3**, gauche | humains, rapport | **C2**, rapport | **C3**, rapport | v8, rapport |
|---|---|---|---|---|---|---|---|
| **avortement** | 0,182 | **0,0045** | 0,288 | 2,22 | **75,2** | **1,27** | 14,0 |
| **libertes civiles** | 0,246 | **0,000** | 0,144 | 1,58 | infini | 2,18 | 10,6 |
| **fin de vie** | 0,396 | **0,000** | 0,186 | 0,80 | infini | 1,52 | 0,89 |
| roles de genre | 0,572 | 0,166 | 0,439 | 1,17 | 3,77 | 0,98 | 1,64 |
| autres, social | 0,490 | 0,142 | 0,335 | 1,07 | 1,94 | 1,11 | 1,28 |
| depenses publiques | 0,490 | 0,417 | 0,173 | 1,16 | 1,00 | 1,91 | 1,81 |
| autres, hors axe | 0,417 | 0,276 | 0,252 | 1,07 | 0,92 | 1,11 | 0,87 |
| autres, economique | 0,637 | 0,425 | 0,522 | 0,94 | 0,99 | 0,93 | 1,22 |

[MESURE] **Le camp de gauche de C2 est litteralement unanime sur trois familles de
sujets.** Gini Simpson de 0,0045 sur les sept items d'avortement, et de **0,000 exactement**
sur les onze items de libertes civiles et les cinq items de fin de vie : les 63 agents a
qui l'on a dit qu'ils etaient de gauche donnent tous la meme reponse, sur 23 questions.
Les memes 63 humains donnent 0,182, 0,246 et 0,396. Les rapports de 75,2 et d'infini ne
sont pas des chiffres a publier tels quels, c'est le numerateur qui les rend absurdes ;
**le chiffre a publier est le zero au denominateur.**

[MESURE] La meme chose en plus faible chez `v8`, la condition demographique de Stanford
qui porte l'etiquette : 0,018 de dispersion a gauche sur l'avortement contre 0,182 chez
les humains, rapport 14,0. Et pas chez `v6`, la condition demographique sans etiquette,
rapport 2,10 sur les 1 052 contre 2,47 chez les humains.

[MESURE] C3, notre condition sans etiquette, ne fait pas cela : 0,288 de dispersion a
gauche sur l'avortement contre 0,182 chez les humains, rapport 1,27 contre 2,22. **Sans
etiquette, l'agent ne durcit pas le camp de gauche, il le disperse trop.**

[MESURE] Sur les familles non attitudinales, les agents ne caricaturent pas : hors axe
0,80 a 1,11 contre 1,07 chez les humains, economique 0,93 a 1,10 contre 0,97. **La
caricature est specifique aux sujets moraux et politiques**, ce qui est coherent avec le
resultat central du dossier, la deformation loge sur l'axe ideologique et nulle part
ailleurs.

### 7.4 L'etiquette, mesure sur les memes 150 personnes

`a30-agents-contrastes.csv`. Les deux conditions d'un couple sont recalculees sur
exactement le meme tirage bootstrap de personnes, ce qui apparie le contraste.

| jeu | avec etiquette | sans etiquette | rapport avec | rapport sans | ecart | intervalle |
|---|---|---|---|---|---|---|
| **GSS, 150 personnes** | **C2** | **C3** | 1,367 | 1,154 | **+0,210** | [0,018 ; 0,384] |
| GSS, 150 personnes | agents v8 | agents v6 | 1,306 | 1,201 | +0,110 | [-0,116 ; 0,352] |
| GSS, 150 personnes | temoin, composite | enquete | 1,157 | 1,294 | -0,135 | [-0,202 ; -0,066] |
| Twin, vague 4 | gpt41mini defaut | demo seules | 1,142 | 1,115 | +0,026 | [-0,005 ; 0,060] |

[MESURE] **Un seul contraste d'etiquette est concluant, le notre.** C2 contre C3, meme
modele, memes 150 personnes, memes 149 questions, seule l'etiquette ideologique change :
le rapport droite sur gauche passe de 1,154 a 1,367, ecart +0,210, intervalle qui exclut
0 de justesse. Le couple v8 contre v6 va dans le meme sens mais son intervalle contient 0.
Le couple Twin est a la limite.

[PROBABLE] **L'etiquette ideologique dans l'invite aggrave la caricature de la variete
interne**, comme elle aggrave deja le gonflement des ecarts entre groupes (facteur 25,
`a19-errata`) et l'appariement des reponses rares (0,19 avec etiquette contre 0,41 sans,
`a28`). Trois mesures independantes pointent dans la meme direction, aucune n'est
decisive seule.

[MESURE] Le troisieme couple est un temoin et **ne doit pas etre lu comme un effet
d'etiquette** : composite et enquete different par la richesse d'information, pas par la
presence de l'ideologie. Il est negatif, ce qui montre que la richesse d'information et
l'etiquette n'agissent pas dans le meme sens.

### 7.5 Twin, treize configurations

| condition | rapport global | ecrasement gauche | ecrasement droite | rapport sur les 10 attitudes |
|---|---|---|---|---|
| **humains vague 4** | **1,068** | 1,000 | 1,000 | **1,294** |
| gpt41mini defaut | 1,142 | 0,537 | 0,574 | **1,885** |
| gpt41mini demo seules | 1,116 | 0,523 | 0,546 | **3,514** |
| gpt41mini texte, temperature par defaut | 1,121 | 0,603 | 0,633 | 2,023 |
| gpt41mini json | 1,069 | 0,639 | 0,639 | 1,848 |
| gpt41mini resume | 1,144 | 0,590 | 0,632 | **3,650** |
| gpt41mini finetune500 | 1,287 | 0,566 | 0,682 | 1,948 |
| gpt41 json | 1,052 | 0,656 | 0,646 | 1,155 |
| gpt41 json predout | 0,998 | 0,625 | 0,584 | 0,930 |
| gemini flash 2.5 texte | 1,136 | 0,692 | 0,735 | **3,166** |

[MESURE] **Douze configurations sur treize placent le rapport au dessus de la valeur
humaine sur les dix items d'attitudes politiques**, de 1,155 a 3,650 contre 1,294 chez les
humains. La configuration `demo_only`, celle qui ne recoit que les demographies, monte a
3,514 ; `resume` a 3,650 ; `gemini flash` a 3,166. Les deux seules configurations qui
n'exagerent pas sont les deux qui emploient le gros modele GPT-4.1 en sortie structuree
(1,155 et 0,930).

[MESURE] L'ecrasement est la aussi plus faible a droite qu'a gauche dans onze cas sur
treize.

---

## 8. Figure

`resultats/a30-figure-variete-des-camps.png` et `.svg`. Trois panneaux, tous construits a
partir des tableaux et jamais recalcules dans le script de figure.

A. Dispersion interne par camp et par famille de sujets sur le GSS, cercle plein pour les
vrais humains et cercle vide pour les agents composite, bleu pour la gauche et rouge pour
la droite. La longueur du trait est la perte de variete due a la simulation.
B. Rapport droite sur gauche par condition sur le GSS, sur les memes 150 personnes de
bout en bout, avec les intervalles de bootstrap sur les personnes et la valeur humaine en
trait tirete.
C. Le meme rapport sur Twin, treize configurations et la reference humaine de la vague 4.

---

## 9. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise.**

1. « Sur les 149 items du GSS, la dispersion interne du camp de droite vaut 1,122 fois
   celle du camp de gauche, intervalle [1,100 ; 1,145], et le rapport reste a 1,133 apres
   appariement exact sur genre, race, age et education. »
2. « Ce n'est pas la droite qui est plus variee, c'est la gauche qui est moins variee :
   le centre est indistinguable de la droite, rapport 0,989 [0,973 ; 1,005]. »
3. « L'ecart vaut 2,47 sur les sept items d'avortement, 1,43 sur les libertes civiles,
   1,25 sur les roles de genre, et il s'inverse a 0,97 sur les questions economiques
   personnelles et 0,93 sur la fin de vie. »
4. « La dispersion croit de facon monotone de l'extreme gauche au centre, plus 18 pour
   cent, et ne bouge plus du centre a l'extreme droite, plus 1,4 pour cent. »
5. « A l'interieur de chaque camp, la correlation entre l'axe economique et l'axe social
   vaut 0,447 a gauche et 0,311 a droite, ecart -0,136 [-0,263 ; -0,003], alors meme que
   la droite a plus d'etendue sur les deux axes. »
6. « Les populations simulees n'effacent pas cet ecart, elles l'exagerent : de 1,12 chez
   les humains a 1,35 pour les meilleurs agents de Stanford, jusqu'a 25,9 et 75,2 sur la
   seule batterie d'avortement pour les deux conditions qui portent l'etiquette
   ideologique. »
7. « Sur dix items d'attitudes politiques de Twin, 33 des 50 modalites de reponse sont
   plus endossees par les republicains et 17 par les democrates, dont huit des dix
   modalites neutres du cote republicain. »

**Interdit.**

1. Interdit d'ecrire « la droite est plus heterogene que la gauche » sans nommer le
   domaine. Sur les 275 items de personnalite de Twin, le rapport vaut 0,988 et
   l'intervalle exclut 1 du mauvais cote.
2. Interdit de citer le chiffre global de Twin, 1,020, a cote de celui du GSS, 1,122 : les
   deux jeux n'ont pas la meme composition d'items et la comparaison doit etre bloc a bloc.
3. Interdit d'ecrire « la droite a plus de dimensions ». La premiere composante explique
   1,2 point de variance de moins a droite, mais il faut le meme nombre de composantes des
   qu'on cumule, 13,3 contre 13,4.
4. Interdit d'ecrire « la droite se divise en plus de sous groupes ». Le nombre retenu
   vaut 2 dans les trois camps, 100 tirages sur 100, et la silhouette est plus haute a
   gauche.
5. Interdit d'attribuer l'ecart a la composition demographique : l'appariement exact
   l'augmente au lieu de le reduire.
6. Interdit d'attribuer a l'ecart un exces attitudinal complet : le plancher non
   attitudinal vaut deja 1,073, et l'exces propre au politique doit etre lu au dessus de
   ce plancher.
7. Interdit d'ecrire que l'etiquette ideologique cause l'exageration : un seul des trois
   contrastes d'etiquette a un intervalle qui exclut 0, et de justesse.
8. Interdit de reprendre une densite de sous graphe partisan sans nombre de noeuds
   egalise : le rapport passe de 0,540 a 0,894 par ce seul controle.
9. Interdit de conclure quoi que ce soit d'une difference de rapport de densite
   inferieure a 0,04 : c'est le plancher de bruit mesure entre deux vagues des memes
   personnes.

---

## 10. Ce que cela change a ARBITRAGE.md

`ARBITRAGE.md` porte, dans la liste de ce qui est tombe le 8 septembre : « la droite est
plus heterogene que la gauche (non etabli dans la litterature) ». **Cette ligne doit etre
reecrite, pas supprimee.**

Ce qui est vrai dans la ligne actuelle : la litterature ne l'etablit pas, et
`corpus/05` le documente proprement, deux blocs de resultats s'opposent et le troisieme
dit que la question est mal posee. Cela reste [CONFIRME].

Ce qui est faux dans la ligne actuelle : elle laisse croire que l'idee est morte. **Elle
n'est pas morte, elle est desormais mesuree chez nous, et dans le sens d'Amir.** Ce que
la litterature ne fait pas et que nous faisons ici, c'est mesurer la dispersion sur les
reponses individuelles au lieu de comparer des scores agreges, exactement le reproche
qu'Amir adressait au domaine.

**Reformulation proposee de la ligne, a valider par Amir :**

> « la droite est plus heterogene que la gauche » : non etabli dans la litterature, qui
> mesure sur des scores agreges ; mesure chez nous sur les reponses individuelles, ou la
> gauche est le camp le moins varie des trois, rapport droite sur gauche 1,122
> [1,100 ; 1,145] sur le GSS, 2,47 sur l'avortement, 0,97 sur l'economique personnel, et
> 0,99 sur la personnalite (a30).

**Ce que le volet 3 apporte a l'option A.** L'option A du 8 septembre est « ce que la
simulation efface », version minorites. Le present rapport ajoute un cas ou **la
simulation n'efface pas, elle exagere**, et il l'ajoute sur l'axe qui porte deja tout le
dossier. La formule de l'option A doit donc etre nuancee d'une phrase : la simulation
efface les gens rares **et** durcit les camps. Ce sont deux faces du meme geste,
substituer un type a un individu.

**Ce que le volet 3 apporte a la question ouverte du 7 septembre.** `FAITS-ETABLIS`
section 7 demande un second axe de segmentation non attitudinal qui gonfle, faute de quoi
le dossier predit des attitudes a partir d'une attitude. Ce rapport ne le fournit pas,
mais il montre que **l'axe ideologique n'est pas seulement celui ou le gonflement entre
groupes est le plus fort, c'est aussi celui ou l'ecrasement interne est le plus
asymetrique**. Les deux deformations sont portees par le meme axe, ce qui renforce le
soupcon que le mecanisme est unique et qu'il s'appelle etiquette.

**Ce que cela ne change pas.** Aucun chiffre de `FAITS-ETABLIS` n'est contredit. Les
rapports intra de `a1` etaient calcules toutes segmentations confondues ; ceux d'ici sont
calcules camp par camp, ce sont des quantites differentes qui ne se recouvrent pas.

---

## 11. Ce que je n'ai pas pu verifier

1. **La fiabilite de la variable de segmentation n'est pas corrigee.** `polviews` a une
   fiabilite de 0,66 ([CONFIRME], 05-06). Une erreur de classement melange les camps et
   attenue tout ecart reel, donc **1,122 est probablement un plancher**. Mais l'attenuation
   n'est pas symetrique si les taux d'erreur different d'un camp a l'autre, ce que je n'ai
   pas les moyens d'estimer sans une troisieme mesure de l'ideologie. Le seul controle
   possible ici, le changement d'ancrage vers le parti, fait **baisser** le rapport, ce qui
   est le contraire de ce que l'attenuation seule predirait.
2. **L'axe economique du GSS est ampute.** `eqwlth`, `helppoor`, `helpsick`, `helpblk` et
   `helpnot` ne figurent pas dans le sous ensemble de 149 items de Stanford. L'axe
   economique se reduit donc a la batterie de depenses publiques et a l'impot, ce qui
   explique probablement pourquoi la correlation sur population entiere vaut 0,533 et non
   les 0,30 de 05-03. Le chiffre S4 est un ecart entre camps, il souffre moins de cette
   amputation que le niveau.
3. **La part « composition » n'est pas isolee proprement.** L'appariement porte sur genre,
   race, age et education. Le revenu, la region, la religion et le type de quartier n'y
   sont pas, faute de donnees completes (180 valeurs vides sur 1 052 pour trois d'entre
   elles, exclusion deja actee en `a1`). Le plancher de 1,073 sur les items hors axe n'est
   pas un controle propre non plus : il contient `hunt1`, la chasse, qui est un fait de
   mode de vie fortement lie au camp.
4. **Le volet 2 n'a ete porte qu'a moitie sur Twin.** Les patrons distincts oui, l'ACP, le
   partitionnement et la correlation des deux axes non : le catalogue des auteurs ne
   declare pas l'ordre des modalites hors des matrices de personnalite, et transposer un
   codage ordinal la ou il n'est pas declare reviendrait a inventer une echelle.
5. **La comparaison C2 contre C3 repose sur 150 personnes**, dont 63 a gauche, 45 au
   centre et 42 a droite. L'intervalle de l'ecart, [0,018 ; 0,384], est large et exclut 0
   de justesse. Il faut le second echantillon de 150 personnes de `a21` pour trancher, et
   il n'est pas charge dans le paquet employe ici.
6. **Les modalites non employees par les agents ne sont pas traitees separement.** La
   configuration `demo_only` de Twin n'emploie que 38 des 50 modalites de `QID287` ; une
   partie de son rapport de densite de 0,251 vient de cette absence et non d'une geometrie
   differente. Le nombre de modalites employees est rapporte a cote de chaque densite,
   mais je n'ai pas separe les deux contributions.
7. **La disposition a ressorts et l'ACP de rotation de ResIN ne sont pas reproduites.**
   Elles ne portent aucune quantite dans les papiers d'origine, mais leur absence interdit
   de comparer une figure a la leur.
8. **Aucun test de sensibilite a l'ordre des modalites proposees n'a ete fait** sur les
   sorties d'agents, limite deja ouverte dans `FAITS-ETABLIS` section 4 et qui vaut ici.
9. **Le rapport droite sur gauche n'a pas ete decompose entre effet de position et effet
   de dispersion.** Un camp dont la position moyenne est proche d'un bord d'echelle a
   mecaniquement moins de dispersion possible. Sur l'avortement, la gauche est a 0,160 de
   Gini Simpson, ce qui est proche du plancher : une partie de l'ecart de 2,47 est un effet
   de plafond de consensus et non une propriete du camp. Je n'ai pas construit le temoin
   qui separerait les deux.

---

## 12. Questions ouvertes pour Simon

1. **L'enonce « la gauche est le camp le moins varie » est il defendable en science
   politique, ou faut il le formuler comme un fait de consensus acquis ?** Nos donnees ne
   distinguent pas « la gauche a moins de variete » de « la gauche a deja tranche ces
   questions la ». Y a t il une mesure standard qui separe les deux ?
2. **Le gradient monotone a gauche et plat a droite, sur les sept points de `polviews`,
   correspond il a quelque chose de connu ?** Un cone qui se referme d'un seul cote n'est
   ni une asymetrie de camp ni un effet d'extremite symetrique. Si personne ne l'a decrit,
   c'est peut etre l'objet le plus original du rapport.
3. **Le centre a une correlation economique x social de 0,134, presque nulle.** Est ce le
   « bruit » des 6,5 pour cent de repondants inattentifs de 05-05, ou les 20,7 pour cent de
   positions genuines mal resumees par un axe ? Le distinguer demande un modele de melange
   que nous n'avons pas.
4. **La densite de sous graphe republicaine plus faible que la democrate sur Twin 2024
   contredit la serie ANES de Chen et ses coauteurs sauf pour 2020.** Est ce un effet
   d'annee, un effet de mode de recrutement (Prolific contre ANES), ou un effet du contenu
   des dix items, qui sont tous des politiques publiques progressistes formulees a
   l'endroit sauf deux ?
5. **Comment nommer le fait qu'un agent nourri de l'etiquette ideologique produise un camp
   de gauche unanime sur l'avortement, rapport 75,2 contre 2,47 chez les humains ?** Ce
   n'est ni un stereotype de contenu (la position moyenne est a peu pres juste) ni un
   ecrasement uniforme (l'autre camp garde sa variete). Il manque un mot pour « caricature
   de la dispersion », et c'est le meme manque que la question du trait de deviance
   laissee ouverte en `a9`.

---

## 13. Reproduction

```
.venv/bin/python analyses/a30_humains_gss.py --perm-item 20000
.venv/bin/python analyses/a30_humains_twin.py --perm-item 20000
.venv/bin/python analyses/a30_structure.py --tirages 100 --jeux 200 --boot 1000
.venv/bin/python analyses/a30_agents.py --boot 1000 --perm 2000
.venv/bin/python analyses/a30_resin_twin.py --tirages 200
.venv/bin/python analyses/a30_figure.py
```

Graine unique 20260908 dans `a30_commun.GRAINE`. Duree totale mesuree, quatre coeurs :
environ 45 secondes, dont 12 pour Twin et 10 pour le partitionnement. `a30_agents.py`
emploie les caches `/tmp/a25-matrices.pkl` et `/tmp/a28-foret.npy` produits par `a25` et
`a28` ; s'ils sont absents il les recalcule, ce qui ajoute quelques minutes de foret
aleatoire.

**Fichiers produits.** Scripts : `analyses/a30_commun.py`, `a30_humains_gss.py`,
`a30_humains_twin.py`, `a30_structure.py`, `a30_agents.py`, `a30_resin_twin.py`,
`a30_figure.py`. Tableaux : `a30-gss-classement-items.csv`, `a30-gss-par-item.csv`,
`a30-gss-par-famille.csv`, `a30-gss-par-camp.csv`, `a30-gss-global.csv`,
`a30-gss-appariement.csv`, `a30-twin-par-item.csv`, `a30-twin-par-bloc.csv`,
`a30-twin-par-camp.csv`, `a30-twin-global.csv`, `a30-twin-appariement.csv`,
`a30-structure-patrons.csv`, `a30-structure-patrons-twin.csv`,
`a30-structure-dimensions.csv`, `a30-structure-clusters.csv`, `a30-structure-axes.csv`,
`a30-structure-resume.csv`, `a30-agents-gss.csv`, `a30-agents-gss-150.csv`,
`a30-agents-gss-familles.csv`, `a30-agents-twin.csv`, `a30-agents-contrastes.csv`,
`a30-resin-twin-noeuds.csv`, `a30-resin-twin-densites.csv`. Figure :
`a30-figure-variete-des-camps.png` et `.svg`.
