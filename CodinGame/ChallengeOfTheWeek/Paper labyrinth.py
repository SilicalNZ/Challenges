"""Paper labyrinth


 Goal
You are Alice and you must find the rabbit then go out of the Queen’s labyrinth of death as quickly as you can.
The labyrinth is made of thin walls, each wall is binary-coded in each cell: 1 is the the down wall, 2 the left wall, 4 the top wall and 8 the right wall. If the wall is present, add its number to the cell. For example, 10=8+2 in a cell where you stand means that there are walls on your left and on your right and that you can walk downwards and upwards.
This also means that one-way doors are not forbidden. Look for instance at 10 5, if you are on 5, you can go on 10 but you can’t go back.
In fact, the cells are coded in hexadecimal, 10 is a.
The first simple labyrinth is this one:

________
|S    R|
‾‾‾‾‾‾‾‾


7=4+2+1, it’s the start cell on the left, 0xd=13=8+4+1, it’s the rabbit cell on the right. The other cells are 5=4+1.


https://www.codingame.com/ide/puzzle/paper-labyrinth
"""
import itertools


# 32min = Basic display


def int2bin4(n):
    return '{0:04b}'.format(n)

def hex2int(hex):
    return int(hex, 16)

def hex2bin(hex):
    return int2bin4(hex2int(hex))

def split_every(iterable, n):
    i = iter(iterable)
    slice = list(itertools.islice(i, n))
    while slice:
        yield slice
        slice = list(itertools.islice(i, n))



class Cell:
    __slots__ = 'right', 'up', 'left', 'down'

    def __init__(self, hex_rep, center='◦'):
        bin = hex2bin(hex_rep)
        [setattr(self, slot, bool(int(state))) for state, slot in zip(bin, self.__slots__)]
        self.center = center

    def display(self):
        template = [['█','█','█'], ['█', self.center, '█'], ['█', '█', '█']]

        positions = ((1, 2), (0, 1), (1, 0), (2, 1))
        for n, slot in zip(positions, self.__slots__):
            if not getattr(self, slot):
                template[n[0]][n[1]] = ' '
        return [''.join(i) for i in template]


class Labyrinth:
    __slots__ = 'size', 'cells'

    def __init__(self, size, hex_rep):
        self.cells = [Cell(i) for i in hex_rep]
        self.size = size

    def as_grid(self):
        return [*split_every(self.cells, self.size[0])]

    def display(self, as_str=True):
        results = []
        for cells in self.as_grid():
            layout = zip(*(i.display() for i in self.cells))
            result = '\n'.join([''.join(i) for i in layout])
            results.append(result)
        return '\n'.join(results)


class Navigator:
    __slots__ = 'labyrinth', 'entrance', 'goal'

    def __init__(self, labyrinth, entrance, goal):
        self.labyrinth = labyrinth
        self.entrance = entrance
        self.goal = goal

    def display(self):
        display = self.labyrinth.display()
        display[self.entrance[1]][self.entrance[0]] = 'S'
        return display


hexadecimal = 'e65cabea2519355d'
print(Labyrinth((4, 4), hexadecimal).display())

