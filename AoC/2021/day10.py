import pprint

data = ""
data = [list(map(int, i)) for i in data.split("\n")]

print(data)


def increment(data):
    for y, row in enumerate(data):
        for x, _ in enumerate(row):
            data[y][x] += 1


def cardinal_directions(x, y):
    return (
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
        (x + 1, y - 1),
        (x + 1, y + 1),
        (x - 1, y + 1),
        (x - 1, y - 1),
    )


width, height = len(data[0]) - 1, len(data) - 1


def flash(data):
    flash_occurred = False
    for y, row in enumerate(data):
        for x, _ in enumerate(row):
            cell = data[y][x]
            if cell < 10:
                continue

            data[y][x] = 0
            flash_occurred = True
            for i0, i1 in cardinal_directions(x, y):
                if width < i0 or i0 < 0 or height < i1 or i1 < 0:
                    continue


                cell = data[i1][i0]

                if cell == 0:
                    continue
                else:
                    data[i1][i0] += 1

    return flash_occurred


def iterate(data):
    increment(data)

    finished = False
    while not finished:
        finished = not flash(data)

    pprint.pprint(data)


def count_flashes(data):
    result = 0
    for i in data:
        for j in i:
            if j == 0:
                result += 1

    return result


def all_flashes(data):
    return sum(map(sum, data)) == 0


def counter(data):
    ct = 0
    while True:
        ct += 1
        iterate(data)
        if all_flashes(data):
            return ct


print(counter(data))
