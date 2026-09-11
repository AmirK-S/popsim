# R7 — addendum de reprise, 10 septembre 2026

**Reprise entière autorisée par l'utilisateur.** Les dépendances sont la disponibilité GPU/mémoire après R2b et la prise en compte du plan corrigé ci-dessous, pas une nouvelle demande d'autorisation. Aucun nouveau modèle téléchargé. Aucune conversion ni inférence R7 exécutée pendant cette préparation ; R2b reste exclusif.

Cet addendum corrige les affirmations concernées du brouillon local `r7-preenregistrement.md`, sans modifier son fichier, ses cellules ou ses seuils. Il reste local et non publié. Empreinte du plan original contrôlée après les travaux : `c7c1fa35ace4c73547b299b13ec9c5ee5c53339cb6a5fb2c7f6c8a0f709933bc`.

## Corrections au plan

1. **Lineage (§2–4).** Remplacer « chaîne fermée sans trou / une seule étape sépare deux lignes » par : « quatre checkpoints publiés de la famille Instruct, dont l'appariement direct n'est pas complètement documenté ». Instruct-SFT démarre depuis Think-SFT (§5.2.2 du rapport) ; le RL final a été essayé sur deux candidats DPO (§5.4.1). Base/SFT agrège donc des phases supervisées ; le lien exact DPO publié → final publié reste à établir. Le champ `base_model` ne certifie pas l'identité du checkpoint d'initialisation. [Rapport officiel Olmo 3, §5](https://arxiv.org/html/2512.13961v1#S5), déjà consulté lors de l'audit ; aucune revue bibliographique supplémentaire ici.
2. **Portée des résultats.** Tant que le manifeste run/checkpoint d'entrée/poids publiés manque, les quatre points et leurs contrastes sont **descriptifs de checkpoints**, sans attribution causale à SFT, DPO ou RLVR pris isolément. Les hypothèses originales restent archivées comme hypothèses ; leur lecture causale, notamment « la marche est à SFT », ne pourra pas être déclarée confirmée avec cette seule comparaison. Les clés des conditions, mesures, familles et règles de rejet prévues ne sont pas modifiées par cet addendum. Ne pas acquérir d'autres poids pour fabriquer un appariement supposé.
3. **Appels techniques (introduction).** Remplacer « aucun appel de modèle » par « aucun appel expérimental R7 identifié ; trois petites completions techniques Base/SFT/DPO sont conservées dans le cache ». Elles datent du 9 septembre et prédisent huit tokens chacune. Elles ne sont ni des cellules expérimentales R7 ni un benchmark de durée. Aucun résultat scientifique n'en est tiré.
4. **Acquisition et conversion (§12).** Les quatre snapshots safetensors sont complets en présence/taille/structure ; les hashes intégraux restent à vérifier. Trois GGUF passent la validation structurelle. Le final contient zéro tenseur et son chargement historique échoue. Le `rc=0` du convertisseur ne constitue pas une validation.

## Scripts livrés et résultats hors GPU

| Script | Fonction / résultat |
|---|---|
| `analyses/r7_valider_gguf.py` | Stdlib, aucun réseau, mmap ou poids chargé. Lit environ 3,56 Mo de métadonnées par GGUF complet ; budget 16 Mio maximum. Vérifie architecture, type Q8_0, 355 noms/formes de tenseurs, nombre de paramètres, alignement, bornes, chevauchements et taille finale. |
| `analyses/r7_convertir_finale.py` | Préflight seul par défaut. `--execute` déclenche la conversion finale seule si ressources libres. Aucun serveur lancé, aucune promotion/remplacement de l'original. |
| `analyses/test_r7_preparation.py` | 11 tests réussis en environ 4 s : fichiers réels, corruption des descripteurs, troncature, chevauchement, quantification incorrecte, exclusivité, SHA incorrect, export vide à `rc=0`, provenance et conservation temporaire. |

Validation effective des quatre fichiers :

| Condition | Résultat | Types |
|---|---|---|
| Base | PASS | 226 Q8_0 + 129 F32 |
| SFT | PASS | 226 Q8_0 + 129 F32 |
| DPO | PASS | 226 Q8_0 + 129 F32 |
| Final | **FAIL attendu** | 0 tenseur, attendu 355 |

Le validateur retourne 1 si un fichier échoue : le code 1 global de ce contrôle est attendu. PASS signifie conformité structurelle au schéma R7, **pas** intégrité numérique ni réussite d'inférence. Les tests de fichiers tronqués utilisent des fichiers creux temporaires, sans copier les gigaoctets de poids ; les tests d'orchestration simulent le convertisseur et les hashes. Aucun véritable convertisseur exécuté pendant les tests.

## Conversion finale préparée

Entrée figée :

```
~/Library/Caches/popsim-modeles/hf-cache/hub/models--allenai--Olmo-3-7B-Instruct/snapshots/6e5971d9eba42665f5bd5a0fcf047f299ce1dccc
```

Convertisseur local obligatoire au commit propre `c1d0e7a004015f23bc0233470b747b596f29b264`, Python `outils/venv-conversion/bin/python`, `--outtype q8_0`, sans option vocabulaire. Le script impose le mode offline HF/Transformers et ne contient aucun appel de téléchargement.

Avant de convertir, il recalcule **les trois SHA-256 finaux seulement** et exige les OID officiels incorporés au script. Volume : 14 596 063 712 octets, soit environ 13,59 Gio ; pas les quatre modèles. Cette lecture est **différée aujourd'hui** car le pilote R2b PID 65079 et `llama-server` PID 65085 sont actifs au préflight. C'est une précaution I/O pour le run en cours, pas un doute supplémentaire sur les tailles déjà contrôlées.

Le script refuse l'exécution si R2b, un serveur ou un autre convertisseur est actif, avant les hashes et avant toute création de session. Un verrou empêche deux conversions R7 concurrentes. Pendant les hashes et la conversion, il recontrôle les autres processus ; si un concurrent apparaît, il arrête **son propre** convertisseur, jamais R2b ni un serveur externe. Cette surveillance n'est pas un verrou partagé avec R2b : planifier l'exécution après sa fin reste nécessaire.

Sortie isolée dans une nouvelle session `CACHE/outils/r7-final-*/` :

- `Olmo-3-7B-rlvr-Q8_0.partial.gguf` : conservé temporaire même après succès ; l'original invalide n'est jamais ouvert en écriture.
- `conversion.log` : stdout/stderr du convertisseur.
- `provenance.json` : révision, commit, commande, chemins, SHA des scripts et métadonnées sources, trois SHA attendus/recalculés, code retour, validation, SHA du résultat et dates UTC. Statut `VALIDATED_TEMPORARY` seulement après validation et hash ; sinon `FAILED` avec erreur. Un refus avant création de session est signalé en console.

## Commandes et prochain pas

Depuis la racine du projet, exécutés pendant cette séance :

```sh
python3 -B analyses/r7_valider_gguf.py
python3 -B analyses/r7_convertir_finale.py
python3 -B -m unittest discover -s analyses -p test_r7_preparation.py -v
```

**Après fin de R2b**, conversion autorisée, préparée mais non lancée :

```sh
python3 -B analyses/r7_convertir_finale.py --execute
```

La conversion ne déclenche pas l'expérience. Pour la suite expérimentale déjà autorisée : prendre cet addendum comme correction du plan, préparer pilote/contrastes et tests factices R7, vérifier les IDs/BOS/EOS des invites, puis exécuter les contrôles et sondes prévus lorsque le GPU est disponible. Aucune nouvelle demande d'autorisation n'est nécessaire pour ces étapes dans le périmètre accepté ; aucune publication prévue.
