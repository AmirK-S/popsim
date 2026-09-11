# Twin A→B : résultat préenregistré

## Verdict

**Revendication d'utilité du diagnostic FERMÉE.** Le choix par diagnostic (résidu de régression chute~exactitude) ne fait pas mieux que le choix par exactitude A : il fait significativement **moins bien**. Au principal, Delta = perte_B(diagnostic) − perte_B(exactitude) = **+0,0266**, IC 95 % **[+0,0026 ; +0,0412]**, entièrement positif. R1 (Delta ≤ −0,01), R2 (borne haute < 0), R3 (signe négatif par famille) et R4 (PMM ≤ c_diag) sont **tous faux** : aucun ne va dans le sens attendu par la revendication, et R2 échoue dans la direction opposée (l'IC entier est positif, pas seulement non négatif).

## Tableau

| Analyse | Rotation | c_diag | c_exa | Delta_r | perte_B(c_diag) | perte_B(PMM k=10) |
|---|---|---|---|---|---|---|
| Principal | 1 | Text Persona - Gemini-Flash2.5 | JSON Persona - GPT4.1 | +0,031 | 0,330 | 0,372 |
| Principal | 2 | Text Persona - Gemini-Flash2.5 | JSON Persona - GPT4.1 | +0,023 | 0,324 | 0,382 |
| Principal | 3 | Text Persona - Gemini-Flash2.5 | JSON Persona - GPT4.1 | +0,025 | 0,325 | 0,416 |
| Principal | Delta (IC 95 %) | — | — | **+0,0266** | [+0,0026 ; +0,0412] | statut ferme |
| S1 (1 000 pers.) | Delta (IC 95 %) | — | — | **+0,0208** | [+0,0002 ; +0,0411] | statut ferme, affaibli_sans Product Preferences - Pricing |

Sur les trois rotations, `perte_B(c_diag)` (≈0,324-0,330) est inférieure à `perte_B(PMM k=10)` (≈0,372-0,416) : le contrôle R4 échoue parce que PMM perd *plus*, pas moins, que la configuration choisie par diagnostic — donc R4 ne ferme pas non plus dans le sens qui sauverait la revendication.

## Constat descriptif (pas une revendication)

Sur ce périmètre, les configurations LLM riches (Text Persona - Gemini-Flash2.5, JSON Persona - GPT4.1) ont une perte B inférieure à PMM et aux autres baselines. Ce constat ne participe à aucune règle de décision R1-R4 et ne fonde aucune affirmation de supériorité générale.

## Lien avec la fragilité L15

La limite L15 du préenregistrement notait qu'avec sept candidates, un point de levier sur `exa_A` peut faire pivoter la régression du résidu et désigner comme « diagnostic » une configuration moins exacte. Ici, le diagnostic choisit systématiquement Gemini-Flash2.5 (moins exact sur A) plutôt que GPT4.1 JSON (plus exact sur A et meilleur sur B). C'est une lecture cohérente avec L15, **pas une explication qui sauve la revendication** : le jackknife L15 est un diagnostic de sensibilité descriptif publié à part (`tab-secondaires.csv`), il ne rouvre pas la règle de chute ni ne change le statut « ferme ». Aucune analyse de rattrapage n'a été menée.

## Implication pour l'article

On garde la dissociation des mesures (exactitude A et perte B ne se substituent pas l'une à l'autre) mais on retire toute prétention à guider, via le diagnostic de chute résidualisée, le choix d'une configuration de simulateur.

## Exécution

B = 2 000 réplicats bootstrap (principal + S1). Préenregistrement commité `e051c69` le 11 septembre 2026 à 16:26, antérieur à l'exécution ; sorties `tab-*.csv`/`tab-execution.log` écrites à 16:58 le même jour, soit environ 32 minutes d'exécution totale (dont ~287 s cumulées sur les 5 plis du contrôle de reproduction R).
