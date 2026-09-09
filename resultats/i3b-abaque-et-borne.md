# i3b. L'abaque, la norme, la contamination ciblee, et le fabricant qui vise la bande

Mois 1 du programme B de `MOONSHOTS.md`, la bande humaine comme norme de securite des flux
d'opinion. Suite directe de `resultats/i3-detecteur.md`, dont ce rapport ferme cinq limites
declarees : la taille de flux unique (limite 5), le questionnaire unique (limite 3), la
contamination uniforme (limite 6), le fabricant qui vise la bande non construit (limite 7) et
la question ouverte 6 sur l'abaque.

Zero appel de modele de langage, lecture seule sur `data/`, quatre coeurs. **Aucun fichier
existant n'est modifie.**

**Preenregistrement : `resultats/i3b-preenregistrement.md`, ecrit le 8 septembre 2026 a
21 h 05 CEST, avant l'ecriture des scripts et avant tout calcul de resultat, non modifie
depuis. Empreinte SHA-256
`57f921196aef0789bc17d63ef4d2ebbffa5d95c8c0bb78b5c31497d734781168`.** Les sources, la
segmentation, les cinq statistiques dont deux de reserve, le mode de reechantillonnage, les
trois familles de tests et leurs seuils, la grille de tailles, la regle de choix des trois
marginales, la construction et la calibration du fabricant adverse, la partition en trois des
1 052 personnes et sept predictions y sont figes. Huit ecarts sont declares en section 0.

---

## Reponse en une ligne

**Le seuil de detection depend de la taille du flux au moins autant que du fabricant, la
signature humaine se retrouve sur un second jeu avec les memes deux bords mais pas avec les
memes nombres, et le fabricant qui vise la bande gagne un facteur 1,3 sur son invisibilite sans
rien voler et un facteur 2 en volant 263 vraies lignes, sans qu'aucune de nos deux statistiques
de reserve ne le rattrape.** L'abaque : sur 1 052 personnes et 149 items, le plus petit taux
detectable a puissance 80 pour cent, en bilateral corrige, va de **2,2 pour cent** pour l'agent
a etiquette ideologique a **35,4 pour cent** pour la regression stochastique ; sur **300
personnes** les memes fabricants demandent **4,5** et **60,2 pour cent** ; a 5 000, extrapoles,
**1,1** et **24,8** [MESURE puis PROBABLE, `i3b-abaque.csv`]. **Ces chiffres sont de 1,2 a 1,9
fois plus grands que ceux de i3**, et l'ecart est entierement dans le bruit de reference : i3
sous echantillonne a la moitie de l'effectif avec trois replicats nuls et remet a l'echelle par
0,707 la ou le facteur correct est 1,000 ; corrige, l'adversaire nul n'est plus signale a
5 pour cent, il faut 9,2 pour cent pour le voir [MESURE, section 3.3].

**La bande est bien une norme, et elle est une forme, pas une valeur.** Sur Twin-2K-500, 2 058
autres personnes, 108 autres items, treize configurations d'une autre equipe, la reference
humaine a les **memes deux bords** : moins de patrons que son propre nul, A = -0,0410, et plus
de correlation residuelle, B = +0,0260 ; les treize configurations sont toutes du cote pauvre
sur A ; et le retest humain de la vague 4 tombe **sur** la bande, `|z|` maximal 0,40, jamais
signale. Mais les niveaux different d'un facteur 1,9 a 2,5 a effectif egal, et **A et B changent
avec l'effectif du flux** : un institut ne peut transporter ni un seuil ni une valeur, il doit
recalculer la bande a sa taille et a son questionnaire [MESURE]. Fait nouveau que le GSS ne
montrait pas : **six configurations sur treize sont trop pauvres sur A et trop LIBRES sur B en
meme temps**, ce qui est le meilleur argument mesure en faveur du test bilateral applique
statistique par statistique. Et l'ecart entre le meilleur et le pire fabricant vaut **30** sur
le meme jeu : la detectabilite est une propriete du pipeline, pas du modele, le reglage fin sur
500 exemples reels donnant le generateur le plus degenere du dossier, detecte a **0,43 pour
cent** de contamination.

**La contamination concentree sur un camp, qui est le cas d'une operation, se voit trois a cinq
fois plus tot quand l'auditeur recalcule les statistiques a l'interieur de chaque camp** :
0,69 pour cent du flux total au lieu de 1,78 pour l'agent a etiquette, 2,16 au lieu de 6,47 pour
l'agent a demographies. En lecture globale il n'y a pas de regle : sur cinq fabricants sur neuf
la contamination concentree est **plus** visible que la contamination uniforme, sur quatre elle
l'est moins. Et a taux total egal elle deplace beaucoup plus : trente pour cent de faux
repondants d'un seul camp, fabriques par un agent a demographies, **effacent 58 pour cent de
l'ecart mesure entre camps** [MESURE].

**Le prix de l'invisibilite est chiffre, et il n'est pas ce que le brainstorm annoncait : il
n'est pas croissant.** A 1 052 personnes, aucun fabricant ne peut deplacer l'ecart entre camps
de plus de **6,34 pour cent** ni une marginale publiee de plus de **3,78 points** sans etre vu ;
a 300 personnes le plafond monte a **11,17 pour cent** et **5,15 points**. Le maximum n'est pas
atteint par les fabricants les plus difficiles a detecter : les imputations par tirage,
invisibles jusqu'a un tiers du flux, **portent la personne et ne deplacent presque rien**, et
l'adversaire nul, gratuit et invisible jusqu'a 9,2 pour cent, deplace **0,03 pour cent**.
**Etre invisible et etre utile s'opposent ; le danger est au milieu**, chez l'agent riche, vu a
15,9 pour cent apres avoir deja deplace 6,3 pour cent de l'ecart entre camps, et chez l'agent a
demographies, vu a 8,6 pour cent apres avoir deja deplace **3,78 points** sur l'item le plus
politique du questionnaire, qui est exactement le mode de contamination reel.

---

## 0. Les huit ecarts au preenregistrement, tous declares

### E1. Le bruit de reference `s0(N)` : la correction de population finie ne porte que sur la part d'echantillonnage

Le preenregistrement, section 4, pose
`s0(N) = ecart_type_du_sous_echantillonnage(N) / racine(1 - N / 1052)`. **C'est faux pour A et
pour B**, et la mesure le montre. Ces deux statistiques sont des exces sur une moyenne de `R`
replicats du generateur nul ; la variance de cette moyenne est du **bruit de mesure**, present a
l'identique dans le flux et dans la reference, et il ne doit pas etre multiplie par le facteur
de population finie, qui ne corrige que le fait de tirer sans remise dans une population de
1 052 personnes. La formule executee est donc

```
s0(N)^2 = ( ecart_type_sous_echantillon^2 - v_nul ) x FPC(N)^2 + v_nul
```

ou `v_nul` est la variance de la moyenne des `R = 15` replicats nuls, mesuree tirage par tirage
et publiee dans `i3b-reference-par-taille.csv`. C est une concentration brute, sans retrait du
nul, et la polarisation ne fait intervenir aucun nul : pour elles `v_nul = 0` et la formule se
reduit a celle du preenregistrement. **Le `s0` naif et le `s0` corrige sont publies cote a
cote**, et le controle de validite de la mise a l'echelle est calcule pour les deux
[MESURE, `i3b-controles.csv`] :

| | A, 300 | A, 500 | A, 750 | B, 300 | B, 500 | B, 750 | C, 300 | C, 500 | C, 750 |
|---|---|---|---|---|---|---|---|---|---|
| naif | 1,181 | **1,413** | 1,061 | 1,373 | 1,361 | 1,399 | 1,018 | 1,202 | 1,194 |
| corrige | 1,160 | 1,336 | 0,938 | 1,350 | 1,329 | 1,326 | 1,018 | 1,202 | 1,194 |

Le rapport est celui entre l'ecart type de sous echantillonnage remis a l'echelle et l'ecart
type mesure sur 40 populations independantes de meme taille tirees du generateur nul humain.
Le naif sort de la fourchette declaree [0,7 ; 1,4] une fois, sur A a 500 ; le corrige passe
partout. **Les deux versions restent au dessus de 1, c'est a dire conservatrices : les `tau*`
publies ici sont, s'ils se trompent, trop grands et non trop petits.**

### E2. `s0(1052)` est obtenu par la loi de puissance, faute de pouvoir sous echantillonner la population entiere

Le preenregistrement limite la correction de population finie a `N <= 750` sans dire comment
obtenir `s0` a la taille pleine. Il est obtenu en ajustant `s0 = c x N^(-p)` sur les trois
tailles mesurees et en evaluant en 1 052. Les exposants et leurs `R^2` sont publies et ils sont
un resultat en eux memes, section 3.2.

### E3. Le controle « `s0(1052)` contre i3 » est publie et non bloquant

i3 estime son `s0` par sous echantillonnage a `m = 526` avec **trois** replicats nuls, remis a
l'echelle par `racine(m / N) = 0,707` ; i3b l'estime par loi de puissance sur trois tailles avec
**quinze** replicats nuls et une correction de population finie. Ce ne sont pas les memes
estimateurs et le controle ne peut pas etre bloquant. L'ecart mesure est publie et discute en
section 3.3 : **`s0` de i3b est superieur de 46,5 pour cent sur A, 77,1 pour cent sur B et
46,2 pour cent sur C** [MESURE].

### E4. Sur Twin, deux configurations echouent au controle de masque

Le controle 9.2 exige que la source perde moins de 0,5 pour cent des cellules renseignees chez
les humains. Deux des treize configurations echouent [MESURE, `i3b-twin-controles.csv`] :
**`JSON Persona (Predicted Output) - GPT4.1-mini` perd 9,92 pour cent** des cellules, et
**`JSON Persona (Predicted Output) - GPT4.1` en perd 0,508 pour cent**, juste au dessus du
seuil. Les deux sont conservees, signalees, et leurs `tau*` ne sont pas comparables aux onze
autres : un masque appauvri de dix pour cent change l'effectif par item, donc le nombre de
patrons distincts et la concentration. La seconde, a 0,508 pour cent, est a la limite du bruit
et sa lecture ne change pas. **Aucune conclusion du rapport ne repose sur ces deux lignes.**

### E5. Sur Twin, douze lignes de chargement ont du etre reecrites

`a6.charger_twin` place chacune des trois configurations qui ne couvrent pas les 2 058 sujets
dans un **jeu separe**, avec sa propre nomenclature. Melanger les treize configurations au meme
flux exige une nomenclature commune aux quinze tables et un alignement des trois configurations
partielles sur l'index complet. `a6.charger_twin` et `a6.lire_formatte` sont appelees telles
quelles pour les colonnes cibles, la segmentation et la lecture des fichiers ; seule la
nomenclature commune et l'alignement sont ecrits ici, douze lignes, verifiees par le controle de
reproduction de a6 (sujets, items, configurations et taux de cellules vides).

### E6. La surface d'attaque a 5 000 lit la courbe de consequence ajustee a 1 052

Les quantites de consequence, l'ecart entre camps et les trois marginales, sont des moyennes de
population : leur esperance ne depend pas de la taille du flux, seule leur variance en depend.
La courbe `consequence(tau)` employee a 5 000 est donc celle mesuree a 1 052, et seule la
**position** `tau` de lecture change. C'est declare, et c'est la seule facon de remplir cette
colonne sans une seconde population.

### E7. Le nombre de tirages par cellule n'etait pas fixe

12 tirages de melange par couple (source, taux) pour l'abaque, 10 pour la contamination ciblee,
15 pour l'adversaire, contre 20 dans i3. La **puissance empirique** publiee a donc une
granularite de 1/12, 1/10 et 1/15, et elle est un indicateur, jamais un verdict : les verdicts
reposent sur `z`, sur `p` corrige et sur `tau*`, qui sont calcules sur la moyenne des tirages.

### E8. Le controle de `R^2` de l'ajustement quadratique ne porte que sur les courbes a effet reel

Pour une source dont l'effet reste sous un ecart type de reference au plus haut taux, la
regression de degre 2 ajuste du bruit et son `R^2` n'a pas de sens. Le controle porte donc sur
les seules courbes dont `|z|` depasse 1 au taux maximal.

---

## 0.9 Le score des sept predictions [MESURE]

| | prediction | issue |
|---|---|---|
| **P1** | le rapport `tau*(300) / tau*(1052)` tombe entre 1,5 et 2,3 pour au moins six fabricants sur neuf | **fausse.** Cinq sur neuf seulement : v8 2,05, IM 1,86, E2 1,70, B0 1,62, PMM 1,58 ; en dessous, composite 1,49, C2 1,48, C3 1,35 et v6 1,27. Quatre fabricants decroissent **plus lentement** que la racine de N |
| **P2** | a 5 000, `tau*` de v8 passe sous 1 pour cent et celui de E2 reste au dessus de 10 | **a moitie tenue.** v8 : **1,06 pour cent**, donc fausse, de peu. E2 : **24,8 pour cent**, tenue et largement |
| **P3** | la bande de Twin a les memes deux bords, et les treize configurations sont du cote pauvre sur A | **tenue sur les deux moities.** Humains de Twin : A negatif, B positif, comme sur le GSS ; les treize configurations ont A de -0,084 a -0,793 contre -0,041 |
| **P4** | au moins une configuration de Twin sous 5 pour cent, et un rapport pire sur meilleure superieur a 3 | **tenue et largement.** Quatre configurations sous 5 pour cent, la meilleure a 0,43 ; rapport **30** |
| **P5** | concentre plus detectable en lecture par camp, moins en lecture globale, et deplacement plus fort a taux egal | **deux tiers tenus, un tiers faux.** Lecture par camp : tenue sur les neuf fabricants, facteur 2,9 a 4,7. Lecture globale : **fausse**, la contamination concentree est plus detectable globalement pour cinq fabricants sur neuf. Deplacement : tenue, 1,80 contre 1,45 pour v8 a 30 pour cent |
| **P6** | le fabricant qui vise la bande est constructible sans microdonnees, a moins d'un `s0` sur A et B, et reste vu sous 25 pour cent par une reserve | **fausse sur la premiere moitie, a moitie fausse sur la seconde.** Aucun point de grille ne met A et B a moins d'un `s0` : le meilleur compromis est a **3,36 `s0`**. Et pour `A* deux cibles` **aucune des deux reserves ne le voit sous 45 pour cent**, c'est la statistique publiee B qui le voit a 13,7 |
| **P7** | le prix de l'invisibilite croit avec `tau*`, et reste sous 10 pour cent de la valeur humaine a 1 052 | **fausse sur la premiere moitie, tenue sur la seconde.** Le maximum est atteint par `agents composite`, `tau*` 15,9 pour cent, et non par `E2`, `tau*` 35,4 ; le plafond a 1 052 vaut **6,34 pour cent**, sous 10 |

**Deux predictions tenues, deux fausses, trois a moitie fausses.** Aucune reecriture n'a ete
faite. Les trois plus informatives sont les fausses : **P6**, qui dit que l'adversaire libre ne
rentre pas dans la bande mais que notre statistique de reserve ne sert quand meme a rien ;
**P7**, qui dit que l'invisibilite et la nuisance s'opposent ; et **P1**, dont la faussete a
oblige a mesurer que deux des trois statistiques ne suivent pas la racine de N, ce qui est le
point operationnel de la section 3.2.


---

## 1. Les controles

[MESURE, `i3b-controles.csv`, 56 lignes sur le GSS, **toutes passent**]

1. **Part de cellules renseignees mais hors nomenclature** : 0,000 pour cent chez les humains
   des deux vagues, chez C2, C3, PMM, E2 et IM ; au pire **0,070 pour cent** pour `agents v8`.
   Seuil declare 0,5 pour cent.
2. **Cellules perdues par l'intersection des masques**, lues sur les seules lignes ou la source
   existe : 0,000 pour cent pour C2, C3, PMM, E2, IM et la vague 2 ; **0,171** pour v8,
   **0,244** pour v6, **0,043** pour composite. Seuil 0,5 pour cent.
3. **Taux de repli du generateur nul sous `S_ideo`** : **0,0 pour cent**.
4. **Le flux a taux 0 egale la population de fond**, ecart 0 cellule.
5. **Controle negatif**, le fond melange a lui meme aux cinq taux, ecart 0 cellule.
6. **Validite de la mise a l'echelle du sous echantillonnage**, aux trois tailles et pour les
   trois statistiques : rapports de **0,938 a 1,350**, fourchette declaree [0,7 ; 1,4], contre
   40 populations independantes de meme taille tirees du generateur nul humain. Tableau de
   l'ecart E1.
7. **Reproduction de i3 sur les dix sources pures**, taux 100 pour cent : ecart maximal sur les
   trois statistiques de **0,00222** (`C2`), et **0,00016** sur les humains purs. Seuil declare
   0,005. **La chaine de mesure de i3b est celle de i3, sans une ligne modifiee, et elle redonne
   ses chiffres** [CONFIRME pour l'identite du code, MESURE pour les valeurs] ; ce qui change est
   le bruit de reference, pas la mesure.
8. **Le controle de fausse alarme** : `humains vague 2`, de vraies personnes reinterrogees deux
   semaines plus tard, n'est signale a aucun taux et a aucune taille. Son `tau*` vaut
   **94,6 pour cent a N = 300** et n'existe pas aux trois autres tailles, la courbe n'atteignant
   jamais la cible sur [0 ; 1] [MESURE].

Deux controles supplementaires sont publies, non bloquants, parce qu'ils comparent des
estimateurs qui ne sont pas les memes.

- **Le biais du bootstrap avec remise**, en ecarts types de reference a N = 1 052 :
  **moins 67,1 `s0` sur A**, **plus 3,64 `s0` sur B**, **plus 14,2 `s0` sur C** [MESURE].
  i3 avait mesure ce defaut sur B et l'avait ecrit en ecart E1 ; **il est bien pire sur A et sur
  C**, ce qui etait attendu et n'avait jamais ete chiffre. Un detecteur calibre sur un bootstrap
  avec remise serait deporte de dizaines d'ecarts types et **ne detecterait plus rien**. Le
  sous echantillonnage pivote est le seul mode admissible pour ces statistiques.
- **`s0(1052)` de i3b contre `s0(1052)` de i3** : plus 46,5 pour cent sur A, plus 77,1 pour cent
  sur B, plus 46,2 pour cent sur C. Section 3.3.

---

## 2. Protocole

### 2.1 Ce qui est repris sans une ligne modifiee

Le codage entier, le generateur nul multinomial par segment, les vingt sous ensembles de dix
items, le comptage des patrons distincts, la correlation de Spearman residualisee du segment, la
concentration par segment et la polarisation viennent de `i3_commun` et, par lui, de
`a44_commun`. Le chargeur de Twin-2K-500 vient de `a6_double_distorsion_hors_gss`. La distance
de Hamming vient de `a2_commun`. **Aucun de ces fichiers n'est modifie, aucune formule n'est
reecrite, et les horodatages le montrent** [CONFIRME]. La seule reecriture est celle de l'ecart
E5, douze lignes de chargement sur Twin, et elle est declaree.

### 2.2 Les cinq statistiques, et ce que chacune coute a l'auditeur

| | statistique | ce que l'auditeur doit detenir |
|---|---|---|
| **A** | deficit relatif de patrons de reponses distincts par rapport au nul du flux | la matrice et l'ideologie declaree |
| **B** | exces de correlation de rang residualisee du segment | idem |
| **C** | concentration par segment, part du patron modal | idem |
| **R1**, reserve | structure de correlation a l'**ordre trois** : moyenne des `|E[z_i z_j z_k]|` sur 20 000 triplets d'items, rangs residualises du segment et standardises, **en exces sur le nul du flux** | idem, **rien de plus** |
| **R2**, reserve | moyenne des distances de Hamming au **plus proche voisin** d'un echantillon humain de reference disjoint du flux | **de vraies microdonnees appariables au questionnaire** |

R1 est nulle en esperance sous tout modele a dependance purement de paires, gaussien compris :
elle mesure exactement ce que la matrice de correlation ne contient pas. R2 est la seule des
cinq qui impose un cout a l'auditeur, et c'est le point de la section 6.

### 2.3 Les trois familles de tests et leurs seuils

Test **bilateral**, seuil nominal 5 pour cent, correction de Holm dans chaque famille.

| famille | contenu | `z` du seuil le plus severe |
|---|---|---|
| **F1**, l'abaque et la surface d'attaque | les 3 statistiques appliquees a un fichier, ce que fait un auditeur reel | **2,394** |
| *rappel*, la famille de i3 | 3 statistiques x 9 sources = 27 | *3,113* |
| **F2**, Twin | 3 statistiques x 13 configurations = 39 | **3,220** |
| **F3**, le fabricant qui vise la bande | 3 publiees + 2 de reserve | **2,576** |

Le seuil cite dans le texte est celui de la famille de trois, qui est le bon pour un institut ;
le seuil de i3 est publie a cote de chaque `tau*` pour que les deux rapports se lisent ligne a
ligne.

### 2.4 L'abaque : un seul flux, quatre lectures emboitees

Pour un couple (source, taux, tirage), le flux est construit **une fois** a 1 052 lignes par la
regle de i3, remplacement en place, demographies jamais touchees, masque commun ; puis il est lu
a 300, 500, 750 et 1 052 par **sous echantillonnage emboite**, le sous echantillon a 300 etant
inclus dans celui a 500, lui meme dans celui a 750. La seule chose qui change d'une taille a
l'autre est donc la taille. Le taux realise dans le sous echantillon est aleatoire autour du
taux nominal et il est publie.

**Aucune duplication de personne n'est employee pour depasser 1 052.** L'ecart E1 de i3 et le
controle de biais du bootstrap de la section 1 disent pourquoi : un doublon fabrique du deficit
de patrons et de l'exces de correlation, c'est a dire exactement le signal cherche. Ce qui est
au dela de 1 052 est extrapole et marque comme tel.

---

## 3. L'abaque

### 3.1 Tableau 1 : le plus petit taux detectable, par taille de flux

[MESURE, `i3b-abaque.csv`, puissance 80 pour cent, bilateral 5 pour cent, Holm sur la famille de
trois, meilleure des trois statistiques. Les quatre premieres colonnes sont mesurees ; les
quatre dernieres sont extrapolees et marquees [PROBABLE].]

| fabricant | 300 | 500 | 750 | **1 052** | 1 500 | 2 000 | 3 000 | 5 000 |
|---|---|---|---|---|---|---|---|---|
| `agents v8`, etiquette ideologique | **4,5 %** | 3,2 % | 2,7 % | **2,2 %** | 1,9 % | 1,6 % | 1,3 % | **1,1 %** |
| `C2`, etiquette, local | 5,7 % | 4,8 % | 4,4 % | **3,8 %** | 3,5 % | 3,2 % | 2,8 % | 2,4 % |
| `C3`, sans etiquette, local | 10,7 % | 9,4 % | 8,8 % | **7,9 %** | 7,7 % | 7,5 % | 7,1 % | 6,6 % |
| `agents demographiques (v6)` | 10,9 % | 9,7 % | 9,3 % | **8,6 %** | 7,5 % | 6,7 % | 5,7 % | 4,7 % |
| **`B0 segment`, adversaire nul** | 14,8 % | 11,3 % | 10,5 % | **9,2 %** | 8,4 % | 7,9 % | 7,2 % | 6,4 % |
| `IM m=10 mode des m` | 25,0 % | 19,7 % | 16,2 % | **13,5 %** | 11,4 % | 10,0 % | 8,2 % | 6,5 % |
| `agents composite`, riche | 23,6 % | 19,7 % | 18,9 % | **15,9 %** | 14,7 % | 13,8 % | 12,7 % | 11,3 % |
| `PMM k=10`, imputation par tirage | 52,5 % | 41,2 % | 39,4 % | **33,3 %** | 60,7 % | 51,5 % | 41,1 % | 31,3 % |
| **`E2 regression contexte tirage`** | 60,2 % | 41,8 % | 38,9 % | **35,4 %** | 32,6 % | 30,5 % | 27,8 % | **24,8 %** |
| *`humains vague 2`, controle* | *94,6 %* | *jamais* | *jamais* | *jamais* | *jamais* | *jamais* | *jamais* | *jamais* |

**Trois lectures.**

**Un.** Sur un flux de 300 repondants, taille ordinaire d'une consultation locale ou d'un
sous groupe de sondage, **rien n'est detectable sous 4,5 pour cent, et les deux imputations par
tirage ne le sont pas sous 50 pour cent**. L'agent le plus grossier, celui a etiquette
ideologique, y demande deja 4,5 pour cent contre 2,2 a 1 052 : **diviser le flux par 3,5 double
le taux qu'il faut pour voir.**

**Deux.** Le facteur entre 300 et 1 052 vaut de **1,27 a 2,05** selon le fabricant, et il vaut
moins que `racine(1052 / 300) = 1,87` pour six fabricants sur neuf. La prediction P1, qui
annoncait un rapport entre 1,5 et 2,3 pour au moins six sur neuf, est **fausse** : cinq
fabricants sur neuf seulement y sont, et quatre decroissent plus lentement que la racine. La
raison est mesuree en 3.2 : deux des trois statistiques ne se comportent pas en `1 / racine(N)`.

**Trois.** L'ordre des fabricants est **stable a toutes les tailles** : les deux conditions a
etiquette ideologique d'abord, l'agent sans etiquette et l'agent a demographies ensuite, puis
l'adversaire nul, puis l'agent riche et l'imputation par esperance, et les deux imputations par
tirage en dernier, loin derriere. **La hierarchie de i3 est celle de i3b ; ce sont les niveaux
qui bougent.**

### 3.2 Quelle statistique detecte, et pourquoi la taille compte differemment pour chacune

[MESURE, `i3b-abaque.csv`, statistique qui donne le `tau*` le plus bas]

| fabricant | 300 | 500 | 750 | 1 052 |
|---|---|---|---|---|
| `agents v8` | C | C | C | C |
| `C2` | C | C | C | C |
| `agents demographiques (v6)` | A | A | A | C |
| `C3` | B | B | A | A |
| `B0 segment` | B | B | B | B |
| `agents composite` | B | B | B | B |
| `PMM k=10` | B | B | B | B |
| `E2 regression contexte tirage` | B | B | B | B |
| `IM m=10 mode des m` | C | C | C | C |

La lecture de i3 tient : **C ne voit que la fabrication qui conditionne sur le groupe nomme**,
**B est la statistique de l'auditeur aveugle**, la seule qui attrape a la fois l'agent riche,
les deux imputations par tirage et l'adversaire nul.

**Le fait de methode le plus utile de cette section.** L'exposant de la loi `s0 = c x N^(-p)`
n'est pas 0,5 pour tout le monde [MESURE, `i3b-reference-par-taille.csv`] :

| statistique | `p` | `R^2` |
|---|---|---|
| A, deficit de patrons | **0,131** | 0,985 |
| B, exces de correlation | **0,230** | 0,892 |
| C, concentration | **0,478** | 0,998 |
| P, polarisation | **0,507** | 0,970 |

C et la polarisation suivent la racine, exactement. **A et B ne la suivent pas**, et ce n'est
pas un defaut de mesure : ce sont des statistiques dont la **valeur** depend de l'effectif, le
nombre de patrons distincts saturant et le biais d'echantillonnage de la correlation se
resorbant. La reference humaine de A passe de moins 0,0370 a 300 a moins 0,0684 a 1 052, et
celle de B de 0,0337 a 0,0422. **Un institut ne peut donc pas transporter une bande mesuree sur
1 000 personnes vers un flux de 300 : il doit recalculer la bande a sa taille.** C'est le point
operationnel de tout le rapport et il n'etait dans aucune version de i3.

### 3.3 Ce que devient le tableau 5 de i3

Sous le seuil de i3, famille de 27, a 1 052 personnes, les deux rapports se comparent ligne a
ligne [MESURE] :

| fabricant | `tau*` publie par i3 | `tau*` de i3b | rapport |
|---|---|---|---|
| `agents v8` | 1,9 % | **2,7 %** | 1,40 |
| `C2` | 3,6 % | **4,3 %** | 1,20 |
| `B0 segment` | 6,4 % | **11,2 %** | **1,75** |
| `agents demographiques (v6)` | 6,6 % | **10,1 %** | **1,52** |
| `C3` | 6,7 % | **9,0 %** | 1,34 |
| `IM m=10` | 11,1 % | **16,4 %** | 1,48 |
| `agents composite` | 11,5 % | **19,1 %** | **1,66** |
| `PMM k=10` | 21,9 % | **41,0 %** | **1,87** |
| `E2 regression contexte tirage` | 24,6 % | **43,2 %** | **1,76** |

**i3 etait optimiste d'un facteur 1,2 a 1,9, et la raison est entierement dans le bruit de
reference.** i3 sous echantillonne a `m = 526` avec trois replicats nuls puis multiplie par
`racine(m / N) = 0,707`. Deux effets s'y compensent mal. **Pour une statistique dont l'ecart
type decroit en `1 / racine(N)`, le facteur correct pour passer d'un sous echantillon de 526
tire sans remise dans 1 052 a un echantillon frais de 1 052 vaut `1,000` et non `0,707`** : le
tirage sans remise perd deja un facteur `racine(1 - 526 / 1052) = 0,707` par correction de
population finie, qui annule exactement le gain de taille. Et trois replicats nuls gonflent
l'ecart type mesure. i3 avait valide
cette mise a l'echelle par son controle 1.6 et le controle passait ; il passait parce que les
deux erreurs se compensaient sur des populations nulles, ou A vaut zero. **i3b mesure `s0` a
chaque taille avec quinze replicats nuls et separe les deux sources de variance ; son controle
passe aux trois tailles et pour les trois statistiques.** Consequence pratique :

**A 5 pour cent de contamination, sur 1 052 personnes, sous Holm et en bilateral, le detecteur
signale les deux agents a etiquette ideologique, `agents v8` (`z` de moins 3,18 sur A et plus
4,54 sur C) et `C2` (moins 3,36 et plus 5,09), et rien d'autre.** L'adversaire nul, que i3
signalait a 5 pour cent, ne l'est plus : son `z` sur B vaut moins 1,82 contre un seuil de 2,394
[MESURE]. **Il faut 9,2 pour cent pour le voir, pas 6,4.**

### 3.4 Ce que l'on peut dire a 5 000 et ce qui exige une seconde population

L'extrapolation n'est acceptee que pour les couples (fabricant, statistique) dont la courbe
d'effet est stable en `N`, critere declare : le rapport entre l'effet a 300 et l'effet a 1 052,
lu a 10 pour cent de contamination, doit tomber dans [0,80 ; 1,25]. **Sur les 27 couples des neuf
fabricants, 16 passent et 11 sont refuses** [MESURE, `i3b-abaque-extrapolee.csv`]. Les refus ne
sont pas aleatoires : ils frappent **A six fois sur neuf**, B trois fois et C deux fois. **La
statistique qui s'extrapole le mieux est C**, sept sources sur neuf, ce qui est coherent avec
son exposant de 0,478 ; **A, dont l'exposant vaut 0,131, est celle qui resiste**.

Ce que cela donne :

- **`agents v8` a 5 000 repondants : 1,06 pour cent** [PROBABLE]. La prediction P2 annoncait
  « sous 1 pour cent » ; elle est **fausse, de peu**.
- **`E2` a 5 000 : 24,8 pour cent** [PROBABLE]. La seconde moitie de P2, « au dessus de
  10 pour cent », est **tenue**, et largement.
- `PMM k=10` est le seul cas ou l'extrapolation remonte avant de redescendre, 60,7 pour cent a
  1 500 contre 33,3 mesures a 1 052 : sa seule statistique extrapolable est C, dont la courbe
  d'effet est plate, et le resultat n'est pas croyable. **Cette case est a lire comme un refus
  deguise.**

**Ce qui exige une seconde population humaine, dit en clair.** Trois choses, et aucune ne
s'achete avec du calcul. Un, la valeur de reference de A et de B a 5 000 personnes, qui n'est
pas celle de 1 052 puisque ces statistiques dependent de l'effectif ; on ne peut pas la deviner,
il faut la mesurer sur 5 000 vraies personnes. Deux, le bruit de reference `s0(5 000)` : la loi
de puissance est ajustee sur trois points entre 300 et 750 et rien ne garantit qu'elle tienne
sur une decade. Trois, l'independance du fond : ici la reference humaine **est** la population
qui sert de fond au flux, ce qui rend tous les `tau*` optimistes d'une quantite non mesuree,
limite deja ecrite par i3 et que ce rapport ne leve pas.


---

## 4. La bande est elle la meme ailleurs ? Twin-2K-500

2 058 personnes, 108 items categoriels de la vague 4, treize configurations produites par une
autre equipe avec GPT-4.1, GPT-4.1-mini et Gemini-Flash-2.5, sous licence libre. Le fond du
flux et la reference sont les humains des **vagues 1 a 3** ; le controle de fausse alarme est
le **retest de la vague 4**, melange aux memes taux comme s'il etait un fabricant. La
segmentation est l'ideologie politique a cinq niveaux, analogue exact des sept niveaux du GSS.
Les vingt sous ensembles de dix items sont tires parmi les **60 items renseignes pour tous les
sujets**, seuil declare de 99 pour cent atteint sans repli.

### 4.1 Tableau 3 : la bande humaine sur deux jeux, a la meme taille

[MESURE, `i3b-reference-par-taille.csv` et `i3b-twin-reference.csv`, lues a N = 1 052 des deux
cotes pour que la comparaison soit a effectif egal]

| | GSS, 1 052 personnes, 149 items | Twin, 1 052 personnes, 108 items | rapport |
|---|---|---|---|
| **A**, deficit de patrons | **-0,0684** | **-0,0278** [-0,0318 ; -0,0239] | 2,5 |
| **B**, exces de correlation | **+0,0422** | **+0,0227** [0,0208 ; 0,0243] | 1,9 |
| **C**, concentration | **0,0272** | **0,0115** [0,0107 ; 0,0122] | 2,4 |
| **P**, ecart entre camps | **+0,4505** | **+0,2122** [0,1983 ; 0,2274] | 2,1 |

Les valeurs du GSS a 1 052 sont celles de la population entiere et n'ont pas d'intervalle : on
ne peut pas sous echantillonner une population dans elle meme a sa propre taille. Les
intervalles de Twin a 1 052 viennent de 200 sous echantillons corriges.

**La reponse est oui sur les deux bords, et non sur les niveaux.** Les quatre quantites ont le
**meme signe** sur les deux jeux : de vraies personnes ont moins de patrons que leur propre nul,
plus de correlation residuelle, une concentration positive et un ecart entre camps positif. Les
niveaux different d'un facteur 1,9 a 2,5, ce qui est un ordre de grandeur au sens ou l'on
l'entend ici, mais **pas au sens ou un institut pourrait transporter un nombre d'un
questionnaire a l'autre**. La bande est une forme, pas une valeur.

**Le meilleur controle du rapport est ici.** Les memes 2 058 personnes reinterrogees a la
vague 4 donnent A = -0,0438, B = +0,0282, C = 0,0080, P = +0,2112, contre -0,0410, +0,0260,
0,0085 et +0,2126 pour la reference des vagues 1 a 3 [MESURE, `i3b-twin-sources-pures.csv`].
Melangees au flux comme un fabricant, elles ne declenchent **jamais** le detecteur : `|z|`
maximal **0,40** sur les trois statistiques et les quatre taux jusqu'a 50 pour cent, contre un
seuil de 3,220 [MESURE]. **Un retest humain reel, sur un autre jeu que celui de i3, est
indistinguable de la population de reference.**

### 4.2 Tableau 4 : les treize configurations sont toutes du cote pauvre sur A, et six sont du cote libre sur B

[MESURE, `i3b-twin-sources-pures.csv`, taux 100 pour cent, N = 2 058 sauf mention]

| configuration | A | B | C | P, facteur |
|---|---|---|---|---|
| *humains vagues 1 a 3, reference* | ***-0,0410*** | ***+0,0260*** | ***0,0085*** | ***1,00*** |
| *humains vague 4, retest* | *-0,0438* | *+0,0282* | *0,0080* | *0,99* |
| `LLM Finetuning (500 exemples)`, 1 558 sujets | **-0,7926** | **+0,2459** | **0,4326** | **0,65** |
| `JSON Persona (Predicted Output) - GPT4.1`, 2 050 | -0,2468 | +0,0321 | 0,0266 | 1,28 |
| `JSON Persona - GPT4.1` | -0,2426 | +0,0358 | 0,0388 | 1,19 |
| `Persona Summary - JSON Persona - GPT4.1-mini` | -0,2265 | +0,0581 | 0,1015 | 0,90 |
| `JSON Persona (Predicted Output) - GPT4.1-mini` | -0,2058 | **+0,0176** | 0,0592 | 0,94 |
| `JSON Persona - GPT4.1-mini`, 1 000 sujets | -0,1992 | +0,0705 | 0,0374 | 1,05 |
| `Persona Summary - GPT4.1-mini` | -0,1903 | +0,0390 | 0,0648 | 0,89 |
| `Text Persona - GPT4.1-mini` | -0,1563 | **+0,0250** | 0,0505 | 1,13 |
| `Text Persona (Repeating Questions) - GPT4.1-mini` | -0,1284 | **+0,0246** | 0,0298 | 1,20 |
| `Demographics Only - GPT4.1-mini` | -0,1265 | +0,0288 | 0,1006 | **0,75** |
| `Text Persona (Default Temperature) - GPT4.1-mini` | -0,0919 | **+0,0186** | 0,0341 | 1,11 |
| `Text Persona (Reasoning) - GPT4.1-mini` | -0,0918 | **+0,0215** | 0,0198 | 1,15 |
| `Text Persona - Gemini-Flash2.5` | -0,0842 | **+0,0186** | 0,0191 | 1,21 |

**Le fait nouveau que le GSS ne montrait pas.** Sur le GSS, toutes les conditions a modele de
langage sont a la fois **trop pauvres sur A** et **trop couplees sur B** : les deux bords sont
alignes. **Sur Twin, six configurations sur treize sont trop pauvres sur A et trop LIBRES sur
B** : `Text Persona` et ses trois variantes, la version Gemini, et
`JSON Persona (Predicted Output) - GPT4.1-mini`, toutes en dessous de l'exces de correlation
humain de 0,0260. **Un meme fabricant peut donc occuper les deux bords de la bande en meme
temps, sur deux statistiques differentes.** C'est le meilleur argument mesure en faveur du test
bilateral applique statistique par statistique, et c'est un argument que i3 ne pouvait pas
produire, ses agents etant tous du meme cote sur les deux.

La prediction P3 est **tenue sur ses deux moities** : les deux bords humains ont le meme signe
sur les deux jeux, et les treize configurations sont toutes du cote pauvre sur A.

### 4.3 Tableau 5 : le plus petit taux detectable sur Twin

[MESURE, `i3b-twin-abaque.csv`, meilleure des trois statistiques]

| configuration | Holm(39), N = 2 058 | Holm(39), N = 1 052 | Holm(3), N = 1 052 |
|---|---|---|---|
| `LLM Finetuning (500 exemples)` | **0,43 %** | 0,63 % | 0,50 % |
| `Persona Summary - JSON Persona` | 1,98 % | 2,50 % | 2,00 % |
| `Demographics Only - GPT4.1-mini` | 2,07 % | 2,77 % | 2,20 % |
| `Persona Summary - GPT4.1-mini` | 3,05 % | 3,97 % | 3,16 % |
| `JSON Persona (Predicted Output) - GPT4.1-mini` | *4,22 %* | *5,48 %* | *4,40 %* |
| `Text Persona - GPT4.1-mini` | 6,12 % | 9,20 % | 7,52 % |
| `JSON Persona (Predicted Output) - GPT4.1` | *6,60 %* | *11,06 %* | *9,25 %* |
| `JSON Persona - GPT4.1` | 7,25 % | 10,80 % | 8,94 % |
| `Text Persona - Gemini-Flash2.5` | 8,43 % | 10,56 % | 8,44 % |
| `JSON Persona - GPT4.1-mini` | 8,77 % | 11,95 % | 10,15 % |
| `Text Persona (Reasoning)` | 9,36 % | 12,22 % | 9,84 % |
| `Text Persona (Default Temperature)` | 10,24 % | 13,81 % | 11,16 % |
| `Text Persona (Repeating Questions)` | 12,88 % | 15,66 % | 12,56 % |
| *`humains vague 4`, controle* | *jamais* | *jamais* | *jamais* |

Les deux lignes en italique sont celles dont le controle de masque echoue, ecart E4 ; elles ne
sont pas comparables aux onze autres.

**Ce que ce tableau dit et que le GSS ne disait pas.**

**Un.** L'ecart entre la configuration la plus detectable et la moins detectable vaut un facteur
**30** sur le meme jeu, le meme questionnaire et la meme population : 0,43 pour cent contre
12,88 pour cent. La prediction P4 est **tenue sur ses deux moities**, une configuration sous
5 pour cent et un rapport superieur a 3, et elle l'est tres largement.

**Deux.** **Le reglage compte plus que le modele.** Les quatre variantes de `Text Persona` en
GPT-4.1-mini, qui different par la temperature, le raisonnement et la repetition des questions,
s'etalent de 6,1 a 12,9 pour cent ; et le passage de GPT-4.1-mini a Gemini-Flash-2.5 sur la
meme invite donne 8,4 contre 6,1. **La detectabilite d'un simulateur est une propriete de son
pipeline, pas de son modele**, ce qui est exactement ce qu'une norme d'audit doit pouvoir
constater sans connaitre le pipeline.

**Trois.** **Le reglage fin est le pire de tous.** `LLM Finetuning`, affine sur 500 exemples
reels, a un deficit de patrons de **79,3 pour cent** et une concentration de **0,433** contre
0,0085 chez les humains : il est detecte a **0,43 pour cent de contamination**, c'est a dire
9 lignes sur 2 058. C'est le generateur le plus degenere de tout le dossier, plus que
`agents v8`. L'affinage a appris la reponse modale de chaque item et il ne produit presque plus
de personnes.

**Quatre.** A 5 pour cent de contamination et sous Holm sur la famille de 39,
**quatre configurations sur treize sont signalees** : `LLM Finetuning` (les trois statistiques,
`z` de -14,9, +8,9 et +42,4), `Persona Summary - JSON Persona` (les trois, -5,27, +7,29,
+3,58), `Demographics Only` (A et B, -4,48 et +6,54) et `Persona Summary` (B seule, `p` de Holm
0,0095). Les cinq `Text Persona` et les `JSON Persona` en GPT-4.1 passent [MESURE]. **La
proportion, quatre sur treize a 5 pour cent, est du meme ordre que sur le GSS, deux sur neuf.**

### 4.4 Le resultat d'I4 se transporte, et il se transporte sous sa forme corrigee

[MESURE, `i3b-twin-melanges.csv`, facteur de polarisation a 50 pour cent de contamination]

Sur le GSS, i3 a montre que le signe du biais de polarisation est fixe par **l'etiquette
ideologique recue ou non**, et pas par le mode de fabrication. Twin ne contient aucune
configuration qui recoive une etiquette ideologique explicite ; il contient des configurations
qui recoivent **des demographies seules**, et d'autres qui recoivent **un profil riche** ou
l'attitude politique est noyee dans un texte. La prediction que la variable corrigee d'I4
implique est donc : les premieres aplatissent, les secondes gonflent moderement.

| configuration | facteur a 50 % | correspondance sur le GSS |
|---|---|---|
| `LLM Finetuning` | **0,65** | plus aplatissant que `v6` |
| `Demographics Only - GPT4.1-mini` | **0,75** | `agents v6`, 0,78 |
| `Persona Summary` et `Persona Summary - JSON Persona` | 0,89 et 0,90 | entre `v6` et `C3` |
| `JSON Persona (Predicted Output) - GPT4.1-mini` | 0,94 | `C3`, 0,95 |
| `Text Persona` et ses variantes, Gemini | 1,11 a 1,21 | `agents composite`, 1,21 |
| `JSON Persona - GPT4.1` et `(Predicted Output)` | 1,19 et 1,28 | `agents composite` |

**C'est la meme carte, sur d'autres personnes, d'autres items, d'autres auteurs et d'autres
modeles** : les demographies seules aplatissent l'ecart entre camps de 25 pour cent, le profil
riche le gonfle de 10 a 28 pour cent. Aucune configuration de Twin n'atteint le facteur 1,76 de
`agents v8`, et c'est coherent : aucune ne recoit le camp nomme en clair. **Le facteur 1,76 de
i3 est donc bien l'effet du groupe nomme, et non l'effet d'un profil riche** [MESURE pour les
deux jeux, la lecture conjointe etant PROBABLE].

---

## 5. La contamination concentree sur un seul camp

C'est le cas reel d'une operation d'influence : les faux repondants ne sont pas repartis au
hasard, ils sont tous du camp que l'on veut faire paraitre majoritaire. Le taux `tau` reste la
part du **flux entier** remplacee, aux cinq valeurs 2, 5, 10, 20 et 30 pour cent ; les faux
repondants sont tires uniquement dans le bloc vise. Effectifs des blocs : gauche 417, centre
303, droite 332, sur 1 052 [MESURE]. Deux lectures sont publiees : **globale**, les trois
statistiques sur le flux entier, ce que fait un auditeur qui ne sait pas ou chercher ; et
**par camp**, les trois statistiques sur les seules personnes du bloc vise, avec leur propre
bande et leur propre `s0` a la taille du bloc.

### 5.1 Tableau 6 : le plus petit taux total detectable, concentre contre uniforme

[MESURE, `i3b-camp-detection.csv`, camp vise **droite**, Holm sur la famille de trois]

| fabricant | concentre, lecture par camp | concentre, lecture globale | uniforme, lecture par camp | uniforme, lecture globale |
|---|---|---|---|---|
| `agents v8` | **0,69 %** | 1,78 % | 3,29 % | 2,85 % |
| `C2` | **1,88 %** | 3,82 % | 7,17 % | 4,13 % |
| `agents demographiques (v6)` | **2,16 %** | 6,47 % | 10,15 % | 8,92 % |
| `C3` | **3,42 %** | 12,22 % | 9,90 % | 7,90 % |
| `B0 segment` | **3,51 %** | 9,04 % | 11,47 % | 9,24 % |
| `agents composite` | **4,10 %** | 14,12 % | 15,04 % | 16,23 % |
| `IM m=10` | **8,48 %** | 17,28 % | 25,35 % | 13,45 % |
| `E2 regression contexte tirage` | **12,89 %** | 39,86 % | 37,42 % | 37,04 % |
| `PMM k=10` | **16,28 %** | 34,29 % | 53,37 % | 32,04 % |
| *`humains vague 2`, controle* | *64,7 %* | *jamais* | *96,8 %* | *68,2 %* |

**Le resultat operationnel de la section, en une phrase : un auditeur qui recalcule les trois
statistiques a l'interieur de chaque camp voit une operation concentree a un taux total trois a
cinq fois plus bas qu'un auditeur qui lit le flux entier.** Pour l'agent a etiquette
ideologique, 0,69 pour cent du flux total contre 1,78 ; pour l'agent a demographies, 2,16
contre 6,47 ; pour l'imputation par tirage la plus difficile, 12,9 contre 39,9. Le facteur
correspond a ce qu'on attend : concentrer `tau x 1052` faux repondants dans un bloc de 332
personnes porte le taux **local** a `3,17 x tau`, et la lecture par camp voit ce taux local.

**La prediction P5 est a moitie tenue et a moitie fausse.** La moitie tenue : la lecture par
camp detecte une contamination concentree a un taux total plus bas que la lecture uniforme, sur
les neuf fabricants sans exception, et le facteur est de 2,9 a 4,7. **La moitie fausse : la
lecture globale n'est pas systematiquement moins sensible a la contamination concentree.** Sur
cinq fabricants sur neuf, `agents v8`, `C2`, `agents composite`, `agents demographiques (v6)` et
`B0 segment`, la contamination concentree est **plus** detectable globalement que la
contamination uniforme, parce qu'elle detruit la structure d'un segment entier au lieu de la
diluer sur sept. Sur les quatre autres, `C3`, `IM`, `PMM` et `E2`, elle l'est moins. **Il n'y a
donc pas de regle simple pour l'auditeur aveugle ; il y en a une pour l'auditeur averti, et
elle est de calculer par segment.**

**Le controle de fausse alarme tient dans les deux lectures.** Remplacer les vraies personnes
d'un camp par les memes personnes reinterrogees deux semaines plus tard ne declenche jamais la
lecture globale, et demande 64,7 pour cent de contamination totale pour declencher la lecture
par camp [MESURE].

### 5.2 Tableau 7 : ce que l'operation deplace, a taux total egal

[MESURE, `i3b-camp-polarisation.csv`, facteur de l'ecart entre camps, camp vise droite]

| fabricant | 2 % conc. | 10 % conc. | 30 % conc. | 10 % unif. | 30 % unif. |
|---|---|---|---|---|---|
| **`agents v8`** | **1,061** | **1,276** | **1,799** | 1,157 | 1,447 |
| `agents composite` | 1,013 | 1,071 | 1,199 | 1,040 | 1,129 |
| `PMM k=10` | 1,005 | 1,023 | 1,074 | 1,015 | 1,049 |
| `IM m=10` | 1,000 | 1,000 | 0,994 | 1,015 | 1,045 |
| `B0 segment` | 0,998 | 1,002 | 1,001 | 0,999 | 0,992 |
| `E2 regression` | 0,996 | 0,994 | 0,974 | 0,992 | 0,981 |
| **`agents demographiques (v6)`** | **0,961** | **0,814** | **0,416** | 0,956 | 0,861 |
| *`humains vague 2`* | *1,002* | *1,003* | *1,010* | *1,002* | *0,998* |

**A taux total egal, la contamination concentree deplace l'ecart entre camps beaucoup plus fort
que la contamination uniforme, et pour les deux fabricants qui deplacent quelque chose, le
facteur va du simple au double.** `agents v8` porte l'ecart a 1,80 fois sa valeur humaine a
30 pour cent concentre contre 1,45 uniforme ; `agents v6` le ramene a **0,42** contre 0,86.
Trente pour cent de faux repondants d'un seul camp, fabriques par un agent qui recoit des
demographies sans ideologie, **effacent 58 pour cent de l'ecart mesure entre camps**. La
troisieme moitie de P5 est donc **tenue** [MESURE].

Un fait qui n'etait pas prevu : **le sens du deplacement ne depend pas du camp vise.** Viser la
gauche avec `agents v8` porte l'ecart a 1,46 a 30 pour cent, viser la droite le porte a 1,80 ;
les deux **gonflent**. La raison est celle d'I4 : l'agent recoit l'etiquette de la personne
qu'il remplace, il rend donc le camp vise plus caricatural quel qu'il soit, et l'ecart entre
camps monte des deux cotes [MESURE].

### 5.3 La marginale, qui est ce qu'un institut publie

Sur `letin1a`, l'item au plus grand ecart entre camps chez les humains, la part de la modalite
modale humaine « remain the same as it is » vaut **33,65 pour cent**. Une operation concentree
sur la droite avec `agents demographiques (v6)` la porte a **+15,7 points, soit 49,4 pour cent**,
a 30 pour cent de contamination ; a 10 pour cent elle la porte deja de **+4,96 points**
[MESURE]. Or ce fabricant est detecte a **6,47 pour cent** en lecture globale : **il existe donc
une fenetre, entre 0 et 6,5 pour cent de contamination totale, ou un institut publierait un
mouvement de trois points sur son item le plus politique sans qu'aucun controle structurel ne
se declenche.** C'est la section 7 qui met un chiffre sur toutes ces fenetres.

---

## 6. Le fabricant qui vise la bande, et ce que vaut la statistique gardee en reserve

i3 ecrit en section 7.3 point 2 qu'un fabricant qui viserait la valeur humaine des trois
statistiques ne serait pas detecte, et le classe honnetement [HYPOTHESE] : « c'est un
raisonnement, pas une mesure ». Cette section le construit et le mesure.

### 6.1 Le dispositif : trois populations disjointes

Les 1 052 personnes sont partagees une fois pour toutes, a la graine du projet, en **`H_A`, 526
personnes**, le fond du flux, **`H_B`, 263 personnes**, les microdonnees de reference de
l'**auditeur**, et **`H_C`, 263 personnes**, les microdonnees volees de l'**adversaire**.
Intersections verifiees nulles [CONFIRME]. Le flux travaille donc a N = 526, et la bande des cinq
statistiques y est mesuree sur **300 partitions aleatoires du meme type**.

| statistique | valeur humaine a N = 526 | IC a 95 pour cent | `s0` |
|---|---|---|---|
| **A** | -0,05125 | [-0,05852 ; -0,04502] | 0,004502 |
| **B** | +0,03763 | [0,03514 ; 0,03994] | 0,001765 |
| **C** | 0,03496 | [0,03318 ; 0,03679] | 0,001282 |
| **R1**, ordre trois | **+0,003510** | [0,00259 ; 0,00435] | 0,000635 |
| **R2**, distance au plus proche voisin humain | **0,34130** | [0,33859 ; 0,34404] | 0,002118 |

**R1 n'est pas nulle chez de vraies personnes** : +0,00351, soit **5,5 ecarts types au dessus de
zero**. Il existe donc bien une structure a l'ordre trois dans un vrai jeu de reponses, que la
matrice de correlation ne contient pas et que ni le generateur nul ni un modele a dependance de
paires ne produit. C'etait le pari de la statistique de reserve, et il est gagne sur ce point la.

### 6.2 Le fabricant `A*`, qui ne connait que les marges publiees

`A*` tire `m` archetypes par segment dans les marginales publiees `p_{j,g}^beta`, donne un
archetype a chaque faux repondant, lui fait garder la reponse de son archetype avec la
probabilite `rho` et retirer une valeur fraiche sinon. **Il n'a aucune microdonnee** : `m`, `rho`
et `beta` plus des tableaux croises item par segment, c'est tout ce qu'il lui faut. La grille de
calibration compte 180 points pour `A*` et 45 pour la variante a microdonnees, deux tirages par
point, evalues sur une population entierement fabriquee de 526 lignes.

**Resultat de calibration, et il contredit la prediction P6** [MESURE,
`i3b-adversaire-calibration.csv`] :

| point | `m` | `rho` | `beta` | A | B | C | ecart max A, B |
|---|---|---|---|---|---|---|---|
| meilleur sur A et B, `A* deux cibles` | 2 | 0,60 | 1,2 | -0,0664 (**3,36 `s0`**) | 0,0352 (1,35 `s0`) | 0,1030 (53 `s0`) | **3,36** |
| meilleur sur les trois, `A* trois cibles` | 8 | 0,60 | 0,8 | -0,0571 (1,31 `s0`) | 0,0225 (8,57 `s0`) | 0,0391 (3,24 `s0`) | 8,57 |
| meilleur sur B seule | 3 | 0,60 | 1,0 | -0,0828 (7,01 `s0`) | **0,0379 (0,14 `s0`)** | 0,0714 | 7,01 |
| meilleur sur A seule | 2 | 0,50 | 1,0 | **-0,0436 (1,71 `s0`)** | 0,0253 (7,00 `s0`) | 0,0551 | 7,00 |
| meilleur `A**`, avec microdonnees | -- | 0,70 | 1,1 | -0,0535 (0,51 `s0`) | 0,0215 (9,15 `s0`) | 0,0393 | 9,15 |

**La prediction P6 est fausse sur sa premiere moitie : aucun point de la grille ne met A et B a
moins d'un ecart type des valeurs humaines en meme temps.** La famille sait viser A seule
(1,71 `s0`) ou B seule (0,14 `s0`), pas les deux : le parametre qui cree le deficit de patrons,
la copie d'archetype, cree aussi de la correlation residuelle, et les deux cibles ne sont pas
independantes. **Le meilleur compromis est a 3,36 ecarts types de la bande. Un adversaire libre
qui a lu i3 et qui dispose de trois boutons ne rentre pas dans la bande.** Il faudrait une
famille plus riche, et c'est une borne sur **cet** adversaire, pas sur tous.

### 6.3 Ce qu'il obtient quand meme, et ce que valent les statistiques de reserve

[MESURE, `i3b-adversaire-detection.csv`, `tau*` a puissance 80 pour cent, Holm sur la famille de
cinq, N = 526. En gras la meilleure statistique pour chaque fabricant.]

| fabricant | cout | A | B | C | **R1** | **R2** | meilleure |
|---|---|---|---|---|---|---|---|
| `agents v8`, gabarit a etiquette | gratuit | 5,5 % | 7,9 % | **3,5 %** | 8,1 % | 12,1 % | **3,5 %** |
| `B0 segment`, tirage dans les marges | gratuit | 17,7 % | **10,6 %** | 82,9 % | jamais | 23,8 % | **10,6 %** |
| **`A* trois cibles`** | gratuit | 23,8 % | **10,0 %** | 96,7 % | 73,9 % | 13,3 % | **10,0 %** |
| **`A* deux cibles`** | gratuit | 49,3 % | **13,7 %** | 19,5 % | 47,9 % | 45,5 % | **13,7 %** |
| **`A** microdonnees`** | **263 vraies lignes** | 97,9 % | **21,2 %** | 85,8 % | 84,5 % | 50,5 % | **21,2 %** |
| `E2 regression contexte tirage` | un panel entier | jamais | **35,1 %** | jamais | jamais | 59,0 % | **35,1 %** |
| `PMM k=10` | un panel entier | 61,1 % | 46,9 % | jamais | 81,2 % | **35,0 %** | **35,0 %** |

**Quatre resultats, et trois sont negatifs pour la norme.**

**Un, l'echelle de cout est mesuree, et elle est celle que le brainstorm annoncait, avec des
chiffres.** Un gabarit gratuit est vu a 3,5 pour cent ; un tirage dans les marges publiees,
gratuit aussi, a 10,6 ; le meme tirage regle pour viser la bande, toujours gratuit, a
**13,7 pour cent** ; le meme avec **263 vraies lignes volees, a 21,2 pour cent** ; une imputation
par tirage sur un panel entier, a 35 pour cent. **Viser la bande sans microdonnees fait gagner un
facteur 1,3 sur l'invisibilite par rapport a l'adversaire nul ; voler 263 lignes reelles fait
gagner un facteur 2,0.** C'est le premier chiffrage du cout de la fraude en repondants, et il
dit que **les microdonnees reelles achetent bien de l'invisibilite, mais un facteur deux, pas un
ordre de grandeur**.

**Deux, la statistique de reserve a l'ordre trois ne sert a rien contre ces adversaires.** R1
voit tres bien le gabarit a etiquette, 8,1 pour cent, mais elle ne voit **jamais** l'adversaire
nul, et elle demande 47,9 a 84,5 pour cent pour les trois adversaires qui visent la bande, contre
10,0 a 21,2 pour cent pour B, qui est **publiee**. **La reponse « une partie des statistiques
reste en reserve » ne tient pas telle quelle : la statistique de reserve que nous avions choisie
pour son elegance theorique est strictement dominee par une statistique publiee.** Il faudra
soit une autre reserve, soit abandonner cet etage de la reponse.

**Trois, la statistique qui coute des microdonnees a l'auditeur en gagne sur un seul fabricant.**
R2 est la meilleure des cinq pour `PMM k=10`, 35,0 pour cent contre 46,9 pour B, un gain de
25 pour cent ; ailleurs elle est dominee. **Faire detenir de vraies microdonnees a l'auditeur
n'est donc pas rentable en l'etat.**

**Quatre, et c'est le seul resultat positif de la section : R2 identifie la ROUTE de
fabrication par son signe.** Les fabricants qui tirent dans des marges eloignent le flux des
vraies personnes, R2 monte, `z` de +8,6 pour l'adversaire nul et +14,2 pour `A* trois cibles` a
50 pour cent ; les fabricants qui copient ou predisent de vraies personnes le rapprochent, R2
descend, `z` de -12,4 pour `agents v8` et -4,3 pour `PMM` [MESURE]. **Aucune des trois
statistiques publiees ne separe ces deux routes ; R2 le fait, et c'est peut etre son vrai
emploi : non pas detecter, mais dire de quel genre de fraude il s'agit une fois qu'elle est
detectee.**

### 6.4 La borne, publiee et non annoncee

1. **Un adversaire libre qui a lu i3, qui connait les marges publiees et les valeurs cibles, et
   qui regle trois parametres, ne rentre pas dans la bande** : son meilleur compromis est a
   3,4 ecarts types. **Il gagne quand meme un facteur 1,3 sur l'invisibilite** par rapport a
   l'adversaire nul, 13,7 pour cent contre 10,6, et un facteur **3,9** par rapport au gabarit a
   etiquette, 13,7 contre 3,5. [MESURE]
2. **Voler 263 vraies lignes double l'invisibilite**, de 10,6 a 21,2 pour cent. Le cout impose a
   la fraude est donc reel mais modeste ; il n'y a pas de mur. [MESURE]
3. **La reponse « des statistiques en reserve » est, pour la reserve que nous avons declaree,
   fausse** : R1 est dominee par B partout sauf sur le gabarit, et R2 sur six fabricants sur
   sept. [MESURE]
4. **Ce que la mesure ne dit pas** : qu'aucun adversaire ne puisse rentrer dans la bande. Notre
   famille a trois parametres ; une famille plus riche, ou une optimisation au lieu d'une
   grille, ferait mieux. **La borne publiee ici majore ce que cet adversaire atteint, pas ce qui
   est atteignable.** [HYPOTHESE, explicitement declaree]

---

## 7. La surface d'attaque, ou le prix de l'invisibilite

Pour chaque fabricant, `tau_max` est le plus grand taux auquel il reste sous le seuil de
detection, c'est a dire le `tau*` de la meilleure des trois statistiques publiees sous Holm(3).
Le deplacement maximal non detecte est la valeur des quantites de consequence lue a `tau_max`
sur leur propre ajustement quadratique. Les trois marginales sont celles de la regle mecanique
declaree, les trois items au plus grand ecart entre camps chez les humains :
**`letin1a`** (immigration, modalite modale humaine « remain the same as it is », 33,65 pour
cent), **`racdif1`** (« yes », 52,76 pour cent) et **`natrace/y`** (« about right »,
38,69 pour cent).

### 7.1 Tableau 8 : le prix de l'invisibilite a N = 1 052

[MESURE, `i3b-surface-attaque.csv`. Ecart entre camps en pour cent de la valeur humaine ;
marginales en **points de pourcentage**.]

| fabricant | detecte a | ecart entre camps | `letin1a` | `racdif1` | `natrace/y` |
|---|---|---|---|---|---|
| `agents v8` | 2,2 % | +3,18 % | -0,24 | +0,27 | -0,39 |
| `C2` | 3,8 % | +1,44 % | +0,30 | -0,41 | +0,76 |
| `C3` | 7,9 % | **-3,93 %** | +1,31 | -1,65 | -2,15 |
| **`agents demographiques (v6)`** | 8,6 % | -3,78 % | **+3,78** | **+2,91** | -0,26 |
| `B0 segment`, adversaire nul | 9,2 % | +0,03 % | +0,02 | -0,01 | -0,06 |
| `IM m=10` | 13,5 % | +2,03 % | +0,56 | -0,26 | +0,36 |
| **`agents composite`, riche** | 15,9 % | **+6,34 %** | **+3,27** | -1,39 | **-2,96** |
| `PMM k=10` | 33,3 % | +5,59 % | +0,38 | -0,04 | +0,20 |
| `E2 regression contexte tirage` | 35,4 % | -2,31 % | -0,41 | +0,14 | +0,05 |
| *`humains vague 2`, jamais detecte* | *jamais* | *+0,14 %* | *+0,88* | *-0,53* | *+1,55* |

### 7.2 A N = 300, la meme table, et elle est bien pire

| fabricant | detecte a | ecart entre camps | `letin1a` | `racdif1` | `natrace/y` |
|---|---|---|---|---|---|
| `agents v8` | 4,5 % | +6,44 % | -0,38 | +0,52 | -1,09 |
| `C2` | 5,7 % | +1,76 % | +0,28 | -0,76 | +1,07 |
| `C3` | 10,7 % | -5,87 % | +3,20 | -3,02 | -3,24 |
| `agents demographiques (v6)` | 10,9 % | -3,71 % | **+4,89** | **+3,97** | -1,23 |
| `B0 segment` | 14,8 % | +1,03 % | +0,49 | +0,02 | +0,05 |
| **`agents composite`** | 23,6 % | **+11,17 %** | **+5,15** | -1,58 | **-4,17** |
| `IM m=10` | 25,0 % | +4,12 % | +0,79 | -1,02 | +0,79 |
| `PMM k=10` | 52,5 % | +6,95 % | +0,31 | -0,07 | +0,62 |
| `E2 regression contexte tirage` | 60,2 % | -5,23 % | +1,02 | -0,45 | -0,93 |

### 7.3 Ce que ces deux tableaux disent

**Un, la prediction P7 est fausse sur sa premiere moitie, et la raison est le meilleur resultat
du rapport pour un defenseur.** Le prix de l'invisibilite **n'est pas croissant** avec la
difficulte de detection. Les deux fabricants les plus difficiles a detecter, `PMM` a
33,3 pour cent et `E2` a 35,4, sont des imputations par tirage sur microdonnees reelles : elles
**portent la personne**, donc elles ne deforment presque pas l'agregat. `E2`, invisible jusqu'a
un tiers du flux, ne deplace l'ecart entre camps que de **2,3 pour cent** et les trois
marginales de moins d'un demi point. **Etre invisible et etre utile sont deux proprietes qui
s'opposent** : le fabricant qui ressemble le plus a de vraies personnes deplace le moins, par
construction, puisqu'il **est** presque de vraies personnes. **Le danger n'est ni au bord
gratuit ni au bord cher : il est au milieu, chez l'agent riche.**

**Deux, le maximum est chiffre, et il est petit a 1 052 et grand a 300.** A 1 052 personnes,
aucun fabricant ne peut deplacer l'ecart entre camps de plus de **6,34 pour cent** ni une
marginale publiee de plus de **3,78 points** sans etre vu. La seconde moitie de P7, « sous
10 pour cent de la valeur humaine », est **tenue** [MESURE]. A 300 personnes, le plafond monte a
**11,17 pour cent** sur l'ecart entre camps et **5,15 points** sur une marginale, et P7 serait
fausse. **La taille du flux est la variable de securite, et c'est la chose la moins chere a
changer pour un institut.**

**Trois, l'adversaire nul est le contre exemple parfait de son propre camp.** `B0 segment` reste
invisible jusqu'a 9,2 pour cent et deplace l'ecart entre camps de **0,03 pour cent** et les
marginales de moins d'un dixieme de point. **Il est gratuit, il est difficile a voir, et il ne
sert a rien** : par construction il reproduit les marges, donc il ne peut pas les deplacer.
C'est la reponse mesuree a l'objection « la fraude gratuite suffit » : elle suffit pour gonfler
un volume de reponses, pas pour deplacer une mesure.

**Quatre, le fabricant a surveiller a un nom.** `agents demographiques (v6)`, l'agent qui recoit
des demographies sans ideologie, deplace **+3,78 points** sur l'item le plus politique du
questionnaire tout en restant invisible jusqu'a 8,6 pour cent, et **+4,89 points** a 300
personnes. **Or c'est exactement le mode de contamination reel** que i3 identifie en section 8 :
un vrai repondant qui colle la question dans un assistant sans lui donner son camp. Et la
section 5 montre que concentrer cette contamination sur un camp porte le deplacement a
**+15,7 points** a 30 pour cent, dont **+4,96 points a 10 pour cent** [MESURE].

---

## 8. Les figures

**`resultats/i3b-figure-abaque.png` et `.svg`.** Taille du flux contre plus petit taux
detectable, une courbe par fabricant, echelles logarithmiques, trait plein de 300 a 1 052 pour
la partie mesuree et tirets au dela pour la partie extrapolee, avec le trait vertical qui separe
les deux. Ce que la figure montre et que le tableau dit moins bien : **les neuf courbes sont
presque paralleles et ne se croisent pas**, la hierarchie des fabricants est donc une propriete
du fabricant et non de la taille ; et **la bande des imputations par tirage reste au dessus de
30 pour cent sur toute la plage**, y compris a 5 000 repondants. L'etoile noire isolee en haut a
gauche est le controle humain a 300 personnes, 94,6 pour cent.

**`resultats/i3b-figure-bande-deux-jeux.png` et `.svg`.** Trois panneaux dans le plan (A, B) :
le GSS, Twin en entier, et Twin en zoom autour de la bande. La croix grise a l'origine est le
generateur nul, le rectangle jaune la bande humaine a huit ecarts types, l'etoile la reference.
Ce que la figure montre : **la meme geometrie sur deux jeux independants**, un nuage de
fabricants au nord ouest de la bande, l'origine au sud est, et la reference humaine entre les
deux. Sur le panneau de Twin, le point 14 est le **retest humain de la vague 4** et il est
confondu avec l'etoile : de vraies personnes, un autre jour, tombent sur la bande. Le panneau de
zoom montre le fait que le GSS ne pouvait pas montrer : **six configurations sur treize sont
sous la bande sur B tout en etant a gauche sur A.**

**`resultats/i3b-figure-surface-attaque.png` et `.svg`.** Taux de detection en abscisse
logarithmique contre deplacement maximal non detecte de l'ecart entre camps en ordonnee, a 300
et a 1 052 repondants. Ce que la figure montre : **il n'y a pas de droite montante**. Les points
les plus a droite, PMM et E2, ne sont pas les plus hauts ; le point le plus haut, l'agent riche,
est au milieu ; et l'adversaire nul est sur la ligne du zero. **Le nuage a une forme de cloche,
et le sommet de la cloche est le fabricant qu'un regulateur doit nommer.**

---

## 9. Ce que cela vaut pour un institut ou une administration

**Mode d'emploi, trois phrases.** Sur le fichier livre, calculer les trois statistiques
publiees, deficit de patrons, exces de correlation residualisee et concentration par segment,
chacune contre le generateur nul du fichier lui meme, et les comparer **en bilateral** a la
bande d'un echantillon humain de reference **de la meme taille et du meme questionnaire** ;
recalculer les trois **a l'interieur de chaque camp** en plus du flux entier, ce qui divise par
trois a cinq le taux total detectable quand la fraude est concentree ; et signaler le fichier
des qu'une des lectures sort de la bande. Sur nos donnees, cela attrape un agent a etiquette a
partir de **2,2 pour cent** sur 1 052 repondants et **4,5 pour cent** sur 300, un agent a
demographies a partir de **8,6** et **10,9**, un tirage dans les marges publiees a partir de
**9,2** et **14,8**, une imputation par tirage a partir de **33** et **52**, sans jamais se
declencher sur un panel humain reel reinterroge, ni sur le GSS ni sur Twin-2K-500. Le plancher
absolu du dispositif est la taille du flux : **sous 300 repondants, il n'y a rien a esperer, et
le seul levier bon marche dont dispose un commanditaire est d'augmenter son effectif.**

**Limites, trois phrases.** Le chiffre produit reste **un plancher de contamination de type
gabarit et non une part**, et un « zero detecte » ne doit jamais se lire « fichier propre » :
i3 a mesure que l'estimateur aveugle sous evalue d'un facteur 2,5 a 10 et rend zero pour les
fabricants plus libres que de vraies personnes, et i3b n'a pas ameliore cette quantification.
La bande **ne se transporte pas d'un questionnaire a l'autre ni d'une taille a l'autre** : les
valeurs humaines de A et de B changent avec l'effectif, la reference du GSS et celle de Twin
different d'un facteur deux, et un institut qui appliquerait un seuil publie ailleurs se
tromperait. Enfin, **un adversaire qui vise la bande gagne un facteur 1,3 sur l'invisibilite
sans microdonnees et un facteur 2 avec 263 lignes reelles volees, et la statistique de reserve
que nous avions declaree ne le rattrape pas** : la norme protege contre la fraude paresseuse et
contre la fraude moyenne, pas contre un adversaire informe qui accepte de deplacer peu.

---

## 10. Ce que je n'ai pas pu verifier

1. **Aucun fichier reel a contamination documentee**, ni sur le GSS ni sur Twin. Toutes les
   courbes de ce rapport sont des simulations de contamination. C'est la limite qui rend le
   travail publiable comme methode et pas comme mesure, et c'est la meme que celle de i3.
2. **Une seule population humaine de reference par jeu, et c'est elle qui sert de fond au
   flux.** Un auditeur reel aurait une reference externe, dont le bruit s'ajouterait au sien.
   **Tous les `tau*` de ce rapport restent optimistes d'une quantite non mesuree.** La section 6
   est la seule qui echappe partiellement a ce defaut, sa reference R2 etant disjointe du flux.
3. **Au dela de 1 052 sur le GSS et de 2 058 sur Twin, rien n'est mesure.** L'extrapolation est
   une loi de puissance ajustee sur trois points entre 300 et 750, avec un exposant qui vaut
   0,13 pour A et 0,23 pour B au lieu de 0,5, et un test de stabilite de la courbe d'effet qui
   **refuse douze couples sur vingt sept**. La colonne 5 000 est [PROBABLE] et la ligne `PMM` y
   est incoherente, ce qui est signale.
4. **Le fabricant qui vise la bande est le notre, avec trois parametres et une grille de 180
   points.** Une famille plus riche ou une optimisation continue ferait mieux, peut etre
   beaucoup mieux. **La borne de la section 6.4 majore ce que cet adversaire atteint, pas ce qui
   est atteignable**, et c'est la limite la plus serieuse du rapport.
5. **Les statistiques de reserve sont deux, et elles ont ete choisies avant de mesurer.** Le
   fait qu'elles ne servent pas ne prouve pas qu'aucune reserve ne servirait ; il prouve que ces
   deux la ne servent pas. Une reserve utile devrait viser ce que la famille `A*` ne controle
   pas, et il faudrait la construire **apres** avoir vu l'adversaire, ce qui pose un probleme de
   preenregistrement qu'il faudra trancher.
6. **Deux configurations de Twin echouent au controle de masque**, dont une largement,
   9,92 pour cent de cellules perdues. Leurs `tau*` figurent dans les tableaux, en italique, et
   ne sont comparables a rien.
7. **La segmentation est unique sur chaque jeu**, sept niveaux d'ideologie sur le GSS, cinq sur
   Twin. La sensibilite du detecteur a la segmentation n'est toujours pas mesuree, limite 3 de
   i3 que ce rapport ne leve qu'a moitie : il change de questionnaire, pas de facon de decouper.
8. **La contamination concentree n'est testee que sur des blocs ideologiques.** Une operation
   reelle pourrait cibler une tranche d'age, une region, ou un croisement ; rien ici ne le dit.
9. **Le second camp n'est calcule que pour cinq fabricants sur neuf**, comme le preenregistrement
   l'annonce. Les quatre autres n'ont que le camp droite.
10. **Rien sur le texte libre, rien sur l'identite, rien sur la coordination des comptes.** Un
    audit reel combinerait les trois avec l'audit structurel, et ce rapport ne dit pas ce que la
    combinaison vaut.
11. **La quantification n'a pas ete refaite.** Le tableau 6.3 de i3, l'estimateur aveugle qui
    rend un plancher, reste tel quel ; l'abaque ne dit pas comment l'erreur de quantification
    varie avec la taille du flux. C'est le complement suivant le moins cher.

---

## 11. Questions ouvertes pour Simon

1. **Faut il republier les `tau*` de i3 ?** Le tableau 3.3 dit que i3 est optimiste d'un facteur
   1,2 a 1,9, entierement a cause du bruit de reference, et que la ligne « l'adversaire nul est
   vu des 6,4 pour cent » devient « des 11,2 pour cent » et sort de la famille signalee a
   5 pour cent. Le fait de i3, la bande a deux bords, ne bouge pas ; le chiffre qu'on cite en
   premier bouge. Est ce une erratum, une note dans i3b, ou une reecriture de la reponse en une
   ligne de i3 ?
2. **La reponse en trois etages a l'objection « vous publiez la cible » est cassee au deuxieme
   etage.** La reserve theoriquement elegante, la structure a l'ordre trois, est dominee par une
   statistique publiee sur tous les adversaires sauf le gabarit. Faut il abandonner l'argument
   de la reserve et defendre la norme sur les deux autres etages, le cout en microdonnees et la
   fraude paresseuse, ou chercher une reserve qui marche et accepter qu'elle soit choisie apres
   coup ?
3. **Le resultat le plus vendable de ce mois n'est peut etre pas l'abaque.** C'est que
   **l'invisibilite et la nuisance s'opposent** : le fabricant invisible est celui qui porte la
   personne, donc celui qui ne deplace rien, et le fabricant qui deplace est vu. Si cela tient
   sur un second jeu, la these change : on ne vend plus « on detecte la fraude », on vend
   « toute fraude qui deplace quelque chose est detectable, et voici a partir de quelle
   taille ». Est ce que ce n'est pas cela, le titre du programme B ?
4. **La lecture par camp doit elle devenir le mode par defaut de la norme ?** Elle divise par
   trois a cinq le taux detectable d'une operation concentree, elle ne coute rien, et une
   operation reelle est concentree par definition. Le prix est une famille de tests plus grande,
   trois statistiques fois le nombre de segments, donc un seuil de Holm plus severe. Le calcul
   n'est pas fait ici ; il tient en une heure.
5. **Twin dit que la detectabilite est une propriete du pipeline et pas du modele**, facteur
   deux entre quatre variantes de la meme invite sur le meme modele, facteur 30 entre la
   meilleure et la pire des treize. Est ce que cela ne transforme pas le mois 9, « l'audit de
   trois simulateurs commerciaux », en quelque chose de plus fort : un **banc public ou tout
   fournisseur depose une population et recoit trois nombres**, sans avoir a reveler son
   pipeline ?
6. **Le reglage fin est le pire generateur du dossier**, moins 79 pour cent de patrons, detecte
   a 0,43 pour cent de contamination. C'est contre intuitif et c'est vendable : **affiner un
   modele sur de vraies reponses le rend moins humain, pas plus.** Vaut il un encadre a lui
   seul, ou est ce un artefact de la facon dont Twin a affine, 500 exemples seulement ?
7. **Quelle est la seconde population humaine la moins chere ?** Les trois choses qui manquent a
   l'abaque au dela de 1 052 sont toutes la meme chose : de vraies personnes, en nombre, sur un
   questionnaire ferme, avec un retest. Faut il chercher un panel existant, ou accepter que
   l'abaque s'arrete a 1 052 et publier la partie mesuree seule ?

---

## 12. Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
.venv/bin/python analyses/i3b_abaque.py
.venv/bin/python analyses/i3b_twin.py
.venv/bin/python analyses/i3b_camp.py
.venv/bin/python analyses/i3b_adversaire.py
.venv/bin/python analyses/i3b_surface.py
.venv/bin/python analyses/i3b_figures.py
```

Durees mesurees sur quatre coeurs : **922 s** pour `i3b_abaque.py`, **764 s** pour
`i3b_twin.py`, **582 s** pour `i3b_camp.py`, **527 s** pour `i3b_adversaire.py`, quelques
secondes pour la surface et les figures ; **environ 48 minutes en tout**. `i3b_abaque.py`
accepte `--reutiliser-melanges`, qui relit `i3b-melanges-par-taille.csv` et ne recalcule que la
reference, et `--smoke` pour un passage rapide. Les caches `/tmp/a25-matrices.pkl`,
`/tmp/a28-foret.npy` et `/tmp/a35-methodes.pkl` doivent exister ; ils sont produits par a25, a28
et a35 et ne sont pas recalcules ici. `i3b_camp.py` exige que `i3b_abaque.py` ait tourne avant,
il relit sa reference. Graine unique **20260909** partout.

---

## 13. Fichiers produits

| fichier | contenu |
|---|---|
| `resultats/i3b-preenregistrement.md` | le preenregistrement, horodate le 8 septembre 2026 a 21 h 05 CEST, non modifie |
| `resultats/i3b-controles.csv` | les controles du GSS, 56 lignes, toutes passees |
| `resultats/i3b-reference-par-taille.csv` | la bande humaine et `s0(N)` aux quatre tailles, naif et corrige |
| `resultats/i3b-melanges-par-taille.csv` | les 432 flux lus a quatre tailles, 1 732 lignes |
| `resultats/i3b-abaque.csv` | `z`, `p`, puissance et `tau*` par source, statistique et taille, 432 lignes |
| `resultats/i3b-abaque-extrapolee.csv` | l'extrapolation au dela de 1 052 et son test de stabilite, 120 lignes |
| `resultats/i3b-courbes-consequence.csv` | polarisation et trois marginales par source, taux et taille |
| `resultats/i3b-twin-controles.csv` | les controles de Twin, 21 lignes, deux echecs declares |
| `resultats/i3b-twin-reference.csv` | la bande humaine de Twin aux cinq tailles |
| `resultats/i3b-twin-sources-pures.csv` | les quatorze conditions de Twin a taux 100 pour cent |
| `resultats/i3b-twin-melanges.csv` | les 660 flux de Twin lus a deux tailles, 1 320 lignes |
| `resultats/i3b-twin-abaque.csv` | `z`, `p` de Holm et `tau*` par configuration, 330 lignes |
| `resultats/i3b-camp-reference.csv` | la bande par bloc ideologique, 24 lignes |
| `resultats/i3b-camp-melanges.csv` | les 1 100 flux concentres et uniformes |
| `resultats/i3b-camp-detection.csv` | detection en lecture globale et par camp, 660 lignes |
| `resultats/i3b-camp-polarisation.csv` | l'ecart entre camps et les marginales, 440 lignes |
| `resultats/i3b-adversaire-reference.csv` | la bande des cinq statistiques a N = 526 |
| `resultats/i3b-adversaire-calibration.csv` | les 225 points de grille et le critere, tries |
| `resultats/i3b-adversaire-melanges.csv` | les 420 flux des sept fabricants de la section 6 |
| `resultats/i3b-adversaire-detection.csv` | `z`, `p` de Holm et `tau*` des cinq statistiques, 140 lignes |
| `resultats/i3b-surface-attaque.csv` | le prix de l'invisibilite, 50 lignes |
| `resultats/i3b-meta.json` | les trois marginales declarees, les seuils `z`, les parametres du run |
| `resultats/i3b-figure-abaque.png` et `.svg` | l'abaque |
| `resultats/i3b-figure-bande-deux-jeux.png` et `.svg` | la bande sur deux jeux |
| `resultats/i3b-figure-surface-attaque.png` et `.svg` | le prix de l'invisibilite |
| `analyses/i3b_commun.py` | briques : sous echantillonnage, `s0(N)`, R1, R2, melange concentre, adversaires |
| `analyses/i3b_abaque.py`, `i3b_twin.py`, `i3b_camp.py`, `i3b_adversaire.py`, `i3b_surface.py`, `i3b_figures.py` | les six runs |
