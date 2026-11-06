"""Validate deterministic formatting graders against positives and near misses."""
import importlib.util
import shutil
import sys
import tempfile
import types
from pathlib import Path

ROOT = Path(__file__).parent
stub = types.ModuleType("rewardkit")
stub.criterion = lambda fn: fn
sys.modules["rewardkit"] = stub

for case, filename in [("format-go", "run.go"), ("format-typescript", "handle.ts")]:
    task = ROOT / "tasks" / case
    spec = importlib.util.spec_from_file_location(case, task / "tests/checks.py")
    checks = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(checks)
    names = ["syntax_preserved", "other_files_preserved", "independent_steps_separated"]
    related = "immediate_error_check_kept_together" if case == "format-go" else "initialization_kept_with_assignment"
    names.append(related)
    with tempfile.TemporaryDirectory() as directory:
        workspace = Path(directory)
        shutil.copytree(task / "environment/project", workspace / "project")
        target = workspace / "project" / filename
        assert checks.syntax_preserved(workspace)
        assert not checks.independent_steps_separated(workspace)
        reference = (task / "solution/reference" / filename).read_text()
        target.write_text(reference)
        assert all(getattr(checks, name)(workspace) for name in names), case
        # Pure indentation changes are valid alternatives.
        target.write_text(reference.replace("\t", "    "))
        assert all(getattr(checks, name)(workspace) for name in names), case
        target.write_text(
            reference.replace("repoRoot(dir)", "repoRoot(\n        dir)")
            if case == "format-go"
            else reference.replace("x === y", "x  ===  y")
        )
        assert all(getattr(checks, name)(workspace) for name in names), case
        target.write_text(reference.replace("\n\n", "\n"))
        assert not checks.independent_steps_separated(workspace)
        target.write_text(reference.replace("\n\n", "\n\n\n"))
        assert not checks.independent_steps_separated(workspace)
        pair = "root, err := repoRoot(dir)\n" if case == "format-go" else "let someVariable = 0;\n"
        target.write_text(reference.replace(pair, pair + "\n"))
        assert not getattr(checks, related)(workspace)
        target.write_text(reference.replace("return 0", "return 9") if case == "format-go" else reference.replace("return someVariable", "return 9"))
        assert not checks.syntax_preserved(workspace)
        if case == "format-go":
            target.write_text(reference.replace('"revui:"', '"revui: "'))
            assert not checks.syntax_preserved(workspace)
        target.write_text(reference)
        (target.parent / "unrequested.txt").write_text("extra")
        assert not checks.other_files_preserved(workspace)
    print(f"PASS: {case}: reference, alternative indentation, and deliberate failures")
