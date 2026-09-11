# Résultats : loi d'échelle plate (petit contre grand modèle, Twin-2K-500)
Calcul : `analyses/echelle_twin.py`, réutilise `t1_commun`/`t1_mesures` ; préenregistrement
`echelle-preenregistrement.md`. Écart déclaré : corrélation ordinale bootstrappée à 300
répliques, pas 1 000 (temps de calcul ; percentiles stables au delà de 100). Paire
`JSON Persona - GPT4.1` / `GPT4.1-mini`, périmètre commun 1 000 personnes (pid 1-1000),
segmentation `S_gra`.
| mesure | GPT4.1 | GPT4.1-mini | plancher humain |
|---|---|---|---|
| exactitude, IC 95 % | 0,568 [0,563;0,573] | 0,544 [0,539;0,549] | 0,706 |
| correspondance / plancher | 0,702 | 0,677 | 1,000 |
| corrélation ordinale, IC | 0,211 [0,121;0,290] | 0,205 [0,123;0,298] | 0,497 [0,434;0,555] |
Exactitude : **+2,4 points** pour le grand modèle, IC disjoints — prédiction confirmée.
Correspondance normalisée : **+3,7 % relatif** ; corrélation ordinale : **+2,7 % relatif**,
IC quasi identiques. Les deux sous le seuil de 10 % préenregistré : loi plate confirmée.
**Verdict.** Le grand modèle gagne en exactitude agrégée sans gain proportionnel de
fidélité à la personne : correspondance et corrélation restent loin du plancher humain
(0,70 et 0,50 de celui-ci), quasi inchangées entre les deux tailles.
**En clair** : un modèle plus gros récite mieux le groupe, pas mieux la personne précise.
Gemini-Flash2.5 (autre famille, prompt `Text Persona`, hors paire de taille) :
correspondance 0,698 contre 0,623 pour son homologue GPT4.1-mini, exactitude comparable —
compatible avec l'idée, hors test formel (`echelle-gemini-a-part.csv`).
**Limite** : une seule paire, une seule famille, périmètre restreint à 1 000 personnes ;
ne généralise pas au delà de gpt-4.1.
