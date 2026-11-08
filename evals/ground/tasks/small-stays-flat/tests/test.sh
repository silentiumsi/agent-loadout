#!/bin/bash
set -euo pipefail
if [ "$GROUND_STAGE" != "final" ]; then
  rm -f /tests/judge.toml
fi
rewardkit /tests --workspace /app
