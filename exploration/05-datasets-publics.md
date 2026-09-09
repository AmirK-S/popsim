# 05 - Inventaire des jeux de donnees publics exploitables sans humain et sans budget

Agent 5 de l'exploration popsim. Redige le 2 septembre 2026.
Contraintes appliquees : budget zero, aucun humain recrute, phase exploratoire.
Conventions de redaction : voir CONTEXTE.md. Chaque affirmation non triviale porte
[CONFIRME] avec URL, [PROBABLE] avec le raisonnement, ou [HYPOTHESE].

## 0. Verdict en dix lignes

Le projet n'est pas bloque par les donnees. Il existe deux jeux publics, gratuits, sans
compte, qui contiennent exactement le materiau du papier de reference.

Le premier est une **archive OSF de replication**, telechargee et ouverte fichier par
fichier pour ce rapport : 1 052 participants reels, leurs reponses individuelles au GSS,
au Big Five Inventory 44 et a cinq jeux economiques, **en deux vagues sur les memes
personnes**, plus les reponses produites par cinq conditions d'agents dont une condition
fondee sur entretien. C'est le seul jeu de l'inventaire ou le numerateur et le denominateur
du score normalise sont fournis cote a cote, par individu.

Le second est **Twin-2K-500** : 2 058 individus reels, environ 500 questions chacun, quatre
vagues dont une de retest, licence CC BY 4.0, aucun compte. Publie en mai 2025, il n'etait
pas connu du brief initial.

Deuxieme brique : les reponses individuelles du Pew American Trends Panel utilisees par
Santurkar et al. se telechargent en une commande curl, sans compte, depuis CodaLab
(210 Mo, 15 vagues, environ 1 500 questions, 12 attributs socio demographiques).

Troisieme brique : le General Social Survey complet, y compris son panel a trois vagues
sur les memes personnes, se telecharge sans compte depuis norc.org.

Le vrai risque n'est pas l'acces, c'est la contamination. Section 5.

---

## 1. Grand tableau recapitulatif

Colonnes : N = nombre d'individus. Q = nombre de questions ou variables par individu.
Indiv = reponses individuelles disponibles (pas seulement des agregats).
Long = suivi longitudinal des memes personnes. Ouv = reponses ouvertes ou recits.
Acces : 0 = telechargement immediat sans compte, 1 = compte gratuit en ligne,
2 = formulaire signe, 3 = dossier avec examen, 4 = payant.
Expl = exploitabilite immediate de 1 a 5.

| # | Jeu de donnees | N | Q | Indiv | Long | Ouv | Acces | Licence | Format | Taille | Couverture | Expl |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **0** | **Archive OSF `t6g7k`, replication "LLM Agents Grounded in Self-Reports"** | **1 052** | 177 GSS + 44 BFI + 5 jeux econ | **oui, brut** | **oui, 2 vagues sur les memes personnes** | non | **0** | **aucune declaree** | csv + py + R | 3,4 Mo en rar | vagues non datees, archive du 21 avril 2026 | **5** |
| 1 | **Twin-2K-500** (HF `LLM-Digital-Twin/Twin-2K-500`) | 2 058 | ~500 (256 QuestionIDs, 761 colonnes v1-3) | oui | oui, 4 vagues dont retest | partiel | **0** | CC BY 4.0 | parquet + csv + json | quelques centaines de Mo | 2024-2025, US | **5** |
| 2 | **Twin-2K-500-Mega-Study** (HF, meme equipe) | idem cohorte | 12+ experiences | oui | oui | non | **0** | Apache 2.0 | csv + qsf | ~ | 2025 | 4 |
| 3 | **OpinionQA / human_resp** (CodaLab, Santurkar et al.) | ~ 4 000 a 10 000 par vague, 15 vagues | 1 498 questions au total | oui | non (vagues != memes repondants garantis) | non | **0** | non declaree (repo sans LICENSE) | csv dans tar.gz | 210 Mo | ATP 2017-2021 | **5** |
| 4 | **GSS fichier cumule 1972-2024** | > 70 000 cumules | > 6 000 variables | oui | non | non | **0** | usage public NORC | dta / sav / sas | 47,5 Mo (Stata) | 1972-2024 | **5** |
| 5 | **GSS Panel 2016-2020** | 2 348 completes en 2020 | coeur GSS + modules | oui | **oui, 3 rounds** | non | **0** | usage public NORC | dta / sav | 11,8 Mo | 2016, 2018, 2020 | **5** |
| 6 | **Barometre de la confiance politique CEVIPOF** (CDSP) | ~ 2 000 par vague, 17 vagues | quelques centaines | oui | vagues repetees, echantillons renouveles | **oui, verbatims + entretiens semi directifs** | **0** | CC BY 4.0 | tab / xls / docx | 126 fichiers | 2009-2026 | **4** |
| 7 | **Arcom, Les Francais et l'information** (data.gouv.fr) | non verifie | non verifie | oui, base anonymisee complete | 2 editions | non verifie | **0** | Licence Ouverte v2.0 | csv 14,7 Mo | 2024 et 2026 | 2024-2026 | 4 |
| 8 | **INSEE fichier detail Enquete Emploi 2024** | 353 420 obs | 83 variables | oui | rotation trimestrielle | non | **0** | non precisee sur la page | parquet 11 Mo, csv zip 12 Mo | ~23 Mo | 2024 | 3 |
| 9 | **genagents, banque demographique GSS** (GitHub Stanford) | 3 505 agents | 29 champs de persona | profils, pas de reponses humaines | non | non | **0** | MIT | json | quelques Mo | - | 3 |
| 10 | **ANES 2024 Time Series** | ~5 521 | plusieurs centaines | oui | extension du panel 2016-2020 | **oui, open-ends redacted** | **1** | usage academique | dta / sav / csv | non verifie | 2024-2025 | 4 |
| 11 | **Pew American Trends Panel, vagues brutes** | ~ 5 000 a 10 000 par vague | variable | oui | panel, memes personnes entre vagues | rarement | **1** (a confirmer) | usage Pew | .sav | par vague | 2014-2025 (W169) | 4 |
| 12 | **European Social Survey, rounds 1-11** | > 400 000 cumules | ~ 600 | oui | non (repetee, pas panel) | non | **1** | usage non commercial | sav / dta / csv | par round | 2002-2024 | 4 |
| 13 | **European Values Study 2017 (ZA7500)** | 59 438 | ~ 300 | oui | non | non | **1** (GESIS) | usage academique | sav / dta | ~ | 2017-2020, 36 pays | 3 |
| 14 | **World Values Survey vague 7** | ~ 94 728 | ~ 290 + 50 metadonnees | oui | non | non | **1** (formulaire) | conditions WVSA | sav / dta / sas / R | ~ | 2017-2022, 64 pays | 4 |
| 15 | **Understanding America Study (USC)** | ~ 15 000 | tres nombreux modules | oui | **oui, panel internet** | selon module | **1** puis **2** pour le restreint | selon module | csv / dta | par module | 2014-2026 | 4 |
| 16 | **LISS panel (Pays-Bas)** | ~ 7 500 | Core Study annuel + modules | oui | **oui, mensuel depuis 2007** | selon module | **2**, ~5 jours ouvres | usage non commercial | sav / dta / csv | par etude | 2007-2026 | 4 |
| 17 | **HRS (Michigan)** | > 20 000 | tres nombreux | oui | **oui, biennal** | non | **1** | conditions d'usage | dta / sav / sas | plusieurs Go | 1992-2026 | 3 |
| 18 | **PSID (Michigan)** | > 18 000 individus initiaux | tres nombreux | oui | **oui, depuis 1968** | non | **1** | conditions d'usage | ascii / sas / spss / stata | plusieurs Go | 1968-2026 | 3 |
| 19 | **SOEP (DIW Berlin)** | ~ 30 000 | tres nombreux | oui | **oui, annuel** | non | **2**, ~14 jours, DVD payante | contrat de diffusion | dta / sav | plusieurs Go | 1984-2026 | 2 |
| 20 | **SHARE** | > 140 000 | tres nombreux | oui | **oui** | non | **2** | conditions SHARE-ERIC | sav / dta | plusieurs Go | 2004-2026 | 2 |
| 21 | **Understanding Society (UKHLS)** | ~ 40 000 | tres nombreux | oui | **oui, annuel** | selon module | **1 a 2** via UK Data Service | Safeguarded | sav / dta / tab | plusieurs Go | 2009-2026 | 3 |
| 22 | **Enquetes Generation, CEREQ** (Progedo-ADISP) | ~ 25 000 par cohorte | tres nombreux | oui | **oui, reinterrogations a 3 et 7 ans** | non | **2**, email institutionnel obligatoire | FPR ou standard | dta / sav | ~ | 1992-2026 | 2 |
| 23 | **Enquete electorale francaise ENEF 2024** (CDSP) | non verifie | non verifie | oui | 7 vagues | non verifie | **1 a 2** (fichiers restricted) | CC BY-SA 4.0 | tab / csv / sas | ~7 Mo par vague | 2024 | 3 |
| 24 | **American Voices Project** (Stanford) | > 2 700 menages | entretien long + questionnaire structure | oui | non | **oui, entretiens immersifs** | **3**, plusieurs mois, serveur securise | non publique | transcriptions | ~ | 2019-2022 | 1 mais tres haute valeur |
| 25 | **Banque des 1 000 agents Park et al.** | 1 000 | GSS + Big Five + jeux economiques | non public | non | entretiens 2 h non publics | **3**, sur demande aux auteurs | CC BY-NC 3.0 pour le depot | API restreinte | - | 2024 | 1 |
| 26 | **UK Data Service QualiBank + Pioneers of Social Research (SN 6226)** | > 50 recits de vie | - | recits complets | non | **oui, recits de vie integraux** | **1** (compte UKDS) | Open pour SN 6226 | texte | ~ | 1996-2018 | 3 |
| 27 | **Instacart 2017** | > 200 000 utilisateurs | 3 M de commandes | oui, achats | oui, 4 a 100 commandes par client | non | **0** | non commercial | csv | ~200 Mo | 2017 | 3 mais **pas de persona** |
| 28 | **dunnhumby The Complete Journey** | 2 500 foyers | 2 ans d'achats + demographie | oui | oui | non | **0 a 1** | Source Files dunnhumby | csv | ~ | 2 ans | 3 |
| 29 | **NielsenIQ via Kilts Center** | ~ 100 000 foyers | achats + demographie | oui | oui | non | **4, payant** | licence commerciale | - | To | 2004-2026 | **0 pour nous** |
| 30 | **Anthropic GlobalOpinionQA** (`Anthropic/llm_global_opinions`) | **aucun individu** | 2 556 questions | **non, agregats pays** | non | non | **0** | CC BY-NC-SA 4.0 | csv | petit | WVS + Pew GAS | 2 |
| 31 | **SubPOP** (`jjssuh/subpop`) | **aucun individu** | 3 229 questions ATP + 133 GSS | **non, distributions par sous groupe** | non | non | **1**, gated manuel | CC BY-NC-SA 4.0 | jsonl | petit | ATP W61-W132 | 3 |
| 32 | **`andrewsiah/opinions_qa_users_responses`** | 10 000 a 100 000 | colonnes = items ATP | oui | non | non | **0** | non declaree | parquet | ~ | derive OpinionQA | 3 |
| 33 | **`oxford-llms/world_values_survey_2017_2022_sft`** | 100 000 a 1 M lignes | derive WVS7 | oui, format SFT | non | non | **0** | Apache 2.0 | parquet | ~ | WVS7 | 3 |
| 34 | **AlignSurvey** (`PiLabZJU/AlignSurvey_Datasets`) | annonce 44 K entretiens et 400 K enregistrements | - | **depot vide au 2 sept 2026** | - | - | - | MIT | - | 0 | - | **0** |

---

## 2. Fiches detaillees, par ordre d'interet

### 2.0 Archive OSF `t6g7k`, la replication la plus proche du papier de reference

**Ce que c'est.** Le materiel de replication du papier "LLM Agents Grounded in Self-Reports
Enable General-Purpose Simulation of Individuals". Projet OSF public, cree le 21 avril 2026,
un seul contributeur liste : Jonne Kamphorst.
[CONFIRME] via `https://api.osf.io/v2/nodes/t6g7k/` : `public: true`,
`date_created: 2026-04-21T10:11:34`, `node_license: null`.

**Attention sur l'attribution.** Ce n'est **pas** le papier de Park et al. 2024. Le design
est tres proche (memes instruments, meme logique d'agents construits sur entretien), mais
le titre, la date et le contributeur different. Il faut identifier ce papier avant toute
citation. [CONFIRME] par les metadonnees OSF.

**Ce que contient l'archive, verifie fichier par fichier.** Un unique fichier au telechargement,
`replication_instructions.rar`, **3 406 594 octets**, URL directe
`https://osf.io/download/s2u7c/`. Aucun compte requis, HTTP 200 verifie.
Une fois decompresse : **203 entrees**, dont **65 fichiers CSV**, 33 fichiers texte,
15 scripts Python, 2 scripts R, 6 fichiers Markdown, 8 images PNG.
Trois pipelines autonomes : `figure2/`, `figure3/`, `camerer_five_studies/`.

**Le coeur du jeu, `figure2/data/new_analysis_summaries/`.** Trois domaines : `gss_filtered/`,
`bigfive_main/`, `econ_games_main/`. Dans chaque domaine, un sous dossier `preparation/`
contenant des tables de **1 052 lignes**, une par participant, identifiant
`participant_0001` a `participant_1052` :

| Fichier | Contenu | Dimensions verifiees |
|---|---|---|
| `gss_filtered/preparation/p_wave1_summary.csv` | **reponses humaines reelles, vague 1, verite terrain** | 1 052 x 178 |
| `gss_filtered/preparation/p_wave2_summary.csv` | **reponses humaines reelles, vague 2, auto replication** | 1 052 x 178 |
| `gss_filtered/preparation/composite_agents_summary.csv` | agents "questionnaire + entretien" | 1 052 x 178 |
| `gss_filtered/preparation/survey_agents_summary.csv` | agents "questionnaire seul" | 1 052 x 178 |
| `gss_filtered/preparation/gss_v3_summary.csv` | agents fondes sur l'entretien | 1 052 x 178 |
| `gss_filtered/preparation/gss_v6_summary.csv` | agents fondes sur la demographie | 1 052 x 178 |
| `gss_filtered/preparation/gss_v7_summary.csv` | agents fondes sur un persona | 1 052 x 178 |
| `gss_filtered/preparation/gss_v8_summary.csv` | condition supplementaire | 1 052 x 178 |
| `bigfive_main/preparation/p_wave1_summary.csv` et `p_wave2_summary.csv` | scores Big Five humains, 2 vagues | 1 052 x 6 |
| `econ_games_main/preparation/p_wave1_summary.csv` et `p_wave2_summary.csv` | 5 jeux economiques, 2 vagues | 1 052 x 6 |
| `figure3/data/demographic_summary.csv` | **12 attributs de persona par individu** | 1 052 x 12 |

[CONFIRME] : comptage de lignes et de colonnes effectue par lecture directe de chaque CSV
apres decompression.

**Les donnees sont en clair, pas en codes.** Verifie sur `p_wave1_summary.csv` :
en tete `email, natspac/y, natenvir/y, natheal/y, natcity/y, ...`, premiere ligne
`participant_0001, too little, too little, too little, too much, ...`. Les libelles de
questions sont fournis a part dans `figure2/data/question_master/gss/main.csv`
(177 lignes), avec le texte integral et les modalites, par exemple
`NATSPAC/Y, "Are we spending too much, too little, or about the right amount on ""space exploration""?", ["Too little", "About right", "Too much"]`.
Idem pour `question_master/big_five/main.csv` (44 items du BFI, formulation
`I see myself as someone who is talkative`, echelle en 5 points) et
`question_master/econ_games/main.csv` (enonces complets des jeux : dictateur, deux jeux de
confiance, bien public, dilemme du prisonnier).
[CONFIRME] par lecture directe.

**Les 12 attributs de persona.** `demographic_summary.csv` : age par tranche, division de
recensement, ideologie politique, parti, education, race, ethnicite, genre, revenu,
type de quartier, orientation sexuelle. Exemple verifie :
`participant_0001, 45 - 54, middle atlantic, liberal, not very strong democrat, associate/junior college, white, White/Caucasian, female, Less than $25,000, Rural, Heterosexual/straight`.
[CONFIRME].

**Le denominateur du score normalise est deja calcule, par individu.**
`figure2/data/new_analysis_summaries/gss_filtered/analysis/individual_level.csv`,
1 052 lignes x 33 colonnes, contient entre autres :
`p_wave1__p_wave2__accuracy` et `p_wave1__p_wave2__correl` (la fidelite test retest de
**chaque humain**, qui est le denominateur), face a
`p_wave1__composite_agents__accuracy`, `p_wave1__survey_agents__accuracy`,
`p_wave1__gss_v3__accuracy`, `p_wave1__gss_v6__accuracy`, `p_wave1__gss_v7__accuracy`,
`p_wave1__gss_v8__accuracy`, plus les versions `rep_rate_` de chacune.
[CONFIRME] par lecture de l'en tete.

**Les sept conditions de la figure 2**, documentees dans `FIGURE2_PIPELINE.md` :
Random Baseline, Persona-Based, Demographic-Based, Survey-Based (`survey_agents`),
Interview-Based, Survey + Interview (`composite_agents`), et Participants
(vague 2 contre vague 1). Metriques : exactitude pour le GSS, correlation pour les jeux
economiques et le Big Five. Toutes calculees sur la banque complete de 1 052 participants.
[CONFIRME] lecture de `FIGURE2_PIPELINE.md`.

**Le pipeline est reexecutable tel quel.** `figure2/run_pipeline.py` plus
`Rscript R/figure2_reproduce.R` regenerent `figure2_GSS.png`, `figure2_EconGames.png`,
`figure2_Big5.png` et `figure2_combined.png`. Le bundle est declare autonome.
[CONFIRME] lecture du README.

**Bonus, `camerer_five_studies/`.** Replication de cinq etudes du projet de replication
Camerer en sciences sociales, avec 33 rapports texte par condition, du type
`camerer_study11_wave2_GPT4o_interview_survey.txt` et
`camerer_study11_wave2_GPT4o_survey.txt`, et des CSV d'effets standardises. C'est un
materiau tout fait pour la question "un agent reproduit il l'effet experimental, et pas
seulement la reponse individuelle". [CONFIRME] par le listing.

**Ce qui manque, et c'est important.**
1. **Aucune transcription d'entretien.** La recherche de tout fichier contenant "interview"
   ou "transcript" dans les 203 entrees ne renvoie que les rapports GPT-4o de Camerer.
   Les conditions "Interview-Based" et "Survey + Interview" existent en **sortie**, pas en
   **entree**. On peut donc mesurer ce que l'entretien apporte, mais on ne peut pas
   reconstruire un agent d'entretien soi meme depuis cette archive. [CONFIRME].
2. **Aucun prompt d'agent, aucune fiche de persona brute.** Le dossier
   `figure2/data/agent_bank/source_data/bovitz/gabm_infra/` ne contient qu'un
   `participant_list_rand_order_v1.csv` de 1 051 lignes et 2 colonnes.
3. **Les vagues ne sont pas datees** dans les fichiers inspectes, donc l'intervalle test
   retest est inconnu. C'est une lacune serieuse : le denominateur depend de cet intervalle.
   [NON VERIFIE].
4. **Aucune licence.** `node_license: null` sur OSF, aucun fichier LICENSE dans l'archive.
   Comme pour OpinionQA, une absence de licence est plus restrictive qu'une licence
   permissive, pas moins. Usage de recherche interne : risque faible. Publication ou
   demonstration commerciale : a trancher. [CONFIRME] pour l'absence.

**Comparaison avec la banque des 1 000 agents de Park et al., qui reste fermee.**

| Element | Archive OSF `t6g7k` | Banque des 1 000 agents |
|---|---|---|
| Reponses humaines individuelles | **oui, 1 052 personnes, brutes** | non publiques |
| Deuxieme vague sur les memes personnes | **oui** | non publique |
| Sorties d'agents par individu | **oui, 5 conditions** | agregees seulement en acces ouvert |
| Transcriptions d'entretien | **non** | non, et non prevues |
| Attributs de persona | **oui, 12** | oui, via `genagents` mais fictifs et sans reponses humaines |
| Code d'analyse | **oui, Python et R** | code du moteur, oui, via `genagents` en MIT |
| Acces | **immediat, sans compte** | email aux auteurs, examen ethique, delai inconnu |

Autrement dit : **cette archive fournit gratuitement tout ce que la banque de Stanford
promet, sauf les entretiens eux memes.** La demande d'acces a Park et al. reste utile, mais
elle n'est plus bloquante pour demarrer.

**Note d'exploitabilite : 5/5.** C'est le meilleur point de depart de tout l'inventaire.

---

### 2.1 Twin-2K-500, le second pilier

**Ce que c'est.** Une enquete menee sur un echantillon representatif de 2 058 adultes
americains, 2,42 heures de questionnaire par personne en moyenne, repartie sur quatre
vagues. Les trois premieres couvrent demographie, echelles psychologiques, performance
cognitive, preferences economiques et replications d'experiences d'economie
comportementale. La quatrieme vague, lancee deux semaines apres la troisieme, **repete
les taches des vagues precedentes pour etablir une reference de fidelite test retest**.
[CONFIRME] https://arxiv.org/abs/2505.17479 (resume verbatim recupere) et
https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500

**Pourquoi c'est decisif pour nous.** C'est litteralement le design du papier de Stanford,
mais en acces ouvert. Le denominateur du score normalise, la fidelite test retest des
humains eux memes, est fourni par la vague 4. Le README de la carte du dataset explicite
meme la structure d'evaluation : `wave1_3_persona_text` sert a construire le persona,
`wave4_Q_wave1_3_A` sert de reference test retest humaine, `wave4_Q_wave4_A` sert de
verite terrain. [CONFIRME] lecture du README de la carte HF.

**Acces.** Aucun compte. `gated: False` verifie via l'API Hugging Face. Licence CC BY 4.0.
[CONFIRME] `https://huggingface.co/api/datasets/LLM-Digital-Twin/Twin-2K-500` renvoie
`license: ['cc-by-4.0']`, `gated: False`, 1 776 telechargements, 30 likes, 183 fichiers.

**Fichiers a telecharger, noms exacts.**
- `question_catalog_and_human_response_csv/question_catalog.json` : catalogue des
  256 QuestionIDs uniques, avec type, options, libelles d'echelle et noms de colonnes.
- `question_catalog_and_human_response_csv/wave1_3_response.csv` et
  `wave1_3_response_label.csv` : 2 058 participants x 761 colonnes, en codes numeriques
  et en libelles texte.
- `question_catalog_and_human_response_csv/wave4_response.csv` et
  `wave4_response_label.csv` : 2 058 x 127 colonnes.
- `LLM_simulation_results/GPT4.1-mini-simulation-llm-vs-human/responses_wave4_formatted.csv`
  et `responses_llm_imputed_formatted.csv` : la baseline LLM des auteurs, deja calculee.
- Configurations `datasets` : `full_persona` et `wave_split`.
[CONFIRME] listing des 183 fichiers via l'API HF et lecture du README.

**Bonus.** L'equipe a publie une baseline complete : simulations GPT-4.1, GPT-4.1-mini,
Gemini-Flash-2.5, versions persona JSON, persona texte, fine tuning sur 500 exemples,
avec pour chacune un dossier `accuracy_evaluation` contenant
`mad_accuracy_summary.xlsx` et `within_subject_analysis.xlsx`. On peut donc se comparer
a un etat de l'art publie sans depenser un euro d'API. [CONFIRME] listing des fichiers.

**Publication.** arXiv 2505.17479, mai 2025. Egalement publie dans Marketing Science
(https://pubsonline.informs.org/doi/10.1287/mksc.2025.0262). Code et documentation :
https://github.com/tianyipeng-lab/Digital-Twin-Simulation et
https://digital-twin-simulation-version2.readthedocs.io/en/latest/index.html
[CONFIRME] liens cites dans le README de la carte HF.

**Chiffre a verifier.** Un resume de recherche indique que les jumeaux atteignent 87 pour
cent de la reference test retest en hors echantillon. Ce chiffre n'apparait pas dans le
resume verbatim que j'ai recupere. [PROBABLE], a confirmer dans le corps du papier.

**Note d'exploitabilite : 5/5.**

---

### 2.2 Twin-2K-500-Mega-Study, le complement experimental

`LLM-Digital-Twin/Twin-2K-500-Mega-Study`, licence Apache 2.0, non gated, 71 fichiers,
186 telechargements. Structure : `.dat/<nom_experience>/raw_data/response.csv` plus
`survey.qsf` (definition Qualtrics du questionnaire). Les experiences listees incluent
`accuracy_nudges`, `affective_priming`, `consumer_minimalism`, `context_effects`,
`digital_certification`, `hiring_algorithms`, `idea_evaluation`, `idea_generation`.
[CONFIRME] listing API HF. Papier associe : arXiv 2509.19088.

Interet pour l'axe commercial : `consumer_minimalism`, `idea_evaluation` et
`hiring_algorithms` sont des taches de type etude de marche. C'est le terrain ideal pour
la demonstration "montrez nous votre derniere etude". **Exploitabilite 4/5.**

---

### 2.3 OpinionQA, les reponses individuelles du Pew American Trends Panel

**Ce que c'est.** Le jeu de donnees de Santurkar et al. 2023, "Whose Opinions Do Language
Models Reflect ?" (arXiv 2303.17548). 1 498 questions a choix multiples issues de
15 vagues de l'American Trends Panel, plus les reponses individuelles des repondants Pew.

**Acces, point critique.** Le depot GitHub `tatsu-lab/opinions_qa` ne contient **que le
code**, pas les donnees : 8 fichiers, 14 Mo, aucun dossier `data`. [CONFIRME] via
l'API GitHub. Les donnees sont sur CodaLab, worksheet `0x6fb693719477478aac73fc07db333f69`,
titre "OpinionsQA Dataset", proprietaire `shibani`, permission publique en lecture.
[CONFIRME] via `https://worksheets.codalab.org/rest/interpret/worksheet/0x6fb693719477478aac73fc07db333f69`.

**Les trois bundles et leurs URL de telechargement direct, sans compte.**

| Bundle | UUID | Taille exacte | URL |
|---|---|---|---|
| `model_input` | `0xa6f81cc62d7d4ccb93031a72d2043669` | 510 807 octets | `https://worksheets.codalab.org/rest/bundles/0xa6f81cc62d7d4ccb93031a72d2043669/contents/blob/` |
| `human_resp` | `0x050b7e72abb04d1f9b493c1743e580cf` | **210 273 356 octets** | `https://worksheets.codalab.org/rest/bundles/0x050b7e72abb04d1f9b493c1743e580cf/contents/blob/` |
| `runs` | `0xd70e124707194a77b73e5d20ae074ee9` | 4,1 Go | `https://worksheets.codalab.org/rest/bundles/0xd70e124707194a77b73e5d20ae074ee9/contents/blob/` |

[CONFIRME] : requete HEAD sur les deux premieres URL renvoie HTTP 200, sans cookie
d'authentification, avec `Content-Disposition: attachment; filename="human_resp.tar.gz"`
et l'entete `X-Codalab-Target-Size: 210273356`.

**Structure interne de `human_resp`, verifiee fichier par fichier.**
Un repertoire par vague ATP : W26, W27, W29, W32, W34, W36, W41, W42, W43, W45, W49,
W50, W54, W82, W92. Plus `Pew_American_Trends_Panel_disagreement_500/` (les 500 questions
les plus clivantes) et `topic_mapping.npy` (411 337 octets).
Chaque repertoire de vague contient trois fichiers :
- `info.csv` : une ligne par question, avec la cle (`SAFECRIME_W26`), le mapping des
  modalites, **le texte integral de la question**, la liste des reponses possibles et
  l'ordinalite. Exemple verifie : `"How safe, if at all, would you say your local community
  is from crime? Would you say it is"`.
- `metadata.csv` : les 12 attributs de persona disponibles, avec leurs modalites.
  Verifie sur W26 : `CREGION`, `AGE`, `SEX`, `EDUCATION`, `CITIZEN`, `MARITAL`, `RELIG`,
  `RELIGATTEND`, `POLPARTY`, `INCOME`, `POLIDEOLOGY`, `RACE`.
- `responses.csv` : **une ligne par repondant**, identifiant `QKEY`, horodatage de debut
  et de fin d'interview, type d'appareil, langue, puis toutes les reponses **en clair,
  pas en codes**. Verifie sur W92 : premiere ligne QKEY 100260, interview du 10 juillet
  2021 de 21h13 a 21h33, smartphone, anglais, reponses du type
  `"A great deal of difference in what they stand for"`.
Tailles des `responses.csv` : de 6,2 Mo (W41) a 40 Mo (W92).
[CONFIRME] via l'API de listing CodaLab et lecture directe des premieres lignes.

**Ce que ca vaut.** Les reponses sont deja en langage naturel, ce qui supprime toute la
phase de decodage des codebooks. On peut construire un prompt de persona et un prompt de
question par simple concatenation de `metadata.csv` et `info.csv`. C'est le jeu de donnees
le plus rapide a mettre en production.

**Licence.** Le depot GitHub n'a **aucun fichier LICENSE** et le champ `license` de l'API
GitHub vaut `null`. [CONFIRME]. Les donnees restent la propriete du Pew Research Center.
Pour une publication, il faudra vraisemblablement citer Pew et Santurkar et al., et
verifier les conditions Pew. [HYPOTHESE] sur ce que Pew exige exactement.

**Note d'exploitabilite : 5/5.**

**Source amont.** Les vagues brutes de l'ATP sont sur
https://www.pewresearch.org/american-trends-panel-datasets/ au format `.sav`. La vague la
plus recente listee est la W169, terrain du 28 avril au 4 mai 2025, sur le theme
"Climate and energy". [CONFIRME] par lecture de la page. La page ne precise pas si un
compte est requis, elle renvoie a info@pewresearch.org. [NON VERIFIE] sur ce point precis.
Le depot SubPOP indique qu'il suffit de recuperer les `.sav` des vagues 61 a 132 depuis
cette page, ce qui suggere un acces peu contraint. [PROBABLE].

---

### 2.4 General Social Survey, la reference du papier de Stanford

**Fichier cumule 1972-2024, release 3a de juillet 2026.** Telechargement direct, sans
compte, verifie par requete HEAD :
- Stata : `https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip`
  HTTP 200, **47 562 980 octets**. [CONFIRME]
- SPSS : `https://gss.norc.org/content/dam/gss/get-the-data/documents/spss/GSS_spss.zip`
  HTTP 200, **111 661 090 octets**. [CONFIRME]
Page d'index : https://gss.norc.org/us/en/gss/get-the-data/stata.html

**GSS Panel 2016-2020.** C'est la piece rare : les memes personnes reinterrogees.
- `https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_2020_panel_stata_1a.zip`
  HTTP 200, **11 847 819 octets**, release 1a d'avril 2022. [CONFIRME]
- Codebook :
  `https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/2016-2020%20GSS%20Panel%20Codebook%20-%20R1.pdf`
- Design : trois rounds, entretiens initiaux 2016, entretiens initiaux 2018, reinterrogation
  2020. Les repondants presents aux deux vagues ont recu **les memes questions du coeur GSS,
  a deux ou quatre ans d'intervalle**. 2 348 entretiens completes en 2020, sous echantillon
  aleatoire de 2 146 sur 2 867 pour la cohorte 2016. [PROBABLE], chiffres issus d'un resume
  du codebook, a revalider dans le PDF.
- Il existe aussi des panels 2006-2014, telechargeables sur la meme page.
- **Aucun panel 2020-2024 n'existe a ce jour.** [CONFIRME] par la page de documentation GSS,
  qui ne liste que deux codebooks de panel, 2006-2014 et 2016-2020.

**Interet.** Le panel donne une estimation directe de la fidelite test retest humaine sur
l'instrument exact utilise par Stanford, avec un intervalle de deux ou quatre ans.
C'est un denominateur different de celui de Twin-2K-500 (deux semaines) et l'ecart entre
les deux est en soi un resultat publiable. [HYPOTHESE] sur la valeur scientifique.

**Note d'exploitabilite : 5/5.**

**Attention.** Le paquet R `gssr` de Kieran Healy (https://kjhealy.github.io/gssr/)
distribue les memes donnees pretes a l'emploi, ce qui evite de manipuler des `.dta`.
[CONFIRME] existence du paquet.

---

### 2.5 Le materiau francais, la parade contamination

#### 2.5.1 Barometre de la confiance politique du CEVIPOF, via le CDSP

C'est la trouvaille francaise du rapport. DOI `10.21410/7E4/9K3VGR` sur le Dataverse de
Sciences Po. **Licence CC BY 4.0. 126 fichiers. Tous les fichiers ont `restricted: false`.**
[CONFIRME] via `https://data.sciencespo.fr/api/datasets/:persistentId/?persistentId=doi:10.21410/7E4/9K3VGR`

Telechargement direct verifie, sans compte, par requete HEAD sur
`https://data.sciencespo.fr/api/access/datafile/<id>` :
- id `10529` : `Base Baromètre Confiance Vague 16 - 4 pays.tab`, 4 721 550 octets, HTTP 200.
- id `10525` : `Data Quali Entretiens IA Semi Directifs Vague 16`, docx, 272 659 octets, HTTP 200.
- id `8789` : `Verbatims Baromètre confiance vague 1 web.xls`, 743 936 octets, HTTP 200.
[CONFIRME]

Le corpus couvre au moins 17 vagues depuis 2009, avec des bases par vague, des bases
cumulees multi pays (France, Allemagne, Italie, Pays Bas), les questionnaires, les rapports
et, pour la vague 16, **un guide d'entretiens semi directifs de 10,3 Mo et un fichier de
donnees qualitatives d'entretiens**. Il y a aussi un fichier de verbatims des la vague 1.
[CONFIRME] par le listing.

Le fait qu'il existe a la fois une base de reponses fermees et des entretiens semi
directifs sur le meme dispositif est exactement le type de materiau du papier de Stanford.
**Reserve importante** : rien ne garantit que les personnes interviewees soient les memes
que celles du questionnaire ferme, ni qu'un identifiant permette de les apparier.
[NON VERIFIE], il faut ouvrir le fichier `10525`.

Termes d'usage : mention obligatoire de l'enquete OpinionWay et de l'equipe de recherche,
Bruno Cautres (Sciences Po CEVIPOF). [CONFIRME] champ `termsOfAccess` du Dataverse.

**Note d'exploitabilite : 4/5**, 5/5 si l'appariement entretiens / questionnaire existe.

#### 2.5.2 Enquete electorale francaise ENEF 2024, via le CDSP

Sept vagues publiees, DOI de la vague 1 : `10.21410/7E4/AFCJAY`. Licence CC BY-SA 4.0.
**Difference majeure avec le barometre : les fichiers de donnees sont `restricted: true`.**
Concretement :
- accessible sans compte : `Dictionnaire_ENEF2024.ods` (51 757 o),
  `Documentation_ENEF2024_V1.pdf` (348 786 o), `Questionnaire_ENEF2024_V1.pdf` (786 914 o),
  `fr_cdsp_ddi_enef2024_v1.xml` (279 888 o).
- **restreint** : `fr_cdsp_ddi_enef2024_v1.tab` (4 303 977 o),
  `fr_cdsp_ddi_enef2024_v1-1.tab` (6 834 155 o), `fr_cdsp_ddi_enef2024_v1_csv.zip`
  (1 113 770 o), `fr_cdsp_ddi_enef2024_v1_sas.zip` (1 370 949 o).
[CONFIRME] via l'API Dataverse.
Le Dataverse a `fileAccessRequest: true`, donc une demande d'acces en ligne est possible.
Delai inconnu. [NON VERIFIE].

Les autres DOI des vagues 2 a 7 : `10.21410/7E4/7HRNPP`, `10.21410/7E4/CXKJJR`,
`10.21410/7E4/SCEWBH`, `10.21410/7E4/BNCPUL`, `10.21410/7E4/2DCN6P`, `10.21410/7E4/SZVODV`.
[CONFIRME] via l'API de recherche.

Le catalogue CDSP contient 338 resultats pour "enquete electorale", dont la serie des
enquetes pre et post electorales francaises de 1958 a 2012. [CONFIRME].

#### 2.5.3 Arcom, "Les Francais et l'information", sur data.gouv.fr

Jeu de donnees `les-francais-et-linformation-barometre`. **Licence Ouverte v2.0 (`lov2`).**
Producteur : Arcom. Telechargement direct sans compte.
- Edition 2026, publiee le 4 juin 2026 :
  `https://static.data.gouv.fr/resources/les-francais-et-linformation-barometre/20260604-074907/2026-les-francais-et-linformation-2eme-edition-arcom-base-anonymisee-complete.csv`
  14 760 219 octets, plus la datamap xlsx (126 490 o) et le guide d'utilisation pdf.
- Edition 2024 : base anonymisee complete en txt (5 545 125 o) et xlsx (5 308 201 o),
  datamap et questionnaire pdf.
[CONFIRME] via `https://www.data.gouv.fr/api/1/datasets/les-francais-et-linformation-barometre/`

**Pourquoi c'est strategique.** L'edition 2026 a ete publiee le 4 juin 2026, soit
**apres la date de coupure de connaissance des modeles que nous utiliserons**. C'est la
meilleure parade contamination disponible gratuitement, en francais, avec des reponses
individuelles. Le nombre exact de repondants et de variables n'a pas ete verifie.
[NON VERIFIE].

#### 2.5.4 INSEE, fichiers detail

L'INSEE publie des "fichiers detail" en telechargement direct, sans compte.
Exemple verifie, enquete Emploi 2024, page https://www.insee.fr/fr/statistiques/8632441 :
- `https://www.insee.fr/fr/statistiques/fichier/8632441/FD_EEC_2024.parquet` (11 Mo), HTTP 200
- `https://www.insee.fr/fr/statistiques/fichier/8632441/FD_csv_EEC_2024.zip` (12 Mo), HTTP 200
- `https://www.insee.fr/fr/statistiques/fichier/8632441/Varmod_EEC_2024.csv` (209 Ko), HTTP 200
83 variables, 353 420 observations. [CONFIRME] pour les URL et les tailles, [PROBABLE] pour
le nombre de variables et d'observations, issu de la page.

Limite : l'enquete Emploi est une enquete de situation, pas d'opinion. Elle donne des
attributs de persona tres riches mais peu de questions dont on pourrait cacher la reponse.
Utilite reelle : **construire une population synthetique representative de la France**
pour l'etape de passage a l'echelle. **Exploitabilite 3/5.**

L'enquete Budget de famille est referencee en https://www.insee.fr/fr/metadonnees/source/serie/s1194
mais je n'ai pas verifie si son fichier detail est en telechargement libre ou passe par
Progedo. [NON VERIFIE].

#### 2.5.5 CEREQ et Progedo-ADISP

Les enquetes Generation du CEREQ (cohortes 1992, 1998, 2001, 2004, 2007, 2010, 2013, 2017)
sont diffusees via https://data.progedo.fr/. Serie : https://data.progedo.fr/series/adisp/generation.
Exemple : "Génération 2017 - Interrogation à 3 ans - 2020", doi 10.13144/lil-1649.

Conditions d'acces, verifiees sur https://data.progedo.fr/access_conditions :
- gratuit,
- **adresse mail institutionnelle obligatoire** et rattachement a une unite de recherche
  ou d'enseignement,
- formulaires a signer manuellement et a renvoyer scannes en PDF,
- pour les Fichiers Production Recherche, engagement de confidentialite supplementaire et
  habilitation par le Comite du secret statistique,
- habilitation valable sans limite de temps une fois accordee,
- **delai non precise**.
[CONFIRME] pour tous ces points sauf le delai.

**Verrou pour nous.** Amir n'a pas d'affiliation academique declaree dans CONTEXTE.md.
C'est precisement le point ou le contact MIT de Simon peut debloquer. Voir section 6.

---

### 2.6 Les panels internationaux, par ordre de facilite

#### ANES
Data center : https://electionstudies.org/data-center/. **Inscription requise pour
telecharger**, formulaire de "Data Registration", confirmation par email puis creation du
mot de passe. Rien n'indique un cout. [PROBABLE] a partir de la FAQ ANES.
- Etude 2024 Time Series : release complete le 8 aout 2025, environ 5 521 repondants.
  Composition : echantillon frais en face a face (1 042 pre / 925 post), echantillon frais
  web (2 308 pre / 1 969 post), **extension du panel ANES 2016-2020** (2 171 pre / 2 070 post).
  Terrain pre electoral du 3 aout au 5 novembre 2024, post electoral du 7 novembre 2024 au
  17 fevrier 2025. [PROBABLE], chiffres issus de l'annonce ANES, le nombre 5 521 apparait
  avec une coquille dans la source consultee.
  Page : https://electionstudies.org/data-center/2024-time-series-study/ (renvoie un
  HTTP 403 aux robots, il faut y aller au navigateur).
- **Reponses ouvertes** : ANES publie des jeux "Redacted Open-Ends" pour l'etude 2020,
  couvrant le moment de la decision de vote, les likes et dislikes, la reconnaissance des
  charges publiques et le probleme le plus important. C'est du texte libre par individu.
  [CONFIRME] par l'annonce https://electionstudies.org/anes-announcement-2020-restricted-data-and-new-redacted-open-ends/
- Il existe aussi une "ANES-GSS 2020 Joint Study", potentiellement precieuse pour croiser
  les deux instruments sur les memes personnes. [NON VERIFIE] sur le design exact.

**Exploitabilite 4/5.** Les open-ends font d'ANES le meilleur candidat anglophone gratuit
pour un persona construit a partir de texte libre plutot que de cases cochees.

#### European Social Survey
Portail : https://www.europeansocialsurvey.org/data-portal, moteur https://ess.sikt.no/.
Telechargement gratuit pour usage non commercial **apres une inscription courte**, possible
via eduGAIN, via un compte Google, ou par email. [PROBABLE], convergence de plusieurs
sources secondaires, la page officielle n'a pas pu etre lue par l'outil.
Round 11 (2023/24), troisieme diffusion, edition 4.0 du fichier integre, 30 pays dont
l'Estonie et l'Ukraine. [CONFIRME] par
https://www.europeansocialsurvey.org/news/article/final-release-round-11-data
Pas de suivi longitudinal des memes individus. **Exploitabilite 4/5** pour la variance
inter culturelle, 0 pour le test retest.

#### World Values Survey et European Values Study
- WVS vague 7 : 64 pays, plus de 80 000 repondants selon le site WVSA, environ 94 728 selon
  le papier WorldValuesBench. Telechargement apres remplissage d'un formulaire et
  acceptation des conditions, fichier zip, formats SPSS, Stata, SAS, R.
  [PROBABLE], je n'ai pas reussi a faire lire la page de telechargement par l'outil, le
  contenu est charge dynamiquement.
- EVS 2017, jeu integre ZA7500 : 59 438 repondants, 36 pays, telechargement gratuit apres
  inscription au catalogue GESIS. Jeu joint EVS/WVS 2017-2022 : ZA7505, v5.0.0.
  [PROBABLE], sources GESIS secondaires.
- Derive pret a l'emploi : `oxford-llms/world_values_survey_2017_2022_sft` sur Hugging Face,
  Apache 2.0, 100 K a 1 M lignes, parquet, non gated. [CONFIRME] via l'API HF.
  C'est le chemin le plus court vers du WVS individuel sans formulaire.
- Benchmark academique : https://github.com/Demon702/WorldValuesBench, construit sur WVS7,
  50 champs de metadonnees d'entretien et 290 questions communes. [PROBABLE].

#### Understanding America Study, USC
https://uasdata.usc.edu/. Panel probabiliste par internet, environ 15 000 residents
americains, dont un sur echantillon californien de 3 500 et pres de 700 adolescents.
Donnees gratuites apres creation d'un compte. **Le formulaire demande une adresse email
fournie par une institution de recherche, d'enseignement, gouvernementale ou financiere.**
Certaines donnees sont restreintes et exigent un accord d'utilisation signe.
[PROBABLE], formulation issue de la page d'inscription.
Le panel est longitudinal et couvre education, emploi, sante, logement, **personnalite**,
attitudes sociales et bien etre. C'est un tres bon candidat de second rang.
**Exploitabilite 4/5 si le compte passe, 0 sinon.**

#### LISS panel, Pays Bas
https://www.lissdata.nl/access-data. Environ 5 000 menages, 7 500 individus de plus de
16 ans, questionnaires mensuels depuis 2007. Gratuit pour la recherche scientifique ou
d'interet public non commerciale. Procedure : signature d'une declaration en ligne sur
https://liss.statements.centerdata.nl/, puis reception d'un mot de passe.
**Delai annonce : cinq jours ouvres.** L'affiliation academique n'est pas explicitement
exigee, les etudiants et chercheurs independants sont admis.
[CONFIRME] par lecture de la page d'acces.
**C'est le panel longitudinal riche le plus accessible a quelqu'un sans poste academique.**
**Exploitabilite 4/5, avec cinq jours de delai.**

#### HRS et PSID, Michigan
- HRS : inscription gratuite sur https://hrsdata.isr.umich.edu/user/register, puis
  telechargement des fichiers de diffusion publique. Les donnees de sante sensibles et les
  donnees restreintes exigent des demarches supplementaires. [PROBABLE].
- PSID : donnees d'usage public gratuites pour tout chercheur qui s'enregistre et accepte
  les conditions. Data Center permettant de composer des extraits sur mesure, exports
  ASCII, SAS, SPSS, Stata. https://psidonline.isr.umich.edu/. [PROBABLE].
Les deux sont longitudinaux et tres riches, mais orientes revenus, emploi et sante, peu
d'opinions. **Exploitabilite 3/5** pour notre objet.

#### SOEP, Allemagne
Gratuit pour la recherche scientifique, mais **contrat de diffusion a signer avec le DIW
Berlin, envoi du jeu de donnees sur DVD par courrier assure, 38 euros de frais**, delai
d'environ 14 jours entre la demande et la reception. [PROBABLE], source secondaire.
Les 38 euros violent la contrainte budget zero, meme si le montant est faible.
Alternative gratuite : verifier s'il existe une diffusion par telechargement. [NON VERIFIE].
**Exploitabilite 2/5.**

#### SHARE
https://share-eric.eu/data/data-access. Gratuit apres inscription, mais il faut
**demontrer que la recherche prevue est pertinente pour SHARE** et etre rattache a une
organisation de recherche. [PROBABLE]. **Exploitabilite 2/5** sans affiliation.

#### Understanding Society, Royaume Uni
Diffusion par le UK Data Service. Les personnes hors Royaume Uni et sans organisation
peuvent demander un identifiant, mais certaines collections ne sont pas ouvertes aux
utilisateurs non britanniques, a verifier dans l'onglet "Access" de chaque fiche.
[CONFIRME] par https://ukdataservice.ac.uk/help/registration/registration-login-faqs/
**Exploitabilite 3/5.**

---

### 2.7 La banque des 1 000 agents de Stanford, Park et al.

**Ce qui est ouvert.** Le depot https://github.com/joonspk-research/genagents, licence MIT,
contient :
- le moteur d'agents generatifs complet, avec les gabarits de prompts exacts :
  `simulation_engine/prompt_template/generative_agent/interaction/categorical_resp/singular_v1.txt`
  et `batch_v1.txt`, `numerical_resp/`, `utternace/utterance_v1.txt`,
  `memory_stream/importance_score/`, `memory_stream/reflection/`.
- `environment/interview/interview.py` et `environment/survey/survey.py`.
- **une banque de 3 505 agents demographiques construits a partir du GSS**, dans
  `agent_bank/populations/gss_agents/<uuid>/`. [CONFIRME] : comptage exact via l'arbre Git,
  3 505 repertoires d'agents, arbre non tronque.
  Chaque agent a un `scratch.json` d'environ 1 Ko avec 29 champs. Exemple integralement
  verifie : prenom, nom, age, sexe, ethnicite, race, race detaillee, origine hispanique,
  adresse, ville, etat, opinions politiques, identification partisane, region de residence
  a 16 ans, structure familiale a 16 ans, revenu familial a 16 ans, diplome du pere,
  diplome de la mere, historique de travail de la mere, statut marital, statut d'emploi,
  service militaire, religion, religion a 16 ans, ne aux Etats Unis, citoyennete, plus haut
  diplome, autre langue parlee, patrimoine total.
  **Les noms et adresses sont fictifs.** Les `memory_stream/nodes.json` et
  `embeddings.json` sont vides (2 octets).
- **un agent d'exemple base sur un entretien**, celui d'un des auteurs, dans
  `agent_bank/populations/single_agent/01fd7d2a-0357-4c1b-9f3e-8eade2d537ae/`.

**Ce qui est ferme.** La banque des plus de 1 000 agents construits sur de vrais entretiens
de deux heures n'est pas publique. Le README annonce un systeme a deux niveaux : acces
ouvert aux reponses agregees sur des taches fixes, acces restreint aux reponses
individuelles sur des taches ouvertes, apres examen ethique. [CONFIRME] lecture du README.

**Procedure d'acces.** Il n'y a **aucun formulaire public**. Le README dit de contacter les
auteurs. Contact indique : Joon Sung Park, joonspk@stanford.edu. [CONFIRME].
Le depot Stanford Digital Repository https://purl.stanford.edu/jm164ch6237 porte une
licence CC BY-NC 3.0 et n'est pas en acces libre ; la page ne liste pas les fichiers.
[CONFIRME] lecture de la page.

**Conclusion operationnelle.** On ne peut pas construire notre reproduction sur cette
banque. En revanche on peut, des demain et sans un euro, **rejouer le moteur de Stanford
tel quel** sur les 3 505 agents demographiques, en remplacant l'appel OpenAI par un modele
ouvert local. C'est la baseline "demographie seule" contre laquelle il faut mesurer tout
gain apporte par un persona plus riche. **Exploitabilite 3/5 pour le code, 1/5 pour la
banque d'entretiens.**

---

### 2.8 Corpus d'entretiens et de recits de vie

C'est le maillon le plus faible de l'inventaire, et c'est attendu : un entretien de deux
heures apparie a un questionnaire ferme sur la meme personne est un objet rare, parce que
c'est precisement ce qui rend l'individu reidentifiable.

**American Voices Project, Stanford.** C'est le corpus qui correspond le mieux.
Plus de 2 700 entretiens approfondis menes entre 2019 et 2022 dans environ 300 communautes,
et **chaque entretien est suivi d'un questionnaire structure**, certaines reponses etant
appariees a des donnees administratives. [CONFIRME] lecture de
https://inequality.stanford.edu/data/american-voices-project-data
Acces : transcriptions desidentifiees sur un serveur securise Stanford, avec NVivo, R,
Python, Stata, **une bibliotheque Ollama hebergee localement**, et possiblement le cluster
Carina. Revue de dossier annoncee comme pouvant prendre **plusieurs mois**. Formulaire :
https://docs.google.com/forms/d/e/1FAIpQLSfcgo70aSzM0bR8GXpLQMMnh3mB-y7HIlJxBZlOvcAg7bVdkQ/viewform
Contact : americanvoicesproject@stanford.edu.
La presence d'un Ollama local sur le serveur signifie que **le dispositif est deja pense
pour des traitements LLM sans sortie de donnees**. C'est un signal fort : notre protocole
est realisable chez eux.
**Exploitabilite immediate 1/5, valeur strategique 5/5.** A lancer maintenant parce que le
delai est long.

**UK Data Service QualiBank.** https://discover.ukdataservice.ac.uk/qualibank
Environ 350 collections qualitatives, entretiens, essais, reponses ouvertes et rapports,
avec recherche plein texte et citation au niveau de l'enonce. [PROBABLE].
Collection phare en acces ouvert : "Pioneers of Social Research, 1996-2018", SN 6226,
doi 10.5255/UKDA-SN-6226-6, plus de cinquante recits de vie de chercheurs, transcriptions
integrales et resumes detailles, ouvertement accessibles. Guide d'entretien public :
http://doc.ukdataservice.ac.uk/doc/6226/mrdoc/pdf/6226_pioneers_interview_guide.pdf
[PROBABLE] pour l'ouverture complete, [CONFIRME] pour l'existence et le numero SN.
Limite : la population est composee d'universitaires britanniques, pas d'un echantillon
representatif, et il n'y a pas de questionnaire ferme apparie. Utilite reelle : **calibrer
la longueur, le style et la structure d'un entretien de recit de vie** pour notre futur
protocole, sans recruter personne. **Exploitabilite 3/5 pour cet usage.**

**Corpus mineur mais parfaitement apparie.** "Fostering cultures of open qualitative
research", Universite de Sheffield, trois jeux lies : reponses au questionnaire,
transcriptions d'entretiens, transcription d'atelier, relies par un champ `RespondentID`.
15 transcriptions, 14 des 15 participants selectionnes sur leurs reponses au questionnaire.
CC BY-NC. [PROBABLE].
N est ridicule pour de la statistique, mais c'est un **banc d'essai gratuit et immediat**
pour ecrire et deverminer le pipeline entretien vers persona vers prediction, avant de le
passer sur des donnees serieuses. https://orda.shef.ac.uk/ (chercher les trois datasets).

**Le fichier `10525` du barometre CEVIPOF.** "Data Quali Entretiens IA Semi Directifs
Vague 16", 272 659 octets, telechargeable sans compte. Si ce fichier contient des
transcriptions appariables a la base quantitative de la vague 16, c'est le seul corpus
francais du type Stanford accessible librement. **A ouvrir en priorite.** [NON VERIFIE].

---

### 2.9 Comportement d'achat

**Instacart Online Grocery Shopping Dataset 2017.**
https://www.instacart.com/datasets/grocery-shopping-2017. Plus de 3 millions de commandes,
plus de 200 000 utilisateurs, entre 4 et 100 commandes par utilisateur, avec la sequence
des produits, le jour de la semaine et l'heure. Usage non commercial.
[PROBABLE] pour l'URL S3 exacte, [CONFIRME] pour le contenu et la licence non commerciale.
**Defaut redhibitoire pour nous : aucune donnee demographique sur les utilisateurs.**
On ne peut donc pas construire de persona. Utilite : etudier si un historique d'achat suffit
a lui seul a predire l'achat suivant, ce qui est un autre sujet. **Exploitabilite 3/5 pour
un sujet adjacent, 1/5 pour le notre.**

**dunnhumby, The Complete Journey.** https://www.dunnhumby.com/source-files/
2 500 foyers clients frequents, deux ans d'achats complets, **plus les caracteristiques
demographiques du foyer** et l'historique des sollicitations marketing directes.
[CONFIRME] pour le contenu. C'est le seul jeu gratuit qui relie achats individuels et
profil de foyer. Egalement miroite sur Kaggle
(https://www.kaggle.com/datasets/frtgnn/dunnhumby-the-complete-journey).
La demographie est grossiere (taille du foyer, tranche de revenu, presence d'enfants), donc
le persona sera pauvre. **Exploitabilite 3/5.**

**NielsenIQ via le Kilts Center, Chicago Booth.**
https://www.chicagobooth.edu/research/kilts/research-data/nielseniq/pricing
Tarifs verifies : abonnement individuel enseignant chercheur, 3 000 dollars pour trois ans
pour un jeu, 5 000 pour deux, 7 000 pour trois. Abonnement institutionnel, 4 000 dollars
pour un an pour un jeu, 7 000 pour deux, 10 000 pour trois.
Eligibilite : enseignants chercheurs titulaires ou en voie de titularisation, doctorants et
post doctorants avec projet approuve, aux Etats Unis. [CONFIRME] pour les tarifs et
l'eligibilite.
**Verdict : hors de portee, et pas seulement pour le prix. Amir n'est pas eligible.**
Seule voie : passer par une institution deja abonnee via le contact MIT. Le MIT figure
parmi les institutions susceptibles d'etre abonnees. [HYPOTHESE].
**Alternative gratuite la plus proche : dunnhumby The Complete Journey**, degradee sur la
taille (2 500 foyers contre environ 100 000) mais identique sur la structure.

---

### 2.10 Benchmarks deja construits, identifiants Hugging Face exacts

| Identifiant HF ou depot | Licence | Gated | Niveau | Verdict |
|---|---|---|---|---|
| `LLM-Digital-Twin/Twin-2K-500` | CC BY 4.0 | non | **individuel** | **le meilleur, de loin** |
| `LLM-Digital-Twin/Twin-2K-500-Mega-Study` | Apache 2.0 | non | **individuel** | complement experimental |
| `Anthropic/llm_global_opinions` | CC BY-NC-SA 4.0 | non | **agrege par pays** | **inutilisable pour predire un individu** |
| `jjssuh/subpop` | CC BY-NC-SA 4.0 | **oui, manuel** | distributions par sous groupe | utile comme baseline agregee |
| `andrewsiah/opinions_qa_users_responses` | non declaree | non | **individuel**, colonnes = items ATP | derive OpinionQA, pratique |
| `andrewsiah/opinions_qa_questions_answers_dict` | non declaree | non | questions | complement |
| `timchen0618/OpinionQA` | MIT | non | questions, jsonl | leger |
| `oxford-llms/world_values_survey_2017_2022_sft` | Apache 2.0 | non | **individuel**, format SFT | WVS sans formulaire |
| `PiLabZJU/AlignSurvey_Datasets` | MIT | non | **depot vide** | annonce 44 K entretiens, ne contient que README et .gitattributes au 2 sept 2026 |
| `tatsu-lab/opinions_qa` (GitHub) | **aucune** | - | code seul | donnees sur CodaLab |
| `joonspk-research/genagents` (GitHub) | MIT | - | code + 3 505 personas | moteur de Stanford |
| `josephjeesungsuh/subpop` (GitHub) | BSD 3-Clause | - | pipeline de curation | montre comment repartir des `.sav` Pew bruts |
| `Demon702/WorldValuesBench` (GitHub) | non verifiee | - | benchmark WVS7 | a inspecter |
| `tianyipeng-lab/Digital-Twin-Simulation` (GitHub) | non verifiee | - | pipeline Twin-2K-500 | a inspecter |

[CONFIRME] pour toutes les licences, l'etat gated et le nombre de fichiers : verifies un a
un via `https://huggingface.co/api/datasets/<id>`.

**Point important sur GlobalOpinionQA.** Le brief le cite comme piste. Il faut trancher :
son fichier unique `data/global_opinions.csv` contient, par question, un dictionnaire
`selections` dont la cle est un nom de pays et la valeur le pourcentage de repondants ayant
choisi chaque modalite. **Il n'y a aucun individu.** Ce jeu mesure l'alignement d'un modele
sur des distributions nationales, ce qui est exactement le probleme que le projet veut
depasser. Il sert de contre exemple methodologique, pas de source de donnees.
[CONFIRME] par la carte du dataset.

**Point important sur SubPOP.** Meme logique : SubPOP-Train et SubPOP-Eval sont des
distributions de reponses au niveau de sous populations, tirees des vagues ATP 61 a 132 et
du GSS 2022. C'est de l'agrege. Son interet reel est ailleurs : le depot GitHub documente
**comment reconstruire un jeu individuel a partir des `.sav` bruts de Pew**, en donnant
l'URL amont et la convention de nommage (`ATP W132.sav`). C'est une recette gratuite pour
etendre OpinionQA aux vagues 2022-2025. [CONFIRME] lecture du README.

---

## 3. Ce qui se telecharge en trois minutes, sans compte

Liste operationnelle. Toutes les URL ci dessous ont ete verifiees par requete HTTP le
2 septembre 2026 et renvoient un code 200 sans authentification.

```
# 0. Archive OSF de replication, 3,4 Mo, 1 052 participants, 2 vagues
curl -L -o replication_instructions.rar https://osf.io/download/s2u7c/
unar replication_instructions.rar     # ou: bsdtar -xf replication_instructions.rar

# 1. Twin-2K-500, le second pilier
huggingface-cli download LLM-Digital-Twin/Twin-2K-500 --repo-type dataset

# 2. OpinionQA, reponses individuelles Pew, 210 Mo
curl -L -o human_resp.tar.gz \
  https://worksheets.codalab.org/rest/bundles/0x050b7e72abb04d1f9b493c1743e580cf/contents/blob/
curl -L -o model_input.tar.gz \
  https://worksheets.codalab.org/rest/bundles/0xa6f81cc62d7d4ccb93031a72d2043669/contents/blob/

# 3. GSS cumule 1972-2024, 47,5 Mo
curl -L -O https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip

# 4. GSS Panel 2016-2020, 11,8 Mo
curl -L -O https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_2020_panel_stata_1a.zip

# 5. Barometre CEVIPOF, vague 16, 4 pays
curl -L -o baro_v16.tab https://data.sciencespo.fr/api/access/datafile/10529
curl -L -o baro_v16_quali.docx https://data.sciencespo.fr/api/access/datafile/10525

# 6. Arcom 2026, edition posterieure a la coupure des modeles
curl -L -O https://static.data.gouv.fr/resources/les-francais-et-linformation-barometre/20260604-074907/2026-les-francais-et-linformation-2eme-edition-arcom-base-anonymisee-complete.csv

# 7. Moteur d'agents de Stanford + 3 505 personas GSS
git clone https://github.com/joonspk-research/genagents

# 8. INSEE, population synthetique francaise
curl -L -O https://www.insee.fr/fr/statistiques/fichier/8632441/FD_EEC_2024.parquet
```

Volume total : environ 400 Mo hors `runs` d'OpinionQA. Cout : zero. Humains recrutes : zero.
Le premier telechargement de la liste, l'archive OSF, pese 3,4 Mo et suffit a produire un
premier resultat quantitatif le jour meme.

---

## 4. Ce qui demande une demarche, avec les delais

| Ressource | Type de demarche | Affiliation exigee | Delai estime | Confiance |
|---|---|---|---|---|
| ESS | compte gratuit en ligne, eduGAIN ou Google ou email | non | immediat a 24 h | [PROBABLE] |
| ANES | formulaire d'inscription, email de confirmation | non | immediat a 24 h | [PROBABLE] |
| GESIS / EVS | compte catalogue | non | immediat a 24 h | [PROBABLE] |
| WVS | formulaire de telechargement, acceptation des conditions | non | immediat | [PROBABLE] |
| HRS | inscription en ligne | non | immediat | [PROBABLE] |
| PSID | inscription en ligne | non | immediat | [PROBABLE] |
| `jjssuh/subpop` | demande manuelle sur Hugging Face | non | quelques jours | [CONFIRME] `gated: manual` |
| Pew ATP vagues brutes | non determine | non determine | non determine | [NON VERIFIE] |
| LISS | declaration signee en ligne | non exigee explicitement | **5 jours ouvres** | [CONFIRME] |
| UAS (USC) | compte avec **email institutionnel**, accord signe pour le restreint | oui de fait | quelques jours | [PROBABLE] |
| UK Data Service | demande d'identifiant pour non britanniques | non, mais restrictions par collection | quelques jours | [CONFIRME] |
| CDSP, fichiers ENEF restreints | demande d'acces via le Dataverse | non determine | non determine | [NON VERIFIE] |
| Progedo-ADISP (CEREQ, INSEE FPR) | **email institutionnel obligatoire**, formulaires signes scannes, CSS pour les FPR | **oui, bloquant** | non precise | [CONFIRME] pour l'exigence |
| SHARE | inscription + justification de la pertinence, rattachement a une organisation de recherche | oui | semaines | [PROBABLE] |
| SOEP | contrat de diffusion DIW + **38 euros de DVD** | oui | ~14 jours | [PROBABLE] |
| American Voices Project | dossier de projet, serveur securise Stanford | non exigee explicitement | **plusieurs mois** | [CONFIRME] |
| Banque 1 000 agents, Park et al. | email aux auteurs, examen ethique, **aucun formulaire public** | non determine | inconnu, potentiellement long | [CONFIRME] pour l'absence de formulaire |
| NielsenIQ / Kilts | abonnement payant, eligibilite US titulaire | oui + argent | sans objet | [CONFIRME] |

### Ou le contact MIT de Simon change la donne

Par ordre de rendement decroissant :

1. **La banque des 1 000 agents de Stanford.** Il n'existe aucun formulaire public. Le seul
   chemin est un email a Joon Sung Park. Un email envoye par un chercheur du MIT connu des
   auteurs a un taux de reponse sans commune mesure avec un email froid. **C'est le
   principal usage a faire du contact.** [HYPOTHESE] sur le taux de reponse, [CONFIRME] sur
   l'absence de formulaire.
2. **American Voices Project.** Dossier evalue par l'equipe des investigateurs principaux,
   plusieurs mois. Un co signataire academique credibilise le dossier et permet de repondre
   a la question "pertinence de la recherche". Le serveur securise est deja equipe d'Ollama,
   donc notre protocole y est techniquement realisable.
3. **Progedo-ADISP, donc CEREQ et les fichiers production recherche de l'INSEE.**
   L'exigence d'une adresse mail institutionnelle et d'un rattachement a une unite de
   recherche est **explicite et bloquante**. Sans co signataire academique, cette porte
   est fermee. Avec, elle est gratuite et l'habilitation est illimitee dans le temps.
4. **UAS de USC**, meme logique d'email institutionnel.
5. **NielsenIQ.** Verifier si le MIT est deja abonne au Kilts Center. Si oui, l'acces passe
   par un enseignant chercheur titulaire local, sans depense pour nous. [HYPOTHESE].
6. **SHARE et SOEP**, ou la justification academique est demandee.

---

## 5. Contamination : evaluation par jeu de donnees et parades

### 5.1 Ce qui est en jeu

Si le corpus d'entrainement du modele contient deja les reponses individuelles, ou meme
seulement les distributions marginales de chaque question, alors une partie de notre score
mesure de la memorisation et non de l'inference sur le persona. Le risque n'est pas
symetrique : la contamination **gonfle** la performance moyenne et, surtout, elle peut
**gonfler differemment** selon les sous groupes, ce qui pollue directement la contribution
scientifique visee, la variance inter individuelle.

Repere : la coupure de connaissance du modele utilise ici est mai 2026. Tout ce qui est
public avant cette date est suspect par defaut.

### 5.2 Evaluation par jeu

| Jeu | Risque de contamination | Raisonnement | Effet sur nos mesures |
|---|---|---|---|
| **GSS** | **eleve sur les questions, moyen sur les marges, faible sur les individus** | Le codebook, le libelle exact de chaque item et des dizaines de milliers d'articles citant les distributions sont sur le web depuis des annees. Les microdonnees sont dans des `.zip` de `.dta` binaires, peu susceptibles d'etre tokenises. [PROBABLE] | Le modele connait la question et sa distribution nationale. Il ne connait vraisemblablement pas la ligne du repondant. Le biais pousse vers la reponse modale, donc **ecrase la variance**, ce qui est exactement le defaut que nous voulons mesurer. Risque de confondre defaut du modele et contamination. |
| **OpinionQA** | **tres eleve sur les questions** | Papier de mars 2023, plus de 120 etoiles GitHub, benchmark extremement cite, integre a HELM. Les 500 questions clivantes ont ete reproduites dans des dizaines de papiers. [PROBABLE] | Idem GSS, en pire. En revanche les `responses.csv` individuels sont dans un `tar.gz` de 210 Mo sur CodaLab, jamais rendu en HTML. Contamination des individus peu probable. [HYPOTHESE] |
| **Archive OSF `t6g7k`** | **moyen** | Archive publique depuis le 21 avril 2026, soit environ un mois avant la coupure de mai 2026. Fenetre d'ingestion tres courte, et le contenu est enferme dans un `.rar` unique, format que les crawleurs de corpus texte traitent rarement. [PROBABLE] | Risque reel mais faible. La parade est integree : la colonne `p_wave1__p_wave2__accuracy` donne le plafond humain par individu ; tout agent qui le depasse signale une fuite. En revanche les **items du GSS eux memes** sont massivement contamines, comme partout. |
| **Twin-2K-500** | **moyen a eleve** | Publie en mai 2025 sur arXiv et sur Hugging Face en CC BY 4.0, format parquet et csv, donc **potentiellement crawle**. 1 776 telechargements. [PROBABLE] | C'est le principal danger de notre jeu numero un. Attenuation structurelle : le design test retest fournit un plafond humain ; si le modele memorise, il devrait **depasser** le plafond test retest humain, ce qui est detectable. C'est un test de contamination gratuit et elegant. |
| **ANES** | eleve sur les questions | Meme logique que le GSS. Mais l'etude 2024 Time Series n'a ete diffusee en version complete qu'en aout 2025. [PROBABLE] | Les open-ends redacted sont du texte libre, tres peu susceptible d'avoir ete appris item par item. |
| **WVS / EVS / ESS** | eleve sur les questions et les marges nationales | GlobalOpinionQA a explicitement mis les distributions par pays du WVS et du Pew Global Attitudes Survey en CSV ouvert. **Anthropic les a publiees en CC BY-NC-SA sur Hugging Face.** [CONFIRME] | Pour le WVS, les marges par pays sont presque certainement dans les corpus. Toute mesure d'alignement agrege sur le WVS est suspecte. |
| **Barometre CEVIPOF, ENEF, Arcom, INSEE** | **faible** | Corpus francais, formats `.tab` et `.xls` derriere une API Dataverse, faible notoriete internationale, quasi aucune reprise en anglais. [PROBABLE] | C'est le materiau le plus propre dont nous disposions. |
| **Arcom edition 2026** | **tres faible** | **Publiee le 4 juin 2026, apres la coupure de mai 2026.** [CONFIRME] date de publication de la ressource. | Test quasi vierge. |
| **dunnhumby, Instacart** | moyen | Tres presents sur Kaggle et dans des centaines de notebooks GitHub. Mais ce sont des identifiants de produits et des sequences numeriques, mal memorisables. [PROBABLE] | Faible impact. |

### 5.3 Parades, par ordre de rapport efficacite sur cout

1. **Le test du plafond test retest.** Sur Twin-2K-500, calculer d'abord la fidelite test
   retest humaine vague 3 contre vague 4, item par item. Toute prediction du modele qui
   **depasse** ce plafond sur un item est un signal de fuite, pas de performance. Cout :
   zero, c'est une simple comparaison de deux colonnes deja fournies dans le dataset.
   C'est la parade la plus rentable et elle est disponible immediatement.
2. **Sonde de memorisation a persona vide.** Pour chaque question, interroger le modele
   **sans aucun persona** et lui demander la distribution des reponses. Si la distribution
   predite colle a la distribution reelle de l'echantillon a moins de deux points, la
   question est contaminee. Retirer ces items de l'evaluation, ou les traiter comme un
   sous ensemble separe. Cout : un appel par question, environ 1 500 appels pour OpinionQA,
   faisable en local avec un modele ouvert.
3. **Sonde de completion.** Donner les 15 premiers mots du libelle exact d'une question et
   mesurer si le modele complete verbatim. Cout quasi nul, discrimine bien les items
   celebres.
4. **Vagues posterieures a la coupure.** Par ordre de disponibilite gratuite :
   Arcom edition 2026 (4 juin 2026), Barometre CEVIPOF vague 17 (fevrier 2026), GSS
   release 3a (juillet 2026), vagues ATP Pew de 2025 et 2026, ESS round 11 edition 4.0.
   Constituer un **jeu de validation strictement post coupure**, meme petit, et rapporter
   systematiquement les deux chiffres : performance sur le jeu contamine, performance sur
   le jeu propre. **L'ecart entre les deux est en soi un resultat publiable** et repond par
   avance a l'objection numero un d'un relecteur.
5. **Reformulation.** Reecrire chaque question en francais, ou la paraphraser en conservant
   la structure des modalites, puis mesurer la chute de performance. Une chute forte signale
   une memorisation de surface. Cout : un appel de reformulation par question.
6. **Basculer sur le francais.** Le corpus CEVIPOF et l'INSEE offrent un terrain ou la
   contamination est structurellement plus faible. Le cout est un travail de traduction du
   pipeline, pas d'argent.
7. **Jeux peu connus.** LISS, UAS et les enquetes Generation du CEREQ sont beaucoup moins
   repris que le GSS. A garder en reserve pour la validation finale.

### 5.4 Ce que je recommande d'ecrire dans le papier

Ne pas presenter un seul chiffre de performance. Presenter systematiquement un triplet :
performance brute, performance sur items non contamines selon la sonde a persona vide,
performance sur jeu post coupure. Une equipe qui fait cela se distingue immediatement de la
litterature existante, ou ce controle est presque toujours absent. [HYPOTHESE] sur
l'absence generale de ce controle, fondee sur le fait qu'aucune des recherches menees ici
n'a fait remonter de travail liant explicitement contamination et simulation de repondants.

---

## 6. Recommandation : les jeux a attaquer, dans l'ordre, et la premiere experience de chacun

### Rang 1. Archive OSF `t6g7k`

**Pourquoi.** Parce qu'elle donne, en un `curl` de 3,4 Mo et sans compte, les trois choses
que le projet cherche en meme temps : la verite terrain humaine individuelle sur
177 items du GSS, le denominateur test retest par individu grace a la seconde vague, et
cinq conditions d'agents de reference deja calculees, dont une fondee sur entretien. Aucun
autre jeu de l'inventaire ne reunit les trois. Le volume est ridicule, le temps de mise en
route se compte en minutes, et le resultat est directement comparable a un papier existant.

**Fichiers a telecharger, noms exacts.**
```
curl -L -o replication_instructions.rar https://osf.io/download/s2u7c/
unar replication_instructions.rar
```
Puis, dans `replication_instructions/` :
- `figure2/data/new_analysis_summaries/gss_filtered/preparation/p_wave1_summary.csv`
- `figure2/data/new_analysis_summaries/gss_filtered/preparation/p_wave2_summary.csv`
- `figure2/data/new_analysis_summaries/gss_filtered/preparation/gss_v6_summary.csv`
  (condition demographie seule, notre plancher)
- `figure2/data/new_analysis_summaries/gss_filtered/preparation/composite_agents_summary.csv`
  (condition questionnaire + entretien, notre plafond de reference)
- `figure2/data/new_analysis_summaries/gss_filtered/analysis/individual_level.csv`
- `figure2/data/question_master/gss/main.csv`
- `figure3/data/demographic_summary.csv`

**Premiere experience, lancable demain, sans humain et sans budget.**
Titre : *Le meme plafond, une variance differente.*
1. Recalculer, sans aucun appel de modele, la figure 2 du papier a partir des CSV fournis.
   Cela valide notre lecture des donnees et nous donne les chiffres de reference exacts.
   Duree : une heure.
2. Calculer, pour chaque condition d'agent, non pas la moyenne des exactitudes mais
   **l'ecart type inter individuel des reponses predites**, item par item, et le comparer a
   l'ecart type inter individuel des reponses humaines de la vague 1. L'hypothese du projet
   est que toutes les conditions, y compris la meilleure, sous estiment cette dispersion.
   **Ce calcul n'exige aucun modele, aucune API, aucun euro : les sorties d'agents sont
   deja dans les CSV.** C'est le resultat le plus rapide a produire de tout le projet.
3. Croiser avec `demographic_summary.csv` pour savoir **quels sous groupes sont ecrases**.
   Si l'ecrasement de variance est concentre sur certains profils, c'est une contribution
   nette et facile a defendre.
4. Reproduire ensuite le tout avec un modele ouvert local sur les memes 1 052 personas
   demographiques, pour verifier qu'un modele gratuit atteint le meme plancher que GPT-4o.
   Si oui, la contrainte budget zero cesse d'etre une contrainte scientifique.

**Reserve.** Aucune licence declaree, et l'intervalle entre les deux vagues est inconnu.
Les deux points doivent etre eclaircis avant publication.

### Rang 2. Twin-2K-500

**Pourquoi.** C'est le seul jeu public, gratuit et sans compte qui reunit les cinq criteres
du brief : individus reels, attributs riches, grand nombre de questions par individu, suivi
longitudinal avec retest, et une baseline LLM deja publiee. Il fournit gratuitement le
denominateur du score normalise de Stanford, ce qui evite de recruter qui que ce soit.

**Fichiers a telecharger, noms exacts.**
```
huggingface-cli download LLM-Digital-Twin/Twin-2K-500 --repo-type dataset --local-dir ./twin2k
```
puis, dans `./twin2k` :
- `question_catalog_and_human_response_csv/question_catalog.json`
- `question_catalog_and_human_response_csv/wave1_3_response_label.csv`
- `question_catalog_and_human_response_csv/wave4_response_label.csv`
- `LLM_simulation_results/GPT4.1-mini-simulation-llm-vs-human/responses_wave4_formatted.csv`
- configuration `wave_split` via `load_dataset("LLM-Digital-Twin/Twin-2K-500", "wave_split")`

**Premiere experience, lancable demain, sans humain et sans budget.**
Titre : *Le plafond humain et la variance ecrasee.*
1. Calculer, item par item sur les 127 colonnes de la vague 4, la fidelite test retest
   humaine en comparant `wave4_Q_wave1_3_A` et `wave4_Q_wave4_A`. C'est le denominateur.
   Aucune API, aucun modele, du pandas.
2. Construire trois conditions de persona a partir de `wave_split` :
   (a) demographie seule, (b) `wave1_3_persona_text` complet, (c) `persona_summary`.
3. Interroger un modele ouvert execute en local sur les questions de la vague 4, cent
   individus pour commencer, dix repetitions par individu pour estimer la variance intra.
4. Rapporter trois quantites : le score normalise par le plafond test retest, l'ecart type
   inter individuel predit contre l'ecart type inter individuel reel, et le nombre d'items
   ou le modele **depasse** le plafond humain, qui est notre indicateur de contamination.
Le point 4, deuxieme quantite, **est la contribution scientifique du projet**. Elle est
mesurable des la premiere semaine, sur donnees publiques, sans depenser un euro.
5. Comparer au passage a la baseline GPT-4.1-mini fournie dans le depot, ce qui donne
   gratuitement un point de comparaison avec l'etat de l'art publie.

### Rang 3. OpinionQA, bundle `human_resp`

**Pourquoi.** C'est le passage a l'echelle. Quinze vagues, environ 1 500 questions, des
dizaines de milliers de repondants, des reponses deja en langage naturel, et douze
attributs de persona propres. C'est aussi le benchmark de reference de la litterature, donc
le terrain sur lequel un relecteur attend de nous voir des chiffres.

**Fichiers a telecharger, noms exacts.**
```
curl -L -o human_resp.tar.gz \
  https://worksheets.codalab.org/rest/bundles/0x050b7e72abb04d1f9b493c1743e580cf/contents/blob/
curl -L -o model_input.tar.gz \
  https://worksheets.codalab.org/rest/bundles/0xa6f81cc62d7d4ccb93031a72d2043669/contents/blob/
tar xzf human_resp.tar.gz
```
Puis travailler sur
`human_resp/Pew_American_Trends_Panel_disagreement_500/info.csv` pour les 500 questions les
plus clivantes, et sur `human_resp/American_Trends_Panel_W92/responses.csv` (40 Mo, la vague
la plus riche) plus `metadata.csv` et `info.csv` de la meme vague.

**Premiere experience, lancable demain.**
Titre : *Prediction intra individuelle avec questions tenues secretes.*
1. Sur la vague W92, pour chaque repondant, tirer aleatoirement 80 pour cent de ses reponses
   pour construire le persona et **tenir les 20 pour cent restantes secretes**. Le persona
   est donc, comme chez Stanford, un texte, pas un vecteur de cases.
2. Ajouter les 12 attributs socio demographiques de `metadata.csv`.
3. Predire les reponses tenues secretes, avec un modele ouvert local.
4. Comparer a trois references : le hasard pondere par les marges, la reponse modale du
   sous groupe demographique du repondant, et le modele.
5. Mesurer separement la performance sur les 500 questions clivantes et sur les autres.
   L'hypothese a tester est que l'ecart modele contre reponse modale du sous groupe **se
   reduit** sur les questions clivantes, ce qui serait la demonstration quantitative de
   l'ecrasement de variance.
Aucune contrainte de licence bloquante pour un usage de recherche, mais **verifier les
conditions Pew avant toute publication**.

### Rang 4. GSS, fichier cumule plus panel 2016-2020

**Pourquoi.** C'est l'instrument exact du papier de reference. Le panel donne un second
denominateur test retest, a deux et quatre ans, a comparer avec les deux semaines de
Twin-2K-500. Et les 3 505 personas GSS de `genagents` permettent de rejouer le moteur de
Stanford tel quel, gratuitement, en substituant un modele local a l'appel OpenAI.

**Fichiers a telecharger, noms exacts.**
```
curl -L -O https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip
curl -L -O https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_2020_panel_stata_1a.zip
curl -L -O "https://gss.norc.org/content/dam/gss/get-documentation/pdf/codebook/2016-2020%20GSS%20Panel%20Codebook%20-%20R1.pdf"
git clone https://github.com/joonspk-research/genagents
```
Dans `genagents`, remplacer `simulation_engine/gpt_structure.py` par un client compatible
avec un modele ouvert local, et pointer `POPULATIONS_DIR` sur
`agent_bank/populations/gss_agents`, qui contient 3 505 agents.

**Premiere experience, lancable demain.**
Titre : *Le plafond humain a deux ans, et la baseline demographique de Stanford.*
1. Sur le panel 2016-2020, identifier les items du coeur GSS poses a l'identique aux deux
   vagues, et calculer la stabilite intra individuelle. On obtient un plafond test retest
   a horizon de deux et quatre ans, sur l'instrument du papier de reference.
2. Faire tourner le moteur `genagents` non modifie sur les 3 505 personas demographiques,
   avec un modele ouvert local, sur ces memes items.
3. Rapporter le score normalise obtenu avec **la demographie seule**. C'est le plancher
   contre lequel toute la valeur ajoutee d'un persona construit sur un entretien doit etre
   mesuree. Sans ce plancher, aucun chiffre du projet n'est interpretable.
4. Question a instruire au passage : le plafond test retest a deux ans est necessairement
   plus bas que le plafond a deux semaines. Le score normalise de Stanford depend donc du
   delai de retest choisi. **Si ce point n'est pas deja traite dans la litterature, c'est
   une critique methodologique forte et facile a documenter.** [HYPOTHESE].

### Le cinquieme, non classe mais a lancer en parallele : le francais

Telecharger le meme jour `https://data.sciencespo.fr/api/access/datafile/10525` et le CSV
Arcom 2026. Deux raisons. D'abord, l'edition Arcom du 4 juin 2026 est posterieure a la
coupure des modeles, elle constitue notre unique jeu de validation propre. Ensuite, si le
fichier 10525 contient des transcriptions d'entretiens appariables a la base quantitative
de la vague 16 du barometre, alors nous disposons du seul corpus francais de type Stanford
en acces libre, et le projet peut se positionner sur un terrain que personne n'occupe.

### Les deux emails a envoyer le meme jour

Ils ne coutent rien et leurs delais sont longs, donc ils doivent partir en premier.
1. Joon Sung Park, joonspk@stanford.edu, pour l'acces a la banque des 1 000 agents.
   **Par le canal MIT de Simon**, pas en direct.
2. americanvoicesproject@stanford.edu et le formulaire de projet, pour l'American Voices
   Project. Delai annonce : plusieurs mois. Chaque semaine de retard est une semaine perdue.

---

## 7. Ce que je n'ai pas pu verifier

1. **L'identite exacte du papier associe a l'archive OSF `t6g7k`.** Le titre est
   "LLM Agents Grounded in Self-Reports Enable General-Purpose Simulation of Individuals",
   le seul contributeur liste est Jonne Kamphorst, l'archive date du 21 avril 2026. Je n'ai
   pas retrouve la publication correspondante, ni verifie s'il s'agit d'une equipe liee a
   Park et al. **Ne pas citer ce jeu sans avoir identifie le papier.**
2. **L'intervalle de temps entre la vague 1 et la vague 2 de l'archive OSF.** Aucune date
   dans les fichiers inspectes. Or le denominateur du score normalise en depend
   directement. C'est la lacune la plus genante de ce jeu par ailleurs excellent.
3. **La licence de l'archive OSF.** `node_license: null` et aucun fichier LICENSE dans les
   203 entrees. Absence de licence, pas licence permissive.
4. **Le nombre exact de repondants par vague dans OpinionQA.** J'ai verifie la taille des
   fichiers et la structure, pas le comptage de lignes, qui suppose de telecharger les
   210 Mo. Ordre de grandeur deduit des tailles : quelques milliers a une dizaine de
   milliers par vague.
5. **Les conditions d'usage exactes que le Pew Research Center impose** sur les
   microdonnees de l'American Trends Panel, y compris redistribuees via OpinionQA. La page
   des jeux de donnees ATP renvoie a info@pewresearch.org sans detailler.
6. **Si un compte est necessaire pour telecharger les `.sav` bruts de l'ATP.** Le depot
   SubPOP suggere que non, la page Pew ne le dit pas.
7. **Le contenu reel du fichier CDSP `10525`**, "Data Quali Entretiens IA Semi Directifs
   Vague 16". Je sais qu'il est telechargeable sans compte et qu'il pese 272 659 octets au
   format docx. Je ne sais pas s'il contient des transcriptions integrales, ni si un
   identifiant permet de les apparier a la base quantitative de la meme vague. **C'est la
   verification a plus fort rendement de tout ce rapport.**
8. **Le nombre de repondants et de variables du jeu Arcom**, et si des questions ouvertes y
   figurent. Le CSV pese 14,7 Mo, ce qui suggere plusieurs milliers de repondants.
9. **Les pages de telechargement du World Values Survey et de l'European Social Survey.**
   Les deux sites chargent leur contenu dynamiquement et l'outil de recuperation a renvoye
   des pages vides. Les conditions decrites viennent de sources secondaires convergentes,
   pas des pages officielles. Je n'ai donc **pas d'URL de fichier verifiee** pour ces deux
   sources, et je me refuse a en inventer une.
10. **Le chiffre de 87 pour cent** attribue a Twin-2K-500 comme part de la reference test
   retest atteinte par les jumeaux numeriques. Il vient d'un resume, pas du resume verbatim
   du papier que j'ai recupere.
11. **Les chiffres du panel GSS 2016-2020** (2 867, 2 146, 2 348) proviennent d'un resume du
   codebook, pas de ma lecture du PDF.
12. **Le delai de traitement d'une demande Progedo-ADISP**, et celui d'une demande d'acces
   aux fichiers restreints ENEF via le Dataverse du CDSP.
13. **Si le SOEP propose une diffusion par telechargement** sans les 38 euros de DVD.
14. **Si le MIT est abonne au Kilts Center**, ce qui ouvrirait NielsenIQ sans depense.
15. **La licence exacte des donnees OpinionQA.** Le depot GitHub n'a aucun fichier LICENSE
    et l'API GitHub renvoie `license: null`. Ce n'est pas une licence permissive implicite,
    c'est une absence de licence, ce qui est juridiquement plus restrictif, pas moins.
16. **Le statut de l'enquete Budget de famille de l'INSEE** : fichier detail en libre
    telechargement ou diffusion via Progedo.
17. **Le contenu de `Demon702/WorldValuesBench` et de `tianyipeng-lab/Digital-Twin-Simulation`.**
    Identifies mais non inspectes.
18. **Le lien arXiv donne dans CONTEXTE.md**, https://arxiv.org/html/2603.28066v1, n'a pas
    ete verifie dans le cadre de cette mission. Les references de Park et al. que j'ai
    trouvees sont le depot GitHub `joonspk-research/genagents` et le depot Stanford
    `purl.stanford.edu/jm164ch6237`. Un autre agent de l'exploration devrait trancher.

---

## 8. Questions ouvertes pour Simon

1. **Sais tu qui est derriere l'archive OSF `t6g7k` ?** Le papier s'appelle "LLM Agents
   Grounded in Self-Reports Enable General-Purpose Simulation of Individuals", contributeur
   liste Jonne Kamphorst, depot du 21 avril 2026. C'est le meilleur jeu de donnees de tout
   l'inventaire et il est en acces libre total. Deux questions en decoulent : d'ou vient il,
   et est ce une equipe avec laquelle une collaboration serait plus rapide qu'avec Stanford.

2. **Le contact MIT peut il porter un email a Joon Sung Park ?** C'est le seul chemin vers
   la banque des 1 000 agents, il n'existe aucun formulaire public. Quelle est la nature
   exacte du lien : co auteur, ancien collegue, simple relation de reseau ? La formulation
   de l'email en depend entierement.

3. **Le co signataire academique existe il, et son adresse institutionnelle peut elle etre
   utilisee pour les demandes de donnees ?** Ce n'est pas une question de forme. Progedo,
   UAS et SHARE exigent une adresse mail institutionnelle et un rattachement a une unite de
   recherche. Sans cela, tout le pan francais du CEREQ et de l'INSEE en fichiers production
   recherche est ferme, et le pan americain se limite a ce qui se telecharge sans compte.

4. **Faut il deposer le dossier American Voices Project maintenant ?** Le delai annonce est
   de plusieurs mois. Si nous visons une publication conjointe avec le MIT, un dossier
   depose en septembre 2026 arrive peut etre juste a temps ; un dossier depose en janvier
   arrive trop tard. Leur serveur est deja equipe d'Ollama, donc le protocole y est
   techniquement realisable sans sortie de donnees.

5. **Twin-2K-500 change il le plan de recherche ?** Le brief supposait que la matiere
   humaine manquait. Elle ne manque plus : 2 058 individus, 500 questions, une vague de
   retest, licence CC BY 4.0, aucun compte. La question n'est plus "comment obtenir des
   donnees" mais "sur quoi apporter une contribution que Toubia et al. n'ont pas deja
   apportee". Ma proposition est la variance inter individuelle, qu'ils mesurent peu et que
   le brief identifie comme la limite de la litterature. Est ce le bon angle ?

6. **Le denominateur du score normalise depend du delai de retest.** Deux semaines dans
   Twin-2K-500, deux a quatre ans dans le panel GSS. Un score normalise a deux semaines
   n'est pas comparable a un score normalise a deux ans, et le second sera mecaniquement
   plus flatteur. Le papier de Stanford precise il son delai ? Si la litterature ne
   controle pas ce point, c'est une critique methodologique forte, facile a documenter, et
   qui donne un angle de publication distinct.

7. **Sur la publication du controle de contamination.** Je recommande de rapporter
   systematiquement trois chiffres au lieu d'un : performance brute, performance sur items
   non contamines, performance sur jeu post coupure. Cela affaiblit le chiffre d'affiche
   mais rend le resultat defendable. Est ce compatible avec l'ambition de presenter des
   resultats forts au MIT, ou faut il d'abord un chiffre simple ?

8. **Y a t il une objection ethique ou juridique a utiliser OpinionQA ?** Le depot n'a
   aucune licence, les donnees appartiennent au Pew Research Center. Pour un usage de
   recherche interne, le risque est faible. Pour une publication, et a fortiori pour la
   demonstration commerciale evoquee dans le brief, il faut trancher. Quelqu'un au MIT
   connait il la position de Pew ?

9. **Le corpus francais est il un atout ou une distraction ?** Le barometre CEVIPOF est
   gratuit, sans compte, longitudinal sur 17 vagues, contient des verbatims et
   possiblement des entretiens semi directifs, et il est presque certainement absent des
   corpus d'entrainement anglophones. C'est notre meilleure protection contre la
   contamination. Mais un papier sur donnees francaises se vend moins bien dans une revue
   americaine. Faut il en faire l'axe principal, ou seulement le jeu de validation ?
