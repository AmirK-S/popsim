# État des lieux au 13 septembre 2026 : ce que la nuit a retiré, gagné, et laissé en suspens

statut: courant
mandat: donner à un lecteur pressé la vue d'ensemble qui manque — ce qui a été retiré cette nuit et pourquoi, ce qui a été gagné, ce qui reste sous vérification, et l'ordre de fusion des branches non fusionnées avec les conflits attendus
agent: Claude Opus 5, Anthropic
ecriture: resultats/article-synthese.md, resultats/etat-des-lieux-2026-09-13.md
lecture_seule: tout le reste du dépôt ; `article/manuscrit.md` appartient à un autre agent et n'est ni lu pour écriture ni modifié
interdits: appel payant, réseau, recherche web, arrière-plan, nouveau calcul, commit sur master, fusion de branche, écriture dans article/manuscrit.md
cout_reel_usd: 0.00

Document de consolidation. **Aucun calcul n'a été relancé** : tout chiffre cité ici est lu
dans un CSV nommé, sur une branche nommée. Quand un rapport et son CSV divergent, le CSV
fait foi et la divergence est signalée. Quand une valeur n'a pas de source opposable, elle
est écrite `ABSENT`.

---

## 1. En dix lignes

La nuit du 12 au 13 septembre a produit **douze branches non fusionnées**, dont onze portent
des résultats. Elle a **retiré ou requalifié cinq choses** (la comparaison à la
confidentialité différentielle, le facteur chiffré entre époques, le « coût nul » de la
défense D4, la lecture « la fuite suit la prédictibilité », et le gain dit « items banals »),
**durci quatre choses** (le nul de marge passe au nombre de réplicats préenregistré, la
spécificité LLM est démontrée à information d'entrée égale, le modèle de menace résiste à un
attaquant dégradé, les témoins de relecture sont exacts), et **ouvert une question neuve**
(le risque est binaire et très inégalement réparti : médiane nulle, **79,8 %** des personnes
sous 1 %, **18,3 %** au-dessus de 90 %, Gini **0,816 [0,799 ; 0,832]**, le décile le plus
exposé portant **54,4 % [49,6 ; 60,3]** des identifications — `c7-equite-risque.csv`,
bassin 2 058 ; les trois premiers de ces chiffres **n'ont aucun IC** au CSV).

**Le décompte honnête des réfutations passe de QUATORZE à TREIZE** : dix-sept lignes au
tableau, **treize réfutées, deux non concluantes, une non testable, une retirée**.

**Le point le plus risqué qui reste est la fusion**, et il n'est pas difficile : un seul
conflit réel, un seul blocage de porte, une seule branche à abandonner. Le détail est en §5.

---

## 2. Ce qui a été RETIRÉ cette nuit, et pourquoi

### 2.1 La comparaison à la confidentialité différentielle — retirée en entier

**Branches** : `agent/audit/comparaison-dp` (l'audit qui fait foi) et
`agent/correction/retractation-dp` (qui pose la rétractation).

`resultats/c7-dp-resultats.md` porte désormais `statut: retracte_par:` et
`fait_foi: resultats/audit-comparaison-dp-2026-09-13.md`. Le marqueur canonique est posé
ligne 11 de `resultats/retractation-dp-d4-2026-09-13.md`, et l'en-tête de l'audité est posé
dans le même commit : la porte P4 passe.

**Motif, et il est sévère** : le générateur DP était ajusté sur les **humains** et noté
contre le **jumeau** — deux objets désappariés mis sur la même colonne. Et le témoin
`eps = infini`, **présent dans le CSV livré**, disait déjà que le coût était le même **sans
aucune confidentialité**. Personne ne l'avait lu. La formulation retirée, mot pour mot :
« D4 domine la DP composante par composante à protection egale ou supérieure ».

**Conséquence sur le compteur** : la ligne 14 du tableau des prédictions (« à budget modéré,
la DP est dominée par notre défense sur le tableau agrégé ») **sort des réfutations** et
devient **retirée, non tranchée**. C'est la seule ligne du tableau que la nuit déplace.

### 2.2 Le « coût nul » de D4 — c'était la fuite, pas une utilité préservée

Le résultat le plus dur de la nuit. Les deux composantes à **0,0 point** de D4 (distribution
par item, écarts entre groupes) n'étaient pas un coût évité : elles sont la **republication
exacte** de la statistique. La permutation intra-segment conserve le multiensemble
intra-segment à l'identique : **1 560 / 1 560 couples segment × item**
(`resultats/c7-d4-adaptatif.csv`, branche `agent/correction/retractation-dp` ; registre,
ligne `defense-d4-republication-multiensemble`, valeur 100,0, IC `ABSENT`, « SANS OBJET —
egalite exacte de vecteurs tries »).

La ligne de registre `defense-d4-cout-groupes` (valeur 0,0) passe à **`statut: retracte`**.

**Deux réserves que le dépôt pose lui-même et qu'il ne faut pas perdre** :
- la reconstitution des 40 réponses par un adversaire connaissant les autres membres du
  segment est vraie **par construction, pas par mesure** — elle n'a pas été mise en œuvre ;
- sans connaissance latérale, la fuite directement lisible est **207 cellules sur 82 280
  (0,25 %)**, touchant **0,8 % des personnes**. Le rapport **interdit** de présenter ce
  second chiffre comme « la fuite de D4 ».

**Et sur les items d'opinion, D4 ne protège rien** : jumeau défendu **0,245 %
[0,073 ; 0,471]** contre jumeau **non protégé 0,260 % [0,080 ; 0,484]**
(`c7-d4-adaptatif.csv`, filtre `colonnes_attaquees = "20 items d'opinion"`, n = 2 058). Le
résidu n'est pas un résidu de la défense : c'est la part de la publication que la défense ne
touche jamais.

**Le taux de tête de D4 à publier est 0,29 % [0,10 ; 0,53]** (attaquant adaptatif S1,
`resultats/c7-attaquant-fort.csv`), **pas** 0,13 % (attaque naïve, non adaptative) ni 0,05 %
(stratégie S3 seule, la plus faible des trois, à ne jamais citer seule).

### 2.3 Le facteur 10× entre époques — il n'existe pas

**Branche** : `agent/mesures/residu-trajectoire` (fait foi :
`resultats/c7-residu-trajectoire.csv`).

Selon le critère d'appariement, le résidu vaut **entre 1,3× et 11,4×**. Le dénominateur — le
bout 2023 — **échoue son propre contrôle d'interprétabilité et n'est pas estimable** : son
rapport à la baseline erre entre **2,29 et 3,65** sur des sous-bassins de son propre pool,
là où le bout Twin est stable à ±20 %.

**Interdiction, citée mot pour mot depuis le §10 du rapport** : « toute formulation portant
un facteur chiffré entre les deux époques — “150×”, “15×”, “10×”, et **y compris le 2,5×
mesuré ici** ». La clause générale couvre aussi le 11,4× et le 1,3×.

**Ce qui survit** : à information **effective** appariée (4,3 items indépendants de part et
d'autre, même bassin, même attaque, même convention d'ex aequo), les jumeaux de 2025
dépassent leur propre baseline démographique — **0,34 % [0,29 ; 0,40] contre 0,13 %
[0,11 ; 0,16]**, IC disjoints — et aucun des jumeaux de 2023 ne dépasse la sienne. On
rapporte **une direction, pas une magnitude**. La formulation autorisée intégrale est en §7
de la synthèse.

### 2.4 « La fuite suit la prédictibilité, non la rareté » — à affaiblir et renommer, PAS à supprimer

**Branches** : `agent/mesures/equite-risque` (qui propose la phrase) et
`agent/audit/predictibilite` (qui l'attaque).

**Correction importante par rapport à la consigne reçue.** L'audit ne demande **pas** le
retrait du résultat. Il écrit, mot pour mot (§7) : « **l'affirmation ne doit pas être
retirée, elle doit être affaiblie et renommée.** » Et (§1) : « **La moitié “rareté” tient, et
tient au test le plus dangereux.** »

- **La moitié « prédictibilité » est en grande partie tautologique** — « en grande partie »,
  pas « tautologique » tout court. Un attaquant qui **jette le jumeau** et prend les réponses
  passées de la personne atteint **81,589 %** (`c7-audit-predictibilite.csv`, bloc
  `2 temoin trivial`) — **sans aucun intervalle**, le CSV n'en porte pas. Une fois cette
  exposition triviale tenue constante, le jumeau n'ajoute qu'une **corrélation de Spearman
  partielle de +0,107 [+0,063 ; +0,147]**, contre +0,256 en brut. Mais **l'IC exclut zéro** :
  le tiers restant est réel, petit, et **pas** une tautologie.
- **La moitié « rareté » tient, et c'est le pari central de l'auditeur qui est réfuté.** Sa
  prédiction P6 (le signe s'inverserait sous un attaquant pondéré par la rareté) est
  **réfutée** : le corrélat reste négatif, **−0,185 [−0,228 ; −0,138]** sous A-LLR contre
  −0,181 sous Hamming, et **plus fort encore sur la rareté moyenne, −0,237
  [−0,275 ; −0,198]**.

**Ce qu'il faut donc vraiment faire** : empêcher la phrase de partir au manuscrit **telle
quelle**. Elle n'existe nulle part sur `origin/master` ni dans `article/manuscrit.md` — elle
vit dans deux lignes du rapport `c7-equite-risque-resultats.md` (l. 117 et l. 228, cette
dernière étant le bloc « la phrase que l'article peut écrire »). **Il n'y a donc rien à
rétracter : il y a une phrase à ne pas publier.**

### 2.5 Le gain dit « items banals » — requalifié, et trois formulations interdites

**Branches** : `agent/mesures/attaquant-imparfait` (qui produit le résultat) et
`agent/audit/items-banals` (qui l'attaque).

**Verdict de l'audit, mot pour mot** : « **À affaiblir et à reformuler. Ni publiable tel
quel, ni à retirer.** »

Ce que mesure vraiment le gain : **le nombre de modalités**, pas la banalité. Les 60 items se
répartissent en **41 items à 2 modalités**, 1 à 4, 10 à 5 et 8 à 7 ; les « 45 items les plus
banals » sont les 41 binaires plus quatre autres, et les 40 premiers sont **40 des
41 binaires**. Le balayage donne un **pic à k = 40** (**36,4 % [33,5 ; 39,2]**) et redescend
à **25,2 % [22,6 ; 27,9]** à k = 60.

**Et la baseline monte plus que nous.** Le multiplicateur imputable au jumeau **tombe de
×9,9 à ×6,0** : sur les 60 items, 20,61 % contre une baseline démographique de 2,089 %
(rapport 9,865) ; sur les 45 items à plus basse entropie, 30,24 % contre **5,073 %**
(rapport 5,962). Le contraste en **écart absolu** va pourtant en sens inverse (18,5 pts
→ 25,2 pts) : les deux lectures doivent être données ensemble.

**Interdits, cités intégralement depuis le §8 de l'audit** :

> Interdit à l'article : le mot « banals » ou « ordinaires » pour désigner ces items ; le
> chiffre « 30,25 % sur 45 items » présenté sans le balayage complet et sans sa baseline ;
> et toute phrase du type « une base commerciale ordinaire suffit », que rien ici n'établit
> — ce qui est testé est une propriété du **questionnaire Twin**, pas de ce que détient une
> base commerciale.

**Conflit direct entre deux branches, et rien ne le bloque mécaniquement.** La §7 de
`c7-attaquant-imparfait-resultats.md` — la phrase que cette branche demande à l'article
d'écrire — emploie **simultanément les trois formulations interdites**, sans balayage, sans
baseline et sans le multiplicateur ×6,0. **Aucun marqueur de rétractation n'est posé** sur ce
fichier : la porte ne verra rien, et rien n'empêche cette §7 d'atteindre le manuscrit. C'est
le risque le plus concret de la fusion (voir §5.5).

---

## 3. Ce qui a été GAGNÉ

### 3.1 Le nul de marge passe au nombre de réplicats préenregistré

`agent/correction/t1b-cent-replicats`. Le rho nul à marge appariée passe de **0,974**
(20 réplicats, run publié) à **0,9798947065** aux **100 réplicats que le préenregistrement
prescrivait**, bande **[0,9510489510 ; 0,9930069930]**, contre **0,9650** observé.
**Conclusion inchangée** : l'observé reste dans la bande, `rho_reel_depasse_centile95` =
`false`.

**Nature des bornes** : ce sont des **centiles 5-95 d'une loi nulle simulée, PAS un IC**. Le
CSV l'outille lui-même en colonne dédiée (`nature_des_bornes`). **Collision de graphie à
surveiller** : 0,993 est à la fois le 95ᵉ centile de la loi nulle et la borne haute du
bootstrap de l'observé — deux objets, même chiffre à trois décimales.

### 3.2 La spécificité LLM, enfin démontrée à information d'entrée égale

**Branche non prévue au mandat de consolidation, et c'est le gain le plus important de la
nuit** : `agent/audit/comparateur-conditionne` a **atterri**. C'est la vérification qui était
annoncée « en cours ».

La réserve était fondée sur sa prémisse : les générateurs classiques ne voyaient que le
segment démographique, le jumeau voyait la personne. L'audit reconstruit donc quatre
générateurs classiques sur **exactement la même entrée** (les 634 colonnes des vagues 1-3
dont la persona est faite ; 550 informatives), même bassin (2 058 / 2 058), mêmes 60 items,
attaque importée sans réimplémentation.

**Issue (a) : la spécificité tient.** Le meilleur comparateur équitable atteint **0,45 %
[0,20 ; 0,76]** contre **20,66 % [19,01 ; 22,25]** pour le jumeau — un facteur 45, IC
disjoints, loin des 5 % du critère de réfutation préenregistré.

**Et le résultat qui tranche n'était pas prévu** : le jumeau LLM **Demographics Only**, qui
n'a **jamais vu l'individu**, atteint **2,15 % [1,57 ; 2,77]**, soit **4,8 fois** le meilleur
générateur classique **nourri de la persona complète**. On peut retirer toute l'information
individuelle au LLM et il domine encore. **L'écart n'est donc pas imputable à l'entrée.**

**Mais la réserve change de nature, elle ne disparaît pas** — et c'est à porter dans
l'article : **la totalité de l'écart vit dans les 40 items d'achat**. Sur les 20 items
d'heuristiques et biais, le jumeau (**0,25 % [0,08 ; 0,47]**) est **en dessous** du
comparateur classique équitable (**0,51 % [0,26 ; 0,77]**). Sur ce bloc, le jumeau **dégrade**
l'information qu'on lui donne.

**Et un cadrage est cassé au passage** : rapporter 20,7 % aux 81,6 % de l'attaquant
« réponses passées » donne 25,3 %, mais **ce n'est pas une fraction** — numérateur et
dénominateur ne portent pas sur la même entrée, les items attaqués étant **absents** de la
persona. Rapportée au plafond estimable de sa propre entrée (0,45 %), la part « transmise »
vaudrait **4 600 %**. La lecture juste est inverse : **le jumeau LLM fixe la borne inférieure
du contenu identifiant de la persona**, et aucune méthode classique testée n'en récupère plus
de 0,45 %.

**Ce que `agent/mesures/controle-generateur` établit par ailleurs, et qui tient** : aucun des
quatre générateurs classiques ne dépasse **0,1535 % [0,0894 ; 0,2255]** sur Twin (G1,
marginales par segment) ni **2,266 % [1,844 ; 2,711]** sur GSS, contre **20,739 %
[18,989 ; 22,468]** et **65,551 % [62,662 ; 68,308]** pour les jumeaux LLM — soit des facteurs
**135×** et **29×**. Attention, la phrase à publier de ce rapport écrit « 0,15 % » : **c'est
faux**, la valeur est 0,1535 % et la borne est franchie dans le sens qui arrange (voir §6).

**Une nuance que la consigne de consolidation avait perdue** : « le jumeau tombe exactement
sur la courbe d'un copieur de même exactitude » n'est vrai que **sur Twin**. L'écart 0,006
est la différence entre deux réglages d'un copieur bruité G4(ε), l'un calibré sur la fuite
(ε* = 0,714076), l'autre sur l'exactitude (ε* = 0,719728) — tolérance préenregistrée ±0,10.
Sur **GSS, cet écart vaut 0,165** et le verdict du CSV est l'inverse : « GENERALISE : fuit
**MOINS** qu'un copieur de meme exactitude ». « La fidélité est la fuite » est donc un
constat **propre à Twin**, pas une loi des deux jeux.

### 3.3 Le modèle de menace tient sous attaquant dégradé — mais l'ampleur chute

`agent/mesures/attaquant-imparfait`. Il faut descendre à **6 items sur 60** pour que
l'attaque cesse de battre la démographie : à ce point, **0,3466 % [0,2332 ; 0,4862]** contre
une baseline **recalculée dans la condition dégradée elle-même** de **0,1620 %
[0,0777 ; 0,2915]**, ratio 2,14 — les IC se touchent, `au_dessus_baseline` passe à `False`.
L'attaque résiste à **30 % de réponses fausses** (1,341 % [0,855 ; 1,798] contre 0,308 %,
ratio 4,36, aucune rupture).

**Mais l'ampleur chute**, et il faut le dire avec la configuration exacte : le **3,2 %** est
**3,252 % [2,643 ; 4,023]**, obtenu à **moitié d'items (30 sur 60) ET 10 % de réponses
fausses combinés** — pas l'un ou l'autre. Contre 20,573 % non dégradé, c'est un **facteur
6,3**, soit une personne sur trente et une. Le rapport conclut lui-même : « **la menace est
robuste en nature, fragile en ampleur** », et déclare **6 prédictions réfutées sur 8**,
toutes sauf une dans le sens d'une **surestimation**.

### 3.4 Les témoins de relecture — vérifiés au chiffre près, mais POST HOC

`agent/mesures/temoins-relecture` (fait foi : `resultats/c7-temoins-relecture.csv`). Les cinq
chiffres annoncés sont **exacts au CSV** : 12 items **1,2193 % [1,1118 ; 1,3301]**, 60 items
**20,7191 % [19,0402 ; 22,3837]**, facteur **16,9926** (→ 17,0), rapport à la baseline
**4,2579**, et la baseline démographique gagne **7,4067** sur le même intervalle.

Définitions, à ne pas confondre : le « facteur 17,0 » est le rapport du top-1 du jumeau à
60 items sur son top-1 à 12 items ; « la baseline gagne 7,4 » est **exactement la même
opération appliquée à la baseline démographique**. Le nombre d'items ne gonfle donc pas
seulement le jumeau, il gonfle tout ce qui attaque — le rapport à la baseline ne gagne qu'un
facteur **2,29** entre 12 et 60 items. Le facteur 17,0 **n'a aucun IC**, et l'étendue sur les
30 tirages d'items à k = 12 va de 0,34 % à 3,01 % — un facteur 8,9 entre extrêmes.

**Réserve obligatoire, que le rapport impose de faire suivre partout, manuscrit compris** :

> **POST HOC, NON PRÉENREGISTRÉ.** Les deux témoins de ce fichier ont été conçus après avoir
> vu les résultats qu'ils mesurent […] Ils ne comptent dans aucun dénominateur de
> multiplicité préenregistré et ne réfutent aucune prédiction préenregistrée.

---

## 4. Ce qui reste SOUS VÉRIFICATION, ou n'a été vérifié par personne

### 4.1 Vérifications que personne n'a faites cette nuit, et qui le mériteraient

**(a) A13, l'utilité en aval de D4 — c'est le plus urgent, et personne ne l'a rouvert.**
A13 affirme que D4 **préserve exactement** les comparaisons de groupes, « identiques à
16 décimales ». C'est **la même grandeur** que la ligne de registre `defense-d4-cout-groupes`
que `agent/correction/retractation-dp` vient de faire passer à `statut: retracte`, avec le
motif « ce 0,0 n'est pas un coût nul, c'est la REPUBLICATION EXACTE de la statistique ».
**A13 présente donc comme une utilité préservée exactement ce qui vient d'être requalifié en
fuite.** Aucune branche de la nuit n'a touché `c7-utilite-aval-resultats.md`. À rouvrir en
priorité.

**(b) A6, le 44,7 % de la condition « entretien seul » sur Park.** La synthèse le désigne
comme « le chiffre le plus défendable » tout en déclarant qu'il n'a **jamais** été rejoué
sous l'attaquant fort. Il ne l'a pas été cette nuit non plus. Et
`agent/audit/comparateur-conditionne` observe au passage que sur Park la condition disposant
de l'information individuelle la plus directe (`enquete`) est celle qui ré-identifie le
**moins** bien (20,6 %) — ce qui rend l'ordonnancement des conditions Park moins évident
qu'écrit.

**(c) A3, les taux à FPR = 0,1 %.** Le 44,37 % (Park) et le 1,01 % (Twin) reposent sur
**≈ 1 et ≈ 2 faux positifs absolus**. La synthèse le déclare déjà. Personne n'y a touché.

**(d) Vérifiés au passage et sains, pour mémoire** : A4 (bits) se reconstruit exactement
depuis `resultats/c7-bits.csv` — 3,551 [3,393 ; 3,718], 7,465 [7,273 ; 7,664], normalisés
0,0439 contre 0,0327 ; et 3,551 / 9,1375 pp = 0,389 bit par point, contre 0,079 / 1,1662 =
0,068 pour B2. A10 (échelle) se reconstruit depuis `resultats/c7-echelle.csv` : 0,5320 /
0,1867 = **2,85** à N = 50 et 0,2074 / 0,0214 = **9,69** à N = 2 058. Les deux tiennent.
Noter que la correction de multiplicateur de `agent/audit/items-banals` porte sur le **nombre
d'items**, pas sur la **taille du bassin** : elle ne contamine pas A10.

### 4.2 Réserves que les branches posent elles-mêmes

- **`residu-trajectoire`** : un seul jumeau Twin testé ; 5 sous-ensembles au lieu de 30 ;
  M2 et M3 sont **incompatibles** (aucun sous-ensemble n'apparie simultanément items et bits
  effectifs) ; le contrôle d'interprétabilité à M2 ne passe que **3 sous-ensembles sur 5**.
- **`comparateur-conditionne`** : sur Park, faute de transcriptions publiques, le comparateur
  à même entrée **n'est pas constructible** ; les quatre comparateurs sont des estimateurs
  **faibles** — ils bornent par le bas, ils ne prouvent pas qu'aucune méthode classique n'y
  arriverait ; et la concentration à 100 % sur les items d'achat, jointe au fait que le
  jumeau n'a **jamais vu** les réponses d'achat des vagues 1-3, reste **la question ouverte
  la plus sérieuse du dossier**.
- **`equite-risque`** : un seul attaquant (Hamming) ; le rapport déclare explicitement que
  le signe du corrélat pourrait changer sous un autre attaquant — c'est
  `agent/audit/predictibilite` qui le teste, pas lui.

---

## 5. Les branches non fusionnées, l'ordre de fusion, et les conflits attendus

**C'est la partie la plus utile de ce document : personne n'a de vue d'ensemble, et la fusion
est l'étape la plus risquée qui reste.**

Vérifié par fusion à blanc réelle dans un arbre jetable (`git merge` séquentiel, puis
`--abort`), pas par lecture.

### 5.1 Les douze branches de la nuit

| # | branche | commits | fichiers | apport |
|---|---|---|---|---|
| 1 | `agent/audit/comparaison-dp` | 1 | 1 | l'audit qui **fait foi** pour la rétractation DP |
| 2 | `agent/correction/retractation-dp` | 1 | 9 | pose la rétractation ; D4 requalifié ; 3 lignes de registre |
| 3 | `agent/mesures/residu-trajectoire` | 1 | 4 | le facteur entre époques tombe ; formulation autorisée |
| 4 | `agent/mesures/equite-risque` | 2 | 4 | le risque est binaire (Gini 0,816) |
| 5 | `agent/audit/predictibilite` | 2 | 3 | attaque la phrase de (4) ; témoin trivial 81,6 % |
| 6 | `agent/mesures/controle-generateur` | 1 | 4 | spécificité LLM, **version à réserve** |
| 7 | `agent/audit/comparateur-conditionne` | 2 | 3 | **lève la réserve de (6)** à information égale |
| 8 | `agent/mesures/attaquant-imparfait` | 2 | 4 | modèle de menace sous attaquant dégradé |
| 9 | `agent/audit/items-banals` | 2 | 3 | attaque (8) ; **BLOQUE LA PORTE P4** |
| 10 | `agent/mesures/temoins-relecture` | 1 | 4 | témoins 12 / 60 items |
| 11 | `agent/correction/t1b-cent-replicats` | 3 | 7 | nul de marge à 100 réplicats ; **conflit registre** |
| 12 | `agent/mesures/nul-corrige-csv` | 1 | 3 | **À ABANDONNER — périmée par (11)** |

Pour mémoire, six branches antérieures au 12/09 restent également non fusionnées et ne sont
pas traitées ici : `agent/latex/pdf-soumission`, `agent/latex/pdf-a-jour`,
`agent/portes/entete-outil`, `agent/portes/g31-marqueur`, `agent/orchestrateur/p2-grammaire`,
`agent/orchestrateur/decompte-typologie`, `agent/redaction/renvois-internes`, plus
`agent/biblio/anteriorites`, `agent/manuscrit/t3` et `agent/manuscrit/t4`.

### 5.2 Ordre de fusion recommandé

**Vague A — la rétractation d'abord, pour que rien ne pointe dans le vide.**

1. `agent/audit/comparaison-dp` — **avant** la suivante : c'est le fichier que le `fait_foi:`
   de la suivante désigne.
2. `agent/correction/retractation-dp` — le marqueur et l'en-tête de l'audité sont dans le
   même commit, la porte P4 (b) passe.

**Vague B — additions pures, aucun conflit, ordre libre sauf une contrainte.**

3. `agent/mesures/residu-trajectoire`
4. `agent/mesures/equite-risque`
5. `agent/audit/predictibilite` — après (4) : il attaque une phrase qui n'existe que là.
6. `agent/mesures/controle-generateur`
7. `agent/audit/comparateur-conditionne` — **impérativement après (6)** : il en amende la
   conclusion. Fusionner (6) seule laisserait publiable une affirmation que (7) corrige.
8. `agent/mesures/attaquant-imparfait`
9. `agent/audit/items-banals` — **après (8)**, et **seulement une fois la porte réparée**
   (voir §5.4).
10. `agent/mesures/temoins-relecture`

**Vague C — la seule fusion qui demande une main.**

11. `agent/correction/t1b-cent-replicats` — **conflit sur `resultats/registre-chiffres.csv`**
    (voir §5.3). Le placer en dernier concentre le seul conflit sur une seule opération.

**À ne pas fusionner.**

12. `agent/mesures/nul-corrige-csv` — **périmée**. Son unique commit porte le même titre que
    le premier des trois de (11), qui le contient et ajoute la série à 100 réplicats. La
    fusionner **après** (11) est pire qu'inutile : elle **rebascule** la colonne
    `fait_foi_tableau1` de la série à 100 vers la série à 20, c'est-à-dire qu'elle annule
    silencieusement la correction, et elle réintroduit un `.md` sans le bandeau qui déclare
    la série à 100 comme faisant foi — donc un `.md` qui contredit son propre CSV. La bonne
    action est de la **supprimer**, pas de la fusionner.

### 5.3 Le conflit unique, et comment le résoudre

**Fichier** : `resultats/registre-chiffres.csv`.
**Entre** : `agent/correction/retractation-dp` et `agent/correction/t1b-cent-replicats`.
**Cause** : les deux branches réécrivent le fichier en entier à partir de la même version de
`master`. Git ne peut pas les rapprocher, mais **elles ne se contredisent sur aucune valeur**.

**Résolution — une union, pas un arbitrage :**

- prendre les **trois lignes que seule `retractation-dp` ajoute** :
  `defense-d4-top1-adaptatif-s1`, `defense-d4-top1-opinion-naif`,
  `defense-d4-republication-multiensemble` ;
- prendre ses **deux lignes modifiées**, qui sont les versions rétractantes et doivent
  l'emporter : `defense-d4-cout-groupes` (→ `statut: retracte`) et `twin-d4-top1-residuel`
  (description amendée en « attaque NAIVE NON ADAPTATIVE ») ;
- prendre la **ligne que seule `t1b` ajoute** : `rho-nul-marge-appariee-12conf-n100` ;
- toutes les autres lignes sont identiques des deux côtés.

**Vérification après résolution** : `outils/portes/registre_chiffres.py --registre-seul` doit
compter **37 grandeurs** (33 sur `master`, +3 de `retractation-dp`, +1 de `t1b`).

Si l'on choisissait au contraire de fusionner `nul-corrige-csv`, un **second** conflit
apparaîtrait, à trois fichiers — `analyses/c7_temoin_verite_appariee.py`,
`resultats/c7-nul-corrige-marginal.csv`, `resultats/c7-nul-corrige-marginal.md` — sur des
données **numériquement identiques** mais avec `fait_foi_tableau1` inversée. C'est la
deuxième raison de ne pas la fusionner.

### 5.4 Le blocage de porte, et sa réparation en une ligne

`agent/audit/items-banals` **échoue la porte P4** et ne peut pas être fusionnée en l'état :

```
resultats/audit-items-banals-2026-09-13.md:3: statut « courant (section 0 = preenregistrement,
ecrite et commitee seule avant tout calcul, non modifiee depuis) » non reconnu
```

La porte n'accepte que `courant`, `provisoire`, `perime_par: <fichier>` ou
`retracte_par: <fichier>`. **Réparation** : ramener la ligne 3 à `statut: courant` et
déplacer la parenthèse dans `mandat:` ou dans la prose qui suit. Les onze autres branches
passent les deux volets de la porte.

### 5.5 Un angle mort de la discipline, à connaître avant de fusionner

**Un seul marqueur canonique de rétractation existe dans toute la nuit** : celui de
`retractation-dp-d4-2026-09-13.md` vers `c7-dp-resultats.md`.

Les autres invalidations de la nuit — le facteur entre époques, le « coût nul » de D4 dans
`cout-defense-synthese`, les 19 lignes de `c7-dp-courbe-combinee.csv`, la phrase de
`equite-risque` — **ne sont portées que par de la prose ou par des colonnes `statut` de CSV**.
La porte P4 le dit elle-même : une invalidation écrite sans marqueur « passe sans un mot ».

**Conséquence opérationnelle** : pour tout ce qui n'est pas la DP, **le présent document et
`resultats/article-synthese.md` sont le seul registre de ce qui a été retiré cette nuit.**
C'est exactement le mécanisme qui a déjà laissé partir un chiffre faux à un tiers.

**Le cas le plus dangereux, nommément.** L'audit `items-banals` interdit trois formulations
que la branche `attaquant-imparfait` publie telles quelles dans sa §7 — la section
explicitement destinée à l'article. Les deux branches vont être fusionnées ; **aucun marqueur
ne relie l'une à l'autre** ; après fusion, `master` contiendra donc côte à côte une
interdiction et le texte qu'elle interdit, sans lien machine-lisible. **À traiter à la main au
moment de la fusion de (9)** : soit en posant un marqueur de rétractation depuis l'audit vers
`resultats/c7-attaquant-imparfait-resultats.md` (ce qui oblige à poser l'en-tête dans le même
commit), soit en corrigeant la §7 dans la foulée.

Même remarque, moins grave, pour `controle-generateur` : sa « phrase exacte que l'article
devrait écrire » porte le 0,15 % faux (§6, ligne 12) et sa conclusion est amendée par
`comparateur-conditionne` — sans marqueur non plus.

---

## 6. Divergences rapport ↔ CSV relevées, toutes tranchées en faveur du CSV

| # | divergence | tranché |
|---|---|---|
| 1 | Republication D4 : l'audit dit **1 600** couples, le CSV **1 560** | **1 560** — l'audit comptait 40 segments dont un singleton que `defense_d4` saute. Conclusion inchangée (100 % des deux côtés) |
| 2 | `correction-t1b` §3 et le registre déclarent médiane n=100 = **0,9815884** ; le CSV porte **0,9816303335** | **CSV**. Chiffre déclaré « valeur exacte du CSV » qui n'en est pas une. Non publié, impact nul, mais à corriger |
| 3 | `correction-t1b` §4 écrit que l'observé « est plus bas que le 5ᵉ centile (0,9510) » | **Faux** : 0,9650 > 0,9510. La phrase se contredit elle-même. Le verdict (non-dépassement du p95) n'est pas touché ; c'est l'argument de marge qui tombe |
| 4 | Audit DP §F5 : 0,243 % / 20,656 % / 33,073 % ; CSV de la correction : 0,245 % / 20,639 % / 33,076 % | **CSV** (`c7-d4-adaptatif.csv`) — seul des deux à exister comme fichier. Écarts de 0,002 pt |
| 5 | `residu-trajectoire` §4 : colonne intitulée « contraste brut Twin/Argyle » dont le dénominateur 0,135 est la **baseline Twin**, pas le jumeau Argyle (0,137) | Étiquette fausse, effet numérique faible (11,4× → 11,2×). Les divisions sont faites à la main dans le `.md` ; le CSV qui fait foi ne les porte pas |
| 6 | `residu-trajectoire`, formulation autorisée : « 8.7 » et « between 1.4 and 3.7 » | **Non reconstructibles depuis une seule paire de cellules.** Le 8,7 exige la baseline à `courbe k=12` ; le 1,4 et le 3,7 ne viennent **pas du même balayage**. Point le plus attaquable de la phrase autorisée |
| 7 | `c7-residu-trajectoire.csv` contient des **lignes dupliquées**, et trois valeurs différentes pour `argyle-2023 … B-oracle` | Toute agrégation automatique double les lignes et doit choisir. À nettoyer avant publication |
| 8 | `equite-risque` §0 : top-1 20,69 %, baseline 2,15 %, « 2,13 % à 2 058 », « 13,29 % à 120 », « Park 65,6 % » | **Aucune trace dans `c7-equite-risque.csv`** — ce CSV ne porte aucune ligne de top-1. Non opposables sur lui |
| 9 | Le `+0,107` annoncé comme un gain | C'est une **corrélation de Spearman partielle**, sans dimension, **pas** des points de pourcentage |
| 10 | Le `81,6 %` du témoin trivial | **Aucun intervalle** : `ic_bas`/`ic_haut` vides. C'est un point nu |
| 11 | `comparateur-conditionne` : bloc `controle_interpretabilite` donne K2s à « 0,15 % [0,03 ; 0,32] », identiques à K10, alors que la ligne de mesure donne 0,1166 % | Divergence interne mineure au CSV, sans effet sur le verdict. À signaler |
| 12 | **`controle-generateur` : la phrase à publier écrit « ne dépasse 0,15 % (Twin) », le CSV porte 0,1535 %** | **CSV. C'est la divergence la plus grave de la nuit** : un chiffre faux, dans un texte destiné au manuscrit, et faux **dans le sens qui arrange** (la borne annoncée est franchie). Le même rapport écrit « 0,154 % » en §1 et « 0,16 % » en §3 — trois arrondis incompatibles. Écrire **0,1535 % [0,0894 ; 0,2255]**, ou « moins de 0,16 % » |
| 13 | `controle-generateur` : « AUC de l'ordre de 10⁻³ » pour GSS G1 | `auc_ouvert` = **0,0124**, soit 10⁻². Le tableau du même rapport l'affiche pourtant juste |
| 14 | `controle-generateur` : le contrôle de fidélité est affirmé « les quatre échouent » sans restriction de jeu | Le CSV ne porte **aucune** ligne `controle_fidelite` pour GSS. L'affirmation ne vaut que pour Twin |
| 15 | `items-banals` : « 99,8 % du gain restitué » | Recalculé sur le seul couple V2/V3 annoncé, il vaut **102,0 %** — le 99,8 % mélange deux exécutions. Conclusion inchangée (seuil P3 = 80 %), chiffre non reproductible tel quel |
| 16 | `items-banals` : `entropie_hors_pli, k=45` vaut **35,65 %** en V1 et **35,42 %** en V2, dans le même CSV | Écart de 0,22 pt non signalé ; le rapport cite les deux à des endroits différents |
| 17 | `items-banals` : la structure « 41 items binaires, 1 à 4, 10 à 5, 8 à 7 » | **Aucune ligne CSV** (`diag,-,criteres,45` est vide). Le fait structurel qui porte tout le raisonnement de l'audit n'existe que dans la prose |
| 18 | `items-banals` D4 à k = 6 (entropie basse) : le CSV donne `au_dessus_baseline = True` | Le rapport écrit « aucune rupture jusqu'à 15 items » et **sous-déclare** ce que le CSV montre. Divergence dans le sens **conservateur** |
| 19 | `temoins-relecture` : le « contraste 8,9× » figure dans un tableau de *rapports à la baseline* | C'est un rapport de **taux bruts** (0,012193 / 0,0013734). Le rapport de ces deux rapports vaudrait **2,38**. Ambiguïté de présentation à lever : ce contraste est neutralisé en nombre d'items, **pas** en baseline |

**Collision de graphie à surveiller** : 0,993 est à la fois le 95ᵉ centile de la loi nulle du
nul de marge et la borne haute du bootstrap de l'observé. Et 79,9 % (fraction des personnes à
`p_trivial > 0,999`, branche `predictibilite`) n'est **pas** 79,8 %
(`frac_risque_sous_1pct`, branche `equite-risque`) : deux quantités différentes, deux
branches, graphies voisines.

---

## 7. Le décompte honnête des réfutations

**TREIZE.** Dix-sept lignes au tableau des prédictions du manuscrit :
**treize réfutées, deux non concluantes, une non testable, une retirée.**

Le seul mouvement de la nuit est la **ligne 14** (« à budget modéré, la DP est dominée par
notre défense sur le tableau agrégé »), qui passe de **Réfutée** à **Retirée, non tranchée** :
la comparaison qui produisait ce verdict est rétractée. C'est la fiche R6 de
`retractation-dp-d4-2026-09-13.md` qui l'énonce, et elle chiffre elle-même le nouveau
décompte.

**Les autres lignes ne bougent pas**, mais deux changent de chiffre ou de réserve :
- **ligne 1** (le couplage dépasse un nul apparié sur la seule exactitude) : toujours
  **Réfutée**, valeur mise à jour de 0,974 à **0,980**, bande **[0,951 ; 0,993]** ;
- **ligne 13** (l'attaquant adaptatif casse la défense) : toujours **Réfutée, en faveur de la
  défense**, à 0,29 % — mais désormais assortie de la phrase que la fiche R4 impose :
  aucun de ces taux n'est une **borne**, ce sont les taux des attaques que nous avons
  construites, et sur les 20 items d'opinion le jumeau défendu et le jumeau **non défendu**
  sont indiscernables.

**INTERDIT** : écrire « quatorze », « quinze » ou « seize » ; écrire « réfutée » pour les
lignes 9, 16, 17 (non concluantes / non testable) et désormais **14** (retirée).

**Hors tableau**, et **ne bougeant pas le compteur** — conformément à la discipline déjà
appliquée à A14 et A15 pour les verdicts postérieurs à la clôture du recensement : les
prédictions préenregistrées rendues cette nuit par les audits sur eux-mêmes (P3 de
`comparateur-conditionne` **tenue**, P6 de `predictibilite` **réfutée**, le contrôle attendu
en échec de `residu-trajectoire` **réfuté**). Elles sont rapportées sur place.
