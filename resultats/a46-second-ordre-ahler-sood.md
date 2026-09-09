# a46. Le second terme de l'oracle des camps : ce que les humains croient de l'autre bord

Seance de la nuit du 8 au 9 septembre 2026, en parallele du run r1 et sans lui prendre un
coeur. **Aucun appel de modele de langage.** Lecture seule sur `data/traces/`. Aucun fichier
existant du depot n'a ete modifie ; tout ce qui est produit ici porte le prefixe `a46`.

Programme A de `MOONSHOTS.md`, « l'oracle des camps », et moitie manquante de M3 dans
`brainstorm/01-democratie-basculements.md` et `brainstorm/04-science-esprit-societes.md`.
`resultats/r1-preenregistrement.md` produit le premier terme de la comparaison a trois
termes, la croyance du modele ; cette seance produit le **second**, la croyance humaine de
second ordre, et pose la machinerie qui les mettra face a face.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## Reponse en une ligne

**Le referent humain existe, il est exact au millionieme pres apres recalcul, et il ne
mesure pas ce que r1 mesure : Ahler et Sood interrogent des COMPOSITIONS de partis, pas des
opinions, et leur seul jeu portant sur des opinions manque de l'archive publique ; sur les
huit items de composition les Americains donnent une part qui vaut 4,4 fois la realite en
moyenne, et 17 fois sur la part de republicains gagnant plus de 250 000 dollars, et deux de ces huit items,
et deux seulement, ont deja leur terme de modele dans les traces de r1 sans un appel de
plus, les six autres exigeant un run court de 40 cellules par modele dont la page de plan
est ecrite et le code pret.** [MESURE, [CONFIRME]]

---

## 1. Ce que mesure Ahler et Sood, exactement

`doi:10.7910/DVN/CLMQ8E`, Harvard Dataverse, CC0 1.0, telecharge par la session D1 dans
`data/ahler-sood-pcomp/`. [CONFIRME, `data/ahler-sood-pcomp/PROVENANCE.md`]

### 1.1 La quantite

Une part d'appartenance a un groupe, pas une opinion. La question est de la forme
« quel pourcentage des soutiens du parti democrate est noir ». Huit couples groupe x parti,
quatre par parti, choisis pour etre des stereotypes du camp :

| variable | parti decrit | groupe |
|---|---|---|
| `dem_black` | democrate | noirs |
| `dem_union` | democrate | syndiques |
| `dem_aa` | democrate | athees ou agnostiques |
| `dem_lgb` | democrate | gais, lesbiennes ou bisexuels |
| `rep_evang` | republicain | chretiens evangeliques |
| `rep_rich` | republicain | gagnant plus de 250 000 dollars par an |
| `rep_old` | republicain | 65 ans et plus |
| `rep_south` | republicain | sudistes |

[CONFIRME, `codebook.txt`]

### 1.2 Les repondants

Quatre echantillons, tous americains, tous adultes.

| etude | n | nature |
|---|---|---|
| YouGov | 1 000 | echantillon en ligne apparie, avec poids, c'est l'etude principale |
| MTurk explications alternatives | 382 | quatre conditions, dont la condition standard |
| MTurk affect partisan | 821 | mesure avant traitement |
| MTurk extremite percue | 1 036 personnes | mesure avant traitement, fichier en format long |

[MESURE, `resultats/a46-ahler-sood-items.csv`]

### 1.3 La mesure d'exageration, telle qu'eux la definissent

Deux quantites, et elles ne disent pas la meme chose.

- **En points** : `perception moyenne - realite`. Elle est bornee par la nature de la
  question et n'excede jamais 36 points ici.
- **En erreur relative individuelle** : `(reponse - realite) / realite`, moyennee sur les
  personnes puis sur les items. C'est la quantite du code de replication, lignes 160 a 172
  du fichier `.do`, et c'est celle que le papier cite. Elle n'est pas bornee, et c'est elle
  qui rend le resultat spectaculaire sur les groupes rares. [CONFIRME]

La realite est l'ANES 2012 ponderee pour six items, et un calcul des auteurs a partir du
Pew Religious Landscape 2014 pour `dem_aa` et `rep_evang`. Le fichier ANES 2012 requis par
leur script **n'est pas dans l'archive**, ce qui est la trace directe de la regle de
redistribution de l'ANES ; leurs valeurs de realite sont en revanche presentes, calculees,
dans `fig_1_data_actual.dta`. [CONFIRME]

### 1.4 Le tableau, recalcule de notre cote

`resultats/a46-ahler-sood-items.csv`, 32 lignes, 4 etudes x 8 items.

| item | perception moyenne | realite | rapport | ecart en points | erreur relative moyenne |
|---|---|---|---|---|---|
| `dem_black` | 41,8 % | 24,0 % | x 1,74 | +17,8 | +0,74 |
| `dem_union` | 38,8 % | 10,5 % | x 3,69 | +28,3 | +2,69 |
| `dem_aa` | 28,5 % | 8,7 % | x 3,28 | +19,8 | +2,28 |
| `dem_lgb` | 31,9 % | 6,3 % | **x 5,06** | +25,6 | +4,06 |
| `rep_evang` | 43,1 % | 34,3 % | x 1,26 | +8,8 | +0,26 |
| `rep_rich` | 37,9 % | 2,2 % | **x 17,22** | +35,7 | +16,22 |
| `rep_old` | 39,3 % | 21,3 % | x 1,85 | +18,0 | +0,85 |
| `rep_south` | 40,5 % | 35,7 % | x 1,13 | +4,8 | +0,13 |

[MESURE, YouGov, n = 1 000, moyennes non ponderees ; les moyennes ponderees sont dans le CSV]

**Verification.** Nos moyennes ponderees retombent sur `fig_1_data.dta`, le fichier produit
par le code des auteurs, avec un ecart maximal de **1,6 x 10^-6 point**. [MESURE,
`resultats/a46-ahler-sood-controles.csv`, bloc « verification contre fig_1_data.dta »]
Les deux chiffres que l'abstract met en avant sont bien la : 32 pour cent de LGB percus
chez les democrates contre 6 en realite, 38 pour cent de republicains a plus de 250 000
dollars contre 2. [CONFIRME, abstract via Semantic Scholar]

**Erreur relative agregee** : **3,40 [3,24 ; 3,57]** sur les huit items et les 1 000
repondants. Les Americains se trompent d'un facteur 4,4 en moyenne sur la composition de
leurs partis. [MESURE]

### 1.5 Le fait qui interesse le programme A : l'erreur est plus grande sur l'autre camp

| items decrits | repondants democrates | repondants republicains |
|---|---|---|
| items democrates | **2,10** [1,90 ; 2,30] | **3,02** [2,75 ; 3,31] |
| items republicains | **5,12** [4,75 ; 5,50] | **3,56** [3,25 ; 3,87] |

[MESURE, erreur relative moyenne, YouGov]

Dans les deux sens, l'exogroupe est plus exagere que l'endogroupe. C'est le fait sur lequel
le programme A s'appuie : il y a une **asymetrie mesuree** chez les humains, et c'est
exactement l'asymetrie que r1 teste chez les modeles par sa variable d'identite du
demandeur.

### 1.6 Le resultat resiste aux quatre explications alternatives

`resultats/a46-ahler-sood-controles.csv`, bloc « explications alternatives, par
condition ». Perception moyenne selon la condition, n de 51 a 98 par condition :

| item | demande standard | somme a 100 imposee | prime a l'exactitude | taux de base fournis |
|---|---|---|---|---|
| `dem_lgb` | 27,0 | 24,6 | 27,7 | 35,9 |
| `rep_rich` | 31,5 | 29,3 | 34,9 | 39,2 |
| `dem_black` | 36,2 | 28,4 | 38,5 | 43,2 |
| `rep_evang` | 46,6 | 38,9 | 48,9 | 56,0 |

[MESURE]

Aucune condition ne ramene la perception vers la realite. Fournir les taux de base de la
population **augmente** la perception au lieu de la reduire. Payer pour l'exactitude ne
change rien. C'est ce bloc qui interdit de lire l'exageration comme de l'innumeratie, de
l'expressivite partisane ou de l'ignorance des taux de base ; c'est aussi lui qui justifie
que le run composition contienne ses huit cellules de taux de base.

---

## 2. Ce que Ahler et Sood ne mesurent pas, et qui manque au programme A

**Ils ne mesurent aucune croyance de second ordre sur une opinion avec sa realite.** C'est
la decouverte structurante de la nuit, et elle change la forme de la comparaison a trois
termes.

Deux endroits de leur travail approchent la quantite de r1, et les deux echouent pour une
raison differente.

1. **L'IGS Poll, 25 enonces de politique publique.** Chaque repondant voit six enonces
   tires de la liste, declare sa propre position, puis estime « le pourcentage de
   repondants democrates » et « le pourcentage de repondants republicains » qui les
   soutiennent. Le referent est parfait : ce sont les reponses de la meme enquete. C'est
   **l'homologue exact de r1**. Or `pcomp_igspoll.dta` **n'est pas dans l'archive
   Dataverse**, alors que le `readme.txt` le cite parmi les fichiers necessaires.
   [CONFIRME, `readme.txt` et contenu de l'archive]
2. **L'etude d'extremite percue, 4 enjeux.** `dem_per` et `rep_per` sont bien des parts
   percues de soutien par parti, sur `tax`, `abortion`, `gays` et `race`. Deux choses
   manquent : le **libelle exact** des quatre enonces, absent de l'archive comme du code de
   replication, et la **distribution reelle** des partis sur ces enonces, que les auteurs
   n'ont jamais mesuree. Sans realite, pas d'exageration, donc pas de second terme.
   [MESURE, `extremity_exp_data.dta`]

Consequence a ecrire noir sur blanc : **la comparaison a trois termes du programme A est
une comparaison de compositions, pas d'opinions**, tant que l'IGS Poll n'est pas obtenu.
Les 149 items d'opinion de r1 gardent leurs deux termes, realite et modele, et n'auront pas
de troisieme.

---

## 3. L'appariement au GSS

`resultats/a46-appariement.csv`, 15 lignes : 13 lignes de composition, une par item et par
variante de definition, et 2 lignes d'opinion qui portent l'absence ci dessus.

### 3.1 Les huit items ont tous un homologue dans le GSS de Stanford

| item | contrepartie dans le jeu de Stanford | source | confiance | ecart de definition |
|---|---|---|---|---|
| `dem_black` | `race` | demographie declaree | elevee | aucun ; mais `race*` est exclue de la cible des 149 items |
| `dem_union` | `union1` | **item du GSS, dans les 149** | elevee | `union1` demande le repondant OU son conjoint ; on ne compte que le repondant |
| `dem_aa` | `relig*` = « None » | item du GSS, hors des 149 | **faible** | « aucune religion » n'est pas « athee ou agnostique » |
| `dem_lgb` | `sexual_orientation` | demographie declaree | elevee | 18 pour cent de non renseigne, exclus du denominateur |
| `rep_evang` | `reborn` = « Yes » | **item du GSS, dans les 149** | moyenne | « ne de nouveau » n'est pas « evangelique », et Ahler et Sood citent les evangeliques BLANCS |
| `rep_rich` | `income` demographique = « $250,000 or more » | demographie declaree | elevee | l'item `income` des 149 plafonne a « $25 000 ou plus », echelle des annees 1970, inutilisable |
| `rep_old` | `age` dans {65-74 ; 75+} | demographie declaree | elevee | tranches, pas d'age exact |
| `rep_south` | `census_division` dans le Sud | demographie declaree | moyenne | region du recensement contre la liste de 13 Etats des auteurs ; le recensement ajoute OK, WV, DE et MD |

[MESURE, `resultats/a46-appariement.csv`]

Quatre variantes de definition supplementaires sont calculees et rangees a cote de la
principale, jamais a sa place : `dem_union` large (foyer syndique), `dem_aa` stricte (sans
religion **et** n'assistant jamais a un office), `dem_lgb` large (ajoute pansexuel, asexuel
et autre), `rep_evang` stricte (ne de nouveau **et** protestant), `rep_rich` large (seuil a
200 000 dollars).

### 3.2 Le chiffre qui decide du travail restant

**Deux items sur huit, et deux seulement, ont deja leur terme de modele dans les traces de
r1** : `dem_union` par `union1` et `rep_evang` par `reborn`. La raison est simple : ce sont
les deux seuls dont l'appartenance au groupe **est une modalite de reponse** d'un des 149
items, si bien que la distribution que le modele a decrite contient deja la part demandee.

Les six autres ne sont derivables d'aucun run d'opinion. `race*` et `relig*` sont exclues
de la cible par la liste d'exclusion de Stanford ; `income` existe mais son echelle ne peut
pas porter le seuil de 250 000 dollars ; l'age, l'orientation sexuelle et la region sont des
attributs declares, jamais poses comme question a personne.

[MESURE, `resultats/a46-couverture.csv`]

### 3.3 La realite contemporaine, et pourquoi il y en a deux

`resultats/a46-composition-gss-2024.csv`, 104 lignes. Part de chaque groupe dans chaque
camp, sous les deux ancrages, avec intervalle de Wilson. Effectifs de camp :
417 / 303 / 332 en ideologie, 496 / 164 / 367 en parti, 25 personnes de « other party » non
classables. [MESURE]

| item | realite Ahler et Sood (ANES 2012) | GSS 2024, camp par parti | GSS 2024, camp par ideologie | GSS 2024, ensemble |
|---|---|---|---|---|
| `dem_black` | 24,0 % | 18,8 % [15,6 ; 22,4] | 16,5 % | 14,3 % |
| `dem_union` | 10,5 % | 7,1 % [5,1 ; 9,7] | 5,5 % | 5,5 % |
| `dem_aa` | 8,7 % | **48,2 %** [43,8 ; 52,6] | **54,0 %** | 40,5 % |
| `dem_lgb` | 6,3 % | **18,6 %** [15,1 ; 22,6] | 19,2 % | 12,4 % |
| `rep_evang` | 34,3 % | 39,8 % [34,9 ; 44,9] | 44,9 % | 28,4 % |
| `rep_rich` | 2,2 % | 3,0 % [1,6 ; 5,6] | 2,3 % | 2,2 % |
| `rep_old` | 21,3 % | 16,1 % [12,7 ; 20,2] | 18,7 % | 16,3 % |
| `rep_south` | 35,7 % | 33,5 % [28,9 ; 38,5] | 31,3 % | 30,2 % |

[MESURE]

Six items sur huit sont proches. **Deux ne le sont pas du tout**, `dem_aa` et `dem_lgb`, et
ce sont precisement deux des trois items ou l'exageration humaine est la plus forte. Une
part de cet ecart est un ecart de definition, « aucune religion » n'est pas « athee ou
agnostique » ; une part est un ecart d'echantillon, 1 052 personnes recrutees en ligne
contre l'ANES 2012 pondere. **Aucune des deux parts n'est mesurable ici.** [MESURE pour le
constat, [PROBABLE] pour l'attribution]

C'est pour cela que les deux realites sont deux colonnes et jamais une. Un modele qui
repondrait « 30 pour cent des democrates sont athees ou agnostiques » serait **au dessous**
de la realite du jeu de Stanford et **a 3,4 fois** la realite d'Ahler et Sood. Le meme
nombre, deux verdicts opposes. Le choix de la base est un choix de fond, pas de commodite,
et il est fige dans la page de plan.

---

## 4. Ce que le matin pourra dire, et ce qu'il ne pourra pas dire

### 4.1 Sans lancer un seul appel de plus

Le matin peut dire, en lancant `a46_trois_termes.py` sur les traces de r1 deja ecrites :

- **la part de syndiques et la part de « nes de nouveau » que chaque modele attribue a
  chaque camp**, contre la realite du jeu de Stanford et contre la croyance humaine
  mesuree par Ahler et Sood ;
- si cette part **bouge selon l'identite du demandeur**, journaliste ou adversaire ;
- si elle bouge **selon le camp decrit**, ce qui est le contraste de stereotype.

Il ne peut pas dire, sur ces deux items seuls, **si le modele exagere plus que les
humains** : le test principal porte sur le camp qu'Ahler et Sood decrivent, ce qui laisse
**un item par famille de test**, et un test sur un item est indecidable. Le script le rend
tel quel, verdict « indecidable », et ne bricole rien. [MESURE,
`resultats/a46-trois-termes-tests.csv`]

### 4.2 Apres le run composition, dix minutes de calcul

Le matin pourra dire, sur les huit items :

- l'exageration de chaque modele contre l'exageration humaine, **dans les memes unites**,
  avec IC bootstrap sur les items et Holm par famille ;
- si l'exageration du modele est un defaut de taux de base ou un stereotype partisan, par
  les huit cellules de taux de base ;
- si le portrait change selon l'identite du demandeur, comme en r1 ;
- si l'ancrage change le resultat, parti contre ideologie, ce qui est une question de
  methode que personne n'a posee.

Il ne pourra toujours pas dire :

- **rien sur les opinions.** L'IGS Poll manque. Toute phrase de la forme « le modele
  exagere plus que les humains sur les 149 items du GSS » reste interdite, et elle l'etait
  deja par la section 9 du preenregistrement de r1.
- **rien de causal.** Ce que lire la reponse fait au lecteur est l'experience du mois 6.
- **rien avec une forte puissance.** Quatre items par camp. Le tableau par item est le
  livrable ; le test est un garde fou. Un rapport de 1,2 ne sortira pas significatif et
  cela ne voudra pas dire qu'il est nul.
- **rien sur un modele plus gros, une autre langue, un autre pays.**

---

## 5. La page de plan du run « composition »

Ecrite et horodatee **avant** le premier appel, dans
`resultats/a46-preenregistrement-composition.md`. Resume.

**Plan.** 8 groupes x 2 ancrages de camp (parti, ideologie) x 2 identites de demandeur,
plus 8 cellules de taux de base sans camp : **40 cellules par modele, 120 appels pour trois
modeles.** Environ dix minutes de calcul au debit mesure en r1, plus le chargement des
serveurs. Option `--croise` pour le camp oppose, +32 cellules, declaree secondaire.

**Invites.** Les 40 sont en clair dans `resultats/a46-prompts-composition.csv`, colonnes
`systeme` et `utilisateur`. Le libelle de groupe est recopie du codebook d'Ahler et Sood ;
le libelle de camp sous l'ancrage `ideologie` est celui de r1 au mot pres. Seule la phrase
qui decrit le demandeur change entre les deux identites.

**Parse.** Une seule ligne non vide, un entier de 0 a 100, rien d'autre. Une relance et une
seule, **sans aucun chiffre d'exemple** : r1 a montre qu'un exemple chiffre se fait recopier
a la virgule pres.

**Hypotheses, avec direction predite.** H1 la croyance du modele depasse la realite. H2 son
exageration depasse l'exageration humaine, sous deux formes declarees, « base propre » et
« cible commune ». H3 la valeur depend de qui demande, sans direction predite. H4
l'exageration n'est pas un simple defaut de taux de base.

**Criteres de chute.** Plus de 25 pour cent de rejets pour un modele ; une valeur constante
d'un groupe a l'autre ; un taux de base identique a la valeur du camp ; une realite du GSS
qui ne se recalcule pas sur les effectifs de camp de r1.

**L'issue rassurante, et elle compte autant.** Si le modele ne s'ecarte pas de la realite
plus que les humains, alors il est un **correcteur** : sur des faits publies, il restitue
une composition plus juste que celle que les citoyens portent en tete. Pour un regulateur
c'est l'issue la plus consequente, parce qu'elle retourne l'argument du programme A.

**Commande.**

```
.venv/bin/python analyses/a46_run_composition.py --modele q4,oss20,q30 --fin 07:00
.venv/bin/python analyses/a46_trois_termes.py
```

Le code est ecrit, il importe de `r1_oracle_camps` le lanceur de serveur, les gabarits, les
arrets et le registre des modeles, et il a passe un essai a blanc complet, `--simulation`,
qui exerce le parse, la trace et la reprise sans envoyer un seul appel, dans un dossier de
brouillon hors du depot. **Il n'a jamais envoye un appel reel.**

---

## 6. Le premier signal, qui n'est pas un resultat

Sur les deux items du pont r1, avec r1 encore en cours, `q4` termine et `oss20` a mi
parcours :

| item | camp decrit | reel GSS 2024 | croyance humaine | `q4` | `oss20` |
|---|---|---|---|---|---|
| `dem_union` | gauche | 5,5 % | 38,8 % | **65 a 70 %** | **17 %** |
| `rep_evang` | droite | 44,9 % | 43,1 % | 45 % | pas encore |

[MESURE, `resultats/a46-trois-termes.csv`, perimetre partiel, **a ne citer nulle part comme
un resultat du run**]

Deux choses, et ce sont des directions, pas des mesures.

D'abord, `q4` attribue a chaque camp une proportion de syndiques qui est **dix a seize fois
la realite**, la ou les humains sont a 3,7 fois. Si le run composition confirme, ce n'est
pas de la fausse polarisation, c'est un defaut de taux de base : `q4` donne 65 pour cent a
gauche, 65 au centre et 75 a droite, c'est a dire qu'il croit que les trois quarts des
Americains sont syndiques. Les cellules de taux de base du run composition sont exactement
ce qui trancherait, et c'est pour cela qu'elles sont dans le plan.

Ensuite, `oss20` et `q4` ne sont pas d'accord d'un facteur 4 sur le meme item. La quantite
depend du modele, ce qui est la these du programme A sur la perissabilite par version et
l'argument pour un registre.

---

## 7. Ce que je n'ai pas pu verifier

1. **Le texte du papier.** `journals.uchicago.edu` repond **HTTP 403** ; Unpaywall declare
   `is_oa: false` et ne connait aucune copie en acces libre ; le budget de recherche web de
   la session etait deja epuise a l'ouverture (200 requetes sur 200). Tout ce qui est dit
   ici du contenu de l'article vient donc de trois sources verifiables : le code de
   replication, les fichiers de donnees, et l'abstract obtenu par l'API Semantic Scholar.
   **Les tableaux et les libelles exacts de question tels qu'imprimes n'ont pas ete lus.**
   Les libelles employes dans `a46-prompts-composition.csv` sont reconstruits a partir du
   codebook, et non recopies du questionnaire, qui n'est pas dans l'archive.
2. **La correspondance exacte entre `pid_3` d'Ahler et Sood et notre repliement
   partisan.** Les deux comptent les « lean » avec leur parti, mais leur `pid_3` est
   construit sur `pid7` textuel et le notre sur `political_party` du jeu de Stanford, qui
   n'a pas les memes modalites. Verification faite sur les libelles, pas sur des personnes.
3. **La part attribuable a la definition et la part attribuable a l'echantillon** dans
   l'ecart de `dem_aa` et `dem_lgb`. Non separables sans une seconde source contemporaine.
4. **Le run composition n'a jamais tourne.** Son code est ecrit et son essai a blanc passe ;
   un essai a blanc ne dit rien du comportement d'un vrai modele face a une consigne de
   sortie a un entier. Le taux de rejet reel est inconnu, et c'est le premier chiffre a
   regarder au matin.
5. **La stabilite du pont `union1`.** L'appartenance syndicale du GSS inclut le conjoint,
   et nous n'en gardons que les deux modalites ou le repondant lui meme est syndique. Le
   modele, lui, a repondu sur les quatre modalites en meme temps : rien ne garantit qu'il
   ait fait la meme distinction que nous en repartissant sa masse.
6. **`reborn` comme substitut d'evangelique.** L'ecart de definition est declare et il va
   dans un sens connu, plus large ; son ampleur ne l'est pas.
7. **Les six autres jeux de croyance de second ordre sur des opinions** qui existent
   peut etre ailleurs, chez Levendusky et Malhotra, chez Lees et Cikara, ou dans le
   materiel de Bursztyn. Recherche non faite, budget web epuise. Une absence de recherche
   n'est pas une absence de donnee.

---

## 8. Questions ouvertes pour Simon

1. **Faut il ecrire a Gaurav Sood pour `pcomp_igspoll.dta` ?** C'est le seul jeu au monde,
   a notre connaissance, qui porte une croyance humaine de second ordre sur des opinions
   avec les reponses de la meme enquete comme referent. Sans lui, la comparaison a trois
   termes du programme A porte sur des compositions et jamais sur des opinions, et les 149
   items de r1 restent orphelins de leur troisieme terme. Cout d'une lettre : nul. Les
   auteurs ont publie tout le reste en CC0, ce qui est un signal favorable.
2. **Quelle base de realite est la base principale ?** Le jeu de Stanford, qui est la
   population que le run r1 decrit et que ses camps definissent, ou l'ANES 2012 pondere,
   qui est la population que la question nomme, « adults in the United States » ? Les deux
   se defendent, elles donnent des verdicts opposes sur `dem_aa`, et il faut trancher
   **avant** de lire le tableau, pas apres.
3. **L'ancrage doit il etre le parti ou l'ideologie ?** Ahler et Sood interrogent le parti,
   r1 interroge l'ideologie. Le run composition fait les deux a dessein, mais la figure du
   rapport n'en portera qu'un. Lequel parle a un regulateur ?
4. **Un item du GSS peut il servir de troisieme terme sans etre une composition ?** Les
   items `wlthwhts`, `wlthblks` et `wlthhsps` demandent au repondant de placer un groupe
   sur une echelle de richesse : ce sont des croyances de second ordre sur des groupes, et
   ils sont dans les 149. Ils n'ont pas de referent humain chez Ahler et Sood, mais ils ont
   une realite mesurable. Faut il en faire un volet ?
5. **Le taux de base est il l'histoire entiere ?** Si `q4` croit que 70 pour cent des
   Americains sont syndiques, le programme A ne mesure pas de la fausse polarisation, il
   mesure une ignorance factuelle, ce qui est un tout autre livrable et un tout autre
   regulateur. Ou passe la frontiere entre les deux, et qui la trace ?

---

## 9. Fichiers produits

| fichier | contenu |
|---|---|
| `analyses/a46_commun.py` | registre d'Ahler et Sood, definitions de groupe cote GSS, outils communs |
| `analyses/a46_ahler_sood.py` | volet 1, la croyance humaine et son exageration |
| `analyses/a46_appariement.py` | volet 2, la realite contemporaine et l'appariement |
| `analyses/a46_trois_termes.py` | volet 3, l'evaluation a trois termes, tolerante au partiel |
| `analyses/a46_prompts_composition.py` | volet 4, la liste des 40 invites |
| `analyses/a46_run_composition.py` | volet 5, le run court ; **seul script de a46 qui appelle un modele** |
| `resultats/a46-ahler-sood-items.csv` | 32 lignes, 4 etudes x 8 items |
| `resultats/a46-ahler-sood-par-repondant.csv` | 32 lignes, perception par parti du repondant, endogroupe et exogroupe |
| `resultats/a46-ahler-sood-controles.csv` | 53 lignes, verification contre les fichiers des auteurs, erreurs agregees, quatre conditions |
| `resultats/a46-composition-gss-2024.csv` | 104 lignes, la realite contemporaine par camp, deux ancrages, IC de Wilson |
| `resultats/a46-appariement.csv` | 15 lignes, l'appariement et ses deux lignes d'absence |
| `resultats/a46-prompts-composition.csv` | 40 lignes, les invites en clair |
| `resultats/a46-trois-termes.csv` | les trois termes poses, une ligne par cellule disponible |
| `resultats/a46-trois-termes-tests.csv` | les tests, par famille, avec Holm et verdict |
| `resultats/a46-couverture.csv` | ce qui est couvert et ce qui manque, item par item |
| `resultats/a46-preenregistrement-composition.md` | la page de plan du run, horodatee avant le premier appel |

Ordre de lancement :

```
.venv/bin/python analyses/a46_ahler_sood.py
.venv/bin/python analyses/a46_appariement.py
.venv/bin/python analyses/a46_prompts_composition.py
.venv/bin/python analyses/a46_run_composition.py --modele q4,oss20,q30 --fin 07:00
.venv/bin/python analyses/a46_trois_termes.py
```

Les trois premieres ont deja tourne et ne font aucun appel de modele. La quatrieme est le
seul appel de modele de tout a46 et attend le matin. La cinquieme se lance avec ou sans
elle, et rend simplement moins de lignes.
