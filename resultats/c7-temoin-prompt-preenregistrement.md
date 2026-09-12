# C7-temoin-prompt, preenregistrement : decomposer l'accord inter-jumeaux en plancher de prompt, part de segment, part individuelle

**Ecrit le 12 septembre 2026, avant tout calcul.** Objection hostile a A2 (canal inter-jumeaux,
`resultats/c7-transfert-resultats.md` : 36,4 % de top-1 moyen sur 30 paires a 60 items communs
parmi 7 configurations riches, meilleure paire 83,58 %) : « deux tirages du meme gabarit de
prompt se ressemblent, vous mesurez la stabilite du prompt, pas la personne ». Ce chantier
decompose l'accord entre deux jumeaux en trois parts : ce qui vient du prompt/format (plancher),
ce qui vient du segment demographique-ideologique (population), ce qui reste (individuel).

## Ce qui est repris tel quel, sans une ligne recopiee
- `analyses/t1_commun.charger` : les quinze tables de Twin, les segmentations (`S_ideo`,
  `S_fin`, `S_gra`, `S_parti`), 2 058 personnes, 108 items de vague 4.
- `analyses/a2_commun.distance_hamming` : la distance de Hamming normalisee (items masques).
- `analyses/a2_commun.bootstrap_personnes` : IC 95 % par reechantillonnage des personnes.
- `analyses/c7_reidentification.rangs_attaque`, `graine_nom`, `resume_taux` : le rang du vrai
  repondant contre un bassin, ex aequo departages par tirage aleatoire, et le resume bootstrap.
- `analyses/c7_transfert.items_pair`, `CONFIGURATIONS` : la liste des colonnes pleines a 100 %
  des deux cotes d'une paire de configurations, et les 8 configurations admissibles.
- `resultats/c7-transfert-voletA.csv` : la matrice deja calculee des 56 paires (top-1, top-10,
  n_items) — relue pour identifier les 30 paires riches a 60 items et pour comparer le top-1
  individuel deja publie (36,4 %) au top-1 « mode de segment » calcule ici. **Non recalculee.**

## Ce qui est nouveau ici
1. La decomposition exacte, personne par personne et paire par paire, de l'accord (fraction
   d'items ou les deux jumeaux repondent pareil) en trois termes qui s'additionnent :
   `plancher_i + apport_segment_i + apport_individuel_i = accord_vrai_i`, ou :
   - `plancher_i` = accord moyen entre le jumeau X de la personne i et le jumeau Y de TOUTE
     autre personne du bassin (2 057 autres), sans condition de segment — l'« accord de fond ».
   - `accord_meme_segment_i` = accord moyen entre le jumeau X de i et le jumeau Y des AUTRES
     personnes du meme segment `S_fin` — equivalent analytique exact (esperance, sans bruit de
     Monte-Carlo) d'une permutation intra-segment des identites de jumeau Y.
   - `apport_segment_i = accord_meme_segment_i - plancher_i`.
   - `apport_individuel_i = accord_vrai_i - accord_meme_segment_i` (accord_vrai_i = accord au
     vrai jumeau apparie).
2. Un temoin de population pure : pour chaque paire, un profil de jumeau Y remplace par le
   **mode de son segment `S_fin`, en laissant la personne elle-meme de cote** (mode
   leave-one-out, calcule item par item, ex aequo tranches par le code le plus petit). L'attaque
   d'identification (`rangs_attaque`, reprise sans modification) est relancee du jumeau X contre
   ce bassin de profils-modes : c'est le top-1 atteignable **sans aucune information
   individuelle**.

## Segmentation retenue et pourquoi
La demande porte sur « meme age, meme sexe, meme bord politique ». `t1_commun.segmentations`
offre quatre segmentations : `S_gra` (genre x ethnicite x age, SANS ideologie, tailles de 1 a
259, mediane 23,5 — trop fine, des segments de taille 1 rendent le mode leave-one-out
indefini) ; `S_parti` (parti seul, 4 groupes, mediane 574 — trop grossier, aucune granularite
d'age/sexe) ; `S_fin` (bloc d'ideologie x genre x age, 24 segments, tailles 25 a 192, mediane 82,
couverture 2 058/2 058) — c'est la segmentation qui correspond le mieux a « age x sexe x bord
politique » et qui a des segments assez grands pour un mode leave-one-out stable. **`S_fin` est
retenue.**

## Paires retenues et pourquoi
Les 30 paires dirigees a 60 items communs parmi les 7 configurations riches (hors
`Demographics Only`), deja identifiees dans `c7-transfert-voletA.csv`. Les 12 paires a 19 items
(toutes impliquant `JSON Persona - GPT4.1-mini`) sont ecartees : deja pres du plancher
(0,45 % de top-1) dans `c7-transfert-resultats.md`, et 19 items sont trop peu pour batir un mode
de segment lisible. Les 2 058 personnes sont couvertes des deux cotes pour les 30 paires (pas de
sous-echantillon).

## Predictions chiffrees
- **Plancher (accord de fond)** : entre 45 et 60 % — les items sont categoriels a faible nombre
  de modalites (echelles Likert), un accord de fond eleve est attendu meme entre inconnus.
- **Apport de segment** : petit, 1 a 5 points de pourcentage au-dessus du plancher — `S_fin`
  correle avec une partie des items d'opinion/politique mais pas avec la majorite des 60 items.
- **Apport individuel** : le reste, doit rester nettement positif et representer la MAJORITE de
  l'ecart entre le plancher et l'accord vrai — sinon A2 ne transporte pas d'information au-dela
  du gabarit et du segment.
- **Temoin population (top-1 mode de segment)** : proche du hasard conditionnel a la taille de
  segment, soit environ 1/82 ≈ 1,2 % (mediane des tailles `S_fin`), tres en dessous des 36,4 %
  de top-1 individuel deja publies.

## Regle de decision explicite — ce qui detruirait A2
A2 est jugee **refutee** (le canal inter-jumeaux ne transporterait aucune information
individuelle au-dela de la demographie/ideologie de segment) SI, sur la moyenne des 30 paires :
- le top-1 « mode de segment » atteint **au moins le tiers** du top-1 individuel reel deja publie
  (36,4 % / 3 ≈ 12,1 %), **OU**
- `apport_individuel` (points 4) est **inferieur ou egal** a `apport_segment` — c'est-a-dire que
  la part attribuable au segment egale ou depasse la part attribuable a la personne.

Si aucune de ces deux conditions n'est remplie, A2 survit : le canal transporte une information
individuelle mesurable au-dessus du plancher de prompt ET au-dessus de ce que le segment seul
explique.

## Ce que les donnees ne permettront pas
Aucune donnee de panel externe (GSS, ANES) n'est utilisee ici : la segmentation reste limitee
aux quatre axes deja codes par `t1_commun.segmentations`. Si un axe plus fin (ex. revenu, region)
s'averait necessaire, il faudrait le construire a partir de `demographies_brutes`, ce qui n'est
pas fait ici (perimetre du chantier : temoins a partir des donnees deja disponibles).

## Discipline
Graine fixee `20260912`. Bootstrap 2 000 tirages sur les personnes
(`a2_commun.bootstrap_personnes`, reprise). Deux executions identiques de
`analyses/c7_temoin_prompt.py` requises avant publication des resultats. Aucun appel de modele de
langage, aucun acces reseau, lecture seule sur `data/`. Aucun fichier existant modifie.
