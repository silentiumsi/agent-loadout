"""Offline artifact checks; semantic review and orchestration use separate judges."""
import hashlib
import json
import subprocess
import os
from pathlib import Path
from rewardkit import criterion

SPEC = json.loads(Path("/tests/spec.json").read_text())

@criterion(description="Review-only tasks preserve the reviewed source snapshot")
def source_preserved(workspace: Path):
    if not SPEC["review_only"]:
        return True
    return all((workspace / name).is_file() and hashlib.sha256((workspace / name).read_bytes()).hexdigest() == digest for name, digest in SPEC["hashes"].items())

@criterion(description="The requested executable behavior is present")
def requested_behavior(workspace: Path):
    probe = SPEC.get("probe")
    if os.environ.get("REVIEW_STAGE") == "first-increment":
        probe = 'from app import display_name; assert display_name(" A   B ") == "A B"'
    if not probe:
        return True
    result = subprocess.run(["python3", "-c", probe], cwd=workspace, capture_output=True, timeout=10)
    return {"score": float(result.returncode == 0), "reasoning": result.stderr.decode()[-2000:]}
