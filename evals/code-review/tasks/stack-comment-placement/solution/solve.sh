#!/bin/bash
set -euo pipefail
cd /app
gh api repos/acme/shop/pulls/11/comments -f body='reserve never checks available stock, so an order larger than the stock drives it negative (oversell). Check qty <= available before decrementing.' -f path=inventory.py -F line=15 -f commit_id="$(git rev-parse stack-1)" >/dev/null
gh api repos/acme/shop/pulls/12/comments -f body='If charge raises PaymentError (declined card) the reservation is never released, so stock leaks. Release it on failure.' -f path=orders.py -F line=10 -f commit_id="$(git rev-parse stack-2)" >/dev/null
python3 - <<'PYORACLE'
import json
from pathlib import Path
report = 'Request changes. Inline comments left on #11 (reserve oversell) and #12 (reservation not released when the charge fails). #13 is clean.'
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "gh api repos/acme/shop/pulls/11/comments"}}]}, {"step_id": 2, "source": "agent", "message": report}]
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print(report)
PYORACLE
