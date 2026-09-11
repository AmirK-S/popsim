# R7 — revue indépendante bloquante du pilote, 10 septembre 2026

Périmètre : `analyses/r7_checkpoints.py` et ses tests, confrontés au plan R7 et à
l’addendum du 10 septembre. Aucun évaluateur modifié. Aucun serveur, GPU, réseau ou
conversion exécuté ; aucun poids chargé.

## Défauts bloquants trouvés et corrigés

- L’exclusivité ne détectait que `llama-server` : R2b, une conversion ou un second pilote
  pouvaient coexister. Le contrôle couvre maintenant ces processus avant le hash lourd,
  avant chaque serveur et avant chaque cellule ; la disparition du serveur attendu bloque.
- Aucune garde mémoire n’existait. `memory_pressure` doit être lisible et rester à au moins
  15 %, seuil déjà employé par la règle mémoire amendée de R2b ; contrôle avant/après
  chargement puis chaque minute.
- La provenance du final était crue sans recalculer son SHA-256 et sans imposer révision,
  commit ni taille validée. Ces quatre contrôles sont maintenant obligatoires. Les quatre
  GGUF passent aussi le validateur structurel avant tout serveur ; plan, addendum et
  provenance locale des poids sont empreintés dans le registre.
- Le contrôle tokenizer comparait seulement les longueurs. Il publie maintenant le hash des
  séquences d’IDs et leur égalité exacte, en plus du seuil de longueur de 2 %, des IDs
  BOS/EOS et de l’insertion effective des spéciaux.
- Le rejet final supérieur à 25 % n’était pas matérialisé et une panne technique pouvait
  laisser partir la condition suivante. Le registre porte désormais `REJET_FORMAT`, tandis
  qu’une panne technique arrête le pilote dans un état reprenable. La sonde reste strictement
  « au-dessus de 50 % » à 60 cellules et passe ensuite à la condition suivante.

## Vérification

17 tests factices réussis : 3 576 cellules, égalité de toutes les invites avec R4, arrêt
sonde à 60 et frontière 30/31 rejets, reprise sans duplication, absence de relance, STOP,
fin dure, rejet final, exclusivité, panne bloquante, mémoire, provenance et tokenizers.
Contrôle local supplémentaire sur les 894 vraies invites : les six paires de tokenizers ont
des séquences d’IDs identiques et un écart maximal de longueur de 0 %. Base ne déclare pas
de BOS ; SFT/DPO/final déclarent `<|endoftext|>` (ID 100257), mais les quatre tokenizers
ajoutent effectivement zéro jeton spécial dans ce chemin de completion.

## Verdict

**AUTORISÉ CÔTÉ TECHNIQUE DÈS DÉPÔT DU PLAN ET DE L’ADDENDUM**, avec leur identifiant passé
par `--depot-plan`. Les garde-fous intégrés refuseront ensuite le lancement si le final et sa
provenance ne correspondent pas, si R2b ou un concurrent est actif, si la mémoire est sous
le seuil, ou si une trace de reprise est incompatible. La portée reste descriptive selon
l’addendum. Aucune nouvelle autorisation utilisateur n’est requise.
