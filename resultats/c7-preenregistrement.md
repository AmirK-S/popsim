# C7, preenregistrement : le jumeau ne predit pas, mais retrouve t il la personne ?

**Ecrit le 11 septembre 2026, avant tout calcul d'appariement.** Etude de risque de vie
privee sur un jeu deja public (Twin-2K-500). Aucune identite ni pid retrouve n'est jamais
imprime, ecrit ou publie : seuls des taux agreges sortent de `analyses/c7_reidentification.py`.
Lecture seule sur `data/`, zero appel de modele, zero reseau.

## 0. Verification structurelle faite avant ce texte, aucun appariement calcule
`t1_commun.charger()` releve : **60 des 108 items categoriels sont remplis a 100 pour cent**
chez les 2 058 humains de vague 4, y compris dans les huit configurations admissibles. Sur
le masque des 108 items, **1 651 motifs de manquants distincts sur 2 058 personnes**, taille
de groupe mediane 1, maximale 5 : le masque a lui seul est quasi une empreinte, consequence
de l'affectation aux bras inter sujets deja documentee dans l'audit de provenance. C'est
pourquoi l'attaque de contenu est restreinte aux 60 items toujours remplis, ou aucune
variation de masque n'existe des deux cotes.

## 1. Attaque
Pour chaque personne, sur chaque configuration admissible, comparer sa sortie de jumeau aux
2 058 vecteurs humains **de vague 4** (cible primaire) sur les **60 items communs** (jamais
manquants, humains comme jumeaux), avec la proportion d'accord = `1 - a2_commun.distance_hamming`
(deja ecrite, reprise telle quelle, pas de re-implementation). Vague 4 est retenue en
primaire car c'est la base que retrouverait un attaquant realiste (le questionnaire complete
lui meme) ; **les humains de vagues 1-3 servent de cible secondaire**, pour mesurer si la
fuite survit meme sans la vague exacte. `JSON Persona - GPT4.1-mini` n'a que 1 000 jumeaux :
la cible reste les 2 058 humains, seuls les 1 000 jumeaux disponibles sont attaques.

## 2. Mesures
Top-1, top-10 (rang mediane pour les liens : tirage aleatoire repete 20 fois, moyenne),
rang median, plus les trois memes mesures **a l'interieur du segment `S_gra`** (genre x
ethnicite x age, 40 niveaux, taille 1 a 259) de la personne. IC a 95 pour cent par
`a2_commun.bootstrap_personnes`, 2000 tirages, **graine 20260911**.

## 3. Comparateurs
Hasard exact = 1 / n_cible (0,0486 pour cent a 2 058) pour le top-1, 10/n_cible pour le
top-10. **Demographics Only - GPT4.1-mini**, meme pipeline, memes 60 items : c'est le
comparateur central, pas le hasard seul.

## 4. Garde-fous anti-triche
- Ordre des 2 058 candidats **permute** (graine dediee) avant tout calcul de rang, pour
  qu'aucun raccourci d'index ne puisse imiter une identification.
- Le pid n'est jamais lu par le code d'attaque, seul l'indice de ligne interne sert, jamais
  imprime ni ecrit dans `resultats/`.
- **Controle motifs de manquants seuls** : meme attaque, memes 2 058 cibles, mais sur le
  vecteur binaire present/absent des 108 items (aucune valeur), via le meme
  `distance_hamming` applique a un codage 0/1 sans manquant. Compare tenu de la section 0,
  ce controle n'est PAS attendu au niveau du hasard global (1651 motifs quasi uniques) ; il
  est rapporte contre le hasard **conditionnel a la taille du groupe de motif partage**
  (`moyenne(1/taille_groupe)`), et le point important a publier est si l'attaque de
  **contenu** depasse ce plancher structurel, pas si le controle est nul.

## 5. Configurations
Les 8 admissibles de `twin-ab-audit-provenance-2026-09-11.md` : Demographics Only, JSON
Persona GPT4.1, JSON Persona GPT4.1-mini (1 000), Text Persona (defaut, raisonnement,
repetition, mini), Text Persona Gemini-Flash2.5.

## 6. Prediction et critere « on fonce »
[HYPOTHESE] Meilleur jumeau riche : top-1 environ 5 pour cent contre 0,0486 pour cent au
hasard. **On fonce** (creuser plus, ecrire un article) si, pour au moins un jumeau riche,
top-1 >= 10 pour cent **ET** >= deux fois le top-1 de Demographics Only. Sinon, le rapport
publie les taux mesures sans relance.

## 7. Ce que ce plan ne dira pas
Rien sur le texte libre ni sur une identite reelle. Un seul jeu, une seule metrique de
similarite primaire. Le controle de motifs de manquants n'est pas un test de nullite au sens
classique, vu ce que la section 0 a deja montre.
