#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json
from pathlib import Path
from normalize import normalize
assert normalize([" A ", "", "  ", "B"]) == ["A", "B"]
source = Path("normalize.py").read_text() + "\n" + Path("SKILL.md").read_text()
report = "Approve. Reviewed the uncommitted normalizer and relevant skill instructions. Empty and whitespace-only lines are removed and retained lines are stripped. Focused checks passed. No blocker found; no files changed."
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "cat normalize.py SKILL.md; run normalization assertions"}}], "observation": {"results": [{"content": source + "\nChecks passed"}]}}, {"step_id": 2, "source": "agent", "message": report}]
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"agent": {"name": "synthetic-oracle"}, "steps": steps}))
print(report)
PYORACLE
