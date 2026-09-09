# i3b. Preenregistrement : l'abaque, la norme, la contamination ciblee, le fabricant qui vise la bande

**Ecrit le 8 septembre 2026 a 21 h 05 CEST, avant l'ecriture des scripts `analyses/i3b_*.py` et
avant tout calcul de resultat.** Ce fichier n'est pas modifie apres cette date. Tout ecart entre
ce qui est ecrit ici et ce qui est execute est declare en section 0 du rapport
`resultats/i3b-abaque-et-borne.md`, avec sa raison, sans reecriture du present texte.

Suite directe de `resultats/i3-detecteur.md` (question ouverte 6, limites 2, 3, 5, 6 et 7) et du
mois 1 du programme B de `MOONSHOTS.md`. Zero appel de modele de langage, lecture seule sur
`data/`, quatre coeurs. Aucun fichier existant n'est modifie.

---

## 0. Ce qui a ete regarde avant d'ecrire ce texte, et qui doit etre declare

Trois inspections **structurelles** ont ete faites avant la redaction, sans qu'aucune statistique
de resultat soit calculee. Elles sont declarees ici parce qu'elles ont determine des regles de
protocole.

1. `data/twin2k500/llm_specs/` contient bien les treize configurations annoncees par a6, plus
   `humains_wave4.csv` et `humains_wave1_3.csv`.
2. Sur les 108 items categoriels de la vague 4 de Twin-2K-500, **60 items sont renseignes pour
   les 2 058 sujets** et 48 le sont pour environ la moitie ou le tiers, parce que plusieurs
   experiences sont inter sujets. Le taux global de cellules vides est de 24,1 pour cent, le
   meme pour les quinze conditions (fait deja publie par a6, section 1.4).
3. Parmi ces 60 items complets, 41 sont binaires et 19 ont de 4 a 9 modalites ; le produit des
   nombres de modalites d'un sous ensemble de dix items complets tire au hasard vaut de 1,6e4 a
   1,1e6, donc l'espace des patrons n'est pas sature par 2 058 personnes.

Aucune valeur de A, de B, de C, de polarisation, de puissance ou de taux detectable n'a ete
calculee avant l'ecriture de ce fichier, ni sur le GSS ni sur Twin.

---

## 1. Les cinq questions, figees

1. **L'abaque.** Le plus petit taux de contamination detectable a puissance 80 pour cent, test
   bilateral 5 pour cent corrige, en fonction de la taille du flux, de 300 a 5 000 repondants,
   pour chacun des neuf fabricants de i3.
2. **La norme.** La meme chaine sur Twin-2K-500, autre questionnaire, autres personnes, autres
   auteurs, autres modeles, treize configurations. La bande humaine a t elle les memes deux
   bords et les memes ordres de grandeur ?
3. **La contamination concentree sur un camp**, cas d'une operation d'influence : detection, et
   effet sur l'ecart mesure entre camps.
4. **Le fabricant qui vise la bande** : le construire, mesurer s'il reste vu par une statistique
   gardee en reserve, et dire ce qu'il coute.
5. **La surface d'attaque** : pour chaque fabricant, le deplacement maximal de l'ecart entre
   camps et de trois marginales, atteignable sans depasser le seuil de detection.

---

## 2. Sources, et ce qui est repris sans une ligne modifiee

**GSS.** Les seize matrices de `a44_commun.charger`, sur les 1 052 personnes et les 149 items
d'attitudes, plus les deux matrices d'imputation relues du cache de a35 par `i3_commun.charger`.
Les neuf fabricants sont exactement ceux de i3 : `agents v8`, `agents demographiques (v6)`,
`agents composite`, `C2`, `C3`, `PMM k=10`, `E2 regression contexte tirage`,
`IM m=10 mode des m`, `B0 segment`. Le controle de fausse alarme est `humains vague 2`.

**Twin-2K-500.** Le chargeur `a6_double_distorsion_hors_gss.charger_twin`, importe tel quel,
qui rend les 108 items categoriels de la vague 4, les treize configurations, les deux fichiers
humains et les cinq axes demographiques. Aucune ligne de a6 n'est modifiee ni recopiee.

**Statistiques et generateur nul.** `i3_commun` et, par lui, `a44_commun`, importes tels quels :
codage entier sur la nomenclature ordonnee, generateur nul multinomial par segment, comptage des
patrons distincts, correlation de Spearman residualisee du segment, concentration par segment,
polarisation. `a2_commun` est importe pour `est_manquant`, `en_codes` et `distance_hamming`.
**Aucun de ces fichiers n'est modifie.**

**Segmentation.** GSS : `S_ideo`, les sept niveaux bruts d'ideologie politique, comme i3. Twin :
`QID22`, les cinq niveaux bruts d'opinions politiques, qui est l'analogue exact. Les blocs a
trois niveaux, gauche, centre, droite, servent uniquement a la polarisation et a la
contamination ciblee, par la regle mecanique de `a44_commun._bloc_ideologie` sur le GSS et de
`a6.bloc_ideologie_twin` sur Twin.

---

## 3. Les statistiques

### 3.1 La famille publiee, trois statistiques, identiques a i3

- **A**, deficit relatif de patrons de reponses distincts par rapport au generateur nul du flux
  lui meme, sur vingt sous ensembles de dix items.
- **B**, exces de correlation moyenne des rangs residualises du segment, moins le meme exces sur
  le nul du flux.
- **C**, concentration par segment, part des personnes du segment qui donnent le patron modal du
  segment, sur les memes vingt sous ensembles.

Sur Twin, les vingt sous ensembles de dix items sont tires **parmi les seuls items renseignes
pour au moins 99 pour cent des sujets de reference** ; si moins de vingt items passent ce seuil,
il est abaisse par paliers de 0,05 jusqu'a ce que vingt items passent. B porte sur toutes les
paires d'items ayant au moins 30 repondants communs, comme sur le GSS.

### 3.2 La famille de reserve, declaree ici et jamais publiee comme cible

Deux statistiques, choisies parce qu'elles mesurent une structure que la famille publiee ne
contraint pas, et parce qu'elles ont des couts tres differents pour l'auditeur.

- **R1, structure de correlation a l'ordre trois.** Sur T = 20 000 triplets d'items tires une
  fois pour toutes a la graine du projet, `m_ijk` est la moyenne, sur les personnes dont les
  trois items sont renseignes, du produit des rangs residualises du segment et standardises,
  `z_i z_j z_k`. R1 est la moyenne des `|m_ijk|` sur les triplets ayant au moins 30 personnes
  completes, **moins la meme quantite sur le generateur nul du flux**, exactement comme B.
  Un triplet est retire si l'un de ses items a un ecart type de rang nul. **Cout pour
  l'auditeur : aucun, la matrice de reponses et l'ideologie declaree suffisent.** Sous un modele
  gaussien, ou sous tout modele a dependance purement de paires, l'esperance de `m_ijk` est
  nulle ; R1 mesure donc ce qui ne se lit pas dans la matrice de correlation.
- **R2, distance au plus proche voisin humain.** L'auditeur detient un echantillon humain de
  reference **disjoint du flux**. Pour chaque ligne du flux, la distance de Hamming normalisee,
  sur les cellules renseignees des deux cotes, a la ligne la plus proche de cet echantillon
  (`a2_commun.distance_hamming`, importe tel quel). R2 est la **moyenne** de ces distances ; le
  dixieme percentile est publie a cote, sans test. **Cout pour l'auditeur : de vraies
  microdonnees appariables au questionnaire.**

### 3.3 Les quantites de consequence

- **P, polarisation** : la definition de i3, ecart standardise de rang entre le bloc gauche et
  le bloc droite, moyenne sur les items, signes fixes par les humains purs.
- **Trois marginales**, choisies par une regle mecanique fixee ici : **les trois items dont
  l'ecart standardise de rang entre gauche et droite est le plus grand chez les humains purs**,
  dans l'ordre decroissant. La quantite mesuree sur chacun est **la part de la modalite modale
  humaine**, en points de pourcentage, c'est a dire exactement le nombre qu'un institut publie.

---

## 4. Le reechantillonnage, l'intervalle et le bruit de reference

**Sous echantillonnage sans remise, pivote**, pour les cinq statistiques et pour P. Le
bootstrap avec remise est exclu : i3 a mesure un biais de +0,0056 sur B, soit 6,5 ecarts types
de reference, parce qu'une ligne dupliquee est une co-variation parfaite entre tous les items
que le generateur nul detruit. Le pivot de l'intervalle est **la moyenne des tirages** et non la
valeur de reference, correctif E2 de i3. La valeur du bootstrap avec remise et son biais sont
publies a cote comme controle, sans jamais servir a un test.

**Le bruit de reference a la taille N**, `s0(N)`. Il est estime par sous echantillonnage sans
remise de m = N personnes parmi les 1 052 humains de la vague 1, avec **correction de population
finie** : `s0(N) = ecart_type_du_sous_echantillonnage(N) / racine(1 - N / 1052)`. Le facteur est
la lecture directe de la variance d'un tirage sans remise dans une population finie ; sans lui,
le bruit serait sous estime, d'autant plus que N approche 1 052. Il n'est applique que pour
`N <= 750`, ou il vaut au plus 1,84.

**Validation de la mise a l'echelle**, controle bloquant repris de i3 point 1.6 : pour chaque N
de la grille, K = 40 populations independantes de taille N sont tirees du generateur nul humain,
et le rapport entre l'ecart type de sous echantillonnage corrige et l'ecart type inter
population directement mesure doit tomber **entre 0,7 et 1,4**. Un N qui echoue est publie comme
tel et ses `tau*` sont marques non valides.

**Grille de tailles.** N mesure : 300, 500, 750, 1 052. N extrapole : 1 500, 2 000, 3 000,
5 000. Aucune duplication de personnes n'est employee pour depasser 1 052 : elle est interdite
par l'ecart E1 de i3, qui montre qu'un doublon fabrique du deficit de patrons et de l'exces de
correlation, c'est a dire exactement le signal cherche. **Ce qui exige une seconde population
humaine est donc dit et non contourne.**

---

## 5. Le test, la correction, la puissance

Test **bilateral**, seuil nominal 5 pour cent, comme i3 : deux fabricants sur neuf deplacent A
et B dans la direction opposee a celle des agents, et un test unilateral les laisse passer.

`z` de reference : `(valeur du flux - valeur humaine) / s0(N)`.

**Trois familles declarees, chacune corrigee par Holm.**

- **F1, l'abaque et la surface d'attaque.** L'auditeur reel recoit un fichier et applique les
  trois statistiques : la famille primaire est **les trois statistiques**, `z_Holm(3)` =
  quantile normal de `1 - 0,05 / 6`, soit 2,394. Le seuil de i3, `z_Holm(27)` = 3,113, est
  publie a cote dans chaque tableau pour que les deux rapports soient comparables ligne a ligne.
  Le seuil primaire cite dans le texte est celui de la famille de trois.
- **F2, Twin.** 3 statistiques x 13 configurations = 39 tests, `z_Holm(39)` = quantile normal de
  `1 - 0,05 / 78`.
- **F3, le fabricant qui vise la bande.** 5 tests, les trois publiees plus les deux de reserve,
  `z_Holm(5)` = quantile normal de `1 - 0,05 / 10`, soit 2,576.

**Le plus petit taux detectable `tau*`** est la plus petite racine positive de
`|E[T(tau)] - T(0)| = (z + 0,8416) x s0(N)`, ou la courbe `E[T(tau)] - T(0)` est ajustee par une
regression de degre 2 sans terme constant, comme i3. Le `R^2` de chaque ajustement est publie ;
une courbe dont le `R^2` tombe sous 0,95 voit son `tau*` marque douteux.

**Extrapolation au dela de 1 052.** Elle est faite en deux morceaux, et les deux sont publies.
`s0(N)` est ajuste par une loi de puissance `s0 = c x N^(-p)` sur les quatre N mesures, en
moindres carres sur les logarithmes ; `p` et le `R^2` sont publies. La courbe d'effet
`delta(tau, N)` est testee pour sa stabilite en N : si le rapport entre `delta` a N = 300 et
`delta` a N = 1 052 reste dans [0,8 ; 1,25] pour une statistique, cette statistique est declaree
stable en N et son `tau*` est extrapole ; sinon l'extrapolation est refusee et la case du
tableau porte « exige une seconde population ». **Toute valeur au dela de 1 052 est marquee
[PROBABLE] et jamais [MESURE].**

---

## 6. Le protocole de melange

**GSS**, repris de i3 sans changement : effectif constant, remplacement en place de
`round(tau x N)` personnes par la ligne que la source produit pour cette meme personne,
demographies jamais touchees, masque = intersection du masque humain et du masque de la source.
Taux : 5, 10, 25 et 50 pour cent. `C2` et `C3` sont bornees a 10 pour cent, leur perimetre etant
de 150 personnes. `B0 segment` est regenere a chaque tirage.

**Abaque.** Pour un couple (source, taux, tirage) le flux est construit **une fois** a N = 1 052,
puis sous echantillonne sans remise a chacune des tailles de la grille, en emboitement : le sous
echantillon a 300 est inclus dans celui a 500, lui meme inclus dans celui a 750. Le taux de
contamination du sous echantillon est donc aleatoire autour de `tau` ; sa moyenne et son ecart
type sont publies. Cette regle est choisie pour que la seule chose qui change entre deux tailles
soit la taille.

**Twin.** Meme regle. Reference et fond du flux : **les humains des vagues 1 a 3**. Controle de
fausse alarme : **le retest de la vague 4**, melange aux memes taux comme s'il etait un
fabricant. Les trois configurations qui ne couvrent pas les 2 058 sujets sont melangees
uniquement sur les sujets qu'elles couvrent, et leur taux maximal est borne par
`n_couverts / 2058` : 48,6 pour cent pour `JSON Persona - GPT4.1-mini`, donc taux maximal 25
pour cent ; 75,7 pour cent pour le modele affine et 99,6 pour cent pour
`JSON Persona (Predicted Output) - GPT4.1`, donc taux maximal 50 pour cent.

**Contamination concentree sur un camp.** Les faux repondants sont tires **uniquement dans le
bloc vise**, gauche ou droite. Le taux `tau` reste la part du **flux entier** remplacee, aux
cinq valeurs 2, 5, 10, 20 et 30 pour cent ; un taux qui demanderait plus de personnes que le
bloc n'en contient est declare hors de portee et n'est pas calcule. Le camp primaire est
**droite** ; **gauche** est calcule en second pour les trois fabricants les plus detectables et
les deux les moins detectables. Deux lectures de la detection sont faites et publiees :
**globale**, les trois statistiques sur le flux entier, et **par camp**, les trois statistiques
calculees sur les seules personnes du bloc vise, avec leur propre `s0` a la taille du bloc.

---

## 7. Le fabricant qui vise la bande

**Ce qu'il connait.** Les valeurs humaines publiees de A, B et C, et les marginales publiees de
chaque item a l'interieur de chaque segment `p_{j,g}`, qui sont les tableaux croises que tout
sondage publie. **Il n'a aucune microdonnee.**

**Sa construction, `A* archetypes`, trois parametres.** Pour chaque segment `g`, `m` archetypes
sont tires, chacun etant une ligne complete tiree independamment item par item dans
`p_{j,g}^beta` renormalise. Chaque faux repondant recoit un archetype tire uniformement dans son
segment ; pour chaque item independamment, il garde la reponse de son archetype avec la
probabilite `rho` et tire une valeur fraiche dans `p_{j,g}^beta` avec la probabilite `1 - rho`.
Le masque est celui de la personne remplacee. `m` cree le deficit de patrons, `rho` cree la
correlation residuelle intra segment, `beta` regle la concentration.

**Sa calibration.** Grille `m` dans {2, 3, 5, 8, 12, 20}, `rho` dans {0,10 ; 0,20 ; 0,30 ;
0,40 ; 0,50 ; 0,60}, `beta` dans {0,8 ; 0,9 ; 1,0 ; 1,1 ; 1,2}, deux tirages par point, sur une
population entierement fabriquee. Le point retenu minimise
`max(|A - A_h| / s0(A), |B - B_h| / s0(B))` a la taille du flux de la section 8. La valeur de C
n'entre pas dans le critere : c'est le test de l'affirmation « viser deux statistiques publiees
ne suffit pas ». Une seconde variante, `A* trois cibles`, minimise le maximum sur les trois, et
les deux sont publiees.

**Sa mesure.** `A*` est ensuite traite comme un fabricant de plus : melange aux cinq taux,
teste sur la famille F3 de cinq statistiques, avec `tau*` par statistique.

**L'adversaire qui a des microdonnees, `A** microdonnees`.** Il detient 263 vraies lignes,
disjointes du flux et disjointes de la reference de l'auditeur. Chaque faux repondant copie une
ligne reelle de son segment et resample chaque item avec la probabilite `1 - rho'` dans les
marginales du segment ; `rho'` est calibre sur le meme critere. Il sert a mesurer **le prix de
l'invisibilite du cote de l'attaquant** : de combien les microdonnees reelles abaissent la
detectabilite par la famille de reserve.

**La partition, declaree ici.** Les 1 052 humains sont partages une fois pour toutes, a la
graine du projet, en `H_A` de 526 personnes, fond du flux, `H_B` de 263 personnes, reference
microdonnees de l'auditeur pour R2, et `H_C` de 263 personnes, microdonnees volees de
l'adversaire. La section 7 travaille donc a **N = 526**, et la bande de reference de A, B, C, R1
et R2 y est calculee par 300 partitions aleatoires independantes du meme type.

---

## 8. La surface d'attaque

Pour chaque fabricant et chaque taille de flux, `tau_max` est le plus grand taux auquel le
fabricant reste sous le seuil de detection, c'est a dire `tau*` de la meilleure des trois
statistiques publiees sous `z_Holm(3)`. Le deplacement maximal non detecte est la valeur des
quantites de consequence a `tau_max`, lue sur l'ajustement quadratique de chaque quantite contre
le taux :

- l'ecart entre camps `P`, en facteur de la valeur humaine et en points ;
- les trois marginales declarees, en points de pourcentage.

Le tableau est publie pour N = 300, N = 1 052 et, quand l'extrapolation est acceptee, N = 5 000.
Un fabricant dont `tau*` depasse 100 pour cent est declare **jamais detecte** et son deplacement
maximal est lu a 50 pour cent, le plus haut taux mesure.

---

## 9. Les controles bloquants

1. Part de cellules renseignees mais hors nomenclature, seuil 0,5 pour cent, sur chaque source
   des deux jeux.
2. Cellules perdues par l'intersection des masques, seuil 0,5 pour cent, sur les seules lignes
   ou la source existe.
3. Taux de repli du generateur nul, qui doit rester nul sur les deux segmentations.
4. Le flux a taux 0 egale la population de fond, ecart exact de 0 cellule.
5. Melange de la population de fond avec elle meme, ecart exact de 0 cellule, aux cinq taux.
6. Validite de la mise a l'echelle du sous echantillonnage a chaque N, section 4.
7. **Reproduction de i3 a N = 1 052 sur le GSS** : A, B et C des humains purs et des neuf
   sources pures doivent retomber a moins de 0,005 des valeurs publiees dans les tableaux 1 et 5
   de `i3-detecteur.md`. C'est le controle qui dit que i3b est bien la meme chaine.
8. **Reproduction de a6 sur Twin** : le nombre de sujets, d'items et de configurations, et le
   taux de cellules vides, doivent egaler ceux publies par a6 section 1.4.
9. Le controle de fausse alarme, `humains vague 2` sur le GSS et le retest de la vague 4 sur
   Twin, ne doit etre signale a aucun taux inferieur ou egal a 25 pour cent. S'il l'est, la
   section correspondante est publiee comme un echec.

---

## 10. Les sept predictions

**P1.** `tau*` decroit approximativement comme `1 / racine(N)` : le rapport
`tau*(300) / tau*(1052)` tombe entre 1,5 et 2,3 pour au moins six des neuf fabricants, sur la
meilleure de leurs trois statistiques.

**P2.** A 5 000 repondants, `tau*` de `agents v8` passe sous 1 pour cent et celui de
`E2 regression contexte tirage` reste au dessus de 10 pour cent.

**P3.** La bande de Twin a les memes deux bords que celle du GSS : chez les humains de reference,
le deficit de patrons est negatif et l'exces de correlation positif ; et les treize
configurations sont toutes du cote trop pauvre sur A.

**P4.** Les ordres de grandeur ne sont pas transportables : au moins une configuration de Twin a
un `tau*` inferieur a 5 pour cent, et le rapport entre le `tau*` de la pire et de la meilleure
configuration depasse 3.

**P5.** La contamination concentree sur un camp est detectee a un taux **total** plus eleve que
la contamination uniforme par la lecture globale, et a un taux total plus **bas** par la lecture
a l'interieur du camp vise ; et elle deplace l'ecart entre camps plus fortement, a taux total
egal, que la contamination uniforme.

**P6.** Le fabricant qui vise la bande est constructible **sans microdonnees reelles** : il
existe un point de la grille qui met A et B a moins d'un `s0` des valeurs humaines. Il reste
detectable a moins de 25 pour cent de contamination par au moins une des deux statistiques de
reserve.

**P7.** Le prix de l'invisibilite est croissant avec la difficulte de detection : le fabricant au
`tau*` le plus grand permet le plus grand deplacement non detecte de l'ecart entre camps ; et ce
deplacement reste sous 10 pour cent de la valeur humaine pour tous les fabricants a N = 1 052.

---

## 11. Ce que ce plan ne pourra pas dire, ecrit avant de le lancer

1. Aucun fichier reel a contamination documentee n'entre ici. Tout est simulation de
   contamination, comme dans i3.
2. Une seule population humaine de reference par jeu, et c'est elle qui sert de fond. Les `tau*`
   restent optimistes d'une quantite non mesuree, sauf dans la section 7 ou la partition en
   trois rend la reference de R2 reellement externe au flux.
3. Au dela de 1 052 sur le GSS et de 2 058 sur Twin, rien n'est mesure. L'extrapolation est une
   loi de puissance sur quatre points et une hypothese de stabilite testee, pas une mesure.
4. Le fabricant qui vise la bande est le notre. Un adversaire reel peut faire mieux, et la borne
   publiee est un majorant de ce que **cet** adversaire atteint, pas de ce qui est atteignable.
5. Rien sur le texte libre, rien sur l'identite, rien sur la coordination des comptes.

---

## 12. Sorties prevues

`analyses/i3b_commun.py`, `i3b_abaque.py`, `i3b_twin.py`, `i3b_camp.py`, `i3b_adversaire.py`,
`i3b_surface.py`, `i3b_figures.py`.

`resultats/i3b-controles.csv`, `i3b-reference-par-taille.csv`, `i3b-abaque.csv`,
`i3b-abaque-extrapolee.csv`, `i3b-twin-reference.csv`, `i3b-twin-abaque.csv`,
`i3b-camp-detection.csv`, `i3b-camp-polarisation.csv`, `i3b-adversaire-calibration.csv`,
`i3b-adversaire-detection.csv`, `i3b-surface-attaque.csv`.

`resultats/i3b-figure-abaque.png` et `.svg`, `i3b-figure-bande-deux-jeux.png` et `.svg`,
`i3b-figure-surface-attaque.png` et `.svg`.

`resultats/i3b-abaque-et-borne.md`, le rapport.

Graine unique du projet : **20260909**.
