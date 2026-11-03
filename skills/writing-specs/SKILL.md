---
name: writing-specs
description: Write or revise specifications that make intended behavior, constraints, decisions, and success criteria clear to humans and agents.
---

# Writing Specs

## Establish Purpose and Scope

Establish what needs to change, who or what needs it, and why it matters. Describe the problem and intended outcome clearly enough that a reader can judge whether the proposed work addresses the need. When a request starts with a solution, recover its purpose from available context; ask when that purpose is unclear and would change the requirements.

Define which actors, situations, and capabilities the work covers, and where relevant behavior remains as it is. An actor is a person or system that participates in or is affected by the behavior being specified; use specific role names where known. State exclusions when a reader might reasonably expect them to be included. Keep adjacent improvements separate unless they are necessary to achieve the outcome or explicitly included in the requested scope.

Follow the requested format and destination; otherwise, use established project conventions. Choose depth and organization according to the questions a reviewer or implementer needs answered. A narrow change may need a few precise paragraphs; broader work may need separate treatment of related capabilities and their interactions.

## Ground the Spec in Evidence

Use relevant discussion, existing specifications, implementation, tests, and decision records to understand current behavior and constraints. Distinguish what the system does today from what it should do after the change. Existing behavior may itself be what needs correcting.

Make clear which statements are requirements, agreed decisions, proposals, or assumptions. When sources conflict, surface the disagreement. Use available context to resolve gaps before asking for clarification; ask when missing information could materially change scope, behavior, compatibility, or acceptance. Keep unresolved questions and their consequences visible so readers can tell what is settled and what still needs a decision.

## Describe Behavior Precisely

Describe the conditions that apply, what initiates the behavior, and the observable result. Make relevant rules explicit: who or what may act, which inputs are valid, how state changes, and what happens when an action cannot complete. Include ordering, timing, and interactions where they affect the outcome. Aim for enough precision that separate implementers would arrive at compatible behavior.

Use established domain terms consistently. Replace vague claims such as “handles errors gracefully” with what the actor learns, what state is preserved or changed, and whether recovery is possible. Use examples, tables, or diagrams to clarify rules and their boundaries. Distinguish illustrations from requirements so an example does not accidentally narrow or expand the contract.

Select alternate paths and edge cases by their consequences. Invalid input, unavailable dependencies, repeated or concurrent actions, and partial completion deserve attention where they expose a meaningful rule or decision. Avoid exhaustive variations with the same outcome, and record unresolved behavior as a question rather than inventing a policy.

## Make Constraints and Decisions Useful

State the constraints that limit acceptable solutions. Distinguish hard requirements from preferences and conventions that can be reconsidered. Explain the source or purpose of a constraint when it affects interpretation, and record consequential decisions with enough rationale to guide later judgment and reconsideration.

Specify technical commitments where correctness or compatibility depends on them, including interface contracts, data invariants, and migration constraints. Use a schema, type, or other concise notation when it expresses the commitment more clearly than prose; make clear which parts are binding. Prescribe an implementation approach when it reflects an agreed decision or necessary dependency, and explain why. Otherwise, leave room for approaches that satisfy the requirements.

## Make Success Verifiable

Make each binding requirement verifiable, connecting consequential requirements to explicit acceptance criteria describing observable results under stated conditions. Cover constraints and failure behavior that success on the main path would leave unproven. Acceptance criteria should make the requirements verifiable without introducing additional scope.

Give measurable targets the workload, environment, measurement method, and tolerance needed to interpret them. Replace “fast” or “reliable” with agreed conditions that can be evaluated. If a target is unknown, identify the decision or measurement needed rather than inventing a number. For qualities requiring judgment, describe what to assess and provide useful examples or reference points.

Describe how tests, inspection, measurements, or manual evaluation could demonstrate the required behavior at the relevant interface or system boundary. Prefer checks that remain valid across acceptable implementations. Specify tools or procedures when necessary for credible, reproducible results; leave detailed test construction and task sequencing to implementation planning.

## Make the Spec Usable on Its Own

Write for a reviewer or agent that has not followed the conversation. Include the context needed to interpret the requirements, and replace references such as “as discussed” with the actual decision. Keep authoritative requirements easy to find and maintain each in one place. Link to supporting contracts and decision records with enough local explanation that readers understand their relevance.

Remove repetition, incidental history, and detail that does not help readers decide or implement. Preserve qualifications, exceptions, and rationale that affect meaning. Organize the spec so related rules can be read together and dependencies are clear without reconstructing them from scattered passages.

## Check Coherence and Readiness

Read the spec as a whole. Check for conflicting rules, inconsistent terminology, missing interactions, unsupported commitments, and acceptance criteria that cannot establish the claimed outcome. Walk through representative scenarios against the requirements, including relevant failure paths. Confirm that examples, constraints, and verification criteria agree.

Identify which unresolved questions block implementation and which choices can remain open. For blocking questions, name the decision needed and who can resolve it when known. State readiness in terms of those gaps rather than how complete the document looks. When scope or decisions change, revise affected requirements, examples, and acceptance criteria together. Keep intended behavior distinguishable from what has been implemented or verified.
