# R6 — preuve d'activation de l'amendement 429 v2

Horodatage : 2026-09-11T15:18:15+0200. Ne modifie pas la preuve d'activation v1
(`r6-preuve-activation-amendement-429-2026-09-11.md`).

SHA-256 :
- `resultats/r6-amendement-429-v2-2026-09-11.md` (scellé dans le code) :
  `c522950ad25362cd2dfde188ab1faab35ed03e71d68245311822c951b5067d9a`
- `analyses/r6_oracle_distant.py` : `6eb3d17a4473714669d6b5cfbbd76e3013bc2273867dcd3198b53be8939501fc`
- `analyses/r6_runner_campagnes.py` : `ad87c26ed59a714ecf0279c93485fdc78dd22ffbe61d5ec28e858d80d5ca6a39`

Tests rejoués après activation, exit code 0 chacun : `test_r6_amendement_429.py` (136
vérifications, 0 échec) et `test_r6_runner_campagnes.py`.

`--verifier` sur les 6 modèles (`deepseek/deepseek-v4-flash`, `mistralai/mistral-small-2603`,
`qwen/qwen3.7-plus`, `z-ai/glm-5`, `anthropic/claude-haiku-4.5`, `x-ai/grok-4.3`) :
`amendement_429_actif: true` avec `--amendement-429` + `--amendement-429-sha256` corrects ;
`amendement_429_actif: false` sans ces arguments — vérifié pour chacun des 6.
