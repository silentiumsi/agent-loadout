# Code-writing cases

This initial diagnostic suite ports observed readability failures and an existing
behavioral control from agent-sync. It does not estimate everyday failure rates
or establish broad code-design capability. Only Codex is configured; all checks
are deterministic and run offline in a separate Reward Kit verifier.

| Case | Expected behavior | Evidence and grading limits |
| --- | --- | --- |
| format-go | Separate model setup from UI execution, retaining the immediate error check beside its operation. Preserve syntax and all other files. | agent-sync commit 2749753 (2026-10-14), recorded Codex gpt-6.1-sol result: independent-step separation failed. Ported original fixture and request. Checks two exact boundaries in a formatting-only task; no Go compilation or general readability judgment. |
| format-typescript | Separate independent conditions; keep initialization beside its conditional assignment. Preserve syntax and all other files. | Same historical commit and model: initialization grouping failed. Ported original fixture and request. Checks two exact boundaries, including exactly one separating blank line; no TypeScript execution or general readability judgment. |
| select-columns | Preserve CSV behavior, reuse shared field policy, validate before I/O, add observable CLI regression coverage. | agent-sync commit 3d82060 records both baseline and skill passing on 2026-10-29 with Codex gpt-6.1-terra. Retained as a functional control, not evidence of a failure or uplift. Existing mutation checks accept an equivalent CLI and reject reversed/ignored selections. Cannot detect unnecessary wrappers or establish domain-model quality. |

The formatting fixtures retain comments and string literals exactly when comparing
tokens. Layout scores are preference fidelity; behavior and preservation are
reported separately. Baseline layout failures indicate a difference from
Loadout's preferred grouping, not failure to follow a user-specified spacing rule.

Acceptance decision: run three attempts per case before drafting a skill. An
initial candidate must preserve all functional control scores and improve a
repeated readability failure. Isolated gains support only these boundaries;
selection/discovery, fresh generation and transfer remain unmeasured. No held-out
set is claimed: these historical cases are development/regression cases.

Invalid infrastructure attempts are excluded and rerun unchanged; agent timeouts
remain failures. Never use a model result to calibrate its own grader.
