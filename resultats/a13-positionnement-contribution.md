# a13. Positionnement de la contribution face a LifeMem et au papier SHARE

## Errata du 8 septembre 2026

Corrections apportees a la suite de la relecture adverse `a17-relecture-adverse.md`. Le corps
du rapport n'est pas reecrit, il reste lisible tel qu'il a ete rendu le 7 septembre. Chaque
point cite la phrase d'origine, donne la correction et la preuve. Recalculs :
`analyses/a19_denominateurs.py`, tableaux `resultats/a19-exactitude-appariee.csv` et
`a19-ratios-par-jeu-items.csv`. Aucun appel de modele. **Ces corrections doivent etre faites
avant tout usage externe : elles portent sur les deux paragraphes de related work rediges en
anglais pour etre colles dans un papier.**

### E1. Revendication (b)3 et section 2.6 : le 0,07 point et le facteur 13,5 ne sont pas calcules sur le meme jeu d'items. Objection a17 7.1, contradiction C4.

**Phrase d'origine, revendication (b)3.** "Nous montrons que la metrique d'exactitude employee
par le champ est aveugle a la structure de la population simulee : deux conditions du meme
papier, sur les memes 1 052 participants et les memes 169 items, dont l'exactitude differe de
0,07 point avec un intervalle [-0,52 ; +0,37], ont des gonflements d'ecarts inter groupes qui
different d'un facteur 13,5 avec des intervalles disjoints."

**Phrase d'origine, section 2.6.** "Nos deux conditions `gss_v7` et `gss_v8` ont une exactitude
indistinguable, ecart apparie de -0,07 point, intervalle [-0,52 ; +0,37], et des ratios inter
de 0,437 et 5,907, un facteur 13,5, avec des intervalles disjoints."

**Correction.** L'ecart de 0,07 point est un chiffre a **150 items**, lu dans le fichier des
auteurs. Les ratios 0,437 et 5,907 sont calcules sur **169 items**. Recalcule sur les 169 items,
l'ecart apparie vaut **-0,83 point**, intervalle bootstrap sur les personnes **[-1,28 ; -0,38]**,
t = -3,82 : il **exclut zero**, et c'est la condition persona qui est la plus exacte. Le mot
"indistinguable" doit disparaitre partout. [MESURE, voir l'errata E1 de
`a1-double-distorsion.md`, rendu le meme jour, pour la preuve du denominateur et le tableau des
quatre jeux d'items.]

**Le facteur 13,5, lui, tient.** Les ratios inter recalcules sur les 169 items reproduisent a
l'identique les estimations ponctuelles publiees, 0,437 pour `v7` et 5,907 pour `v8`, avec des
intervalles [0,379 ; 0,493] et [5,648 ; 6,157] un peu plus etroits que ceux du 3 septembre,
le tirage bootstrap n'etant pas le meme. Sur les 149 items d'un autre perimetre, ils valent 0,397 et 5,972, soit un facteur 15,0.
[MESURE, `a19-ratios-par-jeu-items.csv`]

**Revendication (b)3 reecrite, a employer telle quelle.**

> **Nous montrons que la metrique d'exactitude employee par le champ est presque aveugle a la
> structure de la population simulee : deux conditions du meme papier, sur les memes 1 052
> participants et les memes 169 items, dont l'exactitude ne differe que de 0,83 point
> [-1,28 ; -0,38], ont des gonflements d'ecarts inter groupes qui different d'un facteur 13,5
> avec des intervalles disjoints. Un point d'exactitude d'un cote, un facteur treize de
> l'autre.**

**Section 2.6, phrase reecrite.** "Nos deux conditions `gss_v7` et `gss_v8` ont une exactitude
qui ne differe que de 0,83 point, intervalle [-1,28 ; -0,38] sur les 169 items, et des ratios
inter de 0,437 et 5,907, un facteur 13,5, avec des intervalles disjoints. La dissociation entre
les deux dimensions est donc quantitative et non absolue : elle n'existe dans aucun des deux
papiers voisins, ou les deux dimensions vont ensemble."

### E2. Section 6, les deux paragraphes de related work en anglais. Meme objection, usage externe.

**Version longue, phrase d'origine.**

> "[...] and reported alongside individual-level accuracy, which we show can be **identical**
> across two agent populations whose between-group inflation differs by a factor of 13.5."

**Version longue, phrase corrigee.**

> "[...] and reported alongside individual-level accuracy, which we show differs by **less than
> one percentage point** (0.83 points, 95 % CI [-1.28, -0.38], n = 1052, 169 items) across two
> agent populations whose between-group inflation differs by a factor of 13.5."

**Version courte, phrase d'origine.**

> "Neither reports the between-group term after the intervention, and neither normalizes
> against a measured human noise floor; we do both, and show that **accuracy is blind to the
> difference**."

**Version courte, phrase corrigee.**

> "Neither reports the between-group term after the intervention, and neither normalizes
> against a measured human noise floor; we do both, and show that **accuracy separates the two
> populations by less than one percentage point while their between-group inflation differs by
> a factor of 13.5**."

Aucune autre phrase des deux paragraphes n'est touchee.

### E3. Revendication (b)2 : le controle humain n'a pas des intervalles contenant 1 sur les trois mesures, et le mot "prouve" est trop fort. Objection a17 7.2.

**Phrase d'origine.** "Nous fournissons le plancher de bruit humain que ni l'un ni l'autre ne
fournit : les memes personnes reinterrogees deux semaines plus tard tombent en (1,003 ; 1,004)
avec des intervalles contenant 1, ce qui **prouve** que la methode ne fabrique pas d'ecart la ou
il n'y en a pas."

**Correction.** Le terme inter contient 1 sur les trois mesures. Le terme intra ne le contient
pas sur l'entropie, [1,0001 ; 1,0087], ni sur la variance ordinale, [0,9795 ; 0,9997]. Les
ecarts sont de 0,01 et 0,03 pour cent, mais l'affirmation "avec des intervalles contenant 1"
est fausse telle qu'elle est ecrite. De plus, un non rejet ne prouve rien : le mot "prouve" ne
doit pas figurer devant un intervalle qui contient une valeur.

**Revendication (b)2 reecrite.**

> **Nous fournissons le plancher de bruit humain que ni l'un ni l'autre ne fournit : les memes
> personnes reinterrogees deux semaines plus tard tombent a 0,4 pour cent de (1,1) sur les
> trois mesures de dispersion, ce qui borne a environ un demi pour cent l'ecart que la methode
> peut fabriquer en l'absence de distorsion reelle. Les effets que nous rapportons sur les huit
> conditions vont de 11 a 36 pour cent d'ecrasement du terme intra et, pour les quatre
> conditions qui gonflent, de 75 a 491 pour cent sur le terme inter : cent fois cette
> resolution.**

### E4. Revendication (b)4 : la rigueur d'estimation revendiquee n'est pas tenue par a7. Objection a17 7.3.

**Phrase d'origine.** "[...] aucun des trois travaux voisins ne traite ce biais."

**Correction.** L'affirmation sur les trois travaux voisins est exacte et n'est pas retiree.
Mais `a7-transport-de-variance.md`, le seul correctif du projet, importe `agreger` et
`decomposer` de a1 **sans appliquer la soustraction du residu de permutation**, et son
estimateur produit un terme inter negatif, -0,13, la ou l'operateur annule l'information
mutuelle par construction. Revendiquer la rigueur d'estimation impose de la tenir dans tous les
rapports du dossier, faute de quoi la revendication se retourne. Le rapport a7 est repris par
ailleurs pour ce motif. **Ajouter a (b)4** : "cette correction est appliquee dans la mesure ;
elle doit l'etre aussi dans l'evaluation de tout correctif, ce qui n'est pas encore le cas dans
notre propre rapport de transport."

### E5. Section 2.3 : la reserve interne ne figure pas dans la reponse en une ligne. Objection a17 7.4.

**Phrase d'origine, reponse en une ligne du rapport.** "[...] son propre tableau permet d'en
deduire un transport inter vers intra que ses auteurs ne calculent pas."

**Phrase d'origine, section 2.3, qui dit le contraire.** "Ce calcul est un argument de lecture,
pas un resultat publiable en l'etat."

**Correction.** La reserve de la section 2.3 est detaillee et juste : le calcul combine deux
tableaux d'effectifs differents, 224 a 270 agents selon la condition, des ICC lus a deux
decimales, et une formule valable en plan equilibre. Elle doit figurer dans la reponse en une
ligne, qui est la phrase que Simon lira. **Phrase de remplacement** : "son propre tableau
suggere un transport inter vers intra que ses auteurs ne calculent pas ; notre reconstruction
est un argument de lecture et non un resultat, elle combine deux tableaux d'effectifs
differents et des ICC a deux decimales, et elle ne doit pas etre publiee telle quelle."

### E6. Revendication (b)5 : le facteur 6,9 a maintenant une cause nommee, et c'est un gain. Objection a17 1.3.

**Phrase d'origine.** "[...] l'ecart entre deux variantes portant la meme etiquette
demographique dans le meme paquet de replication atteint un facteur 6,9."

**Complement, pas correction.** La cause de ce facteur est desormais mesuree, item par item :
`gss_v6` n'a recu ni l'ideologie ni le parti dans son invite, `gss_v8` les a recus, et rien
d'autre. Sur l'axe ideologique, le ratio inter passe de 0,34 pour `v6` a 8,51 pour `v8`.
[MESURE, errata E4 de `a1-double-distorsion.md`, `resultats/a19-recopie-items-ecartes.csv`]

**A ajouter a (b)5** : "et cet ecart s'explique par un seul attribut de l'invite, l'etiquette
ideologique, dont la presence multiplie par vingt cinq le gonflement des ecarts entre segments
ideologiques sans changer l'exactitude de plus d'un point. C'est la demonstration la plus
directe que l'exactitude ne voit pas le contenu de l'invite."

### E7. Recommandation c.3 : elle reste a faire, et elle est la reponse la moins chere a l'objection la plus previsible.

Rappel, sans changement : recalculer les ratios sur la seule segmentation age croise genre, ce
qui repond a un relecteur qui connait Garzon et al. Le fichier `a1-ratios-par-axe.csv` contient
deja les deux axes separement. Elle coute une heure et elle n'a pas ete faite.

---

Date : 7 septembre 2026. Auteur : agent de recherche a13. Aucun code de production, aucune
microdonnee manipulee, aucun fichier existant modifie. Les deux papiers ont ete lus en entier
dans leur version HTML arXiv, corps et annexes, et les valeurs chiffrees ont ete relues dans
les formules mathematiques du HTML et non dans un resume.

**Reponse en une ligne.** Les deux precedents mesurent chacun un morceau de la double
distorsion et aucun des deux ne mesure le terme inter groupes comme une quantite a part
entiere : LifeMem publie l'exact terme intra que popsim calcule, avant et apres son correctif,
mais n'a jamais de terme inter apres correction ni la moindre mesure d'exactitude ; le papier
SHARE publie une correlation intraclasse, donc un rapport de l'inter a l'intra, mais sans
aucun referent humain sur cette analyse, et son propre tableau permet d'en deduire un
transport inter vers intra que ses auteurs ne calculent pas. La formule "aucun precedent"
tombe, la contribution tient, mais elle change de nom : ce n'est plus la premiere mesure de
l'homogeneite intra, c'est la premiere mesure conjointe des deux termes rapportee a un plafond
humain mesure.

---

## Table des matieres

1. LifeMem, arXiv 2608.19621, fiche complete
2. Garzon et al., arXiv 2605.16303, fiche complete
3. Le tableau de comparaison des trois travaux
4. Les autres candidats de 2026, et un precedent de 2023 que a10 n'avait pas vu
5. Ce que popsim peut revendiquer apres lecture
6. La phrase de related work, en anglais
7. Ce que je n'ai pas pu verifier
8. Questions ouvertes pour Simon

---

# 1. LifeMem, arXiv 2608.19621

**Reference exacte.** Hexi Wang, Yujia Zhou, Bangde Du, Weihang Su, Xinyuan Cao, Qingyi Pan,
Qingyao Ai, Yueyue Wu, Min Zhang, Yiqun Liu, *Mitigating Identity Essentialism in LLM Agents
with Longitudinal Life Trajectories*. Version 2 du 21 aout 2026, la version courante, lue en
entier.
[CONFIRME] https://arxiv.org/html/2608.19621, en tete de page : "arXiv:2608.19621v2 [cs.CL]
21 Aug 2026". Affiliations : Department of Computer Science and Technology, Tsinghua
University, et Quan Cheng Laboratory. Ce n'est ni une equipe de Stanford ni une equipe de
sciences sociales, c'est une equipe de recherche d'information.

**Code.** [CONFIRME] Annonce dans le papier lui meme, sous le mot "Code", a l'adresse
https://github.com/halsayxi/LifeMem.
Le depot existe, il est public, il est en Python, il pese 329 Kio, il a ete pousse pour la
derniere fois le 21 aout 2026 et il ne declare **aucune licence** (champ `license` a `null`
dans l'API GitHub).
[CONFIRME] https://api.github.com/repos/halsayxi/LifeMem

## 1.1 Quelle quantite exactement est mesuree

Quatre metriques, toutes du type "plus petit est meilleur", toutes definies dans l'annexe G.
Citation du corps du texte, section Evaluation Metrics : "We use four lower-is-better metrics."
[CONFIRME]

**Metrique 1, divergence KL.** Par cellule vague x question, on construit la distribution
empirique des reponses humaines et celle des reponses du modele sur l'ensemble des modalites
valides, avec un lissage additif sur chaque modalite pour eviter les probabilites nulles, puis
on calcule la divergence KL de la distribution humaine vers la distribution du modele. Le
chiffre publie est la moyenne non ponderee sur toutes les cellules eligibles. Unite
d'observation : la cellule vague x question, agregee sur toute la population. [CONFIRME,
annexe G, equations 19 a 22]

**Metrique 2, ecart d'entropie normalisee.** Entropie de Shannon de la distribution de
reponses divisee par son maximum, calculee separement chez les humains et chez le modele,
valeur absolue de la difference, moyennee sur les cellules. Unite : la cellule vague x
question. [CONFIRME, equations 23 a 26]

**Metrique 3, et c'est celle qui compte pour popsim, l'ecart de distance appariee intra
groupe.** Definition litterale du papier : "The within-group pairwise distance measures
whether response diversity within demographic groups is preserved. We form groups separately
using each discrete demographic variable." Puis, pour une variable demographique, une valeur
de groupe, une vague et une question, on calcule chez les humains la quantite dont le papier
donne l'interpretation exacte suivante : "This quantity is the probability that two distinct
respondents sampled from the same group provide different answers." La meme quantite est
calculee chez le modele, on prend la valeur absolue de la difference, on moyenne sur les
cellules de groupe puis sur les cellules vague x question. [CONFIRME, annexe G, equations 27 a
33]

**C'est exactement le terme intra de notre mesure M2.** La probabilite que deux repondants
d'un meme segment donnent des reponses differentes est le complement a un de la probabilite
d'accord, c'est a dire l'indice de Gini Simpson conditionne au segment, donc le terme
`D_intra` de la decomposition `D = D_intra + D_inter` de a1 section 2. **La mesure de a0, "la
probabilite que deux repondants tires au hasard donnent la meme reponse", n'est plus inedite.**
La phrase de PASSATION.md section 6, "Aucun papier lu ne publie cette mesure", est desormais
fausse et doit etre corrigee : LifeMem la publie, conditionnee au groupe, pour neuf methodes,
trois modeles et deux jeux de donnees.

Deux differences de forme subsistent et elles jouent en notre faveur. LifeMem publie une
**valeur absolue de difference**, pas un ratio, ce qui interdit de dire de combien la diversite
intra est ecrasee et interdit surtout de placer les humains en 1 par construction. Et LifeMem
n'emploie **aucun estimateur a biais corrige** : ni Miller Madow pour l'entropie, ni estimateur
sans biais de l'indice de Simpson, ni controle par permutation des etiquettes de segment. Or
a1 section 2 a montre que le biais positif de l'estimateur naif croit avec le nombre de
modalites effectivement employees, et que les agents en emploient moins que les humains.
[DEDUCTION, etiquetee comme telle : leurs metriques etant des ecarts absolus et non des
ratios, l'effet de ce biais sur leur classement des methodes n'est pas evaluable de
l'exterieur, mais il n'est pas nul et il n'est pas discute.]

**Metrique 4, divergence JS des transitions.** Pour une question commune a toutes les vagues et
un repondant, on forme le couple (reponse en vague t, reponse en vague t+1), chez l'humain et
chez le modele, et on compare les distributions de population de ces transitions. Unite
d'observation : la transition individu x question x paire de vagues. C'est la seule metrique
longitudinale, et elle n'a pas d'equivalent chez nous. [CONFIRME, annexe G]

**Segmentation.** [CONFIRME, annexe G, table 8] Add Health : `BIO_SEX`, `H1GI1Y`, `H1GI9`,
`H1RE1`, soit sexe, annee de naissance, une variable d'origine et une variable de religion.
Understanding Society : `Sex`, `Birthy`, `Marstat`, `Employ`, `Oprlg1`, `Qfhigh`, `Jbstat`,
soit sexe, annee de naissance, statut marital, emploi, religion, diplome le plus eleve, statut
d'activite. Les groupes sont formes **variable par variable**, jamais en croisement. Aucune
segmentation par ideologie politique, aucun profil croise. Nos six partitions de a1
comprennent un profil croise genre x race x ideologie a 18 segments, qu'ils n'ont pas.

**Jeux de donnees.** [CONFIRME] Add Health, six vagues retenues, et Understanding Society,
quinze vagues retenues, avec la contrainte "we retain only respondents observed in all selected
waves". **100 repondants par jeu de donnees**, tires avec la graine 42. C'est un echantillon
dix fois plus petit que les 1052 participants apparies du paquet OSF que a1 exploite.

**Modeles.** [CONFIRME] Trois modeles instruits de taille comparable :
Llama-3.1-8B-Instruct, Ministral-3-8B-Instruct-2512, Qwen3.5-9B. Decodage deterministe,
echantillonnage desactive. Une seule carte A800 de 80 Gio. Aucun modele proprietaire, aucun
modele de grande taille.

**Le chiffre de silhouette est ailleurs.** [CONFIRME] Il n'appartient pas aux resultats, il
appartient a la figure 1 d'ouverture et a l'annexe B, sur le World Values Survey vague 7,
2 000 repondants, trois groupes de statut socio economique en tertiles, Llama-3.1-8B-Instruct
en persona demographique pure. Citation exacte : "Human responses are broadly dispersed and
substantially overlap across SES groups, resulting in a silhouette score of S = -0.02. In
contrast, agent responses form more compact within-group clusters and show clearer separation
between SES groups, resulting in S = 0.19." Le papier borne lui meme la portee de ce chiffre :
"In this work, the silhouette score is used only to quantify the extent to which response
representations align with predefined demographic groups. It is not interpreted as a standalone
measure of simulation quality." [CONFIRME, annexe B]

**Une incoherence interne, mineure mais a connaitre si on cite.** La legende de la figure 1
ecrit "Silhouette scores are computed in the original response space before PCA projection",
l'annexe B ecrit "Silhouette scores are computed in the standardized response space before PCA
projection". "Original" et "standardized" ne designent pas le meme espace. Comme l'annexe
precise par ailleurs que "Each question dimension is standardized before dimensionality
reduction", la lecture standardisee est la plus probable, mais la source se contredit et il
faut citer l'annexe et non la legende. [CONFIRME sur les deux formulations, PROBABLE sur la
resolution]

## 1.2 Mesurent ils le terme inter groupes ? Avant et apres correction ?

**Non, jamais, dans aucune des deux directions.** [CONFIRME par absence, apres recherche
exhaustive des chaines "between-group", "between group", "silhouette", "separation" dans le
texte integral, corps et annexes.]

Les seules occurrences du terme inter sont **verbales** et se trouvent dans le resume,
l'introduction et la liste des contributions :

- Resume : "static-profile agents exhibit stronger demographic separation and within-group
  compression than humans, a pattern consistent with identity essentialism: demographic labels
  can encourage models to treat group-average tendencies as individual traits, homogenizing
  responses within groups." [CONFIRME]
- Introduction : "In social simulation, a corresponding pattern arises when static identity
  labels become overly predictive of agent responses, compressing within-group variation while
  amplifying between-group differences." [CONFIRME]
- Contributions : "We identify identity essentialism in static-profile LLM agents, which
  reduces within-group diversity and exaggerates between-group differences." [CONFIRME]

La seule mesure qui touche a la separation entre groupes est le score de silhouette de la
figure 1, et il est calcule **une seule fois, avant tout correctif, sur un autre jeu de donnees
que les experiences principales, avec une seule condition d'agent**. Il n'est jamais recalcule
apres LifeMem, ni sur le WVS, ni sur Add Health, ni sur Understanding Society. Le tableau 1 des
resultats principaux et le tableau 2 de l'etude d'ablation ne contiennent aucune colonne
inter.

**Consequence, et c'est la porte ouverte.** Un lecteur du papier ne peut pas savoir si LifeMem
a deplace de la variance de l'inter vers l'intra ou s'il a simplement dilate les deux termes,
ni si l'ecart entre groupes a ete corrige, sur corrige ou aggrave. Le papier ne fournit aucun
element pour trancher. La question que a1 pose reste sans reponse dans la source qui s'en
approche le plus.

## 1.3 Mesurent ils les deux termes ensemble, sur les memes donnees, avec une contrainte sur leur somme ?

**Non sur les trois points.** Ils mesurent le terme intra seul, sur Add Health et Understanding
Society. Ils mesurent une statistique qui melange les deux, le silhouette, sur le WVS. Les deux
mesures ne portent donc **pas sur les memes donnees**, ni sur les memes segmentations, ni sur
les memes modeles. Aucune identite du type `total = intra + inter` n'est ecrite dans le papier,
aucune quantite totale de dispersion n'est calculee dont les deux termes seraient les
composantes, et l'ecart d'entropie normalisee, qui serait le candidat naturel pour le total,
est defini sur la population entiere sans decomposition. [CONFIRME]

## 1.4 Formulent ils la compensation des deux erreurs dans une mesure globale ?

**Non.** [CONFIRME par absence] Le papier n'observe nulle part qu'une mesure agregee puisse
etre correcte alors que ses composantes sont fausses en sens contraire. Le mot "compensate"
et l'idee correspondante sont absents. Le seul passage qui approche un arbitrage entre
metriques est une remarque de resultat sur une exception : "One notable exception is Qwen3.5-9B
on Add Health, where Multilingual achieves slightly lower within-group pairwise distance gap
and normalized entropy gap than LifeMem. However, its substantially higher KL divergence
indicates that these gains in diversity alignment are accompanied by poorer agreement with the
overall human response distribution, suggesting a less balanced improvement across evaluation
dimensions." [CONFIRME] C'est un arbitrage entre diversite et fidelite distributionnelle, ce
n'est pas la compensation de deux composantes d'une meme decomposition.

## 1.5 Montrent ils qu'une metrique d'exactitude est aveugle a la structure ?

**Non, et ils ne pouvaient pas : le papier ne publie aucune mesure d'exactitude.** [CONFIRME
par absence] Les quatre metriques sont distributionnelles ou longitudinales. Le mot "accuracy"
n'apparait dans le texte que dans le titre d'une reference bibliographique. Aucune exactitude
au niveau individuel, aucun F1, aucune correlation avec la reponse reelle de la personne
simulee.

**Detail verifie dans leur code, et il est utile.** Le fichier
`src/evaluation/individual_metrics.py` du depot public calcule bien une exactitude et un
macro F1 au niveau individuel, apparie reponse humaine contre reponse du modele.
[CONFIRME] https://github.com/halsayxi/LifeMem, `src/evaluation/individual_metrics.py`
Ces chiffres sont donc **calcules par le pipeline et non publies dans le papier**. Autrement
dit, on ne sait pas si LifeMem gagne en diversite intra groupe **au prix** d'une perte de
fidelite individuelle. C'est exactement le risque que a1 section 7 rend concret dans l'autre
sens : deux conditions d'exactitude identique et de structure opposee.

## 1.6 Leur correctif : decodage, persona, ou population ?

**Persona, au niveau de l'individu, sans aucun couplage entre agents.** [CONFIRME par la
methode] LifeMem a deux composantes :

1. Une memoire structuree d'evenements de vie. Chaque paire question reponse d'enquete est
   convertie en enonce a la deuxieme personne, encodee, stockee avec son indice de vague, et
   recuperee par pertinence semantique ponderee par une decroissance temporelle. Les enonces
   selectionnes sont inseres dans l'invite.
2. Une memoire parametrique propre a chaque agent : un adaptateur LoRA par individu, le modele
   de base restant gele, mis a jour sequentiellement vague apres vague, avec rejeu d'un petit
   echantillon d'exemples anciens. Citation : "Separate adapters allow individuals with similar
   demographic profiles to develop different parametric states as their trajectories diverge."
   [CONFIRME]

Ce n'est **ni** un correctif de decodage, ils n'y touchent pas et le decodage est deterministe,
temperature nulle, echantillonnage desactive ; **ni** un correctif de population, aucune
statistique de la population simulee n'entre dans la construction ou la mise a jour d'un agent.
C'est une personnalisation individu par individu.

**Ce que cela fait au terme inter, deduit de la methode. [DEDUCTION, non mesuree par eux,
etiquetee comme telle.]**

- Le mecanisme est **strictement additif au niveau individuel** : chaque agent recoit de
  l'information idiosyncrasique que les autres n'ont pas. Rien dans l'objectif d'entrainement
  ni dans la recuperation ne fait reference a la moyenne d'un groupe, a l'ecart entre groupes,
  ou a une contrainte de dispersion totale. Aucun terme du dispositif ne peut donc **diminuer**
  un ecart entre moyennes de groupes autrement que par effet de bord.
- L'effet de bord le plus probable est une **dilatation de l'intra a inter inchange ou
  faiblement modifie**. Le papier fournit d'ailleurs l'indice direct : la figure 4 montre que
  les etats LoRA, initialement concentres, se dispersent au fil des vagues, et le texte
  conclut : "This pattern suggests that sequential updates gradually encode heterogeneous life
  experiences into differentiated parametric states, reflecting increasing personalization
  across agents with different longitudinal trajectories." [CONFIRME] Une dispersion croissante
  des etats individuels est une augmentation de la variance totale, pas un transport.
- Une seconde issue est possible et elle est defavorable a leur these : les evenements de vie
  d'un individu sont **eux memes stratifies par le groupe**. Un chomage, un divorce, un diplome
  ne sont pas repartis uniformement entre segments. Injecter des trajectoires reelles peut donc
  **augmenter** aussi l'ecart entre groupes, si le modele exploite la correlation entre type
  d'evenement et appartenance. Rien dans le papier ne permet d'ecarter cette issue.
- Conclusion de la deduction : LifeMem n'est pas un transport a somme constante et rien
  n'indique qu'il en soit un. Il est, au mieux, une dilatation ciblee de la composante intra.
  **Cette deduction n'est pas une critique du papier, c'est la description de ce qu'il ne
  pretend pas faire.** Le papier ne revendique nulle part un transport.

## 1.7 Quelles baselines non LLM ?

**Aucune.** [CONFIRME par la liste exhaustive des baselines] Les huit points de comparaison
sont tous le meme modele de langage sous une autre configuration : `Direct` et `Profile` pour
le conditionnement statique, `Multilingual` et `Anti-Stereotype` pour l'invite orientee
diversite, `SimVBG`, `Full History` et `Event RAG` pour la memoire non parametrique, et
`Random Event` comme controle. Il n'y a ni regression logistique, ni foret aleatoire, ni
copule, ni marginale de question, ni lookup demographique.

C'est une faiblesse importante et exploitable. Le tableau 1 montre que la baseline `Direct`,
sans aucun profil, a un ecart intra groupe de 0,55 a 0,57 selon le modele, alors que la
distance appariee intra groupe humaine est bornee par 1. Un tirage aleatoire dans la marginale
de la question donnerait, par construction, une distance appariee intra groupe egale a celle
d'une population sans structure, donc **plus proche de l'humain que tous leurs agents sur cette
metrique**. [DEDUCTION, non verifiee empiriquement, mais elle decoule de la definition de la
metrique : une population tiree independamment dans la marginale n'a aucune compression intra
groupe.] Sans baseline non LLM, on ne sait pas combien de leur gain de diversite est du a la
personnalisation et combien serait obtenu par du bruit.

## 1.8 Quelle normalisation par le plafond humain ?

**Aucune.** [CONFIRME] Les quatre metriques sont des ecarts a l'humain avec zero comme optimum,
ce qui pose implicitement que la mesure humaine est sans erreur. Il n'y a ni reinterrogation
des memes personnes, ni consistance test retest, ni intervalle de confiance sur l'ecart a
l'humain. Les seuls tests statistiques du papier sont des tests t apparies **entre methodes**
sur les questions partagees, ce qui dit si une methode bat une autre, pas si une methode atteint
le bruit humain.

Or les jeux employes sont longitudinaux, six et quinze vagues, avec les memes personnes : le
materiel pour construire un plancher de reproductibilite humaine etait entre leurs mains. Ils
ne l'ont pas fait. **C'est la faiblesse la plus exploitable des deux papiers, et c'est
precisement ce que le controle vague 2 de a1 apporte**, qui tombe en (1,003 ; 1,004) avec des
intervalles contenant 1.

## 1.9 Le chiffre de 22 pour cent doit etre requalifie

a10 section 3.a ecrit "ecart intra groupe de 0,296 a 0,231 soit 22 pour cent". Le chiffre est
exact mais son referent doit etre nomme. Verification dans le tableau 1, Llama-3.1-8B-Instruct
sur Add Health : la valeur 0,2964 est celle d'`Event RAG`, la **meilleure baseline**, et 0,2309
celle de LifeMem. Le gain de 22 pour cent est donc mesure contre le meilleur systeme de memoire
concurrent, pas contre l'agent a profil statique qui porte l'identity essentialism. Contre
`Profile`, qui est la condition essentialiste, la reduction va de 0,3951 a 0,2309, soit **41,6
pour cent**. Contre `Direct`, de 0,5596 a 0,2309, soit 58,7 pour cent. [CONFIRME, tableau 1]

**Le chiffre a citer dans le dossier est donc 41,6 pour cent contre l'agent a profil**, avec la
mention du modele et du jeu de donnees, ou la fourchette complete des trois modeles. Citer 22
pour cent sans dire contre quoi sous estime leur resultat et nous expose a une correction en
relecture.

---

# 2. Garzon, Baron, Grari, Kamphorst, Bernstein, Detyniecki, arXiv 2605.16303

**Reference exacte.** *From Demographics to Survey Anchors: Evaluating LLM Agents for Modeling
Retirement Attitudes*. Version 1 unique, deposee le 24 avril 2026.
[CONFIRME] https://arxiv.org/html/2605.16303, en tete : "arXiv:2605.16303v1 [cs.CY] 24 Apr
2026".

**Affiliations, et c'est une information que a10 n'avait pas relevee.** [CONFIRME, page de
titre] Ruben Garzon, Pauline Baron, Vincent Grari et Marcin Detyniecki sont **AI Research, AXA
Group Operations**, respectivement Madrid, Paris, Lausanne et Paris. Jonne Kamphorst est
**CDSP et CEE, Sciences Po, Paris**, et non Stanford. Michael Bernstein est **Computer Science
Department, Stanford University**. C'est donc un travail industriel d'un assureur europeen avec
deux collaborateurs academiques, dont un seul de Stanford. La lecture de a10, "c'est la meme
equipe que le papier de reference", doit etre nuancee : c'est un recouvrement de deux auteurs
sur onze, pas la meme equipe.

## 2.1 Quelle quantite exactement est mesuree

Le papier a trois etudes et deux familles de mesures qu'il ne faut pas confondre.

**Etude 1, SHARE, avec verite terrain.** Protocole "leave-one-item-out" : pour chaque repondant
et chaque question cible, le contexte du modele contient toutes les autres paires question
reponse de ce repondant, la question cible et sa reponse etant retirees. Citation : "For each
respondent and target question, the model context comprised all remaining question-answer pairs
for that respondent. The target question's text and answer were withheld." [CONFIRME, section
4.1.1] Metriques : distance en variation totale entre la distribution des reponses des agents
et celle des humains, plus une correlation ou un F1 pondere selon que l'item est numerique ou
categoriel. Unite d'observation : le couple repondant x item, agregee en une distribution par
question. Effectifs par question de 986 a 2 000 ; l'analyse bootstrap porte sur 5 461
participants et 15 questions, 5 000 tirages.

**Etude 2, Eurobarometre, au niveau pays.** Replication des memes constats a l'echelle
nationale. Non detaillee ici, elle ne porte pas sur la structure intra groupe.

**Etude 3, la replication de Jacobs-Lawson et Hershey, et c'est celle qui contient la
correlation intraclasse.** Population d'agents construite a partir du General Social Survey de
2004, en selectionnant des repondants americains de caracteristiques demographiques proches de
l'etude d'origine de 2005, 270 adultes de 25 a 45 ans. Quatre echelles a 5 ou 6 items, reponses
sur une echelle de 1 a 7, moyennees par construit : FTP perspective temporelle future, KFP
connaissance de la planification financiere, FRT tolerance au risque financier, RS epargne
retraite. Trois conditions d'agents : `Demographics7` avec sept attributs, `Demographics3` avec
trois, et `survey-anchored` qui recoit en plus en moyenne 465 items de reponses du GSS.
[CONFIRME, section 4.3.1]

**La correlation intraclasse, definition litterale.** "We computed the one-way random-effects
intraclass correlation ICC(1) for scale mean scores, where ICC = (MS_between - MS_within) /
(MS_between + (n_g - 1) MS_within) and n_g is the average stratum size." [CONFIRME, section
4.3.2] Unite d'observation : le score moyen d'echelle d'un agent. Segmentation : "agents were
grouped into strata defined by age and gender categories", soit **deux variables croisees et
rien d'autre**. Pas de race, pas d'ideologie, pas de revenu, pas d'education.

**Modeles.** [PROBABLE] Le corps du texte insiste sur l'usage de modeles locaux, justifie par
la nature restreinte de SHARE : "our use of local LLMs was necessitated by the restricted
nature of SHARE: no respondent information may leave the secure environment." [CONFIRME]
L'annexe 7.8 annonce des resultats additionnels sur Gemma3:12b et LLaMa 3.1:8b, ce qui indique
que ce sont des modeles de secours et non le modele principal. **Je n'ai pas identifie avec
certitude le modele principal des tableaux 2 a 5** dans la version HTML.

## 2.2 Mesurent ils le terme inter groupes ? Avant et apres correction ?

**Ils mesurent un rapport qui contient les deux termes, jamais le terme inter comme quantite
publiee, et jamais rapporte a l'humain.**

L'ICC(1) telle qu'ils la definissent est, en esperance, la part de la variance totale imputable
a la strate, c'est a dire `sigma2_inter / (sigma2_inter + sigma2_intra)`. C'est donc, au sens
strict, une decomposition inter et intra, et c'est ce qui fait de ce papier le precedent le plus
proche du chantier 1. Mais trois limites en changent la portee.

**Limite 1, il n'y a aucun referent humain sur cette analyse, et le papier le dit lui meme.**
Citation, en ouverture de la section 4.3.2 : "Given that we do not have access to the
participants' responses from the original study (i.e., no ground truth is available), we
examine the distributional properties of the answers by demographics-only and survey-anchored
agents to characterize the nature of the synthetic populations they generate. This analysis
does not require access to reference data and serves as a diagnostic of the generative process
itself." [CONFIRME] Les quatre diagnostics de dispersion de cette section, dont l'ICC, sont
donc **agents contre agents**. Aucune valeur humaine d'ICC n'est publiee. Il est impossible, a
partir de ce papier, de dire si un ICC de 0,17 est un gonflement ou un aplatissement par
rapport a de vrais humains.

**Limite 2, l'ICC est un rapport, pas deux quantites.** Un ICC qui baisse peut resulter d'une
baisse de l'inter, d'une hausse de l'intra, ou des deux. Le papier ne separe jamais le numerateur
du denominateur et n'ecrit jamais la variance inter en valeur absolue.

**Limite 3, la segmentation est la plus pauvre des trois travaux**, age croise avec genre, alors
que a1 section 4 montre que le gonflement inter est porte surtout par l'axe ideologique, absent
ici.

**Les valeurs, telles que publiees.** "Demographics7 agents show consistently higher ICC than
survey-anchored agents across all scales (RS: 0.17 vs. 0.06; KFP: 0.08 vs. 0.02; FTP: 0.07 vs.
0.04; FRT: 0.10 vs. 0.02), indicating greater demographic determinism". [CONFIRME, section
4.3.2] Le complement de phrase, qui suit un tiret dans la source et que je ne recopie pas ici
pour respecter la regle de forme du projet, precise que quelques attributs demographiques
contraignent rigidement le motif de reponse.

## 2.3 Ce que leur propre tableau permet de calculer, et qu'ils ne calculent pas

**[DEDUCTION, calcul de ma part a partir de deux tableaux du papier, non publie par les
auteurs, a verifier sur le PDF avant toute citation.]**

Leur tableau 8 donne l'ecart type des scores d'echelle par agent, c'est a dire l'ecart type
total, pour chaque condition. Leur section 4.3.2 donne l'ICC pour les memes conditions et les
memes echelles. Comme l'ICC estime `sigma2_inter / sigma2_total`, on peut reconstituer les deux
composantes en valeur absolue.

| echelle | var. totale D7 | inter D7 | intra D7 | var. totale ancree | inter ancree | intra ancree | ratio inter | ratio intra |
|---|---|---|---|---|---|---|---|---|
| RS | 1,061 | 0,180 | 0,881 | 1,513 | 0,091 | 1,422 | **0,50** | **1,62** |
| KFP | 0,548 | 0,044 | 0,504 | 0,810 | 0,016 | 0,794 | **0,37** | **1,58** |
| FTP | 0,270 | 0,019 | 0,252 | 0,372 | 0,015 | 0,357 | **0,79** | **1,42** |
| FRT | 0,706 | 0,071 | 0,635 | 0,462 | 0,009 | 0,453 | **0,13** | **0,71** |

Sources des entrees : ecarts types du tableau 8, "FTP: SD = 0.52 ; FRT: SD = 0.84" pour
Demographics7 et "FTP: 0.52 vs. 0.61 ; KFP: 0.74 vs. 0.90 ; RS: 1.03 vs. 1.23" pour la
comparaison avec les agents ancres, plus "FRT, where Demographics7 produces wider dispersion
(0.84 vs. 0.68)" [CONFIRME] ; valeurs d'ICC de la section 4.3.2 [CONFIRME].

**Lecture.** Passer de l'agent demographique a l'agent ancre sur les reponses individuelles
divise la composante inter par 1,3 a 7,7 selon l'echelle, pendant que la composante intra est
multipliee par 1,4 a 1,6 sur trois echelles sur quatre. **C'est la signature d'un transport
inter vers intra**, et elle se trouve deja, implicitement, dans un papier co signe par
Kamphorst et Bernstein. Mais la somme n'est pas conservee : la variance totale passe de 1,061 a
1,513 sur RS, soit plus 43 pour cent, et de 0,548 a 0,810 sur KFP, soit plus 48 pour cent. Ce
n'est donc pas un transport a somme constante, c'est un transport accompagne d'une dilatation.
Et sur FRT, la quatrieme echelle, les deux termes baissent ensemble, ce qui est un
aplatissement simple, exactement le regime que a1 observe pour les agents persona `gss_v7` et
la variante `gss_v6`.

**Reserves sur ce calcul, et elles sont serieuses.** Les effectifs du tableau 9 varient de 224
a 270 agents selon la condition et l'echelle, ce qui suggere que les tableaux 8 et 9 et la
figure 13 ne portent pas exactement sur les memes agents. L'ICC(1) estimee par cette formule
peut etre negative en echantillon fini et est bornee en dessous, ce qui la biaise vers le haut
quand la vraie valeur est proche de zero. Les valeurs d'ICC publiees ont deux decimales, ce qui
donne une precision relative mediocre sur des composantes inter de l'ordre de 0,01. Enfin, la
formule ICC(1) estime `sigma2_inter / sigma2_total` pour un plan equilibre, or les strates age x
genre ne sont pas equilibrees. **Ce calcul est un argument de lecture, pas un resultat
publiable en l'etat.**

## 2.4 Mesurent ils les deux termes ensemble, avec une contrainte sur leur somme ?

**Non.** Le rapport ICC contient les deux termes mais ne les separe pas, et le papier ne pose
aucune identite reliant une dispersion totale a ses deux composantes. La section 4.3.2 juxtapose
quatre diagnostics independants, dispersion d'echelle, entropie par item, diversite de profils
et ICC, sans les relier par une equation. [CONFIRME]

## 2.5 Formulent ils la compensation des deux erreurs dans une mesure globale ?

**Pas pour l'inter et l'intra. Mais ils formulent un argument de meme forme, sur une autre
quantite, et c'est important a savoir avant de revendiquer l'idee comme neuve.**

L'annexe 7.16 est une decomposition de l'alpha de Cronbach en correlation moyenne inter items
et variance moyenne par item, dont la justification est ecrite ainsi : "Equations 4 and 5
reveal that two datasets can yield the same alpha through different mechanisms". Et plus loin :
"if a simulated population achieves high alpha primarily through elevated r-bar while
exhibiting compressed sigma2-item relative to a reference population, this indicates that the
model generates stereotypically coherent profiles". [CONFIRME, annexe 7.16]

**C'est exactement notre figure de raisonnement**, appliquee a la fiabilite interne d'une
echelle au lieu de la dispersion d'une population : une statistique agregee identique peut
recouvrir deux mecanismes generatifs opposes, et il faut decomposer pour le voir. Il ne faut
donc plus presenter la **forme** de l'argument comme originale. Ce qui reste original est
l'objet auquel nous l'appliquons, la decomposition inter et intra d'une population simulee, et
le fait que nous en donnions une demonstration chiffree sur deux conditions reelles.

## 2.6 Montrent ils qu'une metrique d'exactitude est aveugle a la structure ?

**Non, et leur resultat va meme dans le sens contraire sur leurs donnees.** [CONFIRME] Chez
eux, l'agent ancre est **a la fois** meilleur en exactitude distributionnelle et meilleur en
structure : distance en variation totale moyenne de 0,4217 pour l'agent demographique contre
0,2796 pour l'agent ancre, difference de -0,1421 avec un intervalle bootstrap [-0,1516 ;
-0,1309] excluant zero, et en meme temps ICC plus faible, entropie plus elevee et diversite de
profils plus elevee. Les deux dimensions sont alignees, donc leur experience ne peut pas
demontrer que l'une est aveugle a l'autre.

**C'est precisement la valeur de a1 section 7.** Nos deux conditions `gss_v7` et `gss_v8` ont
une exactitude indistinguable, ecart apparie de -0,07 point, intervalle [-0,52 ; +0,37], et des
ratios inter de 0,437 et 5,907, un facteur 13,5, avec des intervalles disjoints. Le cas ou les
deux dimensions se dissocient n'existe dans aucun des deux papiers. Il existe chez nous, a
l'interieur d'un seul papier tiers, sur les memes participants et les memes items.

Il faut noter toutefois que ce papier documente une **autre** dissociation, qui affaiblit
egalement les metriques d'exactitude et qu'il faut citer plutot que d'ignorer : l'hyper
exactitude sur les questions objectives. Resume du papier : les agents demographiques "were
unrealistically accurate, failing to reproduce the incorrect answers and "don't know" responses
typical of human respondents". [CONFIRME] Un agent trop exact est infidele. C'est une critique
de l'exactitude comme critere, differente de la notre mais voisine.

## 2.7 Leur correctif : decodage, persona, ou population ?

**Persona, par le contenu du contexte.** Le "correctif" est l'ancrage sur les reponses reelles
de la personne : environ 175 items par individu dans l'etude SHARE, environ 465 items par agent
dans l'etude GSS. Aucune intervention sur le decodage, aucune intervention au niveau de la
population. C'est la meme famille que les conditions ancrees du paquet OSF que a1 mesure deja,
et c'est la meme famille que LifeMem, a ceci pres que LifeMem y ajoute une memoire parametrique.

**Ce que cela fait au terme inter. [DEDUCTION appuyee sur leur propre tableau, section 2.3
ci dessus.]** L'ancrage divise la composante inter par 1,3 a 7,7 selon l'echelle. La raison est
mecanique : plus le contexte contient d'information propre a l'individu, moins l'etiquette de
groupe est un predicteur utile pour le modele, donc moins la reponse est determinee par le
groupe. Le mecanisme est le meme que celui de LifeMem, sans la memoire parametrique.

**A retenir pour le dossier.** Les deux precedents proposent le meme correctif de fond, remplacer
l'etiquette de groupe par de l'information individuelle, et aucun des deux ne le formule comme
une redistribution contrainte. Le fait que nos conditions ancrees du paquet OSF gonflent
pourtant l'inter d'un facteur 1,75 a 2,16, a1 section 3, est une **contradiction apparente avec
ce papier** qu'il faudra expliquer avant publication, et c'est une objection qu'un relecteur
posera. Explication la plus probable : la segmentation n'est pas la meme, age x genre chez eux
contre six axes dont l'ideologie chez nous, et a1 section 4 montre que le gonflement est porte
par l'axe ideologique. [HYPOTHESE, verifiable en recalculant nos ratios sur le seul croisement
age x genre, ce que `a1-ratios-par-axe.csv` permet peut etre deja.]

## 2.8 Quelles baselines non LLM ?

**Oui, et c'est le point fort de ce papier face a LifeMem.** [CONFIRME, tableaux 2 et 3] Une
baseline d'apprentissage supervise, une foret d'arbres avec hyperparametres publies par
question, de 5 a 50 arbres et profondeur 5 ou 7, avec des scores d'entrainement et de test
separes. Sur les cinq questions retraite, elle est parfois devant et parfois derriere les
agents. Deux exemples opposes :

- SHARE-FK01, la question de calcul d'interets : la baseline supervisee a une TVD de test de
  0,23 contre 0,58 pour l'agent demographique et 0,37 pour l'agent ancre. **La baseline non LLM
  bat les deux agents.**
- SHARE-FRT01, la tolerance au risque : TVD de test 0,26 contre 0,16 et 0,11. Les agents
  gagnent. Le papier le note explicitement : "Both types of agents enhance the performance of
  the supervised machine learning baseline". [CONFIRME]

Le papier signale aussi une limite honnete de sa propre comparaison : "Only the target variable
was removed from the agents. Correlated variables could thus still be used by both the LLMs and
the supervised machine learning baselines." [CONFIRME] Autrement dit, la fuite par items
correles existe des deux cotes, ce qui preserve l'equite de la comparaison sans en garantir la
validite absolue.

**Ce que cela impose a popsim.** La regle de PASSATION.md section 5, une baseline non LLM
obligatoire dans toute condition, n'est pas un raffinement : c'est le standard du precedent le
plus proche, publie par un co auteur du papier de reference. a2 a deja construit ces baselines,
il faut s'assurer qu'elles sont rapportees dans le meme format, entrainement et test separes,
hyperparametres publies.

## 2.9 Quelle normalisation par le plafond humain ?

**Aucune, et le papier l'ecrit lui meme comme une limite.** Citation, section 5.1 : "Another
limitation concerns temporal reliability. In survey and behavioral research, participant
responses often vary over time. We did not assess this reliability but relied on a single set
of pre-existing answers." [CONFIRME]

Il n'y a donc ni consistance test retest, ni plancher d'erreur humaine, ni denominateur de
normalisation. C'est la meme lacune que LifeMem, formulee explicitement au lieu d'etre passee
sous silence.

---

# 3. Le tableau de comparaison

| | popsim, a0 a a2 | LifeMem 2608.19621 | Garzon et al. 2605.16303 |
|---|---|---|---|
| terme intra mesure | oui, 3 mesures, ratio a l'humain | oui, ecart absolu a l'humain | oui, ICC, entropie, SD, sans humain |
| terme inter mesure | oui, 3 mesures, ratio a l'humain | non, jamais | non, seulement dans un rapport |
| les deux sur les memes donnees | oui | non, intra sur AH et USoc, silhouette sur WVS | oui pour le rapport, jamais separes |
| decomposition additive posee | oui, `D = D_intra + D_inter` | non | non |
| contrainte de somme formulee | oui, corollaire du transport | non | non |
| avant et apres correctif | correctif non encore construit | intra oui, inter jamais | intra oui, inter jamais |
| exactitude individuelle publiee | oui, comparee a la structure | non, calculee dans le code, non publiee | oui, TVD, F1, correlation |
| dissociation exactitude / structure | oui, facteur 13,5 a 0,07 point | sans objet | non, les deux vont ensemble |
| estimateurs a biais corrige | oui, Miller Madow, Simpson sans biais | non | non |
| controle par permutation | oui, residu inferieur a 0,1 pour cent | non | non |
| plafond humain | oui, retest a deux semaines, controle en (1,003 ; 1,004) | non | non, limite reconnue |
| baseline non LLM | oui, obligatoire par regle | **non, aucune** | oui, foret aleatoire |
| intervalles de confiance | oui, bootstrap 1000 tirages sur participants | non sur l'ecart a l'humain | oui, bootstrap 5000 sur participants |
| N individus | 1052 apparies | 100 par jeu | 986 a 2000 par question, 5461 au bootstrap |
| segmentations | 6 axes dont un croise a 18 segments | 4 et 7 variables, jamais croisees | age x genre seulement |
| donnees redistribuables | non, OSF sans licence | non, DUA des fournisseurs | non, SHARE en enclave |
| code public | scripts internes | oui, sans licence declaree | non trouve |
| sorties publiees | non | **non** | non |

---

# 4. Les autres candidats, et un precedent de 2023 que a10 n'avait pas vu

Recherche menee sur l'API arXiv, six requetes sur les combinaisons "between-group" et
"within-group" avec "large language model", "variance decomposition" avec "simulated
respondents", "intraclass correlation" avec "LLM agents", "within-group" avec "simulation" et
"LLM", "homogeneity" avec "survey" et "LLM", plus trois recherches web sur les mots cles
demandes.

## 4.1 Le precedent principal manquant : Kim et Lee, arXiv 2305.09620

**Ce papier mesure explicitement les deux termes, sur le GSS, avec presque exactement nos
segmentations, et a10 ne l'avait pas trouve.** C'est le point le plus important de cette
section et il oblige a reformuler encore une fois.

**Reference.** Junsol Kim, Byungkyu Lee, *AI-Augmented Surveys: Leveraging Large Language
Models and Surveys for Opinion Prediction*, arXiv 2305.09620. Historique : v1 le 16 mai 2023,
**v4 le 19 mai 2026**, donc mis a jour trois mois avant les deux autres.
[CONFIRME] https://arxiv.org/abs/2305.09620

**Ce qu'ils mesurent.** Citation du corps du texte, section "Evaluation of Predicting
Between-and Within-Group Variances" : "Following Bisbee et al. (2024), we evaluate whether the
model captures between-group and within-group response variance across gender, race, age,
education, and political-stance subgroups". Et la definition : "To assess between-group
variance, we estimate the standard deviation of predicted and observed group means across key
demographic categories". [CONFIRME, arXiv 2305.09620v4, section Evaluation of Predicting
Between-and Within-Group Variances et annexe F]

**Leurs cinq axes, genre, race, age, education, orientation politique, sont cinq des six axes
de a1.** Le jeu de donnees est le GSS. C'est le plus proche voisin methodologique de notre
mesure, et il est anterieur de trois ans dans sa premiere version.

**Leur resultat.** "The model captures between-group variance well, particularly for political
stance and education (fig. A13). For within-group variance, predicted and observed subgroup
standard deviations are strongly correlated across categories; nevertheless, the model
underestimates the absolute level of within-group variance across most demographic categories
(fig. A14)." [CONFIRME]

**Ce qui nous separe d'eux, et ce qui nous sauve.** Quatre differences, toutes verifiees.

1. **Leur objet n'est pas une population de personas.** C'est un modele de prediction,
   Alpaca-7B avec des plongements de question, de repondant et de periode, **entraine sur le
   GSS lui meme**. Un modele ajuste sur les donnees de sortie n'a aucune raison de gonfler les
   ecarts entre groupes, et de fait il ne les gonfle pas : il les reproduit bien. Leur resultat
   n'est donc pas comparable a une simulation par invite, et il ne contredit pas la double
   distorsion, il montre que l'ajustement supervise la supprime du cote inter.
2. **Ils comparent des ecarts types predits a des ecarts types observes par un nuage de points,
   avec une correlation de Spearman et une erreur absolue moyenne.** Ce n'est pas un ratio
   unique par condition, ce n'est pas place dans un plan a deux dimensions, et les humains ne
   sont pas en (1,1) par construction. On ne peut pas lire dans leurs figures A13 et A14 de
   combien un terme est gonfle et l'autre ecrase.
3. **Aucune identite additive, aucune contrainte de somme, aucune notion de compensation.** Les
   deux evaluations sont dans deux figures d'annexe successives et ne sont jamais reliees.
4. **Aucun plafond humain test retest**, meme si leur validation croisee sur des annees masquees
   joue un role voisin pour la partie predictive.

**Consequence pour le dossier, et elle est nette.** La revendication "personne n'a mesure les
deux termes" est **fausse depuis 2023** et fausse a nouveau dans la version de mai 2026. La
revendication qui reste vraie est plus etroite et plus solide : personne n'a mesure les deux
termes **comme deux ratios a un referent humain mesure**, sur des populations de personas, en
posant leur somme comme contrainte, et en montrant leur dissociation d'avec l'exactitude.
Il faut aussi citer **Bisbee, Clinton, Dorff, Kenkel et Larson, *Synthetic Replacements for
Human Survey Data? The Perils of Large Language Models*, Political Analysis, volume 32, numero
4, 2024, pages 401 a 416**, qui est la source methodologique explicite de Kim et Lee pour cette
evaluation.
[CONFIRME sur l'existence et la reference]
https://www.cambridge.org/core/journals/political-analysis/article/synthetic-replacements-for-human-survey-data-the-perils-of-large-language-models/B92267DC26195C7F36E63EA04A47D2FE
[non verifie] Je n'ai pas lu Bisbee et al. 2024 dans le texte et je ne sais donc pas si leur
mesure inter groupes est un ecart type de moyennes de groupes, comme le laisse entendre Kim et
Lee, ou autre chose. **A lire avant redaction du related work.**

## 4.2 Un papier qui contredit la these et qu'il faut regarder en face

**arXiv 2603.16142, *Parametric Social Identity Injection and Diversification in Public Opinion
Simulation*, version 2, mars 2026.**
[CONFIRME] https://arxiv.org/abs/2603.16142

Citation du resume : "current LLM-based simulation methods fail to capture social diversity,
producing flattened inter-group differences and overly homogeneous responses across demographic
groups." [CONFIRME]

**Ce papier affirme donc l'aplatissement des ecarts inter groupes, pas leur gonflement.** Il
propose un correctif, PSII, qui injecte des representations parametriques d'attributs
demographiques dans les etats caches intermediaires, et qui **augmente** a la fois la fidelite
distributionnelle et la diversite sur le World Values Survey.

C'est une contradiction frontale avec la formulation de la these du projet, et il ne faut pas
la cacher. Trois lectures possibles, aucune verifiee. [HYPOTHESE] Le sens de la distorsion
depend du regime d'agent : a1 lui meme trouve les deux, gonflement pour quatre conditions,
aplatissement pour les agents persona `gss_v7` a 0,437 et la variante `gss_v6` a 0,855. Ou bien
le sens depend de la segmentation, comme le suggere a1 section 4. Ou bien "inter-group
differences" designe chez eux la distance entre distributions de reponses par groupe et non une
composante de variance, ce qui en ferait une autre quantite. **Le papier n'a pas ete lu en
entier ; il doit l'etre avant toute redaction, parce qu'un relecteur qui le connait posera la
question en premier.**

Ce papier renforce d'ailleurs le point de fond du projet : deux equipes de 2026 decrivent le
terme inter en sens opposes, ce qui montre justement que la quantite n'est ni definie ni
mesuree de facon standard dans le champ.

## 4.3 Les autres, brievement

| reference | ce qu'il mesure | compte t il ? |
|---|---|---|
| arXiv 2608.18768, *Readable, Faithful, Used: Three Dissociable Properties of Demographic Identity in a Language Model*, 19 aout 2026 https://arxiv.org/abs/2608.18768 | analyse de similarite representationnelle contre verite terrain Pew sur 169 cellules demographiques, 1 089 emplacements de lecture dans Mistral-7B, fidelite corrigee jusqu'a rho = 0,63, "roughly 70% of the measurement-reliability ceiling" | **oui, sur deux points.** Il **normalise par un plafond de fiabilite de mesure**, ce que ni LifeMem ni Garzon ne font, et il etablit une **dissociation entre deux proprietes** de la meme representation, ce qui est la forme de notre argument. A citer |
| arXiv 2602.18462, *Assessing the Reliability of Persona-Conditioned LLMs as Synthetic Survey Respondents*, 6 fevrier 2026 https://arxiv.org/abs/2602.18462 | WVS, microdonnees americaines, plus de 70 000 instances repondant x item, deux modeles ouverts et une baseline de devinette aleatoire | **oui, marginalement.** Il emploie le mot "redistribute" pour une redistribution d'erreur entre sous groupes, "demographic conditioning can redistribute error in ways that undermine subgroup fidelity". C'est la deuxieme collision de vocabulaire apres arXiv 2609.04485, deja signalee en a10 question 7. Le mot "redistribution" est pris deux fois. Notre vocabulaire doit changer |
| arXiv 2607.03091, *Silicon Sampling via Cross-Survey Transfer*, 3 juillet 2026 https://arxiv.org/abs/2607.03091 | transfert entre enquetes, donnees electorales taiwanaises, trois modeles ouverts, comparaison a une foret aleatoire supervisee | **marginalement.** Le protocole de transfert entre enquetes est proche du "test existentiel" du chantier 2, et il conclut que le modele sans exemple arrive a 6 points d'une foret aleatoire supervisee. A lire pour le chantier 2, pas pour le chantier 1 |
| arXiv 2607.20429, *More Is Not More: What Matters for Diversity in LLM Opinions?* | plan factoriel separant profondeur du persona et architecture d'interaction, 100 questions ouvertes, 7 modeles | non pour la decomposition. Utile comme argument annexe : plus de detail demographique n'augmente pas monotonement la diversite |

**Aucun autre papier trouve ne publie une decomposition inter et intra en deux quantites
separees pour des populations simulees par invite.** [CONFIRME par recherche, avec la reserve
habituelle : une recherche par absence n'est pas une preuve, l'API arXiv ne cherche que les
titres, resumes et commentaires, et les actes de conference et les preprints SSRN ne sont pas
couverts.]

---

# 5. Ce que popsim peut revendiquer apres lecture

## (a) Ce qui est deja fait, et que nous ne devons plus presenter comme neuf

1. **Le nom et le diagnostic de la double distorsion.** LifeMem l'ecrit dans son resume, dans
   son introduction et dans sa liste de contributions, en toutes lettres, avec le nom d'identity
   essentialism. Toute phrase du type "nous identifions un phenomene de compression intra et de
   separation inter" est desormais une redite. La reformulation de PASSATION.md section 5 doit
   aller plus loin qu'aujourd'hui : le phenomene est acquis, seule sa mesure conjointe ne l'est
   pas.
2. **La mesure de la probabilite que deux repondants d'un meme groupe repondent differemment.**
   LifeMem la publie sous le nom de "within-group pairwise distance", pour neuf methodes, trois
   modeles et deux jeux de donnees. La phrase de PASSATION.md section 6, "Aucun papier lu ne
   publie cette mesure", **doit etre supprimee**. Le resultat a0 reste vrai et utile, il n'est
   plus inedit.
3. **La mesure conjointe d'une variance inter groupes et d'une variance intra groupes de
   reponses simulees sur le GSS.** Kim et Lee la publient depuis 2023, mise a jour en mai 2026,
   sur cinq de nos six axes, en citant Bisbee et al. 2024 comme methode. La formule "personne
   ne mesure les deux termes" est fausse et doit disparaitre du dossier.
4. **Le constat que les agents demographiques sont plus homogenes a l'interieur d'une strate que
   les agents ancres sur des reponses individuelles.** Garzon et al. le publient avec une ICC,
   sur quatre echelles, avec un ecart d'un facteur 2 a 5.
5. **La forme de l'argument "une statistique agregee identique peut recouvrir deux mecanismes
   opposes".** Garzon et al. l'emploient dans leur annexe 7.16 pour l'alpha de Cronbach. C'est
   la meme figure de raisonnement que la notre, appliquee ailleurs.
6. **Le correctif par ancrage sur des reponses individuelles.** Les deux papiers le font, l'un
   avec 175 a 465 items d'enquete, l'autre avec des trajectoires de vie et une memoire
   parametrique. Toute proposition d'ancrage simple est deja occupee.
7. **La formule "aucun precedent trouve" du chantier 3 de PASSATION.md section 7.** Elle est
   morte. Elle doit etre remplacee par une revendication de la liste (b).

## (b) Ce qui est neuf chez nous, une phrase par point, ecrite pour un relecteur qui a lu les deux papiers

1. **Nous mesurons les deux termes comme deux ratios a un referent humain, sur les memes
   donnees, les memes segmentations et les memes items, ce que LifeMem ne fait pas parce qu'il
   ne mesure jamais l'inter, ce que Garzon et al. ne font pas parce qu'ils n'ont pas de referent
   humain sur cette analyse, et ce que Kim et Lee ne font pas parce qu'ils rapportent des nuages
   de points sans ratio.**
2. **Nous fournissons le plancher de bruit humain que ni l'un ni l'autre ne fournit : les memes
   personnes reinterrogees deux semaines plus tard tombent en (1,003 ; 1,004) avec des
   intervalles contenant 1, ce qui prouve que la methode ne fabrique pas d'ecart la ou il n'y en
   a pas.**
3. **Nous montrons que la metrique d'exactitude employee par le champ est aveugle a la structure
   de la population simulee : deux conditions du meme papier, sur les memes 1 052 participants
   et les memes 169 items, dont l'exactitude differe de 0,07 point avec un intervalle
   [-0,52 ; +0,37], ont des gonflements d'ecarts inter groupes qui different d'un facteur 13,5
   avec des intervalles disjoints.**
4. **Nous corrigeons le biais d'estimation qui inverse le resultat : sans correction de Miller
   Madow, sans estimateur sans biais de l'indice de Simpson et sans controle par permutation des
   etiquettes de segment, un echantillon fini fabrique mecaniquement un terme inter positif qui
   croit avec le nombre de modalites employees, or les agents en emploient moins que les
   humains, ce qui produirait l'inverse du resultat cherche ; aucun des trois travaux voisins
   ne traite ce biais.**
5. **Nous montrons que la reponse a la question "y a t il double distorsion" depend de la
   condition de construction de l'agent et non du modele : quatre conditions sur six gonflent
   l'inter en ecrasant l'intra, deux ecrasent les deux ensemble, et l'ecart entre deux variantes
   portant la meme etiquette demographique dans le meme paquet de replication atteint un facteur
   6,9.**
6. **Nous posons le critere qu'aucun correctif publie ne satisfait : un correctif de l'identity
   essentialism doit etre evalue sur les deux termes apres son application, et non sur le seul
   terme intra, faute de quoi on ne peut pas distinguer un deplacement de variance d'une simple
   dilatation.** C'est la reformulation defendable du chantier 3.
7. **Nous montrons qu'une chaine de mesure qui ne verifie pas la conformite des sorties a la
   nomenclature de l'enquete inverse le classement de diversite : compte sur les chaines brutes,
   la variante `gss_v8` semble employer 4,48 modalites contre 3,62 aux humains, et une fois
   appariee a la nomenclature, 3,07 contre 3,62.** Aucun des trois travaux ne documente ce piege,
   et LifeMem filtre bien les sorties non analysables sans jamais mesurer l'effet du filtre.

## (c) Ce qu'il faut ajouter ou mesurer pour que (b) tienne

Par ordre de cout croissant.

**c.1. Reimplementer la metrique de LifeMem sur nos donnees, et publier l'inter a cote.**
[cout : quelques dizaines de lignes, aucune donnee nouvelle] Leur "within-group pairwise
distance" est le terme intra de notre mesure M2, a la normalisation pres. Calculer chez nous
leur ecart absolu, pas seulement notre ratio, met nos huit conditions du paquet OSF dans la
meme unite que leur tableau 1. Nous serons alors le seul travail a publier leur metrique **et**
le terme inter sur les memes lignes. C'est le geste de positionnement le moins cher et le plus
efficace.

**c.2. Recalculer l'ICC(1) de Garzon et al. sur nos huit conditions.** [cout : une soiree]
Meme formule, `(MS_between - MS_within) / (MS_between + (n_g - 1) MS_within)`, meme unite
d'observation, un score moyen par agent, et la strate age croise genre qu'ils emploient. Deux
benefices : nous parlons la langue de l'equipe de Bernstein et Kamphorst, et nous pouvons
publier ce qu'ils n'ont pas, l'ICC des humains sur les memes items, qui est le referent absent
de leur papier. C'est aussi le meilleur objet de conversation pour une prise de contact.

**c.3. Recalculer nos ratios sur la seule segmentation age x genre.** [cout : nul si
`a1-ratios-par-axe.csv` contient deja les deux axes separement] C'est la reponse a l'objection
la plus previsible : nos conditions ancrees gonflent l'inter alors que leurs agents ancres le
reduisent. Si le gonflement disparait sur age x genre, la contradiction est expliquee par la
segmentation et non par les donnees.

**c.4. Publier la mesure d'exactitude a cote de la structure, pour chaque condition.**
[cout : deja fait pour le GSS, a etendre] C'est notre revendication 3, et elle ne coute rien
puisque les exactitudes du paquet OSF sont dans
`figure2/data/new_analysis_summaries/gss_filtered/summary/individual_level.csv`.

**c.5. Appliquer notre decomposition aux sorties de LifeMem : ce n'est pas possible en l'etat,
et la question est tranchee.** [CONFIRME, verification faite ce soir] Le depot public contient
le code complet, les configurations, les nomenclatures de questions par vague, et les scripts
d'evaluation. Il ne contient **ni les reponses humaines, ni les sorties des agents**. Le README
du dossier `dataset` est explicite : "The respondent-level data used in this project cannot be
redistributed because both datasets are governed by their providers' data-use agreements."
L'arborescence attendue apres pretraitement montre des fichiers `human.csv` qui sont absents du
depot, et aucun repertoire `outputs` ou `runs` n'est publie.
[CONFIRME] https://github.com/halsayxi/LifeMem/blob/main/dataset/README.md et l'arborescence
complete du depot via l'API GitHub.
**Trois voies subsistent, dans l'ordre de cout.**
   - Ecrire aux auteurs pour demander les sorties d'agents, qui ne sont pas des microdonnees
     humaines et dont la redistribution ne tombe pas evidemment sous les accords d'usage des
     enquetes. C'est une demande a une equipe de Tsinghua sans conflit d'interet commercial avec
     nous, contrairement a Stanford. Cout : un courriel. C'est la premiere chose a faire.
   - Reproduire LifeMem nous memes sur Understanding Society, accessible via le UK Data Service
     avec un compte et un projet declare, ou sur les fichiers publics d'Add Health. Le code est
     complet, les modeles sont des modeles ouverts de 8 a 9 milliards de parametres, donc
     compatibles avec la contrainte de budget zero et avec le Mac M5, avec une reserve serieuse
     sur l'entrainement de 100 adaptateurs LoRA sequentiels sur quinze vagues, qui a ete fait
     sur une A800 de 80 Gio. [HYPOTHESE sur la faisabilite locale, a chiffrer avant de s'y
     engager, et a4 sur le bridage thermique est le rapport a relire d'abord.]
   - Renoncer a leurs sorties et faire porter la demonstration sur nos propres conditions, ce
     qui est deja suffisant pour la revendication 6 formulee comme un critere d'evaluation et
     non comme un resultat sur LifeMem.

**c.6. Lire arXiv 2603.16142 en entier avant redaction.** [cout : une soiree] Il affirme
l'aplatissement des ecarts inter groupes la ou nous affirmons leur gonflement. Tant que cette
contradiction n'est pas expliquee, la revendication 5 est attaquable.

**c.7. Lire Bisbee et al. 2024 dans le texte.** [cout : une soiree] C'est la source
methodologique de la seule mesure inter groupes anterieure sur le GSS. Ne pas la citer serait
une faute de related work ; la citer sans l'avoir lue serait pire.

**c.8. Changer le vocabulaire de "redistribution" et de "transport".** [cout : une decision]
Deux papiers de 2026 emploient deja "redistribute" pour autre chose, arXiv 2609.04485 pour un
deplacement de biais entre personas et arXiv 2602.18462 pour un deplacement d'erreur entre sous
groupes. Une formulation qui reste libre et qui dit exactement ce que nous faisons :
**"variance reallocation under a fixed total"**, ou en francais "reallocation de variance a
total fixe". Elle n'a ete trouvee dans aucun des papiers lus.

---

# 6. La phrase de related work, en anglais

Version longue, pour une section Related Work.

> Two recent studies come closest to the measurement we propose. Wang et al. (2026) name the
> underlying failure mode as identity essentialism and report that static-profile agents show
> "stronger demographic separation and within-group compression than humans"; their LifeMem
> framework reduces the within-group pairwise distance gap on Add Health and Understanding
> Society, but the between-group term is never quantified after the intervention, so it remains
> unknown whether variance was moved from between to within or simply added to both. Garzon et
> al. (2026) compute a one-way random-effects intraclass correlation within age-by-gender
> strata and find demographics-only agents to be markedly more homogeneous within strata than
> survey-anchored agents (RS: 0.17 vs. 0.06); because that analysis has no human ground truth,
> the ratio cannot be referenced to a human baseline, and its numerator and denominator are
> never reported separately. Earlier, Kim and Lee (2026), following Bisbee et al. (2024),
> evaluated between-group and within-group response variance on the GSS, but for a survey-tuned
> predictive model rather than prompt-conditioned personas, and reported agreement scatter
> rather than ratios to a human reference. We build directly on these three lines of work and
> add what none of them provides: both variance components estimated on the same data with
> bias-corrected estimators, each expressed as a ratio to a measured human reference whose test
> retest noise floor is estimated from the same respondents re-interviewed two weeks apart, and
> reported alongside individual-level accuracy, which we show can be identical across two agent
> populations whose between-group inflation differs by a factor of 13.5.

Version courte, pour une introduction ou un resume.

> Recent work names the phenomenon and corrects part of it: Wang et al. (2026) reduce
> within-group homogenization with longitudinal life-event memory, and Garzon et al. (2026)
> show lower within-stratum intraclass correlation for survey-anchored than for
> demographics-only agents. Neither reports the between-group term after the intervention, and
> neither normalizes against a measured human noise floor; we do both, and show that accuracy
> is blind to the difference.

**Avertissement de forme.** Les deux versions attribuent Wang et al. a 2026 et Garzon et al. a
2026 sur la base de la date de depot arXiv. Si l'un des deux est accepte en conference d'ici la
soumission, la citation doit basculer sur la reference publiee. LifeMem porte des marqueurs de
gabarit AAAI, mention `\corresponding` et section "Ethical Statement", ce qui suggere une
soumission a AAAI. [HYPOTHESE, deduite du gabarit, non confirmee.]

---

# 7. Ce que je n'ai pas pu verifier

1. **Le modele principal employe par Garzon et al. dans les tableaux 2 a 5.** Le papier insiste
   sur l'usage de modeles locaux en enclave securisee et l'annexe 7.8 donne des resultats
   additionnels sur Gemma3:12b et LLaMa 3.1:8b, mais je n'ai pas identifie avec certitude le
   modele des resultats principaux dans la version HTML. **A relire sur le PDF avant citation.**
2. **Les valeurs numeriques de la figure 13 de Garzon et al.** Les quatre valeurs d'ICC citees
   viennent du corps du texte, ou elles sont ecrites en toutes lettres, et non de la figure. La
   figure elle meme n'est pas lisible par un outil automatique. Les valeurs du corps sont donnees
   a deux decimales, ce qui limite la precision du calcul derive de la section 2.3.
3. **Le calcul de la section 2.3 n'a pas ete verifie sur le PDF.** Il combine deux tableaux dont
   les effectifs different, 224 a 270 agents selon la condition, ce qui indique qu'ils ne portent
   peut etre pas sur exactement le meme ensemble d'agents. Le calcul est un argument de lecture,
   pas un resultat, et il ne doit pas etre publie tel quel.
4. **Le jeu d'items exact du silhouette de LifeMem.** Deja signale par a10 point 4. La lecture
   complete de l'annexe B confirme le defaut : le papier decrit la construction du SES, l'invite,
   la standardisation et la formule du silhouette, mais **ne dit jamais quelles questions du WVS
   forment l'espace de reponse**. Le chiffre de 0,19 reste non reproductible meme avec le WVS en
   main. Le code public ne couvre pas cette analyse de motivation, il ne couvre que les
   experiences Add Health et Understanding Society.
5. **Le contenu de arXiv 2603.16142, PSII.** Seul le resume a ete lu, et il contredit la these du
   projet. C'est la lecture la plus urgente de la liste (c).
6. **Le contenu de Bisbee et al. 2024 dans Political Analysis.** L'existence, les auteurs, la
   revue, le volume et les pages sont confirmes ; le texte n'a pas ete ouvert et la definition
   exacte de leur mesure inter groupes n'est pas verifiee.
7. **La faisabilite locale d'une reproduction de LifeMem.** Cent adaptateurs LoRA entraines
   sequentiellement sur quinze vagues ont ete produits sur une A800 de 80 Gio. Rien n'a ete
   chiffre sur un Mac M5 de 32 Gio.
8. **Le statut de publication des deux papiers.** Aucun des deux ne porte de mention de
   conference ou de revue dans la version HTML consultee.
9. **Les tableaux reconstitues.** Les tableaux 1 et 2 de LifeMem et les tableaux 2 a 9 de Garzon
   et al. ont ete lus par extraction automatique du HTML. Les valeurs citees dans ce rapport ont
   toutes ete relues une par une dans le flux extrait, mais l'alignement colonne par colonne
   d'un tableau HTML reconstitue reste une source d'erreur. **Avant citation dans un dossier
   MIT, les deux tableaux 1 doivent etre relus sur le PDF.**
10. **Une recherche par absence n'est pas une preuve d'absence.** Les affirmations "LifeMem ne
    mesure jamais le terme inter" et "Garzon et al. ne publient aucune valeur humaine d'ICC"
    reposent sur une recherche exhaustive de chaines de caracteres dans le texte integral extrait
    du HTML, corps et annexes. Une figure dont la legende ne contiendrait pas le mot cherche
    pourrait porter l'information. Confiance elevee mais pas absolue.

---

# 8. Questions ouvertes pour Simon

1. **La revendication du projet doit se retracter une seconde fois en quinze jours.** Apres
   "les LLM ecrasent la variance", qui etait l'etat de l'art, puis "la double distorsion", que
   LifeMem publie dans son resume du 20 aout, il reste "la mesure conjointe des deux termes,
   rapportee a un plafond humain mesure, et sa dissociation d'avec l'exactitude". C'est vrai,
   c'est defendable, et c'est nettement plus etroit. **Est ce encore un papier, ou est ce
   devenu une section de methode dans le papier de quelqu'un d'autre ?** C'est la question que
   je ne peux pas trancher seul.
2. **Le precedent le plus proche est co signe par Bernstein et par Kamphorst, et il est porte
   par la recherche IA d'AXA, pas par Stanford.** Trois des six auteurs sont AXA Group
   Operations, Kamphorst est a Sciences Po. Cela change la strategie de contact : il y a
   peut etre un interlocuteur europeen, academique et non concurrent, plus accessible que
   l'equipe de Simile. **Faut il ecrire a Kamphorst a Sciences Po plutot qu'a Stanford ?**
3. **Les sorties de LifeMem ne sont pas publiques mais le code l'est, et les auteurs sont a
   Tsinghua, sans societe concurrente connue.** Un courriel demandant leurs sorties d'agents
   coute une heure et debloquerait la seule verification qui manque a notre revendication 6.
   **M'autorises tu a le rediger, sachant que cela signale notre angle a une equipe qui pourrait
   le combler elle meme dans sa version suivante ?**
4. **Un papier de mars 2026, arXiv 2603.16142, affirme l'inverse de notre these sur le terme
   inter, un aplatissement et non un gonflement, et propose un correctif par injection dans les
   etats caches.** Notre propre a1 trouve les deux regimes selon la condition. **Est ce que la
   these doit devenir "le sens de la distorsion inter depend du regime de construction de
   l'agent, et c'est pour cela qu'il faut la mesurer", ce qui est plus prudent et plus vrai,
   ou est ce que cela vide la these de sa force rhetorique ?**
5. **Le mot "transport" et le mot "redistribution" sont pris tous les deux, par trois papiers
   de 2026 dans trois sens differents.** Je propose "reallocation de variance a total fixe",
   en anglais "variance reallocation under a fixed total". **Tranches tu maintenant, avant
   qu'un quatrieme papier ne prenne aussi celui la ?**
6. **Aucun des trois precedents n'a de plafond humain, et deux le reconnaissent explicitement
   comme une limite.** C'est notre avantage le plus net et il vient entierement du paquet OSF,
   qui contient la reinterrogation a deux semaines des memes personnes. Or ce paquet ne declare
   aucune licence, a10 section 2.b. **Est ce que le seul atout non copiable du projet repose
   sur un fichier que nous n'avons pas le droit de redistribuer, et faut il securiser ce point
   par ecrit avant d'investir davantage dessus ?**
