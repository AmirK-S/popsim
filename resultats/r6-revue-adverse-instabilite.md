# R6 — revue adverse indépendante de l’instabilité DeepSeek

## Périmètre et sources

Cette revue a été faite hors ligne, sans appel API ni nouvelle génération. Elle repart des
vingt lignes des deux traces DeepSeek, du référent humain
`r1-distributions-reelles.csv`, des deux traces du contrôle local chat/completion et du
plan R6. Elle contrôle ensuite `r6-instabilite-pilote-deepseek.csv` et son rapport, sans
reprendre leurs résultats comme données d’entrée.

Les sources DeepSeek sont scellées par les SHA-256 suivants :

- essai 1 : `c9ac4ccbad6e25916949834cc2707a021a0d1dbdc4f4e1911ff8c740034ae8c2` ;
- essai 2 : `874d3a91fd4041d3f58675bcabcbea327061015a710a9f86f6eda854dd327164`.

`GO-R6` est absent, `STOP-R6` est présent et le STOP global est absent. Aucune trace de
campagne R6 n’existe.

## Recalcul indépendant

Les dix cellules sont présentes une fois dans chaque passe. Pour chaque cellule, les
options sont dans le même ordre et les distributions somment à un. Les vingt réponses ont
passé le parse strict; il n’y a ni rejet, ni cellule non jouée, ni incident de transport.

Le CSV reproduit exactement les vingt distributions des traces. Tous ses diagnostics
numériques ont été recalculés : l’écart maximal avec les valeurs publiées à six décimales
est `4,68 × 10⁻⁷`, donc un simple effet d’arrondi.

Les résultats indépendants sont :

| mesure | recalcul |
|---|---:|
| distributions strictement identiques | 1/10 |
| TV moyenne ; médiane ; maximum | 0,053 ; 0,050 ; 0,100 |
| IC bootstrap percentile 95 % de la TV moyenne | [0,033 ; 0,074] |
| déplacement maximal d’au moins 5 points | 6/10 |
| déplacement maximal supérieur à 1 point | 9/10 |
| modes identiques ; modes se recouvrant | 5/10 ; 7/10 |
| classement complet identique | 4/10 |
| médiane de Spearman sur les rangs | 0,955 |
| changement absolu moyen ; maximal de Gini-Simpson | 0,03968 ; 0,14220 |

Le plancher humain vague 1/vague 2, recalculé depuis les modalités et effectifs du référent,
a une TV moyenne de 0,028196, une médiane de 0,030439 et un maximum de 0,048193. La TV
DeepSeek est plus grande dans 8 cellules sur 10; le rapport des moyennes est 1,8797 et la
différence moyenne 0,024804. L’IC exploratoire à 95 % de cette différence est
[0,0040 ; 0,0449]. Le contrôle local chat/completion vaut bien zéro sur les dix cellules.

Les intervalles publiés sont reproductibles avec 2 000 tirages, la graine 20260910,
l’ordre des traces et une initialisation séparée du générateur pour chaque intervalle. La
graine seule ne fixe pas complètement un bootstrap Monte-Carlo si l’ordre des lignes et la
réinitialisation ne sont pas également spécifiés; cela ne change ici ni les arrondis
publiés ni l’interprétation exploratoire.

## Égalité exacte et variation pertinente

Le seuil préenregistré échoue sans ambiguïté : 1 est inférieur à 7. Cette décision porte
sur l’égalité exacte des distributions. Elle ne doit pas être reformulée après observation.

Cette égalité répond correctement à la question étroite « le service reproduit-il au
chiffre près la même distribution à température demandée nulle ? ». Elle ne répond pas à
la question plus scientifique « les conclusions de R6 sont-elles stables ? ». Une paire
peut échouer pour un déplacement d’un point sans conséquence sur un contraste, tandis
qu’un modèle pourrait atteindre 7/10 avec trois déplacements très grands. Les six
déplacements d’au moins cinq points, la TV moyenne presque double du plancher humain et les
changements de mode ou de classement montrent que l’échec observé n’est cependant pas une
simple question de représentation décimale. La médiane de Spearman élevée montre en sens
inverse que l’ordre général reste souvent proche. Les deux constats doivent être publiés.

La règle enregistrée n’ordonne pas l’abandon du modèle. Elle impose l’étiquette « non
déterministe » et conditionne la lecture de A4 au plancher machine de quarante cellules.
Lire l’échec 7/10 comme un retrait automatique serait une nouvelle règle, non enregistrée.

## Stabilité de A1 à A4 et des hypothèses

Le pilote ne permet pas de trancher la robustesse des quantités descriptives DeepSeek :

- **A1** utilise la dispersion décrite rapportée à la dispersion réelle sur l’ensemble
  prévu. Le numérateur Gini-Simpson bouge matériellement sur certaines cellules, mais les
  dix cellules ne forment aucun agrégat A1 complet.
- **A2** exige, pour un même item et une même identité, les camps gauche et droite. Aucune
  paire complète n’est présente dans le pilote. Ni sa valeur ni son signe ne sont testés.
- **A3** n’est pas une quantité enregistrée dans R6.
- **A4** exige les deux identités pour un même couple item-camp. Aucune paire complète
  n’est présente. Le pilote justifie l’application du plancher machine enregistré, sans
  démontrer que celui-ci suffira à stabiliser A4.

Le rapport principal dit que l’effet sur H1 à H4 est indéterminé. Cette phrase doit être
nuancée. DeepSeek est un modèle ouvert descriptif, explicitement hors des cinq modèles
fermés des familles confirmatoires. Son instabilité ne peut donc modifier les décisions
formelles H1–H4. Elle laisse indéterminée la stabilité de sa propre ligne A1/A2/A4 et limite
toute généralisation narrative aux modèles ouverts.

## Options prospectives et estimands

| option | estimand obtenu | coût et condition | jugement adverse |
|---|---|---|---|
| Abandon | aucune quantité DeepSeek | 0 appel, 0 USD supplémentaire | Choix le plus propre sous le gel actuel. Réduit la couverture descriptive, sans modifier H1–H4. |
| Fournisseur déterministe | réponse de DeepSeek chez **un autre fournisseur nommé** | nouveau pilote puis campagne; coût inconnu avant catalogue et mesures | Change le couple modèle-fournisseur, donc l’estimand. Une stabilité chez un autre fournisseur ne répare pas DigitalOcean et exige un cadre prospectif. |
| Seed fixe | réponse conditionnelle à DeepSeek/DigitalOcean et à cette graine | au moins un nouveau pilote; si campagne inchangée, 1 270 futurs appels au total, borne pire cas 1,27 USD | Change la charge et l’estimand. Valide seulement si l’API et DigitalOcean attestent le support et l’application du seed. |
| Moyenne de `R` répétitions | espérance de la distribution du service sous sa stochasticité | coût et appels multipliés approximativement par `R` | Répond le mieux à une cible moyenne, mais abandonne l’estimand « une réponse unique ». Demande un plan d’incertitude entre répétitions. |

Pour `R=3`, le chiffre de 3 670 appels du rapport correspond exactement à
`3 × 1 210 + 40` : trois répétitions des cellules analytiques et une seule répétition du
plancher. Ce décompte n’est cohérent que si le plancher reste celui d’une réponse unique.
Si A4 porte sur des distributions moyennées sur trois répétitions, son bruit de référence
doit porter sur le même estimand : `3 × (1 210 + 40) = 3 750` appels de campagne et
plancher, auxquels s’ajouterait tout nouveau pilote requis. À coût moyen inchangé, 3 750
appels valent environ 0,06168 USD; la borne pire cas est 3,75 USD. Ce sont des projections,
pas des autorisations.

Changer seulement de fournisseur ou ajouter un seed cherche à restaurer une réponse
ponctuelle reproductible. Agréger des répétitions accepte la stochasticité et estime une
réponse moyenne. Ces solutions ne sont donc pas interchangeables.

## Verdict adverse

Il n’y a pas de divergence arithmétique matérielle avec le CSV ou les amplitudes du rapport.
Les divergences d’interprétation sont les suivantes :

1. le seuil 7/10 est valide pour la classification préenregistrée, mais insuffisant pour
   établir la stabilité de A1, A2 ou A4 ;
2. l’échec ne constitue pas, dans le plan, un retrait automatique du modèle ;
3. H1–H4 restent formellement inchangées parce que DeepSeek est hors du périmètre
   confirmatoire, alors que sa ligne descriptive reste non identifiable avec ce pilote ;
4. le coût de l’agrégation doit aligner les répétitions du plancher sur l’estimand moyen,
   faute de quoi le dénominateur de A4 ne mesure pas le même objet.

La campagne ne doit pas partir sous le GO consommé. Toute option autre que l’abandon exige
un choix prospectif explicite sur l’estimand, un nouvel enregistrement et un nouveau budget.
