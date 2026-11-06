import csv
import io
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ColumnTests(unittest.TestCase):
    def test_selected_export(self):
        result = subprocess.run([sys.executable, "-m", "orders.export", "orders.json", "--columns", "email,id"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(list(csv.reader(io.StringIO(result.stdout))), [["email", "id"], ["ada@example.test", "O1"]])

    def test_invalid_selection(self):
        for selection in ("", "id,", "unknown", '"id', "id\nemail"):
            with self.subTest(selection=selection):
                result = subprocess.run([sys.executable, "-m", "orders.export", "missing.json", "--columns", selection], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("error:", result.stderr)
                self.assertNotIn("Traceback", result.stderr)
