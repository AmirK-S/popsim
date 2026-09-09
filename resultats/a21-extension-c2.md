# a21. Extension de C2 a 150 personnes de plus, prete a lancer

Rapport du 7 septembre 2026, 23 h 50, ecrit pendant que le run a5 tourne (C2 a
11 800 appels sur 22 350). Rien n'a ete lance, aucun serveur n'a ete demarre, aucune trace
existante n'a ete modifiee.

Scripts ecrits : `analyses/a21_extension_c2.py` (le run), `analyses/a21_evaluer_ext.py`
(l'evaluation sur les 300). `a5_agents_locaux_gss.py`, `a5_evaluer.py` et
`a18_decomposition_traces.py` n'ont pas ete touches.

---

## 1. Pourquoi

a18 section 11 point 2 : le terme inter n'est pas estimable a 55 personnes et
**probablement pas non plus a 150**. Le juge est le controle de la vague 2, qui doit
tomber au voisinage de 1 sur chaque axe ; il ne passe pas sur le genre, la race et
l'education. Doubler l'echantillon de C2 est la premiere des trois issues proposees a
Simon (a18 section 12 question 1), et la seule qui ne coute qu'une fin de nuit.

A 300 personnes, C2 se compare a v8 et a v6 sur la meme population, avec un denominateur
humain deux fois mieux estime.

---

## 2. Ce qui est pret

**`analyses/a21_extension_c2.py`**, qui n'ecrit aucune formule neuve. Il importe de a5 :
`charger`, `grille`, `nomenclature`, `systeme_c2`, `utilisateur`, `gabarit_qwen`,
`MoteurA5`, `masse_des_lettres`, `travaux`, `lancer`, `index_existant`, `chemin_trace`,
`heure_de_fin`, `port_libre`, `premier_port_libre`. Le prompt, le scoring, le seuil de
rejet, l'ordre des appels et le format de trace sont donc ceux de a5 par construction et
non par recopie.

| point | etat |
|---|---|
| Tirage | 30 personnes de plus par pli, **dans le complementaire** des 150 de `a5-personnes.csv`, graine 20260908, memes 5 plis de a2 (graine 20260903 inchangee) |
| Echantillon ecrit | `data/traces/a5-personnes-ext.csv`, colonnes `pid, index, pli`, 150 lignes [MESURE] |
| `a5-personnes.csv` | **jamais ouvert en ecriture**, lu seulement |
| Trace | `data/traces/a5-C2-p1-ext.jsonl`, fichier separe, index de reprise sur ce seul fichier |
| Condition | C2, passe 1, 149 items, 22 350 appels |
| Drapeaux | `--fin`, `--port`, `--parallele`, `--contexte`, plus `--limite`, `--attente-max`, `--verification-seule` |
| Journal | stdout, la file le redirige vers `data/traces/a5-ext.log` |
| Fin | ligne `RUN TERMINE`, meme marqueur que a5 ; serveur arrete dans un `finally` |
| Un seul serveur | `pgrep -f llama-server` avant tout demarrage ; s'il en trouve un, attente par pauses de 30 s jusqu'a `--attente-max` minutes, puis sortie sans rien ecrire |

Le suffixe `ext` a une consequence voulue et verifiee. `a5_evaluer.lire_traces("")` ne
garde que les fichiers dont le nom porte exactement deux tirets ; `a5-C2-p1-ext.jsonl` en
porte trois. **L'evaluation du matin et `a18_decomposition_traces.py` par defaut ne verront
pas cette trace** et resteront sur les 150 personnes d'origine. [MESURE, filtre rejoue sur
les cinq noms de fichiers de `data/traces/`]

**La file de nuit prevoit deja ce script**, `analyses/file_de_nuit.sh` ligne 28 :
`.venv/bin/python analyses/a21_extension_c2.py --fin 07:30 >> $T/a5-ext.log`. L'interface
ecrite correspond exactement.

**`analyses/a21_evaluer_ext.py`**, l'evaluation sur l'union des 300. L'import est possible,
mais **pas l'appel direct des deux `main()`**, pour deux raisons precises :

- `a5_evaluer.lire_traces(suffixe)` lit soit les traces sans suffixe, soit celles d'un
  suffixe donne, jamais les deux ;
- `a18_decomposition_traces.main()` lit en dur `data/traces/a5-personnes.csv` pour definir
  sa population et passe un suffixe unique a `lire_traces`.

Le script appelle donc `lire_traces` **deux fois** et fusionne les deux dictionnaires sur
la cle `(condition, passe)`, puis fait l'union des deux fichiers de population. Tout le
reste est importe sans une ligne recrite : `moyenner_passes`, `en_matrices`, `resumer`,
`ligne_texte`, `mesures_distributionnelles` de a5_evaluer ; `coder`, `masse_valide`,
`Banc`, `compter_frac`, `decomposer_frac`, `agreger2`, `_degenerer`, `MESURES` de a18 ;
`AXES`, `decomposer`, `lire_demographies`, `lire_nomenclature` de a1. Les ratios sont ceux
de a18, avec la meme correction residuelle par permutation, le meme bootstrap recentre sur
les personnes et la meme statistique P(sup).

Il calcule, sur les memes cellules pour toutes les conditions : exactitude par personne
avec IC bootstrap, normalisation par le plafond humain de ces personnes, diversite
conservee, accord par paires, exactitude esperee, entropie par appel et ECE, puis les
ratios inter et intra globaux et par axe pour C2 argmax, C2 distribution, les humains de la
vague 2 et les six conditions de Stanford, v6 et v8 comprises.

**Il mesure la meme chose sur trois populations et les met cote a cote** : les 150
d'origine, les 150 d'extension, les 300. C'est ce tableau qui repond a la question de a18 :
le controle de la vague 2 se resserre t il autour de 1 en passant de 150 a 300 sur le
genre, la race et l'education ? Si non, le probleme n'est pas la taille d'echantillon mais
l'estimateur.

**Il a ete lance sur la trace partielle en cours**, 78 personnes couvertes a 98 pour cent,
et il tourne : `CONTROLE PASSE` sur la degenerescence, ecart maximal 0,000e+00. Les
chiffres obtenus ne sont pas des resultats, la trace est partielle et l'extension n'a pas
tourne. [MESURE, essai `--rapide`]

---

## 3. La commande exacte a lancer

La file de nuit le fait seule apres C3F. Pour un lancement a la main, machine libre :

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
.venv/bin/python analyses/a21_extension_c2.py --fin 07:30 >> data/traces/a5-ext.log 2>&1
```

Le script attend de lui meme qu'aucun `llama-server` ne tourne, jusqu'a 240 minutes par
defaut, `--attente-max` pour changer cette limite.

Au matin, l'evaluation sur les 300 :

```
.venv/bin/python analyses/a21_evaluer_ext.py
.venv/bin/python analyses/a21_evaluer_ext.py --rapide            # essai, 20 s
```

L'evaluation de a5 et la decomposition a18 se lancent comme prevu, sans changement : elles
ne voient pas la trace `ext`.

---

## 4. La sortie de la verification

```
.venv/bin/python analyses/a21_extension_c2.py --verification-seule
```

```
second echantillon ecrit : .../data/traces/a5-personnes-ext.csv (150 lignes)
==========================================================================================
a21 : VERIFICATION SANS SERVEUR DE L'EXTENSION DE C2
==========================================================================================

1. Disjonction des deux echantillons
   premier echantillon  : 150 personnes, 150 index
   second echantillon   : 150 personnes, 150 index
   pid en double        : 0
   index en double      : 0
   doublons internes    : 0
   VERIFICATION PASSEE : intersection vide.
   stratification       : pli 0 : 30, pli 1 : 30, pli 2 : 30, pli 3 : 30, pli 4 : 30
   union des deux       : 300 personnes distinctes

2. Prompts C2 des 3 premieres nouvelles personnes, compares caractere pour
   caractere a celui que a5 construit pour une personne de reference.
   reference : participant_0111, premier echantillon, item spdeg*, 870 caracteres

   participant_0082 (index 81, pli 0), item spdeg*, 872 caracteres
     meme item cible que la reference        : True
     bloc utilisateur identique au caractere : True
     meme nombre de lignes de systeme        : True (16 contre 16)
     premier caractere different             : position 170 sur 591
     lignes differentes                      : 8 sur 16, toutes des lignes d'attribut : True
     preambule identique                     : True
     consigne finale identique               : True
       ligne  3 reference : - Age: 35 - 44
       ligne  3 nouvelle  : - Age: 45 - 54
       ligne  4 reference : - Census division: middle atlantic
       ligne  4 nouvelle  : - Census division: pacific
       ligne  5 reference : - Political ideology: extremely liberal
       ligne  5 nouvelle  : - Political ideology: slightly conservative
       ... 5 autres lignes d'attribut

   participant_0135 (index 134, pli 0), item spdeg*, 852 caracteres
     meme item cible que la reference        : True
     bloc utilisateur identique au caractere : True
     meme nombre de lignes de systeme        : True (16 contre 16)
     premier caractere different             : position 170 sur 591
     lignes differentes                      : 7 sur 16, toutes des lignes d'attribut : True
     preambule identique                     : True
     consigne finale identique               : True
       ligne  3 reference : - Age: 35 - 44
       ligne  3 nouvelle  : - Age: 65 - 74
       ligne  4 reference : - Census division: middle atlantic
       ligne  4 nouvelle  : - Census division: e. nor. central
       ligne  5 reference : - Political ideology: extremely liberal
       ligne  5 nouvelle  : - Political ideology: moderate
       ... 4 autres lignes d'attribut

   participant_0166 (index 165, pli 0), item spdeg*, 872 caracteres
     meme item cible que la reference        : True
     bloc utilisateur identique au caractere : True
     meme nombre de lignes de systeme        : True (16 contre 16)
     premier caractere different             : position 170 sur 591
     lignes differentes                      : 7 sur 16, toutes des lignes d'attribut : True
     preambule identique                     : True
     consigne finale identique               : True
       ligne  3 reference : - Age: 35 - 44
       ligne  3 nouvelle  : - Age: 55 - 64
       ligne  4 reference : - Census division: middle atlantic
       ligne  4 nouvelle  : - Census division: new england
       ligne  5 reference : - Political ideology: extremely liberal
       ligne  5 nouvelle  : - Political ideology: extremely conservative
       ... 4 autres lignes d'attribut

   VERIFICATION PASSEE : hors les valeurs demographiques, les prompts sont
   identiques caractere pour caractere a celui de a5. Meme preambule, meme
   consigne, meme bloc utilisateur, meme gabarit Qwen, fin sans espace.

3. Volume de calcul
   personnes          : 150
   items par personne : 149
   appels prevus      : 22350
   deja dans la trace : 0
   appels a faire     : 22350
   a  16700 appels/h : 1.34 h
   a  11000 appels/h : 2.03 h
   a   7400 appels/h : 3.02 h
   a   4900 appels/h : 4.56 h

   trace visee : .../data/traces/a5-C2-p1-ext.jsonl
   modele Qwen3-4B-Instruct-2507 Q4_K_M, version de prompt a5-p1

VERIFICATION TERMINEE. Aucun serveur lance, aucun appel de modele, aucune trace existante modifiee.
```

Deux verifications supplementaires faites en plus de celle ci.

- **Determinisme du tirage.** Deux lancements successifs donnent le meme fichier au bit
  pres, `md5 f9b2027ba6d8d30469759075e48de4ab`. [MESURE]
- **Refus de demarrer.** Lance a 23 h 46 pendant que le run a5 tourne, avec
  `--attente-max 0`, le script a bien detecte le `llama-server` PID 48437, a refuse de
  demarrer, n'a rien ecrit dans la trace et n'a pas touche au serveur en cours. [MESURE]

---

## 5. Le cout projete

Le debit reel du run a5 sur C2, releve a 23 h 45 dans `data/traces/a5-run.log`, est de
**11 694 appels par heure cumules sur 11 800 appels** [MESURE]. Les 11 000 par heure de la
consigne sont donc le bon ordre de grandeur, legerement conservateur.

| | |
|---|---|
| Appels | 150 personnes x 149 items = **22 350** |
| A 11 000 appels/h | **2 h 03** |
| A 11 694 appels/h, debit mesure ce soir | 1 h 55 |
| A 16 700 appels/h, machine dediee (a5 4.4) | 1 h 20 |
| A 7 400 appels/h, machine chargee | 3 h 01 |

**Un point a signaler sur la file de nuit.** Dans `file_de_nuit.sh`, C3F a une fin dure a
06 h 00 et l'extension prend la suite avec une fin dure a 07 h 30 : **1 h 30 de budget pour
2 h 03 de calcul**. A 11 700 appels par heure, cela laisse environ 17 500 appels, soit
**117 personnes completes sur 150** et une union de 267 personnes au lieu de 300.
[ESTIMATION] Trois issues, dans l'ordre de preference :

1. Relancer le script dans la journee sur la machine libre : il est resumable, l'index de
   reprise porte sur `a5-C2-p1-ext.jsonl` et il ne refera aucun appel deja ecrit. Il
   terminera les 33 personnes manquantes en une vingtaine de minutes.
2. Avancer la fin dure de C3F a 05 h 20, ce qui donne 2 h 10 a l'extension.
3. Accepter 117 personnes. L'ordre des appels est personne par personne, donc la
   troncature coute des personnes entieres et jamais des items, et les 117 sont
   exploitables telles quelles.

---

## 6. Ce que je n'ai pas pu verifier

1. **Aucun appel de modele n'a ete fait.** La machine est prise par le run a5 et la
   consigne interdit un second `llama-server`. Le chemin d'appel de a21 est celui de a5,
   fonction pour fonction, mais **la premiere ligne de trace de `a5-C2-p1-ext.jsonl` n'a
   pas ete produite**. Un smoke test de trois appels reste a faire au demarrage reel, et le
   journal du run le montrera : la ligne `tokens verifies pour K=...` doit apparaitre,
   comme en a5.
2. **La reprise n'a pas ete verifiee en conditions reelles sur ce fichier.** Elle l'a ete
   en a5 sur `a5-C2-p1.jsonl`, avec la meme fonction `index_existant` et la meme cle
   `(pid, item)`. Le fichier `ext` etant vide, `0 appels deja faits` est le seul etat teste.
3. **Le debit de l'extension est suppose egal a celui de C2 ce soir.** Il depend de la
   charge de la machine a 06 h 00, que je ne connais pas, et a5 section 4.4 mesure un
   facteur 9,5 entre un et deux serveurs. Le chiffre de 2 h 03 vaut machine libre.
4. **`a21_evaluer_ext.py` n'a jamais tourne sur une trace `ext`**, qui n'existe pas. Il a
   tourne sur la trace de a5 partielle, 78 personnes, ou la sous population "150
   d'extension" est vide et sautee. Le chemin a trois populations n'a donc ete exerce que
   sur deux d'entre elles.
5. **Le controle de la vague 2 a 300 personnes est inconnu.** C'est toute la question du
   chantier et elle ne sera tranchee qu'au matin. Sur les 78 personnes disponibles, l'ecart
   a 1 est de 0,39 sur le genre et 0,44 sur la race [MESURE, trace partielle, essai
   `--rapide`] : rien ne permet d'en extrapoler la valeur a 300.
6. **La passe 2 n'est pas dans ce chantier.** L'extension est en passe 1 seulement, comme
   a5. Le biais de position reste non mesure, et il vaut pour les 300 comme pour les 150.
7. **Rien n'est fait pour C3.** Doubler C3 couterait environ 4 h 30 de plus et ne rentre
   dans aucune fenetre de cette nuit. La comparaison C2 contre C3 restera donc sur 150
   personnes, et seule C2 aura ses 300.

---

## Fichiers produits

| fichier | contenu |
|---|---|
| `analyses/a21_extension_c2.py` | le run d'extension, importe a5, n'en modifie rien |
| `analyses/a21_evaluer_ext.py` | l'evaluation sur l'union, importe a5_evaluer, a18 et a1 |
| `data/traces/a5-personnes-ext.csv` | les 150 nouvelles personnes, deja ecrit [MESURE] |
| `data/traces/a5-C2-p1-ext.jsonl` | la trace, a produire |
| `resultats/a21-extension-c2.json`, `a21-decomposition.csv`, `a21-ratios-par-axe.csv` | sorties de l'evaluation |
