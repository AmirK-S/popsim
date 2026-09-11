# tab. Préenregistrement : le tournoi A vers B sur Twin-2K-500

**Statut : version candidate, validation du responsable et dépôt OSF en attente.**

Brouillon écrit le 11 septembre 2026 vers 13 h 20 CEST. Arbitrages de l'orchestrateur appliqués le même jour, avant tout calcul de résultat (section 14).

Dépôt git au moment de l'écriture : `e29a53683fcf36791c3ef319112c537b4c36df3f`, arbre de travail non propre, fichiers `tab` non versionnés. **Aucun script d'évaluation n'existe au moment de l'écriture. Aucune exactitude, perte, chute, corrélation ni comparaison de configurations n'a été calculée pour `tab`.**

Tant que cette page n'est pas déposée sur OSF, elle se décrit comme un « plan écrit avant calcul, horodaté sur machine, non déposé », selon la convention de `r2b-preenregistrement.md`. Au dépôt OSF, on reporte ici l'horodatage et l'adresse, sans rien changer d'autre. Toute modification ultérieure est un écart déclaré dans le rapport.

Documents de départ : `resultats/prochaine-validation-externe-2026-09-11.md`, option 1, appelé ci-dessous « document 1 », et `resultats/twin-ab-audit-provenance-2026-09-11.md`, appelé « l'audit ». Là où l'audit invalide une hypothèse du document 1, c'est l'audit qui fait foi. Chaque arbitrage est justifié à l'endroit où il s'applique.

---

## 0. Ce qui a été lu ou vu avant d'écrire, et ce qui ne l'a pas été

1. **Documents** : le document 1, l'audit, `t1-preenregistrement.md`, `r2b-preenregistrement.md`, le code de `analyses/t1_commun.py`, `t1_baselines.py`, `t1_mesures.py` (fonctions `chute` et Q6), `i3b_twin.charger_twin_commun`, `a6.charger_twin`, `a44_commun.permuter_intra` et `a44_mesures.exactitude_codes`.
2. **Métadonnées d'items** : `question_catalog.json` et `wave4_formatted_to_catalog_mapping.json`, soit le type, le sélecteur, le bloc, les lignes, les options et les libellés.
3. **Comptes de structure** : ceux de l'audit (masques, périmètres, cellules `S_gra`) et ceux de la section 4.3, calculés sur le seul statut vide ou renseigné des cellules.
4. **Résultats antérieurs déjà publiés.** `t1` publie, sur les 108 items entiers, l'exactitude, la chute et les résidus des treize configurations. Le document 1 cite `t1-correlation-residus.csv`. L'audit cite trois exactitudes de `t1` et celle du retest humain, que le rédacteur de cette page a donc lues. Le rédacteur n'a ouvert aucun CSV de résultats de `t1`, sauf la ligne d'en-tête de `t1-correlation-residus.csv`. Le projet, lui, connaît ces valeurs : voir la limite L1.

---

## 1. Question et estimand

**Question.** Le diagnostic de correspondance à la personne, calculé sur un bloc d'items A, choisit-il une configuration dont la perte humaine sur un bloc B tenu à l'écart est plus faible que celle de la configuration choisie par l'exactitude sur A ?

**Estimand, repris du document 1.** Pour la rotation r (r = 1, 2, 3), B_r est le bloc r de la partition et A_r le complément.

`Delta_r = perte_B_r(c_diag_r) − perte_B_r(c_exa_r)`, et `Delta = (Delta_1 + Delta_2 + Delta_3) / 3`.

Un `Delta` négatif est favorable au diagnostic. **Si les deux règles choisissent la même configuration dans une rotation, `Delta_r` vaut exactement zéro.** Ce n'est pas une valeur manquante, et elle entre telle quelle dans la moyenne.

---

## 2. Configurations

| rôle | configurations (ordre de `llm_specs/index.json`) | personnes |
|---|---|---|
| **tournoi principal, 7** | `Demographics Only - GPT4.1-mini`, `JSON Persona - GPT4.1`, `Text Persona (Default Temperature) - GPT4.1-mini`, `Text Persona (Reasoning) - GPT4.1-mini`, `Text Persona (Repeating Questions) - GPT4.1-mini`, `Text Persona - GPT4.1-mini`, `Text Persona - Gemini-Flash2.5` | 2 058, pid 1 à 2 058 |
| **sensibilité S1, 8** | les 7, plus `JSON Persona - GPT4.1-mini` | 1 000, pid 1 à 1 000 |
| description seule | `Persona Summary - GPT4.1-mini`, `Persona Summary - JSON Persona - GPT4.1-mini` | 2 058 |
| exclues | les deux `JSON Persona (Predicted Output)`, `LLM Finetuning (500 training samples)` | |

**Justification.**
- **Le principal porte sur 7 configurations et non sur 8.** Les 8 admissibles de l'audit (§2.4) ne se recouvrent que sur 1 000 personnes, parce que `JSON Persona mini` s'arrête au pid 1 000. Le retirer rend au tournoi les 2 058 personnes et un masque qui ne perd aucune cellule humaine (audit §3.2). Les 8 restent examinées en S1.
- **Exclusions.** Les deux `Predicted Output` échouent au contrôle de masque (écart E4 de `i3b`), et le contenu passé comme « sortie prédite » est inconnu. `Finetuning 500` a des poids ajustés sur des réponses humaines dont ni la vague ni les items ne sont documentés (audit §2.4).
- **Les deux `Persona Summary` sont suspectes** de fuite de vague 4. Le seul `persona_summary` documenté est dans `full_persona`, qui contient les réponses de vague 4 aux questions répétées. Elles ne participent à aucune régression, aucun choix ni aucune règle de chute. Elles sont décrites en S7, et c'est tout.
- **Pas de sous-tournoi démographique.** Parmi les admissibles, une seule configuration ne reçoit que des démographies. Le tournoi principal mélange donc des ensembles d'information différents : voir L7 et S2.
- **Départage.** Si deux configurations sont exactement à égalité sur le critère d'une règle, on retient la première dans l'ordre de `llm_specs/index.json`.

---

## 3. Données, périmètres, masque d'analyse

- **Chargement** : `t1_commun.charger`, importé sans modification. Nomenclature commune de `i3b`, 108 colonnes MC et Matrix de la vague 4. Vérité : `humains vague 4`.
- **Masque d'analyse d'un périmètre** : cellules où l'humain de vague 4 répond **et** où toutes les configurations candidates du tournoi répondent. Toutes les quantités d'un tournoi (exactitude A, chute A, perte B), adversaires compris, sont calculées sur ce seul masque. Une prédiction absente sur ce masque compte comme fausse (perte 1). Par construction, c'est impossible pour les candidates.
- **Périmètres** : 2 058 personnes pour le principal et pour S2 à S8, 1 000 pour S1. Règle de `t1` (§3) : **aucune valeur absolue n'est comparée d'un périmètre à l'autre.**

---

## 4. La partition

### 4.1 Règles, appliquées par `analyses/tab_partition.py`

Le script ne lit que le catalogue et le mapping, jamais une réponse. Recherche exhaustive, critères pris dans cet ordre :

1. **Groupement, contrainte dure.** Une unité indivisible est l'un des cas suivants :
   - une expérience inter-sujets entière, tous ses bras ensemble (11 expériences, table de l'audit §3.1) ;
   - un QID matrice entier ;
   - un lien de contenu ;
   - à défaut, un QID à choix multiple seul.

   Cela donne 55 unités. **Ajout à la règle de groupement, retenu par arbitrage du 11 septembre 2026 comme le choix conservateur** : `QID288` et `QID289` notent les quatre mêmes objets (vélos, boissons alcoolisées, usines chimiques, pesticides), en bénéfice puis en risque. Les séparer entre A et B ferait passer du contenu de l'un à l'autre, ce que la règle de groupement veut empêcher. Ils forment donc une seule unité. Le script vérifie au catalogue que leurs lignes sont identiques, et **échoue si deux QID des 108 ont des lignes identiques sans partager une unité**.
2. **Tailles** aussi égales que possible.
3. **Type** : lignes de matrice par bloc.
4. **Famille d'analyse** : les 11 expériences, *False consensus*, *Non-experimental heuristics and biases* et *Pricing*, soit 14 familles. Seules les familles portées par plusieurs unités peuvent être réparties, à savoir *Pricing* et *Non-experimental heuristics and biases*. Pour les autres, l'écart est le même quelle que soit la partition. Les 33 `BlockName` du catalogue ne servent pas de familles d'analyse : 26 n'ont qu'un item, et les bras d'une même expérience portent des `BlockName` différents.
5. **Plan** : items inter-sujets par bloc. Ce critère n'est pas dans l'arbitrage. Il n'intervient qu'à égalité des critères précédents et sert la couverture des blocs.
6. **Nombre d'unités par bloc**, parce que le bootstrap rééchantillonne des unités (section 7).
7. **Égalités restantes** : graine `20260911`. **Aucune autre graine n'a été essayée.**

Chaque critère est une somme d'écarts quadratiques à l'allocation proportionnelle. Les unités sont rangées en 9 classes interchangeables, et **135 576 504 répartitions d'effectifs** sont examinées. L'optimum lexicographique est **unique à l'ordre des blocs près**. La graine ne fait donc que tirer quels membres d'une classe interchangeable vont dans quel bloc : quelles expériences à deux bras, quels items de prix, et lequel de `QID291` ou `QID196`.

### 4.2 Résultat

| | |
|---|---|
| fichier | `resultats/tab-partition-items.csv`, 108 lignes, colonnes `item`, `colonne_catalogue`, `qid_parent`, `type`, `selecteur`, `n_modalites`, `famille`, `famille_analyse`, `experience`, `bras`, `plan`, `unite`, `bloc_B` |
| **SHA-256 de la partition** | **`07b3de89cdce44c9644b54fa88f09c429f9874cc2342d7c23f36a1500b183b05`** |
| SHA-256 du catalogue | `e72e305f0c7c83bb990e97de4c0cf2c718ead18cc197239b7feeb354c9ac1bef` |
| SHA-256 du mapping | `345f7f6645f80dc23bcb423a9bb7c5ae77dbbd17fe572472fdfeb252bdcfc2c7` |
| vecteur de critères optimal | (0, 168, 300, 378, 114) |
| tests | `analyses/test_tab_partition.py`, 13 tests : déterminisme sur deux processus, SHA égal à celui-ci, 108 items, groupement, disjonction, échecs propres, exclusivité des bras sur le masque |

| bloc B | items | lignes de matrice | MC | inter-sujets | unités | familles | composition |
|---|---|---|---|---|---|---|---|
| **B1** | **36** | 10 | 26 | 12 | 21 | 9 | *False consensus* (`QID287`, 10), 6 expériences à deux bras (*Absolute vs. relative*, *Allais*, *Anchoring redwood*, *Disease*, *Myside*, *Outcome bias*), `QID291`, 13 prix |
| **B2** | **36** | 14 | 22 | 15 | 16 | 4 | *Linda* (6), *Less is More + Proportion dominance* (9), `QID288` + `QID289` (8), 13 prix |
| **B3** | **36** | 16 | 20 | 21 | 18 | 5 | *Probability matching* (16), *WTA/WTP Thaler* (3), *Anchoring African* (2), `QID196`, 14 prix |

La répartition des lignes de matrice, 10 / 14 / 16, est l'optimum sous groupement. La borne de 13 à 14 lignes par bloc est inatteignable, parce que *Probability matching* forme à lui seul une unité de 16 lignes (audit §3.3). Pour chaque rotation, A_r compte 72 items.

### 4.3 Comptes de structure sur cette partition

Ces comptes portent sur le statut vide ou renseigné, sur le masque d'analyse. Ils sont calculés avec `i3b_twin.charger_twin_commun` et le seul test `code >= 0`, par un script jetable hors dépôt. Le script d'évaluation les recalculera comme contrôles bloquants (section 8).

| périmètre | rotation | rôle | cellules humaines | cellules du masque | part gardée | couverture minimale d'un item | cellules minimales d'une personne | personnes à moins de 10 cellules |
|---|---|---|---|---|---|---|---|---|
| 7 config., 2 058 | 1 | B | 61 740 | 61 740 | 1,0000 | 1 003 (0,487) | 30 | 0 |
| | 1 | A | 107 028 | 107 028 | 1,0000 | 651 (0,316) | 50 | 0 |
| | 2 | B | 55 566 | 55 566 | 1,0000 | 651 (0,316) | 27 | 0 |
| | 2 | A | 113 202 | 113 202 | 1,0000 | 673 (0,327) | 53 | 0 |
| | 3 | B | 51 462 | 51 462 | 1,0000 | 673 (0,327) | 23 | 0 |
| | 3 | A | 117 306 | 117 306 | 1,0000 | 651 (0,316) | 57 | 0 |
| 8 config., 1 000 | 1 | B | 30 000 | 29 955 | 0,9985 | 465 (0,465) | 16 | 0 |
| | 1 | A | 52 032 | 51 924 | 0,9979 | 311 (0,311) | 23 | 0 |
| | 2 | B | 27 000 | 26 932 | 0,9975 | 311 (0,311) | 14 | 0 |
| | 2 | A | 55 032 | 54 947 | 0,9985 | 319 (0,319) | 26 | 0 |
| | 3 | B | 25 032 | 24 992 | 0,9984 | 319 (0,319) | 9 | 1 |
| | 3 | A | 57 000 | 56 887 | 0,9980 | 311 (0,311) | 30 | 0 |

Ajouter les deux `Persona Summary` au masque des 7 ne change aucune de ces valeurs.

---

## 5. Quantités

- **Q1. Exactitude A**, `exa_A(c)`. Convention Q1 de `t1` : `a44_mesures.exactitude_codes`, importée sans modification, restreinte aux colonnes de A_r et au masque d'analyse. On calcule une exactitude par personne, puis la moyenne sur les personnes qui ont au moins une cellule dans A_r.
- **Q2. Chute A**, `chute_A(c)`. Définition de `t1_mesures.chute` : exactitude vraie moins moyenne des exactitudes permutées, avec **P = 200** permutations `a44_commun.permuter_intra` à l'intérieur de **`S_gra`** (genre × ethnicité × âge, `t1_commun.segmentations`). La chute est absolue, pas relative ni rapportée au plancher humain.
- **Q3. Résidu**, `res_A(c)`. Régression linéaire, `np.polyfit` de degré 1 comme dans `t1` Q6, de `chute_A` sur `exa_A` à travers les configurations candidates du tournoi et elles seules : 7 au principal, 8 en S1, 6 en S2. Aucun adversaire statistique n'entre dans la régression. Le résidu vaut `chute_A − valeur ajustée`.
- **Choix par diagnostic** : `c_diag = argmax res_A`, la configuration qui porte le plus de personne compte tenu de son exactitude.
- **Choix par exactitude** : `c_exa = argmax exa_A`.
- **Q4. Perte B**, `perte_B(c)`. Pour chaque cellule du masque dans B_r :
  - ligne de matrice : `|v(ŷ) − v(y)|`, où `v` est la valeur ordinale de `t1` (`paq["val_ord"]`, rang divisé par K − 1) ;
  - item MC : `1[ŷ ≠ y]`, parce que la règle de `t1` et `a6` ne donne un ordre qu'aux lignes de matrice ;
  - prédiction absente : 1.

  On calcule une moyenne par personne sur ses cellules de B_r, puis la moyenne sur les personnes qui ont au moins une cellule. La perte est dans [0, 1]. Pour les items binaires (65 sur 108 : 49 MC et les 16 lignes de *Probability matching*), les deux distances coïncident.

**Graines** : partition `20260911`, permutations de l'estimation ponctuelle `20260911 + 10`, bootstrap `20260911 + 20`. Les adversaires gardent la graine de `t1`, `20260909`.

---

## 6. Adversaires

`B0 mode`, `B0 tirage`, `B1 argmax`, `B2 argmax` et `PMM k=10` sont produits par `t1_baselines.calculer`, **sans modification** : 5 plis de personnes, graine `20260909`, calcul unique sur les 2 058 personnes, puis restriction au périmètre et au masque.

**Ce que voient les adversaires, déclaré.** Pour prédire une personne, ils sont ajustés item par item sur les réponses de vague 4 des personnes des quatre autres plis, **y compris sur les items de B**. Leurs entrées sont les 14 démographies, les 494 items de contexte non répétés des vagues 1 à 3, ou les deux (audit §4, point 4).

**L'unité tenue à l'écart est la personne pour les adversaires, et le bloc d'items pour la sélection.** C'est cohérent avec l'estimand pour une raison précise : l'estimand porte sur le choix *entre configurations*, et aucun adversaire n'entre dans ce choix. Les adversaires servent de témoin de chute (section 8), de bornes, et de contrôle PMM dans la règle de chute (section 9, R4). Le contrôle R4 pose alors la question pratique suivante : la configuration retenue sans jamais voir B bat-elle une imputation tabulaire ajustée sur un échantillon de référence de réponses de vague 4 d'autres personnes ?

**Comparaison principale et asymétrie d'information, par arbitrage du 11 septembre 2026.** La comparaison principale, celle qui porte la revendication, est `c_diag` contre `c_exa` : deux configurations de modèle de langage choisies parmi les mêmes candidates, notées sur le même B_r, **à information égale**. Aucun adversaire n'y entre. Les adversaires de `t1`, ajustés sur les réponses de vague 4 d'autres personnes, sont rapportés avec leur **asymétrie d'information nommée** : ils connaissent la distribution des réponses de vague 4 aux items de B dans la population d'entraînement, alors que les configurations ne la connaissent pas, sauf mémorisation (L12). Le contrôle R4 emploie cette version. C'est donc un contrôle sévère contre le diagnostic, pas une comparaison à information égale, et le rapport l'écrit à chaque endroit où R4 apparaît.

**Variante la plus stricte, S6.** On garde le même code et les mêmes plis, mais la cible `humains vague 4` est remplacée par `humains vagues 1-3 (retest)` : les adversaires apprennent sur les réponses **antérieures** des autres personnes aux mêmes questions, et plus aucune réponse de vague 4 de qui que ce soit n'est vue. La mise en œuvre passe par une copie de `paq` dont `codes[REF]` est remplacé, sans toucher à `t1_baselines.py`. Aller plus loin est impossible : un adversaire qui ne voit aucune réponse à un item de B n'a pas de cible pour le prédire. **S6 est une analyse secondaire déclarée** (section 10). Elle ne change pas la règle de chute.

---

## 7. Inférence

- **Bootstrap conjoint personnes × unités, B = 1 000 réplicats**, qui refait toute la sélection. Chaque réplicat tire trois choses, appliquées à toutes les configurations, à tous les adversaires et aux trois rotations :
  1. les personnes du périmètre, avec remise ;
  2. dans chaque bloc séparément, autant d'**unités indivisibles** que le bloc en contient, avec remise. On tire des unités et non des items : les lignes d'une matrice et les bras d'une expérience ne sont pas indépendants ;
  3. A_r, formé des unités tirées dans les deux autres blocs.

  On recalcule ensuite `exa_A`, `chute_A` (P = 20 permutations par réplicat), la régression, les deux choix, `perte_B`, `Delta_r` et `Delta`. Les multiplicités d'unités deviennent des poids de colonnes, et les multiplicités de personnes des poids de lignes.
- **Doublons et permutation.** `t1` §7 interdit le tirage avec remise pour la chute : un doublon peut recevoir ses propres réponses sous permutation. Dans chaque réplicat, la permutation porte donc sur les **identités distinctes** tirées dans chaque cellule `S_gra`, et chaque copie garde le poids de sa multiplicité. Une identité ne se voit réattribuer ses propres réponses qu'avec la probabilité qu'elle aurait dans l'échantillon d'origine.
- **Intervalle** : percentiles 2,5 et 97,5 des 1 000 valeurs de `Delta`. Pour chaque rotation, on publie aussi la part des réplicats où `c_diag = c_exa`.
- **Coût** : si, après 20 réplicats, la durée projetée dépasse 6 heures sur 4 cœurs, B passe à 500, et ce passage est déclaré. P n'est pas modifié. Aucun autre allègement n'est permis.
- Aucune valeur p, aucune correction de multiplicité : la décision est la règle de la section 9.

### 7.1 Précisions avant dépôt (2026-09-11)

`analyses/tab_evaluer.py` est écrit, et ses tests (`analyses/test_tab_evaluer.py`, 12/12) passent sur données entièrement synthétiques (`GO-TAB` absent, aucune lecture de Twin). L'écriture du code a mis au jour deux points que le texte ci-dessus laissait ouverts. Ils sont tranchés ici, avant tout calcul, en décrivant exactement ce que fait le code déjà écrit.

1. **Bootstrap conjoint (section 7).** Le tirage avec remise porte séparément sur les personnes du périmètre et, dans chaque bloc, sur ses unités indivisibles. Les multiplicités ne changent jamais le masque d'analyse lui-même : celui-ci reste celui calculé une fois sur le périmètre complet (section 3). Ce sont des **poids** qui portent le tirage — un poids de ligne par personne (son nombre d'occurrences dans le tirage avec remise), un poids de colonne par item (la somme, sur les unités tirées qui le contiennent, du nombre d'occurrences de chacune) — et qui entrent dans une moyenne pondérée par personne, jamais dans une sélection ou une exclusion de lignes ou de colonnes. La permutation intra-segment de la chute (`S_gra`) ne porte pas sur les copies produites par le tirage, mais sur les **identités distinctes** tirées dans le réplicat ; chaque identité distincte garde, après permutation, le poids de sa multiplicité, si bien qu'elle ne se voit réattribuer ses propres réponses qu'avec la probabilité qu'elle aurait dans l'échantillon d'origine — exactement la protection que demande déjà le paragraphe « Doublons et permutation » ci-dessus. Dans chaque réplicat, la sélection complète est refaite : `exa_A`, `chute_A`, la régression du résidu, les deux choix `c_diag` et `c_exa`, puis `perte_B`, `Delta_r` et `Delta`, et cela pour A_r comme pour B_r. Rien de tout cela n'est un écart au texte ; c'est sa mise en œuvre au sens strict (fonctions `_tirer_unites_bloc`, `_poids_colonnes_unites`, `_exa_ponderee`, `_chute_ponderee`, `repliquer_selection` de `tab_evaluer.py`).
2. **Seuil C3 (section 8).** Le contrôle « moins de 10 cellules » ne porte que sur B_r, comme le dit déjà le texte de la ligne C3 (« … ont moins de 10 cellules dans un B_r »). A_r n'y est jamais soumis : il ne reçoit que le premier volet de C3, au moins une cellule par personne, comme B_r et comme les autres contrôles. Le code (`controle_C3`) applique le seuil de part uniquement aux colonnes de `poids_B`, jamais à celles de `poids_A`. Aucune divergence entre le code et le texte n'a été trouvée sur ce point ; c'est une clarification, pas une correction.

**Code d'évaluation figé avant dépôt, testé seulement sur données synthétiques.** SHA-256 au 11 septembre 2026 :

| fichier | SHA-256 |
|---|---|
| `analyses/tab_evaluer.py` | `ef10df1a185c58fbb0f84c7b9b1e451f2cfdcbfac818344802c804d946aecb74` |
| `analyses/test_tab_evaluer.py` | `be656bf16ce80d786e7172791716eb3dde020cf079581fdc02ea9208823d026b` |
| `analyses/tab_partition.py` | `aa3a861e7772ca91af4171833d4fd7ea831780130d274df406fc366403f2e738` |

La garde `GO-TAB` (`verifier_garde` / `charger_reel`, section 8 du fichier de code) empêche toute lecture réelle de Twin-2K-500 tant que `data/traces/GO-TAB` n'existe pas ; ce fichier n'a pas été créé, et cette page ne le crée pas.

**Remplacement du 11 septembre 2026, avant tout calcul.** Une seconde écriture indépendante de `tab_evaluer.py`/`test_tab_evaluer.py` (24 tests, ~25 s, contre 12 tests pour la première) a corrigé cinq défauts confirmés par relecture et par test synthétique dans la version dont le SHA figurait ci-dessus : (1) son `main` ne lançait ni le bootstrap, ni R3, ni S1 à S8, ni la règle de chute — seul `Delta` ponctuel du principal était calculé et imprimé ; (2) son contrôle R comparait l'exactitude sur les 2 058 personnes même pour des configurations à couverture partielle (`JSON Persona - GPT4.1-mini`, 1 000 personnes seulement), ce qui le faisait échouer à tort par construction (démontré : un univers jouet où une configuration à couverture partielle est parfaite sur ses cellules propres échoue quand même le contrôle R, avec un écart de 0,5 très supérieur au seuil 1e-12) ; (3) sa `valider_partition` ne détectait pas une unité indivisible coupée entre deux blocs, seulement les items dupliqués ou les chevauchements A/B (démontré : une partition jouet où une unité a un item dans le bloc 1 et un autre dans le bloc 2 passe silencieusement) ; (4) sa règle de coût divisait la durée projetée du bootstrap par 4 cœurs (`COEURS_COUT`) alors que la boucle de réplicats est un `for` Python séquentiel sans parallélisme réel, ce qui sous-estimerait la durée réelle d'un facteur 4 ; (5) le chemin générique `choix_diag="perte_A"` de l'ancienne version, étiqueté S5 dans son propre commentaire, remplaçait le choix **diagnostic** (`argmax` du résidu) par `argmin perte_A`, alors que la section 10 définit S5 comme un remplacement du choix **conventionnel** (`argmax exa_A`) par `argmin perte_A`, le diagnostic restant inchangé ; une fonction séparée, correcte, existait dans le même fichier sans être reliée à `main`, ce qui laissait deux définitions concurrentes de S5. La nouvelle version est testée : 24/24 tests passent sur données synthétiques (`data/traces/GO-TAB` absent tout du long, aucune lecture de Twin), et les SHA ci-dessus sont ceux de cette version. L'ancienne version est archivée hors dépôt (scratchpad de la session, `tab_evaluer_versionA.py`), non supprimée, pour trace. Voir aussi la section 7.2.

### 7.2 Précisions proposées, à valider par le responsable

Écrire `tab_evaluer.py` a mis au jour huit points que le texte des sections 1 à 10 ne tranche pas à la lettre. Pour chacun, la règle suivie ici est celle déjà énoncée à la section 6 en cas de tension : **l'option la plus conservatrice et la plus proche des conventions déjà fixées par `t1`**, parce que ce sont ces choix déjà fixés, et eux seuls, qui protègent le test contre l'ajustement (L1). Quand le code déjà écrit ne suit pas la résolution proposée ici, le tableau le dit : le code n'est **pas** modifié à l'occasion de cette relecture, l'écart est simplement déclaré, pour arbitrage.

| point | résolution proposée | justification | comportement du code aujourd'hui |
|---|---|---|---|
| **(a) Permutations partagées ou séquentielles** | Suivre la convention de `t1_mesures.chute` : un seul générateur, avancé en séquence à travers les configurations (et, ici, les rotations), plutôt qu'un jeu fixe de P permutations rejoué à l'identique pour toutes. | `t1_mesures.main` crée `rng_p` une fois puis le fait avancer d'un appel de `chute` à l'autre, à travers les conditions et les segmentations (`t1_mesures.py`, boucle `for nom in conditions`) : chaque condition reçoit un tirage frais, pas le même. C'est la convention déjà fixée que `tab` réutilise ailleurs sans y toucher (Q1, Q2). | **Écart.** Le code tire **un seul jeu** de P permutations par estimation ponctuelle (et par réplicat de bootstrap) et le réemploie à l'identique pour **toutes** les configurations et les trois rotations (`analyser_tournoi`, `permutations_identites` appelé une fois, puis passé tel quel à `mesurer` pour chaque `nom`). C'est un choix de réduction de variance (nombres aléatoires communs) documenté en tête de fichier, mais il diverge de la consommation séquentielle de `t1`. |
| **(b) Conditions couvertes par le contrôle R** | R doit porter sur toutes les conditions à couverture pleine (2 058 personnes) de `t1-chute-segmentations.csv` sous `S_gra`, et non sur les seules candidates et adversaires du tournoi ; les conditions à couverture partielle (`JSON Persona - GPT4.1-mini`, `JSON Persona (Predicted Output) - GPT4.1`, `LLM Finetuning`) devraient elles aussi être vérifiées, mais restreintes à leur propre `n` publié par `t1`, jamais comparées sur 2 058 personnes. | R sert à prouver que le pipeline partagé (`t1_commun`, `a44_mesures`) redonne des chiffres déjà publiés, avant tout calcul propre à `tab` : plus la liste vérifiée est large, mieux le contrôle protège, sans coût (aucune donnée nouvelle lue). Comparer une condition à couverture partielle sur le périmètre complet est le défaut confirmé de l'ancienne version (démonstration ci-dessus) : la restriction au bon `n` est nécessaire, pas seulement l'exclusion. | **Écart partiel.** `_lire_reference_t1` ne garde que les lignes dont `n` égale 2 058, donc aucune condition à couverture partielle n'est jamais comparée (le défaut de l'ancienne version ne peut pas se reproduire) ; mais `controle_reproduction` ne boucle que sur `CANDIDATES_PRINCIPAL + ADVERSAIRES` (12 conditions), pas sur toutes les conditions à couverture pleine de `t1` (par exemple les deux `Persona Summary`, à 2 058 personnes elles aussi, n'y sont pas vérifiées). |
| **(c) S2 à S5 ont-elles un intervalle ?** | Non : S2 à S5 restent des estimations ponctuelles, sans bootstrap ni intervalle propre. | La section 10 ne rouvre jamais une revendication fermée à partir de S2 à S5 ; un intervalle n'y est pas décisionnel. La section 7 ne budgète le coût que pour « chaque bootstrap (principal, S1) », pas pour quatre analyses supplémentaires : ajouter leur bootstrap serait un coût de calcul non prévu par le texte figé avant tout résultat. | **Conforme.** `analyser_tournoi(..., avec_regle=False)` (S2) s'arrête après l'estimation ponctuelle, avant l'appel à `bootstrap`. S3, S4, S5 réutilisent directement les quantités déjà mesurées du principal (`secondaires`, `calculer_delta` sur `mes` existant) : aucun bootstrap n'est relancé. |
| **(d) Portée de la règle de coût et « 4 cœurs »** | La règle de coût s'applique séparément à chaque bootstrap (principal, S1), sur sa propre mesure de durée ; « 4 cœurs » ne doit pas être traduit par une division arithmétique de la durée mesurée, puisque la boucle de réplicats ne lance aucun parallélisme réel : la projection doit utiliser la durée mono-cœur telle quelle. | Diviser une durée mono-cœur mesurée par un facteur de parallélisme qui n'existe pas dans le code sous-estimerait le temps réel et retarderait à tort le passage à B = 500 : c'est le défaut confirmé de l'ancienne version. Ne pas diviser est la lecture qui protège le mieux contre un dépassement de coût non détecté. | **Conforme.** Le bootstrap principal et celui de S1 sont deux appels indépendants de `bootstrap(...)`, chacun avec son propre chronométrage et sa propre projection après `n_replicats_projection` réplicats. Aucune constante de type « cœurs » n'existe dans le fichier ; la projection est `duree_mesuree / k * b_cible`, sans division par un nombre de cœurs. |
| **(e) Personne sans cellule dans une analyse R3** | Une personne sans cellule dans un `A_r` ou un `B_r` d'une analyse R3 (retrait d'une famille) rend la **revendication entière** « non concluante », pas seulement le retrait de cette famille de l'agrégat R3. | Toute autre défaillance d'un contrôle bloquant de la section 8 (C1 à C4, T, R) ferme déjà le test sur « non concluant » sans exception partielle ; traiter R3 différemment (ignorer la seule famille en cause) introduirait une règle à deux vitesses non écrite dans le texte. | **Conforme.** `analyser_tournoi` calcule `condition_cellule` pour chacune des 14 familles ; si une seule est fausse, la décision entière devient `{"statut": "non concluant", "motif": "personne sans cellule dans une analyse R3 (I5)"}`, avant même de lire le bootstrap. |
| **(f) S4/S5 refont-elles le choix ?** | Oui, les deux repassent par la fonction générique de sélection, mais seule la partie de la variante qu'elles déclarent change réellement le résultat : S4 ne touche que la métrique de perte (`c_diag`/`c_exa` sont donc identiques au principal), S5 ne touche que le choix conventionnel (`c_diag` reste celui du principal, seul le choix par exactitude devient `argmin perte_A`). | C'est la lecture littérale de la section 10 : S4 ne modifie que Q4, S5 ne modifie que le « choix conventionnel ». Refaire la sélection par la même fonction que le principal, plutôt qu'écrire un chemin de code séparé pour chaque variante, évite exactement la confusion qui a produit le défaut (5) de l'ancienne version, où deux définitions de S5 coexistaient. | **Conforme.** `secondaires` appelle `calculer_delta(mes, cand, variante)` pour S3, S4, S5, qui repasse par `selectionner(...)` ; pour S4, seul `v["perte"]` change (le diagnostic et le conventionnel restent `"residu"`/`"exactitude"`, donc les choix sont mathématiquement identiques au principal) ; pour S5, seul `v["conventionnel"]` devient `"perte_A"`, le diagnostic restant `"residu"` (inchangé). |
| **(g) « B0 » en S8** | Les deux : `B0 mode` et `B0 tirage`, publiés comme deux bornes séparées, en plus de `B1 argmax`. | Le texte de la section 8 nomme les deux `B0` comme témoins bloquants (contrôle T) sans en distinguer un troisième au-dessus de l'autre pour S8 ; en retenir un seul serait un choix silencieux non déclaré, alors que publier les deux ne coûte rien. | **Conforme.** `BORNES_S8 = ["B0 mode", "B0 tirage", "B1 argmax"]` ; `secondaires` écrit une perte B distincte pour chacune des trois, par rotation. |
| **(h) Fichier de la décision, absent du §13** | Écrire la décision (R1 à R4, statut, `Delta`, bornes de l'IC) comme des lignes supplémentaires dans `tab-rotations.csv`, plutôt que créer un fichier hors de la liste fixée au §13. | Le §13 fixe la liste des fichiers avant tout résultat ; ajouter un fichier non prévu serait lui-même un écart aux choix déjà fixés (L1), alors que `tab-rotations.csv` contient déjà une ligne par rotation et s'y prête. | **Conforme.** `_lignes_rotations` ajoute une ligne `role="decision"` par analyse (principal, S1) dans `tab-rotations.csv` ; `ecrire_sorties` y ajoute aussi une ligne `analyse="lecture"` pour la lecture globale, et le statut de S1 apparaît une seconde fois dans `tab-secondaires.csv`. |

---

## 8. Seuils de couverture et contrôles, exécutés avant tout calcul de perte

Tous sont **bloquants** pour le périmètre concerné. Si l'un échoue au principal, le rapport écrit « **non concluant** » : ni survie, ni chute de la revendication. Les seuils ont été fixés en connaissant les comptes de structure du §4.3 et de l'audit, et **aucun chiffre de résultat**.

| contrôle | règle | justification |
|---|---|---|
| **C1, couverture d'item** | dans chaque B_r et chaque A_r, chaque item a au moins **25 %** des personnes du périmètre sur le masque | Par construction, un bras d'expérience à trois bras concerne environ un tiers des personnes. 25 % laisse passer ce plan et arrête une configuration qui viderait une part notable d'un bras : `PredOut mini`, par exemple, perd 56 % des cellules de `Q159` (audit §2.3). |
| **C2, cellules gardées** | dans chaque B_r et chaque A_r, le masque garde au moins **99 %** des cellules humaines observées du périmètre | C'est le double du seuil de signalement par configuration de `t1` et `i3b` (0,5 %), pour tenir compte d'une intersection de plusieurs configurations et d'une concentration possible des pertes dans un bloc. |
| **C3, personnes** | chaque personne a au moins 1 cellule dans chaque B_r et chaque A_r, et **au plus 1 %** des personnes du périmètre ont moins de 10 cellules dans un B_r | Une moyenne par personne a besoin d'au moins une cellule. Au-dessous de 10 cellules, elle est dominée par sa granularité. On borne la part de ces personnes au lieu de les exclure, parce qu'exclure selon la couverture changerait la population d'un bloc à l'autre. |
| **C4, unités** | chaque B_r contient au moins **10 unités indivisibles** | Le bootstrap rééchantillonne des unités. En dessous, l'intervalle côté items est dégénéré. |
| **T, témoin de chute** | `B0 mode` et `B0 tirage` ont une chute A inférieure à **0,005** en valeur absolue dans chaque rotation | Seuil du contrôle 3 de `t1`. Si le témoin chute, le dispositif fabrique de la chute sur les sous-ensembles. |
| **R, reproduction** | sur les 108 items entiers et les 2 058 personnes, l'exactitude calculée par le script d'évaluation égale `exactitude_vraie` de `t1-chute-segmentations.csv` sous `S_gra`, écart maximal **1e-12** | Même chaîne que `t1`. Le script écrit seulement « passe » ou « échoue », pas les valeurs. |
| **H, empreinte** | le SHA-256 de `tab-partition-items.csv` égale celui du §4.2 | Le script d'évaluation refuse de démarrer sinon. |

Pour les analyses laissant une famille de côté (R3), C3 et C4 ne s'appliquent pas : retirer *Pricing* retire 13 ou 14 unités par bloc. Seule la condition d'au moins une cellule par personne demeure.

---

## 9. Règle de chute

**La revendication d'utilité du diagnostic ne survit que si les quatre conditions sont vraies au principal.** Sinon, elle ferme.

- **R1** : `Delta ≤ −0,01`, la perte B étant dans [0, 1].
- **R2** : la borne supérieure de l'intervalle à 95 % de `Delta` est **strictement inférieure à 0**.
- **R3, robustesse par famille** : pour chacune des 14 familles d'analyse f, on retire les items de f de A et de B dans les trois rotations, on refait toute la sélection, et l'estimation ponctuelle `Delta^(−f)` doit être **strictement négative**. Le critère est le signe seul, par arbitrage du 11 septembre 2026. Aucun intervalle n'est calculé pour ces 14 analyses. Si une valeur `Delta^(−f)` est négative mais supérieure à −0,01, le rapport écrit « affaibli sans *f* », sans que la revendication ferme.
- **R4, contrôle PMM** : la revendication ferme si `perte_B(PMM k=10) ≤ perte_B(c_diag)` **dans les trois rotations**, ce qui traduit le « systématiquement » du document 1 par trois rotations sur trois (arbitrage du 11 septembre 2026). `PMM` est ici la version de `t1`, ajustée sur la vague 4 d'autres personnes, avec l'asymétrie d'information de la section 6.

**Interprétation stricte du document 1, faite avant tout résultat.** Au pied de la lettre, le document 1 ferme la revendication si `Delta` ne descend pas à −0,01 **et** si la borne supérieure n'est pas négative. Elle survivrait donc avec R1 seul ou R2 seul, et un effet minuscule mais net suffirait. **Cette page exige les deux conditions, `Delta ≤ −0,01` ET borne supérieure de l'IC 95 % < 0.** C'est une interprétation stricte du document 1, arrêtée par arbitrage le 11 septembre 2026, avant qu'aucun chiffre de `tab` n'existe.

**Écrit d'avance** : si les deux règles choisissent la même configuration dans les trois rotations, `Delta = 0` et la revendication ferme par R1. Ce n'est pas une issue neutre.

---

## 10. Analyses secondaires

Aucune ne peut rouvrir une revendication fermée par la section 9. Toutes emploient `S_gra` seule. Aucune autre segmentation n'est calculée, pour ne pas multiplier les chemins d'analyse.

| | analyse | lecture |
|---|---|---|
| **S1** | 8 configurations, 1 000 personnes (pid 1 à 1 000), règles R1 à R4 appliquées | Si le principal survit et que S1 ferme, le rapport écrit « fragile au périmètre ». |
| **S2** | 6 configurations riches, sans `Demographics Only`, 2 058 personnes | Vérifie qu'un choix ne tient pas seulement à une différence d'information (L7). |
| **S3** | diagnostic = chute A brute, non résidualisée | |
| **S4** | perte B = 1 − exactitude catégorielle B | Contrôle prévu par le document 1. |
| **S5** | choix conventionnel = `argmin perte_A`, même métrique que B, au lieu de `argmax exa_A` | |
| **S6** | **analyse secondaire déclarée** : adversaires ajustés sur le retest des vagues 1 à 3 d'autres personnes seulement, sans aucune réponse de vague 4 (section 6), contrôle R4 recalculé | Rapportée à côté de la version de `t1`, dont l'asymétrie d'information est nommée. Ne change pas la règle. |
| **S7** | les deux `Persona Summary` : `exa_A`, `chute_A`, `perte_B` par rotation, hors de toute régression et de tout choix | Description seule, suspectes de fuite. |
| **S8** | par rotation : `Delta_r`, `c_diag_r`, `c_exa_r`, parts de coïncidence au bootstrap ; meilleur adversaire statistique choisi par `exa_A` parmi `B1`, `B2` et `PMM`, avec sa perte B ; `B0` et `B1` publiés comme bornes | |

---

## 11. Prédictions datées, hors règle de décision

**Écrites le 11 septembre 2026, avant tout calcul de `tab`, et conservées par arbitrage du même jour.** Ce sont des [HYPOTHÈSE]. Elles sont scorées dans le rapport, mais **elles ne font pas partie de la règle de décision** : la survie ou la chute de la revendication se lit uniquement à la section 9, qu'une prédiction soit juste ou fausse.

- **P1** : les deux règles choisissent la même configuration dans au moins deux rotations sur trois, et la revendication ferme par R1. Motif : avec 7 candidates, dont une seule à démographies seules, la sélection est grossière (L2).
- **P2** : `perte_B(PMM) ≤ perte_B(c_diag)` dans les trois rotations, donc R4 ferme aussi. Motif : les adversaires voient la distribution de vague 4 des items de B (section 6).
- **P3** : sous S6, la perte B de `PMM` augmente par rapport à la version de `t1` dans les trois rotations.

---

## 12. Limites, écrites avant tout calcul

- **L1. Test non aveugle : les chiffres de `t1` sur les 108 items sont connus du projet.** Les exactitudes, chutes et résidus de `t1` sur les 108 items entiers sont publiés dans le dossier. Or les quantités sur A (72 items) et B (36 items) sont des restrictions de ces quantités, et un lecteur de `t1` peut anticiper une partie des choix.
  - **Ce que cela implique** : seuls les choix déjà fixés protègent contre l'ajustement. Ce sont la partition, produite par les seules métadonnées d'items et figée par son SHA, la règle de chute, les seuils, les graines et la liste fermée des analyses. L'ignorance des données ne protège rien ici. Tout écart à ces choix, même motivé, retire au test la protection qui lui reste.
  - **Réplication nécessaire** : même si la revendication survit, elle ne vaut qu'à titre conditionnel. Une réplication sur une ressource dont aucun chiffre n'est connu du projet reste nécessaire avant d'écrire que le diagnostic guide le choix d'un simulateur.
- **L2. La sélection parmi 7 candidates est grossière.** La régression du résidu a 5 degrés de liberté, et le choix est un `argmax`. Une seule configuration atypique, par exemple `Demographics Only`, peut déplacer la droite et le choix. Le test porte sur une règle de décision appliquée à 7 points, pas sur la validité générale du diagnostic.
- **L3. Les invites ne sont pas vérifiables localement** (réserve R1 de l'audit). Le classement « admissible » repose sur les noms de configuration, le README et l'examen de l'objet `wave_split`, vérifié propre sur 294 personnes sur 2 058 seulement.
- **L4. Objet persona utilisé** (réserve R2 de l'audit) : `full_persona`, qui contient les réponses de vague 4 aux questions répétées, est absent localement. Rien n'établit qu'aucune des 7 configurations ne l'a employé.
- **L5. Les pid 1 à 500 correspondent probablement aux personnes d'affinage** de `Finetuning 500`. C'est une inférence tirée de leur absence exacte du fichier de sortie. Le périmètre de S1 (pid 1 à 1 000) les contient, n'est pas un échantillon aléatoire, et coïncide avec la couverture de `JSON Persona mini`, dont le mécanisme de sélection est inconnu.
- **L6. Petites cellules `S_gra`.** Sur 2 058 personnes : 40 cellules, dont 1 singleton. Sur les 1 000 de S1 : 39 cellules, 2 singletons, 8 cellules de moins de 5 personnes (21 personnes) et 16 de moins de 10 (audit §3.5). Une personne seule dans sa cellule ne peut pas être permutée, et la chute y est nulle par construction. Cela pèse sur S1 plus que sur le principal, et plus encore dans les réplicats bootstrap, où les identités distinctes d'une cellule sont moins nombreuses.
- **L7. Sous-tournoi démographique supprimé.** Il n'y a qu'une configuration à démographies seules. Le tournoi principal compare donc des ensembles d'information différents : `Demographics Only` en reçoit moins, et `Text Persona (Repeating Questions)` en reçoit peut-être plus, selon ce que signifie « repeating questions » (réserve R3 de l'audit). Un choix peut refléter une différence d'information plutôt que de méthode. S2 retire la première source, pas la seconde.
- **L8. False consensus n'est plus un contrôle externe.** `QID287` reste dans la partition (bloc B1). `QID290` est un curseur hors des 108. Le contrôle externe descriptif prévu par le document 1 disparaît, et aucun contrôle de contenu hors partition ne le remplace.
- **L9. Stratification imparfaite.** Lignes de matrice 10 / 14 / 16, items inter-sujets 12 / 15 / 21, familles d'analyse 9 / 4 / 5 : les trois rotations n'ont pas la même composition et ne sont pas échangeables. Le bloc B2 ne compte que 4 familles, et une famille y pèse jusqu'à 13 items sur 36. La stratification par famille n'a de contenu que pour *Pricing* et *Non-experimental heuristics and biases*.
- **L10. Proximité de contenu résiduelle.** Parmi les 40 items de prix, des catégories voisines sont réparties dans des blocs différents : boissons gazeuses et boissons allégées, chips de pomme de terre et chips de tortilla, bonbons et chocolat, produits laitiers et lait, remèdes contre la migraine et contre le rhume. La règle de groupement ne couvre pas ce cas.
- **L11. Information des adversaires** (section 6) : R4 n'est pas une comparaison à information égale.
- **L12. Mémorisation par pré-entraînement.** Twin-2K-500 est public depuis mai 2025, et les dates de génération des sorties ne sont pas vérifiées.
- **L13. Métriques mêlées.** La perte B mêle une distance ordinale (lignes de matrice) et une distance 0/1 (MC). Les blocs n'ont pas la même composition de types, et une perte B n'est comparable qu'à l'intérieur d'une rotation. `Delta_r` respecte cette contrainte, puisque les deux choix sont notés sur le même B_r.
- **L14. Horodatage.** Page non déposée. Le dossier est synchronisé par iCloud, et l'horodatage n'est pas un dépôt tiers (`a45` point 11).
- **L15. Une candidate nettement plus exacte peut tirer la régression du résidu et déplacer le résidu maximal vers la candidate la moins exacte.** Vu sur synthétique en écrivant les tests de `tab_evaluer.py` : avec sept points seulement (L2), une configuration très à part sur `exa_A` (par exemple une candidate proche de 1,0 quand les six autres sont groupées) a un fort effet de levier sur `np.polyfit` ; le résidu de la candidate la moins exacte peut alors devenir le plus grand, non parce qu'elle porte le plus de personne, mais parce que la droite a pivoté vers le point isolé. Aucune option n'est retenue ici, sans trancher :
  - **Régression robuste** (Theil-Sen, ou une repondération itérative) à la place de `np.polyfit` degré 1 pour Q3. Coût : modifie une quantité déjà figée par le préenregistrement (Q3, section 5), ce qui demande un nouvel arbitrage avant tout calcul réel, pas seulement une correction de bogue ; le calcul lui-même reste bon marché.
  - **Diagnostic de sensibilité descriptif**, publié à côté du choix retenu : un résidu recalculé en retirant tour à tour chacune des candidates (jackknife sur la régression), sans toucher à la règle de décision figée. Coût faible (une sortie de plus), mais ne corrige rien : il documente la fragilité après coup sans protéger le choix qui a servi à R1–R4.
- **L16. Environ 4 % des réplicats du bootstrap ne tirent aucune ligne de matrice à plus de deux niveaux dans un bloc.** Vu sur synthétique : le tirage avec remise des unités d'un bloc (section 7) laisse, par le hasard de l'échantillonnage, une part non négligeable de réplicats sans aucune unité « ligne de matrice à K > 2 » dans ce bloc. Si l'avantage réel du diagnostic ne passe que par la distance ordinale de ces lignes (et non par la distance 0/1 des MC), ces réplicats-là ne peuvent numériquement montrer aucun avantage, ce qui gonfle la queue haute de `Delta` et peut empêcher R2 de fermer même si l'effet est réel. Aucune option n'est retenue ici, sans trancher :
  - **Stratifier le tirage des unités** pour garantir au moins une unité « ligne de matrice à K > 2 » par bloc et par réplicat. Coût : modifie le mécanisme de bootstrap déjà figé (section 7), donc un nouvel arbitrage avant tout calcul réel ; complique aussi l'interprétation de l'intervalle, qui ne serait plus un tirage avec remise simple sur la population réelle d'unités.
  - **Augmenter B** au-delà de 1 000 (voire au-delà des 500 de la règle de coût) pour stabiliser l'estimation des percentiles. Coût : purement calculatoire, ne change aucune règle déjà figée ; mais ne fait pas disparaître le plancher mécanique de ~4 % de réplicats sans signal ordinal, puisque celui-ci vient de la structure du tirage à taille de bloc fixée, pas de la taille de `B`.

---

## 13. Fichiers que `tab` produira

| fichier | contenu |
|---|---|
| `analyses/tab_partition.py`, `analyses/test_tab_partition.py` | la partition et ses tests, **déjà écrits** |
| `resultats/tab-partition-items.csv` | la partition, **déjà écrite**, SHA du §4.2 |
| `analyses/tab_evaluer.py` | l'évaluation. Elle vérifie H, puis C1 à C4, T et R, avant toute perte |
| `resultats/tab-controles.csv` | contrôles de la section 8 |
| `resultats/tab-rotations.csv` | `exa_A`, `chute_A`, `res_A`, `perte_B` par configuration et rotation, choix, `Delta_r` |
| `resultats/tab-bootstrap.csv` | les réplicats de `Delta`, de `Delta_r` et des choix |
| `resultats/tab-familles.csv` | R3, les 14 valeurs `Delta^(−f)` |
| `resultats/tab-secondaires.csv` | S1 à S8 |
| `resultats/tab-resultats.md` | le rapport. Il reproduit cette page, et elle fait foi en cas de divergence |

---

## 14. Arbitrages rendus le 11 septembre 2026, avant tout résultat

1. **Groupement `QID288` + `QID289` conservé**, choix conservateur. La partition et son SHA sont inchangés.
2. **Règle de chute stricte** : R1 **et** R2 sont exigés. C'est une interprétation stricte du document 1 (section 9).
3. **R4 à trois rotations sur trois** ; **R3 au signe seul**.
4. **Comparaison principale à information égale**, `c_diag` contre `c_exa` entre configurations de modèle de langage. Les adversaires de vague 4 inter-personnes sont rapportés avec leur asymétrie d'information nommée. La variante entraînée sur les vagues 1 à 3 seulement est l'analyse secondaire déclarée S6.
5. **Perte 0/1 conservée pour les MC** ; **prédictions P1 à P3 conservées**, dans une section datée séparée de la règle de décision (section 11).

**Reste en attente** : la validation du responsable, qui porte aussi sur le critère 5 de partition (plan inter-sujets, §4.1), et le **dépôt OSF de cette page avant la première exécution de `tab_evaluer.py`**.
