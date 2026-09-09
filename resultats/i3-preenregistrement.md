# i3. Preenregistrement : detecter et quantifier une population synthetique dans un flux de reponses fermees

**Ecrit le 8 septembre 2026 a 19 h 12 CEST, AVANT le moindre calcul, avant l'ecriture des
scripts `analyses/i3_*.py`, et avant tout chargement de matrice.** Ce fichier n'est pas
modifie ensuite. Tout ecart au plan ci dessous sera declare, numerote et justifie dans la
section 0 du rapport `resultats/i3-detecteur.md`, comme a44 l'a fait pour ses trois ecarts.

Aucun appel de modele de langage. Lecture seule sur `data/`. Aucun fichier existant n'est
modifie. Quatre coeurs. Graine `20260909`.

---

## 1. La question, posee de facon falsifiable

Un institut recoit un fichier de reponses a un questionnaire ferme. Il ne dispose d'aucune
etiquette de provenance par repondant, d'aucun exemple etiquete pour entrainer un
classifieur, et d'aucun texte libre. Il dispose des reponses et des demographies declarees.

**Q1.** Existe t il une statistique calculable sur ce seul fichier dont la valeur sur un
flux pur humain est connue avec sa marge, et qui bouge assez quand une part `tau` du flux
est fabriquee pour que l'ecart soit decidable ?

**Q2.** Si oui, a partir de quel `tau` et pour quel type de fabrication ?

**Q3.** Peut on renverser la courbe et estimer `tau` sans connaitre le type de fabrication ?

**Q4.** Ou est la borne : quels fabricants restent invisibles ?

---

## 2. Le materiau, fige

**Le fond humain.** Les 1 052 personnes de la vague 1 du GSS, 149 items, exactement le
perimetre de a2, a25, a28, a35 et a44. Les demographies declarees, les items, les
nomenclatures et le codage entier sont ceux de `a44_commun` (`alphabet`, `coder`), importes
sans une ligne modifiee.

**La segmentation.** `S_ideo`, les sept niveaux bruts d'ideologie politique, seule
segmentation retenue. Justification ecrite d'avance : a44 section 1 point 6 mesure
0,0 pour cent de repli du generateur nul sous `S_ideo` et 7,1 a 64,3 pour cent sous `S_fin`.
Une segmentation qui vide le nul de son conditionnement biaiserait mecaniquement le
detecteur vers la detection. `S_fin` n'est pas employee.

**Les neuf sources synthetiques**, toutes deja produites par des rapports anterieurs, aucune
recalculee ici :

| source | famille | d'ou elle vient |
|---|---|---|
| `agents v8` | modele a etiquette ideologique | six conditions de Stanford, archive OSF t6g7k |
| `agents demographiques (v6)` | modele a demographies | idem |
| `agents composite` | modele riche | idem |
| `C2` | nos agents, etiquette, 150 personnes | run local a5 |
| `C3` | nos agents, sans etiquette, 150 personnes | run local a5 |
| `PMM k=10` | imputation par tirage | a35, cache `/tmp/a35-methodes.pkl` |
| `E2 regression contexte tirage` | imputation par tirage, une imputation stochastique, c'est a dire une des `m` imputations d'une imputation multiple | a35 |
| `IM m=10 mode des m` | imputation multiple, agregee par le mode | a35 |
| `B0 segment` | **adversaire nul** : un faux repondant dont chaque reponse est tiree independamment dans la marginale de son item **a l'interieur de son segment ideologique**, marginales estimees sur les humains de la vague 1 | construit ici par `a44_commun.tirer_nul` applique a la matrice humaine, sans une ligne modifiee |

`B0 segment` est l'adversaire du point 4 de la mission : il n'est pas un modele, il est le
generateur nul du flux humain lui meme. Il a exactement les marginales par segment des
humains et aucune structure individuelle.

---

## 3. Construction du flux, figee

**Regle de melange : remplacement en place, effectif constant.** Le flux compte toujours
`N = 1 052` lignes. Au taux `tau`, on tire sans remise `round(tau * N)` personnes, et pour
chacune la ligne de reponses humaine est remplacee par la ligne de la source synthetique
**pour la meme personne**, c'est a dire par la reponse que la source produit pour ce profil
demographique. La colonne des demographies declarees n'est jamais touchee.

Trois raisons, ecrites d'avance : (1) le nombre de patrons distincts depend de `N`, un flux
a effectif variable rendrait la statistique (a) illisible ; (2) le remplacement en place
laisse la composition par segment strictement invariante, donc aucun signal ne peut venir
d'un desequilibre demographique ; (3) c'est le scenario d'audit reel, un faux repondant
declare un profil et repond.

**Le masque.** La cellule du flux est renseignee si et seulement si la cellule humaine
correspondante est renseignee **et** la cellule de la source l'est. La part de cellules
perdues par cette intersection est un controle bloquant, section 8.

**C2 et C3.** Elles n'existent que sur 150 personnes. Le taux maximal atteignable sans
tirage avec remise, qui dupliquerait des lignes et effondrerait artificiellement le nombre
de patrons distincts, vaut `150 / 1052 = 14,3 pour cent`. **C2 et C3 ne sont donc melangees
qu'aux taux 0, 5 et 10 pour cent**, et cette limite est ecrite ici, avant de savoir ce que
la courbe donne. Aucun taux superieur ne sera produit pour elles par un artifice.

**Les taux.** `tau` dans `{0 ; 5 ; 10 ; 25 ; 50}` pour cent, les cinq de la mission. Aucun
taux intermediaire n'est ajoute : le plus petit taux detectable est obtenu par la formule
de puissance de la section 6, appliquee a la courbe ajustee sur ces cinq points, et non par
un balayage fin.

**Les tirages.** `D = 20` tirages de melange independants par couple (source, taux), graines
fonction de la source, du taux et du numero de tirage, jamais de l'ordre d'execution.

---

## 4. Les trois statistiques, figees

Toutes trois sont calculables sur un flux sans aucune etiquette de provenance et sans aucun
exemple etiquete. Elles ne prennent en entree que la matrice de reponses et la colonne
d'ideologie declaree.

**(a) Deficit de patrons de reponses distincts.** Definition de a44 section 4.1, reprise
sans retouche via `a44_commun.sous_ensembles_items` et `a44_commun.patrons_distincts` :
vingt sous ensembles de dix items tires une fois, graine `20260908` de a44 pour que les sous
ensembles soient **exactement ceux de a44**, une ligne portant une cellule vide etant
ecartee du comptage de son sous ensemble. La statistique est le deficit relatif

```
A = patrons(flux) / moyenne_r patrons(nul du flux)  -  1
```

ou le nul du flux est le generateur conditionnellement independant de Yuan transpose,
`a44_commun.lois_par_segment` et `a44_commun.tirer_nul`, **parametre sur le flux lui meme**
et non sur les humains, masque conserve. Reference attendue chez les humains, a44 :
`-6,9 pour cent`. Chez les agents : `-13,8` a `-32,1 pour cent`.

**(b) Exces de correlation inter items residualisee sur la demographie.** Definition de a44
section 4.2, `a44_commun.correlation_items` avec `seg = S_ideo`, sur les 149 items, seuil de
30 personnes communes par paire :

```
B = Q5(flux) - moyenne_r Q5(nul du flux)
```

Reference attendue chez les humains, a44 : `0,0422`. Chez les agents : `0,077` a `0,105`.

**(c) Concentration par segment, le gabarit.** Statistique nouvelle, definie ici avant tout
calcul. Sur les **memes** vingt sous ensembles de dix items que (a), pour chaque segment `g`
de `S_ideo` et chaque sous ensemble `S` : parmi les personnes de `g` dont les dix reponses
de `S` sont renseignees, la part de celles qui donnent le patron le plus frequent du segment.
La statistique `C` est la moyenne sur les sous ensembles de la moyenne sur les segments
ponderee par le nombre de personnes completes. Elle est publiee **brute**, quantite primaire,
et en exces sur son nul, `C - moyenne_r C(nul)`, quantite secondaire.

Une variante de robustesse, declaree ici et non ajoutee apres coup : la meme statistique sur
les **cinq premiers items** de chacun des vingt sous ensembles, qui donne des effectifs
modaux plus grands.

**Nombre de replicats nuls** : `R = 40` par flux. Justification : a44 emploie 200 replicats
pour une seule population ; ici il y a plusieurs centaines de flux, et l'ecart type inter
replicat du nul divise par `racine(40)` sera publie a cote de chaque courbe pour que le
lecteur juge si `R` est suffisant. Si le temps de calcul le permet, `R` sera augmente et
l'augmentation declaree.

---

## 5. La reference humaine et son intervalle

La reference est la valeur des trois statistiques sur le flux pur, `tau = 0`, avec un
intervalle de confiance a 95 pour cent qui represente la variabilite d'echantillonnage d'un
echantillon humain de 1 052 personnes.

**Deux regimes de reechantillonnage, declares d'avance parce que le probleme est connu.**
a44 section 0 ecrit que le bootstrap sur les personnes de Q3 n'a pas de sens : un tirage
avec remise duplique des personnes et fait baisser mecaniquement le nombre de patrons
distincts. Le meme defaut atteint la concentration `C`, qu'une ligne dupliquee gonfle.
Donc :

- **statistique (b)**, exces de correlation : bootstrap classique sur les personnes,
  tirage avec remise, `B = 1 000`, comme a44 ;
- **statistiques (a) et (c)**, sensibles aux doublons : **sous echantillonnage sans remise**
  a `m = N / 2 = 526` personnes, `B = 1 000`, et intervalle **remis a l'echelle de `N` par le
  facteur `racine(m / N) = 0,7071`**, qui est la mise a l'echelle standard du sous
  echantillonnage pour une statistique convergente en `racine(n)`.

**Controle de validite de cette mise a l'echelle**, bloquant, section 8 point 4.

Pour chaque statistique la reference est publiee avec sa valeur, son IC a 95 pour cent, et
l'ecart type de reference `s_0` qui sert a la puissance.

---

## 6. Detection : le test, la correction, et le plus petit taux detectable

**Le test.** Pour un flux observe, la statistique `T` est comparee a la reference humaine.
Le test est **bilateral**, seuil nominal `alpha = 5 pour cent`, soit `z = 1,960`. Le choix du
bilateral est ecrit d'avance et il est motive : l'adversaire `B0 segment` a par construction
un deficit de patrons nul et un exces de correlation nul, donc il tire le flux **vers le
haut** sur (a) et **vers le bas** sur (b), c'est a dire dans la direction opposee a celle
d'un agent. Un test unilateral cale sur la direction des agents serait aveugle a lui par
construction. Les valeurs unilaterales sont publiees en secondaire.

**La famille et la correction.** La famille primaire compte `3 statistiques x 9 sources = 27`
tests, chacun etant le test « la statistique du flux a `tau = 5 pour cent` differe de la
reference humaine ». Correction de Holm sur ces 27 tests. Les couples (source, taux) au dela
de 5 pour cent sont descriptifs et corriges par Benjamini Hochberg a l'interieur de leur
source.

**Le plus petit taux detectable, `tau*`.** Pour chaque couple (statistique, source), la
moyenne de `T` sur les `D` tirages est ajustee en fonction de `tau` par la regression
polynomiale de degre 2 sans terme constant sur `T(tau) - T(0)`, moindres carres ordinaires,
`R^2` publie. `tau*` est la plus petite racine positive de

```
|E[T(tau)] - T(0)|  =  (z_{1 - alpha/2} + z_{0,80}) * s_0  =  (1,960 + 0,8416) * s_0
```

soit le taux au dela duquel un test bilateral a 5 pour cent detecte avec une probabilite de
80 pour cent. Deux versions publiees : `alpha` nominal de 5 pour cent, et `alpha` corrige de
Holm pour la famille de 27, `alpha' = 0,05 / 27 = 0,00185`, soit `z = 3,113`. La seconde est
la valeur a citer.

**Verification empirique.** A cote de `tau*` calcule, la **puissance empirique** est publiee
a chacun des cinq taux : part des `D` tirages dont la statistique tombe hors de l'IC a
95 pour cent de la reference. Si la puissance empirique et `tau*` se contredisent, c'est la
puissance empirique qui est publiee comme resultat et `tau*` qui est declare invalide.

---

## 7. Quantification, et l'aveugle

**L'estimateur.** Pour un couple (statistique, source), la courbe ajustee de la section 6
est inversee : `tau_chapeau = f^{-1}(T_observe - T(0))`, borne a l'intervalle `[0 ; 1]`.
L'erreur est publiee comme l'erreur absolue mediane et l'erreur quadratique moyenne sur les
`D` tirages de chaque taux, calibration et evaluation etant sur la **meme** source, ce qui
est le cas favorable.

**L'aveugle, qui est le vrai cas.** L'auditeur ne connait pas le type de fabrication.
L'estimateur est donc reevalue **en calibration croisee** : la courbe d'une source `s` est
appliquee aux flux d'une source `s' != s`, pour les huit autres sources, et l'erreur est
publiee dans la meme unite. La prediction ecrite d'avance est en section 9.

**Un estimateur agnostique** est aussi publie : la courbe moyenne des sources a modele de
langage, appliquee a toutes les sources. C'est ce qu'un institut ferait sans autre
information.

---

## 8. Controles bloquants, executes et lus avant toute lecture de resultat

1. **Reproduction de a44.** Sur les flux purs, `tau = 0`, et sur les populations
   synthetiques pures, `tau = 100 pour cent` pour les sept sources du perimetre 1 052, les
   statistiques (a) et (b) doivent retrouver les valeurs de a44 tableaux 3 et 4 a moins de
   0,5 point de pourcentage pour (a) et 0,005 pour (b). Un ecart superieur invalide le
   dispositif et le rapport le dit avant toute autre lecture.
2. **Le flux a `tau = 0` est identique aux humains** cellule par cellule, ecart nul exact.
3. **Perte de cellules par l'intersection des masques**, par source. Seuil declare
   0,5 pour cent. Au dela, la source est lue avec la mention explicite que son masque
   differe de celui des humains, et la statistique brute (c) est declaree non comparable
   pour elle.
4. **Validite de la mise a l'echelle du sous echantillonnage.** On genere `K = 60`
   populations independantes de taille 1 052 avec le generateur nul parametre sur les
   humains ; l'ecart type inter population de (a) et de (c) y est directement mesurable.
   On le compare a l'ecart type de sous echantillonnage a `m = 526` calcule sur une seule de
   ces populations et remis a l'echelle par `racine(m / N)`. Seuil declare : rapport entre
   0,7 et 1,4. En dehors, la mise a l'echelle est declaree invalide et les IC de (a) et (c)
   sont publies **a `m = 526` sans remise a l'echelle**, avec la mention que ce sont des IC
   conservateurs.
5. **Le detecteur ne detecte pas la ou il n'y a rien.** Un melange de la population humaine
   avec **elle meme** (source fictive = les humains) a tous les taux doit donner une
   statistique indistinguable de la reference. C'est le controle negatif du dispositif,
   analogue du `B0 tirage` de a44.

---

## 9. Sept predictions, ecrites avant le calcul

Elles sont scorees dans le rapport, tenue ou fausse, sans reecriture.

**P1.** Les trois statistiques separent `agents v8` a `tau = 25 pour cent` et a
`tau = 50 pour cent` sans ambiguite, avec la correction de Holm.

**P2.** Le plus petit taux detectable `tau*` de la meilleure des trois statistiques est
**inferieur a 10 pour cent pour `agents v8`** et **superieur a 25 pour cent pour
`agents composite`**. Motif : a44 donne un deficit de patrons de 32,1 pour cent pour v8 et
de 18,2 pour cent pour composite, contre 6,9 chez les humains, donc un contraste 3,6 fois
plus grand pour v8.

**P3.** `PMM k=10` **n'est pas detectable en dessous de 25 pour cent** par la statistique de
concentration (c), qui est une statistique de gabarit. Motif : PMM recopie des reponses
observees de vraies personnes.

**P4.** `PMM k=10` **est detectable** par la statistique (a), le deficit de patrons, a un
taux plus bas que par (c). Motif : a44 mesure un deficit de 9,8 pour cent pour PMM contre
6,9 chez les humains, contraste faible mais non nul, et un exces de correlation de 0,0558
contre 0,0422.

**P5.** L'adversaire `B0 segment` deplace (a) et (b) **dans la direction opposee** a celle
des agents : le flux contamine parait **plus** divers que son nul et **moins** couple. Il
est donc invisible a un test unilateral cale sur les agents, et visible a un test bilateral
seulement au dela de 25 pour cent.

**P6.** L'estimateur de `tau` en calibration croisee entre familles, un agent a etiquette
calibrant une contamination par imputation ou l'inverse, a une erreur superieure a
15 points de pourcentage, c'est a dire inutilisable. En calibration sur la bonne source,
l'erreur mediane est inferieure a 5 points au dela de `tau = 10 pour cent`.

**P7.** Pour I4 : l'ecart gauche droite mesure **croit** avec le taux de contamination par
`agents v8` et par `C2` et **decroit** avec le taux de contamination par `PMM k=10`,
`E2 tirage` et `B0 segment`. Motif : a38 mesure un facteur d'amplification de 1,62 pour
l'etiquette et 0,52 sans etiquette ; les imputations par tirage regressent vers la
distribution du segment.

---

## 10. I4, la mesure de polarisation, figee ici

Definie avant tout calcul, sur le flux seul. Pour chaque item `j`, `r_j` est le rang moyen de
la reponse dans la population, `g_j` l'ecart standardise des rangs moyens entre le bloc
`gauche` et le bloc `droite` de l'ideologie declaree, regle a trois niveaux de a1 reprise par
`a44_commun._bloc_ideologie` :

```
g_j = ( moyenne_gauche(r_ij) - moyenne_droite(r_ij) ) / ecart_type(r_ij)
```

La polarisation du flux est `P = moyenne_j [ signe_j * g_j ]`, ou `signe_j` est le signe de
`g_j` **mesure sur les humains purs**, ce qui rend `P` signee et d'esperance nulle en
l'absence de polarisation, au lieu de la moyenne des valeurs absolues qui serait biaisee vers
le haut par le bruit. Sont publies `P(tau)` et le facteur `P(tau) / P(0)`, pour les neuf
sources, aux cinq taux, avec l'IC bootstrap de `P(0)`. Un item est retenu s'il a au moins
30 personnes dans chacun des deux blocs.

---

## 11. Ce qui est explicitement hors perimetre

- Aucun appel de modele de langage, donc aucune condition nouvelle, aucun agent nouveau,
  aucune trace nouvelle.
- Aucun jeu reel a contamination documentee : nous n'en avons pas. Toute courbe de ce
  rapport est une simulation de contamination, jamais une mesure sur un flux reellement
  contamine. Cette phrase sera reprise telle quelle dans le rapport.
- Aucun classifieur supervise, aucune verite terrain par personne. La chute d'exactitude
  sous permutation de a44, qui est la mesure qui separe le mieux, **exige** la verite
  terrain par personne et n'est donc pas utilisable par un auditeur : elle n'entre pas dans
  le detecteur, et c'est le fait qui motive ce rapport.
- Aucun fichier existant n'est modifie. Aucune microdonnee n'est ecrite.

---

## 12. Sorties prevues

`analyses/i3_commun.py`, `analyses/i3_melanges.py`, `analyses/i3_figure.py`.

`resultats/i3-controles.csv`, `i3-reference-humaine.csv`, `i3-melanges.csv`,
`i3-puissance.csv`, `i3-quantification.csv`, `i3-polarisation.csv`,
`resultats/i3-figure-detecteur.png` et `.svg`, `resultats/i3-detecteur.md`.
