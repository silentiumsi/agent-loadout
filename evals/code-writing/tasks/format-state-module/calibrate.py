"""Check the observed failure, reference, alternatives, and boundary near misses."""
import importlib.util
import shutil
import sys
import tempfile
import types
from pathlib import Path

stub = types.ModuleType("rewardkit")
stub.criterion = lambda fn: fn
sys.modules["rewardkit"] = stub
root = Path(__file__).parent
spec = importlib.util.spec_from_file_location("checks", root / "tests/checks.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)
names = [
    "syntax_preserved", "other_files_preserved", "declarations_separated",
    "members_separated", "independent_steps_separated", "related_statements_together",
]

with tempfile.TemporaryDirectory() as directory:
    workspace = Path(directory)
    shutil.copytree(root / "environment/project", workspace / "project")
    target = workspace / "project/state.ts"
    observed = {name: getattr(checks, name)(workspace) for name in names}
    assert observed == dict(zip(names, [True, True, False, False, False, True])), observed
    print("Observed fixture:", observed)

    reference = (root / "solution/reference/state.ts").read_text()
    for valid in [reference, reference.replace("  ", "\t"), reference.replace("\n", "\r\n")]:
        target.write_text(valid)
        assert all(getattr(checks, name)(workspace) for name in names)

    groups = [
        (checks.DECLARATIONS, "declarations_separated", True),
        (checks.MEMBERS, "members_separated", True),
        (checks.STEPS, "independent_steps_separated", True),
        (checks.RELATED, "related_statements_together", False),
    ]
    # Mutate each boundary independently; no untested conjunctions can mask a miss.
    for pairs, criterion, separated in groups:
        for left, right in pairs:
            for count in ([1, 3] if separated else [2]):
                import re
                pattern = r"\s*".join(re.escape(t) for t in checks.tokens(left))
                pattern += r"([ \t]*\n(?:[ \t]*\n)*[ \t]*)"
                pattern += r"\s*".join(re.escape(t) for t in checks.tokens(right))
                found = re.search(pattern, reference)
                assert found, (left, right)
                start, end = found.span(1)
                target.write_text(reference[:start] + "\n" * count + reference[end:])
                assert not getattr(checks, criterion)(workspace), (criterion, left, count)

    target.write_text(reference.replace("generation: 0", "generation: 9"))
    assert not checks.syntax_preserved(workspace)
    target.write_text(reference)
    (target.parent / "extra.ts").write_text("extra")
    assert not checks.other_files_preserved(workspace)
print("PASS: reference, indentation/line-ending alternatives, every boundary mutation, preservation")
