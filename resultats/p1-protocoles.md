# p1. Deux protocoles qu'un partenaire peut signer : ce qui est verifie, ce qui manque

Seance du 9 septembre 2026. Livrables : `protocoles/01-experience-de-lecture.md`,
`protocoles/02-plan-nuit-sce.md`, `protocoles/p1-puissance.py`.

**Aucun appel de modele de langage. Aucun fichier existant du depot n'a ete modifie. Aucune
analyse de donnees.** Le seul calcul est un calcul de puissance sans donnees,
`.venv/bin/python protocoles/p1-puissance.py`, qui ne lit aucun fichier.

Conventions : **[MESURE]** calcule ici, **[CONFIRME]** lu dans une source verifiee avec son
adresse, **[PROBABLE]**, **[HYPOTHESE]**.

---

## Reponse en une ligne

**Le papier d'Ahler et Sood a ete lu en entier pour la premiere fois dans ce dossier, ce qui leve
trois blocages de `a46` d'un coup : leur experience de correction est decrite avec ses trois
conditions, ses deux effectifs et ses trois effets, convertibles en d de Cohen de 0,168 a 0,273 ;
leur condition « taux de base », qui augmente l'exageration de sept a neuf points au lieu de la
reduire, devient un sixieme bras du protocole ; et les vingt-cinq enonces de politique publique de
l'IGS Poll, dont le fichier manque de l'archive Dataverse, sont imprimes en clair dans l'annexe
OA 3.2.1, donc les libelles sont recuperables sans le fichier.** Le protocole de lecture qui en
sort tient en **1 806 analyses et environ 8 900 livres sterling**, moitie basse de la fourchette de
`MOONSHOTS.md`, et le plan de la nuit SCE tient en **28 920 appels et 4 a 6 heures**. [MESURE,
[CONFIRME]]

---

## 1. Ce qui est verifie, et ou

### 1.1 Le papier d'Ahler et Sood, lu en entier

`a46` section 7 point 1 declarait : « `journals.uchicago.edu` repond HTTP 403 ; Unpaywall declare
`is_oa: false` ; les tableaux et les libelles exacts de question tels qu'imprimes n'ont pas ete
lus. » **C'est leve.** La version d'auteur, datee du 15 aout 2017, est en acces libre sur le site
de Gaurav Sood, elle contient le corps, les tableaux et l'annexe en ligne complete, et elle a ete
lue integralement [CONFIRME, http://gsood.com/research/papers/partisanComposition.pdf, 4 720 lignes
apres conversion en texte].

Ce que la lecture confirme du recalcul de `a46`, sans le contredire nulle part :

| fait | source | statut |
|---|---|---|
| 32 pour cent de LGB percus chez les democrates contre 6 en realite ; 38 pour cent de republicains a plus de 250 000 dollars contre 2 | resume du papier | [CONFIRME], identique a `a46` |
| quatre democrates, quatre republicains, les huit dyades du codebook | corps, section de mesure | [CONFIRME] |
| les repondants tapent une estimation entre 0 et 100 dans une case a cote de chaque groupe ; ordre des groupes et ordre des deux batteries randomises | corps | [CONFIRME], et ce sont les libelles que `a46` avait reconstruits du codebook |
| realite calculee sur l'ANES 2012 pondere, sauf `dem_aa` et `rep_evang` pris du Pew Religious Landscape | corps et annexe OA 1.3 | [CONFIRME], identique a `a46` |
| condition « incitation a l'exactitude » : cinq cents de plus par reponse a moins de cinq points de la verite, soit 5,57 dollars de l'heure potentiels contre 2,14 | corps, note 11 | [CONFIRME], detail nouveau |
| condition « somme a 100 » : reduction de 1,94 point seulement, sur une erreur typique de 23,1 points | corps | [CONFIRME], detail nouveau |
| condition « taux de base » : la perception **monte** de sept a neuf points | tableau 2, n de 91 a 98 par condition | [CONFIRME], et c'est le fait qui ajoute un bras au protocole |

### 1.2 L'experience de correction, decrite pour la premiere fois avec ses parametres

C'est ce que la mission demandait de verifier, et voici le protocole exact.

**Deux experiences sur MTurk, differant seulement par la variable de sortie.** La premiere, avril
2014, **n = 1 036**, mesure l'extremite percue et le thermometre. La seconde, novembre 2014,
**n = 821**, mesure la distance sociale [CONFIRME].

**Trois conditions.** `ask`, on pose les quatre questions de composition du camp adverse avant les
mesures de sortie ; `tell`, on pose les memes questions puis **on donne la valeur correcte** avant
les mesures de sortie ; `control`, les mesures de sortie d'abord, les questions de composition plus
tard dans le questionnaire. Les questions de composition sont enveloppees dans une enquete de
connaissance politique plus large, **explicitement pour limiter la demande experimentale**
[CONFIRME].

**La formulation du retour correctif, mot pour mot.** En cas de surestimation : « The percentage of
Democrats (Republicans) who are g is smaller than you think. Only x % are g. (You overestimated by
[...] %) » ; en cas de sous estimation, la phrase symetrique [CONFIRME, annexe OA 4.2].

**Verification de manipulation.** L'erreur absolue moyenne passe de **27,7 a 6,1 points**, chute de
**21,6 points, IC 95 pour cent [-23,6 ; -19,5]**, significative sur chacune des huit dyades
[CONFIRME].

**Conformite et effet sur les conformes.** Est declare conforme celui qui donne au moins une des
quatre estimations de fin de questionnaire a moins de cinq points de la verite ; **74,2 pour cent**
le sont, definition liberale qui rend l'effet sur les conformes conservateur, estime par
assignation comme instrument [CONFIRME].

**Les trois effets, et leur conversion.**

| sortie | tell contre control | IC 95 pour cent | d de Cohen reconstruit |
|---|---|---|---|
| part de placements du sympathisant adverse a l'extreme | **-0,066** | [-0,11 ; -0,02] | **0,219** |
| thermometre, echelle 0 a 1 | **-0,064** | [-0,10 ; -0,03] | **0,273** |
| distance sociale | **-0,025** | [-0,05 ; 0,00] | **0,168** |

[CONFIRME pour les differences et intervalles ; MESURE pour les conversions,
`protocoles/p1-puissance.py` section 3]

**L'effet de la condition `ask` seule** vaut environ la moitie de celui de `tell`, **-0,03, IC
[-0,08 ; 0,01]**, juste sous le seuil conventionnel [CONFIRME]. C'est ce chiffre qui a impose la
conception de la mesure avant sur une moitie d'items tiree au hasard, decrite en q8 du protocole.

**Le placebo.** Aucune information n'etant donnee sur le camp propre, l'effet y est nul :
**0,01, IC [-0,03 ; 0,04]** sur l'extremite du camp propre, et un intervalle de [-0,04 ; 0,03] sur
son thermometre [CONFIRME]. C'est le controle de demande experimentale le moins cher du
dispositif, et il est repris tel quel.

**Ce que les auteurs disent eux memes de leurs limites**, et qui vaut avertissement pour nous :
« the treatment effects are relatively small, especially in the case of the affect experiments
[...] approximately 6 and 3 points on the feeling thermometer and social distance scale [...] we
lack the power to estimate variation in treatment effects by prior beliefs about partisan
composition with precision » [CONFIRME]. La moderation par la croyance de depart est donc declaree
exploratoire dans notre protocole, jamais confirmatoire.

### 1.3 Le fait qui debloque la version forte du programme A

`a46` section 2 etablit que la comparaison a trois termes porte sur des **compositions** et jamais
sur des **opinions**, parce que le fichier `pcomp_igspoll.dta` manque de l'archive Dataverse alors
que le `readme.txt` le cite. C'est exact et cela reste vrai du fichier.

**Mais les libelles ne manquent pas.** Les **vingt-cinq enonces de politique publique** de l'IGS
Poll sont imprimes en clair dans l'annexe **OA 3.2.1** du papier, avec la mention des enonces
inverses [CONFIRME]. Exemples verbatim : « The government should implement a single-payer health
care system, directly providing insurance coverage for all Americans free of charge. (RC) » ;
« The government should raise taxes on people who earn over $250,000 per year and cut taxes for
people who earn less than that. (RC) » ; « US foreign policy should emphasize military strength
over diplomacy. »

Le protocole d'interrogation est decrit lui aussi : chaque repondant voit **six enonces tires au
hasard des vingt-cinq**, declare sa propre position, puis estime le pourcentage de democrates puis
de republicains de Californie qui les soutiennent, ordre des partis randomise [CONFIRME].

**Consequence.** Ce qui manque a la version forte n'est plus le questionnaire, c'est la
**distribution reelle** des camps sur ces enonces. Une vague de calibrage de mille personnes sur la
meme plateforme la produit pour environ **1 400 livres sterling** au tarif verifie en 1.4. La
lettre a Gaurav Sood reste souhaitable, elle n'est plus bloquante.

**Les quatre echelles semantiques d'extremite percue** sont egalement imprimees en entier, annexe
OA 4.5, avec leurs cinq ou six modalites, sur les impots, l'avortement, les droits des homosexuels
et la politique raciale [CONFIRME]. Elles sont reprises au mot pres comme mesure de sortie, ce qui
donne au protocole une comparabilite directe avec l'effet de -0,066 publie.

### 1.4 Les tarifs de recrutement

**Prolific.** Recompense recommandee **9,00 livres sterling ou 12,00 dollars par heure**, minimum
absolu autorise **6,00 livres ou 8,00 dollars par heure** ; frais de plateforme **33,3 pour cent
des recompenses** pour un compte academique ou a but non lucratif, **42,8 pour cent** pour un
compte commercial [CONFIRME, deux adresses concordantes, https://www.prolific.com/pricing et
https://researcher-help.prolific.com/en/article/9cd998, consultees le 9 septembre 2026].

**CloudResearch.** Aucun tarif public. Connect, MTurk Toolkit et Prime Panels renvoient a des
calculateurs interactifs et a une demande de devis ; la seule information chiffree publiee est la
gratuite des frais pendant dix jours pour un compte academique nouveau sur Connect [CONFIRME comme
absence, https://www.cloudresearch.com/pricing/ et
https://www.cloudresearch.com/products/prime-panels/]. **Le budget CloudResearch ne peut pas etre
chiffre**, et c'est une demande a adresser au partenaire.

### 1.5 Le gabarit de preenregistrement

Le protocole 01 suit le gabarit **OSF Preregistration** version 2, cinq pages et vingt-cinq champs,
recuperes du schema lui meme : Study Information (titre, auteurs, description, hypotheses), Design
Plan (type d'etude, aveuglement, aveuglement additionnel, plan, randomisation), Sampling Plan
(donnees existantes, explication, procedures, taille, justification, regle d'arret), Variables
(manipulees, mesurees, indices), Analysis Plan (modeles, transformations, criteres d'inference,
exclusions, manquantes, exploratoire), Other [CONFIRME,
https://raw.githubusercontent.com/CenterForOpenScience/osf.io/develop/website/project/metadata/osf-preregistration.json].
OSF propose quatorze gabarits ; celui la est le plus courant [CONFIRME,
https://help.osf.io/article/145-preregistration].

### 1.6 La litterature de lecture de sorties d'IA sur la polarisation percue, 2024 a 2026

Recherche faite par l'API arXiv, le budget de recherche web de la session etant epuise a
l'ouverture (200 requetes sur 200).

**Aucune experience randomisee ou des humains lisent ce qu'un modele dit d'un camp politique et ou
la perception de ce camp est mesuree avant et apres n'a ete trouvee.** Douze entrees sur la requete
croisant polarisation affective et modele de langage, trois sur meta perceptions et polarisation
percue, cinq sur mauvaises perceptions et modele de langage. Ce sont des absences sur arXiv, qui
n'est ni SSRN ni les revues de science politique.

Les trois voisins les plus proches, tous utiles comme ancrage :

| travail | ce qu'il fait | ce qu'il donne |
|---|---|---|
| **Reranking partisan animosity in algorithmic social media feeds alters affective polarization**, arXiv 2411.14652, publie dans *Science* 390(6776), 27 novembre 2025 | experience de terrain preenregistree de dix jours, **1 256 participants** sur X pendant la campagne de 2024, rerangement par modele de langage des messages exprimant de l'animosite partisane | **deux points sur un thermometre de 100**, soit un d d'environ 0,08 : c'est la borne qui dit qu'une seance unique ne peut pas viser l'affect [CONFIRME] |
| **Personalized Large Language Models Can Increase the Belief Accuracy of Social Networks**, arXiv 2506.06153 | experience preenregistree, **N = 1 265**, election de 2024 | les gens **revisent vers la verite** au contact d'un modele verifie, puis recomposent leur reseau vers des croyances plus exactes [CONFIRME] |
| **Addressing Climate Action Misperceptions with Generative AI**, arXiv 2602.22564 | **1 201 participants**, modele specialise contre recherche web contre agent generaliste | seul le modele specialise augmente la connaissance et l'intention ; un agent generaliste ne suffit pas [CONFIRME] |

**Ce que ces trois travaux disent ensemble, et qui compte pour la conception.** Un modele qui
**corrige** deplace des croyances ; un modele qui **rerange un flux** deplace l'affect de deux
points en dix jours. Personne n'a mesure ce que fait un modele qui **decrit un camp**, sans
intention corrective, dans l'usage ordinaire. C'est exactement le creneau du programme A, et ce
constat est le meilleur argument de nouveaute a mettre dans la lettre au partenaire.

---

## 2. Ce que les deux protocoles decident, et qui n'etait pas decide

### 2.1 Protocole 01, l'experience de lecture

**Quatre decisions de conception, chacune avec sa raison chiffree.**

1. **Le bras modele est decline par modele, pas tire au hasard.** Raison : les trois modeles de R1
   rendent des facteurs de 0,245, 0,618 et 1,268 avec des intervalles disjoints du plancher humain
   **dans des directions opposees** [MESURE, r1 1.2]. Un tirage au hasard estimerait la moyenne
   d'effets de signes predits opposes, et un zero y serait indistinguable de deux issues
   contraires. Ce n'est pas une perte de puissance, c'est une perte d'identification.
2. **Le texte est presente comme une reponse d'assistant.** Raison : c'est la situation reelle, et
   cela supprime toute tromperie sur la source.
3. **Ancrage parti pour les compositions, ideologie pour les opinions.** Reponse a la question
   ouverte 3 de `a46`, avec son cout ecrit : il n'y aura pas de nombre unique resumant
   l'experience.
4. **Un sixieme bras, les taux de base.** Raison : la condition Base Rates d'Ahler et Sood
   **augmente** l'exageration de sept a neuf points, d reconstruit de 0,276 a 0,398, et R1 mesure
   que le defaut des modeles **est** un defaut de taux de base, point fixe vers un tiers sur
   8 718 modalites. Sans ce bras, un effet des bras modele serait attribue a la representation des
   camps alors qu'il pourrait n'etre qu'un ancrage numerique.

**Huit hypotheses**, dont la plus forte est **H4** : les trois bras modele doivent se classer, sur
l'ecart percu entre camps, **dans l'ordre de leurs facteurs mesures en R1**. Elle predit qu'une
quantite calculee sur la machine en une nuit **ordonne des effets sur des lecteurs humains**. C'est
la seule facon de faire de la mesure d'audit autre chose qu'une description, et si elle tombe il
faudra l'ecrire.

**Puissance.** Effet retenu **d = 0,22**, la valeur de la mesure de croyance d'Ahler et Sood ;
puissance 0,80 ; Holm au cas le plus defavorable, alpha 0,0167 ; covariable de depart a **r = 0,45**,
volontairement basse. Plan equilibre equivalent : **345 par bras**. Plan retenu, allocation
optimale a un temoin commun et cinq traitements : **250 par bras traite, 558 au temoin,
1 806 analyses, 2 080 recrutes**, et la precision du contraste est identique au plan equilibre a
345 par bras, `1/250 + 1/558 = 0,005797 = 2/345` [MESURE, `p1-puissance.py` section 5].
L'allocation inegale paye exactement le sixieme bras.

**Budget verifie** : pilote de 150 personnes et etude principale, vingt minutes, 9,00 livres de
l'heure, frais academiques, **8 917,77 livres sterling** ; en compte commercial, 9 553,32
[MESURE sur les tarifs confirmes]. C'est **la moitie basse** de la fourchette de 15 000 a
30 000 euros de `MOONSHOTS.md`, et l'ecart s'explique entierement par le type de panel : la
fourchette du moonshot suppose un panel probabiliste, Prolific n'en est pas un. Ahler et Sood ont
fait exactement ce choix, leur etude descriptive sur YouGov apparie et pondere, leurs quatre
experiences sur MTurk, avec la defense chiffree en note 9 de leur papier [CONFIRME].

**Cinq criteres de chute ecrits avant**, dont deux commandent tout : si le bras distribution vraie
ne reduit pas l'erreur absolue moyenne d'au moins 10 points la ou Ahler et Sood en obtiennent 21,6,
**rien n'est conclu des bras modele** ; si le placebo sur le camp propre sort de [-0,04 ; 0,04],
la demande experimentale n'est pas maitrisee.

**Ce que l'errata E3 de `MOONSHOTS.md` demande et que le protocole ne tient pas.** L'errata demande
des bras indexes par modele **et par identite du demandeur**. A neuf bras, l'allocation optimale
donne 233 par bras traite et 660 au temoin, soit **2 528 analyses et 2 908 recrutes**, environ
40 pour cent de budget en plus, donc **12 237 livres** [MESURE]. C'est hors de la fourchette de
1 500 a 2 000 personnes. L'indexation par demandeur est declaree en extension E1 avec son prix, et
si le budget est fixe, le bras a sacrifier est **gpt-oss-20b**, dont le facteur intermediaire
n'ajoute rien au contraste de H4.

### 2.2 Protocole 02, la nuit sur le SCE

**Modele principal : `gpt-oss-20b`, coupure juin 2024**, anterieure de neuf mois a la premiere date
notee ; **`Llama 3.1 8B`, coupure decembre 2023**, garde comme variation de coupure sur `infl1`
seul. Les deux Qwen sont exclus : aucune coupure publiee, verifiee sur trois sources independantes
par `a3` [CONFIRME comme absence].

**Cohortes et mois** : les six cohortes pleines les plus peuplees, 48 pour cent des observations,
cent menages chacune, 600 agents ; contexte decembre 2024 a fevrier 2025, fenetre notee **mars a
juin 2025**, choisie pour contenir **les deux regles de choc de `c1` a la fois**, la primaire qui
designe juin, la secondaire qui designe avril, et la montee de plus 1,17 point depuis decembre
2024. Toutes les quantites sont rendues sous les deux regles.

**Trois conditions appelees**, C2 demographies seules, C3 avec l'historique du menage, DESC la voie
description ; **quatre adversaires a zero appel**, persistance, demographies, moyenne de cohorte,
et **le controle statistique par tirage**, qui conserve les marges et detruit l'appariement des
personnes.

**Cinq quantites, avec la cible humaine en face** : part inter cohortes **0,019**, part stable
**0,525**, chute sous permutation intra cohorte **superieure a 0,639 puis a 0,615**, rapport
d'ampleur des revisions contre son propre nul a derive **0,43 et non 1,00**, chute sur qui revise
**0,287 dont 0,140 pour la seule volatilite passee**.

**La question qui commandait le run est tranchee** : le jumeau est note sur **ce qu'il ajoute a la
persistance**, la chute complete publiee a cote, parce que la persistance capte deja 96 pour cent
de ce que la foret va chercher.

**Appels et heures** : **28 920 appels**, dont 24 120 sur gpt-oss-20b et 4 800 sur Llama ; aux
debits mesures par `a3` en configuration reelle, 7 212 et 6 384 appels par heure, cela fait
**4 h 06 de machine**, a annoncer **4 a 6 heures**, une nuit.

**Six criteres de chute**, dont un qui ferme une branche du programme, C3 sous 0,615, et un qui
serait un resultat publiable en soi, C2 aussi bon que C3, ce qui serait un contre exemple a `a44`.

**Quatre issues, et ce que chacune veut dire pour une banque centrale**, dont la plus severe : une
population simulee qui rend un rapport d'ampleur proche de 1,00 **bouge deux fois trop**, et une
banque centrale qui s'en servirait surestimerait la reactivite des menages, donc l'effet de sa
propre communication.

---

## 3. Ce qui manque

Trois choses, et aucune n'est un probleme de methode.

**Un partenaire de science politique.** Le protocole 01 n'est pas deposable sans co-signataire :
le champ q2 du gabarit OSF est obligatoire, un comite d'ethique ne siege pas pour un individu sans
rattachement, et Prolific en compte academique exige une affiliation pour les frais a 33,3 pour
cent. C'est le meme manque que `MOONSHOTS.md` liste depuis le debut, et il est desormais **le seul
chemin critique** de l'etage causal : tout le reste est ecrit.

**Un comite.** Comite d'ethique de la recherche d'universite francaise ou *institutional review
board* americain, selon le partenaire. Delai a prevoir de quatre a huit semaines, et c'est le
chemin critique du calendrier, pas la collecte, qui tient en une semaine. Precedent a citer dans la
demande : les etudes d'Ahler et Sood ont ete « deemed exempt by Stanford University and the
University of California, Berkeley » [CONFIRME].

**Un choix de plateforme, et une reponse de CloudResearch.** Prolific est chiffre et verifie.
CloudResearch ne publie rien et exige un devis. Les panels probabilistes, AmeriSpeak et YouGov, qui
justifieraient la fourchette de 15 000 a 30 000 euros du moonshot, n'ont aucun tarif public verifie
ici. Il faut trois devis avant de fixer le budget definitif.

**Ce qui ne manque plus, et qu'il faut cesser de citer comme manquant** : les libelles de l'IGS
Poll, les echelles d'extremite percue, les parametres de l'experience de correction, la forme
exacte du retour correctif, les effectifs et les effets convertis. Tout cela est dans le papier et
il a ete lu.

---

## 4. Ce que je n'ai pas pu verifier

1. **Le budget de recherche web etait epuise a l'ouverture**, 200 requetes sur 200. Tout ce qui est
   verifie ici l'a ete par recuperation directe d'adresses, pas par recherche. Les absences
   signalees en 1.6 sont donc des absences sur arXiv et sur les adresses consultees, **pas des
   absences dans la litterature**. SSRN, les revues de science politique et les preprints de
   psychologie n'ont pas ete interroges.
2. **Les tarifs des panels probabilistes.** AmeriSpeak, NORC, YouGov, Ipsos KnowledgePanel : aucun
   tarif public verifie. La fourchette de 15 000 a 30 000 euros de `MOONSHOTS.md` reste
   [HYPOTHESE].
3. **Le taux de change livre vers euro.** Non verifie. La conversion donnee dans le protocole 01,
   1,15 euro pour une livre, est [HYPOTHESE] et doit etre refaite au jour de la demande.
4. **Le pourcentage de perte de 15 pour cent.** Choisi comme valeur usuelle pour une enquete en
   ligne de vingt minutes avec deux controles d'attention ; **aucune source verifiee**. Le pilote
   le mesurera, et la taille de recrutement doit etre recalculee apres le pilote.
5. **La duree de vingt minutes.** Estimation a partir du nombre d'items, non mesuree. Elle porte
   directement le budget : quinze minutes le ramenent a 6 688 livres, vingt-cinq minutes le
   portent au dela de 11 000. Le pilote la tranche.
6. **La correlation r = 0,45 entre la mesure avant et la mesure apres.** C'est une hypothese de
   travail, prise basse parce que la covariable porte sur l'autre moitie des items. Si elle vaut
   0,30, il faut 394 par bras en plan equilibre au lieu de 345, soit environ 15 pour cent de
   participants en plus. La table de sensibilite est publiee dans le protocole precisement pour
   cela.
7. **Que la prose d'un modele porte la distribution que R1 lui a fait ecrire en chiffres.** Rien ne
   le garantit, et c'est le risque technique numero un du protocole 01. Le controle est ecrit,
   distance de variation totale sous 0,05 entre la distribution impliquee par la prose et la
   cellule R1, avec liste de reserve et retrait du bras au dela de trois echecs sur seize ; il n'a
   jamais tourne.
8. **Les debits de `a3` transposes au run SCE.** Les 7 212 et 6 384 appels par heure sont mesures
   sur des prefixes de persona de 3 029 tokens dans la configuration de la phase 1, pas sur les
   prefixes du regime C3 du SCE, qui contiennent un historique de trois mois sur cinq variables.
   La duree de 4 h 06 est donc une estimation transposee [PROBABLE], d'ou l'annonce a 4 a 6 heures.
9. **Que le choc de 2025 soit le choc tarifaire.** Reserve recopiee de `c1` et non levee : le mois
   est defini depuis les donnees par une regle ecrite d'avance, aucune donnee externe n'a ete
   consultee [HYPOTHESE].
10. **Le run composition de `a46` n'avait pas rendu** a l'heure de cette seance. Le protocole 01
    suppose que les huit dyades ont un terme de modele ; si le run echoue, six d'entre elles n'en
    ont pas, et le bloc composition du protocole se reduit a `union1` et `reborn`. Le protocole ne
    depend pas de ce run pour exister, mais son bloc composition en depend pour etre compare a R1.
11. **`a37`, `a38`, `a44`, `a46`, `c1`, `a3` et `r1` sont cites tels que ces rapports se citent
    eux memes.** Aucun n'a ete rejoue ici, et `MOONSHOTS.md` a ete modifie pendant la seance par
    l'errata E3, qui a ete lu et pris en compte.

---

## 5. Questions ouvertes pour Simon

1. **Le bras F change t il la nature du protocole 01 ?** Il repond a une question de psychologie du
   jugement, l'ancrage numerique, et non a une question de representation des camps. Il est
   indispensable comme controle et il coute 250 participants. Faut il le garder en famille
   confirmatoire, comme ici, ou le passer en secondaire pour rendre alpha aux trois bras modele ?
2. **H4, la prediction d'ordonnancement, est elle trop ambitieuse pour un preenregistrement ?**
   Elle predit que trois nombres calcules sur une machine ordonnent trois effets humains. Si elle
   tombe, elle tombera bruyamment, et un relecteur y verra la faiblesse du programme entier. Faut
   il la porter en tete, ou la declarer confirmatoire mais secondaire ?
3. **Ecrit on a Gaurav Sood maintenant ou apres le run composition ?** La lettre coute une heure et
   ne bloque plus rien puisque les libelles sont recuperes ; mais le fichier donnerait la
   distribution reelle et economiserait la vague de calibrage de 1 400 livres.
4. **Le protocole 02 attend une ligne d'Amir.** Il est ecrit, fige, chiffre, et **aucun appel ne
   doit partir avant cette ligne**. La seule chose encore ouverte est le fichier SCE 2013-2016, et
   la reponse peut etre non sans rien coder.

---

## 6. Fichiers produits

| fichier | contenu |
|---|---|
| `protocoles/01-experience-de-lecture.md` | le preenregistrement de l'experience de lecture, aux vingt-cinq champs du gabarit OSF |
| `protocoles/02-plan-nuit-sce.md` | la page de plan de la nuit SCE, a valider en une ligne avant tout appel |
| `protocoles/p1-puissance.py` | le calcul de puissance et les conversions d'effets, sans aucune donnee |
| `resultats/p1-protocoles.md` | ce rapport |

## 7. Rejouer

```
cd /Users/amirkellousidhoum/Desktop/Code/Projets/popsim
.venv/bin/python protocoles/p1-puissance.py
```

Aucune donnee n'est lue, aucun fichier n'est ecrit.
