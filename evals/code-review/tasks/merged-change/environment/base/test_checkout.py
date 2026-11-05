import unittest
from checkout import total


class Tests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total([100, 250]), 350)
