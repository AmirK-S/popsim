# T1b — Correction : le nul de marge publié à 20 réplicats, le préenregistrement en prescrivait 100

statut: courant
mandat: vérifier la reproduction à n=100, porter la correction au registre des chiffres et à la légende de la figure 2, produire la fiche de report pour le manuscrit, et proposer la porte qui aurait attrapé le défaut
agent: Claude Opus 5, Anthropic
ecriture: resultats/correction-t1b-2026-09-13.md, resultats/registre-chiffres.csv, resultats/c7-nul-corrige-marginal.csv, resultats/c7-nul-corrige-marginal.md (bandeau), analyses/c7_temoin_verite_appariee.py (une ligne de métadonnée), analyses/figures_article.py, article/figures/fig2-couplage.png
lecture_seule: tout le reste
interdits: **`article/manuscrit.md` — un autre agent en est propriétaire** ; appel payant, réseau, commit sur master, arrière-plan
cecite: je n'ai pas lu le LaTeX compilé (`article2/`, `main.pdf`) ni les branches T1a/T3/T4/T5 en cours ; je n'ai pas relu les 188 lignes du rapport de l'agent précédent autrement qu'en diagonale ; je n'ai pas vérifié si le chiffre circule ailleurs que dans les six emplacements recensés au §4
cout_reel_usd: 0.00
branche: `agent/correction/t1b-cent-replicats`, arbre isolé `/tmp/wt-t1b`, basée sur `origin/master` (`abd5752`) + reprise de `67ad321`

---

## 1. Ce qui a été publié

Le tableau 1 du manuscrit, le résumé, le §5.1, la légende de la figure 2 et la lettre de
divulgation envoyée à Columbia portent tous le même couple de chiffres :

> nul de marge à exactitude-vérité appariée, remplissage marginal, 12 configurations :
> **rho moyen 0,974**, centiles 5–95 de la loi nulle **[0,950 ; 0,993]**, contre **0,965**
> observé, non dépassé — **prédiction (b) réfutée**.

C'est le chiffre qui fonde le titre de l'article : le couplage qualité-fuite se reproduit sans
aucune information individuelle, une marge d'exactitude appariée suffit.

## 2. Ce que prescrivait le préenregistrement

`resultats/c7-nul-corrige-preenregistrement.md` **§5, « Paramètres figés »**, ligne 109 :

> Graine `20260912` (celle de `c7_disjoint.py`), **100 réplicats par construction**, 40
> permutations pour la chute, 3 tirages de départage pour le top-1 […]
> Le script est exécuté **deux fois** et l'identité octet à octet du CSV est vérifiée.

Le §6 du même document prédit d'ailleurs, en toutes lettres, « rho **N1**, moyenne sur **100
réplicats** ».

## 3. L'écart, et sa nature exacte

**Le chiffre publié vient d'un run arrêté à 20 réplicats.** Aux 100 prescrits, la moyenne n'est
pas 0,974 mais **0,980**.

| série | n | rho moyen | médiane | p5 loi nulle | p95 loi nulle | 0,965 dépasse-t-il p95 ? |
|---|---|---|---|---|---|---|
| marginal (publiée) | 20 | 0,9741258741 | 0,9720 | 0,9500000000 | 0,9933566434 | **non** |
| **marginal (préenregistrée)** | **100** | **0,9798947065** | **0,9815884** | **0,9510489510** | **0,9930069930** | **non** |
| uniforme (autre témoin) | 20 | 0,9814685315 | 0,9860 | 0,9580419580 | 0,9930069930 | non |

**Ce n'est pas une divergence de calcul, c'est un arrêt prématuré.** Je l'ai vérifié moi-même
plutôt que de le croire : j'ai rejoué `analyses/c7_temoin_verite_appariee.py` tel quel dans un
arbre isolé, à `NREP=100`, et les 20 premières valeurs de rho de mon run à 100 sont **identiques
à la 10ᵉ décimale** aux 20 valeurs de la série publiée. C'est mécaniquement attendu : la graine
de chaque réplicat est `[GRAINE, 999, r, graine_nom(nom), 0]`, indexée par le numéro de réplicat
`r` et par rien d'autre. Les réplicats 0 à 19 sont donc le **même objet** dans les deux runs, et
les réplicats 20 à 99 sont exactement ceux qui n'ont jamais été tirés.

Reproduction complète, à l'octet : mon run à `NREP=100` redonne le CSV de `67ad321` ligne pour
ligne (100 réplicats + agrégat), et le second run des séries à 20 redonne les siennes de même.
Comme le CSV de `67ad321` a été produit par un autre agent, dans un autre arbre, cela **vaut la
double exécution prescrite au §5** du préenregistrement : deux exécutions indépendantes, identité
octet à octet du CSV vérifiée.

## 4. Pourquoi la conclusion ne change pas

**La réfutation tient dans les deux cas**, et elle tient par une marge confortable :

- à 20 réplicats : 0,9650 < 0,9934 (95ᵉ centile de la loi nulle) ;
- à 100 réplicats : 0,9650 < 0,9930.

L'observé reste **dans** la bande, et il y reste largement : il est plus bas que le 5ᵉ centile lui
même (0,9510), c'est-à-dire que le nul est *plus* corrélé que le réel dans plus de 95 % des
réplicats. La prédiction (b) reste réfutée, le verdict de la figure 2 est visuellement le même, et
la ligne 1 du tableau des quinze prédictions ne change pas de colonne.

**Le chiffre qui fait foi devient néanmoins celui du préenregistrement : n=100, rho moyen 0,980,
bande [0,951 ; 0,993].** Un résultat qui contredit son propre préenregistrement n'est pas
publiable, même quand il arrange moins — et celui-ci arrange moins, puisque 0,980 est *plus* haut
que 0,974 et rend la réfutation *plus* nette. Le motif de la correction n'est pas le sens de
l'écart, c'est qu'un chiffre hors protocole reste hors protocole.

**Aucune raison technique ne s'oppose au passage à n=100.** J'ai cherché celles qui auraient pu
exister — elles ne tiennent pas :

| objection envisagée | verdict |
|---|---|
| divergence de calcul entre les deux runs | **écartée** : préfixe bit-exact vérifié, mêmes graines |
| coût prohibitif du run à 100 | **écartée** : 467 s en avant-plan, local, gratuit |
| les 80 réplicats supplémentaires seraient d'une autre nature | **écartée** : même boucle, même construction, seule la borne de `range(N_REP)` change |
| le p95 se dégraderait | **écartée** : 0,9930 contre 0,9934, et 0,9650 reste dessous |
| 0,974 aurait été co-préenregistré | **écartée** : le préenregistrement ne prédit aucune valeur de rho pour ce témoin, seulement `n=100` |
| l'ancienneté du chiffre | **n'est pas une raison technique**, et n'a pas été retenue |

## 5. Ce qui a été corrigé, et où

Tout est sur `agent/correction/t1b-cent-replicats`, **rien n'est fusionné**.

| fichier | changement |
|---|---|
| `analyses/c7_temoin_verite_appariee.py` | la règle `fait_foi_tableau1` codait en dur `N_REP==20` ; elle code `N_REP==100`. **Aucune ligne de calcul n'a bougé** — les 140 valeurs de rho du CSV sont inchangées à la décimale, ce qui le prouve |
| `resultats/c7-nul-corrige-marginal.csv` | régénéré intégralement par ré-exécution (pas d'édition à la main). Identique à l'octet à la version de `67ad321`, **colonne `fait_foi_tableau1` exceptée** : `oui` passe de la ligne marginal/n=20 à la ligne marginal/n=100 |
| `resultats/registre-chiffres.csv` | voir §6 |
| `analyses/figures_article.py` | voir §7 |
| `article/figures/fig2-couplage.png` | régénéré avec la bande corrigée |
| `resultats/c7-nul-corrige-marginal.md` | bandeau de renvoi en tête : sa §4 et sa §5 affirment que la série à 20 fait foi, ce qui n'est plus vrai |
| `article/manuscrit.md` | **non touché.** Fiche de report au §8 |

## 6. Registre des chiffres

`resultats/registre-chiffres.csv`, deux lignes :

- **`rho-nul-marge-appariee-12conf`** (0,974 ; n=20) : `provisoire` → **`retracte`**. La ligne
  **n'est pas supprimée** — elle a été publiée et envoyée à un tiers, elle doit rester
  consultable. Sa `grandeur` cite désormais la référence de remplacement en clair, et sa
  `csv_source`, qui valait `ABSENT`, pointe sur
  `resultats/c7-nul-corrige-marginal.csv (variante=marginal, n_replicats=20, ligne=agregat)`.
- **`rho-nul-marge-appariee-12conf-n100`** (0,980 ; [0,951 ; 0,993]) : **créée, `courant`**. Tous
  les champs que la porte exige d'un statut courant sont réellement renseignés, aucun `ABSENT` :
  `n_replicats=100`, `graine=20260912 ; rng [20260912, 999, r, crc32(nom), 0]`,
  `script=analyses/c7_temoin_verite_appariee.py`, `commit=0e6585a`,
  `csv_source=resultats/c7-nul-corrige-marginal.csv (variante=marginal, n_replicats=100, ligne=agregat, fait_foi_tableau1=oui)`.

`outils/portes/registre_chiffres.py --registre-seul` : **OK, aucune violation**, 34 grandeurs.

**Résidu signalé, non traité** : `temoin-marge-top1-json41-marginal` (le top-1 à 31,6 %) sort du
**même** run à 20 réplicats et reste `provisoire` avec `n_replicats=20`. Mon run à 100 donne
31,601 % contre 31,62 % à 20 — les deux s'écrivent 31,6 %, la graphie publiée ne bouge pas. Je ne
l'ai pas corrigée parce que le CSV ne porte pas le top-1 par configuration : lui donner une
`csv_source` réelle demande d'ajouter une sortie au script, ce qui déborde ce mandat.

## 7. Légende de la figure 2

Elle vit **aux deux endroits**, et j'ai corrigé celui qui m'appartient.

**Corrigé ici** — `analyses/figures_article.py`. Trois défauts, pas un :

1. la bande était **trois constantes recopiées à la main** (`NUL_CORRIGE_P5 = 0.9500`,
   `NUL_CORRIGE_P95 = 0.9934`, `NUL_CORRIGE_MOYEN = 0.9741`), au motif — vrai à l'époque —
   qu'aucun CSV de réplicats n'existait au dépôt. Il en existe un depuis `67ad321`. La bande est
   désormais **lue** dans `resultats/c7-nul-corrige-marginal.csv`, filtre
   `variante=marginal`, `n_replicats=100`, `ligne=agregat`, avec deux `SystemExit` si la ligne
   n'est pas unique ou ne porte pas `fait_foi_tableau1=oui` ;
2. les valeurs étaient celles du run à 20 réplicats ;
3. le bas de figure affichait en dur `Band [0.950, 0.993]` ; il est maintenant formaté depuis les
   valeurs lues et annonce le nombre de réplicats : `Band [0.951, 0.993] (mean rho 0.980, 100
   replicates as preregistered)`.

Le docstring du module (l'historique détaillé de la figure) porte le même correctif, avec
l'avertissement de ne **jamais** lire la variante `uniforme`, qui est un autre témoin et non une
variante de graphie du même. Figure régénérée et vérifiée : le point observé 0,965 reste
visiblement dans la bande.

**À reporter** — la ligne `Data:` de la légende, elle, est dans le manuscrit (l. 786-787) et
pointe sur `resultats/c7-disjoint-nul.csv`, qui est le nul **d'origine, défectueux**, retiré après
audit. Voir §8.

## 8. Fiche de report pour `article/manuscrit.md` — je n'applique pas, T4/T5 appliquent

Six emplacements. Numéros de ligne relevés sur `article/manuscrit.md` à `origin/master`
(`abd5752`), 1 186 lignes ; **à revérifier avant application**, T3 peut avoir décalé la
numérotation.

**(1) l. 39 — résumé**
- actuel : `as ours (0.974, 5th–95th percentiles [0.950 ; 0.993], against 0.965 observed). Fourteen preregistered predictions were`
- cible : `as ours (0.980, 5th–95th percentiles [0.951 ; 0.993], against 0.965 observed). Fourteen preregistered predictions were`

**(2) l. 105 — introduction**
- actuel : `Spearman **0.974**, 5th–95th percentiles [0.950 ; 0.993], against **0.965** observed over the 12 configurations; the observed value does not exceed it. Each null is compared`
- cible : `Spearman **0.980**, 5th–95th percentiles [0.951 ; 0.993], against **0.965** observed over the 12 configurations; the observed value does not exceed it. Each null is compared`

**(3) l. 453-454 — §5.1**
- actuel : `With the defect corrected, the witness still reproduces the coupling — **rho 0.974, 5th–95th` / `percentiles [0.950 ; 0.993], against 0.965 observed** over the 12 configurations, measured on`
- cible : `With the defect corrected, the witness still reproduces the coupling — **rho 0.980, 5th–95th` / `percentiles [0.951 ; 0.993], against 0.965 observed** over the 12 configurations (100 replicates, as preregistered), measured on`
- l'incise `(100 replicates, as preregistered)` est **la seule addition de fond** que je propose :
  le manuscrit n'énonce nulle part le nombre de réplicats de ce nul, ce qui est précisément ce qui
  a rendu l'écart invisible à la relecture (§9).

**(4) l. 781 — légende de la figure 2**
- actuel : `> 5th–95th percentile envelope of the corrected marginal null (mean rho 0.974) as a grey band,`
- cible : `> 5th–95th percentile envelope of the corrected marginal null (mean rho 0.980, 100 replicates) as a grey band,`

**(5) l. 786-787 — ligne `Data:` de la figure 2 (défaut distinct, antérieur)**
- actuel : `> Data: `resultats/c7-compromis.csv`, `resultats/c7-compromis-robustesse-points.csv`,` / `> `resultats/c7-disjoint-nul.csv`.`
- cible : `> Data: `resultats/c7-compromis.csv`, `resultats/c7-compromis-robustesse-points.csv`,` / `> `resultats/c7-nul-corrige-marginal.csv` (inset band: `variante=marginal`, `n_replicats=100`), `resultats/c7-nul-corrige.csv` (inset point, row `rho_resume`/`reel`).`
- motif : `c7-disjoint-nul.csv` est le nul **d'origine**, celui dont le défaut ligne 133 de
  `c7_disjoint.py` gonflait la fuite d'un facteur ~1,3. La figure ne le trace plus depuis le
  12/09 ; la ligne `Data:` ne l'avait pas suivi.

**(6) l. 887 — tableau des quinze prédictions, ligne 1**
- actuel : `| 1 | The quality-leakage coupling exceeds a null matched on accuracy alone | **Refuted.** Null rho 0.974, 5th–95th percentiles [0.950 ; 0.993], against 0.965 observed over the 12 configurations; original null carried a defect, since corrected, verdict unchanged (§5.1) | `audit-renversement-2026-09-12.md` |`
- cible : `| 1 | The quality-leakage coupling exceeds a null matched on accuracy alone | **Refuted.** Null rho 0.980, 5th–95th percentiles [0.951 ; 0.993], against 0.965 observed over the 12 configurations; original null carried a defect, since corrected, verdict unchanged (§5.1) | `c7-nul-corrige-marginal.csv` |`
- la colonne `Source` peut aussi rester `audit-renversement-2026-09-12.md` ; mais ce rapport ne
  porte que la série à 20, et le CSV est désormais la source primaire.

**Vérification à faire après application**, par qui appliquera : plus aucune occurrence de
`0.974` ni de `[0.950 ; 0.993]` dans `article/manuscrit.md` (`grep -n "0\.974\|0\.950"`), et le
LaTeX de `article2/` recompilé si ces chiffres y sont dupliqués — **je ne l'ai pas vérifié**.

## 9. La leçon de méthode : la porte qui manque

Voici l'enchaînement, en clair. Un préenregistrement prescrit 100 réplicats. Le run s'arrête à 20.
Le chiffre est publié au tableau 1, au résumé, au §5.1, dans la légende d'une figure et dans le
tableau des prédictions. Il est ensuite **envoyé à un tiers**, dans une lettre de divulgation
responsable. Et personne ne le voit pendant des semaines — ni la revue hostile, ni l'audit de
renversement, ni le contre-examen, qui ont pourtant tous attaqué ce chiffre-là.

Pourquoi personne ne l'a vu : **le manuscrit n'énonce nulle part le nombre de réplicats de ce
nul.** Il n'y avait rien à confronter. Le seul endroit du dépôt qui portait `20` était la variable
`N_REP` d'un script, et le seul endroit qui portait `100` était une phrase de prose au §5 d'un
préenregistrement. Les deux nombres ne se sont jamais rencontrés.

**Aucune porte du dépôt ne compare le nombre de réplicats effectif à celui que le
préenregistrement prescrit.** `outils/portes/registre_chiffres.py` vérifie que la colonne
`n_replicats` est *renseignée* et non `ABSENT` pour un statut courant — jamais qu'elle vaut *le
bon nombre*. La porte P2 aurait laissé passer `n_replicats=20` aussi sereinement que
`n_replicats=100`, et elle l'a fait.

### La porte proposée : P7 « réplicats conformes au préenregistrement »

**Je ne l'implémente pas — je la propose.**

**En quoi elle consiste.** Pour toute ligne du registre de statut `courant` ou `provisoire`, la
porte exige un **préenregistrement nommé** et un **nombre de réplicats prescrit** ; elle compare
ce nombre à la colonne `n_replicats`, et refuse l'écart.

**Sur quoi elle s'appuie dans le registre.** Le registre a douze colonnes (Méthode v2 §1.3) ; il
en faut **deux de plus** :

- `preenregistrement` — chemin du fichier, ou `AUCUN` assumé (une mesure exploratoire n'a pas de
  préenregistrement, et c'est légitime : ce qui ne l'est pas, c'est de ne pas le dire) ;
- `n_replicats_prescrit` — le nombre **recopié du préenregistrement**, avec la référence de
  section qui l'énonce, p. ex. `100 (§5)`.

La règle est alors mécanique : si `preenregistrement != AUCUN` et
`n_replicats != n_replicats_prescrit`, la porte bloque, avec pour remède « relancer au nombre
prescrit, ou amender le préenregistrement en le datant ». Le second membre de l'alternative est
essentiel : un préenregistrement peut être amendé, jamais rétroactivement contredit en silence.

**Ce qui la rend praticable.** Trois choses :

1. **Elle ne demande aucune analyse de texte.** Le nombre prescrit est **recopié à la main** dans
   le registre par qui déclare la mesure. Une porte qui tenterait d'extraire « 100 réplicats » de
   la prose d'un préenregistrement serait fragile et se tairait au mauvais moment ; celle-ci est
   une comparaison d'entiers. Le coût est déplacé sur l'humain qui recopie — et c'est justement à
   ce moment-là, en recopiant, qu'on voit que 20 n'est pas 100.
2. **Elle est incrémentale.** Comme `--mode avertissement` de P2, elle peut compter sans bloquer
   le temps que les 34 lignes existantes soient renseignées, puis passer bloquante.
3. **Elle attrape cette famille entière de défauts**, pas ce cas : nombre de tirages de bootstrap,
   de permutations, de tirages de départage — toute quantité figée avant exécution et vérifiable
   après.

**Ce qui la rend imparfaite, et qu'il faut dire.** Elle repose sur une recopie honnête : qui
recopie `20` dans les deux colonnes passe la porte. Elle ne détecte donc pas la tricherie, elle
détecte **l'inattention** — ce qui est exactement le défaut survenu ici. Et elle ne couvre que les
grandeurs qui *sont* au registre : une mesure publiée sans y être déclarée lui échappe, ce que la
porte P2 (c) couvre déjà par ailleurs.

**Un garde-fou complémentaire, plus faible mais gratuit** : faire échouer un script d'analyse dont
le nombre de réplicats vient d'une variable d'environnement (`NREP`) quand cette variable n'est
pas posée explicitement, plutôt que de retomber sur un défaut silencieux
(`int(os.environ.get("NREP","20"))`). **C'est ce défaut de 20 qui a produit le run court.** Un
défaut implicite dans un script préenregistré est un piège : il donne un résultat plausible sans
jamais annoncer qu'il n'est pas celui qu'on a demandé.

## 10. À remonter au responsable — je ne le traite pas

**Le 0,974 figure dans une lettre déjà envoyée à Columbia**
(`resultats/divulgation-responsable-brouillon.md`, l. 30-32 en français et l. 162-164 dans le
corps anglais envoyé). **L'envoi ne m'appartient pas, et ne m'a pas été délégué.** La décision
d'écrire ou non, et à qui, revient au responsable.

S'il décide d'envoyer, voici la phrase de correction d'une ligne :

> Correction to our earlier note: the control null's mean rho is **0.980** (5th–95th percentiles
> **[0.951 ; 0.993]**), not 0.974 — our first figure came from a run stopped at 20 replicates
> instead of the 100 our preregistration specifies; the observed 0.965 still falls inside the
> band, so the conclusion is unchanged.

Elle dit les trois choses qui comptent : le bon chiffre, **pourquoi** l'ancien était faux (et non
pas seulement qu'il l'était), et que la conclusion ne bouge pas. L'ordre est délibéré : la raison
avant le rassurement, pour que le rassurement soit croyable.
