# C7, resultats : le jumeau ne predit pas la personne, mais il la retrouve

Preenregistre dans `resultats/c7-preenregistrement.md`, calcule par `analyses/c7_reidentification.py`
(60 items communs, 20 tirages de depart pour les ex aequo, bootstrap 2000, graine 20260911). Etude de
risque de vie privee sur Twin-2K-500, deja public. **Aucune identite ni pid n'est imprime ici**, tout
est un taux agrege sur `resultats/c7-reidentification.csv` et `c7-controle-motifs-manquants.csv`.

## 1. Ré-identification, cible = humains de vague 4, sur 2 058 candidats

| configuration | n attaques | top-1 | IC 95 % | top-10 | rang median | top-1 dans segment S_gra |
|---|---|---|---|---|---|---|
| Demographics Only | 2 058 | 2,13 % | [1,56 ; 2,75] | 9,38 % | 301 | 13,98 % |
| JSON Persona GPT4.1 | 2 058 | **20,68 %** | [18,96 ; 22,43] | 42,75 % | 20 | 45,71 % |
| JSON Persona GPT4.1-mini | 1 000 | 12,26 % | [10,27 ; 14,29] | 27,44 % | 67 | 32,35 % |
| Text Persona Gemini-Flash2.5 | 2 058 | 13,12 % | [11,78 ; 14,50] | 32,31 % | 40 | 36,68 % |
| Text Persona (Reasoning) | 2 058 | 9,34 % | [8,19 ; 10,61] | 24,42 % | 87 | 28,26 % |
| Text Persona (Repeating Questions) | 2 058 | 7,35 % | [6,29 ; 8,35] | 23,17 % | 83 | 28,15 % |
| Text Persona mini | 2 058 | 5,53 % | [4,63 ; 6,46] | 19,28 % | 113 | 25,70 % |
| Text Persona (temp. defaut) | 2 058 | 5,58 % | [4,64 ; 6,50] | 17,96 % | 126 | 23,85 % |

Hasard : top-1 = 0,0486 %, top-10 = 0,486 %, rang median attendu ≈ 1 029. Sur vagues 1-3 comme cible
secondaire, les taux sont proches a 1-2 points (JSON Persona GPT4.1 : 19,07 % top-1) : la fuite ne
tient pas a la vague exacte utilisee comme base de comparaison.

## 2. Controle anti-triche : motifs de manquants seuls

Attaque identique, mais sur le seul vecteur present/absent des 108 items (aucune valeur) : top-1
entre 79,85 % et 80,22 % selon la configuration, tres loin du hasard global (0,05 %) mais **collant
au hasard conditionnel a la taille du groupe de motif partage** (0,80 ; ecart < 0,006 partout). Sur
Twin, 1 651 motifs de manquants sont deja quasi uniques sur 2 058 personnes : c'est l'affectation aux
bras inter sujets, pas une empreinte propre au jumeau. Le controle passe donc au sens preenregistre
(rien au dela du plancher structurel), et confirme que restreindre l'attaque principale aux 60 items
toujours renseignes elimine bien ce canal.

## 3. Verdict par rapport au critere preenregistre

**Critere : top-1 >= 10 % ET >= 2x Demographics Only, pour au moins un jumeau riche. Rempli.**
JSON Persona GPT4.1 atteint 20,7 %, soit 9,7 fois Demographics Only (2,13 %) et 425 fois le hasard.
Quatre configurations sur sept depassent 10 %, les trois autres restent a 2,6-4,4 fois Demographics
Only. **On fonce.**

## 4. Ce que ça implique pour la publication de jumeaux

Un jumeau qui n'explique que quelques points de variance propre au repondant (cf. Ahn et al., 3,05 %)
peut neanmoins retrouver ce repondant, dans un cinquieme des cas, parmi plus de deux mille inconnus,
loin au dela de ce que la demographie seule permet. Ce n'est pas une fuite de texte libre ni d'identite
directe : c'est un motif de reponses categorielles suffisamment specifique pour trier une population.
Publier des sorties de jumeaux individuelles, meme depourvues de nom, mérite donc le même soin qu'un
jeu de microdonnees appariables, sans que cela remette en cause l'utilite du jeu Twin-2K-500 pour la
recherche en agregat.
