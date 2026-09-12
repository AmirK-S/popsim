# Positionnement vie privée — antériorité, lieux, collaborateurs, objections

Assemblage des recherches d'un agent précédent, disparu sans livrer ce fichier. Aucun calcul ni appel ici ; chiffres repris tels quels de `resultats/article-synthese.md`.

## 1. Antériorité — verdict

Aucun travail ne devance nos deux revendications neuves : le **canal inter-jumeaux** (A7 — relier deux ensembles de sorties synthétiques d'une même personne, sans aucune donnée réelle) et la **mesure de fuite en bits transportable entre jeux** (A4). Distinctions à écrire dans le texte :

- **Anonymeter** (Giomi et al., PoPETs 2023) — emploie « linkability », source de confusion possible. Sa définition formelle partitionne les attributs d'un **seul** jeu original, l'attaquant détenant les valeurs **réelles** d'une partie d'entre eux ; et elle conclut que la liaison est le risque le plus **faible** des trois qu'elle mesure — nous contredisons cette conclusion dans un régime qu'elle n'a pas testé (deux générations indépendantes, aucune valeur réelle détenue).
- **Synth-MIA** (Ward et al., arXiv 2509.18014) — énonce en prose la relation qualité-fuite sur 9 générateurs, mais avec une qualité **agrégée**, un risque d'**appartenance**, sans coefficient (seul chiffre : DCR contre Max-AUC, r = 0,225).
- **Guépin et al.** (arXiv 2307.01701) — supprime l'hypothèse de données auxiliaires réelles mais vise l'appartenance au jeu d'entraînement d'un générateur unique, jamais l'appariement entre deux générations indépendantes.
- **Ko et al.** (ICML 2026, arXiv 2603.18382) et **Lermen et al.** (arXiv 2602.16800) — le LLM y est l'attaquant sur du texte réel ; chez nous il est la source de la fuite.
- **Yeom et al.** (CSF 2018) et **Feldman** (STOC 2020) — parade contre « connu depuis 2018 » : ces résultats portent sur un modèle **entraîné** sur la population, avec écart train/test ; notre pipeline n'entraîne rien, la personne n'est dans aucun jeu d'entraînement, la fidélité vient du conditionnement.
- Notre **auto-réfutation** (le nul de marge de A1, réfutant l'axe unique) est elle-même une contribution, sur le modèle de Das, Zhang et Tramèr (arXiv 2406.16201, témoin aveugle en MIA sur modèles de fondation).
- La **mesure en bits** (A4) est un instrument dérivé, pas une découverte : cas de fuite en min-entropie de Rényi (Smith, FoSSaCS 2009) dans l'esprit du surprisal d'Eckersley (PETS 2010).

## 2. Cadrage retenu

L'axe unique « fidélité = identifiabilité » a été réfuté par notre propre témoin (nul de marge, A1) : le cadrage n'est plus causal mais empirique et borné — des taux de liaison mesurés sur deux jeux et en monde ouvert (90,40 % Park en monde fermé, 60,17 % en monde ouvert à 1 % de FPR) ; un canal inter-jumeaux répliqué sur deux jeux (A7) ; une mesure en bits transportable (A4) ; une défense chiffrée qui résiste à un attaquant adaptatif (0,24 % puis 0,29 %, A8/A11) ; et un couplage qualité-fuite documenté mais **non distinguable** d'un effet de qualité globale (A1).

## 3. Lieux de publication, classés

| Rang | Lieu | Échéance / cycle | Coût | Remarque |
|---|---|---|---|---|
| 1 | **PoPETs 2027.3** | dépôt 30 novembre 2026, cycle Revise ~4 mois | gratuit | présentation à distance admise ; taux d'acceptation ~26 % ; tête de liste |
| 2 | **Journal of Privacy and Confidentiality** | au fil de l'eau, ~24 semaines | 500 USD à l'acceptation | — |
| 3 | **Journal of Official Statistics** | au fil de l'eau | gratuit, accès libre | financé par Statistics Sweden |

Repli gratuit : *Transactions on Data Privacy* (diamant). À écarter : USENIX Security et CCS (présence payante obligatoire) ; ACM TOPS (frais pleins dès 2027).

## 4. Collaborateurs prioritaires

| Collaborateur | Institution | Accroche |
|---|---|---|
| Park & Bernstein | Stanford | « votre avertissement était exact, voici son ampleur mesurée » — 90,40 % en monde fermé sur leur propre archive |
| Toubia, Peng, Gui (tianyi.peng@columbia.edu) | Columbia | créateurs de Twin-2K-500 ; lettre de divulgation responsable déjà en brouillon |
| Luc Rocher (luc.rocher@oii.ox.ac.uk) | Oxford | mesure en bits (A4) répond au même problème de transportabilité que son κ de la loi d'échelle (*Nat. Commun.* 2025) |
| De Cristofaro & Ganev (emiliano.decristofaro@ucr.edu) | UC Riverside | angle MIA sur modèles de fondation, témoins aveugles (litt. proche de notre nul de marge A1) |
| Reiter (jreiter@duke.edu) & Drechsler | Duke / IAB | angle défense : notre D4 est une variante PRAM/data swapping dans leur tradition |
| Rothschild | Microsoft Research, co-président AAPOR | canal de politique publique |
| Creţu | CISPA | relecture méthodologique |

## 5. Objections prévisibles et parade

| Objection | Parade expérimentale |
|---|---|
| O1 — « Tautologie : un modèle fidèle identifie, évidemment » | Nul de marge (A1) : le rho observé (0,969) ne dépasse pas le nul (0,984) — objection non écartée sur ce point ; ce qui tient : A2, deux méthodes à exactitude quasi égale fuient à deux ordres de grandeur d'écart |
| O2 — « Twin/Stanford se contredisent, artefact de taille de bloc » | Contrôle à 20 items : Stanford 11,7 % contre Twin 0,24 %, à entropie par item inférieure — ni le nombre d'items ni l'entropie n'expliquent l'écart |
| O3 — « Ce n'est pas de la ré-identification, l'attaquant a déjà les réponses » | Assumé : cadrage *linkability* (G29/RGPD) explicite ; A7 élargit la menace à un tiers sans aucune réponse humaine |
| « Connu depuis 2018 » (Yeom/Feldman) | Leur cadre suppose un modèle entraîné sur la population avec écart train/test ; ici rien n'est entraîné, la fidélité vient du conditionnement |
| « Anonymeter a déjà mesuré ça » | Anonymeter détient des valeurs réelles sur un seul jeu et conclut que la liaison est le risque le plus faible ; nous contredisons cette conclusion dans un régime non testé par eux (A7) |
| « La DP suffit » | A12 : la DP protège l'appartenance, pas la liaison d'un individu déjà connu ; le générateur DP n'échappe à notre attaque qu'en refusant la tâche même du jumeau (fidélité quasi nulle) |
| « Votre défense est fragile face à un attaquant qui connaît le mécanisme » | A8/A11 : attaquant adaptatif informé plafonne à 0,29 %, deux ordres de grandeur sous 20,69 % non défendu |
| « Le couplage qualité-fuite est un artefact de dragage » | 3 bis : 34 prédictions préenregistrées, 11 réfutées et 3 non concluantes (~un tiers) — signature inverse d'un dragage |

## 6. Vérifications bibliographiques restantes

1. **Anonymeter (Giomi et al., PoPETs 2023)** : relire la définition formelle de la *linkability* sur le PDF original, pour confirmer la citation ajoutée à A7 (partition d'un seul jeu, valeurs réelles détenues par l'attaquant).
2. **ZAK-MIA (PoPETs 2024)** : l'extraction de son contenu a échoué lors de la veille d'antériorité — à reprendre pour vérifier l'absence de chevauchement avec A1/A7.
