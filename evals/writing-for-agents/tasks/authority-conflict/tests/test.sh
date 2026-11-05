#!/bin/bash
set -eu

# Blind staging: the judge sees only the submission and trusted authority, with no
# skill or condition names.
mkdir -p /tmp/judge/submission /tmp/judge/authority
mkdir -p /tmp/judge/submission/.
cp -r /tests/.project/. /tmp/judge/authority/
if [ -f "/app/project/AGENTS.md" ]; then cp "/app/project/AGENTS.md" "/tmp/judge/submission/AGENTS.md"; else printf 'No submission.\n' > "/tmp/judge/submission/AGENTS.md"; fi

# The judges run in the /tmp/judge staging copy, outside the workspace the other
# checks read, so they cannot disturb them; --yolo acknowledges rewardkit's
# shared-workspace guard, which assumes judges run inside the workspace.
uvx --python '>=3.12,<3.14' --from 'harbor-rewardkit==0.2.*' rewardkit /tests --workspace /app --yolo
