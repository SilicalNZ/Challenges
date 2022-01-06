import sys
import math


def printf(*args):
    print(*args, file=sys.stderr, flush=True)


class Tile:
    char = ' '
    def __init__(self, char=None):
        self.char = char if char else self.char

    def __repr__(self):
        return repr(self.char)

    def __str__(self):
        return str(self.char)


class Hole(Tile):
    def __init__(self, char='O'):
        super().__init__(char)
        self.state = False

    def __setitem__(self, key, value):
        self.state = value

    def __bool__(self):
        return self.state


class Ore(Tile):
    def __init__(self, char='Z'):
        super().__init__(char)
        self.state = 0
        self.noticed = False

    def __setitem__(self, key, value):
        if value != '?':
            self.noticed = False
            self.state = int(value)

    def __bool__(self):
        return self.state and self.noticed


class Cell:
    def __init__(self, object, position):
        self.stack = object
        self.position = position
        self.hole = Hole()
        self.ore = Ore()

    def remove(self, object):
        self.stack.remove(object)

    def append(self, object):
        if self.exec_condition(object):
            self.stack.append(object)
            return True
        return False

    def retrieve(self, object):
        container = []
        for item in self:
            if item == object:
                return item
            if item.__class__ == object:
                container.append(item)
        return item

    def __iter__(self):
        yield from self.stack

    def __eq__(self, other):
        return other in self.stack or any(i .__class__ == other for i in self)

    def __getattr__(self, item):
        return getattr(self.stack, item)

    def top(self):
        return self.stack[-1]

    def show(self):
        return self.top.show()

    def wipe(self):
        self.stack = [self.stack[0]]


class Area:
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
        yield from [self._data[y][x] for x, y in self.get_positions()]


class Layout(Area):
    def __init__(self, data):
        self.data = [[Stacker(x, (x0, y0)) for x0, x in enumerate(y)] for y0, y in enumerate(data)]

    def __setitem__(self, key, value):
        self.handle_outofbounds(key)
        x, y = key
        self._data[y][x].append(value)

    def insert(self, position, object):
        self[position] = object

    def retrieve(self, position, object):
        return self[position].retrieve(object)

    def __getitem__(self, key):
        self.handle_outofbounds(key)
        x, y = key
        return self._data[y][x]

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
        return cls([[default for x in y] for y in size])

    def wipe(self):
        for cell in self.get_data():
            cell.wipe()


class MovingTile(Tile):
    def __init__(self, layout, position, char=None):
        super().__init__(char)
        self.prev_position = None
        self.position = position
        self.layout = layout

    def update_layout(self):
        if self.prev_position:
            self.layout.remove(self.prev_position, self.__class__)
        self.layout.insert(self.position, self)

    @property
    def position(self):
        return self._position

    def _position_setter(self, value):
        self.prev_position = self._position
        self._position = value
        self.update_layout()

    @position.setter
    def position(self, value):
        self._position_setter(value)


class Entity(MovingTile):
    items = {-1: None, 2: 'radar', 3: 'trap', 4: 'ore'}
    def __init__(self, id, item, layout, position, char=None):
        super().__init__(layout, position)
        self.id = id
        self.item = items[item]


class Radar(Entity):
    char = 'R'


class Trap(Entity):
    char = 'T'


class Robot(Entity):
    char = '>'

    def __init__(self, id, item, layout, position, char=None):
        super().__init__(self, layout, position, char=None)
        self.id = id

    def wait(self):
        print('WAIT')

    def move(self, position):
        x, y = position
        print(f'MOVE {x} {y}')

    def dig(self, position):
        x, y = position
        print(f'DIG {x} {y}')

    def request(self, item):
        print(f'REQUEST {item.upper()}')


class Player:
    def __init__(self, layout):
        self.score = None
        self._units = {}
        self.radar_cooldown = 0
        self.trap_cooldown = 0
        self.layout = layout

    def __getitem__(self, item):
        return self._units[item]

    def pop(self, value):
        self._units.pop(value)

    @property
    def units(self):
        return self._units.values()

    def __iter__(self):
        yield from self.units

    def __call__(self, id, item, position, layout):
        self._units[id] = Entity(id, item, layout, position)


class ParseInput:
    def __init__(self):
        self.layout = None
        self.p1 = Player()
        self.p2 = Player()
        self.entities = {0: self.p1, 1: self.p2, 2: Radar, 3: Trap}
        self.width, self.length = None, None

    def _input(self):
        return [*map(int, input().split())]

    def update_area(self):
        self.width, self.height = self._input()

    def reset_layout(self):
        self.layout = Layout.from_size(Tile())

    def update_layout(self):
        for y in (self.layout.length):
            inputs = input().split()
            for x in range(self.layout.width):
                self.layout[(x, y)].ore = inputs[2*x]
                self.layout[(x, y)].hole = int(inputs[2*x+1])

    def update_entity(self):
        entity_id, entity_type, x, y, item = self._input()
        self.entities[entity_type](entity_id, item, (x, y), self.layout)

    def operate(self, i):
        self.p1[i].operate()

    def run(self):
        self.update_area()
        while True:
            self.reset_layout()
            self.update_layout()
            self.p1.score, self.p2.score, self._input()
            entities, self.p1.radar_cooldown, self.p1.trap_cooldown = self._input()
            for _ in range(entity_count):
                self.update_entity()

        for i in range(5):
            self.operate(i)


if __name__ == '__main__':
    ParseInput().run()
