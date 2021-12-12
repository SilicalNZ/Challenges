data = ""
data = tuple(tuple(map(int, i)) for i in data.split("\n"))


result = 0
for y, row in enumerate(data):
    for x, cell in enumerate(row):
        if x - 1 >= 0 and row[x - 1] <= cell:
            continue
        if x + 1 < len(row) and row[x + 1] <= cell:
            continue
        if y - 1 >= 0 and data[y - 1][x] <= cell:
            continue
        if y + 1 < len(data) and data[y + 1][x] <= cell:
            continue

        result += cell + 1