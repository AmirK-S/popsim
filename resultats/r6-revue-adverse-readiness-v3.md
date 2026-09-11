# R6 — revue adverse indépendante de la readiness PREPARE-3

## Verdict

**NO-GO pour transformer PREPARE-3 en manifeste exécutable dans son état actuel.** Le
manifeste est correctement inerte (`state = PREPARE_BLOCKED`, `executable = false`), le GO
de campagne est absent, `STOP-R6` est présent et le GO du pilote DeepSeek est archivé comme
consommé. Aucun risque immédiat de POST ne subsiste. Avant tout nouveau pilote ou toute
campagne, il faut toutefois corriger les deux incohérences ci-dessous, regeler code, tests et
manifeste, puis déposer un nouvel addendum OSF prospectif. Les changements sont
opérationnels et portent sur la sélection des fournisseurs et les règles d'arrêt financier;
ils sont donc matériels pour la collecte même s'ils ne changent aucune hypothèse.

Audit effectué hors ligne le 10 septembre 2026. Aucun appel distant, GET authentifié, POST
de génération ou calcul de résultat scientifique n'a été exécuté.

## Contrôles rejoués

- `analyses/test_r6_client.py` : **231 contrôles OK**, code 0;
- `analyses/test_r6_evaluer.py` : **16 tests OK**, code 0;
- `analyses/test_r6_runner_pilotes.py` : **OK**, couvrant les sept lignes compatibles, les
  quatre incompatibles, STOP, reprise, fournisseur imposé, GO one-shot et registre;
- les 20 fichiers nommés dans PREPARE-3 ont tous leur SHA-256 courant, sans divergence;
- SHA-256 courant de PREPARE-3 :
  `60a49b3de1603820c078335b7fa0cb9cf5e6be1e49aef5cfe2bd2e47bce43edc`;
- registre réel : 20 opérations pilote DeepSeek, toutes réconciliées, coût
  `0.0003289566 USD`; aucune opération campagne/plancher; total global identique;
- `data/traces/GO-R6` absent, `data/traces/STOP-R6` présent et archive du GO `k5qfh`
  présente.

## Changements matériels postérieurs au gel `k5qfh`

Le client gelé sous `k5qfh` était spécialisé pour le pilote DeepSeek/DigitalOcean. Le code
courant ajoute quatre mécanismes qui n'appartiennent pas à ce gel :

1. une politique pilote lue dans un manifeste hashé, avec réglages et prix exigés à
   l'identique plutôt que comme seules bornes supérieures;
2. un runner générique pour sept nouveaux couples modèle-fournisseur, avec deux passes des
   dix mêmes cellules, reprise exacte et comptabilité pilote séparée par modèle;
3. un plafond cumulatif par modèle, sous le verrou du registre global, pour les passes F1,
   F2 et plancher, fourni par `--plafond-modele`;
4. un GO JSON one-shot propre au modèle et au hash du manifeste, conservé pendant une
   reprise puis renommé seulement après les vingt cellules complètes.

Les fournisseurs choisis, leurs plafonds tarifaires, les quatre incompatibilités de charge
et les plafonds pilotes proviennent de métadonnées publiques observées avant les réponses
scientifiques. Il n'y a pas de sélection sur un résultat de modèle. Cette antériorité doit
néanmoins être rendue publique avant les appels, car le fournisseur fait partie de
l'estimand enregistré et les nouvelles bornes peuvent interrompre une collecte.

## Corrections bloquantes

### 1. Le plafond « modèle » ne compte pas le pilote

`RegistreGlobal.total_modele()` additionne seulement `campagne` et `plancher`, tandis que
PREPARE-3 appelle `prepared_model_spend_cap_usd` la borne du modèle et, pour DeepSeek,
présente explicitement la somme F1 + F2 + plancher + pilote réglé. Le plan calcule aussi la
projection sur les 1 270 appels, pilote compris. Dans l'état courant, la garde autoriserait
jusqu'à la borne entière pour campagne/plancher **en plus** du coût pilote. Les plafonds par
trace préparés pour DeepSeek maintiennent fortuitement la somme sous 0,06 USD, mais la garde
générique ne garantit pas cette propriété.

Correction requise : faire entrer `essai-1` et `essai-2` dans le total cumulatif du modèle,
réservations et coûts réglés compris, puis tester qu'un pilote consommé réduit exactement le
solde disponible pour F1/F2/plancher. Le plafond historique pilote de 0,02/0,04 USD reste une
seconde garde, plus étroite, propre aux vingt appels.

### 2. La vérification DeepSeek annoncée n'existe pas dans le manifeste réel

PREPARE-3 dit `execution_status = "consumed; runner permits verification only"`. Or la ligne
DeepSeek porte `pilot_plan.required = false`; `politique_modele()` la refuse avant que le
mode `--verifier` puisse lire les 20 opérations consommées. Le test passe parce que sa
fixture DeepSeek utilise au contraire `required = true`. La non-réexécution est bien sûre :
le runner réel refuse DeepSeek et le registre prouve 20/20. L'affirmation de vérification est
cependant fausse.

Correction minimale : remplacer cette valeur par
`"consumed; runner refuses every new execution; consumption verified from the global ledger"`.
Alternative de code acceptable : autoriser le diagnostic `--verifier` avant d'exiger
`pilot_plan.required`, tout en conservant le refus absolu en exécution.

## Points conformes et limites résiduelles

Le fournisseur est effectivement imposé par `provider.order` avec
`allow_fallbacks = false`; prix, `max_tokens`, raisonnement, liste et hash des cellules sont
scellés par le manifeste. Le verrou global rend atomiques préflight, réservation et
reconciliation. Le verrou de trace interdit deux runners sur la même passe; le verrou du GO
interdit deux utilisateurs du même fichier GO. Une interruption conserve le GO et la trace,
et la reprise saute les identités déjà réglées. Un 21e appel pilote ou un second achat d'une
identité est refusé sous verrou.

Le champ `pilot_runner_guard.allowed_models` est déclaratif : le runner ne vérifie pas
explicitement l'appartenance à cette liste et se fie aux lignes compatibles du panel. Le
hash du manifeste et le GO correspondant empêchent une modification silencieuse, donc ce
n'est pas un risque dans PREPARE-3 courant. Pour que le contrat soit exact, ajouter le refus
`modele not in allowed_models` et une fixture contradictoire. Les quatre lignes sans
fournisseur compatible sont actuellement refusées avant clé et avant POST.

## Texte exact proposé pour le nouvel addendum OSF

> **Addendum prospectif R6 — exécution multi-modèles et plafonds cumulatifs.** Après le
> pilote DeepSeek enregistré sous `k5qfh`, et avant tout nouvel appel de modèle, le runner
> des pilotes payants est généralisé aux couples suivants, choisis uniquement à partir de
> métadonnées publiques de disponibilité, de paramètres et de prix, sans consultation de
> réponse scientifique : Mistral Small 2603/Mistral (0,15/0,60 USD/M), Qwen 3.7
> Plus/Alibaba (0,32/1,28), Kimi K2.5/SiliconFlow (0,45/2,25), GLM-5/StreamLake
> (0,60/1,92), Gemini 3.8 Flash/Google AI Studio (0,375/1,875), Claude Haiku
> 4.5/Anthropic (1/5) et Grok 4.3/xAI (1,25/2,50). Le fournisseur est imposé sans repli.
>
> Chaque nouveau payant conserve les deux passes ordonnées des dix mêmes cellules, la
> température 0, `max_tokens=150`, le raisonnement désactivé, l'invite et les critères
> d'arrêt déjà enregistrés. Les cinq premiers couples ont une réservation maximale de
> 0,001 USD par appel et 0,02 USD pour vingt appels; Haiku et Grok ont respectivement
> 0,002 USD et 0,04 USD. Les plafonds cumulatifs par modèle, pilote compris, sont : 0,12
> USD pour Mistral, 0,24 pour Qwen, 0,345 pour Kimi, 0,42 pour GLM-5, 0,585 pour Gemini,
> 0,78 pour Haiku et 0,825 pour Grok. Pour DeepSeek, le pilote `k5qfh` est consommé et ne
> sera pas rejoué; son coût réglé de 0,0003289566 USD entre dans sa borne modèle de 0,06
> USD avec F1, F2 et le plancher.
>
> Chaque autorisation est prise sous le verrou du registre global. Elle exige le hash du
> manifeste READY et un GO one-shot propre au modèle; le GO est conservé pendant une
> reprise exacte et consommé après vingt cellules complètes. Les coûts réglés et les
> réservations des pilotes, F1, F2 et du plancher réduisent atomiquement la borne du modèle.
> Le plafond global de 4,40 USD, la réserve de compte de 1,50 USD et les gardes de clé
> restent inchangés.
>
> Llama 4 Maverick, GPT-5.6 Luna, GPT-5.4 et Claude Sonnet 5 restent non exécutables tant
> qu'aucun fournisseur unique ne supporte la charge enregistrée sans modification. Ce
> constat de compatibilité n'est ni un retrait scientifique ni un résultat. Aucun modèle
> incompatible ne sera adapté ou remplacé sans nouvel addendum prospectif. Les hypothèses,
> familles, statistiques, prompts, cellules et critères scientifiques de R6 ne changent
> pas.

Après les deux corrections bloquantes, ce texte doit être déposé avec les hashes du client,
du runner, des tests, du manifeste READY final et de la liste des dix cellules. Un GO créé
avant ce nouveau dépôt ne doit pas être accepté.
