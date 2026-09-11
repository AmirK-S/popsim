# Brouillon FR pour la section « Ethics Considerations » (PoPETs 2027.3)

Note : `resultats/positionnement-vie-privee-2026-09-12.md` n'existe pas encore au moment de la
rédaction (peut-être en cours par un autre agent). Ce brouillon s'appuie sur `c7-resultats.md`,
`c7-contre-examen-2026-09-11.md` et `c7-mecanisme-resultats.md`. À relire contre ce fichier de
positionnement dès qu'il existe.

**1. Jeu de données.** Twin-2K-500 (Toubia et al., arXiv 2505.17479) est public sous licence
CC BY 4.0. Aucune donnée nouvelle collectée : l'attaque n'utilise que le contenu déjà publié
(réponses humaines et sorties de jumeaux). Aucun consentement supplémentaire nécessaire, mais
limite à noter : les participants n'ont pas consenti spécifiquement à un test de
ré-identification sur les jumeaux générés à partir de leurs réponses.

**2. Aucun individu identifié.** Aucun nom ni identifiant reliant un `pid`/`TWIN_ID` à une
personne réelle n'est publié ou listé. Seuls des taux agrégés sur les 2 058 personnes sont
rapportés (top-1, top-10, intervalles bootstrap) ; aucun cas individuel n'est nommé ni montré.

**3. Absence de préjudice nouveau.** Twin-2K-500 publie déjà, pour chaque personne, ses
identifiants et ses réponses réelles à côté de son jumeau : l'appariement est trivial sans
attaque (`pid` = `TWIN_ID`). Le résultat ne crée pas de préjudice nouveau sur ce jeu précis ; il
documente un risque générique pour quiconque publierait des jumeaux « anonymisés » sans cette
clé, scénario que Twin-2K-500 ne pratique pas (cf. contre-examen, « Modèle de menace »).

**4. Bénéfice pour la communauté.** Plusieurs équipes publient des sorties de jumeaux LLM
individualisées sans analyse de risque de liaison (Ahn et al., Park et al. 2024). Notre mesure
fournit un premier chiffre de ce risque sur un jeu public et une méthode reproductible pour le
tester ailleurs avant publication.

**5. Divulgation responsable.** Prévue auprès des auteurs de Twin-2K-500 avant toute mise en
ligne du code ou du rapport (brouillon dans `divulgation-responsable-brouillon.md`), délai de
réponse 30 jours, offre de partage du code et du rapport en amont.

**6. Publication du code d'attaque, pour et contre.** *Pour* : réplicabilité, permet à d'autres
détenteurs de panels de tester leurs jumeaux avant publication, pratique standard en sécurité
(divulgation puis publication). *Contre* : abaisse le coût pour un attaquant qui possède déjà
les vraies réponses d'un panel tiers et un fichier de jumeaux correspondant. *Arbitrage
proposé* : publier le code, car il n'agit que si l'attaquant détient déjà les réponses réelles
aux mêmes items (rare hors détenteur du panel), et la contre-mesure (agrégation) est simple une
fois le risque connu.

**7. Défenses recommandées.** (a) ne pas publier les sorties de jumeaux item par item pour les
blocs à forte spécificité inter-personnes (ici, les items d'achat en bloc) ; publier des
agrégats ou du bruit calibré ; (b) casser l'alignement personne-jumeau dans les fichiers publics
(ne pas aligner `pid` et `TWIN_ID`) ; (c) publier des jumeaux régénérés, sans copie des
métadonnées de vague (`StartDate`/`EndDate`/`Duration`/`RecordedDate`, relevé dans le
contre-examen) ; (d) documenter un test de liaison minimal avant toute mise en ligne de jumeaux ;
(e) mélange intra-segment (permuter les réponses corrélées entre personnes du même groupe
démographique), qui ramène le top-1 de 20,68 % à 0,13 % au prix de 4,4 points sur les
corrélations entre items (distribution et écarts entre segments exactement préservés) ;
sur ce même indicateur, l'écart aux réponses humaines s'aggrave de 68 % (5,78 → 9,71),
`resultats/c7-defense-resultats.md`.

**8. Cas Park et al. (archive des 1 052 agents génératifs).** Leur matériel supplémentaire
(section « Participant Consent ») avertissait déjà les participants d'une possibilité que
leurs informations (démographie, histoire personnelle, opinions politiques) soient
« inadvertently shared », et reconnaissait qu'« achieving complete anonymity remains
challenging ». Ils avaient donc nommé le risque, obtenu un accord d'éthique travaillé plus de
six mois, pseudonymisé, restreint l'accès aux réponses individuelles et prévu un retrait sur
25 ans. Aucun audit public ne mesurait jusqu'ici l'ampleur de ce risque nommé : nos chiffres
(44,7 % d'identification à partir du seul entretien parmi 1 052, 65,7 % pour le composite,
20,4 % en monde ouvert à 1 % de fausses accusations) en sont la première quantification
connue. Le message aux auteurs doit rester « votre avertissement était exact, voici son
ampleur mesurée », jamais « vous avez eu tort » (cf. lettre 2 de
`divulgation-responsable-brouillon.md`).

**9. Argument d'intérêt public.** Le rapport AAPOR du 8 mai 2026 classe la génération de
réponses synthétiques comme la tâche la plus risquée en vie privée parmi celles qu'il évalue,
et nomme la ré-identification par liaison (sections 6.2.1 et 6.2.4) sans jamais la quantifier.
Combiné à l'absence d'audit public sur l'archive Park et al. (point 8), ce sont les deux
meilleurs arguments d'intérêt public pour publier : un risque déjà nommé par les praticiens et
les organismes professionnels, mais jamais mesuré, justifie une mesure indépendante suivie
d'une divulgation responsable plutôt que le silence.

**Références internes** : `resultats/c7-resultats.md` (résultat principal Twin, critère
préenregistré) ; `resultats/c7-contre-examen-2026-09-11.md` (baselines, modèle de menace,
antériorité) ; `resultats/c7-mecanisme-resultats.md` (signal localisé au bloc d'achat) ;
`resultats/c7-stanford-provenance-resultats.md` (44,7 % / 65,7 %, contamination exclue) ;
`resultats/c7-monde-ouvert-resultats.md` (20,4 % Stanford / 3,0 % Twin en monde ouvert) ;
`resultats/c7-defense-resultats.md` (mélange intra-segment).

## Manque à déclarer : aucune détermination IRB / exemption

Cette section ne comporte, à ce jour, **aucune détermination d'exemption ou d'approbation
éthique pour ce travail lui-même** — seul l'IRB *de Park et al.* (point 8) est mentionné,
pour leur propre collecte, pas pour la présente ré-identification. PoPETs attend une phrase
explicite, avec institution nommée, même pour conclure à une recherche hors du champ
« sujets humains ». Tant que cette détermination n'est pas obtenue et citée ici, c'est un
manque réel à signaler dans le dossier de soumission, distinct de la vérification de licence
menée dans `resultats/licences-sources-verification-2026-09-11.md` (qui porte sur les
conditions d'usage des données, pas sur l'approbation éthique de cette étude).
