# 06. Lecture complete : ce que l'alignement fait aux distributions, a la diversite, a la calibration

Chantier mene le 8 septembre 2026 selon `corpus/lecture-complete/00-CONSIGNE.md`, a partir des 42
entrees confirmees de `corpus/06-alignement-diversite-dicible.md` (errata du 8 septembre inclus),
des lectures integrales deja faites en `resultats/a26-collisions-2608-03044-et-2609-00565.md` et
`resultats/a27-lecture-2607-25292.md`, de `FAITS-ETABLIS.md` section 3 et de `ARBITRAGE.md`.

Methode appliquee : remontee et descente des citations par l'API Semantic Scholar
(`api.semanticscholar.org/graph/v1`, sans cle) et par l'API arXiv, sur les entrees pivots du theme
(06-01 Santurkar, 06-14 Kirk, 06-18 Verbalized Sampling, 06-20 Murthy, plus la piste Arditi laissee
ouverte en section 4 point 10 du fichier initial). Le budget de recherche par moteur generaliste
etait deja epuise a l'ouverture du chantier (200 requetes sur 200) ; toute la prospection s'est donc
faite par les deux API de citations et par l'API arXiv, ce qui est exactement ce que la consigne
demande. Aucun fichier existant n'a ete modifie.

**Etat de la lecture. 25 references nouvelles entrees dans la table, dont 14 lues au texte integral
ou sur la totalite de leurs sections de resultats** (PDF officiels convertis avec `pdftotext
-layout`), 9 lues au resume seul, 2 au titre seul. Le chantier s'est arrete quand les citations
avales des quatre pivots ont cesse de rendre des objets nouveaux : les trois dernieres vagues ne
ramenaient plus que des variantes de correctifs de decodage sans referent humain.

**Convention de certitude.** Identique au fichier initial. [CONFIRME] veut dire que le corps du
papier a ete ouvert, et la cellule dit quelles sections. Quand une valeur n'existe qu'en figure,
c'est dit dans la cellule et repris en section 6.

**Convention de la colonne « trouve par ».** `table initiale` pour les 42 entrees de
`corpus/06-alignement-diversite-dicible.md`, qui ne sont pas recopiees ici et restent lisibles la
bas ; `citation aval de 06-NN` quand la reference cite une entree de la table initiale et a ete
trouvee par l'API de citations ; `citation amont de X` quand elle est citee par X ; `API arXiv`
quand elle vient d'une requete de mots clefs sur l'API arXiv, faute de moteur generaliste
disponible. Les entrees nouvelles sont numerotees a partir de 06-43.

**Regle de forme.** Francais, aucun tiret cadratin ni demi cadratin, citations exactes en anglais,
decimales a la virgule.

---

## 1. La table etendue

Les lignes 06-01 a 06-42 sont dans `corpus/06-alignement-diversite-dicible.md`, colonne « trouve
par » = `table initiale`, avec les trois corrections de l'errata du 8 septembre. Les lignes
ci dessous sont les entrees ajoutees par ce chantier.

| id | reference | question posee | donnees | modeles | mesure exacte | resultat chiffre principal | faille ou limite | rapport a la these | certitude | trouve par |
|---|---|---|---|---|---|---|---|---|---|---|
| 06-43 | GX-Chen, Prakash, Guo, Fergus, Ranganath 2025, arXiv 2510.20817, « KL-Regularized Reinforcement Learning is Designed to Mode Collapse » | L'objectif optimise par le post entrainement a recompense a t il seulement une solution diverse ? | Simulations didactiques ; tache verifiable 1 ou 2 ; WildChat ; modeles chimiques de langue | Qwen2.5-3B, Qwen3-1.7B, modeles chimiques REINVENT | Forme de la distribution optimale de `J = E[R] moins beta D(pi, pi_ref)`, pour KL inverse et KL directe ; entropie de reponse valide ; EAD, diversite semantique | Remarque 4.2 : a support egal dans la reference, le rapport des probabilites finales vaut `exp((R1 moins R2)/beta)` ; pour un ecart de recompense de 0,1 et un `beta = 1e-3` courant, **l'echantillon le mieux recompense devient 2,6 fois 10 puissance 43 plus probable**. Remarque 4.3 : a **recompense egale**, le rapport des probabilites finales vaut exactement le rapport des probabilites dans la reference, **independamment de beta** ; donc « RL with any KL-regularization does not increase the relative probability of lower-support samples to high-support ones, as long as their rewards are the same ». Leur correctif MARA (deux lignes) porte Mean Distinct de 3,88 (RLOO) et 3,96 (GRPO) a 4,62, au dessus du modele de base a 4,01, sans perte de recompense hors distribution (1,604 contre 1,317) | Modeles petits ; la partie LLM est une tache jouet a deux reponses plus une tache creative ; aucune enquete, aucun referent humain | **Soutient, et c'est le mecanisme formel qui manquait au theme.** Il donne la raison mathematique pour laquelle un modele aligne rend la reponse la plus typique du groupe : a qualite egale entre deux reponses, l'optimisation **recopie le rapport de frequences du modele de base** et ne remonte jamais une reponse rare. C'est la formulation exacte de notre substitution personne vers groupe, au niveau de l'objectif | [CONFIRME] PDF lu, sections 1 a 6, remarques 3.1 a 4.4, tables 1 et 2 | API arXiv (`mode-seeking` et `RLHF`), et citation aval de 06-14 |
| 06-44 | Banayeeanzade, Yang, Tarsadiya, Bahrani, Blas, Samuel, Jia, Razaviyayn, Karimireddy 2026, arXiv 2605.11128, « Sampling More, Getting Less : Calibration is the Diversity Bottleneck in LLMs » | La perte de diversite est elle un defaut de decodage ou un defaut de calibration de la distribution ? | Taches a ensemble valide connu exactement (tirage de chiffres de longueur d, somme contrainte, nommer un Etat americain), plus NoveltyBench ; 10 graines | 14 modeles, familles Qwen-3, Llama-3, Olmo-3, sur 9 tailles **et etapes d'entrainement** | Deux calibrations : **ordre** (les jetons valides sont ils classes avant les invalides, mesure par precision et rappel locaux) et **forme** (concentration de la masse, mesuree par validite et par diversite = exponentielle de l'entropie normalisee par la taille de l'ensemble valide) | Theoreme 4.2 : les erreurs locales se composent multiplicativement, `Rec_seq(S) <= (1 moins delta) puissance moins C fois e puissance moins cm`. Theoreme 5.2 : sous decroissance geometrique de la distribution rangee, toute mise a l'echelle en temperature satisfait `Div(p) <= e puissance moins m c(epsilon)`, avec `c(epsilon)` qui tend vers `ln 2`. Filtre oracle de validite applique aux **deux premieres etapes seulement** : diversite d'embedding **0,40 plus ou moins 0,15** contre 0,33 pour top-k, 0,29 pour min-p, 0,25 pour top-p et 0,25 sans filtrage ; Self-BLEU 0,69 contre 0,86 | Le juge de validite est un modele ; les valeurs de la figure 4 (effet de la taille et de l'etape d'entrainement) ne sont pas tabulees ; taches de generation, pas d'enquete | **Soutient, et il ferme le trou que la section 3 point 2 du fichier initial declarait ouvert.** La litterature de la diversite et celle de la calibration sont ici jointes explicitement : la diversite est bornee par la calibration de la distribution conditionnelle. Notre jonction reste vraie mais doit se restreindre a **la calibration au sens de l'enquete**, probabilite annoncee contre frequence realisee sur des modalites, qu'ils ne mesurent pas | [CONFIRME] PDF lu, sections 1 a 6, theoremes 4.2 et 5.2, table 1 | citation aval de 06-18 |
| 06-45 | « More Is Not More : What Matters for Diversity in LLM Opinions ? » 2026, arXiv 2607.20429 | Quel type d'intervention augmente reellement la diversite d'opinion d'une population simulee ? | 100 questions ouvertes de vrais utilisateurs ; extraction d'opinions atomiques par un appel a temperature 0, precision 98,2 pour cent | 7 modeles (dont Gemini, Kimi, GPT-mini, Qwen) | Plan factoriel a deux facteurs : **profondeur de persona** a 5 niveaux (None, Role, Basic, Mid, Pro) fois **architecture d'interaction** (appel unique, multi tours, multi agents). Alpha diversite par distance moyenne entre paires (MPD), richesse de categories rarefiee (CC), score de Vendi ; beta diversite par beta-VS et par taux de grappes uniques (UCR). Wilcoxon apparie, delta de Cliff, correction de Benjamini Hochberg | **Le premier pas de conditionnement fait presque tout le gain** : une seule phrase de profession (Role) donne `delta >= 0,62` sur les 7 modeles. **Ajouter les attributs demographiques par dessus (Basic) n'ameliore pas et degrade sur trois modeles**, Gemini, Kimi, GPT-mini (`delta = +0,60 a +0,72`, Role superieur a Basic). Basic vers Mid : `+0,004` de MPD en moyenne, « approximately 60 additional words of structured demographic information contribute almost nothing ». Les 4 astuces bon marche sont marginales : Role vaut environ **2,5 fois** le meilleur des bas couts ; l'assignation de trait vaut **37 pour cent** de Role ; la temperature est « particularly uninstructive ». **La largeur du vivier bat la profondeur** : 20 personas partages en 4 groupes donnent un UCR inter groupes de **59 a 82 pour cent**. Multi tours et multi agents couvrent des regions disjointes, UCR excedentaire d'environ **50 pour cent** au dessus du plancher de 30 pour cent | Aucun referent humain : toutes les mesures sont modele contre modele ; questions ouvertes, pas de nomenclature fermee ; le decompte d'opinions passe par un extracteur automatique | **Soutient directement notre resultat d'etiquette, et l'elargit.** Ils mesurent, sur 7 modeles et 100 questions, que **l'ajout d'attributs demographiques a une identite deja posee reduit la diversite** sur trois modeles sur sept. Notre a19 et a23 mesurent le meme signe sur l'axe ideologique avec un referent humain, ce qu'ils n'ont pas. Leur phrase « the key driver of diversity is identity differentiation itself, not the volume or realism of the persona description » est la formulation la plus proche de notre conclusion de conditionnement | [CONFIRME] PDF lu, sections 3 a 5, figures 4 a 6 | citation aval de 06-18 et de 06-20 |
| 06-46 | Samuel et al. 2026, arXiv 2605.30021, « Recovering Diversity Without Losing Alignment : A DPO Recipe for Post-Trained LLMs » (REDIPO) | Peut on reintroduire par des donnees de preference la diversite que le modele de base possedait ? | NoveltyBench, MTBench, IFEval, HarmBench, Arena-Hard | **Qwen3-4B**, OLMo-3-7B, LLaMA-3.1-8B, chacun en base, instruct, DPO, DivPO, REDIPO | `distinct_k` de NoveltyBench ; scores de qualite et de securite ; IC bootstrap a 95 pour cent, 1 000 retirages | Table 1, colonne NoveltyBench. **Qwen3-4B : base 8,780 plus ou moins 0,295, instruct 2,560 plus ou moins 0,390**, soit **29,2 pour cent de la diversite du modele de base conservee**, facteur 3,43. OLMo-3-7B : 8,170 vers 5,570, soit 68,2 pour cent. LLaMA-3.1-8B : 8,790 vers 5,160, soit 58,7 pour cent. DPO et DivPO ne restaurent rien (2,560 et 2,570 sur Qwen3-4B) ; REDIPO porte Qwen3-4B a **6,000**, soit 68,3 pour cent du socle, avec MTBench 7,044 contre 7,450 et HarmBench qui **baisse** de 0,042 a 0,029 | Generation ouverte, aucune enquete, aucun referent humain ; `distinct_k` est une metrique de banc ; demande un entrainement DPO complet, hors de notre budget | **Soutient, et c'est la ligne chiffree la plus proche de notre materiel.** C'est la seule mesure publiee d'un ecart base contre instruct **sur Qwen3-4B**, et elle dit que cette famille perd davantage que les deux autres (29 pour cent conserve contre 59 et 68). Cela pese sur la question ouverte de FAITS-ETABLIS section 7 : notre modele n'est pas un modele moyen sur cet axe | [CONFIRME] PDF lu, sections 2 a 3.4, table 1 | citation aval de 06-18 et de 06-20 |
| 06-47 | « Argument Collapse : LLMs Flatten Long-Form Public Debate » 2026, arXiv 2606.01736 | Les modeles convergent ils vers un petit ensemble d'arguments, et lesquels perdent ils ? | **1 039 reponses humaines de 195 debats du New York Times**, 448 reponses humaines de 61 forums de la Boston Review, **23 381 essais produits par modele** ; trois regimes : vanilla, diversified, position-guided | 5 modeles frontieres (GPT, Claude, Gemini, DeepSeek, Minimax) | Taux d'arguments principaux uniques dans un debat ; taux de recouvrement des grappes d'arguments humains ; taux de sous arguments uniques ; preferences de 6 evaluateurs (Skywork-Reward-V2, ArmoRM, MT-Bench, WildBench, qualite d'argument, Writing RM) | **65,3 pour cent des arguments principaux humains sont uniques dans leur debat, contre 3,4 pour cent chez les modeles.** Un modele diversifie ne recouvre que **50 pour cent (Claude) a 55 pour cent (Gemini)** des grappes d'arguments humains ; **la mise en commun des 5 modeles monte a 73,9 pour cent, mais de facon selective : les arguments portes par plusieurs humains sont recouverts 98,1 pour cent du temps, ceux portes par un seul humain 67,8 pour cent**. Sous arguments : **9,1 pour cent d'uniques chez les modeles contre 41,0 pour cent chez les humains**, 22,9 pour cent en diversified. Sur les six forums posterieurs a la coupure de trois modeles, le motif tient : humains 84,0 pour cent d'uniques, vanilla 35,6, diversified 53,8. **Les six evaluateurs preferent l'argument partage a l'argument rare**, jusqu'a 74,7 pour cent (Skywork-V2) et 67,0 pour cent (ArmoRM) sur les essais humains | Essais argumentatifs, pas de reponses d'enquete ; l'appariement des arguments passe par des juges modeles ; le referent humain est un corpus edite, donc deja filtre | **Soutient, et c'est la meilleure preuve directe que ce qui disparait est le rare, avec referent humain.** Le couple 98,1 contre 67,8 est la version mesuree de « la simulation efface les minorites d'opinion » de `ARBITRAGE.md`, sur un autre objet. Et la preference des modeles de recompense pour l'argument partage donne le maillon de recompense qui manquait entre 06-18 et 06-11 | [CONFIRME] PDF lu, sections 2 a 4.2 et table 3 | citation aval de 06-18 |
| 06-48 | Fafula 2026, arXiv 2607.17427, « Abliteration Is Not a Scalpel : Off-Target Effects of Refusal Removal on Decision Disposition Across Model Families » | Retirer la direction de refus d'un modele change t il ce qu'il exprime en dehors du refus ? | **21 600 decisions** sous incertitude : paris hebdomadaires a la hausse ou a la baisse sur 60 actions de la Bourse de Varsovie, 18 semaines, pipeline gele, une invite figee octet pour octet ; preenregistrement | Deux paires de meme provenance, **Gemma-4-26B-A4B-it** et **Qwen3-30B-A3B-Instruct-2507**, chacune contre sa version abliterée par le meme auteur (huihui-ai), checkpoints BF16 officiels | Taux d'optimisme, confiance moyenne declaree, longueur de justification, lexiques d'incertitude et de concession, unanimite entre echantillons ; bootstrap par grappes sur les 18 semaines, N = 5 000 | **La tache ne declenche aucun refus, donc tout ecart est un effet collateral pur.** Optimisme : **plus 12,2 points (IC [+8,5 ; +16,0]) sur Gemma et plus 7,4 (IC [+5,0 ; +9,7]) sur Qwen**. Verbosite de la justification : plus 4,0 et plus 7,4 mots. Lexique d'incertitude pour 100 mots : **3,68 vers 2,73 (moins 0,95) sur Gemma, 3,46 vers 1,29 (moins 2,17) sur Qwen**. Confiance declaree : **signes opposes**, moins 0,008 sur Gemma et plus 0,109 sur Qwen, IC de famille disjoints. **Unanimite entre echantillons de 91 a 95 pour cent dans les quatre bras**, taux de retournement de 5 a 9 pour cent : l'abliteration ne rend aucune variance par appel. Aucun bras ne bat le marche | Une seule tache, financiere, non liee a l'opinion politique ; un seul auteur d'abliteration ; deux familles | **Soutient, et c'est la seule mesure publiee de ce que l'abliteration fait aux enonces exprimes.** Trois consequences pour nous. Un, l'abliteration **deplace la position** (optimisme, vocabulaire du doute) **sans restaurer la dispersion**, ce qui la disqualifie comme correctif de notre deficit. Deux, le sens du deplacement de confiance **depend de la famille**, donc rien ne se transpose d'un modele a l'autre. Trois, leur audit de provenance a trouve **deux canaux de contamination**, un quantificateur mal apparie et un gabarit de conversation communautaire perime, avec la conclusion « studies that do not verify rendered prompts token-for-token can silently measure the template, not the intervention » : c'est notre risque exact en GGUF Q4_K_M | [CONFIRME] PDF lu, sections 3 a 5, tables et figures 1 a 5 | API arXiv (`abliteration`) |
| 06-49 | « Is Convergence Inevitable ? Tracing Output Homogeneity Back to Base Models » 2026, arXiv 2608.11426 | L'homogeneite nait elle a l'alignement ou avant ? | INFINITY-CHAT 100 (100 requetes ouvertes), 50 reponses par requete, top-p 0,9, temperature 1,0 ; plus une version de LIMA augmentee de metaphores (950 echantillons) | Suites completes Tulu 3 (8B, 70B) et OLMo 3 (7B, 32B) aux etapes SFT, DPO, RLVR ; Llama-3.1 8B base pour les injections LoRA ; Llama 3.1 8B, Olmo 3 7B, Qwen3 8B comme socles | Similarite cosinus moyenne entre paires de reponses a une meme requete (`text-embedding-3-small`) ; frequence du vehicule dominant dans une tache de metaphore ; trois regimes d'invite sur socle : completion nue, trois exemples, gabarit d'assistant | **La convergence est deja installee apres le SFT** : distribution fortement decalee a droite, masse au dessus de 0,7 de similarite moyenne ; DPO et RLVR ne deplacent la moyenne que modestement. **L'injection SFT amplifie mais n'introduit pas** : injecter le vehicule le plus frequent le porte a **48 a 92 pour cent**, le sixieme plus frequent a **1 a 12 pour cent**, et **les vehicules absents de la distribution initiale (champ lexical alimentaire) echouent tous** ; il faut 5 a 7 occurrences pour imposer un vehicule invraisemblable. **Sur les socles, la convergence s'obtient par l'invite seule** : la completion nue donne des vehicules varies, les trois exemples et surtout le prefixe d'assistant `Sure! Happy to help.` produisent « the most homogeneous answers », avec une similarite intra vehicule de **0,69 a 0,91**. « Qwen3 requires less guidance to converge, possibly reflecting greater exposure to instruct-like samples during pretraining » | Une seule famille de taches (metaphores) pour la partie causale ; similarite d'embeddings ; les valeurs des figures 1, 4, 7, 8 ne sont pas tabulees ; aucun referent humain | **Soutient, et c'est le maillon amont qui manquait a la chaine causale.** Il repond a la question que 06-22 et 06-24 laissaient ouverte, en disant qu'aucune des deux etapes n'est coupable : le SFT est un **revelateur** proportionnel a la frequence deja presente. Consequence directe et couteuse pour nous : **notre E2 n'est pas un controle de format, c'est une variable de premier ordre**, puisque le seul prefixe d'assistant sur un socle reproduit l'effondrement ; et le fait que Qwen converge avec moins de guidage vise notre famille de modeles | [CONFIRME] PDF lu, sections 1 a 6 | citation aval de 06-20 |
| 06-50 | Lu et al. 2025, arXiv 2506.17871, « LLM Probability Concentration : How Alignment Shrinks the Generative Horizon » | De combien l'alignement resserre t il l'espace des continuations, et cet effet domine t il les autres facteurs ? | MMLU-STEM, Cognac, BBCLatestNews, generation d'histoires, chaines aleatoires, Just-Eval-Instruct ; M = 50 sequences par estimation | Familles Llama-2, Llama-3, Llama-3.1, OLMo-2, DeepSeek-distilles, en base et en aligne | **Branching Factor (BF)**, nombre effectif de branches plausibles, exponentielle de l'entropie normalisee par la longueur ; analyse de Pareto des facteurs (alignement, taille, generation, complexite d'invite) | **L'alignement reduit le BF d'un facteur 2 a 5 globalement, et jusqu'a un ordre de grandeur en debut de sortie (de 12 a 1,2)** ; le rapport base sur aligne culmine a **10 fois** sur les chaines aleatoires et est le plus faible sur OLMo-2. Analyse de Pareto : **l'alignement franchit ou approche le seuil de 80 pour cent d'impact cumule sur toutes les taches, loin devant la taille, la generation et la complexite d'invite**. Table 1, MMLU-STEM, chute relative maximale quand on quitte le decodage par defaut : **Llama-3-70B-Instruct 3,31 pour cent contre Llama-3-70B 18,59 ; Llama-3.1-8B-Instruct 19,84 contre Llama-3.1-8B 31,48**. Nudging : conditionner un socle 70B par un prefixe de style aligne produit par un 8B aligne suffit a faire chuter le BF, surtout en debut de generation | Taches de generation, pas d'enquete ; le BF est une entropie exponentiee, donc il ne dit rien de la justesse ; les valeurs de la figure 4a sont en carte de chaleur | **Soutient, et il chiffre le point qui nous interesse le plus : l'insensibilite au decodage.** La table 1 est la version publiee de notre a4 sur le bridage thermique : **un modele aligne perd 3 a 20 pour cent quand on ouvre le decodage, un socle en perd jusqu'a 31**, parce qu'il y a des branches a ouvrir. Et l'hypothese du nudging rejoint 06-49 : l'alignement ne cree pas la trajectoire pauvre, il oriente vers un jeton de style qui la debloque | [CONFIRME] PDF lu, sections 1, 3, 4 et 5, table 1, figure 6 | citation aval de 06-20 |
| 06-51 | « Narrative Flattening : How Post-Training Compresses Thematic, Affective, and Stylistic Variation in LLM Fiction » 2026, arXiv 2605.27878 | A quelle etape du post entrainement la variation se perd elle, quand on a un referent humain apparie ? | Trois corpus humains : The New Yorker (3 023 nouvelles), TMAS (230), StoryStar (100) ; continuations appariees, quatre points de coupe | **Quatre points de controle OLMo 32B de la meme lignee : Base, SFT, DPO, RLVR**, architecture, echelle, tokenizer et pre entrainement partages | Trois axes : coefficient de variation des sauts semantiques phrase a phrase (`text-embedding-3-large`), prevalence affective (GoEmotions adapte, 28 classes), diversite linguistique par MMD aux plongements de style et variance inter histoires | **Mouvement thematique, CV par histoire** : humains environ 0,105, **Base 0,096 (moins 8,0 pour cent), SFT 0,089 (moins 15,1), DPO et RLVR 0,081 (moins 22,2)**, effet mixte confirme `beta = moins 0,0228`, IC [moins 0,0234 ; moins 0,0222], p inferieur a 0,001. **Style, table 3** : MMD au carre a l'humain **0,25 (Base), 0,41 (SFT, plus 64 pour cent), 0,53 (DPO, plus 112), 0,52 (RLVR, plus 108)** ; variance inter histoires rapportee a l'humain **6,03 (Base), 0,84 (SFT, moins 86 pour cent), 0,49 (DPO, moins 92), 0,52 (RLVR, moins 91)**. **Affect** : le socle est deja **mal centre**, conflit environ 47 pour cent et surprise curiosite environ 33 contre 20 et 21 chez les humains, neutre 13 contre 29 ; a RLVR, conflit environ 7,5, surprise curiosite environ 13, neutre environ 45, « each marker now further from the human distribution than the base model was, in the opposite direction ». **Ecarts entre domaines** : etendue du CV thematique **0,0116 (humains) vers 0,0037 (RLVR), moins 62 pour cent** ; etendue affective **17,8 vers 3,3 points, moins 81 pour cent** ; MMD au carre inter domaines **0,61 chez les humains contre 0,01 au maximum a RLVR** | Fiction, pas d'enquete ; le referent humain est un corpus edite ; les valeurs des figures 2 a 4 sont partiellement en figure | **Soutient, et c'est le meilleur gradient par etape avec referent humain de tout le theme.** Deux enseignements durs pour nous. Un, **le modele de base n'est pas un bon simulateur, il est sur disperse et mal centre** : sa variance vaut 6,03 fois celle des humains et son affect est deja hors cible. Deux, **le post entrainement ne ramene pas vers l'humain, il depasse l'humain dans l'autre sens**. Cela oblige a reecrire la question de `ARBITRAGE.md` option C : ce n'est pas « base ou aligne », c'est « de quel cote du referent humain chacun tombe » | [CONFIRME] PDF lu, sections 3 a 5, tables 1 a 3 | citation aval de 06-20 |
| 06-52 | « Distribution-First Population Simulation : Collapse, Calibration, and Recall in Non-WEIRD LLM Persona Modeling » 2026, arXiv 2607.18310 | Que fait la calibration par verbalisation a une population simulee, et jusqu'ou peut on lui faire confiance ? | Microdonnees reelles de la World Values Survey, **2 414 repondants turcs** ; 16 scenarios en 3 classes structurelles ; 4 scenarios fois 5 graines ; une tache agentique de reservation ; un backtest electoral national | Qwen3.6-35B (MoE), GLM-5.2, Gemma-4-26B | Concentration (masse modale), entropie de Shannon, distance de variation totale, **rapport d'ecarts types modele sur humain (SD-ratio)** ; controle placebo ; attaque de memorisation | **Agents independants** : concentration 0,358 [0,345 ; 0,374] en route distribution contre **0,685 [0,614 ; 0,764]** en route agents ; entropie 1,464 contre **0,770** ; TVD 0,437 [0,383 ; 0,498] ; **taux d'effondrement 85 pour cent**. **Verbalized Sampling** : fidelite plus 10,1 (GLM-5.2), plus 6,8 (Qwen3.6-35B, p = 0,002, d = 6,2), plus 8,2 (Gemma-4-26B) ; **mais le SD-ratio passe de 0,46, 0,56 et 0,40 a 1,26, 1,36 et 1,37**, c'est a dire de la sous dispersion a la sur dispersion, « a structural over-corrector ». **Backtest electoral** : la route agents ancres porte la part du premier parti de **42,6 pour cent reels a 88,0 pour cent predits, TVD = 0,454**, dans tous les modeles et tous les modes ; la route distribution atteint TVD = 0,051 mais « this is plain recall, not simulation ». **Placebo** : la manipulation non pertinente deplace l'opinion de plus 1,49 contre plus 1,13 pour la manipulation pertinente, donc la sensibilite contrefactuelle est non specifique | Un pays, 16 scenarios, trois modeles ; le verificateur est deterministe mais construit par les auteurs ; le backtest porte sur un resultat anterieur a la coupure | **Soutient, et c'est le papier le plus dangereux pour la famille B du plan de a18 et pour toute restauration de variance.** Il mesure ce que le fichier initial demandait en E5 et E6 : **la recalibration repare la dispersion en la depassant**, 0,4 vers 1,37, et **ce qu'elle gagne au niveau agrege, elle le perd au niveau des sous groupes**, contamine par le rappel. Le 42,6 vers 88,0 est la meme substitution que la notre, avec un referent exterieur verifiable | [CONFIRME] PDF lu, sections 4 a 8, tables 1 a 4 | citation aval de 06-01 |
| 06-53 | « From Demographics to Survey Anchors : Evaluating LLM Agents for Modeling Retirement Attitudes » 2026, arXiv 2605.16303 | Une etiquette demographique suffit elle a definir un agent qui predit une reponse d'enquete ? | SHARE vague 9 (2021-2022), **N = 5 461 participants**, France, Allemagne, Espagne ; 15 questions de 3 construits de finances personnelles | **Qwen3-14B quantifie** en principal, plusieurs LLM locaux en exploratoire ; foret aleatoire comme reference supervisee | Distance de variation totale entre distribution generee et distribution reelle, par question ; replication d'une regression hierarchique publiee | Agents demographiques a 7 attributs contre agents ancres sur des reponses d'enquete : **TVD moyenne 0,422 contre 0,280, ecart moyen moins 0,142 (moins 29,02 pour cent), IC a 95 pour cent [moins 0,1516 ; moins 0,1309]**, avantage aux agents ancres sur 12 questions sur 15. Trois defauts nommes des agents demographiques : **biais de tendance centrale** (surestiment les modalites rares, sous estiment la modalite majoritaire, mais sur une distribution globalement resserree), **hyper exactitude** (sur la question d'interets composes ils rendent la bonne reponse, 2 420 euros, a « nearly 100% frequency », la ou les humains se trompent), et **absence de « je ne sais pas »**. Sensibilite au format : reponse ouverte sur 0 a 100 contre modalites discretes, distributions differentes, biais de sous estimation persistant. Les agents demographiques reproduisent les trois effets principaux de la regression publiee **mais pas leur interaction** | Un domaine, trois pays, 15 questions ; un modele quantifie principal ; la comparaison n'est pas base contre instruct | **Soutient, et c'est la mesure d'enquete la plus proche de notre design.** Il donne un nom a ce que nous avons mesure sans le nommer : l'agent defini par etiquette **substitue au repondant une version corrigee de son groupe**, qui ne se trompe pas et qui ne dit jamais « je ne sais pas ». Notre trou de non reponse, signale en section 3 point 5 du fichier initial, est ici documente comme une absence pure | [CONFIRME] PDF lu, sections 3 a 4.1.6, tables de TVD par question | citation aval de 06-20 |
| 06-54 | « Beyond Alignment : Value Diversity as a Collective Property in Multicultural Agent Systems » 2026, arXiv 2606.05985 | La diversite de valeurs d'un systeme d'agents est elle predite par son alignement ? | World Values Survey, **19 cultures**, questions a choix ferme ; systemes multi agents de tailles variees ; etude de cas de budget participatif | **18 modeles de fond**, dont GPT-5.4, Claude Opus 4.7, Gemini 2.5 Pro, Grok, **Qwen3-32B, Qwen2.5-32B-Instruct, Qwen3.5-27B**, Llama 3.1 et 4 | Alignement agent vers humain ; **diversite de valeurs** systemique, par paires et par arbre couvrant minimal sur le graphe de dissimilarite entre agents conditionnes sur des cultures differentes | **Reference humaine 44,07 par paires et 39,37 en structurel ; meilleur systeme, gemini-2.5-pro, 36,12 et 29,60 ; Qwen3-32B 24,61 et 18,97 ; Qwen2.5-32B-Instruct 20,44 et 16,19**, le plus bas de la table. **Alignement et diversite ne sont pas correles, Pearson r = moins 0,12** sur l'ensemble des systemes. Les fonds melanges reduisent l'ecart sans le combler ; l'interaction sociale erode encore la diversite en poussant au consensus | Diversite definie **entre cultures**, donc un terme inter, jamais intra ; 19 cultures seulement ; aucun plancher de bruit humain | **Soutient, et confirme la lecture de a26 sur le compromis.** Sur 18 modeles, la correlation alignement contre diversite est de moins 0,12 : **le « trade-off » du titre de 2609.00565 n'est pas une contrainte, c'est une trajectoire**, ce que a26 avait deduit de leur seule annexe F. C'est desormais mesure independamment. Et la table donne un ordre : les modeles Qwen sont dans le tiers le moins divers | [CONFIRME] PDF lu, sections 3 a 4, table 1 | citation aval de 06-20 |
| 06-55 | « Group Alignment-Induced Sycophancy : A Two-Sided Evaluation of Steerable Pluralistic Alignment » 2026, arXiv 2608.11528 | Aligner un modele sur un groupe demographique coute t il quelque chose, et le meme budget profite t il a tous les groupes ? | OpinionQA (Santurkar) pour l'alignement ; TriviaQA et TruthfulQA (1 002 questions) et un banc « are-you-sure » (1 000 questions) pour la sycophancie ; 200 messages Reddit filtres pour l'inferabilite | Qwen-2.5-3B, Qwen-2.5-7B, Llama-3.1-8B, OLMo-3-7B, fois **13 groupes demographiques** (politique, genre, education, revenu, statut matrimonial), fois 3 methodes (invite, SFT, DPO) = **156 bras** a budget apparie par axe | Gain d'accord avec le mode du groupe sur questions retenues ; **decalage** de sept metriques sociales et de sycophancie, mesure contre le bras non conditionne du meme modele ; bootstrap a 1 000 retirages, test de McNemar | « A matched budget does not move these models uniformly ; it redistributes ». **Chaque groupe progresse, et chaque ecart se creuse** : sur les axes politique, genre et statut matrimonial, les IC a 95 pour cent des contrastes de gain excluent zero ; sur education et revenu, non. Le decalage de sycophancie forme un profil **specifique au groupe et a la metrique**, pas un deplacement unidimensionnel. Le DPO obtient les gains les plus grands et les plus constants, l'invite seule sert de plancher, « a single demographic label where the parametric arms receive tens of thousands of respondent-derived preferences » | Les gains sont des accords au mode du groupe, pas des amplitudes d'ecart entre groupes ; les juges sociaux sont un modele ; les valeurs par groupe sont en figure 3 | **Soutient, et ouvre un terme que nous n'avons pas.** Ils mesurent l'**inegalite du gain de fidelite entre groupes**, quand nous mesurons l'amplitude de l'ecart entre groupes. Les deux sont complementaires et personne ne les met cote a cote. Leur plancher « invite seule » est litteralement notre condition avec etiquette : ils la traitent comme la borne basse de ce qu'une etiquette peut deplacer | [CONFIRME] PDF lu, sections 3 a 4.1 ; valeurs par groupe lues en figure | citation aval de 06-01 |
| 06-56 | Arditi, Obeso, Syed, Paleka, Panickssery, Gurnee, Nanda 2024, arXiv 2406.11717, « Refusal in Language Models Is Mediated by a Single Direction » | Le refus est il porte par une structure simple des activations ? | Jeux d'instructions nuisibles et inoffensives | 13 modeles de discussion ouverts jusqu'a 72B | Direction unique dans le flux residuel ; effet de son effacement et de son ajout | « refusal is mediated by a one-dimensional subspace, across 13 popular open-source chat models » ; effacer la direction empeche le refus d'instructions nuisibles, l'ajouter provoque le refus d'instructions inoffensives ; le jailbreak en boite blanche qui en decoule a « minimal effect on other capabilities » | Le papier mesure le refus, pas l'opinion ; l'affirmation d'effet minimal sur les autres capacites est contredite en aval, voir 06-48 et 06-57 | **Soutient indirectement, et c'est l'amont technique de l'abliteration.** Il donne la raison pour laquelle le curseur securite et refus de 06-35 et 06-36 est **un seul curseur** : il est litteralement unidimensionnel. Pour nous, il ferme la piste que la section 4 point 10 du fichier initial laissait ouverte | [CONFIRME] resume et enonces principaux lus ; corps non lu en entier | citation amont de 06-48, piste repertoriee non ouverte du fichier initial |
| 06-57 | « Comparative Analysis of LLM Abliteration Methods : A Cross-Architecture Evaluation » 2025, arXiv 2512.13655 | Les outils d'abliteration publics ont ils le meme cout collateral ? | GSM8K et bancs de capacite | **16 modeles instruits de 7B a 14B**, quatre outils (Heretic, DECCP, ErisForge, FailSpy) | Variation de GSM8K en points, divergence KL a la distribution d'origine | Les methodes a passe unique preservent le mieux : GSM8K moins 0,28 point (ErisForge) et moins 0,13 (DECCP) en moyenne sur trois modeles ; l'abliteration optimisee bayesiennement donne une **divergence KL de 0,043 a 1,646** ; sur l'ensemble, la variation de GSM8K va de **plus 1,51 a moins 18,81 points, soit moins 26,5 pour cent en relatif**, selon l'outil et l'architecture | Bancs de capacite, aucune mesure d'opinion ni de distribution de reponses ; sous ensembles differents par outil | **Muet sur la these, decisif sur la methode.** Il chiffre ce que 06-56 minimise : le cout collateral de l'abliteration va jusqu'a moins 26,5 pour cent sur une capacite, et **la divergence KL a la distribution d'origine varie d'un facteur 38 selon l'outil**. Toute experience popsim sur un modele non censure devrait donc nommer l'outil, pas seulement le modele | [PROBABLE] resume lu, corps non ouvert | citation aval de 06-56 |
| 06-58 | Wright, Ruas et al. 2025, arXiv 2510.04226, « What and Whose Knowledge ? Measuring Epistemic Diversity in Large Language Models » | La diversite des affirmations produites par les modeles a t elle une reference exterieure ? | 155 sujets, 12 pays, **1,7 million de reponses et 70 millions d'affirmations** ; reference : jusqu'aux 40 premiers resultats Google par sujet | **27 modeles** sur trois ans, en memoire parametrique et en RAG | Diversite de Hill Shannon (HSD) sur les affirmations rarefiees ; modeles lineaires a effets mixtes | La diversite epistemique a **augmente** sur trois ans, mais **tout modele reste sous la reference de recherche** : « search is at least 18.7% more diverse than our best model (GPT-5) », HSD moyenne **3 110 contre 2 621**. Le RAG augmente significativement la diversite ; **les grands modeles sont moins divers que les petits** ; la connaissance parametrique privilegie l'anglais sur la langue locale pour les sujets propres a un pays | Affirmations extraites automatiquement ; la reference de recherche est faible et les auteurs le disent ; pas d'enquete, pas d'opinion individuelle | **Soutient, et fournit une reference exterieure non humaine mais non modele.** Deux points utiles. Un, il replique sur un troisieme objet l'effet d'echelle inverse de 06-28 : plus gros ne veut pas dire plus divers. Deux, la piste RAG est la seule intervention du theme qui augmente la diversite sans toucher aux poids ni au decodage, ce qui la rend comparable a notre famille B | [CONFIRME] PDF lu, sections 6.3 et 6.4 ; le reste au resume | citation aval de 06-20 |
| 06-59 | « Where Models Converge and Humans Diverge : A Coverage Framework for Distributional Pluralism in Open-Ended Generation » 2026, arXiv 2608.05576 | Comment mesurer la largeur distributionnelle d'un contenu produit par modele, avec un referent humain ? | Taches d'ideation et de narration, distribution empirique de reponses humaines par sujet | Non lu | Deux mesures : LLM Coverage (LLM-Cov) et In-Boundary Rate (IBR), qui separent la plausibilite de la largeur | « current LLMs produce plausible but narrow content that concentrates near the center of the human response space » | Non lu au dela du resume ; generation ouverte | **Soutient, et propose la separation dont nous avons besoin** : plausible et large ne sont pas la meme chose. C'est le vocabulaire manquant pour repondre a l'objection de 06-26 sans passer par un seuil de qualite arbitraire | [PROBABLE] resume lu | citation aval de 06-01 |
| 06-60 | « Benchmarking large language model agent societies against human behavioural distributions » 2026, arXiv 2608.28182 (SILICA) | Une societe d'agents reproduit elle les distributions humaines publiees, et resiste t elle aux perturbations ? | Cinq environnements a ancrage humain publie, plus perturbations et variantes a paiements deplaces | **12 modeles a poids ouverts**, sur une seule carte graphique grand public | Marges d'equivalence aux ancrages humains ; effet des permutations | « Agreement with human data is confined to starting points » : les contributions du premier tour tombent dans la marge d'equivalence pour 8 modeles sur 11, **aucun modele ne reproduit l'etat final** ; **permuter l'ordre de deux actions coute a un modele 58 points de cooperation** ; seul le modele entraine au raisonnement place son seuil d'acceptation la ou l'incitation l'exige | Non lu au dela du resume ; jeux economiques, pas d'enquete | **Soutient, et donne le chiffre d'ordre le plus violent du theme** : 58 points sur une simple permutation d'ordre. C'est la borne haute de l'objection que a23 laisse ouverte chez nous, l'effet de l'ordre des modalites non mesure sur 43 questions a modalite dominante | [PROBABLE] resume lu | citation aval de 06-01 |
| 06-61 | « Every Token Counts : Exact Likert-Scale Distributions for Measuring LLM Attitudes and Biases » 2026, arXiv 2608.10503 | Peut on mesurer une attitude de modele sans bruit d'echantillonnage ? | Etude de cas d'ethnocentrisme du consommateur | 5 modeles | Plans factoriels completement croises ; **fonctions de masse exactes au niveau des jetons** au lieu d'un echantillonnage Monte Carlo ; consensus ordinal multivarie et ANOVA distributionnelle | Cadre analytique, pas de resultat d'ampleur cite dans le resume | Non lu au dela du resume ; pas de referent humain de population | **Muet sur la these, aligne sur notre methode.** C'est la formalisation de ce que nous faisons deja en lisant `n_probs` a temperature 0 : ils appellent cela « we eliminate Monte Carlo text sampling noise by operating directly on exact, token-level Probability Mass Functions ». A citer comme precedent methodologique | [PROBABLE] resume lu | citation aval de 06-01 |
| 06-62 | « Beyond the Hivemind : Escaping LLM Homogeneity via Meta-Persona Anchoring and Sequential Temperature Scaling » 2026, arXiv 2608.02618 | Peut on defaire l'homogeneite mesuree par 06-29 sans reentrainer ? | INFINITY-CHAT | Modeles ouverts sous environ 20 milliards de parametres | Similarite cosinus moyenne entre paires ; ancrage sur une meta persona auto choisie puis filtrage top-p suivi d'une temperature extreme (`T >= 4,0`) | Similarite moyenne de **environ 0,85 vers environ 0,65**, majorite des questions sous le seuil de 0,7 | Non lu au dela du resume ; aucun referent humain ; la temperature extreme n'est pas evaluee en qualite d'enquete | **Repond directement a 06-29 et concerne notre a4.** La temperature de 4,0 et plus, appliquee **apres** un filtre de validite et non seule, produit un gain la ou notre balayage nu echouait. C'est la version de decodage de ce que 06-44 demontre en theorie : il faut couper avant de chauffer | [PROBABLE] resume lu | citation aval de 06-18 |
| 06-63 | « What LLMs Think When You Don't Tell Them What to Think About ? » 2026, arXiv 2602.01689 | Que produit un modele quand l'invite ne contient aucun sujet ? | **256 000 echantillons**, jeu publie | **16 modeles** | Repartition thematique des sorties non contraintes | Preferences thematiques fortes et systematiques par famille : GPT-OSS programmation 27,1 pour cent et mathematiques 24,6 ; Llama contenu litteraire 9,1 ; DeepSeek souvent du religieux ; **Qwen souvent des questions a choix multiple** | Non lu au dela du resume ; aucun referent humain | **Soutient sur un point precis et inattendu pour nous.** Si Qwen produit spontanement des questions a choix multiple, alors notre regime d'invite categorielle tombe dans le mode par defaut de la famille, ce qui est une source de confusion entre le modele et le format qu'aucun de nos rapports n'a envisagee | [PROBABLE] resume lu | citation aval de 06-20 |
| 06-64 | « Stable Personas : Dual-Assessment of Temporal Stability in LLM-Based Human Simulation » 2026, arXiv 2601.22812 | Une persona tient elle sur la duree d'une conversation ? | **3 473 conversations** entre conversations, **1 370 conversations** et 18 tours en intra ; 4 conditions de persona, 3 formulations equivalentes | 7 modeles | Auto declaration de la persona contre notation par observateur | Les auto declarations restent **tres stables** entre et dans les conversations ; **les notations par observateur montrent un declin de l'expression de la persona au fil des tours** | Non lu au dela du resume ; personas cliniques, pas demographiques | **Nuance 06-42 et notre conditionnement.** Le modele continue de **dire** qu'il est la personne pendant que son comportement retourne au defaut. Sur une enquete a 149 items dans un seul contexte, c'est exactement le risque de derive que nous n'avons pas mesure | [PROBABLE] resume lu | citation aval de 06-20 |
| 06-65 | « Magic, Madness, Heaven, Sin : LLM Output Diversity is Everything, Everywhere, All at Once » 2026, arXiv 2604.01504 | Le mot « diversite » designe t il la meme chose selon la tache ? | Revue et cadre | Sans objet | Axe homogeneite contre heterogeneite, valorise selon quatre contextes normatifs : epistemique, interactionnel, societal, securite | Analyse de toutes les interactions croisees : « optimizing for one objective, such as improving safety, can inadvertently harm demographic representation or creative diversity » | Papier de cadre, aucune mesure | **Utile a la redaction, pas a la preuve.** Il donne le vocabulaire pour dire que notre objet est la diversite au sens **societal, de representation**, et non au sens creatif, ce qui neutralise par avance la moitie des objections de 06-26 | [PROBABLE] resume lu | citation aval de 06-20 |
| 06-66 | « APO : Alpha-Divergence Preference Optimization » 2025, arXiv 2512.22953 | Peut on regler le curseur entre recherche de mode et couverture de masse dans l'optimisation de preference ? | Non lu | Non lu | Divergence alpha comme famille contenant KL directe et KL inverse | Non lu | Titre seul | **Piste, non evaluee.** A ouvrir seulement si 06-43 devait etre discute au niveau de l'algorithme plutot qu'au niveau de la solution | [NON LU] titre seul | API arXiv (`mode seeking` et `preference`) |
| 06-67 | « Reference-Distribution Dependence in LLM-Based Synthetic Persona Data : Diagnosis and Post Hoc Adjustment of Demographic Distributions » 2026, arXiv 2608.28668 | Peut on corriger apres coup la distribution demographique d'un panel synthetique ? | Non lu | Non lu | Non lu | Non lu | Titre seul | **Piste directement pertinente pour la famille de correctifs**, non ouverte faute de temps | [NON LU] titre seul | citation aval de 06-01 |

---

## 2. Comment ca fonctionne

### 2.1 La chaine causale complete, maillon par maillon, et ou chacun a ete mesure

Le fichier initial posait la chaine en quatre etages, pre entrainement, ajustement supervise,
preference, decodage, et concluait que l'attribution etait « non tranchee » entre le SFT (06-22) et
le DPO (06-24). Cette passe de lecture ne tranche pas ce debat : **elle le dissout**, parce que
trois papiers nouveaux montrent que la question etait mal posee.

Le premier maillon est le pre entrainement, et il porte davantage que ne le disait le fichier
initial. Dodge et al. (06-37) etablissaient que le corpus avait deja ete filtre de facon
demographiquement orientee, ce qui est une soustraction. arXiv 2608.11426 (06-49) etablit quelque
chose de plus fort et de plus genant : **la convergence elle meme est deja dans le socle, et il
suffit de l'invite pour la faire sortir**. Leur experience decisive n'est pas une comparaison de
modeles mais une comparaison de trois invites sur le meme socle. En completion nue, un socle produit
des metaphores variees ; avec trois exemples, il converge ; avec le seul prefixe `Sure! Happy to
help.`, il produit « the most homogeneous answers », avec une similarite intra vehicule de 0,69 a
0,91. La consequence est qu'un ecart mesure entre un socle en completion et un modele instruit sous
gabarit de conversation **ne mesure pas les poids**, il mesure au moins autant la mise en scene de
l'assistant. C'est exactement l'avertissement que a27 tirait de l'ecart de 0,081 de TVD entre
completion et gabarit chez 2607.25292, et il est ici demontre en positif : le format seul suffit a
produire l'effet.

Le deuxieme maillon, l'ajustement supervise, cesse alors d'etre un coupable pour devenir un
amplificateur proportionnel. Le meme papier injecte des metaphores dans un jeu de SFT et mesure la
reponse selon la frequence prealable de la cible : le vehicule le plus frequent monte a 48 a 92 pour
cent, le sixieme a 1 a 12 pour cent, et **les vehicules absents de la distribution initiale ne
prennent jamais**, sauf a les repeter 5 a 7 fois. Autrement dit, la fonction de transfert du SFT est
croissante en la frequence prealable, et nulle en dehors du support. C'est la version experimentale
du resultat formel de 06-43 : a recompense egale, le rapport des probabilites dans la solution
optimale d'un objectif regularise par KL vaut exactement le rapport des probabilites dans la
reference, quelle que soit la force de la regularisation. **Ni le SFT ni la preference ne remontent
jamais une reponse rare.** Le premier ne le peut pas parce que la reponse n'est pas dans le support ;
la seconde ne le veut pas parce que l'objectif ne le demande pas.

Le troisieme maillon, la preference, apporte le gradient d'amplitude. C'est ici que 06-51 fournit ce
qui manquait a tout le theme : **quatre points de controle OLMo 32B de la meme lignee, avec un
referent humain apparie**. La divergence de style a l'humain croit de facon monotone, 0,25 au socle,
0,41 apres SFT, 0,53 apres DPO, 0,52 apres RLVR ; la variance entre histoires s'effondre de 6,03 fois
la variance humaine au socle a 0,84 apres SFT, puis 0,49 et 0,52. Les deux mouvements sont de sens
oppose et simultanes : **on s'eloigne de l'humain en position pendant qu'on se retrecit en
dispersion**. Le meme motif se lit dans le mouvement thematique, humains a environ 0,105, socle
0,096, SFT 0,089, DPO et RLVR 0,081. Le SFT fait le gros du chemin sur la variance, la preference
fait le gros du chemin sur la position. C'est la reconciliation de 06-22 et de 06-24, et elle dit
que les deux avaient raison sur des quantites differentes.

Le quatrieme maillon, le decodage, est desormais borne des deux cotes. 06-50 mesure que l'alignement
divise le nombre effectif de branches par 2 a 5 globalement, et jusqu'a un ordre de grandeur en debut
de sortie, de 12 a 1,2, et que dans une analyse de Pareto **l'alignement franchit a lui seul le seuil
de 80 pour cent d'impact cumule, loin devant la taille du modele et la complexite de l'invite**. La
consequence operationnelle est dans leur table 1 : quand on passe du decodage par defaut au decodage
le plus ouvert sur MMLU-STEM, un modele aligne perd 3,31 pour cent (Llama-3-70B-Instruct) a 19,84
(Llama-3.1-8B-Instruct), un socle en perd 18,59 a 31,48. Le decodage n'a d'effet que la ou il y a des
branches. 06-44 donne la borne theorique correspondante : sous decroissance geometrique de la
distribution rangee, toute mise a l'echelle en temperature satisfait `Div(p) <= e puissance moins m
c(epsilon)`, donc la diversite decroit exponentiellement avec le nombre de positions de branchement
des qu'on impose un plancher de validite. Notre borne de 6,29 en temperature, deja confirmee par
a27, recoit ici sa raison : ce n'est pas que la temperature necessaire soit grande, c'est que le
compromis validite contre diversite est exponentiel en longueur.

**Le gradient complet, quand on met bout a bout les quantites comparables, est donc le suivant.** La
frequence dans le corpus fixe le support et l'ordre ; l'invite, y compris le seul gabarit
d'assistant, revele la concentration deja presente ; le SFT l'amplifie proportionnellement a cette
frequence et effondre la variance entre productions (variance sur humain de 6,03 a 0,84 chez 06-51) ;
la preference deplace la position sans corriger la variance (MMD de 0,41 a 0,53) ; le decodage ne
peut plus rien parce qu'il n'y a plus de branches (BF de 12 a 1,2 chez 06-50). Chaque maillon a
desormais au moins une mesure, ce qui n'etait pas le cas au debut de la journee.

### 2.2 La typicalite : pourquoi un modele aligne rend la reponse la plus typique du groupe

C'est la partie du chantier ou la lecture rend le plus, parce qu'elle transforme une intuition en
theoreme et en mesure.

Le fichier initial tenait la typicalite par un seul papier, 06-18, qui l'estimait dans les donnees de
preference sous une forme fonctionnelle imposee, `r = r_vrai + alpha log pi_ref + epsilon`, avec
`alpha` a 0,57 plus ou moins 0,07 et 0,65 plus ou moins 0,07. Cette estimation reste la plus directe,
mais elle etait isolee et sa forme etait choisie. Trois nouvelles entrees la soutiennent par trois
chemins independants.

Le chemin formel est 06-43. Sa remarque 4.3 est courte et sans echappatoire : pour deux echantillons
de meme recompense, le rapport de leurs probabilites dans la solution optimale vaut le rapport de
leurs probabilites sous la politique de reference, **independamment du coefficient de
regularisation**. Les auteurs l'ecrivent ainsi : « RL with any KL-regularization does not increase
the relative probability of lower-support samples to high-support ones, as long as their rewards are
the same ». Transposee a une enquete, la phrase se lit : sur un item ou deux modalites sont egalement
defendables, l'optimisation **recopie la frequence relative du modele de base** et n'a aucun moyen de
remonter la modalite minoritaire. Et la remarque 4.2 dit le sort de la modalite legerement moins
approuvee : a support egal, un ecart de recompense de 0,1 avec un `beta` usuel de 1e-3 la rend
2,6 fois 10 puissance 43 fois moins probable. C'est la formule generale de nos 80 pour cent de
cellules a probabilite maximale superieure a 0,99.

Le chemin empirique cote donnees est 06-49, deja decrit : la capacite d'une reponse a etre amplifiee
par le SFT est croissante en sa frequence prealable et nulle hors du support.

Le chemin empirique cote humains est 06-47, et c'est le plus parlant pour la these. Sur 195 debats du
New York Times avec 1 039 reponses humaines appariees, 65,3 pour cent des arguments principaux
humains sont uniques dans leur debat contre 3,4 pour cent chez les modeles. Mais le chiffre decisif
n'est pas celui la, c'est la **selectivite du recouvrement** : en mettant en commun cinq modeles
diversifies, on recupere 73,9 pour cent des grappes d'arguments humains, dont **98,1 pour cent de
ceux portes par plusieurs humains et 67,8 pour cent de ceux portes par un seul**. La perte est donc
exactement indexee sur la raretete. Et le meme papier ferme la boucle avec le maillon de recompense
que 06-11 et 06-12 laissaient qualitatif : les six evaluateurs testes, dont deux modeles de
recompense entraines sur preference humaine, **preferent l'essai a argument partage a l'essai a
argument rare**, jusqu'a 74,7 pour cent pour Skywork-Reward-V2 et 67,0 pour ArmoRM. La cible
optimisee prefere le typique, mesure sur un objet ou le typique et le vrai ne coincident pas.

**Ce que cela donne pour notre substitution personne vers groupe.** Le mecanisme candidat de
`ARBITRAGE.md` recoit ici trois etages : la reponse typique du groupe est celle qui a la plus grande
masse dans la reference, l'objectif d'alignement ne peut pas la deloger a qualite egale, et
l'annotateur comme le modele de recompense la preferent quand la qualite differe. La formulation
defendable, et elle est nouvelle, est que **la substitution n'est pas un defaut d'entrainement, c'est
la solution du probleme tel qu'il est pose**. C'est exactement l'argument que 06-12 tenait au niveau
sociologique, « une fonction de recompense unique ne peut pas representer une societe humaine
diverse » ; 06-43 le tient desormais au niveau de l'objectif, et les deux se citent l'un l'autre sans
le savoir.

### 2.3 Base contre instruct sur la prediction individuelle, et les pieges de format

Le fichier initial comptait quatre equipes pour le modele de base, une contre, avec une reponse par
regime. Cette lecture ajoute trois choses, dont une qui coute cher a l'option C de `ARBITRAGE.md`.

Premiere chose, un ordre de grandeur sur notre propre famille de modeles. 06-46 est la seule table
publiee qui mesure un ecart base contre instruct **sur Qwen3-4B** : `distinct_k` de NoveltyBench passe
de 8,780 a 2,560, soit 29,2 pour cent conserve, quand OLMo-3-7B conserve 68,2 pour cent et
LLaMA-3.1-8B 58,7. Notre modele appartient donc a la famille qui perd le plus sur cet axe, et le
chiffre est du meme ordre que nos 65,4 et 67,4 pour cent de variete conservee, avec une metrique
differente et sans referent humain. Cela ne valide pas notre chiffre, cela dit que la question ouverte
de FAITS-ETABLIS section 7 n'a pas la meme reponse selon la famille.

Deuxieme chose, et c'est la mauvaise nouvelle : **le socle n'est pas du bon cote du referent
humain**. 06-51 mesure une variance de style a 6,03 fois la variance humaine au socle et un profil
affectif deja hors cible, conflit a environ 47 pour cent contre 20 chez les humains. Les auteurs
l'ecrivent sans detour : « The base model is not simply human-like : it can be affectively
over-marked and stylistically wide-ranging and unstable ». 06-52 mesure la meme chose du cote de la
correction : la verbalisation de distribution fait passer le rapport d'ecarts types de 0,40 a 0,56
vers 1,26 a 1,37, c'est a dire qu'elle traverse la cible. Et 2607.25292, lu en a27, disait deja que
les socles echouent aussi, « every base fails both 5-way targets ». La conclusion est donc que **la
comparaison base contre instruct est une comparaison entre deux erreurs de signe oppose**, et que la
question utile n'est pas laquelle des deux est la meilleure mais de combien chacune manque le
referent humain. Notre E1 doit se rapporter en ces termes, sous peine de mesurer un gagnant sans
mesurer un ecart.

Troisieme chose, les pieges de format sont plus gros que ce que le fichier initial supposait, et il
faut les hierarchiser. Le fichier initial retenait de 06-25 un rapport de 25 a 300 pour cent du a un
gabarit de conversation. Il faut y ajouter quatre elements nouveaux. Un, 06-49 montre que **le seul
prefixe d'assistant, sur un socle, produit la sortie la plus homogene des trois regimes testes** ;
donc le gabarit n'est pas un facteur de nuisance a controler, c'est un traitement a part entiere.
Deux, a27 avait deja mesure chez 2607.25292 que le format d'invite vaut 0,081 de TVD sur un meme
point de controle, soit environ la moitie de l'ecart base contre instruct de la famille Llama ; les
taux d'echec d'extraction publies dans leur `parse_fail` disent par ailleurs qu'un socle a trois
exemples repond dans le format demande dans plus de 95 pour cent des cas, ce qui enterre l'objection
Rozado des 42 pour cent d'invalides. Trois, 06-53 mesure sur SHARE que **le seul passage d'une
reponse ouverte sur 0 a 100 a des modalites discretes change la forme de la distribution predite**,
en gardant le meme biais de sous estimation. Quatre, 06-60 mesure sur cinq environnements que
**permuter l'ordre de deux actions coute a un modele 58 points de cooperation**, ce qui borne par le
haut le risque que a23 laisse ouvert chez nous sur nos 43 questions a modalite dominante.

**Il faut ajouter un piege que personne n'avait signale dans le dossier.** 06-63 mesure, sur 256 000
sorties non contraintes de 16 modeles, que chaque famille a un mode par defaut, et que **Qwen produit
spontanement des questions a choix multiple**. Si notre modele produit ce format quand on ne lui
demande rien, alors notre invite categorielle ne le sort pas de son regime habituel, elle l'y
enfonce, et le taux de sorties hors nomenclature que E1 doit publier sera artificiellement bon pour
une raison qui n'a rien a voir avec la fidelite.

### 2.4 La calibration des modeles instruits sur choix ferme, et ce que les recalibrations font a la structure de groupe

Le fichier initial etablissait la degradation (06-32, facteur 10,6 sur l'ECE) et une reparation
possible a un parametre (06-33, `T = 2,5`), avec l'attribution nuancee par 06-34. Cette lecture change
deux choses.

La premiere est que **la jonction diversite et calibration, que la section 3 point 2 du fichier
initial revendiquait comme non faite, a ete faite en mai 2026**, par 06-44, et il faut le dire avant
un relecteur. Leur these est que la diversite est bornee par deux defauts de calibration de la
distribution conditionnelle : la calibration d'ordre, les jetons valides ne sont pas classes avant
les invalides, et la calibration de forme, la masse est concentree sur quelques valides avec une
queue lourde melangee. Leur filtre oracle, applique aux deux premieres etapes de decodage seulement,
porte la diversite d'embedding de 0,25 (sans filtrage) a 0,40 et le Self-BLEU de 0,86 a 0,69, ce qui
prouve que **les alternatives valides sont dans la distribution et que les regles de coupe par rang
ne savent pas les atteindre**. Notre revendication de jonction ne disparait pas pour autant, mais
elle doit se restreindre a ce qu'ils ne mesurent pas : leur calibration est une calibration de
validite au niveau du jeton, la notre est une calibration au sens de l'enquete, probabilite annoncee
contre frequence realisee sur des modalites d'une nomenclature, avec un referent humain. Ce sont deux
objets differents et le second n'est toujours pas dans la litterature.

La seconde chose est la reponse, desormais chiffree, a la question que le fichier initial posait en
E5 et E6 : **que font les recalibrations a la structure de groupe ?** Trois reponses convergent, et
elles sont mauvaises pour la famille des correctifs.

06-52 mesure la verbalisation de distribution sur la WVS turque, avec 2 414 repondants reels. Elle
gagne de 6,8 a 10,1 points de fidelite dans trois familles, ce qui est le resultat annonce par 06-18.
Mais elle **traverse la cible** : le rapport d'ecarts types passe de 0,46, 0,56 et 0,40 a 1,26, 1,36
et 1,37, et les auteurs qualifient cela de propriete structurelle, « a structural over-corrector ».
Et surtout, ce qu'elle gagne en agrege, elle ne le gagne pas en sous groupe : leur controle placebo
montre que la manipulation non pertinente deplace l'opinion de plus 1,49 la ou la manipulation
pertinente la deplace de plus 1,13, donc la sensibilite contrefactuelle est non specifique, et « VS
keeps aggregate strength while subgroup and individual claims are contaminated by recall and
underdetermination ».

a27 avait deja etabli le meme motif sur PPA : la randomisation de l'ordre et de la formulation
recupere 21 pour cent de l'erreur agregee a la population, ameliore la correlation de l'ecart
democrate moins republicain avec le Pew de 0,573 a 0,678, mais **ne publie aucun rapport d'amplitude
a l'humain ni aucun cout individuel**.

06-54 apporte le troisieme temoignage, et il est negatif au bon sens du terme : sur 18 modeles de
fond et 19 cultures de la WVS, la correlation entre alignement et diversite de valeurs vaut Pearson
`r = moins 0,12`, c'est a dire rien. Cela confirme independamment ce que a26 avait deduit de la seule
annexe F de 2609.00565 : **le compromis alignement contre diversite n'est pas une contrainte, c'est
une trajectoire d'entrainement**. La contrainte de total que le projet veut poser reste donc la seule
formulation qui soit une identite et non une correlation observee.

Enfin, une piece nouvelle sur l'inegalite de la reparation. 06-55 aligne quatre modeles sur 13
groupes demographiques par trois methodes, a budget apparie, soit 156 bras, et trouve que « a matched
budget does not move these models uniformly ; it redistributes » : **chaque groupe progresse et
chaque ecart se creuse**, avec des intervalles excluant zero sur les axes politique, genre et statut
matrimonial, et non sur education et revenu. C'est un terme que nous n'avons pas et que personne ne
met en regard d'un rapport d'amplitude : l'inegalite du **gain de fidelite** entre groupes, a cote de
l'inegalite de **l'ecart entre groupes**.

### 2.5 L'ablitération et les modeles non censures : ce qui change, mesure

C'est la piste que le fichier initial listait comme non ouverte, section 4 point 10, en supposant
qu'elle donnerait « le mecanisme interne du refus ». Elle le donne, et elle donne aussi une reponse
plus utile que prevu a la question qui nous interesse.

Le mecanisme est etabli par 06-56 : le refus est porte par un sous espace de dimension un, sur 13
modeles de discussion ouverts jusqu'a 72 milliards de parametres ; effacer la direction supprime le
refus des instructions nuisibles, l'ajouter provoque le refus d'instructions inoffensives. Cela
explique en une ligne la correlation de Spearman de 0,89 de 06-35 entre taux de rejet sur invites
sures et sur invites toxiques : les modeles n'apprennent pas ou est la ligne parce qu'il n'y a pas de
ligne a apprendre, il y a un curseur unidimensionnel.

L'effet sur ce que le modele exprime est mesure par 06-48, et c'est la seule mesure publiee de ce
genre. Le protocole est bon : 21 600 decisions sous incertitude, une tache **qui ne declenche aucun
refus**, donc tout ecart entre bras est un effet collateral pur ; provenance tenue constante, meme
auteur d'abliteration, meme pile de service, invite figee octet pour octet. Trois effets se repliquent
sur les deux familles. Les modeles ablitérés sont plus optimistes, de plus 12,2 points sur Gemma et
plus 7,4 sur Qwen, intervalles excluant zero. Ils se justifient plus longuement, de plus 4,0 et plus
7,4 mots. Et ils **amincissent le vocabulaire du doute**, le lexique d'incertitude pour 100 mots
passant de 3,68 a 2,73 sur Gemma et de 3,46 a 1,29 sur Qwen. Un quatrieme effet change de signe selon
la famille : la confiance declaree baisse sur Gemma, moins 0,008, et monte sur Qwen, plus 0,109,
intervalles de famille disjoints.

**Le chiffre qui compte le plus pour nous n'est pas dans le resume : l'unanimite entre echantillons
reste de 91 a 95 pour cent dans les quatre bras.** L'abliteration deplace la position et le
vocabulaire, elle ne rend aucune variance par appel. Elle est donc **disqualifiee comme correctif du
deficit de dispersion**, ce que personne n'avait ecrit, et notre a20 n'a pas de concurrent de ce cote
la. Deux corollaires. D'une part, le cout collateral est reel et depend de l'outil : 06-57 mesure une
variation de GSM8K allant de plus 1,51 a moins 18,81 points, moins 26,5 pour cent en relatif, et une
divergence KL a la distribution d'origine allant de 0,043 a 1,646 selon l'outil, soit un facteur 38.
D'autre part, l'audit de provenance de 06-48 a trouve deux canaux de contamination sur quatre points
de controle, un couple de quantificateurs mal apparies et un gabarit de conversation communautaire
perime qui rendait l'invite systeme sous forme de liste echappee, et les auteurs en tirent la phrase
qu'il faut coller au dessus de notre E1 : « studies that do not verify rendered prompts
token-for-token can silently measure the template, not the intervention ». a27 signalait deja comme
hypothese que nos quantifications GGUF tierces pouvaient degrader la calibration differemment selon
qu'il s'agit d'un socle ou d'un modele instruit ; ce n'est plus une hypothese, c'est un incident
documente sur un banc preenregistre.

---

## 3. Ce qui se contredit, et la variable qui explique

**C1. Le signe de l'effet sur les ecarts entre groupes.** 2608.03044 mesure un gonflement d'environ
un facteur 2 apres post entrainement ; 2609.00565 mesure un aplatissement d'un facteur 3 a 6 apres
reglage culturel ; 06-51 mesure un aplatissement des ecarts entre domaines de 62 a 81 pour cent ;
06-54 mesure une diversite de valeurs entre cultures inferieure de 18 a 54 pour cent a l'humain ;
nous mesurons un gonflement de 7,64 avec etiquette et 0,73 sans. **La variable qui explique est la
presence, ou non, d'une etiquette de groupe dans l'invite.** Quand le groupe est nomme dans l'invite,
le modele joue le groupe et l'exagere : c'est 2608.03044, c'est 06-55 dont le plancher « invite
seule » est precisement une etiquette, et c'est notre a19 et a23. Quand le groupe n'est pas nomme et
n'existe que dans le materiau, socle contre corpus chez 06-51, cultures conditionnees mais evaluees
en distance mutuelle chez 06-54 et 2609.00565, l'alignement rabat tout vers un centre commun et les
ecarts s'ecrasent. Cette lecture est nouvelle, elle est coherente avec les cinq mesures, et elle
repond a la question 4 posee a Simon en a26 sans avoir a accuser un article accepte en Findings :
les deux quantites ne sont pas contradictoires, elles sont mesurees sous deux regimes de
conditionnement differents. **Elle est testable chez nous a cout nul**, voir T1 en section 4.

**C2. Le SFT ou le DPO.** 06-22 attribue au SFT, 06-24 au DPO, 06-34 a l'ajustement par instruction
pour la calibration. **La variable qui explique est la quantite mesuree.** 06-51, qui mesure les deux
sur les memes points de controle et contre un referent humain, montre que la variance entre
productions s'effondre au SFT, de 6,03 a 0,84 fois la variance humaine, et bouge peu ensuite, 0,49 et
0,52 ; tandis que la position, mesuree par la divergence de style a l'humain, continue de s'eloigner
apres le SFT, de 0,41 a 0,53. Le SFT est l'etape de la variance, la preference est l'etape de la
position. Les deux camps mesuraient des choses differentes sur des lignees differentes.

**C3. Le modele de base est il un meilleur simulateur.** 06-19, 06-15, 06-16 et 2608.03044 disent
oui ; 06-26 dit non sous controle de qualite ; 06-51 dit **oui en position et non en dispersion, avec
un depassement dans l'autre sens** ; 2607.25292 dit que le socle echoue aussi sur sa propre tache.
**La variable qui explique est le cote du referent humain ou tombe l'erreur.** Le socle est sur
disperse, 6,03 fois l'humain chez 06-51, et le modele post entraine est sous disperse, 0,49. Les deux
manquent la cible ; les travaux qui declarent le socle vainqueur mesurent une distance a un uniforme
ou a une cible synthetique, pas une distance a une population. C'est la reformulation la plus utile
pour `ARBITRAGE.md` option C : la nuit de calcul base contre aligne ne doit pas rendre un vainqueur,
elle doit rendre deux ecarts signes au referent humain.

**C4. La temperature est elle inutile.** Le fichier initial concluait que non, en s'appuyant sur
06-25 (la temperature ne repare pas), 06-33 (une seule temperature repare la calibration) et notre
borne de 6,29. 06-45 mesure que la temperature est « particularly uninstructive » au niveau d'une
population, 06-50 mesure qu'un modele aligne perd 3 a 20 pour cent de performance quand on ouvre le
decodage alors qu'un socle en perd 31, et 06-62 obtient un gain reel a `T >= 4,0`. **La variable qui
explique est l'ordre des operations.** 06-44 le demontre : une temperature appliquee **seule** deplace
la masse vers la queue invalide plus vite qu'elle ne recupere les valides rares ; une temperature
appliquee **apres** une coupe qui garantit la validite recupere de la diversite. Notre a4 balayait la
temperature nue. La ligne defendable devient « la temperature seule ne repare pas », et non « la
temperature ne repare pas ».

**C5. Plus gros, mieux calibre.** 06-28 mesurait un effet d'echelle inverse sur la calibration
d'ouverture, Qwen-0,6B battant Qwen-8B. 06-58 le retrouve sur la diversite epistemique, « large models
are counterintuitively less diverse than smaller ones ». 06-44 mesure au contraire une tendance
legere a la hausse de l'aire sous la frontiere precision rappel avec la taille, tout en precisant que
« larger models do not reliably recover more valid continuations under a high-precision constraint ».
**La variable qui explique est la contrainte de validite.** Sans contrainte, la taille aide un peu ;
sous contrainte de validite elevee, elle n'aide pas. Pour notre nuit sur gpt-oss-20b, cela veut dire
qu'il faut publier la mesure **a taux de sorties dans la nomenclature fixe**, sans quoi on comparera
deux points de compromis differents.

**C6. Un desaccord non resolu, a signaler comme tel.** 06-46 restaure 68 pour cent de la diversite du
socle sur Qwen3-4B par des donnees de preference construites a partir du socle, sans perte de
qualite ; 06-52 montre que toute restauration de dispersion depasse la cible et contamine les sous
groupes ; 06-43 montre qu'un changement de deux lignes dans la recompense suffit a rendre la solution
multimodale. Les trois ne se contredisent pas logiquement, mais **aucun des trois ne mesure ce que sa
restauration fait a l'appariement individuel**, c'est a dire a notre critere A6. Il n'existe donc
aucune donnee permettant de dire si ces trois correctifs reparent les bonnes personnes ou fabriquent
du bruit bien place. C'est la contradiction la plus utile pour nous, parce qu'elle est vide.

---

## 4. Ce que ca permet de tester chez nous tout de suite, avec le cout

Les tests sont classes par rapport gain sur cout. Aucun ne demande d'argent. Les couts en appels sont
convertis au debit reel de a5 et a23, 13 217 appels par heure en regime court et 4 886 en regime
long ; une condition complete vaut 22 350 appels, soit de l'ordre de deux a cinq heures.

**T1. Le regime de conditionnement explique t il le desaccord de signe. Cout : nul, sur traces
existantes.** C1 propose une explication testable : le gonflement inter apparait quand le groupe est
**nomme** dans l'invite, l'aplatissement quand il ne l'est pas. Nous avons deja les deux conditions,
C2 avec etiquette ideologique et sa variante sans, sur 300 personnes. Il suffit de recalculer, sur
les memes traces, un terme inter **defini a la maniere de 2609.00565**, c'est a dire l'esperance de
la distance entre deux individus tires dans deux groupes differents, en plus de notre terme inter
actuel. Si notre condition sans etiquette donne un aplatissement au sens de leur mesure pendant que
notre condition avec etiquette donne un gonflement au sens de la notre, alors nous avons **la
variable qui reconcilie deux articles acceptes en Findings d'EMNLP 2026**, sans accuser ni l'un ni
l'autre. C'est la reponse la moins couteuse et la plus elegante a la question 4 posee a Simon en a26.
Quelques minutes de calcul, zero appel.

**T2. Sur quelle modalite le modele s'ancre t il. Cout : nul, sur traces existantes.** a26 avait
identifie chez 2609.00565 deux modes d'echec distincts, l'ancrage sur la modalite majoritaire pour
les items categoriels et le retrait vers le milieu de l'echelle pour les items ordinaux. 06-53 en
ajoute un troisieme, le **biais de tendance centrale au sens de l'enquete**, qui surestime les
modalites rares et sous estime la majoritaire tout en resserrant l'ensemble, et un quatrieme,
l'**hyper exactitude**, l'absence des erreurs humaines et des « je ne sais pas ». Nos 46 et 43
questions sur 149 a modalite dominante ne sont classees selon aucun de ces quatre criteres. Le
classement se fait sur les traces des 44 700 appels, sans un seul appel de modele, et il transforme
un constat de degenerescence en une typologie. Quelques minutes.

**T3. La voie describe, deja recommandee par a27, renforcee ici. Cout : 149 appels, moins d'une
minute.** a27 la classait comme l'experience la moins chere du dossier, sur la foi de 2607.25292 et
de 2608.03044. 06-52 la mesure maintenant sur une enquete reelle avec 2 414 repondants, et ajoute
l'information qui manquait : elle gagne de 6,8 a 10,1 points de fidelite **mais fait passer le
rapport d'ecarts types de 0,4 a 1,37**. Il faut donc l'executer chez nous en rapportant **les deux**
quantites, fidelite et rapport de dispersion, et non la seule fidelite. Si notre modele reproduit le
depassement, nous avons une replication independante sur le GSS ; s'il ne le reproduit pas, nous avons
un resultat contre eux sur un modele de 4 milliards de parametres.

**T4. Le gabarit de conversation comme traitement, pas comme controle. Cout : une condition, deux a
cinq heures.** C'est E2 du fichier initial, dont le statut change. 06-49 montre que le seul prefixe
d'assistant, sur un socle, produit la sortie la plus homogene des trois regimes ; 06-48 montre qu'un
gabarit perime a suffi a contaminer un bras entier d'une etude preenregistree. La condition a faire
tourner est donc : meme modele instruit, memes 150 personnes, memes 149 items, en **completion a
trois exemples** au lieu du gabarit de conversation, avec les trois exemples pris hors du support des
items testes, sur le modele de la constante `BASE_SHOTS` de 2607.25292. Elle doit passer **avant** E1,
et non a cote, sans quoi E1 mesurera le paquet format plus poids. Ajouter, comme le demande 06-48,
une verification du rendu de l'invite jeton par jeton dans les deux conditions.

**T5. L'ordre des modalites, avec un chiffre pour justifier le cout. Cout : une condition, deux a
cinq heures, ou un sous ensemble a un quart du cout.** L'ablation de PPA lue en a27 donnait deja
l'ordre seul a 60 pour cent de l'effet total. 06-60 borne le risque par le haut : **58 points de
cooperation perdus sur une simple permutation de deux actions**. Nos 43 questions a modalite dominante
sont le terrain le plus expose du dossier. Un sous ensemble de 40 items avec ordre permute sur les
memes 150 personnes coute environ 6 000 appels, soit moins d'une heure, et suffit a transformer une
limite declaree en une mesure.

**T6. La temperature apres coupe de validite, et non seule. Cout : nul, sur distributions deja
enregistrees.** E5 du fichier initial proposait de balayer une temperature unique sur les
probabilites de modalite deja produites. 06-44 dit pourquoi cela peut echouer et comment le reparer :
il faut **restreindre a l'ensemble valide avant de chauffer**. Chez nous, l'ensemble valide est connu
exactement, c'est la nomenclature de l'item, ce qui nous met dans la situation privilegiee de leurs
taches a ensemble valide connu. Le balayage doit donc se faire sur les probabilites **renormalisees
sur les seules modalites de la nomenclature**, et rapporter ECE, entropie individuelle et ratio
intra en fonction de T. Aucun appel supplementaire.

**T7. Le panneau de cinq cibles synthetiques comme controle de sanite. Cout : quelques milliers
d'appels, de l'ordre de la dizaine de minutes.** Deja propose en a27 question 4. 06-43 ajoute une
raison de le faire : leur tache jouet « produire 1 ou 2 uniformement » est le cas ou la remarque 4.3
mord le plus fort, et elle donne un point de comparaison ou l'on sait ce que la reponse devrait etre.

**T8. Ce qu'il ne faut pas faire.** Ne pas ouvrir la piste des modeles non censures comme correctif
de dispersion. 06-48 mesure que l'unanimite entre echantillons reste de 91 a 95 pour cent apres
abliteration, donc l'operation ne rend aucune variance ; 06-57 mesure que le cout collateral atteint
moins 26,5 pour cent sur une capacite et que la divergence a la distribution d'origine varie d'un
facteur 38 selon l'outil. Le rapport gain sur risque est defavorable et le dossier peut le dire avec
deux citations.

---

## 5. Ce que personne n'a fait

1. **Personne n'a mesure la calibration au sens de l'enquete sur une paire base et instruct.** 06-44
   a fait la jonction diversite et calibration, mais au niveau du jeton et de la validite
   syntaxique. 06-32 et 06-34 mesurent l'ECE sur des bancs de connaissance. **Aucune equipe ne
   publie, sur des reponses a une enquete, la probabilite annoncee contre la frequence realisee par
   modalite, pour un socle et pour son modele instruit, avec un referent humain.** C'est exactement
   ce que nos 44 700 appels produisent deja d'un cote et que E1 produirait de l'autre.

2. **Personne n'a mesure ce qu'un correctif de dispersion fait a l'appariement individuel.** Ni la
   verbalisation (06-18, 06-52), ni PPA (a27), ni REDIPO (06-46), ni MARA (06-43), ni le decodage
   conformatif (06-24) ne comptent les personnes reparees contre les personnes cassees. Notre critere
   A6 est le seul instrument de ce type dans le dossier, et il est desormais reclame par trois
   correctifs distincts qui ne l'ont pas.

3. **Personne n'a rapporte l'inegalite du gain de fidelite entre groupes a l'amplitude de l'ecart
   entre groupes.** 06-55 mesure la premiere sur 156 bras, nous mesurons la seconde. Les deux
   quantites decrivent la meme injustice sous deux angles et n'ont jamais ete publiees ensemble.

4. **Personne n'a mesure la frequence d'un groupe dans le corpus de pre entrainement en regard de la
   fidelite du modele a ce groupe.** 06-49 etablit la fonction de transfert frequence vers
   amplification au niveau du SFT et sur des metaphores ; 06-37 etablit le filtrage oriente du
   corpus ; 06-04 etablit l'effet d'un pre entrainement partisan supplementaire. Le maillon
   manquant, la frequence des groupes tels qu'ils sont **decrits dans le texte**, mise en regard de
   la representativite mesuree par 06-01, n'a ete mesure par personne. Nos requetes ne rendent rien
   sur ce point, et c'est la seule case de la chaine causale qui reste vide apres ce chantier.

5. **Personne n'a traite l'absence de « je ne sais pas » comme une non reponse d'enquete.** 06-53
   l'observe et le nomme, « the survey-anchored agents never generated Don't know or Refusal
   responses, and the demographics-only agents produced such responses only rarely », mais ne
   l'analyse pas avec l'appareil des donnees manquantes. Combine a 06-08, dont 95 pour cent des
   reponses invalides sont des derobades et 6 pour cent seulement des refus explicites, cela reste la
   place la plus libre du theme, et c'est celle qui touche le plus directement le dicible.

6. **Personne n'a mesure ce que l'abliteration fait a une distribution d'opinion.** 06-48 est la
   seule mesure d'effet collateral sur des enonces exprimes, et son terrain est financier. Aucune
   equipe n'a passe un modele non censure sur une enquete d'opinion avec referent humain. C'est une
   place libre, mais T8 explique pourquoi elle ne vaut probablement pas la nuit de calcul.

7. **Personne n'a verifie si la derive de persona de 06-64 se produit sur une passation d'enquete
   longue.** Leurs 18 tours de conversation montrent que l'auto declaration reste stable pendant que
   l'expression observee decline. Nos 149 items en une passation sont un cas intermediaire que
   personne n'a mesure, et qui, s'il derivait, expliquerait une part de notre bruit de deviance.

8. **Personne n'a applique le cadre de coverage de 06-59 a une nomenclature d'enquete.** Separer la
   plausibilite de la largeur est exactement ce dont le dossier a besoin pour repondre a 06-26 sans
   dependre d'un seuil de qualite arbitraire, et sur choix ferme la separation est triviale a
   calculer.

---

## 6. Ce que je n'ai pas pu verifier

1. **Le budget de recherche par moteur generaliste etait epuise avant l'ouverture du chantier**, 200
   requetes sur 200. Toute la prospection est passee par l'API de citations de Semantic Scholar et
   par l'API arXiv. Consequence : les travaux hors informatique que la consigne demande de garder,
   psychologie sociale, science politique, methodologie d'enquete, ne sont atteignables par ces API
   que s'ils sont cites par un papier d'informatique du theme. **Ce chantier est donc structurellement
   biaise vers l'informatique**, et il faut le dire. Les deux seules entrees hors informatique du
   theme, 06-39 Science Advances et 06-40 Creativity and Cognition, restent celles de la table
   initiale.

2. **L'API de references de Semantic Scholar ne rend rien pour les identifiants arXiv recents** ; la
   remontee des citations (« ce que la reference cite ») n'a donc pu se faire que par lecture des
   sections de travaux connexes dans les PDF, pas par appel d'API. La descente (« ce qui la cite »)
   a fonctionne normalement. La remontee est donc moins systematique que la descente dans ce
   chantier.

3. **Les valeurs de la figure 4 de 06-44** ne sont pas tabulees. C'est la figure qui porte l'effet de
   la taille **et de l'etape d'entrainement** sur la calibration d'ordre, pour Qwen-3, Llama-3 et
   Olmo-3 sur neuf tailles. C'est precisement la donnee qui repondrait a la question ouverte de
   FAITS-ETABLIS section 7. Le texte est confirme, les valeurs ne le sont pas.

4. **Les valeurs par groupe de la figure 3 de 06-55** ne sont accessibles qu'en figure ; seuls les
   enonces et le statut des intervalles par axe sont confirmes sur le texte.

5. **Les valeurs des figures 1, 4, 7 et 8 de 06-49** ne sont pas tabulees. Les enonces cites
   (convergence installee apres le SFT, amplification de 48 a 92 pour cent contre 1 a 12, echec des
   vehicules hors distribution, similarite intra vehicule de 0,69 a 0,91, condition assistant la plus
   homogene) sont confirmes sur le texte.

6. **La carte de chaleur des rapports de BF de 06-50, figure 4a**, n'est pas tabulee ; les valeurs
   citees, facteur 2 a 5, 12 vers 1,2 et pointe a 10 fois, sont dans le texte, et la table 1 est
   integralement lue.

7. **06-57, 06-59, 06-60, 06-61, 06-62, 06-63, 06-64 et 06-65 n'ont ete lus qu'au resume.** Aucun
   chiffre repris d'eux ne doit passer en redaction sans une lecture au texte. Le cas le plus
   sensible est le « 58 points de cooperation » de 06-60, qui est cite en T5 comme borne haute : il
   vient du resume et il faut l'ouvrir avant de s'en servir comme argument de cout.

8. **06-66 et 06-67 n'ont ete lus qu'au titre.** 06-67, sur l'ajustement a posteriori des
   distributions demographiques d'un panel synthetique, est le plus proche de notre famille de
   correctifs et merite d'etre ouvert au prochain chantier.

9. **Aucun chiffre d'aucun papier n'a ete reproduit.** Trois depots publics existent parmi les
   entrees nouvelles (06-46, 06-43 et le depot de 2607.25292 deja lu en a27) ; la commande de ce
   chantier interdit l'analyse de donnees, donc rien n'a ete recalcule. Les chiffres sont pris tels
   quels dans les PDF officiels.

10. **La coincidence entre les 29,2 pour cent de diversite conservee par Qwen3-4B chez 06-46 et nos
    65,4 et 67,4 pour cent de variete conservee ne doit pas etre exploitee.** Ce sont deux
    quantites differentes, `distinct_k` de NoveltyBench sur generation ouverte d'un cote, part de la
    variete de reponses humaines sur nomenclature fermee de l'autre, sur deux modeles qui ne sont
    meme pas le meme point de controle : le leur est un `Qwen3-4B` en poids d'origine, le notre un
    `Qwen3-4B-Instruct-2507` en GGUF Q4_K_M. La seule chose defendable est que les deux mesures
    placent cette famille du cote des grandes pertes.

11. **La lecture de 06-51 est faite sur OLMo 32B, pas sur notre echelle.** Le rapport de variance de
    6,03 au socle est un resultat sur une lignee de 32 milliards de parametres, sur de la fiction,
    avec un referent litteraire. Rien ne garantit qu'un socle de 4 milliards soit sur disperse sur
    une enquete. C'est une hypothese de travail pour E1, pas un fait transposable.
