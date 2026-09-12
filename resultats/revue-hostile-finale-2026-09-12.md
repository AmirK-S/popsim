# Revue hostile finale — PoPETs, 12 septembre 2026

Relecteur adverse, avis par défaut : rejet. Objet : `article/manuscrit.md` (1 108 lignes),
contrôlé contre `resultats/article-synthese.md`, `article-travaux-connexes.md`,
`positionnement-vie-privee-2026-09-12.md`, et — pour les deux points où j'ai soupçonné qu'un
chiffre ne mesurait pas ce que le texte prétend — contre `analyses/c7_disjoint.py`,
`resultats/c7-disjoint-resultats.md`, `c7-monde-ouvert-resultats.md`,
`c7-attaquant-fort-resultats.md`, `c7-fort-resultats.md`, `c7-synth-ajuste-resultats.md`,
`c7-contre-examen-2026-09-11.md`.

Convention : **défaut fatal** = l'article affirme quelque chose de faux, ou tire d'une mesure une
conclusion qu'elle ne permet pas. **Défaut de formulation** = l'article est vrai mais dit plus que
ce qu'il a mesuré.

---

## Verdict

**Révision majeure, à un cheveu du rejet** : le résultat négatif que l'article met dans son titre
— le « nul de marge » qui absorberait le couplage qualité-fuite — repose sur un témoin qui fabrique
ses réponses en recopiant celles de la cible, donc sur le contraire d'un prédicteur sans empreinte
individuelle ; la conclusion centrale de la section 5.1 n'est pas établie, ni dans un sens ni dans
l'autre.

Ce qui retient mon avis d'aller au rejet franc : les mesures descriptives du papier (A3, A6/A11,
A8, A13) ne dépendent pas de cette lecture et tiennent. L'article est réparable, mais pas par une
retouche de rédaction : il doit changer de titre, de résumé et d'introduction.

---

## Défauts classés par gravité

### F1 — FATAL. Le « nul de marge » est construit à partir des réponses de la cible : il ne peut pas tester l'absence d'empreinte individuelle

**Revendication touchée : A1** — et avec elle le titre, le résumé, §1.1, §5.1, la figure 2, la
ligne 1 du tableau 3, ainsi que les sections 5 et 6 de `positionnement-vie-privee` et la section 5
de `article-travaux-connexes`.

**Phrases en cause.**

Titre, ligne 1 :
> `Linkability of LLM Digital Twins: Open-World Rates, a Twin-to-Twin Channel, and a Null That Absorbs Our Own Coupling`

Lignes 65-68 :
> `We constructed a *marginal null*: 100 artificial predictors possessing nothing but a per-person conditional accuracy margin — no individual fingerprint, no structure whatsoever beyond "this predictor happens to be better on this person than on that one".`

Lignes 70-71, et c'est la phrase que je conteste :
> `**The coupling is real, robust and measured, but it demonstrates no individual specificity: a plain global-quality axis already suffices to produce it.**`

Lignes 391-393 :
> `The observed 0.969 does not exceed the null; it is below it. The coupling demonstrates no individual specificity. A plain global-quality axis already suffices to produce it.`

**Ce que fait réellement le témoin.** `analyses/c7_disjoint.py`, fonction `construire_nul`,
ligne 134 :

```python
out = np.where(masque, np.where(tirage_correct, y_ref, faux), -1).astype(x_reel.dtype)
```

avec, ligne 131, `tirage_correct = rng.random((n, m)) < q[:, None]` où `q` est le taux d'exactitude
de la personne. Cellule par cellule, le prédicteur « nul » émet **la vraie réponse de la cible**,
`y_ref`, avec probabilité q_i, et une modalité fausse sinon. Le vecteur produit pour la personne i
est donc une copie bruitée du vecteur de réponses réelles de la personne i.

C'est l'empreinte individuelle la plus forte qu'on puisse construire, pas son absence. Un tel
prédicteur s'accorde avec sa cible au taux q_i et avec les autres candidats au taux d'accord de
fond de la population ; il identifie par construction, et il identifie d'autant mieux que q_i est
grand. Les deux axes du nul — fidélité mesurée par `chute_brute`, fuite mesurée par `fuite_top1`
contre `y_ref` — sont des fonctions monotones du même q_i. Le rho de 0,984 est alors très proche
d'une identité arithmétique : exactement l'objection que le test sur items disjoints était censé
écarter, réintroduite par le témoin lui-même.

**Conséquence.** La prédiction (b) n'est pas « réfutée » : elle n'est **pas testée**. L'article
tire de ce témoin une conclusion qu'il ne permet pas. Et l'erreur ne sauve pas la thèse initiale
non plus — un témoin invalide ne confirme rien : A1 redevient une question ouverte. Le titre
annonce donc un résultat négatif qui n'existe pas, et le résumé en fait son argument d'intégrité
(« Following Das, Zhang and Tramèr, we built the control this literature was missing, and it
absorbs our own effect », lignes 31-32). Un relecteur qui ouvre le script voit cela en dix minutes ;
c'est le genre de découverte qui transforme un papier honnête en papier suspect.

**Ce qu'il faut faire.** Reconstruire le témoin de sorte que ses réponses ne soient jamais tirées
de `y_ref` : réaliser la marge d'exactitude par personne contre une cible permutée, ou contre les
marges de population, de manière que le prédicteur soit « bon sur cette personne » en moyenne sans
jamais copier ses réponses. Puis, séparément, **publier ce que le script calcule déjà sans le
sauvegarder** : le top-1 de chaque prédicteur nul, configuration par configuration (`fui[nom]`
dans la boucle des lignes 221-235, jamais écrit dans `c7-disjoint-nul.csv`, qui ne contient que le
rho). Si le nul actuel fuit à ~20 %, c'est la démonstration directe qu'il porte une empreinte.

**Coût.** Une demi-journée, en local, zéro appel de modèle. Le code existe déjà à 90 %.

---

### F2 — FATAL. Réfutation n° 16 tirée de zéro événement sur 30 personnes, avec un intervalle « [0 ; 0] » impossible

**Revendication touchée : A9**, et le décompte « sixteen refuted predictions » qui structure §1.3,
§7.1 et le résumé.

**Phrases en cause.** Ligne 605 :
> `fidelity **0.1714** against their 0.708; top-1 and top-10 **0.00 % [0 ; 0]** — below even our cheap twins (0.83 % at best).`

Ligne 606 :
> `**Two further preregistered predictions refuted**: accuracy > 0.55 and top-1 > 5 %.`

Ligne 815, tableau 3, ligne 16 :
> `| 16 | That same twin reaches top-1 > 5 % | **Refuted.** 0.00 % [0 ; 0], below our cheap twins | `c7-fort-resultats.md` |`

**Le défaut.** Le bras payant porte sur **30 personnes** (ligne 603, ligne 629). Observer 0 succès
sur 30 tirages donne, par la règle de trois, une borne haute à 95 % de **≈ 9,5 %**. La prédiction
préenregistrée était « top-1 > 5 % » : 5 % est **à l'intérieur** de l'intervalle compatible avec
l'observation. Cette prédiction n'est pas réfutée, elle est non concluante. Le « [0 ; 0] » est un
artefact connu du bootstrap percentile sur données à zéro événement — le rééchantillonnage de
trente zéros ne peut produire que des zéros — et non un intervalle de confiance.

Le même artefact affecte la ligne 428 (donneur avantagé, `0.00 % [0 ; 0]`), mais là sur 2 058
personnes : la borne exacte y est ≈ 0,15 %, très en dessous des 20,7 % du jumeau. **A2 survit donc
à cette correction ; A9 non.** C'est pourquoi je classe le premier en formulation et le second en
fatal.

Conséquence de comptage : l'article annonce seize réfutations, il en a quinze. Or le taux de
réfutation d'« environ un tiers » est précisément l'argument anti-dragage de §7.4. Gonfler ce
compteur avec une réfutation non établie abîme l'argument qu'il sert.

**Ce qu'il faut faire.** Remplacer tous les intervalles à zéro événement par des intervalles exacts
(Clopper-Pearson) ; reclasser la prédiction 16 en « non concluante, puissance insuffisante (n = 30) » ;
ramener le compte à quinze partout.

**Coût.** Quelques minutes de calcul, une demi-journée de reprise du texte.

---

### F3 — FATAL de portée. T2 n'a jamais été mesuré entre deux organisations, et le témoin qui distinguerait la personne du prompt n'existe pas

**Revendication touchée : A7** (contribution n° 1, la seule revendiquée sans antériorité).

**Phrases en cause.** Ligne 276, intitulé du modèle de menace :
> `### T2 — Two organisations publish twins of the same cohort; attacker holds nothing real`

Lignes 277-279 :
> `If several organisations each publish their own twins of the same panel with sufficient item overlap, a third party cross-references them holding no human answer at all.`

**Ce qui a été mesuré.** Sur Twin, des paires de **configurations de la même équipe**, produites par
le même pipeline à partir des **mêmes fichiers de persona** (les mêmes 494 items de contexte des
vagues 1-3). Sur Park, deux **conditions** des agents de la même équipe (entretien / enquête). Dans
aucun des deux cas il n'y a deux organisations, deux collectes, ni deux profils sources distincts.
Ce qui est établi est : « deux sorties de modèle conditionnées sur **le même fichier d'entrée** se
désignent mutuellement ». Le titre du modèle de menace annonce autre chose.

**Le témoin manquant, et c'est le point de validité de construction.** Le contrôle anti-artefact
est un leurre du même segment démographique (ligne 499) : il écarte la similarité de segment, il
n'écarte pas la similarité d'**entrée**. Tant que les deux jumeaux partagent la même chaîne de
persona, rien ne distingue « la sortie garde une empreinte de la personne » de « la sortie garde
une empreinte du prompt ». Le témoin qui trancherait : régénérer les deux jumeaux à partir de
personas dont le **contenu** a été permuté entre personnes d'un même segment, en gardant la
structure et la longueur du prompt. Si l'appariement survit à cette permutation, le canal relie des
prompts et non des personnes, et sa portée vie privée s'effondre à « ne publiez pas deux fois la
même entrée ». S'il s'effondre, A7 se renforce nettement.

Je note que ce témoin est aujourd'hui **infaisable** avec les moyens du projet, puisque §5.7 établit
que l'équipe ne sait pas reproduire des jumeaux à fidélité comparable. C'est une raison de
restreindre l'affirmation, pas de la maintenir en attendant.

**Ce qu'il faut faire.** Renommer T2 en « deux publications dérivées des mêmes profils sources » ;
retirer « two organisations » du titre du modèle de menace et de la contribution n° 1 ; énoncer le
témoin manquant dans les limites, nommément. L'affirmation défendable devient : *deux jeux de
sorties conditionnées sur le même profil restent appariables sans aucune réponse humaine* — ce qui
reste neuf et publiable.

**Coût.** Retrait et reformulation : une journée, zéro calcul. Le témoin lui-même : hors de portée
actuelle, à déclarer comme tel.

---

### F4 — SÉVÈRE, validité de construction. L'ablation présentée comme « la preuve la plus forte » ne prouve rien

**Revendication touchée : A5.**

**Phrases en cause.** Lignes 537-541 :
> `The ablation is the strongest evidence: permuting the order of each twin's 40 purchase answers drops closed-world top-1 from **33.1 % [31.2 ; 35.2] to 0.046 % [0 ; 0.11]**, below chance. [...] The identifying quantity is the dependence structure between answers, carried by the conditioning — not any answer taken in isolation.`

**Le défaut.** Permuter l'**ordre** des 40 réponses à l'intérieur d'un même jumeau détruit la
correspondance entre réponse et item. Après cette opération, la réponse à l'item 7 est comparée à
la vraie réponse de l'item 23. **Tout** prédicteur, y compris le retest humain, y compris un
prédicteur purement marginal, tombe au hasard. L'expérience ne sépare pas « structure de dépendance »
de « exactitude item par item » : elle supprime les deux. Que le résultat passe **sous** le hasard
(0,046 % contre 0,049 %) est le signe que la condition est dégénérée, pas qu'elle est informative.

Ce qui soutient réellement A5 se trouve ailleurs dans le papier et mérite la place : l'oracle du
seul compte de « oui » à 0,29 % (ligne 539), et surtout D4 (§6), qui permute entre personnes **à
item fixé** — la bonne ablation, qui préserve les marges et détruit la structure jointe, et qui
donne 0,13 %. C'est D4 qui démontre le point de A5, pas la permutation intra-personne.

**Ce qu'il faut faire.** Retirer la phrase « The ablation is the strongest evidence » et la
permutation intra-personne, ou la reclasser explicitement en contrôle de cohérence. Promouvoir
l'oracle du compte et D4 comme support de A5.

**Coût.** Nul — c'est un retrait. Aucun calcul nouveau.

---

### F5 — SÉVÈRE, statistique. « L'instrument voyage » est établi sur deux points avec un normalisateur libre

**Revendication touchée : A4** (contribution n° 5).

**Phrase en cause.** Lignes 561-563 :
> `Bits normalised by human entropy give 0.0439 (Twin) against 0.0327 (Park) — a factor of **1.34** — where top-1 varies by a factor of **3.2**.`

**Le défaut.** Deux jeux de données, donc deux points, et un normalisateur (l'entropie humaine)
choisi par les auteurs. Avec deux points et un paramètre d'échelle libre, on peut faire converger
presque n'importe quelle paire de quantités ; le rapport 1,34 contre 3,2 ne démontre pas une
propriété de transport, il constate que ce normalisateur-là rapproche ces deux nombres-là. Le mot
« transports » du titre de section (ligne 554, `the instrument transports, the rate does not`) et de
la contribution n° 5 est une généralisation à partir de n = 2.

Aggravant : §7.2 reconnaît, pour un problème voisin, que « an isolated success between two failures
is a coincidence, not a law » (lignes 842-846). Le même standard doit s'appliquer ici.

**Ce qu'il faut faire.** Requalifier : « cohérent sur les deux jeux dont nous disposons », et
déclarer que la transportabilité n'est pas testable à n = 2. Retirer le mot « transports » du titre
de section et de la liste des contributions.

**Coût.** Nul — reformulation.

---

### F6 — SÉVÈRE, statistique. La mesure que l'article déclare la plus défendable est la seule sans intervalle de confiance

**Revendication touchée : A3.**

**Phrases en cause.** Lignes 446-451 :
> `Removing that assumption gives the number we consider hardest to attack in review.` / `At a false-accusation rate of 1 %, the best twin recovers the right person **4.28 %** of the time on Twin-2K-500 and **60.17 %** on the Park archive under the strong attack. At FPR = 0.1 %: **1.01 %** and **44.37 %**.`

**Le défaut.** Vérification faite dans les sources : ni `c7-monde-ouvert-resultats.md` ni
`c7-attaquant-fort-resultats.md` ne portent d'intervalle sur les colonnes TPR@0,1 % et TPR@1 %,
alors que les colonnes top-1 des mêmes tableaux en portent. Tous les autres chiffres du papier sont
accompagnés d'un IC ; celui-là, non — et c'est celui que §5.3 et la figure 1 désignent comme le plus
robuste en relecture.

L'omission n'est pas cosmétique. À FPR = 0,1 % sur Twin, le seuil est calibré sur environ deux
fausses accusations parmi 2 058 candidats : la position du seuil est extrêmement instable, et
« 1,01 % » est un point sans incertitude déclarée. Sur Park à FPR = 1 %, une dizaine de fausses
accusations fixent le seuil qui produit le 60,17 % du résumé.

Je crédite les auteurs d'avoir refusé de tracer une courbe entre deux points mesurés (l'avertissement
des lignes 482-484 est exemplaire et rare). Il faut aller au bout : deux points sans incertitude
restent deux points sans incertitude.

**Ce qu'il faut faire.** Bootstrap sur les personnes, à seuil refixé dans chaque rééchantillon
(sinon l'incertitude du seuil est perdue), pour les quatre valeurs publiées.

**Coût.** Quelques heures, en local, zéro appel.

---

### F7 — SÉVÈRE. L'article retire un chiffre puis s'en sert quarante lignes plus loin comme base de comparaison

**Revendications touchées : A8 et A12.**

**Phrase qui retire.** Ligne 700 :
> `A previously circulated mean of 1.47 points divided by three an effect that falls entirely on one component, and is withdrawn.`

**Phrase qui s'en sert.** Ligne 739 :
> `the DP synthesiser at eps = 3 and eps = 10 loses **3.33** and **3.38** points of utility, within 5 points of D4's 1.47`

**Et encore.** Ligne 813, tableau 3, ligne 14 :
> `eps = 3/10 lose 3.33/3.38 points against D4's 1.47`

**Le défaut.** La comparaison à la confidentialité différentielle — donc la réfutation n° 14, donc
l'argument « we do not claim our defense beats DP » — est adossée à une statistique que la section
précédente déclare retirée, et retirée précisément parce qu'elle noie un effet concentré sur une
seule composante. Soit la moyenne de 1,47 est utilisable et §6 a tort de la retirer, soit elle ne
l'est pas et §6.2 compare la DP à un chiffre qui n'existe plus. En l'état, l'article se contredit à
quarante lignes d'intervalle, sur deux affirmations différentes.

**Ce qu'il faut faire.** Refaire la comparaison DP composante par composante (distribution,
groupes, corrélations), comme §6 l'exige désormais pour D4.

**Coût.** Faible, les composantes sont déjà dans `c7-dp-resultats.md` et `c7-defense-resultats.md`.

---

### F8 — SÉVÈRE, dossier. La revendication de nouveauté repose sur deux vérifications bibliographiques que l'article déclare lui-même non faites

**Revendication touchée : A7**, et la position générale du papier.

**Phrase en cause.** Résumé, lignes 20-21 :
> `We report a channel with no direct precedent:`

**Ce que le même document déclare.** Ligne 1080, OPEN ITEMS 5 : la définition formelle de la
linkability d'Anonymeter — le travail le plus proche, cité trois fois comme point de démarcation
(§1.2, §2.1, §3/T2) — n'a **jamais été lue sur le PDF original**. Ligne 1084, OPEN ITEMS 6 :
ZAK-MIA (PoPETs 2024) n'a **jamais été vérifié**, l'extraction ayant échoué, et l'article demande
lui-même de « confirm it does not constitute closer prior art to §5.4 » — c'est-à-dire à la section
qui porte la contribution n° 1.

Aggravant, ligne 1071 : `article/references.bib` **n'existe pas**, et toutes les clés de la section
References sont des conjectures auteur-année.

Pour PoPETs, affirmer « no direct precedent » dans le résumé tout en déclarant en annexe qu'on n'a
pas lu l'antériorité la plus proche est le motif de rejet le moins discutable de toute cette revue,
parce qu'il ne demande au relecteur aucun jugement technique.

**Ce qu'il faut faire.** Lire les deux articles, construire la bibliographie, et n'écrire « no
direct precedent » qu'après. Si ZAK-MIA recouvre §5.4, la contribution n° 1 tombe.

**Coût.** Deux à trois jours, aucun appel payant.

---

### F9 — SÉVÈRE, dossier. « Préenregistré » n'est pas attestable, et c'est l'argument central d'intégrité

**Revendication touchée : toutes** — le mot structure §4.4, §5, le tableau 3 et §7.4.

**Phrase en cause.** Ligne 354 :
> `The preregistration plans are not yet third-party timestamped; see `[OPEN ITEMS]`.`

**Le défaut.** §7.4 répond à l'accusation de dragage de données en invoquant 34 prédictions
préenregistrées dont un tiers réfutées. Cet argument n'a de force que si l'antériorité des plans est
attestable par un tiers. Sans horodatage, un relecteur hostile n'a aucun moyen de distinguer un
plan écrit avant calcul d'un plan écrit après, et l'argument s'effondre entièrement — non parce
qu'il est faux, mais parce qu'il est invérifiable. Un horodatage ne peut pas être rétroactif : si
le dépôt OSF n'a pas lieu, le mot doit changer partout.

**Ce qu'il faut faire.** Dépôt OSF horodaté avec DOI avant soumission. À défaut, remplacer
« preregistered » par « written before computation, not third-party timestamped » à chaque
occurrence, et retirer l'argument anti-dragage de §7.4.

**Coût.** Décision, pas travail. Mais sur le chemin critique.

---

### F10 — SÉVÈRE, statistique. L'IC du rho mesure la variabilité des partages, pas l'incertitude sur les méthodes

**Revendication touchée : A1.**

**Phrase en cause.** Lignes 385-387 :
> `over 50 stratified random A/B splits: Spearman **0.969**, median 0.972, 95 % CI **[0.937 ; 0.993]**, with 100 % of splits above 0.7`

**Le défaut.** Les 50 partages rééchantillonnent les **items**, pas les méthodes ni les personnes.
L'intervalle [0,937 ; 0,993] décrit donc la stabilité du rho d'un découpage d'items à l'autre. Il ne
dit rien de l'incertitude qui compte ici : celle qui vient du fait que le rho est calculé sur
**n = 12 méthodes**, choisies par les auteurs, et évaluées sur les **mêmes 2 058 personnes**. Un
Spearman sur 12 points a une distribution d'échantillonnage très large ; l'article publie un
intervalle étroit qui donne l'impression contraire. La ligne 406 (`Twelve points.`) reconnaît le
problème en note de limite, mais l'intervalle publié dans le corps le masque.

Les douze valeurs de fuite étant de surcroît mesurées sur la même cohorte, elles sont fortement
dépendantes : un bootstrap sur les personnes les ferait bouger ensemble, ce qui resserre
artificiellement tout intervalle calculé ainsi.

**Ce qu'il faut faire.** Étiqueter explicitement [0,937 ; 0,993] comme « dispersion entre partages
d'items », et ajouter un test de permutation sur les 12 méthodes pour l'incertitude qui compte.

**Coût.** Faible, local.

---

### F11 — SÉVÈRE. A2, la seule revendication forte qui survit, n'est appariée que sur l'exactitude *moyenne*

**Revendication touchée : A2.**

**Phrase en cause.** Lignes 413-417 :
> `At comparable marginal accuracy, no non-LLM predictor we tested exceeds 0.3 % top-1 where the twin reaches 20.7 % [...] JSON Persona GPT4.1 attains that rate at accuracy 0.590. The comparators, at accuracy 0.457–0.511`

**Le défaut.** Vérification faite dans `c7-contre-examen-2026-09-11.md` §1 : le tableau des
comparateurs ne rapporte qu'une exactitude **moyenne** par prédicteur. La **dispersion de
l'exactitude par personne** n'est reportée nulle part, pour aucune méthode. Or c'est précisément la
quantité qui gouverne l'identification : un prédicteur exact à 0,50 sur tout le monde n'identifie
personne ; un prédicteur exact à 0,50 en moyenne mais à 0,75 sur Alice et 0,25 sur Bob désigne Alice
sans difficulté. Deux méthodes « à exactitude comparable » au sens de l'article peuvent donc être
radicalement différentes au sens qui compte.

Le papier possède déjà l'objet qui trancherait — c'est `construire_nul`, qui fabrique exactement un
prédicteur calibré sur le profil d'exactitude par personne d'une méthode donnée — mais il ne s'en
sert que pour le rho, et ne publie jamais le top-1 qui en résulte.

Je souligne que A2 reste, en l'état, la revendication la mieux défendue du papier : le donneur
avantagé, ajusté directement sur le bloc cible, à 0,584 d'exactitude, avec un vrai signal individuel
(chute de 0,142 sous permutation) et un top-1 borné à ≈ 0,15 %, est un comparateur sérieux et
honnêtement choisi. Ce défaut n'est pas une réfutation ; c'est le seul trou qui reste, et il est
bouchable.

**Ce qu'il faut faire.** Publier la distribution de l'exactitude par personne pour les 12 méthodes,
et mesurer le top-1 d'un comparateur apparié à cette distribution, pas seulement à sa moyenne.

**Coût.** Faible, local, zéro appel — et c'est le même calcul que celui qui répare F1.

---

### Défauts de formulation (l'article est vrai, mais dit plus que ce qu'il a mesuré)

**f12 — Régimes d'attaque mélangés dans le résumé.** Lignes 33-35 : `a 1998 mechanism (PRAM)
applied to twins reduces closed-world top-1 from 20.68 % to 0.13 %`. Ces deux nombres sont des
mesures sous attaque **naïve**, alors que le taux vedette du même résumé (23,23 %) est celui de
l'attaque forte. Les chiffres correspondants sous attaque forte existent (23,23 % → 0,24 %) et
disent la même chose. *Correctif :* les employer. *Coût :* nul.

**f13 — Comptage des contributions incohérent.** Ligne 83 annonce `a set of five measurements` ;
§1.2 en énumère six, et dans l'ordre (1) (2) (3) (4) **(6) (5)** — la contribution 6 (lignes
125-128) précède la 5 (lignes 130-135), alors que la ligne 88 promet un ordre `from the least
expected to the most`. *Correctif :* renuméroter. *Coût :* nul.

**f14 — Renvoi circulaire.** Ligne 614 : `an independent check additional to the seven regenerated
twins of §5.7`, à l'intérieur de §5.7 même. *Coût :* nul.

**f15 — Une identité algébrique présentée comme un résultat.** Lignes 766-768 : `Group comparisons
are **identical to 16 decimal places**`. Permuter à l'intérieur d'un segment ne peut pas déplacer
une moyenne de segment : c'est vrai par construction, et §6 le dit (`exactly, by construction`,
ligne 695). Le présenter en §6.3 comme une mesure gonfle la liste des acquis. *Correctif :*
l'annoncer comme vérification numérique d'une identité. *Coût :* nul.

**f16 — Un chiffre du manuscrit sans artefact stocké.** Ligne 656 : `the Park archive gives 34.0 %
[23.5 ; 51.5]` à k = 60. L'OPEN ITEM 9 (ligne 1097) reconnaît que ce point n'est qu'« imprimé à
l'écran » et jamais écrit dans un CSV. Un chiffre publié doit avoir un fichier source ; c'est aussi
une exigence d'artefact PoPETs. *Coût :* minutes.

**f17 — Portée du 44,7 % en monde fermé.** Lignes 647-649 : `the cleanest demonstration that an
agent built from a conversation alone identifies its person`. C'est un taux en **monde fermé**, sous
attaque **naïve**, dans un pool de 1 052. Aucune mesure en monde ouvert n'existe pour la condition
« entretien seul » — or §5.3 pose que le monde ouvert est la seule mesure défendable. L'article ne
peut pas à la fois établir ce principe et présenter un chiffre en monde fermé comme sa démonstration
la plus propre. *Correctif :* soit mesurer le monde ouvert sur cette condition, soit retirer
« cleanest demonstration ». *Coût :* la mesure, quelques heures en local.

**f18 — Dossier éthique incomplet, déjà déclaré.** Lignes 992-997 : aucune détermination IRB ou
d'exemption propre à cette étude ; lignes 950-954 : lettres de divulgation non envoyées. Les deux
sont honnêtement déclarés, mais PoPETs attend une phrase nommant une institution, et la fenêtre de
30 jours est sur le chemin critique. *Coût :* décision.

---

## Ce qui survit — même si toutes les objections ci-dessus sont accordées

C'est la partie qui importe. Si j'accorde intégralement la tautologie (O1), la critique de validité
de construction du canal inter-jumeaux, la critique de portée et la critique statistique, il reste
**un papier de mesure, pas un papier de thèse** — et ce papier tient.

1. **A3 — les taux en monde ouvert, comme mesures.** Ils ne dépendent d'**aucune** lecture du
   couplage qualité-fuite, ni causale ni corrélationnelle. C'est la raison pour laquelle le choix de
   la figure 1 est le bon choix, et je le dis sans réserve. *Condition :* ajouter les IC (F6).

2. **A6 + A11 — le taux en monde fermé sur l'archive Park sous attaquant fort, 90,40 % [88,6 ; 92,2].**
   Paramètres estimés **hors pli sur 5 plis**, donc aucun candidat scoré avec des paramètres ajustés
   sur lui-même ; variante en échantillon (A-MI, 93,25 %) explicitement écartée du résultat publié.
   C'est la mesure la plus propre du papier. Le fait qu'elle **corrige à la hausse** la mesure
   précédente des mêmes auteurs, contre leur intérêt narratif, est un point d'intégrité que je
   crédite.

3. **A2 — le contraste à exactitude comparable sur le top-1.** Survit à la correction de
   l'intervalle à zéro événement (borne exacte ≈ 0,15 % contre 20,7 %), survit au comparateur
   explicitement avantagé, survit aux deux générateurs échantillonnés, et la réserve sur le top-10
   est déclarée par les auteurs eux-mêmes. C'est la seule revendication qui résiste frontalement à
   l'objection de tautologie. *Condition :* F11 — apparier aussi sur la dispersion par personne.

4. **A8 — la défense D4, avec son coût réel et l'attaquant adaptatif.** 20,69 % → 0,24 % sous
   attaque forte recalibrée, 0,29 % sous attaquant qui connaît le mécanisme et sait quels items sont
   intacts, jamais au-dessus de 1 %. Le coût est rapporté par composante après correction (4,4 points
   sur les corrélations), et la dégradation vers les humains (5,78 → 9,71) est déclarée contre
   l'intérêt des auteurs. La réserve sur le découpage 40/20 est portée. C'est la contribution
   constructive du papier et, à mon sens, sa meilleure.

5. **A13 — l'utilité en aval.** Mesurée, honnête, avec la reconnaissance que le jumeau non protégé
   se trompait déjà, et une recommandation praticable. Rien à redire.

6. **A12 — l'argument théorique sur la DP** (appartenance contre liaison ; le générateur DP
   n'échappe à l'attaque qu'en refusant la tâche du jumeau). C'est un argument, pas une mesure, et il
   est juste. *Condition :* F7 — le refonder sans le chiffre retiré.

7. **A10 — l'échelle**, avec son refus explicite d'extrapoler au-delà de N ≈ 4 000 et la
   justification de ce refus. Exemplaire.

8. **A9 comme résultat négatif honnête** : l'incapacité à reproduire la fuite, y compris avec un
   modèle de frontière payant et la recette per-item, énoncée sans atténuation. *Condition :* retirer
   la réfutation n° 16 (F2), qui n'est pas établie.

**A7 survit sous une forme réduite** : deux jeux de sorties conditionnées sur les mêmes profils
sources restent appariables sans aucune réponse humaine, à 36,4 % (60 items communs) contre 0,04 %
de contrôle. C'est neuf et c'est publiable. Ce qui ne survit pas, c'est l'emballage « deux
organisations » et l'idée que le témoin de segment suffit à écarter l'artefact de prompt.

---

## Ce qui ne survit pas et doit être retiré ou requalifié

| Élément | Statut | Action |
|---|---|---|
| **A1, dans les deux sens** | Le témoin est invalide (F1) : ni la thèse de l'axe unique ni sa réfutation ne sont établies | Retirer la réfutation, rouvrir la question, **changer le titre** |
| **Titre du papier** | Annonce un résultat négatif non établi | Refaire, autour du monde ouvert et du canal |
| **Résumé, lignes 24-32** | Présente le nul comme le contrôle manquant construit et concluant | Réécrire après F1 |
| **Figure 2 et son encart** | Trace une bande de nul qui ne mesure pas ce qu'elle prétend | Ne pas produire avant F1 |
| **Réfutation n° 16, et le compte de 16** | Zéro événement sur n = 30, « > 5 % » non réfuté | Reclasser en non concluante ; compter 15 |
| **« no direct precedent » (ligne 20)** | Antériorité la plus proche jamais lue (F8) | Ne réécrire qu'après lecture d'Anonymeter et ZAK-MIA |
| **T2 « two organisations » (ligne 276)** | Jamais mesuré (F3) | Renommer, restreindre |
| **« the instrument transports » (ligne 554)** | n = 2, normalisateur libre (F5) | Requalifier en « cohérent sur nos deux jeux » |
| **« The ablation is the strongest evidence » (ligne 537)** | L'ablation est dégénérée (F4) | Retirer ; promouvoir l'oracle du compte et D4 |
| **« D4's 1.47 » (lignes 739, 813)** | Chiffre retiré ligne 700 puis réemployé (F7) | Refaire la comparaison DP par composante |
| **Intervalles « [0 ; 0] »** | Artefact de bootstrap sur zéro événement | Clopper-Pearson partout |
| **« preregistered »** | Non attestable sans horodatage tiers (F9) | Déposer, ou changer le mot partout |

---

## Ce que je dirais au comité

L'article a une qualité que je rencontre rarement : il déclare ses échecs en première page, il
corrige ses propres chiffres contre son intérêt, et il refuse d'extrapoler là où beaucoup
extrapoleraient. Rien de ce qui précède ne met en cause sa bonne foi.

Mais il a construit son identité — titre, résumé, introduction — autour d'un résultat négatif tiré
d'un témoin qui fait exactement le contraire de ce que sa docstring annonce. Tant que ce point n'est
pas réparé, le papier raconte une histoire qu'il n'a pas démontrée, et le fait avec l'autorité que
lui donne précisément son honnêteté affichée ailleurs. C'est réparable en une semaine de travail
local, sans un seul appel payant — et le papier qui en sortira, un papier de mesure assumé, sera
plus solide que celui-ci.
