import unittest
from pager import paginate


class Tests(unittest.TestCase):
    def test_first(self):
        self.assertEqual(paginate(list(range(10)), 1, 3), [0, 1, 2])
