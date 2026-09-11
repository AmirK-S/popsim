# R6 — erratum instrumental : chargeurs d'analyse et cellules rejouées après un 429 non facturé

Date : 2026-09-11. Correction du contrôle d'intégrité des chargeurs. Plan scellé, estimands, colonnes et statistiques inchangés.

**Motif.** Un 429 porteur d'un `generation_id`, prouvé non facturé, donne pour une même identité la suite réservation → annulation → réservation → réconciliation. `r6_analyse_fine.py` refusait toute seconde réservation (« opération ledger dupliquée ») et exigeait un ordre exact. `r6_evaluer.py` exigeait un rang strictement croissant. Lu sur les seules métadonnées du registre de production, l'ancien chargeur rejette déjà DeepSeek à cause de `fucitzn`. Le nouveau s'arrête sur la garde normale : campagne non terminale, 1 250 opérations réglées exigées.

**Périmètre exact.**
- `r6_analyse_fine.py`, `_operations_terminales` : un rejeu est admis seulement si chaque annulation porte une preuve 429. Deux formes sont reconnues : un texte commençant par `429-non-facture` (amendement 429), ou l'un des trois textes manuels exacts du registre, chacun lié à sa seule identité (`fucitzn/gauche/journaliste` deux fois, `colhomo/gauche/adversaire` une fois).
- Autres conditions du rejeu : au plus 2 annulations, même `empreinte_requete` et même `fournisseur_impose` que la réservation précédente, dernière opération réglée. La cellule compte une fois, à la position de sa dernière réservation.
- `r6_analyse_fine.py`, `_ordre_conforme` : l'ordre de plan reste strict pour toute cellule sauf une cellule rejouée. Celle-ci peut apparaître plus tard, jamais avant une cellule non rejouée qui la précède au plan. La règle vaut pour le ledger et pour les traces (`_charger_trace`). Les comptes 894/316/40 restent exacts.
- `r6_evaluer.py`, `charger_traces` : même exception, pour une ligne portant `rapprochement_429.statut == "non_facture"`.
- Restent refusés comme avant : annulation sans preuve 429, texte manuel appliqué à une autre identité, 3 annulations, empreinte ou fournisseur changé, réservation ouverte, doublon, cellule déplacée sans rejeu.

**Affirmation vérifiable : aucune statistique n'est modifiée.**
- Dans `r6_analyse_fine.py`, aucune ligne n'a changé à partir de `_consensus` : fonctions analytiques, `analyser` et `ecrire` sont intactes. Dans `r6_evaluer.py`, seules les lignes d'ordre de `charger_traces` ont changé.
- Rejeu manuel à sa position : `test_rejeux_manuels_fucitzn_colhomo_a_leur_position` vérifie par `assert_frame_equal` que les 8 tables sont identiques à celles d'une campagne sans rejeu.
- Rejeu automatique décalé : `test_rejeu_automatique_decale_en_fin_de_passe` compare la couverture (identique) et la table par item, triée, identique aux arrondis flottants près.
- Aucune sortie de modèle R6 réelle n'a été lue : tous les tests sont synthétiques.
