# 03. Paysage concurrentiel : qui vend deja de la simulation de population

Agent 3. Recherche menee le 2 septembre 2026. Toutes les sources sont accessibles publiquement
sauf mention contraire. Conventions de redaction : voir CONTEXTE.md.

---

## 0. Le resultat qui change le cadrage du projet

Avant toute cartographie, un fait qui doit remonter en premier a Simon.

[CONFIRME] Les auteurs du papier de Stanford que le projet veut reproduire ont fonde une
entreprise. Elle s'appelle **Simile**. L'equipe fondatrice comprend **Joon Sung Park** (premier
auteur de "Generative Agents" 2023 et de "Generative Agent Simulations of 1,000 People" 2024),
**Michael Bernstein** et **Percy Liang**, tous trois co-auteurs du papier de reference, plus
Lainie Yallen au commercial.
Sources : https://www.latent.space/p/simile ,
https://www.indexventures.com/perspectives/life-the-universe-and-simile-leading-similes-series-a/

[CONFIRME] Simile a leve 100 millions de dollars en Serie A menee par Index Ventures, annonce
le 12 fevrier 2026, avec Bain Capital Ventures, A*, Hanabi Capital, et en business angels
Fei-Fei Li et Andrej Karpathy. Puis 200 millions de dollars en Serie B a 2 milliards de
valorisation, annonce le 30 juillet 2026, cinq mois apres la Serie A.
Sources : https://techcrunch.com/2026/07/30/synthetic-user-startup-simile-raises-200m-at-2b-valuation-5-months-after-100m-series-a/ ,
https://www.bloomberg.com/news/articles/2026-02-12/ai-startup-nabs-100-million-to-help-firms-predict-human-behavior (Bloomberg, paywall, titre et date verifies via resultats de recherche uniquement)

[CONFIRME] Methode revendiquee par Simile, decrite par Park lui meme : trois familles de
donnees, entretiens qualitatifs longs, donnees comportementales (transactions, activite web),
et donnees de mecanisme causal issues d'essais randomises. Recrutement de populations
representatives avec consentement et incitation, sessions de laboratoire d'environ deux heures
melant entretien et experiences comportementales. Deux types de modeles maintenus, un modele
au niveau population et un modele au niveau individu. Environ 60 salaries, dont pres de 20 pour
cent d'anciens collegues de Microsoft Research. Siege a San Francisco, bureau a New York.
Client cites : CVS, Deloitte, Wealthfront, Gallup.
Source : https://www.latent.space/p/simile

[CONFIRME] Park declare explicitement entrainer les modeles a reproduire l'irrationalite et les
erreurs humaines, et oppose cela aux modeles frontieres optimises pour la rationalite, qu'il
juge mauvais simulateurs sur les populations non generales. Il cite 20 a 60 pour cent de
precision pour ChatGPT et Claude sur des populations de niche, contre les 85 pour cent du
papier de 2024.
Source : https://www.latent.space/p/simile

**Consequence directe pour popsim.** L'atout declare "acces possible aux auteurs de Stanford"
n'est pas un atout, c'est la description du concurrent le mieux finance du marche. Les auteurs
ne sont plus des academiques disponibles pour une collaboration, ils sont dirigeants d'une
societe a 2 milliards de valorisation en concurrence frontale avec le projet. Voir section 6.

---

## 1. Les deux segments, definis avant de trier

Le porteur du projet affirme n'avoir vu qu'une seule societe qui vende de la simulation de
population au sens scientifique. **Cette intuition etait juste au moment ou elle a ete formee,
elle ne l'est plus.** [PROBABLE, fonde sur la chronologie des levees : Aaru Serie A decembre
2025, Simile Serie A fevrier 2026, Electric Twin Serie A fevrier 2026, Simile Serie B juillet
2026. Le segment A s'est constitue en une dizaine de mois.]

Criteres retenus pour trancher, plus stricts que la communication des acteurs.

**Segment A, simulation de population avec pretention scientifique.** Trois conditions cumulees :
1. les agents sont calibres sur des donnees d'individus reels identifies, pas sur une
   description demographique generique ;
2. l'acteur publie ou fait publier une validation quantifiee contre une enquete reelle, avec
   une metrique nommee ;
3. la methode est descriptible autrement que par un argument commercial.

**Segment A moins, pretention scientifique revendiquee mais preuve non inspectable.** Les
acteurs qui affirment calibrer sur des donnees reelles et qui annoncent des chiffres de
fidelite, mais dont la methodologie et le protocole de validation ne sont pas publies. C'est
la categorie la plus peuplee, et il est methodologiquement malhonnete de la fondre dans le
segment A.

**Segment B, personas synthetiques marketing.** Personas generes a partir de descriptions,
de briefs ou de documents clients, sans calibration sur des individus reels identifies et
sans validation publiee contre une population reelle. Vendus comme outil creatif, de pre test
ou d'acceleration qualitative.

**Segment C, hors sujet mais souvent confondu.** Entretiens conduits par IA aupres d'humains
reels, et augmentation statistique d'echantillons humains reels. Aucune population simulee.
Ces acteurs sont les mieux finances du secteur en nombre, ils polluent toutes les recherches
sur "AI market research", et il faut les ecarter explicitement.

---

## 2. Tableau de mapping

Legende de la colonne Segment : A, A moins, B, C. Legende du niveau de confiance : le
classement porte sur la preuve trouvee, pas sur la qualite reelle du produit.

| Acteur | Segment | Offre exacte | Methode revendiquee | Validation publique | Pricing | Clients cites | Financement | Equipe | Publication |
|---|---|---|---|---|---|---|---|---|---|
| **Simile** (US, SF) | **A** | Jumeaux numeriques d'individus reels, modeles population et individu, requetables | Entretiens longs + donnees comportementales + RCT de mecanisme causal, sessions labo 2 h | Papier arXiv 2411.10109, 1052 participants, 85 pour cent du test retest humain sur le GSS | Non public. Contrats "a plusieurs centaines de milliers voire millions de dollars" evoques en interview, chiffre non confirme par la societe | CVS, Deloitte, Wealthfront, Gallup | 100 M USD Serie A (Index, fev. 2026) + 200 M USD Serie B a 2 Md USD (juil. 2026) | ~60 personnes | Oui, arXiv 2411.10109 et Generative Agents 2023 |
| **Aaru** (US) | **A moins** | Simulation de populations pour prediction electorale et etudes marche | Agents entraines sur des donnees comportementales et de resultats reels plutot que sur des declarations, exploitation de l'ecart intention comportement | Une etude de cas EY, correlation mediane 0,90 sur six mois de recherche wealth ; primaire de New York a moins de 2000 voix, une autre source dit 371 voix. Aucun protocole publie | Non public | EY, Accenture, Interpublic Group, Breakwater, campagnes politiques | Serie A menee par Redpoint, ~88 M USD, valorisation affichee 1 Md USD, dec. 2025, structure multi tranches donc valorisation melangee inferieure | Non trouve | Aucune publication scientifique trouvee |
| **Electric Twin** (UK) | **A moins** | Plateforme d'audiences synthetiques | IA, apprentissage automatique et sciences sociales, simulation d'audiences reelles | Revendique 95 pour cent de precision sur 155 pays et "10 000x plus rapide". Aucun protocole publie trouve | Non public | Non trouve | 24 M USD au total, dont Serie A de 10 M USD en fev. 2026 | Non trouve. Fondee 2023 par Alex Cooper et Ben Warner | Aucune trouvee |
| **Subconscious AI** (US) | **A moins** | Experiences causales sur repondants synthetiques | Population synthetique "fondee sur 800 M de repondants humains", jumeau entraine sur 3,5 M d'individus reels, conjoint et economie comportementale | Revendique 93 pour cent de precision humaine et validation contre plus de 1000 experiences comportementales. Page "Evidence" existe, protocole non verifie par moi | Revendique 10 USD par experience contre 20 000 a 120 000 USD, chiffre issu du marketing de la societe, non verifie | Non trouve | Non trouve. Passe par Transform Cohort 2, Polsky Center, Univ. de Chicago | Non trouve | Fondateur Avi Yashchin. Aucun papier revu par les pairs trouve |
| **Ipsos** (FR) | **A en construction** | Digital Twins adosses au KnowledgePanel | Base de verite terrain construite sur le KnowledgePanel, validation conjointe | Partenariat academique annonce en aout 2025 avec le Polarization and Social Change Lab de Stanford, objectif explicite de valider et d'identifier les limites | Non public | Non applicable, institut | Societe cotee | Non applicable | Programme de recherche annonce, resultats non encore publies a ma connaissance |
| **Qualtrics** (US) | **A moins, mais le mieux documente du lot** | Edge Audiences, panels synthetiques integres a la plateforme | Modele affine sur des millions de reponses humaines reelles agregees, validation en quatre etapes (generalisation, forme des donnees, diversite, transferabilite) | Etude de replication McLean 2026 : ecart de 0,07 ecart type contre 0,87 a 0,88 pour ChatGPT 5 et Gemini, 518 repondants apparies par source, taux d'echec synthetique 2,7 pour cent, taux d'exclusion humain 16,5 pour cent | Non public | Non applicable | Societe cotee puis privatisee | Non applicable | Billet de blog et etude de replication publies, pas de revue par les pairs |
| **Artificial Societies** (UK, YC W2025) | **B** | Reseaux d'IA simulant des audiences a fort enjeu, test de posts, emails, publicites | Personas en reseau qui interagissent et s'influencent, contextes predefinis | Aucune validation chiffree publiee trouvee | Non public | Non trouve | 5,35 M USD seed, Point72 Ventures, Kindred, YC, Pioneer Fund | Fondee 2024, James He et Patrick Sharpe, scientifiques du comportement | Aucune trouvee |
| **Synthetic Users** (PT / US / UK) | **B** | Repondants synthetiques pour entretiens, enquetes, tests d'usage | Architecture multi agents, plusieurs LLM coordonnes, RAG sur donnees proprietaires | Aucune validation chiffree independante trouvee. Citee par Gartner comme leader du segment | **Public** : plans a partir de 12 500 USD par an, systeme de jetons, entretien de 2 a 60 USD selon la profondeur | Non trouve | Aucune levee externe identifiee | Fondee 2023, Kwame Ferreira et Hugo Alves | Aucune trouvee |
| **Evidenza** (US) | **B** | Recherche synthetique B2B en 72 h, personas de decideurs, clones de CMO | Copies IA des clients, focalisation sur les populations difficiles a atteindre (CEO, CIO, CFO) | Revendique 88 pour cent de precision moyenne en tests face a face, **auto declare** | Non public. Une estimation tierce circule a 50 000 a 100 000 USD par an, c'est une estimation d'un site de review, pas un prix officiel | BlackRock, Microsoft, JP Morgan, Salesforce, Mars, EY. Partenariat Dentsu juin 2025 | Non trouve | Fonde par Jon Lombardo et Peter Weinberg, ex LinkedIn B2B Institute | Aucune trouvee |
| **Yabble** (NZ) | **B** | Virtual Audiences, repondants synthetiques, upload de donnees proprietaires | Personas nourris de donnees clients | Validation evoquee comme "hautement comparable" aux resultats traditionnels, aucun chiffre public trouve | Non public | Non trouve | Non trouve | Non trouve | Aucune trouvee |
| **Fairgen** (IL) | **C** | FairBoost, amplification de segments sous echantillonnes | Modele apprenant la relation entre groupes enquetes et extrapolant vers les petits segments. **Part d'humains reels** | Contraintes publiees : minimum 300 repondants reels, segment a booster inferieur a 15 pour cent de l'enquete, garantie moyenne de boost x3 validee sur des centaines de tests paralleles. Livre blanc public | Non public | Non trouve | 8 M USD seed, Maverick Ventures Israel, Tal Ventures, IGNIA, Creator Fund | Non trouve | Conseiller scientifique principal Emmanuel Candes, professeur de statistiques a Stanford. Livre blanc, pas de papier revu par les pairs trouve |
| **Zappi** (UK) | **C puis B** | Test de concepts, approche hybride | Repondants synthetiques valides par 50 a 100 reponses humaines reelles | Pas de chiffre public trouve, mais la methode hybride est en soi un dispositif de validation | Non public | Non trouve | Non trouve | Non trouve | Aucune trouvee |
| **Listen Labs** (US) | **C** | Entretiens vocaux IA a grande echelle aupres d'humains reels | Aucune simulation | Sans objet | Non public | Microsoft, Canva, Chubbies | 27 M USD seed + Serie A (Sequoia), puis 69 M USD Serie B (Ribbit) a 500 M USD | Non trouve | Non applicable |
| **Outset** (US, YC S2023) | **C** | Entretiens moderes par IA, texte, voix, video, plus de 40 langues | Aucune simulation | Sans objet | Non public | HubSpot, Glassdoor, Microsoft, WeightWatchers, Nestle, Uber | 17 M USD Serie A puis 30 M USD Serie B, total 51 M USD, Radical Ventures, M12, YC, 8VC | Non trouve | Non applicable |
| **Strella** (US) | **C** | Entretiens clients moderes par IA | Aucune simulation | Sans objet | Non public | Amazon, Chobani | 18 M USD au total, 4 M seed (Decibel) + 14 M Serie A (Bessemer), oct. 2025 | Non trouve | Non applicable |
| **Genway** (UK) | **C** | Entretiens utilisateurs conduits par IA, tests de prototype Figma | Aucune simulation | Sans objet | Non public | Non trouve | Non trouve | Non trouve | Non applicable |
| **Roundtable** (US, YC) | **C, apres pivot** | A demarre sur un outil de "synthetic humans", **a pivote** vers la detection de fraude et de bots dans les enquetes (Proof of Human) | Biometrie comportementale | Sans objet | Non public | Non trouve | 500 K USD, Brickyard et YC, fondee 2023, New York | Non trouve | Non applicable |
| **Versive** (US, YC W2023) | **C** | Etudes moderees par IA avec analyse automatisee | Aucune simulation | Sans objet | Non public | Non trouve | YC | Non trouve | Non applicable |
| **Studio** (US, YC S2026) | **A moins, a surveiller** | Modeles de marche vivants, segments d'audience interconnectes | Explicitement **pas** des jumeaux de repondants d'enquete, mais des modeles construits sur des donnees de comportement de consommation tracables | Revendique plus de 97 pour cent de correspondance avec des KPI reels (chiffre d'affaires, achat). Auto declare | Non public | Non trouve | YC S2026 | Non trouve | Aucune trouvee |
| **LATO** (YC S2026) | **A moins, a surveiller** | Etude de marche de bout en bout avec simulation | Donnees publiques plus entretiens de premiere main, simulation ancree | Aucune trouvee | Non public | Non trouve | YC S2026 | Non trouve | Aucune trouvee |
| **Quantilope** (DE / US) | **B** | Synthetic Insights dans une plateforme d'automatisation d'etudes | Non detaille | Aucune trouvee | Une source tierce annonce 50 000 a 75 000 USD par an en abonnement illimite. Source de review, **non confirmee par l'editeur** | Non trouve | Non trouve | Non trouve | Aucune trouvee |
| **Kantar, NIQ** | **B / prudence affichee** | Offres d'augmentation synthetique | Positionnement explicite d'augmentation bornee, pas de remplacement | Pas de benchmark chiffre public trouve | Non public | Non applicable | Groupes etablis | Non applicable | Aucune trouvee |
| **Bain** | Conseil | Publication de these sur les "synthetic customers" | Sans objet | Sans objet | Non public | Non applicable | Non applicable | Non applicable | Article de these, pas de recherche |
| **Viewpoints AI, Perceptif, Personax, Rally, Panoplai, Brox, Simsurveys** | **B, non documente** | Panels de consommateurs synthetiques, personas | Non detaille publiquement | Aucune trouvee | Non public | Non trouve | Non trouve | Non trouve | Aucune trouvee |
| **McKinsey QuantumBlack** | Non trouve | Aucune offre de repondants synthetiques identifiee dans mes recherches | Sans objet | Sans objet | Sans objet | Sans objet | Sans objet | Sans objet | Sans objet |

### Comptage

- **Segment A strict, un seul acteur : Simile.** C'est le seul qui coche les trois conditions,
  et il les coche parce que le papier de reference du projet est son propre papier.
- **Segment A moins, cinq a six acteurs** : Aaru, Electric Twin, Subconscious AI, Studio, LATO,
  plus Qualtrics qui est de loin le mieux documente du groupe et qui pourrait basculer en A si
  son etude de replication etait soumise a revue par les pairs. Ipsos y entrera si le programme
  Stanford aboutit a une publication.
- **Segment B, une quinzaine d'acteurs identifies**, marche effectivement encombre, faible
  barriere technique, aucune validation.
- **Segment C**, les mieux finances en nombre de tours, sans rapport avec la these du projet.

---

## 3. La validation publiee : y a t il un standard de marche

Question posee : quelqu'un publie t il une validation chiffree de sa fidelite, et un standard
emerge t il pour dire "notre simulation est fidele a X pour cent" ?

### 3.1 Ce qui existe reellement

[CONFIRME] **Le papier de Stanford est le seul etalon academique reconnu du segment.** Park et
al., "Generative Agent Simulations of 1,000 People", arXiv 2411.10109, 15 novembre 2024. 1052
participants recrutes par echantillonnage stratifie representatif des Etats Unis sur l'age, le
genre, la race, la region, l'education et l'ideologie politique. Les agents reproduisent les
reponses au General Social Survey a 85 pour cent de la precision avec laquelle les participants
se reproduisent eux memes deux semaines plus tard. C'est ce chiffre, et sa metrique normalisee
par le test retest, qui sert de reference implicite a tout le marche.
Source : https://arxiv.org/abs/2411.10109

[CONFIRME] **Qualtrics est le seul acteur commercial a avoir publie une replication comparative
inspectable.** Etude McLean 2026, replication d'un protocole Paxton et Yang 2024. Quatre
sources comparees : modele synthetique affine de Qualtrics, ChatGPT 5, Gemini, panel humain.
Ecart moyen de 0,07 ecart type pour le modele affine contre 0,87 a 0,88 pour les LLM
generalistes. Echantillon apparie de 518 repondants par source. Taux d'echec synthetique
2,7 pour cent, taux d'exclusion humain 16,5 pour cent. L'auteur appelle explicitement le
marche a se doter de standards : etudes de validation publiques contre des benchmarks etablis,
taux d'echec et d'hallucination declares, sources d'entrainement explicitees, limites et cas
d'usage inadaptes documentes.
Source : https://www.greenbook.org/insights/data-science/testing-synthetic-data-against-academic-benchmarks-a-replication-study

[CONFIRME] **PyMC Labs publie des chiffres avec la metrique nommee**, jusqu'a 90 pour cent
d'alignement avec des donnees d'enquete humaines et 85 pour cent de similarite
distributionnelle sur des etudes de concept et de prix, et une methode nommee, le Semantic
Similarity Rating, atteignant 90 pour cent de la fiabilite test retest humaine sur l'elasticite
prix.
Source : https://www.pymc-labs.com/blog-posts/synthetic-consumers-a-practical-guide

[CONFIRME] **Fairgen publie ses contraintes d'usage, ce qui est rare et vaut validation
partielle** : minimum 300 repondants reels, segment cible sous 15 pour cent de l'enquete,
garantie de boost x3 en moyenne, validee par comparaison cote a cote d'un boost reel et d'un
boost synthetique. Conseiller scientifique Emmanuel Candes, Stanford.
Source : https://www.fairgen.ai/press-releases/fairgen-raises-8m-for-statistically-accurate-ai-generated-survey-responses

[CONFIRME] **Ipsos a construit un partenariat academique de validation**, annonce en aout 2025,
avec le Polarization and Social Change Lab de Stanford, autour d'une base de verite terrain
adossee au KnowledgePanel, avec pour objectif explicite d'identifier et de reduire les risques
et limites des jumeaux numeriques.
Source : https://www.ipsos.com/en/ipsos-partners-stanford-university-pioneer-future-market-research-synthetic-data

[CONFIRME] **Un cadre normatif existe depuis juin 2025.** Le code ICC/ESOMAR, cinquieme edition,
introduit une definition officielle de la donnee synthetique et d'un persona synthetique, et
impose la transparence : l'acheteur doit etre informe de l'usage de donnees synthetiques, et le
fournisseur doit declarer ses methodes et les seuils minimaux de donnees appliques.
Sources : https://iccwbo.org/news-publications/business-solutions/iccesomar-international-code-market-opinion-social-research-data-analytics/ ,
https://esocorpwebsitestg.blob.core.windows.net/strapi-uploads/uploads/icc_esomar_international_code_on_market_opinion_and_social_research_and_data_analytics_2025_7e74a25b54.pdf

### 3.2 Ce qui n'existe pas

[CONFIRME par constat de recherche] **Il n'existe aucun benchmark public partage, aucun jeu de
test commun, aucune metrique standardisee permettant de comparer deux fournisseurs.** Chaque
acteur annonce un pourcentage calcule sur son propre protocole, avec sa propre metrique, sur sa
propre population. 85 pour cent chez Simile, 88 pour cent chez Evidenza, 90 pour cent de
correlation mediane chez Aaru, 93 pour cent chez Subconscious AI, 95 pour cent chez Electric
Twin, 97 pour cent chez Studio. Ces nombres ne sont pas comparables entre eux, et aucun ne
designe la meme quantite. Le seul qui soit precisement defini est celui de Simile, parce qu'il
est normalise par le test retest humain, ce qui est une convention explicite et publiee.

[CONFIRME] La revue de PyMC Labs constate directement le probleme : absence de metriques
standardisees, revue par les pairs inconstante, dependance forte a des etudes proprietaires
plutot qu'a des benchmarks publies, litterature dispersee entre disciplines.

[PROBABLE] La progression documentee dans cette meme revue est un indicateur a garder : sur
285 comparaisons entre 2022 et 2023, 25 pour cent seulement montraient un alignement fort ;
sur la periode fin 2023 a debut 2025, 50 pour cent montraient une similarite forte, 36 pour
cent partielle, 14 pour cent minimale. La marge de progres restante est reelle mais elle se
referme.

### 3.3 La litterature critique de 2026, qui recadre la contribution visee

C'est le point le plus important de cette section pour l'ambition scientifique du projet.

[CONFIRME] **"When Synthetic Users Fail: A Cross-Domain Benchmark of LLM-Simulated Human Survey
Responses"**, arXiv 2607.26348, depose le 28 juillet 2026, en cours de revue. Benchmark sur le
General Social Survey (vagues 2016 a 2024, 10 questions) et la World Values Survey (vague 7,
63 pays, 16 questions), avec quatre modeles (Claude Haiku 4.5, Claude Sonnet 4.6,
Llama-3.1-8B, Llama-3.3-70B). Resultats : sur le GSS, les LLM egalent ou sont en dessous d'une
simple baseline demographique a 0,589 de precision, le meilleur a moins 0,001 de marge, le pire
9,3 points en dessous. Sur la WVS, tous les modeles sont 11,8 a 21,8 points sous la baseline de
0,388, avec des precisions de 0,170 a 0,277.
**Le point critique** : les auteurs contredisent l'hypothese de l'ecrasement de la variance.
Ils observent une **sur determination demographique**, pas une homogeneisation. Les opinions
politiques expliquent 1,5 pour cent de la variation de la confiance dans les banques chez les
humains, et jusqu'a 67 pour cent chez les modeles. L'indice de stereotypie est systematiquement
positif. Sur 28 a 41 pour cent des items de la WVS, les humains ne montrent aucune difference
notable la ou les modeles fabriquent de grands ecarts. Ils qualifient le phenomene de
**caricature**, pas d'homogeneisation.
Source : https://arxiv.org/html/2607.26348

[CONFIRME] **"Plausible but Not Valid: A Psychometric Audit of LLMs as Synthetic Survey
Respondents"**, Lukauskas et Sarkauskaite, arXiv 2608.14606, juillet 2026. 37 modeles audites,
jeu de donnees lituanien de psychologie du travail, 263 employes, 68 items, 12 sous echelles.
Cadre a six dimensions (Psychometric Similarity Score) ancre sur cinq baselines statistiques et
un plafond humain contre humain a 0,825.
Resultats : une baseline **copule gaussienne** sans langage, a 0,69, bat tous les LLM sur la
distribution, la correlation et la fiabilite. Le meilleur LLM atteint 0,71, a peine au dessus.
Les auteurs concluent que l'essentiel de la fidelite psychometrique est recuperable a partir de
la structure de covariance humaine, sans modele de langage. Sur la variance : restriction
d'etendue et sur coherence, homogeneite moyenne entre LLM a 0,73 superieure a la similarite
LLM vers humain, decalage d'acquiescement de plus 0,84 ecart type. Validite predictive sur
humains non vus effondree, R carre de moins 0,18 contre 0,28 pour des modeles entraines sur
humains. Effets de mediation significatifs fabriques sur 3 des 10 chemins nuls.
Source : https://arxiv.org/html/2608.14606

**Lecture combinee.** Ces deux papiers de 2026 disent la meme chose de deux facons : le
diagnostic "les LLM ecrasent la variance" tel qu'il figure dans CONTEXTE.md est **incomplet et
partiellement date**. La litterature recente montre deux defauts distincts et simultanes,
une restriction d'etendue intra individuelle (les reponses sont trop coherentes et trop
centrees) et une exageration des ecarts inter groupes (les modeles caricaturent les
demographies). Ce n'est pas une mauvaise nouvelle pour le projet, c'est une **precision de la
question de recherche**. Une contribution qui se contenterait de "restaurer la variance"
serait battue par une copule gaussienne, comme le montre l'audit de 2608.14606. Une
contribution qui separerait proprement les deux pathologies, et qui proposerait une metrique
distinguant variance intra groupe et ecart inter groupes, n'a pas encore d'occupant.

**Conclusion de la section 3.** L'angle "personne ne publie de validation serieuse" **n'est plus
disponible tel quel**. Simile publie, Qualtrics publie, PyMC Labs publie, Ipsos et Stanford
construisent un dispositif de validation. L'angle qui reste disponible est plus etroit et plus
defendable : **personne ne publie de benchmark comparatif inter fournisseurs sur un jeu de test
commun**. Aucun acteur n'a interet a le faire, puisque chacun choisit sa metrique. C'est une
place vacante pour un laboratoire academique, pas pour un vendeur.

---

## 4. L'economie du market research traditionnel : le pitch tient il

Pitch a verifier : "12 000 euros et 3 mois deviennent 1 000 euros et 2 secondes."

### 4.1 Le cout du repondant seul

[CONFIRME] **Prolific.** Frais de plateforme de 42,8 pour cent pour les entreprises, 33,3 pour
cent pour l'academique et le non lucratif, ajoutes par dessus la remuneration du participant,
qui recoit l'integralite de ce qui est affiche. Remuneration recommandee 9 livres ou 12 dollars
de l'heure, minimum autorise 6 livres ou 8 dollars de l'heure. Exemple documente : une etude de
200 personnes sur 15 minutes au tarif recommande revient a environ 857 dollars hors TVA, soit
**environ 4,30 dollars par repondant**.
Sources : https://www.prolific.com/pricing ,
https://researcher-help.prolific.com/en/articles/445239-what-is-your-pricing

[CONFIRME] **Panels programmatiques (Cint, Dynata, Toluna).** Le cout par interview complete en
population generale se situe autour de 2 a 15 dollars. Les audiences a faible incidence, sous
5 pour cent, sont facturees a un multiple important. Les devis pour un meme echantillon varient
de 4 a 50 dollars par complete selon le taux d'incidence, la longueur du questionnaire et la
specificite de l'audience. Dynata et Cint pratiquent le devis sur mesure, pas de tarif public.
Sources : https://www.koji.so/blog/survey-sample-cost-cpi-incidence-rate-2026 ,
https://www.driveresearch.com/market-research-company-blog/what-is-cpi-in-market-research-glossary/
[Note de fiabilite : ces fourchettes viennent de guides d'editeurs et d'agences, pas de tarifs
officiels des panelistes. Aucun des quatre panelistes cites ne publie de grille. Traiter comme
ordre de grandeur, pas comme prix source. Respondi n'a pas de tarif public trouve.]

[CONFIRME] **France, tarifs publics d'instituts.** Symbial annonce des enquetes flash a partir
de 4 900 euros HT pour 1 000 repondants representatifs, methode des quotas, panel certifie,
base de donnees et rapport de synthese inclus. Selvitys annonce des reponses a partir de
1,80 euro HT par repondant avec un minimum de 800 euros HT. IntoTheMinds indique que les
prestataires facturent souvent entre 2 et 10 euros par questionnaire administre et analyse, et
qu'une enquete en ligne sur base client revient a environ 7 500 euros en moyenne, questionnaire,
programmation, administration et analyse compris.
Sources : https://www.symbial.fr/enquete_flash/ , https://selvitys.fr/nos-tarifs/ ,
https://www.intotheminds.com/blog/en/market-research-what-does-it-cost/

### 4.2 Le cout d'un projet complet

[CONFIRME] **Etats Unis.** Un projet d'etude sur mesure, qualitatif ou quantitatif, se situe
autour de 25 000 a 65 000 dollars en 2025 et 2026. Par methode : enquete en ligne 5 000 a
15 000 dollars et plus pour environ 400 completes sur un marche, enquete telephonique 15 000 a
30 000 dollars et plus, enquete en face a face 20 000 a 50 000 dollars et plus.
Sources : https://www.driveresearch.com/market-research-company-blog/how-much-does-market-research-cost/ ,
https://www.thefarnsworthgroup.com/blog/market-research-cost ,
https://www.market-xcel.com/us/blogs/market-research-cost-usa

### 4.3 Le delai reel

[CONFIRME] Un projet sur mesure complet prend generalement 6 a 12 semaines. Une enquete
quantitative simple prend 2 a 4 semaines si le questionnaire, la cible et la logique d'analyse
sont clairs. Une enquete telephonique 4 a 8 semaines. Les etudes conjointes et de choix discret
6 a 12 semaines. Decomposition typique : 2 a 3 semaines de conception et de questionnaire, 2 a
4 semaines de terrain sur echantillon complexe, 2 a 4 semaines d'analyse.
Sources : https://www.driveresearch.com/market-research-company-blog/how-long-does-market-research-take/ ,
https://www.insightfulresearch.co.uk/post/how-long-does-it-take-to-conduct-market-research

### 4.4 La taille du marche

[CONFIRME] Industrie mondiale des insights, chiffres ESOMAR relayes par Research World :
142 milliards de dollars en 2023, **153 milliards de dollars en 2024**, plus de 160 milliards
projetes pour 2025. Decomposition 2024 : 56 milliards pour la recherche marche stricto sensu
(croissance 4,8 pour cent), 62 milliards pour les logiciels de recherche (croissance
11,5 pour cent), 35 milliards pour le reporting (croissance 8 pour cent). Dans le sous secteur
recherche marche, environ 62 pour cent en full service incluant le terrain, 31 pour cent en
abonnement et logiciel, 7 pour cent en conseil.
Sources : https://researchworld.com/articles/inside-the-153bn-insights-industry ,
https://researchworld.com/articles/drivers-of-our-142bn-insights-industry

[NON VERIFIE] **Je n'ai trouve aucun chiffre fiable sur la part du marche deja captee par
l'IA ou par les donnees synthetiques.** L'article ESOMAR de reference n'en donne aucun. Les
seuls chiffres qui circulent sont declaratifs, du type "95 pour cent des directeurs marketing
prevoient d'utiliser de la donnee synthetique dans les 12 mois" (Qualtrics, octobre 2025), ce
qui mesure une intention et non un chiffre d'affaires. Une prevision Qualtrics reprise par
PyMC Labs annonce plus de 50 pour cent d'ici 2027, source d'editeur, a traiter comme du
marketing. Ne pas utiliser ces chiffres devant le MIT.

### 4.5 Verdict argumente sur le pitch

**Le terme "12 000 euros" est defendable, en bas de fourchette et pour l'Europe.** Il correspond
a un projet quantitatif francais complet de taille moyenne, entre les 7 500 euros d'une enquete
en ligne sur base client et les 25 000 dollars du bas de la fourchette americaine. Aux Etats
Unis, ou le projet vise a se vendre, **12 000 dollars est en dessous du marche** pour un projet
full service, et le pitch se prive de moitie de son effet. Le chiffre honnete aux Etats Unis
serait 25 000 a 65 000 dollars. [CONFIRME par les sources ci dessus]

**Le terme "3 mois" est defendable et meme conservateur** pour du full service ou du conjoint,
6 a 12 semaines etant la norme. Il est **malhonnete pour une enquete simple sur panel en ligne**,
qui se boucle en 2 a 4 semaines et parfois en quelques jours en programmatique. [CONFIRME]

**Le terme "1 000 euros" n'a pas de fondement etabli.** Il n'existe aucun prix public dans le
segment A auquel le comparer. Simile, Aaru, Evidenza, Electric Twin ne publient rien. Le seul
prix public du secteur est celui de Synthetic Users, segment B : a partir de 12 500 dollars par
an, avec un entretien entre 2 et 60 dollars. Sur cette base, **1 000 euros par etude est
plausible comme prix de vente mais ne peut pas etre presente comme un prix de marche verifie**.
[HYPOTHESE, a assumer comme telle]

**Le terme "2 secondes" est le plus fragile.** Il decrit le temps d'inference, pas le temps de
livraison. Chez Simile, la construction du modele de population suppose le recrutement d'une
population representative et des sessions de laboratoire de deux heures. Chez Evidenza, l'engagement
public est de 72 heures, pas de 2 secondes. Chez Fairgen, il faut au minimum 300 repondants
reels. **La partie couteuse et lente n'est pas la reponse, c'est la calibration**, et le pitch
la fait disparaitre. Sous contrainte "aucun humain recrute", c'est exactement la partie que
popsim ne peut pas encore produire. [CONFIRME par les methodes decrites en section 2]

**Le terme "5 pour cent de marge d'erreur" est le plus risque.** Aucune source publiee ne
soutient 5 pour cent d'erreur sur une reproduction d'etude arbitraire. Le meilleur resultat
academique disponible est 85 pour cent du test retest humain, ce qui n'est pas 95 pour cent de
precision et n'est pas la meme quantite. Le benchmark de juillet 2026 (arXiv 2607.26348) montre
des LLM generalistes **sous une baseline demographique** sur la WVS. Promettre 5 pour cent
devant un acheteur d'etudes competent est un risque de credibilite immediat. [CONFIRME]

**Sur quel segment le pitch est credible.** Concept testing, test de messages, pre test
publicitaire, priorisation de features, sondage d'opinion agrege sur des questions deja posees
ailleurs. Ce sont des usages directionnels, ou l'ordre de classement compte plus que le niveau
absolu, et ou l'echec est peu couteux.
**Sur quel segment il est malhonnete.** Toute etude ou le niveau absolu engage une decision
chiffree : elasticite prix reelle, prevision de part de marche, recherche clinique, et surtout
les segments minoritaires ou peu representes, precisement la ou la litterature de 2026 documente
la caricature demographique. Le pitch "montrez nous votre derniere etude, on la reproduit" est
d'ailleurs biaise par construction : reproduire une etude deja realisee n'est pas la meme tache
que predire une etude non encore realisee, et un acheteur averti le fera remarquer.

---

## 5. Se vendre depuis San Francisco : ce qui est documente

### 5.1 Le modele "research lab to company" est le modele dominant de ce secteur precis

[CONFIRME] Ce n'est pas une intuition, c'est le motif observe sur les trois acteurs les plus
finances du segment A et A moins.
- **Simile** : sortie directe du laboratoire de Stanford, papier d'abord (2023 puis 2024),
  societe ensuite (2025 ou 2026), 300 millions de dollars leves en cinq mois. Park decrit
  l'entreprise comme un hybride laboratoire de recherche et societe produit, avec pres de
  20 pour cent d'anciens de Microsoft Research.
  Source : https://www.latent.space/p/simile
- **Artificial Societies** : fondee par deux scientifiques du comportement, passee par YC W2025,
  5,35 millions de dollars.
  Source : https://www.ycombinator.com/companies/artificial-societies
- **Fairgen** : leve 8 millions de dollars en affichant un professeur de statistiques de
  Stanford comme conseiller scientifique principal, mentionne dans le communique de levee lui
  meme.
  Source : https://www.fairgen.ai/press-releases/fairgen-raises-8m-for-statistically-accurate-ai-generated-survey-responses

**La publication scientifique fonctionne bien comme actif commercial dans ce secteur, mais
d'une facon precise** : elle sert de preuve de credibilite au moment de la levee et de la vente
enterprise, pas d'avantage technique durable. [PROBABLE, fonde sur le fait que le papier de
Simile est public et reproductible depuis novembre 2024, et que cela n'a pas empeche la societe
de lever a 2 milliards : ce qui est valorise n'est pas le papier, c'est l'equipe qui l'a ecrit
et le dispositif de collecte de donnees qu'elle construit.]

### 5.2 Les partenariats academiques comme dispositif commercial

[CONFIRME] Ipsos avec le Polarization and Social Change Lab de Stanford, aout 2025, avec pour
objet la construction d'une base de verite terrain et la validation des jumeaux numeriques.
C'est le format le plus proche de ce que popsim pourrait offrir a un institut, et il montre
qu'un institut etabli est pret a acheter de la validation academique, pas seulement de la
technologie.
Source : https://www.ipsos.com/en/ipsos-partners-stanford-university-pioneer-future-market-research-synthetic-data

[CONFIRME] Simile a un partenariat avec Gallup, presente comme apportant un panel
representatif national a echantillonnage probabiliste. Meme logique inversee : le laboratoire
achete la legitimite d'echantillonnage de l'institut.
Source : https://gizmodo.com/an-ai-company-apparently-inspired-by-the-sims-wants-to-revolutionize-public-opinion-research-2000731038

### 5.3 Modeles de prix observes dans le secteur

- **Abonnement annuel avec pool de jetons** : Synthetic Users, a partir de 12 500 dollars par an,
  entretien facture 2 a 60 dollars sur le pool, jusqu'a 20 pour cent des jetons non consommes
  reportes au renouvellement, sieges collaboratifs illimites. **Seul modele entierement public
  du secteur.** Source : https://www.syntheticusers.com/pricing
- **Contrat enterprise negocie, prix non publie** : Simile, Aaru, Evidenza, Electric Twin,
  Qualtrics, Quantilope. C'est la norme absolue du segment A et A moins.
- **Prix a l'experience** : revendique par Subconscious AI (10 dollars par experience), chiffre
  marketing non verifiable.
- [HYPOTHESE] La lecture qui se degage est que **le segment A ne vend pas des etudes a l'unite,
  il vend un modele de population sous contrat annuel**. Vendre 1 000 euros l'etude place
  mecaniquement popsim dans le segment B, cote prix comme cote perception.

### 5.4 Programmes accueillant des fondateurs non americains, conditions publiques

| Programme | Investissement | Dilution ou droits | Note |
|---|---|---|---|
| **Y Combinator** | 500 000 USD : 125 000 pour 7 pour cent en SAFE post money, plus 375 000 en SAFE non plafonne avec clause MFN | 7 pour cent plus dilution future | Montant inchange depuis 2022, aucune negociation possible. YC accepte regulierement des societes internationales, plus de 20 societes venues de l'etranger dans un batch recent. Source : https://www.ycombinator.com/deal |
| **South Park Commons, Founder Fellowship** | 400 000 USD pour 7 pour cent en SAFE, plus 600 000 garantis au prochain tour externe, soit 1 M USD | 7 pour cent | Plus de 900 000 USD de credits partenaires. Deux phases, bootcamp en presentiel a San Francisco puis residence sans date de fin. Source : https://www.southparkcommons.com/faq/ |
| **Neo (Ali Partovi), Neo Residency** | 750 000 USD en SAFE non plafonne, plus de 450 000 USD de credits de calcul | Droits de participation jusqu'a 5 pour cent au prochain tour en equity, pas de dilution immediate | 3 mois d'espace de travail a SF, bootcamp de 2 semaines en Oregon. Volet etudiant : 40 000 USD de bourse par personne. Source : https://neo.com/accelerator-apply |
| **AI Grant (Nat Friedman, Daniel Gross)** | 250 000 USD en SAFE non plafonne, 350 000 USD de credits Azure, 250 000 USD d'autres credits | SAFE non plafonne | Historiquement propose aussi des accords calcul contre equity sur le cluster Andromeda. Source : https://www.microsoft.com/en-us/startups/blog/microsoft-for-startups-supporting-second-cohort-of-ai-grant-to-propel-ai-first-startups/ |
| **Entrepreneur First, parcours US** | Jusqu'a 250 000 USD par societe formee : 125 000 en SAFE post money pour 8 pour cent, plus 125 000 en SAFE MFN non plafonne (EF et Transpose Platform). Bourse sans dilution de 10 000 USD en phase d'ideation | 8 pour cent | On postule seul, appariement de cofondateurs dans la cohorte, constitution d'une C-Corp du Delaware pendant le programme. Plus de 600 000 USD de credits partenaires. Suivi possible jusqu'a 5 M USD jusqu'en Serie B. Source : https://apply.joinef.com/ |

**Visas.** [CONFIRME]
- **O-1A** : il faut satisfaire au moins 3 des 8 criteres de l'USCIS pour l'aptitude
  extraordinaire. Aucune exigence de diplome, aucun seuil de capital. Les criteres les plus
  utilisables par un fondateur sont les contributions originales, le role critique ou essentiel,
  et la publication de materiel a son sujet. Le formulaire I-129 doit etre depose par un
  employeur ou un agent americain, ce que la societe americaine du fondateur peut faire si la
  structure documente clairement le lien de subordination.
  Source : https://www.beyondborderglobal.com/resources/o-1a-startup-founder
- **E-2** : la France est un pays sous traite, y compris la Martinique, la Guadeloupe, la
  Guyane et La Reunion. Il n'existe **aucun montant minimum officiel**, l'investissement doit
  etre "substantiel" au regard du cout total de l'entreprise. Les dossiers aboutis se situent
  souvent entre 80 000 et 300 000 dollars, et les investissements sous 100 000 dollars
  subissent un examen renforce.
  Sources : https://fr.usembassy.gov/visas/treaty-trader-e-1-and-treaty-investor-e-2-visas/ ,
  https://www.immi-usa.com/e2-visa-requirements-for-investors/

**Lecture sous contrainte budget zero.** Le O-1A est la seule voie compatible avec un budget nul
cote capital, et **une publication scientifique en est le principal carburant** : c'est le
premier usage commercial concret du papier vise. Le E-2 est incompatible avec la contrainte,
il suppose un apport en capital. Parmi les programmes, seul Entrepreneur First a une phase
d'ideation remuneree sans dilution, ce qui est la seule porte d'entree compatible avec l'etat
actuel du projet (pas de societe, pas de produit).

---

## 6. Angle de differenciation : evaluation honnete des atouts declares

### 6.1 "Acces possible aux auteurs de Stanford" : atout annule

[CONFIRME] Park, Bernstein et Liang ont fonde Simile. Ils dirigent une societe a 2 milliards de
dollars dont le produit est exactement ce que popsim veut construire, avec les memes clients
cibles. Un contact chaud vers eux n'ouvre pas une collaboration, il ouvre au mieux une
conversation avec un concurrent qui a 300 millions de dollars et 60 personnes d'avance, et au
pire une fuite d'information dans le mauvais sens. **Cet atout doit sortir du dossier, ou etre
requalifie en risque.**

Nuance : Robb Willer, co-auteur du papier de 2024, dirige le Polarization and Social Change Lab
de Stanford, qui a signe avec Ipsos. Il n'apparait pas parmi les fondateurs de Simile. [PROBABLE]
Un acces academique aux co-auteurs restes en laboratoire est donc peut etre possible, mais il
conduit vers un dispositif deja engage avec un institut mondial.

### 6.2 "Reproduire le resultat de Stanford" : sans valeur commerciale, valeur pedagogique reelle

[CONFIRME] Le resultat de 85 pour cent est public depuis novembre 2024 et ses auteurs l'ont deja
industrialise. Une reproduction a petite echelle ne cree aucune position defendable face aux
acteurs finances. **Elle garde de la valeur comme preuve de competence pour une candidature,
un partenariat MIT ou un dossier O-1A, pas comme actif commercial.** Il faut le dire ainsi dans
le dossier plutot que de laisser croire a un avantage.

Point aggravant sous contrainte budget zero et zero humain recrute : la reproduction fidele du
protocole suppose des entretiens de deux heures avec des individus reels consentants, exactement
ce qui est interdit par les contraintes du 2 septembre. Ce qui reste realisable est la
reproduction sur donnees d'enquete publiques deja collectees, sans la couche entretien, ce qui
n'est pas le meme resultat.

### 6.3 "La contribution sur la variance" : encore ouverte, mais mal formulee

C'est l'atout qui resiste le mieux, a condition de le reformuler.

[CONFIRME] Deux papiers de juillet 2026 montrent que le probleme n'est pas celui decrit dans
CONTEXTE.md. arXiv 2607.26348 documente une caricature demographique, avec des ecarts inter
groupes fabriques par les modeles la ou les humains n'en montrent pas. arXiv 2608.14606
documente une restriction d'etendue intra individuelle plus un biais d'acquiescement de plus
0,84 ecart type, et surtout montre qu'une **copule gaussienne sans langage bat tous les LLM sur
la distribution, la correlation et la fiabilite**.

Ce que cela implique.
1. La formulation "les LLM ecrasent la variance, nous la restaurons" est **battue par une
   baseline statistique triviale**. Un evaluateur du MIT posera cette question en premier.
2. La question encore ouverte, et defendable, est la **decomposition** : separer ce qui releve
   de la variance intra groupe et ce qui releve des ecarts inter groupes, et montrer qu'un
   dispositif fait mieux que la copule gaussienne **sur la validite predictive hors echantillon**,
   la ou l'audit de 2608.14606 mesure un R carre de moins 0,18 pour les LLM contre 0,28 pour
   des modeles entraines sur humains.
3. [HYPOTHESE] Une contribution qui proposerait une metrique publique et un jeu de test commun
   pour comparer des fournisseurs occuperait un espace que personne n'a interet a occuper
   commercialement. C'est le seul angle qui soit a la fois vacant, compatible avec un budget
   nul, et coherent avec la position officielle "on veut d'abord un papier".

### 6.4 "Double casquette psychologie et IA de Simon" et contacts MIT

[HYPOTHESE, non verifiable par recherche web] Cet atout a une valeur reelle mais elle est
generique dans ce marche precis. Artificial Societies est fondee par deux scientifiques du
comportement, Simile est fondee par des chercheurs en interaction homme machine et en NLP,
Fairgen s'adosse a un statisticien de Stanford, Ipsos a un laboratoire de Stanford. **Avoir un
psychologue dans l'equipe n'est pas differenciant dans ce secteur, c'est le ticket d'entree.**
Ce qui serait differenciant est une expertise psychometrique formelle, au sens de la theorie de
la reponse a l'item et de la validite de construit, precisement l'outillage qu'utilise l'audit
de 2608.14606 et que les acteurs commerciaux n'utilisent pas. C'est une question a poser a
Simon, elle est en section 8.

### 6.5 Ou popsim n'a aucune chance, et il faut l'ecrire

- **Sur la donnee de calibration.** Le fosse de Simile n'est pas l'algorithme, c'est le
  dispositif de collecte : recrutement representatif, sessions de laboratoire de deux heures,
  donnees transactionnelles, RCT de mecanisme. Sous contrainte budget zero et zero humain
  recrute, popsim ne peut pas s'en approcher. [CONFIRME par la description de methode Simile]
- **Sur la vitesse commerciale.** Simile a signe CVS, Deloitte, Wealthfront et Gallup en moins
  d'un an. Aaru a signe EY, Accenture et IPG. Le marche enterprise du segment A se referme vite.
- **Sur le prix.** Vendre 1 000 euros l'etude dans un marche ou les acteurs credibles vendent
  des contrats annuels a prix negocie place popsim dans le segment B, avec Synthetic Users a
  12 500 dollars par an et une quinzaine de concurrents sans barriere technique.

### 6.6 Position defendable, formulee

[HYPOTHESE assumee, c'est une recommandation et non un fait]
La seule position que je vois tenir simultanement avec les contraintes du 2 septembre et avec
l'etat du marche est celle ci : **ne pas etre un fournisseur de simulation, etre l'autorite qui
mesure les simulations.** Concretement, un benchmark public de fidelite de populations
simulees, construit sur des enquetes publiques deja collectees (GSS, World Values Survey,
European Social Survey), avec une metrique qui separe variance intra groupe et ecart inter
groupes, ancree sur des baselines statistiques explicites dont la copule gaussienne, et une
comparaison des modeles ouverts executables en local.

Pourquoi cette position tient.
- Elle est realisable a budget zero et sans recruter d'humain, puisque les enquetes existent.
- Elle est publiable, donc coherente avec la position officielle du projet et avec un dossier
  O-1A.
- Elle occupe la seule place vacante identifiee en section 3, celle du benchmark inter
  fournisseurs.
- Elle place popsim en amont de Simile, Aaru et Ipsos plutot qu'en concurrence frontale, et
  elle cree une raison pour eux de parler au projet.
- Elle est monetisable plus tard, soit par l'audit, soit en basculant vers un produit une fois
  la metrique reconnue.

Pourquoi elle peut echouer.
- Un benchmark n'est une autorite que s'il est adopte. Sans le nom du MIT ou d'une conference
  reconnue, il ne pese rien. [PROBABLE]
- Qualtrics appelle deja publiquement a ce standard et a les moyens de le publier avant nous.
- Ce n'est pas une entreprise a forte valorisation, c'est un actif de reputation. Si l'objectif
  reel est de lever, cette voie n'y mene pas directement.

---

## 7. Ce que je n'ai pas pu verifier

- **Le prix reel de Simile, Aaru, Evidenza, Electric Twin, Qualtrics Edge et Quantilope.** Aucun
  n'est public. Les chiffres qui circulent (50 000 a 100 000 dollars par an pour Evidenza,
  50 000 a 75 000 pour Quantilope) proviennent de sites de review generes en partie par IA, sans
  source primaire. Je ne les ai pas retenus comme prix, seulement comme rumeur signalee.
- **La mention de contrats "a plusieurs millions de dollars" chez Simile.** Elle apparait dans le
  compte rendu d'une interview, pas dans un document de la societe.
- **La date exacte de la Serie B de Simile.** Le billet d'Index Ventures est date du 30 juillet
  dans le rendu que j'ai obtenu, avec une annee ambigue, alors que l'article TechCrunch la place
  au 30 juillet 2026. J'ai retenu 2026, coherent avec la Serie A de fevrier 2026 et le delai de
  cinq mois. A reverifier avant toute citation.
- **La taille d'equipe** de tous les acteurs sauf Simile. Aucune source fiable trouvee.
- **La part du marche des etudes deja captee par l'IA ou la donnee synthetique.** Aucun chiffre
  de chiffre d'affaires trouve, seulement des intentions declarees. Le rapport ESOMAR Global
  Market Research 2025 est payant et je n'y ai pas eu acces, il contient peut etre la reponse.
- **L'article Bloomberg du 12 février 2026** sur la Serie A de Simile est derriere un paywall.
  Je n'ai lu que le titre et la date via les resultats de recherche.
- **Les pages "Evidence" de Subconscious AI et le livre blanc de validation de Yabble.** Non
  ouverts, donc leurs protocoles ne sont pas verifies.
- **Viewpoints AI, Perceptif, Personax, Rally.** Trop peu de matiere publique pour les classer
  autrement que par defaut en segment B non documente. Il est possible que "Rally" et "Perceptif"
  designent des produits differents de ceux que mes recherches ont ramenes.
- **McKinsey QuantumBlack.** Aucune offre de repondants synthetiques identifiee. Absence de
  preuve, pas preuve d'absence.
- **Le lien entre les deux papiers critiques de 2026 et la litterature revue par les pairs.**
  arXiv 2607.26348 est declare en cours de revue, arXiv 2608.14606 est un preprint. Leurs
  conclusions sont solides sur la forme mais pas encore validees par la communaute.
- **Le statut academique actuel de Robb Willer et des autres co-auteurs du papier de 2024.**
  Je deduis qu'ils ne sont pas chez Simile parce qu'ils ne figurent pas dans la liste des
  fondateurs, ce n'est pas une verification directe.

---

## 8. Questions ouvertes pour Simon

1. **La question qui commande tout le reste.** Sachant que Park, Bernstein et Liang ont fonde
   Simile et leve 300 millions de dollars en cinq mois sur exactement cette these, quelle est la
   raison pour laquelle popsim devrait exister ? Si la reponse est "publier avec le MIT", le
   projet reste entierement valide et il faut alors assumer que ce n'est pas une entreprise. Si
   la reponse est "construire un produit", il faut nommer ce que Simile ne fera pas.
2. **Le contact MIT connait il l'existence de Simile ?** Sa reaction a cette information est
   l'information la plus utile que nous puissions obtenir cette semaine, avant tout travail
   technique.
3. **Sur la variance.** La litterature de juillet 2026 dit deux choses qui contredisent le
   cadrage du projet : les modeles caricaturent les demographies plutot qu'ils ne les
   homogeneisent, et une copule gaussienne sans langage bat tous les LLM sur la fidelite
   distributionnelle. Es tu d'accord pour reformuler la contribution en decomposition variance
   intra groupe contre ecart inter groupes, avec la copule gaussienne comme baseline obligatoire ?
4. **Psychometrie formelle.** Ta double casquette couvre t elle la theorie de la reponse a
   l'item, la validite de construit et l'invariance de mesure ? C'est l'outillage qu'utilise
   l'audit de 2608.14606, et c'est le seul terrain ou notre profil serait reellement rare face
   aux equipes concurrentes.
5. **Le precedent en psychiatrie publie dans Nature** que tu cites dans CONTEXTE.md : peux tu
   donner la reference exacte ? Je ne l'ai pas identifiee et elle changerait le choix du
   journal cible.
6. **Positionnement.** Acceptes tu la bascule proposee en 6.6, de fournisseur de simulation vers
   auteur du benchmark de fidelite ? C'est la seule voie que je trouve compatible avec budget
   zero, zero recrutement humain et un marche qui se ferme.
7. **Le pitch commercial.** Les termes "5 pour cent de marge d'erreur" et "2 secondes" sont
   indefendables en l'etat devant un acheteur competent ou un evaluateur academique. Acceptes tu
   de les retirer du discours tant qu'aucune mesure interne ne les soutient ?
8. **Ipsos.** Ipsos a un partenariat de validation avec un laboratoire de Stanford depuis aout
   2025. Un institut francais equivalent, ou Ipsos France, serait il un meilleur premier
   interlocuteur qu'un acteur americain, compte tenu de nos contraintes et de notre localisation ?
