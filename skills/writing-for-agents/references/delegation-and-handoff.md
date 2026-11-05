# Delegation and handoff

Write for a reader who acts on the first screen and may never reach the second.

## Delegating to a subagent

Open with the goal and the question it must answer. Then the scope (what to look at, what to leave alone), the constraints it must obey (read-only, no edits, files off limits), and the shape of what it returns. Add what you know that it cannot find: a flaky test, a known false positive, an exclusion and its reason.

- State the requirement, not a route ("start by diffing, then read the callers"), and skip the preamble and exhortations.
- Spell out the return format as slots (findings with file and line, severity, what you could not check), so the answer is usable without a follow-up.
- To keep a review independent, omit your own suspicion. Give the scope and the standard, not the conclusion you expect.
- Pass paths and requirements, not "as discussed".

## Handing off work

A handoff note lives in one durable file, written for a reader who has only the repository and this note. Order it:

1. **State:** what is done, what is pending, and what is in doubt, judged against the repository, not the session log or earlier notes. Run the status check and report what it says; where the notes disagree, the repository wins, and if no check exists, mark the state unverified.
2. **First action:** the single next step, with the exact command and the directory it runs from.
3. **Binding constraints:** decisions that must hold, each with its reason and date; steps deliberately skipped, with why. Put each beside the step it affects.
4. **Progress check:** the command that shows whether the work advanced, and what its output looks like when it is right. For a check that exits 0 with problems, see Helper commands in [workflow-mechanics](workflow-mechanics.md).
5. **Open problems:** each unverified claim or known issue next to the thing it concerns, marked as unverified. Do not move doubt to a closing list.

Pin exact files, interfaces, and expected results; leave inferable implementation choices to the reader.
