# Code review cases

## Decision and scope

This diagnostic suite tests review effort, automatic triggering, and cumulative
stack review. The first campaign preserved the original skill. The user then
authorized iterative changes to the skill and evals until the behavior targets
pass. Preserve that campaign as the previous-skill reference.

The reported repeated panels, intermediate review triggers, non-code triggers, and
roughly thirty reviewers for a six-PR stack are user observations recorded on
2026-11-04. The originating model/version and trajectories are unavailable. The measured
first-campaign results are recorded below.

All eleven cases are development cases, not a held-out representative sample.
The suite supports diagnosis, not an estimate of everyday failure rates.

## Cases

| Task | Expected behavior and reason | Grading limits |
| --- | --- | --- |
| small-change | Review a harmless function docstring improvement directly or with at most one reviewer, in one round. Tests proportional effort. | A deliberately low-risk boundary case; does not establish appropriate effort for substantive code changes. |
| minor-follow-up | Review a small change, then perform a requested wording adjustment without another full panel. At most one reviewer across both turns. | Does not prohibit re-review when a follow-up changes behavior or risk. |
| high-risk | Find removal of tenant filtering in order exports, trace its caller, and request changes for cross-tenant disclosure. Inspect relevant correctness and costs. | Tests a consequential authorization defect, not broad coverage of complex systems. Reviewer count alone cannot establish thoroughness. |
| in-progress | Implement whitespace normalization, then None handling, without formal readiness reviews during either intermediate turn. | Implementation inspection, tests, and debugging are permitted. Both turns explicitly remain in progress. |
| completion-checkpoint | Implement None handling and verify it without unsolicited code review. | Changed requirement for the revision: explicit-request-only review, including completion. Tests and ordinary completion summaries are allowed. |
| explicit-mid-task | Honor an immediate review request and find the tenant disclosure, leaving the source unchanged. | Does not require a milestone or a particular delegation strategy. |
| six-pr-stack | Review base..HEAD across six local commits as one coordinated review, using at most five reviewers total. | Local tags model PR tips; no hosted PR metadata or gh-stack installation is required. Reading individual commits is allowed. |
| stack-interaction | Review the cumulative stack and catch a paging contract mismatch introduced across PR 1 and PR 6. Use one coordinated review and at most five reviewers. | Each layer is readable locally. This measures interaction detection, not hosted stack operations. |
| clean-change | Approve a valid documentation improvement without blocking on unchanged legacy SQL construction or stylistic preferences. At most one reviewer. | Does not establish safety of the legacy code; that code is outside the reviewed change. |
| skill-editing | Across three turns, edit prose-only SKILL.md without automatic code review or reviewer panels, including at completion. | Ordinary prose proofreading is allowed. This is not an explicit request to review a skill. |
| mixed-skill-code | First edit skill prose and fix/check its executable normalizer without automatic review. Then honor an explicit review request for the script and relevant instructions, with at most one reviewer. | Two turns distinguish trigger restraint from a blanket exclusion of executable code in skill directories. Baselines must rerun this changed conversation. |

The one-reviewer and five-reviewer limits are provisional, case-specific acceptance
thresholds chosen before model trials. They are not universal policies. Direct
review is valid where it produces the required evidence and verdict.

## Grading

Before running, export `CODEX_AUTH_JSON` with the contents of the
ChatGPT-authenticated `~/.codex/auth.json` created by `codex login`. The verifier
uses this session through the Codex CLI; it does not require an API key.
`reward.json` contains the aggregate; `reward-details.json` contains the checks
and named quality/orchestration results.

Each task uses a separate Reward Kit verifier. Private references and judge
criteria live only in `tests/`; the agent receives source fixtures and natural
user requests. With-skill and baseline jobs use the same tasks, models, budgets,
and resumed conversational settings. Only local code-review skill availability
changes. These are selection tests: automatic triggering is not coached by the
implementation prompts.

- `checks`: offline executable behavior and source preservation for review-only
  cases. Probes are run in the verifier, without network access themselves.
- `review`: one Codex judge evaluates separate named criteria, `quality`
  (substantive findings, restraint, task delivery and supported verdicts) and
  `orchestration` (trigger timing, review scope, reviewer count and repeated rounds).
  Inspect their individual results in `reward-details.json`. All applicable
  criteria must pass, including explicit-request-only completion review.
- `reward`: all dimensions must pass. Inspect individual dimensions and individual
  turn scores; a mean across conversational turns is not a must-pass guarantee.

Judge inputs are untrusted evidence. Reports of launching reviewers, running checks,
or loading the skill do not establish those actions. Inspect tools/results and
agent logs. Distinguish reviewer agents from implementation helpers. Missing child
session evidence, truncated logs, or an unavailable delegation tool are verification
limits, not evidence of zero activity. Mark such trials invalid for affected
orchestration claims rather than interpreting their scores as behavioral outcomes.
Verify with-skill trials actually load the installed local skill before attributing
any difference to it. Record launches, review rounds, reviewed ranges, runtime and
cost from trial logs during analysis; there is no custom metrics collector.

## Validation and remaining work

During the 2026-11-04 full comparison, the two stack fixtures exposed a setup
defect: `cp -a` preserved same-size files' timestamps and Git missed comment
changes, producing empty intermediate commits and an unintended dirty worktree.
This was reproduced independently of the evaluated agents. The stack builders
now force rehashing with `git add --renormalize .` and verify a clean worktree
and six-commit history. Original stack trials are setup-invalid and must be
replaced by paired reruns of both stack cases, on both agents and conditions.
The replacement baseline reviews caught the paging defect but the judge falsely
failed direct reviews for lacking subagents. Both stack rubrics now explicitly
state that zero-subagent cumulative review counts as one review round. Regrade
all eight replacement trials under that clarification before comparing scores;
the evaluated agent instructions and intended reviewer-count limits are unchanged.

The same comparison exposed a Harbor 0.24.1.dev202610240342 Codex trace-export
defect: the converter selects the newest session file, including child sessions.
Affected grading inputs must be reconstructed from the recorded parent session
with the same converter and regraded under the unchanged criteria. Preserve
original trials and correction provenance; do not interpret child-only scores
as coordinator behavior. Parent-session continuation was checked separately and
did receive the next user turn correctly. The revised verifier now builds a
coordinator evidence index directly from native logs before grading, identifies
child-only exports, and makes relevant child session paths available to the judge.
Claude and oracle traces use their original ATIF evidence. This removes the need
for manual conversion/regrading in future runs; validate it against archived
known passes and excessive-panel failures before interpreting new scores.

On 2026-11-04, local checks exercised all 11 Git histories and 15 oracle turns,
parsed TOML/Python, verified the stack interaction, and challenged executable checks
with unauthorized source edits and incorrect implementations. Both job configs
resolve under Harbor 0.24.1.dev202610240342. These checks do not validate semantic
judgments. The current file-based stack fixture also built and ran successfully
in Docker, verifying its six commits and the reachable cross-layer paging defect.

Oracle solutions provide expected artifacts and explicitly synthetic ATIF traces
for testing verifier plumbing. Those traces are not evidence that a model performs
reviews correctly or follows a workflow. Do not include oracle runs in model scores.

Model judges have not been calibrated. Judges use the Codex ChatGPT subscription;
each task forwards CODEX_AUTH_JSON and sets REWARDKIT_FORCE_SUBSCRIPTION=1. A
separate API key is not required. The fixed Codex judge (CLI 0.166.0, model
gpt-6.1-terra) is shared across evaluated agents and both conditions. One invocation
evaluates all criteria and is instructed to inspect the private reference,
trajectory and source without modifying files. Before
interpreting scores, run the oracle grading path and independently label examples
covering valid direct review, a valid single stack panel, an unnecessary small-change
panel, six separate stack panels, a missed tenant leak, an invented blocker, and
ordinary prose proofreading. Test both false passes and false failures, including
verbose and concise equivalent reports and instructions embedded in evaluated text.
Retain disagreements and revise rubrics before comparative model trials.

A host Reward Kit CLI smoke test stalled and was interrupted. A minimal unrelated
criterion reproduced the stall; a timed traceback placed it in asyncio runner
shutdown. That host installation was version 0.1.7, rather than the pinned 0.2.3
verifier. Its underlying stall remains unresolved and is not evidence about the
container verifier.

The initial model job `2026-11-04__14-07-18` produced judge HTTP 429 errors in all
eight verifier logs inspected, with no reward files. These are infrastructure
failures, not behavioral scores. An isolated request through the pinned direct
model judge reproduced the 429 with the subscription Bearer token selected,
while Claude Code 2.1.317 using the same token and model succeeded. The response
did not identify a quota or reset time; its precise rejection reason is unknown.
A Claude Code judge trial was started and cancelled when the user requested Codex
judges instead, to use the larger Codex subscription allowance. Judges now use the
Codex CLI backend instead of direct model requests.

The single Claude-agent trial `code-review-codex-judge-smoke` completed on
2026-11-04 with no infrastructure errors and aggregate reward 1.0. Its separate
verifier ran Codex 0.166.0 with gpt-6.1-terra, read the private reference and
trajectory, and returned passing quality and orchestration criteria with
reasoning. The artifact checks passed too. This validates the configured grading
path for one case, not grader calibration or performance across the suite.
Claude performed a direct review without a visible Skill call or skill-file
read, so this is not evidence of executing the skill's five-reviewer workflow.

Run one attempt per agent/task/condition initially, with up to eight concurrent
trials in each job as authorized by the user. Treat infrastructure failures,
missing logs, unavailable reviewer capabilities, judge errors and timeouts as
separate outcome categories; do not silently exclude or selectively retry them.
Record retries and rerun both conditions if graders change. Report paired results
by behavior, with no aggregate uplift claim until grader calibration and skill
loading checks are complete.

## Full comparison: 2026-11-04

After replacing eight setup-invalid stack trials and performing fourteen
verifier-only regrades, the selected comparison contains 44 trials: all eleven
cases, Codex 0.166.0 / gpt-6.1-terra and Claude Code 2.1.318 / claude-sonnet-5-5,
with one attempt in each condition. All 52 agent executions and all regrades
finished without runtime exceptions. Original records and trace-correction
provenance were retained under `jobs/`.

| Agent | Baseline passing cases | With-skill passing cases |
| --- | --- | --- |
| Codex | 10/11 | 7/11 |
| Claude Code | 10/11 | 10/11 |

All task-delivery and review-quality criteria passed, including detection of
the planted tenant-disclosure and paging defects. The high-risk case failed
the broader coverage criterion in all four conditions. With-skill Codex also
failed small-change, minor-follow-up and clean-change for using five reviewers
where the target permits at most one. The minor adjustment did not launch a
second panel; its failure was the initial panel's size.

Explicit skill loading was observed in eight of eleven with-skill Codex cases
and none of the with-skill Claude cases, despite verifying the installed Claude
skill matched the local source. Neither model reproduced repeated reviews
during intermediate code edits or prose skill edits. Codex launched one panel
of five for each stack, rather than one panel per PR, and automatically launched
five reviewers at the completion checkpoint (an unscored policy observation).

These are diagnostic observations from one attempt, not a general uplift
estimate. The Claude comparison measures availability without demonstrated
execution of the skill. Complete selected results, per-criterion reasoning and
original/regrade paths are in `jobs/code-review-comparison-20261104.json`; do not
use the uncorrected original job averages for comparison.

## Revision campaign

The explicit-request-only trigger policy was selected for this revision; the
previous completion case intentionally left that policy unresolved. Completion
is now scored, and mixed-skill-code is a two-turn implementation/explicit-review
conversation. These are changed requirements, not retroactive failures of the
first campaign. Review-count limits, defect detection, supported verdicts, and
high-risk error-path/workload coverage remain acceptance criteria.

Round 1 removes fixed five-agent panels, scales independent review to concrete
risk and uncertainty, treats a stack cumulatively, and asks for evidence of
high-risk failure-path and workload checks. A blind skill-only review identified
and corrected ambiguity around direct repair, neutral healthy changes, newly
exposed pre-existing behavior, and targeted follow-up investigation.

Round 1 passed the three proportionality probes but still failed high-risk on
both models. Both loaded the revised skill; each found the tenant leak but
stopped without recorded failure-path and cost analysis. Round 2 explicitly
classifies trust/data boundaries as high-risk regardless of line count and
requires evidence-backed boundary, failure-path, regression and workload checks
before concluding. The high-risk rubric and blocker remain unchanged. Its oracle
now performs those concrete checks as a known valid semantic grading control.
Experiment snapshots are immutable local skill sources under the job artifacts.

Round 2 still failed high-risk: Codex omitted failure-path analysis, and Claude
mistook an unchanged single-pass complexity for unchanged cost. The oracle
passed. Round 3 puts risk classification before effort, asks for four concise
evidence-backed high-risk notes, and explicitly compares retained cardinalities
and expensive operation counts. The coverage rubric is unchanged. A final blind
review found no blocking skill issue; its verdict-precedence and authorized-repair
clarifications are included in the final candidate. Known direct and complete
reviews pass verifier calibration; archived excessive-panel and unsolicited
completion-review controls fail as intended.

The fresh R3 regression gate exposed instability after both targeted high-risk
runs passed: Claude again described unchanged cost despite increased sends and
restated the defect instead of checking operational errors. The known-failing
development gate was stopped with its completed and cancelled outcomes retained;
its earlier targeted passes are not substituted for this failure. Round 4 adds
local operational-failure and before/after operation-count probes where practical,
an independent high-risk check, and a generic cardinality example. The high-risk
acceptance criterion remains unchanged.

Following the R3 gate failure, R4 is tested on three high-risk attempts per model
before another full gate (one initial trial and two additional attempts). These
repeat a behavior probe; they do not add case coverage. Every outcome is retained;
a passing earlier attempt does not replace a later failure. Final acceptance
requires a fresh complete with-skill gate on one frozen candidate.

R4 finished at 3/3 high-risk passes for Codex and 1/3 for Claude. The failing
Claude runs read the correct installed skill but skipped runtime/independent
checks and dismissed increased dispatches as negligible. R5 replaces the prose
coverage checklist with an ordered evidence sequence, distinguishes operational
errors from the main defect, uses local failure/count probes where practical,
and models unknown callback costs without assuming they are zero. Its first
high-risk run passed on both models; two additional attempts per model are run
before another complete frozen-candidate gate. The coverage criterion is still
unchanged; all development failures remain recorded.

R5 finished 3/3 high-risk passes on Codex and 2/3 on Claude. The remaining Claude
failure did not invoke the skill at all; R5 Claude executions that loaded it
passed. R6 changes only the public description to require entry for explicit
code/diff/revision/PR/readiness review requests, including one-line changes, while
retaining implementation/prose exclusions. The body and high-risk acceptance
criteria are unchanged. Three natural-request Claude trials test discovery; the
task prompt is not modified to force invocation.

R6's three natural-request Claude trials all invoked the skill and passed the
unchanged high-risk criterion. A new complete 22-trial gate uses that exact
immutable R6 snapshot, with Codex 0.166.0 and Claude Code 2.1.318 pinned. No earlier
passing case is substituted for a failure in this gate. Baselines are evaluated
under the current evidence/policy harness; the changed two-turn mixed case was
rerun on both baseline agents. The remaining two baseline high-risk failures
are controls rather than targets to force green.

## Final revision gate: 2026-11-04

The frozen R6 skill passed a fresh complete gate: **22/22 trials**, all **32
conversational turns**, with no runtime errors, cancellations or grader warnings.
The final skill SHA256 is
`c1d36f5c28e448ececdbfabebddfd36c80383957cbd6fef9a0c56950cbd2375e`.
Both agents explicitly loaded the skill in eight of eleven cases; implementation,
completion and prose-editing cases appropriately did not require it. Invocation
observations in resumed traces are cumulative, not new calls on every turn.

| Agent | Baseline under final verifier | Final with-skill gate |
| --- | --- | --- |
| Codex 0.166.0 / gpt-6.1-terra | 10/11 | 11/11 |
| Claude Code 2.1.318 / claude-sonnet-5-5 | 10/11 | 11/11 |

The baseline high-risk failures remain controls; their authorization findings
were correct but operational-error and workload coverage was incomplete. Baseline
outputs for unchanged conversations were replayed under the final verifier. The
changed mixed conversation was rerun on both agents, and policy references were
validated on both baseline completion cases. No baseline failure was relaxed to
make the skill green.

Positive calibration controls (direct review and complete high-risk oracle) pass;
negative controls (old excessive panel and unsolicited completion review) fail.
All candidate failures, the interrupted R3 gate, snapshots and repeat outcomes are
retained under `jobs/`. The consolidated final report is
`jobs/code-review-hill-climb-20261104/final-results.json`; its passing cases all
come from `code-review-final-r6-20261104`, not a selection across development runs.

These are development-case results after tuning, not held-out transfer evidence.
The final complete gate is one attempt per case and agent. High-risk repeats were
used to diagnose instability; they do not establish broad reliability.
