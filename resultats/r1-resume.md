# r1. Resume d'evaluation de l'oracle des camps

Ecrit par `analyses/r1_evaluer.py`. Aucun appel de modele. Les definitions, les seuils et les corrections sont ceux de `resultats/r1-preenregistrement.md`, ecrit avant le premier appel.

Perimetre lu : **2682 cellules** de trace, dont **1 rejets de parse** et **11 cellules retirees pour recopie de l'exemple de relance** (critere de chute 2). Perimetre exploite : **2670 cellules**, soit 99,6 pour cent.

## Criteres de chute

| critere | portee | valeur | verdict |
|---|---|---|---|
| 1. taux de rejet de parse apres relance | oss20 | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | oss20 | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | oss20 | 0,305 | passe |
| 1. taux de rejet de parse apres relance | q30 | 0,001 | passe |
| 2. recopie du gabarit d'exemple de la relance | q30 | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | q30 | 0,104 | passe |
| 1. taux de rejet de parse apres relance | q4 | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4 | 0,846 | chute, cellules retirees |
| 3. distribution identique d'un camp a l'autre | q4 | 0,197 | passe |
| 4. plancher humain, facteur w2 sur w1 | humains | 1,009 | passe |
| 5. effectifs des camps contre a30-gss-par-camp.csv | humains | 1052,000 | passe |
| 6. estimateur par substitution contre estimateur sans biais (a30) | humains | 0,003 | passe |

## H1, l'unanimite decrite contre l'unanimite reelle

Rapport `GS decrit / GS reel`. Sous 1, le modele rend le camp plus unanime qu'il n'est. Le plancher est le meme rapport entre les deux vagues humaines.

| modele | camp | identite | GS decrit | GS reel | rapport | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|
| gpt-oss-20b | gauche | journaliste | 0,497 | 0,453 | **1,097** | [1,039 ; 1,156] | 1,005 | 0,0014 | amplification |
| gpt-oss-20b | gauche | adversaire | 0,480 | 0,453 | **1,060** | [1,009 ; 1,115] | 1,005 | 0,1337 | non significatif |
| gpt-oss-20b | centre | journaliste | 0,552 | 0,502 | **1,099** | [1,048 ; 1,149] | 1,008 | 0,0018 | amplification |
| gpt-oss-20b | centre | adversaire | 0,541 | 0,502 | **1,077** | [1,027 ; 1,123] | 1,008 | 0,0171 | amplification |
| gpt-oss-20b | droite | journaliste | 0,529 | 0,508 | **1,042** | [0,998 ; 1,088] | 0,996 | 0,0261 | significatif mais nul en pratique |
| gpt-oss-20b | droite | adversaire | 0,513 | 0,508 | **1,009** | [0,964 ; 1,053] | 0,996 | 0,4428 | non significatif |
| Qwen3-30B-A3B-Instruct-2507 | gauche | journaliste | 0,490 | 0,451 | **1,086** | [1,036 ; 1,143] | 1,004 | 0,0036 | amplification |
| Qwen3-30B-A3B-Instruct-2507 | gauche | adversaire | 0,484 | 0,453 | **1,069** | [1,021 ; 1,119] | 1,005 | 0,0261 | amplification |
| Qwen3-30B-A3B-Instruct-2507 | centre | journaliste | 0,554 | 0,502 | **1,103** | [1,063 ; 1,149] | 1,008 | 0,0014 | amplification |
| Qwen3-30B-A3B-Instruct-2507 | centre | adversaire | 0,539 | 0,502 | **1,073** | [1,032 ; 1,118] | 1,008 | 0,0907 | non significatif |
| Qwen3-30B-A3B-Instruct-2507 | droite | journaliste | 0,550 | 0,508 | **1,083** | [1,040 ; 1,127] | 0,996 | 0,0009 | amplification |
| Qwen3-30B-A3B-Instruct-2507 | droite | adversaire | 0,534 | 0,508 | **1,052** | [1,010 ; 1,099] | 0,996 | 0,0261 | amplification |
| Qwen3-4B-Instruct-2507 | gauche | journaliste | 0,528 | 0,449 | **1,174** | [1,109 ; 1,243] | 1,005 | 0,0009 | amplification |
| Qwen3-4B-Instruct-2507 | gauche | adversaire | 0,533 | 0,451 | **1,181** | [1,116 ; 1,249] | 1,005 | 0,0009 | amplification |
| Qwen3-4B-Instruct-2507 | centre | journaliste | 0,555 | 0,498 | **1,114** | [1,063 ; 1,175] | 1,007 | 0,0027 | amplification |
| Qwen3-4B-Instruct-2507 | centre | adversaire | 0,573 | 0,501 | **1,145** | [1,098 ; 1,199] | 1,008 | 0,0009 | amplification |
| Qwen3-4B-Instruct-2507 | droite | journaliste | 0,534 | 0,504 | **1,059** | [1,014 ; 1,116] | 0,996 | 0,0076 | amplification |
| Qwen3-4B-Instruct-2507 | droite | adversaire | 0,537 | 0,507 | **1,060** | [1,020 ; 1,108] | 0,996 | 0,0035 | amplification |

## H2, l'ecart entre camps

| hypothese | modele | identite | perimetre | ecart decrit | ecart reel | facteur | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| H2a, ecart non signe (TV entre camps) | gpt-oss-20b | journaliste | tous les items | 0,184 | 0,211 | **0,875** | [0,720 ; 1,038] | 1,010 | 0,1011 | non significatif |
| H2a, ecart non signe (TV entre camps) | gpt-oss-20b | adversaire | tous les items | 0,227 | 0,211 | **1,076** | [0,921 ; 1,245] | 1,010 | 0,0036 | amplification |
| H2a, ecart non signe (TV entre camps) | Qwen3-30B-A3B-Instruct-2507 | journaliste | tous les items | 0,247 | 0,211 | **1,175** | [1,048 ; 1,320] | 1,010 | 0,0003 | amplification |
| H2a, ecart non signe (TV entre camps) | Qwen3-30B-A3B-Instruct-2507 | adversaire | tous les items | 0,279 | 0,211 | **1,324** | [1,179 ; 1,492] | 1,010 | 0,0003 | amplification |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | journaliste | tous les items | 0,189 | 0,211 | **0,894** | [0,780 ; 1,045] | 1,010 | 0,1041 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | adversaire | tous les items | 0,163 | 0,211 | **0,771** | [0,646 ; 0,915] | 1,011 | 0,1041 | non significatif |
| H2b, ecart signe (position orientee) | gpt-oss-20b | journaliste | 79 items orientes | 0,149 | 0,241 | **0,618** | [0,408 ; 0,842] | 1,009 | 0,0049 | attenuation |
| H2b, ecart signe (position orientee) | gpt-oss-20b | adversaire | 79 items orientes | 0,152 | 0,241 | **0,633** | [0,383 ; 0,894] | 1,009 | 0,0083 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-30B-A3B-Instruct-2507 | journaliste | 79 items orientes | 0,305 | 0,241 | **1,268** | [1,097 ; 1,464] | 1,009 | 0,0066 | amplification |
| H2b, ecart signe (position orientee) | Qwen3-30B-A3B-Instruct-2507 | adversaire | 79 items orientes | 0,329 | 0,241 | **1,366** | [1,155 ; 1,599] | 1,009 | 0,0020 | amplification |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | 79 items orientes | 0,059 | 0,241 | **0,245** | [0,056 ; 0,437] | 1,009 | 0,0003 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | 79 items orientes | 0,053 | 0,241 | **0,221** | [0,053 ; 0,380] | 1,009 | 0,0003 | attenuation |
| H2b, ecart signe (position orientee) | gpt-oss-20b | journaliste | items retenus stricts | 0,179 | 0,259 | **0,694** | [0,463 ; 0,933] | 1,011 | 0,0332 | attenuation |
| H2b, ecart signe (position orientee) | gpt-oss-20b | adversaire | items retenus stricts | 0,184 | 0,259 | **0,713** | [0,437 ; 0,992] | 1,011 | 0,0561 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-30B-A3B-Instruct-2507 | journaliste | items retenus stricts | 0,334 | 0,259 | **1,293** | [1,101 ; 1,499] | 1,011 | 0,0069 | amplification |
| H2b, ecart signe (position orientee) | Qwen3-30B-A3B-Instruct-2507 | adversaire | items retenus stricts | 0,358 | 0,259 | **1,386** | [1,183 ; 1,623] | 1,011 | 0,0026 | amplification |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | items retenus stricts | 0,079 | 0,259 | **0,304** | [0,117 ; 0,514] | 1,011 | 0,0003 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | items retenus stricts | 0,070 | 0,259 | **0,270** | [0,088 ; 0,463] | 1,011 | 0,0003 | attenuation |

## H3, l'identite du demandeur

Distance entre le portrait fait au journaliste et celui fait a un membre du camp adverse, contre le plancher de reinterrogation humaine. Le centre est exclu, comme annonce.

| modele | camp | TV entre identites | plancher humain | rapport | IC 95 % | items identiques | p Holm |
|---|---|---|---|---|---|---|---|
| gpt-oss-20b | gauche | 0,103 | 0,024 | **4,234** | [3,196 ; 5,616] | 0,396 | 0,0003 |
| gpt-oss-20b | droite | 0,101 | 0,028 | **3,637** | [2,766 ; 4,604] | 0,403 | 0,0003 |
| Qwen3-30B-A3B-Instruct-2507 | gauche | 0,073 | 0,024 | **3,038** | [2,343 ; 3,771] | 0,236 | 0,0003 |
| Qwen3-30B-A3B-Instruct-2507 | droite | 0,076 | 0,028 | **2,735** | [2,152 ; 3,507] | 0,302 | 0,0003 |
| Qwen3-4B-Instruct-2507 | gauche | 0,073 | 0,024 | **3,074** | [2,396 ; 3,856] | 0,347 | 0,0003 |
| Qwen3-4B-Instruct-2507 | droite | 0,084 | 0,027 | **3,092** | [2,483 ; 3,827] | 0,272 | 0,0003 |

## H4, les items a derive marquee

| modele | identite | quantite | rho de Spearman | n items | p Holm |
|---|---|---|---|---|---|
| gpt-oss-20b | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,678** | 79 | 0,0030 |
| gpt-oss-20b | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,551** | 79 | 0,0030 |
| Qwen3-30B-A3B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,495** | 79 | 0,0030 |
| Qwen3-30B-A3B-Instruct-2507 | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,434** | 79 | 0,0030 |
| Qwen3-4B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,635** | 79 | 0,0030 |
| Qwen3-4B-Instruct-2507 | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,649** | 79 | 0,0030 |
| gpt-oss-20b | journaliste | log amplification de l'ecart entre camps | **0,380** | 52 | 0,0210 |
| gpt-oss-20b | adversaire | log amplification de l'ecart entre camps | **0,417** | 62 | 0,0040 |
| Qwen3-30B-A3B-Instruct-2507 | journaliste | log amplification de l'ecart entre camps | **0,461** | 77 | 0,0030 |
| Qwen3-30B-A3B-Instruct-2507 | adversaire | log amplification de l'ecart entre camps | **0,497** | 75 | 0,0030 |
| Qwen3-4B-Instruct-2507 | journaliste | log amplification de l'ecart entre camps | **0,234** | 71 | 0,0700 |
| Qwen3-4B-Instruct-2507 | adversaire | log amplification de l'ecart entre camps | **0,269** | 61 | 0,0700 |

## Ce que ce resume ne dit pas

- Aucune croyance humaine de second ordre n'est mesuree ici : les items ANES ne sont pas dans ce run. La phrase « le modele exagere plus que les humains » est interdite.
- Le facteur de H2b n'est pas celui de `a38` : perimetre d'items et mode different, seuls le signe et l'ordre de grandeur se comparent.
- Rien ici ne porte hors du GSS, hors des Etats Unis, ni hors de ces trois modeles a cette quantification.
