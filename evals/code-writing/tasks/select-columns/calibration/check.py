"""Self-check verifier positives and deliberate failures without Docker or judges."""

import importlib.util
import shutil
import sys
import tempfile
import types
from pathlib import Path

TASK = Path(__file__).resolve().parents[1]
stub = types.ModuleType("rewardkit")
stub.criterion = lambda function: function
sys.modules["rewardkit"] = stub
spec = importlib.util.spec_from_file_location("checks", TASK / "tests/checks.py")
checks = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checks)


def evaluate(project):
    names = ("compatibility", "selected_exports", "boundary_errors", "shared_policy", "behavioral_regression_tests", "fixture_integrity")
    return {name: bool(getattr(checks, name)(project)) for name in names}


def main():
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "project"
        shutil.copytree(TASK / "environment/project", project, ignore=shutil.ignore_patterns("__pycache__"))
        initial = evaluate(project)
        assert initial == dict(compatibility=True, selected_exports=False, boundary_errors=False, shared_policy=False, behavioral_regression_tests=False, fixture_integrity=True), initial

        shutil.copy(TASK / "solution/export.py", project / "orders/export.py")
        shutil.copy(TASK / "solution/test_columns.py", project / "tests/test_columns.py")
        reference = evaluate(project)
        assert all(reference.values()), reference

        exporter = project / "orders/export.py"
        original = exporter.read_text()
        exporter.write_text(original.replace("fields = resolve_fields(args.columns)", "fields = tuple(reversed(resolve_fields(args.columns)))"))
        assert not checks.selected_exports(project)

        exporter.write_text(original.replace("fields = resolve_fields(args.columns)", "fields = resolve_fields(None)"))
        assert not checks.boundary_errors(project)

        exporter.write_text(original)
        fields = project / "orders/fields.py"
        fields.write_text(fields.read_text() + "\nALIASES.clear()\n")
        existing = project / "tests/test_existing.py"
        existing.write_text("")
        assert not checks.fixture_integrity(project)
        assert not checks.shared_policy(project)

    print("PASS: original fails new requirements; reference passes all six; deliberate failures detected")


if __name__ == "__main__":
    main()
