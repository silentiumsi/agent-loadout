---
name: documentation
description: Write, revise, and maintain technical documentation. Use for READMEs, guides, API documentation, inline explanations, and architecture decision records (ADRs), including cutting or rewriting existing documentation and updating it after behavior changes.
---

# Documentation

## Start with the Reader

Identify who will use the documentation, what they need to understand, decide, or do, and what they already know. Use that purpose to choose what belongs and the order in which the reader needs it. Ask about missing context only when it would change the content.

Read the existing documentation and repository guidance before choosing a home or structure. Extend the relevant document and follow established conventions. Create a separate document when it serves a distinct reader need; keep the README focused on orientation and getting started, linking to detail where needed.

## Establish the Facts

Check claims against the implementation, tests, configuration, and available decision records. Treat existing prose as something to verify when it conflicts with those sources. Use actual commands, paths, defaults, and examples from the project; identify prerequisites and conditions that affect whether they work.

Distinguish current behavior from proposals and historical decisions. Describe observed behavior without inventing intent; use recorded discussion or the decision-maker's account to explain why a choice was made. Surface conflicting or missing evidence rather than turning an assumption into a confident claim. Keep uncertainty visible until it can be resolved.

## Cut and Rewrite

Cut sections before tightening sentences. Remove material that does not help the reader's task, repeated summaries, and explanations already better maintained elsewhere. Reorder what remains so the reader encounters prerequisites before actions and detail when it becomes useful. Judge the result by how easily readers can find and use the information, rather than by word count.

Understand what a warning, caveat, or repeated instruction protects before removing it. Check its context and history when the purpose is unclear. Preserve necessary context where the reader acts, even when the full explanation lives elsewhere.

Rewrite vague claims and stock introductions into concrete information. Prefer direct verbs and the project's established terms. Use an example, table, or diagram when it can replace a longer explanation; keep prose for conditions the example cannot convey.

Compare the rewrite with the original and its sources. Preserve names, values, units, commands, paths, conditions, trade-offs, and uncertainty unless the evidence supports changing them. Restore lost qualifications and correct unsupported claims; smoother prose must not imply a stronger guarantee.

## Record Decisions

Record a decision when its rationale would otherwise be lost and future readers may need to revisit it: a consequential trade-off, a constraint that explains an unusual design, or a choice that is costly to reverse. Put local reasoning beside the code it explains; use an ADR when the decision spans the system or needs a durable record of its own.

Follow the project's existing ADR location, naming, format, and status conventions. When no naming convention exists, use sequential, zero-padded numbers and descriptive slugs, such as `0001-use-postgresql-for-storage.md`. Default to [Michael Nygard's ADR template](https://github.com/architecture-decision-record/architecture-decision-record/tree/main/locales/en-us/templates/decision-record-template-by-michael-nygard), consulting the source when needed.

Treat ADRs as append-only records: add information without removing or rewriting existing content. When a decision changes, create a new ADR. Add a superseded notice linking to the new ADR in the original, and state which ADR the new record supersedes, linking back to it. Update the documentation that describes current behavior to reflect the decision now in force.

## Keep Documentation in Sync

When behavior changes, find the documentation that describes it and update affected instructions, examples, and references as part of the change. Follow links and search for old names, commands, and assumptions to find related passages. Remove obsolete guidance from current documentation; preserve historical ADRs under the append-only rule above.

Keep one authoritative explanation for information used in several places, and link to it from the others. Retain enough local context for readers to act without unnecessary navigation. When documentation is generated from code or schemas, update the source and regenerate it through the project's workflow.

## Verify the Result

Walk through the finished document from the reader's starting point. Check that prerequisites are available before they are needed, steps produce the described result, and links and references lead to the intended material. Exercise changed commands and examples where practical; use the project's documentation checks when available. Distinguish examples verified by execution from those checked only against source.

Read the document as a whole for gaps, contradictions, and repetition introduced by the edits. Confirm that cuts preserved the conditions and caveats needed to use it correctly. Report unresolved factual questions and checks that could not run, including what prevented them.
