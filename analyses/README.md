# analyses/

Les scripts d'experience du projet. Un script par chantier, prefixe par sa lettre et son
numero (`a*` pour les analyses, `r*` pour les runs preenregistres, `c*`, `i*`, `t*` pour
les autres programmes), plus les files de nuit `file_*.sh`. Chacun porte en tete de fichier
son protocole, ses entrees, ses sorties et sa regle de reprise.

## Le fichier d'arret, `data/traces/STOP`

`touch data/traces/STOP` arrete proprement un run en cours : la boucle relit ce fichier
entre deux appels de modele, ecrit `ARRET DEMANDE` dans son journal, ferme sa trace, ecrit
son resume et sort avec le code 0, sans trace tronquee et sans reprise a la main.
Le script ne l'efface jamais : celui qui l'a pose le retire, sinon le run suivant
s'arreterait aussitot. Lu par `r1_oracle_camps.py` (donc aussi par `r4_oracle_socle.py`,
qui appelle sa boucle) et par `a5_agents_locaux_gss.py`.
Pourquoi : dans la nuit du 8 au 9 septembre 2026, le SIGINT de 05:45 n'a pas arrete R2,
bloque dans un appel HTTP, ni le SIGTERM le serveur ; il a fallu un `kill -9` a 06:01 et
relancer R3 a la main (`JOURNAL-NUIT-2026-09-09.md`, entree de 06:03).

## La relance, et `--sans-relance`

`r1_oracle_camps.py` relance une fois, avec un rappel de format et un exemple chiffre,
quand la premiere reponse n'est pas lisible. `resultats/r4-resultats.md` section 3.1 a
mesure qu'en mode completion cette relance recopie son exemple 45 fois sur 45.
`resultats/r5-preenregistrement.md` section « Relance » la supprime : l'option
`--sans-relance` de `r1_oracle_camps.py` et de `r4_oracle_socle.py` fait d'un echec de
premiere tentative un rejet, jamais rejoue, et le taux de rejet par condition se publie en
tete du rapport (`taux_rejet` dans le resume, `rejets_cumules` ligne a ligne dans la
trace). Le defaut reste le comportement d'origine, pour que R1 et R4 se rejouent a
l'identique.

## Tests

`.venv/bin/python analyses/test_moteur_relance_arret.py` verifie les deux mecanismes
ci dessus avec un faux moteur, sans aucun appel de modele et sans llama-server.

## R6, l'oracle des camps sur les modeles distants

`r6_oracle_distant.py` rejoue l'invite de R1 contre l'API compatible OpenAI d'OpenRouter.
Un seul mode de lecture, celui de R1 : temperature 0, un appel par cellule, `max_tokens`
150, `R1.parser` importe, aucune relance, aucune sequence d'arret a la main
(`resultats/r6-preenregistrement-v2.md`). Les deux formats d'invite viennent de
`R1.systeme`, `R1.utilisateur` et `R5.bloc_exemples`, jamais recopies. Securites : plafond
dur en USD (`--plafond`), feu vert `data/traces/GO-R6` sans lequel aucun appel payant ne
part, fichier d'arret `data/traces/STOP`, reprise sur trace existante, `--essai N` qui
mesure le cout reel par cellule avant d'engager la campagne, et un reglage de raisonnement
au minimum inscrit dans chaque ligne de trace.

`r6_voie_chat.py` est la verification locale de l'etage 0, a zero euro : sur le meme fichier
de poids que R1, 40 cellules tirees d'avance sont jouees par `/completion` avec le gabarit
rendu a la main comme en R1, et par `/v1/chat/completions` avec le client de R6. Seuil
preenregistre : 38 distributions identiques sur 40. Resultat du 9 septembre 2026 : 40 sur
40, distance de variation totale nulle (`resultats/r6-voie-chat.md`).

`.venv/bin/python analyses/test_r6_client.py` verifie le client hors ligne, avec un faux
serveur HTTP local : les deux formats d'invite, la lecture de R1, le plafond, le fichier
d'arret, la reprise, le feu vert, le raisonnement et le resume d'essai. Aucun reseau,
aucune cle lue, aucun octet ecrit dans `data/`.
