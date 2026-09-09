# d4. Page de plan preenregistree : la diversite politique d'un camp, en trois quantites qui ne sont pas la position des items

**Ecrite et horodatee le 2026-09-09 a 12:05 CEST, AVANT le moindre calcul.** Depot a
`d536169dc5361c38edcd723d48816e2ddd06dc4f`. Verification faite a cette minute :
`ls resultats/d4*` et `ls analyses/d4*` ne rendent aucun fichier. Aucun appel de modele de
langage dans ce chantier, aucun serveur d'inference, lecture seule sur `data/`, aucune
microdonnee ecrite. Aucun fichier existant n'est modifie ; tous les fichiers produits sont
prefixes `d4`.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## 1. Ce qui est teste, et pourquoi cette page existe

Amir, qui porte le projet, tient pour vrai que **la droite a plus de diversite politique que
la gauche**. `BRAINSTORM-DECISIONS-2026-09-09.md` point D4 tranche la place de cette
croyance dans le dossier : elle entre **comme prediction qui peut couter**, testee d'abord
chez les humains, **jamais comme premisse**. Cette page est ce test, a zero appel.

Elle existe parce que le dossier a deja mesure que la version naive de l'enonce est vraie et
sans interet. [MESURE, `a30-variete-interne-des-camps.md`] Sur les 149 items du GSS de
Stanford, la dispersion interne du camp de droite vaut **1,1225** fois celle du camp de
gauche, et le centre est indistinguable de la droite. [MESURE, `a37-consensus-liberal-et-simulation.md`
section 4] Sur les 79 items orientables, un temoin qui ne connait **que la position moyenne
de chaque camp** reproduit 1,211 la ou la mesure donne 1,220, et explique **98,1 pour cent**
de la variance item par item du logarithme du rapport ; sur les 46 items a plus de deux
modalites, la ou le temoin peut echouer, il explique encore 91,4 pour cent. La phrase que le
dossier defend aujourd'hui est donc : *la dispersion interne d'un camp sur un item n'est pas
une propriete du camp, c'est une consequence de sa position*.

**Ce que cette page ajoute.** Le 1,12 est mort comme mesure de diversite politique, mais la
croyance d'Amir n'est pas morte avec lui : elle porte sur autre chose que la dispersion
marginale item par item. Trois choses qu'un rapport de dispersion ne voit pas restent
disponibles, et ce sont exactement celles que la question 1 de `a37` section 10 laissait
ouverte : « **y a t il une mesure de consensus intra camp qui soit orthogonale a la
position ?** ». Cette page en propose trois, les preenregistre, et engage un pari.

---

## 2. Ce que le corpus dit deja, et qui n'est pas ce qu'Amir croit

Tout ce bloc est **[CONFIRME]**, lu dans `corpus/05-structure-attitudes-heterogeneite-ideologique.md`
et `corpus/lecture-complete/05-structure-attitudes-heterogeneite-ideologique.md`.

| source | ce qu'elle dit | sens pour H_Amir |
|---|---|---|
| Ditto et al. 2019, 51 tests, N 18 815 | biais partisan liberaux 0,235, conservateurs 0,255, difference 0,009 non significative | **contre** : symetrie |
| Ondish et Stern 2018, GSS et ANES, 80 000 personnes, 400 items, 40 ans | liberaux > conservateurs > moderes en consensus national | **pour**, mais c'est le 1,12 dont a37 montre qu'il est de la position |
| Brandt et al. 2022, ESS 38 pays N 376 129, et Eurobarometre N 375 830 | replication nette sur l'ESS, **aucune** sur l'Eurobarometre | partage, depend du jeu d'items |
| Brandt et Sleegers 2021, 40 populations simulees | mecanisme generatif : le consensus suit la derive agregee des items, liberaux gagnants dans 35 populations sur 40 | **explique** l'asymetrie sans propriete de camp |
| Cely 2025, ESS, 131 partis, 15 pays | la gauche est **plus** alignee, asymetrie large, mais la droite se resserre sur le socioculturel | pour, sur une mesure d'alignement |
| Hanel et al. 2019, ESS 20 pays | les **extremes**, des deux cotes, sont plus heterogenes que les moderes | contre : ce n'est pas un axe gauche droite |
| Treier et Hillygus 2009, ANES 2000 | 38 pour cent des conservateurs declares hors de leur quadrant contre 35 pour cent des liberaux ; les auteurs l'attribuent a la **desirabilite de l'etiquette**, pas a une difference cognitive | pour, faiblement, et pour une raison symbolique |
| Warncke, Chen, Luders et al. 2026, ResIN | avec la meme methode et la meme equipe : droite plus cohesive en Espagne, gauche plus cohesive aux Etats Unis | contre l'universalite |
| Grossmann et Hopkins 2016 | les republicains « prize doctrinal purity » : plus homogenes sur **l'etiquette et le principe**, pas sur les items | l'enonce d'Amir peut etre vrai a un niveau et faux a l'autre |

[MESURE, `a30`] Le controle interne qui tranche le point le plus important : le rapport vaut
**1,122 en segmentant par `polviews`** (l'etiquette symbolique) et **1,094 en segmentant par
`partyid`** (l'appartenance partisane). L'ecart est plus grand sur l'etiquette que sur le
parti, ce qui est le sens attendu si l'asymetrie est symbolique.

**Ce que cela impose ici.** Aucune asymetrie n'est postulee. La direction de H_Amir est
ecrite d'avance, elle est unilaterale au niveau du verdict et bilaterale au niveau de chaque
test, et le contraire de H_Amir est un pari du dossier qui peut se perdre.

---

## 3. La definition : la diversite politique d'un camp, en trois quantites

Une quantite est admissible ici si et seulement si elle satisfait le **critere
d'orthogonalite** suivant, ecrit avant tout calcul.

> **Critere O.** Une quantite de diversite est admissible si sa valeur est **inchangee**
> quand on remplace le camp par une population fictive qui a, item par item, exactement la
> meme distribution marginale de reponses, mais aucune structure entre items et aucune
> structure individuelle. Autrement dit : le generateur nul de `a44` (tirage multinomial
> independant dans la loi de l'item a l'interieur du camp) doit donner a la quantite une
> valeur de reference connue, et la quantite publiee est l'**ecart** a cette reference.

Le critere O est la transposition litterale de la lecon de `a37` : la position d'un camp sur
un item **est** sa marginale ; toute quantite qui ne depend que des marginales est une
quantite de position deguisee, et le dossier a deja montre qu'elle ne mesure rien du camp.
C'est aussi le critere de gabarit de `a44` [CONFIRME, `a44-generateur-nul.md`], applique ici
non plus aux agents mais aux humains.

Les trois quantites, dans l'ordre ou elles seront publiees.

### Q1. Dispersion residuelle, apres controle de la position de l'item et de sa polarite

Pour chaque item `j` et chaque camp `c`, on calcule deux nombres sur exactement les memes
personnes et le meme item :

- `GS_obs(j, c)` : l'indice de Gini Simpson sans biais, estimateur de `a30_commun`, importe
  sans changement.
- `GS_pos(j, c)` : le **temoin de position** de `a37_commun.gs_temoin`, c'est a dire la
  dispersion de la loi d'entropie maximale a moyenne fixee a la position observee du camp
  sur l'echelle de l'item, ramenee a l'echelle de l'estimateur sans biais par le facteur
  `N / (N - 1)`.

**La quantite est le residu** `R(j, c) = GS_obs(j, c) - GS_pos(j, c)`, et la statistique
publiee est la moyenne sur les items du **contraste apparie** `R(j, droite) - R(j, gauche)`.

*Pourquoi elle satisfait le critere O.* `GS_pos` ne depend que de la marginale du camp sur
l'item. Le residu est donc, par construction, ce que la marginale n'explique pas : la forme
de la distribution au dela de sa moyenne. Sous le generateur nul, `GS_obs` et `GS_pos`
different encore, parce que la loi empirique n'est pas la loi de maximum d'entropie a la
meme moyenne ; la reference n'est donc **pas** zero et sera mesuree, jamais supposee.

*Restriction obligatoire, ecrite d'avance.* **Sur un item binaire, la moyenne determine
entierement la loi et `R` vaut zero au dernier chiffre** [MESURE, `a37` section 2.3]. Les 33
items binaires orientes n'apportent donc aucune information a Q1 et ne peuvent que diluer le
contraste vers zero. **Q1 est calculee sur les seuls items a trois modalites ou plus.**
C'est une restriction du perimetre, pas un choix apres coup, et elle est ecrite ici.

*Controle de polarite.* Le residu moyen est ensuite regresse sur la derive agregee `D` de
l'item (definition de `a37_commun.derive`, `D > 0` veut dire que l'echantillon penche a
droite) et sur `|D|`. Si le contraste `R(droite) - R(gauche)` depend encore du signe de `D`,
alors Q1 n'est pas orthogonale a la polarite et le dossier doit le dire. Le contraste est en
outre publie separement dans les deux classes `D < 0` et `D > 0`, ce qui est le test T1 de
`corpus/05` porte sur une quantite residuelle au lieu du rapport brut.

### Q2. Nombre de profils de reponses distincts par camp, a taille egale, en exces du nul

Sur `J_sous = 10` items tires au hasard parmi le perimetre, et `n_egal` personnes tirees sans
remise dans chaque camp (le meme `n_egal` pour tous les camps, egal au plus petit effectif
de camp du perimetre), on compte le nombre de **lignes distinctes**. Convention de `a44` :
une ligne portant une cellule vide est ecartee de son sous ensemble. 200 sous ensembles
d'items, 20 tirages de personnes par sous ensemble.

La quantite publiee est l'**exces sur le nul** :
`E(c) = patrons_obs(c) - patrons_nul(c)`, ou `patrons_nul(c)` est la meme mesure sur une
population fictive de meme taille dont chaque cellule est tiree independamment dans la loi
empirique de l'item **a l'interieur du camp c** (`a44_commun.lois_par_segment` et
`tirer_nul`, importes sans changement, avec le segment reduit au camp). La statistique est
`E(droite) - E(gauche)`.

*Pourquoi elle satisfait le critere O.* Le nul a exactement les memes marginales par camp et
par item, donc exactement les memes positions. Tout ce qui separe `patrons_obs` de
`patrons_nul` est de la dependance entre items a l'interieur du camp, c'est a dire de la
contrainte ideologique.

*Sens attendu du signe, ecrit d'avance.* L'independance maximise le nombre de combinaisons ;
une population contrainte en produit moins. **`E` est donc negatif dans les deux camps, et
un `E` moins negatif veut dire un camp moins contraint, donc plus divers.** H_Amir predit
`E(droite) > E(gauche)`. Toute lecture qui inverserait ce sens serait une erreur de lecture
et non un resultat.

### Q3. Dimension effective de la structure de correlation entre items, camp par camp

Sur le meme perimetre d'items et a taille egale, on calcule la matrice de correlation de
Spearman entre items a l'interieur du camp (les rangs de `a44_commun.rangs_colonne`,
importes sans changement), puis sa **dimension effective**, ou rapport de participation :

    D_eff = (somme des valeurs propres)^2 / (somme des carres des valeurs propres)

`D_eff` vaut `J` exactement quand les items sont mutuellement decorreles, et 1 quand une
seule dimension porte tout. C'est la generalisation de la part de variance de la premiere
composante que `a30` mesure en S2, et elle a l'avantage de ne pas dependre du choix
arbitraire d'un seuil cumule.

La quantite publiee est le **rapport a la dimension effective du nul** :
`Deff_norm(c) = D_eff(c) / D_eff_nul(c)`, ou le nul est celui de Q2, qui a les memes
marginales et aucune correlation vraie. La statistique est
`Deff_norm(droite) - Deff_norm(gauche)`. H_Amir predit une valeur positive : la droite serait
moins contrainte, donc plus proche du nul decorrele.

*Pourquoi elle satisfait le critere O.* Une correlation entre deux items n'est pas une
fonction de leurs marginales ; mais l'**etendue atteignable** d'une correlation depend de
l'asymetrie des marginales, et l'estimation d'une matrice de correlation sur `n` personnes
porte un biais qui gonfle `D_eff` quand `n` est petit. Le denominateur `D_eff_nul` absorbe
exactement ces deux effets, puisqu'il est calcule sur les memes marginales et le meme `n`.

*Le plancher de bruit est obligatoire ici.* [CONFIRME, `a42-plancher-de-bruit.md` et
`a1-double-distorsion.md`] Une matrice de correlation estimee sur des reponses humaines
contient du bruit de reponse : les memes personnes reinterrogees deux semaines plus tard ne
redonnent pas les memes reponses, et une part de `D_eff` est ce bruit. Le plancher est donc
la **meme statistique recalculee sur la vague 2** du GSS de Stanford, memes personnes, memes
items, deux semaines plus tard. Un ecart `Deff_norm(droite) - Deff_norm(gauche)` dont la
valeur absolue est inferieure a l'ecart mesure entre les deux vagues **ne sera pas commente**.

---

## 4. Les donnees, les perimetres, les effectifs

| jeu | fichier | personnes | items | camps | role |
|---|---|---|---|---|---|
| **GSS de Stanford** | `data/osf-t6g7k-stanford/figure2/.../p_wave1_summary.csv` et `p_wave2_summary.csv` | 1 052, memes personnes aux deux vagues | 149, dont **79 orientables** | `political_ideology` replie en trois par `a30_commun.GSS_BLOC3` : gauche 417, centre 303, droite 332 | **mesure principale**, et plancher de bruit a deux semaines |
| **Twin-2K-500** | `data/twin2k500/`, vagues 1 a 3 et vague 4 | 2 058 | 609 categoriels hors demographies, dont le bloc `attitudes` et les 10 items de politique publique de `QID287` | `QID22` replie en trois : gauche 909, centre 582, droite 567 | **replication**, autre recrutement, autre annee, autres items ; plancher de bruit vague 4 |
| **panels GSS de NORC** | `data/gss-panel/*.dta`, quatre panels 2006-2010, 2008-2012, 2010-2014, 2016-2020 | 2 000, 2 023, 2 044 et 5 215, **echantillons disjoints** | noyau commun de 118 items de `a12`, dont **76 orientes** | `polviews` replie par `i1_commun.bloc_ideologie` | **replication externe** : vrais echantillons probabilistes, quatre tirages independants, quinze annees ; plancher a deux et quatre ans |

**Perimetres d'items declares d'avance.**

- `P1`, principal : les items **orientes politiquement** du jeu, c'est a dire les 79 items de
  `a37_commun.ORIENTATION` sur le GSS de Stanford, les 76 correspondants sur les panels, et
  le bloc `attitudes` plus les dix items de `QID287` sur Twin. Q1 y est restreinte aux items
  a trois modalites ou plus (46 sur 79 pour le GSS de Stanford).
- `P0`, controle de falsification : les items **non orientables** du meme jeu, c'est a dire
  les 70 items du GSS que `a37_commun.SANS_ORIENTATION` ecarte (faits biographiques,
  equipement, sante, bien etre, confiance interpersonnelle, pratique religieuse), et sur Twin
  les 275 items de personnalite. **Si l'avantage de la droite est le meme sur `P0` que sur
  `P1`, ce n'est pas de la diversite politique**, c'est une propriete de style de reponse, et
  H_Amir tombe meme si elle est confirmee sur `P1`. Ce controle est bloquant.

**Effectifs egalises.** `n_egal` = plus petit effectif parmi les camps compares dans le
perimetre. Pour le GSS de Stanford avec le centre : 303. Pour la comparaison droite contre
gauche seule : 332. Le nombre est fixe une fois par jeu, avant tout calcul, et le meme
`n_egal` sert a l'observe, au nul et au plancher.

**Le centre est calcule partout et publie partout.** [MESURE, `a30`] Le centre est
indistinguable de la droite sur le rapport de dispersion. Si le centre egale ou depasse la
droite sur Q1, Q2 et Q3, l'enonce « la droite a plus de diversite politique » est faux meme
si le contraste droite contre gauche est positif : la quantite mesuree serait « ne pas etre
de gauche », pas « etre de droite ». Cette lecture est ecrite ici et sera appliquee.

---

## 5. Les hypotheses, et le pari qui peut couter

**H_Amir.** Sur le perimetre `P1` du GSS de Stanford, le camp de droite est plus divers que
le camp de gauche sur **au moins deux des trois quantites** Q1, Q2, Q3, avec le signe predit,
un intervalle de bootstrap qui exclut zero, un `p` de Holm inferieur a 0,05 dans la famille
de trois, et une ampleur superieure au plancher de reinterrogation.

**H_dossier, le pari du dossier, ecrit et engage.** *Il n'y a pas d'asymetrie droite gauche
robuste au controle de la position des items.* Le dossier parie que **zero ou une seule** des
trois quantites porte un contraste significatif dans le sens de H_Amir, et que la ou un
contraste apparait il ne survit pas a au moins un des quatre controles bloquants de la
section 8.

**Ce que le pari coute s'il est perdu.** Si H_Amir est confirmee au sens de la section 7,
alors, sans discussion et le jour meme :

1. La phrase publique du dossier, « la dispersion interne d'un camp n'est pas une propriete
   du camp mais une consequence de sa position » (`a37` section 4), devient **fausse comme
   enonce general** et doit etre restreinte par errata a la dispersion marginale item par
   item, en nommant la quantite qui echappe.
2. L'interdiction numero 1 de `a30` section 9, « interdit d'ecrire que la droite est plus
   heterogene que la gauche sans nommer le domaine », est **maintenue mais retournee** : le
   domaine devient nommable et le dossier doit ecrire l'enonce positif.
3. `a32-papier-diversite-droite.md` cesse d'etre un papier sur un artefact de position et
   devient un papier sur une asymetrie mesuree, avec le changement de these que cela impose.
4. La question 1 de `a37` section 10, posee a Simon, recoit une reponse **oui** : il existe
   une mesure de consensus intra camp orthogonale a la position, et c'est nous qui l'avons.

**Ce que la confirmation de H_dossier coute a Amir.** Elle ne dit pas que sa croyance est
absurde ; elle dit qu'elle est vraie au niveau ou le corpus la met, l'etiquette et le
principe general (Grossmann et Hopkins), et **pas** au niveau des reponses individuelles aux
items, qui est le seul niveau que ce projet mesure. Ce sera ecrit comme cela, sans
menagement et sans jugement, dans la section « ce que ce resultat dit a Amir » du rapport.

---

## 6. Les tests, les familles, la correction de Holm

**Famille A, principale, trois tests, Holm dans une famille de trois.**
A1 : contraste Q1, droite moins gauche, sur `P1` du GSS de Stanford.
A2 : contraste Q2, droite moins gauche, meme perimetre.
A3 : contraste Q3, droite moins gauche, meme perimetre.

**Famille B, replication Twin, trois tests, Holm dans une famille de trois**, jamais melangee
a la famille A.
**Famille C, replication panels NORC, trois tests, Holm dans une famille de trois**, jamais
melangee aux deux autres. Les quatre panels sont d'abord agreges en une seule estimation par
moyenne ponderee par l'effectif ; le detail par panel est publie a cote comme quatre
replications independantes, sans test.

**Famille D, controle de falsification, trois tests, Holm dans une famille de trois** : les
memes trois contrastes sur le perimetre `P0`. Un test de la famille D qui **passe** est un
argument **contre** H_Amir, et c'est ecrit ici pour que ce ne soit pas relu a l'envers.

**Hors famille, publie sans test corrige** : le contraste centre moins gauche, le contraste
droite moins centre, la decomposition de Q1 par signe de la derive, les regressions de
controle de polarite, et les quatre planchers de bruit.

**Intervalles.** Bootstrap sur les **personnes**, jamais sur les cellules, 1 000 tirages,
percentiles a 2,5 et 97,5 pour cent. Pour Q2 et Q3, qui sont deja des moyennes sur des sous
echantillons a taille egale, l'intervalle est celui de la distribution des contrastes
apparies tirage par tirage, avec le test d'inversion de signe de `a30_structure.apparie`,
importe sans changement. Pour Q1, contraste apparie item par item, meme fonction.

**Graine unique** `20260909`, declaree ici, une seule pour tout le chantier.

---

## 7. Ce qui compte comme « asymetrie etablie » et ce qui compte comme « refutee »

**Asymetrie etablie.** Les quatre conditions ensemble, aucune n'etant negociable :

1. **Au moins deux des trois** quantites Q1, Q2, Q3 ont un contraste droite moins gauche du
   signe predit, intervalle de bootstrap excluant zero, `p` de Holm inferieur a 0,05 dans la
   famille A.
2. Chacun de ces contrastes est **superieur en valeur absolue au plancher de
   reinterrogation** du meme contraste, mesure sur la vague 2 du GSS de Stanford.
3. Le signe est **le meme dans au moins une replication**, famille B ou famille C, sur les
   memes quantites, avec un intervalle excluant zero.
4. Le controle `P0` de la famille D **ne reproduit pas** l'avantage : le contraste sur les
   items non politiques est soit non significatif, soit inferieur en ampleur a la moitie du
   contraste sur `P1`.

**Asymetrie refutee.** Une des trois situations suivantes suffit :

1. **Zero ou une seule** des trois quantites passe, apres Holm, dans la famille A.
2. Les contrastes passent mais le controle `P0` les reproduit a plus de la moitie de leur
   ampleur : ce serait un style de reponse et non de la diversite politique.
3. Le signe **s'inverse** entre le GSS de Stanford et au moins une des deux replications,
   avec deux intervalles disjoints. C'est le motif que Brandt et al. rencontrent entre l'ESS
   et l'Eurobarometre, et il compte comme refutation de l'universalite de l'enonce, pas comme
   bruit.

**Asymetrie non concluante.** Tout le reste, et en particulier : deux quantites passent mais
aucune replication ne confirme ; ou les contrastes sont significatifs et sous le plancher de
bruit ; ou le centre egale ou depasse la droite sur les trois quantites. **Le rapport
ecrira « non concluante » quand ce sera le cas, et ne convertira pas un resultat non
concluant en verdict.**

---

## 8. Les quatre controles bloquants, ecrits avant les chiffres

1. **Le nul de gabarit.** Q2 et Q3 ne sont publiees que comme ecarts a un nul qui a les memes
   marginales par camp. Si l'ecart entre l'observe et le nul est du meme ordre que l'ecart
   entre deux replicats du nul, la quantite ne mesure rien et elle est retiree.
2. **L'effectif egalise.** Les trois quantites croissent ou decroissent avec `n`. Toute
   comparaison entre camps se fait a `n_egal` fixe, et la sensibilite a `n_egal` est publiee
   sur trois valeurs.
3. **L'appariement demographique exact.** Le contraste principal est recalcule sur des sous
   echantillons apparies cellule par cellule sur genre x race x age x education
   (`a30_commun.poids_appariement` et `cellules_gss`, importes sans changement). [MESURE,
   `a30`] Sur le rapport de dispersion, cet appariement **augmente** l'ecart au lieu de le
   reduire ; rien ne dit qu'il en va de meme sur Q1, Q2 et Q3.
4. **L'ancrage partisan.** Le contraste principal est recalcule avec les camps definis par
   `partyid` au lieu de `polviews`. [MESURE, `a30`] La fiabilite de `partyid` est 0,84 contre
   0,66 pour `polviews`, et le rapport de dispersion passe de 1,122 a 1,094 par ce seul
   changement. **Une asymetrie qui ne survit pas au changement d'ancrage n'est pas une
   difference entre camps, c'est une difference d'echelle.**

**Critere de chute du chantier entier.** Si le generateur nul reproduit a lui seul les trois
contrastes, c'est a dire si `E(droite) - E(gauche)` et
`Deff_norm(droite) - Deff_norm(gauche)` sont indistinguables de zero **parce que l'observe et
le nul bougent ensemble**, alors les trois quantites sont des quantites de gabarit au sens de
`a44` et ce chantier ne repond pas a la question de `a37`. Ce cas est un resultat et sera
publie comme tel.

---

## 9. Ce qui est fige ici, et ne bougera plus

- Les trois quantites, leurs formules, leur sens de signe, et le critere O.
- Les perimetres `P1` et `P0`, et la restriction de Q1 aux items a trois modalites ou plus.
- `J_sous = 10` items par sous ensemble, 200 sous ensembles, 20 tirages de personnes, 1 000
  tirages de bootstrap, 50 replicats du generateur nul.
- `n_egal` = plus petit effectif de camp du perimetre, calcule sur les donnees et non choisi.
- La graine 20260909, unique.
- Les quatre familles de tests et la correction de Holm a l'interieur de chacune, jamais
  entre elles.
- Les criteres de la section 7, mot pour mot.
- Les quatre controles bloquants de la section 8.

**Ce qui n'est pas fige et sera declare comme tel dans le rapport** : le detail du codage des
items des panels NORC, qui depend de ce que les fichiers `.dta` contiennent reellement et qui
sera verifie a l'execution ; et le nombre exact d'items de Twin retenus dans `P1`, qui depend
du catalogue.

---

## 10. Ce que je n'ai pas pu verifier

1. **Le critere O n'est pas une preuve d'orthogonalite, c'est un test.** Une quantite peut
   passer le critere O et rester correlee a la position par un canal que le nul multinomial
   ne reproduit pas, par exemple si la position d'un camp sur un item est elle meme
   correlee, a travers les items, avec la force de sa contrainte ideologique. Ce canal est
   reel et je ne peux pas le fermer avec ces donnees ; je peux seulement le mesurer, par les
   regressions de controle de polarite de Q1.
2. **Q3 suppose que la correlation de rang entre deux items a un sens comparable d'un camp a
   l'autre.** Si un item est presque unanime dans un camp, sa correlation avec tout le reste
   est mal estimee et le rapport de participation en souffre. Le denominateur `D_eff_nul`
   corrige l'esperance mais pas necessairement la variance.
3. **Le plancher de reinterrogation du GSS de Stanford est a deux semaines.** [MESURE, `a12`]
   La fidelite humaine vaut 77,79 pour cent a deux semaines, 69,53 a deux ans et 67,45 a
   quatre ans : le plancher a deux semaines est le plus favorable de tous et **sous estime**
   le bruit. Les panels NORC donneront un plancher a deux et quatre ans, mais sur d'autres
   personnes et d'autres items.
4. **Aucune de ces trois quantites n'a d'homologue publie.** Ondish et Stern publient un ICC
   de modele multiniveau, Cely une mesure d'alignement de reseau, Hanel une dispersion de
   valeurs. Je ne peux comparer mes chiffres a aucune valeur de reference exterieure, et je
   ne pretendrai pas le contraire.
5. **L'orientation des items est celle de `a37`**, dont 39 sur 79 sont de niveau [PROBABLE]
   et 14 de niveau [HYPOTHESE]. Q1 en depend pour le seul controle de polarite ; Q2 et Q3
   n'en dependent que par la definition du perimetre `P1`.
6. **Les items des panels NORC ne sont pas exactement ceux du GSS de Stanford.** Le noyau
   commun de `a12` compte 118 items dont 76 orientes ; les 3 items orientes manquants et les
   differences de nombre de modalites seront comptes et publies, mais ils empechent une
   comparaison chiffre a chiffre entre les deux perimetres GSS.

---

## 11. Questions ouvertes pour Simon

1. **Le critere O est il le bon critere ?** Une quantite de diversite d'un groupe qui est
   invariante sous remplacement du groupe par un tirage independant dans ses propres
   marginales : est ce une definition connue ailleurs, en ecologie ou en genetique des
   populations, ou est ce que je reinvente un objet qui a deja un nom ?
2. **Si Q2 et Q3 disent la meme chose, laquelle publier ?** Les deux mesurent la contrainte
   entre items, l'une par le comptage de combinaisons, l'autre par le spectre de la matrice
   de correlation. Si elles sont fortement correlees sur nos donnees, est ce une force, deux
   mesures independantes qui concordent, ou une redondance qui ne doit compter que pour un
   seul test dans la famille de Holm ?
3. **Le controle `P0` est il assez severe ?** Il compare le politique au non politique a
   l'interieur du meme questionnaire. Un style de reponse pourrait etre specifique aux items
   d'opinion sans etre politique. Faut il un troisieme perimetre, des items d'opinion non
   politiques ?
4. **A quel niveau la croyance d'Amir est elle vraie ?** Grossmann et Hopkins soutiennent que
   la purete doctrinale republicaine porte sur l'etiquette et le principe general, pas sur
   les items ; notre mesure ne voit que les items. Existe t il un plan de mesure, sur des
   donnees deja publiees, qui separe proprement les deux niveaux ?
