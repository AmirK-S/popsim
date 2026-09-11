# C7-gen, resultats : la fuite de C7 ne survit pas a NOS jumeaux bon marche
Preenregistre dans `resultats/c7-gen-preenregistrement.md`, calcule par
`analyses/c7_gen_analyse.py` (attaque `c7_reidentification.rangs_attaque` reprise telle
quelle). 1 400 appels de generation + 48 de contamination, cout reel **0,5055 USD** sur
1,50 USD autorises. Parse : 100,0 % (99,99 % en excluant 1 ligne sur 2 400). Aucun pid
imprime.
## 1. Reidentification parmi 2 058 humains (hasard top-1 = 0,049 %)
| modele | recette | temp | top-1 | IC 95 % | top-10 | exactitude |
|---|---|---|---|---|---|---|
| llama31-8b | R1 | 0 | 0,00 % | [0 ; 0] | 1,38 % | 39,4 % |
| llama31-8b | R2 | 0 | 0,00 % | [0 ; 0] | 0,45 % | 39,8 % |
| qwen37-flash | R1 | 0 | 0,23 % | [0 ; 0,68] | 1,10 % | 41,5 % |
| qwen37-flash | R2 | 0 | 0,00 % | [0 ; 0] | 0,00 % | 41,2 % |
| deepseek-v4 | R1 | 0 | 0,83 % | [0 ; 2,15] | 1,75 % | 45,5 % |
| deepseek-v4 | R2 | 0 | 0,50 % | [0 ; 1,50] | 2,15 % | 44,9 % |
| qwen37-flash | R1 | 1 | 0,00 % | [0 ; 0] | 0,00 % | 42,0 % |
Comparaison : `Demographics Only` de l'autre equipe = 2,13 %, `JSON Persona - GPT4.1` =
**20,68 %** (`resultats/c7-resultats.md`). Meilleur score ici = deepseek-v4/R1 = 0,83 %,
soit 25x moins que leur Demographics Only.
## 2. Verdict sur les trois predictions
1. **Rejetee.** R1 >= 10 % sur >= 2 modeles sur 3 : aucun modele n'atteint 1 %.
2. **Confirmee.** R2 < 3 % partout (0,00-0,50 %).
3. **Confirmee, non informative.** temp=1 (qwen/R1) top-1 = 0,00 % contre 0,23 % a temp=0 :
   verifiee, mais un effet de plancher (depart deja proche du hasard) n'est pas exclu.
## 3. Contamination (n=8 personnes x 3 modeles x 2 conditions, ~50 appels)
| modele | coupure | verbatim reel | verbatim fictif |
|---|---|---|---|
| llama31-8b | dec. 2023 (< mai 2025) | 0,00 % | 0,00 % |
| qwen37-flash | ~2026 (> mai 2025) | 50,00 % | 0,00 % |
| deepseek-v4 | doc. 2026-04-27 (> mai 2025) | 25,00 % | 0,00 % |
Llama31-8b (ancien) ne recopie RIEN verbatim, meme sur un vrai extrait : pas de
memorisation, et pas de fuite. Les deux modeles recents recopient des extraits reels bien
plus souvent qu'un temoin fictif (0 %) : memorisation probable chez eux. **Mais leur
reidentification reste elle aussi proche du hasard** (0,23 et 0,83 %) : la memorisation
n'explique donc pas l'absence de replication ici (n=8/cellule, indicatif seulement).
Genese des jumeaux de l'autre equipe anterieure a la publication du jeu (23 mai 2025) :
non etablie ici, seule la date de publication est sourcee.
## En clair
Demander nous-memes a des modeles generalistes bon marche de repondre a 60 questions
d'un coup, a partir du profil brut d'une personne, ne retrouve presque personne (au
mieux 0,83 % contre 20,7 % chez l'autre equipe) : la fuite mesuree sur Twin-2K-500 tient
a LEUR recette (finetuning ou formatage propres), pas au simple fait de donner un profil
a un LLM. Le risque de vie privee documente par C7 ne se generalise donc pas
automatiquement a n'importe quel pipeline de jumeau ; il reste specifique a des pipelines
proches de celui de l'article original.
