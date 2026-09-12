# C7 — « loi de distance » : préenregistrement

Écrit le 12 septembre 2026, **avant** `analyses/c7_loi_distance.py` et **avant tout calcul
de paire**. Aucun appel d'API, aucune dépense, aucune recherche web, aucune génération de
jumeau. Lecture seule sur `data/`.

Sorties autorisées : `analyses/c7_loi_distance.py`, ce fichier,
`resultats/c7-loi-distance-resultats.md`, `resultats/c7-loi-distance.csv`.

---

## 0. L'hypothèse mise à l'épreuve

Observation de la nuit (`resultats/c7-reconciliation-facteurs-2026-09-12.md`, §2) : entre
deux jumeaux publiés d'une même personne, à bassin et items identiques, le taux de liaison
décroît par paliers selon **ce qui change** dans le pipeline — décodage 93,3 %, gabarit
87,1 %, raisonnement 53,5 %, format de persona 48,7 %, modèle 45,9 %, contre 13,3 % pour un
adversaire purement démographique.

**H — hypothèse de distance de pipeline.** Le taux de liaison entre deux sorties
synthétiques de la même personne est une fonction **décroissante d'une distance entre les
deux pipelines**, et non une propriété de la personne. Corollaire testable : plus deux
pipelines diffèrent sur des dimensions **observables et déclarées à l'avance**, plus le
taux de liaison est bas — et cela dans deux jeux produits par deux équipes indépendantes.

**H₀ — ce qui la remplace.** Le taux de liaison ne dépend pas de la distance entre
pipelines mais seulement de la **fidélité individuelle** des deux jumeaux comparés : deux
jumeaux qui portent bien la personne se lient bien, quel que soit l'écart de pipeline.
C'est l'alternative la plus sérieuse et elle est explicitement testée (§6).

---

## 1. La distance, définie avant tout calcul

**Définition.** Pour deux pipelines P et Q,

> **d(P, Q) = nombre de descripteurs de pipeline sur lesquels P et Q diffèrent**,

sur une liste de descripteurs **fixée ici**, chacun binaire, tous lisibles dans la
documentation publiée par l'équipe d'origine (nom de configuration, README du jeu, guide de
réplication) — **jamais dans une sortie de jumeau, jamais dans un taux de liaison.**

Liste des neuf descripteurs, valable pour les deux jeux :

| # | descripteur | valeurs |
|---|---|---|
| 1 | modèle (backbone) | identité exacte du modèle |
| 2 | gabarit d'invite | standard / variante déclarée |
| 3 | décodage | température nulle / température par défaut |
| 4 | raisonnement explicite | absent / présent |
| 5 | format de rendu de la persona | texte narratif / JSON / champs listés |
| 6 | bloc « démographie » présent dans le contexte | 0 / 1 |
| 7 | bloc « dossier d'enquête » présent | 0 / 1 |
| 8 | bloc « entretien » présent | 0 / 1 |
| 9 | bloc « auto-description (persona courte) » présent | 0 / 1 |

d est donc une **distance de Hamming sur des descripteurs de pipeline**, entière, à valeurs
dans 0–9. Elle est **ordinale et volontairement non pondérée** : chaque descripteur compte
un. Tout descripteur constant dans un jeu y contribue 0 partout et ne peut donc pas créer
artificiellement de gradient.

**Pourquoi elle n'est pas circulaire.** Elle ne lit aucune sortie de jumeau, aucun accord,
aucun taux de liaison, aucune fidélité. Elle est entièrement déterminée par les
métadonnées publiées avant que la moindre attaque soit lancée. Le tableau des descripteurs
par configuration (§3) est figé dans ce document ; il ne sera pas révisé après les mesures.

**Ses faiblesses, déclarées maintenant.**
- **Poids égaux arbitraires.** Passer de T = 0 à la température par défaut compte autant
  que perdre les 494 items du dossier d'enquête. C'est presque certainement faux. La
  prédiction §5 est formulée en connaissance de cela ; §7 dit ce que je conclurai si c'est
  la source principale d'échec.
- **Réserve R1 de `twin-ab-audit-provenance-2026-09-11.md`** : sur Twin, **aucune invite
  n'est observable localement**. Les descripteurs 1–5 sont lus dans le **nom publié** de la
  configuration, pas dans le prompt réel. Si deux configurations diffèrent en plus sur un
  descripteur non annoncé par leur nom, d est sous-estimée.
- **Additivité supposée.** d suppose que les effets s'ajoutent. Rien ne le garantit.

---

## 2. Configurations retenues, et pourquoi les autres sont écartées

### Twin-2K-500 (équipe Twin, 2 058 personnes)
Treize configurations publiées. Écartées **avant tout calcul**, motifs déjà établis :
- `JSON Persona (Predicted Output)` ×2, `LLM Finetuning (500)`, `Persona Summary` ×2 :
  non admissibles ou suspectes (`twin-ab-audit-provenance-2026-09-11.md`, §2.4).
- `JSON Persona - GPT4.1-mini` : **écartée ici pour une raison propre à cette mission** —
  elle ne partage que **19 items** avec les autres et 1 000 personnes sur 2 058. Or le taux
  dépend mécaniquement du nombre d'items (`c7-transfert-resultats.md` : 36,4 % à 60 items
  contre 0,45 % à 19 items). La garder imposerait 19 items à **toutes** les paires.
  **Bassin et items doivent rester constants entre paires**, c'est la condition de la
  mission ; cette configuration est donc incompatible avec le plan.

**Restent 7 configurations**, toutes à 2 058 personnes et 60 items communs :
Demographics Only - GPT4.1-mini ; JSON Persona - GPT4.1 ; Text Persona - GPT4.1-mini ;
Text Persona (Default Temperature) - GPT4.1-mini ; Text Persona (Reasoning) - GPT4.1-mini ;
Text Persona (Repeating Questions) - GPT4.1-mini ; Text Persona - Gemini-Flash2.5.
→ **21 paires non ordonnées.**

### Park et al. (OSF `t6g7k`, 1 052 personnes)
Trois domaines. **Seul le bloc GSS est retenu** : 177 items catégoriels, même instrument de
mesure que Twin (Hamming). Les deux autres domaines n'ont que **5 items** chacun (jeux
économiques, Big Five) — trop peu pour une ré-identification interprétable, et ils
imposeraient une distance euclidienne, donc un instrument différent. Écartés avant calcul.

Six conditions dans le bloc GSS. `v8` est **exploratoire et non documentée** dans
`FIGURE2_PIPELINE.md` : ses descripteurs ne sont pas assignables sans deviner, elle est
donc écartée (écarter pour cause de documentation absente, pas pour cause de résultat).

**Restent 5 conditions** : persona (auto-description), démographique, enquête, entretien,
composite (enquête + entretien). → **10 paires non ordonnées.**

**Total avant contrôle : 31 paires. C'est peu, et c'est dit franchement.** Les 21 paires
Twin ne sont pas 21 pipelines indépendants : elles viennent de 7 configurations d'un même
atelier, partageant les mêmes fichiers de persona et le même harnais. Les 10 paires Park
viennent de 5 conditions d'un même atelier. L'unité réellement indépendante est la
**configuration** (7 + 5 = 12), pas la paire.

---

## 3. Tableau des descripteurs — figé avant mesure

Descripteurs constants et donc sans effet : sur Twin, blocs entretien et auto-description
absents partout ; sur Park, modèle, gabarit, décodage, raisonnement et format de rendu
identiques partout (une seule équipe, un seul harnais, une seule famille de prompts).

### Twin (descripteurs 1–7 ; 8 et 9 valent 0 partout)

| configuration | modèle | gabarit | décodage | raisonn. | format | démo | enquête |
|---|---|---|---|---|---|---|---|
| Demographics Only - GPT4.1-mini | gpt41-mini | standard | T0 | non | champs listés | 1 | 0 |
| JSON Persona - GPT4.1 | gpt41 | standard | T0 | non | JSON | 1 | 1 |
| Text Persona - GPT4.1-mini | gpt41-mini | standard | T0 | non | texte | 1 | 1 |
| Text Persona (Default Temperature) - GPT4.1-mini | gpt41-mini | standard | **défaut** | non | texte | 1 | 1 |
| Text Persona (Reasoning) - GPT4.1-mini | gpt41-mini | standard | T0 | **oui** | texte | 1 | 1 |
| Text Persona (Repeating Questions) - GPT4.1-mini | gpt41-mini | **répétition** | T0 | non | texte | 1 | 1 |
| Text Persona - Gemini-Flash2.5 | **gemini-flash2.5** | standard | T0 | non | texte | 1 | 1 |

### Park, bloc GSS (descripteurs 6–9 ; 1–5 constants)

| condition | démo | enquête | entretien | auto-description |
|---|---|---|---|---|
| démographique (`gss_v6`) | 1 | 0 | 0 | 0 |
| persona (`gss_v7`, *ablation self-desc*) | 0 | 0 | 0 | 1 |
| enquête (`survey_agents`) | 0 | 1 | 0 | 0 |
| entretien (`gss_v3`) | 0 | 0 | 1 | 0 |
| composite (`composite_agents`) | 0 | 1 | 1 | 0 |

---

## 4. Mesure

- **Estimand** : top-1 de ré-identification jumeau ↔ jumeau, **symétrique** (moyenne des
  deux sens), sur le bassin complet du jeu.
- **Fonctions** : `analyses/c7_reidentification.rangs_attaque` (donc
  `a2_commun.distance_hamming`) pour Twin ; `analyses/c7_stanford.rangs_depuis_accord` +
  `accord_categoriel` pour Park. **Aucune réimplémentation.**
- **Bassin et items constants** : Twin, bassin = 2 058, items = les colonnes renseignées à
  100 % chez **toutes** les configurations retenues et chez les humains (attendu : 60) ;
  Park, bassin = 1 052, items = colonnes renseignées à 100 % chez **toutes** les conditions
  retenues et chez la vague 1. Le même jeu d'items sert à **toutes** les paires du jeu.
- **Intervalles** : bootstrap sur les **personnes**, 2 000 tirages, graine 20260912. Les
  mêmes personnes sont retirées simultanément pour toutes les paires d'un jeu, afin que
  l'incertitude de ρ tienne compte de la corrélation entre paires.

---

## 5. Forme attendue, règle de décision, prédictions par jeu

**Forme attendue** : top-1 décroissant de façon monotone avec d. Estimand principal :
**ρ de Spearman entre d et le top-1**, calculé **séparément sur chaque jeu**.

**Règle de décision, par jeu :**
- **soutenue** si ρ ≤ −0,50 **et** l'IC bootstrap à 95 % de ρ exclut 0 ;
- **réfutée (plate)** si ρ > −0,20 ;
- **indécise** entre les deux, ou si l'IC contient 0.

**Réplication** : les deux jeux sont *soutenus*, avec le même signe.

**Prédictions chiffrées, écrites avant mesure :**
- **Twin** (15 paires après contrôle, d ∈ {1, 2, 3}) : ρ ≈ **−0,7**, IC excluant 0.
- **Park** (6 paires après contrôle, d ∈ {1, 2, 3}) : ρ ≈ **−0,6**, mais **je prédis
  explicitement que l'IC pourra contenir 0** : avec 6 paires et des ex æquo sur d, la
  puissance est faible. Une Park « indécise » ne réfute pas H ; une Park **positive**
  (ρ > 0) la réfute.

**Ce qui réfuterait H — écrit avant de savoir :**
1. **Courbe plate sur Twin** : ρ > −0,20 sur les 15 paires Twin. H est morte, les paliers
   de la nuit sont un artefact de l'ordre dans lequel on les a rangés.
2. **Inversion entre jeux** : ρ nettement négatif sur un jeu et nettement positif sur
   l'autre. Alors d ne mesure rien de transportable : ce serait au mieux une régularité
   locale à un atelier.
3. **Variance intra-niveau supérieure à la variance inter-niveaux** (§6, test B) : si à
   d = 1 les taux s'étalent de 40 à 95 points, la « loi » ne prédit rien d'utile même si ρ
   est négatif. Je le dirai, et le verdict sera au mieux « tendance ».
4. **Le test de fidélité (§6, test A) annule la relation** : voir ci-dessous.

---

## 6. Les trois contrôles qui décident du verdict

**Contrôle d'interprétabilité (préalable, éliminatoire).**
`analyses/c7_controle_interpretabilite.controle_avant_interpretation` est appelée sur
**chaque configuration** avec le bassin et les items réellement utilisés, **avant**
inclusion. Toute configuration qui échoue est **exclue**, et nommée dans le rapport.
- Sur Twin : appel direct de la fonction.
- Sur Park : la fonction est câblée sur Twin (`REF_V4`, `DEMO`). La **règle** est
  transposée à l'identique et réimplémentée pour Park sur les mêmes briques
  (`c7_stanford`) : IC bootstrap non chevauchants entre le top-1 du candidat contre les
  humains de vague 1 et celui de la condition `démographique` contre les mêmes humains, même
  bassin, mêmes items. Transposition déclarée ici, pas après coup.
- **Conséquence connue et acceptée** : la configuration de référence démographique de
  chaque jeu (`Demographics Only` sur Twin, `démographique` sur Park) ne peut pas se
  dépasser elle-même ; elle échoue donc mécaniquement et sort du test. Ses paires seront
  rapportées **à part**, à titre descriptif seulement.

**Test A — la fidélité explique-t-elle tout ? (décisif pour le mot « loi »)**
Pour chaque configuration, sa **fidélité individuelle** = top-1 contre les humains réels,
même bassin, mêmes items (chiffre déjà produit par le contrôle). Pour une paire,
`fid_paire` = moyenne géométrique des deux fidélités. Je calcule la **corrélation partielle
de rang** entre d et le top-1, **à fidélité contrôlée**.
- **H tient au sens fort** si ρ_partiel ≤ **−0,30** avec IC bootstrap excluant 0, sur Twin
  au moins.
- Si ρ_partiel s'effondre vers 0 alors que ρ brut est fortement négatif, **la conclusion
  préenregistrée est : ce n'est pas une distance entre pipelines, c'est la fidélité des deux
  jumeaux**, et je l'écrirai ainsi.

**Test B — dispersion intra-niveau.** Étendue et écart-type du top-1 à d fixé, par jeu.
Rapportés même si défavorables (critère 3 ci-dessus).

---

## 7. Engagements

- Le tableau des descripteurs (§3) et la liste des exclusions (§2) ne seront **pas révisés**
  après avoir vu les taux. Si une révision s'impose pour une raison factuelle, elle sera
  signalée comme **post hoc** et le résultat correspondant sera présenté comme exploratoire.
- Aucun chiffre ne sera inventé ni arrondi en faveur de H. Une courbe plate, ou une
  relation qui ne se réplique pas, sera rapportée comme résultat principal.
- Si, après mesure, la distance me paraît arbitraire — en particulier à cause des poids
  égaux — je l'écrirai explicitement dans le rapport, y compris si ρ est très négatif.
- **Divulgation d'antériorité** : une seule mesure de paire a déjà été produite, pendant le
  test de faisabilité qui a précédé ce document — `Text Persona - GPT4.1-mini` →
  `Text Persona - Gemini-Flash2.5`, un seul sens, bassin 2 058, 60 items : **15,07 %**.
  Elle est ici déclarée, et elle n'a servi qu'à chronométrer le calcul.
- Graine unique : 20260912. Aucun appel payant, aucune génération.
