# Session notes (me and the user, so far)

- User wants a review of the new proration logic in src/billing/ before it ships.
  Compare against main; it's the diff on this branch.
- Skip src/generated/. It's protoc output and not ours to review.
- tests/test_sync.py is flaky (wall-clock timing). Known; ignore it if it fails.
  Everything else in tests/ is trustworthy.
- User cares most about money bugs: rounding, truncation, currency/units.
- The reviewer must not change any files. Read-only.
- I looked at tax.py already and the rounding there seems fine. Don't spend
  time on it.
- I suspect the int() truncation in prorate at invoice.py:6 loses cents, but
  the user wants an independent read, so don't hand that suspicion over.
- Output wanted back: a list of at most 10 findings. Each gets file:line,
  severity (blocker, major, minor), and a one-line description of the failure.
  Then a short list of what was NOT reviewed.
