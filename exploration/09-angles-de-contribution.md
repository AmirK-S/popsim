# 09 - Angles de contribution : attaquer l'ecrasement de variance

Agent 9, exploration popsim. Date : 2 septembre 2026.
Role : generation d'idees et attaque du probleme scientifique central. Les autres agents documentent
l'existant, ce document cherche ce qui n'a pas ete fait et ce qui est testable demain a budget zero.

Regles de lecture : chaque affirmation non triviale porte [CONFIRME] avec URL, [PROBABLE] avec le
raisonnement, ou [HYPOTHESE] pour ce qui n'est pas verifie. Aucune reference n'est inventee.

---

## 0. Resume executif

Le champ a change entre fin 2025 et l'ete 2026. L'ecrasement de variance n'est plus un angle mort,
c'est devenu un sujet actif avec au moins cinq papiers 2026 dedies. La consequence est directe :
**"les LLM ecrasent la variance" n'est plus une contribution, c'est desormais l'etat de l'art.**
Le creneau s'est deplace. Il reste large, mais il faut viser plus precisement.

Surtout, le probleme n'est pas celui que le CONTEXTE decrit. Ce n'est pas un ecrasement, c'est une
**double distorsion de sens contraire**, et c'est l'axe structurant de tout ce document.

- Les ecarts **entre** segments demographiques sont **exageres** d'un facteur deux a quatre
  [CONFIRME par l'orchestrateur sur arXiv 2607.26348, "When Synthetic Users Fail", juillet 2026].
  Le modele caricature les differences de groupe.
- La dispersion **a l'interieur** d'un segment est **ecrasee**. Les membres d'un meme segment se
  ressemblent trop [CONFIRME, converge avec https://arxiv.org/html/2604.06663v1 et
  https://arxiv.org/html/2608.14606].

Ces deux erreurs vont en sens contraire et **se compensent dans toute mesure de variance globale**.
Un simulateur peut donc afficher un ecart-type de population correct tout en etant faux sur les deux
composantes. Toutes les metriques agregees en usage aujourd'hui, ratio SD, TVD marginale, distance
de Wasserstein sur la marge, sont aveugles a cette compensation. C'est la faille centrale du champ
et c'est la contribution la plus accessible du projet.

Quatre creneaux restent ouverts et je les documente dans ce fichier.

1. **Aucune metrique du champ ne separe les trois composantes.** Le champ mesure un "SD ratio"
   global et appelle cela la variance. Personne, dans ce que j'ai lu, ne publie separement la
   variance entre groupes, la variance entre individus d'un meme groupe, et l'instabilite d'un meme
   individu entre deux vagues. Ces trois quantites se compensent deux a deux dans les metriques
   agregees. Une methode peut donc obtenir un bon score en caricaturant les groupes, ou en
   fabriquant des individus incoherents, plutot qu'en produisant une population diverse. C'est un
   defaut de mesure exploitable, et la fiche F3e le transforme en figure.
2. **La sur-correction n'est pas traitee.** Verbalized Sampling corrige la sous-dispersion mais
   passe en sur-dispersion, SD ratio de 0,4-0,56 vers 1,26-1,37 [CONFIRME]
   (https://arxiv.org/html/2607.18310). Personne n'a propose l'operateur de recalage qui ramene a 1.
3. **La baseline statistique humilie les LLM et presque personne ne le dit.** Une copule gaussienne,
   sans aucun modele de langage, atteint un score psychometrique de 0,688 contre 0,714 pour le
   meilleur LLM teste sur 37 [CONFIRME] (https://arxiv.org/html/2608.14606). Au niveau individuel,
   aucun LLM n'egale les modeles de base sur le GSS et le WVS [CONFIRME par l'orchestrateur,
   arXiv 2607.26348]. **C'est une menace existentielle pour le projet, pas un detail.** La section 3
   y est entierement consacree.
4. **La correction de la distorsion inter-groupes n'est traitee par personne.** Tout le champ
   cherche a **augmenter** la variance. Si les ecarts entre groupes sont deja exageres d'un facteur
   deux a quatre, il faut au contraire les **retrecir**. Aucune methode publiee que j'aie vue ne
   fait les deux mouvements a la fois. Voir la fiche C5p.

Les trois chantiers que je lancerais cette semaine sont E1u couplee a F3e, le test des regimes 1 et
3 de la section 3, et C5p. Tous les trois consomment moins de 100 000 appels de modele au total,
soit un quart du budget hebdomadaire local, et deux d'entre eux n'en consomment aucun.

---

## 1. Comprendre la cause, pas le symptome

### 1.1 La distinction centrale : une decomposition a TROIS niveaux, pas deux

C'est le coeur du sujet et le champ le traite mal. Posons la decomposition, qui est celle des
modeles a effets mixtes hierarchiques classiques en psychometrie. Elle a **trois** etages, et non
deux, et c'est precisement le troisieme etage qui manque a la formulation initiale du projet.

Pour une question a reponse numerique ou ordinale, la reponse observee de la personne i, membre du
segment g, a la vague t s'ecrit :

    y_igt = mu + b_g + a_ig + e_igt

- `b_g` est l'effet du segment, l'ecart de la moyenne du groupe a la moyenne generale. Sa variance,
  **`Var_between`**, est l'amplitude des differences entre hommes et femmes, entre diplomes et non
  diplomes, entre tranches de revenu.
- `a_ig` est la deviation propre a l'individu **a l'interieur de son segment**. Sa variance,
  **`Var_within`**, est ce qui fait que deux ouvriers de 47 ans ne pensent pas la meme chose. C'est
  la que vivent les minorites d'opinion, celles qui ne coincident avec aucune categorie.
- `e_igt` est l'instabilite de reponse de la meme personne d'une vague a l'autre. Sa variance,
  **`Var_intra`**, n'est pas du bruit de mesure a eliminer, c'est une propriete reelle de l'opinion
  humaine. Une personne interrogee deux fois ne repond pas identiquement.

La variance inter individuelle dont parle le CONTEXTE est la somme des deux premieres :
`Var_inter = Var_between + Var_within`.

### 1.1.1 La double distorsion et son effet de compensation

Voici le fait central, et il renverse la formulation du probleme.

| Composante | Comportement du LLM | Ordre de grandeur | Source |
|---|---|---|---|
| `Var_between` | **Exageree** | facteur 2 a 4 | [CONFIRME par l'orchestrateur, arXiv 2607.26348, "When Synthetic Users Fail", GSS et WVS] |
| `Var_within` | **Ecrasee** | ratio SD de 0,4 a 0,56, compression de 14 a 62 pour cent selon le modele | [CONFIRME] (https://arxiv.org/html/2607.18310, https://arxiv.org/html/2608.14606) |
| `Var_intra` | **Mal calibree dans les deux sens** | trop basse a temperature basse et persona riche, sur-coherence psychometrique ; trop haute des qu'on monte la temperature | [CONFIRME] (https://arxiv.org/html/2608.14606) |

**Les deux premieres erreurs sont de sens contraire et se compensent.** Un simulateur qui multiplie
par trois les ecarts entre groupes et divise par trois la dispersion intra-groupe peut afficher une
`Var_inter` totale parfaitement correcte. Toutes les metriques en usage aujourd'hui, ratio
d'ecart-type, distance de variation totale sur la marge, distance de Wasserstein, sont calculees sur
la distribution marginale de la population entiere et **ne voient pas la difference**.

Consequences, et elles sont severes.

1. [HYPOTHESE, forte] Une partie des methodes publiees comme "restaurant la fidelite
   distributionnelle" ameliorent une metrique globale sans corriger, voire en aggravant, la
   structure sous-jacente. Personne ne peut le savoir, faute d'avoir publie la decomposition.
2. La direction de correction n'est **pas la meme** selon la composante. Augmenter la temperature,
   enrichir le persona, forcer la diversite : tous ces gestes augmentent la variance **partout**.
   Or il faut **augmenter** `Var_within` et **diminuer** `Var_between`. Un bouton unique ne peut pas
   faire les deux. C'est pour cela qu'aucune methode a bouton unique ne peut resoudre le probleme,
   et c'est un argument theorique, pas empirique.
3. Le produit vendable est detruit par les deux erreurs simultanement, et de facon particulierement
   perverse. L'exageration de `Var_between` fabrique des segments artificiellement nets, donc
   **visuellement convaincants** dans un rapport d'etude, et l'ecrasement de `Var_within` fait
   disparaitre les individus atypiques. Le client recoit un graphique plus propre que la realite. Il
   n'a aucun moyen de s'en apercevoir, et c'est exactement pour cela qu'il faut le lui dire.

### 1.1.2 Le second piege : confondre variance de population et instabilite individuelle

Fait d'ancrage : sur le General Social Survey, les humains reels reproduisent leur propre reponse
anterieure environ 79,5 pour cent du temps lors d'un retest a deux semaines [CONFIRME, chiffre
79,53 pour cent rapporte comme plafond individuel empirique, voir https://arxiv.org/html/2608.14606
et repris comme denominateur du score normalise de Park et al.]. Autrement dit, `Var_intra` humaine
est loin d'etre negligeable, et environ 20 points de "desaccord" ne sont pas de l'erreur de modele,
ce sont de l'instabilite humaine.

**Le second piege que le champ n'a pas ferme.** Les memes metriques agregees melangent aussi
`Var_within` et `Var_intra`. Le meme ecart-type total peut etre obtenu par :

- une population reellement diverse d'individus stables, ce qui est le comportement humain,
- une population homogene d'individus instables, ce qui est ce qu'on obtient en montant la
  temperature de decodage.

Ces deux configurations sont statistiquement indiscernables sur une seule vague et radicalement
differentes en valeur d'usage. Un institut qui achete une segmentation a besoin de la premiere.
La seconde produit des segments qui se dissolvent des qu'on repose la question.

[HYPOTHESE, forte] **Une part significative des gains de "restauration de variance" publies en 2026
sont des gains de `Var_intra` et non de `Var_within`.** Aucun des papiers que j'ai lus ne fournit la
decomposition permettant de trancher. C'est verifiable a cout nul, voir la fiche E1u.

Troisieme piege, symetrique. Le ratio ICC = `Var_within / (Var_within + Var_intra)` ne suffit pas
non plus, parce qu'un modele qui compresse les deux composantes dans la meme proportion obtient le
bon ICC en etant faux sur les deux. **Regle a graver : publier les trois composantes en valeur
absolue, jamais un rapport, jamais une somme.** Tout resume en un chiffre reintroduit la
compensation qu'on cherche a exposer.

Troisieme observation, contre-intuitive et bien documentee : les LLM ne sont pas seulement trop
homogenes entre individus, ils sont aussi **trop coherents a l'interieur d'un individu**. L'audit
psychometrique de 2026 parle de dissociation coherence / fidelite : le alpha de Cronbach et le omega
sont gonfles chez les repondants synthetiques par rapport aux humains [CONFIRME]
(https://arxiv.org/html/2608.14606). Le modele fabrique une personne trop bien construite, sans les
incoherences d'attitude que tout le monde a. Donc `Var_intra` est parfois trop basse, pas trop
haute, contrairement a ce que l'intuition "le LLM est bruite" suggere. Les deux regimes coexistent
selon la methode d'echantillonnage : trop basse quand le persona est riche et la temperature basse,
trop haute quand on force la diversite par la temperature.

### 1.2 Revue des causes candidates et poids estime

Je liste les causes, la preuve dont je dispose, et mon estimation de poids. Les poids sont des
jugements, pas des mesures, et sont etiquetes comme tels.

**C1. Biais de typicalite dans les donnees de preference humaine (RLHF).**
Les annotateurs humains preferent systematiquement le texte familier, ce qui pousse l'optimisation
de preference a concentrer la masse de probabilite sur les reponses modales. Cette cause est
formalisee theoriquement et verifiee empiriquement sur des jeux de donnees de preference
[CONFIRME] (https://arxiv.org/abs/2510.01171).
Poids estime : **eleve**. [PROBABLE] C'est la cause qui explique le mieux pourquoi le probleme
s'aggrave sur les modeles les plus alignes et pourquoi une simple astuce de prompt, verbaliser la
distribution, recupere une grande partie de la diversite perdue : si l'information distributionnelle
etait detruite, aucun prompt ne la ferait revenir.

**C2. Objectif de vraisemblance maximale et decodage.**
La perte par maximum de vraisemblance favorise les reponses centrales [CONFIRME comme diagnostic
pose par les auteurs] (https://arxiv.org/html/2604.06663v1). S'y ajoute le decodage lui-meme,
temperature basse, top-p, qui coupe les queues.
Poids estime : **moyen**. [PROBABLE] C'est une cause reelle mais largement contournable sans
reentrainement, puisque l'information reste dans les logits. Le fait que lire directement les
log-probabilites donne des resultats differents de l'echantillonnage de texte le montre
[CONFIRME] (https://aclanthology.org/2025.naacl-long.2/).

**C3. Effondrement de la diversite dans les representations internes.**
Dans les couches hautes du transformeur, les representations d'identites sociales differentes
convergent et deviennent de moins en moins distinguables. Les approches par prompt echouent parce
que l'impact semantique du persona s'attenue au fil des couches [CONFIRME]
(https://arxiv.org/html/2603.16142v1).
Poids estime : **eleve**. C'est la cause la plus profonde parce qu'elle explique pourquoi enrichir
le prompt a un rendement decroissant. La preuve indirecte est forte : injecter des vecteurs
directement dans les etats caches fait chuter la divergence KL de 65 pour cent et l'ecart d'entropie
de 96 pour cent par rapport a la baseline prompt [CONFIRME, meme source].

**C4. Le modele raisonne sur un stereotype de groupe, pas sur un individu.**
L'inference de persona demographique s'appuie sur des raccourcis au niveau population, ce qui produit
des predictions peu diverses [CONFIRME comme diagnostic] (https://arxiv.org/html/2603.27056v1).
Bisbee et al. observent une variance anormalement basse et des coefficients de regression
desalignes quand on regresse les variables du prompt sur la reponse [CONFIRME]
(https://www.cambridge.org/core/journals/political-analysis/article/synthetic-replacements-for-human-survey-data-the-perils-of-large-language-models/B92267DC26195C7F36E63EA04A47D2FE).
Poids estime : **eleve**. C'est la cause la plus lisible pour un lecteur non technique et celle qui
detruit le plus directement la valeur commerciale, puisque la caricature de groupe est exactement
ce qu'un institut n'achete pas.

**C5. Perte d'information a la compression d'une personne en persona textuel.**
Intuitivement, ecrire une personne en 200 mots detruit ce qui la rend unique. Mais la donnee 2026
nuance : enrichir de 8 a 15 identifiants ameliore nettement, KL de 2,72 vers 0,68, et pousser a 59
identifiants **degrade**, KL remonte a 1,04 [CONFIRME] (https://arxiv.org/html/2604.06663v1).
Poids estime : **moyen, et non monotone**. [PROBABLE] Ce n'est donc pas un probleme de volume
d'information mais de saillance. Au-dela d'un seuil, le modele moyenne sur les attributs au lieu
de les integrer. Cela invalide l'intuition naive "plus le persona est riche, mieux c'est" et ouvre
une piste : selectionner les attributs plutot que les accumuler.

**C6. Sous-representation de certains profils dans les donnees d'entrainement.**
Les modeles refletent mieux certains groupes demographiques que d'autres, et le pilotage par prompt
ne corrige pas ce desalignement [PROBABLE, litterature OpinionQA de Santurkar et al. 2023, que je
n'ai pas re-verifiee dans cette session]. Confirme indirectement par les limites annoncees de PSII :
dependance a la couverture demographique, populations rares insuffisamment modelisees [CONFIRME]
(https://arxiv.org/html/2603.16142v1).
Poids estime : **moyen pour la moyenne, faible pour la variance**. [HYPOTHESE] La sous-representation
deplace le centre du groupe plus qu'elle ne comprime sa dispersion. Elle explique le biais, pas
l'ecrasement. C'est important a dire parce que le champ confond souvent les deux.

**C7. Le tirage repete n'explore pas la vraie incertitude d'une personne.**
Tirer N fois la meme requete echantillonne le bruit du decodeur, pas l'instabilite de l'individu
simule. Les deux distributions n'ont aucune raison de coincider. Une decomposition en composantes
de variance sur les reponses LLM montre que les sources de non-determinisme se repartissent tres
inegalement, le pur effet de repetition ne pesant qu'environ 1 pour cent contre environ 75 pour cent
de variance structuree par les interactions item-systeme [CONFIRME, sur un domaine different, les
reponses de marque] (https://arxiv.org/abs/2607.13304).
Poids estime : **eleve sur la validite, faible sur l'amplitude**. C'est moins une cause de
l'ecrasement qu'une cause de **mauvaise mesure** de l'ecrasement, et c'est pour cela que je le
place au centre de la contribution proposee.

**C8. Sur-coherence psychometrique induite.**
Le modele construit un individu plus consistant qu'un humain, alpha et omega gonfles, encodage
stereotype des demographies [CONFIRME] (https://arxiv.org/html/2608.14606).
Poids estime : **moyen**. C'est le miroir de C4 au niveau intra-individuel.

### 1.3 Ce que cette analyse implique pour la strategie

[PROBABLE] Si C1 et C3 dominent, alors les methodes sans reentrainement, verbalisation de
distribution et lecture de logits, plafonnent, et l'intervention sur les activations est la seule
voie a fort gain. Mais l'intervention sur activations exige des poids ouverts et un GPU, ce qui
tend le budget zero. Le compromis realiste est donc : mesurer d'abord proprement, avec des methodes
sans entrainement, puis ne payer du calcul que la ou la mesure prouve qu'il y a du gain.

C'est aussi la sequence la plus credible face a un chercheur du MIT, qui se mefie d'une methode
proposee avant que le probleme ait ete correctement mesure.

### 1.4 Trois criteres transversaux qui s'appliquent a TOUTES les fiches

Ces trois regles priment sur les criteres particuliers de chaque fiche. Une piste qui ne les
satisfait pas n'est pas evaluee, quel que soit son score.

**Critere T1 : la decomposition exacte par les logits, pas l'echantillonnage.**
En lisant les probabilites des tokens de reponse plutot qu'en generant du texte, on obtient la
distribution complete de la reponse d'un persona a une question fermee. Cela donne la decomposition
**exacte**

    Var_totale = E_personas[ Var_intra(persona) ] + Var_entre_personas[ E[reponse | persona] ]

sans aucun bruit d'echantillonnage, en une passe avant par persona et par question, pour un cout de
l'ordre de mille fois inferieur au tirage repete [CONFIRME par l'agent infrastructure]. C'est la
mesure meme du phenomene etudie, disponible gratuitement et en local. **Toute fiche de ce document
doit etre evaluee ainsi, et non par echantillonnage.** Consequence pratique : une experience qui
demandait des heures se fait en minutes, ce qui change le regime de travail du projet entier.

Corollaire diagnostique, et il est important : la decomposition separe proprement deux pathologies
que l'echantillonnage confond. Un persona **trop sur de lui**, `Var_intra` trop faible, et une
population **trop homogene**, `Var_entre` trop faible. Ce ne sont pas les memes remedes. Le premier
appelle une injection de bruit de reponse calibree, fiche E2u. Le second appelle une modification du
conditionnement, familles B, C et D. Un praticien qui monte la temperature traite le second probleme
avec le remede du premier.

**Critere T2 : le test de la variance utile.**
Augmenter la variance est trivial. Un generateur aleatoire y parvient. La seule question qui compte
est de savoir si le gain de variance **entre individus** est **correle aux vraies differences entre
les personnes reelles**, ou reparti au hasard. Protocole, identique pour toutes les fiches : pour
chaque paire de personnes reelles (i, j), calculer la distance entre leurs vraies reponses, et la
distance entre leurs reponses simulees. Calculer la correlation de Spearman entre les deux vecteurs
de distances, avant et apres l'intervention testee.

- Si la variance augmente et la correlation **monte**, l'intervention capture de la vraie
  heterogeneite. C'est une contribution.
- Si la variance augmente et la correlation **stagne ou baisse**, l'intervention ajoute du bruit
  indifferencie. C'est une astuce de temperature deguisee, et il faut le dire.

**Ce test separe une vraie contribution d'une astuce, et je le fais figurer dans le critere de
reussite de chaque fiche.** [HYPOTHESE] Je n'ai vu aucun papier 2026 le rapporter, alors qu'il est
gratuit une fois les logits lus. C'est peut-etre la contribution la plus simple et la plus utile du
document.

**Critere T3 : la baseline a battre.**
Chaque fiche porte une ligne "baseline a battre" nommant la methode **sans modele de langage** qui
doit etre surpassee. Une piste sans baseline identifiee n'est pas testable, et une piste qui ne bat
pas sa baseline n'a pas de valeur, quel que soit son elegance. La section 3 traite cette question
au niveau du projet entier, ou elle est existentielle.

### 1.5 Le budget de calcul reel

Materiel disponible : Apple M5 de base, 32 Gio de memoire unifiee, permettant de l'ordre de
**400 000 appels de modele par semaine en local et gratuitement** [CONFIRME par l'agent
infrastructure]. C'est l'unite de compte de ce document. En lecture de logits, un appel egale une
passe avant sur un couple persona-question.

Ordre de grandeur pour se reperer : 500 personas fois 200 questions egale 100 000 appels, soit un
quart du budget hebdomadaire. **Presque toutes les fiches sans entrainement de ce document tiennent
dans une seule semaine de ce budget, et je le signale explicitement fiche par fiche.** La ressource
rare de ce projet n'est donc pas le calcul d'inference, c'est le GPU d'entrainement, qui depend de
quotas gratuits externes et non verifies.

---

## 2. Les attaques : 26 fiches

Format homogene. Le "cout" suppose la contrainte dure : zero euro, aucun humain recrute, donnees
publiques uniquement.

Ressources supposees disponibles a cout nul et utilisees dans les protocoles ci-dessous :
- **Twin-2K-500**, 2 058 participants americains, plus de 500 questions, quatre vagues, la vague 4
  repetant des taches des vagues precedentes pour etablir une baseline de test-retest [CONFIRME]
  (https://arxiv.org/html/2505.17479, page HuggingFace https://huggingface.co/papers/2505.17479).
  C'est la ressource la plus precieuse du projet : elle contient a la fois de la variance inter et
  de la variance intra au niveau individuel, sur des personnes reelles, gratuitement.
- **General Social Survey**, gratuit, avec panels a trois vagues [PROBABLE, les panels GSS
  2006-2010, 2008-2012 et 2016-2020 existent, je n'ai pas re-verifie les millesimes exacts].
- **World Values Survey vague 7**, gratuit apres inscription, utilise par PSII avec 97 220
  repondants et 259 questions d'opinion [CONFIRME] (https://arxiv.org/html/2603.16142v1).
- **European Social Survey**, gratuit.
- Modeles a poids ouverts executes localement, famille Llama, Qwen, Mistral, en quantifie, ce qui
  donne acces aux logits. [PROBABLE] Un Mac recent fait tourner un modele 7 a 8 milliards de
  parametres quantifie a vitesse utilisable.
- Calcul GPU gratuit pour les fiches d'entrainement : Google Colab niveau gratuit et Kaggle
  Notebooks, ce dernier offrant un quota hebdomadaire de GPU [PROBABLE, quota de l'ordre de 30
  heures par semaine, a re-verifier avant de planifier dessus].

---

### FAMILLE A - Agir sur le decodage et l'extraction de distribution

---

**A1. Lecture directe de la distribution sur les logits des options de reponse**

- **Mecanisme.** Ne pas generer de texte. Presenter la question a choix multiple, lire en une seule
  passe avant les logits des tokens " A", " B", " C", " D", " E" ou " 1" a " 7", renormaliser sur
  ces seuls tokens. On obtient la distribution de reponse complete de l'agent, pas un tirage.
- **Cause adressee.** C2, decodage. Accessoirement C7, puisque cela supprime le besoin de tirer N
  fois et donc la confusion entre bruit de decodeur et incertitude de l'agent.
- **Precedent.** Existe et est deja critique. Les log-probabilites sont mal calibrees et
  sous-estiment systematiquement la performance des modeles, mais le probleme est attenue par un
  recalage en temperature [CONFIRME] (https://aclanthology.org/2025.naacl-long.2/). Ce n'est donc
  pas une idee nouvelle, c'est une brique d'infrastructure obligatoire.
- **Experience la moins chere.** Modele 8B quantifie en local. 200 questions d'opinion de Twin-2K-500
  a format ferme, 300 personas construits depuis les vagues 1 a 3. Deux conditions : (a) generation
  de texte, 20 tirages par persona, temperature 1,0 ; (b) une passe avant par persona, lecture des
  logits. Comparer les deux distributions agregees a la distribution humaine reelle.
- **Metrique.** Distance de variation totale entre distribution simulee et distribution humaine, par
  question, puis mediane sur les questions. Et cout en passes avant.
- **Critere de reussite.** La condition (b) atteint une TVD mediane au moins aussi bonne que (a)
  pour un cout divise par au moins 15. Si (b) est nettement pire meme apres recalage en temperature,
  c'est un resultat negatif publiable en soi.
- **Cout.** Zero euro. Environ une journee d'ingenierie. Environ 300 passes avant contre 6 000.
- **Baseline a battre.** Le meme modele en generation de texte, 20 tirages. Et, comme temoin sans
  modele de langage, la distribution marginale de l'enquete de l'annee precedente sur la meme
  question, qui est disponible gratuitement et souvent tres difficile a battre.
- **Budget.** Environ 60 000 appels, soit 15 pour cent d'une semaine de budget local. **Testable
  cette semaine.**
- **Verdict.** **Faisable immediatement.** C'est la brique sur laquelle tout le reste s'appuie, a
  faire en premier meme si elle n'est pas originale.

---

**A2. Recalage en temperature de la tete de reponse**

- **Mecanisme.** Apres A1, apprendre un unique scalaire T qui divise les logits des options avant
  renormalisation, ajuste sur un sous-ensemble de questions de developpement pour minimiser la
  divergence a la distribution humaine, puis evalue sur des questions tenues a l'ecart. Un seul
  parametre libre pour tout le systeme.
- **Cause adressee.** C2. Ne touche pas C3 ni C4, et c'est important a dire : le recalage corrige
  la dispersion globale sans corriger la structure inter-groupes.
- **Precedent.** Le recalage en temperature est standard en calibration de classifieurs, et son
  effet sur ce probleme precis est signale [CONFIRME] (https://aclanthology.org/2025.naacl-long.2/).
  L'application systematique comme etape obligatoire d'un pipeline de simulation de sondage n'est
  pas etablie comme standard a ma connaissance [HYPOTHESE].
- **Experience la moins chere.** Reutiliser les logits deja calcules en A1, aucune passe avant
  supplementaire. Ajuster T sur 100 questions, evaluer sur 100 autres. Ajouter une variante ou T est
  ajuste par segment demographique plutot que globalement.
- **Metrique.** TVD mediane et ratio d'ecart-type SD_simule / SD_humain avant et apres recalage.
- **Critere de reussite.** Ratio SD passe de l'ordre de 0,5 a l'intervalle 0,85-1,15 sur les
  questions tenues a l'ecart, sans degrader la TVD sur la moyenne de plus de 2 points.
- **Cout.** Zero euro, quelques heures, aucune inference nouvelle.
- **Baseline a battre.** A1 sans recalage, et la copule gaussienne ajustee sur les memes donnees.
- **Budget.** Zero appel supplementaire, les logits de A1 sont reutilises. **Testable cette
  semaine.**
- **Verdict.** **Faisable immediatement.** Rendement tres eleve par rapport a l'effort.

---

**A3. Correcteur de sur-dispersion pour Verbalized Sampling**

- **Mecanisme.** Verbalized Sampling demande au modele de verbaliser sa distribution de probabilite
  sur les reponses en un seul appel. Le probleme documente est qu'il **sur-corrige** : le ratio
  d'ecart-type passe de 0,4-0,56 a 1,26-1,37 [CONFIRME] (https://arxiv.org/html/2607.18310).
  Proposer un operateur de retrecissement, par exemple elever les probabilites verbalisees a la
  puissance beta puis renormaliser, avec un unique beta ajuste sur un jeu de developpement.
- **Cause adressee.** C1 et C2. Corrige un defaut connu et non traite de la meilleure methode sans
  entrainement du champ.
- **Precedent.** La methode source existe [CONFIRME] (https://arxiv.org/abs/2510.01171), son
  application au sondage aussi [CONFIRME] (https://arxiv.org/html/2607.18310), et la sur-dispersion
  est explicitement laissee ouverte par les auteurs. **Je n'ai trouve aucun travail proposant le
  correcteur.** C'est la lacune la plus nette et la moins chere a combler du champ.
- **Experience la moins chere.** Reproduire VS sur 200 questions du WVS avec un modele local,
  mesurer le ratio SD, ajuster beta sur 100 questions, evaluer sur 100 autres. Comparer trois
  conditions : agents independants, VS brut, VS retreci.
- **Metrique.** Ratio SD, TVD, et surtout la mesure conjointe : le retrecissement doit ramener le
  SD vers 1 **sans** deteriorer la TVD.
- **Critere de reussite.** Ratio SD dans 0,9-1,1 et TVD strictement meilleure que les deux
  conditions de reference. Un ecart de 5 points de TVD suffit a en faire un resultat.
- **Cout.** Zero euro. Deux a trois jours. C'est une contribution de taille "atelier de conference"
  atteignable seul.
- **Baseline a battre.** VS brut, agents independants, et rééchantillonnage bootstrap de l'enquete
  precedente, qui reproduit la dispersion humaine par construction et sert de plancher exigeant.
- **Budget.** Environ 4 000 appels pour VS, negligeable. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement, et c'est le trou le plus visible.**

---

**A4. Decouplage des deux temperatures**

- **Mecanisme.** Utiliser deux sources de stochasticite distinctes. Une temperature de decodage
  basse, voire un decodage deterministe, pour garantir la coherence intra-individu. Et une
  dispersion injectee au niveau du persona, par exemple un vecteur de traits latents tire par
  individu, pour produire la variance inter. Aujourd'hui le champ n'a qu'un bouton et il agit sur la
  mauvaise composante.
- **Cause adressee.** C7 directement, C8 indirectement.
- **Precedent.** [HYPOTHESE] Je n'ai trouve aucun travail formulant explicitement le decouplage des
  deux sources de variance comme principe de conception. PSII injecte du bruit gaussien controle
  dans les etats caches, ce qui en est une version parametrique [CONFIRME]
  (https://arxiv.org/html/2603.16142v1), mais sans opposer les deux composantes.
- **Experience la moins chere.** Grille 3 par 3 : temperature de decodage dans {0,2 ; 0,7 ; 1,2} par
  dispersion de persona dans {nulle, moyenne, forte}, ou la dispersion de persona est obtenue en
  tirant aleatoirement des traits non demographiques. Sur 100 questions, 200 personas, 3 repetitions
  par persona pour pouvoir estimer la variance intra.
- **Metrique.** Estimation separee de `Var_inter` et `Var_intra` par modele a effets mixtes, chacune
  comparee a sa cible humaine issue du test-retest de Twin-2K-500.
- **Critere de reussite.** Montrer une carte ou la temperature de decodage bouge `Var_intra` sans
  bouger `Var_inter`, correlation inferieure a 0,2, et ou la dispersion de persona fait l'inverse.
  Cette carte, a elle seule, est une figure de papier.
- **Cout.** Zero euro. Environ 180 000 passes avant en lecture de logits, soit quelques heures sur
  un modele 8B local. Cinq jours au total.
- **Baseline a battre.** La meilleure temperature unique trouvee par balayage, c'est-a-dire le
  meilleur point de la grille a un seul bouton. Si le decouplage ne bat pas le meilleur reglage a un
  bouton, il n'apporte rien.
- **Budget.** Environ 180 000 appels en lecture de logits, soit 45 pour cent d'une semaine.
  **Testable cette semaine.**
- **Verdict.** **Faisable immediatement. Fort potentiel de figure marquante.**

---

### FAMILLE B - Agir sur le persona

---

**B1. Enrichissement idiosyncratique non demographique**

- **Mecanisme.** Ajouter au persona des details qui n'ont aucune valeur predictive demographique :
  une habitude, un objet possede, un souvenir, une phrase fetiche. L'hypothese est que ces details
  cassent le rappel du stereotype de groupe en forcant le modele a traiter un individu singulier.
- **Cause adressee.** C4 principalement, C5 secondairement.
- **Precedent.** L'ancrage sur des attributs non demographiques est identifie comme benefique
  [CONFIRME comme direction, via SPIRIT] (https://arxiv.org/html/2603.27056v1). Mais la courbe de
  rendement est non monotone : 15 identifiants battent 8 et 59 identifiants sont pires que 15
  [CONFIRME] (https://arxiv.org/html/2604.06663v1). L'effet specifique de details **non predictifs**
  n'est pas isole a ma connaissance [HYPOTHESE].
- **Experience la moins chere.** Trois conditions a demographie identique : (a) demographie seule ;
  (b) demographie plus 5 details idiosyncratiques generes aleatoirement et sans lien avec la
  demographie ; (c) demographie plus 5 details supplementaires correles a la demographie, comme
  temoin. 400 personas, 150 questions, lecture de logits.
- **Metrique.** `Var_inter` estimee, et distance de Wasserstein aux quantiles humains extremes,
  10e et 90e centiles, qui est la ou les instituts regardent.
- **Critere de reussite.** La condition (b) augmente `Var_inter` d'au moins 25 pour cent par rapport
  a (a) sans deplacer la moyenne de plus de 0,1 ecart-type. Si (b) et (c) sont identiques, le
  resultat negatif est interessant : ce n'est pas l'idiosyncrasie qui compte mais le volume.
- **Cout.** Zero euro, deux jours.
- **Baseline a battre.** Une regression logistique multinomiale entrainee sur les memes attributs
  demographiques, qui donne la `Var_between` correcte par construction et une `Var_within` nulle.
  L'enjeu est donc precisement de battre son zero sur `Var_within` sans casser sa `Var_between`.
- **Budget.** Environ 60 000 appels. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement.** Faible risque, gain modere, bonne premiere brique.

---

**B2. Contradictions internes assumees**

- **Mecanisme.** Inscrire explicitement dans le persona une incoherence d'attitude, du type "vous
  etes favorable a la redistribution mais opposee a l'augmentation de vos propres impots", ou plus
  general : "vos opinions ne sont pas toutes coherentes entre elles, comme celles de tout le monde".
- **Cause adressee.** C8, la sur-coherence, qui est mesuree et documentee comme alpha et omega
  gonfles chez les repondants synthetiques [CONFIRME] (https://arxiv.org/html/2608.14606).
- **Precedent.** Le diagnostic est etabli, la correction ne l'est pas. **Je n'ai trouve aucun travail
  injectant deliberement de l'incoherence dans le persona pour recalibrer la fiabilite interne.**
  [HYPOTHESE sur l'absence de precedent, recherche non exhaustive.]
- **Experience la moins chere.** Utiliser un instrument multi-items a sous-echelles connues,
  disponible dans Twin-2K-500. Trois conditions : persona standard, persona avec instruction generale
  d'incoherence, persona avec contradictions specifiques listees. Calculer alpha de Cronbach par
  sous-echelle pour chaque condition et comparer a l'alpha humain.
- **Metrique.** Ecart absolu moyen entre alpha simule et alpha humain, par sous-echelle. Et matrice
  de correlation inter-items, comparee par correlation de Pearson a la matrice humaine.
- **Critere de reussite.** L'ecart d'alpha est divise par deux au moins, sans degrader la
  correlation inter-items de plus de 0,05. Attention au piege : casser la coherence est facile, le
  faire **au bon endroit** ne l'est pas. Le critere doit inclure la structure, pas seulement le
  niveau.
- **Cout.** Zero euro, trois jours.
- **Baseline a battre.** Un modele psychometrique classique a facteur latent plus bruit d'item,
  qui reproduit l'alpha de Cronbach humain par construction. C'est une baseline severe et il faut
  l'annoncer : le LLM doit apporter la **transferabilite** a de nouveaux items, pas la fiabilite.
- **Budget.** Environ 30 000 appels. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement. Originalite elevee, risque moyen.**

---

**B3. Ancrage autobiographique par reponses anterieures reelles**

- **Mecanisme.** Au lieu de decrire la personne, lui montrer ses propres reponses reelles a d'autres
  questions, tirees d'une vague anterieure, et lui demander de repondre a une question tenue a
  l'ecart. Le persona devient un ensemble de comportements observes plutot qu'une description.
- **Cause adressee.** C4 et C5. C'est probablement la voie la plus directe contre le raisonnement
  par stereotype de groupe, puisqu'aucune categorie n'est nommee.
- **Precedent.** C'est le protocole natif de Twin-2K-500, qui partitionne explicitement en JSON de
  persona construit sur les vagues 1 a 3 et en blocs de reponses tenues a l'ecart pour l'evaluation
  [CONFIRME] (https://arxiv.org/html/2505.17479). L'approche est donc connue. Ce qui n'est pas
  documente, a ma connaissance, c'est la **courbe** : combien de reponses anterieures faut-il pour
  restaurer combien de `Var_inter` [HYPOTHESE].
- **Experience la moins chere.** Faire varier k, le nombre de reponses anterieures montrees, dans
  {0, 5, 15, 40, 100, toutes}. Mesurer separement la precision individuelle et `Var_inter`
  populationnelle. 500 personnes de Twin-2K-500, 100 questions tenues a l'ecart.
- **Metrique.** Deux courbes sur le meme graphique en fonction de k : precision individuelle
  normalisee par le plafond de test-retest, et ratio `Var_inter` simule sur humain.
- **Critere de reussite.** Identifier un k ou `Var_inter` atteint 0,8 fois la valeur humaine.
  Resultat encore plus interessant si les deux courbes divergent, c'est-a-dire si ajouter des
  reponses ameliore la precision individuelle **tout en** continuant a comprimer la variance
  populationnelle. Ce serait un resultat contre-intuitif fort et directement publiable.
- **Cout.** Zero euro. Attention aux contextes longs : a k = 100 le prompt devient lourd, prevoir un
  modele a fenetre etendue ou une troncature. Quatre jours.
- **Baseline a battre.** La plus dangereuse du document : les k plus proches voisins sur le meme
  vecteur de k reponses anterieures, sans aucun modele de langage. Sur des donnees denses comme
  Twin-2K-500, cette baseline est tres forte. Si le LLM ne la bat pas a k eleve, la these du persona
  textuel s'effondre pour ce regime, et il faut alors identifier le regime de k faible ou il gagne.
- **Budget.** Environ 50 000 appels pour l'ensemble de la courbe. **Testable cette semaine**, sous
  reserve de la longueur de contexte a k = 100.
- **Verdict.** **Faisable immediatement. C'est l'experience la plus proche du coeur du sujet.**

---

**B4. Persona ecrit a la premiere personne par le modele lui-meme**

- **Mecanisme.** Passer d'une fiche descriptive a la troisieme personne, "Homme, 47 ans, ouvrier",
  a un recit autobiographique a la premiere personne genere par le modele a partir de la fiche, puis
  reutilise comme contexte. Le style de langage devient propre a l'individu.
- **Cause adressee.** C3, l'attenuation du signal de persona dans les couches hautes, sur
  l'hypothese qu'un texte long et stylistiquement marque resiste mieux a la dilution.
- **Precedent.** La generation de personas riches a partir de graines existe a grande echelle, et la
  generation de personas ancres depuis des donnees sociales aussi [PROBABLE, voir Synthia
  https://arxiv.org/pdf/2507.14922]. L'effet propre du **passage a la premiere personne**, a contenu
  informationnel constant, n'est pas isole a ma connaissance [HYPOTHESE].
- **Experience la moins chere.** Meme information, trois encodages : fiche a la troisieme personne,
  recit a la premiere personne, dialogue simule d'entretien. Controler la longueur pour ne pas
  confondre l'effet de forme avec l'effet de volume. 300 personas, 150 questions.
- **Metrique.** `Var_inter`, TVD, et une mesure de persistance : la distance entre la distribution
  de reponse a la question 1 et a la question 100 de la meme session, qui capture la derive de
  persona.
- **Critere de reussite.** Le recit a la premiere personne reduit la derive de persona d'au moins
  30 pour cent a longueur egale. Si l'effet est nul a longueur controlee, c'est un resultat negatif
  utile qui economise du travail a tout le monde.
- **Cout.** Zero euro, deux jours, plus le cout de generation des personas.
- **Baseline a battre.** La fiche a la troisieme personne **completee a longueur egale** par du
  texte neutre, pour ne pas confondre l'effet de forme avec l'effet de volume.
- **Budget.** Environ 45 000 appels. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement.** Potentiel modere, mais le controle de longueur en fait
  une experience propre.

---

**B5. Forcage anti-stereotype calibre**

- **Mecanisme.** Pour chaque persona, tirer d'abord si cet individu sera conforme ou deviant par
  rapport a la modale de son groupe, avec une probabilite de deviance lue dans les donnees humaines
  reelles, puis inscrire le tirage dans le prompt : "sur ce sujet, votre position n'est pas celle de
  la majorite des gens comme vous".
- **Cause adressee.** C4 frontalement. Le modele ne peut plus retomber sur le stereotype puisque le
  prompt lui interdit, et la frequence de l'interdiction est calibree sur le reel.
- **Precedent.** [HYPOTHESE] Je n'ai trouve aucun travail calibrant la frequence d'un forcage
  anti-modal sur la deviance observee dans les donnees d'enquete. Le forcage de diversite existe,
  la calibration de sa frequence sur le taux humain reel ne semble pas etablie.
- **Experience la moins chere.** Estimer, sur le WVS ou le GSS, la proportion reelle de deviants par
  question et par groupe. Tirer le statut conforme ou deviant pour chaque persona selon cette
  proportion. Comparer a la baseline et a un forcage a taux fixe de 30 pour cent, qui sert de temoin.
- **Metrique.** `Var_inter`, et masse de probabilite dans les queues, definie comme la somme des
  probabilites des deux options les moins choisies par le groupe.
- **Critere de reussite.** La masse de queue simulee atteint 0,7 a 1,3 fois la masse de queue
  humaine, contre un facteur typiquement inferieur a 0,4 en baseline. Le temoin a taux fixe doit
  faire moins bien, sinon la calibration n'apporte rien.
- **Cout.** Zero euro, trois jours.
- **Baseline a battre.** Le modele de cellule : tirer la reponse directement dans la distribution
  empirique du groupe demographique. Il reproduit la masse de queue parfaitement sur les questions
  vues et n'apporte rien sur les questions nouvelles. C'est exactement la ou le LLM doit gagner.
- **Budget.** Environ 40 000 appels. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement.** Objection previsible et a anticiper : c'est de la triche,
  on injecte la reponse. Reponse honnete a preparer : oui pour les questions ayant servi a calibrer,
  non si le taux de deviance est appris sur un jeu de questions et transfere a un autre. Le protocole
  **doit** inclure ce transfert, sinon le resultat n'est pas defendable.

---

### FAMILLE C - Agir sur la population entiere

---

**C1p. Recalage sur marges de la population simulee**

- **Mecanisme.** Ne pas corriger chaque agent. Generer N agents, puis leur attribuer des poids par
  ajustement proportionnel iteratif, aussi appele raking, pour que les marges ponderees des reponses
  simulees egalent des marges cibles connues.
- **Cause adressee.** Aucune cause profonde. C'est un correctif de surface, et il faut le dire
  clairement.
- **Precedent.** Le raking est standard en methodologie d'enquete [CONFIRME, methode classique]. Son
  application aux populations synthetiques est deja documentee, avec le compromis identifie : la
  reponderation ameliore la coherence distributionnelle mais **reduit la diversite effective** en
  concentrant la masse sur un petit sous-ensemble d'agents [CONFIRME]
  (https://arxiv.org/html/2602.11569v1).
- **Experience la moins chere.** Appliquer un raking a la population simulee de A1, avec pour cibles
  les marges humaines de 30 questions, puis evaluer sur 100 autres questions non utilisees pour le
  raking. Tracer la taille d'echantillon effective en fonction du nombre d'iterations.
- **Metrique.** TVD sur les questions tenues a l'ecart, et taille d'echantillon effective.
- **Critere de reussite.** Amelioration de la TVD sur les questions tenues a l'ecart d'au moins 15
  pour cent tout en conservant une taille effective superieure a 50 pour cent de N. Si la taille
  effective s'effondre sous 20 pour cent, la piste est un piege et il faut le publier comme tel.
- **Cout.** Zero euro, une journee, aucune inference nouvelle.
- **Baseline a battre.** La population simulee non ponderee, et la post-stratification simple sur
  la jointe demographique.
- **Budget.** Zero appel, post-traitement pur. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement.** Faible originalite, mais c'est la baseline que tout
  reviewer demandera. Ne pas la faire, c'est se faire renvoyer.

---

**C2p. Reechantillonnage par importance vers une distribution jointe cible**

- **Mecanisme.** Generer un vivier surdimensionne, 10 N agents, puis en tirer N par echantillonnage
  d'importance pour approcher non pas les marges mais la **distribution jointe** cible sur plusieurs
  questions simultanement. C'est le raking sans son defaut principal, puisqu'on tire des individus
  entiers au lieu de deformer des poids.
- **Cause adressee.** L'ecrasement de la structure de dependance entre questions, qui est le vrai
  produit vendu. Un institut vend des croisements, pas des marges.
- **Precedent.** L'echantillonnage d'importance est standard. Son application a la selection d'une
  sous-population synthetique pour matcher une jointe multi-questions n'est pas etablie comme
  standard dans ce champ a ma connaissance [HYPOTHESE].
- **Experience la moins chere.** Vivier de 5 000 agents simules. Cible : la distribution jointe
  humaine sur 5 questions choisies. Selectionner 500 agents. Evaluer sur 20 croisements de questions
  **non utilises** dans la selection.
- **Metrique.** V de Cramer simule contre humain sur les croisements tenus a l'ecart, plus taille
  effective.
- **Critere de reussite.** L'ecart moyen de V de Cramer sur les croisements tenus a l'ecart est
  reduit d'au moins 30 pour cent. C'est le vrai test : ameliorer la jointe sur des paires qu'on n'a
  pas ciblees signifie qu'on a capture de la structure, pas qu'on a memorise.
- **Cout.** Zero euro, deux jours, plus 5 000 passes avant, negligeable en lecture de logits.
- **Baseline a battre.** Le raking de C1p, et le tirage direct dans les donnees humaines, qui a la
  jointe exacte et sert de plafond. L'ecart au plafond mesure ce qui reste a gagner.
- **Budget.** Environ 100 000 appels pour le vivier de 5 000 agents sur 20 questions. **Testable
  cette semaine.**
- **Verdict.** **Faisable immediatement. Fort potentiel commercial direct.**

---

**C3p. Hybride copule et LLM**

- **Mecanisme.** Confier au LLM ce qu'il fait bien, les marges conditionnelles a la demographie et
  au contexte semantique, et confier a une copule ce qu'il fait mal, la structure de dependance et
  la dispersion. Le LLM fournit les marges par segment, la copule genere des individus respectant
  ces marges avec la bonne matrice de correlation.
- **Cause adressee.** C3 et C8, en contournant le modele plutot qu'en le corrigeant.
- **Precedent.** Le fait declencheur est publie et il est brutal : une copule gaussienne seule
  atteint un score de similarite psychometrique de 0,688 contre 0,714 pour le meilleur LLM sur 37
  testes, et bat les LLM sur les composantes distribution et correlation inter-items, c = 0,95 et
  r = 0,99 contre c = 0,52 et r = 0,94 [CONFIRME] (https://arxiv.org/html/2608.14606).
  **L'hybride n'est pas construit dans ce papier, il est seulement suggere par le tableau.**
- **Experience la moins chere.** Trois systemes sur les memes questions tenues a l'ecart : copule
  seule ajustee sur les vagues 1 a 3, LLM seul, hybride. La copule n'a pas besoin de GPU, elle
  s'ajuste en quelques secondes sur un ordinateur portable.
- **Metrique.** Une batterie complete : TVD marginale, correlation inter-items, alpha, `Var_inter`,
  et surtout la capacite a repondre a une question **jamais vue par la copule**, ou le LLM devrait
  seul apporter quelque chose.
- **Critere de reussite.** L'hybride bat les deux composants isoles sur au moins 4 des 5 metriques.
  Critere secondaire et plus important scientifiquement : identifier l'ensemble de questions ou le
  LLM apporte une valeur non nulle par rapport a la copule. Si cet ensemble est vide, c'est le
  resultat negatif le plus fort que ce projet puisse produire, et il est publiable.
- **Cout.** Zero euro, une semaine. Nul en GPU pour la partie copule.
- **Baseline a battre.** La copule seule et le LLM seul, par construction de l'experience. C'est la
  seule fiche du document ou la baseline est un composant du systeme teste, ce qui rend la
  comparaison inattaquable.
- **Budget.** Environ 80 000 appels, la partie copule ne consomme aucun appel. **Testable cette
  semaine.**
- **Verdict.** **Faisable immediatement. Meilleur rapport potentiel sur cout de tout le document,
  a egalite avec E2.**

---

**C4p. Appariement par transport optimal entre population simulee et population cible**

- **Mecanisme.** Calculer un couplage de transport optimal entre le nuage des vecteurs de reponse
  simules et le nuage humain, puis mesurer et corriger le deplacement. La correction devient un
  champ de deformation applicable a de nouvelles simulations.
- **Cause adressee.** L'ecrasement geometrique global, sans hypothese sur sa cause.
- **Precedent.** [HYPOTHESE] Le transport optimal est utilise pour comparer des distributions dans
  ce champ, sous la forme de la distance de Wasserstein ou de l'Earth Mover's Distance normalisee
  [CONFIRME comme metrique] (https://arxiv.org/html/2604.06663v1). Son usage comme **operateur de
  correction** plutot que comme metrique n'est pas etabli a ma connaissance.
- **Experience la moins chere.** Reduire chaque repondant, humain et simule, a un vecteur de 50
  reponses. Ajuster un couplage sur un sous-ensemble de questions, appliquer le deplacement au
  reste, evaluer.
- **Metrique.** Distance de Wasserstein entre nuages, avant et apres, sur les dimensions tenues a
  l'ecart.
- **Critere de reussite.** Reduction de 40 pour cent de la distance sur les dimensions non utilisees
  pour ajuster le couplage.
- **Cout.** Zero euro, une semaine. Bibliotheque de transport optimal disponible librement, calcul
  sur processeur pour quelques milliers de points.
- **Baseline a battre.** Le recalage affine simple, c'est-a-dire recentrer et redimensionner chaque
  dimension pour egaler moyenne et ecart-type humains. Si le transport optimal ne bat pas ce
  correctif a deux parametres, il n'est pas justifie.
- **Budget.** Zero appel supplementaire, reutilise les sorties de A1. **Testable cette semaine.**
- **Verdict.** **Faisable, mais risque de sur-ajustement eleve.** A garder en second rideau.

---

**C5p. Retrecissement calibre des ecarts inter-groupes**

- **Mecanisme.** **La seule fiche du document qui va dans le sens inverse de tout le reste.** Si les
  ecarts entre segments sont exageres d'un facteur deux a quatre, il faut les **reduire**. Estimer la
  moyenne simulee de chaque segment, la retrecir vers la moyenne generale d'un facteur lambda ajuste
  sur des donnees humaines, et redistribuer la variance retiree en dispersion intra-segment. Un
  retrecissement de James-Stein applique a l'envers, non pour stabiliser une estimation bruitee mais
  pour degonfler une separation artificielle.
- **Cause adressee.** La premiere branche de la double distorsion, `Var_between` exageree
  [CONFIRME par l'orchestrateur, arXiv 2607.26348], que **aucune methode publiee ne traite** puisque
  tout le champ cherche a augmenter la variance.
- **Precedent.** [HYPOTHESE] Aucun precedent trouve. Le retrecissement vers la moyenne est classique
  en statistique bayesienne empirique, mais son application a la correction d'une caricature de
  groupe produite par un LLM ne semble pas exister. C'est la lacune la plus large du document,
  precisement parce que le champ a mal pose le probleme.
- **Experience la moins chere.** Sur les sorties de logits de A1, calculer les moyennes par segment,
  simulees et humaines. Ajuster un unique lambda sur 30 questions, evaluer sur 100 autres. Deux
  variantes : lambda global, et lambda par variable de segmentation, puisque le genre et le diplome
  n'ont aucune raison d'etre caricatures dans la meme proportion.
- **Metrique.** Ratio `Var_between` simulee sur humaine, et **conjointement** ratio `Var_within`,
  puisque le retrecissement seul degrade la marge globale si la variance retiree n'est pas
  redistribuee.
- **Critere de reussite.** Ratio `Var_between` ramene de l'intervalle 2 a 4 vers 0,85 a 1,15 sur les
  questions tenues a l'ecart, **sans** degradation de la TVD marginale. Combinee a une fiche qui
  augmente `Var_within`, cette fiche doit produire le premier simulateur correct sur les deux
  composantes a la fois, ce qui est l'objectif final du projet.
- **Baseline a battre.** Le modele de cellule, dont la `Var_between` est exacte par construction.
  Le LLM retreci doit l'egaler sur `Var_between` **et** le battre sur `Var_within`, ou il n'a aucun
  interet.
- **Cout.** Zero euro, zero appel supplementaire, deux jours de post-traitement.
- **Budget.** Reutilise les logits de A1. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement, cout quasi nul, et c'est la piste la plus originale du
  document parce qu'elle corrige une erreur que le champ ne cherche meme pas.** A coupler
  obligatoirement avec E1u, qui fournit la mesure.

---

### FAMILLE D - Agir par apprentissage

---

**D1a. LoRA par segment**

- **Mecanisme.** Entrainer un adaptateur de bas rang par segment demographique ou attitudinal, par
  exemple 8 a 20 segments, sur les reponses reelles des membres du segment.
- **Cause adressee.** C3 et C6, en inscrivant l'identite dans les poids plutot que dans le prompt.
- **Precedent.** Etabli. LoRA reduit d'environ 98 pour cent les parametres entrainables tout en
  conservant plus de 95 pour cent des gains du reglage complet, et est deja applique aux reponses
  d'enquete synthetiques [CONFIRME] (https://arxiv.org/pdf/2512.14562).
- **Experience la moins chere.** 8 segments issus d'une classification non supervisee des repondants
  de Twin-2K-500. QLoRA 4 bits sur modele 7B, sur GPU gratuit Colab ou Kaggle. Environ 1 500
  exemples par segment.
- **Metrique.** `Var_inter` entre segments, distance normalisee entre centres de segments,
  precision individuelle.
- **Critere de reussite.** La separation inter-segments, mesuree par distance de transport
  normalisee entre distributions de segments, atteint au moins 0,7 fois la separation humaine,
  contre typiquement moins de 0,3 pour le prompting.
- **Cout.** Zero euro en argent, mais entre 8 et 20 heures de GPU gratuit, contrainte par le quota
  hebdomadaire. Une a deux semaines calendaires.
- **Baseline a battre.** Une regression logistique par segment, et le meme modele en prompting avec
  le segment nomme. La premiere est difficile a battre sur les questions vues.
- **Budget.** Inference negligeable. Le goulot est le GPU d'entrainement gratuit, 8 a 20 heures.
  **Non testable cette semaine.**
- **Verdict.** **Faisable mais lourd.** Faible originalite, precedent direct. A ne lancer qu'apres
  les fiches sans entrainement.

---

**D2a. LoRA par individu : le persona parametrique**

- **Mecanisme.** Une matrice de bas rang par **personne**, rang tres faible, 1 a 4. Le persona n'est
  plus du texte, c'est un point dans un espace de parametres. Consequences immediates et
  attirantes : on peut interpoler entre deux personnes, mesurer la distance entre deux personnes,
  faire une analyse en composantes principales de la population dans l'espace des adaptateurs, et
  echantillonner de nouvelles personnes plausibles en tirant dans cet espace.
- **Cause adressee.** C3, C4, C5 simultanement. Aucune compression textuelle, aucun stereotype
  nomme, aucune dilution a travers les couches.
- **Precedent.** Le LoRA par utilisateur existe, avec des experiences sur 200 utilisateurs et 100 a
  200 interactions chacun [CONFIRME] (https://arxiv.org/pdf/2509.09689). **Ce qui n'existe pas, a
  ma connaissance, c'est l'usage de l'espace des adaptateurs comme espace de population** : mesurer
  si `Var_inter` de la population reelle est preservee dans la geometrie des adaptateurs, et
  echantillonner de nouveaux individus en tirant dans cet espace. [HYPOTHESE sur l'absence de
  precedent.]
- **Experience la moins chere.** Version minimale et honnete du budget zero : 60 personnes de
  Twin-2K-500, environ 300 reponses chacune, LoRA de rang 2 sur les seules matrices de projection
  de valeur, modele 1,5B ou 3B pour tenir dans le quota GPU gratuit. Puis ACP sur les 60 adaptateurs
  aplatis.
- **Metrique.** Trois tests. (1) Precision de prediction sur des questions tenues a l'ecart contre
  la baseline prompt. (2) Correlation entre distance dans l'espace des adaptateurs et distance dans
  l'espace des reponses reelles. (3) Qualite des individus generes en tirant dans l'espace ACP.
- **Critere de reussite.** Le test (2) est le pivot : une correlation de Spearman superieure a 0,5
  entre distance d'adaptateurs et distance de reponses prouve que l'espace des adaptateurs est un
  espace de population, ce qui ouvre tout le reste. Une correlation inferieure a 0,2 ferme la piste
  proprement, et c'est aussi une information utile.
- **Cout.** Zero euro. 60 entrainements courts, estimation entre 10 et 25 minutes chacun sur T4
  gratuit avec un modele 3B en 4 bits [HYPOTHESE de duree, a verifier sur un cas avant de lancer les
  60], soit 10 a 25 heures de GPU, donc deux semaines de quota. Trois semaines calendaires.
- **Baseline a battre.** Les k plus proches voisins individu a individu sur les reponses observees,
  et un modele de reponse a l'item avec un trait latent par personne. Le modele a trait latent est
  la vraie concurrence : lui aussi rend le persona parametrique, avec un seul nombre par personne et
  sans aucun modele de langage. **L'argument du LLM ne peut etre que la generalisation a des
  questions hors du domaine d'entrainement du modele a trait latent, et le protocole doit le
  tester.**
- **Budget.** Inference negligeable. 10 a 25 heures de GPU gratuit. **Non testable cette semaine.**
- **Verdict.** **Faisable mais c'est le projet le plus lourd du document.** Originalite la plus
  elevee. **C'est la piste "papier au MIT" si elle marche.** A lancer seulement apres qu'une des
  pistes legeres ait donne un premier resultat, pour ne pas engager trois semaines a l'aveugle.

---

**D3a. Vecteur de pilotage appris par individu**

- **Mecanisme.** Version pauvre et rapide de D2a. Au lieu d'une matrice, apprendre **une seule
  direction** dans l'espace d'activations par personne, ajoutee aux etats caches a une couche choisie.
  Quelques milliers de parametres par personne au lieu de centaines de milliers.
- **Cause adressee.** C3, avec un cout divise par un ordre de grandeur par rapport a D2a.
- **Precedent.** PSII injecte des vecteurs demographiques plus un bruit gaussien dans les etats
  caches et obtient une baisse de 65 pour cent de la divergence KL et de 96 pour cent de l'ecart
  d'entropie contre la baseline prompt [CONFIRME] (https://arxiv.org/html/2603.16142v1). Les vecteurs
  y sont **par attribut demographique**, pas **par individu**. Le passage a l'individu est la
  variante non couverte [HYPOTHESE].
- **Experience la moins chere.** Reproduire PSII en version reduite sur un modele 1,5B, puis
  remplacer les vecteurs d'attribut par des vecteurs individuels appris par descente de gradient
  sur les reponses de la personne, en gelant tout le reste. 100 personnes.
- **Metrique.** Identique a D2a, plus le rapport gain sur nombre de parametres.
- **Critere de reussite.** Atteindre au moins 70 pour cent du gain de D2a avec moins de 5 pour cent
  de ses parametres. Si D2a n'est pas lance, critere autonome : battre la baseline prompt de 20 pour
  cent en `Var_inter`.
- **Cout.** Zero euro, GPU gratuit, environ 2 a 5 heures au total pour 100 personnes [HYPOTHESE].
  Une semaine.
- **Baseline a battre.** Les vecteurs par attribut demographique de PSII, et le prompting simple.
- **Budget.** 2 a 5 heures de GPU gratuit. **Non testable cette semaine, mais testable la
  suivante.**
- **Verdict.** **Faisable, et c'est la bonne facon de tester D2a a moindre risque.** Faire D3a
  avant D2a.

---

**D4a. Reglage a cible distributionnelle**

- **Mecanisme.** Ne pas entrainer le modele a reproduire la reponse d'une personne mais a reproduire
  la **distribution** de reponses d'un groupe. La perte porte sur la divergence entre la distribution
  predite sur les options et la distribution empirique du groupe, pas sur l'entropie croisee avec un
  token cible.
- **Cause adressee.** C2 a la racine, en changeant l'objectif d'apprentissage lui-meme.
- **Precedent.** [PROBABLE] Des travaux existent sur le forcage de distributions diffuses en sortie
  de modeles de langage, mais je n'ai pas pu les re-verifier dans cette session, et je ne dispose
  pas d'une reference verifiee pour l'application au sondage. A traiter comme une piste dont le
  precedent est incertain.
- **Experience la moins chere.** LoRA sur modele 1,5B, 500 questions du WVS, cible = distribution
  empirique par cellule demographique. Evaluer sur 200 questions tenues a l'ecart.
- **Metrique.** TVD et ratio SD sur les questions tenues a l'ecart. Et test de generalisation croisee
  : entrainer sur le WVS, evaluer sur le GSS, pour verifier qu'on a appris a etre disperse et pas a
  memoriser des marges.
- **Critere de reussite.** Le transfert WVS vers GSS conserve au moins la moitie du gain de ratio SD.
  Sans ce transfert, le resultat est sans valeur.
- **Cout.** Zero euro, GPU gratuit, une a deux semaines.
- **Baseline a battre.** Le modele de cellule, distribution empirique par cellule demographique. Il
  est imbattable sur les questions vues et nul sur les questions nouvelles. Le seul resultat qui
  compte est donc le transfert du WVS au GSS.
- **Budget.** GPU gratuit, une a deux semaines. **Non testable cette semaine.**
- **Verdict.** **Faisable, potentiel eleve, mais precedent mal etabli.** Verifier la litterature
  avant de lancer, sous peine de reinventer.

---

### FAMILLE E - Agir sur l'incertitude et la mesure

---

**E1u. Decomposition a deux composantes avec plafond de bruit humain**

- **Mecanisme.** Estimer, sur des donnees de panel publiques, la variance intra-individuelle humaine
  reelle, et l'utiliser comme plafond de bruit. Puis decomposer l'erreur du simulateur en trois
  parts : biais de moyenne, deficit de `Var_inter`, mauvaise calibration de `Var_intra`. Un
  simulateur qui manque 20 pour cent des reponses individuelles alors que l'humain se contredit
  lui-meme 20 pour cent du temps est **parfait**, pas mediocre. Le champ n'a pas ce cadre.
- **Cause adressee.** C7, et plus fondamentalement le probleme de mesure qui contamine toutes les
  autres pistes.
- **Precedent.** Le plafond individuel de 79,5 pour cent au retest a deux semaines sur le GSS est
  disponible [CONFIRME] (https://arxiv.org/html/2608.14606). Twin-2K-500 integre une baseline de
  test-retest par construction [CONFIRME] (https://arxiv.org/html/2505.17479). Une decomposition en
  composantes de variance de la non-determination des LLM existe, mais sur un autre domaine, les
  reponses de marque, et elle decompose les sources **internes au LLM**, pas l'ecart au comportement
  humain [CONFIRME] (https://arxiv.org/abs/2607.13304). **Le cadre reliant les deux, plafond humain
  et decomposition de l'erreur du simulateur, n'existe pas a ma connaissance.** [HYPOTHESE sur
  l'absence de precedent.]
- **Experience la moins chere.** Aucune inference LLM n'est necessaire pour la premiere moitie.
  Etape 1, pure analyse de donnees : sur Twin-2K-500 et sur un panel GSS, estimer par modele a
  effets mixtes `Var_inter` et `Var_intra` humaines par question et par domaine thematique. Etape 2 :
  appliquer la meme decomposition aux sorties de A1 et A4. Etape 3 : publier le tableau.
- **Metrique.** Les deux composantes en valeur absolue, plus les ratios `Var_inter_LLM` sur
  `Var_inter_H` et `Var_intra_LLM` sur `Var_intra_H`, separement et jamais agreges.
- **Critere de reussite.** Le resultat est le tableau lui-meme, quel qu'il soit. Le resultat
  **remarquable** serait de montrer qu'une methode publiee comme "restaurant la variance" ameliore
  en realite le ratio intra et pas le ratio inter. [HYPOTHESE, mais c'est exactement ce que la
  sur-dispersion documentee de Verbalized Sampling laisse presager.]
- **Cout.** Zero euro. L'etape 1 se fait sur ordinateur portable, sans GPU, en deux a trois jours.
- **Baseline a battre.** Aucune, c'est une mesure et non une methode. Les points de comparaison
  sont les composantes humaines elles-memes, et le modele de cellule, dont la signature attendue est
  `Var_between` exacte et `Var_within` nulle. Placer les LLM sur cet axe entre le modele de cellule
  et l'humain est le contenu de la figure.
- **Budget.** L'etape 1 ne consomme aucun appel. L'etape 2 reutilise les logits de A1. **Testable
  cette semaine, et c'est la fiche a lancer en premier.**
- **Verdict.** **Faisable immediatement, et c'est la piste la moins chere du document au regard de
  son potentiel.** C'est aussi celle qui rend toutes les autres interpretables. **A faire en
  premier.**

---

**E2u. Modele de reponse a deux etages calibre sur panel**

- **Mecanisme.** Modeliser explicitement la reponse comme un latent stable plus un bruit de reponse.
  Le LLM produit le latent, une couche de bruit calibree sur les taux de changement observes dans
  les vagues de panel produit la reponse observable. Le simulateur cesse de pretendre que la personne
  est deterministe.
- **Cause adressee.** C7 et C8.
- **Precedent.** [HYPOTHESE] Standard en psychometrie sous le nom de modele de vraie note, mais je
  n'ai pas trouve d'application ou le bruit de reponse d'un agent LLM est calibre sur des taux de
  changement de panel reels.
- **Experience la moins chere.** Estimer, par question, la matrice de transition humaine entre vagues
  sur Twin-2K-500 vague 4. Appliquer cette matrice en post-traitement aux sorties du simulateur.
  Verifier que la distribution marginale est preservee et que la stabilite test-retest simulee
  rejoint la stabilite humaine.
- **Metrique.** Taux de reproduction test-retest simule contre humain, par question, et preservation
  de la marge.
- **Critere de reussite.** Le taux de reproduction simule tombe dans une fourchette de plus ou moins
  5 points du taux humain sur au moins 80 pour cent des questions, sans deplacer la marge de plus de
  1 point.
- **Cout.** Zero euro, post-traitement pur, deux jours.
- **Baseline a battre.** Une chaine de Markov estimee directement sur les transitions du panel,
  sans aucun modele de langage. Elle reproduit la stabilite test-retest par construction. Le LLM ne
  peut gagner que sur des questions absentes du panel.
- **Budget.** Zero appel, post-traitement pur. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement.** Peu spectaculaire mais indispensable pour toute
  affirmation de fidelite au niveau individuel, et c'est un argument de vente honnete : "nos agents
  changent d'avis a la meme frequence que des humains reels".

---

### FAMILLE F - Agir sur l'evaluation, imposer la metrique du champ

---

**F1e. Score de fidelite de variance, batterie et classement public**

- **Mecanisme.** Publier une batterie standardisee qui refuse de resumer la fidelite en un chiffre
  et impose de rapporter, au minimum : (1) l'erreur de moyenne ; (2) le ratio `Var_inter` ; (3) le
  ratio `Var_intra` ; (4) la masse de queue ; (5) la separation inter-segments ; (6) la preservation
  de la structure de dependance par le V de Cramer ; (7) la taille d'echantillon effective apres
  toute reponderation. Plus un classement public de modeles ouverts.
- **Cause adressee.** Aucune, directement. Elle adresse le fait que le champ optimise la mauvaise
  quantite.
- **Precedent.** Des metriques distributionnelles existent en abondance, TVD, Wasserstein, KL, JS,
  entropie, ratio SD, nEMD, V de Cramer, PSS [CONFIRME, dispersees dans
  https://arxiv.org/html/2604.06663v1, https://arxiv.org/html/2607.18310,
  https://arxiv.org/html/2608.14606]. **Le probleme est qu'il y en a trop et qu'aucune ne separe
  inter et intra.** Le champ n'a pas de standard. Il y a donc une place, et celui qui la prend
  impose son vocabulaire.
- **Experience la moins chere.** Implementer la batterie, l'appliquer a 6 a 8 modeles ouverts sur
  Twin-2K-500 et le WVS, publier le code et le classement.
- **Metrique.** La batterie est la metrique. Le critere de qualite est la lisibilite : chaque
  colonne doit dire quelque chose que les autres ne disent pas, verifiable par la matrice de
  correlation entre colonnes.
- **Critere de reussite.** Aucune paire de colonnes ne correle au-dela de 0,85 sur 8 modeles, ce qui
  prouve que la batterie n'est pas redondante. Et au moins un renversement de classement selon la
  colonne, ce qui prouve qu'un chiffre unique aurait menti.
- **Cout.** Zero euro, une a deux semaines, essentiellement de l'ingenierie.
- **Baseline a battre.** Les metriques agregees existantes, TVD, ratio SD, PSS. La demonstration
  attendue est qu'elles **masquent** la double distorsion, c'est-a-dire qu'il existe deux systemes
  de scores agreges identiques et de decompositions opposees. Construire explicitement ce couple est
  la meilleure figure possible pour justifier la batterie.
- **Budget.** Environ 200 000 appels pour 8 modeles. **Une semaine complete de budget local.**
- **Verdict.** **Faisable immediatement. Meilleur actif strategique du document.** Une metrique
  adoptee est cite par tous les papiers suivants, et c'est aussi l'argument commercial : "voici la
  grille sur laquelle on evalue une population synthetique, et voici notre score".

---

**F2e. Le test de la baseline sans modele de langage**

- **Mecanisme.** Imposer que toute publication de simulation de sondage compare a une baseline
  statistique n'utilisant aucun modele de langage : copule gaussienne, ou simple reechantillonnage
  stratifie d'une enquete anterieure. Rendre ce test obligatoire, et le nommer.
- **Cause adressee.** Aucune. Elle adresse l'exageration systematique du champ.
- **Precedent.** Le fait est deja publie : une copule gaussienne atteint 0,688 contre 0,714 pour le
  meilleur des 37 LLM testes, et bat les LLM sur trois composantes sur six [CONFIRME]
  (https://arxiv.org/html/2608.14606). **Mais il est presente comme un detail dans un audit, pas
  comme une norme methodologique.**
- **Experience la moins chere.** Reprendre 4 a 6 methodes publiees de restauration de variance, les
  reimplementer en version minimale, et les comparer toutes a la copule sur les memes donnees. C'est
  un travail de reproduction, pas d'invention.
- **Metrique.** Fraction des methodes publiees qui battent effectivement la copule, et sur quelles
  metriques.
- **Critere de reussite.** Si au moins deux methodes publiees ne battent pas la copule sur les
  metriques distributionnelles, c'est un resultat negatif propre, de haute valeur, et exactement le
  genre de chose qui interesse un chercheur senior.
- **Cout.** Zero euro. La copule s'ajuste en secondes sur un ordinateur portable. Une a deux semaines
  pour la reproduction des methodes.
- **Baseline a battre.** La baseline **est** l'objet de la fiche. A elargir au-dela de la copule :
  regression logistique sur demographies, modele de cellule, plus proches voisins, bootstrap de
  l'enquete precedente. Quatre baselines, aucune n'utilisant de modele de langage.
- **Budget.** Environ 150 000 appels pour reproduire les methodes publiees. **Testable cette
  semaine.**
- **Verdict.** **Faisable immediatement. Risque politique reel** : ce papier se fait des ennemis. Il
  se fait aussi remarquer. A discuter avec Simon avant de le lancer, c'est une decision de
  positionnement, pas une decision technique.

---

**F3e. Indice de double distorsion**

- **Mecanisme.** Une metrique unique et lisible qui rend la compensation impossible a cacher. Poser
  R_between = `Var_between_LLM` / `Var_between_H` et R_within = `Var_within_LLM` / `Var_within_H`.
  Reporter le couple (R_between, R_within) comme un **point dans un plan**, jamais comme un scalaire.
  L'humain est en (1, 1). Le modele de cellule est en (1, 0). Les LLM actuels se situent, selon les
  chiffres disponibles, dans la region (2 a 4 ; 0,4 a 0,6). Un simulateur qui affiche une variance
  globale correcte se trouve sur l'hyperbole de compensation, qui devient visible immediatement.
- **Cause adressee.** La faille de mesure elle-meme, qui conditionne l'interpretation de toutes les
  autres fiches.
- **Precedent.** [HYPOTHESE] Aucune metrique publiee ne separe ces deux termes a ma connaissance.
  Les batteries existantes rapportent une variance intra-groupe et une distance inter-groupes
  [CONFIRME] (https://arxiv.org/html/2604.06663v1) mais dans des tableaux separes, sans les opposer
  ni signaler la compensation.
- **Experience la moins chere.** Placer sur ce plan les 6 a 8 modeles ouverts evalues en F1e, plus
  les quatre baselines non LLM de F2e, plus chaque intervention testee dans ce document sous forme
  de fleche. **Une seule figure resume alors tout le projet.**
- **Metrique.** Le couple lui-meme, plus la distance euclidienne au point (1, 1) comme resume, a
  n'utiliser **qu'en complement** et jamais seul.
- **Critere de reussite.** Montrer au moins deux systemes de variance globale identique et de
  position tres differente dans le plan. C'est la preuve par l'exemple que la metrique agregee ment,
  et cela suffit a justifier l'adoption de l'indice.
- **Baseline a battre.** Le ratio SD global et la TVD marginale, qu'il s'agit de disqualifier comme
  metriques suffisantes.
- **Cout.** Zero euro, zero appel nouveau, une journee de mise en forme sur les sorties de F1e.
- **Budget.** Aucun appel propre. **Testable cette semaine.**
- **Verdict.** **Faisable immediatement.** C'est le livrable visuel du projet et l'actif de
  vocabulaire le plus facile a imposer. Un nom, une figure, deux axes.

---

### FAMILLE G - Melange et ensembles

---

**G1. Modeles differents pour segments differents**

- **Mecanisme.** Ne pas utiliser un seul modele pour toute la population. Assigner a chaque segment
  le modele qui le simule le mieux, mesure sur des donnees de validation. L'heterogeneite de la
  population est portee par l'heterogeneite du parc de modeles.
- **Cause adressee.** C6, la sous-representation, sur l'hypothese que differents modeles ont
  differents angles morts demographiques.
- **Precedent.** La recommandation de comparaisons multi-modeles pour documenter comment differents
  LLM encodent ou effacent la diversite sociale est explicitement formulee comme priorite de
  recherche [CONFIRME] (https://arxiv.org/html/2604.06663v1). L'usage d'un **melange** de modeles
  affectes par segment n'est pas realise dans ce papier.
- **Experience la moins chere.** 5 modeles ouverts, 8 segments. Matrice 5 par 8 d'erreur par segment.
  Affectation gloutonne du meilleur modele par segment sur une moitie des questions, evaluation sur
  l'autre moitie.
- **Metrique.** TVD globale et `Var_inter` du melange contre le meilleur modele unique.
- **Critere de reussite.** Le melange bat le meilleur modele unique de 10 pour cent en TVD sur les
  questions tenues a l'ecart. **Risque a annoncer d'avance** : si la matrice d'erreur est de rang
  faible, c'est-a-dire si un modele est meilleur partout, la piste est morte, et la matrice elle-meme
  est alors le resultat interessant.
- **Cout.** Zero euro, 5 modeles a telecharger, environ une semaine.
- **Baseline a battre.** Le meilleur modele unique, et une regression logistique globale.
- **Budget.** Environ 5 fois 40 000 egale 200 000 appels. **Une semaine complete de budget local**,
  ou deux si les modeles sont gros.
- **Verdict.** **Faisable immediatement.** Bon ratio, resultat interessant dans les deux cas.

---

**G2. Melange de versions et de quantifications du meme modele**

- **Mecanisme.** Variante pauvre de G1. Utiliser le meme modele en plusieurs quantifications, 4 bits,
  8 bits, 16 bits, et plusieurs versions ou tailles, comme sources de variance supplementaire. La
  degradation par quantification devient une ressource au lieu d'un defaut.
- **Cause adressee.** C2, par introduction d'une perturbation structuree du calcul plutot que du
  tirage.
- **Precedent.** [HYPOTHESE] Aucun precedent trouve. C'est probablement parce que l'idee est
  mauvaise, mais elle est presque gratuite a tester.
- **Experience la moins chere.** Un modele, 3 quantifications, memes personas, memes questions.
  Verifier d'abord si les distributions different, ce qui est la question prealable.
- **Metrique.** Divergence entre distributions par quantification, puis `Var_inter` du melange.
- **Critere de reussite.** Etape 1 : les distributions different de facon mesurable, TVD superieure
  a 0,05 entre quantifications. Si non, arreter la, une demi-journee perdue. Etape 2 : le melange
  augmente `Var_inter` de plus de 15 pour cent sans degrader la moyenne.
- **Cout.** Zero euro, une demi-journee pour l'etape 1 qui sert de filtre.
- **Baseline a battre.** Le modele unique en 16 bits.
- **Budget.** Environ 15 000 appels pour l'etape de filtre. **Testable en une demi-journee.**
- **Verdict.** **Faisable immediatement, cout quasi nul, potentiel faible.** A faire pendant un
  temps mort, pas a planifier.

---

**G3. Simulation par cohorte plutot que par individu**

- **Mecanisme.** [Idee propre] Renverser la formulation. Ne pas demander "que repond cette personne",
  mais "sur 100 personnes de ce profil, combien repondent A, B, C ?". Le modele produit directement
  un comptage. C'est la question a laquelle un modele de langage entraine sur du texte statistique
  et journalistique est le mieux prepare a repondre, puisque c'est la forme sous laquelle les
  resultats d'enquete existent dans ses donnees d'entrainement.
- **Cause adressee.** C4, en retirant au modele l'obligation de jouer un individu, et C1, puisqu'on
  ne lui demande plus de choisir une reponse consensuelle mais de decrire une repartition.
- **Precedent.** Proche de Verbalized Sampling mais pas identique : VS demande une distribution de
  probabilite sur des reponses, ici on demande un **comptage sur une cohorte nommee**, ce qui ancre
  dans un cadre de reference statistique concret. [HYPOTHESE] Je n'ai pas trouve de comparaison
  directe entre les deux formulations.
- **Experience la moins chere.** Trois formulations sur 200 questions et 20 profils : individu tire
  N fois, distribution verbalisee, comptage de cohorte. Le comptage de cohorte coute un seul appel
  par profil et par question.
- **Metrique.** TVD, ratio SD, cout en appels.
- **Critere de reussite.** Le comptage de cohorte atteint une TVD dans les 3 points de la meilleure
  des deux autres formulations pour un cout inferieur d'un facteur 10. Ou, plus interessant, il
  echoue nettement, ce qui indiquerait que le modele recite des statistiques memorisees quand on
  formule ainsi, hypothese testable en comparant les reponses aux vrais chiffres publies avant et
  apres la date de coupure du modele.
- **Cout.** Zero euro, deux jours.
- **Baseline a battre.** Les chiffres publies de l'enquete elle-meme, qui servent de test de
  contamination, et le modele de cellule. Si le comptage de cohorte egale les chiffres publies
  anterieurs a la date de coupure et s'effondre apres, le modele recite au lieu de simuler, et c'est
  le resultat de la fiche.
- **Budget.** Environ 12 000 appels, le comptage de cohorte etant tres econome. **Testable cette
  semaine.**
- **Verdict.** **Faisable immediatement.** Le test de contamination avant et apres date de coupure
  est ce qui rend cette fiche scientifiquement interessante plutot que simplement pratique.

---

## 3. La menace de baseline : ou le LLM doit structurellement gagner

**C'est la section la plus importante du document.** Si une regression logistique sur les
demographies bat un LLM sur la prediction individuelle, toute la these du projet tombe. Or c'est
partiellement le cas : au niveau individuel, aucun LLM n'egale les modeles de base sur le GSS et le
WVS [CONFIRME par l'orchestrateur, arXiv 2607.26348, "When Synthetic Users Fail"], et une copule
gaussienne sans modele de langage atteint 0,688 contre 0,714 pour le meilleur de 37 LLM sur un audit
psychometrique [CONFIRME] (https://arxiv.org/html/2608.14606).

La question n'est donc plus "le LLM simule-t-il bien une population". C'est : **existe-t-il un
regime ou un persona LLM apporte quelque chose qu'aucun modele statistique ne peut apporter ?**
La valeur est la, ou nulle part. Voici les cinq candidats, avec pour chacun le test le moins cher.

### 3.1 Les cinq regimes candidats

**Regime 1. Les questions jamais posees dans l'enquete d'origine.**
Aucune baseline ne peut etre entrainee sur une question qui n'existe pas dans les donnees. Une
regression, une copule, un modele de cellule, un plus-proche-voisin ont tous besoin de la colonne.
Le LLM, lui, comprend l'enonce. **C'est l'avantage structurel le plus net et le moins contestable.**
[PROBABLE, c'est une propriete du type de modele, pas une observation empirique.]
Test le moins cher : prendre 100 questions de Twin-2K-500, entrainer toutes les baselines sur 400
questions **excluant** ces 100, et comparer sur les 100. Zero appel supplementaire si les logits
sont deja calcules. Critere : le LLM bat la meilleure baseline de 10 points de precision normalisee.
**C'est le test decisif du projet et il coute deux jours.**

**Regime 2. Le transfert d'un domaine, d'un pays ou d'une epoque a un autre.**
Une baseline entrainee sur le WVS turc ne transfere pas au GSS americain. Le LLM porte un a priori
semantique transferable. Test : entrainer les baselines sur le WVS, evaluer sur le GSS, comparer au
LLM sans aucun entrainement. Critere : le rapport de performance LLM sur baseline est
significativement plus favorable en transfert qu'en domaine. [HYPOTHESE, non verifiee, mais
testable a cout nul puisque les deux enquetes sont gratuites.]

**Regime 3. Les tres petits echantillons.**
Avec 30 repondants reels, une regression a 12 variables est ingerable et une copule ne s'ajuste pas.
Le LLM part d'un a priori et n'a besoin de rien. Test : faire varier la taille d'entrainement des
baselines dans {10, 30, 100, 300, 1000, 2000} et tracer les deux courbes. **Il existe forcement un
point de croisement**, la seule question est ou il se situe. Si le croisement est a 2 000, le projet
n'a pas de marche, puisque les instituts ont plus que cela. S'il est a 300, le produit d'extension
d'enquete est justifie. **Cette courbe unique vaut plus que toute demonstration, scientifiquement et
commercialement.** Cout : deux jours, zero appel nouveau.

**Regime 4. Les interactions d'ordre eleve entre attributs.**
Une regression capte les effets principaux et quelques interactions d'ordre deux. Un ouvrier
catholique de 62 ans dans une region desindustrialisee est une cellule qui contient trois personnes
dans l'echantillon, donc statistiquement vide. Le LLM peut interpoler semantiquement. Test :
selectionner les cellules demographiques a effectif inferieur a 10 dans le GSS, comparer LLM et
baselines sur ces seules cellules. Critere : l'avantage du LLM croit quand l'effectif de cellule
decroit. [HYPOTHESE.] **Attention, contre-argument serieux** : c'est aussi la ou la
sous-representation dans les donnees d'entrainement frappe le plus fort, et le resultat pourrait
etre inverse. Les deux issues sont informatives.

**Regime 5. Les questions ouvertes et le raisonnement justificatif.**
Aucune baseline statistique ne produit une justification en langage naturel. Mais [PROBABLE] la
valeur y est difficile a evaluer sans jugement humain, ce qui viole la contrainte "aucun humain
recrute". Substitut a cout nul : verifier que la justification generee **predit** la reponse fermee
de la meme personne a une autre question, ce qui teste sa validite sans juge humain. Test partiel
seulement. **A traiter comme differe.**

### 3.2 Ce que cette section impose au projet

1. **Toute fiche de la section 2 doit etre evaluee dans au moins un de ces cinq regimes**, pas en
   domaine plein ou les baselines gagnent. Evaluer une methode de restauration de variance sur des
   questions que la copule connait deja, c'est organiser sa propre defaite.
2. **La contribution vendable n'est probablement pas la simulation, c'est l'extrapolation.** Le
   pitch honnete devient : "vous avez 500 repondants et 80 questions, nous vous donnons les 200
   questions que vous n'avez pas posees, avec une variance calibree". Ce n'est pas le pitch du
   CONTEXTE, et c'est une reorientation a discuter avec Simon.
3. [HYPOTHESE, importante] **Si aucun des cinq regimes ne donne d'avantage net, le resultat negatif
   est publiable et il est fort.** "Les modeles de langage n'apportent rien de mesurable a la
   simulation d'enquete par rapport a des baselines statistiques classiques, dans les cinq regimes
   ou l'on pourrait les attendre" est un papier que la communaute lirait. C'est le plan de repli, et
   il est solide. Il faut le dire des maintenant, avant d'y etre contraint.

---

## 4. Idees produit et strategie de credibilite

### 4.1 Dix usages, classes par monetisabilite et facilite de demonstration

Rappel du cadrage : un institut n'achete pas une moyenne, il achete des segments, des minorites
d'opinion et des queues de distribution. Toute demonstration qui montre une moyenne bien reproduite
demontre exactement ce que le client sait deja faire moins cher.

| # | Usage | Monetisable | Demontrable a budget zero | Commentaire |
|---|---|---|---|---|
| 1 | Detection de segment minoritaire : trouver les 5 a 10 pour cent qui pensent autrement | Tres eleve | Moyen | C'est le produit. Necessite que `Var_within` soit reparee **et** que `Var_between` soit degonflee, donc C5p couplee a A3, B5 ou C2p. Une seule des deux ne suffit pas. |
| 2 | Pre-test de questionnaire : reperer les questions ou la population va se diviser avant le terrain | Eleve | **Eleve** | Ne demande pas de reproduire la reponse, seulement de predire la dispersion. Beaucoup plus facile et deja utile. |
| 3 | Extension d'enquete existante : le client a 500 repondants reels, on en genere 5 000 coherents | Tres eleve | Eleve | Demontrable sur donnees publiques en cachant une partie des repondants. |
| 4 | Detection de question a risque : formulations qui produisent des reponses instables | Eleve | **Tres eleve** | Directement issu de E2u. Se demontre sur donnees publiques seules, sans meme un LLM performant. |
| 5 | Simulation contrefactuelle de message : comment une population reagit a trois formulations | Tres eleve | Faible | Sans validation humaine, invendable. **Differe.** |
| 5b | Extension de questionnaire : le client a 80 questions, on lui donne les 200 qu'il n'a pas posees | Tres eleve | **Tres eleve** | Ajoute apres la section 3. C'est le **regime 1**, le seul ou aucune baseline statistique ne peut concourir. Probablement le vrai produit du projet. |
| 6 | Ponderation et redressement assiste pour enquetes sous-echantillonnees | Moyen | Eleve | Marche mature, marges faibles, mais porte d'entree credible chez les instituts. |
| 7 | Reproduction retrospective d'etudes publiees, pour le pitch "montrez-nous votre derniere etude" | Eleve | **Tres eleve** | Piege majeur : contamination par memorisation. Ne vaut que sur des enquetes posterieures a la date de coupure du modele. |
| 8 | Simulation de sous-populations rares, minorites, professions peu nombreuses | Tres eleve | Faible | C'est precisement la ou les modeles echouent le plus, couverture demographique insuffisante [CONFIRME] (https://arxiv.org/html/2603.16142v1). Honnetement : pas avant longtemps. |
| 9 | Generation de guides d'entretien qualitatif et de personas pour equipes marketing | Faible | Tres eleve | Deja fait par tout le monde avec un abonnement grand public. Sans defense. |
| 10 | Audit de fidelite de populations synthetiques tierces, vendu comme certification | Moyen a eleve | **Tres eleve** | Decoule directement de F1e. Ne demande pas de savoir simuler, seulement de savoir mesurer. Le plus rapide a mettre en vente. |

Lecture strategique : les usages 2, 4, 5b, 7 et 10 sont demontrables **maintenant**, a budget zero,
et trois d'entre eux ne demandent pas de resoudre le probleme scientifique, seulement de le mesurer.
L'usage 10 est le plus sous-estime : vendre la mesure avant de vendre la solution est classique dans
les marches immatures, et le champ est immature. L'usage 5b est celui qui resiste le mieux a la
section 3, puisqu'il se place dans le seul regime ou aucune baseline statistique ne peut concourir.

### 4.2 Strategie de credibilite face au MIT

Postulat, et il faut s'y tenir : **un chercheur ne s'interesse pas a une demonstration.** Une demo
qui marche declenche la question "et par rapport a quoi ?". Ce qui l'interesse, c'est un resultat
negatif propre ou un resultat positif surprenant.

Ordre de presentation recommande.

**Premier temps, le resultat negatif propre : la double distorsion.** Le plan (R_between, R_within)
de la fiche F3e, avec dessus les modeles ouverts, les quatre baselines non LLM, et les methodes de
restauration de variance publiees en 2026 representees par des fleches. Le message tient en une
phrase : "le champ corrige la variance avec un bouton unique alors que les deux composantes sont
fausses en sens contraire, et voici la figure qui le montre". C'est defendable, cela ne coute rien,
et ce n'est pas attaquable sur les moyens puisque ce sont les donnees des autres. **[HYPOTHESE] Si
la figure montre des methodes publiees qui ameliorent la variance globale en degradant la structure,
c'est un papier a soi seul.**

**Deuxieme temps, le resultat qui derange : la delimitation du domaine de validite.** Les cinq
regimes de la section 3, avec pour chacun la courbe LLM contre baselines. Le fait de base est deja
publie, aucun LLM n'egale les modeles de base au niveau individuel [CONFIRME par l'orchestrateur,
arXiv 2607.26348], donc le risque scientifique est faible. La contribution est de dire **ou** la
frontiere passe, en particulier le point de croisement du regime 3, taille d'echantillon. Un
chercheur senior reconnaitra immediatement la valeur de cette delimitation, parce que c'est la
question qu'il se pose deja et que personne n'a chiffree.

**Troisieme temps, la piste positive.** Deux idees, dans cet ordre. D'abord C5p, le retrecissement
inter-groupes, qui est la seule intervention du document allant dans le sens que le champ ignore, et
qui est presque gratuite. Ensuite l'espace des adaptateurs comme espace de population (D3a puis
D2a), la seule idee qui, si elle marche, change la formulation du probleme : un persona cesse d'etre
du texte et devient un point dans un espace metrique. C'est aussi la plus chere, elle ne doit pas
ouvrir la conversation mais la conclure, en tant que programme propose.

**Resultat minimal qui rend la conversation interessante.** [PROBABLE] Une figure et un chiffre.
La figure : le plan (R_between, R_within) sur Twin-2K-500, pour 4 a 6 modeles ouverts et quatre
baselines. Le chiffre : le point de croisement du regime 3, c'est-a-dire la taille d'echantillon
en dessous de laquelle le LLM bat la regression. Cela tient sur une page, ne coute rien, et pose
deux questions auxquelles personne n'a repondu. C'est plus convaincant qu'une simulation de 10 000
agents, qui impressionne un investisseur et laisse un chercheur indifferent.

**Ce qu'il ne faut pas montrer.** La simulation a 10 000 ou 20 000 agents, tant que la fidelite a
petite echelle n'est pas etablie. L'echelle est un argument commercial, et l'exhiber devant un
chercheur signale une confusion de registre. La montee en echelle reste un objectif du projet, elle
n'est simplement pas un argument de credibilite scientifique.

---

## 5. Paris risques

**Tous les items de cette section sont [SPECULATIF].** Faible probabilite de succes, fort impact en
cas de succes. Aucun ne doit etre lance avant qu'une piste de la section 2 ait produit un resultat.

**R1. La variance perdue est-elle recuperable, ou detruite ?**
Question theorique : l'alignement a-t-il **detruit** l'information sur la dispersion des opinions,
ou l'a-t-il seulement **rendue inaccessible au decodage** ? Test : comparer un modele de base non
aligne et sa version alignee, memes poids d'origine, sur la meme tache de sondage en lecture de
logits. Si le modele de base a une meilleure `Var_inter`, l'information est intacte et l'alignement
la masque, ce qui reoriente tout le champ vers des methodes de recuperation plutot que de
reconstruction. Des paires base et aligne sont publiquement disponibles pour plusieurs familles de
modeles ouverts, donc le test est faisable a budget zero. Le risque est que la difference soit
confondue avec l'incapacite du modele de base a suivre le format d'instruction, ce qui exige un
protocole de format tres soigneux. Baseline a battre : aucune, c'est une comparaison interne, ce qui
rend l'experience inhabituellement solide. Budget : environ 60 000 appels, **testable cette
semaine**. **Si le resultat est net, c'est le papier le plus cite de la liste.** A mesurer sur les
deux composantes separement : il se peut que l'alignement ecrase `Var_within` **et** gonfle
`Var_between`, ce qui unifierait les deux branches de la double distorsion sous une cause unique.
Ce serait le resultat theorique le plus fort accessible a ce projet.

**R2. Le persona comme condition initiale d'un systeme, pas comme description.**
Et si l'unicite d'une personne n'etait pas dans ses attributs mais dans sa trajectoire ? Faire
converser deux agents pendant 50 tours avant de leur poser la question du sondage, en variant
uniquement la graine de conversation. L'hypothese est que l'historique cree une divergence
individuelle que le prompt ne cree pas. Test de l'hypothese contraire, plus probable : la
conversation fait **converger** les agents. Les deux resultats sont interessants, et le second
serait une demonstration elegante que la socialisation simulee homogeneise. Baseline a battre : le
meme agent sans historique, a longueur de contexte egale remplie de texte neutre, pour ne pas
confondre effet de trajectoire et effet de contexte long. Cout : eleve en inference, une conversation
de 50 tours par agent, de l'ordre de 100 000 appels pour 200 agents, soit un quart du budget
hebdomadaire. **Testable, mais a reserver a un petit echantillon.**

**R3. Apprendre la deviance plutot que la position.**
Ne pas modeliser l'opinion d'une personne mais son **ecart** a la modale de son groupe, comme une
quantite propre et transferable entre domaines. L'hypothese forte : quelqu'un qui devie de son groupe
sur la politique devie aussi sur la consommation, et cette propension a la deviance est un trait
individuel stable. Testable directement sur Twin-2K-500 sans aucun LLM : correler les scores de
deviance d'une meme personne entre domaines. Si la correlation est superieure a 0,3, il existe un
trait de deviance, on peut le simuler, et cela donnerait une facon entierement nouvelle de restaurer
`Var_within` : un seul parametre par personne au lieu d'un persona, et un parametre qui n'est
correle a aucune demographie, donc qui n'aggrave pas `Var_between`. Baseline a battre : la
demographie seule, dont la deviance predite est nulle par construction. **Cout du test initial : une
journee, aucun appel, aucun GPU, aucun LLM.** C'est le pari risque le moins cher du document et je
le recommanderais presque en section 2, ce que reflete la sequence de la semaine 3.

**R4. Population comme objet, avec une perte au niveau population.**
Traiter la population entiere de N agents comme un objet unique optimise par une perte
populationnelle, et non comme N tirages independants. Chaque agent est genere conditionnellement
aux agents deja generes, avec une contrainte de couverture explicite, comme un echantillonnage
determinantal. Aucun precedent trouve dans ce champ. Le risque est que le cout devienne quadratique
en N et que le procede introduise une dependance artificielle entre repondants, ce qui viole
l'hypothese d'independance dont dependent toutes les statistiques d'enquete. C'est un probleme
serieux et il faudrait le resoudre avant de publier. Baseline a battre : C2p, le reechantillonnage
par importance, qui atteint le meme objectif de couverture par selection au lieu de generation, pour
un cout lineaire. Si C2p suffit, R4 n'a pas de raison d'exister.

**R5. Falsifier la simulabilite.**
Chercher a etablir une borne superieure : existe-t-il des questions ou aucun conditionnement, aussi
riche soit-il, ne permet de predire l'individu au-dela du hasard ? Methode : sur Twin-2K-500,
donner au modele **toutes** les autres reponses de la personne et mesurer ce qui reste impredictible,
apres correction par le plafond de test-retest. Un theoreme d'impossibilite empirique, meme partiel,
serait une contribution majeure et rare, parce que le champ ne publie que des reussites. Risque
principal : un resultat negatif d'impossibilite se confond toujours avec une insuffisance de methode,
et il est tres difficile de convaincre un relecteur du contraire. Attenuation possible : montrer que
**toutes** les methodes, LLM et baselines statistiques confondues, plafonnent au meme niveau sur les
memes questions. Une borne atteinte par des familles de modeles sans rapport entre elles est un
argument bien plus fort qu'une borne atteinte par une seule. Baseline a battre : sans objet, ici les
baselines sont des co-temoins et non des concurrents. Budget : environ 150 000 appels, **testable
cette semaine**. C'est la fiche la plus ambitieuse et la plus fragile.

---

## 6. Classement general : potentiel scientifique contre cout de test

Echelles de 1 a 5. Potentiel : contribution scientifique si le resultat est positif **ou** negatif
proprement etabli. Cout : 1 = une journee sans GPU, 5 = plusieurs semaines avec GPU.

| Rang | Fiche | Potentiel | Cout | Ratio | Commentaire |
|---|---|---|---|---|---|
| 1 | **E1u** decomposition a trois niveaux | 5 | 1 | 5,0 | Aucun appel pour la moitie. Rend toutes les autres pistes lisibles. |
| 2 | **F3e** indice de double distorsion | 5 | 1 | 5,0 | Une figure, deux axes, un nom. L'actif de vocabulaire du projet. |
| 3 | **Section 3, regime 1 et regime 3** questions non posees et petits echantillons | 5 | 1,5 | 3,3 | Ce n'est pas une fiche mais c'est le test decisif du projet. Deux jours. |
| 4 | **C5p** retrecissement inter-groupes | 5 | 1,5 | 3,3 | Corrige une erreur que le champ ne cherche meme pas. Zero appel nouveau. |
| 5 | **F2e** baseline sans modele de langage obligatoire | 5 | 1,5 | 3,3 | Le fait est publie, la norme ne l'est pas. Risque politique a assumer. |
| 6 | **R3** trait de deviance transferable | 5 | 1,5 | 3,3 | Etiquete speculatif mais le test initial coute une journee sans GPU. |
| 7 | **A3** correcteur de sur-dispersion de VS | 4 | 1,5 | 2,7 | Le trou le plus visible et le mieux delimite du champ. |
| 8 | **C3p** hybride copule et LLM | 5 | 2 | 2,5 | Suggere par les donnees publiees, jamais construit. |
| 9 | **A2** recalage en temperature | 3 | 1 | 3,0 | Rendement immediat, originalite faible, indispensable. |
| 10 | **A4** decouplage des deux temperatures | 4 | 2 | 2,0 | Produit une figure marquante. Attention, ne traite pas `Var_between`. |
| 11 | **B3** courbe d'ancrage autobiographique | 4 | 2 | 2,0 | Au coeur du sujet. Baseline des plus proches voisins tres severe. |
| 12 | **C2p** reechantillonnage sur la jointe | 4 | 2 | 2,0 | Le plus proche du produit vendable. |
| 13 | **F1e** batterie standardisee | 4 | 2,5 | 1,6 | Support de F3e. Consomme une semaine entiere de budget local. |
| 14 | **A1** lecture des logits | 2,5 | 1 | 2,5 | Peu original, mais brique obligatoire de toutes les autres fiches. |
| 15 | **E2u** modele a deux etages | 3 | 1,5 | 2,0 | Indispensable a toute affirmation individuelle. |
| 16 | **B2** contradictions assumees | 3,5 | 2 | 1,8 | Cible un defaut documente et non corrige. |
| 17 | **D3a** vecteur de pilotage par individu | 4,5 | 3 | 1,5 | Le bon test preliminaire de D2a. Premier poste de GPU. |
| 18 | **G3** simulation par cohorte | 3 | 1,5 | 2,0 | Le test de contamination lui donne sa valeur. |
| 19 | **B5** forcage anti-stereotype calibre | 3,5 | 2 | 1,8 | Ne vaut que si le transfert entre jeux de questions est inclus. |
| 20 | **G1** modeles differents par segment | 3 | 2,5 | 1,2 | Interessant dans les deux issues. |
| 21 | **B1** enrichissement idiosyncratique | 2,5 | 1,5 | 1,7 | Faible risque, gain modere. |
| 22 | **C1p** raking | 2 | 1 | 2,0 | Baseline exigee par tout relecteur. Pas une contribution. |
| 23 | **D2a** LoRA par individu | 5 | 5 | 1,0 | La piste "papier au MIT" si elle marche. A n'engager qu'apres D3a. |
| 24 | **B4** persona a la premiere personne | 2,5 | 1,5 | 1,7 | Le controle de longueur en fait une experience propre. |
| 25 | **D4a** reglage a cible distributionnelle | 4 | 4 | 1,0 | Precedent mal etabli, verifier avant de lancer. |
| 26 | **C4p** transport optimal correctif | 3 | 3 | 1,0 | Risque de sur-ajustement eleve. |
| 27 | **D1a** LoRA par segment | 2,5 | 4 | 0,6 | Precedent direct, peu d'originalite pour beaucoup de calcul. |
| 28 | **G2** melange de quantifications | 1,5 | 0,5 | 3,0 | Ratio flatteur mais plafond bas. A faire dans un temps mort. |

Observation qui saute aux yeux : **les six premieres lignes du classement ne consomment presque
aucun appel de modele.** Elles sont soit du post-traitement sur des logits deja calcules, soit de
l'analyse de donnees publiques sans LLM. Le goulot de ce projet n'est pas le calcul, c'est la
clarte conceptuelle sur ce qu'il faut mesurer.

Regle de sequencement qui decoule du tableau : **tout ce qui ne demande pas de GPU d'entrainement
d'abord**, parce que sous contrainte de budget zero le GPU est la ressource rare, alors que
l'inference locale ne l'est pas, environ 400 000 appels par semaine gratuits. Ne depenser du GPU
qu'une fois qu'une mesure fiable existe pour juger du resultat, c'est-a-dire apres E1u et F3e.

Sequence concrete sur quatre semaines, a budget zero :
- **Semaine 1** : A1, A2, E1u, F3e, plus les regimes 1 et 3 de la section 3. Environ 80 000 appels.
  A la fin de la semaine, on sait si le projet a un domaine de validite.
- **Semaine 2** : C5p, A3, C3p, F2e. Presque aucun appel nouveau. A la fin, on a une methode qui
  corrige les deux composantes et une comparaison honnete aux baselines.
- **Semaine 3** : A4, B3, C2p, E2u, R3. Environ 250 000 appels.
- **Semaine 4** : D3a sur GPU gratuit, et redaction. D2a seulement si D3a a donne un signal.

---

## 7. Ce que je n'ai pas pu verifier

- **Les deux papiers transmis par l'orchestrateur**, arXiv 2607.26348 "When Synthetic Users Fail"
  et arXiv 2608.14606 "Plausible but Not Valid", sont declares verifies par lui. J'ai lu directement
  le second [CONFIRME]. **Je n'ai pas ouvert le premier moi-meme**, et le facteur deux a quatre
  d'exageration inter-groupes, qui est devenu l'axe structurant de ce document, repose donc sur sa
  verification et non sur la mienne. C'est la dependance la plus lourde du fichier et je la signale
  comme telle. Si ce chiffre est faux, la fiche C5p et une partie de la section 1.1.1 tombent.
- **La decomposition exacte par les logits**, `Var_totale = E[Var_intra] + Var_entre`, est declaree
  verifiee par l'agent infrastructure. Je ne l'ai pas re-derivee ni implementee ici. Elle est
  mathematiquement standard, loi de la variance totale, mais son applicabilite pratique depend de
  l'acces aux logits sur le modele retenu et du fait que la variance intra d'un persona soit bien
  celle de la distribution sur les options a une seule position de token, ce qui suppose des items
  fermes et un format de reponse strictement contraint.
- **Le budget de 400 000 appels par semaine sur M5 32 Gio** vient de l'agent infrastructure. Toutes
  les mentions "testable cette semaine" en dependent. Je n'ai fait aucune mesure de debit.
- **La reference de depart du projet**, https://arxiv.org/html/2603.28066v1, n'a pas ete ouverte
  dans cette session. Le CONTEXTE signale deja qu'elle peut ne pas correspondre au papier attendu.
  Un autre agent couvre ce point.
- **Les quotas GPU gratuits.** J'ai suppose que Kaggle Notebooks offre un quota hebdomadaire de
  l'ordre de 30 heures et que Colab niveau gratuit reste utilisable. Ces conditions changent
  frequemment. **Toutes les fiches de la famille D reposent sur cette hypothese non verifiee** et
  doivent etre reevaluees si le quota a disparu.
- **Les durees d'entrainement** annoncees dans D2a et D3a, 10 a 25 minutes par adaptateur, sont des
  estimations et non des mesures. Faire un cas unique avant d'engager les 60.
- **L'acces effectif a Twin-2K-500.** Le papier et la page HuggingFace existent [CONFIRME], mais je
  n'ai pas telecharge les donnees ni verifie la licence et les conditions de reutilisation. C'est
  la premiere chose a faire, puisque cinq fiches en dependent.
- **Les millesimes exacts des panels GSS** a plusieurs vagues.
- **La disponibilite des top-logprobs sur les API fermees.** J'affirme [PROBABLE] que certaines API
  exposent les 20 premieres log-probabilites, ce qui suffirait pour des items a 5 ou 7 modalites,
  mais je ne l'ai pas verifie dans cette session. Sans cela, la fiche A1 exige des poids ouverts en
  local, ce qui reste compatible avec le budget zero.
- **Santurkar et al. 2023 sur OpinionQA** : cite de memoire, non re-verifie ici.
- **Les travaux sur le forcage de distributions diffuses** mentionnes en D4a : je n'ai pas de
  reference verifiee, la fiche porte donc un precedent incertain.
- **L'exhaustivite de mes affirmations d'absence de precedent.** Chaque fois que j'ecris "je n'ai
  trouve aucun travail", c'est le resultat d'une recherche ciblee de quelques requetes, pas d'une
  revue systematique. Le champ produit plusieurs papiers par mois sur ce sujet precis depuis le
  debut 2026. **Toute fiche que le projet decide de lancer doit faire l'objet d'une verification
  d'anteriorite dediee avant, pas apres.**

## 8. Questions ouvertes pour Simon

1. **Le champ nous a rattrapes, et le probleme n'est pas celui que le CONTEXTE decrit.** Au moins
   cinq papiers 2026 attaquent frontalement l'ecrasement de variance, donc "les LLM ecrasent la
   variance" est desormais l'etat de l'art et non la contribution. Plus important : ce n'est pas un
   ecrasement mais une **double distorsion**, `Var_between` exageree d'un facteur deux a quatre et
   `Var_within` ecrasee. **Le point 4 de l'ambition scientifique du CONTEXTE doit etre reecrit**, et
   c'est une decision qui t'appartient.
2. **Le projet a-t-il un domaine de validite ?** C'est la question de la section 3, et elle est
   existentielle. Si aucun des cinq regimes ne donne d'avantage net au LLM sur une regression
   logistique, la these tombe. Ma recommandation est de **trancher cette question la premiere
   semaine**, avant tout investissement, parce que le test coute deux jours et zero euro. Es-tu
   d'accord pour que le projet accepte, des maintenant, l'hypothese qu'il puisse s'agir d'un papier
   de resultat negatif ?
3. **Faut-il assumer le papier qui derange ?** Publier que des baselines statistiques sans modele de
   langage egalent les LLM (F2e) est le resultat le plus fort disponible a cout nul, et c'est un
   papier qui se fait des ennemis dans une communaute dont on cherche par ailleurs l'acces. Decision
   de positionnement, pas decision technique.
4. **Ta lecture psychologue sur la sur-coherence.** Les repondants synthetiques ont un alpha de
   Cronbach gonfle par rapport aux humains [CONFIRME] (https://arxiv.org/html/2608.14606). Y a-t-il
   une litterature psychometrique sur la structure de l'incoherence attitudinale humaine qui
   permettrait d'injecter l'incoherence **au bon endroit** plutot qu'uniformement, ce qui est le
   point faible de la fiche B2 ?
5. **Le trait de deviance existe-t-il ?** La fiche R3 suppose qu'une propension individuelle a
   devier de son groupe est stable entre domaines. Est-ce un construit connu en psychologie sociale,
   sous quel nom, et est-il mesure ? Si oui, le pari risque le plus interessant du document devient
   une piste ordinaire, et il faut le monter en priorite.
6. **Le precedent Nature en psychiatrie** evoque dans le CONTEXTE : la reference exacte permettrait
   de savoir si ces auteurs ont traite la question inter / intra, qui est centrale en clinique ou la
   variabilite intra-patient est un objet d'etude en soi.
7. **Le contact MIT tolere-t-il un resultat negatif comme entree en matiere ?** Ma recommandation
   est d'ouvrir sur F3e, la figure de double distorsion, et sur la section 3, donc sur des resultats
   qui disent que le champ mesure mal et que les baselines gagnent souvent. C'est le plus solide
   scientifiquement et c'est aussi le plus risque relationnellement si l'interlocuteur est engage
   dans une de ces approches.
8. **Y a-t-il un acces academique a du calcul ?** Toute la famille D bascule de "lourd" a "facile"
   avec quelques centaines d'heures de GPU d'entrainement. L'inference n'est pas le probleme,
   environ 400 000 appels locaux gratuits par semaine sont disponibles. Un rattachement, meme
   informel, a un laboratoire change le classement de la section 6 de facon substantielle.
