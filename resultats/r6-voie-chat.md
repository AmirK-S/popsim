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
