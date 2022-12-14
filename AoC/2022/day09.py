data = """"""

part1 = 2
part2 = 10

knots = [[10, 10] for _ in range(part2)]
log = {(10, 10), }
res = [(i.split(" ")[0], int(i.split(" ")[1])) for i in data.split("\n")]
direct = [{"R": 1, "L": -1}, {"U": 1, "D": -1}]
movement = {2: 1, -2: -1}

for dir, ct in res:
    for _ in range(ct):
        knots[0][0] += direct[0].get(dir, 0)
        knots[0][1] += direct[1].get(dir, 0)

        for tailing, knot in zip(knots[:-1], knots[1:]):
            x_diff = tailing[0] - knot[0]
            y_diff = tailing[1] - knot[1]

            if abs(x_diff) >= 2 or abs(y_diff) >= 2:
                knot[0] += movement.get(x_diff, x_diff)
                knot[1] += movement.get(y_diff, y_diff)

        log.add(tuple(knots[-1]))

print(len(log))
