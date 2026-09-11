# Contrôle A1 : résultats

Calculé après `a1-controle-preenregistrement.md`. Script `analyses/a1_controle.py`. VC 5 plis/personne, IC bootstrap personnes × items apparié, 1000 réplicats, graine 20260909. Référence = effets fixes d'item + propension personne (leave-one-item-out).

## Gain d'AUC hors échantillon (référence + désaccord jumeau/passé)

| configuration | AUC référence | gain [IC 95 %] |
|---|---|---|
| Demographics Only | 0,733 | +0,009 [+0,005 ; +0,014] |
| JSON Persona GPT4.1 (max) | 0,733 | +0,020 [+0,013 ; +0,029] |
| 6 autres jumeaux riches | 0,731-0,733 | +0,014 à +0,019, IC bas > 0 partout |

## Verdicts

- Référence seule : AUC 0,731-0,733, bien au-dessus des 0,649 du désaccord seul (`memoire-resultats.md`) : l'essentiel du signal était la volatilité déjà connue.
- « Gain < +0,01 pour les riches » RÉFUTÉE (+0,014 à +0,020) ; « Demographics Only ≈ 0 » à peu près confirmée (+0,009, le plus petit, IC bas quand même > 0).
- Seuil « signal réel » (gain ≥ +0,02, IC bas > 0) : atteint par aucune configuration (maximum +0,0199, juste sous la barre).

**En clair** : la plus grande partie de l'AUC 0,65 était bien du bruit d'item et de personne, pas une vraie connaissance de la personne — mais il reste un petit quelque chose de réel, juste sous le seuil qu'on s'était fixé avant de le croire.
