# Matrice de revendications après R7, avant R6

Statut : document de rédaction interne, fondé uniquement sur le corpus local déjà lu.
Aucun résultat R6, y compris pilote, trace partielle ou état de queue, ne fonde une
revendication ci-dessous. R6 reste un test prospectif de transport sur des couples
modèle-fournisseur nommés, pas une confirmation anticipée de cette matrice.

La distinction directrice est simple : fidélité de groupe, correspondance à la personne
et utilité pour une décision sont trois cibles différentes. Un bon résultat sur l'une ne
certifie pas les deux autres.

## Comparateur explicite : SimBench et voisins directs

`SimBench` est le voisin le plus large pour la fidélité de simulation : 20 jeux,
45 modèles, TV relative à l'uniforme et dégradation lorsque l'on conditionne sur un
groupe. Il établit déjà que l'alignement et les étiquettes de groupe peuvent dégrader une
simulation. Son score agrège des jeux hétérogènes et ne sépare pas, dans le même dispositif,
dispersion intra-groupe, écart inter-groupes, correspondance à des personnes appariées,
plancher humain de retest et conséquence pour un choix de simulateur.

Les voisins essentiels pour la personne sont Ahn et al., *Item-Mean Surrogates*, qui
montre qu'un LLM prédit peu au-delà de la moyenne de l'item, et Hwang et al., qui montre que
des opinions propres à la personne prédisent mieux que les étiquettes. Xie et al. mesurent
le réalisme statistique sur sept enquêtes et trouvent notamment une entropie LLM plus basse.
*Emulate or Estimate?* et le travail sur les distributions directes montrent déjà que le
mode d'élicitation et le post-entraînement changent le réalisme. Notre place ne peut donc
pas être « découvrir que les LLM échouent », « découvrir que les invites comptent » ou
« inventer la permutation conditionnelle ».

Sources locales de cette comparaison :
`corpus/lecture-complete/01-simulation-individus-populations.md`, lignes L1.02, L1.05,
L1.07, L1.08, L1.10 et L1.14; `resultats/a26-collisions-2608-03044-et-2609-00565.md`;
`resultats/a27-lecture-2607-25292.md`; `resultats/a13-positionnement-contribution.md`.

## Matrice

### 1. Fidélité de groupe : mesurer séparément les objets qui peuvent diverger

| Rubrique | Contenu défendable |
|---|---|
| État de l'art le plus proche | SimBench compare la TV à l'humain, relative à l'uniforme, et l'effet d'un conditionnement de groupe. Xie et al. mesurent distributions, associations et entropie. *Emulate or Estimate?* mesure TV et amplification des écarts de groupes selon le mode et le post-entraînement. |
| Ce que nos preuves ajoutent réellement | Sur les mêmes items, camps et référent humain, le dossier sépare dispersion interne, écart entre camps, erreur de distribution et dépendance au demandeur. Il rapporte ces quantités à un retest humain, plutôt que de les réduire à une précision ou à un score unique. |
| Preuve locale exacte | R1, trois modèles locaux, trouve une sur-dispersion interne dans les 18 cellules, des facteurs d'écart entre camps de 0,245, 0,618 et 1,268, et une variation selon l'identité du demandeur de 2,74 à 4,23 fois le plancher humain : `resultats/r1-resultats.md`, sections 1.1 à 1.5. La réanalyse a13 montre deux conditions à 1 052 personnes et 169 items, séparées par moins de un point d'exactitude mais par un facteur 13,5 sur le terme inter-groupe : `resultats/a13-positionnement-contribution.md`, erratum E1. |
| Risque de surclaim | Ces résultats concernent des modèles, GGUF, invites, GSS, dates et métriques nommés. Ils ne prouvent ni une pathologie universelle des LLM ni que les composantes sont causalement indépendantes. Le résultat a13 est une réanalyse d'un paquet voisin et ses limites documentaires restent les siennes. |
| Test restant | R6 testera seulement le transport descriptif des métriques R1 sur des services et fournisseurs nommés. Pour défendre une mesure générale, il faudrait ensuite une réplication sur une autre enquête avec retest humain et une baseline statistique à information égale. |
| Formulation autorisée | « Une évaluation de population peut rapporter séparément dispersion intra-groupe, écart inter-groupes, erreur au référent et plancher humain; dans nos conditions locales, ces quantités ne donnent pas le même diagnostic. » |
| Formulation interdite | « Notre score mesure la fidélité sociale complète », « les LLM essentialisent toujours les groupes », ou « une bonne exactitude implique une bonne fidélité de groupe ». |

### 2. Correspondance de personne : une structure de groupe ne suffit pas

| Rubrique | Contenu défendable |
|---|---|
| État de l'art le plus proche | Ahn et al. testent directement ce qui dépasse la moyenne de l'item. Hwang et al. montrent que les opinions propres prédisent mieux que les démographies. SimBench évalue groupes et populations, pas l'appariement d'une sortie avec la bonne personne sous permutation conditionnelle. |
| Ce que nos preuves ajoutent réellement | La chute sous réassignation conditionnelle pose un test de correspondance : conserver le segment et les marges, mais échanger les lignes entre personnes. Le nul indépendant par item pose une autre question, celle de la structure de combinaison. Les deux ne sont pas interchangeables. |
| Preuve locale exacte | Sur Twin-2K-500, 2 058 personnes et 108 items, les 13 configurations LLM ont une chute de 42 à 71 % du plancher humain; les témoins aveugles à la personne chutent de 0,05 à 0,10 %, et les 16 contrastes contre `B0 tirage` survivent à Holm : `resultats/t1-mesure-de-personne-twin.md`, réponse en une ligne. Le même rapport montre que les ratios inter/intra sont invariants à cette permutation et que la chute et l'exactitude ne partagent que 28 % de leur variance sur Twin. |
| Risque de surclaim | Une chute sous permutation ne mesure ni une identité psychologique ni une fidélité individuelle complète. Elle dépend des informations reçues, de la segmentation, du masque d'items et du retest. Twin contient peu de conditions explicitement aveugles à la personne; le contraste de classement est donc incomplet. |
| Test restant | Sur un échantillon indépendant, fixer un bloc A pour l'audit et un bloc B, réellement tenu à l'écart, pour la décision. Comparer LLM, PMM et baselines de segment avec la même information. Le score de correspondance doit prédire B au-delà de l'exactitude globale. |
| Formulation autorisée | « La correspondance à la bonne personne peut être testée séparément de la conservation des distributions de groupe; nos témoins montrent que ces deux propriétés répondent à des perturbations différentes. » |
| Formulation interdite | « Les agents LLM effacent les personnes », « la permutation prouve une fidélité individuelle », ou « les seuils Twin sont un standard universel ». |

### 3. Utilité prédictive : la revendication que le dossier ne possède pas encore

| Rubrique | Contenu défendable |
|---|---|
| État de l'art le plus proche | Ahn et al. comparent les LLM à une moyenne d'item. Le travail sur le réalisme statistique et les effets de traitement rappelle qu'un réalisme de distribution ne prédit pas la validité d'usage. SimBench ne fournit pas une validation indépendante montrant qu'un score de fidélité sélectionne le meilleur simulateur pour une tâche individuelle tenue à l'écart. |
| Ce que nos preuves ajoutent réellement | R2 apporte un contre-exemple contrôlé à la promesse commerciale : à information égale et famille d'items retirée, un jumeau de langage ne bat pas les imputations sur les raretés stables. C'est une borne négative utile, pas la validation de notre propre instrument. |
| Preuve locale exacte | Sur 150 personnes, 58 items et 106 cellules rares stables, `C3F gpt-oss-20b` ne dépasse pas le tirage de segment pour le rappel, +0,0315 [−0,0355; +0,1015], Holm 1,0000, et est derrière PMM; sa précision est 0,0542 contre 0,2190 pour PMM : `resultats/r2-resultats.md`, réponse en une ligne et section 2. Le rapport documente aussi les limites de ce régime, dont le biais de position non contrôlé. |
| Risque de surclaim | Ce résultat ne dit pas que tous les panels synthétiques sont inutiles, ni que le signal de correspondance est sans valeur. R2 est un seul régime sévère, avec des unités dépendantes et une question de rareté précise. |
| Test restant | Préenregistrer une validation croisée entre bloc d'audit A et bloc de décision B, une perte commune, une marge d'utilité pratique, les baselines et l'unité de rééchantillonnage. Le gain de B doit être évalué hors des réponses utilisées par la métrique. |
| Formulation autorisée | « Dans un régime sévère et à information égale, notre jumeau de langage ne surpasse pas PMM sur les raretés stables; la valeur prédictive additionnelle d'un score de correspondance reste à démontrer. » |
| Formulation interdite | « Notre métrique choisit déjà le meilleur simulateur », « les jumeaux de langage n'ont aucune utilité », ou « une chute élevée garantit une meilleure prédiction ». |

### 4. Format : l'instrument d'élicitation appartient à l'estimand

| Rubrique | Contenu défendable |
|---|---|
| État de l'art le plus proche | *Emulate or Estimate?* distingue déjà deux modes de production et leurs effets. Le travail sur distribution directe contre individu unique montre aussi une forte dépendance à l'élicitation. SimBench tient l'invite fixe pour comparer les modèles; il ne réalise pas notre décomposition gabarit contre exemples à poids constants. |
| Ce que nos preuves ajoutent réellement | Nous séparons, sur le même GGUF, la contribution d'un gabarit de conversation et celle de trois exemples, avec même référent et mêmes items. L'effet observé ne justifie pas d'attribuer une différence entre configurations aux seuls poids. |
| Preuve locale exacte | R4, `Qwen3-4B-Instruct-2507` inchangé, déplace le facteur d'écart entre camps de 0,245 à 0,727 quand le format change, +0,482 [0,288; 0,675], alors que le contraste socle contre instruit vaut +0,321 [0,134; 0,518] : `resultats/r4-resultats.md`, sections 1.3 et 2.1. R5 attribue +0,382 [0,200; 0,578] de cette marche aux trois exemples et +0,101 [0,017; 0,183] au gabarit, avec λ = 0,79 [0,60; 0,97] : `resultats/r5-resultats.md`, sections 1 et 1.1. |
| Risque de surclaim | Le contraste porte essentiellement sur une famille Qwen et un jeu GSS. Les exemples peuvent ancrer des nombres au lieu d'améliorer une connaissance de population; R5 ne prouve pas une amélioration de la TV globale ou un mécanisme d'apprentissage. Les rejets diffèrent selon conditions, même si les 79 items orientés principaux restent appariés. |
| Test restant | R6 teste seulement le contraste total F2−F1 sur des services nommés; il ne sépare pas gabarit et exemples. Le test décisif futur est factoriel et prospectif: exemples informatifs, quasi uniformes et asymétrie inversée, à longueur et structure égales, sur une seconde famille. |
| Formulation autorisée | « Dans une comparaison à poids constants, trois exemples déplacent substantiellement le contraste de groupe; une évaluation reproductible doit versionner l'invite et ses exemples. » |
| Formulation interdite | « Les exemples réparent la fidélité », « le mode assistant est sans effet en général », ou « les poids n'importent pas ». |

### 5. Checkpoints et entraînement : une limite, pas un mécanisme causal

| Rubrique | Contenu défendable |
|---|---|
| État de l'art le plus proche | SimBench compare 13 paires base-instruct et relie l'alignement à l'entropie. *Emulate or Estimate?* compare aussi base et post-entraîné. Ces travaux occupent déjà le terrain d'une opposition générale base contre instruct. |
| Ce que nos preuves ajoutent réellement | R7 rend visible une limite opérationnelle : quatre checkpoints sous invite commune peuvent différer sans que leur filiation permette d'attribuer une différence à SFT, DPO ou à une étape finale. Le résultat utile est une discipline d'attribution, non une trajectoire découverte. |
| Preuve locale exacte | R7 exécute 25 tests sur 3 576 cellules. Les quatre critères de trajectoire H1–H4 ne sont pas satisfaits; Base, SFT, DPO et Final restent sous 1 sur leur périmètre valide. Le rapport interdit toute causalité de SFT, DPO ou de l'étape finale faute de lineage établi : `resultats/r7-resultats.md`, portée et tableau principal; `resultats/r7-revue-adverse.md`. |
| Risque de surclaim | Des critères non satisfaits ne démontrent ni absence de différence ni équivalence. Les checkpoints ne constituent pas une intervention randomisée ni une filiation démontrée. |
| Test restant | Vérifier une chaîne de filiation et fixer, avant lecture, des paires adjacentes, l'impact attendu et un effectif capable de distinguer une différence utile. |
| Formulation autorisée | « Sous une invite commune, nous ne trouvons pas de trajectoire confirmatoire préenregistrée et nous n'attribuons pas les écarts aux étapes d'entraînement. » |
| Formulation interdite | « SFT/DPO ne changent rien », « l'alignement cause l'écrasement », ou « R7 réfute SimBench ». |

## Hiérarchie de papier recommandée

Le papier le plus défendable aujourd'hui est méthodologique : les benchmarks doivent publier
ensemble fidélité de groupe, correspondance conditionnelle à la personne, références humaines
de retest et une validation d'usage indépendante. R1, R4, R5 et R7 illustrent pourquoi
l'instrument et la version d'invite doivent être scellés. R2 borne négativement une promesse
d'utilité, mais ne valide pas le score de correspondance. R6 pourra être une réplication de
service et de format seulement après sa campagne complète et selon son plan déposé.

Le résumé ne doit jamais annoncer une supériorité de méthode ou une utilité prédictive avant
le test A-vers-B. Il peut annoncer une distinction de mesures, ses contre-exemples et les
conditions qui rendraient une recommandation pratique justifiable.
