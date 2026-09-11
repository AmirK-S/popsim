# R6, revue adverse indépendante des sept pilotes

## Verdict

**GO-CAMPAGNE pour les quatre PASS déterministes: Mistral Small 2603, Qwen 3.7 Plus,
GLM-5 et Claude Haiku 4.5.** Les pilotes satisfont les critères enregistrés et aucune
modification du code, du modèle, du fournisseur, de l'invite, des cellules ou des règles
scientifiques n'est nécessaire pour les admettre en campagne.

Ce GO est un verdict de revue, pas une autorisation d'exécution. Le manifeste contrôlé est
limité aux pilotes, `data/traces/STOP-R6` est présent et `data/traces/GO-R6` est absent. Une
décision de campagne distincte doit donc fixer les plafonds par trace, conserver les
plafonds modèle existants et fournir le GO opérationnel attendu. Aucun de ces actes ne
doit changer la charge scientifique.

DeepSeek et Grok sont séparés des quatre PASS: leurs pilotes passent les critères de coût,
parse et raisonnement, mais ils sont non déterministes, avec respectivement 1/10 et 4/10
distributions exactement répétées. Le plan ne les retire pas pour ce motif. Il impose de
les marquer non déterministes et de ne lire A4 qu'avec le plancher machine. Kimi et Gemini
sont retirés et reçoivent un **NO-GO-CAMPAGNE**.

## Reconstruction indépendante

L'audit lit le manifeste READY de SHA-256
`dc7482c982df7fc80f1fd8298d1421cbe75ac0053dd5a211c2cf43c0b61028fc`, les traces JSONL,
les fichiers de cellules et le ledger append-only. Il ne fait aucun appel réseau et ne
réutilise pas les totaux du bilan comme données d'entrée.

Le ledger contient 143 réservations R6 au total. Pour les sept nouveaux pilotes, il en
contient exactement 123: 103 ont une réconciliation et 20, toutes Gemini, une annulation
prouvée `HTTP-404-sans-generation`. Après reconstruction de l'état final, aucune
réservation n'est ambiguë. Les 103 lignes de réponse et les 20 lignes Gemini non jouées
expliquent donc les **123 POST** sans reste ni doublon.

| modèle | réponses / POST | fournisseur imposé et observé | coût réglé USD | projection 1 270 | seuil 1,5 fois v2 | raisonnement moyen / max | rejets | exactes / 10 | décision |
|---|---:|---|---:|---:|---:|---:|---:|---:|---|
| Mistral Small 2603 | 20 / 20 | Mistral | 0,00059544 | 0,03781044 | 0,120 | 0 / 0 | 0 | 9 | PASS |
| Qwen 3.7 Plus | 20 / 20 | Alibaba | 0,00192640 | 0,12232640 | 0,240 | 0 / 0 | 0 | 8 | PASS |
| Kimi K2.5 | 3 / 3 | SiliconFlow | 0,02253195 | 9,53852550 | 0,345 | 3 285 / 3 835 | 0 | n.d. | retiré |
| GLM-5 | 20 / 20 | StreamLake | 0,00287376 | 0,18248376 | 0,420 | 0 / 0 | 0 | 9 | PASS |
| Gemini 3.8 Flash | 0 / 20 | Google AI Studio imposé, HTTP 404 | 0 | n.d. | 0,585 | n.d. | n.d. | n.d. | retiré |
| Claude Haiku 4.5 | 20 / 20 | Anthropic | 0 | 0 | 0,780 | 0 / 0 | 0 | 10 | PASS |
| Grok 4.3 | 20 / 20 | xAI | 0,00597700 | 0,37953950 | 0,825 | 0 / 0 | 0 | 4 | PASS non déterministe |

La projection est la moyenne du coût réglé des réponses multipliée par 1 270. Pour Haiku,
les vingt réponses ont toutes un identifiant de génération, `cout_source=annonce`,
`cout_annonce_usd=0` et `cout_appel_usd=0`: le zéro est bien la valeur annoncée par le
fournisseur, pas une valeur imputée en l'absence d'usage. À titre de contrôle conservateur,
la tarification maximale appliquée aux jetons observés donnerait 0,00636 USD pour le
pilote et 0,40386 USD projeté, encore sous le seuil de 0,780 USD. Gemini diffère: aucune
réponse n'a été acquise et les vingt réservations ont été annulées après HTTP 404; son coût
nul ne constitue pas une mesure de prix par réponse.

Les lignes de réponse déclarent toutes `reasoning=off`, `max_tokens=150`, le modèle attendu
et le fournisseur fixé. Les jetons de raisonnement sont nuls sauf pour Kimi. Aucun rejet de
parse n'apparaît dans les 103 réponses. Pour les cinq pilotes complets, les deux passes
portent les dix mêmes triplets item, camp et identité dans le même ordre.

## Cas d'arrêt et comptabilité

Kimi a réglé trois réponses à 0,00666630, 0,00874710 et 0,00711855 USD. Le cumul atteint
0,02253195 USD, au-dessus du plafond pilote de 0,02 USD, et les réponses comptent 2 915,
3 835 et 3 105 jetons de raisonnement malgré la désactivation demandée. Le ledger ne
contient que trois réservations Kimi. Le journal montre que le préflight suivant refuse la
cellule suivante avec `budget_pilote_epuise`; il n'existe donc ni quatrième réservation ni
quatrième POST. La dépense réelle supérieure à la réservation est conservée sans
troncature. Coût projeté et raisonnement dépassent chacun leur critère de retrait.

Gemini a reçu les dix mêmes cellules dans chacune des deux passes. Les vingt tentatives se
terminent en HTTP 404 non rejouable depuis le fournisseur imposé, sans réponse, fallback,
réconciliation payante ou ambiguïté. Son retrait est cohérent avec l'échec complet de la
voie fixée.

La somme indépendante des sept pilotes est **0,03390455 USD**. En ajoutant le pilote
DeepSeek antérieur, **0,0003289566 USD**, on retrouve exactement le total réglé R6 de
**0,0342335066 USD**. Les cinq GO des pilotes complets sont archivés comme consommés; les
GO Kimi et Gemini sont archivés avec leur motif de retrait. Grok reste explicitement non
déterministe et n'est pas reclassé comme retrait, conformément à la règle des 7/10.

## Portée du GO

Les quatre PASS déterministes peuvent entrer dans une préparation de campagne sans nouveau
pilote et sans modification scientifique ou logicielle. Leur exécution doit encore être
rendue concrète dans un manifeste de campagne revu, car le manifeste READY actuel ne
contient des commandes de campagne préparées que pour DeepSeek et son autorisation porte
sur les sept pilotes. Les plafonds modèle à conserver sont 0,12 USD pour Mistral, 0,24 pour
Qwen, 0,42 pour GLM-5 et 0,78 pour Haiku; les dépenses pilote déjà réglées doivent continuer
à les réduire.

DeepSeek et Grok restent admissibles selon le texte du plan, mais toute campagne les
concernant doit conserver leur marqueur non déterministe et l'usage du plancher machine
pour A4. Cette revue ne transforme pas leur instabilité en retrait et ne les agrège pas aux
quatre PASS déterministes. Kimi et Gemini restent exclus de toute campagne.
