"""Dead men's shot

    Goal
Captain Jack Sparrow and his pirate friends have been drinking one night. After plenty of rum, they got into an argument about who is the best shot. Captain Jack takes up some paint and paints a target on a nearby wall. The pirates take out their guns and start shooting.

Your task is to help the drunk pirates find out which shots hit the target.

Captain Jack Sparrow drew the target by drawing N lines. The lines form a convex shape defined by N corners. A convex shape has all internal angles less than 180 degrees. For example, all internal angles in a square are 90 degrees.

A shot within the convex shape or on one of the lines is considered a hit.
"""
import sys
import math


class ConnectPoint:
    @staticmethod
    def linear(point0: tuple, point1: tuple, itr: int = 0):
        """Returns all the valid pixel coordinates between 2 points on a 2d-axis
        """
        x0, y0 = point0
        x1, y1 = point1

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
            yield x0, y0
            return

        steps = len(max(xyz, key=len)) if itr <= 1 else itr
        literal_steps = steps - 1

        # Creates a literal len() of each list, for faster comprehension
        xyz = tuple((i, len(i) - 1) for i in xyz)

        for i in range(0, steps):
            progress = i / literal_steps
            x = widths[int(progress * xyz[0][1] + 0.5)]
            y = heights[int(progress * xyz[1][1] + 0.5)]

            yield (x, y)

class Region:
    def __init__(self, x, y):
        width = [0 for _ in range(x)]
        region = [width for _ in range(y)]
        self.region = region

    def label(self, num, *positions):
        for x, y in positions:
            self.region[y][x] = num






class Shape(Region, ConnectPoint):
    def __init__(self):
        Region.__init__()
        self.corners = []
        self.region = []

    def add_corner(self, x: int, y: int):
        self.corners.append((x, y))


    def draw_edges(self):
        width = sorted(self.corners, key=lambda xy: max(x))[0][0]
        length = sorted(self.corners, key=lambda xy: max(y))[0][0]

        self.generate_region(width, length)
        for i, j in zip(self.corners, self.corners[1:] + [self.corners[0]]):
            self.label(1, self.linear(i, j))

















n = int(input())
for i in range(n):
    x, y = [int(j) for j in input().split()]
m = int(input())
for i in range(m):
    x, y = [int(j) for j in input().split()]

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)

print("hit_or_miss")