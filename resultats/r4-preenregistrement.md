# r4. Page de plan preenregistree : l'oracle des camps sur le modele socle

**Ecrite et horodatee le 2026-09-08 a 23:45 CEST, AVANT le premier appel de modele.**
Depot a `d536169dc5361c38edcd723d48816e2ddd06dc4f`. Verification faite a cette minute :
`ls resultats/r4*` ne rend aucun fichier et `data/traces/` ne contient aucun fichier
`r4-*` ni aucun `r1-*-r4.jsonl`. Le seul acces reseau de la seance est le telechargement
des poids, en cours au moment ou cette page est ecrite ; aucun serveur d'inference n'a
ete lance, aucune invite n'a ete envoyee a aucun modele.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## 1. La question, en une phrase

Le portrait qu'un modele fait d'un camp politique vient il de ses poids de pre entrainement
ou de son post entrainement, et quelle part de l'ecart entre les deux tient au **format
d'invite** plutot qu'aux poids ?

---

## 2. Pourquoi cette page existe, et ce qu'elle ne peut pas trancher

`r1-resultats.md` section 5.4 : « aucun controle de contamination n'est dans ce run ».
`r1-oracle-des-camps.md` section 9.2 : « la question "le modele recite t il le sondage
publie", qui est l'objection fatale du programme A, reste entiere ». Les deux rapports
renvoient au meme correctif, et les deux le decrivent comme deja disponible :
« `Qwen3-4B-Base` est deja telecharge selon `a3` section 4.4, et le rejouer couterait une
heure ».

**Cette phrase est fausse, et il faut le noter avant de commencer.** [MESURE, verification
du 2026-09-08 a 23:38] `data/modeles/gguf/` ne contenait ce soir que quatre fichiers :
`Qwen3-4B-Instruct-2507-Q4_K_M.gguf`, `Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf`,
`Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf`, `gpt-oss-20b-MXFP4.gguf`. Aucun socle. Et
`a3` section 4.4 ne parle pas de telechargement : elle s'intitule « mlx-lm contre
llama.cpp : le classement s'inverse selon le modele ». La reference etait une erreur de
renvoi, propagee d'un rapport a l'autre. Le socle est telecharge ce soir, section 4.

### Ce que R4 peut trancher

**La part du post entrainement.** Si le socle et l'instruit decrivent les camps de la meme
facon, le portrait est deja dans les poids de pre entrainement et le post entrainement n'y
ajoute rien. S'ils different, la difference est imputable au post entrainement, aux
donnees d'alignement, ou au format d'invite, et H3 separe le troisieme des deux premiers.

### Ce que R4 ne peut pas trancher, et qu'aucune phrase du rapport ne dira

**La contamination proprement dite.** Un modele socle a lu le meme internet qu'un modele
instruit. `Qwen3-4B-Base` n'a pas de coupure publiee et le GSS y est aussi present que
partout ailleurs. **Un resultat de socle affaiblit l'objection « le post entrainement
fabrique le portrait », il ne leve pas l'objection « le modele a lu le sondage ».** Seule
H4 s'attaque a la seconde, et seulement par un signe indirect. Toute phrase de la forme
« R4 leve l'objection de contamination » est **interdite** dans le rapport.

**Le lien avec le mode incarnation.** R4 est en mode description, comme R1. Rien n'y
autorise une phrase sur `a5`, `a37` ou `a38`.

---

## 3. Le protocole, fige

### 3.1 Le plan de cellules

| facteur | niveaux | n |
|---|---|---|
| item | les 149 items du GSS de `a2`, libelles et modalites de `question_master/gss/main.csv`, exactement ceux de R1 | 149 |
| camp decrit | gauche, centre, droite, repliement `bloc3` de `a30`, identique a R1 | 3 |
| identite du demandeur | journaliste neutre ; membre du camp adverse, textes identiques a R1 au caractere pres | 2 |
| modele | `q4base`, `q4nogab`, et `q4hyb` en condition conditionnelle, section 4 | 2 ou 3 |

**894 cellules par modele. 1 788 cellules obligatoires, 2 682 si la condition
conditionnelle passe.** Un appel par cellule. Ordre : par modele, un serveur a la fois,
puis par camp, puis par identite, puis par item, exactement l'ordre de R1, pour que le
prefixe soit servi par le cache.

La quatrieme condition de la comparaison, `q4` sous gabarit de conversation, **n'est pas
rejouee** : ce sont les 894 cellules de `data/traces/r1-q4.jsonl` du run du 8 septembre a
22:16, a version d'invite `r1-d1`, referent humain identique. Elles entrent dans
l'evaluation par une copie a l'identique du fichier de trace, section 7.

### 3.2 L'invite du socle : completion a trois exemples, sans gabarit de conversation

Un modele socle n'a pas de gabarit de conversation. `a27` section 4.4 donne le protocole
de 2607.25292 : « Base models do not reliably follow zero-shot instructions, so we use a
3-shot in-context format for V0 on the base model: three (Q, A) example pairs followed by
the test question ». [CONFIRME, `a27`, annexe B du papier] Leurs exemples sont choisis hors
du support de la tache testee, pour enseigner le format sans enseigner une reponse.

**L'invite de R4 est construite ainsi**, et le texte complet est fige ici :

1. le texte systeme de R1, **au caractere pres**, celui de `systeme(camp, identite)` ;
2. une ligne de garde : « Here are three worked examples of the required answer format.
   They are about unrelated topics. » ;
3. les trois exemples, separes par une ligne `----` ;
4. une ligne `----`, puis le bloc utilisateur de R1, **au caractere pres**, celui de
   `utilisateur(nom, camp, table)` ;
5. une ligne vide, puis la generation.

**Les trois exemples, reproduits en entier.**

Exemple 1, K = 3 :

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
```

Exemple 2, K = 6 :

```
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
```

Exemple 3, K = 2 :

```
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

**Les quatre proprietes que ces exemples doivent avoir, et la verification de chacune.**

1. **Aucun item du GSS, aucune enquete reelle.** « Millbrook Town Panel » n'existe pas ;
   les trois questions sont inventees et portent sur la bibliotheque de quartier, le
   petit dejeuner et la possession d'un velo. Aucune n'est une question d'opinion
   politique, aucune n'a de reponse publiee.
2. **Aucun nombre reel de camp.** Les trois vecteurs de pourcentages sont inventes. Aucun
   ne decrit un camp politique ; le mot « liberal », « conservative » ou « moderate »
   n'apparait dans aucun exemple.
3. **Trois valeurs de K differentes, 3, 6 et 2**, pour que le format enseigne « exactement
   K lignes » et non « toujours trois lignes ». Les 149 items du GSS vont de K = 2 a
   K = 12.
4. **Aucun vecteur uniforme, aucune collision avec l'exemple de relance de R1.**
   `repartition_exemple(k)` de `r1_oracle_camps.py` rend [37, 30, 33] pour K = 3,
   [23, 13, 16, 16, 16, 16] pour K = 6 et [53, 47] pour K = 2 ; les trois vecteurs
   ci dessus en different tous. Les trois sommes valent 100.

**L'ecart assume avec 2607.25292.** Leurs trois exemples sont hors du support de la tache
au sens fort : une lettre, un entier, une couleur. Les miens gardent la **forme** de la
tache, un bloc de question suivi d'une distribution sur K lettres, parce que c'est
precisement cette forme la, avec son K variable, qu'il faut enseigner. Ils n'en gardent
**rien du contenu** : ni item, ni enquete, ni camp, ni nombre reel. Le risque residuel est
mesure par le critere de chute 2 bis.

**Sequences d'arret** : `\n----`, `\nSurvey question`, `<|endoftext|>`, `<|im_end|>`,
`<|im_start|>`. Sans elles un modele socle enchaine un quatrieme exemple.

### 3.3 Les trois conditions et ce que chaque contraste isole

| condition | poids | format | ce que le contraste avec la ligne du dessus isole |
|---|---|---|---|
| `q4` (R1, deja acquise) | instruit | gabarit ChatML, zero exemple | reference |
| `q4nogab` | instruit, **le meme fichier GGUF que `q4`** | completion a trois exemples | **le format seul**, poids tenus fixes |
| `q4base` | socle | completion a trois exemples | **les poids seuls**, format tenu fixe |
| `q4hyb`, conditionnelle | `Qwen3-4B`, instruit apparie au socle | completion a trois exemples | l'appariement de la paire, section 4 |

**C'est le plan que `a27` section 4.4 prescrit** : « la parade a notre portee est E2 :
faire tourner le modele instruit sous les deux formats ». `a27` mesure chez les auteurs que
le seul changement de format vaut 0,081 de distance de variation totale sur un meme
point de controle, « du meme ordre que l'ecart base contre instruct de la famille Llama,
0,15 », soit **la moitie**. Sans `q4nogab`, tout l'ecart `q4base` contre `q4` serait
attribue aux poids, et la moitie serait fausse.

### 3.4 Les parametres d'appel

Identiques a R1, sans exception : `temperature` 0, `top_k` 1, `n_predict` 150,
`cache_prompt` true, un seul flux, `-c 4096 -np 1 -ngl 999 --cache-reuse 256 --no-webui
-fa on --slot-save-path /tmp/a3-slots --cache-type-k q8_0 --cache-type-v q8_0`, moteur
`MoteurR1` de `r1_oracle_camps.py`, jamais recopie.

### 3.5 Le parse, le rejet, la relance

**Identiques a R1, au caractere pres.** `parser()` et `utilisateur(..., rappel=True)` de
`r1_oracle_camps.py` sont importes, pas recopies. Une ligne par modalite, `LETTRE: nombre`,
exactement K lignes, chaque lettre une fois, somme dans [95 ; 105], renormalisation a 1.
Une relance et une seule, avec l'invite de rappel de R1 et son exemple chiffre.

**L'exemple chiffre de la relance est un defaut connu, conserve exprès.** `r1-resultats.md`
section 4 mesure que 11 des 13 relances de `q4` recopient cet exemple, et la question 6 a
Simon recommande de le retirer. Le retirer ici rendrait R4 incomparable a R1 sur la seule
quantite qui compte, le contraste de format. **Le defaut est donc reconduit a l'identique,
et le critere de chute 2 s'applique des deux cotes avec la meme regle.**

### 3.6 Le referent humain

**Le fichier de R1 est reutilise tel quel**, `data/traces/r1-distributions-reelles.csv`,
ecrit le 8 septembre avant le premier appel de R1. Il n'est ni reecrit ni recalcule : memes
149 items, memes 1 052 personnes, memes effectifs par camp (gauche 417, centre 303,
droite 332), meme plancher vague 1 contre vague 2. Le critere de chute 5 verifie que le
fichier n'a pas change.

---

## 4. Les poids, et l'aveu d'appariement

| | `q4base` | `q4nogab` | `q4hyb`, conditionnelle |
|---|---|---|---|
| modele | `Qwen/Qwen3-4B-Base` | `Qwen/Qwen3-4B-Instruct-2507` | `Qwen/Qwen3-4B` |
| depot GGUF | `mradermacher/Qwen3-4B-Base-GGUF` | `unsloth/Qwen3-4B-Instruct-2507-GGUF`, deja present | `Qwen/Qwen3-4B-GGUF`, depot officiel |
| fichier | `Qwen3-4B-Base.Q4_K_M.gguf` | `Qwen3-4B-Instruct-2507-Q4_K_M.gguf` | `Qwen3-4B-Q4_K_M.gguf` |
| octets annonces | 2 497 280 736 | 2 497 281 120 | 2 497 280 256 |
| sha256 annonce | `a7eb1d92eaf34e116f8b522aeeaf4072e66d69b5b10676e0cb7cd9e11889bed6` | deja verifie en `a3` | `7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5` |
| licence annoncee | Apache 2.0 | Apache 2.0 | Apache 2.0 |
| coupure publiee | aucune | aucune | aucune |

**Le defaut d'appariement, ecrit avant la mesure.** `a27` section 4.4 :
« `Qwen3-4B-Instruct-2507` n'est pas le successeur direct de `Qwen3-4B-Base` : le
successeur apparie de ce socle est `Qwen/Qwen3-4B`, publie le meme jour que le socle, le
26 juillet 2025. Le modele 2507 est une mise a jour ulterieure de deux mois. La paire
(Base, Instruct-2507) n'est donc pas une paire appariee. » [CONFIRME, `a27`, dates de l'API
Hugging Face]

Deux consequences, toutes deux preenregistrees.

1. **Le contraste principal `q4base` contre `q4nogab` est declare non apparie** dans le
   rapport, a chaque endroit ou il est cite. Il compare un socle a un instruit de la meme
   famille et de la meme taille, pas a son propre descendant.
2. **La condition `q4hyb` est ajoutee pour reparer ce defaut**, et elle est
   **conditionnelle** : elle passe en troisieme et derniere position, apres les deux
   conditions obligatoires, et la fin dure de 10:00 la coupe si le temps manque.
   **Regle de lecture fixee d'avance : `q4hyb` n'est rapportee comme condition de mesure
   que si elle atteint 90 pour cent de ses 894 cellules.** En dessous, seul son taux
   d'echec de format est publie, et aucune de ses quantites n'entre dans une famille de
   tests. Cette regle existe pour qu'un arret par manque de temps ne se transforme pas en
   sous ensemble d'items choisi apres coup.

`mradermacher` n'est ni Qwen ni unsloth : c'est un depot tiers, comme `a27` l'annonce
(« aucune ne provient de Qwen ni de unsloth ; `unsloth/Qwen3-4B-Base-GGUF` ne rend aucun
fichier Q4 »). Le champ `base_model` du depot declare `Qwen/Qwen3-4B-Base` et la licence
Apache 2.0. **Rien ne garantit que la conversion soit fidele** ; l'empreinte verifiee
atteste du fichier telecharge, pas de la qualite de la quantification. C'est une limite du
run, ecrite ici pour n'avoir pas a l'inventer apres.

---

## 5. Les hypotheses, ecrites avant tout appel

Le referent des trois premieres est la condition `q4` de R1, dont les valeurs sont
publiees et figees : ratio de dispersion 1,174 / 1,114 / 1,059 en identite journaliste sur
gauche / centre / droite, facteur d'amplification signe H2b 0,245 [0,056 ; 0,437], facteur
non signe H2a 0,894, plancher humain 1,009.

| | enonce | direction predite | l'issue contraire, nommee d'avance |
|---|---|---|---|
| **H1** | le socle decrit la dispersion interne des camps avec un ratio `GS decrit / GS reel` **plus proche de 1** que l'instruct sous gabarit | `abs(R_q4base - 1) < abs(R_q4 - 1)` sur au moins 2 camps sur 3, identite journaliste | le socle est **plus loin** de 1 sur au moins 2 camps sur 3, c'est a dire encore plus sur dispersant que l'instruit. C'est ce que la table 4a de 2607.25292 laisse attendre : la masse sur la cible passe de 0,236 au socle a 0,442 apres RLVR, donc le post entrainement concentre et le socle disperse |
| **H2** | l'ecart entre camps decrit par le socle est **plus proche du reel** que celui de l'instruct | `abs(F_q4base - 1) < abs(F_q4 - 1)` sur H2b, identite journaliste | le socle ecrase davantage (F plus petit que 0,245) ou depasse le reel (F superieur a 1) |
| **H3** | le **format seul** explique une part mesurable de l'ecart socle contre instruit | la part `(X_q4nogab - X_q4) / (X_q4base - X_q4)` tombe dans **[0,20 ; 0,80]** pour X = F (H2b) et pour X = R (dispersion, camp de gauche) | la part n'est pas distinguable de zero, le format ne porte rien ici ; ou elle depasse 1, le format porte plus que l'ecart total et les poids agissent en sens inverse |
| **H4** | le modele est **plus proche des marginales nationales publiees du GSS** que de l'echantillon de 1 052 personnes, signe de restitution | la difference moyenne par item `TV(decrit, echantillon) - TV(decrit, national)` est **positive**, et plus grande pour l'instruit que pour le socle | difference nulle ou negative : le modele n'est pas plus proche du national que de notre echantillon, et la piste de la restitution n'est pas soutenue par ce signe |

**H3, precaution de calcul preenregistree.** Une part est un rapport de differences, et un
rapport de differences explose quand son denominateur approche zero. **La part n'est
calculee que si l'intervalle de confiance de `X_q4base - X_q4` exclut zero.** Sinon, les
trois niveaux sont publies avec leurs intervalles et la phrase est « le format et les
poids ne se separent pas sur cette quantite ». Les trois niveaux sont publies dans tous
les cas, avant toute part.

**H4, ce que le test est et ce qu'il n'est pas.** Il est construit a cout nul, sans un
appel de plus, a partir de donnees deja sur la machine.

- **Referent national** : les vagues 2016 et 2018 du panel GSS 2016-2020,
  `data/gss-panel/gss2020panel_r1a.dta`, colonnes `_1a` et `_1b`, qui sont deux echantillons
  nationaux de probabilite du GSS. C'est la source dont le GSS Data Explorer publie les
  tableaux croises. Ponderation `wtssall`. Ideologie repliee en trois blocs par la meme
  regle `GSS_BLOC3` que `a30`, apres normalisation du libelle
  « moderate, middle of the road » en « moderate ».
- **Perimetre** : les items ou au moins 99 pour cent des reponses etiquetees du panel
  s'apparient a une modalite de `question_master/gss/main.csv`, et ou chaque camp compte
  au moins 100 personnes ponderees. Le sondage de faisabilite du 8 septembre a 23:42 donne
  114 items sur 146 au dessus de 99 pour cent. [MESURE]
- **Quantite** : par (item, camp, modele), `D_ech = TV(p_decrit, p_stanford_w1)` et
  `D_nat = TV(p_decrit, p_national)`. Statistique : moyenne sur les items de
  `D_ech - D_nat`, positive si le modele est plus proche du national.
- **Controle de puissance, preenregistre.** Si la mediane par item de
  `TV(p_stanford_w1, p_national)` est **inferieure au quart** de la mediane de `D_ech`,
  les deux referents sont trop proches l'un de l'autre pour qu'un modele puisse les
  distinguer : **le test est declare sans puissance et son resultat est rapporte comme
  non concluant, jamais comme une absence d'effet.**
- **Ce que le test ne dit pas.** Il ne dit pas que le modele a lu le GSS Data Explorer. Il
  ne compare pas a Pew, dont aucune donnee n'est sur la machine et que je ne telechargerai
  pas. Un resultat positif est un **signe** de restitution, compatible avec d'autres
  explications, a commencer par le fait que l'echantillon de Stanford n'est pas un
  echantillon national et que tout modele approximativement calibre sur la population
  americaine sera mecaniquement plus proche du national.

---

## 6. Les mesures, les tests, les corrections

Les definitions sont **exactement** celles de `r1-preenregistrement.md` section 5, sans une
modification : Gini Simpson par substitution, distance de variation totale, position sur
`i / (K - 1)` orientee par `sens_codeur_A` de `a37`, ecart signe `position(droite) -
position(gauche)`, facteur d'amplification comme rapport des moyennes sur items. Les
calculs sont faits par `r1_evaluer.py`, appele sans modification, section 7.

- **Unite de reechantillonnage : l'item.** Bootstrap sur les items, 2 000 tirages,
  percentiles a 2,5 et 97,5.
- **Test principal** : permutation de signe appariee par item sur le logarithme du rapport,
  20 000 tirages, estimateur de Phipson et Smyth `(b + 1) / (m + 1)`.
- **Contrastes entre conditions** (H1, H2, H3) : les conditions partagent les items, le
  test est donc une permutation de signe **appariee par item** sur la difference des
  quantites par item entre deux conditions, jamais une comparaison d'intervalles de
  confiance a l'oeil.
- **Familles de Holm, jamais fusionnees.**

| famille | contenu | nombre de tests |
|---|---|---|
| **F1**, H1 | ratio de dispersion contre 1, 3 camps x 2 modeles nouveaux | 6 |
| **F2**, H2 | facteur d'amplification contre 1, 2 quantites (H2a, H2b) x 2 modeles nouveaux | 4 |
| **F3**, H3 | contraste apparie de format, `q4nogab` contre `q4`, 2 quantites | 2 |
| **F4**, contraste de poids | `q4base` contre `q4nogab`, 2 quantites | 2 |
| **F5**, H4 | difference `D_ech - D_nat`, 3 conditions | 3 |

- **Seuil** : 0,05 apres Holm dans la famille.
- **Bande de nullite pratique** : un rapport significatif dans [0,95 ; 1,05] est declare
  **nul en pratique**, comme en R1.
- **Perimetre principal** : les 149 items. Les deux seuls sous ensembles autorises sont
  ceux de `a37`, `oriente` (79) et `retenu_strict` (65), declares ici et pas ailleurs.
- **Aucun sous ensemble d'items choisi apres coup**, sauf le perimetre de H4, dont la
  regle de selection est ecrite ci dessus et ne depend d'aucun resultat de modele.

---

## 7. L'evaluateur, et la copie de trace

`analyses/r1_evaluer.py` est appele **sans aucune modification**, avec
`--suffixe r4`. Il lit alors `data/traces/r1-*-r4.jsonl` et, faute de referent suffixe,
retombe sur `data/traces/r1-distributions-reelles.csv`, qui est le bon fichier.

Les traces de R4 s'appellent donc `data/traces/r1-q4base-r4.jsonl`,
`r1-q4nogab-r4.jsonl` et `r1-q4hyb-r4.jsonl`.

**Une copie, declaree ici.** `data/traces/r1-q4-r4.jsonl` est une **copie octet pour octet**
de `data/traces/r1-q4.jsonl`, faite pour que l'evaluateur voie les quatre conditions dans
le meme tableau et applique Holm sur une famille commune plutot que sur deux runs
separes. Aucun appel de modele n'est refait, aucune ligne n'est modifiee, et le fichier
d'origine n'est pas touche. La copie est faite par `r4_oracle_socle.py --evaluer`, qui la
journalise, et l'empreinte des deux fichiers est publiee dans le rapport.

`VERSION_PROMPT` de R4 vaut **`r4-c3`** et non `r1-d1` : deux formats d'invite ne se
melangent pas dans un meme index de reprise. La condition copiee garde `r1-d1`, ce qui rend
la difference lisible ligne par ligne dans la trace.

Les cles de modele `q4base`, `q4nogab` et `q4hyb` sont ajoutees au registre en memoire par
`r4_oracle_socle.py`, jamais dans le fichier `r1_oracle_camps.py`, qui n'est pas modifie.
Sans cet ajout, la figure de `r1_evaluer.py` ignore les cles inconnues et rend `None` ;
les tableaux, eux, les traitent normalement.

---

## 8. Les criteres de chute, ecrits pour pouvoir perdre

Le run est **jete**, en entier ou pour un modele, si l'une de ces conditions est remplie.

1. **Plus de 25 pour cent de rejets de format pour un modele** apres relance. Sur le socle
   c'est le critere qui decide si la voie describe est praticable sans gabarit de
   conversation. `a27` publie 0,83 a 4,25 pour cent d'echec d'extraction sur quatre socles
   avec trois exemples ; un taux d'un ordre de grandeur au dessus dirait que notre invite,
   et non le socle, est en cause. **Le taux est publie des deux cotes quoi qu'il arrive**,
   parce que des denominateurs inegaux sont exactement le reproche que `a26` fait a
   2608.03044 dans sa faille F1.

   **1 bis. La sonde des 60 premieres cellules.** *Ajout du 2026-09-09 a 00:05, avant tout
   appel de modele, apres l'essai a moteur factice de la section 11.* R4 **n'a pas de
   smoke test contre un serveur vivant** : R2, puis R3, puis la file 4 occupent le GPU
   jusqu'au matin, et la consigne de la seance interdit de lancer un serveur. La sonde
   remplace ce smoke test manquant. Chaque modele passe d'abord **60 cellules**, puis son
   taux de rejet est regarde. **Au dessus de 0,50, le modele est arrete la** : son taux
   d'echec de format est publie, ce que le critere 1 prescrit deja, et les vingt minutes
   de sa place vont au modele suivant. En dessous, le meme modele reprend exactement ou
   il s'etait arrete, par le mecanisme de reprise de R1, qui ne refait aucun appel deja
   ecrit. Le seuil de 0,50 est deliberement plus haut que les 0,25 du critere 1 : la
   sonde ne sert pas a juger, elle sert a ne pas gaspiller un creneau sur un modele qui
   ne repond pas du tout.

   **Un modele qui echoue a demarrer n'emporte pas les suivants.** La boucle attrape
   l'exception, la journalise, ecrit une ligne de resume marquee `echec` et passe au
   modele d'apres. Sans cela, un socle que `llama-server` refuserait de charger
   emporterait avec lui les deux conditions instruites et il ne resterait rien de la nuit.
2. **Recopie de l'exemple de la relance**, regle de R1 inchangee : si la distribution
   decrite egale la repartition factice de l'invite de relance, la cellule sort.
3. **2 bis. Recopie des exemples a trois coups.** Nouveau critere, propre a R4, et c'est
   celui qui menace le plus ce protocole. Pour K >= 3 : si la distribution decrite egale
   exactement le vecteur de l'exemple de meme K, la cellule sort, et le taux est publie ;
   si le taux depasse 5 pour cent des cellules d'un modele, **le protocole a trois exemples
   est declare contaminant et le run de ce modele n'est pas interprete**. Pour K = 2 le
   vecteur [43, 57] est une reponse plausible : les cellules ne sont **pas** retirees, et
   le taux est publie a cote du taux de la meme valeur exacte dans les cellules K = 2 de
   `q4` sous gabarit, qui sert de taux de base.
4. **Distribution constante d'un camp a l'autre** dans plus de 90 pour cent des items : le
   modele ignore le camp et c'est ce fait la qu'on publie.
5. **Plancher humain non atteint** : le facteur calcule entre les vagues 1 et 2 des memes
   humains doit tomber dans [0,85 ; 1,15]. Il vaut 1,009 dans R1 ; s'il change, c'est que
   le referent a bouge.
6. **Referent modifie** : `data/traces/r1-distributions-reelles.csv` doit avoir la meme
   empreinte sha256 qu'au lancement de R1. Sinon rien n'est publie.
7. **Deux serveurs a la fois** : si `pgrep -x llama-server` rend plus d'un processus
   pendant le run, le run est jete. La file 5 verifie avant de lancer, et le script refuse
   de demarrer si le port n'est pas libre.

---

## 9. Ce que chaque issue voudrait dire

**Le socle decrit les camps comme l'instruit.** Le portrait est dans les poids de pre
entrainement. Le post entrainement n'est pas le coupable, et une obligation d'audit qui
viserait l'alignement viserait a cote. C'est l'issue la plus derangeante pour le
programme A, et elle est publiable telle quelle.

**Le socle est plus proche du reel que l'instruit.** Le post entrainement degrade la
fidelite de representation des camps. C'est l'issue qui porte le programme, et elle donne
une prise reglementaire directe : la quantite se degrade a une etape identifiable de la
fabrication.

**Le socle est plus loin du reel que l'instruit.** Le post entrainement corrige plutot
qu'il n'abime. `MOONSHOTS.md` perd son mecanisme, et R1 garde son resultat : la quantite
varie d'un modele a l'autre et c'est cela qui s'audite.

**Le format porte l'essentiel de l'ecart.** Alors la comparaison socle contre instruit
n'est pas mesurable sur notre materiel sans balayage de poids, et il faut le dire : ce
serait le resultat methodologique du run, et il vaudrait autant que les autres, parce
qu'il condamne d'avance toute lecture naive de la table 3 de 2607.25292.

---

## 10. Ce qui sera publie quoi qu'il arrive

`resultats/r4-oracle-socle.md`, avec : la provenance verifiee des poids et leurs
empreintes, cette page recopiee, les trois exemples reproduits en entier, la verification
hors ligne, le debit et la projection, la commande du matin, « Ce que je n'ai pas pu
verifier », « Questions ouvertes pour Simon ». Les tableaux `resultats/r1-*-r4.csv` et la
figure `resultats/r1-figure-oracle-r4.png` et `.svg`. `data/modeles/PROVENANCE-r4.md` pour
les poids. Les traces d'appel restent dans `data/traces/`, non versionnees, et ne
contiennent aucune reponse individuelle : que des distributions de groupe et le texte
produit par le modele.

Aucun fichier existant du depot n'est modifie par cette seance.

---

## 11. La verification hors ligne, faite avant le lancement de la file

*Ajout du 2026-09-09 a 00:05, avant tout appel de modele.* Aucun serveur ne pouvant etre
lance ce soir, tout ce qui pouvait etre verifie sans modele l'a ete, dans cet ordre.

1. `r4_oracle_socle.py --verifier` : les trois exemples (sommes a 100, aucun uniforme,
   aucune collision avec l'exemple de relance de R1, aucun mot politique, aucun nom
   d'item du GSS), l'empreinte du referent humain, la taille et l'empreinte des trois
   fichiers de poids, le plan de cellules, cinq essais de parse, trois essais du critere
   2 bis, l'invite complete d'une cellule reelle imprimee en entier, l'invite de relance,
   et l'injection des cles dans le registre de R1.
2. Un **essai a moteur factice** : la boucle complete de R4 sur 12 items et deux modeles,
   avec un moteur qui rend des sorties fabriquees, dont une sur 37 hors format pour
   exercer la relance et une sur 53 recopiant un exemple a trois coups. Il verifie la
   sonde, la reprise (72 cellules deja faites, aucune refaite), le comptage des recopies,
   les champs de la trace et le marqueur `RUN TERMINE`. Puis deux variantes : un moteur
   qui echoue toujours au format, pour voir le critere 1 bis s'appliquer ; un moteur dont
   le serveur refuse de demarrer, pour voir que le modele suivant part quand meme.
3. `r4_oracle_socle.py --evaluer` sur les traces reelles de R1, par la copie de
   `r1-q4.jsonl`, pour verifier que `r1_evaluer.py --suffixe r4` tourne sans une
   modification et retombe sur les valeurs publiees de R1.
4. `r4_oracle_socle.py --h4` sur ces memes traces, pour verifier que le referent national
   se construit et que le controle de puissance rend un chiffre.
5. `file_nuit_5.sh` en mode essai, sur les deux chemins : marqueur present, et heure
   limite atteinte sans marqueur.

Ce qui n'a **pas** pu etre verifie et qui reste le risque principal de la nuit est ecrit
dans le rapport : aucun appel n'a jamais ete envoye a un modele socle sous cette invite.
