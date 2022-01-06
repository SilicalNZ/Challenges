import sys
import math
from itertools import cycle
from functools import lru_cache
import random


### EXCEPTIONS


class InvalidMove(Exception):
    pass


### UTILS


class utils:
    @staticmethod
    def mapsumzip(*args):
        return tuple(map(sum, zip(*args)))

    @staticmethod
    def widening_square(position):
        s = list(position)
        yield s[0], s[1]
        c, w = 0, 1
        while True:
            s[0] -= 1
            s[1] -= 1
            w += 2
            yield from [(s[0] + x, s[1]) for x in range(w)]
            for y in range(1, w - 1):
                yield s[0], s[1] + y
                yield s[0] + w, s[1] + y
            yield from [(s[0] + x, s[1] + w) for x in range(w)]


class Compass:
    @classmethod
    def south(cls, pos=None):
        return (0, 1) if not pos else utils.mapsumzip(cls.south(), pos)

    @classmethod
    def north(cls, pos=None):
        return (0, -1) if not pos else utils.mapsumzip(cls.north(), pos)

    @classmethod
    def east(cls, pos=None):
        return (1, 0) if not pos else utils.mapsumzip(cls.east(), pos)

    @classmethod
    def west(cls, pos=None):
        return (-1, 0) if not pos else utils.mapsumzip(cls.west(), pos)

    @classmethod
    def opposite(cls, direction):
        reverse = {Compass.south(): Compass.north(),
                   Compass.north(): Compass.south(),
                   Compass.east(): Compass.west(),
                   Compass.west(): Compass.east()}

        return reverse[direction]

    @classmethod
    def all(cls, pos=None):
        if pos:
            return cls.north(pos), cls.east(pos), cls.south(pos), cls.west(pos)
        return cls.north, cls.east, cls.south, cls.west


class PaperScissorRock:
    names = ['paper, scissors, rock']

    order = {'left': {
                'ROCK': 'SCISSORS',
                'SCISSORS': 'PAPER',
                'PAPER': 'ROCK'
            },
            'right': {
                'SCISSORS': 'ROCK',
                'PAPER': 'SCISSORS',
                'ROCK': 'PAPER'
            }}

    @classmethod
    def beat(cls, one, two):
        return cls.order['left'][one] == two

    @classmethod
    def inverse(cls, two):
        return cls.order['right'][one]


class BreadthSearch:
    def __init__(self, position, parent=None):
        self.children = []
        self.position = position
        self.parent = parent

        self._next_child = None
        self._current_child = None

        if parent is None:
            self.next_child()

    @property
    def depth(self):
        ct = 0
        i = self
        while i.parent:
            ct += 1
            i = i.parent
        return ct

    def create_children(self):
        for direction in Compass.all(self.position):
            if self.parent and direction == self.parent.position:
                continue
            self.children.append(BreadthSearch(direction, self))

    def next_child(self):
        if self._next_child is None:
            self.create_children()
            self._next_child = self.children[0]
            return self
        elif not self.children and self.parent is None:
            return None

        current = self._next_child
        idx = (self.children.index(current) + 1) % len(self.children)
        self._next_child = self.children[idx]
        self._current_child = current

        current = current.next_child()
        if isinstance(current, tuple):
            return (self, *current)
        return self, current

    def cut(self):
        if self._current_child is None:
            return self.parent.cut()

        self.children.remove(self._current_child)
        if not self.children and self.parent:
            self.parent.cut()

    def __repr__(self):
        return repr(self.position)

    def __getitem__(self, item):
        return self.position[item]


### LAYOUT


class SizeSum:
    """Works off of a 'data' property"""

    def _size(self):
        return len(self._data[0]), len(self._data)

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value
        self.size = self._size()

    @property
    def size_sum(self):
        return self.width * self.length

    @property
    def width(self):
        return self.size[0]

    @property
    def length(self):
        return self.size[1]

    def __repr__(self):
        return repr(self.size)

    def get_positions(self):
        yield from [(x, y) for y in range(self.length) for x in range(self.width)]

    def get_data(self):
        yield from [self._data[y][x] for x, y in self.get_positions()]


class Stacker():
    def __init__(self, object, position, default):
        self.stack = object
        self.position = position
        self.default = default

    def remove(self, object):
        if self == object:
            self.stack = self.default

    def replace(self, object):
        self.stack = object

    insert = replace

    def __eq__(self, other):
        return self.stack == other or self.stack.__class__ == other

    def __repr__(self):
        return repr(self.stack)

    def __str__(self):
        return str(self.stack)

    def __getattr__(self, item):
        return getattr(self.stack, item)



class Layout(SizeSum):
    def __init__(self, data):
        self.default = EmptyTile()
        self.data = [[Stacker(x, (x0, y0), self.default) for x0, x in enumerate(y)] for y0, y in enumerate(data)]

    def _key_converter(self, key):
        return key[0] % (self.width - 1), key[1] % (self.length - 1)

    def __setitem__(self, key, value):
        new_key = self._key_converter(key)
        if new_key != key:
            value.position = new_key
            return
        x, y = key
        self._data[y][x].replace(value)

    def insert(self, position, object):
        self[position] = object

    def __getitem__(self, key):
        key = self._key_converter(key)
        x, y = key
        return self._data[y][x]

    def remove(self, position, object):
        if object == self[position] or object == self[position].__class__:
            self[position].remove(object)

    def _show(self):
        x = '\n'.join([''.join([str(x) for x in y]) for y in self.data])
        print(x, file=sys.stderr)

    def get_type(self, object):
        yield from [self[i] for i in self.get_positions() if self[i] == object]


### TILE TYPES


class Tile:
    def __init__(self, char):
        self.char = char

    def __repr__(self):
        return repr(self.char)

    def __str__(self):
        return str(self.char)


class EmptyTile(Tile):
    def __init__(self):
        super().__init__(' ')


class Wall(Tile):
    def __init__(self, char):
        super().__init__(char)


class Pellet(Tile):
    def __init__(self, layout, value, position):
        super().__init__('-')
        self.value = value
        self.position = position
        self.layout = layout

        if self.is_super:
            self.char = 'X'

    @property
    def is_super(self):
        return self.value == 10


class MaybePellet(Pellet):
    pass


### ENTITY TYPES


class Entity(Tile):
    def __init__(self, layout, char, position):
        super().__init__(char)
        self.layout = layout
        self._position = position
        self.prev_position = None
        self.layout.insert(self.position, self)
        self.last_move = None

    def update_layout(self):
        self.layout.remove(self.prev_position, self)
        self.layout.insert(self.position, self)

    @property
    def position(self):
        return self._position

    def _position_setter(self, value):
        prev_pos = self.prev_position
        self.prev_position = self.position
        self._position = value
        try:
            self.update_layout()
        except InvalidMove:
            self._position = self.prev_position
            self.prev_position = prev_pos
            raise InvalidMove()

    @position.setter
    def position(self, value):
        self._position_setter(value)

    def line_of_sight(self):
        for direction in Compass.all():
            row = []
            position = self.position
            while True:
                position = direction(position)
                tile = self.layout[position]
                if tile != Wall:
                    row.append(tile)
                else:
                    break
            yield row


class BreadthAnaylsis:
    def __init__(self, breadth, unit):
        self.breadth = breadth
        self.unit = unit

    @lru_cache()
    def intersting(self):
        return tuple(filter(lambda x: x != self.unit.layout.default, self.breadth))

    @lru_cache()
    def enemies(self):
        return tuple(filter(lambda x: x == Unit and x.player != self.unit.player, self.breadth))

    @lru_cache()
    def allies(self):
        return tuple(filter(lambda x: x == Unit and x.player == self.unit.player, self.breadth))

    @lru_cache()
    def pellets(self):
        return tuple(filter(lambda x: x == Pellet, self.breadth))

    @lru_cache()
    def super_pellets(self):
        return tuple(filter(lambda x: x == Pellet and x.is_super, self.breadth))

    def extend(self, breadth=None):
        breadth = self.breadth if breadth is None else breadth
        for direction in Compass.all(breadth[-1].position):
            if direction == breadth[-1].position:
                continue
            direction = self.layout._key_converter(direction)
            tile = self.layout[direction]
            if tile != Wall:
                return (*breadth, tile)

    @property
    def end_position(self):
        return self.breadth[-1].position


class Navigation:
    def __init__(self, unit):
        self.unit = unit

    @property
    def player(self):
        return self.unit.player

    @property
    def layout(self):
        return self.unit.layout

    @property
    def position(self):
        return self.unit.position

    def _seedling(self, seedling=None, depth=10):
        seedling = BreadthSearch(self.position) if seedling is None else seedling
        gen = None
        while True:
            breadth = seedling.next_child()
            if not breadth:
                return
            breadth_end = breadth[-1]
            breadth_end.tile = self.layout[breadth_end]
            if breadth_end.tile == Wall or len(breadth) >= depth:
                breadth_end.cut()
            else:
                yield tuple(i.tile for i in breadth[1:])

    def move(self):
        for _breadth in self._seedling():
            breadth = BreadthAnaylsis(_breadth, self.unit)
            if breadth.enemies():
                if PaperScissorRock.beat(self.unit.type_id, breadth.enemies()[0].type_id):
                    self.unit.options = (1 - (1 / 10 * len(_breadth)), _breadth)
                    continue
                else:
                    self.unit.avoid.add(breadth.enemies()[0].position)
            if breadth.allies():
                self.unit.avoid.add(breadth.allies()[0].position)
            if breadth.super_pellets():
                self.unit.options = (2, _breadth)
            elif breadth.pellets():
                self.unit.options = (1 - (1 / 10 * len(_breadth)), _breadth)


class Unit(Entity):
    def __init__(self, layout, position, type_id, speed_turns_left, ability_cooldown, player):
        super().__init__(layout, 'C', position)
        self.player = player
        self.speed_turns_left = speed_turns_left
        self.ability_cooldown = ability_cooldown
        self.type_id = type_id

        self.avoid = set()
        self.navigator = Navigation(self)
        self._options = []
        self.has_moved = False

    @property
    def options(self):
        return self._options

    @options.setter
    def options(self, value):
        self._options.append(value)

    def distant_pellet(self):
        x0, y0 = self.position
        distances = []
        for pellet in (*self.layout.get_type(Pellet), *self.layout.get_type(MaybePellet)):
            x1, y1 = pellet.position
            distances.append((math.sqrt((x1 - x0) ** 2 + (y1 - y0) ** 2), pellet))
        return min(distances, key=lambda x: x[0])[1]

    def ally_bubble(self):
        bubbles = set()
        for unit in self.player.units:
            if unit != self:
                square = utils.widening_square(unit.position)
                [bubbles.add(i) for i in [next(square) for _ in range(8)]]
        return bubbles

    @property
    @lru_cache()
    def moving_to(self):
        self.has_moved = True
        for unit in self.player.units:
            if unit != self and unit.has_moved:
                self.avoid.add(unit.moving_to)
        options = [*filter(lambda x: not any(i.position in self.avoid for i in x[1]), self.options)]

        closest = [*filter(lambda x: len(x[1]) < 3, options)]
        non_closest = [*filter(lambda x: any(x[0] in i for i in closest), closest)]
        other = [*filter(lambda x: x in non_closest, options)]
        if other:
            options = other

        non_bubbles = [*filter(lambda x: not any(i.position in self.ally_bubble() for i in x[1]), options)]
        if non_bubbles:
            options = non_bubbles

        if options:
            options = max(options, key=lambda x: x[0])[1]
        else:
            return self.distant_pellet().position
        if len(options) == 1:
            return options[0].position
        else:
            return options[1].position

    def move(self):
        self.navigator.move()


### GAME STATE


class Player():
    def __init__(self):
        self.score = None
        self._units = {}

    def remove_all(self):
        for unit in self._units.values():
            unit.layout.remove(unit.position, unit)
        self._units = {}

    @property
    def units(self):
        return self._units.values()


class ParseInput():
    def __init__(self):
        self.layout = None
        self.p1 = Player()
        self.p2 = Player()

    def mine(self, bool):
        return self.p1 if bool else self.p2

    def create_layout(self):
        tiles = {' ': EmptyTile(), '#': Wall('H')}

        width, height = [int(i) for i in input().split()]
        layout = []
        for i in range(height):
            layout.append([tiles[i] for i in input()])
        self.layout = Layout(layout)
        self.maybe_pellets()

    def maybe_pellets(self):
        for tile in self.layout.get_data():
            if not tile == Wall:
                tile.replace(MaybePellet(self.layout, 0, tile.position))

    def update_pellets(self):
        visible_pellet_count = int(input())  # all pellets in sight
        pellets = []
        for i in range(visible_pellet_count):
            x, y, value = [int(j) for j in input().split()]
            pellet = Pellet(self.layout, value, (x, y))
            self.layout[(x, y)] = pellet
            pellets.append(pellet.position)

        for unit in self.p1.units:
            for los in unit.line_of_sight():
                los = [*filter(lambda x: x.position not in pellets, los)]
                for tile in los:
                    tile.remove(MaybePellet)
                    tile.remove(Pellet)

    def update_unit(self):
        pac_id, mine, x, y, type_id, speed_turns_left, ability_cooldown = input().split()
        pac_id = int(pac_id)
        mine = mine != "0"
        x = int(x)
        y = int(y)
        speed_turns_left = int(speed_turns_left)
        ability_cooldown = int(ability_cooldown)

        player = self.mine(mine)
        units = player._units
        if pac_id not in units:
            units[pac_id] = Unit(self.layout, (x, y), type_id, speed_turns_left, ability_cooldown, player)
        else:
            units[pac_id].position = (x, y)
        units[pac_id].speed_turns_left = speed_turns_left
        units[pac_id].ability_cooldown = ability_cooldown
        units[pac_id].type_id = type_id

    def run(self):
        self.create_layout()
        while True:
            self.p1.score, self.p2.score = [int(i) for i in input().split()]
            self.p2.remove_all()
            self.p1.remove_all()
            visible_pac_count = int(input())  # all your pacs and enemy pacs in sight
            for i in range(visible_pac_count):
                self.update_unit()
            self.update_pellets()
            if not [*self.p1.units][0].speed_turns_left and not [*self.p1.units][0].ability_cooldown:
                print(' | '.join([f'SPEED {key}' for key in self.p1._units.keys()]))
                continue
            [unit.move() for unit in self.p1.units]
            temp = 'MOVE {0} {1} {2}'
            x = ' | '.join([temp.format(id, *unit.moving_to) for id, unit in self.p1._units.items()])
            print(x)
            self.layout._show()


if __name__ == '__main__':
    ParseInput().run()
