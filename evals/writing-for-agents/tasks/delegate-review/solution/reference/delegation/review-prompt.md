# Review the proration changes in src/billing

Review the new proration logic on this branch (diff against `main`) for money bugs:
rounding, truncation, and currency or unit mistakes. Find defects that would charge a
customer the wrong amount.

## Scope

- Review `src/billing/`. Treat `src/billing/tax.py` rounding as already checked; look at it
  only if something else depends on it.
- Skip `src/generated/` (protoc output, not ours).
- Ignore a failure in `tests/test_sync.py`; it is flaky on wall-clock timing and known. Other
  tests are trustworthy.
- Read-only: do not edit, create, or delete any file.

## Return

At most 10 findings, most severe first. Each has:

- `file:line`
- severity: `blocker`, `major`, or `minor`
- one line describing the failure

Then a short list of what you did not review.
