# Workflow mechanics

Apply a rule only where the task shows the failure it prevents.

## Completion criteria

End each step on a condition the agent can observe, so it can tell done from not done. A vague bound ("understanding reached") invites ending early to reach the steps ahead. Make it demanding where a miss is costly: "every modified module accounted for" drives legwork that "produce a change list" does not.

The final criterion names evidence the agent inspects: the artifact, not a report about it. A passing structural check (the file parses, links resolve) does not show the output works.

## Decisions and failures

Where a consequential step can branch or fail in a way judgment cannot settle, write the transition: which observable result picks the next move (retry, fix, ask, stop). Leave ordinary retries to the agent.

A retry limit stops the work but does not explain the failure. Pair it with what to report when it trips: attempts made, the last error, the current hypothesis.

## User gates

Wait on the user only when the agent cannot find or infer the answer, or the next action is costly or hard to undo. Otherwise it states its assumptions and proceeds. A gate whose answer is usually "yes" does nothing.

## Helper commands

For each command the instructions invoke, give the command, the directory it runs from, and how it signals failure. Say which checks it enforces and which the agent still performs. When a helper prints problems but exits 0, say so and tell the agent to read the output. If `--help` covers the rest, point to it.

## Search work

When a known positive exists, confirm the search finds it before widening. Inspect near-misses. Report the patterns tried, your confidence, and what was not searched; zero matches does not prove absence.
