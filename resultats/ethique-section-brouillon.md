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
contre-examen) ; (d) documenter un test de liaison minimal avant toute mise en ligne de jumeaux.

**Références internes** : `resultats/c7-resultats.md` (résultat principal, critère
préenregistré) ; `resultats/c7-contre-examen-2026-09-11.md` (baselines, modèle de menace,
antériorité) ; `resultats/c7-mecanisme-resultats.md` (signal localisé au bloc d'achat).
