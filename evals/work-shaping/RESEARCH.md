# Research informing work shaping

Sources checked 2026-11-06. These are inputs to the design, not proof of skill uplift.

| Source | Relevant practice | Application and limit |
| --- | --- | --- |
| [Shape Up: Set Boundaries](https://basecamp.com/shapeup/1.2-chapter-03) | Choose an appetite and constrain the solution. | Use the user's reason and constraints to bound work; do not import six-week cycles or fixed team sizes. |
| [Shape Up: Get One Piece Done](https://basecamp.com/shapeup/3.2-chapter-11) | Integrate one usable vertical slice early. | Sequence a tracer bullet before expansions; backend, UI and verification are usually parts of the same outcome. |
| [Jeff Patton: Story Mapping](https://www.jpattonassociates.com/wp-content/uploads/2015/03/story_mapping.pdf) | Retain the whole user journey while slicing for named outcomes. | Preserve the larger goal in epics and item rationales; a release slice can contain multiple work items. |
| [The Pragmatic Programmer: tips 20–21](https://pragprog.com/tips/) | Tracer bullets give feedback on direction; prototypes produce learning. | Distinguish an integrated implementation path from a discovery experiment. Neither implies a particular UI stack. |
| [Anthropic: Effective harnesses for long-running agents](https://www.anthropic.com/research/effective-harnesses-for-long-running-agents) (2025-11-26) | Incremental features, explicit verification and persistent handoff artifacts address overlarge attempts and premature completion. | An item must give a fresh agent sufficient context and observable evidence. This is one reported harness, not a universal task-size rule. |
| [Anthropic: Harness design for long-running application development](https://www.anthropic.com/research/harness-design-long-running-apps) (2026-03-24) | Tractable chunks, context handoffs and explicit evaluator criteria. | Define what a chunk proves. Do not require a specific multi-agent architecture or turn the skill into an execution harness. |
| [Cursor: Scaling long-running autonomous coding](https://cursor.com/blog/scaling-agents) (2026-01-14) | Coordination failures included safe-change churn without end-to-end ownership; planning remains iterative. | Preserve outcome ownership and revisit downstream work after discoveries. Large experimental code volume does not establish production quality or general best practice. |
| [GitHub issue types](https://docs.github.com/en/issues/tracking-your-work-with-issues/using-issues/managing-issue-types-in-an-organization), [Jira work types](https://support.atlassian.com/jira-cloud-administration/docs/what-are-issue-types/), [GitLab tasks](https://docs.gitlab.com/user/tasks/) | Platforms differ in type vocabulary and hierarchy. | Use neutral work items with Type, Parent and Depends on. Adapt existing vocabulary; publishing and native tracker mapping are outside this skill. |

## Design decisions confirmed by the user

The skill shapes discovery, mixed changes and large changes for agent execution.
Sequence matters before parallelism. Prefer a thin end-to-end path with observable
behavior, with explicit exceptions for real prerequisites. Detail actionable work;
leave work gated by unresolved discovery provisional. Inspect available project
sources and identify assumptions when evidence is absent.

Default types are task, bug, spike and epic. Each item has a stable local ID,
explicit blocking dependencies and separate parent membership. Epics group a
shared outcome and are optional. Preserve the reason for each item so an agent
can judge unnecessary complexity. Ask about a missing reason only if it changes
scope; otherwise mark it unknown. Never invent intent.

## Hypotheses to evaluate

Outcome-based slices, decision-gated discovery and grounded rationale should improve
agent handoffs over a generic task list. This is an inference from the sources and
user preferences. Paired trials are needed to measure any skill contribution.
