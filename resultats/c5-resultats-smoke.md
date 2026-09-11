# C5, resultats (verification, suffixe smoke)

**Traces de test, 20 personas exclues de l'echantillon de 300. Aucune conclusion du preenregistrement ne s'applique ici : ce fichier verifie le taux de parse et la grammaire de sortie, pas l'hypothese.**

Comparateurs forts (preenregistrement section 4) : nul tout a 0 sauf welfare = 4.26 points, nul tout a 0 = 6.99 points.

## gpt-oss-20b (`oss20`)

Trace `/Users/amirkellousidhoum/Desktop/Code/Projets/popsim/data/traces/c5/c5-oss20-smoke.jsonl`, 440 lignes, 0 rejets, taux de parse 1.0000, 20 personas avec au moins un appel.

MAE = **6.52** points, IC95 bootstrap [5.70 ; 7.63].
Taux de fausses alertes (5 paires nulles, seuil 5 points) = **0.40**, IC95 bootstrap [0.20 ; 0.40].

| paire | effet humain | nul ? | effet simule | erreur absolue |
|---|---|---|---|---|
| natspac | 1.89 | oui | 0.00 | 1.89 |
| natenvir | 1.98 | oui | -1.75 | 3.73 |
| natheal | -5.21 | non | -2.25 | 2.96 |
| natcity | -16.83 | non | -7.50 | 9.33 |
| natdrug | -1.56 | oui | 6.50 | 8.06 |
| nateduc | 0.12 | oui | 1.00 | 0.88 |
| natrace | -4.73 | non | -2.75 | 1.98 |
| natarms | 1.35 | oui | 8.00 | 6.65 |
| nataid | -6.22 | non | 3.00 | 9.22 |
| natfare | 31.89 | non | 7.50 | 24.39 |
| natcrime | -5.09 | non | -7.75 | 2.66 |

Prediction welfare : effet simule 7.50 points, bon signe, <= 20 points (predit : bon signe et > 20 points, 95 %).
Prediction big cities : signe correct (effet negatif) dans 3/3 cellules camp x modele (gauche=-12.86, centre=-5.71, droite=-3.33), predit au plus la moitie.

**Verdict (section 6) : ZONE GRISE (aucun des trois criteres de la section 6 n'est rempli exactement).**

