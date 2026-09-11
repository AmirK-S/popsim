# C7 Stanford provenance, résultats : le 65,7 % n'est pas une recopie

Préenregistré dans `c7-stanford-provenance-preenregistrement.md`, calculé par
`analyses/c7_stanford_provenance.py`. **Aucun identifiant imprimé**, sorties agrégées
dans `resultats/c7-stanford-provenance-symetrie.csv`.

## 1. Documentation
`FIGURE2_PIPELINE.md` §6.1 : « Survey-Based » construite à partir des réponses d'enquête.
`analyze_gss_filtered.py` : l'agent répond lui-même à un GSS simulé, pas une recopie de
sortie. Article (arXiv 2411.10109) : enquête nourrie par « surveys including General
Social Survey items » — risque théorique, sans filtrage confirmé des items évalués.

## 2. Test de symétrie (décisif), cellules où l'humain a changé (34 915)
| condition | suit vague 1 | suit vague 2 | écart | verdict local |
|---|---|---|---|---|
| composite | 41,6 % [40,98;42,26] | 43,2 % [42,60;43,88] | **−1,6 pt** | pas de biais v1 |
| enquête | 42,8 % [42,21;43,40] | 38,2 % [37,62;38,86] | +4,6 pt | biais v1 réel |
| entretien | 43,5 % [42,84;44,10] | 38,6 % [37,91;39,23] | +4,9 pt | biais v1 réel |
| démographique | 41,9 % [41,27;42,47] | 37,6 % [36,99;38,19] | +4,3 pt | biais v1 réel |
| persona | 38,9 % [38,27;39,54] | 38,5 % [37,85;39,09] | +0,4 pt | pas de biais |

**Décisif** : le biais v1 (~4,3-4,9 pt) est du même ordre pour `démographique` (aucun
accès individuel) que pour `enquête`/`entretien`. Pas une signature de fuite, mais un
artefact de calibration partagé (vague 1 = cible partout dans le pipeline). Une recopie
ferait dépasser 43 % de loin sur des cellules où l'humain a justement changé d'avis ; ce
n'est pas le cas. `composite` (65,7 %) ne montre **aucun** biais v1 (écart négatif).

## 3. Décomposition (reprise de `c7-stanford-reidentification.csv`, non recalculée)
Entretien seul : **44,7 % [41,8;47,5]**, confirmé. Enquête seule : 20,6 %. Démographique :
2,3 %. Composite : 65,7 %.

## 4. Verdict
**Contamination par recopie directe exclue.** Le biais v1 sur trois conditions sur cinq
est un artefact de calibration partagé avec `démographique`, pas une fuite d'item.
Chiffre le plus défendable : **entretien seul (44,7 %)**, zéro exposition théorique à
l'enquête. `composite` (65,7 %) est aussi défendable par ce test, mais garde une
exposition documentaire jamais observée en pratique.

## 5. En clair
L'agent qui a "vu" l'enquête ne recopie pas la réponse de vague 1 plus qu'un agent qui
n'a que l'âge et le genre. Les deux tiers de ré-identification tiennent sur un vrai style
de réponse, pas sur une antisèche.
