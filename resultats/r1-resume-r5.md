# r1. Resume d'evaluation de l'oracle des camps

Ecrit par `analyses/r1_evaluer.py`. Aucun appel de modele. Les definitions, les seuils et les corrections sont ceux de `resultats/r1-preenregistrement.md`, ecrit avant le premier appel.

Perimetre lu : **3576 cellules** de trace, suffixe `r5`, dont **21 rejets de parse** et **50 cellules retirees pour recopie de l'exemple de relance** (critere de chute 2). Perimetre exploite : **3505 cellules**, soit 98,0 pour cent.

## Criteres de chute

| critere | portee | valeur | verdict |
|---|---|---|---|
| 1. taux de rejet de parse apres relance | q4 | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4 | 0,846 | chute, cellules retirees |
| 3. distribution identique d'un camp a l'autre | q4 | 0,197 | passe |
| 1. taux de rejet de parse apres relance | q4base | 0,000 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4base | 1,000 | chute, cellules retirees |
| 3. distribution identique d'un camp a l'autre | q4base | 0,328 | passe |
| 1. taux de rejet de parse apres relance | q4gab3 | 0,022 | passe |
| 2. recopie du gabarit d'exemple de la relance | q4gab3 | 0,000 | passe |
| 3. distribution identique d'un camp a l'autre | q4gab3 | 0,138 | passe |
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
| Qwen3-4B-Instruct-2507 | centre | journaliste | 0,555 | 0,498 | **1,114** | [1,063 ; 1,174] | 1,007 | 0,0037 | amplification |
| Qwen3-4B-Instruct-2507 | centre | adversaire | 0,573 | 0,501 | **1,145** | [1,099 ; 1,200] | 1,008 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | droite | journaliste | 0,534 | 0,504 | **1,059** | [1,013 ; 1,115] | 0,996 | 0,0126 | amplification |
| Qwen3-4B-Instruct-2507 | droite | adversaire | 0,537 | 0,507 | **1,060** | [1,019 ; 1,107] | 0,996 | 0,0042 | amplification |
| Qwen3-4B-Base | gauche | journaliste | 0,520 | 0,447 | **1,164** | [1,092 ; 1,244] | 1,004 | 0,0016 | amplification |
| Qwen3-4B-Base | gauche | adversaire | 0,491 | 0,447 | **1,099** | [1,023 ; 1,182] | 1,004 | 0,0157 | amplification |
| Qwen3-4B-Base | centre | journaliste | 0,570 | 0,497 | **1,147** | [1,095 ; 1,204] | 1,007 | 0,0012 | amplification |
| Qwen3-4B-Base | centre | adversaire | 0,580 | 0,495 | **1,173** | [1,121 ; 1,230] | 1,007 | 0,0012 | amplification |
| Qwen3-4B-Base | droite | journaliste | 0,545 | 0,504 | **1,081** | [1,032 ; 1,138] | 0,995 | 0,0126 | amplification |
| Qwen3-4B-Base | droite | adversaire | 0,528 | 0,505 | **1,046** | [0,996 ; 1,103] | 0,995 | 0,1085 | non significatif |
| Qwen3-4B-Instruct-2507 | gauche | journaliste | 0,494 | 0,449 | **1,101** | [1,036 ; 1,170] | 1,005 | 0,8106 | non significatif |
| Qwen3-4B-Instruct-2507 | gauche | adversaire | 0,487 | 0,453 | **1,074** | [1,012 ; 1,140] | 1,005 | 0,8106 | non significatif |
| Qwen3-4B-Instruct-2507 | centre | journaliste | 0,564 | 0,502 | **1,122** | [1,074 ; 1,179] | 1,008 | 0,1106 | non significatif |
| Qwen3-4B-Instruct-2507 | centre | adversaire | 0,581 | 0,495 | **1,174** | [1,122 ; 1,233] | 1,008 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | droite | journaliste | 0,552 | 0,507 | **1,090** | [1,043 ; 1,141] | 0,996 | 0,0110 | amplification |
| Qwen3-4B-Instruct-2507 | droite | adversaire | 0,518 | 0,504 | **1,028** | [0,978 ; 1,081] | 0,996 | 0,4198 | non significatif |
| Qwen3-4B-Instruct-2507 | gauche | journaliste | 0,502 | 0,452 | **1,110** | [1,048 ; 1,179] | 1,005 | 0,0297 | amplification |
| Qwen3-4B-Instruct-2507 | gauche | adversaire | 0,496 | 0,447 | **1,109** | [1,051 ; 1,180] | 1,005 | 0,0296 | amplification |
| Qwen3-4B-Instruct-2507 | centre | journaliste | 0,576 | 0,494 | **1,166** | [1,114 ; 1,226] | 1,008 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | centre | adversaire | 0,581 | 0,495 | **1,174** | [1,123 ; 1,230] | 1,008 | 0,0012 | amplification |
| Qwen3-4B-Instruct-2507 | droite | journaliste | 0,551 | 0,507 | **1,089** | [1,040 ; 1,143] | 0,996 | 0,0126 | amplification |
| Qwen3-4B-Instruct-2507 | droite | adversaire | 0,530 | 0,503 | **1,054** | [1,004 ; 1,110] | 0,995 | 0,0900 | non significatif |

## H2, l'ecart entre camps

| hypothese | modele | identite | perimetre | ecart decrit | ecart reel | facteur | IC 95 % | plancher | p Holm | verdict |
|---|---|---|---|---|---|---|---|---|---|---|
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | journaliste | tous les items | 0,189 | 0,211 | **0,894** | [0,766 ; 1,044] | 1,010 | 0,1552 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | adversaire | tous les items | 0,163 | 0,211 | **0,771** | [0,643 ; 0,921] | 1,011 | 0,1886 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Base | journaliste | tous les items | 0,128 | 0,210 | **0,610** | [0,468 ; 0,764] | 1,011 | 0,4632 | non significatif |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Base | adversaire | tous les items | 0,246 | 0,212 | **1,161** | [0,974 ; 1,369] | 1,014 | 0,0051 | amplification |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | journaliste | tous les items | 0,212 | 0,212 | **1,002** | [0,863 ; 1,149] | 1,011 | 0,0186 | significatif mais nul en pratique |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | adversaire | tous les items | 0,291 | 0,213 | **1,365** | [1,183 ; 1,560] | 1,012 | 0,0007 | amplification |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | journaliste | tous les items | 0,221 | 0,213 | **1,037** | [0,897 ; 1,185] | 1,010 | 0,0062 | significatif mais nul en pratique |
| H2a, ecart non signe (TV entre camps) | Qwen3-4B-Instruct-2507 | adversaire | tous les items | 0,269 | 0,213 | **1,265** | [1,099 ; 1,452] | 1,012 | 0,0004 | amplification |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | 79 items orientes | 0,059 | 0,241 | **0,245** | [0,056 ; 0,434] | 1,009 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | 79 items orientes | 0,053 | 0,241 | **0,221** | [0,064 ; 0,398] | 1,009 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Base | journaliste | 79 items orientes | 0,136 | 0,241 | **0,566** | [0,380 ; 0,785] | 1,009 | 0,0039 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Base | adversaire | 79 items orientes | 0,106 | 0,241 | **0,440** | [0,163 ; 0,728] | 1,009 | 0,0039 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | 79 items orientes | 0,175 | 0,241 | **0,727** | [0,482 ; 0,984] | 1,009 | 0,1248 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | 79 items orientes | 0,207 | 0,241 | **0,859** | [0,537 ; 1,193] | 1,009 | 0,3953 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | 79 items orientes | 0,151 | 0,241 | **0,627** | [0,385 ; 0,875] | 1,009 | 0,0340 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | 79 items orientes | 0,181 | 0,241 | **0,754** | [0,493 ; 1,036] | 1,009 | 0,1562 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | items retenus stricts | 0,079 | 0,259 | **0,304** | [0,114 ; 0,514] | 1,011 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | items retenus stricts | 0,070 | 0,259 | **0,270** | [0,089 ; 0,454] | 1,011 | 0,0004 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Base | journaliste | items retenus stricts | 0,148 | 0,259 | **0,574** | [0,371 ; 0,811] | 1,011 | 0,0087 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Base | adversaire | items retenus stricts | 0,123 | 0,259 | **0,476** | [0,183 ; 0,786] | 1,011 | 0,0127 | attenuation |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | items retenus stricts | 0,209 | 0,259 | **0,810** | [0,532 ; 1,092] | 1,011 | 0,5958 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | items retenus stricts | 0,254 | 0,259 | **0,982** | [0,638 ; 1,360] | 1,011 | 0,9213 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | journaliste | items retenus stricts | 0,183 | 0,259 | **0,708** | [0,437 ; 0,991] | 1,011 | 0,2362 | non significatif |
| H2b, ecart signe (position orientee) | Qwen3-4B-Instruct-2507 | adversaire | items retenus stricts | 0,209 | 0,259 | **0,808** | [0,513 ; 1,114] | 1,011 | 0,5958 | non significatif |

## H3, l'identite du demandeur

Distance entre le portrait fait au journaliste et celui fait a un membre du camp adverse, contre le plancher de reinterrogation humaine. Le centre est exclu, comme annonce.

| modele | camp | TV entre identites | plancher humain | rapport | IC 95 % | items identiques | p Holm |
|---|---|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | gauche | 0,073 | 0,024 | **3,074** | [2,377 ; 3,897] | 0,347 | 0,0004 |
| Qwen3-4B-Instruct-2507 | droite | 0,084 | 0,027 | **3,092** | [2,483 ; 3,791] | 0,272 | 0,0004 |
| Qwen3-4B-Base | gauche | 0,077 | 0,024 | **3,267** | [2,233 ; 4,420] | 0,528 | 0,0004 |
| Qwen3-4B-Base | droite | 0,137 | 0,027 | **5,048** | [3,923 ; 6,362] | 0,294 | 0,0004 |
| Qwen3-4B-Instruct-2507 | gauche | 0,081 | 0,024 | **3,373** | [2,687 ; 4,276] | 0,329 | 0,0004 |
| Qwen3-4B-Instruct-2507 | droite | 0,115 | 0,027 | **4,202** | [3,518 ; 4,997] | 0,188 | 0,0004 |
| Qwen3-4B-Instruct-2507 | gauche | 0,077 | 0,024 | **3,235** | [2,639 ; 3,924] | 0,262 | 0,0004 |
| Qwen3-4B-Instruct-2507 | droite | 0,079 | 0,027 | **2,925** | [2,437 ; 3,485] | 0,194 | 0,0004 |

## H4, les items a derive marquee

| modele | identite | quantite | rho de Spearman | n items | p Holm |
|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | journaliste | log amplification de l'ecart entre camps | **0,234** | 71 | 0,0880 |
| Qwen3-4B-Instruct-2507 | adversaire | log amplification de l'ecart entre camps | **0,269** | 61 | 0,0880 |
| Qwen3-4B-Base | journaliste | log amplification de l'ecart entre camps | **0,614** | 45 | 0,0040 |
| Qwen3-4B-Base | adversaire | log amplification de l'ecart entre camps | **0,297** | 66 | 0,0645 |
| Qwen3-4B-Instruct-2507 | journaliste | log amplification de l'ecart entre camps | **0,452** | 66 | 0,0040 |
| Qwen3-4B-Instruct-2507 | adversaire | log amplification de l'ecart entre camps | **0,440** | 77 | 0,0040 |
| Qwen3-4B-Instruct-2507 | journaliste | log amplification de l'ecart entre camps | **0,519** | 70 | 0,0040 |
| Qwen3-4B-Instruct-2507 | adversaire | log amplification de l'ecart entre camps | **0,514** | 75 | 0,0040 |
| Qwen3-4B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,635** | 79 | 0,0040 |
| Qwen3-4B-Instruct-2507 | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,649** | 79 | 0,0040 |
| Qwen3-4B-Base | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,628** | 79 | 0,0040 |
| Qwen3-4B-Base | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,627** | 79 | 0,0040 |
| Qwen3-4B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,641** | 79 | 0,0040 |
| Qwen3-4B-Instruct-2507 | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,628** | 79 | 0,0040 |
| Qwen3-4B-Instruct-2507 | journaliste | deficit d'unanimite 1 - GS decrit / GS reel | **-0,631** | 79 | 0,0040 |
| Qwen3-4B-Instruct-2507 | adversaire | deficit d'unanimite 1 - GS decrit / GS reel | **-0,656** | 79 | 0,0040 |

## Ce que ce resume ne dit pas

- Aucune croyance humaine de second ordre n'est mesuree ici : les items ANES ne sont pas dans ce run. La phrase « le modele exagere plus que les humains » est interdite.
- Le facteur de H2b n'est pas celui de `a38` : perimetre d'items et mode different, seuls le signe et l'ordre de grandeur se comparent.
- Rien ici ne porte hors du GSS, hors des Etats Unis, ni hors de ces trois modeles a cette quantification.
