# Sauvetage des scripts du témoin de marge corrigé — 12 septembre 2026

Suite à `resultats/reproductibilite-chaine-2026-09-12.md` §5 : le script qui produit le
chiffre « qui fait autorité » de l'article (rho 0,974 contre 0,965 observé, A1, figure 2)
n'existait que dans un répertoire de scratchpad de session, absent du dépôt Git. Mission :
le retrouver, l'intégrer au dépôt, vérifier qu'il rejoue le chiffre publié, et corriger le
chemin de cache en dur de `analyses/c7_nul_corrige.py`. Tout en avant-plan, aucun appel
d'API, aucun commit git.

## 1. Ce qui a été retrouvé

Recherche sous `/private/tmp/claude-501/-Users-amirkellousidhoum-Desktop-Code-Projets-popsim/`
(6 répertoires de session). Les trois scripts nommés par
`resultats/audit-renversement-2026-09-12.md` (« scripts d'audit dans le scratchpad de
session ») ont tous les trois été retrouvés, intacts, dans **un seul** répertoire de
session (`ed6061e6-124c-4c1f-aeb8-1b15f57c239b/scratchpad/`) — celui de la présente
session :

- `audit2.py` (70 lignes) — trouvé
- `audit3.py` (55 lignes) — trouvé
- `audit_contre_nul.py` (110 lignes) — trouvé, c'est **celui qui produit le rho 0,974**

Rien ne manque : les trois scripts cités par le rapport d'audit adverse ont été localisés.
Le même répertoire contenait aussi le cache de baselines statistiques dont ces scripts
dépendent (`c7-nul-corrige-baselines-60.pkl`, 1,2 Mo), utilisé pour accélérer la
vérification (voir §3).

## 2. Intégration au dépôt

Copiés tel quels dans `analyses/`, sans réécriture du code de calcul — seul un en-tête de
provenance a été ajouté à chaque fichier (docstring, avant le code original) :

| Fichier de scratchpad | Nouveau nom dans `analyses/` | Rôle |
|---|---|---|
| `audit_contre_nul.py` | `analyses/c7_temoin_verite_appariee.py` | **Script central** : construit le nul « exactitude-vérité appariée » et calcule son rho contre la fidélité/fuite — c'est le chiffre 0,974 |
| `audit2.py` | `analyses/c7_audit_lecture_resultats.py` | Relit `resultats/c7-nul-corrige.csv` (déjà versionné) et imprime les tables de diagnostic (dispersion inter/intra, contrôles d'exactitude visée, jackknife, comparaison à la loi de Spearman sous H0) |
| `audit3.py` | `analyses/c7_audit_decomposition.py` | Décomposition « angle 6 » : coïncidence avec un candidat au hasard, ventilée cellules justes/fausses |

Aucun des trois n'a dû être réécrit pour tourner depuis le dépôt.

## 3. Le seul chemin réellement en dur : celui de `c7_nul_corrige.py`

`analyses/c7_nul_corrige.py` ligne ~108-111 codait en dur le chemin de cache
`C7_NUL_CACHE` par défaut vers ce répertoire de scratchpad de session (signalé
indépendamment par les deux rapports). Corrigé : le défaut est maintenant
`/tmp/c7-nul-corrige-baselines-60.pkl` — **exactement la même convention** que le cache
frère `analyses/c7_bits.py` (`C7_BITS_CACHE`, défaut `/tmp/c7-bits-baselines-60.pkl`) déjà
présent dans le dépôt. Logique de calcul inchangée ; toujours surchargeable par variable
d'environnement ; toujours régénéré automatiquement si absent (`os.path.exists(CACHE)`,
inchangé). Le cache retrouvé au §1 a été copié à ce nouvel emplacement portable pour éviter
de refaire un calcul de baselines déjà déterministe.

`c7_temoin_verite_appariee.py` et `c7_audit_decomposition.py` importent `CACHE` directement
depuis `c7_nul_corrige` : la correction se propage automatiquement, aucune autre modification
n'était nécessaire dans les scripts sauvés.

## 4. Chiffres obtenus en rejouant depuis le dépôt, comparés aux chiffres publiés

Toutes les commandes ci-dessous ont été exécutées depuis la racine du dépôt, en avant-plan,
avec le code tel qu'intégré (aucun ajustement des chiffres après coup).

### 4.1 Le chiffre central (rho 0,974 vs 0,965)

`.venv/bin/python analyses/c7_temoin_verite_appariee.py` (20 réplicats, valeur par défaut du
script, déjà réduite par rapport au préenregistrement — comme documenté dans
`resultats/audit-renversement-2026-09-12.md` — **non réduite davantage ici**) :

| | Publié (audit-renversement §1.3) | Obtenu ici depuis le dépôt | Écart |
|---|---|---|---|
| rho, remplissage **marginal** (défaut ligne 133 corrigé) | moyenne 0,9741, p5 0,9500, p95 0,9934 | moyenne **0,9741**, médiane 0,9720, p5 **0,9500**, p95 **0,9934**, min 0,9301, max 1,0000 | aucun |
| rho, remplissage **uniforme** | moyenne 0,9815 | moyenne **0,9815**, médiane 0,9860, p5 0,9580, p95 0,9930 | aucun |
| rho observé (référence) | 0,965 | 0,9650 (importé de `resultats/c7-nul-corrige.csv`) | aucun |

**Reproduit à l'identique.** La fourchette 0,974-0,985 annoncée par la mission correspond
exactement aux deux modes de remplissage (marginal 0,9741, uniforme 0,9815). Durée : 74 s
pour le mode marginal, 74 s de plus pour le mode uniforme (148 s au total pour la partie
rho).

**Incident non corrigé, signalé tel quel** : après avoir imprimé ces deux résultats, le
script plante (`IndexError: index 5 is out of bounds for axis 0 with size 5`) dans son bloc
final « ANGLE 6 » (une décomposition bonus, redondante avec `c7_audit_decomposition.py`, qui
a réussi séparément — voir 4.3). Le chiffre central (rho 0,974/0,965) est imprimé **avant**
ce plantage et n'est pas affecté. Cause probable : la table de fréquences marginales
construite à la volée dans ce bloc n'a pas la marge de sécurité que la même fonction a dans
`audit3.py`/`c7_audit_decomposition.py` (`K = max(...)+2`). C'est un défaut préexistant du
code récupéré, pas introduit par l'intégration ; non corrigé, conformément à la consigne de
ne pas réécrire.

### 4.2 `c7_nul_corrige.py` après correction du chemin de cache

`.venv/bin/python analyses/c7_nul_corrige.py --replicats 10 --bootstrap 300` (réduit depuis
100/2000 préenregistrés — **réduction déclarée**, calcul complet à 8 constructions estimé
>15 min ; sortie redirigée hors `resultats/` pour ne rien écraser). Interrompu volontairement
après ~10 min (4 constructions sur 8) une fois la reproductibilité établie :

| Construction | Publié (reproductibilite-chaine §5) | Obtenu ici, même réduction | Écart |
|---|---|---|---|
| reel (prédicteur publié) | rho = 0,9650 | rho = 0,9650 | aucun |
| N0 nul cassé | rho moyen 0,9839 | rho moyen 0,9839 (médiane 0,9825, p95 0,9930) | aucun |
| N1 mode de segment | rho moyen 0,1918 | rho moyen 0,1918 (médiane 0,2555) | aucun |
| N1b (Bernoulli) | rho = 0,3482 sur le seul réplicat vu avant interruption | rho = 0,3482 sur le seul réplicat vu | aucun |

Le cache s'est chargé depuis le nouveau chemin portable (`baselines relues du cache
/tmp/c7-nul-corrige-baselines-60.pkl`, confirmé dans les logs) : **la correction du chemin
n'a rien cassé**, et le script continue de tourner et de produire les mêmes chiffres qu'avant
correction.

### 4.3 `c7_audit_decomposition.py` (angle 6, décomposition c)

Tourne sans erreur, 3,6 s. Reproduit à l'identique le tableau du défaut 4 de
`audit-renversement-2026-09-12.md` : jumeau réel c_global=0,4319 (justes 0,4776 / fausses
0,3660), nul uniforme c_global=0,4097 (justes 0,4328 / fausses 0,3763), nul marginal
c_global=0,4250 (justes 0,4328 / fausses 0,4138) — et la table complète par construction
(exactitude contre vérité 0,5274 réel / 0,4238 N1 / 0,4066 N2 / 0,4364 N3, etc.), aucun écart.

### 4.4 `c7_audit_lecture_resultats.py`

Tourne sans erreur, 14 s (relit uniquement `resultats/c7-nul-corrige.csv`, déjà versionné,
aucun calcul lourd). Reproduit à l'identique : rho réel 12 points = 0,9650 (p=3,9e-07),
étendue jackknife [0,9545 ; 0,9818], rho 13 points = 0,9725, verdict au seuil z=5 (N1b et
N2b rejetées, verdict inchangé), table par configuration (JSON Persona - GPT4.1 top1
20,73 %, etc.) — tout concorde avec `audit-renversement-2026-09-12.md`.

## 5. `c7_transfert.py` et le 26,11 % — vérifié, non corrigé

Vérifié sans modifier le script : `analyses/c7_transfert.py` ligne 217 imprime
`f"top1 moyen, paires riches (n={len(paires_riches)}) : {m:.4f}"`, un agrégat qui mélange les
régimes à 60 et 19 items communs. Recalcul direct depuis `resultats/c7-transfert-voletA.csv`
(42 paires riches) : moyenne agrégée = **0,2611** (confirme le 26,11 % que l'article interdit
de citer) ; ventilée par `n_items` : 30 paires à 60 items → **0,3638** (36,4 % publié), 12
paires à 19 items → **0,004525** (0,45 % publié). La ventilation correcte n'est pas
automatisée dans le script ; un relecteur qui se contente de lire sa sortie standard obtient
le chiffre retiré.

**Recommandation, à trancher** : ajouter à `c7_transfert.py` une impression de la
ventilation par `n_items` à côté de (ou à la place de) l'agrégat actuel, pour qu'un
relecteur ne puisse pas citer le 26,11 % par erreur. Script non modifié, comme demandé.

## 6. Table script → chiffre de l'article (ce qui manquait à un relecteur d'artefact)

| Chiffre de l'article | Script | Commande | Durée mesurée |
|---|---|---|---|
| Témoin corrigé rho = 0,974 [0,950 ; 0,993] (marginal), 0,982 (uniforme) | `analyses/c7_temoin_verite_appariee.py` | `.venv/bin/python analyses/c7_temoin_verite_appariee.py` (20 réplicats par défaut ; `NREP=` en variable d'environnement pour changer) | ~150 s pour le rho (plante ensuite dans un bloc bonus, §4.1) |
| rho observé 0,965 (référence du témoin) | `analyses/c7_nul_corrige.py` (construction « reel »), ou relecture de `resultats/c7-nul-corrige.csv` | `.venv/bin/python analyses/c7_nul_corrige.py` (100 réplicats préenregistrés — long, voir ci-dessous) ou `analyses/c7_audit_lecture_resultats.py` | 100/2000 complet : >15 min (interrompu deux fois par l'audit précédent) ; réduit 10/300 : ~600 s pour 4 constructions sur 8 |
| N0-N3, abandonnés par l'article | `analyses/c7_nul_corrige.py` | idem | idem |
| Décomposition « angle 6 » (justes vs fausses) | `analyses/c7_audit_decomposition.py` | `.venv/bin/python analyses/c7_audit_decomposition.py` | 3,6 s |
| Tables de diagnostic (jackknife, seuil z, dispersion inter/intra) | `analyses/c7_audit_lecture_resultats.py` | `.venv/bin/python analyses/c7_audit_lecture_resultats.py` | 14 s |
| Canal inter-jumeaux 36,4 % / 0,45 % (PAS le 26,11 %) | `analyses/c7_transfert.py`, puis retabulation manuelle par `n_items` sur `resultats/c7-transfert-voletA.csv` | voir §5 | 521 s (mesure antérieure, non rejouée ici) |

## 7. Ce qui reste à faire, pour mémoire

- Décider du sort de `c7_transfert.py` (§5).
- Le plantage du bloc « ANGLE 6 » de `c7_temoin_verite_appariee.py` (§4.1) n'a pas été
  corrigé : à traiter séparément si ce bloc doit un jour être publié comme preuve, sinon
  sans conséquence puisque le chiffre central est imprimé avant.
- `c7_nul_corrige.py` n'a pas été rejoué à pleine échelle (100 réplicats/2000 bootstrap) ici,
  faute de temps en avant-plan ; le rejeu réduit (10/300) reproduit exactement les valeurs
  déjà vues par l'audit précédent sur les 4 premières constructions.
