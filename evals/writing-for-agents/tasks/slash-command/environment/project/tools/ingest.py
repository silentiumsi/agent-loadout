"""Ingest triage output from stdin (local fixture).

Each nonblank line must be one JSON object with exactly these keys:
  id        integer issue number
  severity  one of "p0", "p1", "p2"
  summary   string of at most 80 characters
Any other line (prose, blank-looking markdown, code fences) is rejected.
Prints {"accepted": N, "rejected": [...]}. Exits 0 even when lines are rejected;
inspect "rejected". Empty input is valid and accepts 0.
"""
import json
import sys

accepted = 0
rejected = []
for number, line in enumerate(sys.stdin, 1):
    line = line.strip()
    if not line:
        continue
    try:
        obj = json.loads(line)
    except json.JSONDecodeError:
        rejected.append({"line": number, "why": "not JSON"})
        continue
    if not isinstance(obj, dict) or set(obj) != {"id", "severity", "summary"}:
        rejected.append({"line": number, "why": "wrong keys"})
    elif not isinstance(obj["id"], int) or isinstance(obj["id"], bool):
        rejected.append({"line": number, "why": "id must be an integer"})
    elif obj["severity"] not in ("p0", "p1", "p2"):
        rejected.append({"line": number, "why": "bad severity"})
    elif not isinstance(obj["summary"], str) or len(obj["summary"]) > 80:
        rejected.append({"line": number, "why": "bad summary"})
    else:
        accepted += 1
print(json.dumps({"accepted": accepted, "rejected": rejected}))
