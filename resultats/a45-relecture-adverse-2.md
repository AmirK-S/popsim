# a45. Seconde relecture adverse : les vingt tests du 8 septembre et de la nuit

Role tenu : relecteur hostile de PNAS, NeurIPS ou Political Analysis, qui a lu Yuan, Peng,
Ahn, van Buuren et Rennard, et qui cherche la phrase qui ne survit pas. Date : 8 septembre
2026. Aucun fichier existant n'a ete modifie, aucun appel de modele n'a ete fait,
`data/` a ete lu seulement.

Convention, reprise de a17 : **[VERIFIE]** si l'objection a ete reproduite par calcul sur les
donnees ou par lecture du code, **[PROBABLE]** si elle vient d'une lecture attentive des
rapports sans recalcul, **[HYPOTHESE]** sinon.

Ce rapport ne rejoue pas a17. Les objections de a17 qui restent ouvertes sont citees quand
elles se propagent dans un rapport neuf, jamais reformulees pour elles memes.

Deux remarques d'entree, en faveur du dossier, parce qu'elles conditionnent la lecture de ce
qui suit. Un, les rapports de la nuit sont, dans l'ensemble, plus severes envers eux memes
que la premiere relecture ne l'etait envers a1 : a44 declare que son critere primaire ne
separe rien, a41 declare qu'il n'est pas preenregistre, a42 declare que son propre instrument
de terciles tombe, i1 declare que son controle 2 etait vide. Deux, la plupart des objections
faciles sont deja ecrites dans les sections « ce que je n'ai pas pu verifier ». Ce rapport ne
compte donc pas ces aveux comme des trouvailles ; il cherche ce qui n'y est pas.

---

## Sommaire des verifications faites

Calculs rejoues avec `.venv/bin/python`, quatre coeurs, aucun appel de modele, en relisant
les caches `/tmp/a25-matrices.pkl`, `/tmp/a28-foret.npy` et `/tmp/a35-methodes.pkl` par
`a44_commun.charger` :

- la chute d'exactitude sous permutation intra segment recalculee pour treize conditions sous
  **neuf segmentations** au lieu des deux du preenregistrement de a44 : aucune segmentation,
  ideologie, ideologie x genre x age, genre, race, age, genre x race x age, parti,
  education x revenu ; puis la meme chose pour C2 et C3 sur les 150 personnes ;
- la meme chute apres retrait des onze items que les conditions recopient a plus de
  95 pour cent, liste etablie par un balayage complet des 149 items x 10 conditions ;
- l'intervalle bootstrap sur les personnes de la chute, absent de `a44-permutation.csv`,
  300 tirages apparies ;
- le plancher de sur ajustement du troisieme terme de a44, la reassignation hongroise,
  lu sur le temoin `B0 tirage` de son propre fichier ;
- la correlation entre exactitude brute et chute sous permutation sur les treize conditions ;
- **le facteur d'amplification de a38 recalcule a l'identique** (v8 3,091, composite 1,829,
  B1 1,209, B2 0,973, humains vague 2 1,025, tous au millieme des valeurs publiees), puis
  soumis a la permutation intra camp et **au generateur nul de a44** ;
- lecture du code de `a44_commun.py`, `a44_mesures.py`, `a35_commun.py`, `a35_familles.py`,
  `a38_mesures.py`, `a28_test1_mode.py`, `a5_agents_locaux_gss.py`, `a2_baselines_gss.py`,
  `a28_commun.py`, `i1_commun.py`, `i1_previsibilite.py` ;
- lecture des fichiers `a44-permutation.csv`, `a44-quantites.csv`, `a38-camp.csv`,
  `a38-camp-robustesse.csv`, `a38-corrections.csv`, `a42-stabilite.csv`,
  `a41-cout-du-retrait.csv`, `a41-c3f-60-personnes.csv`, `a35-couples-regime.csv`,
  `a35-choix-penalite.csv`, `a37-agents-gss.csv`, `a37-agents-gss-150.csv`,
  `i1-auc-synthese.csv`, `i1-nul-remelange.csv`, `i3-reference-humaine.csv`,
  `i3b-twin-reference.csv`, `i3b-reference-par-taille.csv` ;
- horodatage et etat de suivi de version des six preenregistrements.

---

# 0. Le point qui traverse dix rapports : C2 contre C3 n'est pas une ablation de l'etiquette

Ce paragraphe est place avant les sections parce qu'il porte sur la phrase la plus repetee du
dossier et qu'il change la lecture de six mesures presentees comme independantes.

### 0.1 Ce que les invites contiennent reellement. Gravite : bloquante. [VERIFIE]

`analyses/a5_agents_locaux_gss.py`, lignes 165 a 196 :

- `systeme_c2` construit un prompt qui contient **les onze attributs de
  `demographic_summary.csv` et rien d'autre**. Aucune reponse de la personne au
  questionnaire.
- `systeme_c3` construit un prompt qui contient **les environ 119 items de contexte, question
  et reponse en clair**, et **aucune demographie**, aucun attribut, aucune etiquette.

C2 et C3 ne different donc pas par la presence ou l'absence de l'etiquette ideologique :
**ils echangent integralement leur entree**. C2 a l'etiquette et n'a pas la personne ; C3 a la
personne et n'a pas l'etiquette. Le contraste est un contraste de conditionnement a deux
facteurs confondus, pas une ablation a un facteur.

Deux rapports le disent, huit textes le contredisent.

| dit le vrai | dit le contraire |
|---|---|
| a35 section 11 point 5, « le contraste de conditionnement n'est pas controle » | a29 section 8 point 1, « C2 contre C3 est une ablation propre » |
| a43 section 1, tableau des trois conditionnements, qui range C3 dans « 119 reponses de la personne, non, ils voient la personne » | a38 section 4.4 lecture 4, « l'etiquette est ce qui produit la caricature » |
| | a39, « le seul couple ou le modele, les personnes, les questions et les traces sont constants et ou seule l'etiquette bouge, C2 contre C3 » (lignes 47, 353, 448) |
| | a42 section 6, « C2, le meme modele avec onze attributs demographiques » (ligne 72) |
| | a44 sections 7.2 et 10 point 3, « C3, qui est le meme modele et le meme run sans etiquette » (lignes 672, 783) |
| | `ARBITRAGE.md` point 2, « a modele, personnes et questions constants, la seule presence de l'etiquette fait la difference. Six mesures independantes le disent » |
| | `MODELE-DU-MONDE.md` 10.4, « le meme modele, les memes personnes et les memes questions donnent 7 pour cent du plancher avec l'etiquette et 45 pour cent sans » |

La formule de a42, « le meme modele **avec** onze attributs demographiques », est celle qu'un
relecteur citera : elle dit littéralement que C2 est C3 plus l'etiquette, ce que le code
refute en trois lignes.

**Ce que la difference entre les deux facteurs vaut, chiffre.** Le dossier possede les deux
analogues statistiques exacts : `B1 argmax` est une regression sur les onze memes attributs,
`B2 argmax` est un plus proche voisin sur les memes 119 items sans aucune demographie. Le
passage de l'un a l'autre, a moteur statistique constant et **sans aucune ablation
d'etiquette**, deplace la chute sous permutation de **0,175 a 0,358 du plancher humain**, soit
un facteur 2,0 [VERIFIE, `a44-permutation.csv`]. Le passage de C2 a C3 vaut un facteur 6,2. Le
changement d'information explique donc a lui seul une part que le dossier attribue en entier
a l'etiquette, et personne ne l'a bornee.

**Conséquence pour la revendication de nouveaute.** `MODELE-DU-MONDE.md` section 5 place en
tete de ce qui est libre « l'ablation de l'etiquette a modele, personnes, questions et traces
constants : personne ». Si le dossier ne l'a pas faite non plus, la revendication est vide, et
c'est exactement ce qu'un relecteur qui lit le code de l'invite ecrira.

**Correction proposee.** Remplacer partout « ablation de l'etiquette » et « seule l'etiquette
bouge » par « contraste de conditionnement, etiquette seule contre 119 reponses de la personne,
les deux facteurs etant confondus », et faire du placebo d'etiquette (C3 plus etiquette, ou C2
prive de la seule ligne `Political ideology`) le verrou numero un, avant la comparaison
appariee des minorites.

---

# 1. a44-generateur-nul.md

C'est le rapport qui porte desormais la these. Cinq objections, dont deux bloquantes.

### 1.1 La chute sous permutation n'est pas invariante a la segmentation, et le « 7 pour cent » est un artefact de l'axe choisi. Gravite : bloquante. [VERIFIE]

a44 mesure la chute sous deux segmentations seulement, `S_ideo` (l'ideologie a sept niveaux)
et `S_fin` (ideologie x genre x age). **Les deux contiennent l'ideologie, c'est a dire la
variable meme dont l'agent a etiquette tire ses reponses.** Aucune segmentation sans ideologie
n'a ete essayee. Le preenregistrement ne l'exigeait pas, mais le verdict de la section 7.2 en
depend entierement.

J'ai rejoue la mesure sous neuf segmentations, memes matrices, meme fonction
`a44_commun.permuter_intra`, meme definition d'exactitude, 60 permutations par cellule
(200 pour C2 et C3). Quantite lue : la chute relative de la condition divisee par la chute
relative des memes humains reinterroges, c'est a dire exactement la colonne « part du plancher
humain » de a44 tableau 5.

| segmentation | cellules | `v8` | `v6` | `B1` | `B3 foret` | `composite` | `PMM` |
|---|---|---|---|---|---|---|---|
| **ideologie (`S_ideo`, publiee)** | 7 | **0,072** | 0,234 | 0,175 | 0,131 | 0,642 | 0,597 |
| **ideologie x genre x age (`S_fin`, publiee)** | 42 | **0,054** | 0,230 | 0,117 | 0,081 | 0,637 | 0,573 |
| parti politique | 8 | 0,106 | 0,237 | 0,185 | 0,140 | 0,646 | 0,601 |
| **genre x race x age, sans ideologie** | 38 | **0,266** | 0,235 | 0,229 | 0,188 | 0,695 | 0,624 |
| age | 7 | 0,275 | 0,247 | 0,265 | 0,220 | 0,700 | 0,638 |
| race | 3 | 0,311 | 0,247 | 0,311 | 0,252 | 0,710 | 0,656 |
| genre | 2 | 0,315 | 0,251 | 0,315 | 0,254 | 0,712 | 0,659 |
| education x revenu | 54 | 0,312 | 0,227 | 0,233 | 0,201 | 0,698 | 0,631 |
| aucune (permutation globale) | 1 | 0,319 | 0,256 | 0,331 | 0,267 | 0,714 | 0,664 |

Meme chose sur les 150 personnes du run local :

| segmentation | `C2` | `C3` |
|---|---|---|
| ideologie (publiee) | **0,072** | 0,448 |
| ideologie x genre x age (publiee) | 0,073 | 0,453 |
| genre x race x age, sans ideologie | **0,183** | 0,460 |
| age | 0,191 | 0,469 |
| genre | 0,216 | 0,463 |
| aucune | 0,218 | 0,467 |

**Trois lectures.**

1. **Le classement survit, le chiffre non.** Les conditions riches sont partout entre 0,45 et
   0,71 du plancher humain, les conditions a etiquette partout en dessous. Mais le nombre qui
   porte la phrase de `MODELE-DU-MONDE.md` 10.4, « 7 pour cent du plancher avec l'etiquette »,
   vaut **27 a 32 pour cent** des que la segmentation ne contient pas l'axe politique. Le
   rapport entre les deux camps de conditions passe de 9 pour 1 a **2,6 pour 1**.
2. **Ce n'est pas un effet de finesse.** `S_fin` a 42 cellules et donne 0,054 ; genre x race x
   age a 38 cellules et donne 0,266. A granularite egale, le facteur 5 vient de la presence de
   l'ideologie dans le segment, pas du nombre de personnes par cellule.
3. **Le seuil de verdict ne resiste pas.** a44 section 7.2 classe « gabarit » en dessous de
   15 pour cent du plancher humain. Sous genre x race x age, `v8` (0,266), `C2` (0,183),
   `B1` (0,229) et `B3 foret` (0,188) sortent tous de la classe « gabarit ». Le tableau des
   verdicts change de contenu selon un choix que le rapport ne discute pas.

L'objection qu'un relecteur ecrira est plus dure que le chiffre : **la permutation est faite a
l'interieur de la variable meme que l'invite contient**, donc elle mesure par construction
« ce que l'agent sait au dela de ce qu'on vient de fixer ». Un agent a qui l'on a donne
l'ideologie et dont on permute les personnes a ideologie constante ne peut pas chuter, et cela
n'a pas besoin d'etre mesure pour etre vrai. Le test n'est informatif que sous une
segmentation que l'invite ne contient pas ; c'est la seule version qui repond a la question
« l'agent porte il la personne ».

**Correction proposee.** Publier la grille des neuf segmentations en entier, faire du
segment sans ideologie la mesure principale et de `S_ideo` une lecture secondaire, et ecrire
« 18 a 32 pour cent du plancher humain avec l'etiquette contre 46 a 70 sans » au lieu de
« 7 contre 45 a 64 ».

### 1.2 Le troisieme terme n'a pas de plancher, et son plancher est dans le fichier. Gravite : serieuse. [VERIFIE]

a44 lit la reassignation hongroise comme un second critere qui « confirme le premier dans
l'autre sens » : rapport 4,91 pour `v8`, 3,09 pour C2, 1,00 pour les humains. Le controle
invoque est le rapport humain a 1,001, « ce qui leve la reserve du preenregistrement ».

**Ce controle ne borne rien**, parce que le sur ajustement de l'appariement hongrois se voit
sur le gain absolu et non sur le rapport, et parce qu'il est d'autant plus grand que le signal
vrai est petit. Le rapport publie vaut `(hongrois - permutee) / (vraie - permutee)` ; il
explose mecaniquement quand le denominateur tend vers zero. Le plancher correct est le gain
absolu d'une population **sans aucun signal individuel**, et il est dans le fichier de a44 :

| condition | gain hongrois sur permutee | chute vraie | rapport publie |
|---|---|---|---|
| *`B0 tirage`, aucun signal individuel* | **0,0820** | -0,0011 | *non defini* |
| `agents v8` | **0,0688** | 0,0140 | 4,91 |
| `agents v7` | 0,0916 | 0,0307 | 2,99 |
| `B3 foret` | 0,0787 | 0,0285 | 2,76 |
| `B1 argmax` | 0,1014 | 0,0378 | 2,68 |
| `agents composite` | 0,1539 | 0,1524 | 1,01 |
| humains vague 2 | 0,2764 | 0,2760 | 1,001 |

[VERIFIE, calcul direct sur `a44-permutation.csv`, segmentation `S_ideo`]

Le gain hongrois de `v8`, 0,0688, est **inferieur** a celui d'une population sans aucune
structure individuelle, 0,0820. Le « 4,91 » ne mesure donc pas que « la vraie assignation est
arbitraire chez v8 » : il mesure que 0,0140 est un petit denominateur. a44 range
`B0 tirage` en « sans objet » dans la colonne du rapport, alors que c'est precisement la ligne
qui calibre le terme.

**Correction proposee.** Publier le gain hongrois absolu a cote du rapport, poser
`B0 tirage` comme plancher de sur ajustement, et ecrire « chez v8 le gain de l'appariement
optimal, 0,069, est au niveau du gain obtenu sur une population sans structure, 0,082 » plutot
que « une reassignation arbitraire fait cinq fois mieux que la vraie ».

### 1.3 La chute sous permutation est correlee a 0,91 avec l'exactitude brute. Gravite : serieuse. [VERIFIE]

Sur les treize conditions du perimetre 1 052, la correlation de Pearson entre l'exactitude
vraie et la chute absolue vaut **0,906**, celle de Spearman **0,874**. C'est arithmetiquement
attendu, la chute etant une composante additive de l'exactitude, mais cela mine la phrase que
le dossier repete depuis a1 : « l'exactitude ne voit pas la distorsion ». La quantite qui la
voit est a 82 pour cent de variance partagee avec elle. Les exceptions sont reelles et
interessantes, `B0 mode` a 0,593 d'exactitude et 0,000 de chute, `B3 foret` a 0,634 et 0,029,
mais elles doivent etre nommees comme telles.

**Correction proposee.** Ecrire « la chute sous permutation et l'exactitude brute sont
correlees a 0,91 sur nos treize conditions ; ce qui separe n'est pas leur classement mais les
trois conditions ou elles divergent, `B0 mode`, `B3 foret` et `B1` ».

### 1.4 La quantite de verdict est publiee sans intervalle. Gravite : mineure, et elle tombe. [VERIFIE]

`a44-permutation.csv` porte une bande sur l'exactitude permutee (dispersion des 200
permutations) mais **aucun intervalle sur la chute ni sur la part du plancher humain**, qui
sont les deux chiffres du verdict. Le rapport consacre 1 000 tirages bootstrap a la quantite
preenregistree Q5 dont il ecrit lui meme qu'elle ne sert a rien, et zero a celle qui porte la
these.

Je l'ai construit, 300 tirages bootstrap sur les personnes, le meme tirage applique a la
condition et aux humains :

| condition | part du plancher humain | IC 95 pour cent |
|---|---|---|
| `agents v8` | 0,072 | [0,061 ; 0,082] |
| `agents demographiques (v6)` | 0,235 | [0,224 ; 0,245] |
| `agents composite` | 0,642 | [0,632 ; 0,652] |
| C2 (150) | 0,072 | [0,047 ; 0,095] |
| C3 (150) | 0,448 | [0,406 ; 0,485] |

**L'objection tombe sur le fond** : les intervalles sont etroits et aucune conclusion ne
bouge, y compris sur les 150 personnes. Elle reste sur la forme, parce qu'un relecteur ne
publie pas un verdict sans intervalle et que le calcul coute trois minutes.

**Correction proposee.** Ajouter ces cinq intervalles au tableau 5 et retirer la phrase qui
suggere que la precision de la mesure n'a pas ete etablie.

### 1.5 La fuite de `income` de a17 se propage dans le classement de v6. Gravite : mineure. [VERIFIE]

Un balayage des 149 items x 10 conditions remonte onze items recopies a plus de 95 pour cent
par au moins une condition. Quatre le sont par `v6` seul et sont des faits d'etat civil :
`income` 0,994, `othlang` 1,000, `divorced` 0,997, `posslq/y` 0,995 ; les sept autres sont des
items quasi degeneres que tout le monde reussit (`uscitzn*`, `compuse*`, `usewww*`, `webmob`,
`fucitzn`, `mnthsusa`, `evwork`).

En retirant les onze, la chute sous permutation de `v6` passe de **0,235 a 0,177** du plancher
humain, soit un quart de son signal individuel apparent, tandis que `v8` (0,072 a 0,070) et
`composite` (0,642 a 0,638) ne bougent pas. La ligne « `agents v6` intermediaire, 0,235 » du
tableau 7.2 est donc en partie une recopie de demographies, ce que a17 objection 2.2 avait
signale pour l'exactitude et qui n'a jamais ete corrige.

**Correction proposee.** Publier la ligne `v6` avec et sans les quatre items d'etat civil, ou
adopter enfin la liste de retrait que a17 reclamait.

---

# 2. a38-mode-continu-et-camp.md

C'est le rapport que `MODELE-DU-MONDE.md` 9.1 designe comme « le premier resultat du theme qui
passe une correction declaree d'avance », et 10.4 en fait un des trois piliers de la these.
Trois objections, dont deux bloquantes.

### 2.1 Le facteur d'amplification est une quantite de gabarit, reproduite a 100,0 pour cent par le generateur nul de a44. Gravite : bloquante. [VERIFIE]

`a38_mesures.desirabilite_humaine` et `a28_test1_mode.mesurer` construisent le score de
desirabilite d'une condition, dans un camp et sur un item, en comptant les modalites
(`compte(mat, j, it)`) puis en moyennant le score par la frequence. **C'est une fonctionnelle
de la seule table de contingence (camp, modalite).** Elle est donc exactement invariante sous
permutation des personnes a l'interieur de leur camp, et elle relève mot pour mot du critere de
Yuan que a44 applique au reste du dossier.

J'ai verifie les deux points numeriquement.

- **Reproduction.** Je retrouve les facteurs publies au millieme : `v8` 3,091 (a38 : 3,09),
  `composite` 1,829 (1,83), `B1` 1,209 (1,21), `B2` 0,973 (0,97), humains vague 2 1,025 (1,03).
- **Invariance.** Le facteur de `v8` sous permutation des personnes a l'interieur du camp vaut
  **3,091378**, contre 3,091378 pour la vraie assignation. Ecart nul a la sixieme decimale.
- **Generateur nul.** Le generateur conditionnellement independant de a44, parametre sur les
  marginales de la condition dans le segment ideologique, 30 replicats, reproduit :

| condition | facteur mesure | son generateur nul | bande du nul | part reproduite |
|---|---|---|---|---|
| `agents v8` | 3,091 | **3,092** | [3,074 ; 3,107] | **100,0 %** |
| `agents composite` | 1,829 | **1,830** | [1,807 ; 1,865] | **100,1 %** |
| `B1 argmax` | 1,209 | **1,210** | [1,192 ; 1,231] | **100,1 %** |

a44 section 9.2 dresse la liste des « six chemins » a repasser au nul et **n'y fait pas
figurer a38**, alors que a38 est ecrit sept minutes avant le preenregistrement de a44. Le
resultat que la nuit presente comme le remplacant du theme mort de a25 et a28 est donc, par le
critere que la meme nuit adopte, une description du gabarit de groupe et non une mesure du
rapport aux personnes.

Le meme raisonnement vaut sans recalcul pour l'unanimite de a30 et pour la pente de a37 : le
Gini Simpson d'un camp sur un item et le rapport droite sur gauche par item sont eux aussi des
fonctionnelles de la table (camp, modalite). a44 le reconnait pour a30 (« oui par
construction ») et l'omet pour a37 et a38.

**Correction proposee.** Ajouter a38, a37 et a30 au tableau 9.2 de a44, et ecrire dans
`MODELE-DU-MONDE.md` 10.4 que sur les quatre quantites citees comme piliers, **une seule**, la
chute sous permutation, n'est pas reproduite par un generateur sans structure individuelle.

### 2.2 Les deux conditions qui portent la conclusion causale sont exactement celles qui ne passent pas Holm. Gravite : bloquante. [VERIFIE]

`MODELE-DU-MONDE.md` 9.1 ecrit : « C2 a 1,62 [1,06 ; 2,10] contre C3 sans etiquette a 0,52
[0,20 ; 0,82], intervalles disjoints ; huit tests passent Holm sur la famille de 52 ». La
juxtaposition laisse croire que C2 et C3 sont dans les huit. Le fichier
`a38-corrections.csv`, hypothese K4, dit le contraire :

| condition | `p` brut | **`p` Holm, famille de 52** | `p` BH, famille de 52 | `p` Holm, sous famille de 13 |
|---|---|---|---|---|
| `agents v8` | 0,00005 | **0,0026** | 0,00037 | 0,00065 |
| `agents composite` | 0,00005 | **0,0026** | 0,00037 | 0,00065 |
| `agents entretien (v3)` | 0,00005 | **0,0026** | 0,00037 | 0,00065 |
| `agents enquete` | 0,00005 | **0,0026** | 0,00037 | 0,00065 |
| `agents v6` | 0,00005 | **0,0026** | 0,00037 | 0,00065 |
| `agents v7` | 0,00015 | **0,0068** | 0,00098 | 0,00090 |
| `B0 mode`, `B0 tirage` | 0,00005 | **0,0026** | 0,00037 | 0,00065 |
| `B1 argmax` | 0,0264 | **1,0000** | 0,1375 | 0,1058 |
| **`C3`** | 0,0060 | **0,2640** | 0,0347 | 0,0300 |
| **`C2`** | 0,0298 | **1,0000** | 0,1409 | 0,1058 |

**C2 est a `p` de Holm exactement 1,000 et C3 a 0,264.** Les huit qui passent sont les six
conditions de Stanford plus les deux temoins `B0`, c'est a dire precisement les conditions
qui ne permettent aucune inference causale sur l'etiquette. Aucun test de la difference entre
C2 et C3 n'est publie nulle part ; le rapport se contente de constater que deux intervalles ne
se recouvrent pas, ce qui n'est pas un test.

S'y ajoute que l'intervalle du facteur est le seul intervalle de la difference divise par un
denominateur **fixe** : `facteur = 1 - difference / ecart_humain`, avec `ecart_humain` traite
comme une constante (0,2219 sur 150 personnes, 0,2361 sur 1 052). L'incertitude du plancher
humain, mesuree sur les memes 29 items et les memes 150 personnes, n'est pas propagee.

**Correction proposee.** Ecrire « les huit tests qui passent Holm sont les six conditions de
Stanford et les deux temoins ; C2 et C3, les deux conditions du contraste de conditionnement,
ne passent pas la correction principale (Holm 1,00 et 0,26) et ne passent que Benjamini
Hochberg sur la sous famille », et publier un test apparie de la difference C2 moins C3.

### 2.3 `B2 argmax` ne recoit aucune etiquette, et c'est lui qui porte l'argument. Gravite : serieuse. [VERIFIE]

a38 section 4.4 lecture 2 : « les trois predicteurs statistiques **qui recoivent
l'etiquette** reproduisent l'ecart humain sans l'exagerer. `B2 argmax` a 1,01, `B3 foret` a
1,03, `B1 argmax` a 1,24. **Ils ont la meme information ideologique que les agents.** »
Lecture 3 : « ce n'est pas un effet de predicteur : `B2 argmax` est la methode la plus exacte
du jeu et elle est a 1,01 ».

`analyses/a2_baselines_gss.py`, lignes 185 a 190 : `B2` est un plus proche voisin par
**distance de Hamming sur les seuls items de contexte** ; l'encodeur de demographies n'entre
jamais dans son calcul. `B2` ne recoit ni ideologie, ni parti, ni aucun des onze attributs.
Seuls `B1` et `B3` les recoivent, et `B1`, celui des deux qui reproduit le mieux
l'information de l'invite de `v8`, est a **1,24 avec un intervalle qui exclut 1**.

L'argument « trois predicteurs a etiquette reproduisent l'ecart » se reduit donc a deux, dont
un exagere deja. Et `B2` a 1,01 est l'analogue statistique de C3, pas de C2 : il dit qu'un
predicteur nourri des 119 items ne caricature pas, ce qui est un autre resultat, plus faible.

**Correction proposee.** Ecrire « les deux predicteurs qui recoivent les onze attributs sont a
1,03 et 1,24, ce dernier excluant 1 ; le predicteur nourri des 119 items sans demographie est
a 1,01 ».

### 2.4 Quinze des 29 items viennent d'une seule famille, et C2 n'a pas de robustesse. Gravite : mineure. [VERIFIE]

`a38_commun.items_camp` retient 29 items ; **quinze sont des items `nat*` de depenses
publiques**, quatre des `fe*`, trois de tolerance envers les homosexuels, quatre de `racdif`.
La permutation de signe appariee par item traite ces 29 items comme 29 unites echangeables,
alors qu'ils forment cinq blocs ; c'est l'objection 8 de a17 sur a8, repetee.

Le rapport publie bien une robustesse « sans les items de depense », qui fait tomber
`composite` de 1,83 a 1,41 et `v8` de 3,09 a 2,52 : la conclusion tient. Mais
`a38-camp-robustesse.csv` **ne contient aucune ligne pour C2 ni pour C3**, c'est a dire
precisement les deux conditions dont la difference porte la lecture causale.

**Correction proposee.** Etendre `a38-camp-robustesse.csv` au perimetre 150 et publier
C2 et C3 sans les quinze items de depenses.

---

# 3. a35-llm-comme-imputation.md

### 3.1 La regression a 0,7059 est honnete. Gravite : aucune. [VERIFIE]

Point favorable, a dire parce que c'est le chiffre le plus attaquable du rapport.
`a35_commun.choisir_force` coupe **le pli d'entrainement du pli 0** en deux moities, ajuste
sur l'une, mesure sur l'autre, sur 30 items, et ne regarde jamais un pli de test ; la grille
retenue donne 0,03 contre 0,01 a 0,00007 pres, donc le choix n'est pas critique.
`a35_commun.imputations_regression` ajuste l'encodeur `OneHotEncoder` **sur le seul pli
d'entrainement** (`enc.fit(Z[tr])`) et le modele sur ce meme pli. Il n'y a ni fuite du pli de
test, ni fuite de l'item cible, qui est retire du contexte par construction du bloc. Le 0,7059
est defendable tel quel.

### 3.2 Les methodes statistiques recoivent MOINS d'information que les agents, et c'est conservateur. Gravite : mineure, favorable. [VERIFIE]

Le contexte de `E1` dans le regime facile est `setdiff(149 items, bloc)`, soit **119 items** :
le bloc entier de 30 items est retire, pas seulement l'item cible. Les agents de Stanford
disposent, selon la regle des auteurs citee par a14, de **148 items** plus la transcription
d'entretien pour `composite` et `entretien`. La comparaison est donc defavorable a `E1`
d'environ 29 items, et le fait qu'elle gagne quand meme de 2,19 points renforce la conclusion
de a35. Cela doit etre ecrit, c'est un argument gratuit.

### 3.3 Le regime « severe » donne PLUS de contexte que le regime « facile ». Gravite : serieuse. [VERIFIE]

`a35_familles.imputer_par_famille`, ligne 64 : `ctx = np.setdiff1d(np.arange(m), cols)` ou
`cols` est la famille. Les six familles comptent 17, 13, 11, 7, 5 et 5 items
[VERIFIE, `a2_baselines_gss.FAMILLES`]. Le contexte du regime severe compte donc **132 a 144
items**, alors que celui du regime facile en compte **119**. Le regime dit severe est plus
riche de 13 a 25 items que le regime dit facile.

Consequence directe sur la ligne la plus citee de a35 et sur `a41-cout-du-retrait.csv` :
« la regression perd 6,6 points en passant au regime severe, deux fois ce que `B2` perdait »
melange deux changements de signe oppose, le retrait de 5 a 17 items cousins et l'ajout de 13
a 25 items aleatoires. Le cout propre du retrait de famille est **plus grand** que 6,6 points,
et l'exactitude severe de `E1`, 0,6649, est optimiste.

Cela ne renverse aucune conclusion de a41, qui va deja dans ce sens, mais cela rend la phrase
de a35 « sur une question reellement nouvelle, l'agent de langage domine l'imputation par
regression sur l'exactitude ET sur la dispersion » encore moins tenable qu'elle ne l'est deja,
et cela invalide la comparaison facile contre severe comme mesure du cout de l'ablation.

**Correction proposee.** Refaire le regime severe a taille de contexte egale (retirer la
famille **et** completer a 119 items par un tirage aleatoire dans le reste), ou ecrire que
« le cout mesure de 6,6 points est une borne basse, le contexte severe comptant 13 a 25 items
de plus que le contexte facile ».

### 3.4 L'ecart entre argmax et tirage vaut a lui seul l'effet attribue a l'etiquette, et il n'a jamais ete mesure sur les agents. Gravite : serieuse. [VERIFIE pour les statistiques, PROBABLE pour la portee]

`a35-couples-regime.csv`, famille primaire H1 : passer de l'argmax au tirage, **a modele
constant**, fait tomber le ratio inter de `B1` de **1,477** [1,344 ; 1,614] et celui de `B2`
de 0,977, et remonte le ratio intra de 0,363 et 0,427. `B1 argmax` a un ratio inter de 2,673 ;
`B1 tirage` tombe donc autour de 1,20.

Or **toutes** les conditions a modele de langage du dossier sont evaluees en argmax du
tenseur de lettres [VERIFIE, controle de a23 section 0, « controle argmax du tenseur contre
trace, coincide sur toutes les cellules »], et les traces de C2 et C3 contiennent la
distribution complete sur les 40 premieres lettres. **Aucun rapport ne construit un
`C2 tirage`.** Le gonflement de 0,73 a 8,16 attribue a l'etiquette, l'ecrasement de 0,681 a
0,365, le facteur d'amplification de 1,62, l'unanimite de C2 sur 31 items sur 79 : tous
comparent une simulation par le mode a une population humaine echantillonnee, dans un dossier
dont la these centrale est precisément que « le langage est une methode par l'esperance ». Un
relecteur demandera si le mode de decodage, dont l'effet mesure sur les statistiques est du
meme ordre que l'effet attribue a l'etiquette, ne produit pas a lui seul la caricature. Le
test coute zero appel de modele.

**Correction proposee.** Produire `C2 tirage` et `C3 tirage` par echantillonnage dans les
distributions deja stockees dans `data/traces/`, et republier le ratio inter, le facteur
d'amplification et le compte d'unanimite dans les deux regimes de decodage.

---

# 4. a41-regime-severe.md

### 4.1 La premiere comparaison appariee n'est pas appariee, et la penalite est prise sur la mauvaise condition. Gravite : serieuse. [VERIFIE pour l'attribution, PROBABLE pour l'ampleur]

a41 retranche 3,93 points d'exactitude brute a `agents composite` a partir du couple 0,82
contre 0,77 publie par Stanford. Ce couple est mesure sur les **Survey Agents**
[CONFIRME, a14 section 3.4]. `agents composite` recoit, en plus du questionnaire, la
transcription d'entretien : le retrait du bloc GSS lui coute donc necessairement moins qu'a un
agent dont le questionnaire est toute l'entree. La penalite transposee est appliquee a la
condition pour laquelle elle est la plus grande possible, et le rapport ne le dit pas alors
qu'il applique la meme soustraction a `agents enquete`, ou elle est legitime.

C'est le sens qui affaiblit la conclusion negative de a41 : si la penalite propre de
`composite` est inferieure a 1,27 point, l'avantage de 1,27 point survit.

**Correction proposee.** Appliquer la penalite de 3,93 points a `agents enquete` seulement,
et donner pour `composite` un encadrement (0 point si l'entretien absorbe tout, 3,93 s'il
n'absorbe rien) plutot qu'une valeur.

### 4.2 La seconde comparaison appariee change de modele en meme temps que de regime. Gravite : serieuse. [VERIFIE]

C3F est un modele ouvert de 4 milliards de parametres, sur 60 personnes des plis 0 et 1, dont
le frere sans ablation, C3, fait deja **0,6195** contre 0,7304 pour `E1` dans le regime facile
sur les memes 58 items. Un modele qui perd de onze points avant l'ablation perd de treize
apres : la mesure directe ne dit rien de `agents composite` et le rapport le reconnait en une
ligne, mais `MODELE-DU-MONDE.md` 9.3 la cite comme « mesure directe ETABLIE » a cote de la
transposition, et la phrase de synthese « son avance en exactitude ne survit pas a une
comparaison appariee » s'appuie sur les deux ensemble.

Le cout du retrait est en revanche bien symetrique et bien mesure : moins 6,24 points pour
C3F, moins 6,55 pour `E1` [VERIFIE, `a41-c3f-60-personnes.csv` et `a41-cout-du-retrait.csv`].
C'est le seul element de la section qui soit une comparaison appariee au sens strict, et c'est
lui qu'il faut mettre en avant.

**Correction proposee.** Ecrire « la seule quantite appariee que nous mesurons est le cout du
retrait de famille, moins 6,2 points pour notre agent contre moins 6,6 pour la regression :
l'ablation mord autant des deux cotes, et le niveau de C3F ne se transpose pas a Stanford ».

### 4.3 Le rappel des minorites du regime severe repose sur un instrument que a42 detruit douze minutes plus tard. Gravite : serieuse. [VERIFIE]

a41 place au rang de resultat qui survit : « sur les 450 cellules du tercile **non
deductible** de a34 [...] 28,2 pour cent contre 13,8 ». a42 section 5, ecrit douze minutes
apres a41, montre qu'une partition placebo de neuf groupes tires au hasard reproduit le meme
gradient a 0,019 en mediane, et conclut que le dispositif de terciles de a34 est invalide
comme instrument. `MODELE-DU-MONDE.md` 10.1 retire la formulation en « rarete deductible » de
9.3 et 9.6, mais **le corps de a41 n'est pas corrige** et la seule quantite qui reste debout
dans son resume d'une ligne est indexee sur cet instrument.

**Correction proposee.** Ajouter un errata en tete de a41 renvoyant a a42 section 5, et
remplacer le tercile non deductible par la partition « rarete stable en vague 2 », qui est la
seule que a42 conserve.

---

# 5. a42-plancher-de-bruit.md

### 5.1 La circularite est declaree, l'asymetrie de frequence ne l'est pas. Gravite : serieuse. [VERIFIE]

Le preenregistrement declare d'avance que `humains vague 2` vaut 1,000 sur les stables et
0,000 sur les instables par construction, et que le plancher humain y est degenere. C'est
correct et honnete.

Ce qui n'est pas declare est mesure dans le meme fichier : **le plancher de segment n'est pas
le meme dans les deux classes**, 0,1094 sur les raretes stables contre 0,0728 sur les
instables [VERIFIE, `a42-stabilite.csv`]. Une rarete stable est donc, dans le segment de la
personne, **une fois et demie plus frequente** qu'une rarete instable. La partition « vraie
heterogeneite contre bruit » est donc aussi, pour moitie, une partition de frequence, c'est a
dire exactement le defaut que la section 5 du meme rapport reproche aux terciles de a34.

L'exces sur plancher corrige cela **de facon additive**, sur une quantite bornee entre 0 et 1
dont la relation au taux de base n'est pas lineaire. Le test H3, « l'avantage est plus grand
sur les stables que sur les instables », plus 0,1739 pour `composite`, n'est donc pas protege
par la correction employee.

Un element defend le rapport et doit etre ecrit avec l'objection : l'agent n'a aucun acces a
la vague 2, et il ose 3 817 raretes sur 3 130 cellules stables contre 1 603 sur 2 579 cellules
instables, soit 1,22 contre 0,62 par cellule. Cette asymetrie de comportement est un fait,
pas un artefact de selection.

**Correction proposee.** Refaire H3 en appariant les cellules stables et instables sur le
plancher de segment (par exemple par strates de frequence), et publier l'exces en rapport de
cotes plutot qu'en difference.

### 5.2 Le comparateur declare est le plus faible du jeu, et le rapport le sait. Gravite : mineure. [VERIFIE par lecture]

`B1 argmax` est le comparateur declare, au motif que c'est l'adversaire de von der Heyde. Le
rapport ecrit lui meme, en « ce que je n'ai pas pu verifier » point 9, qu'« avec `PMM k=10`
comme comparateur, quatre des six conditions de Stanford perdraient leur avantage sur les
raretes stables ». `MODELE-DU-MONDE.md` 10.4 ecrit pourtant « deux sur cinq contre une sur
douze pour la regression et une sur quatre pour l'appariement sur moyenne predite », ce qui
est exact mais met le comparateur faible en premier.

**Correction proposee.** Mettre `PMM` en comparateur principal dans la phrase de these, comme
la section 10.5 verrou cinq le prevoit deja, et nommer les quatre conditions qui perdent.

---

# 6. a29, a31, a33, a34 : ce que le nul de a44 laisse debout

### 6.1 a31 : le rapport groupe sur personne est publie sans son nul dans le rapport qui le porte. Gravite : serieuse. [VERIFIE par a44]

a44 section 6 montre que le 7,37 de `v8`, cite dans `MODELE-DU-MONDE.md` section 7 comme la
preuve que « le groupe pese jusqu'a huit fois plus », est reproduit a **7,32** par le
generateur nul, ses deux composantes a 99 et 98 pour cent, et le rappel des rares a 91 pour
cent. Le rapport a31 lui meme n'a pas ete assorti d'un errata, et son resume d'une ligne, qui
oppose « 0,56 chez les humains » a « 8,18 pour la foret et 7,37 pour v8 », se lit encore comme
une mesure du rapport aux personnes.

Le point favorable, a ecrire aussi : chez les humains et chez les conditions riches le nul
echoue completement du cote de la personne (0,241 contre 0,001 ; 0,212 contre 0,047), donc la
moitie « rarete de personne » de a31 tient.

**Correction proposee.** Errata en tete de a31 : « les lifts de segment et le rapport groupe
sur personne des conditions a etiquette sont des quantites de gabarit, a44 section 6 ; seul le
lift de personne resiste au generateur nul ».

### 6.2 a29 : « ablation propre » est faux, et c'est ecrit dans la section des limites. Gravite : serieuse. [VERIFIE]

a29 section 8 point 1 : « C2 contre C3 est une ablation propre, mais sur un seul modele ». Le
reste de la phrase enumere les vraies limites (un run, 150 personnes, formulation d'invite) et
laisse passer la seule qui compte, voir section 0 de ce rapport. Le renversement que a29
publie, C2 a 0,194 de correlation par personne contre C3 a 0,410, est le meme contraste de
conditionnement que partout ailleurs.

**Correction proposee.** Remplacer « une ablation propre » par « un contraste de
conditionnement dont les deux facteurs sont confondus ».

### 6.3 a34 : la partie qui reste vraie n'est pas celle que le resume met en avant. Gravite : mineure. [VERIFIE par a42]

a42 section 5 invalide les terciles de deductibilite ; a34 conserve ses rappels mais perd son
interpretation, ce que `MODELE-DU-MONDE.md` 10.1 acte. Le corps de a34 n'est pas corrige et
son resume d'une ligne, entierement construit sur le tercile non deductible, reste en place.
a34 declare par ailleurs, en section 0.1, ne pas revendiquer le preenregistrement.

**Correction proposee.** Errata en tete de a34 renvoyant a a42 section 5.

### 6.4 a33 : la seule condition ou l'ablation de contexte est propre, et personne ne s'en sert. Gravite : mineure, favorable. [VERIFIE]

C3 contre C3F est le seul contraste du dossier ou une seule chose change : le meme modele, la
meme personne, la meme question, la meme invite, moins la famille thematique. Il donne moins
6,24 points d'exactitude et une baisse de la rarete de groupe. C'est la seule ablation propre
que le dossier possede, et elle porte sur le contexte, pas sur l'etiquette. Elle merite d'etre
nommee comme telle a la place du couple C2 contre C3.

---

# 7. a30 et a37 : l'unanimite et la loi de consensus

### 7.1 Les pentes de a37 sont calculees sur des jeux d'items differents selon la condition. Gravite : serieuse. [VERIFIE]

`a37-agents-gss.csv` et `a37-agents-gss-150.csv`, colonne `n_items_perdus_log` : le rapport
droite sur gauche devient infini des qu'un camp est unanime sur un item, et l'item sort de la
regression. Les pentes ne sont donc pas calculees sur le meme support :

| condition | items retenus sur 79 | pente publiee |
|---|---|---|
| humains vague 1 | **79** | -2,22 |
| `agents composite` | 79 | -3,80 |
| `agents entretien (v3)` | 73 | -5,37 |
| **`agents v8`** | **63** | **-12,41** |
| `B3 foret` | 45 | -4,12 |
| **C2 (150 personnes)** | **46** | **-2,73** |
| C3 (150 personnes) | 71 | -1,89 |

a37 le declare en section 3 (lignes 382, 412, 428) et ecrit « le chiffre a lire est le
nombre d'items perdus ». Mais `MODELE-DU-MONDE.md` 10.4 reprend « deforme la loi humaine de
consensus de moins 2,2 a moins 12,4 » **sans le denominateur**, c'est a dire exactement la
faute que a17 objection 2 avait qualifiee de bloquante sur a1 (0,07 point a 150 items contre
facteur 13,5 a 169 items). Le meme fichier donne d'ailleurs une seconde estimation,
`pente_sur_derive_humaine`, qui vaut **-7,57** pour `v8` au lieu de -12,41 : le choix de la
variable explicative deplace le chiffre de 40 pour cent et il n'est pas discute dans la
synthese.

Enfin, la comparaison C2 (46 items, 150 personnes) contre `v8` (63 items, 1 052 personnes)
n'est pas lisible : la troncature est plus forte la ou l'echantillon est plus petit, et
l'unanimite est mecaniquement plus facile sur 63 personnes de gauche que sur 417.

**Correction proposee.** Ecrire dans toute synthese « pente -2,22 sur 79 items chez les
humains, -12,41 sur les 63 items ou elle est definie chez v8, -7,57 si la derive humaine sert
d'abscisse », et ne jamais comparer un compte d'unanimite entre les perimetres 150 et 1 052.

### 7.2 L'unanimite est une quantite de gabarit et un artefact d'argmax. Gravite : serieuse. [VERIFIE pour le premier point, PROBABLE pour le second]

Le Gini Simpson d'un camp sur un item ne depend que de la table (camp, modalite) : il est
exactement invariant sous permutation intra camp et reproduit par le generateur nul de a44,
qui l'admet pour a30 (« oui par construction : une marginale de segment degeneree donne un nul
degenere »). Ce point est donc acquis mais n'est pas porte dans a30.

S'y ajoute le regime de decodage : la population de C2 est un argmax sur un prompt dont le
seul contenu variable est onze attributs, et `a35-couples-regime.csv` montre que le passage a
l'echantillonnage remonte le ratio intra de 0,36 a 0,43 selon les familles. L'unanimite de C2
sur 23 questions n'a jamais ete mesuree en regime de tirage, alors que les traces le
permettent.

**Correction proposee.** Ecrire « le camp de gauche simule par argmax est unanime sur 23
questions ; la mesure en regime de tirage sur les memes traces reste a faire », et signaler
que la quantite est une quantite de marginales.

---

# 8. a39-tranches-de-peng.md

### 8.1 Le seul couple presente comme une ablation n'en est pas une, et c'est le pivot du rapport. Gravite : serieuse. [VERIFIE]

a39 fait reposer sa conclusion la plus fine sur « le seul couple ou le modele, les personnes,
les questions et les traces sont constants et ou seule l'etiquette bouge, C2 contre C3 »
(lignes 47, 353, 448). Voir section 0. Le resultat lui meme, moins 0,0067 [moins 0,0167 ;
0,0035] sur le milieu ordinal, est un **non rejet** : il est presente comme la reproduction a
la lettre du resultat de Peng, alors qu'il s'agit d'un intervalle qui contient zero, sur 150
personnes, sans calcul de puissance. Un relecteur ecrira qu'un non rejet sur 150 personnes ne
« reproduit » rien.

**Correction proposee.** Ecrire « sur notre contraste de conditionnement, l'ecart sur le
milieu ordinal n'est pas decidable, IC [moins 0,017 ; 0,004] sur 150 personnes ; nous ne
pouvons ni confirmer ni infirmer l'egalite de Peng », et publier la taille d'effet detectable
a 80 pour cent de puissance.

### 8.2 Le tirage uniforme qui bat v8 sur la queue est une comparaison a precision ignoree. Gravite : mineure. [PROBABLE]

Le chiffre « le hasard bat l'agent a etiquette de 12,6 points sur la queue » (0,186 contre
0,060) est le plus citable du rapport et il est juste. Ce qu'il faut ecrire a cote est que le
tirage uniforme paie ce rappel par une precision effondree, et que le F1 n'est pas publie pour
cette tranche : un relecteur y verra le compromis rappel precision qu'on lui presente comme
une victoire du hasard.

**Correction proposee.** Publier la precision et le F1 du tirage uniforme sur la tranche
basse a cote de son rappel.

---

# 9. a43-r2-demoyenne.md

### 9.1 Le rapport dit le vrai sur le conditionnement, et le dossier ne l'ecoute pas. Gravite : serieuse, et elle porte contre les autres rapports. [VERIFIE]

a43 section 1 est le seul endroit du dossier qui range explicitement C3, `B2`, `PMM` et `IM`
dans « 119 reponses de la personne, non, ils voient la personne », et `agents composite` dans
« et c'est pire ». Il ecrit meme que ce point « commande toute la lecture » et « n'etait pas
dans le preenregistrement ». Le chiffre « 83 pour cent de signal perdu pour C2 contre 14 pour
C3 », repris dans `MODELE-DU-MONDE.md` 10.4 comme mesure de l'effet de l'etiquette, viole donc
l'avertissement de son propre rapport source.

**Correction proposee.** Dans 10.4, remplacer « 83 contre 14 pour cent de signal perdu au
retrait du segment » par « 83 pour cent pour un agent qui n'a que l'etiquette, 76 et 77 pour
une regression et une foret sur les memes attributs, 14 pour un agent qui a les 119 reponses
de la personne : le remplacement suit le conditionnement, pas le moteur ».

### 9.2 L'adversaire trivial de a43 n'a pas ete porte dans les tableaux des autres rapports. Gravite : mineure. [VERIFIE par lecture]

a43 section 5 etablit qu'une moyenne de segment calculee sans la personne obtient r 0,534 par
personne et n'est battue par aucune des quinze methodes de facon retenue par Holm. C'est
l'adversaire le moins cher du dossier et il n'apparait ni dans a35, ni dans a41, ni dans a44.
Le verrou 5 de la section 10.5 le prevoit ; tant qu'il n'est pas fait, le tableau des
imputations est incomplet du cote le plus embarrassant.

---

# 10. i1-qui-bouge-humains.md

### 10.1 L'artefact hors pli que le rapport isole sur T1 contamine tous les autres predicteurs. Gravite : serieuse. [PROBABLE]

i1 section 4.3 explique correctement pourquoi le temoin de segment a une chute **negative**,
moins 0,0385 : son score varie a l'interieur d'un segment uniquement parce qu'il est estime
hors pli, et cette variation est negativement correlee a la cible par construction. J'ai
verifie le mecanisme dans `i1_previsibilite.scores_hors_pli`, lignes 126 a 133 : `t1` est la
moyenne de `y` sur les personnes du **pli d'entrainement** du meme segment, donc la personne
est exclue de son propre estimateur.

Ce que le rapport ne tire pas : **la meme anticorrelation existe dans la composante de groupe
de tous les autres predicteurs**, qui sont eux aussi ajustes hors pli et encodent des moyennes
de segment (`L1`, `L2` par les indicatrices demographiques, `F` par les splits de la foret).
L'ampleur mesuree sur T1, 0,0385, vaut **28 pour cent de la chute de la foret (0,1368) et 43
pour cent de celle du predicteur primaire (0,0905)**. Tant que cette part n'est pas bornee, la
phrase « cette avance ne vient pas du groupe » est une conclusion tiree d'une mesure dont on
sait qu'elle est biaisee vers le haut d'une quantite du meme ordre.

**Correction proposee.** Refaire la chute de `L2` et de `F` avec des moyennes de segment
estimees en laissant la personne dehors mais son pli dedans, ou soustraire la chute de T1
comme correctif de premier ordre, et publier les deux versions.

### 10.2 « Integralement une consequence comptable » est un non rejet sur 50 replicats. Gravite : mineure. [VERIFIE]

`i1-nul-remelange.csv` : le nul qui conserve la derive et le taux de changement donne un exces
monotone de **11,07 points, ecart type 0,50 sur 50 replicats**, contre 10,4 mesures. L'ecart
vaut 1,35 ecart type ; c'est un non rejet, pas une egalite demontree, et la formule
« integralement une consequence comptable » depasse la mesure. Le rapport a raison sur le
fond, et il devrait ecrire « indistinguable du nul, ecart 0,7 point pour un ecart type de
0,5 ».

### 10.3 Ce qui est solide, et qu'il faut garder. [VERIFIE]

Le controle de chaine reproduit les deux denominateurs de a12 a la quatrieme decimale, la
colonne « items retenus, Holm » correspond bien a la colonne `n_items_holm_normale_retenus`
des fichiers (111 et 97), l'ecart E4 declare honnêtement que le preenregistrement demandait
une correction que 200 permutations interdisaient, et le temoin `T0b` donne exactement 0,5000
et 0,0000, ce qui valide l'implementation de l'AUC. Sur ces points le rapport est au dessus du
reste du dossier.

---

# 11. i3-detecteur.md

### 11.1 La bande humaine n'est pas une constante, et le rapport la presente comme un fait humain. Gravite : bloquante pour la portee, serieuse pour le rapport. [VERIFIE]

i3 fonde tout son dispositif sur deux « faits humains » : deficit de patrons de moins 6,9 pour
cent et exces de correlation de 0,042, avec `s_0` de 0,0029 et 0,00086. Sa phrase centrale,
« de vraies personnes ne sont pas non plus libres », s'en deduit.

Les fichiers de i3b, produits deux heures plus tard, mesurent ces memes quantites sur
Twin-2K-500 **a effectif egal** :

| | GSS, 1 052 personnes | Twin, 1 052 personnes | rapport | ecart en `s_0` de i3 |
|---|---|---|---|---|
| A, deficit de patrons | -0,0684 | **-0,0278** | 2,5 | **14** |
| B, exces de correlation | +0,0422 | **+0,0227** | 1,9 | **23** |
| C, concentration | +0,0272 | **+0,0115** | 2,4 | **25** |

[VERIFIE, `i3b-twin-reference.csv` et `i3-reference-humaine.csv`]

Autrement dit, une population **entierement humaine** issue d'un autre questionnaire se
trouve a 14 a 25 ecarts types de la reference de i3, c'est a dire tres au dela du seuil
bilateral de 3,22. Le detecteur, cale comme i3 le cale, classerait 100 pour cent d'humains
reels comme synthetiques. i3b l'ecrit (« la bande est une forme, pas une valeur ») ; **i3 ne
le porte pas**, et sa section 11 point 3 se contente de dire que Twin n'a pas ete teste.

La meme instabilite existe en taille : sur le GSS, A vaut -0,037 a N = 300, -0,050 a 500,
-0,060 a 750 et -0,068 a 1 052 [VERIFIE, `i3b-reference-par-taille.csv`]. Les trois
statistiques du detecteur ne sont pas des invariants, elles sont des fonctions de l'effectif
et du questionnaire.

**Correction proposee.** Ajouter en tete de i3 : « les trois statistiques varient d'un facteur
1,9 a 2,5 entre le GSS et Twin a effectif egal, et de 1,8 entre N = 300 et N = 1 052 sur le
GSS ; aucun seuil de ce rapport ne se transporte, la reference doit etre recalculee sur la
population et l'effectif audites ».

### 11.2 Le point 10 attribue a `v8` un chiffre qui est celui de C2. Gravite : mineure. [VERIFIE]

i3 section 11 point 10 : « les deux vont dans le meme sens pour v8, facteur 1,76 ici contre
1,62 en a38 ». Le facteur de a38 pour `v8` vaut **3,17** au perimetre 150 et **3,09** au
perimetre 1 052 ; 1,62 est celui de **C2**. La phrase compare la polarisation de `v8` mesuree
par i3 a l'amplification de C2 mesuree par a38.

**Correction proposee.** Ecrire « 1,76 a 50 pour cent de contamination par v8, contre un
facteur d'amplification de 3,09 pour une population de v8 pure en a38 ; les deux quantites ne
sont pas comparables directement ».

### 11.3 Ce qui est solide. [VERIFIE par lecture]

Les cinq ecarts sont declares, dont E1 qui mesure et publie le biais de 13,3 pour cent du
bootstrap avec remise sur l'exces de correlation, et qui signale que **a44 porte le meme
defaut sur Q5 sans l'ecrire**, ce que a44 section 11 point 8 confirme a demi. Trois des sept
predictions sont fausses ou a moitie fausses et sont publiees comme telles. Le point 2 de la
section 11, « une seule population humaine sert de fond, de reference et de source des
marginales, donc tous les `tau*` sont optimistes », est la bonne objection et elle est deja
ecrite.

---

# 12. a25 et a28 : les rapports morts qui n'ont pas d'errata

### 12.1 Le resume d'une ligne de a25 et de a28 affirme encore une these que a38 a tuee. Gravite : serieuse. [VERIFIE par lecture]

`MODELE-DU-MONDE.md` 9.1 et `ARBITRAGE.md` declarent tombee la phrase « la simulation devie la
ou les humains se surveillent ». Les deux rapports sources ne portent aucun errata : a25
ouvre encore sur « le motif tient » avec la reserve qu'il n'est distinguable de zero que pour
C2, et a28 ouvre encore sur son test 1 au rang 1. Un relecteur qui ouvre `resultats/` dans
l'ordre alphabetique lit d'abord la these morte.

Le second point, plus lourd, est que le seul cas ou a25 trouvait un effet distinguable etait
`C2`, moins 0,207 [moins 0,331 ; moins 0,092], c'est a dire une condition sur treize, ce qui
est exactement ce qu'on attend d'une famille de treize tests non corriges ; a28 l'a d'ailleurs
etabli en montrant que le meilleur `p` ajuste vaut 0,144.

**Correction proposee.** Un errata de trois lignes en tete de a25 et de a28, renvoyant a a38
sections 2 et 3.

---

# 13. Les preenregistrements : ce qui est verifiable et ce qui ne l'est pas

### 13.1 Aucun preenregistrement n'est sous suivi de version ni depose. Gravite : bloquante pour la revendication de protocole. [VERIFIE]

Les cinq preenregistrements citent un depot, `d536169dc5361c38edcd723d48816e2ddd06dc4f`.
`git ls-files` execute dans `Projets/popsim` renvoie **zero fichier** : le repertoire entier,
`analyses/` et `resultats/` compris, est non suivi (`git status` : `?? Projets/popsim/analyses/`,
`?? Projets/popsim/resultats/`). Le commit cite est un commit du depot parent qui **ne contient
aucun des fichiers preenregistres**. Aucun depot OSF n'existe, alors que
`PROTOCOLES-DE-RECHERCHE.md` section 2 point 1 en fait la premiere regle du protocole du
projet et que la section 4 point 3 exige « la page est deposee sur OSF, horodatee, avant que
le premier script tourne ».

La seule preuve d'anteriorite disponible est donc l'horodatage du systeme de fichiers, sur un
repertoire place dans un Bureau synchronise par iCloud, et cet horodatage ne survit ni a une
copie, ni a une restauration, ni a une archive. Aucun tiers ne peut le verifier.

**Ce que l'horodatage dit, tel quel** [VERIFIE, `stat -f %Sm`] :

| preenregistrement | ecrit | premier script de la serie | marge |
|---|---|---|---|
| a43 | 15:43:10 | `a43_commun.py` 15:45:20 | 2 min 10 |
| a42 | 15:43:56 | `a42_commun.py` 15:45:36 | 1 min 40 |
| a44 | 15:48:33 | `a44_mesures.py` 15:57:07 | 8 min 34 |
| i1 | 18:32:46 | `i1_commun.py` 18:38:52 | 6 min 06 |
| i3 | 19:11:32 | `i3_commun.py` 19:19:03 | 7 min 31 |

L'ordre est correct dans les cinq cas et aucun preenregistrement n'a ete touche apres son
premier script. C'est le maximum que le dispositif actuel puisse etablir.

**Correction proposee.** Deposer les cinq textes sur OSF avec leur date reelle, ou a defaut
committer `resultats/` et signer les commits ; sans cela, la phrase « preenregistre » ne doit
pas figurer dans un preprint.

### 13.2 Les ecarts declares sont complets, avec une exception. Gravite : mineure. [VERIFIE]

J'ai compare les cinq preenregistrements a leurs rapports quantite par quantite.

- **a44** : trois ecarts declares (E1 deux conditions ajoutees, E2 Q6 et Q7 a 50 replicats,
  E3 complement par finesse), plus l'abandon du bootstrap de Q3, motive. Le classement de la
  section 7.2 est explicitement signale comme post hoc, et les seuils de 15 et 40 pour cent
  aussi. **Un ecart n'est pas declare** : le preenregistrement annonce en section 5 un
  intervalle bootstrap sur la distance pour les sept quantites, et la section 6 ne prevoit
  aucun intervalle sur la chute sous permutation ; le rapport publie la chute sans intervalle
  alors qu'elle devient la quantite du verdict. C'est un ecart par omission, il n'est pas dans
  le tableau des trois.
- **a42** : les ecarts sont declares, y compris le fait que la division de recensement compte
  dix niveaux et non neuf, ce qui est une erreur du preenregistrement publiee comme telle.
- **a43** : le rapport declare que le point qui commande toute la lecture, les trois
  conditionnements, n'etait pas dans le preenregistrement.
- **i1** : quatre ecarts declares, dont E4 qui reconnait que la correction demandee etait
  impossible avec 200 permutations, et le controle 2 declare vide.
- **i3** : cinq ecarts declares, dont E1 qui publie le biais du bootstrap et le compare a celui
  de a44.

Sur ce point le dossier est en avance sur la litterature qu'il critique. La seule chose qui
manque est l'exterieur.

---

# 14. Contradictions entre rapports, avec la ligne a corriger

| # | contradiction | ligne a corriger | statut |
|---|---|---|---|
| D1 | a35 section 11.5 et a43 section 1 disent que le contraste C2 contre C3 est un contraste de conditionnement ; a29 8.1, a38 4.4, a39 (lignes 47, 353, 448), a42 (ligne 72), a44 (lignes 672, 783), `ARBITRAGE` point 2 et `MODELE` 10.4 l'appellent une ablation de l'etiquette | `ARBITRAGE.md` point 2 ; `MODELE-DU-MONDE.md` 10.4, phrase « les memes questions donnent 7 pour cent avec l'etiquette et 45 sans » ; a44 7.2 et 10 point 3 | [VERIFIE] |
| D2 | a44 section 9.2 recense les quantites de gabarit et omet a38, alors que a38 precede a44 de sept minutes ; le facteur d'amplification est reproduit a 100,0 pour cent par le nul | a44 section 9.2, tableau des six chemins ; `MODELE` 10.4, phrase « un facteur d'amplification de 1,62 contre 0,52 » | [VERIFIE] |
| D3 | `MODELE` 9.1 juxtapose « C2 a 1,62 contre C3 a 0,52 » et « huit tests passent Holm » ; C2 est a `p` de Holm 1,000 et C3 a 0,264 | `MODELE-DU-MONDE.md` 9.1, derniere phrase du paragraphe remplacant | [VERIFIE] |
| D4 | a38 4.4 lecture 2 dit que `B2 argmax` recoit l'etiquette ; `a2_baselines_gss.py` lignes 187 a 190 montre qu'il ne recoit que les items de contexte | a38 section 4.4, lectures 2 et 3 | [VERIFIE] |
| D5 | a35 « la regression perd 6,6 points au regime severe » compare un contexte de 119 items a un contexte de 132 a 144 items | a35 section 6 ; `a41-cout-du-retrait.csv` et son commentaire | [VERIFIE] |
| D6 | a41 fait du tercile non deductible de a34 sa quantite qui survit ; a42 section 5, ecrit douze minutes plus tard, invalide l'instrument | a41, resume d'une ligne, phrase « sur les 450 cellules du tercile non deductible » | [VERIFIE] |
| D7 | a31 publie le rapport groupe sur personne comme preuve du poids du groupe ; a44 section 6 le reproduit a 99 pour cent avec un generateur sans structure | a31, resume d'une ligne ; `MODELE` section 7, phrase « le groupe pese jusqu'a huit fois plus » | [VERIFIE] |
| D8 | a25 et a28 affirment encore la these « la simulation devie la ou les humains se surveillent » que a38 et `MODELE` 9.1 declarent tombee | a25 et a28, resumes d'une ligne, sans errata | [VERIFIE] |
| D9 | `MODELE` 10.4 cite « moins 2,2 a moins 12,4 » sans dire que les deux pentes sont calculees sur 79 et 63 items, et que la seconde vaut moins 7,57 si l'abscisse est la derive humaine | `MODELE-DU-MONDE.md` 10.4 ; a37 le declare, la synthese non | [VERIFIE] |
| D10 | i3 section 11 point 10 attribue a `v8` le facteur 1,62 de a38, qui est celui de C2 | i3, section 11, point 10 | [VERIFIE] |
| D11 | a44 declare `S_fin` inutilisable sur le perimetre 150 (64,3 pour cent de repli) pour le generateur nul, mais publie et lit la ligne de permutation `S_fin` de C2 et C3 dans le meme rapport ; la permutation n'emploie pas le nul, donc la ligne est valide, et le rapport ne le precise pas | a44 section 1 point 6, derniere phrase ; a44 section 5.2, dernier paragraphe | [VERIFIE, sans consequence sur les chiffres] |
| D12 | i3 presente la bande humaine comme un fait humain ; i3b la mesure a un facteur 1,9 a 2,5 pres sur Twin a effectif egal | i3, reponse en une ligne, phrase « de vraies personnes ne sont pas non plus libres » | [VERIFIE] |

---

# 15. Les dix objections les plus graves

| rang | objection | rapport | gravite | statut | correction en une phrase |
|---|---|---|---|---|---|
| 1 | C2 et C3 n'echangent pas l'etiquette, ils echangent toute leur entree : onze attributs sans la personne contre 119 reponses de la personne sans etiquette ; le dossier appelle « ablation » un contraste a deux facteurs confondus, dans huit textes, et en fait sa revendication de nouveaute numero un | a29, a38, a39, a42, a44, ARBITRAGE, MODELE | bloquante | [VERIFIE] | Renommer partout en contraste de conditionnement et faire du placebo d'etiquette le verrou numero un |
| 2 | La chute sous permutation n'est mesuree qu'a l'interieur de la variable que l'invite contient ; sous une segmentation sans ideologie de meme finesse, `v8` passe de 0,072 a 0,266 du plancher humain et C2 de 0,072 a 0,183, et quatre conditions sortent de la classe « gabarit » | a44 sections 5.2 et 7.2 | bloquante | [VERIFIE] | Publier la grille des neuf segmentations et prendre le segment sans ideologie comme mesure principale |
| 3 | Le facteur d'amplification de a38, pilier de la these en `MODELE` 10.4, est une fonctionnelle de la table camp par modalite : invariant a la sixieme decimale sous permutation intra camp et reproduit a 100,0 pour cent par le generateur nul de a44 | a38 section 4, a44 section 9.2 | bloquante | [VERIFIE] | Ajouter a38, a37 et a30 au tableau des quantites de gabarit et n'en garder qu'une, la chute sous permutation, comme quantite de personne |
| 4 | C2 et C3 sont les deux seules conditions de a38 qui ne passent pas Holm sur K4, `p` ajuste 1,000 et 0,264, et ce sont elles que la synthese cite juste apres la phrase « huit tests passent Holm » | a38, MODELE 9.1 | bloquante | [VERIFIE] | Ecrire que les huit qui passent sont les six conditions de Stanford et les deux temoins, et publier un test apparie de C2 moins C3 |
| 5 | Le detecteur de i3 est cale sur des constantes humaines qui varient d'un facteur 1,9 a 2,5 entre le GSS et Twin a effectif egal, soit 14 a 25 ecarts types : cale ainsi, il classerait une population entierement humaine comme synthetique | i3, i3b section 4.1 | bloquante pour la portee | [VERIFIE] | Ecrire en tete de i3 qu'aucun seuil ne se transporte et que la reference se recalcule sur la population et l'effectif audites |
| 6 | Le troisieme terme de a44, rapport de reassignation 4,91 pour `v8`, n'a pas de plancher : le gain absolu de l'appariement hongrois sur une population sans structure vaut 0,0820 et celui de `v8` 0,0688, donc en dessous | a44 section 5.2 | serieuse | [VERIFIE] | Publier le gain absolu a cote du rapport et poser `B0 tirage` comme plancher de sur ajustement |
| 7 | Le regime « severe » de a35 donne 132 a 144 items de contexte contre 119 au regime « facile » : le cout de 6,6 points melange le retrait de la famille et l'ajout de 13 a 25 items | a35 section 6, a41 | serieuse | [VERIFIE] | Refaire le severe a taille de contexte egale, ou declarer que 6,6 points est une borne basse |
| 8 | Toutes les conditions a modele de langage sont evaluees en argmax, et le passage argmax vers tirage fait a lui seul tomber le ratio inter de `B1` de 1,48 ; aucun `C2 tirage` n'existe alors que les traces contiennent les distributions | a30, a35, a37, a38, a44 | serieuse | [VERIFIE pour l'ampleur statistique] | Produire C2 tirage et C3 tirage depuis `data/traces/` et republier gonflement, amplification et unanimite dans les deux regimes |
| 9 | Les pentes de a37 sont calculees sur 79, 73, 63 et 46 items selon la condition, et la synthese cite « moins 2,2 a moins 12,4 » sans denominateur : c'est la faute que a17 objection 2 avait declaree bloquante | a37, MODELE 10.4 | serieuse | [VERIFIE] | Ecrire le nombre d'items a cote de chaque pente et donner aussi la variante a derive humaine, moins 7,57 |
| 10 | Aucun preenregistrement n'est sous suivi de version ni depose : `git ls-files` renvoie zero fichier dans `popsim`, le commit cite ne les contient pas, et le protocole du projet exige un depot OSF horodate | a42, a43, a44, i1, i3 | bloquante pour le protocole | [VERIFIE] | Deposer les cinq textes sur OSF ou committer `resultats/`, sans quoi le mot « preenregistre » ne peut pas figurer dans un preprint |

Suivent immediatement, sans faire partie des dix : l'artefact hors pli de i1 qui vaut 28 a 43
pour cent des chutes qu'il sert a valider (10.1) ; la penalite de 3,93 points appliquee a
`composite` alors qu'elle est mesuree sur les Survey Agents (4.1) ; l'asymetrie de frequence
de segment entre raretes stables et instables, 0,109 contre 0,073, corrigee additivement
(5.1) ; `B2 argmax` presente comme recevant l'etiquette (2.3) ; l'absence d'errata en tete de
a25, a28, a31 et a34 ; et la fuite de `income` qui vaut un quart du signal individuel apparent
de `v6` (1.5).

---

# 16. Ce que je n'ai pas pu verifier

1. **Je n'ai rejoue aucun script en entier.** J'ai relu les caches `/tmp` par
   `a44_commun.charger` et rejoue des morceaux : la permutation intra segment sous neuf
   segmentations, le facteur d'amplification de a38 et son generateur nul, l'exactitude par
   item des dix conditions, un bootstrap sur la chute. Je n'ai relance ni `a44_mesures.py`,
   ni `a35_imputation.py`, ni `a38_tests.py`, donc je n'ai pas verifie que les CSV publies
   correspondent a la derniere version des scripts. Les valeurs que j'ai recalculees
   coincident partout avec les valeurs publiees, ce qui est un argument indirect fort.
2. **Le generateur nul applique a a38 tourne sur 30 replicats**, contre 200 dans a44, et sans
   bootstrap sur les personnes. La bande publiee en 2.1 porte donc l'incertitude du nul et pas
   celle de l'echantillon. La conclusion ne peut pas basculer, l'ecart entre la mesure et son
   nul valant 0,001 sur des valeurs de 1,2 a 3,1, mais les intervalles ne sont pas des
   intervalles complets.
3. **L'ampleur de l'artefact hors pli sur `L2` et `F` dans i1 n'est pas mesuree.** Je montre le
   mecanisme et je donne la taille de l'artefact sur T1 ; je n'ai pas construit la version
   corrigee, qui demande de refaire les cinq plis avec un estimateur different.
4. **La penalite propre de `agents composite` sous retrait de bloc n'est pas mesurable ici.**
   Le paquet OSF ne contient, a ma connaissance, aucun fichier de la condition « retrait par
   bloc » ; a17 point 2 signalait deja qu'une heure de recherche dans l'archive trancherait, et
   elle n'a toujours pas ete faite. Mon objection 4.1 porte sur l'attribution, pas sur un
   chiffre de rechange.
5. **Je n'ai pas construit `C2 tirage`.** L'objection 3.4 s'appuie sur l'ampleur mesuree du
   passage argmax vers tirage chez les quatre couples statistiques de a35 et sur le fait que
   les traces contiennent les distributions ; le report de cette ampleur aux agents est une
   inference, pas une mesure.
6. **Rien sur Twin-2K-500 par mes propres calculs.** Les chiffres de la section 11.1 sont lus
   dans `i3b-twin-reference.csv` et `i3b-reference-par-taille.csv`, pas recalcules sur les
   donnees brutes de Twin.
7. **Je n'ai pas ouvert les papiers tiers.** Yuan, Peng, Ahn, Rennard, von der Heyde, Oceno :
   je prends pour exactes les citations des rapports. Mes objections portent sur ce que le
   dossier fait de ces lectures, jamais sur leur fidelite.
8. **Je n'ai pas evalue la puissance des non rejets.** a39 8.1, a44 tableau 1 et i1 10.2
   reposent sur des intervalles qui contiennent zero ; je signale l'absence de calcul de
   puissance sans la combler.
9. **Le codage d'orientation des 79 items de a37 et le bit d'endogroupe des 29 items de a38 ne
   sont pas verifiables de l'exterieur.** Ils sont dans les scripts, donc ecrits avant le
   calcul si l'on accepte l'horodatage, mais rien ne permet de savoir s'ils ont ete choisis
   apres une lecture descriptive, comme a34 le declare pour sa propre famille. a38 publie un
   controle sur les humains, 28 bits sur 29 confirmes, qui est le meilleur argument
   disponible et qui ne repond pas a la question de la selection des 29.
10. **La replication sur Twin de la chute sous permutation n'existe pas**, et c'est ce qu'un
    relecteur demandera en premier apres avoir lu la section 1.1 : si le chiffre depend de la
    segmentation sur le GSS, il faut savoir s'il depend aussi du jeu. `MODELE` 10.5 verrou
    trois le prevoit a zero appel.
11. **L'horodatage des preenregistrements repose sur le systeme de fichiers d'un repertoire
    synchronise par iCloud.** Je constate que l'ordre est correct et qu'aucun fichier n'a ete
    touche apres son script ; je ne peux pas exclure une reecriture qui aurait preserve les
    dates, et aucun tiers ne le pourra tant que rien n'est depose.

---

# 17. En une phrase, pour Simon

Le dossier a change de quantite maitresse au bon moment, mais la nouvelle quantite est
mesuree a l'interieur de la variable que l'agent recoit, le contraste qui lui donne son sens
causal n'est pas une ablation, et deux des quatre piliers de la these reecrite sont, par le
critere que le dossier vient d'adopter, des descriptions du gabarit de groupe. Trois nuits de
calcul a zero appel de modele suffisent a fermer les trois : la grille des segmentations, le
generateur nul passe sur a38, a37 et a30, et le placebo d'etiquette.
