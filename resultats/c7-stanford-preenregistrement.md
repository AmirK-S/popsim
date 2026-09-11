# C7 Stanford, préenregistrement : le jumeau retrouve-t-il la personne, ailleurs que sur Twin ?

**Écrit le 12 septembre 2026, avant tout calcul d'appariement.** Réplique de
`resultats/c7-resultats.md` sur l'archive Stanford des 1 052 agents génératifs
(`data/osf-t6g7k-stanford/`), déjà publique. Aucune identité ni pid retrouvé n'est jamais
imprimé ni écrit ; seuls des taux agrégés sortent de `analyses/c7_stanford.py`.

## 0. Faisabilité vérifiée avant ce texte
`figure2/data/new_analysis_summaries/` apparie humains et agents sur les mêmes 1 052
`participant_XXXX`, mêmes lignes et ordre, en trois blocs : GSS (177 items catégoriels,
quasi aucun manquant), Jeux économiques (5 scores continus), Big Five (5 traits continus).
Vague 1 = cible, vague 2 = retest humain. `figure3/data/demographic_summary.csv` donne
genre, ethnicité, âge, éducation pour les mêmes identifiants. Appariement possible.

## 1. Attaque
Par bloc et par condition d'agent (composite, enquête, entretien, démographique, persona ;
v8 en exploratoire), comparer chaque ligne d'agent aux 1 052 humains de vague 1, ordre des
candidats mélangé. GSS : accord = 1 − distance de Hamming (`a2_commun.distance_hamming`,
repris tel quel). Jeux économiques et Big Five : accord = − distance euclidienne z-scorée
(seule différence de méthode avec Twin, imposée par des items continus).

## 2. Mesures et comparateurs
Top-1, top-10, rang médian, plus les trois mêmes dans le segment démographique (genre ×
ethnicité × âge replié × éducation repliée). IC 95 % par bootstrap sur les personnes, 2000
tirages, graine 20260912. Hasard = 1/1052 (top-1), 10/1052 (top-10). Démographique seul =
condition « agent démographique ». Référence humaine = vague 2 attaquant vague 1 (fournie
par les auteurs, « Participants »).

## 3. Différences déclarées avec Twin
Pas d'items d'achat : bloc dominant attendu = GSS, pas Jeux économiques / Big Five (5
dimensions chacun). Pas de manquants à contrôler. Segment démographique propre à Stanford.

## 4. Prédiction et critère « on fonce »
[HYPOTHÈSE] top-1 ≥ 10 % sur GSS pour au moins une condition riche, et ≥ 5 fois le top-1
démographique. Sinon, le rapport publie les taux mesurés sans relance.
