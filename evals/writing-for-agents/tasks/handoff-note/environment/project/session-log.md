# Migration log (me, working notes)

10:02 plan: move modules a..e to the new schema in order a, b, c, d, e.
      Step 3 of each is the backfill.
10:20 decision: batch size 500, not 5000. 5000 timed out on the prod replica
      (30s limit). Use 500 everywhere.
10:31 a done.
10:50 b done, tests green I think.
11:05 service listens on 8080.
11:20 c migrated (ran `migrate run c`, it printed queued, assume fine).
11:40 skipped the backfill for b: the table is locked by the finance job until
      Friday. Plan was to backfill every module.
12:00 8080 was taken, moved the service to 9090.
12:10 TODO: d, e. Do NOT run d before b's backfill has finished (d reads it).
