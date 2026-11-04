"""Check the artifact after this conversational turn, allowing free prose."""
import json
import os
import re
from pathlib import Path
from rewardkit import criterion

SPEC = json.loads(Path(__file__).with_name("expectations.json").read_text())
STAGE = SPEC[os.environ["WRITING_STAGE"]]


def sections(text):
    """The editor requests these headings; wording within them is unrestricted."""
    parts = re.split(r"^##[ \t]+(.+?)[ \t]*$", text, flags=re.MULTILINE)
    if len(parts[1::2]) != len(set(parts[1::2])):
        return None
    return {name: body.strip() for name, body in zip(parts[1::2], parts[2::2])}


def artifact(workspace):
    path = workspace / "guide.md"
    return path.read_text() if path.is_file() else ""


@criterion(description="The requested increment is in guide.md and later increments remain undrafted")
def increment_boundary(workspace: Path) -> bool:
    text = artifact(workspace)
    if "unchanged" in STAGE:
        return text == STAGE["unchanged"]
    actual = sections(text)
    if actual is None or set(actual) != set(STAGE["sections"]):
        return False
    return all(bool(actual[name]) == bool(patterns)
               for name, patterns in STAGE["sections"].items())


@criterion(description="The artifact contains the requested facts and corrections in the relevant sections")
def delivered_meaning(workspace: Path) -> bool:
    text = artifact(workspace)
    if "unchanged" in STAGE:
        return text == STAGE["unchanged"]
    actual = sections(text)
    if actual is None:
        return False
    return all(name in actual and all(re.search(pattern, actual[name], re.IGNORECASE)
                                     for pattern in patterns)
               for name, patterns in STAGE["sections"].items()) and all(
        not re.search(pattern, text, re.IGNORECASE)
        for pattern in STAGE.get("forbidden", [])
    )


@criterion(description="Previously accepted text outside the authorized revision scope remains unchanged")
def accepted_text(workspace: Path) -> bool:
    actual = sections(artifact(workspace))
    return actual is not None and all(
        actual.get(name) == body for name, body in STAGE.get("protected", {}).items()
    )
