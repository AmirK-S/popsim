# s1. Ce qui manque pour poser la question forte, et le protocole pret a jouer

Seance du 9 septembre 2026. **Aucun appel de modele de langage.** Ce document accompagne
`resultats/s1-resultats.md`, qui rend le test **faisable aujourd'hui** sur une cible degradee,
« le public ». Celui ci dit ce qu'il faudrait pour la cible forte, **un camp**, et il est
ecrit pour etre execute le jour ou la donnee arrive, sans reflexion supplementaire.

Conventions : **[CONFIRME]** lu dans une source verifiee, **[MESURE]** calcule ici,
**[PROBABLE]** interpretation etayee.

---

## 1. La question forte, et le seul terme qui manque

Question forte : quand un modele decrit ce que pense **la gauche**, ressemble t il davantage
a la vraie gauche, ou a ce que **la droite** croit de la gauche ?

Trois termes sont necessaires. Deux sont sur le disque.

| terme | etat | ou |
|---|---|---|
| ce que le modele dit du camp | **present**, 149 items du GSS, 3 camps, 2 identites de demandeur, 5 fichiers de traces | `data/traces/r1-*.jsonl`, `r4` |
| la realite du camp | **present**, distributions humaines par camp et par vague | `data/traces/r1-distributions-reelles.csv`, 2 946 lignes |
| **ce que le camp adverse croit du camp, sur ces opinions** | **absent** | nulle part |

[CONFIRME]

## 2. Ce qui manque, exactement

Il manque **une enquete ou les memes personnes font trois choses** :

1. declarer leur propre position sur un jeu d'enonces d'opinion,
2. estimer la position ou la part de soutien **du parti democrate**, sur ces memes enonces,
3. estimer la meme chose **du parti republicain**,

et ou l'appartenance partisane ou ideologique du repondant est connue, pour separer la
croyance sur son propre camp de la croyance sur le camp adverse.

Le point 1 est ce qui fournit la realite ; sans lui, les points 2 et 3 ne donnent qu'une
perception sans reference, et c'est exactement pourquoi
`data/ahler-sood-pcomp/extremity_exp_data.dta` est inutilisable : ses variables `dem_per` et
`rep_per` donnent les points 2 et 3 sur quatre enjeux, `tax`, `abortion`, `gays`, `race`, et
**aucune mesure de la realite**, ni meme le libelle exact des quatre enonces. [MESURE]

## 3. Les sources publiques qui le fournissent, de la moins chere a la plus chere

### 3.1 ANES, series temporelles, echelles de placement des partis. **Gratuit, inscription.**

C'est la source la moins chere qui fournit les trois points. Les codebooks sont deja sur le
disque, `data/anes-codebooks/`, et listent le triplet **position de soi, position percue du
parti democrate, position percue du parti republicain** sur les echelles a sept points :

- liberal contre conservateur ;
- depenses et services publics ;
- assurance maladie publique contre privee ;
- emploi et niveau de vie garantis par l'Etat ;
- aide aux minorites noires ;
- defense ;
- immigration, environnement contre emploi, avortement selon les annees.

[CONFIRME, `data/anes-codebooks/anes_timeseries_2024_varlist_20250808.pdf` et le codebook
cumulatif]

**Realite du camp** : moyenne des placements de soi des repondants du camp, dans la meme
enquete, la meme annee, avec les poids. **Croyance de second ordre** : moyenne des placements
du parti faits par les repondants de l'autre camp. Les deux sont dans le meme fichier, sur
les memes personnes, ce qui elimine tout probleme d'appariement d'echantillon.

**Cout** : zero euro. Un compte sur `electionstudies.org`, nominatif, et un telechargement
qui interdit la redistribution, ce qui est compatible avec notre regle, `data/` n'etant pas
versionne. **C'est une demande a faire, pas un achat.** Le fichier a viser en premier est le
cumulatif, qui donne la serie longue et donc la variation dans le temps de l'ecart de
perception, quantite que personne n'a mise en face d'un modele.

**Limite a connaitre d'avance** : l'echelle a sept points n'est pas une distribution de
reponses. `r1` demande au modele une repartition en pourcentages sur les modalites d'un item.
Pour comparer, il faut soit demander au modele un placement moyen sur la meme echelle a sept
points, soit transformer les placements humains en distribution. **Le premier choix est le
bon** : il ne transforme rien du cote humain, et il coute un run court, decrit en section 4.

### 3.2 IGS Poll d'Ahler et Sood. **Gratuit si les auteurs le donnent.**

`pcomp_igspoll.dta` est **l'homologue exact** de la question forte, dans le meilleur format
possible : chaque repondant voit six enonces de politique publique tires d'une liste de
vingt cinq, declare son propre soutien, puis estime le pourcentage de repondants democrates
et le pourcentage de repondants republicains qui les soutiennent. Le referent est la meme
enquete. [CONFIRME, `data/ahler-sood-pcomp/codebook.txt`, section IGS Poll, variables
`q5_*`, `q19_*`, `q98_*`, `policy1` a `policy6`]

Il **n'est pas dans l'archive Dataverse**, bien que `readme.txt` le cite. Il faut le demander
a Doug Ahler ou a Gaurav Sood, dont les adresses sont dans le `readme.txt`. C'est une
demande d'une page. **Rapport valeur sur cout imbattable** : c'est la seule source connue qui
donne le second ordre par parti **sur des opinions**, avec sa realite, sur des enonces
contemporains et courts, donc directement transposables en invite.

### 3.3 Perception Gap, More in Common. **Gratuit, donnees agregees.**

Le rapport « The Perception Gap » publie des ecarts de perception par camp sur des enonces
d'opinion. Les microdonnees ne sont pas publiques a notre connaissance ; les tableaux
agreges, oui. Un tableau agrege suffit pour comparer une **moyenne de camp** a une moyenne de
modele, ce qui est exactement la forme de nos tests, mais il interdit tout bootstrap sur les
personnes et tout controle par sous groupe. **Solution de repli**, pas premier choix.

### 3.4 Ce qui ne sert pas

- **CES et GSS** : premier ordre uniquement, aucune question de placement des partis.
- **Twin-2K-500** : cible « le public », deja exploite par `s1-resultats.md`.
- **Westwood 2025** : repondants synthetiques, aucune croyance humaine.

## 4. Le protocole, pret a jouer le jour ou la donnee arrive

Ecrit ici pour n'avoir plus qu'a l'executer. Il ne demande **aucune decision nouvelle**.

### 4.1 Si c'est l'ANES

**Etape 1, sans modele.** Pour chaque item de placement et chaque annee retenue, calculer
trois quantites ponderees : `S(j, c)` position moyenne declaree par les membres du camp `c` ;
`B(j, c, c')` position moyenne que les membres du camp `c'` attribuent au camp `c` ;
`n` par cellule. Sortie `resultats/s2-termes-anes.csv`. Aucun appel.

**Etape 2, page de plan.** Meme squelette que `s1-preenregistrement.md` : hypotheses avec
direction, bootstrap sur les items, permutation de signe exacte si le nombre d'items est
inferieur ou egal a 20, Holm par famille, bande de non materialite [0,95 ; 1,05], criteres de
chute. **Verifier avant d'ecrire** que le nombre d'items permet d'atteindre 0,05 apres Holm :
avec `J` items, la p minimale est `2 / 2^J`, et il faut `2 / 2^J` inferieur a `0,05 / K` pour
`K` tests dans la famille. Avec 8 items et 12 tests, `2 / 256 = 0,0078` contre
`0,05 / 12 = 0,0042` : **cela ne passe pas**, il faut au moins 9 items ou moins de tests.
C'est le calcul que a46 n'a pas fait et que s1 a fait.
**Ajouter le critere de resolution corrige** : le plancher doit etre compare au bruit de la
quantite testee, `plancher / racine(n)` pour une moyenne de camp, jamais au plancher
individuel. C'est l'erreur commise en s1, section 6.

**Etape 3, run.** Reprendre `analyses/r1_oracle_camps.py` sans le modifier, en changeant
seulement la question posee : au lieu de « repartis 100 points sur les modalites », demander
« sur cette echelle en sept points, ou se situe en moyenne un liberal americain », avec les
memes trois modeles locaux, la meme temperature, le meme parse strict, la meme relance unique
sans exemple chiffre. Plan : `J` items x 3 camps x 2 identites de demandeur x 3 modeles.
A `J = 9`, cela fait **162 appels par modele**, soit moins de vingt minutes au debit mesure
en r1. Trace dans `data/traces/s2-*.jsonl`.

**Etape 4, evaluation.** Pour chaque cellule modele x camp decrit x identite du demandeur,
les trois distances : a `S(j, c)`, a `B(j, c, c')` la croyance du camp adverse, et a
`B(j, c, c)` la croyance du camp lui meme. Plus le plancher de reinterrogation, qui existe
dans les panels ANES. Le contraste central devient enfin dicible :
**le portrait fait a un adversaire se rapproche t il de ce que l'adversaire croit deja ?**
C'est la question que `r1` a posee par son axe d'identite et qu'elle n'a jamais pu boucler
faute de referent.

### 4.2 Si c'est l'IGS Poll

Identique, en plus simple, parce que la quantite est deja une part de soutien en pourcentage,
donc directement comparable a une repartition demandee au modele. Les six enonces vus par
chaque repondant sont tires d'une liste de vingt cinq : verifier d'abord le nombre d'enonces
ayant assez de repondants par camp, et **ne pas descendre sous neuf enonces** pour la raison
de puissance ci dessus.

### 4.3 Ce que le protocole coute, en tout

Zero euro. Une demande de compte ANES, ou un courriel a deux auteurs. Un run local de moins
de vingt minutes par modele. Deux scripts nouveaux, prefixes `s2`, qui n'importent que des
briques existantes. **Le seul cout reel est le delai de reponse d'un tiers**, et c'est
pourquoi ce document existe : pour que le jour de la reponse, il ne reste rien a decider.

---

## Ce que je n'ai pas pu verifier

1. **Que les items de placement des partis soient poses dans l'edition 2024 de l'ANES** avec
   les memes libelles que dans le cumulatif. La lecture s'appuie sur la liste de variables et
   sur les index SDA, pas sur le questionnaire administre.
2. **Que More in Common publie encore ses tableaux agreges** et sous quelle licence. Aucune
   requete reseau n'a ete faite dans cette seance.
3. **Que les auteurs d'Ahler et Sood puissent partager l'IGS Poll**, qui peut etre soumis a
   un accord avec l'Institute of Governmental Studies de Berkeley.
4. **Le debit reel d'un run de placement sur echelle**, estime par transposition du debit de
   `r1`, qui demandait une repartition et non un point. Une sortie plus courte devrait etre
   plus rapide, ce n'est pas mesure.
5. **Que les modeles acceptent de placer un camp sur une echelle a sept points** sans refuser
   ni derailler. Aucun essai n'a ete fait, et c'est exactement le genre de chose qui ne se
   sait qu'au premier run.

## Questions ouvertes pour Simon

1. Avez vous un compte ANES, ou faut il en creer un ? Le fichier cumulatif suffit il, ou
   voulez vous l'edition 2024 pour la contemporaneite ?
2. Preferez vous demander l'IGS Poll a Ahler et Sood, ce qui donne la meilleure forme, ou
   partir sur l'ANES tout de suite, ce qui ne depend de personne ?
3. La transformation a faire du cote modele : lui demander un point sur une echelle, ou lui
   demander une repartition puis en tirer une moyenne ? Le premier ne transforme rien du cote
   humain, le second reste comparable a `r1`. Un seul peut etre le protocole principal.
4. Le calcul de puissance avant ecriture, `2 / 2^J` contre `0,05 / K`, doit il devenir une
   section obligatoire de toute page de plan du projet ?
