# R2. La comparaison appariee sur les gens rares, en regime severe

Rapport du 8 septembre 2026, **ecrit avant le run**, pendant que la machine est occupee
par R1. Il execute le **verrou 1** de `MODELE-DU-MONDE.md` section 10.5 :
*« la comparaison appariee du rappel des minorites, restreinte aux raretes stables : un
run en regime severe sur gpt-oss-20b, famille retiree de l'invite [...] ; une nuit »*.

**Etat au moment ou ces lignes sont ecrites : zero appel de modele de langage a ete fait
par cet agent.** Aucun `llama-server` n'a ete lance. Le script est ecrit, verifie hors
ligne sur 33 controles, l'evaluateur est teste sur la trace C3F existante et sur une trace
synthetique, et le fichier `data/traces/r2-pret` est ecrit pour que la file de nuit lance
le run apres R1.

**Preenregistre.** La famille d'hypotheses, les seuils, les planchers et les criteres de
chute sont dans `resultats/r2-preenregistrement.md`, **horodate du 8 septembre 2026 a
22:05:00 CEST**, ecrit avant le moindre appel, et ce fichier n'est plus modifie. Il est
resume en section 2 et il fait foi contre ce rapport en cas de divergence.

Deux scripts nouveaux, `analyses/r2_rares_apparie.py` (le run) et `analyses/r2_evaluer.py`
(l'evaluation). **Aucun script existant n'a ete modifie** ; `a2_baselines_gss`,
`a5_agents_locaux_gss`, `a5_evaluer`, `a28_commun`, `a33_commun`, `a34_commun`,
`a35_commun`, `a35_familles`, `a41_commun`, `a42_commun` et `a44_commun` sont importes
tels quels, memes graines, memes plis, memes 150 personnes, memes 58 items de famille.

---

## Reponse en une ligne, telle qu'elle peut etre donnee ce soir

**Le dispositif est pret et il n'a rien mesure.** Ce qui est etabli ce soir tient en trois
points. Un, la case que le verrou 1 demande, « raretes stables x 58 items de famille x
regime severe », **n'existait dans aucun fichier de `resultats/`** : a42 mesure les
raretes stables sur les 149 items hors regime severe, a41 mesure le regime severe sur les
58 items toutes raretes confondues. Deux, l'evaluateur **reproduit a 0,0007 pres les six
contrastes d'exactitude de a41 section 5** sur la trace C3F existante, ce qui valide la
chaine de mesure avant qu'elle serve. Trois, **la mesure sera peu puissante** : sur les
60 personnes de la trace Qwen3-4B il n'y a que **31 cellules rares stables** dans les
58 items, et aucun contraste de la famille primaire ne franchit Holm sur ce perimetre.
Sur 150 personnes on attend environ 78 cellules. **C'est la limite principale de R2, elle
est connue avant le run, et elle est arithmetique, pas methodologique.**

---

## 1. Le registre des modeles

| | gpt-oss-20b | Qwen3-30B-A3B-Instruct-2507 | Qwen3-4B-Instruct-2507 |
|---|---|---|---|
| Role dans R2 | **primaire** | repli documente | trace de reference existante |
| Fichier | `data/modeles/gguf/gpt-oss-20b-MXFP4.gguf` | `...Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf` | `...Qwen3-4B-Instruct-2507-Q4_K_M.gguf` |
| Taille sur disque | **11,3 Gio** [MESURE] | 17,3 Gio [MESURE] | 2,3 Gio [MESURE] |
| Quantification | MXFP4 | Q4_K_M | Q4_K_M |
| Gabarit | **harmony**, a3 section 4.5 | Qwen, a5 section 2 | Qwen |
| Coupure **publiee** | **juin 2024** | aucune | aucune |
| Source | arXiv 2508.10925, carte de modele OpenAI | cartes et rapport technique muets | idem |
| llama.cpp | version 0.3.0, build 10621, commit c1d0e7a00, Metal [MESURE] | idem | idem |
| Python | 3.13, `.venv/bin/python` | | |

**Pourquoi gpt-oss-20b et pas Qwen3-30B-A3B, qui est plus gros.** Parce que c'est le seul
modele de la pile dont l'auteur publie une date de coupure et dont la taille soit
credible (a3 section 2). Une coupure publiee n'est pas une coupure verifiee, personne ne
l'a auditee, et la litterature documente des fuites posterieures a la coupure annoncee ;
c'est une condition necessaire, pas suffisante, et le rapport ne tirera aucune conclusion
de contamination.

**Le registre est relu de la trace, pas recopie.** `r2_evaluer.registre_modeles()` lit
`modele`, `quantification`, `gabarit`, `variante_fin` et `version_prompt` dans la premiere
ligne de chaque fichier JSONL et les ecrit dans `r2-couverture.csv`. Le registre publie
decrit donc le run, pas l'intention du run. Verifie sur la trace a5 :
`{'modele': 'Qwen3-4B-Instruct-2507', 'quantification': 'Q4_K_M', 'version_prompt':
'a5-p1'}` [MESURE].

---

## 2. La page de plan, en resume

Reproduction complete dans `resultats/r2-preenregistrement.md`. Les quatre familles, toutes
corrigees **separement** par Holm, Benjamini Hochberg a cote, p de bootstrap **apparie sur
les personnes**, 4 000 tirages partages par toutes les methodes, plancher du p a 1 sur
4 000, contraste a denominateur vide a p = 1.

| famille | enonce | tests |
|---|---|---|
| **F1 primaire** | **H1a** l'exces de rappel de `C3F gpt-oss` sur le **plancher de segment**, sur les raretes **stables** des 58 items, est positif ; **H1b** son avantage de rappel sur chacune des six methodes du regime severe est positif | 1 + 6 |
| **F2 secondaire** | **H2a** et **H2b**, les memes contrastes sur la **precision** | 1 + 6 |
| **F3 tertiaire** | **H3a** exactitude par personne contre les six methodes severes ; **H3b** contre `C3F Qwen3-4B` sur les personnes communes | 6 + 1 |
| **F4 quaternaire** | **H4a** diversite conservee contre les methodes a **tirage** ; **H4b** ecart absolu a 1 du ratio intra contre les memes ; **H4c** chute sous permutation intra camp, **descriptif** | 3 + 3 + 0 |

**Les six criteres de chute** sont dans la page de plan, section 4. Les deux qui comptent :
si **H1a** echoue, le dernier avantage mesure du jumeau de langage tombe et
`MODELE-DU-MONDE.md` 10.4 doit recevoir la restriction « hors du regime ou l'information
la plus proche manque » ; si **H1a** passe et **H1b** echoue contre `PMM k=10` et `IM m=10`,
la formulation autorisee devient « il bat le tirage dans le segment, il ne bat pas
l'appariement sur moyenne predite ».

**Les cinq predictions** sont dans la page de plan, section 5, et elles sont datees. La
plus utile est la (b) : je ne sais pas si H1b passe contre `PMM k=10 famille retiree`,
parce que a42 place `PMM k=10` au dessus de C3 sur les raretes stables **hors** regime
severe, et que a41 section 6 mesure que le retrait de la famille lui coute moins 8,9 points
de rappel minoritaire, plus qu'a toute autre methode. Les deux effets vont en sens
contraire.

---

## 3. Le protocole

### 3.1 Ce qui ne change pas par rapport a a5

**Tout, sauf le modele.** Le prompt systeme, le bloc utilisateur, l'ordre des modalites de
`question_master/gss/main.csv`, le decoupage de `a2_baselines_gss.grille` graine 20260903,
l'echantillon de 150 personnes graine 20260907, le scoring par lettre a un token verifie
par encodage du prefixe, le seuil de rejet de masse a 0,5, le format de trace et l'index de
reprise sont **importes** de `a5_agents_locaux_gss.py`, jamais recopies. Une seule fonction
de a5 est reecrite, la lecture des lettres, parce qu'elle suppose chez a5 que la lettre est
precedee d'une espace, ce qui n'est vrai que pour une des deux variantes de fin de prompt.

**Controle publie** : le gabarit Qwen construit par `r2_rares_apparie.construire_prompt`
est **identique caractere pour caractere** a `a5_agents_locaux_gss.gabarit_qwen` [MESURE,
controle 4 de la verification hors ligne].

### 3.2 Ce qui change, et pourquoi

| changement | motif |
|---|---|
| le modele est un drapeau `--modele` | a5 met son chemin en dur, lignes 81 et 95 ; R2 doit pouvoir basculer sur le repli sans editer un script |
| gabarit harmony pour gpt-oss | a3 section 4.5 : sans lui, gpt-oss place **3,2 pour cent** de sa masse sur les lettres, avec lui **99,93 pour cent** |
| C3 est restreint aux 58 items de famille | pour que C3 et C3F soient apparies **cellule a cellule** ; a5 predisait les 149 items en C3 |
| smoke test integre de 20 appels | une nuit d'appels a 3,2 pour cent de masse serait une nuit de bruit renormalise |
| refus de demarrer si un `llama-server` tourne | a5 section 4.4 mesure un **facteur 9,5** de perte de debit avec deux serveurs sur ce GPU |

### 3.3 La sonde de gabarit, mesuree et non supposee

a3 section 4.5 dit que le gabarit ne doit pas se terminer par une espace : avec une espace
finale la masse de gpt-oss tombe de 0,9993 a 0,84, parce que le modele hesite entre le
token `D` et le token ` D`. Deux fins de prompt sont donc possibles, et **le run mesure
laquelle est la bonne au lieu de la deviner** :

- **variante `answer`**, celle de a5 mot pour mot : le prompt s'arrete sur `Answer:` et
  c'est le token ` A`, espace comprise, qui est score ;
- **variante `brut`** : le prompt s'arrete sur l'ouverture du tour assistant,
  `<|start|>assistant<|channel|>final<|message|>`, et c'est le token `A` qui est score.
  C'est la forme exacte reproduite en a3.

Le run score le meme prompt dans les deux variantes, ecrit les deux masses dans le
journal, et **garde `answer` des qu'elle atteint 0,90**, pour que le prompt reste
comparable a la trace Qwen3-4B existante. Il ne bascule sur `brut` que si `answer` echoue
et que `brut` fait mieux. La variante retenue est ecrite dans chaque ligne de trace, champ
`variante_fin`, et dans `version_prompt`.

### 3.4 Le smoke test, et son verdict

Vingt appels reels, ecrits dans une trace separee `r2-smoke-gptoss.jsonl` qui ne se melange
jamais a la trace du run. Trois criteres, tous ecrits dans la page de plan :

| critere | seuil | motif |
|---|---|---|
| masse **mediane** sur les K lettres | >= 0,90 | attrape un gabarit faux ; a5 mesure 1,0000 en mediane sur Qwen |
| masse **minimale** | >= 0,50 | c'est le seuil de rejet par appel de a5 : si un seul appel sur vingt tombe dessous au demarrage, quelque chose ne va pas |
| part d'appels a modalite absente du top 40 | <= 0,25 | la masse peut etre haute et mal repartie |

En cas d'echec, le run **s'arrete sans ecrire une ligne de trace utile**, imprime une ligne
commencant par `arret : masse`, que la file de nuit surveille, et le repli documente est
`--modele qwen30`.

Le verdict est une fonction pure, `verdict_smoke()`, et il est teste hors ligne sur sept
cas synthetiques, dont les trois pannes reelles du dossier [MESURE] :

| cas | masses | verdict attendu | verdict obtenu |
|---|---|---|---|
| gabarit correct | 0,999 x 20 | continuer | continuer |
| **gpt-oss sans gabarit, a3 4.5** | 0,032 x 20 | arret | **arret**, « masse mediane 0.0320 sous le seuil 0.9 » |
| **gabarit avec espace finale, a3 4.5** | 0,84 x 20 | arret | **arret**, « masse mediane 0.8400 sous le seuil 0.9 » |
| un seul appel bas sur vingt | 0,999 x 19 et 0,40 | arret | **arret**, « masse minimale 0.4000 sous le seuil de rejet 0.5 » |
| mediane juste au seuil | 0,90 x 20 | continuer | continuer |
| masse mal repartie | 0,95 x 20, 8 modalites absentes | arret | **arret** |
| appels manquants | 12 au lieu de 20 | arret | **arret** |

### 3.5 La file, la fin dure et la reprise

L'ordre est **C3F d'abord**, parce que c'est le regime severe et donc la mesure du verrou 1,
puis C3. A l'interieur d'une condition, l'ordre est **personne par personne**, puis famille
par famille : une troncature a 08:00 coute des **personnes entieres**, jamais des items, et
toute personne evaluee porte ses 58 cellules.

- **fin dure** : `--fin 08:00`, convertie en epoch **avec le jour** par
  `a5_agents_locaux_gss.heure_de_fin`, qui bascule au lendemain si l'heure est deja passee.
  Controle : lancee a 22:10 le 8 septembre, elle rend le 9 septembre a 08:00 [MESURE] ;
  lancee a 01:00 le 9, elle rendra le 9 a 08:00.
- **PID** dans `data/traces/r2-run.pid`, ecrit avant le lancement du serveur.
- **journal** dans `data/traces/r2-run.log`, ecrit par le script lui meme en plus de la
  sortie standard, pour que la ligne `RUN TERMINE` y soit quel que soit le mode de
  lancement.
- **serveur arrete dans un `finally`**, meme si le run echoue, parce qu'un autre run
  attend la machine.
- **reprise** : l'index est (condition, pid, item). Une relance relit la trace, saute les
  appels deja faits et reprend. Les lignes tronquees par un arret brutal sont ignorees
  sans faire echouer la reprise.

---

## 4. Les resultats du test hors ligne

### 4.1 Trente trois controles, tous passes, aucun appel de modele

`.venv/bin/python analyses/r2_rares_apparie.py --verification-seule` [MESURE, journal dans
`data/traces/r2-verification.log`]

| bloc | ce qui est verifie | resultat |
|---|---|---|
| 1. enumeration | 8 700 appels pour C3F comme pour C3, 58 par personne, **6 prefixes par personne en C3F et 5 en C3** | conforme |
| 2. regime severe | sur 116 prompts de deux personnes : en C3F **ni l'item cible ni aucun de ses cousins** n'apparait dans le contexte ; en C3 l'item cible est absent et **les cousins sont presents** | 0 faute sur 116, dans les deux sens |
| 3. longueur | C3F 21 212 a 24 133 caracteres, environ **5 300 a 6 030 tokens** ; C3 environ 4 800 a 5 200 | tient dans les 8 192 tokens du slot |
| 4. gabarits | aucune variante ne finit par une espace ; le gabarit Qwen est **celui de a5, caractere pour caractere** | conforme |
| 5. reprise | index de 70 lignes relu, **ligne tronquee ignoree sans echec**, 46 appels restants sur 116 | conforme |
| 6. verdict du smoke test | les sept cas de la section 3.4 | conforme |
| 7. fin dure | epoch avec le jour | conforme |
| 8. machine | aucun `llama-server` en cours, les trois modeles presents | conforme |

**Un controle de la longueur des prompts merite d'etre lu.** C3F fait **plus long** que C3,
5 300 a 6 030 tokens contre 4 800 a 5 200, et c'est normal : C3F retire de 5 a 17 items du
contexte, C3 en retire 30. La trace a5 le confirme, `tokens_prompt` y vaut 5 276 sur le
premier appel [MESURE]. C3F est donc **la condition la plus chere du lot par appel
produit** : six prefixes de 5 300 tokens pour 58 appels utiles.

### 4.2 L'evaluateur, teste sur la trace C3F existante

`.venv/bin/python analyses/r2_evaluer.py --essai-sur-a5 --tirages 4000 --permutations 200`
[MESURE, sorties `r2-tableau-essai.csv`, `r2-contrastes-essai.csv`,
`r2-permutation-essai.csv`, `r2-couverture-essai.csv`, `r2-controles-essai.csv`]

**Le controle qui valide la chaine.** Les six contrastes d'exactitude de la famille F3,
calcules par `r2_evaluer` sur les 60 personnes de la trace C3F, doivent reproduire le
tableau de a41 section 5, qui a ete produit par un autre script :

| C3F Qwen3-4B moins | a41 section 5 | R2 sur la meme trace | ecart |
|---|---|---|---|
| `E1 famille retiree` | moins 0,1344 | **moins 0,1341** | 0,0003 |
| `B2 famille retiree (argmax)` | moins 0,1250 | **moins 0,1247** | 0,0003 |
| `IM m=10 mode, famille retiree` | moins 0,1110 | **moins 0,1103** | 0,0007 |
| `PMM k=10 famille retiree` | moins 0,0984 | **moins 0,0978** | 0,0006 |
| `E2 famille retiree (tirage)` | moins 0,0641 | **moins 0,0639** | 0,0002 |
| `B2 famille retiree (tirage)` | moins 0,0434 | **moins 0,0427** | 0,0007 |

**Ecart maximal 0,0007**, attribuable au tirage bootstrap, les deux scripts rendant la
moyenne des differences bootstrap et non la difference observee. Les exactitudes
ponctuelles, elles, sont **identiques a la quatrieme decimale** : C3F 0,5572, E1 0,6917,
B2 argmax 0,6822, IM 0,6681, PMM 0,6555, B0 mode 0,6376, E2 0,6216, B2 tirage 0,6009,
B0 tirage 0,5216, humains vague 2 0,7773 [MESURE, a comparer au tableau de a41 section 5].

**Le controle d'identite de la partition P_A.** a42 declare d'avance que `humains vague 2`
vaut un rappel de 1 sur les raretes stables et de 0 sur les instables, par construction. R2
mesure **1,0000 et 0,0000** [MESURE] : la partition de a42 est correctement importee.

**La mesure nouvelle, sur 60 personnes et 58 items, definition des raretes sur le
perimetre, 31 cellules rares stables.** Elle n'a aucune valeur de verdict, le run n'a pas eu
lieu ; elle est publiee parce qu'elle donne l'ordre de grandeur et la puissance.

| methode | rappel stables | IC 95 % | exces sur plancher de segment | IC 95 % |
|---|---|---|---|---|
| *humains vague 2* | *1,0000* | | *plus 0,8745* | *identite* |
| **`C3F Qwen3-4B`** | **0,2581** | [0,105 ; 0,476] | **plus 0,1245** | **[moins 0,047 ; 0,395]** |
| `E2 famille retiree (tirage)` | 0,2258 | [0,091 ; 0,364] | plus 0,0412 | [moins 0,096 ; 0,184] |
| `PMM k=10 famille retiree` | 0,1290 | [0,000 ; 0,226] | moins 0,0005 | [moins 0,141 ; 0,112] |
| `B2 famille retiree (tirage)` | 0,1290 | [0,000 ; 0,238] | moins 0,0005 | [moins 0,120 ; 0,143] |
| `E1 famille retiree (argmax)` | 0,0968 | [0,000 ; 0,190] | moins 0,0421 | [moins 0,150 ; 0,069] |
| `IM m=10 mode, famille retiree` | 0,0968 | [0,000 ; 0,235] | moins 0,0838 | [moins 0,171 ; 0,055] |
| `B1 argmax` | 0,0968 | [0,000 ; 0,245] | moins 0,0005 | |
| `B3 foret` | 0,0645 | [0,000 ; 0,143] | moins 0,0838 | [moins 0,158 ; moins 0,036] |
| `B2 famille retiree (argmax)` | 0,0323 | [0,000 ; 0,107] | moins 0,1255 | [moins 0,178 ; moins 0,066] |
| `B0 mode` | 0,0000 | | moins 0,1255 | |

Plancher de segment sur ces cellules : **0,1255** [MESURE].

**Aucun contraste de la famille primaire ne franchit Holm sur ce perimetre** : H1a p ajuste
0,585, et H1b va de 0,175 contre `B2 famille retiree (argmax)` a 0,800 contre
`E2 famille retiree (tirage)` [MESURE]. **C'est la puissance, pas le signe** : les six
differences H1b sont positives, de plus 0,032 a plus 0,226, et cinq des six intervalles ont
leur borne basse a zero ou au dessus. Avec 31 cellules, un intervalle bootstrap sur les
personnes ne peut pas etre etroit.

**F3 et F4 franchissent Holm dans le sens defavorable au jumeau**, ce qui est le resultat
connu de a41 : moins 4,3 a moins 13,4 points d'exactitude, p ajuste 0,015 sur les six ; et
sur la structure, C3F conserve 0,590 de diversite contre 0,995 pour `E2 famille retiree`,
soit moins 0,406 [moins 0,465 ; moins 0,348], et il est plus loin de 1 sur le ratio intra
de plus 0,30 a plus 0,32 contre les trois methodes a tirage, les six intervalles disjoints
de zero [MESURE].

### 4.3 H4c, la chute sous permutation, sur 60 personnes

Trois segmentations, comme a44 : `S_fin`, le bloc ideologie x genre x age ; `S_ideo`, les
sept niveaux bruts ; et `S_camp`, le camp a trois niveaux annonce dans la page de plan.
200 permutations.

**`S_fin` est declaree non calculable** : sur 60 personnes le plus gros groupe compte
**4 individus** [MESURE], la permutation y est presque l'identite, et la case reste vide.
C'est ce que la page de plan avait ecrit d'avance.

Sur `S_camp`, trois camps, le plus gros a 26 personnes [MESURE] :

| methode | exactitude | permutee | chute | part du plancher humain |
|---|---|---|---|---|
| *humains vague 2, plancher* | *0,7773* | *0,5777* | ***0,1996*** | *100 %* |
| `PMM k=10 famille retiree` | 0,6555 | 0,5728 | 0,0826 | **41 %** |
| `E1 famille retiree` | 0,6917 | 0,6101 | 0,0815 | 41 % |
| `IM m=10 mode, famille retiree` | 0,6681 | 0,5947 | 0,0734 | 37 % |
| `E2 famille retiree (tirage)` | 0,6216 | 0,5563 | 0,0653 | 33 % |
| `B2 famille retiree (argmax)` | 0,6822 | 0,6348 | 0,0474 | 24 % |
| **`C3F Qwen3-4B`** | 0,5572 | 0,5274 | **0,0298** | **15 %** |
| `B2 famille retiree (tirage)` | 0,6009 | 0,5726 | 0,0282 | 14 % |

[MESURE, descriptif, hors famille d'hypotheses] **Lecture prudente, et une seule.** a44
section 5 mesure sur 149 items et 1 052 personnes que C3 perd 45 pour cent du plancher
humain et PMM 60. Ici, sur 58 items, 60 personnes et **la famille retiree**, C3F en perd 15
et PMM 41. La comparaison directe des deux nombres n'est pas legitime, le perimetre a
change sur trois dimensions a la fois. Ce qui est lisible est **l'ordre** : prive de sa
famille thematique, notre agent porte **moins** la personne que les imputations
statistiques qui subissent la meme privation. C'est coherent avec a41, et c'est une raison
de plus de ne rien conclure avant le run sur gpt-oss.

### 4.4 Le test sur trace synthetique

Une trace synthetique a ete fabriquee hors de `data/traces` (option `--racine-traces`, pour
qu'un essai ne puisse jamais polluer l'index de reprise du run) a partir de la trace a5 :
40 personnes completes en C3F, 25 en C3, une personne partielle, les distributions lissees
vers l'uniforme et l'argmax bascule sur 25 a 40 pour cent des cellules, plus une derniere
ligne volontairement tronquee. [MESURE]

| ce qui est teste | resultat |
|---|---|
| lecture de deux traces R2 et de la trace a5 dans le meme passage | 40, 25 et 60 personnes completes lues, registres distincts |
| tolerance au partiel | la personne partielle est comptee et **ecartee**, 0 erreur |
| ligne tronquee en fin de fichier | ignoree sans echec |
| traces absentes (`qwen30`) | signalees dans `r2-controles.csv`, le reste continue |
| contrastes croises H3b sur personnes communes | 25 et 40 personnes communes, differences non nulles et intervalles finis |
| definitions de rarete perimetre et population | 14 contre 18 cellules stables sur 40 personnes |

Les fichiers de sortie de ce test ont ete **supprimes** : une donnee fabriquee n'a rien a
faire dans `resultats/`. Les fichiers `r2-*-essai.csv`, eux, sont conserves : ils portent
des mesures reelles sur la trace a5.

### 4.5 La projection de debit, et combien de personnes seront couvertes

Deux ancrages mesures, aucune extrapolation libre :

| | valeur | source |
|---|---|---|
| C3F sur Qwen3-4B, machine a charge 1,4 | **2 688 appels par heure** | `data/traces/a5-familles.log` [MESURE] |
| gpt-oss-20b contre Qwen3-4B, regime etabli | 9 569 contre 18 060 appels par heure, rapport **0,53** | a3 section 5.1 [MESURE] |
| gpt-oss-20b, prefill | 492 tokens par seconde contre 790 pour Qwen3-4B | a3 section 5.1 [MESURE] |

**Projection : environ 1 420 appels par heure sur C3F, soit 6,1 h pour les 8 700 appels des
150 personnes.** [ESTIMATION]

**Le budget a ete revise a la baisse apres lecture de `analyses/file_nuit_2.sh`**, ecrite
par l'agent de R1 pendant que ce rapport se redigeait : la fin dure de R1 y est **02:30**,
pas 01:00, et R2 est lance ensuite. Le budget realiste est donc de **5,5 h** et non de 7 h.

**Conclusion de la projection, ecrite avant le run** : **C3F couvre environ 130 des
150 personnes, et C3 ne tournera pas.** [ESTIMATION] Si R1 finit avant sa fin dure, C3F
couvre les 150. C'est le bon arbitrage : C3F est le regime severe, donc la mesure du
verrou 1 ; C3 est le repere, et il existe deja sur Qwen3-4B dans la trace a5. L'ordre
personne par personne garantit que les personnes couvertes le sont sur leurs 58 items.

**La projection est refaite sur mesure au demarrage.** Le smoke test separe le cout d'un
prefixe du cout d'un appel servi par le cache, et le journal ecrit alors, avant le premier
appel de la file, le nombre de personnes que chaque condition couvrira dans le budget
restant. Les deux postes sont projetes separement parce que le prefixe pese 57 pour cent du
temps en a5 section 4.1, et les moyenner en un seul debit se trompe d'un facteur deux selon
la condition.

---

## 5. Ce que l'evaluateur importe, et ce qui n'est pas importable

**Importe et rejoue sans une ligne recopiee** [CONFIRME, `r2-controles-essai.csv`] :

| brique | provenance |
|---|---|
| `E1 famille retiree`, `E2 famille retiree`, `PMM k=10 famille retiree`, `IM m=10 mode, famille retiree` | `a35_familles.imputer_par_famille`, par `a41_commun.construire_severe` |
| `B2 famille retiree (argmax)` | `a33_commun.b2_famille_retiree` |
| `B2 famille retiree (tirage)` | `a41_commun.b2_famille_retiree_tirage` |
| `B0 mode`, `B0 tirage`, `B1 argmax`, `B3 foret`, `humains vague 2` | cache de a25 et de a28 |
| la partition des raretes **stables** | `a42_commun.classes_stabilite` |
| les trois planchers | `a42_commun`, dont le plancher de segment de `a34_commun.frequence_segment` |
| rappel, precision, exces par personne | `a42_commun.mesure_sur` |
| exactitude, diversite, dispersion, bootstrap, Holm | `a35_commun` et `a41_commun` |
| la permutation intra groupe | `a44_commun.permuter_intra` et `a44_commun.segmentations` |
| la lecture des traces JSONL | `a5_evaluer.moyenner_passes` et `en_matrices` |

**Les six methodes du regime severe sont les six importables.** [MESURE, controle
« methodes du regime severe importables : 6 sur 6 »]

**Ce qui n'est PAS importable, et le rapport le dit en tete de chaque tableau :**

1. **Les six conditions d'agents de Stanford dans le regime severe.** Elles gardent les
   items cousins dans leur invite (a8 errata E1, a41 section 0.2). Les replacer en regime
   severe demanderait de relancer leur pipeline. Elles ne sont donc **ni testees, ni
   affichees comme adversaires** dans R2. C'est exactement le biais que R2 existe pour
   contourner : au lieu de corriger leur invite, on impose le regime severe a notre agent.
2. **La precision de reference d'un tirage dans le segment.** `a42_commun.mesure_sur` ne la
   fournit pas, parce que a42 ne teste que le rappel. Elle est construite dans
   `r2_evaluer` avec les memes briques, `moyenne_par_personne` sur le plancher de segment
   restreint aux cellules **osees** par la methode, et le fait est declare ici.
3. **La chute sous permutation sur `S_fin`.** Non calculable sous 60 personnes, groupe
   maximal a 4 individus. Declare d'avance dans la page de plan.
4. **La seconde passe**, ordre inverse des modalites. Elle double les appels et le budget
   de la nuit ne le permet pas. Le biais de position est donc **non controle** dans R2. Il
   est le meme pour C3F et pour C3, donc il ne biaise pas leur comparaison ; il peut biaiser
   la comparaison avec les methodes statistiques, qui n'ont pas de biais de position.

---

## 6. La commande du matin

**Le run, lance par la file de nuit apres R1, sans intervention :**

```bash
.venv/bin/python analyses/r2_rares_apparie.py --fin 08:00
```

Le fichier `data/traces/r2-pret` signale a `analyses/file_nuit_2.sh` que le script est
verifie et que la file peut l'enchainer. Le run refuse de demarrer si un `llama-server`
tourne encore.

**Si le smoke test echoue** (ligne `arret : masse` dans `data/traces/r2-run.log`), le repli
documente, a lancer a la main :

```bash
.venv/bin/python analyses/r2_rares_apparie.py --modele qwen30 --fin 08:00
```

**L'evaluation, au matin, machine libre, zero appel :**

```bash
.venv/bin/python analyses/r2_evaluer.py --tirages 4000 --permutations 200
```

**Verifier l'etat du run en trois commandes :**

```bash
tail -20 data/traces/r2-run.log
grep -c . data/traces/r2-C3F-gptoss.jsonl        # appels ecrits, sur 8 700
cat data/traces/r2-resume-gptoss.json            # debit, projection, variante retenue
```

**Reprendre un run tronque, plus tard dans la journee, sans refaire un seul appel :**

```bash
.venv/bin/python analyses/r2_rares_apparie.py --conditions C3F --fin 23:00
```

---

## 7. Ce que je n'ai pas pu verifier

1. **Que gpt-oss-20b place effectivement sa masse sur les lettres avec ce prompt la.**
   [NON VERIFIE] a3 section 4.5 le mesure a 0,9993, mais sur un prompt court et un persona
   different. Nos prompts C3F font 5 300 a 6 000 tokens et se terminent sur la question
   secrete. Le smoke test integre existe **exactement** pour cette incertitude, et c'est
   pourquoi son verdict est bloquant plutot qu'informatif.
2. **Laquelle des deux variantes de fin de prompt est la bonne pour gpt-oss.** [NON
   VERIFIE] a3 reproduit un gabarit qui s'arrete sur `<|message|>` ; a5 ajoute `Answer:`.
   La sonde tranchera au demarrage, sur mesure, et ecrira les deux masses. Je ne sais pas
   d'avance laquelle gagnera.
3. **Que llama-server accepte le cache KV quantifie sur gpt-oss-20b.** [NON VERIFIE] Ce
   modele a des puits d'attention et une fenetre glissante sur une couche sur deux. Le run
   retente une fois sans `--cache-type-k q8_0` si le serveur ne demarre pas, et le fait est
   ecrit dans le journal.
4. **Le debit reel.** [NON VERIFIE] La projection de 1 420 appels par heure repose sur un
   rapport de debits mesure en regime etabli sur des prompts courts, applique a un debit
   mesure sur des prompts longs. Elle peut se tromper d'un facteur deux dans les deux sens.
   La seule mesure qui vaudra est celle du smoke test.
5. **La puissance sur 150 personnes.** [NON VERIFIE] 31 cellules rares stables sur 60
   personnes donnent environ 78 sur 150, en supposant la proportionnalite. Si le run est
   tronque a 100 personnes, on sera vers 52. **Je ne peux pas dire d'avance si la famille
   primaire franchira Holm meme dans le cas favorable.** C'est la limite qu'il faudra
   ecrire en tete du rapport de demain, quel que soit le resultat.
6. **La contamination.** [NON VERIFIE] La coupure de juin 2024 est publiee par OpenAI, pas
   auditee. R2 n'en tire aucune conclusion et ne doit pas en tirer.
7. **La generalisation aux 1 052 personnes.** [CONFIRME comme limite] Les 150 personnes
   sont un sous echantillon stratifie sur les cinq plis ; les 60 de la trace Qwen3-4B
   viennent des plis 0 et 1 seulement (a33 section 0.1 point 5). La comparaison appariee
   n'en souffre pas, ce sont les memes personnes des deux cotes ; la generalisation, si.
8. **Le comportement de la file de nuit.** [PARTIELLEMENT VERIFIE] `analyses/file_nuit_2.sh`
   a ete ecrite par l'agent de R1 pendant la redaction de ce rapport. Elle lance bien
   `.venv/bin/python analyses/r2_rares_apparie.py --fin 08:00` apres son propre run, elle
   attend le temoin `data/traces/r2-pret` avec un plafond a 01:30, et elle emploie le meme
   `pgrep -x llama-server` que le run. Deux points relies : elle redirige la sortie standard
   vers `data/traces/r2-run.log`, ou le script ecrit deja son journal, et le journal
   detecte ce cas par inode pour ne pas doubler chaque ligne [MESURE, controle]. Ce que je
   n'ai pas verifie : que R1 finisse et libere effectivement le GPU avant 02:30.

---

## 8. Questions ouvertes pour Simon

1. **La definition de la rarete, sur le perimetre ou sur la population.** a42 applique le
   seuil de 10 pour cent aux personnes du perimetre, a41 aux 1 052. Sur 60 personnes les
   deux ne donnent pas le meme ensemble de cellules, 31 contre 30, et sur 40 personnes
   l'ecart monte a 14 contre 18 [MESURE]. R2 publie les deux et **corrige seulement celle
   du perimetre**, qui est la definition declaree. Est ce le bon choix ? L'argument contre :
   une modalite « rare » sur 60 personnes peut etre majoritaire sur 1 052.
2. **Le rappel est il la bonne quantite, ou faut il passer au F1 ?** La page de plan teste
   rappel et precision separement, et le F1 est rapporte sans test. Sur la trace a5, C3F a
   le meilleur rappel des raretes stables et une precision de 0,073 contre 0,188 pour E1
   [MESURE] : un lecteur adverse dira que le jumeau ose des minorites partout. La reponse
   du dossier a toujours ete que le rappel est ce qui compte pour « une societe sans
   minorites », mais elle n'a jamais ete defendue contre la precision.
3. **La chute sous permutation, sur quel groupe ?** a44 mesure sur `S_fin` et `S_ideo` ;
   sur 60 a 150 personnes `S_fin` est vide et `S_ideo` donne deux groupes exploitables. R2
   ajoute `S_camp` a trois niveaux. Faut il faire de `S_camp` la quantite de verdict du
   dossier, ce qui rendrait a44 et R2 comparables, au prix d'un groupe plus grossier ?
4. **Que faire si H1a passe et H1b echoue contre `PMM k=10` seulement ?** Le critere de
   chute 2 de la page de plan couvre le cas ou H1b echoue contre `PMM` **et** `IM`. Si
   `IM` tombe et pas `PMM`, la lecture est ambigue et je preferrerais une regle ecrite
   d'avance plutot qu'un arbitrage apres coup.
5. **Le repli sur Qwen3-30B-A3B change la these de contamination.** Ce modele n'a **aucune**
   coupure publiee. Si le smoke test force le repli, R2 mesure toujours le verrou 1, mais
   il perd l'argument « la question est posterieure a la coupure du modele ». Faut il alors
   preferer Llama-3.1-8B, coupure decembre 2023 publiee, plus petit que Qwen3-4B en
   capacite mais mieux date ?

---

## Rejouer

```bash
# 1. verification hors ligne, sans serveur, machine occupee
.venv/bin/python analyses/r2_rares_apparie.py --verification-seule

# 2. le run, apres R1, un seul llama-server a la fois
.venv/bin/python analyses/r2_rares_apparie.py --fin 08:00

# 3. l'evaluation, zero appel
.venv/bin/python analyses/r2_evaluer.py --tirages 4000 --permutations 200

# 4. le controle qui valide la chaine de mesure, sur la trace a5 seule
.venv/bin/python analyses/r2_evaluer.py --essai-sur-a5 --tirages 4000 --permutations 200
```
