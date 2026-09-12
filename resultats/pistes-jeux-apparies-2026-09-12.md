# Pistes A/B tranchées + seconde chasse sous angles neufs (12 septembre 2026)

Reprend `resultats/chasse-jeux-apparies-2026-09-12.md` (qui laissait les pistes A et B
**[NON VÉRIFIÉ]**), `resultats/troisieme-jeu-2026-09-12.md` et
`resultats/inventaire-donnees-2026-09-12.md`. Recherche web en lecture seule uniquement ;
aucun compte créé, aucun formulaire rempli, rien téléchargé dans `data/`. Les PDF complets
d'arXiv 2609.07987 et 2606.28963 ont été récupérés via WebFetch (mise en cache locale
temporaire hors dépôt) puis lus intégralement page par page avec l'outil de lecture PDF.

---

## Tâche 1 — Piste A : Wang, Hunt, Tang & Joseph (2026), arXiv 2609.07987

**« When Can LLM Digital Twins Reduce Human Measurement? »**, Steven Wang, Kyle Hunt,
Shaojie Tang, Kenneth Joseph — University at Buffalo.

### Appariement individuel : **CONFIRMÉ méthodologiquement**, pas seulement affirmé en notation
La section 3.3.2 (« Moore-Berg extension ») décrit noir sur blanc la construction : « We
generate source predictions for the Moore-Berg respondents... The party-only target prompt
supplies only party affiliation. The common-fields prompt supplies a structured profile...
Nine fields are available in both the Moore-Berg and Twin-2K samples. » Le papier calcule
ensuite, **par répondant réel de Moore-Berg et par modèle**, une corrélation résidualisée
ρ_S = Corr(Y − E[Y|T], Ŷ − E[Ŷ|T]) (Éq. 4) — reportée par exemple en Table F.1 (« Dem MP »,
« Dem MD », « Rep MP », « Rep MD » pour six modèles, ex. GPT-5.4 : 0.256/0.187/0.235/0.212).
Cette statistique **ne peut pas être calculée sans un fichier appariant, ligne à ligne,
la vraie réponse Y_i d'un répondant Moore-Berg réel et la prédiction Ŷ_i générée
spécifiquement pour ce même répondant** par les six modèles testés. Ce n'est donc plus
une simple citation de notation (comme le disait la chasse précédente) : c'est un résultat
empirique chiffré qui prouve l'existence du fichier apparié en interne.

### Données publiquement accessibles : **NON, pas le fichier apparié individuel**
- Appendice D (« GenAI Use Documentation ») donne un dépôt : **repository anonymisé
  `https://anonymous.4open.science/r/llm_digital_twin_stat_sub`** (accès en lecture seule
  confirmé aujourd'hui via son API JSON publique, `curl -A "Mozilla/5.0" .../api/repo/.../files`).
  Nom réel du projet : **« Twin-PPI »**. Contient scripts (`14_...` à `47_...`), prompts,
  et sorties agrégées.
- Le README du dépôt est explicite sur ce qui **n'est pas** suivi par Git : « The repository
  `.gitignore` excludes raw/local data, credentials, virtual environments, model directories,
  `.sav` files, logs, and most generated outputs. In particular, **do not commit** API keys,
  Hugging Face tokens, **respondent-level raw data**, model weights, or other restricted
  data. » et : « `external_data/`, `hf_twin2k/`, model weights, and other local/raw inputs
  are intentionally ignored by Git. »
- Constat direct par listage de l'arborescence réelle (`outputs/model_comparison/`,
  `outputs/moore_berg_mdiff_weighted_power_ppi_qwen35_27b/`, `outputs/paper/`) : **tous les
  fichiers présents sont des agrégats** (par modèle, par estimande, par budget de labels) —
  `source_replication_by_model_estimand.csv`, `moore_berg_survey_only_budget_ppi_by_estimand.csv`,
  etc. **Aucun fichier individu-par-individu n'est présent dans le dépôt public.**
- Le jeu humain original de Moore-Berg et al. (2020) est sur OSF, nœud **`hnq7j`** (vérifié
  via l'API `api.osf.io/v2/nodes/hnq7j/` : `public: true`, **`node_license: null`** — même
  régime d'absence de licence que Park et al. `t6g7k` déjà signalé dans l'inventaire). Il ne
  contient que les réponses humaines, pas les prédictions LLM de Wang et al.

### Format des réponses : **choix fermé**. Les items reconstruits sont des notes de chaleur/humanité
sur échelle 0-100 (huit questions par répondant), pas du texte libre — compatible avec
l'attaque.

### Licence : CC BY 4.0 pour l'article lui-même (arXiv) ; le code du dépôt anonyme n'affiche
pas de licence distincte constatée aujourd'hui ; le jeu humain source (OSF `hnq7j`) est sans
licence déclarée.

### Ce qu'il faudrait faire concrètement
**Aucune adresse de correspondance n'est publiée dans l'article** — vérifié en lisant la
page de titre (PDF) et la version HTML expérimentale (`arxiv.org/html/2609.07987v1`) : les
quatre auteurs sont listés avec la seule affiliation « University at Buffalo », sans note de
bas de page ni email. Deux voies concrètes, ni l'une ni l'autre déjà faite par cette session
(recherche en lecture seule uniquement) :
1. **Écrire aux auteurs** via leurs adresses professionnelles publiques de l'University at
   Buffalo (ex. la page personnelle de Kenneth Joseph, `kennyjoseph.github.io`, liste un
   contact professionnel), en demandant explicitement le fichier apparié individuel
   Moore-Berg humain + prédictions des six modèles — actuellement exclu du dépôt public par
   choix éditorial (`.gitignore`) et non par indisponibilité technique.
2. Le dépôt étant hébergé en anonyme (probable soumission en cours de révision par les
   pairs), une demande directe aux auteurs reste la seule voie tant que l'identité du dépôt
   GitHub réel n'est pas déanonymisée après publication.
**Verdict : piste tranchée. Appariement individuel réel et vérifié dans la méthode, mais
le jeu de données apparié lui-même n'est pas public aujourd'hui — seuls le code et des
agrégats le sont.**

---

## Tâche 1 — Piste B : Choi, Kim, Pugalenthi, Chen & Huang (2026), arXiv 2606.28963

**« Beyond the Mean: Three-Axis Fidelity for Aligning LLM-Based Survey Simulators from
Small Pilot Data »**, University of Southern California. Correspondance publiée dans
l'article : **Eun Cheol Choi <euncheol@usc.edu>** (note de bas de page 1, page de titre).

### Appariement individuel : **CONFIRMÉ**, sur l'enquête réelle de Lee, Lee & Hwang (2023,
*Health Communication*, Corée du Sud, mai 2020, N=1 466)
Le papier tire un pilote de 5 % (n=74, graine fixée) et évalue sur les **1 392 répondants
réels restants**. L'axe « individual fidelity » (section 3.4) est défini comme : « Does each
simulated respondent track their human counterpart? » et calculé comme r_d =
Pearson(d_i^GT, d_i^sim) et MAE_d = moyenne de |d_i^GT − d_i^sim| **à travers les
répondants** — Table 1 et Table 5 (Annexe B.2) rapportent ces valeurs par sous-ensemble
(discernement, désinformation, vraie information) pour six méthodes (ex. LoRA+MLP :
r_d=0.37, MAE_d=0.61). Comme pour la piste A, ce calcul **exige** un fichier ligne à ligne
appariant chaque répondant réel de Lee et al. (2023) à sa prédiction simulée — ce n'est pas
une supposition, c'est arithmétiquement nécessaire pour produire les nombres publiés.

### Données publiquement accessibles : **NON, aucun dépôt trouvé**
Lecture intégrale des 11 pages du PDF (titre, introduction, méthode, résultats, discussion,
limites, divulgation d'usage de l'IA, références, annexes A et B) : **aucune déclaration de
disponibilité des données, aucun lien GitHub/OSF/Zenodo, aucune section « Data Availability »
ou « Code Availability »** n'apparaît nulle part dans le texte. La section « AI tools usage
disclosure » ne mentionne que l'usage de Claude pour la relecture, pas de dépôt de données.
Recherche web ciblée sur le nom du papier + GitHub : aucun résultat pertinent.

### L'enquête humaine source (Lee, Lee & Hwang 2023) a un supplément en ligne
« Supplemental data for this article can be accessed online at
https://doi.org/10.1080/10410236.2022.2125119 » (Taylor & Francis, payant/sur abonnement
pour l'article complet) — **non vérifié aujourd'hui si ce supplément contient les
microdonnées individuelles brutes** ou seulement des tableaux agrégés/le questionnaire ; ce
supplément ne contiendrait de toute façon pas les prédictions LLM de Choi et al. (2026),
produites indépendamment trois ans plus tard.

### Format des réponses : **choix fermé**. 36 items de croyance (18 désinformation, 18 vraie
information) sur échelle Likert à 4 points (« Not accurate at all » à « Very accurate ») plus
une option « Have not seen it » traitée comme donnée manquante — compatible avec l'attaque.

### Licence : CC BY 4.0 pour l'article (constaté sur la page arXiv).

### Ce qu'il faudrait faire concrètement
Écrire à **Eun Cheol Choi <euncheol@usc.edu>** (adresse publiée dans l'article même,
contrairement à la piste A) pour demander (a) le fichier de pilote/évaluation apparié
utilisé pour calculer r_d et MAE_d, et (b) si les auteurs ont obtenu l'accès aux
microdonnées individuelles de Lee et al. (2023) par une voie propre (les auteurs de Choi et
al. ne sont pas ceux de l'enquête originale).
**Verdict : piste tranchée. Appariement individuel réel et vérifié dans la méthode, format
compatible, adresse de correspondance publiée disponible — mais aucune donnée individuelle
déposée publiquement aujourd'hui ; la voie concrète est la lettre aux auteurs, adresse en
main.**

---

## Tâche 2 — Seconde chasse : nouveaux angles

### Candidat trouvé, appariement confirmé mais accès restreint : Kinzinger & Hartmann (2026),
arXiv 2606.04592, « Synthetic Personalities: How Well Can LLMs Mimic Individual Respondents
Using Socio-Economic Microdata? », TUM School of Management
- **Jeu source** : German Socio-Economic Panel (SOEP), panel allemand de 41 ans, plus de
  28 000 répondants en 2023. Sous-échantillon utilisé : **500 participants réels**, 183
  questions retenues (« held-out »), plus de 2,1 millions de réponses de jumeaux générées
  au total.
- **Appariement individuel confirmé par la métrique même** : « rank-order correlation
  measures whether the twins reproduce who scores higher than whom across participants on
  each question » et l'exemple donné (« a twin who answers 6 to a human's 5 on a 1-to-7
  scale scores 0.833 ») montre un calcul par paire répondant réel/jumeau, item par item.
  Meilleur score : 78,8 % d'exactitude, r=0,590 (corrélation de rang) sur l'ensemble
  d'évaluation SOEP.
- **Format** : échelles numériques/Likert (ex. 1 à 7) — choix fermé, compatible.
- **Accès aux données : NON public.** Le SOEP est un panel à accès contrôlé (fichier
  d'usage scientifique du DIW Berlin, demande d'habilitation nécessaire) — même régime que
  le GSS/NORC déjà écarté dans l'inventaire du 12 septembre pour la même raison (pas de
  redistribution libre). Rien dans les six premières pages lues n'indique que les
  auteurs republient un fichier apparié.
- **Correspondance publiée dans l'article** : **Leonard Kinzinger
  <leonard.kinzinger@tum.de>**, auteur correspondant explicitement désigné en note de bas
  de page 1 de la page de titre.
- **Ce qu'il faudrait faire** : écrire à Kinzinger pour (a) confirmer si un fichier apparié
  est prévu en dépôt public après publication, et (b) vérifier si une habilitation SOEP
  distincte permettrait de reproduire leur pipeline sur les mêmes 500 participants avec
  notre propre génération — au prix, comme déjà noté pour Ahler-Sood/SCE, d'introduire notre
  méthode de génération comme facteur confondu plutôt que de tester un jumeau tiers.
- **Verdict : candidat réel et vérifié en appariement, mais pas plus accessible aujourd'hui
  que Twin-2K-500/Park et al. ne l'étaient avant leur publication — accès contrôlé, pas de
  dépôt individuel public.**

### Écarté : arXiv 2609.07305, « Marginal Fidelity Does Not Establish User Simulation... »
(4 septembre 2026). C'est un article **méthodologique/critique**, pas un jeu de données : il
démontre que l'accord marginal (agrégé) entre populations ne prouve rien sur la simulation
individuelle, mais ne publie ni ne cite de fichier apparié humain/IA propre à l'équipe.
Aucune piste de jeu de données à en tirer.

### Rien trouvé de concluant sur les autres angles demandés
- **Thèses et annexes** (recherches en français et en espagnol, HAL, theses.fr,
  dépôts hispanophones) : aucune thèse trouvée déposant un jeu apparié humain/IA à choix
  fermé au-delà de ce que la littérature arXiv couvre déjà.
- **Panels ayant publié leurs deux côtés** (Prolific, CloudResearch, YouGov) : recherche
  ciblée sans résultat — la littérature compare systématiquement à des données humaines
  existantes sans republier de fichier apparié individuel.
- **Littérature non anglophone** : recherches en français et espagnol infructueuses pour un
  jeu de données propre (uniquement des articles de vulgarisation sur les jumeaux numériques
  industriels, hors sujet).

---

## Récapitulatif et estimation finale

| piste | appariement individuel | données publiques | action concrète |
|---|---|---|---|
| A — Wang et al. (Moore-Berg) | **confirmé** (calcul ρ_S publié) | non (dépôt exclut le respondent-level) | écrire à K. Joseph / S. Wang (UB) |
| B — Choi et al. (Lee et al. Corée) | **confirmé** (r_d, MAE_d publiés) | non (aucun dépôt trouvé) | écrire à euncheol@usc.edu |
| Kinzinger & Hartmann (SOEP) | **confirmé** (rank-order par item) | non (SOEP à accès contrôlé) | écrire à leonard.kinzinger@tum.de |

Trois jeux déjà qualifiés et exploitables aujourd'hui, sans démarche supplémentaire :
Twin-2K-500, OSF `t6g7k` (Park et al.), et l'archive Argyle et al. (Dataverse
`10.7910/DVN/JPV20K`). Au-delà, **mon estimation honnête est qu'il n'existe aujourd'hui
probablement qu'une poignée de jeux au monde (single digits, sans doute 4 à 8) où
l'appariement individuel humain/IA à choix fermé est à la fois réel et immédiatement
téléchargeable sans démarche** — la majorité des papiers qui calculent des corrélations
individu-par-individu (comme A et B) le font sur des données qu'ils ne redéposent pas,
soit par choix éditorial (A), soit par absence de déclaration (B), soit parce que la donnée
humaine sous-jacente est elle-même à accès contrôlé (SOEP, GSS). Le goulot d'étranglement
n'est pas la rareté de la méthode — elle se banalise très vite — mais la **redistribution**
du fichier apparié lui-même.
