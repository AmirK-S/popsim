# C7 — pilote de régénération : résultats

statut: courant
mandat: Pilote de regeneration payante : mesurer l'ecart entre deux executions du bras de titre
agent: agent/mesures/pilote-regeneration
ecriture: analyses/c7_pilote_regeneration.py, resultats/c7-pilote-regeneration-*
lecture_seule: tout le reste
interdits: article/manuscrit.md (autre agent), bras complet 2058, commit sur master, fusion
cecite: je n'ai pas lu l'invite reellement employee par l'equipe amont : elle n'est publiee nulle part, et c'est precisement ce qui arrete ce mandat a l'etape 1
cout_reel_usd: 0.4934480000

**Arrêt à l'étape 1.** La configuration du bras de titre `JSON Persona - GPT4.1` **n'est pas
reconstituable avec certitude**, ni depuis le dépôt, ni depuis les sources publiques amont. Le
mandat prévoit explicitement cet arrêt et en fait le livrable. Les étapes 2 et 3 n'ont donc pas eu
lieu : **aucune exécution sur 150 personnes, aucune seconde exécution, aucun écart mesuré.**

L'étape 0 a néanmoins été conduite jusqu'au bout, parce que son produit — le coût réel par personne
— ne dépend pas du libellé de l'invite mais de la taille d'entrée, du tarif et du nombre d'appels,
tous trois établis indépendamment. **Coût total effectivement dépensé : 0,4934480000 USD**, sur un
plafond de mandat de 60,00 USD.

---

## 1. Étape 0 — chiffrer avant de dépenser

### 1.1 Ce qui a été projeté avant le premier appel

Projection écrite dans le journal **avant** la première requête, à partir de la taille d'entrée
réellement mesurée sur disque et du tarif relevé en direct par `GET /models` :

| grandeur | valeur projetée |
|---|---|
| caractères d'entrée par personne | 162 182 |
| dont persona JSON (`wave1_3_persona_json`) | 121 390 environ |
| dont questions de vague 4, réponses retirées | 39 594 |
| jetons d'entrée estimés (4 caractères par jeton, approximation déclarée) | 40 545,5 |
| appels par personne | **1** |
| prix d'entrée, `openai/gpt-4.1` | 2,00 USD par million de jetons |
| prix de sortie, `openai/gpt-4.1` | 8,00 USD par million de jetons |
| **coût projeté par personne** | **0,113091 USD** |

Le nombre d'appels par personne n'est pas une supposition : le pipeline amont
(`run_LLM_simulations.py`) lit **un fichier `pid_<n>_prompt.txt` par personne** et émet **un seul
appel**, la persona et la totalité du questionnaire de vague 4 dans la même requête. L'article amont
le confirme (« un seul appel par jumeau et par enquête »).

### 1.2 Ce qui a été constaté, sur cinq personnes réellement appelées

Cinq appels, zéro échec, zéro reprise. Coût de référence : **`usage.cost` annoncé par OpenRouter**,
jamais une estimation.

| grandeur | valeur constatée |
|---|---|
| personnes appelées | 5 |
| jetons d'entrée, moyenne | **44 348,0** (min 44 168, max 44 540) |
| jetons de sortie, moyenne | 1 249,2 |
| **coût constaté par personne** | **0,0986896000 USD** (min 0,0974560000, max 0,1017480000) |
| coût constaté total | **0,4934480000 USD** |

**Projeté 0,113091 USD par personne, constaté 0,0986896000 USD** : la projection était **haute de
14,6 %**. L'écart vient de la sortie, que j'avais provisionnée à 4 000 jetons et qui en a coûté
1 249 — le modèle répond par un objet JSON compact `QuestionID → réponse`. L'entrée, elle, avait été
sous-estimée (40 545 jetons projetés contre 44 348 constatés, l'approximation « 4 caractères par
jeton » ne tenant pas sur du JSON dense). Les deux erreurs vont en sens contraire et se compensent
partiellement. **Aucun chiffre n'est arrondi ici dans le sens qui nous arrange : la projection était
trop chère, pas trop bon marché.**

### 1.3 Les trois chiffres demandés

| périmètre | coût |
|---|---|
| **5 personnes (constaté)** | **0,4934480000 USD** |
| **150 personnes (extrapolé)** | **14,8034400000 USD** |
| **2 058 personnes, un bras complet, un seul réplicat (extrapolé)** | **203,1031968000 USD** |

Les extrapolations sont linéaires en nombre de personnes, ce qui est justifié ici : la dispersion du
coût par personne est faible (étendue de 0,0975 à 0,1017 USD sur cinq personnes, soit ±2,2 % autour
de la moyenne), parce que le coût est dominé par une entrée de taille presque constante. Elles ne
provisionnent **ni les reprises** (le pipeline amont rejoue jusqu'à 10 fois un appel dont la sortie
échoue à la validation), **ni les échecs**. Un bras complet réel coûterait donc **plus** que
203 USD, pas moins.

### 1.4 Réconciliation du coût — les deux méthodes tombent exactement d'accord

Ce projet a déjà vu une dépense annoncée à 0,32 USD puis 0,55 USD alors que la nuit avait coûté
10,51 USD. Le coût est donc établi ici par deux voies indépendantes :

| méthode | valeur |
|---|---|
| grand livre, somme des `usage.cost` appel par appel | **0,4934480000 USD** |
| compteur `GET /credits`, `total_usage` avant → après | 161,027271878 − 160,533823878 = **0,4934480000 USD** |
| **écart** | **0,0000000000 USD** |

**Piège signalé** : la lecture du compteur faite immédiatement après le dernier appel ne donnait que
0,2938280000 USD, soit exactement le cumul des **trois premiers** appels. Les deux derniers n'étaient
pas encore réglés côté OpenRouter (latence de règlement déjà documentée dans ce dépôt). Une lecture
faite à cet instant-là et publiée telle quelle aurait **sous-déclaré la dépense de 40,5 %**. Le
chiffre publié ci-dessus est celui d'une relecture postérieure au règlement.

---

## 2. Étape 1 — la configuration du bras de titre n'est pas reconstituable

C'est le résultat principal de ce mandat.

### 2.1 Le bras de titre n'a jamais été produit par ce dépôt

`JSON Persona - GPT4.1` est un jeu de jumeaux **téléchargé tel quel** depuis le dépôt HuggingFace
`LLM-Digital-Twin/Twin-2K-500` (`analyses/a8_telecharger_twin_llm.py`, l. 33-47 :
`"JSON Persona - GPT4.1": "spec_json_gpt41.csv"`). Le fichier local
`data/twin2k500/llm_specs/json_persona__gpt41.csv` ne contient que des **réponses formatées**.

L'audit de provenance l'avait déjà écrit, et cette relecture le confirme sans le nuancer
(`twin-ab-audit-provenance-2026-09-11.md`) : « **Aucune invite n'a été lue.** […] Tout le classement
"admissible" repose sur des noms de configuration, sur le README et sur l'examen de l'objet de
contexte, pas sur l'entrée réellement envoyée. »

### 2.2 Ce que les sources publiques amont donnent — et ce qu'elles ne donnent pas

Contrairement à l'audit de septembre, qui n'avait pas pu accéder au réseau, le dépôt amont
`tianyipeng-lab/Digital-Twin-Simulation` a été consulté ici. Ce qu'il publie :

| élément | ce qui est publié | est-ce celui du bras de titre ? |
|---|---|---|
| fichiers de configuration | **un seul**, `text_simulation/configs/openai_config.yaml` | **non** |
| modèle | `gpt-4.1-mini-2025-04-14` | **non** — le bras de titre est GPT-4.1, pas mini |
| format de persona | pipeline persona → **TEXTE** (`convert_persona_to_text.py`) | **non** — le bras de titre est JSON |
| température | **0,0** dans le fichier de configuration | **contredit l'article**, qui donne 0,7 par défaut |
| message système | publié, verbatim | **indéterminé** pour ce bras |
| appels par personne | 1, avec jusqu'à 10 reprises sur échec de validation | vraisemblable |
| post-traitement | `postprocess_responses.py`, publié | vraisemblable |

Le dépôt amont publie **13 jeux de sorties** (23 selon le décompte du README) et **une seule
configuration**. Celle-ci reproduit le bras par défaut (`default_gpt41mini`), pas le bras de titre.
**Aucune source, locale ou amont, ne fait correspondre l'étiquette `JSON Persona - GPT4.1` à un
jeu de paramètres précis.**

### 2.3 Pourquoi cette lacune est fatale à ce mandat en particulier

Le paramètre manquant n'est pas anodin : **c'est la température.** Le fichier de configuration amont
dit 0,0 ; l'article amont dit 0,7 par défaut. Or la grandeur que ce mandat cherche — l'écart entre
deux exécutions de la même configuration — **est gouvernée par ce paramètre et par presque rien
d'autre** :

- à température 0, deux exécutions sont nominalement identiques, et l'écart mesuré ne serait que du
  bruit de fournisseur ;
- à température 0,7, deux exécutions diffèrent réellement, et l'écart mesuré serait la grandeur
  recherchée.

Mesurer l'écart sans connaître la température ne produit donc pas un intervalle sur le procédé : cela
produit un intervalle sur **un procédé de mon invention**, qu'on serait ensuite tenté de lire comme
s'il portait sur le leur. C'est précisément le sinistre que la règle d'arrêt du mandat prévient.

### 2.4 Ce que cela explique de la famille B

Les sept bras régénérés localement (`analyses/c7_gen.py`) ont tous échoué le contrôle
d'interprétabilité — 0,0 à 0,8 % de ré-identification contre un hasard de 0,83 % et une baseline
démographique de 9,20 % sur le même bassin. Cet échec s'éclaire : la famille B n'a jamais tenté de
reproduire le pipeline amont, et **ne le pouvait pas**. Elle employait ses propres invites
(`CONSIGNE`, l. 216-224), trois modèles ouverts distincts, une persona **tronquée à 8 000
caractères**, et une sortie en texte brut `N) k` au lieu de JSON — là où le pipeline amont envoie
**44 348 jetons**, soit l'intégralité de la persona, en un seul appel.

L'écart n'est pas un détail de formulation : c'est un rapport de plus de quinze en quantité
d'information transmise. **La famille B n'était pas une régénération manquée du bras de titre ; c'en
était une autre expérience.** Son échec ne dit rien sur la reproductibilité du bras de titre — et
cette relecture retire donc à cet échec la portée qu'on aurait pu lui prêter.

### 2.5 Statut de la reconstruction employée à l'étape 0

Le script `analyses/c7_pilote_regeneration.py` porte une reconstruction approchée, déclarée comme
telle **dans le code lui-même** : `ConfigBras(..., reconstitue=False, motif_non_reconstitue=...)`, et
le script imprime cet avertissement à chaque exécution. Elle a servi à **chiffrer**, pas à
reproduire. Les cinq sorties produites ne sont versées à aucune analyse de ré-identification et ne
doivent jamais être comparées aux sept bras admissibles.

---

## 3. Étapes 2 et 3 — non conduites

- **Étape 2 (contrôle d'interprétabilité sur 150 personnes)** : non conduite. Elle aurait coûté
  14,80 USD, largement sous le plafond. Elle n'a pas été lancée parce que le contrôle aurait porté
  sur un pipeline dont on sait déjà qu'il n'est pas celui du bras de titre : qu'il passe ou qu'il
  échoue, le résultat n'aurait pas été interprétable comme un énoncé sur le bras publié.
- **Étape 3 (seconde exécution, écart entre les deux)** : non conduite, puisque l'étape 2 ne l'a pas
  autorisée. **L'écart entre deux exécutions du bras de titre reste non mesuré, et ce mandat établit
  qu'il n'est pas mesurable pour ce bras.**

La prédiction préenregistrée (écart d'au moins 2 points, plus probablement 3 à 6) et le seuil
préenregistré (3,4673 points, au-delà duquel les intervalles publiés seraient déclarés inutilisables
comme énoncés sur le procédé) **restent non testés**. Ils ne sont pas retirés : ils sont en attente.

---

## 4. Recommandation chiffrée sur un bras complet

### 4.1 Ce que coûterait un bras complet

| scénario | coût |
|---|---|
| un bras complet, 2 058 personnes, un réplicat | **203,10 USD** |
| deux réplicats (le minimum pour un écart) | **406,21 USD** |
| cinq réplicats (un intervalle à cinq points) | **1 015,52 USD** |
| dix réplicats | **2 031,03 USD** |

Hors reprises et hors échecs, donc plancher, pas devis.

### 4.2 Combien de réplicats pour un intervalle utile

Deux exécutions ne donnent pas un intervalle : elles donnent un écart, c'est-à-dire un minorant de
dispersion à deux points, sans degré de liberté pour en estimer la largeur. Pour publier un
intervalle sur le procédé qui soutienne la comparaison avec l'intervalle sur les personnes
(3,4673 points de large), il faut au minimum **cinq réplicats** — et raisonnablement **dix**, si l'on
veut que la borne haute ne dépende pas d'un tirage. À 2 058 personnes, cela place la facture entre
**1 015 et 2 031 USD**, soit 17 à 34 fois le plafond de ce mandat.

### 4.3 Ce que je recommande, et ce que je ne recommande pas

**Je ne recommande pas de payer un bras complet**, ni maintenant ni après validation, **pour le bras
de titre** — quel que soit le budget. La dépense n'achèterait pas la grandeur cherchée : elle
achèterait la variabilité d'un pipeline reconstruit, qu'aucune source ne permet d'aligner sur celui
qui a produit les 20,6803 % publiés. Un intervalle obtenu ainsi serait plus trompeur que l'absence
d'intervalle, parce qu'il porterait un air de mesure.

**Trois voies restent ouvertes, par ordre de coût croissant :**

1. **Gratuite — écrire ce que le chiffre est.** Le titre à 20,6803 % est un **tirage unique**, c'est
   le **maximum de huit bras**, et son intervalle publié est un bootstrap **sur les personnes** qui
   ne dit rien de la variabilité du procédé. Ces trois faits sont établis et tiennent sans dépense.
   C'est le minimum avant tout dépôt.
2. **Gratuite — demander l'invite aux auteurs amont.** Le seul obstacle à ce mandat est un fichier
   de configuration que l'équipe Twin possède et n'a pas publié. Une demande par courrier, ou une
   question sur leur dépôt, coûte zéro dollar et débloquerait tout le reste. **C'est de loin le
   meilleur rapport entre ce qu'on dépense et ce qu'on apprend.**
3. **Environ 30 USD, et seulement après (2)** — le pilote prévu ici, deux exécutions sur 150
   personnes (14,80 USD chacune), une fois la configuration établie et le contrôle
   d'interprétabilité passé. Ce mandat a produit tout l'outillage nécessaire ; il ne manque que
   l'invite.

---

## 5. Dépense — déclaration finale

| poste | montant |
|---|---|
| étape 0, cinq appels `openai/gpt-4.1` | **0,4934480000 USD** |
| étapes 1, 2, 3 | 0,00 USD (aucun appel) |
| lectures `GET /credits` et `GET /models` | 0,00 USD (gratuites) |
| **total effectivement dépensé** | **0,4934480000 USD** |
| plafond du mandat | 60,00 USD |
| part du plafond consommée | 0,82 % |

Chiffre établi par deux méthodes indépendantes qui tombent d'accord à **0,0000000000 USD près**
(§1.4). Aucun bras complet n'a été lancé. Le pilote ne s'est pas approché des 150 personnes.

## 6. Ce que je n'ai pas fait, et qui reste ouvert

- Je n'ai **pas** écrit dans `article/manuscrit.md`, qui appartient à un autre agent. Le §4.3 (1)
  appelle pourtant une correction du manuscrit : elle doit être portée par son propriétaire.
- Je n'ai **pas** vérifié que les 44 348 jetons d'entrée de ma reconstruction correspondent à ce que
  l'équipe amont envoyait réellement. C'est invérifiable sans leur invite, et c'est le nœud du §2.
- Je n'ai **pas** mesuré la ré-identification des cinq sorties produites : cinq personnes ne
  permettent aucun contrôle d'interprétabilité, et les produire pour les regarder quand même aurait
  été du dragage.
- La branche n'est **pas** fusionnée, conformément au mandat.
