# Textes prêts à coller — AI Use et repositionnement IRB (2026-09-12)

Ce fichier est le seul que j'ai le droit d'écrire. `article/manuscrit.md` reste en lecture
seule ; l'insertion dans le manuscrit est à faire par l'orchestrateur, en une passe unique.
Les deux blocs ci-dessous sont en anglais, autonomes, prêts à être collés tels quels.

---

## Texte 1 — nouvelle section « AI Use »

**Où l'insérer** : nouvelle section, immédiatement après la fin du §9 Availability (après la
ligne 1035 « …No network dependency. », donc après le séparateur `---` de la ligne 1036) et
avant `## References` (ligne 1038). C'est un ajout pur, rien à supprimer : le manuscrit ne
contient aujourd'hui aucune section « AI use » (`grep -i "ai use"` sans résultat, confirmé par
`resultats/conformite-popets-2026-09-12.md`, point 3). Numéroter en cohérence avec le reste
(`## 10. AI Use` si §8/§9 restent numérotés ; sinon reprendre l'intitulé exact du gabarit
LaTeX 2027 une fois consulté — non accessible en lecture seule, cf. le rapport de conformité).

**Intitulé exact attendu** : la politique (crysp.petsymposium.org/authors-2027.php, vérifiée
en direct pour cette tâche) cite les « three mandatory sections per the 2027 template (ethical
considerations, open science, and AI use) » — d'où l'intitulé retenu, `AI Use`, au même style
de casse que les sections existantes (`Ethical Considerations`, `Availability`).

Texte à coller :

```
## 10. AI Use

Large-language-model-based agents were used throughout this project: they wrote the analysis
code, ran the experiments, drafted this manuscript, and conducted adversarial review of both
the code and the text. We state this in full rather than narrowly, because an account that
understated that involvement would mislead a reader more than a plain one.

The responsible investigator directed the work throughout: set the research questions and the
falsifiable predictions in advance of each analysis, decided what to keep, discard, or redo,
authorized all paid computation, and is responsible for the accuracy and integrity of the
submission, including this section. No generative AI tool is listed as an author.

Three checks bear on how much trust the model-produced outputs warrant. First, quantitative
predictions were preregistered in writing, dated, before the corresponding analysis script was
run; the repository holds several dozen such preregistrations, one per analysis. Second, the
analysis pipeline fixes a random seed at every stochastic step, and independent reruns are
checked to reproduce identical output before a result is reported. Third, the manuscript and
code were subjected to adversarial review passes whose default posture is rejection; these
passes are how two substantive defects were found and corrected before submission: a
statistical control meant to carry only each person's accuracy margin that in fact copied
their true individual answer with the complementary probability, which invalidated the
conclusion drawn from it, and a bootstrap confidence interval reported as "[0, 0]" on a
zero-event sample — an artifact of the percentile method rather than a genuine null result,
since replaced with an exact Clopper-Pearson interval.

These checks reduce, but do not remove, the risk that a model-produced number or claim is
wrong; the responsible investigator remains accountable for every figure and statement in this
paper regardless of how it was produced.
```

**Vérifications faites avant d'écrire ce texte** (dans le dépôt, pas seulement dans le
rapport de conformité) :
- Préenregistrement systématique avant calcul : confirmé, plusieurs dizaines de fichiers
  `resultats/*-preenregistrement.md` (`c7-preenregistrement.md`,
  `c7-tautologie-preenregistrement.md`, `c7-nul-corrige-preenregistrement.md`, etc.), chacun
  daté et écrit « avant tout calcul ».
- Graine fixée et réexécution vérifiée bit-à-bit : confirmé, ex. `graine` utilisée dans des
  dizaines de scripts `analyses/*.py`, et `c7-tautologie-preenregistrement.md` : « Graine
  fixée … ; une deuxième exécution complète doit produire un CSV bit-à-bit identique. »
- Témoin statistique invalide trouvé par revue adverse : confirmé,
  `resultats/c7-nul-corrige-preenregistrement.md` : le nul de `analyses/c7_disjoint.py`
  (fonction `construire_nul`, ligne 134) écrivait la vraie réponse `y_ref` avec probabilité
  q_i au lieu de ne porter que la marge d'exactitude — « Le témoin ne teste donc pas ce qu'il
  prétend tester… sans valeur probante. »
- Intervalle de confiance dégénéré trouvé par revue adverse : confirmé,
  `resultats/revue-hostile-finale-2026-09-12.md`, finding **F2 (FATAL)** : intervalle
  bootstrap « [0 ; 0] » sur un échantillon à zéro événement, qualifié d'« artefact connu du
  bootstrap percentile », correction demandée « Clopper-Pearson partout ».
- **Non retenu** : la vérification des références bibliographiques contre leurs sources
  primaires, que tu m'avais donnée comme fait acquis, **n'est pas confirmée** — au contraire,
  `resultats/conformite-popets-2026-09-12.md` (point 1) et le manuscrit lui-même
  (`[OPEN ITEMS]` #4, #5, #6, lignes 1071–1086) déclarent explicitement que ce recoupement
  reste à faire. Je ne l'ai donc pas mise dans le texte.

---

## Texte 2 — repositionnement de la position sur le comité d'éthique

**Où l'insérer** : ceci **remplace** le paragraphe actuel dans `article/manuscrit.md`, §8
Ethics Considerations, lignes 992–997 (sous-titre en gras actuel : **« IRB determination: a
declared gap. »**, qui commence à « This work has no ethics exemption… » et finit à
« …distinct from the data-licence verification conducted separately. »). Le reste de la
section 8 (lignes 930–991, 998) n'est pas concerné.

**Point de vigilance sur la prémisse que tu m'avais donnée** : j'ai vérifié en direct la page
crysp.petsymposium.org/authors-2027.php (deux requêtes séparées, en citant le paragraphe
précédent et le paragraphe suivant pour situer chaque phrase). La phrase « A "no" answer is
not a ground for rejection as long as the authors provide a reasonable explanation » s'y
trouve **exclusivement** dans le paragraphe sur la publication de code/données (section « open
science »), immédiatement après « If 'no', authors will be asked to provide a brief
explanation », et est suivie de « Note that this is distinct from the artifact review… ». Elle
ne porte **pas** sur la question IRB/comité d'éthique. Le paragraphe sur l'éthique dit
seulement : « a justification of the ethics of the work and information about whether the work
was submitted to an external ethics panel such as an IRB or the Tor Research Safety Board » —
sans garantie explicite qu'un « non » y soit sans conséquence. Le texte ci-dessous respecte
donc exactement ce qui est réellement exigé (une information + une justification), sans
invoquer une clause d'exemption qui ne figure pas sur la page pour cette question précise.

Texte à coller (remplace le paragraphe « IRB determination: a declared gap ») :

```
**Ethics review and scope.** This study was not submitted to an external ethics panel such as
an IRB. It relies exclusively on secondary data already made public by their original
publishing teams — Twin-2K-500 (CC BY 4.0) and the Park et al. replication package — and no new
data was collected from any person: we surveyed no one, interviewed no one, and had no contact
with any data subject. On that basis we judged the study out of scope for human-subjects
review; §8 above records the corresponding limit (participants did not specifically consent to
a re-identification test on the twins generated from their answers).

This scoping does not extend to the released artifact: it runs solely on 600 fictitious
persons generated at a fixed seed (`config.GRAINE`), and a guard (`garde.py`) refuses to run if
any path under the repository's `data/` directory is supplied. Nothing we distribute processes
a real person's data.

We regard measuring this risk on already-public data as serving privacy rather than working
against it: the risk was named, not created, by this work. Park et al.'s own consent materials
already warned participants that information might be "inadvertently shared" and that complete
anonymity remained difficult; an outside professional body separately rated synthetic-response
re-identification as high-risk without measuring it. This paper supplies a first measurement,
computed only from material already public, so that other panel holders can test their own
releases before publication rather than after an incident. No individual is identified: only
rates aggregated over full cohorts are reported, and the attack code we release only acts when
the user already holds real answers to the same items, which does not lower the barrier for an
outside attacker who does not. Responsible disclosure to the Twin-2K-500 and Park et al. teams
— the datasets' publishers, whom we have not yet contacted — is planned before any public
posting of this work, with a 30-day response window; see Availability.
```

**Vérifications faites avant d'écrire ce texte** :
- Données secondaires déjà publiques, aucune collecte nouvelle : confirmé, manuscrit lignes
  932–935 (« Twin-2K-500 is public under CC BY 4.0… No new data was collected »).
- Aucun contact avec les personnes concernées : confirmé, lignes 950–954 et `[OPEN ITEMS]` #1
  (lignes 1060–1064) — les lettres de divulgation ne sont pas encore envoyées, donc ni les
  équipes ni a fortiori les participants n'ont été contactés à ce jour.
- Artefact strictement synthétique avec garde-fou : confirmé, `artefact/garde.py` (refuse tout
  chemin résolu vers `data/` ou ses descendants) et manuscrit ligne 1006 (« 600 synthetic
  persons generated at fixed seed »).
- Divulgation responsable prévue auprès des équipes ayant publié les jeux (pas des personnes) :
  confirmé, lignes 950–954.
- Le risque était déjà nommé par Park et al. eux-mêmes et par un tiers (AAPOR) : confirmé,
  lignes 956–958 et 987–990.
- **Corrigé par rapport à ta prémisse** : je n'ai pas écrit qu'un « non » à la question IRB
  n'est « pas rédhibitoire s'il est justifié » comme règle explicite de PoPETs, parce que cette
  garantie précise, sur la page officielle, ne couvre que la question code/données, pas la
  question du comité d'éthique (voir le point de vigilance ci-dessus). Le texte fournit tout de
  même l'information et la justification demandées par le paragraphe éthique lui-même.

Note pour l'orchestrateur : `[OPEN ITEMS]` #3 (lignes 1068–1070) référence l'ancien cadrage
« gap » ; à revoir/retirer une fois ce remplacement fait, puisqu'il n'y a plus de « gap »
déclaré au même sens.
