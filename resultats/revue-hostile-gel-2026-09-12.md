# Revue hostile avant gel — PoPETs 2027.3 — UNE CONSIGNE BORNÉE le 13 septembre 2026

statut: provisoire
borne_par: resultats/correction-t1b-2026-09-13.md
fait_foi: resultats/correction-t1b-2026-09-13.md (pour la consigne D1 et le couple de chiffres du témoin corrigé)
mandat: relecture hostile de article/manuscrit.md avant gel, posture relecteur senior en vie privee, avis par defaut le rejet (mandat d'origine du 12/09, reconstitue depuis le corps du rapport)
agent: relecteur hostile avant gel, 12/09 ; en-tete A2 et bornage poses le 13/09 par Claude Opus 5, sous-agent marqueurs canoniques
ecriture: resultats/revue-hostile-gel-2026-09-12.md (en-tete et bandeau seulement ; le corps d'origine est conserve mot pour mot)
lecture_seule: tout le reste
interdits: appel payant, reseau, recherche web, commit sur master, arriere-plan, toute modification de article/manuscrit.md
cout_reel_usd: 0.00

> ## BORNÉ, le 13/09/2026 — la consigne D1 prescrit un chiffre qui ne fait plus foi
>
> **État : BORNÉ** (le défaut D1 est réel et tient ; le chiffre de remplacement qu'il
> prescrit est périmé). Fait foi : `resultats/correction-t1b-2026-09-13.md`.
>
> Le §D1 ci-dessous conclut « **Ce qu'il faut faire.** Remplacer l. 76 et la ligne 1 du
> tableau 1 par “0.974 [0.950 ; 0.993] against 0.965 observed” ». **Cette consigne ne
> doit plus être exécutée telle quelle.** Le 0,974 est la moyenne d'un run **arrêté à
> 20 réplicats**, alors que `resultats/c7-nul-corrige-preenregistrement.md` §5 en
> prescrivait **100**. Aux 100 prescrits, la série qui fait foi vaut **rho moyen 0,9799,
> bande [0,9510 ; 0,9930]** (`resultats/c7-nul-corrige-marginal.csv`, ligne `marginal` /
> `n_replicats = 100`, seule ligne portant `fait_foi_tableau1= oui`).
>
> **Ce qui tient intégralement :** le défaut D1 lui-même — le manuscrit porte bien deux
> paires de chiffres pour la même démonstration, et l'introduction et le tableau 1 citent
> bien le témoin d'origine (0,984 / 0,969). Le geste à faire est le même ; **seul le
> couple à écrire change**. Et le verdict ne bouge dans aucun des deux cas : la
> prédiction (b) reste réfutée (0,9650 sous le 95ᵉ centile, 0,9934 à n = 20 comme 0,9930
> à n = 100).
>
> **Interdit à partir d'ici :** écrire « 0.974 [0.950 ; 0.993] » dans le manuscrit, le
> résumé, le tableau 1, la légende de la figure 2 ou la lettre de divulgation, au motif
> de cette consigne.

> **NOTE D'ÉTAT (12 septembre 2026) — vérifiée point par point contre `article/manuscrit.md`
> tel qu'il est aujourd'hui, pas rapportée sur la seule foi d'un autre audit.** La plupart des
> constats ci-dessous sont **déjà traités** : **D1** (table 1 et §1.1 citent désormais le
> témoin corrigé 0,974 [0,950 ; 0,993] contre 0,965, l'ancienne paire 0,984/0,969 étant
> explicitement étiquetée comme périmée — l. 877 et alentours) ; **D2** (la figure 2 est
> désormais appelée depuis §5.1, plus orpheline en fin de §5.9) ; **D3** (« composite utility
> index » et « 1.47 is not D4's cost » sont déjà en place aux lignes citées par la revue —
> confirmé indépendamment par `resultats/cout-d4-propagation-2026-09-12.md`, qui identifie ce
> même constat D3 de la présente revue comme périmé et met en garde contre sa réouverture) ;
> **D4** (« We do not claim a measured dissociation between memorization and
> re-identification » remplace l'énoncé trop fort) ; **D5(b)** (titre devenu « No new harm on
> Twin-2K-500 ») ; **D5(c)** (absence de licence OSF et conditions NORC nommées en §8) ;
> **D5(d)** (la contradiction sur l'accès aux réponses Park est résolue en une phrase) ; **D6**
> (clés bibliographiques alignées sur `references.bib` — `toubia2025twin2k500`,
> `park2024agents`, `giomi2023unified` vérifiées directement dans le texte —, entrée AAPOR
> ajoutée au `.bib`, `anon2026decoupling` identifié comme `shafieinejad2026diffusion`) ; **D7**
> (la phrase de réconciliation entre 33,1 % et 20,7 % est désormais présente en §5.5). **Reste
> ouvert, vérifié comme tel** : **D5(a)** — les lettres de divulgation ne sont toujours pas
> parties (« the letters have not been sent », `article/manuscrit.md` l. 1045) ; et **D8** —
> les trois graphies 20,68 % / 20,69 % / 20,7 % coexistent encore, non harmonisées. Ces deux
> points restent valablement signalés. N'a pas été revérifié ligne à ligne : la légende gravée
> dans l'image `fig2-couplage.png` elle-même (31,15 % contre 31,6 %), qui échappe à une lecture
> du texte source.
**Date** : 2026-09-12. **Objet** : `article/manuscrit.md` (1 087 lignes), contrôlé contre
`resultats/article-synthese.md`. **Posture** : relecteur senior en vie privée, avis par défaut
le rejet. Aucun appel d'API, aucune recherche web.

---

## Verdict

**Révision majeure** — non parce que l'article serait faux, mais parce que trois de ses pièces
les plus lues (l'introduction, le tableau 1, l'appareil de références) publient encore l'état
antérieur du texte, et parce que la position éthique n'est pas tenable en l'état pour ce lieu.

**Je n'ai trouvé aucun défaut fatal.** Après vérification, chaque affirmation chiffrée que j'ai
remontée est soutenue par sa source et par son intervalle, et les formulations interdites par la
synthèse sont respectées là où elles comptent. Les défauts ci-dessous sont des défauts de
**couture** et de **formulation** : l'article dit vrai, mais à trois endroits il dit ce qu'il
disait avant d'être corrigé, et à un endroit il revendique plus qu'il n'a mesuré. Tout est
réparable en une à deux journées, sauf D5 qui dépend d'une décision.

---

## Défauts, par gravité

### D1 — L'introduction et le tableau 1 publient les chiffres du témoin que l'article déclare lui-même défectueux
**Gravité : haute. Nature : défaut de formulation** (le verdict est inchangé), **mais le plus
humiliant du lot.**

**Revendication touchée** : A1, la réfutation de la prédiction (b) — le cœur argumentatif du
papier.

**Les phrases exactes.**

- Ligne 75-78 (§1.1) : « The null reaches mean Spearman **0.984**, 95th percentile 1.000
  [c7-disjoint-resultats.md §2]; observed **0.969** does not exceed it. »
- Ligne 813 (tableau 1, ligne 1) : « **Refuted.** Null rho **0.984** (95th pct 1.000) against
  **0.969** observed | `c7-disjoint-resultats.md` §2 »
- Ligne 392-398 (§5.1), qui dit l'inverse sur la provenance : « The original marginal null **did
  carry that defect** […] With the defect corrected, the witness still reproduces the coupling —
  **rho 0.974**, 5th–95th percentiles [0.950 ; 0.993], against **0.965** observed ».
- Ligne 34-35 (résumé), qui utilise bien la paire corrigée : « 0.974 [0.950 ; 0.993] against
  0.965 observed ».

**Le défaut.** Le manuscrit porte deux paires de chiffres pour la même démonstration. Le résumé
et §5.1 citent le témoin **corrigé** (0,974 contre 0,965, source `audit-renversement-2026-09-12.md`,
et c'est celui que la synthèse désigne comme « témoin principal à publier », A1 l. 19).
L'introduction et le tableau 1 citent le témoin **d'origine** (0,984 contre 0,969), celui dont
§5.1 explique trois pages plus loin que ses cellules fausses évitaient la vraie réponse et
gonflaient sa fuite d'un facteur 1,3. Les deux paires sont des comparaisons internement
cohérentes — 0,969 est l'observé sur 50 partages disjoints, 0,965 l'observé sur les 12
configurations — mais rien dans le texte ne le dit, et un relecteur qui lit l'introduction puis
§5.1 conclut que les auteurs ne savent pas lequel de leurs deux témoins ils publient.

**Circonstance aggravante** : §10 (l. 1058-1060) met en avant, comme preuve de sérieux, que la
relecture adverse a trouvé **ce défaut précis** (« a statistical control meant to carry only each
person's accuracy margin that in fact copied their true individual answer »). Le papier se
félicite d'avoir corrigé un témoin dont il publie encore les chiffres non corrigés en
introduction.

**Ce qu'il faut faire.** Remplacer l. 76 et la ligne 1 du tableau 1 par « 0.974 [0.950 ; 0.993]
against 0.965 observed », source `audit-renversement-2026-09-12.md` ; ne laisser 0,984 que dans
§5.1, où il est explicitement présenté comme la valeur d'avant correction. Vérifier que
l'introduction dit, comme §5.1, que la correction ne change pas le verdict.
**Coût** : 15 minutes. **Le verdict ne bouge pas** : (b) reste réfutée avec l'une ou l'autre paire.

---

### D2 — La figure 2 est orpheline, et elle est construite sur le témoin périmé
**Gravité : haute. Nature : couture + contradiction texte/figure.**

**Revendication touchée** : A1, et la lisibilité de la contribution honnête.

**Les faits.**
- Le bloc de légende de la figure 2 est aux **lignes 690-705**, c'est-à-dire **à la fin de §5.9
  (Scale)**, alors qu'elle illustre §5.1.
- **§5.1 ne référence jamais la figure 2.** Recherche sur tout le manuscrit : « Figure 2 »
  n'apparaît qu'à la ligne 690, dans sa propre légende. La figure qui porte la contribution la
  plus délicate du papier n'est appelée nulle part dans le texte qui l'explique.
- Sa source de données, `resultats/c7-disjoint-nul.csv` (l. 705), est le nul **d'origine** :
  ses valeurs tournent autour de 0,986, moyenne 0,984 — le témoin défectueux de D1. La légende
  (l. 699) y place « the observed disjoint-item rho (**0.969**) » : la figure est donc
  l'illustration graphique de la paire périmée.
- La synthèse (l. 132) enregistre en outre un **défaut connu non corrigé** : la légende gravée
  dans `fig2-couplage.png` affiche « 31.15 % top-1 » pour le témoin apparié, alors que le
  chiffre qui fait autorité est **31,6 %** — celui qu'emploie le texte aux lignes 34, 75 et 403.
  Texte et image se contredisent sur le même nombre, dans la figure qui sert de preuve d'honnêteté.

**Ce qu'il faut faire.** Déplacer la légende dans §5.1 et l'y appeler explicitement ; régénérer
la figure depuis le témoin corrigé (ou, si la bande du nul d'origine est conservée à dessein,
l'écrire dans la légende) ; corriger 31,15 → 31,6.
**Coût** : une demi-journée, agent figures. **À coordonner** : `analyses/figures_article.py` est
en cours de modification par un autre agent.

---

### D3 — Le 1,47 point revient deux fois après avoir été retiré
**Gravité : moyenne-haute. Nature : défaut de formulation, violation d'un INTERDIT explicite.**

**Revendication touchée** : A8 (coût de la défense) et A12 (comparaison à la DP).

**Les phrases exactes.**
- Ligne 718-719 (§6) : « A previously circulated mean of 1.47 points divided by three an effect
  that falls entirely on one component, and **is withdrawn**. »
- Ligne 758 (§6.2) : « loses 3.33 and 3.38 points of utility, **within 5 points of D4's 1.47** ».
- Ligne 826 (tableau 1, ligne 14) : « eps = 3/10 lose 3.33/3.38 points **against D4's 1.47** ».

**Le défaut.** Le manuscrit retire une moyenne au §6 puis s'en sert deux fois après, dont une
fois dans le tableau récapitulatif. La synthèse l'interdit nommément (A8, l. 62 : « INTERDIT […]
présenter le coût comme une moyenne unique de 1,47 point »). Un relecteur qui lit §6 puis §6.2
voit le papier employer un chiffre qu'il vient de rétracter.

**Nuance à trancher par les auteurs** : il est possible que la comparaison DP porte légitimement
sur un **indice composite d'utilité** dont 1,47 est la valeur pour D4. Si c'est le cas, le
problème n'est pas le nombre mais son nom : il faut l'appeler autrement (« composite utility
index ») et dire en une clause pourquoi la comparaison à la DP se fait sur l'indice agrégé alors
que le coût de D4 se rapporte par composante. Sinon, remplacer par « 4.4 points on inter-item
correlations (0.0 on distribution, 0.0 on group differences) ».
**Coût** : 20 minutes si l'indice est nommé ; une heure s'il faut recalculer la comparaison.

---

### D4 — La contribution (2) revendique une dissociation qu'elle n'a pas mesurée là où elle compte
**Gravité : moyenne-haute. Nature : défaut de formulation — l'article dit trop.**

**Revendication touchée** : contribution (2), « A dissociation between memorization and
re-identification ».

**Les phrases exactes.**
- Ligne 111-113 (§1.2) : « **(2) A dissociation between memorization and re-identification.** The
  leakage is not regurgitation of training data: a model whose training cutoff precedes the
  panel's publication (llama31-8b) copies nothing verbatim and leaks no more than models that do
  [c7-gen-resultats.md] ».
- Ligne 615-616 (§5.7) : « Memorization is excluded as the explanation: llama31-8b, with a
  training cutoff preceding publication, copies nothing verbatim and leaks no more than the models
  that do copy. »

**Le défaut.** Le témoin llama31-8b vit dans §5.7, dont le sujet entier est que **nos** jumeaux
n'identifient presque personne : 0,00 % à 0,83 % [0 ; 2,15] de top-1 (l. 609-613). Écarter la
mémorisation en comparant des systèmes qui **ne fuient pas** ne dit rien de la fuite qui porte le
papier — 23,23 % sur Twin-2K-500, 90,40 % sur l'archive Park — produite par des pipelines dont
nous ne pouvons sonder ni les données ni la coupure d'entraînement. « Ne fuit pas davantage que
les modèles qui recopient » est vrai dans un régime où personne ne fuit : l'énoncé est sans
contenu pour la question posée.

Ce qui **reste** solide dans la contribution (2) : l'ablation de §5.5 (permuter l'ordre des 40
réponses fait tomber le top-1 de 33,1 % à 0,046 %, l. 563-564) localise bien le signal dans la
structure de dépendance et non dans le contenu d'une réponse — cela affaiblit la mémorisation
comme mécanisme ; et l'argument « the pipeline trains nothing on the target population » (l. 113)
est valide, mais c'est un argument structurel, pas une mesure.

**Ce qu'il faut faire.** Reformuler (2) pour la faire reposer sur l'ablation et sur l'absence
d'entraînement, et redescendre le contrôle de coupure à ce qu'il est : un contrôle sur **nos**
jumeaux, cité comme tel. Ne pas annoncer une « dissociation » établie pour les jumeaux que nous
attaquons.
**Coût** : un paragraphe. **Pourquoi ça presse** : c'est la deuxième contribution listée, donc
la deuxième chose que lit un relecteur, et c'est celle qui tombe le plus vite.

---

### D5 — La section éthique n'est pas tenable en l'état
**Gravité : haute. Nature : mixte — une omission factuelle, un titre qui déborde son argument, une
décision en attente.**

**(a) Les lettres ne sont pas parties, et la soumission est elle-même un événement de divulgation.**
Ligne 949-952 : « Responsible disclosure. Planned with the Twin-2K-500 authors (Toubia et al.) and
with Park et al. **before any preprint posting or code release**, with a 30-day response window
[…] **These letters have not yet been sent.** » Le dépôt à PoPETs met le texte entre les mains
d'un comité qui attend soit une consultation déjà faite, soit une raison écrite de ne pas l'avoir
faite. Le dossier interne le dit déjà sans détour
(`consultant-angles-morts-2026-09-12.md` l. 255-260 : « Aucune notification aux auteurs des
données, **et c'est le point bloquant** »). **Ce qu'il faut faire** : ouvrir le délai de 30 jours
maintenant et écrire dans §8 la date d'envoi ; c'est sur le chemin critique, pas à côté.
**Coût** : décision du responsable, puis 30 jours d'horloge.

**(b) Le titre « No new harm on these datasets » couvre deux jeux, l'argument n'en couvre qu'un.**
Ligne 940-943 : « **No new harm on these datasets.** Twin-2K-500 already publishes, for each
person, their identifiers and real answers beside their twin: matching is trivial without any
attack. The result does not create new harm on **this specific dataset** ». L'argument vaut pour
Twin-2K-500 seulement. L'archive Park — celle qui porte le 90,40 % en monde fermé et le 60,17 %
en monde ouvert, et dont les auteurs ont restreint l'accès aux réponses individuelles **pour
raison de vie privée** (l. 52-53, l. 208) — n'est couverte par aucune phrase. Le titre déborde
exactement là où le risque est le plus élevé. **Ce qu'il faut faire** : titrer « No new harm on
Twin-2K-500 » et ajouter deux phrases sur Park, qui assument que le cas y est différent et
renvoient à la divulgation.

**(c) L'article ne mentionne jamais la contrainte de licence que son propre dépôt a enregistrée.**
`data/PROVENANCE.md` (l. 20-27) est formel : le nœud OSF t6g7k **ne déclare aucune licence** —
« l'accès public n'emporte pas droit de redistribution des réponses individuelles » — et les
conditions NORC « **interdisent la reproduction du GSS sous toute forme sans accord écrit
préalable** » ; verdict retenu en interne : « ne jamais publier ni redistribuer les fichiers de
réponses individuelles […] seuls le code d'analyse et des agrégats revus pour la divulgation sont
publiables, avec citation NORC et attribution Park et al. ». Le manuscrit n'en dit rien : §8
qualifie simplement le paquet de « publicly posted » (l. 931-932), et §9 se borne à « publicly
posted on OSF […] is not redistributed here […] Verify current terms of use on the OSF page
before any download » (l. 1026-1029). Aucune mention de NORC, aucune mention de l'absence de
licence. Pour un lieu consacré à la vie privée, l'omission est plus coûteuse que la contrainte.
**Ce qu'il faut faire** : nommer l'absence de licence et les conditions NORC dans §8 et §9,
attribuer NORC, et écrire que seuls des agrégats sont publiés. **Coût** : un paragraphe.

**(d) Contradiction interne sur ce que Park a réellement restreint.** Ligne 52-53 : « Park et al.
built generative agents for 1,052 participants and, citing privacy, **restricted access to the
individual responses of those agents** ». Or `data/PROVENANCE.md` (l. 14-16) atteste que
l'archive publique que nous avons analysée contient « les réponses individuelles des 1 052
participants […] **[et les] réponses des cinq conditions d'agents** ». Soit la restriction a été
levée, soit elle n'a jamais couvert le paquet de réplication : dans les deux cas la phrase
motrice de l'introduction et la section données se contredisent, et c'est précisément le point
que la lettre de divulgation à Park doit énoncer correctement. **Ce qu'il faut faire** :
reformuler l. 52-53 pour décrire ce qui est effectivement public, et dire en une phrase ce que
cela implique pour la protection annoncée par Park.

**(e) Pas de détermination éthique externe.** Ligne 990-996 : « This study was not submitted to
an external ethics panel such as an IRB […] we judged the study **out of scope** for
human-subjects review ». L'auto-exemption est courante et l'argumentaire (données secondaires,
aucun contact avec une personne) est correctement écrit. Mon avis : **tenable**, à condition que
(a), (c) et (d) soient réglés — une auto-exemption assortie d'une divulgation faite et d'une
licence correctement déclarée passe ; la même auto-exemption avec des lettres non envoyées et
une licence non mentionnée se lit comme un évitement.

---

### D6 — L'appareil de références de `manuscrit.md` ne pointe plus sur la bibliographie
**Gravité : moyenne (haute si `manuscrit.md` est lu par un relecteur). Nature : couture.**

**Sur les 41 clés listées aux lignes 1076-1086, 13 n'existent pas dans `article/references.bib`.**

Onze sont des orthographes périmées, renommées depuis dans le .bib :

| cité dans `manuscrit.md` | clé réelle du .bib |
|---|---|
| `toubia2025twin` | `toubia2025twin2k500` |
| `park2024generative` | `park2024agents` |
| `giomi2023anonymeter` | `giomi2023unified` |
| `taub2018dcap` | `taub2018differential` |
| `argyle2023out` | `argyle2023outofone` |
| `eckersley2010browser` | `eckersley2010unique` |
| `adams2025iscience` | `adams2025fidelity` |
| `byun2025kdd` | `byun2025riskcontext` |
| `satml2025position` | `zhang2024satml` |
| `ganev2024genlaw` | `ganev2024regulatory` |
| `drechsler2024synthetic` | `drechsler2024thirtyyears` |

Deux n'existent **nulle part** dans le .bib :
- `bowen2023synthetic`, cité §2.6 l. 240-241 ;
- `anon2026decoupling`, cité §2.5 l. 229 comme **l'un des trois contradicteurs** — une citation
  porteuse pour la défense en travaux connexes.

**Atténuation, et ce qu'elle révèle.** `article/latex/main.tex` emploie déjà les **bonnes** clés
et ne cite **ni** `bowen2023synthetic` **ni** `anon2026decoupling`. La version compilée est donc
probablement saine — mais cela veut dire que le troisième contradicteur de §2.5 a **disparu** de
la version LaTeX sans que personne ne l'acte. Ce n'est plus un défaut d'appareil, c'est une
**divergence de contenu entre les deux versions du papier** : §2.5 de `manuscrit.md` répond à
trois contradicteurs, §2.5 du LaTeX à deux. À signaler à l'agent LaTeX avant le gel.

**Deux défauts connexes, même famille.**

1. **L'AAPOR est cité deux fois en prose, sans clé et sans entrée bibliographique.** Ligne 55-57
   (introduction) : « the AAPOR task force, which ranks synthetic response generation as the
   highest-privacy-risk task it evaluates and names re-identification by linkage without ever
   quantifying it » ; ligne 985-988 (§8, *Public interest*) : « The AAPOR report of 8 May 2026
   ranks synthetic response generation as the highest privacy-risk task it evaluates ». Recherche
   sur `references.bib` : aucune entrée AAPOR, sous aucun nom. Une source non citée porte à la
   fois la motivation de l'introduction et l'argument d'intérêt public de la section éthique.
   **À corriger impérativement** : c'est le genre de trou qu'un relecteur de PoPETs vérifie.

2. **La phrase de clôture sur les références promet plus que l'audit qu'elle cite.**
   Ligne 1073-1074 : « **all 45 entries have been checked against their sources**, and the audit
   is recorded in `article/references-verification.md` ». Or (i) le .bib compte aujourd'hui **46**
   entrées ; (ii) le document cité dit lui-même (l. 3-6) que **27 des 45** proviennent d'une
   vérification antérieure « reprises telles quelles […] **sans nouvelle vérification** », seules
   18 ayant été vérifiées à la source dans cette passe ; (iii) il signale `gouweleeuw1998pram`
   comme « **À VÉRIFIER avant dépôt** » (aucun DOI retrouvé). Dans un papier dont toute la
   posture est la scrupulosité, une affirmation démentie par le document produit comme sa preuve
   est un mauvais endroit où se faire prendre. **Ce qu'il faut faire** : « the 46 entries are
   recorded in `article/references-verification.md`, 18 re-verified at source in the final pass;
   one DOI remains outstanding ».

**Coût total D6** : une heure, plus la coordination avec l'agent LaTeX sur `anon2026decoupling`.

---

### D7 — Le 33,1 % de l'ablation n'est jamais réconcilié avec le 20,7 % de tête
**Gravité : moyenne. Nature : justification coupée.**

**Revendication touchée** : A5, l'ablation présentée comme « the strongest evidence ».

**La phrase exacte**, ligne 563-564 (§5.5) : « permuting the order of each twin's 40 purchase
answers drops closed-world top-1 from **33.1 % [31.2 ; 35.2]** to 0.046 % [0 ; 0.11] ».

**Le défaut.** Le taux de tête du même jumeau, sur les mêmes 2 058 personnes, est **20,7 %**
(§5.2 l. 428). L'ablation part donc d'une base **supérieure** au résultat principal, sans un mot
d'explication. La raison est lisible pour qui remonte à la source (`c7-mecanisme-resultats.md`
l. 19-24) : l'ablation attaque les **40 items d'achat seuls**, tandis que le chiffre de tête
utilise les **60 items communs**. Autrement dit, les chiffres du papier disent qu'**ajouter les
20 items d'opinion fait tomber le top-1 de 33,1 % à 20,7 %**. C'est très probablement réel et
cohérent avec §5.5 elle-même (les items d'opinion identifient 46× moins, l. 569-571) : la règle
de Hamming naïve dilue le signal quand on lui donne des items peu informatifs. Mais tel
qu'imprimé, cela se lit comme une incohérence, et un relecteur hostile écrira que les auteurs ne
contrôlent pas leur propre dénominateur.

**Ce qu'il faut faire.** Une phrase dans §5.5 : la base de l'ablation est l'attaque sur les 40
items d'achat seuls, supérieure au taux à 60 items parce que la règle naïve est diluée par les
items d'opinion — et, si l'on veut le dire, que c'est une confirmation indépendante de H1.
**Coût** : une phrase. Une demi-journée si l'on veut mesurer la dilution pour l'affirmer.

---

### D8 — Défauts mineurs, à balayer en une passe
- **Le même taux non défendu écrit de trois façons** : 20,68 % (l. 712), 20,69 % (l. 741),
  20,7 % (l. 428). Harmoniser ou dire une fois pourquoi ils diffèrent.
- **Tableau 1, ligne 2** (l. 814) source `c7-monde-ouvert-resultats.md` alors que le fichier qui
  fait autorité pour les IC est `c7-fort-monde-ouvert-ic-2026-09-12.md`, correctement cité en
  §5.3 (l. 462).
- **La liste de références se dit « in order of first appearance »** (l. 1075) et ne l'est pas :
  `giomi2023anonymeter` apparaît d'abord l. 105 mais figure en 11ᵉ position, après
  `adams2025iscience` dont la première occurrence est l. 228 ; `anon2026decoupling` (l. 229) est
  listé après `guepin2023synthetic` (l. 279).
- **§9 liste trois préenregistrements** « each written before any computation » (l. 1031-1033)
  quand §10 parle de « several dozen such preregistrations » (l. 1054). Écrire « for example ».
- **§2.4 l. 213-214** : « None of these works […] measures a re-identification rate from twin
  outputs. **That is the gap we fill.** » La revendication est plus étroite que celle que le
  résumé a pris soin de désamorcer (« We do not claim an absence of prior work », l. 27-28) et
  elle survit — mais la formule « the gap we fill » rappelle exactement l'objection que le résumé
  cherche à prévenir. Reformuler en « that is what we measure ».
- **Titre du papier** : « […] a Twin-to-Twin Channel […] ». Après la chute de T2, le canal existe
  en pipeline partagé et disparaît sinon. Le titre ne ment pas (il ne dit pas
  « cross-organisation »), mais il vend le canal comme acquis. Le laisser est un choix
  défendable ; le savoir est nécessaire.

---

## Sur le retournement A7/T2 : est-il assumé partout ?

**Oui, et proprement.** J'ai cherché des traces de l'ancienne ambition ; je n'en trouve pas.
Le résumé (l. 26-27), la contribution (1) (l. 96-97 et 107-108), le modèle de menace T2
(l. 281-287), §5.4 (l. 543-552) et la ligne 17 du tableau 1 disent tous la même chose, dans le
même sens, avec le même chiffre et le même intervalle. La discipline du « jamais un chiffre sans
son nombre d'items communs » est tenue partout, et le 26,11 % retiré est signalé comme retiré
(l. 512-513).

**Une seule réserve de vocabulaire** : §5.4 et §3 écrivent « **not confirmed** » là où la
synthèse (l. 56) et la règle préenregistrée concluent « **A7 est détruite** dans cette
configuration », et où le tableau 1 ligne 17 écrit « **Refuted** ». Le manuscrit est donc, par
endroits, **plus faible** que son propre verdict — ce qui est le bon sens de l'erreur, mais
l'incohérence de vocabulaire entre le tableau et le corps mérite d'être levée.

---

## Ce qui reste vraiment neuf — réponse franche

L'apport ne se réduit **pas** à préciser où une conclusion d'Anonymeter cesse de valoir. Cette
contradiction mesurée est la **plus faible** des contributions, pas leur somme. Ce qui tient, et
qui suffit largement pour ce lieu :

1. **Les taux en monde ouvert, sur deux jeux, avec leur plafond humain.** Personne ne les a.
   C'est la mesure la plus difficile à attaquer en relecture et elle ne dépend d'aucune lecture
   causale du couplage. C'est la colonne vertébrale du papier.
2. **Le canal jumeau-à-jumeau en pipeline partagé**, avec un contrôle anti-artefact à
   0,04–0,31 % et une décomposition qui attribue 82 % de la montée au-dessus du plancher à la
   personne elle-même. Neuf, même après la chute de T2 — à condition de ne jamais laisser le
   lecteur croire qu'il s'agit du scénario inter-organisations.
3. **Le nul de marge qui absorbe le propre effet des auteurs.** C'est, méthodologiquement, la
   chose la plus précieuse du dossier, et elle est rare : une équipe qui construit le témoin que
   la littérature réclamait (Das/Tramèr) et publie qu'il mange son résultat. Un relecteur
   sérieux valorisera cela plus que le taux lui-même.
4. **PRAM appliqué aux jumeaux avec sa courbe risque-utilité mesurée**, un attaquant adaptatif,
   et les conséquences sur les analyses en aval — le volet constructif, qui manque à presque
   toute la littérature d'attaque.
5. **Une attaque qui falsifie la propre première mesure de l'équipe** (Park, +38 % relatifs).

Deux de ces cinq suffiraient. **Ce qui ne survivrait pas comme « contribution »** : le point (2)
tel qu'il est formulé aujourd'hui (voir D4), et toute croissance future de la revendication de
transportabilité des bits — un facteur 1,34 sur une comparaison à deux jeux est correctement
couvert par les précautions actuelles, mais ne supporterait pas un mot de plus.

---

## Ce qui survit intact

C'est la partie la plus utile de ce rapport : tout ce qui suit a été vérifié et n'a **pas** besoin
d'être retouché avant le gel.

- **§5.3, monde ouvert** (l. 453-480). Chiffres, intervalles, refus explicite de présenter le
  gain de l'attaquant fort comme établi sur Twin, et réserve sur le FPR = 0,1 % nommant le
  **nombre absolu de faux positifs** (« roughly one absolute false positive on Park and two on
  Twin »). Conforme mot pour mot aux exigences d'A3. Rien à changer.
- **§5.1, traitement de la réfutation** (l. 400-423). Toutes les formulations interdites par la
  synthèse sont évitées : pas de causalité, pas d'axe unique, pas de « minorant », et le témoin
  est correctement décrit comme **non dépourvu de structure** (il fuit 31,6 % contre 20,73 %).
  Seuls les **chiffres** de l'introduction et du tableau 1 sont périmés (D1) — le raisonnement,
  lui, est juste partout.
- **§5.4, discipline du nombre d'items** (l. 511-513). Jamais un taux sans son compte d'items
  communs, et le 26,11 % explicitement retiré. Exemplaire.
- **§5.4, anomalie Park** (l. 529-537). Le résidu de ~3× est déclaré non expliqué, les deux
  candidats non testables sont nommés, et rien n'est présenté comme résolu.
- **§6.1, réserve qui borne la garantie** (l. 746-749) : le résidu vient entièrement des 20 items
  d'opinion non permutés, la garantie ne vaut que pour ce découpage. Exactement ce qu'il fallait
  écrire.
- **§6.2, DP** (l. 751-777). La prédiction réfutée est annoncée en titre, la supériorité de D4
  n'est jamais suggérée, et l'argument est réduit à son noyau théorique (appartenance contre
  liaison d'enregistrement). Solide.
- **§6.3, comparaison honnête** (l. 792-796) : « The unprotected twin was already wrong » — avec
  l'inversion des axes correctement imputée à D4 et non au jumeau. C'est le genre de paragraphe
  qui fait gagner la confiance d'un relecteur.
- **§7.1, reclassement des lignes 9 et 16** (l. 831-835), avec la raison arithmétique donnée. Le
  compte est juste : 17 lignes, 15 « Refuted », 2 « inconclusive ». Conforme à l'INTERDIT de la
  synthèse (ni « seize » ni « quatorze »).
- **§7.3, multiplicité** (l. 867-895). Les IC bootstrap ne sont jamais présentés comme des p
  corrigés, les trois seuils fragiles sont nommés par les auteurs eux-mêmes, et l'absence de
  couverture simultanée est déclarée. Très difficile à attaquer.
- **§4.4 et §9, préenregistrement** (l. 351-358, l. 1031-1033). La formulation exacte exigée par
  la synthèse est employée — « no inversion […] provable for the large majority […] a small
  number committed alongside their results or left unversioned » — et l'absence d'horodatage
  tiers est déclarée aux deux endroits. Honnête et suffisant, sous réserve du dépôt OSF.
- **§7.4, limites établies par un échec de recherche** (l. 897-925), avec la ressource manquante
  nommée précisément. C'est la bonne façon d'écrire une limite.
- **§9, artefact** (l. 1003-1036), et surtout le garde-fou « No artifact figure is a result of
  this study » (l. 1021-1024).
- **§10, AI Use** (l. 1040-1067). Divulgation pleine plutôt qu'étroite, responsabilité humaine
  explicite, et les deux défauts trouvés par relecture adverse nommés. Ce paragraphe travaillera
  en votre faveur — à condition que D1 ne le contredise pas.

---

## Ordre d'exécution suggéré

1. **D1** (15 min) et **D3** (20 min) — chiffres périmés, purement mécanique.
2. **D6** (1 h) — références, plus l'alerte à l'agent LaTeX sur `anon2026decoupling`, plus
   l'entrée AAPOR manquante.
3. **D4** (1 paragraphe) et **D7** (1 phrase) — formulation.
4. **D2** (½ journée) — figure, à coordonner avec l'agent figures.
5. **D5** — décision du responsable, sur le chemin critique : lettres de divulgation, mention
   NORC/licence, titre de la sous-section éthique, phrase sur ce que Park a réellement restreint.
6. **D8** — passe de balayage finale.

Rien de ce qui précède ne remet en cause un résultat. Si les six premiers points sont traités, je
recommanderais l'acceptation sous révision mineure.
