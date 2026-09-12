# C7-utilite-aval, resultats : ce que D4 casse dans une analyse reelle

Preenregistre dans `c7-utilite-aval-preenregistrement.md`, calcule par
`analyses/c7_utilite_aval.py` (graine 20260912, `JSON Persona - GPT4.1`, 2 058 personnes,
0 manquant). Humains v4 / jumeau brut / jumeau D4.

## A. Groupes (H-F, item d'achat n°1) | B. Regression (`5_Q295`~genre+age65+n°1+n°2)
| | ecart H-F (A) | signif. A | achat n°1 (B) | achat n°2 (B) |
|---|---|---|---|---|
| humains | -0,047 | **oui** | +0,046 (p<.05) | +0,047 (p<.05) |
| jumeau brut | +0,010 | non | +0,060 (p<.01) | +0,073 (p<.001) |
| jumeau D4 | +0,010 | non | +0,016 (n.s.) | +0,015 (n.s.) |

A, brut vs D4 : identite exacte a 16 decimales (permuter dans `S_gra` ne change aucune
moyenne de groupe) — mais le brut se trompait deja de signe face aux humains, avant D4.
B, coefficients demographiques (genre, age) : signe/significativite stables brut->D4
(tous deux non significatifs dans les trois conditions, sauf bruit de signe deja present
brut vs humains). B, coefficients d'achat : **significatifs chez le jumeau brut,
non significatifs apres D4** — D4 efface deux effets reellement publiables, la ou
l'erreur de depart ne portait que sur des coefficients deja non significatifs.

## C. ACP (40 items d'achat, part des 2 premiers axes)
| condition | part PC1+PC2 | loadings PC1 inverses vs humains |
|---|---|---|
| humains | 15,0 % | - |
| jumeau brut | 9,8 % | 0 % |
| jumeau D4 | 6,3 % | 45 % |

Ecart humains->brut : 5,3 points, deja substantiel. Ecart brut->D4 : 3,5 points ajoutes,
plus petit que l'ecart de depart (prediction 4 confirmee sur la variance) — mais le brut
gardait les bons items sur l'axe 1 (0 % d'inversion), tandis que D4 en inverse 45 % : il
change surtout QUELS items composent la structure, plus que sa force globale.

## Verdict et recommandation
Predictions 1 et 3 confirmees ; prediction 2 partielle (perte de significativite 2/2,
aucun changement de signe) ; prediction 4 confirmee sur la variance, contredite sur les
loadings (D4 est le principal responsable du changement de composition de l'axe).
Avec un jumeau D4 : groupes et regressions a dominante demographique restent fiables.
Devient inexploitable : tout ce qui repose sur le lien entre deux achats d'une meme
personne (regression inter-items, composition d'un axe d'ACP), meme quand la variance
totale expliquee ne s'effondre pas plus que l'erreur de depart du jumeau.

**En clair** : D4 ne ment jamais sur les groupes demographiques, mais rend muet tout ce
qui reliait deux achats d'une meme personne — et le jumeau non protege se trompait deja
ailleurs, avant meme la defense.
