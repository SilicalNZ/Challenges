data = """"""

import math

time, distance = [[int(j) for j in i.split(":")[1].split(" ") if j] for i in data.split("\n")]
x, y = [int(i.split(":")[1]) for i in data.replace(" ", "").split("\n")]
time.append(x)
distance.append(y)
results = []

for a, b in zip(time, distance):
    options = 0
    for i in range(a//2, a+1):
        given_distance = i * (a-i)
        if given_distance > b:
            options += 1
        else:
            break
    for i in range(a//2-1, 0, -1):
        given_distance = i * (a-i)
        if given_distance > b:
            options += 1
        else:
            break
    results.append(options)


print(math.prod(results[:-1]))
print(results[-1])
