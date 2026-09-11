# C7, contre-examen adverse (11 septembre 2026)
Relecture de `c7-preenregistrement.md`, `c7-resultats.md`, `analyses/c7_reidentification.py`. Script jetable hors dépôt (scratchpad de session), zéro appel LLM, lecture seule sur `data/`. **Taux agrégés seulement, aucun pid ni appariement.** Top-1 avec espérance exacte des ex aequo : il reproduit C7 (JSON 4.1 20,69 % contre 20,68 %, Demographics Only 2,15 % contre 2,13 %).

## 1. Comparateurs (60 items, 2 058 candidats de vague 4, hasard top-1 0,049 %, top-10 0,49 %)
B2 et PMM ré-entraînés avec `t1_baselines.calculer` inchangé (5 plis, 494 items de contexte des vagues 1-3 + 14 démographies), cible restreinte aux 60 items.
| prédicteur | exactitude 60 | top-1 [IC 95 %] | top-10 |
|---|---|---|---|
| retest humain, vagues 1-3 (plafond) | 0,745 | **81,6 %** [79,9 ; 83,2] | 91,6 % |
| JSON Persona GPT4.1 | 0,590 | **20,7 %** [19,1 ; 22,5] | 42,7 % |
| Text Persona Gemini / JSON mini (n = 1 000) | 0,56 / 0,55 | 13,1 % / 12,3 % | 32,4 % / 27,2 % |
| Demographics Only (LLM) | 0,494 | 2,15 % [1,6 ; 2,8] | 9,4 % |
| B1 argmax (14 démographies) | 0,504 | 0,30 % | 1,5 % |
| **PMM k=10** | 0,475 | **0,23 %** [0,06 ; 0,42] | 1,7 % |
| **B2 argmax** | 0,511 | **0,07 %** [0 ; 0,19] | 1,2 % |
| LR contexte (argmax / log-vraisemblance) | 0,475 | 0,22 % / 0,24 % | 1,8 % / 2,6 % |
| donneur k=1, vecteur entier du plus proche en contexte (donneur retiré des candidats) | 0,457 | 0,13 % | 1,5 % |
À exactitude comparable (0,47 à 0,51 contre 0,59), aucun prédicteur non LLM ne dépasse 0,3 %. **Le résultat n'est donc pas « toute prédiction individualisée identifie »** : c'est propre aux jumeaux LLM, parmi les comparateurs testés. Le retest montre que 60 réponses sincères sont une quasi-empreinte.

## 2. Fuite : non détectée
- Contexte B2/PMM : 0 colonne de vague 4, 0 QID de vague 4 ; NMI maximale contexte × item 0,16, contre 0,31 pour le retest sur le même item.
- Persona des jumeaux : l'audit de provenance trouve 0 des 75 QID répétés, **mais sur 294 personnes sur 2 058**, et l'objet (`wave_split` ou `full_persona`) reste invérifiable (R2). Test nouveau, sur les 2 058 personnes : sur les cellules où vague 4 ≠ vagues 1-3, la sortie JSON 4.1 égale la vague 4 dans 37,7 % des cas et les vagues 1-3 dans 37,9 %. Même symétrie (36 à 38 %) pour les 7 configurations. Une copie des réponses de vague 4 pencherait vers la vague 4 : aucun indice de copie.
- Canal de randomisation écarté : la colonne `k_Q295` est le produit k à prix fixe chez 100 % des personnes (alignement TWIN_ID = pid). Pas d'ordre ni de prix tiré par personne.

## 3. Où vit le signal (robustesse)
- **100 % dans les 40 items d'achat** (« achèteriez-vous ce produit à ce prix ? ») : JSON 4.1 à 33,1 % sur ces 40 seuls, **0,25 % sur les 20 autres items** (PMM 0,29 %), soit le niveau du hasard.
- Ce n'est pas la propension à acheter : une attaque par le seul nombre de « oui », même vrai (oracle), donne 0,29 %. La corrélation de ce compte vaut 0,16 pour JSON 4.1 et 0,52 pour une ridge non LLM. Le jumeau retrouve **quels** produits la personne achète.
- Autre métrique (accord pondéré par la rareté) : JSON 4.1 5,4 %, retest 70,3 %, PMM 0,29 %.
- 30 items tirés au hasard (moyenne de 20 tirages) : 7,6 %, retest 53,1 %, PMM 0,15 %.
- S1, candidats restreints aux 1 000 du périmètre JSON mini (hasard 0,1 %) : 25,4 %, retest 82,9 %, PMM 0,45 %.
- Test « démographies identiques » : 3 paires seulement, illisible.
Le résultat tient partout contre PMM et B2. Il fond d'un facteur 3 à 4 avec la rareté ou 30 items, et dépend entièrement d'un seul bloc.

## 4. Modèle de menace
Dans Twin, l'appariement est trivial sans attaque : pid et TWIN_ID, et selon l'audit les fichiers de jumeaux recopient ligne à ligne `StartDate`, `EndDate`, `Duration` et `RecordedDate` des humains. Le résultat vise un scénario hypothétique : un détenteur de panel publie des « jumeaux anonymes » sans clé. Un attaquant qui possède **les réponses réelles aux mêmes 40 questions d'achat** (initié, copropriétaire du panel, fuite du fichier source) relie alors un jumeau sur cinq à son répondant. Portée honnête : un fichier de jumeaux LLM individualisés reste **reliable à ses microdonnées sources** (critère de « linkability » du G29 et du RGPD). Il n'est donc pas anonyme par construction. Le résultat ne montre pas qu'un tiers retrouve une personne nommée à partir d'informations publiques : l'identifiant quasi requis est un questionnaire précis, rarement détenu hors du panel.

## 5. Antériorité
- Stadler, Oprisanu, Troncoso (USENIX Security 2022, *Synthetic Data – Anonymisation Groundhog Day*) : les données synthétiques issues de modèles génératifs restent reliables aux enregistrements sources. En substance, c'est connu.
- Les métriques de liaison et DCR sont standard pour les données tabulaires synthétiques (Giomi et al., arXiv 2211.10459).
- Park et al. 2024 (arXiv 2411.10109) restreignent l'accès aux réponses individuelles de leurs 1 052 agents pour raison de vie privée : risque anticipé, non mesuré.
- Le papier Twin-2K-500 ne traite ni vie privée ni liaison.
- Ré-identification par agents LLM (arXiv 2601.05918) : sur du texte et le web, autre objet.
- **Aucune mesure de ré-identification à partir de sorties catégorielles de jumeaux LLM trouvée**, recherche non exhaustive.

## 6. Verdict : **résultat réel mais connu en substance**
Réel : pas de fuite détectée, canal de randomisation écarté, écart de deux ordres de grandeur avec PMM, B2 et un donneur joint. Connu en substance : un enregistrement synthétique individualisé est reliable (Stadler 2022). Neuf mais étroit : la mesure sur des jumeaux LLM, la spécificité LLM face à des prédicteurs de même exactitude, la localisation sur les choix d'achat.

**À ne pas écrire** :
- le contraste « trop faibles pour te prédire » (Ahn et al., 3 %) : autre jeu, autre métrique, et sur ce bloc le jumeau porte bien un signal propre à la personne ;
- « te retrouver » sans préciser que l'attaquant détient déjà tes réponses ;
- 20,7 % sans dire que tout vient de 40 items d'achat.

**Titre honnête** : « Des jumeaux LLM restent reliables à leurs répondants : sur Twin-2K-500, leurs choix d'achat simulés désignent le bon répondant parmi 2 058 dans 21 % des cas, contre moins de 0,3 % pour des prédicteurs statistiques de même exactitude, à condition de détenir ses vraies réponses. »
