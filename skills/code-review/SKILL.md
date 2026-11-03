---
name: code-review
description: Review code in a fresh context across correctness, readability, architecture, security, and performance. Use before merging a PR or change, after feature implementation or a bug fix, when refactoring existing code, or when asked to review code or a diff.
---

# Code Review

## Approval standard

Approve a change when it improves overall code health and has no substantiated blocking defects. Judge it against the requirements and project conventions. Perfect code does not exist; aim for continuous improvement.

Block concrete correctness failures, security vulnerabilities, or material maintainability or performance regressions. The change's benefits do not excuse a blocking defect.

Treat personal preferences and optional improvements as nonblocking. Do not demand your preferred implementation when the author's approach works and fits the project. Keep unrelated pre-existing problems outside the approval decision.

## Fresh-context handoff

Delegate to five fresh-context subagents: one each for correctness, readability, architecture, security, and performance. Start each without inherited conversation. Run them in parallel where capacity allows, or in batches; keep a separate reviewer for every axis.

Establish the **reviewed version**: the base and target revision, or an immutable snapshot of the uncommitted change. All five reviewers must assess that version. New edits require a new reviewed version.

Give each reviewer:

- Its assigned axis, the corresponding criteria below, and the approval standard.
- The reviewed version and scope.
- The requirements and expected behavior, repository guidance, and access to relevant code and tests beyond the diff.
- The findings format below, with instructions to report checks performed and verification limits without editing files.

Withhold the implementation conversation and the author's self-assessment. Give reviewers the evidence needed to judge the change independently, without coaching them toward a verdict. Keep the reviewed version available and unchanged while they work.

If fresh-context subagents are unavailable, report that the independence requirement could not be met. Label any review performed in the current context as a fallback. It may identify blockers, but cannot earn Approve; without substantiated blockers, return Review incomplete until independent review is available.

## Five-axis review

Each reviewer traces the change through relevant callers, dependencies, and tests using its assigned lens. Use the criteria relevant to the change; do not manufacture a finding to fill an axis.

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

## Findings and verdict

Consolidate the five reviews into one report. Verify findings against the reviewed code, merge duplicates across axes, and resolve conflicting recommendations using evidence and the approval standard. Do not count reviewer agreement as proof or discard a substantiated issue because only one reviewer found it.

Order findings by impact, with blockers first. For each finding, include:

- **Classification and axis:** Blocking or nonblocking, and the relevant review dimension.
- **Location:** A file and the smallest useful line range in the reviewed version.
- **Evidence and consequence:** The concrete trigger or scenario, what goes wrong, and why it matters.
- **Remedy:** A targeted correction or direction that addresses the problem without prescribing an unnecessary rewrite.

Keep unresolved questions separate from demonstrated defects. State what evidence would resolve them; do not inflate uncertainty into a blocker or silently treat it as verified behavior.

Identify the reviewed version, summarize coverage of all five axes, and report checks performed and material verification limits. Say explicitly when an axis has no findings or could not be assessed; a clean report must not conceal missing coverage.

End with one verdict:

- **Approve:** The change improves overall code health and has no substantiated blockers. Nonblocking suggestions may remain.
- **Request changes:** One or more substantiated blockers remain. Name what must be addressed.
- **Review incomplete:** Missing context, coverage, or verification prevents a supported approval decision. Name what remains unverified and what is needed to finish.

A review verdict assesses readiness; it does not authorize merging.

## Repair and re-review

For a standalone review request, deliver the consolidated report and stop. When repair work is authorized, return the findings to the implementing agent, who addresses blockers with focused fixes and relevant checks. The review coordinator tracks their disposition and starts re-review. Keep reviewers out of the repair work; leave nonblocking suggestions optional.

If a finding is disputed, resolve it against the requirements and code evidence. Record why it was dismissed or reclassified rather than silently dropping it.

After repairs, establish a new reviewed version and repeat the five-axis review with new fresh-context subagents. Supply the original requirements, the new reviewed version, and the issues to verify, without the prior reviewers' verdicts or the author's self-assessment. Review the complete revised change, including whether the repairs introduce new problems.

Track each previous blocker as resolved, still present, or dismissed with evidence. Declare the change ready only when the revised version earns an Approve verdict under the approval standard. If blockers or material review gaps remain, report them explicitly.
