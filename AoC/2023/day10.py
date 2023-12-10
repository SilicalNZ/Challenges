data = """"""

coord = tuple[int, int]

board = [list(i) for i in data.split("\n")]

directions = (0, -1), (1, 0), (0, 1), (-1, 0)
north, east, south, west = directions

connectors = {
    "|": (north, south),
    "-": (east, west),
    "L": (north, east),
    "J": (north, west),
    "7": (south, west),
    "F": (east, south),
}

def within_board_range(x: int, y: int) -> bool:
    return x >= 0 and x < len(board[0]) and y >= 0 and y < len(board)

def combine_positions(pos0: coord, pos1: coord) -> coord:
    return pos0[0] + pos1[0], pos0[1] + pos1[1]

def next_connection(org_pos: coord, value: str, value_pos: coord) -> coord | None:
    positions = connectors[value]

    for x, pos in enumerate(positions):
        if combine_positions(value_pos, pos) == org_pos:
            return combine_positions(value_pos, positions[x-1])

def find_next_move() -> tuple[coord, coord, str]:
    for y, i in enumerate(board):
        try:
            x = i.index("S")
            break
        except ValueError:
            continue

    start = (x, y)

    connections = []
    start_connections = []

    for direction in directions:
        a, b = combine_positions(start, direction)
        if not within_board_range(a, b):
            continue

        pos = board[b][a]

        if pos == ".":
            continue

        res = next_connection(start, pos, (a, b))

        if res is not None:
            connections.append((a - start[0], b - start[1]))
            start_connections.append(((a, b), res))

    for key, value in connectors.items():
        if value == tuple(connections):
            return start_connections[0][0], start_connections[0][1], key

current_pos, next_pos, start_replace = find_next_move()

steps = 1

new_board = [["." for _ in range(len(board[0]))] for _ in range(len(board))]

while True:
    steps += 1

    value = board[next_pos[1]][next_pos[0]]
    new_board[current_pos[1]][current_pos[0]] = board[current_pos[1]][current_pos[0]]

    if value == "S":
        new_board[next_pos[1]][next_pos[0]] = start_replace
        break

    current_pos, next_pos = next_pos, next_connection(current_pos, value, next_pos)

print(steps // 2)

result_board = [["." for _ in range(len(board[0]))] for _ in range(len(board))]

skip = "-"
counter = 0
for y, i in enumerate(new_board):
    in_pipe = False
    last_corner = "."

    for x, j in enumerate(i):

        if j == "L":
            in_pipe = not in_pipe
            last_corner = "L"
        elif j == "F":
            in_pipe = not in_pipe
            last_corner = "F"
        elif j == "J":
            if last_corner != "F":
                in_pipe = not in_pipe
            last_corner = "J"
        elif j == "7":
            if last_corner != "L":
                in_pipe = not in_pipe
            last_corner = "7"
        elif j == "|":
            in_pipe = not in_pipe
            last_corner = "."
        elif j == "." and not in_pipe:
            result_board[y][x] = "X"
        elif j == "." and in_pipe:
            counter += 1

        previous = j

print(counter)
