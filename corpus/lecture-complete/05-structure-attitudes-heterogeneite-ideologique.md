# 05. Structure des attitudes et heterogeneite ideologique, lecture complete

Seance du 8 septembre 2026 au soir. Methode : `corpus/lecture-complete/00-CONSIGNE.md`. Grille :
`corpus/00-GRILLE.md`. Ce fichier ne remplace pas `corpus/05-structure-attitudes-heterogeneite-ideologique.md`,
il le prolonge : la table de 52 entrees de ce fichier reste valable et n'est pas recopiee ici,
seules les entrees qui portent une conclusion nouvelle y sont rappelees. Aucun fichier existant
n'a ete modifie.

Point de depart impose par la mission : `resultats/a32-papier-diversite-droite.md` (Luders,
Carpentras et Quayle 2024, Chen et al. « Broken Egg », la litterature ResIN) et
`resultats/a30-variete-interne-des-camps.md` (nos mesures : rapport droite sur gauche 1,122 sur
le GSS, 2,47 sur l'avortement, 0,97 sur l'economique personnel, correlation economique x social
0,447 a gauche contre 0,311 a droite, et une simulation qui exagere l'ecart au lieu de l'effacer).

Quatre questions ont ete suivies jusqu'a epuisement des citations :
1. qui a mesure l'heterogeneite intra camp sur des reponses individuelles, et avec quel resultat ;
2. l'asymetrie de contrainte ideologique, et la these d'« Asymmetric politics » qui predit
   l'inverse de notre mesure ;
3. la dynamique temporelle de la variete des camps ;
4. ce que tout cela predit pour une simulation a etiquette.

Certitude : **[CONFIRME]** lu dans le texte, **[PROBABLE]** lu en resume ou dans une source
secondaire fiable, **[NON LU]** titre seul. Aucun chiffre [PROBABLE] ne porte une conclusion.

---

## La table etendue

Colonne « trouve par » : *aval* = trouve en descendant les citations d'une reference confirmee,
*amont* = trouve en remontant sa bibliographie, *initiale* = deja dans `corpus/05`,
*interne* = venu de `resultats/a30` ou `a32`.

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | certitude | trouve par |
|---|---|---|---|---|---|---|---|---|---|---|
| 05-53 | Chen, Speer, de Bruin, Carpentras et Warncke, *A « broken egg » of U.S. Political Beliefs : Using response-item networks (ResIN) to measure ideological polarization*, *Network Science* 13, e20, 2025, DOI 10.1017/nws.2025.10016, acces libre CC BY-NC-ND | la contrainte des systemes de croyances americains a t elle change de 2000 a 2020, et de facon symetrique entre camps ? | ANES 2000, 2004, 2008, 2012, 2016, 2020, six vagues, cinq items communs : `spend_serv`, `gov_health`, `guar_jobs`, `aid_black` (7 modalites chacun) et `abort` (4 modalites), soit 32 noeuds | ResIN : noeud = modalite de reponse, arete = phi de Guilford entre indicatrices, paires du meme item exclues, phi negatifs a zero, Fruchterman-Reingold puis ACP | densite de liens D = somme des poids d'arete sur le nombre de paires de noeuds d'items differents, calculee sur le graphe entier et sur chaque sous graphe partisan ; linearisation = etendue X sur etendue Y ; IQR par 200 reechantillonnages a 80 % sans remise | densite globale +51,1 %, de 0,032 en 2000 a 0,049 en 2020, avec le saut le plus rapide entre 2016 et 2020 ; « Compared to its Republican counterpart, the Democratic subgraph generally showed a lower link density, with the exception of 2020 » ; la densite republicaine culmine en 2008 et decline de 2008 a 2020 ; centralite de force par camp : l'avortement passe des attitudes les moins importantes des democrates du debut des annees 2000 a **l'attitude la plus centrale du camp democrate en 2020**, alors que « Among the Republican community, meanwhile, abortion attitudes never played a pivotal role as an ideological anchor in any of the measured years » ; l'aide aux Noirs perd sa position centrale dans le camp liberal | cinq items seulement, dont quatre economiques ou raciaux et un moral ; les auteurs reconnaissent que « both the structure of ResIN and the derived polarization measures depend on the selection of issue items » ; les valeurs numeriques des densites par camp ne sont que dans la figure 7 ; aucun controle du nombre de modalites par camp | soutient et **date** notre 2,47 sur l'avortement : c'est un fait de 2020, pas une structure | [CONFIRME] | interne puis aval (version publiee, inconnue de `a32` qui n'avait que le preprint OSF) |
| 05-54 | Warncke, Chen, Speer, de Bruin, Luders et Carpentras, *ResIN : A New Method to Analyze Socio-political Attitude Systems*, chapitre 5 de *Computational Social Science of Social Cohesion and Polarization*, Springer, 2026, DOI 10.1007/978-3-032-01373-6_5, acces libre | que peut on inferer de la forme d'un reseau ResIN, et que valent les asymetries visuelles ? | simulations ; ESS pour la Slovaquie, l'Espagne et l'Allemagne ; ANES 2020, 64 items | ResIN, plus un algorithme dirige par les forces sans redimensionnement, plus une ACP a axes obliques en comparaison | taille de cluster et distance normalisee en fonction de la correlation moyenne inter items, du nombre d'items et du desequilibre d'effectif | la taille d'un cluster **decroit** avec la correlation moyenne, fortement de 0 a 0,4 puis a plat au dela ; elle est « almost unchanged » quand on change le nombre d'attitudes par groupe ; la distance normalisee « do not change for uneven group sizes » (90 % contre 10 %) ; Espagne : les attitudes les plus conservatrices forment un amas serre et la deuxieme modalite la plus conservatrice appartient deja a l'amas liberal, ce que les auteurs expliquent par « while the ideological left tends to have broader popularity, it is also more diverse (...) By contrast, the right remains cohesive and ideologically disciplined » ; Allemagne : trois amas, celui qui melange gauche et modere est plus gros que chacun des deux amas de droite ; ANES 2020 : reseau en U, les deux extremes se rejoignent sur l'intervention exterieure, le libre echange, la securite sociale et les routes ; ACP a deux facteurs correles a 0,68, 21 % et 15 % de la variance des items | les simulations calibrent la taille de cluster, pas la densite de sous graphe ; les cas nationaux sont interpretes qualitativement | **contredit la lecture univoque de la figure 2 de Luders** : avec la meme methode, la meme equipe trouve la droite plus cohesive en Espagne et la gauche plus cohesive aux Etats Unis | [CONFIRME] | aval de Luders 2024 |
| 05-55 | Ondish et Stern, *Liberals Possess More National Consensus on Political Attitudes in the United States : An Examination Across 40 Years*, *Social Psychological and Personality Science* 9(8), 2018, 935-943, DOI 10.1177/1948550617729410 | quel camp a le plus de consensus au niveau national ? | GSS et ANES, plus de 80 000 personnes, environ 400 questions politiques, environ 40 ans | modele « one-with-many » du Social Relations Model, ICC des items imbriques dans les individus | part de variance attribuable aux items, standardisee sur la variance totale, calculee separement pour liberaux, moderes et conservateurs | **liberaux > conservateurs > moderes** en consensus, resultat stable apres ajustement sur education, genre et origine | texte non lu, article sous paywall SAGE, sans version libre ; mecanisme propose (les conservateurs feraient consensus au niveau local) non teste | **c'est l'homologue publie de notre 1,122** : meme population, meme sens, mesure differente | [PROBABLE] | aval de la litterature belief network, via Brandt et al. 2021 et Brandt et Sleegers 2021 qui la decrivent en detail |
| 05-56 | Brandt, Aron, Parker, Rodas et Shaffer, *Leftists possess more national consensus in Europe in one of two datasets*, preprint PsyArXiv dm4wt, 2021, et *Social Psychological and Personality Science* 13(4), 2022, 862-874, DOI 10.1177/19485506211041825 | l'effet de consensus liberal existe t il hors des Etats Unis ? | European Social Survey, 38 pays, 9 vagues 2002-2018, N = 376 129, 30 items en moyenne (13 en 2006, 57 en 2002) ; Eurobarometre, 18 pays, 33 vagues 1982-2002, N = 375 830, 20 items en moyenne | meme modele one-with-many qu'Ondish et Stern, puis regression multiniveaux des estimations de consensus sur deux indicatrices | pente moderes contre gauche, et droite contre gauche, sur les estimations de consensus par pays et par vague ; plusieurs specifications d'imbrication, toutes rapportees | ESS : replication nette, la gauche a plus de consensus que les moderes dans tous les modeles et plus que la droite dans presque tous ; les trois modeles non significatifs sont ceux qui ajoutent des pentes aleatoires sur les deux indicatrices. Eurobarometre : **pas de replication**, la difference gauche droite n'est jamais significative. Ecart moyen en valeur absolue gauche moins droite dans l'ESS : **-0,022** pour les pays presents dans les deux enquetes, -0,007 pour les pays propres a l'ESS. Correlation des ecarts par pays entre ESS et EB : r(13) = 0,72, p = 0,002, 73 % de meme signe | analyses non preenregistrees, toutes les specifications publiees faute de choix ; l'Eurobarometre porte surtout sur l'integration europeenne | l'effet existe mais **il varie de signe selon le pays et selon le jeu d'items** : la meme prudence que nous imposons a notre 1,122 | [CONFIRME] | aval d'Ondish et Stern |
| 05-57 | Brandt et Sleegers, *Evaluating Belief System Networks as a Theory of Political Belief System Dynamics*, preprint PsyArXiv b8hfa, 2020, et *Personality and Social Psychology Review* 25(2), 2021, 159-185 | un modele de dynamique de reseau de croyances individuel suffit il a produire les regularites de population ? | simulations ; 40 populations de 1 000 agents chacune | reseau de croyances a 10 noeuds, 8 d'enjeux et 2 d'identite, probabilite de connexion 0,8, aretes toutes positives, multiplicateur de contrainte dans {0,5 ; 1 ; 2 ; 3 ; 4}, 20 pas de temps | influences exogenes identitaires tirees dans N(0,02 ; 0,04), donc legerement a droite ; influences d'enjeux = 0,25 x identite + N(0,03 ; 0,04), donc legerement a gauche ; bruit N(0 ; 0,01) ; puis ICC des enjeux, comme Ondish et Stern | **les liberaux ont le plus de consensus dans 35 populations sur 40 (87,5 %), les conservateurs dans 5 (12,5 %), les moderes dans aucune** ; hors liberaux, les conservateurs battent les moderes dans 34 sur 40. Mecanisme : « The liberal consensus effect seems to occur because policies are pushed in a liberal/left-wing direction by the exogenous influences for all of the simulated participants » | simulation, pas de donnees ; le resultat depend entierement du couple d'hypotheses tire d'Ellis et Stimson | **explication generative de notre 1,122, et elle predit son inversion** : la ou la derive agregee de l'opinion va vers la droite, l'effet doit s'inverser. C'est exactement ce que nos items d'ordre montrent | [CONFIRME] | aval d'Ondish et Stern |
| 05-58 | Cely, *One more constrained than the other : Asymmetrical ideological alignment and its implications for polarization*, *European Journal of Political Research* 64(4), 2025, 1945-1973, DOI 10.1111/1475-6765.70016 | les partisans de gauche sont ils plus alignes dans leurs croyances que ceux de droite, en Europe ? | European Social Survey vagues 4 et 8 (2008, 2016), partisans de 131 partis dans 15 pays europeens, apparies aux positions ideologiques de leur parti | methodes conventionnelles plus modelisation de reseau de croyances | alignement ideologique des croyances a l'interieur de chaque camp partisan | « partisans on the ideological left exhibit greater alignment in their beliefs compared to those on the right, an asymmetry that extends across various issues » ; « both at the European level and within national contexts, there is a broad and substantive asymmetry between the right and the left » ; mais « a significant shift in ideological alignment on sociocultural issues on the right » ; influence marginale du flou de position et de la nichitude programmatique | resume seul, PDF Wiley inaccessible (403), aucun depot ouvert servant le texte ; aucun chiffre repris | **le plus proche homologue publie de notre resultat**, meme sens, autre continent, autre mesure ; et il annonce deja notre exception : la droite se resserre sur le socioculturel | [PROBABLE] | aval de la litterature belief network |
| 05-59 | Kozlowski et Murphy, *Issue alignment and partisanship in the American public : Revisiting the « partisans without constraint » thesis*, SocArXiv jex9k 2019, *Social Science Research* 94, 2021, 102498, DOI 10.1016/j.ssresearch.2020.102498 | la contrainte inter enjeux a t elle augmente depuis 2004 ? | ANES 1972-2016, meme batterie et memes mesures que Baldassarri et Gelman | modeles additifs generalises mixtes (GAMM) sur les correlations inter items, par domaine et par sous groupe | alignement d'enjeux = correlation entre positions ; alignement partisan = correlation entre position et parti ou etiquette | forte croissance de l'alignement d'enjeux apres 2004, **maximale sur les domaines economique et droits civiques, faible sur le domaine moral et sur la securite** ; en 2016 la correlation entre items economiques atteint environ 0,4 jusque dans le tercile de revenu le plus bas ; la croissance est presque entierement confinee aux blancs ; par parti : « Alignments among Democrats generally decrease between 1972 and 2004 but stabilize or climb in each of the three domains and across domain after 2004. Republicans showed greater growth than Democrats prior to 2004, but they show no consistent growth in issue alignment after 2004 » | preprint lu, version publiee non lue ; pas d'intervalle chiffre reproduit ici, les resultats sont des courbes | **deuxieme confirmation independante du croisement vers 2016-2020**, avec une methode qui n'a rien a voir avec ResIN | [CONFIRME] | amont de Chen 2025 via Baldassarri et Gelman |
| 05-60 | Hanel, Zarzeczna et Haddock, *Sharing the Same Political Ideology Yet Endorsing Different Values : Left- and Right-Wing Political Supporters Are More Heterogeneous Than Moderates*, *Social Psychological and Personality Science* 10(7), 2019, 874-882, DOI 10.1177/1948550618803348 | les extremes sont ils plus homogenes que les moderes ? | ESS, 20 pays europeens plus Israel | comparaison directe de variabilite entre groupes moderes, de gauche et de droite | dispersion des valeurs humaines de Schwartz, plus attitudes envers les immigres et confiance dans les institutions | « the values of more extreme (left-wing or right-wing) supporters are usually more heterogeneous than those with more moderate views », replique sur les attitudes envers les immigres et la confiance ; revenu, religiosite et pression parasitaire du pays ne moderent pas | resume seul, SAGE inaccessible ; porte sur des **valeurs**, pas sur des positions de politique publique | **contredit frontalement l'ordre d'Ondish et Stern** (moderes les moins consensuels) ; la variable qui separe les deux est le domaine de mesure | [PROBABLE] | aval d'Ondish et Stern, via Brandt et al. 2021 |
| 05-61 | Grossmann et Hopkins, *Ideological Republicans and Group Interest Democrats : The Asymmetry of American Party Politics*, *Perspectives on Politics* 13(1), 2015, DOI 10.1017/S1537592714003168, et *Asymmetric Politics*, Oxford University Press, 2016 | les deux partis americains sont ils des images en miroir ? | synthese de litterature et de donnees d'opinion | aucun modele formel | argumentation qualitative | « The Republican Party is primarily the agent of an ideological movement whose supporters prize doctrinal purity, while the Democratic Party is better understood as a coalition of social groups seeking concrete government action » ; et, decisif pour nous : « This asymmetry is reinforced by American public opinion, which favors left-of-center positions on most specific policy issues yet simultaneously shares the general conservative preference for smaller and less active government » | resume seul, article et livre sous paywall ; aucune mesure de dispersion individuelle | **la these qui predit l'inverse de notre mesure, et qui contient sa propre refutation** : la premisse qu'elle invoque est exactement l'hypothese generative de 05-57 | [PROBABLE] | recherche dirigee (mission) |
| 05-62 | Liu, Diab et Fried, *Evaluating Large Language Model Biases in Persona-Steered Generation*, *Findings of ACL* 2024, 9832-9850, DOI 10.18653/v1/2024.findings-acl.586 | un modele sait il jouer une personne dont les traits ne vont pas ensemble ? | Pew American Trends Panel ; personas construites a deux composantes, une demographie et une position | gpt-3.5-turbo, Llama-2-70b-chat, Llama-2-7b-chat, tulu-2-dpo-70b et 7b, tulu-2-70b et 7b | persona *incongrue* = persona ou appartenir a la demographie **diminue** la probabilite de la position dans les donnees Pew ; score de pilotabilite juge par GPT-4 (accord humain 96,3 %, kappa 0,808) ; plus quatre metriques auxiliaires de diversite et de caricature | pilotabilite moyenne sur les personas politiques : **base 91,6, congrue 92,5, incongrue 75,9** ; race 89,3 / 89,1 / 81,2 ; genre 83,8 / 82,8 / 78,1 ; ecart moyen congrue moins incongrue **9,7 %**, maximal sur le politique et significatif pour tous les modeles y compris GPT-3.5. Diversite semantique 0,431 congrue contre 0,416 incongrue ; exageration 0,146 contre 0,114 ; individuation 0,624 contre 0,655. R2 = 0,018 (p = 0,033) entre le taux de reponse en QCM et la pilotabilite en generation ; le modele est plus pilotable vers la position qu'il a choisie en QCM **51,5 % du temps**, a peine mieux que le hasard. Les modeles ajustes par RLHF sont plus pilotables, surtout vers les positions associees aux liberaux et aux femmes, mais « significantly decrease the range of views and topics expressed » | personas a deux composantes seulement ; juge automatique ; pas de reference humaine de dispersion | **repond a la question 2 de « ce que personne n'a fait » de `corpus/05`** : la contre pression a bien ete testee cote machine, et elle coute 16,6 points de pilotabilite sur l'axe politique contre 7,9 sur la race et 4,7 sur le genre | [CONFIRME] | aval de CoMPosT (05-16) et de Santurkar (05-14) |
| 05-63 | Chuang, Nirunwiroj, Studdiford, Goyal, Frigo, Yang, Shah, Hu et Rogers, *Beyond Demographics : Aligning Role-playing LLM-based Agents Using Human Belief Networks*, arXiv 2406.17232v2, 2024 | conditionner sur une croyance vaut il mieux que conditionner sur une demographie ? | Controversial Beliefs Survey de Frigo 2022, N = 564 sur MTurk en 2018, 64 sujets, echelle a 6 points sans neutre | ChatGPT (gpt-3.5-turbo-0125), GPT-4o mini, Mistral, LLaMA 3.1 ; apprentissage en contexte et reglage fin supervise | reseau de croyances par analyse factorielle, 9 facteurs orthogonaux ; erreur absolue moyenne entre l'agent et son jumeau humain sur les sujets de test | ChatGPT : sans demographie 1,68, avec demographie **1,70** (donc rien), avec demographie plus une croyance du **meme** facteur 1,34 (gain relatif 22,54 %), avec une croyance d'un **autre** facteur 1,67 (donc rien), borne haute 0,42. Par categorie, le gain relatif vaut 60,83 % sur les fantomes et 56,11 % sur les mediums, mais **6,19 % sur le facteur partisan** et 19,72 % sur l'economique ; GPT-4o mini 3,39 % sur le partisan, Mistral 2,94 %, LLaMA 3,1 14,61 %. Le reglage fin donne le meme patron (gain 59,45 % fantomes contre 14,16 % partisan) | echantillon MTurk de 2018, sujets en partie non politiques ; une seule croyance semee | **repond negativement a A12 et a la question 5 de `corpus/05`** : conditionner sur une croyance plutot que sur une etiquette marche, mais presque pas la ou nous en avons besoin, sur l'axe partisan | [CONFIRME] | aval de Boutyline et Vaisey, cote informatique |
| 05-64 | van Noord, Turner-Zwinkels, Kesberg, Brandt, Easterbrook, Kuppens et Spruyt, *The nature and structure of European belief systems*, *European Sociological Review* 41(1), 2025, 143-161, DOI 10.1093/esr/jcae011, acces libre | combien de systemes de croyances distincts coexistent en Europe, et en quoi different ils ? | ESS, 23 pays europeens, 20 croyances | analyse de classes correlationnelles (CCA), variante de la RCA de Baldassarri et Goldberg | nombre de systemes par pays, correlation entre dimension culturelle et dimension economique par groupe, force moyenne des associations | 2 a 5 systemes par pays, resumables en deux groupes ; correlation culturel x economique : groupe 1 +0,24 sur les systemes moyens et +0,14 sur les systemes individuels, groupe 2 **-0,20** et -0,03 ; « Unexpectedly, the groups did not differ in the strength of association between beliefs » ; l'appartenance au groupe 2 est liee au vote populiste d'extreme droite et a l'abstention ; l'education est le premier predicteur, significative pour 67 % des systemes | les dimensions economique et culturelle n'unissent que quelques croyances sur 20 et correlent faiblement | **contredit Boutyline et Vaisey** : ici l'heterogeneite est dans la logique et pas dans la quantite, chez eux l'inverse | [CONFIRME] | amont de Chen 2025 |
| 05-65 | Warncke, *What Explains Country-Level Differences in Political Belief System Coherence ?*, *Political Behavior* 47(4), 2025, 1853-1876, DOI 10.1007/s11109-025-10015-9, acces libre | la coherence des croyances est elle une propriete des personnes ou du systeme politique ? | ESS, 38 pays europeens, 2002-2020 | modeles de reseau statistiques dedies | mesure de coherence derivee du reseau, plus centralites de noeud | les systemes politiques a liens programmatiques entre citoyens et partis soutiennent des croyances de masse « far more coherent » que ceux ou le lien passe par des faveurs personnelles ; **un peu moins d'un tiers** de cet effet est mediatise par la centralite relative de l'attachement ideologique symbolique ; « Abstract ideological summary positions are not central to all belief systems, but where they are, mass beliefs tend to be more coherent overall » | resume et introduction lus, corps parcouru ; aucun chiffre d'effet repris | **l'ancrage theorique de notre contraste C2 contre C3** : mettre l'etiquette dans l'invite rend l'etiquette maximalement centrale, donc rend le systeme maximalement coherent | [CONFIRME] pour l'enonce cite | amont de Chen 2025 |
| 05-66 | Steiglechner, Smaldino et Merico, *How opinion variation among in-groups can skew perceptions of ideological polarization*, *PNAS Nexus* 4(7), 2025, pgaf184 | pourquoi les mesures de polarisation ideologique se contredisent elles ? | cadre formel, plus donnees d'opinion allemandes sur le climat | modele de perception dependante du contexte | perception de la distance entre opinions, conditionnee par la variance intra groupe | quand la variance d'un groupe **diminue**, ses membres percoivent les opinions deviantes comme plus lointaines et surestiment la polarisation ; « perceived polarization may depend as much on the dynamics of in-group variance as it does on actual opinion divergence in society » ; la direction de l'effet varie dans le temps et selon le groupe partisan | resume, encadre de portee et introduction lus ; les chiffres allemands sont dans les figures et n'ont pas ete extraits | donne un **enjeu** a la variance intra camp : ce n'est pas une statistique descriptive, c'est ce qui regle la perception de la polarisation | [CONFIRME] pour le cadre, [NON LU] pour les chiffres | aval de la litterature ResIN |
| 05-67 | anonyme, *Auditing Alignment Controllability in LLMs via Political Axes*, arXiv 2607.23519, 2026 | ou se loge la variance des reponses politiques d'un modele ? | 12 personas ideologiques plus une reference non pilotee, 70 items du Political Compass, 10 replicats, 7 modeles, 63 700 reponses | GPT-5, Claude, Grok, Gemini, DeepSeek, Kimi, Qwen | decomposition de variance sur les axes economique et societal | **le cadrage contextuel explique environ 88 a 93 % de la variance, l'identite du modele moins de 3 %** ; les desaccords entre audits precedents se resolvent une fois reconnu que les points de depart ne sont pas centres | resume seul ; instrument unique (Political Compass) | l'invite domine le modele : notre C2 contre C3 est donc le bon contraste, et un changement de modele est un second ordre | [PROBABLE] | aval de 05-25 |
| 05-68 | anonyme, *Progressive in Principle, Centrist in Practice : LLM Political Bias Is Instrument-Dependent*, arXiv 2606.00048, 2026 | le biais politique mesure par questionnaire predit il le vote sur des politiques concretes ? | Smartvote, 75 questions, 66 modeles, compares a 184 elus du Conseil national suisse ; puis 48 referendums federaux reels, 9 modeles, 4 langues, 3 conditions d'information | 66 modeles | correlation de rang entre modele et parti ; taux d'accord avec le resultat reel et avec les consignes de vote | sur Smartvote le gradient gauche droite se reproduit, rho moyen **-0,77** ; sur les referendums l'alignement devient centre, plus proche du Mitte et du FDP que du SP et des Verts (Wilcoxon p = 0,008) ; coherence entre langues de **50 % (Mistral) a 98 % (GPT-5.4)** ; deux modeles votent Nein sur 83 a 94 % des referendums, aussi souvent sur des propositions progressistes que conservatrices (binomial p < 0,0001), donc aversion au changement et non biais gauche droite | resume seul ; contexte suisse | confirme la lecon de 05-62 : **le QCM ne predit pas le comportement**, et notre protocole doit se garder de conclure d'un instrument a l'autre | [PROBABLE] | aval de 05-29 |
| 05-69 | anonyme, *Can LLMs Emulate Human Belief Dynamics ?*, arXiv 2605.18781, 2026 | un modele reproduit il la formation et le changement de croyances en reseau social ? | replication d'une etude etablie de dynamique de croyances | 12 modeles, plusieurs familles et plusieurs tailles | distribution initiale des croyances, conformite, homophilie | « The answer is a clear no, and in systematic ways. LLMs fail to capture initial human belief distributions and tend to be overall more conformist than humans » | resume seul | appuie l'exces de coherence deja mesure en `a9` et la densite de reseau plus elevee chez nos agents | [PROBABLE] | aval de 05-63 |
| 05-70 | Baldassarri et Goldberg, *Neither Ideologues nor Agnostics*, *American Journal of Sociology* 120(1), 2014, DOI 10.1086/676042 | comment les Americains organisent ils leurs croyances politiques ? | ANES | analyse de classes relationnelles (RCA) | detection de patrons multiples d'organisation d'opinion | trois sous populations : **ideologues** alignes, **alternatifs** moralement conservateurs et economiquement liberaux ou l'inverse, **agnostiques** aux associations faibles ; revenu, education et religiosite au coeur de la difference ; « The conflictual presence of conservative and liberal preferences has often been resolved by alternative voters in favor of the Republican Party » | resume seul, paywall, aucune version libre trouvee par Unpaywall | **le mecanisme de la variete de droite** : les contre presses se rangent a droite, donc la droite herite d'un stock de combinaisons que la gauche n'a pas | [PROBABLE] | initiale de la mission, confirmee amont de Chen 2025 et de van Noord |
| 05-71 | Boutyline et Vaisey, *Belief Network Analysis*, *American Journal of Sociology* 122(5), 2017, DOI 10.1086/691274 | quelles croyances sont centrales, et les groupes ont ils des logiques differentes ? | ANES 2000 | reseau de correlations entre items, centralite | comparaison de 44 sous populations demographiques, puis recherche inductive | l'identite politique est la croyance centrale ; et « Contra these recent accounts, the study finds that belief systems of different groups vary in the amount of organization but not in the logic that organizes them » | resume seul, paywall | **valide directement nos S3 et S4** : nous trouvons une difference de quantite (0,447 contre 0,311) et pas de logique (2 sous groupes partout) | [PROBABLE] | initiale (05-48), relue par la mission |
| 05-72 | DellaPosta, *Pluralistic Collapse*, *American Sociological Review* 85(3), 2020, DOI 10.1177/0003122420922989 | la polarisation passe t elle par l'extremisation ou par la consolidation ? | GSS, 44 ans, opinions de nombreux domaines | reseau de croyances evolutif | densite et structure de grappes du reseau | polarisation par **consolidation** : les alignements transversaux s'effondrent et les grappes deviennent plus larges et plus englobantes ; « the increasing salience of political ideology and partisanship only partly explains this trend » | resume seul, paywall | meme direction temporelle que 05-53 et 05-59, sur un jeu d'items bien plus large | [PROBABLE] | initiale (05-47), relue par la mission |

Entrees rappelees de `corpus/05` parce qu'elles portent une conclusion ici : 05-01 Converse
(contrainte elite 0,53 contre masse 0,23), 05-02 Baldassarri et Gelman (correlation inter items
0,15, plus 0,02 par decennie, contre 0,17 et plus 0,05 pour le parti), 05-03 Treier et Hillygus
(deux dimensions correlees a 0,30 ; 38 % des conservateurs contre 35 % des liberaux hors
quadrant), 05-04 Ellis et Stimson (un tiers de conservateurs symboliques operationnellement a
gauche), 05-05 Fowler et al. (72,8 % unidimensionnels, 20,7 % de positions genuines mal
resumees, 6,5 % de bruit), 05-06 Hout et Hastings (`partyid` 0,84, `polviews` 0,66), 05-14
Santurkar (convergence vers le mode liberal), 05-16 CoMPosT (personas conservatrice et liberale
au maximum d'ecart sur les sujets controverses), 05-25 Kabir (refus asymetriques sur les
instructions conservatrices), 05-29 Wang et al. (19 patrons de croyances contre 340 chez les
humains).

---

## Comment ca fonctionne

### Le fait de base n'est pas une asymetrie de temperament, c'est une asymetrie de derive

La litterature contient bien un homologue de notre 1,122, et il est plus ancien et plus large que
nous ne le pensions. Ondish et Stern mesurent sur le GSS et l'ANES, plus de 80 000 personnes,
environ 400 questions politiques et environ quarante ans, que les liberaux ont plus de consensus
que les conservateurs, et les deux plus que les moderes (05-55, [PROBABLE]). Ils ne calculent pas
un rapport de dispersion mais une part de variance attribuable aux items dans un modele
one-with-many, ce qui est une autre facon de dire la meme chose : plus les gens d'un camp
repondent pareil aux memes questions, plus la variance se loge dans l'item et non dans la
personne. Notre rapport de Gini Simpson et leur ICC mesurent le meme objet par deux chemins, et
ils donnent le meme sens.

Ce qui est nouveau, et decisif, c'est que **le mecanisme a ete formalise et simule**. Brandt et
Sleegers construisent un modele de dynamique de croyances individuelles, lui donnent deux
hypotheses tirees d'Ellis et Stimson, et retrouvent le fait sans le programmer (05-57,
[CONFIRME]). Les deux hypotheses sont : les positions de politique publique des Americains
penchent en moyenne a gauche, leurs etiquettes ideologiques penchent en moyenne a droite. Dans
leurs quarante populations simulees de 1 000 agents, les liberaux ont le plus de consensus dans
35 cas sur 40, les conservateurs dans 5, les moderes dans aucun. Leur diagnostic est explicite :
« The liberal consensus effect seems to occur because policies are pushed in a liberal/left-wing
direction by the exogenous influences for all of the simulated participants ». Autrement dit, la
gauche est unie parce que la derive agregee de l'opinion va dans son sens, et la droite est
divisee parce que la meme derive tire ses membres loin de leur etiquette.

Cette explication a une consequence testable qui est deja verifiee chez nous. Elle predit que
**l'asymetrie doit s'inverser partout ou la derive agregee va vers la droite**. C'est exactement
ce que `a30` mesure sans l'avoir cherche : rapport 0,63 sur la peine de mort, 0,65 sur la severite
des tribunaux, 0,73 sur le coup porte par un policier, 0,66 sur l'adultere, et 0,93 sur la famille
d'items de fin de vie. Sur ces questions, c'est la droite qui a un consensus acquis et la gauche
qui se divise. Notre propre tableau item par item est donc une confirmation empirique du modele
generatif de 05-57, et cette correspondance n'a ete relevee par personne.

### La centralite d'une attitude explique quelle question porte l'ecart

Le plus grand chiffre de `a30`, le 2,47 sur les sept items d'avortement, a une explication datee
et publiee. Chen et ses coauteurs suivent la centralite de force de chaque modalite de reponse a
l'interieur de chaque sous graphe partisan de 2000 a 2020, et trouvent que l'avortement passe des
attitudes les moins importantes du camp democrate du debut des annees 2000 a **l'attitude la plus
centrale de ce camp en 2020, par des marges substantielles**, alors que « Among the Republican
community, meanwhile, abortion attitudes never played a pivotal role as an ideological anchor in
any of the measured years » (05-53, [CONFIRME]). Une attitude centrale est une attitude qui
contraint les autres ; un camp dont l'ancre est l'avortement est un camp qui a tranche
l'avortement. Notre 0,160 de Gini Simpson a gauche contre 0,396 a droite est la trace, en
dispersion de reponses individuelles, de ce que Chen mesure en centralite de noeud.

Le meme papier montre le mouvement inverse : l'aide aux Noirs, longtemps centrale dans l'amas
liberal, perd presque entierement sa position. Nous avons la aussi le miroir : `nataid` est notre
item le plus favorable a la gauche, rapport 0,44. Deux mesures, deux jeux, meme carte.

### La dispersion et la contrainte ne sont pas la meme quantite, et ne se lisent pas ensemble

`a30` section 6.3 a bien vu que sur les memes dix items de Twin, le rapport de dispersion vaut
1,290 en faveur d'une droite plus variee et le rapport de densite de reseau 0,894 en faveur d'une
droite moins liee. La litterature explique pourquoi cela n'est pas contradictoire, et elle donne
la calibration. Les simulations du chapitre ResIN de 2026 montrent que **la taille d'un amas
decroit avec la correlation moyenne inter items**, fortement entre 0 et 0,4 puis a plat, et que
cette taille est « almost unchanged » quand on change le nombre d'attitudes par groupe (05-54,
[CONFIRME]). Un amas compact veut donc dire des attitudes fortement correlees, et rien d'autre.
La dispersion des reponses, elle, mesure combien de modalites differentes sont employees. Un camp
peut employer peu de modalites tout en les tenant faiblement ensemble, et l'inverse.

Le meme chapitre repond partiellement a l'hypothese de bruit d'echantillonnage que `a32` avait
formulee sans la tester : la distance normalisee entre amas « do not change for uneven group
sizes », teste a 90 % contre 10 % (05-54, [CONFIRME]). L'objection de `a32` sur les 55 republicains
de l'echantillon Prolific de Luders tombe donc pour la geometrie, mais elle n'est pas testee pour
la densite.

### La densite de sous graphe partisan : ce que le code des auteurs dit vraiment

`a32` a ecrit, et `a30` a repris en interdiction numero 8, que toute densite de sous graphe
partisan publiee sans nombre de noeuds egalise est ininterpretable, parce que le rapport passe de
0,540 a 0,894 par ce seul controle. Le depot de code des auteurs, lu integralement
(`github.com/yijingch/broken-egg-polarization`, `src/polar_measures.py`), oblige a corriger ce
diagnostic sur un point de fond. Leur `get_density_weighted` divise la somme des poids d'arete par
`count_all_possible_links`, qui compte les paires de noeuds **du sous graphe lui meme** issues
d'items differents ([CONFIRME], lecture du code). Le denominateur suit donc deja la taille du sous
graphe. Notre propre `analyses/a30_resin_twin.py` fait exactement la meme chose, ligne 118 a 129 :
moyenne des poids d'arete sur les paires de noeuds d'items differents.

La dependance residuelle au nombre de noeuds n'est donc pas un effet de denominateur. [PROBABLE]
C'est un effet de composition : les 16 modalites supplementaires du cote droit sont, dans nos
donnees, en majorite des modalites neutres et peu frequentes, huit des dix « ni l'un ni l'autre »
tombant a droite ; une modalite rare a un phi faible avec presque tout, donc elle abaisse la
moyenne. Or l'absorption des positions neutres par le camp republicain **est le phenomene** decrit
par Luders et par Chen, pas un biais qui le masque. Egaliser le nombre de noeuds ne corrige pas un
artefact, cela change de question : la densite brute repond a « le stock de positions que ce camp
detient effectivement est il serre », la densite egalisee repond a « les positions les plus
caracteristiques de ce camp, a nombre egal, sont elles serrees ». Les deux sont legitimes, aucune
ne remplace l'autre, et l'interdiction numero 8 de `a30` devrait etre reformulee en obligation de
publier les deux avec le nombre de modalites employees, ce que le script fait deja.

### La contrainte est une propriete du systeme politique, pas d'un camp

Trois resultats convergent pour dire que la contrainte n'est pas une caracteristique
psychologique. Converse mesurait 0,53 chez les candidats au Congres contre 0,23 dans le public
(05-01, [CONFIRME]). Malka montre que la correlation entre conservatisme culturel et economique
est negative en moyenne sur 99 nations et que c'est l'engagement politique qui recree l'alignement
(05-08, [CONFIRME]). Warncke ajoute le maillon manquant : sur 38 pays europeens, ce sont les
systemes a liens programmatiques entre citoyens et partis qui soutiennent des croyances de masse
« far more coherent », et un peu moins d'un tiers de cet effet passe par la centralite de
l'attachement ideologique symbolique ; « Abstract ideological summary positions are not central to
all belief systems, but where they are, mass beliefs tend to be more coherent overall » (05-65,
[CONFIRME]).

Cette derniere phrase est la meilleure description theorique de ce que fait notre condition C2.
Mettre « vous etes de gauche » dans l'invite, c'est rendre l'etiquette maximalement centrale dans
le systeme de croyances de l'agent. Warncke predit alors une coherence maximale. Nous mesurons une
coherence infinie : Gini Simpson de 0,0045 sur l'avortement et de 0,000 exactement sur les libertes
civiles et la fin de vie. La simulation a etiquette n'est pas une caricature des conservateurs ou
des liberaux, c'est **un pays imaginaire ou l'ideologie symbolique est la seule chose centrale**.

### Ce que la machine fait de la contre pression

Deux papiers, tous deux inconnus de `corpus/05`, ferment deux questions ouvertes du dossier.

Liu, Diab et Fried definissent une persona *incongrue* comme une persona a deux composantes dont
l'appartenance demographique rend la position moins probable dans les donnees Pew, par exemple un
liberal favorable a une hausse des depenses militaires (05-62, [CONFIRME]). Sur sept modeles, la
pilotabilite moyenne vers les personas politiques vaut 92,5 quand elles sont congrues et **75,9
quand elles sont incongrues**, soit 16,6 points perdus, contre 7,9 sur la race et 4,7 sur le genre.
L'ecart moyen sur les trois domaines vaut 9,7 %. Quand le modele echoue, il produit « the
stereotypical stance associated with its demographic rather than the target stance ». C'est
exactement le mecanisme de substitution que `a31` mesure chez nous sous le nom de faussse rarete
typique du segment, et c'est la premiere mesure publiee de la contre pression cote machine.

Deux details du meme papier valent pour tout notre protocole. D'abord, R2 = 0,018 entre le taux de
reponse a un QCM et la pilotabilite en generation ouverte, et le modele n'est plus pilotable vers
la position choisie en QCM que 51,5 % du temps : **l'audit par questionnaire ne predit pas le
comportement en generation**. Ensuite, les modeles ajustes par RLHF sont plus pilotables, en
particulier vers les positions associees aux liberaux et aux femmes, mais « significantly decrease
the range of views and topics expressed » : plus de pilotabilite, moins de diversite.

Chuang et ses coauteurs repondent a l'autre question, celle de A12 et de la question 5 de
`corpus/05` : faut il conditionner sur des valeurs plutot que sur une etiquette (05-63,
[CONFIRME]). Leur reponse est oui, mais pas la ou nous en avons besoin. Semer une croyance
appartenant au meme facteur du reseau humain fait passer l'erreur absolue moyenne de 1,70 a 1,34
chez ChatGPT, un gain relatif de 22,54 %, alors que la demographie seule ne fait rien du tout
(1,70 contre 1,68 sans demographie) et qu'une croyance d'un autre facteur ne fait rien non plus
(1,67). Mais le gain relatif vaut 60,83 % sur les croyances aux fantomes et **6,19 % sur le
facteur partisan**, 3,39 % pour GPT-4o mini, 2,94 % pour Mistral. Le modele possede deja l'axe
partisan ; lui donner une croyance politique de plus ne lui apprend presque rien. Le
conditionnement par croyance est donc une bonne idee hors du politique, et une fausse piste sur
l'axe qui nous interesse.

Un dernier resultat cadre le tout : sur 63 700 reponses, 7 modeles et 70 items, le cadrage
contextuel explique 88 a 93 % de la variance des positions politiques et l'identite du modele
moins de 3 % (05-67, [PROBABLE]). Notre contraste C2 contre C3 est donc le bon endroit ou
chercher, et la question C d'`ARBITRAGE.md`, « attendre un modele plus gros », est un second ordre.

---

## Ce qui se contredit, et la variable qui explique

**1. Ondish et Stern contre Hanel, Zarzeczna et Haddock.** Les premiers trouvent les moderes les
moins consensuels des trois groupes (05-55, [PROBABLE]) ; les seconds trouvent que les extremes,
de gauche comme de droite, sont **plus** heterogenes que les moderes (05-60, [PROBABLE]). La
variable est le domaine de mesure : Ondish et Stern mesurent des positions de politique publique
americaines, Hanel mesure des valeurs de Schwartz europeennes. Nous avons le controle interne qui
tranche : sur Twin, le rapport droite sur gauche vaut 1,290 sur les dix items d'attitudes
politiques et **0,988 sur les 275 items de personnalite**, intervalle excluant 1 du mauvais cote
(`a30`). Hors du politique, l'asymetrie disparait ou s'inverse. Les deux litteratures ne parlent
pas du meme objet.

**2. Luders 2024 contre Chen 2025, dans la meme equipe.** La figure 2 de Luders montre un amas
democrate compact et un amas republicain etale ; la serie de Chen montre le sous graphe
republicain **plus** dense que le democrate de 2000 a 2016, avec une inversion en 2020. Deux
variables expliquent l'ecart, et elles se renforcent. La premiere est l'annee : Luders replique
sur l'ANES **2020** et collecte son echantillon Prolific en 2021-2022, c'est a dire apres le
croisement. La seconde est le jeu d'items : Chen prend cinq items dont quatre sont economiques ou
raciaux a sept modalites, Luders prend huit items dont cinq sont moraux ou culturels. Le domaine
et l'annee ne sont pas independants, puisque Chen montre que c'est precisement l'avortement qui
devient l'ancre du camp democrate sur cette periode.

**3. La these d'« Asymmetric politics » contre la mesure sur reponses individuelles.**
Grossmann et Hopkins soutiennent que le parti republicain est l'agent d'un mouvement ideologique
dont les partisans « prize doctrinal purity » alors que le parti democrate est une coalition de
groupes sociaux (05-61, [PROBABLE]). Cela predit des republicains plus homogenes que les
democrates, l'inverse de notre 1,122 et de tout le bloc Ondish, Brandt, Cely. La contradiction est
apparente et sa resolution est dans le texte meme de Grossmann et Hopkins : « American public
opinion (...) favors left-of-center positions on most specific policy issues yet simultaneously
shares the general conservative preference for smaller and less active government ». La purete
doctrinale republicaine porte sur **l'etiquette et le principe general**, pas sur les positions
d'items ; et c'est justement ce decalage qui, dans le modele generatif de Brandt et Sleegers,
produit une droite dispersee sur les items. Les deux enonces sont vrais a des niveaux differents,
et notre propre mesure le confirme mecaniquement : le rapport vaut 1,122 quand on segmente par
`polviews`, l'etiquette symbolique, et **1,094 quand on segmente par `partyid`**, l'appartenance
partisane. L'ecart est plus grand sur l'etiquette que sur le parti, ce qui est le sens attendu si
l'asymetrie est symbolique et non organisationnelle.

**4. Boutyline et Vaisey contre van Noord et al.** Les premiers concluent que les systemes de
croyances des groupes « vary in the amount of organization but not in the logic that organizes
them » (05-71, [PROBABLE]) ; les seconds trouvent en Europe deux logiques distinctes, avec des
correlations culturel x economique de signes opposes, et notent « Unexpectedly, the groups did not
differ in the strength of association between beliefs » (05-64, [CONFIRME]). C'est exactement le
contraire, terme a terme. La variable est le pays et la methode : ANES 2000 et centralite de
reseau pour les uns, 23 pays europeens et analyse de classes correlationnelles pour les autres.
Nos propres resultats se rangent du cote de Boutyline et Vaisey : S4 trouve une difference de
quantite (0,447 a gauche contre 0,311 a droite) et S3 ne trouve aucune difference de logique
(deux sous groupes dans les trois camps, 100 tirages sur 100). Cela est attendu, puisque nos
donnees sont americaines.

**5. Brandt et al. contre eux memes, entre deux enquetes europeennes.** L'ESS replique nettement
l'effet de consensus de gauche, l'Eurobarometre ne le replique pas et n'y arrive jamais
significativement (05-56, [CONFIRME]). Les auteurs excluent la composition des pays par un test
direct et retiennent la variable des items : l'Eurobarometre porte surtout sur l'integration
europeenne. C'est la meme variable que le point 1, et elle a une consequence directe pour nous :
notre 1,122 est un chiffre **de batterie**, pas un chiffre de population, et il n'a de sens qu'a
cote de la composition en domaines des 149 items.

---

## Ce que ca permet de tester chez nous tout de suite

**T1. Refaire le rapport droite sur gauche en separant les items par le sens de la derive
agregee.** Le modele de Brandt et Sleegers predit que l'asymetrie suit la direction dans laquelle
l'opinion moyenne a bouge. Nous avons deja la vague 1 et la vague 2 sur les memes personnes, mais
pas de serie longue. Substitut : classer les 149 items du GSS selon que la reponse majoritaire est
la reponse de gauche ou la reponse de droite, puis recalculer le rapport dans chaque classe.
Prediction : rapport nettement superieur a 1 dans la premiere classe, inferieur ou egal a 1 dans
la seconde. **Cout : une passe sur `a30-gss-par-item.csv` et le classement deja ecrit dans
`a30-gss-classement-items.csv`, aucune donnee nouvelle, moins d'une heure, zero appel de modele.**
C'est le test le plus rentable de la liste : il transforme notre tableau item par item en test
d'une hypothese generative publiee.

**T2. Publier la densite de sous graphe dans les deux variantes, avec le nombre de modalites.**
La lecture du code de Chen montre que le denominateur suit deja la taille du sous graphe, donc la
variante brute n'est pas fausse, elle repond a une autre question. `a30_resin_twin.py` calcule deja
les trois partages. **Cout : reecrire la section 6.2 et l'interdiction numero 8 de `a30`, aucun
calcul nouveau, une heure.**

**T3. La centralite de l'avortement chez les agents.** Chen fournit la statistique et la cible :
dans le camp democrate humain de 2020, l'avortement est l'attitude la plus centrale ; dans le camp
republicain il ne l'a jamais ete. Calculer la centralite de force par camp sur nos humains puis
sur chaque condition d'agents, et regarder si les agents reproduisent la hierarchie ou s'ils
donnent la meme centralite aux deux camps. Prediction, en prolongement de `a31` : les agents a
etiquette rendent l'avortement central **dans les deux camps**, parce qu'il est le marqueur le
plus lisible de l'etiquette. **Cout : une fonction de centralite ajoutee au module ResIN existant,
une demi journee, zero appel de modele.** C'est le test qui manque pour passer d'un chiffre de
dispersion a un mecanisme.

**T4. Persona incongrue, version popsim.** Liu, Diab et Fried mesurent une perte de 16,6 points de
pilotabilite sur les personas politiques incongrues. Notre equivalent existe deja dans les
donnees : les contre presses du GSS, gens de gauche conservateurs sur le social ou l'inverse, que
`a30` sait identifier par les scores economique et social. Mesurer l'exactitude des agents sur les
contre presses contre les congruents, a l'interieur de chaque camp. Prediction : la perte est plus
forte en C2 qu'en C3. **Cout : un decoupage des matrices de `a28` par quadrant, une demi journee,
zero appel de modele nouveau.**

**T5. Semer une croyance plutot qu'une etiquette, mais hors du politique.** Chuang montre un gain
de 22,5 % en general et de 6,2 % sur le facteur partisan. Le test utile chez nous n'est donc pas
« conditionner sur une valeur fondamentale ameliore t il l'axe ideologique » (la reponse publiee
est presque non), c'est « le gain de conditionnement par croyance est il nul sur les items
politiques et positif sur les 35 items hors axe du GSS ». Si oui, nous aurons montre que l'axe
ideologique est deja sature dans le modele, ce qui est notre these. **Cout : une nuit de calcul
sur les 150 personnes, une condition d'invite nouvelle, plus le temps de redaction.**

**T6. Compter les modalites neutres par camp chez les agents.** Luders et Chen constatent que les
positions neutres sont absorbees du cote republicain ; `a30` le chiffre a huit sur dix. Prediction
de `a32` section 6, non encore testee : un agent a etiquette place les neutres au milieu,
symetriquement. **Cout : une lecture de `a30-resin-twin-noeuds.csv` etendue aux fichiers d'agents,
deux heures.**

---

## Ce que personne n'a fait

1. **Personne n'a publie un rapport de dispersion intra camp sur reponses individuelles
categorielles, avec intervalle de bootstrap et appariement demographique exact.** Ondish et Stern
publient un ICC de modele multiniveau ; Cely publie une mesure d'alignement de reseau ; Hanel
publie des ecarts types de valeurs ; Chen publie une densite de graphe. Aucun ne publie la
quantite de `a30`, ni ne la normalise par un plancher de reinterrogation des memes personnes.
C'est toujours notre atout non copie, et il est maintenant precisement situe.

2. **Personne n'a mesure la fidelite test retest de la forme d'un reseau d'attitudes.** Aucun des
quatre papiers ResIN ne le fait, et les auteurs de 05-53 listent l'absence de validation
comparative dans leurs limites. `a30` l'a fait sur Twin, plancher de bruit 0,04 sur le rapport de
densite. Ce chiffre n'a d'equivalent nulle part.

3. **Personne n'a decompose le rapport de dispersion entre effet de position et effet de
dispersion.** La limite 9 de `a30` reste entiere apres cette lecture : quand la gauche est a 0,160
de Gini Simpson sur l'avortement, une partie de l'ecart est un plafond de consensus. Chen fournit
l'instrument qui pourrait le trancher, la centralite de noeud, qui ne depend pas du niveau de la
reponse.

4. **Personne n'a croise l'asymetrie de refus (05-25) avec l'asymetrie de variance.** Toujours
vrai apres la lecture complete, et 05-62 ajoute un motif : les modeles RLHF sont plus pilotables
vers les positions liberales, ce qui pourrait produire mecaniquement un camp de gauche plus
homogene en sortie.

5. **Personne n'a applique le modele generatif de Brandt et Sleegers a une population simulee par
modele de langage.** Leur modele produit l'effet de consensus liberal a partir de deux parametres
de derive ; nos agents produisent une version exageree du meme effet. Ajuster leurs deux
parametres sur nos sorties d'agents dirait de combien la simulation deplace la derive supposee.
Personne n'a fait ce pont entre la modelisation a base d'agents de psychologie sociale et les
agents de langage.

6. **Personne n'a mesure la variance intra camp d'une population simulee comme determinant de la
polarisation percue.** 05-66 etablit que la variance intra groupe regle la perception de la
polarisation. Une societe simulee dont le camp de gauche est litteralement unanime est une societe
qui, lue par ses propres membres simules, percevrait une polarisation maximale. C'est une
consequence de nos chiffres que personne n'a tiree.

7. **Personne n'a repris la controverse Converse contre Achen du cote machine.** Inchange.

---

## Ce que je n'ai pas pu verifier

1. **Ondish et Stern 2018 n'a pas ete lu.** SAGE renvoie un 403, Unpaywall ne connait aucune
version libre, Semantic Scholar declare le texte ferme. Tout ce qui en est rapporte ici vient de
deux descriptions independantes et detaillees par Brandt et ses coauteurs (05-56 et 05-57), qui
concordent sur les donnees, la taille, la methode et le sens. **Les tailles d'effet d'Ondish et
Stern ne doivent pas etre citees.** C'est la lacune la plus genante du present etat des lieux,
puisqu'il s'agit de l'homologue direct de notre chiffre central.

2. **Cely 2025 n'a ete lu qu'en resume.** Le PDF Wiley est bloque, le depot d'Aarhus ne sert que
la notice, celui de Masaryk ne repond pas. Le resume est cite mot pour mot et il est riche, mais
aucune valeur numerique n'en est reprise. C'est le second homologue direct, et il reste a lire.

3. **Les valeurs numeriques des densites par camp et par annee de 05-53 restent inaccessibles.**
Elles sont dans la figure 7 que `pdftotext` ne rend pas. Le depot de code existe
(`github.com/yijingch/broken-egg-polarization`) mais les produire demanderait d'executer une
analyse, ce que la mission interdit. Le sens de l'ecart et l'annee de l'inversion sont [CONFIRME]
par le texte, les six couples de valeurs ne le sont pas.

4. **L'interpretation de la dependance residuelle de la densite au nombre de noeuds est de moi.**
La lecture du code de Chen et celle de `a30_resin_twin.py` sont [CONFIRME] : les deux normalisent
par les paires du sous graphe. L'explication par la composition en modalites rares est [PROBABLE]
et n'a ete testee par personne. Le test existe : recalculer les densites en retirant les modalites
sous un seuil de frequence, dans les deux camps.

5. **Hanel et al. 2019, Grossmann et Hopkins 2015 et 2016, Baldassarri et Goldberg 2014,
Boutyline et Vaisey 2017, DellaPosta 2020 n'ont ete lus qu'en resume.** Tous sous paywall, aucune
version libre trouvee. Les citations exactes rapportees ici viennent des resumes indexes par
OpenAlex, qui sont les resumes d'auteur.

6. **Kozlowski et Murphy a ete lu dans sa version preprint SocArXiv de 2019**, pas dans la version
publiee de 2021 dans *Social Science Research*. La citation sur la divergence democrates
republicains apres 2004 vient du preprint. Il faut verifier qu'elle survit a la revue.

7. **Le budget de recherche web etait deja epuise a l'ouverture de la seance** (200 requetes sur
200 consommees plus tot dans la journee). Toute la collecte s'est faite par OpenAlex, Semantic
Scholar, Crossref, Unpaywall, Europe PMC, arXiv, OSF et les depots institutionnels. OpenAlex a
par ailleurs limite le debit de sa recherche plein texte pendant une partie de la seance, ce qui a
oblige a passer par la traversee de citations plutot que par la recherche par mots cles. Des
travaux tres recents hors de ces index ont donc pu etre manques.

8. **Les chiffres allemands de 05-66 n'ont pas ete extraits**, ils sont dans les figures. Seul le
cadre theorique est [CONFIRME].

9. **Trois entrees informatiques de 2026 (05-67, 05-68, 05-69) sont anonymes dans les metadonnees
arXiv consultees** et n'ont ete lues qu'en resume. Elles ne portent ici aucune conclusion seule.

---

## Ce que cela change au dossier

**Sur `ARBITRAGE.md`.** La reformulation proposee par `a30` section 10 tient, mais elle est
incomplete sur un point : elle dit que la litterature ne mesure la variete des camps que sur des
scores agreges. C'est vrai de la mesure, ce n'est pas vrai du fait. Le fait a un nom publie,
*liberal consensus effect*, une mesure sur 80 000 personnes et 40 ans, une replication europeenne
partielle et un modele generatif qui le reproduit. **Nous ne decouvrons pas le fait, nous le
mesurons autrement et nous le montrons exagere par la simulation.** La phrase a defendre devient
plus forte et non plus faible : « l'effet de consensus liberal est etabli chez les humains depuis
2018 et explique par la derive de l'opinion ; une population simulee a partir d'etiquettes ne le
reproduit pas, elle le pousse jusqu'a l'unanimite ».

**Sur la datation.** Trois series independantes disent que l'asymetrie a change de signe entre
2016 et 2020 : la densite de sous graphe partisan de Chen, l'alignement d'enjeux par parti de
Kozlowski et Murphy, et la centralite de l'avortement dans le camp democrate. Nos donnees sont de
2024 des deux cotes, archive de Stanford et Twin-2K-500. **Notre 1,122 est un chiffre d'apres le
croisement, et il doit etre presente comme tel**, faute de quoi un relecteur de science politique
le refusera comme une generalisation abusive.

**Sur les questions ouvertes pour Simon (`a30` section 12).** La question 1 a une reponse :
l'enonce defendable en science politique est « effet de consensus liberal », et la mesure standard
qui separe « moins de variete » de « a deja tranche » est la centralite de noeud dans un reseau de
croyances, pas une dispersion. La question 4 a une reponse partielle : Chen et Luders ne
contredisent pas notre mesure sur Twin, ils mesurent une autre annee et une autre batterie. La
question 2, le cone monotone a gauche et plat a droite sur les sept points de `polviews`, n'a
d'equivalent nulle part dans ce que j'ai lu : Ondish et Stern travaillent en trois groupes, Hanel
en trois groupes, Cely en deux camps. **Le gradient en sept points reste l'objet le plus original
du dossier.**
