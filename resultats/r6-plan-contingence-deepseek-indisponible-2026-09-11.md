# R6 — contingence prospective : DeepSeek indisponible après le troisième 429

## Statut et déclencheur

Ce document est un plan de mise en œuvre conditionnel. Il ne lance rien, ne modifie ni la
file active, ni le registre, ni un GO, ni une trace. Il ne s’applique que si le couple
`deepseek/deepseek-v4-flash` / DigitalOcean atteint **trois observations HTTP 429** pendant
la campagne, sans identifiant de génération et sans coût ambigu, et est clos proprement.
Le constat doit être archivé avec l’empreinte de la trace partielle, de son rapport
d’interruption et du journal privé non secret des incidents. Une réservation ambiguë, un
identifiant de génération ou un coût incertain interdit la contingence et impose d’abord le
rapprochement existant.

La garde actuelle s’arrête lorsque le nombre de 429 est strictement supérieur à trois.
La mise en œuvre prospective devra remplacer ce seul comparateur par `>= SEUIL_429`, sans
changer les trois reprises 5/20/60 s, les requêtes, le fournisseur, les cellules ou les
budgets. Le certificat de contingence ne peut être créé qu’après cet arrêt propre.

## File, identités et budget conservés

La file `QUEUE_READY`, son SHA-256 et son ordre à six modèles restent immuables. DeepSeek
reste premier et descriptif ; aucune de ses cellules absentes n’est générée, remplacée,
copiée ni comptée comme réglée. Les identités, traces partielles, registres et GO existants
restent inchangés et conservent leurs empreintes.

Les cinq successeurs gardent l’ordre enregistré : Mistral, Qwen, GLM-5, Claude Haiku puis
Grok. Leurs rôles, fournisseurs, invites, formats F1/F2/plancher, plafonds par appel et par
modèle, plafond global de 4,40 USD et réserve de 1,50 USD ne changent pas. Aucun montant
DeepSeek non dépensé n’est réalloué : le registre continue de compter les dépenses réglées
et toute réservation ambiguë. Les GO déjà présents restent valides pour le SHA de la file
immuable ; ils ne sont ni réécrits ni régénérés.

## Artefact minimal et garde exacte à implémenter ultérieurement

Créer seulement un sidecar, par exemple
`data/traces/reprise/R6-deepseek-indisponible-20260911.json`, signé par son SHA-256 et lié
au SHA exact de `QUEUE_READY`. Il contient : version dédiée, SHA de la file parente, modèle
exact, fournisseur exact, motif `trois_429`, nombre d’observations égal à 3, empreintes de
la trace/rapport/journal d’arrêt, état `INDISPONIBLE`, et l’affirmation que le modèle n’a pas
1 250 opérations réglées. Il ne contient ni clé, ni secret, ni résultat scientifique.

Le runner recevra plus tard les deux arguments obligatoires
`--contingence-deepseek` et `--contingence-deepseek-sha256`. Sans eux, son comportement reste
octet pour octet identique. Avec eux, `verifier_predecesseurs` ne peut ignorer que DeepSeek,
seulement pour un successeur, seulement si le sidecar correspond au SHA de la file, au couple
modèle–fournisseur et aux trois 429, et si le registre ne contient aucune réservation ni coût
ambigu. Tous les autres prédécesseurs doivent encore satisfaire les 1 250 opérations réglées,
894/316/40 et l’ordre cellule par cellule. Le contrôle de GO reste inchangé : il vérifie le
SHA de la file parente, pas celui du sidecar.

## Validation factice requise avant toute application

Ajouter des tests hors réseau pour : refus sans sidecar ; refus de SHA, modèle, fournisseur,
compteur ou état invalide ; refus si coût ambigu ou réservation ouverte ; succès du seul saut
DeepSeek après exactement trois 429 ; refus du saut d’un autre prédécesseur ; conservation du
SHA de file et du GO existant ; conservation des plafonds/rôles/ordre ; et rejet de toute
tentative de produire ou de faire passer 1 250 cellules DeepSeek. Vérifier aussi le nouvel
arrêt au troisième 429 avec serveur factice, sans POST réel.

## Portée analytique après contingence

DeepSeek est rapporté `INDISPONIBLE — collecte incomplète`, exclusivement descriptif, sans
estimation de campagne, stabilité, IC, classement ou contribution aux masques. Les résultats
des cinq successeurs restent limités à leurs couples modèle–fournisseur effectivement
collectés. H1 reste indécidable car il exige les cinq fermés nommés ; H2 et H3 restent
indécidables au niveau de leurs familles de cinq, même si des lignes individuelles Haiku ou
Grok sont calculables. H4 est indisponible : ses paires exigent GPT-5.4/GPT-5.6 Luna ou
Sonnet/Haiku, et les premières conditions ne sont pas jouées. Aucune conclusion intermodèle
ou confirmatoire ne peut être étendue à partir des deux fermés restants.
