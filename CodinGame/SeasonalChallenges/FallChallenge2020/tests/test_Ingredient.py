import unittest

from main import Ingredient


class TestIngredient(unittest.TestCase):
    def test_Ingredient_tier(self):
        val = 1

        self.assertEqual(Ingredient(val).tier, val)
        self.assertEqual(Ingredient.tier_0().tier, 0)
        self.assertEqual(Ingredient.tier_1().tier, 1)
        self.assertEqual(Ingredient.tier_2().tier, 2)
        self.assertEqual(Ingredient.tier_3().tier, 3)

        self.assertEqual(Ingredient.tier_0(), Ingredient.tier_0())

    def test_Ingredient_from_multiple_returns_list(self):
        self.assertIsInstance(Ingredient.from_multiple(0, 0), list)

    def _Ingredient_from_multiple_values(self, tier, amount):
        ingredients = Ingredient.from_multiple(tier, amount)
        self.assertEqual(len(ingredients), amount)
        for ingredient in ingredients:
            self.assertIsInstance(ingredient, Ingredient)
            self.assertEqual(ingredient.tier, tier)

    def test_Ingredient_from_multiple_values(self):
        testcases = (
            (0, 0), (1, 0), (0, 1), (1, 100)
        )
        for testcase in testcases:
            self._Ingredient_from_multiple_values(*testcase)
