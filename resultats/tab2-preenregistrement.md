# tab2. Préenregistrement : Twin A→B v2, candidats hétérogènes et cible de correspondance

**Statut : figé le 2026-09-11, publié par commit Git avant toute implémentation et toute exécution.** Même convention que `tab-preenregistrement.md` : le commit public daté tient lieu de dépôt tiers, et toute modification ultérieure est un écart déclaré. Dépôt au moment de l'écriture : `6accc1b`, arbre non propre. **Aucun code `tab2` n'existe. Aucune corrélation, chute, perte ni exactitude n'a été calculée pour `tab2`.** `data/traces/GO-TAB2` n'existe pas.

## 0. Transparence : ce test n'est pas aveugle

**Ce qui est déjà connu du projet, et en partie du rédacteur.**
1. `t1` publie sur les 108 items et 2 058 personnes l'exactitude, la chute sous permutation (quatre segmentations, dont `S_gra`) et les résidus des 13 configurations et de `B0 mode`, `B0 tirage`, `B1 argmax`, `B2 argmax`, `PMM k=10` (version entraînée sur la vague 4 d'autres personnes). Il publie aussi la part de variance commune entre chute et exactitude, 28 %.
2. `tab` v1 publie, **par rotation et sur la même partition**, `exa_A`, `chute_A` et `perte_B` des 7 LLM, des 5 adversaires dans leurs deux versions (vague 4 et retest, S6) et des deux `Persona Summary` (`tab-rotations.csv`, `tab-secondaires.csv`). **Les choix des règles de la section 4 sur A peuvent donc se lire presque entièrement dans ces fichiers**, aux graines de permutation près.
3. Valeurs lues par le rédacteur : Delta v1 = +0,0266 [+0,0026 ; +0,0412] ; `c_diag` = `Text Persona - Gemini-Flash2.5` et `c_exa` = `JSON Persona - GPT4.1` dans les 3 rotations ; `perte_B` de 0,324 à 0,330 pour `c_diag` contre 0,372 à 0,416 pour `PMM` (version vague 4) ; S3 donne Delta = 0 ; résidus des 7 LLM dans [−0,010 ; +0,013] et `perte_B` des LLM entre 0,30 et 0,37 (revue hostile) ; exactitudes `t1` de 0,4625, 0,5646 et 0,5738, et 0,7119 pour le retest humain (audit). Le rédacteur n'a ouvert aucune colonne de valeurs de `tab-rotations.csv`, `tab-secondaires.csv` ni des CSV `t1`, seulement leurs en-têtes.
4. Comptes faits pour la section 9 : sur les humains seuls, cellules rares stables et nomenclature des modalités. Pour les configurations, seul le statut vide ou renseigné a été lu.

**Ce qui ne l'est pas.** Aucune corrélation entre prédiction et réponse, intra-segment ou non, n'a jamais été calculée dans le projet sur un bloc de Twin, pour aucun candidat, ni la chute sur B, ni le rappel des raretés stables sur Twin.

**Pourquoi le test reste informatif.** La cible primaire (ρ_B, §5), la garde de perte, les règles par rangs et sous contrainte et la règle à trois issues sont nouvelles. Elles sont fixées ici sans aucune valeur de ρ. Ce que l'on sait des quantités sur A permet d'anticiper *quel* candidat chaque règle choisit, pas *ce que ce choix vaut* sur la cible primaire. **Risque déclaré** : l'écart de `perte_B` connu entre LLM riches et `PMM` rend prévisible l'échec de la garde (§7) si une règle choisit un adversaire statistique.

**Ce qu'exigerait un test aveugle.** Une ressource dont aucun chiffre de sélection ni de cible n'est connu du projet : un autre panel à retest, par exemple un panel ANES ou GSS, avec des simulateurs générés par un tiers et la vérité gardée par ce tiers jusqu'au gel du code. Variante partielle, **non vérifiée** : juger sur les 12 curseurs de Twin, jamais évalués par le projet, en supposant que les sorties LLM les contiennent. Seul le côté B serait alors aveugle.

## 1. Question et estimand

**Question.** Parmi des méthodes réellement hétérogènes, un audit sur A qui combine exactitude et correspondance choisit-il mieux qu'un audit sur l'exactitude seule, pour une utilisation au niveau individuel sur B ?

**Estimand principal.** Pour r = 1, 2, 3, B_r est le bloc r de la partition v1 et A_r son complément.
`Delta_r = [rho_B,r(c_rang,r) − rho_B,r(c_exa,r)] / rho_B,r(retest)` et `Delta = moyenne des trois`. Un Delta positif est favorable à l'audit combiné.
**Garde** : `Gamma_r = perte_B,r(c_rang,r) − perte_B,r(c_exa,r)`, et `Gamma` est leur moyenne.
Si les deux règles choisissent le même candidat dans une rotation, `Delta_r` et `Gamma_r` valent exactement 0.

## 2. Candidats : dix, sur 2 058 personnes (pid 1 à 2 058)

| # | candidat | contexte individuel reçu | réponses humaines d'autres personnes aux items cibles |
|---|---|---|---|
| 1 | `Demographics Only - GPT4.1-mini` | **non**, démographies seules | non |
| 2 à 7 | `JSON Persona - GPT4.1`, `Text Persona (Default Temperature)`, `(Reasoning)`, `(Repeating Questions)`, `Text Persona` (les quatre en GPT4.1-mini), `Text Persona - Gemini-Flash2.5` | **oui**, persona des vagues 1 à 3 sans item répété (réserves R1 et R2 de l'audit ; R3 pour *Repeating Questions*) | non |
| 8 | `B1 argmax [retest]` | **non**, 14 démographies | oui, vagues 1 à 3, 5 plis de personnes |
| 9 | `B2 argmax [retest]` | **oui**, 494 items de contexte des vagues 1 à 3 | oui, idem |
| 10 | `PMM k=10 [retest]` | **oui**, contexte et démographies | oui, idem |

Les 7 LLM sont les candidates du principal v1, dont `Demographics Only`. **Adversaires en version retest** (S6 v1, `t1_baselines.calculer` sur une copie de `paq` où `codes[REF]` est remplacé par le retest) : ainsi aucun candidat ne voit une réponse de vague 4 de qui que ce soit, hors mémorisation. Ils gardent une asymétrie déclarée, puisqu'ils voient les réponses antérieures d'autres personnes aux mêmes questions. La version vague 4 est la secondaire S1. Départage : ordre du tableau.

**Exclus.** Les deux `Persona Summary`, par défaut. Le seul `persona_summary` documenté vient de `full_persona`, qui porte les réponses de vague 4 de la personne à toutes les questions répétées, et **les 108 items sont tous répétés**. Un résumé fuité encoderait donc la cible de chaque item de B. Il dominerait à la fois `exa_A`, `chute_A` et ρ_B, et le test mesurerait la détection d'une fuite, pas l'utilité d'un audit de correspondance. L'indice faible contraire de l'audit (aucune configuration au-dessus de 0,5738) ne lève pas le doute. Leurs quantités sont publiées en S5, sans rôle. Sont aussi exclus : `JSON Persona - GPT4.1-mini` (1 000 personnes), les deux `Predicted Output` et `Finetuning 500` (audit §2.4). `B0 mode` et `B0 tirage` sont des témoins, et `humains vagues 1-3 (retest)` sert de normaliseur.

## 3. Données, masque, partition

Les données, le masque (humain de vague 4 et les 10 candidats répondent), la partition (`tab-partition-items.csv`, SHA `07b3de89…3b05`), les unités, les familles et `S_gra` sont **ceux de v1, inchangés**. Graines : adversaires `20260909`, permutations `20260911 + 30`, bootstrap `20260911 + 40`. Aucune autre graine ne sera essayée.

## 4. Règles de sélection, calculées sur A seul

Quantités sur A, identiques à v1 : `exa_A` (Q1) et `chute_A` (Q2 : P = 200 permutations intra `S_gra`, chute absolue).
- **R_exa** : `argmax exa_A`.
- **R_chute** (S3 v1) : `argmax chute_A`.
- **R_rang, règle combinée primaire** : on classe les candidats par `exa_A` décroissante et par `chute_A` décroissante (rangs moyens en cas d'égalité), puis on retient `argmin` de la somme des deux rangs. En cas d'égalité, on prend la plus forte `exa_A`, puis l'ordre du tableau. Il n'y a ni régression ni paramètre, ce qui écarte la fragilité L15.
- **R_contrainte, secondaire** : `argmax exa_A` parmi les candidats dont `chute_A ≥ 0,5 × max chute_A`.

Aucune quantité de B n'entre dans une règle. Aucun réglage n'est permis après lecture.

## 5. Cibles sur B, déclarées d'avance

**Cible primaire : ρ_B, la capacité à ordonner les personnes à l'intérieur de leur segment.**
- **Items admissibles** E_r : lignes de matrice (`est_ordinal`) et items MC à exactement 2 codes dans la nomenclature commune, soit 28 / 27 / 33 items (§9).
- **Valeurs** : pour une ligne de matrice, v = `val_ord`, comme en v1 ; pour un item binaire, v = l'indice du code (0 ou 1).
- **Corrélation par item** j : on prend les personnes du masque, avec un poids w_i. On centre `v(ŷ)` et `v(y)` par leur moyenne pondérée dans la cellule `S_gra` de la personne, puis `rho_j = Σ w x̃ ỹ / √(Σ w x̃² · Σ w ỹ²)`, fixé à **0** si l'un des deux termes de variance est nul.
- **Agrégat** : `rho_B,r(c)` est la moyenne des `rho_j` sur E_r, pondérée par les poids de colonnes.
- **Normaliseur** : `rho_B,r(retest)` est la même quantité où la réponse des vagues 1 à 3 de la personne sert de prédiction.

**Pourquoi cette cible ne se réduit pas à l'exactitude.** (1) ρ_j est invariante à tout décalage de niveau des prédictions, alors que la perte ne l'est pas. (2) Tout prédicteur aveugle à la personne dans son segment a ρ = 0, quelle que soit son exactitude : `B0 mode` donne exactement 0. (3) Le centrage intra-`S_gra` retire l'ordre porté par le seul segment, que le projet a vu gonflé par les LLM (R3). (4) Pour un item binaire, la chute sous permutation vaut deux fois la covariance intra-segment : ρ en est la version **standardisée**, qui ne récompense pas la simple dispersion des prédictions.
C'est ce qui sert une utilisation individuelle : cibler, apparier, relier des réponses entre items. La mesure est proche du « signal apparié » de Wang et al. (2609.07987), ce qui est déclaré.

**Cibles secondaires, sans rôle de décision** : (a) `perte_B`, Q4 de v1, qui sert aussi de garde (§7) ; (b') `chute_B`, soit Q2 sur les colonnes de B avec P = 200.

**Cible (c) retirée.** Le rappel des raretés stables sur B suit la définition de R2 (modalité de part humaine < 10 % en vague 4, `a8_commun.modalites_minoritaires` ; stable = réponse identique au retest). Le minimum fixé **avant le comptage** était de 300 cellules rares stables sur au moins 5 items par bloc. Le compte donne 1 471 cellules (15 items), 1 045 (21) et **180 (5)** : B3 échoue, donc la cible est retirée. Rappel et précision sont publiés en S6 pour les rotations 1 et 2 seulement, à titre descriptif.

## 6. Inférence

**Bootstrap** conjoint personnes × unités, B = 2 000, mécanisme v1 (`tirer_replicat`) : personnes avec remise, unités par bloc avec remise, poids de lignes et de colonnes, permutations sur les identités distinctes (P = 20 par réplicat pour `chute_A`). Chaque réplicat refait `exa_A`, `chute_A`, les quatre règles, ρ_B de chaque candidat et du retest (forme close, sans permutation), `perte_B`, Delta et Gamma. Intervalles : percentiles 2,5 et 97,5.
**Règle de coût v1** : si la projection après 20 réplicats dépasse 6 h, B passe à 1 000, déclaré. **Robustesse par famille** : pour chacune des 14 familles, retrait dans A et B, puis estimation ponctuelle de `Delta^(−f)`.

## 7. Règle de décision à trois issues

Seuils : utilité pratique **δ = 0,05**, soit 5 % de la capacité d'ordre du retest humain, fixé sans aucune valeur de ρ ; marge de non-infériorité **m = 0,01** sur `perte_B`, le seuil R1 de v1. Les conditions sont évaluées **dans cet ordre**, et la première vraie l'emporte :
1. **Indécision (non concluant)** si un contrôle bloquant du §8 échoue.
2. **Fermeture** si R_rang et R_exa choisissent le même candidat dans les 3 rotations, à l'estimation ponctuelle.
3. **Fermeture** si la borne haute de l'IC de Delta est < δ, ou si la borne basse de l'IC de Gamma est > m : l'ordre gagné se paie en exactitude.
4. **Succès** si Delta ≥ δ, borne basse de Delta > 0, borne haute de Gamma ≤ m, et `Delta^(−f)` > 0 pour les 14 familles.
5. **Indécision** sinon. Le motif est écrit : IC trop large, garde incertaine ou fragilité par famille.

Contrastes rapportés avec IC, **sans rôle de décision** : R_chute contre R_exa, R_contrainte contre R_exa, R_rang contre R_chute, sur ρ_B, `perte_B` et `chute_B`.

## 8. Contrôles bloquants, exécutés avant tout calcul de cible

**H, C1 à C4, T et R de v1, inchangés** : R porte sur les 7 LLM et les 5 adversaires en version vague 4 contre `t1`, à 1e-12 près ; T exige `|chute_A|` < 0,005 pour les deux `B0` en version retest.
**T2** : `|rho_B|` de `B0 tirage [retest]` < 0,02 dans chaque rotation. **N** : `rho_B,r(retest)` ≥ 0,10 dans chaque rotation. **E** : `|E_r|` = 28, 27 et 33 exactement. **K** : masque du retest égal à celui de la vague 4.

## 9. Faisabilité, vérifiée par lecture du code et comptes de structure

- Les 7 LLM couvrent **168 768 cellules sur 168 768** du masque humain. Pas de valeur manquante de `S_gra` sur les 2 058 personnes. Le masque du retest est identique à celui de la vague 4 (0 cellule d'écart).
- `t1_baselines.calculer` rend des matrices (2 058, 108) en codes. Chaque ligne de test reçoit une prédiction pour chaque item où l'entraînement a au moins une réponse, c'est-à-dire les 108 items. La version retest existe déjà (`tab_evaluer._charger_twin_brut`, `adv6`).
- **Mêmes personnes, mêmes items pour les 10 candidats** : oui.
- **ρ_B** est calculable. `val_ord` et `est_ordinal` sont dans `paq`. La nomenclature commune compte plus de codes que le catalogue pour 12 items : 8 lignes `False Cons. self` (jusqu'à 9 codes pour 5 options), `Q174` à `Q176` et `Q192`. Les lignes gardent `val_ord` comme en v1 (non-linéarité déclarée). `Q192` porte un troisième code et sort de E_1.
- **chute_B** : calculable (`mesurer`, colonnes A et B interverties).
- **Cible (c)** : infaisable sur B3, retirée (§5).

## 10. Secondaires, aucune ne change l'issue

**S1** : adversaires en version vague 4 à la place des versions retest, règle entière, mêmes réplicats. **S2** : 8 candidats à contexte individuel seulement (sans `Demographics Only` ni `B1`), estimation ponctuelle. **S3** : ρ_B total, sans centrage de segment.
**S4** : par rotation, choix des 4 règles, part de coïncidence au bootstrap, τ de Kendall entre `exa_B` et `rho_B` sur les 10 candidats (diagnostic de non-réduction). **S5** : les deux `Persona Summary` (`exa_A`, `chute_A`, ρ_B, `perte_B`), hors de tout choix. **S6** : rappel et précision des raretés stables, rotations 1 et 2. **Pas de prédiction datée** : les quantités sur A se lisent dans les fichiers v1.

## 11. Limites

**L1** : test non aveugle (§0). **L2** : une seule ressource ; 10 candidats issus de deux familles de modèles de langage et de trois méthodes statistiques ; invites non observables, objet persona non certifié (audit R1 à R3). **L3** : l'asymétrie d'information des adversaires reste, amoindrie.
**L4** : ρ sur étiquettes dures pénalise les prédicteurs peu dispersés, et phi est borné par l'écart des marges. **L5** : les 19 items nominaux sont absents de la cible primaire. **L6** : mémorisation de Twin non contrôlée. **L7** : petites cellules `S_gra` (1 singleton, contribution nulle).

## 12. Plan d'implémentation, pour l'agent suivant

**Fichiers.** `analyses/tab2_evaluer.py` importe `tab_evaluer` **sans le modifier**, et `analyses/test_tab2_evaluer.py`. Sorties : `resultats/tab2-controles.csv`, `tab2-rotations.csv`, `tab2-bootstrap.csv`, `tab2-familles.csv`, `tab2-secondaires.csv`, puis le rapport `tab2-resultats.md`.

**À réutiliser.** Garde et chargement : `verifier_garde(chemin_go=GO_TAB2)`, `_charger_twin_brut` ; les versions retest entrent dans `d["configs"]` sous les noms suffixés `[retest]`, le retest humain dans `decrits`. Structure et mesures : `structure_partition`, `colonnes_rotations`, `verifier_rotation`, `lignes_perimetre`, `matrice_perte`, `preparer_tournoi`, `permutations_identites`, `mesurer`. Contrôles : `controles_structure`, `controle_temoin`, `controle_reproduction`. Bootstrap : `tirer_replicat` et la logique de coût de `bootstrap`. **Ne pas réutiliser** `selectionner`, `calculer_delta`, `regle_de_chute`, propres à v1.
**À ajouter.** `items_admissibles`, `rho_intra_segment` (pondérée, forme close), `rho_B` ; `rangs_moyens`, `choisir(mes, candidats, r, regle)` pour les quatre règles, sur A seul ; `delta_gamma`, `decision_tab2` (ordre du §7) ; `controles_tab2` (T2, N, E, K) ; `bootstrap_tab2`, `familles_tab2`, `secondaires_tab2`, `ecrire_sorties_tab2`, `executer`, `main`.

**Tests synthétiques exigés, sans lecture de Twin et sans GO-TAB2.** (1) ρ = 1 pour un prédicteur parfait, inchangé sous décalage de niveau alors que la perte change ; (2) ρ = 0 pour un prédicteur constant, ρ ≈ 0 pour un prédicteur qui ne connaît que le segment alors que ρ total est positif ; (3) poids entiers équivalents à la répétition des lignes et des colonnes ; (4) rangs moyens, départages, règle sous contrainte ; (5) Delta = Gamma = 0 exactement pour des choix identiques ; (6) table de vérité de `decision_tab2` : trois issues, ordre des conditions, chaque motif d'indécision ;
(7) modifier les prédictions sur B ne change aucun choix ; (8) garde absente ou SHA faux : refus avant toute lecture ; (9) bootstrap reproductible à graine fixe, règle de coût simulée ; (10) E exclut un item MC à 3 codes et garde une ligne binaire de matrice ; (11) N en échec donne l'indécision ; (12) `tab_evaluer.py` identique à son blob au commit `6accc1b`.

**Gel.** Le SHA du code et des tests est ajouté à cette page en addendum daté, commité avant que l'orchestrateur crée `data/traces/GO-TAB2`. L'agent d'implémentation ne crée pas ce fichier.
**Durée attendue.** Chargement et deux jeux d'adversaires : environ 5 min (5 plis à environ 29 s, deux fois). Bootstrap : 10 candidats au lieu de 7, cible en forme close. Total **30 à 60 min** en séquentiel ; v1 a pris environ 18 min de calcul (32 min entre le commit et les sorties).
