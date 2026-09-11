# Consultant externe : angles morts du dossier C7, 12 septembre 2026

Lecture seule du dépôt, aucun calcul, aucun appel. Sources lues : `c7-resultats.md`,
`c7-stanford-resultats.md`, `c7-contre-examen-2026-09-11.md`, `c7-mecanisme-resultats.md`,
`c7-defense-resultats.md`, `c7-preenregistrement.md`, `c7-stanford-preenregistrement.md`,
`c7-echelle-preenregistrement.md`, `c7-compromis-preenregistrement.md`,
`revue-hostile-programme-2026-09-11.md`, `veille-anteriorite-2026-09-11.md`,
`twin-ab-audit-provenance-2026-09-11.md`, verdicts de `b123`, `memoire-long`, `echelle`,
`caricature-profil`, plus `data/osf-t6g7k-stanford/FIGURE2_PIPELINE.md` et
`figure2/.../analysis/individual_level.csv` (lecture de 5 lignes).
`resultats/positionnement-vie-privee-2026-09-12.md` n'existe pas.

Neuf points classés par valeur décroissante, puis la chose à ne pas faire.

---

## 1. Le monde ouvert n'a jamais été testé : le chiffre central n'est pas calibré

**Constat.** Dans `analyses/c7_reidentification.py` (`rangs_attaque`) comme dans
`c7_stanford.py`, la vraie personne est **toujours dans le pool** et le rang est calculé
contre elle. Tout le dossier rapporte un top-1 / top-10 / rang médian. `grep` sur
`precision|faux positif|monde ouvert|seuil|abstention` dans `resultats/c7-*.md` et
`analyses/c7_*.py` ne renvoie rien de pertinent. Il n'existe donc **aucune précision, aucun
taux de faux positifs, aucune règle de décision, aucune abstention**.

**Pourquoi c'est important.** Un attaquant réel ne sait pas si sa cible figure dans le
fichier, et un top-1 de 20,7 % ne dit rien de ce qui arrive quand elle n'y est pas : si le
meilleur score en l'absence de la cible est indiscernable du meilleur score en sa présence,
l'attaque ne « retrouve » personne, elle produit un candidat toujours confiant et faux dans
79 % des cas. C'est la première objection de tout relecteur de PETS, USENIX Security ou
CCS : depuis Carlini et al., une attaque de vie privée se rapporte en TPR à FPR fixé, pas
en exactitude moyenne. Aujourd'hui, le résultat est présenté dans la métrique la plus
flatteuse qui existe, et la plus facile à démonter. C'est, à mon avis, la faiblesse la plus
coûteuse du dossier, devant l'antériorité.

**Test qui tranche.** Refaire l'attaque en retirant la vraie personne du pool (2 057
candidats, cible absente), comparer la **distribution du meilleur score** avec et sans
cible, publier la courbe précision-rappel et le TPR à FPR = 0,1 % et 1 %. Ajouter une règle
d'abstention (écart entre le 1er et le 2e score) et rapporter la précision parmi les
attaques non abstenues. **Coût : quelques heures, local, zéro appel, code existant.**

---

## 2. Le bon comparateur est le plafond humain, et il n'est appliqué nulle part

**Constat.** Le retest humain donne 81,6 % sur Twin (`c7-contre-examen`, §1) et 96,8 % sur
Stanford (`c7-stanford-resultats.md`, §1). Ces deux nombres disent que **60 réponses
sincères sont déjà une quasi-empreinte**, indépendamment de toute IA. Or les rapports
comparent le jumeau au hasard (×425, ×691) et au démographique (×9,7, ×29), jamais au
plafond. Les ratios normalisés sont 20,7/81,6 = **25 %** et 65,7/96,8 = **68 %**. Pire :
`c7-stanford-resultats.md` §4 explique l'écart 20,7 → 65,7 par la taille du pool et la
richesse de l'agent, alors que **les plafonds eux-mêmes diffèrent** (81,6 contre 96,8) et
que le nombre d'items diffère d'un facteur 3 (60 contre 177). La comparaison des deux
chiffres bruts, telle qu'écrite, n'est pas valide.

**Pourquoi c'est important.** Le programme entier repose ailleurs sur la normalisation au
plancher de retest (`t1`, `part_du_plancher_humain`) ; ne pas l'appliquer ici est une
incohérence méthodologique interne qu'un relecteur attentif verra, et qui donne l'impression
d'un choix de métrique opportuniste. La quantité normalisée est aussi la seule comparable
entre les deux jeux, et c'est elle qui porte l'énoncé fort : *le jumeau transmet le quart
(Twin) ou les deux tiers (Stanford) de l'empreinte que la personne porte elle-même.*

**Action.** Rapporter partout le taux normalisé au retest, à côté du taux brut. Publier le
point **k = 60 items** de Stanford, que `analyses/c7_stanford.py` calcule déjà
(`courbe_items_gss`, ligne ~414, imprimé à l'écran, absent du rapport et des CSV) : sans ce
point, la « réplication » n'est pas à information égale. **Coût : une heure, rédaction plus
une réexécution d'un script existant.**

---

## 3. La provenance des agents Stanford n'est pas auditée : la recopie n'est pas exclue

**Constat.** Côté Twin, l'équipe a fait le travail : `twin-ab-audit-provenance-2026-09-11.md`
(exclusion de 3 configurations sur 13, `wave_split` vérifié propre sur 294 personnes) et le
test de symétrie du contre-examen (§2 : sur les cellules où la vague 4 diffère des vagues
1-3, la sortie colle à la vague 4 dans 37,7 % et aux vagues 1-3 dans 37,9 % — pas de copie).
Côté Stanford, **rien d'équivalent**. `FIGURE2_PIPELINE.md` §5 ne documente pas ce qui
alimente `survey_agents_summary.csv` ni `composite_agents_summary.csv` ; aucun audit de
provenance Stanford n'existe dans `resultats/`. Or la condition « enquête » de Park et al.
est, selon toute vraisemblance, conditionnée sur les réponses d'enquête du participant —
possiblement les réponses GSS de vague 1, qui sont exactement la cible de l'attaque.

**Pourquoi c'est important.** Si c'est le cas, les 20,6 % de l'enquête seule et une part du
65,7 % composite ne mesurent pas une empreinte reconstruite mais une **ré-expression bruitée
d'une entrée qui contenait déjà la cible** : tautologique, et fatal pour le résultat le plus
spectaculaire du dossier. Indice rassurant, lu dans
`figure2/data/new_analysis_summaries/gss_filtered/analysis/individual_level.csv` : sur 5
participants, l'exactitude `survey_agents` vaut 0,57 à 0,71 et `composite` 0,66 à 0,77,
contre 0,79 à 0,87 pour le retest humain — loin d'une recopie parfaite. Ce n'est **pas une
preuve** : une recopie dégradée par la génération produirait exactement ce profil. (Détail à
vérifier au passage : ces exactitudes sont des multiples de 1/150 alors que le rapport
annonce **177 items** GSS.)

**Test qui tranche.** Transposer le test de symétrie du contre-examen : sur les items où
vague 1 ≠ vague 2 chez l'humain, l'agent colle-t-il préférentiellement à la vague 1 (celle
qu'il aurait vue) ou est-il symétrique ? Si asymétrie, la condition « enquête » et le
composite sont disqualifiés et le chiffre défendable devient **l'entretien seul, 44,7 %** —
qui reste un excellent résultat, et bien plus intéressant (le texte d'un entretien
oral suffit à identifier). **Coût : une à deux heures, lecture seule, aucun appel.
À faire avant toute soumission ou tout contact externe.**

---

## 4. Le résultat vaut par la spécificité LLM, et ce pilier n'a qu'un seul étage

**Constat.** Le seul énoncé réellement neuf du dossier, une fois Stadler et al. 2022 admis,
est celui du contre-examen §1 : à exactitude comparable (0,47–0,51 contre 0,59), **aucun
prédicteur non LLM ne dépasse 0,3 %** (PMM 0,23 %, B2 0,07 %, LR 0,22 %, donneur k=1
0,13 %) quand le jumeau atteint 20,7 %. Deux ordres de grandeur. Mais ces comparateurs sont
tous des **prédicteurs**, pas des **générateurs de données synthétiques**. Or l'antériorité
invoquée contre vous (Stadler, Giomi) porte sur les synthétiseurs tabulaires.

**Pourquoi c'est important.** Un relecteur hostile dira : « vous comparez un générateur
individualisé à des prédicteurs qui régressent vers la moyenne — évidemment que le premier
identifie. » C'est la réduction la plus probable à « évident », et elle est en partie juste.
Y répondre demande un comparateur de la **même famille fonctionnelle** : un synthétiseur
tabulaire qui produit un enregistrement complet par personne.

**Test qui tranche, et selon moi la meilleure dépense du dossier.** Ajouter un ou deux
synthétiseurs classiques (copule gaussienne conditionnée sur le contexte, synthpop/CART,
CTGAN si le temps le permet) calibrés à la **même exactitude 0,59** sur les 60 items, et
mesurer leur top-1 avec exactement `rangs_attaque`. Trois issues, toutes publiables : ils
identifient autant (le résultat n'est pas propre aux LLM, mais devient un résultat propre à
l'individuation, et il faut le dire) ; ils identifient beaucoup moins (vous tenez
« à utilité égale, un jumeau LLM fuit d'un ordre de grandeur de plus qu'un synthétiseur
classique » — neuf, net, et c'est votre titre) ; ils identifient plus (vous avez un résultat
de méthode sur les synthétiseurs). **Coût : une journée, local, zéro appel.**

---

## 5. La question plus profonde : trois reformulations qui haussent le travail

Le dossier vend un risque de vie privée. La vie privée est ici le **révélateur**, pas
l'objet. La quantité mesurée est la quantité d'information sur un conditionnement qu'une
sortie générée retransmet. Trois reformulations, par ordre de promesse.

**(a) L'identité comme structure de dépendance, pas comme contenu.** C'est déjà dans vos
données et personne ne l'a vu : H3 (`c7-mecanisme-resultats.md`) montre que permuter l'ordre
des 40 réponses d'achat fait tomber le top-1 de **33,1 % à 0,046 %**, sous le plancher du
hasard, et qu'aucun résumé (compte de « oui », oracle inclus, 0,29 %) ne reconstitue le
signal. Et la défense D4 (permutation intra-segment) supprime la fuite en ne détruisant
**que les corrélations entre items** (`c7-defense-resultats.md` : distribution et écarts
entre segments *exactement* préservés, coût 4,4 points sur les seules corrélations).
Autrement dit : **ce qui identifie une personne n'est aucune de ses réponses, c'est la
structure de dépendance entre elles** — et un LLM conditionné transmet cette structure sans
transmettre beaucoup d'exactitude marginale. C'est un énoncé sur ce qu'est une identité dans
un modèle statistique, pas une note de sécurité. *Test :* construire un attaquant qui ne
reçoit **que** la matrice de corrélations intra-personne du jumeau (marges détruites,
copule seule), et un autre qui ne reçoit **que** les marges ; publier les deux top-1. Si
copule seule ≈ 20 % et marges seules ≈ 0 %, l'énoncé est démontré. *Coût : une journée.*

**(b) Prédiction ou ré-expression d'un contexte ? Une frontière mesurable.** Le jumeau
ne prédit pas mieux qu'une baseline (0,59 contre 0,51) mais identifie 100 fois mieux. Cela
signifie que l'information qu'il porte sur la personne **n'est pas dans l'axe de la
prédiction**. La formulation générale : un modèle conditionné définit un canal entre son
contexte et sa sortie, dont la capacité se décompose en une part généralisante (utile,
mesurée par l'exactitude) et une part idiosyncrasique (identifiante, inutile pour prédire).
Le programme a déjà les deux mesures ; il lui manque de les traiter comme les deux
coordonnées d'un même objet. *Test :* les jumeaux régénérés par vos soins (`c7_gen.py`, en
cours) avec le contexte **tronqué** et **permuté entre personnes du même segment** — si le
top-1 s'effondre avec la permutation du contexte à exactitude quasi inchangée, la part
idiosyncrasique est établie comme transmission de contexte, pas comme mémorisation du
modèle. *Coût : déjà engagé cette nuit, à condition d'ajouter le bras « contexte permuté ».*

**(c) Bits d'identité par bit d'utilité, comme grandeur comparable entre méthodes.** Le plan
`c7-compromis-preenregistrement.md` va dans cette direction mais s'arrête à un Spearman sur
12 points, ce qui est faible (12 points, IC large, l'équipe le dit elle-même). La version
forte : convertir le rang en bits (log2 N moins l'entropie du rang, ou l'information mutuelle
empirique entre jumeau et identité) et rapporter **bits d'identité / point d'exactitude**
pour les 12 unités. Une constante donnerait une loi ; une dispersion donnerait une frontière
de Pareto exploitable par un concepteur de panel. C'est la forme qui intéresse un relecteur
de NeurIPS. *Coût : une demi-journée sur les rangs déjà calculés.*

---

## 6. Twin et Stanford ne se répliquent pas : ils se contredisent sur le mécanisme

**Constat.** Sur Twin, **100 % du signal est dans les 40 items d'achat** et les 20 items
d'opinion donnent 0,25 %, soit le hasard (`c7-contre-examen` §3). Sur Stanford, l'objet
identifiant est **du GSS, c'est-à-dire de l'opinion**, à 65,7 %. `c7-stanford-resultats.md`
§4 présente cela comme une « réplication confirmée … un mécanisme de génération différent ».
C'est au mieux imprudent : selon Twin, l'opinion n'identifie pas ; selon Stanford, elle
identifie mieux que tout. Une des deux lectures est fausse, ou le facteur explicatif est le
nombre d'items (20 contre 177), auquel cas le mécanisme « choix d'achat » de C7-mécanisme
n'est pas un mécanisme mais un artefact de taille de bloc.

**Pourquoi c'est important.** C'est une contradiction interne dans le dossier, visible en
lisant deux rapports voisins, et elle attaque le seul récit mécaniste que vous ayez
(`c7-mecanisme-resultats.md`). Un relecteur qui la trouve doute de tout le reste.

**Test qui tranche.** Courbe top-1 selon le **nombre d'items d'opinion**, sur les deux jeux,
à pool de taille égale (sous-échantillonner Stanford à 20, 40, 60, 100, 177 items GSS ;
Twin est bloqué à 20). Si 20 items GSS identifient à ~0,3 % comme les 20 items d'opinion
Twin, tout s'explique par la taille du bloc et le récit devient : *l'identification est une
fonction du nombre d'items catégoriels, quelle que soit leur nature* — plus simple, plus
fort, et cohérent avec H1 rejetée. **Coût : quelques heures, `courbe_items_gss` existe déjà.**

---

## 7. Le modèle de menace est presque circulaire, et l'attaquant partiel n'est pas étudié

**Constat.** Le contre-examen §4 est honnête : l'attaquant doit détenir **les vraies réponses
aux mêmes 40 questions d'achat**. Mais alors il détient déjà la donnée sensible ; ce qu'il
gagne est une liaison, pas une information. Le dossier a deux points de dégradation isolés
(30 items au hasard : 7,6 % ; vagues 1-3 comme cible : 19,1 %) mais aucune courbe.

**Pourquoi c'est important.** C'est ce qui sépare « linkability au sens du G29 » (vrai, connu
depuis Stadler, peu excitant) d'un **risque quantifié** : combien de réponses un adversaire
doit-il détenir, et à quel niveau de bruit, pour que la liaison tienne ? La réponse « 10
items suffisent » change la portée pratique ; la réponse « il en faut 55 » la ferme
honnêtement. Les deux sont publiables ; ne pas savoir ne l'est pas.

**Test qui tranche.** Courbe top-1 selon le nombre d'items détenus par l'attaquant (1, 5, 10,
20, 40, 60, tirages répétés), croisée avec un bruit de recodage (0 %, 10 %, 25 % des réponses
détenues altérées) et avec un décalage temporel (items des vagues 1-3 au lieu de la vague 4).
Trois courbes, une figure. **Coût : une demi-journée, local.**

---

## 8. Fiabilité du chiffre : bruit instrumental non propagé, ex aequo non documentés

**Constat.** (a) Les jumeaux Twin sont des **sorties uniques** d'un service commercial. Le
pilote R6 (`r6-instabilite-pilote-deepseek.md`, cité dans la revue hostile §4) mesure une TV
de 0,053 [0,033 ; 0,074] entre deux passes à température nulle. Rien ne dit que 20,7 % est
reproductible : peut-être qu'une seconde génération du même jumeau désigne une autre
personne. (b) `rangs_attaque` départage les ex aequo par bruit aléatoire sur 20 tirages, sur
des vecteurs de 60 items dont 40 quasi binaires (entropie médiane 0,99 bit,
`c7-mecanisme-resultats.md` H1). La **taille de la classe d'ex aequo au rang 1** n'est
publiée nulle part. Le contre-examen répond partiellement par une espérance exacte (20,69 %
contre 20,68 %), mais sur une seule configuration.

**Pourquoi c'est important.** Le premier point est une question d'un relecteur en une ligne
(« combien de passes ? »), sans réponse aujourd'hui. Le second détermine si le top-1 est une
mesure ou une convention de départage.

**Action.** Deux passes sur les jumeaux régénérés (`c7_gen.py`) : top-1 par passe, et taux
d'accord sur **l'identité désignée** entre passes — c'est la mesure la plus parlante, et elle
manque totalement. Et publier la distribution de la taille des classes d'ex aequo par
configuration. **Coût : le premier est déjà dans le run de cette nuit si l'on ajoute une
seconde passe ; le second, quelques minutes.**

---

## 9. Co-signature Stanford / MIT / Berkeley : non, pas en l'état

Franchement : le dossier n'est pas co-signable aujourd'hui, et l'obstacle n'est pas
scientifique.

1. **Pas de préenregistrement attestable.** La revue hostile §1 établit que le premier commit
public date du 2026-09-09 et que « préenregistré » ne peut être écrit pour les résultats
fondateurs. Les plans C7 sont locaux, sans DOI OSF. Un chercheur senior ne co-signe pas un
papier de sécurité dont les plans ne sont pas horodatés par un tiers.
2. **Aucune réplication externe.** Contre-examen, revue hostile, audit de provenance : tous
produits par le même dispositif d'agents. Cela vaut contrôle interne, pas indépendance.
3. **Aucune notification aux auteurs des données, et c'est le point bloquant.** Park et al.
(2411.10109) ont **restreint l'accès aux réponses individuelles de leurs 1 052 agents pour
raison de vie privée** — le fait est noté dans votre propre contre-examen §5. Vous publiez une
attaque de ré-identification sur ces données. Aucun chercheur de Stanford ne co-signera cela
sans divulgation préalable aux auteurs concernés, et le faire sans les prévenir transformerait
un bon résultat en incident. Idem pour Toubia et al. sur Twin-2K-500.
4. **Pas de cadre éthique écrit.** Pas d'IRB ou d'exemption documentée, pas de politique de
divulgation responsable, pas de déclaration sur ce qui sera publié (les défenses D4 sont un
excellent argument à mettre **dans** cette déclaration : vous apportez le correctif avec
l'attaque).
5. **Pas de comparateur de même famille** (point 4) ni de calibration en monde ouvert
(point 1), les deux exigences standard d'un relecteur de vie privée.

**Ce qui suffirait, à mon estimation :** points 1, 3 et 4 traités, plus un dépôt OSF horodaté
avec DOI, plus une lettre de divulgation aux deux équipes de données envoyée **avant** tout
preprint, plus une réplication du chemin critique par une personne extérieure au dispositif.
C'est deux à trois semaines, pas une nuit. Avec cela, le dossier devient co-signable ; sans
les points 3 et 4, il reste un preprint que personne d'établi ne voudra endosser.

---

## 10. La chose à ne pas faire : extrapoler le taux à un million de personnes

`c7-echelle-preenregistrement.md` §2 prévoit d'ajuster deux modèles ad hoc — loi puissance
`a·N^b` et loi logarithmique `a − b·log(N)` — sur **six points** allant de N = 50 à
N = 2 058, puis d'extrapoler à N = 10 000, 100 000 et **1 000 000**, le document notant
lui-même que le modèle justifié de Rocher, Hendrickx et de Montjoye n'a pas pu être
implémenté.

**Pourquoi c'est une erreur.** Les deux formes retenues divergent qualitativement hors
domaine (une loi puissance et une loi logarithmique ajustées sur les mêmes six points donnent
des prédictions séparées par des ordres de grandeur à 10⁶) ; la validation croisée
« leave-one-out » sur les six points d'ancrage ne teste rien de l'extrapolation, elle teste
l'interpolation. Une extrapolation sur trois ordres de grandeur au-delà du dernier point
mesuré n'a aucune validité, et l'étiquette « indicative » ne protège de rien : c'est
exactement le nombre qui sera repris, cité, et utilisé pour discréditer le reste du dossier.
Le programme a jusqu'ici la vertu rare de ne mesurer que ce qu'il peut mesurer ; ce serait la
première entorse, et sur le résultat le plus visible.

**À la place.** Mesurer plutôt qu'extrapoler : la courbe empirique jusqu'à N = 2 058 est un
résultat suffisant si elle est rapportée en **rapport au démographique** et au plafond retest
plutôt qu'en valeur absolue, et accompagnée de l'argument structurel (un motif de 40 réponses
quasi binaires porte au plus ~40 bits, borne supérieure honnête et calculable sans ajustement).
Si l'échelle importe vraiment, augmenter le pool réel (Stanford et Twin fusionnés, ou pool
enrichi de vecteurs rééchantillonnés) et publier le dernier N **mesuré**.

**Corollaire pratique :** ne pas lancer une nuit de calculs supplémentaire avant d'avoir fait
les points 1 et 3, qui peuvent l'un et l'autre invalider ce qui tourne actuellement.
