# a9. Le trait de deviance et l'incoherence au bon endroit

## Errata du 8 septembre 2026

Corrections apportees a la suite de la relecture adverse `a17-relecture-adverse.md`. Le corps
du rapport n'est pas reecrit, il reste lisible tel qu'il a ete rendu le 7 septembre. Chaque
point cite la phrase d'origine, donne la correction et la preuve. Aucune donnee nouvelle n'a
ete produite : les corrections sont arithmetiques ou portent sur des rapprochements entre
grandeurs, et elles s'appuient sur les fichiers deja publies, en particulier
`resultats/a9-deviance-un-facteur.csv`. Aucun appel de modele.

### E1. Section 1.6 : le rapprochement avec le 0,40 a 0,56 est faux deux fois. Objection a17 5.1, contradiction C2.

**Phrase d'origine.** "Le taux de deviance des agents vaut 0,45 a 0,66 fois celui des humains.
Cette fourchette recouvre presque exactement le ratio d'ecarts types **intra groupe** de 0,40 a
0,56 retenu dans la these du projet. La deviance au mode du groupe est donc une mesure lisible
du meme phenomene, exprimee en pourcentage de reponses et non en ecart type, ce qui est
beaucoup plus facile a expliquer a un acheteur."

**Premiere erreur : le 0,40 a 0,56 n'est pas un ratio intra groupe.** Deux rapports du dossier
l'etablissent, et ils sont anterieurs de quinze minutes a la remise de ce rapport.
`a10-verification-sources.md` section 1.a attribue la fourchette a Ozkan, arXiv 2607.18310, et
la qualifie de **ratio d'ecarts types par item sur toute la population**, mesure sur le seul
World Values Survey Turquie, et non sur la dispersion residuelle a l'interieur de segments
demographiques ; il conclut qu'"il n'y a pas de comparaison a armes egales possible entre ce
chiffre et le notre, parce que ce ne sont pas les memes grandeurs".
`a15-gonflement-ou-aplatissement.md` section 3.3 designe une seconde source possible de la meme
fourchette, le ratio d'ecarts types 16,1 sur 31,4 egal a 0,513 de Bisbee, Clinton, Dorff,
Kenkel et Larson 2024, *Political Analysis* 32(4), qui porte lui aussi sur la dispersion entre
repondants de toute la population, sur une quantite construite, la polarisation affective, et
non sur une dispersion intra groupe. **Les deux lectures convergent sur le point qui compte
ici : ce n'est pas un ratio intra groupe.** L'attribution exacte de la fourchette de PASSATION,
Ozkan ou Bisbee, n'est pas tranchee par le dossier ; a15 la donne comme [PROBABLE].

**Seconde erreur, superposee a la premiere : les deux quantites ne vivent pas sur la meme
echelle.** Un taux de deviance est une **proportion de reponses** differant du mode d'un
groupe. Un ratio d'ecarts types est un **rapport de dispersions**. Deux nombres voisins ne sont
pas la meme quantite, et le rapprochement n'a aucune raison arithmetique d'exister. Le rapport
en tire de surcroit une consequence commerciale, "beaucoup plus facile a expliquer a un
acheteur", ce qui transforme une coincidence en argument de vente.

**Phrase de remplacement.** "Le taux de deviance des agents vaut 0,45 a 0,66 fois celui des
humains [MESURE]. Cette mesure n'est comparable a aucun ratio d'ecarts types publie, ni au
0,40 a 0,56 de la these du projet, qui est un ratio de dispersion sur toute la population et
non une dispersion intra groupe. Elle doit etre presentee seule."

Le fait mesure, lui, ne bouge pas et reste le resultat de la section : les agents devient de
leur groupe deux fois moins souvent que les humains qu'ils simulent.

### E2. Section 1.4 : "plus fort encore que 0,684" est faux, et les deux r ne sont pas comparables. Objection a17 5.2.

**Phrase d'origine.** "La deviance moyenne sur les six domaines correle a -0,535 [-0,568 ;
-0,502] avec la consistance test retest. C'est plus fort encore que le r = 0,684 entre fidelite
d'agent et stabilite propre releve en section 6 de `a1-double-distorsion.md` sur le GSS."

**Correction, deux fois.** D'abord, en valeur absolue, 0,535 est **inferieur** a 0,684, pas
superieur. Ensuite, et c'est le point de fond, les deux correlations ne portent ni sur les
memes variables, ni sur le meme jeu de donnees, ni sur la meme population : a1 correle la
**fidelite d'un agent** a la stabilite de la personne qu'il simule, sur le GSS et 1 052
participants ; a9 correle la **deviance d'une personne humaine** a sa propre stabilite, sur
Twin-2K-500 et 2 058 participants. Il n'y a pas d'ordre a etablir entre elles.

**Phrase de remplacement.** "La deviance moyenne sur les six domaines correle a -0,535
[-0,568 ; -0,502] avec la consistance test retest [MESURE]. Le confondu est massif et il devait
etre traite. Un lien du meme ordre de grandeur, r = 0,684, est releve par a1 section 6 sur le
GSS, mais entre deux autres quantites et sur une autre population : les deux ne se comparent
pas directement."

### E3. Section 4, "Autorise" point 1 : le plancher de permutation cite n'est pas celui de la quantite annoncee. Objection a17 5.3.

**Phrase d'origine.** "Sur Twin-2K-500, la propension individuelle a s'ecarter du mode de son
groupe est partagee entre six domaines : correlations toutes positives, de 0,07 a 0,31, un
facteur unique expliquant 31 pour cent de la variance, contre un plancher de permutation de
0,000."

**Correction.** Le 0,000 est le plancher de permutation de la **correlation moyenne**,
`r_moyen_permutation = -0,0001` dans `a9-deviance-un-facteur.csv`, et non celui de la part de
variance du premier facteur. Pour une matrice de correlation 6 x 6 dont toutes les correlations
hors diagonale sont nulles, les six valeurs propres valent 1 et la part du premier facteur vaut
**1 sur 6, soit 16,7 pour cent**. Le plancher de la quantite annoncee n'est donc pas 0, il est
16,7 pour cent.

**Verification arithmetique, avec les valeurs du fichier.** Correlation moyenne mesuree 0,1627.
Sous une structure equicorrelee, la premiere valeur propre attendue vaut
`1 + 5 x 0,1627 = 1,8135`, soit **30,2 pour cent** de la variance. La premiere valeur propre
mesuree vaut 1,855, soit **30,9 pour cent**. L'ecart entre les deux est de 0,7 point : la part
de variance du premier facteur ne dit rien de plus que la correlation moyenne, elle en est une
reecriture. [MESURE, `a9-deviance-un-facteur.csv`]

**L'exces reel sur le plancher est de 14,2 points, pas de 31.**

**Phrase de remplacement.** "Sur Twin-2K-500, la propension individuelle a s'ecarter du mode de
son groupe est partagee entre six domaines : correlations toutes positives, de 0,07 a 0,31,
correlation moyenne 0,163 contre un plancher de permutation de -0,0001 et un 95e centile de
permutation a 0,006 ; le premier facteur explique 30,9 pour cent de la variance, contre
16,7 pour cent attendus sous independance et 30,2 pour cent attendus sous une structure
equicorrelee au meme r moyen." [MESURE]

Le point "Interdit" numero 1 de la meme section, qui refusait deja de presenter le trait de
deviance comme un construit, est confirme et renforce par ce calcul.

### E4. Section 4, "Autorise" point 8 : le 71,2 contre 79,5 melange le jeu d'items et le delai. Objection a17 5.5, contradiction C7.

**Phrase d'origine.** "La stabilite test retest humaine vaut 71,2 pour cent sur ce materiel,
contre 79,5 pour cent sur le GSS : le denominateur de normalisation depend du jeu d'items et
n'est pas transferable."

**Correction.** Les deux denominateurs ne different pas seulement par le jeu d'items. a8
section 8 point 6 signale que le retest de Twin-2K-500 porte sur "un delai variable de deux a
quatre semaines selon la vague d'origine", la ou le retest du GSS est a deux semaines fixes.
`a12-delai-de-retest.md` demontre precisement que le delai deplace le denominateur, en le
faisant passer de 77,79 pour cent a deux semaines a 69,53 a deux ans sur le panel GSS. Les huit
points d'ecart entre 71,2 et 79,5 contiennent donc au moins deux composantes que ce rapport ne
separe pas, et deux rapports de la meme nuit se contredisent sur ce point.

**Phrase de remplacement.** "La stabilite test retest humaine vaut 71,2 pour cent sur ce
materiel contre 79,5 pour cent sur le GSS. Le denominateur de normalisation depend du jeu
d'items **et** du delai, qui n'est pas le meme des deux cotes, deux a quatre semaines variables
contre deux semaines fixes. Il n'est transferable ni d'un jeu a l'autre ni d'un protocole a
l'autre, et l'ecart de huit points ne doit pas etre attribue au seul materiel." [MESURE pour
les deux valeurs, [PROBABLE] pour le partage entre les deux causes, qui n'est pas fait.]

Le point "Interdit" numero 4 de la meme section, qui refuse deja de comparer un score normalise
de ce rapport a un score normalise du papier de Stanford, reste valable et couvre le meme
risque.

### E5. Ce que ces errata ne changent pas

Le protocole de la tache A10, le controle par les items stables et instables, le centrage par
item, le temoin de permutation, l'ensemble de la tache A11 sur l'exces de coherence et la
tache 3 sur la structure de l'instabilite humaine ne sont pas touches. Aucun chiffre mesure
n'est retire : ce sont trois rapprochements et une attribution de cause qui le sont.

---

Deux constructions psychologiques testables a zero appel de modele, mesurees sur
Twin-2K-500. Correspond aux fiches A10 et A11 de BRAINSTORM.md, plus une troisieme
mesure preparatoire au correctif E2u de `exploration/09-angles-de-contribution.md`.

Travail du 7 septembre 2026. Aucun appel de modele de langage, aucune microdonnee
recopiee hors de `data/`. Scripts `analyses/a9_commun.py`, `a9_deviance.py`,
`a9_coherence.py`, `a9_instabilite.py`. Duree totale d'execution environ trois minutes.

Convention de lecture. Chaque affirmation non triviale porte [MESURE] si le chiffre a ete
calcule ici, [CONFIRME] s'il vient d'un fichier ou d'un rapport verifie, [PROBABLE] pour
une inference etayee, [HYPOTHESE] pour un pari.

---

## Reponse en une ligne, par tache

**Tache 1, A10.** Le trait de deviance existe, il est faible et il n'est pas ce qu'on
croyait : la propension a devier du mode de son groupe correle de 0,07 a 0,31 entre
domaines, un facteur unique en explique 31 pour cent contre un plancher de permutation nul,
mais la moitie de cette communaute disparait quand on retire la simple instabilite du
repondant, et ce qui reste est porte par les items ou la personne est stable, pas par ceux
ou elle hesite [MESURE]. Les agents, eux, devient deux fois moins souvent que les humains,
ratio 0,45 a 0,66, et ne reproduisent le classement des personnes qu'a r = 0,27 au mieux et
r = 0,03 au pire [MESURE].

**Tache 2, A11.** L'exces de coherence des agents n'est ni uniforme ni meme toujours
positif : sur la batterie d'attitudes politiques l'alpha passe de 0,872 chez les humains a
0,967 chez les agents et la correlation inter items de 0,41 a 0,74, alors que sur les 40
decisions d'achat le meme agent est **moins** coherent que les humains, alpha 0,814 contre
0,444 [MESURE]. Le gonflement le plus violent n'est pas dans une echelle mais **entre** deux
batteries de contenu apparie : la correlation entre l'opinion propre et le consensus percu
sur la meme politique passe de 0,20 a 0,72 [MESURE].

**Tache 3.** L'instabilite humaine reelle est structuree sur trois dimensions mesurables et
aucun bruit simple ne la reproduit : 28,8 pour cent de changements entre vagues, dont
66,4 pour cent de la variance inter personnes n'est pas du tirage, un taux par item qui
correle a 0,91 avec l'entropie de l'item, et une amplitude de changement de 1,43 crans
contre 2,25 pour un bruit uniforme et 1,00 pour un bruit purement adjacent [MESURE].

---

## 0. Ce que contient reellement le jeu, et ce que cela impose au protocole

Verifie fichier par fichier avant de calculer quoi que ce soit.

| fait | source | consequence |
|---|---|---|
| 2 058 participants, `pid` de 1 a 2 058 | `wave1_3_response.csv` | aucune |
| 256 identifiants au catalogue, environ 500 questions posees, 760 colonnes de CSV | `question_catalog_README.md` [CONFIRME] | le comptage retenu ici est la colonne de CSV |
| 623 colonnes categorielles exploitables en vagues 1 a 3, dont 14 demographies, soit 609 items d'analyse ; 108 en vague 4 | [MESURE] | les 108 recoupent exactement le decompte de `a2-baselines.md` section 3.2 |
| les 126 colonnes de la vague 4 existent toutes dans le fichier des vagues 1 a 3 | [MESURE] | le test retest est disponible sur la totalite des items reposes |
| **aucune sortie LLM ne porte sur les items de personnalite** | [MESURE] | A11 ne peut pas etre traitee sur le BFI-44 en comparaison humain / agent |
| `default_gpt41mini_wave4.csv` est la vague 4 humaine, accord cellule a cellule 1,000 avec `wave4_response.csv` sur 126 colonnes et 2 058 personnes | [MESURE] | sert de controle de lecture du format des auteurs |
| 16 fichiers dans `data/twin2k500/llm/`, mais **13 configurations distinctes** : `default_gpt41mini_llm.csv` et `spec_texte_gpt41mini.csv` sont identiques octet pour octet, de meme que `demo_only_gpt41mini_llm.csv` et `spec_demo_only_gpt41mini.csv` | [MESURE], somme md5 | ne jamais compter 15 conditions |
| accord humain / agent par defaut sur les cellules renseignees des deux cotes : 0,483 | [MESURE] | ordre de grandeur coherent avec la litterature |

**La contrainte la plus lourde de ce rapport.** Les simulations publiees par les auteurs
portent uniquement sur les 126 colonnes de la vague 4, c'est a dire les experiences
d'heuristiques et de biais, les 40 decisions d'achat, les 10 items de soutien a des
politiques publiques et les items de perception. Le BFI-44 et les quinze autres matrices du
bloc Personality ne sont **pas** simules. La tache 2 est donc scindee : structure humaine de
reference sur la personnalite, comparaison humains contre agents sur les sept batteries
multi items de la vague 4.

---

## 1. Tache A10, le trait de deviance

### 1.1 Protocole

**Indicateur elementaire.** Pour chaque personne *i* et chaque item categoriel *j*, une
indicatrice vaut 1 si la reponse de *i* differe de la modalite majoritaire de son segment
demographique sur *j*. Le mode est calcule **en retirant la personne elle meme du
comptage**, faute de quoi un individu isole dans une petite cellule serait mecaniquement son
propre mode et ne devierait jamais. Egalites tranchees par le code de modalite le plus
petit ; elles portent sur moins d'un pour mille des cellules [MESURE]. Une cellule de moins
de 15 repondants ne produit pas de mesure.

**Segmentations.** Six, construites a partir des 14 questions du bloc Demographics : genre
(QID12), age (QID13), education (QID14), ethnicite (QID15), ideologie politique (QID22), et
un profil croise genre x age x ideologie, soit 40 cellules pour 2 058 personnes, la plus
petite a 9 personnes. Une septieme reference, le mode de la population entiere, sert de
temoin.

**Domaines.** Six, construits a partir du champ `BlockName` du catalogue : personnalite
275 items, cognitif 50, economique 176, prix 40, heuristiques et biais 58, attitudes
politiques 10. Les 14 items demographiques, les curseurs et les saisies libres sont exclus.
Les 21 items de l'inventaire de depression, poses en choix multiple, sont ramenes a une
colonne chacun par la position la plus elevee cochee, cotation habituelle du BDI ;
91,3 pour cent des 43 217 reponses concernees ne cochent qu'une option [MESURE].

### 1.2 Le niveau de deviance, et un premier resultat inattendu

`resultats/a9-deviance-niveaux.csv`.

| domaine | items | taux de deviance, profil croise | ecart type inter personnes | taux contre le mode de la population entiere |
|---|---|---|---|---|
| personnalite | 275 | 0,592 | 0,073 | 0,589 |
| cognitif | 50 | 0,312 | 0,145 | 0,312 |
| economique | 176 | 0,257 | 0,092 | 0,252 |
| prix | 40 | 0,447 | 0,137 | 0,431 |
| heuristiques et biais | 58 | 0,512 | 0,119 | 0,494 |
| attitudes politiques | 10 | 0,559 | 0,216 | 0,610 |

[MESURE] **Segmenter ne change presque rien.** Passer du mode de la population entiere au
mode d'un profil croise genre x age x ideologie deplace le taux de deviance de moins de
2 points sur cinq domaines sur six. Le seul mouvement notable est sur les attitudes
politiques, de 0,610 a 0,559, ce qui est attendu puisque le segment contient l'ideologie
declaree. Dit autrement : **la demographie ne dit presque rien de qui devie**. Ce n'est pas
une limite du protocole, c'est le point de depart du sujet.

### 1.3 La stabilite inter domaines, avec son plancher de bruit

`resultats/a9-deviance-correlations-domaines.csv`,
`a9-deviance-fiabilite.csv`, `a9-deviance-un-facteur.csv`. Segmentation profil croise.

Fiabilite par moities, corrigee de Spearman-Brown, 50 partages aleatoires :
personnalite 0,852, economique 0,888, cognitif 0,844, prix 0,687, attitudes 0,536,
heuristiques et biais 0,409 [MESURE]. Les deux derniers domaines sont peu fiables, il faut
le dire avant de lire leurs correlations.

Matrice domaine x domaine, correlation de Pearson brute, et entre parentheses desattenuee
par les fiabilites ci dessus :

| | cognitif | economique | prix | heuristiques | attitudes |
|---|---|---|---|---|---|
| personnalite | 0,161 (0,19) | 0,151 (0,17) | 0,075 (0,10) | 0,140 (0,24) | 0,085 (0,13) |
| cognitif | | 0,276 (0,32) | 0,257 (0,34) | 0,309 (0,53) | 0,184 (0,27) |
| economique | | | 0,098 (0,13) | 0,214 (0,35) | 0,095 (0,14) |
| prix | | | | 0,162 (0,31) | 0,122 (0,20) |
| heuristiques | | | | | 0,115 (0,25) |

[MESURE] Correlation moyenne hors diagonale 0,163 brute, 0,243 desattenuee. Toutes les
correlations sont positives. Premiere valeur propre 1,855 sur 6 domaines, soit **30,9 pour
cent de la variance** pour un facteur unique, 38,1 pour cent sur la matrice desattenuee.
Seconde valeur propre 0,965, donc un seul facteur se detache.

**Plancher de bruit.** Vingt permutations independantes par domaine, qui detruisent le lien
individuel en conservant les marges : correlation moyenne inter domaines **-0,0001**,
95e centile 0,0057 [MESURE]. Le signal n'est donc pas un artefact de construction.

**Temoin de composition.** Les experiences d'economie comportementale sont en inter sujets,
chaque personne ne voit qu'une condition. Un score agrege pourrait donc dependre du
sous ensemble d'items tire et non de la personne. Les correlations recalculees apres
centrage de chaque item sur son propre taux moyen sont inchangees a 0,02 pres, sauf sur les
paires impliquant les heuristiques ou l'ecart atteint 0,024 [MESURE]. Le resultat humain
n'est pas un effet de composition.

### 1.4 Le controle indispensable : deviance contre instabilite

`resultats/a9-deviance-controles.csv`, `a9-deviance-correlations-partielles.csv`,
`a9-deviance-items-stables.csv`.

La consistance test retest de la personne est calculee sur les 108 items reposes en
vague 4 : part des items ou la reponse est identique aux deux vagues.

[MESURE] **La deviance moyenne sur les six domaines correle a -0,535 [-0,568 ; -0,502] avec
la consistance test retest.** C'est plus fort encore que le r = 0,684 entre fidelite d'agent
et stabilite propre releve en section 6 de `a1-double-distorsion.md` sur le GSS. Le confondu
est donc massif et il devait etre traite.

Correlations partielles inter domaines, moyenne sur les 15 paires :

| controle retire | r moyen | minimum | maximum |
|---|---|---|---|
| aucun | 0,163 | 0,075 | 0,309 |
| consistance test retest | 0,089 | 0,016 | 0,198 |
| consistance, style extreme, style milieu, acquiescement, non reponse | 0,075 | 0,002 | 0,183 |

[MESURE] **Retirer la seule instabilite du repondant divise la communaute inter domaines par
1,8.** Ajouter les styles de reponse ne retire presque plus rien. Ce qui reste,
r moyen 0,075 a 0,089, est encore quinze fois le plancher de permutation, mais c'est un
effet faible.

Les styles de reponse ne sont pas la cause : le style extreme correle a -0,037
[-0,080 ; 0,013] avec la deviance moyenne, le style milieu a 0,168, l'acquiescement a 0,121,
le taux de non reponse a 0,049 [MESURE]. L'hypothese "la deviance n'est qu'un style de
reponse extreme" est donc ecartee par la mesure, ce qui est contre intuitif et important.

**Le test decisif, la deviance calculee sur les seuls items stables de la personne.** Sur
les 108 items reposes, on separe ceux ou la personne a donne la meme reponse aux deux vagues
de ceux ou elle a change. Puis on correle chacune des deux deviances avec la deviance dans
les domaines non reposes.

| domaine cible (items non reposes) | r avec la deviance sur items **stables** | r avec la deviance sur items **instables** | r sur items stables, consistance partialisee |
|---|---|---|---|
| personnalite | 0,143 | 0,032 | 0,099 |
| cognitif | 0,361 | 0,032 | 0,246 |
| economique | 0,175 | 0,028 | 0,087 |

[MESURE] Taux de deviance moyen 0,434 sur les items stables de la personne, 0,619 sur ses
items instables. **Le signal inter domaines est porte par les items ou la personne ne change
pas d'avis, pas par ceux ou elle hesite.** C'est le resultat le plus solide de la tache 1 :
il retourne l'objection au lieu de la subir. Un artefact d'instabilite produirait le profil
exactement inverse.

### 1.5 La stabilite temporelle de la deviance

`resultats/a9-deviance-retest.csv`, sur les 108 items reposes, deux semaines d'ecart.

| ensemble | items | taux vagues 1 a 3 | taux vague 4 | r test retest | IC 95 pour cent | fiabilite interne |
|---|---|---|---|---|---|---|
| tous | 108 | 0,483 | 0,483 | **0,738** | [0,718 ; 0,758] | 0,669 |
| prix | 40 | 0,447 | 0,457 | 0,755 | [0,734 ; 0,776] | 0,687 |
| attitudes | 10 | 0,559 | 0,545 | 0,674 | [0,647 ; 0,698] | 0,536 |
| heuristiques et biais | 58 | 0,512 | 0,503 | 0,508 | [0,474 ; 0,542] | 0,409 |

[MESURE] La deviance individuelle se reproduit a r = 0,738 a deux semaines, alors que sa
consistance interne entre deux moities du meme ensemble d'items n'est que de 0,669.
**Elle est plus stable dans le temps qu'elle n'est homogene d'un item a l'autre.** Signature
psychometrique nette : ce que l'on mesure n'est pas une propension generale, c'est un
ensemble de positions atypiques attachees a des contenus precis, et ces positions durent.
[PROBABLE] C'est pour cela que la version inter domaines est faible alors que la version
test retest est forte, et c'est la question a poser a Simon.

Reserve honnete : ce r = 0,738 est calcule sur le **meme** ensemble d'items aux deux dates,
il contient donc la part de contenu stable de la personne et pas seulement une propension.
Il n'est pas comparable a une correlation inter domaines.

### 1.6 Les agents ont-ils un trait de deviance ?

`resultats/a9-deviance-llm.csv`, `a9-deviance-llm-domaines.csv`. Treize configurations
distinctes, memes items de vague 4, memes segments demographiques que pour l'humain simule.
Deux references sont calculees : **interne**, le mode du segment calcule sur la population
d'agents, ce qui repond a la question "l'agent devie-t-il de ses semblables" ; **externe**,
le mode humain du segment.

Configurations principales, reference interne :

| configuration | taux de deviance agent | ratio agent / humain | r avec l'humain, brut | r centre par item | temoin de permutation | accord du mode agent et du mode humain |
|---|---|---|---|---|---|---|
| humains | 0,501 | 1,00 | | | | |
| gpt41mini persona texte, defaut | 0,245 | 0,49 | 0,365 | **0,275** | 0,041 | 0,651 |
| gpt41mini texte, repetition | 0,278 | 0,55 | 0,320 | 0,273 | 0,047 | 0,633 |
| gpt41mini texte, temperature par defaut | 0,271 | 0,54 | 0,354 | 0,236 | 0,048 | 0,650 |
| gpt41 persona JSON | 0,286 | 0,57 | 0,269 | 0,268 | 0,043 | 0,638 |
| gemini flash 2.5 texte | 0,329 | 0,66 | 0,315 | 0,063 | 0,042 | 0,483 |
| gpt41mini texte, raisonnement | 0,306 | 0,61 | 0,281 | 0,059 | 0,046 | 0,489 |
| gpt41mini demographies seules | 0,225 | 0,45 | 0,247 | 0,083 | 0,042 | 0,437 |
| gpt41mini affine sur 500 exemples | 0,234 | 0,47 | 0,054 | **0,032** | 0,054 | 0,416 |

[MESURE] **Le taux de deviance des agents vaut 0,45 a 0,66 fois celui des humains.** Cette
fourchette recouvre presque exactement le ratio d'ecarts types intra groupe de 0,40 a 0,56
retenu dans la these du projet. La deviance au mode du groupe est donc une mesure lisible du
meme phenomene, exprimee en pourcentage de reponses et non en ecart type, ce qui est
beaucoup plus facile a expliquer a un acheteur.

[MESURE] **Le classement des personnes n'est reproduit que faiblement.** Apres centrage par
item, qui neutralise la composition du sous ensemble vu par chaque personne, la meilleure
configuration atteint r = 0,275, contre un temoin de permutation a 0,041. Les
demographies seules tombent a 0,083 et le modele affine a 0,032, c'est a dire au niveau du
bruit. Le centrage divise par 2 a 4 les correlations naives : sans lui, on publierait
r = 0,247 pour une condition qui ne connait que la demographie de la personne, ce qui serait
faux.

[MESURE] **Le mode du segment lui meme est faux entre 35 et 60 pour cent du temps.** Pour la
meilleure configuration, la modalite majoritaire des agents d'une cellule demographique
coincide avec celle des humains de la meme cellule dans 65,1 pour cent des cas sur 3 350
couples cellule x item. Pour les demographies seules, 43,7 pour cent.

[MESURE] **Les agents n'ont pas de trait de deviance transversal.** Correlation entre la
deviance d'un agent dans deux domaines, reference interne : chez les humains de la vague 4,
0,147 a 0,170 sur les trois paires disponibles ; chez `gpt41mini_defaut`, -0,097, -0,014,
0,227 ; chez `gpt41mini_resume`, -0,037, 0,116, -0,096. Seul le modele affine sur 500
exemples affiche une structure forte, 0,244 a 0,602, et c'est un symptome de sur coherence
et non de fidelite, cf. tache 2.

**Ce que cela dit de l'identity essentialism.** La formulation de la fiche A10 supposait deux
issues : ou l'agent reproduit la deviance moyenne mais pas le classement, ou il reproduit les
deux. La mesure en donne une troisieme : **l'agent ne reproduit ni le niveau, ni le
classement, ni la structure inter domaines**. Il devie deux fois moins souvent, il devie sur
d'autres personnes, et sa deviance dans un domaine ne dit rien de sa deviance dans un autre.

---

## 2. Tache A11, l'incoherence au bon endroit

### 2.1 La contrainte a annoncer d'emblee

Aucune configuration LLM du depot ne simule les items de personnalite. La comparaison
demandee "alpha humain contre alpha simule sur le BFI-44" **n'est pas realisable sur
Twin-2K-500 en l'etat** [MESURE, verifie sur les 126 colonnes simulees]. Deux volets la
remplacent.

### 2.2 Volet humain : la structure de reference sur la personnalite

`resultats/a9-coherence-personnalite-humains.csv`,
`a9-coherence-bfi-structure-humaine.csv`. 2 058 repondants, vagues 1 a 3.

BFI-44, cles canoniques verifiees contre les libelles des 44 lignes du catalogue :

| facette | items | alpha | r inter items moyen |
|---|---|---|---|
| extraversion | 8 | 0,881 | 0,480 |
| agreabilite | 9 | 0,821 | 0,348 |
| conscience | 9 | 0,874 | 0,452 |
| nevrosisme | 8 | 0,904 | 0,542 |
| ouverture | 10 | 0,845 | 0,365 |

Quinze autres matrices du bloc Personality, cotation alignee sur la premiere composante :
alpha de 0,418 a 0,939, mediane 0,880 [MESURE]. Les deux plus faibles, QID239 a 0,418 et
QID28 a 0,553, sont probablement multidimensionnelles et ne doivent pas servir de reference.

**Structure de l'incoherence humaine sur le BFI**, 946 paires d'items :

| bloc | keyage | paires | r moyen | r absolu moyen |
|---|---|---|---|---|
| meme facette | meme sens | 87 | 0,480 | 0,480 |
| meme facette | sens inverses | 86 | -0,373 | 0,373 |
| facettes differentes | meme sens | 411 | 0,046 | 0,173 |
| facettes differentes | sens inverses | 362 | 0,033 | 0,158 |

[MESURE] Chez l'humain, deux items d'une meme facette cotes en sens inverse correlent
0,107 point **moins fort** en valeur absolue que deux items cotes dans le meme sens. C'est
l'artefact classique de l'item inverse. C'est la reference contre laquelle un agent doit
etre mesure, et c'est exactement le point ou l'on attend qu'il echoue.

### 2.3 Volet humains contre agents, sept batteries de la vague 4

Sept batteries multi items simulees : soutien a 10 politiques publiques (QID287, Likert 5),
consensus percu sur les memes 10 politiques (QID290, curseur 0 a 100), benefice percu de
4 objets (QID288, echelle 7), risque percu des memes 4 objets (QID289, echelle 7),
40 decisions d'achat (QID9, binaire), deux problemes d'appariement de probabilites (QID198
10 items, QID203 6 items, binaires, chacun vu par la moitie de l'echantillon).

Les cles de signe sont estimees une fois sur les humains, par la premiere composante, puis
appliquees telles quelles aux agents : sans cela deux alphas ne seraient pas comparables.

**Alpha de Cronbach, humains contre agents :**

| batterie | humains | gpt41mini defaut | gpt41 JSON | gemini flash | demo seules | affine 500 |
|---|---|---|---|---|---|---|
| soutien aux politiques, 10 items | **0,872** | 0,967 | 0,969 | 0,990 | 0,898 | 0,805 |
| consensus percu, 10 items | **0,816** | 0,966 | 0,964 | 0,862 | 0,911 | 0,934 |
| benefice percu, 4 items | **0,564** | 0,621 | 0,698 | 0,460 | 0,527 | 0,942 |
| risque percu, 4 items | **0,545** | 0,692 | 0,426 | 0,596 | 0,720 | 0,994 |
| decisions d'achat, 40 items | **0,814** | 0,444 | 0,634 | 0,612 | 0,847 | 0,996 |

[MESURE] Le diagnostic "alpha gonfle chez les repondants synthetiques" **n'est vrai que sur
une partie des instruments**. Il l'est massivement sur les deux batteries d'attitude
verbale, 0,872 vers 0,967 et 0,816 vers 0,966. Il est faux, et meme inverse, sur les
40 decisions d'achat, 0,814 vers 0,444 : l'agent ne reproduit pas la propension generale a
acheter qui structure les reponses humaines.

### 2.4 Ou l'exces de coherence se concentre

`resultats/a9-coherence-structure-vague4.csv`, `a9-coherence-par-couple-echelles.csv`,
`a9-coherence-par-categorie-de-paire.csv`, `a9-coherence-items-inverses.csv`.

Sur l'ensemble des paires d'items, configuration `gpt41mini_defaut`, 2 278 paires :
correlation des correlations 0,716, pente de la regression des correlations agent sur
humaines **1,497**, RMSE 0,172, exces moyen de coherence en valeur absolue +0,020 [MESURE].
Cet exces moyen de +0,020 est trompeur, et c'est le point de la section.

**Detail par couple de batteries, `gpt41mini_defaut` :**

| couple | paires | r absolu humain | r absolu agent | exces |
|---|---|---|---|---|
| soutien x consensus percu (memes politiques) | 100 | 0,198 | 0,723 | **+0,525** |
| consensus percu, interne | 45 | 0,325 | 0,712 | +0,387 |
| soutien aux politiques, interne | 45 | 0,406 | 0,742 | +0,335 |
| risque percu x consensus percu | 40 | 0,047 | 0,231 | +0,184 |
| soutien x risque percu | 40 | 0,075 | 0,240 | +0,165 |
| risque percu, interne | 6 | 0,253 | 0,386 | +0,133 |
| benefice percu x consensus percu | 40 | 0,040 | 0,155 | +0,115 |
| benefice percu, interne | 6 | 0,211 | 0,286 | +0,076 |
| soutien x benefice percu | 40 | 0,101 | 0,150 | +0,049 |
| benefice x risque percu (memes objets) | 16 | 0,150 | 0,150 | -0,001 |
| soutien x decisions d'achat | 400 | 0,026 | 0,022 | -0,004 |
| consensus x decisions d'achat | 400 | 0,038 | 0,025 | -0,014 |
| **decisions d'achat, interne** | 780 | **0,099** | **0,029** | **-0,069** |

[MESURE] **L'exces n'est pas uniforme, il est signe.** Il est maximal entre deux batteries
de contenu apparie, fort a l'interieur des batteries d'attitude verbale, nul entre attitude
et achat, et **negatif a l'interieur de la batterie d'achat**. Concentration : 43,1 pour cent
de l'exces positif total est porte par le decile de paires le plus charge, indice de Gini
des exces positifs 0,679, et seulement 34,7 pour cent des paires sont plus coherentes chez
l'agent que chez l'humain [MESURE].

**La paire la plus revelatrice.** Les 100 paires soutien x consensus percu opposent
"soutenez vous cette politique" et "quel pourcentage du public la soutient". Chez les
humains la correlation absolue moyenne vaut 0,198, ce qui est l'effet de faux consensus,
reel et modere. Chez l'agent elle vaut 0,723. Les vingt cinq paires de plus fort exces sont
**toutes** de ce type, jusqu'a r humain -0,014 contre r agent -0,843 [MESURE]. **L'agent ne
distingue pas son opinion de sa croyance sur l'opinion des autres.**

**Les items inverses.** Sur les 45 paires internes a la batterie de soutien, 16 opposent des
items cotes en sens inverse, les deux items conservateurs "augmenter les expulsions" et
"cheques sante pour les seniors".

| configuration | paires meme sens, r absolu | paires sens inverses, r absolu | exces meme sens | exces sens inverses |
|---|---|---|---|---|
| humains | 0,492 | 0,251 | | |
| gpt41mini defaut | 0,840 | 0,563 | +0,348 | +0,313 |
| gemini flash texte | 0,909 | 0,916 | +0,417 | **+0,666** |
| gpt41 JSON, sortie predite | 0,892 | 0,811 | +0,400 | +0,561 |
| gpt41mini resume JSON | 0,698 | 0,046 | +0,206 | **-0,205** |
| gpt41mini demo seules | 0,719 | 0,230 | +0,226 | -0,021 |

[MESURE] Les humains attenuent la coherence sur les paires inversees, 0,492 vers 0,251. Les
agents les plus coherents **suppriment cette attenuation** : gemini flash atteint 0,916 sur
les paires inversees contre 0,909 sur les paires directes, c'est a dire une personne dont
l'opinion politique est un axe parfait sans aucune particularite. [PROBABLE] C'est la
signature la plus nette d'un raisonnement par etiquette ideologique plutot que par position
individuelle sur chaque question.

**Pourquoi c'est plausible.** [HYPOTHESE] Trois mecanismes candidats, non separes par cette
mesure. Un, les dix politiques de QID287 sont des marqueurs partisans bien connus, et le
modele les traite comme une seule variable latente "gauche ou droite" au lieu de dix
positions ; cela explique a la fois l'alpha a 0,97 et la disparition de l'artefact d'item
inverse. Deux, les questions de soutien et de consensus percu sont posees dans les memes
termes et parfois dans la meme session, ce qui est une paraphrase quasi litterale ; le
modele repond deux fois a la meme chose. Trois, les 40 decisions d'achat portent sur des
produits concrets sans marqueur identitaire, le modele n'a pas de stereotype a mobiliser, et
la coherence s'effondre au lieu de gonfler. Ces trois mecanismes predisent tous la meme
regle : **l'exces de coherence suit la charge identitaire du contenu, pas la structure
psychometrique de l'instrument**. Cette regle est testable et ne l'a pas encore ete.

### 2.5 La figure

`resultats/a9-figure-coherence.png` et `.svg`. Trois panneaux. A gauche la matrice de
correlation humaine des dix items de soutien aux politiques, au centre la meme matrice pour
`gpt41mini_defaut`, a droite le nuage des correlations paire par paire, humain en abscisse
et agent en ordonnee, sur les 2 278 paires, avec la diagonale d'egalite. Le nuage montre
d'un coup les trois regimes : un peloton au dessus de la diagonale pour les paires
d'attitude, un amas serre autour de zero et legerement sous la diagonale pour les paires
d'achat, et les paires de contenu apparie loin au dessus.

---

## 3. Tache 3, la structure de l'instabilite humaine reelle

`resultats/a9-instabilite-resume.csv`, `a9-instabilite-ampleur.csv`,
`a9-instabilite-par-item.csv`, `a9-instabilite-par-domaine.csv`. 108 items reposes,
168 768 cellules appariees.

**Combien.** Taux de changement global entre vagues 1 a 3 et vague 4, deux semaines d'ecart :
**28,8 pour cent**, soit une stabilite de 71,2 pour cent [MESURE]. A comparer au plancher de
79,53 pour cent du GSS a deux semaines [CONFIRME, `a1-double-distorsion.md` section 6]. Le
plancher humain n'est donc pas une constante universelle : il depend du jeu d'items, et un
score normalise par 0,795 sur un materiel de ce type serait trop flatteur de 8 points.

**Qui.** Ecart type inter personnes du taux de changement 0,086, contre 0,050 attendu si
toutes les personnes avaient le meme taux, avec 82 items par personne en moyenne. **66,4 pour
cent de la variance inter personnes n'est pas imputable au tirage** [MESURE]. L'instabilite
est elle meme une caracteristique individuelle, et pas un bruit de mesure homogene.

**Sur quels items.** Taux par item de 0,062 a 0,640, ecart type 0,169. Correlation entre le
taux de changement d'un item et son entropie de Shannon : **0,912**. Avec le nombre de
modalites : 0,870 [MESURE]. Par domaine : prix 0,161, attitudes 0,384, heuristiques et
biais 0,407.

**Vers quoi.** Probabilite de changer quand la reponse initiale est le mode de l'item :
0,208. Quand elle ne l'est pas : 0,376 [MESURE]. C'est le mecanisme qui explique le
r = -0,535 de la section 1.4. En revanche, parmi les changements, 37,1 pour cent aboutissent
au mode, contre 37,9 pour cent attendus si la nouvelle reponse etait tiree dans la marginale
de l'item en excluant la reponse anterieure [MESURE]. **Il n'y a pas de regression vers le
mode** : les gens quittent plus souvent une position minoritaire, mais ils n'y reviennent
pas plus souvent vers la majorite qu'un tirage au sort ne le ferait.

**De combien de crans.** Sur les 18 items a echelle ordinale explicite :

| amplitude, en crans | observe | bruit uniforme | bruit marginal | bruit adjacent |
|---|---|---|---|---|
| 1 | 0,697 | 0,360 | 0,480 | 1,000 |
| 2 | 0,213 | 0,277 | 0,279 | 0 |
| 3 | 0,064 | 0,188 | 0,151 | 0 |
| 4 et plus | 0,026 | 0,175 | 0,090 | 0 |
| **amplitude moyenne** | **1,426** | 2,252 | 1,871 | 1,000 |
| distance de variation totale a l'observe | 0 | 0,337 | 0,217 | 0,303 |

[MESURE] **Aucun des trois modeles de bruit ne reproduit l'instabilite humaine**, et ils
echouent dans deux directions opposees : le bruit uniforme et le bruit marginal sont trop
larges, le bruit adjacent est trop etroit. Le meilleur des trois, le bruit marginal, est
encore a 0,217 de distance de variation totale.

**Ce que cela donne comme cahier des charges pour un correctif.** Un modele d'injection
d'incoherence structuree doit satisfaire simultanement quatre contraintes mesurees ici :
probabilite de changement proportionnelle a l'entropie de l'item, r = 0,91 ; probabilite
d'environ 0,21 depuis le mode et 0,38 hors du mode ; amplitude moyenne de 1,43 cran avec
70 pour cent de pas unitaires ; et une variance inter personnes du taux dont deux tiers sont
de la vraie heterogeneite. C'est un modele a quatre parametres, tous estimes, et aucun ne
demande d'appel de modele de langage.

---

## 4. Ce que ces resultats autorisent a ecrire, et ce qu'ils interdisent

### Autorise

1. "Sur Twin-2K-500, la propension individuelle a s'ecarter du mode de son groupe est
   partagee entre six domaines : correlations toutes positives, de 0,07 a 0,31, un facteur
   unique expliquant 31 pour cent de la variance, contre un plancher de permutation de
   0,000." [MESURE]
2. "Cette communaute n'est pas un artefact de l'instabilite du repondant : elle est portee
   par les items sur lesquels la personne donne deux fois la meme reponse, r = 0,14 a 0,36,
   et pas par ceux ou elle change, r = 0,03." [MESURE]
3. "Elle est neanmoins faible : partialiser la seule consistance test retest la ramene de
   0,163 a 0,089 en moyenne." [MESURE]
4. "Les agents de langage devient de leur groupe 0,45 a 0,66 fois moins souvent que les
   humains qu'ils simulent, et ne reproduisent le classement des individus qu'a r = 0,275 au
   mieux, apres neutralisation de la composition des items." [MESURE]
5. "Le mode d'une cellule demographique est faux, chez les agents, dans 35 a 60 pour cent des
   couples cellule x item." [MESURE]
6. "L'exces de coherence des repondants synthetiques n'est pas uniforme : il est concentre
   sur les contenus a charge identitaire, il atteint +0,53 de correlation entre deux
   batteries de contenu apparie, et il s'inverse sur des items de choix concret ou l'alpha
   passe de 0,81 chez les humains a 0,44 chez l'agent." [MESURE]
7. "Les agents suppriment l'attenuation de coherence que les humains presentent sur les items
   cotes en sens inverse." [MESURE]
8. "La stabilite test retest humaine vaut 71,2 pour cent sur ce materiel, contre 79,5 pour
   cent sur le GSS : le denominateur de normalisation depend du jeu d'items et n'est pas
   transferable." [MESURE]
9. "Le depot Twin-2K-500 contient 16 fichiers de simulation mais 13 configurations
   distinctes, deux couples etant identiques octet pour octet." [MESURE]

### Interdit

1. Ecrire que le trait de deviance est etabli comme un construit. Un facteur unique a
   31 pour cent, ramene a environ 0,09 de correlation moyenne apres controle, est un signal,
   pas un construit. Il faudrait au minimum un modele a facteur latent estime proprement, une
   validation sur un second jeu de donnees, et une correlation avec une mesure externe.
2. Ecrire que l'alpha de Cronbach des repondants synthetiques est gonfle, sans dire sur quoi.
   Sur les 40 decisions d'achat il est effondre. La formulation defendable est
   "l'exces porte sur les instruments d'attitude verbale".
3. Presenter le r = 0,738 de stabilite test retest de la deviance comme une preuve de trait :
   il est calcule sur les memes items aux deux dates et contient la position stable de la
   personne.
4. Comparer un score normalise de ce rapport a un score normalise du papier de Stanford. Les
   denominateurs sont differents, 0,712 ici, 0,795 la bas, et le materiel n'est pas le meme.
5. Utiliser les correlations agent / humain **non centrees par item** de la colonne
   `r_agent_humain`. Elles sont gonflees d'un facteur 2 a 4 par la composition du sous
   ensemble d'items vu par chaque personne, effet des experiences inter sujets.
6. Tirer quoi que ce soit des domaines "heuristiques et biais" et "attitudes" pris seuls :
   leurs fiabilites internes, 0,409 et 0,536, sont trop basses.
7. Generaliser hors des Etats Unis et hors du materiel Twin-2K-500. Un seul echantillon, une
   seule periode, un questionnaire tres long.

---

## 5. Ce que je n'ai pas pu verifier

1. **La comparaison humain / agent sur le BFI-44 et les echelles de personnalite.** Aucune
   simulation publiee ne couvre ces items. Elle demanderait de generer nos propres sorties,
   ce qui est possible en local mais sort du cadre "zero appel" de cette session.
2. **Le nom du construit.** Je n'ai lance aucune recherche bibliographique dans cette
   session : le protocole imposait zero appel de modele et je n'ai pas consulte de source
   externe. La question du nom reste ouverte, section 6.
3. **Un modele a facteur latent en bonne et due forme.** Je rapporte la part de variance de
   la premiere composante d'une matrice de correlation a six variables et sa version
   desattenuee. Ce n'est pas une analyse factorielle confirmatoire, il n'y a ni indice
   d'ajustement, ni test de la solution a un facteur contre deux.
4. **La separation des trois mecanismes candidats de la section 2.4.** Charge identitaire,
   paraphrase et absence de stereotype produisent ici les memes predictions. Les separer
   demande de generer des variantes de questions, donc des appels.
5. **L'effet de l'ordre des questions.** Les vagues 1 a 3 et la vague 4 ne presentent pas les
   items dans le meme contexte. Une part du 28,8 pour cent de changement peut etre un effet
   de contexte et non de l'instabilite de la personne. Le jeu ne permet pas de trancher.
6. **La validite de la cotation des items inverses hors BFI.** Pour les quinze autres
   matrices de personnalite, les signes sont alignes empiriquement sur la premiere
   composante, faute de cles publiees dans le catalogue. Les alphas correspondants sont donc
   des maxima optimistes.
7. **Les correlations partielles ne prouvent pas une causalite.** Partialiser la consistance
   test retest retire aussi une part de vraie deviance, puisque les deux sont liees par
   construction. Le chiffre de 0,089 est donc un plancher, pas une estimation non biaisee.
8. **Le taux de deviance des agents en reference externe** n'a pas de plancher de reference :
   je le rapporte, je ne l'interprete pas.

---

## 6. Questions ouvertes pour Simon

Formulees pour qu'un psychologue social puisse trancher sans refaire le calcul.

1. **Le nom.** Une propension individuelle a s'ecarter de la position modale de son groupe,
   faiblement transversale, r moyen 0,09 a 0,16 selon le controle, et fortement stable dans
   le temps sur un contenu donne, r = 0,74 a deux semaines. Est ce un construit nomme ?
   Les candidats que je vois de loin sont le besoin d'unicite, la reactance, la
   non conformite, l'independance de jugement au sens d'Asch, ou une simple distance au
   centroide latente. Si l'un existe et a une echelle validee, A10 cesse d'etre un pari et
   devient une replication, ce qui change sa priorite.
2. **Le profil psychometrique inverse.** Notre mesure est **plus stable dans le temps**,
   0,738, **qu'elle n'est homogene entre items**, 0,669. Est ce le profil d'un trait, celui
   d'une attitude specifique, ou celui d'un artefact de contenu ? En psychometrie classique
   ce profil me semble anormal, et c'est le point sur lequel je suis le moins sur.
3. **Le controle par les items stables est il suffisant ?** Nous mesurons la deviance sur les
   items ou la personne donne deux fois la meme reponse, et elle predit la deviance ailleurs,
   0,14 a 0,36, alors que la deviance sur ses items instables ne predit rien, 0,03. Un
   psychologue trouverait il ce controle convaincant, ou reste-t-il un confondu evident que
   je ne vois pas ?
4. **L'attenuation sur item inverse.** Chez nos humains, deux items d'une meme facette du
   BFI cotes en sens inverse correlent 0,373 en valeur absolue contre 0,480 pour deux items
   de meme sens. Est ce l'ordre de grandeur attendu dans la litterature, ou notre echantillon
   est il particulier ? La reponse determine si "l'agent supprime l'attenuation" est un
   resultat ou un artefact d'echantillon.
5. **Faux consensus.** La correlation entre l'opinion propre et le consensus percu vaut 0,198
   chez nos humains et 0,723 chez l'agent. Quelle est la valeur admise de l'effet de faux
   consensus dans la litterature ? Si 0,198 est deja dans la fourchette normale, alors
   l'agent triple un effet documente, ce qui est un resultat publiable en soi.
6. **L'incoherence attitudinale a-t-elle une litterature de structure ?** Notre tache 3 donne
   quatre parametres, entropie, position modale, amplitude, heterogeneite inter personnes.
   Existe-t-il un modele psychometrique publie de la structure de l'instabilite attitudinale
   auquel comparer ces quatre chiffres, plutot que de les publier comme neufs ?
7. **La question d'arbitrage.** Entre A10, dont le signal est reel mais faible, et A11, dont
   le resultat est fort, chiffre et directement lisible par un acheteur, lequel merite le
   temps ? Mon avis est A11, et la raison est dans la section 2.4 : l'exces de coherence est
   signe et localise, donc corrigeable de facon ciblee, alors qu'un trait de deviance a
   r = 0,09 ne se modelisera pas utilement.

---

## 7. Reproduction

```
.venv/bin/python analyses/a9_deviance.py      # environ 2 minutes
.venv/bin/python analyses/a9_coherence.py     # environ 10 secondes, ecrit la figure
.venv/bin/python analyses/a9_instabilite.py   # environ 4 secondes
```

Graine 20260907 partout. `analyses/a9_commun.py` porte la lecture du catalogue, la
construction des segments et la deviance ; il n'est importe que par les trois scripts ci
dessus. `analyses/a2_commun.py` n'a pas ete modifie.

Tableaux produits, tous agreges, aucune ligne individuelle :

| fichier | contenu |
|---|---|
| `a9-deviance-niveaux.csv` | taux de deviance par segmentation et par domaine |
| `a9-deviance-correlations-domaines.csv` | matrice domaine x domaine, brute, Spearman, centree, desattenuee |
| `a9-deviance-fiabilite.csv` | fiabilite par moities de la deviance, par domaine |
| `a9-deviance-un-facteur.csv` | part du premier facteur et plancher de permutation |
| `a9-deviance-controles.csv` | liens avec consistance, styles de reponse, non reponse |
| `a9-deviance-correlations-partielles.csv` | matrice inter domaines sous trois jeux de controles |
| `a9-deviance-retest.csv` | stabilite test retest de la deviance |
| `a9-deviance-items-stables.csv` | le controle decisif, items stables contre items instables |
| `a9-deviance-llm.csv` | 13 configurations, niveau, classement, accord des modes |
| `a9-deviance-llm-domaines.csv` | matrice inter domaines des agents |
| `a9-coherence-personnalite-humains.csv` | alpha des 21 echelles de personnalite humaines |
| `a9-coherence-bfi-structure-humaine.csv` | structure du BFI par facette et par keyage |
| `a9-coherence-alpha-vague4.csv` | alpha par batterie et par source |
| `a9-coherence-structure-vague4.csv` | correlation des correlations, RMSE, concentration |
| `a9-coherence-par-categorie-de-paire.csv` | exces par categorie de paire |
| `a9-coherence-par-couple-echelles.csv` | exces par couple de batteries, toutes configurations |
| `a9-coherence-items-inverses.csv` | exces sur les paires d'items cotes en sens inverse |
| `a9-coherence-paires-extremes.csv` | les 25 paires de plus fort exces |
| `a9-instabilite-resume.csv` | douze mesures de la structure de l'instabilite |
| `a9-instabilite-ampleur.csv` | amplitude observee contre trois modeles de bruit |
| `a9-instabilite-par-item.csv` | taux de changement des 108 items reposes |
| `a9-instabilite-par-domaine.csv` | idem, agrege par domaine |
| `a9-figure-coherence.png` et `.svg` | la figure de la section 2.5 |
