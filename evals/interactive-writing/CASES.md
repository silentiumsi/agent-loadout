# Interactive writing cases

These cases test editorial control and delivery across real conversational
turns. Each step resumes the same agent session and checks the artifact before
the next editor message. Editor messages are fixed; prompts do not repeat the
skill's workflow rules.

The initial request names the installed skill file because the skill requires
explicit invocation. Baseline jobs use the same request with that file absent.

## Approval and advancement

[Task](tasks/approval-and-advancement)

**Origin: behavior clarification, 2026-11-04.** Earlier sessions followed the old
rule that acceptance alone did not authorize advancing. During evaluation
design, the editor changed that expectation: approval should authorize the
next increment without another permission question. Approval depends on
meaning, not a required keyword.

The agent should propose an approach without drafting, write the first agreed
section, then advance one section after each approving reply. Different
approval phrases exercise that distinction. Later sections must stay undrafted.

The approach check verifies only that the file stays unchanged. It cannot
establish that the agent proposed a useful approach or avoided drafting in chat;
inspect the transcript for those behaviors.

## Revision and delivery

[Task](tasks/revision-and-delivery)

**Origin: observed failure and expected scope boundaries.** In a 2026-11-02
writing session, an agent reported adding a principle, but the editor could not
find it. The agent had renumbered the list without inserting the paragraph.
This case checks the file itself after each requested edit.

A precise version correction should appear directly in the current section.
Further corrective feedback should revise it without drafting the next section.
Approval should then advance. Accepted text outside the authorized scope must
remain unchanged.

Preservation checks protect seeded accepted text, not a snapshot of every
newly accepted section. Rewrites of newly accepted prose can pass if its
required facts survive.

## Meaning across edits

[Task](tasks/meaning-across-edits)

**Origin: observed loss of intent and behavior clarification.** In a 2026-11-02
writing session, revising a principle's wording weakened its purpose; the editor
had to explain the intended mechanism again. During evaluation design on
2026-11-04, the editor clarified that human prose may be improved: preserve its
purpose and meaning, not exact wording.

Between turns, setup edits the current section as a human would. The agent
should reread it and tidy its prose while retaining the added timing, contact,
and vendor-contact restriction. Document-wide UTC guidance should carry into
the next section after approval.

The checks cover those concrete facts and section boundaries. They allow
paraphrasing but do not establish general semantic equivalence or prose quality.
