# s1. Ce que le modele fait de la croyance sur autrui : il exagere le biais de chaque camp

Seance du 9 septembre 2026, 12h02 a 13h00. **Aucun appel de modele de langage.** Lecture
seule de fichiers deja presents dans `data/`. Aucun fichier existant du depot n'est modifie ;
tout ce qui est produit ici porte le prefixe `s1`.

Page de plan : `resultats/s1-preenregistrement.md`, horodatee **2026-09-09 12:02:16 CEST**,
ecrite avant tout calcul de statistique de test. Code : `analyses/s1_second_ordre.py`,
lance une fois.

Conventions de certitude : **[MESURE]** calcule ici, **[CONFIRME]** lu dans une source
verifiee, **[PROBABLE]** interpretation etayee, **[HYPOTHESE]** proposition a tester.

---

## Reponse en une ligne

**Le modele ne ressemble ni au vrai public ni a la caricature qu'un camp s'en fait : il
ressemble a cette caricature poussee plus loin. Sur les dix politiques publiques du bloc
« False consensus » de Twin-2K-500, l'ecart entre ce que la gauche et la droite croient du
public vaut 7,5 points chez les humains et de 8,5 a 37,1 points chez les jumeaux numeriques,
soit une amplification mediane de 3,21 fois, avec 11 intervalles sur 12 entierement au dessus
de 1 ; la meme amplification vaut 1,69 fois seulement sur les opinions de premier ordre, si
bien que le modele deforme environ deux fois plus ce qu'un camp croit des autres que ce que
ce camp pense lui meme.** [MESURE]

Et le pari preenregistre le plus couteux a ete gagne contre notre propre corpus : a1, a6,
a20, t2 et a30 etablissent que les modeles **ecrasent** l'heterogeneite, la page de plan a
quand meme preenregistre une amplification superieure a 1, et c'est ce qui sort. Les deux
faits ne se contredisent pas, ils se completent, et la section 4 dit comment.

---

## 1. Ce qui a rendu ce test possible, et ce qu'il a fallu abandonner

### 1.1 L'inventaire du second ordre, honnete

Six pistes ont ete ouvertes, une seule est utilisable **aujourd'hui**.

| source | second ordre ? | cible | realite appariee ? | verdict |
|---|---|---|---|---|
| `ahler-sood-pcomp`, 8 items de composition | oui | un parti | oui | **compositions seulement**, deja traite par a46 et a46b |
| `ahler-sood-pcomp/extremity_exp_data.dta`, `dem_per` et `rep_per` sur `tax`, `abortion`, `gays`, `race` | oui, sur des **opinions** | un parti | **non**, jamais mesuree, et le libelle des enonces est absent | inutilisable |
| `pcomp_igspoll.dta`, l'homologue exact de r1 | oui | un parti | oui, meme enquete | **absent de l'archive Dataverse** |
| `anes-codebooks` | items de placement des partis | un parti | oui | **codebooks seuls, aucune microdonnee** |
| `westwood-pnas-2025` | non | sans objet | sans objet | repondants synthetiques purs, sert a i3 |
| `osf-t6g7k-stanford`, 149 items du GSS | **non, premier ordre** | soi meme | oui | c'est le terrain de r1 et r4 |
| **`twin2k500`, bloc « False consensus », QID287 et QID290** | **oui** | **le public** | **oui, meme enquete, memes 10 enonces, memes 2 058 personnes, deux vagues** | **le seul test faisable** |

[MESURE et CONFIRME]

### 1.2 Le test sur les attitudes des camps du GSS n'est pas faisable, et la raison est nette

Les traces de r1 et de r4 donnent, pour 149 items du GSS, ce que trois modeles locaux disent
de la gauche, du centre et de la droite, a un journaliste ou a un adversaire. **Il n'existe
sur ce disque aucune mesure de ce que la droite croit que la gauche repond a ces items.** La
docstring de `analyses/r1_oracle_camps.py` l'annonce, `resultats/a46-second-ordre-ahler-sood.md`
section 2 l'etablit, et l'inventaire ci dessus le confirme fichier par fichier. La
comparaison a trois termes de r1 reste donc **a deux termes**, realite et modele. [CONFIRME]

Ce que s1 a fait, c'est changer de jeu de donnees pour obtenir les trois termes, et payer ce
changement d'une **cible differente** : ici le modele decrit **le public**, pas le camp
adverse. Aucune phrase de ce rapport ne dit « le modele ressemble a ce que la droite croit de
la gauche ». La forme forte de la question reste ouverte et son protocole est ecrit dans
`resultats/s1-faisabilite.md`.

### 1.3 Deux pieges de nommage, leves

Sur les 31 fichiers de `data/twin2k500/llm/` et `llm_specs/`, il n'y a que **15 contenus
distincts**. Deux d'entre eux ne sont pas ce que leur nom dit :

1. `llm/default_gpt41mini_wave4.csv` **est le fichier humain de la vague 4**, identique
   octet pour octet a `llm_specs/humains_wave4.csv`, et ses QID287 coincident a 100 pour
   cent avec `wave4_response.csv`. Ce n'est pas une sortie de modele. Exclu. [MESURE]
2. `llm/default_gpt41mini_llm.csv` est la configuration « Text Persona GPT4.1-mini », deja
   presente. « default » n'est pas une quatorzieme configuration. [MESURE]

Restent les 13 configurations de `llm_specs/index.json`, dont **une tombe** au critere de
chute 1 : `json_persona_predicted_output__gpt41_mini` a **31,0 pour cent** de valeurs non
numeriques dans le bloc QID290. **12 configurations sont testees.** [MESURE,
`resultats/s1-controles.csv`]

---

## 2. Les quatre termes, mesures

Toutes les valeurs sont en points de pourcentage sur 0 a 100. Ancrage principal :
l'ideologie declaree, `QID22`, repliee en 909 gauche, 582 centre, 567 droite. L'ancrage par
parti donne les memes conclusions et figure dans tous les CSV. [MESURE]

| quantite | gauche | centre | droite | ensemble |
|---|---|---|---|---|
| **realite** : part qui soutient vraiment, QID287 en 4 ou 5 | 76,8 | 64,2 | 50,0 | **65,9** |
| **croyance humaine** : part du public que le camp croit favorable, QID290 | 54,7 | 55,0 | 51,9 | 54,0 |
| **plancher individuel de reinterrogation** : ecart moyen d'une personne a elle meme entre les deux vagues | 14,4 | 15,8 | 16,1 | 15,3 |
| **plancher de groupe** : deplacement de la moyenne du camp entre les deux vagues | 1,27 | 1,62 | 1,09 | |

[MESURE, `resultats/s1-termes-humains.csv`, `s1-controles.csv`]

Le premier fait, qui n'est pas de nous et qui n'est pas le sujet, mais qu'il faut poser :
**les deux camps sous estiment le public d'environ 12 points**, 54,7 et 51,9 contre 65,9. Le
desaccord entre camps, 2,8 points en moyenne de niveau et **7,52 points en moyenne des ecarts
par enonce**, est petit devant cette erreur commune. [MESURE]

Et le modele, incarnant une personne de chaque camp :

| configuration | gauche | droite | ecart |
|---|---|---|---|
| humains | 54,7 | 51,9 | 2,8 |
| `text_persona__gpt41_mini` | 62,6 | **26,7** | 35,9 |
| `text_persona_default_temperature__gpt41_mini` | 62,5 | 28,1 | 34,4 |
| `persona_summary__gpt41_mini` | **71,4** | 38,3 | 33,1 |
| `persona_summary__json_persona__gpt41_mini` | 67,0 | 37,0 | 30,0 |
| `json_persona__gpt41` | 59,5 | 35,3 | 24,2 |
| `text_persona__gemini_flash25` | 54,7 | 47,1 | 7,6 |
| `llm_finetuning_500__gpt41_mini` | 49,1 | 40,6 | 8,5 |
| `demographics_only__gpt41_mini` | 69,1 | 52,1 | 17,0 |

[MESURE, `resultats/s1-par-enonce.csv`, extrait ; les 12 configurations sont dans le CSV]

---

## 3. Le chiffre de tete : l'amplification de l'ecart de perception

`A(m)` est le rapport de l'ecart entre camps chez le modele a l'ecart entre camps chez les
humains, moyenne par enonce, intervalle de bootstrap sur les dix enonces, 10 000 tirages.

| configuration | ecart modele | ecart humain | **A** | IC 95 % | p exacte | p de Holm |
|---|---|---|---|---|---|---|
| `persona_summary__gpt41_mini` | 37,1 | 7,52 | **4,93** | [2,98 ; 7,78] | 0,008 | 0,125 |
| `text_persona__gpt41_mini` | 36,3 | 7,52 | **4,83** | [2,77 ; 7,68] | 0,006 | 0,123 |
| `text_persona_default_temperature__gpt41_mini` | 35,2 | 7,52 | **4,68** | [2,71 ; 7,38] | 0,006 | 0,123 |
| `persona_summary__json_persona__gpt41_mini` | 30,4 | 7,52 | **4,04** | [2,11 ; 6,71] | 0,014 | 0,125 |
| `text_persona_repeating_questions__gpt41_mini` | 26,2 | 7,52 | **3,49** | [2,29 ; 5,26] | 0,006 | 0,123 |
| `json_persona__gpt41` | 25,5 | 7,52 | **3,39** | [1,96 ; 5,53] | 0,008 | 0,125 |
| `text_persona_reasoning__gpt41_mini` | 22,7 | 7,52 | **3,02** | [1,92 ; 4,62] | 0,008 | 0,125 |
| `json_persona__gpt41_mini` | 19,2 | 7,52 | **2,55** | [1,53 ; 3,99] | 0,018 | 0,125 |
| `demographics_only__gpt41_mini` | 18,4 | 7,52 | **2,45** | [1,29 ; 4,06] | 0,035 | 0,141 |
| `text_persona__gemini_flash25` | 15,2 | 7,52 | **2,03** | [1,60 ; 2,82] | 0,002 | **0,047** |
| `json_persona_predicted_output__gpt41` | 14,8 | 7,52 | **1,97** | [1,28 ; 3,02] | 0,021 | 0,125 |
| `llm_finetuning_500__gpt41_mini` | 8,5 | 7,52 | 1,13 | [0,85 ; 1,60] | 0,457 | 0,457 |

[MESURE, `resultats/s1-amplification.csv`, ancrage ideologie ; l'ancrage parti donne 1,26 a
5,56, memes rangs]

**Mediane 3,21. Onze intervalles sur douze sont entierement au dessus de 1.** Une seule
configuration, le modele affine sur 500 exemples, est indistinguable de l'ecart humain.
[MESURE]

**Un seul test survit a Holm**, `text_persona__gemini_flash25` a p corrigee 0,047, et il faut
dire pourquoi plutot que de le maquiller. Avec dix enonces, l'enumeration exacte des 1 024
patrons de signe donne une p minimale de **0,00195** ; Holm sur douze tests exige 0,05 / 12,
soit **0,00417**, pour le plus petit. Seule une configuration qui obtient les dix signes dans
le meme sens peut donc passer. Le plan avait de la puissance a son seuil brut, il n'en a
presque pas apres correction, et **c'est une limite du plan, pas un resultat sur les
modeles**. C'est exactement la lecon de a46 appliquee : la verifier d'avance a permis
d'ecrire un plan qui, lui, pouvait au moins etre significatif avant correction. [MESURE]

Ce qui porte la conclusion n'est donc pas la p, c'est **la convergence de douze intervalles
independants par configuration**, tous du meme cote sauf un. [PROBABLE]

---

## 4. L'ecrasement et l'amplification ne se contredisent pas

Le corpus popsim dit que les modeles ecrasent l'heterogeneite. Ce rapport dit qu'ils
amplifient l'ecart entre camps. Les deux sont vrais parce qu'ils ne portent pas sur la meme
quantite : **l'ecrasement est intra groupe**, il concerne la variete des personnes dans un
camp ; **l'amplification est inter groupe**, elle concerne la distance entre les camps. Un
generateur qui rend tous les gauchers identiques et tous les droitiers identiques, et qui
place les deux blocs loin l'un de l'autre, fait exactement les deux a la fois. [PROBABLE]

La preuve la plus directe est dans la comparaison des deux ordres :

| configuration | amplification **second ordre** | amplification **premier ordre** | rapport |
|---|---|---|---|
| `persona_summary__gpt41_mini` | 4,93 [2,98 ; 7,78] | **0,95** [0,53 ; 1,49] | **5,20** |
| `demographics_only__gpt41_mini` | 2,45 [1,29 ; 4,06] | **0,51** [0,06 ; 1,07] | **4,76** |
| `persona_summary__json_persona__gpt41_mini` | 4,04 [2,11 ; 6,71] | 1,03 [0,56 ; 1,60] | 3,92 |
| `text_persona__gpt41_mini` | 4,83 [2,77 ; 7,68] | 1,82 [1,53 ; 2,20] | 2,65 |
| `llm_finetuning_500__gpt41_mini` | 1,13 [0,85 ; 1,60] | **0,68** [0,52 ; 0,89] | 1,66 |
| `text_persona__gemini_flash25` | 2,03 [1,60 ; 2,82] | 2,20 [1,86 ; 2,76] | 0,92 |

[MESURE, `resultats/s1-amplification-premier-ordre.csv`, bloc declare exploratoire]

Mediane du premier ordre : **1,69**. Mediane du rapport des deux : **1,93**. Et surtout,
**trois configurations ecrasent le premier ordre et amplifient le second** :
`demographics_only` a 0,51 puis 2,45, `persona_summary` a 0,95 puis 4,93,
`llm_finetuning_500` a 0,68 puis 1,13. La meme sortie du meme modele aplatit ce que les gens
pensent et gonfle ce qu'ils croient des autres. [MESURE]

**C'est l'idee, et elle est postable telle quelle** : la deformation ne porte pas sur les
opinions, elle porte sur les **croyances sur autrui**, et elle y est environ deux fois plus
forte. [HYPOTHESE a confirmer sur un second jeu]

---

## 5. Les trois distances demandees, cellule par cellule

Ancrage ideologie, moyennes sur les dix enonces, en points. Le tableau complet avec
intervalles est dans `resultats/s1-cellules.csv`.

| configuration | camp | `D_reel` | `D_endo` | `D_exo` | plancher indiv. |
|---|---|---|---|---|---|
| `text_persona__gpt41_mini` | gauche | **8,5** | 16,2 | 22,2 | 14,4 |
| `text_persona__gpt41_mini` | droite | 39,2 | **25,2** | 28,1 | 16,1 |
| `json_persona__gpt41` | gauche | **6,4** | 10,3 | 16,8 | 14,4 |
| `json_persona__gpt41` | droite | 31,1 | **16,6** | 19,5 | 16,1 |
| `text_persona__gemini_flash25` | gauche | 11,2 | **9,8** | 14,6 | 14,4 |
| `text_persona__gemini_flash25` | droite | 21,7 | **7,0** | 9,5 | 16,1 |
| `demographics_only__gpt41_mini` | gauche | **11,8** | 23,4 | 31,0 | 14,4 |
| `demographics_only__gpt41_mini` | droite | **15,8** | 18,8 | 15,8 | 16,1 |

[MESURE]

**H1, la substitution, est vraie a droite et fausse a gauche.** Le rapport
`D_endo / D_reel` est **inferieur a 1 dans 11 cellules droite sur 12**, de 0,32 a 0,72 : le
modele qui incarne un droitier est plus pres de ce que la droite croit du public que de ce
que le public pense. A gauche, le meme rapport est inferieur a 1 dans **3 cellules sur 12**
seulement : le modele qui incarne un gaucher est le plus souvent plus pres de la realite.
**Aucun de ces 24 tests ne survit a Holm** ; la plus petite p corrigee vaut 0,094. La
direction est nette et systematique, la significativite apres correction n'y est pas.
[MESURE, `resultats/s1-tests.csv`, famille F1]

**H3, la lentille de gauche, est refutee.** Le modele n'est pas systematiquement plus pres de
la caricature de gauche. Il est plus pres de la caricature **du camp qu'on lui dit d'etre** :
`d_gauche / d_droite` vaut 0,55 a 0,80 dans les cellules gauche, et **1,03 a 1,35 dans
10 cellules droite sur 12**. Il n'y a pas de lentille unique, il y a une obeissance a
l'etiquette, deja etablie par r3 sous une autre forme. [MESURE, famille F3]

**H4, le plancher, est vrai a droite seulement.** `D_reel / plancher individuel` vaut 1,31 a
2,43 dans 11 cellules droite sur 12, et reste sous 1 dans 9 cellules gauche sur 12. Aucun
test ne survit a Holm. [MESURE, famille F4]

### La lecture qui tient les trois ensemble

Le modele **exagere le biais directionnel de chaque camp**. Les humains de droite croient le
public moins favorable qu'il n'est, 51,9 contre 65,9 ; le modele incarnant un droitier
descend a 26,7 a 52,1, **plus bas encore que la caricature de droite**. Les humains de gauche
croient le public un peu plus favorable que ne le croit la droite ; le modele incarnant un
gaucher monte a 49,1 a 71,4, **plus haut que la caricature de gauche**. A gauche, exagerer le
biais rapproche par accident de la realite, parce que la realite est du meme cote. A droite,
exagerer le biais eloigne de tout. **Le modele n'est pas un correcteur a gauche, il est un
exagerateur qui a de la chance.** [PROBABLE]

---

## 6. Le critere de chute 5 s'est declenche, et il etait mal ecrit

La section 7 de la page de plan disait : si le plancher de reinterrogation depasse l'ecart
entre camps, la question n'a pas de resolution et le rapport s'arrete. **Il se declenche** :
plancher individuel 15,3 points, ecart humain entre camps 7,52 points. [MESURE]

Il faut donc dire deux choses, dans cet ordre.

**D'abord, tel qu'il est ecrit, le critere est declenche.** Cela est publie, ce n'est pas
efface, et tout lecteur peut s'arreter la.

**Ensuite, le critere compare deux quantites qui ne sont pas commensurables**, et c'est une
faute de la page de plan, pas des donnees. Le plancher individuel est la dispersion d'**une
personne** ; les quantites testees par H1, H3 et H4 sont des **moyennes de camp** de 567 a
909 personnes, dont la dispersion vaut environ le plancher divise par la racine de
l'effectif. La version de groupe du meme plancher, le deplacement de la moyenne du camp entre
les deux vagues, vaut **1,27 point a gauche et 1,09 a droite**, contre un ecart entre camps de
**7,52 points** : la resolution est d'un facteur 5 a 7, et le bootstrap sur les personnes le
confirme, gauche 54,73 [53,91 ; 55,59] contre droite 51,93 [50,81 ; 53,06], intervalles
disjoints. [MESURE, bloc `exploratoire, plancher de groupe` de `s1-controles.csv`]

Ce bloc de groupe a ete **ajoute apres avoir vu le critere se declencher**. C'est du post hoc,
c'est ecrit comme tel, et il est etiquete exploratoire dans le CSV comme dans le code. Il ne
sert a aucun test et ne change aucune p. La correction a apporter a toute page de plan
future : **un critere de resolution doit porter sur le bruit de la quantite reellement
testee**, jamais sur le bruit individuel quand la quantite testee est une moyenne de groupe.
[PROBABLE]

---

## 7. Ce que ce rapport ne dit pas

- **Rien sur les 149 items du GSS.** r1 et r4 gardent leurs deux termes. Aucune phrase de s1
  ne porte sur eux.
- **Rien sur ce qu'un camp croit d'un autre camp.** La cible mesuree est « le public ».
- **Rien sur les Etats Unis.** Twin-2K-500 n'est pas un echantillon pondere. `R(j)` est la
  realite de ces 2 058 personnes.
- **Rien de causal.** Ce que lire une reponse de modele fait a un lecteur n'est pas teste ici.
- **Rien sur nos modeles locaux.** Les 12 configurations sont celles des auteurs de
  Twin-2K-500, gpt-4.1, gpt-4.1-mini et gemini-flash-2.5. Aucun appel n'a ete fait par nous,
  ni a eux ni a un modele local.
- **Rien de significatif apres Holm**, sauf une amplification sur douze.

---

## Ce que je n'ai pas pu verifier

1. **Que les 12 fichiers de simulation correspondent aux 12 libelles de `index.json`.** La
   verification est une concordance entre deux dossiers telecharges par deux scripts
   differents, plus les deux anomalies de la section 1.3. Elle ne reinterroge pas le depot
   Hugging Face.
2. **Le contexte exact dans lequel les jumeaux ont vu QID290.** Le protocole des auteurs n'a
   pas ete relu ; s'ils ont montre au modele les reponses de la personne a QID287 juste avant,
   l'ecart de second ordre porte en partie ce voisinage.
3. **Le sens de la modalite 3 de QID287**, comptee comme non soutien. Au seuil large, 3 a 5,
   la realite passe de 65,9 a 81,8 points, ce qui deplace `D_reel` mais **pas** `A(m)`, qui
   ne fait intervenir que des ecarts entre camps. Le controle est dans `s1-controles.csv`,
   la reprise complete des tests sous ce seuil n'est pas faite.
4. **Ce que « le public » veut dire** pour un repondant et pour un modele. Le libelle ne le
   precise pas ; si le modele entend « les gens comme moi », l'amplification mesuree est en
   partie un artefact de lecture de la question.
5. **Que le bloc « False consensus » ait ete pose dans le meme ordre et le meme contexte aux
   deux vagues.** Le plancher de reinterrogation en depend.
6. **Si la meme amplification tient hors des Etats Unis, hors de l'anglais, et sur d'autres
   enonces que ces dix, tous de politique publique federale.** Les dix enonces sont
   fortement orientes, huit sur dix sont des politiques de gauche.

## Questions ouvertes pour Simon

1. L'amplification de l'ecart de perception, mediane 3,21, est elle le bon chiffre de tete,
   ou preferez vous le rapport second ordre sur premier ordre, mediane 1,93, qui est le plus
   nouveau mais le moins direct ?
2. Le critere de chute 5 mal specifie doit il faire l'objet d'un errata dans les pages de
   plan deja publiees, r1, r4, a42, a43 et a44, qui emploient toutes un plancher humain ?
   **Je ne les ai pas relues** dans cette seance : je ne sais donc pas si l'une d'elles
   compare, comme la mienne, un plancher individuel a un contraste de groupe.
3. Huit des dix enonces sont des politiques de gauche. Faut il refaire le test sur un
   sous ensemble equilibre, quitte a tomber a quatre enonces et a perdre toute puissance,
   ou publier l'asymetrie du questionnaire comme une limite ?
4. Connaissez vous un jeu public ou des repondants estiment la position **d'un camp** sur des
   opinions, avec la realite dans la meme enquete ? L'IGS Poll d'Ahler et Sood est le seul
   que nous ayons identifie et il n'est pas dans l'archive.
5. `A(m)` varie de 1,13 a 4,93 selon la seule facon de presenter la persona au modele, a
   modele constant. Faut il en faire un resultat a part entiere, dans la ligne de r4 sur le
   format d'invite, plutot qu'un tableau de robustesse ?
