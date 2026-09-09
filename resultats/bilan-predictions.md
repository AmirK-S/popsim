# Bilan de nos propres predictions

Note ecrite le 9 septembre 2026. Elle ne mesure rien de nouveau : elle relit les treize pages
de plan preenregistrees du dossier et les rapports qui leur repondent, et elle note le
dossier sur ce qu'il avait annonce. Aucun calcul n'a ete refait, aucun appel de modele n'a
ete passe, aucun fichier existant n'a ete modifie.

Conventions employees ici. Une prediction est dite tenue, fausse, a moitie ou indecidable.
Le verdict retenu est celui que le rapport se donne lui meme dans son tableau de score ; quand
le rapport n'a pas de tableau de score, c'est le verdict de la section qui traite l'hypothese.
La direction d'une prediction est un jugement de cette note et non du rapport : en faveur de
la these quand sa realisation renforce l'enonce central du dossier, contre la these quand sa
realisation le fragilise ou detruit un de nos instruments, neutre quand elle ne coute ni ne
rapporte rien, typiquement une replication de la litterature ou une calibration.

Enonce central du dossier, tel qu'il est reformule dans MODELE-DU-MONDE.md section 7 : une
etiquette demographique produit un gabarit de groupe, ce qui reste d'une personne au dela de
son segment est de l'ordre du centieme du bruit humain, les populations simulees ecrasent la
variance interne et gonflent l'ecart entre groupes, et l'avantage mesure sur les reponses
rares est de l'heterogeneite reelle et non du bruit de petite cellule.

---

## 1. Preuve d'anteriorite, et ce qu'elle vaut reellement

Le protocole du projet, PROTOCOLES-DE-RECHERCHE.md section 4 point 3, demande que la page
soit deposee sur OSF, horodatee, avant que le premier script tourne. Aucune des treize pages
n'a ete deposee sur OSF ni ailleurs hors de la machine. La seule trace disponible est donc
la date de derniere modification des fichiers, qui est une borne superieure et non une date
de creation, et l'horodatage que la page s'attribue dans sa premiere ligne.

Trois pages, r1, r4 et a46, citent un depot, le commit d536169dc5361c38edcd723d48816e2ddd06dc4f.
Ce commit appartient au depot parent Desktop/Code, il est date du 9 aout 2026, soit un mois
avant ces pages, et il ne contient aucun fichier de popsim : `git ls-files resultats/` ne rend
rien, le projet n'est pas suivi en version. Cette citation ne prouve donc rien du tout, et elle
est ecrite a l'endroit exact ou le lecteur attend une preuve.

Ecarts mesures, en minutes, entre la page et le premier artefact de son experience.

| page | horodatage declare | mtime de la page | premier script ou premiere sortie | ecart |
|---|---|---|---|---|
| a42 | 15:42:15 | 15:43:56 | a42_commun.py, 15:45:36 | 3 min 21 s |
| a43 | 15:41:50 | 15:43:10 | a43_commun.py, 15:45:20 | 3 min 30 s |
| a44 | 15:46 | 15:48:33 | a44_mesures.py, 15:57:07 | 11 min |
| i1 | 18:30 | 18:32:46 | i1_commun.py, 18:38:52 | 8 min 52 s |
| i3 | 19:12 | 19:11:32 | i3_commun.py, 19:19:03 | 7 min |
| i3b | 21:05 | 21:08:28 | i3b_commun.py, 21:10:17 | 5 min 17 s |
| c1 | 22:30 | 22:33:13 | c1_dispersion.py, 22:43:43 | 13 min 43 s |
| t2 | 01:05 | 01:07:18 | t2_amplitude.py, 01:15:40 | 10 min 40 s |
| r1 | 22:06:11 | 22:08:01 | r1-controles-smoke.csv, 22:15 | 8 min 49 s |
| r2 | 22:05:00 | 22:05:42 | r2-tableau-essai.csv, 22:18 | 13 min |
| r3 | 22:30:01 | 22:32:01 | r3-tableau-essai.csv, 22:47 | 17 min |
| r4 | 23:45 | 23:57:57 | r4-h4-restitution.csv, 23:52 | 7 min sur l'horodatage declare, moins 6 min sur le mtime de la page |
| a46 | 22:45 | 22:46:43 | a46_ahler_sood.py, 22:35:54 | moins 9 min |

Deux lignes posent probleme et il faut les nommer.

r4. Le tableau H4, r4-h4-restitution.csv, existe a 23:52, alors que la page de plan a ete
modifiee pour la derniere fois a 23:57:57. Le rapport r4-oracle-socle.md declare de lui meme
que la ligne q4 de H4 est une analyse a posteriori, faite sur des traces qui existaient deja
quand H4 a ete ecrite, et que H4 n'est prospective que pour q4base, q4nogab et q4hyb. La
declaration est honnete ; l'ecart de mtime dit qu'elle est meme un peu plus grave que ce
qu'elle avoue, puisque le chiffre existait avant la derniere ecriture de la page.

a46. Les cinq scripts a46_*.py portent des dates de derniere modification comprises entre
22:35:54 et 22:44:41, toutes anterieures a la page, qui se declare ecrite a 22:45 et dont le
mtime est 22:46:43. Les sorties, elles, sont posterieures, a 22:50. La lecture la plus
probable est celle que r2 et r3 revendiquent explicitement pour eux memes, un script ecrit et
verifie hors ligne avant la page, aucun appel de modele passe ; cette lecture est acceptable,
mais alors elle doit etre ecrite dans la page, comme r2 et r3 le font, et a46 ne le fait pas.

Les onze autres lignes sont coherentes avec leur declaration. Aucune n'est une preuve, parce
que la date de derniere modification se deplace au moindre reenregistrement et que le Bureau
est synchronise ; ce sont des indications concordantes, pas des horodatages.

---

## 2. Le detail, page par page

### a42, le plancher de bruit de cellule et la rarete stable

Quatre predictions signees, notees dans la reproduction du preenregistrement du rapport.

| | enonce | direction | issue |
|---|---|---|---|
| a | H1 passe pour les six conditions de Stanford et pour C3, incertain pour C2, v7 et les trois imputations | en faveur | tenue |
| b | H2 echoue pour B1, B3 foret, PMM et IM | en faveur | fausse, PMM et IM passent |
| c | H3 non significative pour la majorite | neutre | fausse, significativement positive pour six methodes sur treize |
| d | P_C, le placebo, montre un gradient non nul | contre | tenue, et beaucoup plus fort que prevu |

Anteriorite : 3 min 21 s entre la page et le premier script, la plus courte de la serie avec
a43.

Ecarts declares : aucun. La page ne comporte pas de section d'ecarts et le rapport n'en ouvre
pas. Un erratum est ajoute le 9 septembre apres la seconde relecture adverse : la mesure
appelee ablation de l'etiquette dans le resume et dans la section 6 est en realite un
contraste de conditionnement, C2 et C3 n'echangeant pas l'etiquette mais toute leur entree.
Gravite : mesure mal nommee, correction posterieure a la publication.

Resultat post hoc presente comme confirmation : oui, en partie. Le cinquieme paragraphe de la
reponse en une ligne, presente comme une quatrieme mesure independante, ne correspond a aucun
des cinq tests preenregistres H1 a H5, qui ne contiennent pas de contraste C2 contre C3. Il
est place au meme rang que les tests declares, sans marque distinctive.

### a43, ce qui reste d'une personne quand on lui retire son item puis son groupe

Six predictions, P1 a P6, introduites par la phrase qui compte : elles sont celles de la
these, section 7 de MODELE-DU-MONDE.md.

| | enonce | direction | issue |
|---|---|---|---|
| P1 | R2 apres retrait du segment indistinguable de zero pour v6, v8 et C2 | en faveur | fausse au sens strict, vraie au sens pratique |
| P2 | conditions riches strictement positives et sous le dixieme du plafond humain | en faveur | fausse, C3 a 8 pour cent et les riches 21 a 36 |
| P3 | les imputations par tirage sont entre les deux | neutre | fausse, elles sont au niveau des riches |
| P4 | aucune condition a modele de langage ne bat la moyenne d'item leave one out | en faveur | a moitie, vraie pour cinq conditions, fausse pour les trois riches, enonce mal cadre |
| P5 | rapport interaction sur effet de personne superieur a 5 chez nos humains | neutre | tenue, 27,1 et 7,7 a 8,4 |
| P6 | ordre aveugle, etiquette, riche sur le rapport d'ecarts types | en faveur | a moitie, casse sur v8 |

Les trois predictions explicitement tirees de la these, P1, P2 et P3, sont fausses toutes les
trois. Les deux predictions de replication de la litterature, P4 pour sa moitie comparable et
P5, tiennent.

Anteriorite : 3 min 30 s.

Ecarts declares : aucune section d'ecarts. Une analyse non preenregistree est signalee en
clair dans la section 4.3, ajoutee apres avoir vu que B0 mode obtient une correlation non
nulle apres retrait du segment. Gravite : ajout post hoc d'un plancher.

Resultat post hoc presente comme confirmation : oui, sous une forme signalee. Le plancher de
bruit du demoyennage est ajoute apres coup, et c'est lui qui transforme le verdict de P1,
fausse, en la formule que la reponse en une ligne retient, elle n'est pas distinguable du
bruit des que l'echantillon descend a 150 personnes. Le crochet est declare ; la phrase de
tete l'utilise quand meme.

### a44, le generateur nul conditionnellement independant de Yuan

Six predictions, P1 a P6, scorees dans un tableau du rapport.

| | enonce | direction | issue |
|---|---|---|---|
| P1 | C2 et v8 indistinguables de leur nul sur Q1 et Q2 | en faveur | tenue |
| P2 | les conditions riches s'ecartent du nul sur Q5 par le haut | en faveur | tenue mais sans valeur, les treize s'en ecartent |
| P3 | C2 ne s'ecarte pas du nul sur Q5, C3 si | en faveur | fausse, les deux s'en ecartent |
| P4 | les humains s'ecartent tres largement du nul sur Q5 | neutre | tenue |
| P5 | chute d'exactitude proche de zero pour C2 et v8, nette pour les humains et les riches | en faveur | tenue, et c'est le resultat du rapport |
| P6 | Q3 plus grand dans le nul que dans la population simulee | contre | tenue pour les seize conditions |

Anteriorite : 11 min.

Ecarts declares : trois, plus une mesure preenregistree abandonnee. E1 ajoute deux conditions
descriptives de reference, ajout justifie et hors famille. E2 ramene Q6 et Q7 de 200 replicats
a 50, gravite faible, quantites deja secondaires. E3 ajoute un complement descriptif non prevu,
signale post hoc partout. Le bootstrap sur les personnes de Q3, preenregistre, n'a pas de sens
tel qu'ecrit et n'est pas publie. Sept errata s'ajoutent apres la seconde relecture adverse,
dont E2, qui etablit que la chute sous permutation n'est pas invariante a la segmentation, et
E5, qui etablit qu'elle est correlee a 0,91 avec l'exactitude brute.

Resultat post hoc presente comme confirmation : oui, et le rapport l'ecrit lui meme. Le critere
primaire declare, Q5, ne separe rien : les treize conditions recoivent porteur de personne avec
le meme p de Holm. Le seul test qui separe, la permutation intra segment, a ete preenregistre
comme remplacement de la perturbation d'ordre et non comme quantite de verdict, et ses deux
seuils de lecture, 15 pour cent et 40 pour cent du plancher humain, ne sont pas declares avant.
La section 7.2 le signale explicitement ; la reponse en une ligne ouvre quand meme sur ce
critere. C'est le cas le plus grave de la serie : le verdict du rapport repose sur une quantite
et sur des seuils choisis apres les chiffres.

### i1, qui change d'avis dans les panels GSS

Six predictions, scorees dans un tableau du rapport.

| | enonce | direction | issue |
|---|---|---|---|
| P1 | plus de 90 pour cent des items changent plus a quatre ans qu'a deux semaines | neutre | tenue, 93,2 pour cent |
| P2 | part dirigee mediane sous 0,25 | en faveur | tenue, 0,131 |
| P3 | le taux d'aller retour depasse le taux de changement persistant | en faveur | fausse, 0,1172 contre 0,2812 |
| P4 | AUC du predicteur primaire entre 0,55 et 0,65 | neutre | tenue, 0,6100 |
| P5 | chute du predicteur primaire positive et sous 0,03 point d'AUC | en faveur | fausse, 0,0905, trois fois la borne |
| P6 | les hors quadrant changent plus, et l'ecart survit a la permutation | en faveur | a moitie |

Anteriorite : 8 min 52 s.

Ecarts declares : six, plus deux points non executes et non remplaces. E1 remplace un controle
bloquant vide, l'inversion de l'ordre des vagues laissant la part de changement monotone
strictement inchangee par symetrie de la regle. E2 ajoute un cinquieme predicteur, la position
initiale seule. E3 ajoute un temoin. E4 change la machinerie de correction : le p empirique sur
200 permutations a un plancher de 1 sur 201, alors que Holm sur 118 items exige moins de
0,000424, si bien que le preenregistrement demandait une correction que son propre nombre de
permutations rendait impossible ; le p par approximation normale la remplace. E5 et E6 sont des
reductions de cout. Gravite : E4 est un seuil qui bouge, mais dans le sens honnete, parce que
le seuil declare etait inapplicable ; E1 et E2 sont des ajouts post hoc declares avant lecture.

Resultat post hoc presente comme confirmation : non. P3 et P5 sont publiees fausses, la regle
de decision 1 est appliquee telle qu'ecrite et ne se declenche pas.

### i3, detecter et quantifier une population synthetique

Sept predictions, scorees dans un tableau du rapport.

| | enonce | direction | issue |
|---|---|---|---|
| P1 | les trois statistiques separent v8 a 25 et 50 pour cent | en faveur | tenue |
| P2 | tau etoile sous 10 pour cent pour v8, au dessus de 25 pour composite | en faveur | a moitie, composite a 11,5 |
| P3 | PMM non detectable sous 25 pour cent par la concentration | en faveur | tenue |
| P4 | PMM detectable par le deficit de patrons a un taux plus bas | en faveur | tenue |
| P5 | B0 segment deplace A et B en sens inverse, visible au dela de 25 pour cent | neutre | a moitie, direction tenue, seuil faux d'un facteur quatre |
| P6 | erreur au dessus de 15 points en calibration croisee, sous 5 en calibration propre | neutre | a moitie |
| P7 | l'ecart gauche droite croit avec v8 et C2, decroit avec PMM, E2 et B0 segment | en faveur | fausse |

Anteriorite : 7 min.

Ecarts declares : cinq. E1 change le mode de reechantillonnage de la statistique B, avec le
biais mesure et publie, 13,3 pour cent de la valeur ; gravite : changement de mesure, chiffre
a l'appui. E2 change le pivot de l'intervalle. E3 ajoute une source descriptive, hors famille,
apres avoir constate que le controle negatif preenregistre etait trivialement nul. E4 precise
une definition. E5 deplace un calcul du CSV vers le rapport. Deux errata s'ajoutent le 9
septembre, dont E2, qui etablit que le facteur 1,62 attribue a v8 est en realite celui de C2 ;
or ce facteur est le motif ecrit de la prediction P7, qui est fausse.

Resultat post hoc presente comme confirmation : non. Le rapport ecrit que les predictions
fausses sont les plus informatives et ne reecrit aucune.

### i3b, l'abaque, la norme, la contamination ciblee

Sept predictions, scorees dans un tableau du rapport.

| | enonce | direction | issue |
|---|---|---|---|
| P1 | rapport tau etoile 300 sur 1052 entre 1,5 et 2,3 pour six fabricants sur neuf | neutre | fausse, cinq sur neuf |
| P2 | a 5000, tau etoile de v8 sous 1 pour cent, E2 au dessus de 10 | neutre | a moitie, v8 a 1,06 |
| P3 | la bande de Twin a les memes deux bords, treize configurations du cote pauvre | en faveur | tenue |
| P4 | au moins une configuration de Twin sous 5 pour cent, rapport pire sur meilleure au dessus de 3 | contre | tenue et largement, rapport 30 |
| P5 | concentre plus detectable par camp, moins globalement, deplacement plus fort | neutre | a moitie, deux tiers tenus |
| P6 | le fabricant qui vise la bande est constructible, et reste vu sous 25 pour cent par une reserve | en faveur | fausse sur la premiere moitie, a moitie fausse sur la seconde |
| P7 | le prix de l'invisibilite croit avec tau etoile, et reste sous 10 pour cent a 1052 | en faveur | a moitie |

Anteriorite : 5 min 17 s. La page declare en section 0 les trois inspections structurelles
faites avant redaction, ce qui est la bonne pratique du lot.

Ecarts declares : huit. E1 et E2 changent la construction du bruit de reference, E6 fait lire
a la surface d'attaque une courbe ajustee a une autre taille, E7 avoue que le nombre de tirages
par cellule n'etait pas fixe d'avance, E8 restreint un controle. Gravite : deux changements de
mesure et un parametre non fige, tous declares.

Resultat post hoc presente comme confirmation : non. Deux tenues sur sept, publiees telles
quelles, et le rapport designe les fausses comme les plus utiles.

### c1, les anticipations des menages americains

Six predictions, scorees dans un tableau du rapport.

| | enonce | direction | issue |
|---|---|---|---|
| P1 | part inter cohortes sous 0,15 a tous les mois | en faveur | tenue, maximum 0,048 |
| P2 | le mois du choc tombe en avril ou mai 2025 | neutre | fausse sous la regle primaire, juste sous la secondaire |
| P3 | l'IQR monte d'au moins 10 pour cent au choc | en faveur | fausse, il baisse de 14 pour cent |
| P4 | part stable entre 0,25 et 0,55 | en faveur | tenue, 0,525 |
| P5 | chute de H superieure a celle de D de 0,05, et P capte 70 pour cent de F | en faveur | tenue deux fois |
| P6 | chute nulle sur la direction de la revision, ecart au nul sous 3 points | en faveur | a moitie |

Anteriorite : 13 min 43 s. La page declare en section 0 ce qui a ete lu avant, y compris trois
observations brutes, ce qui est la declaration la plus scrupuleuse de la serie.

Ecarts declares : sept, plus un point non execute. E1 est le plus lourd et le plus honnete :
la regle de traitement preenregistree, multiplier l'amplitude par moins un pour la direction
decrease, aurait retourne le signe de cinq variables sur douze et rendu tout le rapport faux,
parce que la colonne du fichier public est deja signee ; la regle n'est pas appliquee et un
controle bloquant est ajoute a la place. E2 ajoute deux controles, E3 corrige un temoin
indefini, E4 change le codage du mois, E5 reduit des tirages, E6 publie le choc sous les deux
regles, E7 ajoute un predicteur de niveau. Gravite : une definition de mesure abandonnee, deux
controles et un predicteur ajoutes.

Resultat post hoc presente comme confirmation : non, a la limite pres qu'il faut nommer. P2 et
P3 sont fausses sous la regle primaire et sauvees, l'une entierement l'autre a moitie, sous la
regle secondaire. Le rapport dit clairement laquelle porte le verdict et E6 declare la double
publication ; l'exercice reste celui qu'un lecteur severe appellera une seconde chance.

### t2, qui bouge, version agregee

Six predictions, scorees dans un tableau du rapport.

| | enonce | direction | issue |
|---|---|---|---|
| P1 | rapport reel sur nul entre 0,35 et 0,60 a quatre ans | en faveur | fausse, 0,625 |
| P2 | rapport plus grand a quatre ans qu'a deux ans | en faveur | tenue |
| P3 | M5 bat M0 d'au moins 0,3 point | en faveur | tenue, plus 0,403 |
| P4 | variance inter groupes expliquee sous 0,25 | en faveur | fausse, 0,447 |
| P5 | la gauche n'est pas le camp qui change le moins, ecart sous 2 points | neutre | a moitie |
| P6 | aucun modele ne bat M0 sur le deplacement projete | en faveur | tenue |

Anteriorite : 10 min 40 s.

Ecarts declares : sept. E1 est le plus instructif du dossier entier : M5, l'oracle empirique de
cellule, avait ete declare comme un plafond et n'en est pas un, il porte tout le bruit
d'echantillonnage d'une moitie et se fait battre par un estimateur lisse ; deux quantites
nouvelles sont ajoutees pour mesurer ce que M5 ne pouvait pas mesurer. E3 porte les permutations
de 200 a 1 000, ecart favorable qui rend Holm satisfiable, et c'est exactement la lecon E4 de
i1, appliquee. E2 retire des intervalles invalides sur un niveau. E4 a E7 sont des reductions de
perimetre pour cout de calcul, dont E6, qui reconduit sans le resorber l'ecart E6 de i1.
Gravite : une mesure declaree plafond qui n'en est pas une, et deux quantites ajoutees apres le
premier calcul.

Resultat post hoc presente comme confirmation : non. La regle de decision 1 reste appliquee
telle qu'ecrite, et les deux quantites ajoutees sont declarees comme telles.

### r1, l'oracle des camps

Cinq predictions directionnelles, H1, H2a, H2b, H3 et H4. Le rapport n'ouvre pas de tableau de
score ; les verdicts ci dessous sont ceux de ses sections 1.1 a 1.5.

| | enonce | direction | issue |
|---|---|---|---|
| H1 | rapport Gini Simpson decrit sur reel inferieur a 1 | en faveur | fausse, rejetee dans la direction inverse, dix huit cellules sur dix huit au dessus de 1 |
| H2a | ecart non signe entre camps superieur a 1 | en faveur | a moitie, non significatif sur deux modeles, superieur sur un seul |
| H2b | ecart signe superieur a 1 | en faveur | a moitie, 0,245 et 0,618 sous le plancher, 1,268 au dessus |
| H3 | l'effet de l'identite du demandeur depasse le plancher humain | en faveur | tenue, six cellules sur six, 2,74 a 4,23 fois le plancher |
| H4 | correlation de rang positive avec la derive de l'item | en faveur | a moitie, dix cellules sur douze passent Holm, la seconde quantite echoue sur Qwen3-4B |

H1 est le rejet le plus important de la serie. La these dit ecrasement de la variance ; les
trois modeles decrivent les camps comme plus varies qu'ils ne sont, et le camp le plus
homogene en realite est celui qu'ils sur decrivent le plus. Le rapport tranche ensuite que
l'ecrasement est une propriete du couple modele et protocole et non du modele, avec un facteur
14 entre le mode description et le mode incarnation sur le meme fichier de poids.

Anteriorite : 8 min 49 s entre la page et la premiere sortie d'essai.

Ecarts declares : pas de tableau d'ecarts. Quatre mesures sont declarees non preenregistrees
en clair dans le texte, dont l'absence de direction sur H3, un controle externe, une lecture de
distribution anti correlee et l'ajustement d'un coefficient de retrecissement. Les cinq criteres
de chute sont appliques : le critere 2 fait sortir onze cellules sur 2 682 et l'analyse de
sensibilite est publiee.

Resultat post hoc presente comme confirmation : un cas, et il est corrige a l'interieur du
dossier. Le rapport de run r1-oracle-des-camps.md ecrit que les douze cellules de H4 passent
Holm ; r1-resultats.md etablit que dix passent et deux sont a p ajuste 0,0700, et signale
l'erreur de lecture du CSV. Une reserve non prevue est ajoutee sur la seconde quantite de H4,
dont la correlation n'est definie que sur les items ou le modele differencie encore les camps,
ce qui la rend non comparable entre modeles.

---

## 3. Le tableau global, notre calibration

Predictions signees et deja tranchees : 53, reparties sur neuf pages de plan.

| page | predictions | tenues | fausses | a moitie |
|---|---|---|---|---|
| a42 | 4 | 2 | 2 | 0 |
| a43 | 6 | 1 | 3 | 2 |
| a44 | 6 | 5 | 1 | 0 |
| i1 | 6 | 3 | 2 | 1 |
| i3 | 7 | 3 | 1 | 3 |
| i3b | 7 | 2 | 2 | 3 |
| c1 | 6 | 3 | 2 | 1 |
| t2 | 6 | 3 | 2 | 1 |
| r1 | 5 | 1 | 1 | 3 |
| total | 53 | 23 | 16 | 14 |

Parts : 43,4 pour cent tenues, 30,2 pour cent fausses, 26,4 pour cent a moitie. En comptant une
moitie pour une demie, le credit global est de 30 sur 53, soit 56,6 pour cent.

Par direction, et c'est la seule chose que ce bilan avait a produire.

| direction | predictions | tenues | fausses | a moitie | credit |
|---|---|---|---|---|---|
| en faveur de la these | 37 | 16 | 12 | 9 | 55,4 pour cent |
| contre la these | 3 | 3 | 0 | 0 | 100 pour cent |
| neutre | 13 | 4 | 4 | 5 | 50,0 pour cent |

Lecture. Nous ne sommes pas beaucoup plus faux quand nous predisons en notre faveur : 55,4
pour cent de credit contre 50,0 sur les predictions neutres, un ecart de cinq points sur des
effectifs de 37 et 13, qui ne veut rien dire. Le defaut de calibration n'est pas la, il est
dans le volume : trente sept predictions en faveur de la these contre trois qui la mettent en
danger. Nous ne perdons pas nos paris orientes, nous n'en prenons presque jamais qui puissent
nous couter. Et les trois seules qui pouvaient nous couter, le placebo de a42, le deficit de
patrons de a44 et la non transportabilite des ordres de grandeur de i3b, sont tenues toutes
les trois : quand nous parions contre nous, nous avons raison a chaque fois, ce qui est le
signe qu'elles etaient plus faciles a voir venir que les autres et qu'elles ont ete ecrites
avec la reponse en tete.

Deuxieme lecture, sur la forme des erreurs. Sur les douze predictions fausses en faveur de la
these, neuf le sont dans le meme sens : le signal est plus grand, plus previsible ou plus
detectable que nous ne l'annoncions. i1 P5, la chute vaut trois fois la borne. t2 P4, la
variance inter groupes expliquee vaut 0,447 pour une borne a 0,25. a43 P2, C3 garde 8 pour cent
du plafond pour un dixieme annonce. i3 P2, composite est detectable a 11,5 pour cent quand nous
annoncions plus de 25. c1 P6, la direction de la revision est plus previsible que prevu. La
lecture il n'y a rien la dedans est systematiquement trop forte, et elle est trop forte du meme
cote a chaque fois.

Troisieme lecture, la plus severe. Les deux rejets dans la direction inverse, a42 c et r1 H1,
disent tous les deux la meme chose : nos populations et nos modeles sont, sur les mesures
concernees, plus varies et non moins. Sur le mode description de r1, l'ecrasement de la variance
n'existe pas, il s'inverse. C'est une prediction dirigee tiree directement de la these, et elle
est fausse a l'unanimite de trois modeles et de dix huit cellules.

---

## 4. Les predictions en attente

Vingt trois predictions signees ne sont pas encore tranchees. Elles sont recopiees ici dans
leur formulation d'origine, pour que le matin les note sans les reecrire. Le verdict attendu
est tenue, fausse, a moitie, ou non testee, jamais non rejetee.

### r2, la comparaison appariee sur les gens rares, en regime severe

Page horodatee 22:05:00. Cinq predictions.

| | enonce | direction |
|---|---|---|
| a | H1a passe pour C3F gpt-oss, exces positif sur le plancher de segment sur les raretes stables des 58 items | en faveur |
| b | H1b passe contre B2 famille retiree argmax, E1 famille retiree et IM m=10 mode ; incertain contre PMM k=10 famille retiree et E2 famille retiree tirage | en faveur |
| c | H2 echoue au moins contre PMM k=10 famille retiree, le modele de langage paie en precision ce qu'il gagne en rappel | contre |
| d | H3a reste entierement negatif, mais l'ecart median passe sous les 9,8 points de Qwen3-4B contre PMM k=10 | contre |
| e | H4a place C3F gpt-oss sous 80 pour cent de diversite conservee | en faveur |

Familles declarees, corrigees separement par Holm : F1 primaire, rappel, 7 tests ; F2
secondaire, precision, 7 tests ; F3 tertiaire, exactitude globale, 7 tests ; F4 quaternaire,
structure, 8 tests plus H4c descriptif et non testable, declare d'avance comme tel.

### r3, la vraie ablation de l'etiquette

Page horodatee 22:30:01. Neuf hypotheses, toutes enoncees dans le sens ou la these les predit,
ce qui doit etre note au moment de la lecture.

| | enonce | direction |
|---|---|---|
| H1a | la chute d'exactitude sous permutation intra segment diminue de C3 a C3E | en faveur |
| H1b | le ratio inter augmente de C3 a C3E | en faveur |
| H1c | la rarete de groupe sur personne augmente de C3 a C3E | en faveur |
| H1d | l'exactitude par personne de C3E est superieure ou egale a celle de C3 | neutre |
| H2a | le ratio inter sur l'axe ideologie tombe de C2 a C2S | en faveur |
| H2b | la chute sous permutation sous segmentation ideologie augmente de C2 a C2S ; sans prediction sous la segmentation sans ideologie | en faveur |
| H2c | la rarete de groupe sur personne diminue de C2 a C2S | en faveur |
| H2d | exactitude par personne, C2 contre C2S, bilaterale | neutre |
| H3 | l'effet C3E contre C3ES depasse en valeur absolue l'effet C3ES contre C3 | en faveur |

H3 n'est testee que si C3ES tourne sur au moins 30 personnes communes ; sinon elle est declaree
non testee, et la page interdit d'ecrire non rejetee.

### r4, l'oracle des camps sur le modele socle

Page horodatee 23:45. Quatre hypotheses.

| | enonce | direction |
|---|---|---|
| H1 | le socle decrit la dispersion interne des camps plus pres de 1 que l'instruit, sur au moins deux camps sur trois en identite journaliste | en faveur |
| H2 | l'ecart entre camps decrit par le socle est plus pres du reel que celui de l'instruit, sur H2b | en faveur |
| H3 | la part du format seul tombe dans 0,20 a 0,80 pour le facteur signe et pour la dispersion du camp de gauche | neutre |
| H4 | le modele est plus proche des marginales nationales publiees du GSS que de l'echantillon de 1 052 personnes, et davantage pour l'instruit que pour le socle | en faveur |

Precisions a respecter au moment de noter. H3 n'est calculee que si l'intervalle de la
difference socle moins instruit exclut zero ; sinon la phrase imposee est le format et les poids
ne se separent pas sur cette quantite. H4 est deja mesuree sur q4, plus 0,0215 et plus 0,0240
selon l'identite, p de Holm 0,0217 et 0,0120, et cette ligne est declaree par le rapport lui
meme comme une analyse a posteriori ; H4 n'est prospective que pour q4base, q4nogab et q4hyb.
Le controle de puissance preenregistre est passe, mediane a 0,107 pour un seuil a 25 pour cent
de 0,233.

### a46, le run court composition

Page horodatee 22:45. Cinq predictions.

| | enonce | direction |
|---|---|---|
| H1 | la croyance du modele depasse la realite, rapport superieur a 1 | en faveur |
| H2a | log croyance modele sur realite decrite, moins log croyance humaine sur realite d'Ahler et Sood, superieur a zero | en faveur |
| H2b | log croyance modele moins log croyance humaine, superieur a zero, lecture de controle | en faveur |
| H3 | la valeur donnee depend de qui demande, aucune direction predite | en faveur |
| H4 | l'ecart croyance camp moins croyance population est positif la ou le groupe est sur represente | en faveur |

L'hypothese nulle interessante est nommee dans la page et doit etre publiee telle quelle si
elle se realise : si les modeles ne s'ecartent pas de la realite plus que les humains, le
modele est un correcteur de l'ignorance pluraliste et non une machine a en produire.

Reserve a porter au moment de la notation : les cinq scripts a46 portent des dates de derniere
modification anterieures a la page, et la page ne declare pas, comme r2 et r3 le font pour eux
memes, que le script etait ecrit et verifie hors ligne avant elle.

---

## 5. Ce que cela dit de la methode

### Erreur recurrente 1, la prediction dirigee quand la litterature ne tranche pas

a43 l'ecrit noir sur blanc : ses predictions sont celles de la these. Les trois qui en
descendent directement, P1, P2 et P3, sont fausses toutes les trois, et les deux qui repliquent
un resultat publie, P4 pour sa moitie comparable et P5, tiennent. r1 H1 est le meme cas a plus
grande echelle : la these dit ecrasement, la mesure dit sur dispersion, sur trois modeles et
dix huit cellules. i3 P7 est le cas le plus net d'une prediction dirigee assise sur un chiffre
fragile : son motif ecrit est le facteur 1,62 attribue a v8, dont l'erratum du 9 septembre
etablit qu'il est celui de C2 ; la prediction est fausse et la variable qui separe n'est pas
celle du motif. Le point commun des trois est qu'aucune de ces pages ne declare, au moment
d'ecrire la prediction, que la litterature est en desaccord ou que le chiffre de motif est
conteste.

Le symptome mesurable est le rapport 37 contre 3. Une famille de predictions dont 70 pour cent
vont dans le sens de l'auteur n'est pas une famille de paris, c'est un plaidoyer avec des
intervalles de confiance.

### Erreur recurrente 2, les bornes declarees qui n'en sont pas

t2 E1 est le cas pur : M5 est declare comme un plafond dans la page et se fait battre par M4
au premier calcul, ce qui est impossible pour un plafond ; deux quantites de remplacement sont
ajoutees apres coup. a42 declare son troisieme plancher, les humains de la vague 2, en precisant
dans la page qu'il est en pratique un plafond, ce qui est la bonne pratique et montre que le
projet sait faire la distinction quand il y pense. a43 decouvre apres coup que le demoyennage
par segment a un plancher de bruit non nul, mesure a 0,0224 sur 18 segments et 0,0449 sur 42,
et ce plancher non prevu est ce qui sauve la lecture de P1. i3b E1 et E2 refont deux fois la
construction du bruit de reference apres avoir vu que la premiere ne tenait pas.

Quatre pages sur neuf ont donc du reparer, en cours de route, une quantite presentee comme une
borne. Aucune des neuf ne demandait, avant le calcul, la preuve que la borne en etait une.

### Erreur recurrente 3, les nuls mal specifies

a44 P2 est le cas d'ecole : la prediction est tenue et sans valeur, parce que les treize
conditions s'ecartent du nul, humains et regression logistique compris. Un test que tout le
monde passe n'est pas un test. i1 E1 decouvre au premier calcul que le controle bloquant 2 est
vide par symetrie de la regle et ne pouvait rien detecter. i3 E3 constate que le controle
negatif preenregistre, les humains melanges a eux memes, est trivialement nul et ne mesure
aucune fausse alarme ; une source descriptive est ajoutee pour en mesurer une vraie. Dans les
trois cas, le defaut etait visible sur le papier, sans donnees : personne n'avait ecrit quel
temoin devait echouer au controle.

Corollaire, et c'est le passage le plus grave de tout le lot : a44 constate que son critere
primaire ne separe rien, le declare, et fonde quand meme son verdict et sa reponse en une ligne
sur une quantite preenregistree comme remplacement d'autre chose, avec deux seuils de lecture
ecrits apres les chiffres.

### Trois regles proposees pour PROTOCOLES-DE-RECHERCHE.md

Elles ne sont pas inserees. Elles viendraient a la suite des dix lignes de la section 4.

R11, la prediction qui coute. Une page de plan n'est pas valide si elle ne contient pas au
moins une prediction dont la realisation affaiblit la these du dossier, et au moins une
quantite dont une valeur nommee d'avance obligerait a reecrire la phrase de la section 7 de
MODELE-DU-MONDE.md. Le rapport score ses predictions par direction, en faveur, contre, neutre,
et publie les trois taux. Motif mesure : 37 predictions en faveur contre 3 contre, et 3 sur 3
tenues du cote contre, ce qui indique des paris pris avec la reponse en tete.

R12, toute borne se prouve avant. Une quantite nommee plancher, plafond, nul ou reference ne
peut porter un verdict que si la page donne, avant le calcul, le temoin qui doit la saturer et
la valeur qu'il doit atteindre, ou l'argument d'invariance qui la rend indepassable. A defaut,
la quantite est publiee comme temoin descriptif, sans p et sans verdict, et le rapport n'a pas
le droit d'ecrire part du plafond ni exces sur le plancher. Motif mesure : t2 E1, a43 section
4.3, i3b E1 et E2, quatre reparations en cours de route sur neuf pages.

R13, le critere de verdict est nomme, il ne se remplace pas, et son anteriorite se prouve hors
de la machine. La page nomme une quantite de verdict et une seule par famille ; si elle ne
separe rien, le rapport publie ce nul comme resultat, et toute quantite de substitution est
publiee en exploration, sans p, sans tableau de verdict, et jamais dans la reponse en une
ligne. La page est horodatee par un temoin exterieur a la machine avant que le premier script
existe, et le rapport publie l'ecart en minutes entre cet horodatage et le premier fichier de
sortie. Motif mesure : a44 section 7.2, verdict porte par une quantite et deux seuils choisis
apres coup ; et l'absence totale de depot externe, avec un commit cite par trois pages qui les
precede d'un mois et ne les contient pas.

---

## 6. Ce que je n'ai pas pu verifier

1. L'anteriorite, au sens strict. Aucune des treize pages n'est deposee hors de la machine.
La date de derniere modification n'est pas une date de creation, elle se deplace au moindre
reenregistrement, et le Bureau est synchronise, ce qui ajoute une source de deplacement. Les
ecarts du tableau de la section 1 sont des indications concordantes, jamais des preuves. Je
n'ai pas non plus pu verifier les pages qui declarent ce fichier n'est plus modifie ensuite.

2. Les verdicts eux memes. Je n'ai refait aucun calcul. Chaque tenue et chaque fausse de ce
bilan est le verdict que le rapport se donne, lu dans son tableau de score. Si un rapport a
mal lu son propre CSV, je l'ai recopie. Le seul cas connu de ce type, les douze cellules de H4
de r1 qui sont dix, a ete trouve par le dossier et non par moi.

3. Le decompte des predictions. Compter une prediction a deux moities comme une ou comme deux
est une convention que j'ai choisie ; la deplacer deplace les parts globales de plusieurs
points. Le total de 53 depend de cette convention, en particulier sur r1, ou j'ai compte H2a
et H2b separement, et sur a42, ou j'ai compte quatre predictions et non les cinq familles
d'hypotheses.

4. La direction. Aucune page ne declare si sa prediction va dans le sens de la these ou contre
elle. Le classement en faveur, contre, neutre est ma lecture, et c'est la partie la plus fragile
du tableau de calibration. Un lecteur qui classerait a44 P6 en faveur plutot que contre ferait
tomber a deux sur deux notre seul echantillon de paris contre nous.

5. Les errata. Je n'ai pas lu a45-relecture-adverse-2.md. Le nombre d'errata par rapport vient
des titres des sections errata, et la gravite des objections qui les ont provoques n'est pas
appreciee ici.

6. Les experiences en attente. r2, r3 et r4 ont deja des fichiers d'essai et de fumee sur le
disque, et a46 a deja ses tableaux Ahler et Sood. Je ne les ai pas ouverts : certaines des
vingt trois predictions en attente sont peut etre deja partiellement decidables, et je ne peux
pas dire lesquelles.

7. Le contenu des runs. Je n'ai lu aucune trace, aucun prompt, aucun cache de modele. Rien
dans ce bilan ne verifie que les conditions comparees sont bien celles que les pages decrivent ;
l'erratum E1 de a42 et l'objection 1 de a45, qui portent exactement sur ce point, montrent que
la question n'est pas theorique.
