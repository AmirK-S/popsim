# R6 — plan d’analyse fine prospective

Statut : plan d’analyse secondaire et exploratoire préparé avant la lecture des résultats de campagne R6. Il complète, sans le modifier, le plan autonome R6 et l’addendum prospectif `kmqnw`. Il ne change ni modèle, ni fournisseur, ni invite, ni cellule, ni ordre, ni budget, ni règle d’arrêt, ni famille confirmatoire. Il ne crée aucune hypothèse confirmatoire supplémentaire.

Le mot « prospective » s’applique aux traces de campagne et de plancher encore à analyser. Les pilotes DeepSeek et Grok déjà collectés ne deviennent pas prospectifs par cette page : leurs décisions de déterminisme restent celles, déjà fixées, des deux passes de dix cellules. Toute analyse fine nouvelle de ces pilotes est descriptive rétrospective et ne peut ni les réparer ni autoriser une campagne.

## 1. Périmètre, unités et garde d’entrée

R6 décrit un **couple modèle–fournisseur–date–configuration**, jamais un modèle abstrait, une famille de poids, une application grand public ou un effet causal. L’unité d’inférence existante est l’item ; les cellules d’un même item ne sont pas des réplications indépendantes.

Les seules sources admises sont les traces explicitement nommées dans le manifeste d’analyse R6 et le référent humain déjà scellé. Elles doivent passer le chargeur strict : JSON valide, ordre de cellules exact, absence de doublon, `version_prompt`, format, modèle, configuration, fournisseur, `quantification`, une seule tentative et absence d’erreur cohérents avec le manifeste. Une cellule rejetée reste un rejet ; elle n’est ni imputée, ni remplacée, ni rejouée pour l’analyse.

| Périmètre | Ce qui est possible | Ce qui ne l’est pas |
|---|---|---|
| F1 `q4` | 149 items × trois camps × deux identités : A1, A2, A4, effets de camp et d’identité. | Aucun effet de format isolé. |
| F2 `q4gab3` | 79 items orientés × gauche/droite × deux identités : A2 et contraste apparié F2−F1. | Ni centre sous F2, ni effet F2 au centre. |
| Plancher machine | 40 cellules F1 de campagne et de répétition : TV de service sur le sous-échantillon commun et condition de lecture A4. | Variance de campagne complète de A1 ou A2. |
| Deux passes pilote | Égalité exacte et diagnostics de variation sur les dix cellules prévues. | Une estimation de stabilité de A1, A2, A4 ou d’une campagne entière. |

Avant tout tableau scientifique, publier un tableau de couverture par modèle, format et passe : cellules attendues/observées, rejets, rejets à deux ou trois modalités, cellules appariables, fournisseur observé, date, configuration et statut. Un fournisseur absent, plusieurs fournisseurs dans une même passe, une `quantification` différente du fournisseur, un modèle renvoyé incompatible avec le modèle demandé, ou une configuration qui varie à l’intérieur d’une passe rend le couple **non interprétable** ; il n’est pas moyenné avec un autre fournisseur.

Le taux de rejet et le nombre de modalités doivent être publiés avant tout effet. Le statut annexe « format non tenu » reste celui du plan : moins de 1 % de rejets et aucun rejet à deux ou trois modalités. Ce statut ne redéfinit pas les verdicts confirmatoires, mais interdit de présenter une différence de moyenne comme une différence de comportement lorsque les formats ont sélectionné des sous-ensembles d’items matériellement différents.

## 2. Hiérarchie d’inférence figée

### Primaire confirmatoire — exactement le plan R6

- **H1 / F1** : règle décisionnelle unique, sans p, sur A2 signé chez les cinq fermés, identité journaliste. Les seules conditions sont celles du dépôt : rapport max/min et IC extrêmes disjoints, ou franchissement opposé du plancher 1,009. Aucun classement post hoc ne crée une statistique nulle ou une correction Holm.
- **H2 / F2** : dix tests, cinq fermés × gauche/droite, sur A4 F1. Bootstrap par item et permutation de signe de `TV_identités − 2 × TV_plancher`, 20 000 tirages ; Holm fixe sur dix. La lecture exige aussi le plancher machine établi par le plan.
- **H3a et H3b / F3** : dix tests, cinq fermés × deux seuils, contraste apparié F2−F1 d’A2 signé, journaliste, 79 items orientés. Bootstrap des triplets appariés et permutations de signe centrées respectivement sur 0 et sur +0,30 ; Holm fixe sur les dix tests réunis.

Les règles de masque, les directions annoncées, 2 000 bootstraps, 20 000 permutations et l’estimateur de Phipson–Smyth restent ceux du plan. Une collecte incomplète, un camp constant dans plus de 90 % des items lorsque le plan prévoit le refus, ou une paire requise manquante produit `PARTIEL` ou `REFUS`, jamais une réduction opportuniste de la famille Holm.

### Secondaire enregistré — description sans nouveau test

Pour tout couple modèle–fournisseur effectivement présent, fermé, ouvert ou gratuit, rapporter avec les mêmes métriques R1 :

- **A1** : ratio de Gini–Simpson décrit/réel par camp et identité, F1 ;
- **A2 signé** : ratio de l’écart gauche–droite décrit/réel, par identité, F1 et F2 lorsque les 79 items sont disponibles ;
- **A4** : ratio de la TV entre les deux identités au plancher humain, F1, par camp ;
- TV entre distribution décrite et distribution humaine, et Gini–Simpson décrite, au niveau cellule puis résumées par item.

Les intervalles déjà prévus pour A1, A2 et A4 restent des intervalles bootstrap par item. Hors H1–H3, ils ne reçoivent ni p, ni Holm, ni vocabulaire de significativité. H4 suit l’addendum `kmqnw` : statistique `T = |A2_haut − 1,009| − |A2_bas − 1,009|` et IC bootstrap apparié sur l’intersection d’items des paires prévues, sans p, Holm, verdict ou généralisation tarifaire. Si le modèle haut n’est pas joué ou si l’intersection est insuffisante, H4 est `INDISPONIBLE`, pas négatif.

### Exploratoire planifié — lecture fine, sans promotion

Les analyses suivantes décrivent l’hétérogénéité d’estimateurs déjà définis. Elles ne produisent pas de p, de seuil décisionnel, de Holm, de sélection de modèle ou de nouvelle hypothèse. Toute figure indique « exploratoire », son masque exact et son nombre d’items.

## 3. Analyses exploratoires prévues

### 3.1 Modèle, format, identité, camp et item

Pour chaque modèle–fournisseur :

1. publier la distribution par item de A1, A2 signé, A4, Gini–Simpson décrit et TV au référent, avec moyenne, médiane, quartiles, minimum, maximum et nombre d’items valides ;
2. décomposer A1 par camp × identité ; pour A2, afficher séparément les contributions gauche et droite au même écart signé ;
3. décrire A4 comme une **distance** seulement. Aucun signe ne permet de dire quelle identité déforme davantage le portrait ; le plan R6 exclut une direction de A4 ;
4. pour F2−F1, afficher la différence par item, camp et identité sur l’intersection exacte F1/F2. Le centre est absent de F2 et n’entre jamais dans une analyse de format ;
5. conserver tous les items valides dans un tableau long. Un classement d’items est descriptif ; les ex æquo sont publiés comme tels et ne sont pas attribués au premier item ou modèle dans l’ordre du fichier.

Les comparaisons entre modèles sont toujours désignées « différences entre couples modèle–fournisseur ». Elles ne sont pas des effets de paramètres, de taille, de post-entraînement, de date ou de fournisseur pris isolément.

### 3.2 Hétérogénéité préspécifiée

Chaque quantité de 3.1 est stratifiée, sans modèle ajusté, par :

- famille thématique portée par la trace ;
- polarité A37 pour A2 et F2−F1 ; les items non orientés ne reçoivent pas une polarité inventée ;
- nombre exact de modalités ;
- consensus humain vague 1.

Le consensus humain est `max(p_humain)` : pour A1 et A4, celui du même item et du même camp ; pour A2 et F2−F1, la moyenne des consensus humain gauche et droite. Les terciles sont construits **une seule fois avant lecture des traces de modèle**, sur le périmètre humain complet pertinent à la quantité ; les égalités à une coupure restent dans la même strate et les effectifs réels sont affichés. Il n’y a ni découpage choisi après résultat, ni tertile forcé par un rang qui casserait les égalités.

Une strate avec moins de cinq items valides est affichée comme `NON_INTERPRÉTABLE (n<5)` sans moyenne ni classement. Les familles ou niveaux plus grands restent descriptifs : une hétérogénéité visible n’établit pas une interaction et une absence visible n’établit pas l’uniformité.

### 3.3 Convergence inter-modèles et retour vers l’uniforme

Sur les cellules valides communes à une paire de couples modèle–fournisseur, calculer :

- la TV moyenne entre leurs distributions décrites ;
- la corrélation de rang par item de leurs écarts signés et de leurs Gini–Simpson ;
- l’étendue et l’écart interquartile des A1, A2 et A4 entre modèles, sans transformer ces résumés en test de dispersion intermodèles supplémentaire.

La convergence est présentée avec la proximité au référent humain. Deux modèles peuvent converger parce qu’ils sont tous deux erronés ; une faible TV entre modèles n’est jamais une validation.

Le diagnostic géométrique de « retour vers l’uniforme » est défini, pour chaque cellule valide à `K` modalités, par :

`S_uniforme = TV(p_modèle, uniforme_K) − TV(p_humain_w1, uniforme_K)`.

`S_uniforme < 0` signifie seulement que la sortie modèle est plus proche de l’uniforme que le référent ; `S_uniforme > 0` qu’elle est moins proche. Le résumer par modèle, format, camp, identité, modalités et consensus. Ce diagnostic utilise la TV déjà employée par R1 ; il ne remplace ni A1, ni A2, ni l’erreur TV au référent. Une proximité accrue de l’uniforme n’est pas, à elle seule, une perte de diversité ou une preuve de biais.

### 3.4 Robustesse leave-one-item et leave-one-family-out

Pour chaque estimateur agrégé déjà calculé, réévaluer sa valeur après retrait, à masque fixe :

- de chaque item valide un à un ;
- de chaque famille entière une à une ;
- pour F2−F1, de l’item ou de la famille dans l’intersection F1/F2 seulement.

Publier la valeur complète, l’intervalle des valeurs retirées, le retrait qui produit l’écart absolu maximal et le nombre d’items/familles réellement admissibles. Signaler si le signe de l’estimateur agrégé ou une condition de lecture descriptive change, mais ne réexécuter ni permutations, ni bootstrap décisionnel, ni Holm et ne réviser aucun verdict H1–H3. Si le retrait d’une seule famille renverse une conclusion narrative, la conclusion est limitée à ce périmètre.

### 3.5 Stabilité machine et services DeepSeek/Grok

Pour chaque modèle ayant les deux passes pilote, et séparément pour chaque campagne disposant de ses 40 cellules de plancher, publier :

- nombre de distributions strictement identiques sur les dix cellules pilote ;
- TV moyenne, médiane et maximum par cellule entre passes ;
- changement absolu de Gini–Simpson, modes identiques ou recouvrants et corrélation de rang des modalités, lorsque les modalités sont comparables ;
- pour le plancher de 40 cellules, TV moyenne campagne–plancher sur l’intersection exacte et son rôle dans la lecture de A4.

Ces diagnostics réemploient les quantités déjà utilisées dans la revue d’instabilité DeepSeek. Ils ne sont pas des tests de H1–H4, n’autorisent pas à modifier le seuil exact 7/10 et ne justifient ni moyenne de répétitions, ni seed, ni changement de fournisseur. Ces derniers changeraient l’estimand et exigeraient un addendum distinct. Les dix cellules pilote ne permettent pas une estimation de stabilité de A1, A2 ou A4 ; une campagne DeepSeek ou Grok n’est pas promue au rang de résultat stable par une simple analyse fine.

## 4. Contrôles de provenance et de fournisseur

Le tableau de provenance conserve, sans secret, modèle demandé et renvoyé, fournisseur demandé et observé, date, format, version d’invite, configuration de raisonnement, `max_tokens`, nombre de modalités, passe, taux de rejet, jetons entrée/sortie/raisonnement, coût agrégé et empreinte de configuration. Il distingue les réponses valides, les rejets de parse, les 429 et les incidents ambigus ; un incident n’est jamais traité comme une distribution manquante au hasard.

Contrôles et conséquences :

| Contrôle | Conséquence si échec |
|---|---|
| fournisseur épinglé et observé unique, sans repli | la ligne entière est non interprétable comme ce couple ; aucun regroupement avec un autre fournisseur |
| configuration identique à l’intérieur d’une passe | pas de comparaison entre lignes de la passe affectée |
| mêmes cellules ordonnées et même masque pour chaque contraste | contraste `INDISPONIBLE` ; aucun appariement partiel inventé |
| référent, orientation, effectifs et plancher humain inchangés | évaluation arrêtée par les contrôles bloquants existants |
| raisonner désactivé et jetons de raisonnement tracés | publier l’écart ; ne pas l’attribuer au modèle ou au format sans manipulation |
| F1 et F2 ont des rejets ou des traces de dates distincts | publier les deux masques et dates ; ne pas lire une différence comme effet pur de format |

Le fournisseur n’est pas randomisé et chaque modèle n’a qu’un fournisseur imposé. Les données R6 ne permettent donc pas un effet de fournisseur, un effet de latence, un effet de coût, ni une séparation du service et du modèle. Elles permettent seulement d’exclure les incohérences observables et de décrire les couples effectivement servis.

## 5. Analyses qui peuvent réfuter le cadrage narratif

Cette page sert aussi à empêcher que les graphiques fins confirment mécaniquement l’histoire préférée. Les résultats suivants doivent limiter ou réfuter les formulations correspondantes :

| Observation possible | Conséquence de rédaction |
|---|---|
| H3 n’est pas retenue ou les effets F2−F1 changent de signe entre modèles/familles | abandonner toute formulation générale selon laquelle les trois exemples réparent ou amplifient les écarts hors de Qwen/R5 |
| Une différence de format disparaît sous le masque commun, leave-one-family-out, ou s’accompagne d’un changement majeur de rejet | décrire une sensibilité au protocole, pas un effet de contenu des exemples |
| Les couples modèle–fournisseur convergent entre eux mais restent éloignés du référent, ou convergent seulement parce que `S_uniforme` est négatif | ne pas appeler cette convergence un accord substantif ni une fidélité de population |
| Les classements A1/A2/A4 changent avec le retrait d’un item ou d’une famille | ne pas classer les modèles ; rapporter une dépendance au domaine d’items |
| A4 est sous le bruit machine, le plancher est absent, ou les deux passes varient matériellement | aucune affirmation sur la dépendance au demandeur pour ce couple ; le statut de déterminisme déjà fixé reste inchangé |
| Les effets sont limités aux modalités nombreuses, au consensus extrême ou à une seule polarité | restreindre la portée à cette strate et ne pas l’étendre au GSS entier |
| La provenance révèle un fournisseur, une configuration ou une date non comparable | retirer le contraste causalement ambigu, sans remplacer a posteriori le service |

Une absence de motif dans ces tableaux ne confirme pas une théorie : elle peut refléter un nombre insuffisant d’items, des rejets ou une variation non résolue.

## 6. Multiplicité, puissance et résolution

La correction multiple ne s’applique qu’aux familles déjà fixées : F2 (10 H2) et F3 (10 H3a/H3b), par Holm. H1 n’a pas de p par construction ; H4 et toutes les analyses fines n’ont ni p ni Holm. Il est interdit d’ajouter après lecture des p par famille, polarité, camp, nombre de modalités, consensus, modèle ouvert, fournisseur, leave-out, convergence, uniforme ou stabilité machine.

Le plan R6 ne contient pas de calcul prospectif de puissance ou de différence minimale détectable pour H1–H3. Aucun calcul de puissance post hoc ne sera présenté comme une propriété des données. À la place, chaque sortie porte : nombre d’items valides, nombre de cellules sous-jacentes, nombre de familles/strates, largeur d’IC quand l’IC est déjà prescrit, taux de rejet, taille de l’intersection et raison exacte de toute indisponibilité. Les p confirmatoires ont la résolution Monte-Carlo déjà fixée par 20 000 permutations ; cette résolution ne vaut ni puissance ni précision des explorations.

Une analyse exploratoire est `NON_INTERPRÉTABLE` si son unité d’item manque, si sa strate a moins de cinq items, si les cellules ne peuvent être appariées exactement, si le fournisseur/configuration n’est pas invariant, ou si le diagnostic demandé excède les répétitions disponibles. Un intervalle large, une absence de p ou un résultat non retenu est rapporté comme indécis, jamais comme équivalence, stabilité, absence d’effet ou convergence prouvée.

## 7. Sorties prévues et séparation de publication

Les sorties publiques dérivées, sans traces brutes ni identifiants de compte, sont :

- `r6-analyse-fine-couverture.csv` : masques, rejets, fournisseur, dates et configuration agrégée ;
- `r6-analyse-fine-par-item.csv` : métriques par item et cellule agrégée, avec statut de validité ;
- `r6-analyse-fine-strates.csv` : famille, polarité, modalités, consensus et effectifs ;
- `r6-analyse-fine-intermodeles.csv` : TV et rangs sur intersections communes ;
- `r6-analyse-fine-uniforme.csv` : diagnostic `S_uniforme` ;
- `r6-analyse-fine-leaveout.csv` : robustesse item et famille ;
- `r6-analyse-fine-stabilite.csv` : pilotes et planchers machine ;
- `r6-analyse-fine.md` : texte séparant les résultats confirmatoires, secondaires, exploratoires, indisponibles et non interprétables.

Les tableaux confirmatoires existants restent la seule source des verdicts H1–H3. Le rapport fin y renvoie sans les recalculer, les corriger ou les enrichir. Il pourra dire qu’un mécanisme est compatible avec les données ; il ne pourra jamais substituer une exploration à une hypothèse, transformer une trace de service en preuve sur l’entraînement, ou dépasser la portée du couple modèle–fournisseur documenté.
