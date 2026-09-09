# a44. Le generateur nul conditionnellement independant de Yuan, applique a nos populations simulees

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Sections 7.2 et 10 point 3 : « le meme modele et le meme run sans etiquette » devient un contraste de conditionnement. Objection a45 numero 1, contradiction D1.

**Phrases d'origine.** Section 7.2 : « Et le depart passe par l'etiquette, pas par le langage
[MESURE] : v8 et C2 sont du cote du gabarit, **C3, qui est le meme modele et le meme run sans
etiquette**, est du cote de la personne, 0,449 contre 0,073 ». Section 10, autorise 3 :
« **Le depart passe par l'etiquette et non par le langage** [MESURE]. C3, meme modele, meme
run, sans etiquette, est a 44,9 pour cent du plancher humain ».

**Correction.** C3 n'est pas C2 moins l'etiquette : c'est C2 dont toute l'entree a ete
remplacee. La revendication « le depart passe par l'etiquette et non par le langage » doit
etre affaiblie en « le depart passe par le conditionnement et non par le moteur », ce que le
rapport etablit par ailleurs proprement avec `B1` et `B3 foret`, qui sont du cote du gabarit
sans etre des modeles de langage. La part attribuable a l'etiquette seule n'est pas bornee
par ce dossier.

**Ce que les deux invites contiennent, mesure sur le code.**
[CONFIRME, `analyses/a5_agents_locaux_gss.py`, `systeme_c2` lignes 164 a 177 et `systeme_c3`
lignes 180 a 196]

| | contenu de l'invite systeme | etiquette ideologique | reponses de la personne |
|---|---|---|---|
| C2 | les **onze attributs** de `demographic_summary.csv`, et rien d'autre | oui, ligne `Political ideology` | **aucune** |
| C3 | les **environ 119 items de contexte**, question et reponse en clair | **non** | oui, toutes |

C2 et C3 ne different donc pas par la presence ou l'absence de l'etiquette : **ils echangent
integralement leur entree**. Le contraste melange deux changements, le retrait de l'etiquette
et le remplacement de la personne par onze attributs ; ses deux facteurs sont confondus et
aucun des textes du dossier ne les separe.

**Ce que le second facteur vaut a lui seul.** `B1 argmax` est une regression sur les memes
onze attributs, `B2 argmax` un plus proche voisin sur les memes 119 items **sans aucune
demographie** [CONFIRME, `a2_baselines_gss.py` lignes 178 et 188 : `enc.transform` n'alimente
que `B1`, `B2` ne voit que `codes[:, contexte]`]. A moteur statistique constant et sans
aucune ablation d'etiquette, le passage de l'un a l'autre deplace la chute sous permutation
de **0,175 a 0,357 du plancher humain**, un facteur 2,0 ; le passage de C2 a C3 vaut un
facteur 6,2 [MESURE, `a47-chute-deux-segmentations.csv`, segmentation `S_ideo`].

**L'ablation propre n'est pas dans ce dossier.** Elle est le run R3 de la nuit du 8 au
9 septembre : C3 plus etiquette contre C3, et C2 prive de la seule ligne `Political
ideology` contre C2. Tant qu'il n'a pas rendu, aucun texte ne doit ecrire « ablation de
l'etiquette » ni « seule l'etiquette bouge ».

### E2. Sections 5.2 et 7.2 : la chute sous permutation n'est pas invariante a la segmentation, et « 7 pour cent » est indexe sur l'axe politique. Objection a45 numero 2.

**Phrases d'origine.** Section 5.2, lecture 3 : « `agents v8` et C2, les deux conditions a
etiquette seule, perdent 2,5 et 2,4 pour cent, **soit 7 pour cent du plancher humain**, et se
placent a deux points des temoins aveugles. » Section 7.2 : « Seuil de lecture, non declare
avant : « gabarit » si la chute vaut moins de **15 pour cent** du plancher humain ».

**Correction.** Les deux segmentations publiees, `S_ideo` et `S_fin`, **contiennent l'une et
l'autre l'ideologie**, c'est a dire la variable meme que l'invite de C2 et de `v8` recoit.
La permutation y mesure ce que l'agent sait au dela de ce qu'on vient de fixer, et non s'il
porte la personne. Sous une segmentation de finesse comparable qui ne contient pas
l'ideologie, genre x race x age, 38 cellules contre 42 pour `S_fin`, le chiffre change de
facteur.

**Preuve.** [MESURE, `a47-chute-deux-segmentations.csv`, produit par
`analyses/a47_chute_segmentations.py`, qui reimporte `a44_commun.permuter_intra`,
`a44_mesures.exactitude_codes` et `a44_mesures.reassignation_codes` sans modification ;
200 permutations par cellule, memes caches, meme codage. Les colonnes `S_ideo` et `S_fin`
reproduisent `a44-permutation.csv` au millieme.]

Part du plancher humain, chute relative de la condition divisee par celle des memes humains
reinterroges sur le meme perimetre :

| condition | `S_ideo` (publiee) | `S_fin` (publiee) | **genre x race x age, sans ideologie** |
|---|---|---|---|
| `agents v8` | **0,072** | 0,055 | **0,267** |
| **C2** | **0,073** | 0,074 | **0,185** |
| `B3 foret` | 0,129 | 0,082 | 0,187 |
| `agents v7` | 0,156 | 0,137 | 0,150 |
| `B1 argmax` | 0,175 | 0,117 | 0,228 |
| `agents demographiques (v6)` | 0,235 | 0,229 | 0,236 |
| `B2 argmax` | 0,357 | 0,348 | 0,424 |
| **C3** | **0,448** | 0,455 | **0,458** |
| `agents entretien (v3)` | 0,532 | 0,526 | 0,613 |
| `agents enquete` | 0,539 | 0,548 | 0,618 |
| `PMM k=10` | 0,595 | 0,573 | 0,625 |
| `agents composite` | **0,642** | 0,638 | **0,695** |
| *`B0 mode`, temoin* | *moins 0,005* | *moins 0,005* | *moins 0,005* |
| *`B0 tirage`, temoin* | *moins 0,006* | *moins 0,008* | *moins 0,008* |
| humains vague 2 | 1,000 | 1,000 | 1,000 |

**Trois consequences.**

1. **Le classement survit, le chiffre non.** Le « 7 pour cent du plancher humain » devient
   **7 pour cent sous la segmentation qui contient l'ideologie et 18 a 27 pour cent sous
   celle qui ne la contient pas**, contre **64 a 70 pour cent pour `agents composite` dans
   les deux**. Le rapport entre les deux camps de conditions passe de 9 pour 1 a 2,6 pour 1.
2. **Ce n'est pas un effet de finesse.** `S_fin` a 42 cellules et donne 0,055 pour `v8` ;
   genre x race x age a 38 cellules et donne 0,267. A granularite comparable, le facteur 5
   vient de la presence de l'ideologie dans le segment.
3. **Le seuil de verdict de la section 7.2 ne resiste pas.** Sous genre x race x age, `v8`
   (0,267), C2 (0,185), `B1` (0,228) et `B3 foret` (0,187) sortent tous de la classe
   « gabarit » a moins de 15 pour cent. Le tableau des verdicts change de contenu selon un
   choix que le rapport ne discute pas.

**Ce qu'il faut ecrire.** Publier les trois segmentations, faire du segment sans ideologie la
lecture principale et de `S_ideo` une lecture secondaire, et **retirer la formule « des
gabarits de groupe a 93 pour cent interchangeables »**, qui est le complement a 1 du seul
chiffre `S_ideo`.

### E3. Section 9.2 : a38 manque au tableau des quantites de gabarit. Objection a45 numero 3, contradiction D2.

**Phrase d'origine.** Le tableau de la section 9.2 recense six chemins et conclut : « **Deux
des six chemins sont des quantites de gabarit, deux ne le sont pas, deux ne sont pas
testes.** »

**Correction.** Le facteur d'amplification de l'ecart entre camps de a38, ecrit sept minutes
avant le preenregistrement de a44 et promu pilier de la these par `MODELE-DU-MONDE.md` 10.4,
ne figure pas dans le tableau. C'est une fonctionnelle de la seule table de contingence
(camp, modalite) : **invariant a zero pres sous permutation des personnes a l'interieur de
leur camp**, sur les 27 lignes mesurees [MESURE, `a47-a38-invariance-facteur.csv`], et
reproduit a 100,0 pour cent par le generateur nul de a44 [a45 section 2.1, 30 replicats]. La
pente de consensus de a37 releve du meme raisonnement, comme l'unanimite de a30 que le
tableau reconnait deja.

Le tableau doit gagner trois lignes, « le facteur d'amplification de l'ecart entre camps
(a38) : **oui, 100,0 pour cent** », « la pente droite sur gauche par item (a37) : **oui par
construction, non teste** », et la conclusion devient : **sur les quantites citees comme
piliers, une seule, la chute sous permutation, n'est pas reproduite par un generateur sans
structure individuelle**.

### E4. Section 5.2 lecture 5 : le rapport de reassignation n'a pas de plancher, et son plancher est dans le fichier. Objection a45 numero 6.

**Phrase d'origine.** « Chez v8 il vaut **4,91**, chez C2 **3,09** [...] **une reassignation
arbitraire des reponses a l'interieur du segment fait trois a cinq fois mieux que la
vraie.** [...] Chez les humains la reassignation optimale ne gagne rien, rapport 1,000 et
1,001 [...] **C'est le controle qui leve la reserve ecrite au preenregistrement.** »

**Correction.** Ce controle ne borne rien. Le rapport publie vaut `(hongrois moins permutee)
/ (vraie moins permutee)` : il explose mecaniquement quand le denominateur tend vers zero,
et le sur ajustement de l'appariement hongrois se lit sur le **gain absolu**, pas sur le
rapport. Le plancher correct est le gain absolu d'une population sans aucun signal
individuel, et il est dans le fichier de a44 : `B0 tirage`, que la colonne du rapport range
en « sans objet », est precisement la ligne qui calibre le terme.

**Preuve.** [MESURE, `a47-plancher-reassignation.csv`, segmentation `S_ideo`, valeurs
identiques a celles de `a44-permutation.csv`]

| condition | gain hongrois absolu | chute vraie | rapport publie |
|---|---|---|---|
| *`B0 tirage`, aucun signal individuel, 1 052 personnes* | **0,0820** | moins 0,0011 | *non defini* |
| `agents v8`, 1 052 personnes | **0,0687** | 0,0139 | 4,91 |
| `B3 foret` | 0,0787 | 0,0285 | 2,76 |
| `agents v7` | 0,0915 | 0,0306 | 2,99 |
| `B1 argmax` | 0,1013 | 0,0378 | 2,68 |
| `agents composite` | 0,1540 | 0,1525 | 1,01 |
| humains vague 2 | 0,2765 | 0,2761 | 1,001 |

Le gain hongrois de `v8`, 0,0687, est **inferieur** a celui d'une population sans aucune
structure individuelle, 0,0820, mesure sur le meme perimetre de 1 052 personnes. Le 4,91 ne
mesure donc pas que la vraie assignation est arbitraire chez `v8` : il mesure que 0,0139 est
un petit denominateur.

**Reserve de perimetre, a ecrire avec.** Le 3,09 de C2 porte sur 150 personnes, ou le gain
hongrois vaut 0,0393 ; `B0 tirage` n'existe qu'a 1 052 personnes et le plancher a 150
personnes n'a pas ete construit. La comparaison directe n'est etablie que pour `v8`.

**Ce qu'il faut ecrire.** « Chez `v8` le gain de l'appariement optimal, 0,069, est au niveau
du gain obtenu sur une population sans structure, 0,082 », et publier le gain absolu a cote
du rapport dans tout tableau.

### E5. Section 5.2 : la chute sous permutation est correlee a 0,91 avec l'exactitude brute. Objection a45 numero 1.3.

**Correction.** Sur les treize conditions du perimetre 1 052, humains vague 1 exclus, la
correlation de Pearson entre l'exactitude vraie et la chute absolue vaut **0,906**, celle de
Spearman **0,874**, soit **82 pour cent de variance partagee** [MESURE,
`a47-correlation-chute-exactitude.csv`, segmentation `S_ideo` ; 0,894 sous `S_fin`, 0,906
sous genre x race x age]. C'est arithmetiquement attendu, la chute etant une composante
additive de l'exactitude, mais cela oblige a nuancer la phrase que le dossier repete depuis
a1, « l'exactitude ne voit pas la distorsion ». La quantite qui la voit partage 82 pour cent
de sa variance avec elle.

**Ce qu'il faut ecrire.** « La chute sous permutation et l'exactitude brute sont correlees a
0,91 sur nos treize conditions ; ce qui separe n'est pas leur classement mais les conditions
ou elles divergent, `B0 mode` a 0,593 d'exactitude et 0,000 de chute, `B3 foret` a 0,634 et
0,029, `B1` a 0,621 et 0,038. »

### E6. Section 7.2 : la ligne `agents v6` est en partie une recopie de demographies. Objection a45 numero 1.5, heritee de a17 objection 2.2.

**Phrase d'origine.** « | `agents v6` | 0,235 | 1,91 | intermediaire | ».

**Correction.** Un balayage complet des 149 items par condition remonte **seize items
recopies a 0,95 ou plus par au moins une condition**. Quatre le sont par `v6` seul et sont
des faits d'etat civil, `income` 0,994, `othlang` 1,000, `divorced` 0,997, `posslq/y` 0,995 ;
les autres sont des items quasi degeneres que toutes les conditions reussissent (`uscitzn*`,
`compuse*`, `usewww*`, `webmob`, `fucitzn`, `mnthsusa`, `evwork`) ou des items ou seul le
retest humain depasse le seuil.

En retirant les seize, sur les 133 items restants, la chute sous permutation de `v6` passe de
**0,235 a 0,181** du plancher humain, soit **un quart de son signal individuel apparent**,
tandis que `v8` (0,072 a 0,072), C2 (0,072 a 0,072) et `composite` (0,643 a 0,638) ne
bougent pas [MESURE, `a47-chute-hors-items-recopies.csv` et `a47-items-recopies.csv`,
produits par `analyses/a47_income_v6.py`, segmentation `S_ideo`, 200 permutations].

**Ce qu'il faut ecrire.** Publier la ligne `v6` avec et sans les items d'etat civil qu'elle
recopie, ou adopter la liste de retrait que a17 reclamait deja et que a19 avait chiffree sur
l'exactitude.

### E7. Section 1 point 6 et section 5.2 : le repli de `S_fin` sur le perimetre 150 ne touche pas la permutation. Contradiction D11.

**Phrase d'origine.** Section 9.2 point 4 : « Son effet est enorme sur le perimetre 150 sous
`S_fin`, 64,3 pour cent des couples, et **il rend cette cellule du plan inutilisable**. »

**Correction.** Cette reserve porte sur le **generateur nul**, qui a besoin des lois par
segment et se replie sur la marginale d'item quand un segment compte moins de cinq
repondants observes. **La permutation intra segment n'emploie pas le nul** : elle ne demande
que l'appartenance de chaque personne a une cellule. Les lignes `S_fin` de C2 et de C3 dans
`a44-permutation.csv` sont donc valides, et le rapport ne le precise pas, ce qui laisse
croire a une incoherence. Aucun chiffre ne change ; c'est une precision de lecture.

---

Rapport du 8 septembre 2026, soiree. Il execute le test 4.2 de
`corpus/lecture-complete/08-veille-ete-2026.md`, « le generateur nul conditionnellement
independant, comme baseline », propose par la lecture de Yuan, « Cultural Bias Without a
Cultural Self », arXiv 2607.02368 v3, declaree menace la plus grave du lot.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Trois scripts
nouveaux, `analyses/a44_commun.py`, `a44_mesures.py`, `a44_structure.py`, plus
`a44_figure.py`. **Aucun script existant n'a ete modifie** ; `a1_double_distorsion`,
`a2_commun`, `a2_baselines_gss`, `a5_evaluer`, `a5_agents_locaux_gss`, `a8_commun`,
`a25_commun`, `a25_mesures`, `a28_commun`, `a29_commun`, `a31_commun` et `a35_commun` sont
importes tels quels, memes graines, memes plis, memes 149 items, memes personnes. Les
matrices de prediction sont relues des caches de a25, a28 et a35 ; `PMM k=10` vient du
cache de a35 et n'est pas recalcule.

**Le preenregistrement est `resultats/a44-preenregistrement.md`, ecrit le 8 septembre 2026
a 15 h 46 CEST (13 h 46 UTC), depot a `d536169dc5361c38edcd723d48816e2ddd06dc4f`, avant
l'ecriture du premier script et avant tout calcul.** Les sept quantites, les deux
segmentations, la famille de tests, le nombre de replicats, la quantite primaire du verdict
et six predictions y sont figes.

Sorties : `a44-controles.csv`, `a44-replis-segments.csv`, `a44-quantites.csv`,
`a44-verdicts.csv`, `a44-permutation.csv`, `a44-rarete.csv`,
`a44-structure-par-finesse.csv`, `a44-figure-generateur-nul.png` et `.svg`.

---

## Reponse en une ligne

**Le gonflement inter et l'ecrasement intra, les deux chiffres qui portent le dossier, sont
reproduits par un generateur qui n'a aucune structure individuelle : sur l'axe ideologie,
`agents v8` mesure 8,130 et son generateur nul 8,175, soit 100,6 pour cent reproduits, C2
6,894 contre 7,209, soit 104,6 pour cent, et le terme intra est reproduit a 99,3 pour cent
pour les onze conditions du perimetre 1 052, 0,4425 contre 0,4398 pour v8**
[MESURE, `a44-quantites.csv`, 200 replicats, IC bootstrap sur 1 000 tirages de personnes
contenant zero pour v8, `p = 0,736`, et pour C2, `p = 0,244`]. **Ce n'est pas une surprise
empirique, c'est un fait arithmetique que le script verifie : les deux termes de a1 ne
dependent que de la table de contingence segment par modalite, donc ils sont exactement
invariants sous permutation des personnes a l'interieur d'un segment, ecart mesure
`0,000e+00` sur seize conditions et deux segmentations.** Le critere de Yuan s'applique
mot pour mot : « any pattern reproducible from item means and variances alone does not
license trait talk. »

**Ce que le generateur nul ne reproduit pas va dans la direction inverse de celle
attendue** : nos populations simulees ont **moins** de patrons de reponses distincts que
leur propre nul, moins 22 a moins 47 pour cent pour les conditions a modele de langage
contre moins 7 pour cent chez les humains, et **plus** de correlation entre items a
l'interieur du segment, deux fois l'exces humain, 0,084 a 0,105 contre 0,042
[MESURE]. L'agent n'est donc pas un gabarit de groupe au sens strict : il est **plus pauvre
qu'un tirage sans structure dans son propre gabarit**, et ses items sont couples deux fois
plus fort que chez de vraies personnes.

**Et la question de savoir si cette structure est celle de la personne est tranchee par la
transposition de la perturbation de cadre.** Permuter les personnes a l'interieur de leur
segment ideologique fait chuter l'exactitude de 34,7 pour cent chez les memes humains
reinterroges, de 22,3 pour cent pour `agents composite`, de 20,7 pour PMM, de 15,0 pour C3,
et de **2,5 pour cent pour `agents v8` et 2,4 pour cent pour C2**, quand les deux temoins
aveugles a la personne, `B0 mode` et `B0 tirage`, sont a moins 0,2 pour cent, c'est a dire
zero [MESURE, `a44-permutation.csv`, 200 permutations]. **Les conditions a etiquette seule
sont a un vingtieme du plancher humain et a deux points d'un generateur qui ignore
totalement qui est la personne.** Le troisieme terme le confirme dans l'autre sens : la
reassignation optimale des personnes a l'interieur du segment ne gagne rien sur les humains,
rapport 1,001, ni sur `agents composite`, 1,010, mais elle gagne **4,9 fois la chute** sur
v8 et 3,1 fois sur C2 : chez eux la vraie assignation des reponses aux personnes n'est pas
la meilleure, elle est arbitraire.

**Verdict.** Le verdict preenregistre, fonde sur la seule correlation residualisee Q5,
classe les treize conditions « porteur de personne » sans exception, `p` de Holm 0,0130
partout : **le critere primaire declare ne separe rien et il faut l'ecrire**. Le seul test
qui separe est la permutation intra segment, ajoutee au preenregistrement comme
remplacement de la perturbation d'ordre et non comme quantite de verdict. Elle est
desormais la mesure a defendre.

---

## 0. Le preenregistrement, et les trois ecarts

Le preenregistrement fixe `R = 200` replicats nuls, `B = 1 000` tirages bootstrap sur les
personnes, `P = 200` permutations, graine `20260908`, seuil de repli de segment a cinq
repondants, deux segmentations `S_fin` et `S_ideo`, treize conditions dans la famille
primaire, Q5 comme quantite du verdict, Holm sur treize tests. **Tout cela a ete execute tel
quel.** Trois ecarts, tous declares ici :

| | ecart | pourquoi |
|---|---|---|
| **E1** | **Deux conditions ajoutees** : les humains des deux vagues restreints aux 150 personnes du run local, `humains vague 1 (150)` et `humains vague 2 (150)`. Elles sont descriptives et n'entrent dans aucune famille. | Sans elles, C2 et C3 n'avaient aucune reference sur leur propre perimetre. Le plancher de bruit de Q4, Q5 et Q3 depend de l'effectif : comparer C2 a la ligne humaine des 1 052 aurait ete faux. Ajoutees avant toute lecture de resultat, apres avoir vu que le tableau manquait sa ligne de reference. |
| **E2** | **Q6 et Q7 sont estimes sur 50 replicats et non 200**, et sans bootstrap sur les personnes. | Cout : ils demandent de repasser chaque replicat en matrice de chaines et de recalculer les masques de a29. Le preenregistrement les classait deja comme secondaires ; l'ecart type inter replicat publie permet de juger de la precision. |
| **E3** | **Un complement descriptif non prevu**, `a44_structure.py`, qui fait varier la finesse du conditionnement sur cinq niveaux. Signale post hoc partout. | Ajoute apres avoir lu que Q5 ne separait rien : il fallait savoir si l'exces de correlation venait d'une demographie plus fine que le segment, ce qui serait encore du gabarit de groupe. |

Une seule mesure du preenregistrement n'a pas de sens tel qu'ecrit et n'est pas publiee
comme test : **le bootstrap sur les personnes de Q3**. Un tirage avec remise duplique des
personnes et fait baisser mecaniquement le nombre de patrons distincts. Q3 est publie avec
la bande de ses replicats nuls seulement.

**Le score des six predictions ecrites avant le calcul** [MESURE] :

| | prediction | issue |
|---|---|---|
| **P1** | C2 et v8 indistinguables de leur nul sur Q1 et Q2 | **tenue.** v8 `d = -0,045`, IC [-0,255 ; 0,159], `p = 0,736` ; C2 `d = -0,315`, IC [-0,448 ; 0,126], `p = 0,244` ; Q2 `p = 0,668` et `p = 0,146` |
| **P2** | les conditions riches s'ecartent du nul sur Q5 par le haut | **tenue mais sans valeur** : les treize s'en ecartent, y compris les humains et les predicteurs statistiques |
| **P3** | C2 ne s'ecarte pas du nul sur Q5, C3 si | **fausse.** Les deux s'en ecartent, C2 `d = 0,047` IC [0,029 ; 0,052], C3 `d = 0,055` IC [0,038 ; 0,059] |
| **P4** | les humains s'ecartent tres largement du nul sur Q5 | **tenue**, `z = 230` et `289` |
| **P5** | chute d'exactitude proche de zero pour C2 et v8, nettement positive pour les humains et les conditions riches | **tenue, et c'est le resultat du rapport** |
| **P6** | Q3 plus grand dans le nul que dans la population simulee | **tenue pour les seize conditions sans exception**, y compris les humains |

---

## 1. Les controles, executes avant toute lecture

[MESURE, `a44-controles.csv`, vingt deux lignes]

1. **Part de cellules renseignees mais hors nomenclature** : 0,00 pour cent chez les humains
   des deux vagues, chez C2, C3, B1, B2, PMM et les trois predicteurs ; au pire 0,118 pour
   cent pour `agents entretien (v3)`. Meme ordre de grandeur qu'en a1. Seuil declare
   0,5 pour cent, passe partout.
2. **L'exactitude calculee sur codes entiers egale celle de `a2_commun` sur les chaines**,
   ecart maximal sur les seize conditions **`0,000000000`**. Le codage n'a rien casse.
3. **Controle bloquant 1, les marginales.** Le generateur nul redonne les marginales par
   item ET par segment de la condition qui le parametre : ecart moyen **0,003863** sur les
   couples non replies, 100 replicats, seuil declare 0,01. L'effet du repli sur la marginale
   d'item, publie a cote comme description et non comme controle, vaut 0,00198 en moyenne.
4. **Controle bloquant 2, l'invariance.** Le ratio inter est **exactement** invariant sous
   permutation des personnes a l'interieur du segment : ecart maximal sur seize conditions
   et deux segmentations, **`0,000e+00`**, seuil declare `1e-12`. Ce n'est pas une
   approximation ; c'est la lecture arithmetique de la section 3.
5. **Concordance avec les rapports anterieurs.** Sans y avoir touche, a44 retrouve a1 et
   a31 :

| quantite | a44 | rapport anterieur | ecart |
|---|---|---|---|
| ratio inter Gini Simpson, axe ideologie, `agents v8` | 8,130 | 8,249 (`a1-ratios-par-axe.csv`) | 1,4 pour cent |
| idem, `agents composite` | 2,156 | 2,115 | 1,9 pour cent |
| idem, `humains vague 2` | 1,019 | 1,015 | 0,4 pour cent |
| lift de rarete de personne, `agents composite` | 0,2116 | +0,21 (a31, 2.3) | au chiffre |
| lift de rarete de segment, `agents composite` | 0,3433 | +0,34 | au chiffre |
| rapport groupe sur personne, `agents v8` | 7,369 | 7,37 | au chiffre |
| idem, `B3 foret` | 8,179 | 8,18 | au chiffre |
| idem, `humains vague 2` | 0,561 | 0,56 | au chiffre |
| idem, C2 et C3 | 4,446 et 0,436 | 4,45 et 0,44 | au chiffre |
| rappel des rares, `agents composite` | 0,3069 | 0,307 (a29) | au chiffre |

Les ecarts de 1 a 2 pour cent sur les ratios de a1 s'expliquent : a1 travaille sur 169
items et soustrait le residu de permutation, a44 travaille sur les 149 items de a2, a25 et
a28 et ne soustrait rien. **a44 emploie l'indice de Gini Simpson et non l'entropie**, parce
que la version vectorisee de a35 n'implemente que celui la ; a1 section 3 montre que les
deux mesures donnent le meme classement et le meme signe, et le tableau ci dessus le
verifie. Le 8,16 de C2 publie en a23 est une valeur d'entropie sur 150 personnes avec
correction residuelle ; l'equivalent Gini Simpson de a44 vaut 6,894. **Ce n'est pas le meme
nombre et il ne faut pas les confondre.**

6. **Taux de repli du generateur nul** [MESURE, `a44-replis-segments.csv`]. Sous `S_ideo`,
   sept segments, **0,0 pour cent de repli partout**. Sous `S_fin`, 42 segments,
   **7,1 pour cent sur le perimetre 1 052 et 64,3 pour cent sur le perimetre 150**. C'est la
   limite majeure du dispositif : **sur les 150 personnes du run local, la segmentation fine
   vide le nul de son conditionnement**, et toute lecture de C2 et C3 sous `S_fin` est
   biaisee vers « la population s'ecarte du nul » pour une raison purement mecanique. **Les
   resultats de C2 et C3 sont lus sous `S_ideo`, ou le repli est nul.**

---

## 2. Protocole : la methode de Yuan, reproduite, et les ecarts

### 2.1 Ce que Yuan fait, lu dans le texte integral

Le papier a ete telecharge et lu en entier, arXiv 2607.02368 v3, `stat.ML`, 30 aout 2026,
rendu PDF du 1er septembre 2026, auteur Yuan Yuan, Auburn University. Tout ce qui suit dans
cette section est lu dans son texte et verifie ligne par ligne contre le rendu PDF
[CONFIRME].

**Sa construction, section 2.** Les 50 reponses d'une passation IPIP-50 sont rangees dans
une matrice item par dimension 10 x 5, une colonne par dimension du Big Five, les reponses
empilees dans l'ordre de presentation. La matrice de correlation de Spearman entre colonnes,
5 x 5, est symetrique definie positive ; elle est traitee comme un point sur la variete des
matrices SPD, envoyee dans l'espace tangent par le logarithme matriciel, et ses dix entrees
hors diagonale servent d'attributs. Trois cadres de mesure : `FO`, toutes les instances
partagent l'ordre standard ; `RO`, chaque instance recoit sa propre permutation uniforme
des 50 items ; `RO-BTSP`, une permutation partagee est tiree au hasard et toutes les
instances `RO` sont relues sous ce cadre commun, moyenne sur 2 000 tirages. La sortie est
un taux de separation des deux personas par regroupement, hasard a 50 pour cent.

**Ses resultats, sections 3 a 5.** Chez l'humain la geometrie tient : `r = 0,77` entre deux
sessions ne partageant ni items, ni ordre, ni contexte, `N = 89` ; identification
d'individus jusqu'a 75,9 pour cent contre 0,38 de hasard sur NEO-PI-R, `N = 263` ; les dix
variables de l'espace tangent predisent la moyenne generale universitaire, `R^2 = 0,281`,
`p` de permutation 0,003, la ou les agregats Big Five tires des **memes** reponses donnent
`R^2 = 0,018`, `p = 0,91`. Chez les quatre modeles, rien : GPT-4o passe de 94,63 pour cent
sous `FO` a 55,23 sous `RO`, et remonte a 83,69 sous `RO-BTSP`.

**Son generateur nul, section 5, equation (2)** :

```
X_ij ~ N(mu_chapeau_{j,g}, sigma_chapeau_{j,g}),  tronque, arrondi sur {1, ..., 5}
```

sans trait latent, sans covariance entre items, sans dependance autoregressive ; les
parametres sont estimes sur les statistiques d'item empiriques du modele evalue, groupe par
groupe ; le faux jeu passe dans **la chaine de mesure identique** ; 100 participants
synthetiques, 50 iterations. Resultat, sa table 6 : **97,2 / 57,6 / 83,2** pour le nul
parametre sur GPT-4o contre **94,6 / 55,2 / 83,7** pour le vrai GPT-4o, et 86,0 / 58,2 /
82,9 pour le nul DeepSeek contre 94,7 / 56,4 / 81,8. Les simulations parametrees sur des
normes humaines ne produisent aucun ecart `FO` contre `RO`, 58,2 contre 58,2 : c'est son
controle negatif.

**Sa recommandation, section 6, citee** : « conditionally independent item-level simulation
provides a reusable null for claims about LLM traits, attitudes, or biases: any pattern
reproducible from item means and variances alone does not license trait talk. »

### 2.2 Ce que a44 reproduit exactement

1. **Le generateur.** Meme principe, transpose au categoriel parce que nos reponses ne sont
   pas sur une echelle a cinq points comparable d'un item a l'autre : 149 items du GSS,
   nomenclatures fermees de tailles differentes, une partie nominale. La loi normale
   tronquee est remplacee par la loi multinomiale empirique de l'item a l'interieur du
   segment, `X_ij ~ Multinomiale(p_chapeau_{j, g(i)})`, tirages independants sur `i` et sur
   `j`. Aucune structure latente, aucune covariance entre items, aucune dependance entre
   cellules. C'est la version categorielle exacte de son equation (2).
2. **Les parametres viennent de la population evaluee elle meme**, jamais des humains,
   exactement comme les siens viennent du modele evalue. Le nul de C2 est construit sur les
   marginales de C2.
3. **Le masque est conserve** : une cellule vide ou refusee dans la condition reste vide
   dans son nul. Le nombre de cellules exploitables par item et par personne est identique,
   ce qui interdit qu'un ecart vienne d'un effectif different.
4. **La chaine de mesure est identique** entre la population et son nul : les memes
   fonctions, importees de a1, a29, a31 et a35, sans une ligne modifiee.
5. **Le controle negatif.** Chez lui, un nul parametre sur des normes humaines ne produit
   aucun ecart. Chez nous, `B0 tirage`, qui tire dans la marginale de l'item sans aucun
   segment, est une population reellement sans structure. Sa distance a son propre
   generateur nul est **nulle sur toutes les quantites** : Q4 `d = 0,0000`, `p = 0,994` ;
   Q5 `d = 0,0000`, `p = 0,970` ; Q3 `d = -0,29` patron sur 794, soit 0,04 pour cent ; Q7
   `d = -0,0018` ; chute sous permutation `-0,22` pour cent [MESURE]. **Le dispositif ne
   fabrique pas de distance la ou il n'y en a pas.** C'est le controle qui autorise a lire
   toutes les autres lignes.

### 2.3 Les ecarts a sa methode, tous declares

| | ce qu'il fait | ce que a44 fait | pourquoi |
|---|---|---|---|
| **la perturbation d'ordre** | chaque instance recoit sa propre permutation des 50 items | **rien** ; remplacee par la permutation des personnes a l'interieur du segment | reconstruire une trace a ordre aleatoire depuis une trace a ordre fixe est impossible ; il faudrait 22 350 appels de modele par condition, ce que a44 n'a pas le droit de faire |
| **la matrice intra instance** | correlation entre dimensions a l'interieur d'UNE passation, point sur la variete SPD | correlation entre items sur la population, apres retrait du segment | il n'y a qu'une passation par personne dans le GSS et aucune structure item par dimension ; la matrice intra instance n'existe pas chez nous |
| **le plancher humain** | trois natures : fidelite test retest, identifiabilite, validite de critere | une seule : la vague 2, les memes personnes reinterrogees deux semaines plus tard | ni identifiabilite individuelle ni critere externe dans le paquet OSF |
| **le materiau** | IPIP-50, deux personas culturelles, quatre modeles de frontiere | 149 items d'attitudes du GSS, six conditions de Stanford, deux conditions locales, cinq predicteurs statistiques | c'est notre plan, et c'est ce que sa limite « open to test » designe |
| **la sortie** | taux de separation de deux personas par regroupement | sept quantites du dossier, dont les deux ratios de a1 | c'est notre chaine de mesure qu'il s'agit de mettre a l'epreuve |
| **le nombre de replicats** | 50 iterations, `N = 100` synthetiques | 200 replicats, `N = 1 052` ou `N = 150` | plus de replicats, meme principe |

---

## 3. Le gonflement et l'ecrasement sont reproduits par le generateur nul

### 3.1 Le fait arithmetique, a lire avant les chiffres

Les deux termes de a1 ne dependent, item par item, que de la **table de contingence
(segment, modalite)**. `a28_commun.dispersion_item` ne recoit que le vecteur de reponses et
le vecteur de segments, et il en construit `c[g, k]`. Toute quantite calculee sur cette
table est donc **exactement invariante sous n'importe quel reetiquetage des personnes a
l'interieur d'un segment**. Le script le verifie plutot que de le supposer, et l'ecart
mesure est `0,000e+00` sur seize conditions et deux segmentations.

**Consequence, ecrite telle quelle : le ratio inter de a1 ne peut pas, par construction,
distinguer une population de personnes d'une population de tirages independants dans le
gabarit de leur segment.** Un generateur qui respecte la table de contingence reproduit la
mesure. C'est exactement la these de Yuan, appliquee a notre mesure principale, et elle
n'avait pas besoin d'etre mesuree pour etre vraie. Ce qui restait a mesurer, et qui suit,
est de combien le tirage s'ecarte en pratique.

### 3.2 Tableau 1 : le ratio inter sur l'axe ideologie, nul construit sur le meme axe

Gini Simpson sans biais, 149 items, 200 replicats, IC bootstrap sur 1 000 tirages de
personnes, le meme tirage applique a la population et a son nul [MESURE,
`a44-quantites.csv`, quantite `Q1b`, segmentation `S_ideo`].

| condition | mesure | son nul | bande du nul | part reproduite | `d` | IC de `d` | `p` |
|---|---|---|---|---|---|---|---|
| humains vague 1 | 1,000 | 1,110 | [1,068 ; 1,145] | 111,0 % | -0,110 | [-0,216 ; 0,001] | 0,058 |
| humains vague 2 | 1,019 | 1,128 | [1,087 ; 1,169] | 110,7 % | -0,109 | [-0,214 ; 0,009] | 0,088 |
| agents composite | 2,156 | 2,245 | [2,208 ; 2,290] | 104,1 % | -0,088 | [-0,277 ; 0,088] | 0,374 |
| agents entretien (v3) | 2,826 | 2,905 | [2,853 ; 2,961] | 102,8 % | -0,079 | [-0,317 ; 0,121] | 0,516 |
| agents enquete | 2,518 | 2,602 | [2,554 ; 2,653] | 103,3 % | -0,084 | [-0,269 ; 0,084] | 0,396 |
| agents v7 | 0,163 | 0,236 | [0,222 ; 0,254] | 144,7 % | -0,073 | [-0,129 ; 0,002] | 0,064 |
| agents v6 | 0,312 | 0,384 | [0,363 ; 0,409] | 123,2 % | -0,072 | [-0,154 ; 0,033] | 0,170 |
| **agents v8** | **8,130** | **8,175** | **[8,122 ; 8,230]** | **100,6 %** | **-0,045** | **[-0,255 ; 0,159]** | **0,736** |
| B1 argmax | 2,673 | 2,743 | [2,698 ; 2,794] | 102,6 % | -0,070 | [-0,180 ; 0,041] | 0,240 |
| B2 argmax | 1,830 | 1,887 | [1,836 ; 1,929] | 103,1 % | -0,057 | [-0,239 ; 0,125] | 0,584 |
| PMM k=10 | 1,354 | 1,458 | [1,419 ; 1,502] | 107,7 % | -0,104 | [-0,229 ; 0,031] | 0,166 |
| B3 foret | 2,781 | 2,823 | [2,774 ; 2,866] | 101,5 % | -0,041 | [-0,159 ; 0,068] | 0,520 |
| *B0 tirage, temoin* | *-0,009* | *0,106* | *[0,091 ; 0,120]* | *sans objet* | *-0,115* | *[-0,133 ; -0,076]* | *0,001* |
| humains vague 1 (150) | 1,000 | 1,839 | [1,703 ; 1,989] | 183,9 % | -0,839 | [-0,716 ; -0,190] | 0,001 |
| humains vague 2 (150) | 0,999 | 1,830 | [1,702 ; 1,959] | 183,3 % | -0,832 | [-0,681 ; -0,199] | 0,001 |
| C3 | 0,724 | 1,310 | [1,206 ; 1,429] | 180,8 % | -0,585 | [-0,563 ; -0,088] | 0,001 |
| **C2** | **6,894** | **7,209** | **[7,045 ; 7,349]** | **104,6 %** | **-0,315** | **[-0,448 ; 0,126]** | **0,244** |

**Trois lectures, dans l'ordre.**

1. **Le nul reproduit le gonflement de toutes les conditions**, de 100,6 pour cent pour v8 a
   111,0 pour cent pour les humains, et il le sur-reproduit systematiquement. **Aucune des
   onze conditions du perimetre 1 052 n'a un intervalle de `d` excluant zero**, sauf le
   temoin `B0 tirage`, dont le ratio vrai est nul par construction et pour qui la
   sur-reproduction est donc tout le signal.
2. **Le `d` est un montant additif a peu pres constant**, moins 0,041 a moins 0,115 sur le
   perimetre 1 052 quelle que soit la taille du ratio. C'est un plancher de bruit :
   `p_chapeau` est estime sur le segment puis retire dans le meme segment, ce qui ajoute une
   couche de bruit multinomial, et le terme inter, qui est une variance entre segments, la
   compte. **Cela explique pourquoi la « part reproduite » est de 111 pour cent chez les
   humains et de 100,6 pour cent chez v8 : le meme montant absolu de bruit represente
   11 pour cent d'un ratio de 1 et 0,6 pour cent d'un ratio de 8.** Il ne faut donc pas lire
   la part reproduite comme un classement de proximite.
3. **Sur le perimetre 150 le plancher est quatre fois plus haut**, moins 0,58 a moins 0,84,
   parce que sept segments de 21 personnes donnent des `p_chapeau` beaucoup plus bruites.
   C2, dont le ratio vaut 6,9, est au dessus de ce plancher et son intervalle contient zero ;
   les humains a 150 et C3, dont les ratios valent 1,0 et 0,7, sont sous le plancher et leur
   intervalle l'exclut. **Le plancher explique entierement ces trois lignes ; elles ne disent
   rien de plus.**

**Un defaut de l'intervalle, a porter avec le tableau.** L'intervalle bootstrap de `d` n'est
pas centre sur l'estimation ponctuelle de `d`. Le tirage avec remise duplique des personnes,
ce qui change l'effectif effectif et donc les estimateurs a biais corrige, differemment pour
la population et pour son nul. Sur le perimetre 1 052 l'ecart est petit et les onze
intervalles du tableau 1 contiennent leur estimation ponctuelle ; sur le perimetre 150 il ne
l'est pas, `d = -0,839` pour les humains a 150 contre un intervalle [-0,716 ; -0,190].
**Aucune conclusion du rapport ne repose sur une ligne du perimetre 150 dont le `p` serait
proche de 0,05**, et la seule ligne de ce perimetre qui porte une conclusion, C2 avec
`p = 0,244`, est loin du seuil dans les deux lectures. Le defaut est signale en section 11.

### 3.3 Tableau 2 : le ratio intra

[MESURE, `a44-quantites.csv`, quantite `Q2`, `S_ideo`]

| condition | mesure | son nul | part reproduite | `d` | IC de `d` | `p` |
|---|---|---|---|---|---|---|
| humains vague 1 | 1,0000 | 0,9933 | 99,33 % | 0,0067 | [-0,003 ; 0,016] | 0,196 |
| humains vague 2 | 1,0025 | 0,9960 | 99,35 % | 0,0065 | [-0,004 ; 0,017] | 0,204 |
| agents composite | 0,8432 | 0,8376 | 99,33 % | 0,0057 | [-0,006 ; 0,019] | 0,382 |
| agents entretien (v3) | 0,7641 | 0,7592 | 99,36 % | 0,0049 | [-0,008 ; 0,018] | 0,478 |
| agents enquete | 0,7922 | 0,7871 | 99,35 % | 0,0052 | [-0,007 ; 0,016] | 0,426 |
| agents v7 | 0,6476 | 0,6431 | 99,31 % | 0,0045 | [-0,011 ; 0,020] | 0,542 |
| agents v6 | 0,6519 | 0,6473 | 99,30 % | 0,0046 | [-0,007 ; 0,016] | 0,434 |
| **agents v8** | **0,4425** | **0,4398** | **99,39 %** | **0,0027** | **[-0,010 ; 0,015]** | **0,668** |
| B1 argmax | 0,6380 | 0,6336 | 99,31 % | 0,0044 | [-0,007 ; 0,015] | 0,422 |
| B2 argmax | 0,5379 | 0,5343 | 99,34 % | 0,0035 | [-0,007 ; 0,015] | 0,522 |
| PMM k=10 | 0,9548 | 0,9483 | 99,32 % | 0,0065 | [-0,004 ; 0,017] | 0,216 |
| **C2** | **0,3646** | **0,3475** | **95,29 %** | **0,0172** | **[-0,006 ; 0,039]** | **0,146** |
| C3 | 0,6808 | 0,6486 | 95,28 % | 0,0321 | [-0,001 ; 0,064] | 0,054 |
| humains vague 2 (150) | 0,9988 | 0,9520 | 95,31 % | 0,0468 | [0,016 ; 0,075] | 0,008 |

**La part reproduite est de 99,3 pour cent pour les onze conditions du perimetre 1 052 et de
95,3 pour cent pour les quatre du perimetre 150, sans exception et a la troisieme decimale
pres.** L'ecrasement intra n'est pas une propriete que le nul ratera jamais : c'est la
moyenne ponderee des dispersions de segment, et le nul les reproduit par construction. Les
onze intervalles de `d` du perimetre 1 052 contiennent zero. **Le 0,365 de C2 est reproduit
a 0,3475 par un generateur qui ne sait rien de la personne.**

### 3.4 La segmentation fine ne change pas la lecture

Sous `S_fin`, 42 cellules, le nul est construit sur ideologie x genre x age et le ratio
mesure sur le meme axe : la part reproduite monte a 102 pour cent pour v8, 116 a 122 pour
cent pour les conditions riches, 147 pour cent pour les humains, avec le meme montant
additif de bruit, plus gros parce que les cellules sont plus petites. **Une seule ligne
sort : C2 sous `S_fin`, `d = +1,24`, IC [0,024 ; 0,364], `p = 0,028`. Elle est un artefact
de la regle de repli** : 64,3 pour cent des couples item x segment de C2 sous `S_fin` sont
replies sur la marginale d'item, donc le nul de C2 y est presque non conditionne, et il
sous-estime le gonflement pour une raison purement mecanique. **Cette ligne ne doit pas etre
citee.**

Quand le nul est construit sur `S_fin` mais le ratio mesure sur l'axe ideologie, la part
reproduite tombe a 79 a 89 pour cent, pour la meme raison : le repli attenue les contrastes
ideologiques des petites cellules. **Le tableau a lire est celui ou le nul et la mesure
partagent le meme axe, c'est a dire le tableau 1.**

---

## 4. Ce que le generateur nul ne reproduit pas, et dans quel sens

### 4.1 Tableau 3 : les patrons de reponses distincts

Nombre moyen de lignes distinctes sur vingt sous ensembles de dix items tires une fois,
graine fixe, partages par toutes les conditions et tous les replicats. Une ligne portant une
cellule vide est ecartee du comptage de son sous ensemble [MESURE, `a44-quantites.csv`,
`Q3`, `S_ideo` ; pas d'IC bootstrap sur les personnes, cf. section 0].

| condition | mesure | son nul | bande du nul | `d` | deficit relatif | `z` |
|---|---|---|---|---|---|---|
| humains vague 1 | 725,7 | 779,7 | [772,5 ; 786,0] | -54,0 | **-6,9 %** | -16,2 |
| humains vague 2 | 727,5 | 787,3 | [781,0 ; 794,7] | -59,8 | **-7,6 %** | -16,4 |
| agents composite | 469,4 | 573,5 | [566,7 ; 579,8] | -104,1 | **-18,2 %** | -27,5 |
| agents entretien (v3) | 394,9 | 495,6 | [488,6 ; 501,2] | -100,7 | **-20,3 %** | -30,3 |
| agents enquete | 416,5 | 504,5 | [496,8 ; 511,5] | -88,0 | **-17,4 %** | -23,1 |
| agents v7 | 230,1 | 288,7 | [283,4 ; 295,6] | -58,6 | **-20,3 %** | -19,7 |
| agents v6 | 217,6 | 282,5 | [277,4 ; 288,2] | -64,9 | **-23,0 %** | -22,6 |
| **agents v8** | **138,9** | **204,7** | **[200,6 ; 209,3]** | **-65,8** | **-32,1 %** | **-28,6** |
| B1 argmax | 311,5 | 356,4 | [349,8 ; 362,2] | -44,9 | -12,6 % | -13,3 |
| B2 argmax | 145,9 | 206,6 | [202,3 ; 210,8] | -60,8 | -29,4 % | -26,0 |
| PMM k=10 | 654,4 | 725,4 | [718,5 ; 733,1] | -71,0 | -9,8 % | -20,4 |
| *B0 tirage, temoin* | *794,3* | *794,6* | *[788,3 ; 802,0]* | *-0,3* | ***-0,04 %*** | *-0,09* |
| humains vague 2 (150) | 135,7 | 139,6 | [138,2 ; 141,1] | -3,9 | -2,8 % | -5,1 |
| C3 | 78,2 | 90,7 | [87,9 ; 93,4] | -12,5 | **-13,8 %** | -9,1 |
| **C2** | **39,5** | **47,1** | **[45,4 ; 48,9]** | **-7,6** | **-16,2 %** | **-8,4** |

**Toutes les seize conditions ont moins de patrons distincts que leur propre generateur nul,
sans exception, et le temoin `B0 tirage` est a moins 0,04 pour cent, c'est a dire zero.** Le
deficit vaut 7 a 8 pour cent chez les humains et 14 a 32 pour cent chez les conditions a
modele de langage. **Un agent est donc plus pauvre qu'un tirage sans aucune structure dans
son propre gabarit de groupe.** C'est une quantite nouvelle, elle n'est dans aucun rapport
anterieur, et elle est la seule du dossier qui place la simulation **en deca** du nul et non
au dessus.

Le mecanisme est la dependance entre items : un tirage independant assemble librement des
reponses qu'un agent assemble toujours de la meme facon [HYPOTHESE pour le mecanisme, MESURE
pour le fait]. Yuan observe le meme fait sur son Sonnet 4.6, « 17 distinct response patterns
in 200 instances » sous ordre fixe, sa figure 6 [CONFIRME]. Le rapprochement avec les
19 patrons de croyances sur 929 de Wang et al. cite en `MODELE-DU-MONDE.md` 3.3 est une
lecture et non une mesure [PROBABLE].

### 4.2 Tableau 4 : la correlation entre items

Moyenne des `|rho|` de Spearman sur les paires d'items ordinaux, au moins 30 personnes
communes par paire, 11 026 paires [MESURE, `a44-quantites.csv`, `Q4` et `Q5`, `S_ideo`].

| condition | Q4 brute | son nul | Q5 apres retrait du segment | son nul | `d` de Q5 | IC de `d` |
|---|---|---|---|---|---|---|
| humains vague 1 | 0,0926 | 0,0508 | 0,0670 | 0,0248 | **0,0422** | [0,0351 ; 0,0402] |
| humains vague 2 | 0,0947 | 0,0512 | 0,0692 | 0,0248 | **0,0444** | [0,0371 ; 0,0425] |
| agents composite | 0,1643 | 0,0937 | 0,1087 | 0,0248 | **0,0838** | [0,0731 ; 0,0826] |
| agents entretien (v3) | 0,1841 | 0,1170 | 0,1140 | 0,0246 | **0,0894** | [0,0779 ; 0,0889] |
| agents enquete | 0,1732 | 0,1092 | 0,1020 | 0,0247 | **0,0773** | [0,0664 ; 0,0771] |
| agents v7 | 0,1340 | 0,0277 | 0,1286 | 0,0241 | **0,1045** | [0,0894 ; 0,1060] |
| agents v6 | 0,1243 | 0,0292 | 0,1157 | 0,0231 | **0,0926** | [0,0808 ; 0,0932] |
| **agents v8** | **0,3330** | **0,2973** | **0,1168** | **0,0226** | **0,0942** | [0,0775 ; 0,0986] |
| B1 argmax | 0,1308 | 0,0969 | 0,0715 | 0,0228 | 0,0487 | [0,0405 ; 0,0458] |
| B2 argmax | 0,1503 | 0,0794 | 0,1025 | 0,0200 | 0,0825 | [0,0712 ; 0,0816] |
| PMM k=10 | 0,1172 | 0,0637 | 0,0799 | 0,0241 | 0,0558 | [0,0469 ; 0,0536] |
| B3 foret | 0,1066 | 0,0818 | 0,0525 | 0,0175 | 0,0351 | [0,0290 ; 0,0335] |
| *B0 tirage, temoin* | *0,0247* | *0,0246* | *0,0247* | *0,0247* | ***0,0000*** | *[-0,0009 ; 0,0009], `p = 0,970`* |
| *B0 mode, temoin* | *0,0012* | *0,0001* | *0,0012* | *0,0001* | *0,0012* | *[0,0011 ; 0,0012]* |
| humains vague 2 (150) | 0,1146 | 0,0817 | 0,1003 | 0,0667 | 0,0336 | [0,0209 ; 0,0364] |
| C3 | 0,1182 | 0,0642 | 0,1100 | 0,0555 | **0,0546** | [0,0378 ; 0,0588] |
| **C2** | **0,2139** | **0,1926** | **0,0863** | **0,0396** | **0,0467** | [0,0286 ; 0,0517] |

**Trois faits.**

1. **La valeur du nul sur Q5 est le plancher de bruit d'echantillonnage et rien d'autre**,
   0,0226 a 0,0248 sur 1 052 personnes, 0,040 a 0,067 sur 150. C'est la valeur attendue de
   `|rho|` pour des colonnes independantes, `racine(2 / pi N)`. Le temoin `B0 tirage` s'y
   colle exactement, `d = 0,0000`, `p = 0,970`. **Q5 est donc bien un test de structure et
   non un artefact.**
2. **Les conditions a modele de langage ont un exces deux fois superieur a celui des
   humains**, 0,077 a 0,105 contre 0,042. `agents v8` est le plus couple en brut,
   `Q4 = 0,333` contre 0,093 chez les humains, soit **3,6 fois**, et l'essentiel de ce
   couplage est de l'ideologie : son nul brut vaut deja 0,297. Une fois le segment retire il
   reste 0,094 d'exces, encore 2,2 fois l'humain. C'est la mesure la plus directe du fait
   de a30 6.2, « les reseaux d'attitudes des agents sont deux fois plus denses que ceux des
   humains » [MESURE pour a44, la concordance avec a30 etant une lecture, PROBABLE].
3. **`B3 foret` est la seule methode sous le niveau humain**, 0,035 contre 0,042, et
   `B1 argmax` est au niveau humain, 0,049. Les deux predicteurs par l'esperance les plus
   simples produisent moins de structure residuelle que les vraies personnes ; les agents en
   produisent deux fois trop.

### 4.3 L'exces de correlation n'est pas de la demographie

[MESURE, `a44-structure-par-finesse.csv`, 50 replicats, **descriptif post hoc, ecart E3**]

L'exces de Q5 mesure la structure qui survit au retrait du segment. Il pouvait venir d'une
demographie plus fine que le segment employe, la race ou l'education, presente dans
l'etiquette de l'agent : ce serait encore du gabarit, simplement d'un groupe plus petit. On
fait donc varier la finesse.

| condition | N0 aucun segment | N1 ideologie | N2 genre x race x ideologie | N3 ideologie x genre x age | N4 ideologie x genre x race x education |
|---|---|---|---|---|---|
| cellules effectives | 1 | 7 | 18 | 42 | 80 |
| humains vague 1 | 0,0679 | 0,0422 | 0,0432 | 0,0425 | **0,0413** |
| humains vague 2 | 0,0700 | 0,0444 | 0,0450 | 0,0444 | **0,0431** |
| agents composite | 0,1397 | 0,0839 | 0,0883 | 0,0880 | **0,0840** |
| agents entretien (v3) | 0,1597 | 0,0894 | 0,0936 | 0,0941 | **0,0892** |
| agents enquete | 0,1489 | 0,0773 | 0,0858 | 0,0847 | **0,0836** |
| agents v7 | 0,1102 | 0,1045 | 0,1053 | 0,1040 | **0,1041** |
| agents v6 | 0,1015 | 0,0926 | 0,0901 | 0,0881 | **0,0863** |
| agents v8 | **0,3097** | 0,0942 | 0,1217 | 0,1202 | **0,1160** |
| B1 argmax | 0,1083 | 0,0487 | 0,0507 | 0,0484 | **0,0457** |
| B2 argmax | 0,1306 | 0,0825 | 0,0872 | 0,0853 | **0,0860** |
| PMM k=10 | 0,0933 | 0,0558 | 0,0581 | 0,0572 | **0,0551** |
| B3 foret | 0,0887 | 0,0351 | 0,0399 | 0,0365 | **0,0358** |
| *B0 tirage, temoin* | *0,0001* | *0,0000* | *0,0001* | *0,0000* | ***0,0002*** |

**L'exces ne descend plus apres le premier conditionnement.** Entre N1, sept cellules, et
N4, quatre-vingts cellules, les humains passent de 0,0422 a 0,0413 et `agents composite` de
0,0839 a 0,0840. **Retirer trois demographies de plus ne retire rien.** Le seul mouvement
important est celui de v8 entre N0 et N1, de 0,3097 a 0,0942 : les deux tiers du couplage de
v8 sont de l'ideologie declaree, ce qui est le meme fait que son ratio inter de 8,13. Le
tiers restant survit a tout.

**Le temoin `B0 tirage` reste a 0,0000 aux cinq niveaux** : la mesure ne fabrique pas
d'exces quand il n'y en a pas.

**Ce que cela permet et ne permet pas de dire.** Cela permet de dire que la structure
residuelle n'est **pas** attribuable aux demographies que l'agent a recues. Cela ne permet
pas de dire qu'elle est celle de la personne : une variable latente unique appliquee a tous
les agents produirait la meme mesure. **C'est la section 5 qui tranche.**

---

## 5. Les trois proprietes de Yuan, transposees

### 5.1 Ce qui est impossible, et il faut le dire d'entree

Yuan perturbe **l'ordre de presentation des items** dans le contexte de chaque instance
[CONFIRME, sa section 2, cadres `FO`, `RO`, `RO-BTSP`].
Chez nous, permuter l'ordre des items dans l'invite de C2 ou de C3 **demanderait de relancer
22 350 appels par condition**, et aucune trace a ordre fixe ne permet de reconstruire une
trace a ordre aleatoire. **Le test d'ordre de Yuan est hors de portee de a44, il n'a pas ete
fait, et rien ici ne doit etre lu comme s'il l'avait ete.** Il reste ce que la veille
section 4.1 chiffre a une nuit courte d'appels.

Ce qui le remplace applique le meme raisonnement a l'autre axe de la matrice. Si un agent est
un gabarit de groupe, alors a l'interieur d'un segment les reponses sont echangeables entre
personnes, et permuter qui recoit quelle reponse simulee ne change rien a l'exactitude. Si
l'agent porte la personne, l'exactitude chute.

| terme de Yuan | notre terme | ce qu'on mesure |
|---|---|---|
| `FO`, ordre fixe partage | assignation vraie | exactitude par personne |
| `RO`, ordre propre a chaque instance | permutation intra segment | exactitude moyenne sur 200 permutations des personnes a l'interieur de leur segment |
| `RO-BTSP`, realignement sur un ordre partage | reassignation optimale intra segment | exactitude sous l'appariement hongrois qui maximise l'accord dans chaque segment |

### 5.2 Tableau 5 : la chute d'exactitude sous permutation intra segment

Axe ideologie, sept segments, 200 permutations, humains vague 2 en reference [MESURE,
`a44-permutation.csv`, `S_ideo`].

| condition | exactitude vraie | permutee | bande | chute | chute relative | **part du plancher humain** | reassignation optimale | part recuperee |
|---|---|---|---|---|---|---|---|---|
| humains vague 1 | 1,0000 | 0,5212 | [0,518 ; 0,525] | 0,4788 | 47,9 % | *reference triviale* | 1,0000 | **1,000** |
| **humains vague 2** | **0,7950** | **0,5190** | **[0,516 ; 0,522]** | **0,2760** | **34,7 %** | **1,000** | **0,7954** | **1,001** |
| agents composite | 0,6839 | 0,5316 | [0,529 ; 0,534] | 0,1524 | 22,3 % | **0,642** | 0,6855 | 1,010 |
| agents enquete | 0,6510 | 0,5291 | [0,526 ; 0,531] | 0,1219 | 18,7 % | **0,539** | 0,6568 | 1,048 |
| agents entretien (v3) | 0,6565 | 0,5354 | [0,533 ; 0,538] | 0,1211 | 18,5 % | **0,531** | 0,6613 | 1,040 |
| PMM k=10 | 0,6684 | 0,5301 | [0,527 ; 0,534] | 0,1383 | 20,7 % | **0,596** | 0,6767 | 1,060 |
| B2 argmax | 0,6717 | 0,5886 | [0,586 ; 0,591] | 0,0831 | 12,4 % | 0,357 | 0,6932 | 1,259 |
| agents v6 | 0,5818 | 0,5344 | [0,532 ; 0,537] | 0,0474 | 8,2 % | 0,235 | 0,6251 | 1,913 |
| B1 argmax | 0,6209 | 0,5830 | [0,581 ; 0,585] | 0,0378 | 6,1 % | 0,175 | 0,6844 | 2,680 |
| agents v7 | 0,5640 | 0,5334 | [0,531 ; 0,536] | 0,0306 | 5,4 % | 0,156 | 0,6249 | 2,988 |
| B3 foret | 0,6340 | 0,6055 | [0,604 ; 0,607] | 0,0285 | 4,5 % | 0,129 | 0,6842 | 2,764 |
| **agents v8** | **0,5591** | **0,5451** | **[0,543 ; 0,547]** | **0,0140** | **2,5 %** | **0,072** | **0,6139** | **4,914** |
| *B0 mode, temoin* | *0,5934* | *0,5944* | *[0,594 ; 0,595]* | *-0,0011* | ***-0,2 %*** | *0,000* | *0,6033* | *sans objet* |
| *B0 tirage, temoin* | *0,4918* | *0,4929* | *[0,491 ; 0,495]* | *-0,0011* | ***-0,2 %*** | *0,000* | *0,5749* | *sans objet* |
| humains vague 1 (150) | 1,0000 | 0,5381 | [0,522 ; 0,555] | 0,4619 | 46,2 % | *reference triviale* | 1,0000 | **1,000** |
| **humains vague 2 (150)** | **0,7915** | **0,5280** | **[0,517 ; 0,541]** | **0,2635** | **33,3 %** | **1,000** | **0,7915** | **1,000** |
| C3 | 0,5817 | 0,4947 | [0,487 ; 0,501] | 0,0870 | 15,0 % | **0,449** | 0,5854 | 1,043 |
| **C2** | **0,5263** | **0,5136** | **[0,510 ; 0,517]** | **0,0128** | **2,4 %** | **0,073** | **0,5529** | **3,087** |

**Cinq lectures.**

1. **Le controle passe.** Les deux temoins aveugles a la personne, `B0 mode` et
   `B0 tirage`, ne perdent rien sous permutation, moins 0,2 pour cent, valeur negative parce
   que la moyenne des permutations inclut la permutation identite avec probabilite nulle et
   du bruit avec probabilite un. La mesure ne fabrique pas de chute.
2. **Le plancher humain est 34,7 pour cent** : les memes personnes reinterrogees perdent un
   tiers de leur exactitude quand on melange qui est qui a l'interieur de leur camp
   politique. C'est ce qu'une population qui porte des personnes fait.
3. **`agents v8` et C2, les deux conditions a etiquette seule, perdent 2,5 et 2,4 pour
   cent, soit 7 pour cent du plancher humain**, et se placent a deux points des temoins
   aveugles. **Au sens operationnel du critere de Yuan, ce sont des gabarits de groupe.**
4. **Les trois conditions riches de Stanford, `PMM k=10` et C3 sont du cote de la personne**,
   45 a 64 pour cent du plancher humain. Elles ne sont pas des gabarits.
5. **Le troisieme terme confirme le premier, dans l'autre sens.** Chez les humains la
   reassignation optimale ne gagne rien, rapport 1,000 et 1,001 : la vraie assignation est
   deja la meilleure, et le sur-ajustement de l'appariement hongrois est negligeable a ces
   tailles de segment. **C'est le controle qui leve la reserve ecrite au preenregistrement.**
   Chez `agents composite`, `entretien`, `enquete`, `PMM` et C3 le rapport reste entre 1,01
   et 1,06. Chez v8 il vaut **4,91**, chez C2 **3,09**, chez v7 2,99, chez `B3 foret` 2,76,
   chez B1 2,68 : **une reassignation arbitraire des reponses a l'interieur du segment fait
   trois a cinq fois mieux que la vraie.** C'est exactement le `RO-BTSP` de Yuan : le signal
   discriminant est dans le gabarit et l'assignation aux instances est arbitraire.

Sous `S_fin`, 42 segments, le classement est identique et les chutes sont plus petites parce
que les segments sont plus petits : v8 1,8 pour cent, C2 1,9 pour cent, composite
20,7 pour cent, humains vague 2 32,5 pour cent sur le perimetre 1 052 et 24,6 pour cent sur
le perimetre 150 [MESURE, `a44-permutation.csv`, `S_fin`]. Le rapport de reassignation y
vaut 5,03 pour v8, 2,76 pour C2, 1,003 pour composite et 1,0005 pour les humains vague 2 :
le depart est le meme et il est plus net.

---

## 6. La rarete de groupe, mise au meme test

[MESURE, `a44-rarete.csv`, `S_ideo`, 50 replicats nuls, **ecart E2**, pas d'IC bootstrap]

| condition | lift personne | son nul | lift segment | son nul | groupe sur personne | son nul | rappel des rares | son nul |
|---|---|---|---|---|---|---|---|---|
| humains vague 2 | 0,241 | **0,001** | 0,135 | 0,184 | 0,561 | 85,5 | 0,548 | 0,089 |
| agents composite | 0,212 | 0,047 | 0,343 | 0,301 | 1,622 | 6,60 | 0,307 | 0,096 |
| agents entretien (v3) | 0,106 | 0,039 | 0,388 | 0,332 | 3,651 | 8,96 | 0,295 | 0,106 |
| agents enquete | 0,199 | 0,046 | 0,378 | 0,341 | 1,902 | 7,73 | 0,231 | 0,092 |
| **agents v8** | **0,101** | **0,100** | **0,743** | **0,728** | **7,369** | **7,324** | **0,172** | **0,156** |
| B1 argmax | 0,095 | 0,053 | 0,503 | 0,462 | 5,281 | 10,78 | 0,058 | 0,036 |
| B2 argmax | 0,549 | 0,099 | 0,614 | 0,549 | 1,117 | 6,23 | 0,036 | 0,012 |
| PMM k=10 | 0,207 | 0,028 | 0,258 | 0,275 | 1,249 | 11,27 | 0,213 | 0,075 |
| B3 foret | 0,099 | 0,016 | 0,811 | 0,513 | 8,179 | 24,67 | 0,014 | 0,006 |
| *B0 tirage, temoin* | *-0,021* | *-0,026* | *-0,019* | *-0,020* | *non defini* | *non defini* | *0,062* | *0,064* |
| humains vague 2 (150) | 0,283 | -0,027 | 0,112 | 0,261 | 0,398 | 62,6 | 0,474 | 0,091 |
| C3 | 0,105 | -0,007 | 0,046 | 0,081 | 0,436 | 20,1 | 0,220 | 0,103 |
| **C2** | **0,072** | **0,056** | **0,319** | **0,313** | **4,446** | **6,32** | **0,129** | **0,108** |

**Le resultat le plus dur du rapport tient en une ligne.** Le rapport groupe sur personne de
`agents v8`, publie a 7,37 par a31 et cite dans `MODELE-DU-MONDE.md` section 7 comme la
preuve que « le groupe pese jusqu'a huit fois plus », **est reproduit a 7,32 par un
generateur qui tire chaque reponse independamment dans la marginale du segment**. Ses deux
composantes le sont aussi : lift de personne 0,101 contre 0,100, lift de segment 0,743
contre 0,728. **Le rappel des rares de v8, 0,172, est reproduit a 0,156, soit 91 pour cent.**
Pour C2, le lift de segment est reproduit a 98 pour cent, le lift de personne a 78, le
rappel a 84.

**Chez les humains et chez les conditions riches, le nul echoue completement du cote de la
personne**, comme il le doit : lift de personne 0,241 chez les humains contre 0,001 pour
leur nul, 0,212 contre 0,047 pour `agents composite`, 0,207 contre 0,028 pour `PMM`, 0,105
contre moins 0,007 pour C3. Ce que le nul reproduit toujours, chez tout le monde, est le
lift de **segment**, entre 88 et 98 pour cent.

**Autrement dit : la moitie « rarete de groupe » de a31 est une quantite de gabarit, la
moitie « rarete de personne » n'en est pas une, et le rapport des deux est une quantite de
gabarit exactement chez les conditions dont le lift de personne est deja au niveau du nul,
c'est a dire v8 et, aux trois quarts, C2.** Le classement de a31 n'est pas invalide ; ce qui
change est que le chiffre de 7,37 ne demontre plus rien de plus que les marginales de v8.

Le temoin `B0 tirage` a un lift de personne de moins 0,021 contre moins 0,026 pour son nul,
et un rappel de 0,062 contre 0,064 : nul partout, comme attendu.

---

## 7. Verdict par condition

### 7.1 Le verdict preenregistre, et pourquoi il ne sert a rien

Le preenregistrement fixe le verdict sur la seule quantite Q5 sous `S_fin`, famille de
treize tests, correction de Holm. Resultat [MESURE, `a44-verdicts.csv`] : **les treize
conditions recoivent « porteur de personne », `p` de Holm 0,0130 pour les treize**, valeur
plancher de Holm sur 1 000 tirages bootstrap. Humains, agents riches, agents a etiquette,
regression, voisins et PMM sont tous a plus de 130 ecarts types de leur nul.

**Le critere primaire declare ne separe rien et il faut l'ecrire.** Sa seule vertu est
negative : la seule population qu'il classe correctement comme sans structure est celle qui
l'est vraiment, `B0 tirage`, `d = 0,0000`, `p = 0,970`. Le critere fonctionne, la question
qu'il pose n'est pas la bonne. Q5 mesure « il reste de la structure une fois le segment
retire » ; elle ne dit pas **de qui** est cette structure, et la section 4.3 montre qu'elle
ne le dira jamais, puisqu'elle ne bouge plus quand on affine le conditionnement.

### 7.2 Le verdict par le critere qui separe

La permutation intra segment est le seul test du rapport qui distingue. Elle a ete
preenregistree comme remplacement de la perturbation d'ordre, pas comme quantite de verdict :
**ce classement est donc post hoc et signale comme tel**. Seuil de lecture, non declare
avant : « gabarit » si la chute vaut moins de 15 pour cent du plancher humain, « porteur de
personne » si elle vaut plus de 40 pour cent, « intermediaire » entre les deux.

| condition | chute, part du plancher humain | rapport de reassignation | lecture |
|---|---|---|---|
| `agents v8` | 0,072 | 4,91 | **gabarit de groupe** |
| C2 | 0,073 | 3,09 | **gabarit de groupe** |
| `agents v7` | 0,156 | 2,99 | intermediaire, du cote du gabarit |
| `B3 foret` | 0,129 | 2,76 | **gabarit de groupe** |
| `B1 argmax` | 0,175 | 2,68 | intermediaire, du cote du gabarit |
| `agents v6` | 0,235 | 1,91 | intermediaire |
| `B2 argmax` | 0,357 | 1,26 | intermediaire |
| C3 | 0,449 | 1,04 | **porteur de personne** |
| `agents entretien (v3)` | 0,531 | 1,04 | **porteur de personne** |
| `agents enquete` | 0,539 | 1,05 | **porteur de personne** |
| `PMM k=10` | 0,596 | 1,06 | **porteur de personne** |
| `agents composite` | 0,642 | 1,01 | **porteur de personne** |
| humains vague 2 | 1,000 | 1,001 | reference |

**Les deux criteres concordent entierement** : les cinq conditions dont la reassignation
arbitraire fait plus de 2,5 fois mieux que la vraie sont exactement les cinq dont la chute
est sous 18 pour cent du plancher humain. **Et le depart passe par l'etiquette, pas par le
langage** [MESURE] : v8 et C2 sont du cote du gabarit, C3, qui est le meme modele et le meme run sans
etiquette, est du cote de la personne, 0,449 contre 0,073, rapport 1,04 contre 3,09. C'est
le meme depart que a29 3, a31 2.3 et a34 4, mesure par un instrument entierement different.

---

## 8. La figure

`a44-figure-generateur-nul.png` et `.svg`. Deux panneaux, la meme liste de conditions dans
le meme ordre, un trait horizontal separant le perimetre 1 052 du perimetre 150.

**Panneau A**, le ratio inter sur l'axe ideologie, echelle logarithmique. Chaque condition
porte deux points relies : la valeur mesuree et celle de son generateur nul, avec la bande
des 200 replicats. **Les traits sont invisibles pour les onze conditions du perimetre
1 052** : le nul tombe sur la mesure. C'est le resultat du rapport, sous sa forme la plus
directe.

**Panneau B**, la correlation entre items apres retrait du segment. Les traits sont longs
partout, et deux fois plus longs pour les conditions rouges que pour les vertes. Le nul y
est un plancher de bruit et non une reproduction.

**Ce que la figure ne montre pas et qu'il faut lire au tableau 5** : la permutation intra
segment, qui est le seul test qui separe les conditions.

---

## 9. Ce que cela change a `MODELE-DU-MONDE.md`, sections 2 et 7

### 9.1 Section 7, la these

La these dit aujourd'hui : « les ecarts entre groupes sont gonfles d'un facteur 1,8 a 5,9 et
la dispersion interne ramenee a 0,64 a 0,89 de celle des humains », puis « sa seule presence
fait passer le gonflement de 0,73 a 8,16, la dispersion interne de 0,681 a 0,365, et
deplace l'attribution des reponses rares [...] au regime statistique, ou le groupe pese
jusqu'a huit fois plus ».

**Aucune de ces valeurs n'est fausse. Ce qui change est ce qu'elles prouvent.** Les trois
quantites citees, ratio inter, ratio intra et rapport groupe sur personne, sont reproduites
par un generateur sans aucune structure individuelle, a 100,6 pour cent, 99,4 pour cent et
99,4 pour cent respectivement pour `agents v8`. **Elles decrivent le gabarit de groupe de la
condition, pas le rapport entre l'agent et la personne.** La phrase « une societe simulee a
partir d'etiquettes remplace chaque personne par l'esperance de son groupe » a besoin d'un
appui qui ne soit pas une fonctionnelle de la table de contingence, et a44 en fournit un :
**la chute d'exactitude sous permutation des personnes intra segment, 2,5 pour cent pour v8
et 2,4 pour cent pour C2 contre 34,7 pour cent chez les memes humains reinterroges, et
2,4 pour cent contre moins 0,2 pour cent pour un temoin aveugle a la personne.**

Proposition de reformulation de la phrase centrale, a discuter :

> Une societe simulee a partir d'etiquettes remplace chaque personne par l'esperance de son
> groupe : melanger les personnes a l'interieur de leur camp politique ne coute que
> 2,5 pour cent d'exactitude a un agent demographique, contre 34,7 pour cent aux memes
> humains reinterroges, et une reassignation arbitraire des reponses a l'interieur du camp
> fait cinq fois mieux que la vraie. Les mesures de gonflement d'ecart entre groupes, qui
> ont porte le premier diagnostic, sont reproduites a un pour cent pres par un generateur
> sans structure individuelle : elles decrivent le gabarit et non son rapport aux personnes.

**Le paragraphe « l'adversaire principal tient en trois objections » gagne une quatrieme
objection, et c'est nous qui l'ecrivons** : « vos deux ratios sont des fonctionnelles de la
table de contingence segment par modalite ; un generateur conditionnellement independant les
reproduit ; ils ne disent rien de la substitution de la personne ». Elle a une reponse,
mesuree, et elle est la section 5 de ce rapport.

### 9.2 Section 2, le mecanisme

Le mecanisme reconstruit en 2.1 n'est pas touche : imputation par l'esperance, quatre
contraintes, van Buuren. La liste des « six chemins » qui disent la meme chose doit en
revanche etre relue quantite par quantite :

| chemin cite en 2.1 | reproduit par le generateur nul ? |
|---|---|
| « l'etiquette deplace le profil d'erreur de treize points vers la modalite majoritaire du segment » (a28 test 3) | **non teste par a44**, mais c'est une quantite de table de contingence ; a verifier |
| « elle fait tomber l'appariement des reponses rares aux bonnes personnes de 0,410 a 0,194 » (a29) | **non**, c'est une quantite d'appariement individuel ; le nul a un lift de personne nul |
| « le rapport groupe sur personne vaut 4,45 avec etiquette, 0,44 sans, 8,18 pour une foret » (a31) | **oui pour v8, 7,37 contre 7,32 ; aux trois quarts pour C2 ; non pour les humains et les conditions riches** |
| « elle ecrase la dispersion interne presque du double, 0,365 contre 0,681 » (a35) | **oui, a 95,3 pour cent** |
| « elle rend le camp de gauche litteralement unanime, Gini Simpson 0,000 » (a30) | **oui par construction** : une marginale de segment degeneree donne un nul degenere |
| « le manque de contexte est refute a personne constante » (a33) | **non teste par a44** |

**Deux des six chemins sont des quantites de gabarit, deux ne le sont pas, deux ne sont pas
testes.** La phrase « nos mesures disent la meme chose par six chemins » doit devenir « par
six chemins, dont deux mesurent le gabarit et deux le rapport aux personnes ». C'est moins
impressionnant et c'est plus solide, parce que les deux qui mesurent le rapport aux
personnes sont exactement celles qu'un relecteur ne peut pas balayer avec le nul de Yuan.

### 9.3 L'anteriorite

La veille ecrivait : « l'anteriorite est desormais a lui ». a44 le confirme sur nos propres
donnees et ajoute une chose que Yuan n'a pas : **son negatif est general, notre positif ne
l'est pas.** Sa proposition S4 dit qu'augmenter le nombre de personas « multiplie les
gabarits plutot qu'il ne cree des selves » ; nos conditions riches, composite, entretien,
enquete, echappent au gabarit sur le test de permutation, 53 a 64 pour cent du plancher
humain, et C3 aussi, 45 pour cent. **Sur des attitudes politiques et avec des personnes
reelles en face, la conclusion negative de Yuan ne vaut que pour les conditions a etiquette
seule.** C'est ce que le dossier a de propre a dire apres sa lecture, et cela ne contredit
pas son papier : il ne teste que deux personas culturelles installees par invite, ce qui est
exactement notre condition a etiquette.

---

## 10. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. **« Nos deux ratios sont des quantites de gabarit de groupe, et nous le demontrons »**
   [MESURE]. Invariance exacte sous permutation intra segment, `0,000e+00` ; part reproduite
   100,6 pour cent sur l'inter de v8 et 99,4 pour cent sur son intra.
2. **« Un agent a etiquette seule est un gabarit de groupe au sens operationnel de Yuan »**
   [MESURE]. Chute de 2,5 pour cent pour v8 et 2,4 pour cent pour C2 sous permutation intra
   segment, contre 34,7 pour cent chez les memes humains reinterroges et moins 0,2 pour cent
   pour un temoin aveugle ; reassignation arbitraire meilleure que la vraie d'un facteur 4,9
   et 3,1.
3. **« Le depart passe par l'etiquette et non par le langage »** [MESURE]. C3, meme modele,
   meme run, sans etiquette, est a 44,9 pour cent du plancher humain avec un rapport de
   reassignation de 1,04 ; C2 est a 7,3 pour cent avec 3,09.
4. **« Les populations simulees sont plus pauvres que leur propre gabarit »** [MESURE].
   Deficit de patrons distincts de 14 a 32 pour cent chez les conditions a modele de langage
   contre 7 a 8 pour cent chez les humains, seize conditions sur seize dans le meme sens,
   temoin aveugle a moins 0,04 pour cent.
5. **« Les items d'un agent sont couples deux fois plus fort que chez de vraies personnes, et
   ce n'est pas de la demographie »** [MESURE]. Exces de correlation residualisee de 0,077 a
   0,105 contre 0,042 chez les humains, stable de sept a quatre-vingts cellules de
   conditionnement.
6. **« Le 7,37 de a31 pour v8 ne prouve pas ce qu'on croyait »** [MESURE, 50 replicats].
   7,32 sous le generateur nul, et ses deux composantes a 99 et 98 pour cent.

### Interdit

1. **Interdit de dire que a44 a fait le test de Yuan.** Le test de Yuan est une perturbation
   d'ordre des items. a44 ne l'a pas faite, elle est hors de portee sans appels de modele, et
   la permutation des personnes est une autre question posee au meme objet.
2. **Interdit de dire que la double distorsion de a1 est fausse.** Elle est exacte, elle est
   reproduite au chiffre pres par a44 dans une autre mesure et sur un autre jeu d'items. Ce
   qui est interdit est de la presenter comme une preuve que l'agent remplace la personne :
   c'est une preuve que la table de contingence de l'agent differe de celle des humains.
3. **Interdit de citer la ligne C2 sous `S_fin`**, `d = +1,24`, `p = 0,028` : 64,3 pour cent
   des couples item x segment y sont replies, le nul n'est pas conditionne, la ligne est
   mecanique.
4. **Interdit de comparer une condition du perimetre 1 052 a une condition du perimetre 150.**
   Le plancher de bruit de toutes les quantites depend de l'effectif : le nul de Q5 vaut
   0,025 a 1 052 personnes et 0,067 a 150, le `d` du ratio inter vaut moins 0,08 a 1 052 et
   moins 0,83 a 150. Les deux blocs sont separes partout, y compris sur la figure.
5. **Interdit d'employer le verdict preenregistre.** Il classe les treize conditions de la
   meme facon ; sa seule valeur est de valider le dispositif sur le temoin `B0 tirage`.
6. **Interdit de traiter le classement de la section 7.2 comme preenregistre.** Les seuils de
   15 et 40 pour cent du plancher humain ont ete choisis apres avoir vu les chiffres. Ce qui
   est preenregistre est la mesure, pas le decoupage.
7. **Interdit de conclure sur les modeles en general a partir de C2 et C3.** Un modele ouvert
   de 4 milliards de parametres, un seul run, 150 personnes, et la limite ouverte de a23 sur
   la formulation des invites reste entiere.
8. **Interdit de dire que l'exces de correlation des agents est de la structure
   individuelle.** a44 montre qu'il n'est pas de la demographie recue ; une variable latente
   unique appliquee a tous les agents produirait la meme mesure. Seule la permutation
   tranche, et elle tranche dans l'autre sens pour v8 et C2.

---

## 11. Ce que je n'ai pas pu verifier

1. **La perturbation d'ordre des items, qui est le test central de Yuan.** Elle demande
   22 350 appels de modele par condition et aucune trace a ordre fixe ne permet de la
   reconstruire. a44 ne l'a pas faite et ne pretend pas l'avoir approchee.

2. **La matrice de correlation intra instance de Yuan n'a pas d'equivalent chez nous.** Il
   range 50 reponses d'une passation en une matrice 10 x 5 et lit la correlation entre
   colonnes **a l'interieur d'une personne**. Le GSS ne donne qu'une passation par personne
   et aucune structure item par dimension. Notre Q5 est une correlation entre items **sur la
   population** apres retrait du segment. Ce n'est pas le meme objet, et la ressemblance de
   nom ne doit pas etre lue comme une replication.

3. **Le plancher humain de a44 n'a qu'une des trois natures du sien.** Nous avons la
   fidelite, la vague 2 des memes personnes. Ni identifiabilite individuelle, ni validite de
   critere externe : rien dans le paquet OSF ne joue le role de sa moyenne generale.

4. **Le seuil de repli du generateur nul est un degre de liberte non teste.** Il est fixe a
   cinq repondants observes, declare avant execution, mais sa sensibilite n'a pas ete
   mesuree. Son effet est enorme sur le perimetre 150 sous `S_fin`, 64,3 pour cent des
   couples, et il rend cette cellule du plan inutilisable.

5. **Q3 n'a pas d'intervalle bootstrap sur les personnes.** Un tirage avec remise duplique
   des personnes et fait baisser mecaniquement le nombre de patrons distincts. La bande
   publiee ne porte que l'incertitude du nul.

6. **Q6 et Q7 sont estimes sur 50 replicats et sans bootstrap sur les personnes**, ecart E2.
   Les valeurs de v8 sont si proches, 7,369 contre 7,324, que la conclusion ne peut pas
   basculer, mais aucune des lignes de la section 6 n'a d'intervalle.

7. **Trois des six chemins de `MODELE-DU-MONDE.md` 2.1 n'ont pas ete passes au nul** : a28
   test 3, a29 correlation par personne, a33 ablation de famille. Le tableau 9.2 le signale
   ligne par ligne.

8. **L'intervalle bootstrap de `d` n'est pas centre sur l'estimation ponctuelle de `d`.**
    Cause : le tirage avec remise duplique des personnes, ce qui modifie l'effectif effectif
    et donc les estimateurs a biais corrige et le plancher de correlation, differemment pour
    la population et pour son nul. Sur le perimetre 1 052 l'ecart est de l'ordre de 2 a
    5 pour cent de `d` et les intervalles de Q1 et Q2 contiennent leur estimation
    ponctuelle ; ceux de Q5 sont systematiquement 2 a 5 pour cent en dessous, par exemple
    `d = 0,0422` pour les humains vague 1 contre un intervalle [0,0351 ; 0,0402]. Sur le
    perimetre 150 l'ecart est grand, cf. section 3.2. **Aucune conclusion du rapport ne
    bascule** : les distances de Q5 valent 130 a 470 ecarts types de leur nul, et les
    quantites dont l'intervalle contient zero, Q1 et Q2 sur le perimetre 1 052, y sont a
    moins d'un demi ecart type de zero. La correction propre serait un bootstrap qui
    reechantillonne aussi les parametres du nul, ce qui n'a pas ete fait.

9. **La convention de centrage de Q4 et Q5.** Les moyennes et variances sont calculees sur
   l'ensemble observe de chaque item et non paire par paire. L'ecart est de l'ordre du taux
   de manquants et la convention est identique pour la population et pour son nul, donc elle
   ne peut pas creer de distance entre les deux ; elle peut deplacer les deux ensemble.

10. **Rien hors du GSS.** Ni Twin-2K-500, ni les jeux de a6, ni le panel de a12. Le perimetre
   est celui de a25, a28, a29 et a31, et rien d'autre.

11. **a44 emploie l'indice de Gini Simpson et jamais l'entropie.** a1 montre que les deux
    donnent le meme classement et le meme signe, et la section 1 point 5 le verifie sur trois
    conditions, mais aucun chiffre de a44 n'est directement comparable au 8,16 d'entropie de
    a23.

---

## 12. Questions ouvertes pour Simon

1. **La question qui commande tout le reste : que fait on de la double distorsion dans le
   papier, maintenant qu'on sait qu'elle est une quantite de gabarit ?** Trois positions
   possibles. (a) La garder comme mesure principale en assumant qu'elle decrit le gabarit,
   ce qui est defendable puisque c'est le gabarit qui est le sujet, mais expose a l'objection
   de Yuan mot pour mot. (b) La retrograder en mesure descriptive et faire porter la these
   par la permutation intra segment, qui est un test de substitution de la personne et pas
   une description de distribution. (c) Publier les deux avec le nul comme baseline
   systematique, ce qui est le plus honnete et le plus long. Ma preference est (c), mais elle
   demande de repasser a28, a29 et a33 au nul.

2. **Faut il depenser la nuit d'appels pour le vrai test d'ordre de Yuan ?** Le prix est
   d'environ deux heures de calcul pour un troisieme regime a ordre randomise par personne
   sur C2 et C3. Le gain est de pouvoir ecrire « confirme par le critere de l'adversaire »
   et non « par un critere que nous avons transpose ». Le risque est que C2 ne bouge pas,
   parce qu'un agent qui n'a que l'etiquette n'a pas de contexte d'items a permuter, ce qui
   rendrait le test vide chez nous et informatif seulement sur C3.

3. **Le fait que les agents aient moins de patrons distincts que leur propre generateur nul
   est il un resultat a lui seul ?** Il n'est dans aucun papier lu [PROBABLE, conclusion d'absence sur le corpus lu], il tient sur seize
   conditions, il a un temoin nul propre, et il dit quelque chose de plus fort que
   l'ecrasement de dispersion : l'agent n'est pas seulement moins disperse que les humains,
   il est moins libre que sa propre distribution marginale. Le nom qui lui va est « deficit
   de combinaison ». Est ce publiable seul, ou faut il l'adosser aux 19 patrons sur 929 de
   Wang et al. ?

4. **La reassignation optimale intra segment est elle acceptable comme troisieme terme ?**
   Le controle humain, rapport 1,001, montre que le sur-ajustement est negligeable a ces
   tailles de segment, ce qui leve la reserve du preenregistrement. Mais ce n'est pas ce que
   Yuan fait, et un relecteur peut refuser une statistique optimisee sur les donnees. Faut il
   la remplacer par une moyenne sur des reassignations tirees au hasard sous contrainte, ce
   qui serait plus proche de son `RO-BTSP` et plus faible ?

5. **`B3 foret` et `B1 argmax` sont du cote du gabarit, avec des rapports de reassignation de
   2,76 et 2,68.** Cela veut dire que le resultat « l'etiquette produit le gabarit » n'est pas
   propre au langage : un predicteur statistique sur les seules demographies fait pareil. Est
   ce un affaiblissement de la these, ou au contraire sa demonstration, puisque c'est
   exactement l'imputation par l'esperance de la section 2 ? Je penche pour la seconde, mais
   la phrase du papier doit alors cesser de dire « les modeles de langage » et dire « toute
   methode qui conditionne sur l'etiquette seule ».

6. **`PMM k=10` est du cote de la personne, 59,6 pour cent du plancher humain, devant C3.**
   Une methode d'imputation classique par tirage chez un donneur porte donc la personne mieux
   que notre agent sans etiquette. C'est cohérent avec a35, qui la trouve deja non dominee,
   mais c'est desagreable a ecrire a cote d'un papier sur la simulation par modele de langage.
   Comment le presente-t-on ?

---

## 13. Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
.venv/bin/python analyses/a44_mesures.py --replicats 200 --bootstrap 1000 --permutations 200
.venv/bin/python analyses/a44_structure.py --replicats 50
.venv/bin/python analyses/a44_figure.py
```

Duree mesuree : 4 148 secondes pour `a44_mesures.py`, environ 300 pour `a44_structure.py`,
quelques secondes pour la figure. Les caches `/tmp/a25-matrices.pkl`, `/tmp/a28-foret.npy` et
`/tmp/a35-methodes.pkl` doivent exister ; ils sont produits par a25, a28 et a35 et ne sont
pas recalcules ici. Graine unique `20260908` partout. Le script s'arrete si l'un des deux
controles bloquants echoue.

---

## 14. Fichiers produits

| fichier | contenu |
|---|---|
| `resultats/a44-preenregistrement.md` | le preenregistrement, horodate avant tout calcul |
| `resultats/a44-controles.csv` | les deux controles bloquants et les taux hors nomenclature, 22 lignes |
| `resultats/a44-replis-segments.csv` | taux de repli et fidelite des marginales par condition et segmentation, 36 lignes |
| `resultats/a44-quantites.csv` | les sept quantites, population contre nul, avec IC bootstrap, 324 lignes |
| `resultats/a44-verdicts.csv` | le verdict preenregistre sur Q5, 26 lignes |
| `resultats/a44-permutation.csv` | les trois proprietes de Yuan transposees, 36 lignes |
| `resultats/a44-rarete.csv` | Q6 et Q7 en detail, avec les deux lifts, 36 lignes |
| `resultats/a44-structure-par-finesse.csv` | l'exces de correlation a cinq niveaux de conditionnement, 90 lignes |
| `resultats/a44-figure-generateur-nul.png` et `.svg` | la figure |
| `analyses/a44_commun.py` | generateur nul, sept quantites, permutation, controles |
| `analyses/a44_mesures.py` | le run principal |
| `analyses/a44_structure.py` | le complement descriptif par finesse de conditionnement |
| `analyses/a44_figure.py` | la figure |
