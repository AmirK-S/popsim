# a37. Notre 1,12 est l'effet de consensus liberal : le modele generatif de Brandt et Sleegers chez les humains, puis ce que la simulation en fait

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md` sections 7.1 et 7.2, contradiction D9, signalees par
`resultats/a47-errata-2.md` section 4. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Aucun recalcul,
aucun appel de modele de langage : les denominateurs cites sont deja dans
`a37-agents-gss.csv` et `a37-agents-gss-150.csv`, colonne `n_items_perdus_log`.

### E1. Sections 3 et 5 : aucune pente ne se cite sans son nombre d'items, et la variante a derive humaine est la seconde estimation. Objection a45 numero 7.1, contradiction D9.

**Phrase d'origine.** « **`agents v8` porte la pente a -12,41, soit 5,6 fois la valeur
humaine** », reprise dans les syntheses sous la forme « deforme la loi humaine de consensus
de moins 2,2 a moins 12,4 ».

**Correction.** Le rapport de dispersion droite sur gauche devient infini des qu'un camp est
unanime sur un item, et l'item sort de la regression : **les pentes ne sont pas calculees
sur le meme support**, et une pente citee sans son denominateur reproduit la faute que a17
objection 2 avait qualifiee de bloquante sur a1. Le rapport le declare en section 3 et
section 5.1 ; ce qui manque est que la synthese le porte.

| condition | items retenus sur 79 | pente publiee |
|---|---|---|
| humains vague 1 | **79** | -2,22 |
| `agents composite` | 79 | -3,80 |
| `agents entretien (v3)` | 73 | -5,37 |
| **`agents v8`** | **63** | **-12,41** |
| `B3 foret` | 45 | -4,12 |
| **C2, 150 personnes** | **46** | **-2,73** |
| C3, 150 personnes | 71 | -1,89 |

La formule a ecrire partout est : **« pente -2,22 sur 79 items chez les humains, -12,41 sur
les 63 items ou elle est definie chez `v8`, -7,57 si la derive humaine sert d'abscisse ».**
La seconde estimation, colonne `pente_sur_derive_humaine`, deplace le chiffre de 40 pour
cent ; la section 5.1 la donne deja et elle ne doit jamais etre omise, car une partie de la
raideur de `v8` vient de ce que sa **propre** derive est comprimee, moins 0,095 contre moins
0,119 chez les humains.

**Interdiction ajoutee.** **Ne jamais comparer un compte d'unanimite entre le perimetre 150
et le perimetre 1 052.** La troncature est plus forte la ou l'echantillon est plus petit, et
l'unanimite est mecaniquement plus facile sur 63 personnes de gauche que sur 417 : le
« 31 sur 79 » de C2 et le « 12 sur 79 » de `v8` ne sont pas sur la meme echelle, et la
comparaison C2 a 46 items contre `v8` a 63 items n'est pas lisible.

### E2. Sections 5 et 6 : la pente de consensus, l'unanimite et le Gini Simpson sont des quantites de gabarit. Objection a45 numero 7.2.

**Correction.** Le Gini Simpson d'un camp sur un item ne depend que de la table
(camp, modalite) : il est exactement invariant sous permutation des personnes a l'interieur
de leur camp, donc une **quantite de gabarit** au sens du critere de Yuan que
`resultats/a44-generateur-nul.md` applique au reste du dossier. Le generateur nul de a44 le
reconnait explicitement, « elle rend le camp de gauche litteralement unanime, Gini Simpson
0,000 (a30) : **oui par construction**, une marginale de segment degeneree donne un nul
degenere » [a44 section 9.2], et son errata classe la pente droite sur gauche par item du
present rapport dans la meme case, « **oui par construction, non teste** ». Ces quantites ne
se publient jamais seules : elles se publient a cote d'une quantite de personne, la chute
d'exactitude sous permutation intra segment, et du plancher humain.

**Reserve de regime de decodage.** L'unanimite de C2 est mesuree en argmax et ne l'a jamais
ete en regime de tirage, alors que les traces le permettent ; `a35-couples-regime.csv`
montre que le passage a l'echantillonnage remonte le ratio intra de 0,36 a 0,43 selon les
familles. [PROBABLE]

---

Seance du 8 septembre 2026. Aucun appel de modele de langage, lecture seule sur `data/`,
quatre coeurs, environ vingt secondes de calcul pour l'ensemble. Aucun fichier existant
n'a ete modifie. `a1_double_distorsion`, `a2_commun`, `a2_baselines_gss`, `a25_commun`,
`a28_commun`, `a9_commun` et les six scripts `a30_*` sont importes tels quels.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu
dans une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## Reponse en une ligne

**Oui, le 1,122 de `a30` est l'effet de consensus liberal, et le modele generatif de
Brandt et Sleegers l'explique presque entierement.** [MESURE] Sur les 79 items du GSS
auxquels une orientation gauche droite peut etre donnee, le logarithme du rapport de
dispersion droite sur gauche est une fonction decroissante de la derive agregee de
l'item : **pente -2,22, intervalle [-2,56 ; -1,96], R2 de 0,68**, correlation de rang
-0,86. Le signe du rapport est predit par le seul signe de la derive dans **72 cas sur
79**. La replication tient sur les dix items de politique publique de Twin-2K-500 (pente
-2,07, R2 0,73), sur la reinterrogation des memes personnes, sur un second codeur
d'orientation entierement automatique, et sur la restriction aux items dont l'orientation
n'est pas discutable. **Une fois la position controlee, il ne reste presque rien** : un
temoin qui ne connait que la position moyenne de chaque camp reproduit un rapport global
de **1,211** la ou la mesure donne **1,220** (ecart 0,010, intervalle [-0,002 ; 0,020]),
et explique **98 pour cent** de la variance item par item du logarithme du rapport. Le
rapport residuel a derive nulle vaut 1,040 [1,005 ; 1,072] et ne survit pas a la
correction de Holm. **La contribution du dossier n'est donc pas le 1,12, c'est ce que la
simulation en fait.** [MESURE] Toutes les conditions riches en information redressent la
pente au dela de la valeur humaine, et **la condition qui porte l'etiquette ideologique la
porte a -12,41 contre -2,22**, en rendant le camp du cote du consensus litteralement
unanime sur douze items ; nos agents locaux avec etiquette (C2) rendent le camp de gauche
unanime sur **31 items sur 79** contre 8 pour C3 sans etiquette et 0 chez les humains, et
ces items unanimes sont exactement ceux dont la derive est la plus a gauche (derive
moyenne -0,286 contre -0,119 sur l'ensemble). **Sans etiquette, C3 donne une pente de
-1,89 [-2,85 ; -0,96], indistinguable de la pente humaine.** La prediction de la these est
verifiee sur les deux volets.

Une reserve de fond, qui n'etait pas prevue : **le second parametre du modele de Brandt et
Sleegers n'est pas verifie dans nos deux echantillons.** Ils supposent que l'etiquette
ideologique penche a droite ; elle penche a gauche chez nous, derive -0,035 sur le GSS de
Stanford et -0,067 sur Twin. Le premier parametre, lui, est verifie et massif : 60 des 79
items penchent a gauche, derive moyenne -0,119.

---

## 0. Ce qui a ete mesure, et sur quoi

| | GSS | Twin-2K-500 |
|---|---|---|
| personnes | 1 052 | 2 058 |
| items d'analyse | 149, dont **79 orientables** gauche droite | 609, dont les **10 items de politique publique** de `QID287` |
| camps | `political_ideology` repliee en trois : gauche 417, centre 303, droite 332 | `QID22` repliee en trois : gauche 909, centre 582, droite 567 |
| controle temporel | vague 2, memes personnes a deux semaines | vague 4, memes personnes |
| simulations | 6 conditions de Stanford, C2, C3, 5 predicteurs statistiques | 15 fichiers de configuration des auteurs |

[MESURE] Le repliement des camps, les estimateurs de dispersion, le moteur de
reechantillonnage par poids et les corrections de tests multiples sont ceux de
`a30_commun`, importes sans une ligne de changement. Ce rapport n'ajoute que trois choses :
l'orientation gauche droite des items, la derive agregee, et le temoin de position.

---

## 1. Famille d'hypotheses, ecrite avant de regarder le moindre resultat

Elle figure en tete de `a37_humains.py` et de `a37_agents.py`, et n'a pas ete revisee.

**Convention de signe, posee avant tout calcul.** Chaque modalite d'un item recoit un
score dans [0, 1], 0 au pole de gauche et 1 au pole de droite. Le point neutre d'un item
est 0,5 : c'est la modalite mediane pour un item a nombre impair de modalites (« about
right », « about the same »), et le partage a parts egales pour un item binaire. La
**derive agregee** D d'un item est la position moyenne de l'echantillon entier moins 0,5.
**D positif veut dire que la majorite penche a droite sur cet item.** Le modele de Brandt
et Sleegers predit alors une **pente negative** du logarithme du rapport de dispersion
droite sur gauche sur D.

**Famille « pentes humaines », quatre tests, Holm.**
H1 : sur le GSS, la pente est negative.
H2 : elle le reste apres retrait des items dont l'orientation est de niveau [HYPOTHESE].
H3 : elle le reste quand l'orientation vient du codeur automatique et non de la lecture.
H4 : elle est negative sur les dix items de politique publique de Twin.

**Famille « ce qui reste », trois tests, Holm.**
H5 : l'ordonnee a l'origine, c'est a dire le rapport attendu pour un item de derive nulle,
ne differe pas de 1. Si H5 n'est pas rejetee, le modele a deux parametres suffit.
H6 : le rapport global predit par le seul temoin de position ne differe pas du rapport
observe.
H7 : la vague 2, memes personnes, donne la meme pente ; c'est le plancher de bruit.

**Famille « accord des codeurs », un test, non corrige.**
H8 : le taux d'accord entre les deux codeurs d'orientation depasse le hasard.

**Famille A1, huit tests, Holm** (six conditions de Stanford, C2, C3) : la pente de la
condition differe de la pente humaine, mesuree sur les memes personnes et les memes items.
**Famille A2, trois tests, Holm** : les conditions qui portent l'etiquette ideologique ont
une pente plus raide que la condition correspondante sans etiquette, contraste apparie.
**A3, un test** : sans etiquette, la pente est indistinguable de la pente humaine.

**Prediction de la these, ecrite avant les resultats.** Avec l'etiquette (C2, v8), la
pente est exageree et le camp du cote du consensus devient unanime ; sans etiquette (C3,
enquete), la pente est proche de l'humaine.

---

## 2. Protocole

### 2.1 L'orientation des items, item par item, et le second codeur

`a37-orientation-items.csv`, une ligne par item, avec la liste des modalites dans l'ordre,
le sens, le niveau de certitude et la justification en clair.

**Codeur A, la lecture du libelle.** Le champ `sens` vaut +1 quand l'ordre des modalites
declare dans `question_master` va du pole de gauche vers le pole de droite, et -1 quand il
va dans l'autre sens. Trois niveaux : **[CONFIRME]** quand la direction est celle d'une
echelle standardisee de la science politique americaine employee telle quelle dans la
litterature du GSS (avortement, tolerance de Stouffer, roles de genre, peine de mort,
immigration, explications de l'ecart racial) ; **[PROBABLE]** quand le libelle et
l'alignement partisan documente du sujet donnent la direction sans ambiguite ;
**[HYPOTHESE]** quand la direction est deduite du sujet seul et pourrait se discuter.

[MESURE] **79 items sur 149 recoivent une orientation : 26 [CONFIRME], 39 [PROBABLE], 14
[HYPOTHESE].** Les 70 autres n'en recoivent aucune, et la raison est ecrite pour chacun
dans `a37_commun.SANS_ORIENTATION` : faits biographiques, equipement, etat de sante, bien
etre, confiance interpersonnelle, perception de richesse d'un groupe, pratique et croyance
religieuses, choix de candidat (qui est la variable de camp elle meme et non une position),
et les trois items de tolerance envers le raciste, ou deux normes s'opposent et ou le pole
de gauche n'est pas defini. C'est la meme decision qu'en `a25_commun` pour la desirabilite,
prise pour la meme raison.

Deux regles uniformes, appliquees a l'identique et declarees avant le classement.
Sur la batterie de depenses publiques, « too little » est le pole de gauche, **sauf pour la
defense nationale** ou c'est « too much » ; les quatre items faiblement ideologiques de la
batterie (espace, routes, parcs, recherche) recoivent [HYPOTHESE] et sortent de l'analyse
stricte. Sur la batterie de confiance dans les institutions, **la direction n'est pas
uniforme** : la confiance dans l'armee, les grandes entreprises, la religion organisee, la
finance et la Cour supreme a son pole de droite en premier, celle dans les syndicats, la
presse, la science, l'education, l'executif federal et la medecine a son pole de gauche en
premier ; deux items, le Congres et la television, ne recoivent aucune direction.

**Codeur B, entierement automatique, qui ne lit aucun libelle.** Le pole de gauche d'un
item est celui que le camp de gauche endosse le plus, mesure par le rang moyen declare
dans chaque camp. Ce codeur a un defaut declare : il est construit sur les memes donnees.
Il ne sert donc pas de mesure principale, seulement de controle.

| accord des codeurs | valeur |
|---|---|
| **items ou A et B s'accordent** | **78 sur 79, taux 0,987** |
| p binomial exact contre le hasard | 1,3 x 10 puissance -22 |
| le seul desaccord | `natroad`, les routes et les ponts, item de niveau [HYPOTHESE] |
| stabilite du codeur B d'une vague a l'autre, 149 items | 0,953 |

[MESURE] **Le seul desaccord entre les deux codeurs porte sur les routes et les ponts**,
que la regle uniforme de la batterie de depenses range a gauche et que les donnees rangent
a droite, avec un ecart de position entre camps de 0,009, c'est a dire rien. C'est
exactement l'item pour lequel le niveau [HYPOTHESE] avait ete pose d'avance.

### 2.2 La derive agregee, et ce qu'elle est

[MESURE] La derive est calculee sur **l'echantillon entier**, camps confondus, et jamais
sur un camp. Elle est donc invariante par permutation de l'etiquette de camp, ce qui rend
le test de permutation lisible : l'hypothese nulle est exactement « la dispersion relative
des deux camps ne depend pas de la derive de l'item », qui est l'hypothese que le modele
de Brandt et Sleegers rejette.

### 2.3 Le temoin de position

C'est le controle que `a30` avait declare manquant, au point 9 de sa section 11 : « le
rapport droite sur gauche n'a pas ete decompose entre effet de position et effet de
dispersion ». Il est construit ici.

Pour chaque camp et chaque item, on prend la position moyenne observee de ce camp sur
l'echelle de l'item, et on calcule la dispersion de la **loi de dispersion maximale a
cette position**, c'est a dire la loi d'entropie maximale a moyenne fixee, p proportionnel
a exp(theta s). C'est la dispersion qu'aurait un camp dont la seule propriete serait sa
position. Le temoin est ramene a l'echelle de l'estimateur employe partout ailleurs en
multipliant par N sur N moins 1, sans quoi la comparaison porterait une correction de
petit echantillon et non une difference de structure.

[MESURE] **Pour un item binaire, la moyenne determine entierement la loi : le temoin
coincide exactement avec la mesure, au dernier chiffre.** Ce n'est pas un defaut du
temoin, c'est le point de fond du rapport : sur un item binaire, la dispersion d'un camp
**est** sa position, et il n'y a rien d'autre a expliquer.

### 2.4 Intervalles, tests, corrections

**Bootstrap sur les personnes, et sur l'echantillon entier.** Un tirage multinomial porte
sur les 1 052 personnes ; les poids des deux camps s'en deduisent en multipliant par le
masque du camp. Reechantillonner les deux camps separement, comme le fait `a30` pour un
contraste de camps, casserait le lien entre l'abscisse et l'ordonnee de la regression, qui
viennent des memes personnes. 1 000 tirages pour les humains, 2 000 pour les agents,
percentiles a 2,5 et 97,5 pour cent.

**Tests.** Permutation de l'etiquette de camp pour les pentes humaines, 2 000
permutations, estimateur de Phipson et Smyth qui ne rend jamais un p nul. Pour les ecarts
entre conditions simulees, p bilateral tire de la distribution de bootstrap appariee, avec
le meme plancher a 1 sur B plus 1. Holm a l'interieur de chaque famille, jamais entre
familles.

**Ce qui a ete repris et non reecrit.** `a30_commun` en entier, `a2_baselines_gss.charger`,
`a25_commun.options_par_item` et `sans_score`, `a28_commun.charger_tout`, `ORDRE_METHODES`,
`holm` et `benjamini_hochberg`, `a9_commun` pour Twin. Aucun de ces fichiers n'a ete touche.

---

## 3. Volet 1, les humains

### 3.1 La pente, et sa robustesse

`a37-regressions-humains.csv`.

| test | pente | intervalle | R2 | rho de Spearman | items | p | p Holm |
|---|---|---|---|---|---|---|---|
| **H1 GSS, codeur A** | **-2,219** | [-2,563 ; -1,958] | **0,677** | -0,859 | 79 | 0,0005 | 0,0020 |
| H2 GSS, orientation stricte | -2,229 | [-2,626 ; -1,905] | 0,653 | -0,833 | 65 | 0,0005 | 0,0020 |
| H3 GSS, codeur B automatique | -2,189 | [-2,544 ; -1,910] | 0,683 | -0,876 | 79 | 0,0005 | 0,0020 |
| **H4 Twin, dix items politiques** | **-2,066** | [-2,249 ; -1,896] | **0,731** | -0,806 | 10 | 0,0005 | 0,0020 |
| H7 GSS vague 2, plancher de bruit | -2,145 | [-2,519 ; -1,875] | 0,668 | -0,835 | 79 | 0,0005 | |
| Twin vague 4, plancher de bruit | -1,964 | [-2,151 ; -1,796] | 0,729 | -0,733 | 10 | 0,0005 | |

[MESURE] **H1 a H4 sont confirmees, toutes les quatre apres correction de Holm.** Le p de
permutation est a la resolution du test, 1 sur 2 001, dans une famille de quatre.

[MESURE] **Le plancher de bruit est de 0,07 sur le GSS et de 0,10 sur Twin** : la
reinterrogation des memes personnes deplace la pente de moins d'un dixieme. Toute
difference de pente inferieure a 0,1 ne doit pas etre commentee.

[MESURE] **Les deux jeux donnent la meme pente a 0,15 pres**, -2,22 sur 79 items du GSS et
-2,07 sur dix items de Twin, alors que les items, l'echelle, le mode de recrutement et
l'annee different. C'est le controle externe le plus fort du rapport.

### 3.2 Le signe du rapport se lit sur le signe de la derive

`a37-gss-par-item.csv`.

| | items | dont le rapport va dans le sens predit |
|---|---|---|
| **derive negative, la majorite penche a gauche** | **60** | **56** |
| **derive positive, la majorite penche a droite** | **19** | **16** |
| total | 79 | **72, soit 91 pour cent** |

[MESURE] **Le premier parametre de Brandt et Sleegers est verifie, et il est massif** : 60
des 79 items orientes penchent a gauche, derive moyenne -0,119. C'est l'hypothese qu'ils
tirent d'Ellis et Stimson, et elle tient sur nos donnees.

[MESURE] **Le second parametre n'est pas verifie.** Ils supposent que l'etiquette
ideologique penche a droite. Sur les sept points de `polviews`, la position moyenne de
l'echantillon de Stanford vaut 0,465 sur une echelle de 0 a 1, soit une derive de
**-0,035, a gauche**. Sur les cinq points de `QID22` de Twin, elle vaut **-0,067, a gauche**
aussi. Les deux echantillons sont plus a gauche que la population americaine, ce qui est
un fait connu du recrutement en ligne. **Consequence a tirer honnetement : nous verifions
la consequence item par item du modele sans que sa seconde premisse tienne dans nos
donnees.** Cela ne refute pas le modele, cela dit que la partie operante de leur mecanisme
est la derive des items, pas celle de l'etiquette.

### 3.3 Les inversions de `a30` etaient l'effet de la derive, et personne ne l'avait vu

Moyennes par famille de sujets du GSS, calculees sur les items orientes de chaque famille.

| famille | items | derive moyenne | dispersion gauche | dispersion droite | rapport |
|---|---|---|---|---|---|
| libertes civiles | 8 | **-0,302** | 0,217 | 0,361 | 1,666 |
| **avortement** | 7 | **-0,244** | 0,160 | 0,396 | **2,469** |
| roles de genre | 5 | -0,174 | 0,535 | 0,668 | 1,249 |
| depenses publiques | 17 | -0,150 | 0,463 | 0,568 | 1,225 |
| autres, social | 24 | -0,086 | 0,423 | 0,501 | 1,185 |
| confiance institutions | 11 | -0,031 | 0,544 | 0,576 | 1,058 |
| **fin de vie** | 5 | **+0,018** | 0,378 | 0,352 | **0,932** |
| **autres, economique** | 2 | **+0,232** | 0,537 | 0,449 | **0,835** |

[MESURE] **L'ordre des huit familles par la derive est exactement l'ordre par le rapport,
sans une inversion.** Les deux familles ou `a30` trouvait un rapport inferieur a 1, la fin
de vie et l'economique personnel, sont exactement les deux familles dont la derive est
positive. Les items nommes dans `a30` se rangent au bon endroit : `cappun` derive +0,122 et
rapport 0,634 ; `courts` +0,154 et 0,650 ; `polhitok/y` +0,157 et 0,733 ; `nataid/y`
+0,318 et 0,436 ; a l'autre bout `abrape` -0,384 et 5,64, `spkhomo/y` -0,438 et 3,51,
`natenvir/y` -0,273 et 2,65.

[CONFIRME] `corpus/lecture-complete/05` ecrit que cette correspondance « n'a ete relevee
par personne ». Elle est ici chiffree : ce n'etait pas une liste d'exceptions, c'etait une
droite.

---

## 4. Ce qui reste du 1,122 une fois la derive controlee

`a37-decomposition.csv`.

| quantite | valeur | intervalle | p |
|---|---|---|---|
| rapport global **observe**, sur les 79 items orientes | **1,2205** | [1,1822 ; 1,2597] | |
| rapport global du **temoin de position** | **1,2106** | [1,1751 ; 1,2449] | |
| **ecart, observe moins temoin** | **+0,0099** | [-0,0016 ; 0,0201] | 0,072 |
| rapport attendu **a derive nulle** (ordonnee de H1) | 1,0403 | [1,0048 ; 1,0719] | 0,026, Holm 0,052 |
| part de la variance item par item du log du rapport expliquee par le temoin | **0,981** | | |
| part expliquee par la derive agregee seule (R2 de H1) | 0,677 | [0,583 ; 0,713] | |

[MESURE] **H6 n'est pas rejetee : le temoin de position reproduit le rapport global.** Un
modele qui ne connait que la position moyenne de chaque camp, item par item, produit 1,211
la ou la mesure donne 1,220. L'ecart de 0,010 a un intervalle qui contient zero et un p de
0,072.

[MESURE] **H5 n'est pas rejetee apres correction.** Le rapport attendu pour un item de
derive nulle vaut 1,040 [1,005 ; 1,072], p de 0,026 qui devient 0,052 apres Holm dans une
famille de trois. Il reste donc peut etre une asymetrie de 4 pour cent que la derive
n'explique pas, mais elle ne passe pas la correction, et elle est du meme ordre que le
plancher de 1,073 que `a30` mesurait sur les items non attitudinaux.

[MESURE] **Le chiffre a retenir est le 0,981.** Le temoin de position explique 98 pour
cent de la variance item par item du logarithme du rapport. La derive agregee seule, qui
n'est qu'un resume a une dimension de la meme information, en explique 68 pour cent.

**Le controle qui empeche de lire une tautologie.** Sur un item binaire, la position
determine entierement la loi, donc le temoin ne peut pas se tromper et sa part expliquee
vaut 1 par construction. 33 des 79 items orientes sont binaires. La quantite lisible est
donc la meme mesure sur les 46 items a plus de deux modalites, ou le temoin peut echouer.

| sous ensemble | items | rapport observe | rapport du temoin | part de variance expliquee par le temoin | pente | R2 de la derive |
|---|---|---|---|---|---|---|
| items binaires | 33 | 1,4976 | 1,4976 | **1,000 par construction** | -2,572 | 0,709 |
| **items a plus de deux modalites** | **46** | **1,1260** | **1,1183** | **0,914** | -1,551 | 0,663 |

[MESURE] **La ou le temoin peut se tromper, il ne se trompe presque pas** : sur les 46
items a plus de deux modalites, il explique 91,4 pour cent de la variance du logarithme du
rapport et reproduit 1,1183 du 1,1260 observe. Le resultat de la section n'est donc pas un
artefact des items binaires.

[PROBABLE] **La phrase defendable est donc : la dispersion interne d'un camp sur un item
n'est pas une propriete du camp, c'est une consequence de sa position.** Un camp proche
d'un bord d'echelle a peu de dispersion possible ; la gauche est proche du bord sur les
sujets ou l'opinion a derive dans son sens, la droite sur les sujets ou elle a derive dans
le sien. Sur un item binaire cette equivalence est une identite arithmetique, verifiee ici
au dernier chiffre. **Ce n'est pas un artefact qui invaliderait le 1,122 : c'est le
mecanisme que Brandt et Sleegers obtiennent par simulation, et il est ici mesure.**

[MESURE] Attention a un piege de lecture : le rapport global sur les 79 items orientes
vaut **1,2205** et non 1,1225. Les deux chiffres ne portent pas sur le meme jeu d'items.
Les 79 items orientes sont, par construction, les items politiques et moraux ; les 70
autres, non orientables, tirent la moyenne des 149 vers 1. **Le 1,1225 de `a30` reste le
chiffre a citer pour les 149 items ; le 1,2205 est le chiffre du sous ensemble orientable
et ne doit jamais etre substitue au premier.**

---

## 5. Volet 2, ce que la simulation fait de la pente

### 5.1 Les six conditions de Stanford, 1 052 personnes, memes 79 items

`a37-agents-gss.csv`. Ecart mesure sur le meme tirage de bootstrap que les humains, donc
apparie personne par personne. Holm dans une famille de douze.

| condition | pente | intervalle | ecart aux humains | intervalle de l'ecart | p Holm | items utilisables | items ou la gauche est unanime |
|---|---|---|---|---|---|---|---|
| **humains vague 1** | **-2,219** | [-2,600 ; -1,941] | | | | 79 | 0 |
| humains vague 2, plancher | -2,145 | [-2,501 ; -1,855] | +0,074 | [-0,173 ; 0,325] | 0,545 | 79 | 0 |
| agents persona (v7) | -1,884 | [-2,381 ; -1,394] | +0,335 | [-0,184 ; 0,904] | 0,390 | 76 | 2 |
| agents demographiques (v6), sans etiquette | -1,689 | [-2,155 ; -1,271] | +0,530 | [0,008 ; 1,055] | 0,180 | 73 | 6 |
| agents composite | -3,796 | [-4,305 ; -3,394] | -1,577 | [-1,954 ; -1,247] | **0,006** | 79 | 0 |
| agents enquete | -3,796 | [-4,523 ; -3,290] | -1,577 | [-2,213 ; -1,113] | **0,006** | 78 | 1 |
| agents entretien (v3) | -5,370 | [-5,869 ; -4,475] | -3,152 | [-3,600 ; -2,285] | **0,006** | 73 | 3 |
| **agents demographiques (v8), avec etiquette** | **-12,414** | [-12,888 ; -7,736] | **-10,195** | [-10,689 ; -5,425] | **0,006** | 63 | **12** |
| B1 regression logistique | -5,247 | [-5,600 ; -4,640] | -3,029 | [-3,391 ; -2,302] | **0,006** | 70 | 8 |
| B2 plus proches voisins | -3,837 | [-4,301 ; -3,304] | -1,619 | [-1,980 ; -1,095] | **0,006** | 70 | 9 |
| B3 foret aleatoire | -4,117 | [-4,559 ; -2,337] | -1,898 | [-2,311 ; -0,040] | 0,180 | 45 | 28 |
| B0 tirage dans la marginale | -0,053 | [-0,209 ; 0,117] | +2,165 | [1,861 ; 2,574] | **0,006** | 79 | 0 |
| B0 mode | -0,012 | [-0,170 ; 0,143] | +2,206 | [1,907 ; 2,601] | **0,006** | 6 | 73 |

[MESURE] **A1 est confirmee pour six conditions sur douze apres Holm.** Les trois
conditions riches en information sur la personne (composite, enquete, entretien) et la
condition demographique a etiquette (v8) redressent la pente ; les deux conditions
demographiques sans etiquette (v6, v7) ne s'ecartent pas de la valeur humaine apres
correction ; la vague 2 humaine ne s'en ecarte pas non plus, ce qui valide le plancher.

[MESURE] **Le temoin `B0 tirage` tombe exactement ou il doit tomber, -0,053.** Un
predicteur qui tire dans la marginale de la population entiere donne la meme distribution
dans les deux camps, donc un rapport de 1 sur chaque item, donc une pente nulle. La mesure
detecte bien l'absence de structure quand il n'y en a pas.

[MESURE] **`agents v8` porte la pente a -12,41, soit 5,6 fois la valeur humaine**, et il y
arrive en rendant le camp de gauche simule unanime sur douze items. Sur ces douze items le
rapport est infini et le logarithme n'existe pas : la pente est calculee sur 63 items
seulement, et **elle sous estime donc l'effet.**

[MESURE] Un fait secondaire mais net. Lue sur l'abscisse humaine tenue fixe au lieu de sa
derive propre, la pente de `v8` tombe a **-7,57** au lieu de -12,41 : une partie de sa
raideur vient de ce que sa **propre** derive est comprimee (derive moyenne -0,095 contre
-0,119 chez les humains), pas seulement de ce que ses rapports sont exageres. Les deux
colonnes sont dans le tableau, elles ne doivent jamais etre confondues.

### 5.2 C2 contre C3, les memes 150 personnes, memes 79 items

`a37-agents-gss-150.csv`. C'est le seul perimetre ou C2 et C3 existent.

| condition | pente | intervalle | ecart aux humains | p Holm | items utilisables | **items ou la gauche est unanime** |
|---|---|---|---|---|---|---|
| **humains vague 1** | **-2,161** | [-3,037 ; -1,459] | | | 79 | **0** |
| humains vague 2 | -2,000 | [-3,015 ; -1,414] | +0,161 | 1,000 | 79 | 0 |
| **C3, sans etiquette** | **-1,887** | [-2,854 ; -0,962] | **+0,274** | **1,000** | 71 | **8** |
| **C2, avec etiquette** | -2,733 | [-3,307 ; -1,360] | -0,572 | 1,000 | **46** | **31** |
| agents demographiques (v6) | -1,057 | [-1,987 ; -0,197] | +1,104 | 0,220 | 67 | 10 |
| **agents v8, avec etiquette** | **-6,268** | [-7,352 ; -2,828] | -4,107 | 0,220 | 53 | **20** |
| agents composite | -3,395 | [-4,400 ; -2,511] | -1,234 | **0,024** | 76 | 1 |
| agents entretien (v3) | -4,188 | [-4,921 ; -2,689] | -2,026 | **0,044** | 70 | 7 |
| agents enquete | -3,570 | [-4,366 ; -2,394] | -1,408 | 0,220 | 76 | 2 |

[MESURE] **A3 est confirmee : C3, sans etiquette, donne -1,887 [-2,854 ; -0,962] contre
-2,161 chez les memes humains, ecart +0,274 avec un p de 0,377 et un p de Holm de 1,000.**
La condition sans etiquette reproduit la pente humaine.

[MESURE] **La pente de C2 ne doit pas etre lue comme une pente.** Elle vaut -2,733, ce qui
semble modere, mais elle est calculee sur **46 items sur 79** : sur les 33 autres, le camp
de gauche simule est unanime ou quasi unanime et le rapport est infini. **Le chiffre a
publier pour C2 n'est pas sa pente, c'est le 31 sur 79.** C'est la meme lecon qu'en `a30`
section 7.3, ou le chiffre a publier n'etait pas le rapport de 75,2 mais le zero au
denominateur.

[MESURE] **L'unanimite tombe exactement la ou le modele generatif predit qu'elle tombe.**
La derive moyenne des items ou la gauche simulee devient unanime vaut **-0,286 chez C2** et
**-0,294 chez v8**, contre **-0,119** sur l'ensemble des 79 items. **L'etiquette pousse a
l'unanimite le camp du cote du consensus, precisement sur les items ou la derive agregee
est la plus forte.** C'est la caricature du mecanisme, pas son effacement.

### 5.3 A2, le contraste d'etiquette

`a37-agents-contrastes.csv`. Les deux conditions d'un couple sont recalculees sur
exactement le meme tirage de personnes. Deux ordonnees sont rapportees : le logarithme du
rapport, qui est la mesure principale mais devient infini des qu'un camp est unanime, et
la **difference** de dispersion, qui est toujours finie et qui sert precisement quand la
premiere est censuree.

| perimetre | avec etiquette | sans etiquette | pente avec | pente sans | ecart | intervalle | p Holm | items unanimes avec / sans |
|---|---|---|---|---|---|---|---|---|
| 150 personnes | **C2** | **C3** | -2,733 | -1,887 | -0,846 | [-1,847 ; 0,832] | 0,487 | **31 / 8** |
| 150 personnes | agents v8 | agents v6 | -6,268 | -1,057 | -5,211 | [-6,419 ; -1,539] | **0,010** | 20 / 10 |
| 1052 personnes | agents v8 | agents v6 | -12,414 | -1,689 | -10,725 | [-11,217 ; -6,050] | **0,0015** | 12 / 6 |

Les memes trois couples, sur la **difference** de dispersion, qui n'est jamais censuree :

| perimetre | couple | pente avec | pente sans | ecart | intervalle | p Holm |
|---|---|---|---|---|---|---|
| 150 personnes | **C2 contre C3** | -0,423 | -0,281 | **-0,142** | [-0,256 ; -0,026] | **0,018** |
| 150 personnes | v8 contre v6 | -0,847 | -0,151 | -0,696 | [-0,812 ; -0,539] | **0,0015** |
| 1052 personnes | v8 contre v6 | -0,819 | -0,189 | -0,630 | [-0,675 ; -0,582] | **0,0015** |

[MESURE] **A2 est confirmee sur les trois couples avec la mesure non censuree, et sur deux
couples sur trois avec le logarithme.** Le couple C2 contre C3 n'est pas concluant sur le
logarithme, avec un intervalle [-1,847 ; 0,832] qui contient zero, **et la raison est
mecanique** : 33 des 79 items sont censures cote C2 contre 8 cote C3, et ce sont les items
ou l'effet est le plus fort qui sont jetes. Sur la difference de dispersion, le meme couple
donne un ecart de -0,142 [-0,256 ; -0,026], p de Holm 0,018.

[PROBABLE] **L'etiquette ideologique dans l'invite ne deplace pas seulement le niveau de la
variete, elle deplace la pente du mecanisme.** Trois contrastes apparies vont dans le meme
sens, deux d'entre eux sont concluants sur les deux mesures, le troisieme sur la seule
mesure que la censure n'atteint pas. C'est un cran au dessus de ce que `a30` pouvait
ecrire, ou un seul contraste sur trois excluait zero et de justesse.

### 5.4 Twin, quinze configurations, dix items

`a37-agents-twin.csv`.

| condition | pente | intervalle | R2 |
|---|---|---|---|
| **humains vague 4** | **-1,964** | [-2,137 ; -1,806] | 0,729 |
| gemini flash 2.5 texte | **-25,509** | [-29,773 ; -22,448] | 0,872 |
| gpt41 json | -11,543 | [-13,282 ; -10,105] | 0,791 |
| gpt41mini json predout | -9,202 | [-10,999 ; -7,848] | 0,603 |
| gpt41mini demo seules | -7,145 | [-9,713 ; -5,385] | 0,236 |
| gpt41mini texte raisonnement | -6,114 | [-7,401 ; -5,115] | 0,334 |
| gpt41 json predout | -6,078 | [-7,111 ; -5,107] | 0,309 |
| gpt41mini defaut | -6,053 | [-7,210 ; -5,184] | 0,470 |
| gpt41mini texte, temperature par defaut | -5,611 | [-6,654 ; -4,790] | 0,480 |
| gpt41mini texte repetition | -5,020 | [-5,773 ; -4,402] | 0,571 |
| gpt41mini json | -4,185 | [-5,655 ; -2,954] | 0,475 |
| gpt41mini finetune500 | **+0,402** | [0,150 ; 0,673] | 0,067 |
| gpt41mini resume | -0,058 | [-2,374 ; 1,938] | 0,000 |
| gpt41mini resume json | **+7,981** | [6,131 ; 9,964] | 0,206 |

[MESURE] **Douze configurations sur quinze redressent la pente au dela de la valeur
humaine**, de -4,19 a -25,51 contre -1,96. Trois font autre chose : les deux configurations
« resume » et la configuration ajustee sur 500 exemples.

[MESURE] **Les deux configurations qui inversent ou effacent la pente sont exactement les
deux qui ecrivent des reponses hors de l'echelle** : `gpt41mini_resume` produit 552
reponses hors des cinq points proposes, `gpt41mini_resume_json` en produit 1 494. Elles
sont comptees manquantes ici. Leur resultat ne doit pas etre lu comme un fait de
mecanisme.

[MESURE] **Un ecart de protocole avec `a30`, a signaler.** `a30` code les items de Twin
avec `coder_numerique_commun`, qui construit la table des modalites a partir des valeurs
rencontrees dans tous les fichiers. Sur `QID287`, les valeurs hors echelle de ces deux
configurations font passer la table de cinq a neuf modalites, et le score de position n'a
alors plus de sens. `a37` impose l'echelle a cinq points declaree et compte le reste
manquant. Sur les dix items politiques, cet ecart de codage inversait le signe de la pente
humaine de Twin. **Aucun chiffre de `a30` n'est affecte** : `a30` ne calcule aucune
position, seulement des dispersions, et une dispersion est invariante par renommage des
modalites. Mais toute mesure future de **position** sur Twin doit imposer l'echelle.

---

## 6. Volet 3, la correction demandee sur la densite de sous graphe

`a37-densite-deux-variantes.csv`, `a37-densite-composition.csv`. Aucun calcul nouveau sur
les microdonnees : les deux tableaux de `a30_resin_twin.py` sont remis en forme.

### 6.1 Ce que `a30` disait, et ce qu'il faut dire

`a30` interdiction numero 8 : « interdit de reprendre une densite de sous graphe partisan
sans nombre de noeuds egalise : le rapport passe de 0,540 a 0,894 par ce seul controle ».

[CONFIRME] `corpus/lecture-complete/05` corrige ce diagnostic apres lecture integrale du
depot de code des auteurs (`github.com/yijingch/broken-egg-polarization`,
`src/polar_measures.py`) : leur `get_density_weighted` divise la somme des poids d'arete
par le nombre de paires de noeuds **du sous graphe lui meme** issues d'items differents.
Le denominateur suit donc deja la taille du sous graphe.

[MESURE] Verification faite sur notre propre code : `a30_resin_twin.densite` calcule
`sub[eligible].sum() / eligible.sum()`, c'est a dire la moyenne des poids d'arete sur les
paires eligibles **du sous graphe**. Notre denominateur suit lui aussi la taille du sous
graphe. **La dependance residuelle au nombre de noeuds n'est donc pas un artefact de
denominateur, et la variante brute n'est pas fausse.**

### 6.2 Les deux variantes cote a cote, et ce que chacune mesure

Humains de Twin, vagues 1 a 3, 540 personnes par camp, 200 tirages a effectifs egaux.

| variante | noeuds droite | noeuds gauche | densite droite | densite gauche | rapport | intervalle |
|---|---|---|---|---|---|---|
| **brut** | 33 | 17 | 0,079 | 0,147 | **0,540** | [0,531 ; 0,549] |
| **egalise** | 17 | 17 | 0,131 | 0,147 | **0,894** | [0,874 ; 0,914] |
| sans neutre | 25 | 15 | 0,105 | 0,181 | 0,580 | [0,567 ; 0,593] |
| **egalise, vague 4, controle** | 17 | 17 | 0,139 | 0,149 | **0,935** | [0,912 ; 0,955] |

**Ce que chacune mesure, en une phrase.**
La variante **brute** repond a : *le stock de positions que ce camp detient effectivement
est il serre ?* Elle prend le camp tel qu'il est, avec toutes les modalites qu'il domine,
y compris les modalites neutres et rares. Elle mesure la coherence du repertoire complet
du camp.
La variante **egalisee** repond a : *les positions les plus caracteristiques de ce camp, a
nombre egal, sont elles serrees ?* Elle prend les dix sept modalites les plus
distinctivement de droite et les dix sept les plus distinctivement de gauche. Elle mesure
la coherence du noyau du camp, a taille de noyau imposee.
La variante **sans neutre** repond a la meme question que la brute, en retirant les dix
modalites « ni l'un ni l'autre ».

**Aucune ne remplace l'autre.** L'ecart entre les deux, 0,540 contre 0,894, n'est pas un
biais corrige : c'est la mesure de l'absorption des positions neutres par le camp de
droite, qui est le phenomene decrit par Luders et par Chen, pas un artefact qui le masque.

### 6.3 La composition, qui explique l'ecart entre les deux variantes

`a37-densite-composition.csv`, humains vagues 1 a 3.

| partage | camp | noeuds | dont neutres | taux d'endossement moyen | noeuds endosses par moins de 10 pour cent |
|---|---|---|---|---|---|
| brut | droite | 33 | **8 sur 10** | **0,221** | **3** |
| brut | gauche | 17 | 2 | **0,410** | 0 |
| egalise | droite | 17 | 2 | 0,251 | **0** |
| egalise | gauche | 17 | 2 | 0,410 | 0 |
| sans neutre | droite | 25 | 0 | 0,232 | 3 |
| sans neutre | gauche | 15 | 0 | 0,432 | 0 |

[MESURE] **Le camp de droite detient 33 modalites endossees en moyenne par 22 pour cent de
ses membres ; le camp de gauche en detient 17 endossees en moyenne par 41 pour cent.** Les
seize modalites que la droite detient en plus sont des modalites peu endossees, dont huit
des dix « ni l'un ni l'autre », et une modalite rare a un phi faible avec presque tout.
[PROBABLE] C'est cette composition, et non le denominateur, qui fait passer le rapport de
0,540 a 0,894.

### 6.4 Un fait nouveau : les agents ne reproduisent pas cette composition

Ecart entre les deux variantes, rapport egalise moins rapport brut, pour chaque condition.
Le partage des noeuds est celui des humains dans toutes les lignes, comme en `a30`.

| condition | rapport brut | rapport egalise | **ecart** | modalites employees sur 50 |
|---|---|---|---|---|
| **humains vagues 1 a 3** | 0,540 | 0,894 | **+0,354** | 50 |
| humains vague 4 | 0,567 | 0,935 | +0,368 | 50 |
| gpt41mini texte, temperature par defaut | 0,502 | 0,824 | +0,323 | 50 |
| gpt41mini defaut | 0,523 | 0,808 | +0,284 | 49 |
| gpt41mini json | 0,455 | 0,691 | +0,236 | 48 |
| gpt41mini texte repetition | 0,454 | 0,678 | +0,224 | 50 |
| gpt41mini texte raisonnement | 0,438 | 0,650 | +0,211 | 50 |
| gpt41mini json predout | 0,585 | 0,715 | +0,130 | 49 |
| gpt41mini resume | 0,412 | 0,525 | +0,114 | 50 |
| gpt41mini resume json | 0,605 | 0,653 | **+0,049** | 50 |
| **gpt41mini demo seules** | 0,210 | 0,251 | **+0,041** | **38** |
| **gpt41mini finetune500** | 0,626 | 0,644 | **+0,018** | 50 |

[MESURE] **Chez les humains, egaliser le nombre de noeuds deplace le rapport de 0,354 ;
chez les agents, de 0,018 a 0,323.** Les deux vagues humaines donnent 0,354 et 0,368, soit
un plancher de bruit de 0,014 sur cet ecart. **Aucune configuration d'agents n'atteint la
valeur humaine.**

[PROBABLE] Deux lectures, qu'il ne faut pas confondre. Pour `demo_seules`, l'ecart faible
s'explique par le fait que la configuration n'emploie que 38 des 50 modalites : les seize
noeuds supplementaires de droite sont en partie vides, la densite brute est deja basse et
l'egalisation ne change presque rien. Pour `finetune500`, qui emploie les 50 modalites,
l'explication ne peut pas etre celle la : **le modele ajuste attribue aux modalites rares
et neutres du camp de droite une connectivite comparable a celle des modalites frequentes,
ce que les humains ne font pas.** Je n'ai pas separe les deux contributions item par item.

### 6.5 Ce que l'interdiction numero 8 de `a30` doit devenir

**Proposition de reformulation, a valider par Amir.**

> Obligatoire de publier une densite de sous graphe partisan dans ses deux variantes, avec
> le nombre de noeuds de chaque sous graphe et le nombre de modalites reellement employees.
> La variante brute repond a « le stock de positions de ce camp est il serre », la variante
> egalisee a « le noyau de ce camp, a taille imposee, est il serre ». Le denominateur suit
> deja la taille du sous graphe, chez Chen et chez nous : l'ecart entre les deux variantes,
> 0,540 contre 0,894 chez les humains de Twin, n'est pas un artefact a corriger, c'est la
> mesure de l'absorption des positions neutres par le camp de droite. Interdit, en
> revanche, de comparer une variante d'un jeu a l'autre variante d'un autre jeu.

---

## 7. Figure

`resultats/a37-figure-consensus.png` et `.svg`. Quatre panneaux, tous construits a partir
des tableaux et jamais recalcules dans le script de figure.

A. Humains du GSS : le logarithme du rapport de dispersion de chaque item contre la derive
agregee de cet item, 79 points, avec la droite de regression. L'avortement et les libertes
civiles sont coloriees, elles occupent le quart en haut a gauche.
B. Deux conditions de Stanford sur les memes 1 052 personnes et les memes items : `v8` avec
etiquette et `enquete` sans, chacune avec sa droite ; la droite humaine en tirets. Les
items ou le camp de gauche simule est unanime sont portes en triangles au bord haut : ils
n'ont pas d'ordonnee.
C. Nos deux conditions locales sur les memes 150 personnes, C2 avec etiquette et C3 sans,
avec les memes conventions. Les triangles rouges de C2 sont le resultat.
D. La pente de chaque condition avec son intervalle de bootstrap sur les personnes, et le
nombre d'items censures a cote de chaque point.

---

## 8. Ce que cela change a `ARBITRAGE.md`

`ARBITRAGE.md` porte, dans le paragraphe des mesures du soir : « la droite est bien plus
variee que la gauche sur le GSS, rapport 1,12, robuste a l'appariement demographique, mais
le centre l'est autant que la droite. (...) Le papier de la capture Reddit ne le mesurait
pas ; nous, oui. »

**Ce qui est faux dans cette phrase et doit etre corrige.** « Le papier ne le mesurait
pas ; nous, oui » ne tient plus. [CONFIRME] Ondish et Stern (2018) mesurent le meme fait
sur le GSS et l'ANES, plus de 80 000 personnes, environ 400 questions et environ quarante
ans, par une part de variance dans un modele one-with-many ; Brandt et ses coauteurs le
repliquent sur 376 129 Europeens ; Brandt et Sleegers en donnent un modele generatif.
**Notre 1,122 est une replication, pas une decouverte.**

**Ce qui reste vrai, et qui est plus etroit qu'ecrit.** Ce que la litterature ne fait pas
et que nous faisons, c'est mesurer la dispersion **sur les reponses individuelles
categorielles**, item par item, avec un intervalle de bootstrap sur les personnes et un
appariement demographique exact. Ondish et Stern travaillent en trois groupes sur une part
de variance agregee, Brandt sur des estimations par pays et par vague.

**Reformulation proposee de la phrase, a valider par Amir :**

> Sur les 149 items du GSS, la dispersion interne du camp de droite vaut 1,122 fois celle
> du camp de gauche, et le centre est indistinguable de la droite : la gauche est le camp
> le moins varie des trois. Ce fait est publie depuis 2018 sous le nom d'effet de consensus
> liberal ; nous le repliquons sur des reponses individuelles au lieu de scores agreges, et
> nous montrons qu'il n'est pas une propriete des camps mais une consequence de leur
> position : le rapport de dispersion d'un item est une fonction decroissante de la derive
> agregee de cet item, pente -2,22 [-2,56 ; -1,96], R2 0,68, et un temoin qui ne connait
> que la position reproduit 98 pour cent de l'effet (a37).

**Ce que ce rapport apporte a l'option A.** L'option A est « ce que la simulation efface »,
version minorites. `a30` y avait ajoute « la simulation n'efface pas, elle exagere ». `a37`
dit maintenant **quoi** elle exagere, et le nomme : elle exagere un mecanisme publie, dont
nous avons la forme fonctionnelle et la valeur humaine de reference. **La phrase a
defendre devient verifiable ligne a ligne :** chez les humains, la variete relative d'un
camp sur un item suit la derive agregee de cet item avec une pente de -2,2 ; une simulation
a etiquette porte cette pente a -12,4 et rend le camp du cote du consensus unanime sur
douze a trente et un items sur soixante dix neuf ; une simulation sans etiquette reproduit
la pente humaine. **C'est le premier endroit du dossier ou nous avons a la fois une loi
mesuree chez les humains, un plancher de bruit, et une deformation de cette loi par la
machine, la meme journee et sur les memes personnes.**

**Ce que cela ne change pas.** Aucun chiffre de `a30` n'est contredit. Le 1,1225 sur 149
items, le 0,989 du centre, le 2,469 de l'avortement, les rapports par condition et les
densites de sous graphe sont tous recalcules ou repris ici a l'identique. Les seuls ajouts
sont l'orientation des items, la derive, le temoin de position, et le codage a echelle
imposee pour les positions sur Twin.

---

## 9. Ce que je n'ai pas pu verifier

1. **L'orientation des items est la mienne, meme documentee.** 39 des 79 orientations sont
   de niveau [PROBABLE] et 14 de niveau [HYPOTHESE]. Le second codeur est automatique mais
   il est construit **sur les memes donnees**, ce qui le rend faible comme controle
   independant : il ne peut pas detecter une erreur systematique commune. Un troisieme
   codeur humain, ou une orientation prise dans un codebook publie, manque.
2. **La derive agregee est mesuree sur un seul point du temps.** Brandt et Sleegers parlent
   d'une derive au sens d'un mouvement ; nous mesurons une position moyenne a un instant.
   La vague 2, deux semaines plus tard, n'est pas une serie temporelle. Sans le GSS
   historique, je ne peux pas distinguer « l'opinion a derive vers la gauche sur cet item »
   de « l'opinion est a gauche sur cet item ».
3. **La position et la dispersion ne sont pas separables sur un item binaire.** C'est une
   identite arithmetique, pas une limite de mesure, et 33 des 79 items orientes sont
   binaires ; le temoin ne peut rien y apprendre. Le controle est fait en section 4, sur
   les 46 items a plus de deux modalites, ou la part expliquee tombe de 0,981 a 0,914 sans
   changer la conclusion. Ce qui reste non verifie, c'est le cas d'un item a beaucoup de
   modalites : nous n'en avons que trois a cinq modalites et aucun a sept ou plus dans le
   sous ensemble oriente.
4. **Le second parametre du modele n'est pas verifie et je n'ai pas teste ce que cela
   coute.** L'etiquette penche a gauche dans nos deux echantillons. Refaire la simulation
   de Brandt et Sleegers avec le signe observe chez nous dirait si le modele produit encore
   l'effet ; ce serait une simulation de leur modele, pas une mesure sur nos donnees, et je
   ne l'ai pas faite.
5. **La comparaison C2 contre C3 repose sur 150 personnes**, dont 63 a gauche et 42 a
   droite, et sur une mesure censuree sur 33 items. Le contraste ne devient concluant que
   sur la difference de dispersion. Le second echantillon de 150 personnes de `a21` n'est
   pas charge ici.
6. **Les items censures ne sont pas traites par un modele de censure.** Ils sont comptes et
   exclus, et une mesure de remplacement non censuree est rapportee a cote. Un modele de
   Tobit ou un rapport regularise donnerait une pente unique ; je n'ai pas voulu introduire
   un parametre de regularisation dans un rapport qui n'en contient aucun ailleurs.
7. **La composition du sous graphe n'est pas decomposee.** La section 6.4 constate que les
   agents ne reproduisent pas l'ecart entre les deux variantes de densite, et propose deux
   explications, l'absence de modalites et la connectivite des modalites rares. Je n'ai pas
   separe les deux contributions.
8. **Aucune analyse de sensibilite a l'ordre des modalites proposees** aux agents, limite
   deja ouverte dans `FAITS-ETABLIS` section 4 et qui vaut ici, d'autant plus que la
   position moyenne y est directement exposee.
9. **Les deux configurations « resume » de Twin sont hors protocole.** Elles produisent 552
   et 1 494 reponses hors de l'echelle a cinq points. Je les compte manquantes, ce qui est
   la decision la moins arbitraire, mais je n'ai pas verifie si ces reponses sont des
   erreurs de format ou une echelle differente employee par le modele.

---

## 10. Questions ouvertes pour Simon

1. **Le rapport de dispersion d'un item binaire est une fonction de sa position. Est ce que
   la litterature de l'effet de consensus liberal le sait ?** Ondish et Stern emploient une
   part de variance dans un modele one-with-many, pas un rapport de dispersion. Si leur
   mesure est elle aussi une fonction de la position, alors quarante ans de resultat
   tiennent a un fait arithmetique et le vrai enonce est « l'opinion americaine penche a
   gauche sur les items », ce qui est un enonce d'Ellis et Stimson et non de psychologie
   des camps. Y a t il une mesure de consensus intra camp qui soit orthogonale a la
   position ?
2. **Le second parametre de Brandt et Sleegers echoue dans nos deux echantillons et le
   resultat tient quand meme. Est ce attendu ?** Leur modele a besoin des deux hypotheses
   pour produire l'asymetrie agregee ; nous verifions la consequence item par item avec une
   seule. Est ce que la pente item par item est une prediction plus faible que l'effet
   agrege, ou une prediction differente ?
3. **Comment nommer une simulation qui exagere une loi au lieu de l'effacer ?** `a30`
   laissait ouverte la question du mot pour « caricature de la dispersion ». `a37` la
   precise : il y a une loi, elle a une pente, la machine la multiplie par 5,6 et pousse a
   l'unanimite du cote ou la loi predit deja le plus de consensus. Est ce que ce genre de
   deformation a un nom en modelisation, quelque chose comme une sur regression vers la
   pente ?
4. **La pente de -2,2 est elle une constante ou un chiffre d'epoque ?** Chen et ses
   coauteurs datent la centralite de l'avortement dans le camp democrate de 2020. Si la
   pente se lit sur l'ANES de 2000 a 2020, elle devient un objet historique et le 2,47 de
   l'avortement devient un point d'une serie. Vaut il la peine d'aller chercher l'ANES pour
   cela ?
5. **La densite brute et la densite egalisee mesurent deux choses differentes, et les
   agents ne reproduisent que la seconde. Est ce que quelqu'un a deja separe, dans un
   reseau de reponses, la coherence du noyau d'un camp et la coherence de son repertoire
   complet ?** Si non, c'est peut etre la mesure la plus originale du volet 3, et elle est
   gratuite : les deux colonnes sont deja calculees.

---

## 11. Reproduction

```
.venv/bin/python analyses/a37_humains.py --boot 1000 --perm 2000
.venv/bin/python analyses/a37_agents.py --boot 2000
.venv/bin/python analyses/a37_densite.py
.venv/bin/python analyses/a37_figure.py
```

Graine unique 20260908 dans `a37_commun.GRAINE`, la meme qu'en `a30`. Duree totale mesuree,
quatre coeurs : environ vingt secondes, dont cinq pour les humains et huit pour les agents.
`a37_agents.py` emploie les caches `/tmp/a25-matrices.pkl` et `/tmp/a28-foret.npy` produits
par `a25` et `a28` ; s'ils sont absents il les recalcule, ce qui ajoute quelques minutes de
foret aleatoire. `a37_densite.py` ne lit que des tableaux de `resultats/` et ne touche
aucune microdonnee.

**Fichiers produits.** Scripts : `analyses/a37_commun.py`, `a37_humains.py`,
`a37_agents.py`, `a37_densite.py`, `a37_figure.py`. Tableaux :
`a37-orientation-items.csv`, `a37-gss-par-item.csv`, `a37-twin-par-item.csv`,
`a37-regressions-humains.csv`, `a37-decomposition.csv`, `a37-agents-gss.csv`,
`a37-agents-gss-150.csv`, `a37-agents-par-item.csv`, `a37-agents-contrastes.csv`,
`a37-agents-twin.csv`, `a37-densite-deux-variantes.csv`, `a37-densite-composition.csv`.
Figure : `a37-figure-consensus.png` et `.svg`.
