import unittest
from app import display_name

class Tests(unittest.TestCase):
    def test_trim(self):
        self.assertEqual(display_name(" A "), "A")
