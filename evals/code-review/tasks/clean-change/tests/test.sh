#!/bin/bash
set -euo pipefail
python3 - <<'PYEVIDENCE'
import json
import os
from pathlib import Path
trace = Path("/logs/agent/trajectory.json")
if not trace.is_file():
    raise RuntimeError("SETUP ERROR: missing trajectory")
exported = json.loads(trace.read_text())
if not exported.get("steps"):
    raise RuntimeError("SETUP ERROR: empty trajectory")
native = {}
for path in Path("/logs/agent/sessions").rglob("rollout-*.jsonl"):
    with path.open() as stream:
        meta = json.loads(stream.readline()).get("payload", {})
    if meta.get("id"):
        native[meta["id"]] = (meta, path)
context = {"exported_session": exported.get("session_id"), "evidence_kind": "ATIF", "coordinator": exported}
if native:
    selected = exported.get("session_id")
    if selected not in native:
        raise RuntimeError("SETUP ERROR: exported Codex session is absent from native logs")
    seen = set()
    while isinstance(native[selected][0].get("source"), dict):
        if selected in seen:
            raise RuntimeError("SETUP ERROR: cyclic native session ancestry")
        seen.add(selected)
        selected = native[selected][0]["source"]["subagent"]["thread_spawn"]["parent_thread_id"]
        if selected not in native:
            raise RuntimeError("SETUP ERROR: missing coordinator session")
    meta, path = native[selected]
    events = []
    for line in path.read_text().splitlines():
        record = json.loads(line)
        item = record.get("payload", {})
        if record.get("type") == "response_item" and item.get("role") not in ("system", "developer"):
            events.append(item)
    children = []
    for sid, (child, child_path) in native.items():
        source = child.get("source")
        if isinstance(source, dict) and source.get("subagent", {}).get("thread_spawn", {}).get("parent_thread_id") == selected:
            children.append({"session": sid, "path": str(child_path), "source": source})
    context = {"evidence_kind": "native coordinator", "exported_session": exported.get("session_id"),
               "coordinator_session": selected, "exported_child_instead_of_coordinator": selected != exported.get("session_id"),
               "coordinator_native_path": str(path), "coordinator_events": events, "direct_child_sessions": children,
               "limits": "Child session metadata proves launches, not review coverage. Inspect child native files when findings or checks were delegated. Failed launch attempts are not completed reviewers."}
context["stage"] = os.environ.get("REVIEW_STAGE", "single")
Path("/logs/verifier/review-context.json").write_text(json.dumps(context, indent=2) + "\n")
PYEVIDENCE
rewardkit /tests --workspace /app
