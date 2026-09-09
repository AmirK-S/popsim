# a3. Inference locale : pile installee et debits mesures

Redige le 3 septembre 2026 sur la machine du projet. Ce document remplace par des mesures
les hypotheses de `exploration/06-infrastructure-zero-cout.md`, section 2.2 et section 2.3,
qui portaient toutes la mention "a mesurer".

Convention de lecture, comme dans le reste du dossier :
`[MESURE]` valeur relevee sur cette machine, rejouable par `analyses/a3_banc_inference.py` ;
`[CONFIRME]` fait verifie dans une source primaire, avec l'adresse ;
`[PROBABLE]` deduction solide mais non verifiee directement ;
`[HYPOTHESE]` ce qui reste une supposition.

Rien de ce qui suit n'a coute un euro. Aucune donnee d'enquete n'est entree dans un modele :
le banc fabrique lui-meme un persona factice et cinquante questions factices, avec une
graine fixe, et les deux moteurs tournent en local sans acces reseau sortant.

---

## 1. Ce qui est installe, et comment le desinstaller

### 1.1 Les commandes passees, dans l'ordre

Tout part d'une machine ou, au releve du 2 septembre, ni ollama, ni llama.cpp, ni mlx
n'etaient presents.

```
# 1. Le moteur principal. Metal est compile dans la bouteille Homebrew, rien a construire.
brew install llama.cpp

# 2. L'environnement Python isole. Le .venv du projet preexistait, il a ete reutilise.
uv venv .venv --python 3.12          # deja present, Python 3.13.14 conserve
uv pip install --python .venv/bin/python huggingface_hub
uv pip install --python .venv/bin/python mlx-lm

# 3. Les modeles. HF_HOME est detourne vers le projet pour que tout soit dans un seul
#    dossier supprimable, et data/ est deja dans le .gitignore.
export HF_HOME=$PWD/data/modeles/hf-cache
.venv/bin/hf download unsloth/Qwen3-4B-Instruct-2507-GGUF \
    Qwen3-4B-Instruct-2507-Q4_K_M.gguf --local-dir data/modeles/gguf
.venv/bin/hf download bartowski/Meta-Llama-3.1-8B-Instruct-GGUF \
    Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf --local-dir data/modeles/gguf
.venv/bin/hf download unsloth/Qwen3-30B-A3B-Instruct-2507-GGUF \
    Qwen3-30B-A3B-Instruct-2507-Q4_K_M.gguf --local-dir data/modeles/gguf
.venv/bin/hf download ggml-org/gpt-oss-20b-GGUF \
    gpt-oss-20b-MXFP4.gguf --local-dir data/modeles/gguf
.venv/bin/hf download mlx-community/Qwen3-4B-Instruct-2507-4bit \
    --local-dir data/modeles/mlx/Qwen3-4B-Instruct-2507-4bit
.venv/bin/hf download mlx-community/Meta-Llama-3.1-8B-Instruct-4bit \
    --local-dir data/modeles/mlx/Meta-Llama-3.1-8B-Instruct-4bit
```

Aucun compte, aucun jeton d'authentification, aucune acceptation de licence en ligne n'a
ete necessaire. Les depots `meta-llama/*` sont sous acces conditionnel sur Hugging Face,
mais les conversions GGUF et MLX redistribuees par des tiers ne le sont pas.

### 1.2 Empreinte disque, etape par etape

Espace libre au depart : 592,6 Gio. [MESURE]

| Etape | Ajout | Detail |
|---|---|---|
| `brew install llama.cpp` | 147 Mio | 18,7 Mio pour llama.cpp, le reste en mises a jour de `ggml`, `libomp`, `openssl@3` |
| `mlx-lm` et `huggingface_hub` | 277 Mio | dont 203 Mio pour `mlx` et `mlx-metal`, 53 Mio pour `transformers` |
| Modeles GGUF, quatre fichiers | 34,9 Gio | Qwen3-4B 2,3, Llama-3.1-8B 4,6, Qwen3-30B-A3B 17, gpt-oss-20b 11 |
| Modeles MLX, deux dossiers | 6,3 Gio | Qwen3-4B 2,1, Llama-3.1-8B 4,2 |
| **Total** | **42 Gio**, releve par `du -sh` | sous le plafond de 60 Gio fixe pour la mission |

Note pour qui refera l'operation : l'espace libre releve par `df` a baisse de bien plus que
42 Gio pendant la session, parce que le deplacement des modeles hors du perimetre iCloud fait
transiter les fichiers en double et parce qu'APFS ne rend pas l'espace immediatement. Se fier
a `du` sur le dossier des modeles, pas a la difference de `df`.

### 1.3 Un piege qui a fausse une campagne entiere : le projet est sur le Bureau

Le dossier du projet est sous `~/Desktop`, donc dans le perimetre de synchronisation iCloud
Drive. Deposer 42 Gio de poids de modeles a cet endroit declenche trois demons systeme en
meme temps : `bird` qui tente de televerser les fichiers, `spotlightknowledged` qui les
indexe, et `XProtectRemediatorDolittle` qui les analyse. Releve pendant une campagne de
mesure : 100 pour cent, 88 pour cent et 91 pour cent d'un coeur chacun, charge moyenne du
systeme a 5 a 7 sur une machine censee etre au repos. [MESURE]

Effet sur les chiffres : le debit de prefill de Qwen3-4B tombe de 725 a 414 tokens par
seconde et le decodage de 33 a 22 tokens par seconde, soit **une sous-estimation de 40 pour
cent**. Une campagne entiere a du etre jetee.

Correctif applique, et il fait partie de l'installation :

```
mkdir -p ~/Library/Caches/popsim-modeles
touch  ~/Library/Caches/popsim-modeles/.metadata_never_index
rsync -a --remove-source-files data/modeles/ ~/Library/Caches/popsim-modeles/
rm -rf data/modeles && ln -s ~/Library/Caches/popsim-modeles data/modeles
```

`~/Library/Caches` est hors du perimetre iCloud et hors de l'indexation Spotlight. Le
dossier `data/modeles` du projet devient un lien symbolique, donc tous les chemins du banc
restent valables. **Regle a retenir pour toute mesure ulterieure : verifier la charge de la
machine avant de chronometrer, et rejeter la mesure si des demons systeme travaillent.**

### 1.4 Desinstallation complete

```
brew uninstall llama.cpp                       # laisse ggml et libomp, utilises ailleurs
rm -rf ~/Library/Caches/popsim-modeles data/modeles   # les 42 Gio de poids et le cache HF
rm -rf /tmp/a3-slots /tmp/a3-llama-server-*.log       # traces laissees par le banc
uv pip uninstall --python .venv/bin/python mlx-lm mlx mlx-metal
# ou, plus radical, si le .venv n'a pas d'autre usage :
rm -rf .venv
```

Trois emplacements sont touches, et c'est tout : `/opt/homebrew` pour llama.cpp, le `.venv`
du projet pour Python, et `~/Library/Caches/popsim-modeles` pour les poids, voir la section
1.3 pour la raison de ce dernier. Aucun service n'a ete
enregistre au demarrage : `llama-server` est lance et arrete par le banc lui-meme, il ne
survit pas a la fin du script. Les journaux du serveur vont dans `/tmp/a3-llama-server-*.log`.

---

## 2. Les modeles retenus et leur date de coupure

La consigne place la date de coupure au-dessus de tous les autres criteres, parce que la
mesure de contamination des jeux d'enquete en depend. **Le resultat de cette verification
est le point le plus derangeant de ce rapport, et il faut le lire en premier.**

| Modele | Format | Poids | Licence | Coupure publiee | Source verifiee |
|---|---|---|---|---|---|
| Qwen3-4B-Instruct-2507 | GGUF Q4_K_M | 2,3 Gio | Apache 2.0 | **aucune** | carte de modele, rapport technique et documentation officielle, tous muets |
| Qwen3-30B-A3B-Instruct-2507 | GGUF Q4_K_M | 17 Gio | Apache 2.0 | **aucune** | idem |
| Meta-Llama-3.1-8B-Instruct | GGUF Q4_K_M | 4,6 Gio | Llama 3.1 Community | **decembre 2023** | "The pretraining data has a cutoff of December 2023", carte officielle Meta |
| gpt-oss-20b | GGUF MXFP4 | 11 Gio | Apache 2.0 | **juin 2024** | "Our model has a knowledge cutoff of June 2024", carte de modele OpenAI |

Sources primaires :
- Llama 3.1 : https://github.com/meta-llama/llama-models/blob/main/models/llama3_1/MODEL_CARD.md
  champ *Data Freshness*. [CONFIRME]
- gpt-oss : arXiv 2508.10925, *gpt-oss-120b & gpt-oss-20b Model Card*, OpenAI. [CONFIRME]
- Qwen3 : carte https://huggingface.co/Qwen/Qwen3-4B-Instruct-2507 et
  https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507, rapport technique arXiv 2505.09388
  section 3.1 sur les donnees de pre-entrainement, et documentation officielle
  https://qwen.readthedocs.io. Les trois decrivent la taille du corpus, 36 000 milliards de
  tokens et 119 langues, et **aucune ne donne de date**. [CONFIRME comme absence, trois
  sources independantes consultees]

### Ce que cela change pour le protocole

`exploration/06-infrastructure-zero-cout.md` recommandait Qwen3 4B et Qwen3 30B-A3B comme
couple principal. Ces deux modeles restent les meilleurs sur le rapport qualite sur debit,
et les mesures de la section 4 le confirment. Mais **ils ne peuvent pas porter le volet
contamination du protocole** : on ne peut pas affirmer qu'un barometre du 4 juin 2026 est
posterieur a la coupure d'un modele dont la coupure n'est pas publiee.

Trois consequences, a arbitrer et non a decider ici :

1. **gpt-oss-20b a ete ajoute a la pile**, hors des recommandations initiales du document
   d'infrastructure. C'est le seul modele a melange d'experts, donc rapide sur cette
   machine, dont la coupure soit publiee par son auteur. Il occupe exactement la place que
   le document reservait a Qwen3-30B-A3B, avec un critere de plus. La substitution est
   proposee, pas faite : les deux sont installes et mesures cote a cote.
2. **Le couple de reference pour toute mesure de contamination doit etre
   Llama 3.1 8B (decembre 2023) et gpt-oss-20b (juin 2024).** Deux coupures distantes de six
   mois, ce qui est un atout : cela donne une variation de la coupure et non un point unique.
3. **Qwen3 reste utile comme troisieme famille de controle**, pour verifier que les
   resultats ne dependent pas d'un fournisseur, mais toute phrase du papier de la forme
   "cette enquete est posterieure a la coupure du modele" devra citer Llama ou gpt-oss.

Une precision d'honnetete : une coupure publiee n'est pas une coupure verifiee. Meta et
OpenAI annoncent une date, personne ne l'a auditee, et la litterature documente des fuites
de donnees posterieures a la coupure annoncee. La date publiee est une condition necessaire,
pas suffisante. Le controle empirique reste a faire, et il est independant de ce rapport.

---

## 3. La verification qui commande tout le reste : les probabilites de tokens

Le protocole du projet ne genere pas de texte. Sur une question fermee, il execute un seul
passage avant et lit la distribution de probabilite du token de reponse. C'est ce qui divise
le cout par plus de mille, et c'est surtout ce qui donne directement la distribution
complete d'une reponse, donc la mesure de diversite que popsim etudie. Si cela ne marche
pas, le plan de travail tombe.

**Cela marche, sur les deux moteurs.** Avec une reserve importante sur le premier.

### 3.1 llama.cpp, par `llama-server`

Le serveur expose la route native `/completion`, qui accepte un parametre `n_probs`
renvoyant les `n` tokens les plus probables a chaque position generee, avec leur
log-probabilite. Exemple complet et minimal, reproductible tel quel une fois le serveur
lance :

```
llama-server -m data/modeles/gguf/Qwen3-4B-Instruct-2507-Q4_K_M.gguf \
    -c 8192 -ngl 999 --no-webui --port 8099 &

curl -s http://127.0.0.1:8099/completion -H 'Content-Type: application/json' -d '{
  "prompt": "Tu reponds a une enquete.\nQuestion. Faut-il davantage de transports en commun ?\nA. oui\nB. non\nC. sans opinion\nReponse :",
  "n_predict": 1, "n_probs": 10, "temperature": 0, "cache_prompt": true
}' | python3 -c '
import json,sys,math
r=json.load(sys.stdin)
for e in r["completion_probabilities"][0]["top_logprobs"]:
    print(f"{e[\"token\"]!r:>8}  p={math.exp(e[\"logprob\"]):.4f}")
print(r["timings"])'
```

Resultat obtenu par le banc sur le persona factice de 3 000 tokens, question 1, cinq
modalites, `n_probs = 40` : les cinq lettres sont toutes presentes dans le top 40, la masse
de probabilite qu'elles portent avant renormalisation est mesuree entre **0,895 et 0,969**
selon le modele, et la renormalisation sur ces cinq lettres donne la distribution
exploitable. Le detail chiffre par modele est en section 4. Une exception importante,
gpt-oss-20b, qui tombe a 0,032 en prompt brut et remonte a 0,999 avec son gabarit de
conversation : voir la section 4.5, c'est le controle qui a rattrape l'erreur.

**Ce que llama-server ne permet pas, et il faut l'ecrire noir sur blanc.** Le serveur ne
renvoie de probabilites qu'aux positions **generees**, jamais aux positions du prompt. Deux
consequences :

1. On n'obtient pas la distribution complete sur le vocabulaire, seulement un top `n`. Pour
   des etiquettes courtes en tete de distribution, c'est sans effet. Pour une modalite rare,
   elle peut sortir du top `n` et etre comptee a zero. Le banc signale explicitement ce cas.
   Parade : monter `n_probs`, et surveiller la masse totale avant renormalisation.
2. Le scoring d'une modalite verbalisee de plusieurs tokens n'est pas direct : il faut la
   parcourir token par token, un aller-retour HTTP par token. Faisable, mais couteux et
   inelegant.

Ce n'est pas eliminatoire, parce que la methode retenue par le projet, celle des etiquettes
courtes, ne demande rien de plus que le top `n` a une seule position. C'est en revanche une
raison de garder mlx-lm sous la main pour tout ce qui touche a la calibration.

### 3.2 mlx-lm

Acces direct aux logits, dans le processus, sans passer par un serveur. `model(ids, cache=c)`
renvoie un tenseur de forme (1, longueur, vocabulaire). On prend la derniere position, on
retire le `logsumexp`, on lit la case de n'importe quel identifiant de token. **La
distribution est complete et exacte, pas tronquee a un top `n`.** Le scoring d'une sequence
de plusieurs tokens se fait en un seul passage avant, en lisant les positions decalees de un.

C'est le moteur qui permet les traitements (b), (c) et (d) de la section suivante. Aucune
restriction constatee.

### 3.3 Le piege : les modalites n'ont ni la meme longueur ni la meme tokenisation

Le probleme, enonce sans detour. La probabilite d'une modalite verbalisee est un produit de
probabilites, une par token. Une modalite de quatorze tokens est donc mecaniquement plus
improbable qu'une modalite d'un token, **quel que soit l'avis du persona**. Comparer
directement ces probabilites revient a classer les modalites par longueur. Deux difficultes
s'y ajoutent :

- la tokenisation depend du contexte gauche : `A` colle et ` A` precede d'une espace ne sont
  pas le meme token, et encoder la modalite isolement donne souvent un autre decoupage que
  celui qui apparait reellement dans le prompt ;
- deux modalites peuvent partager leur premier token (`je ne sais pas` et `je pense que`),
  ce qui rend la lecture du seul premier token invalide des que les modalites sont
  verbalisees.

**Ce n'est pas une inquietude theorique, le banc le mesure.** Sur Qwen3-4B, meme persona,
meme question, cinq modalites de 1, 1, 5, 9 et 14 tokens, les classements obtenus par quatre
methodes de scoring sont les suivants :

| Methode | Classement obtenu |
|---|---|
| (a) etiquette courte, un token | D > E > C > A > B |
| (b) somme brute des log-probabilites du libelle | D > B > A > E > C |
| (c) log-probabilite moyenne par token | E > D > C > B > A |
| (d) PMI conditionnel au domaine | B > C > E > A > D |

Le tau de Kendall entre (a) et (b) vaut **0,00**. [MESURE] Quatre facons de lire la meme
distribution donnent quatre reponses differentes, et trois d'entre elles designent une
modalite gagnante differente. Le choix de la methode de scoring n'est pas un detail
d'implementation, c'est une decision methodologique qui change les resultats.

### 3.4 Les traitements, et celui que le projet doit retenir

**(a) Etiquettes courtes, un token, meme position. C'est le traitement a retenir.**
Le prompt se termine par `Reponse :` et l'on ne score que la lettre. Le biais de longueur
disparait par construction : toutes les modalites sont un token unique, lu a la meme
position, dans le meme contexte gauche. Trois precautions obligatoires :

- verifier a la construction du prompt que les K modalites correspondent bien a K
  identifiants de tokens **distincts**, dans ce contexte gauche precis. Le banc le fait en
  encodant `prompt` puis `prompt + " A"` et en prenant le token qui differe, jamais en
  encodant `" A"` isolement ;
- sur une echelle de Likert, preferer les chiffres 1 a 7 aux libelles ;
- surveiller la masse de probabilite portee par les K modalites avant renormalisation. Elle
  est un indicateur de validite : mesuree entre 0,895 et 0,969 sur les modeles correctement
  formates, elle dit que le modele a bien compris la consigne de format. Elle est tombee a
  **0,032** sur gpt-oss-20b mal formate, cas reel rencontre au cours de ce travail. Sans ce
  controle, la renormalisation aurait fabrique une distribution a partir de presque rien et le
  resultat aurait ete publie sans que rien ne signale l'erreur. Seuil de rejet propose : 0,5.

Limite honnete de ce traitement : la lettre porte un a priori de position. Les modeles
favorisent certaines positions dans une liste, ce qui est documente. La parade est la
permutation de l'ordre des modalites sur deux a quatre passages et la moyenne des
distributions obtenues, ce qui multiplie le cout par deux a quatre. Rapporte au facteur
1 000 gagne sur l'echantillonnage, c'est negligeable, et c'est non negociable.

**(b) Somme brute des log-probabilites du libelle. A ne jamais utiliser seule.** Elle figure
dans le banc comme temoin negatif, pour rendre le biais visible.

**(c) Normalisation par la longueur.** Moyenne des log-probabilites par token. Corrige
l'essentiel du biais mecanique et se calcule sans passage supplementaire. Defaut connu : elle
surpondere les libelles longs dont chaque token est previsible une fois le premier pose, ce
qui se voit dans le tableau ci-dessus ou la modalite la plus longue passe en tete.

**(d) PMI conditionnel au domaine**, `log p(libelle | persona + question)` moins
`log p(libelle | question seule)`. Retire la frequence propre du libelle dans la langue et ne
garde que ce que le persona apporte. C'est la correction de la competition de forme de
surface proposee par Holtzman et al. en 2021. Elle coute un passage avant supplementaire par
modalite sur un contexte court, donc peu. C'est le traitement a employer si le protocole
devait un jour utiliser des modalites verbalisees, par exemple pour reprendre telles quelles
les formulations d'une enquete.

**Recommandation.** Etiquettes courtes avec permutation de l'ordre, traitement (a), pour la
production. Traitement (d) en controle sur un sous-echantillon, pour verifier que le
classement des modalites ne dependait pas de l'etiquetage. Traitement (b) proscrit.

---

## 4. Les mesures

### 4.1 Protocole

Le banc est `analyses/a3_banc_inference.py`. Il fabrique un persona factice de 3 029 tokens
et cinquante questions fermees a cinq modalites, avec une graine fixe, ce qui est exactement
la forme de l'experience de phase 1. Il lance lui-meme `llama-server`, l'interroge, l'arrete.
Sur mlx-lm il charge le modele dans son propre processus.

Configuration retenue pour llama.cpp, celle que recommandait le document d'infrastructure :
`-ngl 999` pour tout mettre sur le GPU Metal, `-fa on`, cache KV quantifie en 8 bits
(`--cache-type-k q8_0 --cache-type-v q8_0`), `--cache-reuse 256`, contexte de 8 192 tokens
par slot, huit slots. Le modele a melange d'experts de 30 milliards tourne a quatre slots,
faute de memoire pour huit.

Sept mesures par modele, T1 a T7, decrites en tete du script. Trois precisions de methode
qui ont change les resultats et qu'il faut connaitre pour relire les chiffres.

**Le vidage du cache.** `llama-server` refuse l'action `erase` sur ses slots s'il n'a pas ete
lance avec `--slot-save-path`, et il repond alors 501. Une premiere version du banc avalait
cette erreur et croyait mesurer un prefill a froid de 30 ms, ce qui est impossible. Corrige.
Regle generale a retenir : **un prefill a froid anormalement rapide est le symptome d'un
cache qui n'a pas ete vide, jamais celui d'une machine rapide.**

**Le test de lots.** Premiere version, fausse : envoyer P requetes simultanees portant le
meme persona. Le serveur les repartit sur P slots, chacun doit alors traiter le persona
entier, et les slots s'evincent au tour suivant. Gain mesure : 0,06, soit seize fois plus
lent. Ce n'etait pas une mesure du lot, c'etait une mesure de la contention. La forme
productive est l'inverse : P personas differents, un par slot, chacun deroulant ses
questions en serie. C'est celle qui est mesuree ici, et c'est aussi celle de la phase 1.

**Le cache de prefixe sous mlx-lm.** Sauvegarder puis recharger le cache depuis le disque
entre deux questions coute plusieurs centaines de mega-octets d'entrees-sorties par appel et
mesure le disque, pas le modele. La bonne primitive est `trim_prompt_cache`, qui retranche
du cache les tokens de la question precedente sans rien recalculer. Le banc verifie d'abord
`can_trim_prompt_cache` et s'arrete si le modele ne le permet pas, ce qui est le controle que
le document d'infrastructure demandait pour les modeles a fenetre glissante.

### 4.2 Le tableau des mesures

Toutes les valeurs qui suivent sont des mesures faites le 3 septembre 2026, machine au
repos, charge moyenne systeme comprise entre 2,0 et 3,2 sur dix coeurs, relevee et
consignee au debut de chaque execution. Persona de 3 029 tokens, question de 63 a 66
tokens, cinquante questions par serie. Fichiers bruts dans `resultats/mesures-a3/*.json`.

| Configuration | Prefill t/s | Decodage t/s | Masse sur A a E | Gain cache | Gain lot | ms par appel | Appels par heure |
|---|---|---|---|---|---|---|---|
| llama.cpp Qwen3-4B, np 8 | **786** | **38,4** | 0,962 | **x26,6** | x1,15 | **199** | **18 060** |
| llama.cpp Llama-3.1-8B, np 8 | 292 | 13,1 | 0,969 | x26,4 | x1,38 | 364 | 9 885 |
| llama.cpp Llama-3.1-8B, np 1 | 294 | 15,5 | 0,969 | x26,0 | non teste | 372 | 9 684 |
| llama.cpp Llama-3.1-8B, cache KV f16 | 302 | 15,6 | 0,969 | x28,2 | non teste | 371 | 9 699 |
| llama.cpp gpt-oss-20b MXFP4, np 8 | 431 | 25,3 | 0,032 puis 0,999 | x16,5 | non teste | 376 | 9 569 |
| llama.cpp Qwen3-30B-A3B, np 4 | 282 | 22,6 | 0,926 | x21,9 | non teste | 432 | 8 340 |
| mlx-lm Qwen3-4B 4 bits | 689 | 27,2 | 0,895 | x16,1 | sans objet | 262 | 13 736 |
| mlx-lm Llama-3.1-8B 4 bits | 432 | 17,8 | 0,941 | x21,8 | sans objet | 329 | 10 934 |

### 4.3 Ce que ces mesures corrigent dans le document d'infrastructure

**Le debit de prefill. L'hypothese de 800 tokens par seconde etait juste pour un modele de
4 milliards de parametres et fausse d'un facteur 2,7 pour celui de 8 milliards.**

| | Estime dans le document | Mesure | Ecart |
|---|---|---|---|
| Prefill, Llama 3.1 8B en 4 bits | 800 t/s [HYPOTHESE] | **292 t/s** [MESURE] | document optimiste x2,7 |
| Prefill, Qwen3 4B en 4 bits | non estime | **786 t/s** [MESURE] | |
| Decodage, 8B en 4 bits | 24 a 29 t/s, valeur de travail 27 | **13,1 t/s** [MESURE] | document optimiste x2,1 |
| Decodage, 4B en 4 bits | 45 a 55 t/s | **38,4 t/s** [MESURE] | document optimiste x1,3 |
| Decodage, Qwen3 30B-A3B | 50 a 70 t/s | **22,6 t/s** [MESURE] | document optimiste x2,7 |
| Gain du cache de prefixe | x8,5 [PROBABLE] | **x16 a x28** [MESURE] | document **pessimiste** x2 a x3 |
| Gain du traitement par lots | x2 [PROBABLE] | **x1,15 a x1,38** [MESURE] | document optimiste x1,5 |

Deux erreurs de sens contraire, qui se compensent en partie : le document surestime les
debits bruts et sous-estime nettement le cache de prefixe. C'est pour cela que son total de
cinq heures pour la phase 1 reste dans le bon ordre de grandeur alors qu'aucun de ses
parametres n'etait bon.

**Le cache de prefixe est le levier decisif, et il l'est plus que le document ne le disait.**
Sur Llama 3.1 8B, un appel coute 10,8 s sans cache et 0,41 s avec, soit un facteur 26,4.
[MESURE] Le persona de 3 029 tokens n'est traite qu'une fois, les 63 tokens de la question
suivante sont les seuls a etre reevalues. La regle du document, persona en tete et question
en queue, est confirmee comme la decision d'architecture la plus rentable du projet.

**Le traitement par lots ne rapporte presque rien sur cette machine, et c'est le resultat le
plus contraire aux attentes.** Mesure sur Llama 3.1 8B, huit slots, un persona different par
slot : 10 604 appels par heure a un persona, 14 222 a deux, 14 637 a quatre. Le gain plafonne
a **x1,38** et non x2. Sur Qwen3-4B il plafonne a x1,15. [MESURE] Un balayage complementaire
donne meme x0,89, c'est a dire une perte, sur Qwen3-4B a huit personas simultanes.

Un balayage de quatre configurations du serveur, detaille en section 4.7, ne trouve aucun
reglage qui renverse ce constat.

L'explication tient a la mecanique observee dans le journal du serveur : le delta de 64
tokens d'une question coute 242 ms quand la requete est seule et 1 301 ms quand huit
requetes sont en vol. Le debit agrege reste donc plat. Sur un M5 de base, un seul flux
sature deja le GPU, et l'ordonnanceur continu de llama.cpp n'a plus rien a fusionner. Le
gain de 2,6x a 3,7x publie pour vllm-mlx a ete obtenu sur un M4 Max, machine dont la bande
passante memoire est trois a quatre fois superieure.

**Consequence pratique immediate, et elle economise de la memoire :** lancer `llama-server`
avec `-np 1` plutot que `-np 8` ne coute que 2 pour cent de debit, 9 684 contre 9 885 appels
par heure, et fait passer l'empreinte memoire de 13,7 Gio a **5,4 Gio**. [MESURE] Sur une
machine de 32 Gio, ces 8 Gio recuperes valent bien mieux que le gain de lot.

Un contre-test le confirme et va plus loin : Qwen3-4B lance avec `-np 2` atteint **21 915 a
22 909 appels par heure** en regime etabli, contre 18 060 avec `-np 8`. [MESURE] Reduire le
nombre de slots ne coute donc pas du debit, il en rend. La raison est la meme que
precedemment : huit slots se disputent un GPU qu'un seul flux sature deja, et le serveur paie
en plus le cout de son ordonnancement. **Recommandation : deux slots, pas huit.**

**La quantification du cache KV en 8 bits ne sert a rien ici.** Cache f16 contre q8_0 sur
Llama 3.1 8B : 9 699 contre 9 885 appels par heure, difference dans le bruit, et l'empreinte
memoire relevee est meme legerement plus basse en f16, ce qui montre que la mesure par RSS ne
resout pas la difference. [MESURE] A 3 000 tokens de contexte le cache KV est petit. Ce
levier ne redevient utile qu'au dela de 16 000 tokens par persona.

### 4.4 mlx-lm contre llama.cpp : le classement s'inverse selon le modele

Le document annoncait llama.cpp 21 a 87 pour cent plus lent que MLX, en citant arXiv
2601.19139. La mesure ne le confirme pas, et donne meme le resultat inverse sur le petit
modele.

| Modele | llama.cpp | mlx-lm | Vainqueur |
|---|---|---|---|
| Qwen3-4B 4 bits | **18 060 appels/h** | 13 736 appels/h | llama.cpp, +31 % |
| Llama-3.1-8B 4 bits | 9 885 appels/h | **10 934 appels/h** | mlx-lm, +11 % |

Sur le prefill, mlx-lm gagne nettement sur le 8B, 432 contre 292 tokens par seconde, et perd
sur le 4B, 689 contre 786. [MESURE] La conclusion utilisable est qu'aucun des deux moteurs ne
domine, que l'ecart n'excede pas 30 pour cent dans un sens ou dans l'autre, et que **le choix
doit se faire sur autre chose que la vitesse** : robustesse, acces aux logits, et maturite.
Sur ces trois criteres llama.cpp reste le socle recommande, mlx-lm restant indispensable pour
la distribution complete sur le vocabulaire et le scoring multi-token.

Point de controle demande par le document et effectue : la reutilisation du cache de prefixe
sous mlx-lm a ete verifiee par `can_trim_prompt_cache` avant chaque serie, et validee sur
Qwen3-4B et sur Llama-3.1-8B. Aucun de ces deux modeles n'est a fenetre glissante. Le banc
s'arrete avec un message explicite si un modele ne le permet pas, ce qui evite le
recalcul silencieux redoute.

### 4.5 gpt-oss-20b : le gabarit de conversation n'est pas optionnel

Interroge avec un prompt brut, comme les autres modeles, gpt-oss-20b ne place que **3,2 pour
cent** de sa masse de probabilite sur les cinq lettres de reponse. Ses tokens les plus
probables sont des retours a la ligne. La lecture des logprobs y est sans valeur.

Interroge avec son gabarit officiel *harmony*, meme persona et meme question, la masse passe
a **0,9993**, la meilleure de tous les modeles testes, et la distribution est nette :
p(D) = 0,66, p(C) = 0,187, p(B) = 0,119. [MESURE]

```
<|start|>system<|message|>Reasoning: low<|end|>
<|start|>user<|message|>{persona}{question}<|end|>
<|start|>assistant<|channel|>final<|message|>
```

Detail qui compte : le gabarit doit se terminer **sans espace**. Avec un espace final, la
masse retombe a 0,84, parce que le modele hesite alors entre le token `D` et le token ` D`.
C'est exactement le piege de tokenisation decrit en section 3.3, pris sur le fait.

**Regle a graver, valable pour tous les modeles :** verifier la masse portee par les
modalites avant de renormaliser. Elle est le detecteur de panne du protocole. Entre 0,89 et
0,97 pour Qwen3 et Llama en prompt brut, 0,999 pour gpt-oss en gabarit correct, 0,03 pour
gpt-oss en prompt brut. Un seuil de rejet a 0,5 aurait attrape l'erreur toute seule.

### 4.6 Stabilite et memoire sur une serie longue

Cinquante questions consecutives sur le meme persona, llama.cpp.

| | Qwen3-4B | Llama-3.1-8B |
|---|---|---|
| Duree de la serie | 10,1 s | 18,2 s |
| Premier appel | 194 ms | 354 ms |
| Mediane des suivants | 199 ms | 364 ms |
| Minimum, maximum | 190 ms, 215 ms | 351 ms, 379 ms |
| Amplitude relative | 12 % | 8 % |
| Memoire au debut, a la fin | 13 418 Mo, 13 418 Mo | 13 687 Mo, 13 687 Mo |

Aucune derive, aucune fuite de memoire, aucune degradation entre la premiere et la seconde
moitie de la serie. [MESURE] La stabilite n'est pas un probleme sur cinquante appels. Elle
reste a verifier sur une serie de plusieurs heures, ce que ce banc ne fait pas.

Reserve importante : l'empreinte est mesuree par la RSS du processus `llama-server`. Sur
Apple Silicon une partie des allocations Metal n'y apparait pas fidelement, et les poids sont
projetes en memoire par `mmap`. Ces chiffres sont un ordre de grandeur, pas une comptabilite.
Le seul enseignement solide est l'absence de croissance au fil de la serie.

### 4.7 Balayage des options du serveur : rien ne bat la configuration simple

Quatre configurations de `llama-server` comparees sur Qwen3-4B, machine au repos, huit
personas distincts, un par slot. La colonne P vaut le nombre de flux simultanes.

| Configuration | P = 1 | P = 8 | Gain du lot |
|---|---|---|---|
| **Reference : `-np 8`, KV q8_0, `--cache-reuse 256`** | **24 104 appels/h** | 21 498 | x0,89 |
| Sans `--cache-reuse` | 20 927 | **24 425** | x1,17 |
| `-b 4096 -ub 2048` | 16 739 | 20 135 | x1,20 |
| `--no-kv-unified` | 16 900 | 22 606 | x1,34 |

Trois enseignements. [MESURE]

D'abord, **le meilleur chiffre absolu du tableau est celui de la configuration de reference
avec un seul flux**, 24 104 appels par heure. Aucun reglage teste ne fait mieux, et le
meilleur resultat en lot, 24 425, lui est statistiquement egal. Le gain de lot annonce par
certaines configurations, jusqu'a x1,34, est un artefact : ces configurations partent
simplement de plus bas a un flux. **Comparer des gains relatifs sans regarder les valeurs
absolues aurait conduit a choisir `--no-kv-unified`, c'est a dire la troisieme pire
configuration du tableau.**

Ensuite, `--cache-reuse 256` aide nettement a un flux, 24 104 contre 20 927, et gene a huit.
C'est coherent avec le reste : le decalage de cache par KV shifting est du travail
supplementaire qui ne se rentabilise que si le slot est seul a travailler.

Enfin, augmenter le lot physique avec `-ub 2048` **degrade** le debit a un flux de 30 pour
cent. Sur cette machine, agrandir les lots ne sert a rien puisque rien ne les remplit.

Ce balayage recoupe le test T6 mene independamment : 24 104 ici contre 24 404 en T6 sur la
meme configuration, soit 1,2 pour cent d'ecart. Les deux mesures se confirment.

---

## 5. Le chiffre attendu : combien d'appels par heure, et combien d'heures pour la phase 1

### 5.1 Appels par heure

Deux chiffres differents, et il faut les distinguer, sinon on se trompe d'un facteur 1,4.

**En regime etabli**, c'est a dire une fois le persona charge dans le cache, une question
apres l'autre, mesure sur une serie de cinquante questions :

| Modele | Appels par heure, regime etabli |
|---|---|
| Qwen3-4B, llama.cpp | **18 060** |
| mlx-lm Llama-3.1-8B | 10 934 |
| Llama-3.1-8B, llama.cpp | 9 885 |
| gpt-oss-20b | 9 569 |
| Qwen3-30B-A3B | 8 340 |

**En configuration reelle de la phase 1**, c'est a dire en payant aussi le calcul des
prefixes de persona, qui ne sont pas gratuits. La phase 1 compte 150 personas par 6
conditions, soit **900 prefixes distincts** a calculer, chacun de 3 029 tokens :

`duree totale = 900 x (3029 / prefill) + 45 000 x (ms par appel)`

| Modele | Cout d'un prefixe | Duree des 45 000 appels | Appels par heure reels |
|---|---|---|---|
| **Qwen3-4B, llama.cpp** | 3,85 s | **3 h 27** | **13 026** |
| mlx-lm Qwen3-4B | 4,39 s | 4 h 22 | 10 287 |
| mlx-lm Llama-3.1-8B | 6,76 s | 5 h 49 | 7 751 |
| gpt-oss-20b | 6,15 s | 6 h 14 | 7 212 |
| **Llama-3.1-8B, llama.cpp** | 9,99 s | **7 h 03** | **6 384** |
| Qwen3-30B-A3B | 10,74 s | 8 h 05 | 5 569 |

Avec le gain de lot mesure, la duree tombe a 3 h 07 pour Qwen3-4B et a 5 h 47 pour
Llama-3.1-8B. Le gain de lot ne s'applique qu'a la partie repetee, pas aux prefixes.

### 5.2 Reponse a la question posee

> Combien d'appels de modele cette machine peut-elle traiter en une heure, dans notre
> configuration reelle ?

**Entre 5 600 et 13 000 appels par heure selon le modele, prefixes de persona compris.**
[MESURE] Le chiffre a retenir pour un plan de travail est **6 400 appels par heure** avec
Llama 3.1 8B, qui est le modele que le projet doit utiliser puisque c'est le seul de la pile
qui allie une taille credible et une coupure documentee.

> Les 45 000 appels de la phase 1, en combien de temps ?

**Sept heures avec Llama 3.1 8B. Trois heures et demie avec Qwen3-4B. Huit heures avec le
melange d'experts de 30 milliards.** [MESURE]

> Le document d'infrastructure annonce environ cinq heures. Confirmer ou corriger.

**A corriger, mais moins que ne le laissaient craindre les erreurs de parametres.** Les cinq
heures annoncees sont :

- **trop pessimistes de 30 pour cent** si la phase 1 tourne sur Qwen3-4B : 3 h 27 mesurees ;
- **trop optimistes de 40 pour cent** si elle tourne sur Llama-3.1-8B : 7 h 03 mesurees ;
- **trop optimistes de 60 pour cent** sur Qwen3-30B-A3B : 8 h 05 mesurees.

Formulation a retenir pour le plan de travail : **la phase 1 est une nuit de calcul, pas une
semaine.** Elle rentre dans une seule nuit sur n'importe lequel des modeles installes, et
dans une demi-nuit sur le petit. La conclusion strategique du document d'infrastructure, qui
etait que la machine locale suffit et que les paliers gratuits d'API ne sont pas le moteur de
production, **est confirmee par la mesure**, et avec une marge confortable.

Ce qui change en revanche, c'est la capacite hebdomadaire annoncee. Le document promettait
plus de 400 000 appels par semaine. En regime reel, huit heures par nuit et sept nuits sur
sept, soit 56 heures :

| Modele | Appels par semaine [MESURE] | Annonce du document |
|---|---|---|
| Qwen3-4B | environ 730 000 | 400 000 |
| Llama-3.1-8B | environ 357 000 | 400 000 |
| Qwen3-30B-A3B | environ 312 000 | 400 000 |

L'ordre de grandeur du document tient. Le rapport de 1 a 30 avec les offres gratuites d'API,
estimees a 12 000 appels par semaine, est confirme.

---

## 6. Les limites de ce travail

Elles sont listees ici parce qu'un relecteur les trouverait de toute facon.

1. **Le persona du banc fait 3 029 tokens, pas 8 000.** Le document d'infrastructure
   raisonne sur un prefixe de 8 000 tokens. La consigne de cette mission demandait 2 000 a
   4 000. Les deux chiffres qui dependent de la longueur du prefixe sont donc a reechelonner
   si le protocole retient 8 000 tokens : le cout d'un prefixe passerait de 10 s a environ
   27 s sur le 8B, ce qui ajouterait environ 4 heures aux 900 prefixes de la phase 1, et
   porterait le total a **environ 11 heures**. [PROBABLE, extrapolation lineaire du prefill
   mesure, non verifiee a 8 000 tokens] Le cout par appel en regime etabli, lui, ne changerait
   presque pas, puisque seul le delta de la question est reevalue.
2. **Une seule serie de cinquante appels par configuration.** Pas de repetition, donc pas
   d'intervalle de confiance sur les debits. L'amplitude interne des series, 8 a 12 pour
   cent, donne une idee de la dispersion a court terme, pas de la dispersion entre
   executions.
3. **La stabilite thermique sur plusieurs heures n'est pas mesuree.** La plus longue serie
   de ce banc dure 18 secondes. Correction du 3 septembre 2026 : une version anterieure de
   cette limite parlait d'un "portable de 14 pouces", ce qui est faux. La machine est un
   Mac17,3, donc un **MacBook Air M5**, et il n'existe pas de MacBook Air 14 pouces. Le
   point important n'etait de toute facon pas la diagonale de l'ecran mais le
   refroidissement : **cet Air n'a pas de ventilateur**, la chaleur sort par le chassis en
   convection passive. C'est le cas le plus defavorable pour une charge GPU continue de
   sept heures.
   **Cette limite est desormais levee, et le resultat est lourd.** La mesure est faite dans
   `resultats/a4-bridage-thermique.md` : sur dix minutes de charge continue, le debit de
   Qwen3-4B passe de 22 023 a 13 385 appels par heure, soit **39 pour cent de perte**, et la
   courbe descendait encore a la dixieme minute. Les durees annoncees en section 5.1
   ci-dessus sont donc des **planchers optimistes** : elles sont a majorer d'au moins 55 a
   70 pour cent, ce qui porte Qwen3-4B a environ 5 h 20 a 5 h 55 et Llama-3.1-8B a environ
   10 h 50 a 12 h 10. Voir le rapport a4 pour la fourchette complete et pour ce qu'elle ne
   dit pas.
4. **La sensibilite a l'activite du systeme est enorme et mal bornee.** Documentee en section
   1.3 : sur Qwen3-4B, le meme banc a mesure 725 tokens par seconde de prefill machine au
   repos et 414 machine occupee a synchroniser iCloud, soit une sous estimation de 40 pour
   cent. Correction du 3 septembre 2026 : une version anterieure de cette limite opposait
   786 a 292 tokens par seconde, ce qui etait faux. Ces deux valeurs figurent au tableau de
   la section 4 mais concernent deux modeles differents, Qwen3-4B et Llama-3.1-8B, et non le
   meme modele dans deux etats de charge. L'effet iCloud est reel et mesure, son ampleur est
   celle du couple 725 contre 414. Toute mesure future
   doit consigner la charge systeme, ce que le banc fait desormais.
5. **Le balayage des options du serveur porte sur quatre configurations, pas cinq.** La
   variante a cache KV en f16 a echoue par arret du serveur pendant le test et n'a pas ete
   reprise. Les quatre autres sont exploitables et figurent en section 4.7. Aucune n'a ete
   repetee, donc aucune n'a d'intervalle de confiance.
6. **Le scoring multi-token n'a ete mesure que sous mlx-lm.** L'API de `llama-server`
   n'expose pas les probabilites aux positions du prompt. C'est sans consequence pour le
   protocole retenu, qui n'utilise que des etiquettes d'un token, mais cela veut dire que
   tout controle par PMI devra passer par mlx-lm.
7. **Aucune mesure de qualite.** Ce rapport ne dit rien de la fidelite des reponses, ni de la
   diversite reelle produite par ces modeles. Les entropies affichees par le banc, de 0,49 a
   2,19 bits selon le modele, portent sur un persona factice et cinquante questions inventees.
   **Elles ne doivent en aucun cas etre lues comme un resultat sur la compression de variance.**
   Elles ne servent qu'a verifier que la lecture des probabilites produit bien une
   distribution et non un pic degenere.
8. **La date de coupure de Qwen3 n'est pas publiee, et le protocole de contamination en
   depend.** C'est le point le plus lourd du rapport et il est traite en section 2. Il ne se
   resout pas par une mesure de debit.
9. **Aucune donnee d'enquete n'a servi a ces tests, ce qui est voulu**, mais cela veut dire
   qu'aucun test n'a ete fait sur un vrai persona reconstruit a partir de microdonnees. La
   longueur, la structure et la tokenisation d'un vrai persona differeront.

---

## 7. Ce qu'il faut faire de ce rapport

Trois decisions sont a prendre, et aucune n'est technique.

**Le modele porteur de la phase 1.** Llama 3.1 8B est le seul candidat qui reunisse une
coupure documentee, une taille credible et une seconde source de comparaison. Il coute
7 heures pour la phase 1. gpt-oss-20b apporte une deuxieme coupure documentee, plus recente
de six mois, pour 6 h 14. Le couple des deux est ce que ce rapport recommande, et il coute
13 heures, soit deux nuits.

**Le sort de Qwen3.** Il est plus rapide et probablement meilleur, mais il ne peut porter
aucune affirmation sur la contamination. Le garder en troisieme famille de controle, jamais
en modele de reference.

**La configuration de production.** `llama-server` avec `-np 1` ou `-np 2`, cache KV en f16, prefixe de
persona en tete et fige, question en queue, etiquettes d'un seul token, permutation de
l'ordre des modalites, et seuil de rejet sur la masse de probabilite non renormalisee. Le
traitement par lots ne merite pas l'effort d'ingenierie qu'il demande sur cette machine.
