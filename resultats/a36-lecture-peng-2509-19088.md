# a36. Lecture integrale de Peng et al., arXiv 2509.19088

« Digital Twins are Funhouse Mirrors: Five Systematic Distortions ». Lecture faite le 8 septembre
2026 sur le PDF arXiv v5 du 19 avril 2026, converti avec `pdftotext -layout` : 223 pages, 7 004
lignes de texte, corps principal, references, materiel supplementaire A a J et les dix neuf
annexes de sous etudes comprises. Plus le depot de code public, lu par l'API GitHub et par
`raw.githubusercontent.com`, sans etre clone ni execute.

Ce rapport repond a la commande de lecture du 8 septembre et remplace, sur ce papier, la seule
ligne L02-01 de `corpus/lecture-complete/02-homogeneite-variance-correctifs.md`. Il leve deux des
six points de la section F de cette lecture, et en ajoute quatre que la lecture precedente n'avait
pas vus, tous les quatre situes dans le depot de code et non dans l'article.

Sources ouvertes pour ce rapport :

- `https://arxiv.org/pdf/2509.19088v5`, 8 892 599 octets, 223 pages.
- `https://arxiv.org/abs/2509.19088` pour l'historique de soumission.
- `https://api.github.com/repos/TianyiPeng/Twin-2K-500-Mega-Study` pour la licence et la date.
- `https://raw.githubusercontent.com/TianyiPeng/Twin-2K-500-Mega-Study/main/post_metric_calculation/average_metrics_by_specification.csv`
- `https://raw.githubusercontent.com/TianyiPeng/Twin-2K-500-Mega-Study/main/post_metric_calculation/joint_vector_metrics.csv` (en tete seulement)
- `https://raw.githubusercontent.com/TianyiPeng/Twin-2K-500-Mega-Study/main/post_metric_calculation/compute_vector_metrics.py`
- `https://raw.githubusercontent.com/TianyiPeng/Twin-2K-500-Mega-Study/main/post_metric_calculation/post_processing_caliberation/README.md`
- `https://raw.githubusercontent.com/TianyiPeng/Twin-2K-500-Mega-Study/main/post_metric_calculation/post_processing_caliberation/calibration_metrics_by_specification.csv`

Aucun calcul n'a ete fait pour ce rapport. Tous les chiffres cites sont lus tels quels, soit dans
le PDF, soit dans un fichier publie par les auteurs.

---

## 0. Fiche d'identite, et deux corrections a porter dans la lecture 02

Vingt trois auteurs, Columbia University pour vingt et un d'entre eux, Yale pour Akshit Kumar,
Yeshiva pour Patryk Perkowski. Auteur correspondant Olivier Toubia. Categorie cs.CY.
[CONFIRME, page de titre du PDF, page 1]

**Correction 1.** La lecture 02 donne le titre « Digital Twins are Funhouse Mirrors: Five
Systematic Distortions ». C'est le titre de la page 1 du PDF. Les metadonnees du meme PDF et la
page de resume arXiv portent un titre different : « Digital Twins as Funhouse Mirrors: Five Key
Distortions », avec **as** et non **are**, et **Key** et non **Systematic**.
[CONFIRME, champ Title de `pdfinfo` et page `arxiv.org/abs/2509.19088`] En redaction, citer le
titre de la page de titre et signaler l'ecart, ou citer la version Science Advances.

**Correction 2.** La lecture 02 ecrit « Grace Jiarui Fan, Malek Ben Sliman, Eric J. Johnson,
Olivier Toubia et 14 autres ». Le compte exact est vingt trois auteurs, dont onze ne sont pas
nommes dans notre notice. [CONFIRME, page de titre]

Historique : v1 du 23 septembre 2025, v2 du 9 octobre 2025, v3 du 7 novembre 2025, v4 du
4 janvier 2026, v5 du 19 avril 2026. [CONFIRME, page de resume arXiv]

---

## 1. Leurs donnees, leurs modeles, leurs conditions, leur decodage

### 1.1 Les donnees

Dix neuf sous etudes preenregistrees sur `researchbox.org/4145`, **164 resultats** preenregistres,
**N = 13 506** participations humaines cumulees sur les sous etudes, **1 784 participants uniques**.
Les humains sont ceux du panel Twin-2K-500, reinvites sur Prolific ; les sous etudes ont tourne
**d'avril a juin 2025**, approbation IRB Columbia, protocole IRB-AAAV5832.
[CONFIRME, corps de l'article page 3 pour les comptes, section Materials and Methods page 27 pour
les dates et l'IRB]

Le point qui compte pour nous : **chaque humain et son jumeau ont recu exactement les memes
questions, y compris les memes tirages de randomisation**. « Respondents and their twins were
always assigned to the same condition(s) ensuring a fair 1-to-1 comparison. »
[CONFIRME, materiel supplementaire, section J, page 86]

La persona complete est construite par apprentissage en contexte a partir de plus de 500 questions,
soit **environ 128 000 caracteres**, soit **environ 30 000 jetons par jumeau** : 14 questions
demographiques, **279 questions de personnalite** issues de 19 tests mesurant 26 construits,
**85 questions de capacites cognitives** sur 11 mesures, **34 questions de preferences economiques**
sur 10 mesures, **48 questions d'heuristiques et biais** issues de 16 experiences, et une etude de
prix de 40 questions. Duree moyenne de passation humaine 145 minutes, quatre vagues.
[CONFIRME, corps de l'article page 5, et section C.1 page 57 pour le compte de jetons]

**Detail decisif pour notre plancher.** Twin-2K-500 comporte quatre vagues, « with wave 4 repeating
questions from waves 1 to 3 for test to retest purposes ». Peng et al. **utilisent la vague 4 comme
entree de la persona**, pas comme plancher de bruit : « For persona construction, when a question
appears in both waves 1 to 3 and wave 4, we use the wave 4 responses. »
[CONFIRME, section C.1, page 57] Le materiel de reinterrogation est donc dans leurs mains, il est
consomme comme information et jamais comme reference.

### 1.2 Les conditions de persona

Cinq conditions dans l'article, et vingt trois specifications dans les sorties publiees.

| condition | contenu de `{Persona Profile}` |
|---|---|
| **full persona** | l'integralite des reponses Twin-2K-500 de la personne, environ 30 000 jetons |
| **persona summary** | resume par enonces, environ 13 000 caracteres, environ 3 000 jetons, avec information distributionnelle, par exemple « score extraversion = 2.125 (26th percentile) » |
| **demographics only** | les **14 variables demographiques** seules |
| **empty persona** | le marqueur litteral `[Empty Persona Profile]`, invite identique pour tous |
| **random** | tirage uniforme sur l'etendue du resultat, **aucun modele appele** |

[CONFIRME, corps pages 8 a 12, sections C.1 a C.4 pages 57 a 67, section G.1 page 77]

Les 14 variables demographiques, enumerees mot pour mot : « region, sex, age, education, race,
citizenship, marital status, religion, religious attendance, **political party**, household income,
**political ideology**, household size, employment status », et les auteurs precisent qu'elles sont
« part of the Twin-2K-500 dataset (and therefore **also included in the full persona description**) ».
[CONFIRME, corps page 9]

**C'est le point le plus important de la lecture pour la question 5.** L'etiquette de parti et
l'etiquette d'ideologie sont dans la condition demographique **et** dans la persona complete.
Aucune condition du papier ne retire l'etiquette en gardant l'information individuelle. Il n'existe
donc, chez eux, aucune ablation de l'etiquette a modele et a personne constants.

### 1.3 Les modeles et le decodage

Modele principal : **GPT-4.1, date 2025-04-14, temperature 0,7 par defaut**. Variantes :
temperature 0 ; **GPT-5** a temperature 1 « due to the API restriction » ; **DeepSeek-R1-0528** a
temperature 0 ; **Gemini-2.5-flash** a temperature 0 ; **Gemini-3-pro** a temperature 1, « as Google
recommends not changing the temperature of this model » ; un **GPT-4.1 ajuste** sur Twin-2K-500,
3 epoques, taille de lot 4, multiplicateur de taux d'apprentissage 2, limite de 65 536 jetons ;
**Centaur**, c'est a dire `marcelbinz/Llama-3.1-Centaur-70B` en BF16, et son socle
**Llama-3.1-70B**, tous deux a temperature 0, en plan 2 par 2 avec persona summary et empty persona.
« All other API parameters for these benchmarks were kept at their default values. »
[CONFIRME, corps page 11, sections G.2 page 77, G.3 page 79, H page 81]

Le decodage : **un seul appel par jumeau et par enquete**, sortie JSON, post traitement pour
garantir l'absence de valeur manquante ou hors domaine, et **reprise de l'appel** en cas d'echec de
validation. [CONFIRME, section Materials and Methods, pages 27 et 28]

**Ce qu'il n'y a pas, et je l'ai cherche mot a mot.** Aucun tirage repete, aucune graine, aucune
lecture de la distribution de sortie, aucune moyenne sur plusieurs echantillons. Les mots `seed`
au sens de graine aleatoire, `replicate`, `repetition` sont absents du protocole. La seule source
de variation de la condition `empty persona` est nommee explicitement : « with serving status and
characteristics of the base model such as temperature being the only source of variation ».
[CONFIRME, corps page 8, et recherche exhaustive dans les 7 004 lignes]

Cela nous concerne directement : nos mesures a23 sur la distribution complete de sortie contre la
reponse la plus probable, et sur la temperature qu'il faudrait pour combler l'ecart, **n'ont aucun
equivalent chez eux**. Ils ne peuvent pas savoir quelle part de leur sous dispersion vient du
tirage.

### 1.4 Les baselines non LLM

Deux, et elles sont serieuses.

1. **Le tirage uniforme** sur l'etendue du resultat. Exactitude individuelle **0,629**, correlation
   **0,001**. Les auteurs s'en servent pour dire que l'echelle absolue de leur exactitude ne veut
   rien dire : « underscoring that absolute levels of individual-level accuracy should be
   interpreted relative to this baseline ». [CONFIRME, corps pages 8 et 9]

2. **XGBoost**, entraine **par resultat** sur un sous echantillon de participants, avec soit la
   persona complete soit les seules demographies comme predicteurs. Perimetre : les 106 resultats
   dont l'effectif depasse 650, taille d'entrainement variee de 50 a 650, jumeaux a temperature 0.
   [CONFIRME, corps page 23 et note 12]

C'est la baseline la plus dure du corpus a ce jour, et elle donne le chiffre le plus derangeant du
papier : **la correlation predictive d'XGBoost sur persona complete reste sous 0,29 meme avec 650
participants d'entrainement**, et les jumeaux atteignent la correlation d'un XGBoost entraine sur
**environ 180 participants**, ou **environ 225** dans le cas demographique, et l'exactitude d'un
XGBoost entraine sur **environ 75**. [CONFIRME, corps pages 24 et 25, figures 5 et 6]

Leur conclusion, a citer telle quelle contre toute lecture triomphaliste de nos propres baselines :
« despite being extensive and based on decades of social science research, the twins' blueprint
data has limited intrinsic potential to capture human behavior in our context ».
[CONFIRME, corps page 24]

---

## 2. Leurs mesures exactes, et leurs chiffres cles

### 2.1 Les quatre mesures, et ce que chacune prend pour unite

| mesure | definition exacte | unite d'appariement |
|---|---|---|
| **exactitude individuelle** | `1 - (MAD / range)`, ou MAD est l'ecart absolu moyen entre la reponse d'un humain et celle de **son** jumeau, `range` l'etendue naturelle du resultat ; moyennee sur les participants pour chaque resultat | apparie personne a personne ; **161** resultats, trois exclus faute d'etendue definie |
| **correlation** | correlation entre reponses humaines et reponses de jumeaux **a travers les participants, pour chaque resultat** ; moyenne globale par transformation z de Fisher | apparie personne a personne ; 164 resultats |
| **Glass's Delta** | `(moyenne_jumeaux - moyenne_humains) / ecart_type_humains`, en valeur absolue ; l'ecart type humain seul, « as the assumption of equal variances between the two samples is not valid in our setting » | agrege, pas d'appariement |
| **rapport d'ecarts types** | `ecart_type(jumeaux) / ecart_type(humains)`, **un rapport par resultat** | agrege, pas d'appariement |

[CONFIRME, corps pages 6 a 8, note 5 pour les 161 resultats, note 6 pour Glass's Delta]

Ils opposent explicitement leur correlation a celle de Park et al. : « Note that (17) report a much
higher correlation in their digital twin study. However, they compute the correlation across
questions for each participant. In contrast, we compute the correlation across participants for
each outcome. This is more often the measure of interest ». [CONFIRME, corps page 11]

### 2.2 Les trois distances MAD, et de quoi a quoi exactement

Les reponses sont **normalisees entre 0 et 1**, puis on calcule l'ecart absolu moyen entre deux
familles de reponses, moyenne sur les resultats. Les trois valeurs :

- **full persona contre demographics only : 0,132**
- **full persona contre empty persona : 0,175**
- **full persona contre humains : 0,252**

Les deux ecarts sont a p inferieur a 0,01. Citation exacte : « That is, answers from full-persona
twins are closer to those from demographics-only twins than to those from empty-persona twins or
real humans. » [CONFIRME, corps page 15, distorsion 2]

Et le mot que la lecture 02 avait releve, dans son unique occurrence de tout le papier : « the
answers are overly "shrunk" towards a base model ». [CONFIRME, corps page 14, distorsion 1]

### 2.3 Le tableau des chiffres

| quantite | valeur | localisation |
|---|---|---|
| exactitude, persona complete | **0,748** | corps p. 8 |
| exactitude, demographies seules | **0,746**, difference non significative, **p = 0,37** | corps p. 9 |
| exactitude, persona vide | 0,734, ecart de 0,014, « albeit statistically significant » | corps p. 8 |
| exactitude, tirage uniforme | 0,629 | corps p. 8 |
| exactitude, meilleure configuration | 0,752, GPT-4.1 a temperature 0 | corps p. 12 |
| correlation, persona complete | **0,197** | corps p. 11 |
| correlation, demographies seules | 0,145 | corps p. 11 |
| correlation, persona vide | 0,080 | corps p. 11 |
| correlation, hasard | 0,001 | corps p. 11 |
| correlation, meilleure configuration | **0,232**, GPT-4.1 a temperature 0 | corps p. 12 |
| correlation positive | 157 sur 164, soit 95,7 % ; significativement dans 97, soit 59,1 % | corps p. 10 |
| ecart de moyennes | **0,352 ecart type** en moyenne ; significatif dans **105 sur 164**, soit 64,0 % | corps p. 10 |
| **ecart type du jumeau inferieur a l'humain** | **154 sur 164, soit 93,9 %** ; significativement dans **140** de ces 154 | corps p. 14 |
| dissociation travaillee | `r_demo` = 0,105 contre `r_full` = 0,555 ; exactitude 0,892 contre 0,907 | corps p. 15, figure 3 |
| desirabilite sociale | **55 resultats sur 164** portent l'etiquette | SI section E, p. 69 |

La dissociation travaillee porte sur un resultat nomme : **« Lack of Control », sous etude 2,
« Affective Primes »**. [CONFIRME, corps page 15]

### 2.4 La definition exacte de « socially costly », et ce qu'elle vaut

Il n'y a pas de definition de « socially costly ». Il y a **une etiquette binaire parmi dix sept**,
dont voici l'enonce complet : « **Social desirability (55 outcomes): has a socially desirable
answer (e.g., willingness to be an organ donor)** ». [CONFIRME, SI section E, page 69]

Ce qu'il faut savoir avant de s'appuyer dessus :

1. Les etiquettes **ne sont pas exclusives** : « The categorical labels in our meta-analysis are not
   mutually exclusive; an outcome may be tagged with multiple labels. » [CONFIRME, SI section E,
   page 69]
2. **Le papier ne dit nulle part qui a code ces 55 resultats, ni comment, ni avec quel accord
   inter juges.** J'ai cherche `coder`, `coded by`, `we label`, `two authors`, `inter-rater`,
   `interrater` dans les 7 004 lignes : aucune occurrence. [CONFIRME par recherche exhaustive]
3. La meta regression est un **modele lineaire mixte a intercepts aleatoires par sous etude**, la
   variable expliquee etant la correlation transformee en z. [CONFIRME, SI section E, page 71]
4. **Le coefficient de la desirabilite sociale n'est ecrit nulle part en chiffres.** Il est dans la
   figure 11, une image. Seuls le signe et la significativite sont dans le texte. La lecture 02
   avait raison sur ce point et l'interdiction reste valable : **ne pas citer d'ampleur.**

La phrase du texte, dans sa forme exacte : « the correlation was significantly lower for outcomes
where social desirability was salient, suggesting twins are less capable of mimicking human
responses in socially-sensitive contexts (descriptive evidence suggests twins are more likely to
provide socially-desirable responses) ». [CONFIRME, corps page 13] Le membre entre parentheses est
donne comme **descriptif**, sans chiffre, sans test et sans renvoi a une annexe.

Autre coefficient utile pour nous : « Correlations were also lower in the political domain
(consistent with previous findings such as (13) or (14)) », et le domaine politique compte
**12 resultats**. [CONFIRME, corps page 13, SI page 70]

---

## 3. Les cinq questions de la commande, une par une

### 3.1 Un terme inter groupes ? Presque pas, et une seule fois

**Dans le corps de l'article : non.** Les expressions `between-group`, `within-group`,
`variance decomposition` n'apparaissent nulle part. Les deux seules occurrences de « between group »
designent une difference de **moyennes** entre humains et jumeaux, pas entre segments de population.
[CONFIRME par recherche exhaustive ; corps pages 7 et 16]

Le rapport d'ecarts types est calcule **par resultat, sur la population appariee entiere**. Il
melange donc, dans un seul nombre, ce que nous separons en terme inter et terme intra. C'est la
raison pour laquelle notre chiffre et le leur ne sont pas la meme quantite, et la raison pour
laquelle notre decomposition reste disponible.

**Il y a une exception, et il faut la connaitre avant de rediger.** La sous etude 7, « Fees
Accuracy », publie les deux moities sur le meme materiau :

- Le terme intra : « Humans expressed significantly more variation in their fairness ratings than
  did their digital twins, based on a Levene's test (**F(1, 798) = 180,48, p < 0,001**). »
  [CONFIRME, SI section J.7, page 141]
- Le terme inter : regression du soutien a la regulation sur l'ideologie centree (1 = very liberal
  a 5 = very conservative), la source (humain ou IA) et leur interaction. Effet principal de
  l'ideologie **b = -0,44, SE = 0,06, t(796) = -7,78, p < 0,001** ; effet principal de la source
  **b = 0,44, SE = 0,09, t(796) = 4,69, p < 0,001** ; et l'interaction **b = -0,53, SE = 0,08,
  t(796) = -6,67, p < 0,001**, « demonstrating that the ideology effect was stronger for the digital
  twins than their human counterparts ». [CONFIRME, SI section J.7, page 142, figure 35]
- Leur commentaire : « digital twins exhibited **exaggerated ideological consistency** with a
  stronger negative association between conservatism and regulation support than human
  participants. This likely reflects LLM's reliance on dominant associations in their training
  data (e.g., conservatism = free-market values), whereas human responses may incorporate more
  contextual nuance. » [CONFIRME, SI section J.7.4, page 143]

**C'est la double distorsion, sur un seul jeu d'items, publiee.** Il faut la citer et dire
precisement ce qui manque : c'est une **pente** sur une echelle d'ideologie et non un rapport
d'ecart entre camps ; c'est **une** sous etude sur dix neuf ; il n'y a **aucun item temoin apparie** ;
il n'y a **aucun plancher** ; et les deux moities ne sont jamais mises dans le meme tableau ni
reliees par une identite. Notre tableau a quatre cases reste non fait par eux.
[PROBABLE pour « reste non fait », fonde sur la recherche exhaustive des mots de variance dans les
7 004 lignes]

Trois autres sous etudes comparent des variances, toujours en interne et jamais par segment :
sous etude 14 sur les violations de vie privee, « F-test on variances » ; sous etude 15 avec un
tableau complet de tests F ; sous etude 19. [CONFIRME, SI pages 189, 195 et 196]

### 3.2 Un plancher test retest ? Non, et le materiel etait dans leurs mains

**Non.** Les dix neuf sous etudes ont ete passees **une fois** par les humains, entre avril et juin
2025. Aucune reinterrogation, aucun plancher de bruit, aucune exactitude relative calculee sur leurs
propres donnees. [CONFIRME, Materials and Methods page 27, et absence complete du calcul]

Ils **connaissent** pourtant la mesure et la citent chez les autres, deux fois : Park et al.,
« relative accuracy of 85% on the General Social Survey, based on the ratio of digital twin accuracy
to test-retest accuracy », et Twin-2K-500, « average accuracy of 72%, relative accuracy of 88%
based on the ratio of digital twin accuracy to test-retest accuracy ».
[CONFIRME, corps pages 3 et 4]

Et la vague 4 de Twin-2K-500, qui est la vague de reinterrogation, est **consommee comme entree de
persona** (section 1.1 ci dessus). Le plancher etait disponible, il a servi a autre chose.

**Ce point est desormais le plus net de tout le dossier popsim.** Les deux equipes qui ont mesure
la meme chose que nous sur les memes donnees n'ont pas de reference de bruit. Nos 0,4 pour cent sur
le GSS et notre intervalle (1,004 ; 1,009) sur Twin sont, a ma connaissance apres cette lecture,
sans equivalent publie.

### 3.3 Une baseline non LLM ? Oui, deux, et c'est a integrer

Oui : tirage uniforme et XGBoost par resultat. Voir section 1.4. **Notre ligne de FAITS-ETABLIS
section 3, « Aucun correctif evalue contre une baseline non LLM », reste vraie mais doit etre
reecrite** : ce qui n'existe toujours pas, c'est un **correctif du defaut de variance** evalue
contre une baseline d'imputation. Peng et al. posent une baseline non LLM pour la **performance**
des jumeaux, pas pour un correctif, et ils ne proposent aucun correctif dans l'article.

Detail a retenir pour D.5 : leur XGBoost est entraine **avec des reponses humaines reelles sur le
resultat vise**, donc ce n'est pas une methode de simulation, c'est une methode de prediction
supervisee qui coute des humains. C'est exactement la distinction que la lecture 02 pose entre
imputation et simulation, et ils ne la posent pas.

### 3.4 Le rappel des reponses rares, et qui recoit la rarete ? Rien dans l'article

**Rien.** Les mots `minority`, `rarity`, `modal`, `unanimous`, `entropy` sont absents ; `rare`
n'apparait que dans deux titres de faux articles de presse d'une sous etude ; `tail` n'apparait que
dans `detailed` et `tailored`. [CONFIRME par recherche exhaustive des 7 004 lignes]

Aucune mesure de rappel sur les reponses minoritaires, aucune analyse de **qui** recoit une reponse
rare, aucun appariement personne contre segment, aucun temoin aveugle. La question centrale de a29
et de a31 n'est pas posee.

**Mais leurs sorties publiees contiennent une mesure de queue qu'ils n'ont jamais rapportee.** Voir
section 6.2 ci dessous : c'est le resultat le plus important de cette lecture pour l'option A de
`ARBITRAGE.md`.

### 3.5 L'unanimite d'un camp ? Jamais mesuree, mais constatee deux fois en passant

**Jamais mesuree.** Deux traces indirectes, toutes deux precieuses parce qu'elles montrent que le
phenomene s'est presente a eux sans qu'ils le comptent :

1. **Note 9, page 11** : « We set correlation to 0 for cases where **there is no variation among
   twin answers**, which may occur with the "empty persona" or "demographics only" benchmarks. »
   [CONFIRME] Ils rencontrent donc la degenerescence complete, la traitent comme un cas de bord
   dans le calcul, et **ne publient nulle part le nombre de fois ou elle se produit**. C'est le
   chiffre exact que a30 publie chez nous, Gini Simpson a 0,000 sur onze items de libertes civiles
   et cinq items de fin de vie pour les 63 agents de gauche de C2.

2. **Sous etude 15, page 198** : « **nearly 100% of twins report that their father completed high
   school (12 years of education)**, whereas the human sample shows a much more diverse educational
   distribution. » [CONFIRME, SI section J.15.4] C'est un effondrement sur la modalite modale, decrit
   en une phrase, sans mesure et sans nom.

3. Il y a aussi, chez eux, la trace du meme mecanisme sur une autre quantite : « The opposite
   pattern was present for digital twins (b = 0,06, SE = 0,03; t(1998) = 2,36; p = 0,018),
   **consistent with regression to the mean** », sur l'extremite d'attitude en sous etude 13.
   [CONFIRME, SI section J.13.4, page 185]

---

## 4. Le « overly shrunk » : leur explication, et leur correctif

### 4.1 L'explication

Elle est bayesienne et elle tient en un paragraphe : « Adopting a Bayesian framework, one may think
of the base LLM as reflecting a **prior distribution** over how an individual may respond to a
particular question. The additional information fed to the LLM to build that person's digital twin
leads to an updated, **posterior distribution** of answers tailored to that individual. »
[CONFIRME, corps page 13, ouverture de la distorsion 1]

Et le diagnostic : « while the additional data is able to steer the distribution in an appropriate
direction (i.e., the variations across digital twins better mirror the variations across people),
**the base model (i.e., the prior) still carries significant weight and influence** on the digital
twins' responses. In other words, the answers are overly "shrunk" towards a base model. »
[CONFIRME, corps page 14]

C'est bien le vocabulaire du retrecissement, mais **sans aucun renvoi a la statistique**. Ni Little
et Rubin, ni van Buuren, ni Meng, ni Robinson, ni Freedman ne sont cites. Le point 5 de la
section E.4 de la lecture 02 est donc confirme : la place est vide.
[CONFIRME, liste de references pages 30 a 37 lue en entier]

Leur attribution des cinq distorsions au socle est presentee par eux comme une speculation, et il
faut le citer si on veut s'en servir : « **One may speculate, and test in future research**, that
several of the distortions we observe are due to properties of the base LLM being transferred to
digital twins. » [CONFIRME, corps page 25] C'est un [HYPOTHESE] de leur part, pas un resultat.

### 4.2 Le correctif : aucun dans l'article, un dans le depot

**Dans l'article, il n'y a pas de correctif.** Il y a cinq « benchmarks for progress », c'est a dire
cinq diagnostics. Celui de la distorsion 1, mot pour mot : « comparing standard deviation of twin
responses to human responses. If full-persona twins approximate the standard deviation of human
responses, this suggests that twins have overcome the homogenization that plagues LLMs. »
[CONFIRME, corps page 14] Celui de la distorsion 2 : « comparing responses of full-persona twins
to those of (1) demographic personas, (2) empty personas, and (3) humans. If full-persona twins are
closer to demographic personas than humans, that suggests an over-reliance on demographics at the
expense of true individuation. » [CONFIRME, corps pages 16 et 17]

Ce second critere est, terme pour terme, le test D.1 que la lecture 02 nous proposait. Il est
formule par eux comme un critere d'evaluation, ce qui nous **oblige** a le rejouer chez nous si nous
voulons etre comparables.

**Dans le depot public, il y a un correctif, et il n'est pas dans l'article.** Le repertoire
`post_metric_calculation/post_processing_caliberation/` contient un pipeline de calibration :
separation aleatoire des 160 et quelques colonnes en 80 d'entrainement et 80 et quelques de test,
completion de matrice par SVD tronquee de **rang 5** sur l'empilement des reponses humaines et des
reponses de jumeaux sur les colonnes d'entrainement, puis regression lineaire par colonne de test.
[CONFIRME, `post_processing_caliberation/README.md`]

Ses resultats declares, sur 83 colonnes de test, lus dans
`calibration_metrics_by_specification.csv` :

| quantite | original | calibre |
|---|---|---|
| correlation moyenne | 0,2335 | **0,3984** |
| exactitude courante | 0,7352 | 0,7518 |
| exactitude standardisee | 0,7258 | 0,7564 |
| **rapport d'ecarts types** | **0,6692** | **0,7240** |
| distance de Wasserstein | 0,1467 | 0,1485 |
| d de Cohen | 0,4999 | 0,4051 |

[CONFIRME, fichier public du depot, 83 colonnes]

**Trois choses a en dire, et elles comptent pour notre positionnement.**

1. **Le correctif exige des reponses humaines reelles sur 80 colonnes.** Ce n'est donc pas une
   methode de simulation, c'est une recalibration supervisee. Elle ne repond pas a la question a
   laquelle un jumeau numerique est cense repondre, qui est de se passer d'humains.
2. **Il ne repare pas la sous dispersion**, il la deplace de 0,669 a 0,724, soit 8 points sur les
   33 manquants. La correlation, elle, monte de 71 pour cent en relatif. C'est exactement le profil
   de notre a7 et a20 : on gagne sur la structure, on ne comble pas le total.
3. **Il n'est pas dans l'article**, et son README porte des formules du type « BREAKTHROUGH
   PERFORMANCE » et « Our calibration method BEATS ALL existing mega study specifications ». Ce sont
   des affirmations de depot, non relues. **Ne pas les citer comme un resultat publie.**
   [CONFIRME pour l'existence et les valeurs, `README.md` et CSV du depot ; le caractere non publie
   est une deduction de l'absence du mot `calibration` dans le PDF, verifiee]

---

## 5. Leur position sur l'etiquette comme cause : ils ne la testent pas

Voici l'etat exact de la question chez eux.

**Ce qu'ils affirment.** « This provides initial evidence that, when predicting an individual's
response, digital twins may mostly rely on **stereotypical demographic-based tendencies** rather
than modeling an individual's distinct cognition. » [CONFIRME, corps page 9] Et : « This suggests
that digital twins **rely heavily on demographic characteristics** rather than the wealth of
additional individual-level information they were provided. » [CONFIRME, corps page 15]

**Ce sur quoi ils l'appuient.** Une distance, MAD full contre demographics = 0,132, plus petite que
MAD full contre empty = 0,175 et que MAD full contre humains = 0,252. Et une non difference
d'exactitude, 0,748 contre 0,746, p = 0,37.

**Ce qu'ils ne font pas, et c'est central.**

1. **Aucune ablation de l'etiquette.** La comparaison va de « persona complete » a « demographies
   seules », c'est a dire qu'elle **retire l'information individuelle en gardant l'etiquette**.
   Il n'existe aucune condition symetrique, qui **retirerait l'etiquette en gardant l'information
   individuelle**. Or c'est celle la, et elle seule, qui separe un effet de l'etiquette d'un effet
   d'un manque d'information.
2. **Aucune variation de l'invite.** Un unique gabarit, une unique fente `{Persona Profile}`. Les
   mots `ablation` et `prompt variation` sont absents du papier ; les deux seules occurrences de
   `robustness` sont une reference bibliographique et un controle statistique sans rapport.
   [CONFIRME par recherche exhaustive ; gabarit complet en SI section B.1, page 55]
3. **L'ideologie et le parti sont classes parmi les 14 variables demographiques**, sans un mot sur
   le fait que ce sont des attitudes declarees et non des attributs. [CONFIRME, corps page 9]

**Conclusion pour nous.** Leur these est une these de **proximite** : le jumeau ressemble a
l'agent a etiquette. La notre est une these de **causalite** : c'est l'etiquette qui produit la
substitution, mesuree a modele, personnes, questions et traces constants. Ces deux theses ne sont
pas la meme, et la seconde n'a pas ete faite.

---

## 6. Code et sorties publics, et quatre choses que le depot dit et que l'article tait

### 6.1 L'etat du public

Donnees : `https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500-Mega-Study`.
Code : `https://github.com/TianyiPeng/Twin-2K-500-Mega-Study`.
Preenregistrements : `https://researchbox.org/4145` pour les dix neuf sous etudes,
`https://aspredicted.org/65ty-73sp.pdf` pour l'enquete d'experts.
[CONFIRME, corps page 6, note 13, et section Data and materials availability page 38]

Depot : licence **Apache-2.0**, dernier envoi le **9 juin 2026**, 18 etoiles, environ 152 Mo.
Arborescence de premier niveau : `configs`, `docs`, `evaluation`, `fine_tuning`,
`mega_study_evaluation`, `ml_prediction`, `post_metric_calculation`, `prediction_comparison`,
`processing_qualtrics_csv`, `processing_qualtrics_qsf`, `relevance_analysis`, `results`, `scripts`,
plus un `Snakefile` et un `Makefile`. Le repertoire `results` contient un sous repertoire par sous
etude, dix neuf en tout. [CONFIRME, API GitHub]

### 6.2 Le point F.1 de la lecture 02 est leve : les valeurs du rapport d'ecarts types sont publiques

La lecture 02 ecrivait, en tete de sa section F : « Les valeurs numeriques du ratio d'ecarts types
de Peng et al. Le texte donne le compte, 154 sur 164 et 140 significatifs, mais les valeurs du
ratio sont dans les figures 2, 10 et 16, qui sont des images. » **C'est vrai de l'article et faux du
depot.**

Le fichier `post_metric_calculation/joint_vector_metrics.csv`, 906 592 octets, porte les colonnes
`study_name, specification_name, specification_type, variable_name, correlation, current_accuracy,
accuracy_bottom_5, accuracy_top_5, accuracy_mid_90, std_ratio, Glass_delta, n_points, human_std`,
soit **un rapport d'ecarts types par resultat et par specification**.
[CONFIRME, en tete du fichier public]

Et le fichier `post_metric_calculation/average_metrics_by_specification.csv` donne la moyenne par
specification. Extrait, colonne `std_ratio_mean`, sur 163 resultats sauf mention :

| specification | `std_ratio_mean` | `correlation_mean` | `current_accuracy_mean` |
|---|---|---|---|
| `random_benchmark` | **1,139** | 0,0006 | 0,629 |
| `full_persona_fine_tuned_temperature_7` | **1,061** (152 res.) | 0,140 | 0,704 |
| `full_persona_fine_tuned_temperature_0` | 0,897 (165 res.) | 0,195 | 0,691 |
| `llama_persona_summary` | 0,924 (162 res.) | 0,074 | 0,624 |
| `deepseek` | 0,734 | 0,200 | 0,744 |
| `gemini` | 0,685 | 0,206 | 0,740 |
| `centaur_persona_summary` | 0,666 (162 res.) | 0,076 | 0,674 |
| **`full_persona_without_reasoning`** | **0,634** | **0,197** | **0,748** |
| `persona_summary` | 0,623 | 0,205 | 0,751 |
| `temperature_zero` (persona complete, T = 0) | 0,615 | **0,232** | 0,752 |
| **`demographics_only`** | **0,575** | **0,145** | **0,746** |
| `demographics_only_temperature_zero` | 0,557 | 0,147 | 0,749 |
| **`empty_persona`** | **0,446** | **0,080** | **0,734** |
| `empty_persona_temperature_zero` | **0,377** | 0,048 | 0,736 |

[CONFIRME, fichier public du depot, valeurs lues telles quelles, aucun calcul de ma part]

**Trois lectures, et la premiere est un cadeau pour nous.**

1. **La dispersion croit de facon monotone avec l'information individuelle** : persona vide 0,446,
   etiquette demographique 0,575, persona complete 0,634. L'ecart entre l'etiquette seule et la
   persona complete vaut **6 points de rapport**, alors que l'ecart d'exactitude vaut 0,2 point.
   C'est **la meme dissociation qu'ils publient sur la correlation, transposee a la dispersion**,
   et ils ne la commentent nulle part.
2. **Le tirage aleatoire est au dessus de 1**, a 1,139, exactement comme notre temoin B0 : un
   predicteur aveugle ne retrecit rien. La mesure est donc valide au meme titre que la notre.
3. **L'ajustement fin a temperature 0,7 sur dispersion au dessus de 1**, a 1,061, en payant
   4 points d'exactitude. Il existe donc, chez eux, une configuration qui **sur disperse**. La
   phrase « les modeles de langage ecrasent la variance » est fausse en general et vraie pour les
   conditions d'invite. Cela renforce la conclusion B.1 de la lecture 02 : la these ne peut pas
   etre l'ecrasement en soi.

Nos chiffres sont maintenant comparables **en signe, en frequence et en ordre de grandeur**, mais
toujours pas en valeur, parce que leur rapport est un rapport **total** et le notre un rapport
**intra**. Notre ligne de FAITS-ETABLIS section 1, « treize configurations sur treize du jeu
Twin-2K-500 tombent dans le meme quadrant, dispersion interne 0,45 a 0,75 », et leur intervalle de
0,377 a 0,734 pour les conditions d'invite, se recouvrent, ce qui est rassurant mais ne prouve rien
puisque les quantites different.

### 6.3 Une mesure de queue existe dans leurs sorties, et n'est nulle part dans l'article

Le fichier `compute_vector_metrics.py` definit, en plus des quatre mesures du papier, trois
exactitudes par tranche : on trie les participants par leur **valeur humaine** sur ce resultat, on
prend les **5 pour cent du bas**, les **5 pour cent du haut** et les **90 pour cent du milieu**, et
on calcule l'exactitude individuelle sur chaque tranche.
[CONFIRME, `compute_vector_metrics.py`, lignes 220 a 263]

Les valeurs moyennes, lues dans `average_metrics_by_specification.csv` :

| specification | `accuracy_mid_90` | `accuracy_bottom_5` | `accuracy_top_5` |
|---|---|---|---|
| `full_persona_without_reasoning` | 0,7643 | **0,5416** | 0,6623 |
| `demographics_only` | **0,7644** | **0,5165** | 0,6475 |
| `empty_persona` | 0,7530 | **0,4644** | 0,6504 |
| `random_benchmark` | 0,6401 | **0,5325** | 0,5221 |

[CONFIRME, fichier public du depot]

**C'est le resultat le plus utile de toute la lecture pour l'option A de `ARBITRAGE.md`.** Lu
ligne a ligne :

- **Sur les 90 pour cent du milieu, l'etiquette demographique seule fait aussi bien que 500 reponses
  reelles de la personne** : 0,7644 contre 0,7643. La difference est nulle au quatrieme chiffre.
- **Sur les 5 pour cent du bas, c'est a dire sur les gens qui repondent a l'extremite de
  l'echelle, l'ecart apparait** : 0,5416 pour la persona complete contre 0,5165 pour l'etiquette
  seule, et 0,4644 pour la persona vide.
- **Et le tirage uniforme, a 0,5325, fait mieux que l'agent a etiquette sur cette tranche**, et
  mieux que la persona vide, alors qu'il est battu de plus de 12 points sur le milieu.

Autrement dit : toute la valeur ajoutee de l'information individuelle est dans les queues, tout
l'ecart entre l'etiquette et le hasard s'inverse dans les queues, et **rien de tout cela n'est dans
l'article**. Les mots `bottom_5`, `top_5` et `mid_90` n'apparaissent dans aucune des 7 004 lignes du
PDF. [CONFIRME par recherche exhaustive]

C'est notre these de a29 et a31, sur leurs donnees, dans leur code, non publiee. **A rejouer chez
nous, et a citer comme convergence externe.**

### 6.4 Un correctif non publie

Voir section 4.2.

---

## 7. Ce que popsim peut encore revendiquer, ligne par ligne

### 7.1 Contre `ARBITRAGE.md`

| enonce d'`ARBITRAGE.md` | etat apres cette lecture |
|---|---|
| « Toute methode qui predit des reponses efface les gens rares » | **Intact et renforce.** Ils ne mesurent pas les rares dans l'article ; leurs propres sorties le mesurent par tranche et donnent le meme sens, et un hasard qui bat l'etiquette sur les 5 pour cent du bas. |
| « La statistique les efface presque tous, l'IA en garde la moitie » | **Intact.** Aucun equivalent : leur XGBoost est evalue en correlation et en exactitude, jamais en rappel de reponses rares. |
| « Elle sait a qui elles appartiennent aux trois quarts » | **Intact.** Aucune mesure d'attribution de la rarete chez eux. |
| « Elle leur prete souvent la mauvaise rarete » | **Intact.** Absent. |
| « L'etiquette demographique aggrave cela » | **Intact, et c'est notre revendication la plus forte.** Ils affirment la dependance a la demographie sans jamais l'ablater. |
| « La simulation pousse le camp le moins varie a l'unanimite » (a30) | **Intact.** Jamais mesure. Deux constats en passant, note 9 page 11 et sous etude 15 page 198, montrent qu'ils ont croise le phenomene sans le compter. |
| « Les fausses raretes sont les raretes typiques du segment, rapport 4,45 avec etiquette contre 0,44 sans » (a31) | **Intact.** Aucun equivalent, ni comme mesure ni comme idee. |
| « Le manque de contexte n'y est pour rien » (a33) | **Intact, mais a nuancer.** Leur comparaison a XGBoost dit que la matiere individuelle a un plafond intrinseque bas, correlation sous 0,29 a 650 personnes d'entrainement. Ce n'est pas notre a33, mais cela va dans le meme sens et il faut le citer. |
| « Nous sommes les premiers a mesurer les deux distorsions » | **Deja tombe le 8 septembre, et confirme ici.** La sous etude 7 publie les deux moities sur un jeu d'items, Levene et interaction d'ideologie. |
| Option A comme these | **Confortee.** Rien dans ce papier ne l'occupe, et leurs sorties non publiees la corroborent. |
| Option B comme chapitre de methode | **Confortee et rendue plus urgente.** Leur critere « comparing responses of full-persona twins to those of demographic personas, empty personas, and humans » devient le standard de fait ; il faut le rejouer chez nous ou etre hors norme. |
| Question ouverte « socle ou aligne » | **Toujours ouverte, et non eclairee par eux.** Centaur, qui est un Llama-3.1-70B ajuste sur 10 millions de choix humains, fait moins bien que GPT-4.1 en exactitude, 0,674 contre 0,751 en persona summary. Cela ne separe pas socle et alignement. |

### 7.2 Contre `FAITS-ETABLIS.md` section 1

| ligne | etat |
|---|---|
| Double distorsion sur 4 des 6 conditions de Stanford, gonflement 1,8 a 5,9, intra 0,64 a 0,89 | **Intacte.** Aucun terme inter chez eux hors sous etude 7. |
| 13 configurations sur 13 de Twin, gonflement 1,57 a 3,73, intra 0,45 a 0,75 | **Intacte, mais a reecrire avec leur chiffre en face.** Leur `std_ratio` total va de 0,377 a 0,734 sur les conditions d'invite. Deux quantites differentes, il faut le dire dans la phrase meme. |
| Le defaut apparait aussi hors GSS, jeux economiques et Big Five | **Intacte.** |
| Plancher de reinterrogation, 0,4 pour cent sur le GSS, (1,004 ; 1,009) sur Twin | **Intacte, et c'est le differentiateur numero un.** Ils n'ont pas de plancher et le materiel etait dans leurs mains. |
| Sur Twin les trois mesures de dispersion ne s'accordent plus, ordinal 0,06 a 0,22 | **Intacte.** Ils n'emploient qu'une seule mesure de dispersion, l'ecart type de la reponse codee. Ils ne peuvent donc pas voir ce desaccord. |
| L'axe qui porte l'effet est l'ideologie | **Intacte et corroboree.** Correlation plus basse dans le domaine politique, 12 resultats ; et « exaggerated ideological consistency » en sous etude 7. |
| La cause est l'etiquette ideologique, facteur 25 entre deux generations d'agents | **Intacte, et sans concurrent.** Aucune ablation chez eux. |
| Preuve de recopie, 20,0 et 16,5 pour cent contre 96,1 et 99,4 | **Intacte.** Rien de comparable. |
| Facteurs 6,9 GSS, 22,8 jeux, 5,7 Big Five | **Intacte.** |
| L'ideologie n'est pas une donnee demographique | **Intacte, et desormais adressee.** Peng et al. rangent « political party » et « political ideology » parmi les 14 « demographic variables », page 9. C'est la cible a nommer. |

### 7.3 Contre `FAITS-ETABLIS.md` section 4

Aucune ligne de la section 4 n'est touchee : Peng et al. ne travaillent pas sur le GSS, n'utilisent
aucun modele ouvert de petite taille en persona complete, et ne posent jamais la question de
l'exactitude contre la reponse majoritaire.

Deux lignes gagnent un element de contexte externe :

- « Nos deux agents sont battus sur les deux axes a la fois par une simple regression logistique. »
  Peng et al. montrent le meme genre de defaite sur un autre terrain : leurs jumeaux GPT-4.1 valent
  un XGBoost entraine sur **environ 75 humains** en exactitude, et sur **environ 180** en
  correlation. [CONFIRME, corps pages 24 et 25] Nous ne sommes donc pas en train de mesurer une
  pathologie de notre modele de 4 milliards de parametres, nous mesurons un regime.
- L'ouverte « l'absence de gonflement sans etiquette est soit un resultat majeur, soit une
  incapacite d'un modele de 4 milliards ». **Rien chez eux ne la tranche**, puisqu'ils n'ablatent
  jamais l'etiquette, a aucune taille de modele. Leur eventail va de Llama-3.1-70B a GPT-5, et
  aucune de ces conditions ne fait varier l'etiquette.

### 7.4 Les trois choses qui doivent changer dans nos textes

1. **`FAITS-ETABLIS.md` section 3, ligne sur la baseline non LLM.** Reecrire : « aucun **correctif**
   du defaut de variance n'est evalue contre une baseline d'imputation », parce que Peng et al.
   posent bien une baseline non LLM, XGBoost par resultat, pour la performance.
2. **`corpus/lecture-complete/02-...` section F point 1.** Le lever : les valeurs du rapport
   d'ecarts types sont publiques, par resultat et par specification, dans le depot.
3. **Toute phrase qui dit « les jumeaux sont sous disperses » sans condition.** Faux en general :
   `random_benchmark` a 1,139 et le GPT-4.1 ajuste a temperature 0,7 a 1,061.

---

## 8. La phrase de related work, en anglais

Version longue, pour une section de positionnement :

> Peng et al. (2026) show, on Twin-2K-500, that digital twins built from more than 500 real answers
> per person end up closer to demographics-only personas (MAD = 0.132) than to the humans they are
> meant to copy (MAD = 0.252), and that twin answers are "overly shrunk towards a base model", with
> a standard deviation below the human one in 154 of 164 outcomes. They report one standard
> deviation ratio per outcome, computed over the whole matched sample. They do not decompose it into
> a between-group and a within-group term; they never remove the demographic label while holding the
> model and the individual data fixed, so their stereotyping result is a statement about distance and
> not about cause; and although Twin-2K-500 contains a fourth, test-retest wave, they consume it as
> persona input rather than using it as a human noise floor. We supply the three. We show that the
> shrinkage is concentrated within ideological camps while the gap between camps is inflated, that
> ablating the ideological label at fixed model, persons and questions moves the error regime from
> group-driven to person-driven (group-to-person lift ratio 4.45 with the label versus 0.44 without,
> against 0.56 for the same humans re-interviewed two weeks later), and that those re-interviewed
> humans give a within-camp dispersion ratio of 1.005, which is the noise floor against which any
> shrinkage estimate must be read.

Version courte, pour une introduction :

> The closest precedent, Peng et al. (2026), reports that digital twins are closer to
> demographics-only personas than to their own humans and are "overly shrunk towards a base model".
> It reports a single, undecomposed dispersion ratio, never ablates the demographic label at fixed
> model, and has no human test-retest floor. We add the decomposition, the ablation, and the floor.

---

## 9. Zhang, Xu et Alvero, section resultats, et une erreur a corriger chez nous

Simone Zhang (NYU Sociology), Janet Xu (Stanford GSB), AJ Alvero (**Cornell**, Information Science
et Center for Data Science for Enterprise and Society), « Generative AI Meets Open-Ended Survey
Responses: Research Participant Use of AI and Homogenization », version du 15 mars 2025, mention
« Forthcoming Sociological Methods & Research ». Lu sur `https://osf.io/download/4esdp/`,
1 676 lignes de texte extrait. [CONFIRME, page 1 du preprint]

**Correction a porter dans la lecture 02.** Notre notice L02-13 ecrit « 462, 1 146 et 915 reponses
humaines appariees », et la section B.5 du meme fichier ecrit « des reponses libres humaines (462,
1 146 et 915) ». **C'est faux dans les deux endroits.** Ces trois nombres sont la colonne TV du
tableau 6, c'est a dire la **taille du vocabulaire total** des reponses humaines pour chacune des
trois questions. Les effectifs apparies reels sont : **n = 223 pour JSD, n = 195 pour Graham,
n = 187 pour Groenendyk**. [CONFIRME, section 5, page 25 du preprint, phrase « At the end, we had
matched sets of n = 223 for JSD, n = 195 for Graham, and n = 187 for Groenendyk », et tableau 6
page 25]

**Ce qu'ils mesurent exactement.** Il n'y a **pas** de « 55 items de desirabilite » chez eux : les 55
resultats etiquetes `social desirability` sont ceux de Peng et al. Zhang, Xu et Alvero travaillent
sur **trois questions ouvertes** issues de trois etudes TESS anterieures a ChatGPT, dont deux
portent sur la perception de groupes sociaux : JSD, perception des personnes noires aux Etats Unis ;
Graham, perception des democrates et des republicains ; Groenendyk, interet pour la politique.
[CONFIRME, sections 3 et 5]

Cinq modeles : **GPT-4o mini (temperature 0,7), GPT-4o, Gemini 1.5 (temperature 1), Claude 3.5
Sonnet (temperature 1), Claude 3 Opus**, les trois premiers nommes etant ceux du corps de l'article.
Les invites ne sont pas ecrites par les auteurs : ce sont **les invites reellement redigees par des
repondants Prolific** qui declarent utiliser des assistants. Taux de refus ou de sortie invalide :
**16 pour cent pour Claude 3.5 Sonnet, 14 pour cent pour Gemini 1.5, 1 pour cent pour GPT-4o mini**.
Appariement **exact** avec un repondant TESS sur race, education (licence ou non), affiliation
partisane et age (45 ans et plus ou non), et sur la version exacte de la question vue.
[CONFIRME, section 5, pages 23 a 25]

Les cinq mesures de leur section resultats :

1. **5.1 Longueur et vocabulaire.** Tableau 6, page 25. Humains : 9,7 mots (Groenendyk), 31,7
   (Graham), 16,1 (JSD). Modeles : de 99,0 a 215,8 mots. Les modeles sont plus longs et plus varies
   lexicalement, et **plus variables en longueur**. [CONFIRME]
2. **5.2 Mots distinctifs, TF-IDF.** Figure 5. Les humains emploient un langage « emotionally
   charged and concrete » ; les modeles un langage « neutral, abstract ». Sur JSD, les humains
   disent « oppressed », « discriminated », « hard » ; les modeles « disparities », « systemic »,
   « challenges ». [CONFIRME, section 5.2, pages 27 et 28]
3. **5.3 Sentiment, VADER.** Figure 6. Les modeles sont plus positifs, les humains plus negatifs.
   Sur Groenendyk, les modeles emploient « nearly twice as many positive words as humans (around
   0.18 to 0.19 for the three LLMs vs. 0.10 for humans) » ; sur JSD, les humains emploient plus du
   double de mots negatifs. [CONFIRME, section 5.3, page 29]
4. **5.4 Langage deshumanisant.** Figure 7. Similarite cosinus des plongements GloVe a 100
   dimensions, ponderee par frequence de terme, a deux vecteurs de concept construits selon
   Mendelsohn et al. 2020 : **vermin**, moyenne des vecteurs de mots de vermine ; **moral disgust**,
   moyenne des mots du Moral Foundations Dictionary pour ce concept. Resultat, cite en entier :
   « AI-generated responses from GPT-4o mini, Gemini 1.5, and Claude 3.5 Sonnet **cluster more
   tightly around a lower cosine similarity** to the vermin and moral disgust vectors than do human
   responses. Whereas human responses reflect a wide range of perspectives and language use, AI
   responses tend to be more uniform. » Et la phrase de conclusion : « these findings indicate that
   **LLM-generated answers truncate the range of views of social groups that exist among people,
   particularly those of a more denigrating or negative nature**. » [CONFIRME, section 5.4,
   pages 30 et 31]
5. **5.5 Homogeneite.** Figure 8. Similarite cosinus moyenne **par paires a l'interieur d'une meme
   source**, sur des vecteurs TF-IDF. Pour les trois questions, la similarite moyenne entre reponses
   de modele depasse celle entre reponses humaines, GPT-4o mini etant le plus homogene. Robuste aux
   autres modeles et aux temperatures, figure S6. [CONFIRME, section 5.5, pages 31 et 32]

**Ce qu'il faut retenir pour nous.** Leur mesure de la part effacee est une **similarite a deux
vecteurs de mots**, pas une annotation ni un item ferme. Il n'y a **aucun ratio de variance**,
**aucune decomposition inter et intra**, **aucun item temoin apparie**, **aucun plancher de
reinterrogation**, et **trois questions**. La conclusion de la lecture 02 tient sans changement :
la revendication « personne n'a formule que la part effacee est celle que les gens ne disent pas
ouvertement » est morte, et ce qui reste a popsim est le contraste sensible contre temoin apparie,
decompose en inter et en intra, avec plancher.

---

## Ce que je n'ai pas pu verifier

1. **La version publiee dans Science Advances.** Le doi 10.1126/sciadv.aeh8260 est derriere un 403
   de science.org. Toute la lecture porte sur arXiv v5 du 19 avril 2026. Il est possible que la
   version publiee contienne des chiffres ou des figures absents de la v5, ou l'inverse.
2. **Le coefficient de la desirabilite sociale dans la meta regression.** Il est dans la figure 11,
   une image. Le depot contient `mega_study_evaluation/meta_analysis_results/`, que je n'ai pas
   ouvert. **Ne pas citer d'ampleur avant d'avoir ouvert ce repertoire.**
3. **Les valeurs par resultat du rapport d'ecarts types.** Je n'ai lu que l'en tete et les deux
   premieres lignes de `joint_vector_metrics.csv`, et les moyennes par specification. Je n'ai fait
   aucun calcul sur ce fichier, conformement a la consigne. La distribution complete reste a lire.
4. **Le contenu exact des figures 2, 5, 6, 10, 11, 16, 17, 18, 19, 20 et 35.** Ce sont des images.
   Tous les chiffres que ce rapport tire de ces figures viennent en realite du texte ou des CSV du
   depot, jamais d'une lecture d'image.
5. **Qui a code les 55 resultats « social desirability », et avec quel accord.** Absent du papier,
   et je n'ai pas cherche dans `manual_variable_extraction.json` du depot, qui pourrait contenir la
   table d'etiquetage, 27 972 octets.
6. **Le contenu de `calibration_results.csv`, 83 lignes**, et donc le detail du correctif non
   publie. Je n'ai lu que le README et le fichier de synthese par specification.
7. **Le fichier `relevance_analysis/`**, non ouvert, dont le nom suggere une analyse absente de
   l'article.
8. **Si les vingt trois specifications du CSV correspondent exactement aux conditions decrites dans
   l'article.** Les noms concordent, mais `full_persona_without_reasoning`, `with_reasoning` et
   `include_reasoning_temperature_zero` designent une distinction, la trace de raisonnement, dont
   l'article ne parle pas explicitement dans les pages lues.
9. **Le supplement en ligne de Zhang, Xu et Alvero** (figures S1, S2, S6, tableau S1), qui porte
   les replications sur GPT-4o, Claude 3 Opus et les autres temperatures. Le preprint y renvoie mais
   ne l'inclut pas.
10. **La version Sociological Methods and Research de Zhang, Xu et Alvero**, doi
    10.1177/00491241251327130. La lecture porte sur le preprint SocArXiv date du 15 mars 2025.

---

## Questions ouvertes pour Simon

1. **Rejoue-t-on leur critere de la distorsion 2 chez nous avant de rediger ?** Ils l'ont pose
   comme le standard d'evaluation, mot pour mot : trois distances MAD, persona complete contre
   etiquette, contre vide, contre humains. Nos conditions C2 et C3 sont exactement le materiel
   requis, et cela coute zero appel de modele. Si notre MAD a l'etiquette est plus petite que notre
   MAD a l'humain, nous sommes comparables ligne a ligne a la seule equipe qui l'a publie. Si elle
   est plus grande, nous avons un resultat plus interessant encore, et il faut le savoir avant de
   choisir A, B ou C.

2. **Reproduit-on leurs trois tranches d'exactitude, bas 5, milieu 90, haut 5 ?** C'est leur code,
   c'est notre these, et ils ne l'ont pas publie. Sur leurs propres sorties, l'etiquette seule egale
   500 reponses reelles sur le milieu (0,7644 contre 0,7643) et perd 2,5 points sur les 5 pour cent
   du bas, ou le tirage aleatoire la depasse. Si le meme profil sort de nos donnees GSS, l'option A
   d'`ARBITRAGE.md` a une corroboration externe sur un autre jeu, un autre modele et une autre
   equipe, et la phrase se poste en deux lignes.

3. **Que fait-on du correctif non publie qui dort dans leur depot ?** Il monte la correlation de
   0,2335 a 0,3984 et le rapport de dispersion de 0,669 a 0,724, mais il exige des reponses humaines
   reelles sur 80 colonnes. C'est, terme pour terme, le point que notre a7 et notre a20 etablissent :
   on gagne sur la structure, on ne comble pas le total, et le prix est des humains. Faut-il en faire
   un paragraphe du chapitre de methode, ou le laisser de cote parce qu'il n'est pas publie ?

4. **Nomme-t-on leur classement de l'ideologie parmi les variables demographiques ?** Ils ecrivent
   « 14 demographic variables (... political party ... political ideology ...) ». Notre dossier
   entier repose sur le fait que ce sont des attitudes declarees. Est-ce un point a soulever
   frontalement, ce qui est defendable et un peu frontal, ou une note de bas de page ?

5. **La sous etude 7 change-t-elle notre revendication de la double distorsion ?** Elle publie un
   Levene et une interaction d'ideologie sur le meme jeu d'items, ce qui est plus proche de notre
   tableau a quatre cases que tout ce que le corpus contenait. Je pense que non, parce qu'il n'y a
   ni item temoin, ni plancher, ni mise en relation des deux termes, mais c'est un arbitrage de
   redaction et pas un fait, et il vaut mieux qu'il soit pris avant qu'un relecteur le prenne pour
   nous.

6. **Faut-il ouvrir `meta_analysis_results/` et `manual_variable_extraction.json` ?** Ce sont les
   deux fichiers qui, s'ils contiennent ce que leur nom annonce, donneraient le coefficient exact de
   la desirabilite sociale et la table d'etiquetage des 55 resultats. Cela leverait les points 2 et 5
   de la section precedente et rendrait leur mesure directement reutilisable comme definition
   d'items sensibles pour notre test D.2. C'est une demi heure de lecture, aucun calcul.

---

## Reproduction

```
curl -sL -o peng.pdf https://arxiv.org/pdf/2509.19088v5
pdftotext -layout peng.pdf peng.txt          # 223 pages, 7 004 lignes
curl -sL -o zhang.pdf https://osf.io/download/4esdp/
pdftotext -layout zhang.pdf zhang.txt        # 1 676 lignes
curl -s https://raw.githubusercontent.com/TianyiPeng/Twin-2K-500-Mega-Study/main/post_metric_calculation/average_metrics_by_specification.csv
curl -s https://raw.githubusercontent.com/TianyiPeng/Twin-2K-500-Mega-Study/main/post_metric_calculation/post_processing_caliberation/calibration_metrics_by_specification.csv
```

Les numeros de page cites sont ceux imprimes dans le PDF, pas les numeros de feuille.
