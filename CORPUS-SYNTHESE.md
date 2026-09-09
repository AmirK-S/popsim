# Ce que dit le corpus, avant la seance

> **Erratum du 9 septembre 2026.** Le rang 2 ecrit « notre ablation est sans equivalent » a propos du couple C2 contre C3 : ce couple n'est pas une ablation de l'etiquette, C2 recevant onze attributs demographiques et C3 les 119 reponses de la personne sans demographie (`a45` section 0, `a47` D1).
> L'ablation propre, a un seul facteur, est le run R3 : `resultats/r3-resultats.md`. La revendication de nouveaute se lit desormais sur R3 et sur lui seul.

Fusion des sept fichiers de `corpus/`, de `FAITS-ETABLIS.md`, de `JOURNAL-2026-09-08.md` et des trois rapports arrives
pendant la redaction : a25 sur les items sensibles au mode, a26 sur les deux collisions, a27 sur arXiv 2607.25292. Le
8 septembre 2026. Direction a tester : « Ce que la simulation efface », une IA qui simule une population efface une
part de l'humain, et cette part n'est pas prise au hasard. a25 apporte le premier test de la these, la moitie tient et
l'autre tombe (section 4) ; a26 et a27 corrigent quatre formulations du dossier (section 5).

Quatre mots, definis une fois. Ecart entre groupes : la distance entre les reponses typiques de deux segments, gauche
et droite par exemple. Dispersion interne : la variete des reponses a l'interieur d'un meme segment. Rapport : la
valeur des agents divisee par celle des humains, donc 1 signifie identique. Plancher humain : ce que donnent les memes
personnes reinterrogees plus tard, donc le bruit sous lequel rien ne se prouve. Certitudes : [CONFIRME] lu dans le
texte, [PROBABLE] lu au resume, [MESURE] calcule chez nous.

---

## 1. Ce que le corpus dit, par question

### 1.1 Quelle fidelite, contre quel plancher ?

Trois chiffres portent le meme mot et ne se comparent pas : 0,85 de correlation sur 476 effets agreges (Ashokkumar
2026, corpus/01) ; 0,226 de distance a une distribution de groupe pour Claude Opus verbalisant contre 0,250 pour le
plancher humain, et 0,550 pour le meme GPT-4 lu par probabilites de jetons (Meister 2025) ; au niveau individuel, une
fidelite qui varie d'un facteur trois a quatre selon le jeu (Park 2026, Peng 2026). Le point utile est leur plancher :
quatre papiers sur cinquante publient ce que rapporte la strategie la plus bete, repondre toujours la modalite
majoritaire, et elle gagne alors, 0,77 contre 0,55 pour GPT-4, battant meme l'ANES a 0,70 (Li, Li et Qiu 2025) ; chez
nous elle bat trois des six conditions de Stanford (a2).

### 1.2 L'ecrasement est il propre aux LLM, ou a tout predicteur ?

Sur la dispersion, la seule reponse publiee nous est defavorable : rapport de 0,67 a 0,85 pour trois modeles et 0,72
pour une foret aleatoire supervisee, predicteur statistique sans alignement (Ku 2026, corpus/01) [CONFIRME]. Ils y
voient une propriete de la tache, et nos mesures concordent : la baseline qui prend la reponse la plus probable garde
73,1 pour cent de la variete humaine, celle qui repond la modalite majoritaire 3,4 (a23). Mais a25 ouvre une breche :
sur le contraste items sensibles contre temoins, les huit conditions a modele de langage montrent un effet et les
quatre baselines statistiques n'en montrent aucun, le retrait d'un seul item leur faisant meme changer de signe
[MESURE]. C'est le seul endroit du dossier ou un effet est propre au modele de langage et non a la prediction.

### 1.3 Qu'est ce qui gonfle les ecarts entre groupes ?

Trois causes tres inegales. L'etiquette : mettre l'ideologie declaree dans l'invite fait passer le gonflement de 0,34
a 8,51, facteur 25, sans changer l'exactitude de plus d'un point (a19, a1), et notre run local le reproduit, 8,16
contre 0,73, intervalles disjoints (a23). L'alignement : un modele post entraine exagere les ecarts d'un facteur
environ 2 la ou son modele de base les comprime a 70 pour cent de l'amplitude humaine (2608.03044, lu en a26)
[CONFIRME]. L'axe : tout l'effet massif se loge sur l'ideologie politique (a1). Deux contre exemples hors politique
sauvent la generalite, l'effet de l'age sur le rock alternatif gonfle d'un facteur vingt (Ma 2026) et un ecart
standardise de 0,56 sur l'education pour un contraste humain nul (Lukauskas 2026) ; et un contre exemple franc, les
ecarts raciaux aplatis voire inverses sur des patients simules (Keough 2026, corpus/02).

### 1.4 L'alignement rend il le modele presentable, et de combien ?

Oui, et l'ampleur depend de ce qu'on mesure. En lexique, 4 pour cent seulement. En semantique, trois equipes trouvent
le meme ordre : l'alignement retire entre les deux tiers et les trois quarts, avec une chute par entree d'un facteur 5
a 10 et une chute entre entrees de 10 a 20 pour cent seulement (Kirk 2024, Karouzos 2026, corpus/06). C'est notre
distinction, perte massive au niveau de l'individu et faible au niveau de la population. L'alignement ne centre pas,
il durcit : le modele converge vers l'opinion modale d'un groupe, jusqu'a 99 pour cent d'approbation de Joe Biden
(Santurkar 2023). Deux pieces cote a cote pour dire qui est efface : le pool d'annotateurs d'InstructGPT compte zero
pour cent de 65 ans et plus (Ouyang 2022), et les groupes les plus mal representes sont les 65 ans et plus, les veufs
et les pratiquants assidus (Santurkar 2023, corpus/06).

### 1.5 Quelle part des reponses humaines est de la presentation de soi ?

Il n'y a pas un chiffre unique. L'estimation la plus defendable, poolee sur 89 articles, donne 8,5 points d'aveux
supplementaires en interrogeant indirectement, intervalle de prediction de moins 11 a plus 28 : la moyenne est faible,
la dispersion est le resultat (Ehler 2021, corpus/04) [CONFIRME]. L'ampleur depend de l'item et non du theme : 80,8
pour cent de faux negatifs au telephone contre 55,6 sur le web (Kreuter 2008), 84,3 de vote declare contre 68,5 valide
(Ansolabehere 2012) ; ailleurs l'ecart est nul et mesure comme tel (Coppock 2017) [PROBABLE]. Regle a tenir : la
falsification existe, parfois massive, jamais l'explication par defaut d'un ecart. Le materiau operatoire est la note
de NORC, dont 12 items sensibles et 65 temoins tombent dans nos 149 (NORC 2023, croisement fait en a25) [MESURE].

### 1.6 Quelle est la structure reelle des attitudes ?

Deux dimensions au minimum, correlees a 0,30 seulement ; un axe suffit pour 72,8 pour cent des gens et rate 20,7 pour
cent d'incoherents genuins, contre 6,5 pour cent d'inattentifs, c'est a dire de bruit (Treier 2009, Fowler 2023,
corpus/05) [CONFIRME]. L'incoherence se loge entre domaines et non a l'interieur d'un domaine, et elle est maximale au
centre, 44 pour cent des moderes etant hors de leur quadrant. Hors des democraties riches, la correlation entre
conservatisme culturel et economique change de signe (Malka 2019). Important pour Amir : l'asymetrie droite gauche
n'est pas etablie, le biais partisan est symetrique, 0,235 contre 0,255, difference non significative (Ditto 2019)
[CONFIRME], et l'autoritarisme de gauche est mesure (Costello 2022). Avertissement : `polviews`, l'axe qui porte tout
notre gonflement, a une fiabilite de 0,66 contre 0,84 pour `partyid` (Hout 2016).

### 1.7 Ce que les modeles en font

Ils reduisent tout a un axe, dans la representation interne et non dans l'invite. Trois protocoles convergent : des
sondes lineaires predisent le score ideologique de 552 elus a 0,854 (Kim 2025) ; une analyse factorielle donne une
dimension dominante a environ 40 pour cent de la variance (Kabir 2026) ; une sonde entrainee sur une seule persona
predit les preferences d'autres personas meme quand leurs utilites sont anti correlees (Gilg 2026, corpus/05). Une
persona est un point sur un axe. Le chiffre le plus parlant porte sur le nombre de combinaisons : 19 patrons de
croyances sur 929 simulations contre 340 chez les humains (Wang 2025, corpus/05).

### 1.8 Le modele de base simule t il mieux ?

La question est mal posee tant qu'on ne dit pas contre quoi. Oui en emulation, 0,457 de distance pour Qwen3-14B base
contre 0,703 post entraine (2608.03044, a26) ; oui sur la distribution (Sorensen 2024), l'homogeneisation de textes
humains (Padmakumar 2024), l'imprevisibilite (West 2025, corpus/06). Deux corrections. 2609.00565 ne compte PAS dans
ce camp, ses six modeles sont tous instruits (a26). Et 2607.25292 n'evalue jamais un modele de base sur une enquete
humaine : il montre, a invite fixe, que la concentration de la distribution conditionnelle croit a chaque etape de
post entrainement, 0,236 au socle, 0,321 apres SFT, 0,411 apres DPO, 0,442 apres RLVR, sur des cibles ecrites dans
l'invite (a27) [CONFIRME]. Il ne prouve donc pas que le socle a la dispersion de la population. La formulation a
retenir : le deficit est en amont du tirage, dans la distribution conditionnelle, et la part de l'invite et la part du
post entrainement ne sont pas separees chez nous. Renversement a connaitre : en estimation, le modele aligne reprend
l'avantage. Il sait decrire une population qu'il ne sait pas incarner.

### 1.9 Contamination et coupures

Le terrain est vide et les outils sont gratuits : aucun comptage du GSS, de l'ANES ou du WVS dans un corpus ouvert n'a
ete publie, alors qu'infini-gram compte n'importe quelle chaine en 20 millisecondes (Liu 2024, corpus/07). Park v3,
Twin-2K-500, Bisbee et Santurkar ne contiennent aucune occurrence des mots contamination, memorisation, coupure ou
fuite [CONFIRME]. Trois garde fous. Un test negatif ne prouve rien : l'inference d'appartenance depasse a peine le
hasard (Duan 2024) et une contamination injectee 144 fois est oubliee apres cinq fois le budget de reference (Bordt
2024). Une coupure annoncee n'est pas auditee, jusqu'a dix mois d'ecart sur gpt-oss (Pezik 2025). Et le seul controle
serieux du champ joue contre nous, 0,74 avant coupure contre 0,90 apres (Ashokkumar 2026) : le bon patron de preuve
est « le lien entre le score et la presence dans le corpus disparait » (Roberts 2023, corpus/07).

### 1.10 Ce que les methodes statistiques font de la variance

Le MRP, methode standard qui estime une opinion locale en empruntant de l'information aux cellules voisines, retrecit
volontairement les ecarts entre groupes : c'est le mecanisme et non un defaut, pour un gain d'environ 10 points de
biais absolu quand l'echantillon est petit (Gao 2021, corpus/03) [CONFIRME]. Il n'a par ailleurs aucune dispersion
interne, produisant une probabilite par cellule et non une reponse par personne. Donc : notre double distorsion est
inter gonfle et intra ecrase, le MRP est inter retreci et intra nul, deux distorsions de signe oppose invisibles a
tout indice global, et les deux litteratures ne se citent pas. Deux bornes au discours commercial : 10 000 humains
plus 100 000 predictions valent au mieux 11 275 humains (Broska 2025), et un panel synthetique n'a d'avantage qu'en
dessous d'environ 100 reponses reelles (corpus/03). La ou tout tombe : sur les reponses choisies par moins de 10 pour
cent des gens, notre baseline en retrouve 3,6 pour cent et l'agent de Stanford 30,7 (a8).

---

## 2. Qui a deja dit quoi

| Revendication possible | Qui l'a deja faite | Ce qui manque chez eux | Ce qui reste a nous |
|---|---|---|---|
| Mesurer les deux termes sur les memes donnees avec le meme referent humain | Qin, Li et Cheng 2026 (2604.06663), 594 humains, deux composantes nommees (corpus/02) | pas de ratio en 1, pas d'identite additive, pas de plancher par reinterrogation ; et chez eux les DEUX termes s'ecrasent ensemble, 0,20 et 0,16 | la forme en ratio, la contrainte de somme, la dissociation d'avec l'exactitude, le plancher test retest. La revendication « premier a mesurer les deux » est morte |
| La double distorsion | 2608.03044 : ecarts entre groupes a 70 pour cent de l'amplitude humaine en base, facteur 2 apres post entrainement (a26) | AUCUN terme intra, verifie par comptage de mots ; aucun intervalle de confiance ; ni code ni sorties ; seule baseline l'uniforme, qui bat le meilleur modele dans 10 comparaisons sur 21 | la mesure conjointe des deux termes survit entierement, plus le plancher humain et la separation etiquette contre alignement |
| L'alignement paie la fidelite par la diversite | 2609.00565 : 37,9 chez les humains contre 5,1 a 9,9 apres reglage culturel, sur le WVS (a26) | leur diversite est l'esperance de la distance entre deux individus de deux PAYS differents : elle additionne ecart entre groupes et dispersion interne au lieu de les separer, verifie dans leur code ; et c'est un aplatissement, donc le signe inverse de 2608.03044 ; aucun correctif, ils l'ecrivent | la separation des deux termes, le plancher humain, et le constat que les deux papiers de la collision se contredisent sur le signe |
| Le deficit vient du post entrainement, et il se corrige par l'invite | 2607.25292, lu en a27 : gradient par etape sur OLMo-2, 0,236 au socle a 0,442 apres RLVR ; correctif PPA, moins 21 pour cent d'erreur contre Pew a cout nul en changeant l'ordre des modalites et la formulation ; code public | il n'evalue JAMAIS un socle sur une enquete humaine, ses socles sont testes sur des cibles ecrites dans l'invite ; zero terme intra, zero plancher de retest, zero desirabilite sociale ; PPA ne publie aucun cout au niveau de l'individu | nos revendications sur le terme intra, le plancher et le dicible tiennent. Mais il rend la voie « describe » et la perturbation d'invite obligatoires a tester, et il chiffre notre dette : le format d'invite vaut a lui seul 0,081 de distance, la moitie de l'ecart base contre instruct |
| L'ecart agent contre humain se concentre sur les items sensibles au mode | Personne. Croisement inexistant au 8 septembre 2026, fait par a25 | sans objet | le resultat est a nous, avec ses limites : il tient sur la liste NORC seule, pas sur le decoupage de la litterature, et il repose en bonne part sur quatre items nominaux |
| Diagnostiquer et corriger l'essentialisme identitaire | LifeMem, Wang 2026 : dispersion interne amelioree de 41,6 pour cent (corpus/02) | ne mesure JAMAIS le terme inter ; aucune exactitude publiee alors que son code la calcule ; aucun plancher, aucune baseline non LLM | les deux termes ensemble apres correction, et un critere qui distingue un deplacement de variance d'une dilatation |
| Publier les deux termes avec referent humain | Bisbee 2024 : ecart type 31,4 contre 16,1, soit 0,513 (corpus/02) | pas de decomposition additive, aucun plafond humain ; le « 7,8 contre 12,5 » n'est pas un ratio inter | le plancher par reinterrogation. A citer honnetement : ils observent deja une compression SELECTIVE sur les items raciaux et religieux, en une phrase, sans mesure |
| Mesurer inter et intra sur le GSS | Kim et Lee, depuis 2023, v4 de mai 2026, cinq de nos six axes (corpus/02) | aucun signe publie pour l'inter, intra sur predictions binarisees ; modele entraine sur le GSS | le regime persona, la forme ratio, le plancher humain |
| L'ancrage sur reponses reelles corrige la structure | Garzon 2026, cosigne Kamphorst et Bernstein : ICC divise par 2 a 5 (corpus/02) | l'ICC est un rapport jamais decompose ; aucun referent humain sur cette analyse, ils l'ecrivent ; segmentation age croise genre seulement | la decomposition, le referent humain, le plancher. Precedent le plus proche, meme maison |
| Le gonflement chiffre des ecarts entre groupes | Chen, Zhu, Zheng 2026 : median 2,3 sur GSS et 2,5 sur WVS (corpus/02) | agents demographiques purs ; porte sur une proportion, pas une composante de variance ; sur le WVS l'axe est le pays | publier notre ratio ET leur indice rend nos chiffres comparables a leurs seize cellules. Positionnement le moins cher qui reste |
| Une population simulee reste separable du reel | Marciaga 2026 : classifieur a 0,35 pendant que les marges sont a 0,68 a 0,87 (corpus/01) | un seul domaine ; grappes construites sur les donnees reelles puis fournies au modele, donc fuite | quinze lignes de code sur nos huit conditions, plus le plancher de la vague 2 |
| Exactitude et fidelite distributionnelle s'opposent | Kolluri 2025, equipe Bernstein : le DPO monte l'individuel, le SFT ameliore la distribution (corpus/01) | aucun plancher humain ; transfert incertain hors de leur repertoire | la meme dissociation normalisee par le meme plancher, sur les memes lignes |
| L'ecrasement est propre au modele de langage | Personne, et Ku 2026 dit l'inverse sur la dispersion : foret aleatoire a 0,72 contre 0,67 a 0,85 (corpus/01) | un seul pays, aucune segmentation donc aucun terme inter | a25 ouvre la breche : sur le contraste de mode, les baselines ne montrent rien. C'est notre seule reponse mesuree a Ku |

---

## 3. Ce que personne n'a fait

Verifie dans les sept fichiers et dans a25, a26, a27. Une recherche par absence n'est pas une preuve d'absence, et
elle a deja faibli deux fois pendant cette campagne.

1. La version continue du test de mode : correler l'ecart agent contre humain avec l'ampleur de l'effet de mode item
   par item. NORC ne publie que trois classes ; recalculer sur les microdonnees du GSS 2022. Faisable, non fait (a25).
2. Publier exactitude et dispersion sur les memes lignes, normalisees par le meme plancher humain (corpus/01,
   corpus/02) : deux colonnes de plus dans un tableau existant.
3. Mesurer le rapport de dispersion d'une baseline statistique dans le meme plan qu'un modele (corpus/01) : le ratio
   sur nos B0, B1, B2 deja enregistrees. Une soiree.
4. Poser un classifieur synthetique contre reel sur nos huit conditions (corpus/01) : quinze lignes de code, avec le
   plancher de la vague 2 que personne n'a. Et documenter le signe oppose du terme inter entre simulation par langage
   et MRP (corpus/03) : un tableau et une figure, aucun calcul.
5. Compter le GSS dans Dolma, RedPajama, The Pile et C4 (corpus/07) : une dizaine de requetes a l'API infini-gram, une
   heure, puis la sonde d'existence a cinq lignes dont une seule est reelle.
6. Essayer la voie « describe », un appel par item qui demande la distribution de la population au lieu de 150 appels
   par persona. Chez eux 0,22 contre 0,46. Cout : 149 appels, moins d'une minute. Jamais teste, absent de la liste E1
   a E6 de `corpus/06` (a27).
7. Rejouer leur panneau de cibles synthetiques sur nos modeles, loi ecrite dans l'invite et entropie observee sur
   appels repetes : notre run ne sait pas produire cette quantite, un appel par cellule. Prealable a toute comparaison
   base contre instruct (a27).
8. Corriger pour tests multiples : sur 39 tests d'un bloc on en attend deux sous 0,05 par hasard et il y en a trois
   (a25). Premiere chose a solidifier.

---

## 4. Cinq idees cles candidates, classees

### Rang 1. La simulation devie la ou les humains se surveillent, sans reproduire cette surveillance

C'est « Ce que la simulation efface » dans sa version la plus forte apres a25, et la seule candidate appuyee par une
mesure a nous. Les huit conditions a modele de langage, six de Stanford et nos C2 et C3, s'ecartent plus de la
distribution humaine sur les 12 items sensibles au mode que sur les 65 temoins, de plus 0,036 a plus 0,074, intervalle
sur les personnes excluant zero dans les huit cas [MESURE]. Les quatre baselines statistiques et les memes humains
reinterroges ne montrent rien : ce n'est pas un effet de predicteur, et c'est notre seule reponse mesuree a Ku 2026.
Mais la direction tombe : onze differences sur douze ne vont pas vers la reponse desirable, C2 est meme moins
presentable que les humains, moins 0,207 ; sur `polabuse`, 9 humains sur 150 approuvent la violence policiere et C2 en
fait approuver 71 [MESURE]. Ce qui est commun aux huit conditions est l'amplitude, pas le sens. Adversaire : l'effet
tient sur la liste NORC seule, disparait sur la classe adjacente et sur le decoupage par sujets de la litterature, et
repose en bonne part sur quatre items nominaux. Test decisif a zero cout : la version continue du croisement, plus une
correction pour tests multiples. Faisabilite : immediate.

### Rang 2. La simulation efface ce qui n'est pas deductible de l'etiquette

Corpus : la mesure la plus robuste du dossier. Le seul groupe qui s'effondre chez Argyle est celui des independants
purs ; l'ideologie explique 1,5 pour cent de la variance reelle et jusqu'a 67 chez le modele, facteur quarante (Chen
2026, corpus/01) ; l'etiquette vaut un facteur 25 chez nous, sur deux echantillons independants. a26 renforce : ni
2608.03044 ni 2609.00565 ne fait varier l'etiquette, notre ablation est sans equivalent. Adversaire : Ku 2026, une
foret aleatoire ecrase autant, donc c'est la prediction et non le langage. Test decisif a zero cout : le rapport de
dispersion de nos baselines sur les memes lignes que les agents. Si la statistique ecrase uniformement et le modele
selectivement, la these tient. Faisabilite : immediate.

### Rang 3. La part effacee est la part minoritaire, et le modele efface par le stereotype

Corpus : c'est ce que a26 chiffre le mieux. Chez Qwen3-4B, le taux de choix majoritaire monte de 38,53 a 52,29 apres
reglage et depasse le referent humain de 49,98, pendant que le nombre d'options distinctes tombe de 2,39 a 1,42 contre
3,61 chez les humains (2609.00565, a26) [CONFIRME]. S'y ajoute le paradoxe de Xiao 2026 : plus la fidelite par persona
est haute, plus la population est stereotypee (corpus/02). Nos agents s'ecartent de leur groupe autant que les humains
mais pas pour les memes personnes, 0,246 contre 0,895. Adversaire : Argyle 2023 reproduit la matrice d'associations
entre douze items a moins 0,026 pres, des lors qu'on lui donne onze vraies reponses en contexte. Test decisif a zero
cout : comparer le profil d'erreur des baselines et des agents cellule par cellule. Une moyenne se trompe
uniformement, un stereotype se trompe par groupe. Faisabilite : immediate.

### Rang 4. Marges justes, structure fausse

Corpus : trois equipes, trois jeux, trois metriques, meme conclusion. Correlation de 0,06 entre matrices
d'associations (Ma 2026), indice de Rand ajuste sous 0,07 (Jia 2026), classifieur a 0,35 avec des marges a 0,68 a 0,87
(Marciaga 2026, corpus/01). Le patron est aussi la signature attendue d'une restitution de tableaux publies, ce que
personne n'envisage (corpus/07). Adversaire : l'idee la plus deja dite du lot. Test decisif a zero cout : le
classifieur sur nos huit conditions et sur le plancher humain de la vague 2. Faisabilite : immediate, faible nouveaute.

### Rang 5. La part effacee est la part incoherente

Corpus : la cible humaine est chiffree, 20,7 pour cent d'incoherents genuins contre 6,5 d'inattentifs (Fowler 2023),
et l'ambivalence se modelise comme une variance conditionnelle, pas comme un residu (corpus/05). Adversaire : l'audit
le plus complet publie conclut que la moderation des modeles est le resultat net de positions compensatoires selon les
sujets, « exactement comme les electeurs moderes » (Aldahoul 2026, corpus/05). Test decisif a zero cout : la part de
contre presses par quadrant, cible 35 a 38 pour cent, plus le comptage de patrons normalise par la vague 2.
Faisabilite : immediate, adversaire serieux.

---

## 5. Les pieges de vocabulaire et de chiffres

Six formulations a retirer du dossier. Une, « compression intra a 70 pour cent » : 2608.03044 ne mesure aucun terme
intra, il n'a que l'ecart entre groupes, a 0,70 en base et environ 2 apres post entrainement (a26). Deux, 2609.00565
n'est pas une comparaison base contre aligne, ses six modeles sont tous instruits, sa mesure de diversite additionne
ecart entre groupes et dispersion interne, verifie dans son code, et son signe est un aplatissement, donc l'inverse de
2608.03044 : les deux papiers de la collision se contredisent, et leur Qwen3-4B est un autre point de sauvegarde, non
comparable au notre. Trois, « la simulation efface ce que les gens cachent » est falsifiee telle quelle par a25 : la
direction ne va pas vers le desirable. Quatre, « LifeMem, seul correctif publie » est faux : PPA en est un second, il
recupere 21 pour cent de l'erreur contre Pew a poids constants en changeant l'ordre des modalites et la formulation,
gratuitement (a27) ; ecrire « le seul correctif publie qui mesure la dispersion interne ». Cinq, « temperature 6,3,
piste fermee » se dit « insuffisante » : la temperature capture environ 15 pour cent du gain de PPA (a27). Six, la
comparaison base contre instruct est faisable chez nous avec une invite a trois exemples, qui enterre l'objection des
42 pour cent d'invalides, mais le format d'invite vaut a lui seul la moitie de l'ecart base contre instruct : le
prealable est « meme modele instruit sous deux formats », et le successeur apparie de Qwen3-4B-Base est Qwen3-4B
(a27).

Mots pris. « Transport » et « redistribution » sont occupes par trois papiers de 2026 dans trois sens differents
(corpus/02) : employer « reallocation de variance a total fixe ». « Flattening » vient de Wang, Morgenstern et
Dickerson 2024 et designe la perte de dispersion interne, pas l'ecart entre groupes.

Chiffres faux. Les 85 pour cent de Stanford sont perimes depuis avril 2026 et sont devenus le chiffre canonique du
champ (corpus/01). Le « 91 pour cent de la variance » attribue a Hewitt est une correlation corrigee lue comme une
part de variance. Le rapport 0,40 a 0,56 qui a circule chez nous porte sur toute une population turque, pas sur une
dispersion intra groupe (Ozkan 2026). La compression dite PsychBench a ete retiree par ses auteurs. Le « 7,8 contre
12,5 » de Bisbee est un ecart de niveau a 2012. Et ne pas ecrire que nos 80 pour cent de cellules quasi degenerees «
coincident » avec leurs 80 pour cent : ce sont deux quantites differentes, une frequence sur 50 appels contre une
probabilite lue a temperature 0 (a27).

Fiabilites, planchers, garde fous. `polviews` a une fiabilite de 0,66 contre 0,84 pour `partyid` (Hout 2016). Le
plancher humain se deplace avec le delai, 77,79 pour cent a deux semaines et 67,45 a quatre ans, ce qui fait passer le
meilleur agent de Stanford de 0,844 a plus de 1,008. Les rapports AAPOR et Coppock 2017 ecartent le votant timide
(corpus/04) ; Ashokkumar 2026 trouve l'inverse de la contamination (corpus/07) ; Cummins 2026 fait varier une
correlation de 0,23 a 0,84 par les seuls choix de pipeline, sur le papier fondateur du champ (corpus/01). Enfin,
declarer la famille d'hypotheses et corriger pour tests multiples, absent de tous nos rapports, a25 compris.

---

## 6. Ce que je n'ai pas pu verifier

- La version continue du test de mode est impossible en l'etat, NORC ne publie aucune ampleur par item (a25). Aucun
  chiffre n'a ete recalcule ici ; les valeurs viennent de a1 a a27.
- `corpus/07` annonce 53 entrees, sa table en compte 49 numerotees. Ecart non resolu.
- Jost 2003 et 2017, piliers de la these de l'asymetrie, sont sous paywall (corpus/05) ; douze classiques du theme 04
  restent [PROBABLE] ; Gui et Toubia 2023 est [NON LU] et le comptage infini-gram du GSS n'a pas ete fait (corpus/07).
- Les chiffres de 2608.03044 ne sont pas reverifiables, ni code ni sorties, et son estimateur de ratio n'est pas
  decrit : toute comparaison a nos 4,80 ou 7,64 compare des estimateurs inconnus (a26). Aucun chiffre de 2607.25292
  n'a ete reproduit non plus, alors que son depot le permettrait sans appel de modele (a27).

## Questions pour Simon, par ce qu'elles debloquent

1. a25 falsifie « presentable » et sauve « devie la ou l'humain se surveille ». Cette version affaiblie porte t elle
   un papier ? (L'idee cle de la seance.)
2. L'effet de a25 tient sur la liste NORC seule et il est a la limite de ce qu'une correction pour tests multiples
   laisserait passer. Consolide t on avant de communiquer ? (Sa solidite.)
3. La nouveaute sur le gonflement tombe a une replication, deux equipes publiant le meme ordre en aout 2026. Repli sur
   la mesure conjointe, ou revendication de la replication ? (Le positionnement.)
4. Les deux papiers de la collision se contredisent sur le signe et leurs quantites ne sont probablement pas la meme.
   Porte t on cette accusation technique ? (La related work.)
5. Le resultat de l'etiquette devient il le resultat principal ? Le papier cesse alors d'etre un papier de simulation
   pour devenir un papier de mesure. (La nature du papier.)
6. a27 met deux experiences a zero cout devant la nuit de calcul, la voie « describe » en 149 appels et le meme modele
   instruit sous deux formats d'invite. On les passe avant ? (Le plan de travail.)
7. Nos agents sont battus par une regression logistique. Assume t on qu'ils sont un banc d'essai ? (Le run local.)
8. Recalcule t on notre terme inter avec l'estimateur de 2608.03044 ? (La comparabilite.)
9. Quel jeu porte le papier, Twin-2K-500 sous licence libre ou le GSS sans licence declaree, et qui demande
   l'autorisation ecrite ? (La publication.)
10. Le trait de propension a s'ecarter de son groupe n'existe pas comme construit, seul le conflit de valeurs existe.
    Reformule t on ? (La famille de correctifs.)

---

## Annexe. Les sept fichiers et leurs references confirmees

| Fichier | Entrees | Confirmees | Note |
|---|---|---|---|
| `corpus/01-simulation-individus-populations.md` | 50 | 42 | 2 [NON LU] dont Dillion 2023, paywall |
| `corpus/02-homogeneite-variance-correctifs.md` | 45 | 35 | 10 [PROBABLE] ; 5 PDF relus en fin de passe |
| `corpus/03-baselines-statistiques-extension-enquete.md` | 39 | 28 | 9 [PROBABLE], 3 [NON LU] ; aucun lecteur de PDF pendant la passe |
| `corpus/04-desirabilite-sociale-opinions-cachees.md` | 51 | 37 | 12 classiques en [PROBABLE], resume seul ; sa prediction dirigee est testee et falsifiee par a25 |
| `corpus/05-structure-attitudes-heterogeneite-ideologique.md` | 52 | 32 | l'incoherence repose sur des [PROBABLE], la dimensionnalite sur des [CONFIRME] |
| `corpus/06-alignement-diversite-dicible.md` | 42 | 42 | seul fichier entierement confirme ; deux lectures de sa section 2.4 corrigees par a26 |
| `corpus/07-contamination-memorisation-coupure.md` | 53 annoncees, 49 numerotees | 40 | ecart de comptage non resolu, voir section 6 |
