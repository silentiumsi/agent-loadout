"""Deterministic fidelity: the command's own example must satisfy the real parser."""

import json
import re
import subprocess
import sys
from pathlib import Path

from rewardkit import criterion

REL = "commands/triage.md"
INGEST = Path(__file__).resolve().parent.parent / ".project" / "tools" / "ingest.py"


def _text(workspace: Path) -> str:
    p = workspace / "project" / REL
    return p.read_text(errors="replace") if p.is_file() else ""


def _example_lines(text: str) -> list[str]:
    """Standalone JSON-looking lines; placeholder templates such as {"id": <integer>} are not examples."""
    return [
        l.strip()
        for l in text.splitlines()
        if l.strip().startswith("{") and l.strip().endswith("}") and not re.search(r"<[^>]+>", l)
    ]


def _ingest(lines: list[str]) -> dict:
    out = subprocess.run([sys.executable, "-I", str(INGEST)], input="\n".join(lines) + "\n", capture_output=True, text=True, timeout=20).stdout
    return json.loads(out)


@criterion
def example_parses(workspace: Path) -> bool:
    """The command shows at least one example line, and the real tool accepts every one."""
    lines = _example_lines(_text(workspace))
    if not lines:
        return False
    r = _ingest(lines)
    return r["accepted"] == len(lines) and not r["rejected"]
