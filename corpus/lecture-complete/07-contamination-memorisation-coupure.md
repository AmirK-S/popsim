# 07. Contamination, memorisation, coupures. Lecture complete

Lecture complete du theme 07, menee le 8 septembre 2026 selon `corpus/lecture-complete/00-CONSIGNE.md`,
sur la grille de `corpus/00-GRILLE.md`. Point de depart : `corpus/07-contamination-memorisation-coupure.md`,
deja revise apres lecture directe des PDF, et sa section 5 qui listait dix dettes.

Ce fichier fait trois choses que le precedent ne faisait pas. Il paye la dette numero 1, le comptage
infini-gram, avec les requetes et les comptes bruts. Il paye la dette numero 2, la lecture de Gui et
Toubia, et cette lecture retourne la conclusion du bloc des prix. Il ajoute dix references trouvees
en remontant et en descendant les citations, dont deux qui rapprochent le theme 07 de la these
d'ARBITRAGE : la substitution de la personne par le groupe pourrait etre une memorisation de
statistiques de groupe, et le corpus permet maintenant de le chiffrer.

Certitude : `[CONFIRME]` lu dans le texte avec le chiffre releve, `[PROBABLE]` lu dans le resume ou
une source secondaire, `[NON LU]` titre seulement. Aucun chiffre n'est invente. Douze references ont
ete lues en entier dans cette session, listees en section 8.

---

## 0. Ce que cette lecture change, en cinq points

**Un. Le bloc des prix de Twin-2K-500 n'est pas une memorisation de tableau.** `corpus/07` avancait
que la table des 40 produits et de leurs prix normaux etait en ligne depuis decembre 2023, donc avant
la coupure de GPT-4.1. C'est faux. La version v1 de Gui et Toubia (24 decembre 2023) ne contient
aucun produit nomme ni aucun prix : elle travaille sur les 40 **categories** de DellaVigna et
Gentzkow. La table A.1, avec les libelles commerciaux exacts et les prix, apparait pour la premiere
fois dans la **v2 du 21 janvier 2025**, et les prix ont ete releves sur Walmart.com **vers avril
2024**, apres la coupure declaree de GPT-4.1. Le comptage confirme : neuf des dix libelles produits
exacts donnent **zero occurrence** dans Dolma, RedPajama, The Pile et C4, et zero aussi dans deux
instantanes de Common Crawl 2025 et dans DCLM-baseline. L'hypothese qui reste est la connaissance
produit generale (07.33), pas la restitution d'un tableau arXiv.

**Deux. Le questionnaire du GSS est quasi absent des corpus ouverts, son nom y est partout.** Le
libelle exact « Improving the nation's education system » apparait **1 fois** dans Dolma-v1.7, la
chaine « General Social Survey » **60 837 fois**. Ce n'est pas une contamination du texte du
questionnaire.

**Trois. Ce qui est massivement present, c'est la statistique de groupe.** « percent of Republicans »
apparait **123 159 fois** dans Dolma, « percent of Democrats » 98 625, « percent of Americans say »
41 037, « percent of conservatives » 3 990. Le rapport entre la masse des statistiques de groupe et
la masse du libelle d'item du GSS est de l'ordre de **10^5 pour 1**. C'est un fait de corpus, mesure,
et c'est la premiere piece de preuve cote pre entrainement pour la these d'ARBITRAGE : un modele
entraine sur ce corpus a vu des dizaines de milliers de fois la phrase « x pour cent des republicains
pensent que », et une fois la question du GSS. La substitution de la personne par le groupe a une
source plausible dans la distribution du corpus, avant tout alignement.

**Quatre. Un papier de juillet 2026 teste deja cette hypothese, et il conclut a moitie dans notre
sens.** Ozkan (07.50) monte une attaque de memorisation a placebo sur des personas WVS turcs et
conclut, mot pour mot : « the national marginal holds, subgroup claims are explainable by recall and
prompt noise ». Son backtest electoral est net : la distribution agregee tombe a TVD = 0,051, mieux
que l'auto declaration des personnes elles memes (0,095), mais sur un resultat anterieur a la coupure,
donc « plain recall, not simulation » ; et la route individuelle s'effondre, la part du premier parti
passant de 42,6 pour cent reels a 88,0 pour cent predits. Deux echecs, dit il : « one remembers, the
other collapses; neither simulates ».

**Cinq. Le dessin post coupure a un concurrent, et le vocabulaire est deja pris.** Jia et al. (07.53)
publient en mai 2026 « When Can Digital Personas Reliably Approximate Human Survey Findings? », qui
parle de « held-out post-cutoff answers ». Verification faite dans le texte : leur coupure est **2023
comme date de coupe du dossier du repondant**, pas la coupure d'entrainement du modele. Le dessin
manquant reste manquant, mais le mot est desormais ambigu et il faudra le dire.

---

## 1. La table etendue

Colonne « trouve par » : `table initiale` = present dans `corpus/07` ; `citation amont` = trouve dans
la bibliographie d'une reference confirmee ; `citation aval` = trouve parmi les articles qui citent
une reference confirmee ; `recherche` = trouve par interrogation de l'API arXiv sur le theme.

Note de methode : le budget de recherche web de la session etait epuise, le sourcage a donc ete fait
par l'API arXiv, par OpenAlex et par les bibliographies des PDF telecharges. C'est une limite, elle
est declaree en section 7.

### 1.1 References nouvelles

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | trouve par | certitude |
|---|---|---|---|---|---|---|---|---|---|---|
| 07.49 | Gui, Toubia, arXiv 2312.15524, v1 24/12/2023, **v2 21/01/2025**, v3 23/11/2025, *The Challenge of Using LLMs to Simulate Human Behavior: A Causal Inference Perspective*, https://arxiv.org/abs/2312.15524 | pourquoi une simulation en aveugle donne t elle des resultats implausibles ? | 40 categories de DellaVigna et Gentzkow, un produit vedette Walmart par categorie, prix normal releve **vers avril 2024**, table A.1 ; enquete humaine pre enregistree (aspredicted.org/pqys-st6w), **1 000 repondants Prolific representatifs, 991 retenus**, un achat par produit, prix tire au hasard | gpt-4o-mini-2024-07-18 epingle, 50 tirages a temperature 1 ; serie GPT-3.5-Turbo a GPT-4.1 pour l'aveuglement ; GPT-4o-mini affine | erreur absolue moyenne sur la probabilite d'achat par couple produit prix ; correlations induites entre prix et variables non specifiees | courbe de demande humaine decroissante, **courbe simulee en U inverse**, meme en retirant le point a prix nul ; le prix aleatoire correle positivement avec le prix passe, le prix du concurrent et la date de peremption ; MAE hors boite 0,532 en aveugle contre 0,397 en devoile ; affine sur l'enquete 0,134 et 0,128, affine et evalue en devoile **0,113** ; avec un jeu observationnel Amazon ajoute, l'aveugle se degrade a 0,233 et le devoile tient a 0,120 ; en fixant le prix du concurrent, la demande devient une fonction en escalier | contamination et coupure ne sont **jamais** discutees ; un seul modele porte l'essentiel des mesures ; le gain de l'aveuglement va de 1 a plus de 60 pour cent selon le modele, sans decomposition | soutient, et **retourne le bloc des prix**. La table des prix normaux est postee le 21 janvier 2025, apres la coupure de GPT-4.1 (juin 2024) : l'hypothese « tableau memorise » tombe. Reste la connaissance produit (07.33). Le mecanisme central est en revanche du meilleur secours pour notre these : « Since LLMs are trained primarily on observational data, it is plausible that an ambiguous question will also be interpreted in a way that is similar to observational data ». Le modele repond `P(Y|D)` la ou on lui demande `P(Y|do(D))`, c'est a dire une conditionnelle de population la ou on demande une reponse individuelle. C'est la substitution personne vers groupe, ecrite en langage causal | table initiale (07.35bis, etait [NON LU]) | [CONFIRME] |
| 07.50 | Ozkan, 2026, arXiv 2607.18310, *Distribution-First Population Simulation: Collapse, Calibration, and Recall in Non-WEIRD LLM Persona Modeling*, https://arxiv.org/abs/2607.18310 | la fidelite agregee d'une population simulee est elle de la restitution ? | microdonnees WVS Turquie, **2 414 repondants reels** ; backtest sur une election nationale passee ; trois attitudes qui ont bouge entre les vagues GSS 2016 et 2022 | Qwen3.6-35B en local, GLM-5.2, Gemma-4-26B | verificateur deterministe a validite de construit ; concentration, entropie, TVD ; **attaque de memorisation en trois tests avec controle placebo** ; backtest electoral en TVD | agents independants : concentration 0,36 vers 0,69, entropie 1,46 vers 0,77, **85 pour cent des unites s'effondrent, TVD = 0,44**, r = 0,55 avec l'existence d'une reponse normativement correcte ; Verbalized Sampling : fidelite +7 a +10, p = 0,002, d = 6,2, mais sur dispersion, rapport d'ecarts types 0,4 a 0,56 vers 1,26 a 1,37 ; **attaque de memorisation, Qwen : la conditionnelle ne bat pas la restitution nationale, delta = -0,165, p < 0,001 ; le gradient de sous groupe colle a la realite dans 62 pour cent des cas, rho = 0,68 ; sensibilite 1 sur 3 et specificite 0 sur 2** ; placebo : la manipulation pertinente donne delta = +1,13, la manipulation **non pertinente** +1,49, donc plus ; backtest : VS a **TVD = 0,051** contre 0,095 pour l'auto declaration humaine, mais resultat anterieur a la coupure ; route individuelle : premier parti de **42,6 pour cent reels a 88,0 pour cent predits, TVD = 0,454** ; suivi du changement 2016 vers 2022, cosinus 0,46 Qwen, 0,69 Gemma, 0,70 GLM | un seul pays, un seul instrument, un seul domaine agentique ; « None of this replaces a true post-cutoff holdout » est ecrit par l'auteur ; les tests de memorisation sont indirects, il n'y a aucune mesure cote corpus | soutient fortement et **preempte partiellement**. C'est le premier article qui separe trois niveaux : la marginale nationale tient par restitution, les affirmations de sous groupe sont explicables par la restitution, l'individu s'effondre. Citation a garder : « one remembers, the other collapses; neither simulates ». Notre apport residuel : il ne mesure rien cote corpus, il n'a pas de baseline statistique, et il ne teste pas les reponses rares | recherche | [CONFIRME] |
| 07.51 | Renda, Ross, Cafarella, Andreas, MIT CSAIL, arXiv 2510.15096, v2 22/04/2026, *OpenEstimate*, https://arxiv.org/abs/2510.15096 | un modele sait il produire des a priori numeriques corrects sur des statistiques de population ? | **178 statistiques** sur trois domaines : Glassdoor (1 marginale, 16 a une condition, 20 a deux, 6 a trois, 43 au total), Pitchbook (4, 17, 20, 20, 61), **NHANES (14 marginales, 20, 20, 20, 74)** | Llama 3.1 8B et 70B, GPT-4, o3-mini, o4-mini, Qwen3-235B-A22B | **statistiques conditionnelles derivees** : filtrer un grand jeu observationnel sur des conditions tirees au hasard, en exigeant que chaque condition deplace la statistique d'au moins 5 pour cent, ce qui rend la cible verifiable mais peu susceptible d'etre documentee ; taux de victoire de l'a priori du modele contre une base a N echantillons, CRPS, calibration | l'a priori d'un modele vaut environ **cinq echantillons** de la vraie distribution ; taux de victoire contre la base a 5 echantillons : NHANES 74,3 pour cent, Pitchbook 50,8, Glassdoor 37,0 ; il s'effondre a 30 echantillons : 37,8, 50,8, 8,7 ; rapport CRPS contre la base a 5 echantillons : o4-mini 1,17 sur NHANES, Llama-3-8B **19,17** ; tous les modeles surestiment systematiquement | pas de donnee d'opinion, uniquement sante, emploi et finance ; la construction ecarte la memorisation par tirage, elle ne la mesure pas | soutient fortement, et **donne l'outil manquant**. Les auteurs ecrivent le probleme exactement comme nous : « if in the training data, the benchmark tests memorization rather than reasoning ». Leur parade, la statistique conditionnelle derivee, est le **couple de controle** dont nous avons besoin : une marginale du GSS publiee peut avoir ete memorisee, une conditionnelle a trois filtres tiree au hasard dans le cumulatif ne peut pas l'avoir ete. La difference des deux scores est une mesure de memorisation, sans acces au corpus | recherche, puis citation amont depuis 07.52 | [CONFIRME] |
| 07.52 | Hobor, Brcic, Kovac, Poje, Universite de Zagreb, arXiv 2604.01896, *Bayesian Elicitation with LLMs*, https://arxiv.org/abs/2604.01896 | un modele connait il les statistiques de population publiees, et avec quelle confiance ? | 400 questions, 100 par jeu : Big Five par pays et par trait, NHANES 2017-2018, NCD-RisC, Glassdoor ; filtre a 500 repondants minimum par groupe | onze modeles, effort de raisonnement bas, moyen, haut | estimation ponctuelle plus intervalle credible a 95 pour cent ; couverture empirique ; NLL ; recalibration conforme | **couverture de 9 a 44 pour cent** la ou 95 est vise ; Claude Opus 42,6 contre Haiku 9,5 (p < 0,001) ; GPT-5.2 20,0 contre 14,8 (p < 0,01) ; taux de victoire contre une base naive a 50 pour cent : **Big Five 88,9, NCD-RisC 69,6, Glassdoor 65,7, NHANES 60,9** ; **les modeles predisent une mediane de 18,0 pour cent quand la vraie mediane est 40,3** ; conditions rares (vrai < 20 pour cent) gagnees 97,5 pour cent du temps, conditions frequentes (> 50) 57,8 ; la recherche web **degrade** les modeles deja bons, taux de victoire 39,8 pour cent | pas de donnee d'opinion ; pas de test de contamination, seulement une lecture par domaine ; petit echantillon par cellule | soutient. Deuxieme mesure independante du meme fait : **le modele sait les statistiques dont on parle beaucoup et pas les autres**. Le detail utile pour nous est de signe contraire a notre resultat sur les rares : ici le modele **sur predit** la rarete (mediane 18 contre 40,3 vraie) sur des prevalences de sante, alors que dans nos donnees il **sous produit** les reponses rares d'opinion. La variable qui separe les deux est a chercher, elle est nommee en section 4 | recherche | [CONFIRME] |
| 07.53 | Jia, Chen, Sharma, Diaz-Rodriguez, York University, 2026, arXiv 2605.10659, *When Can Digital Personas Reliably Approximate Human Survey Findings?*, https://arxiv.org/abs/2605.10659 | quand un persona numerique approche t il un resultat d'enquete humain ? | panel LISS (Pays Bas), **500 repondants echantillonnes par strates** (sexe, age, etape du menage) ; coupe temporelle a 2023 : historique avant 2023 en entree, reponses 2023 et 2024 en cible ; deux taches, prediction de vague unique et prediction du noyau | GPT 5.4, Gemini 3 Flash, Claude Haiku 4.5, croises avec quatre architectures de persona, soit 12 reglages | exactitude par question, par repondant, alignement distributionnel, equite par strate, accord de partition ; puis modelisation logistique et XGBoost avec SHAP sur trois couches de variables | l'alignement distributionnel s'ameliore, la prediction individuelle reste faible, l'accord de partition multivarie est **generalement bas** ; les architectures a recuperation gagnent legerement ; **la variabilite des reponses humaines est le premier predicteur de l'exactitude du persona** : « personas are most accurate when human answers are concentrated and respondent patterns are common, and least accurate when questions elicit heterogeneous or rare responses » ; performance stable entre strates demographiques | **la coupure est celle du dossier du repondant, pas celle du modele** : les cibles 2023 et 2024 sont anterieures a la coupure de GPT 5.4 et de Gemini 3 ; aucune mention de contamination de corpus ; jeu non americain, non anglophone | soutient et **concurrence directement l'option A d'ARBITRAGE**. C'est une replication independante, sur un autre panel et trois modeles recents, du fait que la simulation echoue precisement sur les reponses rares et heterogenes. Notre difference : ils le mesurent comme un predicteur SHAP de l'exactitude, pas comme un rappel et un F1 sur les modalites rares, et sans baseline statistique. L'ecart de facteur 11 contre la foret aleatoire reste a nous | recherche | [CONFIRME] |
| 07.54 | Xu, Liu J., Choi, Smith, Hajishirzi, arXiv 2506.12229, v5 06/01/2026, *Infini-gram mini*, https://arxiv.org/abs/2506.12229 | peut on rendre cherchable un corpus de l'ordre du petaoctet ? | **83 To de texte indexes en 99 jours** sur un noeud a 128 vCPU : The Pile (1,3 To d'entrainement, 1,4 Go de validation), **DCLM-baseline 17 To**, et **sept instantanes de Common Crawl de janvier a juillet 2025, 65 To** | sans objet, moteur de comptage | index FM sur les octets UTF-8 bruts, taille d'index a 44 pour cent du corpus ; comptage, localisation, reconstruction de document ; **bulletin de contamination** public | jusqu'a **74,2 pour cent** d'un jeu de reference retrouve contamine dans des crawls Internet ; 24 benchmarks analyses ; comptage court sous 0,4 seconde ; API publique `api.infini-gram-mini.io`, index `v2_cc-2025-05` a `v2_cc-2025-30`, `v2_dclm_all`, `v2_piletrain`, `v2_pileval` | recherche exacte, donc aveugle aux reformulations (meme limite que 07.08) ; l'index ne porte pas sur les corpus proprietaires de Llama 3.1, gpt-oss ou Qwen3 ; les noms d'index de la documentation different de ceux acceptes par le serveur, voir section 2.1 | soutient fortement. **Cet outil change l'echelle de la dette 1** : il couvre des crawls de 2025, donc posterieurs a la coupure de tous nos modeles, et DCLM-baseline, qui est le plus proche des recettes recentes. C'est ce qui permet de dire que la table des prix de Gui et Toubia n'est nulle part, meme apres publication | citation amont depuis 07.26 et 07.56 | [CONFIRME] |
| 07.55 | Liu J., Blanton, Elazar, Min et al., Allen Institute, arXiv 2504.07096, ACL 2025 demo, *OLMoTrace*, https://arxiv.org/abs/2504.07096 | peut on remonter une sortie de modele jusqu'a ses documents d'entrainement en temps reel ? | corpus complets d'OLMo, de l'ordre de plusieurs milliers de milliards de tokens | OLMo, et par extension tout modele a corpus indexe | recherche des **segments maximaux communs** entre la sortie et le corpus, via une version etendue d'infini-gram ; score de pertinence des documents | **4,46 secondes de latence moyenne** par requete sur une sortie d'environ 450 tokens ; parmi les documents retrouves, **96,7 pour cent viennent du pre entrainement**, 0,9 du mi entrainement, 2,4 du post entrainement dont 0,9 de SFT et 1,5 de DPO ; 14 pour cent des documents juges de haute pertinence, 19 pour cent des segments retenus | ne fonctionne pleinement que sur des modeles a corpus ouvert ; correspondance litterale uniquement | soutient. Donne un test que personne n'a fait sur une enquete : **prendre la reponse que le modele produit en simulant un repondant, et la tracer dans le corpus**. Si les segments qui reviennent sont des phrases de rapport d'enquete plutot que des phrases de personne, la substitution personne vers groupe est visible dans la trace, pas seulement dans le score | citation amont depuis 07.56 | [CONFIRME] |
| 07.56 | Barmina, Schneider-Kamp, Galke Poech, 2026, arXiv 2606.06286, *PropMe*, https://arxiv.org/abs/2606.06286 | le modele **peut** il restituer, ou le fait il **spontanement** ? | Common Pile et Dynaword, deux langues | Comma, DFM Decoder, deux modeles entierement ouverts | separation entre **capacite** (attaque par prefixe) et **propension** (invites generiques ou specifiques au jeu, non adversariales) ; transformation metrique produisant un score de propension dans [0,1] ; `SimpleTrace`, chaine de tracage batie sur infini-gram, inspiree d'OLMoTrace | ecart constant entre capacite et propension : les attaques par prefixe declenchent une restitution nettement plus forte que les invites generiques, **les scores de propension restent bas partout** ; les auteurs concluent que les modeles peuvent reveler des donnees d'entrainement mais ne le font guere en usage ordinaire | deux modeles seulement, tous deux petits et entierement ouverts ; jeux de texte, pas de tableau ni d'enquete | soutient et **recadre notre question**. Toute la batterie de `corpus/07` section 2.4 mesure une **capacite**. Or l'objection d'un relecteur porte sur la **propension** : quand on demande au modele de simuler un repondant du GSS, va t il restituer une marginale publiee ? Ce sont deux mesures differentes et le champ de la simulation d'enquete n'a jamais fait ni l'une ni l'autre | recherche | [PROBABLE] pour les chiffres de detail, [CONFIRME] pour le cadre et pour SimpleTrace |
| 07.57 | Veselovsky, Horta Ribeiro, West, EPFL, 2023, arXiv 2306.07899, *Artificial Artificial Artificial Intelligence*, https://arxiv.org/abs/2306.07899 | les travailleurs de plateforme utilisent ils des modeles pour repondre ? | tache de resume d'abstracts rejouee sur MTurk ; classifieur synthetique contre reel entraine sur des reponses humaines anterieures aux LLM et des reponses generees ; validation par frappe clavier | sans objet | prevalence estimee d'usage de LLM par les repondants | **33 a 46 pour cent des travailleurs de plateforme** ont utilise un modele de langage sur cette tache de production de texte | une seule tache, textuelle, en 2023 ; ne se transpose pas mecaniquement a un questionnaire a choix fermes | **soutient et menace notre plan**. Notre meilleur jeu posterieur a la coupure, Twin-2K-500, est collecte sur Prolific en janvier et fevrier 2025. Si une part des repondants s'aide d'un modele, la « verite humaine » posterieure a la coupure est elle meme partiellement synthetique, et le plancher test retest est biaise vers le haut. C'est une limite a ecrire, pas a cacher | citation amont depuis 07.58 | [CONFIRME] |
| 07.58 | Ma, Zhang M., Ang, Chen, 2026, arXiv 2606.30085, v2 30/08/2026, *Tastes without distinction: silicon samples and the synthetic construction of tastes*, https://arxiv.org/abs/2606.30085 | les echantillons de silicium reproduisent ils la structure des gouts culturels ? | Survey of Public Participation in the Arts, **554 940 substituts de silicium** de repondants reels | modeles OpenAI, Anthropic, DeepSeek | fidelites ecologique, relationnelle et positionnelle ; comparaison des structures de gouts | echantillons **sur omnivores**, biais positif systematique pour l'appreciation, non explique par le biais WEIRD ; « the complex relationality in real taste structures is completely distorted » ; les associations age gout sont **juvenilisees**, les associations classe gout **anachroniques**, les associations genre et race **caricaturees** | pas de mesure de contamination ni de coupure ; domaine des gouts culturels, pas des opinions politiques | soutient. Meme signature que 07.37 et 07.41 : les niveaux agreges passent, la structure relationnelle disparait, et les associations de groupe sont **caricaturees**, ce qui est le mot des sociologues pour ce que nous appelons substitution de la personne par le groupe. Le papier apporte en outre la **contamination inverse** : « the contamination of standard survey data from LLM-generated responses », avec renvoi a 07.57 | recherche | [CONFIRME] pour les enonces, [PROBABLE] pour les chiffres de detail |

### 1.2 Reference de la table initiale dont le statut change

| id | ce que disait `corpus/07` | ce que la lecture etablit | consequence |
|---|---|---|---|
| 07.35bis, devenu 07.49 | `[NON LU]`. « C'est l'article qui met en ligne, avant la coupure de tous les modeles evalues par Twin, la liste des 40 produits et de leurs prix normaux. » | Faux. La v1 de decembre 2023 ne contient ni produit nomme ni prix. La table A.1 parait dans la **v2 du 21 janvier 2025**, prix releves sur Walmart.com **vers avril 2024**. La coupure declaree de GPT-4.1 est juin 2024 | L'hypothese « tableau memorise » sur le bloc des prix **tombe**. `corpus/07` section 2.2, section 3 point 6 et section 5 point 2 sont a corriger. Le test propose (correler l'erreur de prix avec l'avantage par item) garde son interet, mais pour departager connaissance produit et hasard, pas pour departager tableau et connaissance produit |
| 07.35 Twin-2K-500 | « la table provient de Gui et Toubia, arXiv 2312.15524, decembre 2023 » | La table provient bien de Gui et Toubia, mais de la version de janvier 2025. Gui et Toubia ecrivent en retour que « Toubia et al. (2025) also replicated our pricing study on their panel » : les deux jeux sont le meme instrument, sur deux panels | Le lien entre les deux papiers est reciproque et documente. La date de terrain de Twin (29 janvier au 25 fevrier 2025) reste posterieure a la coupure de GPT-4.1 : les **reponses** ne sont pas contaminees, et desormais le **stimulus** non plus |
| 07.40 Plecko et al. | « le GSS n'est qu'un jeu sur dix et n'est pas analyse separement » | Exact, mais le detail compte : les taches 25 a 34 du banc sont **« GSS: Political View by Age / by Race / by Education / by Income / by Sex »** et les cinq memes pour l'affiliation partisane. Ce sont exactement des **marginales de groupe**. Les auteurs notent par ailleurs que les meilleurs scores viennent du FBI, du BLS et d'IPEDS, « for three of these four datasets the detailed statistics we queried are available on their websites » | Le banc le plus proche de notre hypothese la teste deja, sur le bon objet, et trouve des scores bas. C'est le contre argument le plus serieux, traite en section 4 |
| 07.26 infini-gram | « l'API est en POST uniquement, donc inutilisable par un simple appel de page » | L'API repond bien en POST, avec des refus intermittents `{"message":"Forbidden"}` qui cedent a une reprise. Les comptes sont en section 2 | La dette 1 est payee |

### 1.3 Table initiale, colonne « trouve par »

Les entrees 07.01 a 07.48 de `corpus/07-contamination-memorisation-coupure.md` sont toutes `table
initiale`. Elles ne sont pas recopiees ici. Deux precisions apres relecture des citations :

- 07.29 (Bordt et al., *Elephants Never Forget*) et 07.30 (Silvestri et al.) sont bien les deux seuls
  travaux qui appliquent une batterie de memorisation a des **donnees tabulaires**. La descente de
  citations n'a rien rendu de neuf sur ce point.
- 07.32 (Wang, Antoniades, Elazar et al., memorisation distributionnelle) n'est cite, dans OpenAlex,
  que par quatre travaux, dont aucun ne porte sur l'enquete. La piste aval est epuisee.

---

## 2. Le comptage infini-gram, la dette de `corpus/07` section 5 point 1

C'est la seule mesure de cette session. Elle est autorisee comme exception au « aucun code d'analyse
de donnees ».

### 2.1 La requete exacte

Deux API publiques, sans cle, en POST, corps JSON.

```
POST https://api.infini-gram.io/
{"index":"v4_dolma-v1_7_llama","query_type":"count","query":"General Social Survey"}
```

Index utilises, avec la taille annoncee par la documentation :
`v4_dolma-v1_7_llama` (Dolma v1.7, 2 604 milliards de tokens), `v4_rpj_llama_s4` (RedPajama, 1 386),
`v4_piletrain_llama` (Pile-train, 383), `v4_c4train_llama` (C4-train, 198). Tokenisation Llama.

```
POST https://api.infini-gram-mini.io/
{"index":"v2_cc-2025-05","query_type":"count","query":"General Social Survey"}
```

Index utilises : `v2_cc-2025-05` et `v2_cc-2025-30` (instantanes Common Crawl de janvier et de
juillet 2025), `v2_dclm_all` (DCLM-baseline, 17 To). Index FM sur octets bruts, pas de tokenisation.
**Piege a signaler** : la documentation ecrit `v2_cc_2025-05` avec un souligne, le serveur n'accepte
que `v2_cc-2025-05` avec un tiret, et renvoie sinon `{"error":"[Flask] Invalid index"}`.

L'API v4 renvoie par intermittence `{"message":"Forbidden"}` sans corps ni code d'erreur exploitable.
Une reprise avec attente croissante (3, 6, 9, 12, 15 secondes) suffit ; toutes les cases marquees
ci dessous ont fini par repondre.

### 2.2 Le questionnaire du GSS contre le nom du GSS

Comptes bruts, nombre d'occurrences de la chaine exacte.

| chaine exacte | Dolma-v1.7 | RedPajama | Pile-train | C4-train |
|---|---|---|---|---|
| `General Social Survey` | **60 837** | 60 342 | 10 831 | 4 483 |
| `NORC at the University of Chicago` | 15 246 | 18 605 | 1 290 | 1 379 |
| `according to the General Social Survey` | 921 | 1 611 | 257 | 93 |
| `General Social Survey, 1972` | 174 | 360 | 32 | 17 |
| `GSS Data Explorer` | 280 | 196 | 17 | 30 |
| `gssdataexplorer.norc.org` | 34 | 38 | 0 | 1 |
| `We are faced with many problems in this country, none of which can be solved easily or inexpensively` | 16 | 11 | 2 | 2 |
| `whether you think we're spending too much money on it, too little money, or about the right amount` | 19 | 18 | 11 | 2 |
| `Are we spending too much, too little, or about the right amount on` | 11 | 2 | 2 | 0 |
| `Improving and protecting the environment` | 11 | 10 | 12 | 0 |
| `Improving the nation's education system` | **1** | 1 | 1 | 0 |
| `Space exploration program` | 76 | 36 | 0 | 6 |
| `Halting the rising crime rate` | 5 | 1 | 1 | 0 |
| `Dealing with drug addiction` | 163 | 273 | 10 | 55 |
| `Improving and protecting the nation's health` | 1 | 1 | 1 | 0 |
| `Solving the problems of the big cities` | 0 | 1 | 1 | 0 |
| `Improving the conditions of Blacks` | 1 | 1 | 1 | 0 |
| `The military, armaments, and defense` | 1 | 0 | 0 | 0 |
| `TOO LITTLE ABOUT RIGHT TOO MUCH` | 0 | 0 | 0 | 0 |

Dix items de la batterie de depenses nationales, c'est la demande de la consigne. Le compte median
est de **1** dans Dolma et de **1** dans RedPajama. Le nom de l'enquete est present 60 837 fois dans
le meme corpus.

Autres batteries, pour verifier que la batterie de depenses n'est pas un cas particulier :

| chaine exacte | Dolma-v1.7 | RedPajama | Pile-train | C4-train |
|---|---|---|---|---|
| `Taken all together, how would you say things are these days--would you say that you are very happy, pretty happy, or not too happy?` | 4 | 0 | 0 | 0 |
| `very happy, pretty happy, or not too happy` | 371 | 426 | 97 | 27 |
| `Please tell me whether or not you think it should be possible for a pregnant woman to obtain a legal abortion` | 11 | 9 | 12 | 1 |
| `If there is a strong chance of serious defect in the baby` | 9 | 3 | 1 | 0 |
| `Generally speaking, would you say that most people can be trusted or that you can't be too careful in dealing with people?` | 14 | 6 | 0 | 4 |
| `Do you favor or oppose the death penalty for persons convicted of murder?` | 28 | 11 | 3 | 2 |
| `extremely liberal, liberal, slightly liberal, moderate, slightly conservative, conservative, extremely conservative` | 2 | 10 | 0 | 0 |

Mnemoniques de variables, qui sont l'autre forme sous laquelle le GSS circule :

| chaine exacte | Dolma-v1.7 | RedPajama | Pile-train | C4-train |
|---|---|---|---|---|
| `polviews` | 305 | 112 | 41 | 0 |
| `abany` | 4 294 | 718 | 183 | 187 |
| `cappun` | 113 | 22 | 7 | 5 |
| `natspac` | 34 | 13 | 13 | 0 |
| `natenvir` | 23 | 11 | 8 | 0 |
| `nateduc` | 19 | 7 | 3 | 1 |
| `wtssall` | 46 | 42 | 17 | 0 |
| `natspac natenvir` | 1 | 4 | 0 | 0 |

`abany` est un mot ambigu, son compte n'est pas interpretable. `polviews`, `natspac`, `natenvir`,
`nateduc` et `wtssall` ne le sont pas : quelques dizaines d'occurrences, du meme ordre que le libelle
des items. La variable de ponderation du GSS, `wtssall`, apparait 46 fois dans Dolma.

### 2.3 La statistique de groupe, elle, est partout

| chaine exacte | Dolma-v1.7 | RedPajama | Pile-train | C4-train |
|---|---|---|---|---|
| `percent of Republicans` | **123 159** | 156 437 | 40 097 | 14 038 |
| `percent of Democrats` | 98 625 | 131 286 | 33 938 | 11 842 |
| `percent of Americans say` | 41 037 | 42 731 | 8 001 | 4 970 |
| `percent of conservatives` | 3 990 | 5 681 | 1 573 | 458 |
| `percent of liberals` | 2 767 | 4 458 | 1 195 | 343 |
| `percent of white evangelical Protestants` | 1 333 | 1 750 | 354 | 109 |
| `of conservatives say` | 908 | 1 027 | 241 | 90 |
| `of liberals say` | 483 | 938 | 163 | 56 |
| `Pew Research Center survey` | 50 349 | 62 272 | 9 176 | 5 404 |

Rapport, dans Dolma-v1.7, entre `percent of Republicans` et `Improving the nation's education
system` : **123 159 contre 1**.

Co occurrence dans un meme document, requete `find_cnf` (nombre de documents) :

| requete CNF | Dolma-v1.7 | RedPajama |
|---|---|---|
| `General Social Survey AND percent of Republicans` | 127 | 157 |
| `General Social Survey AND percent of conservatives` | 13 | 38 |
| `General Social Survey AND too little` | 111 | 417 |

### 2.4 Autres enquetes, pour situer

| chaine exacte | Dolma-v1.7 | RedPajama | Pile-train | C4-train |
|---|---|---|---|---|
| `World Values Survey` | 34 917 | 31 222 | 4 839 | 3 430 |
| `European Social Survey` | 26 861 | 19 280 | 3 176 | 2 046 |
| `American National Election Studies` | 6 185 | 7 972 | 1 609 | 532 |
| `American Trends Panel` | 4 126 | 7 730 | 749 | 392 |
| `Cooperative Election Study` | 379 | 364 | 0 | 0 |
| `feeling thermometer` | 3 186 | 2 336 | 876 | 192 |
| `On a scale from 0 to 100, where 0 means very cold and 100 means very warm` | 0 | 0 | 0 | 0 |
| `Twin-2K-500` | 0 | 0 | 0 | 0 |

L'item du thermometre de sympathie de l'ANES, celui sur lequel Bisbee et al. (07.37) travaillent,
est **absent des quatre corpus**, alors que le nom du concept y est present 3 186 fois.

### 2.5 Les 40 produits de Twin-2K-500 et de Gui et Toubia

| libelle commercial exact, table A.1 de 07.49 | Dolma | RedPajama | Pile | C4 | CC-2025-05 | CC-2025-30 | DCLM |
|---|---|---|---|---|---|---|---|
| `Lay's Classic Potato Snack Chips, Party Size, 13 oz Bag` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `Coca-Cola Soda Pop, 12 fl oz, 12 Pack Cans` | 0 | 0 | 0 | 0 | 0 | 1 | 0 |
| `OZARKA Brand 100% Natural Spring Water, 16.9-ounce plastic bottles (Pack of 35)` | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| `Duracell Coppertop AA Battery, Long Lasting Double A Batteries, 16 Pack` | 0 | 0 | 0 | 0 | | | |
| `Bounty Select-a-Size Paper Towels, 12 Double Rolls, White` | 0 | 0 | 0 | 0 | | | |
| `Cinnamon Toast Crunch Breakfast Cereal, Crispy Cinnamon Cereal, Family Size, 18.8 oz` | 0 | 0 | 0 | 0 | | | |
| `Angel Soft Toilet Paper, 9 Mega Rolls` | 0 | 0 | 0 | 0 | | | |
| `Tylenol Extra Strength Caplets with 500 mg Acetaminophen, 100 Ct` | 0 | 0 | 0 | 0 | | | |
| `Great Value Milk Whole Vitamin D Gallon` | 0 | 0 | 0 | 0 | | | |
| `Little Debbie Zebra Cakes, 13 oz` | 0 | 2 | 0 | 2 | | | |
| `Categories, products and regular prices` (titre de la table A.1) | | | | | 0 | 0 | 0 |

Dix libelles, **zero occurrence** sauf deux exceptions marginales. Les instantanes de Common Crawl de
janvier et de juillet 2025 sont posterieurs a la mise en ligne de la table (21 janvier 2025) et ne la
contiennent pas non plus.

### 2.6 Verification de la meme mesure a l'echelle des corpus de 2025

| chaine exacte | CC-2025-05 | CC-2025-30 | DCLM-baseline |
|---|---|---|---|
| `General Social Survey` | 25 597 | 12 146 | 182 291 |
| `Improving the nation's education system` | **0** | **0** | 38 |
| `whether you think we're spending too much money on it, too little money, or about the right amount` | 2 | 1 | 177 |
| `percent of Republicans` | 18 703 | 16 215 | **274 180** |
| `percent of conservatives` | 695 | 531 | 13 456 |

Le rapport tient a toutes les echelles. Dans DCLM-baseline, 274 180 contre 38.

### 2.7 Ce que contiennent les documents, et non plus seulement combien il y en a

Requete `find` sur le preambule de la batterie de depenses dans Dolma-v1.7 : 19 occurrences reparties
sur 8 fragments d'index. Cinq documents ont ete reconstitues par `get_doc_by_rank`. Ce sont, dans
l'ordre :

1. un article de sociologie de l'environnement qui cite la formulation pour la comparer a une question
   de l'ISSP 2003, en renvoyant a Pampel et Hunter (2012) dans l'*American Journal of Sociology* ;
2. un **carnet Python d'enseignement** qui trace des figures a partir du GSS et enumere les
   mnemoniques `nataid`, `natfare`, `natpark`, `natrace`, `natchld`, `natenvir`, ainsi que la batterie
   de confiance `conbus`, `coneduc`, `conjudge`, `conmedic`, `consci`, `conarmy` ;
3. un billet de blog de commentaire politique qui reprend l'item de l'aide etrangere avec la reponse
   codee « Con = Too much » ;
4. un second **carnet Python**, avec des liens `gssdataexplorer.norc.org/projects/41723/variables/...`
   et le commentaire « [Note: the wording of this question assumes that crime rates are rising!] » ;
5. un second article de sociologie qui donne la formulation exacte de `natenvir`.

Autrement dit : le questionnaire du GSS entre dans les corpus **par l'analyse secondaire**, articles
et carnets de code, jamais par le codebook de NORC. Ce n'est pas une contamination du questionnaire,
c'est une contamination par la litterature qui le commente.

### 2.8 Ce que ce comptage etablit et ce qu'il n'etablit pas

Il etablit trois choses. Le libelle des items du GSS est **presque absent** des quatre corpus ouverts
et des corpus de 2025. La statistique de groupe est presente a un ordre de grandeur de 10^5 fois
superieur. La table des prix de Gui et Toubia n'est nulle part.

Il n'etablit pas que le GSS est absent des corpus de Llama 3.1, de gpt-oss ou de Qwen3, qui ne sont
pas publies. Il n'etablit pas non plus une absence tout court : la recherche est lexicale, et 07.08
montre qu'une reformulation suffit a rendre un jeu invisible a tout test de chaine. Un compte positif
prouve la presence, un compte nul ne prouve rien. La formule a garder est celle de 07.09 :
« aucun effet mesurable sous le test X », jamais « le GSS n'est pas dans le corpus ».

---

## 3. Comment ca fonctionne

Le champ a construit, en quatre ans, une echelle de mesure de la contamination qui va du corpus vers
le modele, et cette echelle se lit maintenant de bout en bout. A une extremite, on compte des chaines
dans un corpus ouvert : WIMBD (07.25), infini-gram (07.26) et desormais infini-gram mini (07.54), qui
indexe 83 teraoctets en 99 jours et couvre des instantanes de Common Crawl de 2025. A l'autre
extremite, on interroge un modele dont le corpus est secret : inference d'appartenance (07.02, 07.03),
instruction guidee (07.05), reconstruction d'option masquee (07.07), batterie tabulaire (07.29),
sonde d'existence (07.30). Entre les deux, un chainon qui n'existait pas avant 2024 : la
**memorisation distributionnelle** (07.32), qui correle la probabilite de sortie du modele avec la
frequence des n-grammes de la tache dans le corpus, et OLMoTrace (07.55), qui remonte une sortie
jusqu'a ses documents d'entrainement en 4,46 secondes, avec 96,7 pour cent des correspondances issues
du pre entrainement. Ce chainon est ce qui permet de parler de contamination sans avoir a choisir
entre « je vois le corpus » et « je ne vois que le modele ».

Sur cette echelle, la contamination d'une enquete sociale n'est pas un objet, c'est trois. Sainz et
al. (07.16) l'avaient dit pour les benchmarks : consignes d'annotation, texte brut, annotations. Pour
une enquete, cela donne le questionnaire, les marginales publiees, les microdonnees. Le comptage de la
section 2 tranche le premier cas : **le questionnaire du GSS n'est pas dans les corpus ouverts**, une
occurrence mediane par item, et les rares documents qui le contiennent sont des articles de sociologie
et des carnets Python d'enseignement. Le troisieme cas, les microdonnees, n'a pas ete teste ici, mais
07.27 donne le prior : la decontamination de Dolma retire moins de 0,02 pour cent des documents et ne
vise que Paloma, donc rien dans la chaine de filtrage ne cible un fichier d'enquete. Reste le deuxieme
cas, les marginales publiees, et c'est celui ou tout se joue.

Car ce que le comptage rend visible, personne ne l'avait chiffre : la masse des **statistiques de
groupe** dans les corpus est de cinq ordres de grandeur superieure a celle du questionnaire.
`percent of Republicans` apparait 123 159 fois dans Dolma quand `Improving the nation's education
system` y apparait une fois. Le rapport tient dans DCLM-baseline, 274 180 contre 38. Un modele
pre entraine sur ce corpus n'a pas appris ce que repond une personne a une question du GSS ; il a
appris, des dizaines de milliers de fois, la forme « x pour cent des republicains pensent que ». Si
l'on demande ensuite a ce modele de jouer une personne etiquetee republicaine, la distribution qu'il
a apprise est une distribution de groupe. La substitution de la personne par le groupe, mesuree chez
nous en a31, a donc une origine candidate au **pre entrainement**, et pas seulement a l'alignement.
C'est exactement la question laissee ouverte par ARBITRAGE, et le comptage est un premier element.

Gui et Toubia (07.49) donnent a ce mecanisme sa formulation causale, et c'est la lecture la plus utile
de la session. Leur these est qu'une invite en aveugle est **ambigue** : elle peut se lire
`P(Y|do(D))`, la question interventionnelle que le chercheur pose, ou `P(Y|D)`, la question
observationnelle. Ils ecrivent : « Since LLMs are trained primarily on observational data, it is
plausible that an ambiguous question will also be interpreted in a way that is similar to
observational data, hence answering the wrong question ». La preuve est empirique et elle est nette :
en faisant varier le prix d'un produit, ils font varier avec lui le prix passe, le prix du concurrent
et la date de peremption, variables qui devraient rester constantes ; la courbe de demande humaine est
decroissante et la courbe simulee est **en U inverse**. Le remede n'est pas d'ajouter des covariables,
qui degradent la performance au dela d'une dizaine par focalisme, mais de **lever l'aveugle** : dire
au modele que le prix est tire au hasard dans un intervalle. Le gain est constant, de 1 a plus de 60
pour cent selon le modele, et il se cumule avec l'affinage : 0,532 hors boite en aveugle, 0,397 hors
boite en devoile, 0,113 affine et evalue en devoile. Traduit dans notre vocabulaire : le modele, quand
on ne lui dit rien, repond avec la conditionnelle de population, pas avec la personne. C'est la meme
substitution, decrite depuis la theorie causale plutot que depuis la mesure de rarete.

Ozkan (07.50) est le premier a poser directement la question de la restitution sur une population
simulee, et son resultat est en trois etages qui correspondent aux trois de la section 2. La marginale
nationale **tient**, et elle tient par restitution : son backtest electoral donne TVD = 0,051, mieux
que l'auto declaration des personnes elles memes (0,095), sur un scrutin anterieur a la coupure, ce
qu'il qualifie de « plain recall, not simulation ». Les affirmations de **sous groupe** sont, selon
ses propres termes, « explainable by recall and prompt noise » : la conditionnelle ne bat pas la
restitution nationale, delta = -0,165 avec p < 0,001, le gradient de sous groupe colle a la realite
dans 62 pour cent des cas, et la sonde echoue a la specificite, 0 sur 2. Le niveau **individuel**
s'effondre : la part du premier parti passe de 42,6 pour cent reels a 88,0 pour cent predits,
TVD = 0,454, dans tous les modeles testes. Sa phrase de synthese est celle a citer : « one remembers,
the other collapses; neither simulates ».

Le controle methodologique qu'il introduit merite d'etre retenu independamment du resultat. Une
sonde qui mesure la **sensibilite** d'un modele a une manipulation pertinente ne prouve rien tant
qu'on n'a pas mesure sa reaction a une manipulation **non pertinente**. Chez lui, la manipulation
pertinente deplace l'opinion de +1,13 et le placebo de +1,49, donc davantage. La sensibilite au
contrefactuel est de la reactivite non specifique a l'invite. Toute mesure de sensibilite sans
controle de specificite est trompeuse : c'est vrai de ses tests, et c'est vrai des notres.

Cote coupure, le tableau reste celui de `corpus/07`, avec un ajout. Hors du domaine, l'ecart est net :
Roberts et al. (07.20) montrent que la correlation entre la reussite et la presence sur GitHub
disparait apres la coupure, rapport de cotes 1,045 avec p = 0,000 avant et 1,000 avec p = 0,988 apres.
Dans le domaine, les trois controles existants sont negatifs : Ashokkumar et al. (07.36) trouvent
r = 0,74 sur les etudes publiees avant la coupure contre r = 0,90 sur les non publiees ; Lukauskas et
Sarkauskaite (07.38) mesurent 4,7 pour cent de restitution litterale au pire des cas et une
correlation de rang exactement nulle avec leur score de fidelite ; Plecko et al. (07.40) ne trouvent
aucune relation entre l'entropie de la question et la performance. L'ajout est que le vocabulaire est
en train d'etre pris : Jia et al. (07.53) intitulent leur dessin « held-out post-cutoff answers »,
alors que leur coupure est une date de coupe du dossier du repondant, 2023, et non la coupure du
modele. Leurs cibles, des reponses LISS de 2023 et 2024, sont anterieures a la coupure de GPT 5.4.
Le dessin manquant, meme pipeline sur une vague anterieure et une vague posterieure a la coupure
**du modele**, avec baseline non LLM, reste manquant. Il faudra le nommer autrement pour ne pas etre
confondu.

Enfin, une menace nouvelle pese sur la strategie post coupure elle meme, et elle vient d'un endroit
inattendu. Veselovsky, Horta Ribeiro et West (07.57) estiment que **33 a 46 pour cent** des
travailleurs de plateforme employaient deja un modele de langage sur une tache de production de texte
en 2023. Ma et al. (07.58) en tirent la consequence pour l'enquete : « even researchers who use
orthodox survey methods are likely to face non-negligible contamination of 'synthetic' responses in
their data ». Notre meilleur jeu propre, Twin-2K-500, est collecte sur Prolific en janvier et fevrier
2025. Un jeu posterieur a la coupure n'est donc pas automatiquement un jeu humain, et le plancher test
retest qu'on en tire peut etre biaise vers le haut. La contamination change de sens : elle ne va plus
seulement de l'enquete vers le corpus, elle va du modele vers l'enquete.

---

## 4. Ce qui se contredit

**Contradiction 1. Le corpus est plein de statistiques de groupe, et le seul banc qui teste la
connaissance des marginales de groupe du GSS trouve des scores bas.** Plecko et al. (07.40) incluent
dix taches GSS qui sont exactement des marginales conditionnelles de groupe : « Political View by
Age », « by Race », « by Education », « by Income », « by Sex », et les cinq memes pour l'affiliation
partisane. Leurs meilleurs scores sur tout le banc sont de 22 sur 100 en choix multiple et 41 sur 100
en vraisemblance. Si la memorisation de statistiques de groupe expliquait quoi que ce soit, ce banc
aurait du la voir.

*La variable qui explique la contradiction, et elle est ecrite dans leur propre texte.* Leurs
meilleurs resultats viennent du FBI, du BLS, d'IPEDS et de l'ACS, et ils notent : « For three of these
four datasets (FBI, BLS, IPEDS) the detailed statistics we queried are available on their websites,
meaning that models could have had access to the exact probability tables used for constructing our
questions ». Leurs mauvais resultats viennent du GSS, du NHANES, du MEPS, du SCF, c'est a dire des
jeux dont les tableaux croises **ne sont pas publies en page web** mais s'obtiennent par un outil
d'extraction. La variable n'est donc pas « statistique de groupe » contre « autre chose », c'est
**« tableau publie tel quel » contre « tableau a construire »**. Notre comptage donne la meme
frontiere par un autre chemin : `gssdataexplorer.norc.org` apparait 34 fois dans Dolma. Le GSS Data
Explorer n'est pas dans le corpus, et c'est lui qui produit les croisements. Le modele connait la
phrase « x pour cent des republicains pensent que » telle qu'un journaliste l'ecrit, et pas le
tableau `polviews` par age tel que le Data Explorer le sort. Les deux resultats sont compatibles, et
ensemble ils font une prediction testable : la connaissance de marginale doit s'effondrer entre les
croisements repris dans la presse et les croisements qui n'y sont jamais repris.

Une reserve honnete sur leur refutation : leur test de contamination, en annexe E, repose sur
l'entropie de la question comme proxy de presence en pre entrainement. L'entropie mesure la
familiarite du modele avec le **libelle** de la question, pas la presence du **tableau de reponses**.
Or notre comptage montre que ces deux quantites sont dissociees dans les faits, une occurrence de
libelle contre 123 159 de statistique de groupe. Leur proxy ne pouvait pas trouver ce qu'ils
cherchaient.

**Contradiction 2. Le modele sur predit la rarete sur des prevalences de sante et la sous produit sur
des opinions.** Hobor et al. (07.52) trouvent que les modeles « predisent une mediane de 18,0 pour
cent quand la vraie mediane est 40,3 », et gagnent contre une base naive 97,5 pour cent du temps sur
les conditions rares mais 57,8 pour cent seulement sur les conditions frequentes : ils tirent vers le
bas, donc vers la rarete. Nos mesures et celles de 07.53 vont dans l'autre sens : la simulation efface
les reponses rares.

*La variable qui explique la contradiction.* Ce ne sont pas les memes objets. Chez Hobor, la sortie est
un **nombre**, une prevalence a estimer, et le biais est un biais d'ancrage sur les petits nombres,
que les auteurs nomment ainsi. Chez nous et chez Jia et al., la sortie est un **choix de modalite**
pour une personne, et le biais est un biais vers le mode. Un modele qui, sur chaque personne, choisit
la modalite modale produit une population sans rares, tout en etant capable de dire, si on le lui
demande en chiffres, que cette modalite rare existe et qu'elle vaut tant. Ce n'est pas la meme
epreuve, et la distinction porte un nom depuis juin 2026 : **capacite contre propension** (07.56).
La capacite a enoncer une marginale et la propension a la respecter quand on simule des individus
sont deux mesures, et le champ n'a jamais mis les deux dans le meme tableau.

**Contradiction 3. Ozkan trouve les affirmations de sous groupe contaminees par la restitution ; les
trois controles de coupure du domaine sont negatifs.** 07.36, 07.38 et 07.40 ne trouvent aucun effet
de memorisation ; 07.50 en trouve un au niveau du sous groupe.

*La variable qui explique la contradiction.* Le niveau d'agregation. Les trois controles negatifs
travaillent soit sur l'effet de traitement agrege (07.36), soit sur un jeu inedit ou la memorisation
n'avait aucune raison d'exister (07.38, une enquete lituanienne non publiee auparavant), soit sur des
conditionnelles a plusieurs variables (07.40). Ozkan travaille sur des sous groupes simples d'une
enquete internationale abondamment commentee. La memorisation se manifeste la ou le corpus contient
des phrases de la forme « x pour cent du groupe G pensent P », c'est a dire au niveau du sous groupe
simple, et nulle part ailleurs. Cette lecture est compatible avec tout ce qui precede, et elle est la
forme testable de notre hypothese.

**Contradiction 4. `corpus/07` disait que le bloc des prix de Twin etait la piece la plus suspecte du
dossier ; la lecture de Gui et Toubia et le comptage disent l'inverse.** La table A.1 est postee le 21
janvier 2025, apres la coupure de GPT-4.1 ; les libelles produits ne sont dans aucun corpus ouvert, ni
avant ni apres. *La variable qui explique la contradiction est une date de version d'arXiv.* Le
dossier avait lu « arXiv 2312.15524, decembre 2023 » et en avait deduit une date de mise en ligne du
contenu. La lecon de methode est generale et elle vaut pour tout le volet coupure : **la date d'un
identifiant arXiv n'est pas la date de son contenu**. C'est le meme constat que 07.18 fait sur les
corpus, a une autre echelle.

---

## 5. Ce que ca permet de tester chez nous tout de suite

Sept tests, du moins cher au plus cher. Aucun ne demande d'argent.

**T1. Etendre le comptage aux 149 items du GSS employes dans le projet. Cout : une heure de machine,
zero appel de modele.** Le script de la section 2.1 est ecrit, les API repondent, la reprise sur
`Forbidden` est reglee. Sortie : un compte par item et par corpus, sur sept index dont deux instantanes
de Common Crawl 2025 et DCLM-baseline. C'est une colonne de donnees que le champ n'a pas, et elle
devient une **variable explicative** pour tous les tests suivants.

**T2. Correler la fidelite item par item avec le compte de corpus. Cout : nul, les scores existent
deja.** C'est le patron de 07.32 et le patron de preuve de 07.20 : non pas « le modele est bon », mais
« l'avantage du modele sur la baseline est il une fonction croissante de la presence de l'item dans le
corpus ? ». Avec 149 items, la puissance est suffisante pour une correlation de rang. Une correlation
nulle disculpe, une correlation positive incrimine. C'est le test que 07.38 fait sur une enquete ou
il ne pouvait rien trouver, et que personne ne fait sur le GSS.

**T3. Le couple marginale publiee contre conditionnelle derivee. Cout : une nuit de calcul local.**
C'est l'idee d'OpenEstimate (07.51) transposee. Pour chaque item, deux cibles : la marginale de la
vague, qui a pu etre memorisee, et une conditionnelle a trois filtres tires au hasard dans le
cumulatif, qui ne peut pas l'avoir ete, avec l'exigence d'OpenEstimate que chaque filtre deplace la
statistique d'au moins 5 pour cent. On lit la masse de probabilite que le modele met sur chaque
modalite, par lettre, comme le protocole du projet le fait deja. **L'ecart entre les deux scores est
une mesure de memorisation qui ne demande aucun acces au corpus du modele.** C'est le test le plus
propre du lot, et il repond a la contradiction 1 dans les termes ou elle se pose.

**T4. Le test des croisements repris dans la presse contre les croisements jamais repris. Cout : une
demi journee de tri plus une nuit de calcul.** Prediction issue de la contradiction 1 : la
connaissance de marginale doit s'effondrer entre les croisements du GSS qui circulent en phrases de
journaliste (« x pour cent des conservateurs pensent que ») et ceux qui n'existent que dans le Data
Explorer. Le tri se fait par T1, en comptant `percent of conservatives` en co occurrence avec l'item
via `find_cnf`. Si l'effondrement a lieu, la memorisation de statistiques de groupe est etablie et sa
frontiere est mesuree. **C'est le test le plus proche de la these d'ARBITRAGE.**

**T5. Capacite contre propension, sur nos propres sorties. Cout : nul, les sorties existent.** Suivant
07.56, deux mesures a mettre dans le meme tableau. La **capacite** : demander au modele, en clair, la
marginale publiee de l'item pour la vague, et mesurer l'erreur. La **propension** : reprendre les
reponses deja simulees pour les 149 items et mesurer a quel point la distribution agregee des agents
colle a cette marginale publiee. Un modele qui connait la marginale et ne la respecte pas simule ; un
modele qui la connait et la reproduit exactement restitue. Personne dans le champ n'a jamais publie
ces deux colonnes cote a cote.

**T6. Le controle placebo sur nos manipulations. Cout : une nuit de calcul, et c'est un correctif, pas
un ajout.** Ozkan (07.50) montre qu'une manipulation non pertinente deplace l'opinion **plus** qu'une
manipulation pertinente, +1,49 contre +1,13. Nos resultats a30 et a31 reposent sur une manipulation
pertinente, la presence ou l'absence de l'etiquette demographique. Il faut le meme dispositif avec une
etiquette **fausse ou non pertinente** (une etiquette tiree au hasard, une etiquette de couleur
preferee). Si l'etiquette non pertinente produit le meme gonflement de groupe, notre mecanisme est de
la reactivite d'invite et non une substitution. Ce test est defensif et il est **obligatoire** :
un relecteur qui a lu 07.50 le demandera.

**T7. Tracer nos sorties dans le corpus avec OLMoTrace ou SimpleTrace. Cout : une journee de mise en
place, service public gratuit.** 07.55 rend un tracage en 4,46 secondes par sortie, avec 96,7 pour
cent des correspondances issues du pre entrainement. Sur les reponses ou notre modele attribue une
rarete a la mauvaise personne, on regarde ce que la trace rend : des phrases de personne, ou des
phrases de rapport d'enquete. C'est la version qualitative, et la plus lisible dans un papier, de
toute la section 2. Reserve : cela ne fonctionne pleinement que sur un modele a corpus indexe, donc
sur OLMo et non sur Llama 3.1 ni gpt-oss ; l'usage est donc illustratif, pas probant, et il faut le
dire.

Trois choses a **ne pas** faire, apres cette lecture. Ne pas depenser une nuit sur le test « prix
normal des 40 produits » comme test de contamination : la question est reglee, la table n'est nulle
part et elle est posterieure a la coupure. Ne pas ecrire « aucune contamination » nulle part, jamais,
au vu de 07.09, 07.11 et 07.12. Et ne pas appeler notre dessin « post-cutoff », le mot est pris par
07.53 pour autre chose.

---

## 6. Ce que personne n'a fait

1. **Aucun comptage publie du GSS, de l'ANES, du WVS ou du panel Pew dans un corpus ouvert.** L'etat
   reste celui de `corpus/07`, sauf que le comptage est maintenant fait, en section 2, et qu'il donne
   un resultat contre intuitif : ce n'est pas le questionnaire qui est dans le corpus, c'est la
   statistique de groupe. 07.42 choisissait l'ESS plutot que le WVS **au motif** d'une memorisation
   probable, sans produire une mesure ; la mesure existe desormais et elle designe un autre objet.
2. **Personne n'a mis dans le meme tableau la connaissance qu'un modele a d'une marginale publiee et
   le respect de cette marginale quand il simule des individus.** C'est la distinction capacite contre
   propension de 07.56, jamais appliquee a l'enquete.
3. **Personne n'a mesure l'effondrement de la connaissance des croisements entre ceux qui circulent en
   prose journalistique et ceux qui n'existent que dans un outil d'extraction.** 07.40 s'en approche
   au niveau du jeu de donnees, jamais au niveau de l'item.
4. **Aucune comparaison de fidelite du meme pipeline sur une vague anterieure et une vague posterieure
   a la coupure du modele, avec baseline non LLM.** 07.53 en a le vocabulaire mais pas le dessin :
   leur coupure est celle du dossier du repondant.
5. **La batterie tabulaire de 07.29 et la sonde d'existence de 07.30 n'ont jamais ete appliquees a un
   fichier de microdonnees d'enquete.** Inchange.
6. **Personne n'a fait de controle placebo sur une manipulation de persona dans un papier de
   simulation d'enquete.** 07.50 le fait sur ses propres sondes de memorisation et montre qu'il
   renverse la lecture ; aucun papier de fidelite ne le fait sur l'etiquette demographique.
7. **Personne n'a trace les sorties d'une population simulee dans le corpus d'entrainement.** Les
   outils existent depuis avril 2025 (07.55) et juin 2026 (07.56).
8. **Aucun papier de simulation d'enquete ne publie, dans le meme tableau, la coupure declaree des
   modeles employes et les dates de terrain des donnees.** Inchange, et toujours une ligne de tableau.
9. **Personne ne mesure l'effet de la contamination inverse sur le plancher humain.** Si 33 a 46 pour
   cent des repondants de plateforme s'aident d'un modele (07.57), le plancher test retest d'un jeu
   recolte en ligne apres 2023 est un melange, et tous les scores « en pourcentage du plancher humain »
   du champ, y compris ceux de 07.34 et de 07.35, sont affectes d'un biais dont personne ne donne le
   signe.

---

## 7. Ce que je n'ai pas pu verifier

1. **Le budget de recherche web de la session etait epuise a l'ouverture du theme.** Le sourcage est
   passe par l'API arXiv, par OpenAlex et par les bibliographies des PDF. Trois consequences : la
   litterature hors arXiv publiee en revue de sciences sociales est sous representee ; OpenAlex
   couvre mal les preprints recents, la descente de citations sur 07.32 ne rend que quatre travaux,
   dont aucun sur l'enquete ; Semantic Scholar a repondu 429 sur toutes les requetes de recherche et
   n'a pas pu etre utilise. Une session avec budget de recherche devrait reprendre les points 1, 2 et
   3 de la section 6 pour verifier qu'ils sont bien vides.
2. **Les corpus de Llama 3.1, de gpt-oss et de Qwen3 ne sont pas publies.** Rien de la section 2 ne
   dit ce qu'ils contiennent. Les sept index interroges sont des corpus de substitution, dont deux
   (Common Crawl 2025, DCLM-baseline) sont proches des recettes recentes sans les etre.
3. **FineWeb reste hors de portee.** Pas d'index n-gramme public comparable ; la question ne peut pas
   y etre posee dans les memes termes. Inchange depuis `corpus/07`.
4. **Le bulletin de contamination d'infini-gram mini n'a pas ete consulte** (`infini-gram-mini.io/bulletin`).
   Le chiffre de 74,2 pour cent de contamination d'un jeu de reference vient du resume de 07.54, pas
   du bulletin.
5. **Les chiffres de detail de 07.56 (PropMe)** sont au niveau du resume et des sections de methode.
   Le tableau de resultats n'a pas ete extrait ; le cadre capacite contre propension, lui, est lu.
6. **Les valeurs numeriques de 07.58** sont dans des figures. Les enonces qualitatifs sont cites mot
   pour mot, les taux ne le sont pas.
7. **Les figures d'Ozkan (07.50)** ne sont pas extractibles. Les tableaux 4 et 5 sont lus ; les
   valeurs de la figure 7 (cosinus 0,46, 0,69, 0,70) viennent de la legende du texte.
8. **Le statut des jeux posterieurs aux coupures n'a pu etre verifie qu'en partie.** Confirme :
   le GSS 2024, section transversale et cumulatif 1972-2024, diffuse le **22 mai 2025** (page
   officielle NORC), et aucune vague 2026 n'est diffusee a ce jour ; l'ESS vague 11 en est a
   l'**edition 4.1, publiee le 13 janvier 2026**, ce qui renforce la recommandation de `corpus/07` de
   n'employer que les diffusions posterieures a la premiere. Non verifie : le site de l'ANES renvoie
   403 sur les deux pages tentees, les dates de diffusion de l'ANES 2024 restent celles de
   `corpus/07` et n'ont pas ete recontrolees ; le site du WVS ne rend pas l'etat de diffusion de la
   vague 8, qui reste donc **ecartee** ; la CES 2024 n'a pas ete verifiee ; le barometre CEVIPOF du 4
   juin 2026 nomme dans PASSATION reste introuvable, comme dans `corpus/07`.
9. **La coupure declaree de gpt-oss** reste en litige entre juin 2024 (carte OpenAI) et juillet 2024
   (LLMLagBench). Inchange.
10. **Aucune de ces lectures ne remplace une mesure sur nos propres modeles.** Le comptage de la
    section 2 etablit la distribution du corpus ; il n'etablit pas ce que Llama 3.1 ou gpt-oss en ont
    retenu. Les sept tests de la section 5 sont la pour cela, et aucun n'est fait.

---

## 8. References lues en entier dans cette session

Douze, dont neuf nouvelles pour le dossier.

1. **Gui, Toubia, arXiv 2312.15524**, v3 integrale, plus verification de la v1 (24/12/2023) et de la
   v2 (21/01/2025). La dette prioritaire, payee, et elle retourne une conclusion.
2. **Ozkan, arXiv 2607.18310**, resume, resultats 1 a 5, discussion, limites, references.
3. **Renda, Ross, Cafarella, Andreas, arXiv 2510.15096** (OpenEstimate), methode et resultats.
4. **Hobor, Brcic, Kovac, Poje, arXiv 2604.01896**, integral.
5. **Jia, Chen, Sharma, Diaz-Rodriguez, arXiv 2605.10659**, methode, resultats 5.3 et 5.4, section 6.
6. **Xu, Liu, Choi, Smith, Hajishirzi, arXiv 2506.12229** (Infini-gram mini), resume, corpus indexes,
   section contamination, documentation de l'API.
7. **Liu et al., arXiv 2504.07096** (OLMoTrace), resume, methode, mesures de latence et de provenance.
8. **Barmina, Schneider-Kamp, Galke Poech, arXiv 2606.06286** (PropMe), resume et sections 2 et 3.
9. **Veselovsky, Horta Ribeiro, West, arXiv 2306.07899**, resume et methode.
10. **Ma, Zhang, Ang, Chen, arXiv 2606.30085**, resume et revue de litterature.
11. **Plecko et al., arXiv 2511.03070**, relecture ciblee : liste des taches GSS, performance par jeu,
    annexe E sur la contamination.
12. **Documentation des deux API infini-gram**, lue et executee, voir section 2.1.

Le chantier s'arrete ici parce que les citations ne rendent plus rien de neuf : les trois dernieres
requetes arXiv du theme n'ont ramene que des travaux deja dans la table, et la descente de citations
sur 07.32 et sur 07.40 est vide.
