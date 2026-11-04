"""Implementation task: the requested behavior must work."""
import subprocess
from pathlib import Path
from rewardkit import criterion

PROBE = 'from app import display_name; assert display_name(None) == ""; assert display_name(" A ") == "A"'


@criterion(description="The requested behavior works")
def requested_behavior(workspace: Path):
    result = subprocess.run(["python3", "-c", PROBE], cwd=workspace, capture_output=True, timeout=10)
    return {"score": float(result.returncode == 0), "reasoning": result.stderr.decode()[-2000:]}
