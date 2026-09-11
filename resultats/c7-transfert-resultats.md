# C7-transfert, resultats : la fuite traverse-t-elle les configurations et les vagues ?

Calcule par `analyses/c7_transfert.py`, preenregistre dans `c7-transfert-preenregistrement.md`.
Matrice complete (56 paires) dans `resultats/c7-transfert-voletA.csv` ; ici, resume et extremes.

## Volet A — transfert entre les 8 configurations
Top-1 moyen sur les **42 paires riches** (hors Demographics Only) : **26,11 %** (hasard
= 1/n_bassin ≈ 0,05-0,10 %). Meilleure paire : **Text Persona (Default Temperature) →
Text Persona**, deux variantes du meme pipeline mini, **83,58 %** (rang median 1/2058).
Pire paire : **JSON Persona GPT4.1-mini → Text Persona Gemini-Flash2.5**, **0,06 %**,
proche du hasard — ce config a 1 000 jumeaux est un cas a part, top-1 pres du hasard dans
presque toutes ses paires (attaquante ou bassin), artefact propre a cette generation, pas
un echec general du transfert. **Demographics Only** contre les 7 configs riches (14
paires, deux sens) : top-1 moyen **7,76 %** (etendue 0,06-15,3 %), nettement sous les
26,11 % des riches : la seule demographie explique une part reelle mais minoritaire.

## Volet B — transfert vers les humains de vagues 1-3
**Infaisable, confirme par calcul** : 108 items de vague 4 (jumeaux) contre 494 items de
contexte de vagues 1-3 (humains, non reposes en vague 4) → **0 item commun**, aucune
distance de Hamming calculable, aucune attaque lancee.

## Controle anti-artefact (decoy de meme segment S_gra)
Top-1 moyen du controle sur les paires riches : **0,06 %** (maximum sur 56 paires :
0,24 %), contre 26,11 % pour l'attaque reelle, facteur ~450 : le signal n'est pas un
artefact de segment demographique, il est porte par l'identite individuelle.

## Verdicts sur les predictions preenregistrees
- Volet A ≥ 15 % sur les paires riches : **confirme**, 26,11 % obtenu.
- Volet B ≥ 2 % si faisable : **sans objet**, volet declare infaisable avant calcul.
- Demographics Only nettement sous les paires riches : **confirme**, 7,76 % vs 26,11 %.
- Attaque reelle nettement au-dessus du controle intra-segment : **confirme**, 26,11 % vs 0,06 %.

## Implication pour la publication de jumeaux LLM
Deux jumeaux de la MEME personne, produits par des pipelines ou modeles differents, se
recoupent fortement (26 % top-1 en moyenne, jusqu'a 84 %) : si plusieurs organisations
publient chacune leurs jumeaux du meme panel, un tiers peut croiser leurs sorties pour
retrouver les individus, sans aucune reponse humaine — un risque qui s'ajoute a, et
depasse par endroits, la fuite deja documentee contre les vraies vagues (20,68 % top-1,
`resultats/c7-resultats.md`).

## En clair
Deux "doubles numeriques" de la meme personne, meme faits par des IA differentes, se
ressemblent assez pour trahir qui est qui une fois sur quatre en moyenne : la vie privee
ne tient donc pas qu'a cacher les vraies reponses humaines, mais aussi les autres doubles
numeriques de la meme personne.
