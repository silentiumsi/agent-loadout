# Pilot protocol — before skill drafting

Capability diagnosis, not representative measurement. Three constructed briefs target
uncertainty-gated discovery, a large end-to-end change, and a mixed bundle. No production
incident is claimed. Candidate tasks stay in scratch until a trial demonstrates a specific
failure, per evals/AGENTS.md. Criteria in each task's `tests/` were frozen before
inspecting pilot output.
All required semantic criteria and source preservation must pass; aggregate quality cannot
compensate for a missing invariant. No exact output format beyond a Markdown artifact.

Pilot: one attempt per case, Codex gpt-6.1-terra CLI 0.166.0. This is diagnostic only.
After grader validation, compare the same cases with and without the local skill using
identical agent settings and fixtures; block regressions on criteria passed by baseline.
Timeout is a behavioral failure if the agent ran; setup failures are invalid attempts,
reported separately and rerun once after the infrastructure defect is repaired. No
selective behavioral retries. Inspect all traces and verify actual skill loading.
No held-out claim: all pilot cases are development cases. A passing small suite supports
only tested behaviors, not generalization. Grader calibration requires a valid alternative
and deliberate near misses, not only an oracle answer.

## Reproduce

From the repository root, use the setup in [../README.md](../README.md):

```sh
harbor run --config evals/work-shaping/baseline.yaml
harbor run --config evals/work-shaping/with-skill.yaml
harbor run --config evals/work-shaping/baseline.yaml --agent oracle
```

The configs use Codex only, matching the pilot; there is no Claude Code
implementation comparison. The separate verifier uses Claude Code for judging.
Both configs retain the repository default of 16 concurrent trials.

To exercise a calibration submission, copy its task into a fresh scratch
directory, replace only `solution/reference/plan.md`, and run the oracle on
that copy. For example, with an unused destination:

```sh
cp -R evals/work-shaping/tasks/large-export .scratch/export-near-miss
cp .scratch/export-near-miss/calibration/near-miss/plan.md .scratch/export-near-miss/solution/reference/plan.md
harbor run --config evals/work-shaping/baseline.yaml --path .scratch/export-near-miss --agent oracle
```

Use `calibration/alternative/plan.md` for the valid export alternative, or
`calibration/baseline/plan.md` to replay an observed baseline submission.
Expected verdicts are all-pass for reference/alternative plans and failure for
the near misses. Inspect the individual failed criteria, not just the aggregate.
