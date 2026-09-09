# Lecture complete du corpus, consigne commune

Lancee le 8 septembre 2026 au soir, a la demande d'Amir : lire le corpus complet, quitte a y
passer du temps, pour comprendre comment les choses fonctionnent reellement, puis lier.

Methode, pour chaque theme :
1. Partir des references confirmees de corpus/0N. Pour chacune, remonter les citations (ce
   qu'elle cite) et descendre (ce qui la cite) via OpenAlex (api.openalex.org, sans cle) et
   Semantic Scholar (api.semanticscholar.org/graph/v1, sans cle, quotas), sur deux niveaux
   quand c'est pertinent. Garder tout ce qui touche au theme, y compris hors informatique
   (psychologie sociale, science politique, methodologie d'enquete, sociologie).
2. Lire EN ENTIER (HTML arXiv ou pdftotext) chaque papier qui apporte un fait, une mesure ou un
   mecanisme ; les autres, resume et section resultats. Aucun chiffre n'est repris sans avoir
   ete lu dans le texte.
3. Ecrire corpus/lecture-complete/0N-<theme>.md : (a) la table etendue (grille de
   corpus/00-GRILLE.md, plus une colonne « trouve par » : table initiale, citation amont,
   citation aval) ; (b) « Comment ca fonctionne » : les mecanismes etablis, chacun avec ses
   preuves et ses contre preuves, en paragraphes relies entre eux, pas une liste ; (c) « Ce qui
   se contredit » avec la variable qui explique la contradiction quand on la trouve ; (d) « Ce
   que ca permet de tester chez nous tout de suite », chaque test avec son cout ; (e) « Ce que
   personne n'a fait » ; (f) « Ce que je n'ai pas pu verifier ».
4. Forme : francais, jamais de tiret cadratin ni demi cadratin, niveaux [CONFIRME] [PROBABLE]
   [NON LU], citations exactes en anglais.
Le chantier ne s'arrete pas a un nombre de papiers. Il s'arrete quand les citations ne rendent
plus rien de neuf sur le theme.
