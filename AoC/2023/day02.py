data = """"""


limit = {"red": 12, "green": 13, "blue": 14}

possible_games = []

for x, line in enumerate(data.split("\n"), 1):
    possible = True
    for group in line.split(": ")[-1].split("; "):
        possible = True
        for value in group.split(", "):
            number, colour = value.split(" ")
            number = int(number)

            if colour not in limit or not (int(number) <= limit[colour]):
                possible = False
                break
        if not possible:
            break

    if possible:
        possible_games.append(x)

print(sum(possible_games))

import math

res = 0

for line in data.split("\n"):
    smallest = {}

    for group in line.split(": ")[-1].split("; "):
        for value in group.split(", "):
            number, colour = value.split(" ")
            number = int(number)

            if colour not in smallest:
                smallest[colour] = number
            elif smallest[colour] < number:
                smallest[colour] = number

    res += math.prod(smallest.values())

print(res)
