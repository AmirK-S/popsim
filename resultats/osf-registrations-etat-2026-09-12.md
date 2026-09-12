# État des Registrations OSF — hm9wn, consultation du 12 septembre 2026

Consultation en lecture seule du projet OSF privé `https://osf.io/hm9wn/` (« popsim : auditer ce
que les modèles de langage disent des opinions »), compte du responsable. Aucune action
d'écriture n'a été effectuée sur OSF (aucun clic sur Register/Create registration/Make
public/Delete). Lecture faite via l'onglet Registrations de l'interface et via l'API OSF en
lecture seule (`api.osf.io/v2/nodes/hm9wn/registrations/`), qui expose notamment les champs
`public`, `embargoed`, `embargo_end_date`, `pending_registration_approval`, `reviews_state`.

Le nœud `t6g7k` (archive Stanford) n'a pas été touché.

## Constat de premier ordre : 8 Registrations, aucune ne porte sur C7

Le projet `hm9wn` contient **8 Registrations**, toutes créées par Amir KELLOU SIDHOUM
(`/user/hteq7`). Contrairement à ce qui m'a été rapporté en amont (Registrations « des 10, 11 et
12 septembre »), les dates réelles vues à l'écran et dans l'API sont **9 et 10 septembre
2026 uniquement** — aucune n'est du 11 ni du 12. Je signale cet écart tel quel plutôt que de le
laisser passer.

**Aucune des 8 ne concerne le chantier C7** (réidentification par jumeau / Twin-2K-500,
l'article visé par `resultats/preenregistrements-recueil-2026-09-12.md`). Les 8 portent toutes
sur un chantier voisin : l'oracle des camps politiques R5/R6 (fidélité de représentation des
camps par des modèles de langage) et un plan R7 (comparaison de checkpoints OLMo 3). Aucun
titre, aucune description, aucun texte de contenu lu n'emploie les mots « jumeau », « Twin »,
« réidentification », « C7 », « réfutations » ou « deux organisations ».

## Liste détaillée

| # | Titre | Identifiant | URL | Créée le | Statut |
|---|---|---|---|---|---|
| 1 | popsim, pages de plan r5 et r6, 9 septembre 2026 | `3r6zg` | https://osf.io/3r6zg/ | 9 sept. 2026, 12:20:15 | **Publique**, acceptée (`reviews_state: accepted`), `public: true`, non embargoée |
| 2 | popsim, addendum R6 PREPARE-4, 10 septembre 2026 | `6yj8x` | https://osf.io/6yj8x/ | 10 sept. 2026, 23:17:20 | **Privée**, en attente d'approbation (`pending_registration_approval: true`, `reviews_state: initial`), `public: false` |
| 3 | popsim R6 : addendum prospectif corrigé du préflight financier | `k5qfh` | https://osf.io/k5qfh/ | 10 sept. 2026, 22:07:14 | **Privée**, en attente, `public: false` |
| 4 | popsim R6 : addendum prospectif sur le plafond effectif du préflight | `m5nwp` | https://osf.io/m5nwp/ | 10 sept. 2026, 21:55:42 | **Privée**, en attente, `public: false` |
| 5 | popsim R6 : addendum prospectif de prix avant POST | `r72pj` | https://osf.io/r72pj/ | 10 sept. 2026, 21:43:07 | **Privée**, en attente, `public: false` |
| 6 | popsim R6 : addendum prospectif avant appels payants et modèles fermés | `kmqnw` | https://osf.io/kmqnw/ | 10 sept. 2026, 21:34:57 | **Privée**, en attente, `public: false` |
| 7 | popsim R6 : représentation des camps par API, protocole v2 et reprise | `abf7y` | https://osf.io/abf7y/ | 10 sept. 2026, 19:03:18 | **Privée**, en attente, `public: false` |
| 8 | popsim R7 : comparaison descriptive de checkpoints OLMo 3, plan corrigé | `vt2hk` | https://osf.io/vt2hk/ | 10 sept. 2026, 18:18:57 | **Privée**, en attente, `public: false` |

Pour les 7 privées : `embargoed: false` et `embargo_end_date: null` dans les 7 cas — ce ne sont
pas des embargos programmés, ce sont des Registrations dont la révision OSF interne
(« pending_registration_approval ») n'a jamais été validée. Elles ne s'ouvriront donc pas
automatiquement à une date connue ; il faudrait une action du responsable (soumission/validation)
pour qu'elles deviennent publiques. Aucune n'est retirée (`withdrawn: false` partout).

## Contenu réel (lu, pas seulement le titre)

- **#1 `3r6zg` (seule publique)** — Open-Ended Registration. Contient les pages de plan r5 (effet
  gabarit ChatML + trois exemples) et r6 (oracle des camps sur modèles frontière), avec
  hypothèses H1-H4 chiffrées (seuils 0,15 ; 0,3 ; facteur 2), budget prévisionnel (3-12 EUR,
  plafond 25 EUR), et un lien vers `Data/Analytic Code/Materials/Papers/Supplements` — mais
  `has_data`, `has_analytic_code`, `has_materials`, `has_papers`, `has_supplements` sont tous
  `false` dans l'API : ces catégories de ressources sont vides, aucun fichier n'y est réellement
  figé. C'est un texte de plan, pas un dépôt de résultats.
- **#2, #3, #4, #5, #6** — une série d'addenda techniques R6 (garde financière, plafond effectif
  par appel, prix avant POST, runner pilote, compatibilité fournisseur/modèle). Prédictions
  chiffrées présentes mais toutes opérationnelles/budgétaires (plafonds en USD, nombre de tests
  qui passent), aucune prédiction scientifique chiffrée de type « top-1 ≥ X % ».
- **#7 `abf7y`** — le protocole R6 v2 assemblé, avec H1 (dispersion intermodèles, facteur ≥2),
  H2 (dépendance au demandeur, borne >2, 4/5 modèles), H3a/H3b (contraste format ≥ ou = +0,30 sur
  3/5), H4 (palier tarifaire). Prédictions chiffrées écrites avant calcul, mais sur le sujet
  « camps politiques », sans rapport avec C7.
- **#8 `vt2hk`** — plan R7, comparaison descriptive de 4 checkpoints OLMo 3 Instruct 7B, explicitement
  non causal.

## Comparaison avec `resultats/preenregistrements-recueil-2026-09-12.md`

Ce recueil dénombre 59 préenregistrements locaux, dont 35 pour le Tier 1 C7 (le chantier de
réidentification par jumeau) — y compris les points chauds : le compteur de réfutations réel
(actuellement **14**, après le retrait de la réfutation `c7-deux-organisations` et de
`c7-factoriel`, requalifiées « non testables ») et le scénario « deux organisations » (verdict
final : **non testable**, pas réfuté). **Aucun de ces 35 préenregistrements C7, ni leurs
résultats, ni ce compteur, ni ce verdict ne figurent dans les 8 Registrations OSF.** Il n'y a donc
rien de périmé à signaler *dans les Registrations elles-mêmes* sur ces points précis, puisqu'elles
ne les abordent tout simplement pas — le risque n'est pas qu'une Registration porte un chiffre
faux, mais qu'aucune Registration ne porte encore ces chiffres du tout.

## Verdict

**Le dépôt horodaté du dossier anti-p-hacking C7 (réidentification par jumeau) reste entièrement
à faire.** Les 8 Registrations existantes appartiennent à un chantier différent (oracle des camps
R5/R6/R7), sont pour 7 d'entre elles privées et non encore approuvées par OSF (pas d'embargo
programmé, juste en attente), et la seule publique (`3r6zg`) ne contient que des pages de plan
sans fichiers de résultats attachés. Aucune trace du compteur de réfutations, du scénario « deux
organisations », ni d'aucun résultat C7 n'existe sur OSF à ce jour.
