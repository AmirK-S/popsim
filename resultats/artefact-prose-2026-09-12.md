# Relecture de la prose de `artefact/` après le retournement de C7 — 12 septembre 2026

Contexte : `resultats/c7-nul-corrige-resultats.md` retire la réfutation de la prédiction (b)
(le témoin « nul de marge » recopiait la vraie réponse) mais **ne** confirme la causalité
fidélité → identifiabilité (réserve du §6 : « le couplage n'est pas produit par un taux
d'exactitude par personne seul » ≠ « la fidélité à cette personne-là en est le mécanisme »).
`resultats/c7-deux-organisations-resultats.md` détruit le scénario de menace « deux
organisations indépendantes » (top-1 3,66 % < baseline démographique 9,20 %).

Périmètre relu : `artefact/README.md`, tous les docstrings et commentaires de
`artefact/attaque.py`, `defense.py`, `config.py`, `generer_donnees.py`, `garde.py`,
`test_garde.py`, `tableau_final.py`, et les commentaires de `run.sh`.

## Verdict : aucune correction nécessaire

Recherche systématique (lecture intégrale + `grep -rniE
"fidelit|causal|rho|organisation|preuve|demontre que|montre que"`) : **zéro occurrence**
des trois affirmations à risque dans toute la prose de `artefact/` :

1. **Causalité fidélité → identifiabilité présentée comme acquise.** Absente. Le seul
   endroit où l'artefact relie « copier davantage » à « plus identifiable »
   (`README.md`, section *Ce que l'artefact démontre*, point 1 ; `config.py`, commentaire
   sur `SIGNAL_INDIVIDUEL`) décrit un **mécanisme manipulé directement par construction**
   (un cadran `SIGNAL_INDIVIDUEL` qui contrôle littéralement la probabilité de recopie) —
   ce n'est pas la corrélation observationnelle entre fidélité globale et fuite à travers
   des jumeaux différents que `c7-nul-corrige-resultats.md` traite avec prudence. Les deux
   ne sont pas la même affirmation ; l'artefact ne fait à aucun endroit le raccourci entre
   les deux.
2. **Scénario « deux organisations » / liaison de jumeaux entre organisations
   indépendantes.** Absent de `artefact/` : ni le mot « organisation(s) », ni aucune
   formulation suggérant qu'on peut relier des jumeaux publiés par deux pipelines
   distincts. Rien à corriger ni à retirer.
3. **Confusion synthétique / réel.** Déjà explicitement écartée : dès la première phrase
   du README (« sans aucune donnée réelle et sans aucune personne réelle ») jusqu'au
   message imprimé par `tableau_final.py` (« chiffres obtenus sur un jeu de données
   ENTIÈREMENT FICTIF... Ils ne se substituent pas aux chiffres de l'article »), en passant
   par la section *Ce que l'artefact NE démontre PAS* (« Ne citez jamais les chiffres de
   cet artefact comme des résultats de l'étude »). Chaque fichier (`attaque.py`,
   `defense.py`, `generer_donnees.py`) répète « N'IMPORTE PAS DE DONNÉES RÉELLES » /
   « AUCUNE DONNÉE RÉELLE, AUCUNE PERSONNE RÉELLE » en tête de docstring. Aucun endroit ne
   laisse croire que l'artefact démontre un résultat sur des personnes réelles.

Les deux chiffres réels cités par le README pour les prédictions autrefois « réfutées »
(non concluantes) et les chiffres de l'article (20,68 % / 0,13 %, `c7-defense-resultats.md`)
ne sont pas non plus mentionnés dans `artefact/` au-delà de cette seule référence à
20,68 %/0,13 % — qui provient d'une analyse (attaque/défense de base) non affectée par le
retournement (celui-ci porte sur la corrélation de Spearman fidélité/fuite entre les douze
jumeaux dans `c7-nul-corrige`, pas sur le top-1 avant/après D4).

## Vérification des chiffres de démonstration (mission point 4)

`./artefact/run.sh` ré-exécuté intégralement (graine fixe `config.GRAINE = 20260912`) :

```
jumeau Demographics Only (comparateur)     0.150 %  [0.000;0.417]
jumeau riche, AVANT defense                21.900 % [18.791;25.059]
jumeau riche, APRES D4 (melange segment)    0.842 % [0.258;1.609]
reduction du risque (avant / apres)        x26
perte d'utilite de la defense              1.45 points (distrib.=0.00 / groupes=0.00 / corr.=4.36)
```

**Identique au chiffre par chiffre au tableau donné par `README.md`** (21,900 % avant /
0,842 % après, IC compris) : aucun écart entre la prose et ce que le code produit
réellement.

## Ce qui n'a pas été touché, et pourquoi

- Aucune ligne de `artefact/README.md`, d'aucun docstring/commentaire Python, ni de
  `run.sh` n'a été modifiée : la relecture n'a trouvé aucune affirmation fausse, trop
  forte ou périmée à corriger, dans le périmètre du retournement C7 comme dans le reste
  de la prose (numéros de version, durées annoncées, contenu du tableau `Contenu`,
  section « Obtenir les vraies données » — tous cohérents avec l'état actuel des
  fichiers).
- Un point mineur, non lié au retournement et donc **non corrigé** conformément à la
  consigne de sobriété : la durée totale annoncée dans le README (« environ 25 secondes »)
  est nettement supérieure à la durée mesurée ici (~3,7 s, cache déjà chaud). Le README
  anticipe déjà explicitement cette variabilité (machine, cache froid/chaud), donc ce
  n'est ni faux ni périmé — seulement optimiste sur cette machine ; signalé ici par
  prudence plutôt que corrigé, comme demandé pour tout point d'hésitation.

## Suite des tests et exécution

- `./artefact/run.sh` : succès, sortie ci-dessus, aucune erreur.
- `.venv/bin/python artefact/test_garde.py` : **11/11 tests passent** (`OK`).

Aucun fichier fonctionnel (`.py`, `run.sh` hors commentaires) n'a été modifié ; cette
ré-exécution sert uniquement à confirmer que la relecture n'a rien cassé et que les
chiffres cités sont bien ceux que le code produit.
