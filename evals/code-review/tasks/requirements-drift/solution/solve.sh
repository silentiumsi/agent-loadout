#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json, subprocess
from pathlib import Path
diff = subprocess.run(['git', 'diff', 'base..HEAD'], capture_output=True, text=True, check=True).stdout
report = 'Request changes. Reviewed base..HEAD. REFUND_WINDOW is 14 days but docs/adr-007-refunds.md requires refunds to be accepted for 30 days, so valid refunds between day 15 and 30 are rejected. Blocking. Set the window to 30 days and update test_window. Tests were not run.'
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": 'git diff base..HEAD'}}], "observation": {"results": [{"content": diff}]}}]
steps.append({"step_id": 2, "source": "agent", "message": report})
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print(report)
PYORACLE
