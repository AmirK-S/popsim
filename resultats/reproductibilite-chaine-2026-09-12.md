# Reproduction de la chaîne complète depuis un clone vierge — 12 septembre 2026

Objectif : rejouer, depuis un clone GitHub propre (pas le dépôt de travail), les scripts qui
produisent les chiffres mis en avant par `resultats/article-synthese.md`, et comparer chiffre
à chiffre avec ce qui est publié. Aucun appel d'API payant, aucun réseau au-delà du clone
initial, tout en avant-plan. Deux calculs ont dépassé le délai d'une commande et ont été soit
réduits (déclaré ci-dessous), soit interrompus puis relancés avec des paramètres réduits.

## 0. Provenance du clone

```
git clone https://github.com/AmirK-S/popsim.git
```

Commit obtenu : **975e87f8f090153ef8135499ab148aacea8ec063** (« LaTeX : figures synchronisees
automatiquement, garde-fou et artefacts ignores »). Clone placé dans le scratchpad de session,
jamais dans le dépôt de travail. `data/` n'est pas versionné (confirmé par `.gitignore` :
`data/`, `*.dta`, `*.sav`, `*.parquet`, `*.csv`, sauf `resultats/*.csv`) : un clone nu ne peut
rien calculer qui touche Twin-2K-500 ou l'archive Park.

Environnement recréé selon `reproductibilite/ENVIRONNEMENT.md` : Python 3.13.14, venv dédié,
paquets **directement importés** par les scripts ciblés installés aux versions épinglées de
`requirements.txt` (numpy 2.5.2, pandas 3.0.5, scipy 1.18.1, scikit-learn 1.9.0, pyreadstat
1.3.6, openpyxl 3.1.5, pyarrow 25.0.1, threadpoolctl 3.6.0). matplotlib/mlx/transformers non
installés : aucun script ciblé ne les importe (vérifié par grep des `import` avant
l'installation). Accès aux données locales via un **lien symbolique en lecture**
`clone/data -> data/` du dépôt de travail ; aucune écriture constatée dans `data/` par les
scripts exécutés (vérifié par grep des appels d'écriture avant exécution).

## 1. Vérification statique (gratuite, avant tout calcul)

`python -m py_compile` sur les 254 fichiers de `analyses/` du clone : **0 erreur de syntaxe**.
Ne garantit rien sur l'exécution (imports circulaires, chemins de données, dépendances
runtime), seulement l'absence de fautes de syntaxe Python 3.13.

## 2. Catégories

### (a) Tourne depuis le clone seul, sans donnée réelle

- `analyses/verifier_paquet_public.py` (mentionné par `reproductibilite/USAGE.md`) — non testé
  faute de temps, mais ne dépend d'aucune donnée.
- Tout script dont l'en-tête annonce « aucune donnée réelle » (ex. `artefact/`) — non exploré
  ici, hors périmètre des revendications de tête.

### (b) Tourne depuis le clone + données locales en lecture seule (catégorie testée ici)

Six scripts rejoués avec succès, code de sortie 0, aucune écriture hors `resultats/` du clone
ou du scratchpad :

| Script | Rôle | Durée mesurée |
|---|---|---|
| `analyses/a0_diversite_osf.py` | Premier résultat du README | 0,4 s |
| `analyses/c7_attaquant_fort.py` | Attaquant fort, monde ouvert, défense, adaptatif (A3, A8, A11) | 81 s |
| `analyses/c7_fort_monde_ouvert_ic.py` | IC bootstrap du 60,17 % et voisins (A3) | 359 s, complet (voir §4) |
| `analyses/c7_transfert.py` | Canal inter-jumeaux (A7) | 521 s |
| `analyses/c7_disjoint.py` | Corrélation fidélité/fuite sur items disjoints (A1) | 204 s, **réduit** (voir §3) |
| `analyses/c7_nul_corrige.py` | Témoins corrigés du nul de marge (A1, abandonnés par l'article) | ~600 s, **interrompu deux fois** (voir §3 et §5) |

### (c) Ne tourne plus / ne peut pas être rejoué depuis le dépôt publié

- **Le script qui produit le chiffre qui « fait autorité » pour le témoin de marge (rho 0,974
  contre 0,965, cité comme définitif par `resultats/article-synthese.md` §1 et A1) n'existe pas
  dans le dépôt versionné.** Voir §5 : découverte la plus importante de cet audit.
- `analyses/c7_nul_corrige.py`, lui, est bien versionné mais dépend par défaut d'un chemin en
  dur non portable (§6, obstacle n°1).
- Aucun autre script n'a été identifié comme cassé dans le sous-ensemble testé ; le reste des
  ~250 scripts de `analyses/` n'a pas été rejoué (voir §7, hors du périmètre de tête faute de
  temps).

## 3. Réductions déclarées

- `analyses/c7_disjoint.py` : `--splits 10 --nul 20` au lieu des valeurs préenregistrées
  (`--splits 50 --nul 100`). Conséquence directe : ma moyenne Spearman sur 10 partages
  (0,9781, IC [0,9465 ; 0,9984]) n'est **pas directement comparable** à la moyenne publiée sur
  50 partages (0,969, IC [0,937 ; 0,993]) — ordre de grandeur et robustesse (100 % des partages
  > 0,7) confirmés, valeur exacte non revérifiée à taille pleine faute de temps.
- `analyses/c7_nul_corrige.py` : tentative `--replicats 10 --bootstrap 300` au lieu de 100/2000
  (préenregistrés). Calcul toujours trop long (~150-230 s par construction sur 7
  constructions) : interrompu avant la fin après avoir couvert « reel », « N0 » et une partie de
  « N1 »/« N1b » (voir §5 pour ce que ces résultats partiels montrent).
- `analyses/c7_fort_monde_ouvert_ic.py` : une réduction a été **tentée** (surcharge des
  constantes `N_BOOT_FIGE`/`N_BOOT_REESTIME` avant l'appel à `main()`) mais **n'a pas eu
  d'effet** — les valeurs par défaut du script sont capturées comme valeurs par défaut
  d'arguments de fonction au moment de la définition, donc figées avant toute surcharge de
  variable de module après import. Le calcul a donc tourné à **pleine échelle** (2000 tirages
  « figés » + 300 tirages « ré-estimés » par jeu), et a terminé en 359 s : la réduction visée
  était inutile, mais je le signale car une tentative de réduction a bien eu lieu, sans succès,
  et le résultat obtenu est donc le résultat complet, pas un résultat dégradé.

## 4. Comparaison chiffre à chiffre — revendications de tête

Toutes reproduites depuis `analyses/c7_attaquant_fort.py` et `analyses/c7_fort_monde_ouvert_ic.py`,
graines fixées, **égalité stricte à la précision publiée** :

| Chiffre publié | Valeur obtenue | Écart |
|---|---|---|
| Park, monde ouvert, TPR @ 1 % FPR = **60,17 %** [54,5 ; 64,4] | 60,17 % [reestime 54,52 ; 64,41] | **aucun** |
| Twin, monde ouvert, TPR @ 1 % FPR = **4,28 %** [3,3 ; 5,6] | 4,28 % [reestime 3,29 ; 5,64] | **aucun** |
| Park, TPR @ 0,1 % FPR = **44,37 %** [23,3 ; 53,8] | 44,37 % [reestime 23,34 ; 53,76] | **aucun** |
| Twin, TPR @ 0,1 % FPR = **1,01 %** [0,05 ; 2,82] | 1,01 % [reestime 0,05 ; 2,82] | **aucun** |
| Park, monde fermé A-LLR hors pli, top-1 = **90,40 %** | 90,40 % [88,59 ; 92,21] | **aucun** |
| Twin, monde fermé A-LLR hors pli, top-1 = **23,23 %** | 23,23 % | **aucun** |
| Défense D4 sous attaquant fort recalibré = **0,24 %** | 0,24 % [0,05 ; 0,49] | **aucun** |
| Défense D4 sous attaquant adaptatif (S1, S1+S3) = **0,29 %** | 0,29 % (S1 = S1+S3 = 0,0029, identiques comme annoncé) | **aucun** |
| FP absolus @ 0,1 % : ≈ 1 (Park), ≈ 2 (Twin) | 1,05 / 2,06 | **aucun** |

Canal inter-jumeaux (`analyses/c7_transfert.py`, retabulation manuelle par nombre d'items
communs à partir de `resultats/c7-transfert-voletA.csv`, la même retabulation que celle
décrite dans `article-synthese.md`) :

| Chiffre publié | Valeur obtenue | Écart |
|---|---|---|
| 30 paires à 60 items communs, top-1 moyen **36,4 %** | 36,38 % | **aucun** (arrondi identique) |
| 12 paires à 19 items communs, top-1 moyen **0,45 %** | 0,45 % | **aucun** |
| Contrôle anti-artefact, paires à 60 items = **0,04 %** | 0,04 % | **aucun** |
| Contrôle anti-artefact, paires à 19 items = **0,10 %** | 0,10 % | **aucun** |
| Demographics Only contre les riches = **7,76 %** | 7,76 % | **aucun** |

**Obstacle pratique associé (à corriger avant dépôt) :** le « resume volet A » que
`analyses/c7_transfert.py` **imprime lui-même** à la fin de son exécution donne
**top1 moyen, paires riches (n=42) : 0,2611** — c'est le chiffre unique à 26,11 % que
`article-synthese.md` interdit explicitement de publier (« un chiffre unique moyennant les
deux régimes d'items (l'ancien 26,11 %) »). Un relecteur qui se contente de lancer le script et
de lire sa sortie standard obtient le chiffre retiré, pas le 36,4 % / 0,45 % cité par l'article
: la retabulation par nombre d'items communs n'est **pas automatisée dans le script**, elle
doit être refaite à la main sur le CSV (comme je l'ai fait ci-dessus). Le script devrait
imprimer directement la ventilation par `n_items`.

Témoin de marge (rho nul contre rho observé, A1) — voir §5, résultat partiel et discordant.

## 5. Découverte principale : le témoin de marge « qui fait autorité » n'est pas reproductible depuis le dépôt

`resultats/article-synthese.md` désigne le couple **rho nul 0,974 [0,950 ; 0,993] contre 0,965
observé** comme « chiffres qui font autorité », sourcés dans
`resultats/audit-renversement-2026-09-12.md`. Ce document indique lui-même, dès sa deuxième
ligne : *« Tout recalculé en avant-plan ; scripts d'audit dans le scratchpad de session
(`audit2.py`, `audit_contre_nul.py`, `audit3.py`) »*.

**Vérifié : ces trois scripts ne sont pas versionnés.**

```
git ls-files | grep -iE "audit2|audit3|audit_contre_nul"   ->  (vide)
```

Ils n'existent que comme fichiers de scratchpad d'un agent, jamais commités. **Un relecteur
d'artefact qui clone le dépôt public n'a aucun moyen de rejouer le calcul qui produit le
chiffre que l'article présente comme définitif pour son résultat central (A1, figure 2).** Ce
n'est pas un script qui « ne tourne plus » : c'est un script qui n'a jamais été publié.

En parallèle, le script *versionné* qui traite ce même sujet, `analyses/c7_nul_corrige.py`,
calcule des témoins différents (N0 à N3/N1b/N2b) — et l'article dit explicitement que leurs
résultats sont **abandonnés** (« le "renversement" de `c7-nul-corrige-resultats.md` est
abandonné [...] n'appliquer aucune des six modifications de son §7 »). Rejeu partiel (interrompu
avant la fin, §3) :

- construction « **reel** » (le prédicteur publié lui-même) : **rho = 0,9650**, identique à la
  valeur « observée sur les 12 configurations » citée par l'article (0,965) — **aucun écart**.
- construction « N0 » (nul cassé d'origine, importé tel quel) : rho moyen = 0,9839 sur 10
  réplicats — cohérent avec l'ancien couple publié puis retiré (« nul 0,984 contre 0,969 sur
  items disjoints »).
- construction « N1 » (mode de segment) : rho moyen = 0,1918, très en dessous de l'observé —
  confirme indépendamment que ce témoin corrigé **ne reproduit pas** le couplage, cohérent avec
  la décision de l'article de l'abandonner.
- N1b (rho = 0,3482 sur le seul réplicat vu avant interruption) : même constat.
- N2, N2b, N3 non atteints avant interruption.

**Conclusion de cette section** : la valeur « observée » (0,965) est bien reproductible depuis
le clone, à l'identique. La valeur « nulle » qui l'accompagne dans le texte définitif de
l'article (0,974) ne l'est pas, parce que son script n'est pas publié ; le script publié qui
traite ce sujet calcule autre chose, et ce autre chose confirme (sans le prouver au même
niveau de précision, faute d'avoir terminé le calcul) que ces témoins-là ne tiennent pas la
comparaison — ce qui est cohérent avec la décision de l'article de les abandonner, mais ne
permet pas de vérifier le 0,974 lui-même.

## 6. Obstacles pratiques, classés par gravité

1. **[Bloquant pour la relecture]** Le script produisant le chiffre « qui fait autorité » du
   témoin de marge (0,974 contre 0,965) n'est pas dans le dépôt (§5). À publier avant dépôt, ou
   à retirer la mention « qui fait autorité » du texte.
2. **[Défaut réel, contournable]** `analyses/c7_nul_corrige.py`, ligne ~108-111 : le chemin de
   cache par défaut (`C7_NUL_CACHE`) est une valeur codée en dur, propre à une machine et à une
   session (`/private/tmp/claude-501/.../scratchpad/...pkl`). Sur toute autre machine, ce chemin
   n'existe pas ; le script fonctionne quand même car il régénère le cache si absent — mais un
   relecteur pressé qui verrait le chemin dans les logs pourrait croire, à tort, qu'il manque un
   fichier. Corrigible en une ligne (chemin relatif au dépôt, ou variable d'environnement sans
   valeur par défaut absolue). Ce défaut avait déjà été signalé indépendamment par
   `resultats/audit-renversement-2026-09-12.md` §2 (« Chemin de cache non reproductible ») ;
   cet audit le confirme de façon indépendante.
3. **[Ergonomie, pas un bug]** `analyses/c7_transfert.py` imprime un agrégat (26,11 %) que
   l'article interdit de citer, sans imprimer la ventilation par nombre d'items qui, elle, est
   citée (§4). À corriger avant dépôt pour éviter qu'un relecteur ne cite le mauvais chiffre en
   lisant seulement la sortie du script.
4. **[Durée]** Trois scripts sur six dépassent la minute (81 s, 204 s pour une version réduite,
   359 s, 521 s) ; `c7_nul_corrige.py` dépasse largement les 10 minutes à pleine échelle (calcul
   interrompu deux fois dans cet audit). Pour un relecteur qui n'a pas accès à des scripts à
   paramètres réduits comme ceux improvisés ici, la durée seule n'empêche pas la reproduction
   mais devrait être documentée dans `reproductibilite/USAGE.md` (aucune estimation de durée
   n'y figure aujourd'hui).
5. **[Dépendance non déclarée mais bénigne]** `analyses/c7_nul_corrige.py` s'appuie sur
   `analyses/c7_disjoint.construire_nul` et sur un cache de prédicteurs statistiques
   (`t1_baselines`) : aucun problème constaté, seulement signalé car c'est le genre de couplage
   inter-scripts qu'un clone frais peut casser silencieusement s'il manque un fichier
   intermédiaire — ici il ne manquait rien.

Aucun chemin absolu propre à la machine d'origine (hors le cache ci-dessus) n'a été rencontré
dans les six scripts exécutés ; aucune dépendance non déclarée dans `requirements.txt` n'a été
rencontrée pour ces six scripts (le sous-ensemble minimal installé a suffi).

## 7. Ce qui n'a pas été couvert

- Les scripts d'appel de modèle (A9, A11 volet payant, `c7_fort.py`, `c7_dp.py`,
  `c7_utilite_aval.py`, `c7_stanford*.py`, `c7_bits.py`, `c7_mecanisme.py`,
  `c7_courbe_gen.py`, `c7_generateur.py`, `c7_synth_ajuste.py`, `c7_echelle.py`,
  `c7_deviations.py`, `c7_anomalie_park.py`, `c7_temoin_prompt.py`, `c7_deux_organisations.py`,
  `c7_monde_ouvert.py`/`c7_monde_ouvert_ic.py` en tant que tels — seul leur usage importé par
  `c7_attaquant_fort.py` a été exercé) n'ont pas été rejoués individuellement, faute de temps.
- Les figures (`analyses/c7_compromis_figure.py` et consorts) n'ont pas été régénérées.
- Le témoin de marge complet (N2, N2b, N3 de `c7_nul_corrige.py`) n'a pas été atteint avant
  interruption ; sa reprise demanderait encore ~15-20 minutes en une seule commande, au-delà du
  budget de cet audit.
- Les ~250 autres fichiers de `analyses/` n'ont subi qu'une vérification syntaxique (§1), jamais
  une exécution.
- Aucune vérification de licence, de conformité éthique ni de contenu de `data/` (hors
  lecture par les scripts eux-mêmes) n'a été tentée : hors périmètre de cette mission.
