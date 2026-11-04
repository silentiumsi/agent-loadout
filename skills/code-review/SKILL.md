---
name: code-review
description: Use for every explicit request to review repository code, a diff or revision range, a PR, a PR stack, or merge readiness. Invoke even for one-line changes; choose review depth after loading. Implementation, routine checks, and prose editing do not trigger this skill.
---

# Code Review

## Trigger and scope

Start a review when the user requests one. A standing user request to review at a named milestone counts; review once at that checkpoint. Intermediate edits, passing checks, finishing an implementation, and editing skill instructions or other prose do not independently trigger review.

Establish the **reviewed version**: the base and target revision, or an immutable snapshot of the uncommitted change. Review that scope, including relevant callers and tests. Keep unrelated working-tree changes outside the verdict.

For a PR stack, use the bottom PR's base and the top PR's head as one cumulative reviewed version. Trace interactions between layers. Reading individual commits can explain the change; it does not create a separate review or reviewer panel for each PR.

## Choose review effort

Classify risk before choosing effort. Changes to trust or privilege boundaries, data isolation, destructive state transitions, or money movement take the high-risk path even when the diff is one line. Use the smallest review that can support the decision within that path. The five dimensions below are lenses, not a required number of agents.

- **Small, low-risk changes:** review directly. A localized wording change, behavior-preserving cleanup, or straightforward fix usually needs no subagents and a short report.
- **Broader or uncertain changes:** investigate directly and delegate specific independent questions when that adds evidence. Combine related dimensions in one reviewer where useful.
- **High-risk changes:** follow the evidence sequence below. Add specialists only for distinct risks or complexity; launching reviewers alone does not establish coverage.

Use one coordinated review per version, shared across the whole change or stack. Add targeted investigation when new evidence warrants it; do not launch duplicate panels or repeat completed work. Once the review is complete, stop; routine edits and checks do not start another round.

### High-risk evidence sequence

Finding a blocker establishes that changes are needed; it does not complete the review. Complete these steps before returning the verdict:

1. Trace the changed boundary through callers, inputs, and sensitive operations. Inspect the relevant regression tests and establish what they actually cover.
2. Check operational failure and cost behavior. When the project runtime is available, use small local probes with stubs to exercise a failing operation and count relevant operations before and after. Injected callbacks, hooks, and adapters can fail even when the caller contains no explicit raise. Follow the error through propagation, partial effects, and reported completion. A missing test framework is not a reason to skip available runtime probes. When execution is impractical, document the concrete barrier and inspect these flows instead.
3. Obtain one fresh independent check when subagents are available. Ask it to challenge the failure-path and cost analysis, not merely rediscover the first blocker. Combine related questions in this reviewer. Reconcile its evidence with the direct checks; do not rely on agreement alone.
4. Include four short evidence notes in the report: **Boundary and callers**, **Failure behavior**, **Regression coverage**, and **Workload costs**. State the specific behavior checked, the observed result or source evidence, and material verification limits. Keep demonstrated blockers separate from coverage notes.

For costs, compare retained cardinalities and operation counts on the same inputs. An unknown callback or service cost is not zero or negligible: model it as a per-call cost and explain how the number of calls changes. Both implementations scanning N items does not establish equal cost when one dispatches K selected items and the other dispatches all N. One root cause can affect security and performance; merge duplicate findings while retaining the relevant consequences and checks.

## Approval standard

Approve a change when it meets the requirements, preserves or improves code health, and has no substantiated blocking defects. Judge it against project conventions. Perfect code does not exist; aim for continuous improvement.

Block concrete correctness failures, security vulnerabilities, or material maintainability or performance regressions. The change's benefits do not excuse a blocking defect.

Treat personal preferences and optional improvements as nonblocking. Do not demand your preferred implementation when the author's approach works and fits the project. Keep unrelated pre-existing problems outside the approval decision.

## Independent handoff

When delegating, start reviewers without inherited conversation. Give each a distinct question or set of relevant dimensions. Run independent investigations in parallel where capacity allows.

Give each reviewer:

- Its assigned question or dimensions, the relevant criteria below, and the approval standard.
- The reviewed version and scope.
- The requirements and expected behavior, repository guidance, and access to relevant code and tests beyond the diff.
- The findings format below, with instructions to report checks performed and verification limits without editing files.

Withhold the implementation conversation and the author's self-assessment. Give reviewers the evidence needed to judge the change independently, without coaching them toward a verdict. Keep the reviewed version available and unchanged while they work.

If independent review is needed but unavailable, state the verification limit and investigate directly where useful. Return Review incomplete when that missing evidence prevents a supported approval. A direct review can approve a change when its risk and the available evidence support that decision.

## Review dimensions

Trace the change through relevant callers, dependencies, and tests. Use the dimensions relevant to the change; do not manufacture a finding to fill an axis.

### Correctness

Check whether the change meets the requirements and preserves behavior outside its intended scope. Trace boundary values, empty or missing inputs, error paths, state transitions, and concurrency where applicable.

Assess whether tests exercise the changed behavior and would catch its regression. For a bug fix, check both the failure scenario and the regression test. Run focused checks where practical; distinguish observed results from conclusions based on inspection.

### Readability

Check whether a maintainer can understand the code without the author explaining it. Look for misleading names, tangled control flow, hidden assumptions, and comments that obscure or contradict intent.

Assess whether abstractions earn their complexity and whether the change makes the code easier to reason about. Suggest simplifications that remove a concrete comprehension burden; do not equate fewer lines with clearer code or impose personal style over project conventions.

### Architecture

Trace responsibility and dependency boundaries. Check that logic lives with the concept it owns, dependencies flow in the intended direction, and contracts remain compatible with their consumers.

Assess new abstractions, coupling, and duplication in context. For refactors, check whether complexity is reduced rather than relocated. Propose a targeted structural remedy when a boundary causes a concrete maintenance problem; avoid demanding speculative generalization or an unrelated redesign.

### Security

Trace untrusted data across system boundaries to sensitive operations. Check validation, authentication and authorization, injection risks, output encoding, and exposure of secrets or personal data where relevant. Inspect changed dependencies and permissions for added attack surface.

Ground findings in a reachable path and the trust or privilege it crosses.

### Performance

Assess costs at realistic workloads, including algorithmic growth, repeated queries or network calls, unbounded fetching, blocking work, resource retention, and hot-path allocations or rendering.

Use measurements or a concrete workload and cost model to support material regressions. Identify hypotheses that need profiling as unresolved questions.

For selection, batching, or caching changes, compare how many values are retained and how many expensive operations occur before and after. Equal asymptotic complexity does not establish equal cost: a single pass can retain more data or perform many more queries, writes, or deliveries. State the input and selected cardinalities, or use concrete counts, and explain which costs change.

For example, selecting K items from N candidates can remain O(N) while dispatches grow from K to N. Check the counts on the same inputs before concluding that the cost is unchanged.

## Findings and verdict

Produce one report for the reviewed version. Verify findings against the code, merge duplicates, and resolve conflicting recommendations using evidence and the approval standard. Do not count reviewer agreement as proof or discard a substantiated issue because only one reviewer found it.

Order findings by impact, with blockers first. For each finding, include:

- **Classification and axis:** Blocking or nonblocking, and the relevant review dimension.
- **Location:** A file and the smallest useful line range in the reviewed version.
- **Evidence and consequence:** The concrete trigger or scenario, what goes wrong, and why it matters.
- **Remedy:** A targeted correction or direction that addresses the problem without prescribing an unnecessary rewrite.

Keep unresolved questions separate from demonstrated defects. State what evidence would resolve them; do not inflate uncertainty into a blocker or silently treat it as verified behavior.

Identify the reviewed version and report checks performed and material verification limits. Scale the report to the change. A small clean diff needs a short supported verdict; a high-risk report includes the coverage above. Do not substitute a list of reviewer roles for that evidence.

End with one verdict:

- **Approve:** The change meets requirements, preserves or improves code health, and has no substantiated blockers. Nonblocking suggestions may remain.
- **Request changes:** One or more substantiated blockers remain. Name what must be addressed.
- **Review incomplete:** Missing context, coverage, or verification prevents a supported approval decision. Name what remains unverified and what is needed to finish.

When a substantiated blocker and missing coverage coexist, return Request changes and report the remaining coverage gaps. Use Review incomplete when missing evidence prevents a decision and no blocker has been established.

A review verdict assesses readiness; it does not authorize merging.

## Repair and re-review

For a standalone review request, deliver the report and stop. When repair work is authorized, the implementing agent addresses blockers with focused fixes and relevant checks. If you own both review and repair, make those fixes directly, then assess the new reviewed version. Delegated reviewers remain read-only. Leave nonblocking suggestions optional.

Authorization to repair review findings includes focused verification of the repairs and reassessing readiness of the revised change.

If a finding is disputed, resolve it against the requirements and code evidence. Record why it was dismissed or reclassified rather than silently dropping it.

When re-review is requested or already authorized, establish a new reviewed version and choose effort again. Verify the repairs and their effects on the complete change. A minor wording adjustment does not justify repeating a panel; a changed trust boundary or substantial redesign may require broader investigation. If delegating again, use fresh reviewers and provide the requirements, new reviewed version, and issues to verify, without prior verdicts or the author's self-assessment.

Track each previous blocker as resolved, still present, or dismissed with evidence. Declare the change ready only when the revised version earns an Approve verdict under the approval standard. If blockers or material review gaps remain, report them explicitly.
