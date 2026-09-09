# a20. Le transport de variance rejoue : les deux objections bloquantes de a17, corrigees

**Reponse en une ligne.** Les deux objections sont fondees et elles ne changent pas la
conclusion de a7, elles la deplacent : l'estimateur d'information mutuelle rend bien -0,10 a
-0,15 la ou la verite est zero, mais une nulle de permutation **appariee a la structure de
l'operateur** ramene ce residu a 0,000 sur les trois mesures [MESURE], et une fois cette
correction faite l'enonce central de a7 tient, "l'intervalle apres transport contient 1 pour
trois des quatre conditions", sous Gini Simpson comme sous l'entropie [MESURE] ; en revanche
l'enonce d'impossibilite de a7 doit etre coupe en deux, parce que **le plafond du ratio intra
depasse 1 pour quatre couples condition x axe sur huit sous la variance ordinale** et pour
aucun sous les deux mesures nominales [MESURE], **mais atteindre (1, 1) reste impossible sous
les trois mesures**, puisque cela exigerait un ratio de dispersion totale `T` egal a 1 et que
`T` vaut au mieux 0,954 [MESURE]. Rejoue sous la variance ordinale sur les 70 items ordinaux,
le transport amene le terme inter a 1 dans 15 des 16 configurations, y laisse le terme intra a
0,935 a 0,956 alors que le plafond vaut 1,044 a 1,053, et **echoue toujours au critere A6** :
le net de reparation est negatif dans les 32 lignes mesurees et la correlation de Spearman
entre distances humaines et simulees baisse dans les 16 cas [MESURE].

Date : 8 septembre 2026. Reproduction :
`.venv/bin/python analyses/a20_transport_variance_v2.py`, environ treize minutes, quatre
coeurs, **aucun appel de modele de langage**. `analyses/a7_transport_variance.py` n'a pas ete
modifie : il est importe, avec ses estimateurs, son operateur et ses decoupages.
`data/traces/` n'a pas ete lu.

---

## 0. Ce que ce rapport corrige, et ce qu'il ne touche pas

Deux objections de `a17-relecture-adverse.md`, classees bloquantes au rang 4 et au rang 5 de
son tableau final :

- **objection 4**, a17 section 3.1 : la correction de Miller Madow n'est pas invariante sous
  l'operateur de transport ; a lambda 0 le ratio inter estime vaut -0,136 alors que
  l'operateur annule l'information mutuelle empirique par construction, et ce biais depasse
  la demi largeur des intervalles publies ;
- **objection 5**, a17 section 3.2 : l'enonce d'impossibilite n'est etabli que sur deux des
  trois mesures de a1, et sur la troisieme le plafond depasse 1 ;
- accessoirement, **a17 section 3.3**, la troisieme verification de la meme section : le
  plafond publie par a7 est lu a lambda 0 et non a inter nul, et le `w` deduit des valeurs a
  lambda 1 (0,046) contredit celui deduit du plafond publie (0,053).

Ne sont pas traites ici, et restent ouverts : a17 section 3.4 (a7 n'applique pas la
soustraction du residu la ou a1 l'applique, ce rapport le fait mais ne recalcule pas
l'agregat des six axes de a1), 3.5 (24 cellules contre 48), 3.6 (le temoin de hasard a 0,167
plutot que 0,3497), et les quatre manques listes en 3.8.

Le protocole de a7 est garde entier : memes 149 items, memes 1 052 personnes, memes 5 blocs
d'items et 5 plis de personnes, meme graine 20260907, variantes naive et informee, temoin de
dilatation pure, deux axes de transport, calibration de lambda hors de l'item evalue.

---

## 1. Objection 4 : l'estimateur sous l'operateur

### 1.1 Le diagnostic de a17 est reproduit

A lambda 0, l'operateur force `p(r|s) = p(r)` pour tout segment : l'information mutuelle
empirique est nulle par construction. Un estimateur sans biais doit rendre zero. Axe
ideologie politique, valeurs du ratio inter [MESURE, `a20-lambda0-controle.csv`] :

| condition | M1 entropie, 149 items | M2 Gini Simpson, 149 items | M3 variance ordinale, 70 items |
|---|---|---|---|
| agents composite | **-0,1362** | **-0,1044** | **-0,0577** |
| agents enquete | -0,1352 | -0,1009 | -0,0565 |
| agents entretien (v3) | -0,1368 | -0,0997 | -0,0613 |
| agents demographiques (v8) | -0,1169 | -0,0949 | -0,0615 |

Les valeurs d'entropie reproduisent a la quatrieme decimale celles que a17 avait lues dans
`a7-trajectoires.csv`. **Le probleme n'est donc pas propre a l'entropie.** Gini Simpson, dont
a1 mesure un residu de permutation inferieur a 0,1 pour cent, rend -0,10 ; la variance
ordinale rend -0,06. La demi largeur d'intervalle bootstrap de ces memes quantites vaut 0,011
a 0,019 [MESURE] : le biais est de cinq a huit fois l'incertitude. **Changer de mesure
principale pour Gini Simpson ne suffit donc pas a corriger l'artefact.**

### 1.2 Deux nulles, et la lecture litterale ne corrige rien

Le residu de permutation a ete recalibre a chaque lambda, de deux facons.

- **Nulle A, permutation seule.** On permute les etiquettes de segment **sur la population
  deja transportee**. C'est la lecture litterale de la correction de a1.
- **Nulle B, permutation puis transport.** On permute les etiquettes sur la population
  d'origine, **puis on applique le meme transport au meme lambda** avec ces etiquettes
  permutees. La nulle porte alors la meme structure de quotas deterministes que la mesure.

Resultat, axe ideologie, mesure entropie, 149 items [MESURE] :

| condition | brut | apres nulle A | apres nulle B | demi largeur IC 95 % |
|---|---|---|---|---|
| agents composite | -0,1362 | **-0,1545** | **+0,0004** | 0,0169 |
| agents enquete | -0,1352 | -0,1527 | -0,0002 | 0,0170 |
| agents entretien (v3) | -0,1368 | -0,1562 | 0,0000 | 0,0161 |
| agents demographiques (v8) | -0,1169 | -0,1302 | 0,0000 | 0,0124 |

**La nulle A n'ameliore rien, elle aggrave.** La raison est mecanique et elle merite d'etre
ecrite : permuter les etiquettes sur la population transportee **rend au tableau croise le
bruit multinomial que le transport venait de lui retirer**. La nulle mesure alors le biais de
l'estimateur sur des donnees i.i.d., c'est a dire exactement ce que la correction de Miller
Madow corrige deja ; elle est aveugle a l'artefact. La correction telle qu'elle est enoncee
dans a1 ne peut donc pas etre transposee au transport sans changer sa construction.

**La nulle B ramene le residu a zero.** Elle a deux proprietes qu'il faut annoncer ensemble,
la bonne et la mauvaise.

1. A lambda 1 le transport est l'identite, donc la nulle B **redonne exactement le residu de
   permutation de a1** : la correction se raccorde a celle du rapport principal, et n'est pas
   un estimateur de plus [CONFIRME par construction, verifie numeriquement].
2. A lambda 0 l'annulation est **vraie par construction** et n'est donc pas un test
   independant : la nulle et la mesure produisent la meme configuration de quotas. Ce que la
   verification (c) etablit n'est pas que l'estimateur est sans biais, c'est que **le residu
   negatif publie par a7 est entierement imputable a la difference de structure entre les
   donnees transportees et les donnees i.i.d.**, et non a un signal residuel [MESURE].

Ce qui est reellement teste, c'est le comportement aux lambdas intermediaires. Il est
monotone et sans discontinuite : pour les agents composite en entropie, le ratio inter corrige
par la nulle B descend de 2,131 a lambda 1 jusqu'a 0,0004 a lambda 0, en passant par 0,987 a
lambda 0,7, la ou l'estimateur brut de a7 donne 2,130 puis -0,136 en passant par 0,924
[MESURE, `a20-trajectoires.csv`].

### 1.3 Verification (c), et sa limite

**Sur l'axe ideologie politique, oui, pour les trois mesures.** Le terme inter estime a lambda
0 vaut entre -0,0004 et +0,0006 selon la condition et la mesure, contre une demi largeur
d'intervalle de 0,011 a 0,019. Zero est dans l'intervalle dans les 20 cellules mesurees pour
la nulle B, et dans aucune pour la nulle A ni pour l'estimateur brut [MESURE].

**Sur l'axe profil croise, non, et ce n'est pas un defaut d'estimateur.** Le terme inter
corrige y vaut 0,102 a 0,489 selon la condition. La cause a ete mesuree plutot que supposee :
l'operateur de a7 ne transporte pas un couple (item, segment) de moins de 20 personnes.

| axe | segments | cellules transportees | part des cellules | part de la population |
|---|---|---|---|---|
| ideologie politique | 7 | 1 043 sur 1 043 | **100,0 %** | **100,0 %** |
| profil croise | 18 | 1 937 sur 2 682 | **72,2 %** | 93,4 % |

Sur le profil croise, **a lambda 0 l'operateur n'annule pas l'information mutuelle
empirique** : plus d'un quart des cellules n'est pas touche, et l'ecart entre segments qui
subsiste est du vrai signal non transporte. La phrase de a7 section 3, "a lambda egal 0, tout
ecart entre segments est supprime : c'est le maximum deplacable", **est fausse pour le profil
croise** [MESURE]. Elle reste vraie pour l'ideologie.

Consequence pour a17 : sa reconstitution de `w` et de `T`, qui resout l'identite a partir des
valeurs a lambda 0 et lambda 1, est valide sur l'ideologie et biaisee sur le profil croise.
C'est ce qui explique le seul desaccord chiffre entre son tableau et le mien, voir section 3.

---

## 2. Le tableau du critere 1, republie

Axe de transport : ideologie politique. Lambda calibre hors de l'item evalue, sur la mesure
principale Gini Simpson corrigee par la nulle B. Intervalles bootstrap a 95 pour cent,
400 tirages sur les personnes, recentres sur l'estimation ponctuelle, regle de a1.
[MESURE, `a20-avant-apres.csv`]

| condition | lambda | inter M2 avant | inter M2 apres | intra M2 avant | intra M2 apres | total |
|---|---|---|---|---|---|---|
| humains vague 2 (controle) | non transporte | 1,019 [0,982 ; 1,057] | | 1,003 [0,998 ; 1,007] | | 1,003 |
| agents composite | 0,7 | 2,154 | **1,053** [0,968 ; 1,145] | 0,843 | **0,901** | 0,909 |
| agents enquete | 0,6 | 2,516 | **0,908** [0,821 ; 0,995] | 0,792 | **0,877** | 0,878 |
| agents entretien (v3) | 0,6 | 2,822 | **1,016** [0,898 ; 1,137] | 0,764 | **0,859** | 0,867 |
| agents demographiques (v8) | 0,3 | 8,118 | **0,977** [0,861 ; 1,111] | 0,442 | **0,818** | 0,826 |

Meme tableau en entropie corrigee, mesure secondaire, au meme lambda :

| condition | inter M1 avant | inter M1 apres | intra M1 apres |
|---|---|---|---|
| agents composite | 2,131 | **0,987** [0,904 ; 1,068] | 0,889 |
| agents enquete | 2,525 | **0,850** [0,773 ; 0,924] | 0,858 |
| agents entretien (v3) | 2,788 | **0,933** [0,835 ; 1,032] | 0,862 |
| agents demographiques (v8) | 8,379 | **0,908** [0,800 ; 1,020] | 0,797 |

**Reponse a la question posee : "l'intervalle apres transport contient 1" tient.** Il tient
pour trois des quatre conditions sous Gini Simpson (composite, entretien, `v8`) et pour trois
des quatre sous l'entropie (les memes trois). La condition qui echoue est la meme que dans a7,
les agents enquete, mais **elle echoue dans l'autre sens** : a7 publiait, en entropie,
1,096 [1,014 ; 1,180], un sur ajustement ; a20 mesure 0,850 [0,773 ; 0,924] en entropie et
0,908 [0,821 ; 0,995] en Gini Simpson, une sur correction. La cause est le
lambda retenu, qui passe de 0,7 a 0,6 sur une grille au dixieme : a lambda 0,7 le ratio
corrige vaut 1,231, a lambda 0,6 il vaut 0,908, et l'ecart a 1 est plus petit pour 0,6
[MESURE, `a20-trajectoires.csv`]. Aucun lambda de la grille ne place cette condition sur 1.

**Ce que a17 predisait et qui n'est pas confirme.** a17 ecrivait : "la calibration s'arrete
donc trop tot, et le transport est systematiquement sous applique". Mesure : le lambda
calibre bouge d'au plus un cran, et dans les deux sens. Il est inchange pour les agents
composite (0,7) et les agents entretien (0,6), et il descend d'un cran pour les agents enquete
(0,7 vers 0,6) et pour `v8` (0,4 vers 0,3) [MESURE, `a20-lambda-calibre.csv`]. La correction
demande **davantage** de retrecissement, pas moins.

**Ce que a17 predisait et qui est confirme.** Sa re inflation grossiere donnait 0,99 pour les
agents composite ; la mesure au meme lambda 0,7 donne 0,987 en entropie [MESURE]. L'ordre de
grandeur de son objection etait juste.

**Le controle passe toujours.** Les humains de la vague 2, non transportes, tombent en
(1,019 ; 1,003) en Gini Simpson et (1,017 ; 1,004) en entropie, intervalles contenant 1 sur
les deux termes. Sous la variance ordinale, (1,039 ; 0,988), intervalles contenant 1
egalement [MESURE].

**Le cout en exactitude, variante informee, 149 items :**

| condition | a7 | a20 | ecart apparie a20 | IC de l'ecart |
|---|---|---|---|---|
| agents composite | 0,6750 | **0,6750** | -0,0090 | [-0,0101 ; -0,0079] |
| agents enquete | 0,6446 | **0,6410** | -0,0100 | [-0,0112 ; -0,0087] |
| agents entretien (v3) | 0,6430 | **0,6423** | -0,0142 | [-0,0158 ; -0,0128] |
| agents demographiques (v8) | 0,5282 | **0,5249** | -0,0343 | [-0,0375 ; -0,0311] |

Les ecarts se creusent legerement pour les deux conditions dont le lambda a baisse d'un cran.
Aucun intervalle ne contient zero : la conclusion de a7 section 4 est inchangee.

---

## 3. Objection 5 : `w`, `T` et le plafond, pour les trois mesures

### 3.1 Le tableau complet

`w` est la part du terme inter dans la dispersion totale **des humains** ; `T` est le ratio de
dispersion totale de la condition sur celle des humains ; le plafond du ratio intra quand le
terme inter est annule vaut `T / (1 - w)`. Contrairement a a17 qui reconstituait `w` et `T` en
resolvant l'identite entre lambda 0 et lambda 1, **les deux quantites sont ici mesurees
directement** sur la decomposition, ce qui evite le biais du profil croise decrit en 1.3.
[MESURE, `a20-plafond.csv`]

`w`, qui ne depend que des humains :

| axe | jeu d'items | M1 entropie | M2 Gini Simpson | M3 variance ordinale |
|---|---|---|---|---|
| ideologie politique | 149 items | 0,0460 | 0,0499 | sans objet |
| ideologie politique | 70 items ordinaux | 0,0439 | 0,0437 | **0,0887** |
| profil croise | 149 items | 0,0520 | 0,0542 | sans objet |
| profil croise | 70 items ordinaux | 0,0466 | 0,0442 | **0,0949** |

`T` et le plafond, par condition et par axe :

| condition | axe | jeu | mesure | `T` | plafond | plafond > 1 |
|---|---|---|---|---|---|---|
| composite | ideologie | 149 items | M1 | 0,8933 | 0,9364 | non |
| composite | ideologie | 149 items | M2 | 0,9087 | 0,9564 | non |
| composite | ideologie | 70 ordinaux | M1 | 0,8919 | 0,9328 | non |
| composite | ideologie | 70 ordinaux | M2 | 0,9106 | 0,9522 | non |
| composite | ideologie | 70 ordinaux | **M3** | 0,8969 | **0,9842** | non |
| composite | profil croise | 149 items | M1 | 0,8933 | 0,9423 | non |
| composite | profil croise | 149 items | M2 | 0,9087 | 0,9607 | non |
| composite | profil croise | 70 ordinaux | M1 | 0,8919 | 0,9354 | non |
| composite | profil croise | 70 ordinaux | M2 | 0,9106 | 0,9526 | non |
| composite | profil croise | 70 ordinaux | **M3** | 0,8969 | **0,9909** | non |
| enquete | ideologie | 149 items | M1 | 0,8583 | 0,8997 | non |
| enquete | ideologie | 149 items | M2 | 0,8783 | 0,9244 | non |
| enquete | ideologie | 70 ordinaux | M1 | 0,8575 | 0,8969 | non |
| enquete | ideologie | 70 ordinaux | M2 | 0,8761 | 0,9161 | non |
| enquete | ideologie | 70 ordinaux | **M3** | 0,8782 | **0,9637** | non |
| enquete | profil croise | 149 items | M1 | 0,8583 | 0,9053 | non |
| enquete | profil croise | 149 items | M2 | 0,8783 | 0,9286 | non |
| enquete | profil croise | 70 ordinaux | M1 | 0,8575 | 0,8994 | non |
| enquete | profil croise | 70 ordinaux | M2 | 0,8761 | 0,9166 | non |
| enquete | profil croise | 70 ordinaux | **M3** | 0,8783 | **0,9703** | non |
| entretien (v3) | ideologie | 149 items | M1 | 0,8649 | 0,9066 | non |
| entretien (v3) | ideologie | 149 items | M2 | 0,8669 | 0,9124 | non |
| entretien (v3) | ideologie | 70 ordinaux | M1 | 0,8898 | 0,9306 | non |
| entretien (v3) | ideologie | 70 ordinaux | M2 | 0,9004 | 0,9415 | non |
| entretien (v3) | ideologie | 70 ordinaux | **M3** | 0,9513 | **1,0439** | **oui** |
| entretien (v3) | profil croise | 149 items | M1 | 0,8649 | 0,9123 | non |
| entretien (v3) | profil croise | 149 items | M2 | 0,8669 | 0,9165 | non |
| entretien (v3) | profil croise | 70 ordinaux | M1 | 0,8898 | 0,9332 | non |
| entretien (v3) | profil croise | 70 ordinaux | M2 | 0,9004 | 0,9420 | non |
| entretien (v3) | profil croise | 70 ordinaux | **M3** | 0,9513 | **1,0510** | **oui** |
| `v8` | ideologie | 149 items | M1 | 0,8022 | 0,8409 | non |
| `v8` | ideologie | 149 items | M2 | 0,8256 | 0,8690 | non |
| `v8` | ideologie | 70 ordinaux | M1 | 0,8304 | 0,8686 | non |
| `v8` | ideologie | 70 ordinaux | M2 | 0,8485 | 0,8873 | non |
| `v8` | ideologie | 70 ordinaux | **M3** | 0,9535 | **1,0462** | **oui** |
| `v8` | profil croise | 149 items | M1 | 0,8022 | 0,8461 | non |
| `v8` | profil croise | 149 items | M2 | 0,8256 | 0,8729 | non |
| `v8` | profil croise | 70 ordinaux | M1 | 0,8304 | 0,8710 | non |
| `v8` | profil croise | 70 ordinaux | M2 | 0,8485 | 0,8877 | non |
| `v8` | profil croise | 70 ordinaux | **M3** | 0,9535 | **1,0534** | **oui** |

### 3.2 Ce qui change par rapport a a17 : quatre couples sur huit, pas cinq

a17 comptait cinq couples au dessus de 1 sous M3, en incluant composite x profil croise a
1,002. La mesure directe donne **0,9909** pour ce couple, donc **quatre sur huit** [MESURE].
J'ai reproduit la methode de reconstitution de a17 a partir de `a7-trajectoires.csv` : elle
donne bien 1,0019 pour ce couple. L'ecart vient de ce que sa methode resout l'identite en
utilisant la valeur a lambda 0, et que sur le profil croise l'operateur ne transporte que
72,2 pour cent des cellules : la valeur a lambda 0 n'est pas le point a inter nul, et la
resolution surestime `T` (0,9027 reconstitue contre 0,8969 mesure). **Sur l'ideologie, ou la
couverture est de 100 pour cent, sa reconstitution et ma mesure coincident a la troisieme
decimale** (0,9840 contre 0,9842 pour composite ; 1,0447 contre 1,0439 pour entretien).

### 3.3 Verification (c) de a17, section 3.3 : le plafond publie par a7 etait le mauvais

a17 objectait que a7 publie comme plafond la valeur du ratio intra lue **a lambda 0**, ou le
terme inter estime vaut -0,13 et non 0, et que le plafond a inter strictement nul vaut 0,936
et non 0,943. C'est exact, et l'incoherence interne qu'il signalait disparait.

| condition, axe ideologie, entropie | a7, intra lu a lambda 0 | a20, plafond a inter nul `T/(1-w)` | a20, intra corrige lu a lambda 0 |
|---|---|---|---|
| agents composite | 0,943 | **0,9364** | 0,9356 |
| agents enquete | 0,906 | **0,8997** | 0,8989 |
| agents entretien (v3) | 0,913 | **0,9066** | 0,9060 |
| agents demographiques (v8) | 0,846 | **0,8409** | 0,8401 |

Les deux colonnes de droite coincident maintenant a la troisieme decimale, alors que a7
publiait un plafond incompatible avec son propre `w`. Les valeurs de a17 (0,936 ; 0,899 ;
0,906 ; 0,840) sont retrouvees a la quatrieme decimale [MESURE].

### 3.4 L'enonce d'impossibilite, reecrit, et une correction a a17

L'enonce de a7 section 0 melangeait deux affirmations qu'il faut separer.

**Affirmation 1, sur le plafond du seul terme intra. Elle depend de la mesure.**

> Sous M1 (entropie) et sous M2 (Gini Simpson), sur les 149 items comme sur les 70 items
> ordinaux, le plafond du ratio intra a terme inter nul est **en dessous de 1 pour les huit
> couples condition x axe**, entre 0,841 et 0,961. Sous M3 (variance ordinale), sur les 70
> items ordinaux, il est **au dessus de 1 pour quatre couples sur huit** : les agents
> entretien et les agents demographiques `v8`, sur les deux axes, avec des valeurs de 1,044 a
> 1,053. Pour les agents composite et les agents enquete, il reste en dessous, a 0,964 a
> 0,991. [MESURE]

**Affirmation 2, sur le point (1, 1). Elle ne depend d'aucune mesure, et a17 se trompe en
disant que l'impossibilite disparait.**

L'identite `T = w x ratio_inter + (1 - w) x ratio_intra` impose que si les deux ratios valent
1, alors `T` vaut 1. Or `T` mesure **0,802 a 0,954** sur les 40 couples condition x axe x jeu
x mesure de ce rapport, sans exception [MESURE]. **Aucun operateur a somme constante ne peut
donc amener une de ces quatre conditions en (1, 1), sous aucune des trois mesures.** Ce que
le plafond superieur a 1 autorise, c'est d'atteindre `ratio_intra = 1` **seul**, et au prix
d'un ratio inter qu'on peut chiffrer, `inter = (T - (1 - w)) / w` :

| couple ou le plafond depasse 1 | `w` | `T` | ratio inter requis pour amener l'intra a 1 |
|---|---|---|---|
| entretien x ideologie, M3 | 0,0887 | 0,9513 | **0,45** |
| entretien x profil croise, M3 | 0,0949 | 0,9513 | **0,49** |
| `v8` x ideologie, M3 | 0,0887 | 0,9535 | **0,48** |
| `v8` x profil croise, M3 | 0,0949 | 0,9535 | **0,51** |

Autrement dit, la ou le transport pur peut restaurer la dispersion intra groupe, il ne le peut
qu'en **effacant la moitie de l'ecart entre segments qui existe reellement chez les humains**.
Ce n'est pas une correction, c'est un echange d'une distorsion contre une autre, de signe
oppose. La phrase de a17, "sur cette mesure le transport pur suffit et l'impossibilite
annoncee disparait", est donc a nuancer : elle vaut pour le terme intra pris seul, pas pour la
cible (1, 1).

**Corollaire sur le chiffre le plus cite de a7.** a17 a raison : `w` n'est pas "4,6 pour
cent" tout court. Il vaut 0,046 en entropie sur les 149 items, 0,050 en Gini Simpson sur les
149 items, 0,044 en entropie comme en Gini Simpson sur les 70 items ordinaux, et **0,089 en
variance ordinale** [MESURE]. La phrase "chez les humains, l'ideologie politique declaree
n'explique que 4,6 pour cent de l'entropie des reponses au GSS" reste exacte avec le mot
entropie ; sans lui, elle ne l'est pas.

**Ou est loge le deficit de dispersion totale.** `T` est nettement plus proche de 1 sous M3
que sous M1 et M2 pour les agents entretien (0,951 contre 0,865 a 0,900) et pour `v8` (0,954
contre 0,802 a 0,849), et il ne l'est pas pour les agents composite (0,897 contre 0,892 a
0,911) ni pour les agents enquete (0,878 contre 0,858 a 0,878) [MESURE]. M3 ne voit que la
position sur l'echelle ordinale ; M1 et M2 voient aussi quelles modalites sont employees.
Lecture : **pour les agents entretien et `v8`, le deficit de dispersion est un deficit de
repertoire de modalites, pas un deficit d'etalement sur l'echelle** ; pour les agents
composite et enquete, il est present dans les deux [PROBABLE, la mesure est nette mais
l'interpretation par le repertoire n'a pas ete testee directement].

---

## 4. Le transport rejoue sous M3, sur les 70 items ordinaux

Lambda calibre hors item sur le terme inter M3 corrige, transport applique aux seuls 70 items
ordinaux. Variante informee ; les ratios de la variante naive sont identiques par
construction, seuls les intervalles et l'exactitude different.
[MESURE, `a20-m3-ordinal.csv`]

| condition | axe | lambda | inter avant | inter apres | intra avant | intra apres | plafond | 1 dans IC inter | 1 dans IC intra |
|---|---|---|---|---|---|---|---|---|---|
| composite | ideologie | 0,7 | 2,360 | **1,071** [0,964 ; 1,178] | 0,755 | **0,880** [0,864 ; 0,898] | 0,984 | oui | non |
| composite | profil croise | 0,6 | 2,207 | 0,988 [0,900 ; 1,074] | 0,760 | 0,891 [0,873 ; 0,910] | 0,991 | oui | non |
| enquete | ideologie | 0,6 | 2,673 | 0,966 [0,883 ; 1,064] | 0,704 | 0,870 [0,854 ; 0,887] | 0,964 | oui | non |
| enquete | profil croise | 0,6 | 2,359 | 1,006 [0,929 ; 1,093] | 0,723 | 0,868 [0,850 ; 0,884] | 0,970 | oui | non |
| **entretien (v3)** | ideologie | 0,6 | 3,218 | 1,067 [0,940 ; 1,191] | 0,731 | **0,940** [0,921 ; 0,960] | **1,044** | oui | **non** |
| **entretien (v3)** | profil croise | 0,5 | 3,078 | 0,964 [0,857 ; 1,076] | 0,728 | **0,952** [0,934 ; 0,972] | **1,051** | oui | **non** |
| **`v8`** | ideologie | 0,4 | 7,708 | 1,148 [0,999 ; 1,293] | 0,296 | **0,935** [0,909 ; 0,960] | **1,046** | oui | **non** |
| **`v8`** | profil croise | 0,3 | 6,805 | 1,010 [0,867 ; 1,155] | 0,340 | **0,956** [0,928 ; 0,983] | **1,053** | oui | **non** |

**Reponse : non, il n'atteint pas (1, 1), meme la ou le plafond le permet.** Sur les quatre
couples dont le plafond depasse 1, le lambda qui amene le terme inter sur 1 laisse le terme
intra a 0,935 a 0,956, et l'intervalle exclut 1 dans les quatre cas [MESURE]. C'est
exactement ce que l'arithmetique de la section 3.4 predisait : atteindre l'intra 1 demanderait
d'abaisser l'inter a 0,45 a 0,51, et personne ne peut vouloir des deux a la fois.

Le terme inter, lui, est corrige proprement : l'intervalle contient 1 dans 15 des 16
configurations (4 conditions x 2 axes x 2 variantes), la seule exception etant `v8` x
ideologie en variante naive, a 1,148 [1,015 ; 1,295] [MESURE].

**Critere 2, l'exactitude individuelle.** Le transport ne touchant que 70 items sur 149, son
cout global est environ deux fois moindre que celui du run principal.

| condition | axe | exactitude 149 items, apres | ecart apparie sur 149 | ecart apparie sur les 70 ordinaux |
|---|---|---|---|---|
| composite | ideologie | **0,6785** | -0,0054 [-0,0062 ; -0,0047] | -0,0116 [-0,0133 ; -0,0099] |
| enquete | ideologie | 0,6467 | -0,0042 [-0,0051 ; -0,0034] | -0,0090 [-0,0109 ; -0,0073] |
| entretien (v3) | ideologie | 0,6478 | -0,0088 [-0,0098 ; -0,0078] | -0,0187 [-0,0208 ; -0,0167] |
| `v8` | ideologie | 0,5421 | -0,0170 [-0,0190 ; -0,0152] | -0,0363 [-0,0404 ; -0,0323] |

Variante informee. Aucun intervalle ne contient zero : la baisse reste distinguable, comme
dans a7. **Les agents composite passent a 0,6785 apres transport, contre 0,6717 pour la
baseline B2** de a2, soit 0,7 point au dessus au lieu de 0,3 point dans a7 [MESURE]. Les
agents entretien et enquete restent sous B2, comme avant le transport.

**Critere 3, A6.** Il echoue exactement comme dans a7.

| condition | axe | variante | bascules | reparations | casses | net | taux de reparation |
|---|---|---|---|---|---|---|---|
| composite | ideologie | naive | 4 101 | 731 | 2 322 | **-1 591** | 0,178 |
| composite | ideologie | **informee** | 4 101 | 1 050 | 1 902 | **-852** | **0,256** |
| enquete | ideologie | naive | 5 248 | 1 033 | 2 747 | -1 714 | 0,197 |
| enquete | ideologie | **informee** | 5 248 | 1 512 | 2 177 | **-665** | **0,288** |
| entretien (v3) | ideologie | naive | 6 040 | 1 151 | 3 252 | -2 101 | 0,191 |
| entretien (v3) | ideologie | **informee** | 6 040 | 1 431 | 2 806 | **-1 375** | 0,237 |
| `v8` | ideologie | naive | 16 546 | 4 263 | 7 190 | -2 927 | 0,258 |
| `v8` | ideologie | **informee** | 16 546 | 4 397 | 7 069 | **-2 672** | 0,266 |

Verite vague 1. **Le net est negatif dans les 32 lignes du fichier** (4 conditions x 2 axes x
2 variantes x 2 vagues de verite), sans exception [MESURE, `a20-m3-critere-a6.csv`]. La
correlation de Spearman entre distances humaines et distances simulees, calculee sur les 70
items ordinaux et les 552 826 paires, **baisse dans les 16 cas** :

| condition | avant | naive | informee |
|---|---|---|---|
| agents composite | 0,5312 | 0,4806 | **0,4861** |
| agents enquete | 0,5794 | 0,5315 | **0,5472** |
| agents entretien (v3) | 0,4369 | 0,3697 | **0,3724** |
| agents demographiques (v8) | 0,3020 | 0,1994 | **0,1685** |

**Le critere A6 n'est pas satisfait sous M3 non plus.** Changer de mesure et restreindre aux
items ordinaux ne renverse rien : le correctif casse toujours plus qu'il ne repare, et la
structure des distances entre personnes se degrade toujours. La conclusion de a7 section 5
tient telle quelle.

---

## 5. Ce qui ne change pas

**L'invariance de la marge.** Le ratio de dispersion totale est constant sur tout le balayage
de lambda, a la troisieme decimale : 0,8933 a lambda 1 et 0,8926 a lambda 0 pour les agents
composite en entropie, 0,9087 et 0,9084 en Gini Simpson [MESURE, `a20-trajectoires.csv`]. La
propriete revendiquee par a7 section 2.1 est confirmee, et a17 section 3.7 avait raison de la
declarer exacte pour les trois mesures.

**La cecite des metriques du champ.** Pour les agents composite, la diversite conservee passe
de 0,8932 a 0,8929 et l'accord par paires de 0,5390 a 0,5391 [MESURE], pendant que le ratio
inter passe de 2,15 a 1,05. L'argument methodologique de a7 section 4 est intact.

**Le temoin de dilatation pure.** Il fabrique toujours de la dispersion au lieu d'en deplacer :
pour les agents composite en Gini Simpson corrigee, le total passe de 0,909 a **1,036**, le
ratio intra atteint 1,020 et le ratio inter reste a **1,329** [MESURE,
`a20-dilatation-temoin.csv`]. Le cout en exactitude est de -0,0307 contre -0,0090 pour le
transport, et le net de reparation de -4 805, contre -1 406 pour le transport publie par a7
au meme lambda. La conclusion de a7 section 6 sur
ce que les metriques de LifeMem ne permettent pas de distinguer est inchangee.

**L'effet sur les axes non cibles.** Corriger sur le profil croise ecrase les axes marginaux :
pour les agents enquete, le ratio inter du genre tombe de 1,048 a 0,399 et celui de la race de
1,358 a 0,479 ; pour `v8`, le genre tombe de 0,981 a -0,025 [MESURE, `a20-par-axe.csv`,
mesure Gini Simpson corrigee]. La conclusion de a7 section 7 est inchangee, et les valeurs
sont un peu plus severes qu'avec l'estimateur brut.

**La convention d'imputation du residu ne change presque rien.** Ce rapport transfere le
residu du terme inter vers le terme intra pour que le total reste invariant, la ou a1 le
retranche du seul terme inter. L'ecart sur le ratio intra publie va de -0,11 a +0,38 pour
cent sur les 40 couples [MESURE, `a20-convention-residu.csv`].

**Effet de la seule soustraction du residu, sans transport** (objection 3.4 de a17, mesuree
ici sur les deux axes du transport). Sur l'ideologie, le ratio inter des agents composite en
entropie passe de 2,1295 sans soustraction a 2,1309 avec, soit +0,07 pour cent. Sur le profil
croise, il passe de 1,89 (valeur publiee par a7) a **1,953**, soit +3,3 pour cent [MESURE].
L'effet est donc negligeable sur l'ideologie et reel sur le profil croise, la ou le residu de
permutation humain vaut 6,6 pour cent contre 1,0 pour cent [MESURE].

---

## 6. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise.** Un estimateur d'information mutuelle, ou de tout terme inter a biais corrige, ne
peut pas etre applique tel quel a une population dont les effectifs conditionnels ont ete
fixes par un operateur deterministe : sur le GSS, l'estimateur de Miller Madow rend -0,136 en
unites de ratio la ou la verite est zero, l'estimateur sans biais de Gini Simpson rend -0,104
et la composante de variance ordinale -0,058, contre une incertitude bootstrap de 0,011 a
0,019 [MESURE]. La correction qui marche est une nulle de permutation **appariee a la
structure de l'operateur**, permutation puis transport au meme reglage ; elle se raccorde
exactement au residu de permutation classique quand le reglage est neutre [MESURE].

**Autorise, et c'est la reecriture demandee par a17.** Sous M1 et M2, sur les 149 items comme
sur les 70 items ordinaux, le plafond du ratio intra a terme inter nul est en dessous de 1
pour les huit couples condition x axe, entre 0,841 et 0,961 ; sous M3 sur les 70 items
ordinaux, il est au dessus de 1 pour quatre couples sur huit, entre 1,044 et 1,053 [MESURE].

**Autorise, et c'est le point que a17 a manque.** Atteindre (1, 1) par un operateur a somme
constante reste impossible sous les trois mesures et pour les quatre conditions, parce que
cela exigerait un ratio de dispersion totale egal a 1 et que ce ratio mesure 0,802 a 0,954 sur
les 40 couples [MESURE]. Ou le plafond depasse 1, restaurer la dispersion intra groupe
exigerait d'abaisser le terme inter a 0,45 a 0,51, c'est a dire d'effacer la moitie de l'ecart
entre segments que les humains presentent reellement.

**Autorise.** Apres correction de l'estimateur et recalibration de lambda, l'intervalle a
95 pour cent du terme inter apres transport contient 1 pour trois des quatre conditions, sous
Gini Simpson comme sous l'entropie ; la quatrieme, les agents enquete, est a 0,908
[0,821 ; 0,995] [MESURE]. Le cout en exactitude individuelle est de 0,90 a 3,43 points sur les
149 items, et de 0,42 a 1,70 point quand le transport est restreint aux 70 items ordinaux
[MESURE].

**Interdit.** Ecrire que la correction de l'estimateur sauve le prototype : elle ne change ni
le critere 2 ni le critere A6, qui echouent tous les deux exactement comme dans a7 [MESURE].
Ecrire que le transport pur suffit sous la variance ordinale : il amene le terme intra a
0,935 a 0,956, jamais a 1, et l'intervalle exclut 1 dans les quatre couples ou le plafond le
permettait [MESURE]. Ecrire "w vaut 4,6 pour cent" sans nommer la mesure : il vaut 0,089 en
variance ordinale [MESURE]. Ecrire que a lambda 0 tout ecart entre segments est supprime :
c'est vrai sur l'ideologie, faux sur le profil croise ou 27,8 pour cent des cellules ne sont
pas transportees [MESURE]. Ecrire que la calibration de a7 sous appliquait systematiquement le
transport : le lambda calibre bouge d'au plus un cran et dans les deux sens [MESURE].
Reprendre le plafond de 0,943 publie par a7 : le plafond a inter nul vaut 0,9364 [MESURE].

---

## 7. Ce que je n'ai pas pu verifier

1. **Si la nulle B est la bonne nulle, ou seulement une nulle qui donne le resultat
   attendu.** A lambda 0 son annulation du terme inter est vraie par construction, donc ce
   point n'est pas un test. Ce qui plaide pour elle est son raccord exact avec a1 a lambda 1
   et sa monotonie entre les deux. Ce qui manque est un jeu de donnees synthetique ou la
   vraie information mutuelle apres transport serait connue analytiquement, ce qui
   trancherait. Non fait [HYPOTHESE].
2. **Si le seuil de 20 personnes par cellule explique tout l'ecart du profil croise.** La
   couverture de 72,2 pour cent des cellules est mesuree, mais je n'ai pas balaye le seuil.
   Un seuil a 10 ou a 30 dirait si le terme inter residuel a lambda 0 varie comme la
   couverture. Meme manque que a7 point 6.
3. **L'agregat des six axes de a1, avec l'estimateur corrige.** a17 objection 3.4 demande de
   decomposer l'ecart 1,753 contre 1,806 entre le changement de jeu d'items et le changement
   d'estimateur. Ce rapport ne mesure que les deux axes de transport, et publie l'effet de
   l'estimateur sur ces deux la (+0,07 pour cent et +3,3 pour cent). L'agregat des six axes
   demanderait de rejouer a1, ce qui n'a pas ete fait.
4. **Si la conclusion tient sur un autre jeu de donnees.** Tout ce rapport porte sur le GSS et
   sur un seul pipeline. L'impossibilite d'atteindre (1, 1) est arithmetique et vaut partout,
   mais les valeurs de `T`, 0,802 a 0,954, sont specifiques. Sur Twin-2K-500, `T` pourrait
   etre plus proche de 1. Test identique a celui deja propose par a7 point 2 [HYPOTHESE].
5. **La sensibilite a la graine des cinq blocs de calibration**, que a17 section 3.8 signale
   comme non declaree. Elle reste non testee ici.
6. **La grille de lambda au dixieme.** Les agents enquete se retrouvent a 0,908 parce
   qu'aucun point de la grille ne les place sur 1 : entre 0,6 et 0,7 le ratio corrige passe
   de 0,908 a 1,231. Une grille au centieme reglerait ce cas particulier, au prix d'un risque
   de sur ajustement a la calibration. Non teste.
7. **La correction pour tests multiples**, absente ici comme dans a7, sur 32 lignes de critere
   A6 et 40 couples de plafond.

---

## 8. Questions ouvertes pour Simon

1. **Faut il publier les deux affirmations separement ?** Le tableau de la section 3 permet
   d'ecrire, en une phrase et sans arithmetique, que le point (1, 1) est hors d'atteinte pour
   tout operateur a somme constante quel que soit l'indice de dispersion, et que le plafond
   du seul terme intra depend, lui, de l'indice. Cette separation rend l'argument plus fort ou
   plus fragile devant un relecteur ?
2. **Le fait que `T` soit proche de 1 sous la variance ordinale et loin de 1 sous les mesures
   nominales, pour les agents entretien et `v8` seulement, est il un resultat en soi ?** Il
   dit que ces deux conditions etalent correctement sur l'echelle mais emploient un repertoire
   de modalites trop pauvre, ce qui oriente vers un probleme de decodage et non de
   conditionnement. Est ce assez pour une section, ou faut il d'abord mesurer directement le
   repertoire de modalites par item ?
3. **La nulle appariee a la structure est elle une contribution methodologique publiable
   separement ?** Le probleme, "un estimateur a biais corrige applique a des donnees dont les
   effectifs conditionnels ont ete fixes par un post traitement", va se poser a tout correctif
   qui manipule des distributions conditionnelles, donc a une bonne partie de la litterature
   qui vient. Personne ne semble l'avoir ecrit.
4. **Faut il abandonner le profil croise comme axe de transport ?** L'operateur n'y couvre que
   72,2 pour cent des cellules, la nulle ne s'y annule pas, et corriger dessus ecrase les axes
   marginaux jusqu'a -0,03 sur le genre. Le garder oblige a publier trois mises en garde ; le
   retirer prive le rapport de l'axe qui approche le mieux l'invite d'un agent demographique.
5. **Le critere A6 ayant echoue une deuxieme fois, sous une autre mesure et sur un autre jeu
   d'items, doit on arreter la piste du transport ?** Deux echecs pour des raisons
   independantes, l'un arithmetique et l'autre empirique, ne se rattrapent pas par un reglage.
   La question de a7 devient : combien de tentatives avant de declarer la famille A close et
   de basculer sur la famille B de `exploration/09` ?

---

## 9. Fichiers produits

| fichier | contenu |
|---|---|
| `analyses/a20_transport_variance_v2.py` | le script rejouable, une commande, aucun appel de modele ; importe a7 sans le modifier |
| `a20-figure-transport-v2.png` et `.svg` | l'objection 4 en barres, les trajectoires corrigees sous M2 et sous M3, et les plafonds |
| `a20-lambda0-controle.csv` | verification (c) : terme inter a lambda 0, brut, nulle A, nulle B, demi largeur bootstrap |
| `a20-trajectoires.csv` | balayage de lambda, ratios brut et corriges par les deux nulles, trois mesures, deux jeux d'items |
| `a20-plafond.csv` | objection 5 : `w`, `T`, plafond a inter nul et intra mesure a lambda 0, 3 mesures x 2 jeux x 4 conditions x 2 axes |
| `a20-couverture-cellules.csv` | part des cellules (item, segment) reellement transportees, par axe |
| `a20-lambda-calibre.csv` | lambda retenu par bloc, pour les trois mesures de calibration |
| `a20-avant-apres.csv` | avant / apres au lambda calibre, intervalles bootstrap, exactitude appariee |
| `a20-m3-ordinal.csv` | le transport rejoue sous M3 sur les 70 items ordinaux, criteres 1 et 2 |
| `a20-m3-critere-a6.csv` | critere A6 du run M3, reparations, casses, Spearman, deux vagues de verite |
| `a20-par-axe.csv` | effet sur les six axes, mesure Gini Simpson corrigee |
| `a20-dilatation-temoin.csv` | le temoin a un seul bouton, avec estimateur corrige |
| `a20-convention-residu.csv` | ce que change le transfert du residu vers le terme intra |

Rappel : `.gitignore` exclut `*.csv`. Les chiffres qui comptent sont recopies dans le present
rapport, qui l'est. Aucune microdonnee n'a quitte `data/`.
