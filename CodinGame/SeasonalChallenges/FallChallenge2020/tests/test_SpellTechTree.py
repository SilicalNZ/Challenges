import unittest
from pprint import pprint


from main import Spell, SpellTechTree


class TestSpellTechTree(unittest.TestCase):
    def test_SpellTechTree_find(self):
        combinations = (
            (2, 0, 0, 0),
            (-1, 1, 0, 0),
            (0, -1, 1, 0),
            (0, 0, -1, 1),
            (0, 0, 2, 0),
            (3, 0, 0, 0),

            (0, 1, 0, 0),
            (0, 2, -2, 3),
            (0, -3, 3, 0),
            (1, 1, -1, 1)
        )

        product = (0, 0, 0, -5)

        spells = []
        for combination in combinations:
            spell = Spell.from_input(*combination, None, None)
            spells.append(spell)

        tech = SpellTechTree(Spell.from_input(*product, None, None), *spells)
        tech.find()

    def test_SpellTechTree_find_recursive(self):
        # Make sure this doesn't get stuck in a recursive loop

        combinations = (
            (1, -1, 0, 0),
            (-1, 1, 0, 0),
        )

        product = (0, 0, 0, -5)

        spells = []
        for combination in combinations:
            spell = Spell.from_input(*combination, None, None)
            spells.append(spell)

        tech = SpellTechTree(Spell.from_input(*product, None, None), *spells)
        tech.find()

    def test_SpellTechTree_path(self):
        combinations = (
            (2, 0, 0, 0),
            (-1, 1, 0, 0),
            (0, -1, 1, 0),
            (0, 0, -1, 1),
            (0, 0, 2, 0),
            (3, 0, 0, 0),

            (0, 1, 0, 0),
            (0, 2, -2, 3),
            (0, -3, 3, 0),
            (1, 1, -1, 1)
        )

        product = (0, 0, 0, -5)

        spells = []
        for combination in combinations:
            spell = Spell.from_input(*combination, None, None)
            spells.append(spell)

        tech = SpellTechTree(Spell.from_input(*product, None, None), *spells)
        pprint(tech.path())