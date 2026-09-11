# R6 — preuve d'activation, amendement 429 (2026-09-11)

- SHA-256 document figé `r6-amendement-429-2026-09-11.md` : `96c0a6716fc250d59c0c99f17e162d0abe30285e2f51e2f700c71c553ce51579`.
- SHA-256 `analyses/r6_oracle_distant.py` : `24e1a334d1eef937a60a8f624e6bb6dea74b1f21691b38227a635ac70521d297`.
- SHA-256 `analyses/r6_runner_campagnes.py` : `955fdc57900d2706f1248960ce9dab5adc9d513da9cc5e9a341d2f31ed5de199`.
- Tests exit 0 : `test_r6_amendement_429.py` (113), `test_r6_client.py`,
  `test_r6_runner_campagnes.py`, `test_r6_runner_pilotes.py`,
  `test_r6_reconciliation_resume.py`, `unittest test_r6_analyse_fine
  test_r6_evaluer test_r6_lancer_analyse_fine` (32).
- `--verifier`, 6 modèles de la file QUEUE_READY-20260910 (SHA `115e1b2e15b115f5926c70d47bef8a45ac46fb65315ec9f2bf7b014d14eb36e4`) :
  `amendement_429_actif` true avec `--amendement-429`+`--amendement-429-sha256`, false sans, pour chacun.
- Horodatage d'activation : 2026-09-11T13:51:13+0200.
