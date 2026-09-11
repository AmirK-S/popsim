# Prochaine validation externe après R6

Décision préparée le 11 septembre 2026 à partir des rapports, jeux de données et scripts déjà présents dans le dossier. Aucun appel de modèle, aucun appel payant et aucune trace R6 ne sont lus ou modifiés. Ce document ne change aucune page de plan existante.

## Question de décision

Le dossier possède désormais des diagnostics de fidélité de groupe, de correspondance conditionnelle à la personne et de stabilité de protocole. Il ne possède pas encore la preuve qui justifie leur emploi pratique : qu'un diagnostic calculé sur des réponses humaines d'audit permet de choisir, avant de voir une autre cible humaine, la méthode qui prédit mieux cette cible.

Le test utile doit donc contenir quatre objets séparés : un bloc A pour mesurer le diagnostic, un bloc B humain tenu à l'écart pour noter la décision, des méthodes concurrentes ayant la même information admissible, et une règle qui ferme la revendication si le choix par le diagnostic ne fait pas mieux qu'un choix par exactitude brute.

## Idées écartées avant sélection

R2 et R2b ne conviennent pas : ils évaluent une rareté précise dans le même paquet Stanford et ne fournissent pas une cible B indépendante. Le détecteur i3 et i3b ne convient pas : il manque une contamination réelle connue et une décision prédictive à noter. R7 ne convient pas : ses checkpoints n'ont pas de vérité humaine nouvelle. Le bloc de second ordre s1 est intéressant, mais ses dix énoncés seuls ne donnent pas assez d'unités de contenu pour porter le premier test de sélection. Toute analyse des traces R6 est exclue tant que la collecte est active et, de toute façon, R6 ne fournit pas une cible humaine future.

## Option 1, recommandée : tournoi A vers B sur Twin-2K-500

### Estimand

Sur chaque partition d'items, le diagnostic de correspondance à la personne calculé sur le bloc A sélectionne une configuration dont la perte humaine sur le bloc B est inférieure à celle sélectionnée par l'exactitude A seule.

La quantité primaire est

`Delta = perte_B(configuration choisie par diagnostic) moins perte_B(configuration choisie par exactitude A)`.

La convention est que `Delta` doit être négatif. La perte primaire est la distance ordinale normalisée par item, puis l'exactitude catégorielle est publiée comme contrôle. Le diagnostic est la chute sous permutation intra `S_gra`, résidualisée par rapport à l'exactitude A parmi les configurations admissibles, exactement dans l'esprit de `t1-correlation-residus.csv`. Il teste ce que la correspondance à la personne ajoute à la précision apparente, au lieu de choisir simplement la configuration qui imite le mieux les modalités fréquentes.

### Données et découpage

Twin-2K-500 est un jeu CC BY 4.0, produit par une autre équipe, avec 2 058 personnes, trois vagues de contexte, une vague 4 de retest et treize configurations déjà générées. `t1` a déjà vérifié l'alignement des personnes, des 108 items catégoriels répétés et des treize sorties. C'est le seul jeu local à la fois redistribuable, indépendant de Stanford, suffisamment grand et déjà doté de plusieurs fabricants de jumeaux.

Les 108 items de vague 4 sont répartis avant calcul en trois blocs B de 36 items, stratifiés par famille de questionnaire et type de réponse. Pour chaque rotation, les 72 autres items constituent A. Une configuration ne participe que si elle couvre les mêmes personnes et les mêmes cellules dans A et B, selon un seuil fixé avant lecture. Les deux sorties dont le contrôle de masque échoue déjà dans `i3b` restent hors du tournoi principal. Les fichiers `QID287` et `QID290` du bloc False consensus sont gelés comme contrôle externe descriptif, non comme cible primaire : dix énoncés ne suffisent pas pour porter seuls le verdict.

### Adversaire

Le premier adversaire est la sélection conventionnelle : retenir la configuration qui a la meilleure exactitude dans A. Le second est PMM k=10, calculé hors pli sur le même contexte de vagues 1 à 3, avec B1 et B2 publiés comme bornes. Le tournoi principal sépare les configurations riches qui reçoivent le contexte de la personne des conditions démographiques seules, afin de ne jamais présenter une différence d'information comme une victoire de méthode.

La règle de choix est fixée avant résultat : une seule configuration issue du diagnostic, une seule issue de l'exactitude et le meilleur adversaire statistique. Il n'y a ni réglage de seuil sur B, ni sélection après lecture d'un item.

### Puissance et faisabilité

Chaque bloc B contient environ 74 000 réponses potentielles, mais l'unité de généralisation n'est pas la cellule. L'inférence doit rééchantillonner simultanément les 2 058 personnes et les 36 items B, puis refaire le choix complet dans chaque réplication. Cela donne une puissance réelle sur les personnes sans prétendre avoir 74 000 sujets indépendants. Les trois rotations, les analyses laissant une famille entière dehors et le contrôle False consensus rendent visible une éventuelle dépendance au contenu.

Le calcul utilise les chargeurs et les baselines de `t1_commun.py` et `t1_baselines.py`, plus les sorties déjà présentes dans `data/twin2k500/`. Il ne demande aucun modèle, aucun service, aucune donnée nouvelle et aucun euro. Le coût marginal est quelques heures de calcul local et un nouveau préenregistrement externe avant le premier chiffre.

### Critère de chute

La revendication d'utilité du diagnostic ferme si, sur la moyenne des trois rotations, le choix par diagnostic ne réduit pas la perte B d'au moins 0,01 point de distance normalisée par rapport au choix par exactitude et si la borne supérieure de son intervalle à 95 pour cent n'est pas inférieure à zéro. Elle ferme aussi si le résultat disparaît lorsque chaque famille d'items est laissée dehors ou si PMM égale ou bat systématiquement la configuration retenue.

Un résultat négatif serait excellent scientifiquement : le papier garderait la démonstration que les dimensions se dissocient, mais retirerait explicitement toute prétention à guider le choix d'un simulateur. Un résultat positif serait la première pièce qui transforme notre audit en outil de décision contrôlable, et non en tableau descriptif de métriques.

## Option 2 : validation chronologique sur les anticipations SCE

### Estimand

Choisir avant mars 2025, à partir d'une fenêtre d'audit historique, entre une population simulée riche, une population à étiquette, la persistance individuelle, PMM et le tirage de cohorte, puis noter la méthode retenue sur les révisions réellement observées entre mars et juin 2025.

La cible primaire serait le gain hors échantillon sur la composante résiduelle au delà de la persistance, mesuré par Spearman intra mois et intra cohorte. Les cibles secondaires seraient la chute sous permutation, la part inter cohortes et le rapport d'ampleur des révisions contre le nul à dérive. C'est une vraie cible temporelle humaine postérieure à la coupure déclarée de gpt oss 20b et de Llama 3.1 8B.

### Données, adversaire et faisabilité

Le SCE contient 82 535 observations de 10 974 ménages sur 70 mois. `c1` établit que l'historique du ménage atteint une chute de 0,639, la persistance seule 0,615 et les démographies 0,003. Le protocole existant `protocoles/02-plan-nuit-sce.md` fournit déjà le contexte de décembre 2024 à février 2025, les quatre mois de cible et les contrôles C2, C3, DESC, persistance, cohorte et tirage.

Pour devenir une validation de sélection, il faudrait ajouter une fenêtre d'audit antérieure, sans toucher aux mois cibles, puis geler quelle règle choisit une méthode. Même limitée à `infl1`, cette extension double à peu près le bloc machine principal, soit environ 9 600 appels locaux et deux à trois heures de machine dans la configuration déjà mesurée. Elle ne demande pas d'achat, mais les microdonnées SCE ne sont pas redistribuables comme Twin : le code serait public, les tables agrégées reproductibles par un lecteur autorisé, les lignes individuelles ne le seraient pas.

### Critère de chute et valeur scientifique

Elle ferme si la méthode choisie par audit ne bat pas la persistance sur la composante résiduelle dans la fenêtre mars à juin 2025, ou si C3 ne bat pas C2 après que les deux ont reçu leur information déclarée. Un échec démontrerait directement qu'un jumeau de ménage ne fournit pas un outil de prévision ou de politique au delà de la réponse précédente. Un succès aurait une valeur appliquée forte pour les anticipations macroéconomiques.

Cette option est moins bonne comme prochaine validation : elle introduit simultanément une nouvelle famille de modèles, un jeu sous licence d'usage, une fenêtre temporelle et une application bancaire. Si elle échoue, on ne saura pas si le diagnostic est mauvais, si les modèles échouent ou si le dispositif de ménages est trop difficile. Elle doit venir après une réponse nette de Twin, pas à sa place.

## Recommandation

Faire d'abord l'option 1. Elle est le test le plus propre de notre revendication centrale : le diagnostic choisit ou ne choisit pas une meilleure méthode sur un autre bloc humain, dans un jeu externe, redistribuable, avec treize fabricants déjà disponibles, sans appel et sans dépense. Préenregistrer ensuite l'option 2 seulement si l'option 1 montre un gain qui survit aux blocs d'items et à PMM. Cet ordre évite de consacrer une nuit de simulation et un récit d'application à une métrique dont l'utilité n'aurait pas encore passé son test le plus simple.

## Ce que je n'ai pas pu vérifier

Je n'ai pas relu le protocole de génération de chacune des treize configurations Twin pour prouver que chaque item B est absent de tout contexte présenté au modèle. Cette provenance doit être auditée avant le préenregistrement, avec exclusion automatique de toute configuration qui aurait vu une réponse B autrement que par l'historique de retest autorisé. Je n'ai pas calculé la distribution des 108 items entre familles, ni la taille exacte après intersection des masques : le script de partition devra l'écrire et arrêter le run si un bloc B perd sa couverture ou n'atteint pas le seuil fixé. Enfin, SCE est disponible sans frais sous conditions de licence FRBNY, mais ce document ne conclut pas qu'il peut être versé tel quel dans un dépôt public.
