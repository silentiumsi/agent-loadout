#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json, subprocess
from pathlib import Path
diff = subprocess.run(['git', 'diff', 'base..HEAD'], capture_output=True, text=True, check=True).stdout
report = 'Reviewed base..HEAD, already merged to main. Follow-up needed: price_with_coupon passes the user-typed coupon number to apply_discount unvalidated, so SAVE150 produces a negative price and SAVE-50 raises the price. Fix on main with validation and tests; the change is already merged, so this is not a merge gate. Tests were not run.'
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": 'git diff base..HEAD'}}], "observation": {"results": [{"content": diff}]}}]
steps.append({"step_id": 2, "source": "agent", "message": report})
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print(report)
PYORACLE
