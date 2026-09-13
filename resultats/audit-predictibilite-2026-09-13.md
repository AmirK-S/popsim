# C7, audit : « la fuite suit la prédictibilité, non la rareté » — est-ce une découverte ou une tautologie ? (13 septembre 2026)

statut: courant
mandat: Attaquer l'affirmation établie sur `agent/mesures/equite-risque` selon laquelle le risque individuel de ré-identification décroît avec l'atypicité (ρ = −0,181) et croît avec la cohérence test-retest (+0,256). Déterminer si ce résultat survit (a) au contrôle du bruit de mesure, (b) à une autre définition de la rareté, (c) à l'analyse partielle rareté × stabilité, (d) au contrôle du nombre d'items, (e) au changement d'attaquant pour A-LLR pondéré par la rareté. Aucun appel payant, aucun réseau, aucun arrière-plan, aucune donnée individuelle imprimée.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_audit_predictibilite.py, resultats/audit-predictibilite-2026-09-13.md, resultats/c7-audit-predictibilite.csv
lecture_seule: tout le reste du dépôt, notamment analyses/c7_reidentification.py, analyses/c7_attaquant_fort.py, analyses/c7_equite_risque.py (branche `agent/mesures/equite-risque`)
interdits: appel payant, réseau, recherche web, arrière-plan, fusion sur master, écriture dans article/manuscrit.md, impression de tout identifiant / réponse / combinaison individuelle
cout_reel_usd: 0.00

## 0. Préenregistrement — écrit et commité AVANT le premier calcul

### 0.1 Ce que je cherche à détruire

> ρ(risque, atypicité) = −0,181 [−0,225 ; −0,135] ; ρ(risque, cohérence test-retest) = +0,256 [+0,213 ; +0,293]. « La fuite suit la prédictibilité, pas la rareté. »

### 0.2 L'explication plate, et pourquoi elle est probablement la bonne

Le jumeau Twin-2K-500 est **construit à partir de la persona des vagues 1-3** (`data/twin2k500/README.md`, champs `wave1_3_persona_text` / `wave1_3_persona_json`) et l'attaque l'apparie contre les réponses **vague 4**. La « cohérence interne test-retest » est, par définition, l'accord entre v1-3 et v4 : c'est-à-dire **l'accord entre la source d'information de l'attaquant et sa cible**. Dire « les cohérents sont plus exposés » reviendrait alors à dire « on retrouve mieux quelqu'un quand les informations dont on dispose sur lui sont encore exactes » — un énoncé sur la **qualité de la donnée auxiliaire**, tautologique, sans rapport avec le jumeau LLM ni avec la vie privée.

### 0.3 Prédictions, fixées avant calcul

- **P1 (tautologie du témoin trivial).** Un attaquant **trivial** qui utilise, comme « jumeau », les **réponses v1-3 de la personne elle-même** — aucun modèle de langage — produira une corrélation risque ~ cohérence **au moins aussi forte** que celle du jumeau LLM : ρ_trivial ≥ +0,60. *Prédiction : vraie.*
- **P2 (médiation).** La corrélation partielle ρ(risque_LLM, cohérence | risque_trivial) **tombera sous +0,10 en valeur absolue**, c'est-à-dire que l'effet « cohérence » du jumeau LLM est entièrement porté par la qualité de la donnée auxiliaire. *Prédiction : vraie.*
- **P3 (rareté et stabilité confondues).** ρ(atypicité, cohérence) sera **négative et non nulle** (|ρ| ≥ 0,15) : les réponses rares sont aussi les moins stables. En conséquence, la corrélation **partielle** ρ(risque, atypicité | cohérence) sera **d'au moins 40 % plus faible** en valeur absolue que la corrélation brute −0,181. *Prédiction : vraie.*
- **P4 (définition de la rareté).** Le signe négatif **survivra** à un changement de définition de la rareté (rareté moyenne `−log q_j(x_ij)` sous les marginales de population hors pli ; et log-vraisemblance hors pli sous un modèle de classes latentes ajusté sur les **autres** personnes). *Prédiction : vraie — le signe est robuste à la définition, ce n'est pas là que l'affirmation casse.*
- **P5 (prédictibilité sans retest).** Une mesure de prédictibilité **n'utilisant pas le retest** — log-vraisemblance hors pli sous le modèle de classes latentes — corrélera **positivement** au risque, ρ ≥ +0,10. *Prédiction : vraie.* Mais je préenregistre aussi le point conceptuel : sous un modèle de population, « prédictible » et « typique » sont **la même variable**, donc P5 vraie ne sépare pas prédictibilité et rareté — elle montre qu'elles coïncident, et donc que l'opposition « prédictibilité *contre* rareté » est mal posée.
- **P6 (attaquant, le test décisif).** Sous **A-LLR pondéré par la rareté** (`c7_attaquant_fort.scores_hors_pli`, hors pli, bassin strictement identique), le signe de ρ(risque, atypicité) **s'inversera ou deviendra non significatif** : ρ_A-LLR ≥ −0,05. *Prédiction : vraie.* A-LLR est construit pour récompenser l'accord sur les modalités rares ; si le signe dépend de l'attaquant, le résultat n'est pas une propriété des données.
- **P7 (nombre d'items).** Le contrôle du nombre de réponses non manquantes (108 items) ne changera **pas** les conclusions (|Δρ| < 0,03) : sur les 60 items retenus, tout le monde est renseigné par construction. *Prédiction : vraie, c'est un confondant nul ici.*

### 0.4 Critère de réfutation de mon propre audit

**Mon audit est réfuté, et l'affirmation de l'agent tient**, si **toutes** les conditions suivantes sont réunies :
1. la corrélation partielle ρ(risque_LLM, cohérence | risque_trivial) **reste ≥ +0,15** (l'effet n'est pas médié par la qualité de la donnée auxiliaire) ; **et**
2. la corrélation partielle ρ(risque, atypicité | cohérence, prédictibilité hors retest) **reste ≤ −0,10** (la rareté protège au-delà de la stabilité) ; **et**
3. le signe reste **négatif et significatif sous A-LLR** (ρ_A-LLR ≤ −0,10).

Si (3) échoue seul, le résultat est **dépendant de l'attaquant** : l'article doit le dire ainsi, pas le présenter comme une propriété des données. Si (1) échoue, le corrélat « cohérence » est **tautologique** et doit sortir de la phrase.

### 0.5 Garde-fous

Bassin **strictement constant** entre toutes les conditions : les 2 058 humains vague 4, les mêmes 60 items toujours renseignés, les mêmes personnes attaquées (celles couvertes par `JSON Persona - GPT4.1`), risque `p_i(B = 100)` par la transformation déterministe du rang de `c7_equite_risque.risque_a_bassin_constant`. Graine fixée 20260913. Aucune donnée individuelle imprimée, aucun groupe de moins de 20 personnes. Le modèle de classes latentes et les marginales de rareté sont estimés **hors pli** (5 plis), jamais sur la personne évaluée.

<!-- FIN DU PREENREGISTREMENT — tout ce qui suit a été écrit après les calculs -->
