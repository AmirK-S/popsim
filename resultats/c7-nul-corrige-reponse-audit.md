# Réponse à l'audit adverse du renversement C7 — 12 septembre 2026

## VERDICT EN UNE LIGNE

**Mon renversement tombe.** L'auditeur a raison sur la charge décisive : mes cinq témoins
détruisent l'exactitude contre la vérité (0,407–0,436 contre 0,527), donc précisément la
grandeur dont l'objection affirme qu'elle explique tout ; j'ai vérifié son témoin et il
reproduit le couplage. La réfutation publiée **tient**, les six modifications du §7 de
`c7-nul-corrige-resultats.md` doivent rester **gelées**, et « Issue B / thèse soutenue »
est **retiré**.

---

## 1. Charge principale : mes constructions préservent-elles l'exactitude par personne ?

**Non. Vérifié dans mes données, pas dans mon intention.** Moyenne sur les 12 configurations
de `exactitude_contre_verite`, colonne de mon propre `c7-nul-corrige.csv` :

| construction | exactitude contre la vérité | écart au réel |
|---|---|---|
| prédicteur réel | 0,5274 | — |
| N0 nul cassé | 0,5274 | **0,0000** |
| N1 / N1b mode de segment | 0,4238 | **−0,1037** |
| N2 / N2b vecteur d'autrui | 0,4066 / 0,4068 | **−0,1208** |
| N3 identités permutées | 0,4364 | **−0,0910** |

Le chiffre était dans mon CSV et dans le tableau que j'ai moi-même imprimé ; je ne l'ai pas
traité comme disqualifiant. Il l'est. Mes témoins apparient q_i contre une **cible de
substitution**, et l'exactitude contre la **vérité** — la seule qui soit l'objet de
l'objection — s'effondre de 0,10 à 0,12. Un nul qui supprime la variable explicative
candidate ne peut pas réfuter l'explication par cette variable. **Concédé sans réserve.**

## 2. Son témoin est-il correct ? Je l'ai reconstruit et mesuré

Construction : effectif exact de cellules justes **contre la vérité**, positions tirées
uniformément, cellules fausses tirées dans la **marginale de population** avec rejet sur la
vraie valeur (ce qui purge le défaut de la ligne 133). *Réduction déclarée : 10 réplicats au
lieu de 100, bits sur 1 réplicat ; script `scratchpad/verif_audit.py`, ~90 s, avant-plan.*

| témoin à exactitude-vérité appariée | rho moyen | médiane | p5 | p95 | rho réel 0,965 le dépasse ? |
|---|---|---|---|---|---|
| remplissage marginal (l. 133 corrigée) | **0,9776** | 0,9790 | 0,9510 | 1,0000 | **non** |
| remplissage uniforme | 0,9853 | 0,9930 | 0,9682 | 0,9969 | **non** |

**Contrôle non trivial, celui qui manquait au mien** : `max |exactitude(out_i, y_i) − q_i|`
= **0,000000 pour les douze configurations**. Son témoin apparie l'exactitude contre la
vérité exactement, par personne et par configuration — ce que mes N1/N2/N3 ne font pas.

Ses chiffres sont reproduits à la précision du nombre de réplicats près (il annonce 0,9741,
je mesure 0,9776 sur 10 réplicats ; il annonce 31,62 % de top-1 pour JSON Persona 4.1, je
mesure 31,15 %). **Sa construction est correcte et son verdict est le bon : la prédiction (b)
reste réfutée.** Le renversement que j'ai publié n'était pas la conséquence de la réparation
d'un défaut, mais d'un **changement de nul**. Il a raison de le dire ainsi.

## 3. L'objection épistémique : je l'avais écrite contre moi et j'ai publié quand même

C'est le point le plus grave et je le reconnais entièrement. Le §8 de mon préenregistrement
disait qu'un nul correct détruit les deux axes, donc que le dépasser était « presque acquis
d'avance ». L'auditeur le chiffre : sous mes nuls, la dispersion inter-configuration est plus
petite que le bruit d'une seule configuration (0,16–0,23 contre 7,5 pour le réel), et leurs
95es centiles (0,547–0,594) sont ceux du Spearman sous H0 à n = 12 (0,497). Mon test se
réduisait à « rho ≠ 0 », déjà établi à p = 3,9·10⁻⁷. **Un test qui ne peut pas échouer ne
démontre rien.** Mon garde-fou (`len(set(...)) < 2`, axe exactement constant) ne pouvait
jamais se déclencher sur du bruit continu : le 0/100 annoncé est exact et vide. Le bon
garde-fou était le sien — dispersion inter-configuration contre bruit intra.

## 4. Ce que je maintiens, et qui n'est pas une défense de mon résultat

Un seul point, et il ne sauve rien : **le témoin à exactitude appariée n'est pas « sans
empreinte individuelle »**, et l'article ne peut pas continuer à le décrire ainsi. Mesuré
sur son propre témoin, remplissage marginal, défaut l. 133 purgé (JSON Persona 4.1) :
**top-1 31,15 %, 4,63 bits d'identité** — contre 20,73 % et 3,56 bits pour le jumeau réel, et
0,049 % pour le hasard. Un objet qui désigne la bonne personne dans 2 058 une fois sur trois
porte de l'information individuelle, par toute définition opérationnelle.

La phrase du résumé (l. 26-27) — « 100 predictors carrying only a per-person accuracy margin
and **no individual structure at all** » — est donc **factuellement fausse**, indépendamment
du verdict. Ce n'est pas un désaccord avec l'auditeur : **sa propre « phrase exacte » ne
l'emploie pas**, elle dit « une exactitude par personne appariée et des positions exactes
tirées au hasard ». Nous convergeons. Le verdict est le sien ; seule la description de
l'objet doit être corrigée, et sa formulation le fait déjà.

Sur ligne 133 contre 134 : je me range à son analyse. Fixer une exactitude par personne
**exige** d'écrire la vraie réponse sur k_i positions ; ce n'est pas un défaut. Je note
seulement, sans en tirer de verdict, que l'essentiel de la fuite vient de cette copie et non
de la l. 133 (31,1 % subsistent des 39,5 % une fois la l. 133 purgée) — ce qui est
exactement pourquoi l'objet ne peut pas être appelé « sans empreinte ». Question de nom,
pas de verdict.

## 5. Défauts secondaires : concédés

* **Défaut 3 — contrôle vacant.** Exact et tautologique : je mesurais l'exactitude contre la
  cible de substitution que je venais d'écrire. `ecart_max = 0,0000` ne pouvait pas échouer.
  Le contrôle contre la **vérité** aurait fait apparaître le défaut 1 tout seul. C'est la
  leçon de méthode la plus utile de cet audit : j'avais préenregistré un contrôle qui validait
  l'échantillonneur, pas l'appariement de la grandeur sous test.
* **Défaut 4 — mécanisme du « minorant » faux.** Sa décomposition de c par type de cellule
  (juste 0,478 contre 0,433 ; fausse 0,366 contre 0,376) démontre que l'écart vient des
  cellules **justes** : le jumeau réel a raison préférentiellement sur les items banals. Ma
  phrase « le jumeau converge vers la moyenne là où il se trompe » est **démentie par la
  mesure** ; je la retire. Le fait (un témoin synthétique à exactitude égale fuit 1,5 à 1,9
  fois plus) tient, et je l'ai reproduit une troisième fois ici (31,1 % et 39,5 % contre
  20,7 %). « Minorant » est mal nommé : c'est une **borne de ce que l'attaque extrait à
  exactitude donnée**, pas de ce qu'un générateur peut produire.
* **Défaut 5 — seuil z.** Ajustement postérieur, déclaré. J'ajoute la phrase qu'il demande :
  **le verdict est inchangé au seuil préenregistré de 5**, trois témoins sur cinq le passant.
* **Défaut 6 — N1 fuit un peu (0,063 % contre 0,0486 %).** Confirmé ; N2 reste le meilleur
  plancher, ce qui ne change rien au verdict.
* **Défaut 7 — descriptif.** (a) rho porte sur **12** points, pas 13 : `spearman12` n'utilise
  que `noms_12`, le retest humain est calculé et exclu ; le tableau §4 en montre 13 et prête
  à confusion, à préciser. (b) Le chemin de cache codé en dur aux l. 108-111 de
  `analyses/c7_nul_corrige.py` est propre à cette session : l'identité bit à bit n'est
  vérifiable qu'ici. Défaut réel de reproductibilité.

## 6. Ce qui survit de mon travail

Sans plaidoyer, et rien au-delà : le **tableau du §4** (top-1, bits et IC **par
configuration**, que la boucle des lignes 221-235 de `c7_disjoint.py` calculait et jetait) —
apport non contesté par l'audit ; la **reproductibilité bit à bit**, vérifiée
indépendamment ; le fait que le défaut l. 133 est réel ; et l'arbitrage N2 sur N1. Le reste
— Issue B, « thèse soutenue faiblement », les six modifications de l'article — est retiré.

## 7. Ce que l'article doit faire

1. **Geler les six modifications** du §7 de `c7-nul-corrige-resultats.md`. Ne pas changer le
   titre. Ne pas rebasculer la figure 2 sur `construction == "N2 vecteur d'autrui"` : cette
   bande est celle d'un nul sans information, que le point observé dépasse trivialement.
   Conserver « seize prédictions réfutées ».
2. **Adopter la « phrase exacte » du §final de l'audit**, qui est correcte et que j'endosse.
3. **Corriger la seule description fausse** : remplacer « no individual structure at all »
   (résumé l. 26-27, et formulations parallèles en §1.1 et §5.1) par la description exacte de
   l'objet — « des prédicteurs dont l'exactitude par personne est appariée à celle du jumeau
   et dont les positions exactes sont tirées au hasard » — en notant que ce témoin fuit
   **davantage** que le jumeau réel (31,1 % contre 20,7 %, 4,63 bits contre 3,56). Cela
   renforce la réfutation au lieu de l'affaiblir : le témoin est un adversaire plus fort que
   nos jumeaux, pas un prédicteur inerte.
4. **Publier le témoin à exactitude-vérité appariée, remplissage marginal**, comme témoin
   principal, et N1–N3 comme plancher « aucune information individuelle », utile mais non
   probant sur l'objection d'exactitude.

Je n'ai modifié ni `c7-nul-corrige-resultats.md`, ni le manuscrit, ni `article-synthese.md`,
ni `figures_article.py`, ni le rapport d'audit. Aucun commit. Lecture seule sur `data/`,
aucun appel de modèle, aucun réseau.
