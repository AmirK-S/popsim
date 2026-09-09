# a39. Les tranches de Peng, rejouees sur nos donnees

## Errata du 9 septembre 2026

Corrections apportees a la suite de la seconde relecture adverse,
`resultats/a45-relecture-adverse-2.md`. **Le corps du rapport n'est pas reecrit** ; chaque
point cite la phrase d'origine, donne la correction et donne la preuve. Recalculs :
`analyses/a47_chute_segmentations.py`, `analyses/a47_verifications.py` et
`analyses/a47_income_v6.py` ; tableaux `resultats/a47-*.csv` ; synthese
`resultats/a47-errata-2.md`. Aucun script existant n'a ete modifie, aucun appel de modele
de langage, lecture seule sur `data/` et sur les caches de a25, a28 et a35.

### E1. Lignes 47, 353 et 448 : « seule l'etiquette bouge » devient un contraste de conditionnement. Objection a45 numero 1, contradiction D1.

**Phrase d'origine.** « Mais sur le seul couple ou le modele, les personnes, les questions et
les traces sont constants et ou **seule l'etiquette bouge**, C2 contre C3, l'ecart sur le
milieu ordinal vaut moins 0,0067 [moins 0,0167 ; 0,0035] [...] Leur egalite du milieu est
donc **un fait d'ablation**, et elle se reproduit chez nous exactement la ou elle est une
ablation. »

**Correction.** Le couple C2 contre C3 n'est pas une ablation : les deux invites echangent
integralement leur entree. La formule juste est « sur notre contraste de conditionnement,
etiquette seule contre 119 reponses de la personne ». La phrase « elle se reproduit
exactement la ou elle est une ablation » perd son support, puisque le dossier ne possede pas
d'ablation d'etiquette.

**Ce que les deux invites contiennent, mesure sur le code.**
[CONFIRME, `analyses/a5_agents_locaux_gss.py`, `systeme_c2` lignes 164 a 177 et `systeme_c3`
lignes 180 a 196]

| | contenu de l'invite systeme | etiquette ideologique | reponses de la personne |
|---|---|---|---|
| C2 | les **onze attributs** de `demographic_summary.csv`, et rien d'autre | oui, ligne `Political ideology` | **aucune** |
| C3 | les **environ 119 items de contexte**, question et reponse en clair | **non** | oui, toutes |

C2 et C3 ne different donc pas par la presence ou l'absence de l'etiquette : **ils echangent
integralement leur entree**. Le contraste melange deux changements, le retrait de l'etiquette
et le remplacement de la personne par onze attributs ; ses deux facteurs sont confondus et
aucun des textes du dossier ne les separe.

**Ce que le second facteur vaut a lui seul.** `B1 argmax` est une regression sur les memes
onze attributs, `B2 argmax` un plus proche voisin sur les memes 119 items **sans aucune
demographie** [CONFIRME, `a2_baselines_gss.py` lignes 178 et 188 : `enc.transform` n'alimente
que `B1`, `B2` ne voit que `codes[:, contexte]`]. A moteur statistique constant et sans
aucune ablation d'etiquette, le passage de l'un a l'autre deplace la chute sous permutation
de **0,175 a 0,357 du plancher humain**, un facteur 2,0 ; le passage de C2 a C3 vaut un
facteur 6,2 [MESURE, `a47-chute-deux-segmentations.csv`, segmentation `S_ideo`].

**L'ablation propre n'est pas dans ce dossier.** Elle est le run R3 de la nuit du 8 au
9 septembre : C3 plus etiquette contre C3, et C2 prive de la seule ligne `Political
ideology` contre C2. Tant qu'il n'a pas rendu, aucun texte ne doit ecrire « ablation de
l'etiquette » ni « seule l'etiquette bouge ».

### E2. Meme passage : le resultat cite est un non rejet sur 150 personnes, sans calcul de puissance. Objection a45 numero 8.1.

**Phrase d'origine.** « [...] l'ecart sur le milieu ordinal vaut moins 0,0067 [moins 0,0167 ;
0,0035], p ajuste par Holm 0,579, **c'est a dire rien** ».

**Correction.** L'intervalle contient zero sur 150 personnes et aucun calcul de puissance
n'accompagne le resultat. Un non rejet ne reproduit rien : il ne distingue pas « les deux
conditions sont egales » de « l'echantillon est trop petit pour trancher ». Ecrire « sur
notre contraste de conditionnement, l'ecart sur le milieu ordinal n'est pas decidable, IC
[moins 0,017 ; 0,004] sur 150 personnes ; nous ne pouvons ni confirmer ni infirmer l'egalite
de Peng », et publier la taille d'effet detectable a 80 pour cent de puissance.

---

Rapport du 8 septembre 2026. Il execute la question ouverte numero 2 de
`a36-lecture-peng-2509-19088.md` : rejouer chez nous la mesure de queue que le depot public de
Peng et al. calcule et que leur article ne publie pas. Sur leurs sorties, l'etiquette
demographique seule egale 500 reponses reelles de la personne sur les 90 pour cent du milieu,
0,7644 contre 0,7643, et perd 2,5 points sur les 5 pour cent du bas, ou le tirage aleatoire la
depasse, 0,5325 contre 0,5165. C'est, sur un autre jeu, un autre modele et une autre equipe, la
these de a29 et de a31. Ce rapport regarde si le meme profil sort de nos donnees GSS.

Zero appel de modele de langage. Lecture seule sur `data/`. Quatre coeurs. Trois scripts
nouveaux, `analyses/a39_commun.py`, `a39_tranches.py`, `a39_figure.py`. **Aucun script existant
n'a ete modifie** ; `a2_commun`, `a2_baselines_gss`, `a5_evaluer`, `a5_agents_locaux_gss`,
`a25_commun`, `a25_mesures` et `a28_commun` sont importes tels quels, memes graines, memes plis,
memes 149 items, memes personnes. La foret aleatoire `B3 foret` est relue du cache de a28, elle
n'est pas redefinie.

**Controle de protocole, execute avant toute lecture.** La colonne « ensemble » de la definition
rarete est, par construction, l'exactitude globale par cellule sur les 149 items. Elle reproduit
les valeurs publiees par a2 dans `resultats/a2_gss_resultats.json` **au sixieme chiffre pour les
neuf conditions verifiees**, ecart maximal 0,000000 : `agents composite` 0,683932,
`agents entretien (v3)` 0,656493, `agents enquete` 0,650988, `agents demographiques (v6)`
0,581787, `B0 mode` 0,593386, `B0 tirage` 0,491828, `B1 argmax` 0,620856, `B2 argmax` 0,671709,
`humains vague 2` 0,795002 [MESURE]. Le script echoue s'il en va autrement. Rien n'a bouge dans
la chaine.

Sorties : `a39-tranches.csv`, `a39-classement.csv`, `a39-contrastes.csv`,
`a39-definition-tranches.csv`, `a39-ecarts-types.csv`, `a39-ecarts-types-items.csv`,
`a39-ecarts-types-decomposition.csv`, `a39-comparaison-peng.csv`, `a39-figure-tranches.png`
et `.svg`.

---

## Reponse en une ligne

**La forme de leur resultat se reproduit, sa lettre non, et le seul endroit ou elle se reproduit
a la lettre est celui ou la comparaison est une ablation propre.** La forme : pour douze des
treize methodes, le retard sur le plancher humain est **1,2 a 4,0 fois plus grand sur les 5 pour
cent du bas que sur les 90 pour cent du milieu**, mediane 2,4 sur la definition par la rarete et
1,9 sur la definition ordinale, et le classement des methodes n'est pas le meme d'une tranche a
l'autre, correlation de rang entre la tranche basse et le
milieu **plus 0,007 sur la definition par la rarete** [MESURE, `a39-contrastes.csv`,
`a39-classement.csv`]. La lettre : chez eux l'etiquette egale la persona complete sur le milieu a
0,0001 pres ; chez nous, entre deux generations d'agents de Stanford, l'ecart est de **10,8
points sur la definition par la rarete** et de **5,1 points sur la definition ordinale**, tous
deux a p ajuste 0,004 [MESURE]. **Mais sur le seul couple ou le modele, les personnes, les
questions et les traces sont constants et ou seule l'etiquette bouge, C2 contre C3, l'ecart sur
le milieu ordinal vaut moins 0,0067 [moins 0,0167 ; 0,0035], p ajuste par Holm 0,579, c'est a
dire rien** [MESURE, `a39-contrastes.csv`, famille « replique Peng », 16 tests declares avant
execution]. Leur egalite du milieu est donc un fait d'ablation, et elle se reproduit chez nous
exactement la ou elle est une ablation.

**L'inversion de la queue se reproduit, et seulement sur la mesure categorielle.** Sur les 5 pour
cent du bas, definition par la rarete, 1 052 personnes : `agents v8`, qui ne recoit qu'une
etiquette d'ideologie, de parti, de race et de genre, est a **0,0596 [0,0472 ; 0,0718]**, le
tirage **uniforme** est a **0,1860 [0,1677 ; 0,2056]**, difference **moins 0,1263**
[moins 0,1486 ; moins 0,1040], p ajuste 0,004. Le hasard bat l'agent a etiquette de 12,6 points
sur la queue, alors qu'il est battu de 19,4 points sur le milieu [MESURE]. **Et la statistique
tombe le plus bas** : `B2 argmax` 0,0018, `B3 foret` 0,0053, `B1 argmax` 0,0222, contre 0,4994
pour les memes humains reinterroges. Sur la definition ordinale, qui est leur mesure exacte,
**l'inversion ne se produit pas** : aucune de nos conditions ne descend sous le tirage uniforme
sur la tranche basse, parce que nous n'avons pas de condition « persona vide » et que c'est la
seule des leurs qui passe sous le hasard, 0,4644 contre 0,5325.

**Et leur quatrieme mesure, le rapport d'ecarts types, ne separe pas ce qu'elle pretend
separer.** Leur echelle publiee monte de 0,446 pour la persona vide a 0,575 pour l'etiquette et
0,634 pour la persona complete, et a36 la lisait comme « la dispersion croit avec l'information ».
Chez nous, sur les 71 items ordinaux et sur la meme quantite totale, **C2 est a 0,771
[0,719 ; 0,823] et C3 a 0,781 [0,752 ; 0,807] : le meme nombre**. Leur decomposition dit deux
choses opposees : **C2 a un rapport inter segments ideologiques de 1,96 et un rapport intra de
0,50 ; C3 a 0,75 et 0,79** [MESURE, `a39-ecarts-types-decomposition.csv`, hors famille]. Le meme
retrecissement total recouvre, d'un cote, un ecart entre camps double et une variete interne
divisee par deux, et de l'autre une population simplement un peu resserree. **La mesure qu'ils
publient est aveugle a la distorsion que popsim mesure**, et le plancher humain le prouve : les
memes humains reinterroges donnent 0,999 en total, 1,033 en inter et 0,997 en intra.

---

## 0. Le protocole, ecrit avant les resultats

La famille est recopiee sans retouche de l'entete de `analyses/a39_tranches.py`, ou elle a ete
ecrite avant l'execution. La seule verification possible pour un tiers est la lecture de la
docstring.

### 0.1 Leur definition, et les cinq ecarts avec la notre

Leur code, `compute_vector_metrics.py`, lignes 220 a 263, trie les participants par leur valeur
humaine sur chaque resultat, prend les 5 pour cent du bas, les 5 pour cent du haut et les 90 pour
cent du milieu, et calcule sur chaque tranche l'exactitude individuelle `1 - MAD / etendue`
[CONFIRME, a36 section 6.3]. Nos donnees sont des reponses categorielles du GSS. Deux
transpositions sont possibles et les deux sont faites.

| | **definition par la rarete** | **definition ordinale** |
|---|---|---|
| perimetre | les 149 items | les **71** items ordinaux de a25 |
| tranche **bas** | la vraie modalite est donnee par **moins de 5 pour cent** des repondants observes de l'item | les repondants sont tries par leur vraie valeur, les **5 pour cent du bas** par rang |
| tranche **haut** | la vraie modalite est la modalite majoritaire **et** cette modalite depasse **95 pour cent** | les **5 pour cent du haut** par rang |
| tranche **milieu** | le reste | le reste |
| exactitude | concordance exacte, seule mesure definie sur une reponse nominale | **la leur**, `1 - ecart absolu / etendue`, les modalites recevant leur rang normalise dans [0, 1] |

**Ecart 1, et il est le plus important : la tranche haute n'existe presque pas sur le GSS.**
Sur les 1 052 personnes, **6 items sur 149** portent une modalite majoritaire au dela de 95 pour
cent, 7 sur les 150 personnes. La tranche haute de la definition par la rarete pese 6 219
cellules sur 156 748, soit **3,97 pour cent**, et la tranche basse 1 710 cellules, soit **1,09
pour cent** [MESURE, `a39-definition-tranches.csv`]. Leurs tranches font 5 et 5 pour cent par
construction ; les notres non, parce que la rarete d'une modalite n'est pas un rang. **Il ne faut
donc pas lire nos trois tranches comme des quantiles, et la comparaison chiffre a chiffre avec
leurs valeurs est illegitime en niveau.** Elle ne l'est pas en forme, et c'est la forme que ce
rapport lit.

**Ecart 2 : les egalites.** Sur la definition ordinale, la tranche fait bien 5 pour cent par
construction, 3 763 cellules sur 74 692 sur les 1 052 personnes. Mais une echelle a trois
modalites produit des egalites massives : les 5 pour cent du bas sont presque toujours un sous
ensemble arbitraire des personnes qui ont donne la valeur minimale. Les egalites sont departagees
par une **permutation aleatoire de graine fixe, 20260908**. C'est le seul point ou notre
definition ajoute une convention a la leur. Leur code, sur des reponses continues ou sur des
echelles longues, ne rencontre pas ce probleme au meme degre. **Une variante sans convention est
rapportee en robustesse**, « ordinale extremes », qui remplace le tri par rang par
l'appartenance au bout de l'echelle : bas = la personne a donne la modalite la plus basse, haut =
la plus haute. Elle donne des tranches de 28,5 et 21,5 pour cent et ne change aucune conclusion.

**Ecart 3 : leur temoin n'est pas le notre, et il a fallu en construire un.** Leur
`random_benchmark` est un tirage **uniforme sur l'etendue du resultat**. Notre `B0 tirage` est un
tirage dans la **marginale observee** de l'item : il connait la distribution de la population et
se concentre donc sur la modalite majoritaire. Sur les 5 pour cent du bas, la difference est
decisive. Ce rapport ajoute donc **`B0 uniforme`**, qui tire uniformement parmi les modalites
declarees de l'item dans `question_master/gss/main.csv`, defini dans `a39_commun.py`, et le
declare comme quatorzieme methode non humaine. **Signale honnetement : ce temoin a ete ajoute
apres un premier passage a 300 tirages qui a montre que `B0 tirage` n'etait pas leur temoin.
La structure des familles n'a pas change, seul le nombre de methodes est passe de 13 a 14.**

**Ecart 4 : l'ordre des modalites est herite et non verifie.** Le rang normalise d'une modalite
suit l'ordre de `question_master/gss/main.csv`, le meme que celui employe par a1, a25 et a28 pour
la distance de Wasserstein. Si cet ordre n'etait pas l'ordre de l'echelle pour un item, la mesure
ordinale serait fausse pour cet item. Je n'ai pas relu les 71 nomenclatures.

**Ecart 5 : le compte d'items ordinaux.** La commande annonce 70 items ordinaux, le filtre de a25
en donne **71** : un item figure dans `ORDINAUX` et ne porte aucune modalite du type
« Inapplicable ». Le chiffre employe partout ici est 71.

**Convention sur les refus, reprise de a29 sans changement.** Une cellule est evaluable des que
la vraie reponse de la vague 1 est observee ; une prediction absente compte comme fausse et reste
au denominateur, ce qui est la convention la plus severe. Le taux de refus est au plus **0,20
pour cent**, atteint par `agents demographiques (v6)`, et il est nul pour C2, C3 et les cinq
temoins [MESURE, `a39-tranches.csv`].

### 0.2 Les quatre familles declarees

| | enonce | nombre de tests |
|---|---|---|
| **primaire** | pour chacune des 13 methodes non humaines autres que le temoin, pour chacune des deux definitions et pour les tranches bas et milieu : l'exactitude differe de celle de `B0 uniforme` sur la meme tranche | **52** |
| **secondaire** | les memes contrastes, contre `humains vague 2` | **56** |
| **replique Peng** | (a) etiquette contre riche sur le milieu, (b) etiquette contre riche sur le bas, (c) etiquette contre uniforme sur le bas, (d) riche contre uniforme sur le bas ; couple `agents v8` contre `agents composite` sur les 1 052, couple `C2` contre `C3` sur les 150 ; deux definitions | **16** |
| **dispersion** | pour chacune des 14 methodes, le rapport d'ecarts types moyen sur les items ordinaux differe de celui de `humains vague 2` | **14** |

Les quatre familles sont corrigees **separement** par **Holm**, valide sans hypothese sur la
dependance, ce qui est necessaire puisque les contrastes portent sur les memes personnes et les
memes items. **Benjamini Hochberg** est rapporte a cote dans le CSV. Tous les p sont des p de
**bootstrap apparie sur les personnes, 4 000 tirages**, lus sur la position de zero dans la
distribution ; ils ne descendent jamais sous 1 / 4 000 = 0,00025, donc le plancher de Holm vaut
0,013 sur la famille primaire, 0,014 sur la secondaire, 0,004 sur la replique et 0,0035 sur la
dispersion.

**Prediction ecrite avant execution**, telle que la commande la formule : sur le milieu,
l'etiquette seule egale les conditions riches et les baselines ; sur le bas, l'etiquette seule
tombe sous le tirage aleatoire, les conditions riches restent au dessus, et la statistique tombe
le plus bas.

**N'entrent dans aucune famille**, et sont des descriptions : la tranche haute ; la variante
« ordinale extremes » ; le perimetre 150 pour les onze methodes qui disposent du 1 052,
echantillon emboite ; le classement par tranche et les correlations de rang entre tranches ; le
detail par item ; la comparaison chiffre a chiffre avec leurs valeurs publiees ; et **la
decomposition du rapport d'ecarts types en un terme inter et un terme intra**, qui porte des
intervalles bootstrap sur 1 000 tirages et aucun test.

---

## 1. L'exactitude par tranche

### 1.1 Definition par la rarete, 149 items, 1 052 personnes

[MESURE, `a39-tranches.csv`, IC bootstrap sur les personnes, 4 000 tirages]

| condition | 5 % du bas | 90 % du milieu | 5 % du haut | ensemble |
|---|---|---|---|---|
| ***humains vague 2*** | ***0,4994 [0,472 ; 0,526]*** | ***0,7905 [0,785 ; 0,796]*** | ***0,9847*** | ***0,7950*** |
| agents demographiques (v6) | **0,2316 [0,210 ; 0,253]** | 0,5686 [0,564 ; 0,573] | 0,9939 | 0,5818 |
| agents composite | 0,2199 [0,198 ; 0,242] | **0,6769 [0,673 ; 0,681]** | 0,9797 | 0,6839 |
| agents entretien (v3) | 0,2193 [0,198 ; 0,241] | 0,6488 | 0,9598 | 0,6565 |
| **B0 uniforme** | **0,1860 [0,168 ; 0,206]** | **0,3535 [0,351 ; 0,356]** | **0,3936** | **0,3532** |
| agents enquete | 0,1111 [0,094 ; 0,130] | 0,6479 | 0,8741 | 0,6510 |
| agents v8 | 0,0596 [0,047 ; 0,072] | 0,5470 | 0,9875 | 0,5591 |
| agents v7 | 0,0456 [0,036 ; 0,056] | 0,5543 | 0,9397 | 0,5640 |
| B0 tirage | 0,0322 [0,024 ; 0,040] | 0,4764 | 0,9879 | 0,4918 |
| **B1 argmax** | 0,0222 [0,016 ; 0,029] | 0,6119 | 0,9998 | 0,6209 |
| **B3 foret** | **0,0053 [0,002 ; 0,009]** | 0,6259 | 1,0000 | 0,6340 |
| **B2 argmax** | **0,0018 [0,000 ; 0,004]** | **0,6657** | 1,0000 | 0,6717 |
| B0 mode | 0,0000 | 0,5832 | 1,0000 | 0,5934 |

Sur les 150 personnes du run local, memes references restreintes : `C3` 0,1844 [0,137 ; 0,235] de
bas et 0,5669 de milieu, `C2` 0,1393 [0,092 ; 0,191] et 0,5136, `B0 uniforme` 0,2213
[0,170 ; 0,271] et 0,3517, `humains vague 2` 0,4057 et 0,7867 [MESURE].

**Cinq lectures.**

1. **Le tirage uniforme est cinquieme sur treize sur la queue et dernier sur le milieu**
   [MESURE]. Il est battu de 32,3 points par `agents composite` et de 19,4 points par
   `agents v8` sur le milieu, et il bat **huit des douze autres methodes** sur la queue.
   **C'est exactement le profil de leur tableau**, ou le `random_benchmark` est battu de plus de
   12 points sur le milieu et depasse l'etiquette seule sur les 5 pour cent du bas.
2. **La statistique tombe le plus bas, et de tres loin** [MESURE]. `B2 argmax` retrouve 0,18 pour
   cent des cellules rares, la foret 0,53 pour cent, la regression logistique 2,2 pour cent, la
   modalite majoritaire 0. Sur le milieu, les memes methodes sont deuxieme, sixieme et septieme.
   **C'est le meme fait que a29 section 1, vu par la tranche au lieu du rappel.**
3. **La prediction « l'etiquette seule tombe sous le tirage aleatoire » est vraie pour `agents
   v8` et fausse pour `agents demographiques (v6)`** [MESURE]. v8 est a moins 0,1263 du tirage
   uniforme, p ajuste 0,013 dans la famille primaire ; v6 est a **plus 0,0456**
   [0,0146 ; 0,0760], p ajuste **0,033**, et c'est **la seule methode du perimetre 1 052 qui
   depasse significativement le tirage uniforme sur la queue**. La difference entre les deux est
   exactement celle que a19 a etablie : v6 n'a recu ni ideologie ni parti, v8 les a recus. **Ce
   n'est donc pas l'etiquette demographique en general qui fait tomber la queue, c'est
   l'etiquette ideologique.** C'est le resultat le moins attendu de ce rapport et il renforce
   la ligne de FAITS-ETABLIS sur l'axe qui porte l'effet.
4. **La prediction « les conditions riches restent au dessus » ne tient qu'a moitie** [MESURE].
   `agents composite` est a plus 0,0339 [0,0044 ; 0,0628] et `agents entretien (v3)` a plus
   0,0333, **aucun des deux ne passant Holm sur la famille primaire**, p ajuste 0,120. Et
   `agents enquete`, qui est une condition riche, est a **moins 0,0749**
   [moins 0,1021 ; moins 0,0478], p ajuste 0,013, **c'est a dire significativement sous le
   hasard**. Il faut le dire ainsi : sur les reponses que moins d'une personne sur vingt donne,
   la meilleure population simulee du corpus ne fait pas mieux qu'un des a jouer.
5. **Sur la tranche haute, quatre methodes battent le plancher humain** [MESURE, descriptif].
   `B0 mode`, `B2 argmax`, `B3 foret` et `B1 argmax` sont a 1,0000, 1,0000, 1,0000 et 0,9998,
   les humains reinterroges a 0,9847. Sur une tranche ou 95 pour cent des gens donnent la meme
   reponse, predire toujours la majorite est parfait et la vraie personne, elle, change parfois
   d'avis. **La tranche haute du GSS mesure la degenerescence de la question, pas la qualite de
   la methode.** C'est la raison pour laquelle elle est hors famille.

### 1.2 Definition ordinale, leur mesure, 71 items, 1 052 personnes

[MESURE, `a39-tranches.csv`]

| condition | 5 % du bas | 90 % du milieu | 5 % du haut | ensemble |
|---|---|---|---|---|
| ***humains vague 2*** | ***0,8356 [0,824 ; 0,847]*** | ***0,8734 [0,870 ; 0,877]*** | ***0,8270*** | ***0,8692*** |
| agents enquete | **0,6940 [0,683 ; 0,706]** | 0,7764 | 0,6761 | 0,7672 |
| agents composite | 0,6777 [0,666 ; 0,690] | **0,8001 [0,797 ; 0,803]** | 0,7443 | 0,7911 |
| B2 argmax | 0,6603 [0,649 ; 0,671] | **0,8078 [0,805 ; 0,810]** | 0,6039 | 0,7901 |
| agents entretien (v3) | 0,6598 | 0,7778 | 0,7473 | 0,7703 |
| B1 argmax | 0,6378 | 0,7760 | 0,5773 | 0,7591 |
| B3 foret | 0,6234 | 0,7906 | 0,5557 | 0,7703 |
| agents v7 | 0,6089 | 0,7380 | 0,5073 | 0,7198 |
| agents v8 | 0,6007 [0,587 ; 0,614] | 0,7246 | 0,6443 | 0,7143 |
| agents demographiques (v6) | 0,5874 | 0,7490 | 0,5309 | 0,7298 |
| B0 mode | 0,5674 | 0,7742 | 0,4653 | 0,7482 |
| B0 tirage | 0,5419 | 0,6872 | 0,4816 | 0,6695 |
| **B0 uniforme** | **0,5009 [0,488 ; 0,513]** | **0,5928** | **0,5163** | **0,5843** |

Sur les 150 personnes : `C3` 0,6197 [0,589 ; 0,650] de bas et 0,7291 de milieu, `C2` 0,5773
[0,549 ; 0,606] et 0,7224, `humains vague 2` 0,8163 et 0,8737 [MESURE].

**Trois lectures.**

1. **Sur leur propre mesure, l'inversion ne se produit pas chez nous** [MESURE]. `B0 uniforme`
   est **dernier des treize sur les trois tranches**. Les douze contrastes de la famille primaire
   sur cette definition sont tous positifs et tous passent Holm. La raison est structurelle :
   sur une echelle a trois ou cinq modalites, un tirage uniforme centre le predicteur au milieu
   de l'echelle, donc son `1 - MAD` sur une reponse extreme vaut environ 0,50, et il faut etre
   **systematiquement au mauvais bout** pour descendre plus bas. C'est ce que fait leur
   `empty_persona`, a 0,4644 contre 0,5325 pour leur hasard. **Nous n'avons pas de condition
   persona vide**, et c'est la piece manquante de la replication.
2. **Le retard sur le plancher humain double dans la queue** [MESURE, `a39-contrastes.csv`,
   famille secondaire, les 56 contrastes passent Holm a p ajuste 0,014]. Sur les 1 052 personnes,
   le rapport entre le retard sur la tranche basse et le retard sur le milieu vaut, pour les
   douze methodes, **de 1,19 a 2,70 sur la definition ordinale, mediane 1,92**, et **de 0,72 a
   3,99 sur la definition par la rarete, mediane 2,41** : `agents composite` moins 0,158 contre
   moins 0,073, rapport 2,15 ; `B2 argmax` moins 0,175 contre moins 0,066, rapport 2,67 ;
   `agents v8` moins 0,235 contre moins 0,149, rapport 1,58. **Le tirage uniforme est le plus bas
   des douze sur les deux definitions, 1,19 et 0,72, et le seul a descendre sous 1** : le hasard
   est le seul predicteur dont le defaut ne se concentre pas dans les queues, ce qui est la
   definition meme d'un temoin. Sur les 150 personnes, C2 et C3 ne doublent pas sur la definition
   par la rarete, rapports 0,98 et 1,01, et doublent a demi sur l'ordinale, 1,58 et 1,36 : la
   puissance de 150 personnes sur une tranche de 568 cellules est faible et il faut le dire.
3. **`agents enquete` est premier sur la queue et sixieme sur le milieu ; `B2 argmax` est
   troisieme sur la queue et deuxieme sur le milieu** [MESURE]. Le classement bouge, mais moins
   que sur la definition par la rarete, voir la section suivante.

### 1.3 Le classement n'est pas le meme d'une tranche a l'autre

[MESURE, `a39-classement.csv`, correlation de rang de Spearman entre les exactitudes des treize
methodes non humaines, hors famille]

| definition et perimetre | rho(bas, milieu) | rho(bas, haut) | rho(milieu, haut) |
|---|---|---|---|
| **rarete, 1 052** | **plus 0,007** | moins 0,662 | plus 0,239 |
| rarete, 150 | moins 0,225 | moins 0,595 | plus 0,479 |
| ordinale, 1 052 | plus 0,832 | plus 0,797 | plus 0,594 |
| ordinale, 150 | plus 0,701 | plus 0,864 | plus 0,415 |

**Sur la definition par la rarete, savoir quelle methode gagne au milieu ne dit rien sur celle qui
gagne dans la queue, rho plus 0,007 sur les 1 052 personnes.** L'ordre du milieu est
`agents composite`, `B2 argmax`, `agents entretien` ; l'ordre de la queue est
`agents demographiques (v6)`, `agents composite`, `agents entretien`, puis le tirage uniforme, et
`B2 argmax` est **dernier des douze evaluables**. C'est la version chiffree du reproche que a29
adresse a l'exactitude globale : **un score moyen ne dit rien de la queue, et c'est precisement
ce que la mesure de Peng et al. rend visible et que leur article ne publie pas.**

Sur la definition ordinale, le classement est stable, rho plus 0,83. Les deux definitions ne
mesurent donc pas la meme chose, et il faut le dire : **la concordance exacte punit l'abstention,
la distance ordinale ne la punit pas.** Une methode qui repond toujours « about right » perd tout
sur la queue categorielle et perd peu sur la queue ordinale.

### 1.4 La robustesse « extremes de l'echelle »

[MESURE, `a39-tranches.csv`, definition « ordinale extremes », hors famille]

La variante qui supprime la convention d'egalite, en definissant la tranche basse comme
« la personne a donne la modalite la plus basse de l'item », donne des tranches de 28,5 pour cent
et 21,5 pour cent au lieu de 5 et 5. **Le classement et le sens ne changent pas** :
`B0 uniforme` reste dernier partout, 0,4984 sur le bas ; le retard au plancher humain reste plus
grand sur les extremes que sur le milieu pour toutes les conditions a modele de langage ; et
l'ablation garde son signe, `C3` 0,6978 contre `C2` 0,6157 sur la tranche basse. La convention
d'egalite ne porte donc aucune conclusion.

---

## 2. Les quatre lignes de leur tableau, une par une

[MESURE, `a39-contrastes.csv`, famille « replique Peng », 16 tests declares, Holm]

| definition | contraste | couple | difference | IC 95 % | p Holm |
|---|---|---|---|---|---|
| rarete | a. etiquette contre riche, **milieu** | v8 moins composite | **moins 0,1299** | [moins 0,134 ; moins 0,125] | **0,004** |
| ordinale | a. etiquette contre riche, **milieu** | v8 moins composite | **moins 0,0755** | [moins 0,079 ; moins 0,072] | **0,004** |
| rarete | a. etiquette contre riche, **milieu** | **C2 moins C3** | moins 0,0533 | [moins 0,064 ; moins 0,042] | **0,004** |
| **ordinale** | **a. etiquette contre riche, milieu** | **C2 moins C3** | **moins 0,0067** | **[moins 0,0167 ; 0,0035]** | **0,579** |
| rarete | b. etiquette contre riche, **bas** | v8 moins composite | moins 0,1602 | [moins 0,183 ; moins 0,138] | **0,004** |
| ordinale | b. etiquette contre riche, **bas** | v8 moins composite | moins 0,0770 | [moins 0,090 ; moins 0,065] | **0,004** |
| rarete | b. etiquette contre riche, **bas** | C2 moins C3 | moins 0,0451 | [moins 0,115 ; 0,024] | 0,579 |
| ordinale | b. etiquette contre riche, **bas** | C2 moins C3 | moins 0,0424 | [moins 0,081 ; moins 0,005] | 0,177 |
| **rarete** | **c. etiquette contre uniforme, bas** | **v8 moins B0 uniforme** | **moins 0,1263** | **[moins 0,149 ; moins 0,104]** | **0,004** |
| ordinale | c. etiquette contre uniforme, **bas** | v8 moins B0 uniforme | plus 0,0998 | [0,082 ; 0,117] | **0,004** |
| rarete | c. etiquette contre uniforme, **bas** | C2 moins B0 uniforme | moins 0,0820 | [moins 0,147 ; moins 0,015] | 0,112 |
| ordinale | c. etiquette contre uniforme, **bas** | C2 moins B0 uniforme | plus 0,0436 | [moins 0,002 ; 0,088] | 0,256 |
| rarete | d. riche contre uniforme, **bas** | composite moins B0 uniforme | plus 0,0339 | [0,004 ; 0,063] | 0,177 |
| ordinale | d. riche contre uniforme, **bas** | composite moins B0 uniforme | plus 0,1768 | [0,160 ; 0,194] | **0,004** |
| rarete | d. riche contre uniforme, **bas** | C3 moins B0 uniforme | moins 0,0369 | [moins 0,104 ; 0,027] | 0,579 |
| ordinale | d. riche contre uniforme, **bas** | C3 moins B0 uniforme | plus 0,0860 | [0,041 ; 0,129] | **0,004** |

**Ligne a, l'egalite du milieu : elle se reproduit exactement la ou la comparaison est une
ablation, et nulle part ailleurs** [MESURE]. Entre `agents v8` et `agents composite`, deux
generations d'agents differentes, deux invites differentes, deux tailles de contexte differentes,
l'ecart est de 13,0 et 7,6 points selon la definition. Entre `C2` et `C3`, **meme modele, memes
150 personnes, memes 149 questions, memes traces, seule l'etiquette bouge**, l'ecart sur le milieu
ordinal vaut moins 0,0067 et l'intervalle contient zero. **Leur 0,7644 contre 0,7643 n'est donc
pas un fait sur les etiquettes en general : c'est un fait sur une comparaison a modele et a
personnes constants**, et sur la seule comparaison de ce type que nous ayons, il se reproduit.
[PROBABLE] plutot que [CONFIRME] : un seul modele, un seul run, 150 personnes, et l'ecart de
5,3 points sur la meme paire dans la definition par la rarete montre que la mesure d'exactitude
choisie change le verdict.

**Ligne c, le hasard qui bat l'etiquette dans la queue : elle se reproduit sur la definition
categorielle et pas sur la leur** [MESURE]. Moins 12,6 points pour v8, p ajuste 0,004. Sur les
150 personnes, C2 est a moins 8,2 points du tirage uniforme, l'intervalle exclut zero mais la
correction ne passe pas, p ajuste 0,112. **Le signe est le bon dans les deux perimetres, la
puissance manque sur 150 personnes.**

**Ligne d, la condition riche qui reste au dessus du hasard dans la queue : vraie sur la
definition ordinale, indecidable sur la rarete** [MESURE]. Plus 17,7 points pour `agents
composite` et plus 8,6 points pour `C3` sur l'ordinale, p ajuste 0,004 ; plus 3,4 points et
moins 3,7 points sur la rarete, aucun des deux ne passant. **Sur les cellules ou moins d'une
personne sur vingt donne la reponse, aucune de nos conditions riches n'est demontrablement
meilleure qu'un des.**

---

## 3. Leur rapport d'ecarts types, et ce qu'il confond

### 3.1 Nos valeurs, et pourquoi elles ne se comparent pas aux leurs en niveau

[MESURE, `a39-ecarts-types.csv`, 71 items ordinaux, echantillon apparie, ecart type sans biais,
IC bootstrap sur les personnes]

| condition | rapport moyen | IC 95 % | mediane par item | items sous 1 sur 71 |
|---|---|---|---|---|
| **B0 uniforme** | **1,268** | [1,256 ; 1,282] | 1,220 | 6 |
| B0 tirage | 1,000 | [0,991 ; 1,011] | 1,000 | 35 |
| ***humains vague 2*** | ***0,999*** | ***[0,994 ; 1,005]*** | ***1,001*** | ***35*** |
| agents entretien (v3) | 0,946 | [0,937 ; 0,956] | 0,935 | 42 |
| agents composite | 0,924 | [0,916 ; 0,932] | 0,920 | 46 |
| **agents v8** | **0,914** | [0,899 ; 0,929] | 0,954 | 38 |
| agents enquete | 0,907 | [0,899 ; 0,916] | 0,890 | 46 |
| B1 argmax | 0,807 | [0,797 ; 0,817] | 0,830 | 66 |
| **C3** | **0,781** | [0,752 ; 0,807] | 0,770 | 57 |
| **C2** | **0,771** | [0,719 ; 0,823] | 0,779 | 56 |
| agents v7 | 0,689 | [0,672 ; 0,706] | 0,643 | 68 |
| B2 argmax | 0,685 | [0,677 ; 0,693] | 0,731 | 70 |
| agents demographiques (v6) | 0,654 | [0,645 ; 0,663] | 0,661 | 65 |
| B3 foret | 0,598 | [0,588 ; 0,606] | 0,654 | 69 |
| B0 mode | 0,042 | [0,041 ; 0,043] | 0,000 | 71 |

**Trois faits, et le premier est un cadeau.**

1. **Notre plancher de bruit sur cette mesure vaut 1,000** [MESURE]. Les memes humains
   reinterroges deux semaines plus tard donnent 0,9994 [0,9937 ; 1,0053], le seul des quatorze
   contrastes de la famille dispersion qui ne passe pas Holm etant `B0 tirage`, a plus 0,0011,
   p 0,817. **Peng et al. n'ont aucun equivalent** : ils ne peuvent pas dire de combien un
   rapport de 0,634 s'ecarte de ce qu'un humain donnerait a lui meme. Nous pouvons.
   C'est le differentiateur numero un de FAITS-ETABLIS, ici transporte sur leur mesure a eux.
2. **Le tirage uniforme est au dessus de 1, a 1,268, exactement comme leur `random_benchmark` a
   1,139** [MESURE]. Un predicteur aveugle ne retrecit rien, il elargit. La mesure est donc valide
   au meme titre que la leur, et la phrase « les modeles de langage ecrasent la variance » reste
   fausse en general.
3. **Nos niveaux sont beaucoup plus hauts que les leurs et ne sont pas comparables en valeur**
   [MESURE]. Leur echelle va de 0,377 a 0,734 pour les conditions d'invite ; la notre va de 0,654
   a 0,946 pour les conditions a modele de langage. Trois raisons : le jeu, le GSS contre
   Twin-2K-500 ; le codage, un rang normalise sur 3 a 12 modalites contre leurs echelles ; et le
   perimetre, 71 items ordinaux contre 163 resultats. **Ne jamais poser nos chiffres a cote des
   leurs dans la meme colonne sans cette phrase.**

### 3.2 La decomposition, et ce que leur echelle ne peut pas voir

[MESURE, `a39-ecarts-types-decomposition.csv`, axe ideologie a sept niveaux, decomposition
exacte de la variance, IC bootstrap sur 1 000 tirages de personnes, **hors famille, descriptif**]

| condition | rapport **total** | rapport **inter** segments | rapport **intra** segment |
|---|---|---|---|
| ***humains vague 2, 1 052*** | ***0,999*** | ***1,033*** | ***0,997*** |
| agents entretien (v3) | 0,946 | 1,629 | 0,839 |
| agents composite | 0,924 | 1,530 | 0,851 |
| **agents v8** | **0,914** | **3,033** | **0,525** |
| agents enquete | 0,907 | 1,666 | 0,812 |
| B1 argmax | 0,807 | 1,451 | 0,731 |
| **C3, sans etiquette** | **0,781** | **0,746** | **0,787** |
| **C2, avec etiquette** | **0,771** | **1,960** | **0,503** |
| agents v7 | 0,689 | 0,510 | 0,712 |
| B2 argmax | 0,685 | 1,093 | 0,643 |
| agents demographiques (v6) | 0,654 | 0,466 | 0,675 |
| B3 foret | 0,598 | 1,183 | 0,510 |
| B0 uniforme | 1,268 | 0,546 | 1,322 |
| B0 tirage | 1,000 | 0,424 | 1,047 |
| B0 mode | 0,042 | 0,010 | 0,046 |

**C'est le tableau du rapport, et il vise leur mesure et pas la notre.**

1. **C2 et C3 ont le meme rapport total, 0,771 et 0,781, et deux decompositions opposees**
   [MESURE]. C2 gonfle l'ecart entre camps d'un facteur 1,96 et divise la variete interne par
   deux, 0,503 ; C3 resserre legerement les deux, 0,746 et 0,787. **Meme modele, memes personnes,
   memes questions, memes traces, seule l'etiquette bouge.** Un lecteur qui ne dispose que du
   rapport total conclut que les deux conditions se valent. **Elles ne se valent pas, elles font
   deux erreurs contraires.**
2. **`agents v8` est le cas extreme et il est instructif** [MESURE]. Son rapport total, 0,914,
   est le troisieme meilleur des conditions a modele de langage et il n'est qu'a 8,5 points du
   plancher humain. Sa decomposition dit 3,033 entre camps et 0,525 a l'interieur. **Sur la
   mesure que Peng et al. publient, l'agent le plus stereotype du corpus passe pour l'un des
   moins retrecis.** C'est, chiffres a l'appui, la limite de leur distorsion 1.
3. **Leur echelle « vide 0,446, etiquette 0,575, persona complete 0,634 » ne se reproduit pas
   en ordre chez nous** [MESURE]. Nos conditions a etiquette occupent les deux extremes de la
   colonne totale, v8 a 0,914 et v6 a 0,654, et nos conditions riches occupent le haut. **La
   lecture « la dispersion croit avec l'information individuelle » est donc [PROBABLE] chez eux
   et fausse chez nous en niveau total**, parce que le signe du terme inter depend de ce que
   contient l'etiquette. v6, qui n'a recu ni ideologie ni parti, a un rapport inter de 0,466 ;
   v8, qui les a recus, de 3,033. **Le meme type de condition, a une etiquette pres, se place
   aux deux bouts.**
4. **Le plancher humain vaut 1,03 en inter et 1,00 en intra** [MESURE]. Toute lecture d'un
   rapport inter superieur a 1 comme un gonflement, et d'un rapport intra inferieur a 1 comme un
   ecrasement, est donc calibree et non postulee.

Precision necessaire : ce terme inter est calcule sur la valeur numerique de la reponse, pas sur
l'indice de Gini Simpson de a1. **Les deux quantites ne sont pas la meme** et les chiffres de ce
tableau ne remplacent pas ceux de FAITS-ETABLIS section 1 ; ils disent la meme chose sur une
autre echelle, ce qui est une corroboration interne et non un doublon.

---

## 4. La figure

`a39-figure-tranches.png` et `.svg`, quatre panneaux, produits par `a39_figure.py` qui ne
recalcule rien et lit les tableaux.

- **Panneau 1**, exactitude par tranche sur la definition par la rarete, 1 052 personnes, une
  courbe par methode, bande d'intervalle bootstrap. On voit d'un coup la remontee monotone vers
  la droite pour toutes les methodes sauf le tirage uniforme, qui est presque plat.
- **Panneau 2**, la meme chose sur la definition ordinale, avec **leurs quatre specifications
  publiees tracees en gris et en tirets**. Leur profil et le notre ont la meme forme en accent
  circonflexe, milieu haut et deux queues basses, et leurs niveaux tombent au milieu des notres.
- **Panneau 3**, definition ordinale sur les 150 personnes, avec l'ablation C2 contre C3.
- **Panneau 4**, le rapport inter en abscisse, en echelle logarithmique, contre le rapport intra
  en ordonnee, un point par methode, C2 et C3 cernes de noir, le point de fidelite parfaite en
  (1 ; 1). C'est le panneau qui montre que leur rapport total confond deux positions opposees.

---

## 5. Ce que ce resultat autorise a ecrire, et ce qu'il interdit

### Autorise

1. « Sur nos donnees comme sur les leurs, la valeur d'une population simulee est concentree au
   milieu de la distribution : le retard sur ce que les memes humains donnent d'une vague a
   l'autre est de 1,2 a 4,0 fois plus grand sur les 5 pour cent du bas que sur les 90 pour cent
   du milieu, mediane 2,4 sur douze methodes, et le seul predicteur dont le defaut ne se
   concentre pas dans la queue est un tirage au hasard. » [MESURE]
2. « Sur les reponses que moins d'une personne sur vingt donne, un tirage uniforme bat un agent
   a etiquette ideologique de 12,6 points, alors qu'il est battu de 19,4 points sur le reste de
   la distribution. C'est le meme renversement que les sorties publiees de Peng et al., sur un
   autre jeu, un autre modele et une autre equipe. » [MESURE]
3. « Sur ces memes cellules, une regression logistique retrouve 2,2 pour cent des reponses, une
   foret aleatoire 0,5 pour cent, les trente plus proches voisins 0,2 pour cent, et les memes
   humains reinterroges 49,9 pour cent. » [MESURE]
4. « Savoir quelle methode gagne au milieu ne dit rien de celle qui gagne dans la queue :
   la correlation de rang entre les deux classements vaut plus 0,007. » [MESURE]
5. « A modele, personnes, questions et traces constants, retirer l'etiquette demographique ne
   change rien a l'exactitude sur les 90 pour cent du milieu, moins 0,007 [moins 0,017 ; 0,004],
   et change tout a la structure de la dispersion : le rapport d'ecarts types entre camps passe
   de 1,96 a 0,75 et le rapport a l'interieur des camps de 0,50 a 0,79, pour un rapport total
   identique, 0,77 contre 0,78. » [MESURE]
6. « La mesure de retrecissement que publie le seul travail comparable au notre est un rapport
   total. Sur nos donnees, deux conditions qui ne different que par la presence d'une etiquette
   donnent le meme rapport total et deux decompositions opposees. La mesure est aveugle a la
   distorsion. » [MESURE]
7. « Notre plancher de bruit sur cette mesure vaut 0,999 en total, 1,033 entre groupes et 0,997
   a l'interieur des groupes : les memes humains reinterroges ne retrecissent rien. » [MESURE]
8. « Ce n'est pas l'etiquette demographique en general qui fait tomber la queue, c'est
   l'etiquette ideologique : l'agent demographique sans ideologie ni parti est la seule methode
   qui depasse significativement le tirage uniforme sur les 5 pour cent du bas, plus 0,046, et
   le meme agent avec ideologie et parti est 12,6 points en dessous. » [MESURE]

### Interdit

1. **Interdit d'ecrire que nos chiffres de tranche reproduisent les leurs en valeur.** [MESURE]
   Nos tranches ne sont pas des quantiles : la tranche basse pese 1,09 pour cent des cellules et
   la haute 3,97 pour cent, contre 5 et 5 chez eux, et notre exactitude categorielle n'est pas
   leur `1 - MAD / etendue`. La comparaison porte sur la forme et sur le signe, jamais sur le
   niveau.
2. **Interdit d'ecrire que l'etiquette seule egale la persona complete sur le milieu.** [MESURE]
   C'est vrai chez eux, c'est vrai chez nous sur la seule ablation propre dont nous disposons,
   et c'est **faux** entre deux generations d'agents de Stanford, ou l'ecart vaut 13,0 points sur
   la rarete et 7,6 points sur l'ordinale, p ajuste 0,004.
3. **Interdit de dire que nous reproduisons leur inversion « le hasard bat l'etiquette dans la
   queue » sur leur mesure.** [MESURE] Nous la reproduisons sur la concordance exacte. Sur leur
   distance ordinale, aucune de nos conditions ne descend sous le tirage uniforme, et la
   condition qui le fait chez eux, la persona vide, **n'existe pas dans notre dispositif**.
4. **Interdit d'ecrire que les conditions riches restent au dessus du hasard sur la queue.**
   [MESURE] Sur la definition par la rarete, `agents composite` est a plus 0,034 sans passer la
   correction, et `agents enquete`, qui est riche, est significativement **sous** le hasard, moins
   0,075, p ajuste 0,013.
5. **Interdit de citer la tranche haute du GSS comme une mesure de qualite.** [MESURE] Elle ne
   porte que 6 items sur 149, et quatre methodes y battent le plancher humain en repondant
   toujours la majorite.
6. **Interdit d'employer nos rapports d'ecarts types a la place de ceux de a1.** [MESURE] Ceux ci
   portent sur la valeur numerique de la reponse sur 71 items ordinaux, ceux la sur l'indice de
   Gini Simpson et sur l'entropie de 149 items. Les deux se corroborent, ils ne se substituent
   pas.
7. **Interdit d'employer la comparaison C2 contre C3 pour conclure sur les modeles en general.**
   Un modele ouvert de 4 milliards de parametres, un seul run, 150 personnes, et la limite
   ouverte de a23 sur la formulation des invites reste entiere. C'est la meme restriction qu'en
   a29 et a31, mot pour mot.

---

## 6. Ce que cela change a `ARBITRAGE.md`

**L'option A gagne sa corroboration externe et perd une de ses deux formulations.**

1. **La corroboration.** La phrase « toute methode qui predit des reponses efface les gens rares »
   a maintenant un equivalent chez la seule equipe qui a mesure la meme chose, sur un autre jeu,
   un autre modele et une autre mesure d'exactitude, avec le meme signe et la meme forme.
   La phrase se poste desormais en deux lignes et avec une reference : **le retard sur le plancher
   humain double dans la queue, le hasard bat l'agent a etiquette sur la queue et se fait ecraser
   au milieu, et la statistique disparait presque completement de la queue.** C'est ce que la
   question ouverte numero 2 de a36 demandait de verifier ; c'est verifie.

2. **Ce qui doit sortir du texte.** « Les conditions riches restent au dessus » ne tient pas sur
   la definition categorielle : deux des trois conditions riches ne passent pas la correction
   contre un tirage uniforme sur les 5 pour cent du bas, et la troisieme est significativement
   en dessous. **La phrase doit devenir « les conditions riches sont les seules a ne pas tomber
   sous le hasard, et elles ne le depassent pas de facon demontrable ».**

3. **Ce qui gagne un argument nouveau, et c'est le plus important.** Le paragraphe de methode de
   l'option B disposait de la decomposition inter et intra comme d'un raffinement. Il en dispose
   maintenant comme d'une **refutation de la mesure standard** : sur la quantite exacte que le
   depot de Peng et al. publie par resultat, deux conditions qui ne different que par une
   etiquette donnent 0,771 et 0,781, c'est a dire le meme nombre, pour 1,96 contre 0,75 entre
   camps et 0,50 contre 0,79 a l'interieur. **Ce n'est plus « nous ajoutons une decomposition »,
   c'est « la mesure publiee ne peut pas voir l'effet ».** C'est l'argument le plus fort du
   dossier pour faire du chapitre de methode autre chose qu'une annexe.

4. **Ce qui est confirme pour la nuit de calcul.** L'axe qui porte l'effet reste l'ideologie et
   non la demographie : v6 sans ideologie depasse le hasard sur la queue, v8 avec ideologie tombe
   12,6 points en dessous, et leur rapport inter passe de 0,47 a 3,03. La quantite a surveiller
   sur un modele plus gros s'enrichit d'une seconde : au **rapport groupe sur personne** de a31,
   ajouter le **couple (rapport inter, rapport intra)** du panneau 4.

---

## 7. Ce que je n'ai pas pu verifier

1. **Nous n'avons pas de condition « persona vide ».** C'est la piece manquante de la
   replication, et c'est celle qui porte chez eux le resultat le plus spectaculaire, une queue a
   0,4644 sous un hasard a 0,5325. Une condition C4, meme modele, meme protocole, invite sans
   persona ni etiquette, la fournirait pour un run.
2. **L'ordre des modalites des 71 items ordinaux est herite de a25 et non relu.** Si l'ordre de
   `question_master/gss/main.csv` n'est pas l'ordre de l'echelle pour un item, la mesure ordinale
   est fausse pour cet item. Je n'ai verifie aucune des 71 nomenclatures.
3. **Le niveau de nos chiffres n'est pas comparable au leur** et je n'ai pas construit de
   transformation qui les rendrait comparables. Il faudrait rejouer leur code sur nos matrices,
   ce qui suppose de definir une etendue par item et une normalisation identiques aux leurs, et
   je ne l'ai pas fait.
4. **La convention d'egalite sur la definition ordinale.** Elle est departagee par une seule
   graine. La variante « extremes de l'echelle » montre que le classement ne bouge pas, mais je
   n'ai pas mesure la dispersion des valeurs sur plusieurs graines de departage.
5. **Le seuil de 5 pour cent.** Il est celui de leur code. Je n'ai pas mesure la sensibilite du
   classement a un seuil de 2 ou de 10 pour cent, alors que a29 montre que le passage de 10 a
   20 pour cent resserre nettement les ecarts.
6. **Twin-2K-500.** Toute l'analyse porte sur le GSS, comme a29 et a31. **Or leurs chiffres
   portent sur Twin-2K-500, et nous avons ce jeu.** Rejouer les tranches sur nos matrices Twin,
   avec les treize configurations de a6 et a8, mettrait les deux mesures sur le meme jeu de
   donnees. C'est la verification la plus utile qui manque, et elle ne coute aucun appel de
   modele.
7. **Un seul axe pour la decomposition.** Le terme inter est calcule sur l'ideologie a sept
   niveaux, parce que c'est le seul axe dont a1, a23, a28, a29 et a31 disent tous qu'il separe.
   Les cinq autres axes ne sont pas mesures ici.
8. **La comparabilite des six conditions de Stanford entre elles.** Six conditions, deux
   generations d'agents demographiques, des tailles d'invite tres differentes. Ce rapport les met
   dans le meme tableau parce que a1, a2, a25, a28 et a29 le font deja, pas parce que j'ai
   verifie qu'elles sont comparables.
9. **Leur fichier `joint_vector_metrics.csv`.** a36 n'en a lu que l'en tete. Les valeurs par
   resultat de leurs trois exactitudes de tranche y sont, et la distribution complete permettrait
   de comparer nos dispersions par item aux leurs. Je ne l'ai pas telecharge et ce rapport ne
   fait aucun calcul sur leurs donnees.

---

## 8. Questions ouvertes pour Simon

1. **Faut il ajouter une condition « persona vide » a la prochaine nuit de calcul ?** C'est la
   seule piece qui manque pour que la replication soit complete, elle coute un run de 150
   personnes sur 149 items, et c'est chez eux la condition qui porte le renversement. Sans elle,
   nous pouvons dire « le hasard bat l'etiquette dans la queue » ; avec elle, nous pourrions dire
   « et une invite sans information tombe sous le hasard », qui est leur phrase.

2. **Rejoue-t-on les tranches sur Twin-2K-500 avant de rediger ?** C'est leur jeu, nous l'avons,
   et cela coute zero appel de modele. Le resultat serait alors une comparaison sur les memes
   donnees et non seulement sur la meme forme. Je le recommande avant toute phrase de related
   work qui affirme une corroboration.

3. **Le panneau 4 est il la figure du papier ?** Il dit en une image que la mesure standard du
   retrecissement est aveugle a la distorsion que nous mesurons, avec deux points cernes de noir
   qui ne different que par une etiquette et un plancher humain calibre en (1 ; 1). C'est plus
   fort que la figure de a1, parce qu'il attaque une mesure publiee et pas seulement un phenomene.

4. **Que fait-on du resultat sur v6 ?** L'agent demographique sans ideologie est la seule methode
   du perimetre 1 052 qui depasse significativement le tirage uniforme sur les 5 pour cent du
   bas, et son rapport inter est de 0,466, c'est a dire qu'il **sous** separe les camps. C'est
   le meilleur argument du dossier pour dire que le probleme est l'etiquette ideologique et non
   la demographie, mais c'est aussi un agent que a19 decrit comme mal specifie. Est ce un pilier
   ou une note ?

5. **La definition categorielle et la definition ordinale ne donnent pas le meme classement**,
   rho plus 0,007 contre plus 0,832. Laquelle porte le papier ? La categorielle est plus severe,
   plus proche de ce qu'un institut achete, et c'est celle qui reproduit leur renversement.
   L'ordinale est la leur, donc la seule qui autorise une phrase du type « meme mesure, memes
   conclusions ».

6. **Faut il ecrire, en clair, que leur distorsion 1 est mal mesuree ?** Le point 2 de la section
   3.2 est frontal : sur la mesure qu'ils publient, l'agent le plus stereotype du corpus passe
   pour l'un des moins retrecis. C'est defendable, c'est chiffre, et c'est une critique d'un
   article de Science Advances signe par vingt trois auteurs. Arbitrage de redaction, pas de fait.

---

## Rejouer

```
.venv/bin/python analyses/a39_tranches.py --cache /tmp/a25-matrices.pkl \
    --cache-foret /tmp/a28-foret.npy --tirages 4000
.venv/bin/python analyses/a39_figure.py
```

Les deux caches sont ceux de a25 et de a28, les memes que a28, a29 et a31. S'ils manquent, ils
sont reconstruits, ce qui coute environ deux minutes et demie pour la foret aleatoire. Duree
totale ensuite : **79 secondes** pour `a39_tranches`, 5 pour la figure, sur quatre coeurs.
Graine d'analyse 20260908 partout, graine de grille 20260903, celle du run a5.
