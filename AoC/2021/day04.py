from __future__ import annotations

from typing import Tuple
import pprint

data = ""


def positions_between_points(point0, point1) :
    x0, y0 = point0
    x1, y1 = point1
    if point0 == point1:
        yield point0
        return

    print(point0, point1)

    if x0 == x1:
        for i in range(min(y0, y1), max(y0, y1) + 1):
            yield x0, i
    elif y0 == y1:
        for i in range(min(x0, x1), max(x0, x1) + 1):
            yield i, y0
    else:
        x_negative, y_negative = -1 if x1 - x0 < 0 else 1, -1 if y1 - y0 < 0 else 1
        print(*zip(*(range(x0, x1 + x_negative, x_negative), range(y0, y1 + y_negative, y_negative))))
        yield from zip(*(range(x0, x1 + x_negative, x_negative), range(y0, y1 + y_negative, y_negative)))



class Grid:
    def __init__(self, x, y):
        self.grid = [[0 for _ in range(x)] for _ in range(y)]

    def increment_coordinate(self, x, y):
        self.grid[y][x] += 1

    def points_greater_than_2(self) -> int:
        result = 0
        for y in self.grid:
            for x in y:
                if x >= 2:
                    result += 1
        return result

    def __str__(self):
        return pprint.pformat(self.grid)

    __repr__ = __str__

    def save(self):
        with open("./output.txt", "w") as fp:
            fp.write(str(self.grid))


class Vent:
    def __init__(self, x0, y0, x1, y1):
        self.x0 = x0
        self.y0 = y0

        self.x1 = x1
        self.y1 = y1

    @property
    def pos0(self):
        return self.x0, self.y0

    @property
    def pos1(self):
        return self.x1, self.y1

    @property
    def is_diagonal(self) -> bool:
        return not (self.x0 == self.x1 or self.y0 == self.y1)

    def apply_to_grid(self, grid: Grid):
        for position in positions_between_points(self.pos0, self.pos1):
            grid.increment_coordinate(*position)

    def __str__(self):
        return f"({self.x0}, {self.y0}, {self.x1}, {self.y1})"

    __repr__ = __str__


class VentAggregator:
    def __init__(self, grid: Grid, vents: Tuple[Vent]):
        self.vents = vents
        self.grid = grid

    @classmethod
    def from_text(cls, text: str, diagonals_suck=True) -> VentAggregator:
        text = text.split("\n")
        vents = []
        max_size = [0, 0]
        for i in text:
            result = []
            for j in i.split(" -> "):
                result.extend(j.split(","))
            vent = Vent(*map(int, result))

            if diagonals_suck and vent.is_diagonal:
                continue
            vents.append(vent)

            if vent.x0 > max_size[0]:
                max_size[0] = vent.x0
            elif vent.x1 > max_size[0]:
                max_size[0] = vent.x1
            elif vent.y0 > max_size[1]:
                max_size[1] = vent.y0
            elif vent.y1 > max_size[1]:
                max_size[1] = vent.y1

        max_size = max_size[0] + 1, max_size[1] + 1
        print(max_size)
        return cls(Grid(*max_size), vents)

    def apply_array(self) -> Tuple[Tuple[int]]:
        for vent in self.vents:
            vent.apply_to_grid(self.grid)


aggre = VentAggregator.from_text(data, False)
aggre.apply_array()
print(aggre.grid.points_greater_than_2())
