---
name: ground
description: Work out what to build before building it, ending in one specification an agent can build from without further decisions. Use when the user invokes ground, wants to plan an initiative or project up front, doesn't yet know the depth of what they're building, or wants unknowns surfaced before implementation starts.
---

# Ground

The goal is a **spec** that a junior engineer or an agent could build from and deliver exactly what was agreed, with no unknowns, scope creep, or surprises, plus a **slice file** that breaks the spec into buildable pieces. The user often doesn't yet know the depth of what they're building. Bring the unknowns out and let them decide; a decision enters the spec only after the user confirms it.

**Done** means every slice is `ready` and coverage holds in both directions: every spec part is built by at least one slice, and no slice builds something the spec doesn't describe. Report that and stop. Do not create tickets, proposals, or code, and do not run a build loop. Otherwise stop when the user does.

## Files

Two files in one folder in the repo, `ground/` unless the user names another place.

- `spec.md`: one coherent document organized by what is being built. Start with **Foundations** (stack, cross-cutting decisions, shared contracts, glossary), then the system's parts, then **Unknowns**.
- `slices.md`: a fenced YAML list of slices, then a Mermaid diagram of them that you regenerate each round and never hand-edit. Each slice has `id`, `title`, `depends_on`, `status`, a one-line summary, the spec parts it builds, and the decision ids it cites.

Each part of the spec states: goal; in scope and out of scope; decisions, each with an id, its reason, and the evidence for it; what it takes from and gives to other parts; how it is built; design references; acceptance criteria that can be tested. Parts refer to Foundations and don't repeat them.

State lives in these files. On every run, read them to find where you are. A first run starts from the user's one-sentence intent, and the files are first created at the end of the first round, after the user has seen what goes in them.

Statuses: a slice or spec part starts `draft`; a slice becomes `ready` by passing the readiness test; a `ready` slice becomes `stale` when something it cites changes. Spec parts stay `draft` until every slice that builds them is `ready`.

## Existing work

Before the first interview, read what already exists: the code, repo docs, existing specs, and any earlier planning notes. If the repo refers to planning material it doesn't contain, ask the user once where it lives. Treat all of it as evidence, not as confirmed decisions: put a decision in the spec only after the user confirms it. List built parts under Foundations as existing context; they get no slices.

## Each round

Interview with the `grilling` skill: ask everything you can ask now, each with a recommendation, then wait for answers. Ask about the project, never about how this skill works. Work on the first of these that applies:

1. A risky unknown with no evidence.
2. A slice or spec part still in `draft`.
3. A slice that is `stale`.

Stack and feasibility questions always come before designs. After the interview, update the files and run the readiness test on every `draft` or `stale` slice whose parts have no open unknowns.

**Unknowns.** Propose a first list of areas to probe for this project, from the intent. The user strikes and adds. Keep extending it whenever you find something new to decide. Each item is `open` or `resolved`, and a resolved item links to its evidence.

**Risk.** Flag an unknown as risky if it is new to the user or you, depends on an unproven external system or library, is expensive to undo, or has other parts depending on it. Say why; the user can overrule. Depth follows risk: go deep there, skim the rest.

**Evidence.** A risky decision counts as made only with evidence, such as a spike result. Propose the spike and wait for a yes, naming the exact question and what result would change the decision. Run it in a throwaway directory outside the repo. Record the question, result, and conclusion under the decision it supports. If the user declines a spike, record the decision as an accepted risk, labeled so.

**Designs.** Each mockup or diagram records how it is built and which decision ids it relies on.

**Slices.** A slice is the largest unit one agent session can build and verify, with its own testable acceptance criteria; split anything bigger. Build and revise the slice file as you learn.

**Staleness.** When a decision changes, mark `stale` each slice that cites it and everything downstream.

## Readiness test

Give a fresh-context subagent only the spec parts the slice points to, Foundations, and the decisions cited, never the conversation. Ask it to list every question it would need answered and every assumption it would have to make, limited to those whose answer would change what gets built. The slice becomes `ready` only when both lists are empty. Put anything it lists into the spec as an open item and take it to the user.

## Closing a round

Before saving, show the user what changed in the spec, the slices, and the unknowns, and which slices went stale. Save after they've seen it.
