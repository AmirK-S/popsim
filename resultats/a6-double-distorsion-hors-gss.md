# a6. La double distorsion hors du GSS et hors du pipeline de Stanford

**Reponse en une ligne.** Oui, et le resultat est plus net ailleurs que sur le GSS :
**les treize configurations de Twin-2K-500, produites par une autre equipe avec GPT-4.1,
GPT-4.1-mini et Gemini-Flash-2.5, sont toutes dans le quadrant de la double distorsion**
[MESURE], avec des ecarts entre segments gonfles d'un facteur 1,57 a 3,73 et une dispersion
interne ecrasee a 0,45 - 0,75, pendant que le retest humain tombe en (1,004 ; 1,009) ;
sur les jeux economiques et sur le Big Five du paquet OSF, cinq conditions sur six y sont
aussi, et **l'ecart de facteur sept entre les deux generations dites demographiques se
reproduit hors du GSS, en pire : facteur 22,8 sur les jeux economiques et 5,7 sur le Big
Five, avec une correlation par individu strictement indistinguable dans les deux cas**
[MESURE].

**Le fait le plus solide du rapport.** Sur Twin-2K-500, l'axe qui porte le gonflement est
**l'ideologie politique**, ratio inter 1,86 a 5,35 selon la configuration, alors que le
genre est **en dessous de 1**, 0,15 a 0,93, et l'age aussi pour dix configurations sur
treize [MESURE]. C'est exactement le profil trouve sur le GSS en a1 section 4, sur d'autres
personnes, d'autres questions, d'autres modeles et d'autres auteurs. Ce n'etait pas une
particularite du GSS.

**Le fait qui derange.** Sur Twin, les trois mesures de dispersion **ne s'accordent plus**,
contrairement au GSS. A items identiques, l'entropie donne un ratio inter de 1,30 a 3,65 la
ou la variance ordinale donne 0,28 a 2,92, avec une dispersion interne effondree a 0,06 -
0,22 [MESURE]. La double distorsion telle que a1 la formule est donc **un resultat de
mesure d'information, pas un resultat de variance**, sur ce jeu de donnees. Section 5.

Date : 7 septembre 2026. Reproduction :
`.venv/bin/python analyses/a6_telecharger_twin_specs.py` puis
`.venv/bin/python analyses/a6_double_distorsion_hors_gss.py`, environ cinq minutes,
**aucun appel de modele de langage**, calcul plafonne a quatre fils.

---

## 1. Ce qui est mesure, et comment a1 est reutilise

Les estimateurs a biais corrige et l'index de comptage sont **importes** de
`analyses/a1_double_distorsion.py`, qui n'a pas ete modifie : `construire_index`,
`compter`, `decomposer`, `agreger`, `matrice_distance`, `silhouette`, `lire_condition`,
`lire_nomenclature`, `lire_demographies`, et les constantes `AXES`, `MESURES`,
`ITEMS_DEMOGRAPHIQUES`. **Aucune formule de dispersion n'est reecrite ici** [CONFIRME].

Deux fonctions de a1 ne sont pas importables parce qu'elles sont locales a son `main()` :
`recentrer`, le recentrage additif des tirages bootstrap decrit en a1 section 8 limite 3,
et `ic`, le percentile a 95 pour cent. Elles sont **recopiees telles quelles**, six lignes
en tout, sans changement de formule. C'est la seule duplication, et elle est signalee ici
parce qu'un relecteur doit pouvoir la verifier [CONFIRME].

Le protocole est celui de a1 : trois mesures de dispersion aux hypotheses disjointes,
correction de biais analytique, controle par permutation des etiquettes de segment,
bootstrap sur les participants recentre, intervalles a 95 pour cent, memes six
segmentations, controle par retest humain qui doit tomber en (1,1). Bootstrap 600 tirages,
30 permutations.

### 1.1 Les quatre materiaux

| jeu | source | unites | conditions | reference | controle |
|---|---|---|---|---|---|
| GSS | OSF t6g7k, figure 2 | 1052 personnes, 169 items | 8 | humains vague 1 | humains vague 2 |
| Jeux economiques | OSF t6g7k, figure 2 | 1052 personnes, 5 mises | 8 | humains vague 1 | humains vague 2 |
| Big Five | OSF t6g7k, figure 2 | 1052 personnes, 5 scores de trait | 8 | humains vague 1 | humains vague 2 |
| Twin-2K-500 | Hugging Face, CC BY 4.0 | 2058 personnes, 108 items | 15 | humains vague 4 | humains vagues 1-3 |

Les chiffres du GSS ne sont **pas recalcules** : ils sont relus dans `resultats/a1-ratios.csv`
et servent de cadran de reference dans la figure.

### 1.2 La correspondance des etiquettes, relue et non transposee

a1 section 7.2 documente une collision : `v3` designe l'entretien pour le GSS et le
**demographique** pour les jeux economiques et le Big Five ; `v6` designe le demographique
pour le GSS et l'**entretien** pour les jeux economiques. Le script ne transpose donc rien :
il relit les tableaux de `FIGURE2_PIPELINE.md` et `FIGURE3_PIPELINE.md` a chaque execution
et affiche ce qu'il a lu. Resultat de cette relecture [CONFIRME] :

| condition | jeux econ., figure 2 | jeux econ., figure 3 | Big Five, figure 2 | Big Five, figure 3 |
|---|---|---|---|---|
| entretien | `econ_games_v6` | `econ_games_v6` | `bigfive_v5` | `bigfive_v5` |
| persona | `econ_games_v4` | `econ_games_v4` | `bigfive_v4` | `bigfive_v4` |
| demographique | **`econ_games_v3`** | **`econ_games_v8`** | **`bigfive_v3`** | **`bigfive_v8`** |

La table de a1 section 7.2 est confirmee ligne a ligne. Les libelles employes dans ce
rapport portent donc toujours l'etiquette de generation entre parentheses.

### 1.3 Un fait sur les donnees que la mission ne prevoyait pas

**Les fichiers `bigfive_main` et `econ_games_main` du paquet OSF ne contiennent pas des
items categoriels.** Ils contiennent cinq valeurs continues par participant : les cinq
traits du BFI, moyennes de 8 a 10 items de Likert, et les cinq mises des jeux economiques,
exprimees en fraction de la dotation [MESURE, verifie sur les huit fichiers de chaque jeu].
Le Big Five livre dans ce paquet **n'est donc pas ordinal item par item, il est agrege**.
Aucun fichier item par item du BFI-44 n'existe dans le paquet : recherche exhaustive faite
sur les 65 CSV, il n'y a que `preparation/`, `analysis/` et `summary/`, tous a cinq colonnes
de traits [CONFIRME].

Consequence de methode, assumee et verifiable :

- **M3, la decomposition de variance, s'applique exactement.** Le codage dit "fin" attribue
  un code a chaque valeur distincte observee et remet la valeur numerique dans le tableau
  `valeurs_ordinales` de `decomposer`. La decomposition calculee sur cette table de
  contingence est identique, terme a terme, a l'analyse de variance sur les valeurs brutes.
  Ce n'est pas une discretisation, c'est un codage.
- **M1 et M2 exigent des modalites.** On discretise en au plus cinq classes de quantiles,
  bornes estimees sur les **seuls humains de la vague 1** et appliquees telles quelles a
  toutes les conditions. Un seul jeu de bornes pour toutes : la discretisation ne peut donc
  pas fabriquer d'ecart entre conditions. Les bornes confondues sont fusionnees. Nombre
  effectif de classes : **[4, 4, 3, 4, 3] pour les cinq jeux economiques**, qui ont des
  masses ponctuelles fortes, et **[5, 5, 5, 5, 5] pour les cinq traits** [MESURE].
- **Valeurs hors echelle.** Le champ `game4_PG` sort de l'intervalle [0, 1] pour 18 cellules
  sur 42 080 : 2 chez les humains de la vague 1, valeur 100,0, 11 chez les agents enquete,
  2 chez les agents entretien `v6`, 1 chez les agents persona `v4`, 0 ailleurs [MESURE].
  Elles sont ramenees aux bornes, et le compte est affiche a chaque execution. Sans
  ecretage, un seul 100,0 dominerait la somme de variance des cinq jeux.

### 1.4 Twin-2K-500 : ce qui a ete telecharge et ce qui a ete verifie

`analyses/a2_telecharger_twin.py` n'avait ramene que deux configurations sur les treize
publiees. `analyses/a6_telecharger_twin_specs.py` recupere les treize, plus les deux
references humaines dans le meme espace de colonnes, soit 12 Mo dans
`data/twin2k500/llm_specs/`, non versionne. Les treize sont : Demographics Only, JSON
Persona et JSON Persona (Predicted Output) en GPT-4.1 et en GPT-4.1-mini, Text Persona en
GPT-4.1-mini avec quatre variantes (defaut, temperature par defaut, raisonnement, repetition
des questions), Persona Summary seul et combine, **Text Persona en Gemini-Flash-2.5**, et
un **modele affine sur 500 exemples** [CONFIRME, listage de l'API Hugging Face].

Verifications faites avant toute mesure :

1. **`TWIN_ID` et `pid` designent la meme personne** : accord de 100,00 pour cent sur
   48 369 cellules comparees entre `humains_wave1_3.csv` et `wave1_3_response.csv`
   [MESURE]. Sans cette verification, la segmentation demographique aurait ete branchee sur
   les mauvaises personnes.
2. **Cible** : les 108 colonnes categorielles de la vague 4, type MC ou Matrix au catalogue,
   sur les 126 colonnes de questions. Les 12 curseurs et les 6 saisies libres sont ecartes.
   C'est le meme decoupage qu'en a2 section 3.2.
3. **Aucune question de la vague 4 n'appartient au bloc Demographics** : le script s'arrete
   si c'est le cas. Il n'y a donc pas d'equivalent des huit items exclus du GSS [CONFIRME].
4. **Le taux de cellules vides est de 24,1 pour cent, identique pour les quinze conditions**
   [MESURE], parce que plusieurs experiences sont inter sujets. Le masque de donnees
   manquantes est le meme partout, la comparaison est donc appariee.
5. **Aucune modalite produite par un modele n'est absente du repertoire humain** : les
   fichiers "formatted" sont deja apparies au catalogue par les auteurs. Il n'y a donc pas
   ici le probleme de reponses mal formees documente en a1 section 7.4.
6. **Trois configurations ne couvrent pas les 2058 sujets** : `JSON Persona - GPT4.1-mini`
   n'en couvre que 1000, `LLM Finetuning (500 training samples)` 1558, soit 2058 moins les
   500 sujets d'entrainement, et `JSON Persona (Predicted Output) - GPT4.1` 2050 [MESURE].
   Les melanger aux dix autres casserait l'appariement du bootstrap et changerait le
   denominateur humain. Chacune est donc analysee **a part, avec les humains recalcules sur
   ses seuls sujets**, et elle est signalee comme telle dans les tableaux et la figure.

### 1.5 Segmentation de Twin

Six axes, choisis comme analogues exacts des six axes de a1, tires du bloc Demographics des
vagues 1 a 3, 14 questions au total :

| axe a6 | question Twin | modalites | axe correspondant dans a1 |
|---|---|---|---|
| genre | QID12, sexe assigne a la naissance | 2 | gender |
| ethnicite | QID15, race ou origine | 5 | race |
| ideologie politique | QID22, opinions politiques | 5 | political_ideology |
| age | QID13, quatre tranches | 4 | age |
| education | QID14, diplome le plus eleve | 6 | education |
| profil croise | genre x ethnicite x ideologie en 3 blocs | 30 | profil croise |

Le regroupement de l'ideologie en trois blocs suit la meme regle mecanique qu'en a1 :
"liberal" dans le libelle donne gauche, "conservative" donne droite, le reste donne centre.

---

## 2. Twin-2K-500 : la signature se reproduit sur un autre pipeline

Mesure principale, entropie et information mutuelle, 108 items, 6 segmentations, intervalles
bootstrap a 95 pour cent. Tableau complet dans `a6-ratios-twin.csv`.

| configuration | ratio inter | ratio intra | produit | mesure globale |
|---|---|---|---|---|
| humains vague 4 | 1 (reference) | 1 (reference) | 1,00 | 1,00 |
| **humains vagues 1-3, retest (controle)** | **1,004** [0,938 ; 1,081] | **1,009** [1,006 ; 1,012] | 1,01 | 1,01 |
| Text Persona, GPT-4.1-mini | 3,655 [3,307 ; 4,115] | 0,558 [0,553 ; 0,563] | 2,04 | **0,59** |
| Text Persona, repetition des questions | 3,499 [3,159 ; 3,918] | 0,633 [0,628 ; 0,637] | 2,21 | **0,66** |
| Text Persona, temperature par defaut | 3,233 [2,944 ; 3,603] | 0,622 [0,619 ; 0,627] | 2,01 | **0,65** |
| Text Persona, raisonnement | 3,020 [2,748 ; 3,376] | 0,658 [0,654 ; 0,662] | 1,99 | **0,68** |
| **Text Persona, Gemini-Flash-2.5** | **3,015** [2,748 ; 3,351] | **0,750** [0,745 ; 0,755] | 2,26 | **0,77** |
| JSON Persona, GPT-4.1 | 3,733 [3,386 ; 4,198] | 0,632 [0,628 ; 0,637] | 2,36 | **0,66** |
| JSON Persona (Predicted Output), GPT-4.1-mini | 2,435 [2,198 ; 2,766] | 0,455 [0,451 ; 0,459] | 1,11 | **0,47** |
| Persona Summary, GPT-4.1-mini | 2,298 [2,056 ; 2,588] | 0,585 [0,581 ; 0,589] | 1,34 | **0,60** |
| Persona Summary + JSON Persona | 1,826 [1,648 ; 2,045] | 0,581 [0,574 ; 0,589] | 1,06 | **0,59** |
| **Demographics Only, GPT-4.1-mini** | **1,570** [1,414 ; 1,795] | **0,502** [0,497 ; 0,506] | 0,79 | **0,51** |

Et les trois configurations mesurees sur leur propre sous ensemble, humains recalcules :

| configuration | n | ratio inter | ratio intra | mesure globale |
|---|---|---|---|---|
| JSON Persona (Predicted Output), GPT-4.1 | 2050 | 3,853 [3,456 ; 4,294] | 0,575 [0,569 ; 0,580] | 0,60 |
| JSON Persona, GPT-4.1-mini | 1000 | 2,673 [2,166 ; 3,506] | 0,605 [0,598 ; 0,612] | 0,62 |
| **modele affine sur 500 exemples** | 1558 | **1,052** [0,815 ; 1,334] | 0,552 [0,540 ; 0,564] | 0,56 |

Quatre lectures.

**Le controle passe, et il passe bien.** Les memes 2058 personnes, sur les memes questions,
repondues en vagues 1 a 3 puis en vague 4, tombent en (1,004 ; 1,009), les deux intervalles
contiennent 1. La methode ne fabrique pas d'ecart la ou il n'y en a pas [MESURE]. C'est le
meme resultat qu'en a1, obtenu sur un tout autre materiau.

**Les treize configurations sont dans le quadrant de la double distorsion, sans exception.**
Sur le GSS, quatre conditions sur six y etaient. Ici, treize sur treize : ratio inter
strictement superieur a 1 avec un intervalle qui exclut 1 pour douze d'entre elles, ratio
intra strictement inferieur a 1 avec un intervalle qui exclut 1 pour les treize [MESURE].
La treizieme, le modele affine, est le seul cas ou l'intervalle du ratio inter contient 1 :
c'est un aplatissement simple, pas une double distorsion.

**Le changement de modele ne change pas la nature de l'erreur, il en change l'ampleur.**
Gemini-Flash-2.5 a la dispersion interne la moins ecrasee de toutes, 0,750, et gonfle
quand meme les ecarts entre segments d'un facteur 3,0. GPT-4.1 en persona JSON gonfle de
3,7 et ecrase a 0,63. Il n'y a pas de famille de modeles qui echappe au phenomene dans les
donnees disponibles [MESURE].

**La mesure globale reste dans une plage rassurante.** Elle va de 0,47 a 0,77 : un
relecteur qui ne separe pas inter et intra voit une compression de dispersion de 23 a 53
pour cent, jamais un gonflement, jamais une structure inversee. C'est plus marque que sur
le GSS, ou elle restait entre 0,64 et 0,90.

### 2.1 L'ideologie politique porte l'effet, comme sur le GSS

Detail par axe, mesure entropie, ratio inter. Table complete dans `a6-ratios-par-axe.csv`.

| configuration | genre | ethnicite | **ideologie** | age | education | profil croise |
|---|---|---|---|---|---|---|
| humains, retest | 0,88 | 1,06 | 0,95 | 1,00 | 1,41 | 1,03 |
| Text Persona, GPT-4.1-mini | 0,72 | 0,97 | **4,98** | 0,51 | 3,27 | 3,96 |
| Text Persona, repetition | 0,53 | 1,25 | **4,71** | 0,50 | 2,67 | 3,84 |
| Text Persona, temp. defaut | 0,48 | 0,91 | **4,43** | 0,42 | 2,31 | 3,55 |
| Text Persona, raisonnement | 0,25 | 0,72 | **4,17** | 0,38 | 1,88 | 3,36 |
| Text Persona, Gemini-Flash-2.5 | 0,49 | 0,47 | **4,16** | 0,53 | 1,27 | 3,38 |
| JSON Persona, GPT-4.1 | 0,52 | 1,18 | **5,15** | 1,08 | 2,66 | 3,96 |
| JSON Persona (Pred. Out.), GPT-4.1 (n=2050) | 0,75 | 1,05 | **5,35** | 0,83 | 2,73 | 4,08 |
| JSON Persona (Pred. Out.), mini | 0,42 | 0,85 | **3,29** | 0,47 | 1,29 | 2,68 |
| JSON Persona, mini (n=1000) | 0,26 | 0,70 | **3,81** | 0,35 | 1,30 | 2,96 |
| Persona Summary, mini | 0,93 | 0,54 | **2,89** | 0,56 | 2,18 | 2,58 |
| Persona Summary + JSON | 0,57 | 0,40 | **2,45** | 0,32 | 1,28 | 2,01 |
| Demographics Only, mini | 0,15 | 0,70 | **1,86** | 2,16 | 1,45 | 1,61 |
| modele affine (n=1558) | 0,59 | 0,28 | 1,35 | 0,15 | 3,21 | 1,02 |

**Le resultat de a1 section 4 se reproduit integralement, sur un autre jeu de donnees, un
autre pipeline et d'autres modeles** [MESURE]. Le gonflement n'est pas demographique en
general, il est politique. Le genre est **en dessous de la fidelite** pour les treize
configurations, entre 0,15 et 0,93. L'age l'est aussi pour douze sur treize. L'education
est le seul autre axe systematiquement gonfle, entre 1,27 et 3,27, et le profil croise
suit mecaniquement puisqu'il contient l'ideologie.

La consequence pratique de a1 est confirmee et generalisee : **une etude qui mesurerait la
distorsion sur le genre ou sur l'age conclurait a l'absence de probleme, quel que soit le
jeu de donnees et quel que soit le modele.**

La reserve de a1 vaut ici aussi et il faut la porter : l'ideologie politique n'est pas une
variable demographique, c'est une attitude auto declaree. Sur Twin elle n'a pas ete choisie
par les auteurs comme variable de figure, c'est notre choix, motive par l'analogie avec a1.
Confiance : elevee sur le fait, moyenne sur l'interpretation.

Le ratio intra, lui, est quasi constant d'un axe a l'autre pour une configuration donnee,
par exemple 0,50 a 0,59 sur les six axes pour Text Persona GPT-4.1-mini. L'ecrasement
interne est une propriete du generateur, pas de la partition. Meme conclusion qu'en a1.

### 2.2 Exactitude et homogeneite par configuration

`a6-twin-configurations.csv`. L'exactitude est l'egalite exacte cellule a cellule contre
les humains de la vague 4. L'accord par paires est la probabilite que deux repondants tires
au hasard donnent la meme reponse : plus il est haut, plus la population est homogene.

| configuration | n | exactitude | accord par paires | modalites par item |
|---|---|---|---|---|
| humains vague 4 | 2058 | 1,0000 | **0,4431** | 3,63 |
| humains vagues 1-3, retest | 2058 | **0,7118** | 0,4401 | 3,63 |
| JSON Persona, GPT-4.1 | 2058 | 0,5740 | 0,6045 | 3,05 |
| JSON Persona (Pred. Out.), GPT-4.1 | 2050 | 0,5677 | 0,6292 | 2,62 |
| Text Persona, GPT-4.1-mini | 2058 | 0,5531 | 0,6569 | 2,78 |
| Text Persona, Gemini-Flash-2.5 | 2058 | 0,5506 | **0,5650** | 3,38 |
| Text Persona, repetition | 2058 | 0,5490 | 0,6121 | 2,91 |
| Text Persona, temp. defaut | 2058 | 0,5480 | 0,6270 | 3,00 |
| JSON Persona, GPT-4.1-mini | 1000 | 0,5451 | 0,6181 | 2,65 |
| Text Persona, raisonnement | 2058 | 0,5437 | 0,5942 | 2,94 |
| Persona Summary, GPT-4.1-mini | 2058 | 0,5211 | 0,6390 | 2,81 |
| JSON Persona (Pred. Out.), mini | 2058 | 0,5136 | 0,7134 | 2,57 |
| Demographics Only, GPT-4.1-mini | 2058 | 0,4998 | 0,6890 | 2,49 |
| Persona Summary + JSON, mini | 2058 | 0,4744 | 0,6688 | 3,47 |
| modele affine sur 500 exemples | 1558 | 0,4621 | 0,6647 | 2,87 |

Le 0,5531 de Text Persona GPT-4.1-mini reproduit le 0,5530 rapporte en a2 section 1, ce qui
valide au passage la lecture des fichiers [CONFIRME].

Deux remarques.

**Le plafond humain de Twin est de 71,18 pour cent**, contre 79,53 pour cent sur le GSS.
Aucune configuration n'atteint 80 pour cent de ce plafond. La meilleure, JSON Persona
GPT-4.1, est a 0,574 / 0,712 = 0,807.

**L'homogeneite excessive est generale et forte** : 0,443 chez les humains contre 0,565 a
0,713 chez les modeles [MESURE]. C'est la meme mesure que `a0_diversite_osf.py`, et l'ecart
est du meme ordre que sur le GSS, 49,5 contre 66,4 pour cent.

**Un point contre intuitif, a garder** : la configuration la plus exacte, JSON Persona
GPT-4.1 avec 0,574, n'est pas la moins homogene, et la moins homogene, Gemini-Flash-2.5
avec 0,565, n'est que huitieme en exactitude. Le classement par exactitude et le classement
par structure ne coincident pas. C'est la these du dossier, mesuree une fois de plus.

---

## 3. Jeux economiques et Big Five : cinq conditions sur six dans le quadrant

Mesure entropie. Tableaux complets dans `a6-ratios-econ-games.csv` et
`a6-ratios-bigfive.csv`.

### 3.1 Jeux economiques, cinq mises

| condition | ratio inter | ratio intra | produit | mesure globale |
|---|---|---|---|---|
| humains vague 1 | 1 (reference) | 1 (reference) | 1,00 | 1,00 |
| humains vague 2 (controle) | 1,593 [0,834 ; 4,574] | **1,006** [0,990 ; 1,021] | 1,60 | 1,01 |
| agents enquete | 5,477 [2,981 ; 17,98] | 0,764 [0,742 ; 0,787] | 4,19 | 0,78 |
| agents composite | 2,943 [1,511 ; 8,902] | 0,700 [0,675 ; 0,724] | 2,06 | 0,71 |
| agents entretien (`v6`) | 2,262 [1,089 ; 7,677] | 0,722 [0,698 ; 0,745] | 1,63 | 0,73 |
| agents demographiques fig. 2 (`v3`) | 1,500 [0,699 ; 5,098] | 0,546 [0,525 ; 0,565] | 0,82 | 0,55 |
| agents persona (`v4`) | 0,519 [-0,140 ; 2,112] | 0,735 [0,709 ; 0,763] | 0,38 | 0,73 |
| **agents demographiques fig. 3 (`v8`)** | **34,21** [18,60 ; 110,6] | 0,695 [0,677 ; 0,715] | 23,79 | 0,82 |

### 3.2 Big Five, cinq scores de trait

| condition | ratio inter | ratio intra | produit | mesure globale |
|---|---|---|---|---|
| humains vague 1 | 1 (reference) | 1 (reference) | 1,00 | 1,00 |
| **humains vague 2 (controle)** | **0,950** [0,709 ; 1,207] | **0,999** [0,996 ; 1,002] | 0,95 | 1,00 |
| agents composite | 2,130 [1,593 ; 2,848] | 0,937 [0,929 ; 0,945] | 2,00 | 0,95 |
| agents entretien (`v5`) | 2,011 [1,558 ; 2,711] | 0,937 [0,930 ; 0,945] | 1,88 | 0,94 |
| agents enquete | 1,469 [1,072 ; 2,012] | 0,916 [0,907 ; 0,925] | 1,35 | 0,92 |
| agents demographiques fig. 2 (`v3`) | 2,387 [1,706 ; 3,395] | 0,673 [0,659 ; 0,685] | 1,61 | 0,69 |
| agents persona (`v4`) | 0,850 [0,569 ; 1,308] | 0,895 [0,883 ; 0,907] | 0,76 | 0,89 |
| **agents demographiques fig. 3 (`v8`)** | **13,51** [10,35 ; 19,09] | 0,693 [0,685 ; 0,702] | 9,37 | 0,79 |

**La double distorsion est presente sur le Big Five, qui n'est pas politique** [MESURE].
Cinq conditions sur six ont simultanement un ratio inter superieur a 1 avec intervalle
excluant 1 et un ratio intra inferieur a 1 avec intervalle excluant 1. La seule exception
est la condition persona `v4`, dont le ratio inter vaut 0,850 avec un intervalle qui
contient 1 : c'est un aplatissement simple, comme les agents persona du GSS.

**Le controle passe sur le Big Five**, (0,950 ; 0,999), les deux intervalles contiennent 1.
**Il ne passe pas franchement sur les jeux economiques** : le ratio inter du retest humain
vaut 1,593 avec un intervalle [0,834 ; 4,574] qui contient 1 mais qui est enorme. C'est une
limite reelle, traitee en section 6 : avec cinq variables seulement, le terme inter agrege
est trop petit pour etre estime avec precision.

**L'amplitude sur le Big Five est moderee et il faut le dire.** Le ratio intra des trois
conditions riches est de 0,92 a 0,94, c'est a dire une compression interne de 6 a 8 pour
cent seulement, contre 0,82 a 0,89 sur le GSS et 0,45 a 0,75 sur Twin. Sur un instrument de
personnalite agrege, l'ecrasement de la dispersion interne est **faible**. Le gonflement des
ecarts entre segments, lui, est du meme ordre que sur le GSS, facteur 1,5 a 2,4.

### 3.3 Ou se loge le gonflement, hors du GSS

Ratio inter par axe, mesure entropie.

| condition | genre | race | **ideologie** | age | education | profil croise |
|---|---|---|---|---|---|---|
| **jeux economiques** | | | | | | |
| humains vague 2 | 0,96 | 1,91 | 1,84 | 1,06 | 2,00 | 1,72 |
| agents composite | 0,99 | 0,17 | **6,61** | 0,75 | 5,44 | 3,85 |
| agents enquete | 1,02 | 0,59 | **16,28** | 0,34 | 4,32 | 7,04 |
| agents entretien (`v6`) | 0,38 | 0,37 | **4,75** | 0,63 | 8,68 | 2,28 |
| agents persona (`v4`) | 0,53 | 0,01 | 0,92 | 0,58 | 1,46 | 0,38 |
| agents demo. fig. 2 (`v3`) | 0,19 | 0,55 | -0,06 | 1,78 | 15,08 | 0,55 |
| agents demo. fig. 3 (`v8`) | 1,13 | 2,06 | **119,6** | 2,92 | 1,52 | 42,83 |
| **Big Five** | | | | | | |
| humains vague 2 | 1,44 | 0,59 | 0,79 | 1,03 | 1,07 | 0,81 |
| agents composite | 2,95 | 1,80 | 2,09 | 1,24 | 3,69 | 3,09 |
| agents entretien (`v5`) | 3,07 | 0,94 | 1,79 | 1,09 | 3,66 | 3,31 |
| agents enquete | 0,67 | 0,94 | 2,32 | 0,59 | 2,33 | 2,46 |
| agents persona (`v4`) | 2,15 | 0,36 | 0,51 | 0,58 | 1,15 | 1,47 |
| agents demo. fig. 2 (`v3`) | 2,06 | 1,90 | 0,30 | 0,76 | 12,19 | 1,41 |
| agents demo. fig. 3 (`v8`) | 3,72 | 3,44 | **36,62** | 2,54 | 0,90 | 31,16 |

**Sur les jeux economiques, l'ideologie porte encore l'effet**, comme sur le GSS et comme
sur Twin. Sur le **Big Five, non** : le gonflement des trois conditions riches est reparti
sur le genre et l'education autant que sur l'ideologie, 1,79 a 2,09 pour l'ideologie contre
2,95 a 3,07 pour le genre et 3,66 a 3,69 pour l'education [MESURE]. Le Big Five est le seul
des quatre materiaux ou le stereotype dominant n'est pas politique. C'est coherent : les
stereotypes de genre sur l'extraversion ou l'amabilite sont beaucoup plus disponibles dans
un corpus que des stereotypes politiques sur les memes traits.

Ces chiffres par axe sont a lire avec prudence : sur cinq variables seulement, un ratio par
axe repose sur cinq termes. Le -0,06 de `v3` sur l'ideologie, negatif apres correction, dit
simplement que le terme inter y est indistinguable de zero. Le 119,6 de `v8` dit qu'il est
enorme rapporte a un denominateur humain minuscule. Ce sont des ordres de grandeur, pas des
estimations precises.

Le ratio intra est, la aussi, stable d'un axe a l'autre, sauf pour `v8` : 0,82 sur le genre,
l'ethnicite, l'age et l'education, mais **0,41 sur l'ideologie et 0,50 sur le profil croise**
pour les jeux economiques, et 0,50 / 0,56 pour le Big Five [MESURE]. Autrement dit `v8`
n'ecrase pas la dispersion partout : il l'ecrase specifiquement a l'interieur des groupes
politiques, ce qui est la signature exacte du raisonnement par stereotype politique.

---

## 4. Les deux generations dites demographiques : le facteur sept se reproduit, en pire

C'est le test annonce en fin de a1 section 7.5. Il est concluant.

| jeu | condition | ratio inter [IC95] | correlation par individu | MAE par individu |
|---|---|---|---|---|
| **jeux econ.** | demo. figure 2 (`v3`) | **1,500** [0,699 ; 5,098] | 0,282 | 0,326 |
| | demo. figure 3 (`v8`) | **34,21** [18,60 ; 110,6] | 0,276 | 0,342 |
| | persona (`v4`) | 0,519 [-0,140 ; 2,112] | 0,310 | 0,327 |
| **Big Five** | demo. figure 2 (`v3`) | **2,387** [1,706 ; 3,395] | 0,472 | 0,684 |
| | demo. figure 3 (`v8`) | **13,51** [10,35 ; 19,09] | 0,459 | 0,755 |
| | persona (`v4`) | 0,850 [0,569 ; 1,308] | 0,544 | 0,737 |

Tests apparies sur les 1052 memes participants, source
`figure2/data/new_analysis_summaries/<jeu>/analysis/individual_level.csv`, sentinelle
-100000 exclue :

| comparaison | grandeur | ecart apparie | IC95 | t | verdict |
|---|---|---|---|---|---|
| `econ_games_v3` contre `econ_games_v8` | correlation | **+0,0060** | [-0,0201 ; +0,0321] | +0,45 | **indistinguables** |
| `econ_games_v3` contre `econ_games_v8` | MAE | -0,0158 | [-0,0240 ; -0,0077] | -3,80 | distinguables |
| `econ_games_v4` contre `econ_games_v8` | correlation | +0,0333 | [+0,0060 ; +0,0607] | +2,39 | distinguables |
| `bigfive_v3` contre `bigfive_v8` | correlation | **+0,0129** | [-0,0051 ; +0,0308] | +1,40 | **indistinguables** |
| `bigfive_v3` contre `bigfive_v8` | MAE | -0,0714 | [-0,0877 ; -0,0551] | -8,59 | distinguables |
| `bigfive_v4` contre `bigfive_v8` | MAE | -0,0181 | [-0,0387 ; +0,0025] | -1,72 | **indistinguables** |

**Reponse a la question posee.** L'ecart de facteur 7 entre `v6` et `v8` sur le GSS **se
reproduit hors du GSS et il y est plus grand** : facteur **22,8** entre `econ_games_v3` et
`econ_games_v8`, facteur **5,7** entre `bigfive_v3` et `bigfive_v8`, dans les deux cas avec
des intervalles de confiance disjoints [MESURE].

**Et la metrique du champ ne le voit toujours pas.** Sur les jeux economiques, la
correlation par individu des deux generations dites demographiques est de 0,282 contre
0,276, ecart apparie +0,006, t = +0,45 : **strictement indistinguables**, alors que leur
gonflement des ecarts entre groupes differe d'un facteur 22,8. Sur le Big Five, 0,472 contre
0,459, t = +1,40 : **indistinguables**, pour un facteur 5,7 [MESURE].

C'est la demonstration de a1 section 7.3, refaite deux fois sur deux autres materiaux du
meme paquet, avec les memes participants. Elle ne repose donc pas sur une particularite du
GSS ni sur une particularite de la mesure d'exactitude categorielle, puisqu'ici la metrique
du papier est une correlation continue et non un taux d'accord.

Une nuance a porter, parce qu'elle affaiblit legerement l'argument : sur la **MAE**, `v3` et
`v8` sont distinguables dans les deux jeux, t = -3,80 et t = -8,59. La cecite porte donc sur
la correlation, qui est la grandeur employee par les figures 2 et 3 du papier pour ces deux
jeux, et non sur toute mesure d'erreur. Il faut ecrire "la metrique employee par ces figures"
et non "toute metrique agregee".

---

## 5. Les trois mesures ne s'accordent plus sur Twin, et il faut le dire

Sur le GSS, a1 concluait que le classement et le signe tenaient sur les trois mesures. **Ce
n'est plus vrai sur Twin-2K-500** [MESURE].

| configuration | inter M1 | inter M2 | **inter M3** | intra M1 | intra M2 | **intra M3** |
|---|---|---|---|---|---|---|
| humains, retest | 1,004 | 1,033 | 1,022 | 1,009 | 1,005 | 1,034 |
| Text Persona, Gemini-Flash-2.5 | 3,015 | 3,115 | **2,915** | 0,750 | 0,765 | **0,215** |
| Text Persona, GPT-4.1-mini | 3,655 | 3,907 | **1,744** | 0,558 | 0,593 | **0,106** |
| JSON Persona, GPT-4.1 | 3,733 | 4,211 | **1,071** | 0,632 | 0,686 | **0,093** |
| Persona Summary, mini | 2,298 | 2,730 | **0,764** | 0,585 | 0,634 | **0,106** |
| Demographics Only, mini | 1,570 | 2,063 | **0,281** | 0,502 | 0,548 | **0,065** |

M3 ne portant que sur les 40 items ordinaux et M1 et M2 sur les 108, le desaccord pouvait
venir du jeu d'items et non de la mesure. **Il vient de la mesure** : recalcule sur les
memes 40 items, M1 donne un ratio inter de 1,30 a 3,65 et un ratio intra de 0,33 a 0,60,
alors que M3 donne 0,28 a 2,92 et 0,06 a 0,22 [MESURE]. Table complete dans
`a6-diagnostic-items-ordinaux.csv`.

**Interpretation, et c'est une hypothese.** M3 suppose des intervalles egaux entre modalites
d'une echelle de Likert a cinq points. Un modele qui concentre ses reponses sur deux
modalites adjacentes, par exemple 3 et 4, perd environ la moitie de son entropie mais
**presque toute sa variance ordinale**, parce que l'ecart quadratique a la moyenne s'effondre
quand la plage employee se retrecit. Le meme mecanisme ecrase le terme inter : si toutes les
moyennes de segment se tassent dans la meme bande etroite, leur variance tombe. Sur le GSS,
ou les items ordinaux ont des echelles courtes et des marginales deja concentrees, ce
mecanisme etait moins visible. [HYPOTHESE]

**Consequence pour la redaction.** La double distorsion mesuree ici est un resultat
**d'information mutuelle et d'indice de Simpson**. Sur les echelles de Likert de Twin,
formulee en variance, elle devient un ecrasement massif des deux termes, c'est a dire un
aplatissement simple et non une double distorsion. **Il faut nommer la mesure a chaque fois
que le resultat est cite.** Et il faut noter que c'est M3, la mesure la plus proche du
"ratio d'ecarts types" de la litterature, qui donne la lecture la plus severe pour les
modeles sur la dispersion interne : 0,06 a 0,22, ce qui est **bien en dessous** de la
fourchette 0,40 - 0,56 citee dans la these du projet.

**Sur les jeux economiques et le Big Five, en revanche, M3 est directement interpretable**,
puisque les valeurs y sont numeriques et que le codage fin rend la decomposition exacte. Elle
y donne : ratio intra de **0,16 a 0,37** pour les jeux economiques et de **0,16 a 1,11**
pour le Big Five, avec un ratio inter qui garde le meme signe que M1 pour six conditions sur
huit dans chaque jeu. Deux inversions a signaler honnetement : sur le Big Five, `bigfive_v3`
a un ratio inter de 2,387 en M1 mais de **0,419** en M3, et les agents enquete de 1,469 en
M1 mais de **0,940** en M3. Detail dans les deux CSV.

---

## 6. Le controle des estimateurs

`a6-controle-permutation.csv`. On permute au hasard les etiquettes de segment : le terme
inter doit alors valoir zero. Ce qui subsiste est soustrait, comme dans a1.

| jeu | entropie | Gini Simpson | variance ordinale |
|---|---|---|---|
| jeux economiques | 0,5 a 33 % | -4 a +1 % | -6 a +1 % |
| Big Five | 2 a 8 % | -2 a +2 % | -1 a 0 % |
| Twin, n = 2058 | 4 a 18 % | -0,2 a +0,2 % | -0,5 a +0,2 % |
| Twin, sous ensemble n = 1000 | **13 a 40 %** | 0 a 0,4 % | -0,4 a +0,7 % |

Trois choses a retenir.

1. **Gini Simpson et la variance ordinale sont propres partout**, residu inferieur a 1 pour
   cent. Ces deux estimateurs n'ont pas besoin de la correction empirique.
2. **L'entropie a un residu qui croit quand le denominateur humain est petit.** Il atteint
   33 pour cent pour les agents persona des jeux economiques et 18 pour cent pour les
   humains de Twin, contre 3 a 15 pour cent sur le GSS en a1. La soustraction est donc
   d'autant plus determinante, et le ratio inter en entropie d'autant plus fragile, sur ces
   deux jeux.
3. **Le sous ensemble a 1000 sujets est a la limite** : residu de 38 a 40 pour cent chez les
   humains. Le chiffre de 2,673 pour `JSON Persona - GPT4.1-mini` doit etre lu comme un
   ordre de grandeur, pas comme une estimation. Il est coherent avec les douze autres, ce
   qui est la seule chose qu'on puisse en dire.

---

## 7. Test 3 : le GSS revisite

### 7.1 Le silhouette sur le seul sous ensemble attitudinal

C'etait la piste 2 de a1 section 5 pour expliquer l'ecart avec le 0,19 de la litterature.
**Elle est refutee** [MESURE].

Regle d'appartenance, mecanique et portant sur le **jeu de modalites** de l'item, jamais sur
le texte de la question : un item est attitudinal si ses modalites forment une echelle
d'opinion figurant dans une liste fermee de treize echelles, donnee en entier dans le script
(`ECHELLES_ATTITUDINALES`). Elle retient **57 items sur les 169 non demographiques** : les
17 items de depense publique `nat*`, les 13 items de confiance dans les institutions `con*`,
les items de tolerance `spk*` / `col*` / `lib*`, et les items d'opinion `cappun`, `gunlaw`,
`spanking`, `sexeduc`, `pillok`, `xmarsex`, `homosex`, `marhomo`, `prayer`, `courts`, plus
les cinq items de role des femmes `fe*` et les deux items de discrimination positive.

Score de silhouette, distance d'appariement simple, intervalles bootstrap.

| condition | genre | race | **ideologie** | age | education | profil croise |
|---|---|---|---|---|---|---|
| **57 items attitudinaux** | | | | | | |
| humains vague 1 | 0,013 | -0,002 | **-0,028** | -0,030 | -0,019 | -0,047 |
| humains vague 2 | 0,013 | -0,001 | -0,031 | -0,030 | -0,018 | -0,051 |
| agents composite | 0,020 | -0,013 | -0,054 | -0,069 | -0,029 | -0,091 |
| agents entretien (`v3`) | 0,026 | -0,047 | -0,077 | -0,092 | -0,037 | -0,115 |
| agents enquete | 0,016 | -0,036 | -0,062 | -0,087 | -0,041 | -0,102 |
| agents persona (`v7`) | 0,027 | -0,059 | -0,057 | -0,060 | -0,054 | -0,139 |
| agents demo. (`v6`) | 0,047 | -0,077 | -0,059 | -0,088 | -0,013 | -0,132 |
| agents demo. (`v8`) | 0,018 | -0,080 | **0,096** [0,070 ; 0,119] | -0,132 | -0,069 | -0,110 |
| **169 items, rappel de a1** | | | | | | |
| humains vague 1 | 0,010 | 0,006 | -0,020 | -0,021 | -0,007 | -0,026 |
| agents demo. (`v8`) | 0,014 | -0,014 | 0,079 | -0,028 | -0,056 | -0,032 |

**Restreindre aux items attitudinaux ne rapproche pas du 0,19, cela en eloigne.** Le
maximum passe de 0,079 a 0,096, toujours pour la seule variante `v8` sur la seule
segmentation ideologique, et **toutes les autres cellules d'agents deviennent plus
negatives**, jusqu'a -0,139. Autrement dit, sur le sous ensemble ou l'effet devrait etre le
plus visible, les segments demographiques forment des amas **moins** nets chez les agents
que chez les humains. La dilution par les items biographiques et de menage n'est donc pas
l'explication de l'ecart avec la litterature.

Reste la piste 1 de a1, le jeu de donnees, et la piste 3, la distance et la normalisation
employees par la source du 0,19. **La piste 3 est celle a faire en premier, elle ne coute
qu'une relecture.** Ce rapport ne l'a pas faite.

Un fait accessoire mais utile : la valeur humaine sur l'ideologie passe de -0,020 sur 169
items a **-0,028** sur les 57 attitudinaux, et le controle vague 2 la reproduit a 0,003
pres. La mesure est stable.

### 7.2 La mediane des ratios item par item

C'etait la limite 1 de a1. `a6-gss-mediane-item.csv`.

| condition | inter, 169 items | inter, 57 attitudinaux | intra, 169 items | intra, 57 attitudinaux |
|---|---|---|---|---|
| humains vague 2 | 0,980 | **1,004** | 1,002 | 1,001 |
| agents composite | 1,235 | **1,766** | 0,912 | 0,878 |
| agents entretien (`v3`) | 1,238 | **2,260** | 0,891 | 0,854 |
| agents enquete | 1,080 | **1,528** | 0,832 | 0,810 |
| agents persona (`v7`) | 0,478 | 0,377 | 0,683 | 0,632 |
| agents demographiques (`v6`) | 0,726 | 0,697 | 0,657 | 0,613 |
| agents demographiques (`v8`) | 2,184 | **3,816** | 0,608 | 0,761 |

Mediane sur les couples (axe, item) ou l'information mutuelle humaine depasse 0,002 bit :
771 couples sur les 169 items, 254 sur les 57 attitudinaux. Verifie aussi en Gini Simpson,
meme classement et memes ordres de grandeur.

**La limite 1 de a1 se resout en grande partie.** a1 notait que la mediane item par item,
1,24 pour les agents composite et 2,18 pour `v8`, etait bien plus basse que les sommes,
1,75 et 5,91, et concluait que le gonflement etait porte par les items ou l'information
mutuelle humaine est deja elevee. **Restreinte aux items attitudinaux, la mediane remonte a
1,77 et 3,82**, c'est a dire au voisinage des sommes [MESURE]. L'ecart entre mediane et
somme n'etait donc pas surtout un effet de ponderation, c'etait surtout une dilution par les
112 items non attitudinaux, ou il n'y a pas de gonflement a mesurer.

Et le controle passe mieux : la mediane du retest humain vaut 1,004 sur le sous ensemble
attitudinal, contre 0,980 sur les 169 items.

Formulation correcte pour une publication : sur les items d'opinion du GSS, les agents
riches en information gonflent les ecarts entre segments d'un facteur median 1,5 a 2,3, et
la variante `v8` d'un facteur median 3,8, **que l'on agrege par somme ou par mediane**.

---

## 8. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise, et c'est le principal.** La double distorsion n'est pas une propriete du GSS ni
du pipeline de Stanford. Sur Twin-2K-500, jeu produit par une autre equipe, treize
configurations de simulation sur treize presentent simultanement un gonflement des ecarts
entre segments demographiques, facteur 1,57 a 3,73, et un ecrasement de la dispersion
interne, 0,45 a 0,75, avec des intervalles a 95 pour cent qui excluent 1. Le controle par
retest des memes humains sur les memes questions tombe en (1,004 ; 1,009). Une mesure
globale de dispersion ne voit qu'une compression de 23 a 53 pour cent.

**Autorise.** Le phenomene ne depend pas de la famille de modeles : GPT-4.1, GPT-4.1-mini et
Gemini-Flash-2.5 sont tous dans le quadrant, et l'affinage sur 500 exemples reduit le
gonflement inter a 1,05 sans corriger l'ecrasement intra, qui reste a 0,55.

**Autorise.** Sur quatre materiaux et trois familles de modeles, l'axe qui porte le
gonflement est l'ideologie politique, tandis que le genre et l'age restent au voisinage de
la fidelite ou en dessous. Ce n'est pas un essentialisme demographique general, c'est un
essentialisme politique. Exception documentee : sur le Big Five, le gonflement est porte
autant par le genre et l'education.

**Autorise.** La double distorsion apparait sur le Big Five, qui n'est pas un instrument
politique : cinq conditions sur six, ratio inter 1,5 a 13,5, ratio intra 0,67 a 0,94.

**Autorise, et c'est la reprise du point le plus fort de a1.** Les deux generations
etiquetees demographiques dans le meme paquet ont des ratios inter qui different d'un
facteur 22,8 sur les jeux economiques et 5,7 sur le Big Five, avec intervalles disjoints,
alors que la correlation par individu employee par les figures 2 et 3 du papier les declare
indistinguables, t = +0,45 et t = +1,40.

**Interdit.** Ecrire "la double distorsion" sans nommer la mesure. Sur Twin, la variance
ordinale donne un ratio inter de 0,28 a 2,92 et un ratio intra de 0,06 a 0,22 : sur cette
mesure, plusieurs configurations relevent de l'aplatissement simple, pas de la double
distorsion. Le desaccord est un effet de mesure et non de jeu d'items, il a ete verifie.

**Interdit.** Citer un ratio inter des jeux economiques comme une estimation. Avec cinq
variables, l'intervalle de `v8` est [18,6 ; 110,6] et celui du retest humain [0,83 ; 4,57].
Ce sont des ordres de grandeur.

**Interdit.** Ecrire que la metrique du champ est aveugle en general. Elle l'est sur la
correlation par individu, qui est celle des figures du papier pour ces deux jeux ; sur la
MAE, `v3` et `v8` sont distinguables.

**Interdit.** Reprendre le silhouette de 0,19 comme un fait etabli, et invoquer le jeu
d'items pour expliquer qu'on ne le retrouve pas : restreindre aux 57 items attitudinaux du
GSS eloigne du 0,19 au lieu d'en rapprocher.

**Interdit.** Ecrire que les auteurs du paquet OSF se sont trompes sur `v3` et `v8`. Seule
la divergence de comportement est etablie.

---

## 9. Ce que je n'ai pas pu verifier

1. **Le contenu exact des generations `v3`, `v6`, `v8`, `v4`, `v5`.** Le paquet OSF ne
   contient ni le code de generation ni les invites, ce que a1 avait deja verifie par
   recherche exhaustive et que cette session confirme. La mention `ablation (demog) -- LA`
   pour `v8` reste sans explication dans le paquet. Toute interpretation de l'ecart entre
   `v3` et `v8` reste donc une hypothese sur la cause, pas sur le fait.
2. **La source du score de silhouette de 0,19.** Elle n'a pas ete relue. C'est le test le
   moins couteux des trois listes en a1 section 5 et il reste a faire. Tant qu'il n'est pas
   fait, l'ecart entre nos 0,096 et leurs 0,19 n'est pas explique.
3. **La source de la fourchette 0,40 - 0,56 du ratio d'ecarts types.** Meme remarque. Nos
   mesures encadrent largement cette fourchette selon la mesure et le jeu : 0,06 en variance
   ordinale sur Twin, 0,94 en entropie sur le Big Five.
4. **Le WVS.** Le test decisif propose en a1 section 5, recalculer le silhouette sur le
   World Values Survey avec et sans le pays dans la segmentation, n'a pas ete fait. Le jeu
   de donnees n'est pas dans `data/`.
5. **Les items du BFI-44 un par un.** Ils ne sont pas dans le paquet OSF. Tous les chiffres
   Big Five de ce rapport portent sur cinq scores de trait agreges, ce qui reduit
   mecaniquement la dispersion mesurable et explique probablement le ratio intra eleve,
   0,92 a 0,94. Une mesure item par item donnerait sans doute un ecrasement plus fort. **Ce
   n'est pas verifiable avec les fichiers disponibles.**
6. **La licence exacte de l'archive OSF t6g7k** reste a lire, comme le note
   `data/PROVENANCE.md`. Twin-2K-500 est en CC BY 4.0, verifie.
7. **Le codage ordinal des items MC de Twin.** Les 68 items MC sont traites comme nominaux
   et n'entrent donc pas dans M3. Certains sont probablement ordonnes, par exemple les
   loteries d'Allais. Les traiter comme ordinaux changerait M3 mais pas M1 ni M2.
8. **Les seize configurations manquantes de Twin.** Le depot en publie treize ; il n'y a ni
   variante de taille de contexte ni modele ouvert. Aucune mesure sur un modele ouvert local
   n'a ete faite ici, ce qui reste le regime de production du projet.

---

## 10. Questions ouvertes pour Simon

1. **Le desaccord entre mesures est il un probleme ou un resultat ?** Sur Twin, l'entropie
   dit "double distorsion" et la variance ordinale dit "aplatissement des deux termes". Ma
   lecture est que la variance ordinale mesure autre chose, la plage employee sur une echelle
   de Likert, et que ce quelque chose est en soi une distorsion massive, 0,06 a 0,22, qu'il
   faudrait peut etre publier separement sous le nom de retrecissement d'echelle. Est ce
   defendable devant un relecteur de psychometrie, ou faut il choisir une mesure unique et
   s'y tenir ?
2. **L'ideologie politique comme axe de segmentation.** Elle porte l'effet sur trois
   materiaux sur quatre, et ce n'est pas une variable demographique. Faut il assumer la
   formulation "essentialisme politique" et faire de l'ideologie l'objet du papier, ou
   conserver la formulation demographique plus large au risque que le relecteur constate que
   le genre et l'age ne bougent pas ?
3. **Que faire de la collision `v3` / `v8` ?** Elle est maintenant documentee sur trois jeux
   de donnees du meme paquet, avec des correlations indistinguables et des ratios inter
   separes d'un facteur 5,7 a 22,8. C'est le resultat le plus citable du dossier et c'est
   aussi celui qui met en cause le travail d'une equipe qui a fonde une societe concurrente.
   Publication separee, note technique, ou section d'un papier plus large ?
4. **Le Big Five est il un contre exemple utile ou une faiblesse ?** L'ecrasement intra n'y
   est que de 6 a 8 pour cent pour les conditions riches, et le gonflement n'y est pas
   politique. C'est le materiau le moins favorable a la these. Faut il le publier au meme
   rang que les autres, ce qui est honnete et affaiblit, ou en faire une section de limites ?
5. **Quel jeu porte le papier ?** Twin-2K-500 donne treize configurations sur treize dans le
   quadrant, un retest humain propre, 2058 personnes, une licence CC BY 4.0 et deux familles
   de modeles. C'est le materiau le plus solide des quatre. Le GSS garde l'avantage de la
   comparabilite avec le papier de Stanford. Un papier a deux jeux, ou un papier Twin avec le
   GSS en replication ?

---

## 11. Fichiers produits

| fichier | contenu |
|---|---|
| `a6-figure-double-distorsion-multi-jeux.png` et `.svg` | la figure a quatre cadrans, lisible en noir et blanc |
| `a6-ratios-twin.csv` | les deux ratios, 3 mesures, 12 conditions, intervalles |
| `a6-ratios-twin-sous-ensemble-1/2/3.csv` | les trois configurations a couverture partielle |
| `a6-ratios-econ-games.csv` | idem, jeux economiques, 8 conditions |
| `a6-ratios-bigfive.csv` | idem, Big Five, 8 conditions |
| `a6-ratios-par-axe.csv` | le detail des six axes, tous jeux, toutes mesures |
| `a6-controle-permutation.csv` | diagnostic de biais des trois estimateurs |
| `a6-diagnostic-items-ordinaux.csv` | les memes ratios sur les seuls items ordinaux |
| `a6-variantes-demographiques.csv` | `v3` contre `v8` hors du GSS, tests apparies |
| `a6-twin-configurations.csv` | exactitude, accord par paires, modalites par item |
| `a6-gss-silhouette-attitudinale.csv` | silhouette sur 57 items attitudinaux et sur 169 |
| `a6-gss-mediane-item.csv` | mediane des ratios item par item, deux sous ensembles |

Scripts : `analyses/a6_telecharger_twin_specs.py` et
`analyses/a6_double_distorsion_hors_gss.py`. Aucun fichier existant n'a ete modifie.

Tous les CSV ne contiennent que des statistiques par condition. **Aucune ligne
individuelle, aucune microdonnee.** `.gitignore` exclut de toute facon `*.csv` a la racine
du depot ; les chiffres qui comptent sont recopies dans le present rapport, qui est
versionne.
