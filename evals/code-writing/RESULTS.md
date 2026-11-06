# Codex comparison, 2026-11-06

Keep the code-writing skill as a preference aid. The comparison shows improved
logical grouping on one TypeScript formatting case, with no detected regressions
in the Go formatting case or CSV behavior control. All nine with-skill trials
found and read the skill through normal discovery. These results provide no
reason to add a hook for these tasks.

| Case | Baseline fully passing | With skill fully passing |
| --- | --- | --- |
| format-go | 3/3 | 3/3 |
| format-typescript | 0/3 | 3/3 |
| select-columns | 3/3 | 3/3 |

In the TypeScript baseline, two attempts left independent conditions together;
one separated initialization from its conditional assignment. All preserved
syntax and other files. Every with-skill TypeScript attempt satisfied both
grouping preferences and preservation checks. All six CSV attempts passed all
six behavior, shared-policy, test-mutation, and fixture-integrity criteria.
Submitted artifacts and trajectories were inspected alongside scores.

Both conditions used Codex CLI 0.166.0, openai/gpt-6.1-terra, three attempts per
case, resumed trajectories, and a concurrency limit of 16. Resolved configs
differed only in local skill availability. Task checksums matched across all
attempts and conditions. Prompts did not explicitly invoke the skill. No Claude
agent or model judge ran. Each condition had nine valid trials and no errors,
timeouts, exclusions, or retries.

The deterministic graders run offline through Reward Kit 0.2.3 in a separate
verifier. Calibration accepted reference solutions and alternate formatting,
and rejected deliberate grouping, preservation, and behavior failures. The final
Docker oracle job passed all three cases. Two earlier oracle validation jobs
exposed grader syntax/workspace setup defects and are excluded; they were fixed
before any Codex trial ran, and the corrected reference run passed 3/3.

Median agent execution time was 21.4 seconds without the skill and 23.5 seconds
with it; these values exclude environment and agent setup. Across nine trials,
baseline input/cache/output tokens were 645,709/589,312/6,823; with-skill totals
were 689,915/628,864/8,082. These small runs do not establish a stable latency or
cost difference; most input tokens were cached.

This is a diagnostic result on three development cases, not an estimate of
success on typical code-writing work. Repeated trials add reliability evidence
within these fixtures, not independent task coverage. There is no held-out
transfer result. The spacing checks measure Loadout's preference, not a baseline
instruction violation. Broader data-model, abstraction, and boundary-design
improvements remain unmeasured; the CSV control was already saturated. Normal
discovery here also does not establish discovery among a full installed skill
catalog. Leave a hook out unless future selection failures establish a need.

The evaluated and final skill SHA256 values, per-trial criteria, matched task
checksums, token counts,
and job names are recorded in [results-2026-11-06.json](results-2026-11-06.json).
The only skill changes after evaluation were line wrapping and trailing blank
line cleanup; wording is unchanged. Raw job directories are local ignored
artifacts under `jobs/`:

- `code-writing-oracle-final-20261106`
- `code-writing-baseline-20261106`
- `code-writing-with-skill-20261106`
