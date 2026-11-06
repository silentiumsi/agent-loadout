---
name: work-shaping
description: Shape discovery, a bundle of changes, or one large change into small, sequenced work-item drafts for coding agents, with rationale, types, parent relationships, and dependencies. Use when breaking down or slicing work for implementation; creating tracker issues is outside this skill.
---

# Work Shaping

Turn the request into bounded work another agent can pick up and verify. Start
with the intended outcome and the available project evidence. Produce drafts;
do not implement the work or create issues in a tracker.

## Establish the outcome and boundaries

Identify the problem, who benefits, why it matters, and what would count as
success. Preserve stated constraints, appetite, and exclusions. Inspect relevant
code and documents before choosing seams or dependencies; distinguish existing
capabilities from proposals and assumptions.

Challenge a proposed solution when it obscures the outcome or adds unnecessary
scope. Ask about missing intent only when the answer materially changes the
breakdown; otherwise mark it unknown. Never invent a business reason. When
project sources are unavailable, identify what the plan assumes and what needs
checking before implementation.

For a bundle, separate unrelated outcomes rather than forcing them into one
epic. A request already small enough may need just one task.

## Find the first useful increment

Prefer a **tracer bullet**: a thin, integrated path through the necessary parts
of the system that produces observable behavior and feedback on the approach.
Name what it proves. It can be a CLI invocation, data flow, migration, or API
interaction; a UI is not required.

Include the implementation and verification needed to complete that path in
the same work item. Splitting by database, backend, frontend, then tests leaves
integration feedback until the end. Preserve essential correctness and safety
constraints in the first usable slice; narrow supported scope instead of
deferring those constraints to a hardening ticket.

Use a separate prerequisite when a real constraint prevents an integrated
increment, and explain what it unlocks. For refactoring or infrastructure, use
an executable behavior, compatibility check, or operational result as evidence.
Split an item when it contains independent outcomes or substantial unresolved
uncertainty, not to hit an arbitrary duration, line count, or item count.

If uncertainty could change the architecture or invalidate the next slice,
shape a bounded spike first. Specify the question, evidence to collect, stopping
condition, and decision it unlocks. Unsupported and inconclusive are legitimate
results. A dependency on a spike does not make an assumed solution ready:
leave affected downstream work provisional and reshape it after the findings.
Detail the next actionable work; outline later work only as far as evidence
supports it.

## Classify and connect the work

Use existing project type names when supplied. Otherwise use these defaults:

| Type | Purpose |
| --- | --- |
| `task` | Deliver a bounded change, including features, refactoring, documentation, or maintenance. |
| `bug` | Correct behavior that violates an established expectation; include reproduction and regression evidence. |
| `spike` | Resolve uncertainty through bounded discovery and a decision artifact. |
| `epic` | Group tasks, bugs, or spikes toward a shared outcome with completion criteria. |

Give every item a stable local ID and a type. Record **Parent** separately from
**Depends on**. Membership groups work; a dependency means the prerequisite
must finish before this item can start. An epic completes when its agreed
outcome is met by its children; do not encode that roll-up as a start dependency
on its children. Create an epic only when a shared goal benefits from grouping.

List drafted prerequisites by local ID; identify external blockers with source
references or descriptive labels. Explain the
artifact, decision, or behavior each prerequisite supplies. Prefer direct edges
over redundant transitive edges unless a separate requirement needs explaining.
Keep IDs and relationships consistent when revising the breakdown.

Establish a valid delivery sequence before proposing parallel work. Identify
parallel opportunities only where prerequisites are met and shared interfaces
and integration responsibilities are clear. Different files alone do not prove
independence; shared files do not automatically require serial execution.

## Make each draft usable

Adapt the presentation to the destination, keeping these meanings explicit:

- **ID and title:** the bounded outcome.
- **Type, Parent, Depends on:** classification, membership, and blocking order;
  state none when absent.
- **Why:** the problem this item solves and its contribution to the larger goal.
  Carry the constraints or tradeoffs that help an agent reject overengineering;
  a link to a parent alone is insufficient context.
- **Scope and context:** relevant existing behavior and source pointers, what
  changes, and important exclusions. Leave implementation choices open where
  they do not affect the boundary.
- **Acceptance and evidence:** observable completion criteria, how to verify
  them, and what completion proves. Include negative or failure scenarios where
  they establish an essential requirement.
- **Readiness:** unresolved decisions and provisional status where applicable.
  For spikes, include the investigation boundary and decision artifact.

Epic drafts can summarize the shared why, outcome, children, and completion
evidence rather than duplicate child implementation details.

Finish with the delivery sequence, justified parallel opportunities, and the
points where findings require reshaping. Check that references resolve,
dependency and parent graphs have no cycles, essential requirements are owned,
and every ready item can be completed and verified without unspecified work
hidden in another item. Return the drafts and remaining questions or assumptions.
