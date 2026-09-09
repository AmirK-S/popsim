# r5. Page de plan : gabarit ChatML plus trois exemples, et relance sans nombre

Ecrite le 9 septembre 2026 a 09:50, avant tout appel. Validee par Amir (« R5 oui go ») ; deposee sur OSF le 9 septembre 2026 a 12:20 CEST, registration https://osf.io/3r6zg/ , avant le premier appel du run.

## Question

R4 mesure « le format » comme un bloc : gabarit de conversation contre completion a trois
exemples. Cette page separe les deux. La condition `q4gab3` prend le meme fichier GGUF
`Qwen3-4B-Instruct-2507`, le gabarit ChatML de R1, et les trois exemples de R4 places dans
le tour utilisateur. Les 894 cellules de R1 sont rejouees a l'identique (149 items, 3 camps,
2 demandeurs, temperature 0, `top_k` 1, un seul serveur).

## Hypotheses, ecrites avant

- H1 : les exemples font la marche. `q4gab3` sur l'ecart entre camps decrit est a moins de
  0,15 de `q4nogab` (0,727). Alors le gabarit est innocent et la lecon est « donnez des
  exemples ».
- H2 : le gabarit fait la marche. `q4gab3` reste a moins de 0,15 de `q4` (0,245). Alors le
  gabarit ecrase meme avec des exemples, et la lecon vise le mode assistant lui meme.
- H3 : les deux comptent. `q4gab3` tombe entre les deux, hors des deux bandes. Aucune des
  deux lectures simples n'est permise.
Pari : H3, avec une valeur plus proche de `q4nogab` que de `q4`. Ce pari est contre la
these « le mode assistant censure », donc il peut couter.

## Relance

La relance de R1 recopie son exemple chiffre 45 fois sur 45 en completion. Elle est
supprimee : un echec de premiere tentative est compte comme rejet, jamais rejoue. Le taux de
rejet par condition est publie en tete du rapport. Un item est retire d'un contraste si une
des deux conditions comparees le rejette.

## Analyse

Meme evaluateur (`r1_evaluer.py --suffixe r5`), memes 79 items orientes, bootstrap par item
2 000 tirages, permutation de signe 20 000 tirages, Holm sur les trois contrastes de cette
page et sur eux seuls. Aucun autre test.

## Cout

894 appels, environ une heure, zero euro, rien ne sort de la machine.
