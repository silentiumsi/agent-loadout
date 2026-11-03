---
name: debugging-and-error-recovery
description: Trace failures to their root causes and fix them at the source or an appropriate ownership boundary. Use when tests fail, builds break, runtime behavior is wrong, a regression appears, or an unexpected error interrupts work. Stop the line before building on a failure.
---

# Debugging and Error Recovery

## 1. Stop the line

When an unexpected failure appears, pause work that depends on the failing behavior and investigate before building on it. Do not carry a broken assumption into the next feature or layer.

Preserve the evidence before retries, restarts, cleanup, or edits change it: the exact error, triggering input or steps, expected versus actual behavior, and relevant environment or state. Capture enough to compare the original failure with later experiments.

Establish whether the failure came from the current change, already existed, or remains unattributed. Use a focused check against a known-good baseline where available; preserve user changes while comparing. An existing failure still needs diagnosis if the current work depends on it.

Keep failing checks and errors visible. Skipping a test, weakening an assertion, suppressing an exception, or adding a fallback to keep moving leaves the cause unresolved. Continue independent work only when it does not rely on the broken behavior or disturb the evidence needed to investigate it.

## 2. Trace to the source

Find the smallest reproduction that preserves the failure. For intermittent failures, compare failing and successful runs for differences in timing, environment, and state; instrument gaps in the evidence.

Trace the failing value or operation upstream from the error location. Compare expected and actual behavior at each boundary until you find the first broken contract, then investigate why it broke. Check that contract against requirements, callers, and tests: the receiver may be mishandling valid input.

For example:

```text
Receipt shows a total 100 times too large
  ← formatter treats the amount as dollars
  ← caller passes cents
  ← required unit conversion is missing
```

Record which causal links the evidence supports and which remain unproven before choosing a fix location.

Identify ownership boundaries and whether an upstream correction is available when the cause lies in another team's code or an external service.

## 3. Prove the cause

State a hypothesis that explains the causal chain from the suspected defect to the observed failure. Predict what you would observe if it were true and choose a focused experiment that could disprove it or distinguish it from competing explanations.

Change one relevant factor at a time. Compare the result with the prediction before making another change. A disappearing error alone does not prove the cause: a guard, retry, or fallback may bypass the failing path while leaving the defect intact.

Discard experimental changes that the evidence does not support; preserve observations that narrow the search. If experiments repeatedly contradict the hypothesis, revisit the trace and gather evidence at the unresolved boundary instead of stacking speculative patches.

Proceed when the evidence explains both why the failure occurs and how the proposed correction addresses it. If access or reproducibility limits prevent confirmation, state what remains uncertain and what observation would resolve it; keep any proposed repair provisional.

## 4. Fix at the source or boundary

Choose the repair location from the proven causal chain and ownership boundaries. Correct the mechanism that introduces the failure where feasible, even when patching the nearest consumer would be easier. Keep the change focused on restoring the intended contract; avoid distributing compensating logic across callers.

When an upstream correction is unavailable, restore the contract in the integration layer responsible for that boundary. Make the handling specific to the known upstream behavior so valid inputs and other consumers retain their intended behavior. Preserve visibility into unexpected failures.

Judge guards, retries, and fallbacks by what they accomplish. They are a fix when they implement the required boundary behavior and address the diagnosed failure; they are containment when they only reduce its impact. For containment, state the remaining defect, the limits of the mitigation, and the upstream correction still needed.

## 5. Verify and resume

Rerun the original reproduction and check the expected outcome, including any side effects. Confirm that the correction repairs the failing path rather than bypassing it. For intermittent failures, exercise the conditions that exposed them; a single passing retry is insufficient evidence.

Add a regression guard where practical that fails without the correction and passes with it. For a boundary fix, cover the diagnosed upstream behavior and valid inputs that must remain unchanged.

Check whether the same cause affects other paths or consumers, and run the affected tests and required repository checks. Investigate new failures before resuming work that depends on them.

Resume dependent work when the evidence shows the behavior it needs is correct. Report the diagnosed cause, repair location, and verification results. Mark checks that could not run as unverified, and distinguish a verified local boundary fix from an upstream defect that remains unresolved. If only containment is in place, state which dependent work is safe to resume and which remains blocked.
