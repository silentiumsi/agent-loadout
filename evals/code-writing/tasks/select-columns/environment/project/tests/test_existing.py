import csv
import io
import unittest

from orders.export import render_csv
from orders.fields import resolve_fields


class ExistingTests(unittest.TestCase):
    def test_default_export(self):
        rows = [{"id": "O1", "email": "a@example.test", "total": 120, "note": 'hello, "Sam"'}]
        self.assertEqual(list(csv.reader(io.StringIO(render_csv(rows)))), [
            ["id", "email", "total", "note"], ["O1", "a@example.test", "120", 'hello, "Sam"'],
        ])

    def test_empty_export(self):
        self.assertEqual(list(csv.reader(io.StringIO(render_csv([])))), [["id", "email", "total", "note"]])

    def test_table_field_policy(self):
        self.assertEqual(resolve_fields(' CUSTOMER ,email,"Delivery, note",order'), ("email", "note", "id"))
