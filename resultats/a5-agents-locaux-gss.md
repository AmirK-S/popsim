# a5 : premier run d'agents locaux sur le GSS

Rapport du 7 septembre 2026, ecrit pendant que le run tourne. Chantier de la nuit.

C'est le premier travail du projet qui produit **nos** agents. Jusqu'ici tout, de a0 a a2,
etait une reanalyse des sorties de Stanford et des baselines statistiques. Ici un modele de
langage tourne en local, sur nos prompts, et rend une distribution de probabilite complete
par couple (personne, item), sur exactement le meme decoupage que les baselines de a2.

Scripts : `analyses/a5_agents_locaux_gss.py` (le run), `analyses/a5_evaluer.py`
(l'evaluation). Aucun script existant n'a ete modifie.

---

## 1. Ce qui a ete lance

| | |
|---|---|
| Lancement | 7 septembre 2026 a 22 h 45 min 40 s, heure locale [MESURE] |
| PID du run | note dans `data/traces/a5-run.pid` [MESURE] |
| Journal | `data/traces/a5-run.log` [MESURE] |
| Fin dure | 8 septembre 2026 a 07 h 30, le script s'arrete seul et proprement [CONFIRME] |
| Conditions dans la file | C2 puis C3, passe 1 uniquement |
| Passe 2 de C3 | **pas dans cette file**, drapeau `--passe 2`, a lancer separement |
| Condition C3F, familles | **pas dans cette file**, drapeau `--familles`, voir section 4.4 |
| Echantillon | 150 personnes, 30 par pli, 149 items chacune, soit 22 350 appels par condition |
| Fichier de l'echantillon | `data/traces/a5-personnes.csv`, 150 lignes, ecrit avant le premier appel [MESURE] |

A la fin, le script arrete son `llama-server`, ecrit `data/traces/a5-resume.json` et imprime
la ligne `RUN TERMINE` dans le journal. Un second run peut donc enchainer sur la machine en
surveillant la disparition du PID ou l'apparition de cette ligne. L'arret du serveur est
dans un bloc `finally` : il a lieu meme si le run echoue. [CONFIRME]

**Les deux conditions.**

- **C2, persona demographique seul.** Les 11 attributs de `figure3/data/demographic_summary.csv`
  en clair dans le prompt systeme, sans recodage. Les trois attributs incomplets portent la
  mention explicite `not reported`, meme convention qu'en a2 : omettre la ligne dirait au
  modele autre chose que "non renseigne". Prompt court, 169 a 303 tokens. [MESURE]
- **C3, persona construit sur les reponses d'enquete.** Les ~119 items de contexte du bloc,
  presentes en paires `Q: <libelle> / A: <reponse>`, puis la question secrete. Prompt de
  4 519 a 4 655 tokens. [MESURE] Aucune demographie n'y figure : c'est le regime
  "questionnaire seul" du papier de Stanford, celui ou le modele doit gagner.
- **C3F, persona questionnaire avec la famille retiree.** Ecrite et disponible, pas dans la
  file de cette nuit. Meme persona que C3, mais le contexte est ampute de la **famille
  thematique entiere** de l'item cible, et c'est cette famille qui est predite. Six
  familles, 58 items, listes `FAMILLES` de `a2_baselines_gss.py`, regime identique a
  `analyses/a8_familles.py`. Motif : la tache 2 du rapport a8 montre que les agents
  composite de Stanford battent B2 des que la famille entiere sort du contexte, alors que
  B2 les bat en decoupage aleatoire. C'est donc le regime ou notre C3 a une chance, et le
  chiffre global le masque.

**Le decoupage est celui de a2, sans une ligne de code recrite.** Le script importe
`charger()` et `grille()` de `analyses/a2_baselines_gss.py`, graine 20260903 : 5 plis de
personnes, 5 blocs d'items de 30, 30, 30, 30 et 29 items. Chaque couple (personne, item) est
predit une fois, l'item est secret et les ~119 autres items forment le contexte. Nos agents
sont donc comparables **cellule a cellule** a B0, B1, B2 et aux six conditions d'agents de
Stanford. [CONFIRME]

L'echantillon de 150 personnes est stratifie sur les 5 plis, 30 par pli, graine 20260907
distincte de celle du decoupage pour que changer la taille de l'echantillon ne deplace pas
les plis. La stratification n'est pas cosmetique : B1 et B2 sont evaluees pli par pli et
entrainees sur les autres, un echantillon desequilibre melangerait des tailles
d'entrainement differentes selon la personne.

**Ordre des appels.** Personne par personne, et a l'interieur d'une personne bloc par bloc.
Consequence voulue : si la fin dure tronque le run, ce sont des personnes entieres qui
manquent, jamais des items. Les mesures de a1 sont par item et exigent les 149 items pour
chaque personne retenue. [CONFIRME]

---

## 2. La configuration exacte

Ligne de commande du serveur, relevee sur le processus en cours :

```
llama-server -m data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
  --host 127.0.0.1 --port 8100 -c 65536 -np 8 -ngl 999 \
  --cache-reuse 256 --no-webui -fa on --slot-save-path /tmp/a3-slots \
  --cache-type-k q8_0 --cache-type-v q8_0
```

C'est la configuration de reference de a3 section 4.7, celle qui donne le meilleur chiffre
absolu du balayage. Le client serveur est la classe `MoteurLlama` de
`analyses/a3_banc_inference.py`, etendue par heritage dans `MoteurA5` et non recopiee : le
lancement, l'attente de disponibilite, l'arret et le transport HTTP sont ceux de a3.

| | |
|---|---|
| Modele | Qwen3-4B-Instruct-2507, GGUF Q4_K_M, 2,5 Gio |
| llama.cpp | version 0.3.0, build 10621, commit c1d0e7a00, Metal [MESURE] |
| Python | 3.13.14, via `.venv/bin/python` |
| Contexte | 8 192 tokens par slot, 8 slots, 65 536 au total |
| Cache KV | q8_0 sur K et V, attention fusionnee active |
| Port | 8100, choisi automatiquement parmi les premiers ports libres |
| Flux | un seul, sequentiel. a3 4.7 mesure 24 104 appels/h a un flux contre 21 498 a huit sur cette configuration |
| Parametres d'appel | `n_predict` 1, `temperature` 0, `n_probs` 40, `cache_prompt` true, `post_sampling_probs` false |

**Le gabarit de conversation Qwen est applique**, lecon de a3 section 4.5 :

```
<|im_start|>system
{persona}<|im_end|>
<|im_start|>user
Question. {libelle}
A. {modalite 1}
B. {modalite 2}
...<|im_end|>
<|im_start|>assistant
Answer:
```

Le prompt se termine sur `Answer:` **sans espace final**. C'est le token ` A` qui est score,
espace comprise, pas le token `A`. Sur gpt-oss-20b l'espace finale faisait tomber la masse
de probabilite de 0,999 a 0,84 (a3 4.5) ; la precaution est reprise ici.

Le prompt est en anglais, comme le materiel d'enquete lui meme. Les libelles de question et
de modalite sont recopies tels quels de `figure2/data/question_master/gss/main.csv`, sans
traduction ni reformulation.

**L'ordre des modalites suit la nomenclature de `main.csv`, verifie.** Les identifiants de
question y sont en majuscules et en minuscules dans les fichiers de reponses, les libelles
de modalite y sont capitalises et en minuscules dans les reponses : les deux correspondances
sont faites une seule fois, au chargement. Les 149 items cibles ont tous un libelle dans
`main.csv`, et **toutes** les reponses observees en vague 1 et en vague 2 tombent dans les
modalites declarees une fois la casse ramenee. [MESURE, controle sur les 177 items du
fichier] L'item cible le plus riche est `income`, a 12 modalites, d'ou 13 lettres declarees.

---

## 3. Le scoring, et les quatre controles

Traitement (a) de a3 section 3.4 : etiquettes courtes d'un token, lues a une seule position,
dans le meme contexte gauche pour toutes les modalites. Le biais de longueur disparait par
construction. Quatre controles sont en place.

**Controle 1, identifiants de tokens distincts.** Verifie par la methode imposee : on encode
`prompt`, puis `prompt + " A"`, et on prend le token qui s'ajoute. On n'encode jamais " A"
isolement. Le script leve une exception si l'ajout modifie le prefixe, si la lettre fait
plus d'un token, ou si deux lettres partagent un identifiant. Resultat, identique dans les
trois runs de la soiree :

```
A=362  B=425  C=356  D=422  E=468  F=434  G=479   [MESURE]
```

Sept identifiants distincts pour les sept premieres lettres, verification faite pour chaque
valeur de K rencontree (2, 3, 4, 5, 6 et 7 dans le smoke test). [MESURE]

**Controle 2, masse de probabilite sur les K lettres avant renormalisation.** Enregistree a
chaque appel dans la trace, seuil de rejet 0,5.

| condition | masse minimale | masse mediane | appels rejetes | modalites absentes du top 40 |
|---|---|---|---|---|
| C2, 90 appels | 0,9999 | 1,0000 | 0 | 0 |
| C3, 90 appels | 0,9997 | 1,0000 | 0 | 0 |
| C3, 900 appels de la mesure de debit | | | 0 | 0 |

[MESURE] C'est nettement au dessus des 0,895 a 0,969 de a3 sur prompt brut. Le gabarit de
conversation et la consigne de format expliquent l'ecart. [PROBABLE]

**Controle 3, les probabilites ne dependent pas de la temperature.** Verification faite parce
que le run tourne a temperature 0 et qu'un lecteur pourrait croire que la distribution en est
un artefact. Meme prompt, meme question, trois temperatures :

```
spdeg*   T=0,0  p(F)=1,0000     prayer   T=0,0  p(A)=1,0000
spdeg*   T=1,0  p(F)=1,0000     prayer   T=1,0  p(A)=1,0000
spdeg*   T=2,0  p(F)=1,0000     prayer   T=2,0  p(A)=1,0000
```

[MESURE] Avec `post_sampling_probs: false`, llama-server renvoie les log-probabilites du
modele avant echantillonnage. La temperature n'y touche pas. Les distributions enregistrees
sont donc bien celles du modele.

**Controle 4, les identifiants sont lus par identifiant et non par chaine.** `top_logprobs`
renvoie bien un champ `id` sur cette version de llama.cpp, exemple releve :
`{'id': 434, 'token': ' F', 'bytes': [32, 70], 'logprob': -2.38e-07}`. [MESURE] La lecture se
fait par identifiant, avec repli sur la chaine exacte ` A` si le champ manquait. Jamais par
un `strip()`, qui confondrait `A` et ` A`.

**Ce que la trace contient, une ligne par appel.** `pid`, `item`, `condition`, `passe`,
`pli`, `bloc`, `version_prompt`, `modele`, `quantification`, `ordre_modalites`, `duree_ms`,
`masse_lettres`, `rejet`, `modalites_absentes`, `distribution` (dictionnaire modalite vers
probabilite renormalisee), `argmax`, `tokens_prompt`, `tokens_calcules` (tokens reellement
recalcules, donc le complement du cache), `prompt_ms`.

**Ce que la trace ne contient pas : la vraie reponse de la personne.** L'evaluateur la relit
dans `data/`. C'est la position par defaut de METHODOLOGIE tant que le point de droit n'est
pas tranche : trace expurgee, renvoi au fichier officiel par identifiant.

**Index unique et reprise.** La cle est (condition, passe, pid, item). Une relance relit la
trace, saute les appels deja faits et reprend. Verifie en conditions reelles : un second
lancement sur une trace de 90 lignes a bien affiche `90 appels deja faits` et n'a ecrit que
les 5 nouveaux appels demandes. [MESURE] Les lignes tronquees par un arret brutal sont
ignorees sans faire echouer la reprise. L'ecriture est incrementale avec `flush` a chaque
ligne et `fsync` tous les 200 appels.

---

## 4. Le debit mesure, et la projection

### 4.1 La mesure

Mesure dediee sur **900 appels C3**, 15 personnes et 2 blocs, soit 30 prefixes pour 900
appels. C'est exactement le rapport du run reel, 5 prefixes pour 149 appels.

| | |
|---|---|
| Duree | 11,0 minutes pour 900 appels |
| **Debit global** | **4 921 appels par heure** [MESURE] |
| Appels servis par le cache de prefixe | 870 sur 900, mediane 313 ms, 52 tokens recalcules |
| Appels payant le prefixe complet | 30, mediane 12 339 ms, 4 617 tokens |
| Debit de prefill mesure | 380 tokens par seconde [MESURE] |
| Part du temps passee dans les prefixes | 57 pour cent [MESURE] |
| Appels rejetes | 0 |

Le cache de prefixe fonctionne : 52 tokens recalcules la ou le prompt en compte 4 617, soit
le seul bloc utilisateur qui change d'une question a l'autre. [MESURE] C'est ce que l'ordre
des appels cherchait a obtenir.

Le debit se degrade au fil de la mesure, par fenetres de 150 appels :

| fenetre | appels par heure |
|---|---|
| 0 a 150 | 7 648 |
| 150 a 300 | 5 344 |
| 300 a 450 | 5 126 |
| 450 a 600 | 4 870 |
| 600 a 750 | 4 231 |
| 750 a 900 | 3 791 |

[MESURE] Perte de 50 pour cent en onze minutes. C'est du meme ordre que les 39 pour cent en
dix minutes de a4, avec une aggravation attribuable a la charge de la machine.

### 4.2 La charge de la machine, et pourquoi ce chiffre est un plancher

Le debit de a3, 13 026 appels par heure en configuration reelle, a ete mesure **machine au
repos**. Ce n'etait pas le cas ici, et les charges relevees a chaque etape le montrent :

| moment | charge moyenne sur 1 minute |
|---|---|
| debut de session, 22 h 25 | 5,01 |
| debut de la mesure de debit, 22 h 33 | 3,37 |
| fin de la mesure de debit, 22 h 44 | 21,35 |
| lancement du run, 22 h 45 | 21,22 |
| 22 h 46 | 30,67 |
| 22 h 48 | 8,98 |
| 22 h 50 | 21,04 |

[MESURE] Le processus `bird` d'iCloud, signale au demarrage de la mission, s'est calme.
Ce qui reste est la charge d'autres agents faisant des analyses pandas en parallele sur la
meme machine, ce qui est le fonctionnement normal du poste. Le debit de prefill mesure a
380 tokens par seconde, contre 790 attendus d'apres a3, est coherent avec cette
concurrence. [PROBABLE]

**Le 4 921 appels par heure est donc un plancher mesure sous concurrence, pas le debit de la
machine.** La fourchette 6 400 a 13 000 de a3 et a4 reste plausible si la machine se libere.

### 4.3 La projection

Deux scenarios, les deux mesures ici, aucune extrapolation :

| | debit C2 | debit C3 | duree C2 | duree C3 | total |
|---|---|---|---|---|---|
| Scenario mesure ce soir sous charge | 7 400/h | 4 900/h | 3 h 01 | 4 h 34 | **7 h 35** |
| Scenario machine plus calme | 12 000/h | 8 000/h | 1 h 52 | 2 h 48 | **4 h 40** |

Budget disponible depuis 22 h 45 jusqu'a 07 h 30 : **8 h 45**. Les deux scenarios rentrent,
le premier avec 1 h 10 de marge seulement. [ESTIMATION]

**Decision sur la taille de l'echantillon : 150 personnes, pas 200 ni 250.** La consigne
prevoyait de monter si le smoke test montrait un debit superieur. Il montre l'inverse,
4 921 appels par heure contre 6 400 a 13 000 attendus. Passer a 200 personnes porterait la
projection du scenario bas a 10 h 07, au dela de la fin dure. Rester a 150 avec un run
resumable et un ordre personne par personne est le choix qui protege le resultat : si la
machine cale, ce sont des personnes entieres qui manquent, et les 149 items de chaque
personne mesuree restent complets.

### 4.4 L'incident qui explique la moitie des chiffres de debit

A 22 h 47 min 46 s, **un second `llama-server` a ete lance sur la machine par un autre
agent**, sur le port 8199, avec le meme modele Qwen3-4B, pour un smoke test du run Twin
(`analyses/a11_agents_locaux_twin.py`). Il a tourne jusqu'a 22 h 59. [MESURE, releve sur le
processus, PID 49092, parent 49069]

L'effet sur notre debit est net et mesure :

| fenetre | appels C2 par heure | contexte |
|---|---|---|
| 22 h 50 a 22 h 58 | 1 759 | deux `llama-server` sur le meme GPU |
| 22 h 59 a 23 h 00 | **16 720** | un seul `llama-server`, le notre |

[MESURE] Facteur 9,5 entre les deux regimes. **C'est le chiffre le plus utile de cette
section** : sur cette machine, deux serveurs d'inference simultanes ne se partagent pas le
GPU, ils s'effondrent mutuellement. La consigne de n'en lancer qu'un a la fois n'est pas une
precaution de principe, elle vaut un facteur 9,5. [MESURE]

Consequences pour la lecture de ce rapport. Les 4 921 appels par heure de la mesure de
debit de la section 4.1 ont ete obtenus **avant** cet incident mais sous une charge pandas
elevee ; ils restent un plancher. Le chiffre a retenir pour une machine dediee au run est
plutot **16 700 appels par heure sur C2**. [MESURE, une fenetre d'une minute seulement]

Debit observe sur le run lui meme, condition C2, cumule :

| appels | debit cumule | heure | machine |
|---|---|---|---|
| 200 | 8 200/h | 22 h 46 min 52 s | charge 30, un serveur |
| 400 | 11 333/h | 22 h 47 min 31 s | charge 30, un serveur |
| 600 | 7 402/h | 22 h 50 min 16 s | deux serveurs |
| 1 165 | 16 720/h sur la derniere minute | 22 h 59 min 46 s | un serveur, charge 4 |

[MESURE] Les variations suivent le nombre de serveurs et la charge de la machine, pas le
modele.

### 4.5 La condition C3F, ecrite mais non lancee cette nuit

`--familles` bascule C3 en C3F : le contexte perd la famille thematique entiere de l'item
cible, et c'est cette famille qui est predite. Six familles, 58 items, 8 700 appels pour
150 personnes. Elle **n'est pas dans la file de cette nuit** et voici pourquoi, chiffres a
l'appui.

C3F demande **six prefixes par personne pour 58 appels utiles**, la ou C3 en demande cinq
pour 149. Le prefixe est le poste de cout dominant : il pese deja 57 pour cent du temps de
C3. [MESURE] En reprenant le cout de prefixe mesure, 12,3 s sous charge et environ 5,8 s
sur machine libre :

| | machine chargee | machine libre |
|---|---|---|
| 900 prefixes | 3 h 04 | 1 h 27 |
| 8 700 appels | 0 h 45 | 0 h 29 |
| **total C3F** | **3 h 49** | **1 h 56** |

[ESTIMATION, a partir des couts de prefixe mesures en 4.1] Ajoute aux 4 h 40 a 7 h 35 de
C2 plus C3, C3F ne rentre pas dans les 8 h 45 disponibles dans le scenario charge, et ne
rentre dans le scenario libre qu'a la condition que la machine reste libre toute la nuit,
ce que l'incident de 22 h 47 rend improbable.

**Suite a faire, dans cet ordre.** Si le journal montre `RUN TERMINE` avec les deux
conditions completes avant 05 h 30, lancer :

```
.venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --familles --fin 07:30
```

Sinon, la lancer dans la journee sur une machine libre. Elle est resumable comme les
autres, et son ordre est personne par personne : une troncature coute des personnes
entieres, jamais des items.

**Ce qui a ete verifie sans appel de modele**, la machine etant occupee par le run :
l'enumeration de C3F produit bien 58 appels par personne repartis en six prefixes, et sur
les 116 prompts de deux personnes, **ni l'item cible ni aucun de ses cousins de famille
n'apparait dans le contexte**. [MESURE, controle par recherche du libelle exact de chaque
question dans le texte du prompt systeme] Le meme controle sur C3 confirme que l'item cible
est absent alors que ses cousins sont presents, ce qui est le regime voulu. Le chemin de
scoring de C3F est celui de C3, sans une ligne differente.

---

## 5. Les premiers chiffres du smoke test

Smoke test : 3 personnes, 1 bloc de 30 items, C2 puis C3, 90 appels chacune. L'echantillon
est minuscule, ces chiffres n'ont pas d'intervalle de confiance utilisable. Ils servent a
verifier que la chaine produit quelque chose de sense, pas a conclure.

### 5.1 Exactitude

| condition | exactitude argmax | 90 cellules | duree mediane | tokens de prompt |
|---|---|---|---|---|
| C2, persona demographique | 0,5444 | 3 personnes x 30 items | 105 ms | 169 a 303 |
| C3, persona questionnaire | 0,6556 | 3 personnes x 30 items | 186 ms | 4 519 a 4 655 |

[MESURE] Points de repere de a2 sur 1 052 personnes et 149 items : agents demographiques de
Stanford 0,5818, agents enquete 0,6510, B1 argmax 0,6209, B2 argmax 0,6717. Nos deux
conditions tombent dans le bon voisinage de leurs homologues, avec 90 cellules seulement.
[MESURE] C'est le seul enseignement a en tirer : la chaine n'est pas cassee.

L'evaluateur, lance sur ces memes traces, place C3 a 0,6556 contre 0,7000 pour les agents
enquete de Stanford restreints aux memes 3 personnes et aux memes 30 items, et 0,8444 pour
le plafond humain test retest de ces trois personnes. [MESURE]

### 5.2 Le resultat qui compte deja, et il est desagreable

**Les distributions sont quasi degenerees.**

| condition | entropie moyenne par appel | entropie maximale moyenne | part | appels a p max > 0,99 | ecart de calibration |
|---|---|---|---|---|---|
| C2 | 0,105 bits | 1,590 bits | 6,6 % | 82,2 % | 0,4265 |
| C3 | 0,146 bits | 1,590 bits | 9,2 % | 71,1 % | 0,3210 |

[MESURE] Le modele conserve moins d'un dixieme de l'entropie disponible par question, et il
est certain a plus de 0,99 sur sept a huit appels sur dix. Table de calibration de C3 :

| decile de confiance | n | confiance moyenne | exactitude reelle | ecart |
|---|---|---|---|---|
| 0,9 a 1,0 | 80 | 0,9920 | 0,6625 | -0,3295 |
| 0,8 a 0,9 | 2 | 0,8383 | 0,5000 | -0,3383 |
| 0,6 a 0,7 | 4 | 0,6718 | 0,7500 | +0,0782 |

Quand ce modele dit 0,99, il a raison deux fois sur trois. [MESURE, sur 80 cellules
seulement] La verification a temperature 0, 1 et 2 exclut que ce soit un artefact du
parametrage.

Deux consequences a garder en tete pour l'interpretation du run complet.

1. **La diversite conservee mesuree par argmax et la diversite conservee mesuree par les
   distributions ne diront pas la meme chose.** Sur ce smoke test, C2 conserve 81,7 pour cent
   de la diversite humaine en argmax, alors que ses distributions individuelles sont
   quasi degenerees. La dispersion vient de la variation entre personnes, pas de
   l'incertitude du modele. C'est exactement la distinction inter et intra de la these du
   projet, et elle apparait ici au niveau de l'appel. [MESURE]
2. **L'exactitude esperee est presque egale a l'exactitude argmax** : 0,5427 contre 0,5444
   pour C2, 0,6445 contre 0,6556 pour C3. [MESURE] Un modele qui hesitait donnerait un ecart
   large. Celui ci n'hesite pas.

Ce comportement est celui d'un modele de 4 milliards de parametres en 4 bits avec une
consigne de format forte. [HYPOTHESE] Il faudra le comparer a un modele plus gros avant d'en
faire un resultat.

### 5.3 Controle de sante du run lui meme, a 23 h 01

Releve sur la trace `data/traces/a5-C2-p1.jsonl` en cours d'ecriture, 1 671 appels :

- masse sur les lettres, minimum 0,9982, mediane 1,0000 ; [MESURE]
- **zero appel rejete, zero modalite absente du top 40** ; [MESURE]
- 11 personnes ont leurs 149 items complets, la douzieme est en cours : l'ordre personne par
  personne fonctionne comme prevu, une troncature coutera des personnes entieres. [MESURE]

---

## 6. Evaluer au matin

Le run doit s'etre termine, ligne `RUN TERMINE` dans `data/traces/a5-run.log`.

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
grep -E "appels en|RUN TERMINE" data/traces/a5-run.log
wc -l data/traces/a5-C2-p1.jsonl data/traces/a5-C3-p1.jsonl
.venv/bin/python analyses/a5_evaluer.py
```

Comptez cinq a dix minutes : le recalcul de B0, B1 et B2 sur le decoupage complet de a2 est
la partie longue. `--sans-baselines` le saute si seul le tableau des agents est voulu.

Sortie : `resultats/a5_resultats.json` plus un tableau sur la sortie standard. L'evaluateur a
ete teste sur les traces partielles du smoke test, il tourne. [MESURE]

Ce qu'il calcule, sur les memes personnes et les memes items que le run, jamais sur les
1 052 :

- exactitude par personne en argmax, intervalle de confiance a 95 pour cent par bootstrap
  **sur les personnes** (2 000 tirages, fonction de `a2_commun`) ;
- exactitude normalisee par le plafond humain test retest **de ces personnes la** ;
- diversite conservee et accord par paires, fonctions de `a2_commun`, donc identiques a a0
  et a a2 ;
- les memes chiffres pour B0 mode, B0 tirage, B1 argmax et B2 argmax, recalcules sur le
  decoupage de a2 puis restreints a ces personnes en test, l'apprentissage se faisant sur les
  autres ;
- les memes chiffres pour les humains de la vague 2 et pour les six conditions de Stanford,
  composite, enquete, v3, v6, v7 et v8 ;
- exactitude esperee, calibration par decile avec ecart de calibration attendu, et entropie
  moyenne par appel avec sa part de l'entropie maximale ;
- **un tableau par famille thematique**, les six familles de `FAMILLES` dans
  `a2_baselines_gss.py`, pour toutes les methodes ci dessus, avec un plafond humain
  recalcule famille par famille. Sortie dans `resultats/a5-familles.csv`.

**Comment lire le tableau par famille sans se tromper.** Il repond a la tache 2 du rapport
a8 : avec des blocs aleatoires, un item secret garde ses cousins thematiques dans le
contexte et B2 en profite, alors que les agents composite de Stanford battent B2 des que la
famille entiere sort du contexte. Le chiffre global masque donc l'endroit ou un modele de
langage sert a quelque chose.

Mais nos C2 et C3, comme les B0, B1 et B2 recalculees ici, sont en decoupage par **blocs
aleatoires**, celui du run : leurs cousins thematiques sont restes dans le contexte. Seule
C3F, si elle a tourne, est en regime famille retiree. La comparaison stricte avec
`a8_familles.py` est donc **C3F contre la ligne "B2 famille retiree" de
`resultats/a8-familles-gss.csv`**, et non C3 contre elle. Ce point est ecrit en commentaire
dans le code, il se perd sinon.

Si la passe 2 de C3 est lancee plus tard, l'evaluateur la detecte seul, moyenne les deux
passes **au niveau des modalites et non des lettres** (c'est pourquoi la trace stocke des
modalites), et rapporte en plus chaque passe seule pour rendre visible l'ampleur du biais de
position.

Pour lancer la passe 2 :

```
.venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --passe 2 --fin HH:MM
```

Elle ne doit jamais tourner en meme temps qu'un autre `llama-server`.

---

## 7. Ce que je n'ai pas pu verifier

1. **Le run n'est pas fini au moment ou ces lignes sont ecrites.** Tous les chiffres de
   resultat de ce rapport viennent du smoke test, 90 cellules par condition. Aucune
   conclusion scientifique ne peut en sortir. Le rapport dit ce qui a ete lance et comment,
   pas ce qui en sort.
2. **Le debit n'a pas ete mesure machine au repos.** La charge est passee de 3 a 30 pendant
   la soiree, du fait d'autres agents travaillant en parallele. Les 4 921 appels par heure
   sont un plancher sous concurrence. Impossible de separer la part du bridage thermique de
   a4 et la part de la concurrence sans une mesure au repos, qui prendrait la machine pour
   dix minutes et retarderait le run.
3. **Le debit de prefill, 380 tokens par seconde, est deux fois plus bas que les 790 de a3.**
   Attribue a la concurrence, mais non demontre. Si la vraie cause etait la longueur du
   contexte C3, 4 617 tokens contre 3 029 dans le banc de a3, la projection serait fausse.
   [HYPOTHESE non tranchee]
4. **Le prompt n'a pas ete compare a celui de Stanford.** Nos conditions C2 et C3 visent le
   meme regime que leurs agents demographiques et leurs agents enquete, mais la formulation
   exacte de leurs prompts n'a pas ete relue dans l'archive. Un ecart de score peut donc
   venir du prompt et non du modele. C'est la limite la plus serieuse pour toute comparaison
   directe avec leurs chiffres.
5. **Un seul modele.** Qwen3-4B en 4 bits. La quasi degenerescence des distributions vue au
   smoke test peut etre une propriete de ce modele, de cette quantification, ou des deux.
   Aucun controle sur Llama-3.1-8B ni sur gpt-oss-20b n'a ete fait.
6. **Le controle (d), PMI conditionnel au domaine**, recommande par a3 comme controle sur un
   sous echantillon, n'a pas ete fait. Rien ne garantit encore que le classement des
   modalites ne depend pas de l'etiquetage par lettres.
7. **Le biais de position n'est pas mesure**, puisque la passe 2 n'est pas dans la file de
   cette nuit. Tant qu'elle n'a pas tourne, l'ampleur du biais est inconnue et les chiffres
   de C3 en passe 1 sont a lire avec cette reserve.
7bis. **Le regime famille retiree n'a pas tourne non plus.** C3F est ecrite, testee a la
   syntaxe et branchee dans l'evaluateur, mais aucun appel n'a ete fait. Le tableau par
   famille du matin comparera donc des blocs aleatoires a des blocs aleatoires, ce qui est
   utile mais ne repond pas encore a la question de a8. Voir la section 4.5.
8. **Deux `llama-server` ont coexiste deux fois.** La premiere a 22 h 45, une minute : un
   serveur du test de reprise ne s'est pas arrete alors que son processus parent avait fini.
   Constate et tue a la main ; cause non identifiee, le mode `nohup` avec redirection vers
   un fichier, qui est celui du run de production, n'a pas montre ce comportement. La
   seconde de 22 h 47 a 22 h 59, douze minutes, du fait du smoke test d'un autre agent
   (`a11_agents_locaux_twin.py`, port 8199). Elle n'a pas ete interrompue, le travail de
   l'autre agent n'etant pas le mien a arreter. Effet mesure, facteur 9,5 sur le debit,
   detail en section 4.4. **Les chiffres de debit des sections 4.1 a 4.3 sont donc tous des
   planchers, et une partie d'entre eux mesure la concurrence plutot que la machine.**
9. **Aucune verification que les 149 items n'ont pas de correlat trivial dans le contexte.**
   Un controle a ete fait sur la fuite exacte entre item cible et attribut demographique :
   aucun couple parmi les 149 x 11 n'atteint 0,5 d'accord de chaine, `polviews` ayant deja
   ete retire par a2. [MESURE] Mais deux items proches l'un de l'autre, l'un secret et
   l'autre en contexte, restent possibles : c'est la limite 7 de a2, non traitee ici.

---

## 8. Questions ouvertes pour Simon

1. **La quasi certitude du modele est elle un resultat ou un artefact de taille ?** Sept a
   huit appels sur dix a p max superieure a 0,99, avec une exactitude reelle de 0,66 dans ce
   decile. Si cela tient sur le run complet, c'est une mesure d'ecrasement de variance au
   niveau de l'appel qu'aucun papier lu ne publie, et elle est gratuite puisqu'elle sort de
   la meme trace. Faut il en faire une mesure du dossier, ou attendre de l'avoir reproduite
   sur un modele plus gros avant d'y consacrer du texte ?
2. **Quelle diversite publier ?** Nous en avons maintenant deux, et elles ne disent pas la
   meme chose : la diversite de la population predite en argmax, qui est celle de a0 et de
   a2 et qui permet la comparaison avec Stanford, et l'entropie des distributions
   individuelles, qui n'existe que chez nous. Les publier cote a cote demande de nommer
   clairement la difference. Faut il les traiter comme deux sous scores de l'indice de
   diversite de METHODOLOGIE E1.6, ou comme deux mesures separees ?
3. **Le prompt doit il etre aligne sur celui de Stanford ?** Deux positions defendables. Le
   reprendre mot pour mot rend la comparaison de scores propre et fait de nous des
   reproducteurs. Ecrire le notre mesure notre pipeline et interdit la comparaison directe.
   La reponse change la lecture de tout le tableau du matin.
4. **Le budget de la passe 2 contre celui de C3F.** Les deux coutent une nuit et il faut
   choisir laquelle passe en premier. La passe 2 corrige un biais de position documente
   dont nous ne connaissons pas l'ampleur sur ce materiel. C3F ouvre le seul regime ou le
   rapport a8 montre les agents de Stanford battant B2. Mon avis, a contredire : mesurer le
   biais de position sur 30 personnes suffit a decider s'il faut la passe 2 complete, ce qui
   libere la nuit suivante pour C3F. Est ce le bon arbitrage ?
5. **Que faire de C4 et de C7 ?** METHODOLOGIE E1.4 les declare obligatoires. C7, le controle
   d'extraction, est le plus important des deux pour la credibilite : sans lui nous ne savons
   pas quelle part de la performance de C3 est de la recuperation d'un item correle deja
   present dans le contexte plutot que de la prediction. Il coute une nuit de plus. Passe t
   il avant la passe 2 de C3 ?

---

## Rejouer

```
# le run, C2 puis C3, passe 1
.venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C2,C3 --passe 1 \
    --personnes 150 --fin 07:30

# la passe 2 de C3, separement, jamais en meme temps
.venv/bin/python analyses/a5_agents_locaux_gss.py --conditions C3 --passe 2 --fin HH:MM

# l'evaluation
.venv/bin/python analyses/a5_evaluer.py
```

Les traces vont dans `data/traces/`, qui n'est pas versionne. Aucune microdonnee ne sort de
`data/`. Aucun appel API distant. Le modele et le serveur tournent en local.
