# t1. Preenregistrement : la mesure de personne repliquee sur Twin-2K-500

**Ecrit le 9 septembre 2026 a 01 h 08 CEST (8 septembre 2026, 23 h 08 UTC), avant
l'ecriture du premier script de t1 et avant tout calcul de resultat.** Depot a
`d536169dc5361c38edcd723d48816e2ddd06dc4f`.

Ce document fige la question, les quantites, les segmentations, les conditions, la famille
de tests, le nombre de replicats, le mode d'intervalle, les seuils de controle et les
predictions. Tout ce qui s'en ecartera sera declare comme ecart dans le rapport, avec sa
raison.

---

## 1. Ce qui a ete inspecte AVANT d'ecrire ce document, et rien d'autre

Pour ecrire un preenregistrement executable il a fallu connaitre la structure du jeu. Ce
qui suit a ete lu ; **aucune quantite de resultat n'a ete calculee**, ni exactitude, ni
chute, ni ratio, ni correlation.

1. Les scripts et rapports du dossier : `analyses/a44_commun.py`, `a44_mesures.py`,
   `a47_chute_segmentations.py`, `a2_commun.py`, `a2_baselines_twin.py`,
   `a6_double_distorsion_hors_gss.py`, `a1_double_distorsion.py`, `i3b_twin.py`,
   `i3b_commun.py`, `i3_commun.py`, `a35_commun.py` ; `resultats/a44-generateur-nul.md`
   avec ses errata, `a47-errata-2.md`, `a45-relecture-adverse-2.md`,
   `a6-double-distorsion-hors-gss.md`, `i3b-abaque-et-borne.md`.
2. La structure de `data/twin2k500` : 108 colonnes categorielles de la vague 4 sur 126,
   type `MC` ou `Matrix` au catalogue, 2 058 sujets, 13 configurations plus deux
   references humaines dans `llm_specs/`, 14 questions du bloc `Demographics`,
   494 colonnes categorielles des vagues 1 a 3 non reposees en vague 4, largeur totale de
   leur codage indicatrice 2 056 colonnes.
3. **Les modalites des cinq variables de segmentation candidates**, effectifs compris :
   `QID12` genre (Female 1 044, Male 1 014), `QID13` age en quatre tranches, `QID14`
   education en six niveaux, `QID15` ethnicite en cinq niveaux, `QID22` **ideologie
   politique en cinq niveaux** (Moderate 582, Liberal 564, Conservative 430, Very liberal
   345, Very conservative 137), `QID20` **parti en quatre niveaux** (Democrat 847,
   Independent 609, Republican 540, Something else 62). Aucune valeur manquante sur ces
   six variables : les six sommes valent 2 058.
4. Un banc de temps sur **matrices aleatoires** de la forme reelle, pour dimensionner le
   nombre de replicats. Aucune donnee reelle n'y est entree.

**Reponse a la question posee par la mission : Twin a l'ideologie et il a le parti.** La
segmentation principale sera donc l'ideologie, analogue exact de `S_ideo` du GSS, et le
repli sur genre x age x education n'a pas lieu d'etre. Le parti recoit une segmentation a
lui, secondaire.

---

## 2. La question

`a44` mesure, sur le GSS, la chute d'exactitude sous permutation des personnes a
l'interieur de leur segment, et en fait la quantite qui separe le gabarit de groupe du
porteur de personne. `a47` montre que le chiffre depend de la segmentation. `a45`, point 10
de sa section « ce que je n'ai pas pu verifier », ecrit : « la replication sur Twin de la
chute sous permutation n'existe pas, et c'est ce qu'un relecteur demandera en premier apres
avoir lu la section 1.1 : si le chiffre depend de la segmentation sur le GSS, il faut
savoir s'il depend aussi du jeu ».

**t1 repond a cela, et a rien d'autre.** Autres personnes, autres items, autres auteurs,
autres modeles, autre pipeline : 2 058 personnes, 108 items de la vague 4, treize
configurations produites par l'equipe Twin-2K-500 avec GPT-4.1, GPT-4.1-mini et
Gemini-Flash-2.5.

---

## 3. Conditions

**Famille primaire, seize conditions.** Les treize configurations de `llm_specs/index.json`
plus les trois predicteurs statistiques `B1 argmax`, `B2 argmax` et `PMM k=10` construits
ici.

**Hors famille, descriptif.**
- `humains vague 4` : la verite. Son exactitude vaut 1 par construction, sa chute est une
  reference triviale.
- `humains vagues 1-3 (retest)` : **le plancher humain**, equivalent de `humains vague 2`
  sur le GSS. C'est le denominateur de la colonne « part du plancher humain ».
- `B0 mode` et `B0 tirage` : les deux temoins aveugles a la personne. `B0 mode` predit la
  modalite majoritaire de l'item, `B0 tirage` tire dans la marginale de l'item. **Leur
  chute doit valoir zero. Si elle ne le vaut pas, le dispositif fabrique de la chute et
  toutes les autres lignes sont sans valeur.**

**Perimetres.** Trois configurations ne couvrent pas les 2 058 sujets :
`JSON Persona - GPT4.1-mini` 1 000, `LLM Finetuning (500 training samples)` 1 558,
`JSON Persona (Predicted Output) - GPT4.1` 2 050. Regle de `a6` et interdit numero 4 de
`a44` : **chacune est mesuree sur son propre perimetre, avec le plancher humain recalcule
sur les memes sujets, et jamais comparee en valeur absolue a une condition d'un autre
perimetre.** La colonne « part du plancher humain » est la seule comparable entre
perimetres, et elle est publiee comme telle.

**Deux configurations echouent au controle de masque de `i3b` (ecart E4)** :
`JSON Persona (Predicted Output) - GPT4.1-mini`, 9,92 pour cent de cellules perdues, et
`JSON Persona (Predicted Output) - GPT4.1`, 0,508 pour cent. Elles sont conservees,
recontrolees ici, et signalees dans tous les tableaux.

---

## 4. Segmentations

Quatre, declarees maintenant, la premiere etant la principale.

| nom | definition | cellules attendues | role |
|---|---|---|---|
| `S_ideo` | `QID22`, ideologie a cinq niveaux | 5 | **principale**, analogue exact de `S_ideo` du GSS |
| `S_fin` | bloc d'ideologie (3) x genre (2) x age (4) | au plus 24 | fine, contient l'ideologie ; analogue de `S_fin` du GSS |
| `S_gra` | genre (2) x ethnicite (5) x age (4) | au plus 40 | **fine et sans ideologie**, analogue de la segmentation que `a47` E2 impose comme lecture principale sur le GSS |
| `S_parti` | `QID20`, parti a quatre niveaux | 4 | secondaire ; Twin a le parti, le GSS ne l'avait pas dans `a44` |

Le bloc d'ideologie a trois niveaux emploie la regle mecanique de `a1` et de
`a6.bloc_ideologie_twin`, deja ecrite : « liberal » dans le libelle donne gauche,
« conservative » donne droite, le reste donne centre. Aucune retouche.

**Ecrit avant le calcul, parce que `a47` E2 l'exige** : si `S_ideo` et `S_gra` donnent des
parts du plancher humain differentes d'un facteur superieur a 2 pour au moins une
configuration, alors le rapport publiera `S_gra` en lecture principale et `S_ideo` en
lecture secondaire, comme `a47` l'impose au GSS.

---

## 5. Les quantites

**Q1. Exactitude vraie par personne.** Convention de `a2` et de `a44` : une cellule compte
au denominateur des que la reponse humaine de la vague 4 est observee ; une prediction
absente compte comme fausse.

**Q2. La chute sous permutation intra segment.** `P = 200` permutations par couple
(condition, segmentation), tirees avec `a44_commun.permuter_intra` importe sans
modification. Sorties : exactitude permutee moyenne, bande des permutations aux
percentiles 2,5 et 97,5, chute absolue, chute relative, **part du plancher humain**
(chute relative de la condition divisee par celle du retest humain sur le meme perimetre
et la meme segmentation).

**Q3. La reassignation optimale intra segment**, appariement hongrois, et **son plancher**.
`a47` E4 interdit de publier le rapport `(hongrois - permutee) / (vraie - permutee)` sans
son plancher : le **gain hongrois absolu** est publie a cote, et `B0 tirage`, population
sans aucune structure individuelle, calibre le terme sur chaque perimetre.

**Q4. Le generateur nul, ratio inter et ratio intra sur l'axe ideologie.** Generateur nul
categoriel de `a44` : `X_ij ~ Multinomiale(p_{j, g(i)})`, `p` estimee sur la condition
elle meme, repli sur la marginale d'item sous cinq repondants observes, masque conserve a
l'identique. `R = 200` replicats. La mesure est la chaine de `a1` et `a6`,
`construire_index` puis `compter` puis `decomposer` puis `agreger`, entropie de Miller
Madow, **importee sans une ligne modifiee**, avec la correction par permutation des
etiquettes de segment de `a1`, `30` permutations pour la population et `10` par replicat
nul. **Le nul et la mesure partagent le meme axe**, comme le tableau 1 de `a44` l'impose.

**Q5, secondaire et descriptive. Le ratio agrege sur les six axes de `a6`**, sous un nul
conditionne sur la seule ideologie. Cette lecture est declaree d'avance comme une **borne
inferieure** de la part reproduite : un nul qui ne connait que l'ideologie ne peut pas
reproduire les contrastes de genre, d'age, d'education et d'ethnicite.

**Q6. La correlation de la chute avec l'exactitude brute**, Pearson et Spearman, sur les
seize conditions de la famille primaire, par segmentation. **Version partialisee, decidee
maintenant** : regression lineaire de la chute sur l'exactitude a travers les conditions,
et publication des **residus**, ordonnes. Une configuration dont le residu est negatif
porte moins de personne que son exactitude ne le laisserait croire.

**Q7. La coherence avec `i3b`.** Correlation de Spearman entre la part du plancher humain
et, d'une part, le deficit de patrons `A` de `i3b-twin-sources-pures.csv`, d'autre part le
plus petit taux detectable `tau*` sous Holm(39) a N = 2 058 de `i3b-twin-abaque.csv`. Ces
deux fichiers sont **lus, jamais recalcules**.

---

## 6. Les controles, executes avant toute lecture de resultat

Deux sont **bloquants** : si l'un echoue, le rapport le declare et la lecture concernee
n'est pas publiee.

1. **Bloquant 1, l'invariance.** Le ratio inter et le ratio intra doivent etre exactement
   invariants sous permutation des personnes a l'interieur de leur segment. Seuil declare
   `1e-12`. C'est le fait arithmetique de `a44` section 3.1 : ces deux termes ne dependent
   que de la table de contingence (segment, modalite). S'il echoue, l'implementation est
   fausse.
2. **Bloquant 2, les marginales du nul.** Le generateur nul doit redonner les marginales
   par item et par segment de la condition qui le parametre. Ecart moyen sur les couples
   non replies, seuil declare `0,01`, sur 100 replicats.
3. **Le temoin.** `B0 mode` et `B0 tirage` doivent avoir une chute inferieure a
   `0,5 pour cent` en valeur absolue sous les quatre segmentations.
4. **Le masque.** Part des cellules ou la reponse humaine de la vague 4 est observee et la
   prediction absente, par condition. Seuil de signalement `0,5 pour cent`, celui de
   `i3b` 9.2. Les depassements sont publies, pas exclus.
5. **Le repli du nul.** Taux de couples (item, segment) replies sur la marginale d'item,
   par segmentation et par perimetre. `a44` interdit de lire un nul dont le repli est
   massif : **au dela de 30 pour cent de repli, la ligne est publiee et declaree non
   lisible**, comme la ligne `C2` sous `S_fin` de `a44`.
6. **La reproduction de `a6`.** Le ratio inter et le ratio intra de la population,
   axe ideologie, entropie, doivent redonner `a6-ratios-par-axe.csv` a 2 pour cent pres.
   Non bloquant : `a6` mesure sur quinze tables reparties en quatre jeux et t1 sur une
   nomenclature commune aux quinze, ecart E5 de `i3b`.
7. **La reproduction de l'exactitude.** L'exactitude sur codes entiers doit egaler celle
   de `a2_commun.exactitude_par_personne` sur les chaines, ecart maximal declare `1e-12`.

---

## 7. Intervalles de confiance et tests

**Regle declaree, tiree de `i3b` : le bootstrap avec remise n'est admissible que pour les
statistiques qui sont des moyennes sur les personnes.**

- **Q1, exactitude** : bootstrap sur les personnes avec remise, `B = 1 000` tirages. C'est
  une moyenne par personne, le tirage avec remise est sans biais.
- **Q2 et Q3, chute et gain hongrois** : **sous echantillonnage pivote**,
  `m = N / 2`, `S = 200` sous echantillons, mise a l'echelle par `racine(m / N)`,
  correction de population finie `1 / racine(1 - m / N)`, pivot sur la moyenne des sous
  echantillons, via `i3b_commun.ic_pivote` importe sans modification. Raison : dupliquer
  une personne dans un segment permet a la permutation de lui reassigner ses propres
  reponses, ce qui gonfle mecaniquement l'exactitude permutee et **ecrase la chute**.
- **Q4, ratios** : bande des 200 replicats nuls, et **sous echantillonnage pivote** pour
  l'incertitude d'echantillon. Les estimateurs a biais corrige dependent de l'effectif
  effectif, que le tirage avec remise change.
- **Q6, correlations** : intervalle par sous echantillonnage pivote sur les personnes, et
  test de permutation sur les conditions.

**Famille de tests et correction.** **Holm** sur la famille primaire, seize conditions,
declaree ici : le test est « la chute de la condition est elle superieure a celle du
temoin `B0 tirage` sur le meme perimetre et la meme segmentation ». La segmentation du
verdict est **`S_gra`**, celle qui ne contient pas l'ideologie, conformement a `a47` E2.
Les trois autres segmentations sont publiees sans correction, en lecture.

**Graine unique** `20260909`. Quatre coeurs. Aucun appel de modele de langage. Lecture
seule sur `data/`. Aucun script existant n'est modifie. Le `llama-server` de R2 n'est pas
touche.

---

## 8. Le classement, et son seuil

`a44` section 7.2 emploie un seuil non declare avant calcul, et son interdit numero 6 le
signale. **Ici le seuil est declare maintenant**, avant tout calcul, dans la meme echelle,
la part du plancher humain :

- **gabarit de groupe** : part du plancher humain **inferieure a 0,15** ;
- **porteur de personne** : part **superieure a 0,40** ;
- **intermediaire** entre les deux.

Il est applique sous `S_gra`, la segmentation du verdict, et reporte sous les trois autres
pour montrer ce qui change.

---

## 9. Les huit predictions, ecrites avant tout calcul

| | prediction |
|---|---|
| **P1** | Les deux temoins `B0 mode` et `B0 tirage` ont une chute inferieure a 0,5 pour cent sous les quatre segmentations. |
| **P2** | `Demographics Only - GPT4.1-mini`, la seule configuration de Twin qui ne recoit que des etiquettes, a la plus petite part du plancher humain des treize, et elle est sous 0,30 sous `S_gra`. |
| **P3** | Les configurations `Text Persona` et `JSON Persona`, qui recoivent un profil riche, sont au dessus de 0,40 du plancher humain sous `S_gra`, donc du cote du porteur de personne, comme `agents composite` sur le GSS. |
| **P4** | La part du plancher humain **change moins entre `S_ideo` et `S_gra` sur Twin que sur le GSS**. Raison ecrite d'avance : aucune configuration de Twin ne recoit l'etiquette ideologique en clair, alors que `v8` et `C2` la recoivent ; l'effet de `a47` E2 est un effet de « on fixe la variable que l'agent a recue », il ne doit donc pas se produire ici. **C'est la prediction la plus risquee du lot et celle qui teste la lecture causale de `a47`.** |
| **P5** | Le ratio inter de l'axe ideologie est reproduit par le generateur nul a plus de 95 pour cent pour les treize configurations, comme sur le GSS, et l'intervalle de la difference contient zero pour au moins dix d'entre elles. |
| **P6** | La correlation de Pearson entre la chute et l'exactitude brute sur Twin est **superieure a 0,80**, du meme ordre que le 0,906 du GSS. Si elle l'est, la mesure de personne n'ajoute pas grand chose a l'exactitude et le rapport devra l'ecrire sans l'adoucir. |
| **P7** | `LLM Finetuning (500 training samples)`, que `i3b` designe comme le generateur le plus degenere du dossier, deficit de patrons de 79,3 pour cent, est **du cote du gabarit** : part du plancher humain sous 0,15. |
| **P8** | La correlation de Spearman entre la part du plancher humain et le `tau*` de `i3b` est **positive et superieure a 0,5** : plus une configuration porte la personne, plus il faut la contaminer pour la detecter. |

---

## 10. Ce qui est declare hors de portee avant de commencer

1. **La perturbation d'ordre des items de Yuan.** Elle demande des appels de modele. Elle
   n'est pas faite ici, pas plus qu'en `a44`.
2. **Aucun nouvel appel de modele, aucune nouvelle simulation.** Les treize configurations
   sont celles que l'equipe Twin a publiees ; t1 ne fabrique pas d'agent.
3. **`PMM k=10` sur Twin n'est pas le `PMM` de `a35`.** `a35` impute un item du GSS a
   partir des autres items de la meme vague, par blocs. Sur Twin le contexte est temporel
   et disjoint par construction, vagues 1 a 3 contre vague 4, donc il n'y a pas de bloc a
   retirer. La recette de tirage chez un donneur est celle de
   `a35_commun.imputations_regression`, la structure de validation croisee est celle de
   `a2_baselines_twin`. **C'est une transposition, pas un import.** Si son cout depasse
   soixante minutes, `PMM` est abandonne et l'abandon est declare.
4. **Rien sur le GSS n'est recalcule.** La comparaison GSS contre Twin lit
   `a44-permutation.csv` et `a47-chute-deux-segmentations.csv`, elle ne les refait pas.
5. **Les conditions analogues ne sont pas identiques.** `Demographics Only` de Twin recoit
   des demographies sans etiquette ideologique nommee ; `agents v8` du GSS recoit
   l'ideologie en clair. `a6` et `i3b` le disent tous les deux. **La comparaison de la
   question 5 de la mission est donc une comparaison d'ordres de grandeur entre conditions
   analogues, jamais une equivalence**, et le rapport l'ecrira ainsi.

---

## 11. Fichiers que t1 produira

| fichier | contenu |
|---|---|
| `analyses/t1_commun.py` | chargement, segmentations, quantites, controles |
| `analyses/t1_mesures.py` | la chute, la reassignation, le generateur nul, les correlations |
| `analyses/t1_baselines.py` | `B0`, `B1`, `B2`, `PMM k=10` sur Twin |
| `analyses/t1_figure.py` | la figure |
| `resultats/t1-controles.csv` | les sept controles |
| `resultats/t1-chute-segmentations.csv` | la chute, quatre segmentations, toutes conditions |
| `resultats/t1-reassignation.csv` | le gain hongrois absolu et son plancher |
| `resultats/t1-generateur-nul.csv` | les ratios, population contre nul |
| `resultats/t1-correlation-chute-exactitude.csv` | Q6, brute et partialisee |
| `resultats/t1-classement.csv` | le verdict par configuration et sa coherence avec `i3b` |
| `resultats/t1-gss-contre-twin.csv` | les conditions analogues des deux jeux |
| `resultats/t1-figure-personne-twin.png` et `.svg` | la figure |
| `resultats/t1-mesure-de-personne-twin.md` | le rapport |

---

Fin du preenregistrement. Horodatage du systeme de fichiers a l'ecriture :
**9 septembre 2026, 01 h 08 CEST**. Limite connue et deja signalee par `a45` point 11 : le
repertoire est synchronise par iCloud, l'horodatage n'est pas un depot tiers.
