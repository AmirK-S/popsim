# Addendum R6 au préenregistrement v2 — plafond et pilotes antérieurs

Cet addendum complète séparément `r6-preenregistrement-v2.md`. Il ne change ni les
hypothèses, ni les familles de tests, ni les seuils, ni les plans F1/F2, ni les règles
d’analyse fixées dans la v2.

La limite totale de la clé OpenRouter réservée à R6 est désormais de **4,40 USD**, sans
renouvellement (`reset: null`), au lieu du plafond expérimental de 4,50 USD prévu dans la
v2. La règle appliquée est la plus restrictive : aucune dépense nouvelle de R6 ne peut
dépasser 4,40 USD sur cette clé, et la réserve de compte de 1,50 USD demeure. Avant chaque
appel payant, le client relit sous verrou la limite et le solde, réserve une borne pour
l’appel, impose un fournisseur sans repli, puis rapproche le coût annoncé et
l’identifiant de l’appel. Toute issue ambiguë bloque la suite.

Avant le dépôt OSF de la v2, quatre essais exploratoires gratuits ont produit 40 lignes :
**29 réponses**, dont le champ de coût annonce 0 USD, et **11 incidents de transport**,
dont le coût par réponse est absent. Les incidents concernent des identifiants `:free` ;
leur borne tarifaire est donc enregistrée séparément à 0 USD d’après le catalogue local.
Cette borne n’est pas présentée comme une preuve de facturation nulle. Le snapshot actuel
de clé (`usage: 0`) ne prouve rien rétroactivement, car aucun identifiant non secret de
l’ancienne clé n’a été trouvé dans les traces.

Le manifeste privé classe les 40 lignes comme `ancien-pilote`. Les vraies passes v2 sont
vides au moment du dépôt. Ces essais ne seront ni comptés comme résultats confirmatoires,
ni renommés en passes v2, ni répétés sous un autre suffixe pour contourner l’historique.
La reprise technique indexe chaque cellule déjà écrite et interdit sa réplication
silencieuse.

R6 transmet uniquement l’invite, des libellés publics du GSS et les modalités publiques
des questions. Aucune réponse individuelle, fiche de personne, microdonnée ou donnée
personnelle ne quitte la machine. Le référent humain reste local et contrôlé par empreinte.
