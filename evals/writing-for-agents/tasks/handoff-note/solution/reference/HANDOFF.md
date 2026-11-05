# Migration handoff

Migrating modules a..e to the new schema. Run commands from the project root.

## State (checked against the repo, not the log)

`python tools/migrate.py status`: **a and b are done; c, d, e are pending.**

- The log says c was migrated. It only printed `queued` and status still shows c pending; treat c as not done.
- The log says b's tests were green, unverified. `python tools/check.py` exits 0 but reports a problem: **module b: missing index on orders.customer_id.** Fix it before relying on b. (Read the `problems` list; exit 0 does not mean pass.)

## Next

1. Fix the b index problem and re-run the check.
2. Migrate c (`python tools/migrate.py run c`), then confirm with `status`.
3. Backfill for b was **skipped**: the table is locked by the finance job until Friday. Do it after Friday.
4. **Do not run d until b's backfill has finished**; d reads it. e can follow d.

## Settings that bind

- Batch size is 500 for every module. 5000 timed out on the prod replica (30s limit).
- The service now listens on 9090. 8080 was taken.
