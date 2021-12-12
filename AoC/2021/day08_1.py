import math

data = ""
data = tuple(tuple(map(int, i)) for i in data.split("\n"))


def find_zero(data):
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == 9:
                yield x, y


visited = []
height, width = len(data), len(data[0])


def cardinal_directions(x, y):
    return (
        (x, y - 1),
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
    )


def navigate(x, y, data, local_visited=None):
    if local_visited is None:
        local_visited = []

    # Faster to use try/except
    for i0, i1 in cardinal_directions(x, y):
        if width < i0 or i0 < 0 or height < i1 or i1 < 0:
            continue
        if (i0, i1) in local_visited:
            continue
        if (i0, i1) in visited:
            raise LookupError("Cannot reach inside of checked boundary")

        try:
            cell = data[i1][i0]
            if cell != 9:
                local_visited.append((i0, i1))
                navigate(i0, i1, data, local_visited)
        except IndexError:
            continue

    return local_visited


results = []
for i in find_zero(data):
    for j in cardinal_directions(*i):
        try:
            result = navigate(*j, data)
        except LookupError:
            continue
        if not result:
            continue

        visited.extend(result)
        results.append(result)

prod = []
for _ in range(3):
    t = max(results, key=len)
    results.remove(t)
    prod.append(len(t))

print(prod)
print(math.prod(prod))
