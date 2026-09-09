# r1. Resume d'evaluation de l'oracle des camps

Ecrit par `analyses/r1_evaluer.py`. Aucun appel de modele. Les definitions, les seuils et les corrections sont ceux de `resultats/r1-preenregistrement.md`, ecrit avant le premier appel.

Perimetre lu : **52 cellules** de trace, suffixe `smoke`, dont **0 rejets de format** (0,0 pour cent).

## Criteres de chute

| critere | portee | valeur | verdict |
|---|---|---|---|
| 1. taux de rejet de format apres relance | oss20 | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | oss20 | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | oss20 | n. d. | passe |
| 1. taux de rejet de format apres relance | q30 | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | q30 | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | q30 | n. d. | passe |
| 1. taux de rejet de format apres relance | q4 | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4 | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | q4 | 0,125 | passe |
| 4. plancher humain, facteur w2 sur w1 | humains | 1,019 | passe |
| 5. effectifs des camps contre a30-gss-par-camp.csv | humains | 1052,000 | passe |
| 6. estimateur par substitution contre estimateur sans biais (a30) | humains | 0,003 | passe |

## H1, l'unanimite decrite contre l'unanimite reelle

Rapport `GS decrit / GS reel`. Sous 1, le modele rend le camp plus unanime qu'il n'est. Le plancher est le meme rapport entre les deux vagues humaines.

| modele | camp | identite | GS decrit | GS reel | rapport | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | gauche | journaliste | 0,631 | 0,447 | **1,411** | [1,185 ; 1,765] | 1,004 | 0,0468 | amplification |
| Qwen3-4B-Instruct-2507 | gauche | adversaire | 0,611 | 0,447 | **1,366** | [1,115 ; 1,723] | 1,004 | 0,0943 | non significatif |
| Qwen3-4B-Instruct-2507 | centre | journaliste | 0,630 | 0,543 | **1,160** | [1,062 ; 1,287] | 1,004 | 0,0468 | amplification |
| Qwen3-4B-Instruct-2507 | centre | adversaire | 0,630 | 0,543 | **1,161** | [1,057 ; 1,294] | 1,004 | 0,0586 | non significatif |
| Qwen3-4B-Instruct-2507 | droite | journaliste | 0,591 | 0,601 | **0,984** | [0,920 ; 1,044] | 0,996 | 0,6811 | non significatif |
| Qwen3-4B-Instruct-2507 | droite | adversaire | 0,541 | 0,601 | **0,901** | [0,829 ; 0,986] | 0,996 | 0,1227 | non significatif |

## H2, l'ecart entre camps

| hypothese | modele | identite | perimetre | ecart decrit | ecart reel | facteur | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | journaliste | tous les items | 0,130 | 0,299 | **0,435** | [0,258 ; 0,722] | 0,990 | 0,2162 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | adversaire | tous les items | 0,181 | 0,299 | **0,606** | [0,471 ; 0,829] | 0,990 | 0,1226 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | items retenus stricts | -0,069 | 0,282 | **-0,243** | [-0,483 ; -0,047] | 1,007 | 0,0299 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | items retenus stricts | -0,093 | 0,282 | **-0,329** | [-0,662 ; -0,021] | 1,007 | 0,0299 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | 79 items orientes | -0,074 | 0,250 | **-0,298** | [-0,640 ; -0,093] | 1,019 | 0,0160 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | 79 items orientes | -0,081 | 0,250 | **-0,325** | [-0,671 ; 0,000] | 1,019 | 0,0160 | attenuation |

## H3, l'identite du demandeur

Distance entre le portrait fait au journaliste et celui fait a un membre du camp adverse, contre le plancher de reinterrogation humaine. Le centre est exclu, comme annonce.

| modele | camp | TV entre identites | plancher humain | rapport | IC 95 % | items identiques | p Holm |
|---|---|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | gauche | 0,062 | 0,028 | **2,218** | [0,569 ; 4,553] | 0,375 | 0,2785 |
| Qwen3-4B-Instruct-2507 | droite | 0,109 | 0,030 | **3,566** | [2,656 ; 5,103] | 0,000 | 0,0139 |

## H4, les items a derive marquee

| modele | identite | quantite | rho de Spearman | n items | p Holm |
|---|---|---|---|---|---|
| gpt-oss-20b | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **n. d.** | 2 | n. d. |
| Qwen3-30B-A3B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **n. d.** | 2 | n. d. |
| Qwen3-4B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,976** | 8 | 0,0010 |
| Qwen3-4B-Instruct-2507 | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,976** | 8 | 0,0010 |
| Qwen3-4B-Instruct-2507 | journaliste | log amplification de l'ecart entre camps | **-0,107** | 7 | 0,8426 |
| Qwen3-4B-Instruct-2507 | adversaire | log amplification de l'ecart entre camps | **0,536** | 7 | 0,4768 |

## Ce que ce resume ne dit pas

- Aucune croyance humaine de second ordre n'est mesuree ici : les items ANES ne sont pas dans ce run. La phrase « le modele exagere plus que les humains » est interdite.
- Le facteur de H2b n'est pas celui de `a38` : perimetre d'items et mode different, seuls le signe et l'ordre de grandeur se comparent.
- Rien ici ne porte hors du GSS, hors des Etats Unis, ni hors de ces trois modeles a cette quantification.
