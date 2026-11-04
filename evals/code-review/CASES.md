# Code review cases

These are regression cases: each exists because a specific failure was observed.
They show whether that failure returns, not how well the skill reviews code. No
case currently tests whether reviews catch defects.

## Cases

| Task | Failure it guards against | Expected behavior | Grading limits |
| --- | --- | --- | --- |
| small-change | Codex launched five reviewers to review a docstring change. | Review the change directly or with at most one reviewer, in one round, and reach a supported clean verdict. | The change is deliberately trivial, so this says nothing about effort on substantive changes. |
| completion-checkpoint | Codex launched five reviewers on finishing an implementation nobody asked to have reviewed. | Implement the change without launching reviewers or issuing a formal readiness review. | Tests one implementation request. It does not cover reviews at an agreed milestone. |

## Grading

Each task uses a separate Reward Kit verifier with private references and judge
criteria under `tests/`. Agents receive only source fixtures and natural requests.

- **`checks`:** offline checks that review-only tasks leave the source unchanged and
  that requested behavior works.
- **`review`:** a Codex judge reads the agent's tool calls and results, including
  child sessions. It scores `quality` and `orchestration` in small-change, and only
  `orchestration` in completion-checkpoint.

All criteria must pass. Reports of launching reviewers or running checks do not
establish those actions; the judge relies on the recorded tool calls.

Before running, export `CODEX_AUTH_JSON` with the contents of the
ChatGPT-authenticated `~/.codex/auth.json` created by `codex login`.
