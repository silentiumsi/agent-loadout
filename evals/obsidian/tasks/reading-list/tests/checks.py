"""Check a reading list in the discovered vault without changing existing files."""

import hashlib
import re
from datetime import date
from pathlib import Path

import yaml
from rewardkit import criterion

# sha256 of every file the environment ships in the vault.
FIXTURE = {
    "AGENTS.md": "f0eb0022713b40bbab3b53d02b010cd62ca39af99f1a487571a0cf835ba1ad6d",
    "Daily/2026-10-25.md": "f7c3c594a1e2a4d29f151c0b36d5645fab633a160fa7bc8a5055b7cab78860e5",
    "Home.md": "f67a19939980174c22709b68723c7afe6fe85618a9335a400234f46790aa3a87",
    "Lists/Books to Read.md": "5a19754e7dbad08e9aafe1f747ead994dc6543c2819c49ebc92445b983709367",
    ".obsidian/app.json": "4c8c70ca6865928c0d7f17d527b800168de408f331016511701f65915e958940",
    "Projects/Garden.md": "cee5012bbfa7df2c0ddbb99d89e9d72e18b80661031ede50abbaf9779ed3773e",
}
SMALL_WORDS = {"a", "an", "and", "by", "for", "in", "of", "on", "or", "the", "to"}


def new_files(workspace: Path) -> list[Path]:
    files = [p for p in workspace.rglob("*") if p.is_file()]
    return [p for p in files if p.relative_to(workspace).as_posix() not in FIXTURE]


def new_note(workspace: Path) -> Path | None:
    files = new_files(workspace)
    return files[0] if len(files) == 1 and files[0].suffix == ".md" else None


@criterion(description="Exactly one new file was added to the vault, and it is a .md note")
def one_new_note(workspace: Path) -> bool:
    return new_note(workspace) is not None


@criterion(description="The new note is filed in Lists/, as AGENTS.md requires")
def filed_in_lists(workspace: Path) -> bool:
    note = new_note(workspace)
    return note is not None and note.parent == workspace / "Lists"


@criterion(description="The new note's filename is in Title Case")
def title_case_name(workspace: Path) -> bool:
    note = new_note(workspace)
    if note is None:
        return False

    words = note.stem.split()
    return all(
        not w[0].islower() or (i > 0 and w in SMALL_WORDS) for i, w in enumerate(words)
    )


@criterion(description="The new note starts with frontmatter holding tags and a YYYY-MM-DD created date")
def has_frontmatter(workspace: Path) -> bool:
    note = new_note(workspace)
    if note is None:
        return False

    match = re.match(r"---\n(.*?)\n---\n", note.read_text(), re.DOTALL)
    if match is None:
        return False

    try:
        front = yaml.safe_load(match.group(1))
        if not isinstance(front, dict) or "tags" not in front or "created" not in front:
            return False
        created = str(front["created"])
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", created):
            return False
        date.fromisoformat(created)
    except (yaml.YAMLError, ValueError):
        return False
    return True


@criterion(description="The new note contains all three requested book titles")
def requested_books(workspace: Path) -> bool:
    note = new_note(workspace)
    if note is None:
        return False

    text = note.read_text().casefold()
    return all(
        title.casefold() in text
        for title in ("A Wizard of Earthsea", "Kindred", "The Hobbit")
    )


@criterion(description="No file the vault shipped with was changed, moved or deleted")
def fixture_untouched(workspace: Path) -> bool:
    return all(
        (workspace / rel).is_file()
        and hashlib.sha256((workspace / rel).read_bytes()).hexdigest() == digest
        for rel, digest in FIXTURE.items()
    )
