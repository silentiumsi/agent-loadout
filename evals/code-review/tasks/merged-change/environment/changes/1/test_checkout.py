import unittest
from checkout import apply_discount, price_with_coupon, total


class Tests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total([100, 250]), 350)

    def test_discount(self):
        self.assertEqual(apply_discount(200, 10), 180)

    def test_coupon(self):
        self.assertEqual(price_with_coupon(200, "SAVE10"), 180)
