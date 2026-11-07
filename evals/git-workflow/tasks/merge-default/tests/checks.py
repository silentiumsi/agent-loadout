"""Check the merge action recorded by the local GitHub fixture."""
import json
from pathlib import Path
from rewardkit import criterion


@criterion
def squash_merge_performed(workspace: Path) -> bool:
    record = workspace / "merge.json"
    if not record.is_file():
        return False
    action = json.loads(record.read_text())
    return action.get("number") == 42 and action.get("method") == "squash"
