# Code-writing evaluation

Run from the repository root. Only Codex is configured; there are no model
judges or Claude credentials. See CASES.md for evidence and scoring limits.

Validate reference solutions and deliberate failures locally:

```sh
python evals/code-writing/calibrate.py
python evals/code-writing/tasks/select-columns/calibration/check.py
harbor run --config evals/code-writing/baseline.yaml --agent oracle
```

Measure the no-skill baseline before drafting guidance:

```sh
harbor run --config evals/code-writing/baseline.yaml --n-attempts 3
```

Read each trial's verifier/reward-details.json and agent trajectory. Treat the
formatting preference scores separately from functional correctness. The
select-columns control previously saturated; passing it cannot establish uplift.
A candidate comparison must use the same tasks, settings, and trial count with
only local skill availability changed. Selection/discovery is a separate claim.
