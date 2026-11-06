"""Behavior and syntax-based layout, independent of implementation identifiers."""
import json
import subprocess
from functools import lru_cache
from pathlib import Path

from rewardkit import criterion


@lru_cache
def inspect(workspace: Path) -> dict:
    result = subprocess.run(
        ["node", str(Path(__file__).with_name("inspect.cjs")),
         str(workspace / "project/state.ts")],
        capture_output=True, text=True, timeout=45,
    )
    if result.returncode:
        return {"error": result.stderr}
    return json.loads(result.stdout)


@criterion
def types_valid(workspace: Path) -> bool:
    return inspect(workspace).get("types_valid", False)


@criterion
def public_types_preserved(workspace: Path) -> bool:
    return inspect(workspace).get("public_types_preserved", False)


@criterion
def pagination_contract(workspace: Path) -> bool:
    names = ["pagination_and_navigation", "failure_and_retry", "overlapping_refresh",
             "workspace_isolation", "pending_more_is_noop"]
    return all(inspect(workspace).get(name, False) for name in names)


@criterion
def declarations_separated(workspace: Path) -> bool:
    return inspect(workspace).get("declarations_separated", False)


@criterion
def members_separated(workspace: Path) -> bool:
    return inspect(workspace).get("members_separated", False)
