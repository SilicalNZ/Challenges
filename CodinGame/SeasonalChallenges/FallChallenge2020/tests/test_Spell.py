import unittest

from tests.testcases import combinations
from main import Spell, Ingredient, separate_plus_minus


class TestSpell(unittest.TestCase):
    def test_Spell_input(self):
        more_combinations = (
            *combinations,
            (-3, 0, 1, 0),
            (-1, -1, 1, 1)
        )

        for testcase in more_combinations:
            result_testcase = separate_plus_minus(*testcase)

            result = Spell.from_input(*testcase, None, None)
            self.assertEqual(len(result.price), sum(result_testcase[0]))
            self.assertEqual(len(result.product), sum(result_testcase[1]))
