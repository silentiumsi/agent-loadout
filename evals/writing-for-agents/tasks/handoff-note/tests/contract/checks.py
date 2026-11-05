"""File contracts, kept apart from fidelity and prose quality."""

from pathlib import Path

from rewardkit import criterion

OUTPUTS = ('HANDOFF.md',)
TRUSTED = Path(__file__).resolve().parent.parent / ".project"


@criterion
def outputs_present(workspace: Path) -> bool:
    return all(
        (workspace / "project" / n).is_file()
        and (workspace / "project" / n).read_text(errors="replace").strip()
        for n in OUTPUTS
    )


@criterion
def other_files_preserved(workspace: Path) -> bool:
    project = workspace / "project"
    expected = {str(p.relative_to(TRUSTED)) for p in TRUSTED.rglob("*") if p.is_file()}
    actual = {str(p.relative_to(project)) for p in project.rglob("*") if p.is_file()}
    if not expected <= actual or actual - expected - set(OUTPUTS):
        return False
    return all(
        n in OUTPUTS or (project / n).read_bytes() == (TRUSTED / n).read_bytes()
        for n in expected
    )
