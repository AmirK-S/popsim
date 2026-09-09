# SYNTHESE

Etat au 3 septembre 2026, apres une phase exploratoire menee par neuf agents.
Sources detaillees dans `exploration/`, 10 600 lignes, chaque affirmation y porte son
niveau de confiance. Ce document ne repete pas les preuves, il tranche.

---

## 1. Ce qu'on sait maintenant et qu'on ne savait pas il y a vingt quatre heures

### 1.1 Le projet est finançable a zero euro, et ce n'est pas un pis aller

Le paquet de replication du papier de Stanford est public sur https://osf.io/t6g7k/ et il
contient bien plus qu'un resume. Verifie fichier par fichier : 1 052 participants reels,
177 items du General Social Survey, **les reponses en clair, item par item, individu par
individu**, pour les humains en vague 1, les memes humains en vague 2, et chacune des
conditions d'agents du papier. Trois heures apres le debut de l'exploration, la matiere
humaine que le projet croyait devoir collecter etait sur le disque.

S'y ajoute Twin-2K-500, sous licence CC BY 4.0 et sans compte : 2 058 personnes, plus de
500 questions chacune, quatre vagues dont une de retest. Et OpinionQA, 15 vagues du panel
Pew, reponses individuelles en clair, pour le passage a l'echelle.

### 1.2 L'entretien de deux heures n'achete presque rien

C'est le resultat qui reorganise tout le projet. Dans la version 3 du papier, du 28 juin
2026, les scores normalises sont de 83 pour cent pour un agent construit sur l'entretien
de deux heures, **82 pour cent pour un agent construit sur le questionnaire seul**, 86
pour cent pour la combinaison, contre 74 pour cent pour un agent purement demographique.

Deux heures d'entretien par personne achetent un point de fidelite. La contrainte "aucun
humain recrute" ne degrade donc pas le projet, elle le rend simplement moins cher. Et le
fait que l'entretien apporte si peu est en soi une question de recherche ouverte que
personne n'a traitee.

### 1.3 Le premier resultat original existe deja, il a ete calcule

Script `analyses/a0_diversite_osf.py`, rejouable en une commande, aucun appel de modele,
moins d'une seconde. Sur les 177 items du GSS et les 1 052 participants :

| Condition | Entropie moyenne | Part de la diversite humaine | Deux repondants au hasard sont d'accord |
|---|---|---|---|
| Humains, vague 1 | 1,2874 | 100,0 % | 49,5 % |
| Humains, vague 2 | 1,2919 | 100,4 % | 49,3 % |
| Agents composite | 1,1727 | 91,1 % | 53,4 % |
| Agents enquete | 1,1001 | 85,5 % | 55,8 % |
| Agents v8 | 1,0388 | 80,7 % | 57,9 % |
| Agents v7 | 0,8687 | 67,5 % | 66,6 % |
| Agents v6 | 0,8544 | 66,4 % | 66,4 % |

La derniere colonne est la formulation la plus lisible du probleme, et elle se dit en une
phrase devant n'importe quel interlocuteur : **deux personnes reelles tirees au hasard
donnent la meme reponse une fois sur deux ; deux agents demographiques, deux fois sur
trois.** La vague 2 des humains a 100,4 pour cent donne le plafond :
la variabilite n'est pas du bruit de mesure, c'est de la vraie diversite.

Aucun des papiers lus ne publie cette mesure.

### 1.4 Le probleme n'est pas celui que le projet croyait attaquer

La formulation "les LLM ecrasent la variance" est desormais l'etat de l'art et non une
contribution : au moins cinq papiers de 2026 l'attaquent frontalement. Elle est de plus
inexacte. Ce que la litterature documente est une **double distorsion de sens contraire** :

- la variance INTRA groupe est ecrasee, ratio mesure chez nous de **0,64 a 0,89** sur le GSS ;
  le 0,40 a 0,56 qui circulait est un ratio sur toute la population, pas un ratio intra groupe
  [corrige le 8 septembre 2026, voir a10 et a15] ;
- les ecarts INTER groupes sont GONFLES, facteur median 2,3 sur le GSS et 2,5 sur le WVS,
  etendue 1,3 a 4,7.

Les deux erreurs se compensent dans toute mesure globale. Un simulateur peut afficher un
ecart type de population correct en etant faux sur les deux composantes. La cause a un nom
dans la litterature, *identity essentialism* : le modele raisonne sur des stereotypes de
groupe et non sur des individus. Une statistique capte les deux a la fois, le score de
silhouette : 0,19 pour les agents contre -0,02 pour les humains sur le World Values Survey.
Les humains ne se regroupent pas par demographie. Les agents, si.

**Consequence, revue apres mesure :** le correctif ne peut pas etre une simple dilatation de
la variance, mais un transport a somme constante de l'inter vers l'intra est necessaire et
**non suffisant**. Le prototype le montre par l'arithmetique et par la mesure : un operateur a
somme constante laisse invariant le ratio de dispersion totale, qui vaut 0,802 a 0,954 selon la
condition et la mesure, donc le point (1, 1) est hors d'atteinte quel que soit le reglage. Il
faut deux operations, un transport et un comblement du deficit total [corrige le 8 septembre
2026, voir a7 et a20].

La these du projet devient donc : *les populations simulees par LLM ne sont pas trop
homogenes, elles sont mal structurees, trop homogenes dedans et trop separees dehors.*

### 1.5 Le marche s'est referme, et par les auteurs eux memes

Park, Bernstein et Liang, auteurs du papier a reproduire, ont fonde **Simile** : 100
millions de dollars en fevrier 2026, puis 200 millions en juillet a 2 milliards de
valorisation, environ 60 personnes, clients CVS, Deloitte, Gallup. L'intuition de Simon,
une seule societe sur ce segment, etait vraie il y a un an. Elle ne l'est plus : le segment
scientifique compte aujourd'hui cinq a six acteurs, dont Aaru a un milliard de valorisation
et Electric Twin, et le segment des personas marketing en compte une quinzaine.

**"L'acces possible aux auteurs de Stanford" doit sortir de la colonne des atouts.** Ces
auteurs sont le concurrent le mieux finance du marche.

Le pitch commercial ne resiste pas non plus en l'etat. Le cout reel d'une etude est de
25 000 a 65 000 dollars aux Etats Unis pour un projet sur mesure, mais de 4 900 euros hors
taxes pour 1 000 repondants en France. Le delai de trois mois vaut en full service, pas en
panel simple. Et les termes "5 pour cent de marge d'erreur" et "2 secondes" ne sont
soutenus par aucune source, ni interne ni publiee.

### 1.6 La menace qui peut tuer le projet, et son point faible

Une regression logistique multinomiale sur les seules demographies **bat** les quatre LLM
testes au niveau individuel : 0,622 contre 0,589 sur le GSS, 0,393 contre 0,277 sur le WVS,
ou le meilleur LLM tombe meme sous la simple marginale de question. Une copule gaussienne,
sans le moindre modele de langage, approche les 37 LLM testes sans les egaler, 0,688 contre
0,714 pour le meilleur, et les bat sur la correlation inter items ; sur nos propres mesures elle
bat les six conditions d'agents de Stanford sur les 70 items ordinaux du GSS, 0,5840 contre
0,5596 pour le composite [corrige le 8 septembre 2026, voir a10 et a8].

Mais cette defaite est **specifique au regime "persona demographique"**. Avec 100 exemples
reels de la personne en contexte, gpt-oss-120b divise par deux l'erreur de MICE PMM. Le
projet doit donc deserter le premier regime, ou tout le monde perd, et se battre dans le
second, qui est precisement celui que l'archive OSF et Twin-2K-500 permettent.

Regle adoptee : **toute condition experimentale du projet inclut une baseline non LLM
obligatoire.** Un chiffre sans plancher ne veut rien dire. Trois chiffres de "85 pour cent"
circulent deja dans ce champ et ne mesurent pas la meme quantite.

---

## 2. Ce qu'on ne sait pas

1. **Le regime de validite du LLM existe t il vraiment ?** Si aucun des regimes testes ne
   donne d'avantage net au modele de langage sur une regression logistique, la these de
   fond tombe. Le test coute deux jours et zero euro. Il doit etre le premier.
2. **La contamination.** Aucune etude publiee ne mesure la presence du GSS, de l'ANES ou du
   WVS dans les corpus d'entrainement, ni la degradation de fidelite avec l'ecart a la date
   de coupure. C'est la premiere objection d'un relecteur et la reponse n'existe pas encore.
   C'est donc aussi un terrain vierge.
3. **Le delai de retest n'est pas controle par la litterature.** Deux semaines chez
   Stanford, deux a quatre ans dans le panel GSS. Un score normalise a deux ans est
   mecaniquement plus flatteur qu'a deux semaines, et personne ne le signale.
4. **Pourquoi l'entretien n'apporte qu'un point.** Personne ne l'explique. Une part de la
   performance de la condition entretien vient d'une extraction de reponses deja donnees
   pendant l'entretien, et non d'une simulation. Les auteurs le confirment.
5. **La reference exacte du travail Nature evoque par Simon.** Le candidat le plus probable
   est Ashokkumar, Hewitt, Ghezae et Willer, *Large language models can predict the results
   of social science experiments*, Nature 656, aout 2026, r egal 0,85. Ce n'est pas de la
   psychiatrie. Une ligne de reponse de Simon fait gagner une journee.
6. **Ce que le contact MIT ouvre reellement.** Trois portes distinctes, de valeur tres
   inegale : la banque d'agents de Stanford, fermee et sans procedure publique ; les
   transcripts de l'American Voices Project, 2 700 entretiens apparies a un questionnaire,
   sur dossier avec plusieurs mois de delai ; et une adresse institutionnelle, qui
   conditionne le pan francais des donnees, l'acces a un comite d'ethique et des credits de
   calcul.

---

## 3. Les cinq decisions a prendre avec Simon

### Decision 1. La these du projet est elle reecrite ?

**Proposition :** remplacer "les LLM ecrasent la variance" par "les populations simulees
sont mal structurees, trop homogenes dedans et trop separees dehors", et faire du transport
de variance de l'inter vers l'intra le correctif vise, en sachant qu'il est necessaire et non
suffisant : le deficit de dispersion totale doit etre comble en plus [corrige le 8 septembre
2026, voir a7 et a20].

Ce qui est en jeu : la formulation actuelle est deja publiee par cinq equipes en 2026. La
nouvelle est exacte, plus originale, et debouche sur un correctif specifique. Elle implique
en revanche de renoncer a l'idee simple qu'il suffirait d'augmenter la diversite.

**A verser au dossier de cette decision, resultat du 8 septembre.** La difference entre les
deux generations demographiques du paquet de Stanford est un seul attribut d'invite,
l'etiquette ideologique, et elle vaut un facteur 25 sur le ratio inter de l'axe ideologie, de
0,34 pour `gss_v6` a 8,51 pour `gss_v8`, pour moins d'un point d'exactitude individuelle
[corrige le 8 septembre 2026, voir a19].

### Decision 2. Mesurer d'abord, ou corriger d'abord ?

**Proposition, recommandee :** mesurer d'abord. Publier la decomposition et l'indice de
double distorsion avant toute tentative de correctif.

Ce qui est en jeu : le champ manque de vocabulaire commun, six chiffres incomparables
circulent, et imposer la metrique d'un domaine est une contribution en soi doublee d'un
actif commercial. Le correctif est plus vendeur mais il n'a aucune valeur sans instrument
de mesure. Amir voudra probablement aller directement au correctif, Simon doit trancher.

### Decision 3. Quel jeu de donnees porte le premier resultat ?

**Proposition :** l'archive OSF pour la reanalyse immediate, qui ne coute aucun appel de
modele, puis Twin-2K-500 pour la replication de bout en bout, puis OpinionQA pour
l'echelle. Le barometre CEVIPOF du 4 juin 2026, posterieur a la coupure des modeles, sert
de jeu de validation contre la contamination.

Ce qui est en jeu : le corpus francais est notre meilleure protection contre la
contamination, mais un papier sur donnees francaises se vend moins bien dans une revue
americaine. Axe principal ou simple validation ?

### Decision 4. Le projet accepte t il d'etre un resultat negatif ?

**Question de positionnement, pas de technique.** Publier que des baselines statistiques
sans modele de langage egalent ou battent les LLM est le resultat le plus fort disponible a
cout nul. C'est aussi un papier qui se fait des ennemis dans la communaute dont on cherche
par ailleurs l'acces, et dont un acteur pese deux milliards de dollars.

Ma recommandation : oui, et l'assumer des la premiere conversation avec le MIT. Un
chercheur ne s'interesse pas a une demonstration, il s'interesse a un resultat negatif
propre ou a un resultat positif surprenant.

### Decision 5. Que demande t on au contact MIT, et dans quel ordre ?

**Proposition, par rendement decroissant :**
1. Une adresse institutionnelle nominative pour Amir. Elle debloque le pan francais des
   donnees, un comite d'ethique, et des credits de calcul. C'est la demande la moins
   couteuse et la plus structurante.
2. Le depot du dossier American Voices Project maintenant et non en janvier, le delai etant
   de plusieurs mois. Leur serveur est deja equipe d'Ollama, le protocole y est realisable
   sans sortie de donnees.
3. Une introduction aupres de Joon Sung Park, en sachant qu'il est desormais fondateur de
   Simile et que la demande doit etre formulee en consequence.

**A ne pas faire :** presenter "l'acces aux auteurs de Stanford" comme un atout du projet
sans avoir dit a Simon que ces auteurs ont leve 300 millions de dollars sur cette these.
Sa reaction a cette information est le renseignement le plus utile de la semaine.

---

## 4. Le calendrier a proposer

Aucune date n'a ete fixee. Le sequencement propose est par jalons, detaille dans
`ROADMAP.md`. Point de repere utile : le chemin critique jusqu'au premier chiffre
publiable est estime a quatorze taches et une centaine d'heures, et le premier chiffre
original est deja calcule.

---

## 5. Trois choses a ne pas oublier

1. **Le facteur limitant n'a jamais ete l'argent.** La machine fait environ 400 000 appels
   de modele par semaine gratuitement en local, et le calcul de puissance demande 70 a 150
   personas sur 30 a 50 questions, soit quelques heures de calcul. Le budget zero n'est pas
   une contrainte serieuse pour la phase 1.
2. **La trace d'execution contiendra les vraies reponses tenues secretes d'individus
   reels.** Savoir si elle peut etre versionnee doit etre tranche avant le premier run. La
   position par defaut retenue est non : trace publiee expurgee, renvoi au fichier officiel
   par identifiant.
3. **Le pipeline tourne integralement en local tant que les licences ne sont pas lues.**
   Les paliers gratuits des API s'entrainent sur les donnees envoyees, ce qui est
   incompatible avec des microdonnees sous licence. Le modele local n'est pas seulement le
   choix economique, c'est le seul propre.
