# R7 — evaluation descriptive des checkpoints

> **Erratum du 10 septembre 2026.** Toute hypothèse indiquée « non » signifie seulement
> « critère préenregistré non satisfait »; aucune équivalence ni absence d'effet n'en
> découle, car aucune puissance ou marge d'équivalence n'a été préenregistrée. La phrase H4
> ci-dessous exprime une exigence : les deux contrastes **devaient** survivre à Holm pour
> satisfaire H4. Ils n'y survivent pas (`p_Holm=0,0678` et `0,4750`).

**Portee : DESCRIPTIVE checkpoints publies.** Le lineage direct n'est pas etabli ; aucun contraste n'autorise une attribution causale a SFT, DPO ou a l'etape finale.

Tests prescrits : **25**. Executes complets : **25** ; partiels : **0** ; refuses : **0**. Holm est applique separement dans F1--F5 en conservant la taille preenregistree de chaque famille.

H4 est code dans l'orientation des familles : `SFT-DPO < 0` dans F1 et `SFT-Final < 0` dans F2, les deux survivant a Holm.

| famille | contraste | n | statut | difference | p Holm |
|---|---|---:|---|---:|---:|
| F1 | olmo3base - olmo3sft | 75 | EXECUTE | 0,056 | 0,5871 |
| F1 | olmo3sft - olmo3dpo | 74 | EXECUTE | -0,234 | 0,0678 |
| F1 | olmo3dpo - olmo3rlvr | 74 | EXECUTE | 0,112 | 0,3644 |
| F2 | olmo3base - olmo3rlvr | 74 | EXECUTE | -0,077 | 0,5280 |
| F2 | olmo3base - olmo3dpo | 76 | EXECUTE | -0,173 | 0,4750 |
| F2 | olmo3sft - olmo3rlvr | 73 | EXECUTE | -0,119 | 0,4750 |
| F4 | olmo3base - olmo3sft | 77 | EXECUTE | -0,384 | 0,0267 |
| F4 | olmo3sft - olmo3dpo | 76 | EXECUTE | 0,137 | 0,0664 |
| F4 | olmo3dpo - olmo3rlvr | 77 | EXECUTE | -0,099 | 0,1870 |
| F3 | olmo3base contre 1 | 78 | EXECUTE | -0,545 | 0,0002 |
| F3 | olmo3sft contre 1 | 76 | EXECUTE | -0,585 | 0,0002 |
| F3 | olmo3dpo contre 1 | 76 | EXECUTE | -0,370 | 0,0078 |
| F3 | olmo3rlvr contre 1 | 75 | EXECUTE | -0,474 | 0,0011 |
| F5 | olmo3base/gauche contre 1 | 143 | EXECUTE | 0,129 | 0,0080 |
| F5 | olmo3base/centre contre 1 | 146 | EXECUTE | 0,210 | 0,0006 |
| F5 | olmo3base/droite contre 1 | 143 | EXECUTE | 0,164 | 0,0006 |
| F5 | olmo3sft/gauche contre 1 | 141 | EXECUTE | 0,136 | 0,1300 |
| F5 | olmo3sft/centre contre 1 | 140 | EXECUTE | 0,173 | 0,0006 |
| F5 | olmo3sft/droite contre 1 | 140 | EXECUTE | 0,072 | 0,0462 |
| F5 | olmo3dpo/gauche contre 1 | 138 | EXECUTE | 0,180 | 0,0014 |
| F5 | olmo3dpo/centre contre 1 | 136 | EXECUTE | 0,162 | 0,0006 |
| F5 | olmo3dpo/droite contre 1 | 137 | EXECUTE | 0,052 | 0,1945 |
| F5 | olmo3rlvr/gauche contre 1 | 139 | EXECUTE | 0,181 | 0,0014 |
| F5 | olmo3rlvr/centre contre 1 | 138 | EXECUTE | 0,178 | 0,0006 |
| F5 | olmo3rlvr/droite contre 1 | 134 | EXECUTE | 0,071 | 0,1300 |

## Hypotheses

| hypothese | statut | satisfaite |
|---|---|---|
| H1 | EVALUE | non |
| H2 | EVALUE | non |
| H3 | EVALUE | non |
| H4 | EVALUE | non |

## Controles

| condition | cellules | rejets | copies K>=3 | camp constant | statut |
|---|---:|---:|---:|---:|---|
| olmo3base | 894 | 30 | 0 | 0,234 | PASSE |
| olmo3sft | 894 | 57 | 0 | 0,267 | PASSE |
| olmo3dpo | 894 | 61 | 0 | 0,133 | PASSE |
| olmo3rlvr | 894 | 68 | 0 | 0,213 | PASSE |
| referent humain | n.d. | n.d. | n.d. | n.d. | PASSE |
| plancher humain | n.d. | n.d. | n.d. | n.d. | PASSE |
| F contre taux de rejet | n.d. | n.d. | n.d. | 0,600 | PASSE |

Aucune interpretation de nouvelle donnee n'est produite par ce script.
