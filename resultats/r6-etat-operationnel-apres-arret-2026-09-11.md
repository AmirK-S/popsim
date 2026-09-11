# R6, état opérationnel après arrêt

Audit local du 11 septembre 2026. Lecture seule des traces, journaux et ledger. Aucun accès réseau, appel OpenRouter ou relance n’a été effectué.

## Constats vérifiables

- La trace principale `data/traces/r6-deepseek-deepseek-v4-flash-q4-r6v2-campagne-f1.jsonl` contient **220 lignes valides**. Les 220 ont une fin normale `stop`, sans erreur de parsing ni erreur HTTP enregistrée.
- La trace `...campagne-f1-non-jouees.jsonl` contient **3 enregistrements HTTP 429**. Ils correspondent à **2 cellules distinctes**, l’une ayant été rencontrée deux fois. Ces enregistrements ne portent ni identifiant de génération ni coût annoncé.
- Le ledger `data/traces/reprise/r6-v2-registre-global.jsonl` contient, pour ces cellules interrompues, des réservations, rapprochements et annulations. Il ne transforme pas les 429 en réponses valides et ne justifie aucun rejeu automatique.
- Le fichier `.en-cours` de la campagne existe encore. Le journal de queue indique `state=STOPPED`, avec un dernier `MODEL_STOP` en code de sortie 1 après l’exception « campagne interrompue, GO conservé pour reprise exacte ».
- Aucun processus R6, runner, client distant ou serveur associé n’est présent dans l’inventaire local `ps` au moment de l’audit.

## Verdict terminal

Le **processus OS est terminé**, mais le **run n’est pas terminal** au sens opérationnel. La trace principale est complète pour 220 cellules, mais les 3 incidents 429 restent non joués et le marqueur `.en-cours` ainsi que le GO conservé signalent une reprise exacte possible. Il serait incorrect de présenter la campagne comme complète ou comme un échec total.

## Marche sûre minimale

1. Geler les fichiers de trace, le marker `.en-cours`, le GO et le ledger. Ne rien supprimer, renommer ou rejouer.
2. Archiver le statut `STOPPED` et conserver l’exception de sortie comme preuve d’arrêt, sans modifier le ledger.
3. Faire valider par Euler, hors réseau, la correspondance entre les 3 incidents 429, les 2 cellules distinctes et les événements du ledger.
4. Décider ensuite explicitement entre abandon documenté et reprise exacte des cellules non jouées. Une reprise éventuelle doit vérifier le GO, le budget et l’identité de cellule avant un unique POST par cellule ; elle ne doit jamais rejouer les 220 cellules valides.

La décision reste bloquée jusqu’à cette réconciliation et à un nouveau GO explicite. Aucun appel supplémentaire n’est autorisé par cet audit.

