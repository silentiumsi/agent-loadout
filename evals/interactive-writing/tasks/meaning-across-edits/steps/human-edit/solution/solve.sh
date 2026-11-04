#!/bin/bash
set -euo pipefail
cat > /app/guide.md <<'DOCUMENT'
# Willow incident guide

## Scope

This procedure covers the Willow production service.

## Detection

Check the Willow dashboard at 09:00 UTC. If the outage lasts ten minutes, notify duty@example.test. Do not contact the vendor.

## Escalation

DOCUMENT
