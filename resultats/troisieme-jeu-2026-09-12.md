# Troisième jeu de données : vérification à la source (12 septembre 2026)

Suite à `resultats/inventaire-donnees-2026-09-12.md`, qui laissait le pairage individuel d'OSF
`f7na8` **[NON VÉRIFIÉ]** faute de navigateur. Cette session dispose d'un navigateur en
lecture seule et a ouvert l'arborescence de fichiers réelle du dépôt, plus les scripts R
qu'il contient (récupérés en lecture, non enregistrés dans `data/`). Aucun compte créé,
aucun formulaire rempli, aucune condition acceptée, rien écrit hors de ce fichier.

---

## Tâche 1 — OSF `f7na8` (Zhang, Xu & Alvero 2025, *Sociological Methods & Research*)

Source : https://osf.io/f7na8/files/ (arborescence ouverte manuellement dans le navigateur)
et l'API publique `https://api.osf.io/v2/nodes/f7na8/...` (métadonnées + contenu des
scripts `.R`, tous en lecture seule).

### 1. Contenu du dépôt
Un seul dossier racine, `aisurv_osf/`, avec quatre sous-dossiers :
- **`code/`** — 10 scripts R numérotés `01_...` à `09_...` (nettoyage, simulation LLM,
  appariement, analyse textuelle, similarité, déshumanisation).
- **`data/`** — porte les données :
  - `all_prolific_cleaned.RDS` (1,2 Mo) — nouveaux répondants Prolific (2025)
  - `claude_sims_init.RDS` (549 Ko), `gpt_sims_init.RDS` (1,8 Mo), `gemini_sims_init.RDS`
    (445 Ko) — réponses générées par trois LLM
  - `final_llm_responses.RDS` (1,5 Mo) — fichier consolidé des réponses LLM
  - `noAI_Responses - noAI.csv` — réponses humaines sans assistance IA
  - `Graham1155/`, `GroenendykS79/`, `JardinaS61/` — trois enquêtes TESS originales
    (2019-2020, pré-ChatGPT), chacune avec son `.sav`/`.dta` brut, codebook, rapport de
    terrain et IRB
  - `glove.6B.100d.txt` (347 Mo, embeddings GloVe) et `mfd.csv` (dictionnaire de fondations
    morales) — outils d'analyse de texte, pas des données de réponse
  - **`docs/`** et **`output/`** — un PDF d'instructions de codage manuel, et des sorties
    d'analyse.

### 2. Appariement individuel : **NON, confirmé par le code lui-même**
C'est la question décisive, et la réponse est négative — pas seulement faute de preuve, mais
positivement démontrée par les scripts :
- `06_match_prolific_tess.R` associe les nouveaux répondants Prolific aux trois enquêtes
  TESS **par groupe démographique**, pas par identité :
  ```r
  mvars <- c("race_recode", "educ_recode", "age_recode")
  mvars_with_party <- c(mvars, "party_recode")
  prompts_aa_m <- prompts_aa |> left_join(jardina, by = c(mvars_with_party, "mind_version"))
  ```
  Chaque répondant Prolific est joint à *tous* les répondants TESS partageant les mêmes
  tranches de race/éducation/âge(/parti), puis un seul est **tiré au hasard** parmi les
  correspondances. Ce n'est pas un identifiant commun ni une correspondance individuelle
  explicite : c'est un appariement statistique par cellule démographique, avec sélection
  aléatoire — l'inverse de ce qu'il nous faut.
- `04_simulate_responses_init.R` confirme côté génération LLM : le prompt envoyé à l'API est
  le texte brut (`text = prompt`), sans variable démographique ni identifiant individuel
  injecté dans le prompt ; `prompt_id = paste0(question, "-", ResponseId)` sert seulement à
  retrouver la ligne en sortie, pas à personnaliser la génération.

**Verdict : aucun pairage un-à-un. Le jeu ne satisfait pas notre critère décisif.**

### 3. Effectifs
Non documentés de façon centralisée et non trouvés dans le temps imparti (pas de README
global visible sans ouvrir chaque `.docx`/codebook individuellement) ; ce qui est établi :
trois enquêtes TESS distinctes (Graham/political party perceptions, Groenendyk/political
interest, Jardina/associations sur les Afro-Américains) plus une nouvelle vague Prolific
2025, avec trois familles de réponses LLM (Claude, GPT, Gemini). Nombre exact de personnes et
d'items non confirmé — non prioritaire vu le verdict de la section 2.

### 4. Format des réponses
**Texte libre**, pas à choix fermé. Le script `01_prolific_survey_clean.R` montre que les
variables démographiques de filtrage (party, éducation, revenu, usage de l'IA) sont à choix
fermé, mais la variable d'intérêt du papier — celle comparée entre humains et LLM — est la
réponse ouverte envoyée en prompt (`text = prompt`), cohérent avec le titre du papier
(« Open-Ended Survey Responses »). **Incompatible tel quel avec notre attaque actuelle**, qui
travaille sur des items à choix fermé ; il faudrait soit adapter l'attaque au texte libre
(embeddings/similarité, ce que `09_similarity.R` fait déjà côté auteurs), soit écarter ce
jeu pour cette raison seule, indépendamment du problème d'appariement.

### 5. Licence et accès
Confirmé via l'API (`https://api.osf.io/v2/nodes/f7na8/`) : `public: true`, créé le
9 février 2025, **`node_license: null`** — aucune licence déclarée, même régime que l'archive
Park et al. (OSF `t6g7k`). Téléchargement techniquement libre sans compte (fichiers servis
par `files.osf.io` sans authentification), mais l'absence de licence signifie qu'aucun usage
de redistribution n'est couvert explicitement.

**Conclusion Tâche 1 : OSF `f7na8` est écarté.** Pas de pairage individuel humain/IA (démontré
par le code), et format texte libre incompatible avec l'attaque à choix fermé. Les deux
raisons sont indépendantes et suffisent chacune à disqualifier.

---

## Tâche 2 — LISS et British Election Study

- **LISS (Centerdata/Tilburg)** : accès par inscription/signature en ligne, confirmé — c'est
  une infrastructure de panel généraliste (santé, économie, comportement), pas un jeu de
  recherche sur les jumeaux IA. Aucune trace, dans la documentation publique consultée
  (`lissdata.nl/about-us` et résultats de recherche associés), de sorties LLM déjà générées
  et appariées aux panélistes. **Verdict : négatif, ne pas poursuivre.**
- **British Election Study** : téléchargement libre confirmé (panel Internet, ~30 000
  répondants par vague, données ouvertes sur britishelectionstudy.com). C'est un panel
  électoral humain classique ; la recherche n'a trouvé aucune vague ni supplément contenant
  des réponses générées par un LLM appariées aux répondants du panel — seulement des travaux
  externes *utilisant* des données BES pour tester des LLM en simulation, sans fichier de
  sortie apparié publié par le BES lui-même. **Verdict : négatif, ne pas poursuivre.**

Les deux confirment le diagnostic de l'inventaire : accès simple, mais aucun des deux
critères de pairage n'est rempli. Aucune perte de temps supplémentaire justifiée.

---

## Tâche 3 — recherche d'alternatives

Recherches web ciblées (« digital twin survey dataset paired respondent », « synthetic
respondents matched individual panel »). Aucun troisième candidat vérifiable à la source n'a
émergé au-delà de ce que l'inventaire du 12 septembre avait déjà noté :
- Les études « digital twin » citées dans la littérature récente (GSS via interviews
  qualitatives, SOEP allemand, Electric Twin sur des panels britanniques commerciaux) sont
  des **méthodes ou des produits commerciaux**, pas des dépôts de données publics avec
  fichier humain + fichier IA appariés téléchargeable. Aucune URL de dépôt public trouvée
  pour ces trois pistes dans le temps imparti — à ne pas citer comme candidats concrets tant
  qu'un dépôt réel n'est pas localisé.
- Aucun autre nœud OSF, Dataverse ou dépôt institutionnel avec pairage individuel humain/IA
  n'a été identifié en dehors des deux jeux déjà utilisés et d'OSF `f7na8`.

**Aucun candidat de remplacement solide trouvé aujourd'hui.**

---

## Classement final et démarche concrète

1. **Aucun troisième jeu externe ne qualifie aujourd'hui.** OSF `f7na8` est écarté (pas de
   pairage individuel, texte libre). LISS et BES sont écartés (pas de sorties IA du tout).
2. **La piste la plus prometteuse reste celle déjà identifiée dans l'inventaire : la lettre à
   Sean Westwood (Dartmouth)**, demandant le fichier humain apparié aux répondants
   synthétiques d'OSF `ektqr` — brouillon déjà rédigé dans `demandes/`, à compléter (
   affiliation, signature, date) et envoyer. C'est une démarche humaine (écrire/signer/
   envoyer un courriel), pas quelque chose que cette session peut faire : temps estimé,
   quelques minutes de rédaction + délai de réponse du chercheur (jours à semaines,
   incertain).
3. Si aucune réponse de Westwood n'arrive, l'alternative la plus honnête est de **construire
   nous-mêmes des jumeaux** sur un jeu humain déjà propre et libre de droits sur la machine
   (SCE Fed NY ou Ahler-Sood, tous deux CC0/attribution libre) — au prix assumé d'introduire
   notre propre méthode de génération comme facteur confondu, déjà signalé dans l'inventaire.
   Temps : dépend entièrement du budget de génération, pas de la recherche de données.
4. Pas de nouvelle piste externe à explorer dans l'immédiat sans plus d'indices concrets
   (nom d'auteur, DOI) que « digital twin dataset public ».
