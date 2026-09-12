# Contrôle de fidélité préalable — 12 septembre 2026

Calculé par `analyses/c7_controle_interpretabilite.py`, testé par
`analyses/test_controle_interpretabilite.py`. Aucun appel d'API, aucune dépense, aucune
recherche web. Lecture seule sur `data/`. Aucune écriture hors des trois fichiers
autorisés pour cette tâche.

## 1. Ce que ce contrôle empêche de refaire

Cette nuit, deux expériences payantes (les bras B↔M, B↔G, B↔P du plan factoriel, et le
témoin B↔C « deux organisations ») ont mesuré un contraste entre jumeaux sans jamais
vérifier que ces jumeaux portaient une personne. Contre les 120 humains réels du même
bassin, ils la réidentifiaient à 0,0–0,8 %, le hasard valant 0,83 % — c'est-à-dire
jamais — là où les jumeaux publiés par l'équipe Twin, sur ce même bassin, atteignent
jusqu'à 38,9 %. Tous les contrastes de la chaîne A comparaient deux générateurs de
bruit. L'une de ces mesures a fondé une conclusion publiée et annoncée à deux équipes
extérieures avant d'être suspendue. Le contrôle qui l'aurait évité ne coûte rien : le
top-1 candidat contre les humains réels, sur le bassin réellement attaqué, comparé à la
baseline Demographics Only calculée sur ce même bassin.

Second piège, avéré deux fois cette nuit : la baseline dépend fortement de la taille du
bassin — 2,13–2,15 % à 2 058 personnes, 9,20 % à 200, 13,25–13,29 % à 120 (les deux
valeurs à 120 viennent de graines de départage d'ex æquo différentes, cf. §4). Comparer
un top-1 à la baseline d'un *autre* bassin suffit à inverser une conclusion.

## 2. La règle de décision retenue, et pourquoi

**Un candidat passe seulement si la borne basse de son IC bootstrap à 95 % (top-1 contre
les humains réels) est strictement supérieure à la borne haute de l'IC à 95 % de la
baseline Demographics Only, calculée sur EXACTEMENT le même bassin et les mêmes items.**
IC non chevauchants, jamais une comparaison de points (13 % < 21 % ne suffit pas).

Pourquoi ce critère et pas un test de différence directe (ex. bootstrap apparié de
`candidat − baseline`, IC de la différence excluant zéro) : un test de différence
apparié serait plus puissant (il capturerait une partie de la corrélation entre les deux
bootstraps sur le même bassin) mais demanderait de réimplémenter un rééchantillonnage
joint — la mission demande explicitement de réutiliser le bootstrap existant
(`a2_commun.bootstrap_personnes`) sans le modifier, et le sinistre de cette nuit est un
**faux positif** (du bruit interprété comme un signal), pas un faux négatif. Le test
d'IC non chevauchants est le plus conservateur des deux qui se construit sans toucher
au bootstrap existant : en cas de doute il refuse de laisser interpréter, jamais
l'inverse. C'est un choix délibéré, pas un oubli — voir §5 pour son coût réel.

Techniquement : le candidat et la baseline sont chacun passés à
`c7_reconciliation_facteurs.attaque_vers_humain` (déjà câblée avec
`c7_reidentification.rangs_attaque` et `a2_commun.bootstrap_personnes`, 2000 tirages
bootstrap sur les personnes). Rien n'est réimplémenté.

## 3. La baseline ne se fournit jamais à la main

`controle_avant_interpretation(indices_personnes, indices_items, codes_candidat,
nom_candidat, paq=None)` ne prend **aucun paramètre de baseline**. Les seuls leviers de
l'appelant sont `indices_personnes` (les indices, dans la population Twin-2K-500
complète, des personnes du bassin réellement attaqué) et `indices_items` ; la fonction
tranche elle-même `Demographics Only - GPT4.1-mini` et `humains vague 4` sur ces mêmes
indices avant de calculer la baseline. Il n'existe structurellement aucun moyen de
comparer un candidat à la baseline d'un bassin différent : la taille du bassin de la
baseline est *dérivée* de `len(indices_personnes)`, jamais choisie séparément. Une
forme incohérente entre `codes_candidat` et `(indices_personnes, indices_items)` lève
`ValueError` avant tout calcul (testé, cas 4a).

## 4. Résultat réel des tests

Commande exécutée : `.venv/bin/python analyses/test_controle_interpretabilite.py`.

```
TOUT PASSE : 19 verifications.
```

- **Cas 1 (doit échouer, données réelles)** : les cinq jumeaux payés cette nuit (B, C,
  M, G, P), relus depuis `data/traces/c7-deux-organisations.jsonl` et
  `data/traces/c7-factoriel.jsonl` via `c7_reconciliation_facteurs.relire` — **les cinq
  lèvent `EchecControleInterpretabilite`**, top-1 de 0,00 à 0,79 % contre une baseline
  recalculée ici à 13,25 % [7,92 ; 19,46].
- **Cas 2 (doit passer, données réelles)** : `JSON Persona - GPT4.1` (équipe Twin) —
  **passe**, top-1 38,92 % [30,96 ; 47,08], IC entièrement au-dessus de celui de la
  baseline (30,96 > 19,46).
- **Cas 4 (synthétique, déclaré comme tel)** : une forme de matrice incohérente avec le
  bassin déclaré lève `ValueError` ; un candidat entièrement manquant sur un bassin
  synthétique de 3 personnes lève `EchecControleInterpretabilite` pour couverture
  insuffisante (< 5 personnes). Ces deux cas ne portent aucune donnée Twin réelle, ils
  testent uniquement les garde-fous.

**Écart avec l'arbitrage, signalé et non corrigé** : la baseline recalculée ici donne
13,25 % [7,92 ; 19,46] contre 13,29 % [7,50 ; 19,79] dans
`c7-reconciliation-facteurs.csv`. Même chose à l'échelle 2 058 (2,15 % [1,59 ; 2,79] ici
contre 2,13 % publié). L'écart tient entièrement à l'étiquette de graine passée à
`attaque_vers_humain` (`"baseline|demo"` ici contre `"fid|Demographics Only -
GPT4.1-mini"` dans le bloc `fidelite_vs_humain_pool120` de l'arbitrage) qui change le
tirage aléatoire de départage des ex æquo — le rapport d'arbitrage documente lui-même ce
phénomène (« aux aléas de graine de départage près », §2). Quand la fonction est
appelée avec la *même* étiquette que l'arbitrage (`"baseline|demo"`, celle du bloc
`baseline` de la section 5), les chiffres sont bit à bit identiques :
0,1325 / 0,07916... / 0,19458... contre 0,1325 / 0,07916... / 0,19458... dans
`c7-reconciliation-facteurs.csv`, bloc `baseline`. Aucun chiffre n'a été ajusté pour
coller à l'arbitrage.

## 5. Application rétrospective : ce que le contrôle aurait fait cette nuit

**Les deux mauvaises expériences (B↔M, B↔G, B↔P, et par construction B↔C) : arrêtées,
5/5.** Chacun des cinq jumeaux payés cette nuit échoue au contrôle, pour la raison
exacte qui les disqualifie : leur IC ne dépasse jamais la baseline, il tombe dedans ou
en dessous.

**Les bonnes expériences (jumeaux publiés par l'équipe Twin) : résultat mitigé, et c'est
une information, pas un bug.** Sur les huit configurations Twin, au bassin de 120 utilisé
par l'arbitrage :

| configuration | top-1 | passe le contrôle (bassin=120) ? |
|---|---|---|
| Demographics Only - GPT4.1-mini | 13,29 % | — (c'est la baseline elle-même) |
| **JSON Persona - GPT4.1** | **38,92 %** | **oui** |
| JSON Persona - GPT4.1-mini | 26,03 % | non |
| Text Persona (Default Temperature) | 22,29 % | non |
| Text Persona (Reasoning) | 23,00 % | non |
| Text Persona (Repeating Questions) | 20,17 % | non |
| Text Persona - GPT4.1-mini | 21,25 % | non |
| Text Persona - Gemini-Flash2.5 | 26,46 % | non |

Seul 1 des 7 jumeaux non démographiques passe à ce bassin précis. Ce n'est **pas** que
ces six-là ne portent aucune information individuelle — leur top-1 (20 à 26 %) reste
très au-dessus du hasard (0,83 %) et de la baseline ponctuelle (13,3 %). C'est que l'IC
de la baseline Demographics Only, à n = 120, est large ([7,92 ; 19,46]), et qu'un test à
IC non chevauchants exige alors un top-1 nettement supérieur à 19,5 % pour passer sans
ambiguïté. Vérifié à l'échelle 2 058 personnes (baseline recalculée à 2,15 % [1,59 ;
2,79], IC étroit) : `Text Persona - GPT4.1-mini` (5,45 % [4,51 ; 6,40]),
`JSON Persona - GPT4.1-mini` (12,36 % [10,46 ; 14,37]) et
`Text Persona (Repeating Questions) - GPT4.1-mini` (7,30 % [6,28 ; 8,34]) passent tous
les trois sans ambiguïté à ce bassin plus grand, alors même que leur top-1 y est
mécaniquement plus bas (pool plus grand = compétition plus dure). La règle se comporte
donc correctement dans les deux sens : elle ne confond jamais un top-1 plus bas avec une
moins bonne fidélité quand la baseline du même bassin baisse d'autant.

## 6. Limites déclarées

- **Un contrôle qui passe ne garantit pas qu'une expérience est interprétable.** Il
  garantit seulement qu'elle n'est pas disqualifiée d'avance par un générateur qui ne
  porte aucune personne. Une fois passé, la question de savoir si le contraste mesuré
  (modèle, gabarit, persona...) reflète un effet réel reste entière et dépend du plan
  d'expérience, pas de ce contrôle.
- **Le test est conservateur par construction, et cela a un coût mesuré ici** : à petit
  bassin (n = 120), six jumeaux dont la fidélité (20–26 %) dépasse nettement le hasard
  et la baseline ponctuelle ne passent pas le test à IC non chevauchants, parce que
  l'IC de la baseline elle-même est large à ce bassin. Un pipeline légitimement
  informatif peut donc être refusé à petit bassin — la parade n'est pas d'assouplir la
  règle mais d'attaquer un bassin plus grand quand c'est possible (§5 le montre).
- **Le contrôle ne dit rien sur le mécanisme.** Il établit qu'un pipeline échoue ou
  passe, jamais pourquoi (persona ignorée, défaut de parsing, modèle qui ne lit pas le
  dossier...).
- **La reproduction des chiffres de l'arbitrage dépend de l'étiquette de graine passée**
  (§4) : deux appels légitimes avec des noms différents donnent des IC légèrement
  différents (aléas de départage d'ex æquo), jamais le top-1 moyen au-delà de ~0,05
  point ici. Ce n'est pas une instabilité du contrôle, c'est la même propriété que le
  rapport d'arbitrage documente pour ses propres résultats.
- **Portée** : ce contrôle ne s'applique qu'au risque déjà identifié (générateur qui ne
  transporte aucune information individuelle). Il ne remplace aucun des autres
  contrôles déjà en place (couverture, dégénérescence des vecteurs de réponse, motifs
  de manquants).

## 7. Mode d'emploi

**Où l'appeler dans le protocole : avant le premier appel payant sur tout contraste
entre jumeaux, jamais après.** Concrètement, dès qu'un pilote (quelques dizaines de
personnes suffisent, cf. §5) a produit des jumeaux candidats et que les humains réels
correspondants sont disponibles (Twin-2K-500 vague 4), avant de lancer la campagne
complète :

```python
from c7_controle_interpretabilite import (
    controle_avant_interpretation, EchecControleInterpretabilite,
)

# indices_personnes : indices, dans la population Twin-2K-500 complète, du bassin
#   REELLEMENT attaque par le pilote (pas un sous-echantillon choisi a posteriori).
# indices_items     : les colonnes reellement comparees (ex. c7_reidentification.items_communs).
# codes_candidat    : les codes du jumeau pilote, alignes ligne a ligne sur
#   indices_personnes et colonne a colonne sur indices_items.
controle_avant_interpretation(indices_personnes, indices_items, codes_candidat,
                               "nom du pipeline pilote")
# Si ça leve EchecControleInterpretabilite : ARRET. Corriger le generateur (parsing,
# persona transmise, format de sortie) et refaire un pilote AVANT tout appel supplementaire.
# Si ça passe : le pipeline n'est pas disqualifie d'avance -- la campagne complete peut
# etre lancee, l'interpretation du contraste visé reste a etablir par ailleurs (§6).
```

**Formulation à inscrire dans un préenregistrement**, pour que la règle soit opposable :

> Avant tout appel payant portant sur le contraste [décrire le contraste], un pilote
> sera mené sur un bassin d'au moins [N] personnes de Twin-2K-500. Le pipeline candidat
> ne sera jugé interprétable, et la campagne complète ne sera lancée, que si le top-1 de
> réidentification du jumeau candidat contre les humains réels (vague 4), sur ce bassin
> pilote et sur les items effectivement comparés, a un intervalle de confiance bootstrap
> à 95 % (rééchantillonnage sur les personnes, 2000 tirages) dont la borne inférieure
> dépasse strictement la borne supérieure de l'intervalle de confiance à 95 % de la
> baseline Demographics Only, calculée sur ce même bassin pilote et ces mêmes items. Si
> ce contrôle échoue, aucun appel supplémentaire ne sera effectué sur ce pipeline avant
> correction et nouveau pilote. Un contrôle qui passe ne dispense d'aucune autre analyse
> prévue par ailleurs dans ce préenregistrement ; il établit seulement que le pipeline
> n'est pas disqualifié d'avance par un générateur qui ne transporte aucune information
> individuelle.
