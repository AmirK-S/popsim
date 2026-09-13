# Relecture hostile du manuscrit d'après-nuit — un relecteur PoPETs qui veut rejeter — 13 septembre 2026

statut: avis de relecture, non mesuré
fait_foi: article/manuscrit.md à integration/nuit-2026-09-13 (8892e5c) ; resultats/registre-chiffres.csv pour les valeurs canoniques

mandat: relire le manuscrit entier en adversaire compétent, attaquer ce qu'il affirme au-delà de ses données, sa cohérence interne après sept passes, ce qui reste de la contribution, la dépendance à un seul jeu, le trou mécanistique déclaré, la forme ; rendre un avis tranché
agent: relecture / post-nuit, 13/09
ecriture: resultats/relecture-post-nuit-2026-09-13.md
lecture_seule: tout le reste, article/manuscrit.md compris
interdits: appel payant, réseau, recherche web, commit sur master, fusion, écriture hors du fichier du mandat

---

## 0. Avis

**Reject**, dans sa forme actuelle. Pas pour malhonnêteté — c'est le manuscrit le plus scrupuleux
que j'aie relu cette année — mais parce qu'après tous les retraits, la contribution positive
tient sur **un jeu de données, un bloc d'items, une configuration de jumeau, une métrique dont les
auteurs écrivent eux-mêmes que la direction s'inverse si on change k**, et parce que le titre
annonce un résultat que le corps désavoue.

Je passerais à **accept with major revisions** si, et seulement si : (a) le titre est refait,
(b) le 88× et le 29,9× sont traités selon la règle que les auteurs appliquent déjà à Argyle,
(c) la dépendance à k est résolue plutôt que concédée, (d) le PDF ne contient plus de marqueurs
non résolus, (e) la fenêtre de divulgation est ouverte. Rien de tout cela ne demande de nouvelle
mesure payante sauf (c).

---

## 1. Objections rédhibitoires

### R1 — Le titre publie le chiffre du jeu que le papier vient de désavouer

Titre : *« From Chance in 2023 to 60 % in an Open World »*. Le 60 % est
`park-tpr-fpr1-fort-ouvert` = **60,17 %**, c'est-à-dire **Park** (tableau 1 ligne 2 le dit
explicitement). Or §5.8 requalifie Park : armé à l'identique, son comparateur démographique
atteint **29,09 %** au même FPR, soit un rapport de **2,07×**, et **85,17 %** en monde fermé
contre 90,40 % pour l'agent — **1,06×**. Le papier écrit noir sur blanc « Park no longer carries
this paper's claim ». Le titre vend donc le chiffre du corpus dont le papier démontre qu'il ne
démontre pas ce que le titre suggère.

Ce n'est pas la seule faute du titre. Les deux bornes sont fausses chacune à sa façon :

- *« From Chance in 2023 »* : §5.8 dit que les jumeaux Argyle **échouent au contrôle
  d'interprétabilité** et que « no contrast is interpreted ». On ne peut pas déclarer un point
  de départ « au hasard » et, deux pages plus loin, refuser d'interpréter la mesure qui le fixe.
  §1.1 le concède : le point de 2023 « is not estimable ».
- *« 60 % »* n'apparaît **nulle part dans le résumé**. Le résumé annonce 20,7 % / 4,28 %. Titre et
  résumé ne racontent pas la même expérience.
- Le mot *trajectoire* est porté par le titre alors que §1.1, §7.2 et §7.4 disent trois fois que
  la trajectoire est confondue avec le protocole et non résoluble.

**Ce qu'il faut** : un titre qui ne contienne aucun chiffre de Park, aucune borne 2023, et pas le
mot qui suggère une causalité de capacité. Quelque chose comme « Linkability of LLM Digital Twins:
A Measured Rate, a Null That Absorbs Its Explanation, and a Control That Says When Not to
Measure ». Je note que le responsable a laissé le titre inchangé à dessein : en relecture, c'est
la première chose que trois relecteurs sur trois attaqueront, et la plus facile à réparer.

### R2 — Deux poids, deux mesures sur les rapports à dénominateur d'un individu

§5.8, sur Argyle, pose une règle et l'applique contre les auteurs : sous 1 %, « the rate is fixed
by the tie-breaking convention, not by the data ». Le registre va plus loin et **rétracte** le
facteur 2023→aujourd'hui au motif que « le rapport Argyle repose sur 1 à 2 succès absolus sur
2148 et n'est pas identifié par les données ».

Le chiffre de tête du papier viole cette règle. §5.8 : « 4.28 % against 0.05 % at 1 % FPR,
**88×** ». Le 0,05 % est `0,0486 %`, et §5.3 précise ce que c'est : **« one person »** sur 2 058.
Un rapport de 88 dont le dénominateur est un seul événement. Même structure exactement que ce que
les auteurs ont interdit de publier pour Argyle, appliquée cette fois dans le sens qui les arrange.
Le 29,9× fermé est moins grave (0,78 % ≈ 16 personnes) mais mélange un numérateur fort (23,23 %)
avec une phrase, en §5.2, qui annonce des comparateurs en attaque naïve.

**Ce qu'il faut** : publier le 4,28 % avec un intervalle de différence appariée au comparateur, ou
une borne inférieure du rapport, et retirer le « 88× ». Sinon un relecteur qui a lu §5.8 avant
§5.3 conclura que le standard de rigueur dépend du sens du résultat.

### R3 — La direction de la comparaison centrale dépend de k, et le papier le concède sans le résoudre

§5.2 est la section qui porte la thèse : à information d'entrée strictement égale, le jumeau
atteint 20,66 % là où le meilleur générateur classique atteint 0,45 %, et le donneur k=1 nourri
directement du bloc cible obtient **0,00 % [0 ; 0,18]**. Puis, en gras, trois lignes plus bas :
ce même comparateur avantagé atteint un **top-10 de 53,2 %**, *au-dessus* des 42,7 % du jumeau, et
« the direction of the whole contrast depends on the choice of k, which no principle fixes at 1 ».

Un relecteur ne peut pas laisser passer cela. Si la seule chose qui sépare le jumeau du
comparateur classique est le comportement de rang au premier candidat, alors « le jumeau fuit plus »
n'est pas un fait sur la fuite mais un fait sur la métrique. Le papier a besoin ici d'un argument,
pas d'un aveu : pourquoi le top-1 est la bonne quantité (parce qu'il correspond à une accusation
unique et que le top-10 ne correspond à aucune action d'attaquant réaliste ?), ou une courbe
top-k complète pour le jumeau et pour le donneur, ou une métrique qui ne dépend pas de k — les
bits d'identité de §5.6 sont déjà là et feraient l'affaire. En l'état, la concession est honnête
et **désarme le résultat principal** au lieu de le border.

### R4 — Ce que le papier apprend vraiment n'est peut-être pas un fait sur les *jumeaux*

Objection que je ne vois anticipée nulle part. §5.2 rapporte qu'un jumeau conditionné **sur le
seul segment démographique**, « which has never seen the individual », atteint **2,15 %**, contre
0,78 % pour la baseline démographique sous attaque forte et 0,45 % pour le meilleur comparateur
classique nourri de l'individu. §5.7 retrouve 2,13 % pour le Demographics Only de l'autre équipe.
Autrement dit : **un objet qui ne contient par construction aucune information individuelle bat
déjà de 2,7× la baseline démographique**, uniquement parce qu'un LLM produit des vecteurs de
réponses dont la structure de dépendance ressemble à celle des humains.

Mettez cela avec trois autres faits du papier : (i) §5.1, le nul de marge appariée reproduit le
couplage et **fuit davantage** que le jumeau (31,6 % contre 20,7 %) ; (ii) §5.5, toute la fuite
vit dans 40 items d'achat et le mécanisme est « unexplained » ; (iii) §5.5, l'ablation par
permutation des réponses détruit tout, donc ce qui identifie est la *structure de dépendance*.
La lecture concurrente devient difficile à écarter : ce qui est mesuré pourrait être, pour une
part inconnue, un **artefact de population** — la capacité d'un générateur quelconque à produire
des corrélations inter-items réalistes, amplifiée par un classement top-1 sur un bloc
produit × prix à forte structure interne — et non la trace d'une personne. Le papier a le témoin
qui trancherait pour le canal jumeau-à-jumeau (§5.4 : la personne apporte 82 % de la montée
au-dessus du plancher entre étrangers) mais **n'a pas l'équivalent pour la mesure T1 qui porte le
titre**. Il faudrait la même décomposition personne / segment / population sur l'attaque
jumeau→humain, ou un jumeau « segment seul » traité comme baseline officielle plutôt que comme
remarque de passage.

C'est l'objection que je poserais en premier si je n'en posais qu'une.

### R5 — Un seul jeu porteur, un seul bloc, une seule configuration, et un mécanisme inconnu

Après la requalification de Park et l'échec d'Argyle au contrôle, la revendication
jumeau-spécifique repose sur : Twin-2K-500, wave 4, **40 items d'achat sur 60**, configuration
JSON Persona GPT-4.1. §7.4 l'admet (« The mechanism analysis and the defense both rest on a single
block of a single dataset »). La défense D4 est mesurée sur ce même bloc. La concentration sur ce
bloc est déclarée inexpliquée (§7.2). Et §5.5 signale que Park **contredit** la localisation :
là-bas ce sont les items d'opinion qui identifient le plus, à entropie par item *plus basse*.

Est-ce que l'honnêteté sauve ? Non, et il faut le dire franchement au responsable : déclarer un
trou ne le comble pas. Un relecteur PoPETs accepte volontiers « nous ne savons pas pourquoi »
quand le *quoi* est robuste sur plusieurs surfaces. Ici le *quoi* est un bloc unique, la seule
réplication disponible pointe dans l'autre sens, et la seule tentative de reproduction
constructive a échoué (§5.7, gpt-4.1, fidélité 0,1714 contre 0,708). La parade que le papier
donne — Park requalifié « démontre que le risque de liaison existe **sans jumeau du tout** » —
est une bonne parade *pour un autre papier*, celui sur les blocs de quasi-identifiants. Elle ne
soutient pas la thèse annoncée.

**Ce qu'il faudrait, par ordre de coût croissant** : (1) refaire la mesure de tête sur les 20
items d'opinion de Twin et sur un sous-ensemble de 20 items d'achat, et publier les deux, pour que
le lecteur voie le bloc ; (2) une troisième configuration de jumeau Twin passant le contrôle,
pour que le résultat ne soit pas celui d'un modèle ; (3) au minimum, rétrograder §5.5 de
« Mechanism » à « Where the signal lives », puisque le mécanisme n'est pas établi.

---

## 2. Objections graves

### G1 — Le PDF de soumission contient des marqueurs non résolus

`article/latex/main.tex` porte **51 occurrences** de `{{R:...}}` non substituées, dont
**dans le résumé** (l. 74) et dans le tableau 1. Le lecteur du PDF verrait littéralement
`{{R:rho-nul-marge-appariee-12conf-n100}}` à la place de 0,980. Le commit 889a744 dit avoir
régénéré main.tex « après fusion (le LaTeX publiait 0.974) » : la régénération a bien supprimé la
valeur rétractée, mais en la remplaçant par un marqueur mort. Conséquence de relecture :
**personne n'a lu le PDF compilé de bout en bout**. À corriger avant tout envoi ; à vérifier par
une porte `grep -c '{{R:' main.tex == 0`.

### G2 — Le même chiffre sous plusieurs graphies, dans la même sous-section

- **Top-1 fermé du jumeau** : `20,7 %` [19,0 ; 22,4] (canon du registre, résumé, §1.1, §5.1,
  §5.5, §5.9, §6.1, §7.3), **`20,66 %` [19,0 ; 22,3]** (§5.2 l. 509), **`20,6 %`** (§5.5 l. 642).
  Trois graphies et deux intervalles pour une grandeur dont le registre dit « graphie publiée
  20,7 % ».
- **Top-1 sur les 40 items d'achat** : **`33,1 %` [31,2 ; 35,2]** l. 647 et **`33,2 %`
  [31,3 ; 35,1]** l. 660 — treize lignes d'écart, même section, même grandeur, deux intervalles
  différents. C'est le genre de chose qu'un relecteur trouve en dix secondes et qui coûte la
  confiance sur les 200 autres chiffres.
- **T2 B↔C** : le corps §5.4 rend le marqueur canonique (**1,76 %** [0,35 ; 3,63]) mais le
  tableau 1 ligne 17 code en dur **1,8 % [0,4 ; 3,6]**. Le registre signale le conflit de graphie
  et n'a été appliqué qu'à un seul des deux endroits — exactement la rétractation appliquée à
  moitié que vous me demandiez de chercher.

### G3 — Une erreur arithmétique vérifiable sur un témoin de tête

§5.8 : « takes the best of the three to 0,23 % and its baseline to 0,09 % — still overlapping,
still failing the control, **the whole gain four people out of 2,148** ». Le registre donne les
valeurs exactes : 0,002327747 = **5 personnes**, 0,000931099 = **2 personnes**. L'écart est de
**trois** personnes, pas quatre. Chiffre faux dans une phrase dont tout l'effet rhétorique repose
sur sa petitesse.

### G4 — Trois dénombrements de préenregistrements qui ne se raccordent pas

§7.1 : « **Seventeen** predictions were registered before computation; thirteen are refuted ».
§7.3 : « of the **34** preregistered predictions underpinning those claims at the time of the
census, 11 were refuted and 3 judged inconclusive ». Annexe : « The full census covers **47**
adjudicated tests across three families — with 25 confirmed and 15 refuted ».

17 / 34 / 47, et trois taux de réfutation différents (13/17 = 76 %, 11/34 = 32 %, 15/47 = 32 %).
Le papier s'en tire par une subordonnée (« which is why Table 1 and the census do not carry the
same totals ») et renvoie à l'annexe, qui ne réconcilie pas davantage. Or §7.3 utilise le taux de
32 % comme argument anti-dragage (« the opposite of the signature of data dredging ») — argument
qui s'évapore si le lecteur retient le 76 % de §7.1, ou qui devient suspect s'il remarque qu'on a
choisi le dénominateur le plus favorable pour cet argument précis. **Il faut un seul tableau de
recensement, une seule définition de « prédiction », et les autres familles nommées comme
« contrôles » et non comme « prédictions ».**

### G5 — Deux chiffres provisoires du registre publiés comme des mesures, dont un mal attribué

- §6 : « **4,4** points on inter-item correlations (**over ten seeds** ; the amplitude to be
  destroyed is 4.317) ». Le registre est formel : `defense-d4-cout-correlations` = 4,4 est un
  **tirage unique**, statut `provisoire`, et « sur 10 graines la valeur vaut 4,373 ± 0,058
  (étendue [4,254 ; 4,433]), le 4,400 publié étant en haut de l'étendue ». Le manuscrit accole
  donc « over ten seeds » au chiffre qui n'est justement pas celui des dix graines. Reprise
  telle quelle en §8(e) dans les défenses recommandées.
- §6 / §6.1 : `0,13 %` (`twin-d4-top1-residuel`) est également `provisoire` — tirage unique en
  haut d'une étendue [0,000 ; 0,187] dont la moyenne sur 10 permutations vaut 0,096 %. Il est
  bien accompagné du 0,29 % adaptatif comme le registre l'exige, mais rien n'indique au lecteur
  que le 0,13 % est un tirage.

### G6 — La divulgation responsable n'est pas ouverte

§8 : « **As of this submission the letters have not been sent and the 30-day window has not
opened.** » Sur un papier qui mesure une fuite ré-identifiante sur les données nominatives de
1 052 et 2 058 personnes réelles, et qui va publier le code de l'attaque, le comité d'éthique de
PoPETs ne se contentera pas d'une déclaration franche. S'y ajoutent, dans la même section : Park
sans licence déclarée (`node_license: null`), les conditions NORC sur le contenu GSS avec une
interprétation que les auteurs reconnaissent être la leur et non celle de NORC, et l'absence d'IRB.
Chacun est déclaré — mais déclarer trois obstacles ne les lève pas. **La fenêtre doit être ouverte
et close avant décision**, pas avant preprint.

---

## 3. Objections de forme — les cicatrices des sept passes

1. **§1.3(1) annonce des jumeaux « released in 2023, 2025 and 2026 ».** Les trois corpus sont
   Argyle 2023, Park **2024**, Toubia 2025. Il n'existe aucun corpus 2026 dans ce papier. §1.1
   aggrave : « Three years later » après 2023 donne 2026 pour Twin-2K-500. Millésimes à reprendre
   partout.
2. **§3, fin de T1** : « A third, T2, would remove the assumption entirely ». T2 est le
   **deuxième** modèle de menace, et il est décrit juste en dessous. Reste d'une version où T2
   était ailleurs.
3. **Densité et renvois.** §5.8 est appelé **21 fois** et §5.4 **17 fois** depuis le reste du
   texte. Aucune section ne se lit seule : le lecteur du §1.1, du §5.3, du §5.6, du §6.2 et du §8
   est à chaque fois renvoyé à §5.8 pour savoir si ce qu'il vient de lire compte. C'est la
   signature d'une requalification tardive absorbée par des renvois plutôt que par une
   réécriture. Sur douze pages denses, c'est épuisant et cela donne l'impression — injuste mais
   inévitable — qu'on cherche à noyer la requalification.
4. **§5.6, titre : « the instrument transports ».** Le transport est établi sur **deux** points
   (1,34× contre 3,2×), et le troisième jeu est celui où l'instrument « has no ratio worth
   transporting ». Un titre de section affirme au présent générique ce que deux points ne
   soutiennent pas ; « travels between our two usable datasets » serait exact.
5. **§1.3(3), « governed by which element differs, not how many ».** La loi de distance est
   réfutée — bien. Mais « naming them does [predict] » n'est démontré nulle part : il y a quatre
   facteurs à d=1, un chiffre chacun, aucun test prédictif, 15 paires et 6 à 9 configurations
   indépendantes. La réfutation d'une loi ne fonde pas la loi inverse. À reformuler en
   « the spread within a level dwarfs the spread between levels », qui est ce qui est mesuré.
6. **Divergence registre / manuscrit sur le facteur d'inflation par le nombre d'items.** §1.1
   publie « a factor of **8,7** between 12 and 60 items » pour la baseline démographique
   (source `c7-residu-trajectoire-resultats.md` §3) ; le registre canonise
   `temoin-items-apparies-facteur-12-60-baseline` = **7,4** (source `c7-temoins-relecture.csv`),
   avec la mention « CHIFFRE QUI INTERDIT DE LIRE LE FACTEUR 17 COMME UN PROGRÈS DES MODÈLES ».
   Deux études, deux valeurs, la moins canonique publiée. Sans conséquence sur la direction, mais
   à trancher avant qu'un relecteur ne le fasse.
7. **Figure 1** ne donne pas son chemin de fichier là où Figure 2 le donne ; `fig1-monde-ouvert.png`
   existe pourtant. Asymétrie de légende.
8. **Le résumé code en dur des valeurs que le corps laisse en marqueur** (54,5 % ; 20,7 % ;
   4,28 % ; 36,4 %). Tant que G1 n'est pas réglé, résumé et corps peuvent diverger silencieusement
   au prochain recalcul. Le registre avertit d'ailleurs que 54,5 est **aussi** la borne basse de
   `park-tpr-fpr1-fort-ouvert` : collision de graphie dans un résumé qui cite les deux jeux.

---

## 4. Ce que ce papier apprend réellement, après la nuit

Je liste ce qui survit, en étant le plus généreux que je peux l'être honnêtement.

1. **Une règle de méthode, gratuite, avec son coût payé en public.** Le contrôle
   d'interprétabilité a arrêté deux bras payants, la réplication Argyle et la condition `persona`
   de Park. C'est reproductible, c'est applicable avant dépense, et le papier montre ce qu'il en
   coûte quand on l'applique à soi. **C'est la contribution la plus solide du papier — et ce n'est
   pas celle que le titre annonce.**
2. **Un fait négatif net, contre les auteurs** : le couplage fidélité↔fuite, revendiqué en prose
   par Ward et Byun, ne survit pas à un nul apparié sur la marge d'exactitude — qui fuit même
   davantage. C'est publiable seul, et c'est utile à la littérature « blind baselines ».
3. **Une requalification instructive de Park** : un bloc de onze quasi-identifiants laissant
   98,86 % des répondants uniques, plus 177 items, produit 85 % de liaison **sans aucun jumeau**.
   Corollaire méthodologique réel : un taux sur ce genre de corpus n'est pas comparable entre
   études sans déclarer le nombre **et** l'identité des items et la convention de départage.
4. **Une mesure de taux sur Twin-2K-500**, sous réserve de R3 et R4.
5. **Un canal jumeau-à-jumeau intra-pipeline**, réel, avec ses témoins anti-artefact — mais T2
   reste non testé et le papier le dit.

**Est-ce assez pour PoPETs ?** Pour un papier intitulé comme celui-ci, non. Pour le papier qui
est réellement écrit — *un contrôle d'interprétabilité, un nul qui absorbe l'hypothèse centrale,
une requalification de deux corpus publiés, et un taux sur un jeu* — c'est un bon papier **court**,
et je le défendrais en PC meeting sous le titre honnête. Ce qui manque pour la version longue :
une deuxième surface porteuse (autre bloc, autre configuration, ou autre panel), et la résolution
de la dépendance à k.

---

## 5. Si je ne devais poser qu'une objection

Pas le titre — il se répare en une ligne. Celle-ci :

> Vous montrez qu'un jumeau conditionné sur le **seul segment démographique**, qui n'a jamais vu
> l'individu, atteint 2,15 % de top-1, soit 2,7× votre baseline démographique et 4,7× le meilleur
> comparateur classique nourri de l'individu. Vous montrez aussi qu'un nul apparié sur la seule
> marge d'exactitude fuit **plus** que votre jumeau. Quelle part de vos 20,7 % est une propriété
> de *cette personne*, et quelle part est une propriété des vecteurs de réponses que produit un
> LLM sur un bloc produit × prix ? Vous avez la décomposition personne / segment / population
> pour le canal jumeau-à-jumeau (82 %) ; donnez-la pour l'attaque qui porte le papier.

Tant que cette décomposition manque, le titre parle de ré-identification et la mesure pourrait
parler de réalisme de génération.
