# a43. Preenregistrement

**Ecrit le 8 septembre 2026 a 15:41:50 CEST, avant tout calcul.** Aucun chiffre de a43 n'existait
au moment de l'ecriture ; aucune ligne de ce fichier n'est modifiee ensuite. Commit de reference de
l'arbre de travail au moment de l'ecriture : `d536169dc5361c38edcd723d48816e2ddd06dc4f`.

Objet : verrou 7 de `MODELE-DU-MONDE.md` section 6. Porter sur nos donnees la mesure de Ahn, Mao et
Lee (arXiv 2608.29455, lecture 01) et les quatre mesures de Peng et al. (a36), avec et sans retrait
de la moyenne de segment.

---

## 1. Donnees, perimetres, conditions

Aucune donnee nouvelle, aucun appel de modele. Lecture seule sur `data/`. Tout le chargement passe
par `a28_commun.charger_tout`, donc memes 1 052 personnes, memes 149 items, memes cinq plis, memes
graines, memes 150 personnes du run local que a2, a23, a25, a28, a29, a35 et a39. Les matrices
d'imputation de a35 sont relues du cache `/tmp/a35-methodes.pkl` sans etre recalculees.

Deux perimetres, comme partout depuis a28 :

- **1052** : les 1 052 personnes, toutes les conditions sauf C2 et C3 ;
- **150** : les 150 personnes du run local, toutes les conditions, C2 et C3 comprises.

Conditions declarees a l'avance, quatorze plus le plancher :

| groupe | conditions |
|---|---|
| Stanford, six conditions | `agents composite`, `agents entretien (v3)`, `agents enquete`, `agents demographiques (v6)`, `agents v7`, `agents v8` |
| run local | `C2` (etiquette seule), `C3` (119 items, sans etiquette) |
| predicteurs statistiques | `B0 mode`, `B1 argmax`, `B2 argmax`, `B3 foret` |
| imputations de a35 | `PMM k=5`, `PMM k=10`, `IM m=10 mode des m` |
| plancher de bruit | `humains vague 2` |

**Items.** Toutes les mesures de ce rapport sont numeriques : elles exigent une valeur sur une
echelle. Elles sont donc calculees **sur les seuls items ordinaux**, au sens de
`a25_commun.ORDINAUX` prive des items portant une modalite du type « Inapplicable », c'est a dire la
liste exacte que `a39_commun.items_ordinaux` produit. La valeur d'une modalite est son **rang
normalise dans [0, 1]** selon l'ordre de `question_master/gss/main.csv`
(`a39_commun.table_de_rang`). Le nombre d'items ainsi retenus est ecrit dans le rapport ; la liste
complete est deposee dans `a43-items-ordinaux.csv`. Une reponse absente ou hors nomenclature donne
une valeur manquante et la cellule sort du calcul, sauf pour l'exactitude de Peng ou elle recoit
zero, convention severe de a29 et a39.

**Hypothese heritee, declaree ici.** L'ordre des modalites du fichier de Stanford est pris pour
l'ordre de l'echelle. Si cet ordre est faux pour un item, toutes les mesures numeriques de a43 sont
fausses pour cet item. C'est la meme hypothese que a1, a25, a35 et a39 ; elle n'est pas reverifiee.

---

## 2. Les moyennes retirees, et ou elles sont estimees

Deux niveaux de retrait, tous deux **en `leave-one-out` sur les personnes**.

1. **Moyenne d'item.** Pour la cellule (personne `i`, item `j`), `m_j^(-i)` est la moyenne des
   valeurs de la vague 1 des humains de l'item `j`, personne `i` exclue.
2. **Moyenne de segment.** `m_{j,s}^(-i)` est la moyenne des valeurs de la vague 1 des humains de
   l'item `j` **dans le segment `s(i)`**, personne `i` exclue.

**Les deux moyennes sont toujours estimees sur les 1 052 personnes**, y compris quand la mesure est
evaluee sur le perimetre 150. Motif ecrit d'avance : la moyenne d'item et la moyenne de segment sont
des quantites de population ; les estimer sur 150 personnes ajouterait a l'operation de demoyennage
un bruit d'estimation qui abaisserait mecaniquement tous les `R^2` du perimetre 150 et rendrait les
deux perimetres incomparables.

**Segmentation primaire, decidee avant tout calcul** : bloc d'ideologie x genre x tranche d'age
regroupee, soit 3 x 2 x 3 = **18 segments**.

- bloc d'ideologie : la regle mecanique de `a28_commun._bloc_ideologie`, « liberal » vers gauche,
  « conservative » vers droite, le reste vers centre ;
- genre : les deux modalites du fichier ;
- age regroupe : `18 - 24` et `25 - 34` vers « jeune » ; `35 - 44` et `45 - 54` vers « median » ;
  `55 - 64`, `65 - 74` et `75 or more` vers « age ».

Motif du regroupement de l'age : 1 052 personnes reparties sur 42 cellules donneraient une moyenne
de segment estimee sur environ 25 personnes par item, moins les manquants. Le regroupement vise
environ 58 personnes par cellule. **Segmentation secondaire de robustesse**, rapportee a cote et
jamais substituee a la primaire : les 7 tranches d'age d'origine, soit 42 segments.

Une cellule dont le segment est inconnu, ou dont le segment compte moins de **10** repondants
observes sur l'item apres retrait de la personne, est ecartee du calcul apres retrait de segment.
Le nombre de cellules ainsi perdues est rapporte.

---

## 3. Les six mesures, definies avant de les voir

### M1. `R^2` demoyenne d'item

Sur les cellules valides du perimetre, avec `h` la valeur humaine de la vague 1 et `p` la valeur de
la methode :

    x_ij = h_ij - m_j^(-i)
    y_ij = p_ij - m_j^(-i)
    R2_item = corr(x, y)^2 , correlation de Pearson calculee sur l'ensemble des cellules mises bout a bout

Le plafond est la meme quantite calculee avec `p` = reponse de la **vague 2 de la meme personne**.
Le rapport publie aussi `R2_item / plafond`, l'equivalent des « 5,7 pour cent du plafond » de Ahn.

### M2. `R^2` demoyenne d'item et de segment

    x'_ij = h_ij - m_{j,s(i)}^(-i)
    y'_ij = p_ij - m_{j,s(i)}^(-i)
    R2_segment = corr(x', y')^2

C'est **la part personne au dela du groupe**. Meme plafond, calcule sur la vague 2.

Le signe de la correlation est publie a cote du `R^2` : une correlation negative donne un `R^2`
positif et ne serait pas une bonne nouvelle. La statistique testee est **la correlation**, pas son
carre.

### M3. Le test d'Ahn, par personne

Pour chaque personne `i`, `r_i` est la correlation de Pearson **a travers les items** entre `h_ij`
et `p_ij`, valeurs brutes non demoyennees. Trois competiteurs par personne :

- la methode ;
- la **moyenne d'item `leave-one-out`**, qui predit `m_j^(-i)` ;
- la **moyenne de segment `leave-one-out`**, qui predit `m_{j,s(i)}^(-i)`.

Agregation : moyenne des `r_i` transformes en `z` de Fisher, retransformee ; la moyenne brute des
`r_i` est publiee a cote. Une personne comptant moins de 10 items valides est ecartee.
Les deux differences appariees, methode moins moyenne d'item et methode moins moyenne de segment,
sont testees.

### M4. Decomposition de Ahn

Modele a effets aleatoires personne x item sur les valeurs ordinales, estimateurs par sommes de
carres du plan croise, exactement les quatre parts que Ahn publie.

- **Chez les humains**, le plan est personne x item x occasion, les deux occasions etant la vague 1
  et la vague 2. Quatre composantes rapportees en part de la variance totale : effet principal de
  personne, effet principal d'item, **interaction stable personne x item**, erreur transitoire. La
  quantite d'interet est le **rapport interaction sur effet de personne**, a comparer au **8,9** de
  Ahn.
- **Chez chaque methode**, une seule occasion existe. Trois composantes seulement : personne, item,
  residu, ou le residu confond l'interaction stable et l'erreur. Le rapport residu sur personne est
  alors une **borne superieure** du rapport de Ahn et il est nomme comme telle dans le rapport.

### M5. Les quatre mesures de Peng

Sur les memes items ordinaux et les memes valeurs dans [0, 1] :

- **exactitude** `1 - MAD`, l'etendue valant 1 par construction du rang normalise ; agregation par
  personne puis moyenne, une prediction absente recoit zero ;
- **correlation a travers les participants, par item**, moyenne par `z` de Fisher, comme eux et
  contre Park ;
- **Glass's Delta** : `|moyenne_methode - moyenne_humains| / ecart_type_humains`, un par item,
  moyenne sur les items ;
- **rapport d'ecarts types**, un par item, calcule sur l'echantillon apparie, moyenne sur les items.
  Cette quatrieme mesure est celle de `a39_commun.rapport_ecarts_types`, reprise sans modification ;
  a43 verifie qu'elle redonne les valeurs de `a39-ecarts-types.csv` et publie l'ecart maximal.

Colonnes de comparaison, valeurs de Peng lues par a36 section 6.2 et jamais recalculees :
rapport d'ecarts types 0,446 persona vide, 0,575 etiquette, 0,634 persona complete, 1,061 pour
l'ajuste a temperature 0,7 ; exactitude 0,734 / 0,746 / 0,748 ; correlation 0,080 / 0,145 / 0,197.

### M6. Figure

`R^2` demoyenne par methode, deux barres par methode, sans et avec retrait du segment, ligne de
plafond humain vague 2 pour chacune des deux. Perimetre 1052 et perimetre 150 sur deux panneaux.

---

## 4. Predictions ecrites d'avance

Elles sont celles de la these, section 7 de `MODELE-DU-MONDE.md`. Elles sont jugees fausses si
l'intervalle publie les exclut.

- **P1.** Pour les conditions a etiquette seule, `agents demographiques (v6)`, `agents v8` et `C2`,
  le `R^2` apres retrait du segment est **indistinguable de zero** : l'intervalle a 95 pour cent de
  la correlation contient zero.
- **P2.** Pour les conditions portant de l'information individuelle, `agents composite`,
  `agents enquete`, `agents entretien (v3)` et `C3`, le `R^2` apres retrait du segment est
  **strictement positif** et **inferieur au dixieme du plafond humain**.
- **P3.** Les imputations statistiques par tirage, `PMM k=5`, `PMM k=10`, `IM m=10 mode des m`, sont
  **entre les deux** : positives, et au dessous des conditions riches a modele de langage.
- **P4.** Sur M3, **aucune** de nos conditions a modele de langage ne bat la moyenne d'item
  `leave-one-out` ; c'est le resultat de Ahn, `r` 0,34 contre 0,45.
- **P5.** Sur M4, le rapport interaction sur effet de personne chez nos humains est **superieur a 5**.
- **P6.** Sur M5, notre rapport d'ecarts types range nos conditions dans le meme ordre que le leur :
  aveugle sous etiquette sous riche.

Une prediction non tranchee par le calcul est declaree non tranchee, pas confirmee.

---

## 5. Inference, corrections, et ce qui n'est pas fait

**Bootstrap sur les personnes, 2 000 tirages, graine 20260908**, le meme tirage servant a toutes les
conditions d'un meme perimetre pour que les contrastes soient apparies. Deux reponses d'une meme
personne ne sont pas independantes ; un bootstrap sur les cellules donnerait un intervalle
faussement etroit. Aucun bootstrap sur les items n'est fait dans a43 ; c'est une limite, elle est
ecrite ici.

**Les moyennes `leave-one-out` ne sont pas recalculees dans la boucle de bootstrap.** Elles sont
estimees une fois sur l'echantillon complet. Le bootstrap mesure donc l'incertitude de la
correlation, pas celle du demoyennage. C'est un intervalle legerement trop etroit, et c'est ecrit.

**Trois familles de tests, corrigees separement par Holm, et Benjamini Hochberg publie a cote.**

- famille F1 : « la correlation apres retrait du segment differe de zero », un test par condition et
  par perimetre ;
- famille F2 : « la methode bat la moyenne d'item `leave-one-out` sur `r` par personne », un test
  par condition et par perimetre ;
- famille F3 : « la methode bat la moyenne de segment `leave-one-out` sur `r` par personne », meme
  decoupage.

`p` bilateral lu sur la position de zero dans la distribution bootstrap, plancher a 1 sur le nombre
de tirages, convention de a28, a29, a31 et a39. Holm est la correction retenue ; Benjamini Hochberg
suppose une dependance positive non verifiee ici et n'est publie qu'en colonne secondaire.

**Ce que a43 ne fera pas** : aucun appel de modele, aucune condition nouvelle, aucune modification
de fichier existant, aucun bootstrap sur les items, aucune mesure sur les items nominaux, aucun
recalcul des chiffres de Ahn ni de Peng, qui sont recopies de la lecture 01 et de a36.

---

## 6. Sorties prevues

`analyses/a43_commun.py`, `analyses/a43_r2_demoyenne.py`, `analyses/a43_peng.py`,
`analyses/a43_figure.py` ; tableaux `resultats/a43-*.csv` ; figure `resultats/a43-figure-r2.png` et
`.svg` ; rapport `resultats/a43-r2-demoyenne.md`.
