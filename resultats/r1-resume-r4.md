# r1. Resume d'evaluation de l'oracle des camps

Ecrit par `analyses/r1_evaluer.py`. Aucun appel de modele. Les definitions, les seuils et les corrections sont ceux de `resultats/r1-preenregistrement.md`, ecrit avant le premier appel.

Perimetre lu : **3576 cellules** de trace, suffixe `r4`, dont **23 rejets de parse** et **56 cellules retirees pour recopie de l'exemple de relance** (critere de chute 2). Perimetre exploite : **3497 cellules**, soit 97,8 pour cent.

## Criteres de chute

| critere | portee | valeur | verdict |
|---|---|---|---|
| 1. taux de rejet de parse apres relance | q4 | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4 | 0,846 | chute, cellules retirees |
| 3. distribution identique d'un camp a l'autre | q4 | 0,197 | passe |
| 1. taux de rejet de parse apres relance | q4base | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4base | 1,000 | chute, cellules retirees |
| 3. distribution identique d'un camp a l'autre | q4base | 0,328 | passe |
| 1. taux de rejet de parse apres relance | q4hyb | 0,025 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4hyb | 1,000 | chute, cellules retirees |
| 3. distribution identique d'un camp a l'autre | q4hyb | 0,472 | passe |
| 1. taux de rejet de parse apres relance | q4nogab | 0,001 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4nogab | 1,000 | chute, cellules retirees |
| 3. distribution identique d'un camp a l'autre | q4nogab | 0,131 | passe |
| 4. plancher humain, facteur w2 sur w1 | humains | 1,009 | passe |
| 5. effectifs des camps contre a30-gss-par-camp.csv | humains | 1052,000 | passe |
| 6. estimateur par substitution contre estimateur sans biais (a30) | humains | 0,003 | passe |

## H1, l'unanimite decrite contre l'unanimite reelle

Rapport `GS decrit / GS reel`. Sous 1, le modele rend le camp plus unanime qu'il n'est. Le plancher est le meme rapport entre les deux vagues humaines.

| modele | camp | identite | GS decrit | GS reel | rapport | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | gauche | journaliste | 0,528 | 0,449 | **1,174** | [1,112 ; 1,247] | 1,005 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | gauche | adversaire | 0,533 | 0,451 | **1,181** | [1,119 ; 1,254] | 1,005 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | centre | journaliste | 0,555 | 0,498 | **1,114** | [1,063 ; 1,174] | 1,007 | 0,0027 | amplification |
| Qwen3-4B-Instruct-2507 | centre | adversaire | 0,573 | 0,501 | **1,145** | [1,099 ; 1,200] | 1,008 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | droite | journaliste | 0,534 | 0,504 | **1,059** | [1,013 ; 1,115] | 0,996 | 0,0094 | amplification |
| Qwen3-4B-Instruct-2507 | droite | adversaire | 0,537 | 0,507 | **1,060** | [1,019 ; 1,107] | 0,996 | 0,0030 | amplification |
| Qwen3-4B-Base | gauche | journaliste | 0,520 | 0,447 | **1,164** | [1,092 ; 1,244] | 1,004 | 0,0012 | amplification |
| Qwen3-4B-Base | gauche | adversaire | 0,491 | 0,447 | **1,099** | [1,023 ; 1,182] | 1,004 | 0,0105 | amplification |
| Qwen3-4B-Base | centre | journaliste | 0,570 | 0,497 | **1,147** | [1,095 ; 1,204] | 1,007 | 0,0012 | amplification |
| Qwen3-4B-Base | centre | adversaire | 0,580 | 0,495 | **1,173** | [1,121 ; 1,230] | 1,007 | 0,0012 | amplification |
| Qwen3-4B-Base | droite | journaliste | 0,545 | 0,504 | **1,081** | [1,032 ; 1,138] | 0,995 | 0,0094 | amplification |
| Qwen3-4B-Base | droite | adversaire | 0,528 | 0,505 | **1,046** | [0,996 ; 1,103] | 0,995 | 0,1085 | non significatif |
| Qwen3-4B | gauche | journaliste | 0,568 | 0,446 | **1,273** | [1,204 ; 1,357] | 1,005 | 0,0012 | amplification |
| Qwen3-4B | gauche | adversaire | 0,547 | 0,447 | **1,225** | [1,158 ; 1,304] | 1,005 | 0,0012 | amplification |
| Qwen3-4B | centre | journaliste | 0,589 | 0,498 | **1,183** | [1,129 ; 1,244] | 1,008 | 0,0012 | amplification |
| Qwen3-4B | centre | adversaire | 0,593 | 0,495 | **1,199** | [1,148 ; 1,258] | 1,008 | 0,0012 | amplification |
| Qwen3-4B | droite | journaliste | 0,573 | 0,498 | **1,152** | [1,099 ; 1,209] | 0,996 | 0,0012 | amplification |
| Qwen3-4B | droite | adversaire | 0,569 | 0,499 | **1,140** | [1,092 ; 1,198] | 0,996 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | gauche | journaliste | 0,494 | 0,449 | **1,101** | [1,035 ; 1,179] | 1,005 | 0,7938 | non significatif |
| Qwen3-4B-Instruct-2507 | gauche | adversaire | 0,487 | 0,453 | **1,074** | [1,011 ; 1,139] | 1,005 | 0,7938 | non significatif |
| Qwen3-4B-Instruct-2507 | centre | journaliste | 0,564 | 0,502 | **1,122** | [1,073 ; 1,177] | 1,008 | 0,1106 | non significatif |
| Qwen3-4B-Instruct-2507 | centre | adversaire | 0,581 | 0,495 | **1,174** | [1,121 ; 1,234] | 1,008 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | droite | journaliste | 0,552 | 0,507 | **1,090** | [1,044 ; 1,144] | 0,996 | 0,0094 | amplification |
| Qwen3-4B-Instruct-2507 | droite | adversaire | 0,518 | 0,504 | **1,028** | [0,976 ; 1,082] | 0,996 | 0,4140 | non significatif |

## H2, l'ecart entre camps

| hypothese | modele | identite | perimetre | ecart decrit | ecart reel | facteur | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | journaliste | tous les items | 0,189 | 0,211 | **0,894** | [0,769 ; 1,038] | 1,010 | 0,2492 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | adversaire | tous les items | 0,163 | 0,211 | **0,771** | [0,653 ; 0,907] | 1,011 | 0,3712 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Base | journaliste | tous les items | 0,128 | 0,210 | **0,610** | [0,472 ; 0,762] | 1,011 | 0,9303 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Base | adversaire | tous les items | 0,246 | 0,212 | **1,161** | [0,975 ; 1,380] | 1,014 | 0,0049 | amplification |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B | journaliste | tous les items | 0,080 | 0,213 | **0,376** | [0,285 ; 0,482] | 1,009 | 0,8115 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B | adversaire | tous les items | 0,098 | 0,210 | **0,469** | [0,360 ; 0,598] | 1,008 | 0,9303 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | journaliste | tous les items | 0,212 | 0,212 | **1,002** | [0,853 ; 1,155] | 1,011 | 0,0321 | significatif mais nul en pratique |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | adversaire | tous les items | 0,291 | 0,213 | **1,365** | [1,177 ; 1,570] | 1,012 | 0,0028 | amplification |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | items retenus stricts | 0,079 | 0,259 | **0,304** | [0,087 ; 0,510] | 1,011 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | items retenus stricts | 0,070 | 0,259 | **0,270** | [0,088 ; 0,462] | 1,011 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Base | journaliste | items retenus stricts | 0,148 | 0,259 | **0,574** | [0,362 ; 0,819] | 1,011 | 0,0040 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Base | adversaire | items retenus stricts | 0,123 | 0,259 | **0,476** | [0,164 ; 0,784] | 1,011 | 0,0081 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B | journaliste | items retenus stricts | 0,071 | 0,259 | **0,275** | [0,118 ; 0,444] | 1,011 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B | adversaire | items retenus stricts | 0,060 | 0,256 | **0,233** | [0,072 ; 0,418] | 1,010 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | items retenus stricts | 0,209 | 0,259 | **0,810** | [0,528 ; 1,093] | 1,011 | 0,3873 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | items retenus stricts | 0,254 | 0,259 | **0,982** | [0,656 ; 1,336] | 1,011 | 0,9209 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | 79 items orientes | 0,059 | 0,241 | **0,245** | [0,059 ; 0,432] | 1,009 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | 79 items orientes | 0,053 | 0,241 | **0,221** | [0,054 ; 0,389] | 1,009 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Base | journaliste | 79 items orientes | 0,136 | 0,241 | **0,566** | [0,365 ; 0,785] | 1,009 | 0,0012 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Base | adversaire | 79 items orientes | 0,106 | 0,241 | **0,440** | [0,145 ; 0,730] | 1,009 | 0,0021 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B | journaliste | 79 items orientes | 0,063 | 0,241 | **0,262** | [0,113 ; 0,410] | 1,009 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B | adversaire | 79 items orientes | 0,048 | 0,238 | **0,202** | [0,056 ; 0,356] | 1,007 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | 79 items orientes | 0,175 | 0,241 | **0,727** | [0,476 ; 0,988] | 1,009 | 0,0835 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | 79 items orientes | 0,207 | 0,241 | **0,859** | [0,537 ; 1,186] | 1,009 | 0,3986 | non significatif |

## H3, l'identite du demandeur

Distance entre le portrait fait au journaliste et celui fait a un membre du camp adverse, contre le plancher de reinterrogation humaine. Le centre est exclu, comme annonce.

| modele | camp | TV entre identites | plancher humain | rapport | IC 95 % | items identiques | p Holm |
|---|---|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | gauche | 0,073 | 0,024 | **3,074** | [2,411 ; 3,914] | 0,347 | 0,0004 |
| Qwen3-4B-Instruct-2507 | droite | 0,084 | 0,027 | **3,092** | [2,486 ; 3,786] | 0,272 | 0,0004 |
| Qwen3-4B-Base | gauche | 0,077 | 0,024 | **3,267** | [2,310 ; 4,455] | 0,528 | 0,0004 |
| Qwen3-4B-Base | droite | 0,137 | 0,027 | **5,048** | [3,882 ; 6,355] | 0,294 | 0,0004 |
| Qwen3-4B | gauche | 0,059 | 0,024 | **2,463** | [1,817 ; 3,271] | 0,528 | 0,0004 |
| Qwen3-4B | droite | 0,057 | 0,027 | **2,115** | [1,642 ; 2,642] | 0,511 | 0,0004 |
| Qwen3-4B-Instruct-2507 | gauche | 0,081 | 0,024 | **3,373** | [2,645 ; 4,180] | 0,329 | 0,0004 |
| Qwen3-4B-Instruct-2507 | droite | 0,115 | 0,027 | **4,202** | [3,455 ; 4,979] | 0,188 | 0,0004 |

## H4, les items a derive marquee

| modele | identite | quantite | rho de Spearman | n items | p Holm |
|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | journaliste | log amplification de l'ecart entre camps | **0,234** | 71 | 0,0640 |
| Qwen3-4B-Instruct-2507 | adversaire | log amplification de l'ecart entre camps | **0,269** | 61 | 0,0640 |
| Qwen3-4B-Base | journaliste | log amplification de l'ecart entre camps | **0,614** | 45 | 0,0040 |
| Qwen3-4B-Base | adversaire | log amplification de l'ecart entre camps | **0,297** | 66 | 0,0480 |
| Qwen3-4B | journaliste | log amplification de l'ecart entre camps | **0,428** | 39 | 0,0300 |
| Qwen3-4B | adversaire | log amplification de l'ecart entre camps | **0,617** | 35 | 0,0040 |
| Qwen3-4B-Instruct-2507 | journaliste | log amplification de l'ecart entre camps | **0,452** | 66 | 0,0040 |
| Qwen3-4B-Instruct-2507 | adversaire | log amplification de l'ecart entre camps | **0,440** | 77 | 0,0040 |
| Qwen3-4B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,635** | 79 | 0,0040 |
| Qwen3-4B-Instruct-2507 | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,649** | 79 | 0,0040 |
| Qwen3-4B-Base | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,628** | 79 | 0,0040 |
| Qwen3-4B-Base | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,627** | 79 | 0,0040 |
| Qwen3-4B | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,666** | 79 | 0,0040 |
| Qwen3-4B | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,629** | 79 | 0,0040 |
| Qwen3-4B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,641** | 79 | 0,0040 |
| Qwen3-4B-Instruct-2507 | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,628** | 79 | 0,0040 |

## Ce que ce resume ne dit pas

- Aucune croyance humaine de second ordre n'est mesuree ici : les items ANES ne sont pas dans ce run. La phrase « le modele exagere plus que les humains » est interdite.
- Le facteur de H2b n'est pas celui de `a38` : perimetre d'items et mode different, seuls le signe et l'ordre de grandeur se comparent.
- Rien ici ne porte hors du GSS, hors des Etats Unis, ni hors de ces trois modeles a cette quantification.
