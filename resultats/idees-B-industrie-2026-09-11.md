# Idées B : auditer les promesses de l'industrie des répondants synthétiques

Brainstorm du 11 septembre 2026, angle B. Travail en lecture seule sur le dépôt, recherche web, aucun appel de modèle.
Conventions : **[CONFIRMÉ]** lu dans la source citée ; **[PRESSE]** chiffre rapporté par un tiers et non vu sur la page
du vendeur ; **[HYPOTHÈSE]** prédiction à tester. Les antériorités académiques sont celles de
`resultats/veille-anteriorite-2026-09-11.md`.

## 0. Règles du jeu, juridiques et réputationnelles

1. **On teste des métriques et des méthodes publiées, jamais un produit.** La formule type est : « la métrique X, telle que
   définie publiquement, est atteinte à Y par la baseline Z sur les jeux A, B et C ». On n'écrit jamais « le produit de W ne
   marche pas » : leurs items, leurs données et leurs modèles sont privés, et nos résultats ne s'y transposent pas.
2. **Chaque affirmation citée est archivée et datée** (capture web.archive.org), avec une citation exacte et la nature de
   la source (vendeur ou presse). Beaucoup de chiffres ne circulent que dans la presse spécialisée, qui a pu les déformer.
3. **Aucun nom de vendeur dans les titres d'articles.** Les noms n'apparaissent que dans le tableau des affirmations.
4. **Droit de réponse** : envoyer le préprint aux vendeurs cités quelques jours avant la mise en ligne, s'ils l'acceptent.
   Cet envoi exige l'accord explicite de l'utilisateur.
5. **Préenregistrement** avant toute mesure, avec les métriques du vendeur reconstruites *avant* de voir nos scores.
   Si une définition publique est trop vague pour être reconstruite (NDAM, « overlap », « parity »), on le dit, et
   cela devient un constat.

## 1. Inventaire des affirmations chiffrées

| Acteur | Affirmation précise | Métrique déclarée | Source |
|---|---|---|---|
| Electric Twin | 95,5 % en 1-MAE et 92 % en NDAM, « à 2 points du bruit humain » (retest environ 94 % NDAM) ; les panels classiques font 96 % en 1-MAE ; aucune baseline naïve [CONFIRMÉ] | 1-MAE sur proportions ; NDAM normalisée | https://www.electrictwin.com/blog/how-accurate-are-synthetic-audiences |
| Electric Twin | « 10 000 fois plus rapide, 95 % d'exactitude », recherche avec M. Muthukrishna (LSE) [PRESSE] | non définie | https://startupsmagazine.co.uk/electric-twin-raises-14m-to-bring-synthetic-audiences-to-life |
| Aaru | EY Global Wealth Study recréée en un jour, simulation à l'aveugle : Spearman médian 0,90 sur 53 questions à choix unique, écart moyen de 7,1 points [CONFIRMÉ] | Spearman médian, MAE | https://aaru.com/case-studies/ey-wealth-research |
| Aaru | Primaire démocrate de New York 2024 prédite à 371 voix près ; Harris donnée gagnante en 2024 [PRESSE] | écart en voix | https://www.semafor.com/article/09/20/2024/ai-startup-aaru-uses-chatbots-instead-of-humans-for-political-polls ; https://www.natesilver.net/p/ai-polls-are-fake-polls |
| Aaru | Series A à 1 milliard de dollars de valorisation (décembre 2025) ; « simuler le globe entier d'ici deux ans » [PRESSE] | aucune | https://www.aicerts.ai/news/aarus-1b-series-a-highlights-synthetic-datas-market-surge/ |
| Evidenza | EY : 1 000 personas synthétiques, « 95 % de corrélation » avec l'enquête EY auprès de PDG [PRESSE] | corrélation, non précisée | https://www.mi-3.com.au/27-08-2024/synthetic-customers-meet-synthetic-cmos-and-cfos-evidenza-clones-sharp-ritson-binet |
| Evidenza | « 88 % d'exactitude sur plus de 100 validations » ; Dentsu : corrélation de 0,87 [PRESSE, résumé Replism] | moyenne de concordance | https://www.evidenza.ai/ ; https://replism.com/blog/state-of-synthetic-audiences-2026 |
| Simile (Park et al.) | 85 % de l'exactitude de réplication humaine sur le GSS (Park et al. 2411.10109) ; « 85 à 99 % » face à des focus groups pour CVS ; 8 prévisions de résultats trimestriels sur 10 [PRESSE] ; 100 M$ puis 200 M$ à 2 Md$ en 2026 | exactitude normalisée par le retest | https://www.zenml.io/llmops-database/building-digital-twins-at-population-scale-from-generative-agents-to-behavioral-foundation-models ; https://thenextweb.com/news/simile-200-million-agentic-twins-ai-market-research |
| Artificial Societies | 86 % de précision distributionnelle sur 1 000 enquêtes, contre un plafond d'autoréplication humaine de 91 % ; 67 % pour un LLM à biographie ; cohérence interne de 89 % [CONFIRMÉ] ; plus de 80 % sur la performance de posts sociaux [PRESSE] | recouvrement des distributions | https://societies.ai/how-accurate-are-ai-personas/ ; https://siliconangle.com/2025/07/30/ai-startup-artificial-societies-simulates-behavior-target-audiences-speed-market-research/ |
| Synthetic Users | « Synthetic Organic Parity » de 85 à 92 %, score pondéré (recouvrement thématique 30 %, profondeur 30 %, couverture 20 %, alignement 20 %), établi sur **8 entretiens** d'enseignants britanniques [CONFIRMÉ] | score composite qualitatif | https://www.syntheticusers.com/science-posts/how-we-measure-success |
| Qualtrics Edge Audiences | « 12 fois plus exact qu'une IA généraliste » : écart de 0,07 écart-type contre 0,87 pour GPT-5 et Gemini, sur un questionnaire de 11 questions (réplication de Paxton et Yang 2024 par un employé de Qualtrics) [CONFIRMÉ] | écart des moyennes en écarts-types | https://www.greenbook.org/insights/data-science/testing-synthetic-data-against-academic-benchmarks-a-replication-study ; https://www.qualtrics.com/strategy/audiences/ |
| Kantar | Boosting synthétique : « 94 à 95 % d'exactitude contre la vérité terrain » [PRESSE] | non définie | https://www.kantar.com/campaigns/a-definitive-guide-to-synthetic-data-boosting-in-brand-health-tracking |
| Ipsos | Base de vérité terrain pour valider des jumeaux numériques, avec le Politics and Social Change Lab de Stanford ; cadre SURE ; pas de chiffre trouvé [CONFIRMÉ] | à venir | https://www.ipsos.com/en/ai/transforming-research-through-synthetic-data |
| Toluna HarmonAIze Personas | Chaque répondant « imite une réponse humaine individuelle, pas la moyenne d'un segment » ; personas construites sur un panel de 19,4 M ; les personas « raisonnent, expriment des émotions » ; pas de chiffre [CONFIRMÉ] | aucune | https://tolunacorporate.com/transforming-consumer-insights-meet-tolunas-next-gen-synthetic-respondents/ |
| Yabble Virtual Audiences | Plus pertinent, exact et récent qu'un LLM seul ; pas de chiffre [CONFIRMÉ] | aucune | https://www.yabble.com/blog/why-yabbles-virtual-audiences-is-the-ai-tool-for-market-research |
| PyMC Labs et Colgate (méthode SSR, reprise par des vendeurs) | « 90 % de la fiabilité test-retest humaine », similarité KS supérieure à 0,85, sur 57 enquêtes et 9 300 répondants ; code ouvert [CONFIRMÉ] | taux d'atteinte de corrélation, similarité KS | https://arxiv.org/abs/2510.08338 ; https://github.com/pymc-labs/semantic-similarity-rating |
| BCG | 92 % d'exactitude sur des choix de boissons (conjoint) [PRESSE, source unique] | non définie | https://replism.com/blog/state-of-synthetic-audiences-2026 |
| Autres acteurs 2026 | Listen Labs (valorisé 500 M$, rachat par Salesforce discuté en septembre 2026), Outset et Keplar interrogent de **vrais** humains avec un modérateur IA et sont hors sujet ; Sameulation vend un « audit » de panels synthétiques | — | https://techcrunch.com/2026/09/09/ai-research-startup-listen-labs-scrubbed-a-1-5b-funding-round-for-salesforce-talks/ ; https://sameulation.com/ |

**Constat transversal** [CONFIRMÉ sur les pages lues] : aucune page vendeur consultée ne rapporte de **baseline naïve**
(distribution uniforme, marge d'une autre vague, LLM sans persona). Le seul point de comparaison est soit un « LLM
généraliste » (Qualtrics, Artificial Societies), soit un plafond humain (Electric Twin, Simile, Artificial Societies).
Toutes nos idées exploitent ce trou : nous avons les baselines, les plafonds de retest et le préenregistrement.

## 2. Huit idées d'études

### B1. « Le 95 % offert : ce que la distribution uniforme obtient sur les métriques commerciales »

- **Affirmations visées** : 1-MAE de 95,5 % et NDAM de 92 % (Electric Twin) ; 94 à 95 % (Kantar) ; recouvrement de 86 %
  (Artificial Societies) ; 88 % (Evidenza) ; écart de 0,07 écart-type (Qualtrics). Sources en section 1.
- **Pourquoi c'est important** : ces chiffres sont lus comme des pourcentages de bonnes réponses. Un 1-MAE moyenné sur les
  options est mécaniquement proche de 1. Sur un item à 5 options réparti [0,10 ; 0,20 ; 0,30 ; 0,25 ; 0,15], la
  distribution uniforme fait déjà 94 %. Personne n'a publié la **zone gratuite** de ces métriques.
- **Test en moins de 48 h**, presque sans appel de modèle : sur Twin-2K-500 (items catégoriels, retest vague 4), le panel
  GSS 2016-2020 et le SCE, on calcule les métriques telles que définies publiquement (1-MAE, 1 − TVD comme « overlap »,
  écart des moyennes en écarts-types, et une reconstruction documentée de la NDAM) pour :
  - B0, l'uniforme ;
  - B1, la marge nationale d'une **autre** vague ;
  - B2, la marge du sous-groupe démographique d'une autre vague ;
  - B3, un LLM sans persona (un appel par item, Qwen3 local) ;
  - B4, un LLM avec persona (sorties existantes `data/twin2k500/llm/*.csv`).
  
  Plafond : split-half et retest humain. On rapporte la **part informative** = (score − B1) / (plafond − B1).
- **Prédiction** [HYPOTHÈSE] : B0 obtient au moins 88 % de 1-MAE médian sur les items à 4 options ou plus. B1 dépasse
  95 %. B4 capte moins de 30 % de la distance entre B1 et le plafond. L'écart en écarts-types de B1 reste sous 0,10.
- **Nouveauté** : Chen et al. (2607.26348) comparent l'exactitude à une table démographique, sans passer par les métriques
  commerciales elles-mêmes. Ce « traducteur de promesses » est, à notre connaissance, inédit.
- **Risque** : faible. Il ne faut surtout pas conclure que « 95,5 % ne vaut rien » chez un vendeur donné, car ses items
  diffèrent. Conclusion admissible : la métrique ne discrimine pas, et sans baseline naïve publiée le chiffre est
  ininterprétable. Un risque technique existe aussi : la NDAM est sous-définie, et on publiera la reconstruction.

### B2. « Spearman médian 0,90 : l'enquête de l'an dernier fait aussi bien »

- **Affirmations visées** : Spearman médian de 0,90 sur 53 questions et écart de 7,1 points (Aaru pour EY) ; « 95 % de
  corrélation » (Evidenza pour EY) ; 0,87 (Evidenza pour Dentsu).
- **Pourquoi c'est important** : sur une question à k options, la corrélation de rang est quasi binaire. À k = 3, ρ ne
  prend que les valeurs {1 ; 0,5 ; −0,5 ; −1}. À k = 5, ρ ≥ 0,9 correspond à l'identité ou à une permutation adjacente, soit
  5 ordres sur 120. Une médiane de 0,90 peut donc signifier « l'option majoritaire, et à peu près l'ordre, sont retrouvés »,
  ce qu'une enquête ancienne fait très bien.
- **Test en moins de 48 h** : on calcule les deux lectures possibles (ρ entre options dans chaque question, et r entre
  proportions sur l'ensemble des items). Données : GSS panels 2006, 2008, 2010 et 2020 (prédire une vague par la
  précédente), SCE (2024 prédit 2025), Twin-2K-500. Prédicteurs : marge d'une autre vague, marge d'un autre sous-groupe, LLM
  sans persona, LLM avec persona. On ajoute la distribution de ρ sous permutation aléatoire des options, par k.
- **Prédiction** [HYPOTHÈSE] : la marge d'une autre vague atteint un ρ médian d'au moins 0,85 et un écart moyen d'au plus
  5 points. Le LLM sans persona atteint au moins 0,75. Sur les items à 3 options ou moins, ρ = 1 pour au moins 70 % des
  items avec la marge décalée.
- **Nouveauté** : aucune analyse trouvée de la corrélation médiane comme métrique de validation d'enquête synthétique.
- **Risque** : faible. La définition exacte d'Aaru est inconnue, d'où les deux lectures testées et le conditionnel dans
  toute conclusion. EY a publié ses propres pages, on s'y tient.

### B3. « 85 % du plafond humain, dont 70 % sans rien simuler »

- **Affirmations visées** : 85 % de la réplication humaine (Simile, Park et al. 2411.10109) ; 95 % de l'autoréplication
  (Artificial Societies) ; « à 2 points du bruit humain » (Electric Twin).
- **Pourquoi c'est important** : le ratio « exactitude / retest » est devenu l'unité marketing du secteur. Le dénominateur
  (retest bas sur les items bruités) gonfle le ratio, et le numérateur n'est jamais comparé à une réponse sans personne.
- **Test en moins de 48 h**, zéro appel : sur les sorties locales des 1 052 agents de Stanford (`data/osf-t6g7k-stanford/figure2`)
  et sur Twin-2K-500 vague 4, on applique la **formule du vendeur** à :
  - le mode de l'item donné à tout le monde ;
  - le mode du segment âge × sexe × race × parti, calculé en leave-one-out ;
  - le PMM ;
  - le persona permuté dans son segment.
  
  On rapporte aussi la part d'items où le ratio dépasse 1, et les intervalles par bootstrap sur les personnes.
- **Prédiction** [HYPOTHÈSE] : le mode d'item atteint au moins 0,70 normalisé sur le GSS, le mode de segment au moins
  0,76. L'apport propre des agents à entretien serait donc de 0,09 à 0,15 point sur l'échelle « gratuit → plafond ». Plus de
  10 % des items dépassent un ratio de 1.
- **Nouveauté** : **collision partielle** avec Ahn et al. (2608.29455, moyenne d'item) et avec Park et al., qui rapportent
  déjà 0,74 pour les agents démographiques. Le neuf est la traduction systématique du ratio commercial sur trois jeux, ce
  qui en fait un compagnon de B1 plutôt qu'un article seul.
- **Risque** : faible. Park et al. sont des académiques qui publient eux-mêmes leur baseline démographique. Le ton reste
  celui de la réanalyse respectueuse.

### B4. « Individuel en vitrine, segment en coulisses »

- **Affirmation visée** : chaque répondant synthétique « imite une réponse individuelle, pas la moyenne d'un segment »
  (Toluna, URL en section 1). Même promesse implicite dans « digital twins of real consumers » (Simile).
- **Pourquoi c'est important** : c'est l'argument de vente qui justifie des personas riches, construites sur des données
  de panel. Il est testable par la seule méthode, sans le produit.
- **Test en moins de 48 h** : on réutilise la machinerie C2 (permutation conditionnelle au segment) sur Twin-2K-500, avec
  des personas du **type décrit** (démographie, psychographie, habitudes de consommation, blocs présents dans Twin), les
  sorties GPT-4.1-mini existantes et Qwen3 local. Statistique : gain de l'appariement correct sur le persona permuté dans son
  segment, en pourcentage du même gain calculé sur le retest humain (vague 4), plus le taux de compression de la variance
  entre personnes à l'intérieur du segment.
- **Prédiction** [HYPOTHÈSE] : le gain atteint au plus 15 % du gain humain, soit au plus 1,5 point d'exactitude. La
  variance intra-segment est comprimée d'au moins 40 %.
- **Nouveauté** : **collision sérieuse** avec Ahn et al., Wang et al. (2609.07987) et Peng et al. (2509.19088), comme le
  note la veille. Restent neufs le cadrage « vérification d'une promesse commerciale explicite » et la permutation
  conditionnelle. Coût marginal quasi nul, puisque C2 est déjà écrit.
- **Risque** : moyen si le nom Toluna apparaît près du résultat. On cite la promesse comme exemple d'une pratique répandue,
  jamais comme cible, et on ne teste pas HarmonAIze.

### B5. « La cloche vient de l'embedding, pas du consommateur »

- **Affirmation visée** : la méthode SSR atteint « 90 % de la fiabilité test-retest » avec une similarité KS supérieure à
  0,85 (PyMC Labs et Colgate, arXiv 2510.08338). Elle est reprise dans les guides du secteur (« up to 90% alignment »,
  https://www.pymc-labs.com/blog-posts/synthetic-consumers-a-practical-guide).
- **Pourquoi c'est important** : SSR corrige la pauvreté des Likert directs en projetant un texte libre sur cinq ancres par
  similarité d'embeddings. Or une moyenne de similarités normalisées produit **par construction** une distribution étalée
  et en cloche. Le réalisme distributionnel peut donc venir de l'outil de mesure, pas du modèle simulé.
- **Test en moins de 48 h** : code SSR ouvert et un modèle d'embedding local, sur les items Likert de Twin-2K-500
  (distributions humaines et retest). Conditions :
  - SSR sur le texte libre produit avec persona ;
  - SSR sur un texte neutre **identique pour tous** (« ça dépend, je ne sais pas trop ») ;
  - SSR sur le texte d'une **autre** question ;
  - Likert numérique direct ;
  - distribution uniforme.
  
  Métriques : similarité KS par item, et taux d'atteinte de corrélation sur les moyennes d'item, normalisé par le retest.
  On mesure aussi la sensibilité aux six jeux d'ancres.
- **Prédiction** [HYPOTHÈSE] : le texte constant et le texte hors sujet obtiennent chacun une similarité KS d'au moins 0,80,
  donc au moins 80 % du « réalisme » de la condition complète. Le taux d'atteinte de corrélation est nul par construction
  pour le texte constant et d'au plus 0,3 pour le texte hors sujet. Changer de jeu d'ancres déplace la moyenne d'au moins
  0,3 point d'échelle sur au moins un quart des items.
- **Nouveauté** : aucune ablation publique de SSR trouvée (recherche du 11 septembre 2026). La portée est hors domaine :
  pas de concepts produits, ce qui est dit.
- **Risque** : faible. Méthode et code ouverts, auteurs de culture recherche ; présenter comme une ablation et les
  contacter si l'utilisateur l'autorise.

### B6. « Prédire ou se souvenir ? Le test de la date de coupure »

- **Affirmations visées** : « prédit la primaire de New York à 371 voix près » et « les sondages disparaîtront » (Aaru,
  Semafor et Silver Bulletin) ; prévisions de résultats trimestriels (Simile, presse) ; simulation « à l'aveugle » (Aaru
  pour EY). L'aveugle porte sur les résultats de l'enquête, pas sur ce que le modèle a lu du monde en 2025.
- **Pourquoi c'est important** : une simulation qui réussit avant la date de coupure du modèle peut réciter plutôt que
  prédire. Aucune validation commerciale lue ne sépare les deux régimes.
- **Test en moins de 48 h** : SCE mensuel de 2020-01 à 2025-10 (environ 1 200 répondants par mois ; côté humain déjà
  préparé en C1). Deux ou trois modèles à date de coupure documentée (Qwen3 local, un ou deux modèles OpenRouter).
  Persona = démographie SCE + mois de l'enquête ; items : anticipations d'inflation à un an et deux items centraux.
  Comparaison à la **persistance** (distribution humaine du mois précédent), avant et après la coupure de chaque modèle,
  en différence de différences. Témoin de fuite : dire au modèle « nous sommes en 2019 » et vérifier si la poussée de
  2021-2022 apparaît quand même. Ordre de grandeur : 60 mois × 200 personas × 2 modèles, soit 24 000 appels, surtout en
  local.
- **Prédiction** [HYPOTHÈSE] : avant la coupure, la médiane mensuelle synthétique suit la vérité avec r ≥ 0,7. Après la
  coupure, r ≤ 0,3 et l'erreur dépasse d'au moins 50 % celle de la persistance. La différence de différences a un
  intervalle qui exclut 0. Le témoin « 2019 » laisse fuir la poussée d'inflation.
- **Nouveauté** : la fuite temporelle est documentée en prévision générale (« Simulated Ignorance Fails », 2601.13717 ;
  2510.02340). Rien trouvé sur les enquêtes synthétiques avec baseline de persistance.
- **Risque** : faible sur le juridique. Médiatiquement très fort, donc à ne pas surinterpréter : un seul domaine (les
  anticipations économiques), et aucune élection testée.

### B7. « Plus savant que les gens : les personas ne reproduisent pas nos erreurs »

- **Affirmations visées** : les personas « raisonnent, ont des perspectives distinctes » (Toluna) ; « remplacer les focus
  groups » (Simile, presse : https://ai2.work/startups/simile-raises-100m-to-replace-focus-groups-with-ai-digital-twins-2026/) ;
  « prédire comment les audiences réagissent » (Electric Twin, Artificial Societies).
- **Pourquoi c'est important** : un focus group sert à mesurer ce que les gens **croient**, y compris quand c'est faux.
  Un simulateur qui connaît les faits échoue exactement là où la croyance humaine diverge de la réalité.
- **Test en moins de 48 h** : on reprend la machinerie du programme A (a46 pour le référent humain, r1 pour le modèle).
  Ahler et Sood : les Américains surestiment en moyenne de 4,4 fois la part des groupes stéréotypés dans chaque parti. On
  compare trois termes (vérité, perception humaine par camp, perception synthétique par camp) avec des personas YouGov
  démocrates et républicaines, en local et sur un modèle OpenRouter.
- **Prédiction** [HYPOTHÈSE] : le ratio synthétique de surestimation reste sous 2,5, contre 4,4 chez les humains ; les
  personas sont trop près des faits. En revanche, l'écart de perception entre les deux camps est gonflé d'au moins 2 fois
  par rapport à l'écart humain (même sens que Chen et al.).
- **Nouveauté** : fidélité aux croyances de second ordre, contre fidélité aux opinions. L'antériorité sur les
  « misperceptions » simulées par LLM reste **à vérifier** : aucune recherche dédiée n'a été faite ici.
- **Risque** : faible. Seul risque de méthode : ancrage numérique et refus de répondre, à contrôler.

### B8. « Tout est significatif : le taux de faux positifs des tests de messages synthétiques »

- **Pratique visée** : tester idées, messages et concepts sur des milliers de répondants synthétiques en quelques heures
  (Electric Twin, page d'accueil ; Qualtrics : « test concepts in hours » ; plus de 80 % sur la performance de posts chez
  Artificial Societies).
- **Pourquoi c'est important** : de gros n synthétiques à variance comprimée rendent toute différence « significative ».
  Des décisions de campagne se prennent sur ces tests.
- **Test en moins de 48 h** :
  - 20 paires de messages **nuls** (paraphrases de même sens, validées à l'aveugle par deux codeurs de l'équipe) ;
  - 5 témoins positifs dont l'effet humain est connu : l'effet de correction d'Ahler et Sood et les cinq expériences de
    Camerer répliquées par Park et al. (`data/osf-t6g7k-stanford/camerer_five_studies`) ;
  - 500 répondants synthétiques par bras, Qwen3 local, test t standard, puis test par permutation de Helm et Priebe.
- **Prédiction** [HYPOTHÈSE] : au moins 40 % de faux positifs à α = 0,05 sur les paires nulles, pour 5 % nominal. Les d de
  Cohen des témoins positifs valent au moins 2 fois l'effet humain. Le test de Helm et Priebe ramène les faux positifs à
  10 % ou moins, au prix d'une perte de puissance à chiffrer.
- **Nouveauté** : Helm et Priebe (2605.27463, mai 2026) montrent **en théorie** que les tests standards sont invalides
  sous perturbation de prompt et proposent un test par permutation. Lukauskas et Šarkauskaitė (2608.14606) trouvent des
  médiations placebo fabriquées dans 3 cas sur 10. Notre apport serait un taux empirique sur un scénario réaliste de test de
  messages, calibré par des effets humains connus.
- **Risque** : faible ; on vise une pratique, pas un vendeur.

## 3. Antériorité : qui a déjà audité ces promesses ?

- **AAPOR, Task Force on Responsible AI Integration in Survey Research** (mai 2026) : cadrage des risques, variance
  sous-estimée des échantillons synthétiques. Pas de test des affirmations des vendeurs.
  https://aapor.org/wp-content/uploads/2026/05/Responsible-AI-Integration-In-Survey-Research.pdf
- **ESOMAR** : « 20 Questions to Help Buyers of AI-Based Services » et guide d'achat pour les données synthétiques
  augmentées (seuil de données minimales viables). Ce sont des questionnaires, pas des mesures.
  https://esomar.org/20-questions-to-help-buyers-of-ai-based-services
- **Verasight, Synthetic Sampling Reports I à IV** (2025-2026) : c'est l'audit **empirique** côté industrie le plus proche.
  Un échantillon humain de 2 000 adultes est confronté à des échantillons synthétiques appariés, avec des MAE jusqu'à
  33 points sur les questions d'expérience personnelle. Il teste la méthode générique, pas les métriques des vendeurs, et
  Verasight vend des panels humains (conflit d'intérêts). https://www.verasight.io/reports/synthetic-omnibus-survey
- **Journalisme** : « AI polls are fake polls » (Silver Bulletin, 11 avril 2026, sur Aaru et Electric Twin) est une
  critique argumentée sans test. S'y ajoute une critique d'Aaru et du WSJ
  (https://www.thevoiceofuser.com/aaa-billion-dollar-ai-startup-is-selling-you-a-survey-the-wall-street-journal-wrote-a-love-letter-about-it/).
  **Aucun test journalistique chiffré trouvé.**
- **Vendeurs qui s'auditent eux-mêmes** : Qualtrics réplique Paxton et Yang (Greenbook). Sameulation vend des scores
  d'audit et cite un GSS à 0,588 contre 0,589 pour une table démographique, visiblement repris de Chen et al. Conflit
  d'intérêts dans les deux cas. La MeasuringU Review of Experiments with Synthetic Users est une revue et non un audit.
- **Académique, « synthetic respondents fail »** : Chen, Zhu et Zheng (2607.26348), pour qui aucun LLM ne bat la baseline
  démographique ; Peng et al., *Funhouse Mirrors* ; Ahn et al., *Item-Mean Surrogates* ; Bisbee et al. 2024 ; Lukauskas et
  Šarkauskaitė (2608.14606) ; Helm et Priebe (2605.27463). Aucun ne recalcule **les métriques commerciales elles-mêmes**
  (1-MAE, recouvrement, Spearman médian, pourcentage d'autoréplication) contre baselines gratuites et plafonds de retest.
- Hors sujet malgré le titre : l'audit « 42 lignes, 9 vendeurs » de Digital Applied (août 2026) porte sur les benchmarks de
  LLM (OpenAI, Anthropic et d'autres), pas sur la recherche synthétique. Il reste un bon modèle de format pour un audit de
  divulgation.

**Audit existant le plus proche** : Verasight (Reports I à IV) côté industrie, et Chen et al. 2607.26348 côté académique.
Aucun ne confronte les chiffres publiés par les vendeurs à la zone gratuite de leur propre métrique.

## 4. Ordre suggéré

1. **B1 + B2 + B3 en un seul papier court, « traducteur de promesses »** : quasi zéro appel de modèle, moins de 24 h, le
   meilleur rapport visibilité sur risque. Titre indicatif : *What does "95% accurate" mean? Free baselines and retest
   ceilings for synthetic-audience metrics*.
2. **B8**, puis **B5** : des pratiques ou méthodes ouvertes, un résultat net et médiatisable, un risque juridique faible.
3. **B6** : le plus fort médiatiquement, à cadrer strictement sur un seul domaine.
4. **B4** et **B7** réutilisent C2, a46 et r1 : coût marginal faible, nouveauté partielle (B4) ou à vérifier (B7).
