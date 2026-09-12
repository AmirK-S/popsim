# C7-Argyle, préenregistrement : la réidentification tient-elle sur un **troisième** jeu réel ?

**Écrit le 12 septembre 2026, avant toute mesure d'attaque.** Étude de risque de vie privée
sur un jeu déjà public — Argyle, Busby, Fulda, Gubler, Rytting & Wingate (2023), « Out of
One, Many », Harvard Dataverse `doi:10.7910/DVN/JPV20K`, licence **CC0 1.0** (vérifiée dans
le champ `license` de l'API Dataverse au téléchargement). Aucun identifiant ANES, aucun
appariement individuel n'est imprimé ni écrit ; seuls des taux agrégés sortent dans
`resultats/c7-argyle.csv`. Aucun appel d'API payant, aucun jumeau fabriqué par nous : tout
vient de sorties publiées par l'équipe de Brigham Young University.

---

## 0. Ce qui a été vérifié à la source, avant tout le reste

### 0.1 L'appariement, par lecture directe des fichiers

`data/argyle-2023/anesgpt3_task3.csv` : **4 270 lignes, 27 colonnes, 12 items appariés**.

| item | colonne **réelle** (ANES 2016) | colonne **jumelle** (GPT-3) |
|---|---|---|
| gender | `V161342` | `gender_gpt3` |
| race | `V161310x` | `race_gpt3` |
| age | `V161267` | `age_gpt3` |
| education | `V161270` | `education_gpt3` |
| church_goer | `V161244` | `church_goer_gpt3` |
| patriotism | `V162125x` | `patriotism_gpt3` |
| discuss_politics | `V162174` | `discuss_politics_gpt3` |
| political_interest | `V162256` | `political_interest_gpt3` |
| ideology | `V161126` | `ideology_gpt3` |
| pid7 | `V161158x` | `pid7_gpt3` |
| voted_2016 | `V162031x` | `voted_2016_gpt3` |
| votechoice_2016 | `V162062x` | `votechoice_2016_gpt3` |

`V160001_orig` est l'identifiant de cas de l'ANES 2016 ; il est **unique sur les 4 270
lignes** (vérifié). Les colonnes réelles et jumelles sont sur la **même ligne**, donc la
**même personne** : l'appariement est individuel, ligne à ligne, sans jointure à
reconstruire. Les deux fichiers de robustesse en température (`anesgpt3_task3_temp001.csv`,
`anesgpt3_task3_temp10.csv`) portent la **même suite de `V160001_orig`, dans le même
ordre** (vérifié par comparaison exacte des vecteurs) : ce sont trois jumeaux GPT-3
indépendants des **mêmes** personnes.

La colonne `V161155` (pid3) est présente mais n'a **pas** de colonne jumelle : elle ne sert,
dans le code des auteurs, qu'à construire la question de relance sur `pid7`. Elle est donc
exclue des 12 items.

### 0.2 Le crosswalk, vérifié dans le code de génération publié

`GPT3_OtherModels_DataGenerationCode.pdf`, section 1.10 (« Study 3 »), dictionnaire
`questions` : pour chaque variable, les **clés** du champ `vals` sont les codes ANES, et
c'est cette clé qui est écrite dans la colonne `_gpt3` (`coded_response = valnum`). Les deux
côtés sont donc déjà sur la même échelle, à deux exceptions près que je recode explicitement :

- **education** : `vals` est plusieurs-vers-un (`"high school"` pour `V161270` 1→9,
  `"some college"` pour 10→12, `"a four-year college degree"` pour 13, `"an advanced
  degree"` pour 14→16) et `strcompare` retient le **dernier** code correspondant — d'où les
  seules valeurs 9, 12, 13, 16 réellement observées côté GPT-3. Les deux côtés sont ramenés
  aux **4 bandes** des auteurs (identiques à celles de leur `Study3Analysis.R`).
- **votechoice_2016** : ANES 3/4/5 = « someone else », codé 42 côté GPT-3. Les deux côtés
  sont ramenés à {Clinton, Trump, quelqu'un d'autre}.

### 0.3 Le confondu majeur, à déclarer d'emblée : ce jumeau est un **oracle laisse-un-dehors**

C'est la différence la plus importante avec nos deux jeux, et elle n'était pas connue avant
lecture du code. `build_interview(s, human_readable_omit=X)` construit, pour chaque item X,
un entretien contenant les **onze vraies réponses de la personne** aux autres items, puis
demande à GPT-3 (`davinci`, `max_tokens=5`) de produire la douzième. Chaque colonne `_gpt3`
est donc une prédiction **réellement tenue à l'écart** de sa propre cible — il n'y a aucune
tautologie, aucun écho de l'entrée — mais elle est conditionnée sur onze réponses vraies,
là où nos jumeaux Twin et Park sont conditionnés sur un persona.

Conséquence assumée : **ce n'est pas le même canal que le nôtre.** Un jumeau qui a lu onze
vraies réponses doit mécaniquement être plus fidèle par item qu'un jumeau persona. La
comparaison à nos deux jeux est donc biaisée **vers le haut**, et la prédiction ci-dessous
en tient compte explicitement (§3).

### 0.4 Les trois vagues demandées n'existent pas dans ce format — dit précisément

La mission demande de traiter 2012, 2016 et 2020 séparément. **Ce n'est pas possible, et
voici pourquoi, fichier par fichier.**

- Le seul fichier à items multiples appariés, `anesgpt3_task3.csv` (étude 3), est
  **exclusivement ANES 2016** : toutes ses colonnes sont des codes `V16xxxx`, et son
  identifiant `V160001_orig` est l'identifiant de cas 2016.
- Les trois fichiers de vagues, `full_results_2012_2.tab` / `_2016_` / `_2020_` (étude 2),
  contiennent bien 2012 / 2016 / 2020 (5 914 / 4 270 / 5 441 lignes), mais la **seule**
  sortie GPT-3 qu'ils portent est une paire de probabilités de vote (`p_romney`/`p_obama`,
  `p_trump`/`p_clinton`, `p_trump`/`p_biden`). Toutes leurs autres colonnes sont les
  **entrées** ANES ayant servi à construire la mise en récit, pas des sorties de modèle.
  **Un seul item par personne : une attaque de réidentification n'y est pas définissable.**

**Réplication interne de substitution, déclarée ici avant tout calcul** : les trois versions
de jumeaux GPT-3 des **mêmes** 2016 (température principale, 0,01 et 1,0) sont traitées
séparément, exactement comme on aurait traité trois vagues. Elles offrent une variation de
décodage, pas d'époque. Je ne présenterai jamais cela comme la réplication à trois vagues
demandée.

---

## 1. Entrées de la prédiction (calculées sur les **réponses humaines seules**)

Aucune colonne `_gpt3` n'est lue pour ces quantités ; elles sont des **entrées** du modèle,
pas des résultats. Produites par `analyses/c7_argyle.py preparation`.

- **Bassin** : 2 148 personnes valides sur les 12 items (sur 4 270). La restriction aux cas
  complets est le garde-fou déjà en vigueur dans `c7_reidentification.items_communs` : sur
  ce sous-ensemble, aucun motif de manquants ne peut servir d'empreinte.
  **N = 2 148 est à 4 % de l'ancre Twin (N = 2 058)** : aucune extrapolation en taille de
  bassin n'est nécessaire.
- **Items** : 12. **V de Cramér moyen = 0,1620** (55 paires), donc
  **items effectifs = 12 / (1 + 11 × 0,1620) = 4,31** (formule H2 de
  `c7-anomalie-park-2026-09-12.md`, reprise telle quelle).
  Pour mémoire : Twin 60 items → 10,13 effectifs ; Park/Stanford 177 → 9,05.
  **Argyle porte 43 % de l'information effective de Twin.**
- **Entropie humaine totale** : 21,30 bits (dont 6,05 pour le seul âge). Plafond
  d'identification : log2(2 148) = 11,07 bits.

---

## 2. Ce que notre modèle prédit, et d'où ça vient

Notre dépôt a déjà établi (`c7-bits-resultats.md` §2 et §3) que **le taux top-1 ne se
transporte pas** entre jeux (facteur 3,2 entre Twin et Stanford) alors que **les bits
normalisés, oui** (facteur 1,34). La prédiction principale est donc en bits ; la prédiction
en top-1 est dérivée de nos deux **courbes mesurées**, et elle est plus large, à dessein.

### 2.1 Prédiction en top-1 — dérivation

Deux axes mesurés, composés :

**Axe items** — la seule courbe top-1 vs nombre d'items que nous ayons mesurée est
`c7-stanford-courbe-items.csv` (condition composite, N = 1 052) :
k = 10 → 5,24 % ; 20 → 11,73 % ; 40 → 22,10 % ; 60 → 34,03 % ; 177 → 65,50 %.
Convertie en items effectifs avec le V̄ de Stanford (0,1055) : n_eff = 5,13 ; 6,66 ; 7,82 ;
8,31 ; 9,05. Pente log-log entre les deux premiers points : **3,08**.
À n_eff = 4,31 (Argyle) : 5,24 % × (4,31/5,13)^3,08 = **3,07 % à N = 1 052**.

**Axe bassin** — la courbe mesurée de `c7-echelle.csv` (Twin, 60 items, N = 50 → 2 058)
s'ajuste en loi puissance d'exposant **−0,253**. Passage de N = 1 052 à N = 2 148 :
facteur (2 148/1 052)^−0,253 = **0,834**. → **2,56 %**.

**Seconde ancre** — à nombre d'items égalisé (k = 60), Stanford vaut **1,6 fois** Twin
(`c7-stanford-resultats.md` §4). Ancré sur Twin plutôt que Stanford : 2,56 / 1,6 = **1,60 %**.

**Prédiction préenregistrée, bassin complet N = 2 148, meilleur des trois jumeaux GPT-3 :
top-1 = 2,5 %, intervalle [1,0 % ; 6,0 %].** L'intervalle est plus large que l'écart des
deux ancres (1,60–2,56) pour deux raisons déclarées : n_eff = 4,31 est **en dessous** du
plus petit point de la courbe d'items mesurée (5,13), donc extrapolé ; et nos deux ancres se
contredisent déjà d'un facteur 1,6 à items égaux.

**Même prédiction au bassin d'ancre N = 1 052** (calculé aussi, pour comparer à Stanford
sans aucune correction de taille) : **3,1 %, intervalle [1,2 % ; 7,2 %]**.

Pour situer la chute annoncée : notre jeu de référence donne **20,7 %** à 60 items. La
prédiction est donc une chute d'un **facteur ≈ 8**, et c'est elle qui est mise à l'épreuve,
pas le niveau absolu.

### 2.2 Prédiction en bits — le test le plus exigeant

`c7-bits-resultats.md` §2 (P2) : bits normalisés par l'entropie humaine = **0,0439** (Twin,
meilleur jumeau) et **0,0327** (Stanford, meilleur jumeau).
**Prédiction : bits normalisés du meilleur jumeau GPT-3 d'Argyle dans [0,020 ; 0,070]**,
soit **0,43 à 1,49 bits** d'identité absolus sur une entropie de 21,30 bits.
C'est le test qui porte la revendication réelle du dépôt (« la mesure voyage, le taux non »).

### 2.3 Ce que j'attends du contrôle d'interprétabilité

- **B-demo** (imputeur statistique conditionné sur les seules démographies) : j'attends que
  les trois jumeaux GPT-3 le **dépassent nettement**, IC disjoints, et donc **passent** le
  contrôle. Motif : ils disposent de onze vraies réponses, B-demo de quatre démographies.
  Un échec ici serait un résultat fort — il signifierait que même un jumeau nourri de onze
  vraies réponses ne porte pas d'information individuelle démontrable.
- **B-oracle** (imputeur statistique conditionné sur **les mêmes onze vraies réponses**) :
  j'attends que GPT-3 soit **au niveau ou en dessous**. Un plus proche voisin à onze
  réponses vraies est un attaquant très fort ; c'est le comparateur apparié au confondu de
  §0.3, et le seul qui dise si GPT-3 apporte quoi que ce soit. **Ceci n'est pas le
  contrôle** (le contrôle reste B-demo, règle du dépôt) mais il est préenregistré ici pour
  ne pas pouvoir être ajouté après coup.
- Piège n°2 de la nuit, évité par construction : **B-demo n'est jamais une constante reprise
  d'ailleurs.** `controle_avant_interpretation` dans `analyses/c7_argyle.py` n'accepte
  **aucun** argument de baseline ; il reçoit le bassin et recalcule la baseline sur ces
  lignes-là. Le bassin d'ancre N = 1 052 recalcule ses baselines à chacun des 20 tirages.
- Ni B-demo ni B-oracle ne reçoivent jamais la vraie valeur d'un item sur lequel ils sont
  notés : l'item cible est retiré du contexte (`_imputer_loo`), exactement comme GPT-3 ne
  voyait jamais la réponse qu'on lui demandait. Aucune tautologie des deux côtés.

---

## 3. Règle de décision, arrêtée avant de regarder

1. **Contrôle d'abord.** Si aucun des trois jumeaux GPT-3 ne dépasse B-demo avec des IC
   bootstrap 95 % **disjoints** sur le bassin réellement attaqué, **l'analyse s'arrête là** et
   le rapport conclut à une limite des jumeaux de première génération. Aucune interprétation
   du reste. `EchecControleInterpretabilite` n'est jamais attrapée pour continuer.
2. **Si le contrôle passe**, verdict sur le top-1 du meilleur jumeau, bassin complet :
   - dans **[1,0 % ; 6,0 %]** → **réplication réussie** : notre loi prédit correctement la
     chute sur un troisième jeu.
   - **hors intervalle** → **réplication échouée en taux** : notre loi ne prédit pas la
     chute. C'est rapporté comme tel, sans réajustement d'aucun paramètre.
3. **Verdict en bits** (indépendant du 2) : bits normalisés dans **[0,020 ; 0,070]** →
   la revendication de transportabilité (P2) tient sur un troisième jeu ; hors intervalle →
   elle ne tient pas.
4. **Si le format ne permet pas la mesure**, c'est dit précisément, jamais bricolé.

## 4. Ce qui réfuterait notre modèle

- **Réfutation du taux** : top-1 observé **< 1,0 %** ou **> 6,0 %** au bassin complet. Un
  top-1 sous 1 % dirait que nous **surestimons** la fuite quand les items effectifs sont peu
  nombreux ; au-dessus de 6 %, que nous la **sous-estimons**. Les deux comptent.
- **Réfutation de la mesure transportable, la plus grave** : bits normalisés hors
  [0,020 ; 0,070]. Cela invaliderait la conclusion P2 de `c7-bits-resultats.md`, c'est-à-dire
  la seule chose que notre article prétend faire voyager entre jeux.
- **Réfutation du mécanisme** : si le top-1 de **B-oracle** dépasse celui du meilleur jumeau
  GPT-3 avec IC disjoints, alors sur ce jeu le « jumeau LLM » n'ajoute rien à un plus proche
  voisin classique disposant de la même information — ce qui contredirait le cadre de
  `c7-bits-resultats.md` §2 (les jumeaux LLM fuient 4 à 7 fois plus par point d'exactitude
  que les prédicteurs statistiques).
- **Direction attendue du confondu §0.3**, déclarée pour ne pas servir d'échappatoire : le
  conditionnement sur onze vraies réponses pousse le top-1 d'Argyle **vers le haut**. Un
  dépassement de la borne haute est donc l'échec le **moins** informatif sur notre loi et le
  **plus** informatif sur le confondu ; un passage sous la borne basse, lui, est une
  réfutation nette et sans excuse disponible.

## 5. Mesure

`analyses/c7_argyle.py mesure`, graine **20260912**, `.venv/bin/python`, aucun appel réseau.
Fonctions reprises sans réimplémentation : `c7_reidentification.rangs_attaque`,
`.resume_taux`, `.graine_nom`, `.N_BOOTSTRAP` ; `a2_commun.distance_hamming`,
`.bootstrap_personnes` ; `c7_bits.rangs_tous_tirages`, `.bits_et_ic`, `.entropie_item`.
Mesures : top-1, top-10, rang médian, IC 95 % bootstrap **sur les personnes** (2 000
tirages), bits d'identité. Deux bassins : complet (N = 2 148) et ancre (N = 1 052,
20 tirages sans remise, baselines recalculées à chaque tirage). Sortie unique :
`resultats/c7-argyle.csv`.
