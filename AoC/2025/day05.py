data = """"""


def solve() -> int:
    ranges = []
    result = 0
    fruit_zone = False

    for line in data.split("\n"):
        if line == "":
            fruit_zone = True
            continue

        if not fruit_zone:
            x, y = line.split("-")
            ranges.append([int(x), int(y)])
            continue

        for x, y in ranges:
            if x <= int(line) <= y:
                result += 1
                break

    return result

print(solve())

def solve2() -> int:
    the_list = []
    ranges = []
    result = 0

    for line in data.split("\n"):
        if line == "":
            break

        x0, y0 = line.split("-")
        the_list.append([int(x0), int(y0)])

    the_list.sort()

    for x0, y0 in the_list:
        print(x0, y0)
        for em, ranger in enumerate(ranges):
            print(ranger)

            x1, y1 = ranger

            if x1 <= x0 <= y1:
                if y0 >= y1:
                    ranges[em][1] = y0
                break
            elif x1 <= y0 <= y1:
                if x0 <= x1:
                    ranges[em][0] = x0
                break

        else:
            ranges.append([x0, y0])
        print()

    for x0, y0 in ranges:
        result += 1+y0-x0

    print(ranges)
    print(len(ranges))
    print()
    print()
    print()

    print(ranges)

    return result

print(solve2())
