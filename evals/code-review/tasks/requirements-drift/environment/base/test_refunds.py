import unittest
from datetime import datetime
from refunds import RefundError, refund

NOW = datetime(2026, 1, 20)


class Tests(unittest.TestCase):
    def test_partial(self):
        order = {"captured": 100, "refunded": 0, "captured_at": datetime(2026, 1, 15)}
        self.assertEqual(refund(order, 40, NOW), 40)

    def test_cap(self):
        order = {"captured": 100, "refunded": 80, "captured_at": datetime(2026, 1, 15)}
        with self.assertRaises(RefundError):
            refund(order, 30, NOW)
