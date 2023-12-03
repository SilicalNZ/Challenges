data = """"""


lines = data.split("\n")
x_size, y_size = len(lines) - 1, len(lines[0]) - 1
offsets = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1)]
numbers = []
gears: dict[tuple[int, int], list[int, int]] = {}


def is_number(number: str, is_part: bool, gear: tuple):
    if number and is_part:
        int_number = int(number)
        numbers.append(int_number)

        if gear:
            if gear not in gears:
                gears[gear] = [int_number]
            else:
                gears[gear].append(int_number)

for y, line in enumerate(lines):
    number = ""
    is_part = False
    gear = ()

    for x, char in enumerate(line):
        if char.isdigit():
            number += char
        else:
            is_number(number, is_part, gear)

            number = ""
            is_part = False
            gear = ()
            continue

        if is_part:
            continue

        for offset_x, offset_y in offsets:
            new_x = offset_x + x
            new_y = offset_y + y

            if 0 <= new_y <= y_size and 0 <= new_x <= x_size:
                maybe_part = lines[new_y][new_x]
                if maybe_part != "." and not maybe_part.isdigit():
                    is_part = True

                    if maybe_part == "*":
                        gear = new_x, new_y

                    break

    if number and is_part:
        is_number(number, is_part, gear)

print(sum(numbers))

res = 0
for numbers in gears.values():
    if len(numbers) != 2:
        continue

    res += numbers[0] * numbers[1]

print(res)
