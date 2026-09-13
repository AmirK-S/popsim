# C7, décomposition du signal de ré-identification en population / segment / personne — préenregistrement (13 septembre 2026)

statut: courant
mandat: Trancher l'objection R4 de `resultats/relecture-post-nuit-2026-09-13.md` — quelle part des 20,7 % de ré-identification est une propriété de *cette personne*, plutôt qu'une structure de population qu'un modèle de langage reproduit bien sur un bloc produit × prix. Décomposer le taux en trois niveaux (population, segment, personne), construire le témoin à segment constant qui tranche sans soustraction de moyennes, et déclarer avant calcul le seuil sous lequel l'article change de nature. Aucun appel payant, aucun réseau, aucun arrière-plan, aucune donnée individuelle imprimée.
agent: Claude Opus 5, Anthropic — sous-agent décomposition du signal
ecriture: analyses/c7_decomposition_signal.py, resultats/c7-decomposition-signal-preenregistrement.md, resultats/c7-decomposition-signal-resultats.md, resultats/c7-decomposition-signal.csv
lecture_seule: tout le reste du dépôt
interdits: appel payant, réseau, recherche web, arrière-plan, commit sur master, fusion, écriture dans article/manuscrit.md, impression de tout identifiant / réponse / appariement individuel
cecite: je n'ai pas lu article/manuscrit.md (propriété d'un autre agent) ; je ne sais pas si « items d'achat » et « items binaires » désignent la même partition — un autre agent l'examine, je n'anticipe pas son verdict et je n'affirmerai rien sur la cause de la concentration
cout_reel_usd: 0.00

---

## 0. Ce que j'attaque

> « Un objet qui ne contient par construction aucune information individuelle bat déjà de
> 2,7× la baseline démographique, uniquement parce qu'un LLM produit des vecteurs de réponses
> dont la structure de dépendance ressemble à celle des humains. […] Ce qui est mesuré
> pourrait être, pour une part inconnue, un artefact de population […] et non la trace d'une
> personne. Le papier a le témoin qui trancherait pour le canal jumeau-à-jumeau mais n'a pas
> l'équivalent pour la mesure T1 qui porte le titre. »
> — `resultats/relecture-post-nuit-2026-09-13.md`, objection R4

La décomposition personne / segment / population existe pour le canal entre jumeaux. Elle
n'existe pas pour l'attaque qui porte le titre de l'article. Ce document et les deux qui le
suivent la construisent.

## 1. Les faits d'entrée, établis AVANT toute prédiction, et donc déclarés et non prédits

Établis le 13 septembre 2026 avant l'écriture de la section 2, sur le bassin exact de
l'attaque (2 058 personnes, 60 items de `c7_reidentification.items_communs`, dont 40 de
suffixe `_Q295`) :

1. **La segmentation S_gra** (genre × ethnicité × âge, la lecture principale du dépôt) découpe
   les 2 058 personnes en **40 segments**, aucune personne non affectée, taille médiane
   **124**, taille moyenne **139,8**.
2. **Le plafond de segment pour le top-1**, c'est-à-dire ce qu'obtient un attaquant qui
   connaît *parfaitement* le segment de sa cible et **tire au hasard à l'intérieur**, vaut
   `E[1/|S_gra|]` = **1,944 %** sur ce bassin. Le hasard sans segment vaut 1/2 058 =
   **0,0486 %**.
3. **Le jumeau « Demographics Only - GPT4.1-mini » atteint 2,15 %** [1,57 ; 2,77]
   (`resultats/c7-audit-comparateur-conditionne.csv`, bloc `tous`). Ce chiffre et le plafond
   de segment du point 2 sont du même ordre. **C'est une coïncidence de valeurs constatée
   avant calcul, ce n'est pas encore un résultat** : rien n'établit à ce stade que le jumeau
   segment-seul ne fait *que* du segment, et c'est précisément ce que la section 3 teste.
4. **Ce que « Demographics Only » a réellement reçu.** L'audit
   `resultats/audit-comparateur-conditionne-2026-09-13.md` (§1) a établi depuis
   `question_catalog.json` et `wave_persona_chunk_001.parquet` que le jumeau persona est
   conditionné sur les 634 colonnes `wave1_3_persona_json` et que les 60 items attaqués sont
   **60 sur 60** de source `wave4_Q_wave1_3_A`, donc absents du conditionnement. Je
   **n'utiliserai pas la valeur 2,15 % comme témoin du niveau segment sans l'avoir vérifiée
   moi-même** : la section 3 du rapport de résultats contrôlera, sur les sorties elles-mêmes,
   que ce jumeau ne porte aucune information individuelle — un objet qui n'aurait vu que le
   segment doit produire des vecteurs **échangeables à l'intérieur d'un segment**.

## 2. Les trois niveaux, définis avant calcul

**Bassin strictement constant partout** : 2 058 attaqués, 2 058 candidats, 60 items, attaque
`c7_reidentification.rangs_attaque` importée sans réimplémentation, graine **20260913**.

- **N1, plancher de population.** Ce qu'obtient une attaque qui n'exploite ni segment ni
  personne, seulement la structure des réponses dans la population : le hasard (0,0486 %), le
  générateur à marginales indépendantes de population (recalculé ici sur le bassin exact), et,
  en rappel lu au CSV, le meilleur générateur classique conditionné au segment
  (`c7-controle-generateur.csv`, 0,1535 %).
- **N2, marche du segment.** Le supplément obtenu en connaissant le segment démographique :
  le plafond `E[1/|S_gra|]` et le jumeau segment-seul, après vérification du point 1.4.
- **N3, marche de la personne.** Le reste, jusqu'aux 20,66 % du jumeau JSON Persona GPT-4.1.

**Deux échelles, les deux publiées, aucune choisie après coup.** Une décomposition de taux n'a
pas d'échelle canonique et le choix décide du verdict ; je fixe donc les deux avant de
calculer.

- **Échelle des taux** : part personne = (T_personne − T_segment) / T_personne.
- **Échelle des bits d'identité** (log₂ du rapport au hasard, l'échelle déjà employée au §5.6
  du manuscrit) : part personne = log₂(T_personne/T_segment) / log₂(T_personne/T_hasard).

## 3. Le témoin qui tranche, défini avant calcul

Une décomposition par soustraction de moyennes est faible : elle suppose que les deux marches
s'additionnent. Le témoin direct ne suppose rien.

**Témoin à segment constant.** Pour chaque personne attaquée, le pool de candidats est
**restreint à son propre segment S_gra**. La question devient exactement celle du relecteur :
*le jumeau d'une personne retrouve-t-il cette personne mieux qu'il ne retrouve une autre
personne du même segment ?* Toute l'information de segment est tenue constante par
construction ; ce qui reste ne peut plus être une structure de segment.

Deux mesures, parce que la première dépend d'une convention d'ex æquo et la seconde non :

- **T1 intra-segment** : taux de top-1 dans le pool du segment, à comparer au hasard
  intra-segment `E[1/|S_gra|]`. **Convention d'ex æquo déclarée** : celle du dépôt — départage
  aléatoire, moyenné sur 20 tirages, graine fixée (`c7_reidentification.rangs_attaque`). Le
  dépôt a mesuré que la convention vaut un facteur **1,32 sur Twin** et jusqu'à **130** sur
  d'autres jeux (`c7-residu-trajectoire-resultats.md` §7) : le chiffre est donc publié avec sa
  convention, jamais nu.
- **AUC intra-segment**, insensible à la convention : la probabilité que le jumeau de la
  personne *i* s'accorde mieux avec *i* qu'avec un rival *j* tiré dans le même segment, les ex
  æquo comptés une demi-unité. **0,5 = aucune trace de personne**, et cette valeur ne dépend
  d'aucune convention de départage. C'est le chiffre le plus difficile à contester et c'est
  celui que je considérerai comme décisif.

**Le contrôle négatif obligatoire** : les deux mesures sont calculées **aussi** sur le jumeau
Demographics Only, qui n'a jamais vu l'individu. S'il n'est pas au hasard intra-segment et à
AUC 0,5, mon témoin est cassé et je le dirai avant d'interpréter quoi que ce soit du jumeau
persona.

**Lecture par famille d'items** : tout est refait sur les 40 items `_Q295` et sur les 20
autres, bassin de personnes inchangé. Je ne dirai **rien** sur la cause de la concentration ni
sur la coïncidence éventuelle entre « items d'achat » et « items binaires ».

## 4. Mes prédictions, fixées avant calcul

- **P1 (échelle des taux, favorable à l'article).** La part personne dépassera **85 %**.
  *Prédiction : vraie.*
- **P2 (échelle des bits, défavorable à l'article, et je la préenregistre pour cela).** Sur
  l'échelle des bits d'identité, la part personne sera **inférieure à celle du segment** :
  entre **30 % et 45 %**. Autrement dit, la même mesure soutient deux récits opposés selon
  l'échelle, et l'article ne peut pas publier la part sans publier l'échelle. *Prédiction :
  vraie.*
- **P3 (contrôle négatif).** Le jumeau Demographics Only sera **au hasard à segment
  constant** : AUC intra-segment dans [0,48 ; 0,52], IC contenant 0,50, et T1 intra-segment
  compatible avec 1,944 %. *Prédiction : vraie.*
- **P4 (le témoin décisif).** Le jumeau JSON Persona GPT-4.1 sera **très loin** du hasard à
  segment constant : AUC intra-segment ≥ **0,80**, et T1 intra-segment ≥ **25 %**, soit un
  facteur ≥ 12 sur le hasard intra-segment. *Prédiction : vraie.*
- **P5 (familles d'items).** La décomposition **ne sera pas la même** : sur les 40 items
  `_Q295`, AUC intra-segment ≥ 0,85 ; sur les 20 autres, l'AUC intra-segment du jumeau
  persona ne sera **pas distinguable de 0,50** (IC contenant 0,50). *Prédiction : vraie.*

## 5. Le seuil de réfutation — ce qui ferait changer l'article de nature

Il est déclaré ici, avant tout calcul, et il n'est pas négociable après.

**Seuil décisif D.** Si la **borne basse** de l'IC à 95 % de l'**AUC intra-segment** du jumeau
JSON Persona GPT-4.1, sur les 60 items, **n'atteint pas 0,55**, alors l'avantage du jumeau
disparaît à segment constant, **tout le signal est au niveau du segment ou de la population**,
et l'article doit changer de nature : il ne mesure pas une trace individuelle, il mesure la
capacité d'un modèle de langage à produire une structure de réponses réaliste sur un bloc, et
son titre, son résumé et sa contribution doivent être réécrits en conséquence.

**Seuil secondaire S.** Si la part personne sur l'échelle des taux tombe **sous 50 %**, ou si
la part personne sur l'échelle des bits tombe **sous 20 %**, l'article doit requalifier les
20,7 % comme une grandeur **majoritairement de population**, et publier le niveau segment
comme baseline officielle de la mesure T1 — non comme une remarque de passage.

**Ce que je m'interdis.** Conclure en faveur de l'article par défaut. Si D ou S se déclenche,
le rapport de résultats le dit en première ligne, quel que soit le coût pour le dépôt.

## 6. Garde-fous

- Bassin strictement constant (2 058 / 2 058 / 60 items) pour toutes les conditions, y compris
  les chiffres repris d'autres branches ; tout chiffre d'un autre bassin est signalé comme tel
  et n'entre dans aucune comparaison.
- `c7_controle_interpretabilite.controle_avant_interpretation` appelé avant toute
  interprétation, la baseline étant recalculée par la fonction sur le bassin réellement
  attaqué — jamais fournie par l'appelant.
- Convention d'ex æquo déclarée (section 3) et publiée avec chaque taux ; l'AUC, qui n'en
  dépend pas, porte le verdict.
- Graine fixée (20260913). IC par bootstrap sur les **personnes**, jamais sur les cellules.
- Aucune donnée individuelle, aucun `pid`, aucun appariement individuel imprimé ni écrit :
  seuls des taux agrégés et des tailles de segment.
- Les treize formulations interdites de `resultats/marqueurs-canoniques-2026-09-13.md` §3 sont
  respectées ; en particulier aucun facteur chiffré entre époques (I8), aucun emploi des mots
  proscrits par I1, et le plafond des générateurs classiques est cité à **0,1535 %** (I11).
- Aucun appel de modèle de langage, aucun réseau, aucune dépense.

---

*(Ce document est commité avant le premier calcul de décomposition. Les résultats sont dans
`resultats/c7-decomposition-signal-resultats.md`.)*
