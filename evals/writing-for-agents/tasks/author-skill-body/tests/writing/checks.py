"""Padding check: the request seeds generic exhortations that a skill should not carry."""

import re
from pathlib import Path

from rewardkit import criterion

REL = "skills/release-notes/SKILL.md"


def _text(workspace: Path) -> str:
    p = workspace / "project" / REL
    return p.read_text(errors="replace") if p.is_file() else ""


@criterion
def no_generic_filler(workspace: Path) -> bool:
    return re.search(r"double-check your work|professional tone|be accurate|write clearly|be concise", _text(workspace), re.I) is None
