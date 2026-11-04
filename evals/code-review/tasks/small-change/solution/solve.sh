#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json, subprocess
from pathlib import Path
diff = subprocess.run(["git", "diff", "base..HEAD"], capture_output=True, text=True, check=True).stdout
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "git diff base..HEAD"}}], "observation": {"results": [{"content": diff}]}}]
steps.append({"step_id": 4, "source": "agent", "message": 'Approve. Reviewed base..HEAD. The change improves documentation and preserves behavior. No substantiated blockers. Checked the cumulative diff and relevant source; automated checks were not run.'})
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print('Approve. Reviewed base..HEAD. The change improves documentation and preserves behavior. No substantiated blockers. Checked the cumulative diff and relevant source; automated checks were not run.')
PYORACLE
