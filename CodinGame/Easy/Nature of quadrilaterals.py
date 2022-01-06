"""Nature of quadrilaterals

    Goal
You have to print the nature of the quadrilaterals whose vertices’ coordinates are given.
The nature can be:
* nothing, in which case you should write "quadrilateral",
* parallelogram (opposite sides are parallel to each other),
* rhombus (all four sides are equal),
* rectangle (all four angles are right) or
* square (it is a rectangle and a rhombus).
"""
import sys
import math


class FourSidedShape(object):
    def __init__(self, a, x_a: int, y_a: int, b, x_b: int, y_b: int, c, x_c: int, y_c: int, d, x_d: int, y_d: int):
        self.a = (x_a, y_a)
        self.b = (x_b, y_b)
        self.c = (x_c, y_c)
        self.d = (x_d, y_d)
        self.keys = {a: self.a, b: self.b, c: self.c, d: self.d}

    def formula_quadratic(self, x1: int, y1: int, x2: int, y2: int):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def all_sides(self):
        keys = list(self.keys)
        for x, label in enumerate(keys):
            vertex1 = self.keys[label]
            if x + 1 == len(keys):
                vertex2 = self.keys[keys[0]]
            else:
                vertex2 = self.keys[keys[x + 1]]

            self.formula_quadratic(*vertex1, *vertex2)


n = int(input())
for i in range(n):
    this = FourSidedShape(*input().split())


