# Veille d'antériorité avant soumission, 11 septembre 2026

Question : l'article répète-t-il des résultats publiés ? Lecture seule du dépôt ; web en lecture. Environ 45 requêtes
(moteur généraliste, arXiv, ACL Anthology, OpenReview, PMC, Cambridge). Tous les travaux cités ont été ouverts : résumé
pour tous, sections clés pour 2608.29455 (PDF intégral, passages persona swap et plafond), 2609.07987 (HTML), 2509.19088
(HTML) et 2411.10109 (PDF, recherche de mots). Chiffres locaux vérifiés dans la matrice, `tab-resultats.md`, t1
(28 % de variance partagée, l. 68 et 442), a13 (erratum E1, facteur 13,5) et r5 (λ = 0,79 [0,60 ; 0,97]).
Limites : pas d'accès direct à Google Scholar, SSRN ni PsyArXiv hors du moteur ; les HTML de 2609.07987 et 2606.28963
ont été lus par extraction résumée. Revérifier leurs citations mot à mot avant de les reprendre dans l'article.

**Alerte principale, absente du corpus local.** Ahn, Mao et Lee (2608.29455) contiennent un *Persona Swap Control*.
Ils réassignent les personas entre répondants à l'intérieur de chaque étude, 10 000 fois, sur la Megastudy de Peng et al.
construite sur le panel Twin-2K-500. Ils rapportent le résultat au plafond de retest Twin-2K-500, rtt = 0,536. Le
dépôt ne cite ce papier que pour « la moyenne d'item », et `grep "persona swap"` ne renvoie rien dans `resultats/` ni `corpus/`.

## 1. Collisions par revendication

| Rev. | Classement | Travaux en collision (ouverts) | Ce qui est identique | Ce qui reste à nous, précisément |
|---|---|---|---|---|
| C1 | **PARTIELLEMENT FAIT** | Wang, Hunt, Tang, Joseph 2609.07987 ; Choi et al. 2606.28963 ; Chen, Zhu, Zheng 2607.26348 ; Wang H. et al. (LifeMem) 2608.19621 ; Grief-Albert et al. 2608.03044 ; Bisbee et al. 2024 ; Wang, Morgenstern, Dickerson 2402.01908 ; Xie et al. PNAS 2026 | Le principe « séparer les objets de fidélité, car l'agrégat masque le reste » est publié : quatre dimensions chez Wang et al., trois axes chez Choi et al. (CCC 0,80 contre r individuel 0,31). Le gonflement inter-groupes (2 à 4 fois chez Chen et al., environ 2 fois chez Grief-Albert et al.) et la compression intra (LifeMem, Bisbee, Wang et al. 2024) le sont aussi. | Les trois termes (intra, inter, erreur au référent) sur les mêmes personnes et items, chacun rapporté à un plancher humain de retest. Aucun des papiers ouverts ne rapporte les termes de groupe à un retest : Choi et Wang et al. n'en ont pas, Grief-Albert non plus selon a26. Le contre-exemple chiffré (moins d'un point d'exactitude, facteur 13,5 sur l'inter) reste neuf, mais c'est une réanalyse (a13). |
| C2 | **PARTIELLEMENT FAIT, collision sérieuse** | Ahn, Mao, Lee 2608.29455 ; Wang et al. 2609.07987 ; Peng et al. 2509.19088 ; Park et al. 2411.10109 ; Hwang, Majumder, Tandon 2305.14929 | Même logique de test (réassigner les personas et vérifier que l'appariement correct fait mieux), même panel Twin-2K-500, même normalisation par le retest Twin. Wang et al. écrivent qu'un vecteur synthétique « randomly reassigned across people » pourrait reproduire la distribution et l'effet, puis mesurent un signal apparié résidualisé (médiane \|ρ\| 0,028). Park et al. : agents démographiques à 0,74 contre 0,85 normalisé, sans permutation (vérifié). | (a) Permutation **conditionnelle au segment**, qui conserve les marges, contre permutation intra-étude chez Ahn. (b) Le retest humain lui-même permuté comme témoin positif (−45,6 %) et des témoins aveugles à la personne à ~0. (c) Treize configurations publiées comparées, avec 28 % de variance partagée avec l'exactitude. **À réconcilier explicitement** : « 42–71 % du plancher » (chute d'exactitude brute) paraît contredire leurs « 5,7 % du plafond » (R² après retrait de la moyenne d'item). Un relecteur le relèvera. |
| C3 | **NEUF à notre connaissance** (forme exacte) | Plus proches : Wang et al. 2609.07987, qui ne sélectionnent explicitement aucune spécification (« We do not choose a preferred specification ») ; Hullman et al. 2602.15785 ; Peng et al. 2509.19088 | Idée voisine publiée : la fidélité agrégée ne garantit pas la substituabilité, et un persona riche n'améliore pas l'exactitude par rapport aux démographies (0,748 contre 0,746). | Aucun test trouvé où un diagnostic de correspondance, résidualisé contre l'exactitude, sélectionnerait un simulateur sur un bloc A et serait jugé sur un bloc B tenu à l'écart. Requêtes : « validating LLM survey simulators predictive validity held-out … selection », « choosing among LLM persona simulators out-of-sample validation », « digital twin … does not predict … select configuration held-out », « validity of LLM social simulation benchmarks metric predicts downstream use ». Portée étroite : 7 candidates, un seul jeu, levier L15. Le constat « LLM riches meilleurs que PMM sur B » va contre Peng et al. (jumeaux ≈ XGBoost entraîné sur ~75 humains en exactitude) et contre Chen et al. (« No LLM beats even the strongest baseline »). Il reste descriptif et ne doit pas être mis en avant sans cette discussion. |
| C4 | **PARTIELLEMENT FAIT** | Meister, Guestrin, Hashimoto, NAACL 2025 (2411.05403) ; Jang, Lee, Kim 2607.25292 ; Grief-Albert et al. 2608.03044 ; Choi et al. 2606.28963 | « L'élicitation compte » : le few-shot bat le persona chez Meister et al., décrire n'est pas échantillonner chez Jang et al. et Meister et al., un plan 2×2 few-shot contre zero-shot existe chez Choi et al. (où le few-shot dégrade la structure). | La décomposition gabarit contre trois exemples à poids constants, sur l'écart inter-camps rapporté au référent humain (λ = 0,79). Un seul modèle (Qwen3-4B), un seul jeu (GSS), ancrage numérique non exclu : matière pour une annexe ou une note, pas un article. |
| C5 | **DÉJÀ FAIT** (le constat) ; résultat local négatif sans nouveauté | Hu et al., SimBench, ICLR 2026 (2510.17516) ; Jang et al. 2607.25292 ; Karouzos, Tan, Aletras 2604.16027 | Les différences entre base et post-entraînés, et la dégradation par étape, sont publiées. Karouzos et al. attribuent l'effondrement de diversité à des étapes sur trois lignées **documentées** d'Olmo 3 : la condition « attribution possible avec lineage » est déjà remplie ailleurs. | Rien de publiable seul. « Pas de trajectoire, pas d'attribution sans lineage » est une précaution de méthode, à placer en limite. |
| C6 | **PARTIELLEMENT FAIT, largement anticipé** | Chen et al. 2607.26348 ; Peng et al. 2509.19088 ; Ahn et al. 2608.29455 ; Jia et al. 2605.10659 ; Bojic et al. 2604.19787 | Au niveau individuel, les baselines statistiques égalent ou battent les LLM : XGBoost chez Peng et al., moyenne d'item leave-one-out (r 0,34 contre 0,45) chez Ahn et al., classifieur TF-IDF chez Bojic et al. Les personas sont « worst for … rare responses » chez Jia et al. | Seul le régime précis reste à nous : réponses rares **stables**, information égale, famille d'items retirée, PMM et tirage de segment. L'effet est non significatif (R2 : +0,03 [−0,04 ; +0,10] contre tirage ; R2b adaptatif) et en tension avec le constat descriptif de C3. |
| C7 | **DÉJÀ FAIT** | Atil et al. 2408.04667 ; Messina & Scotta, TMLR 2026 (2604.22411) ; Bisbee et al., *Political Analysis* 32(4), 2024 ; Barrie, Palmer, Spirling, « Replication for Language Models » (AJPS, acceptation conditionnelle) ; Ahn et al. 2608.29455, préenregistré sur l'OSF en février 2026 | Non-déterminisme à T = 0 (jusqu'à 15 points d'écart chez Atil et al., « background temperature » chez les grands fournisseurs), dérive dans le temps (Bisbee et al., avril contre juillet 2023), préenregistrement déjà pratiqué dans ce sous-champ. | Le chiffre DeepSeek/DigitalOcean (1 distribution identique sur 10) : une ligne de méthode, pas une contribution. |

## 2. Les cinq travaux les plus menaçants

1. **Ahn, D., Mao, C., Lee, D. (2026). *Item-Mean Surrogates: Why Richer Persona Data Fail to Improve LLMs as Human
   Surrogates*.** arXiv 2608.29455, 29 août 2026, préenregistré. https://arxiv.org/abs/2608.29455 — Permutation des
   personas (10 000 tirages), plafond de retest Twin-2K-500, baseline moyenne d'item, revue de 63 papiers et « quatre
   tests » proposés. Touche C2 de plein fouet, ainsi que C1 et C6. Le cadrage « nous proposons un test de
   correspondance à la personne » est pris.
2. **Wang, S., Hunt, K., Tang, S., Joseph, K. (2026). *When Can LLM Digital Twins Reduce Human Measurement? From
   Behavioral Fidelity to Statistical Substitutability*.** arXiv 2609.07987, 7 septembre 2026.
   https://arxiv.org/abs/2609.07987 — Twin-2K-500, dissociation entre fidélité agrégée et signal apparié, argument de la
   réassignation. Touche C1 et C2, et borde C3 (substituabilité, sans test de sélection).
3. **Peng, T., Gui, G., Brucks, M., Merlau, D. J., Fan, G. J., et al. (2025–2026). *Digital Twins as Funhouse Mirrors:
   Five Key Distortions*.** arXiv 2509.19088 v5 ; paru dans *Science Advances*. https://arxiv.org/abs/2509.19088 —
   19 études préenregistrées sur le panel Twin-2K-500, individuation insuffisante, persona complet ≈ démographique,
   équivalent XGBoost. Touche C2, C6 et le constat de C3.
4. **Chen, Z., Zhu, D., Zheng, L. N. (2026). *When Synthetic Users Fail: A Cross-Domain Benchmark of LLM-Simulated Human
   Survey Responses*.** arXiv 2607.26348. https://arxiv.org/abs/2607.26348 — GSS et WVS : écarts de groupe gonflés de
   2 à 4 fois, aucun LLM au-dessus de la meilleure baseline individuelle. Touche C1 et C6.
5. **Choi, E. C., Kim, Y., Pugalenthi, P., Chen, H.-E., Huang, B.-R. (2026). *Beyond the Mean: Three-Axis Fidelity for
   Aligning LLM-Based Survey Simulators from Small Pilot Data*.** arXiv 2606.28963, atelier Pluralistic Alignment
   @ ICML 2026. https://arxiv.org/abs/2606.28963 — Axes structurel, marginal et individuel ; dissociation chiffrée ;
   plan few-shot 2×2. Touche C1 et C4.

Déjà connus du dépôt et toujours pertinents : Hu et al. (SimBench, ICLR 2026), Grief-Albert, Bo, Jiao, Anderson
(2608.03044, EMNLP Findings 2026), Zhang, Xu, Zhang (2609.00565, EMNLP Findings 2026), Jang, Lee, Kim (2607.25292,
EMNLP Findings 2026), Park et al. (2411.10109), Xie et al. (PNAS 2026, doi 10.1073/pnas.2538145123), Toubia et al.
(Twin-2K-500, 2505.17479).

## 3. Verdict global

**Ridicules ? Non. Redondants ? Oui, si l'article garde le cadrage de la matrice.** Un article intitulé en substance
« la fidélité de groupe et la correspondance à la personne se dissocient ; voici un test par permutation normalisé au
retest » arriverait après Ahn et al. (29 août) et Wang et al. (7 septembre), qui disent l'essentiel sur le même panel.
Un relecteur ayant lu ces deux papiers le jugerait incrémental, voire tardif. C4, C5, C6 et C7 ne portent pas un
article : C5 et C7 sont déjà faits ; C4 et C6 sont locaux, sur un modèle ou un régime, et C6 est non significatif.

**Ce qui reste réellement neuf et publiable :**
1. **C3, résultat négatif préenregistré** : un diagnostic de signal individuel, du type de ceux que proposent Ahn et al.
   et Wang et al., n'aide pas à choisir un simulateur au-delà de l'exactitude ; il fait même un peu pire sur un bloc
   tenu à l'écart. C'est une réponse directe à la question ouverte par ces deux papiers.
2. **Une précision méthodologique sur C2** : ce que la permutation **conditionnelle au segment** identifie par rapport à
   la permutation intra-étude, avec retest humain permuté comme témoin positif et témoins aveugles à ~0. S'y ajoute la
   réconciliation chiffrée avec les « 5,7 % du plafond » d'Ahn et al. (chute d'exactitude brute contre R² après retrait
   de la moyenne d'item).
3. En appui seulement : trois termes de groupe rapportés à un plancher de retest (C1), et la décomposition gabarit contre
   exemples (C4) en annexe.

**Format recommandé : note courte, méthodologique et résultat négatif** (atelier ACL/EMNLP/NeurIPS sur la simulation
sociale ou l'évaluation, ou article court en Findings). Titre indicatif : *Does person-matching signal help choose an
LLM survey simulator? A preregistered held-out test on Twin-2K-500*. Pas un article long de « nouvel instrument ».

**Cadrage qui évite la redite :**
- Citer Ahn et al. comme **auteurs du test par permutation de persona** et Wang et al. comme **auteurs de la
  dissociation agrégat / signal apparié**. Notre place est la question suivante : ce signal sert-il à décider ? Réponse
  préenregistrée : non, dans ce périmètre.
- Présenter la permutation conditionnelle comme une variante justifiée, pas comme une invention. Montrer sur les mêmes
  données les deux permutations (intra-étude et intra-segment) et nos deux métriques, et publier la réconciliation.
- Déclasser explicitement le constat « LLM riches > PMM sur B » (descriptif, contraire à Peng et à Chen) et les limites
  de C3 : 7 candidates, point de levier L15, un seul jeu.
- Retirer de l'abstract les formules « nous montrons que l'élicitation compte », « la base diffère de l'instruit » et
  « l'API n'est pas déterministe à T = 0 ». Ce sont des méthodes et des limites, pas des résultats.
