# T2. Preenregistrement

**Ecrit le 9 septembre 2026 a 01 h 05 CEST (8 septembre 2026 a 23 h 05 UTC), depot a
`d536169dc5361c38edcd723d48816e2ddd06dc4f`, avant l'ecriture du premier script de T2 et
avant tout calcul.** Aucun resultat de T2 n'existe au moment ou ce fichier est ecrit.

Conventions de certitude : **[MESURE]** calcule sur nos donnees, **[CONFIRME]** lu dans une
source verifiee, **[PROBABLE]** interpretation etayee non demontree, **[HYPOTHESE]**
proposition a tester.

Regles de forme heritees du dossier : francais, jamais de tiret cadratin ni demi cadratin,
correction de Holm sur chaque famille de tests, intervalles de confiance par bootstrap **sur
les personnes** et jamais sur les cellules.

---

## 0. Ce que T2 fait, en une phrase

T2 pose deux questions et une seule, la seconde etant le prolongement de la premiere : **au
dela de la derive globale d'un item, existe t il un signal de GROUPE, previsible, sur la part
de personnes qui changent et sur le sens de leur deplacement** ; et **le rapport « le nul a
derive bouge deux fois trop », mesure sur le SCE par C1, se transporte t il aux panels
GSS**.

C'est la version agregee de I1, celle du programme C de `MOONSHOTS.md` : « combien bougent et
dans quel groupe ». I1 a montre que le signal individuel existe mais qu'il est fait aux trois
quarts de l'instabilite de la cellule de depart, et que la direction du changement individuel
est comptable. T2 demande ce qui reste quand on renonce a la personne et qu'on vend le
groupe : c'est ce qu'un institut ou un gouvernement achete.

---

## 1. Donnees, perimetres, et ce qui est reutilise sans modification

**Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Aucun fichier
existant, script ou resultat, n'est modifie.** Un `llama-server` tourne pour R2 et n'est pas
sollicite.

Sont importes tels quels et jamais retouches : `analyses/i1_commun.py` (noyau de 118 items,
codage, perimetres, segment, regle de direction, profils, AUC, permutation intra segment,
Holm, Benjamini-Hochberg, ecriture), `analyses/a12_retest_delai.py` (items de Stanford,
appariement des noms GSS, chargement des panels, consistance, familles thematiques),
`analyses/a2_commun.py` (`est_manquant`, `bootstrap_personnes`), `analyses/a44_commun.py` par
l'intermediaire de i1, `analyses/a30_commun.py` pour les familles de sujets et les axes.
`analyses/c1_commun.py` est importe **si et seulement si** il l'est sans effet de bord de
chargement de donnees SCE ; sinon la definition du nul a derive de C1 est reimplementee a
l'identique dans `t2_commun.py` et le fait est declare comme ecart.

**Perimetre primaire.** Les quatre paires de vagues a **quatre ans** de I1 : 2006-2010,
2008-2012, 2010-2014 et la cohorte 2016 du panel 2016-2020. Attendu **4 683 personnes** et
**118 items** du noyau commun de a12. Personnes disjointes d'un panel a l'autre, donc
bootstrap sur les personnes sans correction de grappe.

**Perimetre secondaire.** Les quatre paires a **deux ans** disjointes de I1, attendu **5 682
personnes**, memes 118 items. Il sert au volet 2 (le rapport reel sur nul par delai) et, si
le temps de calcul le permet, au volet 1.

**Manquants.** Convention de a12 et de I1 : les « ne sait pas », refus et non poses arrivent
en NaN et sont exclus. Les taux de changement publies sont des minorants, comme ceux de a12 et
de I1.

**Aucune microdonnee n'est ecrite.** Tous les fichiers `t2-*.csv` sont des agregats par item,
par groupe, par famille ou par panel.

---

## 2. Les groupes

Les groupes sont construits sur les **demographies de la vague de depart uniquement**,
jamais sur la vague d'arrivee, avec les fonctions de `i1_commun` sans retouche.

| axe | modalites | fonction |
|---|---|---|
| **camp ideologique** | gauche, centre, droite, non renseigne | `i1_commun.bloc_ideologie(polviews)` |
| **age** | 18-34, 35-54, 55+, non renseigne | `i1_commun.bloc_age(age)` |
| **education** | bas, moyen, haut, non renseigne | `i1_commun.bloc_education(degree)` |
| **genre** | homme, femme | `sex` du GSS, 1 et 2, autre valeur en non renseigne |
| **croisements** | camp x age, camp x education, camp x genre, age x education, age x genre, education x genre | produit des deux axes |

**Regle d'effectif suffisant, declaree avant tout calcul.** Un groupe entre dans l'analyse si
son effectif total sur le perimetre est d'au moins **200 personnes**. Une cellule (groupe,
item) entre si l'item est evalue chez au moins **50 personnes du groupe de chaque cote de la
coupure en demi echantillons** definie en 3.2. Les modalites « non renseigne » sont
conservees comme groupes a part entiere si elles passent le seuil, et jamais fusionnees.

**Un axe declare en second ordre, jamais en premier.** Le camp partisan (`partyid`) n'est pas
utilise dans le volet 1 ; il sert uniquement de controle d'ancrage au volet 3, comme a30
l'exige.

---

## 3. Volet 1. La version agregee de « qui bouge »

### 3.1 Les deux quantites a predire

Pour un groupe `g` et un item `j`, sur les personnes de `g` chez qui `j` est evalue aux deux
vagues :

1. **Le taux de changement** `tau(g, j)` : part de ces personnes dont la modalite differe
   entre les deux vagues. Definition de Stanford et de a12, egalite exacte.
2. **Le deplacement net du groupe**, deux versions publiees ensemble :
   - **`pi(g, j)`, deplacement projete sur la derive globale**, defini pour les 118 items.
     Soit `Delta_g` le vecteur des variations de part de chaque modalite dans le groupe et
     `Delta_0` le meme vecteur sur tout le perimetre. Alors
     `pi(g, j) = 100 x <Delta_g, Delta_0 / ||Delta_0||_2>`, en points. Son signe dit si le
     groupe bouge **avec** ou **contre** la derive globale de l'item, sa valeur absolue dit de
     combien. Elle ne suppose aucune ordinalite.
   - **`mu(g, j)`, deplacement ordinal**, defini pour les seuls items marques ordinaux par le
     `question_master` de Stanford (`groups/categorical.csv`, `Categorical = N` veut dire
     ordinal) : moyenne du code GSS en vague d'arrivee moins moyenne en vague de depart, en
     points d'echelle. Le code employe est **le code numerique brut du GSS**, jamais un
     recodage de notre invention ; la liste des items retenus et leurs bornes sont publiees.

### 3.2 Le dispositif d'evaluation : demi echantillons repetes sur les personnes

Le probleme est que la cible est elle meme estimee sur les memes personnes que le modele.
Le dispositif suivant est declare avant tout calcul.

**Cinq repetitions d'une coupure 50 / 50 des personnes**, stratifiee par panel, graine
`20260909`. Pour chaque repetition : tous les modeles sont **ajustes sur la moitie A**, et la
cible `tau(g, j)`, `pi(g, j)`, `mu(g, j)` est **observee sur la moitie B**. L'erreur est
mesuree sur B. Aucune personne n'est des deux cotes. Les cellules retenues sont celles qui
comptent au moins 50 personnes evaluees **des deux cotes**.

**La quantite de verdict est l'erreur absolue moyenne, en points, sur la cellule (groupe,
item)**, moyennee sur les cellules retenues puis sur les cinq repetitions, pour `tau` et pour
`pi`. Une quantite secondaire est la **part de variance inter groupes expliquee** : apres
retrait de la moyenne d'item (que le nul a derive reproduit par construction), le `R2` du
modele sur la cible demoyennee, calcule comme en `a43-r2-demoyenne.md`, `1 - SCE / SCT`, avec
un `R2` negatif publie tel quel.

### 3.3 Les six modeles, declares avant tout calcul

Tous voient la **moitie A seulement**, et de la moitie A la **vague de depart seulement**
plus les demographies. Aucun ne voit jamais la vague d'arrivee de la moitie B.

- **M0, le nul a derive.** Connait la derive agregee de l'item et rien des groupes :
  `tau_hat(g, j) = tau_A(j)`, `pi_hat(g, j) = pi_A(tout, j)`, `mu_hat(g, j) = mu_A(tout, j)`.
  C'est le nul contre lequel tout est compare, et c'est le transport a l'agrege du nul a
  derive de I1 section 3.5 et de C1 section 6.3.
- **M1, modele de segment.** Connait le groupe et rien de l'item : `tau_hat(g, j) = tau_A(g)`,
  taux de changement moyen du groupe sur tous ses items ; idem pour `pi` et `mu`.
- **M2, additif item plus groupe.** `tau_hat(g, j) = tau_A(j) + (tau_A(g) - tau_A(tout))`, le
  modele ou un groupe a une propension a changer constante d'un item a l'autre. Idem pour
  `pi` et `mu`.
- **M3, `P` agrege.** Le predicteur `P` de I1, position initiale seule, agrege a la cellule :
  sur la moitie A, la probabilite de changement des personnes qui donnent la modalite `m` a
  l'item `j` ; sur la moitie B, chaque personne recoit le taux de sa propre modalite de
  vague 1 et la prediction de la cellule est la moyenne dans la cellule. Il connait donc la
  vague 1 par la **composition** du groupe, sans connaitre son etiquette.
- **M4, `P` agrege plus decalage de groupe.** M3 plus un decalage de groupe estime sur les
  residus de M3 dans la moitie A. C'est le modele « qui connait la vague 1 et les
  demographies » du cahier des charges.
- **M5, oracle empirique de cellule.** `tau_hat(g, j) = tau_A(g, j)`, la valeur observee de la
  meme cellule dans l'autre moitie. **Il ne predit rien, il mesure le plafond** : c'est la
  meilleure valeur qu'un modele pourrait viser si tout le signal de groupe etait connu, bruit
  d'echantillonnage compris. Si M5 ne bat pas M0, **il n'y a pas de signal de groupe a
  vendre**, quel que soit le modele.

### 3.4 Tests et intervalles

**Intervalles de confiance : bootstrap sur les personnes de la moitie d'evaluation**, 400
tirages, `a2_commun.bootstrap_personnes` par l'intermediaire de `i1_commun`. Les predictions,
issues de la moitie A, sont tenues fixes ; ce qui est reechantillonne est l'ensemble des
personnes qui produisent la cible et l'erreur. La colonne de contraste est
`erreur(M_k) - erreur(M0)`, appariee cellule par cellule.

**Correction de Holm** sur la famille des dix contrastes : cinq modeles M1 a M5 contre M0,
pour les deux cibles `tau` et `pi`. La cible `mu` porte sa propre famille de cinq contrastes,
corrigee separement, et est declaree secondaire.

**Un test de permutation d'etiquette de groupe** : les etiquettes de groupe sont permutees
entre les personnes **a l'interieur du panel et de l'item**, 200 permutations, et la part de
variance inter groupes est recalculee. Elle donne la bande de ce qu'un decoupage sans contenu
produit.

---

## 4. Volet 2. Le nul a derive « bouge deux fois trop », transporte sur le GSS

### 4.1 Le generateur nul

Transposition exacte du temoin de C1 section 6.3 : « les valeurs de la fenetre apres sont
remelangees entre menages de la meme cohorte ; les deux distributions marginales et la derive
par cohorte sont conservees, seul l'appariement est detruit ». Sur le GSS, item par item :

- **N1, remelange dans le panel.** Pour chaque panel et chaque item, la colonne de vague
  d'arrivee est permutee entre les personnes evaluees aux deux vagues. Les deux marginales du
  panel et sa derive sont conservees exactement ; l'appariement est detruit. C'est le temoin
  `nul_remelange` de `i1_changement.py`, mais mesure ici sur **l'amplitude** et non sur la
  direction.
- **N2, remelange dans la cohorte.** Le meme, restreint au segment
  `ideologie x age x education` de `i1_commun.segment`, ce qui est le pendant exact de la
  cohorte `age x diplome x revenu` de C1. Il conserve en plus les marginales de chaque
  segment, donc il est plus severe.

**50 replicats**, graine `20260909`.

### 4.2 Les quantites d'amplitude

1. **Nombre d'items changes par personne**, rapporte au nombre d'items evalues chez elle :
   c'est le taux de changement individuel de I1 section 3.1, valeur observee attendue 0,3255 a
   quatre ans et 0,3115 a deux ans.
2. **Distance de changement sur les items ordinaux** : moyenne, sur les items ordinaux
   evalues chez la personne, de la valeur absolue de la difference des codes GSS bruts entre
   les deux vagues. C'est l'analogue direct de « l'ampleur moyenne de la revision » de C1, qui
   etait mesuree sur des variables continues.

**Le rapport publie est `reel / nul`**, moyenne sur les replicats, avec intervalle de
confiance par bootstrap sur les personnes, 400 tirages, appliques conjointement au reel et au
nul du meme tirage. Il est publie **par panel**, **par delai** (deux ans et quatre ans), **par
famille d'items** (les familles de `a12_retest_delai.FAMILLES`, reprises telles quelles) et
sous les deux generateurs N1 et N2.

### 4.3 Pourquoi cette quantite compte

Si le rapport vaut aussi environ 0,5 sur le GSS, alors la phrase « une population sans
personnes bouge deux fois trop » devient une quantite de verdict generale, mesuree sur deux
jeux de donnees, deux instruments, deux pays de collecte et deux natures de variable, continue
au SCE et categorielle au GSS, **a zero appel de modele**.

---

## 5. Volet 3. Le lien avec les camps

a30 etablit que **la gauche est le camp le moins varie des trois** sur les 149 items du GSS
transversal, rapport droite sur gauche 1,122 [1,100 ; 1,145], le centre non distinguable de la
droite. T2 demande si le camp le moins varie est aussi celui qui bouge le moins.

Trois mesures, sur les camps du **panel** et non de l'echantillon transversal de a30, ce qui
est une transposition et sera declare comme telle :

1. **Taux de changement par camp** et deplacement projete par camp, avec IC bootstrap sur les
   personnes et test de permutation d'etiquette de camp a l'interieur du panel.
2. **Ou se recrutent les changeurs** : part de chaque camp dans le decile superieur du taux de
   changement individuel, comparee a sa part dans la population ; et la meme chose pour le
   decile inferieur. Un rapport superieur a un pour le centre voudrait dire que les changeurs
   se recrutent au centre.
3. **Le rapport reel sur nul du volet 2, camp par camp** : un camp dont le rapport est plus
   bas est un camp dont les personnes sont plus appariees a elles memes.

**Controle d'ancrage** : les trois mesures sont refaites sur le camp partisan (`partyid`,
repliement standard de a30), dont la fiabilite est superieure a celle de l'ideologie declaree.
Une difference qui ne survit pas au changement d'ancrage n'est pas une difference entre camps.

---

## 6. Volet 4. La figure

`resultats/t2-figure-qui-bouge-agrege.png` et `.svg`, trois panneaux, style des figures du
dossier, sans tiret cadratin dans les libelles.

- **A.** Erreur absolue du meilleur predicteur de groupe contre celle du nul a derive, **item
  par item**, en points, avec la premiere bissectrice. Un nuage sous la bissectrice veut dire
  que le groupe apporte quelque chose.
- **B.** Rapport reel sur nul par panel et par delai, avec IC, et la ligne horizontale a 0,43
  qui est la valeur du SCE.
- **C.** Part de variance inter groupes expliquee par modele, avec la bande de permutation
  d'etiquette de groupe.

---

## 7. Six predictions, ecrites avant tout calcul

| | prediction | falsifiable par |
|---|---|---|
| **P1** | Le rapport reel sur nul du **nombre d'items changes** est compris entre **0,35 et 0,60** sur le perimetre a quatre ans, sous N1. | la valeur mesuree hors de l'intervalle |
| **P2** | Le rapport est **plus grand a quatre ans qu'a deux ans**, parce que le nul depend peu du delai alors que le reel augmente avec lui. | rapport a deux ans superieur ou egal a celui a quatre ans |
| **P3** | **M5, l'oracle empirique de cellule, bat M0** sur l'erreur absolue du taux de changement, d'au moins **0,3 point** en moyenne, apres Holm. | gain inferieur a 0,3 point ou non retenu |
| **P4** | La **part de variance inter groupes expliquee** par le meilleur modele previsionnel, M3 ou M4, est **inferieure a 0,25**. | valeur superieure ou egale a 0,25 |
| **P5** | Le camp de **gauche n'est pas** le camp qui change le moins, et l'ecart maximal entre camps sur le taux de changement est **inferieur a 2 points**. | gauche strictement le plus bas, ou ecart superieur a 2 points |
| **P6** | Sur le **deplacement net projete** `pi`, **aucun** des modeles M1 a M4 ne bat M0 de facon retenue par Holm : le sens du deplacement d'un groupe est la derive globale et rien d'autre. | un modele retenu |

---

## 8. Cinq controles bloquants, executes avant toute lecture de resultat

| | controle | attendu | consequence si echec |
|---|---|---|---|
| **C1** | Consistance du noyau commun reproduite par appel des fonctions de a12 | **0,6953** a deux ans et **0,6745** a quatre ans, a la quatrieme decimale | arret, la chaine de lecture est fausse |
| **C2** | Perimetres | **118 items**, **4 683** personnes a quatre ans, **5 682** a deux ans | arret |
| **C3** | Le nul conserve les marginales | pour chaque item et chaque replicat, ecart maximal entre la marginale de vague d'arrivee reelle et celle du nul **exactement nul** | arret, le generateur n'est pas un nul a derive |
| **C4** | Codage ordinal | la liste des items ordinaux du noyau commun est publiee avec le nombre de codes distincts, le minimum et le maximum ; tout item dont les codes ne sont pas des entiers est ecarte du volet ordinal | le volet ordinal est retire, le volet 2 tient sur le seul nombre d'items changes |
| **C5** | Coupure en demi echantillons | aucune personne des deux cotes, et chaque cellule retenue a au moins 50 personnes de chaque cote | arret |

---

## 9. Deux regles de decision

**Regle 1.** Si **M5 ne bat pas M0** apres Holm sur le taux de changement, alors **il n'existe
pas de signal de groupe au dela de la derive globale**, meme en connaissance parfaite, et la
version agregee de « qui bouge » n'a rien a vendre a un institut : T2 conclut par la negative
et le programme C de `MOONSHOTS.md` perd son etage agrege comme il a deja perdu son etage
individuel de direction. Aucun modele previsionnel n'est alors interprete.

**Regle 2.** Si M5 bat M0 mais qu'**aucun modele previsionnel M2, M3, M4 n'en recupere au
moins la moitie**, alors le signal de groupe existe et n'est pas previsible depuis la vague 1
et les demographies : c'est un resultat different et il doit etre ecrit comme tel, « il y a
quelque chose et nous ne savons pas le predire ».

**Regle 3.** Si le rapport reel sur nul du volet 2 sort de l'intervalle [0,35 ; 0,60], la
quantite de C1 **ne se transporte pas** et ne doit pas etre publiee comme quantite de verdict
generale ; elle reste un fait sur les anticipations de menages.

---

## 10. Sorties declarees

Scripts nouveaux : `analyses/t2_commun.py`, `analyses/t2_agrege.py`,
`analyses/t2_amplitude.py`, `analyses/t2_camps.py`, `analyses/t2_figure.py`.

Tableaux : `resultats/t2-controles.csv`, `t2-groupes.csv`, `t2-par-groupe-item.csv`,
`t2-modeles.csv`, `t2-contrastes.csv`, `t2-variance-inter-groupes.csv`,
`t2-erreur-par-item.csv`, `t2-amplitude.csv`, `t2-amplitude-par-famille.csv`,
`t2-amplitude-par-camp.csv`, `t2-ordinaux.csv`, `t2-camps.csv`, `t2-changeurs-deciles.csv`.

Figure : `resultats/t2-figure-qui-bouge-agrege.png` et `.svg`.

Rapport : `resultats/t2-qui-bouge-agrege.md`.

**Tout ecart a ce preenregistrement sera publie dans une section « Les ecarts au
preenregistrement » du rapport, numerote, avec sa justification.**
