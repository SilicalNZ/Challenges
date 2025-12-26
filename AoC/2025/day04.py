data = """"""

SYMBOL = "@"
EMPTY = "."
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

def solve():
    mappy = [list(i) for i in data.split("\n")]
    result = 0

    for row, line in enumerate(mappy):
        for column, cell in enumerate(line):
            if cell != SYMBOL:
                continue

            adjacent = sum([mappy[row+x][column+y] == SYMBOL for x, y in DIRECTIONS if row+x < len(mappy) and row+x >= 0 and column+y < len(mappy[0]) and column+y >= 0])
            if adjacent <= 3:
                result += 1

    return result

print(solve())

def solve2():
    mappy = [list(i) for i in data.split("\n")]
    removed = 0
    while True:
        can_remove = []

        for row, line in enumerate(mappy):
            for column, cell in enumerate(line):
                if cell != SYMBOL:
                    continue

                adjacent = sum([mappy[row+x][column+y] == SYMBOL for x, y in DIRECTIONS if row+x < len(mappy) and row+x >= 0 and column+y < len(mappy[0]) and column+y >= 0])
                if adjacent <= 3:
                    can_remove.append((row, column))
                    removed += 1

        if not can_remove:
            break

        for remove in can_remove:
            mappy[remove[0]][remove[1]] = EMPTY

    return removed

print(solve2())

