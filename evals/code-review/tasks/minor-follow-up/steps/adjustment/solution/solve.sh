#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json, subprocess
from pathlib import Path
diff = subprocess.run(["git", "diff", "base..HEAD"], capture_output=True, text=True, check=True).stdout
Path('app.py').write_text('def display_name(name):\n    """Remove surrounding whitespace from a display name."""\n    return name.strip()\n')
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "git diff base..HEAD"}}], "observation": {"results": [{"content": diff}]}}]
steps.append({"step_id": 2, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": '{\'app.py\': \'def display_name(name):\\n    """Remove surrounding whitespace from a display name."""\\n    return name.strip()\\n\'}'}}], "observation": {"results": [{"content": "Files updated by oracle"}]}})
steps.append({"step_id": 4, "source": "agent", "message": 'Completed the requested increment. Updated app.py.'})
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print('Completed the requested increment. Updated app.py.')
PYORACLE
