# R2b, amendement a la regle d'arret memoire

**Ecrit le 9 septembre 2026 a 13:28:00 CEST, APRES avoir vu la premiere mesure et APRES que
la regle preenregistree a fait feu.** Ce document n'est donc **pas** preenregistre, et il
est ecrit dans un fichier separe pour que `resultats/r2b-preenregistrement.md` reste tel
qu'il a ete horodate a 13:19:38, sans une seule retouche. Quiconque lit R2b doit lire les
deux pages, et savoir que celle ci est venue apres.

---

## 1. Ce qui s'est passe, sans arrangement

| horodatage | fait [MESURE] |
|---|---|
| 13:19:38 | swap utilise **6 632 Mio** sur 8 192 Mio de swap total, avant tout lancement. Ecrit dans la page de plan section 5 |
| 13:24:26 | run lance, sonde memoire armee, seuil preenregistre 10 240 Mio |
| 13:24:40 | serveur pret en 14,1 s. Swap utilise **12 256 Mio**. Le seuil est deja franchi par le seul chargement du fichier de 11,3 Gio |
| 13:24:54 | sonde de gabarit `answer` 0,9669, `brut` 0,9997 ; variante `answer` retenue, celle de R2 |
| 13:25:08 | smoke test de 20 appels : masse mediane **0,9615**, minimale 0,9472, modalites absentes 0,00, **passe** |
| 13:25:26 | la sonde memoire lit **12 531 Mio**, pose `data/traces/STOP` |
| 13:25:33 | la boucle relit le fichier entre deux appels, ecrit `ARRET DEMANDE`, ferme sa trace sur une ligne entiere, arrete le serveur, ecrit son resume et sort. **38 appels ecrits, 0 rejet, 0 personne complete** |

La regle a fonctionne exactement comme elle etait ecrite, et le mecanisme d'arret a
fonctionne exactement comme `analyses/README.md` le decrit : arret entre deux appels, trace
fermee, serveur arrete, aucune ligne tronquee. C'est la premiere fois qu'un run du dossier
s'arrete proprement sur un critere de machine, et c'est justement le manque qui avait coute
dix sept minutes dans la nuit du 8 au 9.

**Ce qui est en cause n'est pas le mecanisme, c'est l'instrument de mesure.**

---

## 2. Pourquoi le seuil etait mal pose, et la preuve

`sysctl vm.swapusage`, champ `used`, **ne mesure pas la pression memoire courante : il mesure
l'occupation du fichier d'echange, et macOS ne retrecit pas ce fichier.** Mesure directe,
prise **apres** l'arret du serveur et alors qu'**aucun** `llama-server` ne tourne sur la
machine [MESURE, 13:26:17] :

| quantite | avant le run, 13:19 | serveur charge, 13:24 | **serveur arrete, 13:26** |
|---|---|---|---|
| `vm.swapusage used` | 6 632 Mio | 12 256 Mio | **12 426 Mio** |
| `vm.swapusage total` | 8 192 Mio | 13 312 Mio | 13 312 Mio |
| pages occupees par le compresseur | 482 849 | non releve | **272 871** |
| `memory_pressure`, memoire libre systeme | non releve | non releve | **76 pour cent** |

Trois lectures. [MESURE]

1. **Le swap utilise n'a pas baisse d'un Mio quand la charge est partie.** Le processus est
   mort, le serveur est arrete, et le compteur reste a 12,4 Go. Un compteur qui ne descend
   jamais ne peut pas servir de garde fou : une fois franchi, il interdit **tous** les runs
   suivants de la journee, quelle que soit l'etat reel de la machine.
2. **Le compresseur, lui, est redescendu de 482 849 a 272 871 pages**, soit de 7,4 a 4,2 Gio.
   C'est la quantite qui suit vraiment la charge.
3. **`memory_pressure` annonce 76 pour cent de memoire libre systeme** au moment ou le
   compteur de swap affiche 12,4 Go. Les deux chiffres decrivent des choses differentes, et
   c'est le second qui decrit le risque.

**Le seuil de 10 Go etait de surcroit inatteignable a la baisse pour une raison qui n'a rien
a voir avec ce run** : les 6 632 Mio de depart appartiennent aux autres agents qui tournent
sur cette machine depuis 13:18 (charge a une minute mesuree entre 4,3 et 6,0 pendant toute la
sequence). Le fichier de gpt-oss-20b pese 11,3 Gio ; sur une machine de 32 Gio deja occupee,
son chargement pousse mecaniquement 5,9 Go dans le fichier d'echange. **Le franchissement
etait donc certain avant meme le premier appel, et il ne dependait ni de `-np 4`, ni du
comportement du run.**

---

## 3. Ce que cet amendement change, et ce qu'il ne change pas

### Il ne change rien a l'inference

**Aucune quantite statistique n'est touchee.** L'hypothese H1b, le pari ecrit, l'echantillon
de trente personnes et sa graine 20260908, les 58 items, la definition de rarete sur le
perimetre, la partition P_A, le plancher de segment, les 4 000 tirages apparies, les quatre
familles, la correction de Holm, le plancher de lisibilite de 176 personnes et les cinq
predictions accessoires sont **exactement** ceux de la page de plan de 13:19:38. Rien de ce
qui decide le sort du pari ne bouge.

La regle amendee ici est une **regle d'exploitation de la machine**, pas une regle
d'inference. Elle ne peut pas favoriser une issue plutot qu'une autre : elle determine si le
run tourne, jamais ce qu'il mesure. Un lecteur qui voudrait soupconner un choix opportuniste
peut le verifier sur un point : au moment ou cet amendement est ecrit, **aucun contraste n'a
ete calcule**, la trace compte 38 appels sur 1 740 et zero personne complete, donc rien des
resultats n'est connu.

### Il change l'instrument, et le declare

La regle preenregistree etait :

> *« Le swap depasse 10 Go. `sysctl vm.swapusage` est lu toutes les 60 secondes [...] ; au
> dessus de 10 240 Mio utilises, le fichier d'arret est pose. »*

Elle est remplacee, a partir de 13:30 le 9 septembre 2026, par **trois criteres lus toutes
les 60 secondes**, dont deux mesurent la pression reelle et le troisieme la croissance
imputable au run :

1. **Pression memoire systeme.** `memory_pressure`, champ *System-wide memory free
   percentage*, **sous 15 pour cent** : arret. C'est la seule des trois quantites qui monte et
   qui descend avec la charge, et c'est celle que le systeme lui meme emploie.
2. **Croissance imputable au run.** Swap utilise superieur de **plus de 4 096 Mio** a la
   valeur relevee **une fois le serveur pret**, c'est a dire au plateau de chargement : arret.
   Ce critere ignore le fichier d'echange herite des autres agents et ne compte que ce que le
   run ajoute apres son chargement. Le plateau mesure aujourd'hui est de 12 256 Mio, donc le
   declenchement se ferait a 16 352 Mio.
3. **Plafond dur.** Swap utilise au dessus de **24 576 Mio**, soit 24 Go : arret, quoi qu'en
   disent les deux autres. C'est le dernier filet, pose bien au dessus des 14 Go de
   l'incident du 7 au 8 septembre parce que le compteur inclut desormais 12,4 Go herites qui
   ne redescendront pas ; en croissance imputable, 24 Go correspond a 12 Go ajoutes par le
   run, soit deux fois le cout de son chargement.

Les trois autres regles d'arret de la page de plan sont **inchangees** : trois heures de run,
fichier `data/traces/STOP`, attente si un `llama-server` tourne deja et interdiction absolue
de le tuer.

### Consequences pratiques

- `data/traces/STOP` pose par la sonde a 13:25:26 est retire par le meme script qui l'a pose,
  conformement a `analyses/README.md` (« celui qui l'a pose le retire »). Le motif du retrait
  est cet amendement, et il est ecrit dans le journal du run.
- Les **38 appels deja ecrits** dans `data/traces/r2b-C3F-gptoss-ext.jsonl` sont conserves.
  L'index de reprise est le couple (pid, item) ; la relance ne les refait pas et ne les
  reecrit pas. Ils ont ete produits avec la meme variante `answer`, le meme gabarit harmony,
  le meme modele et le meme prompt que le reste.
- Le smoke test de 20 appels **est rejoue** par la relance, parce que le script le fait a
  chaque demarrage de serveur et que ce comportement n'est pas modifie. Ses vingt appels
  s'ajoutent a `data/traces/r2-smoke-r2b.jsonl`, qui est une trace **separee** de celle du
  run : ils n'entrent dans aucune mesure. Les deux passages du smoke test sont publies dans
  le rapport, cote a cote, ce qui donne accessoirement un controle de reproductibilite de la
  masse de probabilite entre deux chargements du meme modele.
- Cet amendement, la sequence horaire ci dessus et la mesure du compteur qui ne redescend pas
  sont repris **en toutes lettres** dans `resultats/r2b-resultats.md`, section « Ce qui a
  tourne », et dans « Ce que je n'ai pas pu verifier ».

---

## 4. Ce qu'il aurait fallu ecrire a 13:19, et qui n'a pas ete ecrit

Par honnetete envers le lecteur qui jugera la discipline du dossier : la page de plan de
13:19:38 **avait releve** le chiffre de depart de 6 672 Mio et **avait ecrit** que le seuil
« peut etre atteint ». Elle n'en a pas tire la conclusion qui s'imposait, a savoir qu'un
modele de 11,3 Gio sur une machine de 32 Gio deja a 6,6 Go de swap franchirait le seuil au
chargement, avant le premier appel. **C'est une faute de calcul faite avant le run, pas une
decouverte faite apres.** Elle a coute une minute de machine et elle est ecrite ici pour
qu'un lecteur puisse la compter contre nous.

Le point qui n'etait pas previsible, en revanche, est le comportement du compteur : que
`vm.swapusage used` ne redescende pas quand la charge disparait est un fait de macOS qu'il a
fallu mesurer, et la mesure est au tableau de la section 2.

---

*Fin de l'amendement. Horodatage : 9 septembre 2026, 13:28:00 CEST. Ecrit apres le
declenchement de la regle et avant la relance du run. Aucun contraste n'etait calcule a cet
instant. Ni cette page ni la page de plan n'ont ete deposees hors machine.*
