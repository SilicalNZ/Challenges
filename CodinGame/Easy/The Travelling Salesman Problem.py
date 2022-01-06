"""The Travelling Salesman Problem

    Goal
The travelling salesman problem (TSP) asks the following question: "Given a list of cities and the distances between each pair of cities, what is the shortest possible route that visits each city exactly once and returns to the origin city?"

In this puzzle not necessarily the shortest route is the answer but an approximation using the greedy algorithm (which in fact could be the shortest route as well).

The greedy algorithm starts at the first input given and always chooses the nearest point next to it. This continues until no points are left and the last point is connected to the first point.

Use the euclidian distance, i.e. sqrt(deltaX^2 + deltaY^2), as the distance between two cities. If there are points with the same distance, always pick the one occurring first in the list.

In general, the greedy algorithm does not find the optimal solution, but nonetheless a greedy heuristic may yield locally optimal solutions that approximate a global optimal solution in a reasonable time.
"""
import sys
import math


class Greddy_Algo(object):
    def __init__(self):
        self.distance_travelled = 0
        self.position = None
        self.locations = []

    def add(self, x, y):
        if self.position is None:
            self.begin = (x, y)
            self.position = (x, y)
            return
        self.locations.append((x, y))

    def execute(self):
        if self.position is None:
            return False

        while self.locations:
            distances = []
            a, b = self.position
            for x, y in self.locations:
                z = math.sqrt((a-x)**2 + (b-y)**2)
                distances.append(z)
            next_distance, next_location = min(zip(distances, self.locations))

            self.distance_travelled += next_distance
            self.locations.remove(next_location)
            self.position = next_location

        a, b = next_location
        x, y = self.begin
        self.distance_travelled += math.sqrt((a - x) ** 2 + (b - y) ** 2)
        return int(round(self.distance_travelled))


n = int(input())
this = Greddy_Algo()
for i in range(n):
    x, y = [int(j) for j in input().split()]
    this.add(x, y)

print(this.execute())
