data = """"""


def expand_board(original_board):
    expansion = []

    for x, line in enumerate(original_board):
        if all(i == "." for i in line):
            expansion.append(x)

    return expansion


def prepare_board(board):
    y_expansion = expand_board(board)

    board = list(zip(*board))

    x_expansion = expand_board(board)

    return x_expansion, y_expansion

def find_galaxies(board) -> list[tuple[int, int]]:
    galaxies: list[tuple[int, int]] = []

    for y, line in enumerate(board):
        for x, val in enumerate(line):
            if val == "#":
                galaxies.append((x, y))

    return galaxies

def galaxy_distances(galaxies, x_expansion, y_expansion, expansion_val):
    distances = 0

    for itr, galaxy in enumerate(galaxies[:-1], 1):
        x0, y0 = galaxy

        for x1, y1 in galaxies[itr:]:
            start, end = min(x0, x1), max(x0, x1)
            mult = 0
            for a in range(start, end + 1):
                if a in x_expansion:
                    mult += 1

            start, end = min(y0, y1), max(y0, y1)
            for a in range(start, end + 1):
                if a in y_expansion:
                    mult += 1

            distances += abs(x0 - x1) + abs(y0 - y1) - mult + mult * expansion_val

    return distances


board = list(map(list, data.split("\n")))
x_expansion, y_expansion = prepare_board(board)
galaxies = find_galaxies(board)
print(galaxy_distances(galaxies, x_expansion, y_expansion, 2))
print(galaxy_distances(galaxies, x_expansion, y_expansion, 1_000_000))
