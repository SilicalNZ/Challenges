data = """"""

# Part 1
cycle, result, x_store = 0, 0, 1
for i in data.split("\n"):
    cycle += 1

    if (cycle - 20) % 40 == 0:
        result += cycle * x_store

    if i == "noop":
        continue

    cycle += 1

    if (cycle - 20) % 40 == 0:
        result += cycle * x_store

    x_store += int(i.split(" ")[-1])

print(result)


# Part 2
gen = lambda: ["." for _ in range(40)]

vamp = gen()
vamp = ["#"] * 3 + vamp[3:]
res = ""

cycle, x_store = -1, 1
for i in data.split("\n"):
    cycle += 1
    res += "#" if vamp[cycle % len(vamp)] == "#" else "."

    if i == "noop":
        continue

    cycle += 1
    res += "#" if vamp[cycle % len(vamp)] == "#" else "."

    x_store += int(i.split(" ")[-1])

    vamp = gen()
    for j in range(max(x_store - 1, 0), min(x_store + 2, len(vamp))):
        vamp[j] = "#"

[print(res[i:i+40]) for i in range(0, len(res), 40)]
