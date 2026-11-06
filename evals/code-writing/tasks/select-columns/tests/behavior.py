"""Trusted end-to-end tests; all expected values come from the task contract."""

import csv
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(sys.argv.pop(1)).resolve()


def invoke(selection=None, rows=None, module="orders.export", missing=False):
    with tempfile.TemporaryDirectory() as directory:
        data = Path(directory) / "input.json"
        if not missing:
            data.write_text(json.dumps(rows if rows is not None else [
                {"id": "Z9", "email": "zoe@example.test", "total": 321, "note": 'Hi, "Zoe"\nDoor 2'},
                {"id": "A2", "email": "ann@example.test", "total": 0},
            ]))

        args = [sys.executable, "-m", module, str(data)]
        if selection is not None:
            args += ["--columns" if module == "orders.export" else "--fields", selection]

        return subprocess.run(args, cwd=ROOT, text=True, capture_output=True, timeout=10)


def csv_rows(result):
    if result.returncode:
        raise AssertionError(result.stderr)

    return list(csv.reader(io.StringIO(result.stdout)))


class Compatibility(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(csv_rows(invoke()), [
            ["id", "email", "total", "note"],
            ["Z9", "zoe@example.test", "321", 'Hi, "Zoe"\nDoor 2'],
            ["A2", "ann@example.test", "0", ""],
        ])
        self.assertEqual(csv_rows(invoke(rows=[])), [["id", "email", "total", "note"]])

    def test_existing_suite(self):
        result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_existing.py"], cwd=ROOT, capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_table(self):
        result = invoke(' CUSTOMER ,email,"Delivery, note",order', module="orders.table")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout), [
            ["zoe@example.test", 'Hi, "Zoe"\nDoor 2', "Z9"], ["ann@example.test", "", "A2"],
        ])


class Selection(unittest.TestCase):
    def test_selected_order(self):
        self.assertEqual(csv_rows(invoke("total,id")), [["total", "id"], ["321", "Z9"], ["0", "A2"]])

    def test_aliases_quotes_and_deduplication(self):
        self.assertEqual(csv_rows(invoke(' CUSTOMER ,email,"Delivery, note",order,ID')), [
            ["email", "note", "id"], ["zoe@example.test", 'Hi, "Zoe"\nDoor 2', "Z9"], ["ann@example.test", "", "A2"],
        ])

    def test_empty_input_and_single_field(self):
        self.assertEqual(csv_rows(invoke("amount", rows=[])), [["total"]])
        self.assertEqual(csv_rows(invoke("id")), [["id"], ["Z9"], ["A2"]])


class Boundary(unittest.TestCase):
    def test_invalid_before_input_io(self):
        for selection in ("", " ", ",", "id,", ",id", "id,,email", "secret", '"id', '"id"x', "id\nemail", "id\n\n", "\n"):
            with self.subTest(selection=selection):
                result = invoke(selection, missing=True)
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
                self.assertNotIn("unrecognized arguments", result.stderr)
                self.assertNotIn("No such file", result.stderr)


if __name__ == "__main__":
    unittest.main()
