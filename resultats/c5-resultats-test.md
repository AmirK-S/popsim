# C5, resultats (verification, suffixe test)

**Traces de test, 20 personas exclues de l'echantillon de 300. Aucune conclusion du preenregistrement ne s'applique ici : ce fichier verifie le taux de parse et la grammaire de sortie, pas l'hypothese.**

Comparateurs forts (preenregistrement section 4) : nul tout a 0 sauf welfare = 4.26 points, nul tout a 0 = 6.99 points.

## Llama 3.3 70B Instruct (`llama-70b`)

Trace `data/traces/c5-api/c5-api-llama-70b-test.jsonl`, 220 lignes, 0 rejets, taux de parse 1.0000, 10 personas avec au moins un appel.

MAE = **4.98** points, IC95 bootstrap [3.39 ; 7.34].
Taux de fausses alertes (5 paires nulles, seuil 5 points) = **0.20**, IC95 bootstrap [0.00 ; 0.20].

| paire | effet humain | nul ? | effet simule | erreur absolue |
|---|---|---|---|---|
| natspac | 1.89 | oui | 7.00 | 5.11 |
| natenvir | 1.98 | oui | 0.00 | 1.98 |
| natheal | -5.21 | non | -2.00 | 3.21 |
| natcity | -16.83 | non | -7.00 | 9.83 |
| natdrug | -1.56 | oui | 1.00 | 2.56 |
| nateduc | 0.12 | oui | 0.00 | 0.12 |
| natrace | -4.73 | non | -13.00 | 8.27 |
| natarms | 1.35 | oui | 2.00 | 0.65 |
| nataid | -6.22 | non | 0.00 | 6.22 |
| natfare | 31.89 | non | 24.50 | 7.39 |
| natcrime | -5.09 | non | -14.50 | 9.41 |

Prediction welfare : effet simule 24.50 points, bon signe, > 20 points (predit : bon signe et > 20 points, 95 %).
Prediction big cities : signe correct (effet negatif) dans 2/3 cellules camp x modele (gauche=-7.50, centre=-10.00, droite=0.00), predit au plus la moitie.

**Verdict (section 6) : ABANDON (MAE entre 4,3 et 7,0, au plus une fausse alerte).**

