# Chasse à un troisième jeu réel avec appariement individuel humain/IA (12 septembre 2026)

Reprend `resultats/inventaire-donnees-2026-09-12.md` et `resultats/troisieme-jeu-2026-09-12.md`, qui
avaient déjà écarté OSF `f7na8` (Zhang, Xu & Alvero — appariement par cellule démographique, texte
libre), LISS et le British Election Study (panels humains sans sortie LLM). Cette passe est allée
chercher dans les paquets de réplication des articles cités par `article/references.bib`, sur
Hugging Face, et dans les bancs d'essai NIST. Recherche web en lecture seule uniquement ; aucun
compte créé, aucun formulaire rempli, rien téléchargé dans `data/`.

---

## 1. Candidat retenu et vérifié : Argyle, Busby, Fulda, Gubler, Rytting & Wingate (2023),
« Out of One, Many: Using Language Models to Simulate Human Samples », *Political Analysis*

- **URL vérifiée** : Harvard Dataverse, DOI `10.7910/DVN/JPV20K`
  (https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/JPV20K —
  interrogé directement via l'API JSON, pas seulement la page web).
- **Équipe** : Brigham Young University (Argyle et al.) — équipe distincte de Toubia/Peng
  (Twin-2K-500) et de Park et al. (OSF `t6g7k`), donc un vrai troisième générateur.
- **Licence** : **CC0 1.0** (domaine public), confirmée dans le champ `license` de l'API Dataverse.
  Aucune inscription requise : les fichiers se téléchargent en accès direct
  (`/api/access/datafile/<id>`, redirigé vers un lien S3 signé mais public).
- **Contenu** : trois études. Seules les études 2 et 3 qualifient (l'étude 1, `gpt3_uber_final.csv`,
  compare des **listes de mots** — texte libre, hors sujet pour notre attaque à choix fermé).
  - Étude 2 (`full_results_2012_2.tab`, `full_results_2016_2.tab`, `full_results_2020_2.tab`) :
    prédiction de vote (Obama/Romney en 2012, etc.) par GPT-3 conditionné sur le profil
    démographique de chaque répondant réel de l'ANES 2012/2016/2020.
  - Étude 3 (`anesgpt3_task3.csv`) : ~13 variables ANES par répondant, réponse réelle **et**
    valeur produite par GPT-3 pour chacune.
- **Format des réponses** : **choix fermé**. Constaté directement dans le fichier téléchargé — les
  valeurs sont des codes entiers (ex. `-9` à `99`), pas du texte.
- **Appariement individuel : CONFIRMÉ, par constat direct du contenu du fichier**, pas par
  déduction. En-tête réel de `anesgpt3_task3.csv` (récupéré en lisant le fichier depuis le lien
  S3 de Dataverse) :
  ```
  "","V160001_orig","V161342","V161310x","V161267","V161270","V161244","V162125x","V162174",
  "V162256","V161126","V161155","V161158x","V162031x","V162062x","age_gpt3","church_goer_gpt3",
  "discuss_politics_gpt3","education_gpt3","gender_gpt3","ideology_gpt3","patriotism_gpt3",
  "pid7_gpt3","political_interest_gpt3","race_gpt3","votechoice_2016_gpt3","voted_2016_gpt3"
  ```
  `V160001_orig` est l'identifiant de cas réel de l'ANES (les colonnes `V16xxxx` sont les codes de
  variables officiels de l'ANES) ; chaque variable réelle a sa colonne jumelle `_gpt3` sur la
  **même ligne, même personne**. Ligne 1 : `V160001_orig = 300001`, réponses réelles ANES en
  colonnes 3-14, réponses GPT-3 en colonnes 15-27. C'est exactement le format d'appariement décrit
  comme décisif dans la consigne — un identifiant commun, correspondance ligne à ligne.
  Le `Master_ReadMe.txt` du dépôt confirme en prose : « Individual-level data from a subset of
  questions in the ANES...and the GPT-3 produced value for each of the corresponding questions. »
- **Effectifs** : ANES 2012 (~5 900 répondants), 2016 (~4 270), 2020 (~8 280) pour l'étude 2 ;
  sous-ensemble non chiffré précisément pour l'étude 3 dans le temps imparti (le fichier
  `anesgpt3_task3.csv` fait 300 764 octets, ~13 items par personne).
- **Réserve honnête** : je n'ai pas vérifié à la source une clause de redistribution propre à
  l'ANES pour les variables publiques utilisées (au-delà du fait général, confirmé par recherche
  web sur electionstudies.org, que les fichiers de diffusion publique de l'ANES sont libres
  d'accès et que seules les variables restreintes — géocodes, dates de naissance exactes — sont
  sous accès contrôlé ; aucune des variables présentes dans ce fichier n'en fait partie). Le jeu
  Dataverse lui-même est public et sous CC0 depuis décembre 2022 sans retrait constaté.

**Verdict : ce jeu qualifie.** C'est le troisième jeu recherché — équipe différente, générateur
différent (GPT-3 plutôt que les pipelines de Twin-2K-500 ou Park et al.), appariement individuel
confirmé par constat direct de fichier, format à choix fermé compatible avec l'attaque.

---

## 2. Trouvé mais écarté : Twin-2K-500-Mega-Study (Hugging Face)

- **URL** : https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500-Mega-Study
- **Licence** : Apache 2.0.
- **Appariement individuel** : confirmé par la fiche du jeu elle-même — colonne `PID` qui
  « matches the Twin-2K-500 dataset », 13 299 exemples sur 19 études.
- **Pourquoi il est écarté malgré l'appariement confirmé** : ce sont **les mêmes personnes** que
  Twin-2K-500 (le jeu déjà utilisé dans l'article — même PID) et **la même équipe** (Toubia/Peng,
  article associé arXiv 2509.19088, déjà cité dans `references.bib` sous `peng2026funhouse`). Ce
  n'est pas un troisième jeu indépendant : c'est une extension du premier jeu à plus de scénarios
  sur la même population, donc il ne répond pas à l'objection « vos résultats tiennent-ils
  ailleurs, sur d'autres gens, avec un autre générateur ».

---

## 3. Piste à vérifier, non confirmée aujourd'hui : Wang, Hunt, Tang & Joseph (2026),
« When Can LLM Digital Twins Reduce Human Measurement? », arXiv 2609.07987

- Le papier réutilise Twin-2K (déjà connu) **et** génère de nouvelles prédictions LLM pour les
  données de Moore-Berg, Karlinsky, Hameiri & Bruneau (2020, *PNAS*, méta-perceptions partisanes,
  échantillon représentatif N=1 056 ; matériel original sur OSF `4tgpb` /
  `osf.io/preprints/psyarxiv/d6bpe/`). Le texte de l'article confirme un appariement individuel
  dans sa notation même : « a separate validation sample contain[ing] n units with both human
  outcomes Y₁,…,Yₙ and corresponding predictions Ŷ₁,…,Ŷₙ. »
- Si ce jeu apparié (humains Moore-Berg + prédictions LLM de Wang et al.) est publié
  quelque part, ce serait un vrai troisième candidat : données humaines d'une équipe (Moore-Berg),
  générateur d'une autre équipe (Wang/Hunt/Tang/Joseph, University at Buffalo) — ni la nôtre ni
  celle des deux jeux déjà utilisés.
- **Ce qui bloque** : aucune déclaration de disponibilité des données ni lien de dépôt
  (GitHub/OSF/Zenodo) trouvé dans le texte HTML accessible de l'article (l'Annexe C,
  « Reproducibility and Documentation », et l'Annexe D, « GenAI Use Documentation », existent dans
  la table des matières mais leur contenu n'était pas dans la version HTML tronquée consultée).
  **[NON VÉRIFIÉ]** — à trancher en ouvrant le PDF complet (arxiv.org/pdf/2609.07987), section
  Annexe C, ou en cherchant un dépôt sous le nom des auteurs (Steven Wang / Kenneth Joseph,
  University at Buffalo) sur GitHub/OSF.

## 4. Piste à vérifier, plus faible : Choi, Kim, Pugalenthi, Chen & Huang (2026),
« Beyond the Mean: Three-Axis Fidelity... », arXiv 2606.28963

- Utilise l'enquête de Lee et al. (2023) sur les croyances de désinformation Covid-19 (Corée du
  Sud, mai 2020, N=1 466) et évalue explicitement une « individual fidelity » — ce qui suppose des
  paires individuelles humain/LLM en interne. Aucune déclaration de disponibilité des données ni
  lien de dépôt trouvé dans le texte HTML consulté. **[NON VÉRIFIÉ]**, priorité plus basse que
  Wang et al. faute d'indice de dépôt public.

## 5. Écarté sans creuser davantage

- **Chen, Zhu & Zheng (2026)**, « When Synthetic Users Fail » (arXiv 2607.26348) : compare des
  LLM au GSS et au World Values Survey sous « demographic prompting » — nature distributionnelle
  (comparaison de distributions par sous-groupe), pas d'indice d'appariement individu-à-individu
  dans le résumé ; non creusé davantage faute de temps, cohérent avec le format « prompting
  démographique » qui n'implique pas nécessairement un identifiant individuel.
- **NIST** (Differential Privacy Synthetic Data Challenge et succession) : jeux SFFD/PUMS,
  aucune sortie de LLM, hors sujet.
- **Bonagiri et al. (2026)**, « Cognitive Digital Twins: Ethical Risks and Governance » : papier de
  gouvernance/éthique, pas de jeu de données associé.

---

## Verdict global

Il existe bien un troisième jeu réel exploitable, vérifié à la source aujourd'hui : **la
réplication d'Argyle et al. (2023), Dataverse `10.7910/DVN/JPV20K`**, avec appariement individuel
confirmé par lecture directe du fichier (`V160001_orig` + colonnes `_gpt3` sur la même ligne),
licence CC0, format à choix fermé. Twin-2K-500-Mega-Study est un vrai jeu apparié mais n'est pas
indépendant (même équipe, mêmes personnes que le jeu 1 déjà utilisé). Une piste concrète et non
encore fermée reste ouverte — les prédictions de Wang et al. (2026) sur les données Moore-Berg —
mais sa disponibilité publique n'est pas confirmée aujourd'hui.
