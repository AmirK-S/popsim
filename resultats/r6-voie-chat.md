# r6, etage 0. La voie `chat` reproduit elle la voie `/completion` de R1 ?

Mesure du 2026-09-09 13:12, en local, sur `Qwen3-4B-Instruct-2507` Q4_K_M, un seul `llama-server`, configuration de a3 section 4.7 (contexte 4096, `-np 1`, cache KV q8_0). Zero appel distant, zero euro. Verification exigee par `resultats/r6-preenregistrement-v2.md`, etage 0, avant tout appel payant.

## Ce qui est compare

40 cellules du plan F1, tirees a graine fixe 20260909 avant le lancement et ecrites dans `data/traces/r6-verif-cellules.txt`. Chaque cellule est jouee par trois voies, sur le meme fichier de poids et la meme invite, construite par `R1.systeme` et `R1.utilisateur` et jamais recopiee.

| voie | transport | gabarit | lecture |
|---|---|---|---|
| `trace` | deja ecrite le 9 septembre | ChatML rendu a la main par `R1.gabarit` | `R1.parser` |
| `compl` | `/completion`, rejouee maintenant | ChatML rendu a la main par `R1.gabarit` | `R1.parser` |
| `chat` | `/v1/chat/completions`, client de R6 | applique par le serveur | `R1.parser` |

## Resultat

| comparaison | distributions identiques | sur | taux |
|---|---|---|---|
| `chat` contre `compl` | 40 | 40 | 1.000 |
| `chat` contre `trace` de R1 | 40 | 40 | 1.000 |
| `compl` contre `trace` de R1 | 40 | 40 | 1.000 |

Distance de variation totale moyenne entre `chat` et `compl` : 0.000000 ; maximum 0.000000.

Rejets de parse : 0 dans la trace de R1, 0 en `compl`, 0 en `chat`.

## Verdict contre le seuil de la v2

Seuil preenregistre : au moins **38 sur 40** distributions identiques entre `compl` et `chat`. Mesure : **40 sur 40**. **PASSE.**

La voie `chat` est donc lisible comme la voie de R1 : les distributions de R6 se comparent directement a `q4`, `q4nogab`, `q4base` et `q4gab3` sans colonne de protocole supplementaire.

## Cout en temps

Chargement du serveur 1.0 s. Voie `compl` 26.2 s pour 40 cellules. Voie `chat` 22.6 s. Total de la seance 49.9 s, soit 0.8 min. Zero euro : aucun appel distant.

Latence mediane de la voie `chat` : 579.9 ms par cellule.

## Ce que je n'ai pas pu verifier

1. **Que le gabarit applique par `llama-server` est celui qu'appliquent les fournisseurs distants.** La mesure porte sur un serveur local qui lit le gabarit embarque dans le fichier GGUF de Qwen. OpenAI, Anthropic, Google et xAI appliquent le leur, qu'aucune API ne rend lisible. Ce qui est verifie ici est que le CLIENT de R6 et la mise en deux tours de conversation ne cassent rien ; ce n'est pas une verification du gabarit de chaque fournisseur.
2. **Le determinisme des API distantes a temperature 0.** Il est mesure ici sur un serveur local, ou il est acquis. La v2 prevoit pour cela le plancher machine des 40 memes cellules rejouees sur chaque modele payant ; il n'est pas joue par ce script.
3. **Que les 40 cellules representent les 894.** Elles sont tirees a graine fixe dans le plan complet, sans stratification par nombre de modalites ni par camp. Un desaccord concentre sur les items a K eleve ne se verrait pas forcement a cet effectif.
4. **Le format `q4gab3`.** La verification porte sur F1, gabarit seul. F2 place les trois exemples dans le tour utilisateur ; rien ne dit qu'un gabarit serveur les traite comme le fait la concatenation de R5, et ce script ne le mesure pas.
5. **Le comportement du client sous erreur 429 et sous limite de debit.** Le serveur local n'en produit aucune ; seul le faux serveur de `analyses/test_r6_client.py` couvre ce chemin.

## Questions ouvertes pour Simon

1. Le seuil de 38 sur 40 a ete pose avant la mesure, sans modele d'erreur. Faut il le lire comme un test binaire, ou publier plutot la distance de variation totale moyenne entre voies a cote de chaque quantite, comme la v2 le fait deja pour le plancher machine ?
2. Si la voie `chat` diverge sur les items a beaucoup de modalites, la reponse est elle de retirer ces items du perimetre comparatif, ou de publier deux colonnes de protocole ?
3. La v2 interdit toute reformulation d'invite. Un modele distant qui refuse le format sur plus de deux cellules sur dix est retire du panel. Est ce le bon arbitrage pour le papier, ou faut il publier le taux de refus de format comme une mesure a part entiere, ce qu'il est ?
4. Le meme fichier de poids servi par un fournisseur distant peut etre quantifie autrement. La ligne de registre porte le champ `provider` ; suffit elle, ou faut il refuser les modeles ouverts dont la quantification aval n'est pas publiee ?

---

## Essai a blanc sur modeles gratuits

Section ajoutee le 9 septembre 2026 a 13:30, apres la mesure ci dessus. Elle est ecrite a
la main : relancer `analyses/r6_voie_chat.py` regenere le rapport et l'effacerait.

Etage 0 de la v2, second point : l'essai a blanc du client OpenRouter sur des modeles
`:free`, avant tout appel payant. `data/traces/GO-R6` n'existe toujours pas, aucun modele
payant n'a ete appele, le solde est inchange a 6,043154 USD avant comme apres.

### Le premier essai a echoue, et c'etait le client

Traces archivees dans `data/traces/r6-essai-echec-2026-09-09/`. Deux defauts, tous deux du
client, aucun du protocole.

1. **Un 429 etait compte comme un rejet de format.** `google/gemma-4-31b-it:free` a rendu
   dix fois « temporarily rate-limited upstream, shared pool » et le client a publie
   100 pour cent de rejets pour un modele qui n'avait rien repondu. Un rejet est un echec
   de parse sur une reponse RECUE ; un 429 ou un 5xx est un incident de transport.
2. **Le raisonnement n'etait pas coupe.** `--raisonnement aucun` n'envoyait aucun champ,
   donc le modele raisonnait par defaut : `nvidia/nemotron-3-super-120b-a12b:free` ecrivait
   son raisonnement dans le contenu (« We need to answer with distribution... »), saturait
   les 150 jetons avant d'avoir repondu, et facturait 165 jetons de raisonnement par
   cellule, dix fois sur dix.

### Ce qui a ete corrige dans `analyses/r6_oracle_distant.py`

| defaut | correction | verifie par |
|---|---|---|
| 429 compte comme rejet | trois reprises, 5 puis 20 puis 60 s, sur les seuls codes 429 et 5xx ; incidents comptes dans `erreurs_reseau` et `statuts_reseau`, jamais dans `taux_rejet` | `test_r6_client.py`, section 9 |
| cellule perdue apres reprises | la cellule est « non jouee » : elle part dans `r6-<cle>-non-jouees.jsonl`, n'entre pas dans la trace principale, et la reprise sur index la rejoue | section 9, reprise verifiee |
| code non rejouable rejoue quand meme | un 400 n'est jamais rejoue, une seule tentative, statut consigne | section 9b |
| raisonnement laisse par defaut | `--raisonnement off` devient le defaut et envoie `{"enabled": false, "exclude": true}` ; `none` envoie `{"effort": "none", "exclude": true}` | section 4 |
| desactivation supposee et non verifiee | ligne « raisonnement desactive effectif », lue sur les jetons factures : `oui`, `non`, ou `inconnu` si le fournisseur ne les compte pas | section 4 |
| modele qui refuse de couper son raisonnement | `--max-tokens` relevable et `--fin-seulement N`, qui ne donne au parse que les N dernieres lignes ; les deux inscrits dans la trace, le cout du raisonnement reste dans le cumul | section 4b |
| `--essai N` pouvait depasser N appels | la limite compte les cellules TENTEES, pas seulement celles qui aboutissent | section 9 |

Le test hors ligne passe 118 verifications, sans reseau et sans cle.

### L'essai propre

Dix cellules du plan F1, tirees a graine fixe avant le lancement dans
`data/traces/r6-essai-cellules.txt`, les memes pour les deux modeles. Format gabarit seul,
temperature 0, `max_tokens` 150, `--raisonnement off`, `--pause 3.5` pour tenir les
20 requetes par minute du palier gratuit, plafond 0,01 USD.

| modele `:free` | cellules jouees | rejets de parse | non jouees | incidents 429 ou 5xx | jetons de raisonnement | raisonnement desactive effectif | latence mediane | jetons d'entree moyens |
|---|---|---|---|---|---|---|---|---|
| `nvidia/nemotron-3-super-120b-a12b:free` | 10 sur 10 | 1, soit 10,0 pour cent | 0 | 0 | 0, maximum 0 | **oui** | 1 463 ms | 214,6 |
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 3 sur 10 | 0 | 0 | 0 | 0, maximum 0 | **oui** | 82 002 ms | 211,0 |

Les deux passent les criteres de l'essai propre : rejets de parse sous 20 pour cent, zero
jeton de raisonnement, aucun incident de transport non gere. Cout : 0,00 USD, fournisseur
aval `Nvidia` pour les deux.

Trois faits utiles a la suite de R6.

- **L'unique rejet est une vraie mesure du modele**, pas un artefact : sur `partfull`,
  centre, adversaire, K egal a 3, le modele a rendu `A: 58  \nB: 58\nB: 22: 22\nC: 20: 20`,
  la lettre C manque et B est donnee deux fois. C'est exactement le genre de refus de format
  que la v2 demande de publier au lieu de le rattraper par une relance.
- **L'estimation de jetons de la v2 tient chez un autre tokenizer.** Elle annoncait
  210 jetons d'entree sous gabarit seul, comptes sur le tokenizer de Qwen, avec une marge
  d'erreur supposee de 15 pour cent. Mesure chez Nvidia : 214,6 et 211,0, soit 2,2 et
  0,5 pour cent d'ecart. La projection de cout de la page v2 n'a pas besoin d'etre revue.
- **Le palier 550 milliards est inutilisable en l'etat** : 82 secondes de latence mediane
  contre 1,5 seconde pour le 120 milliards. A ce debit, les 1 270 cellules du plan
  demanderaient 29 heures pour un seul modele. Il reste dans le panel des gratuits comme
  ligne descriptive, pas comme candidat a un run complet.

### Ce que cet essai n'a pas pu finir

Le second modele s'est arrete a la troisieme cellule sur dix, proprement, sur le fichier
`data/traces/STOP`. Ce fichier n'a pas ete pose par R6 : il porte
`2026-09-09T13:25:26 r2b : swap 12531 Mio au dessus du seuil 10240 Mio`, il a ete ecrit par
le run r2b, qui a fini a 13:25:33. **Il est toujours en place et bloque tout nouveau run**,
le mien comme ceux de la file de nuit. Je ne l'ai pas retire, pour deux raisons : la regle
de la maison veut que celui qui pose le fichier le retire, et surtout la condition qui l'a
fait poser tient encore, le swap etant a 12,3 Gio pour un seuil de 10,2 Gio. Le retirer
laisserait repartir un run local sous la meme pression memoire. C'est a Amir de decider :
retirer `data/traces/STOP`, puis relancer la commande ci dessous pour completer les sept
cellules manquantes, que la reprise sur index rejouera toute seule.

```
.venv/bin/python analyses/r6_oracle_distant.py --modele nvidia/nemotron-3-ultra-550b-a55b:free \
  --plan f1 --liste data/traces/r6-essai-cellules.txt --essai 10 --plafond 0.01 \
  --raisonnement off --pause 3.5 --suffixe r6essai2
```

Deux autres choses ne sont pas verifiees par cet essai. **Le chemin 429 n'a pas ete
exerce en vrai** : les deux modeles Nvidia n'en ont rendu aucun, le mecanisme de reprise
n'est verifie que par le faux serveur du test hors ligne. Et **aucun modele payant n'a ete
touche** : ni le determinisme a temperature 0, ni les jetons de raisonnement des cinq
fermes, ni le comportement du parametre de fournisseur aval ne sont mesures ; ils le seront
par l'essai de dix cellules que la v2 impose modele par modele, apres `GO-R6`.
