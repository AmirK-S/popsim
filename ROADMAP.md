# ROADMAP

Quatre phases, avec un critere de passage explicite entre chacune. La logique est celle de
Simon : si la reproduction marche, on continue ; sinon on passe a autre chose sans regret.
La nouveaute est que le critere d'arret arrive **beaucoup plus tot** qu'un protocole a dix
entretiens, et qu'il coute deux jours au lieu de trois mois.

Aucune date n'est fixee, aucun horizon n'a ete arrete. Le sequencement est par jalons.
Les durees indiquees sont des journees de travail effectif.

---

## Phase 0. La reanalyse

**Duree :** 1 a 2 jours. **Cout :** zero euro, zero appel de modele. **Deja amorcee.**

Reanalyse des donnees publiques de Stanford deja telechargees. Production de la figure de
la double distorsion, du score de silhouette par condition, et de la distribution du plafond
humain de consistance test retest.

**Livrable :** une figure, un tableau, un script rejouable en une commande.

### Critere de passage vers la phase 1
La figure separe visiblement les conditions d'agents publiees, et les deux ratios de variance
se comportent bien dans deux directions opposees.

**Si le critere echoue :** la double distorsion n'est pas visible sur ces donnees. Il faut
alors verifier sur Twin-2K-500 avant de conclure, mais la these centrale du projet est
serieusement affaiblie et il faut le dire tout de suite.

---

## Phase 1. Le test existentiel

**Duree :** 2 jours. **Cout :** zero euro, quelques milliers d'appels locaux.

C'est le point de non retour du projet, et il vient avant la reproduction proprement dite.
Question unique : **existe t il un regime ou un LLM bat une regression logistique sur les
demographies ?** Deux experiences, les questions jamais posees et la courbe de croisement
selon la taille d'echantillon.

**Livrable :** une courbe, un chiffre de croisement, un verdict ecrit.

### Critere de passage vers la phase 2
Au moins un regime donne un avantage net et statistiquement significatif au modele de langage
sur les deux baselines obligatoires.

**Si le critere echoue :** le projet devient un papier de resultat negatif, et c'est une issue
honorable qui a sa valeur. Il faut alors le reconnaitre en une semaine et non en six mois, et
la matiere pour l'ecrire est deja produite par les phases 0 et 1. **C'est le scenario a
accepter par avance, avec Simon, avant de commencer.**

---

## Phase 2. La reproduction de bout en bout

**Duree :** 1 a 2 semaines. **Cout :** zero en local. 35 a 70 dollars si verification sur
modele frontiere, depense a arbitrer et non indispensable.

Reproduction complete sur Twin-2K-500 : 150 personas, 30 a 50 questions, six conditions
experimentales dont deux baselines non LLM et un controle d'extraction. Metriques de fidelite
individuelle et de diversite preservee publiees cote a cote. Observabilite complete des le
premier run. Pre enregistrement du protocole sur l'OSF avant le premier appel.

**Livrable :** le tableau de reproduction, avec les trois chiffres exiges pour chaque score,
brut, hors items contamines, et sur jeu posterieur a la date de coupure.

### Critere de passage vers la phase 3
La reproduction retrouve, dans une marge acceptable, l'ordre des conditions publie par
Stanford : demographique nettement en dessous, enquete proche de l'entretien. Et l'ecart entre
notre mesure et la leur s'explique.

**Si le critere echoue :** avant de conclure, verifier la contamination et le denominateur de
normalisation, qui sont les deux causes d'ecart les plus probables. Un echec de reproduction
proprement documente est lui aussi publiable, et plus utile au champ que la centieme
confirmation.

---

## Phase 3. La contribution

**Duree :** 2 a 4 semaines. **Cout :** zero en local.

Transport de variance a somme constante, retrecissement calibre des ecarts inter groupes,
et le critere transversal qui verifie que tout gain de variance correle aux vraies differences
entre personnes. En parallele, la mesure de contamination, qui est un terrain vierge et
independant du reste.

**Livrable :** le papier. Contribution annoncee : une decomposition qui rend les scores du
champ comparables, et un correctif specifique qui deplace la variance au lieu de l'ajouter.

### Critere de passage vers la phase 4
Le correctif rapproche les deux ratios de 1 **simultanement**, sans degrader la fidelite
individuelle, et le gain de variance passe le test de correlation aux differences reelles.

**Si le critere echoue :** la decomposition et la mesure restent publiables seules. C'est
pourquoi la decision 2 de la synthese recommande de mesurer avant de corriger : cet ordre
garantit qu'il reste un papier meme si le correctif ne marche pas.

---

## Phase 4. Le cas commercial

**Duree :** non estimee. **Prerequis :** phase 3 acquise.

Elle ne s'ouvre que si le papier existe. Position officielle du projet : on veut un papier de
recherche, la commercialisation c'est tant mieux si ca suit. Le paysage concurrentiel donne
une raison supplementaire de tenir cet ordre : le segment est desormais occupe par un acteur
a deux milliards de dollars fonde par les auteurs du papier de reference, et le seul angle
defendable identifie n'est pas d'etre fournisseur de simulation mais d'etre l'instance qui
mesure les simulations. Cet angle se construit par la publication, pas contre elle.

Premier produit candidat : l'extension d'enquete, le seul use case dont la validite soit deja
etayee par la litterature, et dont le test de validation est deja au programme scientifique en
phase 1.

---

## Ce qui court en parallele, independamment des phases

Ces trois demarches ont des delais longs et ne dependent d'aucun resultat. Les lancer tot
coute quelques heures et peut faire gagner des mois.

1. **La demande d'adresse institutionnelle** aupres du contact MIT. Debloque le pan francais
   des donnees, l'acces a un comite d'ethique, et des credits de calcul. Rendement le plus
   eleve pour le cout le plus faible.
2. **Le dossier American Voices Project.** Plusieurs mois de delai. Depose en septembre il
   arrive peut etre a temps pour une publication conjointe ; depose en janvier, non.
3. **La question du rattachement a une structure de recherche francaise.** Elle conditionne
   l'acces GENCI, jusqu'a 50 000 heures de GPU gratuites obtenues en quelques jours. Le contact
   MIT ne la debloque pas, c'est un chemin distinct.

---

## Les points d'arret a acter avant de commencer

Un projet de recherche a besoin de savoir a quoi il renonce. Trois conditions d'arret, a
valider avec Simon avant la phase 0 et non apres.

1. **Aucun regime de validite du LLM en phase 1.** On ecrit le resultat negatif et on s'arrete.
2. **La double distorsion invisible sur deux jeux de donnees independants.** La these centrale
   tombe, il n'y a pas de contribution specifique a apporter.
3. **Reproduction impossible avec un ecart inexplique.** On documente l'echec de reproduction
   et on s'arrete la.

Dans les trois cas, il reste un document publiable et environ trois semaines de travail
engagees, sans argent depense et sans qu'aucune personne reelle n'ait ete sollicitee. C'est
tout l'interet du sequencement retenu.
