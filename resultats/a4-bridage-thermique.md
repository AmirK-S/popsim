# a4. Bridage thermique sous charge continue : la courbe de dix minutes

Redige le 3 septembre 2026 sur la machine du projet. Ce document leve la limite numero 3
de `resultats/a3-inference-locale.md`, qui disait que la stabilite thermique n'etait pas
mesuree et que la plus longue serie du banc a3 durait 18 secondes.

Convention de lecture :
`[MESURE]` valeur relevee sur cette machine le 3 septembre 2026, rejouable par
`analyses/a4_bridage_thermique.py`, donnees brutes dans `resultats/mesures-a4/` ;
`[ESTIMATION]` calcul derive de mesures, avec la regle de calcul donnee ;
`[HYPOTHESE]` ce qui reste une supposition, y compris quand elle est raisonnable.

Aucune donnee d'enquete n'est entree dans un modele. Le persona et les questions sont
factices et fabriques par le script avec une graine fixe, importes de
`a3_banc_inference.py` pour etre identiques a ceux du banc a3.

---

## 0. La reponse, en huit lignes

Sur dix minutes de charge continue, avec la configuration de reference du rapport a3 et
Qwen3-4B en 4 bits :

- premiere minute **22 023 appels par heure**, 163,5 ms par appel ; [MESURE]
- dixieme minute **13 385 appels par heure**, 269,0 ms par appel ; [MESURE]
- **perte de 39,2 pour cent** ; [MESURE]
- **la courbe n'etait pas stabilisee.** Sur les cinq dernieres minutes elle descendait
  encore de 387 appels par heure par minute, intervalle de confiance a 95 pour cent
  [455 ; 320] en baisse, t egal a moins 11,3 sur 1 036 appels. [MESURE]

**Dix minutes ne suffisent donc pas a estimer le regime etabli.** Toute duree obtenue en
appliquant ce facteur aux chiffres de la phase 1 est un **plancher optimiste, pas une
prevision.**

---

## 1. Pourquoi la question se pose sur cette machine, et pas sur une autre

Le rapport a3 decrivait la machine comme "un portable de 14 pouces". C'etait faux, et la
correction a ete portee dans a3 section 6, limite 3. La machine est un **Mac17,3**, c'est
a dire un **MacBook Air M5**, et il n'existe pas de MacBook Air 14 pouces. [MESURE,
`sysctl -n hw.model` rend `Mac17,3`]

La diagonale de l'ecran n'etait de toute facon pas le sujet. Le sujet est le
refroidissement, et il est le suivant : **cet Air n'a pas de ventilateur.** La chaleur
sort par le chassis, en convection passive. Un MacBook Pro monte ses ventilateurs et tient
un regime eleve pendant des heures ; un Air ne le peut pas, par construction. Le banc a3
mesurait des series de 10 a 18 secondes, c'est a dire uniquement le regime de rafale, celui
ou le SoC depense son budget thermique accumule. Toutes les durees de la phase 1 annoncees
en a3 section 5.1 reposaient donc, implicitement, sur l'hypothese que le debit des dix
premieres secondes valait pour les sept heures suivantes. C'est cette hypothese que ce
rapport teste.

Configuration de la machine, relevee et non recopiee : Mac17,3, puce Apple M5, 10 coeurs,
32 Gio, macOS 26.5.2 build 25F84. [MESURE]

---

## 2. L'etat de la machine avant la mesure

C'est la regle inscrite dans a3 section 1.3 apres l'incident iCloud : une mesure prise
pendant que des demons systeme travaillent sous-estime le debit de 40 pour cent, et une
campagne entiere a du etre jetee pour cette raison. Le script a4 refuse donc de mesurer si
la machine n'est pas au repos, et consigne l'etat au lieu de le supposer.

**La regle a servi des le premier essai.** Un lancement a 14 h 46 a ete refuse par le
script : `bird`, le demon de synchronisation iCloud Drive, occupait 31,8 pour cent d'un
coeur, reveille par l'ecriture du script lui-meme dans un dossier du Bureau. Le script a
attendu, et la mesure n'a demarre qu'une fois la machine revenue au repos. [MESURE]

Etat retenu, au demarrage de la campagne de mesure, 14 h 57 :

| Indicateur | Valeur | Source |
|---|---|---|
| Charge moyenne 1, 5, 15 minutes | **3,22 / 2,64 / 2,37** sur dix coeurs | `os.getloadavg` |
| Alimentation | **secteur**, batterie a 100 pour cent, chargee | `pmset -g batt` |
| Avertissement thermique | **aucun enregistre** | `pmset -g therm` |
| Avertissement de performance | **aucun enregistre** | `pmset -g therm` |
| Bridage CPU publie | **aucun enregistre** | `pmset -g therm` |
| Temperature de la batterie | **30,35 degres** | `ioreg -rc AppleSmartBattery` |

Processus au dessus de 5 pour cent d'un coeur, echantillonnes a l'instant du releve :
`WindowServer` 9,7, `top` 7,8 qui est la sonde elle-meme, `WallpaperAerials` 7,5 qui est le
fond d'ecran anime, `kernel_task` 6,0. **Aucun demon iCloud, aucun demon d'indexation,
aucun antivirus.** [MESURE] La charge de 3,22 est dans la plage 2,0 a 3,2 relevee comme
plage de repos pendant toute la campagne a3.

Une reserve a noter et non a cacher : `WallpaperAerials`, le fond d'ecran anime, consomme
en permanence quelques pour cent d'un coeur et une part du GPU. Il etait present a la
premiere minute comme a la dixieme, donc il ne biaise pas la **tendance**, qui est l'objet
de ce rapport. Il abaisse en revanche legerement le **niveau** absolu. [ESTIMATION]

Alimentation secteur : c'est indispensable. Sur batterie, macOS bride deliberement, et la
mesure ne porterait plus sur la thermique mais sur la politique d'energie. Le script
refuse de mesurer sur batterie.

---

## 3. Protocole

### 3.1 La configuration du serveur

Celle du rapport a3 section 4.7, ligne "Reference", qui donne le **meilleur debit absolu**
de tout le balayage, 24 104 appels par heure a un flux. Les options sont recopiees, pas
reinventees :

```
llama-server -m data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
    --host 127.0.0.1 --port 8097 \
    -c 131072 -np 8 -ngl 999 --cache-reuse 256 --no-webui -fa on \
    --slot-save-path /tmp/a3-slots \
    --cache-type-k q8_0 --cache-type-v q8_0
```

Interroge par **un seul flux**, ce qui est la condition du meilleur chiffre de a3 : le
traitement par lots ne rapporte rien sur cette machine et coute meme du debit a huit slots.

### 3.2 La charge

Elle est celle de la phase 1, et non un test de synthese :

- un persona factice de **3 029 tokens** en tete, fige, identique octet pour octet d'un
  appel a l'autre pour que le cache de prefixe fonctionne ;
- des questions fermees a cinq modalites de **66 tokens**, en queue, cinquante questions
  differentes tournant en boucle ;
- un seul passage avant par appel, `n_predict` a 1, `n_probs` a 40, temperature nulle,
  `cache_prompt` actif. C'est exactement la primitive du protocole popsim : on ne genere
  pas, on lit la distribution du token de reponse ;
- deux appels de chauffe non comptes avant le premier chronometre, pour que la premiere
  fenetre mesure le regime etabli et non le prefill initial.

Une fois par fenetre, deux sondes s'ajoutent a la boucle :

- **un prefill a froid** du persona entier, `cache_prompt` a faux, sur un second persona
  range dans un autre slot pour ne pas evincer le cache chaud. C'est la partie
  la plus dependante du calcul GPU, donc la plus sensible au bridage, et c'est aussi ce
  que la phase 1 paie 900 fois ;
- **une sonde de decodage** de 32 tokens. Elle est necessaire parce qu'un appel a
  `n_predict` egal 1 ne donne aucun temps de generation exploitable : llama.cpp compte ce
  token unique dans le temps de prompt et rapporte un temps de generation voisin de zero.
  La premiere version de ce script affichait de ce fait un decodage a un million de tokens
  par seconde, ce qui a ete corrige avant la campagne.

Total effectivement traite : **2 300 appels comptes**, plus 10 prefills a froid et 10
sondes de decodage, en dix minutes sans interruption. [MESURE]

### 3.3 Les indicateurs de bridage, sans sudo

La consigne interdit `sudo`, ce qui exclut `powermetrics`, seul outil qui donne
directement la frequence et la puissance du GPU. Trois indicateurs restent accessibles a
un utilisateur ordinaire, et il faut dire ce que chacun vaut.

| Indicateur | Commande | Verdict d'usage |
|---|---|---|
| Avertissements thermiques et `CPU_Speed_Limit` | `pmset -g therm` | **inutilisable ici**, voir ci-dessous |
| Temperature de la batterie, en centiemes de degre | `ioreg -rc AppleSmartBattery`, champ `Temperature` | **c'est celui qui a servi** |
| Charge moyenne du systeme | `os.getloadavg` | utile comme controle de purete, pas comme indicateur thermique |

**`pmset -g therm` n'a rien publie de toute la campagne.** Ni avertissement thermique, ni
avertissement de performance, ni `CPU_Speed_Limit`, avant, pendant ou apres les dix
minutes. [MESURE] Ce n'est pas la preuve d'une absence de bridage : `pmset` ne parle que du
CPU et ne rapporte que les brides declenchees par un evenement systeme, typiquement un
chargeur insuffisant ou une alerte thermique franche. Une reduction progressive de la
frequence du GPU Metal par la gestion d'energie ne s'y voit pas. **Conclusion a retenir
pour la suite du projet : sur cette machine, `pmset -g therm` ne detecte pas le bridage
GPU. Ne pas s'en servir comme feu vert.** [MESURE]

**L'indicateur qui a servi est la temperature de la batterie**, lue par
`ioreg -rc AppleSmartBattery`, champ `Temperature`, en centiemes de degre. Aucun privilege
requis. Ce n'est pas la temperature du SoC : la batterie est une grosse masse thermique
collee au chassis, elle repond avec un retard de plusieurs minutes et une amplitude
ecrasee. Mais sur un Air sans ventilateur, le chassis **est** le radiateur, donc cette
valeur suit la chaleur reellement evacuee. Elle sert d'indicateur de tendance et d'etat
d'equilibre, jamais de mesure de jonction. [MESURE pour la valeur, ESTIMATION pour
l'interpretation]

---

## 4. Les mesures, fenetre par fenetre

Dix fenetres d'une minute, dix points. Toutes les valeurs sont des [MESURE].

| Minute | Appels | Appels/h | Latence moy. | Ecart-type | Prefill a froid t/s | Prefill du delta t/s | Decodage t/s | Charge | Batterie |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 338 | **22 023** | 163,5 ms | 5,2 | 801,6 | 399,1 | 38,6 | 2,44 | 30,42 |
| 2 | 285 | 18 682 | 192,7 ms | 17,0 | 730,8 | 336,1 | 38,0 | 2,58 | 30,50 |
| 3 | 215 | 14 606 | 246,5 ms | 48,4 | 506,5 | 261,6 | 35,2 | 2,18 | 30,56 |
| 4 | 212 | 14 782 | 243,5 ms | 32,9 | 432,7 | 265,6 | 27,0 | 1,60 | 30,60 |
| 5 | 215 | 14 587 | 246,8 ms | 36,3 | 542,9 | 263,0 | 34,2 | 1,64 | 30,65 |
| 6 | 218 | 14 964 | 240,6 ms | 31,9 | 476,5 | 270,1 | 32,6 | 2,55 | 30,67 |
| 7 | 215 | 14 504 | 248,2 ms | 51,1 | 544,3 | 259,8 | 33,4 | 2,42 | 30,70 |
| 8 | 210 | 14 235 | 252,9 ms | 47,7 | 537,4 | 255,0 | 34,1 | 1,52 | 30,73 |
| 9 | 199 | 13 546 | 265,8 ms | 64,8 | 518,5 | 242,4 | 32,9 | 2,32 | 30,75 |
| 10 | 193 | **13 385** | 269,0 ms | 26,5 | 438,6 | 239,4 | 31,6 | 1,62 | 30,77 |

Etat thermique rapporte par `pmset -g therm` a chaque fenetre : identique aux dix
fenetres, *No thermal warning level has been recorded*, *No performance warning level has
been recorded*, *No CPU power status has been recorded*. `CPU_Speed_Limit` jamais publie.
[MESURE]

Charge moyenne du systeme : entre **1,52 et 2,58** pendant toute la campagne. [MESURE]
Elle ne monte pas, elle baisse plutot, ce qui est logique puisque la charge de travail est
un seul flux GPU. **Aucun demon systeme ne s'est reveille pendant les dix minutes**, donc
l'explication par contention exterieure est ecartee.

Empreinte memoire du serveur, RSS : entre 12 263 et 12 501 Mo, sans tendance. [MESURE]
**Aucune fuite, aucune derive logicielle.** La degradation n'est donc pas un effet
d'accumulation dans le serveur, ce qui laisse le materiel comme explication.

Figure : `resultats/a4-bridage-thermique.png` et `.svg`, axes en francais.

---

## 5. Analyse

### 5.1 La perte

**Premiere minute 22 023 appels par heure, derniere minute 13 385, soit une perte de
39,2 pour cent.** [MESURE]

Une note d'honnetete sur ce chiffre : il **sous-estime** la perte reelle par rapport a un
depart froid. Le rapport a3 section 4.7 mesure 24 104 appels par heure sur la meme
configuration a un flux, sur une rafale de quelques secondes. Notre premiere fenetre est
deja une moyenne sur soixante secondes de charge, prefill a froid compris, et elle ne
donne que 22 023. Rapportee au chiffre de rafale de a3, la perte au bout de dix minutes
est de **44,5 pour cent**. [ESTIMATION, rapport de deux mesures faites dans deux
campagnes differentes]

### 5.2 Les trois debits ne se degradent pas de la meme facon, et cela dit quelque chose

| Grandeur | Minute 1 | Minute 10 | Perte |
|---|---|---|---|
| Prefill a froid, 3 069 tokens d'un coup | 802 t/s | 439 t/s | **45,3 %** |
| Prefill du delta de question, 66 tokens | 399,1 t/s | 239,4 t/s | **40,0 %** |
| Decodage, generation de 32 tokens | 38,6 t/s | 31,6 t/s | **18,2 %** |

[MESURE] Le prefill est limite par le calcul, le decodage est limite par la bande passante
memoire. **Le calcul perd deux fois et demie plus que la bande passante.** C'est la
signature d'une reduction de la frequence et de la puissance du GPU, et non d'un
ralentissement de la memoire. [ESTIMATION, deduction du profil de degradation, non
verifiee directement faute d'acces a `powermetrics` sans sudo]

Consequence pratique importante, et elle est desagreable : c'est la partie **prefill** du
travail qui souffre le plus, or la phase 1 est majoritairement du prefill. Les 900
prefixes de persona et les 45 000 deltas de question sont tous du prefill. Le protocole
popsim, qui ne genere presque rien, est donc dans le pire cas de figure vis a vis du
bridage.

### 5.3 Le point decisif : la courbe s'etait elle stabilisee ?

**Non. Elle descendait encore a la dixieme minute.**

La courbe a deux regimes, et c'est le fait le plus important du rapport.

**Regime 1, minutes 1 a 3 : effondrement rapide.** De 22 023 a 14 606 appels par heure,
soit moins 33,3 pour cent en deux minutes. [MESURE] C'est le budget thermique de rafale
qui s'epuise.

**Regime 2, minutes 3 a 7 : un plateau tres net.** Moyenne 14 689 appels par heure,
ecart-type entre fenetres de 165, soit **1,1 pour cent de dispersion**. [MESURE] Cinq
points quasiment alignes. **Un banc qui se serait arrete a sept minutes aurait conclu, a
juste titre en apparence, que le regime etabli est atteint a moins 33 pour cent.**

**Regime 3, minutes 8 a 10 : la descente reprend.** 14 235 puis 13 546 puis 13 385. La
moyenne des trois dernieres fenetres est de 13 722, soit **8,9 pour cent sous le
plateau** des minutes 3 a 7. [MESURE]

Le test formel, sur les appels individuels et non sur les dix points de fenetre, pour
avoir de la puissance statistique :

| Fenetre d'ajustement | Pente | IC 95 pour cent | t | n appels |
|---|---|---|---|---|
| 5 dernieres minutes | **moins 387 appels/h par minute** | [moins 455 ; moins 320] | **moins 11,3** | 1 036 |
| 4 dernieres minutes | moins 417 | [moins 515 ; moins 320] | moins 8,4 | 818 |
| 3 dernieres minutes | moins 419 | [moins 566 ; moins 271] | moins 5,6 | 603 |
| 2 dernieres minutes | moins 126 | [moins 391 ; plus 140] | moins 0,9 | 393 |

[MESURE] La pente est **negative et tres significative** sur les cinq, quatre et trois
dernieres minutes. Elle ne l'est plus sur les deux dernieres, mais deux minutes ne
contiennent pas assez de duree pour distinguer une pente de moins 126 du bruit :
l'intervalle de confiance y couvre tout, de moins 391 a plus 140. **Cette derniere ligne
n'est pas un signe de stabilisation, c'est un manque de puissance.** L'interpreter comme
une stabilisation serait exactement l'erreur que ce rapport doit eviter.

Rapportee au niveau final, la pente de moins 387 appels par heure par minute represente
**2,9 pour cent du debit perdu par minute**, encore, a la dixieme minute.

**Le thermometre dit la meme chose.** La temperature de la batterie monte de 30,35 degres
avant la charge a 30,77 degres a la dixieme minute, et 30,78 apres l'arret du serveur.
[MESURE] Sur les cinq dernieres minutes, la pente vaut **plus 0,025 degre par minute**,
avec un t de 16,4 : elle est parfaitement lineaire, **sans aucun signe d'inflechissement**.
Une masse thermique qui approche son equilibre voit sa pente s'aplatir. Celle-ci ne
s'aplatit pas. Le chassis n'avait pas fini de chauffer quand la mesure s'est arretee.
[ESTIMATION, lecture d'une courbe de temperature]

**Verdict. La courbe n'etait pas stabilisee a la dixieme minute. Dix minutes ne suffisent
pas a estimer le regime etabli de cette machine. Toute extrapolation a sept heures a
partir de cette mesure est un plancher optimiste, pas une prevision.**

---

## 6. Traduction sur les durees de la phase 1

### 6.1 La regle de calcul, reprise de a3 section 5.1

`duree totale = 900 prefixes x (3 029 tokens / debit de prefill) + 45 000 appels x (ms par appel)`

Les deux durees de reference du rapport a3, decomposees :

| Modele | Prefixes | Appels | Total a3 |
|---|---|---|---|
| Qwen3-4B, llama.cpp | 0,96 h | 2,49 h | **3 h 27** |
| Llama-3.1-8B, llama.cpp | 2,50 h | 4,55 h | **7 h 03** |

Le facteur mesure n'est pas applique en bloc, mais separement aux deux termes, parce que
le prefill et le regime etabli ne se degradent pas au meme rythme, voir section 5.2.

### 6.2 Deux scenarios, qui sont deux planchers

**Scenario A, le plateau des minutes 3 a 7 se maintient pour toujours.** Facteurs mesures
0,624 sur le prefill a froid et 0,662 sur le regime etabli.

**Scenario B, le niveau de la dixieme minute se maintient pour toujours.** Facteurs
mesures 0,547 et 0,600.

| Modele | a3, sans bridage | Scenario A | Scenario B |
|---|---|---|---|
| Qwen3-4B, llama.cpp | 3 h 27 | **5 h 18** (x1,54) | **5 h 54** (x1,71) |
| Llama-3.1-8B, llama.cpp | 7 h 03 | **10 h 53** (x1,54) | **12 h 09** (x1,72) |

[ESTIMATION, application de facteurs mesures a un modele de duree lui-meme mesure]

### 6.3 La fourchette a retenir, et ce qu'elle est vraiment

**Qwen3-4B : entre 5 h 20 et 5 h 55.**
**Llama-3.1-8B : entre 10 h 50 et 12 h 10.**

**Ces deux fourchettes sont des fourchettes de planchers, pas des previsions.** Leur borne
haute suppose que la degradation s'arrete exactement la ou elle en etait a la dixieme
minute. Or la mesure dit qu'elle ne s'y arretait pas. La vraie duree est **au dessus** de
ces bornes, d'une quantite que cette mesure ne permet pas de chiffrer.

Pourquoi je ne donne pas de borne haute. Prolonger lineairement la pente residuelle de
moins 387 appels par heure par minute conduirait a un debit nul en trente-cinq minutes, ce
qui est evidemment faux : un plancher physique existe, la machine ne s'arrete pas. Mais
**rien dans dix minutes de donnees ne dit ou est ce plancher.** Fabriquer une borne haute
demanderait de supposer une forme de courbe, exponentielle amortie ou autre, que la mesure
ne contraint pas. **Je ne peux pas conclure sur le regime etabli, et c'est la reponse
honnete.**

### 6.4 Une reserve qui porte sur la moitie du tableau

**Le facteur de degradation a ete mesure sur Qwen3-4B uniquement.** L'appliquer a
Llama-3.1-8B est une [HYPOTHESE], pas une mesure. Deux raisons de s'en mefier, et elles
vont en sens contraire :

- le 8B est plus lourd, il tient le GPU occupe plus longtemps par appel et pourrait
  chauffer davantage, donc brider plus ;
- le 8B est davantage limite par la bande passante memoire que par le calcul, or c'est le
  calcul qui perd le plus, voir section 5.2. Il pourrait donc brider moins.

Les deux effets existent, aucun n'est chiffre. La ligne Llama-3.1-8B du tableau ci-dessus
doit etre lue comme un ordre de grandeur, pas comme un resultat. **Elle demande sa propre
mesure**, et le script la fait avec `--modele` pointant sur le fichier du 8B.

---

## 7. Ce que ce test ne dit pas, et le test qu'il faut faire

Sept limites, listees ici parce qu'un relecteur les trouverait de toute facon.

1. **Dix minutes couvrent 2,8 pour cent d'une phase 1 sur Qwen3-4B, et 1,4 pour cent sur
   Llama-3.1-8B.** La duree du test a ete imposee a dix minutes par la consigne de la
   mission. Ce rapport n'est pas une mesure du regime etabli, c'est une mesure du
   **transitoire**, et il montre precisement que le transitoire n'etait pas fini.
2. **Le plateau des minutes 3 a 7 est un piege demontre.** Cinq fenetres a 1,1 pour cent
   de dispersion ressemblent a s'y meprendre a un regime etabli, et les trois fenetres
   suivantes le dementent. C'est l'argument le plus fort contre les tests courts, et il
   vaut aussi contre un test de vingt ou trente minutes : rien ne garantit qu'un troisieme
   palier n'attend pas plus loin.
3. **Une seule execution, pas de repetition, donc pas d'intervalle de confiance entre
   executions.** Meme limite que le banc a3. Les intervalles donnes en section 5.3 portent
   sur la dispersion **a l'interieur** de cette execution.
4. **Aucun acces a la frequence ni a la puissance du GPU.** `powermetrics` demande `sudo`,
   ce que la consigne interdit. L'attribution de la degradation a une baisse de frequence
   GPU est une deduction du profil prefill contre decodage, pas une observation.
   [ESTIMATION]
5. **La temperature de la batterie est un capteur lent et decale.** Elle etablit que le
   chassis chauffait encore, ce qui est le point utile, mais elle ne mesure pas la
   jonction du SoC et ne permet aucun calcul thermique.
6. **Le fond d'ecran anime tournait pendant toute la mesure.** Il abaisse le niveau absolu
   de quelques pour cent. Il ne peut pas expliquer une tendance, puisqu'il est constant.
   Pour une mesure de niveau, et non de tendance, il faudrait le desactiver.
7. **Conditions ambiantes non consignees.** Temperature de la piece, position de la machine,
   surface d'appui. Sur un portable a refroidissement passif ces trois facteurs comptent
   autant que le reglage du serveur, et aucun n'a ete controle ici.

### Le test qu'il faut faire, et combien de temps il prend

**Une heure minimum, une heure et demie a deux heures de preference.** [ESTIMATION]
Le raisonnement, pour qu'il soit critiquable : le premier palier est atteint en 3 minutes,
le second commence vers 8 minutes, et la temperature du chassis montait encore lineairement
a 10 minutes sans le moindre inflechissement. La constante de temps d'un chassis en
aluminium a refroidissement passif se compte en dizaines de minutes. Il faut donc mesurer
jusqu'a ce que **la pente de la temperature de la batterie s'annule**, ce qui est le
critere d'arret objectif a retenir, et non une duree fixee a l'avance.

Le script accepte deja cette duree sans modification :

```
python3 analyses/a4_bridage_thermique.py --minutes 90
python3 analyses/a4_bridage_thermique.py --minutes 90 \
    --modele data/modeles/gguf/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf
```

Et le test definitif, celui qui ne demande aucune extrapolation, existe : **faire tourner
la phase 1 en entier une fois, de bout en bout, et chronometrer.** Elle ne coute rien
d'autre qu'une nuit de machine. Toute la difficulte de ce rapport vient de ce qu'on essaie
de deviner le resultat d'une experience de six heures a partir de dix minutes. La reponse
la plus economique reste de faire l'experience.

---

## 8. Ce qu'il faut retenir pour le plan de travail

**La conclusion strategique de a3 n'est pas renversee.** La machine locale suffit toujours,
et la phase 1 tient toujours dans une nuit sur Qwen3-4B. Le rapport de 1 a 30 avec les
paliers gratuits d'API n'est pas menace par un facteur 1,7.

**Ce qui change, c'est la marge.** La phrase de a3, "la phase 1 est une nuit de calcul, pas
une semaine", devient : **une nuit sur le petit modele, et deux nuits sur le 8B.** Les
7 h 03 annonces pour Llama-3.1-8B ne rentrent plus dans une nuit une fois le bridage pris
en compte : la fourchette de planchers commence a 10 h 50, et la vraie valeur est au dessus.
La recommandation de a3 section 7, le couple Llama-3.1-8B plus gpt-oss-20b pour 13 heures,
est a rebudgeter a **au moins 20 heures**. [ESTIMATION, application du meme facteur a
gpt-oss-20b, qui n'a pas ete mesure]

**Trois consequences operationnelles.**

1. **Toute annonce de capacite hebdomadaire de a3 section 5.2 est a diviser par 1,7 environ,
   et le resultat reste un plancher.** Les 730 000 appels par semaine sur Qwen3-4B
   deviennent au plus 430 000 ; les 357 000 sur Llama-3.1-8B deviennent au plus 210 000.
   [ESTIMATION]
2. **Le decoupage du travail en tranches avec des pauses merite d'etre teste.** Le budget de
   rafale se reconstitue quand la machine refroidit. Un decoupage en tranches de trois
   minutes suivies de pauses tournerait a plus de 18 000 appels par heure pendant les
   tranches, mais la duree d'horloge totale depend entierement du temps de refroidissement,
   qui n'est pas mesure ici. C'est une piste, pas une recommandation. [HYPOTHESE]
3. **Ne jamais rechronometrer une configuration sur une rafale de dix secondes.** Le
   balayage de a3 section 4.7, qui classe quatre configurations de serveur, a ete fait en
   regime de rafale. Rien ne garantit que le classement tienne en regime bride, puisque
   le prefill et le decodage se degradent a des rythmes differents. **Ce classement est a
   refaire sous charge continue avant de figer la configuration de production.**

---

## Rejouer ce rapport

```
python3 analyses/a4_bridage_thermique.py --minutes 10
```

Le script releve l'etat de la machine, **refuse de mesurer si elle n'est pas au repos**,
lance et arrete `llama-server` lui-meme, ecrit les mesures brutes dans
`resultats/mesures-a4/a4-<horodatage>.json` et trace la figure. Duree : dix minutes plus
une trentaine de secondes. Aucun `sudo`, aucun acces reseau, aucune donnee d'enquete.
