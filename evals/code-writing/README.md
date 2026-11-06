# Code-writing evaluation

Run from the repository root. Only Codex is configured; there are no model
judges or Claude credentials. See CASES.md for evidence and scoring limits.

Validate reference solutions and deliberate failures locally:

```sh
python evals/code-writing/calibrate.py
python evals/code-writing/tasks/format-state-module/calibrate.py
python evals/code-writing/tasks/select-columns/calibration/check.py
harbor run --config evals/code-writing/baseline.yaml --agent oracle
```

The pagination grader compiles and runs TypeScript. Its Docker verifier includes
the pinned compiler; local calibration additionally needs Node and TypeScript:

```sh
npm install --prefix .scratch/code-writing-compiler --no-audit --no-fund typescript@5.9.3
NODE_PATH="$PWD/.scratch/code-writing-compiler/node_modules" python evals/code-writing/tasks/paginate-state-module/calibrate.py
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

Compare with the local skill, keeping the same Codex agent and settings:

```sh
harbor run --config evals/code-writing/with-skill.yaml --n-attempts 3
```

This condition installs the skill for normal discovery; the task requests do not
explicitly invoke it. Inspect trajectories to verify that the agent reads it.

The initial Codex comparison and its limits are in [RESULTS.md](RESULTS.md).
The module-layout diagnostic and its limits are in
[MODULE-LAYOUT-RESULTS.md](MODULE-LAYOUT-RESULTS.md).

The feature-edit comparison is in [PAGINATION-RESULTS.md](PAGINATION-RESULTS.md).
