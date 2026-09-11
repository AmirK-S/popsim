# C5, resultats

Comparateurs forts (preenregistrement section 4) : nul tout a 0 sauf welfare = 4.26 points, nul tout a 0 = 6.99 points.

## gpt-oss-20b (`oss20`)

Trace `/Users/amirkellousidhoum/Desktop/Code/Projets/popsim/data/traces/c5/c5-oss20.jsonl`, 6600 lignes, 0 rejets, taux de parse 1.0000, 300 personas avec au moins un appel.

MAE = **5.71** points, IC95 bootstrap [5.47 ; 6.00].
Taux de fausses alertes (5 paires nulles, seuil 5 points) = **0.40**, IC95 bootstrap [0.40 ; 0.40].

| paire | effet humain | nul ? | effet simule | erreur absolue |
|---|---|---|---|---|
| natspac | 1.89 | oui | -0.63 | 2.52 |
| natenvir | 1.98 | oui | -1.40 | 3.38 |
| natheal | -5.21 | non | -3.42 | 1.79 |
| natcity | -16.83 | non | -8.22 | 8.61 |
| natdrug | -1.56 | oui | 6.23 | 7.79 |
| nateduc | 0.12 | oui | 1.70 | 1.58 |
| natrace | -4.73 | non | -5.35 | 0.62 |
| natarms | 1.35 | oui | 7.18 | 5.83 |
| nataid | -6.22 | non | 1.13 | 7.35 |
| natfare | 31.89 | non | 9.63 | 22.26 |
| natcrime | -5.09 | non | -6.18 | 1.09 |

Prediction welfare : effet simule 9.63 points, bon signe, <= 20 points (predit : bon signe et > 20 points, 95 %).
Prediction big cities : signe correct (effet negatif) dans 3/3 cellules camp x modele (gauche=-9.70, centre=-4.60, droite=-10.35), predit au plus la moitie.

**Verdict (section 6) : ZONE GRISE (aucun des trois criteres de la section 6 n'est rempli exactement).**

## Qwen3-30B-A3B-Instruct-2507 (`q30`)

Trace `/Users/amirkellousidhoum/Desktop/Code/Projets/popsim/data/traces/c5/c5-q30.jsonl`, 6600 lignes, 0 rejets, taux de parse 1.0000, 300 personas avec au moins un appel.

MAE = **4.68** points, IC95 bootstrap [4.49 ; 4.88].
Taux de fausses alertes (5 paires nulles, seuil 5 points) = **0.00**, IC95 bootstrap [0.00 ; 0.00].

| paire | effet humain | nul ? | effet simule | erreur absolue |
|---|---|---|---|---|
| natspac | 1.89 | oui | -0.88 | 2.77 |
| natenvir | 1.98 | oui | -0.52 | 2.50 |
| natheal | -5.21 | non | -2.37 | 2.84 |
| natcity | -16.83 | non | -5.80 | 11.03 |
| natdrug | -1.56 | oui | 1.22 | 2.78 |
| nateduc | 0.12 | oui | -1.25 | 1.37 |
| natrace | -4.73 | non | -6.87 | 2.14 |
| natarms | 1.35 | oui | 1.78 | 0.43 |
| nataid | -6.22 | non | -1.03 | 5.19 |
| natfare | 31.89 | non | 14.83 | 17.06 |
| natcrime | -5.09 | non | -8.42 | 3.33 |

Prediction welfare : effet simule 14.83 points, bon signe, <= 20 points (predit : bon signe et > 20 points, 95 %).
Prediction big cities : signe correct (effet negatif) dans 3/3 cellules camp x modele (gauche=-2.25, centre=-4.65, droite=-10.50), predit au plus la moitie.

**Verdict (section 6) : ABANDON (MAE entre 4,3 et 7,0, au plus une fausse alerte).**

