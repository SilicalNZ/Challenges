import sys
from math import *
import statistics
from functools import lru_cache

from functools import lru_cache

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


GRAVITY = -3.711


class Boundary:
    def __init__(self, n, max, min):
        self.n = n
        self.max = max
        self.min = min

    def from_edge(self):
        if not self.min < self.n < self.max:
            return False
        return min(self.n - self.min, self.max - self.n)


    def __repr__(self):
        return repr(self.n)


class Lander:
    def __init__(self, x, y, h_speed, v_speed, fuel, rotate, power, landscape):
        super().__init__()
        x = Boundary(x, 0, 7000)
        y = Boundary(y, 0, 3000)
        h_speed = Boundary(h_speed, -40, 40)
        v_speed = Boundary(v_speed, -40, 40)
        fuel = Boundary(fuel, 0, 2000)
        power = Boundary(power, 0, 4)
        self.landscape = landscape

    def update(self, x, y, h_speed, v_speed, fuel, rotate, power):
        self.x = x
        self.y = y
        self.h_speed = h_speed
        self.v_speed = v_speed
        self.fuel = fuel
        self.rotate = rotate
        self.power = power

    def state(self):
        return self.x, self.y, self.h_speed, self.v_speed, self.fuel, self.rotate, self.power


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return repr((self.x, self.y))


class Line:
    def __init__(self, point0, point1):
        self.points = point0, point1

    @lru_cache()
    def linear(self, itr: int = 0):
        """Returns all the valid pixel coordinates between 2 points on a 2d-axis
        """
        x0, y0 = self.point[0]
        x1, y1 = self.point[1]
        if self.point[0] == self.point[1]:
            return [self.point[0]]
        link = []

        width, height = x1 - x0, y1 - y0

        def direction(a: int):
            # determines if pixel needs to be moved, and in what direction
            return -1 if a < 0 else 1 if a > 0 else 0

        w, h = direction(width), direction(height)

        # Create lists of all valid pixels, of each linear planes
        widths = tuple(range(x0, x1 + w, w)) if w != 0 else [x0]
        heights = tuple(range(y0, y1 + h, h)) if h != 0 else [y0]
        xyz = (widths, heights)

        # Return no changes, as there are no changes to be made
        if all(1 == len(i) for i in xyz):
            link.append((x0, y0))
            return link

        steps = len(max(xyz, key=len)) if itr <= 1 else itr
        literal_steps = steps - 1

        # Creates a literal len() of each list, for faster comprehension
        xyz = tuple((i, len(i) - 1) for i in xyz)

        for i in range(0, steps):
            progress = i / literal_steps
            x = widths[int(progress * xyz[0][1] + 0.5)]
            y = heights[int(progress * xyz[1][1] + 0.5)]

            link.append((x, y))
        return link

    @classmethod
    def from_tuple(cls, points):
        return cls(*points)


class Landscape(Line):
    def __init__(self):
        surface_n = int(input())

        self.points = []
        for i in range(surface_n):
            points = tuple(map(int, input().split()))
            self.points.append(Point(*points))
        self.lines = tuple(map(Line.from_tuple, zip(self.points, self.points[1:])))

    @property
    @lru_cache()
    def platform(self):
        for i, j in zip(self.points, self.points[1:]):
            if j.x - i.x >= 1000 and j.y == i.y:
                return i, j


class GameLoop:
    def __init__(self):
        self.landscape = None

    def input(self):
        self.landscape = Landscape()
        while True:
            self.lander = Lander(*map(int, input().split()), self.landscape)
            # self.lander.operate()

if __name__ == '__main__':
    GameLoop().input()
