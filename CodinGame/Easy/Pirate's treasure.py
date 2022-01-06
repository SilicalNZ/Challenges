"""Pirate's treasure
Treasure is placed on free space surrounded by only obstacles.

There are three possibilities how the treasure can be surrounded:
By 3 obstacles when the treasure is in the corner of the map.
By 5 obstacles when the treasure is on the edge of the map.
By 8 obstacles when the treasure is inside the map.

    Goal
Goal of this puzzle is to found pirate's treasure.
"""
import sys


class FindTreasure(object):
    def __init__(self, map: list):
        self.map = map

    def execute(self):
        obj = self._give_border(self.map)
        [print(i, file=sys.stderr) for i in obj]
        return self._calculate(obj)

    # from CoddingGame.Easy.Organic_Compounds
    @staticmethod
    def _give_border(arg):
        num = 1
        result = [[num] + i + [num] for i in arg]
        tmp = [[num for _ in range(len(result[0]))]]
        result = tmp + result + tmp
        return result

    @staticmethod
    def _calculate(arg):
        for y in range(1, len(arg[1:-1]) + 1):
            for x in range(1, len(arg[y][1:-1]) + 1):
                if arg[y][x] == 0:
                    row1 = arg[y-1][x-1:x+2]
                    row2 = arg[y][x-1:x+2]
                    row3 = arg[y+1][x-1:x+2]
                    z = sum(row1 + row2 + row3)
                    if z == 8:
                        return x - 1, y - 1


w = int(input())
h = int(input())

this = FindTreasure([[int(i) for i in input().split()] for _ in range(h)])
print(' '.join([str(i) for i in this.execute()]))
