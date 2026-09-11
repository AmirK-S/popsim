# r1. Resume d'evaluation de l'oracle des camps

Ecrit par `analyses/r1_evaluer.py`. Aucun appel de modele. Les definitions, les seuils et les corrections sont ceux de `resultats/r1-preenregistrement.md`, ecrit avant le premier appel.

Perimetre lu : **3576 cellules** de trace, suffixe `r7`, dont **216 rejets de parse** et **0 cellules retirees pour recopie de l'exemple de relance** (critere de chute 2). Perimetre exploite : **3360 cellules**, soit 94,0 pour cent.

## Criteres de chute

| critere | portee | valeur | verdict |
|---|---|---|---|
| 1. taux de rejet de parse apres relance | olmo3base | 0,034 | passe |
| 2. recopie du gabarit d'exemple de la relance | olmo3base | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | olmo3base | 0,234 | passe |
| 1. taux de rejet de parse apres relance | olmo3dpo | 0,068 | passe |
| 2. recopie du gabarit d'exemple de la relance | olmo3dpo | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | olmo3dpo | 0,133 | passe |
| 1. taux de rejet de parse apres relance | olmo3rlvr | 0,076 | passe |
| 2. recopie du gabarit d'exemple de la relance | olmo3rlvr | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | olmo3rlvr | 0,213 | passe |
| 1. taux de rejet de parse apres relance | olmo3sft | 0,064 | passe |
| 2. recopie du gabarit d'exemple de la relance | olmo3sft | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | olmo3sft | 0,267 | passe |
| 4. plancher humain, facteur w2 sur w1 | humains | 1,009 | passe |
| 5. effectifs des camps contre a30-gss-par-camp.csv | humains | 1052,000 | passe |
| 6. estimateur par substitution contre estimateur sans biais (a30) | humains | 0,003 | passe |

## H1, l'unanimite decrite contre l'unanimite reelle

Rapport `GS decrit / GS reel`. Sous 1, le modele rend le camp plus unanime qu'il n'est. Le plancher est le meme rapport entre les deux vagues humaines.

| modele | camp | identite | GS decrit | GS reel | rapport | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Olmo-3-1025-7B | gauche | journaliste | 0,499 | 0,442 | **1,129** | [1,063 ; 1,202] | 1,005 | 0,0162 | amplification |
| Olmo-3-1025-7B | gauche | adversaire | 0,484 | 0,447 | **1,084** | [1,015 ; 1,155] | 1,004 | 0,2070 | non significatif |
| Olmo-3-1025-7B | centre | journaliste | 0,602 | 0,497 | **1,210** | [1,158 ; 1,272] | 1,008 | 0,0012 | amplification |
| Olmo-3-1025-7B | centre | adversaire | 0,583 | 0,495 | **1,179** | [1,124 ; 1,244] | 1,008 | 0,0012 | amplification |
| Olmo-3-1025-7B | droite | journaliste | 0,580 | 0,498 | **1,164** | [1,114 ; 1,221] | 0,996 | 0,0012 | amplification |
| Olmo-3-1025-7B | droite | adversaire | 0,557 | 0,501 | **1,112** | [1,061 ; 1,169] | 0,996 | 0,0022 | amplification |
| Olmo-3-7B-Instruct-DPO | gauche | journaliste | 0,515 | 0,437 | **1,180** | [1,111 ; 1,260] | 1,005 | 0,0032 | amplification |
| Olmo-3-7B-Instruct-DPO | gauche | adversaire | 0,463 | 0,441 | **1,049** | [0,988 ; 1,117] | 1,005 | 1,0000 | non significatif |
| Olmo-3-7B-Instruct-DPO | centre | journaliste | 0,572 | 0,492 | **1,162** | [1,110 ; 1,222] | 1,010 | 0,0012 | amplification |
| Olmo-3-7B-Instruct-DPO | centre | adversaire | 0,562 | 0,492 | **1,142** | [1,092 ; 1,199] | 1,011 | 0,0012 | amplification |
| Olmo-3-7B-Instruct-DPO | droite | journaliste | 0,521 | 0,495 | **1,052** | [0,995 ; 1,115] | 0,994 | 1,0000 | non significatif |
| Olmo-3-7B-Instruct-DPO | droite | adversaire | 0,500 | 0,497 | **1,005** | [0,946 ; 1,065] | 0,996 | 1,0000 | non significatif |
| Olmo-3-7B-Instruct | gauche | journaliste | 0,516 | 0,437 | **1,181** | [1,112 ; 1,254] | 1,005 | 0,0022 | amplification |
| Olmo-3-7B-Instruct | gauche | adversaire | 0,455 | 0,442 | **1,028** | [0,960 ; 1,098] | 1,004 | 1,0000 | non significatif |
| Olmo-3-7B-Instruct | centre | journaliste | 0,582 | 0,494 | **1,178** | [1,129 ; 1,235] | 1,007 | 0,0012 | amplification |
| Olmo-3-7B-Instruct | centre | adversaire | 0,561 | 0,484 | **1,159** | [1,109 ; 1,216] | 1,009 | 0,0012 | amplification |
| Olmo-3-7B-Instruct | droite | journaliste | 0,522 | 0,487 | **1,071** | [1,013 ; 1,137] | 0,994 | 0,4356 | non significatif |
| Olmo-3-7B-Instruct | droite | adversaire | 0,489 | 0,496 | **0,985** | [0,927 ; 1,047] | 0,995 | 1,0000 | non significatif |
| Olmo-3-7B-Instruct-SFT | gauche | journaliste | 0,502 | 0,441 | **1,136** | [1,070 ; 1,208] | 1,005 | 0,3996 | non significatif |
| Olmo-3-7B-Instruct-SFT | gauche | adversaire | 0,443 | 0,435 | **1,017** | [0,942 ; 1,092] | 1,004 | 1,0000 | non significatif |
| Olmo-3-7B-Instruct-SFT | centre | journaliste | 0,578 | 0,493 | **1,173** | [1,122 ; 1,232] | 1,008 | 0,0012 | amplification |
| Olmo-3-7B-Instruct-SFT | centre | adversaire | 0,570 | 0,493 | **1,157** | [1,113 ; 1,210] | 1,009 | 0,0012 | amplification |
| Olmo-3-7B-Instruct-SFT | droite | journaliste | 0,532 | 0,496 | **1,072** | [1,021 ; 1,130] | 0,995 | 0,1358 | non significatif |
| Olmo-3-7B-Instruct-SFT | droite | adversaire | 0,476 | 0,499 | **0,954** | [0,892 ; 1,020] | 0,995 | 0,5964 | non significatif |

## H2, l'ecart entre camps

| hypothese | modele | identite | perimetre | ecart decrit | ecart reel | facteur | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| H2a, ecart non signe (TV entre camps) | Olmo-3-1025-7B | journaliste | tous les items | 0,184 | 0,214 | **0,859** | [0,688 ; 1,061] | 1,012 | 1,0000 | non significatif |
| H2a, ecart non signe (TV entre camps) | Olmo-3-1025-7B | adversaire | tous les items | 0,211 | 0,215 | **0,982** | [0,792 ; 1,204] | 1,008 | 0,0096 | significatif mais nul en pratique |
| H2a, ecart non signe (TV entre camps) | Olmo-3-7B-Instruct-DPO | journaliste | tous les items | 0,178 | 0,213 | **0,837** | [0,657 ; 1,024] | 1,016 | 0,9285 | non significatif |
| H2a, ecart non signe (TV entre camps) | Olmo-3-7B-Instruct-DPO | adversaire | tous les items | 0,223 | 0,215 | **1,039** | [0,842 ; 1,272] | 1,015 | 1,0000 | non significatif |
| H2a, ecart non signe (TV entre camps) | Olmo-3-7B-Instruct | journaliste | tous les items | 0,152 | 0,212 | **0,717** | [0,535 ; 0,911] | 1,012 | 1,0000 | non significatif |
| H2a, ecart non signe (TV entre camps) | Olmo-3-7B-Instruct | adversaire | tous les items | 0,235 | 0,214 | **1,098** | [0,885 ; 1,334] | 1,017 | 1,0000 | non significatif |
| H2a, ecart non signe (TV entre camps) | Olmo-3-7B-Instruct-SFT | journaliste | tous les items | 0,135 | 0,208 | **0,650** | [0,492 ; 0,838] | 1,013 | 1,0000 | non significatif |
| H2a, ecart non signe (TV entre camps) | Olmo-3-7B-Instruct-SFT | adversaire | tous les items | 0,239 | 0,220 | **1,085** | [0,863 ; 1,353] | 1,012 | 1,0000 | non significatif |
| H2b, ecart signe (position orientee) | Olmo-3-1025-7B | journaliste | items retenus stricts | 0,123 | 0,259 | **0,476** | [0,295 ; 0,689] | 1,010 | 0,0008 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-1025-7B | adversaire | items retenus stricts | 0,133 | 0,259 | **0,515** | [0,253 ; 0,800] | 1,011 | 0,0107 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct-DPO | journaliste | items retenus stricts | 0,149 | 0,256 | **0,584** | [0,312 ; 0,860] | 1,011 | 0,0254 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct-DPO | adversaire | items retenus stricts | 0,191 | 0,259 | **0,737** | [0,439 ; 1,072] | 1,010 | 0,3327 | non significatif |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct | journaliste | items retenus stricts | 0,125 | 0,259 | **0,484** | [0,255 ; 0,759] | 1,009 | 0,0021 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct | adversaire | items retenus stricts | 0,205 | 0,259 | **0,794** | [0,472 ; 1,134] | 1,011 | 0,4681 | non significatif |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct-SFT | journaliste | items retenus stricts | 0,103 | 0,254 | **0,406** | [0,202 ; 0,690] | 1,010 | 0,0010 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct-SFT | adversaire | items retenus stricts | 0,223 | 0,260 | **0,858** | [0,529 ; 1,236] | 1,011 | 0,4681 | non significatif |
| H2b, ecart signe (position orientee) | Olmo-3-1025-7B | journaliste | 79 items orientes | 0,109 | 0,240 | **0,455** | [0,285 ; 0,647] | 1,008 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-1025-7B | adversaire | 79 items orientes | 0,104 | 0,241 | **0,431** | [0,203 ; 0,705] | 1,009 | 0,0006 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct-DPO | journaliste | 79 items orientes | 0,150 | 0,237 | **0,630** | [0,388 ; 0,888] | 1,009 | 0,0300 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct-DPO | adversaire | 79 items orientes | 0,159 | 0,241 | **0,661** | [0,392 ; 0,965] | 1,008 | 0,0703 | non significatif |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct | journaliste | 79 items orientes | 0,126 | 0,240 | **0,526** | [0,327 ; 0,767] | 1,007 | 0,0032 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct | adversaire | 79 items orientes | 0,178 | 0,241 | **0,742** | [0,459 ; 1,065] | 1,009 | 0,2057 | non significatif |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct-SFT | journaliste | 79 items orientes | 0,098 | 0,236 | **0,415** | [0,221 ; 0,646] | 1,008 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Olmo-3-7B-Instruct-SFT | adversaire | 79 items orientes | 0,192 | 0,241 | **0,795** | [0,481 ; 1,131] | 1,009 | 0,2211 | non significatif |

## H3, l'identite du demandeur

Distance entre le portrait fait au journaliste et celui fait a un membre du camp adverse, contre le plancher de reinterrogation humaine. Le centre est exclu, comme annonce.

| modele | camp | TV entre identites | plancher humain | rapport | IC 95 % | items identiques | p Holm |
|---|---|---|---|---|---|---|---|
| Olmo-3-1025-7B | gauche | 0,105 | 0,023 | **4,525** | [3,470 ; 5,783] | 0,279 | 0,0004 |
| Olmo-3-1025-7B | droite | 0,100 | 0,027 | **3,705** | [3,007 ; 4,468] | 0,301 | 0,0004 |
| Olmo-3-7B-Instruct-DPO | gauche | 0,123 | 0,023 | **5,412** | [4,176 ; 6,818] | 0,252 | 0,0004 |
| Olmo-3-7B-Instruct-DPO | droite | 0,117 | 0,026 | **4,450** | [3,376 ; 5,683] | 0,333 | 0,0004 |
| Olmo-3-7B-Instruct | gauche | 0,145 | 0,023 | **6,358** | [4,919 ; 8,016] | 0,217 | 0,0004 |
| Olmo-3-7B-Instruct | droite | 0,124 | 0,026 | **4,755** | [3,666 ; 6,139] | 0,288 | 0,0004 |
| Olmo-3-7B-Instruct-SFT | gauche | 0,122 | 0,023 | **5,392** | [4,030 ; 7,064] | 0,296 | 0,0004 |
| Olmo-3-7B-Instruct-SFT | droite | 0,165 | 0,026 | **6,231** | [4,756 ; 8,033] | 0,381 | 0,0004 |

## H4, les items a derive marquee

| modele | identite | quantite | rho de Spearman | n items | p Holm |
|---|---|---|---|---|---|
| Olmo-3-1025-7B | journaliste | log amplification de l'ecart entre camps | **0,404** | 68 | 0,0080 |
| Olmo-3-1025-7B | adversaire | log amplification de l'ecart entre camps | **0,276** | 54 | 0,0520 |
| Olmo-3-7B-Instruct-DPO | journaliste | log amplification de l'ecart entre camps | **0,285** | 66 | 0,0520 |
| Olmo-3-7B-Instruct-DPO | adversaire | log amplification de l'ecart entre camps | **0,280** | 67 | 0,0520 |
| Olmo-3-7B-Instruct | journaliste | log amplification de l'ecart entre camps | **0,370** | 49 | 0,0520 |
| Olmo-3-7B-Instruct | adversaire | log amplification de l'ecart entre camps | **0,366** | 69 | 0,0210 |
| Olmo-3-7B-Instruct-SFT | journaliste | log amplification de l'ecart entre camps | **0,442** | 51 | 0,0080 |
| Olmo-3-7B-Instruct-SFT | adversaire | log amplification de l'ecart entre camps | **0,344** | 54 | 0,0500 |
| Olmo-3-1025-7B | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,686** | 79 | 0,0040 |
| Olmo-3-1025-7B | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,666** | 79 | 0,0040 |
| Olmo-3-7B-Instruct-DPO | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,481** | 78 | 0,0040 |
| Olmo-3-7B-Instruct-DPO | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,447** | 79 | 0,0040 |
| Olmo-3-7B-Instruct | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,522** | 78 | 0,0040 |
| Olmo-3-7B-Instruct | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,375** | 79 | 0,0040 |
| Olmo-3-7B-Instruct-SFT | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,504** | 79 | 0,0040 |
| Olmo-3-7B-Instruct-SFT | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,269** | 79 | 0,0205 |

## Ce que ce resume ne dit pas

- Aucune croyance humaine de second ordre n'est mesuree ici : les items ANES ne sont pas dans ce run. La phrase « le modele exagere plus que les humains » est interdite.
- Le facteur de H2b n'est pas celui de `a38` : perimetre d'items et mode different, seuls le signe et l'ordre de grandeur se comparent.
- Rien ici ne porte hors du GSS, hors des Etats Unis, ni hors de ces trois modeles a cette quantification.
