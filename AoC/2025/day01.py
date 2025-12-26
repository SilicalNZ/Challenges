data = """"""


def solve() -> tuple[int, int]:
    position = 50
    end = 99
    end_plus_one = end + 1
    part_1 = 0
    part_2 = 0

    for lines in data.split("\n"):
        direction, number = 1 if lines[0] == "R" else -1, int(lines[1:])
        loops = number // end_plus_one
        number -= loops * end_plus_one

        part_2 += loops

        prev_position = position
        position += direction * number
        if position < 0:
            position += end_plus_one

            if prev_position != 0:
                part_2 += 1

        elif position > end:
            part_2 += 1
            position -= end_plus_one
        elif position == 0:
            part_2 += 1


        if position == 0:
            part_1 += 1

    return part_1, part_2

print(solve())