import sys
import math
import random


class InvalidMove(Exception):
    pass


class utils:
    @staticmethod
    def mapsumzip(*args):
        return tuple(map(sum, zip(*args)))

    @staticmethod
    def linear(point0, point1, itr: int = 0):
        """Returns all the valid pixel coordinates between 2 points on a 2d-axis
        """
        x0, y0 = point0
        x1, y1 = point1
        if point0 == point1:
            return [point0]
        link = []

        width, height = x1 - x0, y1 - y0

        def direction(a: int):
            # determines if pixel needs to be moved, and in what direction
            return -1 if a < 0 else 1 if a > 0 else 0

        if abs(width) >= abs(height):
            return x0 + direction(width), y0
        else:
            return x0, y0 + direction(height)

    @staticmethod
    def diamond_from_point(point0, radius: int = 0):
        x0, y0 = point0
        r = radius

        x, y = r, 0
        dx, dy = 1, 1
        err = dx - r << 1

        link = set()

        while x >= y:
            link.update((
                (x0 + x, y0 + y),
                (x0 + y, y0 + x),
                (x0 - y, y0 + x),
                (x0 - x, y0 + y),
                (x0 - x, y0 - y),
                (x0 - y, y0 - x),
                (x0 + y, y0 - x),
                (x0 + x, y0 - y)
            ))

            if err <= 0:
                y += 1
                err += dy
                dy += 2
            if err > 0:
                x -= 1
                dx += 2
                err += dx - r << 1
        return list(link)  # Unsorted due to complexity


class Compass:
    @classmethod
    def south(cls):
        return 0, 1

    @classmethod
    def north(cls):
        return 0, -1

    @classmethod
    def east(cls):
        return 1, 0

    @classmethod
    def west(cls):
        return -1, 0

    @classmethod
    def all(cls):
        return cls.north(), cls.east(), cls.south(), cls.west()

    @classmethod
    def move_all_options(cls, position):
        return [utils.mapsumzip(position, i) for i in cls.all()]


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


class Stacker():
    def __init__(self, *objects):
        self.stack = list(objects)

    def condition_check(self, activator):
        try:
            [i.condition(activator) for i in self.stack if hasattr(i, 'condition')]
        except Exception as e:
            return False
        else:
            return True

    def tile_sharer(self, activator):
        try:
            [i.tile_sharer(activator) for i in self.stack if hasattr(i, 'tile_sharer')]
        except Exception as e:
            return False
        else:
            return True

    def remove(self, object):
        self.stack.remove(object)

    def append(self, object):
        self.stack.append(object)

    def show(self):
        return str(self.stack[-1])

    def __contains__(self, item):
        return item in self.stack


class Map(SizeSum):
    def __init__(self, data):
        self.data = [[Stacker(x) for x in y] for y in data]

    def __setitem__(self, key, value):
        self.handle_outofbounds(key)
        x, y = key
        self._data[y][x].append(value)

    def insert(self, position, object):
        self.handle_outofbounds(position)
        self[position].append(object)

    def __getitem__(self, key):
        self.handle_outofbounds(key)
        x, y = key
        return self._data[y][x]

    def remove(self, position, object):
        if object in self[position]:
            self[position].remove(object)

    def _show(self):
        x = '\n'.join([''.join(['|'] + [j.show() for j in i] + ['|']) for i in self.data])
        print(x, file=sys.stderr)

    def handle_outofbounds(self, key):
        """This is called whenever the key is out of bounds"""
        if 0 > key[0] or key[0] >= self.width or 0 > key[1] or key[1] >= self.length:
            raise InvalidMove()

    def tile_sharers(self):
        yield from [i for i in self.get_positions() if self[i].tile_sharer(None)]


class Tile:
    def __init__(self, char):
        self.char = char

    def __repr__(self):
        return repr(self.char)

    def __str__(self):
        return str(self.char)


class Fog(Tile):
    def __init__(self):
        super().__init__('?')


class MapBlind(SizeSum):
    def __init__(self):
        self.fog = Fog()
        self.data = [[self.fog]]
        self.x = [0, 0]
        self.y = [0, 0]

    def __setitem__(self, key, value):
        x, y = key
        self.data[y - self.y[0]][x - self.x[0]] = value

    def insert(self, position, object):
        position = list(position)
        if position[0] < self.x[0]:
            self.data = [[self.fog] + x for x in self.data]
            self.x[0] -= 1
        elif position[0] > self.x[1]:
            self.data = [x + [self.fog] for x in self._data]
            self.x[1] += 1
        if position[1] < self.y[0]:
            self.data = [[self.fog] * self.width] + self.data
            self.y[0] -= 1
        elif position[1] > self.y[1]:
            self.data = self.data + [[self.fog] * self.width]
            self.y[1] += 1

        self[position] = object

    def remove(self, position, object):
        self[position] = None

    def find_within(self, map: Map):
        for y0, y1 in zip(range(0, map.length + 1), range(self.length, map.length + 1)):
            for x0, x1 in zip(range(0, map.width + 1), range(self.width, map.width + 1)):
                for row_main, row_unknown in zip(map.data[y0:y1], self.data):
                    row_main = row_main[x0:x1]
                    for main_tile, unknown_tile in zip(row_main, row_unknown):
                        if not main_tile.tile_sharer(unknown_tile) and unknown_tile != self.fog:
                            break
                    else:
                        continue
                    break
                else:
                    yield x0, y0

    def merge(self, corner, map):
        for y, i in enumerate(self.data, 0):
            active_corner = list(corner)
            active_corner[0] -= 1
            active_corner[1] += y
            for x, j in enumerate(i, 0):
                active_corner[0] += 1
                if j != self.fog:
                    map[active_corner] = j
                if isinstance(j, Submarine):
                    j._position = active_corner
        map._show()

    def _show(self):
        x = '\n'.join([''.join(['|'] + [str(j) for j in i] + ['|']) for i in self.data])
        print(x, file=sys.stderr)


class Entity(Tile):
    def __init__(self, map, char, position):
        super().__init__(char)
        self.map = map
        self._position = position
        self.map.insert(self.position, self)
        self.prev_position = None
        self.last_move = None

    def update_map(self):
        self.map.remove(self.prev_position, self)
        self.map.insert(self.position, self)

    @property
    def position(self):
        return self._position

    def _position_setter(self, value):
        prev_pos = self.prev_position
        self.prev_position = self.position
        self._position = value
        try:
            self.update_map()
        except InvalidMove:
            self._position = self.prev_position
            self.prev_position = prev_pos
            raise InvalidMove()

    @position.setter
    def position(self, value):
        self._position_setter(value)

    def _get_movement(self, direction):
        return utils.mapsumzip(self.position, direction)

    def move_north(self):
        self.position = self._get_movement(Compass.north())

    def move_east(self):
        self.position = self._get_movement(Compass.east())

    def move_south(self):
        self.position = self._get_movement(Compass.south())

    def move_west(self):
        self.position = self._get_movement(Compass.west())

    _directions = {
        'N': move_north,
        'E': move_east,
        'S': move_south,
        'W': move_west}

    def move_letter(self, direction):
        self._directions[direction](self)
        self.last_move = direction


class Trail(Tile):
    def __init__(self, char):
        super().__init__(char)

    def tile_sharer(self, activator):
        if hasattr(activator, 'trail') and activator.trail == self:
            raise InvalidMove


class Slimy(Entity):
    def __init__(self, map, char, trail_char, position):
        super().__init__(map, char, position)
        self.trail = Trail(trail_char)
        self.prev_positions = []

    @property
    def position(self):
        return self._position

    def _position_setter(self, value):
        self.prev_positions.append(self.prev_position)
        self.map.insert(self.prev_position, self.trail)

    @position.setter
    def position(self, value):
        super()._position_setter(value)
        self._position_setter(value)

    def clear(self):
        for position in self.position:
            self.map.remove(position, self.trail)


class Torpedo:
    radius = 4

    def __init__(self, entity):
        self.entity = entity
        self.fired_at = None

    @property
    def map(self):
        return self.entity.map

    def firing_range(self):
        return utils.diamond_from_point(self.entity.posiiton, self.radius)

    def fire_at_pos(self, position):
        if isinstance(self.map[position][-1], Water) and position in self.firing_range():
            self.entity.torpedo = self.posiiton


class Surface:
    def __init__(self, entity):
        self.entity = entity

    def surface(self):
        self.entity.surfaced = True
        for trail in self.entity.prev_positions:
            self.entity.remove(trail, self.entity.trail)
        print('SURFACE')


class Actions:
    def __init__(self, entity):
        self.torpedo = Torpedo(self)
        self.surface = Surface(self)


class Submarine(Slimy):
    def __init__(self, map, char, trail_char, position):
        super().__init__(map, char, trail_char, position)
        self.torpedo = None
        self.opponent = None
        self.surfaced = False
        self.action = Actions(self)

    def update_map(self):
        self.map.remove(self.prev_position, self)
        self.map.insert(self.position, self)

    def _get_movement(self, direction):
        return utils.mapsumzip(self.position, direction)

    def get_all_movements(self):
        yield from map(self._get_movement, Compass.all())

    def compass_move(self):
        for pos, direction in zip(self.get_all_movements(), self._directions):
            try:
                pos = self.map[pos]
            except InvalidMove:
                continue
            if pos.tile_sharer(self):
                self.move_letter(direction)
                return True

    def move_to_point(self, point):
        next_pos = utils.linear(self.position, point)
        if self.map[next_pos].tile_sharer(self):
            self.compass_move()
        else:
            for direction, movement in zip(self._directions, self.get_all_movements()):
                if movement == next_pos:
                    self.move_letter(direction)
                    return

    def move_to_torpedo(self):
        self.move_to_point(self.opponent.torpedo)

    def auto_move(self):
        if self.opponent.map == self.map:
            self.move_to_point(self.opponent.position)
        elif self.opponent.torpedo and self.opponent.torpedo != self.position:
            self.move_to_torpedo()
        else:
            if not self.compass_move():
                self.action.surface()




class Island(Tile):
    def __init__(self):
        super().__init__('X')

    def tile_sharer(self, activator):
        raise InvalidMove


class Water(Tile):
    def __init__(self):
        super().__init__('-')


class ParseInput:
    def __init__(self):
        self.layout = None
        self.p1 = None
        self.p2 = None

    def create_layout(self):
        tiles = {'.': Water(), 'x': Island()}

        width, height, my_id = [int(i) for i in input().split()]
        layout = []
        for i in range(height):
            layout.append([tiles[i] for i in input()])
        layout = Map(layout)
        return layout

    def create_submarines(self):
        self.p1 = Submarine(self.layout, '1', 'o', random.choice([*self.layout.tile_sharers()]))
        self.p2 = Submarine(MapBlind(), '2', 'x', (0, 0))
        pos = str(self.p1.position[0]) + ' ' + str(self.p1.position[1])
        self.p1.opponent = self.p2
        self.p2.opponent = self.p1
        print(pos)

    def bio_input(self):
        x, y, my_life, opp_life, torpedo_cooldown, sonar_cooldown, silence_cooldown, mine_cooldown = [int(i) for i in
                                                                                                      input().split()]
        return x, y, my_life, opp_life, torpedo_cooldown, sonar_cooldown, silence_cooldown, mine_cooldown

    def sonar_result(self):
        return input()

    def opponent_orders(self):
        for i in input().split('|'):
            i = i.split()
            if i[0] == 'MOVE':
                self.p2.move_letter(i[1])
                corner = None
                if isinstance(self.p2.map, MapBlind):
                    find_within = self.p2.map.find_within(self.p1.map)
                    try:
                        corner = next(find_within)
                        next(find_within)
                    except StopIteration:
                        if corner:
                            self.p2.map.merge(corner, self.p1.map)
                            self.p2.map = self.p1.map
                    else:
                        pass
            elif i[0] == 'TORPEDO':
                self.p2.torpedo = int(i[1]), int(i[2])
            self.p2.map._show()

    def run(self):
        self.layout = self.create_layout()
        self.create_submarines()
        while True:
            self.bio_input()
            self.sonar_result()
            self.opponent_orders()
            self.p1.auto_move()
            print('MOVE', self.p1.last_move, 'TORPEDO')



i = Island()
w = Water()
layout = [[w, w, w, i, i, i, w, w, w, w, w, w],
          [w, w, w, i, i, i, w, w, w, w, w, w],
          [w, w, w, i, i, w, w, w, w, w, w, w],
          [w, w, w, i, i, w, w, w, i, i, w, w],
          [w, w, w, w, w, w, w, w, i, i, w, w],
          [w, w, w, w, w, w, w, w, w, w, w, w],
          [w, w, w, w, w, w, w, w, w, w, w, w],
          [w, w, w, w, w, i, i, w, w, w, w, w],
          [w, w, w, w, w, i, i, w, w, i, i, w],
          [w, w, w, w, w, w, w, w, w, i, i, w],
          [w, w, w, w, w, w, w, w, w, w, w, w]]

layout = Map(layout)

p1 = Submarine(layout, '1', '2', (0, 0))

p2 = Submarine(MapBlind(), '☠', '🍖', (0, 0))
p1.opponent = p2
import time
while True:
    p1.auto_move()
    p1.map._show()
    time.sleep(1)
    print()