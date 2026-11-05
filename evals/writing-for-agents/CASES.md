# Writing for agents cases

These cases test prose that directs an agent: whether it is correct, findable, and
usable by a reader with no other context. Requests are natural and do not name the
skill's rules. Each task reports separate dimensions, not one blended score:

- `contract`: required files exist and other files are untouched. A validity gate; it
  carries no claim about the skill.
- `fidelity`: facts the repository establishes, checked deterministically and by judge.
  Fluent guidance with wrong facts can score well on `writing` and fails `fidelity`.
- `writing`: anchored rubrics (and, where noted, deterministic craft checks) for
  usability by a cold reader.

The judge (Claude Opus 5.5) is a different model from both agents under test and sees a
blind staging copy with no condition names.

## Scope of the suite

Every case and criterion here is one a no-skill baseline fell short of repeatedly in
2026-11-05 trials (Codex gpt-6.1-terra and Claude Code sonnet-5-5, three attempts each):
at least one agent missed full marks in at least two of its three trials. Criteria that
baselines already pass guard against regression but cannot show uplift, so they are not
here. After a skill changes behavior, rerun the baseline before adding any back; at three
attempts a single miss is noise. Rubric headroom is reachable: each task's oracle output
scores full marks.

Every case is a development case. No held-out split exists yet.

## Authority conflict

[Task](tasks/authority-conflict)

**Origin: observed failure, 2026-11-05.** Codex copied two claims from a maintainer's
notes that the repository contradicts: a 32-character service-name limit (the tool
enforces 40) and "CI blocks merges without tests" (CI only lints). Claude Code found the
tool's limit but was inconsistent in labeling which authority each rule came from.

The agent turns raw notes into AGENTS.md. Each rule belongs to one authority: tool
behavior (name limit, regions), a team decision (deploy window, ADR-12), a team
convention nothing enforces (tests before merge), a team preference (Python 3.12
against a 3.11 minimum), or an adaptable default (commit style). The request does not
tell the agent to verify the notes.

Checks: the 40-character limit (a hedged mention of the notes' 32 passes; asserting it
as the limit fails), CI not claimed to enforce tests, a judge on whether each rule names
the right kind of authority, and a usability rubric. They cannot establish that an
authority is stated where an agent needs it beyond the judge's reading.

## Author skill body

[Task](tasks/author-skill-body)

**Origin: observed failure, 2026-11-05.** Given a maintainer's request that includes
generic exhortations ("be accurate, double-check your work, professional tone"), baseline
agents carried them into the skill, and descriptions and completion conditions were
weaker than the repository-specific rules.

The agent writes `skills/release-notes/SKILL.md`. Neighbor skill frontmatter and the
request show the repository's conventions (including user-invoked only).

Checks: no generic filler (deterministic), a rubric for behavior-changing content only,
and a rubric for description triggers and observable completion. Frontmatter, facts, and
helper handling passed at baseline and are not scored. The rubrics grade the skill as
written; they do not show that a downstream agent follows it.

## Delegate review

[Task](tasks/delegate-review)

**Origin: observed failure, 2026-11-05.** Claude Code's prompts were complete but carried
preamble, a generic exhortation, and a scripted route (start by diffing, then read around)
where the requirement and scope should lead. Codex's did not.

The agent writes the prompt for a subagent that starts with none of the session's
context, from rich session notes (scope, exclusions, a known flaky test, read-only rule,
return format, and a suspicion the user wants withheld so the review stays independent).

Check: a rubric grading the prompt as text: goal first, route left to the reviewer, no
padding. It does not show that a real subagent would behave well. Slots and the
withheld suspicion passed at baseline and are not scored.

## Handoff note

[Task](tasks/handoff-note)

**Origin: observed failure, 2026-11-05.** Both agents verified the repository and kept
the log's facts, but handoffs buried the first action or scattered binding constraints,
and showed the check commands only in passing.

The agent writes `HANDOFF.md` for a cold reader from a messy log whose claims the
repository contradicts (module c is pending, not migrated; b has an open problem the log
missed; the port changed; a decision and a skipped step carry reasons and dates).

Check: a cold-usability rubric: state, first action, binding constraints, progress-check
command, uncertainty beside its claim. Accuracy passed at baseline and is not scored,
so a skill that regresses accuracy would not be caught here.

## Slash command

[Task](tasks/slash-command)

**Origin: observed failure, 2026-11-05.** Codex's command correctly specified the output
format, but gave no example of it; a rubric for recipe-over-prohibition scored
Codex's commands below full marks in every trial (Claude Code's in one of three).

The agent writes `commands/triage.md`; its entire output feeds a strict parser
(`tools/ingest.py`) that exits 0 even when it rejects lines, so the format lives only in
the tool's docstring.

Checks: the command's own example lines are accepted by the real parser (deterministic;
placeholder template lines are ignored), and a craft rubric. Whether the format was
correct passed at baseline and is not scored. The example check measures a craft
preference (show the output), not whether the command works.
