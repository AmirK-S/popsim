# Protocoles de recherche, ce qu'il faut connaitre pour popsim

Note ecrite le 8 septembre 2026. Elle repond a une question simple : quelles regles de travail les
chercheurs se donnent pour eviter qu'une idee juste sur le papier tombe au premier test, et
lesquelles popsim applique deja sans le savoir.

## 1. Pourquoi une idee juste sur le papier tombe au test

1. Deux quantites portent le meme nom et on les compare comme si c'etait la meme.
   Chez nous : l'ecart de 0,07 point est calcule sur 150 items, le facteur 13,5 sur 169 ;
   recalcule sur 169 items, l'ecart vaut -0,88 et exclut zero (a17, objection 2).

2. Une deduction vraie d'un cas est reappliquee a un cas voisin ou elle est fausse.
   Chez nous : `gss_v6` n'a recu ni ideologie ni parti (0,200 et 0,165), `gss_v8` les a recus
   (0,961 et 0,994) ; a14 a corrige a2 en lisant le papier qui decrit v8 alors que a2 mesurait v6
   (a17, objection 3).

3. Le correctif repose sur une hypothese que le traitement des donnees casse.
   Chez nous : la correction de Miller Madow n'est pas invariante sous le transport ; a lambda 0 le
   ratio inter estime vaut -0,13, soit plus que la demi largeur des intervalles publies (a17,
   objection 4).

4. La liste des tests est arretee apres avoir vu les chiffres, donc le seuil ne veut plus rien dire.
   Chez nous : a17 releve l'absence totale de correction pour tests multiples dans les cinq
   rapports, la correction de Holm arrive apres coup dans a28, et le retrait des quatre items
   nominaux fait changer de signe C2 et C3.

5. L'effet tient au niveau du groupe et disparait des qu'on regarde chaque cas.
   Chez nous : huit conditions LLM a +0,050 contre cinq predicteurs statistiques a 0,000,
   p = 0,0008 par permutation, mais aucune condition ne passe seule, meilleur p ajuste 0,144
   (a28, test 1).

## 2. Les huit protocoles a connaitre

1. Preenregistrement, sur OSF.
   Ecrire avant de regarder les chiffres la question, les mesures, les analyses et les seuils, puis
   deposer ce texte horodate sur osf.io. Il sert a separer ce qu'on avait predit de ce qu'on a
   explique apres coup, ce que Nosek et ses coauteurs appellent prediction contre postdiction.
   Cout : une a trois heures, gratuit, modifiable si le changement est declare.
   Chez nous : deposer le plan de la prochaine nuit de calcul avant de la lancer.

2. Rapport enregistre.
   Le protocole passe en revue par une revue scientifique avant que les donnees existent ; un accord
   de principe est donne sur la question et la methode, et le papier est publie que le resultat soit
   positif ou nul. Chambers et Tzavella comptent plus de 300 revues et beaucoup moins de resultats
   positifs dans ce format que dans la litterature ordinaire.
   Cout : plusieurs mois de delai, hors de portee pour un preprint ; garder l'idee de criteres de
   qualite fixes avant, independants du resultat.

3. Correction pour tests multiples, avec la famille d'hypotheses fixee d'avance.
   Tester huit conditions sur cent items produit des faux positifs a coup sur ; Holm ou Benjamini
   Hochberg corrigent le seuil, mais seulement si la liste des tests est arretee avant de voir les
   chiffres. Ioannidis le pose comme regle : plus on teste de relations, moins un resultat
   significatif a de chances d'etre vrai. Cout : quelques lignes de code, et de la puissance perdue.
   Chez nous : ecrire la liste des tests dans le preenregistrement, avant de la lancer.

4. Jeu de donnees tenu secret, et separation exploration contre confirmation.
   Mettre une part des donnees de cote, ne jamais la regarder pendant l'exploration, l'ouvrir une
   seule fois pour le test final. Dwork et ses coauteurs montrent que reutiliser le meme jeu pour
   choisir puis pour tester detruit la validite du test, meme sans mauvaise foi.
   Cout : de l'echantillon en moins, et la discipline de ne pas regarder.
   Chez nous : declarer un jeu de confirmation qu'aucun agent n'ouvre avant le test final.

5. Analyse multivers.
   Refaire l'analyse sur toutes les variantes raisonnables de traitement des donnees, mesure,
   exclusions, codage, et publier la distribution des resultats plutot que la meilleure version.
   Steegen, Tuerlinckx, Gelman et Vanpaemel montrent qu'un seul jeu de choix peut induire en erreur.
   Cout : du calcul, et un resultat presente plus prudemment.
   Chez nous : c'est a moitie fait sans etre nomme, trois mesures dans a1, avec et sans les quatre
   items nominaux dans a28 ; il reste a publier la grille entiere plutot que la ligne retenue.

6. Relecture adverse et collaboration adverse.
   La relecture adverse charge quelqu'un de casser le dossier ; la collaboration adverse va plus
   loin : deux personnes qui predisent l'inverse ecrivent ensemble le protocole avant de le lancer,
   s'engagent sur ce que chaque resultat voudra dire, et confient l'execution a un tiers. C'est la
   methode de Mellers, Hertwig et Kahneman sur l'effet de conjonction.
   Cout : lent, et il faut un contradicteur reel.
   Chez nous : a17 est deja une relecture adverse ; demander a Simon d'ecrire sa prediction avant.

7. Replication sur un second jeu de donnees avant publication.
   Rejouer la mesure decisive sur des donnees collectees autrement avant d'annoncer quoi que ce
   soit. Sur cent etudes de psychologie rejouees par l'Open Science Collaboration, 39 pour cent
   seulement ont replique, avec des effets en moyenne deux fois plus petits.
   Cout : une nuit de calcul, deja dans nos moyens.
   Chez nous : le facteur 11,4 sur les minorites vient du GSS de Stanford ; le refaire sur Twin.

8. Criteres d'arret ecrits d'avance.
   Ecrire avant le test ce qui ferait abandonner l'idee, et a quel moment on cesse de collecter.
   C'est la premiere des six exigences de Simmons, Nelson et Simonsohn : la regle d'arret est
   decidee avant, pas quand la courbe devient jolie.
   Cout : nul, sauf le renoncement le jour venu.
   Chez nous : le test 2 a bien tue une idee, mais rien n'etait ecrit ; ecrire la condition de mort
   de l'option A avant de la defendre.

## 3. Ce que le projet fait deja et ce qu'il ne fait pas encore

| protocole | fait | ce qui manque |
|---|---|---|
| Preenregistrement | non | aucun plan depose avant un run ; l'idee cle est choisie apres les chiffres |
| Rapport enregistre | non | sans objet pour un preprint, mais aucun critere de succes fixe avant |
| Tests multiples, famille fixee | partiel | Holm applique dans a28 seulement, et apres coup ; aucune liste ecrite avant |
| Jeu tenu secret, exploration contre confirmation | non | le GSS de Stanford a servi a explorer et a conclure |
| Analyse multivers | partiel | trois mesures dans a1, deux jeux d'items dans a28, jamais publie comme grille |
| Relecture adverse | oui | a17 et a26 le font ; aucune collaboration adverse avec un tiers humain |
| Replication sur un second jeu | partiel | a6 rejoue la double distorsion hors GSS ; le resultat minorites ne l'est pas |
| Criteres d'arret ecrits d'avance | non | trois idees abandonnees en un jour, aucune sur un critere ecrit avant |

## 4. Le protocole du projet, en dix lignes

1. Avant chaque nuit de calcul, un agent redige une page : question, mesure exacte avec son nombre
   d'items, liste complete des tests, seuil apres correction, et ce qui ferait abandonner l'idee.
2. Amir lit cette page et la valide en une ligne. C'est la seule chose qu'il fait lui meme, et elle
   doit se faire avant de voir le moindre chiffre.
3. La page est deposee sur OSF, horodatee, avant que le premier script tourne.
4. Un jeu de confirmation est nomme dans la page et reste ferme jusqu'au test final.
5. Les agents lancent, mesurent, et rendent les resultats de la liste prevue, dans l'ordre prevu.
6. Tout ce qui n'etait pas dans la liste est rendu a part, sous le titre exploration, sans p value.
7. La grille des variantes raisonnables est publiee entiere, pas la ligne la plus favorable.
8. Un agent adverse relit et cherche a casser, comme a17, avant toute diffusion.
9. La mesure decisive est rejouee sur le second jeu ; si elle ne tient pas, l'idee sort, sans debat.
10. Toute deviation du plan est ecrite dans le journal avec sa date et son motif.

## 5. Trois lectures pour aller plus loin

- Gelman et Loken, Le jardin aux sentiers qui bifurquent, 2013 : pourquoi une seule analyse suffit a
  produire un faux positif. https://sites.stat.columbia.edu/gelman/research/unpublished/forking.pdf
- Nosek, Ebersole, DeHaven et Mellor, The preregistration revolution, PNAS 2018 : ce que le
  preenregistrement empeche et ce qu'il n'empeche pas. https://doi.org/10.1073/pnas.1708274114
- Steegen, Tuerlinckx, Gelman et Vanpaemel, Increasing transparency through a multiverse analysis,
  2016 : comment publier toutes les variantes. https://doi.org/10.1177/1745691616658637

## Addendum du 9 septembre 2026, apres le bilan des predictions (resultats/bilan-predictions.md)

Sur 53 predictions preenregistrees et tranchees, 23 tenues, 16 fausses, 14 a moitie. Le defaut
n'est pas d'etre faux en notre faveur, c'est d'avoir ecrit 37 predictions en faveur de la these
contre 3 qui pouvaient couter. Trois regles s'ajoutent :

- R11, la prediction qui coute. Chaque page de plan contient au moins une prediction dont
  l'echec ferait tomber la these, nommee comme telle.
- R12, toute borne se prouve avant. Un plancher, un plafond ou un nul se justifie dans la page
  de plan, jamais ajoute apres les chiffres pour sauver une prediction.
- R13, le critere de verdict se nomme, ne se remplace pas, et son anteriorite se prouve hors
  de la machine. Les empreintes SHA-256 des pages de plan sont dans
  resultats/manifeste-preenregistrements.txt ; un depot externe (OSF ou git avec commit) est a
  mettre en place avant le prochain run.
