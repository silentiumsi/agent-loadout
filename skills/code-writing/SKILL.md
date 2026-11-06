---
name: code-writing
description: Write and change code with clear data models, shared policies, validated boundaries, and readable logical paragraphs. Use when implementing features, fixing code, adding tests, or improving code readability and formatting.
---

# Code Writing

Make the requested behavior easy to understand and change. Inspect the existing
code and its callers before choosing a design. These are Loadout defaults;
explicit repository conventions and the task's constraints take precedence.

## Logical Paragraphs

Separate neighboring type/interface declarations, functions, and class methods
with one blank line. Keep related fields together, with a blank line before the
constructor or first method. Apply this to newly written code as well as edits;
a formatter passing does not establish these boundaries.

Group statements by immediate purpose. Within a function, separate distinct
steps with exactly one blank line, such as validation, preparation, execution,
and result handling. A change of purpose determines the boundary, even when
adjacent statements have the same syntax, such as independent conditional blocks.

Initialization and its immediate conditional assignment form one paragraph; an
operation and its immediate error check form one paragraph. Avoid both
uninterrupted walls of code and blank lines after every statement. Consecutive
variable declarations may belong together: keep inputs for one operation in a
group, then separate that preparation from execution and result handling.

```ts
const state = this.current;
if (!state) return;

const target = state.list;
const cursor = more ? target.data?.cursor : undefined;
const generation = target.generation;

const next = await this.api.list(state.key, cursor);
if (target.generation !== generation) return;

target.data = next;
```

Before finishing, inspect each edited module as a whole and correct its
declaration and class-member spacing, including boundaries beside unchanged
definitions. Check logical paragraphs in changed functions. Honor explicit
limits on formatting scope. For formatting-only work, preserve statements,
identifiers, literals, comments, and behavior.

## Reuse Existing Decisions

Before adding logic, search for the responsibility in the project, its direct
dependencies, and the standard library. Keep the search proportional to what you
would write, including small parsing, formatting, date, URL, and retry helpers.
Use existing functionality directly. Custom code needs a concrete requirement
that the existing implementation cannot meet.

Keep a shared policy in one place so changing it reaches every caller. Prefer a
concrete implementation until a second implementation or an existing boundary
requires an interface. Before passing a new value through several layers, look
for a shorter path. A wrapper earns its place by hiding a decision or complexity.

## Model the Data

Name the core data shape and trace where it is read and written before adding
branches. Encode mutually exclusive states in a status or discriminated union;
use distinct types for values that cannot be interchanged. Derive values rather
than keeping copies in sync. Choose a structure when it removes invalid states,
repeated branching, or duplicated rules; keep local, straightforward data plain.

## Validate at the Boundary

Parse external input into domain values where it enters: CLI arguments, config,
files, network responses, and environment variables. Handle invalid input there.
Inside that boundary, trust established invariants; add guards for legitimate
states rather than fallbacks that conceal broken assumptions.

Keep business logic in plain functions where practical. Let handlers and adapters
own parsing, I/O, and result formatting. Keep state in the smallest useful scope;
prefer returned values and locals over mutable fields or globals.

## Test the Contract

Assert what users can observe: results, errors, readable state, and external
effects. Derive expected values from the requirement. A useful test catches a
broken result or missing effect while surviving an internal refactor with the
same behavior. A payload sent to an external service is observable behavior;
calling an internal helper is an implementation detail.
