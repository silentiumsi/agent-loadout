# Handoff

Migration of modules a..e. a, b and c are migrated; b's tests are green. Remaining: d and e.
Batch size is 500. The service listens on 8080 (moved to 9090 at some point).
The backfill for b was skipped because of the finance job. Don't run d before it finishes.
