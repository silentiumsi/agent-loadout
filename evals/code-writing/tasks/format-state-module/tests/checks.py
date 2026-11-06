"""Exact syntax preservation and narrow, historically observed grouping failures."""
import re
from pathlib import Path
from rewardkit import criterion

FILE = 'state.ts'
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

# Exact, fixture-specific preferences; these do not judge general readability.
DECLARATIONS = [
    ("}", "export interface Entry"),
    ("}", "export interface Section<T>"),
    ("}", "export interface WorkspaceState"),
    ("}", "const section"),
    ("};", "const mergePage"),
    ("};", "export class CatalogState"),
]
MEMBERS = [
    ("private readonly workspaces = new Map<string, WorkspaceState>();", "constructor"),
    (") {}", "select(key: string)"),
    ("}", "cached()"),
    ("}", "open(id: string)"),
    ("}", "back()"),
    ("}", "async loadList"),
]
STEPS = [
    ("for (const item of next.items) items.set(item.id, item);", "return"),
    ("this.workspaces.set(key, state);\n    }", "this.current = state;"),
    ("if (!state) return;", "state.selected = id;"),
    ("if (!state) return;", "const target = state.list;"),
    ("target.pending = true;", "try {"),
]
RELATED = [
    ("let state = this.workspaces.get(key);", "if (!state) {"),
    ("const state = this.current;", "if (!state) return;"),
    ("const next = await this.fetchPage(state.key, cursor);", "if (target.generation !== generation) return;"),
]

@criterion
def declarations_separated(workspace: Path) -> bool:
    return all(gap(source(workspace), left, right, True) for left, right in DECLARATIONS)

@criterion
def members_separated(workspace: Path) -> bool:
    return all(gap(source(workspace), left, right, True) for left, right in MEMBERS)

@criterion
def independent_steps_separated(workspace: Path) -> bool:
    return all(gap(source(workspace), left, right, True) for left, right in STEPS)

@criterion
def related_statements_together(workspace: Path) -> bool:
    return all(gap(source(workspace), left, right, False) for left, right in RELATED)
