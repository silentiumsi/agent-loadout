# Module layout diagnostic, 2026-11-06

A later feature-edit diagnostic is recorded in
[PAGINATION-RESULTS.md](PAGINATION-RESULTS.md); the results below describe the
earlier explicit-formatting experiment.

The implementation failure is real, but the explicit reformatting task did not
reproduce it in three previous-skill attempts. The previous and revised
skills both pass all three attempts on the generic state-module formatting task.
Keep the case as a regression check; it does not establish improvement during
fresh implementation.

The source session used Codex gpt-6.1-sol, CLI 0.166.0, and read code-writing
0.18.0 at 18:48:29 UTC before implementing the module. The skill described
paragraphs within functions but omitted spacing between declarations and class
members. Its final pass also asked the agent to read changed functions rather
than inspect module layout. The revision fills those gaps and illustrates how
to group consecutive variables by purpose without separating every declaration.

The generic fixture removes service-specific types and APIs. Its untouched
layout fails declaration spacing, class-member spacing, and independent-step
spacing while preserving code and keeping related statements together. Harbor's
`nop` agent produces reward 0 on that fixture; the oracle reference produces
reward 1. These are grader-validation results, not model attempts or evidence of
skill uplift.

| Condition | Fully passing module-layout attempts |
| --- | --- |
| No skill | 0/3 |
| Previous skill | 3/3 |
| Revised skill | 3/3 |

All no-skill attempts preserve code and separate declarations, but miss at least
one independent-step boundary; one also misses class-member separation. This
supports the existing skill's value on this task, not additional uplift from
the revision. All nine existing control attempts with the final skill pass.
One TypeScript control could not start because Docker's address pools were
exhausted by concurrent environments. That infrastructure attempt was excluded;
the identical task passed on its replacement attempt. There are no model
timeouts or behavioral retries.

The comparison uses the existing suite's Codex gpt-6.1-terra, CLI 0.166.0,
resumed trajectories, and normal skill discovery. Each condition uses the same
task and settings; only skill availability/content differs. All six previous and
candidate attempts read the intended skill, and their submitted files satisfy
every criterion. The source failure and this comparison use different models;
this is not a controlled reproduction of the source implementation session.

The candidate comparison loaded the revised skill before the blind-review fix
that adds `const generation = target.generation;` to its example. The final skill
has identical instructions and defines that previously unexplained variable.
Regression controls use the final version. Exact versions, task checksums,
criteria, and local job names are in [module-layout-results-2026-11-06.json](module-layout-results-2026-11-06.json).

Calibration accepts the reference and alternative indentation/line endings. It
rejects each independently removed or doubled boundary, blank lines inserted
inside the checked related pairs, changed code, and extra files. The verifier
runs offline in a separate Reward Kit 0.2.3 environment. Its preservation check
compares non-whitespace characters while retaining comments/literals; it does
not parse or compile TypeScript. Layout checks cover named fixture boundaries,
not general readability, all possible groupings, or implementation quality.

No held-out transfer or fresh-generation improvement is claimed. A natural
implementation task with functional checks would be needed to measure whether
the revision prevents this failure while the agent is designing new code.
