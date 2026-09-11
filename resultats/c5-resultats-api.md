# C5, resultats

Comparateurs forts (preenregistrement section 4) : nul tout a 0 sauf welfare = 4.26 points, nul tout a 0 = 6.99 points.

## GPT-4o mini (`gpt4o-mini`)

Trace `data/traces/c5-api/c5-api-gpt4o-mini.jsonl`, 6600 lignes, 0 rejets, taux de parse 1.0000, 300 personas avec au moins un appel.

MAE = **6.59** points, IC95 bootstrap [6.28 ; 6.96].
Taux de fausses alertes (5 paires nulles, seuil 5 points) = **0.20**, IC95 bootstrap [0.20 ; 0.20].

| paire | effet humain | nul ? | effet simule | erreur absolue |
|---|---|---|---|---|
| natspac | 1.89 | oui | -0.17 | 2.06 |
| natenvir | 1.98 | oui | -3.45 | 5.43 |
| natheal | -5.21 | non | -4.53 | 0.68 |
| natcity | -16.83 | non | -1.83 | 15.00 |
| natdrug | -1.56 | oui | 0.12 | 1.68 |
| nateduc | 0.12 | oui | -1.47 | 1.59 |
| natrace | -4.73 | non | -4.37 | 0.36 |
| natarms | 1.35 | oui | 8.87 | 7.52 |
| nataid | -6.22 | non | 2.60 | 8.82 |
| natfare | 31.89 | non | 10.88 | 21.01 |
| natcrime | -5.09 | non | -13.47 | 8.38 |

Prediction welfare : effet simule 10.88 points, bon signe, <= 20 points (predit : bon signe et > 20 points, 95 %).
Prediction big cities : signe correct (effet negatif) dans 2/3 cellules camp x modele (gauche=0.60, centre=-1.00, droite=-5.10), predit au plus la moitie.

**Verdict (section 6) : ABANDON (MAE entre 4,3 et 7,0, au plus une fausse alerte).**

## Gemini 2.5 Flash Lite (`gemini-flash-lite`)

Trace `data/traces/c5-api/c5-api-gemini-flash-lite.jsonl`, 6600 lignes, 0 rejets, taux de parse 1.0000, 300 personas avec au moins un appel.

MAE = **4.78** points, IC95 bootstrap [4.52 ; 5.05].
Taux de fausses alertes (5 paires nulles, seuil 5 points) = **0.00**, IC95 bootstrap [0.00 ; 0.00].

| paire | effet humain | nul ? | effet simule | erreur absolue |
|---|---|---|---|---|
| natspac | 1.89 | oui | 1.10 | 0.79 |
| natenvir | 1.98 | oui | 0.68 | 1.30 |
| natheal | -5.21 | non | 2.30 | 7.51 |
| natcity | -16.83 | non | -8.48 | 8.35 |
| natdrug | -1.56 | oui | -0.35 | 1.21 |
| nateduc | 0.12 | oui | -0.03 | 0.15 |
| natrace | -4.73 | non | -16.20 | 11.47 |
| natarms | 1.35 | oui | 2.72 | 1.37 |
| nataid | -6.22 | non | 0.82 | 7.04 |
| natfare | 31.89 | non | 21.63 | 10.26 |
| natcrime | -5.09 | non | -1.95 | 3.14 |

Prediction welfare : effet simule 21.63 points, bon signe, > 20 points (predit : bon signe et > 20 points, 95 %).
Prediction big cities : signe correct (effet negatif) dans 3/3 cellules camp x modele (gauche=-4.20, centre=-7.20, droite=-14.05), predit au plus la moitie.

**Verdict (section 6) : ABANDON (MAE entre 4,3 et 7,0, au plus une fausse alerte).**

## Claude 3 Haiku (`claude-haiku`)

Trace `data/traces/c5-api/c5-api-claude-haiku.jsonl`, 6600 lignes, 0 rejets, taux de parse 1.0000, 300 personas avec au moins un appel.

MAE = **8.32** points, IC95 bootstrap [7.90 ; 8.75].
Taux de fausses alertes (5 paires nulles, seuil 5 points) = **0.40**, IC95 bootstrap [0.20 ; 0.40].

| paire | effet humain | nul ? | effet simule | erreur absolue |
|---|---|---|---|---|
| natspac | 1.89 | oui | 1.43 | 0.46 |
| natenvir | 1.98 | oui | -0.63 | 2.61 |
| natheal | -5.21 | non | -1.57 | 3.64 |
| natcity | -16.83 | non | -9.33 | 7.50 |
| natdrug | -1.56 | oui | 5.27 | 6.83 |
| nateduc | 0.12 | oui | -1.77 | 1.89 |
| natrace | -4.73 | non | -16.53 | 11.80 |
| natarms | 1.35 | oui | 8.23 | 6.88 |
| nataid | -6.22 | non | 26.17 | 32.39 |
| natfare | 31.89 | non | 22.43 | 9.46 |
| natcrime | -5.09 | non | 2.97 | 8.06 |

Prediction welfare : effet simule 22.43 points, bon signe, > 20 points (predit : bon signe et > 20 points, 95 %).
Prediction big cities : signe correct (effet negatif) dans 3/3 cellules camp x modele (gauche=-5.50, centre=-7.90, droite=-14.60), predit au plus la moitie.

**Verdict (section 6) : ZONE GRISE (aucun des trois criteres de la section 6 n'est rempli exactement).**

## Llama 3.3 70B Instruct (`llama-70b`)

Trace `data/traces/c5-api/c5-api-llama-70b.jsonl`, 6600 lignes, 0 rejets, taux de parse 1.0000, 300 personas avec au moins un appel.

MAE = **4.90** points, IC95 bootstrap [4.63 ; 5.20].
Taux de fausses alertes (5 paires nulles, seuil 5 points) = **0.20**, IC95 bootstrap [0.20 ; 0.20].

| paire | effet humain | nul ? | effet simule | erreur absolue |
|---|---|---|---|---|
| natspac | 1.89 | oui | -0.33 | 2.22 |
| natenvir | 1.98 | oui | -0.30 | 2.28 |
| natheal | -5.21 | non | -3.78 | 1.43 |
| natcity | -16.83 | non | -8.20 | 8.63 |
| natdrug | -1.56 | oui | -1.67 | 0.11 |
| nateduc | 0.12 | oui | -1.17 | 1.29 |
| natrace | -4.73 | non | -9.87 | 5.14 |
| natarms | 1.35 | oui | 7.47 | 6.12 |
| nataid | -6.22 | non | 0.12 | 6.34 |
| natfare | 31.89 | non | 18.82 | 13.07 |
| natcrime | -5.09 | non | -12.33 | 7.24 |

Prediction welfare : effet simule 18.82 points, bon signe, <= 20 points (predit : bon signe et > 20 points, 95 %).
Prediction big cities : signe correct (effet negatif) dans 3/3 cellules camp x modele (gauche=-4.85, centre=-7.65, droite=-12.10), predit au plus la moitie.

**Verdict (section 6) : ABANDON (MAE entre 4,3 et 7,0, au plus une fausse alerte).**

