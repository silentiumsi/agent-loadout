#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PYORACLE'
import json, subprocess
from pathlib import Path
diff = subprocess.run(["git", "diff", "base..HEAD"], capture_output=True, text=True, check=True).stdout
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "git diff base..HEAD"}}], "observation": {"results": [{"content": diff}]}}]
steps.append({"step_id": 4, "source": "agent", "message": 'Request changes. Reviewed cumulative base..HEAD, including all six PRs. Blocking correctness issue at paging.py:5: PR 1 changes page_offset to a zero-based offset but PR 6 subtracts one again. page_items([1,2,3,4],1,2) returns [] rather than [1,2]. Remove the second subtraction and add a first-page regression test. This is a cross-layer contract mismatch, established by source inspection; tests were not run.'})
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"schema_version": "ATIF-v1.6", "agent": {"name": "synthetic-oracle"}, "steps": steps}))
print('Request changes. Reviewed cumulative base..HEAD, including all six PRs. Blocking correctness issue at paging.py:5: PR 1 changes page_offset to a zero-based offset but PR 6 subtracts one again. page_items([1,2,3,4],1,2) returns [] rather than [1,2]. Remove the second subtraction and add a first-page regression test. This is a cross-layer contract mismatch, established by source inspection; tests were not run.')
PYORACLE
