# R6 — arrêt conditionnel du pilote post-OSF

Le 10 septembre 2026, après confirmation par le parent de l'archivage de la registration
OSF `https://osf.io/abf7y/overview`, le client R6 unique a lancé l'essai gratuit Nvidia de
10 cellules prévu avant DeepSeek. Le code, le plan, le manifeste, le registre et les listes
avaient été figés par SHA-256 avant l'appel.

Le client a écrit une première réponse valide, sans rejet, avec un coût annoncé de 0 USD.
La deuxième cellule a rencontré un HTTP 502 sans identifiant de génération. La même clé a
ensuite été établie par le mtime inchangé de `.env` et par `GET /key` : usage 0, limite et
restant 4,40 USD, sans reset. La fiche de la génération réussie confirmait aussi un coût nul.
Le marqueur initial a été archivé à empreinte identique avec cette réconciliation.

La reprise a utilisé exactement la même trace, liste, configuration et cellule : aucune
réponse n'a été rejouée. La cellule précédemment échouée a abouti à coût nul, puis la cellule
suivante a rendu un second HTTP 502 sans identifiant. Ce nouvel incident conserve son
marqueur `.en-cours`; l'ambiguïté de transport persiste et les appels modèle s'arrêtent.

| mesure | résultat |
|---|---:|
| cellules demandées | 10 |
| tentatives totales sur les deux exécutions | 4 |
| réponses uniques écrites | 2 |
| rejets de parse | 0 |
| incidents de transport | 2 × HTTP 502 |
| coût annoncé des réponses | 0 USD |
| coût observé de l'incident | inconnu |
| coût total attribuable à la même clé | 0 USD (`GET /key`) |
| essai propre | non |
| réconciliation requise | oui |

Le compte affiche 149,221451045 USD utilisés, soit 5,778548955 USD restants. Il n'est pas
utilisé pour attribuer une variation à R6. Les deux générations réussies ont chacune une
fiche de facturation à 0 USD. Le registre global n'a pas changé et garde son empreinte
`0ab9093c34c68ad51668d66183f3dd1fb7ba15a98540417014d67940fe5647dd`.

Le critère de poursuite n'est pas satisfait : l'essai est incomplet et une issue de
transport reste sans identifiant de génération. L'API de métadonnées de facturation exige
cet identifiant ; le client actuel ne conserve pas l'éventuel en-tête `X-Generation-Id`
d'une réponse HTTP en erreur. Aucun appel DeepSeek, aucune passe F1/F2 et aucun plancher
machine n'ont été lancés. `GO-R6` a été retiré et archivé de façon récupérable. Le plan OSF
n'a pas été modifié.
