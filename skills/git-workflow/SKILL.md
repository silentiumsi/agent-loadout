---
name: git-workflow
description: Use whenever working in any Git repository, even without an explicit request for Git operations. Guides trunk-based development, save point commits, branches, worktrees, and review requests across Git hosts.
---

# Git Workflow

## Choose the working context

Follow repository rules over these defaults. Inspect the branch, working tree, and remotes; identify trunk and existing user changes before changing Git state.

Use short-lived task branches from current trunk and integrate frequently. Continue existing tasks on their branches; branch from another task only for deliberate dependencies. Work directly on trunk only when repository rules and the task permit it.

Use a separate branch and worktree for concurrent work or when the working directory is occupied. Otherwise, a branch is sufficient. Preserve unrelated changes in place rather than stashing or moving them for convenience.

Adapt review terminology, CI, and merge controls to the Git host.

## Build through save points

A **save point** is a coherent commit whose required checks pass. Establish the check baseline before editing; report failing or unavailable checks rather than claiming a passing save point.

```text
Small change → Required checks
                 ├─ Pass → Commit → Next change
                 └─ Fail → Inspect and retain evidence; compare with baseline
                         ├─ Existing failure → Report limitation
                         └─ Regression → Undo your change
                                       → Investigate from save point
```

Separate refactoring, behavior changes, and unrelated fixes into independently passing commits. Keep implementation with its tests. Preserve these save points as meaningful feature history.

Roll back only your changes since the last save point. Preserve user edits, including those in the same files; retain edits whose ownership is unclear.

## Make commits understandable at a glance

Use Conventional Commits with an optional scope and a concrete subject:

```text
fix(auth): reject expired sessions
refactor(auth): extract session validation
```

Use the body for non-obvious motivation and verification limits.

Stage only the intended concern and inspect the staged diff before committing, especially when files contain unrelated edits. Commit and push together within existing authorization; verify the destination branch before pushing. Keep making local save points when pushing is unavailable or unauthorized.

## Open and maintain a focused review request

Prefer local checks first. Open a draft pull request or merge request when requested or when CI or early feedback would help, even before implementation is complete. Mark it ready after local verification and self-review.

Follow the repository’s description template; scale detail to the change. Describe the problem and resulting behavior. Record what was tested and any limits; leave live CI and approval status to the host:

```text
Expired sessions could still access account settings. Reject them before
loading account data and send the user to sign in again.

Adds regression coverage for expired sessions accessing account settings.
Locally tested session expiry; browser sign-in flow not exercised.
```

Keep the title and description aligned with the current diff. Address review feedback in coherent, checked commits.

## Keep integration safe and current

Integrate current trunk frequently; rerun affected checks after integration and conflict resolution. Rebase private branches when useful; coordinate before rewriting shared history. Preserve coherent commits where repository merge policy permits.

All required checks must pass on the revision being merged, with required reviews satisfied. Enforce this through the host’s CI and merge controls. Flag missing enforcement; change workflows or repository settings only within task authorization.

Never merge without an explicit user request, even when checks and reviews pass. Otherwise, leave merging to the user through the host’s UI.

## Finish and clean up

Link the review request and report checks, unresolved issues, and the user’s next action. Distinguish verified results from checks that could not run.

Remove task branches and worktrees only within authorization, after confirming their work is integrated or preserved elsewhere. Check for uncommitted changes and unpushed commits before removal; retain anything whose preservation is uncertain.
