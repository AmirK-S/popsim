# t3. La grille d'audit, version 0 : ce qui tient dans les textes et ce qui reste une lecture

Rapport court accompagnant `protocoles/03-grille-d-audit.md`, ecrit le 9 septembre 2026.
Mois 9 du programme A de `MOONSHOTS.md`, fusionne avec le livrable de norme du programme B.
**Aucun code, aucun calcul nouveau, aucun fichier existant modifie.** Les textes de loi ont ete
ouverts sur EUR-Lex et cites au mot. Les chiffres sont lus dans les rapports du dossier.

Conventions : **[CONFIRME]** avec URL et article, **[MESURE]**, **[PROBABLE]**, **[HYPOTHESE]**.

---

## Reponse en une ligne

**Les deux textes europeens donnent une prise reelle mais indirecte : ils obligent a evaluer et a
attenuer un « effet négatif réel ou prévisible sur le discours civique » et a le faire sur la base
de « protocoles et d'outils normalisés », sans nommer aucune quantite ni fixer aucun seuil ; la
grille se propose exactement a cette place vide, et le dossier fournit deja quatre des sept
quantites avec leur plancher humain, mais aucune autorite n'a confirme que la fidelite de
representation des camps entre dans le champ, et le detail le plus vendable de la grille, le fait
qu'un tiers l'execute avec un ordinateur portable et zero euro, est aussi ce qui la rend
acceptable sans changer la loi.**

---

## 1. Ce qui est verifie dans les textes

Verifie ici, article par article, sur le texte officiel francais.

**Reglement sur les services numeriques, reglement (UE) 2022/2065**
[https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32022R2065]

| article | ce qu'il dit, verifie au mot | ce que la grille en tire |
|---|---|---|
| art. 33, par. 1 | seuil de designation, « un nombre mensuel moyen de destinataires actifs du service dans l'Union égal ou supérieur à 45 millions » | le champ d'application, et sa limite : le texte vise un service designe, pas un assistant en soi |
| art. 34, par. 1, point c) | risque systemique : « tout effet négatif réel ou prévisible sur le discours civique, les processus électoraux et la sécurité publique » | **le point d'accroche principal du bloc A** |
| art. 34, par. 1, second alinea | evaluation annuelle, et « avant de déployer des fonctionnalités susceptibles d'avoir une incidence critique sur les risques recensés » | la frequence de la grille est deja dans le texte ; la perissabilite par version cesse d'etre une objection |
| art. 34, par. 2 | l'evaluation porte sur « tout autre système algorithmique pertinent », et sur la manipulation intentionnelle « y compris par l'utilisation non authentique ou l'exploitation automatisée du service » | le point d'accroche du bloc C, mais seulement pour un flux interne a une plateforme designee |
| art. 34, par. 3 | conservation trois ans, communication a la Commission et au coordinateur sur demande | l'obligation de garder les sorties brutes existe deja |
| art. 35, par. 1, points d) et f) | mesures d'attenuation : « le test et l'adaptation de leurs systèmes algorithmiques » ; « le renforcement des processus internes, des ressources, des tests, de la documentation ou de la surveillance [...] notamment en ce qui concerne la détection des risques systémiques » | c'est le seul endroit des deux textes ou le mot « test » designe une mesure exigible |
| art. 37, par. 1 et 2 | audit independant annuel aux frais du fournisseur ; acces « à toutes les données et à tous les locaux pertinents » ; interdiction d'entraver l'audit | l'auditeur tiers a un droit d'acces ecrit ; il lui manque une quantite a mesurer |
| art. 40, par. 4 et 8 | acces aux donnees pour chercheurs agrees, « à la seule fin de procéder à des recherches contribuant à la détection, au recensement et à la compréhension des risques systémiques [...] de l'article 34, paragraphe 1 » ; conditions d'agrement, dont publication gratuite des resultats | **le levier le plus concret pour un tiers**, et il nomme exactement la finalite de la grille |

**Reglement sur l'intelligence artificielle, reglement (UE) 2024/1689**
[https://eur-lex.europa.eu/legal-content/FR/TXT/HTML/?uri=CELEX:32024R1689]

| article | ce qu'il dit, verifie au mot | ce que la grille en tire |
|---|---|---|
| art. 3, point 65) | definition du risque systemique, dont « effets négatifs réels ou raisonnablement prévisibles sur [...] les droits fondamentaux ou la société dans son ensemble » | la definition est assez large pour porter la grille, et assez vague pour ne rien garantir |
| considerant 110 | les risques systemiques comprennent « tout effet négatif réel ou raisonnablement prévisible sur les processus démocratiques » | le seul endroit des deux textes ou la democratie est nommee cote modele |
| art. 51, par. 1 et 2 | classification, presomption au dela de 10 puissance 25 operations en virgule flottante | qui est concerne |
| annexe XIII | criteres de designation, dont la portee presumee a 10 000 utilisateurs professionnels enregistres dans l'Union et le nombre d'utilisateurs finaux inscrits | qui d'autre peut l'etre |
| art. 53, par. 1 et 2 | documentation technique, information des integrateurs, politique de droit d'auteur, resume du contenu d'entrainement ; exemption des modeles libres, **sauf** s'ils presentent un risque systemique | un modele ouvert a risque systemique n'echappe pas a la documentation |
| **art. 55, par. 1, point a)** | « effectuent une évaluation des modèles sur la base de protocoles et d'outils normalisés reflétant l'état de la technique, y compris en réalisant et en documentant des essais contradictoires » | **la place exacte de la grille** : le texte exige des protocoles normalises et n'en nomme aucun |
| art. 53, par. 4, et art. 55, par. 2 | un code de bonne pratique vaut demonstration de conformite jusqu'a la publication d'une norme harmonisee ; celui qui n'y adhere pas doit demontrer « d'autres moyens appropriés » | **le vehicule realiste** : un code, pas une obligation nouvelle |
| art. 56, par. 2, points c) et d), et par. 6 | les codes doivent couvrir « l'identification du type et de la nature des risques systémiques » et « les mesures, procédures et modalités d'évaluation et de gestion » ; la Commission peut approuver un code par acte d'execution et lui donner validite generale | le chemin d'adoption, de bout en bout |

---

## 2. Ce qui reste une lecture

1. **Aucun des deux textes ne nomme la representation des groupes politiques.** Ni l'expression
   « fidelite de representation », ni aucune obligation de mesurer ce qu'un systeme dit d'un camp.
   La chaine est : art. 34, par. 1, point c), plus art. 35, par. 1, points d) et f), plus art. 55,
   par. 1, point a). Elle est defendable, elle n'est pas acquise. [HYPOTHESE]

2. **Le DSA ne saisit pas un assistant conversationnel autonome.** Il saisit un service designe au
   titre de l'article 33. Un assistant integre a un service designe entre dans le champ comme
   element de sa conception et de son fonctionnement ; un assistant autonome est une question non
   tranchee ici. [HYPOTHESE]

3. **L'audit structurel d'un flux, bloc C, a une prise plus etroite que le brainstorm ne
   l'esperait.** L'article 34, paragraphe 2, second alinea, sur « l'utilisation non authentique ou
   l'exploitation automatisée du service », vaut pour les sondages, notes, votes et consultations
   internes a une plateforme designee. **Il ne vaut pas pour la consultation publique d'une
   administration**, qui n'est pas un service intermediaire. La question posee par `MOONSHOTS.md`,
   « sous quel article un audit structurel entre dans un dossier de risque systemique », recoit
   donc une reponse partielle : l'article existe pour le flux d'une plateforme, il n'existe pas
   pour le flux d'une administration. [PROBABLE]

4. **Pour un fournisseur de population synthetique, aucun cadre contraignant n'a ete identifie.**
   Le reglement IA atteint le fournisseur du modele, pas le vendeur d'un fichier de reponses
   fabriquees. [PROBABLE] Les cadres du metier de l'enquete, code international CCI et ESOMAR,
   lignes directrices sur la qualite des echantillons en ligne, standards de divulgation de
   l'AAPOR, norme ISO 20252, sont des candidats **et n'ont pas pu etre ouverts** : voir la section
   4. En attendant, le levier n'est pas une regle publique, c'est une clause d'achat, les trois
   nombres du bloc C recalcules a la taille et au questionnaire livres, en condition de reception.
   [HYPOTHESE]

5. **Aucun des deux textes ne fixe de seuil, et le dossier explique pourquoi il serait premature
   d'en fixer un.** Sur la meme quantite, trois modeles ouverts donnent 0,25, 0,62 et 1,27, avec
   des intervalles disjoints du plancher humain **dans des directions opposees** ; un seul modele
   va de 0,12 a 1,62 selon le protocole [MESURE, `r1-resultats.md` sections 1.2 et 2.2]. La grille
   fixe donc un protocole et un registre, et laisse le seuil a la mesure. C'est la lecture que
   l'article 55, paragraphe 1, point a), autorise le mieux : il demande des protocoles, pas des
   valeurs.

6. **La grille ne peut pas remplir toutes ses cases aujourd'hui.** Le bloc B n'a jamais ete mesure
   hors du GSS ; le bloc A n'a jamais ete mesure hors des Etats Unis, hors de trois modeles
   ouverts petits, hors d'une invite ; aucun fichier reel a contamination documentee n'existe ; et
   la comparaison a trois termes n'existe que sur des compositions de camp, avec deux items sur
   huit dotes d'un terme de systeme. Ce sont des trous nommes, pas des trous caches.

---

## 3. A qui l'envoyer, et dans quel ordre

**Un, un chercheur en science politique, avant tout le reste.** C'est le seul destinataire qui
peut lever le trou le plus grave, l'absence de population de reference hors des Etats Unis avec
une vague de reinterrogation. Sans plancher, il n'y a pas de grille. Il apporte aussi ce que la
grille ne peut pas s'acheter avec du calcul : le jeu ou de vrais repondants estiment l'autre camp
sur des **opinions** et non sur des compositions, ce qui decide de la version forte du programme.
Ce qu'on lui envoie : la grille entiere, plus la demande de donnees.

**Deux, une organisation de la societe civile qui a deja le statut de chercheur agree, ou qui peut
l'obtenir.** L'article 40, paragraphe 4, est ecrit pour elle et nomme exactement la finalite de la
grille ; le paragraphe 8 lui impose la publication gratuite des resultats, ce qui est le regime
que la grille demande de toute facon. C'est le destinataire qui peut faire tourner la grille sur
un service reellement servi au public, ce que nous ne pouvons pas faire.
Ce qu'on lui envoie : la grille, plus la fiche de restitution de la section 6.

**Trois, l'autorite.** Le Bureau de l'IA au titre de l'article 56, et non un coordinateur national
au titre du DSA, parce que le vehicule realiste est un code de bonne pratique et non une
obligation nouvelle, et parce que l'article 55, paragraphe 1, point a), a un trou nomme, « des
protocoles et outils normalisés », que la grille remplit. Ce qu'on lui envoie : la section 1, la
section 2 sans les quantites du bloc B, et l'argument d'executabilite par un tiers.
**Ce qu'il ne faut pas lui envoyer : un seuil.** Une autorite veut un seuil et nous rendons une
dispersion ; la seule facon honnete de le dire est de porter d'abord la quantite sur laquelle les
trois modeles concordent, la dependance a l'identite du demandeur, 2,7 a 4,2 fois le bruit humain,
et de garder l'ecart entre camps pour la partie technique.

**Quatre, un journaliste specialise, en dernier et pas avant que les trois autres aient repondu.**
Le resultat se raconte en une phrase, « la reponse depend de qui demande », et c'est precisement
le risque : la phrase voisine, « le systeme caricature le camp adverse pour plaire au demandeur »,
est **fausse en l'etat**, la mesure de direction etant nulle sur les six cellules apres correction.
Un article qui prend la seconde phrase pour la premiere coute plus qu'il ne rapporte.

**Et l'acheteur, hors classement, parce qu'il ne demande la permission a personne.** Un institut,
une administration ou une entreprise qui achete un fichier de reponses peut exiger les trois
nombres du bloc C en condition de reception des demain, sans texte et sans autorite. C'est le seul
usage de la grille qui ne depend d'aucune decision publique, et il coute quelques dizaines de
minutes de calcul sur quatre coeurs.

---

## 4. Ce que je n'ai pas pu verifier

1. **Les cadres du metier de l'enquete.** Budget de recherche web epuise, 200 requetes sur 200 ;
   `esomar.org` ne rend aucun contenu a une lecture automatique, `aapor.org` repond par un blocage.
   Je n'ai donc **aucun** titre, aucune date, aucun contenu d'ESOMAR, de l'AAPOR ou de l'ISO. La
   section 1.2 de la grille est entierement une lecture, et l'affirmation « aucun de ces cadres ne
   traite des repondants synthetiques » n'est **pas** etablie : je ne sais pas.

2. **Le statut juridique d'un assistant conversationnel autonome au regard du DSA.** J'ai verifie
   le texte des articles 33, 34, 35, 37 et 40 ; je n'ai verifie aucune decision de designation,
   aucune ligne directrice de la Commission, aucune decision nationale, aucune jurisprudence.

3. **L'etat des codes de bonne pratique au titre de l'article 56.** J'ai verifie le mecanisme et
   la procedure d'approbation ; je ne sais pas quel code existe aujourd'hui, ce qu'il contient, ni
   s'il couvre les processus democratiques. C'est la premiere chose a verifier avant d'envoyer
   quoi que ce soit au Bureau de l'IA, et c'est ce qui decide si la grille est une contribution ou
   un doublon.

4. **Les versions consolidees.** J'ai lu les textes tels que publies au Journal officiel, pas
   leurs versions consolidees a jour ; je n'ai pas verifie qu'aucune modification n'est intervenue
   depuis, ni l'etat des actes delegues et d'execution pris sur leur fondement.

5. **Les seuils proposes dans la grille sont des propositions, pas des mesures.** Ils sont
   justifies par la position des valeurs observees, et pour la mesure de personne par un
   intervalle vide entre 0,267 et 0,424 sur douze conditions. Aucun n'a ete valide sur une seconde
   population, et aucun n'a ete preenregistre.

6. **Aucun rapport interne n'a ete recalcule.** Aucun script relance, aucun papier tiers ouvert.
   `r1`, `i3b`, `a44`, `a47`, `a46`, `a12` et `a1` sont cites tels qu'ils se citent, y compris
   leurs errata.

7. **La lecture par camp, que la grille rend obligatoire, n'a pas son prix en correction de
   tests.** Trois statistiques fois le nombre de segments donne une famille plus grande et un
   seuil de Holm plus severe ; le calcul n'est pas fait dans le dossier et il tient en une heure.

8. **Rien sur le texte libre, rien sur l'identite, rien sur la coordination de comptes.** Un audit
   reel combine les quatre, et ce que la combinaison vaut n'est pas mesure.

---

## 5. Questions ouvertes pour Simon

1. **Faut il ecrire la grille comme une proposition de code de bonne pratique au titre de
   l'article 56, plutot que comme une grille d'audit ?** C'est le seul vehicule qui existe
   aujourd'hui, il a une procedure d'adoption ecrite jusqu'a l'acte d'execution, et il accepte des
   contributions d'experts independants. Le prix est qu'un code ne contraint que ses adherents.

2. **La dependance a l'identite du demandeur doit elle devenir le titre de la grille ?** C'est la
   seule quantite ou trois modeles de trois familles concordent en niveau, elle se raconte en une
   phrase, et elle ne demande aucun referent humain de second ordre. L'ecart entre camps, plus
   spectaculaire, est celui qui se contredit d'un modele a l'autre.

3. **Faut il publier separement le bloc C comme norme d'audit des flux ?** Il n'a pas le meme
   destinataire, pas le meme texte, pas le meme cout, et il est le seul dont le dossier detienne
   deja la mesure complete avec sa borne adverse. Le fusionner avec le bloc A donne un document
   plus complet et un destinataire plus flou.

4. **Que fait on du resultat negatif sur les statistiques de reserve ?** La reponse en trois
   etages a l'objection « vous publiez la cible » est cassee au deuxieme etage : la reserve
   theoriquement elegante est dominee par une statistique deja publiee. Le publier renforce la
   credibilite de la grille et affaiblit son argument de defense. Je penche pour le publier, en
   tete, parce qu'une norme qui cache sa faiblesse ne survit pas a un premier adversaire.
