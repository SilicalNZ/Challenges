data = """"""


import itertools

new_data = []
for line in data.split("\n"):
    a, b = line.split(" ")
    a = [True if i == "#" else False if i == "." else None for i in a]
    b = [int(i) for i in b.split(",")]
    c = []

    for x, i in enumerate(a):
        if i is None:
            c.append(x)

    new_data.append((a, b, c))

def nest(indexes: list[int], row: list[bool | None], matches: list[int], results: list[int]):
    current, next_indexes = indexes[0], indexes[1:]

    row[current] = True

    if not next_indexes:
        if [len(list(g)) for k, g in itertools.groupby(row) if k] == matches:
            results.append(1)
    else:
        nest(next_indexes, row, matches, results)

    row[current] = False

    if not next_indexes:
        if [len(list(g)) for k, g in itertools.groupby(row) if k] == matches:
            results.append(1)
    else:
        nest(next_indexes, row, matches, results)

result = 0
for a, b, c in new_data:
    results = []
    nest(c, a, b, results)
    result += sum(results)

print(result)
