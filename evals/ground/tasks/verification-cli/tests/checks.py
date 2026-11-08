"""Structural checks for ground output. Judgment lives in judge.toml."""
import os
import re
from pathlib import Path
from rewardkit import criterion

STAGE = os.environ["GROUND_STAGE"]
NEEDS_DIAGRAM = os.environ.get("GROUND_DIAGRAM") == "1"
NO_AREAS_AFTER_BRIEF = os.environ.get("GROUND_NO_AREAS_AFTER_BRIEF") == "1"
NO_AREAS_EVER = os.environ.get("GROUND_NO_AREAS_EVER") == "1"

PROCESS_LANGUAGE = [
    r"\bspikes? (result|results|showed|shows|confirmed|found|proved|demonstrated|revealed|established|run|ran)\b",
    r"\b(confirmed|shown|proved|found|validated|verified|established) (by|in|through|via|with) (a |an |the |our )?(spike|prototype run|experiment)\b",
    r"\bround \d+\b",
    r"\bas (we )?discussed\b",
    r"\bper (our|the) (conversation|discussion|interview)\b",
    r"\bthe user (confirmed|approved|agreed|decided|said|chose)\b",
    r"\bplannotator\b",
]
DECISION_ID = re.compile(r"\b(D\d{1,3}|ADR[- ]?\d+|decision[- ]\d+)\b")
DIAGRAM = re.compile(
    r"```(mermaid|dot|plantuml|d2|ascii|text|txt)\b|^\|.+\|\s*\n\|[\s:|-]+\|\s*$|!\[[^\]]*\]\(",
    re.MULTILINE | re.IGNORECASE,
)


def ground(workspace: Path) -> Path:
    return workspace / "ground"


def read(path: Path) -> str:
    return path.read_text(errors="replace") if path.is_file() else ""


def documents(workspace: Path):
    folder = ground(workspace)
    return sorted(folder.rglob("*.md")) if folder.is_dir() else []


def top_text(workspace: Path) -> str:
    return read(ground(workspace) / "product.md") + "\n" + read(ground(workspace) / "design.md")


@criterion(description="product.md and design.md exist from the first turn, with content in product.md")
def pair_exists(workspace: Path) -> bool:
    product = read(ground(workspace) / "product.md").strip()
    design = (ground(workspace) / "design.md").is_file()
    return len(product) > 40 and design


@criterion(description="The retired spec.md and slices.md layout is not used")
def no_retired_layout(workspace: Path) -> bool:
    return not (ground(workspace) / "spec.md").exists() and not (ground(workspace) / "slices.md").exists()


@criterion(description="Files carry no decision ids or build-process history")
def evergreen_language(workspace: Path) -> bool:
    for path in documents(workspace):
        text = read(path)
        if DECISION_ID.search(text):
            return False
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in PROCESS_LANGUAGE):
            return False
    return True


@criterion(description="A diagram, table or similar visual appears in the top-level files when the project needs one")
def visual_present(workspace: Path) -> bool:
    return not NEEDS_DIAGRAM or STAGE != "final" or bool(DIAGRAM.search(top_text(workspace)))


@criterion(description="No sub-structure exists before the user has approved any")
def no_early_promotion(workspace: Path) -> bool:
    if NO_AREAS_EVER:
        return not any(ground(workspace).rglob("areas"))
    if NO_AREAS_AFTER_BRIEF and STAGE == "brief":
        return not any(ground(workspace).rglob("areas"))
    return True


@criterion(description="Every promoted area has its own product file and is linked from its parent")
def promotions_linked(workspace: Path) -> bool:
    for areas in ground(workspace).rglob("areas") if ground(workspace).is_dir() else []:
        parent = areas.parent
        parent_text = read(parent / "product.md") + read(parent / "design.md")
        for area in sorted(p for p in areas.iterdir() if p.is_dir()):
            if not (area / "product.md").is_file():
                return False
            if f"areas/{area.name}" not in parent_text:
                return False
    return True
