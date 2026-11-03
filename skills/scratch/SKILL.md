---
name: scratch
description: >-
  Place disposable task files: probes, intermediate renders, logs, temporary
  diffs, payloads and throwaway clones. Use when no path is named.
  Not for durable output.
---

# Scratch

Use named paths as given; never clean them up. Otherwise use `.scratch/` under
`git rev-parse --show-toplevel`, or `pwd -P` outside Git. Keep files directly
inside; multi-file outputs get one child directory.

Create the root if needed. In Git, ensure `git rev-parse --git-path info/exclude`
contains a `.scratch/` line; append it on a new line if absent. Never edit
`.gitignore` or global ignores. If `git ls-files .scratch` lists tracked files,
leave them untouched and report them.

Reserve a descriptive kebab-case path atomically: exclusive creation for files,
`mkdir` without `-p` for directories. Retry collisions with another name.
In Git, verify with `git check-ignore -q -- <path>` (trailing slash for directories).
If verification fails or cannot run, remove the reservation and report failure.
Report other preparation failures; never silently use another location.

Return the reserved path. After the task, remove only this run's files;
leave the root and exclude entry.
