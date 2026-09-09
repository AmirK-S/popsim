# r1. Ce que l'oracle des camps etablit sur trois modeles, contre la page de plan

> Erratum du 9 septembre 2026, 09:25 (ligne 551) : « Qwen3-4B-Base est deja telecharge selon a3 section 4.4 » est faux deux fois. a3 4.4 ne parle d aucun telechargement et le socle n etait pas sur la machine ; la reference visee est a27 section 4.4. Le socle a ete obtenu et documente dans resultats/r4-oracle-socle.md, section « Provenance des poids », avant le run R4. Le corps du rapport est laisse tel quel.

Lecture d'interpretation du run R1 (2 682 cellules, nuit du 8 au 9 septembre 2026), ecrite
apres l'evaluation de 23:17. Aucun appel de modele, aucun fichier existant modifie ; deux
scripts nouveaux, `analyses/r1b_contraste_mode.py` et `analyses/r1b_par_item.py`, quatre
coeurs, lecture seule sur `data/traces/`. Le `llama-server` de R2 n'a pas ete touche.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## Reponse en une ligne

**Les trois modeles decrivent tous les camps comme plus varies qu'ils ne sont et adaptent
tous le portrait a l'identite du demandeur, mais ils se contredisent sur l'ecart entre camps
de 0,18 a 1,32 ; et sur les memes 29 items, la meme quantite et le meme fichier de modele,
Qwen3-4B ecrase l'ecart d'un facteur cinq quand il decrit un camp et l'exagere d'un facteur
1,62 quand il incarne des individus etiquetes, soit un facteur 14 entre deux protocoles a
temperature 0 : la fidelite de representation des camps n'est pas une propriete du modele,
c'est une propriete du couple modele et protocole.** [MESURE]

---

## Protocole rappele, en six lignes

149 items du GSS x 3 camps (gauche 417, centre 303, droite 332) x 2 identites de demandeur
(journaliste neutre, membre du camp adverse) x 3 modeles (Qwen3-4B-Instruct-2507 Q4_K_M,
gpt-oss-20b MXFP4, Qwen3-30B-A3B-Instruct-2507 Q4_K_M), un appel par cellule, mode
« describe » de arXiv 2607.25292, temperature 0, `top_k` 1, gabarit de conversation propre a
chaque famille. Referent humain : frequences de la vague 1 ; plancher de bruit : les memes
1 052 personnes reinterrogees a deux semaines. Bootstrap sur les items (2 000 tirages),
permutation de signe appariee par item (20 000 tirages, estimateur de Phipson et Smyth),
Holm a l'interieur des cinq familles preenregistrees et jamais entre elles, seuil 0,05,
bande de nullite pratique [0,95 ; 1,05]. Page de plan horodatee 22:06:11, dix minutes avant
le premier appel : `resultats/r1-preenregistrement.md`.

---

## 1. Les quatre hypotheses, modele par modele et en bloc

### 1.1 H1, l'unanimite : rejetee dans la direction inverse, a l'unanimite des trois modeles

Prediction preenregistree : rapport `GS decrit / GS reel` **inferieur** a 1.
**Les dix huit cellules sont au dessus de 1.** [MESURE, `r1-h1-unanimite.csv`]

| camp | identite | Qwen3-4B | gpt-oss-20b | Qwen3-30B-A3B | plancher |
|---|---|---|---|---|---|
| gauche | journaliste | **1,174** [1,109 ; 1,243] | **1,097** [1,039 ; 1,156] | **1,086** [1,036 ; 1,143] | 1,005 |
| gauche | adversaire | **1,181** [1,116 ; 1,249] | 1,060 [1,009 ; 1,115] *ns* | **1,069** [1,021 ; 1,119] | 1,005 |
| centre | journaliste | **1,114** [1,063 ; 1,175] | **1,099** [1,048 ; 1,149] | **1,103** [1,063 ; 1,149] | 1,008 |
| centre | adversaire | **1,145** [1,098 ; 1,199] | **1,077** [1,027 ; 1,123] | 1,073 [1,032 ; 1,118] *ns* | 1,008 |
| droite | journaliste | **1,059** [1,014 ; 1,116] | 1,042 [0,998 ; 1,088] *nul en pratique* | **1,083** [1,040 ; 1,127] | 0,996 |
| droite | adversaire | **1,060** [1,020 ; 1,108] | 1,009 [0,964 ; 1,053] *ns* | **1,052** [1,010 ; 1,099] | 0,996 |

**Verdict par modele.** Qwen3-4B : six cellules sur six significatives, toutes en
amplification de variete. Qwen3-30B-A3B : cinq sur six. gpt-oss-20b : trois sur six
significatives, une declaree nulle en pratique, deux non significatives, **et les six
au dessus de 1**.

**Verdict en bloc.** H1 est rejetee, et l'effet inverse est etabli sur les trois modeles.
**Le 20 milliards et le 30 milliards font comme le 4 milliards** sur cette hypothese, avec
une intensite decroissante avec la taille du modele sur le camp de gauche (1,17 puis 1,10
puis 1,09) mais pas sur le camp de droite (1,06 puis 1,04 puis 1,08). L'ordre reste stable :
**le camp de gauche est le plus sur decrit, le camp de droite le moins**, alors que le camp
de gauche est en realite le plus homogene des trois (`GS` reel 0,45 contre 0,51 a droite).
Le modele exagere le plus la variete la ou la realite est la plus resserree. [MESURE]

### 1.2 H2, l'ecart entre camps : la reponse depend du modele

Prediction preenregistree : facteur **superieur** a 1, sur les deux quantites.

**H2a, ecart non signe, distance de variation totale entre les deux camps, 149 items**
[MESURE, `r1-h2-ecart.csv`]

| modele | journaliste | adversaire |
|---|---|---|
| Qwen3-4B | 0,894 [0,780 ; 1,045] *ns* | 0,771 [0,646 ; 0,915] *ns* |
| gpt-oss-20b | 0,875 [0,720 ; 1,038] *ns* | **1,076** [0,921 ; 1,245] |
| Qwen3-30B-A3B | **1,175** [1,048 ; 1,320] | **1,324** [1,179 ; 1,492] |

**H2b, ecart signe sur l'echelle de position orientee, 79 items orientes de `a37`**

| modele | journaliste | adversaire | items retenus stricts (65), journaliste |
|---|---|---|---|
| Qwen3-4B | **0,245** [0,056 ; 0,437] | **0,221** [0,053 ; 0,380] | **0,304** [0,117 ; 0,514] |
| gpt-oss-20b | **0,618** [0,408 ; 0,842] | **0,633** [0,383 ; 0,894] | **0,694** [0,463 ; 0,933] |
| Qwen3-30B-A3B | **1,268** [1,097 ; 1,464] | **1,366** [1,155 ; 1,599] | **1,293** [1,101 ; 1,499] |
| *plancher humain* | *1,009* | | *1,011* |

**Verdict.** H2 n'est confirmee que sur Qwen3-30B-A3B. Elle est **rejetee dans la direction
inverse** sur Qwen3-4B et sur gpt-oss-20b, dont les intervalles excluent le plancher humain
par le bas. **Les trois modeles ne concordent pas**, et le classement est le meme sur les
trois perimetres d'items et sur les deux identites de demandeur : le rang est une propriete
du modele, pas de l'echantillon d'items.

**Reponse a la question posee.** Non, le 20 milliards et le 30 milliards ne font pas la meme
chose que le 4 milliards. Le 20 milliards fait comme lui en plus faible (0,62 contre 0,25) ;
**le 30 milliards fait l'inverse** (1,27). La sous representation des ecarts vue a 00:30 sur
Qwen3-4B n'est donc **pas** un fait general du mode description : c'est un fait de Qwen3-4B,
partage a moitie par gpt-oss-20b et contredit par Qwen3-30B-A3B.

**Le mecanisme de l'ecrasement est en partie une indifference au camp.** La part d'items ou
le modele donne **exactement la meme distribution** aux camps de gauche et de droite vaut
0,349 chez gpt-oss-20b, 0,143 chez Qwen3-4B et 0,108 chez Qwen3-30B-A3B en identite
journaliste [MESURE, `r1-par-item-ecarts.csv`]. Le critere de chute 3 (seuil 0,90) passe
partout, mais ces valeurs se lisent : un tiers des items ne recoit aucun camp chez
gpt-oss-20b.

### 1.3 H3, l'identite du demandeur : confirmee, sur les six cellules, sans direction

Aucune direction n'etait predite ; un ecart au plancher l'etait. [MESURE, `r1-h3-identite.csv`]

| modele | camp | TV entre identites | plancher | rapport | items identiques | items au dessus du plancher | p Holm |
|---|---|---|---|---|---|---|---|
| gpt-oss-20b | gauche | 0,103 | 0,024 | **4,23** [3,20 ; 5,62] | 40 % | 59 % | 0,0003 |
| gpt-oss-20b | droite | 0,101 | 0,028 | **3,64** [2,77 ; 4,60] | 40 % | 57 % | 0,0003 |
| Qwen3-4B | droite | 0,084 | 0,027 | **3,09** [2,48 ; 3,83] | 27 % | 67 % | 0,0003 |
| Qwen3-4B | gauche | 0,073 | 0,024 | **3,07** [2,40 ; 3,86] | 35 % | 62 % | 0,0003 |
| Qwen3-30B-A3B | gauche | 0,073 | 0,024 | **3,04** [2,34 ; 3,77] | 24 % | 71 % | 0,0003 |
| Qwen3-30B-A3B | droite | 0,076 | 0,028 | **2,74** [2,15 ; 3,51] | 30 % | 61 % | 0,0003 |

**Verdict.** H3 est confirmee sur les trois modeles, aux deux camps, au p minimal que
20 000 permutations autorisent. C'est le seul resultat du run ou les trois modeles concordent
en niveau et pas seulement en signe : le rapport au plancher tient dans une fourchette de
2,74 a 4,23.

**Et il n'y a aucune direction.** Mesure nouvelle, non preenregistree et declaree comme telle :
le deplacement du camp decrit sur l'echelle orientee de `a37`, signe de sorte qu'une valeur
positive veuille dire « plus caricatural quand c'est l'adversaire qui demande ».
[MESURE, `r1b-direction-identite.csv`, 79 items, bootstrap sur les items, Holm sur six tests]

| modele | camp | deplacement vers le pole du camp | IC 95 % | p Holm |
|---|---|---|---|---|
| gpt-oss-20b | gauche | **-0,018** | [-0,045 ; +0,009] | 0,988 |
| gpt-oss-20b | droite | +0,022 | [-0,013 ; +0,059] | 1,000 |
| Qwen3-30B-A3B | droite | +0,020 | [-0,002 ; +0,039] | 0,286 |
| Qwen3-30B-A3B | gauche | +0,003 | [-0,021 ; +0,026] | 1,000 |
| Qwen3-4B | gauche | +0,002 | [-0,015 ; +0,019] | 1,000 |
| Qwen3-4B | droite | -0,007 | [-0,025 ; +0,010] | 1,000 |

**Aucune cellule ne survit a Holm.** Le portrait bouge beaucoup, trois a quatre fois le bruit
humain, mais il ne bouge pas dans un sens. La phrase « le modele caricature le camp adverse
pour plaire au demandeur » n'est pas soutenue par ce run, et elle est **interdite** tant que
cette mesure reste nulle. Ce qui bouge est la forme de la distribution, pas sa position.
[MESURE]

### 1.4 H4, les items a derive marquee : confirmee sur une quantite sur deux

[MESURE, `r1-h4-derive.csv`, correlation de rang de Spearman avec `|derive agregee|` de `a37`]

| quantite | gpt-oss-20b | Qwen3-30B-A3B | Qwen3-4B |
|---|---|---|---|
| deficit d'unanimite `1 - GS decrit / GS reel`, 79 items | **-0,68** / **-0,55** | **-0,50** / **-0,43** | **-0,64** / **-0,65** |
| log amplification de l'ecart entre camps | **+0,38** (52) / **+0,42** (62) | **+0,46** (77) / **+0,50** (75) | +0,23 (71) / +0,27 (61) *ns* |

*(journaliste / adversaire ; entre parentheses le nombre d'items ou la quantite est definie)*

**Dix cellules sur douze passent Holm, pas douze.** Les deux cellules de Qwen3-4B sur la
seconde quantite sont a `p_holm` = 0,0700 et sont **non significatives** au seuil
preenregistre de 0,05. `resultats/r1-oracle-des-camps.md` ecrit « Les douze cellules passent
Holm » : c'est une erreur de lecture du CSV, a corriger. [MESURE, `r1-h4-derive.csv`,
colonnes `p_holm` lignes 11 et 12]

**Le signe de la premiere quantite demande la phrase que le rapport de run donne deja** : le
deficit est negatif partout puisque le rapport depasse 1, donc une correlation negative avec
la derive veut dire que **la sur dispersion est la plus forte sur les items ou la population
penche le plus massivement d'un cote**. Les modeles sont les plus faux la ou le consensus
reel est le plus grand.

**Une reserve sur la seconde quantite, qui n'est pas dans le rapport de run.** Le log de
l'amplification n'est defini que sur les items ou le modele a donne un ecart non nul entre
les camps. Or ces items exclus sont precisement ceux ou l'ecrasement est total : 27 items sur
79 chez gpt-oss-20b en identite journaliste, 20 sur 79 chez Qwen3-4B en identite adversaire,
2 sur 79 chez Qwen3-30B-A3B [MESURE, `r1-par-item-ecarts.csv`]. **La correlation est donc
calculee sur le sous ensemble ou le modele differencie encore les camps**, ce qui la rend
conservatrice pour les deux modeles qui aplatissent et quasi complete pour celui qui exagere.
La comparaison des trois rho entre eux est a ce titre biaisee, et il faut le dire.

### 1.5 En bloc : ce qui concorde et ce qui ne concorde pas

| | les trois modeles concordent ? |
|---|---|
| H1, sur dispersion interne | **oui**, 18 cellules sur 18 au dessus de 1 |
| H2, ecart entre camps | **non**, 0,25 / 0,62 / 1,27, intervalles disjoints du plancher dans des directions opposees |
| H3, dependance a l'identite du demandeur | **oui**, 2,74 a 4,23 fois le plancher, p Holm minimal partout |
| H3, direction du deplacement | **oui, nulle partout** : aucune cellule ne survit a Holm |
| H4, lien avec la derive de l'item | **oui** sur le deficit d'unanimite ; **non** sur l'amplification, ou Qwen3-4B ne passe pas |

---

## 2. La comparaison au mode simulation

### 2.1 Le pont est construit, et il est exact

Le preenregistrement interdit la comparaison chiffree du facteur H2b au facteur 1,62 de
`a38`, pour trois raisons : perimetre d'items (79 contre 29), echelle (position de
nomenclature contre score de desirabilite de `a25`), mode (description contre incarnation).
**Les deux premieres se levent par le calcul, et l'ont ete.** [MESURE,
`analyses/r1b_contraste_mode.py`]

1. **Les 29 items a pole declare de `a38` sont tous dans les 79 items orientes de `a37`.**
   Verifie a l'execution : 29 sur 29.
2. **Sur ces 29 items, les deux echelles sont la meme quantite.** L'ecart absolu maximal
   entre `desirabilite(gauche) - desirabilite(droite)` et
   `position(droite) - position(gauche)` sur les 29 items est **exactement 0,0**. Les 29
   items ont tous le pole `droite_bas`, et la regle « ordre » de `a25` produit alors le
   complement a 1 de la position de `a37`. Le facteur H2b restreint aux 29 items et le
   facteur de `a38` recalcule sur les distributions decrites tombent au chiffre pres sur les
   memes valeurs [MESURE, `r1b-contraste-mode.csv` et `r1b-h2b-29-items.csv`].
3. **Le referent humain retombe sur celui de `a38`.** L'ecart humain moyen entre camps sur
   les 29 items, recalcule ici depuis `data/traces/r1-distributions-reelles.csv`, vaut
   **0,236063**, exactement la valeur publiee par `a38` au perimetre 1 052. C'est le controle
   de nomenclature du pont, et il passe. [MESURE]
4. **Le modele est le meme fichier.** `a5` fait tourner C2 et C3 sur
   `Qwen3-4B-Instruct-2507-Q4_K_M.gguf`, temperature 0 ; R1 fait tourner `q4` sur le meme
   fichier, meme quantification, meme temperature. [CONFIRME, `a5` sections 1 et 2,
   `r1-oracle-des-camps.md` section 4]

**Il ne reste donc que le mode.** C'est le contraste que la page de plan disait impossible et
qui l'est devenu.

### 2.2 Un seul modele, deux protocoles, un facteur 14

[MESURE, 29 items a pole declare, quantite de `a38`, bootstrap sur les items]

| protocole, Qwen3-4B-Instruct-2507 Q4_K_M, temperature 0 | facteur | IC 95 % | source |
|---|---|---|---|
| description d'un camp, demandeur adversaire | **0,115** | [-0,205 ; 0,503] | `r1b-contraste-mode.csv` |
| description d'un camp, demandeur journaliste | **0,179** | [-0,202 ; 0,578] | `r1b-contraste-mode.csv` |
| incarnation C3, 119 reponses d'enquete, sans etiquette | **0,523** | [0,20 ; 0,82] | `a38-camp.csv`, perimetre 150 |
| *humains reinterroges a deux semaines* | *1,025* | *[0,986 ; 1,064]* | *plancher, perimetre 1 052* |
| incarnation C2, persona demographique a onze attributs dont l'ideologie | **1,617** | [1,06 ; 2,10] | `a38-camp.csv`, perimetre 150 |

**Le contraste, avec ses intervalles.** Entre la description au journaliste (0,179) et
l'incarnation C2 (1,617), les deux intervalles de confiance **ne se recouvrent pas** ; le
test de permutation de signe apparie item par item sur les 29 items donne p = 0,00025 pour
l'identite journaliste et p = 0,00005 pour l'identite adversaire
[MESURE, `r1b-contraste-apparie-modes.csv`]. Le rapport ponctuel vaut **9,0** en identite
journaliste et **14,0** en identite adversaire.

**Le rapport des deux facteurs ne recoit pas d'intervalle lisible, et il faut le dire.**
C'est un rapport de rapports de sommes dont le denominateur (le facteur de description) a un
intervalle qui contient zero ; le bootstrap rend un intervalle qui va de -79 a +90, ce qui
n'est pas une mesure. C'est exactement la propriete que `a47` releve deja sur le ratio inter.
**Ce qui se cite est : les deux facteurs avec leurs intervalles, et le p de la difference
appariee.** Le rapport ponctuel se cite comme un ordre de grandeur, jamais avec un
intervalle.

**Deux signes ?** Non, et c'est une correction a la formulation de la question. Les deux
facteurs sont **positifs** : dans les deux modes, le camp de droite reste du cote droit du
camp de gauche. Ce qui change de cote, c'est **le rapport a 1** : la description tombe cinq a
neuf fois sous la fidelite humaine, l'incarnation etiquetee la depasse de 62 pour cent. La
phrase juste est « deux cotes du plancher humain », pas « deux signes ».

**Ce que le contraste confond, et qui interdit de dire « c'est le mode ».** C2 et la
description ne different pas seulement par le mode. C2 simule 150 personnes, une par une, et
lit la distribution sur les probabilites de token d'un appel a `n_predict` 1 ; la description
fait un appel par camp et lit des pourcentages ecrits en clair. C2 recoit une etiquette
ideologique dans un persona de onze attributs ; la description recoit un nom de camp dans une
consigne d'enquete. **Trois facteurs bougent ensemble : le mode, l'unite simulee et la
lecture.** C3 le montre : incarnation sans etiquette, 0,523, entre les deux, et deja sous le
plancher. L'enonce defendable est donc :

> A modele constant, quantification constante, temperature constante, memes 29 items et meme
> referent humain, le facteur d'amplification de l'ecart entre camps de Qwen3-4B va de 0,115
> a 1,617 selon le protocole, soit un facteur quatorze, alors que le plancher de
> reinterrogation humaine vaut 1,02. [MESURE]

C'est la variable de `a15` reproduite a l'interieur d'un seul modele : `a15` conclut que le
sens de la distorsion inter groupes est une propriete du dispositif de mesure et non du
modele, et ce contraste en est la premiere mesure interne au dossier, sur une seule famille
de modele et un seul jeu d'items. [MESURE, contre `a15` section 7.1 CONFIRME]

### 2.3 gpt-oss-20b et Qwen3-30B-A3B : ce qu'on a et ce qu'on n'a pas

**Ce qu'on a**, sur les memes 29 items, la meme quantite, le meme referent humain 0,236063
[MESURE, `r1b-contraste-mode.csv`] :

| modele | description, journaliste | description, adversaire |
|---|---|---|
| gpt-oss-20b | **0,366** [0,019 ; 0,747] | **0,364** [-0,004 ; 0,833] |
| Qwen3-30B-A3B | **1,319** [1,057 ; 1,672] | **1,518** [1,233 ; 1,917] |

**Ce qu'on n'a pas.** Aucun run d'incarnation n'existe pour ces deux modeles. Ni C2, ni C3,
ni aucune des conditions de `a37` et `a38`, qui sont toutes des runs Qwen3-4B ou des reprises
des traces de Stanford. **Le contraste des deux modes n'existe que sur Qwen3-4B**, et toute
phrase de la forme « les modeles caricaturent en incarnation et aplatissent en description »
est, en l'etat, une phrase sur un seul modele. R2, lance a 23:16, produit une condition de
type C3F sur gpt-oss-20b : quand il aura rendu, le pont existera pour un second modele, mais
**pour la branche sans etiquette seulement**. Le contraste C2, celui qui porte le 1,62, exige
un run de persona etiquete sur gpt-oss-20b et sur Qwen3-30B-A3B qui n'est planifie nulle
part.

**Le fait le plus derangeant du tableau ci dessus.** Qwen3-30B-A3B en mode description
(1,32 a 1,52) est **du meme cote du plancher que Qwen3-4B en mode incarnation etiquetee**
(1,62), et de l'autre cote que Qwen3-4B en mode description (0,18). Autrement dit, sur cette
quantite, **le choix du modele deplace autant que le choix du protocole**. Un audit qui fixe
le protocole et fait varier le modele, et un audit qui fixe le modele et fait varier le
protocole, mesurent des ecarts du meme ordre. [MESURE]

---

## 3. Ou le modele se trompe

### 3.1 L'ampleur de l'erreur, et son plancher

Distance de variation totale moyenne entre le portrait et la realite, identite journaliste
[MESURE, `r1b-erreurs-par-item.csv`] :

| modele | gauche | centre | droite |
|---|---|---|---|
| Qwen3-30B-A3B | 0,199 | 0,205 | 0,217 |
| gpt-oss-20b | 0,249 | 0,237 | 0,253 |
| Qwen3-4B | 0,265 | 0,255 | **0,306** |
| *plancher humain vague 1 contre vague 2* | *0,024* | *0,030* | *0,027* |

L'erreur vaut **sept a onze fois le bruit de reinterrogation humaine**. L'ordre de grandeur
est celui que `a27` publie pour la voie describe, 0,22 de distance de variation totale contre
0,46 pour l'Argyle standard [CONFIRME, `a27` section 3.2] : notre 0,20 a 0,31 par camp est
compatible, ce qui est un controle externe de plus, non preenregistre.

### 3.2 Les plus grands ecarts, par item

Moyenne sur les trois modeles et les trois camps, identite journaliste
[MESURE, `r1b-erreurs-par-item.csv`] :

| item | TV moyenne | part modale reelle | K | lecture |
|---|---|---|---|---|
| `fucitzn` | **0,900** | 99,1 % | 5 | citoyennete du pere : la realite est quasi degeneree, le modele repartit |
| `mnthsusa` | **0,710** | 98,2 % | 6 | mois passes aux Etats Unis, meme structure |
| `jew` | **0,673** | 69,5 % | 5 | appartenance juive, taux de base tres bas sur les modalites minoritaires |
| `jew16*` | **0,647** | 73,2 % | 5 | idem, a seize ans |
| `spjew` | **0,587** | 70,1 % | 5 | idem, conjoint |
| `spfund` | **0,553** | 68,3 % | 4 | fondamentalisme du conjoint |
| `hapmar` | **0,507** | 56,6 % | 4 | bonheur conjugal |
| `joblose` | **0,500** | 44,1 % | 5 | crainte de perdre son emploi |
| `spdeg*` | **0,500** | 51,0 % | 6 | diplome du conjoint |
| `income` | **0,458** | 51,7 % | 12 | revenu, douze modalites |
| `nataid/y` | **0,453** | 70,3 % | 3 | aide etrangere, derive 0,318 |

Et les plus justes : `uscitzn*` 0,039, `compuse*` 0,042, `spkhomo/y` 0,083, `wrkgovt1`
0,084, `wrkgovt2` 0,088, `webmob` 0,090, `abnomore` 0,092, `fepol` 0,092 : **tous a deux
modalites**.

**La lecture n'est ni le sujet ni la derive, c'est la structure de l'item.** Correlation de
rang entre l'erreur et le nombre de modalites : **+0,58** chez Qwen3-4B, +0,49 chez
Qwen3-30B-A3B, +0,40 chez gpt-oss-20b, sur les 149 items [MESURE]. Les items politiques a
forte derive ne sont pas les plus faux ; ce sont les items factuels a nombreuses modalites et
a realite quasi degeneree.

### 3.3 Le mecanisme : un retrecissement vers l'uniforme

Cellule par cellule, on ajuste `p_decrit = alpha x p_reel + (1 - alpha) x uniforme` au sens
des moindres carres. `alpha` = 1 est la fidelite, `alpha` = 0 est l'uniforme, `alpha`
negatif est une distribution anti correlee a la realite. [MESURE, non preenregistre, declare
comme tel]

| modele | `alpha` median, tous items | `alpha` median, K = 2 | `alpha` median, K = 4 |
|---|---|---|---|
| Qwen3-30B-A3B | **0,614** | | 0,764 |
| gpt-oss-20b | **0,429** | | 0,523 |
| Qwen3-4B | **0,332** | | 0,115 |
| *tous modeles* | | *0,758* | |

**Le classement de `alpha` est exactement l'inverse du classement de H1** : le modele qui
retrecit le plus vers l'uniforme est celui qui sur decrit le plus la variete. H1 et cet
`alpha` sont deux lectures du meme fait. Et `alpha` s'effondre quand le nombre de modalites
monte : median 0,758 a deux modalites, 0,157 entre cinq et six.

L'etalonnage par bande de part reelle, sur les 8 718 couples (modalite, cellule)
[MESURE, `r1b-etalonnage-taux-de-base.csv`, tous modeles] :

| part reelle | n | part decrite moyenne | rapport | ecart en points |
|---|---|---|---|---|
| moins de 1 % | 376 | **11,9 %** | **34,4** | +11,6 |
| 1 a 2 % | 306 | **13,6 %** | 8,3 | +11,9 |
| 2 a 5 % | 802 | 13,6 % | 3,9 | +10,2 |
| 5 a 10 % | 769 | 18,7 % | 2,6 | +11,4 |
| 10 a 20 % | 1 470 | 23,0 % | 1,5 | +8,0 |
| 20 a 30 % | 1 241 | 30,2 % | 1,2 | +5,0 |
| 30 a 40 % | 1 065 | 34,1 % | 0,97 | -0,9 |
| 40 a 50 % | 796 | 35,1 % | 0,79 | -9,3 |
| 50 a 60 % | 597 | 41,9 % | 0,77 | -12,7 |
| 60 a 75 % | 654 | 46,6 % | 0,70 | -19,9 |
| plus de 75 % | 642 | **65,6 %** | 0,75 | **-21,7** |

Le point fixe est vers 34 pour cent. **Toute modalite sous un tiers est gonflee, toute
modalite au dessus est rabotee**, et la deformation est monotone. Figure
`resultats/r1b-figure-modes.png` panneau (b).

### 3.4 Le signal syndiques de `a46` : oui pour le mecanisme, non pour l'ampleur

L'item `union1` est dans les 149 items de R1, et le signal de `a46` s'y recalcule
directement. Les deux modalites ou le repondant lui meme est syndique
[MESURE, `data/traces/r1-q4.jsonl`, `r1-oss20.jsonl`, `r1-q30.jsonl`] :

| | reel GSS 2024 | Qwen3-4B | gpt-oss-20b | Qwen3-30B-A3B |
|---|---|---|---|---|
| camp de gauche, journaliste | **5,5 %** | **65 %** | 17 % | 14 % |
| camp de droite, journaliste | **4,8 %** | **75 %** | 7 % | 5 % |

Les chiffres de `a46` sont reproduits exactement (65 a 75 pour cent chez `q4`, 17 pour cent
chez `oss20`).

**Le rang de l'erreur dit tout.** Sur les 149 items, `union1` est le **5e item le plus faux**
chez Qwen3-4B (TV 0,746) mais le **127e** chez Qwen3-30B-A3B (0,087) et le **129e** chez
gpt-oss-20b (0,109). [MESURE, `r1b-erreurs-par-item.csv`]

**Le test de generalite, chiffre.** Avec l'`alpha` median du modele a quatre modalites, la
regle generale de retrecissement predit, pour une realite a 5,5 pour cent :

| modele | `alpha` a K = 4 | part de syndiques predite par la regle generale | observee |
|---|---|---|---|
| Qwen3-4B | 0,115 | **44,9 %** | **65 %** |
| gpt-oss-20b | 0,523 | 26,7 % | **17 %** |
| Qwen3-30B-A3B | 0,764 | 16,0 % | **14 %** |

Et l'`alpha` de la cellule `union1` elle meme : Qwen3-4B **-0,069** a gauche et **-0,210** a
droite, c'est a dire une distribution **anti correlee** avec la realite ; gpt-oss-20b +0,77
et +0,96 ; Qwen3-30B-A3B +0,82 et +0,99, tous deux **au dessus de leur propre mediane**
(58e a 80e percentile de leurs items). [MESURE]

**Reponse.** Le defaut de taux de base est bien un **fait general** : la courbe d'etalonnage
le montre sur les 8 718 modalites du run, et elle explique la plus grande part du chiffre de
Qwen3-4B (5,5 pour cent de realite deviennent 45 pour cent par la seule regle generale du
modele, avant tout effet propre a l'item). **Mais son ampleur n'est pas generale** : elle est
une propriete du modele, et sur cet item precis les deux modeles plus gros sont **meilleurs
que leur propre regle**, pas pires. Les 60 a 75 pour cent de `a46` ne se citent donc pas
comme un fait sur « les modeles » ; ils se citent comme un fait sur Qwen3-4B, dont environ
les deux tiers relevent d'une regle generale de retrecissement et le reste d'un echec propre
a l'item. La phrase de `a46` « ce n'est pas de la fausse polarisation, c'est un defaut de
taux de base » est **confirmee sur le mecanisme et a restreindre sur le perimetre**. [MESURE]

---

## 4. Les cellules relancees exclues, et l'analyse de sensibilite

### 4.1 Le decompte, cellule par cellule

12 cellules sur 2 682 sortent des mesures, soit 0,45 pour cent. [MESURE,
`r1-par-cellule.csv`, colonne `motif_rejet`]

| modele | rejet de parse | recopie de l'exemple de relance | total | items concernes |
|---|---|---|---|---|
| Qwen3-4B | 0 | **11** | 11 | `income` (5), `attend` (2), `wlthwhts`, `wlthblks`, `wlthhsps` |
| Qwen3-30B-A3B | **1** | 0 | 1 | `attend`, somme a 90 |
| gpt-oss-20b | 0 | 0 | 0 | aucune relance du tout |

Les onze recopies sont **13 relances sur 894 cellules chez Qwen3-4B, dont 11 recopient**, soit
0,846 : le critere de chute 2 tombe et les cellules sortent, comme le preenregistrement le
prescrit. Toutes portent sur des items a **sept a douze modalites**.

**Aucun des cinq items concernes n'est dans les 79 items orientes de `a37`.** [MESURE]

### 4.2 Ce que les conclusions deviennent si on les garde

Recalcul complet de H1, H2a, H2b et H3 avec les onze cellules reintegrees ; la cellule de
rejet de parse ne peut pas etre reintegree, elle n'a pas de distribution valide.
[MESURE, `r1b-sensibilite-exclusions.csv`]

| | principal | sensibilite | ecart |
|---|---|---|---|
| H1, q4 gauche journaliste | 1,1741 | 1,1768 | +0,003 |
| H1, q4 centre journaliste | 1,1142 | 1,1222 | +0,008 |
| H1, q4 droite journaliste | 1,0594 | 1,0621 | +0,003 |
| H1, q4 gauche adversaire | 1,1809 | 1,1820 | +0,001 |
| H2a, q4 journaliste | 0,8944 | 0,8840 | -0,010 |
| H2a, q4 adversaire | 0,7710 | 0,7679 | -0,003 |
| **H2b, tous perimetres, tous modeles** | | | **0,000, exactement** |
| H3, q4 gauche | 3,0741 | 3,0191 | -0,055 |
| H3, q4 droite | 3,0915 | 3,0531 | -0,038 |
| **H4, les douze cellules** | | | **0,000, exactement** |

**Aucun verdict ne change, sur aucune hypothese.** Les deux hypotheses centrales sont
strictement insensibles : H2b et H4 ne portent que sur les 79 items orientes, dont aucun
item exclu ne fait partie ; l'egalite est exacte et non approchee.

**Et l'exclusion joue contre le resultat qu'elle sert.** Reintegrer les cellules recopiees
**augmente** les rapports de H1 (l'exemple de relance est presque uniforme, donc de
dispersion elevee) : le rejet de H1 dans la direction inverse serait legerement **plus fort**
si on les gardait. L'exclusion est donc conservatrice dans le bon sens. Sur H2a et H3 elle
joue dans l'autre sens, de trois a cinquante cinq millemes, ce qui ne deplace aucun
intervalle. [MESURE]

**Ce que cette analyse ne repare pas.** Elle ne dit rien de ce qu'aurait donne une invite de
relance sans exemple chiffre : les 11 cellules gardees sont des recopies, pas des reponses.
La question « que vaut la description de Qwen3-4B sur `income` et `attend` » reste sans
reponse, et c'est le prix de l'invite `r1-d1`. La correction, `A: <integer>` sans nombre,
demande de refaire les 2 682 appels, soit une heure de machine.

---

## 5. Ce que cela change a `MOONSHOTS.md` programme A

### 5.1 La troisieme issue, et pourquoi ce n'est pas « faux consensus »

`MOONSHOTS.md` prevoit deux issues : l'exageration, qui porte le programme, et l'archive
fidele, qui est le point d'arret du mois 1. Le journal de 00:30 en nomme une troisieme, la
**sous representation des ecarts**, sur la foi du seul Qwen3-4B. **Le run complet ne la
soutient pas non plus.** [MESURE]

- **Ce n'est pas l'exageration** : deux modeles sur trois ecrasent l'ecart entre camps, et
  les trois sur dispersent l'interieur des camps au lieu de l'unifier.
- **Ce n'est pas l'archive fidele** : les trois modeles sont a sept a onze fois le plancher
  humain en distance de variation totale, et leurs facteurs d'ecart vont de 0,18 a 1,32 avec
  des intervalles disjoints du plancher dans des directions opposees. Des archives seraient
  d'accord entre elles.
- **Ce n'est pas non plus la sous representation** : Qwen3-30B-A3B exagere, sur les deux
  quantites, les deux identites et les trois perimetres d'items.

L'issue reelle est une quatrieme : **la dispersion inter modeles depasse l'erreur de chacun**.
L'ecart entre le facteur le plus bas et le plus haut vaut 5,2 sur les 79 items orientes en
identite journaliste, 7,4 sur les 29 items a pole declare, et 13,2 si on laisse aussi varier
l'identite du demandeur. A l'interieur d'un seul modele, la variation de protocole vaut 14.
**La quantite est reelle, elle est grande, et elle n'a pas de valeur unique.** [MESURE]

C'est pourquoi je recommande, avec la question 1 du rapport de run, de rendre l'enonce du
programme A **neutre en direction** : « la fidelite de representation des camps » decrit les
trois modeles et reste auditable ; « la fausse polarisation fabriquee » ne decrit ni
Qwen3-4B ni gpt-oss-20b et serait dementie par le premier modele branche.

### 5.2 La phrase pour un regulateur

> Sur 149 questions d'opinion americaines dont la distribution reelle par camp politique est
> publiee, trois modeles ouverts de trois familles, interroges avec la meme invite au
> caractere pres et a temperature zero, decrivent tous les camps politiques comme plus varies
> qu'ils ne sont, adaptent tous le portrait qu'ils font d'un camp a l'identite de celui qui
> pose la question, dans une proportion de deux virgule sept a quatre virgule deux fois le
> bruit de reinterrogation d'un panel humain, et se contredisent entre eux sur l'ampleur de
> l'ecart entre les camps d'un facteur cinq, l'un l'ecrasant d'un facteur quatre et l'autre
> l'exagerant d'un quart. Sur un meme modele, changer de protocole d'interrogation deplace
> cette derniere quantite d'un facteur quatorze. La quantite est donc mesurable a cout nul,
> elle varie par modele et par version, et elle n'a pas de valeur de reference : c'est ce que
> l'obligation d'audit doit fixer, un protocole et un registre, avant de fixer un seuil.

Trois choses que cette phrase ne dit pas, et qu'il ne faut pas y ajouter : elle ne compare
pas les modeles aux humains de second ordre, faute des items ANES ; elle ne dit rien de
l'effet sur un lecteur ; elle ne porte que sur trois modeles ouverts petits, un pays et une
enquete.

### 5.3 Ce qu'il reste a tester

| | ce qui manque | cout | ce que ca decide |
|---|---|---|---|
| **le second terme humain** | les items de placement d'Ahler et Sood ; `a46` etablit qu'ils portent sur des **compositions** de camp, jamais sur des opinions, et que **deux items sur huit seulement** ont deja leur terme de modele dans R1 (`union1` et `reborn`) | run composition, 120 appels, trois modeles, file 4 a 08:05 | la version forte du programme A, « le modele exagere plus que les humains » ; en l'etat cette phrase reste **interdite** |
| **les compositions, run de 08:05** | six items sur huit n'ont aucun terme de modele | une demi heure de machine | si le defaut de taux de base tient sur des questions de composition posees directement, et si l'ecart entre `q4` et `oss20` d'un facteur quatre sur `dem_union` se generalise |
| **l'experience de lecture** | trois bras, 1 500 a 2 000 personnes, comite d'ethique, protocole d'Ahler et Sood | 15 000 a 30 000 euros, mois 6 | le seul etage causal ; rien dans R1 ne dit ce que lire une description fait a un lecteur |
| **l'incarnation sur les deux gros modeles** | aucun run C2 sur gpt-oss-20b ni sur Qwen3-30B-A3B ; R2 apporte une condition de type C3 sur gpt-oss-20b seulement | une nuit par modele | si le contraste des deux modes est une propriete de Qwen3-4B ou du champ |
| **un modele socle** | `Qwen3-4B-Base` est telecharge (`a3` 4.4) | une heure | separer « le modele a lu le GSS » de « le post entrainement fabrique le portrait » ; l'objection fatale reste entiere |
| **l'ordre des modalites** | une seule passe, ordre de nomenclature ; `a27` mesure que l'ordre seul porte 60 pour cent de l'effet de leur correctif | 2 682 appels de plus, une heure | la robustesse de tout ce qui precede |
| **une troisieme identite** | neutre mais non journalistique | 894 appels | si H3 mesure un effet d'identite ou un artefact d'invite |

### 5.4 L'honnetete

Ce qui est mesure l'est sur **trois modeles ouverts petits** (4, 20 et 30 milliards de
parametres, tous quantifies en 4 bits ou MXFP4), **un jeu d'items** (149 questions du GSS,
enquete tres presente dans les corpus d'entrainement), **un pays**, **une langue**, **une
formulation d'invite**, **un ordre de modalites**, **temperature 0**. Aucun modele
proprietaire, aucun modele de la taille de ceux que le public interroge. Le mode description
s'est revele **sensible a l'identite du demandeur** (H3, trois a quatre fois le plancher
humain, six cellules sur six) : la quantite mesuree n'est donc pas une propriete stable du
modele, elle depend d'une phrase de l'invite systeme. Enfin, **aucun controle de
contamination** n'est dans ce run : les deux Qwen n'ont pas de coupure publiee et celle de
gpt-oss-20b (juin 2024) est posterieure a toutes les vagues employees, si bien qu'aucun des
trois ne permet de trancher par la date la question « le modele recite t il le sondage
publie ».

---

## Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise.**

1. « Sur les 149 items du GSS, trois modeles ouverts decrivent tous les camps politiques
   comme plus varies qu'ils ne sont, de 1 a 18 pour cent, contre un plancher de
   reinterrogation humaine a 1,00. » [MESURE, 18 cellules, 15 significatives apres Holm]
2. « Le portrait qu'un modele fait d'un camp depend de qui le lui demande, de 2,7 a 4,2 fois
   le bruit de reinterrogation humaine, sur les trois modeles et les deux camps. » [MESURE]
3. « Sur l'ecart entre camps, les trois modeles se contredisent : facteurs de 0,25, 0,62 et
   1,27, intervalles disjoints du plancher humain dans des directions opposees. » [MESURE]
4. « A modele constant, quantification constante et temperature constante, sur les memes
   29 items et la meme quantite, le facteur d'amplification de Qwen3-4B va de 0,12 en
   description a 1,62 en incarnation etiquetee. » [MESURE, p de la difference appariee
   0,00025 et 0,00005]
5. « Les modeles gonflent les modalites rares et rabotent les modalites massives, avec un
   point fixe vers un tiers ; une modalite a moins de 1 pour cent reel recoit 11,9 pour cent
   en moyenne. » [MESURE, 8 718 modalites]
6. « L'exclusion des cellules qui recopient l'exemple de relance ne deplace aucune conclusion
   et joue contre le resultat qu'elle sert. » [MESURE, analyse de sensibilite complete]

**Interdit.**

1. **« Le modele exagere plus que les humains. »** Le second terme n'existe pas dans ce run.
   Interdit par la page de plan section 9, et rien ici ne le leve.
2. **« Les modeles sous representent les ecarts entre camps. »** Vrai sur Qwen3-4B et
   gpt-oss-20b, **faux sur Qwen3-30B-A3B**. La formulation de 00:30 doit etre corrigee
   partout ou elle a ete reprise.
3. **« Les modeles caricaturent le camp adverse pour plaire au demandeur. »** H3 mesure une
   distance, pas une direction, et la mesure de direction est nulle sur les six cellules
   apres Holm.
4. **« Les modeles aplatissent en description et caricaturent en incarnation. »** Le contraste
   n'existe que sur Qwen3-4B, et il confond le mode, l'unite simulee et la lecture.
5. **« H4 est confirmee sur les douze cellules. »** Dix sur douze ; les deux cellules de
   Qwen3-4B sur l'amplification sont a `p_holm` = 0,0700.
6. **Toute citation du facteur de r1 a cote du 1,62 de `a38` sans nommer le perimetre.**
   Le pont existe maintenant, mais il n'est valide que sur les 29 items a pole declare et
   avec le score de desirabilite de `a25`. Le 0,245 des 79 items et le 1,62 de `a38` restent
   incomparables chiffre a chiffre ; les valeurs comparables sont **0,179 contre 1,617**.
7. **Toute generalisation** hors du GSS, hors des Etats Unis, hors de ces trois modeles a
   cette quantification, hors de l'invite `r1-d1` et de l'ordre de nomenclature.

---

## Ce que cela change a `MOONSHOTS.md` et a `ARBITRAGE.md`

**`MOONSHOTS.md`, programme A.**

1. **L'enonce** : « la reponse est plus unanime et plus extreme que la realite » est faux sur
   le premier terme pour les trois modeles et depend du modele sur le second. A remplacer
   par un enonce neutre en direction, « la fidelite de representation des camps ».
2. **L'objection fatale** : « le modele recite le sondage publie et il est exact » est
   **affaiblie mais non levee**. Elle est affaiblie parce que trois archives seraient
   d'accord entre elles et ne le sont pas, et parce que l'erreur vaut sept a onze fois le
   plancher humain. Elle n'est pas levee parce qu'aucun controle de contamination n'est dans
   ce run et qu'aucune des trois coupures ne permet de trancher par la date. Le modele socle
   reste le test qui la leverait, pour une heure de machine.
3. **La raison de ne pas y croire** que `MOONSHOTS.md` invoque, « `a38` donne le facteur 1,62
   a modele constant sous etiquette », **est renforcee et precisee** : le contraste est
   maintenant mesure sur la meme quantite et les memes items, il vaut 0,179 contre 1,617, et
   il porte le programme mieux que le chiffre isole.
4. **Le point d'arret du mois 1**, « si les modeles n'exagerent pas plus que les humains sur
   les items apparies, l'experience est annulee », **n'est pas atteignable en l'etat** :
   il exige les items apparies, et `a46` montre que le jeu d'Ahler et Sood porte sur des
   compositions et couvre deux items sur huit dans R1. Le point d'arret doit etre reformule
   sur ce que le run de 08:05 rendra.
5. **La trajectoire** : le mois 3, « registre des versions de modeles », monte en priorite.
   Ce run montre que la quantite depend plus du modele et du protocole que du pays ou du
   sujet ; le registre n'est pas un accessoire du programme, c'en est le livrable.

**`ARBITRAGE.md`.** Le pari explicite etait : « si le mode description est une archive
fidele, A retombe en audit rassurant et B reprend la tete ». **Le mode description n'est pas
une archive fidele** : sept a onze fois le plancher humain, et trois modeles en desaccord.
Le pari est gagne au sens ou A ne retombe pas ; il l'est **plus faiblement que prevu** au
sens ou la piece qui porte le programme n'est plus « les machines caricaturent » mais « la
quantite n'a pas de valeur de reference et varie d'un facteur cinq a quatorze », ce qui est
un argument d'audit et pas un argument de titre. La recommandation de `MOONSHOTS.md` section
4, lancer les 149 appels et ecrire les trois demandes de donnees, tient sans changement : la
demande ANES devient le chemin critique, puisque c'est elle qui decide de la version forte.

---

## Ce que je n'ai pas pu verifier

1. **Le second terme humain.** Aucun item ANES dans ce run ; la comparaison a trois termes
   n'existe pas. Le run composition de 08:05 n'avait pas rendu a l'heure de cette lecture.
2. **La contamination.** Aucun controle. Les deux Qwen n'ont pas de coupure publiee ; celle
   de gpt-oss-20b est posterieure aux vagues employees. La question de l'archive reste
   entiere.
3. **L'incarnation sur gpt-oss-20b et Qwen3-30B-A3B.** N'existe pas. Le contraste des deux
   modes de la section 2 porte sur un seul modele.
4. **La part du mode dans le contraste C2 contre description.** Trois facteurs bougent
   ensemble, mode, unite simulee et lecture. C3 borne partiellement le probleme (0,523, sans
   etiquette, en incarnation) mais ne le resout pas. L'ablation propre est R3.
5. **L'ordre des modalites.** Une seule passe. `a27` mesure que l'ordre seul porte 60 pour
   cent de l'effet de leur correctif.
6. **Le niveau de raisonnement de gpt-oss-20b.** `Reasoning: low`, repris de `a3` sans
   balayage. gpt-oss-20b est aussi le modele qui donne le plus souvent la meme distribution
   aux deux camps (34,9 pour cent des items) ; je ne peux pas separer ce qui vient du
   gabarit harmony, du niveau de raisonnement et du modele.
7. **Le `alpha` de retrecissement.** Mesure nouvelle, non preenregistree, ajustee par moindres
   carres sans intervalle de confiance ni test. Elle est ici un outil de lecture du
   mecanisme, pas un resultat, et elle doit etre preenregistree si elle sert un jour de
   quantite publiee.
8. **Le contraste apparie des deux modes** repose sur une reconstruction item par item des
   ecarts de `a38` a partir de `a38-par-camp.csv` et
   `a38-desirabilite-humaine-par-camp.csv`. Les valeurs agregees reproduisent celles de
   `a38-camp.csv`, mais je n'ai pas rejoue les traces de `a5` elles memes.
9. **Les perimetres humains different entre les deux modes** : `a38` calcule C2 et C3 contre
   les 150 personnes du run `a5` (ecart humain 0,2219, plancher 0,984) et r1 contre les
   1 052 (ecart humain 0,2361, plancher 1,025). Les deux facteurs sont normalises chacun par
   son propre referent, ce qui rend la comparaison legitime, mais les deux referents ne sont
   pas le meme echantillon.
10. **La litterature.** Aucune recherche web. `a15`, `a27`, `a37`, `a38` et `a46` sont cites
    tels que ces rapports les citent.

---

## Questions ouvertes pour Simon

1. **Faut il un second nom pour le facteur de r1 ?** La reponse est maintenant chiffree : sur
   les 29 items a pole declare, la quantite de `a38` et la quantite de r1 sont **exactement la
   meme fonction** (ecart absolu 0,0). Le probleme n'est donc pas le nom de la quantite mais
   le nom du **perimetre** : 0,245 (79 items, position) et 0,179 (29 items, desirabilite)
   sont deux nombres du meme facteur sur deux jeux d'items. Je propose de publier le
   perimetre dans le nom, `facteur_29` et `facteur_79`, et de ne comparer a `a38` que le
   premier. Est ce la bonne convention ?

2. **L'absence de direction sur H3 est elle un resultat a publier ou un manque de puissance ?**
   Six cellules, 79 items, aucun signe qui survive a Holm, mais des intervalles qui
   contiennent des effets de 4 centiemes de l'echelle de position. Un effet de direction reel
   mais petit serait invisible ici. Faut il le declarer nul, ou declarer que le run ne
   tranche pas ?

3. **Le retrecissement vers l'uniforme doit il devenir une quantite du dossier ?** Il explique
   H1, il explique l'ordre des trois modeles, il explique le signal syndiques de `a46` aux
   deux tiers, et il se calcule sans un appel de plus sur toutes les traces existantes. Mais
   il n'est pas preenregistre, et le publier maintenant serait exactement le genre de
   quantite choisie apres avoir vu les donnees que `a44` et `a45` reprochent au dossier.
   Preenregistrer et rejouer, ou publier avec l'etiquette « exploratoire » ?

4. **Que fait on de la contradiction entre les trois modeles dans un texte pour un
   regulateur ?** Elle est le resultat le plus solide du run et le plus difficile a vendre :
   une autorite veut un seuil, et nous rendons une dispersion. Faut il porter d'abord H3, qui
   concorde sur les trois modeles et se raconte en une phrase (« la reponse depend de qui
   demande »), et garder H2 pour la partie technique ?

5. **Le run doit il etre refait sans exemple chiffre dans l'invite de relance ?** L'analyse de
   sensibilite dit que non pour les conclusions : aucun verdict ne bouge, H2b et H4 sont
   exactement identiques. Elle ne dit rien de ce que Qwen3-4B aurait repondu sur `income` et
   `attend`. Une heure de machine pour cinq items chez un modele : je penche desormais pour
   **ne pas refaire**, contrairement a la recommandation du rapport de run, et pour corriger
   l'invite dans le prochain protocole seulement.

6. **Le modele socle passe t il devant le run composition ?** Il coute une heure, il attaque
   l'objection fatale, et il est deja telecharge. Le run composition coute une demi heure et
   attaque le second terme. Les deux tiennent dans la meme matinee : l'ordre est il indifferent
   ou l'un conditionne t il l'autre ?

---

## Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim

# le contraste des deux modes et l'analyse de sensibilite
.venv/bin/python analyses/r1b_contraste_mode.py

# les erreurs par item, l'etalonnage du taux de base, la direction de H3, la figure
.venv/bin/python analyses/r1b_par_item.py
```

Sorties : `resultats/r1b-contraste-mode.csv`, `r1b-h2b-29-items.csv`,
`r1b-sensibilite-exclusions.csv`, `r1b-erreurs-par-item.csv`,
`r1b-etalonnage-taux-de-base.csv`, `r1b-direction-identite.csv`,
`r1b-contraste-apparie-modes.csv`, `r1b-figure-modes.png` et `.svg`.
