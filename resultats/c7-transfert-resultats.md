# C7-transfert, resultats : la fuite traverse-t-elle les configurations et les vagues ?

Calcule par `analyses/c7_transfert.py`, preenregistre dans `c7-transfert-preenregistrement.md`.
Matrice complete (56 paires) dans `resultats/c7-transfert-voletA.csv` ; ici, resume et extremes.

## Volet A — transfert entre les 8 configurations
**Retabule par nombre d'items communs** (`c7-transfert-voletA.csv`, colonne `n_items`) :
les 42 paires riches (hors Demographics Only) ne forment pas un seul groupe mais deux,
et la moyenne unique publiee auparavant (26,11 %) melangeait les deux.
- **30 paires a 60 items communs : top-1 moyen 36,4 %.**
- **12 paires a 19 items communs : top-1 moyen 0,45 %.**

Les 12 paires a 19 items sont **exactement** les paires impliquant `JSON Persona -
GPT4.1-mini` (les 40 items d'achat de cette config ne recouvrent que partiellement ceux
des autres) ; 6 d'entre elles ont de plus un bassin de 1 000 jumeaux et non 2 058. Mais le
nombre d'items communs, pas la taille du bassin, separe parfaitement les paires basses des
paires hautes : les 6 paires a 19 items et bassin 2 058 sont tout aussi basses que les 6 a
bassin 1 000. **L'explication anterieure (« configuration a 1 000 jumeaux au comportement
aberrant ») est fausse et retiree** : ce n'est pas un artefact d'une generation particuliere,
c'est un effet mecanique du nombre d'items partages entre les deux configs comparees.
Meilleure paire : **Text Persona (Default Temperature) → Text Persona**, deux variantes du
meme pipeline mini, 60 items communs, **83,58 %** (rang median 1/2058). Pire paire :
**JSON Persona GPT4.1-mini → Text Persona Gemini-Flash2.5**, 19 items communs, **0,06 %**
(bassin 2 058, donc pas un effet de petit bassin). **Demographics Only** contre les 7
configs riches (14 paires, deux sens) : top-1 moyen **7,76 %** (etendue 0,06-15,3 %),
nettement sous les 36,4 % des paires riches a 60 items : la seule demographie explique une
part reelle mais minoritaire.

## Volet B — transfert vers les humains de vagues 1-3
**Infaisable, confirme par calcul** : 108 items de vague 4 (jumeaux) contre 494 items de
contexte de vagues 1-3 (humains, non reposes en vague 4) → **0 item commun**, aucune
distance de Hamming calculable, aucune attaque lancee.

## Controle anti-artefact (decoy de meme segment S_gra)
Top-1 moyen du controle sur les 42 paires riches : **0,06 %** (maximum sur 56 paires :
0,24 %), contre la moyenne globale 26,11 % pour l'attaque reelle (facteur ~450). Par
sous-groupe : sur les 30 paires a 60 items, controle 0,04 % contre attaque 36,4 % (facteur
~900) ; sur les 12 paires a 19 items, controle 0,10 % contre attaque 0,45 % (facteur ~4,5,
nettement plus faible — a si peu d'items communs, le signal individuel domine a peine le
bruit de segment). Dans les deux cas le signal reste au-dessus du controle : il n'est pas
un artefact de segment demographique.

## Verdicts sur les predictions preenregistrees
- Volet A ≥ 15 % sur les paires riches : **confirme pour les 30 paires a 60 items
  (36,4 %) ; rejete pour les 12 paires a 19 items (0,45 %)**. La moyenne unique
  auparavant rapportee (26,11 %) masquait ce partage.
- Volet B ≥ 2 % si faisable : **sans objet**, volet declare infaisable avant calcul.
- Demographics Only nettement sous les paires riches : **confirme**, 7,76 % vs 36,4 %
  (paires a 60 items ; comparaison a 0,45 % non pertinente, nombre d'items different).
- Attaque reelle nettement au-dessus du controle intra-segment : **confirme dans les
  deux sous-groupes** (voir ci-dessus), avec un facteur bien plus faible sur les paires a
  19 items.

## Implication pour la publication de jumeaux LLM
Deux jumeaux de la MEME personne, produits par des pipelines ou modeles differents, se
recoupent fortement **quand ils partagent assez d'items communs** (36,4 % top-1 en
moyenne sur 60 items communs, jusqu'a 84 % pour la meilleure paire ; seulement 0,45 % sur
19 items communs) : si plusieurs organisations publient chacune leurs jumeaux du meme
panel avec un recouvrement d'items suffisant, un tiers peut croiser leurs sorties pour
retrouver les individus, sans aucune reponse humaine — un risque qui s'ajoute a, et
depasse par endroits, la fuite deja documentee contre les vraies vagues (20,68 % top-1,
`resultats/c7-resultats.md`).

## En clair
Deux "doubles numeriques" de la meme personne, meme faits par des IA differentes, se
ressemblent assez pour trahir qui est qui plus d'une fois sur trois quand on compare leurs
reponses sur les memes 60 questions -- mais presque jamais quand ils n'en partagent que
19 : la vie privee ne tient donc pas qu'a cacher les vraies reponses humaines, mais aussi
les autres doubles numeriques de la meme personne, a condition qu'ils repondent
suffisamment aux memes questions.

*Corrige apres relecture hostile du 12/09 : le chiffre unique 26,11 % melangeait 30
paires a 60 items (36,4 %) et 12 paires a 19 items (0,45 %) ; l'explication anterieure
(« configuration a 1 000 jumeaux au comportement aberrant ») etait fausse -- toutes les
paires basses sont exactement les paires a 19 items, y compris celles a bassin 2 058.*
