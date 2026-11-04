#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json, subprocess
from pathlib import Path
diff = subprocess.run(["git", "diff", "base..HEAD"], capture_output=True, text=True, check=True).stdout
Path('SKILL.md').write_text('---\nname: meeting-notes\ndescription: Turn meeting transcripts into useful notes.\n---\n# Meeting Notes\n\nSummarize decisions and assign action items to their owners.\n\nName action owners.\nInclude due dates when supplied.\n')
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "git diff base..HEAD"}}], "observation": {"results": [{"content": diff}]}}]
steps.append({"step_id": 2, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "{'SKILL.md': '---\\nname: meeting-notes\\ndescription: Turn meeting transcripts into useful notes.\\n---\\n# Meeting Notes\\n\\nSummarize decisions and assign action items to their owners.\\n\\nName action owners.\\nInclude due dates when supplied.\\n'}"}}], "observation": {"results": [{"content": "Files updated by oracle"}]}})
steps.append({"step_id": 4, "source": "agent", "message": 'Completed the requested increment. Updated SKILL.md.'})
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print('Completed the requested increment. Updated SKILL.md.')
PYORACLE
