---
name: code-review
description: Use for explicit requests to review repository code, a diff or revision range, a PR, a PR stack, or merge readiness, including one-line changes. Implementation, routine checks, and prose editing do not trigger this skill.
---

# Code Review

## Scope and effort

Review when requested, including at an agreed milestone. Finishing implementation or running checks does not independently request a review.

Establish the **reviewed version**: base and target revisions, or a stable snapshot of uncommitted changes. Include relevant callers and tests; keep unrelated changes outside the verdict. Review a PR stack cumulatively from the bottom base to the top head, tracing interactions between layers.

Scale effort to risk and uncertainty, not line count. Review small, low-risk changes directly. Trust boundaries, data isolation, destructive operations, and money movement warrant deeper investigation even in a tiny diff. Finding one blocker does not establish coverage of the remaining risks. For high-risk changes, complete the evidence sequence below before giving a verdict.

Use one coordinated review per version. Delegate distinct questions when independent investigation adds evidence; avoid fixed panels and duplicate work. Keep reviewers from editing the reviewed change; allow isolated verification artifacts. Give them the scope, requirements, relevant code and review criteria without the implementation conversation or author's self-assessment. Reconcile their findings against evidence, not agreement. State when unavailable evidence prevents a supported decision.

### High-risk evidence sequence

Finding a blocker establishes that changes are needed; it does not complete the review. Complete these steps before returning the verdict:

1. Trace the changed boundary through callers, inputs, and sensitive operations. Inspect the relevant regression tests and establish what they actually cover.
2. Check operational failure and cost behavior. When the project runtime is available, use small local probes with stubs to exercise a failing operation and count relevant operations before and after. Injected callbacks, hooks, and adapters can fail even when the caller contains no explicit raise. Follow the error through propagation, partial effects, and reported completion. A missing test framework is not a reason to skip available runtime probes. When execution is impractical, document the concrete barrier and inspect these flows instead.
3. Obtain one fresh independent check when subagents are available. Ask it to challenge the failure-path and cost analysis, not merely rediscover the first blocker. Combine related questions in this reviewer. Reconcile its evidence with the direct checks; do not rely on agreement alone.
4. Include four short evidence notes in the report: **Boundary and callers**, **Failure behavior**, **Regression coverage**, and **Workload costs**. State the specific behavior checked, the observed result or source evidence, and material verification limits. Keep demonstrated blockers separate from coverage notes.

For costs, compare retained cardinalities and operation counts on the same inputs. An unknown callback or service cost is not zero or negligible: model it as a per-call cost and explain how the number of calls changes. Both implementations scanning N items does not establish equal cost when one dispatches K selected items and the other dispatches all N. One root cause can affect security and performance; merge duplicate findings while retaining the relevant consequences and checks.


## Investigate

Use the relevant lenses without manufacturing findings to fill them:

- **Correctness:** Trace requirements, callers, boundary inputs, state transitions, concurrency, and error paths. Check what regression tests actually cover. Follow failures through partial effects and reported completion, including failures in dependencies or callbacks.
- **Readability:** Look for misleading names, hidden assumptions, tangled control flow, and abstractions that make maintenance harder. Suggest simplification for a concrete comprehension problem, not personal style.
- **Architecture:** Check ownership, dependency direction, and compatibility with consumers. Address concrete coupling or misplaced responsibility without demanding speculative generalization or unrelated redesign.
- **Security:** Trace reachable paths from untrusted inputs across trust or privilege boundaries to sensitive operations. Check authorization, validation, injection, and exposure where relevant.
- **Performance:** Assess realistic workloads, repeated queries or calls, resource retention, and growth. Support material regressions with measurements or a concrete cost model.


## Findings and verdict

Block substantiated correctness failures, security vulnerabilities, and material maintainability or performance regressions. Judge against requirements and project conventions; keep preferences, optional improvements, and unrelated pre-existing issues nonblocking. A change's benefits do not excuse a blocker.

Verify findings, merge duplicates, and order by impact. Each finding needs its blocking or nonblocking classification, precise location, concrete trigger and consequence, and a targeted remedy. Keep unresolved questions separate from demonstrated defects and identify evidence needed to resolve them.

Produce one report identifying the reviewed version, findings, checks, and material limits. Scale detail to the change; a small clean diff needs only a short supported verdict. End with:

- **Approve:** Requirements are met, code health is preserved or improved, and no substantiated blockers remain.
- **Request changes:** Substantiated blockers remain; name what must change and disclose any remaining coverage gaps.
- **Review incomplete:** No blocker is established, but missing evidence prevents a supported decision; name what is needed.

The verdict assesses readiness and does not authorize merging.

## Repairs

For a standalone review, report and stop. When repairs are authorized, fix blockers with focused checks and reassess the revised version. Leave nonblocking suggestions optional.

Track previous blockers as resolved, still present, or dismissed with evidence. Verify repairs and their effects on the complete change, scaling effort to the new risk. Minor adjustments do not require another panel; substantial changes may need fresh independent investigation.
