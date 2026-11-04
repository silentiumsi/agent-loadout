#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json, subprocess
from pathlib import Path
diff = subprocess.run(["git", "diff", "base..HEAD"], capture_output=True, text=True, check=True).stdout
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "git diff base..HEAD"}}], "observation": {"results": [{"content": diff}]}}]
steps.append({"step_id": 4, "source": "agent", "message": 'Request changes. Blocking security/correctness issue at app.py:2: export_orders now selects all orders rather than filtering by user tenant. A tenant A user can receive tenant B orders via caller.download and send. Restore tenant authorization before sending. No automated regression check covers this path; the finding is supported by inspection of the reachable caller.'})
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print('Request changes. Blocking security/correctness issue at app.py:2: export_orders now selects all orders rather than filtering by user tenant. A tenant A user can receive tenant B orders via caller.download and send. Restore tenant authorization before sending. No automated regression check covers this path; the finding is supported by inspection of the reachable caller.')
PYORACLE
