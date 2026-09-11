# Préenregistrement : loi d'échelle plate (petit contre grand modèle, Twin-2K-500)
Écrit le 11 septembre 2026, avant `analyses/echelle_twin.py` et tout calcul. Idée 6,
`idees-C-folles-2026-09-11.md` ; admissibilité selon `twin-ab-audit-provenance-2026-09-11.md`.
**Paire même invite / taille** : une seule, admissible et non suspecte : `JSON Persona -
GPT4.1` contre `JSON Persona - GPT4.1-mini`. Périmètre commun imposé : intersection des
couvertures = 1 000 personnes (pid 1-1000). Plancher humain recalculé sur ce périmètre,
jamais sur 2 058. `Text Persona - Gemini-Flash2.5` : troisième point, autre famille (pas
de jumeau GPT4.1 non-mini sur cette invite), rapporté à part, jamais en paire de taille.
**Mesures**, périmètre commun, segmentation `S_gra` (principale, déclarée par `t1`) :
1. Exactitude moyenne par personne (`t1_commun.exactitude_codes`).
2. Correspondance individuelle : chute sous permutation intra-segment de
   `t1_mesures.chute`, rapportée au plancher humain recalculé sur les 1 000.
3. Corrélation ordinale intra-segment : par item Matrix et cellule `S_gra` (≥ 5 des deux
   côtés), Spearman prédit/humain v4 à travers les personnes, moyenne pondérée par paires.
**Prédiction** : grand modèle gagne en exactitude (≥ +2 points) ; correspondance
normalisée et corrélation ordinale n'augmentent pas de plus de 10 % relatifs (« plat »).
**Bootstrap** : remise, graine 20260909, 1 000 répliques, percentiles 2,5/97,5. Personnes
seules pour exactitude/chute (fonctions `t1_commun`) ; personnes ET items ordinaux tirés
indépendamment pour la corrélation.
**Limite** : deux tailles, une famille (gpt-4.1) ; Gemini hors comparaison de taille ;
périmètre commun à cellules `S_gra` petites (médiane ~13).
