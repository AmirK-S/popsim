# C7, generateurs individualises : resultats (12 septembre 2026)
Preenregistre dans `c7-generateur-preenregistrement.md`, calcule par `analyses/c7_generateur.py`
(attaque rejouee via `c7_reidentification.rangs_attaque`, importee sans modification). Deux
generateurs conditionnes sur le meme contexte que B1/B2/PMM (494 items de vagues 1-3 + 14
demographies, jamais les items cibles) : **G-LR** (regression logistique multinomiale,
ECHANTILLONNAGE dans la distribution predite, pas l'argmax) et **G-copule** (memes probabilites
+ copule gaussienne pour la dependance entre items). CART sequentiel (`synthpop`) : absent de
l'environnement Python, non teste, comme prevu.
## 1. Calibration : plafond sous la cible
Balayage 0,02 a 3 (26 points, `c7-generateur-calibration.csv`) : exactitude plate a
0,475-0,476 pour T <= 0,3 (quasi l'argmax), ne baisse qu'au-dela. **Les deux generateurs
plafonnent vers 0,476**, sous la cible 0,590 (JSON Persona GPT4.1) : le plafond deja vu pour
une LR sur ce contexte au contre-examen (0,475 argmax). Risque anticipe, confirme. T retenu
(le plus proche de la cible) : G-LR 0,1, G-copule 0,2.
## 2. Exactitude contre fuite (60 items, pool = 2 058)
| predicteur / generateur | exactitude | top-1 [IC 95%] | top-10 | rang median |
|---|---|---|---|---|
| retest humain (plafond) | 0,745 | 81,6 % | 91,6 % | -- |
| JSON Persona GPT4.1 (jumeau LLM) | 0,590 | **20,7 %** [19,0;22,4] | 42,7 % | 20 |
| Demographics Only (LLM) | 0,494 | 2,15 % [1,6;2,8] | 9,4 % | -- |
| B2 argmax | 0,511 | 0,07 % [0;0,19] | 1,2 % | -- |
| **G-LR (echantillonne, T=0,1)** | 0,476 | 0,25 % [0,11;0,41] | 2,1 % | 610 |
| **G-copule (T=0,2)** | 0,476 | 0,22 % [0,11;0,36] | 2,0 % | 612 |
| PMM k=10 | 0,475 | 0,23 % [0,06;0,42] | 1,7 % | -- |
| LR contexte argmax (contre-examen) | 0,475 | 0,22 % | 1,8 % | -- |
## 3. Verdict : issue (b), specificite LLM confirmee
Top-1 des deux generateurs individualises (0,22-0,25 %) indiscernable de PMM (0,23 %) et de la
LR argmax deja mesuree (0,22 %), a exactitude quasi identique (0,475-0,476), ~85 fois sous le
jumeau LLM (20,7 %) -- malgre un echantillonnage individualise (jamais l'argmax) et une copule
qui reproduit la dependance entre items. Ni l'argmax ni l'absence de structure de dependance ne
limitaient PMM/B2 : l'ecart tient au generateur lui-meme.
## 4. Consequence pour le titre
Aucun changement : « des jumeaux LLM restent reliables a leurs repondants » reste le bon
cadrage, renforce par ce controle. Limite a ajouter : la cible d'exactitude exacte du jumeau
(0,590) n'a pas ete atteinte (plafond 0,476) ; la comparaison porte sur la meilleure exactitude
atteignable par ces generateurs, pas une exactitude strictement appariee.
## En clair
Meme en tirant au hasard dans ses probabilites plutot qu'en choisissant la reponse la plus
probable, et meme en copiant les liens entre questions, un generateur statistique ne retrouve
presque jamais la bonne personne ; le jumeau LLM, si, dans un cas sur cinq.
