import enum
import itertools

CARD_VALUE = 20


class Ingredient(enum.Enum):
    Leaf = 1
    Petal = 2
    Berries = 3
    Water = 4
    Poison = 5
    Crystal = 6
    Mushroom = 7
    Flame = 8
    Power = 9
    Lightning = 10
    Essence = 11
    Scale = 12
    Beetle = 13
    Spirit = 14
    Steel = 15
    Tooth = 16


Leaf = Ingredient.Leaf
Petal = Ingredient.Petal
Berries = Ingredient.Berries
Water = Ingredient.Water
Poison = Ingredient.Poison
Crystal = Ingredient.Crystal
Mushroom = Ingredient.Mushroom
Flame = Ingredient.Flame
Power = Ingredient.Power
Lightning = Ingredient.Lightning
Essence = Ingredient.Essence
Scale = Ingredient.Scale
Beetle = Ingredient.Beetle
Spirit = Ingredient.Spirit
Steel = Ingredient.Steel
Tooth = Ingredient.Tooth


BASE_INGREDIENTS = (Leaf, )
GENERIC_INGREDIENTS = (*BASE_INGREDIENTS, Petal, Berries)
IGNORE_INGREDIENTS = (Steel, Lightning)


class CannotCraftError(Exception):
    pass


RECIPE = tuple[Ingredient, Ingredient]


class Inventory:
    _recipes: dict[RECIPE: Ingredient] = {
        (Leaf, Leaf): Petal,
        (Petal, Petal): Berries,
        (Berries, Berries): Water,
        (Berries, Petal): Poison,
        (Water, Water): Crystal,
        (Berries, Water): Mushroom,
        (Poison, Poison): Flame,
        (Mushroom, Mushroom): Power,
        (Mushroom, Berries): Lightning,
        (Crystal, Petal): Essence,
        (Flame, Flame): Scale,
        (Flame, Poison): Beetle,
        (Power, Mushroom): Spirit,
        (Lightning, Lightning): Steel,
        (Beetle, Beetle): Tooth,
    }

    _inverse_recipes: dict[Ingredient: RECIPE] = {b: a for a, b in _recipes.items()}

    _dust_recipes: dict[RECIPE, int] = {
        (Leaf, Flame): 206,
        (Petal, Scale): 436,
        (Berries, Flame): 253,
        (Water, Scale): 530,
        (Poison, Scale): 499,
        (Flame, Essence): 488,
        (Flame, Scale): 596,
        (Essence, Scale): 702,
        (Scale, Beetle): 702,
        (Scale, Tooth): 1020,
    }

    _wild_cards: dict[RECIPE, int] = {
        (Berries, Spirit): 33 * CARD_VALUE,
        (Mushroom, Spirit): 40 * CARD_VALUE,
        (Power, Spirit): 50 * CARD_VALUE,
        (Lightning, Spirit): 43 * CARD_VALUE,
        (Essence, Spirit): 45 * CARD_VALUE,
    }

    _dust = {**_dust_recipes, **_wild_cards}
    _craft_history: dict[RECIPE, int] = {key: 0 for key in itertools.chain(_recipes.keys(), _dust.keys())}
    _dust_total = 0

    def __init__(self, available_ingredients: dict[Ingredient, int]):
        self._ingredients: dict[Ingredient, int] = available_ingredients
        self._backup: None | 'Inventory' = None

    def has(self, ingredient: Ingredient, amount: int) -> bool:
        return self._ingredients[ingredient] >= amount

    def _append_craft_history(self, recipe: RECIPE):
        self._craft_history[recipe] += 1

    def print_ingredients(self):
        [print(key.name, value) for key, value in self._ingredients.items()]

    def print_craft_history(self):
        [print(key[0].name, key[1].name, value) for key, value in self._craft_history.items() if value != 0]

    def show_craft_history(self) -> str:
        lines = []
        for key, value in self._craft_history.items():
            if value == 0:
                continue

            result = self._dust_recipes.get(key)
            if result:
                result = f"{result} dust"

            if not result:
                result = self._recipes.get(key)
                if result:
                    result = f"{result.name}"

            if not result:
                result = self._wild_cards.get(key)
                if result:
                    result = f"{result // CARD_VALUE} wild cards"


            lines.append(f"{value:3} x ({key[0].name:10s} + {key[1].name:10s}) = {result:15s} x {value:3}")

        lines.append(f"Total Dust: {self._dust_total}")
        return "\n".join(lines)

    def _craft(self, recipe: RECIPE):
        constituent_a, constituent_b = recipe

        if not self.has(constituent_a, 1):
            self.make_ingredient(constituent_a)
        if not self.has(constituent_b, 1):
            self.make_ingredient(constituent_b)
        # Repeat this again, since the constituent_a may have been used in constituent_b
        if not self.has(constituent_a, 1):
            self.make_ingredient(constituent_a)
        if constituent_a == constituent_b and not self.has(constituent_a, 2):
            self.make_ingredient(constituent_a)

        self._ingredients[constituent_a] -= 1
        self._ingredients[constituent_b] -= 1

        self._append_craft_history(recipe)

    def make_ingredient(self, ingredient: Ingredient):
        if ingredient in BASE_INGREDIENTS:
            raise CannotCraftError("Ran out of Base Ingredients, cannot craft more")

        self._craft(self._inverse_recipes[ingredient])

        self._ingredients[ingredient] += 1

    def make_dust(self, recipe: RECIPE):
        if recipe not in self._dust:
            raise CannotCraftError("Recipe does not exist")

        self._craft(recipe)

        self._dust_total += self._dust[recipe]

    def make_dust_optimally(self, recipes: tuple[RECIPE, ...]):
        recipes = (*reversed(recipes[1:]), *recipes)

        self._save()

        for x, recipe in enumerate(recipes, 1):
            try:
                self.make_dust(recipe)
            except CannotCraftError as e:
                self.rollback()
                raise e

            if x == len(recipes) or self._compare_ingredients():
                break

            self.rollback()

    def iterate_make_dust_optimally(self, priority_recipes: tuple[RECIPE, ...]):
        for _ in range(100):
            try:
                self.make_dust_optimally(priority_recipes)
            except CannotCraftError:
                break

        for _ in range(2):
            for recipe, _ in sorted(self._dust.items(), key=lambda x: x[1], reverse=True):
                self._save()
                try:
                    self.make_dust(recipe)
                except CannotCraftError:
                    self.rollback()
                else:
                    break

    def _compare_ingredients(self) -> bool:
        for before, after in zip(reversed(self._backup._ingredients.items()), reversed(self._ingredients.items())):
            if before[0] in IGNORE_INGREDIENTS or before[0] in GENERIC_INGREDIENTS:
                continue

            # Checks if an ingredient that should've been used, was used
            if before[1] > 0:
                if after[1] < before[1]:
                    return True
                return False
        return False

    def _save(self) -> 'Inventory':
        self._backup = Inventory(
            self._ingredients.copy()
        )

        self._backup._craft_history = self._craft_history.copy()
        self._backup._dust_total = self._dust_total

    def rollback(self):
        self._ingredients = self._backup._ingredients.copy()
        self._craft_history = self._backup._craft_history.copy()
        self._dust_total = self._backup._dust_total


if __name__ == "__main__":
    inventory = Inventory({
        Leaf: 26,
        Petal: 22,
        Berries: 21,
        Water: 7,
        Poison: 15,
        Crystal: 6,
        Mushroom: 7,
        Flame: 4,
        Power: 0,
        Lightning: 2,
        Essence: 1,
        Scale: 2,
        Beetle: 0,
        Spirit: 1,
        Steel: 2,
        Tooth: 1,
    })


    print("# Ingredients")
    inventory.print_ingredients()
    print()

    inventory.iterate_make_dust_optimally(((Lightning, Spirit), (Essence, Spirit), (Scale, Tooth)))
    print("Dust", inventory._dust_total)
    print("# Recipes")
    inventory.print_craft_history()
    print()

    print("# Leftover Ingredients")
    print(inventory.show_craft_history())
