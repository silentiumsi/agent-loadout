---
name: interactive-writing
description: Create or revise written artifacts with the human as editor, building through agreed increments and feedback. Use only when explicitly invoked. Supports documentation, READMEs, agent skills, essays, proposals, emails, and other written artifacts.
disable-model-invocation: true
---

# Interactive Writing

## Agree on the approach and increment

Act as the writer, with the human as editor. Develop ideas and prose from the agreed brief; put substantive assumptions to the editor for judgment.

Establish the artifact, its purpose, audience, and destination from the available context. Ask only for missing information that changes what you should write.

Propose an approach and the first **increment**: the bounded amount of writing to produce before returning control to the editor. Choose the smallest useful starting point: an outline to explore breadth, a paragraph to establish voice, or a section to develop one part. Get agreement before drafting. A precise editing request already establishes its scope and direction; carry it out directly.

Size each **increment** to the work. Whole-document drafting requires explicit agreement, even for short artifacts. Either person can propose changing the approach or **increment** size as the work develops; agree on the change before using it.

## Write, review, and advance

Write only the agreed **increment** directly into the artifact. Return a link and a brief review prompt, without repeating the prose in the conversation. If direct editing is unavailable, present the **increment** in the conversation for review.

Stop after delivering each **increment** and wait for the editor. Approval accepts the current work and authorizes the next **increment** under the agreed approach; proceed without another permission question. Interpret approval by meaning, not a required phrase. Apply corrective feedback to the current **increment**, then stop again; revision alone does not authorize advancing.

If the next step falls outside the agreed approach or its scope is unclear, propose it and wait for agreement before writing.

## Preserve editorial control

Treat the file as the source of truth. Before each **increment** or revision, reread the relevant text and enough surrounding context to preserve continuity. Preserve the purpose and meaning of the editor’s direct changes, improving their prose within the authorized revision scope. Ask when the intended meaning is unclear.

Keep revisions within the requested scope. If new writing reveals a problem in previously accepted text, identify the passage and propose a targeted change. Wait for agreement before changing it, unless the editor has already requested that revision. Make the resulting change visible through a brief summary or diff.

## Learn preferences and resume work

Apply explicit editorial guidance at its stated scope. Treat a local correction as local: removing one example does not establish a preference against examples. When repeated edits suggest a broader preference, describe the pattern and ask the editor to confirm it before applying it elsewhere. Carry preferences across documents only when the editor explicitly requests or accepts that broader scope.

For longer projects, keep brief editorial notes outside the finished artifact, using an established project location when available. Record confirmed preferences and their scope, the agreed approach and **increment** size, accepted and pending work, and the stopping point. Keep these notes current without copying the draft or conversation into them. Short tasks can rely on the conversation.

When resuming, read the notes and current artifact before writing. Distinguish accepted text from work awaiting review; a saved next step does not itself authorize advancing.

## Review the completed artifact

When the agreed scope is filled, propose a **blind review** and wait for agreement. Use a subagent in a fresh context with no inherited conversation. Give it the completed artifact and ask it to assess clarity, coherence, gaps, contradictions, repetition, inconsistent terminology or voice, and transitions. Withhold the drafting discussion, editorial notes, design rationale, and your own assessment so the reviewer judges what the artifact communicates on its own. Ask for located findings and targeted suggestions, without direct edits.

Present the **blind review** findings for the editor to decide on, noting any conflicts with confirmed editorial choices. Apply agreed revisions through the same **increment** and review loop. Finish when the editor accepts the artifact; distinguish completed drafting from pending review or unresolved decisions.
