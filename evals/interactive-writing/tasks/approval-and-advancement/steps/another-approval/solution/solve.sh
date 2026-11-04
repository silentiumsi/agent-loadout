#!/bin/bash
set -euo pipefail
cat > /app/guide.md <<'DOCUMENT'
# Ledger export guide

## Prepare

Check the installed version with `ledger --version`.

## Export

Run `ledger export --output snapshot.json` to save an export.

## Restore

Run `ledger restore --input snapshot.json` to restore an export.
DOCUMENT
