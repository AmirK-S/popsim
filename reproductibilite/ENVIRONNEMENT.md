# Environnement d'execution

Etabli le 2026-09-11. Ce document leve le bloquant n° 1 de
`resultats/audit-reproductibilite-publication-2026-09-11.md` : l'absence totale de
declaration d'environnement. Il ne leve aucun des autres bloquants (manifeste de sorties,
licence Stanford/GSS, gel Git, scan de secrets, revue de divulgation).

## Ce qui est declare

| Fichier | Role |
|---|---|
| `pyproject.toml` | Metadonnees du projet, `requires-python`, dependances avec bornes basses. |
| `requirements.txt` | Releve epingle (`==`) de l'environnement observe, avec sa cloture transitive. |
| `reproductibilite/dependances.json` | Registre machine-readable anterieur, conserve tel quel. |

## Environnement observe

- Python : 3.13.14 (main, Jun 10 2026), Clang 21.0.0.
- Plateforme : `macosx-26.0-arm64` (Darwin 25.6.0, Apple Silicon).
- Interpreteur releve : `.venv/bin/python` du depot.
- Methode : `pip list --format=freeze` pour les versions, puis analyse statique `ast` des
  fichiers `.py` de `analyses/` et `protocoles/` pour les imports.

## Recreer l'environnement depuis un clone neuf

```sh
python3.13 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt
```

Sur une machine qui n'est pas en Apple Silicon, les lignes `mlx`, `mlx-lm` et `mlx-metal`
sont neutralisees par leurs marqueurs de plateforme : l'installation aboutit, mais le banc
d'inference local ne fonctionne pas. Le coeur analytique, lui, ne depend pas de MLX.

Variante par bornes basses, si l'on accepte des versions plus recentes que celles relevees :

```sh
.venv/bin/python -m pip install .                      # coeur analytique
.venv/bin/python -m pip install '.[modeles-locaux]'    # + inference MLX
```

`pyproject.toml` n'installe aucun module : il declare seulement l'environnement. Le mode
editable (`-e`) n'a pas ete teste.

## Ce que ce releve garantit

- La version de Python sous laquelle le code a effectivement tourne.
- La liste exhaustive des paquets tiers importes par le code, avec la version installee.
- Un ensemble de versions qui, prises ensemble, etaient co-installees et fonctionnelles sur
  la machine d'origine le 2026-09-11.

## Ce que ce releve ne garantit pas

- **Ce n'est pas un lockfile.** Aucune resolution transitive n'est figee ni prouvee complete :
  la cloture listee est celle observee, pas celle qu'un resolveur recalculerait.
- **Aucun hash de roue** n'est enregistre. Rien ne verifie que la roue reinstallee demain est
  l'artefact installe le 2026-09-11.
- **Une seule plateforme observee** : macOS 26 arm64. Les roues de `pyreadstat`, `pyarrow`,
  `scipy` et `mlx` sont compilees par plateforme ; l'equivalence numerique sur Linux x86-64
  n'a pas ete testee.
- **Pas de determinisme numerique.** Les versions n'impliquent ni graines, ni ordre de
  threads BLAS identique, ni resultats bit a bit reproductibles.
- **Rien sur les outils externes** : `llama.cpp`, poids GGUF, executables de conversion et
  API distantes restent hors de ce perimetre (voir `modeles.json`).

## Paquets declares et usage dans le code

Comptes d'occurrences etablis sur les fichiers `.py` de `analyses/` accessibles a cette
passe (175 fichiers sur 200 ; voir la limite declaree plus bas).

| Paquet | Version relevee | Ou il sert |
|---|---|---|
| `numpy` | 2.5.2 | Socle numerique, present dans 157 fichiers : tirages, permutations, agregats, distances. |
| `pandas` | 3.0.5 | Chargement et pivots des jeux (Twin, GSS, SCE, Ahler-Sood), 144 fichiers ; tables de `resultats/`. |
| `scipy` | 1.18.1 | 19 fichiers : `scipy.stats` (rangs, correlations, lois), `scipy.optimize.linear_sum_assignment`, `scipy.special`, `scipy.sparse` ; egalement `protocoles/p1-puissance.py`. |
| `matplotlib` | 3.11.1 | Toutes les figures, 36 fichiers, dont les modules `*_figure*.py`. |
| `scikit-learn` | 1.9.0 | Baselines et structure (`a2_baselines_*`, `a30_structure`, `a28_commun`, `a34_commun`), 15 fichiers. |
| `pyreadstat` | 1.3.6 | Lecture des fichiers Stata du panel (`pyreadstat.read_dta`) : `a12_retest_delai`, `a12_sensibilite_dk`, `i1_commun`, `r4_oracle_socle`. |
| `openpyxl` | 3.1.5 | Lecture en mode seul-lecture des classeurs Excel de la source SCE (`c1_commun.py`). |
| `pyarrow` | 25.0.1 | Moteur parquet. Jamais importe, mais requis par `pd.read_parquet` / `to_parquet` dans `a11_agents_locaux_twin.py`, `a2_telecharger_twin.py`, `c1_commun.py`. |
| `threadpoolctl` | 3.6.0 | Bridage explicite des threads BLAS (`r2b_evaluer.py`) ; par ailleurs dependance de scikit-learn. |
| `mlx`, `mlx-lm` | 0.32.2, 0.31.3 | Inference locale sur Apple Silicon (`a3_banc_inference.py`). Extra `modeles-locaux`. |
| `tokenizers` | 0.23.1 | Declare par `dependances.json` pour la validation de checkpoints. Non verifie par cette passe. Extra `modeles-locaux`. |

Les telechargements de sources (`a2_telecharger_twin.py`, `a6_telecharger_twin_specs.py`,
`a8_telecharger_twin_llm.py`, `a12_telecharger_panel.py`) utilisent la bibliotheque standard
et n'ajoutent aucune dependance.

## Verification effectuee le 2026-09-11

Venv jetable cree hors du depot, avec le Python 3.13.14 du `.venv`, sur la meme machine.

| Controle | Resultat |
|---|---|
| `pip install -r requirements.txt` | Code de sortie 0, 54 paquets installes. |
| `pip check` | « No broken requirements found. » |
| `pip freeze` du venv jetable compare a celui de `.venv` | Identique, a une ligne pres : `pypdf`, volontairement exclu. |
| Compilation complete des fichiers accessibles | 176 fichiers (175 de `analyses/`, plus `protocoles/p1-puissance.py`), aucune erreur. |
| Execution des instructions d'import non locales de ces fichiers | 1 069 instructions, 0 echec. |
| Moteur parquet | Aller-retour `to_parquet` / `read_parquet` en memoire reussi. |
| MLX | `import mlx.core, mlx_lm, tokenizers` reussi ; operation `mx.array` executee. |
| `pyproject.toml` | Roue `popsim-0.1.0-py3-none-any.whl` construite sur une copie hors depot ; extra `modeles-locaux` resolu en `--dry-run`. |

Ce que cette verification ne couvre pas :

- **Pas une installation depuis une machine vierge.** 68 roues sur 108 lignes de
  telechargement provenaient du cache pip local ; meme machine, meme plateforme.
- **Les imports entre modules du projet n'ont pas ete executes**, ni aucun script : ils
  peuvent lire `data/` au chargement. Seuls les imports de paquets tiers et standard l'ont ete.
- **Aucune analyse n'a ete relancee** ; rien ne montre qu'une table ou une figure de
  `resultats/` est reproduite a l'identique avec cet environnement.
- Les 25 fichiers `r6_*` et `r7_*` n'ont ni ete compiles ni vu leurs imports testes.

## Limites de cette passe et ecarts avec `dependances.json`

1. **25 fichiers sur 200 n'ont pas ete lus** : ceux dont le nom contient `r6_` ou `r7_`,
   en cours de modification par un autre intervenant. Leurs imports ne sont donc pas couverts
   par l'analyse statique. `dependances.json` attribue `tokenizers` a la validation de
   checkpoints R7 ; cette attribution est reprise telle quelle, sans verification
   independante, et `tokenizers` est place dans l'extra plutot que dans le coeur.

2. **Ecart avec `dependances.json` : `pyarrow` y est absent.** Le registre liste les imports
   directs, et `pyarrow` n'est jamais importe ; il est neanmoins indispensable a l'execution
   des appels parquet. Le registre n'a pas ete modifie. C'est un manque a corriger a sa
   prochaine mise a jour, pas une contradiction de versions.

3. **Cloture transitive plus large que dans `dependances.json`.** Le registre liste 18
   dependances transitives ; le releve en epingle 42 (41 plus `mlx-metal`), dont `huggingface_hub`, `httpx`,
   `safetensors`, `tqdm`, `regex` et `typer` tires par `transformers` et `tokenizers`. Le
   registre le reconnait lui-meme (« seulement celles observees et attribuables »). Les 11
   versions d'imports directs et les 18 versions transitives du registre sont identiques au
   releve : aucune version ne le contredit.

4. **Deux paquets du `.venv` ne sont declares nulle part** car aucun code accessible ne les
   importe : `pypdf` 6.18.0 et `pip` 26.1. Ils sont volontairement exclus : on declare ce qui
   est utilise, pas le contenu du venv.
