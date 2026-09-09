# popsim

Reproduire, puis depasser, la simulation d'individus reels par modele de langage.

Projet de recherche mene avec Simon, ouvert le 2 septembre 2026. Le systeme technique et la
recherche sont portes ici. Phase exploratoire terminee le 3 septembre 2026, aucun code de
production n'est ecrit avant validation de la synthese.

## Par ou commencer

| Document | Ce qu'il contient |
|---|---|
| [SYNTHESE.md](SYNTHESE.md) | Ce qu'on sait, ce qu'on ne sait pas, les cinq decisions a prendre avec Simon |
| [METHODOLOGIE.md](METHODOLOGIE.md) | Le protocole de reproduction consolide, en trois etages, pret a derouler |
| [BRAINSTORM.md](BRAINSTORM.md) | Dix neuf idees classees, chacune avec son test de validation le moins cher |
| [ROADMAP.md](ROADMAP.md) | Quatre phases, avec les criteres de passage et les points d'arret |
| [CONTEXTE.md](CONTEXTE.md) | Le contexte du projet et les references verifiees. A lire en premier par tout nouvel arrivant |

Le detail des preuves est dans `exploration/`, neuf rapports, environ 10 600 lignes, chaque
affirmation portant son niveau de confiance et sa source.

## La these

Les populations simulees par modele de langage ne sont pas trop homogenes, elles sont mal
structurees : trop homogenes a l'interieur des groupes, trop separees entre les groupes. Les
deux erreurs se compensent dans toute mesure globale, ce qui les rend invisibles aux
metriques employees aujourd'hui. Le correctif ne peut donc pas etre une dilatation de la
variance, ce doit etre un transport de variance a somme constante.

## Le premier resultat

    python3 analyses/a0_diversite_osf.py

Sur les donnees publiques de Stanford, 1 052 participants reels et 177 items du General
Social Survey : deux personnes reelles tirees au hasard donnent la meme reponse une fois sur
deux, deux agents demographiques deux fois sur trois. Les agents conservent de 66 a 91 pour
cent de la diversite de reponse humaine selon leur construction, la ou les memes humains
reinterrogees deux semaines plus tard en conservent 100,4 pour cent.

Aucun appel de modele, moins d'une seconde, rejouable par un tiers.

## Donnees

Le dossier `data/` n'est pas versionne, et ce n'est pas une question de taille : un commit
est une redistribution, et les licences des enquetes l'interdisent. Voir
[exploration/07-ethique-conformite.md](exploration/07-ethique-conformite.md).

Pour reconstituer le substrat de la phase 0 :

    mkdir -p data && curl -L -o data/replication.rar https://osf.io/download/s2u7c/

## Contraintes de travail

Budget zero, aucune personne recrutee. Ce ne sont pas des handicaps subis : le paquet de
replication de Stanford contient deja les reponses individuelles de 1 052 personnes reelles
en deux vagues, et la condition "questionnaire seul" du papier obtient 82 pour cent contre
83 pour cent pour un entretien de deux heures. La collecte humaine achete un point.

Le pipeline tourne integralement en local sur modeles ouverts, tant que les licences des
enquetes n'ont pas ete lues. Les paliers gratuits des API s'entrainent sur les donnees
envoyees.

## Licence

Code sous licence MIT, textes sous CC BY 4.0 (voir LICENSE). Les microdonnees d enquete ne sont jamais versionnees.
