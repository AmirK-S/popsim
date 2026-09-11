# Préparation hors ligne de l’analyse fine R6

Le chargeur `analyses/r6_analyse_fine.py` est prêt, sans appel réseau, GPU ni lecture de
trace de campagne active pendant sa préparation. Il refuse l’analyse avant toute ouverture
de trace si le manifeste, les empreintes, A37, le référent, le plancher ou le ledger ne sont
pas cohérents. Chaque empreinte de requête et fournisseur imposé d’une trace doivent aussi
correspondre à leur réservation du ledger. Pour chaque couple modèle–fournisseur, le ledger doit reconstruire exactement
1 250 opérations réglées dans l’ordre F1 (894), F2 (316) puis plancher (40). Les deux passes
pilote sont exclues des sources admises, des effectifs, des tableaux et de toute stabilité de
campagne.

Le module émet seulement des tableaux secondaires et exploratoires. Il garde H1--H3 hors de
son périmètre, et n’écrit ni p, Holm, IC ni verdict. F2 est contrôlé contre son plan de
316 cellules gauche/droite : un centre y est bloquant. Les regroupements sous cinq items et
les codifications absentes donnent `NON_INTERPRETABLE`. Les diagnostics de stabilité portent
le marqueur non déterministe, notamment DeepSeek et Grok, sans promotion de leurs pilotes.

Validation locale : `.venv/bin/python analyses/test_r6_analyse_fine.py` a exécuté huit tests
synthétiques temporaires avec succès. Ils couvrent la garde terminale avant lecture de trace,
l’ordre complet, F2 sans centre, les pilotes interdits, leave-one-item, leave-one-family,
les strates non interprétables, la convergence constante, les marqueurs DeepSeek/Grok et la
liaison de provenance trace--ledger.
Ce résultat ne constitue aucune analyse de données R6 ni résultat scientifique.
