data = """"""

def find_match(rows) -> int | None:
    for i in range(1, len(rows)):
        a, b = rows[:i], rows[i:]

        small = min(len(a), len(b))

        a, b = rows[i-small:i], rows[i:i+small]
        a.reverse()

        if a == b:
            return i

result = 0
for land in data.split("\n\n"):
    rows = [row for row in land.split("\n")]

    res = find_match(rows)
    if res is not None:
        result += 100 * res
        continue

    rows = list(zip(*rows))

    res = find_match(rows)
    assert res is not None

    result += res

print(result)
