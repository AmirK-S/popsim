# a11. Nos agents locaux sur Twin-2K-500, second run de la nuit

Rapport de preparation, ecrit avant le run. Il decrit ce qui est en place, ce qui est
mesure, ce qui est projete et ce qui reste incertain. Les chiffres de fidelite seront
produits au matin par `analyses/a11_evaluer_twin.py` ; ce rapport ne les anticipe pas.

Version du 8 septembre 2026, 00 h 55. Machine : Apple M5, 32 Gio de memoire unifiee.
Scripts : `analyses/a11_agents_locaux_twin.py`, `analyses/a11_evaluer_twin.py`.

**Etat au moment de la remise : le run n'a pas tourne cette nuit, et c'est une decision, pas
un accident.** Le detail est en section 6.3. Les deux scripts sont prets, testes et
utilisables tels quels la prochaine nuit.

---

## 1. Ce qu'il faut retenir

1. **Le run est reporte a une autre nuit.** Il a ete lance et mis en attente a 23 h 05,
   PID 54981, puis tue vers 00 h 40 par la pression memoire de la machine ; en parallele, la
   file de nuit a ete reecrite a 23 h 45 pour reporter Twin-2K-500, sur la base de la
   projection de la section 6.2. Les deux scripts sont prets et testes. Section 6.3 pour le
   deroule complet et pour ce qu'il faut faire la prochaine nuit.
2. **Le resultat le plus important de cette preparation est negatif, et il change le plan
   de la nuit.** Le persona texte complet des vagues 1 a 3 pese **27 515 tokens en
   mediane** [MESURE], et le cout de son prefill ne croit pas comme sa longueur mais comme
   son carre : **348,8 secondes pour 27 638 tokens** contre 34,7 secondes pour les 8 192
   premiers [MESURE]. La condition a persona complet sur 150 personnes est un travail de
   dix heures, pas d'une nuit partagee.
3. **Trois conditions au lieu de deux, et l'ordre a change.** `C3b-Twin`, persona tronque a
   8 000 tokens sur une frontiere de question, passe en premier parce qu'elle couvre les
   150 personnes en moins de deux heures. Puis `C2-Twin`, demographies seules. Puis
   `C3-Twin`, persona complet, qui prend ce qui reste. Mettre C3-Twin en tete aurait rendu
   la nuit tout ou rien.
4. **Le scoring fonctionne, et mieux que sur le GSS.** La masse de probabilite portee par
   les lettres avant renormalisation vaut **0,999998 en mediane** [MESURE], contre 0,89 a
   0,97 pour les prompts bruts de a3. Zero appel rejete, zero modalite absente du top 40.
5. **L'alignement sur a5 est un import, pas une recopie.** Client serveur, gabarit Qwen,
   scoring, verification des identifiants de tokens, seuil de rejet, consigne, preambule et
   graine d'echantillonnage viennent de `a5_agents_locaux_gss.py` par `import`. Le format de
   ligne de trace est celui de a5, a trois champs additifs pres.
6. **L'evaluateur rapporte l'exactitude par bloc du catalogue**, comme le demande la tache 4
   du rapport a8, et il traite le bloc des preferences de prix comme un signal de
   contamination possible.

---

## 2. Configuration

### 2.1 Le modele et le serveur

| Element | Valeur | Origine |
|---|---|---|
| Modele | Qwen3-4B-Instruct-2507, GGUF Q4_K_M | meme fichier que a5 |
| Moteur | `llama-server` 0.3.0, build 10621 | pile installee en a3 |
| Contexte | `-c 32768`, un seul slot | persona maximal 28 007 tokens plus la question |
| Parallelisme | `-np 1` | a3 section 4.7 : meilleure valeur absolue mesuree |
| Cache KV | `q8_0`, `-fa on`, `--cache-reuse 256` | configuration de reference de a3 |
| Scoring | passage avant unique, `n_predict 1`, `n_probs 40`, temperature nulle | a3 section 3.4, traitement (a) |

Le contexte est **superieur a la longueur maximale du persona plus la question** : 32 768
contre 28 007 plus 258 au pire, soit une marge de 4 500 tokens. Le script verifie en outre,
persona par persona et au tokeniseur du serveur, que le budget `contexte moins 1 500` est
respecte, et tronque de facon documentee et journalisee s'il ne l'est pas. Sur les 150
personnes retenues, **aucune troncature de contexte ne se declenche** [MESURE]. Le journal
du serveur confirme de son cote `truncated = 0` sur les appels du smoke test.

`-np 8`, la valeur de a5 sur le GSS, est impossible ici : le contexte est partage entre les
slots, et huit slots de 27,5 k tokens demanderaient 220 k tokens de cache KV, soit plus de
17 Gio a `q8_0`.

### 2.2 Les trois conditions

| Code | Matiere donnee au modele | Longueur mediane | Analogue chez les auteurs |
|---|---|---|---|
| **C3b-Twin** | persona texte tronque a 8 000 tokens, sur frontiere de question | 8 000 tokens, 42 questions sur 173 | aucun, condition propre au projet |
| **C2-Twin** | les 14 questions du bloc Demographics seules | 1 084 tokens | `demo_only_gpt41mini` |
| **C3-Twin** | `wave1_3_persona_text` en entier | 27 515 tokens | `default_gpt41mini` |

C3-Twin est l'analogue exact de la configuration par defaut des auteurs : memes personnes,
meme matiere d'entree, meme cible. La comparaison est alors **a modele egal d'information**,
notre Qwen3-4B quantifie en 4 bits contre leur GPT-4.1-mini. C'est la seule comparaison du
projet ou l'ecart mesure ne peut pas etre impute a une difference de contexte. C3b-Twin ne
possede pas cette propriete : elle donne moins d'information que les auteurs, et tout
resultat obtenu sur elle doit le dire.

**La troncature de C3b-Twin, en detail.** Le texte des auteurs separe les questions par une
ligne vide. La coupe se fait sur cette frontiere, jamais au milieu d'un enonce ni entre un
enonce et sa reponse : un persona coupe en plein milieu apprendrait au modele une question
sans reponse, ce qui n'est pas une information appauvrie mais une information fausse. Un
marqueur explicite ferme le texte, `[Only the first part of this person's survey answers is
shown here.]`, sans quoi le modele lit un questionnaire qui s'arrete sans raison. Sur le
persona median, 8 000 tokens couvrent le bloc Demographics en entier, le premier bloc de
personnalite et le debut des tests cognitifs, soit 42 des 173 questions [MESURE].

**Le rendu de C2-Twin n'est pas une reformulation** : c'est le prefixe exact, caractere pour
caractere, du persona complet, verifie sur les 294 personas disponibles [MESURE]. Sans cette
verification, l'ecart entre conditions melangerait un effet de quantite d'information et un
effet de mise en forme. Le run s'arrete si la verification echoue.

### 2.3 L'echantillon et la cible

- **150 personnes**, 30 par pli des 5 plis de a2, graine de decoupage 20260903, graine de
  tirage 20260907, la meme que a5. Identifiants dans `data/traces/a11-personnes.csv`, ecrit
  **avant** le premier appel.
- **108 items** : les colonnes categorielles de la vague 4 retenues par a2, memes items,
  memes exclusions. 68 MC a reponse unique et 40 lignes de matrice. De 2 a 10 modalites,
  3,63 en moyenne, etiquetees A a J.
- **12 268 appels par condition** [MESURE], soit 82 items par personne en moyenne et non
  108 : la vague 4 contient des experiences inter sujets, chaque personne ne voit qu'une
  condition, et 24,1 pour cent des cellules de la cible sont vides. Ces cellules ne sont pas
  interrogees. a2 les exclut deja du numerateur et du denominateur, donc aucun chiffre ne
  change et le run est raccourci d'un quart.
- **Ordre des personnes** : alternance entre les cinq plis. Un ordre pli par pli laisserait,
  en cas de coupure, un echantillon entierement pris dans les deux premiers plis. En
  alternant, tout prefixe de la liste reste equilibre a une personne pres [MESURE : 8, 8, 8,
  8, 8 sur un prefixe de 40].
- **Ordre des items a l'interieur d'une personne** : `Product Preferences - Pricing` 40
  items, puis `Non-experimental heuristics and biases` 10, puis `False consensus` 10, puis
  `Probability matching` 16, puis le reste. Toute personne atteinte a donc le contraste
  prix contre heuristiques, qui est la question de la tache 4 de a8, avant tout le reste.

Ce reordonnancement se fait **a l'interieur d'une personne, jamais entre les personnes**, et
la raison est chiffree. Un ordre bloc majeur, qui passerait le bloc des prix sur les 150
personnes avant de passer au bloc suivant, repaierait le prefixe de 27 500 tokens une fois
par couple personne et bloc, soit un facteur egal au nombre de passes sur la duree du run.
A 348,8 secondes le prefixe, ce n'est pas negociable.

### 2.4 Controles passes avant le premier appel

| Controle | Resultat |
|---|---|
| Le persona des vagues 1 a 3 contient il des questions de la vague 4 ? | **non**, 71 libelles cibles distincts, 0 occurrence sur les 150 personas retenus [MESURE] |
| Le rendu des demographies est il le prefixe exact du persona complet ? | **oui**, 294 sur 294 [MESURE] |
| Les K modalites ont elles K identifiants de tokens distincts ? | **oui**, verifie a chaque nouveau K, methode de a3 3.4 importee de a5 |
| Les personas tiennent ils dans le contexte ? | **oui**, 28 007 tokens au maximum contre un budget de 31 268 [MESURE] |
| Les codes de la trace correspondent ils a ceux de `wave4_response.csv` ? | **oui**, verifie a la main sur les 8 appels du smoke test, la consistance test retest calculee par l'evaluateur sur ces items, 3 sur 8, se retrouve a la main dans le fichier officiel [MESURE] |

---

## 3. Longueur des personas et cout de prefill

Mesure au tokeniseur du serveur, pas par une regle de trois sur le nombre de caracteres.

| | C3-Twin | C3b-Twin | C2-Twin |
|---|---|---|---|
| Minimum | 27 151 | 8 000 environ | 1 083 |
| **Mediane** | **27 515** | **8 000** | **1 084** |
| Maximum | 28 007 | 8 000 environ | 1 095 |

[MESURE] Ecrit dans `data/traces/a11-personas-tokens.csv`, une ligne par personne, avec le
nombre de questions gardees par la troncature.

Le bloc question pese de 28 a 258 tokens selon l'item, mediane 93, et le reste du gabarit
environ 80 tokens. Le prompt le plus long mesure 27 827 tokens.

### 3.1 Le cout du prefill n'est pas proportionnel a la longueur

C'est la mesure qui commande tout le reste. Journal du serveur pendant le smoke test, un
seul persona, un seul flux, **pendant que le serveur a5 occupait la meme machine** :

| Longueur du prefixe | Duree cumulee | Debit cumule | Cout de la tranche de 2 048 tokens |
|---|---|---|---|
| 2 048 | 4,5 s | 455 t/s | 4,5 s |
| 4 096 | 12,7 s | 322 t/s | 8,2 s |
| 8 192 | 34,7 s | 236 t/s | 12,0 s |
| 10 240 | 48,9 s | 210 t/s | 14,2 s |
| 16 384 | 110,6 s | 148 t/s | 24,3 s |
| 20 480 | 170,0 s | 120 t/s | 30,8 s |
| 24 576 | 253,0 s | 97 t/s | 47,6 s |
| **27 638** | **348,8 s** | **79 t/s** | |

[MESURE] Le cout d'une tranche de 2 048 tokens passe de 4,5 secondes a 47,6 secondes entre
la premiere et la douzieme. C'est le cout quadratique de l'attention, invisible sur les
contextes de 3 029 tokens du banc a3, et il domine tout sur ce jeu de donnees.

**Consequence directe** : tronquer le persona a 8 000 tokens ne divise pas le cout de
prefill par 3,4 mais **par 10**, 34,7 secondes contre 348,8. C'est ce qui rend C3b-Twin
possible et C3-Twin difficile.

### 3.2 Le cache de prefixe fonctionne

Une fois le persona calcule, les appels suivants sur la meme personne ne recalculent que le
bloc question : **50 a 59 tokens sur 27 650** [MESURE]. La duree tombe de 348,8 secondes a
**2 080 millisecondes en mediane**, minimum 1 813, maximum 2 158, toujours sous contention.
C'est ce qui justifie l'ordre personne par personne.

---

## 4. Ordre des appels, reprise et arret

- **Ordre** : condition par condition, personne par personne, items prioritaires d'abord.
  Un seul calcul de prefixe par personne et par condition.
- **Index unique** : `(condition, passe, pid, item)`. Une relance ne refait aucun appel deja
  trace. L'index est lu par `index_existant()`, importe de a5, qui ignore sans echouer la
  derniere ligne d'un fichier interrompu en cours d'ecriture.
- **Ecriture** : une ligne JSON par appel, `flush` a chaque ligne, `fsync` toutes les 200.
- **Fin dure a 06 h 15** heure locale, verifiee avant chaque appel. Arret propre, serveur
  arrete dans un `finally`, puis `RUN TERMINE` ecrit dans le journal. Ce n'est pas 07 h 30 :
  `analyses/file_de_nuit.sh` enchaine derriere a11 deux autres travaux, `a5 --familles` puis
  `a5 --passe 2`, et attend la fin de a11 pour demarrer. Un a11 qui deborderait les
  bloquerait tous les deux, et le garde fou de la file le tuerait a 06 h 20 sans arret
  propre.
- **Reserve entre conditions** : chaque condition rend aux suivantes le temps qu'il leur
  faut et pas davantage, 40 minutes pour C2-Twin, rien pour C3-Twin qui est la derniere. La
  reserve est plafonnee a **30 pour cent** du temps restant, et ce chiffre vient de la
  mesure : une personne coute environ 53 secondes en C3b-Twin contre 22 en C2-Twin, et les
  deux conditions parcourant les personnes dans le meme ordre, la comparaison porte sur
  l'intersection, donc sur la condition la plus lente. Un partage a parts egales donnerait a
  C2-Twin deux fois plus de personnes qu'a C3b-Twin, dont la moitie ne servirait a rien.

Les trois conditions parcourent les personnes **dans le meme ordre**. Les premieres minutes
de C2-Twin couvrent donc exactement les personnes que C3b-Twin a eu le temps de traiter, ce
qui maximise l'intersection sur laquelle la comparaison sera faite.

### La file d'attente derriere a5

Le script attend, dans cet ordre, et aucune de ces trois etapes ne suffit seule :

1. l'apparition de `data/traces/a5-run.pid`, puis l'extinction de ce processus ;
2. la ligne `RUN TERMINE` dans `data/traces/a5-run.log` ;
3. la disparition de tout processus `llama-server`, verifiee par `pgrep`.

Si le fichier PID n'apparait jamais, le script ne force pas : il ne demarre que si aucun
`llama-server` ne tourne, et abandonne au bout de dix minutes d'attente supplementaire.

---

## 5. Smoke test

**Ce qui a ete fait.** Serveur dedie sur le port 8199, `-np 1`, `-c 32768`, KV `q8_0`, lance
a 22 h 47 apres verification que `a5-run.pid` existait et que `a5-run.log` montrait le run
complet en cours. Condition C3-Twin, 3 personnes prevues, 8 items par personne.

**Ce qui a ete interrompu, et pourquoi.** Le smoke test a ete arrete a 22 h 58 apres
**8 appels sur les 24 prevus**, sur ordre de l'orchestrateur. La raison est mesuree : les
deux serveurs se disputaient le GPU, le debit du run a5 est tombe de 11 333 a environ 1 700
appels par heure, et chaque persona de C3-Twin monopolisait la machine six minutes. Le
serveur 8199 a ete arrete et n'a pas ete relance. **La condition C2-Twin et la condition
C3b-Twin n'ont donc jamais ete executees contre un serveur**, elles ne sont validees que
hors ligne. C'est la limite principale de cette preparation et elle est reprise en
section 8.

**Ce que le smoke test etablit** [MESURE] :

| Mesure | Valeur |
|---|---|
| Masse de probabilite sur les lettres, avant renormalisation | mediane 0,999998, minimum 0,999982 |
| Appels rejetes, seuil 0,5 | 0 sur 8 |
| Appels avec une modalite absente du top 40 | 0 sur 8 |
| Identifiants de tokens des 5 lettres | A 362, B 425, C 356, D 422, E 468, distincts |
| Prefill a froid | 348,8 s pour 27 638 tokens |
| Appels suivants sur le meme persona | mediane 2 080 ms, 50 a 59 tokens recalcules |
| Troncature de contexte declenchee | aucune, `truncated = 0` cote serveur |

La masse a 0,999998 est le chiffre le plus rassurant du lot. Le piege documente en a3
section 4.5, ou gpt-oss-20b ne placait que 3,2 pour cent de sa masse sur les lettres faute
de gabarit de conversation, ne se produit pas ici : le gabarit Qwen suivi de `Answer:` sans
espace final fait mieux que les prompts bruts du banc, 0,89 a 0,97.

**Ce que le smoke test ne dit pas.** Sur les 8 items, tous du bloc `False consensus` de la
personne 1392, l'agent se trompe 8 fois sur 8, avec une confiance moyenne de 0,765 et une
probabilite moyenne de 0,044 sur la vraie reponse. Le plafond test retest de cette personne
sur ces memes items est de 3 sur 8. **Aucune conclusion n'est tiree de ce chiffre** : une
personne, huit items, une seule batterie d'opinions politiques. Il est rapporte parce qu'il
a servi a verifier a la main que le code predit et le code du fichier officiel sont dans le
meme repere, ce qui est le cas.

**L'evaluateur a ete teste sur cette trace** et produit son tableau complet, plafond test
retest, exactitude normalisee, calibration et exactitude par bloc, sans erreur :

```
.venv/bin/python analyses/a11_evaluer_twin.py --suffixe smoke --conditions C3-Twin --sans-baselines
```

Il a aussi ete teste, avant tout appel de modele, sur une trace **synthetique** de 30
personnes et 2 456 appels par condition, avec les baselines et les references des auteurs.
Sur cette trace il retrouve les chiffres de a2 a moins d'un demi point : B2 argmax 0,5306
contre 0,5301, B1 argmax 0,5229 contre 0,5184, B0 mode 0,5188 contre 0,5216, GPT-4.1-mini
persona complet 0,5444 contre 0,5530, sur 30 personnes au lieu de 2 058. Le controle
d'alignement entre le fichier humain formate et le catalogue vaut 1,0000.

---

## 6. Debit projete et ce que la nuit peut produire

### 6.1 Le calcul

Toutes les mesures ci-dessus ont ete prises **sous contention** avec le serveur a5. Le run
complet tournera **seul**. Le facteur de correction est estime a 2 : a3 mesure 787 tokens
par seconde de prefill a 3 029 tokens sur la meme machine et le meme modele, alors que le
smoke test mesure 455 tokens par seconde cumules a 2 048 tokens en presence du second
serveur. [PROBABLE] Le facteur reel peut se situer entre 1,5 et 2,5, et aucune mesure seule
n'a pu etre prise, l'ordre etant de ne pas relancer de serveur.

Cout par personne, machine seule, en divisant par deux les mesures sous contention
[PROBABLE] :

| Condition | Prefixe | Prefill | 81 appels | Total par personne | 150 personnes |
|---|---|---|---|---|---|
| **C3b-Twin** | 8 000 tokens | 17 s | 36 s | **53 s** | **2 h 13** |
| **C2-Twin** | 1 084 tokens | 2 s | 20 s | **22 s** | **55 min** |
| **C3-Twin** | 27 515 tokens | 175 s | 84 s | **259 s** | **10 h 47** |

Le total des trois conditions completes est de **14 heures de calcul**. La nuit n'en offre
pas le quart.

### 6.2 La fenetre reellement disponible

Le run a5 a demarre a 22 h 45 pour 44 700 appels sur deux conditions. Aux debits observes
dans son journal, environ 11 000 appels par heure pour sa condition demographique et 5 000
pour sa condition d'enquete, il se termine entre **05 h 30 et 06 h 00**, retard du smoke
test compris. [PROBABLE] La fin dure de a11 etant a 06 h 15, cela laisse **quinze a
quarante-cinq minutes**, et non deux heures.

Projection, partage 70 / 30 entre C3b-Twin et C2-Twin [PROBABLE] :

| Si a5 finit a | Fenetre a11 | C3b-Twin | C2-Twin | Intersection evaluable |
|---|---|---|---|---|
| 05 h 30 | 45 min | 31 min, 35 personnes | 14 min, 38 personnes | **environ 35 personnes** |
| 05 h 45 | 30 min | 21 min, 23 personnes | 9 min, 25 personnes | environ 23 personnes |
| 06 h 00 | 15 min | 10 min, 11 personnes | 5 min, 13 personnes | environ 11 personnes |

**Il faut le dire sans habillage : dans le meilleur des cas la nuit produit une comparaison
sur une trentaine de personnes, dans le pire sur une dizaine.** A trente personnes,
l'intervalle de confiance a 95 pour cent sur l'exactitude vaut environ plus ou moins 4
points, ce qui suffit a separer un agent d'une baseline mais pas a departager deux agents
proches. A dix personnes il ne separe plus rien.

La cause n'est pas un defaut d'organisation, elle est mesuree en section 3 : le persona de
Twin-2K-500 coute dix fois plus cher en prefill que celui du GSS, et la machine ne peut pas
porter les deux jeux la meme nuit. **La conclusion a acter est que Twin-2K-500 demande sa
propre nuit**, et la question 1 de la section 9 la pose.

Si a5 se termine plus tot que prevu, le temps gagne va d'abord a C3b-Twin, puis a C3-Twin.
Aucune intervention n'est necessaire.

### 6.3 Ce qui s'est reellement passe, et ou en est le run

| Heure | Evenement |
|---|---|
| 22 h 47 | smoke test lance sur le port 8199, apres verification que le run a5 etait en cours |
| 22 h 58 | smoke test arrete apres 8 appels, sur ordre de l'orchestrateur : les deux serveurs se disputaient le GPU et le debit de a5 etait tombe a environ 1 700 appels par heure |
| 23 h 05 | run a11 lance en attente derriere a5, PID 54981, fin dure 06 h 15, toutes verifications hors ligne passees |
| 23 h 45 | la file de nuit est reecrite en v3 et **reporte Twin-2K-500 a une autre nuit**, au motif que quinze personnes n'auraient rien donne. C'est la conclusion de la section 6.2, prise au serieux |
| vers 00 h 40 | le processus a11 en attente est tue par la pression memoire de la machine, en meme temps que trois taches de surveillance. Le journal s'arrete sur « Attente de sa fin », sans trace d'erreur |
| 00 h 55 | constat fait. **Aucun processus a11 n'est relance** : la file de nuit a repris la main sur le sequencement, et un second processus en attente aurait pu lancer un serveur concurrent |

Dans la file v3, a11 ne figure plus qu'en **repli** : elle le lance, sans `--attendre-a5` et
avec `--fin 07:30`, seulement si `analyses/a21_extension_c2.py` est absent au moment voulu.
Ce mode de lancement ne passe pas par la fonction d'attente, donc personne ne verifie a la
place du script qu'aucun serveur ne tourne. **Un garde fou inconditionnel a ete ajoute pour
cela** : le script refuse desormais de demarrer si un `llama-server` existe, quel que soit
son port et quel que soit le mode de lancement, et sort avec un message explicite. Verifie
en conditions reelles a 00 h 52, le serveur de a5 etant actif.

Le fichier `data/traces/a11-run.pid`, qui pointait vers le processus mort, a ete retire :
un fichier PID qui survit a son processus est un piege pour le lecteur du matin et pour
toute file qui le consulterait.

**Ce qui reste sur le disque et reste valable** : `data/traces/a11-personnes.csv`, les 150
personnes tirees, deterministe et rejouable ; `data/traces/a11-C3-Twin-p1-smoke.jsonl`, les
8 appels du smoke test ; `resultats/a11_twin_resultats-smoke.json`, l'evaluation de cette
trace.

### 6.4 Ce qu'il faut faire la prochaine nuit

Une nuit dediee, sans partage avec le GSS. La commande, telle quelle :

```
cd ~/Desktop/Code/Projets/popsim
nohup .venv/bin/python analyses/a11_agents_locaux_twin.py --fin 07:30 \
    > data/traces/a11-run.log 2>&1 &
```

Sans `--attendre-a5`, puisque rien ne precede. Le garde fou refusera de demarrer si un
serveur traine. Avec sept heures pleines et machine libre, la projection de la section 6.1
donne C3b-Twin et C2-Twin completes sur les 150 personnes en environ trois heures, puis
C3-Twin sur **environ cinquante-cinq personnes** dans les quatre heures restantes. C'est
assez pour la comparaison a modele egal d'information sur la fidelite, et insuffisant pour
le sous score de variance par groupe demographique, qui demande les 150.

Deux mesures a prendre en tete de cette nuit la, elles coutent dix minutes et peuvent tout
changer : le debit de prefill **machine seule** a 8 000 et a 27 500 tokens, et l'effet de
`-b 4096 -ub 2048` sur ce meme prefill. Voir les points 2 et 3 de la section 8.

---

## 7. Commande d'evaluation du matin

```
cd ~/Desktop/Code/Projets/popsim
.venv/bin/python analyses/a11_evaluer_twin.py
```

Sortie : trois tableaux sur la sortie standard et `resultats/a11_twin_resultats.json`.

Par defaut l'evaluateur prend **C3b-Twin et C2-Twin**, et restreint toutes les methodes a
l'intersection des personnes et des cellules couvertes par ces deux conditions.

| Colonne | Definition |
|---|---|
| exactitude | part des items secrets correctement predits, moyenne par personne |
| IC 95 % | bootstrap a 2 000 tirages, **l'unite de reechantillonnage est la personne** |
| normalise | exactitude divisee par le plafond test retest **de ces memes personnes** |
| diversite | somme des entropies predites sur somme des entropies humaines, memes items |
| paires | accord par paires, indice de Simpson |

Methodes dans le meme tableau : nos conditions, GPT-4.1-mini `default` et `demo_only`, B0
mode, B0 tirage, B1 argmax, B1 tirage, B2 argmax, B2 tirage, et le retest humain qui est le
plafond.

Le deuxieme tableau donne **l'exactitude par bloc du catalogue**, au niveau de la cellule,
pour toutes les methodes. Il repond a la tache 4 de a8 : sur Twin, tout l'avantage de
GPT-4.1-mini sur B2 vient des 40 items de preferences de prix, et il perd sur les blocs
d'heuristiques et de biais. **Le bloc des prix est le bloc de contamination possible** : si
un modele local de 4 milliards de parametres y garde le meme avantage que GPT-4.1-mini,
c'est que la connaissance des produits vient du pre entrainement et non du persona. Ce
chiffre est une part de cellules justes et non une moyenne par personne, parce que la
plupart des blocs de la vague 4 ne comptent qu'un item ; il n'est pas comparable au chiffre
global et les deux ne doivent jamais etre melanges.

Le troisieme tableau, reserve a nos conditions parce qu'elles seules produisent une
distribution complete : exactitude esperee en tirage, c'est a dire la probabilite moyenne
attribuee a la vraie reponse ; confiance moyenne, c'est a dire la probabilite moyenne de la
modalite predite ; ecart de calibration entre les deux ; erreur de calibration esperee sur
dix tranches.

Variantes utiles :

```
# la comparaison a modele egal d'information, si C3-Twin a eu du temps.
# Attention : elle ramene TOUTES les methodes a la population de C3-Twin, la plus petite.
.venv/bin/python analyses/a11_evaluer_twin.py --conditions C3b-Twin,C2-Twin,C3-Twin

# le cout de la troncature, persona complet contre persona tronque, memes personnes
.venv/bin/python analyses/a11_evaluer_twin.py --conditions C3-Twin,C3b-Twin

# une seule condition, sur toute sa population, au prix de la comparabilite
.venv/bin/python analyses/a11_evaluer_twin.py --conditions C3b-Twin

# n'evaluer que les personnes couvertes a 90 pour cent au moins
.venv/bin/python analyses/a11_evaluer_twin.py --couverture-min 0.9
```

**A lire avant de citer un chiffre.** La population evaluee sera plus petite que 150. Le
tableau donne la colonne `n`, le JSON donne la liste exacte des `personnes_evaluees` et le
nombre de cellules. Un chiffre a 60 personnes n'est pas faux, il est moins precis, et son
intervalle de confiance le dit. Le plafond de normalisation est recalcule sur ces personnes
la, jamais repris du 0,7119 publie sur les 2 058.

Verifier aussi, dans le JSON, `qualite_des_appels` : masse minimale, masse mediane et
nombre d'appels rejetes par condition. Une masse mediane qui s'effondre en dessous de 0,9
invaliderait la lecture des probabilites, comme en a3 section 4.5.

---

## 8. Ce que je n'ai pas pu verifier

1. **C2-Twin et C3b-Twin n'ont jamais tourne contre un serveur.** Le smoke test a ete
   interrompu apres la seule condition C3-Twin. La construction de leurs prompts, la
   troncature sur frontiere de question et le rendu des demographies sont verifies hors
   ligne, sur les 294 personas, mais aucune de ces deux conditions n'a produit un seul
   appel de modele. C'est la limite la plus serieuse de cette preparation.
2. **Aucun debit n'a ete mesure machine seule.** Tous les chiffres de duree de la section 3
   sont pris pendant que le serveur a5 occupait le GPU. Le facteur de correction de 2
   applique en section 6 est une estimation, pas une mesure.
3. **L'effet des options `-b` et `-ub` sur un prefill long n'est pas teste.** a3 section 4.7
   mesure que `-b 4096 -ub 2048` degrade le debit de 30 pour cent, mais sur un contexte de
   3 029 tokens ou le calcul est domine par le decodage. A 27 500 tokens le calcul est
   domine par le prefill et la conclusion pourrait s'inverser. C'est le levier le moins cher
   a tester, dix minutes de banc, et il pourrait changer la faisabilite de C3-Twin.
4. **La passe 2, ordre inverse des modalites, n'est pas lancee.** a3 section 3.4 la declare
   non negociable comme parade au biais de position. La nuit ne suffit deja pas pour la
   passe 1. Le script la prend en charge par `--passe 2` et l'evaluateur moyenne
   automatiquement les passes disponibles dans le repere des codes de modalite. **Le biais
   de position n'est donc pas neutralise dans ce run.**
5. **La representativite des 294 personas disponibles.** Le fichier
   `wave_persona_chunk_001.parquet` est le seul chunk telecharge en local, il contient 294
   des 2 058 personnes. Leurs identifiants vont de 2 a 2 056 et se repartissent en 61, 56,
   52, 62 et 63 sur les cinq plis, ce qui est compatible avec un tirage aleatoire mais ne le
   prouve pas. Nos 150 personnes sont donc un tirage aleatoire **d'un sous ensemble**, ce
   qui est plus faible qu'un tirage aleatoire du jeu complet.
6. **L'accord par paires manquera sur 5 items.** `a2_commun.accord_par_paires` exige 50
   repondants par item. Parmi nos 150 personnes, 5 items sur 108 en comptent moins, le
   minimum etant 47, a cause des experiences inter sujets. Ces items sortent de la moyenne.
   `a2_commun` n'a pas ete modifie.
7. **La mise en forme des prompts des auteurs.** Leur code de simulation n'a pas ete lu. Je
   ne sais pas s'ils presentent les modalites etiquetees par des lettres, dans quel ordre, ni
   avec quelle consigne. La comparaison a GPT-4.1-mini est donc exacte sur l'information
   donnee et **approximative sur la mise en forme**.
8. **Le comportement du modele sur les enonces les plus longs.** Les problemes d'Allais, de
   la maladie asiatique et de proportion dominance font plusieurs centaines de mots. La
   masse sur les lettres est tracee a chaque appel, mais aucune mesure item par item n'a pu
   etre prise avant le run.
9. **Le run n'a produit aucun appel.** Tout ce qui suit le smoke test est projection. Les
   trois conditions completes, la reprise apres interruption, la fin dure et l'ecriture du
   marqueur `RUN TERMINE` sont ecrites et relues mais jamais exercees de bout en bout.
10. **La robustesse du processus en attente.** Il a ete tue par la pression memoire de la
    machine pendant qu'il attendait, sans rien ecrire dans son journal. Le script charge les
    donnees et construit les 150 personas **avant** de se mettre en attente, ce qui lui fait
    tenir plusieurs centaines de Mio pendant des heures pour rien. Charger apres l'attente
    plutot qu'avant le rendrait beaucoup moins vulnerable, au prix de decouvrir une erreur
    de donnees a 05 h du matin plutot qu'a 23 h. Ce compromis n'est pas tranche et la
    modification n'est pas faite.

---

## 9. Questions ouvertes pour Simon

1. **Le mur du prefill, et la nuit dediee.** Sur cette machine, un persona de 27 500 tokens
   coute 175 secondes de calcul avant la premiere question, et 150 personnes coutent une
   nuit entiere pour une seule condition. Partager la nuit avec le GSS ramene a11 a une
   trentaine de personnes au mieux. Quatre sorties existent et elles ne se valent pas :
   moins de personnes, un persona plus court, un modele plus petit, ou **une nuit dediee a
   Twin-2K-500**. Le calcul de puissance de METHODOLOGIE E1.3 dit 13 personas pour detecter
   un ecart de 0,09 et 42 pour 0,05, donc la fidelite se contenterait de 50 personnes ;
   c'est le sous score de variance par groupe demographique qui demande 150. Laquelle des
   quatre sorties prend on ?
2. **C3b-Twin est elle une condition publiable ou un pis aller ?** Elle donne au modele 42
   des 173 questions de la personne. Elle reste comparable a nos baselines et au plafond
   humain, mais elle **cesse d'etre comparable a GPT-4.1-mini a information egale**, qui est
   pourtant l'argument le plus fort de cette experience. La publier reviendrait a annoncer
   un ecart dont une partie vient de la troncature.
3. **La passe 2 doit elle etre entrelacee sur Twin ?** Sur le GSS, le prefixe est court et
   lancer la passe 2 separement ne coute presque rien. Sur Twin le prefixe coute 175
   secondes et la passe 2 ne change que le bloc question : **la lancer dans la foulee, sur
   la meme personne et le meme cache, ne coute que le decodage, soit un dixieme du cout
   d'une passe separee.** Faut il modifier le protocole pour Twin, et si oui, la passe 2
   devient elle obligatoire puisqu'elle est presque gratuite ?
4. **Le bloc des prix comme signal de contamination.** L'evaluateur rapportera l'exactitude
   des 40 items de preferences de prix separement. Quel ecart, et par rapport a quelle
   reference, ferait conclure a de la contamination plutot qu'a une competence ? Sans un
   seuil decide avant de voir le chiffre, la lecture sera post hoc.
5. **Le denominateur.** Le plafond test retest sera calcule sur les personnes reellement
   evaluees, pas sur les 2 058 du jeu. Confirmer que c'est bien ce qui doit etre publie, et
   que le nombre de personnes doit figurer a cote de chaque score normalise.

---

## 10. Fichiers produits

| Chemin | Contenu |
|---|---|
| `analyses/a11_agents_locaux_twin.py` | le run, trois conditions, file d'attente, reprise |
| `analyses/a11_evaluer_twin.py` | l'evaluation, global, par bloc et calibration |
| `data/traces/a11-personnes.csv` | les 150 personnes, `pid`, `index`, `pli` |
| `data/traces/a11-personas-tokens.csv` | longueur en tokens et questions gardees, par personne |
| `data/traces/a11-<condition>-p1.jsonl` | une ligne par appel, sans la vraie reponse |
| `data/traces/a11-run.log` | journal du run, PID ecrit dans `a11-run.pid` pendant l'execution |
| `data/traces/a11-smoke.log`, `a11-C3-Twin-p1-smoke.jsonl` | le smoke test, 8 appels |
| `resultats/a11_twin_resultats.json` | la sortie de l'evaluateur |
| `resultats/a11_twin_resultats-smoke.json` | la meme, sur la trace du smoke test |

Aucune microdonnee n'est versionnee, `data/` est dans le `.gitignore`. La trace ne contient
pas la vraie reponse de la personne : l'evaluation la relit dans `data/`, conformement a la
position par defaut de METHODOLOGIE.
