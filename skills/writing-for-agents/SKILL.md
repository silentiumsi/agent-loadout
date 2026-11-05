---
name: writing-for-agents
description: Write or rewrite instructions an agent will read. Use for AGENTS.md or CLAUDE.md, rule files, system or task prompts, slash commands, delegating to a subagent, handoff notes for a later session, and the body of a skill. Not for READMEs or other prose for humans.
---

# Writing for Agents

The reader is an agent that starts with none of your context and follows what it finds.

Read when the task matches:

- Handing work to a subagent, or leaving work for a later session: [references/delegation-and-handoff.md](references/delegation-and-handoff.md).
- Steps you have decided to prescribe: ordering, completion, failure handling, helper commands, user gates, or search instructions: [references/workflow-mechanics.md](references/workflow-mechanics.md).
- A skill's folder, frontmatter, or description wording: `creating-skills`.

## Verify before you write

Source material (notes, a request, an old file) is a claim, not a fact. Check each rule, limit, command, and path against the repository: the tool's code, config, CI, `--help`. When notes and repository disagree, write what the repository does and say where the notes differ. Mark anything you cannot check as unverified.

## Name each rule's authority

Label where a rule comes from, so the reader knows what it may bend:

| Authority | Write it as |
| --- | --- |
| Tool or platform behavior | A fact, with the file, command, or limit that enforces it |
| Team decision | The decision, who made it, and when or the record (ADR, ticket) |
| Convention nothing enforces | "By convention", and that no check catches a miss |
| Preference | "Prefer X", never "must" |
| Default | A default, and the observable condition under which to deviate |


## Lead with what the reader needs first

Put the goal, the first action, and the constraints that bind it at the top, in that order. A constraint a reader meets after acting on the wrong assumption does not constrain. Keep a rule beside the step it governs and state it once, in one place. Link to detail the reader only sometimes needs, and say when to follow the link.

A **context pointer** is the text that decides whether the reader opens a file or skill: a description, a line naming a file. If must-have material is missed, sharpen the pointer before inlining the material: start with the words a request would use, and list each distinct case that should open it.

## Give the goal, not the route

State the goal and its constraints; leave the route to the agent. Prescribe a step only where order or exactness matters: a destructive action, a handoff, a format another tool parses. Each added step narrows what the agent may do, so add one for a failure you have seen.

Match the form to the failure:

- **Wrong-shaped output:** show an example of the right shape. When another tool parses the output, the example is the specification; check it by running it through that tool.
- **Omissions:** a template with a slot for each item.
- **Tempting mistake:** name it with its replacement ("use X, not Y"). A bare "don't" invites negotiation.
- **Conditional behavior:** key it to something observable ("if `docs/adr/` exists..."), with the exception as its own condition.

## Cut what adds nothing

When writing or editing, delete a line when you cannot say what the agent would do wrong without it. That covers "be accurate", "double-check your work", "use a professional tone", openers that restate the task, and anything the environment already says (a `package.json` script, a `--help` text). Write what the agent cannot find by looking: the unwritten convention, the reason behind a choice, the trap no config reveals. Cut sections before shortening sentences.

When several instructions repeat one idea, replace them with one familiar term ("tracer bullet" for a thin end-to-end slice that proves the path), define it at first use, and reuse it unchanged.

## Specific files

- **AGENTS.md, CLAUDE.md, rule files:** loaded every session, so each line costs attention every time. Rewriting means deleting stale and discoverable content first, then checking what remains against the repository.
- **Slash commands:** state the arguments the command takes and the one outcome it produces, with an example of any output a tool parses.
