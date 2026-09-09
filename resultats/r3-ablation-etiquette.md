# R3. La vraie ablation de l'etiquette : ce qui est prepare, lance et attendu

Etat au **8 septembre 2026, 22:50 CEST**. Ce rapport est ecrit AVANT que le run ait
produit une seule ligne de trace : R3 ne peut pas demarrer avant que R2 libere la machine,
vers 05:47 le 9 septembre. Il decrit donc le dispositif, ses verifications hors ligne, sa
projection de debit et la commande du matin. La section de resultats sera ecrite par
l'agent qui relira `data/traces/r3-*.jsonl` apres 08:00.

Convention de marquage : **[MESURE]** une valeur produite par un calcul fait ici,
**[CONFIRME]** un fait verifie sur un fichier ou une commande, **[PROBABLE]** une lecture
argumentee sans recalcul, **[HYPOTHESE]** le reste.

---

## 1. Ce que R3 corrige

`resultats/a45-relecture-adverse-2.md`, section 0, objection bloquante numero 1 : C2 et C3
n'echangent pas l'etiquette, ils echangent toute leur entree. C2 porte les onze attributs
demographiques et aucune reponse de la personne ; C3 porte les ~119 reponses et aucune
demographie. Huit textes du dossier appellent ce contraste une ablation.

Verifie ici, sans intermediaire, par egalite de chaines sur les prompts effectivement
construits pour la premiere personne de l'echantillon et le premier bloc [MESURE] :

| condition | caracteres | lignes demographiques | paires question reponse |
|---|---|---|---|
| C2 (a5) | 591 | 11 | 0 |
| C2S (R3) | 501 | **9** | 0 |
| C3 (a5) | 19 250 | **0** | 119 |
| C3E (R3) | 19 608 | **11** | 119 |
| C3ES (R3) | 19 518 | **9** | 119 |

C3E est C3 plus 358 caracteres : les onze lignes demographiques, et rien d'autre. C2S est
C2 moins 90 caracteres : les deux lignes politiques, et rien d'autre. C'est la seule
manière d'ecrire « seule l'etiquette bouge » sans repeter l'erreur que a45 vient de
trouver.

## 2. Page de plan

`resultats/r3-preenregistrement.md`, **horodatee du 8 septembre 2026 a 22:30:01 CEST
(epoch 1788899401)**, ecrite avant le moindre appel de modele de langage de R3 et non
modifiee ensuite [CONFIRME, `date` de la machine].

Elle contient : les trois conditions et leur construction ; le budget et la regle de
partage entre C3E et C2S ; H1 (quatre sous hypotheses, **dirigees vers la BAISSE de la
chute sous permutation**, pas vers la hausse), H2 (cinq), H3 (une) ; les mesures sous
**deux segmentations**, avec et sans ideologie, comme a45 objection 2 l'exige ; Holm par
famille, IC bootstrap apparie sur les personnes ; les **criteres de chute** ; et le
tableau « ce que chaque issue change a MODELE-DU-MONDE 10.4 ».

Reserve deja ecrite dans la page de plan et repetee ici : popsim n'est pas sous suivi de
version. L'horodatage est celui de la machine, rien d'autre ne l'atteste.

## 3. Registre du modele

| champ | valeur | source |
|---|---|---|
| modele | Qwen3-4B-Instruct-2507 | `data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf`, le meme fichier que C2 et C3 de a5 [CONFIRME] |
| quantification | Q4_K_M | registre de `r2_rares_apparie.MODELES["qwen4"]` |
| gabarit | qwen, variante `answer` | `gabarit_qwen` de a5, le prompt s'arrete sur `Answer:` sans espace final |
| coupure publiee | **aucune** | carte de modele, rapport technique et documentation muets |
| version de prompt ecrite en trace | `r3-p1-qwen4-answer` | ligne de trace |
| version de llama-server | relevee au demarrage, ecrite dans `data/traces/r3-run.log` | non disponible avant le run |

Le gabarit et la variante de fin sont **fixes, jamais sondes**. R2 sonde parce qu'il change
de modele ; R3 garde le modele de a5 et doit rester comparable caractere pour caractere aux
traces `a5-C2-p1.jsonl` et `a5-C3-p1.jsonl`. Si la masse de probabilite portee par les
lettres tombe malgre tout, le smoke test arrete le run au lieu de changer le gabarit.

## 4. Verification hors ligne des prompts, quarante controles

`.venv/bin/python analyses/r3_ablation_etiquette.py --verification-seule`, aucun serveur
allume, **40 controles sur 40 passes**, 22:35:37 le 8 septembre [MESURE, journal dans
`data/traces/r3-verification.log`]. Les onze qui portent sur la question de a45 :

- C3E contient le **corps exact de `systeme_c2`** (egalite de chaines, pas relecture) ;
- C3E contient le **corps exact de `systeme_c3`** ;
- C3E est **exactement** `PREAMBULE + demo + reponses + CONSIGNE`, sans un caractere de
  plus ;
- les **onze** libelles demographiques sont presents et **dans l'ordre de a5** ;
- le bloc demographique **precede** le bloc de reponses ;
- **aucun item du bloc secret** ne figure dans le contexte de C3E, teste sur les dix items
  cibles du premier bloc ; le contexte compte **119 paires question reponse** ;
- C3E et C3 ont le **meme nombre** de paires question reponse ;
- C2S ne contient **ni `Political ideology` ni `Political party`** ;
- les **neuf** lignes de C2S sont celles de C2, **caractere pour caractere** ;
- C2S est C2 moins **exactement deux** lignes, et ne contient aucune reponse d'enquete ;
- C3ES ne contient ni ideologie ni parti, et contient bien les 119 reponses.

Les vingt neuf autres : echantillon identique a `a5-personnes.csv` (150 personnes, 30 par
pli) ; 58 items de famille repartis **10/12/14/10/12** sur les cinq blocs, donc cinq
prefixes par personne ; 58 appels et le bon nombre de prompts systeme par personne pour les
trois conditions ; reprise sur trace tronquee ; fin dure calculee en epoch **avec le jour**
(bascule au lendemain verifiee) ; les cinq verdicts du smoke test sur masses synthetiques ;
presence du GGUF et des deux traces de reference.

Extrait du prompt C3E reellement construit, premiere personne, premier bloc :

```
You are simulating one specific person answering a survey. Answer exactly as this
person would answer, not as you would.

Here is what is known about this person:
- Age: 35 - 44
- Census division: middle atlantic
- Political ideology: extremely liberal
- Political party: independent, close to democrat
- Education: high school
- Race: white
- Ethnicity: White/Caucasian
- Gender: female
- Household income: Less than $25,000
- Neighborhood: Urban
- Sexual orientation: Bisexual

Here is how this person answered other questions of the same survey.

Q: Are we spending too much, too little, or about the right amount on "space exploration"?
A: About right
...
```

et le prompt C2S complet, meme personne :

```
You are simulating one specific person answering a survey. Answer exactly as this
person would answer, not as you would.

Here is what is known about this person:
- Age: 35 - 44
- Census division: middle atlantic
- Education: high school
- Race: white
- Ethnicity: White/Caucasian
- Gender: female
- Household income: Less than $25,000
- Neighborhood: Urban
- Sexual orientation: Bisexual

Answer with a single capital letter, the label of the option you choose. Give no
explanation and no other text.
```

## 5. Verification hors ligne de l'evaluateur, sur les traces existantes

`.venv/bin/python analyses/r3_evaluer.py --essai-sur-a5 --suffixe=-essai`, 50 s, aucun
appel de modele. Deux contrastes de controle, sur les **150 personnes** et les **58 items
de famille** :

**Placebo.** La trace `a5-C3-p1.jsonl` lue deux fois sous deux noms. Les neuf mesures
donnent un effet de **0,0000 exactement**, IC [0,0000 ; 0,0000] [MESURE]. C'est le controle
qui dit que le chemin de lecture, la restriction aux 58 items, l'appariement des personnes
et le bootstrap ne fabriquent aucun ecart par eux memes.

**Reference.** C2 contre C3, c'est a dire le contraste de conditionnement que le dossier
appelle a tort une ablation, restreint aux 58 items [MESURE] :

| mesure | C2 | C3 | effet |
|---|---|---|---|
| chute sous permutation, S_ideo | **-0,0020** | 0,0931 | -0,0951 |
| chute sous permutation, S_gra (sans ideologie) | 0,0297 | 0,0800 | -0,0503 |
| ratio inter, axe ideologie | **8,514** | 0,762 | +7,752 |
| ratio inter, axe genre x race x age | 0,779 | 0,820 | -0,041 |
| ratio intra, axe ideologie | 0,254 | 0,669 | -0,415 |
| rarete de groupe sur personne (a31) | **4,446** | 0,436 | +4,010 |
| rappel des cellules rares | 0,129 | 0,220 | -0,091 |
| exactitude par personne | 0,566 | 0,625 | -0,059 |

Trois lectures, toutes utiles pour interpreter R3 quand il sera la.

1. Sur les 58 items, C2 a une chute sous permutation **negative** (-0,002) : permuter les
   personnes a l'interieur de leur camp lui fait gagner de l'exactitude, au bruit pres.
   C'est un gabarit de groupe parfait, et c'est la quantite que R3 doit voir bouger.
2. **L'objection 2 de a45 se reproduit ici sur nos propres conditions** : le rapport de la
   chute entre C3 et C2 vaut **-46 pour un** sous la segmentation ideologique, et **2,7
   pour un** sous la segmentation genre x race x age. Le choix de l'axe change l'ampleur
   d'un ordre de grandeur. Les deux seront publiees pour R3, et aucun verdict ne sera
   retenu si le signe change de l'une a l'autre.
3. Le ratio inter de C2 sur l'axe ideologie, 8,51, retrouve le 8,16 a 8,51 que a1 et a23
   lisent sur ce meme axe : l'evaluateur reproduit le dossier sans avoir ete cale dessus
   [MESURE].

Fichiers : `resultats/r3-couverture-essai.csv`, `r3-tableau-essai.csv`,
`r3-contrastes-essai.csv`, `r3-permutation-essai.csv`, `r3-rarete-essai.csv`,
`r3-controles-essai.csv`.

## 6. Le dispositif de la nuit

### La file

`analyses/file_nuit_3.sh`, **lancee par nohup a 22:42:57, PID 96616** [CONFIRME, `ps`].
Journal `data/traces/file-nuit-3.log`, PID `data/traces/file-nuit-3.pid`. Elle **ne lance
aucun serveur** et n'en arrete qu'un, celui de R2, par le processus qui le possede.

Gardes horaires, toutes en epoch calcule avec le jour, relevees dans son journal au
demarrage [CONFIRME] :

| evenement | horodatage | epoch |
|---|---|---|
| R2 interrompu par SIGINT | 2026-09-09 05:45:00 | 1788925500 |
| limite d'attente du demarrage de R2 | 2026-09-09 04:00:00 | 1788919200 |
| fin dure de R3 | 2026-09-09 08:00:00 | 1788933600 |

Sa sequence : attendre que `data/traces/r2-run.pid` existe, que le PID soit vivant **et
que sa ligne de commande soit bien celle de `r2_rares_apparie`** (un PID mort est
reattribue, on ne signale jamais un numero seul) ; a 05:45, SIGINT, qui leve un
`KeyboardInterrupt` dans R2 dont le `finally` arrete le serveur et dont la trace est
resumable par (condition, pid, item) ; attendre qu'aucun `llama-server` ne tourne, dix
minutes au plus, puis SIGTERM au serveur restant ; lancer R3.

`pgrep -x` et non `pgrep -f`, pour la raison ecrite dans `file_nuit_2.sh` : un processus
dont la ligne de commande contient la chaine ferait attendre la file indefiniment.

Deux ecarts au cahier des charges, tous deux dans le sens de la prudence et tous deux
journalises quand ils se produisent :

- si R2 est **deja mort** avant 05:45, la file n'attend pas 05:45 pour rien et passe a la
  suite. La contrainte est « un seul serveur », pas « ne rien faire avant 05:45 », et
  attendre laisserait le GPU vide ;
- si 08:00 est **deja passe** au moment de lancer, R3 n'est **pas** lance :
  `heure_de_fin()` de a5 basculerait la cible au lendemain et R3 tournerait vingt quatre
  heures de trop.

Quatre branches testees hors ligne avant le lancement, dans un dossier de traces jetable,
en mode essai ou aucun signal n'est envoye [MESURE] : R2 ne demarre jamais et la limite
tombe ; R2 vivant et le SIGINT est atteint a la bonne seconde ; R2 mort avant l'heure et
aucun signal n'est envoye ; l'attente d'un GPU libre, plafonnee, suivie du SIGTERM.

### Le run

`analyses/r3_ablation_etiquette.py --fin 08:00`, journal `data/traces/r3-run.log`, PID
`data/traces/r3-run.pid`, traces `data/traces/r3-C3E-qwen4.jsonl`, `r3-C2S-qwen4.jsonl`,
`r3-C3ES-qwen4.jsonl`, smoke `r3-smoke-qwen4.jsonl`, resume `r3-resume-qwen4.json`.

Il **refuse de demarrer** si un `llama-server` tourne, comme R2 (fonction
`serveurs_en_cours` importee de `r2_rares_apparie`, jamais recopiee). Il fait un **smoke
test de vingt appels** avant d'engager la nuit, avec le verdict de R2 importe tel quel :
masse mediane sous 0,90, ou masse minimale sous 0,50, ou plus de 25 pour cent d'appels a
modalite absente, et le run s'arrete sans avoir ecrit de trace utile. Il ecrit sa trace
avec `flush` a chaque ligne et `fsync` tous les 200 appels, et il attrape
`KeyboardInterrupt` pour arreter son serveur proprement.

## 7. Projection de debit

Couts unitaires resolus a partir de deux mesures de a5 sur le meme modele, les memes
prompts et la meme machine : C3, 22 350 appels en 274,5 min pour 5 prefixes et 149 appels
par personne ; C3F, 3 498 appels en 78,1 min pour 6 prefixes et 58 appels par personne
[MESURE, `data/traces/a5-run.log` et `a5-familles.log`]. Deux equations, deux inconnues :

- **prefixe de persona long : 8,6 s** ;
- **appel servi par le cache : 0,45 s** ;
- appel de C2S, prompt court : **0,27 s** (13 217 appels/h en regime etabli sur C2).

| condition | prefixes par personne | cout par personne | 150 personnes |
|---|---|---|---|
| C3E | 5 | 69 s | **2,9 h** |
| C3ES | 5 | 69 s | 2,9 h |
| C2S | 1 | 16 s | **0,7 h** |

La fenetre, de 05:47 a 08:00, vaut **2,2 h**. Elle ne couvre pas C3E en entier. La page de
plan fixe donc, avant tout appel, une regle de partage : le run reserve a C2S le temps que
sa projection lui donne, majore de 15 pour cent et plafonne a 45 pour cent du budget, et
donne a C3E une fin intermediaire egale a la fin dure moins cette reserve. La projection de
C2S n'est pas faite avec le cout du prefixe long : le run mesure le cout reel de C2S par
une **sonde de six appels** juste apres le smoke test, parce que projeter un prompt de 501
caracteres avec le prefixe d'un prompt de 19 608 donnerait une reserve trois fois trop
grande, qui tuerait H1 pour sauver H2.

**Attendu : C3E couvre environ 75 a 90 personnes sur 150, C2S les 150, C3ES ne tourne
pas** [ESTIMATION]. Les personnes sont parcourues dans l'ordre de `a5-personnes.csv` dans
les trois conditions, donc les perimetres sont emboites et une troncature coute des
personnes entieres, jamais des items.

Consequence sur la puissance, ecrite d'avance : sur ~80 personnes et 58 items, le nombre de
cellules rares stables sera de l'ordre de 40 (R2 annonce 31 sur 60 personnes et ~78 sur
150). Les contrastes de rarete sont donc declares **secondaires et sous puissants**, et
sont publies hors des familles corrigees par Holm. Le contraste primaire, H1a, porte sur la
chute sous permutation, qui utilise toutes les cellules.

## 8. Commande du matin

Dans cet ordre. Rien ne demande de serveur.

```bash
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim

# 1. Ce que la nuit a fait
tail -40 data/traces/file-nuit-3.log
tail -60 data/traces/r3-run.log
cat data/traces/r3-resume-qwen4.json
wc -l data/traces/r3-*.jsonl

# 2. L'evaluation, tolerante au partiel
.venv/bin/python analyses/r3_evaluer.py --tirages 2000 \
    --tirages-permutation 200 --permutations 200 \
    2>&1 | tee data/traces/r3-evaluation.log

# 3. Les tableaux
column -s, -t resultats/r3-couverture.csv
column -s, -t resultats/r3-contrastes.csv
column -s, -t resultats/r3-permutation.csv
```

Si C3E a moins de 30 personnes completes, l'evaluateur declare le contraste **non teste**
et n'ecrit aucun verdict. La reprise est alors :

```bash
# aucun llama-server ne doit tourner ; le run reprend exactement ou il s'est arrete
.venv/bin/python analyses/r3_ablation_etiquette.py --conditions C3E --fin 12:00 \
    >> data/traces/r3-run.log 2>&1
```

## 9. Ce que je n'ai pas pu verifier

1. **Aucun appel de modele n'a ete fait.** Tout ce qui touche au comportement reel de
   Qwen3-4B sur le prompt C3E est non verifie : la masse de probabilite portee par les
   lettres quand le prompt commence par onze lignes demographiques, le taux de rejet, le
   nombre de modalites absentes du top 40. Le smoke test integre les mesurera, mais
   personne ne les aura vues avant 05:47.
2. **Le debit est projete, pas mesure.** Les couts unitaires viennent de deux equations a
   deux inconnues resolues sur des runs de a5 qui datent de la nuit precedente, avec une
   charge machine differente et un autre programme (i3b) sur les coeurs. Le budget reel de
   C3E peut s'ecarter de 30 pour cent dans les deux sens.
3. **Le nombre de personnes de C3E est une estimation.** Si le smoke test mesure un cout de
   prefixe plus eleve, C3E peut tomber sous 60 personnes, et le contraste principal
   deviendrait trop faible pour trancher. Le rapport final devra le dire au premier
   paragraphe et non en annexe.
4. **L'IC bootstrap du ratio inter est biaise.** Sur le contraste de reference C2 contre
   C3, l'effet ponctuel vaut 7,75 et l'intervalle percentile [3,16 ; 5,88] ne le contient
   pas [MESURE]. C'est une propriete du ratio de sommes de dispersion sous re
   echantillonnage des personnes, pas une erreur de code : les segments se vident, le seuil
   `N_MIN_ITEM` de 30 elimine des items, et la statistique change d'estimand. Le p
   unilateral reste lisible comme test de signe, l'intervalle non. Un bootstrap pivotal ou
   BCa reglerait le point ; il n'est pas ecrit.
5. **La passe 2 n'existe pas pour R3.** Le biais de position des modalites n'est pas
   neutralise, il est seulement constant entre les conditions comparees. Cela suffit pour
   un contraste et pas pour un niveau.
6. **Aucune condition n'est evaluee en tirage.** R3 reste en argmax comme tout le dossier
   (objection 8 de a45). Les distributions sont dans la trace, un tirage se reconstruira
   sans nouvel appel.
7. **Le SIGINT a R2 n'a pas ete essaye sur R2 lui meme.** Les quatre branches de la file
   ont ete testees sur un processus factice ; le comportement reel de `r2_rares_apparie`
   sous `KeyboardInterrupt` est deduit de la lecture de son `finally` et de son ecriture au
   fil de l'eau, pas observe. [PROBABLE, lecture du code]
8. **Rien de tout ceci n'est sous suivi de version.** Ni la page de plan, ni les scripts,
   ni les traces. C'est l'objection ouverte de a45 et R3 ne la corrige pas.
9. **C3ES ne tournera probablement pas**, donc H3, qui separe l'etiquette ideologique de
   l'etiquette demographique dans le regime riche, restera **non testee**. Non testee, pas
   non rejetee.

## 10. Questions ouvertes pour Simon

1. **Quel axe de segmentation devient la mesure principale ?** a44 publie la chute sous
   permutation a l'interieur de l'ideologie, c'est a dire a l'interieur de la variable que
   l'invite contient. a45 montre que sous genre x race x age les chiffres changent d'un
   ordre de grandeur, et le controle de reference ci dessus le reproduit sur C2 et C3
   (rapport -46 pour un contre 2,7 pour un). Publier les deux est honnete mais ne tranche
   pas. Un relecteur demandera laquelle porte la these.
2. **Que faut il conclure si H1a est nulle et H2a verifiee ?** C'est l'issue que je
   considere la plus probable : l'etiquette agirait seule et ne ferait rien ajoutee a 119
   reponses. La these devient plus faible et plus interessante (le gabarit de groupe est ce
   que le modele fait faute de mieux). Est ce que le dossier assume ce retrecissement, ou
   est ce que c'est le moment de changer d'objet ?
3. **Faut il un modele plus gros avant de publier l'ablation ?** R3 tourne sur 4 milliards
   de parametres quantifies en 4 bits. Un relecteur dira que l'effet de l'etiquette depend
   de la capacite du modele a exploiter 119 reponses, et qu'un petit modele sature plus
   vite. Le meme protocole sur gpt-oss-20b coute une nuit de plus.
4. **Quelle est la bonne definition du placebo d'etiquette ?** J'ai retire l'ideologie ET
   le parti, parce que les deux sont fortement associes et qu'une ablation qui laisse le
   parti n'est pas une ablation. Si Simon veut l'analogue exact de v6 contre v8 chez
   Stanford, il faut savoir ce que v6 contenait precisement.
5. **Les huit textes du dossier doivent ils etre corriges avant ou apres R3 ?** a45
   propose de remplacer partout « ablation de l'etiquette » par « contraste de
   conditionnement ». Si R3 tombe a moins de 60 personnes, la correction doit etre faite
   quand meme, et sans pouvoir la remplacer par un resultat.
6. **Combien de personnes faut il pour que ce verrou compte ?** Si C3E couvre 80 personnes,
   l'IC sur la chute sous permutation restera large. Vaut il mieux 80 personnes sur 58
   items, ou 150 personnes sur 20 items d'une seule famille ? Le choix se fait avant la
   prochaine nuit, pas apres.
