---
name: code-review
description: Use for explicit requests to review code, a diff or revision range, a PR or PR stack, or merge readiness, however small the change. Implementation, routine checks, and prose editing do not trigger this skill.
---

# Code Review

## Scope and effort

Review when requested, including at an agreed milestone. Finishing implementation or running checks is not a request.

Establish exactly what you are reviewing: base and target revisions, or a stable snapshot of uncommitted changes. Also establish what it must satisfy: search the repo and PR for specs, ADRs, docs, and the ticket. Include relevant callers and tests; keep unrelated changes outside the verdict. List the changed files (for example `git diff --stat`) before reading any diff, and set aside generated code, lockfiles, archived or history docs, and rendered output; read diffs only for the rest, and review how the set-aside files are produced or consumed, not their contents. If the change is already merged or closed, report blockers as follow-ups and give no verdict. Review a PR stack once, cumulatively from the bottom base to the top head, tracing interactions between layers.

Scale effort to risk and uncertainty, not line count. Review small, low-risk changes directly. Trust boundaries, data isolation, destructive operations, and money movement warrant deeper investigation even in a tiny diff. Do not stop at the first blocker; keep checking the other risks.

Do not rerun a review on unchanged code unless asked. Delegate distinct questions when independent investigation adds evidence; avoid fixed panels. Give reviewers the scope, requirements, relevant code and review criteria, without the implementation conversation or the author's self-assessment.

## Existing PR comments

On a hosted PR, form your own findings from the diff first. Then read existing reviews and comments, including inline ones, and check each claim against the code. Agreement adds confidence, so note it in your summary or the existing thread, but do not open a new thread on an issue already flagged. Dispute a wrong comment with evidence.

## Posting to a PR

Report in the conversation unless asked to leave the review on the PR. When asked, post only findings that survived verification, each as an inline comment on the changed line where the defect is visible, in the PR whose diff contains that line. In a stack that is the owning layer, not the top PR; use each PR's own diff or `git blame` to find it. GitHub rejects an inline comment on a line outside that PR's diff.

A finding with no fitting line gets its own conversational comment on the PR where it originates, naming any other layers involved. A summary or verdict comment may accompany the findings but never holds one.

## Investigate

Use the relevant lenses without manufacturing findings to fill them:

- **Correctness:** Check the code against each stated requirement; drift from a spec is a failure even when tests pass. Trace callers, boundary inputs, state transitions, concurrency, and error paths, following failures through partial effects and reported completion. Check what tests actually cover.
- **Readability:** Look for misleading names, hidden assumptions, and tangled control flow that make maintenance harder.
- **Architecture:** Check ownership, dependency direction, and compatibility with consumers.
- **Security:** Trace reachable paths from untrusted inputs across trust or privilege boundaries to sensitive operations.
- **Performance:** Assess realistic workloads, repeated calls, resource retention, and growth. Support material regressions with measurements or a concrete cost model.

## Findings and verdict

Block substantiated correctness failures, security vulnerabilities, and material maintainability or performance regressions. Judge against requirements and project conventions; keep preferences, speculative redesign, and unrelated pre-existing issues nonblocking.

Before reporting, check each candidate finding against the code, drop false positives, merge duplicates, mark anything already flagged, and rank the rest by severity. After delegating, have one fresh **verifier** do this with all the reviewers' candidates and any existing PR comments. Report only what survives. Each finding needs its blocking or nonblocking classification, precise location, concrete trigger and consequence, and a targeted remedy. Keep unresolved questions separate from demonstrated defects.

Produce one report identifying what was reviewed and excluded, the effort chosen and whether you delegated (say why if you reviewed a large or high-risk diff alone), the findings, checks, and material limits. A small clean diff needs only a short supported verdict. Unless the change is already merged or closed, end with:

- **Approve:** Requirements are met and no substantiated blockers remain. This assesses readiness; it does not authorize merging.
- **Request changes:** Substantiated blockers remain; name what must change and disclose coverage gaps.
- **Review incomplete:** No blocker is established, but missing evidence prevents a supported decision; name what is needed.

## Repairs

For a standalone review, report and stop. When repairs are authorized, fix blockers with focused checks, verify them against the complete change, and reassess with effort scaled to the new risk. Leave nonblocking suggestions optional.
