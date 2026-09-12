# Correctifs artefact PoPETs — 12 septembre 2026

## Défaut 1 — plantage de `analyses/c7_temoin_verite_appariee.py`

**Cause réelle** : dans le bloc bonus « ANGLE 6 » (après les chiffres publiés), la fonction
locale `c_moyen` dimensionnait sa table de fréquences marginales `pm` sur `int(v.max())+1`,
où `v` sont les seules valeurs *observées* dans la colonne de référence `y_ref`. Mais
`faux_uniforme` peut fabriquer, pour les cellules fausses, des codes de catégorie jusqu'à
`k_items[j]-1` (toutes les catégories possibles de l'item), qui peuvent dépasser
`v.max()`. D'où `IndexError: index 5 is out of bounds for axis 0 with size 5`.

**Traitement : suppression, pas réparation**, avec preuve de redondance. Le bloc ANGLE 6
recalculait exactement ce que `analyses/c7_audit_decomposition.py` calcule déjà et imprime
sans erreur (même configuration `"JSON Persona - GPT4.1"`, mêmes graines `[GRAINE,12345]`
et `[GRAINE,12346]`, même algorithme `nul_exactitude_verite`/`nul`, identique à une
renomination de variables près). Preuve chiffrée : avant le plantage, la ligne « jumeau
REEL » de ce bloc imprimait `justes c=0.4776 (n=72901) | fausses c=0.3660 (n=50579)` —
strictement identique aux valeurs déjà publiées par `c7_audit_decomposition.py`
(`resultats/sauvetage-scripts-temoin-2026-09-12.md` §4.3). Le bloc a été retiré ; un
commentaire de provenance dans le fichier explique pourquoi et renvoie vers ce document.

**Confirmation après correction** (rejeu complet, avant-plan, ~150 s) : code de sortie 0,
plus aucune trace d'erreur, le script se termine par `termine 151s`.

| | Publié | Obtenu après correctif | Écart |
|---|---|---|---|
| rho, remplissage marginal | 0,9741 | **0,9741** | aucun |
| rho, remplissage uniforme | 0,9815 | **0,9815** | aucun |
| rho observé (référence) | 0,9650 | **0,9650** | aucun |

Aucune valeur publiée n'a changé, pas même à la dernière décimale.

## Défaut 2 — `analyses/c7_transfert.py` et le 26,11 %

**Correctif** : ajout, dans le « resume volet A », d'une ventilation par `n_items` calculée
sur `paires_riches` (déjà construit, aucun calcul modifié) ; l'agrégat mixte reste affiché
mais est désormais explicitement annoté « AGREGAT MIXTE 60+19 items -- ne pas citer ».

**Sortie après rejeu complet** (avant-plan, ~520 s, code de sortie 0) :

```
top1 moyen, paires riches (n=42) : 0.2611 (AGREGAT MIXTE 60+19 items -- ne pas citer, voir ventilation ci-dessous)
top1 moyen, paires riches, VENTILE PAR NOMBRE D'ITEMS COMMUNS (chiffres a citer) :
  n_items= 19 (n_paires=12) : top1 moyen=0.0045
  n_items= 60 (n_paires=30) : top1 moyen=0.3638
```

Conforme à l'article : 36,38 % (60 items) et 0,45 % (19 items). **L'agrégat 26,11 % reste
affiché**, mais annoté comme non citable — décision de suppression totale laissée à
l'utilisateur, comme demandé.

## Discipline

Aucune valeur publiée n'a bougé (rho 0,9741/0,9815/0,9650 ; ventilation 36,38 %/0,45 %) :
seule la lisibilité de la sortie a changé, dans les deux scripts.
