# C5, preenregistrement : onze paires de formulation du GSS, avant tout appel de modele

Ecrit le 11 septembre 2026, AVANT le moindre appel de modele de cette etude. Aucun
`llama-server` ne tourne au moment ou ce fichier est ecrit. Idee C5 du tri
(`resultats/tri-idees-2026-09-11.md`, section 4, top 1, fusionnee avec B8) : le comite a
deja vu et publie les onze paires et les six effets non nuls avant ce fichier, donc le MAE
mesure ici teste la formulation, pas la decouverte des effets.

## 1. Onze paires, effet humain [MESURE, `GSS_panel2010w123_R6 - stata.dta`, vague 1]

Effet = % « too much » forme historique moins forme `Y`, IC95 sur une difference de deux
proportions. Verification independante du tri : les six chiffres non nuls et les cinq nuls
retrouves au dixieme pres sur la seule vague 1 (N 869 a 1023 par forme).

| paire | effet | IC95 | nul ? |
|---|---|---|---|
| natfare/y (welfare) | +31,9 | ±3,6 | non |
| natcity/y (big cities) | −16,8 | ±4,1 | non |
| nataid/y (foreign aid) | −6,2 | ±4,3 | non |
| natheal/y (health) | −5,2 | ±3,4 | non |
| natcrime/y (crime) | −5,1 | ±2,6 | non |
| natrace/y (race) | −4,7 | ±3,7 | non |
| natenvir/y (environment) | +2,0 | ±2,8 | **oui** |
| natspac/y (space) | +1,9 | ±4,4 | **oui** |
| natarms/y (arms) | +1,4 | ±4,2 | **oui** |
| natdrug/y (drugs) | −1,6 | ±2,9 | **oui** |
| nateduc/y (education) | +0,1 | ±1,9 | **oui** |

## 2. Conception

300 personas, vague 1 du panel GSS 2010, cas complets sur neuf attributs (age, sexe, race,
region, education, statut marital, religion, parti, polviews), stratifies a parts egales
sur le camp derive de `polviews` (1-3 liberal, 4 modere, 5-7 conservateur, regle de
`r1_oracle_camps.CAMP_EN`), graine **20260911**. Persona demographique et de camp seulement,
sans contexte de reponses (a la difference de a5 C3).

22 formes (onze paires x deux formulations) x 2 modeles, gpt-oss-20b et
Qwen3-30B-A3B-Instruct-2507 (cles `oss20`/`q30` de `r1_oracle_camps.MODELES`, gabarits
harmony et qwen-chatml verifies en a3). 300 x 22 x 2 = 13 200 appels. Gabarit de
conversation et grammaire de sortie (`LETTRE: pourcentage`, regex `LIGNE_VALIDE`, tolerance
de somme 95-105) repris de `r1_oracle_camps.py`, appliques a UNE personne au lieu d'un
groupe ; `--sans-relance` (regle de R5). Un appel par forme, jamais les deux d'une paire
dans le meme prompt.

## 3. Mesures

**Primaire** : MAE, en points de « too much », entre effet simule (moyenne des 300 personas
forme historique moins forme `Y`) et effet humain (section 1), moyennee sur les onze
paires. IC par bootstrap sur les personas, 2000 tirages.

**Secondaire** : taux de fausses alertes, part des cinq paires nulles ou l'effet simule
depasse 5 points en valeur absolue, bootstrap par persona pour l'intervalle.

## 4. Comparateur fort

Nul « tout a 0 sauf welfare = 30 » : MAE **4,3** points [MESURE, section 1]. Nul « tout a
0 » : MAE 7,0, cite pour memoire.

## 5. Predictions chiffrees

Le modele ne bat pas 4,3 de MAE (65 %) ; au moins 3 fausses alertes sur 5 (55 %) ; welfare
du bon signe et > 20 points (95 %) ; big cities du bon signe dans au plus la moitie des
cellules modele x camp.

## 6. Critere de succes ou d'echec

« Instrument » si MAE < 4,3 avec IC bootstrap strictement sous 4,3. « Mise en garde » si
MAE > 7,0 ET >= 3 fausses alertes sur 5. Abandon (note d'une page) si le MAE tombe entre
4,3 et 7,0 avec au plus une fausse alerte.
