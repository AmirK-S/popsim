# r5. Ce sont les exemples, pas le mode assistant

Run parti le 2026-09-09 a 12:23:43, termine a 12:40:22, marqueur `RUN TERMINE` dans
`data/traces/r5-run.log`. Une condition de 894 cellules, 894 appels locaux, 16 minutes
36 secondes de machine, zero euro, rien n'est sorti de la machine. Essai a blanc de
3 cellules a 12:16:59, dans `data/traces/r5-smoke.jsonl` et `r5-smoke.log`, jamais melange
au run. Script : `analyses/r5_gabarit_exemples.py`, qui importe `MoteurR1` et le bloc
d'exemples de R4 sans en recopier une ligne. Evaluation par
`analyses/r5_gabarit_exemples.py --evaluer`, qui appelle `analyses/r1_evaluer.py --suffixe r5`.

Page de plan : `resultats/r5-preenregistrement.md`, ecrite le 2026-09-09 a 09:50, avant tout
appel. Elle a ete deposee hors de la machine avant le premier appel : l'orchestrateur
rapporte une registration OSF a 12:20:15 CEST, le fichier de porte `data/traces/GO-R5` porte
12:22:54, le premier appel de modele est parti a 12:23:46. **Je n'ai pas verifie le depot
moi meme** : rien ne sort de cette machine et je n'ai consulte aucune page distante ; cet
element est transmis, pas produit ici. Voir la section de cloture.

**Reserve d'anteriorite, dans l'esprit de `resultats/bilan-predictions.md` section 2.** La
page de plan a bien ete modifiee apres son ecriture : `git diff` montre **une seule ligne
changee**, la ligne d'en tete, qui passe de « En attente d'une ligne d'Amir » a la mention de
la validation et du depot OSF ; horodatage de la modification 12:22:54, soit **avant le
premier appel** de 12:23:46. **Aucune hypothese, aucune bande, aucune valeur de reference
n'a bouge.** Je peux l'attester d'une seconde facon : j'ai lu cette page vers 12:13, avant sa
modification et avant tout appel de modele, et les enonces que je tranche ici, H1, H2, H3, la
bande de 0,15 et les valeurs 0,727 et 0,245, sont mot pour mot ceux de la version que j'ai
lue. [MESURE, `git diff resultats/r5-preenregistrement.md`]

A lire avec : `resultats/r4-resultats.md` sections 2.1 et 3.1, dont ce rapport corrige la
lecture sans la contredire, et `resultats/r4-oracle-socle.md` section 3, qui donne les trois
exemples en entier.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## Reponse en une ligne

**Sur l'ecart entre camps decrit, `Qwen3-4B-Instruct-2507` sous gabarit ChatML avec les trois
exemples rend 0,627 fois le reel, contre 0,245 sans les exemples et 0,727 avec les exemples
mais sans gabarit : des +0,482 que R4 attribuait au « format », les exemples en portent
+0,382 [+0,200 ; +0,578] et le gabarit de conversation +0,101 [+0,017 ; +0,183], soit une
position a 0,79 [0,60 ; 0,97] du chemin entre les deux ; la lecon est « donnez des
exemples », et la these « le mode assistant censure » est ecartee.** [MESURE]

**Consequence pour l'audit : ce qui doit entrer dans le registre des versions du programme A,
ce n'est pas « le format » comme un bloc, c'est la presence ou l'absence d'exemples dans
l'invite. Deux auditeurs qui emploient tous deux un gabarit de conversation publieront des
chiffres qui different d'un facteur 2,6 selon qu'ils montrent ou non trois exemples.**
[MESURE pour le fait, PROBABLE pour la portee]

---

## Les taux de rejet, avant tout chiffre

La page de plan les met en tete, et elle a raison : R5 supprime la relance, donc son taux
n'est pas comparable a celui des trois conditions de reference sans precaution.

| | `q4` | `q4nogab` | `q4base` | `q4gab3` |
|---|---|---|---|---|
| relance | conservee | conservee | conservee | **supprimee** |
| echecs de **premiere** tentative | 13, **1,45 %** | 16, **1,79 %** | 24, **2,68 %** | 20, **2,24 %** |
| rejets **finals**, apres relance | 0 | 1, 0,11 % | 0 | **20, 2,24 %** |
| cellules retirees au critere de chute 2 | 11 | 15 | 24 | **0** |
| perimetre exploite | 883 / 894 | 878 / 894 | 870 / 894 | **874 / 894** |

[MESURE, `resultats/r5-rejets.csv`, `r1-controles-r5.csv`, `data/traces/r5-resume.json`]

**La seule ligne comparable entre les quatre conditions est la premiere tentative**, et sur
celle la `q4gab3` a 2,24 pour cent se place entre `q4nogab` (1,79) et `q4base` (2,68). Les
trois exemples coutent donc un peu de conformite de format meme sous gabarit, environ huit
dixiemes de point par rapport a `q4` : un modele a qui l'on montre des exemples arithmetiques
se met a compter, et compte parfois mal. [MESURE]

**Les 20 rejets sont tous arithmetiques et tous sur les items a beaucoup de modalites.** Le
motif est la somme hors de la bande [95 ; 105] dans 20 cas sur 20, jamais un format illisible,
jamais une lettre manquante. Repartition par nombre de modalites : K = 5 deux fois, K = 6 deux
fois, K = 7 deux fois, K = 8 cinq fois, K = 9 cinq fois, K = 12 quatre fois ; **aucun rejet
sous K = 5**. Les items touches sont `wrkstat` (5), `attend` (5), `income` (4), `kidssol` (2),
puis `fucitzn`, `racwork`, `wlthblks` et `jew` une fois chacun. [MESURE]

**Aucun de ces rejets ne touche le perimetre des mesures principales.** Zero rejet sur les
79 items orientes, zero sur les 65 items retenus stricts, dans les deux identites de
demandeur. **Les quatre conditions sont donc comparees sur exactement les memes 79 items et
les memes 65 items**, et les trois contrastes ci dessous ne perdent pas une seule paire. La
regle de la page de plan, « un item est retire d'un contraste si une des deux conditions
comparees le rejette », n'a jamais eu a s'appliquer. [MESURE]

**Le gain cache de la suppression de la relance.** R4 devait retirer 56 cellules au critere de
chute 2, parce qu'en mode completion la relance recopie son exemple chiffre 45 fois sur 45.
`q4gab3` en retire zero, par construction : il n'y a plus de relance, donc plus d'exemple
chiffre a recopier. La conduite preenregistree de R5 supprime une source de biais entiere au
prix de 20 cellules perdues. [MESURE]

**Les autres criteres de chute passent.** Critere 1, seuil 0,25 : 0,022 pour `q4gab3`.
Critere 3, distribution identique d'un camp a l'autre, seuil 0,90 : 0,138, le plus bas des
quatre conditions. Critere 4, plancher humain, facteur w2 sur w1 : 1,009, dans la bande
[0,85 ; 1,15]. Critere 5, effectifs des camps : 417 / 303 / 332, conformes. Critere 6,
empreinte du referent humain : `ea7cd93e...91c811`, inchangee depuis R1, verifiee avant le
premier appel et refusant de lancer le run en cas d'ecart. Un seul `llama-server` a la fois,
verifie par `pgrep -x` avant le lancement et arrete a la fin.
[MESURE, `resultats/r1-controles-r5.csv`, `data/traces/r5-run.log`]

---

## 1. Le verdict, contre le pari ecrit

Quantite : le facteur H2b, ecart signe entre camps decrit rapporte a l'ecart reel, sur les
79 items orientes, identite journaliste. C'est la quantite dont la page de plan cite les deux
valeurs de reference, `q4nogab` 0,727 et `q4` 0,245. Bootstrap sur les items, 2 000 tirages ;
permutation de signe appariee par item, 20 000 tirages, estimateur de Phipson et Smyth ; Holm
sur ces trois tests et sur eux seuls.

| test | contraste apparie | IC 95 % | p | p de Holm | hors de la bande 0,15 |
|---|---|---|---|---|---|
| T1, `q4gab3` contre `q4` | **+0,382** | [+0,200 ; +0,578] | 0,00015 | **0,00045** | **oui** |
| T2, `q4gab3` contre `q4nogab` | **-0,101** | [-0,183 ; -0,017] | 0,026 | **0,026** | **non** |
| T3, `q4gab3` contre le milieu | **+0,141** | [+0,038 ; +0,253] | 0,0097 | **0,019** | non |

Position sur le segment `q4` vers `q4nogab` : **lambda = 0,79 [0,60 ; 0,97]**.
[MESURE, `resultats/r5-contrastes.csv`]

| hypothese preenregistree | enonce | verdict |
|---|---|---|
| **H1**, les exemples font la marche | `q4gab3` a moins de 0,15 de `q4nogab` (0,727) | **VRAIE**, ecart 0,101 |
| **H2**, le gabarit fait la marche | `q4gab3` a moins de 0,15 de `q4` (0,245) | **FAUSSE**, ecart 0,382 |
| **H3**, les deux comptent | entre les deux, **hors des deux bandes** | **FAUSSE**, dans la bande de `q4nogab` |
| **Pari** | H3, valeur plus proche de `q4nogab` que de `q4` | **perdu sur sa lettre, gagne sur sa direction** |

**H1 est vraie, et c'est la lecture simple que la page voulait pouvoir exclure.** L'ecart de
`q4gab3` a `q4nogab` vaut 0,101, sous la barre de 0,15 que la page avait posee avant de voir
le chiffre. La lecon est celle que H1 annonce en toutes lettres : **le gabarit est presque
innocent, et ce qu'il faut retenir est « donnez des exemples »**. [MESURE]

**H2 est fausse, et elle l'est largement.** Ajouter trois exemples a l'interieur d'un gabarit
de conversation, sans toucher un seul poids ni une seule balise de role, deplace la mesure de
+0,382, deux fois et demie la bande de 0,15, avec un intervalle qui ne s'en approche pas.
**La these « le mode assistant censure » ne survit pas a ce test** : le mode assistant est
intact dans `q4gab3`, l'invite systeme est celle de `q4` au caractere pres, le tour assistant
est ouvert de la meme facon, et le portrait des camps se dilate quand meme des trois quarts du
chemin. [MESURE pour le fait, PROBABLE pour la portee au dela de ce modele]

**H3 est fausse, et le pari tombe avec elle.** `q4gab3` tombe bien entre les deux, mais pas
hors des deux bandes : il est dans celle de `q4nogab`. La condition d'exclusion que H3 posait
n'est pas remplie. **Ce pari etait ecrit contre la these « le mode assistant censure », et il
perd du bon cote** : la these visee sort plus affaiblie que si H3 avait ete vraie, puisque le
gabarit ne porte pas un cinquieme de la marche au lieu du tiers ou de la moitie qu'une lecture
intermediaire aurait laisses. La direction pariee, « plus proche de `q4nogab` », est confirmee
de facon decidable, T3, +0,141 [+0,038 ; +0,253], p de Holm 0,019. [MESURE]

**Une nuance qu'il faut ecrire, et que la page de plan n'avait pas prevue.** H1 et H2 sont
enoncees sur la **valeur ponctuelle** du facteur, et c'est ainsi qu'elles sont tranchees ci
dessus. Mais l'intervalle du contraste apparie T2, [-0,183 ; -0,017], **deborde la bande de
0,15 par sa borne basse**. Deux consequences honnetes. La premiere : l'ecart de `q4gab3` a
`q4nogab` est **decidable et non nul**, p de Holm 0,026 ; le gabarit n'est pas exactement
innocent, il porte un cinquieme de la marche. La seconde : les donnees ne permettent pas
d'affirmer une equivalence a 0,15 pres au sens strict d'un test d'equivalence, seulement de
constater que la valeur ponctuelle y tombe. **H1 est vraie a la lettre de la page, et elle
serait indecidable sous une lecture par intervalle.** [MESURE]

### 1.1 La decomposition, en une phrase

Sur les +0,482 que R4 mesurait entre `q4` et `q4nogab` et appelait « le format » :

- **les trois exemples en portent +0,382, soit 79 pour cent** ;
- **le gabarit de conversation en porte +0,101, soit 21 pour cent** ;
- la somme des deux morceaux fait +0,483, contre +0,482 pour la marche mesuree directement :
  la decomposition est additive au millieme, ce qui est attendu puisque les trois quantites
  se calculent sur les memes 79 items avec le meme denominateur. [MESURE]

**Les exemples seuls font plus, a eux seuls, que tout l'ecart entre le socle et l'instruit.**
`q4base` moins `q4` vaut +0,322 sur cette quantite ; les exemples valent +0,382. [MESURE]

### 1.2 La meme decomposition dans les trois autres cellules

Lambda, la part de la marche portee par les exemples, dans les quatre cellules du plan
[MESURE, `resultats/r5-contrastes.csv`]

| perimetre | identite | lambda | IC 95 % |
|---|---|---|---|
| 79 items orientes | journaliste | **0,79** | [0,60 ; 0,97] |
| 79 items orientes | adversaire | **0,84** | [0,70 ; 1,01] |
| 65 items retenus stricts | journaliste | **0,80** | [0,60 ; 0,98] |
| 65 items retenus stricts | adversaire | **0,76** | [0,63 ; 0,87] |

**Les quatre bornes basses sont au dessus de 0,5** : « les exemples portent plus que le
gabarit » est decidable dans les quatre cellules, et non dans la seule cellule preenregistree.
Les trois cellules hors du test principal sont descriptives et sans correction de Holm ; elles
ne servent qu'a montrer que le chiffre principal n'est pas un accident de perimetre. [MESURE]

Verdict de H1 dans les quatre cellules, a la lettre de la page : vraie sur 79 items
journaliste (0,101), vraie sur 79 items adversaire (0,104), vraie sur 65 items journaliste
(0,102), **fausse sur 65 items adversaire (0,174)**. Trois cellules sur quatre. [MESURE]

---

## 2. Le tableau des quatre conditions

Facteur H2b, ecart signe entre camps decrit sur ecart reel. 1,000 serait la fidelite parfaite ;
le plancher de reinterrogation humaine vaut 1,009.
[MESURE, `resultats/r5-tableau.csv`, `r1-h2-ecart-r5.csv`]

| perimetre, identite | `q4` gabarit seul | `q4base` socle, exemples | `q4gab3` **gabarit et exemples** | `q4nogab` exemples seuls |
|---|---|---|---|---|
| 79 items orientes, journaliste | 0,245 | 0,566 | **0,627** | 0,727 |
| 79 items orientes, adversaire | 0,221 | 0,440 | **0,754** | 0,859 |
| 65 items stricts, journaliste | 0,304 | 0,574 | **0,708** | 0,810 |
| 65 items stricts, adversaire | 0,270 | 0,476 | **0,808** | 0,982 |

Intervalles de la ligne principale, 79 items orientes, journaliste : `q4` 0,245
[0,056 ; 0,434], `q4base` 0,566 [0,380 ; 0,785], `q4gab3` 0,627 [0,385 ; 0,875], `q4nogab`
0,727 [0,482 ; 0,984]. Contre le plancher humain, seul `q4` est encore decidablement en
dessous apres Holm dans la famille de l'evaluateur, p 0,0004 ; `q4gab3` l'est de justesse,
p 0,034 ; `q4nogab` ne l'est plus, p 0,125. [MESURE, `resultats/r1-h2-ecart-r5.csv`]

**`q4gab3` et `q4base` ne se distinguent pas.** Contraste apparie +0,060 [-0,106 ; +0,229],
p 0,49, hors famille de Holm. L'instruit sous gabarit avec exemples et le socle avec exemples
decrivent l'ecart entre camps de la meme facon, a la precision de ce run. [MESURE]

### 2.1 Ce que les exemples ne reparent pas

**La dispersion interne, H1.** Les quatre conditions sur decrivent la variete interne des
camps, et les exemples n'y changent rien de systematique.
[MESURE, `resultats/r1-h1-unanimite-r5.csv`, identite journaliste, plancher humain 1,005 /
1,008 / 0,996]

| camp | `q4` | `q4base` | `q4gab3` | `q4nogab` |
|---|---|---|---|---|
| gauche | 1,174 | 1,164 | **1,110** | 1,101 |
| centre | 1,114 | 1,147 | **1,166** | 1,122 |
| droite | 1,059 | 1,081 | **1,089** | 1,090 |

Contrastes apparies de `q4gab3` contre `q4` : gauche -0,056 [-0,092 ; -0,020], centre
+0,044 [+0,021 ; +0,069], droite +0,030 [-0,007 ; +0,064]. **Les exemples rapprochent de 1 sur
la gauche et en eloignent sur le centre**, dans deux directions opposees et dans les deux cas
d'une quantite dix fois plus petite que celle qu'ils deplacent sur H2b. Il n'y a pas de
lecture simple ici, et il ne faut pas en fabriquer une. [MESURE]

**L'erreur globale.** `TV(decrit, reel)` en part du plancher de reinterrogation humaine,
identite journaliste : `q4` 11,1 / 8,6 / 11,3 sur gauche / centre / droite ; `q4gab3` 11,5 /
8,0 / 9,9 ; `q4nogab` 11,6 / 7,7 / 9,6 ; `q4base` 13,4 / 8,3 / 10,3. **Les quatre conditions se
trompent de huit a treize fois le plancher humain, et rien de ce que fait ce run ne le
change.** Elargir l'ecart entre camps n'est pas se rapprocher des humains : c'est deplacer une
erreur, pas la reduire. [MESURE]

**L'effet de l'identite du demandeur, H3 de R1.** `q4gab3` change le portrait d'un camp selon
qui demande, 3,23 fois le plancher humain sur la gauche [2,64 ; 3,92] et 2,92 sur la droite
[2,44 ; 3,48], p de Holm 0,0004 dans les deux cas. C'est la valeur la plus basse des quatre
conditions sur la droite et le milieu du peloton sur la gauche, la fourchette des quatre
allant de 2,92 a 5,05. **Le resultat de R1 tient sous les quatre formats d'invite**, et les
exemples ne l'attenuent pas de facon lisible.
[MESURE, `resultats/r1-h3-identite-r5.csv`]

---

## 3. Ce que cela change a `r4-resultats.md` section 2.1

Rien de la section 2.1 n'est faux, et rien n'y est a reecrire. Ce qui change est ce qu'on a le
droit d'en conclure.

**Ce qui tient sans retouche.** « `q4` et `q4nogab` sont le meme fichier, meme empreinte, meme
moteur, memes parametres d'appel, meme referent humain, memes 894 cellules » : vrai, et
`q4gab3` est ce meme fichier une troisieme fois. « Changer le format d'invite sans toucher un
seul poids deplace la mesure de +0,48 [+0,29 ; +0,68] » : vrai, et R5 le retrouve a +0,482.
« La quantite auditee depend du format d'invite au moins autant que des poids » : vrai, et
renforce, puisque les exemples seuls, +0,382, depassent deja l'ecart socle contre instruit,
+0,322. [MESURE]

**Ce qui doit changer de nom.** La section 2.1 s'intitule « le format seul, poids tenus
fixes ». **« Le format » y designe deux choses a la fois**, et R5 mesure que ces deux choses
ne pesent pas le meme poids : les exemples 79 pour cent, le gabarit 21 pour cent. Toute phrase
qui dit « le format » sans preciser laquelle des deux composantes est visee est desormais trop
vague pour etre auditee. **La formulation correcte est : la presence de trois exemples dans
l'invite deplace la mesure de +0,382 ; le passage d'un gabarit de conversation a une
completion la deplace de +0,101 de plus.** [MESURE]

**Ce qui est interdit a partir de maintenant.** La lecture « le mode assistant, ou le post
entrainement de conversation, ecrase le portrait des camps » ne peut plus etre tiree de la
section 2.1. R4 ne la soutenait pas explicitement, mais son dispositif la laissait ouverte : le
gabarit ChatML etait retire en meme temps que les exemples etaient ajoutes, et rien ne
permettait de dire lequel des deux agissait. **R5 le dit : c'est l'ajout des exemples.**
[MESURE]

**Ce que cela change au tableau de la section 2.1.** La ligne « facteur H2b, 79 items
orientes, 0,245 contre 0,727, contraste +0,482 » gagne une colonne intermediaire a 0,627, et
la lecture de la ligne passe d'un contraste a une decomposition en deux termes inegaux. Les
quatre autres lignes du tableau, ratio H1 camp gauche, H4, alpha, erreur en part du plancher,
ne sont pas retestees ici pour H4 et ne changent pas de verdict pour les trois autres. [MESURE]

**Ce que cela ne change pas.** La section 2.2 de R4, les poids seuls a format tenu fixe, n'est
pas touchee : elle compare `q4base` a `q4nogab`, deux conditions que R5 ne rejoue pas. La
section 2.3 sur l'hybride `q4hyb` n'est pas touchee non plus. Le mecanisme que R4 y decrit,
un modele instruit qui reconstruit un tour d'assistant dans 57 a 64 pour cent de ses relances,
reste la meilleure explication disponible de `q4hyb`, et R5 n'apporte rien contre lui. [MESURE
pour le perimetre, PROBABLE pour le mecanisme, qui reste celui de R4]

### 3.1 Ce que R5 autorise a ecrire, et ce qu'il interdit

**Autorise.** « Sur `Qwen3-4B-Instruct-2507` en Q4_K_M, la presence de trois exemples de
format dans l'invite explique environ quatre cinquiemes de l'ecart de mesure entre les deux
protocoles de R4, le gabarit de conversation environ un cinquieme. » « Un registre de versions
qui note le modele, la quantification et le gabarit, mais pas le nombre d'exemples, laisse
passer la plus grande source de dispersion mesuree dans ce dossier. » [MESURE]

**Interdit.** « Le mode assistant censure le portrait des camps. » « Les exemples rapprochent
le modele des humains » : ils elargissent l'ecart entre camps, ils ne reduisent pas l'erreur,
qui reste a huit ou treize fois le plancher. « Ce resultat vaut pour les modeles de langage » :
il vaut pour un fichier de poids, une quantification, un jeu d'items et une facon de poser la
question. « Trois exemples suffisent a bien mesurer » : `q4gab3` reste a 0,627 d'un plancher de
1,009, et son intervalle est large.

---

## Rejouer

```bash
# la verification hors ligne, aucun serveur, aucun appel
.venv/bin/python analyses/r5_gabarit_exemples.py --verifier

# l'essai a blanc, 3 cellules, fichiers separes du run
.venv/bin/python analyses/r5_gabarit_exemples.py --smoke

# le run, 894 cellules, un seul serveur, ne demarre que si data/traces/GO-R5 existe
.venv/bin/python analyses/r5_gabarit_exemples.py --fin 23:59

# l'evaluation, r1_evaluer.py --suffixe r5, et les copies des trois conditions de reference
.venv/bin/python analyses/r5_gabarit_exemples.py --evaluer

# les trois contrastes apparies, le tableau des quatre conditions, les rejets
.venv/bin/python analyses/r5_gabarit_exemples.py --contrastes
```

---

## Ce que je n'ai pas pu verifier

1. **Le depot de la page de plan hors de la machine.** L'orchestrateur rapporte une
   registration OSF a `https://osf.io/3r6zg/`, horodatee 12:20:15 CEST et **en attente
   d'approbation** au moment ou j'ecris, et le fichier de porte `data/traces/GO-R5` porte
   12:22:54, avant le premier appel a 12:23:46. **Je n'ai consulte aucune page distante** :
   rien ne sort de cette machine, et je n'ai donc verifie ni l'existence de cette
   registration, ni son contenu, ni sa date, ni son approbation. Cet element est **transmis**,
   pas produit ici. Un lecteur qui veut l'anteriorite doit la verifier lui meme sur OSF, et
   attendre que la registration soit approuvee et porte un DOI.
2. **La contamination.** Rien dans ce run ne dit si le modele a lu un sondage publie. R5 change
   la forme de la question, pas ce que les poids ont ingere. L'objection fatale du programme A
   reste entiere, exactement comme apres R1 et apres R4.
3. **Le mecanisme.** Je mesure que les exemples portent quatre cinquiemes de la marche. Je ne
   sais pas **pourquoi**. Trois candidats non departages : les exemples enseignent une variance
   par leurs vecteurs, tous non uniformes ; ils enseignent une longueur de reponse ; ils
   deplacent le modele hors du regime de reponse prudente. Departager demanderait un run avec
   des exemples a vecteurs quasi uniformes, qui n'a pas ete fait. [HYPOTHESE]
4. **La generalite.** Un seul fichier de poids, une seule quantification, une seule famille de
   gabarit, un seul jeu de trois exemples. Le chiffre 0,79 est celui de cette combinaison. Rien
   ne dit qu'il tient sur `gpt-oss-20b` sous harmony, ni sur `Qwen3-30B`, ni avec un autre
   triplet d'exemples.
5. **Le nombre d'exemples.** Trois exemples contre zero. La courbe entre les deux n'est pas
   mesuree, et je ne sais pas si un seul exemple suffirait, ni si dix feraient plus.
6. **Le choix des sequences d'arret.** `q4gab3` tourne avec l'union des arrets de `q4` et de
   `q4nogab`, decidee et ecrite avant le premier appel. L'essai a blanc mesure que cette union
   est **inerte** : sur la cellule sondee, les deux jeux d'arrets rendent le meme texte au
   caractere pres et le serveur s'arrete sur `eos` dans les deux cas. **Cette verification
   porte sur une cellule, pas sur 894.** Je ne peux pas exclure qu'un separateur ait ferme une
   generation ailleurs dans le run ; la trace ne conserve pas le motif d'arret, ce qui est un
   defaut du dispositif de R1 et non une omission de ce run.
7. **Les 20 rejets.** Ils sont hors du perimetre des mesures principales, donc ils n'en portent
   aucune. Mais ils ne sont pas rien : ce sont 20 cellules sur des items a 5 a 12 modalites ou
   le modele n'a pas su compter jusqu'a 100. S'ils avaient ete retenus, ils auraient
   vraisemblablement ete des distributions bruitees, donc plus indifferentes au camp, ce qui
   **abaisserait** legerement le facteur de `q4gab3` et rapprocherait H1 de la verite plutot
   que de l'en eloigner. [PROBABLE, non mesurable sans un run de plus]
8. **L'equivalence au sens strict.** H1 est tranchee sur la valeur ponctuelle, comme la page de
   plan l'ecrit. Aucun test d'equivalence de type TOST n'a ete fait, et l'intervalle de T2
   deborde la bande de 0,15. Un lecteur qui exige une equivalence par intervalle doit lire H1
   comme indecidable, pas comme vraie.
9. **La comparabilite des taux de rejet.** Seule la ligne « premiere tentative » se compare
   entre les quatre conditions. Les rejets finals de `q4gab3` ne se comparent a rien, puisque
   les trois autres conditions ont eu droit a une relance et pas lui.

---

## Questions ouvertes pour Simon

1. **Le registre de versions doit il compter les exemples ?** R5 mesure que le nombre
   d'exemples dans l'invite porte quatre cinquiemes de la dispersion entre protocoles, plus que
   l'ecart socle contre instruit. Faut il en faire un champ obligatoire du registre du
   programme A, au meme rang que le modele et la quantification, ou cela releve t il du
   protocole d'enquete et non de la version du systeme ?
2. **Faut il le run qui departage les trois mecanismes ?** Un quatrieme format, gabarit ChatML
   plus trois exemples **a vecteurs quasi uniformes**, coute 894 appels et une heure. Il dirait
   si ce sont les vecteurs disperses des exemples qui enseignent la dispersion, ou seulement
   leur presence. Sans lui, le « pourquoi » de ce rapport reste une hypothese.
3. **Quelle condition doit servir de reference dans le dossier ?** Quatre conditions donnent
   0,245, 0,566, 0,627 et 0,727 sur la meme quantite. Publier une seule valeur demande de
   choisir un protocole de reference, et ce choix n'est pas scientifique : il est
   conventionnel. Faut il publier une dispersion entre protocoles plutot qu'une valeur, comme
   `MODELE-DU-MONDE.md` section 12 le suggerait deja ?
4. **La relance doit elle etre supprimee partout ?** R5 la supprime et y perd 20 cellules, mais
   y gagne les 56 cellules que R4 devait retirer au critere 2. Le bilan semble favorable. Faut
   il rejouer R1 sans relance pour que les quatre conditions soient enfin sous le meme regime,
   ou vaut il mieux garder R1 fige et documenter l'ecart ?
5. **Une objection que je n'ai pas su lever.** Les exemples de R4 gardent la **forme** de la
   tache, un bloc de question suivi d'une distribution sur K lettres, et n'en gardent rien du
   contenu. Le critere 2 bis de R4 mesure qu'ils ne sont pas recopies. Mais ils montrent trois
   distributions **non uniformes**, et la quantite mesuree est precisement une dispersion. Est
   ce un enseignement de format, ou une fuite de la quantite mesuree dans l'invite ? Je penche
   pour le premier, parce que les trois vecteurs n'ont aucun rapport avec un axe politique,
   mais je ne peux pas le demontrer.
