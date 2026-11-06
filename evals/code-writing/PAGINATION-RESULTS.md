# Pagination feature-edit diagnostic, 2026-11-06

A feature request against known dense code exposes the module-layout failure
that an explicit formatting request masked. On the corrected pagination case,
the previous skill passes 0/3 attempts and the refined skill passes 3/3. Every
condition passes all functional, compilation, and public-export checks; the
difference is declaration and class-member spacing.

| Condition | Functional/type/export checks | Layout preferences |
| --- | --- | --- |
| No skill | 3/3 | 0/3 |
| Previous skill, before module-spacing guidance | 3/3 | 0/3 |
| First module-spacing revision | 3/3 | 2/3 |
| Refined whole-module final pass | 3/3 | 3/3 |

The task adds cursor pagination to a generic catalog state module derived from
the observed implementation failure. It requires stable deduplication, retries,
refresh supersession, pending-state safety, workspace isolation, and preservation
of navigation. It never asks for formatting or names the skill. This tests
whether layout guidance survives competing implementation demands.

Failing artifacts retain adjacent interfaces, fields/constructor, and existing
methods despite reading the skill. Adding rules alone was inconsistent: in an
initial comparison, the first revision passed only 1/3 attempts. The final
instruction explicitly asks the agent to inspect each edited module as a whole,
including boundaries beside unchanged definitions, while honoring explicit
formatting limits. A fresh-context blind review found no issues with that skill.

The initial comparison used grader 1.0 and produced combined pass counts of 0/3
without a skill, 0/3 with the previous skill, and 1/3 with the first revision.
Calibration then identified two missing checks from the existing specification:
opaque empty-string cursors and preserved exported names. The reference's
truthy cursor guard was corrected too. All four conditions were rerun against
frozen grader 1.1; the table uses only those matched runs. The task request and
starting module were unchanged. Earlier runs remain separate evidence, not
extra repetitions pooled into the table.

All conditions use Codex CLI 0.166.0, openai/gpt-6.1-terra, three attempts,
resumed trajectories, and the same tools, task, and budgets. Skill availability
or content is the only comparison difference. Corrected task checksums match,
and all nine skill-bearing trajectories read the exact intended skill content
through normal discovery. Only this skill was available; discovery in a larger
catalog remains unmeasured. Exact hashes, criteria, usage, and job names are in
[pagination-results-2026-11-06.json](pagination-results-2026-11-06.json).

The separate offline verifier uses Reward Kit 0.2.3, TypeScript 5.9.3, and Node
22.16.0. Syntax-node checks accept different names and helper structures.
Calibration accepts two working execution designs, renamed helpers, JSDoc, and
CRLF. It rejects compact working code, individual spacing failures, missing
exports, broken cursors/deduplication/navigation, obsolete responses or cleanup,
cross-workspace writes, and invalid types. Both grader versions passed their
Docker oracle runs. Layout checks do not judge within-function paragraphs;
export-name checks do not establish full source compatibility, and runtime
probes cannot prove correctness for every possible schedule or input.

All twelve regression attempts across the four existing cases pass with the
final skill. Controls ran at concurrency eight because of the host's known
Docker subnet pressure; the checked-in configs retain the default sixteen.
Across the initial comparison, corrected comparison, both oracles, and controls,
there were 35 valid trials, no errors, no timeouts, and no excluded attempts.

This is an observed preference-fidelity improvement on one development task,
not a representative success rate, broad code-quality gain, or held-out result.
Three repetitions do not establish reliability. The related formatting and
feature-edit variants count as one source failure, not independent coverage.
