# C7, troisième jeu de nature différente : inventaire de faisabilité (12 septembre 2026)

Question posée : notre canal de fuite (C7) est-il une propriété de la **famille** Twin-2K-500 /
archive Park et al. (deux panels d'enquête américains, instruments GSS et Big Five, même
milieu), ou un fait plus général ? Recherche d'un troisième jeu, de nature différente, avec
vraies réponses ET sorties simulées pour les mêmes personnes.

## Candidats examinés localement

| candidat | réponses humaines + jumeaux pour les mêmes personnes ? | appariable sans identifiant direct ? | licence : calcul local + agrégat publiable ? | nature vraiment différente ? |
|---|---|---|---|---|
| `data/gss-panel` (4 panels réels 2006-2020) | non ; aucune sortie simulée existante | oui (index de panel) | oui (NORC : lecture et agrégats, `resultats/licences-sources-verification-2026-09-11.md`) | **non** — c'est le GSS lui-même, l'instrument que le relecteur cite déjà |
| `data/sce-fed-ny` (82 535 obs., 70 mois, `userid` stable) | non ; aucune sortie simulée existante | oui, `userid` stable, sans PII | oui, redistribution et dérivés autorisés (licence confirmée) | oui — institution (Fed NY) et instrument (anticipations chiffrées) distincts du GSS/Big Five |
| `data/ahler-sood-pcomp` (YouGov n≈1000, CC0) | non ; `a46_ahler_sood.py` ne calcule que des agrégats de perception, pas de jumeau par personne | oui, pas d'identifiant, CC0 | oui, CC0 sans restriction | oui — psychologie politique de la perception de composition partisane, autre équipe (Dartmouth/Duke), autre plateforme (YouGov/MTurk) |
| `data/westwood-pnas-2025` | sorties synthétiques seules, **aucun fichier humain apparié** (déjà noté dans sa `PROVENANCE.md`) | sans objet | sans objet | disqualifié : pas de vérité terrain humaine |
| `data/norc-mode` | agrégats par item seulement, aucune ligne individuelle | non, ce n'est pas de la donnée individuelle | oui | disqualifié : rien à ré-identifier |
| `data/anes-codebooks` | aucune microdonnée locale, seulement des codebooks | sans objet | sans objet | disqualifié : pas de données |

## Verdict

**Aucun candidat ne convient tel quel.** SCE et Ahler-Sood sont bien de nature différente et
légalement publiables en agrégat, mais aucun des deux n'a de sorties simulées existantes pour
ses répondants : il faudrait les fabriquer nous-mêmes (agents locaux, comme `a5`/`a11`/`a46`
l'ont fait pour le GSS et Twin), ce qui introduit un nouveau confondu — notre méthode de
génération et nos modèles locaux, différents de ceux de Twin-2K-500 et de Park et al. — au lieu
de tester la généralité du phénomène sur des jumeaux produits indépendamment. Ce n'est donc pas
un test à nombre d'items comparable au sens du protocole demandé, et je m'arrête ici plutôt que
de forcer un calcul qui répondrait à une autre question.

Ressource manquante à nommer dans les limites de l'article : un jeu individuel, d'un domaine
distinct du GSS/Big Five (santé, consommation, élections), pour lequel des jumeaux LLM produits
par une équipe tierce (pas nous) existent déjà pour les mêmes répondants, avec licence permettant
un calcul local et la publication d'un taux agrégé.

**En clair.** On n'a pas trouvé, dans ce qu'on a déjà sur la machine, un troisième jeu de données
différent qui ait à la fois des vraies réponses de gens et des réponses fabriquées par une IA
pour ces mêmes gens ; on le dit dans les limites de l'article plutôt que d'inventer un test qui
ne prouverait pas ce qu'on veut prouver.
