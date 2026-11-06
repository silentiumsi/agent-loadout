"""Exact syntax preservation and narrow, historically observed grouping failures."""
import re
from pathlib import Path
from rewardkit import criterion

FILE = 'run.go'
ORIGINAL = Path(__file__).parent / "original" / FILE
TOKEN = re.compile(r"""//[^\n]*|/\*[\s\S]*?\*/|"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|`[^`]*`|[^\s]""", re.MULTILINE)

def tokens(source):
    return TOKEN.findall(source)

def source(workspace):
    return (workspace / "project" / FILE).read_text()

def gap(text, left, right, blank):
    left_pattern = r"\s*".join(re.escape(token) for token in tokens(left))
    right_pattern = r"\s*".join(re.escape(token) for token in tokens(right))
    pattern = left_pattern + r"([ \t]*\n(?:[ \t]*\n)*[ \t]*)" + right_pattern
    found = re.search(pattern, text)
    if not found:
        return False
    return found.group(1).count("\n") == (2 if blank else 1)

@criterion
def syntax_preserved(workspace: Path) -> bool:
    return tokens(source(workspace)) == tokens(ORIGINAL.read_text())

@criterion
def other_files_preserved(workspace: Path) -> bool:
    return {str(p.relative_to(workspace / "project")) for p in (workspace / "project").rglob("*") if p.is_file() and ".git" not in p.parts} == {FILE}

@criterion
def independent_steps_separated(workspace: Path) -> bool:
    return gap(source(workspace), "m.startWatch()", "if _, err := tea.NewProgram(m).Run(); err != nil {", True)

@criterion
def immediate_error_check_kept_together(workspace: Path) -> bool:
    return gap(source(workspace), "root, err := repoRoot(dir)", "if err != nil {", False)
