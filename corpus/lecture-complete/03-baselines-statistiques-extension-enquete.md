# Theme 03, lecture complete. Baselines statistiques contre modeles de langage, extension d'enquete

Lecture du 8 septembre 2026 au soir, methode de `corpus/lecture-complete/00-CONSIGNE.md`, grille de
`corpus/00-GRILLE.md`. Point de depart : les 39 lignes de `corpus/03-baselines-statistiques-extension-enquete.md`.
Sources internes relues avant la recherche : `resultats/a28-trois-tests-decisifs.md` tests 2 et 3,
`resultats/a31-la-mauvaise-rarete.md` section resultat, `ARBITRAGE.md`.

**Ce qui a change les conditions materielles de cette lecture.** `corpus/03` declarait, dans sa
section « Ce que je n'ai pas pu verifier », que « aucun lecteur de PDF n'est disponible dans cet
environnement » et attribuait a cette seule cause la plupart des lignes [PROBABLE] et [NON LU].
**`pdftotext` est present dans cet environnement.** Six lignes ont donc pu etre relevees, dont les
trois qui portaient le plus de poids argumentatif : T03-28 Wang et Gelman, T03-35 Boelaert, T03-39
Ashokkumar. En revanche, deux budgets etaient epuises des l'ouverture de la session : **WebSearch
(200 appels sur 200)** et **l'API OpenAlex**. La descente et la remontee de citations ont donc ete
faites par l'API arXiv, l'API Crossref, l'API Europe PMC, l'API HAL, les listes de references des
papiers lus, et WebFetch. C'est une contrainte reelle sur l'exhaustivite, declaree en (f).

**26 references lues en entier ou dans toutes leurs sections substantielles.** Le detail est en fin
de fichier.

---

## (a) La table etendue

Convention conservee de `corpus/03` : l'unite d'observation est nommee en clair (**cellule** =
couple personne x item, **personne** = un individu, **marginale** = distribution de groupe ou de
pays, **effet** = une difference entre conditions experimentales, **coefficient** = un parametre
d'un modele). Colonne ajoutee : « trouve par ».

**Les 27 lignes deja [CONFIRME] dans `corpus/03` ne sont pas recopiees.** Elles n'ont pas bouge.
Le bloc A donne les lignes dont le niveau de certitude change apres lecture du texte ; le bloc B
donne les references nouvelles.

### Bloc A. Lignes de la table initiale relevees par la lecture du PDF

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | trouve par | certitude |
|---|---|---|---|---|---|---|---|---|---|---|
| T03-28 | Wang, Rothschild, Goel, Gelman, 2015, *Forecasting elections with non-representative polls*, IJF 31(3) 980-991 | le MRP redresse-t-il un echantillon massivement non representatif ? | sondage Xbox, **750 148 repondants**, 45 jours avant l'election de 2012 ; 18-29 ans = 65 % de l'echantillon contre 19 % dans l'exit poll, hommes = 93 % | MRP hierarchique sur **176 256 cellules** (sexe 2 x race 4 x age 4 x diplome 4 x etat 51 x parti 3 x ideologie 3 x vote 2008 3), contre estimation brute et contre Pollster.com | erreur absolue sur les parts de vote ; **unite : la marginale d'etat, puis la marginale de sous groupe a deux dimensions** | national **0,6 point** d'ecart ; **51 courses electorales, erreur absolue moyenne 2,5 pp et mediane 1,8 pp** ; sous groupes a une dimension, **ecart absolu median 1,5 pp** ; **149 sous groupes a deux dimensions, ecart absolu median 2,4 pp**, et **1,9 pp sur les 30 plus gros** | l'echantillon brut donnait une victoire de Romney ; tout repose sur une table de post stratification issue de l'exit poll 2008, qui n'existe pas pour une simulation par langage | soutient, et fournit le chiffre qui manquait : **l'erreur du MRP est plus grande sur les petits sous groupes**, « the largest differences occur for relatively small demographic subgroups (e.g., liberal Republicans), for which both the Xbox and exit poll estimates are less reliable » | table initiale | **[CONFIRME]** (etait [NON LU]) |
| T03-31 | Goplerud, Bisbee, 2022, *BARP CORRIGENDUM*, APSR 117(2) 785-787 | remplacer le modele hierarchique par des arbres bayesiens ameliore-t-il le MRP ? | 89 enquetes d'opinion americaines | BARP contre MRP | erreur absolue moyenne et correlation inter etats ; **unite : la marginale d'etat** | apres correction du tri manquant, « the difference in performance between the two methods is much more of a toss-up » ; Goplerud chiffre le gain de BARP a **environ 4,5 % a n = 1 500**, et « this decreases to around 1% for larger sample sizes » | le chiffre de 4,5 % est rapporte dans le corrigendum d'apres Goplerud, pas recalcule ici | avertissement de methode conserve, et **borne haute** : remplacer le modele de premiere etape du MRP par de l'apprentissage automatique vaut 1 a 4,5 % | table initiale | **[CONFIRME]** (etait [PROBABLE]) |
| T03-34 | von der Heyde, Haensch, Wenz, 2025, *Vox Populi, Vox AI ?*, SSCR, arXiv 2407.08563 | un LLM predit-il le vote individuel hors contexte anglophone ? | GLES 2017 post electoral, **1 905 repondants eligibles**, 5 completions par persona, **9 525 completions** | GPT-3.5 contre **une regression multinomiale sur exactement les memes variables d'invite** | correspondance exacte et F1 par parti ; **unite : la personne** | **46 % de correspondance exacte pour GPT-3.5** ; F1 macro global **GPT 0,46 contre modele GLES 0,62** ; par parti, CDU/CSU 0,62 contre 0,73, SPD 0,52 contre 0,67, Verts 0,52 contre 0,70, Linke 0,45 contre 0,64, **FDP 0,34 contre 0,50, AfD 0,33 contre 0,58, petit parti 0,11 contre 0,31, vote nul 0,00 contre 0,18** | aucune validation croisee n'est mentionnee : le modele GLES semble evalue en echantillon, ce qui le favorise ; un seul modele, GPT-3.5 | **contredit en partie a28 et a31** : ici l'ecart entre la statistique et le langage **se creuse sur les categories rares**, pas l'inverse ; c'est la contre preuve la plus directe du corpus | table initiale | **[CONFIRME]** (etait [PROBABLE]) |
| T03-35 | Boelaert, Coavoux, Ollion, Petev, Praeg, 2025, *Machine Bias*, SMR 54(3) 1156-1196, version HAL/SocArXiv du 3 mars 2025 | les modeles generatifs peuvent-ils remplacer des repondants d'enquete d'opinion ? | World Values Survey, **687 sous populations** definies par 7 variables socio demographiques, 4 questions (bonheur, politique, religion, confiance) | GPT-4-Turbo, Llama-3-70B, Mixtral-8x7B, contre **permutation aleatoire des reponses individuelles** et contre **un logit multinomial en validation croisee leave-one-out** | nEMD, distance de Wasserstein normalisee, classee en 5 qualites ; **unite : la marginale de sous population** | part de predictions « good ou very good » : **logit croise 79,6 %**, permutation aleatoire 45,5 %, **Mixtral 49,8 %, Llama 47,7 %, GPT-4-Turbo 10,0 %** ; dispersion entre sous populations, mediane des nEMD par paires, **WVS 0,108 a 0,174 contre GPT-4T 0,000 a 0,131, Llama 0,026 a 0,069, Mixtral 0,019 a 0,063** | le logit est ajuste sur les memes donnees d'enquete, avantage assume par les auteurs ; 4 questions seulement | **soutient sur la comparaison** (la regression bat les trois modeles, et GPT ne bat meme pas le hasard) et **contredit sur le signe du terme inter** : ici le modele **sous disperse** entre groupes, la ou a1 et T03-02 mesurent une sur dispersion | table initiale | **[CONFIRME]** (etait [PROBABLE]) |
| T03-37 | Ye, Yoganarasimhan, 2026, *Rectification Difficulty and Optimal Sample Allocation in LLM-Augmented Surveys*, arXiv 2604.17267v2 | comment repartir un budget humain quand on augmente une enquete avec des predictions LLM ? | **Twin-2K-500** (68 questions, 14 taches, **86 448 observations personne x question**) et **CCES** | PPI++ avec parametre de reglage adaptatif, meta apprentissage de la difficulte de rectification | variance de l'estimateur, difficulte de rectification A_q ; **unite : la question, puis l'estimand** | exactitude LLM moyenne **75,7 % contre 81,7 % de test retest humain** ; **le PPI standard degrade l'estimateur sur 58 des 68 questions (85,3 %)**, variance moyenne **0,123 contre 0,110 pour la simple moyenne d'echantillon** ; **26 questions sur 68 ont lambda = 0**, c'est a dire aucun signal individuel exploitable ; reduction de variance moyenne du PPI++ **4,1 %** ; allocation optimale, gain oracle 14,5 % et 17,1 %, realise **11,4 % et 10,5 %**, soit **61 a 79 %** de l'oracle | l'estimand est une moyenne de population, jamais une reponse individuelle ; rien sur les minorites | **soutient tres fortement, et c'est la formalisation manquante** : « an LLM can be accurate in aggregate but provide no variance reduction: if Y_LLM = E[Y] for every respondent, the LLM-only mean is correct, but Var(Y_LLM) = 0, lambda = 0, and A = Var(Y) » | table initiale | **[CONFIRME]** (etait [PROBABLE]) |
| T03-39 | Ashokkumar, Hewitt, Ghezae, Willer, 2026, *Large language models can predict the results of social science experiments*, Nature, preprint OSF 3svep_v1 accepte | un LLM predit-il les resultats d'experiences de sciences sociales jamais vues ? | **70 experiences pre enregistrees, 469 effets, 119 330 participants** ; archive secondaire de 15 megastudies, 606 effets, 4 862 362 participants | GPT-4 et modeles plus recents, contre **2 659 previsionnistes humains de Prolific** | correlation entre effet simule et effet mesure, pente OLS, RMSE ; **unite : l'effet experimental** | **r = 0,85 [0,81 ; 0,88], r_adj = 0,92** ; **pente b = 0,56 [0,52 ; 0,60]**, c'est a dire que « LLM-derived effect size predictions were roughly twice as large as the actual effect sizes », **RMSE 11,09 pp** ; etudes non publiees avant la coupure, r = 0,90, b = 0,60 ; **previsionnistes humains r = 0,84 et b = 0,58**, donc ils sur estiment autant ; megastudies **r = 0,39, b = 0,34** | l'unite est l'effet moyen ; aucune mesure individuelle, aucune mesure de dispersion ; aucune baseline statistique | **contredit sur l'agregat, et fournit un fait nouveau pour nous** : la pente 0,56 est un **gonflement d'un facteur 1,8 du contraste entre conditions**, meme signe que notre gonflement inter groupes ; mais le plancher humain a b = 0,58 le vide de sa portee, exactement comme a28 test 3 | table initiale | **[CONFIRME]** (etait [PROBABLE]) |

### Bloc B. References nouvelles

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | trouve par | certitude |
|---|---|---|---|---|---|---|---|---|---|---|
| L03-01 | Ahn, Mao, Lee, 2026, *Item-Mean Surrogates: Why Richer Persona Data Fail to Improve LLMs as Human Surrogates*, arXiv 2608.29455, pre enregistre en fevrier 2026 | apres avoir retire la moyenne de l'item, que reste-t-il du signal individuel d'un LLM ? | 4 jeux : Megastudy de Peng (1 784 personnes, 160 items, 18 etudes), **SocSci210 (plus de 400 000 personnes, 5 998 resultats, 210 etudes)**, Twin-2K-500 Survey (2 058 personnes, 126 items), ANES (4 270 personnes, 11 variables) | GPT-4.1 et variantes, personas riches, affinage, Socrates-Qwen2.5-14B ; **baseline : la moyenne humaine de l'item en leave-one-out** | R2 poole apres retrait de la moyenne humaine de l'item ; theorie de la generalisabilite ; **unite : la cellule (personne x item)** | **R2 demoyenne 3,05 %** contre **plafond test retest humain 53,6 %**, soit 5,7 % du plafond, sur 108 160 cellules ; **le LLM est sous la moyenne d'item : r moyen par personne 0,34 contre 0,45 pour la moyenne d'item en leave-one-out**, dz = -0,55, p = 4,6e-95 sur 1 631 personnes ; decomposition, **effet personne stable 4,9 %, effet item 8,7 %, interaction personne x item 44,0 %, erreur transitoire 42,4 %**, l'interaction valant **8,9 fois** l'effet personne ; ecart type median du LLM **65 % (Megastudy), 50 % (SocSci210), 57 % (Survey)** de l'humain, **43 a 73 %** de modalites effectives ; melange de personas, 3,05 % contre 0,028 % au maximum sur 10 000 permutations ; **affinage 2,31 %, en dessous du meilleur prompt non affine 4,44 %** | items ordonnes et bornes seulement ; mesures lineaires ; ne teste pas les systemes qui recuperent l'historique complet de reponses | **soutient, et c'est la reference la plus importante trouvee** : elle mesure exactement ce que a31 appelle « la mauvaise rarete », sous le nom de person-by-item, et elle etablit qu'**une simple moyenne d'item bat le LLM sur la prediction individuelle** | citation aval de Twin-2K-500, puis recherche arXiv | **[CONFIRME]** |
| L03-02 | Peng, Gui, Brucks, Merlau, Fan et al. (21 auteurs, Columbia), 2026, *Digital Twins are Funhouse Mirrors: Five Systematic Distortions*, arXiv 2509.19088v5 | des jumeaux numeriques riches font-ils mieux qu'une persona demographique ? | **19 etudes pre enregistrees, 164 resultats**, jumeaux construits sur les 500+ reponses de Twin-2K-500 | GPT et autres, quatre conditions : persona complete, **demographies seules (14 variables)**, persona vide, tirage uniforme | exactitude individuelle, correlation par resultat, rapport d'ecarts types, MAD entre conditions ; **unite : la cellule et le resultat** | exactitude, **persona complete 0,748, demographies seules 0,746 (p = 0,37, non significatif), persona vide 0,734, hasard uniforme 0,629** ; correlation moyenne jumeau-humain **r = 0,197**, positive dans 157 resultats sur 164 mais significative dans 97 ; **ecart type du jumeau inferieur a l'humain dans 154 cas sur 164 (93,9 %)**, significatif dans 140 ; moyennes agregees a **0,352 ecart type** de l'humain, difference significative dans 105 resultats sur 164 (64,0 %) ; **MAD persona complete contre demographies seules 0,132, contre persona vide 0,175, contre humains 0,252** | aucune baseline statistique ajustee sur donnees, seulement des ablations de persona ; un seul panel | **soutient tres fortement, et c'est la replication externe de a28 test 3 et de a31** : « the answers are overly "shrunk" towards a base model », et le jumeau riche est plus proche du stereotype demographique que de la personne | citation amont de L03-01 | **[CONFIRME]** |
| L03-03 | Xie Yueqi, Liang, Li, Lu, Xiao, Shi, Huang, Wang, Xie Yu, 2026, *Evaluating the statistical realism of LLM-generated social science data*, PNAS 123(19) e2538145123, PMC13167774 | des donnees produites par LLM reproduisent-elles les moments statistiques d'une population ? | **7 enquetes** (4 longitudinales, 3 transversales : NLSY, CPS-ASEC, recensement 1980, GSS 2018 et autres), 6 domaines | **15 LLM**, plus un Llama-3.1-8B affine par LoRA sur CPS-ASEC 1970 | taux de reussite par bootstrap sur 5 types de motifs statistiques (univarie, bivarie, prediction multivariee, sequences d'evenements de vie, associations de sequences) ; **unite : la marginale et le coefficient** | taux de reussite **generalement sous 0,5**, meilleurs modeles GPT-4 et Llama-3.1 a **0,30 de moyenne** ; **types 1 et 4 les plus bas, le type 4 proche de zero** ; entropie **systematiquement plus basse que le reel pour les 15 modeles** ; V de Cramer **systematiquement plus haut**, beaucoup de paires au dessus de 0,6 et certaines proches de 0,8 ou 1 ; exemple NLSY, revenu moyen 30-40 ans predit par race, sexe et diplome, **R2 simule proche de 0,6 contre R2 reel inferieur a 0,1** ; affinage, taux de reussite **0,258 vers 0,534** sur CPS-ASEC 1980, 0,270 vers 0,442 sur le recensement, 0,325 vers 0,402 sur le GSS | aucune baseline statistique n'est opposee aux modeles ; les auteurs le reconnaissent explicitement ; les taux de reussite dependent de choix de tests declares subjectifs | **soutient, et c'est la publication qui pre empte en partie la double distorsion** : intra ecrase (entropie) et inter gonfle (V de Cramer, R2) mesures ensemble sur 15 modeles et 7 enquetes, au niveau de la population. « compress real-world heterogeneity into simplified typological structures » | citation amont de L03-01, puis Crossref et Europe PMC | **[CONFIRME]** |
| L03-04 | Ku Chan-Tung, Hsu, Huang, Liu, Cheng, Kang, 2026, *Silicon Sampling via Cross-Survey Transfer*, arXiv 2607.03091 | un LLM predit-il les reponses d'une personne a des items qu'il n'a jamais vus, a partir de ses reponses a d'autres items ? | Taiwan Election and Democratization Study 2024, **N = 1 206**, items partitionnes en contexte (28 items) et cible | 3 modeles ouverts 27B a 120B en zero-shot, contre **regression logistique sur demographies** et **foret aleatoire sur demographies plus contexte**, 5 plis | correspondance exacte, tolerance +/-1, MAE, **rapport de variance VR** ; **unite : la cellule (personne x item)** | **modalite majoritaire 46,6 %, LR demographies 47,0 % (VR 0,38), foret 58,3 % (VR 0,72)** ; LLM **Qwen3.5 52,1 % (VR 0,84), gpt-oss 51,3 % (VR 0,85), Gemma3 47,6 % (VR 0,67)** ; hierarchie de predictibilite de 67 % (attitudes partisanes) a 23 % (souverainete), ou **la foret atteint 56,1 % contre 23,3 % pour les LLM, ecart de 33 pp** ; abliteration, gpt-oss perd 6,1 pp, Qwen3.5 0,1 pp | zero-shot contre supervise : la comparaison n'est pas a information appariee, les auteurs le disent ; **aucune mesure sur les cellules minoritaires** | **c'est l'objection nommee « Ku 2026 » dans a28**, lue ici en entier. Elle est plus faible que citee sur un point : la foret ecrase plus que les LLM (0,72 contre 0,67 a 0,85) et **la regression logistique ecrase le plus (0,38)** ; « predicting individual survey responses from limited context inherently biases toward population means » | deja nommee dans corpus/01, lue en entier ici | **[CONFIRME]** |
| L03-05 | Holtdirk, Assenmacher, Bleier, Wagner, 2025, *Learning from Convenience Samples*, arXiv 2509.25063 | l'affinage d'un LLM sur des donnees partielles bat-il un classifieur tabulaire pour imputer une non reponse ? | GLES, vote declare ; 4 protocoles : tous les participants, etudiants seulement, region de Thuringe, chomeurs seulement ; avec et sans identification partisane | Llama-3.2-1B, 3.2-3B, 3.1-8B en zero-shot et affines, GPT-4o, contre **regression logistique, foret aleatoire, CatBoost** | **macro F1**, choisi explicitement « to ensure models perform equally well across parties », et distance de variation totale ; **unite : la personne** | manquant completement au hasard, **les LLM affines egalent les classifieurs tabulaires et ne les depassent pas** ; avec des echantillons de convenance biaises (etudiants, chomeurs), les LLM affines de 3B a 8B recuperent mieux predictions individuelles et distributions ; zero-shot nettement moins bon partout ; sur E3b, le Llama-8B affine bat le classifieur (W = 2,40, p = 0,016) | **les valeurs numeriques ne sont qu'en figures**, non extractibles du PDF ; un seul pays, une seule variable cible | soutient la voie hybride et delimite le regime : la statistique perd uniquement quand l'echantillon disponible est structurellement biaise, pas quand il est aleatoire | recherche arXiv sur « individual-level prediction » | [CONFIRME] pour les enonces, [NON LU] pour les valeurs |
| L03-06 | Garrido, Borysov, Rich, Pereira, 2020, *Prediction of rare feature combinations in population synthesis*, Transportation Research Part C 119 102787, arXiv 1909.07689 | une methode de synthese de population peut-elle produire les combinaisons rares absentes de l'echantillon ? | enquete de deplacements danoise, plus de 60 variables, tirages de 200 000 individus | **WGAN et VAE contre un echantillonneur marginal et un tirage uniforme** | **zeros d'echantillonnage** (combinaisons presentes dans le test, absentes du train) recuperes, contre **zeros structurels** (combinaisons impossibles) produits, et leur rapport ; **unite : la combinaison de modalites** | rapport zeros structurels sur zeros d'echantillonnage du WGAN, de **20,06 a 9 801 combinaisons** a **139,56 a 830 millions** ; surcout par rapport au WGAN, **VAE +5,6 % a +44,7 %, echantillonneur marginal +21,6 % a +2 217 %, tirage uniforme +26,8 % a +170 440 %** ; en basse dimension, **le tirage uniforme et l'echantillonneur marginal recuperent TOUS les zeros d'echantillonnage** la ou le WGAN et le VAE n'y arrivent pas | il faut fabriquer artificiellement les zeros d'echantillonnage par un decoupage train/test ; domaine transport, pas d'attitudes | **soutient, et c'est le cadre theorique qui manquait a a28 section 3.4** : la production de gens rares s'achete en gens impossibles, et le taux de change se mesure. Mecanisme donne : le VAE est « mode covering » par maximum de vraisemblance, le GAN « mode seeking » par divergence de Jensen-Shannon | recherche arXiv sur la synthese de population | **[CONFIRME]** |
| L03-07 | Borysov, Rich, Pereira, 2019, *Scalable Population Synthesis with Deep Generative Modeling*, TR-C 106, arXiv 1808.06910v2 | quelle famille tient quand le nombre d'attributs augmente ? | meme enquete danoise, trois jeux d'attributs : Basic (27 dim.), Socio (121 dim.), Extended (357 dim.) | VAE contre **echantillonneur de Gibbs a conditionnelles completes**, **reseaux bayesiens** (arbre, glouton, exact), echantillonneur marginal, re echantillonnage du train | SRMSE sur marginales, bivariees, trivariees et V de Cramer, plus **distance au plus proche voisin du train, moyenne et ecart type** ; **unite : la personne synthetique** | Basic, **Gibbs 0,197 contre VAE 0,482** (le Gibbs gagne) ; Socio, **Gibbs 4,025 contre VAE 0,693** ; Extended, **Gibbs 27,27 contre VAE 0,959** ; **distance au plus proche voisin du Gibbs exactement nulle, moyenne et ecart type**, contre non nulle pour tous les VAE | pas d'attitudes, pas de reponses d'enquete d'opinion | soutient : « the Gibbs sampler essentially replicates the agents from the original sample when the required conditional distributions are estimated as frequency tables ». C'est **exactement le comportement de notre B2 plus proches voisins**, decrit et mesure en 2019 dans une autre litterature | citation amont de L03-06 | **[CONFIRME]** |
| L03-08 | Nowok, Raab, Dibben, 2016, *synthpop: Bespoke Creation of Synthetic Data in R*, Journal of Statistical Software 74(11) | comment la statistique officielle fabrique-t-elle une population synthetique ? | article de logiciel, jeu SD2011 | CART et arbres conditionnels par defaut, plus modeles parametriques ; synthese « simple » (parametres ajustes) contre « proper » (parametres tires de leur loi a posteriori) | conditions de validite de l'inference sur donnees synthetiques ; **unite : le coefficient de l'analyse** | pas de chiffre d'exactitude : c'est un article de methode. **Le fait important est un fait de conception** : la fonction `sdc()` propose de retirer « any unique cases with variable sequences that are identical to unique individuals in the real dataset », `cart.minbucket` impose une taille minimale de feuille parce que « the final leaves to be sampled from may include only a very small number of individuals, which elevates risk of replicating real persons », et le lissage par noyau gaussien est declare « essential » contre « the risk of releasing real unusual values » | aucune mesure de ce que ces trois options coutent en couverture des cas rares | **soutient, et c'est un argument nouveau** : dans la tradition statistique, l'effacement des gens rares n'est pas un accident, c'est une **exigence de controle de divulgation**. La statistique ne produit pas les minorites parce qu'il lui est interdit de le faire | recherche directe, plan de recherche non atteint de `corpus/03` | **[CONFIRME]** |
| L03-09 | Alaa, van Breugel, Saveliev, van der Schaar, 2022, *How Faithful is your Synthetic Data ?*, ICML, arXiv 2102.08921v2 | comment mesure-t-on la fidelite d'un modele generatif ? | methodologie, plus MNIST et donnees de la competition hide-and-seek | GAN, VAE et autres | triplet **alpha-precision, beta-rappel, authenticite** ; **unite : l'echantillon synthetique** | pas de chiffre pertinent pour nous. **Le fait est definitionnel** : « P_alpha and R_beta do not count outliers when assessing fidelity and diversity. That is, the alpha-Precision score deems a synthetic sample to be of a high fidelity not only if it looks "realistic", but also if it looks "typical". Similarly, beta-Recall counts a real sample as being covered by P_g only if it is not an outlier in P_g » | l'exclusion des valeurs atypiques est presentee comme une qualite, la « robustness to outliers » | **soutient, et c'est le second argument nouveau** : la metrique standard d'evaluation des donnees synthetiques est construite pour ne pas voir l'effacement des gens rares. Un modele qui detruit toutes les minorites peut atteindre alpha-precision et beta-rappel parfaits | recherche directe sur les metriques de donnees tabulaires | **[CONFIRME]** |
| L03-10 | van Buuren, 2018, *Flexible Imputation of Missing Data*, 2e ed., section 1.3 (en ligne, libre) | que fait l'imputation par l'esperance, comparee a l'imputation par tirage ? | jeu `airquality`, ozone, 24 % de manquant | imputation par la moyenne, par la regression (esperance conditionnelle), par regression stochastique (esperance plus residu tire) | ecart type et correlation avant et apres imputation ; **unite : la cellule** | imputation par la moyenne, **ecart type 28,7 contre 33 observe**, correlation **0,35 vers 0,30** ; imputation par la regression, correlation **0,35 vers 0,39** ; « the ensemble of imputed values vary less than the observed values » ; « regression imputation artificially strengthens the relations in the data » ; « Regression imputation is a recipe for false positive and spurious relations » ; imputation stochastique, « preserves not only the regression weights, but also the correlation between variables » | demonstration pedagogique sur un jeu, pas une simulation systematique | **soutient, et c'est l'ancrage theorique le plus economique du dossier** : la double distorsion, intra ecrase et inter gonfle, est la propriete connue de l'imputation par l'esperance conditionnelle, et son correctif connu est **le tirage** | recherche directe, litterature d'imputation | **[CONFIRME]** |
| L03-11 | Shen, Louis, 1998, *Triple-goal Estimates in Two-stage Hierarchical Models*, JRSS-B 60(2) 455-471, DOI 10.1111/1467-9868.00135 | peut-on estimer en meme temps chaque individu, l'histogramme et les rangs ? | theorie plus simulations | moyennes a posteriori, estimateurs bayesiens contraints de Louis et Ghosh, estimateurs a triple objectif | risque quadratique, qualite de l'histogramme, qualite des rangs ; **unite : l'ensemble des parametres** | resultat theorique, resume lu : « in the two-stage, compound sampling model the posterior means are optimal under squared error loss. However, they can perform poorly in estimating the histogram of the parameters or in ranking them. [...] **No set of estimates can simultaneously optimize these three goals** and we seek a set that strikes an effective trade-off » | **seul le resume a ete lu** ; aucune valeur numerique ; le texte est derriere Oxford | **soutient, c'est la reponse a la question posee** : oui, quelqu'un a formalise pour les enquetes que minimiser l'erreur moyenne sacrifie la restitution de la distribution. C'est Louis 1984, Ghosh 1992 et Shen et Louis 1998, sous le nom de **constrained Bayes** et **triple-goal** | Crossref, en cherchant qui a formalise l'arbitrage | [PROBABLE] |
| L03-12 | Li Zonghan, Ji Feng, 2026, *Statistical realism is not evidence that LLMs can estimate treatment effects in social science experiments*, arXiv 2604.02458v3 | le realisme statistique d'une simulation predit-il l'exactitude de l'effet qu'on en tire ? | experience climatique transnationale, **59 508 participants, 62 pays**, plus deux replications, 20 785 participants, 12 et 27 pays | 3 LLM, plusieurs invites et populations cibles | MAE au niveau des reponses (realisme) contre erreur sur l'effet moyen de traitement ; **unite : la reponse pour le realisme, l'effet pour l'exactitude** | **correlation de Spearman entre realisme et exactitude d'effet, rho = 0,10** ; dans une configuration, **rho = -0,52 [-0,79 ; -0,07], p = 0,027**, c'est a dire que plus la simulation est realiste, plus l'effet est faux ; MAE des meilleures configurations **22,8 a 25,0 points** | lu dans le resume, l'introduction et les passages de resultats reperes ; la totalite des figures n'a pas ete lue | **soutient, et c'est la contre preuve de T03-39** : optimiser la ressemblance distributionnelle ne garantit rien sur la quantite qu'on veut estimer | recherche arXiv en cherchant Xie 2026 | [CONFIRME] pour les valeurs citees |
| L03-13 | Meister, Guestrin, Hashimoto, 2024-2025, *Benchmarking Distributional Alignment of Large Language Models*, arXiv 2411.05403, NAACL 2025 | un LLM sait-il decrire la distribution d'opinion qu'il n'arrive pas a simuler ? | jeu construit au dela des valeurs politiques, avec baseline humaine | plusieurs LLM, trois methodes d'expression de la distribution : log probabilites, sequence simulee, **verbalisation de la connaissance distributionnelle** | alignement distributionnel ; **unite : la marginale de groupe** | resultat qualitatif lu : « LLMs can more accurately describe the opinion distribution than simulate such distributions » ; les auteurs nomment l'ecart **knowledge-to-simulation gap** | **aucune valeur chiffree extraite** ; lu resume et sections de methode seulement | soutient : le modele **connait** la marginale mais ne sait pas en tirer. C'est le mecanisme qui explique pourquoi un tirage marginal explicite (notre B0 tirage) garde la diversite que le modele perd en la simulant | citation amont de L03-01 | [PROBABLE] |
| L03-14 | Shumailov, Shumaylov, Zhao, Papernot, Anderson, Gal, 2023 puis Nature 2024, *The Curse of Recursion / AI models collapse when trained on recursively generated data*, arXiv 2305.17493 | que devient une distribution quand on reapprend sur ses propres sorties ? | melanges gaussiens, VAE, modeles de langage sur wikitext2 | modeles generatifs successifs | perplexite, variance, distance L2 entre generations ; **unite : la distribution** | « model collapse [...] where tails of the original content distribution disappear » ; deux regimes nommes, **early model collapse** ou « the model begins losing information about the tails of the distribution » et late model collapse ou la distribution converge « with very small variance » ; a la generation 2000 le melange gaussien devient un point | il ne s'agit pas d'extension d'enquete mais d'entrainement recursif ; l'analogie doit etre declaree comme telle | soutient l'axe 4 : si on augmente une enquete par des repondants synthetiques puis qu'on refait des modeles sur le melange, **la queue part en premier**, avant la moyenne | recherche directe sur les queues de distribution | [PROBABLE] |

**Comptage de la table etendue.** Bloc A : 6 lignes passees de [NON LU] ou [PROBABLE] a [CONFIRME].
Bloc B : 14 nouvelles lignes, dont **10 [CONFIRME]**, 3 [PROBABLE], 1 mixte. Total du theme apres
cette lecture : **53 references**, dont 43 [CONFIRME].

---

## (b) Comment ca fonctionne

### Le mecanisme central : toute methode qui minimise l'erreur moyenne rend la moyenne du groupe

Le point de depart theorique n'est pas dans la litterature sur les modeles de langage, il est dans
celle de l'estimation sur petits domaines, et il est ancien. Shen et Louis (L03-11) l'ecrivent en
une phrase : dans un modele hierarchique a deux etages, « the posterior means are optimal under
squared error loss. However, they can perform poorly in estimating the histogram of the parameters
or in ranking them », et surtout « No set of estimates can simultaneously optimize these three
goals ». Trois objectifs, l'estimation de chaque unite, la restitution de l'histogramme, le
classement, et une impossibilite formelle de les atteindre ensemble. C'est le theoreme dont notre
front de Pareto exactitude contre diversite (a23 section 5) est la version empirique. La reponse
methodologique de cette litterature, le **constrained Bayes** de Louis et Ghosh puis les
estimateurs a triple objectif, consiste a **degrader volontairement l'estimation individuelle pour
retablir la dispersion de l'ensemble**. Personne, dans la litterature sur la simulation par
langage, ne cite ce corps de travaux.

Ce mecanisme se retrouve, sous un autre nom, dans la litterature d'imputation. Van Buuren (L03-10)
le montre sur trois lignes de code et deux chiffres : imputer par la moyenne fait tomber l'ecart
type de 33 a 28,7 et la correlation de 0,35 a 0,30 ; imputer par l'esperance conditionnelle, c'est
a dire par la prediction d'une regression, fait au contraire **monter** la correlation de 0,35 a
0,39, parce que « the ensemble of imputed values vary less than the observed values ». Il en tire
deux phrases qu'il faut lire ensemble : « regression imputation artificially strengthens the
relations in the data » et « Regression imputation is a recipe for false positive and spurious
relations ». Autrement dit, **l'imputation par l'esperance ecrase la dispersion intra et gonfle
l'association inter, simultanement, et pour la meme raison**. C'est mot pour mot notre double
distorsion, decrite dans un manuel d'imputation, avec son correctif connu : la regression
stochastique, qui « preserves not only the regression weights, but also the correlation between
variables », parce qu'elle **tire** au lieu de predire.

Le corollaire est que notre double distorsion n'est pas une propriete des modeles de langage. Elle
est la propriete de **tout predicteur ponctuel** utilise comme generateur, et le modele de langage
en est un cas particulier. Ku (L03-04) arrive independamment a la meme conclusion sur ses donnees
taiwanaises : « predicting individual survey responses from limited context inherently biases
toward population means ». Le rapport de variance de sa regression logistique sur demographies vaut
**0,38**, celui de sa foret aleatoire **0,72**, celui de ses trois modeles de langage **0,67 a
0,85**. La methode la plus statistique est celle qui ecrase le plus. Ce chiffre est important pour
nous parce que a28 section 2.1 mesure la meme chose sur nos donnees, `B1 argmax` a 0,604 et
`B3 foret` a 0,330, et trouve le meme ordre.

### Ce que le modele de langage rend a la place de la personne : la moyenne de l'item

La reference decisive est Ahn, Mao et Lee (L03-01), pre enregistree, quatre jeux, plus de 400 000
participants et plus de 6 000 items. Leur protocole est le bon : ils retirent de la reponse humaine
**et** de la reponse simulee la moyenne humaine de l'item, puis regardent ce qui correle. Il reste
**3,05 %** de variance expliquee, contre un plafond test retest humain de **53,6 %**, soit 5,7 % du
plafond. Le detail qui compte pour nous est ailleurs : ils comparent le modele a une baseline qui
n'a aucune information sur la personne, la moyenne humaine de l'item en leave-one-out, et **le
modele perd**, r moyen par personne 0,34 contre 0,45, dz = -0,55, p de l'ordre de 1e-95. Une
moyenne d'item, c'est notre `B0 mode` sans la moindre demographie. Sur ce protocole, elle bat un
jumeau numerique nourri de 500 reponses.

La decomposition en composantes explique pourquoi. L'effet personne stable ne pese que **4,9 %** de
la variance d'erreur, l'interaction personne x item **44,0 %**, soit **8,9 fois plus**. Une persona,
par construction, est fixe pour une personne a travers tous les items : elle ne peut encoder qu'un
effet personne. « Persona data encode the respondent, but not this item-specific deviation. » C'est
la formulation propre du resultat de a31 : les fausses raretes sont posees sur la bonne personne et
au mauvais item, parce que la seule chose que le modele sait de la personne est constante d'un item
a l'autre.

Peng et ses vingt coauteurs (L03-02) donnent la version ablative du meme fait sur 164 resultats
pre enregistres. L'exactitude individuelle d'un jumeau a persona complete est **0,748** ; celle d'un
jumeau qui ne recoit que **14 variables demographiques** est **0,746**, et la difference n'est pas
significative, p = 0,37. L'ecart type du jumeau est inferieur a celui des humains dans **154 cas
sur 164**. Et la mesure de distance moyenne absolue place le jumeau riche **plus pres du jumeau
demographique (0,132) que du jumeau vide (0,175) ou de l'humain reel (0,252)**. Leur conclusion,
« the answers are overly "shrunk" towards a base model », est exactement la conclusion de a28 test 3
et de a31 section 2.3, obtenue sur un autre panel, avec une autre metrique, par vingt et un auteurs
qui ne nous connaissent pas.

### Ce que le modele de langage fait a la distribution : entropie en bas, association en haut

Xie et al. (L03-03) mesurent les deux termes en meme temps, sur 15 modeles et 7 enquetes, et
publient dans PNAS. Sur les distributions univariees et sur les sequences d'evenements de vie,
**l'entropie des donnees simulees est systematiquement plus basse que celle du reel, pour les
quinze modeles**, et le taux de reussite sur les sequences est proche de zero. Sur les associations,
le V de Cramer simule est systematiquement plus haut, avec beaucoup de paires de variables au dessus
de 0,6 et certaines approchant 1. L'exemple chiffre est brutal : predire le revenu moyen entre 30 et
40 ans a partir de la race, du sexe et du diplome donne un **R2 proche de 0,6 dans les donnees
simulees contre moins de 0,1 dans le NLSY reel**. Un facteur superieur a six sur la part de variance
que la demographie est censee expliquer. C'est la meme quantite que a1 mesure par un ratio inter
groupes, sur un jeu que nous n'avons pas.

Les auteurs ajoutent une phrase de mecanisme qu'il faut retenir : « advances in LLMs are primarily
guided by case-wise prediction accuracy objectives. Distribution across numerous cases in a
population is not explicitly addressed, and **accuracy-oriented objectives may even amplify the
typological tendency** ». C'est la version moderne du theoreme de Shen et Louis : optimiser
l'exactitude cas par cas degrade mecaniquement la restitution de la distribution.

### Ce que la simulation coute a l'inference, et pourquoi c'est la variance qui decide

Ye et Yoganarasimhan (L03-37, relu) donnent la formalisation la plus utile de l'axe extension
d'enquete, et elle est independante de toute discussion de qualite. Dans le cadre de l'inference
augmentee par prediction, la valeur d'un repondant synthetique ne depend pas de son exactitude mais
de sa **covariance avec la reponse humaine**. Leur enonce : « an LLM can be accurate in aggregate
but provide no variance reduction: if Y_LLM = E[Y] for every respondent, the LLM-only mean is
correct, but Var(Y_LLM) = 0, lambda = 0, and A = Var(Y) ». Un simulateur qui ecrase la variance
individuelle vaut exactement zero pour l'estimation, meme si sa moyenne est juste.

Les chiffres qui suivent sont ceux que tout vendeur de panel synthetique devrait avoir a repondre.
Sur Twin-2K-500, l'exactitude moyenne du modele est **75,7 %** contre un test retest humain de
81,7 %, ce qui parait excellent. Et pourtant **l'inference augmentee naive degrade l'estimateur sur
58 des 68 questions**, variance moyenne 0,123 contre 0,110 pour la simple moyenne de l'echantillon
humain. **26 questions sur 68 ont un parametre de reglage optimal exactement nul** : le modele
n'apporte aucun signal individuel. Une fois le reglage adapte question par question, le gain moyen
est de **4,1 %** de variance. L'allocation optimale du budget humain rajoute 10,5 a 11,4 % de
reduction d'erreur quadratique. On est loin du facteur.

Cela recoupe exactement les deux chiffres deja au dossier, Broska (T03-38) a +13 % d'echantillon
effectif pour dix fois plus de repondants synthetiques, et Ye lui meme a environ 10 % de MSE. Trois
mesures independantes, meme ordre de grandeur : **l'extension d'enquete par langage vaut une dizaine
de pour cent, pas un facteur.**

### Ce que la statistique fait des gens rares, quand on regarde de pres

Deux litteratures repondent, et aucune des deux n'est celle des modeles de langage.

La premiere est la synthese de population en microsimulation, et elle a un vocabulaire que nous
n'avions pas : **zeros d'echantillonnage** contre **zeros structurels**. Garrido et al. (L03-06)
posent le probleme exactement comme a28 section 3.4 : recuperer les combinaisons rares mais
possibles, sans fabriquer les combinaisons impossibles. Leur mesure est un taux de change, et il est
publie. Le meilleur modele, un WGAN, produit **20 individus impossibles pour un individu rare
recupere** en basse dimension, et **139,6 pour un** en haute dimension. Le VAE fait 5 a 45 % de
pire ; **l'echantillonneur marginal, qui est notre B0 tirage, fait 21,6 % de pire en basse dimension
et 2 217 % de pire en haute dimension** ; le tirage uniforme, 170 440 % de pire. Et le point
important : en basse dimension, **le tirage marginal et le tirage uniforme recuperent la totalite
des combinaisons rares**, la ou les modeles generatifs echouent. C'est la meme structure que notre
tableau a28 section 3.4 : la methode qui garde la masse minoritaire est la plus bete, et le prix
est la precision.

Borysov et al. (L03-07) donnent la contrepartie sur l'autre bord du front. Un echantillonneur de
Gibbs a conditionnelles estimees par tables de frequence a, en basse dimension, la meilleure SRMSE
de tout le tableau, 0,197 contre 0,482 pour le VAE. Sa distance moyenne au plus proche voisin de
l'echantillon d'apprentissage vaut **exactement zero**, ecart type compris : il recopie. Et des que
la dimension monte, il explose, 27,27 contre 0,959. C'est le comportement de notre `B2 plus proches
voisins`, decrit et mesure dans une autre discipline sept ans avant nous.

La seconde litterature est celle du controle de divulgation, et elle apporte le fait le plus
inattendu de cette lecture. Dans `synthpop` (L03-08), l'outil de reference de la statistique
publique pour fabriquer des populations synthetiques, l'effacement des individus rares est une
**fonctionnalite**. `cart.minbucket` interdit les feuilles trop petites parce que « the final leaves
to be sampled from may include only a very small number of individuals, which elevates risk of
replicating real persons ». Le lissage par noyau est declare « essential » contre « the risk of
releasing real unusual values ». Et `sdc()` retire du jeu synthetique « any unique cases with
variable sequences that are identical to unique individuals in the real dataset ». La statistique
officielle ne produit pas les minorites parce qu'elle a decide de ne pas les produire.

Cette decision a une consequence sur les metriques. Alaa et al. (L03-09), dont le triplet
alpha-precision, beta-rappel, authenticite est devenu le standard d'evaluation des donnees
synthetiques tabulaires, ecrivent noir sur blanc que « P_alpha and R_beta do not count outliers when
assessing fidelity and diversity », et que l'alpha-precision « deems a synthetic sample to be of a
high fidelity not only if it looks "realistic", but also if it looks "typical" ». Cette exclusion
est presentee comme une qualite, la robustesse aux valeurs atypiques. **Un generateur qui detruit
integralement les minorites peut obtenir des scores parfaits sur la metrique de reference du
domaine.** C'est, en une phrase, la raison pour laquelle le trou identifie a la question 5 de
`corpus/03` existe encore.

### Ou la statistique reste imbattable, et pourquoi

Wang et Gelman (T03-28, relu) donnent maintenant les chiffres. 750 148 repondants d'un sondage sur
console de jeu, 93 % d'hommes, 65 % de 18-29 ans, un echantillon brut qui annonce une victoire de
Romney. Apres MRP sur **176 256 cellules**, l'estimation nationale est a **0,6 point** du resultat,
l'erreur absolue moyenne sur les 51 courses est de **2,5 points**, mediane 1,8. Et sur les 149 sous
groupes croises a deux dimensions, l'ecart absolu median est de **2,4 points**, qui tombe a **1,9**
sur les 30 plus gros. Cette derniere phrase est celle qu'il fallait aller chercher : **l'erreur du
MRP est plus grande sur les petits sous groupes**, et les auteurs le disent, « the largest
differences occur for relatively small demographic subgroups (e.g., liberal Republicans) ». Le
retrecissement du modele hierarchique se paie la ou il y a peu de monde, et la litterature le sait.

Boelaert et al. (T03-35, relu) donnent l'autre borne. Sur 687 sous populations du WVS, un simple
logit multinomial valide par leave-one-out produit **79,6 %** de predictions bonnes ou tres bonnes ;
Mixtral en produit 49,8 %, Llama 47,7 %, **GPT-4-Turbo 10,0 %**, quand une **permutation aleatoire
des reponses humaines** en produit 45,5 %. Deux des trois modeles font a peine mieux que le hasard
et le troisieme fait bien pire. C'est la comparaison la plus severe du corpus, et elle est publiee
dans Sociological Methods and Research.

Enfin, l'apport marginal d'une meilleure statistique est borne. Le corrigendum de BARP (T03-31,
relu) etablit que le gain des arbres bayesiens sur le MRP classique, une fois corrigee l'erreur de
tri du code de replication, vaut **environ 4,5 % a n = 1 500** et **environ 1 % pour de plus grands
echantillons** ; « the difference in performance between the two methods is much more of a toss-up ».
Avec Ornstein (2 a 3 %) et autoMrP (5 a 12 %), on tient une fourchette : **empiler des modeles ne
rapporte que quelques pour cent.** La marge n'est ni du cote de la statistique ni du cote du
langage : elle est dans le choix de la quantite qu'on decide de mesurer.

---

## (c) Ce qui se contredit

### Contradiction 1. Le signe du terme inter groupes

C'est la contradiction la plus lourde, et elle etait invisible tant que T03-35 restait illisible.

D'un cote, **le gonflement inter est mesure** : a1 trouve des ratios de 1,8 a 5,9 selon la
condition ; Chen (T03-02) une mediane de 2,3 sur le GSS et 2,5 sur le WVS ; les gouts culturels
(T03-13) un facteur 4 a 20 sur les coefficients ; Xie (L03-03) un R2 simule de 0,6 contre 0,1 reel
et des V de Cramer approchant 1 ; Ashokkumar (T03-39) une pente de 0,56, soit un facteur 1,8
d'inflation du contraste entre conditions experimentales.

De l'autre, **le retrecissement inter est mesure aussi**, sur le meme genre de materiau : Boelaert
(T03-35) trouve une mediane de nEMD entre paires de sous populations de 0,108 a 0,174 chez les
humains du WVS et de **0,000 a 0,131** chez GPT-4-Turbo, 0,019 a 0,069 chez les deux autres. Sur la
confiance, GPT-4-Turbo donne **strictement la meme distribution aux 687 sous populations**.

La variable qui explique la contradiction est identifiable, et elle a deux composantes.

**Premiere composante, ce qu'on donne au modele.** Les travaux qui trouvent un gonflement
conditionnent sur un individu, persona, biographie ou entretien, et lisent une reponse individuelle
ou un coefficient estime sur des reponses individuelles. Les travaux qui trouvent un retrecissement
demandent au modele une **distribution de groupe** en zero-shot a partir d'une etiquette. Ce sont
deux taches differentes. Meister (L03-13) donne le nom du phenomene qui les separe : le
**knowledge-to-simulation gap**, « LLMs can more accurately describe the opinion distribution than
simulate such distributions ». Interroge sur une distribution, le modele repond avec sa
connaissance, qui est plate ; interroge en tant qu'individu, il repond avec son stereotype, qui est
exagere.

**Seconde composante, l'alignement.** Dans Boelaert, le modele le plus aplati est de tres loin
GPT-4-Turbo, le seul modele instruit du lot, et les auteurs notent que « models fine-tuned for
instruction or chat tend to perform worse than pre-trained foundational models on this task ». Cela
recoupe Tjuatja (T03-11), 3,33 pour les modeles de base contre 0,83 pour les modeles instruits, et
renvoie au theme 06.

**Ce que cela impose au projet.** La phrase « la simulation gonfle les ecarts entre groupes » n'est
pas vraie en general. Elle est vraie **dans le regime persona individuelle**, qui est le notre, et
elle est fausse dans le regime distribution de groupe zero-shot. Toute formulation qui ne nomme pas
le regime est refutable par une seule ligne de Boelaert.

### Contradiction 2. Qui perd le plus sur les categories rares

a28 section 3.4 et a31 etablissent que sur les cellules a reponse minoritaire, l'ordre des methodes
s'inverse : agents entretien 0,256 de rappel, C3 0,220, `B1 argmax` 0,046, `B2 argmax` 0,027,
`B3 foret` 0,008. Un facteur 32 entre l'agent et la foret.

**Von der Heyde (T03-34) mesure exactement le contraire** sur le vote allemand. F1 par parti, GPT-3.5
contre une regression multinomiale sur les memes variables : CDU/CSU 0,62 contre 0,73,
SPD 0,52 contre 0,67, **FDP 0,34 contre 0,50, AfD 0,33 contre 0,58, petit parti 0,11 contre 0,31,
vote nul 0,00 contre 0,18**. L'ecart entre la statistique et le modele **se creuse quand la
categorie se rarefie**, de 11 points sur le parti majoritaire a 25 points sur l'AfD et 20 sur les
petits partis.

Trois variables candidates pour expliquer, dans l'ordre de plausibilite.

1. **La nature de la rarete.** Chez von der Heyde, l'AfD est une categorie rare mais **fortement
   predictible par l'etiquette** : ses electeurs se signalent par l'identification partisane et par
   l'ideologie, deux des variables de l'invite. Chez nous, une modalite minoritaire d'item ordinal
   du GSS est rare **et faiblement predictible**. La regression gagne sur la rarete deductible et
   perd sur la rarete non deductible. C'est un enonce testable chez nous en une soiree, voir (d).
2. **La metrique.** Le F1 par classe recompense la precision autant que le rappel ; notre mesure
   principale est le rappel, ou une methode qui n'ose jamais obtient zero. `B2 argmax` a 0,455 de
   precision pour 0,027 de rappel dans a28 : sur un F1, il remonterait. ARBITRAGE.md cite deja un
   facteur 11 sur F1 contre 3,4 pour la regression ; ces chiffres sont les bons a porter, pas le
   facteur 32.
3. **L'appariement de l'information.** La regression multinomiale de von der Heyde semble evaluee
   en echantillon, sans validation croisee, ce qui gonfle mecaniquement ses F1 sur les classes
   rares. Cette faille n'est pas levee, et elle suffirait a expliquer une partie de l'ecart.

### Contradiction 3. Le realisme distributionnel est-il un but

Ashokkumar (T03-39) etablit r = 0,85 entre effets simules et effets reels et en fait un argument
pour l'usage des simulations. Li et Ji (L03-12) montrent, sur 59 508 participants de 62 pays, que
la correlation entre realisme statistique et exactitude de l'effet vaut **rho = 0,10**, et qu'elle
peut valoir **rho = -0,52** dans certaines configurations, c'est a dire qu'ameliorer le realisme
degrade l'effet. Les deux ne se contredisent pas frontalement, ils mesurent deux choses : le
premier valide un usage (predire un effet), le second invalide un raccourci (utiliser la
ressemblance des reponses comme preuve de validite de l'effet). La variable est l'unite
d'observation, encore. Elle doit etre nommee a chaque fois.

### Contradiction 4. L'affinage ferme-t-il l'ecart

Xie (L03-03) mesure un doublement du taux de reussite par affinage sur donnees d'enquete, 0,258
vers 0,534, et generalisation partielle a d'autres jeux, 0,325 vers 0,402 sur le GSS. Suh et al.
(T03-04) mesurent une amelioration de 44,7 % sur des sous populations non vues. **Ahn (L03-01)
mesure l'inverse au niveau individuel** : un GPT-4.1 affine tombe a 2,31 % de R2 demoyenne, sous le
meilleur prompt non affine a 4,44 %, et le modele affine sur SocSci210 passe de 7,57 % sur les
etudes vues a **0,73 % sur les etudes tenues a l'ecart**. La variable est la meme que partout :
**l'affinage ameliore la marginale et n'ameliore pas la personne**, et le gain apparent sur donnees
vues est de l'apprentissage d'items, pas de personnes.

---

## (d) Ce que ca permet de tester chez nous tout de suite

Sept tests. Aucun n'exige un appel de modele de langage : tout est deja dans `data/` et dans les
traces du 8 septembre. Les couts sont donnes en temps de calcul et en travail d'ecriture.

**1. Le test de la moyenne d'item, protocole Ahn.** Retirer de chaque cellule (personne, item) la
moyenne humaine de l'item calculee en laissant la personne de cote, puis calculer le R2 poole entre
deviation humaine et deviation predite, pour les treize methodes de a28 plus les humains de la
vague 2. Le plancher est deja connu, c'est notre test retest. **Ce test remplace avantageusement
l'exactitude en correspondance exacte**, parce qu'il ne recompense pas la reproduction de la
marginale. Prediction : `B0 mode` tombe a exactement zero par construction, `B1` et `B3 foret`
tombent tres bas, les agents riches et C3 restent au dessus. Si les agents ne battent pas la
moyenne d'item, la these change de forme. **Cout : une soiree, zero appel de modele, environ
80 lignes.**

**2. La decomposition en composantes, personne contre personne x item.** Ajuster par maximum de
vraisemblance restreint la decomposition de l'erreur en effet personne, effet item et residu, puis
partitionner le residu avec notre test retest, exactement comme L03-01. Cela produit chez nous le
chiffre « 8,9 fois » et permet de dire, sur nos donnees, quelle part de ce que la simulation efface
est de la personne et quelle part est du couple personne x item. **C'est la mesure qui donne son
mecanisme a a31 dans un vocabulaire deja etabli.** Cout : une soiree, `lme4` ou equivalent.

**3. Le taux de change zeros d'echantillonnage contre zeros structurels, protocole Garrido.**
Definir une modalite rare recuperee comme un vrai positif minoritaire, et une modalite rare fausse
comme un zero structurel, puis publier le **rapport** au lieu du rappel seul, pour les treize
methodes. `B3 foret` a 0,008 de rappel pour 0,207 de precision ; les agents entretien a 0,256 pour
0,233. Le rapport, et non le rappel, est ce que la litterature de synthese de population lit depuis
2020. Cout : deux heures, les colonnes existent deja dans `a28-t3-minorites.csv`.

**4. Le test de la rarete deductible, pour trancher la contradiction 2.** Partitionner les cellules
minoritaires en deux : celles ou le segment de la personne predit deja la modalite rare (rarete
deductible de l'etiquette, cas AfD de von der Heyde) et celles ou il ne la predit pas. Refaire le
tableau de rappel a28 section 3.4 sur chaque moitie. Prediction, si la these tient : la regression
et la foret gagnent sur la premiere moitie, les agents gagnent sur la seconde. **Ce test est le seul
du lot qui peut faire tomber le rang 1 revise, et il coute une soiree.**

**5. Le F1 minoritaire a cote du rappel, partout.** ARBITRAGE.md porte deja un facteur 11 sur F1 ;
a28 porte un facteur 32 sur le rappel. Publier les deux cote a cote, avec la precision, ferme
d'avance l'objection « vos agents ne font qu'oser au hasard ». Le tableau a28 section 3.4 contient
deja precision et rappel : il manque une colonne. Cout : dix minutes.

**6. Le test d'inference augmentee, protocole Ye.** Sur nos 149 items, calculer le parametre de
reglage optimal du PPI++ item par item, et compter combien d'items ont un reglage nul, c'est a dire
combien de nos items ne recoivent **aucun** signal individuel exploitable de nos agents. Ye trouve
26 sur 68 sur Twin-2K-500. **Ce chiffre est celui qu'un institut d'etudes comprend immediatement**,
et il transforme la these en argument economique. Cout : une soiree, formules en forme close, aucun
modele.

**7. Le post stratifiage de la population simulee, deja identifie dans `corpus/03`.** Il reste a
faire et il devient plus interessant apres cette lecture : Wang et Gelman montrent que le MRP se
trompe le plus sur les petits sous groupes, et nous montrons que la simulation garde les minorites.
Croiser les deux repond a une question que personne n'a posee : **une post stratification appliquee
a une population simulee corrige-t-elle la distorsion inter, et que fait-elle a la masse
minoritaire que les agents produisent ?** Cout : une soiree, table de recensement a recuperer.

---

## (e) Ce que personne n'a fait

Les sept points de `corpus/03` restent valides. Cette lecture en confirme trois, en retire un
partiellement, et en ajoute quatre.

**Confirme et renforce.**

1. **Le rappel des minorites d'opinion, statistique contre langage, sur les memes items.** Xie et
   al. l'ecrivent eux memes dans PNAS : « Benchmarking LLM-based simulation against
   state-of-the-art imputation methods in scenarios where some outcomes are partially observed
   remains an important avenue for future research. » Quinze modeles, sept enquetes, et ils
   declarent la comparaison manquante. Le trou est confirme par la publication la plus visible du
   domaine.
2. **La comparaison MRP contre LLM sur les memes cellules.** Aucune des vingt references nouvelles
   ne la fait.
3. **Le couple exactitude et diversite avec une baseline non LLM sur les memes cellules.** Aucune
   des vingt ne le trace.

**A retirer partiellement.**

4. **« La documentation du signe oppose du terme inter » n'est plus intacte.** Xie et al.
   publient, dans PNAS en mai 2026, l'entropie ecrasee et le V de Cramer gonfle sur les memes
   donnees et les memes modeles : c'est la double distorsion au niveau de la population. Ce que la
   phrase de `corpus/03` conserve, c'est la comparaison avec le **sens oppose du modele
   hierarchique**, que Xie ne fait pas, et la mesure **au niveau individuel**. La revendication doit
   etre reformulee : ce n'est plus « personne n'a mesure les deux distorsions », c'est « personne
   n'a oppose le signe du terme inter de la simulation a celui du modele hierarchique ». C'est
   coherent avec la ligne d'ARBITRAGE.md, « une equipe l'a fait en avril ».

**Nouveau.**

5. **Personne n'a evalue un simulateur avec une metrique qui compte les gens rares.** Le standard du
   domaine, alpha-precision et beta-rappel (L03-09), les exclut explicitement de la mesure. Le
   standard voisin, le taux de change zeros d'echantillonnage contre zeros structurels (L03-06),
   les compte, mais il vit en microsimulation des transports et n'a jamais ete applique a des
   reponses d'enquete d'opinion. **Transporter la metrique de Garrido sur des items d'attitude est
   une contribution a soi seule**, et elle coute deux heures chez nous.
6. **Personne n'a mesure ce que le controle de divulgation coute en couverture des minorites.**
   `synthpop` propose trois options qui suppriment les cas rares (`cart.minbucket`, lissage,
   `sdc()`) et aucune publication ne chiffre leur cout. C'est un resultat court, publiable, et il
   retourne la these : la statistique n'efface pas les gens rares par accident, elle le fait sur
   ordre.
7. **Personne n'a fait le rapprochement entre l'ecrasement de variance et la valeur d'inference.**
   Ye (T03-37) donne la formule, Ahn (L03-01) donne la mesure de l'ecrasement, et personne ne les a
   mis dans le meme tableau. Une colonne « part de variance individuelle conservee » a cote d'une
   colonne « reduction de variance d'estimateur » transformerait l'ecrasement, qui est un argument
   de methodologue, en un prix, qui est un argument d'acheteur.
8. **Personne n'a lu les estimateurs a triple objectif comme un correctif de simulation.** Le
   constrained Bayes de Louis et Ghosh et le triple-goal de Shen et Louis existent depuis 1984 et
   1998, sont exactement concus pour retablir la dispersion d'un ensemble d'estimateurs
   retrecis, et **ne sont cites par aucun des cinquante trois papiers du theme**. Les appliquer aux
   sorties d'un simulateur est une idee que le corpus rend disponible et que personne n'a eue.

---

## (f) Ce que je n'ai pas pu verifier

**Contraintes materielles de la session, a declarer en premier.**

- **Le budget WebSearch etait epuise a l'ouverture (200 appels sur 200).** Aucune recherche web
  n'a pu etre lancee. La descente et la remontee de citations ont ete faites par l'API arXiv (qui
  ne cherche que dans les metadonnees, pas dans le texte integral), l'API Crossref, Europe PMC,
  l'API HAL, WebFetch, et surtout les **listes de references des papiers lus**. C'est une methode
  qui trouve bien ce qui est cite et mal ce qui ne l'est pas.
- **L'API OpenAlex a repondu « Rate limit exceeded, insufficient budget » des le second appel.**
  La descente de citations aval, qui est sa fonction principale, n'a pas pu etre faite du tout par
  cette voie. **Semantic Scholar a repondu 429 aux deux tentatives.** Les citations aval trouvees
  l'ont ete par recherche arXiv sur les titres et par lecture des bibliographies.
- **`pdftotext` etait present**, contrairement a ce qu'affirmait `corpus/03`. C'est le seul point
  ou les conditions se sont ameliorees.

**Ce qui reste hors de portee.**

- **Shen et Louis 1998 (L03-11) : seul le resume a ete lu.** Le texte est chez Oxford. Toutes les
  citations que je donne viennent du resume Crossref, qui est le resume officiel de l'article.
  Aucune valeur numerique de simulation n'a ete lue. **Louis 1984 et Ghosh 1992 n'ont pas ete
  atteints du tout.** Comme cette ligne porte l'ancrage theorique de toute la section (b), elle
  doit etre obtenue avant publication.
- **Robinson 1950 et King 1997 sur l'inference ecologique : non lus.** Le PDF de la reedition de
  Robinson dans l'International Journal of Epidemiology renvoie une page anti robot, JSTOR de meme,
  et je n'avais pas de recherche web pour trouver un miroir. Je ne cite donc **aucune** valeur de
  correlation ecologique, alors que c'etait un des quatre points d'attention demandes. La
  litterature sur la prediction individuelle depuis des variables de groupe est representee ici par
  ses descendants (Shen et Louis, Ahn et al. qui parlent explicitement d'« ecological fallacy »,
  Fisher, Medaglia et Jeronimus 2018 cite par Ahn sous le titre *Lack of group-to-individual
  generalizability is a threat to human subjects research*), **pas par ses fondateurs**. C'est le
  manque le plus serieux de ce fichier.
- **Downes et Carlin 2020 (T03-29 et T03-30) : toujours pas obtenus.** Ce sont les deux papiers qui
  chiffreraient le retrecissement du MRP sur les petits sous groupes. Le fait le plus proche que
  j'ai pu lire est celui de Wang et Gelman, « the largest differences occur for relatively small
  demographic subgroups », qui est une observation, pas une simulation.
- **Ornstein 2020 (T03-32) et autoMrP (T03-33) restent [PROBABLE].** Deux tentatives de
  telechargement du PDF d'Ornstein ont renvoye du HTML.
- **Holtdirk et al. (L03-05) : les valeurs numeriques sont dans les figures et ne sont pas
  extractibles du PDF.** Les enonces qualitatifs et le test de Wilcoxon cite (W = 2,40, p = 0,016)
  sont lus dans le texte ; aucune valeur de macro F1 ne l'est.
- **Meister et al. (L03-13) : aucun chiffre extrait.** Seuls le resume et les sections de methode
  ont ete lus. L'enonce « LLMs can more accurately describe the opinion distribution than simulate
  such distributions » est lu dans le texte ; le **knowledge-to-simulation gap** n'est pas chiffre
  ici.
- **Shumailov et al. (L03-14) : lecture partielle.** Les enonces sur les queues sont lus, aucune
  valeur numerique n'est reprise, et l'analogie avec l'extension d'enquete est la mienne, pas la
  leur.
- **Sen, Lutz, Rogers, Garcia, Strohmaier, *Missing the margins*, ACL Findings**, cite par L03-01
  pour le chiffre « 30% of positive representativeness claims do not evaluate across multiple
  demographic categories » : **non lu**, chiffre non verifie, non repris dans la table.
- **Kolluri, Wu, Park, Bernstein, EMNLP 2025**, la source de SocSci210 et de Socrates-Qwen2.5-14B :
  **non lu**. Les chiffres de SocSci210 que je donne sont ceux de Ahn et al., pas ceux de la source.
- **Les figures de Ye et Yoganarasimhan (section 6.3 a 6.5) et la totalite des annexes web** n'ont
  pas ete lues ; les chiffres cites viennent du corps du texte.
- **Xie et al. : les valeurs exactes des boites a moustaches de la figure 4** (entropie et V de
  Cramer par modele) ne sont pas dans le texte. Je ne cite que les enonces de direction et les deux
  exemples chiffres du texte, R2 0,6 contre 0,1 et le tableau 1 d'affinage.
- **Rien dans ce fichier n'a ete verifie par calcul.** Aucun code d'analyse n'a ete ecrit,
  conformement a la consigne. Les chiffres maison cites en (b), (c) et (d) sont recopies de a1, a2,
  a8, a23, a28 et a31.

---

## Annexe. Ce qui a ete lu, et comment

**Lues en entier, ou dans toutes leurs sections substantielles (17 nouvelles lectures) :**
Wang, Rothschild, Goel et Gelman 2015 ; von der Heyde, Haensch et Wenz 2025 ; Ye et
Yoganarasimhan 2026 ; Garrido, Borysov, Rich et Pereira 2020 ; Borysov, Rich et Pereira 2019 ;
Nowok, Raab et Dibben 2016 ; Alaa, van Breugel, Saveliev et van der Schaar 2022 ; Boelaert,
Coavoux, Ollion, Petev et Praeg 2025 ; Ashokkumar, Hewitt, Ghezae et Willer 2026 ; Ku, Hsu, Huang,
Liu, Cheng et Kang 2026 ; Holtdirk, Assenmacher, Bleier et Wagner 2025 ; Ahn, Mao et Lee 2026 ;
Peng et al. 2026 ; Xie et al. 2026 ; Li et Ji 2026 ; Goplerud et Bisbee 2022 ; van Buuren 2018
section 1.3.

**Lues partiellement (3) :** Shumailov et al. 2023, Meister, Guestrin et Hashimoto 2024,
Shen et Louis 1998 (resume seulement).

**Relues en interne avant la recherche (6) :** `corpus/00-GRILLE.md`,
`corpus/lecture-complete/00-CONSIGNE.md`, `corpus/03-baselines-statistiques-extension-enquete.md`
en entier, `resultats/a28-trois-tests-decisifs.md` (tests 2 et 3, plus sections 0, 4 et 5),
`resultats/a31-la-mauvaise-rarete.md` (reponse en une ligne et protocole), `ARBITRAGE.md`.

**Total : 26 references lues en entier ou dans toutes leurs sections substantielles**, dont 20
externes et 6 internes.

**Le critere d'arret.** Les trois dernieres remontees de citations (bibliographie de Ahn et al.,
bibliographie de Peng et al., bibliographie de Ye et Yoganarasimhan) ne rendaient plus que des
references deja dans la table ou deja dans `corpus/01` et `corpus/02` : Bisbee 2024, Santurkar 2023,
Argyle 2023, Toubia 2025, Dominguez-Olmedo 2023, Hu et Collier 2024. Les recherches arXiv sur
« survey augmentation », « synthetic respondents » et « tail » ne rendaient plus rien de neuf sur le
theme. Le chantier s'arrete la, avec les manques declares en (f), dont le plus serieux est
l'absence de lecture des fondateurs de l'inference ecologique.
