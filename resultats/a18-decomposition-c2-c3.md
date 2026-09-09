# a18. Decomposition inter et intra des traces a5 : C2 contre C3, argmax contre distribution

Rapport du 7 septembre 2026, ecrit dans la nuit pendant que le run a5 tourne. Le script est
ecrit, controle et rejouable ; les chiffres ci dessous sont ceux d'une **trace partielle**
et ne sont pas des resultats.

Script : `analyses/a18_decomposition_traces.py`. Aucun appel de modele de langage, aucun
script existant modifie, traces lues en lecture seule, quatre coeurs.

---

## Reponse en une ligne

**Sur les 55 personnes que la trace C2 couvre entierement au moment de l'ecriture, soit
8 116 cellules sur les 22 350 attendues et zero cellule de C3, le deficit de dispersion
totale du modele n'est pas dans le decodage : lire la distribution complete au lieu de
durcir par argmax fait passer le ratio de dispersion totale de 0,659 a 0,673 seulement,
soit 1,4 point sur les 34 qui manquent, et il faudrait une temperature de 5,71, qui
multiplierait par huit l'entropie individuelle moyenne, pour combler le reste**
[MESURE, trace partielle]. Le contraste prioritaire de a15, C2 contre C3, **ne peut pas
etre tranche ce soir** : la trace C3 n'existe pas encore.

---

## 1. Ce qui a ete lu, et l'etat exact de la trace

| | |
|---|---|
| Trace lue | `data/traces/a5-C2-p1.jsonl`, en lecture seule [MESURE] |
| Trace absente | `data/traces/a5-C3-p1.jsonl`, le run n'a pas encore atteint C3 [MESURE] |
| Appels lus | 8 259 sur les 22 350 de C2, soit 37 pour cent [MESURE] |
| Personnes completes | 55 sur 150, couverture d'au moins 98 pour cent des 149 items [MESURE] |
| Population commune | 55 personnes, 149 items, 8 195 cellules |
| Cellules exploitables | 8 116, soit 99,04 pour cent ; le reste est une reponse humaine manquante [MESURE] |

Le run ecrit personne par personne, ce qui garantit qu'une troncature coute des personnes
entieres et jamais des items (a5 section 1). C'est ce qui rend l'analyse partielle
legitime : les 55 personnes mesurees ont bien leurs 149 items.

**Consequence a garder en tete pour tout le rapport.** Les chiffres bougent d'un
lancement a l'autre parce que la trace grandit pendant l'analyse. Entre deux executions
espacees de vingt minutes, le ratio inter de C2 sur l'axe ideologie est passe de 6,36 a
6,63 [MESURE]. Aucun chiffre de ce rapport n'est un resultat. Le rapport dit ce que le
script mesure et comment, et donne la commande a rejouer au matin.

---

## 2. Protocole

### 2.1 Ce qui est reutilise, sans une ligne modifiee

| module | ce qui en vient |
|---|---|
| `a1_double_distorsion` | `lire_nomenclature`, `lire_demographies`, `AXES`, `normaliser`, `construire_index`, `compter`, `decomposer`, `agreger` : les estimateurs a biais corrige et les six axes de segmentation |
| `a2_commun` | `exactitude_par_personne`, `bootstrap_personnes`, `profil_diversite` |
| `a2_baselines_gss` | `charger`, `CONDITIONS_LLM`, `PREP` : les 149 items, les deux vagues, les six conditions de Stanford |
| `a5_agents_locaux_gss` | `TRACES`, `nomenclature` |
| `a5_evaluer` | `lire_traces`, `moyenner_passes`, `en_matrices`, `mesures_distributionnelles` |

Les axes sont ceux de a1 : genre, race, ideologie politique, age, education, profil croise
des trois premiers. Les items sont les 149 de a2, liste d'exclusion de Stanford plus
`polviews`. La reference est **les humains de la vague 1 restreints a ces personnes et a
ces items**, jamais les 1 052.

### 2.2 La version distributionnelle : formule employee

Chaque cellule de C2 et de C3 porte une distribution complete `p_ij` sur les K modalites
de l'item. La version ponctuelle la durcit par argmax et retombe sur le format humain. La
version distributionnelle remplace le comptage d'effectifs par un **comptage de masse** :

```
c[g, k] = somme sur les personnes i du segment g de p_ij(k)        (fractionnaire)
n_g = somme_k c[g, k] = effectif du segment      (chaque personne pese exactement 1)
n_k = somme_g c[g, k]                            N = nombre de personnes
```

La distribution de population de l'item est le **melange** des distributions
individuelles, `P(k) = n_k / N`, et celle du segment g est le melange restreint,
`P_g(k) = c[g, k] / n_g`. Les deux termes sont alors ceux de a1 calcules sur ces melanges :

```
M1  intra = H(R|S) = somme_g w_g H(P_g)      inter = I(R;S) = H(P) - H(R|S)
M2  intra = somme_g w_g D(P_g)               inter = D(P) - intra
```

L'information mutuelle avec le segment se calcule donc bien sur les distributions
moyennes par segment, comme demande.

**Les estimateurs sont ceux de a1, avec deux points a documenter.**

1. Gini Simpson sans biais, `somme_k c_k (c_k - 1) / (N (N - 1))`, s'ecrit tel quel sur
   des effectifs fractionnaires et redonne a1 a l'identique sur des effectifs entiers.
2. Miller Madow, `H + (m - 1) / (2 N ln 2)`. Le `m` de a1 compte les cases d'effectif
   strictement positif. Sur des effectifs fractionnaires cette regle compte **toutes** les
   cases, y compris celles qui portent 1e-7 personne, et la correction devient enorme :
   elle corrigerait un bruit d'echantillonnage qui n'existe pas, la masse d'une case ne
   venant pas d'un tirage mais d'une somme de probabilites. La regle retenue est **case
   occupee = case portant au moins une personne equivalente**, `c >= 1`. Sur des effectifs
   entiers toute case occupee porte au moins 1, donc cette regle redonne a1 a l'identique.

**L'ampleur de ce choix est mesuree et publiee**, `a18-sensibilite-occupation.csv` :

| condition | mesure | inter, seuil 1 | inter, seuil 0 | intra, seuil 1 | intra, seuil 0 |
|---|---|---|---|---|---|
| C2 distribution | entropie | 145,99 | 16,98 | 590,94 | 731,28 |
| C2 distribution | Gini Simpson | 35,25 | 35,25 | 262,47 | 262,47 |

[MESURE] **Gini Simpson est totalement insensible au choix, l'entropie ne l'est pas.**
Consequence de methode : pour la version distributionnelle, **M2 est la mesure principale
et M1 porte un degre de liberte qu'il faut declarer**. Les deux donnent le meme signe et
le meme classement sur la trace partielle, ce qui est le controle attendu.

### 2.3 Le controle de degenerescence, execute a chaque lancement

Les humains n'ont pas de distribution. Leur version distributionnelle est degeneree, une
masse de Dirac sur la reponse donnee. Le script verifie que la voie distributionnelle,
alimentee par ces Dirac, redonne la voie ponctuelle de a1, pour les deux mesures et les
six axes, et **s'arrete si l'ecart depasse 1e-9**.

```
ecart maximal entre les deux voies sur les conditions ponctuelles : 0.000e+00
CONTROLE PASSE. La voie distributionnelle est une generalisation exacte.
```

[MESURE, `a18-controle-degenerescence.csv`, quatre conditions ponctuelles, deux mesures,
deux termes] Ecart nul au bit pres, pas approximativement nul. La version
distributionnelle est donc une generalisation exacte de la version ponctuelle et non une
mesure parallele.

Un second controle a ete ajoute apres avoir trouve une erreur reelle dans la premiere
version du script : l'argmax du tenseur de distributions est confronte a l'argmax
enregistre dans la trace, cellule par cellule, et le script s'arrete au premier desaccord.
La premiere version lisait la distribution la ou elle croyait lire l'argmax dans le
bootstrap, les permutations et la mesure de Chen. Les intervalles de confiance de cette
version etaient faux.

### 2.4 Correction residuelle et bootstrap

Comme dans a1 : 50 permutations des etiquettes de segment, le terme inter obtenu sous
permutation est soustrait ; puis 1 000 tirages bootstrap **sur les personnes**, le meme
tirage applique a toutes les conditions, chaque distribution bootstrap **recentree de
facon additive sur son estimation ponctuelle** avant de former le ratio.

**Une statistique a ete ajoutee, et elle etait necessaire.** Avec 55 personnes, le
denominateur du ratio inter est petit et son tirage bootstrap approche zero : l'intervalle
du ratio explose et devient illisible, `[-15,5 ; 30,1]` pour C2. Le script publie donc
aussi **P(sup)**, la part des tirages ou le terme inter de la condition depasse celui des
humains. Elle repond a la seule question qui compte pour la these et reste definie quand
le ratio ne l'est pas.

---

## 3. Tableau 1 : les deux ratios, deux versions, deux mesures

Entropie, 55 personnes, 8 116 cellules, trace partielle.

| condition | ratio inter | P(sup) | ratio intra | produit | ratio total |
|---|---|---|---|---|---|
| humains vague 1 | 1,000 | reference | 1,000 | 1,000 | 1,000 |
| humains vague 2 (controle) | 1,167 [-0,11 ; 2,59] | 0,89 | **0,986** [0,971 ; 1,001] | 1,151 | 0,990 |
| **C2 argmax** | **3,823** | 1,00 | **0,580** [0,522 ; 0,634] | 2,219 | 0,659 |
| **C2 distribution** | **3,575** | 1,00 | **0,593** [0,530 ; 0,649] | 2,120 | 0,665 |
| agents v8 | 5,028 | 1,00 | 0,709 [0,655 ; 0,757] | 3,566 | 0,814 |
| agents composite | 1,858 | 1,00 | 0,856 [0,836 ; 0,877] | 1,590 | 0,880 |
| agents entretien (v3) | 2,144 | 1,00 | 0,827 [0,798 ; 0,854] | 1,773 | 0,859 |
| agents enquete | 1,797 | 0,99 | 0,808 [0,783 ; 0,835] | 1,453 | 0,832 |
| agents demographiques (v6) | 0,632 | 0,17 | 0,626 [0,591 ; 0,656] | 0,396 | 0,626 |
| agents v7 | 0,166 | 0,06 | 0,618 [0,560 ; 0,677] | 0,103 | 0,607 |

[MESURE, trace partielle] Gini Simpson donne le meme classement et le meme signe pour les
dix lignes, detail dans `a18-decomposition.csv`.

**Le controle intra passe, le controle inter ne passe pas.** Les humains de la vague 2
tombent a 0,986 sur le terme intra, intervalle contenant 1. Sur le terme inter ils sont a
1,167 avec un intervalle qui deborde des deux cotes. **Avec 55 personnes, le terme inter
n'est pas estimable avec la precision de a1**, qui en avait 1 052. C'est une limite de
taille d'echantillon, pas de methode, et elle vaudra encore, attenuee, a 150 personnes.

**Le contraste 2 de a15, argmax contre distribution, est deja lisible.** Sur cette trace,
la version distributionnelle de C2 gonfle **un peu moins** l'inter, 3,575 contre 3,823, et
ecrase **un peu moins** l'intra, 0,593 contre 0,580. Les deux ecarts sont de l'ordre de
6 pour cent et de 2 pour cent. Chen predit que le signe ne change pas et que le mode
distributionnel gonfle **au moins autant**, +0,104 contre +0,081 pour Sonnet. Sur ce
modele le signe ne change pas, mais le mode distributionnel gonfle **legerement moins**.
a5 avait annonce d'avance pourquoi : a temperature 0 et avec 80 pour cent des cellules a
p max superieure a 0,99, la distribution est presque un Dirac et les deux versions ne
peuvent pas differer beaucoup [PROBABLE].

---

## 4. Tableau 2 : le contraste 1 de a15, ratio inter par axe

Mesure entropie. La premiere ligne est **le denominateur**, en bits sur les 149 items :
un ratio dont le denominateur vaut trois dixiemes de bit n'est pas interpretable.

| condition | genre | race | ideologie | age | education | profil croise |
|---|---|---|---|---|---|---|
| *denominateur, inter humain, bits* | *0,30* | *-1,04* | *8,85* | *7,31* | *1,74* | *10,30* |
| humains vague 2 (controle) | 2,11 | 0,21 | **0,99** | **0,95** | 2,74 | **1,10** |
| **C2 argmax** | -1,95 | -1,13 | **6,63** | 0,82 | 4,66 | 3,16 |
| **C2 distribution** | -1,79 | -0,74 | **6,23** | 0,85 | 4,64 | 2,88 |
| agents v8 | -1,78 | -1,84 | **7,78** | 1,74 | 3,72 | 4,68 |
| agents composite | 1,84 | 0,37 | 2,15 | 0,97 | 2,40 | 1,96 |
| agents entretien (v3) | 1,99 | -0,03 | 2,77 | 1,02 | 1,65 | 2,16 |
| agents enquete | 0,84 | 0,12 | 2,24 | 0,80 | 0,83 | 2,06 |
| agents demographiques (v6) | 1,76 | -1,34 | **0,15** | 0,74 | 3,40 | 0,33 |
| agents v7 | -0,16 | 0,33 | 0,22 | 0,14 | 0,14 | 0,19 |

[MESURE, trace partielle]

**Le controle passe sur ideologie, age et profil croise. Il ne passe pas sur genre, race
et education.** Les memes personnes reinterrogees deux semaines plus tard donnent 0,99,
0,95 et 1,10 sur les trois premiers axes, et 2,11, 0,21 et 2,74 sur les trois autres. La
raison est dans la ligne du denominateur : chez les humains, le genre n'explique que 0,30
bit de la dispersion sur 149 items, et le terme inter de la race est **negatif apres
correction**, c'est a dire indiscernable de zero. Diviser par ces quantites ne produit pas
un ratio, cela produit du bruit.

**Le script refuse donc de trancher a15 sur le genre et l'age tant que le controle ne
passe pas**, et il le dit dans sa sortie. C'est le comportement voulu.

### Les trois issues de a15, et laquelle est observee

a15 section 8 ecrit trois issues. Le script les applique mecaniquement.

- **Issue A, l'axe de segmentation commande.** C2 gonfle l'ideologie et reste au voisinage
  de 1 sur genre et age, C3 fait de meme en moins fort.
- **Issue B, l'etiquette de groupe commande.** C2 gonfle uniformement, C3 sur aucun axe.
- **Issue C, le modele reconstruit l'ideologie.** C2 et C3 gonflent l'ideologie a un
  niveau comparable.

**Aucune n'est observee, parce que C3 n'existe pas encore.** Ce qui est observe sur C2
seule est compatible avec A et avec B, et ne separe pas les deux. La sortie du script le
dit dans ces termes et refuse de conclure.

Ce qui est deja acquis sur C2 seule, et c'est reel : **son gonflement est porte par
l'ideologie**, 6,63 contre 0,82 sur l'age, sur deux axes dont le controle passe [MESURE,
trace partielle]. La reserve de a15 doit etre portee avec le chiffre : pour C2, l'axe
`political_ideology` **est dans l'invite**. Mesurer un gonflement sur un axe fourni au
modele n'est pas la meme chose que le mesurer sur un axe qu'il doit inferer. C'est le meme
dispositif que Chen et que Bisbee, donc comparable a eux, mais ce n'est pas la meme
question que C3.

### Le bon vis a vis de C2 dans l'archive : v8 et non v6

Fait etabli par `a17-relecture-adverse.md` objection 3, a partir des taux de recopie
mesures dans le paquet OSF : **gss_v6 est un agent demographique sans ideologie ni parti
dans l'invite**, il recopie marital, religion, diplome et revenu a plus de 99 pour cent
mais n'obtient que 0,20 sur `polviews` ; **gss_v8 est un agent demographique avec ideologie
et parti**, il recopie `polviews` a 0,96 et `partyid` a 0,99 [CONFIRME].

Notre C2 porte les onze attributs de `demographic_summary.csv`, `political_ideology` et
`political_party` compris. **Son homologue est v8. Comparer C2 a v6 n'est pas une
comparaison a armes egales**, et le tableau recapitulatif place desormais les deux lignes
cote a cote avec une colonne qui dit si l'etiquette ideologique est dans l'invite.

| condition | ideologie dans l'invite | ratio inter ideologie |
|---|---|---|
| **C2** | oui | **6,63** |
| **gss_v8** | oui | **7,78** |
| gss_v6 | non | **0,15** |

[MESURE, trace partielle] **C2 tombe du cote de v8, a un facteur 44 de v6.** Notre
pipeline reproduit donc, sur un autre modele, une autre invite et une autre implementation,
le fait que a17 a etabli sur l'archive : ce qui separe v6 de v8 n'est pas une generation
de modele, c'est **la presence de l'etiquette ideologique dans l'invite**, et l'effet est
de premier ordre. C'est le resultat le plus solide de la soiree, parce qu'il ne depend pas
d'un intervalle de confiance : l'ecart est de deux ordres de grandeur.

---

## 5. Tableau 3 : la mesure a la Chen

arXiv 2607.26348. Par item et par axe, `ecart = max_g p_g - min_g p_g` ou `p_g` est la part
du segment g dans le haut de l'echelle, puis mediane du rapport agent sur humain. Puis
`delta eta carre`, part de variance imputable au groupe, agent moins humain. Items ordinaux
seulement, 70 sur 149.

**Deux choix de mise en oeuvre, tous deux imposes par la taille d'echantillon et tous deux
mesures avant d'etre retenus.**

1. **Seuil d'effectif de segment, 8 personnes.** Chen mesure sur 14 704 repondants. Un
   segment de deux personnes donne une proportion qui vaut 0, 0,5 ou 1 ; `max - min` sature
   alors a 1 chez les humains comme chez le modele et le rapport vaut mecaniquement 1.
   L'artefact a ete constate avant d'etre corrige : mediane de rapport egale a 1,0000 sur
   cinq axes a la fois [MESURE].
2. **Un axe supplementaire, l'ideologie en trois blocs.** Avec sept niveaux et 150
   personnes au plus, deux ou trois niveaux seulement passent le seuil et l'ecart porte
   alors sur une paire arbitraire. Le regroupement gauche, centre, droite est celui de a1,
   recopie de sa fonction `bloc_ideologie`, mecanique et sans jugement. **C'est cet axe qui
   porte le chiffre comparable au 2,3 de Chen.**

| condition | version | rapport d'ecart | delta eta carre |
|---|---|---|---|
| humains vague 2 (controle) | ponctuelle | 1,045 | -0,006 |
| **C2** | argmax | **1,364** | **+0,269** |
| **C2** | distribution | **1,315** | **+0,222** |
| agents v8 | ponctuelle | 2,379 | +0,480 |
| agents entretien (v3) | ponctuelle | 1,563 | +0,107 |
| agents composite | ponctuelle | 1,205 | +0,079 |
| agents enquete | ponctuelle | 1,084 | +0,075 |
| agents v7 | ponctuelle | 0,616 | -0,015 |
| agents demographiques (v6) | ponctuelle | 0,507 | -0,036 |

[MESURE, trace partielle, axe ideologie en trois blocs, 65 items ordinaux] Les huit points
demandes sont la, sur la meme regle graduee que Chen.

**Trois lectures.**

- **Six conditions sur huit sont positives sur `delta eta carre`, les deux negatives sont
  les deux invites pauvres, v6 et v7.** Le sens est celui de Chen, gonflement, et non
  celui de l'aplatissement.
- **Les valeurs sont beaucoup plus grandes que les siennes.** Chen publie de +0,026 a
  +0,104 sur le GSS. Nous mesurons +0,269 pour C2 et +0,480 pour v8. Deux explications
  possibles, non separees : nos segments sont plus grossiers, trois blocs contre sept
  niveaux, ce qui concentre l'effet ; et nos 55 personnes surestiment `eta carre` par
  construction, l'estimateur plug in etant positivement biaise en petit echantillon.
  **Les valeurs absolues ne doivent donc pas etre comparees aux siennes, seul le signe et
  le classement le peuvent** [PROBABLE].
- **Le contraste 2 de a15 sur cette mesure va dans le meme sens que la section 3** :
  la version distributionnelle gonfle **un peu moins**, +0,222 contre +0,269, la ou Chen
  trouve l'inverse pour Sonnet. Signe conserve, ampleur legerement moindre.

---

## 6. Tableau 4 : decodage ou conditionnement, la question 3 de a7

a7 section 10 question 3 demandait si le deficit de dispersion totale, `T` de 0,80 a 0,89
pour les conditions de Stanford, vient du **decodage**, donc traitable par la lecture des
logits, ou du **conditionnement**. Nous sommes le seul travail qui puisse y repondre,
parce que nous avons la distribution complete du modele et pas seulement sa sortie.

| version | dispersion totale, bits | ratio | entropie individuelle moyenne | temperature |
|---|---|---|---|---|
| humains vague 1 | 182,42 | 1,000 | 0 par construction | |
| humains vague 2 (controle) | 180,87 | 0,992 | 0 par construction | |
| **C2, version 1, argmax** | **120,25** | **0,659** | 0 | 1 |
| **C2, version 2, tirage** | **122,82** | **0,673** | **0,115 bit** | 1 |
| **C2, version 3, borne en temperature** | 182,42 | 1,000 | **0,928 bit** | **5,71** |

[MESURE, trace partielle, `a18-dispersion-totale.csv`]

**Definition de la version 2, et sa reserve.** Tirer la reponse de chaque personne dans sa
propre distribution donne une distribution de population dont l'**esperance exacte** est le
melange des distributions individuelles. On calcule donc l'entropie de ce melange, ce qui
est l'esperance analytique demandee et non un tirage. La reserve a ecrire : l'entropie de
la distribution esperee n'est pas l'esperance de l'entropie d'un tirage fini, la seconde
est legerement plus basse, d'un terme que la correction de Miller Madow chiffre deja et qui
vaut ici de l'ordre du centieme de bit.

**Definition de la version 3.** On cherche par bissection le scalaire `tau` tel que
`q proportionnel a p^(1/tau)` amene le ratio de la version 2 a 1. L'argmax etant invariant
par cette transformation, **la temperature ne peut pas rendre le modele plus juste, elle ne
peut que le rendre plus disperse** : l'exactitude argmax ne bouge pas d'un centieme, c'est
l'exactitude esperee qui paie.

**Le resultat, et il tranche la question.** Passer de l'argmax au tirage gagne **1,4 point
sur les 34 qui manquent**, soit 4 pour cent du deficit. Le ratio reste a 0,673, loin de 1.
**Le deficit de dispersion totale n'est pas dans le decodage.** Il faudrait une temperature
de 5,71, qui porte l'entropie individuelle moyenne de 0,115 a 0,928 bit, soit un facteur
huit, pour le combler. Ce n'est plus une correction de decodage, c'est le remplacement de
la distribution du modele par une autre.

Ce chiffre repond directement a a7 : la reponse oriente vers la famille B de
`exploration/09`, le conditionnement, et non vers la famille A, la lecture des logits.

### Entropie individuelle et calibration

| | C2, 8 116 cellules |
|---|---|
| entropie individuelle moyenne | 0,115 bit sur un maximum moyen de 1,594, soit **7,2 pour cent** |
| deciles de l'entropie individuelle | q10 0,000 ; q25 0,000 ; **mediane 0,0005** ; q75 0,033 ; q90 0,472 ; max 2,526 |
| part des cellules a p max superieure a 0,99 | **80,0 pour cent** |
| ecart de calibration attendu (ECE) | **0,441** |

[MESURE, trace partielle] **La mediane de l'entropie individuelle vaut cinq dix millemes de
bit.** Le modele n'hesite pas : il est certain, et il a tort une fois sur deux.

| decile de confiance | n | confiance moyenne | exactitude reelle | ecart |
|---|---|---|---|---|
| 0,9 a 1,0 | 7 312 | 0,9952 | **0,545** | **-0,450** |
| 0,8 a 0,9 | 265 | 0,8575 | 0,343 | -0,514 |
| 0,7 a 0,8 | 179 | 0,7542 | 0,363 | -0,391 |
| 0,6 a 0,7 | 172 | 0,6547 | 0,378 | -0,277 |
| 0,5 a 0,6 | 158 | 0,5470 | 0,367 | -0,180 |

[MESURE, trace partielle] Quand ce modele dit 0,995, il a raison une fois sur deux. Le
smoke test de a5 avait mesure 0,66 sur 80 cellules ; sur 7 312 cellules c'est 0,545. La
calibration est **pire** que ce que le smoke test laissait croire.

---

## 7. Tableau 5 : le critere A6 en version positive

a7 a pose le critere A6 en version negative : quand on **fabrique** de la variance intra,
les individus deplaces ne se rapprochent pas de leur vraie reponse, 1 789 reparations
contre 3 195 casses. Ici la version positive : **la variance intra que le modele produit
spontanement est elle placee sur les bons individus ?**

Protocole. Pour chaque personne, sa **deviance** est la part des items ou sa reponse
s'ecarte du mode de son segment, mode calcule sur les humains de la vague 1 **en laissant
la personne de cote**, sans quoi une personne influencerait son propre mode. On correle
ensuite, sur les personnes, la deviance de l'agent et celle de la vraie personne.

Axe profil croise, 55 personnes.

| condition | r | rho | deviance agent | deviance humaine | r exactitude / consistance |
|---|---|---|---|---|---|
| humains vague 2 (controle) | **0,890** | 0,878 | 0,405 | 0,409 | 0,999 |
| agents enquete | 0,870 | 0,875 | 0,394 | 0,409 | 0,789 |
| agents composite | 0,861 | 0,840 | 0,397 | 0,409 | **0,863** |
| agents entretien (v3) | 0,830 | 0,830 | 0,404 | 0,409 | 0,730 |
| agents demographiques (v6) | 0,693 | 0,746 | 0,380 | 0,409 | 0,644 |
| **C2** | **0,638** | 0,619 | **0,462** | 0,409 | **0,361** |
| agents v8 | 0,601 | 0,624 | 0,406 | 0,409 | 0,537 |
| agents v7 | 0,505 | 0,555 | 0,391 | 0,409 | 0,486 |

[MESURE, trace partielle] Axe ideologie dans `a18-critere-a6.csv`, meme classement, valeurs
plus basses.

**Trois lectures.**

1. **Le controle passe.** Les memes personnes deux semaines plus tard sont a r = 0,890 : la
   deviance au mode de segment est une propriete stable de la personne, et la correler a du
   sens.
2. **C2 est la seule condition dont la deviance moyenne DEPASSE celle des humains**, 0,462
   contre 0,409, et sa correlation est parmi les plus basses, 0,638. Autrement dit **C2
   s'ecarte du stereotype de groupe plus souvent que les vraies personnes, et pas pour les
   memes personnes.** C'est du bruit, pas de l'heterogeneite. Toutes les conditions de
   Stanford sont sous la deviance humaine, ce qui est le profil attendu d'un ecrasement.
3. **Le r entre exactitude par personne et consistance test retest reproduit a1 section 6.**
   a1 mesurait 0,684 pour composite sur 1 052 personnes ; nous mesurons **0,863** sur 55.
   Le classement de a1 est reproduit, riches en information au dessus, pauvres en dessous,
   et **C2 est a 0,361**, dans la bande des conditions pauvres que a1 chiffrait a 0,37.

Ce dernier point est le seul chiffre de ce rapport qui reproduise un resultat publie de a1
sur un echantillon dix fois plus petit. Il sert de controle de sante de toute la chaine.

---

## 8. Tableau 6 : le tableau recapitulatif, celui du papier

55 personnes, 149 items, 8 116 cellules. La colonne "ideologie" dit si l'etiquette
ideologique est dans l'invite, seul moyen de savoir avec qui chaque ligne se compare.

| condition | ideologie | exactitude | esperee | inter ideo | inter genre | intra | total | diversite | accord |
|---|---|---|---|---|---|---|---|---|---|
| humains vague 2 | sans objet | 0,7944 | 0,7944 | 0,99 | *2,11* | 0,986 | 0,990 | 99,1 % | 51,1 % |
| **C2** | oui, dans l'invite | **0,5263** | **0,5255** | **6,63** | *-1,95* | **0,580** | **0,659** | **65,9 %** | **67,3 %** |
| agents v8 | oui, dans l'invite | 0,5751 | 0,5751 | 7,78 | *-1,78* | 0,709 | 0,814 | 81,0 % | 58,8 % |
| agents composite | non, a reconstruire | 0,6901 | 0,6901 | 2,15 | *1,84* | 0,856 | 0,880 | 87,8 % | 55,7 % |
| agents enquete | non, a reconstruire | 0,6571 | 0,6571 | 2,24 | *0,84* | 0,808 | 0,832 | 83,1 % | 57,8 % |
| agents entretien (v3) | non, a reconstruire | 0,6697 | 0,6697 | 2,77 | *1,99* | 0,827 | 0,859 | 86,0 % | 57,3 % |
| agents demographiques (v6) | non | 0,6086 | 0,6086 | 0,15 | *1,76* | 0,626 | 0,626 | 63,0 % | 68,8 % |
| agents v7 | inconnu | 0,5871 | 0,5871 | 0,22 | *-0,16* | 0,618 | 0,607 | 61,7 % | 70,0 % |
| C2, version distributionnelle | | | | 6,23 | *-1,79* | 0,593 | 0,665 | | |
| plafond humain test retest | | 0,7944 [0,7685 ; 0,8193] | | | | | | | |

[MESURE, trace partielle] La colonne inter genre est en italique parce que son controle ne
passe pas, section 4. Elle figure au tableau parce que la mission la demande, elle ne doit
pas etre lue.

**La colonne "esperee" n'est informative que pour C2 et C3.** Pour les autres, une reponse
ponctuelle est une distribution de Dirac et l'exactitude esperee vaut l'exactitude argmax
par construction. Pour C2, l'ecart est de **0,0008**, huit dix millemes : le modele
n'hesite pas.

**L'accord par paires de C2 vaut 67,3 pour cent, contre 51,1 pour cent pour les memes
personnes reinterrogees** [MESURE, trace partielle]. Deux repondants tires au hasard dans
notre population simulee donnent la meme reponse deux fois sur trois, contre une fois sur
deux chez les humains. a0 mesure 66,4 pour cent contre 49,5 pour cent sur les agents
demographiques de Stanford et les 1 052 personnes [MESURE, a0]. **Notre pipeline reproduit
donc la mesure fondatrice du projet, a un point pres, sur nos propres agents et un autre
modele.**

---

## 9. La figure

`resultats/a18-figure-c2-c3.png` et `.svg`. Le plan des deux ratios de a1, meme convention,
memes axes logarithmiques, meme hyperbole du produit egal a 1 et meme quadrant grise. Les
six conditions de Stanford, les humains des deux vagues, et **C2 et C3 chacune en deux
points relies par une fleche, argmax vers distribution**. Ce sont les deux versions
demandees, et la fleche est le contraste 2 de a15 rendu visible.

Les intervalles horizontaux ne sont traces que lorsque leur borne basse est positive : une
barre qui sort du cadre ferait croire a une precision qui n'existe pas. Le CSV porte les
valeurs completes.

---

## 10. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise, des maintenant, sur la trace partielle

1. **Que le deficit de dispersion totale n'est pas un artefact de decodage.** Le chiffre
   est direct : 0,659 en argmax, 0,673 en tirage, sur 8 116 cellules. C'est la reponse a la
   question 3 de a7 et aucun autre travail lu ne peut la donner, parce qu'aucun ne conserve
   la distribution complete du modele.
2. **Que la version distributionnelle de la decomposition existe, qu'elle est une
   generalisation exacte de la version ponctuelle, et que le controle le prouve au bit
   pres.** C'est un apport de methode independant du resultat.
3. **Que C2 se comporte comme v8 et pas comme v6 sur l'axe ideologie**, 6,63 contre 7,78 et
   0,15. L'ecart est de deux ordres de grandeur, il ne depend d'aucun intervalle.
4. **Que le modele est certain et faux** : mediane d'entropie individuelle a 0,0005 bit,
   80 pour cent des cellules au dessus de 0,99 de confiance, 54,5 pour cent d'exactitude
   dans ce decile, ECE de 0,441.

### Interdit

1. **Toute conclusion sur C2 contre C3.** La trace C3 n'existe pas. Les trois issues de
   a15 restent ouvertes.
2. **Toute lecture des colonnes genre, race et education.** Le controle de la vague 2 n'y
   passe pas et le denominateur humain y est trop petit. Le dire, ne pas les publier.
3. **Toute comparaison des valeurs absolues de `delta eta carre` avec celles de Chen.**
   Nos segments sont plus grossiers et notre echantillon dix fois plus petit que sa plus
   petite cellule. Seuls le signe et le classement sont comparables.
4. **Toute presentation de C2 comme une replication de l'agent demographique de Stanford.**
   C2 contient l'ideologie et le parti ; c'est la variante augmentee, et son homologue est
   v8 [CONFIRME, a17 objection 3].
5. **Tout chiffre de ce rapport, tel quel, dans un texte destine a Simon.** Ce sont des
   chiffres de trace partielle, ils bougent a chaque lancement.

---

## 11. Ce que je n'ai pas pu verifier

1. **La condition C3 n'a produit aucune cellule.** Tout le contraste prioritaire de a15,
   qui est la raison d'etre de cette analyse, attend le matin. Le script la detecte seule
   et l'ajoute a toutes les tables sans modification.
2. **Le terme inter n'est pas estimable a 55 personnes, et probablement pas non plus a
   150.** Le controle de la vague 2 sort a 1,167 avec un intervalle qui deborde. a1 avait
   1 052 personnes. **Si le controle ne passe toujours pas a 150 personnes sur l'axe
   ideologie, aucun ratio inter de a18 n'est publiable et il faudra soit elargir
   l'echantillon, soit changer d'estimateur.** C'est le risque principal de ce chantier et
   il n'est pas ecarte.
3. **Le seuil d'occupation de Miller Madow est un choix.** Il change le terme inter de
   l'entropie d'un facteur neuf sur la voie distributionnelle, 145,99 contre 16,98. Gini
   Simpson y est totalement insensible et donne le meme signe. Je n'ai pas trouve de
   litterature sur l'estimation d'entropie a partir d'un melange de distributions
   predites ; le choix est raisonne mais il n'est pas source.
4. **La version 3, borne en temperature, suppose que la distribution lue est complete.**
   Une modalite absente du top 40 a une probabilite lue de zero exact, et aucune
   temperature ne la ramene. a5 mesure zero modalite absente sur ses controles, donc
   l'effet est nul ici, mais la propriete du script n'est pas garantie sur un autre run.
5. **Le prompt de C2 n'a pas ete compare a celui de v8.** L'ecart de 6,63 contre 7,78 peut
   venir du modele, de la formulation, ou des deux. C'est la limite 4 de a5 section 7 et
   elle vaut ici aussi.
6. **Un seul modele, Qwen3-4B en 4 bits.** La quasi degenerescence des distributions, qui
   porte les sections 6 et 8, peut etre une propriete de ce modele, de cette
   quantification, ou des deux.
7. **Le biais de position n'est pas mesure.** La passe 2 de C3 n'a pas tourne.
8. **La deviance de la section 7 est calculee sur les items ou l'agent a repondu**, donc
   sur les memes cellules pour toutes les conditions grace au masque commun, mais elle
   n'est pas ponderee par la difficulte de l'item. Une personne dont les items sont faciles
   aura une deviance basse pour une raison qui n'est pas la sienne.

---

## 12. Questions ouvertes pour Simon

1. **Le terme inter est il mesurable a 150 personnes ?** Le controle de la vague 2 est le
   juge, et a 55 personnes il ne passe pas. Trois issues : accepter de ne publier le terme
   inter que sur les 1 052 personnes de a1 et ne publier de C2 et C3 que le terme intra,
   la dispersion totale et la calibration ; monter l'echantillon a 400 personnes, ce qui
   coute trois nuits ; ou changer d'estimateur pour un estimateur bayesien du type NSB, qui
   demande une journee d'implementation. Laquelle ?
2. **La reponse a la question 3 de a7 suffit elle a orienter le chantier ?** Le deficit de
   dispersion totale n'est comblable ni par la lecture des logits ni par une temperature
   raisonnable. Cela ferme la famille A de `exploration/09` et laisse la famille B. Est ce
   assez pour reorienter, ou faut il d'abord reproduire sur un modele plus gros ?
3. **La quasi degenerescence est elle un resultat ou une propriete de Qwen3-4B en 4 bits ?**
   80 pour cent des cellules au dessus de 0,99 de confiance avec 54,5 pour cent
   d'exactitude dans ce decile, c'est une mesure d'ecrasement au niveau de l'appel
   qu'aucun papier lu ne publie. Elle est gratuite, elle sort de la meme trace. Faut il en
   faire une mesure du dossier maintenant, ou attendre gpt-oss-20b ?
4. **Faut il publier la version distributionnelle de la decomposition ?** Elle a un cout :
   un degre de liberte a declarer sur l'entropie, et un ecart avec Chen sur le sens de
   l'ecart argmax contre distribution, il gonfle plus, chez nous elle gonfle un peu moins.
   Elle a un gain : nous serions le seul travail a l'avoir testee a modele, temperature et
   donnees constants. Le gain vaut il l'ouverture au relecteur ?
5. **L'ideologie en trois blocs est elle acceptable comme axe de la mesure a la Chen ?**
   Elle est necessaire a 150 personnes et elle vient de a1, donc elle n'est pas choisie
   pour arranger. Mais elle n'est pas l'axe de Chen, et nos `delta eta carre` sont trois
   fois les siens. Faut il publier l'axe a sept niveaux avec sa reserve, l'axe a trois
   blocs avec la sienne, ou les deux ?
6. **La deviance de C2 depasse celle des humains.** C'est le seul cas du tableau. Un agent
   qui s'ecarte du stereotype de groupe PLUS que les vraies personnes, et pas pour les
   memes, est un cas que la litterature ne decrit pas : elle ne parle que d'ecrasement.
   Est ce un resultat a creuser, ou un artefact de l'invite demographique augmentee de
   l'ideologie ?

---

## 13. La commande a rejouer au matin

Verifier d'abord que le run est fini et que les deux traces sont completes.

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
grep -E "appels en|RUN TERMINE" data/traces/a5-run.log
wc -l data/traces/a5-C2-p1.jsonl data/traces/a5-C3-p1.jsonl
```

Puis, dans cet ordre.

```
# 1. l'evaluation de a5, inchangee, cinq a dix minutes
.venv/bin/python analyses/a5_evaluer.py

# 2. la decomposition de a18, une a deux minutes sur 150 personnes et deux conditions
.venv/bin/python analyses/a18_decomposition_traces.py
```

Options utiles.

```
# essai rapide, bootstrap 100 et 15 permutations, une vingtaine de secondes
.venv/bin/python analyses/a18_decomposition_traces.py --rapide

# si le run a ete tronque et couvre peu de personnes, abaisser le seuil d'item
# et le dire dans le rapport : les termes inter deviennent tres bruites
.venv/bin/python analyses/a18_decomposition_traces.py --n-min 10

# n'exiger qu'une couverture de 90 pour cent des items par personne
.venv/bin/python analyses/a18_decomposition_traces.py --couverture 0.90
```

**Ce qu'il faut regarder en premier dans la sortie, dans cet ordre.**

1. La ligne `CONTROLE PASSE` de la degenerescence. Si elle manque, rien n'est publiable.
2. La ligne `controle vague 2 par axe`. Les axes ou elle s'ecarte de 1 sont a ecarter.
3. Le bloc `VERDICT SUR LES TROIS ISSUES DE a15`, qui nomme l'issue observee.
4. Le bloc `LE BON VIS A VIS DE C2`, qui dit si C2 tombe du cote de v8.
5. La ligne `2 tirage, esperance` du tableau de dispersion totale, qui tranche a7.

---

## 14. Fichiers produits

| fichier | contenu |
|---|---|
| `analyses/a18_decomposition_traces.py` | le script, une commande, aucun appel de modele |
| `a18-figure-c2-c3.png` et `.svg` | le plan (inter, intra), C2 et C3 en deux versions |
| `a18-decomposition.csv` | les deux ratios par condition, version et mesure, avec P(sup) |
| `a18-ratios-par-axe.csv` | le detail axe par axe, avec le denominateur humain |
| `a18-chen.csv` | rapport d'ecart et `delta eta carre`, sept axes, huit conditions |
| `a18-dispersion-totale.csv` | les trois versions du ratio de dispersion totale |
| `a18-calibration.csv` | entropie individuelle, deciles, fiabilite par decile, ECE |
| `a18-critere-a6.csv` | le critere A6 en version positive, deux axes |
| `a18-recapitulatif.csv` | le tableau du papier |
| `a18-controle-degenerescence.csv` | le controle, chiffre |
| `a18-sensibilite-occupation.csv` | la sensibilite au seuil de Miller Madow |
| `a18-journal.json` | tous les agregats, pour un rejeu sans relire la sortie |

`.gitignore` exclut `*.csv` : ces fichiers ne seront pas versionnes, les chiffres qui
comptent sont recopies dans le present rapport, qui l'est. **Aucune microdonnee n'a quitte
`data/`.** Les traces ont ete ouvertes en lecture seule, aucun appel API distant.
