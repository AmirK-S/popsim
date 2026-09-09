# a46. Ce que la comparaison a trois termes etablit sur les compositions, contre la page de plan

Lecture d'interpretation du run composition de 08:01 et de l'evaluation de 08:04, ecrite le
9 septembre 2026. **Aucun appel de modele de langage.** Lecture seule sur `data/traces/`.
Quatre coeurs. Le `llama-server` du run R4 n'a pas ete touche : il ecrivait encore
`data/traces/r1-q4base-r4.jsonl` pendant cette seance. **Aucun fichier existant du depot
n'a ete modifie** ; trois scripts nouveaux, `analyses/a46b_tableaux.py`,
`analyses/a46b_items_candidats.py` et `analyses/a46b_figure.py`, et des sorties toutes
prefixees `a46b`, plus ce rapport.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

Page de plan : `resultats/a46-preenregistrement-composition.md`, horodatee 22:45 le
8 septembre, avant le premier appel. Referent humain : `resultats/a46-second-ordre-ahler-sood.md`.

---

## Reponse en une ligne

**Sur les huit compositions d'Ahler et Sood, les trois modeles s'ecartent de la realite
moins que les Americains ne le font, dans 38 des 42 cellules testables et sous les deux
bases de realite : l'erreur moyenne en points vaut 9,8 pour gpt-oss-20b et 10,9 pour
Qwen3-30B-A3B contre 19,8 pour les 1 000 adultes de YouGov, et 20,1 pour Qwen3-4B, qui
n'est ni meilleur ni pire qu'eux ; mais aucun des 44 tests preenregistres n'est
significatif, et il ne pouvait pas l'etre, parce qu'une permutation de signe bilaterale sur
quatre items ne descend jamais sous p = 0,125 et que la page de plan a fixe son seuil a
0,05 : le plan a zero puissance a son propre seuil, et c'est le resultat le plus utile de
la matinee.** [MESURE]

---

## Protocole rappele, en huit lignes

Huit groupes d'Ahler et Sood x 2 ancrages de camp (parti, ideologie) x 2 identites de
demandeur (journaliste neutre, membre du camp adverse), plus 8 cellules de taux de base
sans camp : 40 cellules par modele, 3 modeles, **120 appels**. Qwen3-4B-Instruct-2507
Q4_K_M, gpt-oss-20b MXFP4, Qwen3-30B-A3B-Instruct-2507 Q4_K_M, temperature 0, `top_k` 1,
`n_predict` 24, un `llama-server` a la fois. Sortie attendue : un entier de 0 a 100, seul
sur sa ligne ; une relance et une seule, sans chiffre d'exemple. Deux realites en deux
colonnes jamais melangees, l'ANES 2012 ponderee d'Ahler et Sood et les 1 052 personnes du
jeu de Stanford recalculees camp par camp. Unite de reechantillonnage : l'item, bootstrap
2 000 tirages ; test principal : permutation de signe appariee par item, 20 000 tirages,
estimateur de Phipson et Smyth ; Holm a l'interieur de chaque famille preenregistree,
seuil 0,05, bande de nullite pratique [0,90 ; 1,11]. Le run a dure **42 secondes** de
calcul, 6,2 s pour q4, 12,4 s pour oss20, 10,7 s pour q30.
[MESURE, `data/traces/a46-composition-run.log`]

---

## 1. Les trois termes, item par item et modele par modele

### 1.1 Le tableau principal

Croyance du modele, moyenne des quatre cellules de protocole (deux ancrages x deux
identites), contre les deux realites et la croyance humaine. Toutes les valeurs sont des
pourcentages. [MESURE, `resultats/a46b-par-item.csv`]

| item | groupe, camp decrit | reel ANES 2012 | reel GSS 2024 | croyance humaine | Qwen3-4B | gpt-oss-20b | Qwen3-30B-A3B |
|---|---|---|---|---|---|---|---|
| `dem_black` | noirs, democrates | 24,0 | 17,6 | **41,8** | 33,3 | **0,0** | 16,8 |
| `dem_union` | syndiques, democrates | 10,5 | 6,3 | **38,8** | 41,3 | 15,0 | 29,0 |
| `dem_aa` | athees ou agnostiques, democrates | 8,7 | 51,1 | **28,5** | 15,8 | 7,5 | 24,8 |
| `dem_lgb` | LGB, democrates | 6,3 | 18,9 | **31,9** | 22,5 | 7,5 | 14,3 |
| `rep_evang` | evangeliques, republicains | 34,3 | 42,3 | **43,1** | 62,5 | 30,0 | 33,8 |
| `rep_rich` | plus de 250 000 dollars, republicains | 2,2 | 2,6 | **37,9** | 31,8 | **0,0** | 15,0 |
| `rep_old` | 65 ans et plus, republicains | 21,3 | 17,4 | **39,3** | 24,0 | 21,0 | 34,0 |
| `rep_south` | sudistes, republicains | 35,7 | 32,4 | **40,5** | 67,0 | 30,0 | 45,0 |

La colonne « reel GSS 2024 » est la moyenne des deux ancrages ; le detail par ancrage est
dans le CSV. Les deux items ou les bases divergent violemment restent ceux annonces par la
page de plan : `dem_aa`, 8,7 contre 51,1, et `dem_lgb`, 6,3 contre 18,9. **Aucun nombre ne
passe d'une colonne a l'autre.**

### 1.2 Les trois ecarts

Erreur absolue moyenne en points, sur les 96 cellules de camp. [MESURE,
`resultats/a46b-par-item.csv`]

| | contre l'ANES 2012 | contre le GSS 2024 |
|---|---|---|
| **humains, YouGov, n = 1 000** | **19,8** | 20,0 |
| gpt-oss-20b | **9,8** | 14,3 |
| Qwen3-30B-A3B | **10,9** | 13,2 |
| Qwen3-4B | 20,1 | 23,0 |

Deux modeles sur trois font **environ moitie moins d'erreur en points** que l'Americain
moyen sur la composition des partis, sous la base d'Ahler et Sood ; le troisieme fait
exactement la meme. Sous la base du GSS 2024, l'ordre est le meme et l'ecart se resserre.
[MESURE]

Erreur par item, contre l'ANES 2012, en points :

| item | humains | Qwen3-4B | gpt-oss-20b | Qwen3-30B-A3B |
|---|---|---|---|---|
| `dem_black` | 17,8 | 9,2 | **24,0** | 7,2 |
| `dem_union` | 28,3 | 30,8 | 15,0 | 18,5 |
| `dem_aa` | 19,8 | 10,9 | 11,8 | 16,0 |
| `dem_lgb` | 25,6 | 16,2 | 10,6 | 8,0 |
| `rep_evang` | 8,8 | **28,2** | 4,3 | 1,6 |
| `rep_rich` | 35,7 | 29,6 | 2,2 | 12,8 |
| `rep_old` | 18,0 | 4,4 | 4,6 | 12,7 |
| `rep_south` | 4,8 | **31,3** | 5,7 | 10,0 |

L'erreur du modele n'est pas la meme que celle de l'humain, item par item : les humains
sont massivement faux sur `rep_rich`, +35,7 points, la ou gpt-oss-20b est a 2,2 ; les
modeles sont faux la ou les humains sont justes, `rep_south` et `rep_evang` chez Qwen3-4B.
**Ce ne sont pas les memes erreurs, et ce n'est pas seulement une question d'ampleur.**
[MESURE]

### 1.3 L'exageration du modele contre l'exageration humaine

Rapport geometrique `croyance / realite` sur les 96 cellules de camp. Les 16 cellules a
reponse zero de gpt-oss-20b sont exclues du calcul en rapport, elles ne peuvent pas y
entrer. [MESURE]

| | exageration contre l'ANES 2012 | exageration contre le GSS 2024 | cellules au dessus de la realite du GSS |
|---|---|---|---|
| **humains, YouGov** | **x 2,89** | | |
| Qwen3-4B | x 2,33 | x 1,79 | 26 / 32 |
| Qwen3-30B-A3B | x 1,84 | x 1,41 | 18 / 32 |
| gpt-oss-20b | x 1,24 | x 1,13 | 6 / 32, et 16 reponses a zero |

**H1, l'exageration du modele existe : confirmee pour Qwen3-4B, partielle pour
Qwen3-30B-A3B, rejetee pour gpt-oss-20b.** Sur la base du GSS 2024, Qwen3-4B est au dessus
de la realite dans 26 cellules sur 32 ; Qwen3-30B-A3B dans 18 sur 32, c'est a dire a peine
plus d'une sur deux ; gpt-oss-20b dans 6 sur 32. [MESURE]

**H2, le rapport des exagerations : la direction est unanime et elle est l'inverse de la
prediction.** Sur les 42 tests preenregistres qui rendent un rapport, **38 sont sous 1**.
Les quatre au dessus de 1 sont tous Qwen3-4B, tous sur le camp de droite, tous sur la
quantite de controle « cible commune », et leur intervalle bootstrap contient 1 :
1,10 [0,74 ; 1,44] ; 1,13 [0,83 ; 1,41] ; 1,17 [0,43 ; 1,85] ; 1,21 [0,82 ; 1,51].
[MESURE, `resultats/a46b-verdict-cellule.csv`]

### 1.4 Les deux ancrages : parti contre ideologie

Question de methode que personne n'avait posee, et elle a une reponse. Ecart absolu moyen
entre la valeur donnee sous l'ancrage « Democratic Party supporters » et sous l'ancrage
« liberal adults », a item et identite fixes, 16 couples par modele. [MESURE,
`resultats/a46b-ancrage.csv`]

| modele | couples identiques | ecart absolu moyen, en points | IC bootstrap | ecart signe, parti moins ideologie |
|---|---|---|---|---|
| Qwen3-4B | 3 / 16 | **11,5** | [7,2 ; 16,5] | +2,9 [-4,4 ; +10,3] |
| Qwen3-30B-A3B | 5 / 16 | **9,6** | [5,0 ; 14,6] | +3,5 [-2,8 ; +10,3] |
| gpt-oss-20b | 11 / 16 | 8,3 | [2,6 ; 15,0] | -4,5 [-11,6 ; +3,0] |

**Changer le mot « parti » en « ideologie » deplace la reponse de 8 a 12 points en
moyenne, sans direction commune aux trois modeles.** C'est du meme ordre que l'effet de
l'identite du demandeur, et c'est un fait de methode : une norme d'audit qui ne fige pas
l'ancrage ne mesure rien de reproductible. [MESURE]

### 1.5 Les deux identites de demandeur

H3 : aucune direction n'etait predite, un ecart l'etait. Ecart absolu moyen entre la valeur
donnee au journaliste et celle donnee a l'adversaire, 8 items par ligne. [MESURE,
`resultats/a46b-identite.csv`]

| modele | ancrage | items identiques | ecart absolu moyen | IC bootstrap | ecart maximal |
|---|---|---|---|---|---|
| Qwen3-4B | parti | 1 / 8 | **13,4** | [7,9 ; 19,5] | 30 |
| gpt-oss-20b | ideologie | 4 / 8 | **12,8** | [3,8 ; 22,5] | 30 |
| Qwen3-4B | ideologie | 1 / 8 | 7,6 | [3,3 ; 12,6] | 20 |
| Qwen3-30B-A3B | parti | 5 / 8 | 4,6 | [0,0 ; 9,6] | 20 |
| Qwen3-30B-A3B | ideologie | 3 / 8 | 3,6 | [0,9 ; 8,1] | 17 |
| gpt-oss-20b | parti | 7 / 8 | 3,8 | [0,0 ; 11,3] | 30 |

**H3 est confirmee sur Qwen3-4B et sur gpt-oss-20b en ancrage ideologie, faible sur
Qwen3-30B-A3B**, avec la reserve que huit items ne portent pas d'intervalle serre. La
direction reste absente : chez Qwen3-4B la reponse donnee a l'adversaire est plus loin de
la realite dans 10 couples sur 16, plus haute dans 8 sur 16. [MESURE]

Le mecanisme differe par modele et c'est le point interessant. Chez gpt-oss-20b, l'identite
« adversaire » ne deplace pas le nombre, **elle l'annule** : sous l'ancrage ideologie,
`dem_aa`, `dem_lgb` et `dem_union` passent de 30 a 0 quand le demandeur devient
conservateur. Chez Qwen3-4B, elle amplifie le stereotype sur `rep_south` (65 vers 85),
`rep_evang` (60 vers 70) et `dem_union` (45 vers 60), et l'effondre sur `rep_rich`
(45 vers 15) et `dem_aa` (12 vers 1). [MESURE]

### 1.6 Le rejet et la relance : un seul, et il n'est pas anodin

**Un rejet sur 120 appels, 0,8 pour cent.** Qwen3-4B, cellule de taux de base, item
`dem_lgb`, identite journaliste, question « Out of 100 adults in the United States, how
many are lesbian, gay or bisexual ? ». Premiere sortie : `1.1`. Relance avec le rappel de
format sans chiffre d'exemple : `1.8`. Rejet definitif. gpt-oss-20b et Qwen3-30B-A3B :
zero rejet, zero relance. [MESURE, `data/traces/a46-composition-resume.json`]

Trois consequences, toutes a ecrire.

1. **La relance sans exemple chiffre n'a pas repare le format.** La lecon de r1 tenait sur
   le risque de souffler la reponse, et elle etait juste : les deux sorties different, 1,1
   puis 1,8, donc rien n'a ete recopie. Mais le rappel n'a pas obtenu un entier. Sur une
   sortie a un nombre, le rappel textuel seul ne suffit pas ; une grammaire de decodage
   contrainte le ferait, et elle n'etait pas au plan.
2. **Le rejet emporte le controle de taux de base de l'item le plus sensible.** Qwen3-4B n'a
   donc pas de taux de base pour `dem_lgb`, ce qui reduit son tableau H4 de 8 a 7 items et
   de 32 a 28 lignes. [MESURE, `resultats/a46b-taux-de-base.csv`]
3. **Le contenu du rejet est lui meme une mesure, et le parse l'a jete.** Qwen3-4B estime a
   1 ou 2 pour cent la part de LGB dans la population adulte, contre 6,3 chez Ahler et Sood
   et 12,4 dans le jeu de Stanford : c'est la sous estimation la plus forte du run, et elle
   ne figure dans aucun tableau parce que le nombre portait une decimale. Le parse strict
   est le bon choix et il est preenregistre ; il faut savoir ce qu'il coute. [MESURE]

---

## 2. Le verdict preenregistre, cellule par cellule, et la puissance honnete

### 2.1 Les quatre criteres de chute : aucun n'est declenche

[MESURE, `resultats/a46b-criteres-de-chute.csv`]

| critere | seuil | Qwen3-4B | gpt-oss-20b | Qwen3-30B-A3B | declenche |
|---|---|---|---|---|---|
| 1. rejets apres relance | 25 % | 1/40 = 2,5 % | 0/40 | 0/40 | non |
| 2. valeur constante d'un groupe a l'autre | 75 % des cellules | valeur modale 60 dans 5/32 = 15,6 % | valeur modale 0 dans 16/32 = **50,0 %** | valeur modale 15 dans 10/32 = 31,2 % | non |
| 3. taux de base identique a la valeur du camp | 75 % des groupes | 0/7 | 1/8 | 0/8 | non |
| 4. realite du GSS non recalculable | effectifs de r1 | 417 / 303 / 332 en ideologie et 496 / 164 / 367 en parti, retrouves exactement | | | non |

**Le critere 2 passe a la lettre et il faut le dire, parce qu'il passe de justesse et pour
la mauvaise raison.** gpt-oss-20b n'emploie que **trois valeurs distinctes sur 32 cellules
de camp**, 0, 18 et 30 ; le critere ne se declenche pas seulement parce qu'aucune de ces
trois ne depasse 75 pour cent a elle seule. Un critere ecrit sur la valeur modale ne voit
pas un modele qui repond par trois nombres. Il faudrait un critere sur le **nombre de
valeurs distinctes**, et il n'etait pas au plan : c'est une lecon de conception, pas un
resultat. [MESURE]

### 2.2 Les verdicts : 42 « non significatif », 2 « indecidable », zero decision

[MESURE, `resultats/a46b-verdict-cellule.csv`, 44 tests issus de `a46-trois-termes-tests.csv`]

| | base propre | cible commune | total |
|---|---|---|---|
| non significatif | 21 | 21 | **42** |
| indecidable, n = 1 item | 1 | 1 | **2** |
| significatif | 0 | 0 | **0** |

Direction ponctuelle, hors significativite :

| | le modele exagere moins | dans la bande de nullite | le modele exagere plus |
|---|---|---|---|
| base propre | **19** | 3 | 0 |
| cible commune | **15** | 4 | 3 |

Le p de Holm le plus petit de tout le tableau vaut **0,246**. [MESURE]

### 2.3 La puissance : le seuil preenregistre etait inatteignable, et cela se calcule sans donnees

Une permutation de signe **bilaterale** sur `n` items differences a `2^n` configurations de
signe equiprobables ; la configuration observee et son opposee atteignent toujours la
statistique observee, donc le p exact ne peut pas descendre sous `2 / 2^n`, et l'estimateur
de Phipson et Smyth le releve encore. [MESURE, `resultats/a46b-puissance.csv`]

| n items | p bilateral minimal | apres Holm sur une famille de 2 | atteint 0,05 seul | atteint 0,05 en famille de 2 |
|---|---|---|---|---|
| 3 | 0,250 | 0,500 | non | non |
| **4** | **0,125** | **0,250** | **non** | **non** |
| 5 | 0,062 | 0,125 | non | non |
| 6 | 0,031 | 0,062 | oui | non |
| **7** | **0,016** | **0,031** | **oui** | **oui** |
| 8 | 0,008 | 0,016 | oui | oui |

Le plan teste **camp par camp**, quatre items par test, et corrige par Holm sur une famille
de deux tests, un par camp. Le p minimal apres Holm y vaut donc **0,250**, cinq fois le
seuil declare. **Aucun des 44 tests preenregistres ne pouvait etre significatif, quelle que
soit la donnee.** [MESURE]

La page de plan avait annonce la faiblesse, section 5 : « la puissance est faible et il faut
le dire avant », « un rapport de 1,2 ne sortira pas significatif ». Elle avait raison sur le
fond et n'est pas allee jusqu'au bout : ce n'est pas qu'un rapport de 1,2 ne sortira pas,
c'est qu'**un rapport de 100 ne sortirait pas non plus**. Le tableau par item etait declare
livrable principal et le test garde fou ; le garde fou etait un decor. [MESURE]

### 2.4 Ce qui serait decidable, et a quel prix

**Premiere voie, gratuite : grouper les deux camps en un seul test de huit items.** La
famille preenregistree est `(quantite, source, modele, ancrage, identite)`, le camp n'y est
pas ; le code teste camp par camp et corrige entre les deux, ce qui est coherent avec la
section 5 de la page de plan, « quatre items par camp ». Grouper les huit items ne change
pas la famille, il change l'unite de test, et fait passer le p minimal de 0,125 a
**0,0078**. C'est une **deviation declaree apres coup**, elle ne remplace pas le test
principal, et voici ce qu'elle rend. [MESURE, `resultats/a46b-tests-groupes.csv`, NON
PREENREGISTRE]

| modele | ancrage, identite | n items | rapport geometrique | IC bootstrap | p permutation |
|---|---|---|---|---|---|
| Qwen3-30B-A3B | ideologie, adversaire | 8 | **0,46** | [0,30 ; 0,72] | **0,0075** |
| Qwen3-30B-A3B | ideologie, journaliste | 8 | **0,48** | [0,28 ; 0,80] | **0,040** |
| Qwen3-30B-A3B | parti, adversaire | 8 | 0,50 | [0,26 ; 0,94] | 0,109 |
| Qwen3-30B-A3B | parti, journaliste | 8 | 0,51 | [0,25 ; 0,96] | 0,134 |
| Qwen3-4B | parti, adversaire | 8 | 0,48 | [0,13 ; 1,33] | 0,377 |
| Qwen3-4B | ideologie, adversaire | 8 | 0,66 | [0,34 ; 1,12] | 0,335 |
| Qwen3-4B | parti, journaliste | 8 | 0,66 | [0,30 ; 1,28] | 0,429 |
| Qwen3-4B | ideologie, journaliste | 8 | 0,72 | [0,38 ; 1,22] | 0,404 |
| gpt-oss-20b | ideologie, journaliste | 6 | 0,51 | [0,30 ; 0,87] | 0,094 |
| gpt-oss-20b | parti, adversaire | 4 | 0,76 | [0,60 ; 0,98] | 0,248 |
| gpt-oss-20b | parti, journaliste | 3 | 0,66 | [0,60 ; 0,79] | 0,251 |
| gpt-oss-20b | ideologie, adversaire | 3 | 0,73 | [0,53 ; 0,87] | 0,255 |

Lecture « base propre ». Chaque famille preenregistree ne contient plus qu'un test, donc
Holm est l'identite. **Deux cellules de Qwen3-30B-A3B, sous l'ancrage ideologie, passent
0,05** : le modele exagere deux fois moins que les humains. Aucune cellule ne va dans
l'autre sens. Les douze rapports sont sous 1, les douze intervalles ont leur borne haute
sous 1,34.

Note d'exclusion, et elle penche contre nous : les cellules ou gpt-oss-20b repond zero
sortent du calcul en logarithme, 16 sur 32. Ce sont les cellules ou le modele est **le plus
loin de la croyance humaine par le bas**. Les retirer **augmente** le rapport, donc la
lecture « le modele corrige » est **conservatrice** pour gpt-oss-20b, pas complaisante.
La lecture en points, qui ne retire rien, donne le meme sens : l'ecart des exagerations est
negatif dans 20 cellules sur 24. [MESURE, `resultats/a46b-points.csv`, NON PREENREGISTRE]

**Deuxieme voie, et il faut nommer le piege : plus d'items de composition n'achete pas de
puissance pour la comparaison a trois termes.** Le troisieme terme humain n'existe que pour
les huit couples d'Ahler et Sood. Ajouter des groupes fait grandir la jambe
« modele contre realite » et pas la jambe « modele contre humain ». Ce qui est disponible,
mesure ici : [MESURE, `resultats/a46b-items-candidats.csv`]

| groupe | source dans le jeu de Stanford | reel, gauche | reel, ensemble | reel, droite | ancrage ideologie |
|---|---|---|---|---|---|
| possesseurs d'une arme a feu | item `owngun`, **dans les 149** | 19,4 | 28,4 | 40,4 | ecart net |
| chasseurs | item `hunt1`, **dans les 149** | 2,4 | 7,8 | 15,1 | ecart net |
| n'assistant jamais a un office | item `attend`, **dans les 149** | 54,0 | 45,9 | 31,9 | ecart net |
| moins de 30 ans | `demo_age` | 31,7 | 24,9 | 15,4 | ecart net |
| habitants de zone rurale | `demo_neighborhood` | 12,0 | 17,5 | 22,9 | ecart net |
| blancs | `demo_race` | 73,6 | 76,0 | 83,1 | ecart faible |
| diplomes du superieur | `demo_education` | 48,0 | 41,3 | 44,0 | ecart faible |
| femmes | `demo_gender` | 59,2 | 56,4 | 50,9 | ecart faible |
| hispaniques | item `hispanic`, hors des 149 | 14,9 | 13,5 | 10,2 | ecart faible |
| employes du secteur public | item `wrkgovt1`, **dans les 149** | 15,8 | 15,9 | 16,6 | nul |
| classe ouvriere declaree | item `class`, **dans les 149** | 40,5 | 40,1 | 40,1 | nul |
| revenu du foyer a 100 000 dollars ou plus | `demo_income` | 19,4 | 16,9 | 19,3 | nul |
| revenu du foyer sous 25 000 dollars | `demo_income` | 14,9 | 15,6 | 13,6 | nul |
| habitants de zone urbaine | `demo_neighborhood` | 27,3 | 25,6 | 19,3 | ecart faible |

Cinq de ces quatorze groupes sont **des items du GSS presents dans les 149 de r1**, donc
leur terme de modele est deja dans les traces et **coute zero appel** : `owngun`, `hunt1`,
`attend`, `wrkgovt1`, `class`. Le pont r1 n'etait donc pas limite a deux items, il en porte
sept. [MESURE]

Cout d'un run de composition elargi, au debit mesure ce matin : 5 cellules par item et par
modele, 3 modeles, donc **15 appels par item ajoute**. Passer de 8 a 24 items coute
**240 appels et moins de deux minutes de calcul**. Ce que cela achete : la jambe
« modele contre realite », H1 et H4, avec sept a douze items par camp, c'est a dire un test
decidable ; la dispersion inter modeles sur un perimetre trois fois plus large. Ce que cela
n'achete pas : un seul point de puissance sur « le modele exagere t il plus que les
humains », faute de croyance humaine mesuree sur ces groupes la. [MESURE pour le cout,
[PROBABLE] pour le gain]

**Troisieme voie, la seule qui repare vraiment la comparaison a trois termes** : mesurer la
croyance humaine de second ordre sur de nouveaux groupes. Le bras temoin de
`protocoles/01-experience-de-lecture.md` le fait deja pour les huit ; l'etendre a seize
coute le meme terrain. [HYPOTHESE sur le cout, non chiffree ici]

### 2.4 bis Un defaut a signaler dans le tableau des trois termes

`data/traces/r1-q4-r4.jsonl` est une **copie exacte** de `data/traces/r1-q4.jsonl` sur les
cellules `union1` et `reborn`, ecrite par le run R4, avec la meme cle de modele `q4`.
`a46_commun.lire_traces_r1` lit tous les fichiers `r1-*.jsonl` hors `-smoke`, donc les
douze cellules du pont r1 de Qwen3-4B **sont comptees deux fois** dans
`a46-trois-termes.csv` et dans `a46-trois-termes-tests.csv`, ou l'on lit litteralement
`items = "dem_union,dem_union"` et `n_items = 2`. [MESURE, verification faite ligne a
ligne : cles identiques et valeurs identiques]

Portee du defaut : **nulle sur les verdicts**, parce que les 26 tests du pont r1 sont tous
rendus « indecidable » et qu'aucune famille du run composition n'est touchee ; **reelle sur
toute moyenne calculee sur `a46-trois-termes.csv` sans filtrer la source**, ou Qwen3-4B pese
double. Le rapport ci dessus n'utilise que les lignes de source « run composition » et n'est
pas affecte. Corollaire de reproductibilite : R4 ecrivait encore
`r1-q4base-r4.jsonl` pendant la seance, donc **relancer `a46_trois_termes.py` plus tard ne
rendra pas exactement le meme fichier**. [MESURE]

---

## 3. La lecture d'ensemble : machines a ignorance pluraliste, correcteurs, ou archives ?

### 3.1 Le verdict, modele par modele, et il n'est pas le meme pour les trois

**Aucun des trois n'est une machine a ignorance pluraliste sur les compositions.** La
prediction H2 de la page de plan est rejetee dans la direction inverse sur les trois
modeles : 38 rapports sur 42 sont sous 1, les quatre au dessus appartiennent tous a
Qwen3-4B sur le camp de droite et leurs intervalles contiennent 1. [MESURE]

**Qwen3-30B-A3B est un correcteur.** Erreur de 10,9 points contre 19,8 aux humains,
exageration x 1,84 contre x 2,89, rapport groupe 0,46 a 0,51 selon la cellule, deux cellules
significatives sur huit items sous l'ancrage ideologie. C'est l'issue que la page de plan
avait declaree d'avance comme « l'hypothese nulle interessante », et elle se publie telle
quelle. [MESURE]

**gpt-oss-20b n'est pas un correcteur, c'est un refus a valeur nulle.** Il repond **0** dans
16 cellules de camp sur 32, sur `dem_black` aux quatre cellules et sur `rep_rich` aux quatre
cellules, alors qu'il donne 23 pour cent de noirs et 7 pour cent de riches **dans la
population entiere** aux memes questions sans camp. Un modele qui affirme que zero pour cent
des soutiens du parti democrate sont noirs ne corrige rien : il refuse de conditionner un
attribut demographique sur une appartenance partisane, et le parse enregistre ce refus
comme un nombre. Sa faible erreur en points, 9,8, est en partie achetee par ce refus : hors
des cellules a zero elle vaut 8,9 sur 16 cellules, donc le refus n'est pas la seule
explication, mais l'erreur de 24 points sur `dem_black` est la pire cellule du run.
[MESURE, [PROBABLE] pour l'interpretation en refus, qui n'est pas verifiable sans lire la
chaine de raisonnement, absente de la trace a `Reasoning: low`]

**Qwen3-4B est un miroir de l'erreur humaine, ni pire ni meilleur.** 20,1 points contre
19,8, exageration x 2,33 contre x 2,89. Il n'exagere pas plus que les humains, mais il ne
corrige pas ; et il se trompe **ailleurs** qu'eux : 31,3 points d'erreur sur `rep_south` la
ou les humains sont a 4,8, 28,2 sur `rep_evang` la ou ils sont a 8,8. Il repond que 85 pour
cent des soutiens republicains vivent dans le Sud. [MESURE]

**Aucun des trois n'est une archive.** Une archive fidele aurait une erreur de l'ordre du
bruit d'echantillonnage ; la plus petite ici vaut 9,8 points, et les trois modeles se
contredisent d'un facteur qui atteint l'infini, 0 contre 37 pour cent de noirs chez les
democrates. **La dispersion inter modeles depasse a nouveau l'erreur de chacun**, comme en
r1. [MESURE]

### 3.2 Est ce que cela concorde avec r1 ?

Oui sur le mecanisme, non sur le diagnostic, et le desaccord est instructif.

**Le retrecissement vers l'uniforme se reproduit sur les compositions.** Etalonnage par
bande de part reelle, 96 cellules de camp, tous modeles : [MESURE,
`resultats/a46b-retrecissement.csv`]

| part reelle GSS | n | part decrite moyenne | rapport | ecart en points |
|---|---|---|---|---|
| moins de 5 % | 12 | 15,6 | **x 5,9** | +13,0 |
| 5 a 10 % | 12 | 28,4 | x 4,5 | +22,1 |
| 10 a 20 % | 36 | 19,3 | x 1,07 | +1,3 |
| 30 a 40 % | 18 | 46,0 | x 1,32 | +11,1 |
| plus de 40 % | 18 | 24,3 | **x 0,50** | **-24,7** |

Les groupes rares sont gonfles, les groupes majoritaires rabotes, exactement comme la courbe
d'etalonnage de r1 section 3.3 sur 8 718 modalites. La bande 30 a 40 pour cent fait
exception, tiree par `rep_evang` et `rep_south` que les trois modeles poussent vers 30 a 65
pour cent. **Le mecanisme de r1 s'observe sur un tout autre instrument.** [MESURE]

Et c'est **ce mecanisme meme qui produit l'apparence de correction**. Les humains d'Ahler et
Sood repondent entre 28 et 43 pour cent sur les huit items, quelle que soit la realite. Un
modele qui tire toute part vers un point fixe d'un tiers atterrit **au dessous** de 28 a 43
sur les items rares, donc plus pres de la realite qu'eux, sans rien savoir de mieux. La
correction mesuree est donc, en partie au moins, **un artefact du meme defaut de calibration
qui produit l'erreur ailleurs**. Elle n'en est pas moins reelle pour un lecteur, et c'est
tout l'objet de la section 4. [MESURE pour les deux courbes, [PROBABLE] pour l'attribution]

**Le taux de base, lui, contredit r1.** Sur les cellules sans camp, les trois modeles sont
presque exacts : `alpha` implicite median 0,98 pour Qwen3-4B, 0,96 pour gpt-oss-20b, 1,04
pour Qwen3-30B-A3B, ou 1 est la fidelite parfaite sur une partition binaire. Six items sur
huit sont a moins de cinq points de la realite. [MESURE]

| item | reel GSS, population | Qwen3-4B | gpt-oss-20b | Qwen3-30B-A3B |
|---|---|---|---|---|
| noirs | 14,3 | 13 | 23 | 12 |
| syndiques | 5,5 | **5** | 7 | 10 |
| athees ou sans religion | 40,5 | 15 | 18 | 10 |
| LGB | 12,4 | rejet, 1,1 puis 1,8 | 25 | 4 |
| evangeliques ou nes de nouveau | 28,4 | 30 | 23 | 25 |
| plus de 250 000 dollars | 2,2 | 12 | 7 | 1 |
| 65 ans et plus | 16,3 | 17 | 18 | 17 |
| sudistes | 30,2 | 31 | 30 | 33 |

Sur les cellules de camp, en revanche, `alpha` s'effondre : 0,36 a 0,42 pour Qwen3-4B, 0,77
a 0,85 pour Qwen3-30B-A3B. **La deformation n'est pas dans le taux de base, elle apparait
quand un camp est nomme.** [MESURE]

### 3.3 Le signal syndiques de r1 : il se reproduit sur le camp, il disparait sur la population

C'etait la question ouverte 5 d'`a46` et la section 3.4 de r1. Voici les deux instruments
cote a cote, camp de gauche, identite journaliste. [MESURE, `resultats/a46b-pont-r1.csv`]

| | reel GSS 2024 | croyance humaine | Qwen3-4B | gpt-oss-20b | Qwen3-30B-A3B |
|---|---|---|---|---|---|
| **population entiere**, question directe | 5,5 | | **5** | 7 | 10 |
| **camp de gauche**, question directe, ancrage ideologie | 5,5 | 38,8 | **35** | 30 | 18 |
| **camp de gauche**, question directe, ancrage parti | 7,1 | 38,8 | **45** | 0 | 45 |
| **camp de gauche**, distribution r1 sur `union1` | 5,5 | 38,8 | **65** | 17 | 14 |
| **camp de droite**, distribution r1 sur `union1` | 4,8 | | **75** | 7 | 5 |

**La reponse est nette et elle inverse la conclusion de r1 pour cet instrument.** Qwen3-4B,
interroge directement, donne **5 pour cent de syndiques dans la population adulte**, c'est a
dire la valeur exacte a 0,5 point pres. Il n'a donc **pas** de defaut de taux de base sur ce
groupe : la phrase d'`a46` section 6, « il croit que les trois quarts des Americains sont
syndiques », est **fausse** des qu'on lui pose la question. Ce qu'il a, c'est une inflation
**conditionnelle au camp** : avec le bon taux de base en tete, il multiplie par 6 a 8 des
qu'on nomme un camp. [MESURE]

La conclusion de r1 section 3.4, « le defaut de taux de base est bien un fait general »,
tient sur les 8 718 modalites du mode description et **ne se transporte pas sur la question
de composition directe**. Le meme fichier de poids, la meme temperature, deux formulations
donnent 65 pour cent et 5 pour cent. **C'est un troisieme exemple de la these centrale de
r1 : la quantite est une propriete du couple modele et protocole, pas du modele.** L'ecart
entre instruments atteint 45 points sur une seule cellule, Qwen3-4B, camp de gauche,
adversaire : 70 pour cent en mode description, 25 pour cent en question directe. [MESURE]

Rapporte a son propre taux de base, chaque modele gonfle la part de syndiques du camp de
gauche : **Qwen3-4B de +20 a +55 points** sur ses quatre cellules, **Qwen3-30B-A3B de +8 a
+35**, **gpt-oss-20b de -7 a +23**, ses deux cellules a zero comprises. L'ecart reel vaut
**0,0 point** sous l'ancrage ideologie et **+1,6** sous l'ancrage parti. Le signal existe
partout ; son ampleur est propre au modele et a l'instrument. [MESURE]

### 3.4 H4, le controle de taux de base : l'exageration n'est pas un simple defaut de taux de base

Concordance de signe entre le contraste du modele, `croyance(camp) - croyance(population)`,
et le contraste reel : [MESURE, `resultats/a46b-taux-de-base.csv`]

| modele | contrastes de signe concordant |
|---|---|
| Qwen3-30B-A3B | **29 / 32** |
| Qwen3-4B | **23 / 28** |
| gpt-oss-20b | 9 / 32 |

**H4 est confirmee pour Qwen3-30B-A3B et Qwen3-4B** : ils savent dans quel sens un groupe
est sur represente dans un camp, et leur erreur porte sur l'ampleur, pas sur la direction.
Elle est **rejetee pour gpt-oss-20b**, dont la concordance est sous le hasard, entierement
a cause des seize zeros qui ecrasent tous les contrastes du meme cote. [MESURE]

---

## 4. Ce que cela change au programme A et a la phrase pour un regulateur

### 4.1 Le point d'arret du mois 1, tel que l'errata E3 le formule, est atteint

E3 ecrit : « sur les huit compositions, apres le run de 08:05 : si aucun des trois modeles
n'exagere plus que les humains sous les deux bases et les deux ancrages, la version forte
ferme sur les compositions, l'issue le modele est un correcteur se publie, et l'experience
de lecture garde son objet sur les opinions seulement. »

**La condition est remplie.** Sous les deux bases et les deux ancrages, aucun des trois
modeles n'exagere plus que les humains de facon significative ; la direction ponctuelle est
« exagere moins » dans 34 tests sur 42 et n'atteint jamais le seuil de materialite dans
l'autre sens. **La version forte du programme A ferme sur les compositions.** [MESURE]

Trois reserves, et elles doivent voyager avec la conclusion.

1. **La condition est remplie avec zero puissance.** « Aucun ne depasse » et « le test
   n'a jamais pu conclure » sont ici la meme phrase. La lecture groupee, non
   preenregistree, donne un vrai signal sur Qwen3-30B-A3B, p = 0,0075 et 0,040, et elle
   seule ; le reste est une direction, pas une decision.
2. **Cela ne vaut que sur huit compositions americaines**, et l'errata E3 le dit deja pour
   les opinions.
3. **Fermer la version forte n'ouvre pas l'issue rassurante pour les trois modeles.**
   Qwen3-30B-A3B corrige ; Qwen3-4B egale l'erreur humaine en la deplacant ailleurs ;
   gpt-oss-20b repond zero une fois sur deux. **Une norme d'audit qui ne distingue pas ces
   trois comportements ne sert a rien**, et c'est le vrai livrable du mois 1.

### 4.2 Ce qu'il faut ajouter a `protocoles/01-experience-de-lecture.md`

Le protocole P1 porte sept hypotheses. Sa **H5** predit que les bras modele **augmentent**
l'estimation des parts rares, sur la foi de la courbe d'etalonnage de r1 : « l'assistant
installe la meme erreur que celle qu'Ahler et Sood documentent chez les humains ». Le run de
ce matin dit qu'**il faut ajouter une hypothese qui va dans l'autre sens sur le bloc
composition**, sans retirer H5, qui porte sur les items d'opinion.

**H9 proposee, dirigee, bloc composition, [HYPOTHESE].** Sur les huit items de composition
d'Ahler et Sood, les bras modele **reduisent** l'erreur absolue moyenne des estimations de
second ordre par rapport au temoin, et cette reduction se classe par modele dans l'ordre
mesure ici : Qwen3-30B-A3B le plus, Qwen3-4B le moins, gpt-oss-20b entre les deux avec une
part de son avantage due a des reponses nulles. Quantite attendue si le lecteur adoptait le
nombre du modele : l'erreur passerait de 19,8 points a 10,9 pour Qwen3-30B-A3B, a 9,8 pour
gpt-oss-20b, et resterait a 20,1 pour Qwen3-4B, contre 0 pour le bras distribution vraie.
[MESURE pour les valeurs, [HYPOTHESE] pour l'effet sur un lecteur, qui n'est pas mesure ici]

Deux remarques qui ne sont pas des details.

- **H9 et H5 ne se contredisent pas.** H5 porte sur les parts rares en valeur absolue, et le
  run la confirme : les groupes sous 5 pour cent recoivent 15,6 pour cent, x 5,9. H9 porte
  sur la comparaison au lecteur humain, qui repond lui 28 a 43 pour cent. **Le nombre du
  modele est entre la verite et la croyance humaine dans 41 cellules sur 96 contre l'ANES
  2012**, au dessous de la verite dans 36 et au dela de la croyance humaine dans 19.
  [MESURE] Un bras modele deplacerait donc le lecteur vers la verite sur une bonne moitie
  des cellules, l'y ferait passer au dela sur un tiers, et le polariserait davantage sur un
  cinquieme.
- **Le bras modele doit etre indexe par identite de demandeur ET par ancrage.** P1,
  decision 3, fige le parti pour le bloc composition ; le run mesure que passer de l'ancrage
  parti a l'ancrage ideologie deplace la reponse de 8 a 12 points en moyenne. La decision 3
  est donc **confirmee comme necessaire** : sans elle, le stimulus n'est pas defini.

### 4.3 La phrase pour un regulateur, corrigee

Ancienne phrase, errata E3 : elle ne disait rien de la croyance humaine de second ordre.
Elle peut maintenant en dire ceci, et rien de plus.

> Sur les huit compositions de partis dont un article publie mesure a la fois la realite et
> ce que 1 000 Americains en croient, trois modeles ouverts de trois familles, interroges a
> temperature zero avec la meme invite au caractere pres, **ne s'ecartent pas de la realite
> plus que les citoyens**, et deux des trois s'en ecartent environ deux fois moins,
> 9,8 et 10,9 points d'erreur absolue moyenne contre 19,8. **L'assistant n'est donc pas,
> sur cette quantite, une machine a ignorance pluraliste.** Il n'est pas non plus une
> archive : les trois modeles se contredisent jusqu'a repondre 0 et 37 pour cent a la meme
> question, l'un d'eux repond zero a la moitie des questions ou un groupe demographique est
> conditionne sur un camp, et changer le mot « parti » en « ideologie », ou l'identite de
> celui qui demande, deplace la reponse de 8 a 13 points. **La quantite a auditer n'est donc
> pas l'exageration, c'est la dispersion** : entre modeles, entre formulations, entre
> demandeurs. Une norme doit fixer le protocole et tenir un registre par version avant de
> fixer un seuil.

Ce que la phrase ne dit pas : rien sur les opinions, l'IGS Poll manquant toujours de
l'archive publique ; rien de causal ; rien hors de trois modeles ouverts petits, un pays,
huit groupes, une invite ; et rien qui repose sur un test significatif au sens
preenregistre, puisqu'il n'y en a aucun.

---

## 5. La figure

`resultats/a46b-figure-trois-termes.png` et `.svg`. Trois panneaux.

- **A.** Le rapport des exagerations, echelle logarithmique sur les deux axes : en abscisse
  l'exageration humaine contre l'ANES 2012, en ordonnee celle du modele contre le GSS 2024,
  lecture « base propre » de la page de plan. La diagonale est l'egalite ; **au dessus le
  modele exagere plus, au dessous il corrige**. Le point est la moyenne des quatre cellules
  de protocole, la barre leur etendue. Les marqueurs creux signalent au moins une cellule a
  reponse zero ; les deux couples ou les quatre cellules valent zero sont epingles sous le
  nuage avec leur libelle, parce que leur rapport n'existe pas.
- **B.** Le meme fait en points, contre la realite d'Ahler et Sood : **aucune cellule
  retiree**, zeros compris. C'est le panneau qui vaut preuve, parce qu'il ne depend d'aucune
  exclusion.
- **C.** Le taux de base, controle H4 : les huit cellules sans camp contre la part reelle
  dans les 1 052 personnes. Les points sont sur la diagonale a deux exceptions, `dem_aa` et
  `rep_rich`.

Palette categorielle a trois emplacements, validee toutes paires en mode clair, ecart CVD
9,2 et vision normale 24,0 ; forme de marqueur en encodage secondaire, de sorte que
l'identite du modele n'est jamais portee par la couleur seule.

---

## Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise.**

1. « Sur les huit compositions de partis d'Ahler et Sood, aucun des trois modeles ne
   s'ecarte de la realite significativement plus que les Americains, sous les deux bases de
   realite et les deux ancrages de camp. » [MESURE]
2. « Deux modeles sur trois font environ moitie moins d'erreur en points que l'Americain
   moyen : 9,8 et 10,9 points contre 19,8. » [MESURE]
3. « Qwen3-30B-A3B exagere environ deux fois moins que les humains, rapport groupe 0,46
   [0,30 ; 0,72], p = 0,0075 sous l'ancrage ideologie, identite adversaire. » [MESURE]
   **avec la mention obligatoire que ce test groupe les huit items et n'est pas
   preenregistre.**
4. « gpt-oss-20b repond zero a 16 des 32 questions de composition conditionnees sur un camp,
   dont les quatre sur la part de noirs chez les democrates, alors qu'il repond 23 pour cent
   a la meme question posee sur la population entiere. » [MESURE]
5. « Le changement d'ancrage, parti contre ideologie, deplace la reponse de 8 a 12 points en
   moyenne ; l'identite du demandeur de 4 a 13 points. » [MESURE]
6. « Le retrecissement vers l'uniforme mesure en r1 sur des distributions d'opinion se
   reproduit sur des questions de composition posees directement : les groupes sous 5 pour
   cent recoivent 15,6 pour cent en moyenne, les groupes au dessus de 40 pour cent en
   perdent 24,7. » [MESURE]
7. « Le taux de base des trois modeles sur ces huit groupes est presque exact ; la
   deformation apparait quand un camp est nomme. » [MESURE]

**Interdit.**

1. **Toute phrase avec le mot « significatif » au sens preenregistre.** Zero test sur 44
   l'est, et aucun ne pouvait l'etre.
2. **« Les modeles corrigent l'ignorance pluralistique. »** Un seul le fait clairement ;
   un deuxieme egale l'erreur humaine ; le troisieme refuse de repondre une fois sur deux.
   Et la correction mesuree est en partie l'effet mecanique d'un retrecissement vers un
   tiers, pas d'une connaissance. [PROBABLE]
3. **Toute phrase sur les opinions.** L'IGS Poll manque toujours ; l'interdiction de la
   section 7 de la page de plan et de la section 9 du preenregistrement de r1 tient sans
   changement.
4. **Toute phrase causale.** Ce run ne mesure pas ce que lire la reponse fait au lecteur.
   H9 est une hypothese pour `protocoles/01`, pas un resultat.
5. **Substituer une realite a l'autre.** `dem_aa` et `dem_lgb` continuent de rendre des
   verdicts opposes selon la base.
6. **Citer une moyenne calculee sur `a46-trois-termes.csv` sans filtrer
   `source_modele`**, a cause de la duplication decrite en 2.4 bis.
7. **Generaliser hors de ces trois modeles, de ces huit groupes, de ce pays, de cette
   invite et de cette quantification.**

---

## Ce que je n'ai pas pu verifier

1. **Pourquoi gpt-oss-20b repond zero.** Le gabarit harmony avec `Reasoning: low` ne laisse
   dans la trace que deux jetons generes ; la chaine de raisonnement n'est pas enregistree.
   L'interpretation « refus de conditionner un attribut demographique sur un camp » est
   [PROBABLE] et non demontree. Le controle qui trancherait, poser la meme question avec un
   camp fictif ou avec un attribut non protege, n'a pas ete fait et couterait quelques
   dizaines d'appels.
2. **Ce que Qwen3-4B aurait repondu sur le taux de base des LGB.** Le parse a rejete `1.1`
   puis `1.8`. La valeur substantive, entre 1 et 2 pour cent, est lisible dans la trace mais
   n'entre dans aucun tableau, et je ne l'ai pas repechee.
3. **La stabilite des reponses.** Un appel par cellule, temperature 0, `top_k` 1 : rien ne
   dit ce que donnerait une autre graine, un autre ordre de cellules ou un cache de prefixe
   dans un autre etat. Le run r1 a montre que le protocole deplace la quantite d'un facteur
   quatorze ; une seule mesure par cellule ne borne pas cela.
4. **La correspondance entre le camp decrit au modele et le camp mesure chez Ahler et
   Sood.** « Democratic Party supporters » posee au modele et `pid_3` construit sur `pid7`
   chez eux ne sont pas verifies personne par personne, la reserve 2 de
   `a46-second-ordre-ahler-sood.md` tient sans changement.
5. **Le texte du papier d'Ahler et Sood.** Toujours HTTP 403 ; rien n'a ete relu ce matin.
   Les libelles employes restent reconstruits a partir du codebook.
6. **La part attribuable a la definition et la part attribuable a l'echantillon** dans
   l'ecart de `dem_aa` et `dem_lgb` entre les deux bases. Non separable ici.
7. **Ce que donnerait un `alpha` de retrecissement ajuste proprement sur les
   compositions.** L'`alpha` implicite rapporte en 3.2 est calcule cellule par cellule sur
   une partition binaire, point fixe 50 pour cent, et non ajuste par moindres carres comme
   en r1 ou la partition a `K` modalites. Les deux nombres ne sont pas directement
   comparables et je ne les ai pas mis dans le meme tableau.
8. **Le comportement des modeles sur les quatorze groupes candidats.** Aucun appel n'a ete
   passe ; le tableau de la section 2.4 ne donne que la realite mesurable.

---

## Questions ouvertes pour Simon

1. **Le test doit il grouper les deux camps ?** Le plan teste quatre items par camp, ce qui
   rend son propre seuil inatteignable ; grouper les huit le rend atteignable et fait sortir
   deux cellules a p inferieur a 0,05. La question n'est pas technique : elle demande si un
   test qui ne peut structurellement pas rejeter compte comme un test. Ma reponse serait
   non, et il faut alors ecrire que la page de plan a preenregistre un test vide et publier
   la lecture groupee comme deviation declaree. **Trancher avant de citer le moindre p.**
2. **Le zero de gpt-oss-20b est il une donnee ou une panne ?** S'il est une donnee, il
   appartient au tableau et le modele est le plus faux des trois sur `dem_black`. S'il est
   une panne de conditionnement, il faut un motif de rejet nouveau, « valeur degeneree », et
   le modele sort du run avec un taux d'echec de 50 pour cent. Le choix change le verdict de
   la moitie du run et il n'est pas dans la page de plan.
3. **Faut il un critere de chute sur le nombre de valeurs distinctes ?** Trois valeurs sur
   32 cellules ont passe le critere 2 tel qu'il est ecrit. Le critere sur la valeur modale
   ne voit pas ce cas. Une regle du type « moins de cinq valeurs distinctes sur trente deux
   cellules » l'aurait vu, et elle serait a preenregistrer pour le prochain run, pas a
   appliquer a celui ci.
4. **Quelle base est la base principale ?** La question 2 d'`a46` reste ouverte ici et
   `protocoles/01` l'a deja tranchee dans son sens, GSS contemporain principal et ANES a
   cote. Le run montre que le choix ne change pas la direction, les douze rapports groupes
   restent sous 1 sous les deux bases, mais qu'il change l'ampleur, x 1,79 contre x 2,33
   pour Qwen3-4B. Faut il aligner la page de plan d'`a46` sur `protocoles/01` par un
   erratum, pour que le dossier ne porte pas deux reponses ?
5. **Ecrire a Gaurav Sood, oui ou non, et quand ?** Rien n'a change depuis cette nuit :
   sans `pcomp_igspoll.dta`, la comparaison a trois termes reste une comparaison de
   compositions. Ce matin ajoute un argument a la lettre : nous avons maintenant un resultat
   publiable sur les compositions, et la question naturelle du lecteur sera « et sur les
   opinions ? ».
6. **Faut il corriger la lecture des traces r1 ?** `lire_traces_r1` prend tous les
   `r1-*.jsonl` et double donc Qwen3-4B depuis que R4 a ecrit sa copie. Le correctif tient
   en une ligne, une liste blanche de fichiers, mais il modifie `a46_commun.py`, ce que
   cette seance s'interdit. A faire, par qui et quand ?
7. **Le run elargi vaut il ses 240 appels ?** Il ne rendra pas un point de puissance sur la
   comparaison a trois termes, faute de croyance humaine sur les nouveaux groupes. Il rendra
   H1 et H4 decidables et triplera le perimetre de la dispersion inter modeles. Est ce le
   bon usage de deux minutes de machine, ou la lettre a Sood passe t elle devant ?

---

## Fichiers produits

| fichier | contenu |
|---|---|
| `analyses/a46b_tableaux.py` | toutes les lectures de ce rapport, aucun appel de modele |
| `analyses/a46b_items_candidats.py` | les quatorze groupes mesurables pour un run elargi |
| `analyses/a46b_figure.py` | la figure, ne recalcule rien |
| `resultats/a46b-par-item.csv` | 96 lignes, les trois termes par item, modele, ancrage et identite |
| `resultats/a46b-taux-de-base.csv` | 92 lignes, H4, le contraste camp moins population |
| `resultats/a46b-identite.csv` | H3, six lignes, IC bootstrap sur les items |
| `resultats/a46b-ancrage.csv` | parti contre ideologie, trois lignes |
| `resultats/a46b-verdict-cellule.csv` | les 44 verdicts preenregistres, avec le p minimal atteignable |
| `resultats/a46b-tests-groupes.csv` | les tests a huit items, NON PREENREGISTRES, trois lectures de base |
| `resultats/a46b-points.csv` | la comparaison en points, qui ne retire aucune cellule |
| `resultats/a46b-criteres-de-chute.csv` | les quatre criteres, evalues |
| `resultats/a46b-pont-r1.csv` | `union1` et `reborn` par deux instruments |
| `resultats/a46b-retrecissement.csv` | l'`alpha` implicite et l'etalonnage sur les compositions |
| `resultats/a46b-puissance.csv` | le p minimal atteignable, de 1 a 12 items |
| `resultats/a46b-items-candidats.csv` | 112 lignes, quatorze groupes, deux ancrages, IC de Wilson |
| `resultats/a46b-figure-trois-termes.png` et `.svg` | la figure, trois panneaux |

Ordre de lancement, aucun appel de modele :

```
.venv/bin/python analyses/a46b_tableaux.py
.venv/bin/python analyses/a46b_items_candidats.py
.venv/bin/python analyses/a46b_figure.py
```
