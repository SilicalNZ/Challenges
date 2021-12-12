data = ""

z = tuple(zip(*data))


def manager(data, use_max=True):
    data_store = data
    for i in range(len(data)):
        i = data_store[i]
        zipped_data = tuple(zip(*data_store))

        if use_max:
            the_max = max(i, key=list(i).count)
        else:
            the_max = min(i, key=list(i).count)

        if len(i) / 2 == list(i).count(the_max):
            if use_max:
                the_max = 1
            else:
                the_max = 0

        new_data = []
        for x, j in enumerate(i):
            if j == the_max:
                new_data.append(zipped_data[x])

        if len(new_data) == 1:
            return new_data[0]

        data_store = tuple(zip(*new_data))

    return data_store


print(manager(z, use_max=True))
print(manager(z, use_max=False))
