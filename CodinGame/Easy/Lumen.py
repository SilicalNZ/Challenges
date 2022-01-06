import random
from pprint import pprint


class Tile:
    __slots__ = ['name', 'graphic']

    def __init__(self, name, graphic):
        self.name = name
        self.graphic = graphic

    def attributes(self):
        return self.name, self.graphic


class Entity(Tile):
    __slots__ = ['tile', 'map', 'positions']

    def __init__(self, tile, map, positions):
        super().__init__(*tile.attributes())
        self.map = map
        self.positions = positions


class Map:
    def __init__(self, size):
        x, y, z = size
        self.size = size
        self.map = [[[[] for _ in range(z)] for _ in range(x)] for _ in range(y)]

    @classmethod
    def from_array(cls, array):
        instance = cls((0, 0, 0))
        instance.map = array
        instance.size = (len(array[0]), len(array), len(array[0][0]))
        return instance

    def valid_positions(self, position0, position1):
        pos = tuple(zip(position0, [i + 1 for i in position1]))

        valid_positions = []
        for y in range(*pos[1]):
            for x in range(*pos[0]):
                for z in range(*pos[2]):
                    if not self.map[y][x][z]:
                        valid_positions.append((x, y, z))
        return valid_positions

    def random_position(self, position0, position1):
        valid_positions = self.valid_positions(position0, position1)
        if valid_positions:
            return random.choice(valid_positions)

    def get_position(self, position):
        x, y, z = position
        return self.map[y][x][z]

    def add_tile(self, position, tile):
        x, y, z = position
        self.map[y][x][z] = tile

    def render(self):
        result0 = []
        for x in range(self.size[0]):
            result1 = []
            for z in range(self.size[2]):
                for y in range(self.size[1] - 1, -1, -1):
                    if self.map[y][x][z]:
                        result1.append(self.map[y][x][z][-1].graphic)
                        break
            result0.append(result1)
        return result0


class Sprite(Entity):
    directions = {'up': (0, 1, 0),
                  'down': (0, -1, 0),
                  'east': (0, 0, 1),
                  'west': (0, 0, -1),
                  'south': (1, 0, 0),
                  'north': (-1, 0, 0)}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.insert_onto_map()

    def move(self, direction):
        raise NotImplementedError

    def erase_from_map(self):
        for x, y, z in self.positions:
            while self in self.map.get_position((x, y, z)):
                self.map.map[y][x][z].remove(self)

    def insert_onto_map(self):
        print(self.positions)
        pending_funcs = []
        for x, y, z in self.positions:
            for tile in self.map.map[y][x][z]:
                if hasattr(tile, 'lock_and_key'):
                    pending_funcs.append(tile.lock_and_key(self))
            self.map.map[y][x][z].append(self)


class WinState(Exception):
    pass


class LossState(Exception):
    pass


class Player:
    def __init__(self, sprite):
        self.sprite = sprite
        self.current_direction = random.choice([self.sprite.directions])

    def move(self, direction):
        self.sprite.move(direction)
        self.current_direction = direction


"""
S N A K E   G A M E
"""

Floor = Tile('floor', '▪')
Apple = Tile('fruit', '🍎')
SnakeHead = Tile('snake_head', '🐍')
SnakeField = Map.from_array([[[[Floor] for _ in range(3)] for _ in range(3)], [[[] for _ in range(3)] for _ in range(3)]])


class Snake(Sprite):
    directions = Sprite.directions.copy()
    directions.pop('up')
    directions.pop('down')

    opposite_directions = {'north': 'south',
                           'south': 'north',
                           'east': 'west',
                           'west': 'east'}

    def __init__(self, positions, map, tile=None):
        tile = SnakeHead if tile is None else tile
        super().__init__(tile, map, positions)
        self.tail = None
        self.current_direction = random.choice([self.directions.keys()])

    def lengthen(self):
        self.positions.append(self.tail)
        self.tail = None

    def move(self, direction):
        if self.current_direction == self.opposite_directions[direction]:
            return
        self.current_direction = direction
        direction = self.directions[direction]
        positions = self.positions[:-1]
        self.tail = self.positions[-1]
        new_pos = self.positions[0]
        new_pos = tuple(map(sum, zip(direction, new_pos)))

        self.erase_from_map()
        self.positions = [new_pos] + positions
        self.insert_onto_map()

    def lock_and_key(self, sprite):
        if isinstance(sprite, Snake):
            raise LossState()


class Fruit(Sprite):
    def __init__(self, positions, map, tile=None):
        tile = Apple if tile is None else tile
        super().__init__(tile, map, positions)

        self.directions = super().directions.copy()
        delattr(self, 'directions')

    def move(self, direction):
        result = self.map.random_position((0, 1, 0), (self.map.size[0] - 1, 1, self.map.size[2] - 1))
        if result is None:
            raise WinState
        else:
            self.positions = [result]
        self.insert_onto_map()

    def lock_and_key(self, sprite):
        if isinstance(sprite, Snake):
            self.erase_from_map()
            sprite.lengthen()
            self.move('Doesn\'t matter')


if __name__ == '__main__':
    snake = Snake([SnakeField.random_position((0, 1, 0), (2, 1, 2))], SnakeField)
    snake = Player(snake)

    Fruit([SnakeField.random_position((0, 1, 0), (2, 1, 2))], SnakeField)
    pprint(SnakeField.render())

    while True:

        snake.move(input('Direction: '))
        [print(i) for i in SnakeField.render()]
