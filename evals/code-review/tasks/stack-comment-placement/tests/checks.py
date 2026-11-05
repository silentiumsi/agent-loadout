"""Placement checks over the comments the fake gh recorded."""
import json
import subprocess
from pathlib import Path
from rewardkit import criterion

POSTS = Path("/logs/agent/gh-posts.jsonl")


def inline(pr, path, first, last):
    if not POSTS.is_file():
        return False
    posts = [json.loads(line) for line in POSTS.read_text().splitlines() if line.strip()]
    return any(p["kind"] == "inline" and p["pr"] == pr and p["path"] == path and first <= p["line"] <= last and p["body"].strip() for p in posts)


@criterion(description="The reviewed source is unchanged")
def source_preserved(workspace: Path):
    return subprocess.run(["git", "-C", str(workspace), "status", "--porcelain"], capture_output=True, text=True).stdout.strip() == ""


@criterion(description="The reserve defect is an inline comment on PR 11 at inventory.py reserve")
def reserve_on_owner(workspace: Path):
    return inline(11, "inventory.py", 14, 15)


@criterion(description="The place_order defect is an inline comment on PR 12 at orders.py place_order")
def order_on_owner(workspace: Path):
    return inline(12, "orders.py", 8, 10)
