---
name: code-simplification
description: Simplify working code while preserving behavior. Use when asked to simplify or clean up code, reduce nesting, or remove unnecessary complexity from a function, module, or recent change.
---

# Code Simplification

## Reduce Mental Load

Reduce the mental load of understanding and changing the code: the concepts a maintainer must track and the places they must look. Prefer clear control flow and names that express intent. Keep abstractions that hide meaningful complexity; remove indirection that only adds another place to look. Fewer lines alone do not establish an improvement. Leave already clear code alone.

Keep the pass within the requested scope; default to the recent change when no scope is given. Follow surrounding conventions so the result is easier to understand in its codebase.

## Chesterton’s Fence

Understand why the fence was built before removing it. Trace callers, tests, and history as needed to establish what a branch, wrapper, or abstraction protects. Remove it when that reason no longer applies; retain it when its purpose remains uncertain.

Preserve observable behavior, including errors, side effects, and evaluation order. A wrapper that looks redundant may turn a synchronous throw into a rejected promise. Check the contract before changing the expression, and keep bug fixes or intentional behavior changes separate from simplification.

## Simplify the Expression

Identify what makes the code hard to follow, then choose a change that removes that burden. Flatten nesting when it clarifies the main path, name conditions when their intent is hard to infer, and replace dense expressions with explicit steps when that makes evaluation easier to follow.

Extract a helper when its name and interface let the reader understand the caller without opening it. If understanding the caller still requires reading the helper, the extraction may only have moved the complexity. Consolidate duplication when the repeated code represents the same rule; keep independently changing rules separate even when they look alike.

## Verify the Improvement

Check the behavior each simplification could affect. Run relevant tests and inspect whether they cover the changed paths; add focused coverage or compare before-and-after behavior where evidence is missing. Passing tests do not establish equivalence for behavior they never exercise. Investigate failures rather than changing expectations to fit the rewrite. Discard changes when behavioral equivalence remains uncertain.

Read the result as a whole. Confirm that it reduces mental load rather than distributing the same complexity across more places. Discard changes whose benefit you cannot explain beyond fewer lines or a preferred style.

Report what became easier to understand, the checks performed, any bugs found, and any behavior that remains unverified.
