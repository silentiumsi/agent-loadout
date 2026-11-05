import unittest
from pager import paginate


class Tests(unittest.TestCase):
    def test_second_page_size(self):
        self.assertEqual(len(paginate(list(range(10)), 2, 3)), 3)
