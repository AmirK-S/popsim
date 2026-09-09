# 05. Structure des attitudes, heterogeneite ideologique, asymetries, incoherence

Cartographie du 8 septembre 2026. Grille commune : `corpus/00-GRILLE.md`. Direction de these :
« Ce que la simulation efface ». Ce theme fournit le referent humain : ce qu'une simulation
*devrait* reproduire de la structure interne des attitudes, et donc l'endroit exact ou une
caricature se voit.

Il est le complement direct de trois resultats internes. `resultats/a1-double-distorsion.md`
section 4 montre que le gonflement inter groupes est porte presque entierement par l'axe
ideologique, facteur 2,1 a 2,7 pour les conditions riches et 8,51 pour `gss_v8`, alors que le
genre reste entre 0,80 et 1,36. `resultats/a9-deviance-et-incoherence.md` montre que la
demographie ne dit presque rien de qui devie, et que l'exces de coherence des agents n'est ni
uniforme ni toujours positif. `BRAINSTORM.md` A10 a A12 demande si le trait de deviance est un
construit connu, s'il existe une litterature sur la structure de l'incoherence attitudinale, et
si le conditionnement par trait latent contourne l'essentialisme identitaire. Les trois
questions ont des reponses dans la litterature, et elles ne sont pas celles qu'on esperait.

Periode : classiques sans limite, plus 2015 a 2026 pour le reste, plus 2023 a 2026 pour le
volet modeles de langage.

Certitude : [CONFIRME] texte lu, [PROBABLE] resume ou source secondaire, [NON LU] titre seul.
Les entrees [PROBABLE] et [NON LU] sont declarees comme telles et jamais utilisees pour porter
un chiffre dans la synthese.

---

## La table

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | certitude |
|---|---|---|---|---|---|---|---|---|---|
| 05-01 | Converse, *The Nature of Belief Systems in Mass Publics*, 1964, reimpression *Critical Review* 18(1-3), 2006, 1-74, DOI 10.1080/08913810608443650 | le public a t il des systemes de croyances contraints, et ses reponses sont elles des attitudes ? | ANES panel 1956-1958-1960 ; 1958 : candidats au Congres contre echantillon national | aucun, tabulations et modele noir et blanc | tau-gamma entre items ; modele a deux populations, stable et aleatoire | contrainte moyenne, elite : 0,53 intra domestique, 0,25 domestique-etranger, 0,37 intra etranger, 0,39 enjeux-parti ; masse : 0,23, 0,11, 0,23, 0,11. Niveaux de conceptualisation : ideologues 2,5 %, quasi ideologues 9 %, interet de groupe 42 %, air du temps 24 %, sans contenu 22,5 %. Modele noir et blanc sur l'item entreprise privee contre etat : correlation de retournement 1956-1958 de 0,24, bifurcation predite 0,00 et 0,47, observee 0,004 et 0,49 ; les autres items bifurquent 0,07 et 0,35 | mesures de 1958-1960, une seule societe, tau-gamma sensible au format ; le modele noir et blanc est refute pour tous les items sauf un | soutient. La reference de base : la contrainte est faible et l'ecart elite / masse est un facteur 2 a 2,5. Une simulation qui produit des correlations inter items de niveau elite reproduit un public qui n'existe pas | [CONFIRME] |
| 05-02 | Baldassarri et Gelman, *Partisans without Constraint*, *American Journal of Sociology* 114(2), 2008, 408-446 | la polarisation americaine est elle un alignement des opinions ou un tri partisan ? | NES cumule, 47 items poses au moins trois fois, periode 1972-2004, 4 domaines | modeles multiniveaux a pente aleatoire sur les correlations | correlation item / parti (partisanship) contre correlation item / item (alignment) | partisanship : moyenne 0,17 (ecart type inter items 0,08), croissance +0,05 par decennie (SE 0,01), 95 % des pentes entre -0,01 et +0,11 ; avec l'ideologie declaree moyenne 0,22 et +0,04 par decennie. Alignment : 1 081 paires possibles, correlation moyenne de paire 0,15 (ecart type 0,11), croissance +0,02 par decennie, 95 % des paires entre -0,02 et +0,06 | correlations de Pearson sur items ordinaux courts, pas de correction pour erreur de mesure ; l'agregation par domaine augmente la contrainte, les auteurs le disent en note 13 | soutient fortement. Chez les humains l'etiquette partisane est de plus en plus predictive **sans** que les opinions se soient alignees entre elles. Un agent qui derive tout d'une etiquette produit exactement la structure que les humains n'ont pas | [CONFIRME] |
| 05-03 | Treier et Hillygus, *The Nature of Political Ideology in the Contemporary Electorate*, *Public Opinion Quarterly* 73(4), 2009, 679-703 | une dimension suffit elle a resumer les preferences politiques du public ? | ANES 2000, 23 items de politique publique | theorie de reponse a l'item ordinale bayesienne, 1D contre 2D | DIC ; parametres de discrimination ; classement en quadrants economique x social | le modele 2D bat le 1D au DIC ; correlation entre dimension economique et sociale 0,30 ; le score 1D correle 0,962 avec l'economique et 0,580 avec le social. 44 % des moderes declares et 47 % des « ne sait pas » sont dans les quadrants contre pression ; seulement 17 % des moderes declares sont centristes sur les deux dimensions (tercile median), 35 % avec le seuil 25e-75e percentile. Asymetrie : 38 % des conservateurs declares sont hors de leur quadrant contre 35 % des liberaux ; moins de 9 % sont totalement mal classes | 2000 seulement, avant la polarisation recente ; 23 items, taux de non reponse jusqu'a 14 % par item, 42 % de repondants complets | soutient. Deux dimensions au minimum, correlees a 0,30 seulement. Une simulation qui place chaque persona sur un seul axe gauche droite efface la moitie du plan, et l'efface justement la ou vivent les moderes | [CONFIRME] |
| 05-04 | Ellis et Stimson, *Symbolic ideology in the American electorate*, *Electoral Studies* 28, 2009, 388-402 (volet article de *Ideology in America*, 2012) | pourquoi les Americains sont ils conservateurs symboliquement et liberaux operationnellement ? | series de sondages 1937-2008, questions d'auto identification ideologique | modeles de series temporelles agregees | part se declarant liberale parmi ceux qui choisissent une etiquette | « autant qu'un tiers de l'electorat, selon les mesures employees » tient des vues conflictuelles operationnel liberal / symbolique conservateur ; l'identification liberale passe d'environ 44 % a environ 35 % de ceux qui choisissent une etiquette ; sur 70 sondages d'avant 1970, 18 donnent une majorite liberale (maximum NORC 1944, 57 %) et 52 une minorite ; moyenne simple d'avant 1966 : 46,8 % | ce papier porte sur l'agregat, le chiffre du tiers est renvoye au livre ; pas de mesure individuelle du conflit ici | soutient. L'etiquette ideologique et le contenu des opinions sont deux choses differentes chez environ un tiers des gens. Un agent qui recopie l'etiquette recopie precisement la variable qui *ne* predit pas les opinions de ce tiers | [CONFIRME] |
| 05-05 | Fowler, Hill, Lewis, Tausanovitch, Vavreck et Warshaw, *Moderates*, *American Political Science Review* 117(2), 2023, 643-660 | les moderes sont ils centristes, inattentifs, ou incoherents ? | CCES 2010 a 2018, N pondere 285 485 | modele de melange a trois types : Downsien, Conversien, inattentif | probabilite posterieure d'appartenance a chaque type | 72,8 % Downsiens (bien resumes par une dimension), 20,7 % Conversiens (positions genuines mal resumees par un axe), 6,5 % inattentifs. Classement net : 48 % des repondants ont une probabilite superieure a 0,99, 66 % superieure a 0,95, 74 % superieure a 0,9. Dans le module 2010 a 133 questions, moins de 1 % d'inattentifs. « Extreme » defini comme une position prise par moins de 35 % des repondants | le modele suppose une echelle de Guttman pour les Downsiens ; la part d'inattentifs depend du nombre de questions, ce que les auteurs signalent | soutient et cadre le chiffrage. **Un cinquieme des gens sont genuinement incoherents et seulement 6,5 % sont du bruit.** C'est la separation exacte que `a9` cherchait entre deviance structuree et instabilite. Une simulation qui ne produit que des Downsiens rate 27 % de la population | [CONFIRME] |
| 05-06 | Hout et Hastings, *Reliability of the Core Items in the General Social Survey*, *Sociological Science* 3, 2016, DOI 10.15195/v3.a43 | quelle est la fiabilite test retest des items du GSS ? | panels a trois vagues du GSS, 2006-2014 | modeles standards et multiniveaux de fiabilite | coefficient de fiabilite par item | 62 items (21 %) au dessus de 0,85 ; 71 items (24 %) entre 0,70 et 0,85 ; 15 items sous 0,40. `partyid` 0,84, aussi fiable que la plupart des faits ; `polviews` 0,66, « substantiellement moins fiable » que le parti ; items de depense entre 0,4 et 0,8 ; `helpnot` le moins fiable des items politiques | le papier donne 283, 293 et 276 items du noyau selon les passages, incoherence interne a signaler ; contexte 2006-2014 marque par la recession et l'election d'Obama, ce qui peut se lire comme de l'infidelite | soutient l'outillage. **Le plancher de bruit par item existe deja, publie, pour le GSS.** Il donne le denominateur item par item que `a0` calcule seulement au niveau de la personne, et il dit lesquels des 149 items du run supportent une mesure de structure | [CONFIRME] |
| 05-07 | Jefferson, *The Politics of Respectability and Black Americans' Punitive Attitudes*, *American Political Science Review*, 2023, DOI 10.1017/S0003055422001289 | qu'est ce qui explique l'heterogeneite des attitudes punitives a l'interieur du groupe noir americain ? | panel Qualtrics 2019 et TurkPrime, dont un echantillon de 500 Noirs americains | OLS multivarie, coefficients standardises | echelle de politique de la respectabilite ; soutien a des politiques punitives ciblant le groupe | 34 % des repondants noirs s'opposent aux arretes municipaux sur le port du pantalon taille basse, soit environ deux tiers de soutien ; l'echelle de respectabilite predit fortement les attitudes punitives, effet d'environ 24 points de pourcentage sur un scenario ; la respectabilite est liee a d'autres croyances mais pas au parti | echantillons non probabilistes, une seule periode ; l'echelle est construite pour l'occasion | soutient. **La variance interne d'un groupe minoritaire est portee par une dimension latente que ni la race ni le parti ne captent.** Un agent conditionne sur « noir, democrate » ecrase precisement cette dimension, et le fait dans le sens de la caricature militante | [CONFIRME] |
| 05-08 | Malka, Lelkes et Soto, *Are Cultural and Economic Conservatism Positively Correlated ?*, *British Journal of Political Science* 49(3), 2019, 1045-1069 | le conservatisme culturel et le conservatisme economique vont ils ensemble ? | World Values Survey et European Values Study, 99 nations, 229 echantillons nation-annee, 1989-2014, N 325 802 | correlations intra nation, puis modeles multiniveaux | correlation intra nation pour 6 paires culture x economie | les six correlations moyennes intra nation sont **petites et negatives** : -0,027, -0,023, -0,046, -0,058, -0,013, -0,023. Part de nations a correlation significativement positive : 7,4 % a 20,8 % ; significativement negative : 34,0 % a 58,0 %. L'engagement politique est un moderateur positif dans quatre paires sur six ; les pays post communistes montrent l'organisation « protection contre liberte » la plus forte (51,9 % a 84,0 % de negatives) | items WVS courts et peu nombreux par dimension ; « conservatisme economique » operationnalise par deux items seulement | soutient. **L'axe unique gauche droite est une propriete des elites de quelques democraties riches, pas une propriete de l'espece.** Un modele qui suppose partout le paquet « droite culturelle plus droite economique » se trompe de signe dans un tiers a la moitie des pays | [CONFIRME] |
| 05-09 | Costello, Bowes et al., *Clarifying the Structure and Nature of Left-Wing Authoritarianism*, *Journal of Personality and Social Psychology* 122(1), 2022, 135-170 | l'autoritarisme de gauche existe t il, et quelle est sa structure ? | six echantillons, N total 7 258, plus de 60 criteres externes | analyses factorielles exploratoires, CFA et ESEM | structure factorielle de l'indice LWA ; correlations avec criteres externes | structure retenue : **trois facteurs correles**, agression anti hierarchique, anti conventionnalisme, censure descendante. Correlations du score total avec l'ideologie de gauche : symbolique 0,46 a 0,57, sociale 0,33 a 0,42, economique 0,46 a 0,60. Par facteur, avec l'economique et le social : agression anti hierarchique 0,41-0,48 et 0,30-0,36 ; anti conventionnalisme 0,55-0,60 et 0,50-0,59 ; censure descendante 0,26-0,32 et 0,12-0,23. Relativement au RWA, le LWA est **plus bas** en dogmatisme et rigidite cognitive, **plus haut** en emotionnalite negative | echantillons en ligne americains ; construction iterative de l'echelle sur les memes donnees qui servent a la valider, les auteurs le reconnaissent | soutient et contredit partiellement la these de l'asymetrie. **La gauche a une structure autoritaire a trois facteurs, et ces facteurs ne se projettent pas de la meme facon sur l'economique et le social.** Le sous groupe « gauche autoritaire » est invisible pour un modele a un axe | [CONFIRME] |
| 05-10 | Ditto, Liu, Clark, Wojcik, Chen, Grady, Celniker et Zinger, *At Least Bias Is Bipartisan*, *Perspectives on Psychological Science* 14(2), 2019, 273-291 (version preprint lue) | le biais partisan est il plus fort a droite qu'a gauche ? | meta analyse de 51 tests experimentaux tires de 38 articles, N 18 815 | meta analyse a effets aleatoires | r du biais partisan, separement pour liberaux et conservateurs | biais global r = 0,245 ; liberaux r = 0,235, conservateurs r = 0,255 ; difference r = 0,009, non significative. Pas de biais de publication detecte, pente du funnel non significative pour la difference | la version publiee circule avec 0,254 / 0,248 / 0,247, tres proche mais non identique ; le choix des etudes a ete conteste par Baron et Jost ; le biais partisan n'est qu'un des construits de la these de l'asymetrie | contredit la these de l'asymetrie sur ce construit precis. Consequence pour nous : **on ne peut pas justifier a priori que le camp conservateur simule doive etre plus rigide ou plus homogene que le camp liberal.** Toute asymetrie qu'on mesurera chez les agents demandera une preuve interne | [CONFIRME] |
| 05-11 | Conway, Zubrod, Chan, McFarland et Van de Vliert, *Is the myth of left-wing authoritarianism itself a myth ?*, *Frontiers in Psychology* 13, 2023, 1041391 | l'autoritarisme de gauche est il un mythe ? | 12 etudes, plus de 8 000 participants americains, plus de 66 000 participants dans le monde via le WVS | correlations, comparaisons intra ideologie | scores LWA, sensibilite a la menace, rigidite cognitive, prejuge | le LWA est lie a la sensibilite a la menace (menaces ecologiques, COVID, monde dangereux, menace Trump), au soutien a des normes restrictives de correction politique, a des evaluations plus negatives des Afro Americains et des Juifs, et a plus de rigidite cognitive. Les effets tiennent en controlant l'ideologie et **en ne regardant que les liberaux**, et sont d'ampleur comparable aux effets RWA correspondants | les auteurs sont partie prenante du debat ; mesures auto declarees ; l'etude 1 mesure des perceptions et non des personnes | contredit la these de l'asymetrie forte. Utile pour nous : **il existe un sous groupe autoritaire a l'interieur du camp de gauche, detectable en controlant l'ideologie.** Un agent « liberal » qui est uniformement tolerant efface un sous groupe reel | [CONFIRME] |
| 05-12 | Osborne, Costello, Duckitt et Sibley, *The psychological causes and societal consequences of authoritarianism*, *Nature Reviews Psychology* 2, 2023, 220-232, PMC9983523 | quel est l'etat de la question sur l'autoritarisme, y compris a gauche ? | revue de litterature, meta analyses citees | modele motivationnel a double processus | correlations meta analytiques | vision du monde dangereux : r = 0,37 avec le RWA et 0,08 avec la SDO ; vision competitive : r = 0,55 avec la SDO et 0,11 avec le RWA (meta analyse de 46 etudes, environ 13 000 participants). RWA et agression : r = 0,31. Etudes de jumeaux : jusqu'a 50 % de variance genetique du RWA. Le lien ideologie de gauche / autoritarisme apparait « regulierement » dans les pays a passe communiste. RWA positivement lie au besoin d'ordre, negativement a l'ouverture et a la confiance dans la science ; LWA positivement lie au besoin de chaos et a la confiance dans la science, negativement a la confiance institutionnelle | revue, pas de donnees nouvelles ; litterature majoritairement WEIRD, les auteurs le disent | soutient la lecture « depend de la mesure ». **Deux axes autoritaires existent, avec des correlats de signes opposes sur des variables identiques.** Une simulation qui projette « autoritaire » sur « conservateur » perd le signe sur la moitie des variables | [CONFIRME] |
| 05-13 | Argyle, Busby, Fulda, Gubler, Rytting et Wingate, *Out of One, Many*, *Political Analysis* 31(3), 2023, 337-351, arXiv 2209.06899 | un modele de langage conditionne sur des personnes reelles reproduit il les structures d'association humaines ? | ANES 2012 et 2016, plus une enquete Lucid | GPT-3 | V de Cramer entre paires d'items, humains contre silicium ; quatre criteres de fidelite algorithmique | etude 3 : conditionnement sur onze reponses ANES 2016 et prediction de la douzieme ; **difference moyenne des V de Cramer entre humains et GPT-3 : -0,026**, et le motif suit les associations fortes et faibles du cote humain | pas d'evaluation au niveau individuel, les auteurs le disent explicitement ; GPT-3 ; conditionnement sur onze vraies reponses, donc regime tres favorable | contredit partiellement, et c'est la piece adverse la plus serieuse du theme. **Avec une dizaine de vraies reponses en contexte, la structure d'association inter items est bien reproduite.** L'ecrasement de structure qu'on mesure doit donc etre attribue au regime demographique, pas au modele en general | [CONFIRME] |
| 05-14 | Santurkar, Durmus, Ladhak, Lee, Liang et Hashimoto, *Whose Opinions Do Language Models Reflect ?*, ICML, PMLR 202, 2023, arXiv 2303.17548 | de quels groupes les opinions des modeles sont elles proches ? | OpinionQA : 1 498 questions issues de 15 vagues Pew ATP, 60 groupes demographiques | 9 modeles, dont bases et ajustes par retour humain | representativite (1 moins distance de Wasserstein normalisee), orientabilite, coherence | **chacun des 60 groupes humains est plus representatif de la population generale que n'importe quel modele teste** ; les modeles ajustes par retour humain sont pires que les modeles bruts ; `text-davinci-003` assigne plus de 0,99 de probabilite a une option sur la plupart des questions et converge vers les vues **modales** des liberaux et des moderes, au point d'« incarner presque des caricatures » de ces groupes, par exemple 99 % d'approbation de Joe Biden ; taux de refus de 1 a 2 % ; l'orientation par invite ameliore l'alignement mais l'amelioration est limitee | echelle Pew, format a choix multiples, modeles de 2022-2023 ; la representativite est une mesure de distribution agregee, pas individuelle | soutient tres directement. **La caricature n'est pas une metaphore, c'est la distribution modale d'un groupe.** C'est exactement le mecanisme que `a1` mesure comme gonflement inter groupes sur l'axe ideologique | [CONFIRME] |
| 05-15 | Durmus, Nguyen, Liao, Schiefer, Askell et al., *Towards Measuring the Representation of Subjective Global Opinions in Language Models*, arXiv 2306.16388, 2023 | de quelles populations nationales les opinions du modele sont elles proches ? | GlobalOpinionQA, questions d'enquetes transnationales (Pew Global Attitudes et WVS) | un modele entraine par Constitutional AI | similarite des distributions de reponses conditionnellement au pays | par defaut les reponses sont plus proches des Etats Unis et de certains pays europeens et sud americains ; l'invite par pays deplace les reponses vers la population visee **mais peut refleter des stereotypes culturels nuisibles** ; traduire les questions dans la langue cible ne rapproche pas necessairement des locuteurs de cette langue | un seul modele ; pas de mesure de dispersion intra pays ; pas de plancher humain | soutient. Le meme motif que 05-14 a l'echelle des nations : l'invite d'appartenance produit un stereotype, pas une distribution | [CONFIRME] |
| 05-16 | Cheng, Piccardi et Yang, *CoMPosT : Characterizing and Evaluating Caricature in LLM Simulations*, EMNLP 2023, arXiv 2310.11501 | quelles personas et quels sujets produisent des caricatures ? | scenarios de simulation issus de travaux existants, deux contextes (forum en ligne, entretien), 100 echantillons par cellule | GPT-4 principalement | individuation (classifieur binaire sur plongements) et exageration (similarite cosinus normalisee a un axe persona-sujet) | presque toutes les personas sont individuables, donc l'exageration porte le diagnostic. Exageration maximale, contexte forum : non binaire, noir, hispanique, moyen oriental et **conservateur** ; contexte entretien : non binaire, hispanique, 80 ans, **conservateur**, moyen oriental. Les personas homme et femme sont les moins caricaturees et les plus difficiles a individuer. L'exageration est inversement liee a la specificite du sujet. Les personas conservatrice et liberale montrent le plus grand ecart entre sujets non controverses et sujets controverses | mesure sur texte libre, pas sur reponses fermees ; un modele principal ; l'axe semantique est construit par les auteurs | soutient tres directement. **La persona conservatrice est, avec les personas de minorites, l'une des plus caricaturees, et surtout sur les sujets ou la politique n'a rien a faire.** C'est le pendant textuel de notre facteur 2,1 a 2,7 sur l'axe ideologique | [CONFIRME] |
| 05-17 | Wang, Morgenstern et Dickerson, *Large language models that replace human participants can harmfully misportray and flatten identity groups*, arXiv 2402.01908, 2024 | les modeles representent ils les groupes comme leurs membres, ou comme les autres les voient ? | 9 questions, 3 200 participants humains recrutes sur Prolific, 16 identites demographiques, 100 echantillons par question | 4 modeles dont GPT-4 et Wizard Vicuna Uncensored | similarite de plongements SBERT au plus proche voisin intra groupe contre hors groupe ; 4 mesures de diversite dont le score Vendi | **les quatre modeles sont moins divers que les humains sur presque toutes les mesures et tous les groupes.** La persona « personne blanche » est plus proche de l'imitation hors groupe que de la representation intra groupe dans 23 comparaisons sur 24, la persona non binaire dans 16 sur 24, la persona malvoyante dans 18 sur 24. Monter la temperature a 1,2 puis 1,4 ne repare pas : seule la diversite en n grammes uniques rattrape l'humain, et seulement par incoherence. Des personas aleatoires atteignent une couverture aussi elevee ou plus que les attributs demographiques sensibles | reponses ouvertes, mesures semantiques ; 9 questions ; pas de plancher test retest humain | soutient. **Deux faits directement reutilisables : la temperature ne repare pas l'ecrasement, ce qui confirme `a18` ; et la persona demographique n'est pas necessaire pour obtenir de la couverture.** Le second est un argument fort pour la famille B, le conditionnement non demographique | [CONFIRME] |
| 05-18 | Hu et Collier, *Quantifying the Persona Effect in LLM Simulations*, arXiv 2402.10811, NAACL 2024 | combien de variance les variables de persona expliquent elles reellement ? | jeux d'annotation subjective existants avec annotateurs identifies | modeles jusqu'a 70 milliards de parametres | part de variance des annotations expliquee par les variables de persona ; gain de l'invite persona | **les variables de persona expliquent moins de 10 % de la variance des annotations** dans les jeux existants ; l'invite persona apporte un gain modeste mais significatif ; en zero shot, un modele 70B avec invite persona capte 81 % de la variance atteignable par une regression lineaire entrainee sur la verite terrain ; le gain est maximal quand beaucoup d'annotateurs sont en desaccord mais que les desaccords sont faibles | taches d'annotation NLP, pas des attitudes politiques ; la mesure de variance depend des jeux choisis | soutient et recoupe `a9`. **La demographie explique moins de 10 % de ce qui separe les gens.** C'est le meme constat que « segmenter ne change presque rien » de `a9` section 1.2, obtenu sur un tout autre materiau. Le plafond du conditionnement demographique est structurel, pas technique | [CONFIRME] |
| 05-19 | Röttger, Hofmann, Pyatkin, Hinck, Kirk et al., *Political Compass or Spinning Arrow ?*, arXiv 2402.16786, EMNLP 2024 | les evaluations d'opinions des modeles sont elles valides ? | revue systematique de 12 travaux utilisant le Political Compass Test ; experiences propres | plusieurs modeles ouverts et fermes | reponses contraintes contre non contraintes ; robustesse aux paraphrases | la plupart des 12 travaux forcent le format a choix multiples ; seuls trois font une forme de test de robustesse. En regime non contraint, **tous les modeles produisent des taux eleves de reponses invalides** ; les modeles refusent explicitement dans seulement 6 % des cas ; accord inter annotateurs Fleiss kappa 66,2 %, desaccord sur 18 cas sur 100. Des paraphrases minimales preservant le sens changent substantiellement les resultats du PCT, y compris item par item | pas de referent humain ; le PCT n'est pas un instrument valide, ce que les auteurs disent eux memes | soutient l'exigence methodologique. **Toute mesure de structure ideologique d'un modele doit etre testee en paraphrase avant d'etre publiee.** Cela s'applique directement a notre dette « les prompts n'ont jamais ete compares a ceux de Stanford » | [CONFIRME] |
| 05-20 | Bisbee, Clinton, Dorff, Kenkel et Larson, *Synthetic Replacements for Human Survey Data ? The Perils of Large Language Models*, *Political Analysis* 32(4), 2024, 401-416 | des repondants synthetiques peuvent ils remplacer une enquete ? | ANES 2016 et 2020, 7 530 repondants humains, 30 repondants synthetiques par humain | ChatGPT | moyennes et ecarts types des thermometres de sentiment ; polarisation affective par sous groupe | toutes les moyennes synthetiques tombent a moins d'un ecart type de la moyenne ANES, mais la variance est bien plus faible ; sur la polarisation affective l'ecart type vaut **16,1 chez ChatGPT contre 31,4 dans l'ANES** ; l'extremite des sous groupes est exageree de 0,5 a 1 ecart type, soit 10 a 20 points de thermometre, surtout chez les democrates et chez les republicains noirs non hispaniques | un seul modele, une seule periode ; les thermometres ne sont pas des attitudes structurees ; pas de plancher test retest humain | soutient. C'est la source la plus probable du 0,40 a 0,56 qui a circule dans PASSATION, et `a15` l'a deja identifiee. **A retenir ici : la sur extremite est maximale sur un sous groupe croise, republicains noirs, c'est a dire exactement la ou l'heterogeneite intra groupe est la plus reelle** | [CONFIRME] |
| 05-21 | Kim, Evans et Schein, *Linear Representations of Political Perspective Emerge in Large Language Models*, arXiv 2503.02080, ICLR 2025 | l'ideologie politique est elle encodee lineairement dans les activations ? | 552 elus americains avec scores DW-NOMINATE ; medias avec scores Ad Fontes | Llama-2-7b-chat, Mistral-7b-instruct, Vicuna-7b | sondes lineaires ridge sur les tetes d'attention ; correlation de Spearman avec DW-NOMINATE | meilleures sondes : Spearman 0,854 (Llama), 0,846 (Mistral), 0,861 (Vicuna) ; en ensemble 0,87 / 0,864 / 0,885 ; les sondes non lineaires n'ameliorent pas (0,855, 0,838, 0,872). Les memes sondes, sans reentrainement, predisent l'orientation des medias a 0,798 / 0,764 / 0,720. Les tetes predictives sont dans les couches intermediaires ; l'intervention lineaire oriente la generation | premiere dimension de DW-NOMINATE seulement ; risque de memorisation partiellement traite ; 3 modeles de 7 milliards | soutient et donne le mecanisme. **Le modele encode l'ideologie comme un axe unique, et un axe suffit a le piloter.** C'est la contrepartie interne du fait que le public, lui, en a deux faiblement correles (05-03). L'aplatissement n'est pas dans l'invite, il est dans la representation | [CONFIRME] |
| 05-22 | Aldahoul, Ibrahim, Kaufman, Rahwan et Zaki, *The Political Ideology of Large Language Models : Measurement, Inconsistency, and Persuasive Influence*, arXiv 2505.04171v2, 2025-2026 | la moderation apparente des modeles est elle une vraie moderation ? | votes de 1 327 elus du 110e au 119e Congres ; 15 juges de la Cour supreme sur 1 749 affaires ; CES 2022 et 2024, 60 000 repondants, 46 et 40 questions ; experience preenregistree N 1 523, 6 072 observations | 43 modeles | W-NOMINATE en deux dimensions ; IRT bayesien unidimensionnel ; ACP sur la matrice repondants et modeles | la premiere composante principale explique **32 %** de la variance sur 46 questions du CES 2022. Les modeles sont moderes sur la premiere dimension face aux elus mais nettement liberaux sur la seconde, celle des droits civiques. **La moderation agregee est le resultat net de positions fortement partisanes et compensatoires selon les sujets, « exactement comme les electeurs moderes ».** Les modeles de base sont pres du centre, les variantes instruites convergent vers le repere democrate fort. Experience : deplacement moyen de 3,5 points de pourcentage, plus de 10 points quand le modele est explicitement oriente, aucun effet detectable sans orientation | mesure d'opinions declarees par questionnaire ; le nombre de modeles varie selon l'analyse (43, 42, 41, 32) ; quatre modeles exclus pour refus ou biais d'ordre | **Reference centrale du theme.** Elle donne le seul resultat publie qui teste l'incoherence attitudinale d'un modele avec les outils de la science politique, et la reponse est nuancee : par sujet, les modeles sont incoherents **comme** des moderes humains. Elle affaiblit une version naive de notre these et il faut la citer | [CONFIRME] |
| 05-23 | Bernardelle, Fröhling, Civelli, Lunardi, Roitero et Demartini, *Mapping and Influencing the Political Ideology of Large Language Models using Synthetic Personas*, arXiv 2412.14843, WWW Companion 2025 | ou se placent les personas synthetiques dans l'espace politique ? | personas PersonaHub ; Political Compass Test | plusieurs modeles ouverts | coordonnees economique et sociale du PCT | les personas se concentrent dans le quadrant gauche libertaire ; tous les modeles se deplacent significativement vers le quadrant droite autoritaire quand on les y pousse, mais **plus faiblement vers gauche libertaire** | PCT non valide (voir 05-19) ; resume lu, texte integral non lu | soutient la these de l'asymetrie de reponse, cote machine. Le point de depart etant deja a gauche, il reste plus de place a droite, ce qui est une explication concurrente et non testee ici | [PROBABLE] |
| 05-24 | Bernardelle, Civelli, Fröhling, Lunardi, Roitero et Demartini, *Political Ideology Shifts in Large Language Models*, arXiv 2508.16013, 2025-2026 | la taille du modele change t elle sa malleabilite ideologique ? | 200 000 personas PersonaHub ; PCT, 62 enonces | 7 modeles ouverts de 7 a plus de 70 milliards | couverture de l'espace politique ; deplacement sur les axes economique et social ; d de Cohen | couverture : Qwen2.5-7B 13,95 %, Llama-3.1-8B 35,11 %, Llama-3.1-70B 49,06 %. Amorcage droite autoritaire, Llama-3.1-70B : +4,67 sur l'axe economique et +7,18 sur l'axe social, d superieur a 4,0 ; amorcage gauche libertaire : -1,02 et -1,90, d inferieur a 2,0. Qwen2.5-72B : 5,55 et 6,88 contre -1,77 et -2,35. Le deplacement vers la droite quadruple presque de 7B (1,59, 1,36) a 72B (5,55, 6,88) | PCT ; les 200 000 personas ne sont pas des personnes reelles ; pas de referent humain | soutient et **eclaire directement notre question ouverte de calcul**. L'asymetrie de reponse a l'etiquette croit avec la taille du modele. Si cela vaut pour nous, la condition C3 sans etiquette sur `gpt-oss-20b` devrait montrer plus d'essentialisme que sur `Qwen3-4B`, et non moins | [CONFIRME] |
| 05-25 | Kabir, *When Models Refuse : Political Steerability and Feature Richness as Measures of Ideological Depth* (v2 lue sous le titre *Beyond the Surface : Probing the Ideological Depth of Large Language Models*), arXiv 2508.21448, 2025-2026 | la profondeur de la representation politique differe t elle entre modeles ? | enonces d'evaluation politique ; auto encodeurs epars publics | Llama-3.1-8B-Instruct, Gemma-2-9B-IT | nombre de traits politiques actives ; taux de refus ; orientation par activation | Gemma active environ **7,3 fois** plus de traits politiques distincts que Llama, 18 458 contre 4 412 ; 368 traits a difference d'amplitude contre 167. **Llama refuse significativement plus sur les instructions conservatrices**, surtout sur les sujets sociaux ; l'ablation des 71 traits politiques saillants de Gemma fait fortement monter les refus. Analyse factorielle : une dimension dominante explique environ **40 %** de la variance totale | deux modeles ; les auto encodeurs epars sont ceux publies par des tiers ; l'analyse factorielle porte sur les reponses aux enonces, pas sur des humains | soutient sur deux points a la fois. **Le refus est asymetrique par camp**, ce qui est une source de distorsion que ni `a18` ni `a23` ne mesurent ; et la structure interne du modele est **a une dimension dominante**, la ou le public en a deux | [CONFIRME] |
| 05-26 | Faulborn, Sen, Pellert, Spitz et Garcia, *Only a Little to the Left : A Theory-grounded Measure of Political Bias in Large Language Models*, arXiv 2503.16148, 2025 | comment mesurer le biais politique sans le Political Compass Test ? | 88 110 reponses generees ; batterie construite selon les principes de conception d'enquete | 11 modeles ouverts et commerciaux, instruits et non instruits | profils de biais par variation d'invite | **le PCT exagere le biais pour certains modeles, dont GPT-3.5** ; les mesures de biais politique sont souvent instables ; les modeles instruits sont generalement plus a gauche | pas de referent humain ; la classification des positions est automatique | soutient l'exigence de mesure. Les chiffres publies sur l'ideologie des modeles dependent lourdement de l'instrument, exactement comme les chiffres de fidelite dependent du denominateur | [CONFIRME] |
| 05-27 | Kamal, Prakash, Rafiuddin, Rakib, Sen et al., *A Detailed Factor Analysis for the Political Compass Test*, arXiv 2506.22493, 2025 | qu'est ce qui deplace vraiment le score politique d'un modele ? | PCT et 8 Values ; dix invites de Röttger et al. | plusieurs modeles ouverts quantifies en 4 bits, avec et sans reglage fin | ANOVA a une et deux voies sur les scores social et economique | les parametres de decodage (top_k, temperature, nombre de faisceaux) ont un effet minime ; **la formulation de l'invite et le reglage fin ont un effet significatif**, individuellement et en interaction ; le reglage fin sur des donnees politiquement riches ne deplace pas differemment de donnees neutres ; l'effet de l'invite est fort sur l'axe economique et pas systematique sur l'axe social | PCT ; petites versions de modeles ; scores calcules par un serveur dont la fonction d'agregation n'est pas publique | soutient `a18` par une autre voie. **Le decodage n'est pas la cause, le conditionnement l'est.** C'est la meme conclusion que « la famille A est fermee, la famille B est la piste restante », obtenue sur un tout autre protocole | [CONFIRME] |
| 05-28 | Sakhawat, Islam, Farhin, Raiyan, Mahmud et al., *Political Alignment in Large Language Models : A Multidimensional Audit of Psychometric Identity*, arXiv 2601.06194, 2026 | un seul axe suffit il a auditer un modele ? | trois inventaires (Political Compass, SapplyValues, 8Values) et une tache d'etiquetage de biais de presse ; plusieurs variantes semantiques d'invite | 26 modeles | ANOVA a deux voies separant effet du modele et effet de l'invite | la plupart des modeles se placent dans le quadrant **gauche libertaire** ; l'identite du modele explique l'essentiel de la variance entre variantes d'invite ; l'axe social du Political Compass s'aligne davantage sur le progressisme culturel que sur les mesures d'autorite ; la position psychometrique **ne predit pas** les erreurs de classification en aval | instruments non valides ; pas de referent humain ; les valeurs numeriques d'effet sont dans des balises mathematiques non extraites ici | soutient la conclusion « une dimension ne suffit pas ». Et un point derangeant pour l'application : **l'ideologie declaree d'un modele ne predit pas son comportement sur tache**, ce qui est le pendant machine du decalage symbolique / operationnel de 05-04 | [CONFIRME] |
| 05-29 | Wang, Hunt, Tang et Joseph, *Can Finetuning LLMs on Small Human Samples Increase Heterogeneity, Alignment, and Belief-Action Coherence ?*, arXiv 2511.21218, 2025 | un reglage fin sur un petit echantillon repare t il l'homogeneite ? | experience comportementale de divulgation d'information, donnees humaines de Hunt et al. 2025, recrutement Prolific | modeles ouverts, base contre regles finement | nombre de structures de croyances uniques ; distance de Jensen-Shannon ; recuperation des coefficients de regression | **le modele non regle produit 19 structures de croyances uniques sur 929 simulations, contre 340 dans les donnees humaines** ; le reglage fin sur environ 30 observations (25 % d'un groupe de traitement) fait passer a au moins 200 structures et divise au moins par deux la distance de Jensen-Shannon ; **aucun modele regle ne reproduit les coefficients de regression de l'etude d'origine** ; l'echantillonnage equilibre par ethnie n'ameliore pas l'alignement des minorites plus que l'echantillonnage aleatoire | une seule experience, domaine securite ; N de simulations modeste ; pas d'attitudes politiques | soutient tres directement, et c'est le meilleur chiffre du theme sur l'effondrement de **structure** et non de variance. **19 contre 340 patrons de reponses.** C'est la mesure que `a9` tache 2 cherche : l'exces de coherence ne se lit pas seulement dans un alpha, il se lit dans le nombre de combinaisons distinctes qui survivent | [CONFIRME] |
| 05-30 | Wang, Zhou, Du, Su, Cao, Pan et al., *Mitigating Identity Essentialism in LLM Agents with Longitudinal Life Trajectories* (LifeMem), arXiv 2608.19621, 2026 | le conditionnement statique par profil produit il de l'essentialisme identitaire ? | 2 000 repondants WVS vague 7 en trois groupes de statut socio economique ; Add Health ; Understanding Society | trois modeles dont Llama-8B | score de silhouette dans l'espace des reponses ; ecart de distance intra groupe par paires humains contre agents | les agents a profil statique montrent une **separation demographique plus forte et une compression intra groupe plus forte** que les humains, motif qualifie d'essentialisme identitaire ; LifeMem, memoire longitudinale a deux composantes, ameliore les distributions, la diversite globale et intra groupe, et les changements intra personne entre etapes de vie | les valeurs de silhouette sont dans des figures et des balises non extraites ici ; comparaison contre des lignes de base d'invite, pas contre un plafond test retest humain | soutient, et occupe le terrain du correctif. Deja identifie dans `a13`. **Le point neuf pour le theme 05 : la solution proposee n'est pas de dilater la variance mais de remplacer l'etiquette par une trajectoire**, ce qui est la famille B de `exploration/09` | [CONFIRME] |
| 05-31 | Xiao, Zhang, Yang, Ma, Xuan, Huang et al., *The Chameleon's Limit : Investigating Persona Collapse and Homogenization in Large Language Models*, arXiv 2604.24698, 2026 | une banque de personas produit elle une population ou une caricature ? | BFI-44 (1 144 personas par modele), 131 scenarios moraux, auto presentations ; reference humaine **Twin-2K-500**, N 2 058 | 10 modeles, generalistes et specialises jeu de role | couverture ; dimension intrinseque locale (LID) ; d de Cohen entre groupes demographiques ; taux de mention d'attribut | humains : couverture 1,0 et LID 14,4 ; meilleur modele Qwen3-4B : 0,80 et 7,3 ; pire, CoSER-Llama-8B : 0,16 et 4,6. **Tous les modeles a fidelite rho superieure a 0,9 produisent des d de Cohen superieurs a 6 entre groupes**, tres au dela du seuil de 2 dit « tres grand » chez les humains. Mention de l'attribut : genre 91 %, pays 90 %, **ideologie politique 62 %**, age 36 %, classe sociale 27 %. Claude-Haiku-4.5 comprime 57 % de la variance demographique sur le genre | pas de plancher test retest humain ; les LID sont sensibles au plongement choisi ; modeles recents non reproductibles a l'identique | **La reference la plus proche de notre travail, sur notre jeu de donnees.** Elle formule la double distorsion sous une autre forme : plus la fidelite par persona est haute, plus la population est stereotypee. Elle rend urgent de citer le plafond humain test retest, qui reste notre element non couvert | [CONFIRME] |
| 05-32 | Wang, Zhou, Du, Ai et Liu, *Parametric Social Identity Injection and Diversification in Public Opinion Simulation*, arXiv 2603.16142, KDD 2026 | ou, dans le reseau, la diversite disparait elle ? | World Values Survey ; 500 agents | plusieurs modeles ouverts | ACP a noyau sur les etats caches du dernier jeton, couche par couche ; divergence KL a l'enquete reelle | **effondrement de diversite** : les couches basses forment des amas compacts, les couches intermediaires s'etalent et atteignent une diversite elevee, les couches hautes se contractent en amas denses. L'injection de vecteurs parametriques d'identite dans les etats caches intermediaires reduit la KL et augmente la diversite | mesure sur representations internes, pas sur reponses ; les gains chiffres sont dans des tables non extraites ici ; WVS uniquement | soutient et donne une localisation. **L'ecrasement se produit dans les dernieres couches, apres que la diversite a existe.** Cela dit ou intervenir, et cela explique pourquoi la temperature echoue : le deficit est deja constitue avant le decodage | [CONFIRME] |
| 05-33 | Gilg, Beckmann, Paleka et Butlin, *Probing Persona-Dependent Preferences in Language Models*, arXiv 2605.13339, 2026 | les personas partagent elles la meme machinerie de preference ? | reservoir de 6 000 taches, choix par paires | Gemma-3-27B, Qwen-3.5-122B, Llama-3.1-8B-Instruct | sondes lineaires sur le flux residuel predisant des utilites ; orientation contrastive | **un axe evaluatif unique** : une sonde entrainee sur la persona Assistant predit les preferences d'autres personas meme quand les utilites de base sont anti correlees (persona « mechante » : correlation de base -0,146, prediction de la sonde +0,243) ; la persona mechante fait passer l'ecart nuisible / benin de -4,52 a +1,15 sur Gemma-3-27B ; l'orientation deplace la probabilite de choix de la tache visee d'environ 0,05 a environ 0,95 | personas artificielles, pas des identites sociales ; taches non politiques ; les auteurs notent que le mecanisme n'est pas exactement le meme selon les personas | soutient le mecanisme. **Changer de persona ne change pas l'espace de preference, cela deplace un point sur un axe.** C'est la formulation la plus economique de l'aplatissement : une persona n'est pas une personne, c'est un scalaire | [CONFIRME] |
| 05-34 | Zaller, *The Nature and Origins of Mass Opinion*, Cambridge University Press, 1992 | comment une reponse d'enquete est elle produite ? | reanalyses ANES et enquetes de campagne | modele Receive-Accept-Sample | ambivalence : la reponse est un echantillon des considerations accessibles au moment de la question | le modele predit l'instabilite des reponses sans supposer l'absence d'attitude, et fait de la sophistication politique le moderateur central de la reception et de l'acceptation | livre non consulte ; aucun chiffre n'est repris ici | soutient conceptuellement. **C'est la reponse theorique a la question A11 : l'incoherence humaine n'est pas du bruit, c'est un echantillonnage de considerations contradictoires reellement detenues.** Un modele qui repond a partir d'un profil fixe echantillonne toujours dans la meme direction | [PROBABLE] |
| 05-35 | Zaller et Feldman, *A Simple Theory of the Survey Response*, *American Journal of Political Science* 36(3), 1992, 579-616, DOI 10.2307/2111583 | pourquoi les gens changent ils de reponse d'une vague a l'autre ? | ANES et experiences d'amorcage | modele a considerations | variance de reponse expliquee par l'accessibilite des considerations | l'ambivalence, et non l'absence d'attitude, explique l'essentiel de l'instabilite | paywall, non consulte | soutient. Version article de 05-34 | [PROBABLE] |
| 05-36 | Achen, *Mass Political Attitudes and the Survey Response*, *American Political Science Review* 69(4), 1975, 1218-1231 | l'instabilite de Converse est elle de l'inattitude ou de l'erreur de mesure ? | memes panels ANES 1956-1960 | modele a erreur de mesure sur variable latente | fiabilite estimee des items | attribue l'essentiel de l'instabilite a la faible fiabilite des instruments plutot qu'a l'absence d'attitude | paywall, non consulte ; la controverse Achen contre Converse n'est pas tranchee dans la litterature | contredit 05-01 sur l'interpretation. **Conclusion pour nous : il faut un plancher de bruit par item avant de conclure quoi que ce soit sur l'incoherence.** Ce plancher existe pour le GSS, c'est 05-06 | [PROBABLE] |
| 05-37 | Feldman, *Structure and Consistency in Public Opinion : The Role of Core Beliefs and Values*, *American Journal of Political Science* 32(2), 1988, 416-440 | qu'est ce qui organise les opinions quand l'ideologie ne le fait pas ? | ANES | modeles structurels sur valeurs fondamentales | egalite des chances, individualisme economique, libre entreprise | les valeurs fondamentales structurent les opinions mieux que l'auto placement ideologique, et elles sont partiellement en conflit chez la meme personne | paywall, non consulte | soutient. **Le conflit de valeurs a l'interieur d'une personne est la source theorique de l'incoherence structuree**, et c'est un candidat direct pour A12, le trait latent de conditionnement | [PROBABLE] |
| 05-38 | Feldman et Johnston, *Understanding the Determinants of Political Ideology : Implications of Structural Complexity*, *Political Psychology* 35(3), 2014, 337-358 | l'ideologie a t elle une ou plusieurs dimensions, et les memes causes ? | ANES et enquetes complementaires | analyse en classes latentes et modeles multidimensionnels | classes latentes ; determinants par dimension | deux dimensions, economique et sociale, sont le minimum pour rendre compte des preferences de politique interieure ; **les determinants de ces deux dimensions different fortement selon les groupes** ; une classe latente combine autoritarisme eleve et positions economiques tres a gauche | paywall, non consulte ; les effectifs de classes ne sont pas repris ici | soutient. La reference demandee au brief. **Elle dit exactement ce qu'une simulation devrait produire : des classes latentes croisant les deux axes, pas un continuum** | [PROBABLE] |
| 05-39 | Jost, Glaser, Kruglanski et Sulloway, *Political Conservatism as Motivated Social Cognition*, *Psychological Bulletin* 129(3), 2003, 339-375 | le conservatisme a t il une base cognitive et motivationnelle propre ? | meta analyse de 88 echantillons, 12 pays, 22 818 cas | meta analyse | r moyens ponderes | anxiete de mort 0,50 ; instabilite du systeme 0,47 ; dogmatisme et intolerance a l'ambiguite 0,34 ; ouverture a l'experience -0,32 ; tolerance a l'incertitude -0,27 ; besoins d'ordre, de structure et de cloture 0,26 ; complexite integrative -0,20 ; peur de la menace et de la perte 0,18 ; estime de soi -0,09. Deux dimensions du conservatisme : resistance au changement et acceptation de l'inegalite | non consulte ; chiffres relayes par une source secondaire lors de la recherche ; meta analyse contestee sur le choix des etudes et l'operationnalisation | pose la these de l'asymetrie. **Elle est le point de depart du debat, pas sa conclusion**, et 05-10, 05-11 et 05-12 la relativisent. A citer avec sa contestation | [PROBABLE] |
| 05-40 | Jost, *Ideological Asymmetries and the Essence of Political Psychology*, *Political Psychology* 38(2), 2017, 167-208 | l'asymetrie est elle l'objet central de la psychologie politique ? | synthese de 181 etudes de motivation epistemique et pres de 100 de motivation existentielle | revue | asymetries en dogmatisme, rigidite, besoins d'ordre, complexite integrative, tolerance a l'ambiguite | l'auteur soutient que les asymetries sont etablies sur ces construits | non consulte, PDF non accessible ; texte de position d'une partie au debat | pose la these forte. A opposer a 05-10 et 05-11 | [PROBABLE] |
| 05-41 | Kinder et Kalmoe, *Neither Liberal nor Conservative : Ideological Innocence in the American Public*, University of Chicago Press, 2017 | l'innocence ideologique de Converse tient elle encore ? | series ANES longues | reanalyses | stabilite de l'auto placement ideologique ; pouvoir predictif compare a l'identification partisane | les vrais liberaux et vrais conservateurs ne se trouvent en nombre que chez les tres engages ; le public est devenu plus partisan sans devenir plus ideologique | livre, non consulte | soutient et recoupe 05-02. **Consequence directe : l'etiquette ideologique dans une invite est une variable a faible contenu pour la majorite du public**, ce qui rend le facteur 8,51 de `gss_v8` d'autant plus anormal | [PROBABLE] |
| 05-42 | Kalmoe, *Uses and Abuses of Ideology in Political Psychology*, *Political Psychology* 41(4), 2020, 771-793 | que mesure t on quand on mesure l'ideologie ? | revue methodologique | aucun | validite des mesures d'ideologie | avertit contre l'usage de l'auto placement comme si c'etait une contrainte attitudinale | acces libre annonce par Unpaywall mais lien de depot non telechargeable ; non consulte | soutient l'exigence de mesure | [NON LU] |
| 05-43 | Alvarez et Brehm, *American Ambivalence Towards Abortion Policy*, *American Journal of Political Science* 39(4), 1995, 1055-1082 ; et *Hard Choices, Easy Answers*, Princeton University Press, 2002 | l'ambivalence se voit elle dans la variance des reponses ? | ANES | probit heteroscedastique | la variance de la reponse, et non seulement sa moyenne, est modelisee | l'ambivalence se manifeste comme une variance conditionnelle accrue chez les personnes tenant des valeurs en conflit | paywall, non consulte | soutient. **Methode directement transposable : modeliser la variance individuelle et non la moyenne.** C'est la forme statistique de « l'incoherence au bon endroit » de A11 | [PROBABLE] |
| 05-44 | Tetlock, travaux sur la complexite integrative, notamment *Journal of Personality and Social Psychology* 1983 et 1986 | la complexite du raisonnement politique differe t elle selon le camp ? | discours d'elus, protocoles verbaux | codage de complexite integrative | differenciation et integration des arguments | la complexite integrative est plus elevee chez les moderes et chez ceux dont les valeurs sont en conflit ; relation en U inverse avec l'extremite plutot que lineaire avec la direction | non consulte ; codage manuel, faible taille d'echantillon dans les etudes d'origine | soutient une lecture non asymetrique. **Si la complexite depend du conflit de valeurs et non du camp, alors ce qu'une simulation doit reproduire est le conflit, pas l'etiquette** | [PROBABLE] |
| 05-45 | Layman et Carsey, *Party Polarization and Conflict Extension in the American Electorate*, *American Journal of Political Science* 46(4), 2002, 786-802 | les nouveaux clivages remplacent ils les anciens ou s'y ajoutent ils ? | NES | modeles de changement d'attitude | correlations par domaine, economique, culturel, racial | these de l'extension du conflit : les clivages culturels s'ajoutent aux clivages economiques chez les partisans engages, sans les remplacer | paywall, non consulte | soutient la multidimensionnalite. Compatible avec 05-02 : plus de partisanship, pas plus d'alignement | [PROBABLE] |
| 05-46 | Malka, Soto, Inzlicht et Lelkes, *Do Needs for Security and Certainty Predict Cultural and Economic Conservatism ?*, *Journal of Personality and Social Psychology* 106(6), 2014, 1031-1051 | les besoins de securite predisent ils les deux conservatismes ? | enquetes transnationales | modeles multiniveaux | correlations besoins x conservatisme culturel et economique | les besoins de securite et de certitude predisent le conservatisme culturel mais **pas** le conservatisme economique, et parfois l'inverse | paywall, non consulte | contredit une lecture unidimensionnelle de 05-39. Complementaire de 05-08 | [PROBABLE] |
| 05-47 | DellaPosta, *Pluralistic Collapse : The « Oil Spill » Model of Mass Opinion Polarization*, *American Sociological Review* 85(3), 2020, 507-536 | la politique contamine t elle des attitudes qui n'etaient pas politiques ? | GSS, 44 ans de donnees, tres nombreux domaines | analyse de reseaux de croyances | consolidation des croyances au cours du temps | la polarisation progresse comme une nappe qui teinte progressivement des opinions auparavant apolitiques | paywall, non consulte | contredit partiellement 05-02 sur l'alignement, avec un materiau plus large. **A tenir avec 05-02 : la contrainte ne croit pas entre items politiques mais croit entre le politique et le reste** | [PROBABLE] |
| 05-48 | Boutyline et Vaisey, *Belief Network Analysis*, *American Journal of Sociology* 122(5), 2017, 1371-1447 | quelles croyances sont centrales dans un systeme de croyances ? | ANES 2000 | reseaux de correlations, mesures de centralite | centralite des noeuds | l'identite politique, et non des schemas parentaux, occupe la position centrale ; la sophistication politique augmente la contrainte inter attitudes | paywall, non consulte | soutient. **Outil directement applicable : mesurer la centralite dans le reseau de correlations des agents contre celui des humains.** C'est plus informatif qu'un alpha de Cronbach global, et cela repond a la question A11 | [PROBABLE] |
| 05-49 | Freeder, Lenz et Turney, *The Importance of Knowing « What Goes with What »*, *Journal of Politics* 81(1), 2019, 274-290 | la contrainte est elle un artefact d'agregation ? | ANES et panels | reanalyse de la mesure de contrainte | contrainte a l'echelle de l'individu | la contrainte apparente au niveau agrege est portee par une minorite informee ; la majorite ne sait pas ce qui va avec quoi | paywall, non consulte | soutient 05-01 contre 05-36 | [PROBABLE] |
| 05-50 | Broockman, *Approaches to Studying Policy Representation*, *Legislative Studies Quarterly* 41(1), 2016, 181-215 ; et Ahler et Broockman, *The Delegate Paradox*, *Journal of Politics* 80(4), 2018, 1117-1133 | les moderes sont ils moderes ? | enquetes sur echantillons nationaux | mesure position par position | part de gens tenant des positions extremes de signes opposes | les « moderes » agreges sont souvent des personnes tenant des positions extremes dans les deux directions ; agreger deux extremes produit un centre qui n'existe chez personne | paywall, non consulte ; le fait est reproduit et chiffre par 05-05, qui est [CONFIRME] | soutient. **Cite ici pour l'anteriorite ; le chiffre a utiliser est celui de 05-05, 20,7 %** | [PROBABLE] |
| 05-51 | Hajnal et Lee, *Why Americans Don't Join the Party*, Princeton University Press, 2011 ; Philpot, *Conservative but Not Republican*, Cambridge University Press, 2017 ; White et Laird, *Steadfast Democrats*, Princeton University Press, 2020 | comment se structurent les attitudes des minorites raciales aux Etats Unis ? | enquetes nationales, dont sur suréchantillons noirs et latinos | varies | independance partisane ; ecart entre ideologie et vote | les Latinos et Asiatiques americains sont massivement non affilies et mal decrits par l'axe partisan ; une part importante des Noirs americains est conservatrice sur le plan social tout en votant democrate de facon quasi unanime, par une norme de groupe | livres, non consultes | soutient. **Le cas le plus net ou l'etiquette de groupe et la position d'attitude divergent.** Un agent « noir americain » qui repond democrate sur tout efface la moitie de la distribution sociale du groupe ; 05-07 le chiffre sur un item | [PROBABLE] |
| 05-52 | Li et Conrad, *Persona-Based Simulation of Human Opinion at Population Scale*, arXiv 2603.27056, 2026 | peut on construire une banque de personas a partir de traces reelles ? | traces de reseaux sociaux liees par consentement a des repondants du panel Ipsos KnowledgePanel | modeles de langage | exactitude au niveau de l'utilisateur ; estimations par banque de personas ponderee | banque de personas utilisee comme panel de repondants virtuels ; analyses par categorie de question et par qualite des traces | resume et table des matieres lus, corps non extrait | pertinent pour la suite du projet plus que pour le theme 05 : c'est la version « traces reelles » du conditionnement non demographique | [PROBABLE] |

---

## Synthese par question

### 1. La these de l'asymetrie droite gauche est elle etablie, contestee, ou dependante de la mesure ?

**Elle depend de la mesure, et le sens du desaccord est connu.** Trois blocs de resultats
s'opposent proprement.

Le bloc qui la soutient est celui des motivations epistemiques et existentielles. La meta
analyse fondatrice donne des r de 0,50 pour l'anxiete de mort, 0,34 pour le dogmatisme et
-0,32 pour l'ouverture (05-39, [PROBABLE]), et la revue de 2017 revendique 181 etudes de
motivation epistemique (05-40, [PROBABLE]). Ces deux entrees n'ont pas pu etre lues dans le
texte, ce qui est une limite serieuse du present etat des lieux.

Le bloc qui la conteste est chiffre et lu. Sur le biais partisan, 51 tests experimentaux et
18 815 participants donnent liberaux 0,235 et conservateurs 0,255, difference 0,009 non
significative (05-10, [CONFIRME]). Sur l'autoritarisme, la gauche a une structure a trois
facteurs et le LWA est **moins** dogmatique et moins rigide que le RWA, mais plus eleve en
emotionnalite negative (05-09, [CONFIRME]) ; douze etudes sur plus de 8 000 Americains
trouvent des effets LWA d'ampleur comparable aux effets RWA, y compris en ne regardant que
les liberaux (05-11, [CONFIRME]). La revue de 2023 tranche par un « les deux, sur des
variables differentes » : le RWA est lie au besoin d'ordre et negativement a la confiance dans
la science, le LWA au besoin de chaos et **positivement** a la confiance dans la science
(05-12, [CONFIRME]).

Le troisieme bloc dit que la question est mal posee, parce que les deux camps n'ont pas la
meme structure interne. Deux dimensions sont necessaires, et elles ne sont correlees qu'a
0,30 (05-03). Les liberaux declares ont une relation plus forte entre leurs dimensions
economique et sociale que les conservateurs declares, et 38 % des conservateurs contre 35 %
des liberaux sortent de leur quadrant (05-03, [CONFIRME]). C'est un ecart faible mais dans le
sens de l'hypothese d'une droite plus heterogene, et les auteurs l'attribuent a la
desirabilite differentielle des deux etiquettes, pas a une difference cognitive. Le decalage
symbolique / operationnel va dans le meme sens : environ un tiers de l'electorat se declare
conservateur tout en voulant plus d'action publique (05-04, [CONFIRME]).

**Ce que cela impose au projet.** Aucune asymetrie ne peut etre postulee dans notre protocole.
Si nos agents sont plus homogenes du cote conservateur que du cote liberal, ce n'est pas un
fait humain reproduit, c'est un artefact a expliquer. Et si la droite humaine est un peu plus
heterogene, c'est parce que l'etiquette « conservateur » y est plus attractive que le contenu,
donc pour une raison **symbolique**, precisement celle que l'invite d'un modele reproduit le
mieux.

### 2. Combien de dimensions ont les attitudes reelles, et lesquelles ?

**Deux au minimum en Amerique du Nord, faiblement correlees ; et le signe de la correlation
s'inverse ailleurs.**

Aux Etats Unis, un modele a deux dimensions bat un modele a une dimension au DIC, les
dimensions sont economique et sociale, et leur correlation vaut 0,30 (05-03, [CONFIRME]). La
premiere composante principale d'une batterie de 46 questions du CES 2022 n'explique que 32 %
de la variance (05-22, [CONFIRME]). Une modelisation en trois types sur 285 485 repondants
attribue 72,8 % des gens a un modele unidimensionnel, 20,7 % a des positions genuines mal
resumees par un axe et 6,5 % a du bruit (05-05, [CONFIRME]). Autrement dit : un axe suffit
pour les trois quarts et rate un cinquieme.

Hors des democraties riches, la structure change de signe. Sur 99 nations et 325 802
personnes, les six correlations moyennes entre conservatisme culturel et conservatisme
economique sont **negatives** (-0,013 a -0,058) ; la part de pays a correlation
significativement negative va de 34,0 % a 58,0 %, contre 7,4 % a 20,8 % de positives (05-08,
[CONFIRME]). L'engagement politique est ce qui recree l'alignement droite gauche.

L'ideologie n'est donc pas une dimension psychologique, c'est un produit d'elite diffuse a
proportion de l'exposition. Converse le disait avec 0,53 chez les candidats au Congres contre
0,23 dans le public (05-01, [CONFIRME]) ; Malka le mesure sur 99 pays soixante ans plus tard.

### 3. Ou se loge l'incoherence reelle, et pourquoi ce n'est pas du bruit ?

Trois faits lus permettent de repondre precisement.

**Premier fait : l'incoherence a une taille et elle est separee du bruit.** 20,7 % de
Conversiens contre 6,5 % d'inattentifs (05-05). L'incoherence est trois fois plus frequente
que le bruit, et le modele de melange les distingue avec une probabilite posterieure
superieure a 0,95 pour 66 % des repondants.

**Deuxieme fait : elle se loge entre domaines, pas dans un domaine.** La correlation moyenne
entre paires d'items vaut 0,15 et n'augmente que de 0,02 par decennie, alors que la
correlation avec le parti vaut 0,17 et augmente de 0,05 par decennie (05-02). Les gens sont
tries par etiquette sans etre alignes entre enjeux. C'est la meme geometrie que Converse
mesurait sur la frontiere domestique / etranger : 0,25 contre 0,53 chez l'elite, 0,11 contre
0,23 dans le public (05-01).

**Troisieme fait : elle est plus frequente chez ceux qui se declarent au centre.** 44 % des
moderes declares et 47 % des « ne sait pas » sont contre pression, et seulement 17 % des
moderes sont reellement centristes sur les deux dimensions (05-03). Le centre agrege est
majoritairement une somme d'extremites de signes opposes.

**Pourquoi ce n'est pas du bruit.** Parce qu'elle est previsible a partir de la structure des
valeurs, pas a partir de la demographie. Les valeurs fondamentales en conflit organisent les
opinions mieux que l'auto placement (05-37, [PROBABLE]) ; l'ambivalence se manifeste comme une
variance conditionnelle modelisable et non comme un residu (05-43, [PROBABLE]) ; et la reponse
d'enquete est un echantillon de considerations reellement detenues, pas un tirage aleatoire
(05-34 et 05-35, [PROBABLE]). Converse lui meme donne le test : le modele purement aleatoire
n'ajuste **qu'un seul** item de sa batterie ; tous les autres exigent une troisieme population
en conversion reelle (05-01, [CONFIRME]).

Cela repond a la question A11 de `BRAINSTORM.md`. Oui, il existe une litterature sur la
structure de l'incoherence attitudinale ; elle porte les noms d'ambivalence, de conflit de
valeurs et de contre pression ; et sa forme statistique est une variance conditionnelle, pas
un bruit additif. Cela repond aussi negativement a A10 : **la propension a devier de son groupe
n'est pas un trait connu de la psychologie sociale.** Ce qui est connu, c'est la propension a
detenir des valeurs en conflit, ce qui n'est pas la meme chose et se mesure autrement.

### 4. Ce que les LLM en font, d'apres les rares papiers qui l'ont teste

**Ils aplatissent sur un axe, et ils le font dans la representation interne, pas dans
l'invite.**

Des sondes lineaires sur les tetes d'attention predisent le DW-NOMINATE de 552 elus a
Spearman 0,854 a 0,861, et les sondes non lineaires n'ameliorent rien (05-21, [CONFIRME]).
Une analyse factorielle des reponses politiques d'un modele donne **une** dimension dominante
a environ 40 % de la variance (05-25, [CONFIRME]). Une sonde entrainee sur une seule persona
predit les preferences d'autres personas meme quand leurs utilites sont anti correlees
(05-33, [CONFIRME]). Trois protocoles independants convergent : le modele possede un axe, et
les personas sont des points sur cet axe.

**La persona conservatrice est bien la caricature symbolique.** Elle figure parmi les personas
au score d'exageration le plus eleve dans les deux contextes testes, aux cotes des personas de
minorites, et l'ecart entre sujets controverses et non controverses est maximal pour les
personas conservatrice et liberale (05-16, [CONFIRME]). Un modele ajuste par retour humain
converge vers les vues **modales** des liberaux et des moderes, au point d'atteindre 99 %
d'approbation de Joe Biden (05-14, [CONFIRME]). L'invite par pays produit des stereotypes
culturels (05-15, [CONFIRME]).

**Deux resultats derangeants pour notre these.** D'abord, conditionne sur onze vraies reponses,
GPT-3 reproduit la matrice de V de Cramer entre douze items avec une difference moyenne de
seulement -0,026 (05-13, [CONFIRME]) : la structure d'association n'est pas perdue dans ce
regime. Ensuite, l'audit le plus complet publie a ce jour conclut que la moderation agregee
des modeles est le resultat net de positions fortement partisanes et compensatoires selon les
sujets, **« exactement comme les electeurs moderes »** (05-22, [CONFIRME]). Sur la dimension
« un axe suffit il », les modeles ressembleraient donc aux humains plutot qu'a une caricature.
Il faut prendre ce resultat au serieux et le citer.

**Ce qui reste solide malgre cela.** L'effondrement porte sur le nombre de patrons distincts,
pas sur la matrice de correlations : 19 structures de croyances uniques sur 929 simulations
contre 340 chez les humains (05-29, [CONFIRME]). Une population entiere reduite a 19 profils
peut parfaitement reproduire des correlations moyennes correctes. C'est la ou la mesure de
`a9` doit se deplacer : compter les combinaisons, pas seulement l'alpha.

**Ou l'ecrasement se produit.** Dans les dernieres couches, apres que la diversite a existe
dans les couches intermediaires (05-32, [CONFIRME]). Cela explique pourquoi le decodage ne
repare rien : ni la temperature jusqu'a l'incoherence (05-17), ni les parametres de decodage
(05-27), alors que l'invite et le reglage fin deplacent tout (05-27), et que 30 observations
humaines suffisent a faire passer de 19 a 200 patrons (05-29). C'est la confirmation externe
de la fermeture de la famille A dans `exploration/09`.

**Un biais non mesure chez nous.** Un modele refuse significativement plus sur les
instructions conservatrices que liberales (05-25, [CONFIRME]). Nos runs ne comptent pas les
refus par camp. Si un tel biais existe sur nos modeles locaux, une partie du ratio intra
mesure sur le segment conservateur est un artefact de refus, pas de croyance.

### 5. Quels items du GSS permettent de mesurer chez nous la structure interne d'un camp

Le GSS contient de quoi construire les deux dimensions de 05-03 et 05-38, et 05-06 dit
lesquels de ces items sont assez fiables pour cela.

**Axe economique et operationnel.** `eqwlth` (l'Etat doit il reduire les ecarts de revenus),
`helppoor`, `helpsick`, `helpblk`, `helpnot`, plus la batterie de depenses `natfare`,
`nateduc`, `natheal`, `natrace`, `natarms`, `natenvir`, `nataid`, `natspac`, `natcity`,
`natcrime`, `natdrug`. Fiabilite des items de depense entre 0,4 et 0,8 selon le sujet, avec
les plus fiables sur environnement, education, aide raciale, espace, defense, aide etrangere
et welfare, et les moins fiables sur science, crime, drogue et questions urbaines. `helpnot`
est le moins fiable des items politiques du GSS (05-06, [CONFIRME]) et doit etre exclu d'une
mesure de structure.

**Axe social et culturel.** La batterie avortement (`abany`, `abdefect`, `abhlth`, `abnomore`,
`abpoor`, `abrape`, `absingle`), la moralite sexuelle (`premarsx`, `homosex`, `xmarsex`,
`teensex`, `pornlaw`), les roles de genre (`fefam`, `fechld`, `fepresch`), la religion a
l'ecole (`prayer`, `bible`), l'ordre (`cappun`, `courts`, `gunlaw`, `grass`).

**Batterie de tolerance, utile parce qu'elle croise les deux axes.** Les items Stouffer
`spkath`, `colath`, `libath` et leurs equivalents pour communiste, militariste, raciste et
homosexuel. Ils opposent les libertaires aux autoritaires **a l'interieur** de chaque camp,
ce qui est exactement la partition que 05-09 et 05-12 rendent necessaire.

**Ancrages.** `polviews` et `partyid`. Attention : `partyid` a une fiabilite de 0,84 et
`polviews` de seulement 0,66 (05-06, [CONFIRME]). L'axe sur lequel `a1` mesure un gonflement
de 2,1 a 8,51 est donc **le moins fiable des deux ancrages disponibles**. Ce point doit
figurer dans le papier : une partie du ratio intra faible sur le segment ideologique est
imputable a l'instabilite de la variable de segmentation elle meme, pas seulement au
generateur.

**Protocole minimal propose, sans code nouveau.** Sur les fichiers de l'archive OSF, calculer
pour chaque personne un score economique et un score social par simple moyenne standardisee
des deux blocs ci dessus, puis : (i) la correlation entre les deux scores chez les humains et
chez les agents, la cible humaine etant de l'ordre de 0,30 (05-03) ; (ii) la part de
contre presses par quadrant a l'interieur de chaque segment de `polviews`, la cible etant de
l'ordre de 35 a 38 % hors quadrant (05-03) ; (iii) le nombre de patrons de reponses distincts
sur un sous ensemble de dix items, humains contre agents, sur le modele du 19 contre 340 de
05-29 ; (iv) le tout normalise par le plancher test retest de la vague 2 humaine, ce que
personne d'autre ne fait.

---

## Ce que personne n'a fait

1. **Aucun papier ne mesure la structure attitudinale simulee contre un plancher humain de
   reinterrogation.** 05-29 compte 19 patrons contre 340, mais ne dit pas combien de patrons
   les memes humains produisent a deux semaines d'intervalle. 05-31 compare couverture et
   dimension intrinseque a une reference humaine unique. La consistance test retest de
   l'archive OSF t6g7k reste le seul instrument qui donne le denominateur, et c'est encore
   l'atout non copie du projet.

2. **Personne n'a teste si un agent reproduit la proportion de contre presses.** Toute la
   litterature LLM mesure la position moyenne d'un camp ou la variance a l'interieur d'un
   camp. Aucune ne mesure la part de gens **du meme camp** qui sont liberaux sur une dimension
   et conservateurs sur l'autre. C'est pourtant la statistique la plus discriminante de la
   science politique sur ce point, et elle est calculable sur nos fichiers en une heure.

3. **Personne n'a croise l'asymetrie de refus avec l'asymetrie de variance.** 05-25 montre que
   les refus sont plus frequents sur les instructions conservatrices. 05-14 montre que le
   modele converge vers le mode liberal. Personne n'a verifie si l'ecrasement intra groupe
   mesure sur un segment est simplement le refus differencie, filtre par l'evaluateur.

4. **Personne n'a compare le conditionnement par etiquette au conditionnement par valeurs
   fondamentales.** 05-30 propose des trajectoires de vie et 05-32 des vecteurs d'identite
   parametriques, mais aucun ne conditionne sur les deux ou trois valeurs de Feldman
   (egalite des chances, individualisme, libre entreprise). C'est pourtant la variante la plus
   directe de A12, et elle ne coute qu'un changement d'invite.

5. **Personne n'a mesure l'heterogeneite intra minorite en simulation.** 05-20 signale en
   passant que la sur extremite est maximale chez les republicains noirs non hispaniques ;
   personne n'en a fait un objet. Or c'est le cas ou l'ecart entre l'etiquette de groupe et la
   distribution reelle est le plus large (05-07, 05-51), donc celui ou une caricature se voit
   le mieux.

6. **Personne n'a repris la controverse Converse contre Achen du cote machine.** La question
   « l'incoherence d'un agent est elle une inattitude ou une erreur de mesure » a exactement la
   meme forme que la question de 1975, et le modele noir et blanc de Converse s'applique tel
   quel a un agent reinterroge trois fois.

---

## Ce que je n'ai pas pu verifier

1. **Les deux piliers de la these de l'asymetrie n'ont pas ete lus.** 05-39 (Jost et al. 2003)
   et 05-40 (Jost 2017) sont derriere paywall ; le PDF hebergee par un des auteurs renvoie une
   connexion refusee. Les r cites (0,50, 0,34, -0,32) proviennent d'un resume de recherche et
   non du texte. **Ils ne doivent pas etre repris dans un livrable sans verification.**

2. **Les livres n'ont pas ete consultes** : Zaller 1992, Kinder et Kalmoe 2017, Ellis et
   Stimson 2012, Hajnal et Lee 2011, Philpot 2017, White et Laird 2020. Pour Ellis et Stimson
   le chiffre du tiers est confirme dans l'article de 2009, qui le donne comme un renvoi au
   livre ; pour les autres, aucun chiffre n'est repris.

3. **Une dizaine d'articles centraux sont sous paywall et n'ont pas ete ouverts** : Zaller et
   Feldman 1992, Achen 1975, Feldman 1988, Feldman et Johnston 2014, Alvarez et Brehm 1995,
   Layman et Carsey 2002, Malka et al. 2014, DellaPosta 2020, Boutyline et Vaisey 2017, Hare
   et Poole 2014, Freeder et al. 2019, Broockman 2016, Kalmoe 2020. Unpaywall ne trouve aucune
   version libre pour douze d'entre eux. La consequence pratique est que **la partie
   « structure de l'incoherence » de la synthese repose sur des [PROBABLE]**, alors que la
   partie « dimensionnalite » et la partie « LLM » reposent sur des [CONFIRME].

4. **Deux chiffres de papiers lus n'ont pas pu etre extraits** parce qu'ils sont dans des
   balises mathematiques ou des figures : les scores de silhouette humains et agents de 05-30,
   et les tailles d'effet de l'ANOVA de 05-28. Ils sont decrits qualitativement et pas chiffres.

5. **Une divergence interne a une source n'est pas resolue.** 05-06 annonce 293 items du noyau
   dans son resume, 283 dans son corps et 276 dans sa conclusion. Les fiabilites citees
   (`partyid` 0,84, `polviews` 0,66) sont lues dans le corps et ne sont pas affectees, mais le
   denominateur du « 21 % au dessus de 0,85 » est incertain.

6. **La version publiee de 05-10 n'a pas ete lue**, seulement le preprint. L'ecart est faible
   (0,245 contre 0,254 pour le global) mais reel. Citer le preprint explicitement.

7. **05-23 n'a ete lu qu'en resume.** Son resultat d'asymetrie de reponse a l'etiquette est
   coherent avec 05-24, qui lui est [CONFIRME], mais il ne doit pas etre cite seul.

8. **Recherche web epuisee en cours de travail** (200 requetes). La derniere partie de la
   collecte s'est faite par les API publiques d'arXiv, OpenAlex, Unpaywall et Europe PMC. Des
   travaux recents sur l'heterogeneite intra camp mesuree chez les LLM ont donc pu etre
   manques, en particulier ceux publies apres juin 2026 hors arXiv.

---

## Cinq questions qu'un psychologue social peut trancher mieux que la litterature

**Q1. Le trait de deviance de A10 doit il etre abandonne au profit du conflit de valeurs ?**
La litterature ne connait pas de « propension a devier de son groupe » comme construit stable.
Elle connait l'ambivalence, le conflit de valeurs et la contre pression, qui se mesurent par
une variance conditionnelle et non par un ecart au mode. `a9` mesure un facteur unique qui
explique 31 pour cent de la communaute, dont la moitie disparait quand on retire l'instabilite
du repondant. **Est ce le meme objet sous un autre nom, ou une quantite sans referent
psychologique ?** Si c'est le second, A10 doit etre reformulee en termes de conflit de valeurs
et devient testable sur les items GSS ci dessus.

**Q2. Quelle est la bonne cible chiffree de contre pression pour valider une simulation ?**
Sur ANES 2000, 44 pour cent des moderes et environ 36 pour cent des ideologues declares sont
hors de leur quadrant. Sur CCES 2010-2018, 20,7 pour cent de la population entiere est
incoherente au sens du melange. Ces deux chiffres ne mesurent pas la meme chose et le second
est calcule sur un modele. **Lequel un relecteur de psychologie sociale accepterait il comme
cible a atteindre pour une population simulee, et avec quelle tolerance ?**

**Q3. L'asymetrie de refus est elle un biais de mesure ou un fait a modeliser ?**
Un modele refuse plus sur les instructions conservatrices. Si un humain conservateur refuse
aussi plus souvent de repondre dans certaines enquetes, alors le refus differentiel est une
partie du phenomene humain et doit etre reproduit. Si ce n'est pas le cas, c'est un artefact
d'alignement qui contamine toutes nos mesures de dispersion par segment. **La litterature de
non reponse par ideologie tranche t elle ?**

**Q4. Combien de patrons de reponses distincts un echantillon humain de 150 personnes sur 10
items produit il, et quelle part de cette diversite est du bruit ?**
Le chiffre 19 contre 340 de 05-29 est le plus parlant du theme, mais il n'a pas de plancher.
Sur nos donnees, la vague 2 humaine permet de calculer combien de patrons **les memes
personnes** produisent a deux semaines. **Quelle statistique un psychometricien recommande t
il ici : nombre de patrons, entropie de la distribution des patrons, ou dimension intrinseque
a la maniere de 05-31 ?**

**Q5. Faut il conditionner sur trois valeurs fondamentales plutot que sur un trait latent
d'IRT ?**
A12 propose un trait latent estime par theorie de reponse a l'item. La litterature suggere une
alternative plus interpretable : conditionner sur deux a trois valeurs fondamentales en
conflit (egalite des chances, individualisme economique, libre entreprise), qui sont la source
theorique de l'incoherence et se mesurent avec des items existants du GSS. **Laquelle des deux
un psychologue social defendrait il devant un relecteur, sachant que la seconde produit un
conditionnement lisible en langage naturel et que la premiere produit un scalaire ?**
