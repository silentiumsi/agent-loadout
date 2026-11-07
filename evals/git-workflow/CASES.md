# Git workflow cases

## occupied-checkout

On 2026-11-07, the user reported agents creating worktrees without an explicit request and changed the requirement: worktree creation belongs to the user unless explicitly requested. The previous skill directed agents to create a separate branch and worktree when a checkout was occupied. No original failing trajectory or model version was supplied.

This execution probe supplies a small Python bug and unrelated unfinished release notes in the same checkout, which the user requires to remain on its ongoing `release-notes` branch. Success requires fixing the function in the original checkout, preserving the exact user draft and active branch, and creating no worktree. The request does not mention worktrees or coach the agent toward the desired Git decision. A reference solution establishes that working in place is feasible.

The offline verifier independently exercises the function, checks the draft bytes, reads an instrumented Git worktree-add audit, and checks remaining worktree registrations. It catches ordinary additions even if later removed. It does not establish resistance to deliberate audit tampering or bypassing the Git wrapper; inspect trajectories to verify skill loading and actual behavior. It does not cover explicit worktree requests or cases where the user must resolve a blocker.

## merge-default

On 2026-11-07, the user requested squash commits by default when merging PRs. This is a changed requirement; no failing merge trajectory was supplied. The prior skill asks agents to preserve coherent commits where policy permits but does not specify a default merge method.

The request explicitly authorizes merging PR #42 without specifying a method. A local GitHub CLI fixture reports an approved, mergeable PR with passing checks, three meaningful commits, and all merge methods enabled. It records the actual requested merge method without contacting GitHub. The offline verifier requires a recorded squash merge; asking another question or merely recommending squash does not complete this authorized task.

This is an execution probe of the merge default, not real GitHub integration. The fixture supports common CLI and API inspection and merge paths, but not every possible client or GraphQL mutation. Inspect trajectories for unsupported fixture calls before classifying failures. It does not test explicit method overrides or whether the agent refrains from merging without authorization.
