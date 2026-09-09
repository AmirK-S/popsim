# r6. Page de plan et de depense : l'oracle des camps sur les modeles frontiere

Ecrite le 9 septembre 2026 a 10:20, avant tout appel et avant toute cle d'API. En attente
de deux lignes d'Amir : la page est validee ; le plafond est valide.

## Question

Les modeles que le public utilise decrivent ils l'ecart entre camps comme les modeles locaux
de R1 et R4, c'est a dire en l'ecrasant, en inventant de la variete interne et en changeant de
portrait selon le demandeur ? Et le facteur trois du format se retrouve t il chez eux ?

## Ce qui sort de la machine

Le mode description seulement : « que repondrait un electeur de droite a la question X »,
149 items du GSS, 3 camps, 2 demandeurs, 894 cellules. Aucune reponse individuelle, aucune
fiche de personne. Le referent humain reste sur la machine.

## Modeles et fournisseurs, dans l'ordre

1. Gratuit, verifie le jour meme : Gemini via AI Studio, Mistral, modeles gratuits
   d'OpenRouter. Conditions d'usage relues avant le premier appel.
2. Payant, plafond dur regle sur la console avant la cle : GPT (OpenAI), Claude
   (Anthropic), Grok, DeepSeek.
Deux modes de lecture, preenregistres comme deux mesures distinctes : lecture des
probabilites par lettre quand le fournisseur les rend (OpenAI, Gemini) ; dix tirages a
temperature un quand il ne les rend pas (Anthropic). Le mode de lecture est verifie en
local sur Qwen3-4B : les deux doivent donner le meme ecart entre camps a 0,05 pres, sinon
la comparaison entre fournisseurs est interdite.

## Hypotheses, ecrites avant

- H1 : les modeles frontiere se contredisent entre eux d'au moins un facteur deux sur
  l'ecart entre camps, comme les trois locaux de R1 (0,245 a 1,268). Pari : vraie.
- H2 : tous changent de portrait selon le demandeur, a plus de deux fois le plancher
  humain. Pari : vraie.
- H3 : le format (gabarit contre trois exemples dans le tour utilisateur) deplace la mesure
  d'au moins 0,3 chez les frontiere comme chez Qwen. Pari : fausse, les modeles frontiere
  sont plus robustes au format ; ce pari va contre la these de R4 et peut couter.
- H4 : les plus gros modeles sont plus proches de 1 que les locaux. Pari : fausse.

## Depense

- Essai : 10 cellules par fournisseur, cout reel mesure, extrapolation ecrite ici avant la
  suite.
- Estimation avant essai : 894 cellules x 2 formats x 320 jetons, soit 0,6 million de jetons
  par modele, entre 0,5 et 3 EUR par modele payant, quatre modeles payants : 3 a 12 EUR,
  plafond dur a 25 EUR toutes cles confondues.
- Alternative gratuite epuisee avant : oui, les fournisseurs gratuits passent en premier.
- Regle d'arret : si l'essai de 10 cellules montre un taux de rejet superieur a 5 pour
  cent ou un cout par cellule superieur au double de l'estimation, arret et correction.
- Usages du resultat : tableau du papier ; carte de demonstration de l'outil ; piece jointe
  de la lettre au cosignataire. Traces gardees dans data/traces/r6-*.jsonl, jamais rachetees.

## Analyse

Meme evaluateur que R1 et R4, memes 79 items orientes, Holm dans les quatre familles ci
dessus et jamais entre elles. Aucun autre test.

## Registre

Chaque euro depense est inscrit dans resultats/registre-depenses.md avec ce qu'il a produit.
