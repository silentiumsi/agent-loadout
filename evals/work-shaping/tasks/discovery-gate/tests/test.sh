#!/bin/bash
set -eu
mkdir -p /tmp/judge/submission /tmp/judge/authority
cp -r /tests/.project/. /tmp/judge/authority/
cp /tests/.request.md /tmp/judge/authority/request.md
if [ -f /app/project/plan.md ]; then cp /app/project/plan.md /tmp/judge/submission/plan.md; else printf 'No submission.\n' > /tmp/judge/submission/plan.md; fi
uvx --python '>=3.12,<3.14' --from 'harbor-rewardkit==0.2.*' rewardkit /tests --workspace /app --yolo
