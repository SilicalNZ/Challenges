"""Ghost Legs

    Goal
Ghost Legs is a kind of lottery game common in Asia. It starts with a number of vertical lines. Between the lines there are random horizontal connectors binding all lines into a connected diagram, like the one below.

A  B  C
|  |  |
|--|  |
|  |--|
|  |--|
|  |  |
1  2  3

To play the game, a player chooses a line in the top and follow the line downwards. When a horizontal connector is encountered, he must follow the connector to turn to another vertical line and continue downwards. Repeat this until reaching the bottom of the diagram.

In the example diagram, when you start from A, you will end up in 2. Starting from B will end up in 1. Starting from C will end up in 3. With a correctly drawn diagram it is guaranteed that every top label will map to a unique bottom label.

Given a Ghost Legs diagram, try to find out which top label is connected with which bottom label. List all connected pairs.
"""
import sys


class Legs(object):
    chars = ('|', '-')

    def __init__(self):
        self.legs = []
        self.size = None

    def _prep(self):
        result = list(zip(*self.legs))

        placeholder = [tuple([' ' for i in range(self.size[1])])]
        result = placeholder + result + placeholder
        self.size.append(len(result))
        return result

    def _analyze(self):
        paths = self._prep()
        for path in range(1, self.size[2], 2):
            current_path = path
            start = paths[path][0]
            for i in range(1, self.size[1] - 1, 1):
                tile = paths[current_path]
                if paths[current_path + 1][i] == self.chars[1]:
                    current_path += 2
                elif paths[current_path - 1][i] == self.chars[1]:
                    current_path -= 2
            finish = paths[current_path][-1]
            print(start + finish)


    def append_legs(self, arg: str):
        # Upon activation
        if self.size is None:
            self.size = [len(arg), 0]
        elif len(arg) != self.size[0]:
            return

        # General append
        self.legs.append(list(arg))
        self.size[1] += 1

        # If legs have ended
        if arg[0] != self.chars[0] and self.size[1] > 1:
            self._analyze()


this = Legs()
w, h = [int(i) for i in input().split()]
for i in range(h):
    line = input()
    line = line.replace('  ', ' ').replace('--', '-')
    this.append_legs(line)
