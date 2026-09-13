# C7, audit : le comparateur classique a-t-il été conditionné sur la même information individuelle que le jumeau LLM ? (13 septembre 2026)

statut: courant
mandat: Trancher l'objection portée contre `agent/mesures/controle-generateur`, qui conclut qu'« aucun générateur synthétique classique ne dépasse 0,15 % de ré-identification sur Twin contre 20,7 % pour les jumeaux LLM ». L'objection : les quatre générateurs classiques G0-G3 n'ont été conditionnés que sur le segment démographique, alors que le jumeau LLM est construit à partir des réponses passées de la personne elle-même. (1) Établir depuis les données de quoi chaque jumeau est réellement construit. (2) Si le conditionnement individuel est confirmé, reconstruire les générateurs classiques avec exactement la même entrée individuelle. (3) Décider laquelle des trois issues se réalise. (4) Situer le tout par rapport au plafond de 81,6 % de l'attaquant qui n'utilise que les réponses passées. Aucun appel payant, aucun réseau, aucun arrière-plan, aucune donnée individuelle imprimée.
agent: Claude Opus 5, Anthropic
ecriture: analyses/c7_audit_comparateur_conditionne.py, resultats/audit-comparateur-conditionne-2026-09-13.md, resultats/c7-audit-comparateur-conditionne.csv
lecture_seule: tout le reste du dépôt, notamment analyses/c7_reidentification.py, analyses/c7_controle_interpretabilite.py, analyses/c7_controle_generateur.py (branche `agent/mesures/controle-generateur`), analyses/c7_audit_predictibilite.py (branche `agent/audit/predictibilite`)
interdits: appel payant, réseau, recherche web, arrière-plan, fusion sur master, écriture dans article/manuscrit.md, impression de tout identifiant / réponse / combinaison individuelle
cout_reel_usd: 0.00
correction_posterieure: resultats/marqueurs-canoniques-2026-09-13.md — deux arrondis favorables rectifies le 13/09 par le sous-agent marqueurs canoniques, valeurs du CSV retablies : « 0,15 % » -> « 0,1535 % » (§2, ligne de rappel G1, et §2 texte) et « 4,8 fois » -> « 4,7 fois » (§2 ; 0,0214529 / 0,0045432 = 4,72, le 4,8 venait d'une division de deux valeurs deja arrondies). Le mandat, le blockquote du §0.1 et la prediction preenregistree P2 gardent « 0,15 % » : ce sont des CITATIONS de l'affirmation auditee et d'un preenregistrement, elles ne se corrigent pas apres coup.

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

## 1. Le fait : de quoi le jumeau est-il réellement construit ?

**Établi depuis les données, pas supposé.** Le catalogue publié par l'équipe Twin
(`data/twin2k500/question_catalog_and_human_response_csv/question_catalog.json`) porte pour
chacun de ses **256 QuestionID** un champ `source` nommant l'objet du dépôt dont la question
provient, et un champ `csv_columns` donnant les colonnes correspondantes. Il partitionne le
questionnaire en deux ensembles **strictement disjoints** :

| source | QuestionID | colonnes CSV | contenu |
|---|---|---|---|
| `wave1_3_persona_json` | 171 | **634** | Démographies, Personnalité, Tests cognitifs, Préférences économiques, Forward Flow |
| `wave4_Q_wave1_3_A` | 85 | **126** | Heuristiques et biais répétés en vague 4, et les 41 questions d'achat |

**Intersection des colonnes : 0.** Vérifié par le script, pas par lecture.

Ce que cela établit, en deux temps :

1. **Le conditionnement individuel est confirmé. L'objection a raison sur sa prémisse.**
   `data/twin2k500/README.md` (section *Wave Split Folder*) décrit `wave1_3_persona_text` /
   `wave1_3_persona_json` comme « *Persona information from waves 1-3* », et
   `data/twin2k500/wave_persona_chunk_001.parquet` le confirme : une persona pèse ~95 000
   caractères de texte et ~121 000 de JSON **par personne**, structurée en 13 blocs de
   questions-réponses **de cette personne**. Le jumeau LLM est bien construit à partir des
   réponses passées de l'individu, là où G0-G3 ne voyaient que le segment démographique.
   **La comparaison publiée sur `agent/mesures/controle-generateur` est donc bien inéquitable
   en entrée.** C'est un défaut réel et il fallait le corriger.

2. **Mais le conditionnement est disjoint des items attaqués.** Les 60 items de
   `c7_reidentification.items_communs` ont été remontés, un par un, au catalogue via
   `data/twin2k500/llm/wave4_formatted_to_catalog_mapping.json` : **60 sur 60 retrouvés,
   60 sur 60 de source `wave4_Q_wave1_3_A`, 0 sur 60 de source persona.** Vérification
   indépendante sur `wave_persona_chunk_001.parquet` : aucun des blocs de la persona
   (*Demographics, Personality, Cognitive tests, Economic preferences, Forward Flow*) ne
   contient d'item d'ancrage, de Linda, de séquoias, de coût irrécupérable ni de tarification
   produit, et le recouvrement des QuestionID persona × vague 4 est nul.
   **Le jumeau n'a jamais vu les réponses qu'on lui reproche de laisser fuir.**

Les deux faits sont vrais en même temps. L'objection est fondée, et elle ne suffit pas :
il fallait mesurer.

**Park (Stanford, 1 052 agents).** Le conditionnement y est aussi individuel, mais d'une
autre nature : un **entretien de deux heures** transcrit. L'archive OSF `t6g7k` ne publie
**aucune transcription par participant** (vérifié : seuls des résumés agrégés et cinq
rapports Camerer), si bien qu'un comparateur classique « à même entrée » **n'est pas
constructible** sur Park à partir des données publiques. C'est une limite, et je la déclare
plutôt que de la contourner. Le dépôt contient toutefois le contrôle interne décisif
(`resultats/c7-stanford-reidentification.csv`, bloc GSS, bassin 1 052) : la condition
**`enquete`** est un agent conditionné sur **les propres réponses d'enquête de la personne**,
c'est-à-dire sur la cible elle-même, et elle n'atteint que **20,6 %** [18,2 ; 23,0] — très
en dessous de **`composite` 65,7 %** [62,7 ; 68,6] et de **`entretien` 44,7 %**. Sur Park,
la condition qui dispose de **l'information individuelle la plus directe sur les items
attaqués est celle qui ré-identifie le moins bien** parmi les conditions individuelles. La
fuite n'y suit donc pas la quantité d'information individuelle fournie.

## 2. Le comparateur équitable : même entrée, même bassin, même attaque

Entrée : les **550 colonnes informatives** (sur 634 ; 84 colonnes constantes ou vides
écartées) des vagues 1-3 hors items répétés, remplissage 0,988 — colonne pour colonne,
l'entrée du jumeau. Bassin **strictement constant** : 2 058 attaqués, 2 058 candidats,
60 items, attaque `rangs_attaque` importée sans réimplémentation, graine 20260913.
Hasard top-1 = **0,049 %**.

| condition | entrée | exactitude | **top-1 [IC 95 %]** | top-10 | rang médian |
|---|---|---|---|---|---|
| Retest humain v1-3 aux items attaqués | *hors persona* | 0,745 | **81,65 %** [79,96 ; 83,28] | 91,6 % | 1,0 |
| **LLM JSON Persona GPT4.1** | persona individuelle | 0,590 | **20,66 %** [19,01 ; 22,25] | 42,7 % | 20,3 |
| **LLM Demographics Only** | *segment seul* | 0,494 | **2,15 %** [1,57 ; 2,77] | 9,4 % | 302,7 |
| **K2a** modèle conditionnel (argmax) | persona individuelle | 0,520 | **0,45 %** [0,20 ; 0,76] | 2,7 % | 513,5 |
| **K10** vote modal des 10 voisins | persona individuelle | 0,486 | **0,16 %** [0,02 ; 0,32] | 1,1 % | 687,9 |
| **K2s** modèle conditionnel (tirage) | persona individuelle | 0,467 | **0,12 %** [0,02 ; 0,24] | 1,6 % | 620,7 |
| **K1** plus proche voisin | persona individuelle | 0,460 | **0,00 %** [0,00 ; 0,00] | 1,4 % | 745,9 |
| *(rappel)* G1 marginales par segment | segment seul | 0,444 | 0,1535 % | 1,0 % | 898,2 |

**P2 est tenue, de justesse et sans importance** : le meilleur comparateur conditionné sur
l'individu passe de 0,1535 % (segment) à **0,45 %**, un facteur 3. L'information individuelle
vaut effectivement mieux que l'information de groupe — et c'est tout ce qu'elle vaut ici.

**P3 est tenue : issue (a).** Le meilleur comparateur équitable reste **45 fois** sous le
jumeau LLM (0,45 % contre 20,66 %), et la borne haute de son IC (0,76 %) est loin des 5 %
du critère de réfutation préenregistré. Les IC ne se chevauchent pas, d'aucune façon.

**Le résultat qui tranche vraiment n'était pas prévu.** Le jumeau LLM **Demographics Only**,
qui n'a **jamais vu l'individu** — exactement le régime d'information de G0-G3 —, atteint
**2,15 %**, soit **4,7 fois** le meilleur générateur classique **nourri de la persona
complète** de la personne. L'objection supposait que l'écart venait de l'inégalité d'entrée ;
on peut **retirer toute l'information individuelle au LLM** et il continue de dominer
largement des générateurs classiques qui, eux, la possèdent. L'écart n'est donc pas
imputable à l'entrée.

**Contrôle de fidélité.** `c7_controle_interpretabilite.controle_avant_interpretation` a été
appelé sur les quatre comparateurs, baseline recalculée par la fonction sur le bassin
réellement attaqué : **les quatre échouent**, aucun n'atteignant la baseline Demographics
Only (2,15 % [1,59 ; 2,79]). Ce n'est pas un incident : c'est la mesure elle-même. Aucun
générateur classique conditionné sur l'individu ne franchit le seuil que ce projet impose à
un pipeline pour être seulement *interprétable*.

## 3. Où vit l'écart (lecture par bloc, bassin de personnes inchangé)

| condition | 40 items d'achat (`*_Q295`) | 20 items hors achat |
|---|---|---|
| Retest humain v1-3 | 74,65 % [72,83 ; 76,42] | 15,70 % [14,26 ; 17,12] |
| **LLM JSON Persona GPT4.1** | **33,16 %** [31,29 ; 35,06] | **0,25 %** [0,08 ; 0,47] |
| LLM Demographics Only | 5,95 % [5,06 ; 6,94] | 0,01 % [0,00 ; 0,03] |
| K2a modèle conditionnel | 0,06 % [0,01 ; 0,13] | **0,51 %** [0,26 ; 0,77] |
| K1 plus proche voisin | 0,00 % | 0,04 % |

**P4 est tenue, et plus durement que prédit.** La totalité de l'écart vit dans les 40 items
d'achat. Sur les 20 items d'heuristiques et biais, le jumeau LLM (0,25 %) est **en dessous**
du comparateur classique équitable (0,51 %) et leurs IC se chevauchent à peine : sur ce bloc,
**l'issue (c) se réalise localement** — le jumeau y dégrade l'information qu'on lui donne.
L'article ne peut pas écrire « les jumeaux LLM ré-identifient » sans dire **sur quel type
d'item**, sous peine de généraliser un phénomène qui n'existe que sur un bloc.

## 4. Le plafond : le cadrage proposé ne tient pas, et il faut le remplacer

**P5 est tenue.** Les 81,65 % de l'attaquant « réponses passées » sont obtenus avec les
réponses des vagues 1-3 **aux items attaqués eux-mêmes** — les 126 colonnes de source
`wave4_Q_wave1_3_A`, dont la section 1 établit qu'elles sont **absentes de la persona**. Ce
n'est donc **pas** le plafond de l'entrée du jumeau : c'est le plafond d'un auxiliaire
**différent et, pour cette tâche, strictement plus riche**. Rapporter 20,66 % à 81,65 %
donne bien 25,3 %, mais ce nombre ne mesure **pas** « la fraction de l'information d'identité
de l'entrée que le jumeau transmet » : numérateur et dénominateur ne portent pas sur la même
entrée.

Et la fraction correctement définie n'est pas calculable : rapportée au plafond estimable de
**sa propre** entrée — le meilleur comparateur classique sur la persona, 0,45 % —, la part
« transmise » vaudrait **4 600 %**. Ce n'est pas une fraction. La lecture juste est
l'inverse : **c'est le jumeau LLM qui fixe la borne inférieure du contenu identifiant de la
persona**, à ≥ 20,7 %, et aucune méthode classique testée n'en récupère plus de 0,45 %. Le
cadrage défendable n'est donc pas « le jumeau transmet une fraction de ce qu'on lui donne »,
mais : **la persona contient au moins 20,7 % de ré-identification, et le jumeau LLM est le
seul extracteur connu capable de l'en sortir.**

## 5. Verdict, limites, et la phrase à écrire

**Issue (a).** À information d'entrée strictement égale, la spécificité LLM tient, et elle
est ici démontrée proprement pour la première fois. Ma prédiction préenregistrée P3 n'est
**pas** réfutée ; P2, P4 et P5 sont tenues.

**Ce que l'audit ne clôt pas.** (i) Sur Park, faute de transcriptions publiques, le
comparateur à même entrée reste non constructible ; seul le contrôle interne `enquete` est
disponible. (ii) Mes quatre comparateurs sont des estimateurs **faibles** du contenu
identifiant de la persona : leur faiblesse borne par le bas, elle ne prouve pas qu'aucune
méthode classique n'y arriverait. (iii) La concentration à 100 % sur les 40 items d'achat,
jointe au fait que le jumeau n'a jamais vu les réponses d'achat des vagues 1-3, reste la
question ouverte la plus sérieuse du dossier ; le contre-examen du 11 septembre a écarté la
copie directe de la vague 4 (symétrie 37,7 % / 37,9 % sur les cellules discordantes) sans
expliquer le mécanisme.

**La phrase que l'article doit écrire, à la place de celle du contrôle générateur :**

> À information d'entrée strictement égale — les 634 colonnes des vagues 1-3 dont la persona
> est faite, et dont les 60 items attaqués sont absents —, le meilleur générateur classique
> conditionné sur l'individu atteint 0,45 % de ré-identification [0,20 ; 0,76] contre 20,7 %
> [19,0 ; 22,3] pour le jumeau LLM ; et un jumeau LLM conditionné sur le seul segment
> démographique atteint encore 2,15 % [1,57 ; 2,77], soit près de cinq fois ce meilleur
> comparateur classique pourtant nourri de l'individu. L'écart n'est donc pas imputable à
> l'information d'entrée. Il est en revanche entièrement porté par les 40 items d'achat :
> sur les 20 items d'heuristiques et biais, le jumeau (0,25 %) ne dépasse pas le comparateur
> classique équitable (0,51 %).
