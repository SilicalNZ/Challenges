from __future__ import annotations

import sys
from typing import List, Optional, Tuple, Union
from functools import lru_cache


def separate_plus_minus(*args: int) -> Tuple[List[int], List[int]]:
    positive = []
    negative = []
    for i in args:
        if i > 0:
            positive.append(i)
            negative.append(0)
        elif i < 0:
            negative.append(abs(i))
            positive.append(0)
        elif i == 0:
            negative.append(0)
            positive.append(0)
    return negative, positive


class Ingredient:
    def __init__(self, tier):
        self.tier = tier

    @classmethod
    @lru_cache()
    def tier_0(cls):
        return Ingredient(0)

    @classmethod
    @lru_cache()
    def tier_1(cls):
        return Ingredient(1)

    @classmethod
    @lru_cache()
    def tier_2(cls):
        return Ingredient(2)

    @classmethod
    @lru_cache()
    def tier_3(cls):
        return Ingredient(3)

    @classmethod
    def from_multiple(cls, tier, amount):
        return [getattr(cls, f"tier_{tier}")() for _ in range(amount)]

    def __str__(self):
        return str(self.tier)

    def __repr__(self):
        return repr(self.tier)


class IngredientInventory:
    def __init__(self, ingredients: List[Ingredient]):
        self.ingredients = ingredients

    @classmethod
    def from_input(cls, inv_0: int, inv_1: int, inv_2: int, inv_3: int):
        ingredients = []
        for tier, amount in zip(range(4), (inv_0, inv_1, inv_2, inv_3)):
            ingredients.extend(Ingredient.from_multiple(tier, amount))

        return cls(ingredients)

    def count(self, ingredient: Ingredient):
        return self.ingredients.count(ingredient)

    def __contains__(self, ingredients: Union[IngredientInventory, Ingredient]):
        ingredients = (ingredients, ) if isinstance(ingredients, Ingredient) else ingredients

        copy_ingredients = self.ingredients[:]
        for i in ingredients:
            if i in copy_ingredients:
                copy_ingredients.remove(i)
            else:
                return False
        return bool(ingredients)

    def difference(self, ingredients: Union[IngredientInventory, Ingredient]):
        ingredients = (ingredients, ) if isinstance(ingredients, Ingredient) else ingredients

        for ingredient in ingredients:
            self.ingredients.remove(ingredient)

    def __iter__(self):
        yield from self.ingredients

    def __len__(self):
        return len(self.ingredients)

    def __str__(self):
        return str(self.ingredients)

    def __repr__(self):
        return repr(self.ingredients)

    def __bool__(self):
        return bool(self.ingredients)

    def copy(self):
        return self.__class__(self.ingredients[:])

class RequireIngredientInventory:
    def __init__(self, ingredients: IngredientInventory):
        self.ingredients = ingredients

    def __contains__(self, item):
        return self.ingredients.__contains__(item)

    def __iter__(self):
        return self.ingredients.__iter__()

    def __len__(self):
        return self.ingredients.__len__()

    def __str__(self):
        return self.ingredients.__str__()

    def __repr__(self):
        return self.ingredients.__repr__()


class Order(RequireIngredientInventory):
    def __init__(self, ingredients: IngredientInventory, id: int, price: int):
        self.id = id
        self.price = price
        super().__init__(ingredients)

    @classmethod
    def from_input(cls, delta_0: int, delta_1: int, delta_2: int, delta_3: int, id: int, price: int):
        return cls(
            IngredientInventory.from_input(
                delta_0, delta_1, delta_2, delta_3
            ),
            id,
            price
        )

    def brew(self):
        print(f"BREW {self.id}")


class Spell:
    def __init__(self, price: Optional[IngredientInventory], product: Optional[IngredientInventory], id, castable):
        self.id = id
        self.castable = castable
        self.price = price
        self.product = product

    @classmethod
    def from_input(cls, delta_0: int, delta_1: int, delta_2: int, delta_3: int, id: int, castable):
        items = []
        for neg_pos in separate_plus_minus(delta_0, delta_1, delta_2, delta_3):
            items.append(IngredientInventory.from_input(*neg_pos))

        return cls(items[0], items[1], id, castable)

    def __str__(self):
        return str((tuple(self.price), tuple(self.product)))

    def __repr__(self):
        return repr((tuple(self.price), tuple(self.product)))

    def cast(self):
        print(f"CAST {self.id}")


class SpellOptions:
    def __init__(self):
        self.items = []

    def append(self, value):
        self.items.append(value)

    def __iter__(self):
        yield from self.items[0]


class SpellSequence:
    def __init__(self, x, items):
        self.x = x
        self.items = items

    def __iter__(self):
        yield from self.items
        yield self.x


class SpellTechTree:
    def __init__(self, target: Spell, *spells: Spell):
        self.target = target
        self.spells = spells

    def find(self, parents=None, depth=0):
        all_results = [] if depth == 0 else SpellOptions()
        for ingredient in self.target.price:
            print(ingredient, file=sys.stderr)
            if parents is not None and ingredient in parents[:-1]:
                return all_results

            if parents is None:
                parents = (ingredient, )
            elif ingredient != parents[-1]:
                parents = (*parents, ingredient)

            results = SpellOptions()
            for spell in self.spells:
                if ingredient in spell.product:
                    if spell.price:
                        result = SpellSequence(spell, SpellTechTree(spell, *self.spells).find(parents, depth=depth+1))
                    else:
                        result = SpellSequence(spell, [])
                    results.append(result)
            all_results.append(results)
        return all_results

    def path(self):
        for i in self.find():
            yield from i


class Actions:
    def __init__(self, recipes: List[Order], spells: List[Spell]):
        self.recipes = recipes
        self.spells = spells

    @classmethod
    def from_input(cls):
        recipes = []
        spells = []
        action_count = int(input())  # the number of spells and recipes in play
        for i in range(action_count):
            action_id, action_type, \
            delta_0, delta_1, delta_2, delta_3, \
            price, tome_index, tax_count, \
            castable, repeatable = input().split()

            action_id = int(action_id)
            delta_0 = int(delta_0)
            delta_1 = int(delta_1)
            delta_2 = int(delta_2)
            delta_3 = int(delta_3)
            price = int(price)
            tome_index = int(tome_index)
            tax_count = int(tax_count)
            castable = castable != "0"
            repeatable = repeatable != "0"

            if not price:
                recipes.append(Order.from_input(abs(delta_0), abs(delta_1), abs(delta_2), abs(delta_3), action_id, price))
            else:
                spells.append(Spell.from_input(delta_0, delta_1, delta_2, delta_3, action_id, castable))

        return cls(recipes, spells)


class Player(RequireIngredientInventory):
    def __init__(self, ingredients: IngredientInventory, score: int):
        super().__init__(ingredients)
        self.score = score

    @classmethod
    def from_input(cls, inv_0: int, inv_1: int, inv_2: int, inv_3: int, score: int):
        return cls(
            IngredientInventory.from_input(
                inv_0, inv_1, inv_2, inv_3
            ),
            score
        )

    def wait(self):
        print("WAIT")


class Thinker:
    def __init__(self, player1: Player, player2: Player, actions: Actions):
        self.perspective = player1
        self.opponent = player2
        self.actions = actions

    @classmethod
    def from_input(cls):
        order = Actions.from_input()
        players = []
        for i in range(2):
            # inv_0: tier-0 ingredients in inventory
            # score: amount of rupees
            players.append(Player.from_input(*[int(j) for j in input().split()]))
        return cls(players[0], players[1], order)

    @classmethod
    def run(cls):
        while True:
            thinker = cls.from_input()
            thinker.brew_spells()

    def make_order(self):
        for recipe in sorted(self.actions.recipes, key=lambda x: x.price, reverse=True):
            if recipe in self.perspective:
                recipe.brew()
                return
        self.perspective.wait()

    def brew_spells(self):
        for recipe in self.actions.recipes[:1]:
            inventory = self.perspective.ingredients.copy()

            for spell in SpellTechTree(Spell(recipe.ingredients, None, None, None), *self.actions.spells).path():
                if spell.product in inventory:
                    inventory.difference(spell.product)
                    pass
                else:
                    spell.cast()


if __name__ == '__main__':
    Thinker.run()
