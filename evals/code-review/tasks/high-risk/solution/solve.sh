#!/bin/bash
set -euo pipefail
cd /app
python3 - <<'PY'
import json
import subprocess
from pathlib import Path
from caller import download

orders = [{"tenant": "a", "id": 1}, {"tenant": "b", "id": 2}]
sent = []
assert download({"tenant": "a"}, orders, sent.append) == 2
assert [order["tenant"] for order in sent] == ["a", "b"]
partial = []
def fail_second(order):
    if partial:
        raise RuntimeError("delivery failed")
    partial.append(order)
try:
    download({"tenant": "a"}, [{**order, "tenant": "a"} for order in orders], fail_second)
except RuntimeError:
    pass
else:
    raise AssertionError("callback failure must propagate")
assert len(partial) == 1
empty = []
assert download({}, [], empty.append) == 0
malformed = []
assert download({}, orders, malformed.append) == 2
assert len(malformed) == 2
source = subprocess.check_output(["git", "diff", "base..HEAD"], text=True)
source += "\n" + Path("app.py").read_text() + "\n" + Path("caller.py").read_text() + "\n" + Path("test_app.py").read_text()
observed = "Mixed-tenant input delivered both tenants' orders. Callback failure propagated after one delivery, with no success count or rollback. Empty input returned zero. Missing tenant identity still delivered all orders."
report = """Request changes. Reviewed base..HEAD.
Blocking security/correctness issue at app.py:2: tenant filtering was removed. caller.download forwards user and orders without an upstream guard, so a tenant-a request sends tenant-b records. Restore filtering before send and add mixed-tenant regression coverage.
Coverage: the direct reproduction through download delivered both tenants' records. A failing second callback propagated RuntimeError after one delivery; the code provides no rollback and returns no success count on failure, as before. Empty input returns zero. Missing tenant identity is now ignored, consistent with the removed authorization check. The test file contains no regression tests; these focused checks do not replace them.
Workload: for N input records and T authorized records, both versions scan N. Retained records and send calls grow from T to N; for N=1000 and T=10 that is 100 times as many retained records and deliveries. Real latency depends on send and collection sizes. No deployment workload was measured. No files were edited."""
steps = [{"step_id": 1, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "git diff base..HEAD; read app.py caller.py test_app.py"}}], "observation": {"results": [{"content": source}]}}, {"step_id": 2, "source": "agent", "tool_calls": [{"function_name": "exec_command", "arguments": {"cmd": "Run mixed-tenant, callback-failure, empty-input, and malformed-user assertions through caller.download"}}], "observation": {"results": [{"content": observed}]}}, {"step_id": 3, "source": "agent", "message": report}]
Path("/logs/agent").mkdir(parents=True, exist_ok=True)
Path("/logs/agent/trajectory.json").write_text(json.dumps({"agent": {"name": "synthetic-oracle"}, "steps": steps}))
print(report)
PY
