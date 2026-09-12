# Antériorité « linkability » : Anonymeter et ZAK-MIA (vérification à la source)

Sources lues intégralement (PDF récupérés et lus page par page, pas de résumé de tiers) :
- Anonymeter : https://petsymposium.org/popets/2023/popets-2023-0055.pdf (PoPETs 2023(2):312-328, DOI 10.56553/popets-2023-0055) — 17 pages, lues intégralement (pages 1-10 pertinentes citées ci-dessous).
- ZAK-MIA : https://petsymposium.org/popets/2024/popets-2024-0108.pdf (PoPETs 2024(4):80-101, DOI 10.56553/popets-2024-0108) — 22 pages, pages 1-3 lues (titre, résumé, définitions, section 2 « Definitions and Threat Model »).

## 1. Anonymeter — définition de la « linkability »

Citation exacte, section 5.2, page 319 :

> « The linkability attack tries to solve the following task: "Given two disjoint sets of original attributes, use the synthetic dataset to determine whether or not they belong to the same individual." »

Réponse à la question posée : **oui, sans ambiguïté**. L'attaquant tient des collections de cibles `T` tirées de `X_ori` (le jeu original réel), et connaît « the values of the attributes in datasets A and B: T[:,A] and T[:,B] » (p. 319, § Attack Phase) — donc des **valeurs réelles** d'attributs de la personne. La liaison se fait entre deux partitions d'attributs (A et B) d'un **même** jeu de données original (`X_ori`), via le jeu synthétique servant d'intermédiaire (Table 1, p. 319, schématise deux « external datasets A and B » qui sont chacun un sous-ensemble d'attributs partageant les mêmes individus que l'original). Ce n'est donc pas une liaison entre deux sorties synthétiques indépendantes : c'est original (scindé en deux vues d'attributs) → synthétique comme pivot. Notre travail (liaison entre deux sorties de jumeaux synthétiques, sans valeurs réelles connues de l'attaquant) diffère bien de ce cadre.

Classement des trois risques — citations exactes :
- Résumé, p. 312 : « we observe that synthetic data exhibits the lowest vulnerability against linkability, indicating one-to-one relationships between real and synthetic data records are not preserved. »
- Section 6.1, p. 320-321 : « in our experiments (Section 6.3), synthetic data exhibits the highest risks to inference and singling out attacks, whereas the risk to linkability is comparably low over all datasets evaluated. »

Confirmé : Anonymeter classe la **linkability comme le risque le plus faible** des trois (singling out, linkability, inference).

## 2. ZAK-MIA

Identifié avec certitude — le sigle correspond au titre du papier (Zero Auxiliary Knowledge → ZAK), même si les auteurs l'abrègent eux-mêmes « ZK MIA » dans le texte :

- **Titre complet** : « A Zero Auxiliary Knowledge Membership Inference Attack on Aggregate Location Data »
- **Auteurs** : Vincent Guan, Florent Guépin (Imperial College London), Ana-Maria Cretu (EPFL), Yves-Alexandre de Montjoye (Imperial College London)
- **Venue** : Proceedings on Privacy Enhancing Technologies 2024(4):80-101
- **DOI** : 10.56553/popets-2024-0108

Nature de l'attaque (lu section 1 Introduction et section 2.3-2.4, p. 80-82) : c'est une **attaque d'appartenance (membership inference)**, pas une liaison. Citation, p. 82 (§ 2.3 Problem Formulation) : « The goal of an adversary Adv performing an MIA on Ā^U is to determine whether their target user u* contributed to Ā^U, inferring IN for u* ∈ U and OUT for u* ∉ U. » La nouveauté du papier est que l'attaquant ne dispose d'aucun jeu auxiliaire de traces réelles d'autres individus (contrairement à l'attaque « Knock-Knock » antérieure de Pyrgelis et al.) : il génère lui-même des traces synthétiques de référence à partir des seuls paramètres statistiques estimés sur l'agrégat publié (résumé, p. 80). L'objet attaqué est un **agrégat de comptages de localisation** (une matrice ROI × époque), pas un enregistrement tabulaire synthétique individuel, et la question posée est « ce record a-t-il été inclus dans le jeu d'entraînement/agrégation ? », jamais « ces deux sorties appartiennent-elles à la même personne ? ». Ce n'est donc en rien une attaque de liaison entre deux sorties.

## Verdict

L'affirmation « aucun précédent direct » n'est **pas tenable telle quelle** (elle laisse croire que la question ne s'est jamais posée), mais elle est **tenable si reformulée** : aucun des deux candidats les plus proches n'attaque le même scénario que le nôtre — Anonymeter définit la linkability comme une liaison entre deux vues d'attributs d'un original réel connu de l'attaquant (et la juge de toute façon comme le risque le plus faible des trois), tandis que ZAK-MIA est une attaque d'appartenance sur des agrégats de localisation, sans lien avec la liaison entre sorties synthétiques.

**Phrase de remplacement proposée pour le résumé** :
« À notre connaissance, aucun travail antérieur n'évalue la liaison (linkability) entre deux sorties synthétiques indépendantes d'un même individu sans que l'attaquant dispose de valeurs réelles de ses attributs : le cadre le plus proche, celui d'Anonymeter (Giomi et al., PoPETs 2023), définit la linkability comme la liaison de deux partitions d'attributs d'un jeu de données original réel via un jeu synthétique intermédiaire — et la classe comme le plus faible des trois risques qu'il mesure — tandis que ZAK-MIA (Guan et al., PoPETs 2024) est une attaque d'appartenance sur des agrégats de localisation, sans rapport avec la liaison entre sorties. »
