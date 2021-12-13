from __future__ import annotations

from typing import Tuple


data = ""
z, v = data.split("\n\n")
only_first = False


def disrupt(coordinates: Tuple[Tuple[int, int]], fold_along_y: bool, fold_line: int):
    results = set()
    for x, y in coordinates:
        if fold_along_y and y > fold_line:
            y = fold_line - (y - fold_line)
        elif not fold_along_y and x > fold_line:
            x = fold_line - (x - fold_line)

        if x < 0 or y < 0:
            continue

        results.add((x, y))
    return tuple(results)


coordinates = tuple(tuple(map(int, i.split(","))) for i in z.split("\n"))

if only_first:
    v = v.split("\n")[:1]

for i in v:
    fold_along, fold_line = i.split(" ")[2].split("=")
    coordinates = disrupt(coordinates, fold_along == "y", int(fold_line))

width = max(tuple(zip(*coordinates))[0])
height = max(tuple(zip(*coordinates))[1])
grid = [[0 for _ in range(width + 1)] for _ in range(height + 1)]

for x, y in coordinates:
    grid[y][x] = 1

for i in grid:
    result = []
    for j in i:
        if j >= 1:
            result.append("▩")
        else:
            result.append(" ")
    print("".join(result))
