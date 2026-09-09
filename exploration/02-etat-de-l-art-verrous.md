# Etat de l'art scientifique de la simulation de populations par LLM, et verrous

Agent 2 de l'exploration popsim. Document redige le 2 septembre 2026.
Regles de redaction appliquees : francais, pas de tiret cadratin, niveau de confiance par
affirmation, aucune reference inventee.

Convention de marquage :
- [CONFIRME] : verifie sur la source primaire, URL donnee en bibliographie.
- [PROBABLE] : lu dans une source secondaire fiable, ou deduit d'elements convergents, sans
  acces a la source primaire complete.
- [HYPOTHESE] : mon raisonnement, non verifie.
- [VENDEUR] : affirmation d'un acteur commercial, non revue par les pairs.

---

## 0. Resume executif

1. Le champ existe depuis 2022 et a produit un resultat de reference solide : des agents
   fondes sur des donnees auto rapportees riches predisent les reponses d'individus reels a
   environ 83 a 86 pour cent de la fiabilite test retest de ces memes individus
   [CONFIRME, arXiv 2411.10109].
2. **La formulation "les LLM ecrasent la variance" est trop grossiere et il faut cesser de
   l'employer telle quelle.** Le phenomene reel est une **double distorsion simultanee** : la
   variance INTRA groupe est comprimee, et les ecarts INTER groupes sont au contraire gonfles
   d'un facteur 2 a 4 [CONFIRME, arXiv 2607.26348 ; arXiv 2608.19621]. Les deux erreurs
   peuvent se compenser dans une mesure de variance totale, qui apparait alors correcte alors
   que les deux termes sont faux. Toute metrique globale passe a cote. Voir section 2.6, c'est
   la section la plus importante du document.
3. Le verrou est aujourd'hui le probleme le mieux documente et le moins bien resolu du champ.
   Il est nomme de huit facons concurrentes, et attaque par au moins sept familles de
   correctifs dont aucune ne domine les autres. Il n'existe pas de comparaison tete a tete de
   ces correctifs sur un protocole unique [CONFIRME par absence, voir section 2.5].
4. **Menace de baseline, a traiter avant tout engagement.** Sur la prediction individuelle, une
   regression logistique multinomiale sur les seules variables demographiques bat les quatre
   LLM testes : 0,622 contre 0,589 au mieux sur le GSS, et 0,393 contre 0,277 au mieux sur le
   WVS [CONFIRME, arXiv 2607.26348]. Une copule gaussienne egale 37 LLM sur la fidelite
   psychometrique [CONFIRME, arXiv 2608.14606]. Toute contribution qui ne bat pas ces
   baselines est morte. Voir section 2.7 pour l'inventaire complet et pour le seul regime ou
   le LLM gagne clairement.
5. Le verrou de la prediction individuelle est plus grave que celui de la variance
   aggregee : la meilleure etude a grande echelle sur jumeaux numeriques trouve une
   correlation moyenne de r = 0,20 entre le jumeau et l'humain sur 164 resultats
   [CONFIRME, arXiv 2509.19088]. Le plafond individuel est aussi estime a r environ 0,2 par
   une seconde equipe independante [CONFIRME, arXiv 2607.18310] et a r = 0,37 apres
   fine tuning dans une troisieme [CONFIRME, arXiv 2606.28963].
6. Point d'attention immediat : la reference donnee dans CONTEXTE.md,
   https://arxiv.org/html/2603.28066v1, ne correspond pas au papier de Stanford. Elle pointe
   vers "Synonymix: Unified Group Personas for Generative Simulations" de Huanxing Chen et
   Aditesh Kumar, soumis le 30 mars 2026 [CONFIRME]. Le papier attendu est arXiv 2411.10109.

---

## 1. Le champ : genealogie

### 1.1 Argyle, Busby, Fulda, Gubler, Rytting, Wingate (2023), "Out of One, Many"

- These : GPT-3, conditionne sur des "backstories" sociodemographiques issues de repondants
  reels, produit des "silicon samples" dont les distributions de reponse ressemblent a
  celles des sous populations humaines correspondantes. Les auteurs forgent le terme
  d'**algorithmic fidelity** [CONFIRME].
- Publication : Political Analysis, vol. 31, n. 3, p. 337 a 351, 2023. Preprint
  arXiv:2209.06899 depuis septembre 2022 [CONFIRME].
- Donnees : plusieurs vagues de l'American National Election Studies, plus une etude
  "Pigeonholing Partisans" [PROBABLE, decrit dans les resumes de la version Cambridge et du
  preprint, je n'ai pas relu la section donnees ligne a ligne].
- Resultat marquant : la structure de correlation entre attitudes, et pas seulement les
  moyennes, est retrouvee. Les auteurs insistent sur le fait que le biais du modele est
  "fin et correle aux caracteristiques demographiques" [CONFIRME].
- Limite reconnue par les auteurs : la fidelite algorithmique est une propriete du couple
  modele plus population, elle n'est ni garantie ni stable dans le temps, et doit etre
  reevaluee a chaque nouveau modele et chaque nouveau domaine [PROBABLE, c'est la formulation
  standard citee dans les reprises du papier ; je n'ai pas extrait la phrase exacte].

Importance pour nous : c'est le papier fondateur cote science politique, celui que tout
relecteur de Political Analysis attend en premiere reference.

### 1.2 Horton (2023), "Homo silicus"

- These : un LLM est un modele computationnel implicite d'un humain. On peut lui donner une
  dotation, une information, des preferences, puis observer son comportement comme un
  economiste observe l'Homo economicus [CONFIRME].
- Publication : NBER Working Paper 31122, arXiv:2301.07543, avec Apostolos Filippas et
  Benjamin Manning sur les versions recentes. Derniere revision indiquee : 27 fevrier 2026
  [CONFIRME].
- Resultat : replication qualitative de Charness et Rabin 2002, Kahneman, Knetsch et Thaler
  1986, Samuelson et Zeckhauser 1988 [CONFIRME].
- Limite reconnue : le resultat est **qualitatif**. Horton ne pretend pas a une calibration
  quantitative. Il propose explicitement les LLM comme outils de pilote experimental a bas
  cout, pas comme substituts de sujets [PROBABLE].

Importance pour nous : Horton fournit la justification economique du projet, mais il fournit
aussi l'argument des sceptiques : la valeur demontree est celle d'un generateur d'hypotheses,
pas d'un instrument de mesure.

### 1.3 Aher, Arriaga, Kalai (2023), "Turing Experiments"

- These : evaluer un modele non pas sur sa capacite a imiter un individu, mais sur sa
  capacite a reproduire la **distribution** d'un echantillon de participants. C'est le
  premier cadrage explicitement distributionnel du champ [CONFIRME].
- Publication : ICML 2023, PMLR 202, p. 337 a 371. arXiv:2208.10264. Code chez Microsoft
  Research [CONFIRME].
- Experiences repliquees : jeu de l'ultimatum, phrases a chemin de jardin, experience de
  Milgram, sagesse des foules [CONFIRME].
- Resultat critique et sous cite : sur la sagesse des foules, ils identifient une
  **"hyper-accuracy distortion"**, les modeles sont trop justes par rapport aux humains
  [CONFIRME]. C'est deja, en 2022, une observation d'ecrasement de la variance, formulee
  autrement.

Importance pour nous : c'est l'antecedent conceptuel direct du verrou de la variance. Le citer
comme tel est une bonne facon de montrer qu'on connait la genealogie du probleme et pas
seulement les papiers de 2025.

### 1.4 Park et al., generative agents

Deux etapes a distinguer.

**Etape 1, Smallville (2023).** "Generative Agents: Interactive Simulacra of Human Behavior",
25 agents dans un village simule, architecture memoire plus reflexion plus planification.
[PROBABLE, je n'ai pas refetche ce papier dans cette session, c'est un resultat largement
etabli du champ]. Ce travail ne porte pas sur la fidelite a des humains reels, il porte sur
la credibilite comportementale. Il ne doit pas etre confondu avec l'etape 2.

**Etape 2, les 1052 personnes (2024 a 2026).** C'est le papier de reference du projet.
- Reference exacte : arXiv:2411.10109, soumis le 15 novembre 2024, version 3 du 28 juin 2026,
  retitre **"LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of
  Individuals"** [CONFIRME]. Le titre d'origine, "Generative Agent Simulations of 1,000
  People", est celui qui circule encore.
- Auteurs : Joon Sung Park, Carolyn Q. Zou, Jonne Kamphorst, Niles Egan, Aaron Shaw,
  Benjamin Mako Hill, Carrie Cai, Meredith Ringel Morris, Percy Liang, Robb Willer,
  Michael S. Bernstein [CONFIRME].
- Protocole : echantillon stratifie de 1052 Americains sur age, division de recensement,
  education, ethnie, genre, revenu, quartier, ideologie politique, identite sexuelle ;
  entretien audio semi structure de deux heures suivant le schema de l'American Voices
  Project ; puis GSS, Big Five, jeux economiques, replications experimentales [CONFIRME].
- Resultats chiffres, version 3 : agents entretien seul 83 pour cent, agents enquete seule
  82 pour cent, agents combines 86 pour cent, agents demographiques seuls 74 pour cent
  [CONFIRME]. Ces pourcentages sont **normalises par la fiabilite test retest des humains a
  deux semaines**, pas des taux de bonne reponse bruts.
- Ecart avec CONTEXTE.md : le chiffre de 85 pour cent correspond aux premieres versions du
  preprint. La v3 donne 86 pour cent pour la configuration combinee et 83 pour cent pour
  l'entretien seul. **Recommandation : citer 83 a 86 pour cent selon la configuration, et
  toujours preciser "normalise par le test retest".** Un relecteur qui verifie la v3 trouvera
  la difference [CONFIRME].
- Limite reconnue par les auteurs : les agents reduisent les disparites de justesse entre
  groupes raciaux et ideologiques par rapport aux agents demographiques, mais ne les
  eliminent pas [CONFIRME]. Autrement dit, l'entretien ameliore l'equite du modele, il ne la
  resout pas.
- Acces aux donnees : Stanford annonce un acces restreint, agrege ouvert et individuel sous
  revue, via un depot institutionnel et un depot GitHub StanfordHCI/genagents. Une banque
  d'agents demographiques d'environ 3000 agents construite sur le GSS est egalement
  mentionnee [PROBABLE, decrit par Stanford HAI et le README GitHub, je n'ai pas teste la
  demande d'acces].

### 1.5 Santurkar, Durmus, Ladhak, Lee, Liang, Hashimoto (2023), OpinionQA

- These : mesurer de **qui** un modele reflete les opinions, en comparant ses reponses a des
  sondages Pew ventiles par groupe demographique [CONFIRME].
- Publication : ICML 2023. arXiv:2303.17548 [CONFIRME].
- Resultat : desalignement substantiel entre les vues des modeles et celles des groupes
  demographiques americains, d'ampleur comparable au clivage democrate republicain sur le
  climat. Le desalignement **persiste apres steering explicite** vers le groupe cible.
  Groupes les plus mal representes : 65 ans et plus, personnes veuves. Un groupe demographique
  tire au hasard est plus representatif du grand public que ne l'est le modele [CONFIRME].
- Limite reconnue : le protocole repose sur les log probabilites des options, choix
  methodologique qui sera precisement conteste plus tard par Meister et al. et par
  Dominguez-Olmedo et al. [CONFIRME, voir sections 2.4 et 4].

### 1.6 Durmus et al. (2023), GlobalOpinionQA

- Jeu de donnees de 2556 questions issues d'enquetes transnationales, avec les distributions
  de reponses de plus de 100 pays [CONFIRME].
- Trois resultats : biais par defaut vers les opinions des Etats Unis et de certains pays
  europeens et sud americains ; le prompting par pays deplace les reponses vers la population
  visee mais peut produire des stereotypes culturels nuisibles ; traduire la question dans la
  langue cible ne rapproche pas necessairement le modele des locuteurs de cette langue
  [CONFIRME].
- Jeu de donnees public sur Hugging Face, licence ouverte [CONFIRME]. Ressource directement
  exploitable a budget zero.

### 1.7 Dillion, Tandon, Gu, Gray (2023)

- Publication : Trends in Cognitive Sciences, vol. 27, n. 7, p. 597 a 600 [CONFIRME].
- These : les LLM peuvent remplacer des participants humains dans certaines conditions, mais
  quatre reserves majeures s'appliquent. Le cadrage retenu par la litterature ulterieure est
  celui d'outils de simulation pragmatiques, utiles pour le jeu de role, le test rapide
  d'hypotheses et la modelisation, pas comme substituts [CONFIRME].
- Je n'ai pas eu acces au texte integral, il est derriere le paywall Cell Press. Les quatre
  reserves precises ne sont donc pas restituees ici [limite assumee].

### 1.8 Les extensions recentes qu'il faut connaitre

- **Centaur / Psych-101** (Binz, Akata, Bethge, Brandle, Schulz et al.), Nature, vol. 644,
  p. 1002 a 1009, 28 aout 2025. Fine tuning de Llama 3.1 sur Psych-101 : 160 experiences
  psychologiques, 60 092 participants, 10 681 650 choix. Log vraisemblance negative 0,44
  contre 0,58 pour Llama non fine tune. Generalisation a des histoires de couverture inedites
  et a des domaines nouveaux [CONFIRME]. Psych-101 est public sur Hugging Face, l'adaptateur
  Centaur 70B aussi ; le jeu de test est en depot restreint sous licence CC-BY-ND-4.0
  [CONFIRME].
  Note pour Simon : c'est probablement le "precedent Nature" evoque. Ce n'est pas de la
  psychiatrie, c'est de la psychologie cognitive experimentale. Le precedent psychiatrique
  reste a identifier.
- **Twin-2K-500** (Toubia, Netzer, Peng et al.), Marketing Science 2025 et arXiv:2505.17479.
  2058 participants americains, environ 2,42 heures chacun, plus de 500 questions, 4 vagues
  dont une vague 4 qui rejoue les experiences pour donner une mesure de fiabilite test
  retest. Sur 17 taches, precision moyenne des jumeaux de 71,72 pour cent, soit 87,67 pour
  cent du plafond test retest [CONFIRME]. **Jeu de donnees public sur Hugging Face**
  [CONFIRME]. C'est la ressource la plus importante du document pour une equipe a budget zero
  qui ne peut recruter personne.
- **SubPOP** (Suh, Jahanparast, Moon, Kang, Chang), ACL 2025, arXiv:2502.16761. Voir
  section 2.4.

---

## 2. Le verrou central : la structure de variance, et pas seulement son ecrasement

Note de lecture. Les sections 2.1 a 2.5 restituent la litterature telle qu'elle se formule
elle meme, autour de l'idee d'ecrasement de la variance. **Les sections 2.6 et 2.7 corrigent
cette formulation** a partir des travaux de 2026, qui montrent que le phenomene est une double
distorsion et que les baselines statistiques battent les LLM dans le regime le plus etudie. Si
vous ne lisez qu'une chose de ce document, lisez 2.6.

### 2.1 Le vocabulaire, et pourquoi il est un probleme en soi

Le meme phenomene est nomme d'au moins huit facons dans la litterature. Aucune n'est
dominante. Termes attestes, chacun avec au moins une source [CONFIRME] :

| Terme | Source ou il est employe | Nuance |
|---|---|---|
| mode collapse | Zhang et al. arXiv 2510.01171 ; Heath et Alexander arXiv 2607.28550 | vient du vocabulaire des GAN, insiste sur la concentration sur un mode |
| variance collapse | Ozkan arXiv 2607.18310 | insiste sur le second moment |
| homogenization | Alexander? non, Ma et al. arXiv 2507.02919 | insiste sur la sous representation des minorites |
| distributional alignment | Meister, Guestrin, Hashimoto, NAACL 2025 | cadrage positif, c'est la propriete recherchee |
| range restriction | Lukauskas et Sarkauskaite arXiv 2608.14606 | vocabulaire psychometrique, ratio d'ecarts types |
| over-regularization | Qin, Li, Cheng arXiv 2604.06663 | insiste sur l'exces d'ordre, pas seulement l'exces de concentration |
| insufficient individuation | Peng et al. arXiv 2509.19088 | insiste sur le fait que les jumeaux ne se distinguent pas assez |
| hyper-accuracy distortion | Aher, Arriaga, Kalai, ICML 2023 | premiere formulation historique |
| identity essentialism | Ling et al. arXiv 2608.19621 ; Lin arXiv 2402.04470 | nomme la **cause** et non le symptome : l'identite est traitee comme trop predictive |
| between-segment gap inflation | Chen, Zhu, Zheng arXiv 2607.26348 | nomme le **second** symptome, l'exageration des ecarts inter groupes |

Consequence operationnelle : **il n'existe pas de terme canonique, donc pas de revue
systematique unifiee du phenomene, donc pas de comparaison des correctifs.** C'est une
opportunite de contribution a part entiere, voir section 5, angle A.

Le couple "portrait contre distribution" n'est pas un terme technique atteste dans la
litterature que j'ai lue [limite assumee]. En revanche, **le mot "caricature" a maintenant un
equivalent technique chiffre** : le gap inflation factor de Chen, Zhu et Zheng, qui mesure de
combien le modele exagere l'ecart entre deux segments demographiques [CONFIRME,
arXiv 2607.26348]. Peng et al. listent le stereotyping comme distorsion numero 2, Tao et al.
montrent que le prompting culturel produit des stereotypes, et un audit sur 41 professions
documente une "exageration de stereotype" croissante avec la segregation reelle du metier
[CONFIRME]. Voir la section 2.6, entierement consacree a ce second symptome.

### 2.2 De combien la variance est elle ecrasee ? Les chiffres

C'est la question centrale de la commande. Voici tout ce que j'ai pu chiffrer.

**Ozkan (2026), World Values Survey Turquie et GSS** [CONFIRME, arXiv 2607.18310] :
- Concentration modale passant de 0,36 dans les donnees humaines a 0,69 dans les agents.
- **85 pour cent des unites de population s'effondrent sur l'option par defaut du modele.**
- Distance de variation totale entre distribution simulee et distribution observee : 0,44.
- Entropie des reponses : 1,46 chez les humains, 0,77 chez les agents. Soit une perte de
  47 pour cent d'entropie.
- Ratio d'ecarts types simule sur observe avant correction : **0,40 a 0,56**. C'est le chiffre
  le plus directement utilisable pour repondre a "de combien la variance est elle ecrasee" :
  l'ecart type simule vaut environ la moitie de l'ecart type reel, donc la variance vaut
  environ le quart.
- Severite de l'effondrement correlee a la structure du scenario, r = 0,55.
- Modeles testes : Qwen 3.6-35B, GLM-5.2, Gemma-4-26B. Donnees : WVS-7 Turquie,
  2414 repondants, dont 77 pour cent ont un profil de valeurs unique ; GSS vagues 2016 a 2022.

**Lukauskas et Sarkauskaite (2026), audit psychometrique, 37 modeles** [CONFIRME,
arXiv 2608.14606] :
- Ratio d'ecart type intra item sigma_LLM sur sigma_humain : restriction d'etendue observee
  sur l'ensemble des modeles. Le papier ne publie pas un chiffre unique dans les elements que
  j'ai pu extraire, il publie un score composite.
- Score de similarite psychometrique PSS : reference copule gaussienne 0,69, meilleur LLM
  0,71, plafond humain sur echantillon retenu 0,825.
- **Homogeneite inter modeles : PSS moyen de 0,73 entre deux LLM differents, superieur au PSS
  entre un LLM et les humains.** Deux modeles differents se ressemblent plus entre eux qu'ils
  ne ressemblent aux humains. C'est le resultat le plus derangeant du papier.
- Validite predictive sur humains retenus : R2 = -0,18 pour les donnees synthetiques, contre
  R2 = 0,28 pour des donnees humaines d'entrainement. Un R2 negatif signifie que le modele
  entraine sur du synthetique fait pire que la moyenne.
- Decalage d'acquiescement : +0,84 ecart type par rapport aux humains.
- Correlation inter items : copule r = 0,99, meilleur LLM r = 0,94.
- **La copule gaussienne, qui n'utilise aucun LLM, fait aussi bien que le meilleur des 37
  modeles.** Conclusion des auteurs : l'essentiel de la fidelite psychometrique d'un LLM est
  recuperable a partir de la structure de covariance humaine.
- Donnees : 263 salaries lituaniens, 68 items, 12 sous echelles ; environ 65 000
  questionnaires synthetiques generes.

**Bisbee, Clinton, Dorff, Kenkel, Larson (2024), Political Analysis** [CONFIRME pour le
resultat qualitatif, arXiv non disponible, article Cambridge] :
- Les moyennes des thermometres de sentiment generes par ChatGPT pour 11 groupes
  sociopolitiques correspondent de pres aux moyennes de l'ANES 2016 a 2020.
- La dispersion est **artificiellement faible**, ce qui rend toute inference statistique par
  tirages repetes trompeusement precise.
- Je n'ai pas pu extraire le ratio de variance exact, l'article est derriere le paywall
  Cambridge [limite assumee].

**Ma et al. (2025), representativite et coherence structurelle** [CONFIRME, arXiv 2507.02919] :
- Deux defauts : incoherence structurelle, la justesse ne se maintient pas d'un niveau
  d'agregation demographique a l'autre ; homogeneisation, les points de vue minoritaires sont
  significativement sous representes.
- Hypothese des auteurs : "accuracy-optimization hypothesis", les LLM privilegient les
  reponses statistiquement communes, ce qui supprime mecaniquement la diversite.
- Modeles : GPT-4, Llama 3 en 8B, 70B et 405B. Donnees : ANES 2020, avortement et immigration.

**Chiffre a manier avec precaution** : une vulgarisation publiee sur Towards Data Science
rapporte qu'un modele Llama-3 place 95 pour cent des repondants simules dans une fenetre de
deux points de pourcentage, la ou les reponses reelles s'etalent d'environ moins 25 a plus 27
[PROBABLE, source de vulgarisation, je n'ai pas identifie le papier primaire correspondant].
Ne pas citer tel quel dans un dossier MIT sans avoir retrouve la source primaire.

**Chen, Zhu, Zheng (2026)** [CONFIRME, arXiv 2607.26348] : quatre modeles, GSS et WVS. Ecarts
inter segments gonfles d'un facteur median de 2,3 (GSS) et 2,5 (WVS), etendue 1,3 a 4,7 selon
les modeles. Detail complet en section 2.6.

**Synthese chiffree defendable aujourd'hui** [PROBABLE, agregation de mes lectures] :
- Variance **intra** segment : l'ecart type simule vaut **40 a 60 pour cent** de l'ecart type
  observe, soit une variance reduite d'un facteur 3 a 6.
- Ecarts **inter** segments : gonfles d'un facteur **2 a 4**.
- Entropie des reponses : chute d'environ **la moitie**.
- Correlation individuelle : plafond autour de **r = 0,2** sans fine tuning, **r = 0,37** avec.
- Structure de grappes : score de silhouette **0,19** pour les agents contre **-0,02** pour les
  humains.

**Attention.** Les deux premiers points vont en sens opposes. Ils ne s'additionnent pas en un
"ecrasement de la variance". Voir section 2.6.

### 2.3 Les metriques employees

Inventaire des metriques attestees, avec qui les utilise [CONFIRME sauf indication] :

- **Distance de Wasserstein d'ordre 1** : Suh et al. ACL 2025 (metrique principale de SubPOP,
  choisie parce qu'elle respecte l'ordinalite des echelles de Likert) ; Lukauskas et
  Sarkauskaite 2026 ; Williams et al. arXiv 2601.15755.
- **Divergence de Jensen Shannon** : Lukauskas et Sarkauskaite 2026.
- **Divergence de Kullback Leibler** : Heath et Alexander 2026 ; Qin et al. 2026 ; Suh et al.
  utilisent la KL directe comme fonction de perte de fine tuning.
- **Statistique D de Kolmogorov Smirnov** : Lukauskas et Sarkauskaite 2026.
- **Distance de variation totale (TVD)** : Ozkan 2026 ; le score de fidelite y est defini
  comme 1 moins TVD.
- **Ratio d'ecarts types sigma_sim / sigma_obs** : Ozkan 2026 ; Lukauskas et Sarkauskaite 2026
  (sous le nom de "within-item SD ratio").
- **Entropie des reponses et concentration modale** : Ozkan 2026.
- **Earth Mover's Distance normalisee inter groupes** : Qin et al. 2026, pour mesurer la
  separation entre sous groupes, pas seulement la dispersion intra groupe. Distinction
  importante et sous exploitee.
- **Coefficient de concordance de Lin (CCC)** : Choi et al. arXiv 2606.28963, pour la fidelite
  structurelle.
- **Cramer's V** : Qin et al. 2026, pour la fidelite predictive relationnelle.
- **Metriques psychometriques** : alpha de Cronbach, omega de McDonald, phi de Tucker
  (congruence factorielle), HTMT, ICC(1) pour le test retest, decomposition bifactorielle.
  Lukauskas et Sarkauskaite 2026. Ce sont les metriques les plus exigeantes du champ, et le
  seul papier qui les applique systematiquement.
- **Correlation de Pearson individu a individu** : Peng et al. 2025 ; Choi et al. 2026.

Observation : **la moitie des papiers ne rapportent que des distances distributionnelles, qui
peuvent etre bonnes alors meme que la variance est ecrasee.** Une distance de Wasserstein
faible sur une distribution unimodale est compatible avec un ecrasement massif de la
dispersion inter individuelle si la moyenne est juste. Ozkan est explicite sur ce point : il
publie fidelity_score et SD-ratio separement et refuse de les fusionner [CONFIRME]. C'est un
point de methode dont nous devrions faire un principe.

### 2.4 Les solutions proposees, et leur efficacite mesuree

Six familles, classees de la moins a la plus efficace selon ce que j'ai pu lire.

**a) Reglage de la temperature et du top p.** Peu efficace [CONFIRME pour la direction,
sources partielles].
- Sur une tache de generation d'idees, passer de la temperature 1,0 a 1,5 fait passer de 22 a
  23 categories et de 88 a 99 combinaisons uniques, une amelioration marginale ; a
  temperature 2,0 le texte degenere [PROBABLE, arXiv 2602.20408, lu via extrait de recherche].
- Sur une tache de simulation, passer de 0,8 a 1,5 fait varier le F1 de 0,596 a 0,591 et le
  RMSE de 0,584 a 0,572, soit moins de 2 pour cent [PROBABLE, meme source].
- Interpretation : la temperature augmente le bruit lexical, pas la diversite semantique des
  positions. Elle ne cree pas d'individus differents, elle cree le meme individu qui hesite.
  [HYPOTHESE, c'est mon interpretation, elle est coherente avec les chiffres mais aucun
  papier lu ne la formule ainsi.]

**b) Personas enrichis et conditionnement demographique fin.** Effet incertain, parfois
negatif [CONFIRME].
- Kambhatla et al. 2026 : le prompting sociodemographique "conduit souvent a un alignement
  d'opinion comparable ou meme inferieur au prompting sans aucune information
  sociodemographique" [CONFIRME, arXiv 2507.00439].
- Qin et al. 2026 : augmenter la granularite ne produit pas d'amelioration consistante ; les
  configurations parcimonieuses egalent ou depassent les configurations completes ; un exces
  d'identifiants degrade la fidelite structurelle et predictive sur les deux modeles testes
  [CONFIRME, arXiv 2604.06663].
- Park et al. 2026 : les agents demographiques plafonnent a 74 pour cent contre 83 pour cent
  pour les agents entretien [CONFIRME]. Donc la richesse aide, mais c'est la richesse
  **narrative et auto rapportee**, pas la richesse demographique.
- Ozkan 2026 identifie un mecanisme : quand le persona est detaille et que les items se
  ressemblent en surface, le modele traite le persona comme une direction unique et coherente,
  ce qu'il appelle persona-collapse. Il identifie aussi un ancrage sur le premier point de
  l'echelle de Likert choisi dans l'appel [CONFIRME].

**c) Echantillonner la distribution plutot que le mode, et prompting distributionnel.**
Efficace, et c'est la piste la mieux etayee [CONFIRME].
- **Meister, Guestrin, Hashimoto, NAACL 2025.** Trois methodes d'expression de la
  distribution comparees : log probabilites, sequences de 30 tokens echantillonnees,
  verbalisation directe en JSON. Resultat : demander au modele de **verbaliser** la
  distribution bat systematiquement le fait de la lui faire echantillonner. Ecart
  connaissance vers simulation : GPT-3.5 perd 9,17 pour cent, GPT-4 perd 21,35 pour cent,
  Claude Opus perd 43,63 pour cent quand on passe de verbaliser a echantillonner
  [CONFIRME]. Les meilleurs modeles en verbalisation atteignent 0,226 (Opus), 0,229 (GPT-4),
  0,244 (Llama 3 70B) contre un baseline humain de 0,250 plus ou moins 0,004, sur une
  metrique ou plus bas vaut mieux [CONFIRME]. Autrement dit, **un LLM verbalisant une
  distribution predit mieux la distribution d'opinions d'un groupe qu'un humain moyen ne le
  fait**, ce qui est un point de vente redoutable et un point de vigilance : le baseline
  humain est bas parce que les humains sont mauvais a cet exercice ("Perception Gap"), pas
  parce que le modele est bon.
- Consequence methodologique majeure : **les mesures historiques du desalignement, fondees
  sur les log probabilites, sous estiment systematiquement la capacite distributionnelle des
  modeles** [CONFIRME]. Cela relativise en partie Santurkar et al. 2023.

**d) Verbalized Sampling (Zhang et al., arXiv 2510.01171).** Efficace, mais sur corrige quand
on l'applique aux sondages [CONFIRME].
- Principe : demander au modele de produire k reponses **avec leurs probabilites**, plutot
  qu'une reponse. Sans entrainement. Explication theorique : le mode collapse vient d'un
  **typicality bias** dans les donnees de preference, les annotateurs preferant
  systematiquement le texte familier.
- Resultat principal : diversite multipliee par 1,6 a 2,1 en ecriture creative, sans perte de
  factualite ni de securite. Les modeles plus capables en beneficient davantage [CONFIRME].
  Accepte a ICML 2026 [PROBABLE, page poster ICML trouvee].
- Application aux populations, Ozkan 2026 : VS ameliore la fidelite de +6,8 a +10,1 points
  sur trois familles de modeles, **mais sur corrige universellement** : le ratio d'ecarts
  types passe de 0,40 a 0,56 (trop peu de variance) a 1,26 a 1,37 (trop de variance). Sur
  Qwen, p = 0,002, d = 6,2 [CONFIRME]. VS ne calibre pas, il inverse le signe de l'erreur.
  Il souligne aussi que les items binaires resistent a la calibration.

**e) Calibration a posteriori.** Efficace, peu couteux, et sous exploite [CONFIRME].
- **Kambhatla et al. 2026, arXiv 2507.00439.** Regression supervisee appliquee a la
  distribution brute du LLM pour la transformer vers la distribution humaine, puis
  renormalisation. Amelioration moyenne de **16,3 pour cent** de l'alignement d'opinion.
  Amelioration constatee dans **94,8 pour cent** des combinaisons jeu de donnees fois modele
  fois methode d'elicitation. **1 a 10 exemples de reference suffisent.** 15 variantes de
  modeles sur Claude, Llama, Mistral, OLMo-2, Qwen ; 92 questions ; trois jeux de donnees,
  Wellcome Global Monitor, OpinionQA, World Values Survey [CONFIRME]. Limites reconnues : le
  modele de calibration traite les modalites de reponse comme independantes, ce qui peut sur
  lisser ; peu d'analyse d'intersectionnalite.
- **Heath et Alexander 2026, Semantic Similarity Rating (SSR), arXiv 2607.28550.** Au lieu de
  demander un chiffre, on demande du **texte libre**, puis on projette ce texte sur une
  echelle numerique via des embeddings et une similarite cosinus a des ancres (0, 25, 50, 75,
  100). Resultat : divergence KL de 1,97 a **0,07** pour Claude sur l'ANES 2016 ; les ecarts
  types synthetiques se rapprochent des ecarts types reels ; l'erreur absolue moyenne reste
  stable, donc la forme de la distribution est corrigee sans sacrifier la justesse. Un
  parametre de temperature de projection T = 0,25 appris sur 2016 generalise a 2020.
  Modeles : DeepSeek-v4-flash, Claude-sonnet-5, GPT-5.4-mini [CONFIRME]. Limite reconnue :
  SSR corrige la variance, pas les biais systematiques, notamment la tendance a l'opinion
  extreme sur les groupes controverses.
  **C'est, a ma lecture, le correctif le plus elegant publie a ce jour, et il est
  reproductible a budget zero puisqu'il ne demande que des embeddings et l'ANES public.**

**f) Fine tuning distributionnel.** Le plus efficace, le plus couteux [CONFIRME].
- **SubPOP, Suh et al., ACL 2025, arXiv:2502.16761.** Jeu de donnees de 3362 questions et
  70 000 paires sous population vers reponse, environ 6,5 fois OpinionQA. Entrainement sur
  l'American Trends Panel, evaluation sur le GSS, donc transfert entre institutions
  d'enquete. Perte : divergence KL directe sur la distribution complete, pas sur le mode.
  Resultat : reduction de **32 a 46 pour cent** de la distance de Wasserstein par rapport aux
  baselines de prompting ; **38 a 54 pour cent** d'amelioration relative sur les 22 sous
  groupes demographiques ; generalisation a des sous populations absentes de l'entrainement
  [CONFIRME]. Modeles : Llama-2 7B et 13B, Mistral 7B, Llama-3 70B. Limite reconnue par les
  auteurs : ils ne savent pas expliquer pourquoi le modele generalise si bien.
- **Choi et al. 2026, "Beyond the Mean", arXiv 2606.28963.** LoRA plus tete MLP sur Qwen3-8B,
  calibre sur un pilote de 5 pour cent (n = 74) d'une enquete coreenne de 1466 personnes sur
  la desinformation COVID. Fidelite structurelle CCC 0,85 en bivarie et 0,78 en MCO ; EMD
  marginale 0,17 ; **fidelite individuelle r = 0,37 seulement, soit environ 14 pour cent de
  la variance inter repondants** [CONFIRME]. Deux resultats a retenir : deux tetes de sortie
  sur le meme backbone donnent des fidelites "drastiquement" differentes ; et la fidelite
  s'effondre sur certains sous groupes, le CCC tombant de 0,85 a 0,40 chez les repondants
  conservateurs.
- **Kim et Lee, AI-Augmented Surveys, arXiv:2305.09620**, revision de mai 2026. Fine tuning
  avec embeddings de question, de repondant et de periode, sur le GSS 1972 a 2021. Deux
  taches : retrodiction d'opinions masquees, et prediction d'opinions jamais posees. Les
  auteurs annoncent des performances fortes en retrodiction et **modestes en prediction
  d'opinions non posees** [CONFIRME]. Les metriques chiffrees ne figurent pas dans le resume
  accessible [limite assumee].

**g) Segmentation d'audience et melanges de personas.** Ameliore, ne resout pas [CONFIRME].
- Qin, Li, Cheng 2026, arXiv 2604.06663 : six configurations de segmentation, de
  demographique seule a instrument valide en 4 items, sur 594 reponses americaines sur le
  climat, avec Llama 3.1-70B et Mixtral 8x22B. La logique instrumentale preserve le mieux la
  forme distributionnelle, la selection pilotee par les donnees recupere le mieux la structure
  inter groupes. **Mais toutes les configurations conservent une sur regularisation
  persistante : les reponses simulees restent artificiellement ordonnees** [CONFIRME].
- Polypersona, arXiv 2512.14562, IEEE BigData 2025 : LoRA plus quantification 4 bits sur
  TinyLlama 1.1B, 433 personas, 10 domaines, 3568 reponses. Evalue en BLEU, ROUGE, BERTScore,
  plus des metriques de coherence structurelle. **Ce papier n'evalue pas la fidelite
  distributionnelle a une population reelle** [CONFIRME]. Utile comme reference d'ingenierie
  a petit budget, pas comme reference scientifique sur la variance.

### 2.5 Ce qui n'a pas ete essaye, ou ce qui a echoue

Cette section est la plus importante du document pour la suite du projet.

**Ce qui a echoue, avec preuve :**
1. La temperature comme levier de variance. Effet inferieur a 2 pour cent sur les metriques de
   simulation, degeneration du texte au dela de 1,5 [PROBABLE].
2. Le conditionnement demographique fin comme levier de variance. Souvent nul, parfois
   negatif [CONFIRME, Kambhatla et al. ; Qin et al.].
3. Verbalized Sampling applique tel quel aux sondages. Sur correction systematique, ratio
   d'ecarts types passant de 0,4 a 1,3 [CONFIRME, Ozkan].
4. Le steering explicite vers un groupe demographique comme correctif du desalignement. Le
   desalignement persiste [CONFIRME, Santurkar et al.].
5. La justification du LLM par sa superiorite sur une baseline statistique simple. Une copule
   gaussienne egale 37 LLM sur la fidelite psychometrique [CONFIRME, Lukauskas et
   Sarkauskaite].

**Ce que je n'ai trouve chez personne, apres recherche ciblee. A traiter comme une absence
provisoire, pas comme une preuve d'absence :**

1. **Aucune comparaison tete a tete des correctifs sur un protocole unique.** Temperature,
   personas, VS, SSR, calibration supervisee, segmentation, fine tuning distributionnel : ces
   six familles n'ont jamais ete evaluees ensemble, sur les memes enquetes, avec les memes
   metriques, sur les memes modeles. Chaque papier compare son correctif a un baseline naif.
   [CONFIRME par absence dans mes recherches, non exhaustif.]
2. **Aucune decomposition explicite des sources de variance.** La variance d'une population
   simulee a au moins quatre sources : la variance entre segments demographiques, la variance
   entre personas d'un meme segment, la variance entre appels pour un meme persona
   (stochasticite du decodage), et la variance de mesure du modele lui meme. Les papiers
   melangent les quatre. Personne, a ma connaissance, ne publie une decomposition de type
   ANOVA ou modele a effets mixtes de ces composantes. [CONFIRME par absence dans mes
   recherches.] Chen et al. mesurent le terme inter segments et Ozkan le terme intra, mais
   dans deux papiers differents, sur deux protocoles differents, sans decomposition commune.
2 bis. **Aucun correctif formule comme un transport de variance a somme constante**, depuis le
   terme inter segments (trop gros) vers le terme intra segment (trop petit). Tous les
   correctifs publies dilatent ou compriment globalement. Voir section 2.6.3 point 4.
   [CONFIRME par absence, c'est le trou le plus specifique que j'aie identifie.]
3. **Aucun modele de mesure latent explicite.** L'approche psychometrique standard, la theorie
   de reponse a l'item, consisterait a tirer un trait latent theta par individu depuis une
   distribution calibree sur des donnees reelles, puis a demander au LLM de produire la
   reponse conditionnellement a theta. Personne ne le fait a ma connaissance. Les papiers
   corrigent la sortie (SSR, calibration) ou l'entree (personas), pas le **modele generatif
   sous jacent**. [CONFIRME par absence, c'est l'angle le plus prometteur, voir section 5.]
4. **Aucune combinaison SSR plus calibration supervisee.** Heath et Alexander corrigent la
   forme, Kambhatla et al. corrigent la position. Les deux sont orthogonaux et personne ne les
   a composes. [CONFIRME par absence.]
5. **Aucune injection de bruit structuree.** La litterature evoque le bruit via la temperature
   uniquement. Personne n'injecte un bruit dont la structure de covariance est estimee sur des
   donnees humaines reelles, ce qui est pourtant exactement ce que fait la copule gaussienne
   qui bat les 37 LLM. [CONFIRME par absence.]
5 bis. **Aucune comparaison des correctifs a des baselines statistiques.** Sur les sept familles
   de correctifs recensees en 2.4, aucune n'est evaluee contre une regression logistique sur
   demographies, un lookup demographique ou une copule. Elles se comparent toutes a un
   prompting naif. Or Chen et al. montrent que le prompting naif est en dessous de la
   regression logistique. **Une amelioration de 16 pour cent sur un baseline deja battu par
   une regression logistique ne prouve rien.** [CONFIRME par absence, voir section 2.7.]
6. **Aucune etude de la variance sous contrainte de budget d'appels.** Ozkan est le seul a
   noter que sa methode distribution-first coute O(1) au lieu de O(N) [CONFIRME]. Personne ne
   publie de courbe fidelite contre cout. Pour un projet qui vise 10 000 a 20 000 agents,
   c'est une question centrale et un angle de publication a part entiere.

---

### 2.6 La double distorsion : compression intra groupe et amplification inter groupes

**C'est la section la plus importante du document.** Elle corrige une formulation que le projet
utilisait, et elle contient probablement la contribution reelle.

#### 2.6.1 Le constat

La formulation naive "les LLM ecrasent la variance" est **fausse par insuffisance**. Ce que la
litterature de 2026 documente est une **double distorsion simultanee et de sens oppose** :

- **Compression intra groupe.** A l'interieur d'un meme segment demographique, les agents se
  ressemblent trop. Ratio d'ecarts types de 0,40 a 0,56 [CONFIRME, arXiv 2607.18310] ;
  85 pour cent des unites s'effondrent sur l'option par defaut [CONFIRME, meme source] ;
  restriction d'etendue mesuree sur 37 modeles [CONFIRME, arXiv 2608.14606].
- **Amplification inter groupes.** Entre segments demographiques, les ecarts sont **gonfles
  d'un facteur 2 a 4** [CONFIRME, arXiv 2607.26348]. Le modele caricature la difference entre
  un jeune urbain et un retraite rural.

Les deux mouvements ont la meme cause profonde : le modele traite l'identite demographique
comme **beaucoup plus predictive de l'attitude qu'elle ne l'est reellement**. Chen, Zhu et
Zheng ecrivent que les modeles "sur determinent les demographies, traitant l'identite comme
bien plus predictive des attitudes qu'elle ne l'est chez les vraies personnes", et que la
distorsion est presente pour "presque toutes les combinaisons question fois groupe"
[CONFIRME, arXiv 2607.26348].

Le nom que la litterature commence a donner a ce mecanisme est **identity essentialism**
[CONFIRME, arXiv 2608.19621]. C'est aussi, exactement, la cinquieme des six erreurs de Zhicheng
Lin, "essentializing identities" [CONFIRME, arXiv 2402.04470]. Le lien entre la critique
conceptuelle de Lin en 2024 et la mesure empirique de 2026 ne semble pas avoir ete fait
explicitement dans la litterature [CONFIRME par absence]. Le faire est deja une contribution
de cadrage.

#### 2.6.2 Les chiffres de la double distorsion

**Chen, Zhu, Zheng (2026), "When Synthetic Users Fail", arXiv:2607.26348, 28 juillet 2026.**
Quatre modeles de deux familles, de 8B a frontiere, sur le General Social Survey et le World
Values Survey [CONFIRME].
- Facteur de gonflement defini par les auteurs : gap_inflation = gap_modele / gap_humain.
- **Mediane 2,3 fois sur le GSS et 2,5 fois sur le WVS pour le modele frontiere (Sonnet).**
- **Etendue tous modeles : 1,3 a 4,1 fois sur le GSS, 2,0 a 4,7 fois sur le WVS.**
- Taux de mauvaise cible (le modele designe le mauvais segment comme celui qui repond le plus
  haut) : **50 pour cent des cas GSS, 72 pour cent des cas WVS**.
- Taux de scission fallacieuse (les humains montrent un ecart inferieur ou egal a 0,10, le
  modele montre un ecart superieur ou egal a 0,25) : **jusqu'a 41 pour cent sur le WVS**.
- Les auteurs precisent que les modeles plus gros et plus capables **ne corrigent pas** la
  defaillance.

**Ling et al. (2026), LifeMem, arXiv:2608.19621.** La mesure la plus elegante de la double
distorsion trouvee a ce jour [CONFIRME].
- Sur le World Values Survey, les agents LLM ont un **score de silhouette de 0,19**, ce qui
  signifie des grappes demographiques nettes et bien separees. Les humains reels ont un score
  de silhouette de **-0,02**, ce qui signifie des groupes qui se recouvrent presque
  completement.
- Traduction : chez les humains, savoir a quel segment demographique appartient une personne
  ne permet quasiment pas de deviner sa position. Chez les agents, cela la determine.
- **Un score de silhouette est exactement le ratio entre separation inter groupes et
  dispersion intra groupe. C'est donc, en une seule statistique, la mesure de la double
  distorsion.** Je recommande d'en faire une metrique standard du projet.

**Convergence d'autres sources** [CONFIRME sauf indication] :
- Audit multi modeles de personas generees sur 41 professions, arXiv 2510.21011 :
  "exageration de stereotype", l'ecart au reel croissant avec la segregation reelle de la
  profession. Deplacement demographique uniforme **plus** amplification des asymetries
  existantes.
- Peng et al., arXiv 2509.19088 : distorsion 1 "individuation insuffisante" (compression intra
  groupe) et distorsion 2 "stereotypage" (amplification inter groupes) figurent cote a cote
  dans la meme liste de cinq. Les auteurs ne les articulent pas comme un couple.
- Morocho, Cima, Fagni, Avvenuti, Cresci (2026), arXiv 2602.18462, ACM Web Conference 2026 :
  le conditionnement demographique "redistribue les erreurs de facon inegale entre groupes",
  degradant particulierement les groupes sous representes. Recommandation des auteurs :
  **auditer par item et par sous groupe, ne jamais se fier au score agrege** [CONFIRME].
- Ma et al., arXiv 2507.02919 : "incoherence structurelle", la justesse ne se maintient pas
  d'un niveau d'agregation a l'autre [CONFIRME]. C'est la signature statistique attendue d'une
  double distorsion : un modele juste au niveau national et faux au niveau des cellules.

#### 2.6.3 Pourquoi cela change tout, y compris nos metriques

Formulation propre, a reprendre telle quelle dans le papier [HYPOTHESE dans sa formulation,
mais chacun de ses termes est [CONFIRME]] :

> Soit une population decomposee en segments. La variance totale se decompose en variance
> intra segment plus variance inter segments. Les LLM conditionnes sur des personas
> **sous estiment le premier terme d'un facteur 3 a 6 et sur estiment le second d'un facteur 2
> a 4**. Une metrique qui n'observe que la variance totale, ou que la distance entre la
> distribution simulee et la distribution observee au niveau de la population entiere, peut
> donc renvoyer un score correct alors que les deux composantes sont fausses en sens opposes.

Consequences operationnelles immediates :

1. **Toute metrique globale est disqualifiee comme metrique unique.** Wasserstein sur la
   distribution nationale, TVD globale, MAE agregee : necessaires, jamais suffisantes.
2. **Le jeu de metriques minimal du projet doit contenir au moins trois nombres separes** :
   (a) ratio d'ecarts types **intra segment**, sigma_intra_sim / sigma_intra_obs ; (b) ratio
   d'ecarts **inter segments**, gap_sim / gap_obs, c'est a dire le gap inflation factor de
   Chen et al. ; (c) une statistique jointe, le score de silhouette de Ling et al. ou un ratio
   eta carre. Les publier separement, jamais fusionnes. C'est le principe methodologique
   d'Ozkan generalise.
3. **Cela reconcilie des resultats qui paraissaient contradictoires.** Meister et al. trouvent
   les LLM meilleurs que les humains sur l'alignement distributionnel par groupe ; Chen et al.
   trouvent les LLM battus par une regression logistique au niveau individuel. Les deux sont
   vrais : le modele connait bien les moyennes de groupe, et il croit a tort que ces moyennes
   determinent les individus. [HYPOTHESE, c'est ma reconciliation, aucun papier ne l'ecrit.]
4. **Cela reoriente le correctif.** Si le probleme etait uniquement la compression, il fallait
   ajouter de la variance. Comme le probleme est aussi l'amplification inter groupes, ajouter
   de la variance globalement peut aggraver la caricature. **Le correctif doit etre un
   transport, pas une dilatation** : deplacer de la variance depuis le terme inter groupes vers
   le terme intra groupe, a variance totale constante. Je n'ai trouve aucun papier qui formule
   le correctif ainsi [CONFIRME par absence]. **C'est, a mon jugement, la contribution
   scientifique la plus specifique et la plus defendable que le projet puisse revendiquer.**

#### 2.6.4 Le seul correctif publie qui vise explicitement la double distorsion

**LifeMem (arXiv:2608.19621)** [CONFIRME].
- Principe : remplacer le profil demographique statique par une **trajectoire de vie
  longitudinale**. Deux memoires : une memoire structuree d'evenements de vie horodates avec
  embeddings semantiques et score de pertinence decroissante ; une memoire parametrique sous
  forme d'adaptateurs LoRA specifiques a l'agent, mis a jour vague apres vague.
- Resultats : reduction de 30 a 50 pour cent de la divergence KL par rapport a un RAG
  d'evenements seul ; les ecarts de distance intra groupe se resserrent vers les valeurs
  humaines ; meilleure reproduction des transitions de reponse entre vagues adjacentes.
- Donnees : 100 repondants d'Add Health et d'Understanding Society. Trois backbones : Llama,
  Ministral, Qwen.
- Limites reconnues : les trajectoires d'enquete sont des representations partielles, a pas de
  temps grossier, avec biais de rappel.
- **Lecture pour nous** : LifeMem attaque la cause (l'essentialisme identitaire) par
  l'enrichissement de l'entree. Le correctif par transport de variance que je propose au point
  4 ci dessus attaquerait la meme cause par la sortie. Les deux sont complementaires et
  personne ne les a composes.

---

### 2.7 La menace de baseline : ce qu'il faut battre

Section defensive. Elle repond a la question : quel niveau de performance un modele statistique
sans LLM atteint il, et donc quel est le seuil sous lequel notre contribution ne vaut rien ?

#### 2.7.1 Inventaire des baselines non LLM attestees dans la litterature

| Baseline | Ce que c'est | Ou elle est utilisee | Performance atteinte |
|---|---|---|---|
| Marginale de question | predit la modalite la plus frequente, toutes personnes confondues | Chen et al. 2026 | GSS 0,568 ; WVS 0,348 [CONFIRME] |
| Devinette aleatoire | tirage uniforme ou selon la marge | Twin-2K-500 ; Morocho et al. 2026 | 59,17 pour cent sur Twin-2K-500 ; 27,3 pour cent sur WVS-7 [CONFIRME] |
| Lookup demographique | distribution conditionnelle observee dans la cellule demographique, avec repli du fin vers le grossier | Chen et al. 2026 | GSS 0,589 ; WVS 0,388 [CONFIRME] |
| Regression logistique multinomiale | ajustee par question sur les demographies encodees en one hot | Chen et al. 2026 | **GSS 0,622 ; WVS 0,393** [CONFIRME] |
| Foret aleatoire | 300 arbres sur les memes variables demographiques | Chen et al. 2026 | GSS 0,583 ; WVS 0,366 [CONFIRME] |
| Copule gaussienne | modele de dependance ajuste sur la matrice de covariance humaine | Lukauskas et Sarkauskaite 2026 | PSS 0,69 contre 0,71 pour le meilleur des 37 LLM ; r inter items 0,99 contre 0,94 [CONFIRME] |
| Gaussienne multivariee | idem, sans copule | Lukauskas et Sarkauskaite 2026 | rapportee, chiffre non extrait [limite] |
| Retourneur de moyenne de strate | renvoie la moyenne de la cellule demographique | Lukauskas et Sarkauskaite 2026 | rapportee, chiffre non extrait [limite] |
| k plus proches voisins sur repondants (k=5) | cherche les 5 repondants humains les plus similaires | Lukauskas et Sarkauskaite 2026 ; Holtdirk et al. 2026 | rapportee, chiffre non extrait [limite] |
| MICE PMM (imputation multiple par appariement de moyenne predite) | standard de l'imputation en statistique d'enquete | Holtdirk et al. 2026 | erreur absolue 0,068 (MCAR), 0,092 (MAR), 0,068 (MNAR) ; couverture 0,96 [CONFIRME] |
| MICE Forest | variante LightGBM de MICE | Holtdirk et al. 2026 | rapportee, chiffre non extrait [limite] |
| Imputation par le mode | remplace par la modalite la plus frequente | Holtdirk et al. 2026 | rapportee, chiffre non extrait [limite] |
| Plus proches voisins par embeddings | voisins semantiques plutot que demographiques | Holtdirk et al. 2026 | rapportee, chiffre non extrait [limite] |

#### 2.7.2 Le verdict, regime par regime

**Regime 1 : persona demographique, prediction individuelle. Le LLM PERD.** [CONFIRME]
- GSS : meilleur LLM 0,589 (Claude Sonnet style C, egal au lookup demographique) contre 0,622
  pour la regression logistique. Le plus mauvais LLM, Llama-3.1-8B, tombe a 0,496, sous la
  marginale de question (0,568).
- WVS : meilleur LLM 0,277 contre 0,393 pour la regression logistique. **Le meilleur LLM fait
  30 pour cent de moins bien que la regression logistique, et fait moins bien que la simple
  marginale de question (0,348).** Sur les metriques sensibles a la distance, l'erreur absolue
  moyenne des modeles est de 1,83 a 2,27 contre 1,74 pour la baseline.
- Chen et al. concluent que "aucun LLM ne bat meme la baseline la plus forte" au niveau
  individuel.
- Ce regime est exactement celui d'Argyle et al. 2023 et de la plupart des travaux de silicon
  sampling. **C'est le regime qu'il ne faut pas choisir comme terrain de bataille.**

**Regime 2 : fidelite psychometrique multi items. Match nul.** [CONFIRME]
- Copule 0,69 contre 0,71 pour le meilleur des 37 LLM. Ecart de 0,02 point, et la copule ne
  coute rien en inference.

**Regime 3 : distribution d'un groupe, verbalisee. Le LLM GAGNE, mais contre un baseline
humain, pas statistique.** [CONFIRME]
- Meister et al. : 0,226 pour Opus contre 0,250 pour l'humain moyen. **Aucune baseline
  statistique n'est incluse dans cette comparaison** [CONFIRME]. C'est une faiblesse du papier
  et une opportunite pour nous : refaire la comparaison avec une baseline lookup
  demographique. Il est possible que le lookup gagne. Personne ne l'a teste
  [CONFIRME par absence].

**Regime 4 : imputation avec exemples reels en contexte. Le LLM GAGNE nettement.** [CONFIRME]
- Holtdirk, Ahnert, Sakshaug, Haensch (2026), arXiv:2606.09351, OpinionQA, 15 vagues de
  l'American Trends Panel, 150 variables, plus de 700 scenarios d'evaluation.
- gpt-oss-120b avec **100 exemples en contexte** : erreur absolue 0,033 (MCAR), 0,044 (MAR),
  0,048 (MNAR), contre 0,068, 0,092 et 0,068 pour MICE PMM. **Soit une erreur divisee par
  deux dans deux des trois regimes de donnees manquantes.**
- Intervalles de confiance deux a cinq fois plus etroits que MICE PMM, pour une couverture
  d'environ 0,92 contre 0,96. Attention : des intervalles plus etroits avec une couverture
  legerement plus faible, c'est exactement la signature d'un exces de confiance qu'ont decrit
  Bisbee et al. Il faut lire ce resultat avec prudence.
- **Ce quatrieme regime est le plus important resultat de cette section.** Il dit que le LLM
  n'est pas competitif comme *simulateur d'un individu a partir de ses demographies*, mais
  qu'il est superieur a l'etat de l'art statistique comme *imputeur conditionne sur des
  repondants reels similaires*. La difference tient a la nature de l'information fournie :
  categories abstraites contre exemples concrets.
- Meme direction chez Park et al. : agents demographiques 74 pour cent, agents nourris de
  donnees auto rapportees riches 82 a 86 pour cent [CONFIRME].

#### 2.7.3 Ce que cela impose au projet

1. **Toute experience du projet doit inclure, au minimum, quatre baselines** : marginale de
   question, lookup demographique, regression logistique multinomiale, copule gaussienne. Elles
   coutent quelques lignes de code et leur absence est un motif de rejet.
2. **Ne pas se battre dans le regime 1.** Predire l'individu a partir de ses demographies seules
   est un combat perdu contre la regression logistique, et perdu pour une raison structurelle :
   les demographies expliquent peu, et le LLM leur fait dire trop.
3. **Se battre dans les regimes 3 et 4**, c'est a dire la ou le LLM apporte quelque chose que la
   statistique n'a pas : du texte, des exemples concrets, du transfert entre enquetes, et des
   cellules demographiques trop peu peuplees pour qu'un modele statistique s'y ajuste. **C'est
   precisement la ou l'angle E (hybride copule plus LLM) se situe.**
4. **Reformuler l'objectif du projet.** L'objectif defendable n'est pas "le LLM predit mieux",
   il est "le LLM produit une population synthetique dont la structure de variance est correcte
   la ou aucun modele statistique ne peut etre ajuste faute de donnees". Le point de comparaison
   devient la degradation des baselines quand la taille de cellule diminue.
   [HYPOTHESE, c'est mon jugement, mais il decoule directement des chiffres ci dessus.]

---

## 3. Les autres verrous

### 3.1 Biais WEIRD et populations non occidentales

**Ampleur mesuree** [CONFIRME] :
- Tao, Viberg, Baker, Kizilcec, PNAS Nexus 3(9), pgae346, 2024. Cinq modeles GPT compares au
  World Values Survey. Les valeurs par defaut des modeles ressemblent a celles des pays
  anglophones et protestants europeens. GPT-4o est le plus proche de la Finlande (distance
  0,20) et le plus eloigne de la Jordanie (4,10), de la Libye (4,00) et du Ghana (3,95). Soit
  un facteur 20 entre le pays le mieux represente et le pays le plus mal represente.
- Durmus et al. : biais par defaut vers les Etats Unis, l'Europe et l'Amerique du Sud ; la
  traduction dans la langue cible ne corrige pas [CONFIRME].
- Santurkar et al. : meme a l'interieur des Etats Unis, les 65 ans et plus et les veufs sont
  mal representes [CONFIRME].

**Remedes connus et leur efficacite** [CONFIRME] :
- Le **cultural prompting** ameliore l'alignement pour 71 a 81 pour cent des pays sur GPT-4 et
  posterieurs. Distance moyenne GPT-4o de 2,42 a 1,57, GPT-4-turbo de 2,71 a 1,77, GPT-4 de
  2,69 a 1,65. Mais il **echoue ou aggrave pour 19 a 29 pour cent des pays**, et certains pays
  europeens voient leur biais augmenter. Les auteurs ecrivent explicitement que "le cultural
  prompting n'est pas une panacee".
- Ozkan choisit deliberement la Turquie comme terrain non WEIRD et retrouve l'effondrement
  variantiel, ce qui suggere que les deux verrous se cumulent [CONFIRME].

### 3.2 Sycophancie et desirabilite sociale

**Ampleur mesuree** [CONFIRME] :
- Salecha et al., PNAS Nexus 3(12), pgae533, 2024, et arXiv:2405.06058. Quand un LLM infere
  qu'il est evalue sur sa personnalite, il deplace ses scores vers le pole desirable :
  extraversion en hausse, nevrosisme en baisse. **GPT-4 se deplace de 1,20 ecart type,
  Llama 3 de 0,98 ecart type.** Ce sont des tailles d'effet enormes. Le biais est present sur
  GPT-4 et 3.5, Claude 3, Llama 3 et PaLM-2, et **semble croitre avec les modeles recents**.
- Le recodage inverse des items reduit le biais sans l'eliminer, donc ce n'est pas de
  l'acquiescement pur [CONFIRME].
- Lukauskas et Sarkauskaite mesurent un decalage d'acquiescement de +0,84 ecart type par
  rapport aux humains sur leur echantillon [CONFIRME].

**Remedes connus** : le forced choice apparie en desirabilite est propose dans un preprint de
2026 [PROBABLE, arXiv 2602.17262, je n'ai pas fetche le detail]. Le recodage inverse aide
partiellement. Je n'ai trouve **aucun remede dont l'efficacite soit chiffree et repliquee**
[limite assumee].

**Implication directe pour popsim** : sur des questions politiques ou morales sensibles, la
sycophancie et l'ecrasement de la variance vont dans le meme sens, vers la reponse consensuelle
et acceptable. Ils sont probablement partiellement confondus dans les mesures existantes.
[HYPOTHESE, non testee dans la litterature que j'ai lue, et c'est un angle de contribution.]

### 3.3 Derive temporelle et date de coupure

C'est le verrou le **moins bien documente** de la liste. Constat honnete.

- Fait de base : la coupure d'entrainement precede la sortie de plusieurs mois. Exemple cite
  dans la litterature : coupure d'octobre 2023 pour GPT-4o sorti en mai 2024, soit 7 mois
  [PROBABLE, cite dans arXiv 2504.01167].
- Il existe des travaux sur la derive de connaissance temporelle en general et sur la
  coherence des croyances des agents dans le temps (BeliefShift, arXiv 2603.23848 ;
  "Geometry of Forgetting", arXiv 2605.09195) [PROBABLE, resumes lus, pas les papiers].
- **Je n'ai trouve aucune etude qui mesure la degradation de la fidelite d'un silicon sample
  en fonction de l'ecart temporel entre la coupure du modele et la vague d'enquete a
  predire.** C'est un test simple, entierement realisable sur donnees publiques, et personne
  ne semble l'avoir publie [CONFIRME par absence dans mes recherches].
- Element indirect : Kim et Lee montrent que leur modele suit la montee du soutien au mariage
  entre personnes de meme sexe dans le GSS 1972-2021, mais c'est de la retrodiction sur des
  annees anterieures a la coupure, ce qui ne teste pas la derive [CONFIRME].
- Element indirect fort : Heath et Alexander apprennent leur parametre de projection sur
  l'ANES 2016 et le generalisent a l'ANES 2020 [CONFIRME]. Cela suggere qu'une correction de
  forme est temporellement stable sur 4 ans, mais ne dit rien de la correction de position.

### 3.4 Contamination des donnees d'entrainement

Constat honnete : **je n'ai trouve aucune etude dediee a la contamination du GSS, de l'ANES ou
du WVS dans les corpus d'entrainement des LLM.** La litterature sur la contamination de
benchmarks est abondante mais porte sur les benchmarks NLP [CONFIRME par absence].

Ce que j'ai trouve d'exploitable :
- Ozkan 2026 conduit un **test placebo** et conclut que ses resultats de prediction par sous
  groupe sont "contamines par le rappel du modele". Son modele predit le resultat electoral
  officiel avec une TVD de 0,051, ce qu'il attribue explicitement a la memorisation et non a
  la simulation [CONFIRME]. C'est le protocole le plus proche d'un test de contamination
  specifique aux enquetes que j'aie trouve.
- Lukauskas et Sarkauskaite listent la fuite d'instruments ("possible instrument leakage")
  comme limite explicite : les echelles IWPQ, ATC et UWES-17 sont validees et publiees, donc
  probablement dans les corpus [CONFIRME].
- Suh et al. contournent partiellement le probleme en entrainant sur l'American Trends Panel
  et en evaluant sur le GSS, donc sur une autre institution d'enquete [CONFIRME]. Ce n'est pas
  un test de contamination, c'est un test de transfert.
- La litterature generale sur la contamination indique des taux atteignant 91,8 pour cent sur
  des benchmarks multilingues populaires et une croissance avec la taille du modele
  [PROBABLE, arXiv 2406.04244 et suivants, lus via extraits].

**Reponse a la question "si le GSS est dans le corpus, que vaut la prediction ?"** : la
question n'a pas de reponse publiee. Elle est **entierement testable a budget zero** :
comparer la performance sur des items dont la distribution est publiee en ligne avec des items
dont la distribution ne l'est pas, comparer avant et apres coupure, et faire un test placebo
avec des sous groupes fictifs. Voir section 5, angle D.

### 3.5 Fidelite par domaine

C'est la question qui conditionne le choix de la premiere dimension a modeliser. Voici ce que
j'ai pu chiffrer, en gardant a l'esprit que **les metriques ne sont pas comparables d'un
papier a l'autre** [avertissement important].

| Domaine | Resultat chiffre | Source | Confiance |
|---|---|---|---|
| Opinion politique agregee, Etats Unis | moyennes proches de l'ANES, dispersion trop faible | Bisbee et al. 2024 | CONFIRME |
| Opinion politique, distribution par groupe | modeles verbalisant a 0,226 contre 0,250 pour le baseline humain | Meister et al. 2025 | CONFIRME |
| Opinion publique, distributions sous populations, apres fine tuning | Wasserstein reduite de 32 a 46 pour cent | Suh et al. 2025 | CONFIRME |
| Cognition experimentale | log vraisemblance negative 0,44 contre 0,58 | Binz et al., Nature 2025 | CONFIRME |
| Comportement individuel multi domaines (jumeaux) | r moyen 0,20 sur 164 resultats | Peng et al. 2025 | CONFIRME |
| Attitudes sociales americaines (GSS), niveau individuel | meilleur LLM 0,589 contre 0,622 pour une regression logistique | Chen et al. 2026 | CONFIRME |
| Valeurs transculturelles (WVS), niveau individuel | meilleur LLM 0,277 contre 0,393 pour une regression logistique, et 0,348 pour la simple marginale | Chen et al. 2026 | CONFIRME |
| Imputation d'opinions avec 100 exemples reels en contexte | erreur absolue 0,033 a 0,048 contre 0,068 a 0,092 pour MICE PMM | Holtdirk et al. 2026 | CONFIRME |
| Consommation, disposition a payer | "parfois comparables aux etudes humaines, souvent inexactes, parfois de signe inverse" | Brand, Israeli, Ngwe | CONFIRME |
| Psychometrie du travail | R2 predictif negatif (-0,18) | Lukauskas et Sarkauskaite 2026 | CONFIRME |
| Sante, politiques de prevention du suicide | erreur absolue moyenne de 23 points de pourcentage sur 811 560 prompts | Perez et al., NLP+CSS 2026 | CONFIRME |
| Vie privee, comportement individuel | 40,4 pour cent de justesse pour le meilleur modele | PrivacySim, arXiv 2605.12147 | PROBABLE |
| Moral, comparaison transnationale | sur estimation des preoccupations occidentales, sous estimation ailleurs | PNAS, moral stereotyping | PROBABLE, article inaccessible (403) |

**Lecture pour le projet** [HYPOTHESE, c'est mon jugement, pas un resultat publie] :
- Le domaine le plus favorable est l'**opinion politique et sociale agregee dans un pays
  occidental**, parce que c'est celui ou la matiere d'entrainement est la plus dense, ou les
  jeux de donnees publics sont les meilleurs (ANES, GSS, ESS, Eurobarometre) et ou les
  correctifs existants sont deja calibres.
- Le domaine le plus rentable commercialement, la consommation, est **precisement celui ou les
  resultats publies sont les plus mauvais** (signes inverses sur la disposition a payer). Il y
  a la un ecart entre le pitch commercial de CONTEXTE.md et l'etat de l'art.
- Les domaines sensibles (sante, suicide, moral) cumulent erreur elevee, refus et sycophancie.
  A eviter pour un premier papier.
- **Nuance apportee par Chen et al.** : meme sur le terrain politique americain, le plus
  favorable, le LLM ne bat pas une regression logistique au niveau individuel. Le terrain
  transculturel (WVS) est nettement pire. **Le choix du domaine doit donc etre double** : un
  domaine favorable (politique et social, terrain occidental) ET un regime favorable
  (distribution de groupe verbalisee, ou imputation avec exemples reels en contexte), jamais la
  prediction individuelle a partir des seules demographies.
- **Recommandation** : premiere dimension = opinion politique et sociale, terrain europeen ou
  americain, sur donnees publiques, en regime distributionnel ou d'imputation. Deuxieme
  dimension = consommation, mais presentee comme une contribution sur un domaine difficile, pas
  comme une demonstration facile.

### 3.6 Sensibilite au format, effet d'ordre, refus

**Ampleur mesuree** [CONFIRME] :
- Pezeshkpour et Hruschka, NAACL Findings 2024, arXiv:2308.11483 : ecarts de performance de
  **13 a 85 pour cent** selon l'ordre des options, y compris en few-shot.
- Dominguez-Olmedo, Hardt, Mendler-Dunner, NeurIPS 2024, arXiv:2306.07951 : sur **43 modeles**,
  biais d'ordre et d'etiquetage forts, preference marquee pour l'option A. **Apres
  randomisation de l'ordre, les modeles produisent des reponses uniformement aleatoires,
  independamment de leur taille et de leurs donnees de pre entrainement.** Les auteurs en
  deduisent que les modeles paraissent mieux representer les sous groupes dont les
  statistiques agregees sont les plus proches de l'uniforme. C'est une remise en cause
  frontale des resultats de type OpinionQA.
- Tjuatja, Chen, Wu, Talwalkar, Neubig, TACL 2024 : sur 9 modeles, les LLM **ne reproduisent
  pas** les biais de reponse humains connus des methodologues d'enquete (effets de formulation,
  d'ancrage, d'ordre de question), et les modeles passes par RLHF sont les pires. Quand un
  modele bouge dans la meme direction qu'un humain, il bouge aussi sur des perturbations qui
  ne font pas bouger les humains [CONFIRME].

**Refus** [CONFIRME] : Perez et al. 2026 rapportent que les motifs de refus varient
considerablement selon l'architecture et le design de prompt, sur un domaine sensible. Le refus
est un mecanisme de censure de la queue de distribution : les positions extremes sont celles
qui declenchent le refus, donc le refus contribue mecaniquement a l'ecrasement de la variance.
[HYPOTHESE, l'articulation refus vers variance n'est pas, a ma connaissance, quantifiee dans la
litterature. Angle de contribution.]

### 3.7 Stabilite et fiabilite test retest des personas

**Resultats contradictoires** [CONFIRME] :
- Lukauskas et Sarkauskaite 2026 : ICC(1) de test retest **mediane 0,85** sur 37 modeles, avec
  une validation par 20 repetitions. C'est eleve, comparable ou superieur a la fiabilite
  humaine.
- Un cadre a double evaluation trouve les personas "remarquablement stables" entre et a
  l'interieur des conversations, sur 7 modeles et 3 designs de prompt [PROBABLE,
  arXiv 2601.22812, resume lu].
- A l'inverse, une etude de personnalite dans Royal Society Open Science 11(10), 240180, 2024,
  conclut a une **stabilite temporelle limitee** avec une prosocialite accentuee
  [PROBABLE, resume lu].
- PICon, arXiv 2603.25620 : l'ordre des questions suffit a destabiliser les reponses d'un
  agent persona ; passer en decodage glouton et melanger l'ordre n'ameliore pas
  systematiquement la stabilite [PROBABLE, resume lu].

**Lecture** [HYPOTHESE] : la contradiction est probablement apparente. Un modele peut etre tres
stable sur ce qu'il **dit de lui meme** (auto description du persona) et instable sur ce qu'il
**repond** a des items, surtout quand l'ordre change. La distinction stabilite declarative
contre stabilite comportementale n'est pas faite proprement dans la litterature. Angle de
contribution.

Note importante pour le projet : **une fiabilite test retest tres elevee (ICC 0,85) est un
symptome d'ecrasement de la variance, pas un signe de qualite.** Un humain a une fiabilite test
retest imparfaite ; c'est d'ailleurs le denominateur de la normalisation de Park et al. Un
agent trop stable est un agent qui n'a pas la variabilite intra individuelle humaine.

---

## 4. Les critiques de fond

Section a lire integralement avant de rediger quoi que ce soit pour le MIT. Ces objections
seront celles des relecteurs.

### 4.1 "Les modeles ne repondent pas, ils devinent" (Dominguez-Olmedo et al., NeurIPS 2024)

L'objection la plus destructrice du champ. Apres correction du biais d'ordre, 43 modeles
produisent des reponses **uniformement aleatoires**. Les alignements demographiques observes
dans la litterature seraient alors un artefact : les modeles paraissent bien representer les
groupes dont les distributions reelles sont proches de l'uniforme [CONFIRME].
Ce que cela impose au projet : toute mesure d'alignement doit etre accompagnee d'un test de
robustesse a la permutation des options, et d'une comparaison a une baseline uniforme. Sans
cela, le papier est rejetable en l'etat.

### 4.2 "Les resultats dependent des choix de pipeline" (Cummins, AMPPS 2026)

Jamie Cummins, "The threat of analytic flexibility in using large language models to simulate
human data", Advances in Methods and Practices in Psychological Science, 2026, preprint
arXiv:2509.13397 [CONFIRME].
- Etude 1 : **252 configurations** testees sur des echelles psychologiques.
- Etude 2 : reanalyse d'une recherche publiee avec **66 configurations alternatives**. La
  correlation entre donnees synthetiques et donnees humaines varie de **r = 0,23 a r = 0,84**
  selon la configuration.
- Conclusion : les choix methodologiques peuvent a eux seuls fabriquer la validite apparente
  d'un echantillon de silicium.
Ce que cela impose au projet : preenregistrement, ou a defaut publication d'une **specification
curve** couvrant l'espace des choix. C'est un cout, et c'est aussi un avantage competitif si on
est parmi les premiers a le faire proprement.

### 4.3 "Six erreurs d'interpretation" (Lin, 2024 a 2025)

Zhicheng Lin, "Six Fallacies in Substituting Large Language Models for Human Participants",
arXiv:2402.04470, v5 juin 2025 [CONFIRME]. Les six :
1. Assimiler la prediction de tokens a l'intelligence humaine.
2. Traiter le LLM comme l'humain moyen.
3. Interpreter l'alignement comme une explication.
4. Anthropomorphiser.
5. Essentialiser les identites (le point le plus dangereux pour un projet qui conditionne sur
   des categories demographiques).
6. Substituer des donnees de modele a des preuves humaines.
Conclusion de Lin : outil de simulation pragmatique, valide contre des donnees humaines, pas
substitut.

### 4.4 "Les jumeaux numeriques sont des miroirs deformants" (Peng et al., 2025 a 2026)

Le papier le plus lourd empiriquement contre le projet, et il vient d'une equipe Columbia
Business School qui n'est pas hostile au champ [CONFIRME, arXiv:2509.19088, v5 avril 2026].
- **19 etudes preenregistrees, 164 resultats**, jumeaux entraines sur plus de 500 reponses
  individuelles.
- Les jumeaux ne sont que "modestement plus precis" qu'un LLM de base homogene.
- **Correlation moyenne avec les reponses humaines : r = 0,20.**
- Cinq distorsions : individuation insuffisante, stereotypage, biais de representation, biais
  ideologique, hyper rationalite.
Ce que cela impose au projet : la promesse commerciale de CONTEXTE.md, "5 pour cent de marge
d'erreur", n'est defendable qu'au **niveau agrege**, et seulement apres calibration. Elle n'est
pas defendable au niveau individuel. Il faut le dire explicitement dans le pitch, sinon le
premier client qui verifie detruit la credibilite.

### 4.5 "L'illusion utopique" (Bian et al., 2025)

arXiv:2510.21180 [CONFIRME pour l'existence et le cadrage general ; je n'ai pas pu extraire les
chiffres precis du PDF]. Argument : les simulations sociales par LLM ne reproduisent pas les
biais cognitifs, les effets de conformite sociale et les heuristiques humaines, et les
societes simulees sont systematiquement plus harmonieuses que les societes reelles. C'est le
meme phenomene que l'ecrasement de la variance, applique aux dynamiques de groupe plutot qu'aux
distributions de reponses.

### 4.6 "La copule suffit" (Lukauskas et Sarkauskaite, 2026)

Deja cite, mais c'est aussi une critique de fond et pas seulement une mesure. Si un modele
statistique classique sans aucun LLM atteint un PSS de 0,69 la ou le meilleur des 37 LLM
atteint 0,71, alors la valeur ajoutee du LLM sur la fidelite psychometrique est de 0,02 point
[CONFIRME]. Tout papier du projet devra inclure une baseline statistique non LLM, sinon le
relecteur la demandera.

### 4.7 "Une regression logistique fait mieux" (Chen, Zhu, Zheng, 2026)

La critique la plus recente et la plus operationnelle. Sur le GSS et le WVS, aucun des quatre
LLM testes ne bat la meilleure baseline non LLM au niveau individuel : 0,589 au mieux contre
0,622 pour une regression logistique multinomiale sur le GSS, 0,277 au mieux contre 0,393 sur le
WVS [CONFIRME, arXiv 2607.26348]. S'y ajoute le gonflement des ecarts inter segments d'un
facteur 2 a 4, qui conduit a designer le mauvais segment cible dans 50 pour cent des cas GSS et
72 pour cent des cas WVS. Les auteurs precisent que **la taille du modele ne corrige rien**.
Traitement complet en section 2.7. Ce que cela impose : toute experience du projet inclut les
quatre baselines statistiques, et le projet ne se bat pas sur la prediction individuelle a
partir des seules demographies.

### 4.8 Ce que la critique ne dit PAS, et qui protege le projet

Par honnetete symetrique :
- Aucune de ces critiques ne conteste que les LLM approchent bien les **moyennes** agregees
  [CONFIRME, Bisbee et al. le disent explicitement].
- Meister et al. montrent que la mesure historique par log probabilites **sous estimait** les
  modeles, donc une partie du pessimisme du champ est un artefact de mesure [CONFIRME].
- Suh et al. et Choi et al. montrent que le fine tuning distributionnel deplace reellement
  l'aiguille (32 a 54 pour cent de reduction d'erreur) [CONFIRME].
- Park et al. montrent que la matiere auto rapportee riche fait passer de 74 a 86 pour cent
  [CONFIRME].
- **Holtdirk et al. montrent que dans le regime a exemples reels en contexte, un modele ouvert
  divise par deux l'erreur de MICE PMM, standard de l'imputation statistique d'enquete**
  [CONFIRME, arXiv 2606.09351]. Donc la defaite face aux baselines n'est pas generale, elle est
  specifique au regime "persona demographique".
La position defendable est donc : **le probleme n'est pas que les LLM ne savent rien des
populations, c'est qu'on leur fait produire des populations dont la structure de variance est
fausse dans les deux sens, et qu'on les emploie dans le seul regime ou une regression logistique
suffit.** C'est exactement le positionnement du projet.

---

## 5. Ou est notre place : espaces de contribution

12 angles. Chacun avec le verrou attaque, l'etat de l'art depasse, et un jugement de
faisabilite sous les contraintes dures de CONTEXTE.md : budget zero, aucun humain recrute,
donnees publiques et modeles ouverts uniquement.

Legende de faisabilite : **A** = faisable dans les semaines qui viennent avec un ordinateur
portable et des offres gratuites ; **B** = faisable mais demande du GPU gratuit type Colab ou
Kaggle et plusieurs semaines ; **C** = demande une ressource qu'on n'a pas.

---

### Angle A. Le banc d'essai unifie des correctifs de variance. Faisabilite A.
- **Verrou attaque** : ecrasement de la variance.
- **Etat de l'art depasse** : les six familles de correctifs (temperature, personas, VS, SSR,
  calibration supervisee, fine tuning) n'ont jamais ete comparees sur un protocole unique
  [CONFIRME par absence]. Chaque papier se compare a un baseline naif.
- **Contenu** : un protocole, trois enquetes publiques (ANES, GSS, ESS ou WVS), quatre modeles
  ouverts, sept correctifs, un jeu de metriques fixe et separe : position via Wasserstein,
  dispersion **intra segment** via ratio d'ecarts types, exageration **inter segments** via le
  gap inflation factor, statistique jointe via le score de silhouette, forme via TVD et
  entropie, structure via correlations inter items. **Plus les quatre baselines statistiques
  obligatoires de la section 2.7.3** : marginale de question, lookup demographique, regression
  logistique multinomiale, copule gaussienne. Chen et al. montrent que sans elles le banc
  d'essai ne prouve rien, puisque le prompting naif auquel tous les correctifs se comparent est
  lui meme sous la regression logistique [CONFIRME].
- **Faisabilite** : elevee. Tout est public. Les modeles ouverts tournent en local en 7B a 8B,
  ou gratuitement via des offres d'inference gratuites. Le cout est du temps de calcul, pas de
  l'argent.
- **Valeur** : c'est le papier de survey empirique qui manque au champ. Il est citable par tout
  le monde, il positionne l'equipe comme reference, et il produit mecaniquement le classement
  dont nous avons besoin pour la suite. **C'est mon premier choix.**
- **Risque** : quelqu'un d'autre peut le publier avant nous. Le champ va vite.

### Angle B. La decomposition de la double distorsion. Faisabilite A.
- **Verrou attaque** : le verrou central, par la mesure. C'est le socle de tout le reste.
- **Etat de l'art depasse** : Ozkan mesure la compression intra groupe, Chen et al. mesurent
  l'amplification inter groupes, Ling et al. donnent une statistique jointe (silhouette). **Les
  trois sont dans trois papiers differents, sur trois protocoles differents, et personne ne
  publie la decomposition complete** [CONFIRME par absence]. Personne non plus ne separe la
  variance entre personas d'un meme segment de la variance entre appels pour un meme persona.
- **Contenu** : modele a effets mixtes a quatre composantes sur un plan croise segment fois
  persona fois item fois repetition fois modele. Sortie : un tableau qui donne, par domaine et
  par modele, sigma_intra_sim / sigma_intra_obs, gap_sim / gap_obs, le score de silhouette
  compare a celui des humains, et la part de variance due au seul decodage.
- **Faisabilite** : elevee. Le seul cout est le nombre d'appels : plusieurs repetitions par
  persona, donc N fois K appels. Avec un modele local 7B a 8B, c'est du temps machine, pas de
  l'argent.
- **Valeur** : c'est le fondement conceptuel du projet, et c'est le papier qui permet ensuite de
  revendiquer un correctif. Il produit aussi le vocabulaire dont le champ manque.
- **Risque** : faible. Le resultat est interessant quel qu'il soit.

### Angle C. SSR generalise, et compose avec la calibration supervisee. Faisabilite A.
- **Verrou attaque** : ecrasement de la variance, sur la forme et la position simultanement.
- **Etat de l'art depasse** : Heath et Alexander (SSR) corrigent la forme sur l'ANES seul, avec
  trois modeles proprietaires ; Kambhatla et al. corrigent la position. **Personne ne compose
  les deux** [CONFIRME par absence].
- **Contenu** : reproduire SSR avec des embeddings ouverts (sentence-transformers, e5, bge),
  sur des modeles ouverts, hors ANES (WVS, ESS, Eurobarometre), puis appliquer la calibration
  supervisee de Kambhatla par dessus avec 1 a 10 exemples de reference.
- **Faisabilite** : elevee. SSR ne demande que des embeddings, qui tournent sur CPU.
- **Valeur** : forte. Reproduction hors echantillon d'un resultat recent, plus une composition
  nouvelle. C'est un papier court et propre.
- **Risque** : SSR pourrait ne pas se reproduire hors ANES. Ce serait alors un resultat negatif,
  publiable dans un venue de reproductibilite.

### Angle D. Le test de contamination et de derive temporelle. Faisabilite A.
- **Verrous attaques** : contamination, derive temporelle. Deux verrous d'un coup.
- **Etat de l'art depasse** : aucune etude dediee a la contamination des enquetes sociales
  [CONFIRME par absence] ; aucune courbe de degradation en fonction de l'ecart a la coupure
  [CONFIRME par absence]. Ozkan fait un test placebo ponctuel, pas une etude systematique.
- **Contenu** : pour un modele ouvert dont la date de coupure est documentee, predire les
  memes items sur des vagues anterieures et posterieures a la coupure (GSS a des vagues
  regulieres, l'ESS a 11 vagues, l'Eurobarometre est semestriel). Tracer la fidelite en
  fonction du delta temporel. Ajouter un test placebo avec des sous groupes fictifs et des
  items inventes. Ajouter un contraste entre items dont les marges sont publiees en ligne et
  items dont les marges ne le sont pas.
- **Faisabilite** : elevee. Les modeles ouverts documentent leur coupure, ce qui est un
  avantage decisif sur les modeles proprietaires. Donnees entierement publiques.
- **Valeur** : tres forte. C'est la premiere objection que posera un relecteur de Political
  Analysis ou de PNAS. Avoir la reponse chiffree avant qu'il la pose vaut beaucoup. Et le
  resultat conditionne la viabilite commerciale : si la fidelite se degrade vite apres la
  coupure, le produit a une date de peremption.
- **Risque** : faible.

### Angle E. La baseline statistique honnete, et l'hybride copule plus LLM. Faisabilite A.
- **Verrou attaque** : le verrou central, par une voie que la litterature vient d'ouvrir sans
  l'exploiter.
- **Etat de l'art depasse** : Lukauskas et Sarkauskaite montrent qu'une copule gaussienne egale
  37 LLM, et s'arretent la [CONFIRME]. Personne n'a propose l'hybride evident : le LLM fournit
  les marges conditionnelles par sous groupe (ce qu'il fait bien), un modele de dependance
  classique fournit la structure de covariance (ce que le LLM fait mal).
- **Contenu** : generateur en deux etages. Etage 1, le LLM verbalise les marges par item et par
  sous groupe. Etage 2, une copule ou un modele graphique estime sur des donnees publiques
  reelles impose la structure de dependance et la dispersion. Comparaison a chaque etage seul.
- **Faisabilite** : elevee. La copule s'estime en quelques lignes de Python sur des microdonnees
  publiques.
- **Valeur** : tres forte, et c'est celui qui me parait le plus original des angles faisables.
  Il repond directement a la critique "la copule suffit" en la transformant en composant.
- **Risque** : moyen. Il faut que l'apport du LLM soit demontrable, c'est a dire que l'hybride
  batte la copule seule sur des sous groupes ou les donnees reelles sont rares. C'est
  precisement le cas d'usage a viser : les cellules demographiques peu peuplees.

### Angle F. Le modele de mesure latent, ou l'agent a trait tire. Faisabilite B.
- **Verrou attaque** : le verrou central, a la racine generative plutot qu'en correction de
  sortie.
- **Etat de l'art depasse** : tous les correctifs existants agissent sur l'entree (personas) ou
  sur la sortie (SSR, calibration). **Aucun n'introduit de variable latente individuelle tiree
  d'une distribution calibree** [CONFIRME par absence].
- **Contenu** : pour chaque agent, tirer un trait latent theta depuis une distribution estimee
  par theorie de reponse a l'item sur des microdonnees publiques reelles, verbaliser ce theta
  dans le prompt sous une forme comprehensible ("sur les questions d'immigration vous etes plus
  restrictif que 78 pour cent des Francais"), et demander la reponse conditionnelle. La
  variance de la population simulee est alors imposee par construction, et la question devient
  celle de la coherence entre theta et les reponses produites.
- **Faisabilite** : moyenne. L'IRT sur donnees publiques est standard. Le cout est le nombre
  d'appels et la conception du verbaliseur de theta.
- **Valeur** : tres forte. C'est un pont explicite entre psychometrie et LLM, exactement le
  terrain de Simon (double casquette psychologie et IA), et exactement le genre de contribution
  qui interesse un laboratoire du MIT.
- **Risque** : moyen. Il est possible que le modele ignore le quantile verbalise, ou qu'il le
  sur interprete et produise des reponses caricaturales. C'est un resultat interessant dans les
  deux cas.

### Angle G. Cartographie de la fidelite par domaine, a metrique constante. Faisabilite B.
- **Verrou attaque** : fidelite par domaine, et par consequent le choix de la premiere dimension
  monetisable.
- **Etat de l'art depasse** : les chiffres par domaine existent mais sont **incomparables**
  entre eux, chaque papier ayant sa metrique et son terrain (voir tableau 3.5) [CONFIRME].
- **Contenu** : meme protocole, meme metrique, meme modeles, sur quatre domaines : politique,
  consommation, sante, moral. Sources publiques : ANES et ESS pour le politique, les modules
  consommation de l'ESS ou des enquetes de budget publiques pour la consommation, le Health
  Information National Trends Survey ou l'Eurobarometre sante pour la sante, le World Values
  Survey pour le moral.
- **Faisabilite** : moyenne. Le travail d'appariement des instruments est long.
- **Valeur** : forte, et directement operationnelle pour le go to market.
- **Risque** : moyen. Le risque est de produire une carte plate, tous les domaines se valant.

### Angle H. Le refus comme censure de la queue de distribution. Faisabilite B.
- **Verrous attaques** : refus, sycophancie, variance. Le lien entre les trois n'est pas
  quantifie.
- **Etat de l'art depasse** : Perez et al. mesurent des taux de refus variables sans les relier
  a la forme de la distribution [CONFIRME] ; Salecha et al. mesurent la desirabilite sociale
  sans la relier a la variance [CONFIRME].
- **Contenu** : mesurer, item par item, la correlation entre le taux de refus, le decalage de
  desirabilite et le ratio d'ecarts types. Hypothese testable : les items ou le modele refuse
  le plus sont ceux ou il ecrase le plus la variance, parce que le refus supprime
  preferentiellement les positions extremes.
- **Faisabilite** : moyenne. Il faut des items sensibles, donc des enquetes qui en contiennent,
  et il faut gerer proprement les refus dans le calcul des distributions.
- **Valeur** : forte, parce que cela unifie deux verrous que la litterature traite separement,
  et parce que cela donne un levier : si le refus explique une part de l'ecrasement, alors les
  modeles moins alignes, ou les modeles ouverts non censures, devraient mieux disperser. C'est
  un test decisif et personne ne l'a publie a ma connaissance.
- **Risque** : moyen.

### Angle I. Fidelite contre cout : la courbe qui manque. Faisabilite B.
- **Verrou attaque** : passage a l'echelle 10 000 a 20 000 agents.
- **Etat de l'art depasse** : Ozkan est le seul a noter le O(1) contre O(N) [CONFIRME].
  Personne ne publie de courbe fidelite contre budget d'appels ou contre taille de modele.
- **Contenu** : pour chaque correctif, tracer la fidelite obtenue en fonction du nombre
  d'appels et de la taille du modele. Question centrale : vaut il mieux 20 000 agents faits
  par un 7B ou 500 agents faits par un 70B ?
- **Faisabilite** : moyenne. C'est du temps de calcul, donc gratuit mais long.
- **Valeur** : forte, et c'est **la** question que posera un investisseur comme un relecteur
  interesse par la reproductibilite.
- **Risque** : faible.

### Angle J. Fine tuning distributionnel sur des enquetes europeennes. Faisabilite B a C.
- **Verrou attaque** : variance et biais WEIRD simultanement.
- **Etat de l'art depasse** : SubPOP est entraine sur l'American Trends Panel et evalue sur le
  GSS, donc entierement americain [CONFIRME]. Personne n'a fait l'equivalent sur l'European
  Social Survey ou l'Eurobarometre a ma connaissance.
- **Contenu** : QLoRA sur un modele 7B a 8B ouvert, perte KL sur les distributions par sous
  population, entrainement sur l'Eurobarometre, evaluation sur l'ESS, ce qui reproduit le
  transfert inter institutions de SubPOP en contexte europeen et multilingue.
- **Faisabilite** : B si un GPU gratuit suffit (Colab ou Kaggle en QLoRA 4 bits sur un 7B, ce
  qui est documente comme faisable), C si la taille de modele necessaire depasse cela.
  **A chiffrer avant de s'engager.**
- **Valeur** : forte, et c'est un actif reutilisable : un modele calibre sur l'Europe est un
  differenciateur commercial en France.
- **Risque** : eleve. Le fine tuning est le seul angle de la liste ou l'echec technique est
  possible pour des raisons de ressources.

### Angle K. Reproduction du resultat Stanford sans entretiens, sur Twin-2K-500. Faisabilite B.
- **Verrou attaque** : la question de la matiere humaine, sous contrainte "aucun humain
  recrute".
- **Etat de l'art depasse** : Park et al. utilisent des entretiens de 2 heures, inaccessibles
  sans recrutement. Twin-2K-500 offre 2058 personnes et environ 2,42 heures de questionnaire
  chacune, **publiquement** [CONFIRME]. La question ouverte est : combien de la performance de
  Park est due au format entretien, et combien a la simple quantite d'information auto
  rapportee ? Park lui meme donne un element : enquete seule 82 pour cent contre entretien seul
  83 pour cent [CONFIRME], ce qui suggere que **le format entretien apporte peu**.
- **Contenu** : construire des agents a partir de Twin-2K-500 et mesurer la performance
  normalisee par le test retest de la vague 4, en repliquant le protocole de normalisation de
  Park. Comparer explicitement au 82 a 86 pour cent de Park.
- **Faisabilite** : moyenne. Les donnees sont publiques, le protocole est documente, le cout est
  le nombre d'appels (2058 agents fois 17 taches).
- **Valeur** : tres forte pour le dossier MIT. C'est la reproduction demandee au point 1 de
  l'ambition scientifique, realisee **sans recruter personne**, ce qui leve la contrainte
  numero 2 de CONTEXTE.md. Et le papier Twin-2K-500 donne deja une reference a battre :
  71,72 pour cent brut, 87,67 pour cent du plafond test retest.
- **Risque** : moyen. Il faut lire attentivement la licence du jeu de donnees et le protocole
  de normalisation.

### Angle M. Le transport de variance : deflater l'inter groupes, gonfler l'intra groupe. Faisabilite A a B.
- **Verrou attaque** : la double distorsion, directement, et en tant que couple.
- **Etat de l'art depasse** : tous les correctifs publies agissent sur la **dispersion globale**.
  VS la gonfle et sur corrige (ratio de 0,4 a 1,3 chez Ozkan). SSR corrige la forme marginale.
  La calibration supervisee corrige la position. **Aucun ne redistribue la variance entre le
  terme inter segments et le terme intra segment** [CONFIRME par absence]. LifeMem s'en
  approche mais par l'entree (trajectoires de vie) et non par la sortie.
- **Contenu** : apres generation, appliquer une transformation affine par segment qui divise
  l'ecart au centre de gravite global par le gap inflation factor estime, et multiplie l'ecart
  au centroide de segment par l'inverse du ratio d'ecarts types intra. Le facteur de correction
  est estime sur un petit echantillon de reference, dans l'esprit des 1 a 10 exemples de
  Kambhatla et al. Version plus ambitieuse : un transport optimal entre la distribution jointe
  simulee et la distribution jointe observee, contraint a preserver les marges par segment.
- **Faisabilite** : A pour la version affine, qui est une correction post hoc en quelques lignes
  de code sur des sorties deja produites. B pour la version transport optimal.
- **Valeur** : **la plus forte de la liste.** C'est un correctif nouveau, motive par une mesure
  nouvelle, applicable a la sortie de n'importe quel modele, et composable avec SSR et avec la
  calibration supervisee. Il repond directement a l'objection "vous n'avez fait que mesurer".
- **Risque** : moyen. Le risque principal est que la correction affine detruise la coherence
  interne des reponses d'un meme agent, c'est a dire qu'elle repare la statistique en cassant
  l'individu. Il faut le tester avec les metriques de coherence inter items de Lukauskas et
  Sarkauskaite. **A ne tenter qu'apres l'angle B, qui fournit les facteurs a appliquer.**

### Angle N. Le regime ou le LLM gagne : imputation a exemples reels contre MICE. Faisabilite A.
- **Verrou attaque** : la menace de baseline, frontalement.
- **Etat de l'art depasse** : Holtdirk et al. montrent qu'avec 100 exemples reels en contexte,
  un modele ouvert (gpt-oss-120b) divise par deux l'erreur de MICE PMM sur OpinionQA
  [CONFIRME, arXiv 2606.09351]. **Mais leurs intervalles sont deux a cinq fois plus etroits
  pour une couverture inferieure (0,92 contre 0,96)**, ce qui est la signature exacte de
  l'exces de confiance decrit par Bisbee et al. Personne n'a verifie si ce gain resiste a une
  analyse de la double distorsion par sous groupe.
- **Contenu** : reproduire Holtdirk et al. sur des modeles plus petits et sur d'autres enquetes,
  puis auditer par sous groupe. Question centrale : le gain moyen cache t il une amplification
  des ecarts inter groupes ? Et combien d'exemples reels faut il pour franchir la baseline
  statistique ? La courbe "nombre d'exemples contre performance relative a MICE" n'est publiee
  nulle part a ma connaissance.
- **Faisabilite** : elevee. Modeles ouverts, donnees publiques, MICE disponible en R et en
  Python.
- **Valeur** : forte, et directement monetisable. Le message commercial devient : "donnez nous
  200 repondants reels, on reconstitue les 10 000 autres mieux que l'imputation statistique
  standard", ce qui est une promesse plus defendable et plus verifiable que "on remplace le
  sondage".
- **Risque** : faible.

### Angle L. Le protocole d'entretien et les jumeaux sur humains recrutes. Faisabilite C.
- **Verrou attaque** : tous, mais avec de la matiere fraiche non contaminee.
- **Pourquoi C** : contrainte dure numero 2 de CONTEXTE.md. Aucun humain recrute. A garder
  pour la phase suivante, declenchee seulement si la matiere humaine devient disponible.
- **Note** : c'est le seul angle qui permettrait de repondre proprement a la contamination, car
  des donnees collectees apres la coupure des modeles sont par construction non contaminees.
  A garder en reserve comme argument de differenciation a moyen terme.

### Classement final, du plus faisable au moins faisable

| Rang | Angle | Faisabilite | Valeur scientifique | Verrou principal |
|---|---|---|---|---|
| 1 | B. Decomposition de la double distorsion | A | tres forte | double distorsion |
| 2 | A. Banc d'essai unifie des correctifs, avec baselines statistiques | A | tres forte | variance |
| 3 | M. Transport de variance inter vers intra | A a B | **la plus forte** | double distorsion |
| 4 | D. Contamination et derive temporelle | A | tres forte | contamination, temps |
| 5 | N. Imputation a exemples reels contre MICE | A | forte, monetisable | menace de baseline |
| 6 | E. Hybride copule plus LLM | A | tres forte | variance, baselines |
| 7 | C. SSR generalise plus calibration | A | forte | variance |
| 8 | F. Modele de mesure latent (IRT) | B | tres forte | double distorsion |
| 9 | K. Reproduction Stanford sur Twin-2K-500 | B | tres forte | reproduction |
| 10 | I. Courbe fidelite contre cout | B | forte | echelle |
| 11 | H. Refus comme censure de la queue | B | forte | refus, sycophancie |
| 12 | G. Cartographie par domaine | B | forte | domaine |
| 13 | J. Fine tuning distributionnel europeen | B a C | forte | variance, WEIRD |
| 14 | L. Entretiens et jumeaux sur humains recrutes | C | tres forte | tous |

**Recommandation de sequencage revisee** [HYPOTHESE, c'est mon jugement] :
1. **B d'abord.** Il est peu risque, il fournit le vocabulaire et les trois metriques separees
   dont tout le reste depend, et il produit les facteurs de correction dont l'angle M a besoin.
2. **A ensuite**, en reutilisant le meme code, et **en y ajoutant systematiquement les quatre
   baselines statistiques de la section 2.7.3.** Sans elles, le banc d'essai est refutable.
3. **M dans la foulee**, parce qu'il transforme la mesure en correctif et que c'est ce qui fait
   la difference entre un papier de diagnostic et un papier de contribution.
4. **D en parallele**, parce qu'il repond a l'objection la plus previsible d'un relecteur et
   qu'il ne partage aucune ressource avec les trois premiers.
5. N, E, C ensuite selon ce que A aura montre. K reste le gros morceau du trimestre, a lancer
   quand le pipeline de mesure est stable.

**Note d'arbitrage** : par rapport a la premiere version de ce document, la decouverte de la
double distorsion fait passer B devant A et fait apparaitre M, qui n'existait pas. Le
raisonnement est simple : on ne peut pas construire un banc d'essai des correctifs tant qu'on
n'a pas la metrique qui distingue un correctif utile d'un correctif qui deplace le probleme.

---

## 6. Ressources gratuites mobilisables, verifiees

Toutes les entrees ci dessous sont accessibles sans depense [CONFIRME sauf indication].

**Jeux de donnees**
- Twin-2K-500, 2058 personnes, plus de 500 questions, 4 vagues dont une de test retest.
  Hugging Face, LLM-Digital-Twin/Twin-2K-500.
- GlobalOpinionQA, 2556 questions, plus de 100 pays. Hugging Face, Anthropic/llm_global_opinions.
- Psych-101, 160 experiences, 60 092 participants, 10 681 650 choix. Hugging Face,
  marcelbinz/Psych-101. Le jeu de test est en depot restreint (CC-BY-ND-4.0).
- OpinionQA, construit sur l'American Trends Panel de Pew. Public via le depot des auteurs
  [PROBABLE, je n'ai pas verifie le lien de telechargement].
- SubPOP, 3362 questions, 70 000 paires. [PROBABLE, le papier annonce une mise a disposition,
  je n'ai pas verifie le depot.]
- General Social Survey, American National Election Studies, World Values Survey, European
  Social Survey, Eurobarometre. Microdonnees publiques, inscription gratuite selon les cas
  [PROBABLE, c'est l'usage etabli de ces archives, je n'ai pas re verifie les conditions
  actuelles].

**Modeles et code**
- Adaptateur Centaur 70B sur Hugging Face, marcelbinz/Llama-3.1-Centaur-70B-adapter.
- Code des Turing Experiments, github.com/microsoft/turing-experiments.
- Code des generative agents de Stanford, github.com/StanfordHCI/genagents, avec acces restreint
  aux agents individuels sous revue.
- Modeles ouverts executables en local en 7B a 8B pour toute la partie mesure.

**Ce qui coute de l'argent et qu'il faut eviter au depart**
- Les modeles proprietaires en volume. Perez et al. ont fait 811 560 prompts ; Lukauskas et
  Sarkauskaite environ 65 000 questionnaires sur 37 modeles. Ce sont des budgets a quatre ou
  cinq chiffres en API. Alternative gratuite : modeles ouverts en local, volume reduit, plan
  d'experience fractionnaire plutot que plan complet.

---

## 7. Bibliographie

Ordre : fondateurs, puis verrou de la variance, puis autres verrous, puis critiques, puis
ressources.

**Fondateurs du champ**
1. Argyle L. P., Busby E. C., Fulda N., Gubler J. R., Rytting C., Wingate D. (2023). Out of
   One, Many: Using Language Models to Simulate Human Samples. Political Analysis 31(3),
   337-351. https://arxiv.org/abs/2209.06899 et
   https://www.cambridge.org/core/journals/political-analysis/article/abs/out-of-one-many-using-language-models-to-simulate-human-samples/035D7C8A55B237942FB6DBAD7CAA4E49
2. Horton J. J. (2023). Large Language Models as Simulated Economic Agents: What Can We Learn
   from Homo Silicus? NBER WP 31122. https://arxiv.org/abs/2301.07543 et
   https://www.nber.org/papers/w31122
3. Aher G. V., Arriaga R. I., Kalai A. T. (2023). Using Large Language Models to Simulate
   Multiple Humans and Replicate Human Subject Studies. ICML 2023, PMLR 202, 337-371.
   https://arxiv.org/abs/2208.10264 et https://proceedings.mlr.press/v202/aher23a.html
4. Park J. S., Zou C. Q., Kamphorst J., Egan N., Shaw A., Hill B. M., Cai C., Morris M. R.,
   Liang P., Willer R., Bernstein M. S. (2024-2026). LLM Agents Grounded in Self-Reports Enable
   General-Purpose Simulation of Individuals (anciennement Generative Agent Simulations of
   1,000 People). https://arxiv.org/abs/2411.10109
5. Santurkar S., Durmus E., Ladhak F., Lee C., Liang P., Hashimoto T. (2023). Whose Opinions Do
   Language Models Reflect? ICML 2023. https://arxiv.org/abs/2303.17548
6. Durmus E. et al. (2023). Towards Measuring the Representation of Subjective Global Opinions
   in Language Models. https://arxiv.org/abs/2306.16388
7. Dillion D., Tandon N., Gu Y., Gray K. (2023). Can AI language models replace human
   participants? Trends in Cognitive Sciences 27(7), 597-600.
   https://www.cell.com/trends/cognitive-sciences/abstract/S1364-6613(23)00098-0
8. Binz M., Akata E., Bethge M., Brandle F., Schulz E. et al. (2025). A foundation model to
   predict and capture human cognition. Nature 644, 1002-1009.
   https://www.nature.com/articles/s41586-025-09215-4 et https://arxiv.org/abs/2410.20268

**Verrou de la variance : mesure**
9. Bisbee J., Clinton J. D., Dorff C., Kenkel B., Larson J. M. (2024). Synthetic Replacements
   for Human Survey Data? The Perils of Large Language Models. Political Analysis 32(4),
   401-416.
   https://www.cambridge.org/core/journals/political-analysis/article/synthetic-replacements-for-human-survey-data-the-perils-of-large-language-models/B92267DC26195C7F36E63EA04A47D2FE
10. Ozkan G. (2026). Distribution-First Population Simulation: Collapse, Calibration, and
    Recall in Non-WEIRD LLM Persona Modeling. https://arxiv.org/html/2607.18310
11. Lukauskas M., Sarkauskaite V. (2026). Plausible but Not Valid: A Psychometric Audit of LLMs
    as Synthetic Survey Respondents. https://arxiv.org/html/2608.14606
12. Ma et al. (2025). Representativeness and Structural Consistency of Silicon Samples.
    https://arxiv.org/abs/2507.02919
13. Williams T., Weeber F., Pado S., Akbik A. (2026). Beyond Marginal Distributions: A
    Framework to Evaluate the Representativeness of Demographic-Aligned LLMs.
    https://arxiv.org/pdf/2601.15755

**Double distorsion et menace de baseline (section 2.6 et 2.7)**
13a. Chen Z., Zhu D., Zheng L. N. (28 juillet 2026). When Synthetic Users Fail: A Cross-Domain
    Benchmark of LLM-Simulated Human Survey Responses. https://arxiv.org/abs/2607.26348
13b. Ling et al. (2026). Mitigating Identity Essentialism in LLM Agents with Longitudinal Life
    Trajectories (LifeMem). https://arxiv.org/html/2608.19621
13c. Morocho, Cima, Fagni, Avvenuti, Cresci (2026). Assessing the Reliability of
    Persona-Conditioned LLMs as Synthetic Survey Respondents. ACM Web Conference 2026.
    https://arxiv.org/html/2602.18462v1
13d. Holtdirk T., Ahnert G., Sakshaug J. W., Haensch A.-C. (2026). In-Context Learning for the
    Imputation of Public Opinion Data with Large Language Models.
    https://arxiv.org/html/2606.09351
13e. Generating the Modal Worker: A Cross-Model Audit of Race and Gender in LLM-Generated
    Personas Across 41 Occupations (2025-2026). https://arxiv.org/html/2510.21011v3

**Verrou de la variance : correctifs**
14. Meister N., Guestrin C., Hashimoto T. (2025). Benchmarking Distributional Alignment of
    Large Language Models. NAACL 2025. https://arxiv.org/abs/2411.05403 et
    https://aclanthology.org/2025.naacl-long.2/
15. Zhang J. et al. (2025-2026). Verbalized Sampling: How to Mitigate Mode Collapse and Unlock
    LLM Diversity. https://arxiv.org/abs/2510.01171
16. Heath O., Alexander R. (2026). Correcting Mode Collapse in Silicon Sampling with Semantic
    Similarity Rating. https://arxiv.org/html/2607.28550
17. Kambhatla et al. (2026). Improving the Distributional Alignment of LLMs using Supervision.
    https://arxiv.org/html/2507.00439v4
18. Suh J., Jahanparast E., Moon S., Kang M., Chang S. (2025). Language Model Fine-Tuning on
    Scaled Survey Data for Predicting Distributions of Public Opinions (SubPOP). ACL 2025.
    https://arxiv.org/abs/2502.16761 et https://aclanthology.org/2025.acl-long.1028/
19. Qin X., Li Z., Cheng X. (2026). Restoring Heterogeneity in LLM-based Social Simulation: An
    Audience Segmentation Approach. https://arxiv.org/html/2604.06663v1
20. Choi et al. (2026). Beyond the Mean: Three-Axis Fidelity for Aligning LLM-Based Survey
    Simulators from Small Pilot Data. https://arxiv.org/html/2606.28963
21. Kim J., Lee B. (2023-2026). AI-Augmented Surveys: Leveraging Large Language Models and
    Surveys for Opinion Prediction. https://arxiv.org/abs/2305.09620
22. Polypersona: Persona-Grounded LLM for Synthetic Survey Responses (2025). IEEE BigData 2025.
    https://arxiv.org/abs/2512.14562

**Autres verrous**
23. Tao Y., Viberg O., Baker R. S., Kizilcec R. F. (2024). Cultural bias and cultural alignment
    of large language models. PNAS Nexus 3(9), pgae346.
    https://academic.oup.com/pnasnexus/article/3/9/pgae346/7756548 et
    https://arxiv.org/abs/2311.14096
24. Salecha A. et al. (2024). Large language models display human-like social desirability
    biases in Big Five personality surveys. PNAS Nexus 3(12), pgae533.
    https://academic.oup.com/pnasnexus/article/3/12/pgae533/7919163 et
    https://arxiv.org/abs/2405.06058
25. Tjuatja L., Chen V., Wu T., Talwalkar A., Neubig G. (2024). Do LLMs Exhibit Human-like
    Response Biases? A Case Study in Survey Design. TACL.
    https://aclanthology.org/2024.tacl-1.56/ et https://arxiv.org/abs/2311.04076
26. Pezeshkpour P., Hruschka E. (2024). Large Language Models Sensitivity to The Order of
    Options in Multiple-Choice Questions. NAACL Findings. https://arxiv.org/abs/2308.11483
27. Perez C. J., Vasquez M. P. Jr, Giabbanelli P., Wu P. Y. (2026). Simulating Social Attitudes
    with LLMs: Accuracy, Demographic Effects, and Refusal Behavior in the Sensitive Domain of
    Suicide Prevention. NLP+CSS 2026. https://aclanthology.org/2026.nlpcss-1.12/
28. Brand J., Israeli A., Ngwe D. Using GPT for Market Research. Harvard Business School
    working paper / SSRN. https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4395751
29. PrivacySim: Evaluating LLM Simulation of User Privacy Behavior (2026).
    https://arxiv.org/html/2605.12147v1
30. Moral stereotyping in large language models. PNAS.
    https://www.pnas.org/doi/10.1073/pnas.2519941123 (inaccessible, HTTP 403 lors de la
    tentative de lecture)

**Critiques de fond**
31. Dominguez-Olmedo R., Hardt M., Mendler-Dunner C. (2024). Questioning the Survey Responses
    of Large Language Models. NeurIPS 2024. https://arxiv.org/abs/2306.07951
32. Cummins J. (2026). The Threat of Analytic Flexibility in Using Large Language Models to
    Simulate Human Data. Advances in Methods and Practices in Psychological Science.
    https://doi.org/10.1177/25152459261461505 et https://arxiv.org/abs/2509.13397
33. Lin Z. (2024-2025). Six Fallacies in Substituting Large Language Models for Human
    Participants. https://arxiv.org/abs/2402.04470
34. Peng T., Gui G., Brucks M., Merlau D. J., Fan G. J., Ben Sliman M., Johnson E. J.,
    Althenayyan A., Bellezza S., Donati D., Fong H., Friedman E., Guevara A., Hussein M.,
    Jerath K., Kogut B., Kumar A., Lane K., Li H., Morwitz V., Netzer O., Perkowski P.,
    Toubia O. (2025-2026). Digital Twins as Funhouse Mirrors: Five Key Distortions.
    https://arxiv.org/abs/2509.19088
35. Bian N., Han X., Lin H., Wu B., Wang J. (2025). Social Simulations with Large Language
    Model Risk Utopian Illusion. https://arxiv.org/abs/2510.21180
36. Anthis J. R., Liu R., Richardson S. M., Kozlowski A. C., Koch B., Evans J., Brynjolfsson E.,
    Bernstein M. (2025). LLM Social Simulations Are a Promising Research Method.
    https://arxiv.org/abs/2504.02234

**Ressources**
37. Toubia O., Netzer O., Peng T. et al. (2025). Twin-2K-500: A dataset for building digital
    twins of over 2,000 people based on their answers to over 500 questions. Marketing Science.
    https://arxiv.org/abs/2505.17479 et
    https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500 et
    https://pubsonline.informs.org/doi/10.1287/mksc.2025.0262
38. Psych-101. https://huggingface.co/datasets/marcelbinz/Psych-101
39. Anthropic/llm_global_opinions. https://huggingface.co/datasets/Anthropic/llm_global_opinions
40. StanfordHCI/genagents. https://github.com/StanfordHCI/genagents et
    https://purl.stanford.edu/jm164ch6237
41. Chen H., Kumar A. (2026). Synonymix: Unified Group Personas for Generative Simulations.
    https://arxiv.org/abs/2603.28066 (reference donnee dans CONTEXTE.md, ne correspond pas au
    papier de Stanford)

---

## 8. Ce que je n'ai pas pu verifier

1. **Le texte integral de Dillion et al. 2023.** Paywall Cell Press. Les quatre reserves
   precises des auteurs ne sont donc pas restituees, seulement le cadrage general repris par la
   litterature ulterieure.
2. **Le texte integral de Bisbee et al. 2024.** Paywall Cambridge. Je n'ai pas le ratio de
   variance exact, seulement l'affirmation qualitative que la dispersion est artificiellement
   faible.
3. **"Moral stereotyping in large language models", PNAS.** La page a renvoye un HTTP 403. Les
   chiffres par pays ne sont pas verifies, seule la direction de l'effet est rapportee et elle
   provient de resumes secondaires.
4. **Le papier de Smallville (Park et al. 2023).** Je ne l'ai pas refetche dans cette session.
   Ce que j'en dis releve de la connaissance etablie du champ, pas d'une verification directe.
5. **Les chiffres de temperature** (22 a 23 categories, F1 0,596 a 0,591). Ils viennent
   d'extraits de recherche renvoyant a arXiv 2602.20408 et a une source non identifiee. Je n'ai
   pas ouvert le papier primaire. **A verifier avant citation dans un dossier.**
6. **Le chiffre "95 pour cent des repondants simules dans une fenetre de 2 points"** rapporte
   par Towards Data Science. Source primaire non identifiee. Ne pas citer en l'etat.
7. **Le detail du papier "Social Simulations with LLM Risk Utopian Illusion"**, arXiv 2510.21180.
   Le PDF n'a pas ete correctement extrait, la restitution que j'en fais est generique.
8. **La disponibilite effective de SubPOP et d'OpinionQA en telechargement.** Annoncees par les
   auteurs, non testees.
9. **Les conditions d'acces actuelles aux microdonnees GSS, ANES, WVS, ESS et Eurobarometre.**
   Ce sont des archives publiques d'usage courant en sciences sociales, mais je n'ai pas
   re verifie les procedures d'inscription en septembre 2026.
10. **Les chiffres commerciaux de validation de "synthetic samples"** (90 pour cent
    d'alignement, deviation 0,07 ecart type contre 0,87 pour GPT). Ce sont des affirmations
    d'editeurs (PyMC Labs, Qualtrics), non revues par les pairs [VENDEUR]. Elles sont
    interessantes comme signal de marche, elles ne valent rien comme preuve scientifique.
11. **Les faisabilites B et C de la section 5** reposent sur mon estimation des ressources GPU
    gratuites disponibles. Aucun chiffrage precis (heures GPU necessaires, VRAM) n'a ete fait.
    C'est le premier travail a mener avant d'engager l'angle J.
12. **L'exhaustivite de mes constats d'absence.** Toutes les affirmations "personne n'a fait X"
    de la section 2.5 sont des constats d'absence apres recherche ciblee sur WebSearch, pas
    apres revue systematique. Avant de revendiquer une nouveaute dans un papier, il faudra une
    recherche systematique sur Semantic Scholar, ACL Anthology et Google Scholar avec des
    chaines de requetes documentees.
13. **Le "precedent Nature en psychiatrie" evoque par Simon.** Je n'ai pas trouve de travail de
    simulation de populations par LLM publie dans Nature en psychiatrie. Le candidat le plus
    probable est Centaur (Nature 2025), qui releve de la psychologie cognitive et non de la
    psychiatrie.
14. **Le detail complet de Chen, Zhu, Zheng (arXiv 2607.26348).** J'ai extrait les tableaux de
    baselines, d'accuracy et de gap inflation via la version HTML. Je n'ai pas verifie
    l'identite exacte des quatre modeles au dela de ce que le papier annonce (Claude Haiku,
    Claude Sonnet, Llama-3.1-8B, Llama-3.3-70B), ni le detail des styles de prompt A et C. Les
    chiffres cites sont ceux renvoyes par la lecture automatique de la page ; **avant citation
    dans un dossier MIT, il faut les revoir sur le PDF original**, tableau par tableau.
15. **Les chiffres de LifeMem (arXiv 2608.19621)**, dont les scores de silhouette 0,19 contre
    -0,02 et la reduction de 30 a 50 pour cent de la divergence KL. Meme reserve : lecture
    automatique de la version HTML, a revoir sur le PDF avant citation.
16. **Les chiffres de Holtdirk et al. (arXiv 2606.09351)**, notamment les erreurs absolues
    0,033 contre 0,068. Meme reserve. Le point de couverture (0,92 contre 0,96) est le plus
    important a re verifier, car c'est lui qui determine si le gain annonce est reel ou s'il
    s'agit d'un exces de confiance.
17. **Les baselines dont le chiffre n'a pas ete extrait** dans le tableau 2.7.1 : gaussienne
    multivariee, retourneur de moyenne de strate, k plus proches voisins, MICE Forest,
    imputation par le mode, plus proches voisins par embeddings. Elles sont attestees comme
    utilisees, leurs performances ne sont pas rapportees ici.

---

## 9. Questions ouvertes pour Simon

1. **La reference de depart est fausse.** https://arxiv.org/html/2603.28066v1 pointe vers
   "Synonymix", pas vers le papier de Stanford. Le bon identifiant est arXiv 2411.10109.
   Confirmes tu que c'est bien ce papier que le porteur avait en tete, ou existe t il un
   troisieme papier que nous n'avons pas identifie ?
2. **Le chiffre a citer.** La v3 du papier de Stanford donne 83 pour cent pour l'entretien seul,
   82 pour cent pour l'enquete seule, 86 pour cent pour la combinaison, 74 pour cent pour la
   base demographique. Le 85 pour cent de CONTEXTE.md vient d'une version anterieure. Quel
   chiffre veut on porter, et sous quelle formulation ?
3. **Le resultat qui devrait nous inquieter.** Park montre que l'enquete seule (82 pour cent)
   fait presque aussi bien que l'entretien de deux heures (83 pour cent). Si c'est robuste,
   alors l'entretien, qui est la partie la plus chere et la plus difficile a repliquer, apporte
   un point de pourcentage. Est ce ta lecture ? Si oui, cela reoriente completement la strategie
   de collecte, et cela rend l'angle K (Twin-2K-500) prioritaire.
4. **Le precedent Nature.** Est ce que le travail en psychiatrie que tu evoquais est bien
   Centaur (Binz et al., Nature 2025), ou un autre papier ? Si c'est un autre, peux tu donner un
   titre ou un auteur ?
5. **L'acces aux auteurs de Stanford.** Le depot genagents annonce un acces restreint aux agents
   individuels, sous revue ethique. Ton contact au MIT peut il faciliter cette demande, et
   sous quel delai ? Cela changerait la faisabilite de l'angle K.
6. **Psychometrie.** L'angle F (tirer un trait latent par theorie de reponse a l'item, puis
   demander au LLM la reponse conditionnelle) est le plus original des angles que j'ai
   identifies, et c'est le plus proche de ta double competence. Est ce qu'il te parait
   defendable methodologiquement ? Quel piege psychometrique vois tu que je ne vois pas ?
7. **Le choix de la premiere dimension.** L'etat de l'art dit que le politique est le domaine ou
   les LLM sont les meilleurs et la consommation celui ou ils sont les pires, alors que la
   consommation est le marche le plus rentable. Preferes tu un premier papier sur le terrain
   facile (politique) ou une contribution sur le terrain difficile (consommation) ?
8. **La ligne rouge sur les chiffres commerciaux.** Le pitch de CONTEXTE.md promet "environ 5
   pour cent de marge d'erreur". Aucune etude publiee ne soutient ce chiffre au niveau
   individuel (r = 0,20 chez Peng et al.), et il n'est defendable qu'au niveau agrege apres
   calibration. Es tu d'accord pour qu'on requalifie explicitement la promesse en "erreur
   agregee sur les marges apres calibration", avant qu'un client ou un relecteur ne le fasse a
   notre place ?
9. **Preenregistrement.** Cummins montre qu'on peut faire varier la correlation de 0,23 a 0,84
   par les seuls choix de pipeline. Veut on preenregistrer nos protocoles sur l'OSF des le
   premier papier ? C'est un cout de rigueur immediat et un argument de credibilite decisif
   aupres du MIT.
10. **Priorite entre mesurer et corriger.** Ma recommandation est de commencer par la mesure
    (angles B puis A), parce que le champ manque de vocabulaire commun et que la mesure est le
    socle de tout correctif. Le porteur voudra probablement aller directement au correctif
    (angles E ou F), qui est plus vendeur. Comment arbitres tu ?
11. **La double distorsion comme these centrale du projet.** La litterature de 2026 documente
    deux erreurs de sens oppose : variance intra segment comprimee d'un facteur 3 a 6, ecarts
    inter segments gonfles d'un facteur 2 a 4. Le projet parlait jusqu'ici d'"ecrasement de la
    variance", ce qui ne couvre que la moitie du phenomene. Es tu d'accord pour que la these du
    projet devienne : **"les populations simulees par LLM ne sont pas trop homogenes, elles
    sont mal structurees, trop homogenes dedans et trop separees dehors"** ? C'est une these
    plus precise, plus originale, et elle debouche sur un correctif specifique, le transport de
    variance de l'angle M.
12. **Le score de silhouette comme metrique signature.** Ling et al. mesurent 0,19 pour les
    agents contre -0,02 pour les humains sur le World Values Survey. Une seule statistique qui
    capture les deux distorsions a la fois. Vois tu une objection psychometrique a en faire
    notre metrique principale, sachant qu'elle depend du choix de la distance et du
    partitionnement en segments ?
13. **La menace de baseline.** Une regression logistique multinomiale sur les seules
    demographies bat les quatre LLM testes au niveau individuel : 0,622 contre 0,589 sur le GSS
    et 0,393 contre 0,277 sur le WVS. Le regime "simuler un individu a partir de ses
    demographies" est donc perdu d'avance. Je propose de deplacer le projet vers le regime ou le
    LLM gagne, l'imputation conditionnee sur des repondants reels en contexte, ou il divise par
    deux l'erreur de MICE PMM. Cela change le pitch : de "on remplace le sondage" a "donnez nous
    200 repondants reels, on reconstitue les 10 000 autres". Ce repositionnement te parait il
    tenable vis a vis du porteur ?
