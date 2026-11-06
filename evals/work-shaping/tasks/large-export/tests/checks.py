from pathlib import Path
from rewardkit import criterion

@criterion
def output_present(workspace: Path) -> bool:
    output = workspace / "project/plan.md"
    return output.is_file() and bool(output.read_text().strip())

@criterion
def sources_preserved(workspace: Path) -> bool:
    trusted = Path(__file__).parent / ".project"
    project = workspace / "project"
    return all((project / p.relative_to(trusted)).is_file() and (project / p.relative_to(trusted)).read_bytes() == p.read_bytes() for p in trusted.rglob("*") if p.is_file())
