# a17. Relecture adverse du dossier

Role tenu : relecteur hostile de NeurIPS, PNAS ou Political Analysis. Objectif : trouver avant
lui ce qu'il trouvera. Date : 7 septembre 2026. Aucun fichier existant n'a ete modifie, aucun
appel de modele n'a ete fait, `data/traces/` n'a pas ete touche.

Convention : **[VERIFIE]** si l'objection a ete reproduite par calcul sur les donnees ou par
lecture du code, **[PROBABLE]** si elle vient d'une lecture attentive des rapports sans
recalcul, **[HYPOTHESE]** sinon.

Ce rapport ne conteste pas la valeur du dossier. Il conteste des phrases precises, et il en
propose la reecriture. Deux objections sur trois sont des problemes de redaction ; trois sont
des problemes de protocole qui changent une conclusion.

---

## Sommaire des verifications faites

Calculs rejoues avec `.venv/bin/python`, quatre coeurs, aucun appel de modele :

- exactitude appariee de `gss_v6`, `gss_v7`, `gss_v8` sur quatre jeux d'items differents
  (177, 169, 150, 149), avec intervalle bootstrap sur les personnes ;
- exactitude item par item des six conditions d'agents contre la vague 1, sur les 149 items
  et sur les 29 items ecartes, pour detecter les recopies ;
- consistance test retest humaine sur les quatre memes jeux d'items ;
- identite `total = w x inter + (1 - w) x intra` reconstituee sur les 24 couples
  condition x axe x mesure du fichier `a7-trajectoires.csv` ;
- correlations et correlations partielles de `a8-twin-par-item.csv` ;
- accord `polviews` contre `political_ideology` et `income` contre l'attribut `income` ;
- lecture du code de `a1_double_distorsion.py`, `a2_commun.py`, `a2_baselines_gss.py`,
  `a7_transport_variance.py`, `a8_commun.py`, `a8_familles.py`, `a8_copule.py`,
  `a12_retest_delai.py`.

---

# 1. a1-double-distorsion.md

### 1.1 Le chiffre de 0,07 point et le facteur 13,5 ne sont pas calcules sur le meme jeu d'items. Gravite : bloquante. [VERIFIE]

C'est le resultat presente comme le plus fort du rapport, section 7.3, repris en section 9
et repris mot pour mot dans a13 revendication (b)3.

**Verification.** Les exactitudes 56,21 et 56,28 et l'ecart apparie de 0,07 point viennent du
fichier `figure2/data/new_analysis_summaries/gss_filtered/summary/individual_level.csv`, que
j'ai ouvert : il contient `p_wave1__gss_v7__accuracy = 56,21` et
`p_wave1__gss_v8__accuracy = 56,28`. Ces valeurs sont calculees par les auteurs sur **150
items**. Je l'etablis par un controle independant : la consistance test retest publiee par les
auteurs, 79,5253, se reproduit exactement sur les 150 items de la liste d'exclusion Stanford
(je mesure 79,5253) et pas ailleurs (177 items : 81,2491 ; 169 items : 81,0072 ; 149 items :
79,5002).

Or les ratios 0,437 et 5,907 de la meme ligne de tableau sont calcules par a1 sur **169
items**. Sur ces memes 169 items, l'ecart apparie recalcule sur les 1 052 participants vaut :

| jeu d'items | v7 | v8 | v8 moins v7, apparie, IC 95 % |
|---|---|---|---|
| 177 items | 55,93 | 55,49 | **-0,44** [-0,84 ; -0,03] |
| **169 items (ceux de a1)** | **56,16** | **55,28** | **-0,88** [-1,29 ; -0,45] |
| 150 items (ceux des auteurs) | 56,17 | 56,18 | +0,01 [-0,41 ; +0,46] |
| 149 items (a2, a7, a8, a12) | 56,40 | 55,91 | -0,49 [-0,92 ; -0,04] |

Sur le jeu d'items qui produit le facteur 13,5, les deux conditions **ne sont pas
indistinguables** : l'intervalle exclut zero, et c'est la condition persona qui est la plus
exacte. La phrase "deux conditions dont l'exactitude est strictement indistinguable ont des
ratios inter qui different d'un facteur 13,5" melange deux denominateurs.

Le meme defaut frappe le premier constat de la section 7.3 : l'ecart v6 contre v8 de 1,85
point [1,41 ; 2,29] est un chiffre a 150 items ; sur les 169 items de a1 il vaut 4,14
[3,72 ; 4,53], sur les 149 items 2,26 [1,83 ; 2,68].

**Correction proposee.** Recalculer les exactitudes appariees sur les 169 items du rapport et
reecrire la section 7.3 avec ces valeurs, ou calculer les ratios sur les 150 items des
auteurs ; dans les deux cas le message change de forme, puisque sur 169 items l'argument
devient "l'ecart d'exactitude est de 0,9 point et l'ecart de structure d'un facteur 13,5", ce
qui reste fort mais n'est plus "indistinguable".

### 1.2 Le controle de la vague 2 ne contient pas 1 sur deux mesures sur trois. Gravite : serieuse. [VERIFIE]

Section 3 : "Le controle passe. La vague 2 tombe en (1,003 ; 1,004), les deux intervalles
contiennent 1." Section 9 : "Le controle par reinterrogation des memes humains valide la
methode."

**Verification, dans le fichier produit par le script lui meme, `a1-ratios.csv`** :

| mesure | ratio intra vague 2 | IC 95 % | contient 1 ? |
|---|---|---|---|
| entropie, mesure principale | 1,0043 | [**1,0001** ; 1,0087] | **non** |
| Gini Simpson | 1,0030 | [0,9992 ; 1,0069] | oui |
| variance ordinale | 0,9894 | [0,9795 ; **0,9997**] | **non** |

Le terme inter contient 1 sur les trois mesures. Le terme intra ne le contient pas sur la
mesure principale ni sur la mesure de controle. L'ecart est minuscule, 0,4 pour cent, mais le
rapport se lie lui meme a ce critere : sa limite 4 declare la methode biaisee au motif que,
en gardant les huit items demographiques, l'intervalle du controle "exclut 1". Le meme
critere, applique au calcul principal, echoue deux fois sur trois.

**Correction proposee.** Ecrire "le controle tombe a 0,4 pour cent de 1 sur les trois mesures,
et l'intervalle exclut 1 de justesse pour le terme intra sur deux d'entre elles, ce qui borne
la resolution de la methode a environ un demi pour cent" ; et cesser d'employer l'inclusion
de 1 comme critere binaire de validite.

### 1.3 La difference entre v6 et v8 est mesurable dans l'archive, et elle est banale. Gravite : serieuse. [VERIFIE]

Section 7.4 : "Non etabli non plus. Ce qui differe concretement entre les deux generations.
Le paquet ne contient pas le code de generation."

**Verification.** L'exactitude de chaque condition sur les 29 items que le dossier ecarte dit
exactement ce que chaque agent avait dans son invite. Taux d'accord avec la vague 1 :

| item | v6 | v8 | v7 | composite | retest humain | modalite majoritaire |
|---|---|---|---|---|---|---|
| `polviews` | **0,200** | **0,961** | 0,217 | 0,539 | 0,833 | 0,288 |
| `partyid` | **0,165** | **0,994** | 0,183 | 0,756 | 0,820 | 0,220 |
| `marital` | **0,999** | 0,461 | 0,600 | 0,974 | 0,952 | 0,420 |
| `relig*` | **0,994** | 0,430 | 0,442 | 0,791 | 0,887 | 0,405 |
| `degree*` | **0,998** | 0,267 | 0,419 | 0,894 | 0,913 | 0,389 |
| `income` | **0,994** | 0,454 | 0,413 | 0,422 | 0,634 | 0,516 |
| `zodiac` | **0,999** | 0,062 | 0,081 | 0,883 | 0,975 | 0,092 |
| `hispanic` | **0,999** | 0,863 | 0,894 | 0,981 | 0,974 | non calcule |
| `sex*` | 0,999 | 0,998 | 0,832 | 0,988 | 0,988 | 0,564 |
| `race*` | 0,998 | 0,999 | 0,804 | 0,933 | 0,979 | 0,760 |

Lecture. **`gss_v8` a recu l'ideologie, le parti, la race et le genre, et rien d'autre** : il
les recopie a 96 a 99 pour cent et il est au niveau du hasard sur tout le reste. C'est
exactement l'invite demographique decrite par le papier et citee par a14 section 3.1.
**`gss_v6` a recu un profil d'etat civil riche** : statut marital, veuvage, religion, diplome,
revenu, date de naissance (d'ou le zodiaque a 0,999), origine hispanique, race, genre, et
**pas la politique** : 0,200 sur `polviews` et 0,165 sur `partyid`, c'est a dire **sous la
modalite majoritaire**.

Consequence pour la section 7.5. Le facteur 6,9 entre les deux variantes demographiques et le
facteur 13,5 entre v7 et v8 ont maintenant une explication triviale : la condition qui gonfle
les ecarts sur l'axe ideologique est celle a qui on a donne l'etiquette ideologique. Un
relecteur ecrira : "votre mesure detecte le contenu de l'invite, pas une pathologie cachee".
L'argument de fond survit, parce que l'exactitude ne voit toujours pas cette difference, mais
la formulation "une dimension entiere que leur mesure ne voit pas" doit ceder la place a
"deux conditions dont l'invite differe sur un seul attribut, l'etiquette politique, sont
notees equivalentes par l'exactitude et opposees par la structure".

**Correction proposee.** Remplacer le point "non etabli" de la section 7.4 par ce tableau, qui
etablit le fait sans le code de generation, et reecrire la section 7.5 en nommant la cause.

### 1.4 Le motif d'exclusion des huit items est faux pour la moitie d'entre eux. Gravite : serieuse. [VERIFIE]

Section 1 : "Huit sont ecartes parce qu'ils redisent litteralement un attribut de
segmentation... Un agent demographique a recu ces valeurs dans son invite."

Le tableau ci dessus montre que ni v6 ni v8 n'ont recu `educ*` (0,000 pour les deux), que v8
n'a recu ni `income`, ni `degree*`, ni `reg16`, et que v6 n'a recu ni `polviews` ni `partyid`.
Aucun agent demographique n'a recu les huit. La justification empirique de la limite 4, elle,
tient : en gardant ces items le controle vague 2 tombe a 0,946. C'est le seul motif
defendable.

**Correction proposee.** Remplacer le motif par le motif empirique : "ces huit items sont
ecartes parce que les garder fait echouer le controle de la vague 2, mesure en limite 4 ;
chacun est recopie par au moins une condition d'agent, mais aucune ne les recopie tous".

### 1.5 Les trois mesures ne donnent pas le meme classement. Gravite : serieuse. [VERIFIE]

Section 3 : "Les deux autres mesures donnent le meme classement et le meme signe pour les huit
conditions. La conclusion ne depend pas du choix de la mesure."

Dans `a1-ratios.csv`, sur le terme intra, la variance ordinale classe agents entretien (0,8899)
**au dessus** des agents composite (0,8605), l'inverse de l'entropie (0,8517 contre 0,8846) et
de Gini Simpson (0,8500 contre 0,8962). Le classement des deux meilleures conditions s'inverse.

De meme, la section 9 autorise a ecrire que les mesures globales "restent entre 0,80 et 0,90".
Sur la variance ordinale, la colonne `ratio_dispersion_globale` vaut **0,9623** pour les agents
entretien et **0,9508** pour `v8`, hors de la fourchette annoncee.

**Correction proposee.** Ecrire "le signe des huit conditions est identique sur les trois
mesures ; le classement des deux conditions les plus proches s'inverse sur la variance
ordinale", et donner la fourchette globale mesure par mesure.

### 1.6 Le bootstrap recentre n'est pas le bootstrap de base. Gravite : mineure. [VERIFIE]

Limite 3 : "les distributions bootstrap sont donc recentrees de facon additive sur
l'estimation ponctuelle, ce qui est le bootstrap de base au sens de Davison et Hinkley".

La fonction `recentrer` calcule `v - moyenne(v) + cible`, donc l'intervalle
`[theta + q2,5 - moyenne ; theta + q97,5 - moyenne]`. Le bootstrap de base est
`[2 theta - q97,5 ; 2 theta - q2,5]`, qui **retourne** l'asymetrie au lieu de la conserver.
Les deux coincident si la distribution est symetrique, pas sinon.

**Correction proposee.** Ecrire "intervalle de percentile translate sur l'estimation
ponctuelle", et publier une fois la comparaison avec le bootstrap de base sur la condition la
plus asymetrique.

### 1.7 Le biais residuel de l'estimateur inter est enorme et il est enterre dans une limite. Gravite : serieuse. [PROBABLE]

La meme limite 3 rapporte que la moyenne bootstrap brute du terme inter depasse la valeur
observee de **24 pour cent chez les humains** et de 2 pour cent chez `v8`. C'est une estimation
bootstrap du biais de l'estimateur, pas seulement du bruit. Elle est condition dependante et
elle porte sur la quantite qui sert de denominateur a tous les ratios. Une correction de biais
bootstrap augmenterait les ratios inter au lieu de les reduire : le choix actuel est
conservateur, donc defendable, mais il doit etre presente comme un choix chiffre et non comme
un detail de recentrage.

**Correction proposee.** Ajouter au tableau de la section 3 une colonne "ratio avec correction
de biais bootstrap" et dire en une phrase que la version publiee est la borne basse.

### 1.8 Le silhouette : une coincidence presentee comme une validation. Gravite : mineure. [VERIFIE par lecture croisee de a10 et a13]

Section 5 : "la valeur humaine est retrouvee au centieme pres, -0,020 sur l'ideologie, ce qui
indique que la mesure est bien implementee".

a10 et a13 section 1.1 etablissent que le -0,02 de la litterature porte sur le World Values
Survey, sur des tertiles de statut socio economique, avec une distance euclidienne sur un
codage ordinal standardise. a1 mesure sur le GSS, sur des segments d'ideologie, avec une
distance d'appariement simple. Deux quantites differentes qui tombent sur la meme valeur ne
valident rien : c'est exactement la faute que la section 4 de PASSATION.md interdit.

**Correction proposee.** Supprimer la phrase de validation et ecrire "la valeur humaine
mesuree ici, -0,020, n'est pas comparable au -0,02 publie, qui porte sur un autre jeu, une
autre distance et une autre segmentation".

### 1.9 Ce qu'un relecteur demandera et qui manque

- **Correction pour tests multiples.** Le rapport publie au moins 48 intervalles a 95 pour cent
  pour les ratios, 48 pour le detail par axe et 48 pour le silhouette, sans aucune correction.
  Sur 144 intervalles, sept faux positifs a 95 pour cent sont attendus. La conclusion ne change
  probablement pas, les effets etant enormes, mais l'absence de la phrase se remarque.
- **Puissance.** Aucun calcul, alors que les conclusions "ne sont pas distinguables"
  (composite contre enquete) sont des non rejets.
- **Sensibilite a la graine.** Une seule graine pour la partition, une seule pour le bootstrap.
- **Le chiffre de 4,6 pour cent** de la section 6 est exact : je mesure 4,66 pour cent de
  participants dont l'agent composite est plus fidele a leur vague 1 que ne l'est leur propre
  vague 2, sur les 169 items. [VERIFIE]

---

# 2. a2-baselines.md

### 2.1 La phrase de conclusion contredit la limite 2 du meme rapport. Gravite : serieuse. [VERIFIE par lecture]

Section 4 point 2 et section 10 : "cinq des six conditions d'agents du papier de Stanford sont
battues par du scikit-learn". Section 9 limite 2 : "La comparaison B2 contre agents
demographiques n'a pas de sens ; celle contre agents enquete et entretien en a un."

Les cinq conditions battues sont v3, enquete, v6, v7 et v8. Trois des cinq sont exactement
celles que la limite declare non comparables. La phrase la plus citable du rapport repose donc
a 60 pour cent sur une comparaison que le rapport lui meme invalide. Elle est reprise telle
quelle par a8 section 7.1, qui la declare "non contredite".

**Correction proposee.** Ecrire "B2 bat les deux conditions d'agents nourries au meme type
d'information, entretien et enquete ; les trois conditions pauvres ne sont pas comparables a
B2 et leur defaite ne doit pas etre comptee".

### 2.2 Une fuite subsiste dans les 149 items, et elle vaut 0,28 point. Gravite : serieuse. [VERIFIE]

Section 2.1 retire `polviews` parce qu'il est identique a l'attribut `political_ideology`
(accord 1,0000, que j'ai reproduit). Mais `income` reste dans la cible, alors qu'il est le
seul autre item que a1 avait ecarte et que la liste de Stanford ne couvre pas.

**Verification.** `gss_v6` obtient **0,9943** sur le seul item `income`, contre 0,634 pour le
retest humain et 0,516 pour la modalite majoritaire. C'est une recopie. Aucun autre item des
149 ne presente ce profil : le balayage complet des 149 items x 6 conditions ne remonte que
`income` chez v6 et, plus faiblement, `jew` chez v6.

L'attribut demographique `income` de `demographic_summary.csv` emploie un decoupage different
(accord exact 0,0000 avec l'item), donc B1 n'en profite pas : je mesure B1 a 0,5181 sur cet
item contre 0,5162 pour la modalite majoritaire. La fuite est du cote de l'agent, pas de la
baseline. Effet sur le chiffre publie : v6 passe de 0,5818 a environ 0,5790, soit -0,28 point.

**Correction proposee.** Ajouter `income` a la liste de retrait, ou publier la note "les 149
items contiennent `income`, que la condition `gss_v6` recopie a 99,4 pour cent, ce qui gonfle
son score de 0,28 point".

### 2.3 La deduction sur l'ideologie politique de l'agent demographique etait juste, et a14 l'a corrigee a tort. Gravite : bloquante pour le dossier, favorable a a2. [VERIFIE]

Voir objection 1.3 et la section a14 ci dessous. Le fichier que a2 evalue est `gss_v6`, qui
n'a recu ni ideologie ni parti. La deduction de a2 section 2.1 est **confirmee par la mesure**.
La variante de B1 privee des attributs politiques, 0,5998, est donc bien la comparaison a armes
egales pour v6, et ne doit pas etre requalifiee en "borne basse" comme a14 le recommande.

**Correction proposee.** Conserver la section 2.1 de a2 telle quelle, en remplacant "Deduction,
et c'est une deduction" par "Fait mesure : `gss_v6` obtient 0,200 sur `polviews` et 0,165 sur
`partyid`, sous la modalite majoritaire, tandis que `gss_v8` obtient 0,961 et 0,994 ; l'invite
demographique decrite par le papier correspond a `gss_v8`, pas a `gss_v6`."

### 2.4 La colonne "normalise" n'emploie pas la definition des auteurs. Gravite : mineure. [VERIFIE par a14 section 2.3]

a2 divise deux moyennes. Les auteurs normalisent chaque individu par sa propre consistance puis
moyennent. L'ecart mesure par a1 est de 0,006. Il est negligeable, mais le dossier fait un
point d'honneur a nommer le denominateur.

**Correction proposee.** Ajouter la note "normalisation par le rapport des moyennes ; la
definition des auteurs, individuelle puis moyennee, donne 0,006 de plus".

### 2.5 Les seuils de croisement n'ont pas d'intervalle. Gravite : mineure. [VERIFIE par lecture du code]

Les 145, 180 et 250 repondants viennent d'une interpolation sur huit points, six tirages par
point, sans intervalle publie, et a8 section 8 point 3 signale qu'ils n'ont ete ni confirmes ni
infirmes depuis. Ce sont les chiffres les plus operationnels du rapport ("le nerf du dossier").

**Correction proposee.** Publier l'ecart type deja calcule par le script sous forme
d'intervalle sur le seuil, par bootstrap sur les six tirages.

### 2.6 Ce qui est verifie propre

- L'unite de reechantillonnage du bootstrap est bien la personne, pas la cellule. [VERIFIE,
  `bootstrap_personnes` dans `a2_commun.py`]
- Les conditions d'agents sont bien recalculees sur exactement les 149 items et les 1 052
  personnes qui servent aux baselines : meme matrice, meme masque, meme fonction
  `exactitude_par_personne`. Le denominateur est identique des deux cotes. [VERIFIE,
  `references_llm` dans `a2_baselines_gss.py`]
- L'encodeur des demographies est ajuste sur le seul pli d'entrainement, l'item predit
  n'entre jamais dans la distance de B2, et le codage entier de `en_codes` ne transporte
  aucune information d'une personne a l'autre. [VERIFIE, lecture de `a2_commun.py`]

---

# 3. a7-transport-de-variance.md

### 3.1 L'estimateur n'est pas invariant sous l'operateur, et le biais est plus grand que l'intervalle. Gravite : bloquante. [VERIFIE]

C'est l'objection la plus lourde du rapport, et elle porte sur son resultat central, "l'inter
passe de 2,13 a 0,92, l'intervalle contient 1 pour trois des quatre conditions".

**Verification.** Dans `a7-trajectoires.csv`, a lambda egal 0, le ratio inter estime vaut :

| condition | inter a lambda 0, entropie |
|---|---|
| agents composite | **-0,1362** |
| agents enquete | -0,1352 |
| agents entretien (v3) | -0,1368 |
| agents demographiques (v8) | -0,1169 |

A lambda egal 0, l'operateur force la distribution de chaque segment a etre **exactement** la
marge poolee : l'information mutuelle empirique est nulle par construction. Un estimateur non
biaise devrait rendre zero. Il rend -0,13. La cause est identifiee dans le code lui meme, a la
ligne 1020 de `a7_transport_variance.py` : la correction de Miller Madow soustrait une quantite
calibree sur le bruit d'echantillonnage present a lambda egal 1, alors que le transport
supprime ce bruit en meme temps qu'il supprime le signal, proportionnellement a lambda au
carre. La sur soustraction contamine donc **tous** les lambdas inferieurs a 1, et son ordre de
grandeur, 0,10 a 0,14 en unites de ratio, est **superieur a la demi largeur des intervalles
publies**, qui vaut environ 0,08.

Consequence directe : les valeurs "apres transport" de 0,924, 1,096, 0,929 et 1,087 sont
biaisees vers le bas. Une re inflation grossiere, en ajoutant `(1 - lambda au carre)` fois le
residu mesure a lambda 0, donne respectivement 0,99, 1,17, 1,02 et 1,19. La phrase "pour trois
des quatre conditions, l'intervalle apres transport contient 1" n'est pas etablie.

Consequence indirecte : lambda est calibre en cherchant le ratio inter le plus proche de 1
**avec le meme estimateur biaise**. La calibration s'arrete donc trop tot, et le transport est
systematiquement sous applique.

**Correction proposee.** Recalculer les ratios apres transport avec un estimateur dont le biais
est estime **sur les donnees transportees** (par exemple en permutant les etiquettes de segment
sur la matrice transportee), et republier le tableau de la section 3 ; a defaut, publier la
valeur a lambda 0 comme mesure du residu et donner les ratios corriges en note.

### 3.2 L'impossibilite d'atteindre (1,1) depend de la mesure choisie. Gravite : bloquante. [VERIFIE]

Section 0 et section 8 : "Le ratio de dispersion totale mesure 0,802 a 0,893, donc le ratio
intra plafonne a 0,846 a 0,943 meme lorsque le terme inter est annule integralement." Section 3
ajoute : "Robustesse a la mesure. Gini Simpson donne la meme conclusion."

La troisieme mesure de a1, la variance ordinale, n'est pas testee. Je l'ai reconstituee a
partir de `a7-trajectoires.csv`, en resolvant `T = w x inter + (1 - w) x intra` sur les couples
lambda egal 1 et lambda egal 0 :

| condition | axe | mesure | w | T | plafond intra a inter egal 0 |
|---|---|---|---|---|---|
| composite | ideologie | entropie | 0,046 | 0,893 | 0,936 |
| composite | ideologie | Gini Simpson | 0,050 | 0,909 | 0,956 |
| composite | ideologie | **variance ordinale** | **0,089** | 0,897 | 0,984 |
| composite | profil croise | **variance ordinale** | 0,099 | 0,903 | **1,002** |
| enquete | ideologie | variance ordinale | 0,088 | 0,878 | 0,963 |
| entretien | ideologie | **variance ordinale** | 0,089 | 0,952 | **1,045** |
| entretien | profil croise | **variance ordinale** | 0,097 | 0,955 | **1,057** |
| `v8` | ideologie | **variance ordinale** | 0,089 | 0,954 | **1,047** |
| `v8` | profil croise | **variance ordinale** | 0,096 | 0,962 | **1,065** |

Sur la variance ordinale, le plafond depasse 1 pour cinq des huit couples condition x axe. Sur
cette mesure, **le transport pur suffit** a amener le ratio intra a 1, et l'impossibilite
annoncee disparait. Le rapport a1 emploie trois mesures precisement pour ne pas dependre d'une
seule ; a7 abandonne la troisieme au moment ou elle contredit sa conclusion.

Corollaire sur le chiffre le plus cite du rapport : **w n'est pas 4,6 pour cent**, c'est 4,6
pour cent en entropie, 5,0 pour cent en Gini Simpson et **8,9 pour cent en variance ordinale**.
La phrase "chez les humains, l'ideologie politique declaree n'explique que 4,6 pour cent de
l'entropie des reponses" est correcte telle qu'elle est ecrite, avec le mot entropie ; la
version courte, "4,6 pour cent de la dispersion", ne l'est pas.

**Correction proposee.** Reecrire la section 0 en indexant l'impossibilite sur la mesure :
"sur les deux mesures nominales, entropie et Gini Simpson, le deficit de dispersion totale
interdit d'atteindre (1,1) par transport pur ; sur la variance ordinale, restreinte aux 75
items ordinaux, le deficit est plus faible et le plafond depasse 1 pour la moitie des couples,
ce qui montre que le deficit total est porte par les items nominaux".

### 3.3 Le plafond publie n'est pas le plafond a inter nul. Gravite : serieuse. [VERIFIE]

Le tableau "intra plafond a lambda 0" donne 0,943, 0,906, 0,913 et 0,846. Ces valeurs sont
lues a lambda egal 0, ou le ratio inter estime vaut -0,13 et non 0. Le plafond a inter
strictement nul, calcule par l'identite avec le w reconstitue, vaut 0,936, 0,899, 0,906 et
0,840. La difference est faible mais la phrase "meme lorsqu'on annule integralement le terme
inter" designe un point que le tableau ne contient pas.

C'est aussi ce qui explique l'incoherence interne suivante, qu'un relecteur trouvera en trois
minutes : le w deduit des valeurs a lambda 1 vaut 0,046, celui deduit du plafond publie vaut
0,053. Les deux ne peuvent pas etre justes ensemble.

**Correction proposee.** Publier la ligne "inter a lambda 0" a cote du plafond, et donner le
plafond a inter nul plutot que le plafond a lambda nul.

### 3.4 a7 et a1 ne mesurent pas la meme chose, et le rapport attribue l'ecart aux items. Gravite : serieuse. [VERIFIE par lecture du code]

Section 1 : "Controle de coherence avec a1. Sur les 149 items, les agents composite mesurent
inter 1,806 et intra 0,871, contre 1,753 et 0,885 publies par a1 sur 169 items. Le changement
de jeu d'items ne deplace rien de substantiel."

`a1_double_distorsion.py` soustrait au terme inter le residu de permutation, qui vaut 3 a 15
pour cent pour l'entropie, avant de former le ratio. `a7_transport_variance.py` importe
`agreger` et `decomposer` de a1 mais **n'applique aucune soustraction de residu** : la
verification est directe, la variable `nul` de a1 n'existe pas dans a7 et aucun appel de
permutation n'y figure. Les deux rapports publient donc "le ratio inter des agents composite"
avec deux estimateurs differents, et attribuent l'ecart au seul jeu d'items.

**Correction proposee.** Ecrire "a7 emploie l'estimateur de a1 sans la soustraction du residu
de permutation ; l'ecart entre 1,753 et 1,806 melange le changement de jeu d'items et le
changement d'estimateur", et publier la decomposition des deux effets.

### 3.5 Le comptage des cellules du critere A6. Gravite : mineure. [VERIFIE]

Sections 5 et 8 : "le net est negatif dans les 24 cellules mesurees, sans exception, pour les
quatre conditions, les deux axes, les trois variantes et les deux vagues de verite". Quatre
fois deux fois trois fois deux vaut 48, et `a7-critere-a6.csv` contient bien 48 lignes, toutes
a net negatif. Le 24 est correct pour la correlation de Spearman, qui ne depend pas de la vague
de verite. Le JOURNAL dit 48, le rapport dit 24.

**Correction proposee.** Ecrire "48 lignes pour le net, 24 valeurs distinctes pour la
correlation de Spearman".

### 3.6 Le temoin de hasard du critere A6 n'est pas celui que le fichier suggere. Gravite : mineure. [VERIFIE]

`a7-critere-a6.csv` porte une colonne `taux_uniforme_1_sur_K` a 0,3497, placee juste apres
`taux_reparation_parmi_changes` a 0,2923. Un lecteur en conclura que la regle informee fait
moins bien que le hasard. Ce n'est pas le cas : la colonne est la moyenne de 1 sur K, et le
temoin correct pour un **taux de reparation** est `1/K` multiplie par la part des cellules
basculees ou l'agent avait faux, soit 0,3497 fois 0,478, environ **0,167**. La regle informee
le bat d'un facteur 1,75, la regle naive de 1,10.

**Correction proposee.** Renommer la colonne ou publier le temoin a 0,167 dans le rapport, ce
qui affaiblit un peu l'argument "la regle informee repare 1,58 fois plus que le hasard" en
montrant que la regle naive n'est deja qu'a peine au dessus du hasard.

### 3.7 L'invariance a somme constante est vraie, et bien verifiee. Gravite : aucune. [VERIFIE]

Point favorable, a dire : l'invariance revendiquee est mathematiquement exacte pour les trois
mesures, et pas seulement pour deux. Le retrecissement `p'(r|s) = lambda p(r|s) + (1 - lambda)
p(r)` laisse la marge poolee inchangee ; or `H(R)`, `1 - somme p(r) au carre` et `Var(R)` ne
dependent que de cette marge. Les trois totaux sont donc invariants, ce que les donnees
confirment : sur les 24 couples reconstitues, `w x inter + (1 - w) x intra` est constant a
moins de 0,001 pres entre lambda 0 et lambda 1.

### 3.8 Ce qu'un relecteur demandera et qui manque

- Le temoin sans donnee humaine pour la regle informee, que le rapport declare lui meme
  manquant en "ce que je n'ai pas pu verifier" point 3. Sans lui, on ne sait pas si le gain de
  1,58 vient du transport ou de B2.
- Une sensibilite au seuil de 20 personnes par cellule, declaree manquante au point 6.
- Une sensibilite a la graine des cinq blocs de calibration, non declaree.
- Aucune correction pour tests multiples sur les 48 lignes du critere A6.

---

# 4. a8-baselines-durcies.md

### 4.1 Le regime "famille retiree" retire l'information a B2 seulement. Gravite : bloquante. [VERIFIE pour le protocole, PROBABLE pour l'ampleur]

C'est le resultat annonce en tete du rapport et repris dans le JOURNAL comme "premiere fois
qu'une condition d'agent domine sur les deux axes".

**Verification du protocole.** Dans `a8_familles.py`, la ligne
`contexte = np.setdiff1d(np.arange(m), cols)` retire bien **toute** la famille du contexte de
B2, pour tous les items de la famille, et pas seulement l'item cible. Le decoupage est correct
et conforme a ce que le rapport annonce.

**Le probleme est ailleurs.** Les conditions d'agents ne sont pas replacees dans le meme
regime. Les agents enquete et composite de l'archive ont recu, dans leur invite, l'ensemble des
reponses de la personne au GSS **moins le seul item predit** : a14 section 3.1 cite la regle des
auteurs, "we ensure that the question we are predicting on is not in the input". Quand on
predit `abany`, l'agent composite dispose donc encore de `abdefect`, `abnomore`, `abhlth`,
`abpoor`, `abrape` et `absingle`. B2, elle, en est privee. Le tableau de la section 3.2 compare
une baseline amputee de ses six cousins a un agent qui les a gardes.

**L'ampleur est chiffrable, et elle suffit a renverser la conclusion.** Le papier publie la
condition appariee : a14 section 3.4 rapporte deux strategies de retrait pour les Survey
Agents, "retrait du seul item predit (0,82) ou retrait du bloc entier du GSS auquel appartient
l'item (0,77)", en score normalise, soit environ 4,0 points d'exactitude brute. Applique aux
0,6711 de l'agent enquete sur les 58 items, cela donne environ 0,631, **sous** les 0,6621 de
B2 famille retiree. [PROBABLE, la transposition d'un chiffre mesure sur 100 agents et sur tous
les items vers 58 items n'est pas exacte.]

**Correction proposee.** Soit refaire la comparaison avec la condition de retrait par bloc du
papier si elle figure dans le paquet, soit ecrire noir sur blanc que "le regime famille retiree
n'est applique qu'a B2, les agents conservant les items de la famille dans leur invite, et que
la comparaison est donc defavorable a B2 d'environ quatre points" ; en l'etat, la phrase "les
agents de Stanford battent B2" ne tient pas devant un relecteur qui a lu l'annexe du papier.

### 4.2 Le compte des victoires par famille est un compte de points, pas de differences. Gravite : serieuse. [VERIFIE]

"L'agent composite bat B2 famille retiree dans cinq familles sur six." Dans
`a8-familles-gss.csv`, pour la famille `fe*`, cinq items : B2 0,5217 [0,5059 ; 0,5373] contre
composite 0,5348 [0,5203 ; 0,5500]. Les intervalles se recouvrent largement. Les tests sont
non apparies alors que les memes 1 052 personnes sont des deux cotes, ce qui est conservateur,
et aucune correction n'est appliquee sur les 36 comparaisons famille x condition.

**Correction proposee.** Ecrire "l'agent composite est au dessus de B2 dans cinq familles sur
six ; la difference est distinguable dans quatre", et fournir l'ecart apparie par famille.

### 4.3 La correlation de 0,80 est un effet a deux amas. Gravite : serieuse. [VERIFIE]

Section 5.3 : "La correlation de rang entre l'avantage du modele par item et la stabilite test
retest de l'item vaut 0,80 [MESURE, p < 0,0001, 108 items]."

**Verification sur `a8-twin-par-item.csv`** :

| calcul | valeur |
|---|---|
| Spearman avantage contre retest, 108 items | 0,797 |
| **la meme, sans les 40 items du bloc de prix, 68 items** | **0,561** |
| Spearman avantage contre exactitude de B0 mode | 0,428 |
| Spearman avantage contre nombre de modalites | -0,704 |
| partielle avantage contre retest, a B0 mode fixe | 0,757 |
| avantage moyen dans le bloc de prix | +0,103 |
| avantage moyen hors bloc de prix | -0,056 |

Trois remarques. D'abord, 40 des 108 items appartiennent a un seul bloc, celui qui porte tout
l'avantage du modele : la correlation est en grande partie la separation entre ce bloc et le
reste. Ensuite, le p inferieur a 0,0001 traite 108 items d'une meme batterie comme 108
observations independantes ; le nombre de blocs est de 33, dont 26 a un seul item. Enfin, le
rapport ne mentionne pas que la meme table contient une colonne
`spearman_avantage_exactitude_B0` a 0,428, c'est a dire que l'avantage suit aussi la facilite
de l'item ; ce controle la, la correlation le passe (partielle 0,757), le controle par bloc
non.

**Correction proposee.** Publier la correlation avec et sans le bloc de prix, et calculer le
test au niveau du bloc et non de l'item.

### 4.4 Ce qui est verifie propre

- **La copule n'emploie jamais l'item cible.** `ctx = np.setdiff1d(np.arange(m), bloc)` retire
  le bloc cible entier du conditionnement ; les seuils, les scores normaux et la matrice de
  correlation latente sont estimes sur le seul pli d'entrainement ; le retrecissement est
  choisi par validation interne a deux plis dans le pli d'entrainement. [VERIFIE, lecture de
  `a8_copule.py`]
- Le perimetre de 70 items ordinaux sur 149 est exact : je l'ai recompte, et le filtre
  supplementaire de `items_ordinaux_utilisables` n'ecarte aucun item. [VERIFIE]
- Point favorable non revendique : la copule dispose d'un contexte de 56 items ordinaux, la ou
  B2 dispose de 119 items. Elle gagne avec moins d'information, ce qui rend le resultat plus
  fort que ce que le rapport en dit.
- Toutes les methodes du tableau de la section 4.2 sont bien recalculees sur les memes 70
  items et les memes 1 052 personnes. [VERIFIE]
- Le decoupage par famille retire bien la famille pour tous ses items. [VERIFIE, objection 4.1]

### 4.5 Ce qu'un relecteur demandera et qui manque

- La contamination des 40 produits, declaree non testee au point 9. Elle porte 100 pour cent
  de l'avantage du modele sur Twin et donc le resultat central de la section 5.2. Test le moins
  cher : demander au modele le prix catalogue des 40 produits sans persona, et regarder s'il le
  connait.
- Aucune correction pour tests multiples sur 13 configurations, 6 familles, 2 seuils de
  minorite et 8 blocs.
- Aucune sensibilite a la graine du decoupage en cinq blocs, qui sert de comparateur "B2
  aleatoire" a la ligne de reference du tableau 3.2.

---

# 5. a9-deviance-et-incoherence.md

### 5.1 Le rapport reintroduit le 0,40 a 0,56, l'erreur que a10 avait corrigee le meme soir. Gravite : serieuse. [VERIFIE par lecture croisee]

Section 1.6 : "Le taux de deviance des agents vaut 0,45 a 0,66 fois celui des humains. Cette
fourchette recouvre presque exactement le ratio d'ecarts types intra groupe de 0,40 a 0,56
retenu dans la these du projet."

Le JOURNAL, entree de 22:38, enregistre la correction de a10 : "Le ratio 0,40 a 0,56 (arXiv
2607.18310) est un ratio d'ecarts types PAR ITEM sur toute la population, WVS Turquie seule.
Ce n'est pas un ratio intra groupe." a9 est rendu a 22:53 et le qualifie pourtant de "ratio
d'ecarts types intra groupe".

Deuxieme confusion superposee : un **taux de deviance**, qui est une proportion de reponses
differant du mode d'un groupe, et un **rapport d'ecarts types** ne vivent pas sur la meme
echelle. Deux nombres voisins ne sont pas la meme quantite. Le rapport en tire une consequence
commerciale, "beaucoup plus facile a expliquer a un acheteur", ce qui aggrave le risque.

**Correction proposee.** Supprimer le rapprochement, et ecrire "le taux de deviance des agents
vaut 0,45 a 0,66 fois celui des humains ; cette mesure n'est comparable a aucun ratio d'ecarts
types publie et doit etre presentee seule".

### 5.2 "Plus fort encore que 0,684" est faux. Gravite : serieuse. [VERIFIE]

Section 1.4 : "La deviance moyenne sur les six domaines correle a -0,535 avec la consistance
test retest. C'est plus fort encore que le r = 0,684 entre fidelite d'agent et stabilite propre
releve en section 6 de a1."

0,535 est inferieur a 0,684. Et les deux correlations ne portent ni sur les memes variables,
ni sur le meme jeu, ni sur la meme population.

**Correction proposee.** Ecrire "elle est du meme ordre que le r = 0,684 releve par a1 sur une
autre quantite et un autre jeu ; les deux ne sont pas comparables directement".

### 5.3 Le plancher de permutation du facteur unique n'est pas zero. Gravite : serieuse. [VERIFIE par arithmetique]

Section 4, "Autorise" point 1 : "un facteur unique expliquant 31 pour cent de la variance,
contre un plancher de permutation de 0,000".

Le 0,000 est le plancher de la **correlation moyenne**, pas celui de la part de variance du
premier facteur. Pour une matrice de correlation 6 x 6 dont toutes les correlations hors
diagonale sont nulles, la premiere valeur propre vaut 1 et la part de variance vaut
**1 sur 6, soit 16,7 pour cent**. Avec une correlation moyenne de 0,163, la premiere valeur
propre attendue est `1 + 5 x 0,163 = 1,815`, soit 30,2 pour cent, tres proche des 1,855
mesures. L'exces reel sur le plancher est donc de 14 points, pas de 31.

**Correction proposee.** Ecrire "premier facteur a 30,9 pour cent de la variance, contre 16,7
pour cent attendus sous independance ; la correlation moyenne inter domaines vaut 0,163 contre
un plancher de permutation de -0,0001".

### 5.4 Le controle decisif compare deux mesures de fiabilites tres inegales. Gravite : serieuse. [PROBABLE]

Section 1.4, le test presente comme "le resultat le plus solide de la tache 1" : la deviance
calculee sur les items **stables** de la personne predit la deviance ailleurs (r de 0,14 a
0,36), celle calculee sur ses items **instables** ne predit rien (r de 0,03).

Les deux scores ne sont pas mesures sur le meme nombre d'items. Avec un taux de changement de
28,8 pour cent sur 108 items, l'ensemble stable compte environ 77 items par personne et
l'ensemble instable environ 31. La fiabilite d'un score moyen croit avec le nombre d'items,
donc la correlation du second est attenuee mecaniquement. Une estimation par Spearman Brown
donne un facteur d'attenuation d'environ 1,25 entre les deux ensembles, alors que le rapport
observe entre 4,5 et 11. La conclusion survit donc probablement, mais elle n'est pas etablie
tant que la correction n'est pas faite, et le rapport ne publie ni le nombre d'items par
ensemble ni la version desattenuee.

**Correction proposee.** Publier le nombre moyen d'items par ensemble et la correlation
desattenuee par les fiabilites par moities, deja calculees ailleurs dans le meme script.

### 5.5 Le 71,2 contre 79,5 melange le jeu d'items et le delai. Gravite : serieuse. [VERIFIE par lecture croisee de a8 et a12]

Section 4, "Autorise" point 8 : "La stabilite test retest humaine vaut 71,2 pour cent sur ce
materiel, contre 79,5 pour cent sur le GSS : le denominateur de normalisation depend du jeu
d'items et n'est pas transferable."

a8 section 8 point 6 ecrit que le retest de Twin porte sur "un delai variable de deux a quatre
semaines selon la vague d'origine, la ou le retest du GSS est a deux semaines fixes". a12
demontre precisement que le delai deplace le denominateur. La conclusion de a9 attribue donc au
seul jeu d'items un ecart qui contient une composante de delai, et deux rapports de la meme
nuit se contredisent sur ce point.

**Correction proposee.** Ecrire "le denominateur depend du jeu d'items **et** du delai, qui
n'est pas le meme des deux cotes, deux semaines fixes contre deux a quatre semaines".

### 5.6 Ce qu'un relecteur demandera et qui manque

- Aucun intervalle sur les alphas de Cronbach comparant humains et agents, alors que le tableau
  de la section 2.3 porte le resultat le plus vendable du rapport ; l'alpha a un intervalle de
  confiance connu et peu couteux.
- Aucune correction pour tests multiples sur 13 configurations x 7 batteries x 2 references.
- Le calcul de la deviance depend d'un seuil de 15 repondants par cellule, non balaye.
- Point favorable a signaler : le temoin de permutation, le centrage par item et le controle
  de composition sont faits, correctement, et le rapport annonce ses propres limites avec
  franchise. La liste "Interdit" de la section 4 est la meilleure du dossier.

---

# 6. a12-delai-de-retest.md

### 6.1 Le champ des auteurs n'est pas calcule sur 177 items. Gravite : serieuse. [VERIFIE]

Section 3 : "appliquee aux deux vagues humaines de l'archive elle donne 0,795002 sur les 149
items contre 0,795253 pour le champ `p_wave1__p_wave2__accuracy` calcule par les auteurs sur
les 177 items".

**Verification.** J'ai recalcule la consistance test retest sur quatre jeux d'items :
177 items, 81,2491 ; 169 items, 81,0072 ; **150 items, 79,5253** ; 149 items, 79,5002. Le champ
des auteurs vaut 79,5253, il porte donc sur les **150 items** de leur liste d'exclusion, pas
sur 177. Le controle de definition est en realite plus concluant que ce que a12 en dit,
puisque l'ecart de 0,000251 s'explique entierement par le retrait de `polviews` ; mais
l'affirmation "177 items" est fausse et elle se propage.

**Correction proposee.** Ecrire "0,795002 sur nos 149 items contre 0,795253 pour le champ des
auteurs, qui porte sur leurs 150 items ; l'ecart est exactement le retrait de `polviews`".

### 6.2 La validation du 0,860 repose sur la mauvaise definition. Gravite : serieuse. [VERIFIE par a14 section 2.3]

Section 4.2 : "Le 0,860 reproduit le 86 pour cent publie par Stanford pour la condition
composite, ce qui valide la chaine de calcul."

a12 calcule un rapport de moyennes. Les auteurs normalisent individu par individu puis
moyennent, ce que a14 etablit par citation et que a1 chiffre a 0,865. Deux estimateurs
differents qui arrondissent au meme 0,86 ne se valident pas l'un l'autre. C'est le meme type de
coincidence que celle relevee en 1.8.

**Correction proposee.** Recalculer avec la definition individuelle, ou ecrire "le rapport des
moyennes donne 0,860 ; la definition des auteurs, individuelle puis moyennee, donne 0,865 ; le
0,86 publie est compatible avec les deux".

### 6.3 Le score de l'agent demographique contient encore la recopie de `income`. Gravite : mineure. [VERIFIE]

Les tableaux 4.1 et 4.2 emploient `gss_v6`, dont l'item `income` est recopie a 99,4 pour cent,
et `income` figure dans les 149 comme dans les 118 items du noyau. Voir objection 2.2.

### 6.4 Ce qui est verifie propre, et c'est l'essentiel

- **L'appariement des 118 items se fait par nom de variable GSS**, pas par libelle approche :
  `noms_gss` traduit le suffixe `/y` en deux variables de ballot fusionnees dans un ordre fixe
  et retire l'asterisque de marquage, sans aucun appariement flou. [VERIFIE, lecture de
  `a12_retest_delai.py`]
- **La definition d'exactitude est la meme des deux cotes** : egalite exacte de modalite,
  moyenne d'abord sur les items renseignes chez une personne puis sur les personnes. Les deux
  seules asymetries sont le seuil `MIN_ITEMS_INDIVIDU = 20` et l'exigence que les deux
  passations soient renseignees, qui n'ont aucun effet du cote Stanford puisqu'il n'y a aucune
  cellule vide. [VERIFIE]
- Le sens du biais des non reponses est declare et va dans le sens conservateur.
- Le controle par le rapport MR119 de NORC est une bonne idee, et le rapport en tire lui meme
  la conclusion qui affaiblit son interpretation.

### 6.5 Ce qu'un relecteur demandera et qui manque

- La phrase d'ouverture, "la consistance vaut 77,79 a deux semaines, 69,53 a deux ans et 67,45
  a quatre ans", est celle qui sera citee, et elle ne porte pas la reserve de la section 6, qui
  dit que ces 8 points melangent le delai, le mode de collecte, la population et le traitement
  des non reponses. La reserve doit figurer dans la meme phrase. [PROBABLE]
- Le noyau commun de 118 items est selectionne comme l'ensemble des items presents dans les 11
  paires de vagues, ce qui favorise les items anciens du coeur du GSS, donc les plus stables.
  Un controle par selection aleatoire de 118 items chez Stanford donnerait la sensibilite a ce
  choix.
- Aucun intervalle sur les scores normalises du tableau 4.1, alors que le message du rapport
  est un ecart de 10 points sur ces scores.

---

# 7. a13-positionnement-contribution.md

### 7.1 La revendication (b)3 herite du melange de jeux d'items. Gravite : bloquante. [VERIFIE]

"sur les memes 1 052 participants et les memes 169 items, dont l'exactitude differe de 0,07
point avec un intervalle [-0,52 ; +0,37]". Faux : le 0,07 est un chiffre a 150 items. Voir
objection 1.1. Cette phrase figure aussi dans les deux versions anglaises de la section 6, qui
sont ecrites pour etre collees dans un papier.

**Correction proposee.** Recalculer et reecrire la phrase avant tout usage externe.

### 7.2 La revendication (b)2 herite du controle qui exclut 1. Gravite : serieuse. [VERIFIE]

"les memes personnes reinterrogees deux semaines plus tard tombent en (1,003 ; 1,004) avec des
intervalles contenant 1, ce qui prouve que la methode ne fabrique pas d'ecart la ou il n'y en a
pas". Voir objection 1.2 : l'intervalle du terme intra en entropie est [1,0001 ; 1,0087].
Le mot "prouve" est de toute facon trop fort pour un non rejet.

**Correction proposee.** "tombent a 0,4 pour cent de (1,1) sur les trois mesures, ce qui borne
a un demi pour cent l'ecart que la methode peut fabriquer en l'absence de distorsion".

### 7.3 La revendication (b)4 accuse les voisins d'un defaut que a7 partage. Gravite : mineure. [VERIFIE]

"aucun des trois travaux voisins ne traite ce biais". C'est vrai. Mais a7, le seul correctif du
projet, ne l'applique pas non plus (objection 3.4) et laisse l'estimateur produire un terme
inter negatif (objection 3.1). Revendiquer la rigueur d'estimation impose de la tenir dans tous
les rapports du dossier.

### 7.4 La reconstruction des composantes de Garzon et al. Gravite : serieuse. [PROBABLE]

La section 2.3 declare elle meme, et en detail, que le calcul combine deux tableaux d'effectifs
differents, des ICC a deux decimales et une formule valable en plan equilibre, et conclut :
"Ce calcul est un argument de lecture, pas un resultat publiable en l'etat." La reponse en une
ligne du rapport, elle, l'annonce sans reserve : "son propre tableau permet d'en deduire un
transport inter vers intra que ses auteurs ne calculent pas". C'est la phrase que Simon lira.

**Correction proposee.** Porter la reserve dans la reponse en une ligne.

### 7.5 Ce que a13 recommande et qui reste le meilleur test disponible

La recommandation c.3, recalculer les ratios sur la seule segmentation age croise genre, est la
reponse directe a l'objection la plus previsible d'un relecteur qui connait Garzon et al. Elle
coute une heure et le fichier `a1-ratios-par-axe.csv` contient deja les deux axes separement.
Elle n'a pas ete faite.

---

# 8. a14-lecture-2411-10109-v3.md

### 8.1 La correction apportee a a2 est fausse, et elle est deja enregistree comme acquise. Gravite : bloquante. [VERIFIE]

Section 3.1 : "Ceci contredit frontalement la deduction de a2 section 2.1", puis la
consequence : "La comparaison a armes egales est donc B1 complet, 0,6209, contre 0,5818."
Le JOURNAL, entree de 23:05, l'enregistre comme acquis.

**Verification.** Le papier decrit une invite demographique contenant ideologie, parti, race,
genre et age. Cette description correspond a `gss_v8`, qui recopie `polviews` a 0,961 et
`partyid` a 0,994. Le fichier que a2 evalue sous l'etiquette "agents demographiques" et dont le
score est 0,5818 est `gss_v6`, qui obtient 0,200 et 0,165 sur les memes items, c'est a dire
**sous la modalite majoritaire**. La deduction de a2 est confirmee par la mesure.

**La reconciliation proposee par a14 est refutee par les donnees.** a14 suppose que la regle
"la question predite est retiree de l'entree" retire l'ideologie de l'invite au moment ou l'on
predit `polviews`. Si cette regle s'appliquait au descripteur demographique, `gss_v8` ne
pourrait pas obtenir 0,961 sur `polviews` ni 0,994 sur `partyid`. Elle ne s'y applique donc
pas, et elle n'explique pas le 0,200 de `gss_v6`.

**Correction proposee.** Annuler la ligne de correction de a14 pour a2 section 2.1, et la
remplacer par : "le papier decrit l'invite demographique de `gss_v8` ; `gss_v6`, que a2 evalue,
est une autre generation qui n'a recu ni ideologie ni parti, ce que la mesure item par item
etablit". Corriger l'entree de 23:05 du JOURNAL.

### 8.2 La demonstration de la double generation peut se faire plus simplement et plus completement. Gravite : serieuse, mais favorable. [VERIFIE]

La reconstruction arithmetique de la section 3.3, a partir de la ligne "Gender" du tableau 5 et
des poids du tableau 1, est elegante et je n'ai pas de raison d'en douter. Mais elle etablit
seulement que deux generations existent, et laisse "non etabli" ce qui les differencie. Le
tableau de l'objection 1.3 etablit les deux d'un coup, sans arithmetique et sans hypothese, sur
les fichiers du paquet. Le sigle `LA` cesse d'etre un mystere utile : `v8` est l'ablation
demographique du papier, `v6` est une ablation a profil d'etat civil sans politique.

**Correction proposee.** Ajouter le tableau des recopies a la section 3.3, et retirer la phrase
"il faut cesser de chercher la" de la section 3.3, remplacee par "le contenu des deux invites
se lit dans les taux de recopie des 29 items ecartes".

### 8.3 Ce qui est verifie propre et precieux

- La definition d'exactitude, la normalisation individuelle, l'absence de baseline non LLM et
  l'absence de discussion du delai sont des lectures citees mot pour mot ; elles sont la partie
  la plus fiable du dossier.
- Le point sur l'absence de temperature et de nombre d'echantillons est une vraie limite a
  porter dans a1, et il l'est.

---

# 9. JOURNAL-NUIT-2026-09-07.md

1. **Entree de 23:05 sur a14. Gravite : bloquante. [VERIFIE]** "L'invite demographique
   CONTIENT l'ideologie politique et le parti : la deduction de a2 section 2.1 est contredite.
   Consequence favorable : la bonne comparaison est B1 complet 0,6209 contre 0,5818." A
   annuler, voir 8.1. C'est la seule ligne du journal qui, appliquee telle quelle, introduirait
   une affirmation fausse dans le dossier.

2. **Entree de 22:50 sur a8. Gravite : serieuse. [VERIFIE]** "Premiere fois qu'une condition
   d'agent domine sur les deux axes" herite du regime asymetrique de l'objection 4.1. A
   assortir de la reserve.

3. **Entree de 23:15 sur a7. Gravite : serieuse. [VERIFIE]** "Atteindre (1,1) par transport pur
   est impossible" est vrai sur deux mesures sur trois seulement, voir 3.2. Et "le terme inter
   humain ne pese que 4,6 pour cent de l'entropie totale" doit garder le mot entropie.

4. **Entree de 23:15, seconde partie. Gravite : mineure. [VERIFIE]** "Plus de casses que de
   reparations dans les 48 lignes" : le journal a raison, le rapport a7 ecrit 24. C'est le
   rapport qu'il faut corriger, pas le journal.

5. **Entree de 22:53 sur a9. Gravite : serieuse. [VERIFIE]** Le resume ne reprend pas le
   rapprochement fautif avec le 0,40 a 0,56, mais il ne le signale pas non plus, alors que
   l'entree de 22:38 venait de le corriger quinze minutes plus tot. Le journal est le seul
   endroit ou cette collision pouvait etre vue.

6. **Horodatage. Gravite : mineure. [VERIFIE]** L'ordre des entrees n'est pas monotone : 22:55,
   puis 23:10, puis 22:58, puis 23:05, puis 23:04, puis 23:05. Le document annonce "chaque
   entree est horodatee". Sans importance scientifique, mais un lecteur exterieur y verra une
   reconstruction apres coup.

---

# 10. Contradictions entre rapports, avec la ligne a corriger

| # | contradiction | ligne a corriger | statut |
|---|---|---|---|
| C1 | a2 section 2.1 deduit que l'agent demographique n'a pas recu l'ideologie ; a14 section 3.1 dit le contraire d'apres le papier | a14, tableau "a2-baselines.md", lignes 2.1 et 2.1 suite. **C'est a14 qui a tort** : le papier decrit `v8`, a2 mesure `v6` | [VERIFIE] |
| C2 | a1 limite 5 compare son 0,64 a 0,89 au 0,40 a 0,56 de la these ; a10 montre que ce n'est pas la meme quantite ; **a9 section 1.6 la refait** | a9, section 1.6, phrase "Cette fourchette recouvre presque exactement le ratio d'ecarts types intra groupe de 0,40 a 0,56" | [VERIFIE] |
| C3 | PASSATION section 5 dit "transport a somme constante" ; a7 section 0 montre que le transport seul ne peut pas atteindre (1,1) sur deux mesures, et **le peut sur la troisieme** | PASSATION section 5, corollaire ; et a7 section 0, qui doit indexer sa conclusion sur la mesure | [VERIFIE] |
| C4 | a1 section 7.3 compare une exactitude a 150 items a des ratios a 169 items ; a13 (b)3 recopie l'erreur | a1 section 7.3, tableau ; a13 revendication (b)3 et les deux versions anglaises de la section 6 | [VERIFIE] |
| C5 | a2 section 4 point 2 "cinq des six conditions battues" contredit a2 section 9 limite 2 ; a8 section 7.1 la valide | a2 sections 4 et 10 ; a8 section 7.1, dernier point | [VERIFIE] |
| C6 | a1 exclut `income` comme fuite demographique ; a2, a7, a8 et a12 le gardent dans leurs 149 items, et `gss_v6` le recopie a 99,4 pour cent | `FUITE_DEMOGRAPHIQUE` dans `a2_baselines_gss.py` et `a12_retest_delai.py`, et les limites de a2 | [VERIFIE] |
| C7 | a9 attribue le 71,2 contre 79,5 au seul jeu d'items ; a8 section 8 point 6 signale que le delai de Twin est variable de deux a quatre semaines ; a12 montre que le delai deplace le denominateur | a9, section 4 "Autorise" point 8 | [VERIFIE] |
| C8 | a1 applique une soustraction du residu de permutation, a7 ne l'applique pas, et a7 attribue l'ecart de ratio au seul jeu d'items | a7, section 1, "Controle de coherence avec a1" | [VERIFIE] |
| C9 | a12 dit que le champ des auteurs porte sur 177 items ; il porte sur 150, comme je le verifie par la valeur exacte 79,5253 | a12, section 3, phrase de controle de la definition | [VERIFIE] |
| C10 | a12 valide sa chaine de calcul sur un 0,860 obtenu par rapport de moyennes ; a14 section 2.3 etablit que la definition des auteurs est individuelle et donne 0,865 | a12, section 4.2, derniere phrase | [VERIFIE] |
| C11 | a1 section 3 affirme que les trois mesures donnent le meme classement ; `a1-ratios.csv` inverse composite et entretien sur le terme intra en variance ordinale | a1, section 3, "Robustesse au choix de mesure" | [VERIFIE] |
| C12 | a7 dit 24 cellules, son propre fichier en contient 48, et le JOURNAL dit 48 | a7, sections 5 et 8 | [VERIFIE] |
| C13 | PASSATION section 6 dit "aucun papier lu ne publie cette mesure" ; a13 section 1.1 montre que LifeMem la publie ; a14 section 5.1 la redeclare vraie "pour ce papier ci" | PASSATION section 6 ; a14 section 5.1, ou la restriction doit etre explicite | [VERIFIE] |

---

# 11. Les dix objections les plus graves du dossier

| rang | objection | rapport | gravite | statut | correction en une phrase |
|---|---|---|---|---|---|
| 1 | Le regime "famille retiree" ampute B2 de ses cousins pendant que les agents les gardent dans leur invite ; le papier publie la condition appariee a environ 4 points de moins, ce qui suffit a renverser le resultat | a8 section 3 | bloquante | [VERIFIE] protocole, [PROBABLE] ampleur | Refaire la comparaison avec la condition de retrait par bloc du papier, ou declarer l'asymetrie et retirer la phrase "les agents battent B2" |
| 2 | L'ecart de 0,07 point est calcule sur 150 items, le facteur 13,5 sur 169 ; sur 169 items l'ecart vaut -0,88 [-1,29 ; -0,45] et exclut zero | a1 section 7.3, a13 (b)3 | bloquante | [VERIFIE] | Recalculer les exactitudes appariees sur les 169 items et reecrire la section 7.3 |
| 3 | La correction que a14 apporte a a2 est fausse : `gss_v6` n'a recu ni ideologie ni parti (0,200 et 0,165), `gss_v8` les a recus (0,961 et 0,994) | a14 section 3.1, JOURNAL 23:05 | bloquante | [VERIFIE] | Annuler la correction, retablir la deduction de a2 et la transformer en fait mesure |
| 4 | La correction de Miller Madow n'est pas invariante sous le transport : a lambda 0 le ratio inter estime vaut -0,13, soit plus que la demi largeur des intervalles publies | a7 section 3 | bloquante | [VERIFIE] | Estimer le biais sur les donnees transportees et republier le tableau du critere 1 |
| 5 | L'impossibilite d'atteindre (1,1) par transport pur ne vaut que sur deux des trois mesures de a1 ; sur la variance ordinale le plafond depasse 1 pour cinq couples sur huit, et w vaut 8,9 pour cent et non 4,6 | a7 sections 0 et 8 | bloquante | [VERIFIE] | Indexer la conclusion sur la mesure et dire que le deficit total est porte par les items nominaux |
| 6 | Le controle de la vague 2 exclut 1 sur le terme intra pour deux mesures sur trois, contrairement au texte et au critere que a1 s'applique a lui meme | a1 section 3, a13 (b)2 | serieuse | [VERIFIE] | Ecrire "a 0,4 pour cent de (1,1)" et cesser d'employer l'inclusion de 1 comme critere binaire |
| 7 | "Cinq des six conditions battues par du scikit-learn" compte trois conditions que le meme rapport declare non comparables a B2 | a2 sections 4 et 10, a8 section 7.1 | serieuse | [VERIFIE] | Reduire la phrase aux deux conditions comparables, entretien et enquete |
| 8 | La correlation de 0,80 entre avantage du modele et stabilite de l'item tombe a 0,561 hors du bloc de prix, et son p traite 108 items de 33 blocs comme independants | a8 section 5.3 | serieuse | [VERIFIE] | Publier la correlation avec et sans le bloc de prix et tester au niveau du bloc |
| 9 | a9 reprend le 0,40 a 0,56 comme un ratio intra groupe quinze minutes apres la correction de a10, et le compare a un taux de deviance qui n'est pas un rapport d'ecarts types | a9 section 1.6 | serieuse | [VERIFIE] | Supprimer le rapprochement et presenter le taux de deviance seul |
| 10 | `income` reste dans les 149 items et `gss_v6` le recopie a 99,4 pour cent contre 63,4 pour cent de retest humain, alors que a1 l'avait ecarte pour ce motif | a2, a7, a8, a12 | serieuse | [VERIFIE] | Ajouter `income` a la liste de retrait ou publier l'effet de 0,28 point sur le score de `gss_v6` |

Suivent immediatement, sans faire partie des dix : le compte des victoires par famille qui
melange points et differences (a8 4.2), le "plancher de permutation de 0,000" pour une part de
variance dont le plancher est 16,7 pour cent (a9 5.3), la confusion entre les 150 et les 177
items dans le controle de definition de a12 (6.1), l'absence totale de correction pour tests
multiples dans les cinq rapports, et l'inversion de classement des trois mesures sur le terme
intra (a1 1.5).

---

# 12. Ce que je n'ai pas pu verifier

1. **Je n'ai rejoue aucun script en entier.** Les objections chiffrees viennent des fichiers
   `resultats/*.csv` produits par ces scripts, de recalculs directs sur les fichiers de
   `data/osf-t6g7k-stanford`, et de la lecture du code. Je n'ai pas relance `a1`, `a7`, `a8`
   ni `a12`, donc je n'ai pas verifie que les CSV publies correspondent bien a la derniere
   version des scripts.
2. **L'ampleur du biais de l'objection 4.1 est une transposition.** Le 0,77 contre 0,82 du
   papier est mesure sur un sous echantillon de 100 agents et sur l'ensemble des items ; je
   l'applique aux 58 items de familles. L'ordre de grandeur est defendable, la valeur exacte
   non. Seul un recalcul avec la condition de retrait par bloc, si elle figure dans le paquet,
   trancherait. Je n'ai pas cherche si un fichier de cette condition existe dans l'archive.
3. **La re inflation des ratios de l'objection 3.1** suppose que le biais de la correction de
   Miller Madow decroit comme lambda au carre. C'est l'approximation du second ordre de
   l'information mutuelle, elle est correcte pour de petites deviations mais je ne l'ai pas
   verifiee numeriquement sur ces donnees. Les valeurs 0,99, 1,17, 1,02 et 1,19 sont donc des
   ordres de grandeur, pas des mesures.
4. **Le calcul d'attenuation de l'objection 5.4** suppose une fiabilite par item identique
   entre items stables et instables, ce qui est probablement faux dans le sens qui affaiblit
   mon objection. Je ne dispose pas du nombre d'items par ensemble, qui n'est pas publie.
5. **Twin-2K-500.** Je n'ai verifie aucun chiffre de a9 ni de a8 sur les donnees brutes de
   Twin ; toutes mes verifications sur ces deux rapports portent sur leurs propres fichiers de
   sortie et sur l'arithmetique interne.
6. **Les rapports a3, a4, a5, a6, a10 et a11** ne m'ont pas ete confies et je ne les ai pas
   lus. Plusieurs objections ci dessus s'appuient sur ce que le JOURNAL et a13 rapportent de
   a10 ; si a10 dit autre chose, les objections C2 et 1.8 doivent etre reverifiees.
7. **Les deux papiers tiers**, LifeMem et Garzon et al., n'ont pas ete ouverts. Je ne conteste
   aucune lecture de a13, je ne signale que l'ecart entre ses reserves internes et sa reponse
   en une ligne.
8. **Le PDF de 2411.10109 v3** n'a pas ete telecharge. Je prends les citations de a14 pour
   exactes ; mon objection 8.1 ne porte pas sur la citation mais sur son application au
   fichier `gss_v6`.
9. **Je n'ai pas cherche a evaluer la puissance** des tests du dossier, ni a construire la
   correction pour tests multiples que je reclame. Les deux demandent de fixer d'abord la
   famille d'hypotheses, ce qui est une decision de redaction et non de calcul.
