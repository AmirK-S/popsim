# Audit de reproductibilité et de publication

Date : 2026-09-11. Audit local en lecture seule, sans réseau ni modèle. Les fichiers
potentiellement secrets et le contenu des traces brutes n'ont pas été lus. Ce document ne
vaut pas avis juridique : il restitue les licences et provenance présentes localement.

## Verdict

Le code et les textes peuvent être préparés à la publication, mais le dépôt n'est pas encore
un paquet exécutable depuis un clone neuf. Le blocage principal est reproductible, non
scientifique : absence de manifeste de dépendances et de verrou d'environnement, absence de
manifestes de données et de poids publiables, et état Git non gelé. Les microdonnées et les
traces doivent rester hors du dépôt public.

Le plus petit paquet propre et exécutable est un sous-paquet Twin-2K-500 qui télécharge lui-même
les fichiers CC BY 4.0 nécessaires, ne distribue aucune copie locale des personnes et ne
contient aucune génération nouvelle.

## 1. Publiable maintenant

| Élément | Statut et condition de publication |
|---|---|
| Code suivi par Git | La licence racine est MIT. Publier après gel d'un commit, avec licence, notice de version et tests réellement exécutés. |
| Textes, protocoles, corpus et rapports | La licence racine les place sous CC BY 4.0. Les rapports doivent conserver leurs errata, leur statut exploratoire ou confirmatoire et la portée exacte de chaque résultat. |
| Tableaux et figures agrégés de `resultats/` | La politique du dépôt les déclare agrégés. Ils sont publiables seulement après contrôle de colonnes et petites cellules : l'exception Git `!resultats/*.csv` ne démontre pas qu'un CSV ne contient pas une ligne de personne. Le fichier nommé `a41-c3f-60-personnes.csv` exige notamment une revue de divulgation avant diffusion. |
| Twin-2K-500 via sa source officielle | La copie locale documente CC BY 4.0 et 2 058 personnes. Le code, les instructions de téléchargement et les résultats agrégés peuvent être publiés avec attribution et lien à la version source. Les fichiers locaux de réponses, `pid`, personas libres et données brutes Qualtrics ne sont pas nécessaires au dépôt. |
| Ahler-Sood, par renvoi | `data/ahler-sood-pcomp/PROVENANCE.md` documente CC0 1.0. Les agrégats produits et le code peuvent sortir; il est néanmoins préférable de renvoyer au DOI Dataverse plutôt que de dupliquer les fichiers individuels. |
| SCE, par renvoi | La provenance locale indique que FRBNY autorise redistribution sous ses conditions et avec sa mention de source. Le choix le plus sûr reste un script d'acquisition et l'attribution FRBNY, plutôt que de joindre 186 Mo de microdonnées et d'identifiants longitudinaux. |
| Préenregistrements | R5 peut être décrit comme déposé selon son texte local. R6 et R7 ne doivent être décrits que comme « enregistrés, statut rapporté Pending approval, sans DOI », car les preuves locales disent explicitement qu'elles dérivent de l'interface observée par le parent, sans vérification indépendante. R1, R2, R2b et T1 doivent conserver la formule « plan horodaté localement » lorsqu'aucun dépôt tiers n'est démontré. |

## 2. À exclure du paquet public ou à remplacer

| Élément | Motif | Remplacement public |
|---|---|---|
| `data/gss-panel/` | Les conditions NORC documentées localement interdisent la redistribution. | Script d'acquisition, nom de fichier, version, SHA-256, citation NORC et adaptateur qui lit un chemin fourni par le chercheur. |
| Microdonnées ANES | Les données ne sont pas présentes, et la provenance indique un usage de recherche et une absence de redistribution à présumer. | Codebooks déjà publics, script d'import et instruction d'obtention par le chercheur. |
| `data/osf-t6g7k-stanford/` | L'archive contient des réponses individuelles et la licence exacte, ainsi que les conditions d'usage du GSS sous-jacent, sont explicitement marquées « à vérifier avant tout usage publié ». | Ne publier que le code, les sorties agrégées contrôlées, les empreintes et un script qui demande au chercheur d'obtenir lui-même l'archive selon ses conditions. |
| `data/traces/`, `data/traces-r2b/` et ledger R6 | 319 fichiers de traces, journaux, reprises, verrous et états opérationnels sont présents. Ils peuvent contenir sorties brutes, identifiants de génération, coûts, horaires ou détails de reprise. | Tables agrégées expurgées, schéma de trace synthétique et tests avec fixtures fictives. Ne jamais publier une trace brute ou un journal de run par défaut. |
| `.env` | Présent et ignoré. Le client R6 le lit pour `OPENROUTER_API_KEY`. | `.env.example` sans valeur, documentation des variables et tests qui ne lisent jamais de clé. |
| Poids et conversions GGUF | `data/modeles` pointe hors projet vers environ 42 Gio de poids. Les licences et révisions diffèrent par modèle; les poids ne sont ni suivis ni inclus. | Manifestes par modèle: dépôt amont, révision ou commit, licence, SHA-256 du poids et du GGUF dérivé, commande de conversion, tokenizer et version de `llama.cpp`. |
| Journaux, notes de coordination et fichiers personnels | La `.gitignore` exclut déjà journaux, brainstorms, décisions, passation, contexte opérationnel et fichiers de demandes. | Un changelog de recherche expurgé, rédigé pour publication, sans noms de machine, PIDs, comptes, clés, soldes ou identifiants de requête. |
| Scripts de files de nuit | Cinq scripts `file*_nuit*.sh` contiennent un chemin absolu vers le poste local. Ils ne sont pas portables et appellent des runs. | Les exclure du paquet minimal. Pour un paquet complet, les remplacer par une CLI relative à la racine avec configuration explicite et mode simulation. |

## 3. Éléments bloquants avant une archive reproductible

1. Aucun `pyproject.toml`, `requirements.txt`, fichier Conda, lockfile, Dockerfile ou Makefile
   n'est présent. Python 3.13.14 est observé localement, mais les versions effectives de
   NumPy, pandas, SciPy, matplotlib, scikit-learn et lecteurs de formats ne sont pas
   déclarées par le projet.

2. Aucun manifeste de publication ne relie une version Git, les tables finales, les figures,
   leurs hashes, les graines, les commandes et les entrées de données. Les scripts sont
   nombreux et importent fortement les uns les autres; un lecteur ne dispose pas d'une
   commande unique pour reproduire une figure.

3. La licence Stanford/GSS sous-jacente est indéterminée dans la provenance locale. Il faut
   lever cette condition avant de joindre tout dérivé qui pourrait permettre une
   ré-identification ou une redistribution substantielle.

4. L'arbre de travail est actif et contient des modifications et fichiers non suivis, dont
   des artefacts R6/R7. Il faut créer un commit ou une archive de publication propre, puis
   générer les résultats depuis cet état gelé.

5. Une recherche de noms de fichiers a trouvé `.env`, sans en lire le contenu. Le code R6
   construit un en-tête Bearer à partir de cette clé. L'absence de secret dans un futur
   export doit être vérifiée sur l'archive effectivement mise en scène par un scanner de
   secrets, pas inférée de `.gitignore`.

6. Les sorties publiques ne disposent pas encore d'un protocole de revue de divulgation.
   Avant diffusion, vérifier au minimum: identifiants directs ou pseudonymes stables,
   texte libre, dates fines, petites cellules, liens de jointure et identifiants techniques.

## 4. Paquet minimal recommandé : Twin sous licence claire

Objectif : refaire les diagnostics de correspondance et de fidélité qui utilisent Twin,
sans données R6, GSS, Stanford, SCE, Ahler-Sood, modèles locaux ni API.

Contenu du paquet :

- code minimal et tests pour le chargeur Twin, les baselines, la permutation conditionnelle,
  le nul indépendant, les tables et figures;
- `pyproject.toml` et lockfile, versions Python et dépendances explicites;
- un script `download_twin.py` qui récupère la révision exacte de
  `LLM-Digital-Twin/Twin-2K-500`, contrôle les hashes et affiche la notice CC BY 4.0;
- une configuration qui utilise seulement le catalogue de questions, les réponses numériques
  normalisées et les sorties LLM déjà publiées nécessaires, jamais les personas texte, les
  fichiers Qualtrics bruts ou les identifiants dans les sorties;
- un jeu fixture entièrement synthétique, versionné, qui fait passer tous les tests sans
  téléchargement;
- des sorties finales agrégées, une commande unique et un manifeste de hashes.

Ce paquet est juridiquement plus simple, scientifiquement lisible et suffit à reproduire
la distinction entre structure de groupe et correspondance conditionnelle. Il doit citer
Twin et conserver CC BY 4.0, sans prétendre redistribuer ou anonymiser davantage les données
source.

## 5. Paquet complet pour un chercheur disposant de ses propres données

Publier un cadre, pas les entrées : schéma de données documenté, adaptateurs séparés
`twin`, `gss`, `stanford`, `sce`, `ahler_sood`, tests synthétiques et une commande qui exige
un répertoire d'entrée fourni par l'utilisateur. Chaque adaptateur doit vérifier les colonnes,
versions, hashes, masque d'items, unités d'analyse et licence déclarée avant calcul.

Le chercheur apporte ses microdonnées sous ses propres droits. Le paquet retourne seulement
tables agrégées, figures, manifestes de provenance et journaux expurgés. Les runs de modèles
doivent être optionnels, isolés du paquet analytique et refuser une clé absente; les poids
sont récupérés de leurs sources avec leurs licences propres. Cette séparation rend le code
réexécutable sans transformer le dépôt en canal de redistribution de données ou de secrets.

## Sources locales auditées

`LICENSE`, `.gitignore`, `README.md`, `analyses/README.md`, `data/PROVENANCE.md`, les
provenances GSS, SCE, ANES et Ahler-Sood, `data/twin2k500/README.md`, les scripts concernés
et les preuves locales de préenregistrement. Aucune licence, aucun statut OSF et aucun droit
extérieur n'a été vérifié sur le réseau durant cet audit.
