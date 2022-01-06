import unittest

from tests.testcases import combinations
from main import Order


class TestOrder(unittest.TestCase):
    def test_Order_input(self):
        for testcase in combinations:
            result = Order.from_input(*testcase, None, None)
            self.assertEqual(len(result.ingredients), sum(testcase))