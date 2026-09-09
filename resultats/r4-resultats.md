# r4. Le socle contre l'instruit : le format d'invite porte plus que les poids

Run de la file 5, parti le 2026-09-09 a 08:03:16, termine a 08:51:31, marqueur `RUN TERMINE`
dans `data/traces/r4-run.log`. Trois conditions de 894 cellules, 2 682 appels locaux,
48 minutes 15 secondes de machine, zero euro, rien n'est sorti de la machine. Evaluation par
`analyses/r1_evaluer.py --suffixe r4`, sans une modification de son fichier, puis par
`analyses/r4b_contrastes.py`, `r4b_diagnostic.py` et `r4b_figure.py`, ecrits pour ce rapport,
qui ne font aucun appel de modele et ne touchent aucun script existant.

Page de plan : `resultats/r4-preenregistrement.md`, horodatee le 2026-09-08 a 23:45.
Preparation et provenance des poids : `resultats/r4-oracle-socle.md`.
Reserve d'anteriorite a lire avant tout : `resultats/bilan-predictions.md` section 2 mesure
que le tableau H4 `r4-h4-restitution.csv` existait a 23:52 alors que la page de plan a ete
modifiee pour la derniere fois a 23:57:57, et qu'aucune page de plan du projet n'a jamais ete
deposee hors de la machine. La ligne `q4` de H4 est donc, de l'aveu de la page elle meme, une
analyse a posteriori ; H4 n'est prospective que pour `q4base`, `q4nogab` et `q4hyb`.

Conventions de certitude : **[MESURE]** calcule ici sur nos donnees, **[CONFIRME]** lu dans
une source verifiee, **[PROBABLE]** interpretation etayee mais non demontree,
**[HYPOTHESE]** proposition a tester.

---

## Reponse en une ligne

**Sur la quantite centrale du programme A, l'ecart entre camps decrit, changer le format
d'invite sans toucher un seul poids deplace la mesure de +0,48 [+0,29 ; +0,68], soit une
marche plus grande que l'ecart total entre le socle et l'instruit, +0,32 [+0,13 ; +0,52] :
le meme fichier GGUF de `Qwen3-4B-Instruct-2507` passe de 0,245 fois le reel sous gabarit de
conversation a 0,727 en completion a trois exemples, le socle donne 0,566 sous ce meme
format, et le successeur apparie du socle, `Qwen3-4B`, retombe a 0,262, c'est a dire
exactement la valeur de l'instruit sous gabarit, +0,017 [-0,15 ; +0,17], p = 0,84 ; les
quatre conditions sur decrivent la variete interne des camps, les quatre changent de portrait
selon qui demande de 2,1 a 5,0 fois le plancher humain, et les quatre se trompent de dix fois
ce plancher.** [MESURE]

**Consequence pour l'audit : la quantite auditee depend du format d'invite au moins autant
que des poids, et le registre des versions du programme A doit inclure le format, sans quoi
deux auditeurs mesurant le meme modele publieront des chiffres qui different d'un facteur
trois.** [MESURE pour le fait, PROBABLE pour la portee]

---

## Protocole rappele, en huit lignes

149 items du GSS x 3 camps (gauche 417, centre 303, droite 332) x 2 identites de demandeur
(journaliste neutre, membre du camp adverse) = 894 cellules par condition, un appel par
cellule, temperature 0, `top_k` 1, un serveur a la fois, moteur `MoteurR1` de
`r1_oracle_camps.py` importe et jamais recopie. Quatre conditions : `q4`, l'instruct-2507 sous
gabarit ChatML, **non rejouee**, copie octet pour octet de la trace de R1 ; `q4nogab`, **le
meme fichier GGUF** en completion a trois exemples ; `q4base`, `Qwen3-4B-Base` sous ce meme
format ; `q4hyb`, `Qwen3-4B`, le successeur apparie du socle selon `a27` section 4.4, sous ce
meme format. Referent humain : `data/traces/r1-distributions-reelles.csv`, empreinte verifiee
identique a celle de R1 ; plancher de bruit : les memes 1 052 personnes reinterrogees a deux
semaines. Bootstrap sur les items, 2 000 tirages ; permutation de signe appariee par item,
20 000 tirages, estimateur de Phipson et Smyth ; Holm a l'interieur des cinq familles
preenregistrees F1 a F5 et jamais entre elles ; bande de nullite pratique [0,95 ; 1,05].
Les contrastes entre conditions sont apparies par item, sur le perimetre des items valides
dans les deux conditions comparees, comme la page de plan section 6 le prescrit.

**Le contraste `q4base` contre `q4nogab` est declare non apparie**, ici comme partout ailleurs :
`Qwen3-4B-Instruct-2507` n'est pas le descendant de `Qwen3-4B-Base`. La paire appariee est
`q4base` contre `q4hyb`, tous deux publies le 26 juillet 2025. [CONFIRME, `a27`, dates de
l'API Hugging Face]

---

## 0. Les criteres de chute, avant tout chiffre

| critere | q4 | q4nogab | q4base | q4hyb | verdict |
|---|---|---|---|---|---|
| 1. rejet de parse apres relance, seuil 0,25 | 0,000 | 0,001 | 0,000 | **0,025** | les quatre passent |
| 1 bis. sonde des 60 premieres cellules, seuil 0,50 | sans objet | 0,000 | 0,000 | 0,017 | les trois passent |
| 2. recopie de l'exemple de la relance | 11 sur 13 | **15 sur 15** | **24 sur 24** | **6 sur 6** | chute, 56 cellules retirees |
| 2 bis. recopie d'un exemple a trois coups, K >= 3 | 0 | **0** | **0** | **0** | passe, seuil 0,05 |
| 3. distribution identique d'un camp a l'autre, seuil 0,90 | 0,197 | 0,131 | 0,328 | 0,472 | les quatre passent |
| 4. plancher humain, facteur w2 sur w1, bande [0,85 ; 1,15] | 1,009 | | | | passe |
| 5. effectifs des camps | 417 / 303 / 332 | | | | passe |
| 6. empreinte du referent humain | `ea7cd93e...91c811` | | | | inchangee |
| 7. deux serveurs a la fois | aucun | | | | passe, un serveur par condition, journalise |
| regle des 90 pour cent pour `q4hyb` | | | | **894 sur 894** | condition de mesure, pas seulement de format |

[MESURE, `resultats/r1-controles-r4.csv`, `data/traces/r4-resume.json`, `r4-run.log`]

Perimetre lu 3 576 cellules, 23 rejets de parse, 56 cellules retirees au critere 2,
**perimetre exploite 3 497 cellules, 97,8 pour cent**.

**Une note de comptage sur Holm, valable pour tout ce rapport.** Les familles F1 et F2 etaient
preenregistrees a 6 et 4 tests, « 2 modeles nouveaux » ; le run en a trois, et l'evaluateur
applique Holm sur toutes les lignes de son tableau, la copie de `q4` comprise : **24 tests pour
F1 et 8 par perimetre pour F2**, la ou la page en prevoyait 6 et 4. La correction effectivement
appliquee est donc **plus severe** que la correction preenregistree, jamais plus permissive :
aucun verdict de ce rapport n'est obtenu par une famille trop petite. La seule consequence
lisible est en sens inverse, sur H4, section 1.4.

**Le critere 2 bis est le seul qui pouvait tuer le protocole, et il passe largement.** Aucune
cellule d'aucune condition, sur les 318 cellules a K = 3 et les 24 a K = 6, ne recopie le
vecteur de l'exemple correspondant. A K = 2, ou la page de plan interdit de retirer les
cellules parce que [43 ; 57] est une reponse plausible, le taux vaut 3 sur 312 pour `q4base`
(0,96 pour cent) et 1 sur 312 pour `q4hyb` (0,32 pour cent), contre 0 sur 312 pour les deux
conditions instruct-2507, qui servent de taux de base. **L'invite a trois exemples de forme
identique a la tache n'est donc pas contaminante a la mesure de ce critere**, et la question 6
posee a Simon en `r4-oracle-socle.md` peut se refermer sans refaire le run. [MESURE,
`resultats/r4b-2bis.csv`]

---

## 1. Les quatre hypotheses preenregistrees, condition par condition

### 1.1 H1, la dispersion interne : rejetee, et le socle n'est pas moins sur dispersant

Enonce preenregistre : `abs(R_q4base - 1) < abs(R_q4 - 1)` sur au moins 2 camps sur 3, en
identite journaliste. Issue contraire nommee d'avance : le socle est **plus loin** de 1, donc
encore plus sur dispersant, ce que la table 4a de 2607.25292 laisse attendre.

Ratio `GS decrit / GS reel`, identite journaliste, plancher humain entre parentheses
[MESURE, `resultats/r1-h1-unanimite-r4.csv`]

| camp | `q4`, gabarit | `q4nogab`, completion | `q4base`, socle | `q4hyb`, hybride | plancher |
|---|---|---|---|---|---|
| gauche | **1,174** [1,112 ; 1,247] | **1,101** [1,035 ; 1,179] *ns* | **1,164** [1,092 ; 1,244] | **1,273** [1,204 ; 1,357] | *1,005* |
| centre | **1,114** [1,063 ; 1,174] | 1,122 [1,073 ; 1,177] *ns* | **1,147** [1,095 ; 1,204] | **1,183** [1,129 ; 1,244] | *1,007* |
| droite | **1,059** [1,013 ; 1,115] | **1,090** [1,044 ; 1,144] | **1,081** [1,032 ; 1,138] | **1,152** [1,099 ; 1,209] | *0,996* |

**H1 est fausse.** Le socle n'est plus proche de 1 que sur le camp de gauche, et il en est
plus loin sur le centre et sur la droite : **1 camp sur 3**, la ou 2 sur 3 etaient exiges.
L'issue contraire nommee d'avance se realise sur deux camps. Et le contraste apparie sur le
camp de gauche, le seul des trois ou le socle ait l'air meilleur, **n'est pas decidable** :
`q4base` moins `q4` vaut -0,009 [-0,064 ; +0,042], p = 0,73. [MESURE,
`resultats/r4b-contraste-h1.csv`]

**La condition appariee aggrave le verdict.** `q4hyb`, qui est le vrai descendant du socle,
sur decrit **plus** que le socle sur les trois camps, +0,11, +0,04 et +0,07 de ratio. Si l'on
lit la paire appariee, le post entrainement **augmente** la sur dispersion, ce qui est le sens
que 2607.25292 predit et le sens contraire de H1.

Les quatre conditions restent au dessus de 1 sur tous les camps sauf deux cellules non
significatives : **aucun format et aucun jeu de poids ne fait decrire un camp comme plus
unanime qu'il n'est.** C'est le resultat le plus stable des deux runs.

### 1.2 H2, l'ecart entre camps : tenue a la lettre, retournee par son propre controle

Enonce preenregistre : `abs(F_q4base - 1) < abs(F_q4 - 1)` sur H2b, identite journaliste.

Facteur d'amplification signe, **79 items orientes de `a37`**
[MESURE, `resultats/r1-h2-ecart-r4.csv`]

| condition | journaliste | adversaire | verdict Holm dans F2 |
|---|---|---|---|
| `q4`, instruct-2507, gabarit ChatML (R1) | **0,245** [0,059 ; 0,432] | **0,221** [0,054 ; 0,389] | attenuation |
| `q4nogab`, **le meme fichier**, completion 3 ex. | 0,727 [0,476 ; 0,988] | 0,859 [0,537 ; 1,186] | non significatif |
| `q4base`, socle, completion 3 ex. | **0,566** [0,365 ; 0,785] | **0,440** [0,145 ; 0,730] | attenuation |
| `q4hyb`, hybride apparie, completion 3 ex. | **0,262** [0,113 ; 0,410] | **0,202** [0,056 ; 0,356] | attenuation |
| *plancher humain* | *1,009* | *1,009* | |

Sur les **65 items retenus stricts** : 0,304 / 0,810 / 0,574 / 0,275 en identite journaliste.
Le classement des quatre conditions est le meme sur les deux perimetres et sur les deux
identites.

**H2 est tenue a la lettre** : `abs(0,566 - 1) = 0,434` est bien inferieur a
`abs(0,245 - 1) = 0,755`, et le contraste apparie `q4base` moins `q4` vaut
**+0,321 [+0,134 ; +0,518], p = 0,0022** [MESURE]. Ce contraste n'appartient a aucune des cinq
familles preenregistrees, qui ne prevoient que `q4nogab` contre `q4` (F3) et `q4base` contre
`q4nogab` (F4) ; il est donc publie avec son p brut et declare comme tel.

**Et elle est retournee par le controle que la meme page de plan imposait.** Sous le meme
format, le socle est **plus loin** du reel que l'instruct-2507, pas plus pres :
`q4base` moins `q4nogab` vaut **-0,161 [-0,336 ; +0,010], p de Holm 0,068** sur les 79 items
orientes, et **-0,237 [-0,428 ; -0,055], p = 0,011** sur les 65 items stricts. La premiere
n'est pas decidable, la seconde l'est. **Toute la confirmation de H2, et davantage, vient du
changement de format.** C'est l'objet de la section 2.

### 1.3 H3, la part du format : fausse, et dans le sens que la page avait nomme

Enonce preenregistre : la part `(X_q4nogab - X_q4) / (X_q4base - X_q4)` tombe dans
**[0,20 ; 0,80]** pour X = facteur H2b et pour X = ratio de dispersion du camp de gauche.
Issue contraire nommee d'avance : « elle depasse 1, le format porte plus que l'ecart total et
les poids agissent en sens inverse ».

Precaution preenregistree : la part n'est calculee que si l'IC de `X_q4base - X_q4` exclut
zero ; sinon la phrase imposee est « le format et les poids ne se separent pas sur cette
quantite ».

[MESURE, `resultats/r4b-part-format.csv`, perimetre commun aux quatre conditions]

| quantite | identite | X sous gabarit | X completion | X socle | numerateur, format | denominateur, socle moins gabarit | part |
|---|---|---|---|---|---|---|---|
| facteur H2b, 79 items orientes | journaliste | 0,245 | 0,727 | 0,566 | **+0,482** [+0,288 ; +0,675] | **+0,321** [+0,134 ; +0,518] | **1,50** [1,00 ; 2,90] |
| facteur H2b, 79 items orientes | adversaire | 0,230 | 0,885 | 0,482 | **+0,655** | **+0,251** | **2,61** [1,28 ; 11,59] |
| ratio H1, camp gauche | journaliste | 1,176 | 1,095 | 1,175 | -0,082 | -0,001 [-0,055 ; +0,052] | **non calculee** |
| ratio H1, camp centre | journaliste | 1,106 | 1,115 | 1,143 | +0,009 | +0,037 | 0,25 [-1,24 ; 1,01] |
| ratio H1, camp droite | journaliste | 1,066 | 1,097 | 1,089 | +0,031 | +0,024 | **non calculee** |

**H3 est fausse sur la quantite qui porte le programme.** La part vaut 1,50 en identite
journaliste et 2,61 en identite adverse, toutes deux hors de la bande [0,20 ; 0,80], et l'IC
de la premiere exclut 0,80 par le bas. **Le format porte plus que l'ecart total, et les poids
du socle agissent en sens inverse** : c'est mot pour mot l'issue contraire que la page de plan
avait nommee d'avance, et c'est la seule prediction de R4 qui pouvait couter.

**Sur la dispersion, la phrase imposee s'applique.** Pour le camp de gauche, l'IC du
denominateur, -0,001 [-0,055 ; +0,052], contient zero : **le format et les poids ne se
separent pas sur cette quantite.** Ils ne se separent pas parce qu'ils s'annulent : le format
seul vaut -0,076 [-0,118 ; -0,037], p de Holm 0,0001, et les poids seuls +0,069
[+0,017 ; +0,123], p de Holm 0,0147, deux effets decidables, de signes opposes, de meme
taille. Le camp de droite est dans le meme cas. [MESURE, `resultats/r4b-contraste-h1.csv`]

### 1.4 H4, les marginales nationales : non soutenue sur les trois conditions prospectives

Enonce preenregistre : la difference moyenne par item `TV(decrit, echantillon) -
TV(decrit, national)` est **positive**, et plus grande pour l'instruit que pour le socle.
Perimetre : 112 items sur 145, regle de selection ecrite avant tout resultat de modele.
Controle de puissance : la mediane par item de `TV(echantillon, national)` vaut **0,107**,
soit **46 pour cent** de la mediane de `D_ech`, 0,233 ; le seuil preenregistre etait 25 pour
cent, **le test a de la puissance**. [MESURE, `resultats/r4-h4-restitution.csv`]

| condition | identite | difference | IC 95 % | p | p de Holm |
|---|---|---|---|---|---|
| `q4`, gabarit, **a posteriori** | journaliste | **+0,0215** | [+0,0037 ; +0,0395] | 0,0217 | 0,0870 |
| `q4`, gabarit, **a posteriori** | adversaire | **+0,0240** | [+0,0046 ; +0,0425] | 0,0120 | **0,0482** |
| `q4nogab`, prospective | journaliste | -0,0062 | [-0,0232 ; +0,0118] | 0,51 | 1,00 |
| `q4nogab`, prospective | adversaire | +0,0051 | [-0,0128 ; +0,0235] | 0,61 | 1,00 |
| `q4base`, prospective | journaliste | -0,0057 | [-0,0238 ; +0,0118] | 0,53 | 1,00 |
| `q4base`, prospective | adversaire | -0,0021 | [-0,0175 ; +0,0139] | 0,80 | 1,00 |
| `q4hyb`, prospective | journaliste | +0,0052 | [-0,0132 ; +0,0252] | 0,60 | 1,00 |
| `q4hyb`, prospective | adversaire | +0,0088 | [-0,0106 ; +0,0276] | 0,37 | 1,00 |

**H4 n'est pas soutenue.** Aucune des six cellules prospectives n'est decidable, et deux des
trois du socle sont de signe negatif. Le seul signe positif de tout le dispositif est celui de
la condition declaree a posteriori.

**Deux precisions de comptage qu'il faut ecrire.** Un, la famille F5 etait preenregistree a
**trois** tests, les trois conditions prospectives ; l'evaluateur a applique Holm sur
**quatre** conditions par identite, la copie de `q4` comprise. Sous la famille preenregistree
a trois tests, aucune ligne prospective ne passe, ce qui ne change rien. Deux, sous la famille
de quatre effectivement appliquee, **la ligne `q4` journaliste ne passe plus le seuil**,
0,0870 apres Holm, la ou `r4-oracle-socle.md` publiait 0,0217 quand elle etait seule dans sa
famille. La phrase de tete de ce rapport de preparation, « p = 0,022 », est donc a lire comme
un p brut ; la ligne adverse, elle, passe a 0,0482. [MESURE]

**Le contraste, qui est ce qui rendait le test interessant.** [MESURE,
`resultats/r4b-contraste-h4.csv`, apparie par (item, camp), 336 cellules]

| contraste | identite | ecart | IC 95 % | p de Holm |
|---|---|---|---|---|
| format seul, `q4nogab` moins `q4` | journaliste | **-0,0277** | [-0,0398 ; -0,0155] | **0,00025** |
| poids seuls, `q4base` moins `q4nogab` | journaliste | +0,0005 | [-0,0118 ; +0,0131] | 0,94 |
| socle contre gabarit, `q4base` moins `q4` | journaliste | **-0,0272** | [-0,0428 ; -0,0111] | **0,0044** |
| format seul, `q4nogab` moins `q4` | adversaire | **-0,0189** | [-0,0302 ; -0,0079] | **0,0050** |
| poids seuls, `q4base` moins `q4nogab` | adversaire | -0,0071 | [-0,0187 ; +0,0046] | 0,59 |

**L'attraction vers les marginales nationales est portee par le gabarit de conversation, pas
par les poids de pre entrainement.** Le changement de format, a poids identiques, l'annule
entierement, -0,028 sur une valeur de +0,022 ; le changement de poids, a format identique, ne
la deplace pas, +0,0005, p = 0,94. **Cela ne leve pas l'objection de contamination et rien
dans ce rapport ne le dira** : le socle a lu le meme internet. Ce que cela dit est plus
etroit et plus utile : **le seul signe positif que nous ayons jamais mesure en faveur de la
restitution n'est pas dans les poids, il apparait avec le gabarit.** [MESURE pour les
contrastes, PROBABLE pour la lecture]

### 1.5 H3 de R1, l'identite du demandeur : confirmee sur les huit cellules, socle compris

Ce n'est pas une hypothese de la page R4, c'est une quantite que l'evaluateur produit pour
toute condition, et c'est le resultat le plus derangeant du run.

[MESURE, `resultats/r1-h3-identite-r4.csv`, p de Holm 0,0004 partout]

| condition | gauche | droite | items identiques, droite |
|---|---|---|---|
| `q4`, gabarit | **3,07** [2,41 ; 3,91] | **3,09** [2,49 ; 3,79] | 0,27 |
| `q4nogab`, completion | **3,37** [2,64 ; 4,18] | **4,20** [3,45 ; 4,98] | 0,19 |
| `q4base`, **socle** | **3,27** [2,31 ; 4,46] | **5,05** [3,88 ; 6,35] | 0,29 |
| `q4hyb`, hybride | **2,46** [1,82 ; 3,27] | **2,12** [1,64 ; 2,64] | 0,51 |

**Un modele socle, sans aucun post entrainement, change le portrait qu'il fait du camp de
droite selon que la question vient d'un journaliste ou d'un membre du camp adverse, de 5,0
fois le bruit de reinterrogation d'un panel humain**, plus que n'importe laquelle des trois
conditions instruites. La dependance au demandeur n'est donc pas une propriete de
l'alignement : elle est deja dans les poids de pre entrainement. [MESURE]

### 1.6 Le score des predictions

| | enonce | direction declaree au bilan | verdict |
|---|---|---|---|
| H1 | le socle est plus pres de 1 que l'instruit sur 2 camps sur 3 | en faveur | **fausse**, 1 sur 3, et l'issue contraire se realise sur 2 sur 3 |
| H2 | l'ecart du socle est plus pres du reel sur H2b | en faveur | **tenue a la lettre**, et retournee par le controle de format que la meme page imposait |
| H3 | la part du format tombe dans [0,20 ; 0,80] | neutre | **fausse**, 1,50 et 2,61, l'issue contraire nommee d'avance |
| H4 | le modele est plus pres du national, et l'instruit plus que le socle | en faveur | **non soutenue** sur les six cellules prospectives |

**Trois predictions sur quatre tombent, dont les deux qui etaient declarees en faveur de la
these, et la seule qui tient le fait a la lettre en etant retournee par son propre controle.**
Comme R2, R4 est un run ou les paris ecrits en notre faveur ne passent pas. La seule
prediction du lot qui pouvait couter, H3, coute. [MESURE, contre
`resultats/bilan-predictions.md` section 4]

---

## 2. La decomposition qui compte

### 2.1 Le format seul, poids tenus fixes, sur le meme fichier GGUF

`q4` et `q4nogab` sont **le meme fichier**, `Qwen3-4B-Instruct-2507-Q4_K_M.gguf`, meme
empreinte, meme moteur, memes parametres d'appel, meme referent humain, memes 894 cellules.
La seule difference est le gabarit ChatML d'un cote, l'invite de completion a trois exemples
de l'autre.

| quantite, identite journaliste | `q4` | `q4nogab` | contraste apparie | p de Holm dans F3 |
|---|---|---|---|---|
| facteur H2b, 79 items orientes | 0,245 | 0,727 | **+0,482** [+0,288 ; +0,675] | **0,0001** |
| facteur H2b, 65 items stricts | 0,304 | 0,810 | **+0,506** [+0,291 ; +0,725] | brut 0,00005 |
| ratio H1, camp gauche | 1,176 | 1,095 | **-0,076** [-0,118 ; -0,037] | **0,0001** |
| H4, attraction nationale | +0,0215 | -0,0062 | **-0,0277** [-0,0398 ; -0,0155] | brut 0,00005 |
| retrecissement vers l'uniforme, `alpha` median (note) | 0,339 | 0,385 | | |
| erreur `TV(decrit, reel)` en part du plancher | 10,3 | 9,6 | | |

[MESURE, `resultats/r4b-contraste-h2b.csv`, `r4b-contraste-h1.csv`, `r4b-contraste-h4.csv`,
`r4b-alpha-uniforme.csv`]

*Note sur `alpha`.* C'est une quantite **declaree apres coup**, dans l'esprit de `r1` section
3.3 : `p_decrit = alpha x p_reel + (1 - alpha) x uniforme`, ajuste sans constante sur les ecarts
a l'uniforme, cellule par cellule, puis mediane. Recalculee ici, elle rend 0,339 pour `q4` en
identite journaliste, la ou `r1` publiait 0,332 sur les deux identites reunies ; l'ecart est
celui du perimetre, pas d'une divergence de definition. Seule la mediane est publiee, la moyenne
etant dominee par quelques cellules a denominateur minuscule.

**Le format seul explique donc, sur la quantite H2b, une part de 1,50 [1,00 ; 2,90] de l'ecart
socle contre instruit : plus que la totalite.** `a27` section 4.4 annonçait, sur les chiffres
des auteurs de 2607.25292, que le format vaudrait « la moitie » de l'ecart base contre
instruct, 0,081 de TV contre 0,15. **Chez nous, sur cette quantite, il en vaut une fois et
demie.** L'avertissement de `a27` etait juste dans sa direction et trop faible dans son
ampleur. [MESURE ; CONFIRME pour le chiffre de `a27`]

**Ce n'est pas un artefact de rejets ni de perimetre.** Sur les 79 items orientes, aucune
condition ne perd de cellule : les quatre contrastes sont calcules sur les 79 memes items. La
sensibilite au perimetre strictement commun aux quatre conditions rend les memes chiffres au
millieme. [MESURE, `resultats/r4b-sensibilite-perimetre.csv`]

### 2.2 Les poids seuls, format tenu fixe : l'alignement rapproche des humains, il n'eloigne pas

| quantite, identite journaliste | `q4base`, socle | `q4nogab`, instruit | contraste apparie | p |
|---|---|---|---|---|
| facteur H2b, 79 items orientes | 0,566 | 0,727 | **-0,161** [-0,336 ; +0,010] | Holm F4 0,068 |
| facteur H2b, 65 items stricts | 0,574 | 0,810 | **-0,237** [-0,428 ; -0,055] | brut 0,011 |
| ratio H1, camp gauche | 1,175 | 1,095 | **+0,069** [+0,017 ; +0,123] | Holm F4 0,0147 |
| H4, attraction nationale | -0,0057 | -0,0062 | +0,0005 [-0,0118 ; +0,0131] | 0,94 |
| erreur `TV(decrit, reel)` en part du plancher | 10,5 | 9,6 | | |

**Sur l'ecart entre camps, l'alignement rapproche des humains.** Le socle ecrase davantage que
l'instruct-2507 sous le meme format, decidable sur le perimetre strict et non decidable sur le
perimetre principal. **Sur la dispersion interne, l'alignement rapproche aussi** : le socle est
plus loin de 1 que l'instruct, +0,069, decidable dans F4. **Sur l'erreur globale, l'instruct
est meilleur** : 9,6 fois le plancher contre 10,5.

**Cela va contre le mecanisme que `MOONSHOTS.md` programme A esperait**, et contre la lecture
naive de la table 3 de 2607.25292 dans notre cadre. Attention a ne pas sur lire : leur table 3
mesure la capacite a echantillonner une loi ecrite dans l'invite, pas la fidelite a un referent
humain ; `a27` section 2.2 le dit au mot. Nos deux quantites ne sont pas les leurs, et notre
resultat ne contredit pas le leur. [MESURE ; CONFIRME pour la distinction]

**Deux limites qui ne peuvent pas etre levees par ce run.** Le contraste est **non apparie** :
`q4base` n'est pas l'ancetre de `q4nogab`. Et la quantification du socle vient d'un depot tiers,
`mradermacher`, dont le procede est inconnu ; une difference de procede se lirait comme une
difference de poids. [MESURE pour le fait, `r4-oracle-socle.md` 1.2]

### 2.3 L'hybride apparie : il se comporte comme l'instruct sous gabarit, et il dit pourquoi

`q4hyb` est `Qwen/Qwen3-4B`, publie le meme jour que le socle, **le seul contraste apparie du
run**. Il recoit exactement la meme invite de completion a trois exemples que `q4nogab` et
`q4base`.

| contraste, 79 items orientes, journaliste | ecart | IC 95 % | p |
|---|---|---|---|
| `q4hyb` contre `q4`, l'instruct **sous gabarit** | **+0,017** | [-0,153 ; +0,174] | **0,84** |
| `q4hyb` contre `q4nogab`, l'instruct **sous le meme format** | **-0,465** | [-0,654 ; -0,289] | **0,00005** |

Sur les 65 items stricts, -0,029 [-0,206 ; +0,150], p = 0,75 contre `q4`, et
-0,535 [-0,751 ; -0,338], p = 0,00005 contre `q4nogab`. [MESURE]

**En completion, sans le moindre gabarit de conversation, `Qwen3-4B` produit la meme mesure
que `Qwen3-4B-Instruct-2507` sous gabarit ChatML, a 0,017 pres, et une mesure trois fois plus
petite que celle du meme instruct sous la meme invite que lui.**

**Pourquoi : il reconstruit le tour de conversation que l'invite ne lui donne pas.** Les
marqueurs, cherches a l'identique dans les quatre conditions, sont comptes sur les 907 a 922
sorties brutes de chacune [MESURE, `resultats/r4b-marqueurs-gabarit.csv`] :

| marqueur dans la sortie brute | `q4` | `q4nogab` | `q4base` | `q4hyb` | dont relances de `q4hyb` |
|---|---|---|---|---|---|
| separateur d'exemple `----` | 0 | 0 | **0** | 18 | 18 sur 28, **64 %** |
| annonce d'une question nouvelle (« Now, the actual question ») | 0 | 1 | **0** | 16 | 16 sur 28, **57 %** |
| auto correction en cours de reponse (« Wait, », « The final answer ») | 0 | 0 | **0** | 18 | 12 sur 28, **43 %** |
| balise `\boxed` | 0 | 0 | **0** | 1 | 1 |

Sur les 918 sorties du socle, **aucune** de ces quatre marques. Sur celles de `q4hyb`, la
sortie typique d'une relance est :

```
----

Now, here's the actual question for you. The question is:
"Which of the following is the best way to describe your political views?"
...
The final answer is:
A: 12
B: 20
...
The answer is \boxed{A:
```

**Le modele n'a pas repondu a la question posee : il a ecrit un quatrieme exemple, avec une
question qu'il a inventee, et il a range sa reponse dans une balise de resultat
mathematique.** [MESURE, `data/traces/r1-q4hyb-r4.jsonl`]

**Lecture.** `Qwen3-4B` est le point de controle hybride de la famille, celui qui porte le
mode raisonnement ; son post entrainement lui a appris un tour d'assistant si fortement qu'il
le **reimpose de lui meme** quand l'invite ne le lui donne pas. Le socle, qui n'a rien appris
de tel, se laisse conduire par les trois exemples ; l'instruct-2507, non hybride, aussi. C'est
l'hypothese du **gabarit implicite** posee dans la mission, et elle est soutenue par une mesure
directe et non par le seul niveau des facteurs. **Elle explique pourquoi les deux conditions
qui produisent 0,25 sont exactement les deux ou un gabarit de conversation est en vigueur, l'un
donne par nous, l'autre reconstruit par le modele.** [MESURE pour les marqueurs, **PROBABLE**
pour le mecanisme : rien ici ne montre que le gabarit reconstruit **cause** l'ecrasement, seule
leur coincidence est mesuree, sur une condition]

**Ce que l'hybride ne fait pas comme l'instruct sous gabarit.** Il ecrase l'ecart par
**indifference** : 50,0 pour cent de ses items donnent la meme distribution a la gauche et a la
droite, contre 14,3 pour cent pour `q4` sous gabarit. Meme mesure, mecanisme different.
[MESURE, `resultats/r4b-indifference.csv`]

### 2.4 Le tableau d'ensemble, quatre conditions

| | `q4` gabarit | `q4nogab` completion | `q4base` socle | `q4hyb` hybride |
|---|---|---|---|---|
| facteur H2b, journaliste | 0,245 | **0,727** | 0,566 | 0,262 |
| ratio H1 gauche, journaliste | 1,174 | 1,101 | 1,164 | **1,273** |
| identite du demandeur, droite | 3,09 | 4,20 | **5,05** | 2,12 |
| attraction nationale, journaliste | **+0,022** | -0,006 | -0,006 | +0,005 |
| erreur en part du plancher humain | 10,3 | **9,6** | 10,5 | 10,1 |
| `alpha`, retrecissement vers l'uniforme | 0,339 | **0,385** | 0,264 | 0,263 |
| items ou les deux camps recoivent la meme distribution | 0,143 | 0,184 | 0,448 | **0,500** |
| rejets apres relance | 0 | 1 | 0 | **22** |

**Aucune condition n'est bonne.** Les quatre se trompent de neuf a dix fois le plancher humain
et retrecissent les distributions vers l'uniforme d'un facteur trois a quatre. La dispersion
entre les quatre conditions d'un **meme modele de 4 milliards de parametres**, facteur 3,0 sur
H2b entre 0,245 et 0,727, est du meme ordre que la dispersion entre les **trois familles de
modeles** de R1, facteur 5,2. [MESURE]

---

## 3. Les rejets, et la sensibilite

### 3.1 Le socle suit le format ; c'est la relance qui casse, et sur un seul modele

| | `q4` | `q4nogab` | `q4base` | `q4hyb` |
|---|---|---|---|---|
| echecs de la **premiere** tentative | 13, **1,45 %** | 16, **1,79 %** | 24, **2,68 %** | 28, **3,13 %** |
| relances rattrapees | 13 sur 13 | 15 sur 16 | **24 sur 24** | **6 sur 28** |
| rejets **apres** relance | 0 | 1, 0,11 % | **0** | **22, 2,46 %** |

[MESURE, `resultats/r4b-rejets.csv`, `data/traces/r4-resume.json`]

**Le socle a suivi l'invite a trois exemples.** Son taux d'echec de premiere tentative, 2,68
pour cent, tombe dans la bande que `a27` rapporte pour quatre socles a trois exemples, 0,83 a
4,25 pour cent [CONFIRME, `a27`], et sa relance rattrape 24 fois sur 24. Le risque principal
de la nuit, ecrit en toutes lettres dans `r4-oracle-socle.md` section 8, ne s'est pas realise.
**Le taux est publie des deux cotes, comme le critere 1 l'exigeait, y compris la ou il
n'accuse personne.**

**Les 22 rejets sont tous sur `q4hyb`, et ils ont deux causes distinctes.**

1. **L'arithmetique sur les items a beaucoup de modalites.** Les 22 rejets se repartissent en
   K = 5 x2, K = 6 x7, K = 7 x6, K = 8 x1, K = 12 x6 ; **aucun sous K = 5**, K median 7. Les
   items concernes sont `racwork` (6), `income` (6), `spdeg*` (4), `kidssol` (2) et quatre
   autres. Les premieres tentatives echouent le plus souvent sur une somme hors bande, 113,
   110, 78. [MESURE]
2. **La relance ne fonctionne pas en mode completion sur ce modele.** 22 des 28 relances
   echouent, et 18 d'entre elles contiennent le separateur d'exemple : le modele repart dans un
   quatrieme exemple au lieu de repondre, section 2.3.

**La relance est un defaut connu, reconduit exprès, et le mode completion le rend total.** Le
critere 2 de la page de plan retire toute cellule ou la distribution egale l'exemple chiffre de
l'invite de relance. Sous gabarit, `q4` recopiait 11 fois sur 13 (85 pour cent) ; **en
completion, les trois conditions recopient 100 pour cent du temps** : 24 sur 24, 15 sur 15,
6 sur 6. Autrement dit, **en mode completion la relance ne rattrape jamais rien d'utilisable :
elle rend soit l'exemple qu'on lui montre, soit un exemple qu'elle invente.** Le mecanisme de
relance de R1 est donc a refaire avant tout run de completion futur, et la question 6 de R1 a
Simon, « retirer l'exemple chiffre de la relance », devient une necessite et non une
preference. [MESURE, `resultats/r1-controles-r4.csv`]

### 3.2 La sensibilite

**Les 22 rejets ne portent aucune conclusion.** Trois verifications.

1. **Perimetre principal.** En identite journaliste, **aucune des quatre conditions ne perd de
   cellule sur les 79 items orientes** : les contrastes de la section 2 sont calcules sur les
   79 memes items dans les quatre conditions. En identite adverse, `q4hyb` en perd deux, 77 sur
   79, et lui seul. Les rejets portent sur des items a K eleve, `income` a douze modalites,
   `racwork` a sept, `spdeg*` a six, dont **deux seulement sont orientes**, `marhomo` et
   `fehire`, un rejet chacun, tous deux en identite adverse.
2. **Perimetre strictement commun aux quatre conditions.** Recalcul complet : le facteur H2b de
   `q4hyb` reste 0,262, les cinq contrastes bougent au plus de 0,005, aucun verdict ne change.
   Sur H1 camp gauche, le perimetre passe de 142 a 142 items et les contrastes de -0,076 a
   -0,082 et de +0,069 a +0,080, avec p qui reste sous 0,001. [MESURE,
   `resultats/r4b-sensibilite-perimetre.csv`]
3. **Direction du biais residuel.** Les cellules perdues par `q4hyb` sont celles ou le modele
   n'a pas su compter jusqu'a 100 sur 7 a 12 modalites. Si ces cellules avaient ete retenues,
   elles auraient vraisemblablement ete des distributions bruitees, donc plus dispersees et
   plus indifferentes au camp, ce qui **abaisserait encore** le facteur de `q4hyb` et
   **renforcerait** la conclusion de la section 2.3 au lieu de l'affaiblir. [PROBABLE, non
   mesurable sans un run de plus]

---

## 4. Ce que cela change

### 4.1 A la section 12 de `MODELE-DU-MONDE.md`

**Un.** La quantite « ecart entre camps decrit » depend du **format d'invite** au moins autant
que du modele. Le facteur 5,2 entre trois familles de modeles de R1 doit desormais se lire a
cote d'un facteur 3,0 entre deux formats d'invite sur **un seul fichier de poids**, et d'un
facteur 14 entre deux protocoles, description et incarnation, deja mesure en R1 section 2.2.
La quatrieme issue de R1, « la dispersion inter modeles depasse l'erreur de chacun », se
precise : **la dispersion inter protocoles, sur un seul modele, est du meme ordre que la
dispersion inter modeles.** [MESURE]

**Deux, la phrase pour un regulateur, corrigee.** Celle de R1 section 5.2 dit « interroges avec
la meme invite au caractere pres ». Elle reste vraie et elle etait deja prudente ; ce que R4
ajoute est que cette clause n'est pas une precaution de style, c'est la moitie de la mesure.
Version corrigee, a substituer :

> Sur 149 questions d'opinion americaines dont la distribution reelle par camp politique est
> publiee, un meme modele ouvert de quatre milliards de parametres, interroge a temperature
> zero, decrit l'ecart entre les camps politiques comme valant 0,25 fois l'ecart reel ou 0,73
> fois selon la seule facon dont la question lui est presentee, sans qu'un octet de ses poids
> ait change ; le modele socle dont il descend, sous la meme presentation, donne 0,57 ; les
> quatre conditions decrivent toutes les camps comme plus varies qu'ils ne sont, toutes se
> trompent d'environ dix fois le bruit de reinterrogation d'un panel humain, et toutes, le
> socle sans aucun post entrainement compris, changent le portrait qu'elles font d'un camp
> selon l'identite de celui qui pose la question, de deux a cinq fois ce bruit. La quantite est
> mesurable a cout nul, elle varie par modele, par version, par protocole et par format
> d'invite, et elle n'a pas de valeur de reference : l'obligation d'audit doit fixer un
> protocole, un format d'invite et un registre avant de fixer un seuil.

Ce que cette phrase ne dit pas, et qu'il ne faut pas y ajouter : rien sur la croyance humaine
de second ordre, faute des items ANES ; rien sur l'effet sur un lecteur ; rien hors d'un
modele, d'une famille, d'un pays, d'une enquete, d'un ordre de modalites.

**Trois, l'objection de contamination.** Elle **reste entiere**, et R4 ne la touche pas : aucun
des trois modeles n'a de coupure publiee, et un socle a lu le meme internet qu'un instruit.
Ce que R4 ajoute est un fait negatif : **le socle n'est pas plus pres des marginales nationales
publiees que de notre echantillon**, -0,006 [-0,024 ; +0,012] en identite journaliste, et le
seul signe positif jamais mesure, celui de `q4` sous gabarit, disparait quand on change le
format a poids identiques, -0,028 [-0,040 ; -0,016]. **Le signe de restitution que nous avions
n'est pas dans les poids de pre entrainement.** [MESURE]

**Quatre, ce qui tombe et ce qui tient.** Tombe : « le post entrainement fabrique le portrait
des camps », qui n'a jamais ete ecrit comme etabli mais qui portait le mecanisme du programme.
Tient et se renforce : la sur dispersion sur les quatre conditions ; la dependance au
demandeur, desormais sur un socle ; l'erreur a dix fois le plancher ; l'absence de valeur de
reference.

### 4.2 A `MOONSHOTS.md`, programme A

**Le registre des versions doit inclure le format d'invite, et c'est desormais le premier
champ, pas le dernier.** Le bloc E3 ecrit « le registre des versions passe du mois 3 au mois 1 :
la quantite depend plus du modele et du protocole que du pays ou du sujet ». R4 le precise :
elle depend du **format** d'un facteur trois sur un modele unique. Un registre qui liste le
modele, sa version et sa quantification, mais pas la presentation de l'invite, ne permet a deux
auditeurs ni de se contredire ni de se confirmer. Champs minimaux : famille et version exacte
du point de controle, quantification, **gabarit de conversation ou completion**, **nombre et
contenu des exemples**, ordre des modalites, temperature, mode description ou incarnation.

**Le point d'arret du mois 1 n'est pas deplace par R4, il est confirme dans son deuxieme
volet.** Le point d'arret sur les 149 opinions etait « les modeles sont une archive fidele et
d'accord entre eux » ; il etait deja franchi dans l'autre sens ; R4 le franchit une seconde
fois, a l'interieur d'un seul modele. Le livrable du mois 1 reste le tableau d'audit par
modele plus le registre, et **le registre y gagne un champ obligatoire**.

**Ce que R4 ferme.** La ligne « un modele socle, une heure, separe le modele a lu le GSS du
post entrainement fabrique le portrait », inscrite au tableau 5.3 de R1, est faite et rendue :
elle separe bien les deux, et **la reponse est que ni l'un ni l'autre ne porte le portrait**.
Le poste de depense « second socle d'une autre famille » ne se justifie plus par la meme
question ; s'il se lance, c'est pour tester si le facteur trois du format est une propriete de
Qwen ou du champ, ce qui est une question differente et meilleure.

### 4.3 A la these finale

**Rien sur les jumeaux, tout sur l'instrument.** R4 ne touche a aucune des trois phrases de la
section 12.2 : il n'y a ici ni chute sous permutation, ni etiquette, ni imputation, ni gens
rares, ni mode incarnation, et aucune phrase de R4 ne porte sur `a5`, `a37` ni `a38`.

Ce que R4 apporte est un quatrieme etage a la partie instrumentale de la these : **la mesure de
la fidelite de representation des camps n'est pas une propriete du modele, c'est une propriete
du couple modele et instrument, et la part de l'instrument est plus grande que la part des
poids.** C'est un renfort direct de ce que R1 disait deja avec son facteur quatorze entre deux
protocoles, et c'est le meme argument avec une variable de plus, controlee, sur le meme fichier
de poids.

---

## Ce que ce resultat autorise a ecrire, et ce qu'il interdit

**Autorise.**

1. « Sur cette quantite, changer le format d'invite a poids identiques deplace la mesure de
   +0,48 [+0,29 ; +0,68], plus que l'ecart entre le socle et l'instruit, +0,32
   [+0,13 ; +0,52]. » [MESURE]
2. « Le meme fichier de poids donne 0,245 et 0,727 selon la presentation de la question. »
   [MESURE]
3. « Sous le meme format, le socle ecrase l'ecart entre camps davantage que l'instruct-2507,
   -0,16 [-0,34 ; +0,01] sur 79 items et -0,24 [-0,43 ; -0,05] sur 65 : l'alignement rapproche
   des humains sur cette quantite, il n'en eloigne pas. » [MESURE, contraste **non apparie**, a
   dire a chaque fois]
4. « Le successeur apparie du socle, en completion sans gabarit, rend la meme mesure que
   l'instruct sous gabarit, +0,017 [-0,15 ; +0,17], et il reconstruit de lui meme un tour de
   conversation dans 57 a 64 pour cent de ses relances, ce que le socle ne fait jamais. »
   [MESURE pour les deux faits]
5. « Un modele socle, sans post entrainement, change le portrait qu'il fait d'un camp selon
   l'identite du demandeur, jusqu'a 5,0 fois le plancher humain. » [MESURE]
6. « Les quatre conditions decrivent les camps comme plus varies qu'ils ne sont et se trompent
   de neuf a dix fois le plancher de reinterpretation humaine. » [MESURE]
7. « L'attraction vers les marginales nationales publiees n'est pas portee par les poids de pre
   entrainement : elle disparait quand on change le format a poids constants, et le socle n'en
   montre aucune. » [MESURE]

**Interdit.**

1. **« R4 leve l'objection de contamination. »** Interdit par la page de plan section 2, et le
   resultat ne la leve pas. Aucune coupure n'est publiee pour aucun des trois modeles.
2. **« Le socle est plus fidele que l'instruit. »** Faux sur l'erreur globale, 10,5 contre 9,6
   fois le plancher, faux sur la dispersion interne, et vrai seulement sur l'ecart entre camps
   compare a la condition sous gabarit, c'est a dire en confondant format et poids.
3. **« Le post entrainement fabrique le portrait des camps. »** Le contraste apparie va dans
   l'autre sens sur la dispersion, et le contraste non apparie sur l'ecart entre camps aussi.
4. **« Le format explique la moitie de l'ecart. »** C'est le chiffre de `a27` tire de
   2607.25292 ; chez nous il en explique une fois et demie. Citer les deux, jamais l'un pour
   l'autre.
5. **Toute phrase sur le mode incarnation**, sur `a5`, `a37`, `a38`, sur les jumeaux, sur la
   chute sous permutation. R4 est en mode description, comme R1.
6. **« Le modele exagere plus que les humains. »** Aucun second terme humain dans ce run.
7. **« La reconstruction du gabarit cause l'ecrasement chez `q4hyb`. »** Seule la coincidence
   est mesuree, sur une condition ; la causalite demanderait une condition ou l'on empeche la
   reconstruction.
8. **« H4 est confirmee. »** Elle ne l'est sur aucune des six cellules prospectives, et la
   ligne qui la soutenait est declaree a posteriori et ne passe plus Holm en identite
   journaliste dans la famille effectivement appliquee.

---

## Ce que je n'ai pas pu verifier

1. **Que la conversion GGUF du socle soit fidele.** Empreinte du fichier verifiee, procede de
   quantification inconnu, depot tiers `mradermacher`, aucune quantification Q4 du socle ne
   provenant de Qwen ni de unsloth. **Une difference de procede de quantification entre le
   socle et l'instruit se lirait exactement comme une difference de poids**, et c'est la limite
   la plus serieuse de la section 2.2.
2. **L'appariement du contraste principal.** `q4base` contre `q4nogab` est non apparie et le
   restera. `q4hyb` repare le defaut, mais sur le seul contraste `q4base` contre `q4hyb`, qui
   n'est pas celui que H2 et H3 utilisent.
3. **La date de coupure des trois modeles.** Aucune n'est publiee. R4 ne tranche rien par la
   date.
4. **Le sens du signe de H4.** L'echantillon de Stanford n'est pas un echantillon national, et
   tout modele approximativement calibre sur la population americaine sera mecaniquement plus
   proche du national. Ce dispositif ne separe pas cette explication de la restitution.
5. **H4 sur Pew.** Aucune donnee Pew sur la machine, aucun telechargement fait.
6. **L'ordre des modalites.** Une seule passe, ordre de nomenclature, dans les quatre
   conditions. `a27` mesure que l'ordre seul porte 60 pour cent de l'effet de leur correctif.
7. **La generalite du gabarit implicite.** Un seul modele hybride, une seule famille, une seule
   invite. Rien ne dit qu'un autre point de controle hybride ferait de meme.
8. **Le mecanisme de la marche de format.** Nous mesurons qu'elle existe et sa taille ; nous ne
   savons pas si elle vient du texte du gabarit, de l'absence d'exemples dans `q4`, ou des trois
   exemples ajoutes dans `q4nogab`. Une condition « gabarit ChatML **plus** trois exemples »
   separerait les deux, elle n'a pas tourne, et elle coute 894 appels.
9. **Le second terme humain.** Toujours absent.
10. **L'anteriorite de la page de plan.** Aucune page du projet n'est deposee hors de la
    machine ; le commit cite par `r4-preenregistrement.md` ne contient aucun fichier de popsim.
    `bilan-predictions.md` mesure de plus que le tableau H4 precede de six minutes la derniere
    ecriture de la page. Les predictions H1, H2 et H3 ne sont pas concernees par cet ecart, la
    condition socle n'existant pas encore ; H4 l'est.

---

## Questions ouvertes pour Simon

1. **Le contraste `q4nogab` est un controle methodologique, pas une quantite auditable ; faut il
   le mettre en tete du rapport ?** Personne n'interroge un assistant en mode completion a trois
   exemples. Mais c'est cette condition qui donne le chiffre le plus grand du run, +0,48, et
   c'est elle qui condamne toute lecture naive du couple socle contre instruit. La question 3 de
   `r4-oracle-socle.md` la posait avant de connaitre la reponse ; maintenant qu'elle est connue,
   la mettre en tete affaiblit la piece la plus lisible du dossier et renforce la piece la plus
   solide. Que choisit on ?

2. **La condition manquante coute 894 appels : la lance t on ?** « Gabarit ChatML **plus** les
   trois exemples » separerait « ce que le gabarit fait » de « ce que les exemples font ». En
   son absence, tout ce que nous pouvons ecrire est « le format », mot qui recouvre deux choses.
   Une heure de machine, aucun risque, et elle rend le resultat central non attaquable.

3. **Le socle contre le socle : faut il une seconde famille ?** La question qui motivait
   « un second socle si R4 rend le socle fait comme l'instruit » n'a plus lieu d'etre sous cette
   forme. La question nouvelle est : le facteur trois du format est il une propriete de Qwen ou
   du champ ? Un socle Llama ou OLMo y repondrait, et OLMo a l'avantage d'avoir ses quatre
   points de controle publies, ce qui donnerait la dose reponse de la table 4a chez nous.

4. **La relance est a refaire avant tout run de completion.** En mode completion elle recopie
   son exemple 100 pour cent du temps ou repart dans un exemple invente. Faut il un gabarit sans
   nombre, du genre `A: <integer>`, au risque que le modele n'apprenne rien, ou faut il
   supprimer la relance et compter les echecs, ce qui est plus honnete et plus simple ?

5. **H4 merite t elle un dispositif propre, maintenant que son signe est attribue au format ?**
   Le contraste qui trancherait, un item dont la marginale nationale est publiee et dont
   l'echantillon de Stanford s'ecarte beaucoup, oppose a un item ou les deux coincident, reste
   constructible sur les 112 items retenus sans un appel de plus. Priorite ou distraction par
   rapport a l'experience de lecture du mois 6 ?

6. **L'erreur de renvoi de `a3` section 4.4 est toujours dans deux rapports de R1.** Elle dit
   qu'un modele est telecharge alors qu'il ne l'etait pas ; un lecteur qui rejouerait la
   recommandation echouerait. Aucun fichier existant n'a ete modifie par R4. La correction
   demande une decision.

---

## Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim

# l'evaluation, r1_evaluer.py sans une modification de son fichier
.venv/bin/python analyses/r4_oracle_socle.py --evaluer > data/traces/r4-evaluation.log 2>&1
.venv/bin/python analyses/r4_oracle_socle.py --h4 >> data/traces/r4-evaluation.log 2>&1

# les contrastes entre conditions, la part du format, la sensibilite
.venv/bin/python analyses/r4b_contrastes.py

# les rejets, les marqueurs de gabarit, le critere 2 bis, le retrecissement
.venv/bin/python analyses/r4b_diagnostic.py

# la figure
.venv/bin/python analyses/r4b_figure.py
```

Sorties de ce rapport : `resultats/r4b-contraste-h2b.csv`, `r4b-contraste-h1.csv`,
`r4b-part-format.csv`, `r4b-contraste-h4.csv`, `r4b-sensibilite-perimetre.csv`,
`r4b-rejets.csv`, `r4b-marqueurs-gabarit.csv`, `r4b-2bis.csv`, `r4b-indifference.csv`,
`r4b-alpha-uniforme.csv`, `r4b-figure-decomposition.png` et `.svg`.
Sorties de l'evaluateur : `resultats/r1-*-r4.csv`, `r1-resume-r4.md`,
`r1-figure-oracle-r4.png` et `.svg`, `r4-h4-*.csv`.
Traces : `data/traces/r1-{q4,q4base,q4nogab,q4hyb}-r4.jsonl`, `r4-run.log`, `r4-resume.json`,
non versionnees, sans aucune reponse individuelle.
