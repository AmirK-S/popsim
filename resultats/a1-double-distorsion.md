# a1. La double distorsion des populations simulees

## Errata du 8 septembre 2026

Corrections apportees a la suite de la relecture adverse `a17-relecture-adverse.md`. Le corps
du rapport n'est pas reecrit, il reste lisible tel qu'il a ete rendu le 3 septembre. Chaque
point cite la phrase d'origine, donne la correction et la preuve. Recalculs :
`analyses/a19_denominateurs.py` et `analyses/a19_exactitude_brute.py`, tableaux
`resultats/a19-exactitude-appariee.csv`, `a19-exactitude-brute.csv`,
`a19-test-retest-par-jeu.csv`, `a19-ratios-par-jeu-items.csv`,
`a19-recopie-items-ecartes.csv`. Aucun appel de modele.

### E1. Section 7.3 et reponse en une ligne : l'exactitude et les ratios n'etaient pas calcules sur le meme jeu d'items. Objection a17 1.1, contradiction C4.

**Phrase d'origine, reponse en une ligne.** "Deux conditions du meme papier, dont l'exactitude
est strictement indistinguable, 56,21 contre 56,28 pour cent, ecart apparie -0,07 point avec
un intervalle [-0,52 ; +0,37], ont des gonflements d'ecarts inter groupes qui different d'un
facteur 13,5."

**Phrase d'origine, section 7.3.** "`gss_v7`, la condition persona, et `gss_v8`, une condition
demographique, ont une exactitude strictement indistinguable : 56,21 contre 56,28 pour cent,
ecart apparie -0,07 point, intervalle [-0,52 ; +0,37], t = -0,32."

**Correction.** Les exactitudes 56,21 et 56,28 sont lues dans le fichier des auteurs, qui les
calcule sur **150 items**. Les ratios 0,437 et 5,907 sont calcules par a1 sur **169 items**.
Les deux chiffres ne portent pas sur le meme denominateur et la phrase les met cote a cote.
Sur les 169 items du rapport, les deux conditions **ne sont pas indistinguables** : v7 obtient
57,03 pour cent, v8 obtient 56,20 pour cent, ecart apparie **-0,83 point**, intervalle
bootstrap sur les personnes [-1,28 ; -0,38], t = -3,82. C'est la condition persona qui est la
plus exacte, et l'intervalle exclut zero. [MESURE]

**Preuve du denominateur.** La consistance test retest publiee par les auteurs, 79,5253, se
reproduit exactement sur les 150 items de leur liste d'exclusion, et sur aucun autre jeu :
177 items 81,2491 ; 169 items 81,0072 ; **150 items 79,5253** ; 149 items 79,5002.
[MESURE, `a19-test-retest-par-jeu.csv`]

**Le tableau complet, exactitude appariee v8 moins v7, meme jeu d'items des deux cotes.**

| jeu d'items | v7 | v8 | v8 moins v7, apparie | IC 95 % | t |
|---|---|---|---|---|---|
| 177 items | 56,76 | 56,90 | +0,15 | [-0,29 ; +0,58] | +0,69 |
| **169 items, ceux de a1** | **57,03** | **56,20** | **-0,83** | **[-1,28 ; -0,38]** | **-3,82** |
| 150 items, ceux des auteurs | 56,17 | 56,19 | +0,02 | [-0,44 ; +0,48] | +0,07 |
| 149 items, ceux de a2, a7, a8 et a12 | 56,40 | 55,92 | -0,48 | [-0,95 ; -0,01] | -2,11 |

**Le premier constat de la section 7.3 est atteint de la meme facon.** "Les deux conditions
demographiques different de 1,85 point d'exactitude, ecart apparie sur les 1052 participants,
intervalle [1,41 ; 2,29]" est un chiffre a 150 items. Sur les 169 items du rapport, v6 obtient
60,37 et v8 56,20, ecart **-4,17 point** [-4,57 ; -3,74], t = -19,63. [MESURE]

**Les ratios, eux, ne bougent pas et le facteur 13,5 tient.** Recalcules sur les deux jeux
avec la meme machinerie que a1, mesure entropie :

| condition | ratio inter, 169 items | ratio inter, 149 items |
|---|---|---|
| agents persona `v7` | 0,437 [0,379 ; 0,493] | 0,397 [0,340 ; 0,454] |
| agents demographiques `v8` | 5,907 [5,648 ; 6,157] | 5,972 [5,704 ; 6,244] |
| rapport v8 sur v7 | **13,5** | **15,0** |

Les estimations ponctuelles a 169 items reproduisent **a l'identique** celles du tableau de la
section 3, 0,437 et 5,907, ce qui verifie que le recalcul emploie bien le meme estimateur. Les
intervalles sont un peu plus etroits que ceux du 3 septembre parce que le tirage bootstrap
n'est pas le meme ; les conclusions de disjonction ne changent pas.
[MESURE, `a19-ratios-par-jeu-items.csv`]

**Formulation qui remplace le resultat phare, a employer partout.** *Deux conditions du meme
papier, sur les memes 1 052 participants et les memes 169 items, dont l'exactitude ne differe
que de 0,8 point, ont des gonflements d'ecarts inter groupes qui different d'un facteur 13,5,
avec des intervalles disjoints.* Le mot "indistinguable" est retire ; l'argument perd la forme
du non rejet et garde son ordre de grandeur, un point d'exactitude contre un facteur treize.

**Reserve de forme.** a17 annonce, pour ce meme tableau, 55,93 et 55,49 sur 177 items et 56,16
et 55,28 sur 169 items. Ces deux lignes ne sont pas reproduites ici. Les lignes 150 items et
149 items de a17 le sont a l'identique, et les quatre consistances test retest de a17 aussi,
ce qui etablit que les jeux d'items sont les memes des deux cotes. La verification arithmetique
tranche en faveur des valeurs ci dessus : 57,03 pour cent pour v7 sur 169 items se reconstitue
exactement a partir de la valeur a 150 items et des taux item par item du tableau E4, et 56,20
pour cent pour v8 de meme. Le calcul a ete fait deux fois, sur les codes apparies a la
nomenclature et sur les chaines brutes, avec le meme resultat a deux centiemes pres.
[MESURE, `a19-exactitude-brute.csv`]

### E2. Section 3 : le controle de la vague 2 n'inclut pas 1 sur deux mesures sur trois. Objection a17 1.2.

**Phrase d'origine.** "Le controle passe. La vague 2 tombe en (1,003 ; 1,004), les deux
intervalles contiennent 1. La methode ne fabrique pas d'ecart la ou il n'y en a pas."

**Correction.** Le terme inter contient 1 sur les trois mesures. Le terme **intra** ne le
contient pas sur la mesure principale ni sur la mesure de controle ordinale, comme le montre le
fichier produit par le script lui meme, `a1-ratios.csv` :

| mesure | ratio intra vague 2 | IC 95 % | contient 1 ? | distance a 1 de la borne la plus proche |
|---|---|---|---|---|
| entropie, mesure principale | 1,0043 | [**1,0001** ; 1,0087] | **non** | 0,01 pour cent |
| Gini Simpson | 1,0030 | [0,9992 ; 1,0069] | oui | sans objet |
| variance ordinale | 0,9894 | [0,9795 ; **0,9997**] | **non** | 0,03 pour cent |

**Phrase de remplacement.** "Le controle tombe a 0,4 pour cent de (1,1) sur les trois mesures.
Sur le terme intra, l'intervalle exclut 1 de justesse pour deux mesures sur trois, de 0,01 et
0,03 pour cent. Ce qu'il faut en conclure n'est pas que la methode echoue, mais qu'elle a une
resolution finie : elle ne peut pas certifier l'absence de distorsion en dessous d'environ un
demi pour cent."

**Ce que cela implique pour la methode.** L'ecart de 0,4 pour cent est un biais residuel de
l'estimateur intra, pas un effet de la reinterrogation : les memes personnes repondent deux
fois, la dispersion vraie a l'interieur des segments est la meme aux deux vagues. L'ordre de
grandeur, un demi pour cent, est **cent fois plus petit** que les effets publies, qui vont de
-11 a -36 pour cent sur le terme intra et de +75 a +490 pour cent sur le terme inter. Le
critere binaire "l'intervalle contient 1" doit cesser d'etre employe comme certificat de
validite, y compris a la limite 4 du meme rapport, ou il sert a justifier l'exclusion des huit
items demographiques. Voir E5.

**Corollaire sur l'inclusion de 1 comme critere.** La limite 4 ecrit : "En les gardant, le
controle vague 2 tombe a 0,946 avec un intervalle [0,927 ; 0,970] qui exclut 1 : la methode
devient biaisee." Ce motif reste valable, mais parce que l'ecart est de 5,4 pour cent, soit
plus de dix fois la resolution mesuree ci dessus, et non parce que l'intervalle exclut 1.

### E3. Section 8 limite 3 : le nom de l'intervalle bootstrap est faux. Objection a17 1.6.

**Phrase d'origine.** "Les distributions bootstrap sont donc recentrees de facon additive sur
l'estimation ponctuelle avant formation du ratio, ce qui est le bootstrap de base au sens de
Davison et Hinkley."

**Correction.** La fonction `recentrer` de `a1_double_distorsion.py` calcule
`v - moyenne(v) + cible`, ce qui produit l'intervalle
`[theta + q2,5 - moyenne ; theta + q97,5 - moyenne]` : une **translation** de la distribution
bootstrap. Le bootstrap de base de Davison et Hinkley est `[2 theta - q97,5 ; 2 theta - q2,5]`,
qui **reflechit** la distribution autour de l'estimation ponctuelle. Les deux coincident
lorsque la distribution est symetrique, et divergent sinon, en inversant le sens de
l'asymetrie. Le nom correct de ce qui est publie est **intervalle de percentile translate sur
l'estimation ponctuelle**. La citation de Davison et Hinkley est retiree. [CONFIRME par lecture
du code, fonction `recentrer`]

Ce changement de nom ne change aucun chiffre publie : la translation est exactement ce qui a
ete calcule, seule son etiquette etait fausse.

**Point voisin, objection a17 1.7, non corrige mais a porter.** La meme limite 3 rapporte que
la moyenne bootstrap brute du terme inter depasse la valeur observee de 24 pour cent chez les
humains et de 2 pour cent chez `v8`. C'est une estimation bootstrap du **biais** de
l'estimateur, dependante de la condition, portant sur la quantite qui sert de denominateur a
tous les ratios inter. Une correction de biais bootstrap augmenterait les ratios inter au lieu
de les reduire ; le choix publie est donc la borne basse, et il doit etre presente comme un
choix chiffre et conservateur, non comme un detail de recentrage. [PROBABLE, la colonne
"ratio avec correction de biais" n'a pas ete calculee.]

### E4. Section 7.4 : ce qui differe entre `v6` et `v8` est etabli, sans le code de generation. Objection a17 1.3, contradiction C1. RESULTAT NOUVEAU.

**Phrase d'origine.** "Non etabli non plus. Ce qui differe concretement entre les deux
generations. Le paquet ne contient pas le code de generation."

**Correction : c'est desormais etabli, par la mesure.** Le taux d'accord de chaque condition
avec la vague 1, item par item, sur les 29 items que le dossier ecarte, dit ce que chaque
agent avait dans son invite. Un taux voisin de 1 est une recopie, un taux inferieur a la
modalite majoritaire est l'absence de l'information. [MESURE,
`analyses/a19_denominateurs.py`, tableau complet dans `resultats/a19-recopie-items-ecartes.csv`]

| item | modalite majoritaire | `v6` | `v8` | `v7` | composite | enquete | entretien | retest humain |
|---|---|---|---|---|---|---|---|---|
| `polviews` | 0,288 | **0,200** | **0,961** | 0,217 | 0,539 | 0,349 | 0,554 | 0,833 |
| `partyid` | 0,220 | **0,165** | **0,994** | 0,183 | 0,756 | 0,291 | 0,741 | 0,820 |
| `marital` | 0,420 | **0,999** | 0,461 | 0,600 | 0,974 | 0,912 | 0,968 | 0,953 |
| `relig*` | 0,405 | **0,994** | 0,430 | 0,442 | 0,791 | 0,560 | 0,758 | 0,887 |
| `degree*` | 0,389 | **0,998** | 0,267 | 0,419 | 0,894 | 0,449 | 0,892 | 0,913 |
| `educ*` | 0,943 | 0,998 | 0,939 | 0,934 | 0,941 | 0,939 | 0,941 | 0,956 |
| `income` | 0,516 | **0,994** | 0,454 | 0,412 | 0,422 | 0,312 | 0,415 | 0,634 |
| `zodiac` | 0,092 | **0,999** | 0,062 | 0,081 | 0,883 | 0,063 | 0,895 | 0,975 |
| `sex*` | 0,564 | **0,999** | **0,998** | 0,832 | 0,988 | 0,561 | 0,985 | 0,988 |
| `race*` | 0,759 | **0,998** | **0,999** | 0,804 | 0,933 | 0,686 | 0,926 | 0,979 |
| `reg16` | 0,187 | 0,144 | 0,129 | 0,277 | 0,666 | 0,146 | 0,667 | 0,785 |
| `hispanic` | 0,865 | **0,999** | 0,863 | 0,894 | 0,981 | 0,865 | 0,980 | 0,974 |
| `widowed` | 0,931 | **1,000** | 0,837 | 0,914 | 0,981 | 0,931 | 0,980 | 0,985 |
| `martype*` | 0,496 | **0,990** | 0,606 | 0,662 | 0,846 | 0,840 | 0,839 | 0,873 |
| `speduc*` | 0,506 | 0,845 | 0,547 | 0,649 | 0,868 | 0,869 | 0,841 | 0,863 |

Les quatorze autres items ecartes, tous sans recopie par `v6` ni par `v8`, sont dans
`resultats/a19-recopie-items-ecartes.csv` : `born`, `dwelown`, `famdif16`, `madeg*`,
`maeduc*`, `mawrkgrw`, `padeg*`, `paeduc*`, `relpersn`, `rvisitor`, `sprtprsn`, `spwrksta`,
`vetyears`, `visitors`. Les colonnes `composite` et `entretien` y sont a 0,68 a 0,99 sur
presque tous les items : c'est attendu, ces deux conditions ont recu l'entretien complet ou
l'enquete complete, elles ne recopient pas un attribut, elles savent la reponse.

**Lecture.** `gss_v8` a recu **l'ideologie, le parti, la race et le genre, et rien d'autre** :
il les recopie a 96 a 99,9 pour cent et il est au niveau du hasard sur tout le reste, y compris
le zodiaque, 6,2 pour cent contre une modalite majoritaire a 9,2 pour cent. C'est exactement
l'invite demographique decrite par le papier et citee par a14 section 3.1. `gss_v6` a recu un
**profil d'etat civil riche et aucune information politique** : statut marital 99,9 pour cent,
religion 99,4, diplome 99,8, revenu 99,4, date de naissance a 99,9 par le zodiaque, origine
hispanique 99,9, race et genre a 99,8 ; et 20,0 pour cent sur `polviews` et 16,5 pour cent sur
`partyid`, c'est a dire **sous la modalite majoritaire** de ces deux items, 28,8 et 22,0.

**Ce que cela explique, et c'est le resultat nouveau.** La difference entre les deux
generations demographiques est identifiee : c'est la presence ou l'absence de l'etiquette
ideologique et du parti dans l'invite. Elle se lit directement dans le detail par axe de la
section 4, `a1-ratios-par-axe.csv`, mesure entropie, ratio inter sur l'axe ideologie :

| condition | ratio inter, axe ideologie | ideologie et parti dans l'invite |
|---|---|---|
| agents demographiques `v6` | **0,34** | non, mesure |
| agents demographiques `v8` | **8,51** | oui, mesure |
| agents persona `v7` | 0,27 | non |
| humains vague 2, controle | 1,01 | sans objet |

**Phrase citable.** *Ajouter l'etiquette ideologique a l'invite d'un agent demographique
multiplie par vingt cinq le gonflement des ecarts entre segments ideologiques, de 0,34 a 8,51
en ratio a la reference humaine, sans que l'exactitude individuelle change de plus d'un point.*

**Consequence pour la section 7.5.** La formulation "une dimension entiere que leur mesure ne
voit pas" cede la place a : "deux conditions dont l'invite differe sur un seul attribut,
l'etiquette politique, sont notees equivalentes a un point pres par l'exactitude et opposees
par la structure". L'argument de fond survit, parce que l'exactitude ne voit toujours pas cette
difference, mais la cause n'est plus mysterieuse, elle est nommee. Il faut l'ecrire avant qu'un
relecteur n'ecrive "votre mesure detecte le contenu de l'invite, pas une pathologie cachee" :
la reponse est que le contenu de l'invite est precisement ce que l'exactitude ne detecte pas.

**Consequence sur la mention `LA`.** Le sigle reste inexplique, mais la question qu'il posait
est resolue : `v8` est l'ablation demographique du papier, `v6` est une ablation a profil
d'etat civil sans politique. a16 section 2.3 declare la recherche du sigle close ; elle peut
l'etre sans dommage.

### E5. Section 1 et limite 4 : le motif d'exclusion des huit items est faux pour la moitie d'entre eux. Objection a17 1.4.

**Phrase d'origine, section 1.** "Huit sont ecartes parce qu'ils redisent litteralement un
attribut de segmentation : `sex*`, `race*`, `educ*`, `degree*`, `income`, `polviews`,
`partyid`, `reg16`. Un agent demographique a recu ces valeurs dans son invite ; il ne les
predit pas, il les recopie."

**Correction.** Le tableau E4 montre qu'**aucun agent demographique n'a recu les huit**. Ni
`v6` ni `v8` ne recopient `educ*` : leurs taux, 99,8 et 93,9 pour cent, sont a comparer a une
modalite majoritaire de 94,3 pour cent, donc `v8` est au niveau du hasard et seul `v6` recopie.
`v8` n'a recu ni `income`, 45,4 contre 51,6 de modalite majoritaire, ni `degree*`, 26,7 contre
38,9, ni `reg16`, 12,9 contre 18,7. `v6` n'a recu ni `polviews` ni `partyid`.

**Motif de remplacement, qui est le seul defendable.** "Ces huit items sont ecartes parce que
les garder fait echouer le controle de la vague 2, qui tombe a 0,946 avec un intervalle
[0,927 ; 0,970], soit dix fois la resolution de la methode etablie en E2. Chacun est recopie
par au moins une condition d'agent, mais aucune condition ne les recopie tous : la recopie est
condition dependante et c'est precisement ce qui rend l'exclusion necessaire." Le motif
empirique de la limite 4 devient le motif principal, le motif d'invite devient une illustration.

### E6. Section 3 : les trois mesures ne donnent pas exactement le meme classement. Objection a17 1.5, contradiction C11.

**Phrase d'origine.** "Les deux autres mesures donnent le meme classement et le meme signe pour
les huit conditions. La conclusion ne depend pas du choix de la mesure."

**Correction.** Le signe est bien identique sur les trois mesures pour les huit conditions.
Le classement, lui, s'inverse pour les deux meilleures conditions sur le terme intra. Dans
`a1-ratios.csv` :

| condition | intra entropie | intra Gini Simpson | intra variance ordinale |
|---|---|---|---|
| agents composite | 0,885 | 0,896 | 0,861 |
| agents entretien (v3) | 0,852 | 0,850 | **0,890** |

Sur les deux mesures nominales, les agents composite conservent plus de dispersion interne que
les agents entretien ; sur la variance ordinale, c'est l'inverse. **Phrase de remplacement** :
"le signe des huit conditions est identique sur les trois mesures ; le classement des deux
conditions les plus proches s'inverse sur la variance ordinale."

**Point lie, section 9.** "Ce fait est invisible aux mesures globales de dispersion, qui restent
entre 0,80 et 0,90." La fourchette est celle de l'entropie. Sur la variance ordinale, la colonne
`ratio_dispersion_globale` de `a1-ratios.csv` vaut 0,9623 pour les agents entretien et 0,9508
pour `v8`, hors de la fourchette annoncee. La fourchette doit etre donnee mesure par mesure.

### E7. Section 5 : la coincidence du -0,020 n'est pas une validation. Objection a17 1.8.

**Phrase d'origine.** "Sur le GSS, la valeur humaine est retrouvee au centieme pres, -0,020 sur
l'ideologie, ce qui indique que la mesure est bien implementee."

**Correction.** Le -0,02 de la litterature porte sur le World Values Survey, sur des tertiles de
statut socio economique, avec une distance euclidienne sur un codage ordinal standardise, comme
l'etablissent a10 et a13 section 1.1. La mesure de a1 porte sur le GSS, sur des segments
d'ideologie, avec une distance d'appariement simple. Deux quantites differentes qui tombent sur
la meme valeur ne se valident pas l'une l'autre ; c'est exactement la faute que la section 4 de
PASSATION.md interdit et que le dossier releve deja trois fois ailleurs. **Phrase de
remplacement** : "la valeur humaine mesuree ici, -0,020, n'est pas comparable au -0,02 publie,
qui porte sur un autre jeu de donnees, une autre distance et une autre segmentation ; la
coincidence numerique ne vaut pas validation." Le reste de la section 5, y compris le constat
que 0,19 n'est pas retrouve, n'est pas affecte.

### E8. Ce que ces errata ne changent pas

Les huit conditions gardent leurs ratios, les figures et les fichiers CSV du 3 septembre sont
inchanges et ont ete reproduits a l'identique par `a19_denominateurs.py` sur les 169 items
(0,437 et 5,907 pour `v7` et `v8`, mesure entropie). La double distorsion, son absence chez
`v7` et `v6`, la compensation partielle dans une mesure globale, le plafond humain et le detail
par axe ne sont pas touches par cette relecture.

---

**Reponse en une ligne.** La double distorsion apparait, mais pas partout : sur quatre des
six conditions d'agents du paquet OSF t6g7k, les ecarts entre segments demographiques sont
gonfles d'un facteur 1,8 a 5,9 pendant que la dispersion a l'interieur des segments est
ecrasee a 0,68 - 0,89, et une mesure globale de dispersion ne voit qu'un ecart de 8 a 20
pour cent. Sur les deux autres, agents persona et une des deux variantes d'agent
demographique, les deux termes sont ecrases ensemble : ce n'est pas une double distorsion,
c'est un aplatissement simple.

**Le resultat le plus fort n'etait pas celui qui etait cherche.** Deux conditions du meme
papier, dont l'exactitude est strictement indistinguable, 56,21 contre 56,28 pour cent,
ecart apparie -0,07 point avec un intervalle [-0,52 ; +0,37], ont des gonflements d'ecarts
inter groupes qui different d'un **facteur 13,5**, avec des intervalles qui ne se chevauchent
pas. La metrique employee par le champ est aveugle a une difference de structure majeure.
Section 7.

Date : 3 septembre 2026. Reproduction : `.venv/bin/python analyses/a1_double_distorsion.py`,
environ deux minutes, aucun appel de modele de langage.

---

## 1. Ce qui est mesure, et sur quoi

Source : paquet de replication OSF `t6g7k` du papier arXiv 2411.10109 v3, dossier
`figure2/data/new_analysis_summaries/gss_filtered/preparation/`. Huit fichiers, 1052
participants apparies ligne a ligne, 177 items du General Social Survey en clair.

Les libelles des conditions ne sont pas devines, ils sont lus dans le paquet. Table de
correspondance et sources exactes en section 7. Pour le GSS : `gss_v3` entretien, `gss_v7`
persona, `survey_agents` questionnaire, `composite_agents` questionnaire plus entretien, et
**deux conditions distinctes portant toutes deux l'etiquette demographique**, `gss_v6` et
`gss_v8`.

**Segmentation.** Six partitions demographiques, tirees de
`figure3/data/demographic_summary.csv`, complet pour les 1052 participants. Les trois
premieres, genre, race, ideologie politique, sont exactement celles que le papier emploie
pour sa figure 3, constante `DPD_VARS`. Elles n'ont donc pas ete choisies pour arranger le
resultat. S'y ajoutent l'age, l'education, et un profil croise genre x race x ideologie
ramenee a trois blocs, soit 18 segments, qui approche ce qu'un agent demographique recoit
dans son invite. Revenu, type de quartier et orientation sexuelle sont ecartes : 180 valeurs
vides sur 1052.

**Items.** 169 items sur 177. Huit sont ecartes parce qu'ils redisent litteralement un
attribut de segmentation : `sex*`, `race*`, `educ*`, `degree*`, `income`, `polviews`,
`partyid`, `reg16`. Un agent demographique a recu ces valeurs dans son invite ; il ne les
predit pas, il les recopie. Cette exclusion n'est pas cosmetique, voir la section 8.

**Codage.** Chaque reponse est appariee a la nomenclature officielle de son item,
`question_master/gss/main.csv`, apres retrait de la ponctuation entourante. Ce qui ne tombe
pas dans la nomenclature est compte comme non codable. Taux mesure : **0,00 pour cent chez
les humains des deux vagues**, de 0,04 a 0,33 pour cent chez les agents, qui produisent
parfois une phrase de justification a la place d'une modalite. Ne pas traiter ces reponses
uniques comme des modalites valides : elles gonfleraient artificiellement la diversite des
agents.

---

## 2. Les mesures de dispersion, et pourquoi trois

Les reponses sont categorielles, une partie seulement est ordinale : 79 items sur 177 sont
marques ordinaux par les auteurs eux memes dans `question_master/gss/groups/categorical.csv`.
Aucune mesure de dispersion ne s'impose. Trois sont calculees, choisies pour ne pas partager
les memes hypotheses.

| | decomposition | terme intra | terme inter | hypothese d'ordre |
|---|---|---|---|---|
| **M1 entropie** | H(R) = H(R\|S) + I(R;S) | entropie conditionnelle | information mutuelle | aucune |
| **M2 Gini Simpson** | D = D_intra + D_inter | moyenne ponderee des D de segment | residu, positif par convexite | aucune |
| **M3 variance ordinale** | Var = E[Var(R\|S)] + Var(E[R\|S]) | variance intra | composante de variance inter | oui, intervalles egaux |

M3 est un controle et non une mesure principale : elle suppose des intervalles egaux entre
modalites, ce qui est faux pour la plupart des echelles du GSS. Elle ne porte que sur les 75
items ordinaux retenus.

**Le biais qu'il a fallu traiter, et il change le resultat.** L'estimateur naif de I(R;S) et
de D_inter est positivement biaise : meme quand le segment n'explique rien, un echantillon
fini donne une valeur strictement positive, et ce biais croit avec le nombre de modalites
effectivement employees. Or les agents en emploient moins que les humains. Comparer des
estimateurs naifs aurait donc fabrique mecaniquement un ratio inter inferieur a 1, c'est a
dire l'inverse du resultat cherche. Chaque mesure emploie un estimateur a biais corrige :
correction de Miller Madow pour l'entropie, estimateur sans biais de l'indice de Simpson,
composante de variance au sens de l'analyse de variance pour M3.

**Controle de ces corrections.** On permute au hasard les etiquettes de segment : le terme
inter doit alors tomber a zero. Resultat, dans `a1-controle-permutation.csv` : le residu est
inferieur a 0,1 pour cent pour Gini Simpson et pour la variance ordinale, ce qui valide ces
deux estimateurs. Il subsiste 3 a 15 pour cent pour l'entropie, dont la correction de Miller
Madow n'est qu'un premier ordre ; ce residu est soustrait explicitement.

---

## 3. Les deux ratios

Chaque terme est rapporte a celui des humains de la vague 1, qui valent donc 1 par
construction. Les humains de la vague 2 sont les memes personnes reinterrogees deux semaines
plus tard : ils sont le controle et doivent tomber en (1, 1).

**Mesure principale, entropie et information mutuelle.** Intervalles a 95 pour cent,
bootstrap sur 1000 tirages avec remise des participants, le meme tirage etant applique a
toutes les conditions pour preserver l'appariement.

| condition | ratio inter | ratio intra | produit | ce que voit une mesure globale |
|---|---|---|---|---|
| humains vague 1 | 1 (reference) | 1 (reference) | 1,00 | 1,00 |
| **humains vague 2 (controle)** | **1,003** [0,971 ; 1,037] | **1,004** [1,000 ; 1,009] | 1,01 | 1,00 |
| agents composite | 1,753 [1,679 ; 1,832] | 0,885 [0,880 ; 0,889] | 1,55 | **0,90** |
| agents entretien (v3) | 2,156 [2,039 ; 2,284] | 0,852 [0,846 ; 0,857] | 1,84 | **0,88** |
| agents enquete | 1,824 [1,738 ; 1,913] | 0,822 [0,816 ; 0,827] | 1,50 | **0,84** |
| agents persona (v7) | 0,437 [0,363 ; 0,513] | 0,667 [0,653 ; 0,680] | 0,29 | 0,66 |
| agents demographiques (v6) | 0,855 [0,772 ; 0,943] | 0,637 [0,629 ; 0,645] | 0,55 | 0,64 |
| agents demographiques (v8) | 5,907 [5,495 ; 6,379] | 0,684 [0,676 ; 0,691] | 4,04 | **0,80** |

**Le controle passe.** La vague 2 tombe en (1,003 ; 1,004), les deux intervalles contiennent
1. La methode ne fabrique pas d'ecart la ou il n'y en a pas.

**La derniere colonne est le point du dossier.** Pour les agents composite, une mesure
globale de dispersion, celle qui ne separe pas inter et intra, affiche 0,90 : un ecart de
dix pour cent, qu'un relecteur qualifierait de compression legere. La decomposition montre
au meme moment +75 pour cent entre segments et -11 pour cent a l'interieur. Les deux erreurs
ne se compensent pas exactement, contrairement a la formulation d'hypothese la plus forte,
mais elles se compensent assez pour qu'une metrique agregee ne les voie pas.

**Robustesse au choix de mesure.** Les deux autres mesures donnent le meme classement et le
meme signe pour les huit conditions. Detail complet dans `a1-ratios.csv`.

| condition | inter M1 | inter M2 | inter M3 | intra M1 | intra M2 | intra M3 |
|---|---|---|---|---|---|---|
| humains vague 2 | 1,003 | 1,011 | 1,014 | 1,004 | 1,003 | 0,989 |
| agents composite | 1,753 | 1,792 | 2,055 | 0,885 | 0,896 | 0,861 |
| agents entretien (v3) | 2,156 | 2,212 | 2,746 | 0,852 | 0,850 | 0,890 |
| agents enquete | 1,824 | 1,891 | 2,149 | 0,822 | 0,846 | 0,827 |
| agents persona (v7) | 0,437 | 0,339 | 0,222 | 0,667 | 0,657 | 0,552 |
| agents demographiques (v6) | 0,855 | 0,795 | 0,499 | 0,637 | 0,643 | 0,502 |
| agents demographiques (v8) | 5,907 | 5,928 | 5,916 | 0,684 | 0,710 | 0,749 |

La conclusion ne depend pas du choix de la mesure. C'etait la question posee, la reponse est
non.

**Ce qui n'est pas distinguable.** Agents composite et agents enquete ont des intervalles qui
se chevauchent sur le ratio inter, [1,679 ; 1,832] contre [1,738 ; 1,913] : ils ne sont pas
distinguables sur cette dimension et il ne faut pas les classer. Les agents entretien sont
au dessus des deux, sans chevauchement.

---

## 4. Ou se loge le gonflement : un seul axe le porte

Le detail par axe, `a1-ratios-par-axe.csv`, mesure entropie, ratio inter.

| condition | genre | race | ideologie | age | education | profil croise |
|---|---|---|---|---|---|---|
| humains vague 2 | 0,97 | 1,03 | 1,01 | 0,98 | 1,01 | 1,01 |
| agents composite | 1,26 | 1,48 | **2,09** | 1,17 | 1,35 | 1,89 |
| agents entretien (v3) | 1,36 | 1,61 | **2,72** | 1,19 | 1,27 | 2,44 |
| agents enquete | 0,80 | 1,22 | **2,49** | 0,78 | 1,06 | 2,06 |
| agents persona (v7) | 0,99 | 0,73 | 0,27 | 0,72 | 0,35 | 0,38 |
| agents demographiques (v6) | 1,57 | 2,44 | 0,34 | 0,70 | 2,69 | 0,71 |
| agents demographiques (v8) | 1,09 | 4,01 | **8,51** | 3,50 | 0,37 | 6,64 |

**Le gonflement n'est pas demographique en general, il est politique.** Pour les trois
conditions riches en information sur la personne, composite, entretien et enquete, il est
porte presque entierement par l'ideologie politique, facteur 2,1 a 2,7, tandis que le genre
reste entre 0,80 et 1,36 et l'age entre 0,78 et 1,19, c'est a dire au voisinage de la
fidelite. Le modele n'essentialise pas la demographie en bloc : il essentialise
l'appartenance politique.

Ce resultat n'est ecrit dans aucun des papiers lus. Il a une consequence pratique
immediate : une etude qui mesurerait la distorsion sur le genre ou l'age conclurait a
l'absence de probleme. Confiance : elevee sur le fait, moyenne sur l'interpretation.

Une reserve a porter avec le resultat : l'ideologie politique n'est pas une variable
demographique, c'est une attitude auto declaree. Le papier l'emploie comme telle dans sa
figure 3, et on l'a suivi pour ne pas choisir la segmentation qui arrange, mais l'effet
principal repose dessus.

Le ratio intra est au contraire tres stable d'un axe a l'autre, 0,85 a 0,90 pour les agents
composite quel que soit l'axe. C'est attendu : l'ecrasement interne est une propriete du
generateur, pas de la partition.

---

## 5. Score de silhouette : le chiffre de la litterature n'est pas retrouve

Distance d'appariement simple, soit la proportion des 169 items ou deux participants
different, calculee sur les items ou les deux ont repondu. C'est le coefficient de Gower
reduit au cas purement categoriel, et c'est la seule distance qui ne suppose pas d'unite
commune entre items nominaux et ordinaux.

| condition | genre | race | ideologie | age | education | profil croise |
|---|---|---|---|---|---|---|
| humains vague 1 | 0,010 | 0,006 | **-0,020** | -0,021 | -0,007 | -0,026 |
| humains vague 2 | 0,010 | 0,007 | -0,021 | -0,020 | -0,008 | -0,026 |
| agents composite | 0,014 | 0,004 | -0,032 | -0,038 | -0,012 | -0,044 |
| agents entretien (v3) | 0,016 | -0,016 | -0,044 | -0,048 | -0,015 | -0,052 |
| agents enquete | 0,011 | -0,012 | -0,041 | -0,056 | -0,018 | -0,058 |
| agents persona (v7) | 0,017 | -0,022 | -0,035 | -0,039 | -0,021 | -0,079 |
| agents demographiques (v6) | 0,024 | -0,032 | -0,062 | -0,081 | -0,001 | -0,091 |
| agents demographiques (v8) | 0,014 | -0,014 | **0,079** [0,062 ; 0,094] | -0,028 | -0,056 | -0,032 |

**Reponse claire : non.** La litterature rapporte 0,19 pour des agents contre -0,02 pour des
humains sur le World Values Survey. Sur le GSS, **la valeur humaine est retrouvee au
centieme pres**, -0,020 sur l'ideologie, ce qui indique que la mesure est bien implementee.
Mais **aucune condition d'agent n'approche 0,19**. Le maximum est 0,079, pour la seule
variante v8 sur la seule segmentation ideologique, avec un intervalle [0,062 ; 0,094] qui
exclut la valeur humaine. Toutes les autres cellules sont negatives : les segments
demographiques ne forment pas des amas dans l'espace des reponses, ni chez les humains ni
chez les agents.

**Hypothese sur l'origine de l'ecart, et comment la trancher.** Le fait que la valeur humaine
soit reproduite et pas la valeur agent oriente vers une difference de jeu de donnees et non
vers une erreur de calcul. Trois candidats, par ordre de plausibilite decroissante.

1. **Le jeu de donnees.** Nous mesurons sur le GSS, la litterature sur le World Values
   Survey. Le WVS est international : ses segments demographiques y sont imbriques dans des
   segments nationaux, et un modele de langage a des stereotypes nationaux beaucoup plus
   marques que des stereotypes intra americains. Un silhouette de 0,19 sur le WVS pourrait
   donc mesurer surtout une separation par pays. **Test decisif : recalculer le silhouette
   sur le WVS avec la meme distance, une fois avec le pays dans la segmentation et une fois
   sans.** Si l'ecart s'effondre en retirant le pays, la question est reglee.
2. **Le jeu d'items.** Nos 169 items du GSS melangent attitudes politiques, elements
   biographiques et faits de menage ; ces derniers ne sont pas segmentables par ideologie et
   diluent l'effet. **Test : refaire le calcul sur le seul sous ensemble attitudinal.**
3. **La distance ou la normalisation.** La source de 0,19 n'a pas ete relue pour ce rapport
   et pourrait employer un codage ordinal avec distance euclidienne, ce qui donnerait un
   poids arbitraire aux items a nombreuses modalites. **Test : relire la source, section
   methode.** C'est le moins couteux des trois et il doit etre fait en premier.

**Et une remarque qui vaut pour le dossier.** Le silhouette est lui meme une mesure globale
de separation : il agrege les 169 items et noie un effet localise sur l'ideologie politique,
qui est justement celui que la section 4 met en evidence. Le silhouette subit donc exactement
le defaut que ce rapport documente. Ce n'est pas le bon instrument, et c'est un argument
methodologique a garder.

Confiance sur le chiffre de 0,079 : elevee. Confiance sur l'explication de l'ecart avec la
litterature : faible tant que les trois tests ci dessus ne sont pas faits.

---

## 6. Le plafond humain : une distribution, et non une moyenne

Champ `p_wave1__p_wave2__accuracy` de
`figure3/data/new_analysis_summaries/gss_filtered/analysis/individual_level.csv`, 1052
individus.

Moyenne **79,53 pour cent**, identique au denominateur de normalisation du papier, ce qui
valide au passage la lecture du fichier. Ecart type 8,65 points. Centiles : 10e a 69,4,
mediane 81,3, 90e a 88,7. **Minimum 25,3 pour cent, maximum 97,3 pour cent.** 10,1 pour cent
des participants sont sous 70 pour cent de consistance, 3,5 pour cent sous 60.

**L'heterogeneite est reelle mais moderee**, coefficient de variation 10,9 pour cent, rapport
du 90e au 10e centile 1,28. Il faut le dire honnetement : elle ne suffit pas a invalider la
normalisation du papier au niveau agrege. Normaliser chacun par sa propre consistance puis
moyenner donne 0,865 pour les agents composite, contre 0,859 en divisant les deux moyennes.
L'ecart est de 0,006, negligeable.

**Ce qui, en revanche, est une vraie faiblesse.** Le score normalise varie fortement d'un
individu a l'autre. Pour les agents composite, ecart type des ratios individuels 0,089,
10e centile 0,776 et 90e centile 0,952. Un chiffre unique de 86 pour cent ne dit donc rien
de la fidelite pour une personne donnee, alors que c'est precisement ce que promet un
simulateur individuel. Et surtout, **la fidelite de l'agent est fortement correlee a la
stabilite propre de la personne** : r = 0,684 pour les agents composite, 0,53 et 0,54 pour
entretien et enquete, 0,37 pour les trois conditions pauvres. Autrement dit une part
substantielle de ce que mesure le score n'est pas une propriete du modele mais une propriete
du repondant. Deux consequences.

1. Un score moyen recompense un echantillon de personnes stables. Il n'est pas transferable a
   une autre population sans mesurer d'abord sa consistance test retest.
2. La chute de r de 0,68 a 0,37 entre les agents riches et les agents pauvres en information
   est elle meme un resultat : plus l'agent dispose de reponses reelles, plus il colle a
   l'individu, y compris a son instabilite.

Enfin, 4,6 pour cent des participants ont un agent composite plus fidele a leur vague 1 que
ne l'est leur propre vague 2. Le plafond n'est donc pas un plafond pour tout le monde.
Confiance : elevee, chiffres directement calcules.

---

## 7. Deux generations portent l'etiquette demographique, et notre mesure les separe d'un facteur sept

Cette section etait initialement redigee comme la limite principale du travail. La lecture de
la documentation du paquet montre qu'il ne s'agit pas d'une ambiguite de notre part mais d'un
fait du paquet, et le fait est plus interessant que la limite.

### 7.1 Les faits, avec leur source exacte

| # | fait | source dans le paquet |
|---|---|---|
| 1 | La figure 2, sous graphique GSS, ligne **Demographic-Based**, lit `p_wave1__gss_v6__accuracy` | `FIGURE2_PIPELINE.md`, section 6.1 |
| 2 | La figure 3, GSS, ligne **Demographic Agents**, lit `p_wave1__gss_v8__accuracy` | `FIGURE3_PIPELINE.md`, section 5.2 |
| 3 | `gss_v6` est commente **"GSS demographic-based (ablation demog)"** | `figure2/code/plotting/plot_figure_2.py`, ligne 102 |
| 4 | `"Demographic Agents"` est associe a `p_wave1__gss_v8__accuracy` | `figure3/code/dpd/build_dpd_summaries.py`, ligne 38 |
| 5 | `v8` est la variante **"demographic-ablation LA"**, avec la note explicite : *"`v8` is **not** interview-transcript-only ; it is `ablation (demog) -- LA` in the generation code"* | `camerer_five_studies_results.md`, section "Agent-type naming used in this repo", lignes 21 et 24 |

Les cinq points ont ete verifies dans les fichiers eux memes. Confiance : elevee.

Les deux figures du meme papier s'appuient donc sur deux generations differentes, toutes deux
designees comme demographiques pour le GSS. Ce ne sont pas deux etiquettes du meme fichier :
l'accord cellule a cellule entre `gss_v6` et `gss_v8` est de **60,8 pour cent** sur les 177
items et 1052 participants, c'est a dire du meme ordre que l'accord de chacune avec les
humains, 60,9 et 57,1 pour cent. Ce sont bien deux generations distinctes.

### 7.2 La collision d'etiquettes s'etend a tous les jeux de donnees

Detail supplementaire, verifie, et il aggrave le point. La correspondance entre etiquette de
generation et condition experimentale **n'est pas la meme d'un jeu de donnees a l'autre**.

| condition | GSS fig. 2 | GSS fig. 3 | Jeux econ. fig. 2 | Jeux econ. fig. 3 | Big-5 fig. 2 | Big-5 fig. 3 | Camerer |
|---|---|---|---|---|---|---|---|
| Entretien | `v3` | `v3` | **`v6`** | `v6` | `v5` | `v5` | `v2` |
| Demographique | **`v6`** | **`v8`** | **`v3`** | `v8` | `v3` | `v8` | `v8` |
| Persona | `v7` | `v7` | `v4` | `v4` | `v4` | `v4` | `v4` |

Sources : `FIGURE2_PIPELINE.md` sections 6.1, 6.2 et 6.3, `FIGURE3_PIPELINE.md` section 5.2,
`camerer_five_studies_results.md` lignes 18 a 22.

Deux collisions frontales sont a signaler. **`v3` designe la condition entretien pour le GSS
et la condition demographique pour les jeux economiques et le Big-5.** **`v6` designe la
condition demographique pour le GSS et la condition entretien pour les jeux economiques.**
Un tiers qui reproduirait ce travail en transposant la correspondance d'un jeu de donnees a
l'autre inverserait silencieusement deux conditions, sans aucun message d'erreur, et
publierait un resultat inverse.

Une regularite se degage et merite d'etre notee : la figure 3 et l'analyse Camerer emploient
`v8` comme condition demographique pour les trois jeux de donnees, tandis que la figure 2
emploie une etiquette propre a chaque jeu, `v6` puis `v3` puis `v3`. Ce n'est pas un desordre
aleatoire ; cela ressemble a deux campagnes de generation successives. **Cette lecture est une
hypothese, pas un fait etabli** : le paquet ne contient ni le code de generation ni les
invites, seulement le code d'analyse et de trace, ce qui a ete verifie par recherche
exhaustive sur les fichiers du paquet.

### 7.3 Ce que notre mesure ajoute

| condition GSS | exactitude, chiffre du papier | score normalise | ratio inter, notre mesure |
|---|---|---|---|
| agents demographiques `v6` | 58,12 % (et. type 7,02) | 0,74 | **0,855** [0,772 ; 0,943] |
| agents demographiques `v8` | 56,28 % (et. type 8,26) | 0,71 | **5,907** [5,495 ; 6,379] |
| agents persona `v7` | 56,21 % (et. type 8,29) | 0,71 | **0,437** [0,363 ; 0,513] |

Source des exactitudes :
`figure2/data/new_analysis_summaries/gss_filtered/summary/individual_level.csv`.

**Premier constat.** Les deux conditions demographiques different de **1,85 point
d'exactitude**, ecart apparie sur les 1052 participants, intervalle [1,41 ; 2,29], soit trois
points de score normalise. Sur notre mesure, leur gonflement des ecarts inter groupes differe
d'un **facteur 6,9**, 0,855 contre 5,907, avec des intervalles de confiance qui ne se
chevauchent pas du tout et ne s'en approchent pas. Une des deux ecrase les ecarts entre
groupes, l'autre les multiplie par six.

**Second constat, et c'est le plus fort.** `gss_v7`, la condition persona, et `gss_v8`, une
condition demographique, ont une exactitude **strictement indistinguable** : 56,21 contre
56,28 pour cent, ecart apparie **-0,07 point**, intervalle [-0,52 ; +0,37], t = -0,32. Sur la
metrique du champ, ce sont deux conditions equivalentes. Sur notre mesure, leurs ratios inter
sont 0,437 et 5,907, un **facteur 13,5**, avec des intervalles qui ne se chevauchent pas.
L'une compresse les ecarts entre groupes de plus de moitie, l'autre les multiplie par six.

Autrement dit : **la metrique d'exactitude ne distingue pas deux conditions dont la structure
de reponse est opposee.** Ce n'est pas un raffinement de notre mesure sur la leur, c'est une
dimension entiere que leur mesure ne voit pas.

### 7.4 Ce qui est etabli et ce qui ne l'est pas

**Etabli.** Deux generations distinctes existent dans le paquet. Elles portent toutes deux
l'etiquette demographique pour le GSS, chacune dans une figure differente du meme papier.
Elles se comportent tres differemment sur notre mesure, avec des intervalles disjoints.

**Non etabli, et il ne faut pas l'ecrire.** Que ce soit une erreur des auteurs. Ils ont pu
choisir sciemment une ablation differente par figure, par exemple parce que la figure 3 exige
une condition comparable entre trois jeux de donnees, ce que `v8` fournit et pas `v6`. Cette
explication est coherente avec la table de la section 7.2. Elle reste une hypothese.

**Non etabli non plus.** Ce qui differe concretement entre les deux generations. Le paquet ne
contient pas le code de generation. Le seul element est la mention `ablation (demog) -- LA`
pour `v8`, dont la signification de `LA` n'est explicitee nulle part dans le paquet. Ce qui
peut etre observe de l'exterieur, et c'est instructif : compte fait sur les seules reponses
conformes a la nomenclature, `v8` emploie en moyenne **3,07 modalites distinctes par item**,
`v6` 3,15, la condition persona `v7` 3,36, contre **3,62 chez les humains**. La variante qui
gonfle le plus les ecarts entre groupes est donc aussi celle qui emploie le vocabulaire le
plus pauvre. Elle ne distingue pas les segments en mobilisant plus de modalites, elle
distingue en allouant differemment un jeu de modalites plus restreint : c'est la signature
attendue d'un raisonnement par stereotype de groupe.

Avertissement de methode sur ce dernier chiffre, parce qu'il a failli etre publie a
l'envers. Compte sur les chaines brutes, sans appariement a la nomenclature, le classement
s'inverse : `v8` semble employer 4,48 modalites contre 3,62 aux humains, ce qui suggererait
un vocabulaire plus riche. L'ecart vient entierement des reponses mal formees des agents,
phrases de justification et variantes de ponctuation, dont chaque occurrence unique compte
comme une modalite nouvelle. Les humains n'en produisent aucune, section 1. Toute mesure de
diversite de reponse sur ces fichiers doit donc etre precedee d'un appariement a la
nomenclature, faute de quoi elle credite les agents d'une diversite qui n'est que du bruit
de formatage.

### 7.5 La consequence pour le champ

Si le gonflement des ecarts inter groupes varie d'un facteur sept entre deux variantes d'une
meme condition nominale, et d'un facteur treize entre deux conditions que la metrique
d'exactitude declare equivalentes, alors :

1. **Les chiffres publies sur les agents demographiques ne sont pas stables.** Selon la
   variante retenue, la meme condition nominale ecrase ou gonfle les ecarts entre groupes.
   Citer un chiffre de distorsion demographique sans nommer la generation exacte n'a pas de
   sens.
2. **Ils ne sont pas comparables entre etudes.** Deux equipes qui declarent toutes deux
   mesurer des agents demographiques peuvent mesurer des objets structurellement opposes, et
   la metrique d'exactitude ne le revelera pas.
3. **La metrique d'exactitude, seule, est insuffisante comme critere de publication.** Elle
   attribue le meme score a deux populations simulees dont la structure interne est inverse.
   C'est la these du projet, et elle est ici demontree **a l'interieur d'un seul papier**,
   sur les memes participants et les memes items, ce qui elimine toute explication par une
   difference de protocole, de population ou de periode.

Le troisieme point est le plus utile au dossier : il ne demande au lecteur de croire ni notre
mesure ni la leur, seulement de constater que deux conditions notees identiques par la
seconde sont notees opposees par la premiere.

**Test suivant, peu couteux.** Les fichiers `econ_games_v3` / `econ_games_v8` et
`bigfive_v3` / `bigfive_v8` sont presents dans le paquet, avec les memes 1052 participants.
Recalculer les deux ratios dessus dirait si l'ecart entre variantes demographiques se
reproduit hors du GSS. Si oui, le resultat cesse d'etre une particularite du GSS.

---

## 8. Limites, dans l'ordre de gravite

1. **L'agregation change l'amplitude, pas le sens.** Le tableau de la section 3 rapporte des
   sommes sur 169 items et 6 axes. La mediane des ratios item par item est plus basse : 1,24
   au lieu de 1,75 pour les agents composite, 2,18 au lieu de 5,91 pour `v8`. Le gonflement
   est donc porte surtout par les items ou l'information mutuelle humaine est deja elevee,
   c'est a dire les items politiques. Le signe et le classement sont inchanges. Toute
   publication doit donner les deux chiffres.
2. **L'effet principal repose sur l'ideologie politique**, qui est une attitude auto declaree
   et non une variable demographique. Voir section 4. En retirant cet axe, le gonflement des
   agents composite tombe de 1,75 a un voisinage de 1,3.
3. **Le bootstrap est recentre.** Le terme inter est une composante de variance de faible
   valeur ; un tirage bootstrap y ajoute une seconde couche de bruit d'echantillonnage, qui
   s'y loge entierement. Mesure : la moyenne bootstrap brute du terme inter depasse la valeur
   observee de 24 pour cent chez les humains contre 2 pour cent chez les agents `v8`, ce qui
   ecraserait tous les ratios vers 1. Les distributions bootstrap sont donc recentrees de
   facon additive sur l'estimation ponctuelle avant formation du ratio, ce qui est le
   bootstrap de base au sens de Davison et Hinkley. Les intervalles donnent la forme de la
   distribution d'echantillonnage, pas son centre.
4. **L'exclusion des huit items demographiques est necessaire, et verifiee.** En les gardant,
   le controle vague 2 tombe a 0,946 avec un intervalle [0,927 ; 0,970] qui **exclut 1** : la
   methode devient biaisee. La cause est identifiee, les humains se declarent avec une
   inconsistance normale entre deux vagues alors que les agents recopient l'attribut recu.
   Rejouable par `--tous-items`.
5. **Le ratio intra mesure ici, 0,64 a 0,89, est nettement plus haut que le 0,40 a 0,56 cite
   dans la these du projet.** L'ecrasement de la dispersion interne est donc reel mais plus
   faible qu'annonce. Meme hypothese qu'en section 5 : la valeur citee vient du World Values
   Survey et non du GSS, et un jeu international offre plus de dispersion intra a ecraser.
   **Trancher demande deux choses : relire la source du 0,40 - 0,56 pour savoir sur quelle
   mesure et quel jeu elle porte, puis recalculer notre decomposition sur le WVS ou sur
   Twin-2K-500 avec le meme code.** Tant que ce n'est pas fait, ne pas reprendre la fourchette
   0,40 - 0,56 comme si elle etait notre resultat.
6. **Six segmentations et non une.** Les ratios sommes melangent des partitions a 2 et a 18
   segments. Le detail par axe est fourni pour cette raison, et il est plus informatif que le
   chiffre agrege.
7. **Un seul jeu de donnees, un seul modele, une seule equipe.** Rien ici ne dit que le
   resultat tient hors du GSS et hors du pipeline de Stanford. La replication sur
   Twin-2K-500 est le test suivant.

---

## 9. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise.** Sur le GSS et sur le paquet de replication de Stanford, quatre conditions
d'agents sur six presentent simultanement un gonflement des ecarts entre segments
demographiques et un ecrasement de la dispersion interne, avec des intervalles a 95 pour cent
qui excluent 1 dans les deux sens. Ce fait est invisible aux mesures globales de dispersion,
qui restent entre 0,80 et 0,90. Le controle par reinterrogation des memes humains valide la
methode. Le resultat tient sur trois mesures de dispersion aux hypotheses disjointes.

**Autorise, et plus fort.** Deux conditions du meme papier, sur les memes participants et les
memes items, dont l'exactitude est indistinguable a 0,07 point pres, ont des gonflements
d'ecarts inter groupes qui different d'un facteur 13,5 avec des intervalles disjoints. La
metrique d'exactitude employee par le champ ne separe pas deux populations simulees de
structure opposee.

**Autorise, avec la source.** Deux generations portent l'etiquette demographique pour le GSS
dans le meme paquet de replication, l'une dans la figure 2 et l'autre dans la figure 3, et la
correspondance entre etiquette de generation et condition experimentale change d'un jeu de
donnees a l'autre.

**Interdit.** Ecrire que le phenomene de double distorsion est general : il n'apparait pas
pour les agents persona ni pour la variante `v6`, qui ecrasent les deux termes a la fois.
Ecrire que la compensation est exacte : le produit des deux ratios vaut 1,5 a 4,0, pas 1.
Reprendre le ratio d'ecarts types de 0,40 a 0,56 comme notre resultat : la compression
interne mesuree ici est de 0,64 a 0,89. Invoquer le score de silhouette de 0,19 comme un fait
etabli : il n'est pas retrouve ici, le maximum est 0,079. Et surtout, ecrire que les auteurs
se sont trompes sur `v6` et `v8` : ce n'est pas etabli, seule la divergence de comportement
l'est.

---

## 10. Fichiers produits

| fichier | contenu |
|---|---|
| `a1-figure-double-distorsion.png` et `.svg` | la figure, lisible en noir et blanc |
| `a1-ratios.csv` | les deux ratios, 3 mesures, 8 conditions, intervalles, mesure globale |
| `a1-ratios-par-axe.csv` | le meme detail pour chacun des 6 axes demographiques |
| `a1-silhouette.csv` | silhouette par condition et par axe, intervalles bootstrap |
| `a1-plafond-humain.csv` | distribution de la consistance test retest, effet de normalisation |
| `a1-controle-permutation.csv` | diagnostic de biais des trois estimateurs |
| `a1-etiquettes-demographiques.csv` | `gss_v6` contre `gss_v8` : tests apparies, accord, vocabulaire |

Attention : `.gitignore` exclut `*.csv` a la racine du depot, pour empecher tout commit de
microdonnees. Les sept fichiers ci dessus ne seront donc pas versionnes. Les chiffres qui
comptent sont recopies dans le present rapport, qui l'est.
