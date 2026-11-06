"""Score actual CLI behavior, shared policy propagation, and submitted tests."""

import ast
import csv
import hashlib
import io
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from rewardkit import criterion

TESTS = Path(__file__).parent


def run(command, project):
    result = subprocess.run(command, cwd=project, text=True, capture_output=True, timeout=45)
    return result.returncode, result.stdout + result.stderr


def behavior(project, group):
    return run([sys.executable, str(TESTS / "behavior.py"), str(project), group], project)[0] == 0


@criterion
def compatibility(workspace: Path) -> bool:
    return behavior(workspace, "Compatibility")


@criterion
def selected_exports(workspace: Path) -> bool:
    return behavior(workspace, "Selection")


@criterion
def boundary_errors(workspace: Path) -> bool:
    return behavior(workspace, "Boundary")


@criterion
def shared_policy(workspace: Path) -> bool:
    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "project"
        shutil.copytree(workspace, project, ignore=shutil.ignore_patterns(".git", "__pycache__", ".scratch"))
        fields = project / "orders/fields.py"
        with fields.open("a") as stream:
            stream.write('\nALIASES["buyer"] = "email"\n')

        result = subprocess.run([sys.executable, "-m", "orders.export", "orders.json", "--columns", "buyer,id"], cwd=project, capture_output=True, text=True, timeout=10)
        return result.returncode == 0 and list(csv.reader(io.StringIO(result.stdout))) == [
            ["email", "id"], ["ada@example.test", "O1"],
        ]


def replace_main(source, body):
    tree = ast.parse(source)
    function = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "main")
    lines = source.splitlines(keepends=True)
    return "".join(lines[:function.lineno - 1]) + body + "\n" + "".join(lines[function.end_lineno:])


EQUIVALENT_MAIN = '''def main():
    import argparse
    import csv
    import json
    import sys
    from pathlib import Path
    from orders.fields import resolve_fields

    command = argparse.ArgumentParser()
    command.add_argument("input", type=Path)
    command.add_argument("--columns")
    options = command.parse_args()
    try:
        columns = resolve_fields(options.columns)
    except ValueError as error:
        command.error(str(error))

    records = json.loads(options.input.read_text())
    output = csv.DictWriter(sys.stdout, fieldnames=columns, extrasaction="ignore")
    output.writeheader()
    output.writerows(records)
'''


@criterion
def behavioral_regression_tests(workspace: Path) -> bool:
    command = [sys.executable, "-m", "unittest", "discover", "-s", "tests"]
    if run(command, workspace)[0] != 0:
        return False

    with tempfile.TemporaryDirectory() as directory:
        project = Path(directory) / "project"
        shutil.copytree(workspace, project, ignore=shutil.ignore_patterns(".git", "__pycache__", ".scratch"))
        exporter = project / "orders/export.py"
        original = exporter.read_text()
        variants = [
            (EQUIVALENT_MAIN, True),
            (EQUIVALENT_MAIN.replace('columns = resolve_fields(options.columns)', 'columns = tuple(reversed(resolve_fields(options.columns)))'), False),
            (EQUIVALENT_MAIN.replace('columns = resolve_fields(options.columns)', 'columns = resolve_fields(None)'), False),
        ]
        for body, should_pass in variants:
            exporter.write_text(replace_main(original, body))
            shutil.rmtree(project / "orders/__pycache__", ignore_errors=True)
            passed = run(command, project)[0] == 0
            if passed != should_pass:
                return False

    return True


@criterion
def fixture_integrity(workspace: Path) -> bool:
    expected = json.loads((TESTS / "preserved.json").read_text())
    return all(
        (workspace / name).is_file()
        and hashlib.sha256((workspace / name).read_bytes()).hexdigest() == digest
        for name, digest in expected.items()
    )
