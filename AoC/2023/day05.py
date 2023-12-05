data = """"""

seeds = tuple(map(int, data.split("\n")[0].split(": ")[-1].split(" ")))
converted = [[i] for i in seeds]

converters = data.split("\n\n")[1:]
for y, converter in enumerate(converters):
    map_type, ranges = converter.split(":\n")

    for x, seed in enumerate(converted):
        matched = False
        for ranger in ranges.split("\n"):
            destination, source, length = map(int, ranger.split(" "))

            if source <= seed[y] <= source + length:
                converted[x].append(destination + abs(source - seed[y]))
                matched = True
                break

        if not matched:
            converted[x].append(seed[y])

print(min(i[-1] for i in converted))

seeds = tuple(map(int, data.split("\n")[0].split(": ")[-1].split(" ")))
pairs = tuple(zip(seeds[::2], seeds[1::2]))
converters = tuple([tuple(map(int, j.split(" "))) for j in converter.split(":\n")[-1].split("\n")] for converter in data.split("\n\n")[1:])


def worker(pair: tuple[int, int], conversion: tuple[int, int, int]):
    pair_source, pair_length = pair
    pair_bound = pair_source+pair_length - 1
    destination, source, length = conversion
    destination_bound, source_bound = destination + length - 1, source + length - 1

    if pair_source > source_bound or pair_bound < source:
        return

    if pair_source >= source and pair_bound <= source_bound:
        return (), (destination+pair_source-source, min(length, pair_length))

    if pair_source < source:
        difference = source-pair_source

        extra, result = worker((source, pair_length-difference), conversion)

        return ((pair_source, difference), *extra), result

    if pair_bound > source_bound:
        difference = pair_bound-source_bound

        extra, result = worker((pair_source, pair_length-difference), conversion)

        return ((source_bound, difference), *extra), result

    assert 1 == 2


for converter in converters:
    results = []
    new_pairs = []

    for conversion in converter:
        new_pairs = []

        for pair in pairs:
            result = worker(pair, conversion)
            if result is None:
                new_pairs.append(pair)
                continue

            extracted, converted = result

            new_pairs.extend(extracted)
            results.append(converted)

        pairs = tuple(new_pairs)

    results.extend(new_pairs)
    pairs = tuple(results)

print(min(x for x, _ in pairs))
