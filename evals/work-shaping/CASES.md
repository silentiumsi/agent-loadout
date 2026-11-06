# Work-shaping cases

This is a diagnostic suite for two failures observed in a local pilot on
2026-11-06 with Codex `gpt-6.1-terra`, CLI `0.166.0`. The briefs are constructed
trials, not production incidents. Criteria were set before the pilot and skill
draft. See [PROTOCOL.md](PROTOCOL.md) for comparison rules and
[RESEARCH.md](RESEARCH.md) for the design sources.

| Case | Observed failure motivating the case | Expected behavior |
| --- | --- | --- |
| `discovery-gate` | The pilot produced nine children before establishing vendor capabilities and postponed source-to-destination freshness validation until after ingestion, deletion, and operational work. | Bound discovery with evidence and a decision; keep affected later work provisional; outline a narrow integrated path rather than a complete assumed platform. |
| `large-export` | The pilot split the endpoint, UI, isolation tests, and full-flow verification into separate items, deferring the first complete customer path. It also expressed epic completion as dependencies on its children. | Deliver a thin customer-to-download path with essential tenant and size constraints included; use child membership for the epic roll-up and prerequisites for execution order. |

Both cases also check grounded context, useful rationale, types, stable IDs,
relationship consistency, scope restraint, and observable completion evidence.
The task instruction supplies the common draft contract to both conditions.
Tracer-bullet slicing is a desired quality under evaluation, not a claim that
the baseline agent violated an explicit command to follow this skill's process.

## Grading limits

Reward Kit runs in a separate verifier environment. Offline checks establish
that the plan exists and source fixtures were preserved. A blinded Claude Code
judge (`claude-opus-5-5`) assesses six semantic criteria against the original
request and trusted project files. It sees neither the condition name nor the
skill. Every criterion must pass; the details retain individual verdicts.
There is no required ticket count, wording, or Markdown layout.

Reference plans in `solution/reference/` are valid examples, not unique answers.
Observed pilot submissions are retained in each task's `calibration/baseline/`.
Accepted skill-condition examples are in `calibration/with-skill/`. Run results
and their limits are recorded separately in [RESULTS.md](RESULTS.md).
Each task's `calibration/near-miss/plan.md` introduces a consequential error into
an otherwise usable reference: assumed vendor capabilities or deferred tenant
isolation. Check grader acceptance of valid alternatives as well as rejection
of these near misses before interpreting scores.
The export case also supplies `calibration/alternative/plan.md`, a single
integrated task without an epic, to check that a valid different breakdown passes.

The suite does not execute the proposed work, establish production readiness,
measure user clarification across turns, or establish broad capability uplift.
It does not cover every supported input shape. A mixed-change pilot produced
a sound breakdown and was not promoted into a scored task, following
`evals/AGENTS.md`'s observed-failure rule. Small single tasks, missing rationale,
project-specific type mappings, and more complex dependency graphs remain
coverage gaps until real use or a trial exposes a specific failure.
