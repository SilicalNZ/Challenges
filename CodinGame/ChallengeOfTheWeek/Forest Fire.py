import sys


def mapsumzip(itr0, itr1):
    return tuple(map(sum, zip(itr0, itr1)))


class InvalidMove(Exception):
    pass


class Tile:
    char = '?'

    @classmethod
    def show(cls):
        return cls.char


class Tree(Tile):
    char = 'T'
    pass


class Fire(Tile):
    char = 'F'
    pass


class Area:
    """Works off of a 'data' property"""
    def __init__(self, data):
        self.data = data

    @property
    def size(self):
        return len(self.data[0]), len(self.data)

    @property
    def area(self):
        return self.width * self.length

    @property
    def width(self):
        return self.size[0]

    @property
    def length(self):
        return self.size[1]

    def get_positions(self):
        yield from [(x, y) for y in range(self.length) for x in range(self.width)]

    def get_data(self):
        yield from [self.data[y][x] for x, y in self.get_positions()]


class Layout(Area):
    def __init__(self, data):
        super().__init__(data)

    def __setitem__(self, key, value):
        self.handle_outofbounds(key)
        x, y = key
        self.data[y][x] = value

    def insert(self, position, object):
        self[position] = object

    def retrieve(self, object):
        return [pos for data, pos in zip(self.get_data(), self.get_positions()) if data == object]

    def __getitem__(self, key):
        self.handle_outofbounds(key)
        x, y = key
        return self.data[y][x]

    def __contains__(self, item):
        return any(item in i for i in self.data)

    def remove(self, position, object):
        if object in self[position]:
            self[position].remove(object)

    def _show(self):
        x = '\n'.join([''.join([j.show() for j in i]) for i in self.data])
        print(x, file=sys.stderr)

    def handle_outofbounds(self, key):
        if 0 > key[0] or key[0] >= self.width or 0 > key[1] or key[1] >= self.length:
            raise InvalidMove()

    @classmethod
    def from_size(cls, size, default):
        return cls([[default for x in range(size[0])] for y in range(size[1])])

    def subset(self, corner, size):
        layout = Layout.from_size(size, None)
        for position in layout.get_positions():
            try:
                layout[position] = self[mapsumzip(corner, position)]
            except InvalidMove:
                pass
        return layout


class Pattern:
    def __init__(self, corner, layout, fires):
        self.corner = corner
        self.layout = layout
        self.fires = fires


class Patterns:
    def __init__(self, *args):
        self.patterns = [*args]

    def __getitem__(self, item):
        return self.patterns[item]

    def append(self, pattern):
        self.patterns.append(pattern)

    def find(self, attr, value):
        for pattern in self.patterns:
            if getattr(pattern, attr) == value:
                return pattern

    def __iter__(self):
        return iter(self.patterns)


class _Units:
    water_used = None
    area = None

    def __init__(self, layout: Layout):
        self.layout = layout
        self.fires = Patterns()

    def bycorner(self, corner):
        return self.layout.subset(corner, self.area)

    def bylayout(self):
        for position in self.layout.get_positions():
            layout = self.bycorner(position)
            if None in layout:
                continue
            elif layout:
                self.fires.append(Pattern(position, layout, len(layout.retrieve(Fire))))
        return self.fires

    def favoured_option(self):
        potential = self.bylayout()
        return max(potential, key=lambda pattern: pattern.fires)


class Canadair(_Units):
    unit_code = 'C'
    water_used = 2100
    area = (3, 3)
    min_fires = 4


class FireHelicopter(_Units):
    unit_code = 'H'
    water_used = 1200
    area = (2, 2)
    min_fires = 2


class SmokeJumpersSquad(_Units):
    unit_code = 'J'
    water_used = 600
    area = (1, 1)
    min_fires = 1


class Director:
    def __init__(self, stage):
        self.stage = stage
        self.layout = self.stage.layout
        self.units = (Canadair(self.layout),
                    FireHelicopter(self.layout),
                    SmokeJumpersSquad(self.layout))

    def direct(self):
        for unit in self.units:
            if self.stage.water < unit.water_used:
                continue
            option = unit.favoured_option()
            if option.fires >= unit.min_fires:
                if option.fires == 4 and isinstance(unit, Canadair):
                    heli = FireHelicopter(option.layout)
                    new_option = heli.favoured_option()
                    if new_option.fires == 4:
                        new_option.corner = mapsumzip(option.corner, new_option.corner)
                        unit, option = heli, new_option
                print(f'{unit.unit_code} {option.corner[0]} {option.corner[1]}')
                self.stage.water -= unit.water_used
                return


class ParseInput:
    def __init__(self):
        size = int(input())
        self.size = size, size
        self.water = int(input())
        self.layout = None
        while True:
            self.fires()
            Director(self).direct()

    def fires(self):
        layout = Layout.from_size(self.size, Tree)
        for i in range(int(input())):
            layout[tuple(map(int, input().split()))] = Fire
        self.layout = layout


ParseInput()
