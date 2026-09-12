# Inscriptions retrouvées dans la boîte mail (12 septembre 2026)

Recherche en lecture seule sur `aboutdotblank@gmail.com` (boîte réelle : `amirksmain@gmail.com`),
six derniers mois, via les outils Gmail (`search_threads`, `get_message`). Aucun message envoyé,
modifié, étiqueté ou marqué ; aucune autre donnée que les inscriptions n'est rapportée ici.

---

## 1. LISS Data Archive (Centerdata, Tilburg) — **en attente, accès non accordé**

- **2026-09-09 10:13** — `statements@centerdata.nl`, « Your data statement from LISS Data
  Archive » : accusé de réception d'une déclaration de données soumise par le responsable
  (formulaire signé en ligne). Le message dit seulement que « the statement will be processed »,
  délai indicatif 5 jours ouvrés. Une pièce jointe PDF (« LISS Statement ... ») existe ; je ne
  l'ai pas ouverte, son contenu n'est pas nécessaire au verdict.
- **2026-09-09 13:26** — même expéditeur, « LISS Data Archive » : une personne (Gamze Demirel,
  assistante de recherche) répond en demandant des précisions **avant** d'accorder l'accès :
  le but de la recherche, si les données serviront à une mission rémunérée, et plus de détails
  sur le projet popsim et le rôle du responsable dedans.
- **Aucune réponse envoyée** par le responsable trouvée dans les messages envoyés
  (`in:sent` ne retourne rien pour centerdata/LISS). **État réel : demande d'accès en attente
  d'une réponse du responsable, aucun accès accordé.**
- **Ce à quoi ça donnerait accès, si accordé** : le panel LISS (infrastructure généraliste de
  panel néerlandais — santé, économie, comportement, réinterrogation longitudinale), pas un jeu
  construit autour de jumeaux LLM.
- **Pairage individuel humain/jumeau : NON tranchable comme qualifiant, et ce n'est pas la peine
  d'attendre la réponse pour le savoir.** `resultats/troisieme-jeu-2026-09-12.md` (tâche 2) a
  déjà vérifié la documentation publique LISS et n'y a trouvé aucune trace de sorties LLM
  générées et appariées aux panélistes — verdict déjà posé : négatif, ne pas poursuivre. Cette
  inscription ne change pas ce verdict, même une fois l'accès obtenu.

## 2. British Election Study — **compte créé, mais processus de connexion inachevé à ce jour**

- **2026-09-09 10:15** — `admin@britishelectionstudy.com`, « [The British Election Study]
  Login Details » : confirme la création d'un compte (nom d'utilisateur `AmirKS`) et invite à
  définir un mot de passe via un lien à usage unique pour terminer l'inscription. Le message
  précise que l'usage des données BES est soumis à leurs conditions d'utilisation (page dédiée
  citée dans le courriel).
- **2026-09-10 09:01** — même expéditeur, « [The British Election Study] Password Reset » :
  une nouvelle demande de réinitialisation de mot de passe pour le même compte `AmirKS`, un jour
  plus tard — signe que le mot de passe n'avait pas été fixé du premier coup, ou a été oublié.
- Je n'ai trouvé **aucun courriel ultérieur** confirmant une connexion réussie ou un
  téléchargement. **État réel : compte créé, mais je ne peux pas confirmer que le responsable a
  terminé la définition du mot de passe ni téléchargé quoi que ce soit.**
- Je n'ai **pas recopié** les liens de réinitialisation de mot de passe (à usage unique) — ils
  existent dans les deux courriels ci-dessus si besoin de les utiliser soi-même.
- **Ce à quoi ça donne accès** : le panel électoral BES (~30 000 répondants par vague, panel
  Internet britannique), téléchargement libre une fois le compte actif.
- **Pairage individuel humain/jumeau : déjà tranché négativement dans
  `resultats/troisieme-jeu-2026-09-12.md`** (tâche 2) — aucune vague ni supplément BES ne
  contient de réponses générées par un LLM appariées aux répondants du panel. Cette inscription
  n'apporte rien de nouveau pour l'attaque, même une fois active.

## 3. Open Science Framework (OSF) — compte existant, **pas une inscription à un jeu de données**

- **2026-09-09 10:06** — « OSF Account Verification » : vérification d'adresse e-mail pour un
  compte OSF.
- **2026-09-09 10:12** — « Now, public. Next, impact. » : félicitations automatiques pour avoir
  rendu public le projet OSF « popsim : auditer ce que les modèles de langage disent des
  opinions ».
- **2026-09-11 21:17** — « Welcome to Open Science Framework (OSF)! » : courriel d'onboarding
  automatique (webinaires, guides), envoyé deux jours après la vérification — cohérent avec une
  séquence de bienvenue différée, pas une deuxième inscription.
- **Ce que c'est réellement** : le compte OSF utilisé pour héberger et déposer les
  préenregistrements du projet popsim lui-même (R5, R6, etc., déjà mentionnés dans la mémoire du
  projet), **pas** une inscription donnant accès à un jeu de données tiers. Je le mentionne pour
  mémoire mais il ne répond pas à la question posée.

## 4. Autres pistes citées dans la consigne : rien trouvé

Recherché sans résultat pertinent sur six mois : ICPSR, Dataverse/Harvard Dataverse, Zenodo,
Figshare, ANES, GESIS, UK Data Service, NORC, Prolific, Qualtrics, Kaggle, SOEP, ELIPSS, Progedo,
CESSDA, ainsi que les formulations génériques (« data access », « account created », « terms of
use », « application approved »). Les seuls autres comptes/connexions trouvés dans le même
créneau (Hugging Face — courriels de connexion et de confirmation d'adresse, mars/avril/juillet
2026) sont des notifications de connexion à un compte déjà existant, sans lien identifié avec une
demande d'accès à un nouveau jeu de données de recherche.

## Point de confidentialité

Deux courriels BES contiennent des liens de réinitialisation de mot de passe à usage unique et un
lien de vérification OSF à usage unique existe dans le courriel du 2026-09-09 10:06 — je signale
leur existence et leur emplacement (les courriels cités ci-dessus) sans en recopier la valeur. Le
PDF joint au courriel LISS du 2026-09-09 10:13 n'a pas été ouvert.

---

## Verdict global pour la question du responsable

**Aucune des deux inscriptions actives (LISS, BES) ne débloque un troisième jeu utilisable pour
l'attaque.** Toutes deux sont des panels humains classiques sans sortie de jumeau/agent LLM
appariée publiée par l'archive elle-même — verdict déjà établi indépendamment dans
`resultats/troisieme-jeu-2026-09-12.md` et confirmé ici par le contenu réel des courriels. LISS
est en plus bloqué en amont : la demande d'accès elle-même est en attente d'une réponse du
responsable à une question de l'archiviste, jamais envoyée à ce jour.
