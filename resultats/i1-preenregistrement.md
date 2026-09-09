# I1, preenregistrement : qui change d'avis dans les panels GSS, et est ce previsible

**Ecrit le 8 septembre 2026 a 18 h 30 CEST, soit 16 h 30 UTC.** Depot a
`d536169dc5361c38edcd723d48816e2ddd06dc4f`, branche `chore/restauration-arborescence`.

**Etat au moment de l'ecriture.** Aucun calcul d'I1 n'a ete lance. Aucun script
`analyses/i1_*.py` n'existe, aucun fichier `resultats/i1-*` n'existe hors cette page. Ont
ete faits avant cette page, et rien d'autre : la lecture de `BRAINSTORM-IMPACT.md` en
entier, de `MODELE-DU-MONDE.md` section 10, de `resultats/a12-delai-de-retest.md`, de
`resultats/a44-generateur-nul.md` et de son preenregistrement, des scripts
`analyses/a12_retest_delai.py`, `a2_commun.py`, `a44_commun.py`, `a30_commun.py`,
`a30_structure.py`, `a25_commun.py`, et de `data/gss-panel/PROVENANCE.md` ; puis une
**inspection strictement structurelle** des quatre fichiers Stata, par
`pyreadstat.read_dta(metadataonly=True)`, qui n'a lu que des **noms de colonnes** pour
verifier que `polviews`, `age`, `educ`, `degree`, `sex`, `race`, `partyid`, `attend` et
`relig` existent a chaque vague des quatre panels. **Aucune valeur de reponse, aucune
marginale, aucun taux de changement n'a ete lu ni calcule.**

Cette page n'est pas modifiee apres le premier calcul. Tout ecart au protocole est declare
dans le rapport, section « ecarts au preenregistrement », avec son motif.

---

## 1. Les trois questions, en une phrase chacune

**Q-A.** Sur les quatre panels GSS et les 118 items du noyau commun de a12, quelle part du
changement entre deux vagues est du changement **monotone**, c'est a dire dirige dans le
sens de la derive agregee de la periode, et quelle part est de l'aller retour, c'est a dire
du bruit de reponse au sens du retest a deux semaines de Stanford ?

**Q-B.** Peut on predire, a partir des seules reponses de vague 1 d'une personne et de ses
demographies, **qui** changera d'avis sur un item donne, mieux qu'un temoin qui ne connait
que la probabilite marginale de l'item et mieux qu'un temoin qui ne connait que le segment
ideologie x age x education de la personne ? La quantite de verdict est la **chute de l'AUC
sous permutation des personnes a l'interieur du segment**, transposition directe de la
mesure de personne de a44.

**Q-C.** Les personnes incoherentes en vague 1, au sens des cross pressures de a30
(quadrant economique x social discordant), changent elles davantage que les congruentes ?
C'est le volet humain d'I2.

---

## 2. Donnees, perimetre, et ce qui est fixe

**Fichiers.** `data/gss-panel/*.dta`, les quatre panels de `PROVENANCE.md`, en lecture
seule. Aucune microdonnee n'est ecrite. Tous les fichiers de sortie sont des agregats par
item, par segment ou par decile.

**Items.** Les **118 items du noyau commun** de a12, c'est a dire les items apparies dans
les onze paires de vagues a la fois. Ils sont recalcules par appel direct des fonctions de
`analyses/a12_retest_delai.py` (`items_stanford`, `noms_gss`, `charger_panel`,
`consistance`), importe comme module, **sans aucune modification**. Si le compte ne tombe
pas sur 118, le rapport le dit et le protocole s'applique au compte obtenu.

**Paires de vagues.**

- **Perimetre primaire : les quatre paires a quatre ans**, 2006-2010, 2008-2012, 2010-2014
  et la cohorte 2016 du panel 2016-2020 reinterrogee en 2020. Les quatre echantillons de
  depart sont des tirages distincts du GSS : les personnes sont **disjointes** d'un panel a
  l'autre, ce qui autorise la mise en commun et le bootstrap sur les personnes sans
  correction de grappe. Effectif attendu de l'ordre de 4 683 personnes (a12, 3.1).
- **Perimetre secondaire : les quatre paires a deux ans disjointes**, la premiere de chaque
  panel a trois vagues plus 2018-2020, pour verifier que rien ne depend du delai.
- **Perimetre a trois vagues** : les trois panels 2006, 2008 et 2010 seulement, pour la
  decomposition aller retour contre changement persistant.

**Segment.** `ideologie x age x education`, tel que demande, avec les replis mecaniques
suivants, fixes ici :
- ideologie, trois blocs a partir de `polviews` de vague 1 : 1 a 3 gauche, 4 centre, 5 a 7
  droite. C'est la regle de a1 et de a44 (`_bloc_ideologie`), transposee aux codes
  numeriques du panel ;
- age, trois blocs a partir de `age` de vague 1 : 18 a 34, 35 a 54, 55 et plus ;
- education, trois blocs a partir de `degree` de vague 1 : 0 et 1 bas, 2 et 3 moyen, 4
  haut.
Soit **27 cellules au plus**. Une personne dont l'un des trois est manquant forme le
segment « non renseigne », qui est un segment comme un autre pour la permutation. Un segment
de moins de **10 personnes** dans un pli est replie sur la marginale du pli.

**Graine** `20260908`, la meme que a44. **200 permutations**, **1 000 tirages bootstrap sur
les personnes**, **5 plis de validation croisee**, decoupes **sur les personnes** et non sur
les cellules : une personne est entiere dans un seul pli, tous items confondus.

---

## 3. Q-A : les definitions du changement, fixees avant tout calcul

Pour une personne `i`, un item `j`, une paire de vagues `(a, b)` :

**Changement brut.** `chg_ij = 1` si les deux cellules sont renseignees et les modalites
different. Definition d'egalite exacte de modalite, celle de Stanford et de a12, reprise
sans retouche. Les manquants etendus de Stata, `DK`, `IAP`, `NA`, arrivent en NaN et sont
exclus, comme dans le calcul principal de a12 ; la variante « non reponse comptee comme
modalite » de `a12_sensibilite_dk.py` n'est pas refaite ici et le rapport le dit.

**Derive agregee de l'item, en laisse un dehors.** Pour l'item `j` et la paire `(a, b)`,
`Delta p_j(m) = part(m) en b moins part(m) en a`, calculee sur les personnes observees aux
deux vagues. Pour classer la personne `i`, `Delta p` est **recalculee sans elle**. Cette
regle est posee avant tout calcul et elle est le point technique du protocole : sans elle,
un changement de `m1` vers `m2` pousse mecaniquement `Delta p(m2)` vers le haut et se
classerait monotone tout seul, ce qui fabriquerait le resultat.

**Changement monotone.** `chg_ij = 1`, la personne passe de `m1` a `m2`, et
`Delta p_{j,-i}(m2) > 0` **et** `Delta p_{j,-i}(m1) < 0`. La modalite quittee perd du
terrain, la modalite prise en gagne : la personne va dans le sens de la derive de la
periode.

**Changement contraire.** Meme chose avec les deux inegalites inversees.

**Changement indetermine.** Tout le reste, y compris les cas ou l'une des deux parts ne
bouge pas dans le sens attendu.

Cette regle n'exige **aucune hypothese d'ordinalite** : elle vaut pour les items nominaux
comme pour les echelles. Aucune version ordinale, aucune moyenne de code, n'est publiee
comme resultat primaire.

**Derive nette de l'item.** `TV_j = 0,5 x somme_m |Delta p_j(m)|`, la distance en variation
totale entre les deux marginales. C'est la part minimale de la population qui a du bouger
pour produire la marginale de vague `b`. `TV_j / d_j` ou `d_j` est le taux de changement
brut est la **part dirigee** du mouvement ; `1 - TV_j / d_j` est l'agitation.

**Plancher de bruit, deux definitions, les deux publiees.**
1. **Plancher de Stanford** : `d_j^{2sem} = 1 - consistance a deux semaines de l'item j`,
   relue de `resultats/a12-items-stables-instables.csv`, colonne `consistance_2sem`. Le
   surcroit de changement `d_j^{4ans} - d_j^{2sem}` est le changement qui n'est pas
   attribuable au bruit de reponse d'un retest court, **sous l'hypothese explicite que le
   bruit de reponse de l'echantillon Bovitz en ligne et celui du panel NORC en face a face
   sont du meme ordre**. a12 section 6 dit que cette hypothese est fausse dans une mesure
   inconnue et dans le sens qui gonfle notre surcroit ; c'est ecrit dans le rapport a cote
   du chiffre, pas en note.
2. **Plancher interne, sans Stanford** : sur les trois panels a trois vagues, l'**aller
   retour**, `y_a = y_c` et `y_b` different des deux, est du bruit pur par construction ;
   `2 x taux d'aller retour` est un estimateur du taux de changement de bruit dans une
   paire, sous un modele de bruit symetrique a deux etats. Il ne depend d'aucun echantillon
   exterieur.

**Trois vagues, decomposition.** Sur les trois panels a trois vagues, pour les cellules
renseignees aux trois passations :
- **stable** : `y_a = y_b = y_c` ;
- **aller retour** : `y_a = y_c`, `y_b` different ;
- **persistant** : `y_a` different de `y_c`, et `y_b` dans `{y_a, y_c}` ;
- **erratique** : trois modalites distinctes.
Le **changement monotone persistant** est un persistant dont la direction `y_a -> y_c`
satisfait la regle de derive ci dessus, sur la paire a quatre ans.

---

## 4. Q-B : les predicteurs, les temoins, la quantite de verdict

**Cible.** Deux cibles binaires, par item, sur le perimetre primaire :
`Y_chg` = changement brut ; `Y_mono` = changement monotone, contre tout le reste, y compris
le changement contraire. `Y_chg` est primaire.

**Ce que le predicteur a le droit de voir.** Uniquement la vague `a` : les reponses de la
personne aux 117 autres items, sa reponse a l'item `j` lui meme, et ses demographies de
vague `a`, `polviews`, `partyid`, `age`, `sex`, `race`, `degree`, `educ`, `attend`,
`relig`, plus l'indicatrice de panel. Jamais la vague `b`, jamais la derive de l'item, qui
est une information de vague `b`.

**Quatre predicteurs.**
- **L1, logistique resumee** : demographies, la reponse de la personne a `j` en vague `a`,
  et six resumes de son profil de vague `a` : score economique, score social, ecart
  standardise entre les deux, distance de Hamming au patron modal de son segment, part de
  modalites rares tenues au seuil de 10 pour cent de a8, part de cellules manquantes.
- **L2, logistique complete** : les demographies plus le profil complet de vague `a` en
  indicatrices, item `j` inclus, penalisation L2.
- **V, k plus proches voisins**, `k = 25`, distance de Hamming de `a2_commun` sur le profil
  de vague `a` prive de l'item `j` ; probabilite predite egale a la part de voisins qui ont
  change sur `j`.
- **F, foret aleatoire**, 300 arbres, profondeur non bornee, sur codes entiers du profil de
  vague `a` et demographies.

Tous sont ajustes **par item** et **par pli**, sur les seules personnes du pli
d'entrainement, et notes sur le pli de test. Les scores hors pli sont concatenes pour
former une prediction par personne et par item.

**Trois temoins.**
- **T0, nul avec derive.** Chaque personne recoit la meme probabilite, le taux de changement
  de l'item estime sur le pli d'entrainement. Sans structure individuelle, son AUC vaut
  0,5 par construction ; il est **simule 200 fois** pour publier la **bande d'echantillonnage
  de l'AUC sous absence totale de signal**, a l'effectif reel de chaque item. C'est cette
  bande, et non 0,5, qui sert de reference.
- **T1, temoin de segment.** Probabilite predite egale au taux de changement du segment
  `ideologie x age x education`, estime sur le pli d'entrainement seul. C'est le gabarit de
  groupe applique au changement.
- **T2, permutation intra segment.** Transposition exacte de `a44_commun.permuter_intra`.
  Les scores hors pli d'un predicteur sont **permutes entre personnes du meme segment**,
  puis l'AUC est recalculee contre les vraies etiquettes de changement. Repetee 200 fois.

**Quantite de verdict, declaree.** Pour chaque predicteur et chaque item,
**`chute = AUC_observee - moyenne(AUC_permutee)`**. Elle est nulle si le predicteur ne
porte que du segment, positive s'il porte de l'individu. C'est la seule quantite sur
laquelle porte le verdict d'I1. L'AUC brute et le rappel sont descriptifs.

**Rappel des changeurs.** Au seuil qui signale exactement autant de personnes qu'il y a de
changeurs reels sur l'item, la part de changeurs reels signales. Publie pour les quatre
predicteurs et les trois temoins.

**Agregation.** Moyenne sur les items ponderee par le nombre de personnes evaluees, et
mediane non ponderee a cote. IC a 95 pour cent par bootstrap **sur les personnes**, 1 000
tirages : une personne tiree entre avec toutes ses lignes item, ce qui respecte la
dependance entre items d'une meme personne.

**Correction pour tests multiples.** Un test par item, `p` unilateral issu de la
distribution de permutation, `p = (1 + nombre de permutations dont l'AUC atteint ou depasse
l'AUC observee) / (1 + 200)`. Correction de **Holm** sur les 118 items pour le predicteur
primaire, et **Benjamini-Hochberg** en second, par `a44_commun.holm` et
`a44_commun.benjamini_hochberg`, reutilises tels quels.

**Predicteur primaire declare : L2, la logistique complete, sur la cible `Y_chg`, sur le
perimetre primaire a quatre ans.** Les trois autres sont secondaires. Ce choix est fait
avant tout calcul pour qu'il ne soit pas le meilleur choisi apres coup.

---

## 5. Q-C : les cross pressures, volet humain d'I2

**Axes.** `AXE_ECONOMIQUE` et `AXE_SOCIAL` de `a30_commun.py`, importes tels quels,
restreints aux items presents dans le panel. Score par personne : premiere composante
principale du bloc, standardisee, estimee sur l'echantillon complet du perimetre et non
segment par segment, orientation fixee par correlation positive avec `polviews` en sept
points. C'est la methode de `a30_structure.scores_axes`, transposee aux codes du panel.

**Quadrant.** Signe de `z_eco` et signe de `z_soc`. **Hors quadrant, ou sous cross
pression** : les deux signes different. **Congruent** : ils coincident. Mesure continue de
cross pression : `|z_eco - z_soc|`.

**Autres profils testes**, tous mesures en vague `a` :
1. position initiale : la personne tient elle la modalite majoritaire de l'item, une
   modalite rare au seuil de 10 pour cent ;
2. incoherence initiale : distance de Hamming au patron modal de son segment ;
3. cross pression : quadrant et `|z_eco - z_soc|` ;
4. consistance test retest propre, **estimee en laissant l'item dehors** : sur les trois
   panels a trois vagues, le taux d'aller retour de la personne sur les 117 autres items.
   Elle n'est calculee que la ou elle existe, et jamais sur l'item predit.

**Test.** Ecart de taux de changement monotone entre hors quadrant et congruents, avec IC
bootstrap sur les personnes, **et le meme ecart apres permutation des etiquettes de
quadrant a l'interieur du segment** : si l'ecart disparait sous permutation, la cross
pression n'est qu'un autre nom du segment.

---

## 6. Six predictions, ecrites avant le calcul

| | prediction |
|---|---|
| **P1** | Le taux de changement brut a quatre ans depasse le taux a deux semaines de Stanford sur **plus de 90 pour cent** des 118 items. |
| **P2** | La part dirigee `TV_j / d_j` du mouvement est **inferieure a 0,25** en mediane : l'essentiel du changement entre deux vagues est de l'agitation, pas de la derive. |
| **P3** | Le taux d'aller retour sur les trois panels a trois vagues est **superieur au taux de changement persistant**. |
| **P4** | L'AUC observee du predicteur primaire L2 sur `Y_chg` est **comprise entre 0,55 et 0,65** : un signal existe, mais il est faible. |
| **P5** | La **chute sous permutation** du predicteur primaire est **positive et inferieure a 0,03 point d'AUC** ; autrement dit le signal individuel existe mais l'essentiel de l'AUC est du segment et de la position initiale sur l'item. |
| **P6** | Les personnes hors quadrant changent **plus** que les congruentes, et l'ecart **survit** a la permutation intra segment. |

Une prediction fausse est publiee comme fausse. Le score des six est un tableau du rapport.

---

## 7. Les regles de decision, ecrites avant de voir les chiffres

1. **Si la chute sous permutation du predicteur primaire n'est pas distinguable de zero
   apres correction de Holm sur les 118 items**, alors il n'existe pas de signal individuel
   de changement au dela du segment dans ces donnees, et **I1 est mort avant tout appel de
   modele** : aucun jumeau ne peut battre sur les personnes une quantite qui n'existe pas
   chez les humains. Cette issue est publiee telle quelle, elle est le resultat.
2. **Si la chute est positive et retenue**, sa valeur est **la barre qu'un jumeau devra
   battre** dans le run C3 du jour 5, sur la meme quantite, la meme segmentation et la meme
   correction.
3. **Si le temoin de segment T1 atteint la meme AUC que les quatre predicteurs**, alors la
   previsibilite du changement est entierement une propriete de groupe, et c'est le gabarit
   encore, applique au changement au lieu de l'etre a l'etat.
4. **Aucune de ces trois issues ne depend d'un appel de modele de langage.** Il n'y en a
   aucun dans I1 jour 1.

---

## 8. Controles bloquants

1. **Reproduction de a12.** Le taux de changement moyen recalcule ici sur le noyau commun
   doit reproduire `1 - 0,6745` a quatre ans et `1 - 0,6953` a deux ans, a moins de
   **0,002** pres. Sinon la chaine de lecture des panels est fausse et rien n'est publie.
2. **Neutralite de la regle en laisse un dehors.** Sur un jeu ou l'ordre des deux vagues est
   **inverse item par item par tirage a pile ou face**, la part de changement monotone doit
   tomber a la part de changement contraire, a l'erreur d'echantillonnage pres. Si elle n'y
   tombe pas, la regle de direction fabrique de la monotonie et le resultat est retire.
3. **Invariance de l'AUC des temoins sous permutation.** L'AUC de T0 doit etre invariante
   sous permutation intra segment, ecart nul a l'erreur numerique pres, et celle de T1 aussi
   par construction. Si l'une des deux bouge, la permutation est mal implementee.
4. **Effectif minimal.** Un item n'entre dans les tableaux que s'il a au moins **100
   personnes evaluees** et au moins **30 changeurs** sur le perimetre considere ; c'est le
   seuil `MIN_PAIRES_ITEM` de a12 pour le premier. Les items ecartes sont comptes et
   nommes.

---

## 9. Ce que ce jour 1 ne fera pas

Aucun appel de modele de langage. Aucune ecriture dans `data/`. Aucune modification d'un
script existant : `a2_commun.py`, `a44_commun.py`, `a12_retest_delai.py`, `a30_commun.py`
et `a25_commun.py` sont importes tels quels. Aucun jumeau, aucun agent, aucune condition de
Stanford n'est evaluee ici : ce rapport porte sur les **humains seuls**, et il fixe la barre
que le run du jour 5 devra franchir.
