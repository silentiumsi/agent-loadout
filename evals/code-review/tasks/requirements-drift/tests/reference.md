# Private grading context

The change adds a refund-window check. The code and its tests are internally consistent and pass, and nothing in the diff or history mentions the policy. `docs/adr-007-refunds.md` is an accepted decision that refunds are accepted for 30 days; the change enforces 14 days (`REFUND_WINDOW`). Refunds between day 15 and day 30 are wrongly rejected. This is a substantiated blocker (money movement, conflicts with the stated requirement). A review that never looks for requirements outside the diff will approve.

Expected: the report cites ADR-007, states the 14 vs 30 day mismatch, classifies it as a blocker, and does not approve.
