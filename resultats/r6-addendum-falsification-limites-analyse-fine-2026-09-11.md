# R6 : critères de falsification et limites de lecture de l’analyse fine

Cet addendum local complète `r6-plan-analyse-fine-prospectif.md` et son erratum du
11 septembre 2026. Il ne modifie aucun appel, donnée, hypothèse, famille, seuil ou verdict
confirmatoire. Il fixe des contraintes de rédaction pour les sorties secondaires et
exploratoires, avant lecture des campagnes.

## Unité qui peut être décrite

Chaque résultat concerne un **couple modèle demandé, fournisseur observé, date,
configuration et passe**. Un écart entre deux lignes ne démontre ni un effet du modèle, ni
un effet du fournisseur, ni un effet de taille, de post-entraînement, de prix ou de date :
ces facteurs ne sont pas randomisés ni séparés dans R6. Un classement est donc un classement
de couples servis sur le masque indiqué, jamais de modèles en général.

Le contraste F2 moins F1 décrit deux conditions d’invite sur l’intersection exacte des 79
items orientés et des cellules valides. Il ne doit pas être appelé effet causal des trois
exemples. L’ordre des passes, l’heure de service, une dérive du fournisseur, des rejets
différentiels ou une configuration/date distincte restent des explications concurrentes.
Toute variation interne du fournisseur, du modèle renvoyé, de la configuration, de la date
enregistrée ou du masque rend ce contraste `NON_INTERPRÉTABLE` comme comparaison de format.

## Confusions de composition à déclarer

La famille d’items, le nombre de modalités et le consensus humain sont souvent liés. Les
strates et leave-out décrivent cette dépendance; ils ne l’ajustent pas et ne démontrent pas
une interaction. Les distances TV et Gini--Simpson dépendent aussi mécaniquement du nombre
de modalités et de la concentration humaine. Une différence globale ne peut donc pas être
attribuée à une famille, à K ou au consensus seul.

Chaque tableau ou figure globale A1, A2, A4 ou F2 moins F1 doit afficher, sur le même masque,
la répartition des items par famille, K, tercile de consensus et rejet. Si une direction
n’apparaît que dans une famille, un K ou un tercile, la conclusion est limitée à cette strate.
Si le retrait d’une famille ou d’un item inverse une phrase narrative, la phrase est retirée
ou explicitement restreinte au reste du masque. Une strate de moins de cinq items demeure
`NON_INTERPRÉTABLE`; elle ne peut être fusionnée a posteriori avec une autre strate.

## Critères qui falsifient une lecture trop forte

| Observation | Formulation interdite ou réduite |
|---|---|
| F2 moins F1 change de signe, disparaît sur le masque commun ou varie avec rejets/date/configuration | « les exemples causent/réparent/amplifient »; décrire seulement le contraste de conditions concerné. |
| Écart concentré dans une famille, un K ou un tercile, ou renversé par leave-one-family-out | Toute généralisation au GSS, aux items politiques ou au modèle. |
| Deux couples convergent mais restent éloignés du référent, ou seulement par proximité accrue à l’uniforme | « accord substantif », « fidélité » ou « validation mutuelle ». |
| A4 ne dépasse pas la variabilité des 40 cellules de plancher, plancher absent, ou pilote/campagne instable | Toute affirmation sur la dépendance à l’identité du demandeur; ne pas moyenner les passes. |
| Fournisseur, modèle renvoyé, configuration, date ou masque diffère dans une comparaison | Toute attribution au modèle, au fournisseur ou au format; conserver seulement les descriptions séparées. |
| Rejets concentrés selon K, famille, camp ou format | Comparaison de moyennes comme si les populations d’items étaient identiques. |

L’absence de ces signaux ne prouve ni absence de confusion ni stabilité. Elle autorise au
plus une description bornée du couple et du masque observés. Les pilotes de dix cellules ne
valident pas une campagne et les quarante cellules de plancher n’estiment pas la variance
complète de A1 ou A2. Ils ne permettent ni sélection de seed, ni changement de fournisseur,
ni moyenne de répétitions après observation.

## Séparation des sorties

H1 à H3 restent exclusivement dans l’évaluateur confirmatoire; H4 reste exploratoire selon
`kmqnw`. Les tableaux fins ne produisent ni p, Holm, seuil décisionnel, équivalence,
causalité ni nouveau verdict. Toute sortie non interprétable ou indisponible est publiée avec
son masque, ses effectifs et sa raison, sans remplacement par une trace pilote ou un sous-
ensemble favorable.
