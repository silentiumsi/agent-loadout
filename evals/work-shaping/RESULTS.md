# Work-shaping diagnostic results

Run date: 2026-11-06. Criteria and pilot baseline preceded the skill draft.
The two retained cases passed 0/2 without the skill and 2/2 with it. No criterion
passed by the baseline regressed. Both skill-condition traces explicitly read
`/root/.agents/skills/work-shaping/SKILL.md` through normal skill discovery.

| Case | Condition | All-pass score | Failed criteria | Agent execution | Output tokens |
| --- | --- | --- | --- | --- | --- |
| `discovery-gate` | baseline | 0 | first_path | 46.1s | 2,024 |
| `discovery-gate` | skill | 1 | none | 57.3s | 2,775 |
| `large-export` | baseline | 0 | vertical_first, sequence_parallel | 44.0s | 1,908 |
| `large-export` | skill | 1 | none | 54.8s | 2,244 |

The discovery baseline deferred early source-to-store freshness evidence behind
broader ingestion, deletion and operational work. The export baseline split the
endpoint, page and verification into separate tickets. The skill-condition
plans instead include integrated paths and explicit follow-on sequencing.
Inspect the actual plans under each task's `calibration/baseline/` and
`calibration/with-skill/`; scores alone do not show whether a plan is useful.

## Conditions and validation

- Harbor `0.24.1.dev202610240342`; Codex `0.166.0`, model `openai/gpt-6.1-terra`;
  subscription authentication; one attempt per case; 900-second agent budget;
  local Docker; configured concurrency 16, with two retained trials per condition.
- Judge: Claude Code with `anthropic/claude-opus-5-5`, separate verifier,
  condition-blind staging. Judge CLI installation follows the existing repository
  pattern and is not version-pinned, which limits future exact reproduction.
- Prompts, task budgets, environment files and all grader files were checked
  byte-identical across the two retained baseline and skill conditions. Only
  skill availability differed. The baseline job also contained the mixed-change
  pilot, which passed and was not promoted into a permanent scored task.
- Retained reference plans passed 2/2; deliberate near misses failed 2/2 on the
  intended safety/assumption criteria. A valid one-task export alternative with
  no epic passed. An additional mixed-change alternative reversed implementation
  ordering and also passed during pilot calibration.
- All completed trials had zero setup or execution exceptions and no behavioral
  retries. One initial launch aborted at Harbor's environment-variable
  confirmation before executing any trial; it is outside the comparison.
- The skill passed structural validation and a fresh-context blind review. The
  review prompted one clarification about identifying external blockers before
  the skill-condition runs.

Agent execution excludes container setup and judging. Token counts are the
agent's reported output tokens, not total system cost; grader usage and human
review effort are not included. Setup dominated the roughly five-minute pilot
job. The paired sample is too small to estimate reliability, resource savings,
or a meaningful population effect. These are development cases used to design
the skill, not held-out evidence. Missing rationale, single-task restraint,
project-specific types and conversational reshaping remain unmeasured.

Tested skill SHA-256: `fd34243bd2e554f7d17ed6ea7dbb9dfa28d5bcd47d9a268bb31fb78dd33a85f8`.

Local job evidence (ignored by Git): `jobs/work-shaping-pilot-baseline-run/`,
`jobs/work-shaping-with-skill/`, `jobs/work-shaping-oracle-calibration/`,
`jobs/work-shaping-near-miss-calibration/`, and
`jobs/work-shaping-export-alternative/`. The shared case inputs are now under
`evals/work-shaping/tasks/`; scratch candidate paths in the original job configs
were used only for the pilot. Follow [PROTOCOL.md](PROTOCOL.md) to rerun.
