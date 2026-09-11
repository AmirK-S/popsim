# Mémoire : prédictions écrites avant calcul

Écrit le 11 septembre 2026, avant tout calcul. Question : un jumeau LLM fait-il mieux que
« elle répondra comme la dernière fois » (persistance = réponse vagues 1-3 retest) sur les
108 items catégoriels répétés de Twin-2K-500, vague 4 ? Et voit-il venir un changement
d'avis ? Fait déclaré : le persona des vagues 1-3 ne contient aucune des 75 QID répétées
(`resultats/twin-ab-audit-provenance-2026-09-11.md` §2.2) — le jumeau n'a pas l'information
que la persistance utilise. C'est la question, pas un artefact à corriger.

Périmètre : les 8 configurations « admissibles sous réserve » de l'audit (exclut PredOut,
Finetuning 500, Persona Summary). Chaque configuration sur son propre périmètre de
personnes (règle `t1` : jamais de valeur absolue comparée entre périmètres). Cellule
retenue : item répété × personne où l'humain vague 4 répond ET où persistance (vagues 1-3)
est renseignée. « Changée » : code vagues 1-3 ≠ code vague 4 sur cette cellule ; « inchangée »
sinon. Exactitude = moyenne des cellules où prédiction et vérité sont toutes deux non vides.
AUC (P3) : score binaire = 1 si jumeau ≠ passé (désaccord), 0 sinon ; cible = cellule
changée ; AUC calculée par paire concordante sur cellules changées vs inchangées. Règle
combinée (P4), fixée ici : garder la persistance partout, sauf quand le jumeau diffère de
la persistance ET qu'au moins 5 des 8 jumeaux admissibles s'accordent sur cette même
réponse alternative (accord inter-jumeaux comme proxy de confiance, aucune probabilité
n'étant fournie par les fichiers de sortie) — alors prendre cette réponse commune.
IC : bootstrap personnes × items, 1000 réplicats, tirage avec remise indépendant sur l'axe
personne et sur l'axe item, graine fixe 20260909.

Prédictions :
- **P1.** Exactitude globale vague 4 : persistance > meilleur jumeau, d'au moins 10 points.
- **P2.** Sur les cellules changées (persistance = 0 par construction), le meilleur jumeau
  ne fait pas mieux que B0 mode, à moins de 2 points près.
- **P3.** AUC(désaccord jumeau/passé → changement) < 0,60.
- **P4.** La règle combinée n'améliore pas l'exactitude de la persistance de plus d'un point.
