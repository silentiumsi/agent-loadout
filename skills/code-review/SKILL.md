---
name: code-review
description: Use for explicit requests to review code, a diff or revision range, a PR or PR stack, or merge readiness, however small the change. Implementation, routine checks, and prose editing do not trigger this skill.
---

# Code Review

## Scope and effort

Review when requested, including at an agreed milestone. Finishing implementation or running checks is not a request.

Establish exactly what you are reviewing: base and target revisions, or a stable snapshot of uncommitted changes. Include relevant callers and tests; keep unrelated changes outside the verdict. Review a PR stack once, cumulatively from the bottom base to the top head, tracing interactions between layers.

Scale effort to risk and uncertainty, not line count. Review small, low-risk changes directly. Trust boundaries, data isolation, destructive operations, and money movement warrant deeper investigation even in a tiny diff. Do not stop at the first blocker; keep checking the other risks.

Do not rerun a review on unchanged code unless asked. Delegate distinct questions when independent investigation adds evidence; avoid fixed panels. Give reviewers the scope, requirements, relevant code and review criteria, without the implementation conversation or the author's self-assessment.

## Existing PR comments

On a hosted PR, read existing reviews and comments first, including inline ones. Check each claim against the code. Agreement adds confidence, so note it in your summary or the existing thread, but do not open a new thread on an issue already flagged. Dispute a wrong comment with evidence.

## Investigate

Use the relevant lenses without manufacturing findings to fill them:

- **Correctness:** Trace requirements, callers, boundary inputs, state transitions, concurrency, and error paths, following failures through partial effects and reported completion. Check what tests actually cover.
- **Readability:** Look for misleading names, hidden assumptions, and tangled control flow that make maintenance harder.
- **Architecture:** Check ownership, dependency direction, and compatibility with consumers.
- **Security:** Trace reachable paths from untrusted inputs across trust or privilege boundaries to sensitive operations.
- **Performance:** Assess realistic workloads, repeated calls, resource retention, and growth. Support material regressions with measurements or a concrete cost model.

## Findings and verdict

Block substantiated correctness failures, security vulnerabilities, and material maintainability or performance regressions. Judge against requirements and project conventions; keep preferences, speculative redesign, and unrelated pre-existing issues nonblocking.

Before reporting, check each candidate finding against the code, drop false positives, merge duplicates, mark anything already flagged, and rank the rest by severity. After delegating, have one fresh **verifier** do this with all the reviewers' candidates and any existing PR comments. Report only what survives. Each finding needs its blocking or nonblocking classification, precise location, concrete trigger and consequence, and a targeted remedy. Keep unresolved questions separate from demonstrated defects.

Produce one report identifying what was reviewed, the findings, checks, and material limits. A small clean diff needs only a short supported verdict. End with:

- **Approve:** Requirements are met and no substantiated blockers remain. This assesses readiness; it does not authorize merging.
- **Request changes:** Substantiated blockers remain; name what must change and disclose coverage gaps.
- **Review incomplete:** No blocker is established, but missing evidence prevents a supported decision; name what is needed.

## Repairs

For a standalone review, report and stop. When repairs are authorized, fix blockers with focused checks, verify them against the complete change, and reassess with effort scaled to the new risk. Leave nonblocking suggestions optional.
