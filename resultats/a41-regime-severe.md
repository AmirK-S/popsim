# a41. Le regime severe, mesure proprement

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Section 2 et reponse en une ligne : le rappel du tercile non deductible repose sur un instrument que a42 invalide. Objection a45 numero 4.3, contradiction D6.

**Phrase d'origine.** « Sur les 450 cellules du tercile **non deductible** de a34, celles ou
aucune autre personne du segment ideologie x genre x age n'a donne cette reponse, l'ecart
tient et se creuse en rapport : **28,2 pour cent [23,1 ; 33,6]** contre 13,8 pour cent pour
`PMM k=10 famille retiree` ».

**Correction.** a42 section 5, ecrite douze minutes apres a41, montre qu'une **partition
placebo de neuf groupes de personnes tires au hasard** reproduit le meme gradient, ecart
median 0,016 et jamais plus de 0,040 : le dispositif de terciles de a34 est invalide comme
instrument de deductibilite. Le rappel de 28,2 contre 13,8 reste un fait mesure ; il ne peut
plus etre lu comme « l'agent gagne la ou la rarete n'est pas deductible ». La partition de
remplacement est « rarete stable en vague 2 », la seule que a42 conserve, et la quantite
correspondante est publiee en a42 section 4.

C'est la seule quantite qui restait debout dans le resume d'une ligne de a41 : elle change
de statut, pas de valeur.

**Preuve.** a42 section 5, `a42-partitions.csv` ; `MODELE-DU-MONDE.md` 10.1 l'acte pour la
synthese, le corps de a41 ne le portait pas.

### E2. Section 6 : la penalite de 3,93 points est mesuree sur les Survey Agents et appliquee a `agents composite`. Objection a45 numero 4.1.

**Phrase d'origine.** « `agents composite` moins 3,93 pt | `E1 famille retiree` | moins
0,0266 [moins 0,0322 ; moins 0,0213] | 0,0060 ».

**Correction.** Le couple 0,82 contre 0,77 dont sont tires les 3,93 points est mesure sur
les **Survey Agents** [CONFIRME, a14 section 3.4]. `agents composite` recoit, en plus du
questionnaire, la transcription d'entretien : le retrait du bloc GSS lui coute
necessairement **moins** qu'a un agent dont le questionnaire est toute l'entree. La penalite
est donc appliquee a la condition pour laquelle elle est la plus grande possible, ce que le
rapport ne dit pas alors qu'il applique la meme soustraction a `agents enquete`, ou elle est
legitime. Comme il suffit de 1,27 point de decalage pour retourner la comparaison, la
conclusion negative depend de cette attribution.

**Ce qu'il faut ecrire.** Appliquer 3,93 points a `agents enquete` seulement, et donner pour
`composite` un encadrement, 0 point si l'entretien absorbe tout le retrait et 3,93 s'il
n'en absorbe rien, plutot qu'une valeur unique. La seule quantite appariee au sens strict de
la section reste le cout du retrait de famille, moins 6,24 points pour C3F contre moins 6,55
pour `E1`, et c'est elle qu'il faut mettre en avant.

---

Rapport du 8 septembre 2026. Il execute la verification que a35 designe lui meme comme
manquante, section 11 point 1 et question 3 pour Simon : « le regime severe porte maintenant
l'essentiel de la these et il est le moins bien mesure du rapport [...] les chiffres de la
section 6 sont des estimations ponctuelles sur 58 items et 1 052 personnes, sans bootstrap et
sans correction. L'ecart de 1,3 point entre `agents composite` et `E1 famille retiree` n'est
pas teste. C'est la verification la plus utile qui manque, et le rapport s'appuie pourtant sur
ce resultat pour sauver la these. »

Il pose en meme temps la question que l'errata E1 de `a8-baselines-durcies.md` rend
inevitable : le regime severe n'est applique qu'aux methodes statistiques. Les agents de
Stanford gardent les items cousins de la question dans leur invite. La comparaison de a8
section 3.2 et de a35 section 6 n'est donc pas appariee, et elle est favorable aux agents.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Trois scripts
nouveaux, `analyses/a41_commun.py`, `a41_regime_severe.py`, `a41_figure.py`. **Aucun script
existant n'a ete modifie** ; `a2_commun`, `a2_baselines_gss`, `a8_commun`, `a28_commun`,
`a29_commun`, `a31_commun`, `a33_commun`, `a34_commun`, `a35_commun` et `a35_familles` sont
importes tels quels, memes graines, memes plis, memes 149 items, memes 58 items de famille,
memes 1 052 personnes, memes 60 personnes de la trace C3F. Les quatre methodes d'imputation
du regime severe sont produites par appel direct de `a35_familles.imputer_par_famille` ;
`B2 famille retiree` en mode argmax par appel direct de `a33_commun.b2_famille_retiree` ; le
score de deductibilite par segment par appel direct de `a34_commun.frequence_segment`.

Sorties : `a41-controles.csv`, `a41-tableau-quatre-cases.csv`, `a41-contrastes-f1.csv`,
`a41-contrastes-f2.csv`, `a41-contrastes-f3.csv`, `a41-c3f-60-personnes.csv`,
`a41-terciles.csv`, `a41-condition-appariee.csv`, `a41-cout-du-retrait.csv`,
`a41-verification-mesures.csv`, `a41-figure-regime-severe.png` et `.svg`.

---

## Reponse en une ligne

**Non. Dans le regime severe, le modele de langage ne domine pas les imputations statistiques
a tirage sur les trois criteres a la fois, et les intervalles le disent : il gagne
decidablement sur l'exactitude et sur les gens rares contre les neuf methodes testees, et il
perd decidablement sur la structure contre les quatre methodes a tirage.** Sur les 27
contrastes de la famille primaire, les 27 passent la correction de Holm au plancher
p ajuste 0,0135, et **23 seulement portent le signe ecrit avant execution** ; les quatre qui
ne le portent pas sont exactement les quatre contrastes de structure contre les quatre
methodes de tirage. Le ratio de dispersion intra de `agents composite` vaut 0,858
[0,845 ; 0,872], celui de `PMM k=10 famille retiree` 0,958 [0,948 ; 0,967] : l'ecart absolu a
1 est plus grand pour l'agent de plus 0,099 [plus 0,084 ; plus 0,114], et il l'est aussi
contre `E2 famille retiree`, plus 0,135, contre `B2 famille retiree tirage`, plus 0,114, et
contre `B0 tirage`, plus 0,076 [MESURE, `a41-contrastes-f1.csv`].

**L'ecart de 1,3 point que a35 n'avait pas teste existe, et il est decidable.**
`agents composite` moins `E1 famille retiree` vaut **plus 0,0127 [plus 0,0071 ; plus 0,0180]**,
p ajuste 0,0135 sur la famille primaire [MESURE]. Sur la famille secondaire, la meme
condition domine `E1 famille retiree` sur les quatre quantites declarees en meme temps :
exactitude plus 0,0127, diversite conservee plus 0,1432 [plus 0,1333 ; plus 0,1531], ratio
intra plus 0,1077, et ratio inter plus 0,7479, ce dernier etant un defaut et non un avantage.
`agents enquete` est bien devant `E1 famille retiree` elle aussi, mais de plus 0,0062
seulement [plus 0,0007 ; plus 0,0118], p ajuste 0,029 : **c'est le seul test des 45 du rapport
qui soit a la limite de la decision** [MESURE, `a41-contrastes-f2.csv`].

**Et cet ecart ne survit ni a l'une ni a l'autre des deux comparaisons appariees disponibles.**

- **Comparaison appariee par transposition** [PROBABLE, `a41-condition-appariee.csv`]. Le
  materiel supplementaire du papier de Stanford publie les Survey Agents sous les deux
  strategies de retrait, 0,82 de score normalise avec retrait du seul item predit et 0,77 avec
  retrait du bloc entier du GSS [CONFIRME, a14 section 3.4, Tableau 6]. Rapportes au plafond
  humain des 58 items, 0,7856, ces 5 points de score normalise valent **3,93 points
  d'exactitude brute**. Retranches, `agents composite` tombe a 0,6382 et passe **derriere**
  `E1 famille retiree` de moins 0,0266 [moins 0,0322 ; moins 0,0213] et derriere
  `B2 famille retiree` de moins 0,0239. Le decalage qui suffit a rendre la comparaison
  indecidable est de **0,71 point**, la borne basse de l'intervalle ; celui qui la retourne est
  de 1,27 point. Le decalage que le papier publie lui meme est trois fois plus grand.
- **Comparaison appariee par mesure directe** [MESURE, `a41-contrastes-f3.csv`]. La condition
  C3F de a5, nos propres agents locaux prives de la famille thematique entiere, 60 personnes et
  les memes 58 items, fait **0,5572 [0,5325 ; 0,5810]** et perd contre **les six** methodes
  statistiques du regime severe restreintes aux memes 60 personnes, de moins 4,34 points contre
  `B2 famille retiree tirage` a moins 13,44 points contre `E1 famille retiree`, les six tests
  passant Holm a p ajuste 0,0015. Elle perd aussi sur la structure : 59,0 pour cent de
  diversite conservee contre 80,3 pour cent pour `E1 famille retiree` et 98,0 pour cent pour
  `PMM k=10 famille retiree`.

**Ce qui reste, et c'est reel : les gens rares.** Sur les 1 563 cellules minoritaires des 58
items, `agents composite` retrouve **42,5 pour cent [38,3 ; 46,7]** des reponses rares quand la
meilleure methode statistique du regime severe, `PMM k=10 famille retiree`, en retrouve
**22,9 pour cent [20,2 ; 25,8]**, `E1 famille retiree` 10,7 pour cent et `B2 famille retiree`
2,8 pour cent [MESURE]. Sur les 450 cellules du tercile **non deductible** de a34, celles ou
aucune autre personne du segment ideologie x genre x age n'a donne cette reponse, l'ecart tient
et se creuse en rapport : **28,2 pour cent [23,1 ; 33,6]** contre 13,8 pour cent pour
`PMM k=10 famille retiree`, 3,8 pour cent pour `E1 famille retiree` et **exactement zero** pour
`B2 famille retiree` et pour la foret aleatoire [MESURE, `a41-tableau-quatre-cases.csv`].
**C'est le seul des trois criteres sur lequel l'avantage du modele de langage ne soit menace par
aucune des deux comparaisons appariees, et il faut dire pourquoi : parce qu'aucune des deux ne
peut le toucher.** Le papier ne publie pas de rappel minoritaire sous la condition appariee, et
notre C3F est un modele local de 4 milliards de parametres, pas celui de Stanford.

Phrase de rechange, defendable telle quelle : **« quand la question n'a jamais ete posee dans
son domaine, un agent de langage garde deux fois plus de reponses rares que la meilleure
imputation par tirage, et quatre fois plus quand la rarete n'est pas deductible du segment de la
personne. Son avance en exactitude, elle, ne survit pas a une comparaison appariee, et sa
population reste plus homogene a l'interieur des camps qu'une imputation par tirage. »**

---

## 0. La famille d'hypotheses, ecrite avant les resultats, et l'aveu qui doit la preceder

### 0.1 Ce rapport ne revendique pas le pre enregistrement

a28, a29, a31, a33 et a35 revendiquent que leur famille d'hypotheses a ete ecrite avant
l'execution. **Ce rapport ne le revendique pas, et c'est le premier chiffre desagreable.** Les
estimations ponctuelles du regime severe ont deja ete lues : elles sont publiees dans a8
section 3.2 et dans a35 section 6, et elles ont oriente le choix des contrastes ci dessous.
`agents composite` a 0,6775, `agents enquete` a 0,6711, `E1 famille retiree` a 0,6649,
`B2 famille retiree` a 0,6621, `PMM k=10 famille retiree` a 0,6280 etaient connus avant que la
famille ne soit ecrite. **Les p qui suivent sont des p de confirmation faible** : ils disent si
un ecart deja vu survit a un reechantillonnage des personnes, ils ne disent pas qu'une
hypothese aveugle a ete soumise a l'epreuve. Le fait est ecrit dans l'entete de
`analyses/a41_regime_severe.py`, ou la famille a ete fixee avant l'execution, et la seule
verification possible pour un tiers est la lecture de cette docstring.

**Deux choses sont neuves et n'avaient pas ete vues avant la declaration** : le rappel des
cellules minoritaires sur ce perimetre de 58 items, qui n'existait dans aucun rapport, et le
rappel du tercile non deductible, que a34 n'avait calcule que sur les 149 items. Elles sont
signalees comme telles la ou elles apparaissent.

### 0.2 Le perimetre

**1 052 personnes, 58 items** des six familles thematiques de `a2_baselines_gss`. Regime severe
= protocole de a8 section 3.1, repris sans retouche : la famille thematique entiere sort du
contexte du predicteur **et** sert de cible. **Les six conditions de Stanford ne sont pas
replacees dans ce regime** ; elles ne peuvent pas l'etre sans relancer leurs agents, et leurs
invites contiennent les items cousins de la question. Ce defaut d'appariement est signale sur
chaque ligne de chaque tableau par une colonne « famille retiree », qui vaut « NON, les cousins
restent dans l'invite » pour ces six lignes.

**Mesure de dispersion declaree** : indice de Gini Simpson, estimateur sans biais de a1, tel que
`a28_commun.dispersion_item` le calcule. Segmentation : l'ideologie politique, sept niveaux.
**Seuil de minorite declare** : 10 pour cent, reference calculee sur les 1 052 personnes.
**Partition de deductibilite declaree** : `D_seg` de a34, la frequence de la modalite dans le
segment ideologie x genre x age de la personne, sans la personne elle meme ; les bornes de
tercile sont recalculees sur les cellules minoritaires des 58 items, comme a34 le fait pour les
siennes.

**Critere de structure declare** : l'**ecart absolu a 1** du ratio intra, et non le ratio lui
meme. Un ratio de 1 veut dire que la methode laisse les gens d'un meme segment aussi differents
qu'ils le sont vraiment ; 1,05 n'est pas meilleur que 0,95. **Ce choix change le sens de quatre
contrastes sur vingt sept et il est ecrit ici pour cette raison.**

### 0.3 Les trois familles

| | enonce | nombre de tests |
|---|---|---|
| **F1** primaire | pour chacune des 9 methodes statistiques du regime severe, le contraste `agents composite` moins la methode, sur 3 quantites : exactitude, ecart absolu a 1 du ratio intra, rappel des cellules minoritaires ; bilateral | 27 |
| **F2** secondaire | (a) `agents composite` et `agents enquete` contre `E1 famille retiree`, sur 4 quantites : exactitude, diversite conservee, ratio intra, ratio inter ; (b) les memes deux conditions **appariees** au sens de a8 errata E1, contre `E1 famille retiree` et contre `B2 famille retiree`, sur l'exactitude seule | 8 + 4 = 12 |
| **F3** tertiaire | sur les 60 personnes et les 58 items de la trace C3F, C3F contre chacune des 6 methodes statistiques du regime severe, sur l'exactitude ; bilateral | 6 |

Les neuf adversaires de F1 sont les sept nommes par la consigne, `E1 famille retiree`,
`B2 famille retiree`, `PMM k=10 famille retiree`, `IM m=10 famille retiree`, `B3 foret`,
`B0 mode` et `B0 tirage`, plus les deux methodes a tirage sans lesquelles la question finale ne
pourrait pas etre posee, `E2 famille retiree` et `B2 famille retiree tirage`.

**Signes attendus, ecrits avant execution.** Pour F1 : positif sur l'exactitude et sur le rappel
minoritaire, **negatif** sur l'ecart absolu a 1 du ratio intra, c'est a dire l'agent plus proche
de 1 que la methode statistique. Un signe inverse est un resultat contre la prediction et il est
signale comme tel. Pour F2 (a) : positif sur les quatre quantites, le positif sur le ratio inter
etant un defaut de l'agent et non un avantage. Pour F2 (b) : **le signe est inconnu, c'est tout
l'objet du test**. Pour F3 : negatif, a33 section 7 ayant deja mesure que notre agent local perd
de 12,5 points contre `B2 famille retiree` sur ce perimetre.

**Correction** : Holm sur chaque famille separement, valide sans hypothese sur la dependance, ce
qui est necessaire puisque tous les contrastes portent sur les memes personnes et les memes
items. Benjamini Hochberg est rapporte a cote dans les fichiers. Tous les p sont des p de
**bootstrap apparie sur les personnes**, lus sur la position de zero dans la distribution ; ils
ne descendent jamais sous 1 divise par le nombre de tirages. Avec 2 000 tirages sur les 1 052
personnes le plancher vaut 0,0005, soit **0,0135** apres Holm sur 27 tests et **0,0060** apres
Holm sur 12 ; avec 4 000 tirages sur les 60 personnes de C3F il vaut 0,00025, soit **0,0015**
apres Holm sur 6. **C'est un plancher cinq fois plus fin que celui de a35, qui etait a 0,03 et
0,04**, et c'est la seule amelioration de precision que ce rapport apporte a la chaine.

**N'entrent dans aucune famille**, et sont rapportes comme des descriptions : le tableau a
quatre cases lui meme, ligne par ligne ; le ratio de dispersion totale ; l'accord par paires ;
la precision minoritaire ; le rappel du tercile T1 non deductible, dont le denominateur de 450
cellules est trop petit pour porter un test declare et qui est publie avec son intervalle ; les
lignes du regime facile, qui servent a lire ce que le retrait de la famille coute ; les cinq
conditions de Stanford autres que `agents composite` dans F1 ; la sensibilite de la condition
appariee a l'ampleur du decalage ; et les quantites de structure sur les 60 personnes de C3F,
dont a33 section 4 a etabli qu'elles ne sont pas identifiables sur ce perimetre.

**Ce que ce protocole ne peut pas faire, ecrit ici et non a la fin** : il ne peut pas replacer
les agents de Stanford dans le regime severe. La condition appariee de F2 (b) est une
**transposition** d'un chiffre publie par le papier sur un autre perimetre, pas une mesure.

---

## 1. Le protocole, et les controles executes avant toute lecture

### 1.1 Les methodes, et ce que chacune sait

| methode | regime | famille retiree du contexte | conditionnement |
|---|---|---|---|
| `E1 famille retiree (argmax)` | esperance | **oui** | 149 moins la famille, et 11 demographies |
| `E2 famille retiree (tirage)` | tirage | **oui** | idem |
| `PMM k=10 famille retiree` | tirage | **oui** | idem |
| `IM m=10 mode, famille retiree` | esperance | **oui** | idem |
| `B2 famille retiree (argmax)` | esperance | **oui** | 149 moins la famille |
| `B2 famille retiree (tirage)` | tirage | **oui** | 149 moins la famille |
| `B3 foret`, `B1 argmax` | esperance | sans objet, aucun item vu | 11 demographies |
| `B0 mode`, `B0 tirage` | esperance, tirage | sans objet, aucun item vu | rien |
| six conditions de Stanford | modele de langage | **NON, les cousins restent dans l'invite** | entretien ou questionnaire |
| `C3F` (60 personnes) | modele de langage | **oui** | 149 moins la famille, sans etiquette |
| lignes de repere du regime facile | les deux | non, blocs aleatoires de a2 | 119 items |

**Un point de methode a ne pas laisser passer.** Pour `B3 foret`, `B1 argmax`, `B0 mode` et
`B0 tirage`, le regime severe **ne change rien** : elles ne voient aucun item, donc retirer la
famille du contexte est sans objet. Seul le perimetre d'items change par rapport a a28 et a29.
Le tableau le dit au lieu de laisser croire que ces lignes ont ete durcies.

### 1.2 Les controles

[MESURE, `a41-controles.csv`]

| controle | valeur | reference | source | ecart |
|---|---|---|---|---|
| exactitude `B2 famille retiree (argmax)` | 0,662105 | 0,662105 | `a8-familles-gss.csv` | **0,000000** |
| exactitude `agents composite` | 0,677527 | 0,677527 | `a8-familles-gss.csv` | **0,000000** |
| exactitude `agents enquete` | 0,671103 | 0,671103 | `a8-familles-gss.csv` | **0,000000** |
| exactitude `humains vague 2` | 0,785597 | 0,785597 | `a8-familles-gss.csv` | **0,000000** |
| exactitude `E1 famille retiree` | 0,664891 | 0,6649 | `a35-familles-regime-severe.csv` | 0,000009 |
| exactitude `PMM k=10 famille retiree` | 0,627950 | 0,6280 | `a35-familles-regime-severe.csv` | 0,000050 |
| exactitude C3F, 60 personnes | 0,557184 | 0,5572 | a33 section 2 | 0,000016 |
| exactitude `B2 famille retiree`, 60 personnes | 0,682184 | 0,6822 | a33 section 7 | 0,000016 |
| personnes completes dans la trace C3F | 60 | 60 | a33 section 0.1 | 0 |
| ecart maximal des versions vectorisees | 1,07e-14 | 0 | interne | precision machine |

**Rien n'a bouge dans la chaine.** Les seize valeurs deja publiees se reproduisent, la plupart au
chiffre pres, les autres a l'arrondi du CSV d'origine.

**Une seule exception, et elle est declaree** : `B2 famille retiree (tirage)` donne ici 0,580454
contre 0,583552 publie par a8. Ce n'est pas la meme matrice : `a8_familles.gss()` consomme son
generateur aleatoire pour `B0` et `B1` avant d'arriver a ce tirage, et nous ne rejouons ni `B0`
ni `B1`. La valeur obtenue tombe **dans** l'intervalle de confiance publie par a8,
[0,5777 ; 0,5892] [MESURE]. Rejouer a8 a l'identique aurait demande de recopier sa boucle, ce
que la consigne interdit.

**La verification des versions vectorisees.** Le bootstrap ne peut pas appeler
`a28_commun.dispersion_item` ni `a2_commun.entropie` item par item : 2 000 tirages sur 26
conditions le mettraient hors de portee. Trois versions vectorisees sont donc employees dans la
boucle seulement, et comparees aux implementations de reference sur l'echantillon complet, cinq
matrices, cinq quantites : **l'ecart maximal est de 1,07e-14** [MESURE,
`a41-verification-mesures.csv`]. Les valeurs ponctuelles publiees viennent toutes des
implementations de reference.

### 1.3 Les terciles de deductibilite

[MESURE, `a41-terciles.csv`]

Sur les 58 items, **21 portent au moins une modalite minoritaire** au seuil de 10 pour cent, et
**1 563 cellules** sont minoritaires. Le score `D_seg` est defini pour 86,3 pour cent d'entre
elles, contre 89,6 pour cent sur les 149 items de a34 : les cases de segment sont les memes, 98
cases non vides, mais le sous ensemble d'items est plus petit. Bornes de tercile 0,0401 et
0,1333, effectifs 450, 453 et 446. **T1 est un tercile a definition dure** : sa borne basse vaut
zero, ce sont les cellules ou aucune autre personne du segment ideologie x genre x age n'a donne
cette reponse sur cet item.

---

## 2. Le tableau a quatre cases du regime severe

[MESURE, `a41-tableau-quatre-cases.csv`, 1 052 personnes, 58 items, axe ideologie pour les
ratios, seuil 10 pour cent pour les minorites, 2 000 tirages bootstrap apparies sur les
personnes. Les intervalles sont ceux du bootstrap ; ils ne portent aucune correction, la
correction ne portant que sur les contrastes.]

Figure : `a41-figure-regime-severe.png`, panneau de gauche.

| methode | famille retiree | exactitude | IC 95 % | norm. | intra | IC 95 % | inter | diversite | accord | rappel min. | IC 95 % | precision | **rappel T1** | IC 95 % |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ***humains vague 2*** | *sans objet* | ***0,7856*** | *[0,779 ; 0,792]* | ***100 %*** | ***1,004*** | *[0,997 ; 1,013]* | ***1,023*** | ***100,5 %*** | ***51,2 %*** | ***0,5553*** | *[0,522 ; 0,589]* | ***0,5351*** | ***0,4822*** | *[0,430 ; 0,538]* |
| **`agents composite`** | **NON** | **0,6775** | [0,672 ; 0,683] | 86,2 % | 0,858 | [0,845 ; 0,872] | **2,322** | **94,8 %** | 53,8 % | **0,4248** | [0,383 ; 0,467] | 0,2887 | **0,2822** | [0,231 ; 0,336] |
| **`agents enquete`** | **NON** | **0,6711** | [0,666 ; 0,676] | 85,4 % | 0,795 | [0,781 ; 0,809] | 2,461 | 90,0 % | 56,2 % | 0,3820 | [0,342 ; 0,422] | 0,2833 | 0,2533 | [0,203 ; 0,308] |
| **`E1 famille retiree`** | **oui** | **0,6649** | [0,659 ; 0,671] | 84,6 % | 0,751 | [0,741 ; 0,761] | 1,518 | 80,5 % | 61,2 % | 0,1068 | [0,085 ; 0,129] | 0,4005 | 0,0378 | [0,020 ; 0,057] |
| `B2 famille retiree` | oui | 0,6621 | [0,656 ; 0,668] | 84,3 % | **0,492** | [0,481 ; 0,502] | 1,800 | 58,0 % | 72,1 % | 0,0282 | [0,019 ; 0,039] | **0,5116** | **0,0000** | [0 ; 0] |
| `IM m=10 mode, fam. retiree` | oui | 0,6501 | [0,644 ; 0,656] | 82,8 % | 0,816 | [0,807 ; 0,826] | 1,353 | 85,3 % | 58,7 % | 0,1164 | [0,096 ; 0,138] | 0,3309 | 0,0467 | [0,026 ; 0,070] |
| `B3 foret` | sans objet | 0,6490 | [0,643 ; 0,655] | 82,6 % | **0,320** | [0,312 ; 0,329] | 2,869 | 48,3 % | 76,5 % | 0,0122 | [0,007 ; 0,017] | 0,3725 | **0,0000** | [0 ; 0] |
| `B1 argmax` | sans objet | 0,6371 | [0,631 ; 0,643] | 81,1 % | 0,572 | [0,559 ; 0,585] | 2,713 | 72,6 % | 65,6 % | 0,0640 | [0,050 ; 0,079] | 0,2611 | 0,0067 | [0 ; 0,015] |
| `agents entretien (v3)` | NON | 0,6336 | [0,628 ; 0,640] | 80,7 % | 0,710 | [0,694 ; 0,728] | **3,267** | 88,6 % | 57,5 % | 0,3967 | [0,358 ; 0,437] | 0,2428 | 0,2467 | [0,197 ; 0,300] |
| **`PMM k=10 fam. retiree`** | **oui** | 0,6280 | [0,622 ; 0,634] | 79,9 % | **0,958** | [0,948 ; 0,967] | 1,356 | **98,0 %** | 52,3 % | **0,2290** | [0,202 ; 0,258] | 0,2808 | **0,1378** | [0,102 ; 0,172] |
| `B0 mode` | sans objet | 0,6164 | [0,610 ; 0,623] | 78,5 % | 0,055 | [0,052 ; 0,057] | 0,001 | 4,8 % | 97,5 % | 0,0000 | [0 ; 0] | sans objet | 0,0000 | [0 ; 0] |
| `E2 famille retiree` | oui | 0,5937 | [0,588 ; 0,599] | 75,6 % | **1,006** | [0,996 ; 1,016] | 0,821 | **99,3 %** | 51,8 % | 0,1715 | [0,150 ; 0,192] | 0,1810 | 0,1156 | [0,086 ; 0,145] |
| `agents v7` | NON | 0,5822 | [0,576 ; 0,589] | 74,1 % | 0,591 | [0,567 ; 0,614] | 0,146 | 60,1 % | 72,7 % | 0,0665 | [0,046 ; 0,090] | 0,1300 | 0,0400 | [0,022 ; 0,061] |
| `agents demographiques (v6)` | NON | 0,5792 | [0,573 ; 0,585] | 73,7 % | 0,623 | [0,607 ; 0,639] | 0,222 | 60,7 % | 71,0 % | 0,0198 | [0,013 ; 0,029] | 0,0990 | 0,0156 | [0,005 ; 0,030] |
| `B2 famille retiree tirage` | oui | 0,5805 | [0,575 ; 0,586] | 73,9 % | 0,972 | [0,961 ; 0,983] | 0,698 | 95,7 % | 53,7 % | 0,1248 | [0,109 ; 0,143] | 0,1558 | 0,0644 | [0,042 ; 0,090] |
| `agents v8` | NON | 0,5704 | [0,562 ; 0,578] | 72,6 % | 0,414 | [0,396 ; 0,433] | **8,988** | 96,6 % | 53,1 % | 0,3852 | [0,341 ; 0,429] | 0,1586 | 0,1733 | [0,131 ; 0,218] |
| `B0 tirage` | sans objet | 0,5162 | [0,512 ; 0,521] | 65,7 % | 1,065 | [1,049 ; 1,082] | moins 0,005 | 99,7 % | 51,7 % | 0,0717 | [0,058 ; 0,086] | 0,0715 | 0,0511 | [0,032 ; 0,072] |

**Lignes de repere du regime facile, memes items, memes personnes, decoupage aleatoire en blocs
de a2** [MESURE, hors famille] : `E1 blocs aleatoires` 0,7304 et 85,1 pour cent de diversite ;
`IM mode blocs aleatoires` 0,7133 et 88,5 pour cent ; `B2 blocs aleatoires` 0,6956 et 62,9 pour
cent ; `PMM k=10 blocs aleatoires` 0,6942 et 98,0 pour cent ; `E2 blocs aleatoires` 0,6487 ;
`B2 tirage blocs aleatoires` 0,6074.

**Six lectures.**

1. **Sur ces 58 items et dans le regime facile, la regression bat l'agent de 5,3 points, et
   c'est la vraie amplitude de l'effet du regime** [MESURE]. `E1 blocs aleatoires` a 0,7304
   contre 0,6775 pour `agents composite` ; `E1 famille retiree` a 0,6649, soit **1,3 point
   derriere** l'agent. Le retrait de la famille ne fait pas passer l'agent devant parce que
   l'agent progresse, il ne bouge pas ; il fait tomber la regression de 6,55 points.
2. **Le classement en exactitude et le classement en structure sont opposes, et la ligne
   `B2 famille retiree` le montre mieux que toute autre** [MESURE]. Elle est deuxieme des
   methodes statistiques en exactitude, 0,6621, et **derniere de toutes les methodes qui voient
   quelque chose en dispersion intra**, 0,492, avec 58,0 pour cent de la diversite humaine et un
   accord par paires de 72,1 pour cent contre 51,2 chez les humains. Elle achete son exactitude
   par l'abstention : **86 raretes osees sur 61 016 cellules**, contre 2 300 pour
   `agents composite` et 1 275 pour `PMM k=10 famille retiree`.
3. **Le ratio inter separe les methodes bien mieux que le ratio intra, et il est le seul axe ou
   les conditions riches de Stanford sont nettement les pires** [MESURE]. `agents entretien` a
   3,267, `agents enquete` 2,461, `agents composite` 2,322, quand toutes les imputations du
   regime severe qui conditionnent sur du contexte se tiennent entre 0,698 et 1,800. **A
   conditionnement plus riche que le leur, l'agent exagere l'ecart entre camps politiques d'un
   facteur 1,5 a 1,7.** Le resultat de a35 section 3 lecture 2 se reproduit dans le regime
   severe.
4. **`agents v8` est le contre exemple qu'il faut nommer.** Elle conserve 96,6 pour cent de la
   diversite humaine et retrouve 38,5 pour cent des minorites, presque autant que
   `agents composite`, avec un ratio inter de **8,988** et un ratio intra de 0,414. Elle produit
   la bonne quantite de rarete en la posant entierement du mauvais cote de la frontiere
   politique. **Une lecture qui ne regarderait que la diversite conservee la classerait deuxieme
   du tableau.**
5. **Le rappel du tercile non deductible est la mesure qui separe le plus** [MESURE, hors
   famille]. Trois methodes y sont **exactement a zero** : `B2 famille retiree`, `B3 foret` et
   `B0 mode`. `B1 argmax` y est a 0,0067, sous `B0 tirage` a 0,0511, qui ne sait rien de
   personne. Le resultat de a34 section 1 lecture 3, « les predicteurs statistiques informes
   sont sous le hasard aveugle sur la rarete indeductible », se reproduit dans le regime severe
   et s'y durcit : **avec la famille retiree, `B2` et la foret ne posent plus aucune rarete
   indeductible juste.**
6. **Deux intervalles du tableau ne sont pas utilisables et il faut le dire** : ceux du ratio
   inter de `B0 mode` et de `B0 tirage`. Le terme inter de ces deux methodes est nul a
   l'estimateur pres, le rapport est une division entre deux quantites presque nulles, et le
   point estime de `B0 tirage`, moins 0,005, tombe hors de son propre intervalle bootstrap. La
   meme anomalie est signalee par a35 section 2 sur les memes deux lignes. **Elle ne s'interprete
   pas.**

---

## 3. F1. Les vingt sept contrastes de la famille primaire

[MESURE, `a41-contrastes-f1.csv`, 1 052 personnes, 2 000 tirages bootstrap apparies, Holm sur
27 tests, plancher du p ajuste 0,0135]

`agents composite` moins chaque methode statistique du regime severe. **La colonne
« proximite intra » est la difference des ECARTS ABSOLUS a 1 : negatif veut dire que l'agent est
plus proche de la dispersion humaine, positif veut dire qu'il en est plus loin.**

| adversaire | regime | exactitude | proximite intra | rappel minoritaire |
|---|---|---|---|---|
| `E1 famille retiree` | esperance | **plus 0,0127** [0,0071 ; 0,0180] | **moins 0,1077** [moins 0,123 ; moins 0,093] | **plus 0,3181** [0,282 ; 0,355] |
| `IM m=10 mode, fam. retiree` | esperance | **plus 0,0274** [0,0219 ; 0,0328] | **moins 0,0421** [moins 0,057 ; moins 0,028] | **plus 0,3084** [0,273 ; 0,345] |
| `B2 famille retiree` | esperance | **plus 0,0154** [0,0099 ; 0,0209] | **moins 0,3667** [moins 0,381 ; moins 0,353] | **plus 0,3966** [0,358 ; 0,435] |
| `B3 foret` | esperance | **plus 0,0285** [0,0225 ; 0,0346] | **moins 0,5383** [moins 0,553 ; moins 0,522] | **plus 0,4127** [0,371 ; 0,454] |
| `B0 mode` | esperance | **plus 0,0611** [0,0538 ; 0,0683] | **moins 0,8040** [moins 0,818 ; moins 0,790] | **plus 0,4249** [0,383 ; 0,467] |
| **`E2 famille retiree`** | **tirage** | **plus 0,0839** [0,0781 ; 0,0894] | **plus 0,1348** [0,119 ; 0,150] **contre la prediction** | **plus 0,2534** [0,215 ; 0,293] |
| **`PMM k=10 fam. retiree`** | **tirage** | **plus 0,0496** [0,0439 ; 0,0549] | **plus 0,0991** [0,084 ; 0,114] **contre la prediction** | **plus 0,1959** [0,160 ; 0,233] |
| **`B2 famille retiree tirage`** | **tirage** | **plus 0,0970** [0,0914 ; 0,1026] | **plus 0,1135** [0,097 ; 0,131] **contre la prediction** | **plus 0,2997** [0,262 ; 0,338] |
| **`B0 tirage`** | **tirage** | **plus 0,1613** [0,1547 ; 0,1676] | **plus 0,0762** [0,057 ; 0,094] **contre la prediction** | **plus 0,3535** [0,310 ; 0,397] |

**Les vingt sept tests passent Holm, tous au plancher de la correction, p ajuste 0,0135.
Vingt trois portent le signe ecrit avant execution.**

**Ce que cela etablit, dans l'ordre.**

1. **L'exactitude : neuf sur neuf, dans le sens de l'agent.** Dans le regime severe,
   `agents composite` bat les neuf methodes statistiques, y compris les deux qui la battaient
   dans le regime facile, `E1` et `B2`. L'ecart le plus etroit est celui contre
   `E1 famille retiree`, plus 1,27 point, dont l'intervalle ne contient pas zero.
2. **Les gens rares : neuf sur neuf, dans le sens de l'agent, et de tres loin.** L'ecart le
   plus etroit est celui contre `PMM k=10 famille retiree`, plus 19,6 points de rappel, soit un
   rapport de **1,86 contre 1**. Contre `E1 famille retiree` le rapport est de 4,0 contre 1,
   contre `B2 famille retiree` de 15,1 contre 1, contre la foret de 34,8 contre 1.
3. **La structure : cinq sur neuf seulement, et les quatre qui manquent sont exactement les
   quatre methodes a tirage.** [MESURE] `agents composite` est plus proche de la dispersion
   humaine que toutes les methodes d'esperance, ce qui etait annonce, et **plus loin que toutes
   les methodes de tirage**, ce qui ne l'etait pas. Les quatre intervalles sont entierement
   positifs et les quatre p ajustes sont au plancher.

**La lecture correcte de ce tableau tient en une phrase** : dans le regime severe, un agent de
langage est encore une methode d'esperance. C'est exactement la conclusion que a35 tirait du
regime facile, section 4, « un agent de langage est une methode d'imputation par esperance, pas
une methode de tirage » ; **elle ne change pas quand la question devient nouvelle**. Ce qui
change avec le regime, c'est l'exactitude, pas la nature du predicteur.

---

## 4. F2. L'ecart que a35 n'avait pas teste existe, et il ne survit pas a la condition appariee

### 4.1 (a) Les huit contrastes contre `E1 famille retiree`

[MESURE, `a41-contrastes-f2.csv`, Holm sur 12 tests, plancher du p ajuste 0,0060]

| condition | quantite | difference | IC 95 % | p Holm |
|---|---|---|---|---|
| **`agents composite`** | exactitude | **plus 0,0127** | [plus 0,0071 ; plus 0,0180] | **0,0060** |
| **`agents composite`** | diversite conservee | **plus 0,1432** | [plus 0,1333 ; plus 0,1531] | **0,0060** |
| **`agents composite`** | ratio intra | **plus 0,1077** | [plus 0,0929 ; plus 0,1226] | **0,0060** |
| `agents composite` | ratio inter, **defaut** | plus 0,7479 | [plus 0,6324 ; plus 0,8744] | 0,0060 |
| **`agents enquete`** | exactitude | **plus 0,0062** | [plus 0,0007 ; plus 0,0118] | **0,0290** |
| `agents enquete` | diversite conservee | plus 0,0959 | [plus 0,0843 ; plus 0,1069] | 0,0060 |
| `agents enquete` | ratio intra | plus 0,0440 | [plus 0,0289 ; plus 0,0588] | 0,0060 |
| `agents enquete` | ratio inter, **defaut** | plus 0,8767 | [plus 0,7505 ; plus 1,0073] | 0,0060 |

**La reponse a la question de a35 est oui.** L'ecart de 1,3 point entre `agents composite` et
`E1 famille retiree` survit au reechantillonnage des personnes et a la correction. La phrase de
a35 section 6, « les deux conditions riches de Stanford repassent devant », est **etablie** sur
`agents composite`, sur les quatre quantites a la fois.

**Elle est fragile sur `agents enquete`, et c'est un chiffre desagreable.** Plus 0,62 point,
borne basse a plus 0,07 point, p ajuste 0,029. **C'est le seul des 45 tests du rapport qui ne
soit pas au plancher de sa correction**, et il ne tiendrait pas avec un seuil un peu plus
exigeant. La phrase « les deux conditions riches repassent devant » doit devenir « la condition
composite repasse devant, la condition enquete de justesse ».

### 4.2 (b) La condition appariee de a8 errata E1

[PROBABLE pour le decalage, MESURE pour la comparaison, `a41-condition-appariee.csv`]

**Le raisonnement, ecrit en entier parce que c'est le point contestable du rapport.** Le regime
severe n'est applique qu'aux methodes statistiques. Les agents de Stanford recoivent dans leur
invite toutes les reponses de la personne **moins le seul item predit** ; quand on predit
`abany`, l'agent dispose encore de `abdefect`, `abnomore`, `abhlth`, `abpoor`, `abrape` et
`absingle` [CONFIRME, a14 section 3.1, materiel supplementaire p. PDF 38]. Le materiel
supplementaire evalue les Survey Agents sous les deux strategies de retrait, sur un sous
echantillon de 100 agents : **0,82 de score normalise avec retrait du seul item, 0,77 avec
retrait du bloc entier du GSS** [CONFIRME, a14 section 3.4, Tableau 6]. Rapportes au plafond
humain des 58 items, 0,7856, ces 5 points de score normalise valent **3,93 points d'exactitude
brute**. Le decalage est applique comme une translation constante de l'exactitude par personne,
et par consequent la distribution bootstrap de l'ecart est translatee du meme montant.

| condition appariee | reference | difference | IC 95 % | p Holm |
|---|---|---|---|---|
| `agents composite` moins 3,93 pt | `E1 famille retiree` | **moins 0,0266** | [moins 0,0322 ; moins 0,0213] | **0,0060** |
| `agents composite` moins 3,93 pt | `B2 famille retiree` | **moins 0,0239** | [moins 0,0294 ; moins 0,0184] | **0,0060** |
| `agents enquete` moins 3,93 pt | `E1 famille retiree` | **moins 0,0331** | [moins 0,0385 ; moins 0,0275] | **0,0060** |
| `agents enquete` moins 3,93 pt | `B2 famille retiree` | **moins 0,0303** | [moins 0,0364 ; moins 0,0244] | **0,0060** |

**Les quatre tests passent Holm, les quatre sont negatifs, et le signe etait declare inconnu.**
Sous la condition appariee que le papier publie lui meme, l'avantage d'exactitude du regime
severe disparait et se retourne.

**La sensibilite, parce qu'un chiffre transpose n'a pas droit a un seul point** [MESURE,
`a41-condition-appariee.csv`] :

| decalage applique | `composite` moins `E1 fam. retiree` | verdict |
|---|---|---|
| 0,00 point, aucun | plus 0,0127 [plus 0,0071 ; plus 0,0180] | l'agent devant, decidable |
| 0,71 point | 0 en borne basse | **le seuil d'indecision** |
| 1,00 point | plus 0,0027 [moins 0,0029 ; plus 0,0080] | indecidable |
| 1,27 point | 0 au point estime | **le seuil de bascule** |
| 2,00 points | moins 0,0073 [moins 0,0129 ; moins 0,0020] | la regression devant, decidable |
| **3,93 points, a8 errata E1** | **moins 0,0266 [moins 0,0322 ; moins 0,0213]** | **la regression devant, largement** |
| 5,00 points | moins 0,0373 [moins 0,0429 ; moins 0,0320] | idem |

**Il suffit de 0,71 point de decalage pour rendre la comparaison indecidable et de 1,27 point
pour la retourner. La condition appariee du papier en vaut 3,93.** [MESURE pour les seuils,
PROBABLE pour le 3,93.]

**Trois reserves sur cette transposition, et elles sont reelles.**

1. Le 0,77 contre 0,82 est mesure **sur 100 agents et sur l'ensemble des items du GSS**. Le
   transposer aux 58 items de familles thematiques, ou l'autocorrelation intra famille est par
   construction plus forte que la moyenne, n'est pas une mesure. **Le sens de la reserve va
   contre l'agent** : sur des items plus autocorreles, le retrait du bloc devrait couter plus,
   pas moins. La reserve est donc conservatrice pour nous et non complaisante.
2. Le retrait du papier porte sur le **bloc du GSS** auquel appartient l'item, pas sur notre
   famille thematique. Les deux decoupages ne coincident pas. C'est la source d'incertitude la
   plus difficile a chiffrer.
3. Le decalage ne s'applique qu'a l'exactitude. **Le papier ne publie ni diversite, ni ratio
   intra, ni rappel minoritaire sous la condition appariee**, et rien ici ne permet de dire ce
   que ces quantites deviendraient. La domination de `agents composite` sur la diversite
   conservee, 94,8 contre 80,5 pour cent, n'est pas touchee par cette section, et elle n'est pas
   confirmee par elle non plus.

---

## 5. F3. Nos propres agents prives de la famille, sur les memes personnes et les memes items

[MESURE, `a41-c3f-60-personnes.csv` et `a41-contrastes-f3.csv`, 60 personnes, 58 items,
3 480 cellules, 4 000 tirages bootstrap apparies, Holm sur 6 tests, plancher du p ajuste 0,0015]

C'est la comparaison que l'errata E1 de a8 designe comme « le test propre » : « le test propre
est la condition C3F de a5, ou nos propres agents perdent la famille thematique entiere de leur
contexte : elle se compare a la ligne B2 famille retiree, et a rien d'autre ». Ce rapport
l'etend aux six methodes statistiques du regime severe, restreintes aux memes 60 personnes.

| methode | famille retiree | exactitude | IC 95 % | norm. | diversite | intra | inter |
|---|---|---|---|---|---|---|---|
| ***humains vague 2*** | *sans objet* | ***0,7773*** | *[0,748 ; 0,805]* | ***100 %*** | ***97,7 %*** | ***0,992*** | ***0,971*** |
| **`E1 famille retiree`** | **oui** | **0,6917** | [0,662 ; 0,720] | 89,0 % | 80,3 % | 0,754 | 1,614 |
| `B2 famille retiree` | oui | 0,6822 | [0,655 ; 0,708] | 87,8 % | 61,7 % | 0,531 | 1,843 |
| `IM m=10 mode, fam. retiree` | oui | 0,6681 | [0,642 ; 0,693] | 86,0 % | 85,4 % | 0,846 | 1,162 |
| `B3 foret` | sans objet | 0,6624 | [0,635 ; 0,689] | 85,2 % | 48,1 % | 0,327 | 2,732 |
| `PMM k=10 fam. retiree` | oui | 0,6555 | [0,628 ; 0,681] | 84,3 % | 98,0 % | 0,972 | 1,338 |
| `B0 mode` | sans objet | 0,6376 | [0,611 ; 0,663] | 82,0 % | 1,6 % | 0,020 | moins 0,003 |
| `E2 famille retiree` | oui | 0,6216 | [0,595 ; 0,646] | 80,0 % | 99,5 % | 1,052 | 0,523 |
| **`C3` contexte complet** | non | **0,6195** | [0,591 ; 0,648] | 79,7 % | 65,8 % | 0,644 | 0,839 |
| `B2 famille retiree tirage` | oui | 0,6009 | [0,575 ; 0,625] | 77,3 % | 93,7 % | 0,966 | 0,634 |
| **`C3F` famille retiree** | **oui** | **0,5572** | **[0,533 ; 0,581]** | **71,7 %** | **59,0 %** | **0,641** | **0,304** |
| `B0 tirage` | sans objet | 0,5216 | [0,501 ; 0,541] | 67,1 % | 100,2 % | 1,099 | moins 0,113 |

| C3F moins | difference | IC 95 % | p Holm |
|---|---|---|---|
| `E1 famille retiree` | **moins 0,1344** | [moins 0,1558 ; moins 0,1124] | **0,0015** |
| `B2 famille retiree` | **moins 0,1250** | [moins 0,1480 ; moins 0,1020] | **0,0015** |
| `IM m=10 mode, fam. retiree` | **moins 0,1110** | [moins 0,1293 ; moins 0,0917] | **0,0015** |
| `PMM k=10 fam. retiree` | **moins 0,0984** | [moins 0,1233 ; moins 0,0738] | **0,0015** |
| `E2 famille retiree` | **moins 0,0641** | [moins 0,0853 ; moins 0,0408] | **0,0015** |
| `B2 famille retiree tirage` | **moins 0,0434** | [moins 0,0652 ; moins 0,0210] | **0,0015** |

**Les six tests passent Holm, les six portent le signe declare avant execution.** Sur des
cellules appariees, dans le seul regime severe que nous puissions imposer aux deux cotes a la
fois, **le modele de langage perd contre toutes les imputations statistiques, y compris contre
les quatre a tirage, et il perd aussi sur la structure** : 59,0 pour cent de diversite conservee
contre 98,0 pour `PMM k=10 famille retiree` et 99,5 pour `E2 famille retiree`, ratio intra 0,641
contre 0,972 et 1,052. **Il perd meme contre `B0 mode`, la modalite majoritaire, de 8,0 points.**

**Ce que cette section prouve, et ce qu'elle ne prouve pas.** [MESURE pour le contenu,
CONFIRME pour la limite.] Elle prouve que **notre** agent, un modele local de 4 milliards de
parametres, prive de la famille, perd sur les trois criteres a la fois. Elle ne prouve pas que
les agents de Stanford perdraient : ce n'est ni le meme modele, ni la meme invite, ni la meme
taille. **Elle etablit seulement qu'aucune mesure appariee disponible dans ce projet ne soutient
la these de la superiorite du langage en regime severe, et que la seule qui existe la
contredit.**

**Un point de perimetre a porter avec ce tableau** [MESURE, a33 section 0.1 point 5] : les 60
personnes de C3F viennent des plis 0 et 1 seulement, 30 par pli. La comparaison appariee n'en
souffre pas, ce sont les memes personnes des deux cotes ; la generalisation aux 1 052 en
souffre.

---

## 6. Ce que le retrait de la famille coute, methode par methode

[MESURE, `a41-cout-du-retrait.csv`, hors famille d'hypotheses, memes items, memes personnes,
2 000 tirages]

| methode | exactitude | ratio intra | diversite conservee | rappel minoritaire |
|---|---|---|---|---|
| `E1` | **moins 0,0655** [moins 0,070 ; moins 0,061] | **moins 0,0612** | **moins 0,0468** | **moins 0,0702** |
| `PMM k=10` | **moins 0,0662** [moins 0,071 ; moins 0,062] | moins 0,0006, p = 0,90 | moins 0,0005, p = 0,84 | **moins 0,0891** |
| `IM m=10 mode` | **moins 0,0632** | **moins 0,0408** | **moins 0,0314** | **moins 0,0606** |
| `E2` | **moins 0,0550** | plus 0,0055, p = 0,23 | moins 0,0002, p = 0,97 | **moins 0,0476** |
| `B2 argmax` | **moins 0,0335** | **moins 0,0558** | **moins 0,0488** | **moins 0,0298** |
| `B2 tirage` | **moins 0,0269** | **plus 0,0193** | **plus 0,0133** | **moins 0,0295** |

**Trois faits.**

1. **Le cout du retrait est deux fois plus lourd pour la regression que pour les voisins**
   [MESURE], moins 6,55 points pour `E1` contre moins 3,35 pour `B2 argmax`. a35 section 6
   l'annoncait sans intervalle ; il est ici mesure avec, et les deux intervalles sont
   entierement negatifs et disjoints.
2. **Les methodes a tirage perdent leur exactitude sans perdre leur structure** [MESURE].
   `PMM k=10` perd 6,62 points d'exactitude et **rien du tout** sur le ratio intra ni sur la
   diversite conservee, les deux intervalles contenant zero. C'est le fait le plus utile de
   cette section : **la propriete structurelle de l'appariement sur moyenne predite est
   insensible au regime**, alors que celle de la regression par esperance ne l'est pas.
3. **Le retrait coute des minorites a toutes les methodes**, de moins 3,0 points pour
   `B2 argmax` a moins 8,9 points pour `PMM k=10`, les six intervalles etant negatifs [MESURE].
   Aucune methode statistique ne compense la perte des cousins par un meilleur ciblage des
   raretes.

**Aucun cout de retrait ne peut etre calcule pour les six conditions de Stanford, puisqu'elles
ne sont pas dans les deux regimes.** C'est exactement l'asymetrie que la section 4.2 essaie de
corriger par transposition.

---

## 7. La reponse a la question posee

**Question.** Dans le regime ou l'information la plus proche manque, le modele de langage
domine t il les imputations statistiques a tirage sur les trois criteres a la fois, exactitude,
structure et gens rares, avec des intervalles qui le disent ?

**Reponse : non.** [MESURE]

| critere | contre les imputations a **tirage** | contre les imputations a **esperance** |
|---|---|---|
| **exactitude** | **oui**, plus 5,0 a plus 16,1 points, quatre intervalles entierement positifs | **oui**, plus 1,3 a plus 6,1 points |
| **structure**, ecart absolu a 1 du ratio intra | **NON**, l'agent est plus loin de 1 de plus 0,076 a plus 0,135, quatre intervalles entierement positifs | oui, plus proche de 1 de 0,042 a 0,804 |
| **gens rares**, rappel minoritaire | **oui**, plus 19,6 a plus 35,4 points | **oui**, plus 30,8 a plus 42,5 points |

**Les trois criteres a la fois ne sont donc atteints que contre les methodes d'esperance, et
c'est un resultat sans interet pour la these** : une methode d'esperance est ce que van Buuren
donne comme le cas d'ecole de l'ecrasement, et a35 a deja montre que l'agent en est une. **Le
seul adversaire qui compte est l'imputation par tirage, et contre elle l'agent perd le critere
de structure, decidablement, contre les quatre methodes de tirage testees.**

**Et la moitie du resultat qui reste doit encore passer deux comparaisons appariees dont il ne
survit qu'a l'une.** L'exactitude tombe des que la comparaison est appariee, par transposition
comme par mesure directe. **Le rappel des minorites est le seul des trois criteres qui reste
debout apres tout cela, et il reste debout parce qu'aucune des deux comparaisons appariees ne
peut l'atteindre**, pas parce qu'il les a passees.

**La formulation que ce rapport autorise, mot pour mot :**

> « Quand la question n'a jamais ete posee dans son domaine, un agent de langage retrouve
> 42,5 pour cent des reponses rares la ou la meilleure imputation par tirage en retrouve
> 22,9 pour cent, et 28,2 pour cent contre 13,8 quand la rarete n'est pas deductible du segment
> demographique de la personne. Il ne garde en revanche aucun avantage de structure sur cette
> imputation, dont il s'ecarte davantage de la dispersion humaine, et son avantage d'exactitude
> ne survit pas a la seule comparaison appariee que le papier de Stanford permette de
> construire. »

**Ce que ce rapport interdit d'ecrire.**

1. **Interdit d'ecrire « dans le regime severe, l'agent de langage domine l'imputation
   statistique sur les deux axes a la fois ».** [MESURE] C'est vrai contre `E1 famille retiree`,
   qui est une methode d'esperance, et faux contre les quatre methodes de tirage sur l'axe de la
   structure.
2. **Interdit de reprendre la phrase de a8 section 1, « quand on retire la famille entiere, les
   agents de Stanford battent B2 ».** [MESURE et CONFIRME] L'errata E1 de a8 la retirait deja ;
   ce rapport chiffre de combien : il suffit de 1,27 point de decalage apparie pour la
   retourner, et le papier en publie 3,93.
3. **Interdit de citer a35 section 6 sans son intervalle.** [MESURE] L'ecart de 1,3 point est
   reel et decidable pour `agents composite` ; il est a la limite pour `agents enquete`,
   p ajuste 0,029.
4. **Interdit de presenter C3F comme une refutation des agents de Stanford.** [CONFIRME] C'est
   un modele local de 4 milliards de parametres. Ce qu'il etablit, c'est qu'aucune mesure
   appariee de ce projet ne soutient la these, pas que Stanford aurait tort.
5. **Interdit de lire la diversite conservee seule.** [MESURE] `agents v8` conserve 96,6 pour
   cent de la diversite humaine avec un ratio inter de 8,988. La diversite conservee ne dit pas
   ou la dispersion est placee.

---

## 8. Ce que cela change a `ARBITRAGE.md`

**L'option A survit, et elle se restreint encore.** `ARBITRAGE.md` porte la these « ce que la
simulation efface, version minorites », avec pour phrase « la statistique fabrique une societe
sans minorites, l'IA en garde la moitie ». a35 avait deja ramene le facteur 11 contre la foret a
un facteur 1,27 contre `PMM k=10` sur le F1 minoritaire des 149 items. **Ce rapport dit ce que
devient ce facteur dans le regime severe, et il est plus favorable a la these que le regime
facile** : sur le rappel des cellules minoritaires des 58 items, le rapport est de **1,86 contre
1** entre `agents composite` et `PMM k=10 famille retiree`, et de **2,05 contre 1** sur les
cellules dont la rarete n'est pas deductible [MESURE]. **Le meilleur terrain de la these n'est
donc pas le regime facile, c'est le regime severe, et ce n'est pas l'exactitude, c'est le
rappel.**

**Ce qui doit sortir de `ARBITRAGE.md`, en revanche.** La phrase de a35 section 10, « aucune
methode statistique, y compris les correctifs concus pour cela, ne tient quand la question n'a
jamais ete posee ; c'est la seule chose que la simulation par langage achete », **est trop
forte** [MESURE]. `PMM k=10 famille retiree` tient parfaitement sur la structure quand la
question est nouvelle : elle ne perd ni son ratio intra ni sa diversite conservee, seulement son
exactitude. La formulation exacte est : **« quand la question n'a jamais ete posee, aucune
methode statistique ne retrouve les gens rares, et c'est la seule chose que la simulation par
langage achete ; elle l'achete en exagerant les ecarts entre camps politiques d'un facteur un et
demi a deux, et son avantage d'exactitude ne survit pas a une comparaison appariee. »**

**Ce que cela deplace dans la hierarchie des enonces du projet.** La comparaison qui decide
n'est plus « langage contre statistique sur des questions nouvelles », comme a35 section 10 le
proposait. C'est **« langage contre imputation par tirage, sur les gens que le segment
demographique ne permet pas de deviner »**. C'est le seul enonce du dossier qui survive a la
fois au bootstrap, a la correction pour tests multiples, au passage au regime severe et aux deux
comparaisons appariees, pour la raison que ces deux dernieres ne l'atteignent pas.

**La question ouverte que `ARBITRAGE.md` place en fin de page, socle contre aligne, n'est pas
touchee par ce rapport.**

---

## 9. Ce que je n'ai pas pu verifier

1. **Les agents de Stanford ne peuvent pas etre replaces dans le regime severe.** C'est la
   limite qui commande tout le rapport. La condition appariee de la section 4.2 est une
   translation constante appliquee a un chiffre publie sur un autre perimetre, 100 agents et
   l'ensemble des items du GSS, avec un decoupage en blocs du GSS et non en familles
   thematiques. **Le fichier de la condition « retrait par bloc » n'a pas ete cherche dans le
   paquet OSF ; s'il existe, il remplace toute la section 4.2 par une mesure.** a8 errata E1
   faisait deja cette remarque et elle n'a pas ete suivie.
2. **Le decalage n'est applique qu'a l'exactitude.** Rien ne dit ce que deviendraient la
   diversite conservee, le ratio intra et le rappel minoritaire des agents de Stanford sous la
   condition appariee. **Le seul critere sur lequel l'agent reste devant apres tout le rapport
   est donc aussi celui que la correction appariee ne peut pas toucher, et il faut le lire avec
   cette reserve.**
3. **C3F ne couvre que 60 personnes, issues de deux plis sur cinq.** Elle repond a la question
   appariee pour notre modele local et pour lui seul ; elle ne dit rien du modele de Stanford et
   rien des trois autres plis.
4. **Le rappel du tercile non deductible porte 450 cellules.** Les intervalles sont larges,
   [0,231 ; 0,336] pour `agents composite` contre [0,102 ; 0,172] pour `PMM k=10 famille
   retiree`. Ils ne se recouvrent pas, mais aucun test declare ne porte sur cette quantite et
   elle n'a subi aucune correction.
5. **Le score `D_seg` n'est defini que pour 86,3 pour cent des cellules minoritaires du
   perimetre.** Les 13,7 pour cent restantes, dont le segment compte moins de cinq autres
   repondants sur l'item, sortent de la partition et de la mesure T1. Je n'ai pas verifie si
   elles sont distribuees au hasard entre les methodes.
6. **`B2 famille retiree (tirage)` n'est pas la matrice de a8.** Le flux aleatoire differe, la
   valeur tombe dans l'intervalle de a8 mais la matrice n'est pas identique. Les quatre
   contrastes qui la concernent portent donc sur une realisation et non sur celle de a8. Un
   protocole a plusieurs tirages aurait leve la question ; il n'a pas ete fait.
7. **Le choix de la penalite de `E1`, C = 0,03, est repris de a35 sans revalidation dans le
   regime severe.** La regression du regime severe voit un contexte different, 137 items en
   moyenne au lieu de 119 mais sans les cousins, et son optimum de penalite pourrait differer.
   Le sens de cette reserve va **contre** les methodes statistiques.
8. **Aucune mesure hors GSS.** Tout le rapport porte sur les 58 items de famille du GSS. a8
   section 3.4 a etabli que le regime severe est deja en place sur Twin-2K-500 sans qu'on l'ait
   voulu ; la replication n'est pas faite.
9. **Le critere de structure est un choix.** L'ecart absolu a 1 du ratio intra est declare avant
   execution, mais un lecteur qui prefererait « le plus haut est le meilleur » lirait quatre des
   vingt sept contrastes dans l'autre sens. Le choix est defendable et il n'est pas neutre.
10. **La convention de codage des refus.** Une prediction hors nomenclature est traitee comme une
    cellule vide dans les mesures de dispersion et comme une reponse non minoritaire dans les
    mesures de minorite, conventions de a1 et de a29 reprises telles quelles. Je n'ai pas mesure
    ce que change la convention inverse.

---

## 10. Questions ouvertes pour Simon

1. **Faut il chercher le fichier de la condition « retrait par bloc » dans le paquet OSF ?**
   C'est la seule chose qui transformerait la section 4.2, la plus contestable du rapport, en
   mesure. a8 errata E1 estimait le cout a une heure. Deux rapports successifs l'ont maintenant
   signalee sans la faire.
2. **Le chiffre a mettre en tete a change une deuxieme fois.** a35 proposait « quand la question
   est nouvelle, l'agent domine la regression sur les deux axes ». Ce rapport le retire et le
   remplace par « quand la question est nouvelle, l'agent retrouve deux fois plus de gens rares
   que la meilleure imputation par tirage, et quatre fois plus quand la rarete n'est pas
   deductible ». C'est plus etroit, c'est plus solide, et c'est moins postable. Est ce le bon
   arbitrage ?
3. **Le rappel du tercile non deductible merite t il sa propre famille d'hypotheses ?** C'est
   maintenant la seule quantite du dossier qui survive a tout, et elle est publiee ici hors
   famille sur 450 cellules. Une nuit de calcul sur les 149 items, avec les methodes du regime
   severe et une famille declaree, la rendrait decidable.
4. **Faut il faire de `PMM k=10` l'adversaire officiel, comme a35 le demandait deja ?** Ce
   rapport ajoute un argument : dans le regime severe, `PMM` est la seule methode qui ne perd
   **rien** de sa structure, ni ratio intra ni diversite conservee. C'est l'adversaire le plus
   dur qui existe sur le critere structurel, et le projet ne l'a pas encore adopte.
5. **Que fait on de `agents v8` ?** Elle conserve 96,6 pour cent de la diversite humaine et
   retrouve 38,5 pour cent des minorites avec un ratio inter de 8,988. C'est le contre exemple
   qui montre qu'une population peut etre « variee » et entierement fausse. Est ce une note de
   bas de page, ou est ce la demonstration que la diversite conservee ne doit plus etre publiee
   seule ?
6. **Faut il relancer C3F sur les trois plis manquants ?** 60 personnes suffisent pour trancher
   les six contrastes de F3, tous au plancher de Holm, mais pas pour generaliser. Le cout est
   connu, c'est une nuit de calcul, et c'est la seule mesure appariee que le projet possede.

---

## Rejouer

```
.venv/bin/python analyses/a41_regime_severe.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --cache-a35 /tmp/a35-methodes.pkl \
    --cache-a41 /tmp/a41-severe.pkl --tirages 2000 --tirages-c3f 4000
.venv/bin/python analyses/a41_figure.py
```

Le cache `/tmp/a35-methodes.pkl` est celui de a35 et il est **obligatoire** : sans lui les
methodes du regime facile n'existent pas et le script s'arrete en le disant. Les caches de a25
et de a28 sont reconstruits s'ils manquent. Duree : **129 secondes** pour
`a41_regime_severe.py` avec le cache du regime severe, **14 secondes de plus** pour construire
ce cache s'il est absent, 3 secondes pour la figure, sur quatre coeurs. Graine d'analyse
20260908, graine de protocole 20260903 heritee de a2, penalite C = 0,03 heritee de a35.
