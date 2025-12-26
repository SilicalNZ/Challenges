data = """"""

def solve() -> int:
    invalid = 0

    for ids in data.strip("\n").split(","):
        first, last = ids.split("-")

        for i in range(int(first), int(last) + 1):
            str_i = str(i)
            len_str_id = len(str_i)

            if len_str_id % 2 != 0:
                continue

            half_len_str_id = len_str_id // 2

            if str_i[:half_len_str_id] == str_i[half_len_str_id:]:
                invalid += i

    return invalid


print(solve())

def solve_2() -> int:
    invalid = 0

    for ids in data.strip("\n").split(","):
        first, last = ids.split("-")

        for i in range(int(first), int(last) + 1):
            str_i = str(i)
            len_str_id = len(str_i)
            #print(i)

            for j in range(1, len_str_id//2+1):
                # print(set(zip(*([iter(str_i)] * j))))
                if len_str_id % j != 0:
                    continue

                if len(set(zip(*([iter(str_i)] * j), strict=True))) == 1:
                    invalid += i
                    break

    return invalid

print(solve_2())