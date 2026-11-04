#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json, subprocess
from pathlib import Path
diff = subprocess.run(["git", "diff", "base..HEAD"], capture_output=True, text=True, check=True).stdout
Path('app.py').write_text('def display_name(name):\n    return "" if name is None else " ".join(name.split())\n')
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "git diff base..HEAD"}}], "observation": {"results": [{"content": diff}]}}]
steps.append({"step_id": 2, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": '{\'app.py\': \'def display_name(name):\\n    return "" if name is None else " ".join(name.split())\\n\'}'}}], "observation": {"results": [{"content": "Files updated by oracle"}]}})
subprocess.run(["python3", "-c", 'from app import display_name; assert display_name(None) == ""; assert display_name(" A ") == "A"; assert display_name(" A   B ") == "A B"'], check=True)
steps.append({"step_id": 3, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": 'from app import display_name; assert display_name(None) == ""; assert display_name(" A ") == "A"; assert display_name(" A   B ") == "A B"'}}], "observation": {"results": [{"content": "Checks passed"}]}})
steps.append({"step_id": 4, "source": "agent", "message": 'Completed the requested increment. Updated app.py. Focused executable checks passed.'})
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print('Completed the requested increment. Updated app.py. Focused executable checks passed.')
PYORACLE
