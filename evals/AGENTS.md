# Evaluation guidance

## Case records

Add a task only for a specific failure, observed in real use or in a trial; do not add
tasks speculatively to widen coverage. Change an existing task when it grades or
prompts the wrong thing.

When adding, removing, or changing a task, update `evals/<skill>/CASES.md` in
the same change. Record the expected behavior, why the case exists, and grading
limits. Distinguish observed failures from expected behavior or changed
requirements; include dates and model/version evidence when known.

`CASES.md` describes the suite as it stands now. Do not use it as a log of runs,
results, or past changes; Git holds that history.

## Comparable jobs

Use 16 concurrent trials by default for evaluation jobs. Keep this default in
new job configs unless the user requests a different limit. Keep the total across
simultaneous local Docker jobs at 16 trials or fewer: separate verifier networks
can exhaust the default address pools even with spare CPU and memory.

Keep each skill's `with-skill.yaml` and `baseline.yaml` on the same tasks,
models, and settings; only skill availability should differ. Use local skill
sources. For conversational tasks, enable `resume_trajectory` on both agents
and verify each turn with Harbor's native steps.

## Verification

Use Reward Kit in a separate verifier environment; keep deterministic checks
offline. Validate graders with oracle solutions and deliberately wrong outputs
before interpreting model scores. Distinguish setup errors from behavioral
failures, and verify that with-skill trials actually load the skill.

Keep `evals/README.md` focused on running evaluations and reading results.
Update it when those instructions change; put case-specific context in
`CASES.md`.
