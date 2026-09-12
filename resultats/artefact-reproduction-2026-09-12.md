# Reproduction hostile de l'artefact PoPETs (C7) — 12 septembre 2026

Relecteur simulé : de mauvaise foi, pressé, machine « vierge ». Protocole : clone Git
frais du dépôt distant (`git clone https://github.com/AmirK-S/popsim.git`) dans le
scratchpad de session, **sans aucun fichier ignoré par git** (pas de `.venv/`, pas de
`data/`, pas de `donnees_fictives/`, pas de `resultats_artefact/`) — donc uniquement ce
qui est réellement publié. Aucune modification du dépôt original, aucun commit. Toutes
les commandes ci-dessous ont été exécutées dans ce clone jetable.

## Verdict

**Reproductible avec écarts.** Les quatre chiffres annoncés sont reproduits à l'identique
(voir plus bas) et le déterminisme est parfait sur trois exécutions consécutives. Mais le
mode d'emploi de `artefact/README.md`, suivi à la lettre (créer `.venv`, lancer
`./artefact/run.sh`), **échoue immédiatement** : aucune étape n'indique d'installer une
seule dépendance. Le garde-fou, lui, est contournable de façon triviale sur plusieurs
vecteurs (casse, séparateur, variable d'environnement hors liste, lien symbolique), même
si — nuance importante détaillée plus bas — aucun script de `artefact/` n'exploite
aujourd'hui ces vecteurs pour un accès réel à `data/`.

## Écarts entre le mode d'emploi et la réalité

1. **Dépendances non installées, aucune instruction pour le faire (majeur).**
   `artefact/README.md` ne contient nulle part la commande `pip install`. Il montre
   seulement :
   ```
   .venv/bin/python -m venv .venv   # si besoin, ou utilisez votre propre python3.10+
   ./artefact/run.sh
   ```
   Suivi tel quel sur un venv fraîchement créé : `generer_donnees.py` plante immédiatement
   avec `ModuleNotFoundError: No module named 'numpy'`. La section « Versions » du même
   README ne fait que *constater* les versions utilisées par l'auteur (numpy 2.5.2, pandas
   3.0.5, scikit-learn 1.9.0) sans jamais dire comment les obtenir. Le `README.md` racine
   du dépôt ne comble pas ce trou non plus (aucune occurrence de `pip install` dans tout
   le dépôt). Il a fallu deviner et lancer `pip install -r requirements.txt` (fichier à la
   racine, jamais mentionné par `artefact/README.md`) pour que quoi que ce soit fonctionne.
   Cette installation s'est faite avec accès réseau (PyPI) — network que le README de
   l'artefact promet pourtant explicitement absent (« sans reseau »), en confondant
   l'exécution de `run.sh` (qui, elle, est bien hors-ligne) avec la mise en place initiale
   de l'environnement (qui ne l'est pas et n'est pas documentée).

2. **Python annoncé incohérent entre les deux fichiers (mineur).**
   `artefact/README.md` dit « utilisez votre propre python3.10+ » ; `pyproject.toml` à la
   racine déclare `requires-python = ">=3.13"`. Lequel fait foi n'est pas précisé. Non
   testé sur 3.10-3.12 faute d'interpréteur disponible ici ; signalé comme incohérence
   documentaire, pas comme échec constaté.

3. **Cascade de dépendances internes non triviale à vérifier (mineur, transparence).**
   `attaque.py`/`defense.py` importent `analyses/c7_reidentification.py` et
   `analyses/c7_defense.py`, qui importent en cascade `t1_commun`, `a6_double_distorsion_hors_gss`,
   `i3b_twin`, `i3_commun`, `i3b_commun`, `a44_commun`, `a44_mesures`, `a1_double_distorsion`,
   `a28_commun`, `a29_commun`, `a31_commun`, `a35_commun`, `a8_commun`, `c7_mecanisme` — soit
   14 modules de `analyses/`, contre les 7 annoncés dans le README de l'artefact. Tous
   présents dans le dépôt et tous inoffensifs à l'import (vérifié : aucun ne touche
   `data/` ni le réseau hors de la fonction `charger()`, jamais appelée). Le README
   sous-déclare donc la profondeur réelle de la cascade, sans que cela cause de défaut de
   fonctionnement — seulement un défaut de complétude documentaire pour un relecteur qui
   voudrait auditer *tout* ce qui s'importe.

Aucun autre écart : une fois les dépendances posées, `run.sh` s'exécute sans aucune
autre intervention manuelle, sans édition de code, sans variable d'environnement à
positionner.

## Chiffres obtenus contre chiffres annoncés

Sortie exacte de `tableau_final.py` (trois exécutions consécutives, valeurs identiques
au chiffre près) :

| ligne | annoncé (README) | obtenu | écart |
|---|---|---|---|
| jumeau Demographics Only (comparateur) | 0,150 % | 0,150 % [0,000 ; 0,417] | aucun |
| jumeau riche, AVANT défense | 21,900 % [18,791 ; 25,059] | 21,900 % [18,791 ; 25,059] | **aucun, exact** |
| jumeau riche, APRÈS D4 | 0,842 % [0,258 ; 1,609] | 0,842 % [0,258 ; 1,609] | **aucun, exact** |
| réduction du risque | x26 | x26 | aucun |
| perte d'utilité | 1,45 points | 1,45 points (distribution 0,00 / groupes 0,00 / corrélations 4,36) | aucun |
| critère « attaque démontrée » | vrai | `True` | aucun |
| critère « défense réussie » | vrai | `True` | aucun |

Les deux chiffres cités dans la mission (fuite ≈ 21,90 % tombant à 0,84 % après D4) sont
donc reproduits exactement, jusqu'à la troisième décimale et jusqu'aux bornes de l'IC à
95 %. C'est la meilleure nouvelle de ce rapport : une fois l'environnement posé, aucun
écart numérique, même infime.

## Déterminisme

Trois exécutions consécutives de `run.sh` (même clone, sans purge entre les runs) :
`attaque.csv`, `defense.csv` et les données fictives générées (`twin_riche.csv`, etc.)
sont **strictement identiques en MD5** d'une exécution à l'autre. Le seul contenu qui
diffère entre les logs des deux premiers runs est la ligne de temps mesuré (voir
ci-dessous) : `diff run1.log run2.log` ne montre aucune autre différence. Aucune source
d'aléa non fixée détectée (graine `config.GRAINE = 20260912` propagée partout via
`np.random.default_rng`, y compris dans les sous-graines dérivées pour le bootstrap et
les permutations).

## Garde-fou (`artefact/garde.py`) : tentatives de contournement

Contournements **réussis** (le garde-fou laisse passer un chemin qui, littéralement,
mène à `data/`, testé directement contre `verifier_environnement()`/`_suspect()` avec un
faux `data/twin2k500/reponses.csv` créé dans le clone jetable — jamais dans le vrai
dépôt) :

1. **Casse différente** : `DATA/x.csv` ou `Data/x.csv` → non détecté (`_suspect` fait un
   test de composant strictement sensible à la casse : `"data" in composants`).
2. **Séparateur inhabituel** : `data\twin2k500\reponses.csv` (séparateur Windows) sur ce
   système POSIX → non détecté, car `os.sep` vaut `/` ici et le chemin entier devient un
   seul composant opaque qui ne matche jamais `"data"`.
3. **Variable d'environnement hors liste** : le garde ne vérifie que 4 noms fixes
   (`POPSIM_DATA`, `TWIN2K500`, `DATA_DIR`, `RACINE_TWIN`). N'importe quel autre nom
   (`POPSIM_TWIN_PATH`, etc.) portant un chemin vers `data/` est ignoré.
4. **Variable d'environnement en minuscules** : `popsim_data` (au lieu de `POPSIM_DATA`)
   → ignorée (comparaison de nom de variable sensible à la casse via `os.environ.get`).
5. **Lien symbolique de nom neutre** : `ln -s ../data artefact/raccourci_prive` puis
   chemin `raccourci_prive/twin2k500/reponses.csv` → `_suspect()` répond `False` (aucun
   composant littéral nommé `data`), et une simple `open()` de ce chemin lit bien le
   contenu du dossier `data/` réel (démontré avec un fichier factice écrit uniquement
   dans le clone jetable, jamais dans le vrai dépôt). Le garde ne résout jamais les liens
   symboliques (pas d'appel à `os.path.realpath`) : il ne juge que la chaîne de
   caractères fournie.

Tentative **échouée** (le garde résiste, comportement correct) : chemin relatif
remontant construit pour cacher `data/` derrière un des deux dossiers listés en
exception (`donnees_fictives/../../../data/x` ou `resultats_artefact/../../data/x`) —
`os.path.normpath()` est appliqué *avant* le test des dossiers autorisés, donc le
composant `data` réapparaît intact après normalisation et reste détecté. Ce vecteur
précis, qui semblait le plus prometteur sur le papier, ne fonctionne pas.

**Nuance nécessaire, pour ne pas surcoter la gravité** : à l'examen de tout
`artefact/*.py`, aucun script n'utilise `sys.argv` au-delà de l'appel implicite
`argv[0]`, ni aucune des 4 variables d'environnement listées, pour construire un chemin
de fichier réel — tous les chemins de données sont des constantes internes
(`donnees_fictives/`, `resultats_artefact/`) jamais dérivées d'une entrée utilisateur.
Le garde-fou est donc aujourd'hui un fusible symbolique qui ne protège aucun accès
fichier réellement exercé par le code livré ; les contournements ci-dessus sont réels
sur la fonction de garde elle-même (elle ne tient pas la promesse du README : « casse
différente, séparateurs inhabituels » y compris), mais ne se traduisent pas, en l'état,
par une lecture effective de `data/` par `run.sh`. C'est un défaut de robustesse du
garde et un risque latent si le code évolue pour accepter un chemin en argument — pas
une fuite de données démontrée sur l'artefact tel qu'il est livré aujourd'hui.

## Autonomie et durée

- **Réseau** : aucun appel réseau pendant `run.sh` (recherché explicitement dans toute la
  cascade de 14 modules : aucun `requests`, `urllib`, `socket`, `hf_hub_download`, aucune
  URL appelée — la seule occurrence d'une URL dans la cascade est une chaîne de message
  d'aide inerte dans `a1_double_distorsion.py`, jamais exécutée). Seule la mise en place
  initiale de l'environnement (`pip install`) a besoin du réseau, et cela n'est pas
  documenté (voir écart n°1).
- **Données absentes du dépôt** : aucune. `data/` n'existe pas dans le clone (ignoré par
  git, confirmé absent après clonage) et n'est jamais lu.
- **Durée réelle** : très variable selon l'état du cache. Prembattre `run.sh` sur un
  venv fraîchement peuplé (`__pycache__` froid) : **23,17 s** réel. Deux exécutions
  consécutives suivantes (cache chaud) : **3,7 s** et **3,7 s**. Détail par étape (cache
  froid) : génération 0,29 s, attaque 1,73 s, défense 1,64 s, tableau final 0,22 s — soit
  3,9 s de calcul pur ; le reste du premier lancement (~19 s) est de la compilation
  bytecode/lecture disque première fois des paquets numpy/pandas/scipy/scikit-learn.
  Dans tous les cas, sous la barre des 5 minutes annoncée et cohérent avec le « environ
  25 secondes » du README (plutôt optimiste dans le sens où les runs suivants sont
  nettement plus rapides).
- **Python et dépendances réellement nécessaires** : Python 3.14.7 (testé, fonctionne,
  alors que le README parle de 3.10+ et `pyproject.toml` de ≥3.13 — voir écart n°2) ;
  paquets requis au minimum pour la chaîne d'import réellement empruntée : `numpy`,
  `pandas`, `scipy`, `scikit-learn` (les autres du `requirements.txt` — `matplotlib`,
  `pyreadstat`, `openpyxl`, `pyarrow`, `mlx*`, `transformers`, etc. — n'ont pas été
  constatés nécessaires pour `run.sh` lui-même, mais `requirements.txt` ne distingue pas
  ce sous-ensemble ; installer le fichier complet fonctionne et a été la voie suivie ici).

## Corrections à apporter, par gravité

**Critique**
- Aucune (aucune fuite de données réelles démontrée sur l'artefact tel que livré).

**Majeur**
- Ajouter dans `artefact/README.md` la commande d'installation des dépendances
  (`pip install -r requirements.txt` ou équivalent) avant `./artefact/run.sh` : sans
  cela, l'artefact ne démarre pas du tout pour un relecteur qui suit le texte à la
  lettre.
- Corriger ou compléter `garde.py` : comparaison de composants insensible à la casse,
  normalisation des séparateurs avant test (`chemin.replace("\\", "/")` avant split),
  et — le plus important — résolution du chemin réel (`os.path.realpath`) avant de
  juger, pour couvrir le cas des liens symboliques. La liste de 4 variables
  d'environnement devrait aussi soit s'élargir, soit être clairement documentée comme
  non exhaustive plutôt que présentée comme une protection générale.

**Mineur**
- Aligner la version Python annoncée entre `artefact/README.md` (« python3.10+ ») et
  `pyproject.toml` (« >=3.13 »).
- Mettre à jour la liste des modules importés en cascade dans `artefact/README.md`
  (7 cités, 14 réellement importés) pour que le tableau de traçabilité soit exact.
- Préciser dans le README que le chiffre « environ 25 secondes » correspond à un cache
  froid ; les exécutions répétées sont nettement plus rapides (~4 s), ce qui est plutôt
  une bonne nouvelle mais vaut d'être noté pour ne pas surprendre un relecteur qui
  chronomètre.
