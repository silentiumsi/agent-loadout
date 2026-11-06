"""Requires Node and TypeScript 5.9.3 resolvable through NODE_PATH."""
import json
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).parent
RUNNER = ROOT / "tests/inspect.cjs"
LAYOUT = ["declarations_separated", "members_separated"]
BEHAVIOR = ["pagination_and_navigation", "failure_and_retry", "overlapping_refresh",
            "workspace_isolation", "pending_more_is_noop"]


def inspect(text):
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "state.ts"
        target.write_text(text)
        result = subprocess.run(
            ["node", str(RUNNER), str(target)],
            text=True, capture_output=True, timeout=45, check=True,
        )
        return json.loads(result.stdout)


reference = (ROOT / "solution/reference/state.ts").read_text()
original = (ROOT / "environment/project/state.ts").read_text()
result = inspect(original)
assert result["types_valid"]
assert not any(result[name] for name in LAYOUT)
assert not all(result[name] for name in BEHAVIOR)

# A second valid design merges refresh/pagination execution in one public method.
header = reference[:reference.index("  async loadList")]
alternative = header + '''  async loadList(more = false): Promise<void> {
    const state = this.current;
    if (!state) return;
    if (more && (state.list.pending || state.list.data?.cursor == null)) return;

    const target = state.list;
    const cursor = more ? target.data!.cursor : null;
    const generation = ++target.generation;
    target.pending = true;

    try {
      const next = await this.fetchPage(state.key, cursor);
      if (target.generation !== generation) return;

      target.data = more ? mergePage(target.data, next) : next;
    } finally {
      if (target.generation === generation) target.pending = false;
    }
  }

  loadMore(): Promise<void> {
    return this.loadList(true);
  }
}
'''
for valid in [reference, alternative, reference.replace("loadPage", "requestPage"),
              reference.replace("\n", "\r\n"),
              reference.replace("export interface Entry", "/** Catalog entry. */\nexport interface Entry")]:
    result = inspect(valid)
    assert all(result.get(name) for name in ["types_valid", "public_types_preserved", *LAYOUT, *BEHAVIOR]), result

compact = inspect(reference.replace("\n\n", "\n"))
assert all(compact[name] for name in ["types_valid", *BEHAVIOR])
assert not any(compact[name] for name in LAYOUT)

for old, new, criterion in [
    ("}\n\nexport interface Entry", "}\nexport interface Entry", "declarations_separated"),
    ("  }\n\n  cached()", "  }\n  cached()", "members_separated"),
    ("state.list.data.cursor, true", "null, true", "pagination_and_navigation"),
    ("return { ...next, items: [...items.values()] };",
     "return { ...next, items: [...(previous?.items ?? []), ...next.items] };", "pagination_and_navigation"),
    ("      if (target.generation !== generation) return;\n", "", "overlapping_refresh"),
    ("if (target.generation === generation) target.pending = false;",
     "target.pending = false;", "overlapping_refresh"),
    ("target.data = more ? mergePage(target.data, next) : next;",
     "this.current!.list.data = more ? mergePage(target.data, next) : next;", "workspace_isolation"),
    ("    state.selected = id;", "    state.selected = null;", "pagination_and_navigation"),
    ("    target.pending = true;", "    target.pending = true;\n    target.data = undefined;", "failure_and_retry"),
]:
    assert old in reference
    result = inspect(reference.replace(old, new))
    assert result.get("types_valid"), result
    assert not result[criterion], (criterion, result)

missing_export = inspect(reference.replace("export interface Entry", "interface Entry"))
assert missing_export["types_valid"] and not missing_export["public_types_preserved"]
empty_cursor_bug = inspect(reference.replace("state.list.data?.cursor == null", "!state.list.data?.cursor"))
assert empty_cursor_bug["types_valid"] and not empty_cursor_bug["pagination_and_navigation"]

invalid = inspect(reference.replace("items: T[]", "items: MissingType[]"))
assert not invalid["types_valid"]
print("PASS: observed failure, two designs, renamed helper, CRLF/JSDoc, compact code, layout and behavior mutants, invalid types")
