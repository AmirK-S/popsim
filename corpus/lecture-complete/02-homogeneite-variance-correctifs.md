# Theme 02, lecture complete. Homogeneite, variance, stereotypes, correctifs

Passe de lecture complete lancee le 8 septembre 2026 au soir, methode de
`corpus/lecture-complete/00-CONSIGNE.md`, grille de `corpus/00-GRILLE.md`. Base de depart :
`corpus/02-homogeneite-variance-correctifs.md`, 45 lignes, 35 en [CONFIRME]. Lectures integrales
deja faites et non refaites ici : `resultats/a26-collisions-2608-03044-et-2609-00565.md` (arXiv
2608.03044 et 2609.00565) et `resultats/a27-lecture-2607-25292.md` (arXiv 2607.25292). Elles sont
citees, pas rejouees.

**Ce que cette passe ajoute.** 14 references lues en entier ou corps et resultats complets, dont
aucune ne figure dans la table de depart, plus une douzaine lues au resume. Elles ont ete trouvees
en descendant les citations de quatre points d'ancrage (Bisbee et al. 2024 par OpenAlex, Wang,
Morgenstern et Dickerson 2024 par Semantic Scholar, Orlikowski et al. 2023 par Semantic Scholar,
Qin, Li et Cheng 2026 par Semantic Scholar) et en remontant celles d'Orlikowski vers la statistique
d'enquete. Trois resultats changent le dossier :

1. **La double distorsion est un theoreme d'imputation, pas une propriete des modeles de langage.**
   L'imputation par la valeur predite ecrase la variance residuelle et gonfle les relations portees
   par le modele d'imputation. C'est ecrit, chiffre et enseigne depuis Little et Rubin. Voir L02-12.
2. **La substitution de la personne par son groupe est mesuree, sur Twin-2K-500, avec le materiel
   individuel complet.** Peng et al., 19 etudes preenregistrees, 164 resultats : les jumeaux a
   persona complete sont **plus proches des jumeaux construits sur les seules demographies que des
   humains qu'ils copient**. C'est la these de `ARBITRAGE.md` mesuree par une autre equipe, sur le
   jeu que popsim compte utiliser. Voir L02-01.
3. **L'anisotropie de la compression selon la sensibilite de l'item n'est plus seulement une phrase
   en passant chez Bisbee.** Zhang, Xu et Alvero la mesurent sur du texte libre, et Peng et al. la
   mesurent sur 55 resultats etiquetes "social desirability". Voir L02-01, L02-13, et la section
   "Ce que personne n'a fait", qui doit etre reecrite.

Convention de certitude inchangee : [CONFIRME] texte lu dans cette session, [PROBABLE] resume lu
dans cette session, [NON LU] titre seulement. [DEDUCTION] marque un raisonnement de cette note et
non un resultat publie. Forme : francais, aucun tiret cadratin ni demi cadratin, citations exactes
en anglais.

---

## A. Table etendue

Colonnes de `corpus/00-GRILLE.md`, plus la colonne "trouve par". Les identifiants L02 continuent la
numerotation T02 de la table de depart, qui n'est pas recopiee ici.

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | trouve par | certitude |
|---|---|---|---|---|---|---|---|---|---|---|
| L02-01 | Tianyi Peng, George Gui, Melanie Brucks, Daniel J. Merlau, Grace Jiarui Fan, Malek Ben Sliman, Eric J. Johnson, Olivier Toubia et 14 autres (Columbia, Yale, Yeshiva), *Digital Twins are Funhouse Mirrors: Five Systematic Distortions*, arXiv 2509.19088 v5 du 19 avril 2026, publie dans Science Advances 2026, doi 10.1126/sciadv.aeh8260. https://arxiv.org/abs/2509.19088 | un jumeau numerique nourri de plus de 500 reponses reelles par personne reproduit-il la personne ? | **Twin-2K-500**, 19 sous etudes preenregistrees, **164 resultats**, humains et leurs jumeaux apparies un a un | GPT-4.1 (2025-04-14) en principal, temperature 0,7 et 0 ; plus GPT-5, DeepSeek-R1, Gemini-2.5-flash, Gemini-3-pro, un GPT-4.1 ajuste sur Twin-2K-500, et Centaur 70B | **quatre mesures, dont deux avec appariement individuel.** Exactitude individuelle 1 moins l'ecart absolu normalise par l'etendue ; **correlation entre humains et jumeaux, calculee a travers les participants pour chaque resultat** (et non a travers les questions pour chaque participant, difference qu'ils soulignent contre Park et al.) ; Glass's Delta sur les moyennes ; **ratio d'ecarts types jumeau sur humain, resultat par resultat**. Plus trois distances MAD entre familles de jumeaux | exactitude : persona complete **0,748**, demographies seules **0,746** (difference non significative, p = 0,37), persona vide 0,734, tirage uniforme 0,629. Correlation : persona complete **0,197**, demographies seules 0,145, persona vide 0,080, hasard 0,001 ; meilleure configuration GPT-4.1 a temperature 0, r = 0,232. **L'ecart type du jumeau est inferieur a celui de l'humain dans 154 des 164 resultats, soit 93,9 pour cent, significativement dans 140.** Moyennes : ecart moyen de 0,352 ecart type, difference significative dans 105 resultats sur 164, soit 64,0 pour cent. **MAD persona complete contre demographies seules 0,132 ; contre persona vide 0,175 ; contre humains 0,252** (les deux ecarts p < 0,01). Cas de dissociation : r_demo = 0,105 contre r_full = 0,555 pour une exactitude quasi inchangee, 0,892 contre 0,907 | pas de decomposition inter et intra nommee : le ratio d'ecarts types est calcule par resultat sur toute la population appariee, pas par segment. Les valeurs du ratio sont dans les figures 2, 10 et 16, pas dans le texte. Aucun plancher de reinterrogation ; l'exactitude du hasard a 0,629 montre que l'echelle absolue ne veut rien dire | **c'est la these de popsim, mesuree par une autre equipe, sur Twin-2K-500.** Trois faits a integrer : (a) l'enrichissement individuel massif n'ameliore pas l'exactitude par rapport a l'etiquette demographique seule ; (b) les jumeaux sont **plus proches des agents a etiquette que des personnes** ; (c) les auteurs ecrivent que les reponses sont "overly shrunk towards a base model", ce qui est le vocabulaire du retrecissement statistique. Ils fournissent aussi la dissociation exactitude contre correlation que le dossier croyait inedite. **Et la correlation est significativement plus basse sur les resultats ou la desirabilite sociale est saillante**, 55 resultats sur 164 | citation aval de Bisbee et al. 2024, OpenAlex | [CONFIRME], PDF v5 relu par `pdftotext -layout`, 7 004 lignes, annexes comprises |
| L02-02 | Yuanming Shi (Adobe), Andreas Haupt (Stanford), *The Collapse of Heterogeneity in Silicon Philosophers*, arXiv 2604.23575 v2 du 29 avril 2026, AIES 2026, doi 10.1145/3805689.3806760. https://arxiv.org/abs/2604.23575 | les echantillons de silicium preservent-ils le desaccord d'une communaute d'experts ? | **277 philosophes professionnels** de PhilPeople, profils publics, 100 questions du PhilPapers Survey, 5 870 reponses humaines ; validation croisee contre le **PhilPapers 2020 Survey, N = 1 785** | GPT-4o, GPT-5.1, Claude-Sonnet-4.5, Llama-3.1-8B, Llama-3.1-8B ajuste par DPO, Mistral-7B, Qwen-3-4B | **variance intra question, avec referent humain, plus structure de correlation.** Table 1 : "Per-Q Var = average within-question variance". Plus effets de specialite testes par khi deux a correction de Yates contre deux verites terrain ; matrices de correlation 100 fois 100 comparees par test de Mantel et coefficient RV ; entropie de Shannon par question ; analyse en composantes principales | **variance intra question : humains 0,053 ; GPT-4o 0,014 ; GPT-5.1 0,014 ; Qwen-3-4B 0,016 ; Llama-3.1-8B ajuste 0,019 ; Claude-Sonnet-4.5 0,026 ; Llama-3.1-8B 0,026 ; Mistral-7B 0,028**, soit le "1.9 to 3.9 times lower variance than human philosophers" du resume. La correlation humaine la plus forte vaut 0,80 en valeur absolue ; **les modeles produisent des correlations de 1,0 pour certains couples specialite vers question, "due to near-uniform responses within specialist groups"**. Taux de correlations significatives 7,6 a 9,0 pour cent contre 4,1 pour cent chez les humains. Effets fabriques : Philosophie de la biologie vers identite personnelle biologique, **11,4 points de pourcentage non significatif chez l'humain contre environ 43 points chez les modeles**, quatre modeles sur sept a p < 0,001 ; Philosophie ancienne vers raison pratique aristotelicienne, **1,9 point non significatif contre 68,9 points, sept modeles sur sept**. Effet reel reproduit : Philosophie de la religion vers argument cosmologique, 40,3 points chez l'humain, 60,1 chez Claude. **La RMSE par question correle a 0,75 avec la variance de la verite terrain.** Six premieres composantes : 71,1 pour cent de variance chez les humains contre 83,0 chez GPT-4o et 81,6 chez GPT-5.1 | 277 profils auto declares, biais nord americain, 61,1 pour cent de manquants chez les humains contre 17 a 40 chez les modeles, imputation par PCA iterative pour la seule ACP. Les groupes sont des specialites declarees, pas des demographies. Pas de plancher de reinterrogation | **soutient l'ensemble de la these, sur un axe non demographique.** Trois apports uniques : (a) une variance intra groupe avec referent humain **sur des groupes d'appartenance professionnelle** ; (b) la phrase de mecanisme la plus nette du corpus, "**LLMs anchor on demographic labels to assign stereotypical stances**" ; (c) le fait que la predictibilite du modele suit la convergence humaine, r = 0,75, donc le modele est juste la ou il n'y a rien a dire. Le contre exemple de biologie vers biologique suggere en plus un mecanisme lexical, "the surface-level lexical overlap between biology and biological may explain this spurious prediction" | citation aval de Bisbee et al. 2024, OpenAlex | [CONFIRME], PDF v2 relu par `pdftotext -layout` |
| L02-03 | Matthias Orlikowski, Paul Rottger, Philipp Cimiano, Dirk Hovy, *The Ecological Fallacy in Annotation: Modelling Human Label Variation goes beyond Sociodemographics*, ACL 2023, arXiv 2306.11559 v1 du 20 juin 2023. https://arxiv.org/abs/2306.11559 | les attributs socio demographiques ameliorent-ils la prediction du comportement individuel d'un annotateur ? | Kumar et al. 2021, echantillon de **5 002 annotateurs, 111 780 annotations, 22 360 commentaires**, 20 a 120 annotations par annotateur ; attributs genre, age, education, orientation sexuelle | RoBERTa avec une tete par annotateur (modele multi annotateurs de Davani et al. 2022), plus des couches specifiques de groupe, **plus un temoin a assignation de groupe randomisee a tailles de groupes preservees** | **gain de performance apporte par le groupe, avec temoin de permutation.** F1 macro par groupe, trois iterations de validation croisee a quatre plis, tests de significativite par analyse de replicabilite de Dror et al. et bootstrap apparie | **aucun gain significatif.** Genre : hommes 68,00 pour la reference, 67,66 pour le modele socio demographique, 67,63 pour le temoin randomise ; femmes 62,23 / 62,25 / 62,41 ; non binaires 56,33 / 56,80 / 58,00. Meme absence sur l'age, l'education et la sexualite. **Pour la plupart des groupes, le modele a groupes randomises obtient la meilleure moyenne** | une seule tache, la toxicite, une seule population, les Etats Unis, quatre attributs pris un a un et jamais croises. Les auteurs notent que le gain pourrait apparaitre en croisant les attributs, ou sur des jeux ou le contenu vise les groupes analyses | **c'est le pont le plus propre entre popsim et la statistique.** La citation de reference du champ y est faite explicitement : "aggregate group behaviour does not necessarily explain individual behaviour (Robinson, 1950; Freedman, 2015)". Et le temoin de permutation par assignation aleatoire de groupe est **exactement notre controle de permutation de a1 et a6**, publie trois ans avant. C'est aussi la source de la formule "the risk of the ecological fallacy in annotator modelling" | table de depart absente, trouve par recherche arXiv sur "ecological fallacy language model" | [CONFIRME], PDF relu par `pdftotext -layout` |
| L02-04 | Tiancheng Hu, Nigel Collier (Cambridge), *Quantifying the Persona Effect in LLM Simulations*, ACL 2024, arXiv 2402.10811 v2 du 17 juin 2024. https://arxiv.org/abs/2402.10811 | quelle part de la variance des reponses humaines les variables de persona peuvent-elles expliquer, et combien le modele en recupere-t-il ? | sept jeux a annotations desagregees : Kumar et al. 2021 toxicite, Diaz et al. 2018 sentiment, Social-Chem-101, NLPositionality (deux taches), SBIC, EPIC ironie, **plus l'ANES 2012, 2 728 repondants** | Tulu-2 7b, 13b, 70b, plus GPT | **plafond de variance explicable par le groupe, par regression mixte, puis part recuperee par le modele.** R carre marginal des variables de persona en effets fixes, R carre conditionnel avec un effet aleatoire par texte. Puis R carre d'une regression a effets fixes predisant l'annotation humaine par la prediction du modele | **R carre marginal, c'est a dire la part de variance que l'etiquette peut expliquer : 0,036 sentiment ; 0,097 acceptabilite sociale Social-Chem ; 0,005 et 0,017 sur les deux taches NLPositionality ; 0,031 biais social SBIC ; 0,091 ironie EPIC ; 0,719 vote presidentiel ANES 2012.** Le texte lui meme, en effet aleatoire, explique jusqu'a 70 pour cent. Il reste 25 a 70 pour cent de variance non expliquee ni par le texte ni par la persona. **Un modele de 70 milliards avec persona capte 81 pour cent du R carre cible.** Quand le R carre cible est inferieur a 0,1, le R carre predit s'effondre souvent a zero | la regression est lineaire et sans interaction entre variables de persona, donc c'est une borne basse, les auteurs le disent. Annotations, pas items d'enquete a modalites, sauf pour l'ANES | **c'est le plafond que le dossier n'a pas.** Il dit combien de variance individuelle une etiquette peut au mieux porter, et la reponse est : moins de 10 pour cent sur les jugements subjectifs, plus de 70 pour cent sur un vote presidentiel polarise. **Le rapport inter sur intra d'une population n'est donc pas une constante du domaine, c'est une propriete de l'item.** Toute affirmation popsim sur le gonflement de l'inter doit etre indexee sur ce plafond, item par item. La formule "the more persona variables are correlated with the outcome variable, the better LLM predictions are using persona prompting" est le resultat le plus reutilisable de la passe | citation aval d'Orlikowski et al., Semantic Scholar | [CONFIRME], PDF v2 relu par `pdftotext -layout` |
| L02-05 | Mahammed Kamruzzaman, Shrabon Kumar Das, Gene Louis Kim (University of South Florida), *Demographic Prompting at Scale: When More Attributes Hurt LLM-Human Agreement*, arXiv 2607.10590 v1 du 12 juillet 2026. https://arxiv.org/abs/2607.10590 | ajouter des attributs demographiques a l'invite ameliore-t-il l'accord avec les humains, et pourquoi ? | cinq taches subjectives a annotations desagregees : toxicite, sentiment, politesse, offensivite, attribution d'emotion (ISEAR) ; **toutes les combinaisons d'attributs, du simple au complet** | Gemma, Llama-3.2, Qwen, DeepSeek, Mistral, cinq modeles ouverts | **accord individuel par attribut et par combinaison, plus trois diagnostics de l'attribut.** Kappa de Cohen a ponderation quadratique, ou exactitude pour l'emotion. Diagnostics : importance SHAP de l'attribut sur l'annotation humaine, apprenabilite du signal par LSVC, et **coherence directionnelle**, correlation de Fisher moyennee entre les vecteurs de reponse des categories d'un meme attribut. Plus un sondage de neurones specialises | **l'ensemble complet d'attributs n'est jamais le meilleur, sur aucune tache et aucun modele.** L'accord culmine a un a trois attributs a fort signal. Degradations chiffrees, politesse : ajouter la race fait passer Llama de kappa 0,349 a 0,252, DeepSeek de 0,244 a 0,101. **L'importance SHAP de l'attribut chez les humains ne predit pas le gain du modele** : les 25 correlations de Spearman vont de -0,595 a +0,571, aucune significative. **L'apprenabilite predit le gain a l'envers** : quatre modeles sur cinq donnent rho inferieur ou egal a -0,700, l'age etant l'attribut le plus apprenable, 0,316, et celui qui degrade le plus. Neurones : correlations negatives fortes sur le sentiment (Gemma -0,888) et l'emotion (Gemma -0,983, Llama -0,772) | pas de referent de variance, pas de population simulee : c'est de l'annotation. Cinq modeles ouverts, tous petits ou moyens. Le sondage de neurones est correlatif, sans intervention | **c'est le meilleur travail du corpus sur le mecanisme de l'etiquette, et il ferme une porte.** Il dit que la quantite d'information demographique n'est pas ce qui compte, que le volume de neurones actives non plus (le "high-volume paradox"), et que le facteur decisif est la **coherence directionnelle** du signal du groupe : un attribut dont les sous groupes se contredisent ne peut etre porte par aucune persona unique. C'est une explication precise de pourquoi l'etiquette gonfle l'inter au lieu de le calibrer | citation aval d'Orlikowski et al., Semantic Scholar | [CONFIRME], PDF relu par `pdftotext -layout` |
| L02-06 | Pia Sommerauer (VU Amsterdam), Giulia Rambelli (Bologne), Tommaso Caselli (Groningue), *Simulating Identity, Propagating Bias: Abstraction and Stereotypes in LLM-Generated Text*, EMNLP 2025, arXiv 2509.08484 v1 du 10 septembre 2025. https://arxiv.org/abs/2509.08484 | l'invite de persona modifie-t-elle le niveau d'abstraction linguistique, marqueur etabli du stereotype ? | **Self-Stereo**, jeu de stereotypes auto declares recueillis sur Reddit, introduit par les auteurs ; couples categorie socio demographique et attribut, stereotypique, non stereotypique, ou aleatoire ; 11 personas contre un assistant generique | six modeles a poids ouverts, familles LLaMa3 et Qwen2.5 | **abstraction, au sens du Linguistic Category Model et du Linguistic Expectancy Bias, en trois metriques.** Concretude (moyenne des scores de concretude des mots), specificite, et negation. Referent : le meme modele en assistant generique, plus les textes humains de Self-Stereo | **les textes generes sont "always mildly concrete, very generic, and with almost no negations", quelle que soit la persona.** La specificite est remarquablement stable, valeurs groupees entre 2,10 et 2,14 selon les conditions. Les modeles Qwen2.5 varient de moins de 0,05 sur la concretude entre conditions. **L'appartenance au groupe ne change rien** : les modeles a persona Millennial ne different pas des autres personas d'age quand ils decrivent des Millennials, alors que la psychologie sociale predit une abstraction plus basse en intra groupe (Maass et al. 1989). Les differences de surface existent pourtant, mesurees par BLEU et ROUGE-L | pas de population simulee, pas d'items d'enquete, pas de variance de reponse. Texte court genere, anglais | **c'est le mecanisme psycholinguistique de la substitution, et il est nomme.** "Even when they describe a social category by taking a specific person (e.g. Let's meet Alex...), the overall degree of abstraction still leads to generalizations towards the entire category." Autrement dit le modele parle **de la categorie meme quand on lui donne un individu**. C'est la version textuelle exacte de ce que a31 mesure sur les raretes de segment. Le Linguistic Category Model donne un cadre theorique en psychologie sociale, exterieur a l'informatique, que le dossier n'a pas | citation aval d'Orlikowski et al., Semantic Scholar | [CONFIRME], PDF relu par `pdftotext -layout` |
| L02-07 | Sola Kim, Jieshu Wang, Marco A. Janssen, John M. Anderies (Arizona State, Stony Brook), *How Large Language Models Misrepresent American Climate Opinions*, arXiv 2512.23889 v2 du 18 avril 2026. https://arxiv.org/abs/2512.23889 | les modeles reproduisent-ils les motifs demographiques et intersectionnels de l'opinion climatique americaine ? | enquete nationale representative d'opinion climatique, **978 repondants reels, 20 questions**, profils passes en invite, reponses IA comparees aux reponses reelles des memes personnes | six modeles | **deux termes, tous deux avec referent humain apparie.** (a) Terme inter : regression de l'ecart modele moins humain sur les caracteristiques demographiques, avec effets fixes de question et de modele, plus des modeles d'interaction pour l'intersectionnalite. (b) Terme de dispersion : **ratio de variance modele sur humain, par question** | **ratio de variance moyen 0,72 sur les 20 questions, soit 27,9 pour cent de variance en moins.** Terme inter, coefficients de l'ecart : Noirs +0,030, revenu eleve +0,015, femmes -0,021, liberaux -0,029, **tres conservateurs -0,077**, tous a p < 0,05. Le nuage des moyennes de groupe est **comprime vers la moyenne de population** : "Groups with lower actual climate concern were overestimated (points above the diagonal), while groups with higher actual concern were underestimated (points below the diagonal)". Interaction : les modeles appliquent un motif de genre uniforme qui colle pour les Blancs et les Hispaniques et se trompe pour les Noirs | un seul domaine, 20 questions, six modeles. Le ratio de variance est global par question, pas intra segment. Pas de plancher de reinterrogation. Les auteurs emploient un vocabulaire prudent, "appear to" | **contredit la version simple de la these sur le signe de l'inter, et donne la variable qui explique le signe.** Ici l'inter est **comprime**, pas gonfle, exactement comme chez Qin, Li et Cheng et chez Keough. Mais la compression suit les lignes ideologiques, avec le plus grand ecart chez les tres conservateurs, ce qui est la meme asymetrie que a30 trouve sur le GSS, dans l'autre sens. **La quantite mesuree n'est pas la meme : ici c'est l'ecart de la moyenne de groupe a la verite, pas l'amplitude des ecarts entre groupes.** Un modele peut simultanement tirer chaque groupe vers le centre et exagerer l'ecart entre deux groupes donnes | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [CONFIRME], PDF v2 relu par `pdftotext -layout`, sections 3 et 4 |
| L02-08 | Steven Wang, Kyle Hunt, Shaojie Tang (Buffalo), Kenneth Joseph, *Can Finetuning LLMs on Small Human Samples Increase Heterogeneity, Alignment, and Belief-Action Coherence?*, arXiv 2511.21218 v1 du 26 novembre 2025. https://arxiv.org/abs/2511.21218 | un ajustement fin sur un echantillon pilote repare-t-il l'homogeneite, le desalignement et l'incoherence croyance action ? | experience comportementale de divulgation d'information de Hunt et al. 2025, huit groupes de traitement, **929 simulations**, ethnies au sens des categories Prolific | modeles ouverts ajustes sur des fractions de l'echantillon humain, jusqu'a **25 pour cent d'un seul groupe de traitement, environ 30 observations** | **quatre grandeurs, dont une mesure directe de degenerescence.** Nombre de structures de croyance uniques ; distance de Jensen-Shannon par sous groupe ethnique ; ecart croyance action ; **recuperation des coefficients de regression de l'etude d'origine, notee en F1 sur le signe** | **le modele non ajuste produit 19 structures de croyance uniques sur 929 simulations, contre 340 chez les humains.** Tous les modeles ajustes en produisent au moins 200, de 244 a 374. La distance JS est **au moins divisee par deux** chez toutes les variantes. Ecart croyance action : proche de 100 pour cent sans ajustement, **23,8 et 24,4 pour cent apres ajustement sur les huit groupes, contre 24,7 pour cent chez les humains**. Mais recuperation des coefficients : le meilleur modele atteint **F1 de signe d'environ 0,769 avec un taux de faux positifs d'environ 0,333**. Deux resultats negatifs : echantillonner a parts egales entre ethnies **n'ameliore pas** l'alignement des minorites, et la distance JS reste toujours la plus basse pour les participants blancs ; retirer les informations demographiques de l'invite ne degrade **pas** l'alignement par sous groupe | un seul domaine, un seul jeu, effectifs modestes, comparaisons surtout visuelles pour la dispersion, pas de decomposition inter et intra | **c'est le correctif le mieux documente du corpus sur la dissociation dispersion contre structure.** Trente observations suffisent a restaurer la dispersion et la coherence, et ne suffisent pas a restaurer l'inference. [DEDUCTION] l'ajustement fin est un dilatateur qui recalibre aussi la marge, pas un transporteur ; il ne touche pas au terme inter, puisque l'ajout d'information demographique n'a aucun effet mesure sur l'alignement par sous groupe | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [CONFIRME], PDF lu integralement, extraction en ordre de lecture |
| L02-09 | *Two-Faced Social Agents: Context Collapse in Role-Conditioned Large Language Models*, arXiv 2511.15573 v1 du 19 novembre 2025. https://arxiv.org/abs/2511.15573 | des agents a persona socio economique gardent-ils leur role quand la tache impose une bonne reponse ? | **15 conditions de role**, trois scenarios, 28 items de mathematiques du SAT et 16 questions de preference affective, plus une replication etendue | GPT-5, Claude Sonnet 4.5, Gemini 2.5 Flash | **part de variance imputable au role, par PERMANOVA sur les reponses, plus silhouette.** Plus tailles d'effet d de Cohen entre roles sur les preferences | **SAT : GPT-5, PERMANOVA p = 1,000, R carre = 0,0004, silhouette -0,0034 ; Gemini 2.5 Flash p = 0,120, R carre = 0,0020, silhouette -0,0038 ; Claude Sonnet 4.5 p < 0,001, R carre = 0,0043, silhouette 0,014.** Preferences affectives, memes modeles, memes roles : **d moyen de 0,52 a 0,58**. Claude presente en outre un gradient socio economique **inverse**, les personas a bas statut surpassant celles a haut statut, eta carre de 0,15 a 0,19 en replication etendue | pas de referent humain : le R carre PERMANOVA est une part de variance inter groupes sans point de comparaison humain. Trois modeles, un seul instrument cognitif | **le terme inter n'est pas une propriete du modele, c'est une propriete du couple modele et tache.** Le meme modele passe de R carre 0,0004 a d = 0,55 selon que la question a une bonne reponse ou non. C'est la variable qui explique une partie des contradictions du champ, et elle n'est dans aucune ligne de la table de depart. Les auteurs nomment trois mecanismes : pression d'optimisation, compression distributionnelle, et **"contextual essentialism"** ou la persona reste une invite statique jamais internalisee | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [CONFIRME], PDF relu par `pdftotext -layout`, sections 2 a 3 |
| L02-10 | *When Persona Attributes Improve Population Alignment in Large Language Models*, arXiv 2609.02526 v1 du 2 septembre 2026. https://arxiv.org/abs/2609.02526 | quand l'invite de persona aide-t-elle, et quelle methode de selection des attributs employer ? | **quatre enquetes sociales generales, deux pays**, 20 questions cibles par enquete, choisies aux deux extremes de la dispersion | six modeles, familles Llama et Qwen, de 3 a 70 milliards | **la dispersion des reponses humaines comme variable explicative.** "Human response variation" mesuree par entropie de Shannon normalisee pour les variables nominales et par le **dissention** pour les ordinales, les deux normalisees entre 0 et 1. Performance : distance de Jensen-Shannon entre distribution predite et distribution reelle sur l'ensemble des participants. Quatre methodes de selection d'attributs : correlation, importance de variable, selection d'ensemble par le modele, notation par le modele | **l'invite de persona fait mieux sur les questions a forte dispersion humaine et moins bien sur celles a faible dispersion, pour les quatre methodes de selection ; et l'effet s'inverse pour la condition sans persona.** Les baselines statistiques calculees sur les donnees d'enquete battent les selections faites par le modele lui meme, sur les quatre enquetes et les deux familles. Stabilite de la selection croissante avec la taille : le grand Llama choisit le meme attribut le plus important dans pres de 60 pour cent des tirages | la mesure de performance est une distance entre distributions de population, jamais separee en inter et intra. Pas de plancher humain. Les questions cibles sont choisies aux extremes, ce qui exagere le contraste | **soutient et precise L02-04 sur une autre unite d'observation.** L'etiquette n'aide que la ou les gens sont partages. La ou ils convergent, elle nuit. C'est la meme loi que la RMSE contre variance de Shi et Haupt, r = 0,75, obtenue par un chemin independant. C'est aussi un argument direct pour la these : la simulation efface la ou il y a le plus a effacer | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [CONFIRME], PDF relu, resume et sections 5.1 a 5.3 |
| L02-11 | David A. Freedman (Berkeley), *Ecological Inference and the Ecological Fallacy*, International Encyclopedia of the Social and Behavioral Sciences 6, pages 4027 a 4030, Technical Report 549, 30 octobre 1999. https://www.stat.berkeley.edu/~census/549.pdf | peut-on inferer le comportement individuel a partir de donnees agregees par groupe ? | Robinson 1950 sur les 48 Etats de 1930 ; replication sur la **Current Population Survey de mars 1995**, 50 Etats, personnes de 25 ans et plus | aucun modele de langage : regression ecologique de Goodman, methode des bornes de Duncan et Davis, modele a coefficients aleatoires de King 1997, modele de voisinage | **correlation ecologique contre correlation individuelle, et estimation par groupe contre verite connue.** Le referent est la verite individuelle, disponible dans les microdonnees | **Robinson 1930, nativite et alphabetisation : correlation ecologique 0,53, correlation individuelle -0,11.** Replication CPS 1995, nativite et revenu eleve : **correlation ecologique 0,52, correlation individuelle -0,05**. Estimation de la part a haut revenu, **verite 35 pour cent chez les natifs et 28 pour cent chez les nes a l'etranger** ; regression ecologique 29 et **85** ; modele a coefficients aleatoires de King 30 et **72** ; **modele de voisinage 34 et 36**. "The track record in the tests tends to favor the neighborhood model" | texte de 1999, sept pages, pas de modele de langage, pas de simulation. Les exemples portent sur des unites geographiques et non sur des cellules demographiques | **c'est la matrice theorique de la these, et elle a soixante quinze ans.** Trois transferts directs. (a) La "constancy assumption", "the statistical behavior of a demographic group is not allowed to depend on area of residence", est litteralement l'hypothese que fait un agent a etiquette. (b) L'inversion de signe entre niveau de groupe et niveau individuel est le cas extreme de ce que a31 mesure. (c) **Le modele de voisinage, ou le contexte remplace la demographie, bat les deux modeles demographiques.** C'est le pendant statistique exact du resultat de a31 : appariement 0,41 sans etiquette contre 0,19 avec etiquette | remontee de citations depuis Orlikowski et al., qui cite Robinson 1950 et Freedman 2015 | [CONFIRME], PDF de sept pages lu integralement |
| L02-12 | Stef van Buuren, *Flexible Imputation of Missing Data*, deuxieme edition, CRC Press, version en ligne libre, sections 1.3.3 a 1.3.5 et 2.6. https://stefvanbuuren.name/fimd/ | que fait a une distribution le fait de remplacer une valeur manquante par sa valeur predite ? | jeu `airquality` de R, ozone et rayonnement solaire, 24 pour cent de manquants ; plus une simulation de comparaison de methodes | aucun modele de langage : imputation par la moyenne, imputation par regression, imputation par regression stochastique | **effet de la methode d'imputation sur l'ecart type, sur la correlation, et sur la validite de l'inference.** Plus, en section 2.6, la RMSE entre valeur vraie et valeur imputee comme critere de selection de methode | **imputation par la moyenne : "The standard deviation in the imputed data is equal to 28.7, much smaller than from the observed data alone, which is 33" ; "The correlation drops from 0.35 in the blue points to 0.3 in the combined data".** Imputation par la valeur predite : les points imputes ont une correlation de 1 par construction, **"If the red and blue dots are combined, then the correlation increases from 0.35 to 0.39"**, et "correlations are biased upwards, and the variability of the imputed data is systematically underestimated. The degree of underestimation depends on the explained variance and on the proportion of missing cases (Little and Rubin 2002, 64)". Section 2.6 : **"the method yielding the lowest RMSE is bad for imputation"**, la regression atteint une RMSE de 0,725 contre 1,025 pour l'imputation multiple correcte, et c'est la premiere qui est invalide | manuel, pas article de recherche ; l'exemple est bivarie et continu, pas ordinal a modalites ni segmente par groupe. Le probleme est celui des donnees manquantes, pas celui de la simulation de population | **la double distorsion de popsim est un theoreme d'imputation.** Remplacer une personne par la valeur predite depuis son groupe **ecrase la variance residuelle et gonfle les relations que porte le modele**, les deux a la fois, par construction. Deux consequences pour le dossier. (1) L'imputation de la these ne peut plus etre "les modeles de langage font ceci" : c'est ce que fait tout predicteur de moyenne conditionnelle, ce qui rejoint Ku et al. mot pour mot. (2) La section 2.6 publie la dissociation exactitude contre structure sous sa forme la plus dure : le critere qui minimise l'erreur individuelle **selectionne la mauvaise methode**. La phrase de van Buuren, "regression imputation, as well as its modern incarnations in machine learning is probably the most dangerous of all methods described here", est la citation d'ouverture que le papier popsim n'a pas | remontee depuis L02-03 vers la statistique d'enquete | [CONFIRME], pages `sec-simplesolutions.html` et `sec-true.html` lues |
| L02-13 | Simone Zhang (NYU), Janet Xu (Stanford GSB), AJ Alvero (Florida), *Generative AI Meets Open-Ended Survey Responses: Research Participant Use of AI and Homogenization*, Sociological Methods and Research 2025, doi 10.1177/00491241251327130, preprint SocArXiv 10.31235/osf.io/4esdp v3 | les reponses libres generees par modele different-elles de celles des humains, et ou ? | enquete originale sur Prolific pour l'usage declare ; **trois etudes TESS anterieures a ChatGPT**, questions ouvertes sur les perceptions de groupe et l'interet pour la politique, **462, 1 146 et 915 reponses humaines** appariees | GPT-4o mini, Gemini 1.5, Claude 3.5 Sonnet, avec les strategies d'invite reellement rapportees par les participants | **homogeneite lexicale et semantique contre referent humain, plus une mesure orientee sur le contenu socialement couteux.** Nombre de mots, vocabulaire total, et **similarite cosinus des plongements GloVe de chaque reponse a des vecteurs de concepts, "vermin" et "moral disgust"** | 34 pour cent des participants declarent utiliser un modele pour repondre aux questions ouvertes. Longueur : humains 9,7, 31,7 et 16,1 mots en moyenne selon la question, contre 123,5 a 215,8 pour les modeles, avec un vocabulaire plus large mais **une homogeneite plus forte entre reponses**. Et le point decisif : **"In sensitive questions about group perceptions and stereotypes, human-written responses are more likely to feature dehumanizing language than LLM-simulated responses"**, les reponses des trois modeles se groupant plus etroitement et **plus bas** sur les deux vecteurs de concept que les reponses humaines | texte libre, pas d'items a modalites, donc pas de ratio de variance ni de decomposition inter et intra. Trois questions seulement. La mesure de deshumanisation est une similarite a deux vecteurs de mots, pas une annotation | **c'est le precedent le plus proche de la these de popsim publie a ce jour, et il faut le citer.** Il etablit, avec un referent humain et sur les memes questions, que **la part effacee est la part socialement couteuse**. Ce qui reste a popsim apres lui : la mesure sur des items fermes, la decomposition inter et intra, le contraste chiffre entre items sensibles et items temoins apparies, et le plancher de reinterrogation. La revendication "personne n'a formule que la part effacee est celle que les gens ne disent pas ouvertement" **doit etre retiree** et remplacee par une revendication de mesure | citation aval de Bisbee et al. 2024, OpenAlex | [CONFIRME], preprint SocArXiv v3 relu par `pdftotext -layout` |
| L02-14 | *Beyond Averages: Evaluating LLMs on Human Survey Replication at the Distributional Level*, arXiv 2606.09013 v1 du 10 juin 2026. https://arxiv.org/abs/2606.09013 | les modeles reproduisent-ils la forme de la distribution, ou seulement la moyenne ? | **experience de choix de consommation non publique**, nouilles instantanees, Coree, 2010, choisie parce qu'elle a peu de chances d'etre dans les corpus d'entrainement ; trois types de variable, binaire, categorielle, comptage | Gemini-2.5-Pro, GPT-5.2, GPT-4.1-nano, Qwen2.5-VL 7B et 72B, Qwen3-VL 8B et 30B, Llama-3.2-11B-Vision | **trois niveaux compares a trois baselines humaines.** Niveau moyen par erreur absolue moyenne ; motif par correlation de Pearson entre conditions ; **distributionnel par distance de Wasserstein**. Baseline decisive : **une marginale insensible aux conditions, tiree de la distribution humaine groupee** | sur la quantite achetee, **aucun modele ne bat la baseline insensible aux conditions**. Sur l'incidence d'achat, plusieurs modeles produisent des correlations inversees (Qwen2.5-VL-72B -0,291, Qwen3-VL-30B -0,274, GPT-5.2 -0,197) et **quatre modeles predisent l'achat dans toutes les conditions, donc une variance nulle et une correlation indefinie**. Sur le choix de marque en revanche, les meilleurs modeles battent les trois baselines, Qwen2.5-VL-72B a une MAE de 0,055, plus de trois fois inferieure a la marginale. **L'invite de raisonnement explicite degrade l'alignement de facon monotone** | un seul jeu, un seul pays, une seule annee, pas de segmentation demographique, donc aucun terme inter | **soutient la menace de baseline et ajoute une cause.** La phrase "models that match human means well can still produce distributions further from humans than this baseline, mean-based evaluation alone can be actively misleading" est la formulation la plus directe de l'aveuglement de la moyenne, sur un jeu non contamine. Et la degradation monotone par le raisonnement explicite converge avec L02-09 : plus le modele optimise, moins il tient son role | citation aval de Qin, Li et Cheng, Semantic Scholar | [CONFIRME], PDF relu, sections de resultats |
| L02-15 | Nikita Soni, Dhruv Vijay Kunjadiya, Pratham Piyush Shah, Dikshya Mohanty, H. Andrew Schwartz, Niranjan Balasubramanian (Stony Brook), *Addressing the Ecological Fallacy in Larger LMs with Human Context*, arXiv 2603.05928 v1 du 6 mars 2026 | traiter les textes d'un meme auteur comme dependants ameliore-t-il un modele de 8 milliards ? | corpus multi documents ordonnes temporellement par auteur, huit taches en aval | Llama 8B, HuLM en pre entrainement continu par QLoRA, HuFT en ajustement | perplexite et performance en aval, aucun referent de variance de population | l'ajustement en contexte d'auteur ameliore le modele de 8 milliards ; le pre entrainement continu HuLM donne un modele generalisable sur huit taches avec un simple classifieur lineaire | ce n'est pas une simulation de population et il n'y a pas d'items d'enquete. Le "ecological fallacy" y designe l'independance supposee des textes d'un meme auteur, pas l'inference du groupe vers l'individu | **meme mot, autre chose, et il faut le savoir avant de citer.** Utile sur un point : les auteurs justifient leur travail en ecrivant que le langage detache de son auteur "lack the richness and variance that natural human contexts bring (e.g. generated language lacks variance in expressed psychological traits)". C'est une troisieme famille de causes, l'objectif de pre entrainement lui meme | recherche arXiv sur "ecological fallacy language model" | [CONFIRME] pour le resume, l'introduction et le cadre ; [PROBABLE] pour les tableaux de resultats |

### Lignes lues au resume seulement

| id | reference | apport | rapport a la these | trouve par | certitude |
|---|---|---|---|---|---|
| L02-16 | Yuan Gao, Dokyun Lee, Gordon Burtch, Sina Fazelpour, *Take caution in using LLMs as human surrogates*, PNAS 122, 2025, doi 10.1073/pnas.2501660122 | jeu de la demande d'argent 11-20 : presque toutes les approches avancees echouent a reproduire la distribution du comportement humain, et les causes d'echec sont "diverse and unpredictable, relating to input language, roles, safeguarding" | la profondeur de raisonnement est un axe d'echec distinct de la variance ; utile pour dire que l'echec n'a pas une cause unique | citation aval de Bisbee, OpenAlex | [PROBABLE] |
| L02-17 | Yueqi Xie, Shuzhen Li, Yifu Lu, Zhiwen Xiao et al., *Evaluating the statistical realism of LLM-generated social science data*, PNAS 2026, doi 10.1073/pnas.2538145123 | **SSDataBench**, cinq familles de motifs statistiques (distributions univariees, associations bivariees, predictions multivariees, distributions de sequences d'evenements de vie, associations entre sequences et covariables) sur quatre panels longitudinaux et trois enquetes transversales | c'est le benchmark de "realisme statistique" que le champ n'avait pas, et il porte sur la population, pas sur l'individu. A lire avant toute proposition de metrique standard | citation aval de Bisbee, OpenAlex | [PROBABLE] |
| L02-18 | *Statistical realism is not evidence that LLMs can estimate treatment effects in social science experiments*, arXiv 2604.02458 | experience transnationale, **59 508 participants, 62 pays**, trois modeles, plus deux replications sur 12 et 27 pays et 20 785 participants : la correlation entre realisme statistique et exactitude de l'effet de traitement est faible, et optimiser le premier peut degrader le second | c'est la dissociation exactitude contre structure portee sur un troisieme couple de grandeurs, avec les plus grands effectifs du corpus. A citer contre toute metrique unique | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [PROBABLE] |
| L02-19 | Yutong Xie, Ruoyi Gao, Qiaozhu Mei, *Distributional Alignment for Social Simulation with LLMs: A Mixture Modeling Approach*, doi 10.1145/3770855.3818919 | l'heterogeneite humaine est modelisee comme un **melange d'invites systeme**, dont les poids sont estimes par esperance maximisation et par renforcement de gradient ; evalue sur la personnalite, les comportements economiques et les valeurs ideologiques | famille du melange de personas, cousine de Mixture-of-Personas. [DEDUCTION] un melange dont les poids sont ajustes sur une distribution cible dilate la dispersion totale et n'impose rien au partage inter et intra | citation aval de Bisbee, OpenAlex | [PROBABLE] |
| L02-20 | *Adaptive Querying with AI Persona Priors*, arXiv 2605.00696 | modele a variable latente ou l'etat d'un utilisateur est son appartenance a un **dictionnaire fini de personas**, chacune fournissant une distribution de reponses produite par le modele ; mise a jour bayesienne en forme close ; teste sur WorldValuesBench | **c'est la formulation hierarchique explicite** : le modele fournit la loi a priori de groupe, les reponses observees de la personne fournissent la vraisemblance. C'est la structure exacte du retrecissement vers la moyenne de groupe, ecrite pour la premiere fois dans ce champ | citation aval de Peng et al., Semantic Scholar | [PROBABLE] |
| L02-21 | *Distribution Shift Alignment Helps LLMs Simulate Survey Response Distributions*, arXiv 2510.21977 | ajustement en deux etapes qui aligne les distributions **et les deplacements de distribution entre contextes** plutot que d'ajuster la distribution d'entrainement ; sur cinq jeux d'enquete publics, reduit de 53,48 a 69,12 pour cent la quantite de donnees reelles necessaire | famille de la calibration de distribution. Apprendre le **deplacement** entre groupes plutot que le niveau est, formellement, apprendre le terme inter. C'est le seul travail qui cible cette quantite directement | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [PROBABLE] |
| L02-22 | *The Prompt Makes the Person(a): A Systematic Evaluation of Sociodemographic Persona Prompting*, arXiv 2507.16076 | cinq modeles ouverts, **15 groupes intersectionnels**, taches ouvertes et fermees : le format d'adoption du role et la strategie d'amorcage demographique changent le resultat ; **le format entretien et l'amorcage par prenom reduisent le stereotype** ; OLMo-2-7B fait mieux que Llama-3.3-70B | famille de l'invite. Converge avec Wang, Morgenstern et Dickerson, chez qui les noms codes identitairement rapprochent des representations intra groupe sans les atteindre | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [PROBABLE] |
| L02-23 | *Improving the Distributional Alignment of LLMs using Supervision*, arXiv 2507.00439 | une supervision simple ameliore plus regulierement l'alignement des distributions avec des groupes de population, sur trois jeux, sante publique, opinion publique, valeurs et croyances ; l'alignement est aussi rapporte **groupe par groupe** | famille de la calibration au niveau du groupe, avec la meme reserve : agit sur l'inter, ne dit rien de l'intra | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [PROBABLE] |
| L02-24 | *Human diversity fuels collective creativity that large language models cannot simulate or sustain*, arXiv 2607.26899 | experience preenregistree de metaphores creatives avec des scripteurs anglophones natifs et non natifs ; puis simulation du **vivier entier** par des personas construites sur les vrais profils, trois familles de modeles, invite en langue native, temperatures elevees : **"Every simulated pool fell below every human pool, and pushing models further induced diversity only through degenerate text"** | preuve d'intra sans decomposition, mais avec la comparaison la plus severe possible, vivier contre vivier. La mention "degenerate text" est la meilleure formulation publiee de la limite de la famille des dilatateurs | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [PROBABLE] |
| L02-25 | *Modeling the Structure of Human Behavior with AI Prompt Vectors*, arXiv 2608.18265 | **119 147 decisions, 78 657 sujets, plus de 35 pays, 10 roles de jeux economiques classiques** : le comportement humain est approche en donnant au modele un vecteur de type, et **trois dimensions suffisent**, aversion au risque, sophistication strategique, confiance ; les types requis pour ajuster les individus se groupent en **moins d'une douzaine de groupes**, et predisent sur des jeux non vus | **c'est le contre argument le plus fort a la these**, et il faut y repondre. Si le comportement humain est reellement de faible dimension et se ramene a une douzaine de types, alors remplacer une personne par son type n'est pas un appauvrissement, c'est une compression fidele. La reponse a preparer : leurs types sont des **types comportementaux estimes par ajustement**, pas des **etiquettes demographiques donnees a l'avance**, et c'est precisement la difference que L02-04 chiffre | citation aval de Peng et al., Semantic Scholar | [PROBABLE] |
| L02-26 | *On Epistemic Diversity in Large Language Models*, arXiv 2609.04835 | formalise la diversite epistemique comme l'etendue des reponses, explications et voies de raisonnement valides exposees a l'utilisateur ; constate que les modeles de pointe "collapse large valid answer spaces onto small canonical subsets" | cadre conceptuel, aucune mesure de variance de population. Utile pour la phrase d'introduction, comme T02-22 | citation aval de Wang, Morgenstern et Dickerson, Semantic Scholar | [PROBABLE] |
| L02-27 | Megan A. Brown, Shubham Atreja, Libby Hemphill, Patrick Y. Wu, *The Context Dependency of Demographic Bias in LLM Annotation*, FAccT 2026, doi 10.1145/3805689.3812212 | le biais demographique de l'annotation par modele depend du contexte | a lire avant toute generalisation d'un resultat d'un jeu a l'autre ; convergent avec L02-05 et L02-09 | citation aval de Bisbee, OpenAlex | [NON LU], titre et notice seulement |

---

## B. Comment ca fonctionne

### B.1 Le mecanisme central n'est pas propre aux modeles de langage

La lecture la plus utile de cette passe est celle qui vient du dehors du champ. Quand on remplace la
reponse d'une personne par la valeur predite depuis les variables qu'on connait d'elle, deux choses
se produisent simultanement et par construction : la dispersion residuelle disparait, et les
relations que porte le modele de prediction sont renforcees. Van Buuren le chiffre sur un exemple
bivarie a 24 pour cent de manquants : l'imputation par la moyenne fait tomber l'ecart type de 33 a
28,7 et la correlation de 0,35 a 0,30 ; l'imputation par la valeur predite fait **monter** la
correlation de 0,35 a 0,39, parce que les points imputes sont exactement sur la droite et ont donc
une correlation de 1 entre eux (L02-12, [CONFIRME]). C'est, terme pour terme, la double distorsion
que popsim mesure : intra ecrase, inter gonfle. La formule generale est deja dans la table de depart
sous la plume de Ku et al., "predicting individual survey responses from limited context inherently
biases toward population means, rather than solely an LLM artifact" (T02-42, [CONFIRME]), et les
auteurs le prouvent en montrant qu'une foret aleatoire supervisee, sans alignement, s'ecrase autant,
ratio de variance 0,72 contre 0,67 a 0,85 pour les modeles de langage. Peng et al. arrivent au meme
mot sans citer la statistique : les reponses des jumeaux sont "overly shrunk towards a base model"
(L02-01, [CONFIRME]).

La consequence pour la redaction est nette et elle coute peu : **la these ne peut pas etre "les
modeles de langage ecrasent la variance"**, parce que c'est un theoreme de prediction. Elle doit
etre une these sur ce que l'etiquette fait de plus qu'un predicteur optimal, et sur **quelle** part
est effacee.

### B.2 L'etiquette n'est pas une information, c'est une ancre

Trois travaux independants, sur trois objets differents, disent la meme chose. Chez Hu et Collier,
les variables de persona expliquent moins de 10 pour cent de la variance des annotations sur six
jeux subjectifs, R carre marginal de 0,005 a 0,097, et plus de 70 pour cent sur le vote presidentiel
de l'ANES 2012, R carre marginal 0,719 (L02-04, [CONFIRME]). Il y a donc un plafond de ce que
l'etiquette peut legitimement porter, et il varie d'un facteur cent selon l'item. Chez Orlikowski et
al., mettre explicitement le groupe dans l'architecture n'apporte rien : sur 5 002 annotateurs, le
modele a couches socio demographiques ne bat ni la reference sans groupe ni le temoin a **groupes
tires au hasard**, et pour la plupart des groupes c'est le temoin randomise qui a la meilleure
moyenne (L02-03, [CONFIRME]). Chez Peng et al., l'exactitude d'un jumeau nourri de plus de cinq
cents reponses reelles de la personne, 0,748, n'est pas significativement meilleure que celle d'un
agent construit sur quatorze variables demographiques, 0,746, p = 0,37 (L02-01, [CONFIRME]).

Ces trois faits ne disent pas que l'etiquette est neutre. Ils disent qu'elle deplace la reponse sans
l'informer. Kamruzzaman et al. le montrent au niveau de l'attribut : l'importance de l'attribut chez
les humains, mesuree par SHAP, **ne predit pas** le gain du modele, aucune des 25 correlations n'est
significative ; et l'apprenabilite du signal predit le gain **a l'envers**, rho inferieur ou egal a
-0,700 sur quatre modeles sur cinq, l'age etant a la fois l'attribut le plus apprenable et celui qui
degrade le plus (L02-05, [CONFIRME]). Leur explication est la coherence directionnelle : un attribut
dont les sous groupes portent des signaux opposes ne peut etre represente par une persona unique,
donc le modele choisit une direction et l'applique a tout le groupe. C'est le mecanisme du
gonflement de l'inter, decrit sans le nommer.

Shi et Haupt fournissent la preuve la plus visuelle du meme mecanisme, sur des groupes qui ne sont
pas demographiques. Sur les 277 philosophes, les modeles fabriquent des associations specialite vers
position qui n'existent pas : 11,4 points de pourcentage non significatifs chez les humains
deviennent environ 43 points chez quatre modeles sur sept, et 1,9 point non significatif devient
68,9 points chez sept modeles sur sept. Et le mecanisme est en partie lexical : "the surface-level
lexical overlap between biology and biological may explain this spurious prediction, a pattern
consistent across architectures" (L02-02, [CONFIRME]). L'etiquette agit comme un mot dont le modele
cherche l'echo dans les options de reponse.

### B.3 Ce que le modele produit quand on lui donne un individu, c'est une description de categorie

Sommerauer, Rambelli et Caselli mesurent l'abstraction linguistique, marqueur etabli du stereotype
dans le Linguistic Category Model, sur des textes generes par six modeles sous onze personas. Les
resultats sont plats : la specificite reste entre 2,10 et 2,14 quelle que soit la condition, la
concretude bouge de moins de 0,05 chez Qwen2.5, et l'appartenance de la persona au groupe decrit ne
change rien, alors que la psychologie sociale predit une abstraction plus basse en intra groupe.
Leur conclusion est la formulation la plus directe du mecanisme : "Even when they describe a social
category by taking a specific person (e.g. Let's meet Alex...), the overall degree of abstraction
still leads to generalizations towards the entire category" (L02-06, [CONFIRME]). Le modele produit
un enonce sur la categorie, habille en enonce sur une personne. C'est ce que a31 mesure sous forme
de raretes de segment attribuees a des personnes, avec un rapport de 4,45 avec etiquette contre 0,44
sans.

Peng et al. le mesurent sur les distances. Les jumeaux a persona complete sont a une distance MAD de
0,132 des agents construits sur les seules demographies, de 0,175 des agents sans aucune
information, et de **0,252 des humains qu'ils sont censes copier**, les deux ecarts a p < 0,01
(L02-01, [CONFIRME]). Autrement dit : donner a un modele cinq cents reponses reelles d'une personne
le rapproche de l'agent a etiquette, pas de la personne. C'est la these de `ARBITRAGE.md`, mesuree,
publiee, et sur Twin-2K-500.

### B.4 Le terme inter n'est pas une propriete du modele, c'est une propriete du couple modele et tache

Cette variable manquait au dossier et elle explique une part des contradictions du champ. Les memes
trois modeles de pointe, avec les memes quinze personas socio economiques, donnent une part de
variance imputable au role de R carre = 0,0004 sur des items de mathematiques du SAT (GPT-5,
PERMANOVA p = 1,000) et un d de Cohen de 0,52 a 0,58 sur des questions de preference affective
(L02-09, [CONFIRME]). Quand la question a une bonne reponse, la persona disparait ; quand elle n'en
a pas, elle reapparait. Les auteurs nomment trois mecanismes : la pression d'optimisation vers la
bonne reponse, la compression distributionnelle, et le "contextual essentialism" ou la persona reste
une invite statique jamais internalisee.

Deux resultats independants pointent dans la meme direction. Chez Shi et Haupt, la RMSE par question
correle a 0,75 avec la variance de la verite terrain : le modele est exact la ou les philosophes
sont d'accord, et se trompe la ou ils se divisent (L02-02, [CONFIRME]). Et le travail de 2609.02526
etablit la reciproque sur quatre enquetes sociales et six modeles : l'invite de persona ameliore la
prediction sur les questions a forte dispersion humaine et la degrade sur celles a faible
dispersion, tandis que **la condition sans persona fait l'inverse** (L02-10, [CONFIRME]). La
simulation efface donc precisement la ou il y a le plus a effacer, ce qui est un argument direct et
inattendu pour la these.

### B.5 Le precedent qui compte : la part effacee est la part socialement couteuse

La table de depart concluait que personne n'avait formule cette idee et que Bisbee et al. s'en
approchaient dans une phrase sans mesure. Deux travaux de cette passe la mesurent.

Zhang, Xu et Alvero comparent, sur trois etudes TESS anterieures a ChatGPT et sur les memes
questions, des reponses libres humaines (462, 1 146 et 915) a des reponses generees par trois
modeles avec les strategies d'invite reellement rapportees par des participants. Les reponses de
modele sont plus longues, plus riches en vocabulaire, et **plus homogenes** ; et sur les questions
sensibles de perception de groupe, la mesure est explicite : "In sensitive questions about group
perceptions and stereotypes, human-written responses are more likely to feature dehumanizing
language than LLM-simulated responses". La similarite cosinus a des vecteurs de concept "vermin" et
"moral disgust" montre les reponses de modele groupees plus etroitement et plus bas que les
reponses humaines (L02-13, [CONFIRME]).

Peng et al. le mesurent sur des items fermes, avec appariement individuel. Sur les 164 resultats,
55 sont etiquetes "social desirability", c'est a dire "has a socially desirable answer", et la meta
regression a effets mixtes conclut que "the correlation was significantly lower for outcomes where
social desirability was salient, suggesting twins are less capable of mimicking human responses in
socially-sensitive contexts (descriptive evidence suggests twins are more likely to provide
socially-desirable responses)" (L02-01, [CONFIRME]).

Le contraste que le dossier voulait construire existe donc deja, sur deux unites d'observation
differentes, avec referent humain. Ce qui n'existe toujours pas, c'est le meme contraste **decompose
en terme inter et terme intra**, et c'est ce qu'il faut aller chercher.

### B.6 Ce que font les correctifs aux deux termes

La table de depart classait quatre familles. Cette passe en confirme trois et en ajoute une.

**Ajustement fin sur echantillon pilote, avec mesure de degenerescence.** Wang, Hunt, Tang et Joseph
donnent le chiffre le plus parlant du corpus sur l'homogeneite : le modele non ajuste produit **19
structures de croyance uniques sur 929 simulations**, contre 340 chez les humains ; trente
observations suffisent a remonter au dela de 200, la distance de Jensen-Shannon est divisee par
deux, et l'ecart croyance action passe de pres de 100 pour cent a 23,8 et 24,4 pour cent, contre
24,7 pour cent chez les humains. Mais la recuperation des coefficients de regression plafonne a un
F1 de signe d'environ 0,769 avec un taux de faux positifs d'environ 0,333 (L02-08, [CONFIRME]).
Deux resultats negatifs y sont plus interessants encore que le resultat principal :
**l'echantillonnage a parts egales entre ethnies n'ameliore pas l'alignement des minorites**, et
retirer l'information demographique de l'invite **ne degrade pas** l'alignement par sous groupe.
[DEDUCTION] cette famille est un dilatateur qui recalibre la marge ; elle ne touche pas au terme
inter, et le second resultat negatif suggere que l'etiquette n'y contribuait deja rien.

**Ajustement fin par preference.** Chez Shi et Haupt, DPO ameliore la structure de correlation entre
questions, correlation element par element 0,020 vers 0,044 et divergence KL des correlations 0,195
vers 0,176, et augmente l'entropie moyenne de 0,737 a 0,794 ; mais il deplace la distribution de
reponse loin de l'humain, la part de reponses "Agnostic" passant de 1,5 pour cent a **34,7 pour
cent** contre 1,4 pour cent chez les humains, et la divergence KL de reponse de 0,07 a 0,40
(L02-02, [CONFIRME]). C'est un transport partiel achete au prix d'un biais de niveau, et c'est la
figure la plus nette du corpus de ce que les auteurs appellent "the variance-fidelity trade-off in
its clearest form".

**Invite et format.** L02-22 trouve que le format entretien et l'amorcage par prenom reduisent le
stereotype sur 15 groupes intersectionnels ([PROBABLE]). L02-14 trouve que l'invite de raisonnement
explicite **degrade** l'alignement de facon monotone ([PROBABLE]), ce qui converge avec le mecanisme
de pression d'optimisation de L02-09. L02-05 etablit qu'ajouter des attributs au dela de trois ne
sert jamais, sur cinq taches et cinq modeles ([CONFIRME]).

**Retrecissement bayesien explicite, famille nouvelle.** L02-20 modelise l'etat d'un individu comme
son appartenance a un dictionnaire fini de personas, chacune fournissant une distribution de
reponses produite par le modele, avec mise a jour bayesienne en forme close ([PROBABLE]). C'est le
premier travail du champ a ecrire explicitement la structure hierarchique : loi de groupe fournie
par le modele, vraisemblance fournie par les reponses de la personne. [DEDUCTION] cette famille est
la seule qui puisse en principe faire un transport a somme controlee, parce que le poids relatif des
deux termes y est un parametre et non un effet de bord. C'est la famille a surveiller.

---

## C. Ce qui se contredit

### C.1 Le signe du terme inter, et la variable qui l'explique

Le corpus contient maintenant six mesures d'un terme inter avec referent humain, et elles ne vont
pas dans le meme sens.

Gonflement : Bisbee et al. sur la polarisation affective croisee race et parti (T02-03) ; Ma et al.
sur le gout culturel, biais de coefficient de 3 a 4 fois l'effet vrai (T02-09) ; Chen, Zhu et Zheng,
gonflement median 2,3 sur le GSS et 2,5 sur le WVS (T02-02) ; Shi et Haupt, effets de specialite
fabriques de 43 a 69 points de pourcentage la ou la verite terrain est nulle (L02-02).

Aplatissement : Qin, Li et Cheng, nEMD 0,03 pour la configuration demographique contre 0,19 chez
les humains (T02-35) ; Keough, ecart Noirs contre Blancs simule -0,131 contre +0,330 dans la
population (T02-10) ; Zhang, Xu et Zhang, diversite entre pays sous 11,0 contre 37,9 chez les
humains apres ajustement culturel (T02-19) ; Kim et al. sur le climat, coefficients d'ecart signes
qui tirent chaque groupe vers le centre, jusqu'a -0,077 chez les tres conservateurs (L02-07).

**Trois variables expliquent la contradiction, et elles sont maintenant identifiables.**

La premiere est deja au dossier depuis a26 : la quantite mesuree n'est pas la meme. Un ecart de
moyenne de groupe a la verite, une distance moyenne entre deux individus tires dans deux groupes
differents, et un rapport d'amplitudes d'ecarts entre groupes sont trois choses distinctes.
L02-07 en est l'illustration la plus propre : Kim et al. mesurent un tirage de chaque groupe vers le
centre, ce qui est compatible avec un rapport d'amplitude gonfle entre deux groupes particuliers.

La deuxieme est le regime : invite contre ajustement fin. La lecture de a26 l'avait etablie et cette
passe la confirme sans exception. L'invite demographique gonfle, l'ajustement culturel ou par
preference ecrase et deplace (L02-02 sur DPO, T02-19 sur le SFT culturel).

La troisieme est neuve : **la tache**. Le meme modele donne une part de variance imputable au role
de 0,0004 sur une question a bonne reponse et un d de 0,55 sur une question de preference (L02-09,
[CONFIRME]). Et la dispersion humaine de l'item pilote le sens de l'effet de l'etiquette (L02-10,
[CONFIRME]). Toute table de resultats popsim qui melange des items ordinaux d'opinion et des items a
reponse verifiable melange deux regimes.

### C.2 Le modele efface-t-il la variance, ou la fabrique-t-il ?

Rennard et Xypolopoulos mesurent une **sur** dispersion d'entropie a toutes les profondeurs
intersectionnelles, Delta H de +0,18 a +0,23 nats (T02-07). Ozkan trouve une sous dispersion globale
a 0,40 puis une sur dispersion a 1,37 apres correctif (T02-06). Peng et al. trouvent une sous
dispersion dans 154 resultats sur 164 (L02-01). Shi et Haupt trouvent une variance intra question
de 1,9 a 3,9 fois inferieure (L02-02). L02-14 trouve **quatre modeles a variance strictement nulle**
sur une variable binaire, et sur une autre variable du meme jeu des modeles qui battent toutes les
baselines.

La variable qui explique ici est le niveau d'agregation de la mesure. Une entropie de distribution
de population peut monter pendant que la variance a l'interieur de chaque cellule tombe : il suffit
que le modele repartisse ses cellules plus largement tout en rendant chaque cellule unanime. C'est
exactement ce que decrit Shi et Haupt en une phrase, "LLMs produce perfect correlations (|r| = 1.0)
for some specialist-question pairs due to near-uniform responses within specialist groups"
(L02-02, [CONFIRME]). Le corpus contient donc au moins un cas ou l'entropie de population et la
variance intra groupe bougent en sens contraire, dans le meme papier. C'est le meilleur argument
disponible pour exiger la decomposition.

### C.3 L'etiquette apporte-t-elle de l'information ?

Chez L02-25, le comportement de 78 657 sujets dans dix jeux economiques se resume a trois dimensions
et a moins d'une douzaine de types, qui generalisent a des jeux non vus ([PROBABLE]). Chez L02-04 et
L02-03, l'etiquette demographique explique moins de 10 pour cent de la variance d'annotation et une
architecture qui la represente ne bat pas une assignation de groupe au hasard ([CONFIRME] pour les
deux). Ces deux resultats ne se contredisent qu'en apparence, et la variable est le mode
d'obtention du groupe. Les types de L02-25 sont **estimes par ajustement sur le comportement**, ce
sont des groupes latents ; les groupes de L02-03 et L02-04 sont **donnes a l'avance par une
etiquette declarative**. La litterature statistique dit la meme chose depuis Freedman : le modele de
voisinage, qui remplace la demographie par le contexte, bat la regression ecologique et le modele de
King, 34 et 36 pour cent contre 29 et 85 et 30 et 72, la verite etant 35 et 28 (L02-11, [CONFIRME]).
C'est la meme observation que a31 fait chez nous : sans etiquette 0,41, avec etiquette 0,19.

---

## D. Ce que ca permet de tester chez nous tout de suite

Les couts sont donnes en appels de modele et en heures d'analyse, sur les jeux deja au depot.

**D.1 Reproduire les trois distances de Peng et al. sur nos propres agents.** Cout : zero appel
nouveau si les sorties des conditions "sans etiquette", "etiquette demographique" et "ancre sur
reponses reelles" existent deja dans `resultats/`, sinon une nuit. Calculer les trois MAD moyennes,
persona complete contre etiquette seule, contre persona vide, contre humains. Le test est binaire :
si notre MAD a l'etiquette est plus petite que notre MAD a l'humain, la these de `ARBITRAGE.md` est
verifiee chez nous avec la mesure exacte de la seule equipe qui l'a publiee, et devient comparable
ligne a ligne. C'est le test le moins cher et le plus decisif de la liste.

**D.2 Le contraste sensible contre temoin, en inter et en intra separement.** Cout : une demi
journee d'analyse sur les sorties existantes du GSS. C'est le test que la table de depart designait
deja comme prioritaire ; il devient plus urgent, parce que L02-13 et L02-01 ont pris la moitie de la
revendication. Le geste neuf est de calculer le ratio **intra** et le ratio **inter** separement sur
les items sensibles et sur les items temoins apparies, ce que ni Zhang, Xu et Alvero, ni Peng et al.
ne font. Etiqueter les items comme Peng et al. l'ont fait, "has a socially desirable answer", et
publier le nombre d'items dans chaque classe.

**D.3 Le plafond de variance explicable par l'etiquette, item par item.** Cout : une heure, aucun
appel de modele. Reproduire le geste de Hu et Collier sur nos jeux : regression a effets mixtes de
la reponse humaine sur les etiquettes en effets fixes et un effet aleatoire par item, et publier le
R carre marginal. Cela donne le denominateur qui manque a toutes nos figures : un gonflement de
l'inter d'un facteur 5,9 sur un item dont le R carre marginal humain vaut 0,03 n'a pas le meme sens
que sur un item a 0,72. **Ce chiffre change l'interpretation de a1, a6, a18 et a21 sans rejouer un
seul appel.**

**D.4 Le temoin de permutation de groupe, deja fait, a repositionner.** Cout : nul, c'est
`resultats/a1-controle-permutation.csv` et `a6-controle-permutation.csv`. Orlikowski et al.
publient exactement ce temoin en 2023 et notre note ne le cite pas. Il faut le citer et verifier que
notre convention est la meme : tailles de groupes preservees, seule l'affectation permutee.

**D.5 La comparaison a l'imputation par regression, sur les memes items.** Cout : une demi journee,
aucun appel. Construire trois predicteurs statistiques sur nos donnees, la moyenne de cellule, la
regression logistique, et l'appariement sur moyenne predite (predictive mean matching), puis publier
pour chacun le ratio intra et le ratio inter, dans le meme tableau que les agents. Le resultat
attendu d'apres L02-12 et T02-42 est que la moyenne de cellule ecrase l'intra a zero par
construction et que l'appariement sur moyenne predite le conserve. **Si nos agents se placent entre
les deux, la these devient une these de position et non une these d'accusation**, et elle est bien
plus difficile a refuter.

**D.6 Separer les items a bonne reponse des items d'opinion.** Cout : une heure de retri. D'apres
L02-09 et L02-10, le regime n'est pas le meme. Si nos jeux contiennent des items de connaissance ou
de calcul melanges a des items d'attitude, tout ratio agrege est une moyenne de deux populations.

**D.8 Socle contre aligne, ce que la passe apporte a la question ouverte de `ARBITRAGE.md`.**
Cout : nul avant la nuit de calcul, une lecture. Trois elements nouveaux cadrent l'attente. (a)
Shi et Haupt font l'experience la plus proche disponible : DPO sur Llama-3.1-8B ameliore la
structure de correlation entre questions, correlation element par element 0,020 vers 0,044, sans
resoudre l'effondrement de variance, et en deplacant fortement la distribution de reponse, part
d'"Agnostic" de 1,5 a 34,7 pour cent contre 1,4 chez les humains (L02-02, [CONFIRME]). **Un
ajustement par preference deplace donc le partage sans le reparer.** (b) Les trois mecanismes de
L02-09, pression d'optimisation, compression distributionnelle et essentialisme contextuel, sont
attribues par leurs auteurs au post entrainement pour le premier et au pre entrainement pour le
second, sans test qui les separe ([CONFIRME] pour l'attribution, non teste). (c) Ku et al. avaient
deja montre que l'abliteration deplace le ratio de variance dans deux sens opposes selon la
famille, 0,85 vers 0,90 et 0,67 vers 0,45 (T02-42). **La prediction a poser avant la nuit de calcul
est donc que le socle changera l'ampleur et non le signe de la substitution**, et le test qui
tranche est celui de a31, rapport des fausses raretes de segment aux raretes de personne, rejoue
sur le modele socle.

**D.7 Le test de dispersion humaine comme moderateur.** Cout : une heure. Pour chaque item, calculer
la dispersion des reponses humaines (entropie normalisee pour les nominales, dissention pour les
ordinales, comme L02-10), puis regresser notre ratio intra et notre ratio inter sur elle. Prediction
issue de L02-02 et L02-10 : le ratio intra doit se degrader quand la dispersion humaine augmente.
Si c'est vrai chez nous, nous avons la loi qui manque au champ, et elle tient en une figure.

---

## E. Ce que personne n'a fait

Cette section remplace celle de la table de depart sur trois points, et en conserve quatre.

**E.1 Ce qui n'est plus disponible.** La formule "personne n'a formule que la part effacee est celle
que les gens ne disent pas ouvertement" **doit tomber**. Zhang, Xu et Alvero l'ont mesuree sur du
texte libre avec referent humain apparie sur les memes questions TESS (L02-13, [CONFIRME]) ; Peng et
al. l'ont mesuree sur 55 items fermes etiquetes "social desirability" parmi 164, avec une meta
regression et un signe (L02-01, [CONFIRME]). Deux equipes, deux unites d'observation, deux fois le
meme signe. Ce qui reste a popsim est plus etroit et plus solide : **le contraste sensible contre
temoin apparie, decompose en terme inter et terme intra, avec un plancher de reinterrogation.**
Aucun des deux ne separe les deux termes, et aucun n'a de plancher.

**E.2 Ce qui n'est plus disponible non plus.** La dissociation entre exactitude et structure sur les
memes participants, que la table de depart donnait comme non faite, est publiee deux fois. Peng et
al. la publient avec un exemple travaille : r_demo = 0,105 contre r_full = 0,555 pour une exactitude
individuelle de 0,892 contre 0,907 (L02-01, [CONFIRME]). Et van Buuren la publie dans un manuel sous
sa forme generale, "the method yielding the lowest RMSE is bad for imputation", RMSE 0,725 contre
1,025 (L02-12, [CONFIRME]). Ce qui reste est la dissociation entre exactitude et **partage inter et
intra**, qui n'est publiee nulle part.

**E.3 Ce que la passe confirme comme non fait, et c'est le coeur de ce qui reste.**

1. **Aucun tableau a quatre cases**, inter et intra, avant et apres correctif, sur les memes items et
   le meme modele. Reverifie sur les 27 nouvelles lignes. L02-08 mesure la dispersion avant et apres
   et ne mesure aucun terme inter ; L02-02 mesure l'entropie et la structure de correlation avant et
   apres DPO et ne mesure aucun terme intra par groupe ; L02-21 apprend explicitement le deplacement
   entre contextes et ne publie rien sur l'intra.
2. **Aucune identite additive ni contrainte de somme.** Rien de neuf.
3. **Aucun plancher de bruit humain par reinterrogation des memes personnes.** Rien de neuf. Peng et
   al. travaillent sur Twin-2K-500, qui contient le materiel, et ne le construisent pas.
4. **Aucun correctif evalue contre une baseline non LLM.** Confirme sur les nouvelles lignes.
   L02-14 est le seul travail de la passe a poser une baseline vraiment severe, une marginale
   insensible aux conditions tiree de la distribution humaine, et il constate qu'aucun modele ne la
   bat sur la quantite ([PROBABLE]).

**E.4 Ce que la passe fait apparaitre comme non fait, et qui est neuf.**

5. **Personne dans ce champ n'ecrit que la sous dispersion est le comportement attendu d'un
   estimateur de moyenne conditionnelle, ni ne le teste contre l'imputation.** Ku et al. l'ecrivent
   en une phrase et n'ont pas de baseline d'imputation ; Peng et al. emploient le mot "shrunk" sans
   renvoyer a la statistique. **Aucun travail du corpus ne cite Little et Rubin, van Buuren, Meng,
   Robinson ni Freedman**, a l'exception d'Orlikowski et al. qui citent Robinson et Freedman pour le
   seul cadre conceptuel. Un papier qui poserait la simulation par etiquette comme un cas
   d'imputation par valeur predite, et qui la comparerait aux trois methodes standard, occuperait
   une place vide. C'est peu cher, voir D.5.
6. **Personne n'indexe son ratio de variance sur le plafond de variance explicable par l'etiquette.**
   Hu et Collier fournissent le denominateur, personne ne l'utilise, et aucun des travaux de
   variance du corpus ne le cite. Voir D.3.
7. **Personne ne separe les items a bonne reponse des items d'opinion dans un meme protocole de
   variance.** L02-09 le fait pour la fidelite de role et pas pour la variance. Voir D.6.
8. **Personne n'a repris le modele de voisinage de Freedman dans ce champ.** L'idee est qu'un
   predicteur qui utilise le contexte et ignore la demographie bat les modeles demographiques. Notre
   a31 mesure exactement cela sans le nommer, 0,41 sans etiquette contre 0,19 avec. **Le nommer, et
   citer Freedman, transforme un resultat local en instance d'un fait statistique connu**, ce qui
   est la meilleure defense possible en revue.

---

## F. Ce que je n'ai pas pu verifier

1. **Les valeurs numeriques du ratio d'ecarts types de Peng et al.** Le texte donne le compte, 154
   sur 164 et 140 significatifs, mais les **valeurs** du ratio sont dans les figures 2, 10 et 16, qui
   sont des images. Aucun ratio moyen n'est ecrit dans le texte de l'article ni dans le materiel
   supplementaire lu. Notre chiffre ne peut donc pas etre compare au leur en valeur, seulement en
   signe et en frequence.
2. **La version publiee dans Science Advances de Peng et al.** est derriere un 403 de science.org.
   La lecture porte sur arXiv 2509.19088 v5 du 19 avril 2026. L'ordre des auteurs differe entre la
   notice OpenAlex de l'article publie et la page de titre du PDF arXiv ; la liste retenue ici est
   celle du PDF.
3. **Le coefficient exact de la desirabilite sociale dans la meta regression de Peng et al.** Il est
   dans la figure 11, une image. Seul le signe et la significativite sont dans le texte. **Ne pas
   citer d'ampleur.**
4. **Les tables 5, 22, 23 a 27 de Kamruzzaman et al.**, qui portent les valeurs de coherence
   directionnelle par attribut, n'ont ete lues que partiellement dans la conversion en texte, les
   colonnes se recouvrant. Les valeurs citees ici, kappa de politesse et rho de LSVC, viennent du
   corps de l'article et non des tables.
5. **Les figures 1 a 3 de Wang, Hunt, Tang et Joseph**, qui portent les distributions de croyance et
   les distances JS par ethnie, sont des images. Le "au moins divise par deux" est leur phrase, pas
   une lecture de valeurs.
6. **La reference "Freedman, 2015" citee par Orlikowski et al.** n'a pas ete identifiee avec
   certitude. Le texte lu ici est le Technical Report 549 de 1999, qui correspond a l'entree de la
   premiere edition de l'International Encyclopedia of the Social and Behavioral Sciences ; la
   deuxieme edition est de 2015. Les chiffres cites sont ceux du rapport de 1999. **Verifier avant
   de citer une annee.**
7. **Robinson 1950 n'a pas ete lu.** Les valeurs 0,53 et -0,11 sont lues dans Freedman, qui les
   attribue a Robinson. La valeur souvent citee de 0,946 pour les neuf divisions du recensement ne
   figure pas dans Freedman et n'a pas ete verifiee. [NON LU] pour Robinson lui meme.
8. **Meng 1994 sur la non congenialite n'a pas ete lu.** Le PDF de Statistical Science n'est pas
   accessible en telechargement direct. C'est pourtant le resultat theorique le plus proche de la
   these ; il est signale comme piste, pas comme preuve.
9. **Little et Rubin 2002, page 64**, citee par van Buuren pour le degre de sous estimation de la
   variabilite, n'a pas ete ouverte.
10. **Les cinq references lues au resume seulement de la section A** (L02-16 a L02-24) portent des
    chiffres qui viennent de leurs resumes. Trois d'entre elles sont importantes et doivent etre
    lues sur PDF avant tout usage externe : L02-17 (SSDataBench, PNAS), L02-18 (realisme contre
    effet de traitement, 59 508 participants) et L02-25 (trois dimensions, 78 657 sujets), cette
    derniere parce que c'est le contre argument le plus serieux a la these.
11. **La recherche par absence a encore faibli.** Deux des affirmations d'absence de la table de
    depart sont tombees dans cette seule passe, et les deux sources qui les font tomber etaient
    accessibles depuis des mois. La descente de citations a couvert quatre points d'ancrage ; elle
    n'a couvert ni la psychometrie de la desirabilite sociale anterieure aux modeles de langage, ni
    la sociologie quantitative hors arXiv au dela de ce que la citation de Bisbee ramene, ni SSRN.
    **Il faut supposer qu'il en reste.**
12. **OpenAlex a atteint sa limite de budget quotidien en cours de passe**, ce qui a interrompu la
    descente de citations sur ce service apres le premier point d'ancrage. Les trois autres
    descentes ont ete faites par Semantic Scholar, dont la couverture des actes de conference
    recents n'est pas la meme. Un second passage OpenAlex sur Wang, Morgenstern et Dickerson, sur
    Qin, Li et Cheng et sur Ku et al. reste a faire.
13. **La recherche par mots cles d'arXiv n'a rien rendu** pour "language model multiple imputation
    survey", "poststratification language model survey" et "language model small area estimation".
    Le moteur exige que tous les termes apparaissent, donc l'absence de resultat n'est pas une
    preuve d'absence de travaux, seulement du fait qu'aucun titre ou resume ne porte ces
    combinaisons.
14. **Le budget de recherche web de la session etait epuise a son debut**, ce qui a interdit toute
    recherche generaliste. Tout ce qui precede vient des API OpenAlex, Semantic Scholar et Crossref,
    du moteur de recherche d'arXiv, et de telechargements directs.
