# a7. Le transport de variance a somme constante : premier prototype, et son echec

## Errata du 8 septembre 2026

Les deux objections bloquantes que `a17-relecture-adverse.md` porte contre ce rapport, ses
sections 3.1 et 3.2, ont ete traitees par un recalcul complet dans
`resultats/a20-transport-de-variance-v2.md`, script `analyses/a20_transport_variance_v2.py`.
Le corps du present rapport n'est pas reecrit : il reste lisible tel qu'il a ete rendu le
7 septembre. Ce qui suit dit ce qui tient, ce qui tombe, et ou lire la version corrigee.
Aucun script existant n'a ete modifie ; a20 importe a7 tel quel, memes graines, memes plis.

**E1. L'estimateur n'etait pas invariant sous l'operateur. Le diagnostic de a17 est
confirme, sur les trois mesures et pas seulement sur l'entropie.** Section 3, "Robustesse a
la mesure". A lambda 0 l'operateur annule l'information mutuelle empirique par construction ;
le ratio inter estime vaut -0,136 en entropie, **-0,104 en Gini Simpson** et **-0,058 en
variance ordinale**, contre une demi largeur d'intervalle bootstrap de 0,011 a 0,019
[MESURE, `a20-lambda0-controle.csv`]. Changer de mesure ne suffisait donc pas. Le correctif
retenu par a20 est un residu de permutation **recalibre a chaque lambda et apparie a la
structure de l'operateur** : on permute les etiquettes de segment puis on applique le meme
transport au meme lambda. Ce residu ramene le terme inter a 0,000 a lambda 0 sur les trois
mesures, et se raccorde exactement au residu de permutation de a1 a lambda 1. La lecture
litterale de la correction de a1, permuter sur la population deja transportee, n'ameliore
rien et aggrave legerement, parce qu'elle rend au tableau croise le bruit multinomial que le
transport venait de retirer [MESURE].

**E2. Le tableau du critere 1 change, mais sa conclusion tient.** Section 3. Avec
l'estimateur corrige et lambda recalibre, mesure principale Gini Simpson, axe ideologie :
composite 2,154 vers **1,053** [0,968 ; 1,145] ; enquete 2,516 vers **0,908** [0,821 ; 0,995] ;
entretien 2,822 vers **1,016** [0,898 ; 1,137] ; `v8` 8,118 vers **0,977** [0,861 ; 1,111]
[MESURE, `a20-avant-apres.csv`]. La phrase "pour trois des quatre conditions, l'intervalle
apres transport contient 1" **reste vraie**, sous Gini Simpson comme sous l'entropie. La
condition qui echoue est toujours les agents enquete, mais dans l'autre sens : a7 publiait un
sur ajustement a 1,096, a20 mesure une sur correction a 0,908, parce que le lambda calibre
passe de 0,7 a 0,6. La prediction de a17 selon laquelle "le transport est systematiquement
sous applique" n'est pas confirmee : le lambda bouge d'au plus un cran, et dans les deux sens.

**E3. Le plafond publie n'etait pas le plafond a inter nul. a17 section 3.3 a raison.**
Section 3, tableau "intra plafond a lambda 0". Les valeurs 0,943, 0,906, 0,913 et 0,846 sont
lues a lambda 0, ou le terme inter estime vaut -0,13 et non zero. Le plafond a terme inter
strictement nul, `T / (1 - w)`, vaut **0,9364, 0,8997, 0,9066 et 0,8409** [MESURE,
`a20-plafond.csv`]. L'incoherence interne que a17 signalait, `w` egal 0,046 deduit d'un cote
et 0,053 de l'autre, disparait : avec l'estimateur corrige, le plafond calcule et le ratio
intra lu a lambda 0 coincident a la troisieme decimale.

**E4. L'enonce d'impossibilite de la section 0 doit etre coupe en deux.** Section 0 et
section 8. Il melangeait deux affirmations qui n'ont pas le meme statut.

- *Le plafond du seul terme intra depend de la mesure.* Sous l'entropie et sous Gini Simpson,
  sur les 149 items comme sur les 70 items ordinaux, il est en dessous de 1 pour les huit
  couples condition x axe, entre 0,841 et 0,961. **Sous la variance ordinale, sur les 70 items
  ordinaux, il est au dessus de 1 pour quatre couples sur huit**, entre 1,044 et 1,053 : les
  agents entretien et les agents demographiques `v8`, sur les deux axes [MESURE]. a17 comptait
  cinq couples ; la mesure directe en donne quatre, l'ecart portant sur composite x profil
  croise, a 0,991 et non 1,002, parce que la reconstitution de a17 s'appuie sur la valeur a
  lambda 0 et que sur cet axe l'operateur ne transporte que 72,2 pour cent des cellules.
- *Le point (1, 1) reste hors d'atteinte, sous les trois mesures.* L'identite impose que si les
  deux ratios valent 1, le ratio de dispersion totale `T` vaut 1. Or `T` mesure **0,802 a
  0,954** sur les quarante couples condition x axe x jeu d'items x mesure, sans exception
  [MESURE]. La ou le plafond depasse 1, amener le terme intra a 1 exigerait d'abaisser le terme
  inter a 0,45 a 0,51, c'est a dire d'effacer la moitie de l'ecart entre segments que les
  humains presentent reellement. **La conclusion d'impossibilite de a7 est donc juste, mais sa
  demonstration par le plafond du terme intra ne l'etait pas.**

**E5. La phrase "a lambda egal 0, tout ecart entre segments est supprime" est fausse sur le
profil croise.** Section 3. L'operateur ne transporte pas un couple (item, segment) de moins
de 20 personnes. Sur l'axe ideologie, a 7 segments, la couverture est de 1 043 cellules sur
1 043, soit 100 pour cent. Sur le profil croise, a 18 segments, elle est de 1 937 sur 2 682,
soit **72,2 pour cent des cellules et 93,4 pour cent de la population** [MESURE,
`a20-couverture-cellules.csv`]. A lambda 0 il subsiste donc sur cet axe un ecart entre
segments qui est du vrai signal non transporte, et non un artefact d'estimateur.

**E6. Ce qui ne change pas.** L'invariance de la marge, verifiee sur les trois mesures.
L'echec du critere 2 : la baisse d'exactitude reste distinguable de zero pour les quatre
conditions. L'echec du critere A6 : rejoue sous la variance ordinale sur les 70 items
ordinaux, le net de reparation reste negatif dans les 32 lignes mesurees et la correlation de
Spearman entre distances humaines et simulees baisse dans les 16 cas [MESURE,
`a20-m3-critere-a6.csv`]. La cecite de la diversite conservee et de l'accord par paires au
transport. Le temoin de dilatation pure et ce qu'il dit des metriques de LifeMem.
L'aplatissement des axes marginaux quand on corrige sur le profil croise. **Aucune conclusion
sur l'utilite du correctif n'est modifiee par ces errata.**

**Restent ouvertes, non traitees par a20** : a17 section 3.4 pour l'agregat des six axes de
a1, section 3.5 (le rapport ecrit 24 cellules, le fichier en contient 48), section 3.6 (le
temoin de hasard du critere A6 vaut 0,167 et non 0,3497), et les quatre manques de la
section 3.8.

---

**Reponse en une ligne.** Le transport a somme constante ramene bien le gonflement des
ecarts entre segments de 2,13 a 0,92 pour les agents composite, il ne coute que 0,90 point
d'exactitude individuelle, et il **ne peut pas** amener les deux ratios en (1, 1) : la
dispersion totale des agents vaut deja 0,80 a 0,89 fois celle des humains, or un operateur
a somme constante laisse ce total invariant, donc le ratio intra plafonne a 0,94 meme
lorsqu'on annule integralement le terme inter [MESURE]. De plus, les individus que le
correctif deplace ne se rapprochent pas de leur vraie reponse : 1 789 reparations contre
3 195 casses, et la correlation de Spearman entre distances humaines et distances simulees
baisse de 0,706 a 0,672 [MESURE]. Le critere A6 n'est pas satisfait, et le correctif doit
donc etre declare pour ce qu'il est a ce stade : **une astuce de temperature mieux ciblee,
pas une restauration d'heterogeneite**.

Date : 7 septembre 2026. Reproduction : `.venv/bin/python analyses/a7_transport_variance.py`,
environ huit minutes, quatre coeurs, **aucun appel de modele de langage**.

---

## 0. Ce qui change dans la these du projet

PASSATION.md section 5 affirme : *le correctif ne peut pas etre une dilatation de la
variance, ce doit etre un transport de variance a somme constante, de l'inter vers
l'intra*. Cette phrase est **fausse telle qu'elle est ecrite**, et ce rapport le demontre
par l'arithmetique et par la mesure [MESURE].

Soit `w` la part du terme inter dans la dispersion totale des humains, et `T` le ratio de
dispersion totale de la condition simulee sur celle des humains. Un operateur a somme
constante laisse `T` invariant, donc apres correction :

    w * ratio_inter + (1 - w) * ratio_intra = T

Si les deux ratios valaient 1, alors `T` vaudrait 1. Or `T` mesure **0,802 a 0,893** selon
la condition [MESURE]. **Aucun operateur a somme constante ne peut donc atteindre (1, 1),
quel que soit son reglage.** Ce n'est pas un defaut de calibration, c'est une impossibilite.

La formulation correcte est : le correctif doit **transporter** de l'inter vers l'intra
**et** combler le deficit de dispersion totale, soit deux boutons et non un, et le second
n'est pas un transport. La contribution du projet n'est donc pas "le transport plutot que
la dilatation", elle est **"mesurer les deux termes et le total ensemble, ce qu'aucun
correctif publie ne fait"**.

---

## 1. Pourquoi 149 items et non 169

Les deux jeux d'items du projet coexistent : a1 ecarte 8 items purement demographiques et
en garde 169, a2 reprend la liste d'exclusion de Stanford elle meme, recopiee de
`figure2/code/source/new_analysis/analyze_gss_filtered.py`, plus `polviews`, et en garde
149 [CONFIRME, lu dans les deux scripts].

**Le jeu de 149 est retenu ici**, pour trois raisons.

1. La liste de Stanford est un sur ensemble strict des 8 items de a1. Elle retire tout item
   qui redit une information deja fournie a l'agent dans son invite [CONFIRME].
2. Un transport agit sur `p(r | segment)`. Sur un item comme `polviews`, dont la reponse
   **est** l'etiquette de segment, retrecir `p(r | s)` vers `p(r)` detruirait
   mecaniquement l'exactitude sans mesurer quoi que ce soit de la structure des opinions
   [CONFIRME par construction de l'operateur].
3. L'exactitude devient directement comparable au tableau de a2 section 4, calcule sur
   exactement ces 149 items et ces 1 052 personnes.

**Controle de coherence avec a1.** Sur les 149 items et les six axes agreges, les agents
composite mesurent inter 1,806 et intra 0,871, contre 1,753 et 0,885 publies par a1 sur 169
items [MESURE]. Le changement de jeu d'items ne deplace rien de substantiel. Le controle
des humains de la vague 2 tombe en (1,011 ; 1,004) sur les six axes et (1,017 ; 1,004) sur
l'ideologie, intervalles contenant 1 [MESURE].

---

## 2. Le protocole

### 2.1 L'operateur

Pour chaque item `j` et chaque segment `s` d'un axe donne :

    p'(r | s) = lambda * p(r | s) + (1 - lambda) * p(r)

ou `p(r)` est la marge poolee de l'agent sur l'item. Comme `p(r)` est **exactement** la
moyenne des `p(r|s)` ponderee par les effectifs de segment, la marge poolee est invariante :
`H(R)` est conserve, `I(R;S)` diminue et `H(R|S)` augmente d'autant [CONFIRME par
construction].

**Verification numerique** de cette propriete, condition composite, lambda 0,5, axe
ideologie : la somme inter plus intra passe de 1004,632 a 1004,318, soit un ecart de
-0,031 pour cent pour l'entropie, -0,008 pour cent pour Gini Simpson et -0,071 pour cent
pour la variance ordinale [MESURE]. Le residu vient de l'arrondi des effectifs cibles a
l'entier, methode du plus grand reste. La propriete tient.

### 2.2 Qui change de reponse

Retrecir une distribution ne dit pas quels individus basculent. Deux regles, plus un temoin.

- **Naive**, le temoin de la mission : parmi les individus du segment portant une modalite
  excedentaire, on tire au hasard ceux qui basculent, et vers quelle modalite deficitaire.
- **Informee** : on bascule en priorite les individus dont le profil de reponses sur les
  **autres** items rend la nouvelle modalite plus plausible. La plausibilite est
  `log q_i(r)`, ou `q_i` est la distribution des reponses **humaines** a l'item `j` chez
  les 30 personnes du pli d'entrainement dont le profil humain ressemble le plus au profil
  **produit par l'agent** pour la personne `i` sur les items de contexte. C'est la baseline
  B2 de a2, k egal 30, distance de Hamming normalisee, reemployee comme score
  d'appariement et non comme predicteur. L'affectation est un appariement glouton sur le
  gain de plausibilite, sous contrainte des effectifs cibles.
- **Dilatation pure**, temoin ajoute apres coup : meme operateur, mais retrecissement vers
  la loi **uniforme** sur le support de l'item au lieu de la marge poolee, avec un mu
  calibre pour amener le ratio intra a 1. C'est le correctif a un seul bouton. Voir la
  section 6.

**Fait important et il simplifie la lecture.** Les variantes naive et informee produisent
**exactement** les memes effectifs par couple (item, segment). Leurs ratios inter et intra
sont donc rigoureusement identiques : ecart maximal mesure 0,00e+00 [MESURE]. Elles ne
different que par la fidelite individuelle. C'est pour cela que la figure ne trace qu'une
trajectoire par condition, et que le choix de la regle d'affectation ne peut jamais etre
juge sur les ratios.

### 2.3 Ce qui protege contre la fuite

- **Lambda est calibre hors de l'item evalue.** Les 149 items sont repartis en 5 blocs
  aleatoires, graine 20260907. Pour chaque bloc, lambda est choisi sur les 4 autres blocs,
  critere : ratio inter le plus proche de 1 sur les items de calibration. Chaque item est
  evalue une fois et une seule, avec un lambda choisi sans lui.
- **Les voisins sont cherches hors du pli de la personne.** Validation croisee a 5 plis sur
  les 1 052 participants. Aucune reponse d'une personne du pli de test n'entre dans son
  propre score de plausibilite.
- **La verite humaine de l'item evalue n'entre jamais** dans la construction du correctif,
  ni pour le choix de lambda, ni pour le choix des individus qui basculent.

**Stabilite de lambda.** Le lambda retenu est identique sur les 5 blocs dans 6 des 8
couples condition x axe, et differe d'un cran dans les 2 autres [MESURE, `a7-lambda-calibre.csv`].
La calibration generalise. Valeurs : 0,7 pour composite et enquete, 0,6 a 0,7 pour
l'entretien, 0,4 pour `v8`.

### 2.4 Estimateurs

Aucun estimateur n'a ete ecrit pour ce rapport. Sont importes tels quels :
entropie corrigee Miller Madow, Gini Simpson sans biais, variance ordinale par composante
d'analyse de variance, decomposition et agregation depuis `analyses/a1_double_distorsion.py` ;
`profil_diversite`, `exactitude_par_personne`, `bootstrap_personnes` et la distance de
Hamming depuis `analyses/a2_commun.py`. Le bootstrap est recentre de facon additive sur
l'estimation ponctuelle, regle de a1 section 8 point 3. 400 tirages avec remise sur les
participants, le meme tirage servant a toutes les conditions.

---

## 3. Critere 1 : les deux ratios se rapprochent ils de 1 simultanement ?

**Non. L'un y arrive, l'autre ne le peut pas.** Mesure entropie, axe de transport
ideologie politique, lambda calibre hors item, intervalles a 95 pour cent.

| condition | inter avant | inter apres | intra avant | intra apres | total avant | total apres |
|---|---|---|---|---|---|---|
| humains vague 2 (controle) | 1,017 [0,982 ; 1,053] | non transporte | 1,004 [0,999 ; 1,008] | non transporte | 1,004 | non transporte |
| agents composite | 2,129 [2,041 ; 2,217] | **0,924** [0,841 ; 1,006] | 0,833 [0,826 ; 0,840] | **0,892** [0,883 ; 0,899] | 0,893 | 0,893 |
| agents enquete | 2,521 [2,411 ; 2,623] | **1,096** [1,014 ; 1,180] | 0,777 [0,770 ; 0,786] | **0,846** [0,839 ; 0,855] | 0,858 | 0,858 |
| agents entretien (v3) | 2,784 [2,621 ; 2,948] | **0,929** [0,826 ; 1,032] | 0,771 [0,761 ; 0,781] | **0,862** [0,852 ; 0,871] | 0,865 | 0,865 |
| agents demographiques (v8) | 8,319 [7,680 ; 8,958] | **1,087** [0,961 ; 1,212] | 0,436 [0,424 ; 0,449] | **0,788** [0,777 ; 0,798] | 0,802 | 0,802 |

**Le terme inter est corrige, et proprement.** Pour trois des quatre conditions,
composite, entretien et `v8`, l'intervalle apres transport contient 1. Pour l'enquete il
est a 1,096 avec [1,014 ; 1,180], soit un leger sur ajustement qui exclut 1 de peu. Le cas
`v8` est le plus spectaculaire : un facteur 8,3 ramene a 1,09 [MESURE].

**Le terme intra ne peut pas suivre.** Il monte de 0,833 a 0,892 pour composite, de 0,436 a
0,788 pour `v8`, et s'arrete la. La cause est arithmetique, pas empirique.

**Le plafond, chiffre.** A lambda egal 0, tout ecart entre segments est supprime : c'est le
maximum deplacable.

| condition | intra avant | intra plafond a lambda 0 | intra vise | exactitude au plafond |
|---|---|---|---|---|
| agents composite | 0,833 | **0,943** | 1,000 | 0,6396 |
| agents enquete | 0,777 | **0,906** | 1,000 | 0,6134 |
| agents entretien (v3) | 0,771 | **0,913** | 1,000 | 0,6113 |
| agents demographiques (v8) | 0,436 | **0,846** | 1,000 | 0,5056 |

Le poids du terme inter dans la dispersion totale des humains vaut **w = 0,046** sur l'axe
ideologie et **0,057** sur le profil croise [MESURE, deduit de l'identite de la section 0
appliquee aux valeurs a lambda 1 et lambda 0]. Autrement dit, chez les humains, l'ideologie
politique declaree n'explique que **4,6 pour cent** de l'entropie des reponses au GSS. Un
agent qui multiplie ce terme par 2,1 gonfle une tranche de 4,6 pour cent : degonfler cette
tranche jusqu'a sa valeur humaine ne libere que `w * (2,13 - 1) = 5,2` points de dispersion
totale a reverser dans l'intra, ce qui remonte le ratio intra de 0,833 a 0,888. C'est
exactement ce qui est mesure, 0,892 [MESURE]. **Les 10 points d'intra manquants ne sont pas
dans le terme inter. Ils ne sont nulle part : ils n'ont pas ete produits.**

**Robustesse a la mesure.** Gini Simpson donne la meme conclusion : composite passe de
2,156 a 1,001 sur l'inter, de 0,843 a 0,904 sur l'intra, avec un total constant a 0,9087
puis 0,9085 [MESURE]. Le resultat ne depend pas du choix de la mesure de dispersion.

**Effet sur l'agregat des six axes**, celui que publie a1 : composite passe de 1,806
[1,749 ; 1,860] a 1,077 [1,031 ; 1,126] sur l'inter et de 0,871 a 0,889 sur l'intra, en ne
corrigeant que l'ideologie [MESURE]. Corriger un seul axe suffit a ramener l'agregat pres
de 1, ce qui confirme le diagnostic de a1 section 4 : le gonflement est porte par
l'ideologie.

---

## 4. Critere 2 : l'exactitude individuelle, la diversite, l'accord par paires

Exactitude par personne, egalite exacte de modalite, 149 items. L'ecart est teste
**apparie**, en bootstrappant le vecteur des differences personne par personne, 2 000
tirages : deux intervalles qui se chevauchent ne prouvent rien, l'intervalle de l'ecart si.

| condition | variante | exactitude | IC 95 % | ecart apparie | IC de l'ecart | diversite conservee | accord paires |
|---|---|---|---|---|---|---|---|
| humains vague 2 | reference | 0,7950 | [0,7896 ; 0,7999] | plafond | | 1,004 | 0,491 |
| agents composite | avant | 0,6840 | [0,6800 ; 0,6880] | 0 | | 0,893 | 0,539 |
| agents composite | **informee** | **0,6750** | [0,6710 ; 0,6791] | **-0,0090** | [-0,0101 ; -0,0079] | 0,893 | 0,539 |
| agents composite | naive (temoin) | 0,6658 | [0,6620 ; 0,6697] | -0,0181 | [-0,0193 ; -0,0170] | 0,893 | 0,539 |
| agents enquete | avant | 0,6510 | [0,6471 ; 0,6548] | 0 | | 0,858 | 0,554 |
| agents enquete | informee | 0,6446 | [0,6409 ; 0,6483] | -0,0063 | [-0,0074 ; -0,0053] | 0,858 | 0,555 |
| agents enquete | naive | 0,6349 | [0,6313 ; 0,6384] | -0,0161 | [-0,0172 ; -0,0150] | 0,858 | 0,555 |
| agents entretien (v3) | avant | 0,6565 | [0,6526 ; 0,6602] | 0 | | 0,865 | 0,560 |
| agents entretien (v3) | informee | 0,6430 | [0,6391 ; 0,6466] | -0,0136 | [-0,0150 ; -0,0122] | 0,865 | 0,560 |
| agents entretien (v3) | naive | 0,6339 | [0,6306 ; 0,6373] | -0,0226 | [-0,0240 ; -0,0212] | 0,865 | 0,560 |
| agents demographiques (v8) | avant | 0,5592 | [0,5544 ; 0,5642] | 0 | | 0,802 | 0,581 |
| agents demographiques (v8) | informee | 0,5282 | [0,5240 ; 0,5324] | -0,0310 | [-0,0340 ; -0,0279] | 0,802 | 0,581 |
| agents demographiques (v8) | naive | 0,5255 | [0,5218 ; 0,5292] | -0,0337 | [-0,0362 ; -0,0311] | 0,802 | 0,581 |

**Le critere 2 n'est pas satisfait, mais l'echec est petit et il est mesure.** L'exactitude
baisse de 0,63 a 3,10 points selon la condition, et **aucun de ces ecarts ne contient
zero** : la baisse est distinguable, contrairement a ce que le critere autorisait [MESURE].
Elle reste toutefois d'un ordre de grandeur inferieur au deplacement du ratio inter, qui va
de 2,13 a 0,92.

**La regle informee vaut la moitie de la perte.** Sur composite, elle divise la degradation
par deux, -0,0090 contre -0,0181, avec des intervalles disjoints [MESURE]. Le transport
comme appariement individuel est donc strictement meilleur que le transport comme tirage,
et cette difference est le seul acquis positif de ce rapport sur la fidelite individuelle.
Sur `v8` l'ecart entre les deux regles s'efface, -0,0310 contre -0,0337, intervalles qui se
chevauchent : quand l'agent est mauvais au point de bouger 25 750 cellules, savoir vers qui
diriger le changement ne sert plus a grand chose [MESURE].

**La baseline a battre reste debout.** B2, les plus proches voisins humains de a2, obtient
0,6717 sur ces memes 149 items [CONFIRME, a2 section 4]. Apres transport, composite est a
0,6750, toujours au dessus, de 0,3 point seulement. Les agents entretien et enquete
descendent a 0,6430 et 0,6446, c'est a dire **sous** B2, ce qu'ils etaient deja avant le
transport. Le correctif ne renverse aucune comparaison avec les baselines sans modele de
langage.

**Le point le plus derangeant de cette section.** La diversite conservee et l'accord par
paires sont **rigoureusement inchanges** par le transport : 0,893 et 0,539 avant, 0,893 et
0,539 apres, pour les agents composite [MESURE]. C'est la consequence directe de
l'invariance de la marge. Autrement dit, **un relecteur qui n'emploie que les metriques du
champ, diversite d'entropie et indice de Simpson, ne verrait strictement aucune difference
entre l'agent d'origine et l'agent transporte**, alors que le ratio inter est passe de 2,13
a 0,92. C'est l'image en miroir du resultat de a1 : la ou a1 montre qu'une metrique globale
ne voit pas une distorsion, a7 montre que la meme metrique ne voit pas sa correction.

---

## 5. Critere A6 : le gain de variance intra est il informatif ?

**Non. Et c'est le resultat qui condamne le prototype.**

Le journal du correctif enregistre chaque bascule (personne, item, ancienne modalite,
nouvelle modalite). On confronte chaque bascule a la vraie reponse de la personne, vague 1,
et a sa reponse de la vague 2 comme controle.

Reparation : l'agent avait faux et la nouvelle reponse est juste. Casse : l'agent avait
juste et la nouvelle reponse est fausse. Agents composite, axe ideologie.

| variante | verite | bascules | reparations | casses | net | taux de reparation |
|---|---|---|---|---|---|---|
| naive (temoin) | vague 1 | 6 121 | 1 129 | 3 972 | **-2 843** | 0,184 |
| naive (temoin) | vague 2 | 6 121 | 1 072 | 4 067 | -2 995 | 0,175 |
| **informee** | vague 1 | 6 121 | 1 789 | 3 195 | **-1 406** | **0,292** |
| **informee** | vague 2 | 6 121 | 1 818 | 3 196 | -1 378 | 0,297 |
| dilatation (temoin) | vague 1 | 11 198 | 2 149 | 6 954 | -4 805 | 0,192 |

Trois lectures, dans l'ordre de ce qu'elles autorisent.

**La regle informee n'est pas du hasard.** Son taux de reparation est de 0,292 contre 0,184
pour le tirage aleatoire dans le meme segment, sur exactement les memes 6 121 bascules
[MESURE]. Elle repare 1,58 fois plus. La correlation de Spearman entre la part d'items
changes pour une personne et le taux d'erreur de l'agent sur cette personne **change de
signe** : -0,198 pour la regle naive, +0,148 pour la regle informee [MESURE]. Le correctif
informe vise donc bien les individus que l'agent rate.

**Et pourtant il casse plus qu'il ne repare, toujours.** Le net est negatif dans les 24
cellules mesurees, sans exception, pour les quatre conditions, les deux axes, les trois
variantes et les deux vagues de verite [MESURE, `a7-critere-a6.csv`]. La raison est simple
et elle etait previsible : dans un segment, la majorite des individus qui portent une
modalite excedentaire la portent **a juste titre**, puisque l'agent a deja 68 pour cent
d'exactitude. Deplacer des effectifs vers une modalite deficitaire deplace donc surtout des
reponses correctes.

**Le test T2 de la section 1.4 de `exploration/09` echoue.** La correlation de Spearman
entre la distance humaine et la distance simulee, sur les 552 826 paires de participants,
baisse dans les 24 cas :

| condition | avant | naive | informee | dilatation |
|---|---|---|---|---|
| agents composite | 0,7062 | 0,6834 | **0,6715** | 0,6565 |
| agents enquete | 0,7373 | 0,7276 | **0,7181** | 0,7095 |
| agents entretien (v3) | 0,5863 | 0,5637 | **0,5447** | 0,5463 |
| agents demographiques (v8) | 0,3754 | 0,2956 | **0,2490** | 0,2754 |

Le critere de la fiche etait : si la variance augmente et la correlation monte,
l'intervention capture de la vraie heterogeneite ; si elle stagne ou baisse, c'est une
astuce de temperature deguisee et il faut le dire. **Elle baisse.** On le dit.

**La vague 2 confirme que ce n'est pas un artefact de vague.** Les chiffres contre la vague
2 sont a moins de 2 pour cent de ceux contre la vague 1, dans les deux sens [MESURE]. Le
correctif n'est pas en train de rater une cible instable, il rate une cible stable.

**Un piege a signaler pour les lecteurs presses.** La correlation entre le taux de
changement d'un item et le taux d'erreur de l'agent sur cet item vaut +0,343 [MESURE], ce
qui a l'air d'un bon signe : le correctif travaille la ou l'agent se trompe. Mais elle est
**identique** pour la regle naive, qui detruit la fidelite. C'est une propriete de
l'operateur de retrecissement, pas de la regle d'affectation, et elle ne prouve rien sur
l'utilite du gain de variance. Ne pas la citer comme un resultat favorable.

---

## 6. Le temoin a un seul bouton, et ce qu'il dit de LifeMem

LifeMem, Wang et al., arXiv 2608.19621, publie le 20 aout 2026, corrige explicitement
l'identity essentialism et publie un ecart intra groupe reduit de 22 pour cent et une
divergence KL reduite de 30 pour cent [CONFIRME, cf. `resultats/a10-verification-sources.md`
section 3.a]. **Il ne republie jamais le terme inter apres correction et ne formule aucune
contrainte de somme constante** [CONFIRME par absence dans le papier]. On ne peut donc pas
savoir, en le lisant, s'il a deplace de la variance ou s'il en a cree.

Ce que ce papier ne mesure pas, on le mesure ici sur un temoin construit expres : meme
operateur, mais retrecissement vers la loi **uniforme**, avec un mu calibre par bloc
d'items pour amener le ratio intra a 1. C'est l'analogue mesurable d'un correctif a un seul
bouton qui vise la dispersion interne.

| condition | mu | inter avant | inter apres | intra avant | intra apres | **total avant** | **total apres** | exactitude | ecart apparie |
|---|---|---|---|---|---|---|---|---|---|
| agents composite | 0,8 | 2,129 | 1,141 [1,051 ; 1,234] | 0,833 | **1,028** [1,018 ; 1,037] | **0,893** | **1,033** | 0,6533 | -0,0307 [-0,0324 ; -0,0290] |
| agents enquete | 0,8 | 2,521 | 1,349 [1,260 ; 1,426] | 0,777 | **0,990** [0,981 ; 1,000] | 0,858 | 1,007 | 0,6259 | -0,0251 |
| agents entretien (v3) | 0,8 | 2,784 | 1,505 [1,373 ; 1,647] | 0,771 | **0,995** [0,983 ; 1,007] | 0,865 | 1,019 | 0,6244 | -0,0321 |
| agents demographiques (v8) | 0,6 | 8,319 | 2,282 [2,067 ; 2,500] | 0,436 | **0,982** [0,970 ; 0,995] | 0,802 | 1,043 | 0,4888 | -0,0704 |

**Trois conclusions, et la deuxieme est inconfortable pour le projet.**

1. **Un correctif a un seul bouton peut afficher un ratio intra parfait.** Les quatre
   conditions arrivent entre 0,982 et 1,029 sur l'intra [MESURE]. Un papier qui ne publie
   que ce terme, comme LifeMem, presenterait ces chiffres comme une reussite complete.
2. **Le total, lui, deborde.** Il passe de 0,893 a 1,033 pour composite et de 0,802 a 1,043
   pour `v8` [MESURE]. La dispersion n'a pas ete deplacee, elle a ete **fabriquee**, et en
   quantite suffisante pour depasser le niveau humain. Le ratio inter, lui, reste a 1,14 a
   2,28 : le gonflement entre segments **n'est pas corrige**, il est seulement dilue dans un
   total plus grand. C'est exactement le mecanisme de compensation que a1 documente, en
   sens inverse.
3. **Le cout individuel est trois fois celui du transport.** -0,0307 contre -0,0090 pour
   composite [MESURE], et un net de reparation de -4 805 contre -1 406, avec un taux de
   reparation de 0,192 contre 0,292. Le temoin degrade la diversite mesuree aussi : l'accord
   par paires tombe a 0,475 contre 0,491 chez les humains, c'est a dire qu'il **depasse**
   l'heterogeneite humaine [MESURE].

Ce temoin ne prouve rien sur LifeMem lui meme, qui emploie un tout autre mecanisme et un
autre jeu de donnees [HYPOTHESE sur la transposition]. Il prouve que **la metrique publiee
par LifeMem ne permet pas de distinguer un transport d'une fabrication de variance**, et
que la publication conjointe des deux termes et du total est la seule facon de trancher.
C'est la contribution qui reste disponible.

---

## 7. Critere 4 : ce qui arrive aux autres axes quand on corrige sur un seul

Ratio inter, mesure entropie, avant et apres transport informe. `a7-par-axe.csv`.

| condition | transport sur | genre | race | ideologie | age | education | profil croise |
|---|---|---|---|---|---|---|---|
| agents composite | avant | 1,27 | 1,63 | **2,13** | 1,23 | 1,39 | 1,89 |
| | ideologie | 1,14 | 1,42 | **0,92** | 1,20 | 1,43 | 1,06 |
| | profil croise | 0,74 | 1,00 | 1,46 | 1,19 | 1,35 | **1,08** |
| agents enquete | avant | 0,87 | 1,38 | **2,52** | 0,82 | 1,12 | 2,06 |
| | ideologie | 0,79 | 1,05 | **1,10** | 0,76 | 1,10 | 1,08 |
| | profil croise | **0,39** | **0,60** | 1,49 | 0,75 | 1,05 | **0,92** |
| agents entretien (v3) | avant | 1,36 | 1,78 | **2,78** | 1,26 | 1,35 | 2,44 |
| | ideologie | 1,23 | 1,38 | **0,93** | 1,15 | 1,33 | 1,08 |
| | profil croise | 0,63 | 0,79 | 1,55 | 1,15 | 1,28 | **1,09** |
| agents demographiques (v8) | avant | 0,99 | 4,06 | **8,32** | 3,22 | 0,42 | 6,26 |
| | ideologie | 0,53 | 3,38 | **1,09** | 2,97 | **0,26** | 1,30 |
| | profil croise | **0,08** | 0,51 | 2,86 | 2,72 | 0,25 | **1,07** |

**Corriger sur l'ideologie est le choix le moins destructeur.** Le profil croise, qui
contient l'ideologie, est ramene de 1,89 a 1,06 pour composite sans avoir ete cible, et le
genre et l'age restent au voisinage de leur valeur d'origine [MESURE]. C'est coherent avec
a1 section 4 : l'axe qui porte le gonflement est bien l'ideologie, et le corriger corrige
l'essentiel.

**Corriger sur le profil croise casse les axes marginaux.** Pour les agents enquete, le
genre tombe de 0,87 a 0,39 et la race de 1,38 a 0,60 [MESURE] : ces axes etaient deja au
voisinage de 1 ou en dessous, et le transport les enfonce. La cause est mecanique : le
profil croise a 18 segments, retrecir a l'interieur de chacun d'eux efface aussi les ecarts
des axes qui le composent. **Un transport sur une partition fine n'est pas une correction
locale, c'est un aplatissement.**

**Le cas `v8` merite d'etre isole.** Corriger l'ideologie fait passer l'education de 0,42 a
0,26 [MESURE]. Cet axe etait deja **sous** 1, c'est a dire que l'agent y ecrasait les
ecarts au lieu de les gonfler ; le correctif l'ecrase davantage. Le transport n'a aucun
mecanisme pour distinguer un axe gonfle d'un axe deja ecrase : il retrecit tout ce qui
correle avec l'axe cible.

**Consequence de protocole.** Tout transport doit etre publie avec le tableau complet des
axes, y compris ceux qu'on n'a pas cibles. Un rapport qui ne montrerait que l'axe corrige
presenterait un succes qui n'existe pas.

---

## 8. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise.** Sur le GSS et le paquet de replication de Stanford, un retrecissement des
distributions conditionnelles au segment vers la marge poolee, calibre sur des items
disjoints de ceux qui l'evaluent, ramene le gonflement des ecarts entre segments de 2,1 a
8,3 vers l'intervalle 0,92 a 1,10, et l'intervalle a 95 pour cent contient 1 pour trois des
quatre conditions [MESURE]. La marge globale est preservee a moins de 0,1 pour cent, ce qui
fait de cet operateur un transport et non une dilatation [MESURE]. Le cout en exactitude
individuelle est de 0,63 a 3,10 points selon la condition.

**Autorise, et c'est le resultat le plus utile du rapport.** Un operateur a somme constante
**ne peut pas** amener les deux ratios en (1, 1) tant que la dispersion totale de la
population simulee est inferieure a celle des humains. Le ratio de dispersion totale mesure
0,802 a 0,893, donc le ratio intra plafonne a 0,846 a 0,943 meme lorsque le terme inter est
annule integralement [MESURE]. La correction complete demande deux operations de nature
differente, un transport et un comblement du deficit total, et le second n'est pas un
transport. **La formulation de PASSATION.md section 5 doit etre corrigee.**

**Autorise, avec le temoin a l'appui.** Un correctif a un seul bouton qui vise la seule
dispersion intra segment peut afficher un ratio intra de 0,98 a 1,03 tout en portant le
total a 1,01 a 1,04 et en laissant le ratio inter a 1,14 a 2,28 [MESURE]. Publier le terme
intra sans le terme inter et sans le total ne permet donc pas de distinguer un transport
d'une fabrication de variance. LifeMem, arXiv 2608.19621, publie un ecart intra groupe
reduit de 22 pour cent et une KL reduite de 30 pour cent, sans republier le terme inter
apres correction et sans contrainte de somme constante [CONFIRME]. C'est cette lacune de
mesure, et non l'absence de precedent, qui reste disponible pour le projet.

**Autorise, et c'est un argument methodologique fort.** La diversite conservee et l'accord
par paires, les deux metriques employees par a0 et a2, sont rigoureusement inchanges par le
transport, a la troisieme decimale [MESURE], alors que le ratio inter passe de 2,13 a 0,92.
Les metriques globales du champ sont aveugles a la correction comme elles sont aveugles a la
distorsion.

**Interdit.** Ecrire que le transport de variance restaure la fidelite : il ne la restaure
pas, il la degrade legerement, de 0,63 a 3,10 points, avec des intervalles apparies qui
excluent zero [MESURE]. Ecrire que le gain de dispersion intra est informatif : il ne l'est
pas, le net de reparation est negatif dans les 24 cellules mesurees et la correlation de
Spearman entre distances humaines et simulees baisse dans les 24 cas [MESURE]. Ecrire que
la variante informee resout le probleme : elle divise le cout par deux et ne renverse aucun
signe. Ecrire que le correctif bat une baseline sans modele de langage : apres transport,
composite est a 0,6750 contre 0,6717 pour B2, soit 0,3 point, et les agents entretien et
enquete restent sous B2 [MESURE]. Ecrire "aucun precedent" a propos du retrecissement des
ecarts inter groupes : LifeMem occupe le voisinage depuis le 20 aout 2026 [CONFIRME].
Presenter la correction d'un seul axe comme une correction generale : corriger sur le profil
croise fait tomber le ratio inter du genre a 0,39 pour les agents enquete [MESURE].

---

## 9. Ce que je n'ai pas pu verifier

1. **Si un autre choix de qui bascule renverserait le signe du net de reparation.** La
   regle informee testee ici est un appariement glouton sur un score de plus proches
   voisins humains. Trois pistes n'ont pas ete essayees, faute de temps : un couplage de
   transport optimal exact au lieu du glouton, un score issu d'une regression logistique
   par item plutot que de voisins, et un score qui combinerait plausibilite et incertitude
   de l'agent. **Ce que je peux dire est que le glouton informe repare 1,58 fois plus que le
   hasard sans jamais atteindre l'equilibre** [MESURE] ; il faudrait tripler ce facteur pour
   que le net devienne positif, ce qui est un ordre de grandeur, pas un reglage [HYPOTHESE].
2. **Si le deficit de dispersion totale se retrouve sur d'autres jeux de donnees.** Tout ce
   rapport tient sur le GSS et sur un seul pipeline. L'impossibilite de la section 0 est
   arithmetique et vaut partout, mais la valeur numerique de `T`, 0,80 a 0,89, est
   specifique a ce jeu. Sur Twin-2K-500, `T` pourrait etre plus proche de 1, auquel cas le
   transport pur suffirait davantage. **Test : rejouer `a7` sur Twin-2K-500 avec le meme
   code.** [HYPOTHESE]
3. **Si la variante informee importe simplement l'information de B2.** Le score de
   plausibilite vient de voisins humains, donc d'une source d'information exterieure a
   l'agent. Un temoin manque : la meme regle informee avec un score construit **sans aucune
   donnee humaine**, par exemple la coherence interne des reponses de l'agent lui meme. Sans
   ce temoin, on ne peut pas separer ce que le transport apporte de ce que B2 apporte
   [HYPOTHESE].
4. **Le comportement a lambda par item plutot que par bloc.** Un seul lambda est estime par
   bloc de 30 items. Un lambda par item, calibre par validation croisee sur les personnes,
   serait plus fin mais aussi beaucoup plus expose au sur ajustement. Non teste.
5. **Les valeurs numeriques exactes de LifeMem sur nos mesures.** Le temoin de dilatation
   est un analogue construit par nous, pas une reimplementation de LifeMem, qui exige des
   trajectoires de vie longitudinales indisponibles ici [CONFIRME, a10 section 3.a]. Aucune
   comparaison chiffree directe n'est donc possible et il ne faut pas en fabriquer une.
6. **La sensibilite au seuil d'effectif de cellule.** Un couple (item, segment) de moins de
   20 personnes n'est pas transporte. Ce seuil n'a pas ete balaye. Il affecte surtout le
   profil croise, a 18 segments.

---

## 10. Questions ouvertes pour Simon

1. **Faut il reformuler la these du projet, ou l'abandonner ?** La section 0 montre que "le
   correctif doit etre un transport a somme constante" est faux quand le total est
   deficitaire. Deux reecritures possibles. La prudente : "la correction demande deux
   operations distinctes, un transport et un comblement, et aucune methode a bouton unique
   ne peut faire les deux". L'offensive : "la contribution n'est pas le correctif, c'est la
   mesure qui rend les correctifs comparables". Laquelle tient devant un relecteur ?
2. **Un echec propre sur le correctif, publie comme tel, a t il une valeur dans ce champ ?**
   Ce rapport est un resultat negatif solide : l'operateur le plus naturel echoue, pour une
   raison arithmetique identifiee, et le temoin montre que le correctif concurrent ne
   pourrait pas le savoir avec ses propres metriques. Est ce publiable seul, ou seulement
   comme section d'un papier dont le corps est a1 ?
3. **Le deficit de dispersion totale de 10 a 20 pour cent est il reparable, et par quoi ?**
   Il ne vient pas de la structure entre segments. Il vient de ce que l'agent n'emet pas
   certaines modalites, ou les emet trop rarement. Est ce un probleme de decodage, donc
   traitable par la lecture des logits, ou un probleme de conditionnement ? La reponse
   oriente vers la famille A ou vers la famille B de `exploration/09`.
4. **Faut il continuer a traiter l'ideologie politique comme un axe de segmentation ?** Elle
   porte tout l'effet et elle n'est pas une variable demographique, c'est une attitude auto
   declaree. La reserve de a1 section 4 devient ici une question de fond : si on retire cet
   axe, le probleme du gonflement inter groupes est il encore un probleme ?
5. **Le critere A6 doit il devenir un critere d'acceptation du projet entier ?** Il vient de
   disqualifier notre propre correctif. Le faire figurer dans le papier revient a fournir au
   relecteur l'instrument qui condamne la moitie des methodes du champ, la notre comprise.
   Est ce une force ou une imprudence ?

---

## 11. Fichiers produits

| fichier | contenu |
|---|---|
| `analyses/a7_transport_variance.py` | le script rejouable, une commande, aucun appel de modele |
| `a7-figure-transport.png` et `.svg` | trajectoires dans le plan (inter, intra) quand lambda varie, exactitude en couleur, et exactitude en fonction de lambda avec le plancher B2 et le plafond humain |
| `a7-trajectoires.csv` | le balayage complet, 11 lambdas x 4 conditions x 2 axes x 2 variantes x 3 mesures |
| `a7-avant-apres.csv` | avant / apres au lambda calibre, six axes de mesure, intervalles bootstrap, ecart apparie d'exactitude |
| `a7-par-axe.csv` | effet du transport sur les six axes, y compris ceux qu'on n'a pas cibles |
| `a7-critere-a6.csv` | reparations, casses, T2, correlations item et personne, vagues 1 et 2 |
| `a7-lambda-calibre.csv` | lambda retenu par bloc d'items, avec le ratio inter avant et apres sur les items de calibration |
| `a7-dilatation-temoin.csv` | le temoin a un seul bouton, avec le total avant et apres |

Rappel : `.gitignore` exclut `*.csv`, ces fichiers ne seront pas versionnes. Les chiffres
qui comptent sont recopies dans le present rapport, qui l'est. Aucune microdonnee n'a
quitte `data/`.
