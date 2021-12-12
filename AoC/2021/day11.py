from __future__ import annotations

from typing import Optional, List
from collections import Counter
import pprint


data = ""

START = 'start'
END = 'end'


class Visited:
    def __init__(self):
        self.visited: List[Cave] = []

    def append(self, value: Cave) -> Visited:
        visited = self.copy()
        visited.visited.append(value)
        return visited

    def copy(self) -> Visited:
        visited = Visited()
        visited.visited = self.visited[:]
        return visited

    def visited_twice(self) -> bool:
        for key, value in Counter(self.visited).items():
            if not key.is_size_large and value == 2:
                return True

    def __contains__(self, item):
        return item in self.visited


class Cave:
    def __init__(self, name: str):
        self.name = name
        self.connection: List[Cave] = []

    @property
    def is_size_large(self) -> bool:
        return self.name.upper() == self.name

    @property
    def is_end(self) -> bool:
        return self.name == END

    @property
    def is_start(self) -> bool:
        return self.name == START

    def add_connection(self, cave: Cave):
        self.connection.append(cave)

    @classmethod
    def from_data(cls, data: str) -> Cave:
        caves = {}
        for i in data.split("\n"):
            x, y = i.split("-")

            if y not in caves:
                caves[y] = Cave(y)
            if x not in caves:
                caves[x] = Cave(x)
            caves[x].add_connection(caves[y])
            caves[y].add_connection(caves[x])

        return caves["start"]

    def __str__(self):
        return f"{self.name}"

    def navigate(self, visited: Optional[Visited] = None) -> List[Cave]:
        if visited is None:
            visited = Visited()

        for child in self.connection:
            if child.is_start:
                continue
            elif not child.is_size_large and child in visited and visited.visited_twice():
                continue

            copied_visited = visited.append(child)

            if child.is_end:
                yield [self, child]
            else:
                for result in child.navigate(copied_visited):
                    yield [self, *result]

    __repr__ = __str__


cave = Cave.from_data(data)

for x, i in enumerate(cave.navigate()):
    print(x, i)
