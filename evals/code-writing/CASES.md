# Code-writing cases

This diagnostic suite covers observed readability failures and an existing
behavioral control, including historical cases ported from agent-sync. It does not estimate everyday failure rates
or establish broad code-design capability. Only Codex is configured; all checks
are deterministic and run offline in a separate Reward Kit verifier.

| Case | Expected behavior | Evidence and grading limits |
| --- | --- | --- |
| format-go | Separate model setup from UI execution, retaining the immediate error check beside its operation. Preserve syntax and all other files. | agent-sync commit 2749753 (2026-10-14), recorded Codex gpt-6.1-sol result: independent-step separation failed. Ported original fixture and request. Checks two exact boundaries in a formatting-only task; no Go compilation or general readability judgment. |
| format-typescript | Separate independent conditions; keep initialization beside its conditional assignment. Preserve syntax and all other files. | Same historical commit and model: initialization grouping failed. Ported original fixture and request. Checks two exact boundaries, including exactly one separating blank line; no TypeScript execution or general readability judgment. |
| paginate-state-module | Add working cursor pagination while separating module declarations and class members. Preserve refresh races, retries, navigation, and cached workspace isolation. | Feature-edit reproduction of the same observed implementation failure as format-state-module, with competing functional demands and no formatting request. Codex gpt-6.1-terra CLI 0.166.0 trials on 2026-11-06 retained inherited dense layout after reading the skill. TypeScript AST checks declaration/member boundaries, independent of identifiers or helper design; runtime checks exercise the specified API. Does not grade within-function paragraphs or claim broad code quality. Export checks cover names, not complete source compatibility. |
| format-state-module | Separate top-level declarations and class members; separate cache lookup from selection, guards from work, accumulation from return, and request setup from execution. Keep lookup/guard and operation/staleness-check pairs together. Preserve tokens and other files. | Observed 2026-11-06 in a state module produced with Codex gpt-6.1-sol, CLI 0.166.0, after reading code-writing 0.18.0. The generic catalog-state reproduction fails all three layout groups before reformatting; the source project used a formatter. Checks exact fixture boundaries, not arbitrary module quality, compilation, or fresh generation. |
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

For format-state-module, the source session is
`01a1b230-86f7-74d0-9567-dc69e10b3dea`: the 18:48:29 UTC tool call reads
code-writing 0.18.0 before implementation. The fixture removes service-specific
API types and retains the observed declaration, class-member, and statement
layout. The original failure is evidence from implementation; this task asks for
formatting and cannot reproduce implementation-time competing demands.

Before revising guidance, compare three previous-skill and three candidate
attempts on the same fixture and settings. Require all preservation checks to
pass and more fully passing candidate attempts, with no regressions in the
existing controls. If the previous skill already passes, report the reproduction
as saturated rather than claiming measured improvement. Calibration tests each
boundary independently, alternative indentation and line endings, and altered
syntax/extra files. These checks measure preference fidelity, not behavior.

For paginate-state-module, freeze the task, grader, and skills before trials.
Compare three no-skill, previous-skill, and revised-skill attempts with matching
settings. Primary outcome is functional/type correctness plus declaration and
class-member spacing; report all dimensions separately. A revision gain requires
more fully passing attempts with no functional regressions. Preserve failures;
do not make the prompt more directive after seeing a score. This is a development
diagnostic derived from the source failure, not a held-out or representative case.

The pagination grader uses TypeScript 5.9.3 syntax nodes for neighboring
module declarations and class members, plus strict compilation and runtime
contract probes. Calibration accepts different helper names and two execution
designs; it rejects compact working code, isolated spacing misses, missing
exports, incorrect deduplication/cursors, obsolete cleanup, cross-workspace
writes, and invalid types. Version 1.1 also checks opaque empty-string cursors
and exported type names, which were missing from the initial grader; compare
conditions only within the same grader version. These are related development
variants of one observed failure, not additional independent case coverage.
