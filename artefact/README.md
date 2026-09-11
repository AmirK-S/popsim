# Artefact de relecture : reidentification et defense (C7)

Cet artefact permet a un relecteur de **rejouer l'attaque de reidentification et sa
defense en une seule commande, sans aucune donnee reelle et sans aucune personne
reelle**. Il accompagne l'article sur le risque de vie privee des jumeaux numeriques
(`resultats/c7-resultats.md`, `resultats/c7-defense-resultats.md`).

```
.venv/bin/python -m venv .venv   # si besoin, ou utilisez votre propre python3.10+
./artefact/run.sh
```

Duree mesuree localement : **environ 25 secondes** (bien sous la barre des 5 minutes),
sur un Mac portable, sans GPU, sans reseau, sans appel de modele de langage.

## Ce que l'artefact demontre

1. **La mecanique de l'attaque** : un jumeau qui, sur un bloc de type "matrice produits x
   prix", recopie ne serait-ce qu'une fraction reglable des reponses individuelles d'une
   personne (`config.SIGNAL_INDIVIDUEL`) devient reidentifiable par simple comparaison de
   Hamming a la population, tres au-dessus du hasard ET du comparateur "Demographics
   Only" (aucune recopie individuelle, seulement le segment demographique).
2. **La mecanique de la defense (D4)** : permuter les reponses de ce bloc entre personnes
   du meme segment demographique (`c7_defense.defense_d4`, importee telle quelle) fait
   quasiment disparaitre la fuite, pour une perte d'utilite faible et concentree sur les
   correlations entre items (jamais sur les moyennes par item ni sur les ecarts entre
   groupes, qu'une permutation intra-segment preserve exactement).
3. Que ces deux mecaniques sont **bien celles qui tournent dans l'article** : `attaque.py`
   importe `items_communs`, `rangs_attaque`, `rang_dans_segment`, `graine_nom` depuis
   `analyses/c7_reidentification.py`, et `defense.py` importe `defense_d4` et
   `mesurer_utilite` depuis `analyses/c7_defense.py` -- rien n'est recopie, seule la
   fonction `t1_commun.charger()` (qui lit `data/`) n'est jamais appelee.

## Ce que l'artefact NE demontre PAS

- **Aucun chiffre ici ne se substitue a ceux de l'article.** Les chiffres publies
  (20,68 % de top-1 avant defense, 0,13 % apres D4, etc.) sont mesures sur Twin-2K-500,
  un jeu de donnees reel non redistribuable ici. Le jeu fictif de cet artefact a une
  structure comparable (items categoriels, bloc matrice produits x prix, segments
  demographiques, retest) mais des effectifs et une force de signal differents, choisis
  pour rester illustratifs et rapides (600 personnes fictives contre 2 058 humains
  reels). Ne citez jamais les chiffres de cet artefact comme des resultats de l'etude.
- Aucune replication des huit configurations de jumeaux, ni du controle sur les motifs de
  manquants seuls, ni de l'archive Stanford (`c7_stanford.py`) : l'artefact se limite au
  coeur demontrable, attaque + defense D4, sur un seul jumeau fictif "riche" et un seul
  comparateur "Demographics Only".
- Aucune garantie que le reglage `SIGNAL_INDIVIDUEL = 0.25` reproduise fidelement la
  force du mecanisme reel (bloc Product Preferences - Pricing) : c'est un cadran de
  demonstration, documente et modifiable dans `config.py`.

## Contenu

| fichier | role |
|---|---|
| `config.py` | tous les parametres du jeu fictif et de la demonstration (N, items, `SIGNAL_INDIVIDUEL`, graine). |
| `garde.py` | garde-fou commun : refuse de demarrer si un chemin vers `data/` est detecte (argv, variables d'environnement). |
| `generer_donnees.py` | genere `donnees_fictives/` a graine fixe : personnes, segments, items opinion/achat/contexte, retest, deux jumeaux simules. |
| `attaque.py` | importe la logique de `analyses/c7_reidentification.py`, calcule top-1/top-10/rang median et les comparateurs. |
| `defense.py` | importe `defense_d4` et `mesurer_utilite` de `analyses/c7_defense.py`, mesure risque et utilite avant/apres. |
| `tableau_final.py` | assemble les deux CSV de sortie en un tableau lisible. |
| `run.sh` | enchaine les quatre etapes ci-dessus. |
| `donnees_fictives/` | sortie de `generer_donnees.py` (cree a l'execution, pas versionne). |
| `resultats_artefact/` | sortie de `attaque.py`/`defense.py` (cree a l'execution, pas versionne). |

## Le jeu de donnees fictif

Genere par `generer_donnees.py`, graine fixe `config.GRAINE = 20260912`. **Aucune donnee
reelle, aucune personne reelle** : tout est tire par `numpy.random.default_rng`.

- 600 personnes fictives, segmentees selon un `S_gra` fictif (genre x age x ethnicite,
  24 segments).
- 60 items "opinion" categoriels (5 modalites), toujours renseignes, **sans aucune
  signature individuelle** (loi de segment uniquement) -- role joue par le bloc
  d'opinion de Twin.
- 40 items "achat", matrice produits x prix (5 paliers), avec un **signal individuel
  reglable** : chaque personne a un profil stable, et sa reponse "verite terrain" en
  vient avec probabilite `PROB_INDIVIDU_ACHAT_VERITE` -- role joue par le bloc Product
  Preferences - Pricing, identifie dans `resultats/c7-mecanisme-resultats.md` comme le
  vecteur de la fuite reelle.
- 20 items de "contexte", avec manquants (30 %), jamais utilises par l'attaque : ils
  servent uniquement a exercer `items_communs()` sur un jeu qui n'est pas rempli a 100 %
  partout, comme le vrai Twin-2K-500 (60 items communs sur 108).
- un retest humain (memes personnes, meme profil individuel, tirage independant :
  fiabilite test-retest imparfaite).
- deux jumeaux simules : `twin_riche` (recopie la verite avec probabilite
  `SIGNAL_INDIVIDUEL = 0.25` sur le bloc achat) et `twin_demo` (jamais de recopie
  individuelle, comparateur "Demographics Only").

## Obtenir les vraies donnees (pour reproduire les chiffres de l'article, pas pour cet artefact)

- **Twin-2K-500** : depot Hugging Face `LLM-Digital-Twin/Twin-2K-500`, licence **CC BY
  4.0**, telechargement direct, aucun compte requis. C'est la source utilisee par
  `analyses/t1_commun.py` (`data/twin2k500/`).
- **Archive de replication Stanford** (agents generatifs, utilisee par
  `analyses/c7_stanford.py`) : paquet de replication poste publiquement sur
  `https://osf.io/t6g7k/`. Il contient des reponses individuelles reelles de 1 052
  participants humains ; ce depot ne le redistribue pas et cet artefact ne le lit
  jamais. Verifiez les conditions d'usage et d'acces en vigueur sur la page OSF avant
  tout telechargement -- elles peuvent avoir change depuis l'ecriture de ce texte.
- Dans les deux cas : **lecture seule**, jamais de reecriture, jamais de redistribution
  dans ce depot (voir `README.md` et `METHODOLOGIE.md` a la racine).

## Preenregistrements et rapports correspondants

- `resultats/c7-preenregistrement.md` : preenregistrement de l'attaque de
  reidentification, ecrit avant tout calcul.
- `resultats/c7-resultats.md` : resultats mesures sur Twin-2K-500 (huit configurations).
- `resultats/c7-defense-preenregistrement.md` : preenregistrement des quatre familles de
  defense (D1 agregation, D2 bruit, D3 retrait, D4 melange intra-segment).
- `resultats/c7-defense-resultats.md` : resultats de defense, reglage recommande D4.
- `resultats/c7-stanford-preenregistrement.md` / `c7-stanford-resultats.md` : replication
  sur l'archive Stanford (hors perimetre de cet artefact).

## Versions

Mesure sur la machine ayant produit cet artefact :

- Python **3.13.14** (`.venv/bin/python`, aucune dependance reseau)
- numpy **2.5.2**, pandas **3.0.5**, scikit-learn **1.9.0**

`analyses/c7_reidentification.py` et `analyses/c7_defense.py` importent aussi, en
cascade, `t1_commun`, `a2_commun`, `a6_double_distorsion_hors_gss`, `i3b_twin`,
`i3b_commun`, `a44_commun`, `a1_double_distorsion` (le meme environnement `.venv` du
depot). Aucun de ces modules ne touche `data/` a l'import : seule leur fonction
`charger()` le ferait, et cet artefact ne l'appelle jamais.

## Duree et sortie attendues

- `generer_donnees.py` : environ 2 secondes.
- `attaque.py` : environ 10-15 secondes (l'import en cascade domine le temps de calcul).
- `defense.py` : environ 10 secondes.
- `tableau_final.py` : instantane.
- **Total : environ 25 secondes.**

Sortie attendue de `tableau_final.py` (chiffres exacts obtenus lors de la redaction,
reproductibles a l'identique avec la graine fixe) :

```
jumeau Demographics Only (comparateur)     0.150 %  (hasard exact = 0.167 %)
jumeau riche, AVANT defense                21.900 % [18.791 ; 25.059]
jumeau riche, APRES D4 (melange segment)    0.842 % [0.258 ; 1.609]
reduction du risque (avant / apres)        x26
perte d'utilite de la defense              1.45 points (quasi entierement les correlations)
```

La fuite tombe de pres de 22 % a moins de 1 %, pour une perte d'utilite sous 2 points --
exactement le critere preenregistre dans `resultats/c7-defense-preenregistrement.md`,
demontre ici sur un jeu qui ne contient aucune personne reelle.
