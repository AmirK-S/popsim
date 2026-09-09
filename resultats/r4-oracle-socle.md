# r4. L'oracle des camps sur le modele socle : ce qui est prepare, et ce qui tournera au matin

Seance de la nuit du 8 au 9 septembre 2026, ouverte a 23:37 et fermee a 00:05. **Aucun
appel de modele n'a ete fait pendant cette seance** : le GPU est occupe par R2 jusqu'a
05:45, par R3 jusqu'a 08:00, puis par la file 4 jusqu'a 08:50 au plus tard, et la consigne
interdit de lancer un serveur. Le run de R4 part tout seul derriere la file 4, par
`analyses/file_nuit_5.sh`, lancee sous `nohup`.

Le seul acces reseau de la seance est le telechargement de deux fichiers de poids depuis
Hugging Face. Rien d'autre n'est sorti de la machine. Aucun fichier existant du depot n'a
ete modifie.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## Reponse en une ligne

**Le socle est telecharge, verifie, et la file part a 08:50 au plus tard ; le run couvre
trois conditions et 2 682 cellules, dont les deux qui separent les poids du format ; et un
resultat est deja tombe sans un appel de plus : sur les traces de R1, Qwen3-4B decrit les
camps sensiblement plus pres des marginales nationales du GSS que de l'echantillon de
1 052 personnes que nous mesurons, de 0,021 de distance de variation totale
[0,004 ; 0,040], p = 0,022.** [MESURE, `r4-h4-restitution.csv`]

---

## 0. Ce qui est fait, et ce qui reste a faire

| | etat |
|---|---|
| page de plan `resultats/r4-preenregistrement.md` | **ecrite a 23:45**, avant tout appel, avant meme le premier essai a moteur factice |
| poids `Qwen3-4B-Base` Q4_K_M | **telecharges, taille et sha256 conformes** [MESURE] |
| poids `Qwen3-4B` Q4_K_M, depot officiel Qwen | **telecharges, taille et sha256 conformes** [MESURE] |
| `analyses/r4_oracle_socle.py` | ecrit, verifie hors ligne, essaye a moteur factice |
| `analyses/file_nuit_5.sh` | ecrit, essaye sur ses deux chemins, **lancee sous nohup, PID 15079** |
| evaluateur | `r1_evaluer.py --suffixe r4`, **essaye sur les traces reelles de R1**, sans une modification de son fichier |
| H4, marginales nationales | **construit et mesure**, sur les traces de R1, 112 items |
| le run lui meme | **pas commence.** Il part quand la file 4 pose son marqueur, ou a 09:00 |
| smoke test contre un serveur vivant | **impossible ce soir**, et c'est le risque principal, section 8 |

---

## 1. La provenance des poids

### 1.1 Une erreur de renvoi a corriger dans deux rapports

`r1-oracle-des-camps.md` question 4 et `r1-resultats.md` tableau 5.3 disent tous les deux
que « `Qwen3-4B-Base` est deja telecharge selon `a3` section 4.4 ». **C'est faux, deux fois.**
[MESURE, verification du 2026-09-08 a 23:38]

- `data/modeles/gguf/` ne contenait ce soir que quatre fichiers, tous instruits :
  `Qwen3-4B-Instruct-2507-Q4_K_M.gguf`, `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`,
  `Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf`, `gpt-oss-20b-MXFP4.gguf`. Aucun socle.
- `a3` section 4.4 ne parle d'aucun telechargement : elle s'intitule « mlx-lm contre
  llama.cpp : le classement s'inverse selon le modele ». La section des telechargements est
  la 1.1.

La reference est vraisemblablement une confusion avec `a27` section 4.4, qui **etudie** la
faisabilite des poids du socle sans les telecharger. [PROBABLE] Les deux rapports de R1
ne sont pas modifies ; l'erreur est signalee ici et dans `data/modeles/PROVENANCE-r4.md`.

### 1.2 Ce qui a ete telecharge, et verifie

Meme methode qu'`a3` section 1.1 : `HF_HOME` detourne vers `data/modeles/hf-cache`,
`--local-dir data/modeles/gguf`, aucun compte, aucun jeton. `data/modeles` est le lien
symbolique vers `~/Library/Caches/popsim-modeles`, hors iCloud et hors Spotlight, pour la
raison d'`a3` section 1.3.

```
export HF_HOME=$PWD/data/modeles/hf-cache
.venv/bin/hf download mradermacher/Qwen3-4B-Base-GGUF \
    Qwen3-4B-Base.Q4_K_M.gguf --local-dir data/modeles/gguf
.venv/bin/hf download Qwen/Qwen3-4B-GGUF \
    Qwen3-4B-Q4_K_M.gguf --local-dir data/modeles/gguf
```

| | `Qwen3-4B-Base.Q4_K_M.gguf` | `Qwen3-4B-Q4_K_M.gguf` |
|---|---|---|
| depot | `mradermacher/Qwen3-4B-Base-GGUF`, tiers | `Qwen/Qwen3-4B-GGUF`, **officiel** |
| `base_model` declare | `Qwen/Qwen3-4B-Base` | `Qwen/Qwen3-4B` |
| licence declaree | Apache 2.0 | Apache 2.0 |
| octets annonces / **sur le disque** | 2 497 280 736 / **2 497 280 736** | 2 497 280 256 / **2 497 280 256** |
| sha256 annonce / **calcule** | `a7eb1d92...9bed6` / **identique** | `7485fe6f...4fdf5` / **identique** |

[MESURE] Les empreintes completes et la revision du depot sont dans
`data/modeles/PROVENANCE-r4.md`.

**Pourquoi un depot tiers pour le socle.** `a27` section 4.4 l'etablit et la recherche de ce
soir le confirme : **aucune quantification GGUF de `Qwen/Qwen3-4B-Base` ne provient de Qwen
ni de unsloth**, et `unsloth/Qwen3-4B-Base-GGUF` ne publie aucun fichier Q4. [CONFIRME par
`a27` ; MESURE sur cinquante depots rendus par l'API ce soir] `mradermacher` a ete retenu
sur trois criteres : il declare son modele source dans `base_model`, il est la conversion
droite du socle la plus telechargee (359 contre 234 pour `DevQuasar`), et il publie un
Q4_K_M, la quantification exacte des trois autres modeles du dossier, ce qui evite
d'ajouter une variable de quantification a la comparaison.

**Ce que l'empreinte n'atteste pas.** Elle atteste que le fichier telecharge est celui que
le depot annonce. Elle n'atteste pas que la conversion soit fidele aux poids de
`Qwen/Qwen3-4B-Base`, ni que la quantification ait ete faite avec la meme matrice
d'importance que celle d'unsloth pour l'instruit. **Une difference de procede de
quantification entre le socle et l'instruit se lirait comme une difference de poids.**
C'est une limite du run, irreductible sans les poids en pleine precision.

### 1.3 Le defaut d'appariement, et sa reparation

`a27` section 4.4 : « le successeur apparie de ce socle est `Qwen/Qwen3-4B`, publie le meme
jour que le socle, le 26 juillet 2025. Le modele 2507 est une mise a jour ulterieure de deux
mois. **La paire (Base, Instruct-2507) n'est donc pas une paire appariee.** » [CONFIRME]

Le contraste principal `q4base` contre `q4nogab` est donc **declare non apparie** partout
ou il est cite. Et `Qwen/Qwen3-4B` a ete telecharge pour reparer le defaut, en troisieme et
derniere condition, coupable par la fin dure de 10:00. **Regle fixee d'avance :** `q4hyb`
n'est rapportee comme condition de mesure que si elle atteint 90 pour cent de ses 894
cellules ; en dessous, seul son taux d'echec de format est publie.

---

## 2. Le plan, et ce que chaque contraste isole

| condition | poids | format | ce que le contraste avec la ligne du dessus isole |
|---|---|---|---|
| `q4`, **deja acquise en R1** | instruit | gabarit ChatML, zero exemple | reference |
| `q4nogab` | instruit, **le meme fichier GGUF que `q4`** | completion a trois exemples | **le format seul**, poids tenus fixes |
| `q4base` | **socle** | completion a trois exemples | **les poids seuls**, format tenu fixe |
| `q4hyb`, conditionnelle | instruit apparie au socle | completion a trois exemples | l'appariement de la paire |

149 items x 3 camps x 2 identites = **894 cellules par condition**, memes items, memes
camps, memes textes d'identite au caractere pres qu'en R1. 1 788 cellules obligatoires,
2 682 si `q4hyb` passe. La quatrieme condition n'est pas rejouee : ce sont les 894 cellules
de `data/traces/r1-q4.jsonl`.

**Pourquoi `q4nogab` n'est pas un luxe.** `a27` mesure chez les auteurs de 2607.25292 que le
seul changement de format d'invite, a poids identiques, vaut 0,081 de distance de variation
totale, « du meme ordre que l'ecart base contre instruct de la famille Llama, 0,15 », soit
**la moitie**. [CONFIRME, `a27`, annexe B du papier] Sans cette condition, tout l'ecart
socle contre instruit serait attribue aux poids, et la moitie serait fausse. C'est
exactement l'experience E2 que `a27` section 4.4 declare « prealable obligatoire de E1, pas
son complement ».

---

## 3. L'invite a trois exemples, reproduite

Protocole de 2607.25292, lu en `a27` : « Base models do not reliably follow zero-shot
instructions, so we use a 3-shot in-context format for V0 on the base model: three (Q, A)
example pairs followed by the test question ». [CONFIRME, annexe B du papier]

L'invite de R4 est : le texte systeme de R1 **au caractere pres**, une ligne de garde, les
trois exemples separes par `----`, puis le bloc utilisateur de R1 **au caractere pres**,
puis une ligne vide. Aucun gabarit de conversation, aucune balise de role.

**Les trois exemples, en entier.**

```
Survey question, Millbrook Town Panel wording:
"How often do you use the public library in your neighborhood: often, sometimes, or never?"

Answer options:
A. Often
B. Sometimes
C. Never

Out of 100 adults in the fictional town of Millbrook, how many would give each answer?

Reply with exactly 3 lines and nothing else: the option letter, a colon, and an integer percentage. The 3 percentages must add up to 100.
A: <percentage>
B: <percentage>
C: <percentage>

A: 17
B: 46
C: 37

----

Survey question, Millbrook Town Panel wording:
"Which of these did you last have for breakfast?"

Answer options:
A. Toast
B. Porridge
C. Eggs
D. Fruit
E. Cereal
F. Nothing at all

Out of 100 adults in the fictional town of Millbrook, how many would give each answer?

Reply with exactly 6 lines and nothing else: the option letter, a colon, and an integer percentage. The 6 percentages must add up to 100.
A: <percentage>
B: <percentage>
C: <percentage>
D: <percentage>
E: <percentage>
F: <percentage>

A: 22
B: 9
C: 14
D: 11
E: 27
F: 17

----

Survey question, Millbrook Town Panel wording:
"Do you own a bicycle?"

Answer options:
A. Yes
B. No

Out of 100 adults in the fictional town of Millbrook, how many would give each answer?

Reply with exactly 2 lines and nothing else: the option letter, a colon, and an integer percentage. The 2 percentages must add up to 100.
A: <percentage>
B: <percentage>

A: 43
B: 57
```

Et la ligne de garde, entre le texte systeme et le premier exemple :

> Here are three worked examples of the required answer format. They are about unrelated
> topics.

**Les quatre proprietes exigees, et leur verification.** [MESURE, `--verifier`]

1. **Aucun item du GSS, aucune enquete reelle.** « Millbrook Town Panel » est invente ;
   bibliotheque de quartier, petit dejeuner, possession d'un velo. Le controle automatique
   verifie qu'aucun des 149 noms d'items n'apparait dans le texte des exemples.
2. **Aucun nombre reel de camp, aucun mot politique.** Le controle refuse les mots
   `liberal`, `conservative`, `moderate`, `american`, `democrat`, `republican` et
   `general social survey` dans les exemples. Aucun n'y figure.
3. **Trois K differents, 3, 6 et 2.** Les items du GSS vont de K = 2 a K = 12, repartis
   ainsi : 52 items a K = 2, 53 a K = 3, 18 a 4, 15 a 5, 4 a 6, 4 a 7, un a 8, un a 9, un
   a 12. [MESURE] **109 items sur 149 partagent leur K avec un exemple**, et sont donc
   exposes au risque de recopie, mesure par le critere de chute 2 bis.
4. **Aucun vecteur uniforme, aucune collision** avec l'exemple chiffre de l'invite de
   relance de R1, qui rend [37, 30, 33] pour K = 3, [23, 13, 16, 16, 16, 16] pour K = 6 et
   [53, 47] pour K = 2. Les trois sommes valent 100.

**L'ecart assume avec 2607.25292.** Leurs exemples sont hors du support au sens fort : une
lettre, un entier, une couleur. Les miens gardent la **forme** de la tache, un bloc de
question suivi d'une distribution sur K lettres, parce que c'est cette forme la, avec son K
variable, qu'il faut enseigner. Ils n'en gardent rien du contenu.

**Le cout en invite.** L'invite complete fait 2 394 caracteres en moyenne, environ 598
tokens, contre 954 caracteres et 238 tokens en R1. Mais **1 790 caracteres sont le prefixe
commun** au groupe (camp, identite) et sont servis par le cache : la part recalculee a
chaque cellule fait 604 caracteres, du meme ordre qu'en R1. [MESURE]

**L'exemple chiffre de la relance est conserve exprès.** `r1-resultats.md` section 4 mesure
que 11 des 13 relances de `q4` le recopient, et la question 6 a Simon recommande de le
retirer. Le retirer ici rendrait R4 incomparable a R1 sur la seule quantite qui compte. Le
defaut est donc reconduit a l'identique et le critere de chute 2 s'applique des deux cotes.

---

## 4. Les hypotheses, et le referent

Referent des trois premieres : la condition `q4` de R1, dont les valeurs sont publiees et
figees, ratio de dispersion 1,174 / 1,114 / 1,059 sur gauche / centre / droite en identite
journaliste, facteur signe H2b 0,245 [0,056 ; 0,437], plancher humain 1,009.

| | enonce | direction predite | l'issue contraire, nommee d'avance |
|---|---|---|---|
| **H1** | le socle decrit la dispersion interne des camps plus pres du reel que l'instruct | `abs(R_q4base - 1) < abs(R_q4 - 1)` sur au moins 2 camps sur 3 | le socle est **plus loin** de 1, encore plus sur dispersant. C'est ce que la table 4a de 2607.25292 laisse attendre : la masse sur la cible passe de 0,236 au socle a 0,442 apres RLVR, donc le post entrainement concentre et le socle disperse |
| **H2** | l'ecart entre camps decrit par le socle est plus proche du reel | `abs(F_q4base - 1) < abs(F_q4 - 1)` sur H2b | le socle ecrase davantage que le facteur 0,245 de `q4`, ou depasse le reel |
| **H3** | le format seul explique une part mesurable de l'ecart | la part `(X_q4nogab - X_q4) / (X_q4base - X_q4)` dans **[0,20 ; 0,80]** | part non distinguable de zero, le format ne porte rien ; ou part au dessus de 1, les poids agissent en sens inverse |
| **H4** | le modele est plus proche des marginales nationales publiees que de notre echantillon | difference moyenne par item positive | difference nulle ou negative |

**H3, precaution de calcul.** Une part est un rapport de differences, instable quand son
denominateur approche zero. **La part n'est calculee que si l'intervalle de confiance de
`X_q4base - X_q4` exclut zero** ; sinon les trois niveaux sont publies avec leurs
intervalles et la phrase est « le format et les poids ne se separent pas sur cette
quantite ».

Familles de Holm, jamais fusionnees : F1 (H1, 6 tests), F2 (H2, 4), F3 (H3, 2), F4
(contraste de poids, 2), F5 (H4, 3). Bootstrap sur les items, 2 000 tirages ; permutation
de signe appariee par item, 20 000 tirages, estimateur de Phipson et Smyth. Bande de
nullite pratique [0,95 ; 1,05]. Criteres de chute : les sept de la page de plan, section 8.

---

## 5. H4, le test des marginales publiees : construit, et il donne deja un chiffre

**Il est constructible a cout nul, et il l'a ete.** La consigne demandait de dire si le
test etait faisable ; il est fait.

### 5.1 Le referent national

`data/gss-panel/gss2020panel_r1a.dta`, vagues **2016** et **2018** du panel GSS 2016-2020,
colonnes `_1a` et `_1b`, qui sont deux echantillons nationaux de probabilite du GSS. C'est
la source dont le GSS Data Explorer publie les tableaux croises. Ponderation `wtssall`,
ideologie repliee en trois blocs par la regle `GSS_BLOC3` de `a30` apres normalisation du
libelle « moderate, middle of the road » en « moderate », seule normalisation faite.

Les noms d'items de l'archive de Stanford **sont** des noms de variables du GSS, et la
correspondance des modalites se fait par les etiquettes de valeur de Stata contre
`question_master/gss/main.csv`, avec la fonction `canoniser` de `a5`.

**Perimetre : 112 items retenus sur 145 presents dans le panel.** [MESURE,
`r4-h4-perimetre.csv`] La regle, ecrite avant de regarder un resultat : au moins 99 pour
cent des reponses etiquetees s'apparient a une modalite de la nomenclature, et au moins 100
personnes ponderees par camp. Les items ecartes le sont pour des raisons visibles :
`income`, `satfin`, `hunt1` et `union1` ont dans le panel des etiquettes qui ne
correspondent a aucune modalite de Stanford, `colhomo`, `aged` et `spkath/y` s'apparient a
12, 15 et 19 pour cent seulement.

### 5.2 Le resultat, sur les traces de R1, sans un appel de plus

| condition | identite | n items | `TV(decrit, echantillon) - TV(decrit, national)` | IC 95 % | p | p Holm |
|---|---|---|---|---|---|---|
| `q4` | journaliste | 112 | **+0,0215** | [0,0037 ; 0,0395] | 0,0217 | 0,0217 |
| `q4` | adversaire | 112 | **+0,0240** | [0,0046 ; 0,0425] | 0,0120 | 0,0120 |

[MESURE, `resultats/r4-h4-restitution.csv`]

**Le controle de puissance passe.** La mediane par item de `TV(echantillon, national)` vaut
**0,107**, soit **46 pour cent** de l'erreur du modele a l'echantillon, 0,233. Le seuil
preenregistre etait 25 pour cent : les deux referents sont assez differents l'un de l'autre
pour qu'un modele puisse les distinguer. [MESURE]

**Ce que ce chiffre dit, et surtout ce qu'il ne dit pas.**

- Il dit que **Qwen3-4B-Instruct-2507 decrit les camps politiques americains sensiblement
  plus pres du GSS national que de l'echantillon de 1 052 personnes de Stanford**, sur 112
  items, dans les deux identites de demandeur. [MESURE]
- L'ampleur est petite : 0,021 sur une erreur de 0,233, soit **9 pour cent de l'erreur**.
  Le modele n'est proche d'aucun des deux referents.
- **Une explication concurrente est au moins aussi bonne que la restitution** : l'echantillon
  de Stanford n'est pas un echantillon national, et tout modele approximativement calibre
  sur la population americaine sera mecaniquement plus proche du national. Ce test ne les
  separe pas, et aucune phrase de la forme « le modele recite le GSS Data Explorer » n'est
  autorisee par ce chiffre.
- **Il n'est pas comparable a Pew.** Aucune donnee Pew n'est sur la machine et aucune n'a
  ete telechargee.
- **Pour `q4` cette ligne est une analyse a posteriori**, faite sur des traces qui
  existaient deja quand H4 a ete ecrite. Elle n'est prospective que pour `q4base`,
  `q4nogab` et `q4hyb`, dont aucune cellule n'existe encore.

Ce qui rend le test interessant au matin, c'est le contraste : **si le socle est nettement
moins tire vers le national que l'instruit, la restitution est une affaire de post
entrainement ; s'il l'est autant, elle est dans les poids.** Aucune des deux issues n'est
predite ici.

---

## 6. La verification hors ligne, dans le detail

Aucun serveur ne pouvant etre lance, tout ce qui pouvait etre verifie sans modele l'a ete.

| | ce qui a ete verifie | resultat |
|---|---|---|
| 1 | `--verifier` : exemples, referent, poids, plan, parse, critere 2 bis, invite imprimee en entier, registre | **aucun defaut**, code de sortie 0 [MESURE] |
| 2 | empreinte du referent humain de R1 | `ea7cd93e...91c811`, identique ; le critere de chute 6 refuse de tourner si elle bouge [MESURE] |
| 3 | cinq essais de parse sur des sorties fabriquees | format demande, gras, lettre manquante, somme hors bande, bavardage : les cinq verdicts sont ceux attendus [MESURE] |
| 4 | trois essais du critere 2 bis | la recopie d'un exemple est detectee sur K = 3, 6 et 2 ; une distribution uniforme ne l'est pas [MESURE] |
| 5 | **essai a moteur factice** de la boucle complete, 12 items, deux modeles | 72 cellules par modele, sonde a 0 rejet, relances declenchees et rattrapees, une recopie d'exemple comptee, marqueur `RUN TERMINE` pose [MESURE] |
| 6 | **reprise** apres l'essai | 72 cellules deja faites reconnues, **aucune refaite** [MESURE] |
| 7 | **critere 1 bis**, avec un moteur qui echoue toujours au format | le modele est arrete a 60 cellules, taux 1,000, et le suivant part quand meme [MESURE] |
| 8 | **echec de demarrage du serveur** | l'exception est attrapee, une ligne `echec` entre au resume, et le modele suivant part [MESURE] |
| 9 | `--evaluer` sur les traces reelles de R1 | `r1_evaluer.py --suffixe r4` tourne **sans une modification de son fichier** et ecrit les dix sorties [MESURE] |
| 10 | `--h4` sur ces memes traces | referent national construit, 112 items, controle de puissance rendu [MESURE] |
| 11 | `file_nuit_5.sh` en mode essai, deux chemins | marqueur present ; heure limite atteinte sans marqueur. Les deux menent au lancement [MESURE] |

### 6.1 L'evaluateur retombe sur R1, aux bornes de bootstrap pres

Le point de comparaison le plus utile de la soiree : la condition `q4` de R1, relue par le
chemin de R4, rend **exactement les memes estimateurs ponctuels**.

| quantite | R1 publie | par le chemin R4 |
|---|---|---|
| ratio de dispersion, gauche, journaliste | 1,174107 | **1,174107** |
| facteur H2b, 79 items orientes, journaliste | 0,244619 | **0,244619** |
| plancher humain, facteur vague 2 sur vague 1 | 1,008930 | **1,008930** |

[MESURE] En revanche les **bornes de bootstrap different au troisieme decimal** :
[1,109 ; 1,243] en R1 contre [1,112 ; 1,247] ici, et le p de Holm passe de 0,0003 a 0,0001.
La raison n'est pas un defaut : le generateur aleatoire est consomme dans un ordre
different quand le tableau contient une condition au lieu de trois, et la taille de la
famille de Holm change avec le nombre de conditions. **Au matin, la ligne `q4` du tableau
de R4 ne sera donc pas, au troisieme decimal, celle du tableau de R1, et il ne faudra pas
y voir une incoherence.** L'estimateur ponctuel, lui, est identique au sixieme decimal.

### 6.2 La copie de trace, declaree

`data/traces/r1-q4-r4.jsonl` est une **copie octet pour octet** de `data/traces/r1-q4.jsonl`,
sha256 `8ada444f4573cf079ab6cb9a73f2e49d1bde2156ebf08dd191ab8af33d64482b`. Elle existe pour
que l'evaluateur voie les quatre conditions dans le meme tableau et applique Holm sur une
famille commune. Aucun appel n'est refait, aucune ligne n'est modifiee, le fichier d'origine
n'est pas touche. La condition copiee garde sa version d'invite `r1-d1`, les conditions
nouvelles portent `r4-c3` : la difference reste lisible ligne par ligne dans la trace.

### 6.3 Les cles de modele, ajoutees sans modifier R1

`q4base`, `q4nogab` et `q4hyb` sont ajoutees au registre de `r1_oracle_camps.MODELES`
**en memoire**, a l'import de `r4_oracle_socle`, jamais dans le fichier de R1. De meme, le
gabarit `completion-3ex` est injecte dans `R1.gabarit` et dans `R1.ARRETS`. Sans cet ajout,
la figure de `r1_evaluer.py` ignore les cles inconnues et ne trace rien ; les tableaux, eux,
les traitent normalement. **Aucun fichier existant n'est modifie.**

---

## 7. La file 5, et la projection

`analyses/file_nuit_5.sh`, lancee sous `nohup` a **23:58:01**, **PID 15079**, dans
`data/traces/file-nuit-5.pid`, journal `data/traces/file-nuit-5.log`.

1. attendre la ligne `FILE 4 TERMINEE` dans `data/traces/file-nuit-4.log`, **ou**
   **2026-09-09 09:00:00**, epoch **1788937200** ;
2. attendre qu'aucun `llama-server` ne tourne, dix minutes au plus, puis SIGTERM ; **si un
   serveur survit au SIGTERM, R4 n'est pas lance** et la file s'arrete, parce que deux
   serveurs a la fois sont le critere de chute 7 ;
3. `r4_oracle_socle.py --modele q4base,q4nogab,q4hyb --fin 10:00`, fin dure
   **2026-09-09 10:00:00**, epoch **1788940800**, journal `data/traces/r4-run.log`, qui contient deja une ligne, celle de la copie de
   trace de 23:52, et aucun marqueur `RUN TERMINE` : le test de la file n'est pas trompe ;
4. puis, sans serveur, `--evaluer` et `--h4`, pour que les tableaux existent au reveil
   meme si le run a ete tronque.

**Toutes les gardes horaires sont des epochs calcules avec le jour**, et l'horloge machine
au lancement etait le 2026-09-08 a 23:58 CEST. **`pgrep -x` et non `pgrep -f`** : un
processus de surveillance dont la ligne de commande contient la chaine `llama-server`
bloquerait une attente en `-f`, piege rencontre et documente en R1 section 8.

### Projection

| | valeur |
|---|---|
| debit de reference | `q4` en R1 : 894 cellules en 18,2 min, **2 950 par heure** [MESURE] |
| part recalculee de l'invite | 604 caracteres en R4 contre environ 600 en R1 : le prefixe des trois exemples, 1 790 caracteres, est servi par le cache |
| duree attendue par condition | **18 a 22 min**, plus une a deux secondes de chargement de serveur pour un 4 milliards |
| duree attendue des trois | **55 a 70 min** [PROBABLE] |
| creneau si la file 4 finit vers 08:20 | 100 min : **les trois conditions passent** |
| creneau si la file 4 va jusqu'a 08:50 | 70 min : **les deux obligatoires passent, `q4hyb` est a risque** |

La regle de lecture de `q4hyb` est fixee d'avance, section 1.3 : en dessous de 90 pour cent
de ses cellules, seul son taux d'echec de format est publie.

### Commande du matin

La file fait l'evaluation toute seule. Si elle a echoue, ou pour la refaire :

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim

# l'etat de la file
cat data/traces/file-nuit-5.log
tail -30 data/traces/r4-run.log

# l'evaluation, r1_evaluer.py sans une modification
.venv/bin/python analyses/r4_oracle_socle.py --evaluer > data/traces/r4-evaluation.log 2>&1

# H4, les marginales nationales
.venv/bin/python analyses/r4_oracle_socle.py --h4 >> data/traces/r4-evaluation.log 2>&1

# reprendre un run tronque, si le GPU est libre et qu'il reste du temps
.venv/bin/python analyses/r4_oracle_socle.py --modele q4hyb --fin 12:00
```

**Ne pas passer la sortie de l'evaluateur dans `head`** : `head -3` ferme le tuyau, le
processus meurt sur SIGPIPE avant d'ecrire le resume, et laisse des CSV a jour avec un
resume perime. Piege mesure en R1, section 8. Rediriger vers un fichier, ou ne rien filtrer.

Sorties attendues : `resultats/r1-par-cellule-r4.csv`, `r1-par-item-ecarts-r4.csv`,
`r1-identite-r4.csv`, `r1-h1-unanimite-r4.csv`, `r1-h2-ecart-r4.csv`,
`r1-h3-identite-r4.csv`, `r1-h4-derive-r4.csv`, `r1-controles-r4.csv`,
`r1-figure-oracle-r4.png` et `.svg`, `r1-resume-r4.md`, plus `r4-h4-restitution.csv`,
`r4-h4-par-cellule.csv` et `r4-h4-perimetre.csv`.

**Attention, ces fichiers existent deja** : ils portent la seule condition `q4` de l'essai
hors ligne de 23:55. Ils seront ecrases au matin par le run complet. Une facon simple de
verifier qu'ils sont a jour est de compter les cles de modele dans
`r1-par-cellule-r4.csv` : une seule ce soir, quatre attendues au matin.

---

## 8. Ce que je n'ai pas pu verifier

1. **Le run lui meme.** Il n'a pas commence. Aucun chiffre de ce rapport ne porte sur une
   sortie de modele socle, et il n'y en a aucun a citer.
2. **Aucun appel n'a jamais ete envoye a un modele socle sous cette invite, et c'est le
   risque principal de la nuit.** R1 avait un smoke test en cinq etapes qui a trouve deux
   bugs ; R4 n'en a aucun, parce que la machine est occupee jusqu'au matin et que la
   consigne interdit de lancer un serveur. Trois choses peuvent mal tourner et ne seront
   vues qu'a 08:50 : le socle peut ne pas suivre le format malgre les trois exemples ; les
   sequences d'arret peuvent ne pas se declencher et faire generer un quatrieme exemple a
   chaque appel, ce qui multiplierait la duree par cinq ; `llama-server` peut refuser de
   charger un GGUF depourvu de gabarit de conversation. **Le premier risque est couvert par
   le critere 1 bis**, qui arrete un modele a 60 cellules si plus de la moitie echoue.
   **Le troisieme est couvert** par l'attrape d'exception qui laisse partir les modeles
   suivants. **Le deuxieme ne l'est pas** : il se verra a la duree, pas au taux de rejet,
   et il mangera le creneau. La seule parade est de regarder `data/traces/r4-run.log` a
   09:00 si quelqu'un est reveille.
3. **Que la conversion GGUF du socle soit fidele.** Empreinte verifiee, procede de
   quantification inconnu, depot tiers. Section 1.2.
4. **Que `mradermacher/Qwen3-4B-Base-GGUF` soit bien une conversion de
   `Qwen/Qwen3-4B-Base` et de rien d'autre.** Le champ `base_model` de sa carte le declare ;
   personne ne l'a verifie sur les poids.
5. **La date de coupure des trois modeles.** Aucune n'est publiee, pour aucun des trois.
   **Cela veut dire que R4 ne tranche rien par la date, et donc que l'objection de
   contamination reste entiere**, exactement comme en R1. R4 separe le post entrainement
   des poids ; il ne separe pas « le modele a lu le sondage » du reste.
6. **H4 sur Pew.** Aucune donnee Pew sur la machine, aucun telechargement fait. Le seul
   referent externe est le GSS national du panel 2016-2020.
7. **Le sens du signe de H4.** Le chiffre de la section 5.2 est compatible avec la
   restitution et avec le simple fait que l'echantillon de Stanford n'est pas national.
   Rien dans ce dispositif ne les separe.
8. **L'ordre des modalites.** Une seule passe, ordre de nomenclature, comme en R1. `a27`
   mesure que l'ordre seul porte 60 pour cent de l'effet de leur correctif.
9. **La litterature.** Aucune recherche web n'a ete faite cette nuit en dehors de l'API
   Hugging Face pour la provenance des poids. Les references a `a26`, `a27`, `a30`, `a37`
   et `a38` sont citees telles que ces rapports les citent.
10. **Le second terme humain.** Toujours absent. Aucune phrase de la forme « le modele
    exagere plus que les humains » n'est autorisee, en R4 comme en R1.

---

## 9. Questions ouvertes pour Simon

1. **Si le socle fait comme l'instruit, que devient le programme A ?** C'est l'issue la
   plus derangeante et elle est parfaitement possible. Elle dirait que le portrait des
   camps est dans les poids de pre entrainement, que le post entrainement n'y ajoute rien,
   et qu'une obligation d'audit qui viserait l'alignement viserait a cote. Faut il la
   publier telle quelle, ou attendre un second socle d'une autre famille avant de l'ecrire ?

2. **Le contraste non apparie est il publiable tel quel ?** `a27` etablit que
   (Base, Instruct-2507) n'est pas une paire appariee. `q4hyb` repare le defaut, mais elle
   passe en dernier et la fin dure de 10:00 peut la couper. Si elle est coupee, faut il
   publier `q4base` contre `q4nogab` en le declarant non apparie, ou attendre une nuit de
   plus pour la paire propre ?

3. **Le facteur d'amplification doit il etre lu sur une condition de completion ?** Toute
   la lecture publiee de R1 porte sur des modeles sous gabarit de conversation, qui est le
   regime dans lequel un citoyen interroge un assistant. La condition `q4nogab` mesure une
   chose que personne n'utilise en produit. C'est un controle methodologique, pas une
   quantite auditable. Faut il le dire dans le rapport de resultats, au risque d'affaiblir
   la piece la plus solide du run ?

4. **H4 merite t elle un dispositif propre ?** Le signe est la, l'ampleur est petite, et
   l'explication concurrente est bonne. Le test qui trancherait est un item dont la
   distribution nationale est publiee et dont l'echantillon de Stanford s'ecarte
   beaucoup, oppose a un item ou les deux coincident. Ce contraste est constructible sur
   les 112 items retenus, sans un appel de plus. Est ce prioritaire, ou est ce une
   distraction par rapport a l'experience de lecture du mois 6 ?

5. **L'erreur de renvoi de `a3` section 4.4 doit elle etre corrigee dans les deux rapports
   de R1 ?** Deux rapports affirment qu'un modele est telecharge alors qu'il ne l'est pas,
   et un lecteur qui rejouerait la recommandation echouerait. Je n'ai modifie aucun fichier
   existant ; la correction demande une decision.

6. **Faut il un troisieme exemple hors support au sens fort ?** Les miens gardent la forme
   de la tache, ceux de 2607.25292 non. Si le critere 2 bis mesure au matin un taux de
   recopie non nul, la conclusion sera qu'un exemple de meme forme contamine, et il faudra
   refaire le run avec des exemples de forme differente, en payant le fait que le socle
   suivra peut etre moins bien le format. Ou preferer d'emblee un gabarit sans nombre, du
   genre `A: <integer>`, au risque que le socle n'apprenne rien ?

---

## Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim

# la verification hors ligne, aucun serveur, aucun appel
.venv/bin/python analyses/r4_oracle_socle.py --verifier

# le run complet, trois conditions l'une apres l'autre, un serveur a la fois
.venv/bin/python analyses/r4_oracle_socle.py --modele q4base,q4nogab,q4hyb --fin 10:00

# une seule condition
.venv/bin/python analyses/r4_oracle_socle.py --modele q4base --fin 12:00

# un smoke test, quand le GPU sera libre : huit items, une condition
.venv/bin/python analyses/r4_oracle_socle.py --modele q4base --items 8 --fin 23:59

# l'evaluation et H4
.venv/bin/python analyses/r4_oracle_socle.py --evaluer
.venv/bin/python analyses/r4_oracle_socle.py --h4

# la file de nuit
nohup zsh analyses/file_nuit_5.sh > data/traces/file-nuit-5.nohup.log 2>&1 &
echo $! > data/traces/file-nuit-5.pid

# la file en mode essai, sans rien executer
R4_ESSAI=1 R4_PAS=2 zsh analyses/file_nuit_5.sh
```
