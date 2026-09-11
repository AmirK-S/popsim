# Mémoire à long terme : préenregistrement (2 et 4 ans, panel GSS)

Écrit le 2026-09-11, avant tout appel de modèle. Suite à `resultats/memoire-resultats.md`
(persistance bat le jumeau IA de 14 points à **deux semaines** sur Twin-2K-500) : est-ce
que ça tient à des horizons où les gens changent réellement, 2 et 4 ans, sur le panel GSS
(`data/gss-panel/`, panels 2006-2010, 2008-2012, 2010-2014, trois vagues à ~2 ans d'écart) ?

## Conception
- ~400 personnes, échantillonnées à parts égales sur les trois panels à trois vagues
  (2006-2010, 2008-2012, 2010-2014 ; le panel 2016-2020 est exclu, ses deux cohortes ne
  partagent pas trois vagues par personne), parmi celles répondant aux trois vagues sur
  au moins 60 des ~129 items de contexte et au moins 10 des 20 items cibles.
- Profil par personne : 11 attributs démographiques de la vague 1 (âge, sexe, race,
  diplôme, région, revenu, parti, idéologie, statut marital, religion, statut d'emploi)
  + réponses de la vague 1 aux items AUTRES que les 20 cibles (~129 items).
- 20 items cibles, choisis sur métadonnées SEULES (famille thématique de `FAMILLES` dans
  `a2_baselines_gss.py`, ordre alphabétique, présence des colonnes Stata aux trois vagues
  dans les trois panels), avant tout calcul de changement : jusqu'à 4 items par famille
  (6 familles), complété alphabétiquement hors famille jusqu'à 20.
- Cibles : réponse à la vague 2 (+2 ans) et à la vague 3 (+4 ans) du même item, un seul
  appel modèle par (personne, item, horizon) — le profil (vague 1 seule) ne change pas
  entre les deux horizons, seul l'énoncé de l'horizon dans le bloc utilisateur change.

## Comparateurs
- **Persistance** : la réponse de la vague 1 au même item, recopiée aux deux horizons.
- **Mode du segment** : modalité la plus fréquente à la vague 1 parmi les ~400 personnes
  de l'échantillon, pour cet item (équivalent du « B0 mode » de memoire-resultats.md).
- **Règle combinée**, fixée d'avance : IA si (IA ≠ persistance) ET (IA == mode du
  segment), sinon persistance. N'utilise que des quantités calculées avant la vérité.

## Mesures, par horizon (+2, +4 ans)
Exactitude globale des quatre comparateurs ; exactitude restreinte aux cellules où la
vraie réponse a changé entre la vague 1 et la vague cible ; AUC(désaccord IA / vague 1 →
changement réel). IC à 95 % par bootstrap sur les personnes, 1000 réplicats, graine
20260911.

## Prédictions chiffrées
1. La persistance reste devant l'IA aux deux horizons, avec un écart qui diminue de
   +2 à +4 ans (le passé pèse moins loin dans le temps).
2. Sur les cellules changées, l'IA ne bat pas le mode du segment (comme à 2 semaines).
3. AUC(désaccord → changement) < 0,62 aux deux horizons, sans progression avec l'horizon.

## Autres éléments
Modèle : gpt-oss-20b (défaut), Qwen3-30B-A3B-Instruct-2507 en repli si disponibilité
machine meilleure au moment du lancement différé — un seul modèle par run complet, choix
écrit dans le résumé JSON. Graine d'échantillon 20260911, graine de bootstrap 20260911.
Client et parse : `analyses/r1_oracle_camps.py` (MoteurR1, gabarit, ARRETS), adaptés à
une réponse d'une seule lettre (pas une distribution). Scripts : `analyses/memoire_long_gss.py`
(collecte, reprise sur index, fichier STOP) et `analyses/memoire_long_analyse.py`.
