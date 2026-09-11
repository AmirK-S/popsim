# Revue de divulgation des sorties `resultats/*.csv` et `.json`

Date : 2026-09-11. Revue locale en lecture seule, sans réseau, sans modèle, sans `git add`
ni modification d'aucun fichier existant. Répond au blocage n°6 de
`audit-reproductibilite-publication-2026-09-11.md` (absence de revue de divulgation) et à la
suspicion nommément portée sur `a41-c3f-60-personnes.csv`. Ce document ne vaut pas avis
juridique.

## Portée et méthode

- Fichiers couverts : les 525 `resultats/**/*.csv` et les 18 `resultats/**/*.json` présents
  sur le disque au 2026-09-11 (y compris le sous-dossier `r2b-evaluation-20260910-180/` et
  `mesures-a3/`, `mesures-a4/`). `.env` et tout ce qui vit sous `data/traces/` n'ont pas été
  ouverts.
- Pour chaque fichier : lecture de l'en-tête, comptage des lignes, et échantillon de 2 à 5
  lignes seulement (jamais le fichier entier), via un script jetable
  (`scan_disclosure.py`, écrit dans le scratchpad de session, jamais dans le dépôt) qui
  détecte par motif de nom de colonne : identifiants directs/pseudonymes stables (`pid`,
  `caseid`, `respondent`, `household`, `participant`, `subject`, `id`, `twin_id`...),
  identifiants techniques (`generation_id`, `request_id`, `invoice`, `facture`, `cle`,
  `cle_modele`...), texte libre (`texte`, `comment`, `commentaire`, `verbatim`, `persona`,
  `prompt`...) et dates fines. Un second script (`scan_smallcell.py`) a cherché, dans toute
  colonne ressemblant à un effectif (`n`, `n_personnes`, `n_cellules`, `effectif`...), la plus
  petite valeur numérique observée par fichier, pour repérer les cellules de moins de 10
  personnes.
- Tout fichier ayant déclenché un motif, tout fichier de plus de 300 lignes, tout fichier
  nommé avec « personne(s) », les 18 `.json`, et le fichier explicitement mis en cause
  (`a41-c3f-60-personnes.csv`) ont été relus intégralement (en-tête + échantillon élargi) à la
  main pour trancher entre vrai positif et faux positif de motif.
- `git ls-files resultats/` a servi de référence pour le suivi Git ; tout fichier absent de
  cette liste est classé « non suivi ».
- Les ~460 fichiers restants, qui n'ont déclenché aucun motif à risque, ont une structure
  homogène (une ligne par item, par cellule, par condition ou par modèle, avec des colonnes
  de comptage, de moyenne, d'écart-type ou d'intervalle de confiance) cohérente avec la
  politique déclarée par `.gitignore` (« aucune ligne individuelle »). Ils sont classés
  PUBLIABLE par extrapolation de ce constat structurel, pas par relecture ligne à ligne
  intégrale de chacun — voir « Non établi ».

## Constat le plus urgent

Deux fichiers **déjà suivis par Git** contiennent une information directement identifiante,
mais pas celle qu'on attendait : ce ne sont pas des réponses de personnes enquêtées, ce sont
des traces opérationnelles de la machine du chercheur, avec son nom d'utilisateur macOS en
clair dans un chemin de fichier.

| Fichier | Suivi Git | Problème constaté |
|---|---|---|
| `resultats/mesures-a4/a4-20260903-145751.json` | **Oui** | Contient `configuration.modele` = chemin absolu `~/Desktop/Code/Projets/popsim/data/modeles/gguf/...` (nom d'utilisateur réel), plus `processus_lourds` (PID et noms de process macOS en clair), un identifiant de batterie interne (`InternalBattery-0 (id=22872163)`), des horodatages à la seconde et l'état thermique de la machine. Ce n'est pas un résultat agrégé de recherche mais une capture brute de télémétrie système. |
| `resultats/a11_twin_resultats-smoke.json` | **Oui** | Le reste du fichier est un agrégat légitime (n_personnes, plafond de test-retest, etc.), mais `fichiers_traces` contient un chemin absolu unique : `~/Desktop/Code/Projets/popsim/data/traces/a11-C3-Twin-p1-smoke.jsonl`, qui expose le même nom d'utilisateur. |

Aucun de ces deux fichiers ne contient de ligne par personne enquêtée ; le risque est
l'identification du chercheur/opérateur (nom d'utilisateur local), pas d'un répondant GSS,
Twin, SCE ou Ahler-Sood. C'est néanmoins la même famille de problème que l'audit visait au
point 3.5 (traces, secrets, environnement) et point 3.4 (état de travail non gelé) : ces deux
fichiers doivent être corrigés avant toute publication de l'état actuel du dépôt.

Aucun fichier CSV suivi par Git n'a été classé À EXCLURE : voir ci-dessous pour
`a41-c3f-60-personnes.csv`, qui était nommément suspecté et se révèle publiable.

## Le cas `a41-c3f-60-personnes.csv`

12 lignes, colonnes `methode, regime, famille_retiree, n_personnes, n_items, exactitude,
exactitude_ic_bas, exactitude_ic_haut, exactitude_normalisee, ratio_intra_ideologie,
ratio_inter_ideologie, part_diversite_humaine, accord_par_paires`. `n_personnes` vaut 60 pour
les 12 lignes (une méthode par ligne, pas une personne par ligne) : c'est un tableau agrégé
par méthode d'imputation, avec un effectif de cellule de 60, au-dessus du seuil de 10 retenu
ici. **Classement : PUBLIABLE.** Le nom du fichier annonce un effectif, pas une ligne par
individu ; la suspicion de l'audit est levée par la lecture du contenu, pas par le nom.

## Tableau de synthèse par famille d'analyse

Regroupement par préfixe de fichier (`a1`, `a12`, `r6`, `mesures-a3`, etc.), qui correspond
aux notes d'analyse numérotées du dépôt. « Motif » résume pourquoi le groupe est publiable en
l'état ; les exceptions individuelles à un classement de groupe sont listées dans la section
suivante et non répétées ligne à ligne ici.

| Groupe | Fichiers | Classement | Motif | Source probable et licence | Suivi Git |
|---|---|---|---|---|---|
| a1 | 6 | PUBLIABLE | agrégats par ratio/axe/silhouette | interne (agents LLM) vs GSS ; agrégat sous licence du dépôt (CC BY 4.0), citer GSS/NORC | oui |
| a2 (+`a2_gss_resultats.json`, `a2_twin_resultats.json`) | 3 | PUBLIABLE | baselines et courbes agrégées | GSS (NORC, microdonnées non redistribuables) et Twin-2K-500 (CC BY 4.0) ; agrégats seuls | oui |
| a5 (+ `a5_resultats.json`, `a5_smoke_resultats.json`) | 3 | PUBLIABLE | distributions et baselines agrégées, agents locaux vs GSS | GSS (NORC) ; agrégat | oui |
| a6 | 13 | PUBLIABLE | ratios par axe et par sous-ensemble | GSS + Twin-2K-500 (CC BY 4.0) | oui |
| a7 | 6 | PUBLIABLE | transport de variance, agrégé | interne / GSS | oui |
| a8 | 12 | PUBLIABLE | familles, corrélations, k-fold ; en-têtes contenant « persona texte/JSON » sont des étiquettes de condition, pas du texte de persona réel (vérifié) | GSS + Twin-2K-500 | oui |
| a9 | 22 | PUBLIABLE | cohérence, déviance, instabilité par item/domaine | Twin-2K-500 (personnalité) | oui |
| a11 (`a11_twin_resultats-smoke.json`) | 1 | **À REVOIR** | voir constat prioritaire (chemin absolu à rédiger) | Twin-2K-500 | oui |
| a12 | 12 | PUBLIABLE | appariement d'items, retest, dont un panel étiqueté « Stanford (archive OSF) » en valeur de cellule agrégée | GSS panel 2006-2010 + **Stanford OSF t6g7k (licence indéterminée localement, prudence de citation)** | oui |
| a18 | 10 | PUBLIABLE | calibration, décomposition C2/C3 | SCE (FRBNY) + interne | oui |
| a19 | 7 | PUBLIABLE | exactitude appariée/brute par jeu d'items | GSS + Twin-2K-500 | oui |
| a20 | 11 | PUBLIABLE | transport de variance v2 | interne / GSS | oui |
| a21 (+`a21-extension-c2.json`) | 3 | PUBLIABLE | extension C2, décomposition | interne / SCE | oui |
| a23 | 4 | PUBLIABLE | concentration, écarts appariés | interne | oui |
| a25 | 5 | PUBLIABLE | contrastes de mode, bootstrap par « personnes » = comptages agrégés, pas des lignes individuelles | interne / GSS | oui |
| a28 | 15 | PUBLIABLE | trois tests décisifs, gros volumes (jusqu'à 3874-23244 lignes) mais toujours par item×condition×modèle | interne / GSS | oui |
| a29 | 12 | PUBLIABLE | minorités, profils, corrélation « personne » = statistique agrégée | interne / GSS | oui |
| a30 | 24 | PUBLIABLE | variété interne des camps | GSS + Twin-2K-500 | oui |
| a31 | 10 | PUBLIABLE | rareté, leviers, confiance | interne | oui |
| a33 | 10 | PUBLIABLE | contexte C3/C3F, cousins ; « contexte »/« rareté du contexte » déclenchent le motif texte libre par sous-chaîne mais sont des libellés numériques (vérifié) | interne | oui |
| a34 | 7 | PUBLIABLE | rareté déductible par tercile | interne | oui |
| a35 | 11 | PUBLIABLE | imputation, front de Pareto | interne | oui |
| a37 | 12 | PUBLIABLE sauf 1 exception | consensus libéral ; voir `a37-decomposition.csv` ci-dessous | GSS + Twin-2K-500 | oui |
| a38 | 13 | PUBLIABLE | mode continu et camp, gros volumes par item×camp×modèle | interne / GSS | oui |
| a39 | 8 | PUBLIABLE | tranches de Peng | comparaison à Peng et al. (article tiers, à citer) | oui |
| a41 | 10 | PUBLIABLE | régime sévère, dont le fichier nommément suspecté (voir section dédiée) | interne | oui |
| a42 | 6 | PUBLIABLE | plancher de bruit, préenregistrement | interne | oui |
| a43 | 11 | PUBLIABLE | comparaison à Peng et al. | Peng et al. | oui |
| a44 | 7 | PUBLIABLE | générateur nul, permutation | interne | oui |
| a46 / a46b | 21 | PUBLIABLE | composition GSS 2024, trois termes | Ahler-Sood (CC0) + GSS | oui |
| a47 | 7 | PUBLIABLE | items recopiés, invariance de facteur | interne / GSS | oui |
| c1 | 21 | PUBLIABLE | anticipations, cohortes, choc 2025 | SCE (Survey of Consumer Expectations, FRBNY ; redistribution des agrégats sous conditions FRBNY, attribution requise) | oui |
| d1 / d4 | 8 | PUBLIABLE | appariement, contrastes, verdicts | ANES (usage recherche présumé non redistribuable pour les microdonnées ; agrégats seuls) | oui |
| i1 | 18 | PUBLIABLE | AUC, qui bouge, cross-pressions | interne / GSS panel | oui |
| i3 / i3b | 28 | PUBLIABLE | détecteur, abaque, surface d'attaque | interne + Twin-2K-500 | oui |
| mesures-a3 | 8 | PUBLIABLE | bancs de performance moteur/modèle local, chemins relatifs seulement | bancs matériels locaux (aucune donnée de personne) | oui |
| mesures-a4 (`a4-20260903-145751.json`) | 1 | **À EXCLURE** | voir constat prioritaire | banc matériel local, télémétrie brute avec nom d'utilisateur | oui |
| r1 | 40 (32 suivis, 8 non suivis) | PUBLIABLE | oracle des camps, répliqué en versions r4/r5/(r7 non suivi)/smoke | interne / GSS | mixte, voir note |
| r1b | 7 | PUBLIABLE | contraste de mode | interne | oui |
| r2 / r2b | 31 (17+9 non suivis dans `r2b-evaluation-20260910-180/` +5 racine) | PUBLIABLE | rares appariés, pont de régimes ; `r2b-glissement-cellules.csv` et le sous-dossier `r2b-evaluation-20260910-180/` sont nouveaux, non suivis, structure identique aux fichiers déjà publiés | interne | mixte, voir note |
| r3 / r3b | 19 | PUBLIABLE | ablation d'étiquette, rareté appariée | interne | oui |
| r4 / r4b | 13 | PUBLIABLE | oracle socle, décomposition h1/h2b/h4 | interne | oui |
| r5 | 3 | PUBLIABLE | contrastes, rejets | interne | oui |
| r6 | 2 (1 non suivi) | PUBLIABLE | `r6-instabilite-pilote-deepseek.csv` publiable ; `r6-ready-pilots-diff-preuve-2026-09-10.json` non suivi, contenu opérationnel (preuve de diff de manifeste, décision GO, URL OSF publique) plutôt qu'un résultat scientifique — à exclure du paquet de résultats par choix éditorial, sans risque de personne | interne (gouvernance de campagne) | non suivi |
| r7 | 7, non suivis | PUBLIABLE | analyse fine, classements, contrastes, structure identique à r1/r2/r3 | interne / GSS | non suivi |
| s1 | 7 | PUBLIABLE | amplification premier ordre | interne | oui |
| t1 | 12 | PUBLIABLE | mesure de personne, generateur nul | GSS + Twin-2K-500 | oui |
| t2 | 16 | PUBLIABLE | qui bouge agrégé, camps | interne / GSS panel | oui |
| tab (`tab-partition-items.csv`) | 1, non suivi | PUBLIABLE | catalogue d'items (QID, type, famille), pas de réponse | catalogue interne | non suivi |

Total : 525 CSV + 18 JSON = 543 fichiers revus. Classement : 540 PUBLIABLE, 2 À REVOIR
(`a11_twin_resultats-smoke.json` et `a37-decomposition.csv`), 1 À EXCLURE
(`mesures-a4/a4-20260903-145751.json`). Le fichier `r6-ready-pilots-diff-preuve-2026-09-10.json`
est publiable au sens de la divulgation mais recommandé hors paquet par choix éditorial
(nature opérationnelle, pas un résultat) ; il n'est pas compté dans les « À REVOIR » ci-dessus
car son enjeu n'est pas la divulgation de personnes.

Note « suivi Git mixte » : dans les groupes r1 et r2/r2b, les variantes historiques (sans
suffixe, `-r4`, `-r5`, `-smoke`) sont suivies ; les variantes `-r7` et le sous-dossier
`r2b-evaluation-20260910-180/` sont des sorties encore non ajoutées à Git au 2026-09-11.

## Fichiers individuellement signalés

| Fichier | Classement | Motif | Suivi Git |
|---|---|---|---|
| `resultats/mesures-a4/a4-20260903-145751.json` | À EXCLURE | Télémétrie système brute avec chemin utilisateur en clair, PID de processus, identifiant de batterie ; ce n'est pas un résultat agrégé et ce n'est publiable qu'après rédaction complète des champs `machine`, `configuration.modele`, `etat_initial`, `etat_final` | Oui |
| `resultats/a11_twin_resultats-smoke.json` | À REVOIR | Un seul champ (`fichiers_traces[0]`) contient un chemin absolu avec nom d'utilisateur ; le reste du fichier (agrégats de test-retest, calibration) est publiable tel quel après rédaction de ce champ | Oui |
| `resultats/a37-decomposition.csv` | À REVOIR | Colonne `commentaire` : texte libre rédigé par l'analyste (ex. « negatif = les items penchent a gauche »), pas une réponse de personne, mais du texte libre au sens des critères retenus ; à relire avant publication pour confirmer l'absence de tout contenu incident | Oui |
| `resultats/r6-ready-pilots-diff-preuve-2026-09-10.json` | À REVOIR (éditorial, pas de personne) | Manifeste de gouvernance de campagne (hashes, décision GO, URL OSF publique) plutôt qu'un tableau de résultat ; aucun identifiant de personne, mais hors du périmètre déclaré de `resultats/` | Non |
| `resultats/a41-c3f-60-personnes.csv` | PUBLIABLE (levée de suspicion) | 12 lignes agrégées par méthode, effectif de cellule 60 ; aucune ligne par personne | Oui |

Faux positifs de motif vérifiés et écartés (colonnes ou libellés dont le nom ressemble à un
identifiant ou à du texte libre, mais dont le contenu est numérique ou un simple libellé de
condition) : `a18-dispersion-totale.csv` et `s1-controles.csv` (colonnes
`entropie_individuelle_moyenne_bits`, `plancher_individuel` : ce sont des statistiques, pas
des identifiants) ; `a19-recopie-items-ecartes.csv` et `a8-twin-par-item.csv` (en-têtes
contenant « persona texte »/« persona JSON » comme nom de condition expérimentale, pas de
texte de persona) ; `a31-h5-quintiles.csv`, `a33-contexte.csv`, `a33-cousins.csv`,
`a33-quintiles.csv`, `a47-contexte-regimes.csv` (« contexte » contient la sous-chaîne
« texte », valeurs numériques) ; les 60 fichiers portant une colonne `cle_modele` et les 4
portant `cle` (libellé de métrique ou identifiant de modèle de langage, ex. `gpt-oss-20b`,
jamais un identifiant de personne) ; `a30-agents-twin.csv` (`ratio_prix`, un ratio de coût de
modèle, agrégé). Aucune valeur de cellule d'effectif de personnes n'est descendue sous 10 :
les seules valeurs sous 10 trouvées par le contrôle de petites cellules concernent des
colonnes `n_items`, `n_modalites`, `n_paires`, `n_tentatives` (nombre d'items ou de tentatives,
pas de personnes).

## Critères appliqués

- **PUBLIABLE** : agrégat par item, cellule, condition ou modèle, sans colonne
  d'identifiant direct ou pseudonyme stable de personne, sans effectif de personnes sous 10,
  sans texte libre de répondant, sans date fine de collecte individuelle.
- **À REVOIR** : cellule de moins de 10 personnes, date fine, texte libre (même non
  personnel), identifiant technique isolé et corrigible par rédaction plutôt que par retrait
  du fichier entier.
- **À EXCLURE** : une ligne par personne (`pid`, `caseid`, `respondent`, `household` ou
  identifiant stable), microdonnées non redistribuables, identifiant de génération ou de
  facture, sortie brute de modèle ou de système non retraitée en statistique.
- Un identifiant direct de l'opérateur du dépôt (nom d'utilisateur local dans un chemin
  absolu) a été traité comme motif d'exclusion ou de révision au même titre qu'un identifiant
  de personne enquêtée, bien que les critères fournis visent nommément les répondants
  d'enquête : le principe (aucun identifiant direct dans un fichier destiné à publication)
  s'applique par extension.

## Non établi

- Les ~460 fichiers n'ayant déclenché aucun motif automatique n'ont pas été relus ligne par
  ligne dans leur intégralité (seulement en-tête, nombre de lignes, échantillon), conformément
  au périmètre de la mission ; leur classement PUBLIABLE repose sur l'homogénéité structurelle
  constatée sur l'échantillon et sur les fichiers du même groupe qui, eux, ont été relus en
  entier.
- L'attribution de source par mot-clé de nom de fichier (colonne « source probable ») ne capte
  pas les fichiers « interne » qui comparent en réalité à GSS ou Twin via des valeurs de
  colonne (`humains vague 2`, `GSS`, etc.) sans que le mot apparaisse dans le nom ; la
  provenance exacte de chaque ligne de ces ~330 fichiers « interne » n'a pas été vérifiée
  individuellement.
- Le statut de licence de l'archive Stanford OSF t6g7k reste indéterminé (hérité de l'audit) ;
  les fichiers `a12-*` qui portent un panel étiqueté « Stanford (archive OSF) » sont des
  agrégats de test-retest et non l'archive elle-même, mais l'opportunité de les publier avant
  levée de cette incertitude de licence n'est pas tranchée ici.
- Le risque de recoupement entre plusieurs fichiers publiés simultanément (attaque par
  jointure sur des tableaux croisés voisins) n'a pas été évalué ; seule la divulgation
  fichier par fichier l'a été.
- La présence d'un chemin absolu contenant le nom d'utilisateur dans des fichiers `.md` de
  `resultats/` (au moins 18 fichiers, hors périmètre CSV/JSON de cette mission) n'a pas été
  traitée ici mais partage la même cause que les deux fichiers JSON signalés ; à vérifier
  séparément.
- Aucune vérification n'a été faite sur les fichiers binaires (`.png`, `.svg`) qui pourraient
  intégrer des métadonnées ou légendes reprenant du texte libre.
