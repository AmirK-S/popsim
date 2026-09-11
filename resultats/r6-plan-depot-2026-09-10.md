# R6 — texte autonome à déposer sur OSF

Version assemblée le 10 septembre 2026 à partir de `r6-preenregistrement-v2.md` et de
`r6-addendum-osf-2026-09-10.md`, avant toute passe confirmatoire. Les deux sources restent
inchangées. Ce texte fixe le plan applicable au lancement.

## Question, périmètre et données

R6 demande si des modèles servis par API décrivent l’écart entre camps politiques comme
les modèles locaux de R1, R4 et R5 : déplacement par rapport au plancher humain, variété
interne inventée et portrait dépendant de l’identité du demandeur. Il teste aussi si l’effet
des trois exemples observé dans R5 se retrouve dans plusieurs familles de modèles.

Le mode est uniquement descriptif. Chaque requête contient l’invite publique, le libellé
et les modalités publics d’un item du GSS, le camp décrit et l’identité du demandeur ; F2
ajoute les trois exemples publics de R4. Aucune réponse individuelle, fiche de personne,
microdonnée ou donnée personnelle ne quitte la machine. Le référent humain reste local et
son empreinte est contrôlée.

R6 mesure A1, dispersion décrite sur dispersion réelle par camp ; A2 signé, écart entre
camps décrit sur réel sur 79 items orientés, plancher humain 1,009 ; et A4, dépendance au
demandeur, plancher 1,00 par construction. Les modèles ouverts et gratuits sont descriptifs.
Le périmètre confirmatoire des hypothèses est constitué des cinq modèles fermés 7 à 11.

## Modèles, ordre et protocole

Étape 0 : vérification locale de la voie chat sur 40 cellules, avec seuil d’au moins 38
distributions identiques sur 40 entre `/completion` et `/v1/chat/completions`, puis essai du
client sur un modèle `:free`, 10 cellules dans un fichier smoke séparé. Les gratuits prévus sont
`google/gemma-4-31b-it:free`, `nvidia/nemotron-3-super-120b-a12b:free` et
`nvidia/nemotron-3-ultra-550b-a55b:free`. Chacun reçoit 1 210 cellules F1+F2, à 20 requêtes
par minute et dans la limite annoncée de 1 000 requêtes par jour ; le plan prévoit donc
environ deux jours par gratuit si cette limite est globale au compte.

Étape 1, ouverts payants dans cet ordre : `deepseek/deepseek-v4-flash`,
`mistralai/mistral-small-2603`, `meta-llama/llama-4-maverick`, `qwen/qwen3.7-plus`,
`moonshotai/kimi-k2.5`, `z-ai/glm-5`. Étape 2, fermés économiques :
`openai/gpt-5.6-luna`, `google/gemini-3.8-flash`, `anthropic/claude-haiku-4.5`,
`x-ai/grok-4.3`. Étape 3 : `openai/gpt-5.4`; `anthropic/claude-sonnet-5` n’entre que si
la dépense réelle le permet selon la règle budgétaire préenregistrée. Après abaissement de
la limite totale à 4,40 USD, Sonnet n’entre que si l’usage R6 observé plus sa borne projetée
reste au plus à 4,40 USD : avec sa ligne v2 de 1,03 USD, l’usage doit être au plus de
**3,37 USD** avant son lancement. La borne courante vérifiée avant chaque appel prévaut.

Chaque cellule utilise un texte à température 0, un appel, `max_tokens=150`, le parse strict
de R1, aucune séquence d’arrêt ajoutée et aucune relance après échec de parse. Le raisonnement
est réglé au minimum offert et inscrit au registre. Le fournisseur aval est imposé sans
repli et enregistré avec l’identifiant et la date.

F1 est le gabarit seul, invite R1 au caractère près : 149 items × 3 camps × 2 identités,
soit 894 cellules. F2 ajoute les trois exemples de R4 comme dans R5 : 79 items orientés ×
2 camps (gauche, droite) × 2 identités, soit 316 cellules. Chaque payant ajoute 40 cellules
F1 rejouées pour le plancher machine et un essai de 10 cellules F1 envoyé deux fois. Total :
1 270 appels par modèle. A4 n’est lisible que si la distance entre identités dépasse deux
fois la distance moyenne entre les deux passes du plancher machine.

## Hypothèses et familles confirmatoires

**H1, dispersion intermodèles.** Sur A2 signé, identité journaliste, parmi les cinq fermés,
le rapport maximum/minimum est au moins 2 et les intervalles extrêmes sont disjoints, ou un
intervalle est entièrement sous 1,009 et un autre entièrement au-dessus. Un test. Pari :
vraie. La v2 ne définit ni statistique nulle ni p pour cette règle composée après classement
des cinq modèles. H1 est donc une **règle décisionnelle confirmatoire unique, sans p** ; aucun
p ne sera inventé après observation. La correction de Holm est sans objet pour cette règle
unique.

**H2, identité du demandeur.** Pour chacun des cinq fermés et chacun des camps gauche et
droite, la borne basse de A4 est supérieure à 2 et la distance entre identités dépasse deux
fois le plancher machine. Dix tests. Pari : vraie sur au moins quatre modèles sur cinq.

**H3, format.** Contraste apparié F2−F1 sur A2 signé, 79 items, identité journaliste, par
modèle fermé, bootstrap sur les items et permutation de signe appariée. H3a : contraste
positif avec intervalle excluant zéro sur au moins trois fermés sur cinq ; pari vrai. H3b :
contraste au moins égal à +0,30 sur au moins trois fermés sur cinq ; pari faux. Cinq tests
pour H3a et cinq pour H3b. Pour rendre ces dix tests exécutables, notons
`C = mean(d_F2 - d_F1) / mean(r)`. H3a centre la permutation sur zéro et change par item le
signe de `d_F2 - d_F1`. H3b centre la permutation sur +0,30 et change le signe de
`d_F2 - d_F1 - 0,30 r`. Les permutations sont bilatérales, 20 000 tirages, avec estimateur
de Phipson–Smyth ; le bootstrap rééchantillonne les triplets appariés `(d_F2, d_F1, r)`.
Une hypothèse élémentaire est retenue seulement dans la direction annoncée et si son p
survit à Holm dans F3 ; les intervalles correspondants sont rapportés.

**H4, palier dans une famille.** Pour `gpt-5.4` contre `gpt-5.6-luna`, et pour
`claude-sonnet-5` contre `claude-haiku-4.5` si le modèle conditionnel est joué, le palier
supérieur est plus proche de 1,009 sur A2 signé : contraste apparié sur la distance absolue
au plancher, intervalle excluant zéro. Un ou deux tests. Pari faux. Avec une seule paire,
H4 est déclaré « un test, non généralisable ».

Holm est appliqué séparément, au seuil 0,05 : F1 contient la règle unique sans p de H1 et
n’appelle pas de correction ; F2 contient les dix tests de H2 ; F3 les cinq tests H3a et les
cinq H3b réunis ; F4 les un ou deux tests de H4.
Il n’y a jamais de correction entre familles et aucun autre test confirmatoire. Les ouverts
et gratuits se lisent sans p.

Prédiction annexe, hors familles : chez les fermés, le taux de rejet de première tentative
est inférieur à 1 % sous les deux formats et aucun rejet ne touche un item à deux ou trois
modalités. Sinon le modèle est marqué « format non tenu ».

## Vérifications et critères d’arrêt

Pour chaque payant, l’essai de dix cellules envoyé deux fois applique exactement ces règles :

- projection sur 1 270 cellules supérieure à 1,5 fois sa ligne v2 : une seule correction,
  raisonnement au minimum, puis nouvel essai ; second dépassement, retrait du modèle ;
- moyenne de jetons de raisonnement supérieure à 50 : même correction puis retrait ;
- plus de deux rejets de parse sur dix : retrait, sans reformulation de l’invite ;
- moins de sept distributions identiques sur dix entre passes : modèle marqué non
  déterministe, A4 lisible seulement avec le plancher machine ;
- plus de trois erreurs 429 sur vingt appels : attente d’une heure puis reprise, sans
  seconde clé.

Les critères hérités 1 à 7 restent vérifiés par modèle : (1) plus de 25 % de rejets de
format « après relance » rend la voie non praticable ; R6 n’ayant aucune relance, il publie
le taux de première tentative ; (2) la recopie de l’exemple de relance retire les cellules
concernées, mais ce critère est sans objet ici puisqu’il n’y a aucune relance ;
(3) une distribution constante d’un camp à l’autre dans plus de 90 % des items invalide
H1 et H2 ; (4) le facteur humain vague 2/vague 1 doit rester dans [0,85 ; 1,15] ; (5) les
distributions réelles doivent se recalculer à l’identique et les effectifs retomber sur
417, 303 et 332 ; (6) l’empreinte SHA-256 du référent doit rester
`ea7cd93e8eb3b34d279171ac9a202a0451554afc3d34c7a142dfce761391c811` ; (7) plus d’un
`llama-server` simultané jette le run local,
contrôle sans objet pour les appels API distants. Aucun critère applicable n’est omis.

L’évaluation utilise le même évaluateur que R1, R4 et R5, les mêmes 79 items orientés et
149 items A1/A4, 2 000 tirages bootstrap, 20 000 permutations de signe appariées et
l’estimateur de Phipson–Smyth. La référence de format reste le lambda R5, 0,79
[0,60 ; 0,97], sans recalcul.

## Coût, historique et différences avec les sources

La v2 fixait un plafond expérimental toutes lignes de 4,50 USD et une réserve de compte de
1,50 USD. Depuis, la clé R6 a une limite totale plus restrictive de **4,40 USD**, sans reset,
avec usage actuel 0. La limite 4,40 gouverne donc toute dépense nouvelle ; la réserve 1,50
reste intacte. Avant chaque appel payant, le client relit sous verrou la clé et le solde,
réserve la borne du dernier appel, puis rapproche coût et identifiant. Toute issue ambiguë
bloque la suite.

Les sorties publiques contiennent uniquement le plan, les identifiants publics des modèles,
le fournisseur aval, la date, les dénominateurs, rejets, coûts agrégés, estimations et
intervalles. La clé API, les en-têtes d’autorisation, identifiants de compte et de requête,
soldes détaillés, fichiers de verrou, manifeste privé, traces brutes et captures non expurgées
restent locaux et ne sont jamais déposés. Une preuve de réglage éventuellement jointe est
expurgée de tout identifiant ou secret avant publication.

Avant ce dépôt, quatre pilotes gratuits exploratoires ont produit 29 réponses au coût
annoncé confirmé de 0 USD et 11 incidents dont le coût observé est inconnu. Leur borne
tarifaire distincte est 0 USD, car les modèles sont `:free` dans le catalogue local ; cette
borne n’est pas une preuve de facturation nulle. Aucun identifiant non secret ne relie
l’ancienne clé au snapshot actuel. Le manifeste privé classe les 40 lignes
`ancien-pilote`; les vraies passes v2 sont vides. Ces lignes ne deviennent pas des résultats
confirmatoires et ne sont pas rejouées sous un autre suffixe.

Les différences entre ce texte assemblé et le rapport v2 original sont donc : limite
opérationnelle abaissée de 4,50 à 4,40 USD et seuil conditionnel Sonnet recalé à 3,37 USD ;
documentation séparée des 29 réponses et 11 incidents exploratoires ; registre global,
borne par appel et fournisseur sans repli rendus exécutoires ; H1 explicitée comme règle
confirmatoire sans p et les p de seuil H3b définis avant observation. Les hypothèses
substantielles, seuils, plans et règles d’interprétation de la v2 restent inchangés.

R6 décrit la réponse du modèle et du fournisseur nommés à cette invite. Il ne mesure ni
l’application grand public, ni la température de service, ni des personnes, ni la
contamination, ni un effet causal, ni une autre langue ou un autre pays, ni la direction de
A4. H4 porte sur un palier tarifaire, pas sur une taille non publiée. Une ligne ne vaut que
pour l’identifiant, le fournisseur et la date enregistrés.
