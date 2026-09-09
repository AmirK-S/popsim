# Modele du monde, popsim, 8 septembre 2026, nuit

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps de ce document n'est pas reecrit** ; les
passages a reprendre au matin sont listes en section 4 de `resultats/a47-errata-2.md`, avec
les runs dont ils dependent. Chaque point ci dessous cite la phrase d'origine, donne la
correction et donne la preuve. Recalculs : `analyses/a47_chute_segmentations.py`,
`analyses/a47_verifications.py` et `analyses/a47_income_v6.py` ; tableaux
`resultats/a47-*.csv`. Aucun script existant n'a ete modifie, aucun appel de modele de
langage, lecture seule sur `data/`.

### E1. Sections 10.4, 10.3, 9.2 et 5 : « ablation de l'etiquette » devient « contraste de conditionnement ». Objection a45 numero 1, contradiction D1.

**Phrases d'origine.** 10.4 : « L'etiquette ideologique est ce qui transforme un agent en
gabarit : **le meme modele, les memes personnes et les memes questions donnent 7 pour cent du
plancher avec l'etiquette et 45 pour cent sans** ». 9.2 : « sur **l'ablation propre C2 contre
C3**, le milieu ordinal est egal ». Section 5 : « L'ablation de l'etiquette a modele,
personnes, questions et traces constants : **personne** », place en tete de ce qui est libre.

**Correction.** C2 et C3 n'echangent pas l'etiquette, ils echangent integralement leur
entree. C2 recoit **les onze attributs de `demographic_summary.csv` et rien d'autre**, aucune
reponse de la personne ; C3 recoit **les environ 119 items de contexte, question et reponse
en clair**, et aucune demographie [CONFIRME, `analyses/a5_agents_locaux_gss.py`, `systeme_c2`
lignes 164 a 177, `systeme_c3` lignes 180 a 196]. Le contraste melange donc deux changements
et ses deux facteurs sont confondus. **La revendication de nouveaute de la section 5 est
vide tant que l'ablation n'est pas faite** : le dossier ne l'a pas faite non plus.

**Ce que le second facteur vaut a lui seul.** `B1 argmax` est une regression sur les memes
onze attributs, `B2 argmax` un plus proche voisin sur les memes 119 items sans aucune
demographie [CONFIRME, `a2_baselines_gss.py` lignes 178 et 188]. A moteur statistique
constant et **sans aucune ablation d'etiquette**, le passage de l'un a l'autre deplace la
chute sous permutation de **0,175 a 0,357 du plancher humain**, un facteur 2,0 ; le passage
de C2 a C3 vaut un facteur 6,2 [MESURE, `a47-chute-deux-segmentations.csv`, `S_ideo`]. Le
changement d'information explique a lui seul une part que la these attribue en entier a
l'etiquette, et personne ne l'a bornee.

**Ce qu'il faut ecrire partout.** « contraste de conditionnement, etiquette seule contre 119
reponses de la personne, les deux facteurs etant confondus ». L'ablation propre est le run R3
de la nuit du 8 au 9 septembre, C3 plus etiquette contre C3 et C2 prive de la seule ligne
`Political ideology` contre C2 ; elle devient le verrou numero un, avant la comparaison
appariee des minorites.

### E2. Section 10.3 et 10.4 : le « 7 pour cent du plancher humain » est indexe sur une segmentation qui contient l'ideologie, et le « 93 pour cent » est retire. Objection a45 numero 2.

**Phrases d'origine.** 10.3 : « v8 et C2 perdent 2,5 et 2,4, **soit 7 pour cent du
plancher** [...] **Les agents a etiquette ideologique sont des gabarits de groupe a 93 pour
cent interchangeables** ». 10.4 : « donnent **7 pour cent du plancher avec l'etiquette et 45
pour cent sans** ».

**Correction.** Les deux segmentations publiees par a44, `S_ideo` et `S_fin`, contiennent
l'une et l'autre l'ideologie, c'est a dire la variable meme que l'invite de C2 et de `v8`
recoit ; la permutation y mesure ce que l'agent sait au dela de ce qu'on vient de fixer.
Sous une segmentation de finesse comparable qui ne la contient pas, **genre x race x age, 38
cellules contre 42**, les chiffres changent de facteur.

**Preuve.** [MESURE, `a47-chute-deux-segmentations.csv`, 200 permutations par cellule ; les
colonnes `S_ideo` et `S_fin` reproduisent `a44-permutation.csv` au millieme]

| condition | `S_ideo` | `S_fin` | **genre x race x age, sans ideologie** |
|---|---|---|---|
| `agents v8` | **0,072** | 0,055 | **0,267** |
| **C2** | **0,073** | 0,074 | **0,185** |
| `B3 foret` | 0,129 | 0,082 | 0,187 |
| `B1 argmax` | 0,175 | 0,117 | 0,228 |
| `agents demographiques (v6)` | 0,235 | 0,229 | 0,236 |
| **C3** | **0,448** | 0,455 | **0,458** |
| `agents composite` | **0,642** | 0,638 | **0,695** |
| humains vague 2 | 1,000 | 1,000 | 1,000 |

**Ce qu'il faut ecrire.** « **7 pour cent du plancher humain sous la segmentation qui
contient l'ideologie, 18 a 27 pour cent sous celle qui ne la contient pas, contre 64 a 70
pour cent pour `agents composite` dans les deux.** » Le rapport entre les deux camps de
conditions passe de 9 pour 1 a 2,6 pour 1. **La formule « des gabarits de groupe a 93 pour
cent interchangeables » est retiree** : elle est le complement a 1 du seul chiffre `S_ideo`.
Sous genre x race x age, `v8`, C2, `B1` et `B3 foret` sortent tous de la classe « gabarit »
que a44 7.2 fixe a moins de 15 pour cent.

### E3. Section 10.4 : le facteur d'amplification de a38 est une quantite de gabarit. Objection a45 numero 3, contradiction D2.

**Phrase d'origine.** « [...] **un facteur d'amplification de l'ecart entre camps de 1,62
contre 0,52 quand humains et statistiques sont a 1** », cite comme l'un des piliers de la
these reecrite.

**Correction.** Le facteur d'amplification est une fonctionnelle de la seule table de
contingence (camp, modalite) : `a28_test1_mode.mesurer` le construit par `compte(mat, j, it)`,
qui denombre les modalites sur les lignes du camp. **Il mesure les marges par camp, pas les
personnes.** Mesure : il est **exactement invariant** sous permutation des personnes a
l'interieur de leur camp, ecart 0,00e+00 sur les 27 lignes testees [MESURE,
`a47-a38-invariance-facteur.csv`], et le generateur nul de a44 le reproduit a 100,0 pour cent
[a45 section 2.1, 30 replicats]. Le meme raisonnement vaut pour l'unanimite de a30, que a44
reconnait deja, et pour la pente de a37.

**Ce qu'il faut ecrire.** « Sur les quatre quantites citees comme piliers en 10.4, **une
seule, la chute sous permutation, n'est pas reproduite par un generateur sans structure
individuelle** ; les trois autres, gonflement inter, ecrasement intra et facteur
d'amplification, decrivent le gabarit de groupe et doivent etre publiees a cote d'elle,
jamais seules. » Le tableau 9.2 de a44 doit gagner les lignes a38 et a37.

### E4. Section 9.1 : C2 et C3 ne passent pas Holm, et la juxtaposition laisse croire l'inverse. Objection a45 numero 4, contradiction D3.

**Phrase d'origine.** « C2 a 1,62 [1,06 ; 2,10] contre C3 sans etiquette a 0,52 [0,20 ;
0,82], intervalles disjoints ; **huit tests passent Holm sur la famille de 52** (a38,
section 4). »

**Correction.** Les huit tests qui passent Holm sont **les six conditions de Stanford
(`composite`, `entretien (v3)`, `enquete`, `v6`, `v7`, `v8`) et les deux temoins `B0 mode` et
`B0 tirage`**, c'est a dire precisement les conditions qui ne permettent aucune inference sur
le conditionnement. **C2 est a `p` de Holm exactement 1,0000 et C3 a 0,2640.** Deux
intervalles disjoints ne sont pas un test, et aucun test apparie de la difference C2 moins C3
n'est publie nulle part.

**Preuve.** [MESURE, `a38-corrections.csv`, hypothese `K4 camp`, colonne
`p_holm_famille_complete` : six conditions de Stanford et deux temoins a 0,0026 ou 0,0068 ;
`B1 argmax` 1,0000 ; **C3 0,2640** ; **C2 1,0000**.]

**Ce qu'il faut ecrire.** « Les huit tests qui passent Holm sont les six conditions de
Stanford et les deux temoins ; C2 et C3, les deux conditions du contraste de conditionnement,
ne passent pas la correction principale, Holm 1,00 et 0,26, et ne passent que Benjamini
Hochberg sur la sous famille de 13. »

### E5. Section 7 : « le groupe pese jusqu'a huit fois plus » est une quantite de gabarit. Objection a45 numero 6.1, contradiction D7.

**Phrase d'origine.** Section 7, le 7,37 de `v8` et le 8,18 de la foret cites comme preuve
que « le groupe pese jusqu'a huit fois plus ».

**Correction.** a44 section 6 reproduit le 7,37 a **7,32** avec un generateur sans structure
individuelle, ses deux composantes a 99 et 98 pour cent, et le rappel des rares a 91 pour
cent. La phrase doit porter la mention « quantite de gabarit ». Ce qui reste debout est le
lift de personne, que le nul n'atteint pas, 0,241 contre 0,001 chez les humains et 0,212
contre 0,047 chez les conditions riches.

### E6. Section 10.4 : « moins 2,2 a moins 12,4 » est cite sans son denominateur. Objection a45 numero 9, contradiction D9.

**Phrase d'origine.** « [...] **deforme la loi humaine de consensus de moins 2,2 a moins
12,4** ».

**Correction.** Les pentes de a37 ne sont pas calculees sur le meme support : le rapport
droite sur gauche devient infini des qu'un camp est unanime sur un item, et l'item sort de la
regression. Les humains gardent **79 items sur 79**, `agents composite` 79, `entretien (v3)`
73, **`agents v8` 63**, `B3 foret` 45, **C2 46** et C3 71 [a37 section 3, colonne
`n_items_perdus_log` de `a37-agents-gss.csv`]. Le meme fichier donne une seconde estimation,
`pente_sur_derive_humaine`, qui vaut **moins 7,57** pour `v8` au lieu de moins 12,41 : le
choix de la variable explicative deplace le chiffre de 40 pour cent. a37 le declare ; la
synthese ne le reprend pas, ce qui est exactement la faute que a17 objection 2 avait
qualifiee de bloquante sur a1.

**Ce qu'il faut ecrire.** « Pente moins 2,22 sur 79 items chez les humains, moins 12,41 sur
les 63 items ou elle est definie chez `v8`, moins 7,57 si la derive humaine sert d'abscisse »,
et ne jamais comparer un compte d'unanimite entre les perimetres 150 et 1 052. **Le corps de
a37 n'a pas recu d'errata : ce rapport n'entre pas dans le perimetre du chantier a47.**

### E7. Section 10.4 : « 83 contre 14 pour cent de signal perdu » suit le conditionnement, pas l'etiquette. Objection a45 numero 9.1.

**Phrase d'origine.** « [...] **83 contre 14 pour cent de signal perdu au retrait du
segment** ».

**Correction.** a43 section 4.2, source du chiffre, mesure aussi 76 et 77 pour cent pour la
regression et la foret sur les memes onze attributs, et a43 section 1 est le seul endroit du
dossier qui range explicitement C3, `B2`, `PMM` et `IM` dans « ils voient la personne ». La
formule juste est : « 83 pour cent pour un agent qui n'a que l'etiquette, 76 et 77 pour une
regression et une foret sur les memes attributs, 14 pour un agent qui a les 119 reponses de
la personne : **le remplacement suit le conditionnement, pas le moteur**. »

### E8. Sections 9.1 et 10.1 : les rapports sources declares tombes n'ont pas d'errata. Contradiction D8, hors perimetre du chantier a47.

`MODELE-DU-MONDE.md` 9.1 declare tombee la phrase « la simulation devie la ou les humains se
surveillent ». **Les deux rapports sources, a25 et a28, ne portent aucun errata** : a25 ouvre
encore sur « le motif tient » et a28 sur son test 1 au rang 1. Un lecteur qui ouvre
`resultats/` dans l'ordre alphabetique lit d'abord la these morte. a25 et a28 ne font pas
partie des rapports confies au chantier a47 ; l'errata de trois lignes qui leur revient est
liste en section 4 de `resultats/a47-errata-2.md`.

### E9. Sections 9, 10 et 10.5 : la mention « preenregistre » n'est pas verifiable de l'exterieur. Objection a45 numero 10, [VERIFIE par a45, non recalcule ici].

Les cinq preenregistrements citent un commit du depot parent qui ne contient aucun des
fichiers preenregistres ; `git ls-files` renvoie zero fichier dans `Projets/popsim`, et aucun
depot OSF n'existe, alors que `PROTOCOLES-DE-RECHERCHE.md` section 4 point 3 l'exige. La
seule preuve d'anteriorite est l'horodatage d'un repertoire synchronise par iCloud. a45
section 13.1 constate que l'ordre est correct dans les cinq cas et qu'aucun preenregistrement
n'a ete touche apres son premier script ; c'est le maximum que le dispositif etablisse.
**Tant que rien n'est depose ni committe, le mot « preenregistre » ne doit pas figurer dans
un preprint.**

---

Ce document ne resume pas le dossier, il le relie : comment une population simulee par un modele de langage se
fabrique, ou chaque distorsion entre, pourquoi une personne y devient son groupe, et ce qu'on peut encore
debloquer. Il est ecrit pour un lecteur intelligent qui n'est pas du metier ; chaque terme technique est
explique a sa premiere occurrence. Conventions : une source courte suit chaque affirmation, « aN » designant le
rapport interne resultats/aN, « lecture 0N » le fichier corpus/lecture-complete/0N, un nom d'auteur et une
annee renvoyant a la lecture ou le papier est detaille. Niveaux de certitude : [ETABLI] mesure chez nous et
relu ; [ETABLI AILLEURS] lu dans un texte externe ; [PROBABLE] ; [HYPOTHESE]. Les rapports a34, a35, a36 et a37
sont arrives pendant la redaction et sont integres ; a34 signale lui meme qu'il n'est pas preenregistre.

Quatre mots reviennent partout. Ecart entre groupes : la distance entre les reponses typiques de deux segments,
gauche et droite par exemple. Dispersion interne : la variete des reponses a l'interieur d'un meme segment.
Rapport : la valeur des agents divisee par celle des humains, 1 voulant dire identique. Plancher humain : ce que
donnent les memes personnes reinterrogees deux semaines plus tard, c'est a dire le bruit sous lequel rien ne se
prouve. Exactitude : la part des reponses ou l'agent donne la meme modalite que la personne.

## 1. Comment une population simulee se fabrique, et ou chaque distorsion entre

Une population simulee est le produit d'une chaine a six maillons : le texte sur lequel le modele a ete
entraine, le modele de base qui en sort, l'alignement qui le transforme en assistant, l'invite qu'on lui donne,
la regle de tirage de la reponse, et l'instrument qui mesure le resultat. Le dossier a mis, pour la premiere
fois, au moins une mesure a chaque maillon.

### 1.1 Le texte d'entrainement : la statistique de groupe, cent mille fois plus presente que le questionnaire

Le fait de corpus est mesure. Dans Dolma, un corpus ouvert de 2 604 milliards de jetons representatif de ce
qu'un modele lit, le libelle exact d'un item du GSS, l'enquete sociale americaine qui sert de reference au
dossier, apparait une fois en mediane, « General Social Survey » 60 837 fois et « percent of Republicans »
123 159 fois ; dans DCLM, plus recent, 274 180 contre 38 (lecture 07, section 2) [ETABLI AILLEURS, comptage
fait par nous sur des corpus publics]. Le questionnaire n'entre dans les corpus que par la litterature qui le
commente, jamais par le codebook (lecture 07, 2.7). Un modele n'a donc pas appris ce qu'une personne repond a
une question du GSS ; il a appris des dizaines de milliers de fois la forme « x pour cent des republicains
pensent que ».

Deux corollaires sont publies. Gui et Toubia le formulent en langage causal : un modele entraine sur des
donnees d'observation repond, quand la question est ambigue, la conditionnelle de population P(Y|D) la ou on lui
demande une reponse individuelle sous intervention P(Y|do(D)) (Gui et Toubia 2025, lecture 07) [ETABLI
AILLEURS]. Ozkan le teste sur des personas turcs avec un controle placebo : la marginale nationale tient par
restitution, les affirmations de sous groupe sont « explainable by recall and prompt noise », et l'individu
s'effondre, la part du premier parti passant de 42,6 pour cent reels a 88,0 predits ; « one remembers, the
other collapses; neither simulates » (Ozkan 2026, lecture 07) [ETABLI AILLEURS].

Ce qui est etabli : la distribution du corpus. Ce qui est hypothese : que Llama, Qwen ou gpt-oss en aient
retenu cette distribution, leurs corpus n'etant pas publies (lecture 07, 7). Le seul banc qui teste les
croisements du GSS trouve des scores bas, mais sur des tableaux que le GSS ne publie pas en page web (Plecko et
al., lecture 07) ; un modele sait les statistiques dont on parle beaucoup et pas les autres (Hobor et al. 2026).
La distinction utile vient de PropMe : la capacite a restituer une statistique et la propension a la respecter
en simulant sont deux mesures, jamais mises dans le meme tableau (lecture 07, 4).

### 1.2 Le socle : la convergence est deja la, et le socle est trop disperse dans l'autre sens

Le modele de base, avant tout alignement, n'est pas la reponse. La convergence des sorties est deja dans le
socle et le seul prefixe d'assistant « Sure! Happy to help. » suffit a la faire sortir (2608.11426, lecture 06)
[ETABLI AILLEURS]. Sur la seule lignee ou quatre points de controle du meme modele sont compares a un referent
humain, OLMo 32B sur de la fiction, le socle a une variance de 6,03 fois celle des humains et un profil
affectif hors cible ; le post entrainement ne ramene pas vers l'humain, il traverse la cible (2605.27878,
lecture 06) [ETABLI AILLEURS, sur fiction]. Sur des distributions ecrites dans l'invite, « every base fails both 5-way targets; instruction
tuning amplifies an existing tendency » (2607.25292, a27) [ETABLI AILLEURS]. Le budget d'identite, c'est a dire
le fait qu'un modele a qui l'on donne deux etiquettes n'en garde qu'une, est deja dans le socle : le deficit de
race vaut moins 10,8 points dans Llama-3.1-8B de base et l'alignement le deplace de plus 0,6, non distinguable
de zero (Rennard et Xypolopoulos 2026, lecture 01, L1.01c) [ETABLI AILLEURS]. Sur les ecarts entre groupes, le
socle fait l'inverse du modele aligne : il les comprime a 0,70 de l'amplitude humaine la ou le modele post
entraine les exagere d'un facteur 2, sur trois paires appariees et 59 items Pew (2608.03044, a26) [ETABLI
AILLEURS, sans terme intra ni intervalle]. Ce qui reste ouvert, et c'est la question numero un du dossier :
aucun socle n'a jamais ete evalue sur une enquete humaine avec un referent de dispersion (a27, 4.2).

### 1.3 L'alignement : recopie des frequences, concentration par etape

L'alignement enchaine un ajustement supervise (SFT), une optimisation de preference (DPO) et un renforcement
(RLVR). Le dossier a dissous le debat « SFT ou DPO » : les deux mesurent des quantites differentes. Le SFT est
l'etape de la variance, 6,03 fois l'humain au socle puis 0,84, 0,49, 0,52 ; la preference est l'etape de la
position, la divergence de style continuant de croitre de 0,41 a 0,53 (2605.27878, lecture 06, C2) [ETABLI
AILLEURS]. Le SFT amplifie proportionnellement a la frequence prealable, 48 a 92 pour cent pour la cible la
plus frequente, 1 a 12 pour la sixieme, rien pour une cible hors support (2608.11426, lecture 06). Le theoreme
existe : dans tout objectif de renforcement regularise par la divergence de Kullback Leibler, deux reponses de
meme recompense gardent exactement leur rapport de probabilites de reference, « RL with any KL-regularization
does not increase the relative probability of lower-support samples » (2510.20817, lecture 06) [ETABLI
AILLEURS]. Six evaluateurs preferent l'argument partage a l'argument rare (2606.01736, lecture 06), et sur 264
modeles l'alignement deplace les profils vers le socialement desirable (Zierahn 2026, lecture 04) [PROBABLE].
La lecture d'ensemble : la substitution de la reponse typique a la reponse rare n'est pas un defaut
d'entrainement, c'est la solution du probleme tel qu'il est pose (lecture 06, 2.2). Ce qui reste hypothese :
que cette chaine, mesuree sur des metaphores, de la fiction et des cibles synthetiques, produise la meme chose
sur une enquete d'opinion.

### 1.4 L'invite : l'etiquette comme ancre lexicale, et le budget d'identite

C'est le maillon ou le dossier a sa mesure la plus solide et la plus repliquee. A modele, temperature,
personnes et questions constants, la seule presence de l'etiquette ideologique dans l'invite fait passer le
gonflement des ecarts entre groupes de 0,73 [0,47 ; 0,99] a 8,16 [5,43 ; 15,55], replique a 7,64 sur 300
personnes (a23, a21) [ETABLI]. Chez Stanford, entre deux generations d'agents demographiques qui ne different
que par l'etiquette, le facteur est 25 sans que l'exactitude change de plus d'un point (a19, a1) [ETABLI].

Pourquoi l'etiquette agit elle tant alors qu'elle informe si peu ? Parce qu'elle est une ancre et non une
information. Sur 277 philosophes, un effet de specialite de 1,9 point chez les humains devient 68,9 points chez
sept modeles sur sept, en partie par echo lexical, « biology » appelant « biological » (Shi et Haupt 2026,
lecture 02) [ETABLI AILLEURS]. L'importance d'un attribut chez les humains ne predit pas le gain du modele, et
son apprenabilite le predit a l'envers (Kamruzzaman et al. 2026, lecture 02). Le plafond est connu : moins de
10 pour cent de la variance sur les jugements subjectifs, 72 sur un vote presidentiel (Hu et Collier 2024,
lecture 02) ; en epidemiologie sociale, la part de variance entre strates identitaires depasse rarement 10 pour
cent (tutoriel MAIHDA, lecture 01, L1.16) [ETABLI AILLEURS]. Le budget d'identite donne la forme du defaut : les sous groupes humains se composent
additivement, poids total 1,83, les huit modeles testes restent sur la ligne alpha plus beta egale 1, et ils
gardent la mauvaise etiquette, 3 a 7 points au dessus du hasard (Rennard et Xypolopoulos 2026, lecture 01).
Enfin ce qui cree la diversite est qu'il y ait une identite differente d'un appel a l'autre, pas son contenu :
60 mots de detail demographique valent plus 0,004 de dispersion (2607.20429, lecture 01, L1.09). Ce qui reste
hypothese : nos invites n'ont jamais ete comparees a celles de Stanford, et un simple changement de format vaut
0,081 de distance sur un meme point de controle, la moitie de l'ecart base contre instruct (a27, 4.4).

### 1.5 Le decodage : rien a y chercher, sauf en surface

Lire la distribution complete du modele au lieu de sa reponse la plus probable ne rend que 1,4 point sur 34,6
manquants de dispersion totale ; combler le reste exigerait une temperature de 6,29, qui multiplierait par 8,6
l'hesitation a chaque question (a23, a18) [ETABLI] ; le calcul homologue chez 2607.25292 donne 17 et 56 (a27).
Huit interventions d'invite qui demandent un tirage echouent, un seul appel qui decrit la distribution reussit
(a27) [ETABLI AILLEURS]. Un modele aligne n'a plus de branches a ouvrir (2506.17871, lecture 06), et l'abliteration
deplace la position sans rendre aucune variance (2607.17427, lecture 06). Deux nuances : la temperature apres
une coupe de validite recupere de la diversite (2605.11128, lecture 06), et randomiser l'ordre des modalites et
la formulation, a poids constants, recupere 21 pour cent de l'erreur a la population (PPA, a27). L'effet de
l'ordre des modalites n'est pas mesure chez nous, sur 43 questions a modalite dominante (a23) [OUVERT].

### 1.6 La mesure : la note aveugle, le delai de retest, la chaine d'extraction

Le dernier maillon fabrique de la distorsion dans les deux sens. La note d'exactitude est presque aveugle a la
structure : deux conditions du meme papier, memes 1 052 participants, dont l'exactitude ne differe que de 0,83
point, ont des gonflements qui different d'un facteur 13,5 (a1, a19) [ETABLI] ; Peng et al. publient une
dissociation voisine, correlation 0,105 contre 0,555 a exactitude egale (a36). Le delai de retest deplace le
score a lui seul : 77,79 pour cent a deux semaines, 67,45 a quatre ans, et le meilleur agent de Stanford passe
de 0,844 a 1,008 selon le delai retenu (a12) [ETABLI]. La chaine d'extraction inverse le classement de
diversite, 4,48 modalites contre 3,62 avant appariement au vocabulaire de l'enquete, 3,07 apres (a16). Les metriques standard des donnees synthetiques excluent explicitement les valeurs atypiques
(Alaa et al. 2022, lecture 03), et synthpop retire les cas rares par exigence de controle de divulgation (Nowok
et al. 2016, lecture 03) [ETABLI AILLEURS]. Enfin 33 a 46 pour cent des repondants de plateforme s'aidaient d'un
modele des 2023, donc un plancher recolte en ligne apres cette date est deja en partie synthetique (Veselovsky
et al. 2023, lecture 07). Le manuel d'imputation dit tout cela en une phrase : « the method yielding the lowest
RMSE is bad for imputation » (van Buuren, lecture 02, L02-12).

## 2. Pourquoi une personne devient son groupe

### 2.1 Le mecanisme, reconstruit

Mettons les pieces bout a bout. Le modele porte, du pre entrainement, une loi a priori faite de statistiques
de groupe et presque pas de reponses individuelles (1.1). Son objectif d'alignement recopie les rapports de
frequence de reference et ne remonte jamais une reponse rare (1.3). On lui donne une etiquette qui cherche son
echo dans les options, sans ponderation par ce qu'elle explique (1.4). On lui demande une reponse unique dans
une nomenclature fermee, ou la reponse la plus probable est, par construction, la modalite typique du segment
(1.5). Le produit de ces quatre contraintes a un nom en statistique : l'imputation par l'esperance, le
remplacement d'une valeur inconnue par sa valeur predite.

Le manuel chiffre ce que fait cette operation : imputer par la valeur predite fait tomber la dispersion
residuelle et monter les correlations, de 0,35 a 0,39 sur son exemple, parce que les points imputes sont sur la
droite ; « regression imputation artificially strengthens the relations in the data » (van Buuren, lectures 02
et 03) [ETABLI AILLEURS]. C'est, terme pour terme, la double distorsion du dossier. Et le theoreme se verifie
sur nos cellules : passer de la reponse la plus probable au tirage dans la meme loi, a modele constant, coute
7,8 a 10,2 points d'exactitude, remonte la dispersion interne de 0,20 a 1,01 et fait tomber l'ecart entre
groupes de 0,58 a 1,48, douze contrastes passant la correction de Holm sur une famille declaree avant (a35, H1)
[ETABLI]. Ahn, Mao et Lee donnent la raison pour laquelle enrichir la persona ne repare rien : apres retrait de
la moyenne de chaque item, il reste 3,05 pour cent de variance individuelle expliquee contre un plafond de
53,6, et l'interaction personne x item vaut 8,9 fois l'effet personne stable (lecture 03, L03-01) [ETABLI
AILLEURS]. Une persona est fixe d'un item a l'autre ; elle encode « qui est cette personne en moyenne », jamais
« comment elle s'ecarte sur cette question ». La marge n'est pas dans l'entree parce que l'entree est du
mauvais type.

Nos mesures disent la meme chose par six chemins, tous a modele, personnes, questions et traces constants.
L'etiquette deplace le profil d'erreur de treize points vers la modalite majoritaire du segment, 0,610 contre
0,481 (a28, test 3). Elle fait tomber l'appariement des reponses rares aux bonnes personnes de 0,410 a 0,194
(a29). Elle ajoute de la rarete de groupe aux fausses raretes, plus 0,034 [0,025 ; 0,043], et rien du cote de la
personne ; le rapport groupe sur personne vaut 4,45 avec etiquette, 0,44 sans, 0,56 chez les memes humains
reinterroges, 8,18 pour une foret aleatoire (a31). Elle ecrase la dispersion interne presque du double, 0,365
contre 0,681 (a35, section 4). Elle rend le camp de gauche simule litteralement unanime, indice de Gini Simpson
de 0,000 sur seize items ou les memes 63 humains sont a 0,246 et 0,396, ce que la condition sans etiquette ne
fait pas (a30) [ETABLI pour les cinq]. Et l'explication concurrente, le manque de contexte, est refutee a
personne constante : retirer la famille thematique entiere de l'invite coute six points d'exactitude et fait
baisser, pas monter, la rarete de groupe des fausses raretes (a33) [ETABLI].

Le rapport a34 restreint la portee du mecanisme, et c'est important. Sur les seules fausses raretes que le
groupe ne predit pas, l'ablation C2 contre C3 survit intacte, 4,12 contre moins 0,75, et l'agent demographique
v8 reste a 8,27 ; mais les trois conditions riches de Stanford tombent sous 1, composite a 0,02, entretien a
0,09, du cote humain (a34, section 4) [ETABLI, famille ecrite apres une lecture descriptive]. Sur la rarete
indeductible, un agent nourri d'information individuelle place ses erreurs par la personne, comme les
humains ; seul l'agent qui n'a que l'etiquette les place par le groupe. La substitution de la personne par le
groupe est donc un mecanisme de l'etiquette, pas du langage.

### 2.2 Ce que la statistique classique fait de pareil et de different

a35 met vingt et une methodes sur les memes cellules et donne la reponse. Ce qui est pareil : sept conditions
a modele de langage sur huit ecrasent la dispersion interne plus qu'une regression multinomiale sur le
contexte par l'esperance (0,797), jusqu'a 0,365 pour C2 ; seule la condition composite se place entre
l'esperance et le tirage, 0,843, par 0,047 (a35, H2) [ETABLI]. Un agent de langage est une methode par
l'esperance, pas une methode par tirage. Ce qui est different, et c'est le seul point ou le langage fait
qualitativement autre chose : a conditionnement comparable, l'agent gonfle davantage l'ecart entre camps
politiques que toute imputation, 2,16 a 2,83 contre 1,37 a 1,83 (a35, 3) ; il garde les reponses rares, F1 de
0,315 contre 0,247 pour l'appariement sur moyenne predite, la methode standard qui tire une vraie reponse chez
un voisin proche, et 0,03 pour la foret (a35, a29) ; et il vise les bonnes personnes a 73 pour cent du plafond
humain la ou un tirage aveugle est a zero (a29). Le chiffre le plus dur : sur les reponses que moins d'une
personne sur dix donne, la regression, la foret et les voisins par l'esperance font moins bien qu'un tirage au
sort dans le segment ideologie x genre x age de la personne, dans les trois terciles de deductibilite, et sur la
rarete non deductible la regression retrouve 1,45 pour cent des reponses la ou un tirage aveugle dans la
marginale de l'item en retrouve 4,72 (a34, 3) [ETABLI]. Ce n'est pas une maladresse, c'est leur regle de
decision : une modalite que le segment ne donne jamais n'est jamais la plus probable.

Ce qui est desagreable, et qu'il faut porter. Dans le regime facile, une regression regularisee sur les 119
questions deja posees et les 11 demographies bat les six conditions de Stanford sur l'exactitude, 0,7059
contre 0,6839 ; l'imputation multiple en mode est indistinguable de composite sur la dispersion interne, plus
exacte et deux fois moins gonflante sur l'inter ; l'appariement sur moyenne predite conserve 96,3 pour cent de
la diversite humaine contre 89,6 ; sur trois criteres, sept methodes sont non dominees et une seule est un
modele de langage, par 0,004 (a35, 3 et 5) [ETABLI, conditionnement non apparie]. Les regles de Rubin le
disent en prix : remplir un fichier par la reponse la plus probable donne des intervalles qui ratent la vraie
marginale cinq fois sur six, une seule imputation par tirage une fois sur vingt sept (a35, 7). Ce qui sauve le
dossier : quand la famille thematique entiere sort du contexte, la regression perd 6,6 points, deux fois ce que
perdent les voisins, et repasse derriere composite et enquete, 0,6649 contre 0,6775, qui dominent aussi sur la
diversite conservee, 94,8 contre 80,5, et sur la dispersion interne ; seul l'ecart entre groupes reste contre
elles, 2,32 contre 1,52 (a35, 6) [ETABLI, sans bootstrap ni famille]. Le MRP, la post stratification
hierarchique, retrecit volontairement les ecarts entre groupes et n'a aucune dispersion interne, son erreur
etant la plus grande sur les petits sous groupes (Gao et al. 2021, Wang et Gelman 2015, lecture 03).

La position exacte du dossier, en une phrase : dans le regime facile, un jumeau de langage est une methode
d'imputation par l'esperance, dominee par le tirage sur la dispersion et par la regression sur l'exactitude ;
son avantage n'apparait que quand l'information la plus proche manque, et il tient alors sur l'exactitude, la
diversite et les gens rares non deductibles a la fois, au prix d'ecarts entre camps exageres d'un facteur 2. Le
modele de voisinage de Freedman, qui remplace la demographie par le contexte et bat la regression ecologique,
est le pendant statistique de C3 contre C2 (Freedman 1999, lecture 02, L02-11).

### 2.3 Ce que le mecanisme predit et qui n'est pas teste

Si la substitution est une imputation par l'esperance ancree lexicalement, alors une etiquette factice doit
produire un gonflement bien plus faible qu'une vraie etiquette, sinon c'est de la reactivite d'invite, le
placebo d'Ozkan deplacant davantage que la manipulation pertinente, plus 1,49 contre plus 1,13 (lecture 07) [non
teste]. Le R2 apres retrait de la moyenne d'item doit etre le meme avec et sans etiquette pendant que
l'exactitude brute change (lecture 01, test 2) [non teste]. Nos agents doivent etre plus proches de l'agent a
etiquette que des humains sur la distance de Peng, et l'etiquette seule doit egaler la persona complete sur le
milieu et perdre sur les 5 pour cent du bas, ou le tirage la depasse, comme dans les sorties non publiees de
Peng, 0,7644 contre 0,7643 et 0,5165 contre 0,5416 (a36, 6.3) [non teste]. La substitution doit etre presente
dans le socle mais moindre, puisque le budget d'identite l'est deja et que le socle comprime les ecarts ; un
modele plus gros doit l'aggraver si la capacite se met au service de la conformite comme chez les humains
(Kahan et al. 2017, lecture 04) [HYPOTHESE]. Le modele doit connaitre la marginale du GSS qu'il ne sait pas
incarner, ce que la voie « describe » teste en 149 appels (a27) [non teste].

## 3. Ce qui est humain la dedans

### 3.1 La variete des camps

Sur les 149 items du GSS, la dispersion interne du camp de droite vaut 1,122 fois celle de la gauche
[1,100 ; 1,145], le centre est indistinguable de la droite, l'ecart vaut 2,47 sur l'avortement et s'inverse a
0,63 sur la peine de mort ; l'enonce exact est « la gauche est le camp le moins varie » (a30) [ETABLI]. Ce fait
a un homologue publie, l'effet de consensus liberal sur 80 000 personnes et 40 ans (Ondish et Stern 2018,
lecture 05) [PROBABLE, paywall], et surtout un mecanisme simule : les positions de politique publique penchent
a gauche, les etiquettes a droite, et un modele de dynamique de croyances produit alors le consensus liberal
dans 35 populations sur 40 (Brandt et Sleegers 2021, lecture 05) [ETABLI AILLEURS]. Le rapport a37 le mesure
sur nos humains et il explique presque tout : sur les 79 items du GSS auxquels une orientation gauche droite
peut etre donnee, le logarithme du rapport droite sur gauche decroit avec la derive agregee de l'item, pente
moins 2,22 [moins 2,56 ; moins 1,96], R2 0,68, signe predit dans 72 cas sur 79, replique sur Twin (moins 2,07)
et sur la vague 2 ; un temoin qui ne connait que la position moyenne de chaque camp reproduit 1,211 du 1,220
observe et 98 pour cent de la variance item par item, 91 sur les seuls items a plus de deux modalites ou il
peut se tromper ; le rapport residuel a derive nulle vaut 1,040 et ne passe pas Holm (a37, sections 3 et 4)
[ETABLI]. La dispersion interne d'un camp sur un item n'est donc pas une propriete du camp, c'est une
consequence de sa position : la gauche est pres du bord sur les 60 items sur 79 ou l'opinion penche a gauche.
Reserve : le second parametre du modele, l'etiquette penchant a droite, est faux dans nos deux echantillons
(a37) ; et le 1,22 des 79 items orientes ne remplace jamais le 1,12 des 149. L'asymetrie est aussi datee, trois
series placant le croisement entre 2016 et 2020 (Chen et al. 2025, Kozlowski et Murphy 2021, lecture 05).

Ce que la simulation en fait, et c'est desormais la mesure la plus complete du dossier : une loi humaine, un
plancher, et sa deformation sur les memes personnes. Sans etiquette, C3 donne une pente de moins 1,89 contre
moins 2,16 chez les memes humains, p de Holm 1,000 : le modele reproduit la structure (a37, A3) [ETABLI]. Avec
etiquette, v8 porte la pente a moins 12,41, 5,6 fois la valeur humaine, et C2 rend le camp de gauche unanime
sur 31 items sur 79 contre 8 pour C3 et 0 chez les humains ; ces items unanimes sont exactement ceux dont la
derive est la plus a gauche, moins 0,286 contre moins 0,119 en moyenne (a37, section 5) [ETABLI]. Sur Twin,
douze configurations sur quinze redressent la pente au dela de l'humain, de moins 4,2 a moins 25,5 contre
moins 1,96. La simulation ne caricature pas un camp, elle caricature un mecanisme : elle pousse a l'unanimite le
camp du cote du consensus, la ou la loi predit deja le plus de consensus. Warncke fournit la theorie : la ou
l'attachement ideologique symbolique est central, les croyances de masse sont plus coherentes ; « vous etes de
gauche » dans l'invite rend l'etiquette maximalement centrale (Warncke 2025, lecture 05). Les reseaux
d'attitudes des agents sont deux fois plus denses que ceux des humains dans les deux camps (a30, 6.2).

### 3.2 La presentation de soi

La reponse socialement desirable a trois sources, couts materiels, image sociale, image de soi ; un agent n'a
que la troisieme, installee par l'alignement (Bursztyn et al. 2025, Zierahn 2026, lecture 04). Chez les
humains, la desirabilite est un phenomene de comportement verifiable, pas d'attitude : la presence d'un tiers ne
change rien aux attitudes du GSS (Smith 1995, MR086), et les resultats negatifs sur les attitudes politiques
s'accumulent sur 24 pays et 14 000 repondants (Magalhaes et Aarslew, Kaftan, Engelhardt, lecture 04)
[PROBABLE]. Ce qui est massif est ailleurs : 55 a 80 pour cent de l'ecart partisan sur des faits est de
l'expression, payee pour disparaitre (Bullock et al. 2015, lecture 04) ; l'attitude declaree suit « almost
exclusively » la position affichee du parti, et le repondant le nie (Cohen 2003) ; le pole desirable d'un item
evaluatif s'inverse selon le camp et l'annee (Oceno 2025) ; les conservateurs declarent plus d'auto censure
(Gibson et Sutherland 2023, lecture 04).

Ce que la simulation touche : les huit conditions a modele de langage s'ecartent plus des humains sur les
douze items que NORC a mesures sensibles au mode de collecte que sur les 65 temoins, et les cinq predicteurs
statistiques ne le font pas, p de 0,0008 sur le contraste de groupe ; mais aucune condition ne passe seule la
correction, et l'effet est porte par quatre items binaires (a25, a28) [ETABLI en bloc]. Ce qu'elle manque,
doublement. Elle ne reproduit pas le sens : onze differences sur douze ne vont pas vers le pole desirable, C2
est moins presentable que les humains de 0,207 (a25). Et elle ne reproduit pas le jeu social lui meme : 95
humains sur 150 declarent avoir vote la ou l'agent en predit 25 ; 9 humains approuvent un coup porte par la
police contre 71 agents (a25), mais 86 pour cent des « non » humains a cette question absolue approuvent au
moins une situation concrete (Smith 1981, MR010, lecture 04). Les humains du GSS 2021 etaient en choix force
comme les agents (L04-04), et quand une modalite d'echappement est visible jusqu'a 62,8 pour cent la prennent
(MR141) ; l'agent ne dit jamais « je ne sais pas » (2605.16303, lecture 06). Ce qu'il efface n'est pas
l'opinion cachee, c'est le jeu autour de la reponse, dans les deux sens.

### 3.3 L'incoherence genuine

Chez les humains, deux dimensions correlees a 0,30, un axe unique ratant 20,7 pour cent de positions genuines
contre 6,5 de bruit (Treier et Hillygus, Fowler et al., lecture 05). Chez nous, la correlation entre axe
economique et axe social vaut 0,447 a gauche, 0,311 a droite et 0,134 au centre : les moderes ne sont pas au
milieu, leurs deux axes ne communiquent pas (a30, S4) [ETABLI]. Une part de la minorite d'opinion est de
l'instabilite : la propension aux reponses rares correle a moins 0,32 avec la fidelite test retest, et aucune
methode ne reproduit ce lien (a29) ; un humain qui donne une reponse rare a tort le fait surtout parce qu'il est
du genre a repondre rarement, rapport 0,56 (a31). La simulation manque cette couche partout : 19 patrons de
croyances sur 929 contre 340 (Wang et al. 2025, lecture 05) ; coherence interne 0,967 contre 0,872 (a9) ; nos
agents s'ecartent de leur groupe autant que les humains mais pas pour les memes personnes, 0,246 contre 0,895,
du bruit et non de l'heterogeneite (a23). L'adversaire existe : l'audit de 43 modeles conclut que leur
moderation est le resultat net de positions compensatoires, « comme les electeurs moderes » (Aldahoul 2026,
corpus 05) [PROBABLE]. Le trait de « deviance » n'existe pas en psychologie ; seul le conflit de valeurs
existe, mesure en variance conditionnelle (corpus 05).

## 4. Les contradictions du champ, et la variable qui les explique

Le champ contient des resultats qui se contredisent frontalement, et presque toujours une variable de
protocole, jamais nommee dans les resumes, les reconcilie.

Le signe de l'ecart entre groupes. Gonfle chez nous (1,8 a 5,9, a1), chez Chen (mediane 2,3), chez Xie dans
PNAS (R2 du revenu 0,6 simule contre 0,1 reel), chez 2608.03044 apres alignement (2,0), chez Shi et Haupt.
Aplati chez Boelaert, ou GPT-4-Turbo donne la meme distribution aux 687 sous populations du WVS, chez Qin, Li et
Cheng, chez Kim sur le climat, chez 2609.00565. Trois variables cumulatives. Le regime : interroge sur une
distribution de groupe, le modele repond avec sa connaissance, qui est plate ; interroge en tant qu'individu,
avec son stereotype, qui est exagere (Meister, Boelaert, lecture 03). Le groupe nomme ou non dans l'invite :
nomme, le modele le joue et l'exagere ; present seulement dans le materiau d'ajustement, l'alignement rabat
tout vers un centre (lecture 06, C1). La quantite mesuree : un ecart de moyenne a la verite, une distance entre
deux individus de deux groupes et un rapport d'amplitude sont trois choses, et la « diversite » de 2609.00565
additionne inter et intra, verifie dans son code (a26). Toute phrase sans regime est refutable en une ligne.

La dispersion interne, ecrasee ou fabriquee. Ecrasee en texte libre (Wang, Morgenstern et Dickerson ; Zhang,
Xu et Alvero), dans 154 resultats sur 164 chez Peng, de 1,9 a 3,9 fois chez Shi et Haupt. Excessive dans les
distributions fermees de Rennard (plus 0,18 nats), chez Ozkan apres verbalisation (1,37), et dans les sorties
non publiees de Peng ou l'ajustement fin depasse 1 et ou la dispersion croit avec l'information, 0,446 vide,
0,575 etiquette, 0,634 persona complete (a36). Deux variables : le format de sortie, texte libre contre
distribution fermee (lecture 01), et le niveau d'agregation, une entropie de population pouvant monter pendant
que chaque cellule devient unanime (lecture 02, C.2). « Les modeles ecrasent la variance » est faux en general.

Le socle, meilleur ou pire. Meilleur chez 2608.03044, Sorensen, Padmakumar ; pas meilleur chez 2607.25292 ni
chez 2605.27878. La variable est le cote du referent humain ou tombe l'erreur, le socle sur disperse et
l'aligne sous disperse, les travaux qui declarent le socle vainqueur mesurant une distance a un uniforme ou a
une cible synthetique, pas a une population (lecture 06, C3) ; s'y ajoute le format d'invite.

Qui garde les categories rares. L'agent chez nous, facteur 11 contre la foret (a29) ; la regression chez von
der Heyde, F1 de 0,58 contre 0,33 sur le vote AfD, l'ecart se creusant avec la rarete (lecture 03). Le test
qui pouvait faire tomber la these est fait : sur les cellules ou aucune autre personne du segment n'a donne la
reponse, les agents riches retrouvent 21,8 pour cent des raretes, la regression 1,45, la foret 0,21, et les
huit conditions a modele de langage ont un avantage positif passant Holm (a34, H2) [ETABLI]. Le rapport est de
15 contre 1 sur la rarete indeductible contre 3,3 sur la deductible ; mais en ecart absolu l'avantage y est le
plus petit, plus 0,204 contre plus 0,281, et sur le F1 l'ecart est plat (a34, H3) [ETABLI]. Les variables qui
restent sont donc chez eux, une regression evaluee en echantillon sur un vote de parti deductible de
l'identification presente dans l'invite, et chez nous le comparateur : contre l'imputation par tirage, le
facteur sur le F1 est 1,27 (a35). Deux reserves : a34 n'est pas preenregistre, et aucune de ses partitions n'est
a la fois non circulaire pour le plancher et non tautologique pour la regression (a34, 9).

Le stereotype, caricature ou artefact de bruit. Les personas contre stereotypiques coutent 9,7 points de
pilotabilite (Liu, Diab et Fried 2024, lecture 05) ; Rennard ne trouve aucune penalite une fois soustrait le
bruit d'echantillonnage des petites cellules et avertit que tout audit sans ce controle « rediscover[s] a
spurious counter-stereotypical effect » (lecture 01, contradiction 3). La variable est le plancher de bruit de
cellule ; a34 le paye a moitie, par tercile, et il reste a le payer sur les quantites de a29 et a31.

L'etiquette aide ou nuit. Elle aide sur les items ou les humains sont partages et nuit ou ils convergent
(2609.02526, lecture 02) ; conditionner sur un groupe degrade tous les modeles de SimBench, le plus sur la
religion et la politique (lecture 01, L1.08). La variable est la dispersion humaine de l'item, dont le plafond
explicable varie d'un facteur cent (Hu et Collier), et le type de tache : R2 de 0,0004 pour le role sur des
items a bonne reponse, d de 0,55 sur des preferences (2511.15573, lecture 02).

La desirabilite du modele. GPT-4 derive vers la reponse desirable quand il se croit evalue (Salecha 2024), les
societes simulees sont des « illusions utopiques » (2510.21180, lecture 04) ; a25 mesure l'inverse. La
variable : conversation libre contre items fermes avec referent apparie, et attitude contre comportement ; sur
les attitudes, l'absence de direction chez nous se range avec la litterature humaine (lecture 04).

L'asymetrie droite gauche. Grossmann et Hopkins predisent des republicains plus homogenes ; Ondish, Brandt,
Cely mesurent l'inverse ; Luders voit une droite etalee, Chen une droite plus dense sauf en 2020. Quatre
variables : le niveau, l'etiquette et le principe general contre les positions d'items, ce que notre 1,122 par
ideologie contre 1,094 par parti confirme (lecture 05) ; l'annee ; le domaine, 1,29 sur dix items politiques de
Twin contre 0,988 sur 275 items de personnalite (a30) ; et surtout la position, qui explique 98 pour cent de
l'asymetrie item par item (a37) : les deux camps sont pareils, c'est l'opinion qui penche.

L'ecrasement, propre au langage ou a la prediction. Ku dit tout predicteur ; a35 le confirme, sept conditions
sur huit ecrasant plus que la regression ; a25 et a28 disent que seuls les modeles de langage devient sur les
items sensibles au mode ; a28 test 2 dit que seuls les predicteurs statistiques ecrasent selectivement. La
variable est la quantite : le niveau de dispersion est une propriete de tout predicteur, le lieu de la
deviation et la queue de distribution separent les familles, et l'ecart entre groupes est le seul terme ou le
langage fait qualitativement autre chose (a35, 3).

Le contexte individuel, utile ou pas. Deux heures d'entretien valent 9,5 points chez Stanford (a14) ; Peng
trouve 0,748 contre 0,746 pour l'etiquette seule ; Ahn trouve que le LLM perd contre la moyenne des autres
repondants. La variable est ce qui est mesure : sur le milieu rien ne bouge, toute la valeur de l'information
individuelle est dans les queues, 0,5416 contre 0,5165 (a36, 6.3), et la ou l'information proche manque (a35).

| contradiction | variable qui l'explique |
|---|---|
| ecart entre groupes gonfle ou aplati | regime persona contre distribution ; groupe nomme ou non ; quantite mesuree |
| dispersion interne ecrasee ou excessive | texte libre contre choix ferme ; entropie de population contre variance de cellule |
| socle meilleur ou pire | cote du referent humain ; prefixe d'assistant |
| qui garde les rares | rapport contre ecart absolu ; evaluation en echantillon ; esperance contre tirage ; pas la deductibilite |
| caricature ou bruit | plancher de bruit des petites cellules |
| etiquette utile ou nuisible | dispersion humaine de l'item ; tache a bonne reponse ou non |
| societe presentable ou non | conversation libre contre items apparies ; comportement contre attitude ; pole par camp |
| droite ou gauche plus variee | etiquette contre items ; annee ; domaine |
| contexte utile ou non | milieu contre queues ; regime facile contre question jamais posee |

## 5. Ce qui est deja pris, et ce qui est libre

Sans complaisance, parce que trois revendications sont tombees en une journee. Qin, Li et Cheng mesurent les
deux termes contre 594 humains (corpus 02). Xie et al. publient dans PNAS l'entropie ecrasee et le V de Cramer
gonfle sur quinze modeles et sept enquetes (lecture 03). 2608.03044 publie le facteur 2 apres alignement, sans
intra, sans intervalle, sans code (a26). Rennard et Xypolopoulos publient le budget d'identite sur des cellules,
jamais des personnes (lecture 01). Ahn, Mao et Lee publient exactitude, dispersion et planchers dans le meme
tableau, sans segmentation (lecture 03). Ozkan publie la restitution contre l'effondrement avec placebo, sans
corpus ni baseline (lecture 07). Zhang, Xu et Alvero mesurent que la part effacee est la part denigrante, sur
trois questions ouvertes de 187 a 223 reponses (a36, 9). Peng et al.
mesurent sur Twin-2K-500 que les jumeaux a 500 reponses sont plus proches de l'agent a etiquette (0,132) que des
humains (0,252), « overly shrunk », ecart type inferieur dans 154 resultats sur 164, une sous etude avec test de
Levene et interaction d'ideologie, deux baselines non LLM ; mais aucune ablation de l'etiquette, aucun plancher
de retest alors que la vague 4 a ete consommee comme entree, aucun rappel des rares, et une mesure de queue dans
leur depot que l'article ne publie pas (a36). LifeMem corrige la dispersion interne sans mesurer l'inter ; PPA
corrige 21 pour cent de l'erreur sans mesurer l'intra ni le cout individuel (a27). Van Buuren a ecrit le
theoreme avant tout le monde, et aucun des 330 papiers du corpus ne le cite (lecture 02, E.4).

Ce qui est libre, avec la reserve que la recherche par absence a deja cede quatre fois. L'ablation de
l'etiquette a modele, personnes, questions et traces constants : personne (a26, a36). Le plancher de bruit
humain par reinterrogation des memes personnes, pose en regard de chaque metrique : personne, et c'est le
differentiateur numero un (a36, 3.2). Les deux termes comme rapports a un referent humain sur les memes
personnes, relies par une identite de total : personne. Le modele de langage mis dans le tableau des methodes
d'imputation, avec les regles de Rubin, sous le nom que la statistique lui donne : personne, et Xie le declare
manquant dans PNAS (a35). Le fait qu'aucun predicteur par l'esperance ne batte un tirage au sort dans le segment
de la personne sur les reponses rares, et que l'avantage du langage tienne la ou la rarete n'est pas deductible
(a34) : personne, et cela ne parle meme pas d'IA. L'unanimite d'un camp avec etiquette (a30), l'attribution de
la fausse rarete au groupe restreinte aux conditions qui n'ont que l'etiquette (a31, a34), le contraste
sensible contre temoin decompose en inter et intra avec plancher (lecture 02, E.1), la loi de Brandt et
Sleegers mesuree item par item chez les humains puis deformee par une population simulee sur les memes
personnes (a37), le comptage du questionnaire contre la statistique de groupe dans les corpus (lecture 07) :
personne. Le 1,12 lui meme est une replication de l'effet de consensus liberal, pas une decouverte.

Ce que popsim peut revendiquer, en trois phrases faites pour survivre a un relecteur qui a tout lu. Une, a
modele, temperature, personnes et questions constants, la seule presence de l'etiquette ideologique fait passer
le gonflement des ecarts entre groupes de 0,73 a 8,16, la dispersion interne de 0,681 a 0,365, et le rapport
groupe sur personne des fausses raretes de 0,44 a 4,45, la ou les memes humains reinterroges sont a 0,56 ; ce
rapport survit sur les seules raretes que le groupe ne predit pas, et les agents riches y placent leurs erreurs
par la personne : l'etiquette est la cause mesuree de la substitution, pas l'alignement, pas le manque de
contexte, pas le langage. Deux, mis sur les memes cellules que vingt methodes d'imputation, un agent de langage
est une methode par l'esperance, dominee dans le regime facile par la regression sur l'exactitude et par
l'imputation par tirage sur la dispersion ; son avantage propre apparait quand l'information la plus proche
manque, ou il domine sur l'exactitude, la diversite et les reponses rares indeductibles, une sur cinq contre une
sur soixante dix pour la regression, et il le paye en exagerant les ecarts entre camps d'un facteur 2 jusqu'a
rendre le camp le moins varie unanime. Trois, chaque quantite est normalisee par un plancher obtenu en
reinterrogeant les memes personnes deux semaines plus tard, ce qu'aucun travail concurrent ne possede.

## 6. Ce qu'on peut essayer de debloquer

Huit verrous, classes par rapport gain sur cout. Un appel de modele coute environ une seconde ; une condition
complete vaut 22 350 appels, soit deux a cinq heures (a5, a23).

Verrou 1, le regime severe, mesure proprement. Pourquoi : depuis a35, c'est le seul regime ou la simulation par
langage domine une statistique d'enquete correctement outillee, et c'est le moins bien mesure du dossier, des
estimations ponctuelles sur 58 items sans bootstrap ni famille (a35, 11). Ce qui le tient ferme : l'ecart de 1,3
point entre composite et la regression privee de famille n'est pas teste et peut ne pas survivre au
reechantillonnage des items. L'experience : une famille ecrite avant, deposee ; un bootstrap sur personnes et
sur items ; les memes methodes sur Twin-2K-500 ; et la mesure conjointe de l'exactitude, de la diversite et du
rappel des rares indeductibles dans ce regime. Cout : une soiree, zero appel. Gain : la revendication deux de la
section 5 tient ou tombe, et avec elle la these.

Verrou 2, le plancher de bruit de cellule, a finir. Pourquoi : tout le resultat sur les minorites porte sur de
petites cellules, et Rennard demontre que l'absence de ce controle fabrique un effet la ou il n'y en a pas
(lecture 01, test 5). Ce qui est fait : a34 soustrait un plancher par tercile, et l'exces des agents reste
positif partout quand celui des predicteurs statistiques est negatif partout. Ce qui le tient ferme : le
plancher et le score de deductibilite y sont le meme calcul sur une partition, et la confiance de l'adversaire
sur l'autre ; a29 et a31 ne sont pas floores ; le tercile « indeductible » est une absence parmi neuf personnes
en mediane, en partie un zero d'echantillonnage (Garrido et al. 2020, lecture 03) ; a34 n'est pas
preenregistre. L'experience : une partition tierce sur un predicteur qui ne soit ni la regression ni une
frequence de segment ; le plancher a deux moities applique a a29 et a31 ; le taux de change de Garrido ; une
famille deposee avant. Cout : une soiree, zero appel. Gain : la these des rares survit a sa contre expertise ou
tombe avant qu'un relecteur la fasse tomber.

Verrou 3, la desirabilite indexee par camp, et l'ampleur continue par item. Pourquoi : a25 fixe un pole
desirable unique par item, et Oceno montre qu'il s'inverse selon le camp ; une direction nulle en moyenne peut
cacher deux directions opposees (lecture 04, T5). Ce qui le tient ferme : l'ampleur par item existe dans MR099,
MR141 et l'atlas, pas dans la note NORC employee. L'experience : le sens de a25 recalcule par camp ; le score
fabrique remplace par les ampleurs mesurees ; l'ecart agent contre humain correle a la part de modalite
volontaire de MR141 ; polabuse rejuge contre le profil situationnel. Cout : une demi journee, zero appel. Gain :
« la simulation devie la ou les humains se surveillent » redevient un resultat par condition, ou est enterre.

Verrou 4, le placebo d'etiquette. Pourquoi : tout l'effet de l'etiquette repose sur une manipulation
pertinente, et Ozkan montre qu'une manipulation non pertinente peut deplacer davantage (lecture 07, T6). Si une
etiquette permutee entre personnes produit le meme gonflement, le meme rapport groupe sur personne et la meme
unanimite, le mecanisme est de la reactivite d'invite. Ce qui le tient ferme : une condition de collecte manque.
Cout : une condition, deux a cinq heures. Gain : la revendication une devient presque inattaquable.

Verrou 5, a quelle etape la substitution apparait, teste a invite fixe. Pourquoi : c'est la question ouverte de
l'arbitrage, et le champ la pose mal en cherchant un vainqueur entre socle et aligne alors que les deux
manquent le referent de cotes opposes (lecture 06, C3). Ce qui le tient ferme : le format d'invite vaut la
moitie de l'ecart base contre instruct (a27) ; la paire (Qwen3-4B-Base, Instruct-2507) n'est pas appariee, le
successeur direct est Qwen3-4B (a27, 4.4) ; une quantification tierce peut mesurer le format et non
l'intervention (2607.17427, lecture 06). L'experience, dans l'ordre : E2, le meme modele instruit en completion
a trois exemples contre son gabarit de conversation ; puis E1, le socle et le successeur apparie, probabilites
lues, taux de sorties hors nomenclature publie des deux cotes ; surveiller la valeur H2b et son exces sur le
temoin aveugle, non le rapport groupe sur personne, non identifiable sous 150 personnes (a33, 4), plus le
gonflement et l'unanimite. Predictions ecrites d'avance : le budget d'identite dit que la substitution est deja
dans le socle, Zierahn que la desirabilite apparait a l'alignement, 2608.03044 que le socle comprime les
ecarts. Cout : deux a trois conditions, une nuit. Gain : la phrase a defendre gagne son etage.

Verrou 6, le mecanisme de Brandt et Sleegers, ce qui reste apres a37. Pourquoi : la loi humaine et sa
deformation sont mesurees, mais trois choses les fragilisent. L'orientation des 79 items est la notre, 14 de
niveau hypothese, et le second codeur est construit sur les memes donnees ; la derive est une position a un
instant, pas un mouvement, ce que le mot suppose ; et le second parametre du modele est faux chez nous sans que
l'on sache ce que cela coute (a37, 9). Une question de fond s'y ajoute : si la mesure d'Ondish et Stern est
elle aussi une fonction de la position, quarante ans de resultat tiennent a un fait arithmetique (a37, question
1). L'experience : une orientation prise dans un codebook publie ; la pente sur l'ANES de 2000 a 2020 pour
savoir si moins 2,2 est une constante ou un chiffre d'epoque ; la simulation de Brandt et Sleegers refaite
avec le signe d'etiquette observe ; et une mesure de consensus orthogonale a la position. Cout : une journee,
zero appel, l'ANES a recuperer. Gain : la premiere loi du dossier gagne sa validite externe.

Verrou 7, le R2 demoyenne avec et sans etiquette, et les criteres de Peng. Pourquoi : c'est le test qui dit,
sans le mot « stereotype », si l'etiquette n'ajoute que de la moyenne de groupe (lecture 01, test 2), et Peng a
pose ses trois distances et ses trois tranches comme standard de fait (a36). L'experience : le R2 apres retrait
de la moyenne d'item, divise par la fidelite de la vague 2, pour C2, C3 et les six conditions ; les distances a
l'agent a etiquette, a l'agent vide, aux humains ; les tranches bas 5, milieu 90, haut 5. Cout : une soiree,
zero appel. Gain : comparabilite ligne a ligne avec les deux papiers les plus proches.

Verrou 8, la voie « describe » et le comptage de corpus item par item. Pourquoi : si le modele sait decrire la
marginale du GSS qu'il ne sait pas incarner, le defaut est une incapacite de restitution et non une ignorance,
et le comptage donne une variable explicative par item (a27, lecture 07). L'experience : 149 appels de
description, le compte infini-gram des 149 libelles, la correlation entre l'avantage du modele et la presence
dans le corpus. Cout : une minute d'appels, une soiree. Gain : capacite contre propension sur nos sorties.

## 7. La these, dans sa forme la plus forte et la plus honnete

Resume, tel qu'il pourrait ouvrir un preprint.

Les populations simulees par modele de langage servent deja a estimer des opinions, et la note d'exactitude qui
les certifie ne voit pas leur structure. Nous montrons, sur 1 052 participants de l'enquete sociale americaine
reinterroges deux semaines plus tard, sur 2 058 participants du panel Twin-2K-500 et sur 300 personnes simulees
par un modele ouvert de 4 milliards de parametres, qu'une societe simulee a partir d'etiquettes remplace chaque
personne par l'esperance de son groupe. Ce remplacement a deux faces mesurees ensemble et normalisees par le
meme plancher humain : les ecarts entre groupes sont gonfles d'un facteur 1,8 a 5,9 et la dispersion interne
ramenee a 0,64 a 0,89 de celle des humains, quand les memes humains reinterroges tombent a un demi pour cent du
point neutre. C'est le comportement que la statistique attend d'une imputation par l'esperance depuis Little et
Rubin, et nous le verifions sur les memes cellules : passer de la reponse la plus probable au tirage, a modele
constant, coute huit a dix points d'exactitude et rend la dispersion. Mis dans le tableau de vingt methodes
d'imputation, un jumeau de langage est une methode par l'esperance, et dans le regime ou les questions voisines
ont deja ete posees il est domine, par une regression sur l'exactitude et par l'appariement sur moyenne predite
sur la dispersion. Son avantage propre apparait quand l'information la plus proche manque : il domine alors sur
l'exactitude, la diversite conservee et les reponses rares que le groupe ne predit pas, une sur cinq retrouvee
contre une sur soixante dix pour la regression, la ou tout predicteur par l'esperance fait moins bien qu'un
tirage au sort dans le segment de la personne. Il le paye en exagerant les ecarts entre camps d'un facteur 2.

La cause de cette exageration n'est ni le tirage, qui ne rend que 1,4 point sur 34,6, ni le manque de contexte,
dont l'ablation a personne constante baisse l'exactitude sans deplacer l'erreur vers le groupe, ni le langage,
puisque sur la rarete indeductible les agents riches placent leurs erreurs par la personne comme les humains ;
c'est l'etiquette elle meme. A modele, temperature, personnes et questions constants, sa seule presence fait
passer le gonflement de 0,73 a 8,16, la dispersion interne de 0,681 a 0,365, et deplace l'attribution des
reponses rares du regime humain, ou la personne pese plus que le groupe, au regime statistique, ou le groupe
pese jusqu'a huit fois plus. Le meme geste deforme une loi humaine mesuree : chez les humains, la variete
relative d'un camp sur un item suit la derive agregee de cet item avec une pente de moins 2,2, ce qui est
l'effet de consensus liberal ramene a un fait de position ; sans etiquette la simulation reproduit cette pente,
avec etiquette elle la porte a moins 12,4 et rend le camp du cote du consensus unanime sur 12 a 31 items sur 79.

Ce que la these ne dit pas. Ni que les modeles de langage font pire que la statistique ni mieux : ils sont une
methode d'imputation parmi d'autres, avec un profil propre. Ni que la part effacee est la part que les gens
cachent : la simulation devie la ou les humains se surveillent, en bloc et non condition par condition, et pas
dans le sens de la surveillance. Ni a quelle etape, socle ou alignement, la substitution apparait, ni si un
modele plus gros la corrige. Rien hors du choix ferme a modalites exclusives, hors de l'axe ideologique, qui est
une attitude declaree et non une demographie, et hors des Etats Unis de 2024.

L'adversaire principal tient en trois objections. Le resultat des rares est du bruit de petites cellules,
controle a moitie par un plancher circulaire dans un rapport non preenregistre, et l'avantage du langage dans le
regime severe est une estimation ponctuelle sans intervalle. L'effet de l'etiquette est un effet de formulation
d'invite sur un petit modele, non compare aux invites de Stanford et sans placebo. Et « imputation par
l'esperance ancree » est un renommage de Peng, Xie et Rennard. La reponse aux deux premieres est la section 6 ;
la reponse a la troisieme est que ces trois travaux n'ont ni l'ablation, ni le plancher, ni le tableau des
imputations, et que ces trois choses sont la seule facon de transformer une ressemblance en cause et une
accusation en position.

## 8. Ce que je ne sais pas

Je ne sais pas si les corpus reels de Llama, Qwen ou gpt-oss ressemblent aux corpus ouverts comptes. Je ne sais
pas si l'avantage du regime severe survit a un bootstrap sur les items, ni si la mesure d'Ondish et Stern est,
comme la notre, une fonction de la position. Je ne sais pas si l'absence de gonflement sans etiquette est un
fait sur les modeles ou une incapacite d'un modele de 4 milliards de parametres, ni quelle part de l'ecart C2
contre C3 vient de la formulation des invites, jamais comparee a celle de Stanford. Je ne sais pas si le
tercile « indeductible » de a34 est un zero structurel ou un zero d'echantillonnage sur neuf personnes. Je ne
sais pas comment nommer, avec un psychologue, ce qu'une personne fait quand elle repond rarement, ni si
« stereotype » est tenable pour ce qu'un estimateur bayesien correct fait aussi sans autre information. Je ne
sais pas si la verite terrain de Stanford a ete collectee en ligne, ce qui change le signe de la section sur la
presentation de soi. Je n'ai pas lu Ondish et Stern, Cely, Robinson, King, Meng ni le SSRN qui transpose Kuran
aux agents generatifs. Et je ne sais pas si la recherche par absence tient : elle a cede quatre fois aujourd'hui.

## 9. Addendum de la nuit du 8 au 9 septembre

Quatre rapports sont arrives apres la redaction du corps : a38 (version continue et par camp du test des items
sensibles), a39 (tranches de Peng rejouees), a41 (regime severe apparie) et la veille de l'ete 2026, lecture 08
(a40). Deux changent la these. Le corps ci dessus n'est pas modifie ; cet addendum dit, paragraphe par
paragraphe, ce qui est remplace. Sauf mention, tout ce qui suit est [ETABLI] ; a41 signale, comme a34, qu'il
n'est pas preenregistre.

### 9.1 Ce qui tombe et ce qui le remplace, section 3.2 et section 7

Tombe : « la simulation devie la ou les humains se surveillent », y compris sous sa forme en bloc. La version
continue, avec les ampleurs de mode reellement publiees par NORC et l'atlas, 21 items dont 16 de depenses, ne
donne aucune correlation pour aucune methode, et le contraste de groupe passe de plus 0,356 (p 0,0009) sur le
score fabrique de a28 a plus 0,176 (p 0,047) puis disparait quand la couverture s'elargit (a38, section 2). Le
motif de a25 et a28 est entier sur les attitudes, plus 0,059 avec p 0,0012, et nul sur les comportements
declares, plus 0,008 avec p 0,77 : c'est l'inverse de ce que la litterature humaine predit, la desirabilite
mesuree contre verite terrain etant un phenomene de comportement verifiable (a38, section 3). La formulation
qui survit est « la simulation devie la ou NORC a mesure que la distribution bouge avec le mode, et c'est un
phenomene d'attitude » ; le confondant de la modalite d'echappement (MR141) est mesure et ne va pas dans le
sens de l'objection.

Remplacant, et c'est le premier resultat du theme qui passe une correction declaree d'avance : la caricature
par camp. Sur 29 items ideologiques a pole d'endogroupe documente, on mesure de combien une methode reproduit
l'ecart gauche moins droite humain sur le score de desirabilite. Les memes humains reinterroges sont a 0,98 ;
les trois predicteurs statistiques qui recoivent l'etiquette sont a 1,01, 1,03 et 1,24 ; les quatre conditions
riches de Stanford et C2 exagerent l'ecart d'un facteur 1,8 a 3,2, C2 a 1,62 [1,06 ; 2,10] contre C3 sans
etiquette a 0,52 [0,20 ; 0,82], intervalles disjoints ; huit tests passent Holm sur la famille de 52 (a38,
section 4). Reserve a porter : v6 et v7, qui ont une etiquette demographique mais pas l'ideologie ni le parti
(a19), sous reproduisent l'ecart, 0,29 et 0,39 ; la cause est donc l'etiquette ideologique, pas l'etiquette en
general, ce que a39 confirme sur la queue (9.2). Dans la section 7, la phrase « la simulation devie la ou les
humains se surveillent, en bloc et non condition par condition » est a remplacer par cette caricature par camp.

### 9.2 Ce que a39 ajoute a la section 4 et a la revendication trois

Les tranches de Peng se reproduisent en forme : le retard sur le plancher humain est 1,2 a 4,0 fois plus grand
sur les 5 pour cent du bas que sur le milieu, et le classement des methodes au milieu ne dit rien de la queue,
correlation de rang plus 0,007. Sur la queue categorielle, un tirage uniforme bat v8, l'agent a etiquette
ideologique, de 12,6 points (0,186 contre 0,060) ; v6, l'agent demographique sans ideologie, est la seule
methode significativement au dessus du hasard, plus 0,046 ; la statistique par l'esperance tombe a 0,2 a 2,2
pour cent ; sur l'ablation propre C2 contre C3, le milieu ordinal est egal, moins 0,007 [moins 0,017 ; 0,004]
(a39, sections 1 et 2). Deux conditions riches ne depassent pas demontrablement le hasard sur la queue, et une
lui est inferieure : « les conditions riches restent au dessus » ne s'ecrit plus. Le point qui compte pour la
section 4, contradiction « dispersion interne » : le rapport d'ecarts types total que Peng publie donne le
meme chiffre a C2 et C3, 0,771 et 0,781, pour des decompositions opposees, 1,96 contre 0,75 entre camps et
0,50 contre 0,79 a l'interieur, avec un plancher humain a 0,999, 1,033 et 0,997 (a39, section 3). La mesure
standard est aveugle a la distorsion ; la revendication trois de la section 5 cesse d'etre « nous ajoutons une
decomposition » et devient « la mesure publiee ne peut pas voir l'effet ».

### 9.3 Ce que a41 retire a la section 5, phrase deux, et a la section 7, premier paragraphe

La phrase « son avantage propre apparait quand l'information la plus proche manque, ou il domine sur
l'exactitude, la diversite et les reponses rares indeductibles » n'est pas etablie. Non apparie, l'avantage
d'exactitude de composite sur la regression privee de famille existe et est decidable, plus 1,27 point ; mais
par la condition appariee que le papier de Stanford publie lui meme, retrait du bloc entier au lieu du seul
item, soit 3,93 points d'exactitude brute, composite tombe derriere E1 (moins 0,027) et derriere B2, et il
suffit de 1,27 point de decalage pour retourner la comparaison ; par mesure directe, C3F, nos agents prives de
la famille sur 60 personnes, perd contre les six methodes statistiques restreintes aux memes personnes, de
moins 4,3 a moins 13,4 points, Holm 0,0015, et perd sur la structure, 59 contre 98 pour cent de diversite
conservee (a41, sections 4 et 5) [transposition PROBABLE, mesure directe ETABLIE sur 4 milliards de
parametres]. Contre les quatre imputations par tirage, l'agent est plus loin de la dispersion humaine, de
0,076 a 0,135, dans le regime severe comme dans le facile : un agent de langage reste une methode par
l'esperance quand la question devient nouvelle. Ce qui reste debout est le rappel des minorites, 0,425 contre
0,229 pour l'appariement sur moyenne predite prive de famille, et 0,282 contre 0,138 sur le tercile non
deductible ou B2 et la foret sont exactement a zero ; et il reste debout parce qu'aucune des deux comparaisons
appariees ne peut l'atteindre, pas parce qu'il les a passees (a41, section 7). La phrase de a35 « aucune
methode statistique ne tient quand la question n'a jamais ete posee » est trop forte : l'appariement sur
moyenne predite ne perd rien de sa structure dans le regime severe, seulement son exactitude.

La revendication deux de la section 5 se reecrit ainsi : compare equitablement, un jumeau de langage est une
imputation par l'esperance, dominee par les imputations par tirage sur la structure dans les deux regimes
mesures et par la regression sur l'exactitude des que la comparaison est appariee ; son seul avantage mesure,
les gens rares que le segment ne permet pas de deviner, attend une comparaison appariee ; l'etiquette
ideologique est la cause mesuree de sa caricature des groupes, facteur 1,62 contre 0,52.

### 9.4 Ce que la veille ajoute a la section 5

Yuan, « Cultural Bias Without a Cultural Self » (2607.02368, lecture 08, 1.1), publie le mecanisme de la these
avec un generateur nul : « the cultural signal is a group template, not a property of any instance », la
separation des personas passant de 94,7 pour cent en ordre fixe au hasard en ordre aleatoire, et un tirage
conditionnellement independant sans structure latente reproduisant tout le motif, 97,2 / 57,6 / 83,2 contre
94,6 / 55,2 / 83,7 pour GPT-4o [ETABLI AILLEURS]. L'anteriorite du mecanisme est desormais a lui ; ce qui reste
a nous est le meme mecanisme sur des reponses d'enquete, avec des personnes reelles en face, un plancher de
reinterrogation et les reponses rares. Li et al. (2608.24912) retablissent « la simulation rend une societe
presentable » sur trois axes nommes, desirabilite sociale, prosocialite, aversion au dommage, ou une persona
malveillante ne peut plus passer sous la reference humaine ; la variable qui reconcilie leur resultat et a25
est le decoupage des items, unidirectionnel sur les axes que l'alignement vise, bidirectionnel ailleurs. Holtdirk
et al. (2606.09351) montrent que l'imputation par LLM bat MICE PMM et MICE Forest sur l'erreur de coefficient,
0,033 contre 0,068 ; la variable est la quantite notee, exactitude de cellule contre erreur de coefficient, et
« nos agents sont battus par une regression » ne porte que sur la premiere. ACE-Align (2601.12962) nomme
Stereotyping et Erasure ce que le dossier appelle gonflement et ecrasement : a citer. Enfin trois planchers
humains existent maintenant, reinterrogation chez Ahn, deux moities d'echantillon chez Cai, ligne humaine chez
Yu ; la phrase « aucun plancher publie » doit nommer la quantite, le notre restant le seul par reinterrogation
des memes personnes applique a un partage inter et intra.

### 9.5 Les verrous, reclasses

Un, la comparaison appariee du rappel des minorites, seul critere debout et seul jamais teste a armes egales :
soit un run en regime severe, famille retiree de l'invite, sur un modele serieux, gpt-oss-20b deja installe,
une nuit, soit le fichier de la condition « retrait par bloc » du paquet OSF de Stanford s'il existe, une heure
de recherche que deux rapports ont signalee sans la faire, plus les 90 personnes manquantes de C3F ; famille
declaree avant, avec le rappel du tercile non deductible comme quantite primaire. Deux, le placebo d'etiquette,
une condition, inchange. Trois, le generateur nul de Yuan sur toute notre chaine de mesure, en cours (a44), et
sa perturbation d'ordre : si le gonflement de 8,16 s'effondre sous ordre aleatoire et revient sous
realignement, la these est confirmee par son propre criterium, une nuit courte. Quatre, le plancher de bruit
de cellule avec partition tierce et le test de permutation de personas d'Ahn, zero appel. Cinq, l'etape
d'apparition, E2 puis E1, avec les 67 paires socle et post entraine de Plisiecki (2607.20082) comme
dispositif ; Li localise deja le biais de bienveillance au post entrainement. Six, l'anomalie v6 et v7 et le
controle par identification partisane sur le facteur d'amplification, une heure sur les traces. Sept, la
desirabilite par camp sur Twin et la jonction entre les items ou le camp de gauche simule s'ecrase et les axes
de Li. Huit, le R2 demoyenne, la voie « describe » et les tranches sur Twin, zero appel.

### 9.6 La these, reecrite apres ces quatre rapports

Une societe simulee a partir d'etiquettes remplace chaque personne par l'esperance de son groupe, et c'est le
comportement d'une imputation par l'esperance, verifie sur les memes cellules : compare equitablement a vingt
methodes d'imputation, dans le regime facile comme dans le regime ou l'information la plus proche manque, un
jumeau de langage est domine par les imputations par tirage sur la structure et par la regression sur
l'exactitude. Ce qu'il fait d'autre est mesure et n'est pas encore compare a armes egales : il retrouve deux
fois plus de reponses rares que la meilleure imputation par tirage, quatre fois plus quand la rarete n'est pas
deductible du segment, et un tirage uniforme le bat sur la queue des que l'etiquette ideologique est dans
l'invite. La cause de sa caricature des groupes est cette etiquette, mesuree a modele, personnes et questions
constants : elle fait passer le facteur d'amplification de l'ecart entre camps de 0,52 a 1,62 quand humains et
statistiques sont a 1, deforme la loi humaine de consensus de moins 2,2 a moins 12,4, et rend le camp du cote
du consensus unanime. La mesure standard du retrecissement ne voit rien de cela. L'adversaire principal est
desormais double : Yuan, qui a publie le mecanisme avec un generateur nul, et la comparaison appariee du rappel
des minorites, qui n'existe pas encore et qui peut faire tomber la derniere phrase.

## 10. Addendum final, 9 septembre

Trois rapports preenregistres avant calcul, a42 (plancher de bruit de cellule), a43 (R2 demoyenne et mesures de
Ahn et Peng) et a44 (generateur nul de Yuan), sont arrives apres la section 9. Le troisieme change la nature des
chiffres qui portent le dossier depuis a1. Le corps et la section 9 ne sont pas modifies ; ce qui est remplace
est cite. Tout ce qui suit est [ETABLI], sauf mention.

### 10.1 a42 : l'objection du bruit de cellule tombe, et l'instrument des terciles avec elle

Sur les raretes que la personne redonne a l'identique deux semaines plus tard, 54,8 pour cent des reponses
rares, donc sur de l'heterogeneite verifiee et non sur du bruit de reponse, composite retrouve 40,8 pour cent
des reponses rares contre 8,0 pour la regression et 2,2 pour la foret, pour un plancher de 10,9 obtenu par un
tirage au sort dans le segment ideologie x genre x age ; exces plus 0,289 [0,267 ; 0,311], et l'avantage est
plus grand sur les raretes stables que sur les instables, plus 0,174, Holm 0,0068 (a42, sections 3 et 4). La
premiere objection de la section 7 est levee sur ses trois griefs, et le preenregistrement a fait deux
predictions fausses, ce qui prouve qu'il a ete ecrit avant. Deux corrections en decoulent. Une partition placebo
de neuf groupes tires au hasard reproduit trait pour trait le gradient de deductibilite de a34, ecart median
0,016 : un tercile de frequence de segment est d'abord un tercile de frequence d'item, et toute formulation en
« rarete deductible », y compris « quatre fois plus quand la rarete n'est pas deductible » en 9.3 et 9.6, est
retiree ; les rappels de a34 restent justes, leur interpretation tombe (a42, section 5). Et l'appariement sur
moyenne predite bat le plancher de segment, plus 0,150, plus que quatre conditions de Stanford sur six : la
phrase juste nomme les predicteurs par l'esperance sur demographies, pas « tout predicteur » (a42, section 3).
L'ablation donne sa cinquieme mesure : sur les raretes stables du run local, C3 est a plus 0,162 au dessus du
plancher de son segment, C2 a plus 0,033, non distinguable d'un tirage au sort dans le segment (a42, section 6).
« Une sur cinq contre une sur soixante dix » devient « deux sur cinq contre une sur douze ».

### 10.2 a43 : la mesure de Ahn se reproduit, et le remplacement est propre au conditionnement

A conditionnement egal a celui de Ahn, persona fixe sans reponse de la personne, nos agents retrouvent son
chiffre : 1,10 a 5,47 pour cent de variance individuelle apres retrait de la moyenne d'item, contre 3,05 chez
lui, sur un plafond humain a deux semaines de 44,33 ; le dz de v8 contre la moyenne d'item vaut moins 0,55, le
sien au centieme ; la decomposition se reproduit une fois les echelles orientees, interaction personne x item
7,7 a 8,4 fois l'effet personne contre 8,9 (a43, sections 4 a 6). Apres retrait de la moyenne de segment, C2
perd 83 pour cent de son signal individuel et v8 92, contre 14 pour C3 ; mais la regression et la foret sur
demographies perdent 76 et 77 : le remplacement de la personne par le groupe est propre au conditionnement sur
le groupe, quel que soit le moteur (a43, 4.2). Ce qui reste au dela du groupe n'est pas nul, 0,8 a 2,7 pour
cent du plafond, indistinguable du plancher de bruit du demoyennage sur 150 personnes : ne jamais ecrire
« nulle ». Et un adversaire trivial nouveau : la moyenne du segment de la personne, calculee sans elle, r 0,534
par personne, n'est battue par aucune des quinze methodes de facon retenue par Holm (a43, section 5). Elle
coute zero appel et onze attributs.

### 10.3 a44 : les deux ratios du dossier sont des quantites de gabarit, et le test qui separe est ailleurs

Les ratios inter et intra de a1 ne dependent que de la table segment x modalite ; ils sont exactement
invariants sous permutation des personnes a l'interieur d'un segment, ecart 0,000e+00 (a44, section 3.1). Un
generateur qui tire chaque reponse independamment dans la marginale de son segment, sans aucune structure
individuelle, reproduit le gonflement de toutes les conditions, v8 8,130 contre 8,175, C2 6,894 contre 7,209,
et l'ecrasement a 99,3 pour cent ; il reproduit le 7,37 de a31 a 7,32, le lift de segment de tout le monde a
88 a 98 pour cent, et le rappel des rares de v8 a 91 pour cent ; il ne reproduit pas le lift de personne des
humains ni des conditions riches, 0,241 contre 0,001, 0,212 contre 0,047 (a44, sections 3 et 6). Aucune de ces
valeurs n'est fausse ; ce qui change est ce qu'elles prouvent : elles decrivent le gabarit de groupe de la
condition, c'est a dire que ses marginales par segment different de celles des humains, et rien de plus. Le
critere de Yuan s'applique mot pour mot. Deux des six chemins de la section 2.1 mesurent le gabarit (a31, a35),
deux mesurent le rapport aux personnes (a29 et, par a42, l'exces sur les raretes stables), deux ne sont pas
passes au nul (a28 test 3, a33).

Le test qui separe est la chute d'exactitude quand on permute les personnes a l'interieur de leur camp : les
memes humains reinterroges perdent 34,7 pour cent, c'est le plancher ; composite perd 22,3, soit 64 pour cent
du plancher, PMM 60, enquete 54, entretien 53, C3 45 ; v8 et C2 perdent 2,5 et 2,4, soit 7 pour cent du
plancher, a deux points des temoins aveugles a moins 0,2 ; et une reassignation arbitraire des reponses a
l'interieur du camp fait 4,9 fois mieux que la vraie chez v8, 3,1 chez C2, 1,00 chez les humains et 1,01 chez
composite (a44, section 5) [classement post hoc sur une mesure preenregistree]. Les agents a etiquette
ideologique sont des gabarits de groupe a 93 pour cent interchangeables ; les agents riches, C3 et PMM portent
la personne ; la foret et la regression sur demographies sont du cote du gabarit, 2,76 et 2,68 : c'est le
conditionnement, pas le langage. Deux faits neufs : toute population simulee a moins de patrons de reponses
distincts que son propre generateur nul, moins 14 a moins 32 pour cent contre moins 7 chez les humains, et ses
items sont couples deux fois plus fort qu'entre vraies personnes, exces 0,077 a 0,105 contre 0,042, stable de
sept a quatre vingts cellules de conditionnement, donc non attribuable aux demographies recues (a44, section 4).
Le critere preenregistre, la correlation residualisee, ne separe rien ; le test d'ordre de Yuan n'a pas ete
fait, il coute une nuit courte d'appels.

### 10.4 La these, reecrite ; remplace 9.6 et le second paragraphe de la section 7

Une societe simulee a partir d'etiquettes remplace chaque personne par un gabarit de son groupe, et cela se
mesure par une quantite de personne et non par une quantite de distribution : melanger les personnes a
l'interieur de leur camp ne coute que 2,5 pour cent d'exactitude a un agent a etiquette ideologique contre 34,7
aux memes humains reinterroges, et une reassignation arbitraire fait cinq fois mieux que la vraie. Les mesures de
gonflement d'ecart entre groupes et d'ecrasement de dispersion qui ont porte le premier diagnostic, exactes et
repliquees, sont reproduites a un pour cent pres par un generateur sans structure individuelle : elles decrivent
le gabarit, et elles doivent etre publiees a cote de la chute sous permutation et du plancher humain, jamais
seules. L'etiquette ideologique est ce qui transforme un agent en gabarit : le meme modele, les memes personnes
et les memes questions donnent 7 pour cent du plancher avec l'etiquette et 45 pour cent sans, 83 contre 14
pour cent de signal perdu au retrait du segment, un facteur d'amplification de l'ecart entre camps de 1,62
contre 0,52 quand humains et statistiques sont a 1, et un camp de gauche unanime la ou la loi humaine de
consensus predit seulement le plus de consensus ; et c'est le conditionnement sur le groupe qui produit le
gabarit, une regression sur demographies le fait autant. Compare equitablement a vingt methodes d'imputation, un
jumeau de langage est une imputation par l'esperance, dominee par les imputations par tirage sur la structure et
par la regression sur l'exactitude, y compris dans le regime ou l'information la plus proche manque, et il ne
bat pas la moyenne du segment de la personne. Son seul avantage mesure tient sur les gens rares reels : sur les
reponses rares que la personne redonne deux semaines plus tard, il en retrouve deux sur cinq contre une sur
douze pour la regression et une sur quatre pour l'appariement sur moyenne predite, avantage plus grand sur ces
raretes verifiees que sur les instables, et il attend sa comparaison appariee. Ce que la these ne dit plus :
« deductible de l'etiquette », « nulle », « tout predicteur », « les modeles de langage », et « la ou les humains
se surveillent ».

### 10.5 Les verrous, reclasses une derniere fois

Un, la comparaison appariee du rappel des minorites, restreinte aux raretes stables : un run en regime severe
sur gpt-oss-20b, famille retiree de l'invite, ou le fichier « retrait par bloc » de Stanford, plus les 90
personnes manquantes de C3F, avec la chute sous permutation comme seconde quantite ; une nuit. Deux, le placebo
d'etiquette et le test d'ordre de Yuan sur C2 et C3, deux conditions courtes : a44 fournit le nul, pas le
placebo, et le test d'ordre est le criterium de l'adversaire. Trois, passer a28 test 3, a29 et a33 au
generateur nul, faire de la chute sous permutation une quantite de verdict preenregistree, et la rejouer sur
Twin ; zero appel. Quatre, l'etape d'apparition, E2 puis E1, avec la chute sous permutation et le facteur
d'amplification comme sorties, et les 67 paires de Plisiecki. Cinq, adopter la moyenne de segment sans la
personne comme plancher trivial et PMM comme adversaire officiel dans tout tableau, et repasser a28 et a29 sur
eux ; zero appel. Six, l'anomalie v6 et v7 et le controle par identification partisane. Sept, un second delai
de retest pour distinguer heterogeneite stable et memoire de reponse, et la question de savoir si la
decomposition de Ahn porte sur la reponse ou sur l'erreur, une lecture. Huit, le deficit de combinaison, moins
de patrons que son propre nul, comme resultat a part, avec Twin.

Ce que je ne sais plus, ou pas encore : si les 1,1 pour cent qui restent a v6 au dela de son groupe sont de la
personne ou une segmentation trop grossiere ; si la stabilite a deux semaines est de la conviction ou de la
memoire ; si la chute sous permutation, mesure preenregistree mais classement post hoc, tiendra ses seuils sur
Twin ; et si un modele plus gros, sous etiquette, reste un gabarit.

## 11. Ce que la nuit du 9 septembre change, avant les runs R2, R3, R4 et le run composition

Ecrit a 03:10 sur le fil de la nuit (JOURNAL-NUIT-2026-09-09), r1-resultats, i3b, c1, a45, a47, a46, r4 et d1.
Quatre runs n'ont pas rendu : R2, arrete a 05:45 ; R3, fin dure 08:00 ; le run composition, 08:05 a 08:50 ; R4,
fin dure 10:00. La ou ils decident, la ligne porte [EN ATTENTE] et rien n'est anticipe (errata E9 applique).

### 11.1 Ce qui bouge dans la chaine causale de la section 1

Le mode d'interrogation devient un maillon a part entiere. Le maillon « invite » (1.4) supposait un seul mode,
l'incarnation d'une personne etiquetee lue sur les probabilites de token. R1 mesure l'autre mode, la description
d'un camp par des pourcentages ecrits en clair, sur les memes 149 items, le meme fichier GGUF, temperature 0. Sur
les memes 29 items, la meme quantite et le meme referent humain, Qwen3-4B va de 0,115 a 0,179 en description a
1,617 en incarnation etiquetee, C3 a 0,523 entre les deux, humains 1,025, p apparie 0,00005 et 0,00025 (r1, 2.2)
[ETABLI]. Trois choses bougent ensemble, le mode, l'unite simulee (un camp en un appel contre 150 personnes une
par une) et la lecture (pourcentages contre probabilites de token) : le maillon se nomme « protocole
d'interrogation » et ne se reduit pas au mode. Son poids est du meme ordre que celui du modele : Qwen3-30B-A3B en
description est a 1,32 a 1,52, du meme cote du plancher que Qwen3-4B en incarnation (r1, 2.3) [ETABLI].

Le taux de base et le retrecissement vers l'uniforme, distorsion que la section 1 n'avait pas. En description,
l'erreur vaut sept a onze fois le plancher de reinterrogation (distance de variation totale 0,20 a 0,31 contre
0,024 a 0,030), et les pires items ne sont pas politiques : items factuels a nombreuses modalites et a realite
quasi degeneree, fucitzn, mnthsusa, jew, income ; correlation entre l'erreur et le nombre de modalites +0,40 a
+0,58 (r1, 3.1 et 3.2) [ETABLI]. Le mecanisme est une compression vers l'uniforme, alpha median 0,33 a 4
milliards, 0,43 a 20, 0,61 a 30, point fixe vers 34 pour cent : une modalite sous 1 pour cent reel recoit 11,9
pour cent, une modalite au dessus de 75 perd 21,7 points (r1, 3.3) [ETABLI comme fait ; quantite declaree apres
coup, sans intervalle]. Ce n'est ni le corpus (1.1), ni l'ancre lexicale (1.4), ni le decodage (1.5) ; c'est une
distorsion propre au modele, decroissante avec sa taille. Elle explique H1, les trois modeles decrivant les camps
comme plus varies qu'ils ne sont, 1,04 a 1,18, la gauche le plus alors qu'elle est le camp le plus homogene (r1,
1.1) [ETABLI], et les deux tiers du signal syndiques de a46, 65 a 75 pour cent a 4 milliards contre 5,5 reels
(r1, 3.4) [ETABLI]. La prediction de 2.3, « le modele doit connaitre la marginale qu'il ne sait pas incarner »,
est fausse a 4 milliards. Sa seule trace est une attraction vers les marginales nationales du GSS, plus 0,02 de
distance, p 0,02, 9 pour cent de l'erreur, avec une explication concurrente aussi bonne, l'echantillon de
Stanford n'etant pas national (r4, 5.2) [ETABLI pour le signe, PROBABLE pour la lecture].

La dependance au demandeur. En description, l'identite de celui qui demande, journaliste neutre ou membre du camp
adverse, deplace le portrait de 2,7 a 4,2 fois le plancher, trois modeles, deux camps, Holm 0,0003, sans
direction : le deplacement vers le pole du camp est nul sur les six cellules apres Holm (r1, 1.3) [ETABLI]. Ce
qui bouge est la forme, pas la position. C'est l'homologue en description de l'ancre lexicale de 1.4 : une phrase
de l'invite systeme deplace la mesure plus que le bruit humain, et « caricature pour plaire » n'est pas soutenu.

### 11.2 Ce qui bouge dans le mecanisme central de la section 2

La substitution de la personne par le groupe est propre au conditionnement, pas au moteur. La section 2.1
concluait « un mecanisme de l'etiquette, pas du langage » ; la seconde moitie tient, la premiere tombe. Apres
retrait de la moyenne de segment, C2 perd 83 pour cent de son signal individuel, v8 92, une regression et une
foret sur les memes onze attributs 76 et 77, C3 14 (a43, 4.2 ; errata E7) [ETABLI]. C2 et C3 n'echangent pas
l'etiquette, ils echangent toute leur entree, onze attributs sans aucune reponse contre 119 reponses sans aucune
demographie ; a moteur constant, passer de B1 a B2 deplace deja la chute sous permutation de 0,175 a 0,357 (a45,
0 ; errata E1) [ETABLI]. Les six chemins « independants » de 2.1 sont six lectures d'un seul contraste confondu.

L'ablation propre est R3, en cours : C3 plus l'etiquette contre C3, C2 prive des lignes ideologie et parti contre
C2, Qwen3-4B, 150 personnes, 58 items de famille, deux segmentations, page de plan horodatee 22:30 avant tout
appel ; predictions ecrites, ajouter l'etiquette a C3 reduit la chute, retirer l'ideologie de C2 fait tomber le
gonflement (JOURNAL, 01:15) [EN ATTENTE, fin 08:00 ; projection 75 a 90 personnes pour C3 plus etiquette].

La mesure de personne depend de la segmentation. La chute sous permutation vaut 7 pour cent du plancher humain
pour v8 et C2 sous la segmentation qui contient l'ideologie, 18 a 27 sous genre x race x age de finesse
comparable, composite 64 a 70 dans les deux ; le rapport entre les deux classes de conditions passe de 9 pour 1 a
2,6 pour 1, et « gabarits a 93 pour cent interchangeables » est retire (a47, 1 ; errata E2) [ETABLI]. Permuter a
l'interieur de la variable que l'invite contient mesure ce que l'agent sait au dela de ce qu'on vient de fixer ;
la segmentation sans ideologie est celle qui repond a « l'agent porte t il la personne ». Des quatre piliers de
10.4, un seul est une quantite de personne ; gonflement, ecrasement, facteur d'amplification (invariant a
0,00e+00), unanimite et pente de consensus sont des quantites de gabarit (a47, 2 et 3 ; errata E3) [ETABLI], et
la chute partage 82 pour cent de sa variance avec l'exactitude brute (errata E5) [ETABLI]. Twin manque toujours.

Complement venu des menages. Sur le SCE, sans aucune variable politique : part inter cohortes 0,019, part stable
0,525 en borne haute, chute sous permutation 0,639 pour l'historique du menage contre 0,003 pour les
demographies, la persistance seule captant 96 pour cent de ce que la foret trouve ; et un nul a derive, calibre
sur ses marges sans appariement des personnes, fait bouger ses menages deux fois trop, rapport 0,43 (c1)
[ETABLI, humains seulement]. Le gabarit ecrase l'interieur quel que soit le segment (c1, question 5) [PROBABLE].

### 11.3 La contradiction du champ, resolue par un fait a modele constant

La premiere ligne du tableau de la section 4, ecart gonfle ou aplati, invoquait trois variables jamais mesurees
ensemble. La nuit mesure la premiere a l'interieur d'un seul fichier de modele : 0,12 a 0,18 en description,
0,52 en incarnation sans etiquette, 1,02 chez les humains reinterroges, 1,62 en incarnation etiquetee, memes 29
items, meme quantite, meme referent, intervalles disjoints, facteur neuf a quatorze selon l'identite du
demandeur (r1, 2.2) [ETABLI]. Les deux valeurs sont des deux cotes du plancher humain, pas de signes opposes. La
deuxieme ligne, dispersion interne ecrasee ou excessive, recoit la meme mesure interne : en description les trois
modeles sur dispersent, 1,04 a 1,18 ; en incarnation C2 ecrase a 0,365 (a35, 4) [ETABLI]. Mais la resolution
n'est pas « c'est le mode » : mode, unite et lecture bougent ensemble, et le choix du modele deplace autant que
le protocole, 0,25, 0,62 et 1,27 sur 79 items a identite fixe. La contradiction n'est pas resolue par une
variable, elle est dissoute : la quantite n'a pas de valeur de reference, elle varie d'un facteur 5,2 entre
modeles a identite fixe, 13,2 en variant l'identite, 14 en variant le protocole (r1, 5.1) [ETABLI]. « Toute
phrase sans regime est refutable en une ligne » devient « toute phrase sans protocole ni modele ». Reserves : le
contraste n'existe que sur Qwen3-4B, R2 en donne la branche sans etiquette sur gpt-oss-20b [EN ATTENTE] ; et le
regime de decodage, argmax contre tirage, n'est mesure sur aucun agent (a45, 3.4).

### 11.4 Les trois phrases revendicables de la section 5, reecrites

Une. A modele, quantification, temperature, personnes et questions constants, remplacer les 119 reponses de la
personne par onze attributs dont l'etiquette ideologique fait passer la part du plancher humain perdue sous
permutation de 45 a 7 pour cent sous la segmentation qui contient l'ideologie et de 46 a 18 sous celle qui ne la
contient pas ; une regression et une foret sur les memes attributs perdent 76 et 77 pour cent de signal
individuel contre 83 : la substitution suit le conditionnement, quel que soit le moteur, et la part propre a
l'etiquette est celle que R3 mesure [EN ATTENTE]. Le meme fichier de modele, interroge en description sur les
memes 29 items, donne un facteur d'ecart entre camps de 0,12 a 0,18 la ou l'incarnation etiquetee donne 1,62 et
les humains 1,02 : la caricature est une propriete du couple modele et protocole, et elle depend de qui demande.

Deux. Compare equitablement a vingt methodes d'imputation, un jumeau de langage est une imputation par
l'esperance, dominee par les imputations par tirage sur la structure et par la regression sur l'exactitude dans
les deux regimes mesures, et il ne bat pas la moyenne du segment de la personne calculee sans elle. Son seul
avantage mesure, les gens rares que la personne redonne deux semaines plus tard, deux sur cinq contre une sur
douze pour la regression et une sur quatre pour l'appariement sur moyenne predite, est mesure contre le
comparateur le plus faible et attend R2 sur gpt-oss-20b, famille retiree de l'invite [EN ATTENTE, arret 05:45].
Sur les menages, la barre est ecrite avant tout appel : 0,615 pour battre la persistance seule (c1, 7.3).

Trois. Chaque quantite est posee en regard d'un plancher obtenu en reinterrogeant les memes personnes, applique
au partage inter et intra, aux gens rares et, depuis cette nuit, au mode description, ou l'erreur des trois
modeles vaut sept a onze fois ce plancher. La nuit etablit que ce plancher est une courbe, 0,659 a un mois et
0,280 a onze sur les anticipations d'inflation (c1, 5.1), et que la bande humaine varie d'un facteur 1,9 a 2,5
entre deux questionnaires a effectif egal (i3b, 4.1). Ce que le dossier revendique n'est plus un plancher que
personne n'a, trois existent ailleurs (9.4), mais la regle qu'aucune quantite ne se publie sans le plancher de
sa population, de son effectif, de son delai et de son protocole.

### 11.5 Les verrous, reclasses, et ce que chaque run decide

Un, R3, l'ablation propre de l'etiquette, fin dure 08:00. Si l'etiquette ajoutee a C3 reduit la chute et si
l'ideologie retiree de C2 fait tomber le gonflement, la phrase une garde l'etiquette comme cause mesuree et la
section 5 recouvre sa revendication de nouveaute ; sinon la cause est le conditionnement et l'etiquette une ancre
parmi d'autres. Le placebo, etiquette permutee entre personnes, reste a faire dans les deux cas [EN ATTENTE].
Deux, R2, la comparaison appariee sur les gens rares, gpt-oss-20b, C3F sur 150 personnes puis un debut de C3,
arret 05:45. Si le rappel des cellules rares stables tient au dessus de PMM et de l'imputation multiple en regime
severe, la derniere clause de la phrase deux survit sur un modele serieux ; sinon la these devient entierement
negative. Puissance connue d'avance, environ 78 cellules rares stables [EN ATTENTE].

Trois, R4, socle contre instruit a invite fixe, fin dure 10:00. Si le socle est plus pres de 1 que l'instruit sur
la dispersion et l'ecart entre camps, le portrait des camps est fabrique par le post entrainement ; s'il fait
comme lui, il est dans les poids et une obligation d'audit visant l'alignement viserait a cote (r4, question 1) ;
q4nogab separe le format des poids. R4 ne tranche pas la contamination, aucune coupure n'etant publiee ; aucun
appel n'a jamais ete envoye a un socle sous cette invite, le run peut echouer a 09:00 [EN ATTENTE].
Quatre, le run composition, 120 appels, 08:05 a 08:50. Sur les huit compositions d'Ahler et Sood, deux bases de
realite et deux ancrages, il dit si l'exageration du modele depasse l'exageration humaine, 3,40 en erreur
relative, et, par ses huit cellules de taux de base, si c'est un defaut de taux de base ou un stereotype
partisan ; si le modele n'exagere pas plus que les humains, il est un correcteur et l'argument du programme A se
retourne (a46, 5). Quatre items par camp : un tableau, pas un verdict [EN ATTENTE].
Cinq, zero appel : C2 tirage et C3 tirage depuis les traces (a45, 3.4) ; le generateur nul sur a38, a37 et a30 ;
la chute sous permutation sur Twin ; PMM en adversaire officiel et la moyenne de segment sans la personne en
plancher trivial ; le depot OSF ou le commit de resultats/. Six, appels : l'incarnation C2 sur gpt-oss-20b et
Qwen3-30B-A3B, seule facon de savoir si le facteur quatorze est un fait de Qwen3-4B ou du champ ; l'ordre des
modalites ; une troisieme identite. Sept, programme C : le run simule sur le SCE, 600 agents, C2 contre C3 contre
description, coupure anterieure a mars 2025, barre 0,615, 0,019, 0,525 et 0,43 (c1). Huit, programme B : une
seconde population humaine, LISS et BES a la main d'Amir ; un fichier reel contamine, lettres 03 et 04 ; une
statistique de reserve qui marche ou l'abandon de cet etage ; la lecture par camp par defaut (i3b, 11).

Ce que je ne sais pas encore, a 03:10 : si l'etiquette a un effet propre ; si l'avantage sur les gens rares
survit a un modele serieux ; si le portrait des camps est dans les poids ou dans le post entrainement ; si le
modele exagere plus que les humains sur les compositions ; si l'absence de direction de H3 est un resultat ou un
manque de puissance.

## 12. Ce que la nuit du 9 au 10 septembre a etabli

Ecrit au matin du 10 septembre, apres lecture du journal de nuit, des rapports r1, r2, r3, i3b, c1, t1, t2,
a46 et sa composition, r4, d1, p1, t3, du bilan des predictions et des errata a47. Niveaux : [ETABLI] mesure
chez nous et relu, [PROBABLE], [HYPOTHESE], [EN ATTENTE]. Aucun chiffre annule par un errata n'est repris.
« Chute sous permutation » : ce qu'un agent perd en exactitude quand on melange les personnes a l'interieur
de leur groupe, en part de ce que perdent les memes humains reinterroges, le « plancher humain ».

### 12.1 Les runs, et ce que chacun a tranche

R1, l'oracle des camps, 2 682 cellules, trois modeles, une heure de machine (r1). Les trois modeles decrivent
tous les camps comme plus varies qu'ils ne sont, rapport 1,04 a 1,18 pour un plancher a 1,00, la gauche, camp
le plus homogene, etant la plus sur decrite (r1, 1.1) [ETABLI]. Sur l'ecart entre camps ils se contredisent,
0,25, 0,62 et 1,27 fois le reel, intervalles disjoints du plancher dans des directions opposees (r1, 1.2)
[ETABLI]. Tous adaptent le portrait a l'identite de celui qui demande, 2,7 a 4,2 fois le plancher, sans
direction mesurable : « caricature pour plaire » n'est pas soutenu (r1, 1.3) [ETABLI]. Sur un seul fichier de
modele, les memes 29 items et la meme quantite, la description donne 0,12 a 0,18 la ou l'incarnation
etiquetee donne 1,62 et les humains 1,02 : un facteur quatorze entre deux protocoles a temperature zero (r1,
2.2) [ETABLI]. C'est la quatrieme issue : ni exageration, ni archive fidele, ni sous representation, mais une
quantite sans valeur de reference, facteur 5 entre modeles et 14 entre protocoles (r1, 5.1) ; le mecanisme
dominant est un retrecissement vers l'uniforme, point fixe vers 34 pour cent (r1, 3.3).

R2, la comparaison appariee sur les gens rares, gpt-oss-20b, 150 personnes, 8 700 appels en regime severe
plus 6 090 avec cousins (r2). Il ferme le verrou 1 de 10.5 dans le sens negatif. Quand la famille thematique
de la question est retiree de l'invite du jumeau comme du contexte des methodes statistiques, le jumeau ne
retrouve pas les reponses rares stables mieux qu'un tirage au sort dans le segment de la personne, exces
+0,03 [-0,04 ; +0,10], Holm 1,00 (r2, 2.1) [ETABLI]. Il est derriere l'appariement sur moyenne predite, PMM,
de 0,09, sans que Holm decide : la phrase autorisee est « il ne bat pas PMM », jamais « PMM le bat » (r2,
2.1). Il est dernier en precision, sous la reponse majoritaire en exactitude, 0,53 contre 0,62, dernier en
diversite conservee, 0,44 contre 0,98 pour PMM, et dernier en chute sous permutation, 10,8 pour cent du
plancher (r2, 2.2 a 2.4) [ETABLI]. Passer de 4 a 20 milliards ne reduit aucun ecart (r2, 4.1). L'avantage
revendique depuis a42 venait des items cousins gardes dans l'invite : avec eux, la meme trace passe tout, PMM
compris ; sans eux, rien (r2, 4.2) [ETABLI]. Les quatre avantages revendiques sont tombes (r2, 5.5).

R3, l'ablation propre de l'etiquette, Qwen3-4B, 58 items, C3E sur 94 personnes et C2S sur 130, C3ES non
lance faute de temps (r3). Ajouter les onze attributs, ideologie comprise, aux 119 reponses de la personne ne
change pas l'exactitude, +0,005, ni la chute sous permutation, 0,455 contre 0,448 du plancher humain sous la
segmentation ideologique, 0,511 contre 0,564 sous genre x race x age, Holm 0,95 et 0,99 ; mais fait passer le
ratio inter sur l'axe ideologie de 0,80 a 2,34, le lift de rarete de segment de 0,24 a 0,73, Holm 0,002, et le
rapport groupe sur personne de 0,82 a 3,23, Holm 0,008 (r3, 1) [ETABLI]. Retirer l'ideologie et le parti des
onze attributs fait tomber le ratio inter de 10,1 a 0,04, Holm 0,0025, a exactitude egale, et fait passer les
modalites minoritaires osees de 254 a 20 sur 7 540 cellules, comme v6 contre v8 chez Stanford (r3, 2)
[ETABLI]. Correction a lire avant tout : le journal de 08:05 disait que le rappel des raretes tombait de 0,25
a 0,14 ; c'etait un artefact de perimetre, 58 items contre 149 ; a cellules appariees l'effet vaut +0,016, et
sur les raretes stables le rappel monte avec l'etiquette, 0,535 vers 0,634 (r3, 3 et 1.4) [ETABLI]. Il n'y a
pas substitution mais addition : lift de segment +0,49, lift de personne +0,03, p 0,645 (r3, 1.4) ; la lecture
causale de a42 se retourne, a31 est la seule mesure anterieure qui traverse l'ablation intacte (r3, 4.3). Ce
que cela tranche : l'etiquette agit dans les deux regimes d'information, mais sur des quantites de gabarit,
ecart entre groupes et rarete de groupe, et sur aucune quantite de personne. La prediction primaire de la page
de plan, « ajouter l'etiquette reduit la chute », est fausse, et sous genre x race x age l'effet est de signe
contraire et decidable, +0,008 [0,0004 ; 0,011] (r3, 1.2). Reserves : pour H1 l'ablation porte sur onze
attributs et non sur les deux lignes politiques, C3ES n'ayant pas tourne ; un seul modele de 4 milliards ;
aucune segmentation n'est neutre pour une condition a etiquette seule, la chute de C2 sous genre x race x age
mesurant ce que porte l'etiquette, 21 pour cent, non la personne (r3, 2.2).

Le run composition, second terme du programme A, 120 appels en 42 secondes, trois modeles, huit compositions
d'Ahler et Sood (a46-resultats-composition). Les trois modeles s'ecartent de la realite moins que les
Americains dans 38 cellules sur 42 : erreur absolue 9,8 points pour gpt-oss-20b, 10,9 pour Qwen3-30B-A3B,
20,1 pour Qwen3-4B, contre 19,8 pour les 1 000 adultes de YouGov ; exageration geometrique 1,24 a 2,33 contre
2,89 (idem, 1.2 et 1.3) [ETABLI en direction]. Mais le plan preenregistre a zero puissance a son propre seuil,
quatre items par cellule ne descendant jamais sous p 0,125 ; aucun des 44 tests n'est significatif, seule une
lecture groupee, non preenregistree, fait passer deux cellules de Qwen3-30B-A3B, 0,46, p 0,0075 (idem, 2.3).
Les trois modeles ne font pas la meme chose : Qwen3-30B-A3B corrige ; gpt-oss-20b repond zero dans 16
cellules sur 32, un refus enregistre comme un nombre ;
Qwen3-4B egale l'erreur humaine en la deplacant, 85 pour cent des republicains dans le Sud (idem, 3.1)
[MESURE, PROBABLE pour la lecture en refus]. Le retrecissement vers l'uniforme fabrique une part de
l'apparence de correction [PROBABLE]. Le signal syndiques de R1 s'inverse selon l'instrument : Qwen3-4B donne
5 pour cent de syndiques en question directe, reel 5,5, contre 65 a 70 en mode description (idem, 3.3)
[ETABLI]. Le point d'arret du mois 1 est atteint : la version forte ferme sur les compositions, et la phrase
pour un regulateur se reecrit autour de la dispersion entre modeles, protocoles et instruments (idem, 4.3).

R4, le socle contre l'instruit : en attente. Demarre a 08:03 sur Qwen3-4B-Base, sonde passee, zero rejet, fin
dure 10:00, resultat attendu vers 09:15 (data/traces/r4-run.log) [EN ATTENTE], a ajouter en addendum. Le seul
resultat de r4 a zero appel : Qwen3-4B decrit les camps un peu plus pres des marginales nationales du GSS que
de l'echantillon de Stanford, +0,02, p 0,02, 9 pour cent de l'erreur, avec une explication concurrente aussi
bonne (r4, 5.2) [ETABLI pour le signe, PROBABLE pour la lecture].

### 12.2 La these finale, en trois phrases

Ce qu'elle affirme. Une, la mesure de personne, la chute sous permutation contre un plancher obtenu en
reinterrogeant les memes personnes, distingue ce que les mesures du domaine ne voient pas : exactitude,
dispersion et ecart entre groupes sont reproduits par un generateur sans structure individuelle, la chute ne
l'est pas, sur le GSS comme sur Twin (a44, t1). Deux, l'etiquette ideologique caricature les groupes, facteur
3 a 25 selon la mesure, ratio inter 0,80 vers 2,34 dans le regime riche et 0,04 vers 10,1 dans le regime
pauvre, a exactitude constante, mais elle ne retire pas la personne quand ses reponses sont donnees, la chute
restant a 45 pour cent du plancher avec et sans (r3). Trois, compare equitablement, sur les memes personnes,
les memes cellules et la meme information, un jumeau de langage n'apporte rien qu'une imputation a tirage
n'apporte, ni en exactitude, ni en structure, ni sur les gens rares reels (r2).

Ce qu'elle mesure. La chute sous permutation, sous deux segmentations, avec et sans l'ideologie, et seulement
pour des conditions dont l'invite ne contient aucune variable de la segmentation (a47 E2, t1, r3, 2.2) ; des
quantites de gabarit, ratio inter, ratio intra, facteur d'amplification, unanimite, lift de rarete de segment,
qui ne se publient jamais seules (a44, a47 E3, t1, r3) ; le rappel et la precision sur les raretes stables
contre un plancher de segment, en regime apparie (r2) ; et, en description, la dispersion, l'ecart entre camps
et la dependance au demandeur contre le plancher de reinterrogation, sans valeur de reference (r1).

Ce qu'elle ne dit pas. Rien sur les simulateurs vendus ni sur les six conditions de Stanford, qui n'ont pas ete
replacees en regime severe (r2, interdit 3) ; rien sur les 1 052 personnes, R2 et R3 tenant sur 150 ; rien sur
la contamination (r1, 5.4) ; rien sur ce que lire une description fait a un lecteur (p1) ; rien hors de trois
modeles ouverts petits, un pays, une enquete, une invite ; pour R3, rien hors d'un modele de 4 milliards.

### 12.3 Les trois programmes a l'etat du matin

Programme A, la fidelite de representation des camps, ancien « oracle des camps ». La nuit lui a apporte son
levier causal, une ligne d'invite qui deplace l'ecart entre camps d'un facteur 3 a 260 sans deplacer
l'exactitude, ce qui ajoute le contenu de l'invite au registre d'audit (r3, 5.4) ; sa quatrieme issue, la
dispersion inter modeles qui depasse l'erreur de chacun (r1, 5.1) [ETABLI] ; le facteur quatorze a modele
constant et la dependance au demandeur (r1, 2.2 et 1.3) [ETABLI] ; le second terme humain, Ahler et Sood,
obtenu en CC0, qui porte sur des compositions et non sur des opinions, et sur lequel les modeles s'ecartent
moins de la realite que les Americains, sans puissance au seuil preenregistre (a46-resultats-composition)
[ETABLI en direction] ; les 25 enonces de l'IGS Poll retrouves dans l'annexe du papier, ce qui rend la version
forte sur les opinions faisable avec une vague de calibrage a 1 000 personnes (p1, 1.3) [CONFIRME] ; un
protocole d'experience de lecture chiffre, 2 080 recrutes, environ 8 900 livres, six bras (p1, 2.1) ; et une
grille d'audit adossee au
DSA art. 34 et 35 et au reglement IA art. 55, qui exigent des protocoles normalises sans en nommer aucun
(t3, 1) [CONFIRME au mot]. Le socle est en attente (R4) ; le point d'arret du mois 1 est atteint, le livrable
devient le tableau d'audit par modele avec son registre ; l'objection « le modele recite le sondage » est
affaiblie, pas levee (r1, 5.4).

Programme B, la bande humaine. Le mois 1 est rendu (i3b). L'abaque : plus petit taux detectable de 2,2 pour
cent pour l'agent a etiquette a 35,4 pour cent pour la regression a tirage sur 1 052 personnes, 4,5 a 60,2 sur
300 (i3b, 3.1) [ETABLI] ; i3 etait optimiste d'un facteur 1,2 a 1,9 et l'adversaire nul demande 9,2 pour cent,
pas 6,4 (i3b, 3.3) [ETABLI]. La bande ne se transporte pas : memes deux bords sur Twin, retest humain jamais
signale, mais niveaux differents d'un facteur 1,9 a 2,5 a effectif egal ; la bande est une forme, pas une
valeur (i3b, 4.1) [ETABLI]. La borne adverse : un fabricant qui vise la bande sans microdonnees gagne un
facteur 1,3 sur l'invisibilite, vu a 13,7 pour cent ; avec 263 vraies lignes volees, un facteur 2, vu a 21,2 ;
les deux statistiques de reserve sont dominees par une statistique publiee (i3b, 6) [ETABLI, borne sur cet
adversaire]. La surface d'attaque : aucun fabricant ne deplace l'ecart entre camps de plus de 6,3 pour cent
ni une marginale de plus de 3,8 points sans etre vu a 1 052 personnes ; invisibilite et nuisance s'opposent
(i3b, 7) [ETABLI] ; la lecture par camp voit une operation concentree 2,9 a 4,7 fois plus tot (i3b, 5.1). La
mesure de personne est transportee sur Twin : les treize configurations sont du cote du porteur de personne,
0,42 a 0,71 du plancher, les seuls gabarits sont les trois predicteurs statistiques, et la sensibilite a la
segmentation depend de l'entree de la condition, facteur 1,0 a 1,06 contre 3,7 pour v8 (t1) [ETABLI].

Programme C, le banc des basculements. Le SCE est obtenu, 194 Mo, licence permissive, identifiants stables
entre fichiers (d1, c1). Le cote humain est fait : la part de la dispersion des anticipations d'inflation qui
separe les cohortes vaut 0,019 en mediane, jamais plus de 0,048 (c1, 4.1) [ETABLI] ; la part stable vaut
0,525 en borne haute, retest 0,66 a un mois et 0,28 a onze (c1, 5) [ETABLI] ; la persistance seule capte 96
pour cent de ce que la foret trouve (c1, 6.1) [ETABLI] ; et un nul a derive calibre sur ses marges fait bouger
les menages deux fois trop, rapport 0,43 (c1, 6.3) [ETABLI]. Sur les panels GSS, qui bouge par groupe est
previsible, correlation entre moities 0,60, 0,447 de variance inter groupes expliquee pour un plafond de
0,638, mais la direction ne l'est pas, camp dans la bande de permutation, seul l'age sort (t2, 3.3) [ETABLI] ;
le « bouge deux fois trop » se transporte en direction, pas en valeur, 1,4 a 2,6 selon la famille d'items
(t2, 4) [ETABLI]. Le plan de la nuit SCE est ecrit, 28 920 appels, et attend la ligne d'Amir (protocoles/02).

### 12.4 Ce que la relecture adverse et le bilan des predictions ont corrige

Un. C2 contre C3 n'etait pas une ablation de l'etiquette mais un contraste de conditionnement : C2 recoit onze
attributs et aucune reponse, C3 recoit 119 reponses et aucune demographie ; a moteur statistique constant, le
seul changement d'information deplace deja la chute de 0,175 a 0,357 (a45, a47 E1) [ETABLI]. Huit textes
disaient « seule l'etiquette bouge » ; ils ont recu un errata, et R3 a fait l'ablation propre (12.1).

Deux. Le « 7 pour cent du plancher humain » depend de la segmentation : 7 sous la segmentation qui contient
l'ideologie, 18 a 27 sous genre x race x age, contre 64 a 70 pour l'agent composite dans les deux ; « 93 pour
cent interchangeables » est retire, le classement survit, le chiffre non (a47 E2) [ETABLI]. La sensibilite
vient du recouvrement entre la segmentation et l'entree de la condition, pas du jeu (t1, 9), et le 7 contre 45
est le facteur d'information, pas d'etiquette (r3, 5.1). Trois des quatre piliers de 10.4 sont des quantites
de gabarit ; seule la chute est une quantite de personne (a47 E3). C2 et C3 ne passent pas Holm dans a38 (a47
E4). La chute partage 82 pour cent de sa variance avec l'exactitude sur le GSS, 26 a 28 sur Twin (a47 E5, t1).

Trois. Le bilan des 53 predictions preenregistrees deja tranchees : 23 tenues, 16 fausses, 14 a moitie, credit
56,6 pour cent (bilan, 3). Le defaut n'est pas d'etre faux en notre faveur, c'est le volume : 37 predictions en
faveur de la these contre 3 qui pouvaient couter, et les 3 sont tenues, ce qui indique des paris ecrits avec la
reponse en tete (bilan, 3). R2 est le premier run ou les deux predictions ecrites contre la these tiennent et
deux des trois en faveur tombent (r2, 2.5). Trois regles sont proposees et non inserees : R11 la prediction qui
coute, R12 toute borne se prouve avant, R13 le critere de verdict se nomme et son anteriorite se prouve hors
machine (bilan, 5). Aucune page de plan n'est deposee hors de la machine ; le commit cite par r1, r4 et a46 ne
contient aucun fichier du projet (bilan, 1) [ETABLI]. Deux erreurs de lecture corrigees : H4 de R1 passe dix
cellules sur douze (r1, 1.4) ; « le socle est deja telecharge selon a3 » etait faux (r4, 1.1).

### 12.5 Les verrous restants, classes

A zero appel, des ce matin. C2 tirage et C3 tirage depuis les traces (a45) ; le generateur nul sur a38, a37 et
a30 ; PMM en adversaire officiel et la moyenne de segment sans la personne en plancher trivial ; t2 sur les
seuls items d'attitude ; la ponderation de panel pour i1, a12 et t2 ; deposer les pages de plan sur l'OSF ou
dans un depot avec commit avant tout run nouveau, et inserer les regles R11 a R13 ; recalculer a38, a30 et a37
sur les traces C3E et C2S (r3, 8.6) ; un erratum aux huit textes « ablation de l'etiquette » (r3, question 6).

Appels courts, moins d'une nuit. C3ES, la troisieme condition de R3, une heure de machine, seule facon
d'ecrire « etiquette ideologique » plutot que « bloc demographique » dans le regime riche (r3, 2.5) ; le
placebo a etiquette permutee sur C2, verrou 2 de 10.5 (r3, 5.2) ; les 176 personnes qui rendraient decidable
le contraste contre PMM, moins de deux heures, issue probable defavorable (r2, 3.2) ; les 90 personnes
manquantes de C3F Qwen3-4B ; la seconde passe d'ordre des modalites sur C3F gpt-oss, 4,5 heures (r2, non
verifie 1) ; une troisieme identite dans R1 ; q4hyb si la fin dure de R4 la coupe ; un run composition avec
assez d'items pour avoir de la puissance.

Une nuit chacune. L'incarnation C2 sur gpt-oss-20b et Qwen3-30B-A3B, seule facon de savoir si le facteur
quatorze est un fait de Qwen3-4B ou du champ (r1, 2.3) ; le protocole de R3 sur gpt-oss-20b (r3, question 5) ;
la nuit SCE apres la ligne d'Amir ; un second socle si R4 rend « le socle fait comme l'instruit » (r4, q. 1).

A la main d'Amir. LISS, BES, compte ANES et lettre 01 ; lettres 02 a 07 ; un cosignataire en science
politique par la lettre 08 et la note 09 a Simon, seul chemin critique de l'experience de lecture avec le
comite d'ethique (p1, 3) ; une lettre a Gaurav Sood pour l'IGS Poll (a46, question 1) ; sans fichier reel a
contamination documentee, le programme B publie une methode et pas une mesure (i3b, 10).

Ce que je ne sais pas encore : si le portrait des camps est dans les poids ou dans le post entrainement (R4) ;
si la correction des compositions par Qwen3-30B-A3B tient avec plus de huit items ; si l'effet de R3 dans le
regime riche revient aux deux lignes politiques ou aux onze attributs, et s'il tient sur un modele plus gros ;
quelle segmentation porte la mesure de personne pour une condition a etiquette seule (r3, question 2) ; si
l'absence de direction de H3 est un resultat ou un manque de puissance (r1, question 2).

## 12 bis. R4, le socle

Ecrit le 10 septembre apres r4-resultats.md. Remplace pour la lecture le « R4 : en attente » de 12.1, complete 12.3 et 12.5.

R4, 2 682 cellules, quatre conditions, 48 minutes de machine (r4). Les trois conditions nouvelles ont rendu 894 sur 894 ;
la quatrieme est la trace de R1 copiee octet pour octet. Le risque principal de la nuit ne s'est pas realise : le socle a
suivi l'invite a trois exemples, 2,68 pour cent d'echec de premiere tentative et zero rejet apres relance (r4, 3.1)
[ETABLI]. Ce que R4 tranche n'est pas la question posee : sur l'ecart entre camps decrit, le format d'invite porte plus
que les poids. Le meme fichier GGUF de Qwen3-4B-Instruct-2507 donne 0,245 fois le reel sous gabarit ChatML et 0,727 en
completion a trois exemples, marche de +0,48 [+0,29 ; +0,68], quand l'ecart total socle contre instruit ne vaut que
+0,32 [+0,13 ; +0,52] ; la part du format vaut 1,50 [1,00 ; 2,90] en identite journaliste et 2,61 en identite adverse,
hors de la bande [0,20 ; 0,80] preenregistree (r4, 2.1) [ETABLI]. a27 annoncait la moitie ; c'est une fois et demie. Sur la
dispersion, format et poids s'annulent et ne se separent pas (r4, 1.3) [ETABLI].

Le sens du post entrainement est celui que le programme n'attendait pas. Sous le meme format, le socle ecrase davantage
que l'instruct-2507, -0,16 [-0,34 ; +0,01] sur 79 items orientes et -0,24 [-0,43 ; -0,05] sur 65 items stricts, sur decrit
davantage la variete interne, et se trompe plus globalement, 10,5 contre 9,6 fois le plancher humain : l'alignement
rapproche des humains sur ces quantites (r4, 2.2) [ETABLI pour les mesures, contraste declare non apparie]. Le gabarit
implicite : Qwen3-4B, successeur apparie du socle, rend en completion la mesure de l'instruit sous gabarit, +0,017 avec
p 0,84, et une mesure trois fois plus petite que le meme instruct sous la meme invite, -0,465 [-0,654 ; -0,289] ; il
reconstruit le tour d'assistant que l'invite ne donne pas, dans 57 a 64 pour cent de ses relances, zero fois sur les 918
sorties du socle (r4, 2.3) [ETABLI pour les marqueurs, PROBABLE pour le mecanisme]. Et la dependance au demandeur n'est
pas un fait d'alignement : le socle change son portrait du camp de droite selon qui demande, 5,0 fois le plancher humain,
plus que les trois conditions instruites, Holm 0,0004 (r4, 1.5) [ETABLI].

La contamination reste entiere, aucune coupure n'etant publiee pour aucun des trois modeles. Le seul fait nouveau est
negatif : le socle n'est pas plus pres des marginales nationales que de notre echantillon, -0,006 [-0,024 ; +0,012], et le
signe positif de q4 disparait quand on change le format a poids constants, -0,028 [-0,040 ; -0,016] ; le signe de
restitution n'est pas dans les poids (r4, 1.4) [ETABLI pour les contrastes, PROBABLE pour la lecture]. Les paris : trois
des quatre predictions tombent, dont les deux ecrites en faveur de la these ; H2 tient a la lettre et son controle de
format la retourne ; H3, la seule qui pouvait couter, coute, dans le sens nomme d'avance (r4, 1.6) [ETABLI].

Ce que cela change ailleurs. A 12.3, le registre des versions du programme A gagne un champ obligatoire, le format
d'invite, gabarit et exemples compris : sans lui, deux auditeurs du meme modele publient des chiffres qui different d'un
facteur trois. A 12.5, la ligne « un second socle si R4 rend le socle fait comme l'instruit » est fermee sous cette forme,
remplacee par la condition manquante « gabarit ChatML plus trois exemples », 894 appels, et par un socle d'une autre
famille, OLMo de preference ; la relance de R1 est a refaire avant tout run de completion, ou elle recopie son exemple
chiffre 45 fois sur 45 (r4, 3.1) [ETABLI]. A 12.2, rien ne bouge : R4 ne porte ni sur les jumeaux, ni sur l'etiquette, ni
sur la chute sous permutation ; il ajoute un etage a la partie instrumentale, la fidelite de representation des camps est
une propriete du couple modele et instrument, et la part de l'instrument depasse celle des poids.
