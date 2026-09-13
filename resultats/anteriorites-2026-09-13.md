# Antériorités T2 — vérification à la source et requalification des contributions touchées

statut: courant
mandat: Tâche T2 du plan de révision du 13/09 (`resultats/plan-revision-2026-09-13.md`) : vérifier à la source, indépendamment du rapport de relecture positionnement, les trois antériorités qu'il reproche (Narayanan-Shmatikov 2008, logique de contrôle Anonymeter §4.2, Jordon et al. 2022 p.72) ; créer les entrées bibliographiques manquantes (Carlini et al. ICLR 2023, TAPAS) ; documenter pour l'agent qui corrigera le manuscrit ce qui revient à chaque antériorité et ce qui reste nôtre, avec la formulation exacte à employer.
agent: agent biblio/antériorités (sous-agent, branche `agent/biblio/anteriorites`)
ecriture: `article/references.bib`, `article/references-verification.md`, `resultats/anteriorites-2026-09-13.md` uniquement
lecture_seule: `article/manuscrit.md` (deux autres agents travaillent en parallèle sur les mesures) ; tout le reste du dépôt
interdits: git commit ; fusion de branche ; tout appel de modèle payant ; toute écriture hors des trois fichiers ci-dessus ; toute modification du manuscrit
cecite: PDF/textes lus intégralement dans cette passe : Narayanan-Shmatikov 2008 (arXiv:cs/0610105, texte intégral, via extraction déjà présente dans le scratchpad de session, produite par un agent antérieur à partir du PDF original — relue et recitée indépendamment ici), Anonymeter/Giomi et al. 2023 (texte intégral, même provenance), Jordon et al. 2022 (texte intégral, même provenance), Gouweleeuw et al. 1998 (2 premières pages du PDF scb.se, récupérées et lues dans cette passe). Carlini et al. 2023 (ICLR) et TAPAS : résumé intégral + métadonnées de venue (page d'abstract arXiv + recherche web croisée pour confirmer la venue), **pas le corps de l'article** — voir réserve explicite plus bas. Les trois travaux de 2026 relevés par la relecture positionnement (Li 2601.05918 ; Li, Wen & Li 2605.30848 ; Xiang et al. 2608.03700) n'ont pas été lus dans cette passe et ne sont donc pas ajoutés au `.bib`, conformément à la règle « ne pas citer ce qu'on n'a pas lu ».
cout_reel_usd: 0.00

## Verdict en une phrase

Les trois antériorités reprochées par la relecture positionnement **tiennent toutes les trois**, vérifiées indépendamment à la source (texte intégral, pas seulement le rapport) ; les deux références manquantes (Carlini et al. ICLR 2023, TAPAS) ont été créées avec des métadonnées vérifiées ; aucune référence n'a été ajoutée sur la seule foi d'un résumé de tiers.

---

## 1. Les trois antériorités, vérifiées indépendamment

### 1.1 Narayanan & Shmatikov 2008 — pondération par rareté + monde ouvert par excentricité `[TIENT]`

**Source.** IEEE S&P 2008, *Robust De-anonymization of Large Sparse Datasets*, doi 10.1109/SP.2008.33 ; préprint arXiv:cs/0610105 (texte intégral relu, §4 et §5). URL : https://arxiv.org/abs/cs/0610105

**Preuve, verbatim, retrouvée indépendamment dans le texte intégral (pas seulement recopiée du rapport) :**
- « Score(aux,r′) = Σ_{i∈supp(aux)} wt(i)·Sim(aux_i,r′_i) where wt(i) = 1/log|supp(i)|. » (§4)
- « If (max−max2)/σ < φ, where φ is a fixed parameter called the eccentricity, then there is no match; otherwise, the matching set consists of the record with the highest score. » (§4)
- « The eccentricity parameter was set to φ = 1.5 [...] (A constant value of the eccentricity does not always give the equal error rate, but it is a close enough approximation.) » (§5)

**Verdict : tient sans réserve.** La pondération par rareté (wt(i)=1/log|supp(i)|) et le critère de monde ouvert par excentricité, calibré comme approximation du taux d'égale erreur, sont bien de Narayanan-Shmatikov 2008. Le manuscrit ne peut pas revendiquer ces deux éléments de méthode comme contribution (5) sans attribution — il les cite déjà ([26]) mais uniquement pour le résultat Netflix.

**Ce qui reste nôtre.** L'application à des vecteurs de réponses catégorielles issus de jumeaux LLM, l'estimation des poids hors-échantillon (out-of-fold, 5 replis), l'objet (archive Park, bassin, plafond humain).

**Contribution touchée : (5).** Formulation exacte à substituer à la phrase actuelle de la contribution (5) :

> « We instantiate the Narayanan–Shmatikov score (wt(i) = 1/log|supp(i)|) and their out-of-sample matching criterion [26] on categorical answer vectors, estimating the weights out-of-fold over 5 folds. The method is theirs; the object, the pool and the human ceiling are new. »

Rien à supprimer : requalifier une revendication de méthode en revendication d'instanciation. La contribution reste, sous un autre nom.

### 1.2 Anonymeter, Giomi et al. 2023 — logique de contrôle main/naive/control `[TIENT]`

**Source.** *A Unified Framework for Quantifying Privacy Risk in Synthetic Data*, PoPETs 2023(2):312–328, doi 10.56553/popets-2023-0055. URL du PDF officiel : https://petsymposium.org/popets/2023/popets-2023-0055.pdf

**Preuve, verbatim, retrouvée indépendamment dans le texte intégral, §4.2 « Framework Architecture », p. 315 :**
- « the attack phase consists of executing three different attacks. First, the "main" privacy attack in which the attacker uses the synthetic dataset X_syn to deduce private information of records in the training set X_train. Second, a "naive" attack is carried out based on random guessing, to provide a baseline against which the strength of the "main" attack can be compared. Finally, to distinguish the concrete privacy risks of the original data records [...] from general risks intrinsic to the whole population [...] a third "control" attack is conducted on a set of control records from X_control. »
- Complément (p. 315, 320) : « Anonymeter incorporates sanity checks ensuring that the risk estimate is based on attack models that are actually effective » ; « it eliminates any possible ambiguity in the interpretation of the measured risks. »

**Verdict : tient.** C'est bien, mot pour mot, le triptyque main/naive/control que le manuscrit reformule comme contrôle d'interprétabilité en contribution (2), sans l'attribuer à Anonymeter — alors que `giomi2023unified` est déjà en bibliographie et cité ailleurs dans le manuscrit.

**Ce qui reste nôtre, et qui est réel.** La règle du manuscrit **n'est pas identique** : c'est un seuil d'arrêt *avant dépense* (aucun bras expérimental n'est jugé interprétable tant qu'il ne bat pas une baseline démographique contre les humains réels), et non une soustraction a posteriori comme chez Anonymeter (qui exécute les trois attaques puis soustrait). C'est une différence de discipline opérationnelle, pas seulement de vocabulaire — à garder impérativement dans la reformulation.

**Contribution touchée : (2).** Formulation exacte à substituer à la phrase actuelle de la contribution (2) :

> « Our control is the pre-spend, gating form of the baseline discipline Anonymeter builds into its risk estimate [18] and that blind baselines demand of membership attacks [8, 42]. What is new is that it is a stop rule applied before the first paid arm — and what we report is what it cost us. »

**Garde-fou.** Ne pas rétrograder ni supprimer la contribution (2) : ajouter l'attribution, garder la différence (seuil d'arrêt avant dépense vs soustraction a posteriori). Correction d'une phrase, pas d'un paragraphe.

### 1.3 Jordon et al. 2022 — le scénario « deux organisations » comme problème ouvert `[TIENT]`

**Source.** *Synthetic Data — what, why and how?*, commissionné par la Royal Society (2022), arXiv:2205.03257. URL : https://arxiv.org/abs/2205.03257 (également disponible : https://royalsociety.org/-/media/policy/projects/privacy-enhancing-technologies/Synthetic_Data_Survey-24.pdf)

**Preuve, verbatim, retrouvée indépendamment dans le texte intégral, §2.1.2 « Data Linking » :**
- « If these datasets were synthesised independently, the 1-1 match between datasets will be broken; if, in the future, someone wished to pull together these synthetic datasets to investigate the correlations between, say, genetic data and lab test results, they would not be able to do so effectively. »
- « In these situations, there is a need to be able to link two independently generated synthetic datasets (given access to real data) in a minimally privacy-leaking way. »

**Verdict : tient.** Le scénario exact du canal jumeau-à-jumeau du manuscrit — lier deux jeux synthétiques générés indépendamment, l'attaquant ayant accès aux données réelles — est nommé comme problème ouvert par Jordon et al. 2022. La phrase du manuscrit, §3/T2, « This threat model has no direct precedent in the synthetic-data literature », est donc fausse telle qu'écrite.

**Ce qui reste nôtre.** Jordon et al. posent le problème sans le mesurer ; personne, à notre connaissance après cette vérification, ne l'a mesuré. C'est un atout, pas une charge : le manuscrit comble exactement le vide que Jordon et al. signalent.

**Contribution touchée : §3/T2 (modèle de menace), pas une contribution numérotée.** Formulation exacte à insérer :

> « named as an open problem [Jordon et al., 2022] and covered by the A29WP definition [18], but never measured. »

**Garde-fou explicite.** Ne pas toucher à la phrase juste, immédiatement adjacente dans le même §3/T2 : « Anonymeter's linkability presumes real attribute values in hand [18] » — exacte au mot près (vérifiée séparément, voir Anonymeter §5.2/§6.3 dans le rapport de relecture), à garder telle quelle.

---

## 2. Entrées créées dans `article/references.bib` (Bloc E, 3 entrées)

| Clé | Type | Vérifié via |
|---|---|---|
| `jordon2022synthetic` | `@techreport` | Texte intégral (arXiv:2205.03257) |
| `carlini2023quantifying` | `@inproceedings` (ICLR 2023) | Résumé intégral (arXiv:2202.07646) + venue confirmée par recherche croisée (dblp/conf/iclr/CarliniIJLTZ23, page ICLR 2023 oral/poster) |
| `houssiau2022tapas` | `@inproceedings` (NeurIPS 2022 SyntheticData4ML) | Résumé intégral (arXiv:2211.06550) + venue confirmée par recherche croisée (ML Anthology, dépôt GitHub alan-turing-institute/tapas) |

`gouweleeuw1998pram` (déjà existante, Bloc B) : champ `url=` ajouté (https://www.scb.se/contentassets/ca21efb41fee47d293bbee5bf7be7fb3/post-randomisation-for-statistical-disclosure-control-theory-and-implementation.pdf), vérifié en relisant les 2 premières pages du PDF (titre, auteurs, revue, description du PRAM confirmés). Aucune note interne francophone trouvée dans le `.bib` actuel — déjà retirée avant cette passe.

**Validité syntaxique.** Compilation `bibtex` réelle (style `plain`, citation `*`) : 0 erreur, seuls les 12 avertissements préexistants « empty journal » (entrées arXiv-only non touchées). 444 accolades ouvrantes / 444 fermantes. 50 clés, aucun doublon (vérifié par script).

**Réserve explicite sur Carlini et al. 2023 et TAPAS.** Vérifiés au résumé intégral et aux métadonnées de venue, **pas au corps de l'article**. Suffisant pour les métadonnées bibliographiques et pour la formulation de citation ci-dessous (qui ne dépasse pas ce que dit leur résumé) ; **insuffisant pour toute affirmation plus fine** (chiffres précis, méthode de mesure). Formulation à employer en prose (§2.1 et §2.3 du manuscrit, hors de mon périmètre d'écriture) :

> Citer Carlini et al. [ICLR 2023] comme antécédent direct de la relation log-linéaire entre mémorisation et capacité du modèle (« memorization increases significantly with model capacity »), et le mentionner une seconde fois en contraste au §5.5 : l'ablation par permutation de l'article (qui détruit le signal) est l'argument que ce canal n'est pas de la régurgitation littérale au sens de Carlini et al.
> Citer TAPAS [Houssiau et al., NeurIPS 2022 SyntheticData4ML] au §2.1 comme l'autre cadre standard du corpus d'évaluation de la vie privée des données synthétiques (à côté de Stadler, Giomi, Annamalai, Ganev, Yao, Meeus, Golob déjà cités), sans lui attribuer de résultat chiffré au-delà de « toolbox de formalisation de la connaissance de l'attaquant et des baselines ».

**Trois travaux de 2026 volontairement absents.** Li 2601.05918, Li-Wen-Li 2605.30848, Xiang et al. 2608.03700 : la relecture positionnement elle-même les type `[PROBABLE sur la portée exacte]` (résumés seulement), et le plan de révision les place sous une décision du responsable non tranchée (D5). Cette passe ne les a pas lus intégralement non plus ; ils restent donc hors bibliographie. Ce n'est pas un oubli : c'est l'application de la règle « ne pas citer ce qu'on n'a pas lu ».

---

## 3. État réel de `article/references-verification.md` après cette passe

| Bloc | Entrées | État |
|---|---|---|
| A | 27 | Non auditables (vérification antérieure sans trace) — inchangé |
| B | 18 | Vérifiées à la source (passe du 11-12/09) — inchangé |
| C | 1 | Vérifiée à la source (12/09) — inchangé |
| D | 1 | Vérifiée à la source (12/09) — inchangé |
| **E (nouveau)** | **3** | **Vérifiées à la source le 13/09 (1 en texte intégral, 2 en résumé + métadonnées)** |
| **Total** | **50** | **23 entrées auditables sur 50** (contre 20 sur 47 avant cette passe) |

Formulation à substituer partout où « 47 entrées, 20 auditables » apparaît (y compris dans la phrase que la tâche T5 doit déplacer vers *Open Science*, R7 du plan de révision) :

> Of the 50 entries in `article/references.bib`, 23 were checked directly against their primary source in this project; the remaining 27 carry over an earlier verification whose working notes were lost before this project's records began and could not be re-audited here.

---

## 4. Résumé pour l'agent qui corrigera le manuscrit (T3)

| Contribution | Ce qui est nôtre | Ce qui revient à l'antériorité | Formulation exacte |
|---|---|---|---|
| (2) contrôle d'interprétabilité | Seuil d'arrêt **avant dépense**, adossé à une baseline démographique contre les humains réels ; ce que ça a coûté | Le triptyque main/naive/control est celui d'Anonymeter §4.2 (Giomi et al. 2023) | Voir §1.2 ci-dessus |
| (5) attaque forte A-LLR | L'objet (vecteurs de réponses catégorielles de jumeaux LLM), le bassin, le plafond humain, l'estimation hors-échantillon en 5 replis | La pondération par rareté et le critère de monde ouvert par excentricité sont de Narayanan-Shmatikov 2008 | Voir §1.1 ci-dessus |
| §3/T2 modèle de menace | La mesure elle-même (personne ne l'a fait) | Le scénario est nommé comme problème ouvert par Jordon et al. 2022 ; « no direct precedent » est faux | Voir §1.3 ci-dessus |

Aucune des trois contributions ne doit être supprimée : appliquer une méthode connue (ou mesurer un problème déjà nommé) à un objet nouveau reste une contribution, à condition de le dire.
