# r7. Page de plan, brouillon : la dose reponse d'Olmo 3, ou l'ecrasement apparait dans l'entrainement

**Brouillon ecrit le 2026-09-09 entre 13:35 et 14:30 CEST. Aucun appel de modele n'a ete
fait pendant cette seance.** Le seul acces reseau est la lecture de l'API publique de
Hugging Face, la lecture de la documentation d'infini-gram, le clonage du depot llama.cpp et
le telechargement de quatre jeux de poids publics sous licence Apache 2.0. Rien du referent
humain, aucune microdonnee, aucun libelle d'item n'est sorti de la machine.

**Statut : brouillon, non depose.** La regle du dossier depuis
`DECISIONS-CONSOLIDEES-2026-09-09.md` est qu'aucune page ne se dit « preenregistree » sans
depot hors machine. Celle ci se decrit comme « plan ecrit avant le run, horodate sur
machine, non depose », et le restera tant qu'elle n'aura pas d'enregistrement OSF, comme
R5 en a un (https://osf.io/3r6zg/). Elle attend aussi l'arbitrage d'Amir sur les cinq
points listes en section 12.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

Provenance des poids, empreintes, commandes et journal de conversion :
`~/Library/Caches/popsim-modeles/PROVENANCE-r7.md`, ecrit dans la meme seance.

---

## 1. La question, en une phrase

A format d'invite tenu fixe, **a quelle etape de l'entrainement post preentrainement l'ecart
entre camps decrit s'ecrase t il**, quand on parcourt les quatre points de controle publies
d'Olmo 3 en 7B : Base, SFT, DPO, RLVR ?

---

## 2. Pourquoi cette page existe

### 2.1 Ce que R4 a trouve, et le trou qu'il laisse

R4 a compare un socle et un instruit apparies, `Qwen3-4B-Base` et `Qwen3-4B`, sous le meme
format de completion a trois exemples. Le resultat, sur le facteur H2b (ecart signe entre
camps, 79 items orientes, demandeur journaliste) :

| condition | poids | facteur, journaliste | facteur, adversaire |
|---|---|---|---|
| `q4base` | `Qwen3-4B-Base`, socle | **0,566** | 0,440 |
| `q4hyb` | `Qwen3-4B`, l'instruit apparie du socle | **0,262** | 0,202 |
| `q4nogab` | `Qwen3-4B-Instruct-2507`, instruit non apparie | 0,727 | 0,859 |

[MESURE, `resultats/r1-h2-ecart-r4.csv`]

**Sur la seule paire apparie du dossier, l'alignement divise par deux l'ecart entre camps
decrit, a format tenu fixe.** C'est le fait le plus proche d'une these causale que R4
produise. Mais il est fait d'un seul point de depart et d'un seul point d'arrivee : entre
les deux, Qwen ne publie rien. On ne sait donc pas si l'ecrasement est l'oeuvre du reglage
supervise, de l'alignement par preferences, ou de l'apprentissage par renforcement, ni si la
trajectoire est monotone.

**Olmo 3 est le seul dispositif public qui permet de le savoir a zero euro.** Ai2 publie les
quatre points de controle separement, en 7B, tous sous licence Apache 2.0, et chacun declare
son parent dans le champ `base_model` de sa carte : `Olmo-3-1025-7B` puis
`Olmo-3-7B-Instruct-SFT` puis `Olmo-3-7B-Instruct-DPO` puis `Olmo-3-7B-Instruct`.
[CONFIRME, API Hugging Face, consultee le 2026-09-09] La chaine est donc apparie par
construction, ce qui est exactement ce que `a27` section 4.4 reproche a notre paire Qwen
d'origine.

### 2.2 Ce que cette page peut trancher

- **A quelle etape** la marche se produit, si elle se produit.
- **Si la trajectoire est monotone** ou non. Une chute a SFT suivie d'une remontee partielle
  ne se lit dans aucun dispositif a deux points.
- **Si l'ecrasement est un fait de l'alignement ou un fait de Qwen.** Deux familles
  independantes qui montrent la meme marche valent beaucoup plus qu'une.

### 2.3 Ce qu'elle ne peut pas trancher, et qu'aucune phrase du rapport ne dira

- **Elle ne dit rien du mecanisme interne.** Aucun sondage d'activations, aucune
  intervention causale sur les poids. Le pilier « sondage des activations » est mort dans
  `DECISIONS-CONSOLIDEES-2026-09-09.md` et ne revient pas ici.
- **Elle ne dit pas que l'alignement « censure ».** R5 a deja ecarte la these « le mode
  assistant censure » sur Qwen ; une marche a une etape donnee ne la ressuscite pas.
- **Elle ne separe pas les donnees de la methode.** SFT, DPO et RLVR different a la fois par
  l'algorithme et par le corpus de reglage. Ce que la courbe mesure est l'effet du couple,
  jamais de l'algorithme seul.
- **Elle ne se generalise pas au 32B sans le mesurer.** Le 32B existe et se convertit ; il
  n'est pas dans cette page, et la conclusion sera ecrite en 7B.
- **Elle ne remplace pas un test de contamination.** La section 10 dit pourquoi le test
  disponible ne porte pas sur le bon corpus.

---

## 3. Les quatre conditions

| cle | depot Hugging Face | etape | parent declare |
|---|---|---|---|
| `olmo3base` | `allenai/Olmo-3-1025-7B` | preentrainement, socle | aucun |
| `olmo3sft` | `allenai/Olmo-3-7B-Instruct-SFT` | reglage supervise | `allenai/Olmo-3-1025-7B` |
| `olmo3dpo` | `allenai/Olmo-3-7B-Instruct-DPO` | preferences, DPO | `allenai/Olmo-3-7B-Instruct-SFT` |
| `olmo3rlvr` | `allenai/Olmo-3-7B-Instruct` | RLVR, modele final | `allenai/Olmo-3-7B-Instruct-DPO` |

**La branche retenue est Instruct, pas Think.** Ai2 publie deux branches paralleles a partir
du meme socle, Instruct et Think. Think produit un bloc de raisonnement avant sa reponse,
ce qui change la longueur de generation et donc le budget de jetons, et introduit une
variable de plus que la page ne controle pas. La branche Think est **declaree ici comme
extension possible et ne sera pas repechee apres coup si Instruct ne donne rien.**

**Les 32B ne sont pas dans cette page.** Meme regle : declares comme extension, jamais
repeches.

---

## 4. Le format d'invite, fixe, et pourquoi celui la

**Les quatre conditions emploient la completion a trois exemples, sans gabarit de
conversation, dans la forme figee par `r4-preenregistrement.md` section 3.2, au caractere
pres.** C'est le format des conditions `q4nogab` et `q4base` de R4.

**La justification tient en trois pas.**

1. **Le socle n'a pas de gabarit de conversation.** Il n'existe aucun gabarit ChatML
   applicable a `Olmo-3-1025-7B` : sa carte ne declare pas de `chat_template`, alors que les
   trois autres en declarent un. [CONFIRME, champ `config.tokenizer_config` de l'API
   Hugging Face, 2026-09-09] Toute condition qui appliquerait un gabarit aux trois etapes
   alignees et pas au socle melangerait l'effet des poids et l'effet du format.
2. **Le format d'invite porte plus que les poids, et le chiffre est chez nous.** R4 mesure
   que changer de format sans toucher un poids deplace la mesure de +0,48 [+0,29 ; +0,68],
   plus que l'ecart total socle contre instruit, +0,32 [+0,13 ; +0,52]. [MESURE,
   `resultats/r4-resultats.md`] R5 decompose ce +0,48 : les exemples en portent +0,382
   [+0,200 ; +0,578], le gabarit +0,101 [+0,017 ; +0,183]. [MESURE, `r5-contrastes.csv`]
   Un contraste d'etapes lu sous deux formats differents serait donc domine par le format.
3. **Le contraste devient apparie.** Les quatre conditions partagent le fichier d'invite au
   caractere pres, les memes 149 items, les memes trois camps, les memes deux demandeurs,
   les memes parametres d'appel. **La seule chose qui bouge entre deux lignes voisines de la
   courbe est un jeu de poids, et une etape d'entrainement les separe.** C'est le sens de
   « dose reponse » : la dose est l'etape, la reponse est le facteur H2b.

**Le prix a payer, ecrit ici pour ne pas etre decouvert apres.** Faire tourner `Olmo-3-7B-Instruct`
en completion nue, sans son gabarit, n'est **pas** la maniere dont ce modele s'emploie en
production. Le chiffre de la condition `olmo3rlvr` ne dit donc pas « ce qu'un utilisateur
d'Olmo 3 obtiendrait ». Il dit « ce que les poids de l'etape RLVR font, format tenu fixe ».
C'est le prix de l'appariement, et il est le meme que celui que R4 a paye pour `q4nogab`.
Une condition supplementaire sous gabarit, pour les trois etapes alignees seulement, est
declaree en section 11 comme extension conditionnelle, avec sa propre famille de Holm.

**Sequences d'arret**, identiques a R4 dans leur role, adaptees au vocabulaire d'Olmo 3 :
`\n----`, `\nSurvey question`, `<|endoftext|>`, `<|im_end|>`, `<|im_start|>`. Le jeton de
fin declare par les quatre depots est `<|endoftext|>`. [CONFIRME, API Hugging Face]

---

## 5. Le plan de cellules, et les parametres d'appel

**Identiques a R1, R4 et R5, sans exception.**

| facteur | niveaux | n |
|---|---|---|
| item | les 149 items du GSS de `a2` | 149 |
| camp decrit | gauche (417 personnes), centre (303), droite (332) | 3 |
| identite du demandeur | journaliste neutre ; membre du camp adverse | 2 |
| condition | `olmo3base`, `olmo3sft`, `olmo3dpo`, `olmo3rlvr` | 4 |

**894 cellules par condition, 3 576 appels en tout, un appel par cellule.** Ordre
d'execution : par condition (un serveur a la fois), puis par camp, puis par identite, puis
par item, pour le cache de prefixe.

Parametres : `temperature` 0, `top_k` 1, `n_predict` 150, `cache_prompt` true, un seul flux,
`-c 4096 -np 1 -ngl 999 --cache-reuse 256 --no-webui -fa on --cache-type-k q8_0
--cache-type-v q8_0`. Moteur `MoteurR1` de `analyses/r1_oracle_camps.py`, importe, jamais
recopie. `VERSION_PROMPT` vaut `r7-c3` : meme construction d'invite que `r4-c3`, index de
reprise separe.

**Relance : supprimee, comme en R5.** Un echec de premiere tentative est un rejet, jamais
rejoue, par `--sans-relance`. Le taux de rejet des quatre conditions se publie en tete du
rapport. La raison est mesuree : en completion, la relance de R1 recopie son exemple chiffre
45 fois sur 45. [MESURE, `r4-resultats.md` section 3.1]

**Referent humain** : `data/traces/r1-distributions-reelles.csv`, empreinte sha256 verifiee
identique a celle du lancement de R1 avant tout appel. Plancher de bruit : les memes 1 052
personnes reinterrogees a deux semaines.

---

## 6. Les mesures et la quantite principale

Definitions **exactement** celles de `r1-preenregistrement.md` section 5, sans une
modification. Calculs par `analyses/r1_evaluer.py`, appele sans modification, avec
`--suffixe r7`.

**Quantite principale, une seule, declaree ici :** le facteur H2b, ecart signe entre camps
decrit divise par l'ecart reel, `position(droite) - position(gauche)`, moyenne sur les **79
items orientes** de `a37`, demandeur **journaliste**. Toutes les autres sont secondaires et
seront publiees, jamais promues.

Quantites secondaires publiees quoi qu'il arrive : le meme facteur pour le demandeur
adversaire ; le meme facteur sur les 65 items retenus stricts ; le facteur H2a (ecart non
signe, distance de variation totale entre camps, 149 items) ; le ratio H1 de dispersion
interne par camp ; l'erreur TV(decrit, reel) en part du plancher humain ; le taux de rejet.

---

## 7. Les hypotheses, ecrites avant tout appel

Notons `F(e)` la quantite principale a l'etape `e`, avec `e` dans {base, sft, dpo, rlvr}.

- **H1, il se passe quelque chose.** Au moins un contraste apparie entre deux etapes
  voisines est significatif apres Holm dans la famille F1.
- **H2, l'alignement ecrase.** `F(rlvr) < F(base)`, contraste apparie par item.
  C'est la transposition directe du seul fait apparie de R4, ou `q4hyb` (0,262) tombe sous
  `q4base` (0,566).
- **H3, la marche est a SFT.** `F(sft) < F(base)` est le plus grand des trois contrastes
  entre etapes voisines en valeur absolue.
- **H4, la courbe est non monotone.** `F(dpo) > F(sft)` **et** `F(rlvr) > F(sft)`, c'est a
  dire que le minimum de la courbe est atteint a l'etape SFT et non a la fin.

### Le pari, et ce qu'il coute

**Pari du dossier : H1, H2, H3 et H4 sont toutes vraies. La courbe descend brutalement a
SFT, puis remonte partiellement a DPO et se stabilise ou remonte encore a RLVR. Le minimum
est a SFT.**

**Pourquoi ce pari peut couter.** Il est plus fort et plus refutable que son contraire de
trois manieres.

1. **Il predit une forme, pas un signe.** « L'alignement ecrase » (H2) a une chance sur deux
   d'etre juste par hasard. « Le minimum est exactement a SFT parmi quatre positions
   possibles » n'en a qu'une sur quatre si la position est tiree au sort, et le pari les
   cumule.
2. **Il parie contre la lecture confortable.** La facon naturelle de raconter « l'alignement
   ecrase » est une degradation qui **s'accumule** a chaque tour, donc une courbe monotone
   decroissante, base > sft > dpo > rlvr. C'est la forme que tout le monde attend et qui se
   resume en une phrase. Le pari dit l'inverse a partir de SFT. **Si la courbe est monotone
   decroissante, H4 tombe, et il faudra l'ecrire en tete du rapport.** Aucun element du
   dossier ne soutient aujourd'hui la non monotonie : `a15` ne porte pas sur des etapes
   d'entrainement mais sur l'axe de segmentation, et R4 n'a que deux points. **H4 est donc
   un pari a decouvert, et c'est exactement pour cela qu'il est ecrit ici et pas apres.**
3. **Il parie contre son propre appareil de mesure.** Si SFT est le minimum et que le taux
   de rejet de SFT est aussi le plus haut des quatre, l'explication triviale sera « SFT
   suit mal le format » et non « SFT ecrase ». Le critere de chute 3 est ecrit exactement
   pour cela, et il peut tuer H3 et H4 a lui seul.

**Contre pari, ecrit ici pour qu'on ne puisse pas le nier apres :** la lecture concurrente
est monotone decroissante, chaque etape retirant un peu d'ecart. Si c'est ce que la courbe
montre, le rapport dira que le pari du dossier a echoue, et la these « l'ecrasement est un
fait du reglage supervise, que les etapes suivantes corrigent en partie » sera abandonnee,
pas amendee.

**Une raison independante de douter, deja mesuree.** Dans R4, `q4base` (0,566) est **au
dessus** de `q4hyb` (0,262) mais **en dessous** de `q4nogab` (0,727). Le socle n'est donc
pas systematiquement le point haut de sa famille. Si `olmo3base` sort bas et que les etapes
alignees montent, H2 tombe des la premiere ligne du tableau.

---

## 8. Les tests, les familles, la correction

- **Unite de reechantillonnage : l'item.** Bootstrap sur les items, 2 000 tirages,
  percentiles a 2,5 et 97,5.
- **Test principal** : permutation de signe **appariee par item** sur la difference du
  facteur par item entre deux conditions, 20 000 tirages, estimateur de Phipson et Smyth
  `(b + 1) / (m + 1)`. Jamais une comparaison d'intervalles de confiance a l'oeil.
- **Perimetre d'un contraste** : les items valides dans **les deux** conditions comparees.
  Un item rejete d'un cote sort du contraste des deux cotes, regle de R5 inchangee.

**Familles de Holm, jamais fusionnees.**

| famille | contenu | nombre de tests |
|---|---|---|
| **F1**, etapes voisines | base contre sft, sft contre dpo, dpo contre rlvr, sur la quantite principale | 3 |
| **F2**, H2 et bornes | base contre rlvr, base contre dpo, sft contre rlvr, sur la quantite principale | 3 |
| **F3**, le facteur contre 1 | les quatre etapes contre 1, sur la quantite principale | 4 |
| **F4**, replication demandeur adversaire | les trois contrastes de F1, demandeur adversaire | 3 |
| **F5**, H1 dispersion interne | ratio de dispersion contre 1, 3 camps x 4 etapes | 12 |

Seuil 0,05 apres Holm **dans** la famille. Bande de nullite pratique : un rapport
significatif dans [0,95 ; 1,05] est declare **nul en pratique**, comme en R1.

**H4 se teste comme une conjonction, pas comme un dessin.** `F(dpo) - F(sft) > 0` et
`F(rlvr) - F(sft) > 0`, les deux dans F1 et F2, les deux devant survivre a Holm. Une figure
qui « a l'air non monotone » sans ces deux tests ne vaut rien et ne sera pas publiee comme
resultat.

**Aucun sous ensemble d'items choisi apres coup.** Les seuls perimetres autorises sont ceux
de `a37`, `oriente` (79) et `retenu_strict` (65), et les 149 items complets.

---

## 9. Les criteres de chute, ecrits pour pouvoir perdre

Le run est jete, en entier ou pour une condition, si l'une de ces conditions est remplie.

1. **Plus de 25 pour cent de rejets de format pour une condition.** Le taux est publie des
   quatre cotes quoi qu'il arrive, denominateurs compris. `a27` mesure chez les auteurs de
   2607.25292 que `OLMo-2-1124-7B-SFT` echoue a l'extraction dans 6,67 pour cent des cas et
   `OLMo-2-1124-7B-DPO` dans 8,25 pour cent, **les deux pires de leurs dix points de
   controle**, socles compris. [CONFIRME, `a27` section 4.4] **Ce critere est donc le plus
   menacant de la page**, et il l'est de facon dissymetrique, precisement sur les etapes ou
   le pari attend la marche.
2. **La sonde des 60 premieres cellules**, regle de R4 inchangee. Au dessus de 0,50 de rejet
   sur les 60 premieres, la condition est arretee la, son taux est publie, et le creneau
   passe a la suivante. Une condition qui echoue n'emporte pas les autres.
3. **Le taux de rejet explique la marche.** Nouveau critere, propre a R7. Si l'ordre des
   quatre conditions sur la quantite principale est le meme que leur ordre sur le taux de
   rejet, avec un rho de Spearman superieur a 0,8 en valeur absolue, **la courbe n'est pas
   interpretee comme une dose reponse** : elle est publiee comme un artefact possible de
   conformite de format, et le rapport le dit dans sa premiere ligne.
4. **Recopie des exemples a trois coups**, regle 2 bis de R4 inchangee. Pour K >= 3, une
   distribution egale au vecteur de l'exemple de meme K sort ; au dela de 5 pour cent des
   cellules d'une condition, le protocole est declare contaminant pour cette condition et
   elle n'est pas interpretee. Pour K = 2 le vecteur [43, 57] reste, et son taux est publie
   a cote du taux de base.
5. **Distribution constante d'un camp a l'autre** dans plus de 90 pour cent des items : la
   condition ignore le camp, et c'est ce fait la qu'on publie.
6. **Plancher humain non atteint** : le facteur entre vagues 1 et 2 des memes humains doit
   tomber dans [0,85 ; 1,15]. Il vaut 1,009 dans R1.
7. **Referent modifie** : `data/traces/r1-distributions-reelles.csv` doit avoir la meme
   empreinte sha256 qu'au lancement de R1. Sinon rien n'est publie.
8. **Deux serveurs a la fois** : si `pgrep -x llama-server` rend plus d'un processus pendant
   le run, le run est jete.
9. **Quantification non identique.** Les quatre fichiers GGUF doivent porter la meme
   quantification et etre issus du meme commit de `convert_hf_to_gguf.py`. Une seule
   difference de procede entre deux etapes se lirait comme une difference de poids, et c'est
   la limite exacte que `PROVENANCE-r4.md` section 3 a du ecrire pour Qwen. Ici elle est
   evitee par construction, et le commit est inscrit dans `PROVENANCE-r7.md`.
10. **Tokeniseur different entre deux etapes.** Les quatre depots ne servent pas le meme
    fichier `tokenizer.json` : Base a le sien, SFT le sien, DPO et RLVR partagent le meme
    blob git. [MESURE, API Hugging Face, `paths-info`, 2026-09-09] Si le nombre de jetons de
    l'invite differe entre deux conditions de plus de 2 pour cent, la difference est publiee
    avec la courbe et le contraste concerne est marque comme non strictement apparie.

---

## 10. Controle de contamination : le comptage Dolma par infini-gram

**A preparer, pas a executer.** Cette section fixe le protocole ; aucun appel a infini-gram
n'a ete fait sur un libelle d'item pendant cette seance.

### 10.1 Ce que ce controle veut savoir

Un modele peut decrire un camp correctement parce qu'il a lu le GSS, pas parce qu'il modelise
une population. Le comptage repond a une question etroite et verifiable : **les libelles de
nos 149 items apparaissent ils dans le corpus de preentrainement, et a quelle frequence ?**
Le patron est celui de Roberts, deja retenu dans `DECISIONS-CONSOLIDEES-2026-09-09.md` comme
remplacant du pilier « sondage des activations ».

### 10.2 L'outil, verifie

Point d'acces : `https://api.infini-gram.io/`, POST, corps JSON
`{"index": ..., "query_type": "count", "query": ...}`. La reponse rend `count`, `approx`,
`token_ids`, `tokens` et `latency`. [CONFIRME, documentation officielle et essai reel du
2026-09-09 : la requete `public library` sur `v4_dolma-v1_7_llama` rend
`count = 1 525 681`, `approx = false`, 55 ms.] [MESURE]

Index utiles, tous en tokenisation Llama-2 :

| identifiant | corpus | jetons |
|---|---|---|
| `v4_dolma-v1_7_llama` | Dolma v1.7 | 2 604 642 372 173 |
| `v4_olmo-mix-1124_llama` | OLMo-mix-1124 | 4 575 475 702 047 |
| `v4_olmo-2-1124-13b-instruct_llama` | melange complet d'OLMo 2 13B Instruct | 4 610 749 614 285 |
| `v4_dclm-baseline_llama` | DCLM-baseline | 4 341 627 197 578 |

[CONFIRME, documentation infini-gram, 2026-09-09]

### 10.3 La limite, et elle est serieuse

**Il n'existe aucun index infini-gram du corpus d'Olmo 3.** Les identifiants
`v4_dolma-v3_llama`, `v4_dolma3_llama` et `v4_olmo-3-1025-7b_llama` renvoient tous
`Invalid index`. [MESURE, essai direct du 2026-09-09] Le service s'arrete a Dolma v1.6 et
v1.7 et aux melanges d'OLMo 2.

Consequence, a ecrire dans le rapport et jamais a taire : **le comptage sera fait sur un
corpus voisin, pas sur le corpus d'Olmo 3.** Il fournit une borne inferieure plausible de
presence, pas une mesure de contamination du modele teste. Deux usages restent legitimes,
et un seul est interdit.

- Legitime : classer les 149 items du plus au moins present dans Dolma v1.7, puis regarder
  si le contraste entre etapes est plus grand sur les items rares que sur les items
  frequents. C'est un test **interne** a notre courbe, qui n'a pas besoin que l'index soit
  celui d'Olmo 3, seulement que la frequence d'un libelle sur le web soit correlee d'un
  corpus a l'autre. [PROBABLE, non demontre]
- Legitime : publier le comptage tel quel comme information de provenance des items.
- **Interdit** : ecrire ou laisser entendre que ce comptage montre que Olmo 3 a vu, ou n'a
  pas vu, un item. Il ne le montre pas.

### 10.4 Le protocole, fige

1. **Ce qui est interroge** : le libelle de question de chacun des 149 items, tel quel,
   plus la liste des modalites concatenee, en deux requetes separees par item. Ce sont des
   libelles publics du GSS, pas des microdonnees ; aucune reponse de personne, aucun
   identifiant, aucun chiffre de notre referent ne part.
2. **Une requete de calibrage par item** : les cinq premiers mots du libelle, pour distinguer
   « le libelle exact n'est pas dans le corpus » de « le sujet n'est pas dans le corpus ».
3. **Index** : les quatre du tableau ci dessus, dans cet ordre, pour que la comparaison entre
   index serve de controle a elle meme.
4. **Volume** : 149 items x 3 requetes x 4 index = 1 788 requetes. A 55 ms mesurees, moins
   de deux minutes de service, mais avec un delai de 200 ms entre requetes et une reprise
   sur trace, soit environ six minutes.
5. **Sorties** : `resultats/r7-contamination-comptages.csv` (item, index, requete, count,
   approx, latence), `resultats/r7-contamination-terciles.csv` (les 149 items ranges en
   terciles de presence).
6. **Test declare ici** : le contraste `base` contre `sft` sur la quantite principale est
   calcule separement dans le tercile le plus present et le tercile le moins present. Un
   seul test, une seule comparaison, hors des familles F1 a F5, dans une famille F6 a lui
   seul. **Aucun autre decoupage.**
7. **Le service peut ne pas repondre.** La documentation demande une gestion d'exception et
   des reprises. Le script attend, ne relance pas plus de trois fois, et une requete
   definitivement echouee est publiee comme manquante, jamais imputee.

---

## 11. Le cout en temps, et la quantification

### 11.1 La quantification retenue : Q8_0 pour les quatre

**Q8_0, identique pour les quatre conditions**, produite par le meme
`convert_hf_to_gguf.py --outtype q8_0`, au meme commit.

Pourquoi Q8_0 et pas Q4_K_M :

- **La memoire le permet.** Un Olmo 3 7B en Q8_0 pese environ 7,8 Gio. La machine a 32 Gio
  de memoire unifiee, et un seul serveur tourne a la fois, a 4 096 jetons de contexte.
  Le rapport entre la memoire disponible et la taille du fichier est d'environ quatre.
- **Le bruit de quantification est la variable parasite la plus dangereuse ici.** La page
  mesure des ecarts entre etapes qui, chez Qwen, valaient 0,30 de facteur. Q4_K_M perd plus
  d'information que Q8_0, et rien ne garantit qu'il en perde autant sur quatre jeux de poids
  differents. Q8_0 rapproche les quatre conditions du calcul en pleine precision et rend la
  perte plus homogene.
- **Un seul procede, un seul commit, aucune matrice d'importance.** C'est ce qui manquait a
  R4 : `PROVENANCE-r4.md` section 3 a du ecrire qu'une difference de procede de
  quantification entre le socle et l'instruit se lirait comme une difference de poids. Ici
  les quatre fichiers sortent de la meme commande, appliquee a quatre dossiers de poids.

**Repli, declare ici et pas apres :** si une condition ne se charge pas en Q8_0 ou si le
debit tombe sous 5 jetons par seconde en decodage, **les quatre** sont refaits en Q4_K_M,
jamais une seule. Une courbe a quantifications melangees n'est pas une courbe.

### 11.2 Le temps, extrapole des mesures du dossier

Ancrages mesures sur cette machine :

| mesure | valeur | source |
|---|---|---|
| 894 cellules, Qwen3-4B Q4_K_M, completion a trois exemples | 951,2 s et 945,2 s | `data/traces/r4-resume.json` [MESURE] |
| decodage, Qwen3-4B en 4 bits | 38,4 jetons par seconde | `a3` [MESURE] |
| decodage, Llama 3.1 8B en 4 bits | 13,1 jetons par seconde | `a3` [MESURE] |
| perte au bridage thermique, decodage sur charge continue | 18,2 pour cent | `a4` [MESURE] |
| perte au bridage thermique, appels par heure | 39,2 pour cent | `a4` [MESURE] |

Le decodage local est domine par la lecture des poids. Deux extrapolations encadrantes, pour
un fichier de 7,8 Gio contre 2,3 Gio pour le Qwen3-4B Q4_K_M :

- **borne basse**, mise a l'echelle par les octets a partir du 4B : 951 s x 3,3 soit environ
  **52 minutes par condition** ;
- **borne haute**, mise a l'echelle par les octets a partir de l'ancrage 8B, qui est plus
  pessimiste que le simple rapport des tailles : environ **80 minutes par condition**.

**Quatre conditions : 3 h 30 a 5 h 20 de machine.** Avec le bridage thermique de `a4` sur une
charge continue de plusieurs heures, la fourchette de travail est **4 h a 7 h**, plus environ
une minute de chargement par condition. Cela tient dans une nuit, une seule, sans rien
d'autre sur le GPU.

**Zero euro.** Aucun appel payant, aucun jeton d'API, rien ne sort de la machine pendant le
run.

### 11.3 Extensions conditionnelles, declarees et non repechables

Chacune n'existe que si Amir la valide **avant** le run, et chacune porte sa propre famille
de Holm.

- **E1, le gabarit.** Les trois etapes alignees sous leur gabarit natif, 2 682 appels de
  plus, environ 3 h. Mesure la marche de format sur Olmo 3, replication de R5 hors famille
  Qwen.
- **E2, la branche Think.** Les trois etapes Think, 2 682 appels, plus lentes car la
  generation est plus longue.
- **E3, le 32B.** Quatre conditions en 32B, environ 34 Gio par fichier en Q8_0, donc Q4_K_M
  obligatoire et une courbe qui ne se compare pas a celle du 7B.

---

## 12. Ce qui est deja fait, et ce qui reste

| | etat au 2026-09-09 |
|---|---|
| identification des quatre depots par l'API Hugging Face | **fait**, `PROVENANCE-r7.md` |
| telechargement des quatre en safetensors | **fait**, tailles et empreintes journalisees |
| conversion en GGUF Q8_0, meme commit pour les quatre | **fait**, journal dans le cache |
| chargement de controle par `llama-server` | **fait**, dix secondes chacun, sequentiel |
| `analyses/r7_dose_reponse.py` | **a ecrire** : registre des quatre cles, import de `MoteurR1`, `--sans-relance`, sonde des 60 cellules, reprise sur trace |
| essai a moteur factice, hors ligne | **a faire** avant tout appel |
| depot de cette page hors machine | **a faire**, sans quoi elle reste un brouillon |
| comptage infini-gram | **a preparer**, section 10, jamais avant le depot |

**Les cinq points qu'Amir doit trancher.**

1. Branche **Instruct** et non Think : d'accord ou non.
2. **7B seulement** cette nuit, 32B jamais dans cette page : d'accord ou non.
3. Quantification **Q8_0** pour les quatre, avec le repli tout Q4_K_M : d'accord ou non.
4. **Depot OSF de cette page avant le run**, comme R5 : oui ou non. Si non, le rapport dira
   « plan ecrit avant le run, horodate sur machine, non depose ».
5. Les extensions E1, E2, E3 : lesquelles sont validees maintenant, sachant qu'aucune ne
   pourra etre repechee apres avoir vu la courbe.

---

## Ce que je n'ai pas pu verifier

1. **Le contenu du rapport technique d'Olmo 3**, arXiv 2512.13961, n'a pas ete lu dans cette
   seance. Les etapes sont etablies par le champ `base_model` des cartes, pas par le texte du
   rapport. Il reste possible que la chaine reelle comporte des etapes intermediaires non
   publiees, ou que « Instruct » agrege plusieurs passes de RLVR.
2. **Que l'etape finale soit bien du RLVR et non un autre algorithme de renforcement.**
   `verif-fournisseurs-2026-09-09.md` point 4 l'ecrit, sur la foi des cartes de modele ;
   le nom du depot final est `Olmo-3-7B-Instruct`, sans mention d'algorithme. Le rapport
   ecrira « etape finale » et non « RLVR » tant que ce point n'est pas verifie dans
   2512.13961.
3. ~~La longueur de contexte d'Olmo 3.~~ **Levee dans cette seance.** Le point 14 de
   `verif-fournisseurs-2026-09-09.md` la donnait pour non verifiee ; le `config.json` des
   quatre depots donne `max_position_embeddings` 65 536, un `rope_scaling` YARN de facteur
   8 sur une longueur d'origine de 8 192, et une fenetre glissante de 4 096 sur toutes les
   couches sauf une sur quatre. [MESURE, `config.json` telecharge, 2026-09-09] Sans
   consequence ici, l'invite fait environ 320 jetons et le serveur tourne a 4 096, ce qui
   tombe exactement sur la fenetre glissante native.
4. **Le debit reel du 7B en Q8_0 sur cette machine.** Aucune mesure de debit n'a ete faite
   dans cette seance ; les chiffres de la section 11.2 sont une extrapolation de mesures
   faites sur d'autres modeles, et ils peuvent etre faux d'un facteur deux.
5. **Le taux de rejet de format d'Olmo 3 sous notre invite.** Les chiffres de `a27` portent
   sur OLMo 2, pas sur Olmo 3, et sur l'invite de 2607.25292, pas sur la notre.
6. **La correlation entre la frequence d'un libelle dans Dolma v1.7 et sa frequence dans le
   corpus d'Olmo 3.** Elle est supposee, jamais mesuree, et c'est ce qui rend la section 10
   un controle faible.
7. **Que Ai2 n'ait pas mis en ligne un index infini-gram d'Olmo 3 ailleurs** que sur le
   service public interroge. Trois identifiants plausibles ont ete essayes, pas davantage.

---

## Questions ouvertes pour Simon

1. **La dose reponse sur les etapes publiees d'un modele ouvert a t elle deja ete faite sur
   un referent humain, a format d'invite tenu fixe ?** 2607.25292 fait tourner des points de
   controle OLMo 2 SFT et DPO, mais sur une tache de generation de population, pas sur la
   description d'un camp, et sans courbe d'etapes. Si quelqu'un l'a deja publiee, la page
   n'a plus lieu d'etre sous cette forme et devient une replication.
2. **Le contraste apparie par item entre deux points de controle d'une meme lignee est il
   le bon test**, ou faut il un modele a effets aleatoires sur les items ? La permutation de
   signe appariee est ce que le dossier emploie depuis R1 ; un statisticien de metier
   dirait peut etre autre chose, et il vaut mieux l'entendre avant le run qu'apres.
3. **Le prix de la completion nue sur un modele final est il acceptable pour un referee ?**
   La page l'assume au nom de l'appariement. Un relecteur peut objecter que la condition
   `olmo3rlvr` ne correspond a aucun usage reel. L'extension E1 est la reponse prevue ;
   faut il la rendre obligatoire plutot que conditionnelle ?
4. **Le controle de contamination sur un corpus voisin vaut il mieux que pas de controle ?**
   Il est faible, la section 10.3 le dit. Vaut il mieux le publier avec ses limites, ou ne
   rien publier et ecrire que le controle est impossible faute d'index ?
5. **Son institution peut elle donner acces a un GPU pour refaire les quatre etapes en
   pleine precision ?** Ce serait la seule facon de retirer completement la quantification
   de l'equation, et cela ouvrirait aussi le balayage alpha de la table 11 de 2607.25292,
   ferme a une machine de 32 Gio.
