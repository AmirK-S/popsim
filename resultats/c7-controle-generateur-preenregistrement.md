# C7, controle generateur banal : preenregistrement (13 septembre 2026)

statut: courant
mandat: Un generateur synthetique banal, sans IA, ajuste sur les memes humains, fuit-il autant qu'un jumeau LLM ?
agent: Opus 5, Anthropic
ecriture: analyses/c7_controle_generateur.py, resultats/c7-controle-generateur-preenregistrement.md, resultats/c7-controle-generateur-resultats.md, resultats/c7-controle-generateur.csv
lecture_seule: tout le reste
interdits: appel payant sans GO, reseau, commit sur master, arriere-plan
cout_reel_usd: 0

**Ecrit avant tout calcul, avant la premiere ligne de `analyses/c7_controle_generateur.py`.**

## 0. La question, et ce qu'elle peut couter

L'article affirme que les jumeaux numeriques produits par un LLM laissent fuiter l'identite
des repondants dont ils sont issus (Twin : top-1 20,6 % ; Park et al./GSS : top-1 65,6 %,
TPR@FPR=1 % 60,17 % pour l'attaquant fort). **Rien dans le protocole actuel ne demontre que le
LLM y est pour quelque chose.** Si un generateur de donnees synthetiques banal, sans aucune IA,
ajuste sur les memes humains, reproduit le meme taux, le resultat n'est pas un resultat sur les
LLM : c'est une redecouverte de la fuite des donnees synthetiques (Narayanan-Shmatikov 2008 et
la litterature *synthetic data release*). Si au contraire le jumeau LLM fuit nettement plus, le
resultat est specifiquement un resultat sur les LLM, et plus fort que ce qui est ecrit.

`c7_generateur.py` (G-LR, G-copule) ne tranche pas cette question : ses generateurs ne
conditionnent **jamais** sur les reponses cibles, plafonnent a 0,476 d'exactitude et ne sont
donc pas « le generateur qu'utiliserait un praticien » sur ces memes donnees. `c7_synth_ajuste.py`
(donneur 1-PPV) est un comparateur de plafond a information inegale. Il manque l'echelle de
memorisation, qui est le coeur de ce livrable.

## 1. Bassin : strictement identique, aucune exception

Piege qui a deja coute deux erreurs a ce projet : le top-1 depend mecaniquement de la taille du
bassin. Ici, **le bassin de candidats et l'ensemble des personnes attaquees sont, pour chaque
generateur, exactement ceux du jumeau LLM**, sans une personne ni un item de difference :

- **Twin-2K-500** : 2 058 personnes attaquees, 2 058 candidats (humains vague 4), les 60 items
  toujours renseignes de `c7_reidentification.items_communs`. Hasard = 1/2 058 = 0,0486 %.
- **Park et al. / GSS (archive Stanford)** : 1 052 personnes, 1 052 candidats (humains vague 1),
  les 177 items categoriels de `c7_stanford.charger_domaine("gss")`. Hasard = 0,0951 %.

Chaque generateur produit **une ligne par personne reelle**, alignee ligne a ligne comme le
jumeau LLM : la ligne i est le profil synthetique attribue a la personne i, et c'est cette
personne i qui est la « vraie » reponse de l'attaque. Meme convention que le jumeau, sinon rien
n'est comparable.

## 2. Les quatre generateurs (aucune IA, aucun appel reseau)

Tous ajustes sur les memes donnees humaines (le bloc cible lui-meme), tous produisant le meme
nombre de profils que le jumeau.

- **G0, marginales independantes.** Chaque item tire selon sa distribution empirique observee
  dans la population entiere, sans aucun lien entre items et sans aucun conditionnement sur la
  personne. C'est le plancher : il ne doit presque rien fuiter.
- **G1, marginales conditionnees au segment demographique.** Meme tirage, mais dans la
  distribution observee a l'interieur du segment de la personne. Twin : `S_gra` (40 segments,
  taille mediane 23). Stanford : genre x race x tranche d'age (42 cellules). **Repli declare** :
  une cellule de moins de 10 personnes retombe sur la marginale globale de l'item. C'est le
  generateur qu'utiliserait n'importe quel praticien, et le comparateur le plus honnete.
- **G2, Chow-Liu global.** Arbre couvrant de poids maximal sur l'information mutuelle par paires
  d'items, estimee sur la population entiere ; echantillonnage ancestral (marginale a la racine,
  conditionnelles le long des aretes). Capture les liens entre items, sans conditionnement sur
  la personne. Code ici en une centaine de lignes (`synthpop`, `copulas`, `sdv`, `ctgan` absents
  du venv ; **rien n'est installe**).
- **G3, Chow-Liu par segment.** Meme modele, ajuste a l'interieur du segment de la personne.
  **Repli declare** : un segment de moins de 30 personnes retombe sur l'arbre global. C'est le
  plus fort des comparateurs non memorisants.
- **G4(eps), copie perturbee — le cas decisif.** Le profil i est le vrai vecteur de la personne
  i, dont chaque item est remplace, independamment et avec probabilite eps, par un tirage dans
  la marginale globale de cet item. eps = 0 est la copie litterale ; eps = 1 redonne G0 en
  esperance. Grille : eps de 0 a 1 par pas de 0,05 (21 points). **Ce n'est pas un generateur
  qu'on proposerait a quiconque : c'est l'etalon du haut**, qui dit combien de fuite correspond
  a quel degre de memorisation.

## 3. Attaque, mesures, reductions declarees

L'attaque n'est pas reimplementee : `c7_reidentification.rangs_attaque` est importee telle
quelle (20 tirages de depart d'ex aequo, ordre des candidats melange). Le monde ouvert reprend
`c7_monde_ouvert.marges_deux_regimes` et `c7_monde_ouvert.roc_et_taux` sans modification (marge
top-1 moins top-2, regime « personne retiree du bassin » par simple masquage de sa colonne).
IC a 95 % par `a2_commun.bootstrap_personnes`, 2 000 reechantillonnages **de personnes**.

Mesures rapportees pour chaque generateur : exactitude par personne sur les items de l'attaque,
top-1 et top-10 en monde ferme, AUC / TPR@FPR=0,1 % / TPR@FPR=1 % en monde ouvert, tous avec IC.

**Reductions declarees** (budget local, aucun appel paye) : 5 tirages de generation par
generateur stochastique (moyennes par personne avant bootstrap), 5 tirages d'ex aequo pour le
monde ouvert comme dans `c7_monde_ouvert.py`, grille eps au pas de 0,05 et non continue. Graine
fixee a 20260913, declinee par nom de generateur via `c7_reidentification.graine_nom`.
`analyses/c7_controle_interpretabilite.py` est applique a chaque generateur **avant toute
interpretation** : un generateur qui echoue au controle est declare comme ne transportant
aucune information individuelle demontrable sur ce bassin, et c'est exactement l'issue attendue
pour G0 a G2. Aucune donnee individuelle, aucun pid, aucun appariement n'est imprime ni ecrit.

## 4. Classement attendu [HYPOTHESE]

`hasard ~ G0 < G1 < G2 <~ G3 << jumeau LLM << G4(eps petit)`.

Chiffres preenregistres. Twin : G0 <= 0,2 %, G1 <= 1 %, G2 <= 1 %, G3 <= 2 %, contre 20,6 %
pour JSON Persona GPT4.1. Stanford : G0 a G3 <= 5 %, contre 65,6 % pour l'agent composite.
G4(0) = 100 % par construction ; G4 decroissant en eps.

## 5. Ce qui me ferait conclure que le jumeau LLM n'a rien de particulier

Soit **M** le meilleur top-1 parmi G0, G1, G2, G3 (les generateurs **non memorisants** ; G4 est
exclu de ce calcul, il memorise par construction) et **L** le top-1 du jumeau LLM, sur le bassin
strictement identique. Seuils fixes ici, avant de voir M :

- **Non specifique aux LLM** si `M >= 0,5 x L`, **ou** si les IC a 95 % de M et de L se
  chevauchent. Twin : M >= 10,3 %. Stanford : M >= 32,8 %. Dans ce cas l'article perd sa
  nouveaute, le titre doit etre reecrit, et la phrase du point 7 doit etre publiee telle quelle.
- **Affaibli** si `0,2 x L <= M < 0,5 x L` (Twin : 4,1 % a 10,3 %). L'effet LLM existe mais est
  bien plus petit qu'annonce ; le titre doit etre qualifie et l'ecart chiffre en premiere page.
- **Specifique aux LLM** si `M < 0,2 x L` **et** borne haute de l'IC de M < borne basse de l'IC
  de L (meme regle que `c7_controle_interpretabilite`).

La meme regle, avec les memes seuils relatifs, est appliquee en monde ouvert sur TPR@FPR=1 %.

## 6. Ou se situe le jumeau LLM sur l'echelle de memorisation

Deux lectures de la courbe G4(eps), a comparer l'une a l'autre :

- `eps*_fuite` : la valeur de eps ou le top-1 de G4 egale celui du jumeau LLM (interpolation
  lineaire sur la grille mesuree).
- `eps*_exactitude` : la valeur de eps ou l'exactitude de G4 egale celle du jumeau LLM.

Verdict preenregistre, tolerance +-0,10 :

- `eps*_fuite ~ eps*_exactitude` : le jumeau se comporte **comme un modele qui recopie**. Sa
  fuite est exactement celle qu'implique mecaniquement son exactitude, ni plus ni moins.
- `eps*_fuite > eps*_exactitude + 0,10` : le jumeau fuit **moins** qu'un copieur de meme
  exactitude. Il **generalise** plus qu'il ne recopie ; la fuite est un sous-produit de
  l'exactitude et non d'une memorisation.
- `eps*_fuite < eps*_exactitude - 0,10` : le jumeau fuit **plus** qu'un copieur de meme
  exactitude. Memorisation au-dela de ce que l'exactitude explique : c'est la forme la plus
  forte de la these de l'article.

[HYPOTHESE] Prediction : `eps*_fuite > eps*_exactitude`, le jumeau fuit moins qu'un copieur de
meme exactitude.

## 7. La phrase a publier si le verdict tombe contre nous

Si `M >= 0,5 x L`, l'article doit ecrire, sans attenuation :

> Le taux de re-identification que nous mesurons sur des jumeaux produits par un LLM est
> atteint aussi par un generateur synthetique classique ajuste sur les memes donnees, sans
> aucun modele de langage. Notre resultat n'est donc pas un resultat sur les LLM : il
> redecouvre, sur un nouveau support, la fuite des donnees synthetiques deja etablie par la
> litterature de *synthetic data release*.

Ce verdict est rendu meme s'il demolit l'article. Ce projet a retire cinq conclusions en deux
jours, dont quatre qui l'arrangeaient.
