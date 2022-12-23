import enum


class Ingredients(enum.Enum):
    Leaf = 1
    Sand = 2
    Water = 3
    Lightning = 4
    Poison = 5
    Beetle = 6
    Tooth = 7
    Flame = 8
    Steel = 9
    Scale = 10
    Essence = 11
    Power = 12
    Shadow = 13
    Spirit = 14



Leaf = Ingredients.Leaf
Sand = Ingredients.Sand
Water = Ingredients.Water
Lightning = Ingredients.Lightning
Poison = Ingredients.Poison
Beetle = Ingredients.Beetle
Tooth = Ingredients.Tooth
Flame = Ingredients.Flame
Steel = Ingredients.Steel
Scale = Ingredients.Scale
Essence = Ingredients.Essence
Power = Ingredients.Power
Shadow = Ingredients.Shadow
Spirit = Ingredients.Spirit


ingredients = {
    Leaf: 48,
    Sand: 55,
    Water: 30,
    Lightning: 23,
    Poison: 10,
    Beetle: 15,
    Tooth: 6,
    Flame: 9,
    Steel: 9,
    Scale: 6,
    Essence: 2,
    Power: 3,
    Spirit: 4,
    Shadow: 1,
}

recipes = {
    (Leaf, Sand): Water,
    (Leaf, Water): Lightning,
    (Leaf, Lightning): Beetle,
    (Leaf, Power): Spirit,
    (Sand, Lightning): Poison,
    (Sand, Essence): Shadow,
    (Water, Beetle): Tooth,
    (Lightning, Poison): Flame,
    (Lightning, Beetle): Steel,
    (Tooth, Flame): Scale,
    (Tooth, Steel): Essence,
    (Flame, Steel): Power,
}

recipes = {**recipes, **{(key[1], key[0]): value for key, value in recipes.items()}}

c_cost = 20

dust = {
    (Leaf, Poison): 16 * c_cost,
    (Leaf, Flame): 430,
    (Leaf, Scale): 820,
    (Leaf, Shadow): 47 * c_cost,
    (Sand, Shadow): 47 * c_cost,
    (Water, Poison): 19 * c_cost,
    (Water, Shadow): 49 * c_cost,
    (Lightning, Shadow): 52 * c_cost,
    (Poison, Flame): 590,
    (Poison, Steel): 40 * c_cost,
    (Poison, Scale): 980,
    (Poison, Shadow): 68 * c_cost,
    (Beetle, Flame): 590,
    (Beetle, Scale): 980,
    (Flame, Essence): 1170,
    (Flame, Shadow): 1270,
    (Steel, Scale): 1210,
    (Steel, Shadow): 66 * c_cost,
    (Scale, Essence): 1210,
    (Scale, Shadow): 1660,
}

crafts = {key: 0 for key in recipes.keys()}


def craft(key):
    value = recipes[key]
    a, b = key

    if ingredients[a] < 1 or ingredients[b] < 1:
        return

    ingredients[a] -= 1
    ingredients[b] -= 1
    ingredients[value] += 1
    crafts[key] += 1


def exhaust():
    result = 0

    for key, value in reversed(dust.items()):
        a, b = key

        c, d = ingredients[a], ingredients[b]

        if c <= 0 or d <= 0:
            continue

        ingredients[a] -= 1
        ingredients[b] -= 1

        result += value

    return result


def shadow(ingredient_a, ingredient_b):
    def constituents(ingredient, depth=0, result=None):
        if result is None:
            result = {}

        for key, value in recipes.items():
            if value != ingredient:
                continue

            result[key] = value
            print("     " * 4 * depth, key)

            if key[0] not in (Sand, Leaf):
                constituents(key[0], depth+1, result)

            if key[1] not in (Sand, Leaf):
                constituents(key[1], depth+1, result)

            break

        return result

    def build_ingredient(constituents, ingredient):
        counter = 0
        while ingredients[ingredient] == 0 and counter <= 40:
            counter += 1

            for key, value in constituents.items():
                if ingredients[value] > 0:
                    continue

                craft(key)


    constituent_a = constituents(ingredient_a)
    constituent_b = constituents(ingredient_b)
    result = 0
    for i in range(1000):
        build_ingredient(constituent_a, ingredient_a)
        build_ingredient(constituent_b, ingredient_b)

        c, d = ingredients[ingredient_a], ingredients[ingredient_b]

        if c <= 0 or d <= 0:
            break

        ingredients[ingredient_a] -= 1
        ingredients[ingredient_b] -= 1

        result += dust.get((ingredient_b, ingredient_a), dust.get((ingredient_a, ingredient_b)))

    return result


print(shadow(Shadow, Scale))
[print(key[0].name, key[1].name, value) for key, value in crafts.items() if value != 0]

exit()


for key, value in dust.items():
    new = ingredients.copy()

    result = 0
    result += shadow(*key)
    result += exhaust()
    print(key[0].name, "+", key[1].name, "=", result)

    ingredients = new
