# Vérification des licences et sources externes

Date de consultation : 2026-09-11. Recherche documentaire web en lecture seule, en
complément de l'audit `audit-reproductibilite-publication-2026-09-11.md` (bloquant n° 3).
**Ceci n'est pas un avis juridique.**

## 1. OSF t6g7k (Stanford)

**Établi (source primaire).** L'API OSF (`https://api.osf.io/v2/nodes/t6g7k/`, consultée le
2026-09-11) renvoie `node_license: null` — **aucune licence n'est déclarée** sur le nœud OSF.
Titre exact du projet : « LLM Agents Grounded in Self-Reports Enable General-Purpose
Simulation of Individuals », créé le 21 avril 2026, catégorie « Project ». Ce titre correspond
à celui de l'article arXiv 2411.10109 (consulté le 2026-09-11), auteurs Joon Sung Park,
Carolyn Q. Zou, Jonne Kamphorst, Niles Egan, Aaron Shaw, Benjamin Mako Hill, Carrie Cai,
Meredith Ringel Morris, Percy Liang, Robb Willer, Michael S. Bernstein (v1 15 nov. 2024,
renommé depuis « Generative Agent Simulations of 1,000 People »). Aucune mention de licence
ni de « data availability statement » n'a été trouvée dans les métadonnées de l'article.

**Interprétation.** L'absence de licence déclarée sur OSF ne vaut pas domaine public : par
défaut, une œuvre sans licence explicite reste sous droits réservés de ses auteurs/ayants
droit. Le fait que l'archive soit publiquement accessible n'emporte pas droit de
redistribution des données individuelles qu'elle contient.

**Verdict : renvoi.** Ne pas republier l'archive ni ses fichiers de réponses individuelles.
Citer l'article et l'OSF, et renvoyer le lecteur vers `https://osf.io/t6g7k/` pour obtention
directe.

## 2. Contenu individuel et redistribution GSS

**Établi (lecture locale).** Les README locaux de `data/osf-t6g7k-stanford/figure2/` et
`figure3/` déclarent explicitement des données « de-identified » avec des identifiants
`participant_0001` à `participant_1052` — donc des **réponses individuelles pseudonymisées**,
pas des agrégats, pour le GSS, les jeux économiques (Camerer) et le Big Five.

**Établi (source primaire, doublement confirmé : fetch direct + citation déjà présente dans
`data/gss-panel/PROVENANCE.md`).** Les conditions générales NORC
(`https://gss.norc.org/us/en/gss/terms-and-conditions.html`, consulté 2026-09-11) :
> « No part of the contents of NORC websites may be reproduced, stored, or transmitted in any
> form or by any means […] without the express written consent of NORC. »

Aucune page NORC trouvée ne traite explicitement des tableaux agrégés dérivés (page
« data-use-statement » introuvable, 404). Rien n'établit qu'un agrégat calculé par un tiers à
partir du GSS soit couvert par la même interdiction que la republication de microdonnées ;
rien n'établit non plus le contraire.

**Interprétation.** La pseudonymisation par identifiant stable n'est pas une anonymisation :
le couplage avec les fichiers GSS publics (variables démographiques rares, dates, réponses
combinées) peut permettre une ré-identification. Republier ces fichiers individuels, même
« de-identified », combine deux problèmes distincts et cumulables : la licence OSF absente et
l'interdiction NORC de reproduction sans consentement écrit.

**Verdict : exclure.** Ne jamais publier `data/osf-t6g7k-stanford/**/data/` (réponses
individuelles GSS ou dérivées). Publiable : le code (`run_pipeline.py`, scripts R), à
condition qu'il lise des données fournies par le chercheur et ne les embarque pas.

## 3. Ce qui est publiable pour un dépôt de code et d'agrégats

- **Publiable** : code d'analyse, scripts de récupération, manifestes de hachage, figures et
  tableaux agrégés produits localement à condition d'une revue de divulgation (pas de petites
  cellules, pas d'identifiant individuel, pas de texte libre).
- **À exclure** : tout fichier contenant une ligne par personne provenant de l'archive OSF ou
  du GSS (réponses brutes, `pid`/`participant_*`, personas texte, exports Qualtrics bruts).
- **Mentions obligatoires** : citation NORC (« Smith, Tom W., Davern, Michael, Freese, Jeremy,
  and Morgan, Stephen L., General Social Surveys, panel files. Chicago: NORC. », déjà consignée
  localement) ; citation de l'article Park et al. et de l'URL OSF pour tout usage du paquet
  Stanford ; mention que la licence OSF n'est pas déclarée et que l'obtention relève du
  chercheur sous ses propres conditions.

## 4. Twin-2K-500 et SCE — vérification rapide

**Twin-2K-500 : établi (source primaire).** La fiche officielle Hugging Face
(`https://huggingface.co/datasets/LLM-Digital-Twin/Twin-2K-500`, consultée 2026-09-11) déclare
`license: cc-by-4.0` dans ses métadonnées, en cohérence exacte avec `data/twin2k500/README.md`
local. **Verdict : publier** (code, script de téléchargement, agrégats), avec attribution CC
BY 4.0 et lien vers le dépôt HF — pas de copie locale des personas ou réponses individuelles
dans le dépôt public.

**SCE/FRBNY : établi (source secondaire concordante avec la provenance locale).** La
recherche web confirme la mention de source imposée par la Federal Reserve Bank of New York
(« Source: Survey of Consumer Expectations, © 2013-FRBNY […] may be used subject to license
terms posted there ») et une licence non exclusive couvrant la redistribution et les œuvres
dérivées, conforme à `data/sce-fed-ny/PROVENANCE.md`. Le texte intégral de la licence
(`https://www.newyorkfed.org/privacy/termsofuse`) n'a pas pu être récupéré verbatim par cet
agent (page non restituée par l'outil de lecture web) ; la citation vient d'un résultat de
recherche, pas d'une lecture directe de la page. **Verdict : publier par renvoi** — script
d'acquisition et attribution FRBNY, pas de copie des 194 Mo de microdonnées.

## Non établi

- Le texte intégral et la version exacte de la licence FRBNY (`termsofuse`) n'a pas été lu
  directement par cet agent, seulement via un extrait de recherche.
- Aucune page NORC officielle traitant spécifiquement des **agrégats dérivés** (par
  opposition aux microdonnées brutes) n'a été localisée ; le statut d'un tableau agrégé au
  regard des conditions NORC reste une zone grise non tranchée par une source primaire.
- La liste des contributeurs/auteurs OSF n'a pas pu être extraite de l'API (endpoint séparé
  non interrogé) ; l'identification des auteurs repose sur la correspondance de titre avec
  l'article arXiv, pas sur les métadonnées OSF elles-mêmes.
- Aucune vérification n'a été faite sur d'éventuelles conditions OSF générales par défaut
  (politique de la plateforme OSF elle-même en l'absence de licence choisie par l'utilisateur).

**Rappel : ceci n'est pas un avis juridique.** Il restitue des sources primaires et secondaires
consultées le 2026-09-11 et leur interprétation raisonnable pour guider une décision de
publication ; une revue par un juriste reste recommandée avant toute diffusion publique
impliquant des données de recherche sur des personnes.
