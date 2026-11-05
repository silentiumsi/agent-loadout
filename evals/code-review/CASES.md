# Code review cases

These are regression cases: each exists because a specific failure was observed.
They show whether that failure returns, not how well the skill reviews code. The
cases that seed a defect check that a review finds that one defect; none measures
overall detection quality.

## Cases

| Task | Failure it guards against | Expected behavior | Grading limits |
| --- | --- | --- | --- |
| small-change | Codex launched five reviewers to review a docstring change. | Review the change directly or with at most one reviewer, in one round, and reach a supported clean verdict. | The change is deliberately trivial, so this says nothing about effort on substantive changes. |
| completion-checkpoint | Codex launched five reviewers on finishing an implementation nobody asked to have reviewed. | Implement the change without launching reviewers or issuing a formal readiness review. | Tests one implementation request. It does not cover reviews at an agreed milestone. |
| requirements-drift | A review of a stack missed code/spec drift unless an existing comment cited the spec. | Find the accepted ADR, report that the code enforces a 14-day refund window where it requires 30, block, and do not approve. | Regression guard only: the original skill also passed once it loaded, so it does not show the requirements guidance helps. The request names the skill, so skill triggering is not tested. One seeded drift; the ADR is in `docs/`. |
| generated-noise | A review of a 190-file diff spent effort on generated code and archived docs, and never said what it excluded. | Set aside the generated, lock and archived files without reading them wholesale, find the pagination defect, and say in the report what it excluded and whether it delegated. | The `focus` criterion depends on the judge reading tool calls; a path-filtered diff passes. |
| merged-change | Blocking verdicts were given for a change that had already merged. | Find the unvalidated coupon percentage, report it as a follow-up, and give no merge verdict. | Merge state is stated in the request; there is no hosted PR to inspect. The defect is reachable from a user-typed coupon because agents ignored an unreachable one. |

## Grading

Each task uses a separate Reward Kit verifier with private references and judge
criteria under `tests/`. Agents receive only source fixtures and natural requests.

- **`checks`:** offline checks that review-only tasks leave the source unchanged and
  that requested behavior works.
- **`review`:** a Codex judge reads the agent's tool calls and results, including
  child sessions. It scores `quality` and `orchestration` in small-change, only
  `orchestration` in completion-checkpoint, and named per-case criteria in the
  others (see each task's `tests/review.toml`).

All criteria must pass. Reports of launching reviewers or running checks do not
establish those actions; the judge relies on the recorded tool calls.

Before running, export `CODEX_AUTH_JSON` with the contents of the
ChatGPT-authenticated `~/.codex/auth.json` created by `codex login`.
