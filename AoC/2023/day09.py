data = """"""


def worker(values: list[int]) -> list[int]:
    result = []

    for a, b in zip(values, values[1:]):
        result.append((a - b)*-1)

    return result

res_to_add = 0
res_to_take = 0
for i in data.split("\n"):
    results = []

    values = list(map(int, i.split(" ")))
    results.append(values)

    while True:
        result = worker(results[-1])

        if not any(result):
            to_add = 0
            for j in reversed(results):
                to_add += j[-1]

            to_take = 0
            for j in reversed(results):
                to_take = j[0] - to_take

            res_to_add += to_add
            res_to_take += to_take

            break
        else:
            results.append(result)

print(res_to_add)
print(res_to_take)