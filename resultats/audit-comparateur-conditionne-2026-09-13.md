# C7, audit : le comparateur classique a-t-il été conditionné sur la même information individuelle que le jumeau LLM ? (13 septembre 2026)

statut: courant
mandat: Trancher l'objection portée contre `agent/mesures/controle-generateur`, qui conclut qu'« aucun générateur synthétique classique ne dépasse 0,15 % de ré-identification sur Twin contre 20,7 % pour les jumeaux LLM ». L'objection : les quatre générateurs classiques G0-G3 n'ont été conditionnés que sur le segment démographique, alors que le jumeau LLM est construit à partir des réponses passées de la personne elle-même. (1) Établir depuis les données de quoi chaque jumeau est réellement construit. (2) Si le conditionnement individuel est confirmé, reconstruire les générateurs classiques avec exactement la même entrée individuelle. (3) Décider laquelle des trois issues se réalise. (4) Situer le tout par rapport au plafond de 81,6 % de l'attaquant qui n'utilise que les réponses passées. Aucun appel payant, aucun réseau, aucun arrière-plan, aucune donnée individuelle imprimée.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_audit_comparateur_conditionne.py, resultats/audit-comparateur-conditionne-2026-09-13.md, resultats/c7-audit-comparateur-conditionne.csv
lecture_seule: tout le reste du dépôt, notamment analyses/c7_reidentification.py, analyses/c7_controle_interpretabilite.py, analyses/c7_controle_generateur.py (branche `agent/mesures/controle-generateur`), analyses/c7_audit_predictibilite.py (branche `agent/audit/predictibilite`)
interdits: appel payant, réseau, recherche web, arrière-plan, fusion sur master, écriture dans article/manuscrit.md, impression de tout identifiant / réponse / combinaison individuelle
cout_reel_usd: 0.00

---

## 0. Préenregistrement — écrit et commité AVANT le premier calcul de comparateur

### 0.1 Ce que j'attaque

> « Aucun générateur synthétique classique ne dépasse 0,15 % de ré-identification sur Twin
> et 2,3 % sur Park, contre 20,7 % et 65,6 % pour les jumeaux LLM ; ce que nous mesurons
> n'est pas la fuite générique des données synthétiques. »
> — `agent/mesures/controle-generateur`, `resultats/c7-controle-generateur-resultats.md`

L'objection à trancher : **G0-G3 ne voient que le segment démographique, le jumeau LLM voit
la personne**. Si c'est exact, la comparaison oppose un générateur qui a vu l'individu à des
générateurs qui ne l'ont jamais vu, et elle ne démontre rien sur les LLM.

### 0.2 Le fait, établi avant toute prédiction (section 1), donc déclaré et non prédit

Établi le 13 septembre 2026 **avant** l'écriture de cette section, directement depuis
`data/twin2k500/question_catalog_and_human_response_csv/question_catalog.json`,
`data/twin2k500/wave_persona_chunk_001.parquet` et `data/twin2k500/README.md` : le catalogue
partitionne ses **256 QuestionID** en deux sources disjointes, `wave1_3_persona_json`
(171 QuestionID, **634 colonnes CSV**) et `wave4_Q_wave1_3_A` (85 QuestionID,
**126 colonnes CSV**). Le jumeau est conditionné sur la **première** ; l'attaque porte sur
la **seconde**. Le conditionnement individuel est donc **confirmé** — et il est
**disjoint des items attaqués**. Le détail et les vérifications sont en section 1 ; ce fait
est une donnée d'entrée de ce préenregistrement, pas un de ses résultats.

### 0.3 Le comparateur équitable, fixé avant calcul

Entrée individuelle **strictement identique** à celle du jumeau : les **634 colonnes** des
vagues 1-3 hors items répétés. Bassin **strictement constant** : 2 058 attaqués,
2 058 candidats, les **60 items** de `c7_reidentification.items_communs`, attaque importée
telle quelle (`rangs_attaque`), graine fixée. Quatre générateurs :

- **K1** plus proche voisin sur la persona : le vecteur vague 4 entier du plus proche voisin (la personne elle-même exclue du don).
- **K10** vote modal par item des 10 plus proches voisins sur la persona.
- **K2a** modèle conditionnel par item ajusté sur la persona, hors pli, argmax.
- **K2s** le même, tirage dans la loi prédite (générateur véritable, pas un prédicteur).

### 0.4 Prédictions, fixées avant calcul

- **P2 (l'objection mord un peu).** Le meilleur comparateur équitable dépassera d'au moins un facteur 3 le plafond publié des générateurs conditionnés au segment : **top-1 ≥ 0,5 %** (contre 0,15 %). *Prédiction : vraie.* L'information individuelle vaut mieux que l'information de groupe, personne ne le conteste, et cela doit se voir.
- **P3 (la prédiction qui décide, et la mienne est défavorable à l'objection).** Le meilleur comparateur équitable restera néanmoins **sous 3 % de top-1**, soit moins du sixième des 20,7 % du jumeau LLM. **Issue (a)** : la spécificité LLM tient. *Prédiction : vraie.*
- **P4 (où vit l'écart).** L'avantage du jumeau sera concentré sur les **40 items d'achat** ; sur les **20 autres items**, jumeau et comparateur équitable seront à moins d'un facteur 3 l'un de l'autre et tous deux proches du hasard (0,049 %). *Prédiction : vraie.*
- **P5 (le plafond du mandat ne tient pas tel qu'énoncé).** Les 81,6 % de l'attaquant « réponses passées » utilisent les réponses des vagues 1-3 **aux items attaqués eux-mêmes**, qui sont **exclues de la persona**. Ce n'est donc **pas** le plafond de l'entrée du jumeau, mais le plafond d'un auxiliaire **strictement différent et plus riche pour cette tâche**. Je prédis que le jumeau **dépassera** l'estimation du plafond de sa propre entrée (le meilleur comparateur équitable), c'est-à-dire que la « fraction de l'information d'identité transmise » **excédera 100 %** et n'est donc pas une fraction. *Prédiction : vraie.*

### 0.5 Critère de réfutation de mon propre audit

Ma prédiction **P3 est réfutée**, et l'objection l'emporte, si la **borne basse** de l'IC à
95 % du top-1 du meilleur comparateur équitable atteint **5 %** — auquel cas l'**issue (b)**
se réalise et la contribution doit être réécrite en « tout générateur conditionné sur
l'individu fuit ». L'**issue (c)** se réalise si cette borne basse dépasse la **borne haute**
de l'IC du jumeau LLM (22,5 %) : le jumeau dégraderait alors l'information qu'on lui donne,
et l'article devrait le dire.

Je préenregistre aussi que **P2 fausse serait un résultat en soi** : un comparateur
équitable qui ne ferait pas mieux que le comparateur de segment signalerait que les
634 colonnes de persona ne portent presque aucune information sur les 60 items attaqués,
ce qui rendrait la performance du jumeau d'autant plus difficile à expliquer.

### 0.6 Garde-fous

- Bassin strictement constant (2 058 / 2 058 / 60 items) pour toutes les conditions comparées, y compris les chiffres repris des deux branches. Deux erreurs de ce projet portent déjà sur ce point.
- `c7_controle_interpretabilite.controle_avant_interpretation` appelé sur chaque générateur avant toute interprétation, la baseline étant recalculée par la fonction sur le bassin réellement attaqué.
- Le donneur K1/K10 exclut toujours la personne elle-même ; le modèle K2 est ajusté **hors pli** (5 plis).
- Graine fixée. Aucune donnée individuelle, aucun `pid`, aucun appariement individuel n'est imprimé ni écrit : seuls des taux agrégés.
- Aucun appel de modèle de langage, aucun réseau, aucune dépense.

---

*(Sections 1 et suivantes écrites après calcul.)*
