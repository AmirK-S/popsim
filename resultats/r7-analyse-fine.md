# R7, analyse fine descriptive post hoc

## Portée

Cette analyse est exploratoire et postérieure aux résultats R7. Elle ne crée aucun test,
ne modifie aucune famille confirmatoire et n'attribue aucun effet causal à une étape
d'entraînement. Elle lit seulement `r1-par-cellule-r7.csv`,
`r1-par-item-ecarts-r7.csv`, les métadonnées A37 et
`r1-par-item-ecarts-r5.csv`. Les différences de checkpoint sont toujours définies comme
valeur ultérieure moins valeur antérieure.

Parmi les 79 items orientés, 72 ont un écart signé disponible aux quatre checkpoints pour
l'identité journaliste et 76 pour l'adversaire. Les valeurs manquantes par checkpoint sont
respectivement 1, 3, 3 et 4 chez le journaliste, puis 0, 2, 2 et 0 chez l'adversaire. Les
comparaisons R4/R5 reposent sur une intersection unique de 58 items stricts, disponibles
dans les quatre checkpoints R7 et les trois conditions `q4`, `q4nogab` et `q4gab3`.

## Une moyenne faite de mouvements opposés

Chez le journaliste, les moyennes par item des différences SFT moins Base, DPO moins SFT
et Final moins DPO valent -0,008, +0,056 et -0,027. Les médianes sont +0,005, +0,060 et
0,000. Le premier contraste est presque équilibré, avec 50,0 % de différences positives,
45,8 % négatives et 4,2 % nulles. DPO moins SFT est plus cohérent, avec 65,3 % positives,
19,4 % négatives et 15,3 % nulles. Final moins DPO reste partagé, avec 31,9 % positives,
43,1 % négatives et 25,0 % nulles. Les moyennes absolues de 0,129, 0,122 et 0,078 sont
nettement supérieures aux différences signées correspondantes. L'annulation entre items
est donc substantielle, surtout aux première et dernière transitions.

Sur ce même périmètre commun de 72 items, les facteurs descriptifs sont 0,455, 0,422,
0,658 et 0,544. Ils sont proches des valeurs principales calculées sur les périmètres
valides propres, mais DPO est un peu plus élevé ici. Cela illustre l'effet limité mais réel
du choix de périmètre et ne change aucun verdict enregistré.

Chez l'adversaire, SFT moins Base est plus net: moyenne +0,089, médiane +0,103 et 60,5 %
d'items positifs. DPO moins SFT vaut ensuite -0,033 en moyenne, puis Final moins DPO +0,024.
Ces directions diffèrent de celles du journaliste. Au niveau des camps et après orientation,
la première différence adversaire combine surtout un déplacement à droite de +0,147 et un
déplacement à gauche de -0,050. Chez le journaliste, la différence DPO moins SFT combine
+0,097 à droite et +0,036 à gauche; la hausse plus forte à droite produit l'écart signé
positif. Les changements de dispersion et d'erreur TV ont généralement une médiane nulle,
malgré des moyennes absolues non nulles. Aucun déplacement uniforme des trois camps
n'apparaît.

## Hétérogénéité et classement

Les familles ne dessinent pas une trajectoire commune. Les 17 items de dépenses publiques
ont des différences moyennes +0,026, +0,055 et -0,005. Les 7 items d'avortement suivent
-0,220, +0,304 et -0,221. Les 8 items de libertés civiles suivent +0,140, -0,198 et +0,099.
Les familles de deux à cinq items sont publiées dans le CSV mais sont trop petites pour une
lecture autonome.

La polarité de codage sépare aussi les trajectoires journaliste: SFT moins Base vaut
-0,065 sur les 23 items de polarité négative et +0,019 sur les 49 positifs; DPO moins SFT
vaut -0,007 et +0,086. Cette association peut refléter l'ordre des modalités, le contenu
des familles ou leur composition. Elle ne permet pas de choisir une explication. Les items
à deux modalités ont des mouvements absolus plus grands que ceux à trois ou quatre, et le
tertile de consensus humain le plus fort a également les mouvements les plus amples. Ces
strates se recouvrent et aucune analyse ajustée n'était prévue.

Le classement par item est seulement partiellement stable. Chez le journaliste, les
corrélations de Spearman entre checkpoints adjacents valent 0,653, 0,630 et 0,737, mais
Base contre Final tombe à 0,254. Base est le minimum pour 50,0 % des items, tandis que DPO
est le maximum pour 47,2 %. Pourtant, 49 items sur 72, soit 68,1 %, présentent au moins une
inversion de signe entre deux mouvements adjacents. Chez l'adversaire, cette proportion est
71,1 %. Il n'existe donc pas de trajectoire monotone dominante au niveau des items.

## Rejets et valeurs manquantes

Les taux globaux déjà rapportés augmentent de 3,36 % à Base à 6,38 % à SFT, 6,82 % à DPO
et 7,61 % à Final. Le camp explique peu cette progression. Le nombre de modalités explique
beaucoup plus la distribution brute des rejets: aucun sur 1 248 cellules à deux modalités,
0,24 % sur 1 272 cellules à trois, 6,7 % à quatre, 13,6 % à cinq, puis 33,3 %, 52,1 %,
62,5 %, 70,8 % et 87,5 % pour 6, 7, 8, 9 et 12 modalités. Les derniers niveaux ont peu
d'items. Comme les écarts signés exigent les camps gauche et droite valides, l'analyse
complète exclut précisément une partie des cas les plus sujets au rejet. Seulement deux
items journaliste complets ont au moins un rejet dans un autre camp; leur comparaison ne
permet pas d'estimer l'effet des rejets sur la trajectoire.

## Repère d'amplitude R4/R5

Sur les 58 items strictement communs, les moyennes absolues par item des trois mouvements
R7 sont 0,138, 0,129 et 0,087. Le changement de format R4 `q4nogab - q4` vaut 0,204 et
l'ajout des trois exemples sous gabarit R5 `q4gab3 - q4` vaut 0,176. Les mouvements R7
représentent ainsi 43 % à 68 % de l'amplitude absolue du repère R4 et 50 % à 79 % du repère
R5. Avec le même dénominateur humain de 0,2565, les différences signées de facteur sont
-0,066, +0,201 et -0,112 pour R7, contre +0,531 pour R4 et +0,416 pour R5.

Les distributions R4/R5 sont aussi plus larges, mais elles recouvrent fortement celles de
R7. Ce repère compare des modèles et protocoles distincts; il situe une échelle observée et
ne mesure pas la part d'une étape d'entraînement. Le résultat négatif principal demeure:
aucune décomposition par item, camp, famille, polarité, modalités ou consensus ne transforme
la trajectoire moyenne R7 en progression uniforme.

## Sorties

- `r7-analyse-fine-items.csv`: trajectoires, différences, métadonnées et rejets par item;
- `r7-analyse-fine-strates.csv`: distributions par camp, identité et strate;
- `r7-analyse-fine-classements.csv`: stabilité des rangs, minima, maxima et inversions;
- `r7-analyse-fine-comparaison-format.csv`: comparaison sur les 58 items stricts communs;
- `r7-analyse-fine.png` et `r7-analyse-fine.svg`: figure descriptive reproductible;
- `analyses/r7_analyse_fine.py`: génération locale de toutes les sorties numériques.
