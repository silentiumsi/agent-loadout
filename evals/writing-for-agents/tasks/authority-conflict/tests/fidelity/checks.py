"""Deterministic fidelity: facts the repository establishes, against the notes' errors."""

import re
from pathlib import Path

from rewardkit import criterion


def _text(workspace: Path) -> str:
    p = workspace / "project" / "AGENTS.md"
    return p.read_text(errors="replace") if p.is_file() else ""


@criterion
def name_limit_is_40(workspace: Path) -> bool:
    """tools/kc.py rejects names over 40. Guidance may mention the notes' 32 only to flag the conflict."""
    t = _text(workspace)
    if re.search(r"\b40\b", t) is None:
        return False
    for line in t.splitlines():
        if re.search(r"\b32\b", line) and not re.search(r"\b(notes?|Dana|said|says|claims?|but|actually|differs?|however|conflicts?|contradicts?|stale|wrong)\b", line, re.I):
            return False
    return True


@criterion
def ci_not_claimed_to_enforce_tests(workspace: Path) -> bool:
    """CI only lints. Guidance must not say CI blocks, runs, or rejects on tests."""
    for line in _text(workspace).splitlines():
        if re.search(r"\bCI\b[^.\n]{0,40}\b(blocks?|enforces?|rejects?|requires?|runs? the tests?|gates?)\b", line, re.I):
            if not re.search(r"\b(not|n't|nothing|only|lint)\b", line, re.I):
                return False
    return True
