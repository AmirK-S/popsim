# État des lieux des demandes d'accès à des données — 12 septembre 2026

Vérification en lecture seule (recherche web read-only, aucun envoi, aucun formulaire soumis,
aucun compte créé), et complétion des champs vides dans `demandes/`.

## 0. Correction de comptage

Le répertoire `demandes/` ne contient **pas huit lettres de demande d'accès à des données, mais
sept** : `01-anes.md`, `02-frbny-sce.md`, `03-fichier-contamine-consultation.md`,
`04-fichier-contamine-plateforme.md`, `05-westwood-fichier-apparie.md`,
`06-panel-europeen-elipss.md`, `07-panel-europeen-soep.md`. C'est aussi le compte donné par le
tableau de `demandes/README.md`.

Les autres fichiers numérotés ne sont pas des demandes de données :
- `08-cosignataire-science-politique.md` est une lettre de **cosignature d'article**
  (préenregistrement), pas une demande de données. Elle est de plus **obsolète** : `10-` et `11-`
  la remplacent explicitement pour tout envoi à froid.
- `10-lettre-papier-de-mesure.md` et `11-lettre-experience-de-lecture.md` sont deux lettres de
  cosignature d'article (papier de méthodes ; expérience de lecture), pas des demandes de
  données. Elles ne relèvent pas de cette mission et n'ont pas été modifiées.
- `09-note-pour-simon-cosignataire.md` et `12-cibles-et-ordre.md` sont des notes internes de
  ciblage, pas des lettres.

Si le chiffre huit vient d'un décompte incluant `08-`, il faut le corriger : cette lettre est
remplacée par `10-` et `11-`, elle ne doit plus être envoyée.

## 1. Tableau des sept lettres

| # | fichier | destinataire réel | jeu visé | ce qui manquait | statut au 12/09 |
|---|---|---|---|---|---|
| 01 | anes.md | anes@electionstudies.org | ANES Time Series 2020/2024, module GSS | AFFILIATION, NOM, DATE ; procédure d'accès non vérifiée ; sort du module GSS incertain | **complétée et corrigée** |
| 02 | frbny-sce.md | équipe SCE, NY Fed | stabilité de `userid` entre 4 fichiers publics SCE | AFFILIATION, NOM, DATE ; adresse de destinataire non confirmée | **complétée et corrigée** |
| 03 | fichier-contamine-consultation.md | NY AG, Bureau of Internet and Technology | extrait étiqueté des faux commentaires FCC 2017 | AFFILIATION, NOM, DATE ; canal réel non vérifié | **complétée, canal corrigé (FOIL)** |
| 04 | fichier-contamine-plateforme.md | à choisir (aucune cible) | fichier de répondants frauduleux étiquetés | AFFILIATION, NOM, DATE ; **destinataire lui-même** | **champs complétés, cible toujours manquante** |
| 05 | westwood-fichier-apparie.md | Sean.J.Westwood@dartmouth.edu | fichier humain apparié à l'OSF `ektqr` | AFFILIATION, NOM, DATE | **complétée** |
| 06 | panel-europeen-elipss.md | CDSP, Sciences Po/CNRS | ELIPSS, données individuelles | AFFILIATION, NOM, DATE ; procédure réelle non vérifiée | **complétée, canal corrigé (portail Progedo)** |
| 07 | panel-europeen-soep.md | SOEP, DIW Berlin | SOEP-Core individuel | AFFILIATION, NOM, DATE ; portée de l'exigence d'affiliation non confirmée | **complétée, verdict : très probablement sans issue** |

## 2. Ce qui a été complété partout (7 lettres)

- `[AFFILIATION]` → « I am an independent researcher, with no institutional affiliation. »,
  suivi d'une ligne sur le code et les résultats publics du projet
  (`https://github.com/AmirK-S/popsim`, vérifié public le 12/09) là où la lettre ne le
  mentionnait pas déjà.
- `[NOM ET SIGNATURE]` → « Amir Kellou Sidhoum, independent researcher, popsim project » +
  `aboutdotblank@gmail.com`.
- `[DATE]` → 12 September 2026.

## 3. Ce qui reste uniquement entre les mains d'Amir

- **Lettre 04** : aucune cible n'est choisie. Rien ne peut être vérifié (adresse, procédure,
  formulaire en ligne) tant qu'un nom d'organisation n'est pas fixé.
- **Décider s'il faut vraiment router la lettre 03 par FOIL** (voir §4) : c'est un choix de
  stratégie, pas un point de fait.
- **Lettre 05** : arbitrer avec la lettre 10 (`demandes/10-lettre-papier-de-mesure.md`, hors
  périmètre de cette mission) le risque de double courriel à Westwood sur deux objets — déjà
  signalé dans `demandes/12-cibles-et-ordre.md`, rappelé ici parce que la lettre 05 en fait
  partie.
- Toute décision d'envoi elle-même : rien n'a été transmis, rien ne le sera par cette session.

## 4. Procédures réelles vérifiées (lecture seule), et où elles diffèrent de ce que la lettre supposait

- **ANES (01)** : inscription en libre accès (« Data Registration », courriel puis mot de passe),
  aucune mention trouvée d'un projet à faire approuver pour les fichiers publics. `electionstudies.org`
  reste bloqué (Cloudflare, HTTP 403) depuis cette machine ; solutions de repli confirmées :
  ICPSR (`icpsr.umich.edu/web/ICPSR/series/3`) et SDA Berkeley, qui héberge déjà la documentation
  du fichier 2024 (`sda.berkeley.edu/sdaweb/docs/anes2024full/DOC/hcbk.htm`). **Fait nouveau** : le
  module GSS existe bel et bien, sous le nom « ANES-GSS 2020 Joint Study », publié dans un fichier
  séparé environ 18 mois après le fichier principal ; l'équivalent 2024 est annoncé mais pas encore
  sorti. La lettre demandait « est-ce que ça existe » ; elle demande maintenant directement l'accès
  au fichier joint 2020 et la date du fichier joint 2024.
- **SCE (02)** : aucun contact dédié à la SCE elle-même n'existe ; le canal confirmé est
  `research.publications@ny.frb.org` (`newyorkfed.org/contacts`).
- **NY AG / FCC (03)** : la lettre visait le mauvais canal. Le Bureau of Internet and Technology
  n'a ni courriel ni formulaire dédié ; le canal réel est une **requête FOIL**
  (`ag.ny.gov/i-want/make-foil-request`), donc une démarche administrative formelle et non plus
  une lettre de courtoisie — le texte peut servir de description des dossiers recherchés jointe à
  la requête, mais le dépôt lui-même reste à faire par Amir sur le portail. Aucune annexe de
  données n'a été retrouvée publiée par le procureur. **Alternative gratuite à vérifier d'abord** :
  le jeu Kaggle de Jeff Kao (`github.com/j2kao/fcc_nn_research`), qui donne texte + doublons mais
  probablement pas d'horodatage, d'État ni d'indicateur de fraude confirmé — à inspecter avant de
  déposer une FOIL.
- **ELIPSS (06)** : l'accès réel ne passe pas par un courrier à la CDSP mais par le portail
  **Quetelet-PROGEDO-Diffusion** (`data.progedo.fr`), avec dossier examiné par le Comité
  Scientifique et Technique d'ELIPSS, et un champ « institution de rattachement » obligatoire dans
  le formulaire. Aucune page ne tranche explicitement le cas d'un chercheur indépendant. La lettre
  a été reformulée en question d'éligibilité préalable à la CDSP, pas en demande d'accès directe.
- **SOEP (07)** : confirmé texte à l'appui, `diw.de` : « Individuals (without an institutional
  affiliation) are not permitted to use the SOEP data. » Les modes plus légers (SOEPremote-execution,
  SOEPremote-access, sur site) sont soumis à la même exigence. Aucun mode d'accès sans
  rattachement institutionnel n'a été trouvé.
- **Westwood (05)** : adresse déjà confirmée par le dossier (`demandes/12-cibles-et-ordre.md`),
  rien de nouveau à vérifier ici.

## 5. Est-ce que chaque lettre demande la bonne chose ?

Le critère décisif du projet — des sorties synthétiques appariées individuellement à des
répondants humains — n'est vraiment rempli que par une seule lettre :

- **Westwood (05)** correspond exactement au besoin : le dépôt OSF `ektqr` donne déjà le côté
  synthétique (environ 28 000 réponses générées, 300 profils) ; le fichier humain apparié demandé
  compléterait la paire manquante. C'est la lettre la plus directement alignée avec l'objectif du
  troisième jeu de données.
- **03 et 04** visent un objectif voisin mais différent : un fichier réel de fraude humaine
  (répondants faux ou bannis) avec un taux vrai connu, utile pour valider le détecteur i3, pas pour
  reproduire la comparaison jumeau contre humain. Utile, mais ce n'est pas la même pièce manquante.
- **01, 02, 06, 07** demandent des données humaines pures (ANES, SCE, ELIPSS, SOEP) : elles
  donnent une deuxième ou troisième **population humaine de référence** (plancher de
  réinterrogation, item par item), ce qui sert à généraliser la mesure, mais ne produit aucune
  sortie synthétique appariée. À ne pas présenter comme « le troisième jeu de données » du même
  genre que Twin-2K-500 : c'est un usage différent, légitime, mais distinct.

## 6. Classement bénéfice/effort

1. **ANES (01)** — inscription en libre accès, procédure désormais claire, forte probabilité de
   succès rapide ; donne un module joint directement comparable au GSS. À envoyer en premier.
2. **Westwood (05)** — un seul courriel, adresse confirmée, la pièce la plus alignée avec le besoin
   réel de troisième jeu de données ; réponse incertaine (l'auteur a déjà choisi de ne pas tout
   publier), mais le coût d'essai est nul. À envoyer, en gérant la collision avec la lettre 10.
3. **SCE (02)** — question de documentation, pas d'accès à négocier, réponse probablement rapide ;
   gain limité (clarifie des données déjà en main plutôt que d'en ouvrir de nouvelles).
4. **ELIPSS (06)** — effort moyen, verdict d'éligibilité incertain (silence des pages officielles),
   passage obligé par un portail à champ institutionnel même en cas de réponse favorable.
5. **NY AG / FCC (03)** — désormais une démarche FOIL formelle, effort et délai plus lourds, succès
   incertain (dossier d'enquête, exemptions possibles) ; à tenter seulement après avoir vérifié que
   le jeu Kaggle de Kao ne suffit pas.
6. **Plateforme (04)** — ne peut pas partir tant qu'aucune cible n'est choisie ; effort et
   probabilité de succès non évaluables en l'état.
7. **SOEP (07)** — **jugée sans espoir en l'état** : la page d'accès exclut explicitement les
   chercheurs sans affiliation, sous toutes les formes d'accès vérifiées. À n'envoyer que comme
   question fermée pour mémoire, sans attente de résultat, sauf si un chercheur affilié accepte de
   porter la demande.

Recommandation : envoyer 01 et 05 d'abord ; envisager 02 en complément gratuit ; garder 06 et 03
en réserve ; ne pas investir de temps sur 07 sans un tiers affilié ; ne rien faire sur 04 avant
qu'Amir choisisse une cible.
